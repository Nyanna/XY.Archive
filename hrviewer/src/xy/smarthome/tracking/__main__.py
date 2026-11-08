"""Standalone runner: ``python -m xy.smarthome.tracking [--config FILE]``."""
from __future__ import annotations
import argparse
import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from . import web
from .config import TrackingConfig
from .tracker import Tracker

class _Viewer:

    @staticmethod
    def _send_json(handler, payload) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.send_header('Content-Length', str(len(body)))
        handler.end_headers()
        handler.wfile.write(body)

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config', help='JSON config (default: $SMH_TRACK_CONFIG)')
    ap.add_argument('--http-bind', default='0.0.0.0')
    ap.add_argument('--http-port', type=int, default=8090)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    cfg = TrackingConfig.from_file(args.config) if args.config else TrackingConfig.from_env()
    tracker = Tracker(cfg)

    class Handler(BaseHTTPRequestHandler):

        def do_GET(self) -> None:
            if not web.handle_get(_Viewer, tracker, self):
                self.send_error(404)

        def log_message(self, *args) -> None:
            pass
    tracker.start()
    server = ThreadingHTTPServer((args.http_bind, args.http_port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        tracker.stop()
if __name__ == '__main__':
    main()