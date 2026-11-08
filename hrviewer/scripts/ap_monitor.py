#!/usr/bin/env python3
"""Passive collector for AP traffic: SNMP traps (UDP 162), syslog (UDP 514), DHCP (UDP 67/68).

Standard library only. Events are written as JSON lines.
Requires CAP_NET_BIND_SERVICE and CAP_NET_RAW (see run_ap_monitor.sh).
"""
import argparse
import json
import logging
import selectors
import signal
import socket
import struct
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
log = logging.getLogger("apmon")
event_log = logging.getLogger("apmon.events")


def emit(kind, src, **fields):
    event_log.info(json.dumps(
        {"ts": datetime.now(timezone.utc).isoformat(), "type": kind, "src": src, **fields},
        ensure_ascii=False))


# ---------------------------------------------------------------- SNMP (minimal BER)

def ber_read(data, pos):
    tag = data[pos]
    first = data[pos + 1]
    if first < 0x80:
        length, start = first, pos + 2
    else:
        n = first & 0x7F
        length = int.from_bytes(data[pos + 2:pos + 2 + n], "big")
        start = pos + 2 + n
    end = start + length
    if end > len(data):
        raise ValueError("truncated BER element")
    return tag, data[start:end], end


def ber_children(value):
    pos, items = 0, []
    while pos < len(value):
        tag, body, pos = ber_read(value, pos)
        items.append((tag, body))
    return items


