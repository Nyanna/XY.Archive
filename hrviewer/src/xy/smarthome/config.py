"""Paths of the single script (native XML + exported Python) and broker
coordinates. Use :meth:`SmartHomeConfig.from_mqtt` to inherit the broker
host/credentials from an existing ``MqttConfig`` (only the client-id differs).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from xy.hrv.viewer.config import _env

DEFAULT_NATIVE_PATH = "smarthome/smarthome.xml"
DEFAULT_PY_PATH = "smarthome/smarthome_generated.py"


@dataclass
class SmartHomeConfig:
    """Runtime configuration for the SmartHome engine."""

    native_path: str = field(
        default_factory=lambda: _env("SMH_NATIVE_PATH", DEFAULT_NATIVE_PATH)
    )
    python_path: str = field(
        default_factory=lambda: _env("SMH_PY_PATH", DEFAULT_PY_PATH)
    )

    mqtt_host: str = field(default_factory=lambda: _env("SMD_MQTT_HOST", "127.0.0.1"))
    mqtt_port: int = field(default_factory=lambda: int(_env("SMD_MQTT_PORT", "1883")))
    mqtt_user: str = field(default_factory=lambda: _env("SMD_MQTT_USER", ""))
    mqtt_password: str = field(default_factory=lambda: _env("SMD_MQTT_PASSWORD", ""))
    mqtt_keepalive: int = field(
        default_factory=lambda: int(_env("SMD_MQTT_KEEPALIVE", "60"))
    )
    mqtt_client_id: str = field(
        default_factory=lambda: _env(
            "SMH_MQTT_CLIENT_ID", f"smarthome-{os.urandom(4).hex()}"
        )
    )

    # State topic ``<base>/<device>``, command topic ``<base>/<device>/set``.
    base_topic: str = field(default_factory=lambda: _env("SMH_BASE_TOPIC", "zigbee2mqtt"))

    @classmethod
    def from_mqtt(cls, mqtt_cfg) -> "SmartHomeConfig":
        cfg = cls()
        cfg.mqtt_host = mqtt_cfg.mqtt_host
        cfg.mqtt_port = mqtt_cfg.mqtt_port
        cfg.mqtt_user = mqtt_cfg.mqtt_user
        cfg.mqtt_password = mqtt_cfg.mqtt_password
        cfg.mqtt_keepalive = mqtt_cfg.mqtt_keepalive
        return cfg
