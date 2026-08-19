Implementiere eine Änderung des Backfills in `/home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py`. Der Backfill soll auf der Configuration basierend laufen nicht mehr auf Basis der bestehenden Metriken im Hive. Hintergrund: die finale Datenübernahme ist nur relevant, daher muss der Backfill auf Basis eines leeren Hive laufen können.
SystemInit:  id=b917dfb7-c117-4c35-bd32-4a4554ba220a, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: 6981771d-7994-4a42-9177-5f7476e4acb4
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  reason: "Aktuellen Backfill-Code verstehen, um Umstellung auf Configuration-Basis zu planen"
```
/answer 6981771d-7994-4a42-9177-5f7476e4acb4 allow
ReasoningToken: 18
Control Request:
```yaml
id: 6766f526-68ba-4270-af1a-74af2af18749
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  reason: "Konfigurationsstruktur verstehen, um Sensor/Metric-Paare aus der Config statt aus dem Hive zu ermitteln"
```
/answer 6766f526-68ba-4270-af1a-74af2af18749 allow
ReasoningToken: 39
Control Request:
```yaml
id: 15359127-51d0-42bf-8173-703d83e45bbf
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck
  reason: "Alle Dateien im mqttduck-Modul auflisten, um verwandte Konfigurationsteile zu finden"
```
/answer 15359127-51d0-42bf-8173-703d83e45bbf allow
Control Request:
```yaml
id: 225f802d-dbf4-46a0-8271-f97f49be7394
result:
  structuredContent:
    entries:
    - __init__.py
    - __main__.py
    - app.py
    - backfill.py
    - client.py
    - config.py
    - transform.py
    - writer.py
```
/answer 225f802d-dbf4-46a0-8271-f97f49be7394 allow
Control Request:
```yaml
id: 5c23ba7f-dae0-42ad-a479-856edb95e714
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer
  pattern: backfill|test_backfill|smarthome
  reason: "Tests und Konfigurationsdateien zum Backfill finden, um Erwartungen an die Änderung zu verstehen"
```
/answer 5c23ba7f-dae0-42ad-a479-856edb95e714 deny es gibt keine Tests, mit Konfiguration sind die Akzeptierten Metriken der MQTT Subrscriptions gemeint.
ReasoningToken: 367
ReasoningToken: 2659
Control Request:
```yaml
id: f94414fb-653e-474e-95d5-f13beed236a0
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  old_text: |2-
        vm_export_path: str = field(
            default_factory=lambda: _env("SMD_VM_EXPORT_PATH", "/api/v1/export/csv")
        )
  new_text: |2-
        vm_export_path: str = field(
            default_factory=lambda: _env("SMD_VM_EXPORT_PATH", "/api/v1/export/csv")
        )
        # Series-discovery endpoint: used by the backfill to find out which
        # sensors VM actually holds data for, per configured metric -- this is
        # what lets the backfill run against a completely empty Hive.
        vm_series_path: str = field(
            default_factory=lambda: _env("SMD_VM_SERIES_PATH", "/api/v1/series")
        )
  reason: "vm_series_path Feld ergänzen, damit der Backfill Serien direkt bei VM anhand des konfigurierten Metriknamens ermitteln kann statt aus dem Hive"
```
/answer f94414fb-653e-474e-95d5-f13beed236a0 allow
Control Request:
```yaml
id: 6b6828c2-0471-4299-b7cd-12984b979daa
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  old_text: |2-
        @property
        def vm_export_url(self) -> str:
            return f"{self.vm_scheme}://{self.vm_host}:{self.vm_port}{self.vm_export_path}"
  new_text: |2-
        @property
        def vm_export_url(self) -> str:
            return f"{self.vm_scheme}://{self.vm_host}:{self.vm_port}{self.vm_export_path}"

        @property
        def vm_series_url(self) -> str:
            return f"{self.vm_scheme}://{self.vm_host}:{self.vm_port}{self.vm_series_path}"
  reason: vm_series_url Property analog zu vm_export_url ergänzen
