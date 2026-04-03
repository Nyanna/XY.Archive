#!/usr/bin/env python3
"""Generate night_hr_trajectory.csv from Gadgetbridge DB."""

import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

DB_PATH = Path(__file__).parent / "Gadgetbridge"
OUT_PATH = Path(__file__).parent / "night_hr_trajectory.csv"

tz = ZoneInfo("Europe/Berlin")


def sleep_night(ts_utc_seconds):
    dt = datetime.fromtimestamp(ts_utc_seconds, tz=timezone.utc).astimezone(tz)
    if dt.hour < 12:
        dt = dt - timedelta(days=1)
    return dt.strftime("%Y-%m-%d")


def main():
    conn = sqlite3.connect(DB_PATH)

    # Load main sleep sessions (>= min)
    sleep_df = pd.read_sql_query(
        "SELECT TIMESTAMP, WAKEUP_TIME, TOTAL_DURATION FROM XIAOMI_SLEEP_TIME_SAMPLE "
        "WHERE TOTAL_DURATION >= 90",
        conn,
    )
    sleep_df["start_ts"] = sleep_df["TIMESTAMP"] / 1000  # ms -> s
    sleep_df["wakeup_ts"] = sleep_df["WAKEUP_TIME"] / 1000

    # Load all HR samples
    hr_df = pd.read_sql_query(
        "SELECT TIMESTAMP, HEART_RATE FROM XIAOMI_ACTIVITY_SAMPLE WHERE HEART_RATE > 0",
        conn,
    )
    conn.close()

    hr_ts = hr_df["TIMESTAMP"].values
    hr_vals = hr_df["HEART_RATE"].values

    rows = []
    for _, sess in sleep_df.iterrows():
        s_start = sess["start_ts"]
        s_end = sess["wakeup_ts"]
        dur_h = (s_end - s_start) / 3600

        # HR samples within sleep window
        mask = (hr_ts >= s_start) & (hr_ts <= s_end)
        hr_t = hr_ts[mask]
        hr_v = hr_vals[mask]

        if len(hr_v) < 10:
            continue

        # Time in hours since sleep start
        ts_hours = (hr_t - s_start) / 3600

        # Linear regression
        slope, intercept = np.polyfit(ts_hours, hr_v, 1)
        r2 = float(np.corrcoef(ts_hours, hr_v)[0, 1] ** 2)

        # Entry/Exit HR (first/last 30 min)
        entry_mask = ts_hours <= 0.5
        exit_mask = ts_hours >= (ts_hours[-1] - 0.5)
        entry_hr = float(np.mean(hr_v[entry_mask])) if entry_mask.any() else np.nan
        exit_hr = float(np.mean(hr_v[exit_mask])) if exit_mask.any() else np.nan
        drop = entry_hr - exit_hr

        # Quartile means
        q_bounds = np.linspace(0, ts_hours[-1], 7)
        q_means = []
        for i in range(6):
            qm = (ts_hours >= q_bounds[i]) & (ts_hours < q_bounds[i + 1])
            q_means.append(float(np.mean(hr_v[qm])) if qm.any() else np.nan)
        q1, q2, q3, q4, q5, q6 = q_means


        # Pattern classification
        if r2 > 0.25 and slope < -1.0:
            pattern = "-2"
        elif r2 > 0.12 and slope < -0.5:
            pattern = "-1"
        elif r2 < 0.05 and abs(slope) < 0.5:
            pattern = "0"
        elif slope > 0.3 and r2 > 0.05:
            pattern = "1"
        else:
            pattern = ""

        night = sleep_night(s_start)
        period = "PRE" if night < "2025-03-01" else "POST"

        start_local = (
            datetime.fromtimestamp(s_start, tz=timezone.utc)
            .astimezone(tz)
            .strftime("%H:%M")
        )

        rows.append(
            {
                "night": night,
                "period": period,
                "start_time": start_local,
                "dur_h": round(dur_h, 2),
                "slope": round(slope, 3),
                "r2": round(r2, 3),
                "entry_hr": round(entry_hr, 1),
                "exit_hr": round(exit_hr, 1),
                "drop": round(drop, 1),
                "q1_mean": round(q1, 1),
                "q2_mean": round(q2, 1),
                "q3_mean": round(q3, 1),
                "q4_mean": round(q4, 1),
                "q5_mean": round(q4, 1),
                "q6_mean": round(q4, 1),
                "pattern": pattern,
            }
        )

    result = pd.DataFrame(rows).sort_values("night").reset_index(drop=True)
    result.to_csv(OUT_PATH, index=False)
    print(f"Exported {len(result)} nights to {OUT_PATH}")

if __name__ == "__main__":
    main()
