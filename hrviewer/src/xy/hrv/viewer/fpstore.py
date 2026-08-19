"""Pure-Python read backend on top of pandas + fastparquet.

Drop-in alternative to :class:`~xy.hrv.viewer.db.DuckDbStore` for hosts where
DuckDB is unavailable (the NanoPi mirror). It reimplements the exact same
queries the DuckDB store runs, entirely in pandas/numpy, and returns the same
:class:`~xy.hrv.viewer.arrow_ipc.ColumnsResult` (nanoarrow -> Arrow IPC).

Scope note: this backend reads *its own* fastparquet-written Hive (the mirror
builds its Hive from MQTT via :class:`~xy.mqttduck.writer.FastparquetSink`); it
does not need to read the main server's DuckDB-written Parquet (which may use
encodings fastparquet cannot decode). The two servers are independent and each
reads only the format it writes.

The throughput requirements here are modest (a single-user mirror), so the
implementation favours simplicity and stability over the DuckDB store's
streaming/partition-pruning sophistication.
"""
from __future__ import annotations

import glob as _glob
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import fastparquet

from .arrow_ipc import ColumnsResult, QueryResult
from .config import Config
from .store import Store

_DAY_MS = 86_400_000
# epoch_ms(TIMESTAMP '2026-01-01') -- the sleep-session split point.
_SLEEP_SPLIT_MS = int(datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)


def _empty(columns: list[str]) -> ColumnsResult:
    return ColumnsResult(
        {c: np.array([], dtype=np.int64 if c != "value" else np.float64)
         for c in columns}
    )


