"""DuckDB data access layer.

The Hive is streamed directly from disk on every query. We explicitly:

* disable the object cache (``enable_object_cache=false``) so nothing is
  cached between requests,
* cap ``memory_limit`` to keep RAM usage minimal,
* never copy the data into DuckDB (no ``CREATE TABLE``); ``read_parquet`` reads
  the source files lazily and only the row-groups matching the predicate.

Results are handed out as Arrow tables/IPC so the browser can consume them via
apache-arrow without an intermediate JSON round-trip.
"""
from __future__ import annotations

import threading
from datetime import datetime, timezone

import duckdb
import pyarrow as pa

from .config import Config


class HiveStore:
    """Read-only, streaming access to the Parquet Hive via DuckDB."""

    def __init__(self, config: Config):
        self._cfg = config
        self._lock = threading.Lock()
        self._con = duckdb.connect(database=":memory:")
        self._configure()

    def _configure(self) -> None:
        con = self._con
        con.execute(f"SET memory_limit='{self._cfg.memory_limit}'")
        con.execute(f"SET threads={self._cfg.threads}")
        # No caching: read straight from disk every time.
        con.execute("SET enable_object_cache=false")
        # We never need row ordering to be preserved across scans -> less RAM.
        con.execute("SET preserve_insertion_order=false")

    # ------------------------------------------------------------------
    # Series query
    # ------------------------------------------------------------------
    def series(
        self,
        segment: str,
        metric: str,
        start_ms: int,
        end_ms: int,
        max_points: int | None = None,
    ) -> pa.Table:
        """Return a downsampled time series as an Arrow table (``ts``, ``value``).

        ``ts`` is epoch milliseconds (UTC). Values are averaged into uniform
        time buckets so the number of returned points never exceeds
        ``max_points`` -- this keeps memory bounded regardless of range width.
        """
        max_points = max_points or self._cfg.max_points
        span = max(1, end_ms - start_ms)
        bucket = max(1, span // max(1, max_points))

        glob = self._cfg.hive_glob(segment, metric)
        start_date = _ms_to_date(start_ms)
        end_date = _ms_to_date(end_ms)

        sql = f"""
            SELECT
                CAST((ts / {bucket}) AS BIGINT) * {bucket} AS ts,
                avg(value)                                 AS value
            FROM read_parquet(?, hive_partitioning=true)
            WHERE dt BETWEEN ? AND ?
              AND ts BETWEEN ? AND ?
            GROUP BY 1
            ORDER BY 1
        """
        params = [glob, start_date, end_date, start_ms, end_ms]
        with self._lock:
            return self._con.execute(sql, params).fetch_arrow_table()

    # ------------------------------------------------------------------
    def close(self) -> None:
        with self._lock:
            self._con.close()


def _ms_to_date(ms: int):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date()


def table_to_ipc(table: pa.Table) -> bytes:
    """Serialise an Arrow table to a self-contained IPC stream."""
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)
    return sink.getvalue().to_pybytes()
