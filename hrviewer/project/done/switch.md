Smarthome und Engine `/home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/__init__.py` soll in MQTT Duck nur durch Aktivierung eines CLI-Arguments aktiviert werden. Der Metrikserver braucht diese Funktionalität nicht.
SystemInit:  id=05bbecd1-ee44-47ba-b8a4-74d72a3f6da7, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: 1470-3
toolName: python-ast-outline
arguments:
  paths:
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/__init__.py
  reason: Struktur der Smarthome-Engine verstehen
```
/answer 1470-3 allow
Control Request:
```yaml
id: 1470-4
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy
  reason: Projektstruktur finden für CLI-Einstiegspunkte und Metrikserver
```
/answer 1470-4 allow
Control Request:
```yaml
id: 1470-5
result:
  structuredContent:
    entries:
    - __init__.py
    - hrv/__init__.py
    - hrv/viewer/__init__.py
    - hrv/viewer/__main__.py
    - hrv/viewer/app.py
    - hrv/viewer/arrow_ipc.py
    - hrv/viewer/config.py
    - hrv/viewer/db.py
    - hrv/viewer/fpstore.py
    - hrv/viewer/store.py
    - mqttduck/__init__.py
    - mqttduck/__main__.py
    - mqttduck/app.py
    - mqttduck/backfill.py
    - mqttduck/client.py
    - mqttduck/config.py
    - mqttduck/transform.py
    - mqttduck/writer.py
    - smarthome/__init__.py
    - smarthome/config.py
    - smarthome/cron.py
    - smarthome/engine.py
    - smarthome/web.py
```
/answer 1470-5 allow
ReasoningToken: 17
Control Request:
```yaml
id: 1470-6
toolName: python-ast-outline
arguments:
  paths:
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/__main__.py
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/engine.py
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/config.py
  reason: CLI-Argumente und Startlogik von mqttduck sowie Smarthome-Engine-Struktur analysieren
```
/answer 1470-6 allow
Text:
 Jetzt die relevanten Dateien im Detail lesen: `__main__.py` (CLI-Args), `app.py` (Nutzung des Engines), `config.py` (SmartHomeConfig.enabled?).
Control Request:
```yaml
id: 1470-7
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/__main__.py
  reason: "CLI-Argumente und build_config-Logik prüfen, um Smarthome-Aktivierung per Argument einzubauen"
```
/answer 1470-7 allow
Control Request:
```yaml
id: 1470-8
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  reason: Nutzung von SmartHomeEngine/SmartHomeConfig in MqttDuck.app verstehen
```
/answer 1470-8 allow
Control Request:
```yaml
id: 1470-9
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/config.py
  reason: SmartHomeConfig-Struktur inkl. from_mqtt prüfen
```
/answer 1470-9 allow
Control Request:
```yaml
id: 1470-a
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  script: grep -rn -i "metrikserver\|metrics.server\|mirror" --include="*.py" --include="*.md" --include="*.service" --include="*.sh" . | grep -v '.git'
  reason: "Suche nach Referenzen auf 'Metrikserver' im Repo, um Deployment-Kontext zu verstehen"
```
/answer 1470-a deny das ist nicht notwendig, ein CLI-Argument reicht den Rest mache ich
ReasoningToken: 150
Control Request:
```yaml
id: 1470-b
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  min_line: 77
  max_line: 190
  reason: "MqttConfig-Felder ansehen, um passenden Ort für smarthome_enabled zu finden"
