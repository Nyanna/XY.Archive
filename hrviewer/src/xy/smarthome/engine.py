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
