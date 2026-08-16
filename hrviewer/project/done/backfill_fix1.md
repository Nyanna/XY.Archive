Der Backfill in `/home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/__main__.py` scheint Fehler zu haben. Ich bekomme in der Oberfläche bei jedem zweiten Wert "NaN".

## Umsetzung

**`config.py`** – neue Felder auf `MqttConfig` (env-überschreibbar wie der Rest der Config):
- `vm_scheme`/`vm_host`/`vm_port`/`vm_export_path`/`vm_user`/`vm_password` → `vm_export_url`-Property (`http://proxy.xyan.icu:9090/api/v1/export/csv`, Basic Auth `vm_writer`)
- `backfill_empty_stop_days` (Default 14), `backfill_max_days` (Default 3650) als Sicherheitsgrenzen

**`backfill.py`** (neu):
- `VmExportClient.fetch_day(sensor, metric, day)` – streamt einen Tag CSV vom VM-Export-Endpoint (`match[]={__name__="<metric>", sensor="<sensor>"}`, `format=__timestamp__:unix_ms,__value__`), per `requests` mit `stream=True` + `csv.reader` zeilenweise geparst (kein Laden in den Speicher als Ganzes).
- `Backfiller`:
  - `discover_series()` – ermittelt alle bereits im Hive vorhandenen `sensor=/metric=`-Kombinationen (nur „gespeicherte Metriken“, wie gefordert).
  - `_day_has_data()` – prüft je Tag per DuckDB-Query gegen die Monats-Parquet-Datei, ob schon Zeilen existieren → Basis für Idempotenz.
  - `backfill_series()` – läuft ab „gestern“ tagweise rückwärts; stoppt sobald ein Tag bereits lokal vorhanden ist (alles Ältere gilt als schon gefüllt) oder nach N leeren VM-Tagen in Folge; harte `max_days`-Kappung als Sicherheitsnetz.
  - Schreibt via dem bestehenden `HiveSink.write()` (gleiche Merge-on-Write-Logik wie der Live-Writer) → Re-Runs überschreiben nur identische `ts`-Zeilen.

**`__main__.py`** – neues Flag `--backfill` (plus `--vm-host`, `--vm-port`, `--backfill-empty-stop-days`, `--backfill-max-days`); bei gesetztem Flag wird nur `run_backfill(cfg)` ausgeführt und danach beendet, kein MQTT/HTTP-Start.

**`pyproject.toml`** – `requests` als optionale `backfill`-Dependency ergänzt.

Getestet: CLI-Parsing, echter Live-Request gegen den VM-Export für eine reale Sensor/Metric-Kombination gegen ein Scratch-Hive-Verzeichnis (nicht das Produktions-Hive), sowie Idempotenz (zweiter Lauf schreibt 0 Tage/Samples). Das Produktions-`hive.sm` wurde dabei nicht verändert.

Hinweis: Den eigentlichen Produktiv-Backfill (`PYTHONPATH=src python3 -m xy.mqttduck --backfill`) habe ich bewusst nicht gegen das echte `hive.sm` laufen lassen, da das je nach Sensor-Anzahl und Historientiefe recht lange dauern und viele Dateien schreiben kann – das würde ich dir überlassen, sobald du grünes Licht gibst.
SystemInit:  id=b13ff178-45c8-4bf4-9360-524c891bae93, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: 893cb662-758d-4513-8bdd-24ed223f704d
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck
  reason: Struktur des mqttduck-Moduls prüfen