```
/answer 6b6828c2-0471-4299-b7cd-12984b979daa allow
Text:
 Nun `backfill.py` anpassen: Docstring, `VmExportClient.list_sensors`, und `Backfiller.discover_series` auf Konfigurationsbasis umstellen.
Control Request:
```yaml
id: 5920ebaf-ebd0-4763-86d8-925abbe49336
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  old_text: |-
    """Backfill: fill the sensor Hive with historical data from VictoriaMetrics.

    Before MQTT-Duck existed, samples were scraped (via ``mqtt2prometheus``) into
    VictoriaMetrics. That instance is still reachable and still holds everything
    older than the Hive. This module walks the Hive *backwards* one day at a time,
    per already-known (sensor, metric) series, and streams the missing days in
    from VM's CSV export endpoint (``/api/v1/export/csv``).

    Idempotent & efficient by construction:

    * Only *series already present in the Hive* are considered (a series is
      "known" once the live MQTT path has created its first partition).
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
  new_text: |-
    """Backfill: fill the sensor Hive with historical data from VictoriaMetrics.

    Before MQTT-Duck existed, samples were scraped (via ``mqtt2prometheus``) into
    VictoriaMetrics. That instance is still reachable and still holds everything
    older than the Hive. This module walks *backwards* one day at a time, per
    series, and streams the missing days in from VM's CSV export endpoint
    (``/api/v1/export/csv``).

    Which series to backfill is driven entirely by *configuration*, not by the
    current contents of the Hive: for every metric accepted by the MQTT
    subscriptions (``cfg.metrics``), VM's series-discovery endpoint
    (``/api/v1/series``) is asked which sensors actually have data for it. This
    is deliberate -- the final data take-over only matters once, and it must be
    possible to run the backfill against a completely empty Hive (nothing to
    discover there yet).

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
  reason: "Moduldokumentation an das neue, konfigurationsbasierte Verhalten des Backfills anpassen"
