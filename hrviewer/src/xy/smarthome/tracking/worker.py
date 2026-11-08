"""Background thread base class."""
from __future__ import annotations
import logging
import threading
log = logging.getLogger(__name__)

class Worker:
    name = 'worker'

    def __init__(self) -> None:
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self._thread = threading.Thread(target=self._guard, name=self.name, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5)

    def run(self) -> None:
        raise NotImplementedError

    def _guard(self) -> None:
        try:
            self.run()
        except Exception:
            log.exception('%s crashed', self.name)