"""HR Viewer -- DuckDB/Arrow backed dashboard server.

Public API::

    from xy.hrv.viewer import HrViewer, Config
    HrViewer(Config()).run()
"""
from __future__ import annotations

from .app import HrViewer
from .config import Config

__all__ = ["HrViewer", "Config"]
