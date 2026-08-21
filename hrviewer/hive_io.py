#!/usr/bin/env python3
"""
Local DuckDB/Parquet Hive I/O helper.
=====================================

All time series
are stored as a local, Hive-partitioned Parquet dataset that is later
synchronised to the server with rsync. Because the layout is a plain
directory tree of small per-day Parquet files, an incremental run only
rewrites the handful of day files it actually touches, so rsync uploads a
minimal delta.

Layout
------
    <HIVE_PATH>/
        segment=<raw|hrv>/
            metric=<name>/
                dt=<YYYY-MM-DD>/          # UTC day of the samples
                    data.parquet          # columns: ts, value

Two segments share one Hive (per the project design):
  * segment=raw : source series written by gadgetbridge_migrate.py
                  (heart_rate_generic, heart_rate_xiaomi_activity,
                  rr_interval_ms, sleep_*)
  * segment=hrv : aggregated series (hrv_*, hrv_band_*)
The segment is derived from the metric name (hrv_* -> hrv, else raw).

Sample model
------------
Every row is (ts BIGINT ms-epoch, value DOUBLE). A logical series is the
set of rows sharing one metric name. There is no per-sample label
dimension: anything that used to distinguish samples of one metric (e.g. a
measurement source) is folded into the metric name itself
(heart_rate_generic vs. heart_rate_xiaomi_activity).

Watermarks & idempotency
------------------------
* latest_timestamp_ms(metric) reads MAX(ts) for a series straight from the
  Hive -> the incremental watermark, no external state store.
* Writes are merge-on-write: a partition file is rewritten as the dedup of
  its existing rows UNION the new rows, keyed on ts, with the new row
  winning. Re-importing an overlap (migration boundary re-scan) or
  recomputing a minute is therefore idempotent -- exactly the guarantee VM
  gave us via identical-(series, timestamp) dedup, now enforced locally.

Memory
------
The move away from VM was driven by its memory use. This layer keeps its
own footprint small: samples are staged into an on-disk DuckDB table (which
spills to disk) and merged partition-by-partition, and reads stream from
Parquet in record batches. The only large in-RAM arrays are the RR arrays
the aggregators deliberately materialise for windowed analysis.
"""

import atexit
import os
import shutil
import tempfile
from pathlib import Path

import duckdb

# --- Configuration ----------------------------------------------------
HIVE_PATH = Path(os.environ.get("HIVE_PATH", Path(__file__).parent / "hive"))

DEFAULT_BATCH_SAMPLES = 50_000        # Python-side buffer before staging
_MERGE_THRESHOLD = 1_000_000          # staged rows before an auto-merge
DEFAULT_CSV_CHUNK_ROWS = 200_000      # read batch size for RR streaming

_RAW_SEGMENT = "raw"
_HRV_SEGMENT = "hrv"


def _segment_for(metric: str) -> str:
    """Map a metric name to its Hive segment (hrv_* -> hrv, else raw)."""
    return _HRV_SEGMENT if metric.startswith("hrv_") else _RAW_SEGMENT


# --- DuckDB connection ------------------------------------------------
_con = None
_stage_db = None


def _connect() -> "duckdb.DuckDBPyConnection":
    """Lazily open the shared connection.

    Backed by a throwaway on-disk database so large staging tables spill to
    disk instead of pinning RAM. Reads go straight against Parquet files.
    """
    global _con, _stage_db
    if _con is None:
        fd, _stage_db = tempfile.mkstemp(prefix="hive_stage_", suffix=".duckdb")
        os.close(fd)
        os.unlink(_stage_db)  # let DuckDB create it fresh
        _con = duckdb.connect(_stage_db)
        _con.execute("SET TimeZone='UTC'")
        _con.execute(
            f"SET temp_directory='{tempfile.gettempdir()}'"
        )
        atexit.register(_cleanup)
    return _con


def _cleanup() -> None:
    global _con
    try:
        if _con is not None:
            _con.close()
    except Exception:
        pass
    for suffix in ("", ".wal", ".tmp"):
        try:
            if _stage_db:
                p = _stage_db + suffix
                if os.path.exists(p):
                    if os.path.isdir(p):
                        shutil.rmtree(p, ignore_errors=True)
                    else:
                        os.unlink(p)
        except Exception:
            pass


def _metric_glob(metric: str) -> str:
    segment = _segment_for(metric)
    return str(HIVE_PATH / f"segment={segment}" / f"metric={metric}" / "dt=*" / "data.parquet")


