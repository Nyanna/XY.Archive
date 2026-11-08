"""Periodic SNMP polling of the DAP-2610 wireless client table."""
from __future__ import annotations
import logging
import time
from ...model import ClientSample, norm_mac
from ...snmp import SnmpClient, SnmpError
from ...worker import Worker
log = logging.getLogger(__name__)
BASE = '1.3.6.1.4.1.171.10.37.59.2.1.3.3.4'
'# dot11ClientInformationRefresh / number of clients per band'
SUMMARY = f'{BASE}.1.1'
'# dot11ClientInformationEntry'
CLIENTS = f'{BASE}.2.1'
REFRESH_COLUMN, REFRESH_GET = (1, 1)
COL_MAC, COL_BAND, COL_RSSI, COL_IP = (2, 3, 5, 10)
COL_TX_BYTES, COL_RX_BYTES, COL_TX_RATE, COL_SIGNAL = (11, 12, 13, 14)
_STANDARDS = {0: '802.11a', 1: '802.11b', 2: '802.11g', 3: '802.11n', 4: '802.11ac'}
_5GHZ_CODES = (0, 4)
_N_CODE = 3

def _split(entries: list[tuple[str, object]], base: str) -> dict[str, dict[int, object]]:
    """``<base>.<column>.<index...>`` -> ``{index: {column: value}}``."""
    rows: dict[str, dict[int, object]] = {}
    for oid, value in entries:
        column, _, index = oid[len(base) + 1:].partition('.')
        rows.setdefault(index, {})[int(column)] = value
    return rows

def _int(value) -> int | None:
    return value if isinstance(value, int) else None

def parse_clients(rows: dict[str, dict[int, object]], band_index_5ghz: tuple[int, ...]) -> list[ClientSample]:
    samples = []
    for index, row in rows.items():
        mac = norm_mac(row.get(COL_MAC, b''))
        if mac is None:
            continue
        code = _int(row.get(COL_BAND))
        band_idx = int(index.split('.')[0])
        is_5ghz = code in _5GHZ_CODES or (code == _N_CODE and band_idx in band_index_5ghz)
        ip = row.get(COL_IP)
        samples.append(
            ClientSample(
                mac=mac, band='5G' if is_5ghz else '2.4G', standard=_STANDARDS.get(code), signal_pct=_int(
                    row.get(COL_SIGNAL)), rssi=_int(
                        row.get(COL_RSSI)), ip=ip if isinstance(
                            ip, str) else None, tx_bytes=_int(
                                row.get(COL_TX_BYTES)), rx_bytes=_int(
                                    row.get(COL_RX_BYTES)), link_rate_mbps=_int(
                                        row.get(COL_TX_RATE))))
    return samples

class DapSnmpPoller(Worker):
    name = 'tracking-snmp'

    def __init__(self, tracker) -> None:
        super().__init__()
        self._tracker = tracker
        self._cfg = tracker.cfg

    def run(self) -> None:
        while not self._stop.is_set():
            started = time.monotonic()
            for host in self._cfg.snmp_targets:
                if self._stop.is_set():
                    return
                try:
                    self.poll(host)
                except (SnmpError, OSError) as exc:
                    log.warning('SNMP poll of %s failed: %s', host, exc)
            self._stop.wait(max(1.0, self._cfg.snmp_interval_s - (time.monotonic() - started)))

    def poll(self, host: str) -> None:
        cfg = self._cfg
        started = time.time()
        with SnmpClient(host, cfg.snmp_community, timeout=cfg.snmp_timeout_s) as client:
            for band in _split(client.walk(SUMMARY), SUMMARY):
                try:
                    client.set_int(f'{SUMMARY}.{REFRESH_COLUMN}.{band}', REFRESH_GET, cfg.snmp_write_community)
                except SnmpError as exc:
                    log.debug('%s band %s refresh failed (%s), using cached table', host, band, exc)
            self._stop.wait(1.0)
            rows = _split(client.walk(CLIENTS), CLIENTS)
        samples = parse_clients(rows, cfg.band_index_5ghz)
        self._tracker.on_client_table(host, samples, ts=time.time(), started=started)