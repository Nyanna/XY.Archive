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

import hive_io as be_io

HERE = Path(__file__).parent

DB_PATH = Path(os.environ.get("HRV_DB_PATH", str(HERE / "Gadgetbridge")))
DB_REMOTE_URL = "https://drive.google.com/file/d/1yropB-j0couqP8f-XItaAJm3dVsfgc1t/view?usp=sharing"
DB_TMP_PATH = DB_PATH.with_suffix(".tmp")

HIVE_PATH = Path(os.environ.get("HIVE_PATH", str(HERE / "hive")))
HIVE_SSH_KEY = Path("/home/user/.ssh/hivebee")
HIVE_SSH_USER = "hivebee"
HIVE_SSH_HOST = "proxy.xyan.icu"

HIVE_REMOTE_DIR = os.environ.get("HIVE_REMOTE_DIR", "/home/admin/hive")
HIVE_GIT_BRANCH = "master"
# scp-like syntax so git tunnels the transfer over ssh (same key/host as the
# previous rsync/rclone setup); the remote side only permits running `git`
# (no plain shell/sftp/rsync anymore).
HIVE_GIT_REMOTE_URL = f"{HIVE_SSH_USER}@{HIVE_SSH_HOST}:{HIVE_REMOTE_DIR}"
# All git<->remote traffic (fetch/pull/push, plus the explicit remote
# worktree update below) goes through this ssh invocation with the dedicated
# key. Merged into the subprocess env for every git call in sync_hive().
HIVE_GIT_ENV = {
    **os.environ,
    "GIT_SSH_COMMAND": f"ssh -i {HIVE_SSH_KEY} -o SendEnv=GIT_PROTOCOL",
    "GIT_PROTOCOL": "version=2",
}


def _git(args: list[str]) -> None:
    """Run a git command against the local Hive repo, abort pipeline on error."""
    result = subprocess.run(
        ["git", "-c", "protocol.version=2", "-C", str(HIVE_PATH), *args],
        env=HIVE_GIT_ENV,
    )
    if result.returncode != 0:
        print(f"ERROR: git {' '.join(args)} exited with code {result.returncode}. Aborting pipeline.")
        sys.exit(result.returncode)


def _git_soft(args: list[str]) -> bool:
    """Run a git command against the local Hive repo without aborting the pipeline.

    Used for the remote-facing operations (pull/push)
    """
    result = subprocess.run(
        ["git", "-c", "protocol.version=2", "-C", str(HIVE_PATH), *args],
        env=HIVE_GIT_ENV,
    )
    return result.returncode == 0


def _origin_configured() -> bool:
    """Whether the local Hive repo has a usable `origin` remote to sync with."""
    remote = subprocess.run(
        ["git", "-C", str(HIVE_PATH), "remote", "get-url", "origin"],
        env=HIVE_GIT_ENV, capture_output=True, text=True,
    )
    return remote.returncode == 0 and bool(remote.stdout.strip())


def _same_path(a: Path, b: Path) -> bool:
    try:
        return a.resolve() == b.resolve()
    except OSError:
        return str(a) == str(b)


def _ensure_hive_repo() -> None:
    """Make sure the local Hive dir is a git repo, wiring up `origin` if useful.

    When HIVE_PATH already *is* HIVE_REMOTE_DIR (the server running this
    script directly inside its own Hive worktree).
    """
    HIVE_PATH.mkdir(parents=True, exist_ok=True)
    if not (HIVE_PATH / ".git").exists():
        _git(["init", "-b", HIVE_GIT_BRANCH])

    if _same_path(HIVE_PATH, Path(HIVE_REMOTE_DIR)):
        return

    remote = subprocess.run(
        ["git", "-C", str(HIVE_PATH), "remote", "get-url", "origin"],
        env=HIVE_GIT_ENV, capture_output=True, text=True,
    )
    if remote.returncode != 0:
        _git(["remote", "add", "origin", HIVE_GIT_REMOTE_URL])
    elif remote.stdout.strip() != HIVE_GIT_REMOTE_URL:
        _git(["remote", "set-url", "origin", HIVE_GIT_REMOTE_URL])


