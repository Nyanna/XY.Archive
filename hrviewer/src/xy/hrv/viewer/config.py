"""Runtime configuration for the HR Viewer.

All values can be overridden via environment variables or CLI arguments.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

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

    @property
    def statics_dir(self) -> Path:
        return (Path.cwd() / STATICS_DIR).resolve()

    def hive_glob(self, segment: str, metric: str) -> str:
        """Return the parquet glob for a single (segment, metric) pair.

        The Hive layout is ``segment=<s>/metric=<m>/dt=<date>/data.parquet``.
        """
        return os.path.join(
            self.hive_path,
            f"segment={segment}",
            f"metric={metric}",
            "*",
            "*.parquet",
        )