```
/answer 1470-b allow
Control Request:
```yaml
id: 1470-c
result:
  structuredContent:
    checksum: d5d2c524fff25236dc0ad31daa3e5b5851af1784684b6fede3cec6f6edc4ea06
    content: |+
      class MqttConfig(Config):
          """MQTT-Duck runtime configuration (extends the HR-Viewer Config)."""

          # ---- Hive location & partition scheme (overrides the base defaults) ----
          hive_path: str = field(
              default_factory=lambda: _env("SMD_HIVE_PATH", DEFAULT_SM_HIVE_PATH)
          )
          part_names: ClassVar[tuple[str, str]] = ("sensor", "metric")
          time_part: ClassVar[str] = "month"

          # ---- Storage backend (overrides the base HRV_BACKEND env name) ----
          # "duckdb" on the main server, "fastparquet" on the NanoPi mirror.
          backend: str = field(default_factory=lambda: _env("SMD_BACKEND", "duckdb"))

          # ---- HTTP server (distinct default port so it can run beside hrv) ----
          port: int = field(default_factory=lambda: int(_env("SMD_PORT", "8081")))

          # Static root ("/") redirect target -- points to the heating dashboard
          # view by default.
          root_redirect: str = field(
              default_factory=lambda: _env(
                  "SMD_ROOT_REDIRECT", "dashboard.html?config=heating"
              )
          )

          # ---- MQTT broker (Mosquitto) ----
          mqtt_host: str = field(default_factory=lambda: _env("SMD_MQTT_HOST", "127.0.0.1"))
          mqtt_port: int = field(default_factory=lambda: int(_env("SMD_MQTT_PORT", "1883")))
          mqtt_user: str = field(default_factory=lambda: _env("SMD_MQTT_USER", ""))
          mqtt_password: str = field(default_factory=lambda: _env("SMD_MQTT_PASSWORD", ""))
          mqtt_keepalive: int = field(
              default_factory=lambda: int(_env("SMD_MQTT_KEEPALIVE", "60"))
          )
          mqtt_client_id: str = field(
              default_factory=lambda: _env(
                  "SMD_MQTT_CLIENT_ID", f"mqtt-duck-{os.urandom(4).hex()}"
              )
          )

          # ---- Writer thread tuning ----
          # Low expected throughput -> monthly Parquet files, relaxed flush cadence.
          # The interval is the *normal* case: batch a few minutes of samples into
          # one merge. ``flush_max_samples`` is only a safety cap that forces an
          # earlier flush should throughput ever spike, bounding the writer's RAM.
          flush_interval_s: float = field(
              default_factory=lambda: float(_env("SMD_FLUSH_INTERVAL_S", "30"))
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
          # Series-discovery endpoint: used by the backfill to find out which
          # sensors VM actually holds data for, per configured metric -- this is
          # what lets the backfill run against a completely empty Hive.
          vm_series_path: str = field(
              default_factory=lambda: _env("SMD_VM_SERIES_PATH", "/api/v1/series")
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

          @property
          def vm_series_url(self) -> str:
              return f"{self.vm_scheme}://{self.vm_host}:{self.vm_port}{self.vm_series_path}"

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
```
/answer 1470-c allow
ReasoningToken: 233
Text:
 Jetzt implementiere ich das Flag: `smarthome_enabled` in `MqttConfig`, CLI-Argument `--smarthome` in `__main__.py`, und bedingte Aktivierung in `app.py`.
Control Request:
```yaml
id: 1470-d
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  old_text: |2-
        queue_max: int = field(default_factory=lambda: int(_env("SMD_QUEUE_MAX", "100000")))

        # ---- Subscriptions & metrics (mirrors smarthome.yaml) ----
  new_text: |2-
        queue_max: int = field(default_factory=lambda: int(_env("SMD_QUEUE_MAX", "100000")))

        # ---- SmartHome automation engine (opt-in via --smarthome / env; off on
        # the metrics-server-only deployment) ----
        smarthome_enabled: bool = field(
            default_factory=lambda: _env("SMD_SMARTHOME", "").lower()
            in ("1", "true", "yes")
        )

        # ---- Subscriptions & metrics (mirrors smarthome.yaml) ----
  reason: "smarthome_enabled Feld mit env-Default hinzufügen, damit die Aktivierung optional/steuerbar ist"
```
/answer 1470-d allow
Text:
 Nun das CLI-Argument in `__main__.py`:
Control Request:
```yaml
id: 1470-e
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/__main__.py
  old_text: |2-
        p.add_argument("--flush-interval", type=float, default=cfg.flush_interval_s)
        p.add_argument("--flush-max", type=int, default=cfg.flush_max_samples)
  new_text: |2-
        p.add_argument("--flush-interval", type=float, default=cfg.flush_interval_s)
        p.add_argument("--flush-max", type=int, default=cfg.flush_max_samples)
        # SmartHome automation engine (not needed on the metrics-server-only host)
        p.add_argument(
            "--smarthome",
            dest="smarthome",
            action="store_true",
            default=cfg.smarthome_enabled,
            help="Enable the SmartHome automation engine.",
        )
  reason: "CLI-Flag --smarthome ergänzen, das die Engine standardmäßig deaktiviert lässt"
```
/answer 1470-e allow
Control Request:
```yaml
id: 1470-f
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/__main__.py
  old_text: |2-
        cfg.flush_interval_s = args.flush_interval
        cfg.flush_max_samples = args.flush_max
  new_text: |2-
        cfg.flush_interval_s = args.flush_interval
        cfg.flush_max_samples = args.flush_max
        cfg.smarthome_enabled = args.smarthome
  reason: Geparstes --smarthome-Flag in die Config übernehmen
```
/answer 1470-f allow
Text:
 Jetzt `app.py` anpassen, sodass `SmartHomeEngine` nur bei aktivem Flag erzeugt/gestartet/gestoppt/geroutet wird:
Control Request:
```yaml
id: 1470-10
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  old_text: |2-
            # SmartHome automation: own MQTT client, same broker + credentials.
            self.smarthome = SmartHomeEngine(SmartHomeConfig.from_mqtt(cfg))

        # -- routing: intercept SmartHome API, else inherited surface -------
        def handle_get(self, handler) -> None:
            if sh_web.handle_get(self, self.smarthome, handler):
                return
            super().handle_get(handler)

        def handle_post(self, handler) -> None:
            if sh_web.handle_post(self, self.smarthome, handler):
                return
            super().handle_post(handler)
  new_text: |2-
            # SmartHome automation: own MQTT client, same broker + credentials.
            # Opt-in only (--smarthome) -- the metrics server doesn't need it.
            self.smarthome = (
                SmartHomeEngine(SmartHomeConfig.from_mqtt(cfg))
                if cfg.smarthome_enabled
                else None
            )

        # -- routing: intercept SmartHome API, else inherited surface -------
        def handle_get(self, handler) -> None:
            if self.smarthome and sh_web.handle_get(self, self.smarthome, handler):
                return
            super().handle_get(handler)

        def handle_post(self, handler) -> None:
            if self.smarthome and sh_web.handle_post(self, self.smarthome, handler):
                return
            super().handle_post(handler)
  reason: SmartHomeEngine nur bei aktivem Flag instanziieren; Routing entsprechend absichern
```
/answer 1470-10 allow
Control Request:
```yaml
id: 1470-11
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  old_text: |2-
            self.writer.start()
            self.mqtt.start()
            self.smarthome.start()
  new_text: |2-
            self.writer.start()
            self.mqtt.start()
            if self.smarthome:
                self.smarthome.start()
  reason: "Engine nur starten, wenn aktiviert"
```
/answer 1470-11 allow
Control Request:
```yaml
id: 1470-12
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  old_text: |2-
            self.smarthome.stop()
            # Stop the source first so no new samples race the final flush.
  new_text: |2-
            if self.smarthome:
                self.smarthome.stop()
            # Stop the source first so no new samples race the final flush.
  reason: "Engine nur stoppen, wenn aktiviert"
```
/answer 1470-12 allow
Control Request:
```yaml
id: 1470-13
toolName: python-ast-validate
arguments:
  paths:
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/__main__.py
  reason: Syntaxprüfung der geänderten Dateien
```
/answer 1470-13 allow
Text:
 Nun validieren:
Alle drei Dateien sind syntaktisch valide.

Zusammenfassung der Änderungen:

- **`smarthome/config.py`** – neues Feld `MqttConfig.smarthome_enabled` (Default `False`, per `SMD_SMARTHOME`-Env überschreibbar).
- **`mqttduck/__main__.py`** – neues CLI-Argument `--smarthome` (store_true), das `cfg.smarthome_enabled` setzt.
- **`mqttduck/app.py`** – `SmartHomeEngine` wird nur noch instanziiert, gestartet, gestoppt und ins Routing eingebunden, wenn `cfg.smarthome_enabled` gesetzt ist (`self.smarthome` ist sonst `None`).

Ohne `--smarthome` bleibt die SmartHome-Engine komplett inaktiv – für den Metrikserver ändert sich damit nichts am Verhalten, solange das Flag dort nicht gesetzt wird.