def sync_hive(direction: str) -> None:
    """Sync the local Hive with the remote Git repo over ssh — robustly.

    direction="pull": fetch + fast-forward the local Hive before running, if
    an `origin` remote is configured and reachable. Otherwise this is a
    no-op (e.g. on the server, which works directly in the worktree and has
    nothing to pull from).

    direction="push": always commits local changes (this must succeed), but
    only pushes them if `origin` is configured and reachable. HIVE_REMOTE_DIR
    is a non-bare checkout on the server with receive.denyCurrentBranch set
    to updateInstead, so `git push` alone already updates its worktree to
    match the new HEAD — no separate remote checkout step is needed. On the
    server itself there is no `origin` to push to, so the push is skipped
    and the commit stands as the only effect.
    """
    _ensure_hive_repo()
    t = time.monotonic()

    if direction == "pull":
        if not _origin_configured():
            print("No Hive `origin` remote configured — skipping pull (nothing to sync from).")
            return
        print(f"Syncing Hive (pull) via git: {HIVE_PATH} <- {HIVE_GIT_REMOTE_URL}")
        if not _git_soft(["pull", "--ff-only", "origin", HIVE_GIT_BRANCH]):
            print("WARNING: Hive pull failed/unavailable — continuing without it.")
    elif direction == "push":
        _git(["add", "-A"])
        status = subprocess.run(
            ["git", "-C", str(HIVE_PATH), "status", "--porcelain" ],
            env=HIVE_GIT_ENV, capture_output=True, text=True,
        )
        if status.stdout.strip():
            _git(["commit", "-c", "user.name=srv", "-c", "user.email=<>", "-m", f"pipeline sync {time.strftime('%Y-%m-%d %H:%M:%S')}"])
        else:
            print("No local Hive changes to commit.")

        if not _origin_configured():
            print("No Hive `origin` remote configured — skipping push (nothing to sync to).")
            return
        print(f"Syncing Hive (push) via git: {HIVE_PATH} -> {HIVE_GIT_REMOTE_URL}")
        if not _git_soft(["push", "origin", HIVE_GIT_BRANCH]):
            print("WARNING: Hive push failed/unavailable — commit was kept locally.")
    else:
        raise ValueError(f"invalid direction: {direction}")

    elapsed = time.monotonic() - t
    print(f"Runtime [git {direction}]: {elapsed:.1f}s")


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
    be_io.force_flush()

    run("hrv_aggregate.py",        passthrough_args)
    run("spectral_bands_aggregate.py", passthrough_args)


def main() -> None:
    global DB_PATH, DB_TMP_PATH, HIVE_REMOTE_DIR, HIVE_GIT_REMOTE_URL, HIVE_PATH

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
    parser.add_argument(
        "--db-path",
        type=Path,
        metavar="PATH",
        help=(
            "Download location for the Gadgetbridge DB (overrides "
            "HRV_DB_PATH / the default 'Gadgetbridge' next to this script)."
        ),
    )
    parser.add_argument(
        "--hive-remote-dir",
        metavar="DIR",
        help=(
            "Hive git repo directory on the server (overrides HIVE_REMOTE_DIR). "
            "Used both to build the ssh remote URL and, if it matches the "
            "local Hive working dir, to detect server-side operation."
        ),
    )
    parser.add_argument(
        "--hive-path",
        type=Path,
        metavar="PATH",
        help=(
            "Local Hive working directory (overrides HIVE_PATH / the default "
            "'hive' next to this script). Also exported as HIVE_PATH into the "
            "environment so every pipeline stage (gadgetbridge_migrate.py, "
            "hrv_aggregate.py, spectral_bands_aggregate.py), which import "
            "hive_io.py in their own subprocess, read the same Hive."
        ),
    )
    args, passthrough_args = parser.parse_known_args()

    if args.db_path:
        DB_PATH = args.db_path
        DB_TMP_PATH = DB_PATH.with_suffix(".tmp")
    if args.hive_remote_dir:
        HIVE_REMOTE_DIR = args.hive_remote_dir
        HIVE_GIT_REMOTE_URL = f"{HIVE_SSH_USER}@{HIVE_SSH_HOST}:{HIVE_REMOTE_DIR}"
    if args.hive_path:
        HIVE_PATH = args.hive_path
        os.environ["HIVE_PATH"] = str(HIVE_PATH)

    t_total = time.monotonic()

    sync_hive("pull")

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
