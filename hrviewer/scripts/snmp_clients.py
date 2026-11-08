#!/usr/bin/env python3
"""One-off read of the wireless client table of a DAP-2610 (dot11ClientInformationTable).

Triggers dot11ClientInformationRefresh per band (SNMP SET, needs the write community), then walks
dot11GetClientInformationTable and dot11ClientInformationTable.
Writes <out-dir>/<host>_clients_<timestamp>.json and prints a table.
"""
import argparse
import json
import math
import random
import socket
from datetime import datetime
from pathlib import Path

from ap_monitor import SCRIPT_DIR
from snmp_poll import SnmpError, enc_int, enc_oid, parse_response, tlv, walk

BASE = "1.3.6.1.4.1.171.10.37.59.2.1.3.3.4"
SUMMARY = f"{BASE}.1.1"
CLIENTS = f"{BASE}.2.1"

SUMMARY_COLUMNS = {1: "refresh", 2: "numberOfClients"}
CLIENT_COLUMNS = {
    1: "index", 2: "mac", 3: "band", 4: "authentication", 5: "rssi", 6: "psm", 7: "ssid",
    10: "ip", 11: "txBytes", 12: "rxBytes", 13: "txRate", 14: "signalStrength",
    15: "ssidNumber", 26: "systemInfo",
}
ENUMS = {
    "band": {0: "11a", 1: "11b", 2: "11g", 3: "11n", 4: "11ac?"},
    "authentication": {1: "opensystem", 2: "sharedkey", 3: "opensystem-sharedkey", 4: "wpa-psk",
                       5: "wpa-eap", 6: "wpa2-psk", 7: "wpa2-eap", 8: "wpa2-auto-psk",
                       9: "wpa2-auto-eap", 10: "dot1x", 11: "wep"},
    "psm": {0: "off", 1: "on"},
}
REFRESH_GET = 1
FREQ_MHZ = {"2.4": 2437, "5": 5500}
BANDS_5GHZ = {0, 4}


def estimate_distance(percent, band_code, tx_dbm, exponent):
    """Log-distance path loss; percent is mapped linearly to -100..-50 dBm. Returns (metres, saturated)."""
    if not isinstance(percent, int) or percent <= 0:
        return None, False
    rssi_dbm = percent / 2 - 100
    freq = FREQ_MHZ["5" if band_code in BANDS_5GHZ else "2.4"]
    loss_1m = 20 * math.log10(freq) - 27.55
    metres = 10 ** ((tx_dbm - loss_1m - rssi_dbm) / (10 * exponent))
    return metres, percent >= 100


def set_int(sock, host, community, oid, value, retries=2):
    reqid = random.getrandbits(30)
    varbind = tlv(0x30, enc_oid(oid) + enc_int(value))
    pdu = tlv(0xA3, enc_int(reqid) + enc_int(0) + enc_int(0) + tlv(0x30, varbind))
    packet = tlv(0x30, enc_int(1) + tlv(0x04, community.encode()) + pdu)
    for _ in range(retries + 1):
        sock.sendto(packet, (host, 161))
        try:
            while True:
                data, addr = sock.recvfrom(65535)
                if addr[0] != host:
                    continue
                rid, err, _ = parse_response(data)
                if rid == reqid:
                    if err:
                        raise SnmpError(f"error-status {err}")
                    return
        except socket.timeout:
            continue
    raise SnmpError("timeout")


def split_entries(entries, base, columns):
    rows = {}
    for oid, value in entries:
        column, *index = oid[len(base) + 1:].split(".")
        name = columns.get(int(column), f"col{column}")
        rows.setdefault(".".join(index), {})[name] = value
    return rows


def fmt(name, value):
    if name == "mac" and isinstance(value, str) and value.startswith("0x"):
        return ":".join(value[i:i + 2] for i in range(2, len(value), 2))
    if isinstance(value, (bytes, bytearray)):
        return ":".join(f"{b:02x}" for b in value) if name in ("mac", "systemInfo") else value.decode(errors="replace")
    return ENUMS.get(name, {}).get(value, value)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("host", nargs="?", default="192.168.1.251")
    ap.add_argument("--community", default="public")
    ap.add_argument("--write-community", default="private")
    ap.add_argument("--no-refresh", action="store_true", help="skip the refresh SET")
    ap.add_argument("--tx-power", type=float, default=15.0, help="assumed client EIRP in dBm")
    ap.add_argument("--exponent", type=float, default=3.0, help="path loss exponent (2 free space, 3-4 indoor)")
    ap.add_argument("--timeout", type=float, default=3.0)
    ap.add_argument("--out-dir", default=str(SCRIPT_DIR / "dumps"))
    args = ap.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(args.timeout)
    try:
        bands = sorted({idx for idx in split_entries(walk(sock, args.host, args.community, SUMMARY),
                                                      SUMMARY, SUMMARY_COLUMNS)})
        if not args.no_refresh:
            for band in bands:
                try:
                    set_int(sock, args.host, args.write_community, f"{SUMMARY}.1.{band}", REFRESH_GET)
                except SnmpError as exc:
                    print(f"band {band}: refresh failed ({exc}), using cached table")
        summary = split_entries(walk(sock, args.host, args.community, SUMMARY), SUMMARY, SUMMARY_COLUMNS)
        clients = split_entries(walk(sock, args.host, args.community, CLIENTS, max_rep=25, limit=100_000),
                                CLIENTS, CLIENT_COLUMNS)
    except SnmpError as exc:
        raise SystemExit(f"{args.host}: {exc}")
    finally:
        sock.close()

    for row in clients.values():
        metres, saturated = estimate_distance(row.get("signalStrength"), row.get("band"),
                                              args.tx_power, args.exponent)
        row["distanceM"] = None if metres is None else round(metres, 1)
        row["distanceIsUpperBound"] = saturated

    result = {
        "host": args.host,
        "ts": datetime.now().astimezone().isoformat(),
        "bands": {band: {k: fmt(k, v) for k, v in row.items()} for band, row in summary.items()},
        "clients": {idx: {k: fmt(k, v) for k, v in row.items()} for idx, row in clients.items()},
    }

    for band, row in result["bands"].items():
        print(f"band {band}: {row.get('numberOfClients')} clients")
    for idx, row in result["clients"].items():
        dist = row.get("distanceM")
        dist = "n/a" if dist is None else f"{'<' if row['distanceIsUpperBound'] else '~'}{dist}m"
        print(f"{dist:>8} ", end="")
        print(f"{idx:>5}  {row.get('mac')}  {row.get('ip')}  {row.get('ssid')}  {row.get('band')}  "
              f"rssi={row.get('rssi')} sig={row.get('signalStrength')}% rate={row.get('txRate')}  "
              f"tx={row.get('txBytes')} rx={row.get('rxBytes')}  {row.get('authentication')}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{args.host}_clients_{datetime.now():%Y%m%d_%H%M%S}.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
