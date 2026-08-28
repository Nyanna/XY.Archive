#!/usr/bin/env bash
# Start the HR Viewer. Run from the project root. Args (e.g. --port 9000) pass through.
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
# PyArrow sizes its internal CPU thread pool
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
PYTHONPATH=src python3 -m xy.hrv.viewer "$@"