```
/answer 5920ebaf-ebd0-4763-86d8-925abbe49336 deny die Dokumentation soll kompakt sein und nur Aspekte behandeln die sich nicht oder nicht leicht aus dem Code lesen lassen. Anforderungen sollen nicht direkt in Kommentaren gespiegelt werden.
Control Request:
```yaml
id: 6d7cf382-8349-4b76-a92f-decb01fd3cbd
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  old_text: |-
    """Backfill: fill the sensor Hive with historical data from VictoriaMetrics.

    Before MQTT-Duck existed, samples were scraped (via ``mqtt2prometheus``) into
    VictoriaMetrics. That instance is still reachable and still holds everything
    older than the Hive. This module walks the Hive *backwards* one day at a time,
    per already-known (sensor, metric) series, and streams the missing days in
    from VM's CSV export endpoint (``/api/v1/export/csv``).

    Idempotent & efficient by construction:

    * Only *series already present in the Hive* are considered (a series is
      "known" once the live MQTT path has created its first partition).
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
  new_text: |-
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
  reason: Moduldokumentation kompakt an das konfigurationsbasierte Discovery-Verhalten anpassen
```
/answer 6d7cf382-8349-4b76-a92f-decb01fd3cbd allow
Control Request:
```yaml
id: 03175897-c123-4a2d-abde-25397f669b54
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  old_text: |2-
                    samples.append(Sample(sensor=sensor, metric=metric, ts_ms=ts, value=value))
            return samples
  new_text: |2-
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
  reason: "Series-Discovery über VM /api/v1/series ergänzen, um Sensor-Namen pro Metrik ohne Hive-Zugriff zu ermitteln"
```
/answer 03175897-c123-4a2d-abde-25397f669b54 allow
Control Request:
```yaml
id: ff2b8214-14e7-4892-8e51-aa3351c7e836
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  old_text: |2-
        # -- discovery -------------------------------------------------------
        def discover_series(self) -> list[tuple[str, str]]:
            """Every ``(sensor, metric)`` pair already known to the Hive."""
            p0, p1 = self._cfg.part_names
            out: list[tuple[str, str]] = []
            if not self._hive.is_dir():
                return out
            for sensor_dir in sorted(self._hive.glob(f"{p0}=*")):
                if not sensor_dir.is_dir():
                    continue
                sensor = sensor_dir.name.split("=", 1)[1]
                for metric_dir in sorted(sensor_dir.glob(f"{p1}=*")):
                    if not metric_dir.is_dir():
                        continue
                    out.append((sensor, metric_dir.name.split("=", 1)[1]))
            return out
  new_text: |2-
        # -- discovery -------------------------------------------------------
        def discover_series(self) -> list[tuple[str, str]]:
            """Every ``(sensor, metric)`` pair, for the metrics in ``cfg.metrics``,
            that VM has recorded at least one sample for."""
            out: list[tuple[str, str]] = []
            for metric in self._cfg.metrics:
                for sensor in self._vm.list_sensors(metric.name):
                    out.append((sensor, metric.name))
            return out
  reason: Serien-Discovery des Backfills von Hive-Verzeichnisstruktur auf konfigurierte Metriken + VM-Series-Lookup umstellen
```
/answer ff2b8214-14e7-4892-8e51-aa3351c7e836 allow
Control Request:
```yaml
id: c694670e-0d29-4f51-a38a-9f41a3dd8f70
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  start: "    # -- everything"
  end: "    def close(self) -> None:"
  reason: "Aktuelle run()-Methode inspizieren, um Log-Zeile korrekt anzupassen"
```
/answer c694670e-0d29-4f51-a38a-9f41a3dd8f70 allow
Control Request:
```yaml
id: 67751e7b-6014-41ca-aa5c-6de97cbc8160
result:
  structuredContent:
    checksum: 5658c3925fa443ab6aa3b100d9ad7667e8e6abf33589b5d203aa353072cacbe1
    content: |2-
          # -- everything -------------------------------------------------------
          def run(self, log=print) -> None:
              series = self.discover_series()
              log(f"[backfill] {len(series)} known series in {self._hive}", flush=True)
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
```
/answer 67751e7b-6014-41ca-aa5c-6de97cbc8160 allow
Control Request:
```yaml
id: 4bd73b17-f130-4eaa-9265-01d289e84c2a
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  old_text: "        log(f\"[backfill] {len(series)} known series in {self._hive}\", flush=True)"
  new_text: "        log(f\"[backfill] {len(series)} series found in VM\", flush=True)"
  reason: "Log-Meldung an die neue, VM-basierte Discovery anpassen"
```
/answer 4bd73b17-f130-4eaa-9265-01d289e84c2a allow
Control Request:
```yaml
id: fce3b9d4-827b-422f-818d-d17f248e6f72
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  script: python3 -m py_compile src/xy/mqttduck/backfill.py src/xy/mqttduck/config.py && echo OK
  reason: Syntaxprüfung der geänderten Dateien
```
/answer fce3b9d4-827b-422f-818d-d17f248e6f72 allow
Control Request:
```yaml
id: 6eb7b57b-c7b0-42ae-913f-3f3c1b672c47
result:
  structuredContent:
    stdout: |
      OK
```
/answer 6eb7b57b-c7b0-42ae-913f-3f3c1b672c47 allow
ReasoningToken: 34
Text:
 Jetzt `VmExportClient` um Series-Discovery erweitern und `discover_series` in `Backfiller` umstellen:
Text:
 Jetzt noch die Log-Zeile in `run()` anpassen, da sie sich nun nicht mehr auf "known series in {hive}" bezieht:
ReasoningToken: 71
Beide Dateien kompilieren fehlerfrei. Zusammenfassung der Änderung:

**`config.py`**: `vm_series_path` (Default `/api/v1/series`) und `vm_series_url` ergänzt.

**`backfill.py`**:
- `VmExportClient.list_sensors(metric)` fragt VMs `/api/v1/series` ab und liefert die Sensor-Labels für eine Metrik.
- `Backfiller.discover_series()` iteriert nun über `cfg.metrics` (die konfigurierten, akzeptierten Metriken) und ermittelt je Metrik über VM die zugehörigen Sensoren – statt vorhandene `sensor=/metric=`-Verzeichnisse im Hive zu scannen.
- Damit läuft der Backfill auch gegen einen komplett leeren Hive, da die Serienliste nicht mehr aus dem Hive, sondern aus der Konfiguration + VM abgeleitet wird. Die Tageslücken-Erkennung (`_day_has_data`) bleibt unverändert und funktioniert bei leerem Hive bereits korrekt (liefert `False`, sodass alle Tage regulär rückwirkend befüllt werden).
