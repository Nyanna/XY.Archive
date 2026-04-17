#!/usr/bin/env python3
"""
Gadgetbridge SQLite Cleanup Script
-----------------------------------
1. Entfernt alle leeren Tabellen.
2. Aendert Spaltentypen von INTEGER auf TIMESTAMP fuer Datumsspalten,
   ohne die gespeicherten Werte zu konvertieren.

Erstellt vor der Bearbeitung ein Backup: Gadgetbridge.bak
"""

import sqlite3
import shutil
import sys
import re
import runpy
import gdown
import time
from pathlib import Path

DB_PATH = Path(__file__).parent / "Gadgetbridge"
EXPIRY_HOURS = 2 * 3600

# Spaltennamen, die Zeitpunkte (nicht Dauern) darstellen.
# Muster werden case-insensitive geprueft.
TIMESTAMP_PATTERNS = [
    r"^TIMESTAMP$",
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

# Spalten die trotz "time" im Namen keine Zeitpunkte sind
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
    r"^TIME$",  # ambig in workout tables -- eher Dauer
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


def get_tables(conn):
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    return [r[0] for r in cur.fetchall()]


def table_row_count(conn, table):
    return conn.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0]


def get_create_sql(conn, table):
    cur = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)
    )
    return cur.fetchone()[0]


def get_columns(conn, table):
    cur = conn.execute(f"PRAGMA table_info([{table}])")
    return cur.fetchall()  # (cid, name, type, notnull, dflt_value, pk)


def rebuild_table_with_types(conn, table):
    """Baut die Tabelle neu auf, wobei INTEGER-Timestamp-Spalten als TIMESTAMP definiert werden."""
    columns = get_columns(conn, table)
    cols_to_change = []
    for col in columns:
        col_name = col[1]
        col_type = (col[2] or "").upper()
        if col_type == "INTEGER" and is_timestamp_column(col_name):
            cols_to_change.append(col_name)

    if not cols_to_change:
        return []

    original_sql = get_create_sql(conn, table)
    tmp_table = f"_tmp_rebuild_{table}"

    # Neue CREATE-Anweisung: INTEGER -> TIMESTAMP fuer erkannte Spalten
    new_sql = original_sql
    for col_name in cols_to_change:
        # Ersetze "col_name" INTEGER oder col_name INTEGER durch ... TIMESTAMP
        # Handles: "COL" INTEGER, [COL] INTEGER, COL INTEGER
        pattern = re.compile(
            rf'("{re.escape(col_name)}"|\[{re.escape(col_name)}\]|{re.escape(col_name)})\s+INTEGER\b',
            re.IGNORECASE,
        )
        new_sql = pattern.sub(rf"\1 TIMESTAMP", new_sql, count=1)

    # Tabellenname in CREATE auf tmp aendern
    new_sql = new_sql.replace(
        f"CREATE TABLE {table}",
        f"CREATE TABLE [{tmp_table}]",
        1,
    )
    new_sql = new_sql.replace(
        f'CREATE TABLE "{table}"',
        f"CREATE TABLE [{tmp_table}]",
        1,
    )

    col_names = ", ".join(f"[{c[1]}]" for c in columns)

    # Xiaomi_Activity_Sample speichert Timestamps in Sekunden statt Millisekunden.
    # Bei dieser Tabelle die Werte beim Kopieren umrechnen (* 1000).
    needs_sec_to_ms = table.upper() == "XIAOMI_ACTIVITY_SAMPLE"

    if needs_sec_to_ms:
        select_exprs = []
        for c in columns:
            cname = c[1]
            if cname in cols_to_change:
                select_exprs.append(f"[{cname}] * 1000")
            else:
                select_exprs.append(f"[{cname}]")
        select_clause = ", ".join(select_exprs)
    else:
        select_clause = col_names

    conn.execute(new_sql)
    conn.execute(f"INSERT INTO [{tmp_table}] SELECT {select_clause} FROM [{table}]")
    conn.execute(f"DROP TABLE [{table}]")
    conn.execute(f"ALTER TABLE [{tmp_table}] RENAME TO [{table}]")

    return cols_to_change

def downloadDB():
    gdown.download("https://drive.google.com/uc?id=1NwUmQ_v7WOQIe5tYm2GixOQYm5HSt-xh", "Gadgetbridge", quiet=False)

def main():
    if not DB_PATH.exists() or (time.time() - DB_PATH.stat().st_ctime) > EXPIRY_HOURS:
        downloadDB()
    
    if not DB_PATH.exists():
        print(f"Fehler: Datenbank nicht gefunden: {DB_PATH}")
        sys.exit(1)

    # Backup
    backup_path = DB_PATH.with_suffix(".bak")
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup erstellt: {backup_path}")

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = OFF")

    tables = get_tables(conn)
    print(f"\nTabellen gesamt: {len(tables)}")

    # 1. Leere Tabellen entfernen
    empty = []
    nonempty = []
    for t in tables:
        if t.startswith("sqlite_"):
            nonempty.append(t)
            continue
        if table_row_count(conn, t) == 0:
            empty.append(t)
        else:
            nonempty.append(t)

    print(f"Leere Tabellen: {len(empty)}")
    for t in empty:
        conn.execute(f"DROP TABLE [{t}]")
        print(f"  DROP {t}")

    # 2. Spaltentypen aendern
    # Spaltentypen ändeern funktioniert nicht in Metabase, der JDBC-Treiber konvertiert nur in eine Richtung.
    # print(f"\nVerbleibende Tabellen: {len(nonempty)}")
    # for t in nonempty:
    #    if t.startswith("sqlite_"):
    #        continue
    #    changed = rebuild_table_with_types(conn, t)
    #    if changed:
    #        print(f"  {t}: {', '.join(changed)} -> TIMESTAMP")

    conn.commit()
    conn.execute("VACUUM")
    conn.close()
    print("\nFertig.\nStarte verarbeitung...")
    runpy.run_path("hrv_aggregate.py", run_name="__main__")


if __name__ == "__main__":
    main()
