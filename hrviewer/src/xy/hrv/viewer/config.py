"""Runtime configuration for the HR Viewer.

All values can be overridden via environment variables or CLI arguments.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar

# The server is always started from the project root.
STATICS_DIR: Path = Path("statics")

# Default location of the Parquet Hive.
DEFAULT_HIVE_PATH = "/home/user/xyan/XY.Archiv/hrviewer/hive"


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(slots=True)
class Config:
    """Central server configuration."""

    host: str = field(default_factory=lambda: _env("HRV_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(_env("HRV_PORT", "8080")))
    debug: bool = field(default_factory=lambda: _env("HRV_DEBUG", "0") == "1")

    hive_path: str = field(
        default_factory=lambda: _env("HRV_HIVE_PATH", DEFAULT_HIVE_PATH)
    )

    # DuckDB tuning
    memory_limit: str = field(default_factory=lambda: _env("HRV_MEMORY_LIMIT", "64MB"))
    threads: int = field(default_factory=lambda: int(_env("HRV_THREADS", "1")))

    # Query defaults
    max_points: int = field(default_factory=lambda: int(_env("HRV_MAX_POINTS", "5000")))

    # ------------------------------------------------------------------
    # Partition scheme.
    #
    # A Hive addresses a single logical series by two *selector* partitions
    # (the first picks the top level, the second the metric) followed by one
    # *time* partition. The HR-Viewer's own Hive is laid out as
    # ``segment=<s>/metric=<m>/dt=<YYYY-MM-DD>/``. Subclasses (e.g. the
    # MQTT-Duck sensor Hive ``sensor=<s>/metric=<m>/month=<YYYY-MM>/``) only
    # override these three names + ``part_value`` and inherit every query.
    part_names: ClassVar[tuple[str, str]] = ("segment", "metric")
    time_part: ClassVar[str] = "dt"

    @property
    def statics_dir(self) -> Path:
        return (Path.cwd() / STATICS_DIR).resolve()

    def hive_glob(self, selector: str, metric: str) -> str:
        """Return the parquet glob for a single (selector, metric) pair.

        The generic Hive layout is
        ``<p0>=<selector>/<p1>=<metric>/<time>=<value>/*.parquet`` where the
        partition names come from :attr:`part_names` / :attr:`time_part`.
        """
        p0, p1 = self.part_names
        return os.path.join(
            self.hive_path,
            f"{p0}={selector}",
            f"{p1}={metric}",
            "*",
            "*.parquet",
        )

    def part_value(self, ms: int):
        """Map an epoch-ms timestamp to the value of the time partition.

        Returned so that lexical/temporal ``BETWEEN`` filtering over the
        partition column bounds the file scan. The default (daily) scheme
        returns a ``date``; monthly schemes return a ``YYYY-MM`` string.
        """
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date()
