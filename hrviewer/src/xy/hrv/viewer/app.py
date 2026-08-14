"""HR Viewer application -- entry class on top of the stdlib HTTP server.

Two endpoints:

* **Statics**  -- ``GET /<file>`` serves the file of that name from the
  statics directory.
* **DB query** -- ``POST /api/query`` runs a single read-only DuckDB request
  and returns the result as an Apache Arrow IPC stream.
"""
from __future__ import annotations

import json
import mimetypes
import shutil
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .config import Config
from .db import HiveStore, table_to_ipc

DEFAULT_SEGMENT = "raw"
DEFAULT_METRIC = "heart_rate_generic"

ARROW_MIME = "application/vnd.apache.arrow.stream"


class HrViewer:
    """The HR Viewer server: DuckDB-backed, statics-serving HTTP server."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.store = HiveStore(self.config)
        self.statics_dir = Path(self.config.statics_dir)

    def handle_get(self, handler: "_Handler") -> None:
        rel = urlparse(handler.path).path.lstrip("/")
        self._serve_static(handler, rel)

    def handle_post(self, handler: "_Handler") -> None:
        if urlparse(handler.path).path == "/api/query":
            self._api_query(handler)
        else:
            handler.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def _api_query(self, handler: "_Handler") -> None:
        length = int(handler.headers.get("Content-Length", 0) or 0)
        body = handler.rfile.read(length) if length else b""
        req = json.loads(body or b"{}")

        now_ms = _now_ms()
        kind = str(req.get("kind", "series")).lower()
        start_ms = int(req.get("start", now_ms - 24 * 3600 * 1000))  # default: 24h
        end_ms = int(req.get("end", now_ms))
        max_points = req.get("max_points")
        max_points = int(max_points) if max_points is not None else None
        fmt = str(req.get("format", "arrow")).lower()

        if kind == "dominance_daily":
            table = self.store.dominance_daily(start_ms, end_ms)
        elif kind == "sleep_daily":
            table = self.store.sleep_daily(
                start_ms, end_ms, session=str(req.get("session", "after"))
            )
        else:  # "series"
            table = self.store.series(
                segment=req.get("segment", DEFAULT_SEGMENT),
                metric=req.get("metric", DEFAULT_METRIC),
                start_ms=start_ms,
                end_ms=end_ms,
                max_points=max_points,
                agg=str(req.get("agg", "avg")),
            )

        if fmt == "json":
            cols = table.to_pydict()
            self._send_json(
                handler,
                {
                    "start": start_ms,
                    "end": end_ms,
                    "rows": table.num_rows,
                    "columns": table.column_names,
                    "data": cols,
                },
            )
        else:
            self._send_bytes(handler, table_to_ipc(table), ARROW_MIME, cache="no-store")

    def _serve_static(self, handler: "_Handler", rel: str) -> None:
        base = self.statics_dir.resolve()
        target = (base / rel).resolve()
        # Prevent path traversal outside the statics directory.
        if base != target and base not in target.parents:
            handler.send_error(HTTPStatus.FORBIDDEN, "Forbidden")
            return
        self._send_file(handler, target)

    def _send_file(self, handler: "_Handler", path: Path) -> None:
        if not path.is_file():
            handler.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        handler.send_response(HTTPStatus.OK)
        handler.send_header("Content-Type", ctype)
        handler.send_header("Content-Length", str(path.stat().st_size))
        handler.end_headers()
        with path.open("rb") as f:
            shutil.copyfileobj(f, handler.wfile)  # streamed, low RAM

    def _send_bytes(
        self, handler: "_Handler", payload: bytes, ctype: str, cache: str | None = None
    ) -> None:
        handler.send_response(HTTPStatus.OK)
        handler.send_header("Content-Type", ctype)
        handler.send_header("Content-Length", str(len(payload)))
        if cache:
            handler.send_header("Cache-Control", cache)
        handler.end_headers()
        handler.wfile.write(payload)

    def _send_json(self, handler: "_Handler", obj) -> None:
        self._send_bytes(handler, json.dumps(obj).encode("utf-8"), "application/json")

    def run(self) -> None:
        cfg = self.config
        httpd = _Server((cfg.host, cfg.port), _Handler)
        httpd.viewer = self
        print(
            f"[hrviewer] serving on http://{cfg.host}:{cfg.port}  "
            f"(hive={cfg.hive_path})",
            flush=True,
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.shutdown()
            httpd.server_close()
            self.store.close()


class _Server(ThreadingHTTPServer):
    """Threaded HTTP server holding a reference to the owning HrViewer."""

    daemon_threads = True
    allow_reuse_address = True
    viewer: HrViewer


class _Handler(BaseHTTPRequestHandler):
    server_version = "HrViewer/0.1"

    def do_GET(self) -> None:  # noqa: N802 (stdlib naming)
        self._guard(self.server.viewer.handle_get)

    def do_POST(self) -> None:  # noqa: N802 (stdlib naming)
        self._guard(self.server.viewer.handle_post)

    def _guard(self, fn) -> None:
        try:
            fn(self)
        except BrokenPipeError:
            pass
        except Exception as exc:  # keep the server alive on request errors
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def log_message(self, fmt: str, *args) -> None:
        print(f"[hrviewer] {self.address_string()} {fmt % args}", flush=True)


def _now_ms() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)
