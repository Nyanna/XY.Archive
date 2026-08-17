"""Metric transformation: MQTT (topic, payload) -> (sensor, metric, ts, value).

This is the architecturally separated "what does an MQTT message mean" stage.
It is deliberately free of any MQTT or Hive dependency so it can be unit-tested
in isolation and reused.

Payloads are expected to be JSON objects (the smarthome devices -- zigbee2mqtt,
Tasmota SENSOR, the Viessmann bridge -- all publish JSON). The object is
flattened; each configured :class:`~xy.mqttduck.config.Metric` then pulls its
value out either by top-level key or, for ``.``-prefixed names, by leaf key
anywhere in the (possibly nested) structure.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone

from .config import Metric, Subscription


@dataclass(frozen=True)
class Sample:
    sensor: str
    metric: str
    ts_ms: int
    value: float


def _now_ms() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)


def _coerce(value) -> float | None:
    """Best-effort numeric coercion; returns None for non-numeric values."""
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return None
        try:
            return float(s)
        except ValueError:
            # tolerate simple on/off style states
            low = s.lower()
            if low in ("on", "true", "yes"):
                return 1.0
            if low in ("off", "false", "no"):
                return 0.0
            return None
    return None


def _flatten(obj, out_top: dict, out_leaf: dict) -> None:
    """Collect top-level keys and leaf-key (last path component) values.

    ``out_top`` maps only the top-level object keys; ``out_leaf`` maps every
    leaf key found at any depth (last one wins on collision).
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                _flatten(v, {}, out_leaf)
            else:
                out_leaf[k] = v


class Transformer:
    """Turns raw MQTT messages into :class:`Sample` objects per the config."""

    def __init__(self, subscriptions, metrics, now_fn=_now_ms):
        self._subs: list[Subscription] = list(subscriptions)
        self._metrics: list[Metric] = list(metrics)
        self._now = now_fn

    def _sensor_for(self, topic: str) -> str | None:
        for sub in self._subs:
            dev = sub.device_id(topic)
            if dev is not None:
                return dev
        return None

    def transform(self, topic: str, payload: bytes | str) -> list[Sample]:
        """Return the samples carried by one MQTT message (possibly empty)."""
        sensor = self._sensor_for(topic)
        if sensor is None:
            return []

        if isinstance(payload, (bytes, bytearray)):
            payload = payload.decode("utf-8", errors="replace")
        try:
            doc = json.loads(payload)
        except (json.JSONDecodeError, ValueError):
            return []
        if not isinstance(doc, dict):
            return []

        top: dict = {k: v for k, v in doc.items() if not isinstance(v, dict)}
        leaf: dict = {}
        _flatten(doc, top, leaf)

        ts = self._now()
        out: list[Sample] = []
        for m in self._metrics:
            if m.leaf_only:
                raw = leaf.get(m.key)
            else:
                raw = top.get(m.key)
                if raw is None:
                    raw = leaf.get(m.key)
            if raw is None:
                continue
            val = _coerce(raw)
            if val is None:
                continue
            out.append(Sample(sensor=sensor, metric=m.name, ts_ms=ts, value=val))
        return out
