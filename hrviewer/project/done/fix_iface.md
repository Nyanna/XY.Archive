Korrigiere in `/home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/tracking/tracker.py` die Ermittelung des Interface.
Alle Geräte werden initial als LAN betrachtet es sei denn das Config Mapping definiert WLAN.
Darüber hinaus wird das Interface auf WLAN geändert, wenn über Syslog oder SNMP Polling (vom WLAN AP bestätigt) eine Meldung zu einem Gerät eingeht.
SystemInit:  id=5656bb55-7d91-408a-af7f-f114db7ec40b, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5-5
Control Request:
```yaml
id: 6f24-97-0
toolName: ast_outline
arguments:
  paths:
  - /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/tracking/tracker.py
  reason: Understand tracker structure
```
/answer 6f24-97-0 allow
Control Request:
```yaml
id: 6f24-98-97
result:
  structuredContent:
    results:
    - path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/tracking/tracker.py
      nodes:
      - id: IqKLbY|5bOUUW
        signature: "'In-memory device tracker: merges DHCP, syslog and SNMP observations.'"
      - id: EALEmt|puCXC2
        signature: from __future__ import annotations
      - id: BXYK7q|1nCVSv
        signature: _PRUNE_INTERVAL_S = 3600
      - id: iso
        signature: "def _iso(ts: float | None) -> str | None:"
      - id: Tracker
        signature: "class Tracker:"
        children:
        - id: Tracker.init
          signature: "def __init__(self, cfg: TrackingConfig | None=None, clock=time.time) -> None:"
        - id: Tracker.kMCeqM|vxMlFG
          signature: '''# -- lifecycle ---------------------------------------------------------'''
        - id: Tracker.start
          signature: "def start(self) -> None:"
        - id: Tracker.stop
          signature: "def stop(self) -> None:"
        - id: Tracker.0IUclp|MuLeJl
          signature: '''# -- observations ------------------------------------------------------'''
        - id: Tracker.on_dhcp
          signature: "def on_dhcp(self, mac: str, hostname: str | None=None, ip: str | None=None, confirmed: bool=False, ts: float | None=None) -> None:"
        - id: Tracker.on_station
          signature: "def on_station(self, ev: StationEvent) -> None:"
        - id: Tracker.on_client_table
          signature: "def on_client_table(self, ap_ip: str, samples: list[ClientSample], ts: float | None=None, started: float | None=None) -> None:"
          docstring: Authoritative snapshot of the clients associated with one AP.
        - id: Tracker.SPOzWi|Mw85kM
          signature: '''# -- query -------------------------------------------------------------'''
        - id: Tracker.snapshot
          signature: "def snapshot(self, now: float | None=None) -> dict:"
        - id: Tracker.aWLUoT|Ubzx0z
          signature: '''# -- internals ---------------------------------------------------------'''
        - id: Tracker.now
          signature: "def _now(self, ts: float | None=None) -> float:"
        - id: Tracker.register_ap
          signature: "def _register_ap(self, ap: AccessPoint) -> None:"
        - id: Tracker.ap
          signature: "def _ap(self, ip: str | None, mac: str | None) -> AccessPoint:"
        - id: Tracker.device
          signature: "def _device(self, mac: str, ts: float) -> Device | None:"
        - id: Tracker.prune
          signature: "def _prune(self, now: float) -> None:"
        - id: Tracker.locate
          signature: "def _locate(self, dev: Device, ap: AccessPoint, band: str | None, ts: float) -> None:"
        - id: Tracker.apply_sample
          signature: "def _apply_sample(self, dev: Device, ap: AccessPoint, s: ClientSample, ts: float) -> None:"
        - id: Tracker.disconnect
          signature: "@staticmethod def _disconnect(dev: Device, ts: float) -> None:"
        - id: Tracker.render_ap
          signature: "def _render_ap(self, ap: AccessPoint) -> dict:"
        - id: Tracker.render
          signature: "def _render(self, d: Device, now: float) -> dict:"
```
/answer 6f24-98-97 allow
Control Request:
```yaml
id: 6f24-99-0
toolName: search
arguments:
  items:
  - directory:
    - /home/user/xyan/XY.Archiv/hrviewer/src
    pattern: interface|wlan|WLAN|LAN
    include:
    - tracker.py
    limit: 50
  reason: Find interface logic
```
/answer 6f24-99-0 allow
Control Request:
```yaml
id: 6f24-9a-99
result:
  structuredContent:
    results:
    - directory:
      - /home/user/xyan/XY.Archiv/hrviewer/src
      matches:
      - path: xy/smarthome/tracking/tracker.py
        matches:
        - interface = (mapping.interface if mapping else None) or (
        - '''wlan'' if d.seen_on_ap else ''lan'' if d.seen_dhcp else None)'
        - "if interface == 'wlan':"
        - "elif interface == 'lan':"
        - "'interface': interface,"
```
/answer 6f24-9a-99 allow
Control Request:
```yaml
id: 6f24-9b-0
toolName: ast_read
arguments:
  items:
  - path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/tracking/tracker.py
    ids:
    - Tracker.render
    - Tracker.on_station
    - Tracker.on_client_table
    - Tracker.on_dhcp
    - Tracker.locate
    - Tracker.apply_sample
  reason: Read relevant methods
```
/answer 6f24-9b-0 allow
Control Request:
```yaml
id: 6f24-9c-9b
result:
  structuredContent:
    results:
    - path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/tracking/tracker.py
      nodes:
      - id: Tracker.render
        type: FunctionDef
        code: |-
          def _render(self, d: Device, now: float) -> dict:
              cfg = self.cfg
              mapping = self.cfg.mappings.get(d.mac)
              interface = (mapping.interface if mapping else None) or ('wlan' if d.seen_on_ap else 'lan' if d.seen_dhcp else None)
              location = None
              if d.ap_ip:
                  ap = self._aps.get(d.ap_ip)
                  location = {
                      'ap_ip': d.ap_ip,
                      'ap_mac': ap.mac if ap else None,
                      'ap_name': ap.name if ap else None,
                      'floor': ap.floor if ap else None,
                      'room': ap.room if ap else None,
                      'band': d.band,
                      'signal_pct': d.signal_pct,
                      'rssi': d.rssi,
                      'distance_m': d.distance_m,
                      'distance_is_upper_bound': d.distance_is_upper_bound,
                      'wifi_standard': d.wifi_standard,
                      'link_rate_mbps': d.link_rate_mbps,
                      'updated': _iso(
                          d.located_at)}
              if interface == 'wlan':
                  connected = d.connected
              elif interface == 'lan':
                  connected = d.last_dhcp is not None and now - d.last_dhcp < cfg.lan_connected_s
              else:
                  connected = None
              since_move = None if d.last_moved is None else now - d.last_moved
              return {
                  'mac': d.mac,
                  'display_name': (
                      mapping.name if mapping else None) or d.hostname or d.mac,
                  'owner': mapping.owner if mapping else None,
                  'hostname': d.hostname,
                  'interface': interface,
                  'ip': d.ip,
                  'connected': connected,
                  'first_seen': _iso(
                      d.first_seen),
                  'last_seen': _iso(
                      d.last_seen),
                  'last_active': _iso(
                      d.last_active),
                  'disconnected_at': _iso(
                      d.disconnected_at),
                  'idle_s': None if d.last_active is None else round(
                      now - d.last_active),
                  'location': location,
                  'movement': {
                      'moving': bool(
                          d.connected and since_move is not None and (
                              since_move <= cfg.moving_s)),
                      'recently_moved': since_move is not None and since_move <= cfg.recent_move_s,
                      'last_moved': _iso(
                          d.last_moved),
                      'roam_count': d.roam_count}}
      - id: Tracker.on_station
        type: FunctionDef
        code: |-
          def on_station(self, ev: StationEvent) -> None:
              ts = self._now(ev.ts)
              with self._lock:
                  ap = self._ap(ev.ap_ip, ev.ap_mac)
                  dev = self._device(ev.mac, ts)
                  if dev is None:
                      return
                  dev.seen_on_ap = True
                  if ev.ip:
                      dev.ip = ev.ip
                  if ev.kind == 'leave':
                      same_band = ev.band is None or dev.band is None or ev.band == dev.band
                      if dev.connected and dev.ap_ip == ap.ip and same_band:
                          self._disconnect(dev, ts)
                      return
                  self._locate(dev, ap, ev.band, ts)
                  dev.connected = True
                  dev.disconnected_at = None
                  if ev.kind in ('join', 'active'):
                      dev.last_active = ts
      - id: Tracker.on_client_table
        type: FunctionDef
        code: |-
          def on_client_table(self, ap_ip: str, samples: list[ClientSample], ts: float | None=None, started: float | None=None) -> None:
              """Authoritative snapshot of the clients associated with one AP."""
              ts = self._now(ts)
              started = ts if started is None else started
              with self._lock:
                  ap = self._ap(ap_ip, None)
                  present: set[str] = set()
                  for sample in samples:
                      dev = self._device(sample.mac, ts)
                      if dev is None:
                          continue
                      present.add(sample.mac)
                      '# a cached row of the old AP must not override a fresh location elsewhere'
                      if dev.connected and dev.ap_ip not in (None, ap.ip) and (ts - dev.located_at < self.cfg.stale_s):
                          continue
                      self._apply_sample(dev, ap, sample, ts)
                  for dev in self._devices.values():
                      if dev.connected and dev.ap_ip == ap.ip and (dev.mac not in present) and (dev.located_at < started):
                          self._disconnect(dev, ts)
      - id: Tracker.on_dhcp
        type: FunctionDef
        code: |-
          def on_dhcp(self, mac: str, hostname: str | None=None, ip: str | None=None, confirmed: bool=False, ts: float | None=None) -> None:
              ts = self._now(ts)
              with self._lock:
                  dev = self._device(mac, ts)
                  if dev is None:
                      return
                  dev.seen_dhcp = True
                  dev.last_dhcp = ts
                  dev.last_active = ts
                  if hostname:
                      dev.hostname = hostname
                  if ip and (confirmed or dev.ip is None):
                      dev.ip = ip
      - id: Tracker.locate
        type: FunctionDef
        code: |-
          def _locate(self, dev: Device, ap: AccessPoint, band: str | None, ts: float) -> None:
              if dev.ap_ip and dev.ap_ip != ap.ip and (ts - dev.located_at <= self.cfg.roam_window_s):
                  dev.last_moved = ts
                  dev.roam_count += 1
              if dev.ap_ip != ap.ip or (band and band != dev.band):
                  dev.signal_pct = dev.rssi = dev.signal_at = dev.distance_m = None
                  dev.distance_is_upper_bound = False
              dev.ap_ip = ap.ip
              if band:
                  dev.band = band
              dev.located_at = ts
      - id: Tracker.apply_sample
        type: FunctionDef
        code: |-
          def _apply_sample(self, dev: Device, ap: AccessPoint, s: ClientSample, ts: float) -> None:
              cfg = self.cfg
              pct = s.signal_pct if s.signal_pct and s.signal_pct > 0 else None
              if dev.connected and dev.ap_ip == ap.ip and (s.band is None or s.band == dev.band) and (pct is not None) and (dev.signal_pct is not None) and (dev.signal_at is not None) and (ts - dev.signal_at <= cfg.signal_window_s) and (abs(pct - dev.signal_pct) >= cfg.signal_move_delta):
                  dev.last_moved = ts
              dev.seen_on_ap = True
              self._locate(dev, ap, s.band, ts)
              dev.connected = True
              dev.disconnected_at = None
              dev.signal_pct, dev.rssi = (pct, s.rssi)
              dev.signal_at = ts if pct is not None else None
              dev.distance_m, dev.distance_is_upper_bound = (None, False)
              if pct is not None:
                  metres, saturated = estimate_distance(pct, dev.band == '5G', cfg.tx_power_dbm, cfg.path_loss_exponent)
                  dev.distance_m = None if metres is None else round(metres, 1)
                  dev.distance_is_upper_bound = saturated
              if s.standard:
                  dev.wifi_standard = s.standard
              if s.link_rate_mbps:
                  dev.link_rate_mbps = s.link_rate_mbps
              if s.ip and s.ip != '0.0.0.0':
                  dev.ip = s.ip
              if s.tx_bytes is not None and s.rx_bytes is not None:
                  total = s.tx_bytes + s.rx_bytes
                  if dev.traffic_total is not None and total - dev.traffic_total >= cfg.activity_min_bytes:
                      dev.last_active = ts
                  dev.traffic_total = total
```
/answer 6f24-9c-9b allow
ReasoningToken: 242
Control Request:
```yaml
id: 6f24-9d-0
toolName: ast_edit_block
arguments:
  items:
  - path: /home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/tracking/tracker.py
    id: Tracker.render
    old_text: interface = (mapping.interface if mapping else None) or ('wlan' if d.seen_on_ap else 'lan' if d.seen_dhcp else None)
    new_text: |-
      wifi_mapped = mapping is not None and (mapping.interface or '').lower() == 'wlan'
          interface = 'wlan' if wifi_mapped or d.seen_on_ap else 'lan'
  reason: "Default LAN, WLAN via mapping or AP confirmation"
```
/answer 6f24-9d-0 allow
Result Stats: id=5656bb55-7d91-408a-af7f-f114db7ec40b, total: 13414, in: 8, out: 1561, reason: 58, read: 25308, write: 11845, start: 1794147889213, end: 1794147894503, time: 5229, total: 23923, io: 0, control: 61, sent: 0, recv: 110
ReasoningToken: 58
Ich habe die Ermittlung des Interface in `Tracker._render` in `tracker.py` geändert. Getestet habe ich die Änderung nicht.

Die neue Regel:
- **Standard:** Jedes Gerät gilt als `lan`.
- **Config-Mapping:** Ist dort `wlan` eingetragen, ist das Gerät `wlan`.
- **AP-Bestätigung:** Sobald eine Syslog-Station-Meldung oder ein SNMP-Client-Table-Eintrag (`seen_on_ap`) vom WLAN-AP eingeht, wechselt das Gerät auf `wlan`. Das gilt auch für Geräte, die im Mapping als `lan` stehen.

Vorher hatte ein Mapping immer Vorrang, und ohne Mapping war das Interface `None`, solange das Gerät weder auf einem AP noch per DHCP gesehen wurde. `None` kommt jetzt nicht mehr vor. Der Zweig `connected = None` im selben Code ist damit toter Code, ich habe ihn aber stehen lassen.

Ein Leave-Event vom AP setzt `seen_on_ap` ebenfalls (das macht `on_station` bereits so). Ein Gerät, das einmal vom AP gemeldet wurde, bleibt deshalb `wlan`, auch nach dem Disconnect.
