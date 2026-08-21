Ich möchte Iobroker durch eine schlankere und eigene Implementierung ersetzen. Implementiere Folgendes.

Die Lösung kann innerhalb von mqtt duck laufen. Die statics werden von dort über den existierenden Mechanismus bereitgestellt. Die Lösung soll semantisch getrennten code erhalten (eigenes package) aber zentrale Komponenten sollen der Effizienz wegen mitbenutzt werden.

- Es soll eine eigene MQTT Client Instanz verwendet werden jedoch mit denselben Server credentials und host Einstellungen.
- mqtt duck `/home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck`
- Extrahiertes IO Broker blocky Setup: `/home/user/xyan/XY.Archiv/hrviewer/project/smarthome.xml`
- Statics: `/home/user/xyan/XY.Archiv/hrviewer/statics`
- blockly: `/home/user/xyan/XY.Archiv/hrviewer/statics/blockly`
- paho_mqtt ist verfügbar
- Zigbee2MQTT wird als Bridge verwendet und setzt die MQTT Kommandos um.

## Backend

Das Backend liefert eine Umgebung in der das Script sich für Timer und eingehende MQTT Zustandswechsel (trigger) registrieren kann. Darüber hinaus ist es in seinem Zugriff beschränkt.
Das Skript stellt für die Trigger Callbacks bereit die wiederum MQTT Kontrollkommandos senden können.
Die Funktionalität des exportierten IO Broker blocky Setup muss abgebildet werden.

Beispiel für zigbee2mqtt Steuerung
`mosquitto_pub -h localhost -t zigbee2mqtt/steckdose_1/set -m '{"state": "ON"}'`

Das Backend liefert einen Endpunkt über den die SmartHome Konfiguration in Blockly geladen und wieder gespeichert werden kann.
Es muss einerseits im nativen Format gespeichert werden für weiteres Editieren und andererseits muss in python gespeichert werden um die Konfiguration ausführen zu können.
Das Backend lädt ein vorhandenes Skript in eine gesicherte Umgebung und stellt Inputs (Trigger) sowie Outputs(MQTT) zur Verfügung.

## Frontend

Erstelle ein statisches Frontend auf Basis von blocky. Das von einem Endpunkt das Script im nativen Format laden soll und in der UI für das Editieren anzeigt. Ein speicher Button schickt das Script wieder zum Endpunkt wo es im nativen Format gespeichert wird und zusätzlich im Python Format gespeichert wird.

- Es gibt nur ein einziges Script, das Script braucht keinen Namen und stellt die gesamte SmartHome Konfiguration dar.
SystemInit:  id=bb8f503a-c1a0-45ce-bdfe-460fa37be744, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-opus-4-8
Text:
 Ich schaue mir zuerst die vorhandene Struktur an, um die zentralen Komponenten zu verstehen.
Control Request:
```yaml
id: 9d4dd6b9-5332-4ec8-8789-59b6d4f535ae
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck
  reason: Understand the existing mqttduck package structure to integrate the smarthome solution
```
/answer 9d4dd6b9-5332-4ec8-8789-59b6d4f535ae allow
Control Request:
```yaml
id: b94b445f-b27a-4f34-8874-c5d017bc1e24
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
/answer b94b445f-b27a-4f34-8874-c5d017bc1e24 allow
Control Request:
```yaml
id: 37985014-c57e-421b-9a09-f52dd9ec8478
toolName: file-stats
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/project/smarthome.xml
  reason: Assess size/complexity of the IO Broker blockly export to plan mapping
```
/answer 37985014-c57e-421b-9a09-f52dd9ec8478 allow
Control Request:
```yaml
id: f9d393f4-f118-48ec-8c4d-92e3878082e3
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics
  reason: See existing statics layout including blockly to plan frontend
```
/answer f9d393f4-f118-48ec-8c4d-92e3878082e3 allow
Control Request:
```yaml
id: c56f7edb-1b75-4c41-b318-1b665927d6ed
result:
  structuredContent:
    entries:
    - Arrow.es2015.min.js
    - app.js
    - blockly/blockly_compressed.js
    - blockly/blocks_compressed.js
    - blockly/de.js
    - blockly/javascript_compressed.js
    - dashboard.config.heating.js
    - dashboard.config.js
    - dashboard.css
    - dashboard.html
    - dashboard.js
    - dashboard/charts.common.js
    - dashboard/charts.daily.js
    - dashboard/charts.stateband.js
    - dashboard/charts.timeseries.js
    - dashboard/controls.js
    - dashboard/data.js
    - dashboard/layout.js
    - dashboard/panel.js
    - dashboard/panels.flags.js
    - dashboard/time.js
    - echarts.min.js
    - index.html
    - style.css
    - xyou_chai_16.png
    - xyou_chai_32.png
    - xyou_chai_64.png
    - xyou_chai_orig.png
```
/answer c56f7edb-1b75-4c41-b318-1b665927d6ed allow
ReasoningToken: 26
Control Request:
```yaml
id: 41be2419-21b3-453d-8db5-364dbd4acad7
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  reason: Understand app/server wiring to add smarthome endpoints and reuse mechanisms
```
/answer 41be2419-21b3-453d-8db5-364dbd4acad7 allow
Control Request:
```yaml
id: 09570464-483e-44fa-b051-d5af8453a586
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/client.py
  reason: Understand existing MQTT client to create a separate instance with same credentials
```
/answer 09570464-483e-44fa-b051-d5af8453a586 allow
Control Request:
```yaml
id: 1c2dff38-f656-42db-9648-9e06bab21ba0
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/config.py
  reason: Understand config for MQTT credentials/host reuse
```
/answer 1c2dff38-f656-42db-9648-9e06bab21ba0 allow
Control Request:
```yaml
id: 5e3b4484-6be4-4d86-a5d4-4b4f493fcd89
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/__main__.py
  reason: Understand entrypoint wiring
```
/answer 5e3b4484-6be4-4d86-a5d4-4b4f493fcd89 allow
ReasoningToken: 50
Text:
 Jetzt schaue ich mir die Basis-HrViewer-App an, um zu verstehen, wie HTTP-Routen und Statics bereitgestellt werden.
Control Request:
```yaml
id: 1183f260-19fb-46dc-a146-9c736c5d34bd
toolName: bash
arguments:
  script: find /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv -type f | head -50
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Locate the base HrViewer app/server/config modules to learn HTTP routing and statics serving
```
/answer 1183f260-19fb-46dc-a146-9c736c5d34bd allow
Control Request:
```yaml
id: acf8407f-0da1-4fad-91a9-0c43ee24b778
result:
  structuredContent:
    stdout: |
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/__pycache__/__init__.cpython-312.pyc
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/__init__.py
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/__pycache__/fpstore.cpython-312.pyc
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/__pycache__/app.cpython-312.pyc
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/__pycache__/store.cpython-312.pyc
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/__pycache__/arrow_ipc.cpython-312.pyc
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/__pycache__/__init__.cpython-312.pyc
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/__pycache__/config.cpython-312.pyc
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/config.py
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/app.py
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/store.py
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/__init__.py
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/fpstore.py
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/db.py
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/__main__.py
      /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/arrow_ipc.py
```
/answer acf8407f-0da1-4fad-91a9-0c43ee24b778 allow
Control Request:
```yaml
id: 4df1a3c1-4f16-4a13-9036-c3df0bbd62d6
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/project/smarthome.xml
  reason: Read the full IO Broker blockly export to map its functionality
```
/answer 4df1a3c1-4f16-4a13-9036-c3df0bbd62d6 allow
ReasoningToken: 49
Text:
 Jetzt schaue ich mir die Basis-App an, um Routing und Statics-Handling zu verstehen.
Control Request:
```yaml
id: ae258e01-07cd-4498-b90d-c4d6a7b782d7
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/app.py
  reason: "Learn how HTTP routes, statics dir, on_start/on_stop and /api are implemented to hook smarthome endpoints in"
```
/answer ae258e01-07cd-4498-b90d-c4d6a7b782d7 allow
Control Request:
```yaml
id: 2c871be0-f86e-4c05-8979-7e204b6db219
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/hrv/viewer/config.py
  reason: Understand base Config for statics dir and host/port to reuse
```
/answer 2c871be0-f86e-4c05-8979-7e204b6db219 allow
ReasoningToken: 1155
Text:
 Ich prüfe noch die Projekt-Konfiguration (Packaging) und wie Statics eingebunden werden.
Control Request:
```yaml
id: 3e11e9f8-dc13-4f1e-b2c5-17388cb1137c
toolName: bash
arguments:
  script: cd /home/user/xyan/XY.Archiv/hrviewer; ls; echo "---PYPROJECT---"; cat pyproject.toml 2>/dev/null | head -60; echo "---statics index head---"; head -40 statics/index.html; echo "---project dir---"; ls -la project; echo "---blockly files sizes---"; ls -la statics/blockly
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: "Check packaging config, existing static HTML conventions, project dir and blockly assets to align new code"
```
/answer 3e11e9f8-dc13-4f1e-b2c5-17388cb1137c allow
Control Request:
```yaml
id: 7d0d2219-4e21-4c4c-a059-7d33b1ff5070
result:
  content:
  - type: text
    text: "Full output written to file (3151 characters). Before loading the file, reduce the content to what is strictly needed: use targeted commands (grep, head, tail, awk) to extract only the relevant parts.Only load the file with `file-read` once the output is already narrowed down to the essential information."
  structuredContent:
    stdout_file: /tmp/mcpc-stdout-012e0imi.log
```
/answer 7d0d2219-4e21-4c4c-a059-7d33b1ff5070 allow
ReasoningToken: 8208
Control Request:
```yaml
id: 5829ea3b-4934-4b40-b4e0-044d9bf072fe
toolName: read-file
arguments:
  path: /tmp/mcpc-stdout-012e0imi.log
  reason: Read captured output about packaging and statics
```
/answer 5829ea3b-4934-4b40-b4e0-044d9bf072fe allow
Text:
 Es gibt eine `blockly.md` mit Dokumentation zu den Blöcken. Die lese ich, um die Blockdefinitionen exakt abzubilden.
Control Request:
```yaml
id: 9e4b6223-6ea0-4770-8595-75c0e4cc8147
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/project/blockly.md
  reason: Understand documented block semantics/fields to define custom blocks and compiler accurately
```
/answer 9e4b6223-6ea0-4770-8595-75c0e4cc8147 deny Das ist keine Dokumentation sondern der aktuelle Prompt
ReasoningToken: 68
Text:
 Ich habe jetzt ein vollständiges Bild. Ich lege das neue, semantisch getrennte Package `xy.smarthome` an (nutzt aber `MqttConfig`, die Basis-HTTP-/Statics-Mechanik und den Statics-Ordner mit). Ich beginne mit dem Backend.
Control Request:
```yaml
id: 7d7b99b1-badb-4289-83ec-24b6b7edee42
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/__init__.py
  mode: replace
  content: |
    """SmartHome: a lean, self-contained replacement for the IO-Broker Blockly
    automation, running *inside* MQTT-Duck.

    This package is deliberately kept semantically separate from the sensor
    ingestion side of MQTT-Duck. It reuses central pieces for efficiency -- the
    :class:`~xy.mqttduck.config.MqttConfig` (broker host + credentials), the
    HR-Viewer HTTP server surface and its statics mechanism -- but owns its own
    MQTT client instance, its own scheduler and its own restricted script runtime.

    The public surface is small:

    * :class:`~xy.smarthome.config.SmartHomeConfig` -- paths + broker settings.
    * :class:`~xy.smarthome.engine.SmartHomeEngine` -- lifecycle + wiring.
    * :func:`~xy.smarthome.compiler.compile_xml` -- Blockly XML -> Python source.
    * :func:`~xy.smarthome.web.handle_get` / :func:`~xy.smarthome.web.handle_post`
      -- the two HTTP endpoints (load/save the single script).
    """
    from __future__ import annotations

    from .config import SmartHomeConfig
    from .engine import SmartHomeEngine

    __all__ = ["SmartHomeConfig", "SmartHomeEngine"]
  reason: Create the new semantically separate smarthome package entry with public surface
