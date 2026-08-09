#!/usr/bin/env python3
"""
Gadgetbridge SQLite -> Victoria Metrics replication
===================================================

Reads the local Gadgetbridge SQLite database (never modified) and imports
a curated subset of its samples into Victoria Metrics as time series.

Mapping (source table.column -> VM metric{labels})
--------------------------------------------------
GENERIC_HEART_RATE_SAMPLE.HEART_RATE  -> heart_rate{source="generic"}
XIAOMI_ACTIVITY_SAMPLE.HEART_RATE     -> heart_rate{source="xiaomi_activity"}
HEART_RR_INTERVAL_SAMPLE.RR_MILLIS    -> rr_interval_ms{seq="<SEQ>"}
XIAOMI_SLEEP_STAGE_SAMPLE.STAGE       -> sleep_stage
XIAOMI_SLEEP_TIME_SAMPLE.*            -> sleep_is_awake, sleep_total_duration,
                                         sleep_deep_sleep_duration,
                                         sleep_light_sleep_duration,
                                         sleep_rem_sleep_duration,
                                         sleep_awake_duration, sleep_timestamp

Timestamp semantics
-------------------
Every series' timestamp is the source row's time column converted to ms.
GENERIC_HEART_RATE / RR / SLEEP_STAGE store ms already; XIAOMI_ACTIVITY
stores seconds (scaled x1000). For XIAOMI_SLEEP_TIME the *wakeup* time
(WAKEUP_TIME) is the series timestamp, while the row's own TIMESTAMP (bed
time) is preserved as a separate data series `sleep_timestamp`.

RR sequence semantics
--------------------
Several RR intervals may share one TIMESTAMP (SEQ 0..8 orders them). Since
a VM series requires unique timestamps, SEQ is carried as a label so each
sub-sequence becomes its own series; readers merge by (timestamp, seq).

Incremental & idempotent
-----------------------
Per series the newest sample timestamp already in VM is used as a
watermark; only source rows at/after it are re-imported. VM deduplicates
repeated (series, timestamp) samples, so boundary re-imports are harmless.
Use --force to ignore watermarks and re-import everything.
"""

import argparse
import sqlite3
import time
from pathlib import Path

from vm_io import VMWriter, force_flush, latest_timestamp_ms

# --- Source -----------------------------------------------------------
DB_PATH = Path(__file__).parent / "Gadgetbridge"

# Heart-rate readings of 0 are a "no measurement" sentinel in
# XIAOMI_ACTIVITY_SAMPLE (and never legitimately 0 elsewhere); drop them.
HR_MIN_VALID = 1

# --- Mapping ----------------------------------------------------------
# Each mapping describes one source table and the VM series derived from
# it. A "series" pulls one value column into one metric; `labels` are
# static, `seq_label` (RR only) turns a column into a per-value label.
#   ts_unit: 's' or 'ms' — native unit of ts_col in SQLite.
#   min_value: optional inclusive lower bound applied to the value.
MAPPINGS = [
    {
        "table": "GENERIC_HEART_RATE_SAMPLE",
        "ts_col": "TIMESTAMP",
        "ts_unit": "ms",
        "series": [
            {
                "metric": "heart_rate",
                "labels": {"source": "generic"},
                "value_col": "HEART_RATE",
                "min_value": HR_MIN_VALID,
            },
        ],
    },
    {
        "table": "XIAOMI_ACTIVITY_SAMPLE",
        "ts_col": "TIMESTAMP",
        "ts_unit": "s",
        "series": [
            {
                "metric": "heart_rate",
                "labels": {"source": "xiaomi_activity"},
                "value_col": "HEART_RATE",
                "min_value": HR_MIN_VALID,
            },
        ],
    },
    {
        "table": "HEART_RR_INTERVAL_SAMPLE",
        "ts_col": "TIMESTAMP",
        "ts_unit": "ms",
        "series": [
            {
                "metric": "rr_interval_ms",
                "labels": {},
                "value_col": "RR_MILLIS",
                "seq_label": "SEQ",
            },
        ],
    },
    {
        "table": "XIAOMI_SLEEP_STAGE_SAMPLE",
        "ts_col": "TIMESTAMP",
        "ts_unit": "ms",
        "series": [
            {"metric": "sleep_stage", "labels": {}, "value_col": "STAGE"},
        ],
    },
    {
        "table": "XIAOMI_SLEEP_TIME_SAMPLE",
        "ts_col": "WAKEUP_TIME",
        "ts_unit": "ms",
        "series": [
            {"metric": "sleep_is_awake",             "value_col": "IS_AWAKE"},
            {"metric": "sleep_total_duration",       "value_col": "TOTAL_DURATION"},
            {"metric": "sleep_deep_sleep_duration",  "value_col": "DEEP_SLEEP_DURATION"},
            {"metric": "sleep_light_sleep_duration", "value_col": "LIGHT_SLEEP_DURATION"},
            {"metric": "sleep_rem_sleep_duration",   "value_col": "REM_SLEEP_DURATION"},
            {"metric": "sleep_awake_duration",       "value_col": "AWAKE_DURATION"},
            # TIMESTAMP (bed time) is a data field here, not the series ts.
            {"metric": "sleep_timestamp",            "value_col": "TIMESTAMP"},
        ],
    },
]

