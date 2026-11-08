"""In-memory device tracker: merges DHCP, syslog and SNMP observations."""
from __future__ import annotations
import threading
import time
from dataclasses import replace
from datetime import datetime, timezone
from .config import TrackingConfig
from .distance import estimate_distance
from .model import AccessPoint, ClientSample, Device, StationEvent
from .worker import Worker
_PRUNE_INTERVAL_S = 3600

def _iso(ts: float | None) -> str | None:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec='seconds')

class Tracker:

    def __init__(self, cfg: TrackingConfig | None=None, clock=time.time) -> None:
        self.cfg = cfg or TrackingConfig()
        self._clock = clock
        self._lock = threading.RLock()
        self._devices: dict[str, Device] = {}
        self._aps: dict[str, AccessPoint] = {}
        self._ap_by_mac: dict[str, AccessPoint] = {}
        self._ignored: set[str] = {m for m, v in self.cfg.mappings.items() if v.kind == 'ap'}
        self._last_prune = clock()
        self._workers: list[Worker] = []
        for ap in self.cfg.access_points:
            self._register_ap(replace(ap))
    '# -- lifecycle ---------------------------------------------------------'

    def start(self) -> None:
        from .dhcp import DhcpListener
        from .vendors.dlink_dap2610 import create_workers
        workers: list[Worker] = []
        if self.cfg.dhcp_enabled:
            workers.append(DhcpListener(self, self.cfg.dhcp_iface))
        workers.extend(create_workers(self))
        for worker in workers:
            worker.start()
        self._workers = workers

    def stop(self) -> None:
        for worker in self._workers:
            worker.stop()
        self._workers = []
    '# -- observations ------------------------------------------------------'

    def on_dhcp(self, mac: str, hostname: str | None=None, ip: str | None=None, confirmed: bool=False, ts: float | None=None) -> None:
        ts = self._now(ts)
        with self._lock:
            dev = self._device(mac, ts)
            if dev is None:
                return
            dev.seen_dhcp = True
            dev.last_active = ts
            if hostname:
                dev.hostname = hostname
            if ip and (confirmed or dev.ip is None):
                dev.ip = ip

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
    '# -- query -------------------------------------------------------------'

    def snapshot(self, now: float | None=None) -> dict:
        now = self._now(now)
        with self._lock:
            self._prune(now)
            devices = sorted(self._devices.values(), key=lambda d: -d.last_seen)
            return {
                'generated_at': _iso(now),
                'retention_days': self.cfg.retention_s / 86400,
                'access_points': [
                    self._render_ap(ap) for ap in self._aps.values()],
                'devices': [
                    self._render(
                        d,
                        now) for d in devices]}
    '# -- internals ---------------------------------------------------------'

    def _now(self, ts: float | None=None) -> float:
        return self._clock() if ts is None else ts

    def _register_ap(self, ap: AccessPoint) -> None:
        self._aps[ap.ip] = ap
        if ap.mac:
            self._ap_by_mac[ap.mac] = ap
            self._ignored.add(ap.mac)

    def _ap(self, ip: str | None, mac: str | None) -> AccessPoint:
        ap = self._aps.get(ip) if ip else None
        if ap is None and mac:
            ap = self._ap_by_mac.get(mac)
        if ap is None:
            ap = AccessPoint(ip=ip or mac or 'unknown')
            self._aps[ap.ip] = ap
        if mac and ap.mac is None:
            ap.mac = mac
            self._ap_by_mac[mac] = ap
            self._ignored.add(mac)
            self._devices.pop(mac, None)
        return ap

    def _device(self, mac: str, ts: float) -> Device | None:
        if mac in self._ignored:
            return None
        if ts - self._last_prune > _PRUNE_INTERVAL_S:
            self._prune(ts)
        dev = self._devices.get(mac)
        if dev is None:
            dev = self._devices[mac] = Device(mac=mac, first_seen=ts, last_seen=ts)
        elif ts > dev.last_seen:
            dev.last_seen = ts
        return dev

    def _prune(self, now: float) -> None:
        cutoff = now - self.cfg.retention_s
        for mac in [m for m, d in self._devices.items() if d.last_seen < cutoff]:
            del self._devices[mac]
        self._last_prune = now

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

    @staticmethod
    def _disconnect(dev: Device, ts: float) -> None:
        dev.connected = False
        dev.disconnected_at = ts
        dev.traffic_total = None

    def _render_ap(self, ap: AccessPoint) -> dict:
        return {'ip': ap.ip, 'mac': ap.mac, 'name': ap.name, 'floor': ap.floor, 'room': ap.room}

    def _render(self, d: Device, now: float) -> dict:
        cfg = self.cfg
        mapping = self.cfg.mappings.get(d.mac)
        interface = (mapping.interface if mapping else None) or (
            'wlan' if d.seen_on_ap else 'lan' if d.seen_dhcp else None)
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
        connected = d.connected if interface == 'wlan' else None
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