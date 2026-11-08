"""Syslog parsing and UDP server for DAP-2610 access points."""
from __future__ import annotations
import logging
import re
import socket
from ...model import StationEvent, norm_mac
from ...worker import Worker
log = logging.getLogger(__name__)
_HEADER = re.compile(
    '^<\\d+>\\[(?P<ap_mac>[0-9a-f:]{17})\\]\\[(?P<ap_ip>[\\d.]+)\\]\\[\\d+\\]\\s*(?P<body>.*)$',
    re.IGNORECASE | re.DOTALL)
_STA = re.compile('\\bSTA\\s+(?P<mac>[0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)
_BAND = re.compile('\\b(2\\.4G|5G)\\b', re.IGNORECASE)
_ASSIGN = re.compile('assign IP (?P<ip>\\d+\\.\\d+\\.\\d+\\.\\d+) TO Mac:(?P<mac>[0-9a-f:]{17})', re.IGNORECASE)
_LEAVE = ('deauth', 'disassociate', 'kickout')
_JOIN = ('association success', '4-way handshake success')
_SEEN = ('group key update', '4-way handshake start')

def parse_syslog(message: str, src_ip: str, ts: float | None=None) -> StationEvent | None:
    header = _HEADER.match(message.strip())
    if header:
        ap_ip, ap_mac, body = (header['ap_ip'], norm_mac(header['ap_mac']), header['body'])
    else:
        ap_ip, ap_mac, body = (src_ip, None, message)
    band_match = _BAND.search(body)
    band = band_match[1].upper() if band_match else None
    assign = _ASSIGN.search(body)
    if assign:
        mac = norm_mac(assign['mac'])
        return mac and StationEvent(ap_ip, mac, 'active', ap_mac, band, assign['ip'], ts)
    sta = _STA.search(body)
    mac = norm_mac(sta['mac']) if sta else None
    if mac is None:
        return None
    text = body.lower()
    if any((k in text for k in _LEAVE)):
        kind = 'leave'
    elif any((k in text for k in _JOIN)):
        kind = 'join'
    elif any((k in text for k in _SEEN)):
        kind = 'seen'
    else:
        return None
    return StationEvent(ap_ip, mac, kind, ap_mac, band, None, ts)

class DapSyslogServer(Worker):
    name = 'tracking-syslog'

    def __init__(self, tracker, bind: str='0.0.0.0', port: int=514) -> None:
        super().__init__()
        self._tracker = tracker
        self._addr = (bind, port)

    def run(self) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(self._addr)
        except OSError as exc:
            log.error('syslog server disabled, cannot bind %s:%d: %s', *self._addr, exc)
            return
        sock.settimeout(1.0)
        with sock:
            while not self._stop.is_set():
                try:
                    data, addr = sock.recvfrom(65535)
                except socket.timeout:
                    continue
                except OSError:
                    break
                try:
                    message = data.decode('utf-8', 'replace').rstrip('\x00\n')
                    event = parse_syslog(message, addr[0])
                    if event:
                        self._tracker.on_station(event)
                except Exception:
                    log.debug('bad syslog message', exc_info=True)