class FastparquetStore(Store):
    """Read-only access to a fastparquet-written Hive via pandas."""

    def __init__(self, config: Config):
        self._cfg = config

    # -- file selection ------------------------------------------------
    def _read(self, files: list[str], columns: list[str]) -> pd.DataFrame:
        if not files:
            return pd.DataFrame({c: pd.Series(dtype="float64") for c in columns})
        return fastparquet.ParquetFile(files).to_pandas(columns=columns)

    def _partition_files(
        self,
        p0: str, selector: str,
        p1: str, metric: str,
        time_part: str, lo: str, hi: str,
    ) -> list[str]:
        """Collect *.parquet whose time-partition value lies in [lo, hi].

        Both the daily (``YYYY-MM-DD``) and monthly (``YYYY-MM``) schemes order
        correctly as strings, so a lexical range prunes the file scan just like
        DuckDB's ``BETWEEN`` on the Hive partition column.
        """
        base = Path(self._cfg.hive_path) / f"{p0}={selector}" / f"{p1}={metric}"
        out: list[str] = []
        for d in sorted(base.glob(f"{time_part}=*")):
            value = d.name.split("=", 1)[1]
            if lo <= value <= hi:
                out.extend(sorted(_glob.glob(str(d / "*.parquet"))))
        return out

    def _series_files(
        self, selector: str, metric: str, start_ms: int, end_ms: int
    ) -> list[str]:
        p0, p1 = self._cfg.part_names
        tp = self._cfg.time_part
        lo = str(self._cfg.part_value(start_ms))
        hi = str(self._cfg.part_value(end_ms))
        return self._partition_files(p0, selector, p1, metric, tp, lo, hi)

    def _daily_files(
        self, segment: str, metric: str, lo_date, hi_date
    ) -> list[str]:
        # HRV daily queries always use the segment/metric/dt layout.
        return self._partition_files(
            "segment", segment, "metric", metric, "dt", str(lo_date), str(hi_date)
        )

    # -- series --------------------------------------------------------
    def series(
        self,
        segment: str,
        metric: str,
        start_ms: int,
        end_ms: int,
        max_points: int | None = None,
        agg: str = "avg",
    ) -> QueryResult:
        agg = (agg or "avg").lower()
        max_points = max_points or self._cfg.max_points
        files = self._series_files(segment, metric, start_ms, end_ms)
        df = self._read(files, ["ts", "value"])
        df = df[(df["ts"] >= start_ms) & (df["ts"] <= end_ms)]

        if agg == "none":
            df = df.sort_values("ts").head(max(1, int(max_points)))
            return ColumnsResult({
                "ts": df["ts"].to_numpy(np.int64),
                "value": df["value"].to_numpy(np.float64),
            })

        if df.empty:
            return _empty(["ts", "value"])

        span = max(1, end_ms - start_ms)
        bucket = max(1, span // max(1, int(max_points)))
        buckets = (df["ts"].to_numpy(np.int64) // bucket) * bucket
        grp = pd.DataFrame({"ts": buckets, "value": df["value"].to_numpy(np.float64)})

        if agg == "spread":
            agg_df = grp.groupby("ts", sort=True)["value"].agg(["max", "min", "mean"])
            # (max - min) / NULLIF(avg, 0) -> NaN where avg == 0 (Arrow null).
            value = (agg_df["max"] - agg_df["min"]) / agg_df["mean"].replace(0, np.nan)
            ts_out = agg_df.index.to_numpy(np.int64)
            val_out = value.to_numpy(np.float64)
        else:  # avg (default)
            mean = grp.groupby("ts", sort=True)["value"].mean()
            ts_out = mean.index.to_numpy(np.int64)
            val_out = mean.to_numpy(np.float64)

        return ColumnsResult({"ts": ts_out, "value": val_out})

    # -- dominance_daily ----------------------------------------------
    def dominance_daily(self, start_ms: int, end_ms: int) -> QueryResult:
        files = self._daily_files(
            "hrv", "hrv_b7b8_dom", _ms_to_date(start_ms), _ms_to_date(end_ms)
        )
        df = self._read(files, ["ts", "value"])
        df = df[(df["ts"] >= start_ms) & (df["ts"] <= end_ms) & (df["value"] < -0.5)]
        if df.empty:
            return _empty(["ts", "value"])
        day = (df["ts"].to_numpy(np.int64) // _DAY_MS) * _DAY_MS
        grp = pd.DataFrame({"ts": day, "value": df["value"].to_numpy(np.float64) + 0.5})
        s = grp.groupby("ts", sort=True)["value"].sum()
        return ColumnsResult({
            "ts": s.index.to_numpy(np.int64),
            "value": s.to_numpy(np.float64),
        })

    # -- sleep_daily ---------------------------------------------------
    def sleep_daily(
        self, start_ms: int, end_ms: int, session: str = "after"
    ) -> QueryResult:
        sess_files = self._daily_files(
            "raw", "sleep_timestamp", _ms_to_date(start_ms), _ms_to_date(end_ms)
        )
        stage_files = self._daily_files(
            "raw", "sleep_stage", _ms_to_date(start_ms - _DAY_MS), _ms_to_date(end_ms)
        )
        sess = self._read(sess_files, ["ts", "value"])
        sess = sess[(sess["ts"] >= start_ms) & (sess["ts"] <= end_ms)]
        stages = self._read(stage_files, ["ts", "value"])

        bed = sess["value"].to_numpy(np.int64)
        wake = sess["ts"].to_numpy(np.int64)
        keep = (bed < _SLEEP_SPLIT_MS) if session == "before" else (bed > _SLEEP_SPLIT_MS)
        bed, wake = bed[keep], wake[keep]
        if len(bed) == 0 or stages.empty:
            return _empty(["ts", "phases", "deep", "rem"])

        stage_ms = stages["ts"].to_numpy(np.int64)
        stage = stages["value"].to_numpy(np.float64)
        phases: dict[int, int] = defaultdict(int)
        deep: dict[int, int] = defaultdict(int)
        rem: dict[int, int] = defaultdict(int)
        # Sessions are sparse (one per night) -> a per-session mask is cheap and
        # reproduces the DuckDB range-join (a stage counts once per session it
        # falls into), grouped by the wake-up day.
        for b, w in zip(bed, wake):
            m = (stage_ms >= b) & (stage_ms <= w)
            if not m.any():
                continue
            day = int((w // _DAY_MS) * _DAY_MS)
            phases[day] += int(m.sum())
            deep[day] += int(((stage == 2) & m).sum())
            rem[day] += int(((stage == 4) & m).sum())

        days = sorted(phases)
        return ColumnsResult({
            "ts": np.array(days, dtype=np.int64),
            "phases": np.array([phases[d] for d in days], dtype=np.int64),
            "deep": np.array([deep[d] for d in days], dtype=np.int64),
            "rem": np.array([rem[d] for d in days], dtype=np.int64),
        })

    # -- lifecycle -----------------------------------------------------
    def close(self) -> None:
        # Stateless (files opened per query) -- nothing to release.
        pass


def _ms_to_date(ms: int):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date()
