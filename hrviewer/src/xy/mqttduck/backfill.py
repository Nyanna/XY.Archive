"""Backfill: fill the sensor Hive with historical data from VictoriaMetrics.

Before MQTT-Duck existed, samples were scraped (via ``mqtt2prometheus``) into
VictoriaMetrics. That instance is still reachable and still holds everything
older than the Hive. This module walks *backwards* one day at a time, per
series, and streams the missing days in from VM's CSV export endpoint
(``/api/v1/export/csv``). Which series exist is looked up per configured
metric via VM's ``/api/v1/series`` endpoint, so the walk needs no pre-existing
Hive content to start from.

Idempotent & efficient by construction:

* Per series, days are walked backwards starting the day before "today". As
  soon as a day already has at least one local sample it is considered
  complete -- everything older was necessarily backfilled (or live-ingested)
  in a previous run, so the walk stops there.
* A day with *no* VM data counts as an empty day; after
  ``backfill_empty_stop_days`` consecutive empty days the series is assumed
  exhausted (no older history in VM) and the walk stops. A hard
  ``backfill_max_days`` cap bounds worst-case runtime regardless.

Fetched rows are merged through the very same :class:`~xy.mqttduck.writer.HiveSink`
the live writer uses, so re-running the backfill (or racing the live writer)
is safe: identical ``(sensor, metric, month, ts)`` rows simply overwrite
themselves.
"""
from __future__ import annotations

import csv
import math
import threading
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import duckdb
import requests

from .config import MqttConfig
from .transform import Sample
from .writer import HiveSink

_DAY_MS = 24 * 3600 * 1000


def _day_start_ms(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp() * 1000)


class VmExportClient:
    """Streams one day of one series from VictoriaMetrics as CSV."""

    def __init__(self, cfg: MqttConfig, session: requests.Session | None = None):
        self._cfg = cfg
        self._session = session or requests.Session()
        if cfg.vm_user:
            self._session.auth = (cfg.vm_user, cfg.vm_password)

    def fetch_day(self, sensor: str, metric: str, day: date) -> list[Sample]:
        """Return the samples VM holds for ``(sensor, metric)`` on ``day``."""
        start_ms = _day_start_ms(day)
        end_ms = start_ms + _DAY_MS
        params = {
            "match[]": f'{{__name__="{metric}", sensor="{sensor}"}}',
            "format": "__timestamp__:unix_ms,__value__",
            "start": str(start_ms),
            "end": str(end_ms),
        }
        samples: list[Sample] = []
        with self._session.get(
            self._cfg.vm_export_url, params=params, stream=True, timeout=60
        ) as resp:
            resp.raise_for_status()
            lines = resp.iter_lines(decode_unicode=True)
            reader = csv.reader(line for line in lines if line is not None)
            next(reader, None)  # header: __timestamp__:unix_ms,__value__
            for row in reader:
                if len(row) < 2 or not row[0] or not row[1]:
                    continue
                try:
                    ts = int(row[0])
                    value = float(row[1])
                except ValueError:
                    continue
                # VM/Prometheus staleness markers are exported as the literal
                # string "NaN" (and, in principle, "Inf"/"-Inf" could show up
                # too). `float()` parses these without raising -- silently
                # turning "no fresh sample here" into a stored NaN value that
                # then renders as "NaN" in the UI. Treat non-finite values the
                # same as a missing/empty row: skip them.
                if not math.isfinite(value):
                    continue
                samples.append(Sample(sensor=sensor, metric=metric, ts_ms=ts, value=value))
        return samples

    def list_sensors(self, metric: str) -> list[str]:
        """Return every ``sensor`` label VM has recorded for ``metric``."""
        resp = self._session.get(
            self._cfg.vm_series_url,
            params={"match[]": f'{{__name__="{metric}"}}'},
            timeout=60,
        )
        resp.raise_for_status()
        sensors = {
            series["sensor"]
            for series in resp.json().get("data", [])
            if "sensor" in series
        }
        return sorted(sensors)


class Backfiller:
    """Walks every known series backwards, day by day, filling gaps from VM."""

    def __init__(self, cfg: MqttConfig, vm: VmExportClient | None = None):
        self._cfg = cfg
        self._hive = Path(cfg.hive_path)
        self._con = duckdb.connect(database=":memory:")
        self._con.execute("SET TimeZone='UTC'")
        self._lock = threading.Lock()
        self._sink = HiveSink(cfg, self._con, self._lock)
        self._vm = vm or VmExportClient(cfg)

    # -- discovery -------------------------------------------------------
    def discover_series(self) -> list[tuple[str, str]]:
        """Every ``(sensor, metric)`` pair, for the metrics in ``cfg.metrics``,
        that VM has recorded at least one sample for."""
        out: list[tuple[str, str]] = []
        for metric in self._cfg.metrics:
            for sensor in self._vm.list_sensors(metric.name):
                out.append((sensor, metric.name))
        return out

    # -- per-day completeness ---------------------------------------------
    def _day_has_data(self, sensor: str, metric: str, day: date) -> bool:
        month = self._cfg.part_value(_day_start_ms(day))
        part = (
            self._hive
            / f"sensor={sensor}"
            / f"metric={metric}"
            / f"month={month}"
            / "data.parquet"
        )
        if not part.exists():
            return False
        start_ms = _day_start_ms(day)
        end_ms = start_ms + _DAY_MS
        with self._lock:
            row = self._con.execute(
                "SELECT 1 FROM read_parquet(?) WHERE ts >= ? AND ts < ? LIMIT 1",
                [str(part), start_ms, end_ms],
            ).fetchone()
        return row is not None

    # -- one series -----------------------------------------------------
    def backfill_series(self, sensor: str, metric: str, log=print) -> tuple[int, int]:
        """Backfill one series; returns (days_written, samples_written)."""
        today = datetime.now(tz=timezone.utc).date()
        day = today - timedelta(days=1)
        empty_streak = 0
        days_written = 0
        samples_written = 0
        steps = 0

        while steps < self._cfg.backfill_max_days:
            steps += 1
            if self._day_has_data(sensor, metric, day):
                break  # everything older was already backfilled/live-ingested

            samples = self._vm.fetch_day(sensor, metric, day)
            if samples:
                n = self._sink.write(samples)
                samples_written += n
                days_written += 1
                empty_streak = 0
                log(
                    f"[backfill] {sensor}/{metric} {day.isoformat()}: "
                    f"+{n} samples",
                    flush=True,
                )
            else:
                empty_streak += 1
                if empty_streak >= self._cfg.backfill_empty_stop_days:
                    log(
                        f"[backfill] {sensor}/{metric}: "
                        f"{empty_streak} empty days, stopping at "
                        f"{day.isoformat()}",
                        flush=True,
                    )
                    break

            day -= timedelta(days=1)

        return days_written, samples_written

    # -- everything -------------------------------------------------------
    def run(self, log=print) -> None:
        series = self.discover_series()
        log(f"[backfill] {len(series)} series found in VM", flush=True)
        total_days = 0
        total_samples = 0
        for sensor, metric in series:
            d, s = self.backfill_series(sensor, metric, log=log)
            total_days += d
            total_samples += s
        log(
            f"[backfill] done: {len(series)} series, "
            f"{total_days} days, {total_samples} samples written",
            flush=True,
        )

    def close(self) -> None:
        with self._lock:
            self._con.close()


def run_backfill(cfg: MqttConfig) -> None:
    b = Backfiller(cfg)
    try:
        b.run()
    finally:
        b.close()
