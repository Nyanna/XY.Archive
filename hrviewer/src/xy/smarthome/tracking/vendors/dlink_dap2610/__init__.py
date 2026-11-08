"""D-Link DAP-2610: syslog server and SNMP client table polling."""
from __future__ import annotations
from .snmp import DapSnmpPoller
from .syslog import DapSyslogServer, parse_syslog
__all__ = ['DapSnmpPoller', 'DapSyslogServer', 'create_workers', 'parse_syslog']

def create_workers(tracker) -> list:
    cfg = tracker.cfg
    workers: list = []
    if cfg.syslog_enabled:
        workers.append(DapSyslogServer(tracker, cfg.syslog_bind, cfg.syslog_port))
    if cfg.snmp_enabled:
        workers.append(DapSnmpPoller(tracker))
    return workers