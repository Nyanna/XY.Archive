"""DHCP broadcast listener (raw packet socket, needs CAP_NET_RAW)."""
from __future__ import annotations
import logging
import socket
import struct
from .model import norm_mac
from .worker import Worker
log = logging.getLogger(__name__)
_ETH_P_IP = 2048
_VLAN_TYPES = (33024, 34984)
_MAGIC_COOKIE = b'c\x82Sc'
_TYPES = {1: 'DISCOVER', 2: 'OFFER', 3: 'REQUEST', 4: 'DECLINE', 5: 'ACK', 6: 'NAK', 7: 'RELEASE', 8: 'INFORM'}

def parse_dhcp(p: bytes) -> dict:
    if len(p) < 240 or p[236:240] != _MAGIC_COOKIE:
        raise ValueError('not a DHCP packet')
    hlen = min(p[2], 16)
    info = {'op': 'request' if p[0] == 1 else 'reply', 'ciaddr': socket.inet_ntoa(
        p[12:16]), 'yiaddr': socket.inet_ntoa(p[16:20]), 'chaddr': p[28:28 + hlen]}
    pos = 240
    while pos < len(p):
        code = p[pos]
        if code == 255:
            break
        if code == 0:
            pos += 1
            continue
        if pos + 1 >= len(p):
            break
        ln = p[pos + 1]
        val = p[pos + 2:pos + 2 + ln]
        pos += 2 + ln
        if code == 53 and val:
            info['msg_type'] = _TYPES.get(val[0])
        elif code == 12:
            info['hostname'] = val.rstrip(b'\x00').decode('utf-8', 'replace')
        elif code == 50 and len(val) == 4:
            info['requested_ip'] = socket.inet_ntoa(val)
    return info

def parse_frame(f: bytes) -> dict | None:
    """DHCP payload of an Ethernet frame, or ``None`` if it is not DHCP."""
    if len(f) < 14:
        return None
    eth_type, off = (struct.unpack('!H', f[12:14])[0], 14)
    while eth_type in _VLAN_TYPES and len(f) >= off + 4:
        eth_type = struct.unpack('!H', f[off + 2:off + 4])[0]
        off += 4
    if eth_type != _ETH_P_IP or len(f) < off + 20 or f[off + 9] != 17:
        return None
    udp = off + (f[off] & 15) * 4
    if len(f) < udp + 8:
        return None
    sport, dport = struct.unpack('!HH', f[udp:udp + 4])
    if sport not in (67, 68) or dport not in (67, 68):
        return None
    return parse_dhcp(f[udp + 8:])

class DhcpListener(Worker):
    name = 'tracking-dhcp'

    def __init__(self, tracker, iface: str | None=None) -> None:
        super().__init__()
        self._tracker = tracker
        self._iface = iface

    def run(self) -> None:
        try:
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(_ETH_P_IP))
            if self._iface:
                sock.bind((self._iface, 0))
        except (AttributeError, OSError) as exc:
            log.error('DHCP listener disabled (needs Linux + CAP_NET_RAW): %s', exc)
            return
        sock.settimeout(1.0)
        with sock:
            while not self._stop.is_set():
                try:
                    frame = sock.recv(65535)
                except socket.timeout:
                    continue
                except OSError:
                    break
                try:
                    info = parse_frame(frame)
                    if info:
                        self._handle(info)
                except Exception:
                    log.debug('bad DHCP frame', exc_info=True)

    def _handle(self, info: dict) -> None:
        mac = norm_mac(info['chaddr'])
        if mac is None:
            return
        msg = info.get('msg_type')
        if info['op'] == 'request' and msg in ('DISCOVER', 'REQUEST', 'INFORM'):
            renewing = info['ciaddr'] != '0.0.0.0'
            ip = info['ciaddr'] if renewing else info.get('requested_ip')
            self._tracker.on_dhcp(mac, info.get('hostname'), ip, confirmed=renewing)
        elif info['op'] == 'reply' and msg == 'ACK' and (info['yiaddr'] != '0.0.0.0'):
            self._tracker.on_dhcp(mac, None, info['yiaddr'], confirmed=True)