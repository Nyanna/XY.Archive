"""Minimal SNMPv2c client (GETBULK walk, integer SET) over UDP."""
from __future__ import annotations
import random
import socket
_TAG_INT, _TAG_OCTETS, _TAG_NULL, _TAG_OID, _TAG_SEQ = (2, 4, 5, 6, 48)
_TAG_SET, _TAG_BULK, _TAG_RESPONSE = (163, 165, 162)
'# noSuchObject, noSuchInstance, endOfMibView'
_EXCEPTIONS = (128, 129, 130)

class SnmpError(Exception):
    pass

def _length(n: int) -> bytes:
    if n < 128:
        return bytes([n])
    raw = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return bytes([128 | len(raw)]) + raw

def tlv(tag: int, body: bytes) -> bytes:
    return bytes([tag]) + _length(len(body)) + body

def enc_int(value: int) -> bytes:
    size = max(1, (value.bit_length() + 8) // 8)
    return tlv(_TAG_INT, value.to_bytes(size, 'big', signed=True))

def enc_oid(oid: str) -> bytes:
    arcs = [int(a) for a in oid.strip('.').split('.')]
    body = bytearray([arcs[0] * 40 + arcs[1]])
    for arc in arcs[2:]:
        chunk = [arc & 127]
        arc >>= 7
        while arc:
            chunk.append(128 | arc & 127)
            arc >>= 7
        body.extend(reversed(chunk))
    return tlv(_TAG_OID, bytes(body))

def ber_read(data: bytes, pos: int) -> tuple[int, bytes, int]:
    tag = data[pos]
    first = data[pos + 1]
    if first < 128:
        length, start = (first, pos + 2)
    else:
        n = first & 127
        length = int.from_bytes(data[pos + 2:pos + 2 + n], 'big')
        start = pos + 2 + n
    end = start + length
    if end > len(data):
        raise ValueError('truncated BER element')
    return (tag, data[start:end], end)

def ber_children(value: bytes) -> list[tuple[int, bytes]]:
    pos, items = (0, [])
    while pos < len(value):
        tag, body, pos = ber_read(value, pos)
        items.append((tag, body))
    return items

def decode_oid(body: bytes) -> str:
    if not body:
        return ''
    first = body[0]
    arcs = [first // 40, first % 40] if first < 80 else [2, first - 80]
    acc = 0
    for b in body[1:]:
        acc = acc << 7 | b & 127
        if not b & 128:
            arcs.append(acc)
            acc = 0
    return '.'.join(map(str, arcs))
_END = object()

def decode_value(tag: int, body: bytes):
    """INTEGER/counters -> int, OCTET STRING -> bytes, OID/IpAddress -> str."""
    if tag == _TAG_INT:
        return int.from_bytes(body, 'big', signed=True)
    if tag == _TAG_OCTETS:
        return bytes(body)
    if tag == _TAG_NULL:
        return None
    if tag == _TAG_OID:
        return decode_oid(body)
    if tag == 64 and len(body) == 4:
        return socket.inet_ntoa(body)
    if tag in (65, 66, 67, 70):
        return int.from_bytes(body, 'big')
    if tag in _EXCEPTIONS:
        return _END
    return bytes(body)

def parse_response(data: bytes) -> tuple[int, int, list[tuple[str, object]]]:
    _, msg, _ = ber_read(data, 0)
    parts = ber_children(msg)
    tag, pdu = parts[2]
    if tag != _TAG_RESPONSE:
        raise ValueError('not a response PDU')
    fields = ber_children(pdu)
    varbinds = []
    for _, vb in ber_children(fields[3][1]):
        oid, val = ber_children(vb)[:2]
        varbinds.append((decode_oid(oid[1]), decode_value(*val)))
    return (decode_value(*fields[0]), decode_value(*fields[1]), varbinds)

class SnmpClient:

    def __init__(self, host: str, community: str='public', port: int=161, timeout: float=3.0, retries: int=2) -> None:
        self.host, self.community, self.port, self.retries = (host, community, port, retries)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(timeout)

    def __enter__(self) -> 'SnmpClient':
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        self._sock.close()

    def _exchange(self, pdu_tag: int, community: str, a: int, b: int, varbind: bytes):
        reqid = random.getrandbits(30)
        body = enc_int(reqid) + enc_int(a) + enc_int(b) + tlv(_TAG_SEQ, tlv(_TAG_SEQ, varbind))
        packet = tlv(_TAG_SEQ, enc_int(1) + tlv(_TAG_OCTETS, community.encode()) + tlv(pdu_tag, body))
        for _ in range(self.retries + 1):
            self._sock.sendto(packet, (self.host, self.port))
            try:
                while True:
                    data, addr = self._sock.recvfrom(65535)
                    if addr[0] != self.host:
                        continue
                    try:
                        rid, err, varbinds = parse_response(data)
                    except (ValueError, IndexError):
                        continue
                    if rid != reqid:
                        continue
                    if err:
                        raise SnmpError(f'error-status {err}')
                    return varbinds
            except socket.timeout:
                continue
        raise SnmpError(f'{self.host}: timeout')

    def set_int(self, oid: str, value: int, community: str | None=None) -> None:
        self._exchange(_TAG_SET, community or self.community, 0, 0, enc_oid(oid) + enc_int(value))

    def walk(self, base: str, max_rep: int=25, limit: int=100000) -> list[tuple[str, object]]:
        out: list[tuple[str, object]] = []
        cursor, prefix = (base, base + '.')
        while len(out) < limit:
            varbinds = self._exchange(_TAG_BULK, self.community, 0, max_rep, enc_oid(cursor) + tlv(_TAG_NULL, b''))
            if not varbinds:
                break
            finished = False
            for oid, value in varbinds:
                if value is _END or not oid.startswith(prefix):
                    finished = True
                    break
                out.append((oid, value))
                cursor = oid
            if finished:
                break
        return out