"""Data model of the device tracker."""
from __future__ import annotations
import re
from dataclasses import dataclass
_NON_HEX = re.compile('[^0-9a-f]')

def norm_mac(value) -> str | None:
    """Lower-case colon separated MAC, or ``None`` if ``value`` is not a MAC."""
    if isinstance(value, (bytes, bytearray)):
        digits = bytes(value).hex()
    else:
        digits = _NON_HEX.sub('', str(value).lower())
    if len(digits) != 12:
        return None
    return ':'.join((digits[i:i + 2] for i in range(0, 12, 2)))

@dataclass
class AccessPoint:
    ip: str
    mac: str | None = None
    name: str | None = None
    floor: str | None = None
    room: str | None = None

@dataclass
class Mapping:
    """Configured identity of a MAC address."""
    '# "ap" | "device"'
    kind: str = 'device'
    '# "wlan" | "lan"'
    interface: str | None = None
    name: str | None = None
    owner: str | None = None

@dataclass
class StationEvent:
    """Vendor independent event about a station at an access point.

    kind: ``join`` (association), ``seen`` (presence proof), ``active``
    (presence + activity, e.g. IP assignment), ``leave``.
    """
    ap_ip: str
    mac: str
    kind: str
    ap_mac: str | None = None
    '# "2.4G" | "5G"'
    band: str | None = None
    ip: str | None = None
    ts: float | None = None

@dataclass
class ClientSample:
    """One row of an access point's client table."""
    mac: str
    band: str | None = None
    standard: str | None = None
    signal_pct: int | None = None
    rssi: int | None = None
    ip: str | None = None
    tx_bytes: int | None = None
    rx_bytes: int | None = None
    link_rate_mbps: int | None = None

@dataclass
class Device:
    mac: str
    first_seen: float
    last_seen: float
    hostname: str | None = None
    ip: str | None = None
    seen_on_ap: bool = False
    seen_dhcp: bool = False
    last_dhcp: float | None = None
    connected: bool = False
    disconnected_at: float | None = None
    last_active: float | None = None
    '# last known location'
    ap_ip: str | None = None
    located_at: float = 0.0
    band: str | None = None
    signal_pct: int | None = None
    rssi: int | None = None
    signal_at: float | None = None
    distance_m: float | None = None
    distance_is_upper_bound: bool = False
    wifi_standard: str | None = None
    link_rate_mbps: int | None = None
    traffic_total: int | None = None
    '# movement'
    last_moved: float | None = None
    roam_count: int = 0