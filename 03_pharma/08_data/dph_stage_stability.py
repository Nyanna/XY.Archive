#!/usr/bin/env python3
"""
DPH Phase A — Schlafstadien-Stabilität: Transitions, Episodenzahl, Episodenlänge.
Vergleich first 5h vs. late, PRE vs. DPH.
"""

import sqlite3
import sys
from datetime import datetime, timezone, timedelta
import numpy as np

DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "Gadgetbridge"
CEST = timedelta(hours=2)
DPH_CUTOFF_UTC = datetime(2026, 4, 4, 20, 0).timestamp()
EARLY_HOURS = 5


def local_dt(utc_s):
    return datetime.fromtimestamp(utc_s, tz=timezone.utc) + CEST


def count_transitions(stages):
    """Returns (transitions, episodes, avg_episode_length_min)."""
    if len(stages) < 2:
        return 0, 0, 0.0
    trans = sum(1 for i in range(1, len(stages)) if stages[i][1] != stages[i - 1][1])
    eps = trans + 1
    dur_min = (stages[-1][0] - stages[0][0]) / 60
    avg_ep = dur_min / eps if eps > 0 else 0.0
    return trans, eps, avg_ep


def main():
    con = sqlite3.connect(DB_PATH)

    sessions = con.execute(
        "SELECT TIMESTAMP/1000, WAKEUP_TIME/1000 "
        "FROM XIAOMI_SLEEP_TIME_SAMPLE ORDER BY TIMESTAMP"
    ).fetchall()

    all_stages = con.execute(
        "SELECT TIMESTAMP/1000, STAGE FROM XIAOMI_SLEEP_STAGE_SAMPLE ORDER BY TIMESTAMP"
    ).fetchall()

    print(f"Schlafstadien-Codes: {sorted(set(s[1] for s in all_stages))}")
    print(
        f"\n{'Night':>14} {'Grp':>3} | {'Trans':>5} {'Ep':>3} {'AvgLen':>6} | "
        f"{'Trans_L':>7} {'Ep_L':>4} {'AvgLen_L':>8}"
    )
    print("-" * 65)

    pre_e, pre_l, dph_e, dph_l = [], [], [], []

    for ts, wu in sessions:
        ld = local_dt(ts)
        dur_h = (wu - ts) / 3600
        if ld.year < 2026 or dur_h < 3 or (10 <= ld.hour < 20):
            continue

        stg = [s for s in all_stages if ts <= s[0] <= wu]
        if len(stg) < 5:
            continue

        is_dph = ts >= DPH_CUTOFF_UTC
        tag = "DPH" if is_dph else "PRE"
        cutoff = ts + EARLY_HOURS * 3600

        early = [s for s in stg if s[0] < cutoff]
        late = [s for s in stg if s[0] >= cutoff]

        t5, e5, a5 = count_transitions(early)
        tl, el, al = count_transitions(late)

        print(
            f"  {ld.strftime('%m-%d %H:%M')} {tag:>3} | "
            f"{t5:>5} {e5:>3} {a5:>6.1f}m | "
            f"{tl:>7} {el:>4} {al:>8.1f}m"
        )

        (dph_e if is_dph else pre_e).append(a5)
        if al > 0:
            (dph_l if is_dph else pre_l).append(al)

    print(f"\n=== Zusammenfassung: Mittlere Episodenlänge (Minuten) ===")
    for label, early, late in [("PRE", pre_e, pre_l), ("DPH", dph_e, dph_l)]:
        if early and late:
            print(f"  {label}  first {EARLY_HOURS}h: {np.mean(early):.1f} ± {np.std(early):.1f}")
            print(f"  {label}  late:     {np.mean(late):.1f} ± {np.std(late):.1f}")

    con.close()


if __name__ == "__main__":
    main()
