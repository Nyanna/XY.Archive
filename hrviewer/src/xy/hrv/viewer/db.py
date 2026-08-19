"""DuckDB data access layer.

The Hive is streamed directly from disk on every query. Queries are built as
parameterised DuckDB *relations* (``con.sql(sql, params=...)``): relations are
injection-safe and expose the Arrow C stream interface natively, so results are
handed to the browser as zero-copy Arrow IPC via nanoarrow -- no PyArrow, no
intermediate table materialisation.
"""
from __future__ import annotations

import threading
from datetime import datetime, timezone

import duckdb
import numpy as np

from .arrow_ipc import QueryResult, stream_to_ipc
from .config import Config
from .store import Store


class RelationResult(QueryResult):
    """A lazy DuckDB relation wrapped as a backend-neutral query result.

    Execution happens when the result is serialised, guarded by the shared
    connection lock (the HTTP server is sequential; the only other user of the
    connection is the MQTT-Duck writer thread). The relation exposes the Arrow
    C stream interface, so ``to_ipc`` streams straight to IPC bytes.
    """

    def __init__(self, relation, lock: threading.Lock):
        self._rel = relation
        self._lock = lock

    def to_ipc(self) -> bytes:
        with self._lock:
            return stream_to_ipc(self._rel)

    def to_pydict(self) -> dict[str, list]:
        with self._lock:
            cols = self._rel.fetchnumpy()
        out: dict[str, list] = {}
        for name, values in cols.items():
            if np.ma.isMaskedArray(values):
                out[name] = [
                    None if m else _py(v) for v, m in zip(values.data, values.mask)
                ]
            else:
                out[name] = [_py(v) for v in values]
        return out


def _py(v):
    if isinstance(v, np.floating):
        f = float(v)
        return None if f != f else f
    if isinstance(v, np.integer):
        return int(v)
    return v


