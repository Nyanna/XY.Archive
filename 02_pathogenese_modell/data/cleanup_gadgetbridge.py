#!/usr/bin/env python3
"""
Gadgetbridge SQLite -> Postgres Replication
--------------------------------------------
Downloads the Gadgetbridge SQLite database if missing or stale, refreshes
the derived HRV_MINUTE_AGGREGATED table, and replicates every non-empty
SQLite table into a local Postgres instance. The source SQLite database
is never modified by this script.

Column names and types are preserved verbatim from the source (INTEGER
is mapped to BIGINT because Postgres INTEGER is 32-bit and would
overflow on millisecond timestamps; REAL is mapped to DOUBLE PRECISION
and BLOB to BYTEA for semantic equivalence).

Every INTEGER column that holds a point in time (Unix epoch, ms or s)
is replaced in Postgres by a single TIMESTAMPTZ column named
`<original_lowercase>_at`. The bigint variant is not replicated, so
the target schema only carries the canonical timestamptz form. The
unit (ms vs. seconds) is detected from the raw value's magnitude:
values <= 10^11 are treated as seconds (covers BATTERY_LEVEL,
XIAOMI_ACTIVITY_SAMPLE), larger values as milliseconds.

Idempotent: database / schema / tables / columns are created on demand,
rows are upserted via INSERT ... ON CONFLICT on each table's primary key.
Tables without a primary key are fully replaced (TRUNCATE + INSERT).
"""

import argparse
import os
import re
import runpy
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import gdown
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

# --- Source -----------------------------------------------------------
DB_PATH = Path(__file__).parent / "Gadgetbridge"
DB_REMOTE_URL = "https://drive.google.com/uc?id=1NwUmQ_v7WOQIe5tYm2GixOQYm5HSt-xh"
EXPIRY_SECONDS = 1 * 3600

# --- Postgres target --------------------------------------------------
PG_HOST = os.environ["PGHOST"]
PG_PORT = int(os.environ.get("PGPORT", "5432"))
PG_DB = os.environ["PGDATABASE"]
PG_USER = os.environ.get("PGUSER", "gadgetbridge")
PG_PASSWORD = os.environ["PGPASSWORD"]
PG_SCHEMA = "public"

BATCH_SIZE = 5000

# --- Timestamp column detection --------------------------------------
TIMESTAMP_PATTERNS = [
    r"^TIMESTAMP$",
    r"^TIMESTAMP_MS$",
    r"^TIMESTAMP_FROM$",
    r"^TIMESTAMP_TO$",
    r".*_TIMESTAMP$",
    r"^DOWNLOAD_TIMESTAMP$",
    r"^FILE_TIMESTAMP$",
    r"^LAST_SYNC_TIMESTAMP$",
    r"^START_TIME$",
    r"^END_TIME$",
    r"^WAKEUP_TIME$",
    r"^BED_TIME$",
    r"^RISING_TIME$",
    r"^PREPARE_SLEEP_TIME$",
    r"^LAST_UPDATE_CHECK$",
    r"^LAST_TIMESTAMP$",
    r"^OTHER_TIMESTAMP$",
    r"^DATE$",
    r"^END_TIMESTAMP$",
    r"^START_TIMESTAMP$",
    r"^MODIFY_TIMESTAMP$",
]

EXCLUDE_PATTERNS = [
    r".*_MINUTES$",
    r"^TIMEZONE$",
    r"^TIME_LOW$",
    r"^TIME_MODERATE$",
    r"^TIME_HIGH$",
    r"^TOTAL_TIME$",
    r"^RECOVERY_TIME$",
    r"^GROUND_CONTACT_TIME$",
    r"^HANG_TIME$",
    r"^DIVING_UNDERWATER_TIME$",
    r"^DIVING_BREAK_TIME$",
    r"^TIME_DELTA$",
    r"^RUN_PACE_ZONE\d+_TIME$",
    r"^UPDATE_AVAILABLE$",
    r"^TIME$",
]