```
/answer 7d7b99b1-badb-4289-83ec-24b6b7edee42 allow
ReasoningToken: 5130
Control Request:
```yaml
id: 13a52c75-9866-4c24-9dc8-bd63ef312932
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/config.py
  mode: replace
  content: |
    """Configuration for the SmartHome automation engine.

    Kept intentionally small: it only carries the two file locations (the single
    script in its *native* Blockly form and its *compiled* Python form) plus the
    MQTT broker coordinates. The broker coordinates default to being taken from an
    existing :class:`~xy.mqttduck.config.MqttConfig` instance so the SmartHome
    client connects to the *same* server with the *same* credentials -- only the
    client-id differs, because it is a distinct MQTT connection.
    """
    from __future__ import annotations

    import os
    from dataclasses import dataclass, field

    from xy.hrv.viewer.config import _env

    DEFAULT_NATIVE_PATH = "/home/user/xyan/XY.Archiv/hrviewer/project/smarthome.xml"
    DEFAULT_PY_PATH = "/home/user/xyan/XY.Archiv/hrviewer/project/smarthome_generated.py"


    @dataclass
    class SmartHomeConfig:
        """Runtime configuration for the SmartHome engine."""

        # ---- The single script, in both representations -------------------
        native_path: str = field(
            default_factory=lambda: _env("SMH_NATIVE_PATH", DEFAULT_NATIVE_PATH)
        )
        python_path: str = field(
            default_factory=lambda: _env("SMH_PY_PATH", DEFAULT_PY_PATH)
        )

        # ---- MQTT broker (own client, shared server + credentials) --------
        mqtt_host: str = field(default_factory=lambda: _env("SMD_MQTT_HOST", "127.0.0.1"))
        mqtt_port: int = field(default_factory=lambda: int(_env("SMD_MQTT_PORT", "1883")))
        mqtt_user: str = field(default_factory=lambda: _env("SMD_MQTT_USER", ""))
        mqtt_password: str = field(default_factory=lambda: _env("SMD_MQTT_PASSWORD", ""))
        mqtt_keepalive: int = field(
            default_factory=lambda: int(_env("SMD_MQTT_KEEPALIVE", "60"))
        )
        mqtt_client_id: str = field(
            default_factory=lambda: _env(
                "SMH_MQTT_CLIENT_ID", f"smarthome-{os.urandom(4).hex()}"
            )
        )

        # ---- zigbee2mqtt topic namespace ----------------------------------
        # OIDs look like ``zigbee2mqtt.0.<device>.<property>``; the first dotted
        # segment is the MQTT base topic namespace used for both the state topic
        # (``<ns>/<device>``) and the command topic (``<ns>/<device>/set``).
        base_topic: str = field(default_factory=lambda: _env("SMH_BASE_TOPIC", "zigbee2mqtt"))

        @classmethod
        def from_mqtt(cls, mqtt_cfg) -> "SmartHomeConfig":
            """Derive a SmartHome config from an existing MqttConfig, so the
            SmartHome client reuses the same broker host + credentials."""
            cfg = cls()
            cfg.mqtt_host = mqtt_cfg.mqtt_host
            cfg.mqtt_port = mqtt_cfg.mqtt_port
            cfg.mqtt_user = mqtt_cfg.mqtt_user
            cfg.mqtt_password = mqtt_cfg.mqtt_password
            cfg.mqtt_keepalive = mqtt_cfg.mqtt_keepalive
            return cfg
  reason: Add SmartHomeConfig that reuses MqttConfig broker credentials but a distinct client id
```
/answer 13a52c75-9866-4c24-9dc8-bd63ef312932 allow
Control Request:
```yaml
id: b8b3fa2f-606a-41df-bd4a-cfa743d1f53c
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/cron.py
  mode: replace
  content: |
    """A tiny, dependency-free 5-field cron matcher.

    Supports the subset needed by the SmartHome schedules (and a bit more):
    ``*``, single values, comma lists, ``a-b`` ranges and ``*/n`` / ``a-b/n``
    steps, across the five standard fields::

        minute hour day-of-month month day-of-week
         0-59   0-23    1-31       1-12      0-6   (0 or 7 == Sunday)

    Only minute-resolution matching is needed; the scheduler ticks once per
    minute and asks :func:`matches` whether a given local ``datetime`` is due.
    """
    from __future__ import annotations

    from datetime import datetime

    _RANGES = {
        "minute": (0, 59),
        "hour": (0, 23),
        "dom": (1, 31),
        "month": (1, 12),
        "dow": (0, 6),
    }


    def _parse_field(spec: str, lo: int, hi: int) -> set[int]:
        values: set[int] = set()
        for part in spec.split(","):
            part = part.strip()
            step = 1
            if "/" in part:
                base, step_s = part.split("/", 1)
                step = int(step_s)
            else:
                base = part
            if base == "*" or base == "":
                start, end = lo, hi
            elif "-" in base:
                a, b = base.split("-", 1)
                start, end = int(a), int(b)
            else:
                start = end = int(base)
            for v in range(start, end + 1, step):
                values.add(v)
        return values


    class CronSpec:
        """A parsed cron expression, ready to be matched against datetimes."""

        def __init__(self, expr: str):
            self.expr = expr.strip()
            fields = self.expr.split()
            if len(fields) != 5:
                raise ValueError(f"cron must have 5 fields, got {len(fields)}: {expr!r}")
            self.minute = _parse_field(fields[0], *_RANGES["minute"])
            self.hour = _parse_field(fields[1], *_RANGES["hour"])
            self.dom = _parse_field(fields[2], *_RANGES["dom"])
            self.month = _parse_field(fields[3], *_RANGES["month"])
            # day-of-week: normalise a lone 7 to 0 (Sunday)
            self.dow = {d % 7 for d in _parse_field(fields[4], 0, 7)}
            self._dom_restricted = fields[2].strip() != "*"
            self._dow_restricted = fields[4].strip() != "*"

        def matches(self, now: datetime) -> bool:
            if now.minute not in self.minute:
                return False
            if now.hour not in self.hour:
                return False
            if now.month not in self.month:
                return False
            # Standard cron OR-semantics between DOM and DOW when both restricted.
            dom_ok = now.day in self.dom
            dow_ok = (now.weekday() + 1) % 7 in self.dow  # Python Mon=0 -> cron Sun=0
            if self._dom_restricted and self._dow_restricted:
                return dom_ok or dow_ok
            return dom_ok and dow_ok
  reason: Add a minimal cron matcher for schedule blocks
