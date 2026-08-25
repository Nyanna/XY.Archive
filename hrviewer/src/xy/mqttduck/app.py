"""MQTT-Duck application: the HR-Viewer with MQTT ingestion bolted on.

``MqttDuck`` *inherits* from :class:`~xy.hrv.viewer.app.HrViewer`. It keeps the
entire inherited HTTP surface (statics + ``/api/query``) -- now reading the
sensor Hive -- and, via the base server's ``on_start`` / ``on_stop`` hooks,
supervises three cooperating pieces:

* :class:`~xy.mqttduck.client.MqttClient`  -- receives + transforms messages,
* :class:`~xy.mqttduck.writer.SampleBuffer` -- the inter-thread hand-off,
* :class:`~xy.mqttduck.writer.WriterThread` -- dedup + monthly merge-on-write.

The writer persists through the *same* DuckDB connection the read path uses.
"""
from __future__ import annotations

from xy.hrv.viewer.app import HrViewer
from xy.smarthome import SmartHomeConfig, SmartHomeEngine
from xy.smarthome import web as sh_web

from .client import MqttClient
from .config import MqttConfig
from .writer import SampleBuffer, WriterThread, create_sink


class MqttDuck(HrViewer):
    def __init__(self, config: MqttConfig | None = None):
        super().__init__(config or MqttConfig())
        cfg: MqttConfig = self.config  # type: ignore[assignment]

        # Read + write go through the same backend (duckdb | fastparquet); the
        # DuckDB sink shares the read store's connection + lock, the
        # fastparquet sink is self-contained.
        self.buffer = SampleBuffer(maxsize=cfg.queue_max)
        self.sink = create_sink(cfg, self.store)
        self.writer = WriterThread(cfg, self.buffer, self.sink)
        self.mqtt = MqttClient(cfg, self.buffer)

        # SmartHome automation: own MQTT client, same broker + credentials.
        self.smarthome = (
            SmartHomeEngine(SmartHomeConfig.from_mqtt(cfg))
            if cfg.smarthome_enabled
            else None
        )

    # -- routing: intercept SmartHome API, else inherited surface -------
    def handle_get(self, handler) -> None:
        if self.smarthome and sh_web.handle_get(self, self.smarthome, handler):
            return
        super().handle_get(handler)

    def handle_post(self, handler) -> None:
        if self.smarthome and sh_web.handle_post(self, self.smarthome, handler):
            return
        super().handle_post(handler)

    # -- ingestion lifecycle (bracketing the HTTP serve loop) ----------
    def on_start(self) -> None:
        cfg: MqttConfig = self.config  # type: ignore[assignment]
        print(
            f"[mqtt-duck] ingesting into hive={cfg.hive_path} "
            f"(sensor/metric/month), broker={cfg.mqtt_host}:{cfg.mqtt_port}",
            flush=True,
        )
        self.writer.start()
        self.mqtt.start()
        if self.smarthome:
            self.smarthome.start()

    def on_stop(self) -> None:
        print(
            f"[mqtt-duck] stopping (written={self.writer.written}, "
            f"deduped={self.writer.deduped}, dropped={self.buffer.dropped})",
            flush=True,
        )
        if self.smarthome:
            self.smarthome.stop()
        # Stop the source first so no new samples race the final flush.
        self.mqtt.stop()
        self.writer.stop()
        self.writer.join(timeout=30)