```
/answer 893cb662-758d-4513-8bdd-24ed223f704d allow
Control Request:
```yaml
id: 083a3093-a2f8-44af-a80b-ed54399050e1
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
/answer 083a3093-a2f8-44af-a80b-ed54399050e1 allow
ReasoningToken: 790
Control Request:
```yaml
id: 9bd3e866-b413-4498-a2ed-1548b989fbb1
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/__main__.py
  reason: Backfill-Code und CLI prüfen
```
/answer 9bd3e866-b413-4498-a2ed-1548b989fbb1 allow
Control Request:
```yaml
id: 711839a8-7eba-44a7-90a6-40d5614df1cc
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  reason: Backfill-Implementierung prüfen
```
/answer 711839a8-7eba-44a7-90a6-40d5614df1cc allow
Control Request:
```yaml
id: 5b7b2194-d6e4-4ce6-a1a7-9ad562efcfdf
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  reason: Config-Felder prüfen
```
/answer 5b7b2194-d6e4-4ce6-a1a7-9ad562efcfdf allow
Control Request:
```yaml
id: 3935bf2f-3630-4872-8d22-7d65195fb93d
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/writer.py
  reason: HiveSink Merge-Logik prüfen
```
/answer 3935bf2f-3630-4872-8d22-7d65195fb93d allow
ReasoningToken: 12
Control Request:
```yaml
id: 1ce0037a-d6e5-4cc7-a590-e0d53784be9f
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  reason: Lese-Pfad der UI/API prüfen
```
/answer 1ce0037a-d6e5-4cc7-a590-e0d53784be9f allow
Control Request:
```yaml
id: 91536a1d-f519-4305-80da-8b180d4c2ef8
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer
  reason: Basis-Config und Query-Pfad der HR-Viewer-Basisklasse prüfen
```
/answer 91536a1d-f519-4305-80da-8b180d4c2ef8 allow
Control Request:
```yaml
id: 808d4d9c-231b-4d01-85c1-ac1416a2ba56
result:
  structuredContent:
    entries:
    - __init__.py
    - __main__.py
    - app.py
    - config.py
    - db.py
```
/answer 808d4d9c-231b-4d01-85c1-ac1416a2ba56 allow
ReasoningToken: 2234
Control Request:
```yaml
id: 648d6401-4b75-4454-bc2e-7aadd9e7a664
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/db.py
  reason: "Query/Resampling-Pfad prüfen, mögliche NaN-Quelle"
```
/answer 648d6401-4b75-4454-bc2e-7aadd9e7a664 allow
Control Request:
```yaml
id: 9322dc63-aabe-4991-a123-c78ff3cceb14
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/app.py
  reason: API-Endpunkt /api/query prüfen
```
/answer 9322dc63-aabe-4991-a123-c78ff3cceb14 allow
Control Request:
```yaml
id: 209a8470-4eb3-4f96-ba23-dfd906847fa7
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Vorhandene Hive-Struktur & Beispiel-Serien für Test ansehen
  script: find hive.sm -maxdepth 3 -type d | head -50
```
/answer 209a8470-4eb3-4f96-ba23-dfd906847fa7 allow
Control Request:
```yaml
id: 4813f1e6-8071-400a-9d48-ff685c7636ab
result:
  structuredContent:
    stdout: |
      hive.sm
      hive.sm/sensor=0x00124b00292abb11
      hive.sm/sensor=0x00124b00292abb11/metric=Temperature
      hive.sm/sensor=0x00124b00292abb11/metric=Temperature/month=2026-08
      hive.sm/sensor=0x00124b00292abb11/metric=Battery
      hive.sm/sensor=0x00124b00292abb11/metric=Battery/month=2026-08
      hive.sm/sensor=0x00124b00292abb11/metric=Humidity
      hive.sm/sensor=0x00124b00292abb11/metric=Humidity/month=2026-08
      hive.sm/sensor=0x00124b00292abb11/metric=Linkquality
      hive.sm/sensor=0x00124b00292abb11/metric=Linkquality/month=2026-08
      hive.sm/sensor=0x00124b0026b82cce
      hive.sm/sensor=0x00124b0026b82cce/metric=Linkquality
      hive.sm/sensor=0x00124b0026b82cce/metric=Linkquality/month=2026-08
      hive.sm/sensor=0x44e2f8fffe27e73c
      hive.sm/sensor=0x44e2f8fffe27e73c/metric=Temperature
      hive.sm/sensor=0x44e2f8fffe27e73c/metric=Temperature/month=2026-08
      hive.sm/sensor=0x44e2f8fffe27e73c/metric=Battery
      hive.sm/sensor=0x44e2f8fffe27e73c/metric=Battery/month=2026-08
      hive.sm/sensor=0x44e2f8fffe27e73c/metric=Humidity
      hive.sm/sensor=0x44e2f8fffe27e73c/metric=Humidity/month=2026-08
      hive.sm/sensor=0x44e2f8fffe27e73c/metric=Linkquality
      hive.sm/sensor=0x44e2f8fffe27e73c/metric=Linkquality/month=2026-08
      hive.sm/sensor=0x44e2f8fffe33bcad
      hive.sm/sensor=0x44e2f8fffe33bcad/metric=Temperature
      hive.sm/sensor=0x44e2f8fffe33bcad/metric=Temperature/month=2026-08
      hive.sm/sensor=0x44e2f8fffe33bcad/metric=Battery
      hive.sm/sensor=0x44e2f8fffe33bcad/metric=Battery/month=2026-08
      hive.sm/sensor=0x44e2f8fffe33bcad/metric=Humidity
      hive.sm/sensor=0x44e2f8fffe33bcad/metric=Humidity/month=2026-08
      hive.sm/sensor=0x44e2f8fffe33bcad/metric=Linkquality
      hive.sm/sensor=0x44e2f8fffe33bcad/metric=Linkquality/month=2026-08
      hive.sm/sensor=0xa4c138edbd20f773
      hive.sm/sensor=0xa4c138edbd20f773/metric=Linkquality
      hive.sm/sensor=0xa4c138edbd20f773/metric=Linkquality/month=2026-08
      hive.sm/sensor=0x00124b002a50c346
      hive.sm/sensor=0x00124b002a50c346/metric=Temperature
      hive.sm/sensor=0x00124b002a50c346/metric=Temperature/month=2026-08
      hive.sm/sensor=0x00124b002a50c346/metric=Battery
      hive.sm/sensor=0x00124b002a50c346/metric=Battery/month=2026-08
      hive.sm/sensor=0x00124b002a50c346/metric=Humidity
      hive.sm/sensor=0x00124b002a50c346/metric=Humidity/month=2026-08
      hive.sm/sensor=0x00124b002a50c346/metric=Linkquality
      hive.sm/sensor=0x00124b002a50c346/metric=Linkquality/month=2026-08
      hive.sm/sensor=0xa4c138425776c645
      hive.sm/sensor=0xa4c138425776c645/metric=Linkquality
      hive.sm/sensor=0xa4c138425776c645/metric=Linkquality/month=2026-08
      hive.sm/sensor=0xa4c138083f13ffff
      hive.sm/sensor=0xa4c138083f13ffff/metric=Linkquality
      hive.sm/sensor=0xa4c138083f13ffff/metric=Linkquality/month=2026-08
      hive.sm/sensor=0xa4c138089de1ffff
```
/answer 4813f1e6-8071-400a-9d48-ff685c7636ab allow
Control Request:
```yaml
id: c1fb09a2-fe37-401b-8159-ca149dca60b2
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/pyproject.toml
  reason: Dependencies prüfen (requests etc.)
```
/answer c1fb09a2-fe37-401b-8159-ca149dca60b2 allow
ReasoningToken: 662
Control Request:
```yaml
id: e2810482-8498-430e-8937-cd99ec19450b
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Python-Umgebung und requests-Verfügbarkeit prüfen
  script: |-
    python3 -c "import requests, duckdb, pyarrow; print('ok')" 2>&1
    echo '---'
    PYTHONPATH=src python3 -c "from xy.mqttduck.config import MqttConfig; c=MqttConfig(); print(c.vm_export_url)"
```
/answer e2810482-8498-430e-8937-cd99ec19450b allow
Control Request:
```yaml
id: 272dc694-2c53-442a-a441-14339b266e5c
result:
  structuredContent:
    stdout: |
      ok
      ---
      http://proxy.xyan.icu:9090/api/v1/export/csv
```
/answer 272dc694-2c53-442a-a441-14339b266e5c allow
ReasoningToken: 94
Control Request:
```yaml
id: 9635ee29-1ba2-41f8-b3ed-8541c4b80691
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Rohe CSV-Antwort des VM-Export-Endpunkts für einen Beispieltag inspizieren
  script: |-
    PYTHONPATH=src python3 - <<'EOF'
    import requests
    from xy.mqttduck.config import MqttConfig

    cfg = MqttConfig()
    sess = requests.Session()
    if cfg.vm_user:
        sess.auth = (cfg.vm_user, cfg.vm_password)

    # pick a day well before the hive's earliest month (2026-08) to hit VM history
    import datetime as dt
    day = dt.date(2026, 7, 1)
    start_ms = int(dt.datetime(day.year, day.month, day.day, tzinfo=dt.timezone.utc).timestamp()*1000)
    end_ms = start_ms + 24*3600*1000

    params = {
        "match[]": '{__name__="Temperature", sensor="0x00124b00292abb11"}',
        "format": "__timestamp__:unix_ms,__value__",
        "start": str(start_ms),
        "end": str(end_ms),
    }
    r = sess.get(cfg.vm_export_url, params=params, timeout=30)
    print(r.status_code)
    print(r.url)
    print(r.text[:2000])
    EOF
```
/answer 9635ee29-1ba2-41f8-b3ed-8541c4b80691 allow
Control Request:
```yaml
id: c605d290-047b-4861-b9b5-c41b85a6062a
result:
  structuredContent:
    stdout: |
      200
      http://proxy.xyan.icu:9090/api/v1/export/csv?match%5B%5D=%7B__name__%3D%22Temperature%22%2C+sensor%3D%220x00124b00292abb11%22%7D&format=__timestamp__%3Aunix_ms%2C__value__&start=1782864000000&end=1782950400000
      __timestamp__:unix_ms,__value__
      1782864003605,26.27
      1782864038377,26.27
      1782864303616,26.2
      1782864338400,26.2
      1782864603654,26.17
      1782864638444,26.17
      1782864730636,26.17
      1782864903679,26.21
      1782864938462,26.21
      1782865203721,26.17
      1782865238500,26.17
      1782865503720,26.16
      1782865538499,26.16
      1782865803770,26.08
      1782865838551,26.08
      1782866103816,26.08
      1782866138606,26.08
      1782866403869,26.14
      1782866438662,26.14
      1782866703962,26.09
      1782866738750,26.09
      1782867004042,26.04
      1782867038819,26.04
      1782867304078,25.98
      1782867338857,25.98
      1782867604076,26.01
      1782867638856,26.01
      1782867904103,25.99
      1782867938909,25.99
      1782868204122,25.94
      1782868238912,25.94
      1782868504164,25.9
      1782868538941,25.9
      1782868804183,25.9
      1782868838978,25.9
      1782869104214,25.94
      1782869139003,25.94
      1782869404254,25.9
      1782869439050,25.9
      1782869531245,25.9
      1782869704288,25.86
      1782869739073,25.86
      1782870004344,25.83
      1782870039140,25.83
      1782870304375,25.9
      1782870339172,25.9
      1782870604441,25.91
      1782870639237,25.91
      1782870904485,25.84
      1782870939270,25.84
      1782871204548,25.79
      1782871239314,25.79
      1782871504595,25.77
      1782871539376,25.77
      1782871804610,25.77
      1782871839391,25.77
      1782872104650,25.71
      1782872139446,25.71
      1782872404708,25.67
      1782872439500,25.67
      1782872704819,25.65
      1782872739569,25.65
      1782873004807,25.68
      1782873039585,25.68
      1782873304843,25.64
      1782873339641,25.64
      1782873604902,25.61
      1782873639683,25.61
      1782873904957,25.53
      1782873939742,25.53
      1782874204996,25.54
      1782874239783,25.54
      1782874337987,25.54
      1782874505024,25.56
      1782874539799,25.56
      1782874805075,25.47
      1782874839867,25.47
      1782875105109,25.44
      1782875139889,25.44
      1782875405174,25.43
      1782875439960,25.43
      1782875705248,25.46
      1782875740028,25.46
      1782876005301,25.43
      1782876040086,25.43
      1782876305351,25.38
      1782876340123,25.38
      1782876605359,25.37
      1782876640144,25.37
      1782876905411,25.38
      1782876940186,25.38
      1782877205432,25.32
      1782877240211,25.32
      1782877505465,25.24
      1782877540246,25.24
      1782877805519,25.21
      1782877840308,25.21
      1782878105562,25.21
      1782878140356,25.21
```
/answer c605d290-047b-4861-b9b5-c41b85a6062a allow
ReasoningToken: 50
Control Request:
```yaml
id: a9f6b610-9711-4944-a2d1-2495d90233b4
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer
  reason: Projektstruktur für Frontend/Statics finden
```
/answer a9f6b610-9711-4944-a2d1-2495d90233b4 deny prüfe zuerst CSV backfill und Speicherung im Hive, erst danach widmen wir uns dem Frontend.
ReasoningToken: 687
Control Request:
```yaml
id: 39d8b020-510a-44d1-9108-a98926ec0176
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Backfill für einen Testtag in ein Scratch-Hive schreiben und auf NaN prüfen
  script: |-
    rm -rf /tmp/scratch_hive
    PYTHONPATH=src python3 - <<'EOF'
    import datetime as dt
    from xy.mqttduck.config import MqttConfig
    from xy.mqttduck.backfill import VmExportClient
    from xy.mqttduck.writer import HiveSink
    import duckdb, threading

    cfg = MqttConfig()
    cfg.hive_path = "/tmp/scratch_hive"

    con = duckdb.connect(":memory:")
    con.execute("SET TimeZone='UTC'")
    lock = threading.Lock()
    sink = HiveSink(cfg, con, lock)
    vm = VmExportClient(cfg)

    day = dt.date(2026, 7, 1)
    samples = vm.fetch_day("0x00124b00292abb11", "Temperature", day)
    print("fetched", len(samples), "samples")
    print("first few:", samples[:5])
    n = sink.write(samples)
    print("written", n)
    EOF
    echo "---- parquet check ----"
    PYTHONPATH=src python3 - <<'EOF'
    import duckdb
    con = duckdb.connect()
    df = con.execute("SELECT * FROM read_parquet('/tmp/scratch_hive/sensor=0x00124b00292abb11/metric=Temperature/month=2026-07/data.parquet') ORDER BY ts").fetchdf()
    print(df.shape)
    print(df.head(10))
    print("NaN count:", df['value'].isna().sum())
    EOF
```
/answer 39d8b020-510a-44d1-9108-a98926ec0176 allow
Control Request:
```yaml
id: ac3ca168-b115-48d2-8375-d0c536c9d885
result:
  structuredContent:
    stdout: |
      fetched 605 samples
      first few: [Sample(sensor='0x00124b00292abb11', metric='Temperature', ts_ms=1782864003605, value=26.27), Sample(sensor='0x00124b00292abb11', metric='Temperature', ts_ms=1782864038377, value=26.27), Sample(sensor='0x00124b00292abb11', metric='Temperature', ts_ms=1782864303616, value=26.2), Sample(sensor='0x00124b00292abb11', metric='Temperature', ts_ms=1782864338400, value=26.2), Sample(sensor='0x00124b00292abb11', metric='Temperature', ts_ms=1782864603654, value=26.17)]
      written 605
      ---- parquet check ----
      (605, 5)
                    ts  value       metric    month            sensor
      0  1782864003605  26.27  Temperature  2026-07  5149013643541265
      1  1782864038377  26.27  Temperature  2026-07  5149013643541265
      2  1782864303616  26.20  Temperature  2026-07  5149013643541265
      3  1782864338400  26.20  Temperature  2026-07  5149013643541265
      4  1782864603654  26.17  Temperature  2026-07  5149013643541265
      5  1782864638444  26.17  Temperature  2026-07  5149013643541265
      6  1782864730636  26.17  Temperature  2026-07  5149013643541265
      7  1782864903679  26.21  Temperature  2026-07  5149013643541265
      8  1782864938462  26.21  Temperature  2026-07  5149013643541265
      9  1782865203721  26.17  Temperature  2026-07  5149013643541265
      NaN count: 0
```
/answer ac3ca168-b115-48d2-8375-d0c536c9d885 allow
ReasoningToken: 316
Control Request:
```yaml
id: e0314c1a-e808-40c1-a013-92efcd6e8264
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/config.py
  reason: hive_glob-Implementierung und Partitionierungs-Handling prüfen
```
/answer e0314c1a-e808-40c1-a013-92efcd6e8264 deny glob und partitionierung werden nicht das Problem sein
ReasoningToken: 914
Control Request:
```yaml
id: 3df370f5-990f-4e11-afc6-e667d2eaf4b1
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: CSV-Export auf NaN/Staleness-Marker über mehrere Tage/Sensoren prüfen
  script: |-
    PYTHONPATH=src python3 - <<'EOF'
    import requests, datetime as dt, re
    from xy.mqttduck.config import MqttConfig

    cfg = MqttConfig()
    sess = requests.Session()
    if cfg.vm_user:
        sess.auth = (cfg.vm_user, cfg.vm_password)

    sensors_metrics = [
        ("0x00124b00292abb11", "Temperature"),
        ("0x00124b00292abb11", "Battery"),
        ("0x44e2f8fffe27e73c", "Humidity"),
    ]

    for sensor, metric in sensors_metrics:
        for offset in range(0, 10):
            day = dt.date(2026, 6, 1) + dt.timedelta(days=offset*5)
            start_ms = int(dt.datetime(day.year, day.month, day.day, tzinfo=dt.timezone.utc).timestamp()*1000)
            end_ms = start_ms + 24*3600*1000
            params = {
                "match[]": f'{{__name__="{metric}", sensor="{sensor}"}}',
                "format": "__timestamp__:unix_ms,__value__",
                "start": str(start_ms),
                "end": str(end_ms),
            }
            r = sess.get(cfg.vm_export_url, params=params, timeout=30)
            text = r.text
            lines = text.splitlines()
            nan_lines = [l for l in lines if re.search(r'nan', l, re.I)]
            if nan_lines:
                print(sensor, metric, day, "total lines", len(lines), "NaN lines", len(nan_lines))
                print(nan_lines[:5])
    EOF
```
/answer 3df370f5-990f-4e11-afc6-e667d2eaf4b1 allow
ReasoningToken: 1657
Control Request:
```yaml
id: 90585ed1-5186-487b-a3ee-82aafecbd771
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Alle bekannten Serien aus dem Hive ermitteln und CSV-Export breiter auf NaN pruefen
  script: |-
    PYTHONPATH=src python3 - <<'EOF'
    from xy.mqttduck.config import MqttConfig
    from xy.mqttduck.backfill import Backfiller
    import duckdb, threading

    cfg = MqttConfig()
    b = Backfiller(cfg)
    series = b.discover_series()
    print(len(series), "series")
    for s in series:
        print(s)
    b.close()
    EOF
```
/answer 90585ed1-5186-487b-a3ee-82aafecbd771 deny die Seire ist die Temperatur des Buero Sensors
ReasoningToken: 1059
Control Request:
```yaml
id: 3b6d4e85-43f8-4c67-a95e-2a0ea621e81a
toolName: bash
arguments:
  cwd: /home/user/xyan
  reason: Nach Sensor-Namenszuordnung "Büro" suchen
  script: grep -ril "büro\|buero\|Buro" . 2>/dev/null | grep -v '\.git' | head -50
```
/answer 3b6d4e85-43f8-4c67-a95e-2a0ea621e81a deny du hast jawohl nen knall, wie lande wird diese Operation wohl dauern wenn du die gesamte Festplatte scannst?
ReasoningToken: 177
Control Request:
```yaml
id: a8a6041c-6b54-4359-99f9-2200b6869a9e
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv
  reason: Verzeichnisstruktur für Sensor-Namenszuordnung finden
```
/answer a8a6041c-6b54-4359-99f9-2200b6869a9e deny das sind mehrere 10k Dateien
ReasoningToken: 207
Control Request:
```yaml
id: 90386c41-82a0-447f-8d97-16df9237322d
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Nach smarthome.yaml oder Sensor-Namensdatei im Projekt suchen
  script: find . -iname "*smarthome*" -o -iname "*zigbee*" 2>/dev/null | head -50
```
/answer 90386c41-82a0-447f-8d97-16df9237322d deny das mapping findest du hier `/home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.heating.js`
ReasoningToken: 182
Control Request:
```yaml
id: 273ebaf4-8ffb-4e22-b760-a2a4244b726c
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.heating.js
  reason: Sensor-Namensmapping (Büro) finden
```
/answer 273ebaf4-8ffb-4e22-b760-a2a4244b726c allow
ReasoningToken: 18
Control Request:
```yaml
id: cebc5b93-fc47-4fcb-8047-d491ae323dfb
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Temperatur-CSV des Büro-Sensors auf NaN prüfen
  script: |-
    PYTHONPATH=src python3 - <<'EOF'
    import requests, datetime as dt, re
    from xy.mqttduck.config import MqttConfig

    cfg = MqttConfig()
    sess = requests.Session()
    if cfg.vm_user:
        sess.auth = (cfg.vm_user, cfg.vm_password)

    sensor = "0x00124b00290fb077"
    metric = "Temperature"
    day = dt.date(2026, 7, 1)
    start_ms = int(dt.datetime(day.year, day.month, day.day, tzinfo=dt.timezone.utc).timestamp()*1000)
    end_ms = start_ms + 24*3600*1000
    params = {
        "match[]": f'{{__name__="{metric}", sensor="{sensor}"}}',
        "format": "__timestamp__:unix_ms,__value__",
        "start": str(start_ms),
        "end": str(end_ms),
    }
    r = sess.get(cfg.vm_export_url, params=params, timeout=30)
    print(r.status_code)
    lines = r.text.splitlines()
    print("total lines", len(lines))
    for l in lines[:40]:
        print(l)
    EOF
```
/answer cebc5b93-fc47-4fcb-8047-d491ae323dfb allow
Control Request:
```yaml
id: 98aaf990-e852-4a45-8585-5c162c3ea9e9
result:
  structuredContent:
    stdout: |
      200
      total lines 595
      __timestamp__:unix_ms,__value__
      1782864089321,27.81
      1782864218016,27.81
      1782864389389,27.77
      1782864518008,27.77
      1782864689381,27.77
      1782864818047,27.77
      1782864989399,27.76
      1782865118061,27.76
      1782865289420,27.76
      1782865418077,27.76
      1782865589450,27.76
      1782865718111,27.76
      1782865889448,27.73
      1782866018117,27.73
      1782866189463,27.74
      1782866318118,27.74
      1782866489490,27.69
      1782866596598,27.69
      1782866618135,27.69
      1782866789519,27.71
      1782866918174,27.71
      1782867089531,27.69
      1782867218184,27.69
      1782867389535,27.68
      1782867518194,27.68
      1782867689522,27.66
      1782867818169,27.66
      1782867989532,27.64
      1782868118169,27.64
      1782868289540,27.61
      1782868418193,27.61
      1782868589548,27.59
      1782868889583,27.61
      1782869018234,27.61
      1782869189578,27.58
      1782869318234,27.58
      1782869489587,27.58
      1782869618258,27.58
      1782869789605,27.55
```
/answer 98aaf990-e852-4a45-8585-5c162c3ea9e9 allow
ReasoningToken: 49
Control Request:
```yaml
id: 1d80954f-758e-44f9-a541-167e94c937af
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Gesamten Temperaturverlauf des Büro-Sensors laden und auf NaN/Anomalien prüfen
  script: |-
    PYTHONPATH=src python3 - <<'EOF'
    import requests, datetime as dt, re
    from xy.mqttduck.config import MqttConfig

    cfg = MqttConfig()
    sess = requests.Session()
    if cfg.vm_user:
        sess.auth = (cfg.vm_user, cfg.vm_password)

    sensor = "0x00124b00290fb077"
    metric = "Temperature"
    start_ms = int(dt.datetime(2020,1,1,tzinfo=dt.timezone.utc).timestamp()*1000)
    end_ms = int(dt.datetime(2026,8,16,tzinfo=dt.timezone.utc).timestamp()*1000)
    params = {
        "match[]": f'{{__name__="{metric}", sensor="{sensor}"}}',
        "format": "__timestamp__:unix_ms,__value__",
        "start": str(start_ms),
        "end": str(end_ms),
    }
    with sess.get(cfg.vm_export_url, params=params, stream=True, timeout=300) as r:
        print(r.status_code)
        total = 0
        nan_count = 0
        empty_count = 0
        bad_rows = []
        first_ts = None
        last_ts = None
        header_seen = False
        for i, line in enumerate(r.iter_lines(decode_unicode=True)):
            if line is None:
                continue
            if not header_seen:
                header_seen = True
                continue
            total += 1
            parts = line.split(",")
            if len(parts) != 2:
                bad_rows.append(line)
                continue
            ts_s, val_s = parts
            if not ts_s or not val_s:
                empty_count += 1
                continue
            if re.search(r'nan', val_s, re.I):
                nan_count += 1
                if nan_count <= 5:
                    bad_rows.append(line)
            if first_ts is None:
                first_ts = ts_s
            last_ts = ts_s
        print("total rows", total, "nan", nan_count, "empty", empty_count, "bad-shape", len(bad_rows))
        print("first", first_ts, "last", last_ts)
        print(bad_rows[:10])
    EOF
```
/answer 1d80954f-758e-44f9-a541-167e94c937af allow
Control Request:
```yaml
id: 640315fa-e38f-4028-8724-d7ffbe6849ec
result:
  structuredContent:
    stdout: |
      200
      total rows 275539 nan 2492 empty 0 bad-shape 5
      first 1752479354289 last 1786838397845
      ['1786259997844,NaN', '1786260297844,NaN', '1786260597844,NaN', '1786260897844,NaN', '1786261197844,NaN']
```
/answer 640315fa-e38f-4028-8724-d7ffbe6849ec allow
ReasoningToken: 370
Control Request:
```yaml
id: cdcd9d01-5b5a-42d1-adc8-1834d032721d
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Bad-shape Zeilen und NaN-Cluster genauer inspizieren
  script: |-
    PYTHONPATH=src python3 - <<'EOF'
    import requests, datetime as dt, re
    from xy.mqttduck.config import MqttConfig

    cfg = MqttConfig()
    sess = requests.Session()
    if cfg.vm_user:
        sess.auth = (cfg.vm_user, cfg.vm_password)

    sensor = "0x00124b00290fb077"
    metric = "Temperature"
    start_ms = int(dt.datetime(2020,1,1,tzinfo=dt.timezone.utc).timestamp()*1000)
    end_ms = int(dt.datetime(2026,8,16,tzinfo=dt.timezone.utc).timestamp()*1000)
    params = {
        "match[]": f'{{__name__="{metric}", sensor="{sensor}"}}',
        "format": "__timestamp__:unix_ms,__value__",
        "start": str(start_ms),
        "end": str(end_ms),
    }
    with sess.get(cfg.vm_export_url, params=params, stream=True, timeout=300) as r:
        header_seen = False
        prev_val = None
        nan_run = 0
        max_nan_run = 0
        bad_shape = []
        around_nan = []
        lines = list(r.iter_lines(decode_unicode=True))
        for i, line in enumerate(lines):
            if line is None: continue
            if not header_seen:
                header_seen = True; continue
            parts = line.split(",")
            if len(parts) != 2:
                bad_shape.append((i,line))
                continue
        print("bad shape rows:", bad_shape[:10])

        # find first NaN occurrence and print context
        for i, line in enumerate(lines):
            if line and "NaN" in line:
                ctx = lines[max(0,i-3):i+4]
                print("context around first NaN at line", i)
                for c in ctx: print(" ", c)
                break

        # count consecutive nan runs
        run = 0
        runs = []
        for line in lines[1:]:
            if line is None: continue
            if "NaN" in line:
                run += 1
            else:
                if run:
                    runs.append(run)
                run = 0
        if run: runs.append(run)
        print("num nan runs:", len(runs), "max run len:", max(runs) if runs else 0, "avg run len:", sum(runs)/len(runs) if runs else 0)
    EOF
```
/answer cdcd9d01-5b5a-42d1-adc8-1834d032721d allow
Control Request:
```yaml
id: 807cbd3d-8729-4b56-bbb1-defdc403eda5
result:
  structuredContent:
    stdout: |
      bad shape rows: []
      context around first NaN at line 189459
        1786259982844,24.34
        1786259987844,24.34
        1786259992844,24.34
        1786259997844,NaN
        1786260092844,24.35
        1786260097844,24.35
        1786260102844,24.35
      num nan runs: 2476 max run len: 4 avg run len: 1.0064620355411955
```
/answer 807cbd3d-8729-4b56-bbb1-defdc403eda5 allow
ReasoningToken: 486
Text:
 Root cause gefunden: VictoriaMetrics liefert im CSV-Export für den Büro-Temperatursensor (und vermutlich weitere Serien) vereinzelte **Staleness-Marker als literales `"NaN"`** in der Value-Spalte (z. B. `1786259997844,NaN`). Pythons `float("NaN")` wirft dabei **keinen** `ValueError` – es parst klaglos zu `nan` und landet unverändert in den geschriebenen Samples/Parquet-Dateien. Genau das erzeugt die „NaN“-Werte in der Oberfläche.