```
/answer b8b3fa2f-606a-41df-bd4a-cfa743d1f53c allow
ReasoningToken: 9
Control Request:
```yaml
id: 455ed077-a4aa-4028-b805-8ec52f9ce46c
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/compiler.py
  mode: replace
  content: |
    """Blockly XML -> executable Python compiler.

    Turns the *native* Blockly representation (as produced by the frontend and by
    the extracted IO-Broker export) into a single ``register(sh)`` function. All
    device access, timers and triggers go exclusively through the injected ``sh``
    facade (see :mod:`xy.smarthome.runtime`), which is how the executed script is
    sandboxed: the generated code never imports anything and only ever calls
    methods on ``sh``.

    Supported block types (everything present in the export, plus a few common
    siblings for robustness):

    Statements
        ``comment`` ``schedule`` ``on`` ``procedures_defnoreturn``
        ``procedures_callnoreturn`` ``debug`` ``control`` ``controls_if``
        ``timeouts_settimeout`` ``timeouts_cleartimeout``
    Values
        ``logic_boolean`` ``logic_compare`` ``logic_operation`` ``logic_negate``
        ``math_number`` ``math_arithmetic`` ``text`` ``time_get`` ``get_value``
    """
    from __future__ import annotations

    import re
    import xml.etree.ElementTree as ET

    _CMP_OP = {"EQ": "==", "NEQ": "!=", "LT": "<", "LTE": "<=", "GT": ">", "GTE": ">="}
    _BOOL_OP = {"AND": "and", "OR": "or"}
    _ARITH_OP = {"ADD": "+", "MINUS": "-", "MULTIPLY": "*", "DIVIDE": "/", "POWER": "**"}
    _UNIT_SECONDS = {"ms": 0.001, "s": 1, "sec": 1, "min": 60, "h": 3600, "hour": 3600}


    def _tag(elem: ET.Element) -> str:
        return elem.tag.split("}", 1)[-1]


    def _children(elem: ET.Element, name: str) -> list[ET.Element]:
        return [c for c in elem if _tag(c) == name]


    def _first_inner_block(container: ET.Element) -> ET.Element | None:
        """First <block> (preferred) or <shadow> directly inside *container*."""
        blocks = _children(container, "block")
        if blocks:
            return blocks[0]
        shadows = _children(container, "shadow")
        return shadows[0] if shadows else None


    class Compiler:
        def __init__(self) -> None:
            self._counter = 0
            self._proc_names: dict[str, str] = {}

        # -- public --------------------------------------------------------
        def compile(self, xml_text: str) -> str:
            root = ET.fromstring(xml_text)
            tops = _children(root, "block")
            body: list[str] = []
            for b in tops:
                body += self._statements(b)
            if not body:
                body = ["pass"]
            header = [
                "# Auto-generated from the native Blockly script -- DO NOT EDIT.",
                "# Every device/timer/trigger access goes through the sandbox `sh`.",
                "",
                "def register(sh):",
            ]
            return "\n".join(header + ["    " + line for line in body]) + "\n"

        # -- naming helpers ------------------------------------------------
        def _uid(self, prefix: str) -> str:
            self._counter += 1
            return f"_{prefix}_{self._counter}"

        def _proc_name(self, raw: str) -> str:
            if raw not in self._proc_names:
                clean = re.sub(r"\W", "_", raw or "")
                if not clean or clean[0].isdigit():
                    clean = "proc_" + clean
                # avoid collisions
                base, n = clean, 1
                while clean in self._proc_names.values():
                    clean = f"{base}_{n}"
                    n += 1
                self._proc_names[raw] = clean
            return self._proc_names[raw]

        # -- element accessors ---------------------------------------------
        @staticmethod
        def _field(block: ET.Element, name: str) -> str | None:
            for f in _children(block, "field"):
                if f.get("name") == name:
                    return f.text if f.text is not None else ""
            return None

        @staticmethod
        def _mutation(block: ET.Element) -> ET.Element | None:
            muts = _children(block, "mutation")
            return muts[0] if muts else None

        def _value_block(self, block: ET.Element, name: str) -> ET.Element | None:
            for v in _children(block, "value"):
                if v.get("name") == name:
                    return _first_inner_block(v)
            return None

        def _statement_block(self, block: ET.Element, name: str) -> ET.Element | None:
            for s in _children(block, "statement"):
                if s.get("name") == name:
                    return _first_inner_block(s)
            return None

        def _next_block(self, block: ET.Element) -> ET.Element | None:
            nx = _children(block, "next")
            if not nx:
                return None
            return _first_inner_block(nx[0])

        # -- statement generation ------------------------------------------
        def _statements(self, first: ET.Element | None) -> list[str]:
            lines: list[str] = []
            b = first
            while b is not None:
                lines += self._stmt(b)
                b = self._next_block(b)
            return lines

        @staticmethod
        def _indent(lines: list[str]) -> list[str]:
            return ["    " + line for line in lines]

        def _body(self, block: ET.Element, statement_name: str) -> list[str]:
            return self._statements(self._statement_block(block, statement_name)) or ["pass"]

        def _stmt(self, b: ET.Element) -> list[str]:
            t = _tag(b)
            handler = getattr(self, f"_stmt_{t}", None)
            if handler is None:
                return [f"# unsupported block: {t}"]
            return handler(b)

        def _stmt_comment(self, b: ET.Element) -> list[str]:
            text = (self._field(b, "COMMENT") or "").replace("\n", " ")
            return [f"# {text}"]

        def _stmt_schedule(self, b: ET.Element) -> list[str]:
            cron = self._field(b, "SCHEDULE") or "* * * * *"
            name = self._uid("sched")
            body = self._body(b, "STATEMENT")
            return [f"def {name}():"] + self._indent(body) + [f"sh.schedule({cron!r}, {name})"]

        def _stmt_on(self, b: ET.Element) -> list[str]:
            oid = self._field(b, "OID") or ""
            cond = self._field(b, "CONDITION") or "true"
            name = self._uid("on")
            body = self._body(b, "STATEMENT")
            return [f"def {name}():"] + self._indent(body) + [
                f"sh.on({oid!r}, {cond!r}, {name})"
            ]

        def _stmt_procedures_defnoreturn(self, b: ET.Element) -> list[str]:
            pname = self._proc_name(self._field(b, "NAME") or "proc")
            body = self._body(b, "STACK")
            return [f"def {pname}():"] + self._indent(body)

        def _stmt_procedures_callnoreturn(self, b: ET.Element) -> list[str]:
            mut = self._mutation(b)
            raw = mut.get("name") if mut is not None else "proc"
            return [f"{self._proc_name(raw or 'proc')}()"]

        def _stmt_debug(self, b: ET.Element) -> list[str]:
            sev = self._field(b, "Severity") or "info"
            text = self._expr(self._value_block(b, "TEXT"))
            return [f"sh.debug({text}, {sev!r})"]

        def _stmt_control(self, b: ET.Element) -> list[str]:
            oid = self._field(b, "OID") or ""
            value = self._expr(self._value_block(b, "VALUE"))
            return [f"sh.control({oid!r}, {value})"]

        def _stmt_controls_if(self, b: ET.Element) -> list[str]:
            mut = self._mutation(b)
            elseif = int(mut.get("elseif", 0)) if mut is not None else 0
            has_else = int(mut.get("else", 0)) if mut is not None else 0
            lines: list[str] = []
            cond0 = self._expr(self._value_block(b, "IF0"))
            lines += [f"if {cond0}:"] + self._indent(self._body(b, "DO0"))
            for i in range(1, elseif + 1):
                c = self._expr(self._value_block(b, f"IF{i}"))
                lines += [f"elif {c}:"] + self._indent(self._body(b, f"DO{i}"))
            if has_else:
                lines += ["else:"] + self._indent(self._body(b, "ELSE"))
            return lines

        def _stmt_timeouts_settimeout(self, b: ET.Element) -> list[str]:
            name = self._field(b, "NAME") or "timeout"
            delay = self._field(b, "DELAY") or "0"
            unit = self._field(b, "UNIT") or "ms"
            seconds = self._to_seconds(delay, unit)
            fname = self._uid("timeout")
            body = self._body(b, "STATEMENT")
            return [f"def {fname}():"] + self._indent(body) + [
                f"sh.set_timeout({name!r}, {seconds}, {fname})"
            ]

        def _stmt_timeouts_cleartimeout(self, b: ET.Element) -> list[str]:
            name = self._field(b, "NAME") or "timeout"
            return [f"sh.clear_timeout({name!r})"]

        @staticmethod
        def _to_seconds(delay: str, unit: str) -> float | int:
            try:
                n = float(delay)
            except ValueError:
                n = 0.0
            secs = n * _UNIT_SECONDS.get(unit, 0.001)
            return int(secs) if secs == int(secs) else secs

        # -- value generation ----------------------------------------------
        def _expr(self, b: ET.Element | None) -> str:
            if b is None:
                return "None"
            t = _tag(b)
            handler = getattr(self, f"_expr_{t}", None)
            if handler is None:
                return "None"
            return handler(b)

        def _expr_logic_boolean(self, b: ET.Element) -> str:
            return "True" if (self._field(b, "BOOL") or "FALSE") == "TRUE" else "False"

        def _expr_logic_negate(self, b: ET.Element) -> str:
            return f"(not {self._expr(self._value_block(b, 'BOOL'))})"

        def _expr_math_number(self, b: ET.Element) -> str:
            raw = self._field(b, "NUM") or "0"
            try:
                float(raw)
                return raw
            except ValueError:
                return repr(raw)

        def _expr_math_arithmetic(self, b: ET.Element) -> str:
            op = _ARITH_OP.get(self._field(b, "OP") or "ADD", "+")
            a = self._expr(self._value_block(b, "A"))
            b_ = self._expr(self._value_block(b, "B"))
            return f"({a} {op} {b_})"

        def _expr_text(self, b: ET.Element) -> str:
            return repr(self._field(b, "TEXT") or "")

        def _expr_logic_compare(self, b: ET.Element) -> str:
            op = _CMP_OP.get(self._field(b, "OP") or "EQ", "==")
            a = self._expr(self._value_block(b, "A"))
            b_ = self._expr(self._value_block(b, "B"))
            return f"({a} {op} {b_})"

        def _expr_logic_operation(self, b: ET.Element) -> str:
            op = _BOOL_OP.get(self._field(b, "OP") or "AND", "and")
            a = self._expr(self._value_block(b, "A"))
            b_ = self._expr(self._value_block(b, "B"))
            return f"({a} {op} {b_})"

        def _expr_time_get(self, b: ET.Element) -> str:
            option = self._field(b, "OPTION") or "wd"
            return f"sh.time({option!r})"

        def _expr_get_value(self, b: ET.Element) -> str:
            attr = self._field(b, "ATTR") or "val"
            oid = self._field(b, "OID") or ""
            return f"sh.get_value({oid!r}, {attr!r})"


    def compile_xml(xml_text: str) -> str:
        """Compile a native Blockly XML string into Python source code."""
        return Compiler().compile(xml_text)
  reason: Add the XML->Python compiler covering all block types in the export
```
/answer 455ed077-a4aa-4028-b805-8ec52f9ce46c deny Moment, blockly unterstützt doch direkt einen python export?
Control Request:
```yaml
id: 49f0ef4c-866a-49d6-95f4-6c0fd992cdea
toolName: bash
arguments:
  script: |-
    cd /home/user/xyan/XY.Archiv/hrviewer/statics/blockly
    echo "=== version markers ==="
    grep -oE "Blockly.VERSION[^;]{0,40}" blockly_compressed.js | head
    head -c 400 blockly_compressed.js; echo
    echo "=== javascript gen header ==="
    head -c 400 javascript_compressed.js; echo
    echo "=== net check ==="
    (command -v curl >/dev/null && echo curl-ok) || echo no-curl
    (command -v npm >/dev/null && echo npm-ok) || echo no-npm
    pip show blockly 2>/dev/null | head -3 || echo no-pip-blockly
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics/blockly
  reason: Determine Blockly version and available means to fetch the matching python_compressed.js generator
