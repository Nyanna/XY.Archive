"""Configuration for MQTT-Duck.

This is the single source of truth (a *Python* config, as required).

``MqttConfig`` extends the HR-Viewer :class:`~xy.hrv.viewer.config.Config` so
the inherited read path (statics + ``/api/query``) transparently serves the
sensor Hive. It only re-points the Hive location and re-declares the partition
scheme::

    hive.sm/ sensor=<deviceid> / metric=<prom_name> / month=<YYYY-MM> / data.parquet
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import ClassVar

from xy.hrv.viewer.config import Config, _env

# Default location of the MQTT sensor Hive (sibling of the HR-Viewer Hive).
DEFAULT_SM_HIVE_PATH = "/home/user/xyan/XY.Archiv/hrviewer/hive.sm"


@dataclass(slots=True, frozen=True)
class Subscription:
    """One MQTT topic to subscribe to plus how to derive the sensor label.

    ``device_id_regex`` must contain a named group ``deviceid`` that is matched
    against the *received* topic; its capture becomes the ``sensor`` partition.
    """

    topic: str
    device_id_regex: str
    qos: int = 0

    @property
    def pattern(self) -> "re.Pattern[str]":
        return re.compile(self.device_id_regex)

    def device_id(self, topic: str) -> str | None:
        m = self.pattern.search(topic)
        if not m:
            return None
        try:
            return m.group("deviceid")
        except IndexError:
            return None


@dataclass(slots=True, frozen=True)
class Metric:
    """A value to extract from a payload and the metric name to store it under.

    * ``mqtt_name`` -- key to look up in the (flattened) JSON payload. A
      leading ``.`` means "match this leaf key anywhere in a nested object"
      (mqtt2prometheus gjson-style), otherwise a top-level key is preferred
      with a leaf-name fallback.
    * ``name``      -- the ``metric`` partition the sample is stored under.
    """

    name: str
    mqtt_name: str

    @property
    def key(self) -> str:
        """The payload leaf key (mqtt_name without a leading dot)."""
        return self.mqtt_name[1:] if self.mqtt_name.startswith(".") else self.mqtt_name

    @property
    def leaf_only(self) -> bool:
        return self.mqtt_name.startswith(".")


@dataclass(slots=True)
class MqttConfig(Config):
    """MQTT-Duck runtime configuration (extends the HR-Viewer Config)."""

    # ---- Hive location & partition scheme (overrides the base defaults) ----
    hive_path: str = field(
        default_factory=lambda: _env("SMD_HIVE_PATH", DEFAULT_SM_HIVE_PATH)
    )
    part_names: ClassVar[tuple[str, str]] = ("sensor", "metric")
    time_part: ClassVar[str] = "month"

    # ---- HTTP server (distinct default port so it can run beside hrv) ----
    port: int = field(default_factory=lambda: int(_env("SMD_PORT", "8081")))

    # ---- MQTT broker (Mosquitto) ----
    mqtt_host: str = field(default_factory=lambda: _env("SMD_MQTT_HOST", "127.0.0.1"))
    mqtt_port: int = field(default_factory=lambda: int(_env("SMD_MQTT_PORT", "1883")))
    mqtt_user: str = field(default_factory=lambda: _env("SMD_MQTT_USER", ""))
    mqtt_password: str = field(default_factory=lambda: _env("SMD_MQTT_PASSWORD", ""))
    mqtt_keepalive: int = field(
        default_factory=lambda: int(_env("SMD_MQTT_KEEPALIVE", "60"))
    )
    mqtt_client_id: str = field(
        default_factory=lambda: _env("SMD_MQTT_CLIENT_ID", "mqtt-duck")
    )

    # ---- Writer thread tuning ----
    # Low expected throughput -> monthly Parquet files, relaxed flush cadence.
    # The interval is the *normal* case: batch a few minutes of samples into
    # one merge. ``flush_max_samples`` is only a safety cap that forces an
    # earlier flush should throughput ever spike, bounding the writer's RAM.
    flush_interval_s: float = field(
        default_factory=lambda: float(_env("SMD_FLUSH_INTERVAL_S", "300"))
    )
    flush_max_samples: int = field(
        default_factory=lambda: int(_env("SMD_FLUSH_MAX_SAMPLES", "500"))
    )
    queue_max: int = field(default_factory=lambda: int(_env("SMD_QUEUE_MAX", "100000")))

    # ---- Subscriptions & metrics (mirrors smarthome.yaml) ----
    subscriptions: list[Subscription] = field(default_factory=list)
    metrics: list[Metric] = field(default_factory=list)

    # ---- VictoriaMetrics backfill source (historical data pre-dating the
    # Hive; the whole reason MQTT-Duck exists is that we *left* VM for the
    # live path, but its export endpoint is still the source of truth for
    # everything older than the Hive) ----
    vm_scheme: str = field(default_factory=lambda: _env("SMD_VM_SCHEME", "http"))
    vm_host: str = field(default_factory=lambda: _env("SMD_VM_HOST", "proxy.xyan.icu"))
    vm_port: int = field(default_factory=lambda: int(_env("SMD_VM_PORT", "9090")))
    vm_export_path: str = field(
        default_factory=lambda: _env("SMD_VM_EXPORT_PATH", "/api/v1/export/csv")
    )
    vm_user: str = field(default_factory=lambda: _env("SMD_VM_USER", "vm_writer"))
    vm_password: str = field(
        default_factory=lambda: _env(
            "SMD_VM_PASSWORD", "tkQa6XahTPi2S7IIpRrDlkYyYY/Vwv5Y7FRnW8cMzcM="
        )
    )

    # ---- Backfill walk tuning ----
    # How many consecutive *empty* days (VM returned nothing) are tolerated
    # before a series is considered exhausted (no older history exists).
    backfill_empty_stop_days: int = field(
        default_factory=lambda: int(_env("SMD_BACKFILL_EMPTY_STOP_DAYS", "14"))
    )
    # Hard safety cap on how many days a single series walks back, regardless
    # of the empty-day streak (bounds worst-case runtime).
    backfill_max_days: int = field(
        default_factory=lambda: int(_env("SMD_BACKFILL_MAX_DAYS", "7"))
    )

    @property
    def vm_export_url(self) -> str:
        return f"{self.vm_scheme}://{self.vm_host}:{self.vm_port}{self.vm_export_path}"

    def __post_init__(self) -> None:
        if not self.subscriptions:
            self.subscriptions = list(DEFAULT_SUBSCRIPTIONS)
        if not self.metrics:
            self.metrics = list(DEFAULT_METRICS)

    # -- monthly time partition: YYYY-MM, compares correctly as a string --
    def part_value(self, ms: int) -> str:  # type: ignore[override]
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m")

    @staticmethod
    def month_of(ms: int) -> str:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m")


DEFAULT_SUBSCRIPTIONS: tuple[Subscription, ...] = (
    # All zigbee2mqtt devices. The single-level '+' wildcard matches the
    # per-device state topic (zigbee2mqtt/<id>) while leaving multi-level
    # side topics (zigbee2mqtt/<id>/availability, zigbee2mqtt/bridge/...)
    # untouched. The device id is extracted from the received topic.
    Subscription(
        topic="zigbee2mqtt/+",
        device_id_regex=r"zigbee2mqtt/(?P<deviceid>(.+))",
    ),
    # All Tasmota SENSOR topics; the regex keeps only tasmota_* devices.
    Subscription(
        topic="tele/+/SENSOR",
        device_id_regex=r"tele/(?P<deviceid>(tasmota_.+))/SENSOR",
    ),
)

DEFAULT_METRICS: tuple[Metric, ...] = (
    # zigbee sonoff temperature sensor
    Metric("Temperature", "temperature"),
    Metric("Humidity", "humidity"),
    Metric("Battery", "battery"),
    Metric("Linkquality", "linkquality"),
    # tasmota esp main power meter
    Metric("Power_curr", ".Power_curr"),
    Metric("Total_in", ".Total_in"),
)
