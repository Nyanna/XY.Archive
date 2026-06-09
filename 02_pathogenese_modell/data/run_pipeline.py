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


def main() -> None:
    _, passthrough_args = argparse.ArgumentParser(add_help=False).parse_known_args()

    t_total = time.monotonic()

    t_download = ensure_db()
    if t_download > 0:
        print(f"Download time: {t_download:.1f}s")

    run("gadgetbridge_migrate.py", passthrough_args)
    run("hrv_aggregate.py",        passthrough_args)
    run("spectral_bands_aggregate.py", passthrough_args)

    print(f"Total time: {time.monotonic() - t_total:.1f}s")


if __name__ == "__main__":
    main()