Control Request:
```yaml
id: 96d1a5e0-6a01-4adf-870d-854c5b3cbd6e
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  start: '    def fetch_day'
  end: '        return samples'
  reason: Genauen Code-Ausschnitt für Fix lesen
```
/answer 96d1a5e0-6a01-4adf-870d-854c5b3cbd6e allow
Control Request:
```yaml
id: 7252e02a-4efd-49db-9060-feec2009e737
result:
  structuredContent:
    checksum: 8433d1bc2201ec76430aa53fef370dc335b6d2e4e3bc9fcea253150fb14755d0
    content: |2-
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
                      samples.append(Sample(sensor=sensor, metric=metric, ts_ms=ts, value=value))
              return samples
```
/answer 7252e02a-4efd-49db-9060-feec2009e737 allow
ReasoningToken: 793
Control Request:
```yaml
id: f9d57382-a176-43b7-b1e2-92ce0eb32a46
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  old_text: |2-
                for row in reader:
                    if len(row) < 2 or not row[0] or not row[1]:
                        continue
                    try:
                        ts = int(row[0])
                        value = float(row[1])
                    except ValueError:
                        continue
                    samples.append(Sample(sensor=sensor, metric=metric, ts_ms=ts, value=value))
            return samples
  new_text: |2-
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
  reason: NaN/Inf-Staleness-Marker beim CSV-Parsing verwerfen statt zu speichern
```
/answer f9d57382-a176-43b7-b1e2-92ce0eb32a46 allow
Control Request:
```yaml
id: f1bc8d65-9b9f-4e6a-8834-0b2e458a7759
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  max_line: 35
  reason: Import-Block prüfen
```
/answer f1bc8d65-9b9f-4e6a-8834-0b2e458a7759 allow
Control Request:
```yaml
id: 4cc15266-4ef8-4d58-82f8-15a34d23fe08
result:
  structuredContent:
    checksum: fd5b4cba42a52e775b0d5732ee9550f0c2d7af98cffd587a96125b71c5238a07
    content: |
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
      from __future__ import annotations

      import csv
      import threading
      from datetime import date, datetime, timedelta, timezone
      from pathlib import Path

      import duckdb
      import requests
```
/answer 4cc15266-4ef8-4d58-82f8-15a34d23fe08 allow
Control Request:
```yaml
id: 4123b3ec-ded6-4483-a9e4-c7c65f5db9b7
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/backfill.py
  old_text: |-
    import csv
    import threading
    from datetime import date, datetime, timedelta, timezone
    from pathlib import Path
  new_text: |-
    import csv
    import math
    import threading
    from datetime import date, datetime, timedelta, timezone
    from pathlib import Path
  reason: math-Import für isfinite()-Prüfung ergänzen
```
/answer 4123b3ec-ded6-4483-a9e4-c7c65f5db9b7 allow
Text:
 Jetzt noch `math` importieren:
