#!/usr/bin/env python3
"""One-off recovery: export the 2026-07-02..07-03 data gap from the local
Postgres Gadgetbridge replica into a SQLite file shaped like the source
Gadgetbridge DB (bigint ms/s TIMESTAMP columns, as gadgetbridge_migrate.py
expects), then that file can be fed to gadgetbridge_migrate.py --full to
backfill the Hive.

Gap found in the Hive: heart_rate_generic has only 2 rows between
2026-07-02 10:13:33.768 UTC and 2026-07-03 13:42:11.643 UTC, while the local
Gadgetbridge SQLite exports are fragmented across archive files and never
cover that stretch. The local Postgres replica (db "gadgetbridge") has the
full, continuous data for the whole window (confirmed: 106,643
GENERIC_HEART_RATE_SAMPLE rows spanning 2026-07-02 06:38 UTC ..
2026-07-03 15:41 UTC, vs. 20,044 fragmented rows locally).

Usage:
    python3 recover_gap_from_postgres.py
    python3 run_pipeline.py --db gap_recovery.db --full
"""
import sqlite3
from pathlib import Path

import psycopg2

# Window with margin around the reported/observed gap so RR beat
# reconstruction (needs neighboring packets) and edge dedup have context.
LO = "2026-07-02 04:38:00+00"
HI = "2026-07-03 17:41:00+00"

OUT_PATH = Path(__file__).parent / "gap_recovery.db"

PG_DSN = dict(host="localhost", port=5432, user="postgres", password="postgres", dbname="gadgetbridge")


def main():
    if OUT_PATH.exists():
        OUT_PATH.unlink()
    sconn = sqlite3.connect(str(OUT_PATH))
    pconn = psycopg2.connect(**PG_DSN)
    pcur = pconn.cursor()

    # --- GENERIC_HEART_RATE_SAMPLE (TIMESTAMP ms, HEART_RATE) ----------
    sconn.execute(
        "CREATE TABLE GENERIC_HEART_RATE_SAMPLE (TIMESTAMP INTEGER, HEART_RATE INTEGER)"
    )
    pcur.execute(
        'SELECT (extract(epoch FROM timestamp_at)*1000)::bigint, "HEART_RATE" '
        'FROM "GENERIC_HEART_RATE_SAMPLE" WHERE timestamp_at BETWEEN %s AND %s',
        (LO, HI),
    )
    rows = pcur.fetchall()
    sconn.executemany("INSERT INTO GENERIC_HEART_RATE_SAMPLE VALUES (?, ?)", rows)
    print(f"GENERIC_HEART_RATE_SAMPLE: {len(rows)} rows")

    # --- XIAOMI_ACTIVITY_SAMPLE (TIMESTAMP s, HEART_RATE) ---------------
    sconn.execute(
        "CREATE TABLE XIAOMI_ACTIVITY_SAMPLE (TIMESTAMP INTEGER, HEART_RATE INTEGER)"
    )
    pcur.execute(
        'SELECT extract(epoch FROM timestamp_at)::bigint, "HEART_RATE" '
        'FROM "XIAOMI_ACTIVITY_SAMPLE" WHERE timestamp_at BETWEEN %s AND %s',
        (LO, HI),
    )
    rows = pcur.fetchall()
    sconn.executemany("INSERT INTO XIAOMI_ACTIVITY_SAMPLE VALUES (?, ?)", rows)
    print(f"XIAOMI_ACTIVITY_SAMPLE: {len(rows)} rows")

    # --- HEART_RR_INTERVAL_SAMPLE (TIMESTAMP ms, SEQ, RR_MILLIS) --------
    sconn.execute(
        "CREATE TABLE HEART_RR_INTERVAL_SAMPLE (TIMESTAMP INTEGER, SEQ INTEGER, RR_MILLIS INTEGER)"
    )
    pcur.execute(
        'SELECT (extract(epoch FROM timestamp_at)*1000)::bigint, "SEQ", "RR_MILLIS" '
        'FROM "HEART_RR_INTERVAL_SAMPLE" WHERE timestamp_at BETWEEN %s AND %s',
        (LO, HI),
    )
    rows = pcur.fetchall()
    sconn.executemany("INSERT INTO HEART_RR_INTERVAL_SAMPLE VALUES (?, ?, ?)", rows)
    print(f"HEART_RR_INTERVAL_SAMPLE: {len(rows)} rows")

    # --- XIAOMI_SLEEP_STAGE_SAMPLE (TIMESTAMP ms, STAGE) -----------------
    sconn.execute(
        "CREATE TABLE XIAOMI_SLEEP_STAGE_SAMPLE (TIMESTAMP INTEGER, STAGE INTEGER)"
    )
    pcur.execute(
        'SELECT (extract(epoch FROM timestamp_at)*1000)::bigint, "STAGE" '
        'FROM "XIAOMI_SLEEP_STAGE_SAMPLE" WHERE timestamp_at BETWEEN %s AND %s',
        (LO, HI),
    )
    rows = pcur.fetchall()
    sconn.executemany("INSERT INTO XIAOMI_SLEEP_STAGE_SAMPLE VALUES (?, ?)", rows)
    print(f"XIAOMI_SLEEP_STAGE_SAMPLE: {len(rows)} rows")

    # --- XIAOMI_SLEEP_TIME_SAMPLE (WAKEUP_TIME ms + duration fields) ----
    sconn.execute(
        "CREATE TABLE XIAOMI_SLEEP_TIME_SAMPLE ("
        "WAKEUP_TIME INTEGER, TIMESTAMP INTEGER, IS_AWAKE INTEGER, "
        "TOTAL_DURATION INTEGER, DEEP_SLEEP_DURATION INTEGER, "
        "LIGHT_SLEEP_DURATION INTEGER, REM_SLEEP_DURATION INTEGER, "
        "AWAKE_DURATION INTEGER)"
    )
    pcur.execute(
        'SELECT (extract(epoch FROM wakeup_time_at)*1000)::bigint, '
        '(extract(epoch FROM timestamp_at)*1000)::bigint, "IS_AWAKE", '
        '"TOTAL_DURATION", "DEEP_SLEEP_DURATION", "LIGHT_SLEEP_DURATION", '
        '"REM_SLEEP_DURATION", "AWAKE_DURATION" '
        'FROM "XIAOMI_SLEEP_TIME_SAMPLE" WHERE wakeup_time_at BETWEEN %s AND %s',
        (LO, HI),
    )
    rows = pcur.fetchall()
    sconn.executemany(
        "INSERT INTO XIAOMI_SLEEP_TIME_SAMPLE VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows
    )
    print(f"XIAOMI_SLEEP_TIME_SAMPLE: {len(rows)} rows")

    sconn.commit()
    sconn.close()
    pconn.close()
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
