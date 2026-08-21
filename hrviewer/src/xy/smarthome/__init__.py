"""SmartHome automation engine (runs inside MQTT-Duck, own MQTT client).

Reuses ``MqttConfig`` broker credentials and the HR-Viewer HTTP/statics
surface; keeps its own client, scheduler and restricted script runtime.
"""
from __future__ import annotations

from .config import SmartHomeConfig
from .engine import SmartHomeEngine

__all__ = ["SmartHomeConfig", "SmartHomeEngine"]