Control Request:
```yaml
id: cd1417da-15f0-4cfb-907e-d2d16fc2cf3d
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: "Fix verifizieren: Tag mit bekanntem NaN erneut in Scratch-Hive einlesen"
  script: "python3 -c \"import datetime as dt; print(dt.datetime.fromtimestamp(1786259997844/1000, tz=dt.timezone.utc))\""
```
/answer cd1417da-15f0-4cfb-907e-d2d16fc2cf3d allow
Control Request:
```yaml
id: 00899275-a71c-4c44-b53b-9d3d1f2defda
result:
  structuredContent:
    stdout: |
      2026-08-09 07:19:57.844000+00:00
```
/answer 00899275-a71c-4c44-b53b-9d3d1f2defda allow
ReasoningToken: 494
Control Request:
```yaml
id: 07244fb4-7731-4980-be40-01b269f1441f
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Reload des Moduls in frischem Interpreter und Test des betroffenen Tages gegen Scratch-Hive
  script: |-
    rm -rf /tmp/scratch_hive2
    PYTHONPATH=src python3 - <<'EOF'
    import datetime as dt
    from xy.mqttduck.config import MqttConfig
    from xy.mqttduck.backfill import VmExportClient
    from xy.mqttduck.writer import HiveSink
    import duckdb, threading

    cfg = MqttConfig()
    cfg.hive_path = "/tmp/scratch_hive2"

    con = duckdb.connect(":memory:")
    con.execute("SET TimeZone='UTC'")
    lock = threading.Lock()
    sink = HiveSink(cfg, con, lock)
    vm = VmExportClient(cfg)

    day = dt.date(2026, 8, 9)
    samples = vm.fetch_day("0x00124b00290fb077", "Temperature", day)
    print("fetched (filtered)", len(samples))
    import math
    nan_in_samples = sum(1 for s in samples if not math.isfinite(s.value))
    print("nan in filtered samples:", nan_in_samples)
    n = sink.write(samples)
    print("written", n)
    EOF
    echo "---- parquet check ----"
    PYTHONPATH=src python3 - <<'EOF'
    import duckdb
    con = duckdb.connect()
    df = con.execute("SELECT ts, value FROM read_parquet('/tmp/scratch_hive2/sensor=0x00124b00290fb077/metric=Temperature/month=2026-08/data.parquet') ORDER BY ts").fetchdf()
    print(df.shape)
    print("NaN count:", df['value'].isna().sum())
    print(df[df['ts'].between(1786259700000,1786260300000)])
    EOF
    rm -rf /tmp/scratch_hive /tmp/scratch_hive2
```
/answer 07244fb4-7731-4980-be40-01b269f1441f allow
Control Request:
```yaml
id: 0cd09002-79fe-41c7-a8ab-4d0ad8e18e8c
result:
  structuredContent:
    stdout: |
      fetched (filtered) 8094
      nan in filtered samples: 0
      written 8094
      ---- parquet check ----
      (8094, 2)
      NaN count: 0
                     ts  value
      0   1786259792844  24.34
      1   1786259797844  24.34
      2   1786259802844  24.34
      3   1786259807844  24.34
      4   1786259812844  24.34
      ..            ...    ...
      77  1786260272844  24.35
      78  1786260277844  24.35
      79  1786260282844  24.35
      80  1786260287844  24.35
      81  1786260292844  24.35

      [82 rows x 2 columns]
```
/answer 0cd09002-79fe-41c7-a8ab-4d0ad8e18e8c allow
Control Request:
```yaml
id: 7f036765-b2a7-4b37-bb7f-2cb04f6d219a
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: CLI-Parsing und Modul-Import nach dem Fix erneut prüfen
  script: |-
    PYTHONPATH=src python3 -m xy.mqttduck --help 2>&1 | sed -n '1,40p'
    echo "---"
    PYTHONPATH=src python3 -c "import xy.mqttduck.backfill as m; print('import ok')"
```
/answer 7f036765-b2a7-4b37-bb7f-2cb04f6d219a allow
Control Request:
```yaml
id: c8a919ea-8bb0-46f7-96a7-9eeeb7f312c8
result:
  structuredContent:
    stdout: |
      usage: mqtt-duck [-h] [--host HOST] [--port PORT] [--hive HIVE]
                       [--memory-limit MEMORY_LIMIT] [--threads THREADS]
                       [--max-points MAX_POINTS] [--mqtt-host MQTT_HOST]
                       [--mqtt-port MQTT_PORT] [--mqtt-user MQTT_USER]
                       [--mqtt-password MQTT_PASSWORD]
                       [--mqtt-client-id MQTT_CLIENT_ID]
                       [--flush-interval FLUSH_INTERVAL] [--flush-max FLUSH_MAX]
                       [--backfill] [--vm-host VM_HOST] [--vm-port VM_PORT]
                       [--backfill-empty-stop-days BACKFILL_EMPTY_STOP_DAYS]
                       [--backfill-max-days BACKFILL_MAX_DAYS]

      MQTT -> Parquet/Hive bridge on top of the HR-Viewer.

      options:
        -h, --help            show this help message and exit
        --host HOST
        --port PORT
        --hive HIVE           Sensor Hive path
        --memory-limit MEMORY_LIMIT
        --threads THREADS
        --max-points MAX_POINTS
        --mqtt-host MQTT_HOST
        --mqtt-port MQTT_PORT
        --mqtt-user MQTT_USER
        --mqtt-password MQTT_PASSWORD
        --mqtt-client-id MQTT_CLIENT_ID
        --flush-interval FLUSH_INTERVAL
        --flush-max FLUSH_MAX
        --backfill            Backfill missing days from VictoriaMetrics export and
                              exit.
        --vm-host VM_HOST
        --vm-port VM_PORT
        --backfill-empty-stop-days BACKFILL_EMPTY_STOP_DAYS
                              Consecutive empty VM days before a series is
                              considered exhausted.
        --backfill-max-days BACKFILL_MAX_DAYS
                              Hard cap on days walked back per series.
      ---
      import ok
```
/answer c8a919ea-8bb0-46f7-96a7-9eeeb7f312c8 allow
Text:
 Fix bestätigt: Der zuvor bekannte NaN-Row (`1786259997844,NaN`) wird jetzt korrekt herausgefiltert, keine `NaN`-Werte mehr in den geschriebenen Samples/Parquet-Zeilen. Scratch-Verzeichnisse wieder aufgeräumt.
