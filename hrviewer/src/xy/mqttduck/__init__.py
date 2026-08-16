"""MQTT-Duck -- an MQTT -> Parquet/Hive bridge built on top of the HR-Viewer.

MQTT-Duck *inherits* from the HR-Viewer: it reuses the very same DuckDB /
Parquet Hive machinery (statics server + ``/api/query`` read path) and adds,
architecturally separated, an MQTT client, a metric transformation stage and a
buffered writer thread that persists the incoming samples into a sensor Hive.

Package layout::

    config.py     -- Python configuration (mirrors the old smarthome.yaml)
    transform.py  -- MQTT topic/payload -> (sensor, metric, ts, value) samples
    writer.py     -- buffer + writer thread + monthly merge-on-write Hive sink
    client.py     -- paho-mqtt client wiring
    backfill.py   -- ``--backfill``: fill Hive gaps from VictoriaMetrics export
    app.py        -- MqttDuck(HrViewer): server + ingestion supervisor
    __main__.py   -- CLI entry point
"""
from __future__ import annotations

from .app import MqttDuck
from .config import MqttConfig

__all__ = ["MqttDuck", "MqttConfig"]