PROGRESS_EVERY = 500_000


def _selector(series: dict) -> str:
    """PromQL selector matching a series' metric name + static labels."""
    labels = series.get("labels", {})
    if not labels:
        return series["metric"]
    parts = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
    return f'{series["metric"]}{{{parts}}}'


def _to_ms(raw, ts_unit: str) -> int:
    return int(raw) * 1000 if ts_unit == "s" else int(raw)


def _from_ms_native(ms: int, ts_unit: str) -> int:
    """Convert a ms watermark back into the source column's native unit."""
    return ms // 1000 if ts_unit == "s" else ms


def replicate_mapping(sqlite_conn, writer: VMWriter, mapping: dict, force: bool):
    table = mapping["table"]
    ts_col = mapping["ts_col"]
    ts_unit = mapping["ts_unit"]
    series_defs = mapping["series"]

    # Watermark: newest ts already stored for the first series of the
    # mapping (all series of a mapping share the same row timestamps).
    watermark_ms = None
    if not force:
        watermark_ms = latest_timestamp_ms(_selector(series_defs[0]))

    # Build the SELECT: ts column + every distinct value/seq column.
    value_cols = []
    for s in series_defs:
        for col in (s["value_col"], s.get("seq_label")):
            if col and col not in value_cols:
                value_cols.append(col)
    select_cols = [ts_col] + value_cols
    col_index = {c: i for i, c in enumerate(select_cols)}

    where = ""
    params: tuple = ()
    if watermark_ms is not None:
        where = f" WHERE [{ts_col}] >= ?"
        params = (_from_ms_native(watermark_ms, ts_unit),)

    select_sql = (
        "SELECT " + ", ".join(f"[{c}]" for c in select_cols)
        + f" FROM [{table}]" + where
    )

    total_rows = sqlite_conn.execute(
        f"SELECT COUNT(*) FROM [{table}]" + where, params
    ).fetchone()[0]

    cur = sqlite_conn.execute(select_sql, params)
    n_read = 0
    n_written = 0
    t0 = time.monotonic()
    while True:
        row = cur.fetchone()
        if row is None:
            break
        n_read += 1
        ts_raw = row[col_index[ts_col]]
        if ts_raw is None:
            continue
        ts_ms = _to_ms(ts_raw, ts_unit)

        for s in series_defs:
            value = row[col_index[s["value_col"]]]
            if value is None:
                continue
            min_value = s.get("min_value")
            if min_value is not None and value < min_value:
                continue
            labels = dict(s.get("labels", {}))
            seq_col = s.get("seq_label")
            if seq_col is not None:
                seq_val = row[col_index[seq_col]]
                if seq_val is None:
                    continue
                labels["seq"] = str(int(seq_val))
            writer.add(s["metric"], labels, ts_ms, float(value))
            n_written += 1

        if n_read % PROGRESS_EVERY == 0:
            pct = (n_read / total_rows * 100) if total_rows else 100.0
            print(
                f"\r  {table:30s} {n_read:>9,}/{total_rows:,} ({pct:3.0f}%)"
                f" [{time.monotonic() - t0:.0f}s]",
                end="", flush=True,
            )

    writer.flush()
    mode = (
        f"incremental (>= ms {watermark_ms})"
        if watermark_ms is not None else "full"
    )
    return n_read, n_written, mode


def main():
    parser = argparse.ArgumentParser(
        description="Replicate a Gadgetbridge SQLite subset into Victoria Metrics.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore per-series watermarks and re-import every source row.",
    )
    args, _ = parser.parse_known_args()

    if not DB_PATH.exists():
        raise SystemExit(f"ERROR: source database not found: {DB_PATH}")

    sqlite_conn = sqlite3.connect(str(DB_PATH))
    writer = VMWriter()
    mode_label = "FORCE full" if args.force else "incremental"
    print(f"Importing Gadgetbridge subset into Victoria Metrics  [{mode_label}]")
    try:
        for mapping in MAPPINGS:
            t_start = time.monotonic()
            n_read, n_written, mode = replicate_mapping(
                sqlite_conn, writer, mapping, force=args.force,
            )
            dt = time.monotonic() - t_start
            print(
                f"\r  {mapping['table']:30s} rows={n_read:<9,} "
                f"samples={n_written:<9,} mode={mode} ({dt:.1f}s)"
            )
    finally:
        sqlite_conn.close()

    flushed = force_flush()
    print(
        f"Import done. {writer.total:,} samples written to Victoria Metrics."
    )


if __name__ == "__main__":
    main()
