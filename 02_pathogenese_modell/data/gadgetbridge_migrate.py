#!/usr/bin/env python3
"""
Gadgetbridge SQLite -> Hive (DuckDB/Parquet) replication
========================================================

Reads the local Gadgetbridge SQLite database (never modified) and imports
a curated subset of its samples into the local Hive (segment=raw) as time
series. The Hive is later synced to the server with rsync.

Mapping (source table.column -> metric{labels})
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
Several RR intervals may share one TIMESTAMP (SEQ 0..8 orders them). Rather
than exploding these into up to 9 seq-labelled sub-series (9x the series
index + export lines), each packet is *resolved in time*: the beats of a
packet are laid out around the packet timestamp using their own RR
distances (cumulative offsets, mean-centered on TIMESTAMP), so every beat
gets a unique, physically meaningful timestamp and the packet ends up
centered in its window. The spread is clamped to half the gap to the
preceding/following packet, bounding the jitter symmetrically in both
directions and guaranteeing that beats of adjacent packets never cross.
The result is a single rr_interval_ms series with strictly increasing
timestamps whose ascending order reproduces the exact device (TIMESTAMP,
SEQ) order — no client-side seq merge needed. See _reconstruct_beat_times.

Because a packet's layout depends on its next neighbor, the very last
packet of an import is held back (its next gap is not yet known) and
re-imported once a following packet exists; incremental runs reload a
small RR_REIMPORT_MARGIN_MS overlap so interior packets reconstruct
identically and the Hive deduplicates the re-written points.

Incremental & idempotent
-----------------------
Per series the newest sample timestamp already in the Hive is used as a
watermark; only source rows at/after it are re-imported. The Hive's
merge-on-write deduplicates repeated (ts, labels) samples, so boundary
re-imports are harmless.
Use --full to ignore watermarks and re-import everything.
"""

import argparse
import sqlite3
import time
from pathlib import Path

from hive_io import HiveWriter as VMWriter, force_flush, latest_timestamp_ms

# --- Source -----------------------------------------------------------
# Default working DB (the file run_pipeline.py downloads to). The concrete
# source file is normally passed explicitly via --db, so no run is pinned
# to a constant snapshot.
DEFAULT_DB_PATH = Path(__file__).parent / "Gadgetbridge"

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

# RR reconstruction (see module docstring / _reconstruct_beat_times).
# Fallback half-window when a neighboring packet gap is unknown (very first
# packet of all data, or an isolated packet after a long recording gap).
RR_DEFAULT_GAP_MS = 60_000
# Incremental RR re-scan overlap: reload this much source history before the
# stored watermark so the boundary packets reconstruct with the same
# neighbors as the prior run (idempotent via VM's identical-(series,ts) dedup).
RR_REIMPORT_MARGIN_MS = 60_000


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


def _reconstruct_beat_times(
    ts_ms: int,
    rr_list: list,
    gap_prev_ms: int | None,
    gap_next_ms: int | None,
) -> list:
    """Assign each beat of one packet a unique timestamp around ts_ms.

    A packet reports up to 9 RR intervals (SEQ order) sharing a single
    device TIMESTAMP. We reconstruct the beats' real times by taking their
    cumulative RR offsets, mean-centering them on ts_ms (so the packet sits
    in the middle of its window), and clamping the spread to half the gap
    to the preceding/following packet. This bounds the jitter symmetrically
    and guarantees adjacent packets' beats never overlap, so the ascending
    timestamp order equals the original (TIMESTAMP, SEQ) order.

    Returns a list of strictly increasing int timestamps (ms), one per beat.
    """
    m = len(rr_list)
    if m == 1:
        return [ts_ms]

    cum = []
    acc = 0
    for r in rr_list:
        acc += r
        cum.append(acc)
    mean = acc / m  # acc == cum[-1] == total span
    offsets = [c - mean for c in cum]  # ascending; offsets[0] < 0 < offsets[-1]

    gp = gap_prev_ms if gap_prev_ms is not None else (
        gap_next_ms if gap_next_ms is not None else RR_DEFAULT_GAP_MS)
    gn = gap_next_ms if gap_next_ms is not None else (
        gap_prev_ms if gap_prev_ms is not None else RR_DEFAULT_GAP_MS)

    max_fwd = offsets[-1]
    max_back = -offsets[0]
    scale = 1.0
    if max_fwd > 0:
        scale = min(scale, (gn / 2.0) / max_fwd)
    if max_back > 0:
        scale = min(scale, (gp / 2.0) / max_back)

    beats = []
    last = None
    for o in offsets:
        b = int(round(ts_ms + scale * o))
        if last is not None and b <= last:
            b = last + 1  # keep strictly increasing after rounding/clamping
        beats.append(b)
        last = b
    return beats


