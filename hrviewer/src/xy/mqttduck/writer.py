"""Buffered ingestion + monthly merge-on-write Hive sink.

Data flow (two threads, per the project design)::

    MQTT callback thread            Writer thread
    ------------------              -------------
    transform() -> Sample           drain queue
    buffer.put(sample)   ==Queue==> last-value dedup (cache)
                                    stage kept samples
                                    flush -> merge-on-write Parquet

Only samples that (a) *just* arrived via MQTT and (b) differ from the previous
value for their (sensor, metric) series are persisted -- no scraping, no
unchanged-value churn. The last value per series is cached; on first encounter
the cache is seeded from the Hive so restarts stay consistent.

The Hive layout is monthly (throughput is low)::

    <hive>/ sensor=<s> / metric=<m> / month=<YYYY-MM> / data.parquet   (ts, value)

Writes reuse the *same DuckDB connection* the HR-Viewer read path uses, guarded
by its lock, so ingestion and queries share one instance over one Hive.
"""
from __future__ import annotations

import os
import queue
import threading
from pathlib import Path

import pyarrow as pa

from .config import MqttConfig
from .transform import Sample


class HiveSink:
    """Monthly merge-on-write persistence into the sensor Hive.

    Uses the DuckDB connection + lock owned by the HR-Viewer ``HiveStore`` so
    reads and writes go through one instance. Each ``write`` groups the batch
    by (sensor, metric, month) and rewrites only the touched ``data.parquet``
    files as ``existing UNION new`` deduplicated on ``ts`` (new wins).
    """

    def __init__(self, cfg: MqttConfig, con, lock: threading.Lock):
        self._cfg = cfg
        self._con = con
        self._lock = lock
        self._hive = Path(cfg.hive_path)
        with self._lock:
            self._con.execute("SET TimeZone='UTC'")

    # -- paths ---------------------------------------------------------
    def _part_dir(self, sensor: str, metric: str, month: str) -> Path:
        return (
            self._hive
            / f"sensor={sensor}"
            / f"metric={metric}"
            / f"month={month}"
        )

    def _series_glob(self, sensor: str, metric: str) -> str:
        return str(
            self._hive
            / f"sensor={sensor}"
            / f"metric={metric}"
            / "month=*"
            / "*.parquet"
        )

    # -- reads ---------------------------------------------------------
    def latest_value(self, sensor: str, metric: str) -> float | None:
        """Newest stored value for a series, or None if it has no files."""
        import glob as _glob

        if not _glob.glob(self._series_glob(sensor, metric)):
            return None
        sql = (
            "SELECT value FROM read_parquet(?, hive_partitioning=true) "
            "ORDER BY ts DESC LIMIT 1"
        )
        with self._lock:
            row = self._con.execute(sql, [self._series_glob(sensor, metric)]).fetchone()
        return float(row[0]) if row and row[0] is not None else None

    # -- writes --------------------------------------------------------
    def write(self, samples: list[Sample]) -> int:
        """Merge a batch of samples into their monthly partitions.

        Returns the number of samples written.
        """
        if not samples:
            return 0

        # Group into (sensor, metric, month) -> {ts: value} (last write wins).
        groups: dict[tuple[str, str, str], dict[int, float]] = {}
        for s in samples:
            month = MqttConfig.month_of(s.ts_ms)
            groups.setdefault((s.sensor, s.metric, month), {})[s.ts_ms] = s.value

        written = 0
        with self._lock:
            for (sensor, metric, month), rows in groups.items():
                written += self._merge_partition(sensor, metric, month, rows)
        return written

    def _merge_partition(
        self, sensor: str, metric: str, month: str, rows: dict[int, float]
    ) -> int:
        pdir = self._part_dir(sensor, metric, month)
        pdir.mkdir(parents=True, exist_ok=True)
        final = pdir / "data.parquet"
        tmp = pdir / "data.parquet.tmp"

        ts_list = list(rows.keys())
        val_list = [rows[t] for t in ts_list]
        batch = pa.table({"ts": ts_list, "value": val_list})
        self._con.register("_smd_new", batch)

        existing = ""
        if final.exists():
            existing = (
                "UNION ALL SELECT ts, value, 0 AS prio "
                f"FROM read_parquet('{final.as_posix()}')"
            )
        try:
            self._con.execute(
                f"""
                COPY (
                  WITH u AS (
                    SELECT ts, value, 1 AS prio FROM _smd_new
                    {existing}
                  ),
                  d AS (
                    SELECT ts, value,
                           row_number() OVER (PARTITION BY ts
                                              ORDER BY prio DESC) AS rn
                    FROM u
                  )
                  SELECT ts, value FROM d WHERE rn = 1 ORDER BY ts
                ) TO '{tmp.as_posix()}'
                  (FORMAT PARQUET, PARQUET_VERSION V2, COMPRESSION ZSTD);
                """
            )
        finally:
            self._con.unregister("_smd_new")
        os.replace(tmp, final)
        return len(rows)


class SampleBuffer:
    """Thread-safe bounded queue between the MQTT thread and the writer."""

    def __init__(self, maxsize: int = 0):
        self._q: "queue.Queue[Sample]" = queue.Queue(maxsize=maxsize)
        self.dropped = 0

    def put(self, sample: Sample) -> None:
        try:
            self._q.put_nowait(sample)
        except queue.Full:
            # Never block the MQTT network loop; drop and count instead.
            self.dropped += 1

    def get(self, timeout: float | None = None) -> Sample | None:
        try:
            return self._q.get(timeout=timeout)
        except queue.Empty:
            return None

    def qsize(self) -> int:
        return self._q.qsize()


class WriterThread(threading.Thread):
    """Drains the buffer, deduplicates and flushes to the Hive sink.

    The last-value cache lives here (single owner -> lock-free). A sample is
    kept only if its value differs from the cached previous value for its
    series; the cache is seeded lazily from the Hive on first encounter.
    """

    def __init__(self, cfg: MqttConfig, buffer: SampleBuffer, sink: HiveSink):
        super().__init__(name="mqtt-duck-writer", daemon=True)
        self._cfg = cfg
        self._buf = buffer
        self._sink = sink
        self._stop_evt = threading.Event()
        self._last: dict[tuple[str, str], float] = {}
        self.written = 0
        self.deduped = 0

    def stop(self) -> None:
        self._stop_evt.set()

    def _keep(self, s: Sample) -> bool:
        key = (s.sensor, s.metric)
        if key not in self._last:
            seeded = self._sink.latest_value(s.sensor, s.metric)
            if seeded is not None:
                self._last[key] = seeded
        prev = self._last.get(key)
        if prev is not None and prev == s.value:
            self.deduped += 1
            return False
        self._last[key] = s.value
        return True

    def run(self) -> None:
        import time

        staged: list[Sample] = []
        last_flush = time.monotonic()
        interval = max(0.1, self._cfg.flush_interval_s)

        while not self._stop_evt.is_set():
            s = self._buf.get(timeout=0.5)
            if s is not None and self._keep(s):
                staged.append(s)

            due = (time.monotonic() - last_flush) >= interval
            full = len(staged) >= self._cfg.flush_max_samples
            if staged and (due or full):
                self.written += self._sink.write(staged)
                staged.clear()
                last_flush = time.monotonic()

        # Drain whatever is still queued, then final flush.
        while True:
            s = self._buf.get(timeout=0.0)
            if s is None:
                break
            if self._keep(s):
                staged.append(s)
        if staged:
            self.written += self._sink.write(staged)