def _metric_dir(metric: str) -> Path:
    segment = _segment_for(metric)
    return HIVE_PATH / f"segment={segment}" / f"metric={metric}"


def _has_files(metric: str) -> bool:
    import glob as _glob
    return bool(_glob.glob(_metric_glob(metric)))


# --- Writer -----------------------------------------------------------
class HiveWriter:
    """Buffers samples and merge-writes them into the Hive.

        w = HiveWriter()
        w.add("heart_rate_generic", ts_ms, 78)
        w.flush()

    add() appends to a small Python buffer; at batch_samples the buffer is
    staged into an on-disk DuckDB table. flush() stages the remainder and
    merges every touched partition (existing UNION staged, deduped on ts,
    new wins) into its data.parquet. Large imports auto-merge once staging
    crosses _MERGE_THRESHOLD so neither RAM nor the staging table grows
    without bound.
    """

    def __init__(self, batch_samples: int = DEFAULT_BATCH_SAMPLES):
        self.batch_samples = batch_samples
        self._buf: list = []
        self._staged = 0
        self.total = 0
        self._con = _connect()
        self._stg = f"_stg_{id(self)}"
        self._con.execute(
            f"CREATE TABLE IF NOT EXISTS {self._stg}"
            "(segment VARCHAR, metric VARCHAR, ts BIGINT, value DOUBLE)"
        )

    def add(self, name: str, ts_ms: int, value: float) -> None:
        self._buf.append(
            (_segment_for(name), name, int(ts_ms), float(value))
        )
        if len(self._buf) >= self.batch_samples:
            self._stage()

    def _stage(self) -> None:
        if self._buf:
            # Vectorized bulk insert via a pandas frame, natively supported
            # by DuckDB (no PyArrow/nanoarrow dependency needed for the
            # write path -- same pattern as mqttduck.writer.DuckDbSink).
            # Plain executemany() with no explicit transaction lets DuckDB
            # commit each row individually (~1ms/row -> ~50s per 50k-row
            # batch, i.e. minutes of dead silence before the caller's coarse
            # PROGRESS_EVERY print ever fires, looking exactly like a hang).
            # A single columnar insert is >100x faster for batches in the
            # tens-of-thousands.
            import pandas as pd

            segment, metric, ts, value = zip(*self._buf)
            batch = pd.DataFrame(
                {
                    "segment": segment,
                    "metric": metric,
                    "ts": ts,
                    "value": value,
                }
            ).astype({"segment": "string", "metric": "string",
                      "ts": "int64", "value": "float64"})
            self._con.register(f"{self._stg}_arrow", batch)
            self._con.execute(
                f"INSERT INTO {self._stg} SELECT * FROM {self._stg}_arrow"
            )
            self._con.unregister(f"{self._stg}_arrow")
            self._staged += len(self._buf)
            self._buf = []
        if self._staged >= _MERGE_THRESHOLD:
            self._merge()

    def flush(self) -> None:
        self._stage()
        self._merge()

    def _merge(self) -> None:
        if self._staged == 0:
            return
        parts = self._con.execute(
            f"SELECT DISTINCT segment, metric, "
            f"strftime(to_timestamp(ts // 1000), '%Y-%m-%d') AS dt FROM {self._stg}"
        ).fetchall()
        for segment, metric, dt in parts:
            self._merge_partition(segment, metric, dt)
        self.total += self._staged
        self._staged = 0
        self._con.execute(f"DELETE FROM {self._stg}")

    def _merge_partition(self, segment: str, metric: str, dt: str) -> None:
        pdir = HIVE_PATH / f"segment={segment}" / f"metric={metric}" / f"dt={dt}"
        pdir.mkdir(parents=True, exist_ok=True)
        final = pdir / "data.parquet"
        tmp = pdir / "data.parquet.tmp"

        existing = ""
        if final.exists():
            existing = (
                f"UNION ALL SELECT ts, value, 0 AS prio "
                f"FROM read_parquet('{final.as_posix()}')"
            )

        self._con.execute(
            f"""
            COPY (
              WITH u AS (
                SELECT ts, value, 1 AS prio FROM {self._stg}
                  WHERE segment = ? AND metric = ?
                    AND strftime(to_timestamp(ts // 1000), '%Y-%m-%d') = ?
                {existing}
              ),
              d AS (
                SELECT ts, value,
                       row_number() OVER (PARTITION BY ts
                                          ORDER BY prio DESC) AS rn
                FROM u
              )
              SELECT ts, value FROM d WHERE rn = 1 ORDER BY ts
            ) TO '{tmp.as_posix()}' (FORMAT PARQUET, PARQUET_VERSION V2, COMPRESSION ZSTD);
            """,
            [segment, metric, dt],
        )
        os.replace(tmp, final)


