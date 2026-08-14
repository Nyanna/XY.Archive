"""CLI entry point: ``python -m xy.hrv.viewer`` / console script ``hrv``."""
from __future__ import annotations

import argparse

from .app import HrViewer
from .config import Config


def build_config(argv: list[str] | None = None) -> Config:
    cfg = Config()  # env-based defaults
    parser = argparse.ArgumentParser(
        prog="hrv",
        description="HRV Viewer -- DuckDB/Arrow backed dashboard (read-only).",
    )
    parser.add_argument("--host", default=cfg.host, help="Bind host")
    parser.add_argument("--port", type=int, default=cfg.port, help="Bind port")
    parser.add_argument("--hive", default=cfg.hive_path, help="Parquet Hive path")
    parser.add_argument("--memory-limit", default=cfg.memory_limit)
    parser.add_argument("--threads", type=int, default=cfg.threads)
    parser.add_argument("--max-points", type=int, default=cfg.max_points)
    parser.add_argument("--debug", action="store_true", default=cfg.debug)
    args = parser.parse_args(argv)

    cfg.host = args.host
    cfg.port = args.port
    cfg.hive_path = args.hive
    cfg.memory_limit = args.memory_limit
    cfg.threads = args.threads
    cfg.max_points = args.max_points
    cfg.debug = args.debug
    return cfg


def main(argv: list[str] | None = None) -> None:
    HrViewer(build_config(argv)).run()


if __name__ == "__main__":
    main()
