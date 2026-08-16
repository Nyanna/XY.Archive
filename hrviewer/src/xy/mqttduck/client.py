"""paho-mqtt client wiring for MQTT-Duck.

Thin adapter: subscribes to the configured topics, runs the transform on each
message and pushes the resulting samples into the shared buffer. The heavy
lifting (transformation, dedup, persistence) lives elsewhere -- this module
only bridges the network loop to the buffer.
"""
from __future__ import annotations

import paho.mqtt.client as mqtt

from .config import MqttConfig
from .transform import Transformer
from .writer import SampleBuffer


class MqttClient:
    def __init__(self, cfg: MqttConfig, buffer: SampleBuffer):
        self._cfg = cfg
        self._buf = buffer
        self._tf = Transformer(cfg.subscriptions, cfg.metrics)

        self._client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=cfg.mqtt_client_id,
            clean_session=True,
        )
        if cfg.mqtt_user:
            self._client.username_pw_set(cfg.mqtt_user, cfg.mqtt_password or None)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_disconnect = self._on_disconnect

    # -- callbacks -----------------------------------------------------
    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code != 0:
            print(f"[mqtt-duck] connect failed: {reason_code}", flush=True)
            return
        for sub in self._cfg.subscriptions:
            client.subscribe(sub.topic, qos=sub.qos)
            print(f"[mqtt-duck] subscribed: {sub.topic}", flush=True)

    def _on_disconnect(self, client, userdata, *args):
        print("[mqtt-duck] disconnected", flush=True)

    def _on_message(self, client, userdata, msg):
        try:
            samples = self._tf.transform(msg.topic, msg.payload)
        except Exception as exc:  # never let a bad payload kill the loop
            print(f"[mqtt-duck] transform error on {msg.topic}: {exc}", flush=True)
            return
        for s in samples:
            self._buf.put(s)

    # -- lifecycle -----------------------------------------------------
    def start(self) -> None:
        self._client.connect_async(
            self._cfg.mqtt_host, self._cfg.mqtt_port, self._cfg.mqtt_keepalive
        )
        self._client.loop_start()  # background network thread
        print(
            f"[mqtt-duck] connecting to mqtt://{self._cfg.mqtt_host}:"
            f"{self._cfg.mqtt_port}",
            flush=True,
        )

    def stop(self) -> None:
        try:
            self._client.loop_stop()
            self._client.disconnect()
        except Exception:
            pass