# Backwards-compatible alias (call sites still say VMWriter).
VMWriter = HiveWriter


def force_flush() -> bool:
    """No-op: merge-on-write already made every flush() durable & queryable."""
    return True


# --- Watermarks -------------------------------------------------------
def latest_timestamp_ms(metric: str, lookback: str = "3650d") -> int | None:
    """Newest sample timestamp (ms) for a metric, or None.

    `lookback` is accepted for API compatibility with the old VM backend
    and ignored -- MAX(ts) over the Parquet files is O(files) and needs no
    windowing.
    """
    if not _has_files(metric):
        return None
    row = _connect().execute(
        f"SELECT max(ts) FROM read_parquet('{_metric_glob(metric)}')"
    ).fetchone()
    return int(row[0]) if row and row[0] is not None else None


# --- Deletion ---------------------------------------------------------
def delete_series(metric: str) -> None:
    """Delete every sample of a metric (used by the aggregators' --full path)."""
    mdir = _metric_dir(metric)
    if mdir.exists():
        shutil.rmtree(mdir)


# --- Reads ------------------------------------------------------------
def export(metric: str, start_ms: int | None = None, end_ms: int | None = None):
    """Return (timestamps_ms, values) for a metric, ascending by ts.

    Used for presence metrics (small, and incremental callers pass
    start_ms to bound the scan).
    """
    if not _has_files(metric):
        return [], []
    where, params = [], []
    if start_ms is not None:
        where.append("ts >= ?")
        params.append(int(start_ms))
    if end_ms is not None:
        where.append("ts < ?")
        params.append(int(end_ms))
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    rows = _connect().execute(
        f"SELECT ts, value FROM read_parquet('{_metric_glob(metric)}') "
        f"{where_sql} ORDER BY ts",
        params,
    ).fetchall()
    if not rows:
        return [], []
    ts_list, val_list = zip(*rows)
    return [int(t) for t in ts_list], list(val_list)


def load_rr_intervals_chunks(
    min_ts_ms: int | None = None,
    max_ts_ms: int | None = None,
    chunk_rows: int = DEFAULT_CSV_CHUNK_ROWS,
):
    """Stream rr_interval_ms as (ts_ms, rr) numpy chunks, ascending by ts.

    rr_interval_ms carries unique, physically-reconstructed per-beat
    timestamps (gadgetbridge_migrate.py), so ascending ts order already
    reproduces the device order.
    """
    import numpy as np

    if not _has_files("rr_interval_ms"):
        return
    where, params = [], []
    if min_ts_ms is not None:
        where.append("ts >= ?")
        params.append(int(min_ts_ms))
    if max_ts_ms is not None:
        where.append("ts < ?")
        params.append(int(max_ts_ms))
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    con = _connect()
    con.execute(
        f"SELECT ts, value FROM read_parquet('{_metric_glob('rr_interval_ms')}') "
        f"{where_sql} ORDER BY ts",
        params,
    )
    # Chunked pandas fetch (no PyArrow dependency for the read path either).
    # DuckDB hands out chunks in units of its internal vector size (2048
    # rows), so approximate the requested chunk_rows in those units.
    vectors_per_chunk = max(1, chunk_rows // 2048)
    while True:
        df = con.fetch_df_chunk(vectors_per_chunk)
        if df.empty:
            break
        ts = df["ts"].to_numpy(dtype=np.int64, copy=False)
        rr = df["value"].to_numpy(dtype=np.float64, copy=False)
        yield ts, rr


def load_rr_intervals(min_ts_ms: int | None = None, max_ts_ms: int | None = None):
    """Full-series convenience wrapper around load_rr_intervals_chunks()."""
    import numpy as np

    chunks = list(load_rr_intervals_chunks(min_ts_ms=min_ts_ms, max_ts_ms=max_ts_ms))
    if not chunks:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.float64)
    ts = np.concatenate([c[0] for c in chunks])
    rr = np.concatenate([c[1] for c in chunks])
    if ts.size and not np.all(ts[:-1] <= ts[1:]):
        order = np.argsort(ts, kind="stable")
        ts, rr = ts[order], rr[order]
    return ts, rr
