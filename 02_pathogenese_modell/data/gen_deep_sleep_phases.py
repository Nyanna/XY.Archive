#!/usr/bin/env python3
"""Detect deep-sleep phases (Nulldurchgänge) from minute-level HRV data.

Reads per-minute HRV metrics from Postgres (HRV_MINUTE_AGGREGATED),
restricts to vagal-dominant minutes (B7B8_DOM > 0), smooths HR/RMSSD/SDNN
with a rolling median, identifies contiguous blocks where the smoothed
values cross the threshold, and writes results to a local SQLite database.
"""

import os
import sqlite3
import statistics
import sys
from datetime import time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import psycopg2

PG_HOST = os.environ["PGHOST"]
PG_PORT = int(os.environ.get("PGPORT", "5432"))
PG_DB = os.environ["PGDATABASE"]
PG_USER = os.environ.get("PGUSER", "gadgetbridge")
PG_PASSWORD = os.environ["PGPASSWORD"]

TZ = ZoneInfo("Europe/Berlin")
NIGHT_START = time(0, 0)
NIGHT_END = time(7, 30)

HR_THRESHOLD = 80
RMSSD_THRESHOLD = 60
SDNN_THRESHOLD = 60
MIN_PHASE_MINUTES = 5
SMOOTH_WINDOW = 5
SESSION_GAP_MINUTES = 30

OUT_DB = Path(__file__).parent / "deep_sleep_phases.db"


def connect_pg():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD,
        dbname=PG_DB, sslmode="require",
    )


def load_vagal_minutes(pg_conn):
    """Load vagal-dominant minutes (B7B8_DOM > 0) within 00:00–07:30 local."""
    query = """
        SELECT
            "timestamp_ms_at" AT TIME ZONE 'Europe/Berlin' AS ts_local,
            "HR_BPM",
            "RMSSD_MS",
            "SDNN_MS"
        FROM public."HRV_MINUTE_AGGREGATED"
        WHERE "B7B8_DOM" > 0
          AND "HR_BPM" IS NOT NULL
          AND "RMSSD_MS" IS NOT NULL
          AND "SDNN_MS" IS NOT NULL
          AND ("timestamp_ms_at" AT TIME ZONE 'Europe/Berlin')::time >= '00:00'
          AND ("timestamp_ms_at" AT TIME ZONE 'Europe/Berlin')::time < '07:30'
        ORDER BY "timestamp_ms_at"
    """
    with pg_conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def split_into_nights(rows):
    """Group contiguous vagal minutes into sessions, assign night dates.

    A gap > SESSION_GAP_MINUTES separates sessions. Each session is
    assigned to a night date using an 18:00 cutoff (consistent with
    other scripts in this pipeline).
    """
    if not rows:
        return {}

    sessions = []
    current = [rows[0]]
    for prev, row in zip(rows, rows[1:]):
        if (row[0] - prev[0]) > timedelta(minutes=SESSION_GAP_MINUTES):
            sessions.append(current)
            current = []
        current.append(row)
    sessions.append(current)

    nights = {}
    for session in sessions:
        night_date = session[0][0].date().isoformat()
        if night_date not in nights:
            nights[night_date] = []
        nights[night_date].extend(session)

    return nights


def rolling_median(values, window):
    """Centered rolling median with edge-shrinking window."""
    n = len(values)
    half = window // 2
    result = []
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        result.append(statistics.median(values[lo:hi]))
    return result


def smooth_night(minutes):
    """Apply rolling median to HR, RMSSD, SDNN. Returns new tuples."""
    minutes.sort(key=lambda m: m[0])
    hrs = rolling_median([m[1] for m in minutes], SMOOTH_WINDOW)
    rmssds = rolling_median([m[2] for m in minutes], SMOOTH_WINDOW)
    sdnns = rolling_median([m[3] for m in minutes], SMOOTH_WINDOW)
    return [
        (minutes[i][0], hrs[i], rmssds[i], sdnns[i],
         minutes[i][1], minutes[i][2], minutes[i][3])
        for i in range(len(minutes))
    ]


def qualifies(hr, rmssd, sdnn):
    return hr < HR_THRESHOLD and rmssd <= RMSSD_THRESHOLD and sdnn <= SDNN_THRESHOLD


def detect_phases(smoothed):
    """Find contiguous qualifying blocks of >= MIN_PHASE_MINUTES.

    Each entry: (ts, hr_smooth, rmssd_smooth, sdnn_smooth, hr_raw, rmssd_raw, sdnn_raw)
    """
    phases = []
    current = []

    for row in smoothed:
        ts, hr_s, rmssd_s, sdnn_s = row[0], row[1], row[2], row[3]
        if qualifies(hr_s, rmssd_s, sdnn_s):
            if current and (ts - current[-1][0]) > timedelta(minutes=2):
                if len(current) >= MIN_PHASE_MINUTES:
                    phases.append(current)
                current = []
            current.append(row)
        else:
            if len(current) >= MIN_PHASE_MINUTES:
                phases.append(current)
            current = []

    if len(current) >= MIN_PHASE_MINUTES:
        phases.append(current)

    return phases


