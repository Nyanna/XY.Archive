#!/usr/bin/env python3
"""
DPH Phase A — Gesamtanalyse: HR-Floor, Phasenstabilität, HR-Variabilität.
Erwartet: Gadgetbridge SQLite-DB als erstes Argument.
Zeitzone: CEST (UTC+2). Schlafnacht-Cutoff: 18:00 lokal.
DPH-Grenze: Ab 4. April 2026 22:00 CEST.
"""

import sqlite3
import sys
from datetime import datetime, timezone, timedelta
import numpy as np

DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "Gadgetbridge"
CEST = timedelta(hours=2)
CEST_OFF_S = 2 * 3600
DPH_CUTOFF_UTC = datetime(2026, 4, 4, 20, 0).timestamp()  # 22:00 CEST


def local_dt(utc_s):
    return datetime.fromtimestamp(utc_s, tz=timezone.utc) + CEST


def get_nights(con, year=2026, min_dur_h=3):
    """Filtert Schlaf-Sessions auf Nächte (≥3h, kein Tages-Nap)."""
    sessions = con.execute(
        "SELECT TIMESTAMP/1000, WAKEUP_TIME/1000 "
        "FROM XIAOMI_SLEEP_TIME_SAMPLE ORDER BY TIMESTAMP"
    ).fetchall()

    nights = []
    for ts, wu in sessions:
        ld = local_dt(ts)
        dur_h = (wu - ts) / 3600
        if ld.year < year or dur_h < min_dur_h or (10 <= ld.hour < 20):
            continue
        nights.append({
            "start": ts, "end": wu,
            "dph": ts >= DPH_CUTOFF_UTC,
            "label": ld.strftime("%m-%d %H:%M"),
            "dur_h": dur_h,
        })
    return nights


def get_hr(con, start, end):
    """HR-Werte zwischen start und end (UTC seconds), gefiltert."""
    rows = con.execute(
        "SELECT TIMESTAMP, HEART_RATE FROM XIAOMI_ACTIVITY_SAMPLE "
        "WHERE TIMESTAMP BETWEEN ? AND ? AND HEART_RATE > 0 AND HEART_RATE < 200 "
        "ORDER BY TIMESTAMP",
        (start, end),
    ).fetchall()
    return rows


def get_stages(con):
    """Alle Schlafstadien (Timestamp in Sekunden)."""
    return con.execute(
        "SELECT TIMESTAMP/1000, STAGE FROM XIAOMI_SLEEP_STAGE_SAMPLE ORDER BY TIMESTAMP"
    ).fetchall()


def count_transitions(stages):
    if len(stages) < 2:
        return 0, 0, 0.0
    trans = sum(1 for i in range(1, len(stages)) if stages[i][1] != stages[i - 1][1])
    eps = trans + 1
    dur_min = (stages[-1][0] - stages[0][0]) / 60
    avg_ep = dur_min / eps if eps > 0 else 0.0
    return trans, eps, avg_ep


