#!/usr/bin/env python3
"""Pipeline: download → gadgetbridge_migrate → hrv_aggregate → spectral_bands_aggregate.

Stops immediately if any step exits with a non-zero return code.
Prints per-script and total runtimes on completion.
"""

import argparse
import os
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

HIVE_PATH = HERE / "hive"
HIVE_SSH_KEY = Path("/home/user/.ssh/hivebee")
HIVE_SSH_USER = "hivebee"
HIVE_SSH_HOST = "proxy.xyan.icu"
HIVE_REMOTE_DIR = "/home/admin/hive"
HIVE_RCLONE_REMOTE_NAME = "hivebee"
# No path suffix: server_command below already anchors the served fs at
# HIVE_REMOTE_DIR, so the remote root *is* the Hive dir.
HIVE_RCLONE_REMOTE = f"{HIVE_RCLONE_REMOTE_NAME}:"
# Define the sftp remote purely via env vars (no rclone.conf entry needed).
# Only the `rclone` binary is permitted to run on the remote side (no plain
# ssh/sftp-subsystem/rsync access there anymore), so instead of the regular
# SSH "sftp" subsystem we run `rclone serve sftp --stdio` as the remote
# command over the SSH exec channel — the rclone equivalent of how rsync
# spawns a remote `rsync --server` and talks to it over stdin/stdout.
# The installed rclone version (1.53.3) also doesn't support on-the-fly
# ":sftp,host=...:" connection strings, so RCLONE_CONFIG_<NAME>_* env vars
# are used instead. Merged into the subprocess env in sync_hive().
HIVE_RCLONE_ENV = {
    "RCLONE_CONFIG_HIVEBEE_TYPE": "sftp",
    "RCLONE_CONFIG_HIVEBEE_HOST": HIVE_SSH_HOST,
    "RCLONE_CONFIG_HIVEBEE_USER": HIVE_SSH_USER,
    "RCLONE_CONFIG_HIVEBEE_KEY_FILE": str(HIVE_SSH_KEY),
    "RCLONE_CONFIG_HIVEBEE_SERVER_COMMAND": f"rclone serve sftp --stdio {HIVE_REMOTE_DIR}",
}
# Only sync the Hive partitions (segment=*), never the remote user's home-dir
# clutter (.bash_history, .ssh, ...) that happens to live in the same dir.
HIVE_RCLONE_FILTERS = ["--filter=+ segment=*/**", "--filter=- *"]
# Strictly sequential, single-connection transfer to keep RAM usage minimal:
# one file in flight at a time, no parallel checkers/listers, small buffer
# (default is 16M per transfer; 1M keeps footprint tiny since we never run
# more than one transfer at once anyway).
HIVE_RCLONE_LOWMEM_FLAGS = [
    "--transfers=1",
    "--checkers=1",
    "--buffer-size=1M",
    "--use-mmap",
]
# Progress reporting: "--progress" redraws a single line via carriage-return
# cursor control, which only makes sense on an interactive terminal — when
# the pipeline runs unattended (cron/systemd timer, output redirected to a
# logfile), that turns into an unreadable wall of \r-separated garbage. So we
# pick the flavour based on whether stdout is actually a terminal.
HIVE_RCLONE_PROGRESS_FLAGS = (
    ["--progress"] if sys.stdout.isatty() else ["--stats=15s", "--stats-one-line"]
)


def sync_hive(direction: str) -> None:
    """Sync the local Hive with the remote copy via rclone (sequential, low-RAM).

    direction="pull": remote -> local (fetch the latest Hive before running).
    direction="push": local -> remote (upload the changes made by this run).

    Uses `rclone copy` (not `sync`) to mirror the previous `rsync -a` behaviour:
    files are copied/updated but nothing is deleted on the destination.
    """
    HIVE_PATH.mkdir(parents=True, exist_ok=True)
    local = str(HIVE_PATH)
    if direction == "pull":
        src, dst = HIVE_RCLONE_REMOTE, local
    elif direction == "push":
        src, dst = local, HIVE_RCLONE_REMOTE
    else:
        raise ValueError(f"invalid direction: {direction}")

    cmd = [
        "rclone", "copy",
        *HIVE_RCLONE_FILTERS,
        *HIVE_RCLONE_LOWMEM_FLAGS,
        *HIVE_RCLONE_PROGRESS_FLAGS,
        src, dst,
    ]
    print(f"Syncing Hive ({direction}) via rclone: {src} -> {dst}")
    t = time.monotonic()
    result = subprocess.run(cmd, env={**os.environ, **HIVE_RCLONE_ENV})
    elapsed = time.monotonic() - t
    if result.returncode != 0:
        print(f"ERROR: rclone ({direction}) exited with code {result.returncode}. Aborting pipeline.")
        sys.exit(result.returncode)
    print(f"Runtime [rclone {direction}]: {elapsed:.1f}s")


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

    #sync_hive("pull")

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

    sync_hive("push")

    print(f"\nTotal time: {time.monotonic() - t_total:.1f}s")


if __name__ == "__main__":
    main()