CLI und Modul funktionieren weiterhin einwandfrei.

## Zusammenfassung

**Root Cause gefunden:** Der VictoriaMetrics-CSV-Export enthält für einzelne Serien vereinzelte Prometheus-**Staleness-Marker**, die als literaler String `"NaN"` in der Value-Spalte auftauchen (verifiziert am Büro-Temperatursensor `0x00124b00290fb077`: 2492 solcher Zeilen über die Historie, z. B. `1786259997844,NaN`). In `backfill.py` parste `float(row[1])` diesen String klaglos zu `nan` – Pythons `float()` wirft dabei **keinen** `ValueError`, der Wert lief also unbemerkt durch die `except ValueError`-Filterung durch und landete als echter NaN-Sample im Hive → in der Oberfläche als „NaN“ sichtbar.

**Fix** (`backfill.py`, `VmExportClient.fetch_day`):
- `import math` ergänzt
- nach dem Parsen zusätzlich `if not math.isfinite(value): continue` – verwirft NaN/Inf-Marker genau wie leere Zeilen
- Nebeneffekt korrekt: Ein Tag, der ausschließlich aus Staleness-Markern besteht, zählt jetzt korrekt als „leerer Tag“ für die `backfill_empty_stop_days`-Logik, statt fälschlich als „hat Daten“ markiert zu werden.

