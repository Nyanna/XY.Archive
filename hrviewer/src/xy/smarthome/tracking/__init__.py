"""Tracking of LAN/WLAN devices by access point cell, signal strength and activity.

Sources: DHCP broadcasts, AP syslog and SNMP client tables. State is kept in
memory only. Started by the SmartHome engine; served via ``/api/smarthome/devices``.
"""
from __future__ import annotations
from .config import TrackingConfig
from .tracker import Tracker
__all__ = ['Tracker', 'TrackingConfig']