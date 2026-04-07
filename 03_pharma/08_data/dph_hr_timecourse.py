#!/usr/bin/env python3
"""
DPH Phase A — HR-Zeitverlauf in 30-Minuten-Bins pro Nacht.
Zeigt PRE- und DPH-Nächte im Vergleich.
"""

import sqlite3
import sys
from datetime import datetime, timezone, timedelta
import numpy as np

DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "Gadgetbridge"
CEST = timedelta(hours=2)
DPH_CUTOFF_UTC = datetime(2026, 4, 4, 20, 0).timestamp()
BIN_SIZE = 1800  # 30 min


def local_dt(utc_s):
    return datetime.fromtimestamp(utc_s, tz=timezone.utc) + CEST


def main():
    con = sqlite3.connect(DB_PATH)

    sessions = con.execute(
        "SELECT TIMESTAMP/1000, WAKEUP_TIME/1000 "
        "FROM XIAOMI_SLEEP_TIME_SAMPLE ORDER BY TIMESTAMP"
    ).fetchall()

    for ts, wu in sessions:
        ld = local_dt(ts)
        dur_h = (wu - ts) / 3600
        if ld.year < 2026 or dur_h < 3 or (10 <= ld.hour < 20):
            continue

        tag = "DPH" if ts >= DPH_CUTOFF_UTC else "PRE"
        hrs = con.execute(
            "SELECT TIMESTAMP, HEART_RATE FROM XIAOMI_ACTIVITY_SAMPLE "
            "WHERE TIMESTAMP BETWEEN ? AND ? AND HEART_RATE > 0 AND HEART_RATE < 200 "
            "ORDER BY TIMESTAMP",
            (ts, wu),
        ).fetchall()

        if not hrs:
            continue

        print(f"\n=== {tag} {ld.strftime('%Y-%m-%d %H:%M')} ({dur_h:.1f}h) ===")
        print(f"{'Bin':>7} | {'n':>3} | {'min':>3} | {'mean':>5} | {'max':>3}")
        print("-" * 35)

        for bin_s in range(int(ts), int(wu), BIN_SIZE):
            bh = [h[1] for h in hrs if bin_s <= h[0] < bin_s + BIN_SIZE]
            if bh:
                t = local_dt(bin_s)
                print(
                    f"{t.strftime('%H:%M'):>7} | {len(bh):>3} | {min(bh):>3} | "
                    f"{np.mean(bh):>5.1f} | {max(bh):>3}"
                )

    con.close()


if __name__ == "__main__":
    main()