def decode_oid(body):
    if not body:
        return ""
    first = body[0]
    arcs = [first // 40, first % 40] if first < 80 else [2, first - 80]
    acc = 0
    for b in body[1:]:
        acc = (acc << 7) | (b & 0x7F)
        if not b & 0x80:
            arcs.append(acc)
            acc = 0
    return ".".join(map(str, arcs))


def decode_value(tag, body):
    if tag == 0x02:
        return int.from_bytes(body, "big", signed=True)
    if tag == 0x04:
        try:
            text = body.decode("utf-8")
            if text.isprintable():
                return text
        except UnicodeDecodeError:
            pass
        return "0x" + body.hex()
    if tag == 0x05:
        return None
    if tag == 0x06:
        return decode_oid(body)
    if tag == 0x40 and len(body) == 4:
        return socket.inet_ntoa(body)
    if tag in (0x41, 0x42, 0x43, 0x46):
        return int.from_bytes(body, "big")
    return "0x" + body.hex()


def decode_varbinds(body):
    out = []
    for _, vb in ber_children(body):
        oid, val = ber_children(vb)[:2]
        out.append({"oid": decode_oid(oid[1]), "value": decode_value(*val)})
    return out


PDU_NAMES = {0xA0: "get", 0xA1: "getnext", 0xA2: "response", 0xA3: "set",
             0xA4: "trap-v1", 0xA5: "getbulk", 0xA6: "inform", 0xA7: "trap-v2"}


def parse_snmp(data):
    _, msg, _ = ber_read(data, 0)
    parts = ber_children(msg)
    version = decode_value(*parts[0])
    result = {"version": {0: "v1", 1: "v2c", 3: "v3"}.get(version, version)}
    if version == 3:
        result["raw_hex"] = data.hex()
        return result
    result["community"] = decode_value(*parts[1])
    ptag, pbody = parts[2]
    result["pdu"] = PDU_NAMES.get(ptag, hex(ptag))
    f = ber_children(pbody)
    if ptag == 0xA4:
        result.update(enterprise=decode_oid(f[0][1]), agent_addr=decode_value(*f[1]),
                      generic_trap=decode_value(*f[2]), specific_trap=decode_value(*f[3]),
                      uptime_ticks=decode_value(*f[4]), varbinds=decode_varbinds(f[5][1]))
    else:
        result.update(request_id=decode_value(*f[0]), varbinds=decode_varbinds(f[3][1]))
    return result


# ---------------------------------------------------------------- DHCP

DHCP_TYPES = {1: "DISCOVER", 2: "OFFER", 3: "REQUEST", 4: "DECLINE", 5: "ACK",
              6: "NAK", 7: "RELEASE", 8: "INFORM"}


def mac(raw):
    return ":".join(f"{b:02x}" for b in raw)


def parse_dhcp(p):
    if len(p) < 240 or p[236:240] != b"\x63\x82\x53\x63":
        raise ValueError("not a DHCP packet")
    hlen = min(p[2], 16)
    info = {
        "op": "request" if p[0] == 1 else "reply",
        "xid": p[4:8].hex(),
        "ciaddr": socket.inet_ntoa(p[12:16]),
        "yiaddr": socket.inet_ntoa(p[16:20]),
        "giaddr": socket.inet_ntoa(p[24:28]),
        "chaddr": mac(p[28:28 + hlen]),
    }
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
            info["msg_type"] = DHCP_TYPES.get(val[0], val[0])
        elif code == 12:
            info["hostname"] = val.decode("utf-8", "replace")
        elif code == 50 and len(val) == 4:
            info["requested_ip"] = socket.inet_ntoa(val)
        elif code == 54 and len(val) == 4:
            info["server_id"] = socket.inet_ntoa(val)
        elif code == 60:
            info["vendor_class"] = val.decode("utf-8", "replace")
        elif code == 61:
            info["client_id"] = val.hex()
        elif code == 55:
            info["param_request_list"] = list(val)
        elif code == 82:
            sub, i = {}, 0
            while i + 1 < len(val):
                sl = val[i + 1]
                sub[{1: "circuit_id", 2: "remote_id"}.get(val[i], f"sub{val[i]}")] = val[i + 2:i + 2 + sl].hex()
                i += 2 + sl
            info["relay_agent"] = sub
    return info


# ---------------------------------------------------------------- Handlers

def handle_datagram(kind, data, addr):
    src = f"{addr[0]}:{addr[1]}"
    try:
        if kind == "snmp_trap":
            emit(kind, src, **parse_snmp(data))
        else:
            emit(kind, src, message=data.decode("utf-8", "replace").rstrip("\x00\n"),
                 raw_hex=None if data.isascii() else data.hex())
    except Exception as exc:
        emit(kind, src, parse_error=str(exc), raw_hex=data.hex())


def handle_frame(f):
    if len(f) < 14:
        return
    eth_type, off = struct.unpack("!H", f[12:14])[0], 14
    while eth_type in (0x8100, 0x88A8) and len(f) >= off + 4:
        eth_type = struct.unpack("!H", f[off + 2:off + 4])[0]
        off += 4
    if eth_type != 0x0800 or len(f) < off + 20 or f[off + 9] != 17:
        return
    udp = off + (f[off] & 0x0F) * 4
    if len(f) < udp + 8:
        return
    sport, dport = struct.unpack("!HH", f[udp:udp + 4])
    if sport not in (67, 68) or dport not in (67, 68):
        return
    src = f"{socket.inet_ntoa(f[off + 12:off + 16])}:{sport}"
    dst = f"{socket.inet_ntoa(f[off + 16:off + 20])}:{dport}"
    try:
        emit("dhcp", src, dst=dst, eth_src=mac(f[6:12]), eth_dst=mac(f[0:6]), **parse_dhcp(f[udp + 8:]))
    except Exception as exc:
        emit("dhcp", src, dst=dst, parse_error=str(exc), raw_hex=f[udp + 8:].hex())


def udp_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.setblocking(False)
    return s


def packet_socket(iface):
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    if iface:
        s.bind((iface, 0))
    s.setblocking(False)
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--iface", help="interface for DHCP capture (default: all)")
    ap.add_argument("--logdir", default=str(SCRIPT_DIR / "logs"))
    ap.add_argument("--trap-port", type=int, default=162)
    ap.add_argument("--syslog-port", type=int, default=514)
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logdir = Path(args.logdir)
    logdir.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(logdir / "ap_traffic.log", maxBytes=50 * 2**20,
                                  backupCount=10, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))
    event_log.addHandler(handler)
    event_log.propagate = False

    try:
        sockets = {
            "snmp_trap": udp_socket(args.trap_port),
            "syslog": udp_socket(args.syslog_port),
            "dhcp": packet_socket(args.iface),
        }
    except PermissionError as exc:
        raise SystemExit(f"Missing capabilities (run via run_ap_monitor.sh): {exc}")
    except OSError as exc:
        raise SystemExit(f"Cannot bind: {exc}")

    sel = selectors.DefaultSelector()
    for kind, s in sockets.items():
        sel.register(s, selectors.EVENT_READ, kind)

    running = True

    def stop(*_):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    log.info("Listening: UDP %d (SNMP trap), UDP %d (syslog), DHCP sniffer on %s",
             args.trap_port, args.syslog_port, args.iface or "all interfaces")

    while running:
        for key, _ in sel.select(timeout=1.0):
            kind = key.data
            try:
                if kind == "dhcp":
                    handle_frame(key.fileobj.recv(65535))
                else:
                    data, addr = key.fileobj.recvfrom(65535)
                    handle_datagram(kind, data, addr)
            except BlockingIOError:
                continue
            except Exception:
                log.exception("error handling %s", kind)

    for s in sockets.values():
        s.close()
    log.info("Stopped")


if __name__ == "__main__":
    main()