def _iter_rr_packets(cursor, ts_unit: str, counter: list):
    """Yield (ts_ms, rr_list) per device packet from a (TIMESTAMP, SEQ)-ordered
    cursor. rr_list is in SEQ order. counter[0] tracks rows read.
    """
    cur_ts = None
    cur_rr: list = []
    for ts_raw, _seq, rr in cursor:
        counter[0] += 1
        if ts_raw is None or rr is None:
            continue
        if cur_ts is None:
            cur_ts, cur_rr = ts_raw, [rr]
        elif ts_raw == cur_ts:
            cur_rr.append(rr)
        else:
            yield _to_ms(cur_ts, ts_unit), cur_rr
            cur_ts, cur_rr = ts_raw, [rr]
    if cur_ts is not None:
        yield _to_ms(cur_ts, ts_unit), cur_rr


def replicate_rr_mapping(sqlite_conn, writer: VMWriter, mapping: dict, force: bool):
    """RR-specific replication: resolve each SEQ packet into a single
    rr_interval_ms series with unique per-beat timestamps.

    A 1-packet lookahead supplies each packet's next-neighbor gap; the very
    last packet is held back (next gap unknown) and picked up by the next
    run's overlap re-scan.
    """
    table = mapping["table"]
    ts_col = mapping["ts_col"]
    ts_unit = mapping["ts_unit"]
    series = mapping["series"][0]
    metric = series["metric"]
    value_col = series["value_col"]
    seq_col = series["seq_label"]

    watermark_ms = None
    if not force:
        watermark_ms = latest_timestamp_ms(metric)

    where = ""
    params: tuple = ()
    if watermark_ms is not None:
        lo_native = _from_ms_native(
            watermark_ms - RR_REIMPORT_MARGIN_MS, ts_unit
        )
        where = f" WHERE [{ts_col}] >= ?"
        params = (lo_native,)

    total_rows = sqlite_conn.execute(
        f"SELECT COUNT(*) FROM [{table}]" + where, params
    ).fetchone()[0]

    select_sql = (
        f"SELECT [{ts_col}], [{seq_col}], [{value_col}] FROM [{table}]"
        + where
        + f" ORDER BY [{ts_col}], [{seq_col}]"
    )
    cur = sqlite_conn.execute(select_sql, params)

    counter = [0]
    packets = _iter_rr_packets(cur, ts_unit, counter)
    n_written = 0
    n_held_back = 0
    t0 = time.monotonic()

    def _emit(ts_ms, rr_list, gap_prev, gap_next):
        nonlocal n_written
        beats = _reconstruct_beat_times(ts_ms, rr_list, gap_prev, gap_next)
        for b, rr in zip(beats, rr_list):
            writer.add(metric, {}, b, float(rr))
            n_written += 1

    prev_ts = None
    cur_pk = next(packets, None)
    if cur_pk is not None:
        for nxt in packets:
            cur_ts, cur_rr = cur_pk
            gap_prev = (cur_ts - prev_ts) if prev_ts is not None else None
            gap_next = nxt[0] - cur_ts
            _emit(cur_ts, cur_rr, gap_prev, gap_next)
            prev_ts = cur_ts
            cur_pk = nxt

            if counter[0] % PROGRESS_EVERY == 0:
                pct = (counter[0] / total_rows * 100) if total_rows else 100.0
                print(
                    f"\r  {table:30s} {counter[0]:>9,}/{total_rows:,} ({pct:3.0f}%)"
                    f" [{time.monotonic() - t0:.0f}s]",
                    end="", flush=True,
                )
        # cur_pk is the final packet: its next-neighbor gap is unknown, so
        # hold it back for the next run's overlap re-scan.
        n_held_back = len(cur_pk[1])

    writer.flush()
    mode = (
        f"incremental (>= ms {watermark_ms - RR_REIMPORT_MARGIN_MS})"
        if watermark_ms is not None else "full"
    )
    if n_held_back:
        mode += f", held back {n_held_back} boundary beat(s)"
    return counter[0], n_written, mode


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
        description="Replicate a Gadgetbridge SQLite subset into the local Hive.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        metavar="DB_FILE",
        help="Path to the source Gadgetbridge SQLite database to import "
             "(default: %(default)s).",
    )
    parser.add_argument(
        "--full",
        dest="force",
        action="store_true",
        help="Ignore per-series watermarks and re-import every source row "
             "(same flag name as the aggregators, so the pipeline forwards it "
             "to every stage).",
    )
    args, _ = parser.parse_known_args()

    db_path = args.db
    if not db_path.exists():
        raise SystemExit(f"ERROR: source database not found: {db_path}")

    sqlite_conn = sqlite3.connect(str(db_path))
    writer = VMWriter()
    mode_label = "FORCE full" if args.force else "incremental"
    print(f"Importing Gadgetbridge subset into the local Hive  [{mode_label}]")
    try:
        for mapping in MAPPINGS:
            t_start = time.monotonic()
            # RR packets (any series carrying a seq_label) need the
            # timestamp-resolving path; everything else is a plain column map.
            if any("seq_label" in s for s in mapping["series"]):
                replicate = replicate_rr_mapping
            else:
                replicate = replicate_mapping
            n_read, n_written, mode = replicate(
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
        f"Import done. {writer.total:,} samples written to the local Hive."
    )


if __name__ == "__main__":
    main()