def is_timestamp_column(col_name: str) -> bool:
    name = col_name.upper()
    for pat in EXCLUDE_PATTERNS:
        if re.match(pat, name):
            return False
    for pat in TIMESTAMP_PATTERNS:
        if re.match(pat, name):
            return True
    return False


# --- Type mapping SQLite -> Postgres ---------------------------------
SQLITE_TO_PG = {
    "INTEGER": "BIGINT",
    "INT": "BIGINT",
    "BIGINT": "BIGINT",
    "SMALLINT": "SMALLINT",
    "TINYINT": "SMALLINT",
    "TEXT": "TEXT",
    "VARCHAR": "TEXT",
    "CHAR": "TEXT",
    "CLOB": "TEXT",
    "STRING": "TEXT",
    "REAL": "DOUBLE PRECISION",
    "DOUBLE": "DOUBLE PRECISION",
    "FLOAT": "DOUBLE PRECISION",
    "NUMERIC": "NUMERIC",
    "DECIMAL": "NUMERIC",
    "BOOLEAN": "BOOLEAN",
    "BLOB": "BYTEA",
    "DATE": "DATE",
    "DATETIME": "TIMESTAMPTZ",
    "TIMESTAMP": "TIMESTAMPTZ",
}


def sqlite_type_to_pg(sqlite_type: str) -> str:
    if not sqlite_type:
        return "TEXT"
    base = re.match(r"^([A-Za-z]+)", sqlite_type.strip())
    if not base:
        return "TEXT"
    return SQLITE_TO_PG.get(base.group(1).upper(), "TEXT")


# Unix-epoch values <= 10^11 are seconds (year 5138 max), values
# above are milliseconds (lower bound year 2001). All Gadgetbridge
# raw timestamps fall comfortably outside the ambiguous band.
_EPOCH_MS_THRESHOLD = 100_000_000_000


def epoch_to_ts(v):
    if v is None:
        return None
    secs = v / 1000.0 if v >= _EPOCH_MS_THRESHOLD else float(v)
    return datetime.fromtimestamp(secs, tz=timezone.utc)


def ts_at_name(col_name):
    return f"{col_name.lower()}_at"


# --- Download --------------------------------------------------------
def download_db():
    gdown.download(DB_REMOTE_URL, str(DB_PATH), quiet=False)


# --- SQLite introspection --------------------------------------------
def get_user_tables(conn):
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    return [r[0] for r in rows if not r[0].startswith("sqlite_")]


def table_row_count(conn, table):
    return conn.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0]


def get_columns(conn, table):
    # (cid, name, type, notnull, dflt_value, pk)
    return conn.execute(f"PRAGMA table_info([{table}])").fetchall()


def get_primary_key(columns):
    pks = [c for c in columns if c[5] > 0]
    return [c[1] for c in sorted(pks, key=lambda c: c[5])]


# --- Postgres helpers ------------------------------------------------
def ensure_database():
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD,
        dbname=PG_DB, sslmode="require",
    )
    conn.autocommit = True
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (PG_DB,))
        if cur.fetchone() is None:
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(PG_DB))
            )
            print(f"Created Postgres database: {PG_DB}")
    finally:
        conn.close()


def connect_target():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD,
        dbname=PG_DB, sslmode="require",
    )


def ensure_schema(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute(
            sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                sql.Identifier(PG_SCHEMA)
            )
        )
    pg_conn.commit()