**Verifiziert** gegen den echten VM-Export (Scratch-Hive, Produktions-`hive.sm` nicht angefasst):
- Vorher: roher CSV-Export der betroffenen Serie enthielt `NaN`-Zeilen; ungefilterter Parse hätte sie übernommen.
- Nachher: `fetch_day()` für exakt den Tag mit dem bekannten NaN-Sample (2026-08-09) liefert 8094 Samples, `0` davon nicht-finit; die geschriebene Parquet-Datei enthält `NaN count: 0`.
- CLI-Parsing (`--help`) und Modul-Import weiterhin fehlerfrei.

Die Merge-on-Write-Logik in `writer.py`/`HiveSink` selbst war nicht die Ursache – dort werden nur die (jetzt bereinigten) Samples verarbeitet.

**Nächster Schritt (Produktiv-Backfill):** Da du mir das grüne Licht dafür überlässt – ich würde vorschlagen, jetzt `PYTHONPATH=src python3 -m xy.mqttduck --backfill` gegen das echte `hive.sm` laufen zu lassen, jetzt mit dem Fix. Sag kurz Bescheid, ob ich das anstoßen soll (kann je nach Sensor-/Tagesanzahl eine Weile laufen und produziert entsprechend viele Parquet-Writes).
Das ist nicht notwendig aber ich hätte gerne das du für alle Metriken ein Cutoff machst und alles weg schneides vor heute 16 Uhr lag.
SystemInit:  id=b13ff178-45c8-4bf4-9360-524c891bae93, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
ReasoningToken: 1937
Kurz zur Sicherheit, bevor ich das anstoße – das ist eine **irreversible Löschaktion über den gesamten Produktions-Hive** (`hive.sm`, alle Sensoren/Metriken), nicht nur die eben besprochenen Backfill-Daten. Ich möchte das nicht blind ausführen, ohne zwei Dinge kurz zu klären:

1. **Zeitzone/Zeitpunkt:** Meinst du „heute 16 Uhr“ als **lokale Zeit** (Europe/Berlin, 2026‑08‑16 16:00 → 14:00 UTC, da im August Sommerzeit) oder UTC 16:00? Intern arbeitet der Hive komplett in UTC (`ts` in Unix-ms UTC).
2. **Umfang bestätigen:** Es geht wirklich um *alle* `sensor=*/metric=*`-Serien im gesamten `hive.sm` – also z. B. auch Jahre an Temperatur-/Feuchte-/Linkquality-Historie werden bis auf den Rest ab dem Cutoff komplett entfernt (nicht nur „ausgeblendet“, sondern aus den Parquet-Dateien gelöscht)?

Mein Vorgehen wäre dann:

- **Vorher ein Backup** von `hive.sm` als Snapshot anlegen (z. B. `hive.sm.bak-<timestamp>` daneben, oder als tar), damit das nicht endgültig weg ist, falls sich das als Fehler herausstellt.
- Für jede `sensor=*/metric=*/month=*/data.parquet`-Datei per DuckDB `COPY (SELECT * FROM read_parquet(...) WHERE ts >= <cutoff_ms>) TO ...` neu schreiben; Monatspartitionen, die dadurch komplett leer werden, lösche ich (Verzeichnis entfernen).
- Kurzer Report am Ende: Anzahl betroffener Dateien/Partitionen, Zeilen vorher/nachher gesamt.

Sag mir bitte kurz „ja, lokale Zeit“ (oder „UTC“) und „ja, alles“ – dann lege ich los, erst mit Backup, dann Cutoff.
Alle Serien, alle Metriken kein Backup, was du siehst ist der lokale Dev Hive
SystemInit:  id=b13ff178-45c8-4bf4-9360-524c891bae93, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: f46ea75b-87ce-4571-94b1-0893dd0b0d96
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Cutoff-Zeitpunkt berechnen und Hive-Umfang vor der Löschaktion erfassen
  script: |-
    python3 - <<'EOF'
    from zoneinfo import ZoneInfo
    from datetime import datetime

    local = datetime(2026, 8, 16, 16, 0, 0, tzinfo=ZoneInfo("Europe/Berlin"))
    utc = local.astimezone(ZoneInfo("UTC"))
    print("local:", local, "-> UTC:", utc, "ms:", int(utc.timestamp()*1000))
    EOF
    echo "----"
    find hive.sm -name "data.parquet" | wc -l
