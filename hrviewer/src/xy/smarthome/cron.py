"""A tiny, dependency-free 5-field cron matcher.

Supports the subset needed by the SmartHome schedules (and a bit more):
``*``, single values, comma lists, ``a-b`` ranges and ``*/n`` / ``a-b/n``
steps, across the five standard fields::

    minute hour day-of-month month day-of-week
     0-59   0-23    1-31       1-12      0-6   (0 or 7 == Sunday)

Only minute-resolution matching is needed; the scheduler ticks once per
minute and asks :func:`matches` whether a given local ``datetime`` is due.
"""
from __future__ import annotations

from datetime import datetime

_RANGES = {
    "minute": (0, 59),
    "hour": (0, 23),
    "dom": (1, 31),
    "month": (1, 12),
    "dow": (0, 6),
}


def _parse_field(spec: str, lo: int, hi: int) -> set[int]:
    values: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        step = 1
        if "/" in part:
            base, step_s = part.split("/", 1)
            step = int(step_s)
        else:
            base = part
        if base == "*" or base == "":
            start, end = lo, hi
        elif "-" in base:
            a, b = base.split("-", 1)
            start, end = int(a), int(b)
        else:
            start = end = int(base)
        for v in range(start, end + 1, step):
            values.add(v)
    return values


class CronSpec:
    """A parsed cron expression, ready to be matched against datetimes."""

    def __init__(self, expr: str):
        self.expr = expr.strip()
        fields = self.expr.split()
        if len(fields) != 5:
            raise ValueError(f"cron must have 5 fields, got {len(fields)}: {expr!r}")
        self.minute = _parse_field(fields[0], *_RANGES["minute"])
        self.hour = _parse_field(fields[1], *_RANGES["hour"])
        self.dom = _parse_field(fields[2], *_RANGES["dom"])
        self.month = _parse_field(fields[3], *_RANGES["month"])
        # day-of-week: normalise a lone 7 to 0 (Sunday)
        self.dow = {d % 7 for d in _parse_field(fields[4], 0, 7)}
        self._dom_restricted = fields[2].strip() != "*"
        self._dow_restricted = fields[4].strip() != "*"

    def matches(self, now: datetime) -> bool:
        if now.minute not in self.minute:
            return False
        if now.hour not in self.hour:
            return False
        if now.month not in self.month:
            return False
        # Standard cron OR-semantics between DOM and DOW when both restricted.
        dom_ok = now.day in self.dom
        dow_ok = (now.weekday() + 1) % 7 in self.dow  # Python Mon=0 -> cron Sun=0
        if self._dom_restricted and self._dow_restricted:
            return dom_ok or dow_ok
        return dom_ok and dow_ok
