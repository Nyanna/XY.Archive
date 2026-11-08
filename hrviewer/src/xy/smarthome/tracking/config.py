"""Configuration of the device tracker (JSON file + a few env overrides)."""
from __future__ import annotations
import json
import os
from dataclasses import dataclass, field, fields
from .model import AccessPoint, Mapping, norm_mac

def _default_aps() -> list[AccessPoint]:
    return [AccessPoint(ip=f'192.168.1.{n}') for n in range(251, 255)]

@dataclass
class TrackingConfig:
    access_points: list[AccessPoint] = field(default_factory=_default_aps)
    mappings: dict[str, Mapping] = field(default_factory=dict)
    dhcp_enabled: bool = True
    dhcp_iface: str | None = None
    lan_connected_s: float = 8 * 3600.0
    syslog_enabled: bool = True
    syslog_bind: str = '0.0.0.0'
    syslog_port: int = 514
    snmp_enabled: bool = True
    '# default: IPs of access_points'
    snmp_hosts: list[str] | None = None
    snmp_community: str = 'public'
    snmp_write_community: str = 'private'
    snmp_interval_s: float = 60.0
    snmp_timeout_s: float = 3.0
    '# dot11bandIndex values of the 5 GHz radio (decides a/n ambiguity)'
    band_index_5ghz: tuple[int, ...] = (2,)
    retention_s: float = 28 * 86400
    tx_power_dbm: float = 15.0
    path_loss_exponent: float = 3.0
    moving_s: float = 120.0
    recent_move_s: float = 900.0
    roam_window_s: float = 900.0
    signal_window_s: float = 150.0
    signal_move_delta: int = 12
    activity_min_bytes: int = 2048

    @property
    def snmp_targets(self) -> list[str]:
        return list(self.snmp_hosts) if self.snmp_hosts else [ap.ip for ap in self.access_points]

    @property
    def stale_s(self) -> float:
        return self.snmp_interval_s * 1.5

    @classmethod
    def from_dict(cls, data: dict) -> 'TrackingConfig':
        data = dict(data)
        aps = data.pop('access_points', None)
        maps = data.pop('mappings', None) or {}
        unknown = set(data) - {f.name for f in fields(cls)}
        if unknown:
            raise ValueError(f'unknown config keys: {sorted(unknown)}')
        cfg = cls(**data)
        cfg.band_index_5ghz = tuple(cfg.band_index_5ghz)
        if aps is not None:
            cfg.access_points = [_parse_ap(a) for a in aps]
        for raw_mac, entry in maps.items():
            mac = norm_mac(raw_mac)
            if mac is None:
                raise ValueError(f'invalid MAC in mappings: {raw_mac!r}')
            cfg.mappings[mac] = _parse_mapping(entry)
        return cfg

    @classmethod
    def from_file(cls, path: str) -> 'TrackingConfig':
        with open(path, encoding='utf-8') as fh:
            return cls.from_dict(json.load(fh))

    @classmethod
    def from_env(cls) -> 'TrackingConfig':
        path = os.environ.get('SMH_TRACK_CONFIG')
        cfg = cls.from_file(path) if path else cls()
        if os.environ.get('SMH_TRACK_DHCP_IFACE'):
            cfg.dhcp_iface = os.environ['SMH_TRACK_DHCP_IFACE']
        if os.environ.get('SMH_TRACK_SYSLOG_PORT'):
            cfg.syslog_port = int(os.environ['SMH_TRACK_SYSLOG_PORT'])
        return cfg

def _parse_ap(entry: dict) -> AccessPoint:
    mac = entry.get('mac')
    if mac is not None and norm_mac(mac) is None:
        raise ValueError(f'invalid AP MAC: {mac!r}')
    return AccessPoint(
        ip=entry['ip'],
        mac=norm_mac(mac) if mac else None,
        name=entry.get('name'),
        floor=entry.get('floor'),
        room=entry.get('room'))

def _parse_mapping(entry: dict) -> Mapping:
    kind = entry.get('type', 'device')
    interface = entry.get('interface')
    if kind not in ('ap', 'device'):
        raise ValueError(f"mapping type must be 'ap' or 'device', got {kind!r}")
    if interface not in (None, 'wlan', 'lan'):
        raise ValueError(f"mapping interface must be 'wlan' or 'lan', got {interface!r}")
    return Mapping(kind=kind, interface=interface, name=entry.get('name'), owner=entry.get('owner'))