"""CLI entry point: ``python -m xy.mqttduck`` / console script ``mqtt-duck``."""
from __future__ import annotations

import argparse

from .app import MqttDuck
from .config import MqttConfig


def build_config(argv: list[str] | None = None) -> tuple[MqttConfig, argparse.Namespace]:
    cfg = MqttConfig()  # env-based defaults + smarthome mapping
    p = argparse.ArgumentParser(
        prog="mqtt-duck",
        description="MQTT -> Parquet/Hive bridge on top of the HR-Viewer.",
    )
    # HTTP / Hive (inherited surface)
    p.add_argument("--host", default=cfg.host)
    p.add_argument("--port", type=int, default=cfg.port)
    p.add_argument("--hive", default=cfg.hive_path, help="Sensor Hive path")
    p.add_argument("--memory-limit", default=cfg.memory_limit)
    p.add_argument("--threads", type=int, default=cfg.threads)
    p.add_argument("--max-points", type=int, default=cfg.max_points)
    # MQTT broker
    p.add_argument("--mqtt-host", default=cfg.mqtt_host)
    p.add_argument("--mqtt-port", type=int, default=cfg.mqtt_port)
    p.add_argument("--mqtt-user", default=cfg.mqtt_user)
    p.add_argument("--mqtt-password", default=cfg.mqtt_password)
    p.add_argument("--mqtt-client-id", default=cfg.mqtt_client_id)
    # Writer
    p.add_argument("--flush-interval", type=float, default=cfg.flush_interval_s)
    p.add_argument("--flush-max", type=int, default=cfg.flush_max_samples)
    # Backfill (one-shot: fetch missing history from VictoriaMetrics, then
    # exit -- does not start the MQTT client or the HTTP server).
    p.add_argument(
        "--backfill",
        action="store_true",
        help="Backfill missing days from VictoriaMetrics export and exit.",
    )
    p.add_argument("--vm-host", default=cfg.vm_host)
    p.add_argument("--vm-port", type=int, default=cfg.vm_port)
    p.add_argument(
        "--backfill-empty-stop-days",
        type=int,
        default=cfg.backfill_empty_stop_days,
        help="Consecutive empty VM days before a series is considered exhausted.",
    )
    p.add_argument(
        "--backfill-max-days",
        type=int,
        default=cfg.backfill_max_days,
        help="Hard cap on days walked back per series.",
    )
    args = p.parse_args(argv)

    cfg.host = args.host
    cfg.port = args.port
    cfg.hive_path = args.hive
    cfg.memory_limit = args.memory_limit
    cfg.threads = args.threads
    cfg.max_points = args.max_points
    cfg.mqtt_host = args.mqtt_host
    cfg.mqtt_port = args.mqtt_port
    cfg.mqtt_user = args.mqtt_user
    cfg.mqtt_password = args.mqtt_password
    cfg.mqtt_client_id = args.mqtt_client_id
    cfg.flush_interval_s = args.flush_interval
    cfg.flush_max_samples = args.flush_max
    cfg.vm_host = args.vm_host
    cfg.vm_port = args.vm_port
    cfg.backfill_empty_stop_days = args.backfill_empty_stop_days
    cfg.backfill_max_days = args.backfill_max_days
    return cfg, args


def main(argv: list[str] | None = None) -> None:
    cfg, args = build_config(argv)
    if args.backfill:
        from .backfill import run_backfill

        run_backfill(cfg)
        return
    MqttDuck(cfg).run()


if __name__ == "__main__":
    main()