class DuckDbStore(Store):
    """Read-only, streaming access to the Parquet Hive via DuckDB."""

    def __init__(self, config: Config):
        self._cfg = config
        self._lock = threading.Lock()
        # `import duckdb` also brings up a separate, hidden module-level
        # `default_connection` (backing the top-level convenience API,
        duckdb.default_connection().execute(
            f"SET threads={max(1, self._cfg.threads)}"
        )
        # Pass `threads` in via the connect-time config
        self._con = duckdb.connect(
            database=":memory:",
            config={
                "threads": str(self._cfg.threads),
                "autoload_known_extensions": "false",
                },
            )
        self._configure()

    def _configure(self) -> None:
        con = self._con
        con.execute(f"SET memory_limit='{self._cfg.memory_limit}'")
        # No caching: read straight from disk every time.
        con.execute("SET enable_object_cache=false")
        # We never need row ordering to be preserved across scans -> less RAM.
        con.execute("SET preserve_insertion_order=false")

    def _sql(self, sql: str, params: list) -> RelationResult:
        """Build a parameterised relation under the lock, wrap it as a result."""
        with self._lock:
            rel = self._con.sql(sql, params=params)
        return RelationResult(rel, self._lock)

    # ------------------------------------------------------------------
    # Aggregate expressions selectable via the ``agg`` request parameter.
    #
    #   avg    -- arithmetic mean of the bucket (default)
    #   none   -- raw samples, no bucketing, no aggregation
    #   spread -- relative spread, used for RR intervals:
    #                 (MAX(value) - MIN(value)) / NULLIF(AVG(value), 0)
    _AGG_EXPR = {
        "avg": "avg(value)",
        "spread": "(max(value) - min(value)) / NULLIF(avg(value), 0)",
    }

    def series(
        self,
        segment: str,
        metric: str,
        start_ms: int,
        end_ms: int,
        max_points: int | None = None,
        agg: str = "avg",
    ) -> QueryResult:
        """Return a time series as an Arrow result (``ts``, ``value``).

        ``ts`` is epoch milliseconds (UTC). ``agg`` selects the aggregate
        function applied inside uniform time buckets:

        * ``avg``    -- bucket mean (default), bounded by ``max_points``;
        * ``spread`` -- relative RR spread ``(max-min)/avg`` per bucket;
        * ``none``   -- raw samples, no bucketing (for sparse metrics).
        """
        agg = (agg or "avg").lower()
        glob = self._cfg.hive_glob(segment, metric)
        tp = self._cfg.time_part
        start_part = self._cfg.part_value(start_ms)
        end_part = self._cfg.part_value(end_ms)

        if agg == "none":
            max_points = max_points or self._cfg.max_points
            sql = f"""
                SELECT ts, value
                FROM read_parquet(?, hive_partitioning=true)
                WHERE {tp} BETWEEN ? AND ?
                  AND ts BETWEEN ? AND ?
                ORDER BY ts
                LIMIT ?
            """
            params = [glob, start_part, end_part, start_ms, end_ms,
                      max(1, int(max_points))]
            return self._sql(sql, params)

        expr = self._AGG_EXPR.get(agg, self._AGG_EXPR["avg"])
        max_points = max_points or self._cfg.max_points
        span = max(1, end_ms - start_ms)
        bucket = max(1, span // max(1, max_points))

        sql = f"""
            SELECT
                (ts // {bucket}) * {bucket}                AS ts,
                {expr}                                     AS value
            FROM read_parquet(?, hive_partitioning=true)
            WHERE {tp} BETWEEN ? AND ?
              AND ts BETWEEN ? AND ?
            GROUP BY 1
            ORDER BY 1
        """
        params = [glob, start_part, end_part, start_ms, end_ms]
        return self._sql(sql, params)

    # ------------------------------------------------------------------
    def dominance_daily(self, start_ms: int, end_ms: int) -> QueryResult:
        """Daily sympathetic-dominance time below the -0.5 threshold.

        Reproduces the Grafana "Sympathic Dominance Time under threshold"
        panel: ``SUM(value + 0.5)`` over ``hrv_b7b8_dom`` samples < -0.5,
        grouped by calendar day. Returns (``ts``, ``value``).
        """
        glob = self._cfg.hive_glob("hrv", "hrv_b7b8_dom")
        sql = """
            SELECT
                epoch_ms(date_trunc('day', to_timestamp(ts / 1000)))::BIGINT AS ts,
                SUM(value + 0.5)                                             AS value
            FROM read_parquet(?, hive_partitioning=true)
            WHERE dt BETWEEN ? AND ?
              AND ts BETWEEN ? AND ?
              AND value < -0.5
            GROUP BY 1
            ORDER BY 1
        """
        params = [glob, _ms_to_date(start_ms), _ms_to_date(end_ms),
                  start_ms, end_ms]
        return self._sql(sql, params)

    def sleep_daily(
        self, start_ms: int, end_ms: int, session: str = "after"
    ) -> QueryResult:
        """Daily sleep-phase counts per sleep session (Grafana panels 7/8).

        A session spans ``bed_ms`` (value of ``sleep_timestamp``) to
        ``wake_ms`` (its ``ts``). Stage samples inside a session are counted
        into ``phases`` (all), ``deep`` (stage 2) and ``rem`` (stage 4),
        grouped by the wake-up day. ``session`` selects whether the bed time
        lies ``before`` or ``after`` 2026-01-01.
        """
        cmp = "<" if session == "before" else ">"
        sess_glob = self._cfg.hive_glob("raw", "sleep_timestamp")
        stage_glob = self._cfg.hive_glob("raw", "sleep_stage")
        # Stages can start the evening before the wake day -> widen the lower
        # bound of the stage partition scan by one day.
        stage_lo = _ms_to_date(start_ms - 86_400_000)
        stage_hi = _ms_to_date(end_ms)
        sql = f"""
            WITH sessions AS (
                SELECT CAST(value AS BIGINT) AS bed_ms, ts AS wake_ms
                FROM read_parquet(?, hive_partitioning=true)
                WHERE ts BETWEEN ? AND ?
            ),
            stages AS (
                SELECT ts AS stage_ms, value AS stage
                FROM read_parquet(?, hive_partitioning=true)
                WHERE dt BETWEEN ? AND ?
            )
            SELECT
                epoch_ms(date_trunc('day', to_timestamp(s.wake_ms / 1000)))::BIGINT AS ts,
                COUNT(*)                              AS phases,
                COUNT(*) FILTER (WHERE st.stage = 2)  AS deep,
                COUNT(*) FILTER (WHERE st.stage = 4)  AS rem
            FROM stages st
            JOIN sessions s
              ON st.stage_ms >= s.bed_ms
             AND st.stage_ms <= s.wake_ms
             AND s.bed_ms {cmp} epoch_ms(TIMESTAMP '2026-01-01')
            GROUP BY 1
            ORDER BY 1
        """
        params = [sess_glob, start_ms, end_ms,
                  stage_glob, stage_lo, stage_hi]
        return self._sql(sql, params)

    # ------------------------------------------------------------------
    def close(self) -> None:
        with self._lock:
            self._con.close()


# Backwards-compatible alias (the class used to be called ``HiveStore``).
HiveStore = DuckDbStore


def _ms_to_date(ms: int):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date()
