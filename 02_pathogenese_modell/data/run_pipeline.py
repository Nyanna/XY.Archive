#!/usr/bin/env python3
"""Pipeline: download → gadgetbridge_migrate → hrv_aggregate → spectral_bands_aggregate.

Stops immediately if any step exits with a non-zero return code.
Prints per-script and total runtimes on completion.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

import gdown

import hive_io as vm_io

HERE = Path(__file__).parent
DB_PATH = HERE / "Gadgetbridge"
DB_REMOTE_URL = "https://drive.google.com/file/d/1yropB-j0couqP8f-XItaAJm3dVsfgc1t/view?usp=sharing"
DB_TMP_PATH = DB_PATH.with_suffix(".tmp")


class _SameSize(Exception):
    pass


def ensure_db() -> float:
    """Download DB if remote size differs from local. Returns elapsed time (0.0 if skipped).

    Downloads to a .tmp file so the existing DB is never corrupted on abort.
    The progress callback aborts as soon as bytes_total matches the local file
    size — at most one chunk is written to .tmp before cancellation.
    """
    local_size = DB_PATH.stat().st_size if DB_PATH.exists() else -1
    skip_reason: str | None = None

    def _progress(bytes_so_far: int, bytes_total: int | None) -> None:
        nonlocal skip_reason
        if bytes_total is not None and bytes_total == local_size:
            skip_reason = f"remote size matches local ({local_size:,} bytes)"
            raise _SameSize

    t = time.monotonic()
    try:
        gdown.download(DB_REMOTE_URL, str(DB_TMP_PATH), quiet=False, progress=_progress)
        DB_TMP_PATH.replace(DB_PATH)
        elapsed = time.monotonic() - t
    except _SameSize:
        for f in HERE.glob(DB_TMP_PATH.name + "*"):
            f.unlink(missing_ok=True)
        elapsed = 0.0

    if skip_reason:
        print(f"Download skipped: {skip_reason}.")

    if not DB_PATH.exists():
        print(f"ERROR: database not found: {DB_PATH}")
        sys.exit(1)
    return elapsed


def run(script: str, args: list[str]) -> None:
    """Run a Python script as subprocess, print its runtime, abort pipeline on error."""
    t = time.monotonic()
    result = subprocess.run([sys.executable, str(HERE / script), *args])
    elapsed = time.monotonic() - t
    if result.returncode != 0:
        print(f"ERROR: {script} exited with code {result.returncode}. Aborting pipeline.")
        sys.exit(result.returncode)
    print(f"Runtime [{script}]: {elapsed:.1f}s")


def run_pipeline_once(db_file: Path, passthrough_args: list[str]) -> None:
    """Import one source DB and run the aggregators over the resulting Hive.

    The concrete source file is passed straight to gadgetbridge_migrate via
    --db (no copy to a constant working path). The aggregators then operate
    on the Hive that this import produced. Every stage shares the same --full
    flag name, so passthrough args (e.g. --full, --limit-minutes) are simply
    forwarded to all stages unchanged.
    """
    run("gadgetbridge_migrate.py", ["--db", str(db_file), *passthrough_args])
    vm_io.force_flush()

    run("hrv_aggregate.py",        passthrough_args)
    run("spectral_bands_aggregate.py", passthrough_args)


def main() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--db",
        nargs="+",
        type=Path,
        metavar="DB_FILE",
        help=(
            "Process one or more local Gadgetbridge SQLite files in sequence "
            "instead of the default DB (supports shell wildcards, e.g. "
            "--db /path/to/*.db). Skips the remote download step."
        ),
    )
    args, passthrough_args = parser.parse_known_args()

    t_total = time.monotonic()

    if args.db:
        db_files = sorted(args.db)
        print(f"Processing {len(db_files)} local database file(s), download skipped.")
        for i, db_file in enumerate(db_files, start=1):
            print(f"\n=== [{i}/{len(db_files)}] {db_file} ===")
            if not db_file.exists():
                print(f"ERROR: database file not found: {db_file}")
                sys.exit(1)
            run_pipeline_once(db_file, passthrough_args)
    else:
        t_download = ensure_db()
        if t_download > 0:
            print(f"Download time: {t_download:.1f}s")
        run_pipeline_once(DB_PATH, passthrough_args)

    print(f"\nTotal time: {time.monotonic() - t_total:.1f}s")


if __name__ == "__main__":
    main()
