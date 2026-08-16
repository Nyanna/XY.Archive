#!/usr/bin/env bash
# Start MQTT-Duck (MQTT -> Hive bridge + HR-Viewer read server).
# Run from the project root. Args (e.g. --mqtt-host 10.0.0.5) pass through.
cd "$(dirname "$0")"
# PyArrow / DuckDB internal CPU thread pools kept small (footprint was the
# whole reason we left VictoriaMetrics).
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
PYTHONPATH=src python3 -m xy.mqttduck "$@"