def ensure_table(pg_conn, table_name, columns, pk_cols, ts_cols):
    """Create or extend the target table.

    Bigint timestamp columns (members of `ts_cols`) are NOT replicated
    as raw integers; instead a TIMESTAMPTZ `<col>_at` column is created
    and used as the canonical timestamp. PK references to a ts_col are
    rewritten to its `_at` counterpart.
    """
    ts_set = set(ts_cols)
    pk_set = set(pk_cols)
    pg_pk_cols = [ts_at_name(c) if c in ts_set else c for c in pk_cols]
    pg_pk_set = set(pg_pk_cols)

    col_defs = []
    for c in columns:
        name = c[1]
        if name in ts_set:
            continue   # bigint ts columns are no longer materialised
        notnull = c[3]
        pg_type = sqlite_type_to_pg(c[2])
        parts = [sql.Identifier(name), sql.SQL(pg_type)]
        # PK columns are implicitly NOT NULL in PG; avoid redundant clause.
        if notnull and name not in pg_pk_set:
            parts.append(sql.SQL("NOT NULL"))
        col_defs.append(sql.SQL(" ").join(parts))

    for ts_col in ts_cols:
        at_name = ts_at_name(ts_col)
        # Source bigint was NOT NULL for every observed ts column; PK ts
        # cols are implicitly NOT NULL. Mark non-PK explicitly.
        parts = [sql.Identifier(at_name), sql.SQL("TIMESTAMPTZ")]
        if at_name not in pg_pk_set:
            parts.append(sql.SQL("NOT NULL"))
        col_defs.append(sql.SQL(" ").join(parts))

    if pg_pk_cols:
        col_defs.append(
            sql.SQL("PRIMARY KEY ({})").format(
                sql.SQL(", ").join(sql.Identifier(c) for c in pg_pk_cols)
            )
        )

    create_stmt = sql.SQL("CREATE TABLE IF NOT EXISTS {}.{} ({})").format(
        sql.Identifier(PG_SCHEMA),
        sql.Identifier(table_name),
        sql.SQL(", ").join(col_defs),
    )

    with pg_conn.cursor() as cur:
        cur.execute(create_stmt)

        # Handle schema drift: add any missing columns (without NOT NULL).
        # information_schema.columns.column_name preserves case for quoted
        # identifiers, so compare case-sensitively.
        cur.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            """,
            (PG_SCHEMA, table_name),
        )
        existing = {r[0] for r in cur.fetchall()}

        for c in columns:
            name = c[1]
            if name in ts_set or name in existing:
                continue
            pg_type = sqlite_type_to_pg(c[2])
            cur.execute(
                sql.SQL("ALTER TABLE {}.{} ADD COLUMN {} {}").format(
                    sql.Identifier(PG_SCHEMA),
                    sql.Identifier(table_name),
                    sql.Identifier(name),
                    sql.SQL(pg_type),
                )
            )
            existing.add(name)

        for ts_col in ts_cols:
            at_name = ts_at_name(ts_col)
            if at_name in existing:
                continue
            cur.execute(
                sql.SQL(
                    "ALTER TABLE {}.{} ADD COLUMN {} TIMESTAMPTZ"
                ).format(
                    sql.Identifier(PG_SCHEMA),
                    sql.Identifier(table_name),
                    sql.Identifier(at_name),
                )
            )
            existing.add(at_name)
    pg_conn.commit()


def get_target_max(pg_conn, table_name, col_name):
    """Max value of a target column, or None if target is empty/missing.
    Errors (missing table, missing column) are swallowed so first-run
    semantics fall back to a full load.
    """
    try:
        with pg_conn.cursor() as cur:
            cur.execute(
                sql.SQL("SELECT MAX({}) FROM {}.{}").format(
                    sql.Identifier(col_name),
                    sql.Identifier(PG_SCHEMA),
                    sql.Identifier(table_name),
                )
            )
            row = cur.fetchone()
            return row[0] if row else None
    except psycopg2.Error:
        pg_conn.rollback()
        return None


def replicate_table(sqlite_conn, pg_conn, table_name, force=False):
    columns = get_columns(sqlite_conn, table_name)
    pk_cols = get_primary_key(columns)
    ts_cols = [
        c[1] for c in columns
        if (c[2] or "").upper().startswith("INT")
        and is_timestamp_column(c[1])
    ]
    ts_set = set(ts_cols)

    ensure_table(pg_conn, table_name, columns, pk_cols, ts_cols)

    # PG-side PK: bigint ts cols are stored as their _at counterpart.
    pg_pk_cols = [ts_at_name(c) if c in ts_set else c for c in pk_cols]

    # Incremental watermark: if the first PK column was a bigint
    # timestamp, query MAX(<col>_at) on the target (timestamptz). The
    # SQLite source still stores the raw integer; convert the datetime
    # back into the source's native unit for the WHERE filter. `>=`
    # ensures boundary rows (composite PK ties) are re-upserted.
    watermark_col = None       # SQLite source column
    watermark_sqlite = None    # value in SQLite source unit (int)
    watermark_dt = None        # datetime, for log output
    if not force and pk_cols:
        first = pk_cols[0]
        first_info = next(c for c in columns if c[1] == first)
        first_type = (first_info[2] or "").upper()
        if first_type.startswith("INT") and is_timestamp_column(first):
            target_max = get_target_max(
                pg_conn, table_name, ts_at_name(first)
            )
            if target_max is not None:
                watermark_col = first
                watermark_dt = target_max
                # Probe one row to detect SQLite's native unit (ms vs s).
                probe = sqlite_conn.execute(
                    f"SELECT [{first}] FROM [{table_name}] "
                    f"WHERE [{first}] IS NOT NULL LIMIT 1"
                ).fetchone()
                if probe is None:
                    watermark_col = None
                else:
                    sample = probe[0]
                    epoch_ms = int(target_max.timestamp() * 1000)
                    if sample >= _EPOCH_MS_THRESHOLD:
                        watermark_sqlite = epoch_ms
                    else:
                        watermark_sqlite = epoch_ms // 1000

    # Postgres-side column order: non-ts source columns followed by
    # the derived _at columns. The bigint ts cols themselves are
    # dropped from the projection.
    keep_indices = [i for i, c in enumerate(columns) if c[1] not in ts_set]
    keep_names = [columns[i][1] for i in keep_indices]
    at_names = [ts_at_name(t) for t in ts_cols]
    ts_indices = [next(i for i, c in enumerate(columns) if c[1] == t)
                  for t in ts_cols]

    # SQLite stores BOOLEAN columns as 0/1 integers; Postgres bool is
    # strict and rejects integer literals, so convert in Python.
    bool_indices = [
        i for i, c in enumerate(columns)
        if (c[2] or "").upper().startswith("BOOL")
    ]
    bool_keep_positions = [
        keep_indices.index(i) for i in bool_indices if i in keep_indices
    ]

    all_cols = keep_names + at_names
    insert_cols = sql.SQL(", ").join(sql.Identifier(c) for c in all_cols)

    if pg_pk_cols:
        pk_set = set(pg_pk_cols)
        update_cols = [c for c in all_cols if c not in pk_set]
        if update_cols:
            set_clause = sql.SQL(", ").join(
                sql.SQL("{col} = EXCLUDED.{col}").format(
                    col=sql.Identifier(c)
                )
                for c in update_cols
            )
            on_conflict = sql.SQL(
                "ON CONFLICT ({pk}) DO UPDATE SET {upd}"
            ).format(
                pk=sql.SQL(", ").join(sql.Identifier(p) for p in pg_pk_cols),
                upd=set_clause,
            )
        else:
            on_conflict = sql.SQL("ON CONFLICT ({pk}) DO NOTHING").format(
                pk=sql.SQL(", ").join(sql.Identifier(p) for p in pg_pk_cols)
            )
    else:
        # No PK: full replace.
        with pg_conn.cursor() as cur:
            cur.execute(
                sql.SQL("TRUNCATE TABLE {}.{}").format(
                    sql.Identifier(PG_SCHEMA),
                    sql.Identifier(table_name),
                )
            )
        on_conflict = sql.SQL("")

    insert_stmt = sql.SQL(
        "INSERT INTO {}.{} ({}) VALUES %s {}"
    ).format(
        sql.Identifier(PG_SCHEMA),
        sql.Identifier(table_name),
        insert_cols,
        on_conflict,
    )

    src_col_names = [c[1] for c in columns]
    select_cols = ", ".join(f"[{n}]" for n in src_col_names)
    select_query = f"SELECT {select_cols} FROM [{table_name}]"
    select_params = ()
    if watermark_col is not None:
        select_query += f" WHERE [{watermark_col}] >= ?"
        select_params = (watermark_sqlite,)
    cur = sqlite_conn.execute(select_query, select_params)

    total = 0
    batch = []
    with pg_conn.cursor() as pcur:
        def flush():
            nonlocal batch, total
            if not batch:
                return
            execute_values(pcur, insert_stmt, batch, page_size=BATCH_SIZE)
            total += len(batch)
            batch = []

        while True:
            row = cur.fetchone()
            if row is None:
                break
            row = list(row)
            for pos in bool_keep_positions:
                src_idx = keep_indices[pos]
                if row[src_idx] is not None:
                    row[src_idx] = bool(row[src_idx])
            kept = [row[i] for i in keep_indices]
            ts_values = [epoch_to_ts(row[i]) for i in ts_indices]
            batch.append(tuple(kept + ts_values))
            if len(batch) >= BATCH_SIZE:
                flush()
        flush()

    pg_conn.commit()
    mode = (
        f"incremental (>= {watermark_dt.isoformat()})"
        if watermark_col is not None
        else ("full (no pk, truncate+insert)" if not pk_cols else "full")
    )
    return total, ts_cols, mode


def main():
    parser = argparse.ArgumentParser(
        description="Replicate Gadgetbridge SQLite into Postgres.",
        epilog="Unknown flags are forwarded to hrv_aggregate.py.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore per-table watermarks and fully re-upsert every row. "
             "Use when source rows below the target max have changed.",
    )
    args, passthrough_args = parser.parse_known_args()

    if not DB_PATH.exists() or (time.time() - DB_PATH.stat().st_ctime) > EXPIRY_SECONDS:
        download_db()

    if not DB_PATH.exists():
        print(f"ERROR: database not found: {DB_PATH}")
        sys.exit(1)

    ensure_database()
    sqlite_conn = sqlite3.connect(str(DB_PATH))
    pg_conn = connect_target()
    try:
        ensure_schema(pg_conn)

        tables = get_user_tables(sqlite_conn)
        non_empty = [t for t in tables if table_row_count(sqlite_conn, t) > 0]
        mode_label = "FORCE full" if args.force else "incremental"
        print(
            f"\nReplicating {len(non_empty)} non-empty tables to "
            f"{PG_USER}@{PG_HOST}:{PG_PORT}/{PG_DB}.{PG_SCHEMA}  [{mode_label}]"
        )

        for t in non_empty:
            t_start = time.monotonic()
            n, ts, mode = replicate_table(
                sqlite_conn, pg_conn, t, force=args.force,
            )
            dt = time.monotonic() - t_start
            extra = f"  [+{len(ts)} _at]" if ts else ""
            print(f"  {t:38s} rows={n:<8} mode={mode} ({dt:.1f}s){extra}")

    finally:
        sqlite_conn.close()
        pg_conn.close()

    hrv_path = str(Path(__file__).parent / "hrv_aggregate.py")
    forwarded = " ".join(passthrough_args) if passthrough_args else "(none)"
    print(f"\nReplication done. Running hrv_aggregate.py  [args: {forwarded}]")
    saved_argv = sys.argv
    try:
        sys.argv = [hrv_path, *passthrough_args]
        runpy.run_path(hrv_path, run_name="__main__")
    finally:
        sys.argv = saved_argv


if __name__ == "__main__":
    main()
