#!/usr/bin/env bash
# Start MQTT-Duck (MQTT -> Hive bridge + HR-Viewer read server).
# Run from the project root. Args (e.g. --mqtt-host 10.0.0.5) pass through.
cd "$(dirname "$0")"
# nanoarrow / DuckDB internal CPU thread pools kept small (footprint was the
# whole reason we left VictoriaMetrics).
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
# Mirror node has no DuckDB -> default to the fastparquet backend. Override
# with SMD_BACKEND=duckdb or a trailing --backend argument.
export SMD_BACKEND="${SMD_BACKEND:-fastparquet}"
PYTHONPATH=src python3 -m xy.mqttduck "$@"
