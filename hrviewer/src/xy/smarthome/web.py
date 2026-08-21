"""HTTP glue for the SmartHome script + status.

* ``GET``/``POST`` ``/api/smarthome/script`` -> Blockly XML load/save.
* ``GET`` ``/api/smarthome/status`` -> :meth:`SmartHomeEngine.metrics`.

The functions return ``True`` when they handled the request, so the host app
can fall through to its inherited routes otherwise.
"""
from __future__ import annotations

import json
import os
from http import HTTPStatus
from urllib.parse import urlparse

from .engine import SmartHomeEngine

_ROUTE = "/api/smarthome/script"
_STATUS_ROUTE = "/api/smarthome/status"


def handle_get(viewer, engine: SmartHomeEngine, handler) -> bool:
    path = urlparse(handler.path).path
    if path == _STATUS_ROUTE:
        viewer._send_json(handler, engine.metrics())  # noqa: SLF001
        return True
    if path != _ROUTE:
        return False
    xml = _read(engine.cfg.native_path)
    viewer._send_json(  # noqa: SLF001 - intentional reuse of base helpers
        handler,
        {"xml": xml, "error": engine.script_error},
    )
    return True


def handle_post(viewer, engine: SmartHomeEngine, handler) -> bool:
    if urlparse(handler.path).path != _ROUTE:
        return False
    length = int(handler.headers.get("Content-Length", 0) or 0)
    body = handler.rfile.read(length) if length else b"{}"
    try:
        req = json.loads(body or b"{}")
        xml = req.get("xml", "")
        python = req.get("python", "")
        if not isinstance(xml, str) or not isinstance(python, str):
            raise ValueError("xml and python must be strings")
    except Exception as exc:
        viewer._send_json(handler, {"ok": False, "error": f"bad request: {exc}"})
        return True

    _write(engine.cfg.native_path, xml)
    _write(engine.cfg.python_path, python)

    # Reload from the freshly written Python and report any script error.
    engine._exec_source(python)  # noqa: SLF001 - engine-internal reload
    err = engine.script_error
    viewer._send_json(handler, {"ok": err is None, "error": err})
    return True


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)  # atomic