def phase_stats(phase):
    """Compute stats from raw (unsmoothed) values stored in positions 4-6."""
    hrs = [m[4] for m in phase]
    rmssds = [m[5] for m in phase]
    sdnns = [m[6] for m in phase]

    rmssd_mean = statistics.mean(rmssds)
    sdnn_mean = statistics.mean(sdnns)

    return {
        "start_time": phase[0][0].isoformat(),
        "end_time": (phase[-1][0] + timedelta(minutes=1)).isoformat(),
        "duration_min": len(phase),
        "hr_mean": round(statistics.mean(hrs), 2),
        "hr_std": round(statistics.pstdev(hrs), 2),
        "rmssd_mean": round(rmssd_mean, 2),
        "rmssd_std": round(statistics.pstdev(rmssds), 2),
        "rmssd_cv": round(statistics.pstdev(rmssds) / rmssd_mean, 4) if rmssd_mean > 0 else None,
        "sdnn_mean": round(sdnn_mean, 2),
        "sdnn_std": round(statistics.pstdev(sdnns), 2),
        "sdnn_cv": round(statistics.pstdev(sdnns) / sdnn_mean, 4) if sdnn_mean > 0 else None,
    }


def init_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS deep_sleep_phases")
    cur.execute("DROP TABLE IF EXISTS deep_sleep_nights")
    cur.execute("""
        CREATE TABLE deep_sleep_phases (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            night         TEXT NOT NULL,
            start_time    TEXT NOT NULL,
            end_time      TEXT NOT NULL,
            duration_min  INTEGER NOT NULL,
            hr_mean       REAL,
            hr_std        REAL,
            rmssd_mean    REAL,
            rmssd_std     REAL,
            rmssd_cv      REAL,
            sdnn_mean     REAL,
            sdnn_std      REAL,
            sdnn_cv       REAL
        )
    """)
    cur.execute("""
        CREATE TABLE deep_sleep_nights (
            night            TEXT PRIMARY KEY,
            n_phases         INTEGER NOT NULL,
            total_deep_min   INTEGER NOT NULL,
            mean_phase_min   REAL,
            median_phase_min REAL,
            max_phase_min    INTEGER,
            min_phase_min    INTEGER,
            first_phase_time TEXT,
            last_phase_time  TEXT
        )
    """)
    conn.commit()
    return conn


def main():
    pg_conn = connect_pg()
    rows = load_vagal_minutes(pg_conn)
    pg_conn.close()

    if not rows:
        print("No vagal-dominant HRV data found.", file=sys.stderr)
        sys.exit(1)

    nights = split_into_nights(rows)
    print(f"Loaded {len(rows)} vagal-dominant minutes across {len(nights)} nights.")

    sq_conn = init_sqlite(OUT_DB)
    cur = sq_conn.cursor()

    total_phases = 0
    total_deep = 0
    nights_with_phases = 0

    for night_date in sorted(nights):
        minutes = nights[night_date]
        smoothed = smooth_night(minutes)
        phases = detect_phases(smoothed)
        if not phases:
            continue

        nights_with_phases += 1
        durations = []

        for phase in phases:
            stats = phase_stats(phase)
            cur.execute("""
                INSERT INTO deep_sleep_phases
                    (night, start_time, end_time, duration_min,
                     hr_mean, hr_std, rmssd_mean, rmssd_std, rmssd_cv,
                     sdnn_mean, sdnn_std, sdnn_cv)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                night_date,
                stats["start_time"], stats["end_time"], stats["duration_min"],
                stats["hr_mean"], stats["hr_std"],
                stats["rmssd_mean"], stats["rmssd_std"], stats["rmssd_cv"],
                stats["sdnn_mean"], stats["sdnn_std"], stats["sdnn_cv"],
            ))
            durations.append(stats["duration_min"])
            total_phases += 1
            total_deep += stats["duration_min"]

        first_phase_time = phases[0][0][0].strftime("%H:%M")
        last_phase_time = phases[-1][0][0].strftime("%H:%M")

        cur.execute("""
            INSERT INTO deep_sleep_nights
                (night, n_phases, total_deep_min, mean_phase_min,
                 median_phase_min, max_phase_min, min_phase_min,
                 first_phase_time, last_phase_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            night_date,
            len(durations),
            sum(durations),
            round(statistics.mean(durations), 1),
            round(statistics.median(durations), 1),
            max(durations),
            min(durations),
            first_phase_time,
            last_phase_time,
        ))

    sq_conn.commit()
    sq_conn.close()

    print(f"\nErgebnis → {OUT_DB}")
    print(f"  Nächte mit Phasen: {nights_with_phases}/{len(nights)}")
    print(f"  Phasen gesamt:     {total_phases}")
    print(f"  Tiefschlaf gesamt: {total_deep} min")
    if total_phases > 0:
        print(f"  Mittlere Dauer:    {total_deep / total_phases:.1f} min/Phase")


if __name__ == "__main__":
    main()
