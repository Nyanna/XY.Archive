#!/usr/bin/env python3
"""Generate tau_timeseries.csv – B7-Abschaltzeitkonstante τ aus nächtlichen HR-Daten."""

import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from scipy.optimize import curve_fit

DATA_DIR = Path(__file__).parent
DB_PATH = DATA_DIR / "Gadgetbridge"
SEIZURES_PATH = DATA_DIR / "seizures.csv"
OUT_PATH = DATA_DIR / "tau_timeseries.csv"

tz = ZoneInfo("Europe/Berlin")


def sleep_night(ts_utc_seconds):
    dt = datetime.fromtimestamp(ts_utc_seconds, tz=timezone.utc).astimezone(tz)
    if dt.hour < 12:
        dt = dt - timedelta(days=1)
    return dt.strftime("%Y-%m-%d")


def exp_decay(t, amplitude, tau, floor):
    return floor + amplitude * np.exp(-t / tau)


def main():
    conn = sqlite3.connect(DB_PATH)

    # Load main sleep sessions (≥90 min)
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

    # Load seizure dates
    seizure_df = pd.read_csv(SEIZURES_PATH)
    seizure_dates = set(
        pd.to_datetime(seizure_df["Date"], format="%d/%m/%y").dt.strftime("%Y-%m-%d")
    )

    rows = []
    for _, sess in sleep_df.iterrows():
        s_start = sess["start_ts"]
        s_end = sess["wakeup_ts"]
        dur_h = (s_end - s_start) / 3600

        # HR samples within sleep window
        mask = (hr_ts >= s_start) & (hr_ts <= s_end)
        hr_t = hr_ts[mask]
        hr_v = hr_vals[mask].astype(float)

        if len(hr_v) < 10:
            continue

        # Time in hours since sleep start
        ts_hours = (hr_t - s_start) / 3600

        # Entry HR: mean of first 15 minutes
        entry_mask = ts_hours <= 0.25
        entry_hr = float(np.mean(hr_v[entry_mask])) if entry_mask.any() else np.nan

        # Exit HR: lowest value of 10-min rolling mean
        hr_series = pd.Series(hr_v, index=ts_hours)
        rolling_mean = hr_series.rolling(window=10, min_periods=1).mean()
        exit_hr = float(rolling_mean.min())

        drop = entry_hr - exit_hr

        # Exponential fit: HR(t) = floor + amplitude * exp(-t / tau)
        p0 = [drop if drop > 0 else 5.0, 1.0, exit_hr]
        bounds = ([0, 0.01, 30], [80, 12, 100])

        try:
            popt, _ = curve_fit(exp_decay, ts_hours, hr_v, p0=p0, bounds=bounds, maxfev=5000)
            amplitude, tau_h, floor_hr = popt
        except (RuntimeError, ValueError):
            continue

        night = sleep_night(s_start)
        period = "PRE" if night < "2025-03-01" else "POST"

        start_local = (
            datetime.fromtimestamp(s_start, tz=timezone.utc)
            .astimezone(tz)
            .strftime("%H:%M")
        )

        rows.append(
            {
                "sleep_night": night,
                "period": period,
                "start_time": start_local,
                "dur_h": round(dur_h, 2),
                "tau_h": round(tau_h, 4),
                "amplitude": round(amplitude, 1),
                "floor": round(floor_hr, 1),
                "seizure": 1 if night in seizure_dates else 0,
            }
        )

    result = pd.DataFrame(rows).sort_values("sleep_night").reset_index(drop=True)
    result.to_csv(OUT_PATH, index=False)
    print(f"Exported {len(result)} nights to {OUT_PATH}")


if __name__ == "__main__":
    main()