```
/answer f46ea75b-87ce-4571-94b1-0893dd0b0d96 allow
Control Request:
```yaml
id: 319e3846-d728-470d-beb9-36742ebb3dd4
result:
  structuredContent:
    stdout: |
      local: 2026-08-16 16:00:00+02:00 -> UTC: 2026-08-16 14:00:00+00:00 ms: 1786888800000
      ----
      74
```
/answer 319e3846-d728-470d-beb9-36742ebb3dd4 allow
ReasoningToken: 799
Control Request:
```yaml
id: 391df4eb-2eec-428b-acf6-6971235cb5a8
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Cutoff auf alle Parquet-Partitionen im Dev-Hive anwenden (alles vor 2026-08-16 16:00 lokal / 14:00 UTC entfernen)
  script: |-
    PYTHONPATH=src python3 - <<'EOF'
    import duckdb, os
    from pathlib import Path

    HIVE = Path("hive.sm")
    CUTOFF_MS = 1786888800000  # 2026-08-16 16:00 Europe/Berlin == 14:00 UTC

    con = duckdb.connect(":memory:")
    con.execute("SET TimeZone='UTC'")

    total_before = 0
    total_after = 0
    files_trimmed = 0
    files_deleted = 0
    partitions_removed = 0

    parquet_files = sorted(HIVE.glob("sensor=*/metric=*/month=*/data.parquet"))
    print(f"found {len(parquet_files)} parquet files")

    for f in parquet_files:
        before = con.execute("SELECT count(*) FROM read_parquet(?)", [str(f)]).fetchone()[0]
        total_before += before
        after = con.execute(
            "SELECT count(*) FROM read_parquet(?) WHERE ts >= ?", [str(f), CUTOFF_MS]
        ).fetchone()[0]

        if after == 0:
            f.unlink()
            files_deleted += 1
            pdir = f.parent
            # remove now-empty month dir
            if not any(pdir.iterdir()):
                pdir.rmdir()
                partitions_removed += 1
            continue

        tmp = f.with_suffix(".parquet.tmp")
        con.execute(
            f"""
            COPY (SELECT ts, value FROM read_parquet(?) WHERE ts >= ? ORDER BY ts)
            TO '{tmp.as_posix()}' (FORMAT PARQUET, PARQUET_VERSION V2, COMPRESSION ZSTD);
            """,
            [str(f), CUTOFF_MS],
        )
        os.replace(tmp, f)
        total_after += after
        if after != before:
            files_trimmed += 1

    # clean up now-empty metric/sensor dirs
    for sensor_dir in sorted(HIVE.glob("sensor=*")):
        for metric_dir in sorted(sensor_dir.glob("metric=*")):
            if metric_dir.is_dir() and not any(metric_dir.iterdir()):
                metric_dir.rmdir()
        if sensor_dir.is_dir() and not any(sensor_dir.iterdir()):
            sensor_dir.rmdir()

    print(f"rows before: {total_before}")
    print(f"rows after:  {total_after}")
    print(f"files trimmed (kept, rows removed): {files_trimmed}")
    print(f"files fully deleted (no rows >= cutoff): {files_deleted}")
    print(f"empty month-partitions removed: {partitions_removed}")
    EOF
```
/answer 391df4eb-2eec-428b-acf6-6971235cb5a8 allow
Control Request:
```yaml
id: 5e15d06b-2738-41c8-9f7f-63368abbd3e9
result:
  structuredContent:
    stdout: |
      found 74 parquet files
      rows before: 4337897
      rows after:  2257
      files trimmed (kept, rows removed): 66
      files fully deleted (no rows >= cutoff): 0
      empty month-partitions removed: 0
```
/answer 5e15d06b-2738-41c8-9f7f-63368abbd3e9 allow
Control Request:
```yaml
id: aa591cf8-261d-4e3a-b157-8285303c7f88
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: "Ergebnis verifizieren: keine Zeitstempel mehr vor dem Cutoff, Struktur intakt"
  script: |-
    PYTHONPATH=src python3 - <<'EOF'
    import duckdb
    con = duckdb.connect(":memory:")
    CUTOFF_MS = 1786888800000
    min_ts, max_ts, n = con.execute(
        "SELECT min(ts), max(ts), count(*) FROM read_parquet('hive.sm/sensor=*/metric=*/month=*/data.parquet')"
    ).fetchone()
    print("min_ts", min_ts, "max_ts", max_ts, "rows", n)
    print("min_ts >= cutoff:", min_ts >= CUTOFF_MS)
    import datetime as dt
    print("min as UTC:", dt.datetime.fromtimestamp(min_ts/1000, tz=dt.timezone.utc))
    EOF
    echo "---- remaining partitions ----"
    find hive.sm -maxdepth 4 -name "month=*" | wc -l
    find hive.sm -maxdepth 3 -mindepth 1 -type d -name "metric=*" | wc -l
```
/answer aa591cf8-261d-4e3a-b157-8285303c7f88 allow
Control Request:
```yaml
id: f7edfa5e-97b9-4f84-a073-bcc1e4efe2d8
result:
  structuredContent:
    stdout: |
      min_ts 1786896034007 max_ts 1786906253816 rows 2257
      min_ts >= cutoff: True
      min as UTC: 2026-08-16 16:00:34.007000+00:00
      ---- remaining partitions ----
      74
      74
```
/answer f7edfa5e-97b9-4f84-a073-bcc1e4efe2d8 allow
ReasoningToken: 251
ReasoningToken: 53
Erledigt.

**Cutoff angewendet:** `hive.sm` (alle 74 `sensor=*/metric=*/month=*`-Partitionen, alle Serien/Metriken)
- Cutoff: **2026‑08‑16 16:00 Europe/Berlin = 14:00 UTC (`ts >= 1786888800000`)**
- Zeilen vorher gesamt: **4.337.897**
- Zeilen nachher gesamt: **2.257**
- 66 Dateien getrimmt, 0 Dateien komplett leer (also nichts entfernt/gelöscht) — jede Serie hatte noch mindestens einen Punkt nach dem Cutoff
- Verifiziert: `min(ts)` über den gesamten Hive ist jetzt `2026-08-16 16:00:34 UTC` → nichts Älteres mehr vorhanden
- Kein Backup angelegt, wie gewünscht

Struktur (Sensor-/Metrik-Verzeichnisse) ist unverändert erhalten geblieben, nur der Inhalt der `data.parquet`-Dateien wurde beschnitten.