def main():
    con = sqlite3.connect(DB_PATH)
    nights = get_nights(con)
    all_stages = get_stages(con)

    pre = [n for n in nights if not n["dph"]]
    dph = [n for n in nights if n["dph"]]

    print(f"Nächte: {len(nights)} (PRE={len(pre)}, DPH={len(dph)})")

    # === 1. HR-Floor ===
    print("\n=== HR-Floor pro Nacht ===")
    pre_mins, dph_mins = [], []
    pre_p5, dph_p5 = [], []

    for n in nights:
        hrs = get_hr(con, n["start"], n["end"])
        if not hrs:
            continue
        vals = [h[1] for h in hrs]
        p5 = np.percentile(vals, 5)
        tag = "DPH" if n["dph"] else "PRE"
        print(
            f"  {tag} {n['label']} | min={min(vals):>2} p5={p5:.0f} "
            f"mean={np.mean(vals):.1f}"
        )
        (dph_mins if n["dph"] else pre_mins).append(min(vals))
        (dph_p5 if n["dph"] else pre_p5).append(p5)

    print(f"\nFloor-Summary:")
    print(f"  PRE  min: {np.mean(pre_mins):.1f}±{np.std(pre_mins):.1f} ({min(pre_mins)}-{max(pre_mins)})")
    print(f"  DPH  min: {np.mean(dph_mins):.1f}±{np.std(dph_mins):.1f} ({min(dph_mins)}-{max(dph_mins)})")
    print(f"  PRE  p5:  {np.mean(pre_p5):.1f}±{np.std(pre_p5):.1f}")
    print(f"  DPH  p5:  {np.mean(dph_p5):.1f}±{np.std(dph_p5):.1f}")

    # === 2. Episodenlänge (first 5h vs late) ===
    print("\n=== Schlafphasen-Episodenlänge ===")
    pre_ep_e, pre_ep_l = [], []
    dph_ep_e, dph_ep_l = [], []

    for n in nights:
        stg = [s for s in all_stages if n["start"] <= s[0] <= n["end"]]
        if len(stg) < 5:
            continue
        cutoff = n["start"] + 5 * 3600
        early = [s for s in stg if s[0] < cutoff]
        late = [s for s in stg if s[0] >= cutoff]

        _, _, a5 = count_transitions(early)
        _, _, al = count_transitions(late)

        tag = "DPH" if n["dph"] else "PRE"
        print(f"  {tag} {n['label']} | early5h: {a5:.1f}m | late: {al:.1f}m")

        target_e = dph_ep_e if n["dph"] else pre_ep_e
        target_l = dph_ep_l if n["dph"] else pre_ep_l
        target_e.append(a5)
        if al > 0:
            target_l.append(al)

    print(f"\nEpisodenlänge-Summary:")
    print(f"  PRE  first 5h: {np.mean(pre_ep_e):.1f} ± {np.std(pre_ep_e):.1f}")
    print(f"  PRE  late:     {np.mean(pre_ep_l):.1f} ± {np.std(pre_ep_l):.1f}")
    print(f"  DPH  first 5h: {np.mean(dph_ep_e):.1f} ± {np.std(dph_ep_e):.1f}")
    print(f"  DPH  late:     {np.mean(dph_ep_l):.1f} ± {np.std(dph_ep_l):.1f}")

    # === 3. HR-Variabilität ===
    print("\n=== HR-Variabilität (std) ===")
    pre_s_e, pre_s_l = [], []
    dph_s_e, dph_s_l = [], []

    for n in nights:
        cutoff = n["start"] + 5 * 3600
        early_hr = [h[1] for h in get_hr(con, n["start"], min(cutoff, n["end"]))]
        late_hr = [h[1] for h in get_hr(con, cutoff, n["end"])]

        if len(early_hr) > 5:
            s = np.std(early_hr)
            (dph_s_e if n["dph"] else pre_s_e).append(s)
        if len(late_hr) > 5:
            s = np.std(late_hr)
            (dph_s_l if n["dph"] else pre_s_l).append(s)

    print(f"  PRE  early 5h: {np.mean(pre_s_e):.1f} ± {np.std(pre_s_e):.1f}")
    print(f"  PRE  late:     {np.mean(pre_s_l):.1f} ± {np.std(pre_s_l):.1f}")
    print(f"  DPH  early 5h: {np.mean(dph_s_e):.1f} ± {np.std(dph_s_e):.1f}")
    print(f"  DPH  late:     {np.mean(dph_s_l):.1f} ± {np.std(dph_s_l):.1f}")

    # === 4. Tages-Resting-HR ===
    print("\n=== Tages-Resting-HR (Daily Summary) ===")
    rows = con.execute(
        "SELECT TIMESTAMP/1000, HR_RESTING, HR_MIN, HR_AVG "
        "FROM XIAOMI_DAILY_SUMMARY_SAMPLE ORDER BY TIMESTAMP DESC LIMIT 10"
    ).fetchall()
    for r in rows:
        dt = local_dt(r[0])
        print(f"  {dt.strftime('%Y-%m-%d')}: resting={r[1]} min={r[2]} avg={r[3]}")

    con.close()


if __name__ == "__main__":
    main()
