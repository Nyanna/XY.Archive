#!/usr/bin/env bash
# Grants the Python interpreter the capabilities needed for ports < 1024 and raw capture, then starts ap_monitor.py.
# Usage: run_ap_monitor.sh [grant|revoke|run] [-- script args]   (default: run)
# Interpreter: $PYTHON (default python3, e.g. a venv with scrapy installed)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACTION="${1:-run}"
[[ $# -gt 0 ]] && shift
[[ "${1:-}" == "--" ]] && shift

PY_PATH="$(command -v "${PYTHON:-python3}")" || { echo "python interpreter not found" >&2; exit 1; }
PY_REAL="$(readlink -f "$PY_PATH")"
CAPS="cap_net_bind_service,cap_net_raw=+ep"

case "$ACTION" in
  grant)  sudo setcap "$CAPS" "$PY_REAL"; getcap "$PY_REAL" ;;
  revoke) sudo setcap -r "$PY_REAL"; echo "capabilities removed from $PY_REAL" ;;
  run)
    sudo setcap "$CAPS" "$PY_REAL"
    trap 'sudo setcap -r "$PY_REAL"' EXIT
    "$PY_PATH" "$SCRIPT_DIR/ap_monitor.py" "$@"
    ;;
  *) echo "usage: $0 [grant|revoke|run] [-- ap_monitor.py args]" >&2; exit 2 ;;
esac
