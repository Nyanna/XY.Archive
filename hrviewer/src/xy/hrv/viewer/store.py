"""Storage backend abstraction for the read path.

The HR-Viewer read path used to talk to DuckDB directly. It now goes through
the :class:`Store` interface, which has two interchangeable implementations
selected by ``config.backend``:

* ``duckdb``      -- :class:`~xy.hrv.viewer.db.DuckDbStore`, the original
  streaming DuckDB access (default, main server).
* ``fastparquet`` -- :class:`~xy.hrv.viewer.fpstore.FastparquetStore`, a pure
  pandas/fastparquet reimplementation of the same queries for hosts where
  DuckDB is unavailable (e.g. the NanoPi mirror).

Both return :class:`~xy.hrv.viewer.arrow_ipc.QueryResult` objects, so the HTTP
layer is backend-agnostic and always emits the identical Arrow IPC stream.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from .arrow_ipc import QueryResult
from .config import Config


class Store(ABC):
    """Read-only access to the Parquet Hive, returning Arrow results."""

    @abstractmethod
    def series(
        self,
        segment: str,
        metric: str,
        start_ms: int,
        end_ms: int,
        max_points: int | None = None,
        agg: str = "avg",
    ) -> QueryResult:
        ...

    @abstractmethod
    def dominance_daily(self, start_ms: int, end_ms: int) -> QueryResult:
        ...

    @abstractmethod
    def sleep_daily(
        self, start_ms: int, end_ms: int, session: str = "after"
    ) -> QueryResult:
        ...

    @abstractmethod
    def close(self) -> None:
        ...


def create_store(config: Config) -> Store:
    """Instantiate the read backend selected by ``config.backend``."""
    backend = (config.backend or "duckdb").lower()
    if backend == "duckdb":
        from .db import DuckDbStore

        return DuckDbStore(config)
    if backend == "fastparquet":
        from .fpstore import FastparquetStore

        return FastparquetStore(config)
    raise ValueError(
        f"unknown backend {backend!r} (expected 'duckdb' or 'fastparquet')"
    )