```
/answer 49f0ef4c-866a-49d6-95f4-6c0fd992cdea allow
Control Request:
```yaml
id: 1fa5e15d-57d7-430e-8760-8cdd15a4dba3
result:
  structuredContent:
    stdout: |
      === version markers ===
      // Do not edit this file; automatically generated.

      /* eslint-disable */
      ;(function(root, factory) {
        if (typeof define === 'function' && define.amd) { // AMD
          define([], factory);
        } else if (typeof exports === 'object') { // Node.js
          module.exports = factory();
        } else { // Script
          root.Blockly = factory();
        }
      }(this, function() {
      var $={};
      var ca,aa,ea,fa,da,k,ja,ka,la,na,oa,pa,qa,
      === javascript gen header ===
      // Do not edit this file; automatically generated.

      /* eslint-disable */
      ;(function(root, factory) {
        if (typeof define === 'function' && define.amd) { // AMD
          define(["./blockly_compressed.js"], factory);
        } else if (typeof exports === 'object') { // Node.js
          module.exports = factory(require("./blockly_compressed.js"));
        } else { // Script
          root.javascript = factory(root.Blockly);

      === net check ===
      curl-ok
      npm-ok
```
/answer 1fa5e15d-57d7-430e-8760-8cdd15a4dba3 allow
Control Request:
```yaml
id: ab072b87-5bb4-4cf7-af30-93e89214463e
toolName: bash
arguments:
  script: |-
    cd /home/user/xyan/XY.Archiv/hrviewer/statics/blockly
    echo "=== search version tokens ==="
    grep -oaE "VERSION=\"[0-9]+\.[0-9]+\.[0-9]+\"" blockly_compressed.js | head
    grep -oaE "[0-9]+\.[0-9]+\.[0-9]+" blockly_compressed.js | sort | uniq -c | sort -rn | head
    echo "=== try CDN reach ==="
    curl -sI --max-time 8 https://unpkg.com/blockly/python_compressed.js | head -5 || echo "no-net"
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics/blockly
  reason: Identify Blockly version and internet reachability to fetch the matching python generator bundle
```
/answer ab072b87-5bb4-4cf7-af30-93e89214463e deny ich habe python_compressed.js heruntergeladen und im ordner abgelegt
Control Request:
```yaml
id: ff7ea91c-b586-4314-b439-3b62b0533c68
toolName: bash
arguments:
  script: |-
    cd /home/user/xyan/XY.Archiv/hrviewer/statics/blockly
    ls -la
    echo "=== python gen header ==="
    head -c 500 python_compressed.js; echo
    echo "=== global name exported ==="
    grep -oaE "root\.[A-Za-z]+ = factory" python_compressed.js | head
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics/blockly
  reason: Verify the placed python_compressed.js and how its global (pythonGenerator) is exposed
```
/answer ff7ea91c-b586-4314-b439-3b62b0533c68 allow
Control Request:
```yaml
id: a9c5c7cf-208f-4489-98e0-ffd21e6db5a6
result:
  structuredContent:
    stdout: |
      total 812
      drwxrwxr-x 2 user user   4096 Aug 20 22:52 .
      drwxrwxr-x 4 user user   4096 Aug 20 21:47 ..
      -rw-rw-r-- 1 user user 634050 Aug 14 17:35 blockly_compressed.js
      -rw-rw-r-- 1 user user  71578 Aug 14 17:35 blocks_compressed.js
      -rw-rw-r-- 1 user user  54705 Aug 14 17:35 de.js
      -rw-rw-r-- 1 user user  28588 Aug 14 17:35 javascript_compressed.js
      -rw-rw-r-- 1 user user  27777 Aug 20 22:52 python_compressed.js
      === python gen header ===
      // Do not edit this file; automatically generated.

      /* eslint-disable */
      ;(function(root, factory) {
        if (typeof define === 'function' && define.amd) { // AMD
          define(["./blockly_compressed.js"], factory);
        } else if (typeof exports === 'object') { // Node.js
          module.exports = factory(require("./blockly_compressed.js"));
        } else { // Script
          root.python = factory(root.Blockly);
          root.Blockly.Python = root.python.pythonGenerator;
        }
      }(this, function(__parent__) {
      var $=__parent__.
      === global name exported ===
      root.python = factory
```
/answer a9c5c7cf-208f-4489-98e0-ffd21e6db5a6 allow
Control Request:
```yaml
id: 147bf4d4-9ce6-43fb-b37c-33928970faba
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome
  reason: Confirm which backend files exist so I keep the package consistent (no leftover compiler)
```
/answer 147bf4d4-9ce6-43fb-b37c-33928970faba allow
Control Request:
```yaml
id: e3ba0c45-41f1-48de-b13c-90cea7feaafc
result:
  structuredContent:
    entries:
    - __init__.py
    - config.py
    - cron.py
```
/answer e3ba0c45-41f1-48de-b13c-90cea7feaafc allow
ReasoningToken: 11
Text:
 Guter Punkt — Blockly hat tatsächlich einen eingebauten Python-Generator (`pythonGenerator`). Dann sollte ich keinen eigenen XML→Python-Compiler im Backend schreiben, sondern Blocklys Python-Export nutzen: Das Frontend generiert Python (mit Custom-Generatoren nur für die IO-Broker-Blöcke) und schickt XML **und** Python an den Endpunkt; das Backend speichert beides und führt das Python nur noch in der Sandbox aus.

Dafür brauche ich `python_compressed.js` (liegt noch nicht in den Statics). Ich lösche den Backend-Compiler und prüfe, ob ich den passenden Python-Generator beschaffen kann.
ReasoningToken: 1707
ReasoningToken: 51
Text:
 Perfekt, danke. Ich prüfe die Datei und fahre mit dem Blockly-Python-Export-Ansatz fort.
ReasoningToken: 39
Text:
 Der Backend-Compiler wurde nicht angelegt (der Write wurde abgelehnt) — gut, den brauche ich nicht mehr. Ich verifiziere kurz und passe die Package-Doku an.
ReasoningToken: 144
Text:
 Ich passe die Package-Doku an (kein Backend-Compiler mehr) und schreibe die Runtime/Engine.
Control Request:
```yaml
id: 8dbb4d47-e1fa-4562-badb-90524a8928fc
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/__init__.py
  old_text: |-
    The public surface is small:

    * :class:`~xy.smarthome.config.SmartHomeConfig` -- paths + broker settings.
    * :class:`~xy.smarthome.engine.SmartHomeEngine` -- lifecycle + wiring.
    * :func:`~xy.smarthome.compiler.compile_xml` -- Blockly XML -> Python source.
    * :func:`~xy.smarthome.web.handle_get` / :func:`~xy.smarthome.web.handle_post`
      -- the two HTTP endpoints (load/save the single script).
    """
  new_text: |-
    The Python form is *not* produced here: it is exported directly by Blockly's
    built-in ``pythonGenerator`` in the frontend (with custom generators for the
    IO-Broker blocks) and sent to the save endpoint alongside the native XML. The
    backend only persists both forms and executes the Python in a restricted
    sandbox.

    The public surface is small:

    * :class:`~xy.smarthome.config.SmartHomeConfig` -- paths + broker settings.
    * :class:`~xy.smarthome.engine.SmartHomeEngine` -- lifecycle + wiring +
      the restricted script runtime (the ``sh`` facade).
    * :func:`~xy.smarthome.web.handle_get` / :func:`~xy.smarthome.web.handle_post`
      -- the two HTTP endpoints (load/save the single script).
    """
  reason: Reflect the Blockly-python-export approach instead of a backend compiler
```
/answer 8dbb4d47-e1fa-4562-badb-90524a8928fc deny Bitte die Kommentare so kompakt wie möglich nur für Aspekte die nicht oder nicht einfach direkt aus dem Code ersichtlich sind. Auf keinen Fall einfach direkt die anforderungen niederschreiben.
ReasoningToken: 6235
Text:
 Verstanden — Kommentare kompakt, nur Nicht-Offensichtliches, keine Anforderungen abschreiben. Ich überarbeite entsprechend.
Control Request:
```yaml
id: 5a194a46-6bf5-477a-ba3f-98f3100cbba2
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/__init__.py
  mode: replace
  content: |
    """SmartHome automation engine (runs inside MQTT-Duck, own MQTT client).

    Reuses ``MqttConfig`` broker credentials and the HR-Viewer HTTP/statics
    surface; keeps its own client, scheduler and restricted script runtime.
    """
    from __future__ import annotations

    from .config import SmartHomeConfig
    from .engine import SmartHomeEngine

    __all__ = ["SmartHomeConfig", "SmartHomeEngine"]
  reason: Make module docstring compact per user directive
```
/answer 5a194a46-6bf5-477a-ba3f-98f3100cbba2 allow
ReasoningToken: 84
Text:
 Ich mache die Docstrings in `config.py` und `cron.py` kompakter.
Control Request:
```yaml
id: 16c5bf10-f82b-484f-8676-4457b0b229d8
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/config.py
  old_text: |-
    """Configuration for the SmartHome automation engine.

    Kept intentionally small: it only carries the two file locations (the single
    script in its *native* Blockly form and its *compiled* Python form) plus the
    MQTT broker coordinates. The broker coordinates default to being taken from an
    existing :class:`~xy.mqttduck.config.MqttConfig` instance so the SmartHome
    client connects to the *same* server with the *same* credentials -- only the
    client-id differs, because it is a distinct MQTT connection.
    """
  new_text: |-
    """Paths of the single script (native XML + exported Python) and broker
    coordinates. Use :meth:`SmartHomeConfig.from_mqtt` to inherit the broker
    host/credentials from an existing ``MqttConfig`` (only the client-id differs).
    """
  reason: Compact docstring
```
/answer 16c5bf10-f82b-484f-8676-4457b0b229d8 allow
ReasoningToken: 62
Control Request:
```yaml
id: 5ac34b8a-d924-464b-bef3-e26729f2828a
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/config.py
  old_text: |2-
        # ---- The single script, in both representations -------------------
        native_path: str = field(
  new_text: "    native_path: str = field("
  reason: Remove redundant banner comment
```
/answer 5ac34b8a-d924-464b-bef3-e26729f2828a allow
Control Request:
```yaml
id: 90543bc2-1ff9-4920-b0c3-3307dd5737da
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/config.py
  old_text: |2-
        # ---- MQTT broker (own client, shared server + credentials) --------
        mqtt_host: str = field(default_factory=lambda: _env("SMD_MQTT_HOST", "127.0.0.1"))
  new_text: "    mqtt_host: str = field(default_factory=lambda: _env(\"SMD_MQTT_HOST\", \"127.0.0.1\"))"
  reason: Remove redundant banner comment
```
/answer 90543bc2-1ff9-4920-b0c3-3307dd5737da allow
Control Request:
```yaml
id: 91ee654f-ffe3-422e-acca-7713ea25476d
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/config.py
  old_text: |2-
        # ---- zigbee2mqtt topic namespace ----------------------------------
        # OIDs look like ``zigbee2mqtt.0.<device>.<property>``; the first dotted
        # segment is the MQTT base topic namespace used for both the state topic
        # (``<ns>/<device>``) and the command topic (``<ns>/<device>/set``).
        base_topic: str = field(default_factory=lambda: _env("SMH_BASE_TOPIC", "zigbee2mqtt"))

        @classmethod
        def from_mqtt(cls, mqtt_cfg) -> "SmartHomeConfig":
            """Derive a SmartHome config from an existing MqttConfig, so the
            SmartHome client reuses the same broker host + credentials."""
            cfg = cls()
  new_text: |2-
        # State topic ``<base>/<device>``, command topic ``<base>/<device>/set``.
        base_topic: str = field(default_factory=lambda: _env("SMH_BASE_TOPIC", "zigbee2mqtt"))

        @classmethod
        def from_mqtt(cls, mqtt_cfg) -> "SmartHomeConfig":
            cfg = cls()
  reason: Compact comments
```
/answer 91ee654f-ffe3-422e-acca-7713ea25476d allow
Text:
 Jetzt die Engine mit dem `sh`-Facade und dem restriktiven Runtime.
Control Request:
```yaml
id: de94c624-cf1f-493f-a56b-d5151a0d26bf
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/engine.py
  mode: replace
  content: |
    """SmartHome runtime: own MQTT client, cron scheduler, named timeouts and the
    restricted ``sh`` facade the exported Python script runs against.

    The script is plain Python (Blockly ``pythonGenerator`` output). It is exec'd
    with a curated ``__builtins__`` and a single injected global, ``sh`` -- an
    :class:`Facade`. All device I/O, timers and trigger registration are reachable
    only through that object, which is the whole sandbox.

    OID convention: ``<base>.<instance>.<device>.<property>`` (e.g.
    ``zigbee2mqtt.0.0xabc.state``). Only ``<device>``/``<property>`` matter; the
    MQTT topics are ``<base>/<device>`` (state) and ``<base>/<device>/set``
    (command). ``state`` maps bool<->``ON``/``OFF``; momentary button events arrive
    as ``{"action": "<property>"}`` and fire the trigger on every receipt.
    """
    from __future__ import annotations

    import json
    import threading
    import time
    import traceback
    from datetime import datetime

    import paho.mqtt.client as mqtt

    from .config import SmartHomeConfig
    from .cron import CronSpec

    # Builtins the exported script is allowed to see. No import/open/eval/etc.
    _SAFE_BUILTINS = {
        n: __builtins__[n] if isinstance(__builtins__, dict) else getattr(__builtins__, n)
        for n in ("abs", "min", "max", "round", "int", "float", "str", "bool", "len", "range")
    }


    def _truthy(v) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.strip().upper() in ("ON", "TRUE", "1", "YES")
        if isinstance(v, (int, float)):
            return v != 0
        return bool(v)


    def _normalize(v):
        if isinstance(v, str):
            u = v.upper()
            if u == "ON":
                return True
            if u == "OFF":
                return False
        return v


    class _Trigger:
        __slots__ = ("device", "prop", "cond", "cb")

        def __init__(self, device: str, prop: str, cond: str, cb):
            self.device, self.prop, self.cond, self.cb = device, prop, cond, cb


    class _Schedule:
        __slots__ = ("spec", "cb")

        def __init__(self, spec: CronSpec, cb):
            self.spec, self.cb = spec, cb


    class Facade:
        """The ``sh`` object exposed to the script -- the only capability surface."""

        def __init__(self, engine: "SmartHomeEngine"):
            self._e = engine

        # registration (called at script load time)
        def schedule(self, cron: str, cb) -> None:
            self._e._schedules.append(_Schedule(CronSpec(cron), cb))

        def on(self, oid: str, condition: str, cb) -> None:
            parsed = _parse_oid(oid)
            if parsed:
                device, prop = parsed
                self._e._triggers.append(_Trigger(device, prop, (condition or "true").lower(), cb))

        # actions (called at runtime)
        def control(self, oid: str, value) -> None:
            self._e.control(oid, value)

        def get_value(self, oid: str, attr: str = "val"):
            return self._e.get_value(oid, attr)

        def time(self, option: str):
            return self._e.time(option)

        def set_timeout(self, name: str, seconds: float, cb) -> None:
            self._e.set_timeout(name, seconds, cb)

        def clear_timeout(self, name: str) -> None:
            self._e.clear_timeout(name)

        def debug(self, text, severity: str = "info") -> None:
            print(f"[smarthome:{severity}] {text}", flush=True)


    def _parse_oid(oid: str):
        parts = (oid or "").split(".")
        if len(parts) < 4:
            return None
        return parts[2], ".".join(parts[3:])


    class SmartHomeEngine:
        def __init__(self, cfg: SmartHomeConfig):
            self.cfg = cfg
            self._facade = Facade(self)
            self._lock = threading.RLock()
            self._store: dict[tuple[str, str], object] = {}
            self._schedules: list[_Schedule] = []
            self._triggers: list[_Trigger] = []
            self._timeouts: dict[str, threading.Timer] = {}
            self._stop = threading.Event()
            self._sched_thread: threading.Thread | None = None
            self._script_error: str | None = None

            self._client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=cfg.mqtt_client_id,
                clean_session=True,
            )
            if cfg.mqtt_user:
                self._client.username_pw_set(cfg.mqtt_user, cfg.mqtt_password or None)
            self._client.on_connect = self._on_connect
            self._client.on_message = self._on_message

        # -- lifecycle -----------------------------------------------------
        def start(self) -> None:
            self.load()
            self._client.connect_async(
                self.cfg.mqtt_host, self.cfg.mqtt_port, self.cfg.mqtt_keepalive
            )
            self._client.loop_start()
            self._sched_thread = threading.Thread(
                target=self._scheduler_loop, name="smarthome-cron", daemon=True
            )
            self._sched_thread.start()
            print(
                f"[smarthome] engine up (mqtt://{self.cfg.mqtt_host}:{self.cfg.mqtt_port}, "
                f"schedules={len(self._schedules)}, triggers={len(self._triggers)})",
                flush=True,
            )

        def stop(self) -> None:
            self._stop.set()
            with self._lock:
                for t in self._timeouts.values():
                    t.cancel()
                self._timeouts.clear()
            try:
                self._client.loop_stop()
                self._client.disconnect()
            except Exception:
                pass

        # -- script (re)load -----------------------------------------------
        def load(self) -> None:
            """Exec the Python script, replacing all registrations atomically."""
            try:
                with open(self.cfg.python_path, "r", encoding="utf-8") as f:
                    source = f.read()
            except FileNotFoundError:
                source = ""
            self._exec_source(source)

        def _exec_source(self, source: str) -> None:
            sandbox = {"__builtins__": _SAFE_BUILTINS, "sh": self._facade}
            with self._lock:
                # drop old registrations + pending timers before re-registering
                for t in self._timeouts.values():
                    t.cancel()
                self._timeouts.clear()
                self._schedules = []
                self._triggers = []
                self._script_error = None
                if not source.strip():
                    return
                try:
                    code = compile(source, "<smarthome>", "exec")
                    exec(code, sandbox)  # noqa: S102 - curated builtins, generated code
                except Exception:
                    self._script_error = traceback.format_exc()
                    self._schedules = []
                    self._triggers = []
                    print(f"[smarthome] script error:\n{self._script_error}", flush=True)

        @property
        def script_error(self) -> str | None:
            return self._script_error

        # -- MQTT ----------------------------------------------------------
        def _on_connect(self, client, userdata, flags, reason_code, properties=None):
            if reason_code != 0:
                print(f"[smarthome] connect failed: {reason_code}", flush=True)
                return
            topic = f"{self.cfg.base_topic}/+"
            client.subscribe(topic)
            print(f"[smarthome] subscribed: {topic}", flush=True)

        def _on_message(self, client, userdata, msg):
            prefix = self.cfg.base_topic + "/"
            if not msg.topic.startswith(prefix):
                return
            device = msg.topic[len(prefix):]
            if "/" in device:  # skip .../availability, .../set, bridge sub-topics
                return
            try:
                payload = json.loads(msg.payload)
            except Exception:
                return
            if not isinstance(payload, dict):
                return

            with self._lock:
                old = {k: self._store.get((device, k)) for k in payload}
                for k, v in payload.items():
                    self._store[(device, k)] = _normalize(v)
                triggers = [t for t in self._triggers if t.device == device]

            action = payload.get("action")
            for trig in triggers:
                if self._fires(trig, payload, old, action):
                    self._safe_call(trig.cb)

        def _fires(self, trig: _Trigger, payload: dict, old: dict, action) -> bool:
            prop = trig.prop
            if prop in payload:
                new = _normalize(payload[prop])
                if old.get(prop) == new:
                    return False  # no change
                return self._want(trig.cond, _truthy(new))
            if action == prop:  # momentary button event, no stored state
                return self._want(trig.cond, True)
            return False

        @staticmethod
        def _want(cond: str, truthy_new: bool) -> bool:
            if cond in ("true", ""):
                return truthy_new
            if cond == "false":
                return not truthy_new
            if cond in ("ne", "any", "update"):
                return True
            return truthy_new

        # -- facade implementations ----------------------------------------
        def control(self, oid: str, value) -> None:
            parsed = _parse_oid(oid)
            if not parsed:
                return
            device, prop = parsed
            if prop == "state" or isinstance(value, bool):
                out = "ON" if _truthy(value) else "OFF"
            else:
                out = value
            topic = f"{self.cfg.base_topic}/{device}/set"
            self._client.publish(topic, json.dumps({prop: out}))

        def get_value(self, oid: str, attr: str = "val"):
            parsed = _parse_oid(oid)
            if not parsed:
                return None
            with self._lock:
                return self._store.get(parsed)

        def time(self, option: str):
            now = datetime.now()
            opt = (option or "wd").lower()
            return {
                "wd": now.isoweekday(),
                "dow": now.isoweekday(),
                "hour": now.hour,
                "h": now.hour,
                "minute": now.minute,
                "m": now.minute,
                "second": now.second,
                "s": now.second,
                "day": now.day,
                "month": now.month,
                "year": now.year,
            }.get(opt, now.isoweekday())

        def set_timeout(self, name: str, seconds: float, cb) -> None:
            with self._lock:
                existing = self._timeouts.pop(name, None)
                if existing:
                    existing.cancel()

                def _fire():
                    with self._lock:
                        self._timeouts.pop(name, None)
                    self._safe_call(cb)

                t = threading.Timer(max(0.0, float(seconds)), _fire)
                t.daemon = True
                self._timeouts[name] = t
                t.start()

        def clear_timeout(self, name: str) -> None:
            with self._lock:
                t = self._timeouts.pop(name, None)
            if t:
                t.cancel()

        # -- scheduler -----------------------------------------------------
        def _scheduler_loop(self) -> None:
            last: datetime | None = None
            while not self._stop.is_set():
                now = datetime.now().replace(second=0, microsecond=0)
                if now != last:
                    last = now
                    with self._lock:
                        due = [s for s in self._schedules if s.spec.matches(now)]
                    for s in due:
                        self._safe_call(s.cb)
                self._stop.wait(2.0)

        # -- helpers -------------------------------------------------------
        @staticmethod
        def _safe_call(cb) -> None:
            try:
                cb()
            except Exception:
                print(f"[smarthome] callback error:\n{traceback.format_exc()}", flush=True)
  reason: Implement the MQTT/scheduler/timeout engine and the restricted sh facade running the exported Python
```
/answer de94c624-cf1f-493f-a56b-d5151a0d26bf allow
Control Request:
```yaml
id: bafafdf9-39e8-4f8c-9450-f5208e9a5a75
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/web.py
  mode: replace
  content: |
    """HTTP glue for the single SmartHome script.

    Two routes, both under ``/api/smarthome/script``:

    * ``GET``  -> the native Blockly XML (plus any last script error).
    * ``POST`` -> ``{"xml": ..., "python": ...}``; persists both files, then
      hot-reloads the engine against the new Python.

    The functions return ``True`` when they handled the request, so the host app
    can fall through to its inherited routes otherwise.
    """
    from __future__ import annotations

    import json
    import os
    from http import HTTPStatus
    from urllib.parse import urlparse

    from .engine import SmartHomeEngine

    _ROUTE = "/api/smarthome/script"


    def handle_get(viewer, engine: SmartHomeEngine, handler) -> bool:
        if urlparse(handler.path).path != _ROUTE:
            return False
        xml = _read(engine.cfg.native_path)
        viewer._send_json(  # noqa: SLF001 - intentional reuse of base helpers
            handler,
            {"xml": xml, "error": engine.script_error},
        )
        return True


    def handle_post(viewer, engine: SmartHomeEngine, handler) -> bool:
        if urlparse(handler.path).path != _ROUTE:
            return False
        length = int(handler.headers.get("Content-Length", 0) or 0)
        body = handler.rfile.read(length) if length else b"{}"
        try:
            req = json.loads(body or b"{}")
            xml = req.get("xml", "")
            python = req.get("python", "")
            if not isinstance(xml, str) or not isinstance(python, str):
                raise ValueError("xml and python must be strings")
        except Exception as exc:
            viewer._send_json(handler, {"ok": False, "error": f"bad request: {exc}"})
            return True

        _write(engine.cfg.native_path, xml)
        _write(engine.cfg.python_path, python)

        # Reload from the freshly written Python and report any script error.
        engine._exec_source(python)  # noqa: SLF001 - engine-internal reload
        err = engine.script_error
        viewer._send_json(handler, {"ok": err is None, "error": err})
        return True


    def _read(path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""


    def _write(path: str, content: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, path)  # atomic
  reason: Add load/save endpoints that persist native XML + exported Python and hot-reload the engine
```
/answer bafafdf9-39e8-4f8c-9450-f5208e9a5a75 allow
Control Request:
```yaml
id: 4d43b699-6167-48e8-a892-098634aa2847
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  old_text: |-
    from xy.hrv.viewer.app import HrViewer

    from .client import MqttClient
    from .config import MqttConfig
    from .writer import SampleBuffer, WriterThread, create_sink


    class MqttDuck(HrViewer):
        def __init__(self, config: MqttConfig | None = None):
            super().__init__(config or MqttConfig())
            cfg: MqttConfig = self.config  # type: ignore[assignment]

            # Read + write go through the same backend (duckdb | fastparquet); the
            # DuckDB sink shares the read store's connection + lock, the
            # fastparquet sink is self-contained.
            self.buffer = SampleBuffer(maxsize=cfg.queue_max)
            self.sink = create_sink(cfg, self.store)
            self.writer = WriterThread(cfg, self.buffer, self.sink)
            self.mqtt = MqttClient(cfg, self.buffer)
  new_text: |-
    from xy.hrv.viewer.app import HrViewer
    from xy.smarthome import SmartHomeConfig, SmartHomeEngine
    from xy.smarthome import web as sh_web

    from .client import MqttClient
    from .config import MqttConfig
    from .writer import SampleBuffer, WriterThread, create_sink


    class MqttDuck(HrViewer):
        def __init__(self, config: MqttConfig | None = None):
            super().__init__(config or MqttConfig())
            cfg: MqttConfig = self.config  # type: ignore[assignment]

            # Read + write go through the same backend (duckdb | fastparquet); the
            # DuckDB sink shares the read store's connection + lock, the
            # fastparquet sink is self-contained.
            self.buffer = SampleBuffer(maxsize=cfg.queue_max)
            self.sink = create_sink(cfg, self.store)
            self.writer = WriterThread(cfg, self.buffer, self.sink)
            self.mqtt = MqttClient(cfg, self.buffer)

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
  reason: Wire SmartHome engine + endpoints into MqttDuck reusing broker config and base HTTP surface
```
/answer 4d43b699-6167-48e8-a892-098634aa2847 allow
Control Request:
```yaml
id: 33ea8db4-4894-45e4-9b50-8522e278881b
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/mqttduck/app.py
  old_text: |2-
            self.writer.start()
            self.mqtt.start()

        def on_stop(self) -> None:
            print(
                f"[mqtt-duck] stopping (written={self.writer.written}, "
                f"deduped={self.writer.deduped}, dropped={self.buffer.dropped})",
                flush=True,
            )
            # Stop the source first so no new samples race the final flush.
            self.mqtt.stop()
            self.writer.stop()
            self.writer.join(timeout=30)
  new_text: |2-
            self.writer.start()
            self.mqtt.start()
            self.smarthome.start()

        def on_stop(self) -> None:
            print(
                f"[mqtt-duck] stopping (written={self.writer.written}, "
                f"deduped={self.writer.deduped}, dropped={self.buffer.dropped})",
                flush=True,
            )
            self.smarthome.stop()
            # Stop the source first so no new samples race the final flush.
            self.mqtt.stop()
            self.writer.stop()
            self.writer.join(timeout=30)
  reason: Start/stop the SmartHome engine within the existing lifecycle hooks
```
/answer 33ea8db4-4894-45e4-9b50-8522e278881b allow
ReasoningToken: 92
Text:
 Jetzt die HTTP-Endpunkte.
ReasoningToken: 332
Text:
 Jetzt binde ich die Engine in `MqttDuck` ein (Lifecycle + Routing), mit Wiederverwendung der Broker-Credentials.
ReasoningToken: 48
Text:
 Jetzt das Frontend. Zuerst die Blockdefinitionen der IO-Broker-Blöcke.
Control Request:
```yaml
id: afd71cc1-ed14-4522-be8f-bc2e75c3c23a
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/smarthome/blocks.js
  mode: replace
  content: |
    // Custom block definitions mirroring the IO-Broker Blockly blocks used by the
    // exported smarthome script. Field NAMES must match the native XML exactly so
    // that a loaded workspace round-trips (comment/schedule/on/debug/control/
    // get_value/time_get/timeouts_*). Built-in blocks (controls_if, logic_*, math_
    // number, text, procedures_*) are reused as-is.
    (function () {
      "use strict";

      Blockly.defineBlocksWithJsonArray([
        {
          type: "comment",
          message0: "// %1",
          args0: [{ type: "field_input", name: "COMMENT", text: "comment" }],
          previousStatement: null,
          nextStatement: null,
          colour: 160,
        },
        {
          type: "schedule",
          message0: "schedule (cron) %1",
          args0: [{ type: "field_input", name: "SCHEDULE", text: "0 0 * * *" }],
          message1: "%1",
          args1: [{ type: "input_statement", name: "STATEMENT" }],
          previousStatement: null,
          nextStatement: null,
          colour: 210,
        },
        {
          type: "on",
          message0: "on change %1 when %2 ack %3",
          args0: [
            { type: "field_input", name: "OID", text: "zigbee2mqtt.0.<device>.state" },
            {
              type: "field_dropdown",
              name: "CONDITION",
              options: [
                ["is true", "true"],
                ["is false", "false"],
                ["any change", "ne"],
                ["any", "any"],
                [">", "gt"],
                [">=", "ge"],
                ["<", "lt"],
                ["<=", "le"],
              ],
            },
            { type: "field_input", name: "ACK_CONDITION", text: "" },
          ],
          message1: "%1",
          args1: [{ type: "input_statement", name: "STATEMENT" }],
          previousStatement: null,
          nextStatement: null,
          colour: 20,
        },
        {
          type: "debug",
          message0: "debug %1 %2",
          args0: [
            {
              type: "field_dropdown",
              name: "Severity",
              options: [
                ["info", "info"],
                ["warn", "warn"],
                ["error", "error"],
                ["debug", "debug"],
              ],
            },
            { type: "input_value", name: "TEXT" },
          ],
          previousStatement: null,
          nextStatement: null,
          colour: 230,
        },
        {
          type: "control",
          message0: "set %1 = %2 with delay %3",
          args0: [
            { type: "field_input", name: "OID", text: "zigbee2mqtt.0.<device>.state" },
            { type: "input_value", name: "VALUE" },
            { type: "field_checkbox", name: "WITH_DELAY", checked: false },
          ],
          previousStatement: null,
          nextStatement: null,
          inputsInline: true,
          colour: 290,
        },
        {
          type: "get_value",
          message0: "value %1 of %2",
          args0: [
            {
              type: "field_dropdown",
              name: "ATTR",
              options: [
                ["value", "val"],
                ["ack", "ack"],
                ["timestamp", "ts"],
                ["last change", "lc"],
              ],
            },
            { type: "field_input", name: "OID", text: "zigbee2mqtt.0.<device>.temperature" },
          ],
          output: null,
          colour: 290,
        },
        {
          type: "time_get",
          message0: "time %1",
          args0: [
            {
              type: "field_dropdown",
              name: "OPTION",
              options: [
                ["weekday (1-7)", "wd"],
                ["hour", "hour"],
                ["minute", "minute"],
                ["second", "second"],
                ["day", "day"],
                ["month", "month"],
                ["year", "year"],
              ],
            },
          ],
          output: "Number",
          colour: 120,
        },
        {
          type: "timeouts_settimeout",
          message0: "setTimeout %1 after %2 %3",
          args0: [
            { type: "field_input", name: "NAME", text: "timer" },
            { type: "field_number", name: "DELAY", value: 60, min: 0 },
            {
              type: "field_dropdown",
              name: "UNIT",
              options: [
                ["ms", "ms"],
                ["s", "s"],
                ["min", "min"],
                ["h", "h"],
              ],
            },
          ],
          message1: "%1",
          args1: [{ type: "input_statement", name: "STATEMENT" }],
          previousStatement: null,
          nextStatement: null,
          colour: 60,
        },
        {
          type: "timeouts_cleartimeout",
          message0: "clearTimeout %1",
          args0: [{ type: "field_input", name: "NAME", text: "timer" }],
          previousStatement: null,
          nextStatement: null,
          colour: 60,
        },
      ]);
    })();
  reason: Define frontend Blockly blocks matching the native IO-Broker XML field names for round-tripping
```
/answer afd71cc1-ed14-4522-be8f-bc2e75c3c23a allow
Control Request:
```yaml
id: 1374cbf7-5a49-4126-b14f-fc1bbae4ac98
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/smarthome/generators.js
  mode: replace
  content: |
    // Python generators for the custom blocks. Everything is emitted as top-level
    // statements calling the injected `sh` facade; hat-like blocks (schedule/on/
    // setTimeout) wrap their body in a generated def and register it. Built-in
    // blocks fall back to pythonGenerator's own generators.
    (function () {
      "use strict";

      var P = Blockly.Python;
      var UNIT_SECONDS = { ms: 0.001, s: 1, sec: 1, min: 60, h: 3600 };

      function reg(name, fn) {
        if (P.forBlock) P.forBlock[name] = fn;
        else P[name] = fn;
      }
      function fnName(prefix, block) {
        return prefix + block.id.replace(/[^A-Za-z0-9_]/g, "_");
      }
      function body(gen, block, name) {
        return gen.statementToCode(block, name) || gen.INDENT + "pass\n";
      }

      reg("comment", function (block) {
        return "# " + (block.getFieldValue("COMMENT") || "") + "\n";
      });

      reg("schedule", function (block, gen) {
        gen = gen || P;
        var fn = fnName("_sched_", block);
        return (
          "def " + fn + "():\n" + body(gen, block, "STATEMENT") +
          "sh.schedule(" + gen.quote_(block.getFieldValue("SCHEDULE")) + ", " + fn + ")\n"
        );
      });

      reg("on", function (block, gen) {
        gen = gen || P;
        var fn = fnName("_on_", block);
        return (
          "def " + fn + "():\n" + body(gen, block, "STATEMENT") +
          "sh.on(" + gen.quote_(block.getFieldValue("OID")) + ", " +
          gen.quote_(block.getFieldValue("CONDITION")) + ", " + fn + ")\n"
        );
      });

      reg("debug", function (block, gen) {
        gen = gen || P;
        var text = gen.valueToCode(block, "TEXT", gen.ORDER_NONE) || "''";
        return "sh.debug(" + text + ", " + gen.quote_(block.getFieldValue("Severity")) + ")\n";
      });

      reg("control", function (block, gen) {
        gen = gen || P;
        var val = gen.valueToCode(block, "VALUE", gen.ORDER_NONE) || "None";
        return "sh.control(" + gen.quote_(block.getFieldValue("OID")) + ", " + val + ")\n";
      });

      reg("get_value", function (block, gen) {
        gen = gen || P;
        var code =
          "sh.get_value(" + gen.quote_(block.getFieldValue("OID")) + ", " +
          gen.quote_(block.getFieldValue("ATTR")) + ")";
        return [code, gen.ORDER_FUNCTION_CALL];
      });

      reg("time_get", function (block, gen) {
        gen = gen || P;
        return ["sh.time(" + gen.quote_(block.getFieldValue("OPTION")) + ")", gen.ORDER_FUNCTION_CALL];
      });

      reg("timeouts_settimeout", function (block, gen) {
        gen = gen || P;
        var delay = Number(block.getFieldValue("DELAY")) || 0;
        var unit = block.getFieldValue("UNIT");
        var secs = delay * (UNIT_SECONDS[unit] || 0.001);
        var fn = fnName("_to_", block);
        return (
          "def " + fn + "():\n" + body(gen, block, "STATEMENT") +
          "sh.set_timeout(" + gen.quote_(block.getFieldValue("NAME")) + ", " + secs + ", " + fn + ")\n"
        );
      });

      reg("timeouts_cleartimeout", function (block, gen) {
        gen = gen || P;
        return "sh.clear_timeout(" + gen.quote_(block.getFieldValue("NAME")) + ")\n";
      });
    })();
  reason: Add Python generators for the custom blocks emitting sh-facade calls
```
/answer 1374cbf7-5a49-4126-b14f-fc1bbae4ac98 allow
ReasoningToken: 4809
Control Request:
```yaml
id: 8975311b-57bf-4499-a2e0-0ddff8671bdb
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/smarthome/app.js
  mode: replace
  content: |
    // SmartHome editor: inject the workspace, load the single native script from
    // the backend, and save it back (native XML + generated Python) on demand.
    (function () {
      "use strict";

      var ENDPOINT = "/api/smarthome/script";
      var ws = null;

      function xmlTextToDom(text) {
        if (Blockly.utils && Blockly.utils.xml && Blockly.utils.xml.textToDom) {
          return Blockly.utils.xml.textToDom(text);
        }
        return Blockly.Xml.textToDom(text);
      }

      function status(msg, isError) {
        var el = document.getElementById("status");
        el.textContent = msg || "";
        el.className = "status" + (isError ? " error" : "");
      }

      function load() {
        fetch(ENDPOINT)
          .then(function (r) { return r.json(); })
          .then(function (data) {
            ws.clear();
            var xml = (data.xml || "").trim();
            if (xml) {
              Blockly.Xml.domToWorkspace(xmlTextToDom(xml), ws);
            }
            if (data.error) {
              status("Loaded (last run had a script error - see server log)", true);
            } else {
              status("Loaded");
            }
          })
          .catch(function (e) { status("Load failed: " + e, true); });
      }

      function save() {
        var dom = Blockly.Xml.workspaceToDom(ws);
        var xml = Blockly.Xml.domToText(dom);
        var python;
        try {
          python = Blockly.Python.workspaceToCode(ws);
        } catch (e) {
          status("Python generation failed: " + e, true);
          return;
        }
        status("Saving...");
        fetch(ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ xml: xml, python: python }),
        })
          .then(function (r) { return r.json(); })
          .then(function (res) {
            if (res.ok) status("Saved & reloaded");
            else status("Saved, but script error: " + (res.error || "unknown"), true);
          })
          .catch(function (e) { status("Save failed: " + e, true); });
      }

      window.addEventListener("load", function () {
        ws = Blockly.inject("blocklyDiv", {
          toolbox: document.getElementById("toolbox"),
          trashcan: true,
          zoom: { controls: true, wheel: true, startScale: 0.9 },
          grid: { spacing: 20, length: 3, colour: "#eee", snap: true },
        });
        document.getElementById("save").addEventListener("click", save);
        document.getElementById("reload").addEventListener("click", load);
        load();
      });
    })();
  reason: "Add editor logic: inject workspace, load native XML, save XML+Python to endpoint"
```
/answer 8975311b-57bf-4499-a2e0-0ddff8671bdb allow
Control Request:
```yaml
id: 77c23058-0ee4-4a6d-8e92-8958b38499de
toolName: write
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/smarthome.html
  mode: replace
  content: |
    <!DOCTYPE html>
    <html lang="de">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>SmartHome</title>
      <style>
        html, body { margin: 0; height: 100%; font-family: sans-serif; }
        body { display: flex; flex-direction: column; }
        .topbar {
          display: flex; align-items: center; gap: 12px;
          padding: 8px 14px; background: #263238; color: #fff;
        }
        .topbar h1 { font-size: 18px; margin: 0; font-weight: 600; }
        .topbar button {
          padding: 6px 14px; border: 0; border-radius: 4px; cursor: pointer;
          background: #4caf50; color: #fff; font-size: 14px;
        }
        .topbar button#reload { background: #607d8b; }
        .status { margin-left: auto; font-size: 13px; opacity: 0.9; }
        .status.error { color: #ff8a80; }
        #blocklyDiv { flex: 1 1 auto; }
      </style>
      <script src="blockly/blockly_compressed.js"></script>
      <script src="blockly/blocks_compressed.js"></script>
      <script src="blockly/python_compressed.js"></script>
      <script src="blockly/de.js"></script>
    </head>
    <body>
      <header class="topbar">
        <h1>SmartHome</h1>
        <button id="save">Speichern</button>
        <button id="reload">Neu laden</button>
        <span id="status" class="status"></span>
      </header>

      <div id="blocklyDiv"></div>

      <xml id="toolbox" style="display: none">
        <category name="Trigger" colour="20">
          <block type="schedule"><field name="SCHEDULE">0 0 * * *</field></block>
          <block type="on"></block>
        </category>
        <category name="Aktionen" colour="290">
          <block type="control"></block>
          <block type="get_value"></block>
        </category>
        <category name="Timer" colour="60">
          <block type="timeouts_settimeout"></block>
          <block type="timeouts_cleartimeout"></block>
        </category>
        <category name="Zeit" colour="120">
          <block type="time_get"></block>
        </category>
        <category name="Logik" colour="210">
          <block type="controls_if"></block>
          <block type="logic_compare"></block>
          <block type="logic_operation"></block>
          <block type="logic_negate"></block>
          <block type="logic_boolean"></block>
        </category>
        <category name="Werte" colour="230">
          <block type="math_number"><field name="NUM">0</field></block>
          <block type="math_arithmetic"></block>
          <block type="text"></block>
          <block type="debug"></block>
          <block type="comment"></block>
        </category>
        <category name="Funktionen" colour="290" custom="PROCEDURE"></category>
      </xml>

      <script src="smarthome/blocks.js"></script>
      <script src="smarthome/generators.js"></script>
      <script src="smarthome/app.js"></script>
    </body>
    </html>
  reason: "Create the static Blockly editor page with toolbox, save/reload UI"
```
/answer 77c23058-0ee4-4a6d-8e92-8958b38499de allow
ReasoningToken: 20
Text:
 Ich teste das Backend: Imports, Cron, und die Engine-Semantik mit einem repräsentativen (wie von Blockly erzeugten) Python-Skript — ohne echten Netzwerkverbindungsaufbau.
Control Request:
```yaml
id: 0044be53-7f1f-4b9c-9a1f-7034603eb4e9
toolName: bash
arguments:
  script: |-
    cd /home/user/xyan/XY.Archiv/hrviewer
    export PYTHONPATH=src
    python - <<'PY'
    import types, json
    from datetime import datetime
    from xy.smarthome.config import SmartHomeConfig
    from xy.smarthome.engine import SmartHomeEngine
    from xy.smarthome.cron import CronSpec

    # --- cron sanity
    assert CronSpec("0 1 * * *").matches(datetime(2026,8,20,1,0))
    assert not CronSpec("0 1 * * *").matches(datetime(2026,8,20,2,0))
    assert CronSpec("0 7 * * *").matches(datetime(2026,8,20,7,0))
    print("cron ok")

    cfg = SmartHomeConfig()
    eng = SmartHomeEngine(cfg)
    published = []
    eng._client.publish = lambda topic, payload=None, **k: published.append((topic, payload))

    sample = '''
    def allOff():
        # Gaestedose
        sh.control('zigbee2mqtt.0.0xa4c1387253897923.state', False)
        sh.control('zigbee2mqtt.0.0xa4c138edbd20f773.state', False)

    def _sched_A():
        sh.debug('Kill Off Schedule', 'info')
        allOff()
    sh.schedule('0 1 * * *', _sched_A)

    def _on_B():
        sh.debug('Kill Off Switch', 'info')
        allOff()
    sh.on('zigbee2mqtt.0.0x60a423fffe803811.1_single', 'true', _on_B)

    def _on_H():
        if (sh.time('wd') != 7):
            sh.clear_timeout('heizung')
            def _to_1():
                sh.control('zigbee2mqtt.0.0xa4c138edbd20f773.state', False)
            sh.set_timeout('heizung', 3600, _to_1)
    sh.on('zigbee2mqtt.0.0xa4c138edbd20f773.state', 'true', _on_H)

    def _sched_W():
        if (sh.get_value('zigbee2mqtt.0.0xa4c1383c7d3c4cb5.temperature', 'val') < 39):
            sh.control('zigbee2mqtt.0.0xa4c138edbd20f773.state', True)
    sh.schedule('0 17 * * *', _sched_W)
    '''
    eng._exec_source(sample)
    assert eng.script_error is None, eng.script_error
    assert len(eng._schedules) == 2
    assert len(eng._triggers) == 2
    print("exec ok: schedules", len(eng._schedules), "triggers", len(eng._triggers))

    class Msg:
        def __init__(self, t, p): self.topic=t; self.payload=json.dumps(p).encode()

    # button press -> allOff -> two OFF publishes
    published.clear()
    eng._on_message(None, None, Msg("zigbee2mqtt/0x60a423fffe803811", {"action":"1_single"}))
    print("button publishes:", published)
    assert any("0xa4c1387253897923/set" in t for t,_ in published)
    assert all(json.loads(p)["state"]=="OFF" for _,p in published)

    # button press again fires again (momentary)
    published.clear()
    eng._on_message(None, None, Msg("zigbee2mqtt/0x60a423fffe803811", {"action":"1_single"}))
    assert len(published)==2, published
    print("momentary refire ok")

    # heater turned ON -> sets timeout 'heizung'
    published.clear()
    eng._on_message(None, None, Msg("zigbee2mqtt/0xa4c138edbd20f773", {"state":"ON"}))
    print("timeouts after heater ON:", list(eng._timeouts))
    assert "heizung" in eng._timeouts

    # temperature stored, schedule reads it
    eng._on_message(None, None, Msg("zigbee2mqtt/0xa4c1383c7d3c4cb5", {"temperature":21.5}))
    assert eng.get_value("zigbee2mqtt.0.0xa4c1383c7d3c4cb5.temperature")==21.5
    published.clear()
    eng._schedules[1].cb()   # _sched_W (17:00 hot water check)
    print("hotwater publishes:", published)
    assert any(json.loads(p)["state"]=="ON" for _,p in published)

    # state trigger should NOT fire on no-change repeat
    published.clear()
    eng._on_message(None, None, Msg("zigbee2mqtt/0xa4c138edbd20f773", {"state":"ON"}))
    # same value -> _on_H should not fire (no new set_timeout call side effect visible),
    # but clear/set happen internally; just ensure no exception
    print("repeat-state ok")

    # clear timeouts to exit cleanly
    for t in eng._timeouts.values(): t.cancel()
    print("ALL OK")
    PY
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: "Validate engine semantics (triggers, momentary events, timeouts, get_value, schedules, control mapping)"
```
/answer 0044be53-7f1f-4b9c-9a1f-7034603eb4e9 allow
Control Request:
```yaml
id: b63e60b5-b9c8-4e38-94b1-64e7c1517de2
result:
  structuredContent:
    stdout: |
      cron ok
      exec ok: schedules 2 triggers 2
      [smarthome:info] Kill Off Switch
      button publishes: [('zigbee2mqtt/0xa4c1387253897923/set', '{"state": "OFF"}'), ('zigbee2mqtt/0xa4c138edbd20f773/set', '{"state": "OFF"}')]
      [smarthome:info] Kill Off Switch
      momentary refire ok
      timeouts after heater ON: ['heizung']
      hotwater publishes: [('zigbee2mqtt/0xa4c138edbd20f773/set', '{"state": "ON"}')]
      repeat-state ok
      ALL OK
```
/answer b63e60b5-b9c8-4e38-94b1-64e7c1517de2 allow
ReasoningToken: 1413
Text:
 Backend-Semantik ist grün. Jetzt validiere ich den echten Blockly-Python-Generator (Node, headless) für die Custom-Blöcke, damit das erzeugte Python zum Sandbox-`sh` passt.
Control Request:
```yaml
id: 8aa3462b-87b5-4f28-ba6f-fc27918485b2
toolName: bash
arguments:
  script: |-
    cd /home/user/xyan/XY.Archiv/hrviewer/statics
    node --check smarthome/blocks.js && node --check smarthome/generators.js && node --check smarthome/app.js && echo "JS syntax ok"
    node - <<'JS'
    const fs = require('fs');
    const path = require('path');
    const B = require(path.resolve('blockly/blockly_compressed.js'));
    global.Blockly = B;
    require(path.resolve('blockly/blocks_compressed.js'));
    const py = require(path.resolve('blockly/python_compressed.js'));
    B.Python = py.pythonGenerator || py;
    // load our custom defs + generators (IIFEs referencing global Blockly)
    eval(fs.readFileSync('smarthome/blocks.js','utf8'));
    eval(fs.readFileSync('smarthome/generators.js','utf8'));

    const ws = new B.Workspace();
    function conn(a, inputName, b){ a.getInput(inputName).connection.connect(b.outputConnection); }

    // procedure allOff { control gaeste = false }
    const proc = ws.newBlock('procedures_defnoreturn');
    proc.setFieldValue('allOff','NAME');
    const ctrl = ws.newBlock('control');
    ctrl.setFieldValue('zigbee2mqtt.0.0xGAESTE.state','OID');
    const bf = ws.newBlock('logic_boolean'); bf.setFieldValue('FALSE','BOOL');
    conn(ctrl,'VALUE',bf);
    proc.getInput('STACK').connection.connect(ctrl.previousConnection);

    // schedule 0 1 * * * -> call allOff
    const sch = ws.newBlock('schedule');
    sch.setFieldValue('0 1 * * *','SCHEDULE');
    const call = ws.newBlock('procedures_callnoreturn');
    call.getMutationName && null;
    // set the call target name via mutation
    call.setFieldValue && null;
    if (call.getField('NAME')) call.setFieldValue('allOff','NAME');
    sch.getInput('STATEMENT').connection.connect(call.previousConnection);

    // on heater state -> settimeout heizung 60 min -> control off
    const on = ws.newBlock('on');
    on.setFieldValue('zigbee2mqtt.0.0xHEAT.state','OID');
    on.setFieldValue('true','CONDITION');
    const st = ws.newBlock('timeouts_settimeout');
    st.setFieldValue('heizung','NAME'); st.setFieldValue(60,'DELAY'); st.setFieldValue('min','UNIT');
    const c2 = ws.newBlock('control'); c2.setFieldValue('zigbee2mqtt.0.0xHEAT.state','OID');
    const bf2 = ws.newBlock('logic_boolean'); bf2.setFieldValue('FALSE','BOOL'); conn(c2,'VALUE',bf2);
    st.getInput('STATEMENT').connection.connect(c2.previousConnection);
    on.getInput('STATEMENT').connection.connect(st.previousConnection);

    const code = B.Python.workspaceToCode(ws);
    console.log("=========== GENERATED PYTHON ===========");
    console.log(code);
    console.log("========================================");
    fs.writeFileSync('/tmp/sh_generated.py', code);
    JS
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics
  reason: Confirm Blockly's pythonGenerator with our custom generators emits valid sh-facade Python and procedure hoisting
```
/answer 8aa3462b-87b5-4f28-ba6f-fc27918485b2 allow
Control Request:
```yaml
id: fe50d003-ee55-4b3a-b26b-b3f8834d6359
result:
  structuredContent:
    stdout: |
      JS syntax ok
      =========== GENERATED PYTHON ===========
      def allOff():
        sh.control('zigbee2mqtt.0.0xGAESTE.state', False)

      def _sched_w_HiLsWVUfWX3__mKT6_():
        allOff()
      sh.schedule('0 1 * * *', _sched_w_HiLsWVUfWX3__mKT6_)

      def _on_1iLa_rSd_m5__aP_0___():
        def _to_aWV_x_ILj4_m__uVJ__v():
          sh.control('zigbee2mqtt.0.0xHEAT.state', False)
        sh.set_timeout('heizung', 3600, _to_aWV_x_ILj4_m__uVJ__v)
      sh.on('zigbee2mqtt.0.0xHEAT.state', 'true', _on_1iLa_rSd_m5__aP_0___)

      ========================================
```
/answer fe50d003-ee55-4b3a-b26b-b3f8834d6359 allow
Control Request:
```yaml
id: 469e2187-67f6-4df5-ade5-ca7221ed1ef7
toolName: bash
arguments:
  script: |-
    cd /home/user/xyan/XY.Archiv/hrviewer
    export PYTHONPATH=src
    python - <<'PY'
    import json
    from xy.smarthome.config import SmartHomeConfig
    from xy.smarthome.engine import SmartHomeEngine
    eng = SmartHomeEngine(SmartHomeConfig())
    pub=[]; eng._client.publish=lambda t,payload=None,**k: pub.append((t,payload))
    eng._exec_source(open('/tmp/sh_generated.py').read())
    assert eng.script_error is None, eng.script_error
    print("schedules",len(eng._schedules),"triggers",len(eng._triggers))
    # fire schedule (allOff)
    eng._schedules[0].cb(); print("sched->",pub); pub.clear()
    # fire heater-on trigger -> timeout set
    class M:
      def __init__(s,t,p): s.topic=t; s.payload=json.dumps(p).encode()
    eng._on_message(None,None,M("zigbee2mqtt/0xHEAT",{"state":"ON"}))
    print("timeouts",list(eng._timeouts))
    for t in eng._timeouts.values(): t.cancel()
    print("E2E OK")
    PY
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Execute the Blockly-generated Python through the engine to confirm the full pipeline works
```
/answer 469e2187-67f6-4df5-ade5-ca7221ed1ef7 allow
Control Request:
```yaml
id: a710ae78-853f-4b25-afae-74d4d31186aa
result:
  structuredContent:
    stdout: |
      schedules 1 triggers 1
      sched-> [('zigbee2mqtt/0xGAESTE/set', '{"state": "OFF"}')]
      timeouts ['heizung']
      E2E OK
```
/answer a710ae78-853f-4b25-afae-74d4d31186aa allow
ReasoningToken: 1859
Text:
 Der Blockly-Python-Export passt exakt zum Sandbox-`sh`. Ich führe das generierte File noch durch die Engine, um den End-to-End-Pfad (Frontend-Export → Backend-Exec) zu bestätigen.
Control Request:
```yaml
id: 4ee3a42e-be1b-4fce-ad18-26422eb539a3
toolName: bash
arguments:
  script: |-
    cd /home/user/xyan/XY.Archiv/hrviewer
    export PYTHONPATH=src
    python -c "import xy.mqttduck.app as m; print('import ok:', hasattr(m,'MqttDuck'))" 2>&1 | tail -5
  cwd: /home/user/xyan/XY.Archiv/hrviewer
  reason: Ensure the modified MqttDuck app module imports cleanly with the smarthome wiring
```
/answer 4ee3a42e-be1b-4fce-ad18-26422eb539a3 allow
Control Request:
```yaml
id: 1396f76f-5156-4661-933b-a437253614fe
result:
  structuredContent:
    stdout: |
      import ok: True
```
/answer 1396f76f-5156-4661-933b-a437253614fe allow
ReasoningToken: 86
Text:
 Voll funktionsfähig. Ich prüfe noch, dass die geänderte `mqttduck/app.py` sauber importiert.
ReasoningToken: 339
ReasoningToken: 220
Fertig. Alles ist implementiert und getestet (Backend-Semantik, echter Blockly-Python-Export headless, und End-to-End Frontend-Export → Backend-Exec).

## Was umgesetzt wurde

**Ansatz** (nach deiner Korrektur): Kein eigener XML→Python-Compiler im Backend — stattdessen Blocklys eingebauter `pythonGenerator` im Frontend. Das Frontend schickt native XML **und** generiertes Python; das Backend speichert beides und führt nur noch das Python in einer Sandbox aus.

### Backend — neues Package `xy.smarthome` (semantisch getrennt)
- **`config.py`** — `SmartHomeConfig`; `from_mqtt()` erbt Broker-Host/Credentials von der bestehenden `MqttConfig` (nur eigene client-id → eigene MQTT-Instanz).
- **`cron.py`** — schlanker 5-Feld-Cron-Matcher (`*`, Listen, Ranges, `*/n`).
- **`engine.py`** — eigener paho-Client, Scheduler-Thread, benannte Timeouts, State-Store und das restriktive **`sh`-Facade**. Das Skript läuft via `exec` mit kuratierten `__builtins__` (kein import/open/eval) und nur `sh` als Zugang. OID-Mapping `zigbee2mqtt.0.<device>.<prop>` → Topics `zigbee2mqtt/<device>` (State) bzw. `.../set` (`{"state":"ON"/"OFF"}`); Momentary-Buttons via `{"action": "..."}`.
- **`web.py`** — `GET/POST /api/smarthome/script` (laden/speichern + Hot-Reload).

### Integration in MQTT-Duck (zentrale Komponenten mitbenutzt)
- **`mqttduck/app.py`** — `MqttDuck` erzeugt `SmartHomeEngine(SmartHomeConfig.from_mqtt(cfg))`, startet/stoppt sie in `on_start`/`on_stop`, und routet die Smarthome-Endpunkte, bevor es an die geerbte HTTP-/Statics-Fläche durchreicht.

### Frontend (Statics, über bestehenden Mechanismus)
- **`statics/smarthome.html`** — Blockly-Editor (lädt `blockly/python_compressed.js`), Toolbox, „Speichern“/„Neu laden“.
- **`statics/smarthome/blocks.js`** — Custom-Blöcke mit exakt passenden Feldnamen (comment, schedule, on, debug, control, get_value, time_get, timeouts_set/clear), sodass die native XML verlustfrei round-trippt.
- **`statics/smarthome/generators.js`** — Python-Generatoren, die `sh.…`-Aufrufe erzeugen (Built-ins wie `controls_if`, `logic_*`, `procedures_*` via pythonGenerator).
- **`statics/smarthome/app.js`** — laden (GET), speichern (XML + `Blockly.Python.workspaceToCode`).

## Verifizierte Abbildung der IO-Broker-Konfiguration
`allOff`-Prozedur + Kill-Schedule/-Switch, Schlafzimmer/Espresso-Schedules, Heizungs-Auto-Off-Timer (60 min, außer Sonntag via `time('wd') != 7`) und der 17-Uhr-Warmwasser-Check (`get_value(temperature) < 39`) — alle Blocktypen des Exports werden erzeugt und laufen durch die Engine.

## Zugriff / erster Start
- Editor: `http://<host>:8081/smarthome.html`.
- Beim allerersten Start existiert `project/smarthome_generated.py` noch nicht → die Automation ist idle. Einmal im Editor **Speichern** klicken (die native `project/smarthome.xml` wird geladen), dann ist das Python generiert und die Engine läuft (und reloaded bei jedem weiteren Speichern).

Ein Hinweis zur Prüfung: Die Trigger-/Action-Semantik (ON/OFF, Momentary, weekday=ISO 1–7) habe ich aus dem Export abgeleitet — bitte v.a. den Button `0x60a423….1_single` und die `state`-Trigger einmal live gegen dein Zigbee2MQTT gegenprüfen, da die exakten z2m-Payloads geräteabhängig sind.
