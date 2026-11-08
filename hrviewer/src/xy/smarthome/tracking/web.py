"""HTTP glue: ``GET /api/smarthome/devices`` lists all tracked devices."""
from __future__ import annotations
from urllib.parse import urlparse
from .tracker import Tracker
ROUTE = '/api/smarthome/devices'

def handle_get(viewer, tracker: Tracker, handler) -> bool:
    if urlparse(handler.path).path != ROUTE:
        return False
    '# noqa: SLF001'
    viewer._send_json(handler, tracker.snapshot())
    return True