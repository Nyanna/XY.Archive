#!/usr/bin/env python3
"""
Per-minute HRV band power aggregator (Lomb-Scargle, individualized bands)
=========================================================================

Fills the Postgres table HRV_SPECTRAL_BANDS_MINUTE with one row per
minute. Each row holds the integrated power (ms²) of the 15 frequency
bands derived from the user-specific spectral fingerprint
(spectral_fingerprint.py, snapshot 2026-04-25). Band edges are the
geometric means between adjacent peak centers, so the bands are
non-overlapping and the sum across all bands equals the total power
within the resolved spectral support.

Band-to-window mapping
----------------------
Five circadian / multi-hour bands  (3.8 h – 24 h period)   →  48 h window
Three ULF bands                    (7.6 – 21.9 min period) →  90 min window
Two VLF bands                      (4.2 – 5.3 min period)  →  30 min window
LF Mayer + four HF respiratory     (2.4 – 10.6 s period)   →  5 min window

Each window is centered on the target minute. The window's beats are
artifact-corrected (local-median, ±500 ms, 5 % budget per ESC/NASPE
1996), linearly detrended, then a single Lomb-Scargle PSD is computed
on the irregular beat times. Per-band power is integrated (∫PSD df)
across the band's edges. NULL when the window has too few beats,
artifact fraction exceeds 5 %, or the LS computation fails.

Standalone & incremental
------------------------
Not called from cleanup_gadgetbridge.py. The target's existing
timestamp_ms_at values define a skip-set (converted internally to
minute-start ms) so only new minutes are computed. RR samples older
than (max(target) - 48 h) are not loaded from Postgres on
incremental runs.
"""

import argparse
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import psycopg2
from astropy.timeseries import LombScargle
from psycopg2 import sql as pgsql
from psycopg2.extras import execute_values

from rr_quality import correct_artifacts, quality_mask

# --- Postgres -------------------------------------------------------
PG_HOST = os.environ["PGHOST"]
PG_PORT = int(os.environ.get("PGPORT", "5432"))
PG_DB = os.environ["PGDATABASE"]
PG_USER = os.environ.get("PGUSER", "gadgetbridge")
PG_PASSWORD = os.environ["PGPASSWORD"]
PG_SCHEMA = "public"
PG_TABLE = "HRV_SPECTRAL_BANDS_MINUTE"
DEVICE_ID = 2  # H9Z 40647
FLUSH_EVERY = 2000

# --- IBI sanity (matches hrv_aggregate.py) --------------------------
MIN_RR = 300
MAX_RR = 2000

# Artifact handling is shared via rr_quality: Layer 1 (correct_artifacts,
# local-median point-ectopic correction, per window) and Layer 2
# (quality_mask block exclusion of strap-slip corruption, applied once in
# load_rr_data). Lomb-Scargle tolerates the resulting gaps natively.

# --- Band definitions -----------------------------------------------
# Each band: (column_name, f_low_hz, f_high_hz, center_hz_for_grid)
# Edges are geometric means between adjacent peak centers from
# spectral_fingerprint.py (snapshot 2026-04-25). Bands are
# non-overlapping; their union covers ~5e-7 .. 0.5 Hz with one tiny
# gap between the two VLF/LF transitions where no peak was detected.
BANDS = [
    # name             f_low      f_high     center
    ("CIRC_24H",       5.0e-7,    1.728e-5,  1.17e-5),
    ("CIRC_11H",       1.728e-5,  3.421e-5,  2.55e-5),
    ("CIRC_6H",        3.421e-5,  5.190e-5,  4.58e-5),
    ("CIRC_5H",        5.190e-5,  6.598e-5,  5.88e-5),
    ("CIRC_4H",        6.598e-5,  2.371e-4,  7.40e-5),
    ("ULF_22MIN",      2.371e-4,  1.106e-3,  7.60e-4),
    ("ULF_10MIN",      1.106e-3,  1.881e-3,  1.61e-3),
    ("ULF_8MIN",       1.881e-3,  2.624e-3,  2.20e-3),
    ("VLF_5MIN",       2.624e-3,  3.541e-3,  3.13e-3),
    ("VLF_4MIN",       3.541e-3,  1.944e-2,  4.01e-3),
    ("LF_MAYER_10S",   1.944e-2,  1.302e-1,  9.42e-2),
    ("HF_BREATH_5S",   1.302e-1,  2.091e-1,  1.80e-1),
    ("HF_BREATH_4S",   2.091e-1,  2.937e-1,  2.43e-1),
    ("HF_BREATH_3S",   2.937e-1,  3.862e-1,  3.55e-1),
    ("HF_BREATH_2S",   3.862e-1,  0.5,       4.20e-1),
]
BAND_NAMES = [b[0] for b in BANDS]

# --- Window groups: each tier shares one Lomb-Scargle per minute ----
# (window_seconds, freq_min, freq_max, n_freq, min_beats, [band_names])
TIER_WINDOWS = [
    # tier_name     win_s     fmin       fmax       nfreq min_beats  bands
    ("circadian",   48*3600,  5e-7,      2.5e-4,    400,  20_000,
        ["CIRC_24H","CIRC_11H","CIRC_6H","CIRC_5H","CIRC_4H"]),
    ("ulf",         90*60,    2.0e-4,    3.0e-3,    400,  3_000,
        ["ULF_22MIN","ULF_10MIN","ULF_8MIN"]),
    ("vlf",         30*60,    2.5e-3,    2.0e-2,    400,  900,
        ["VLF_5MIN","VLF_4MIN"]),
    ("lf_hf",       5*60,     1.5e-2,    0.5,       600,  150,
        ["LF_MAYER_10S","HF_BREATH_5S","HF_BREATH_4S",
         "HF_BREATH_3S","HF_BREATH_2S"]),
]

# Largest backward-looking window — for incremental RR loading.
MAX_WINDOW_MS = max(t[1] for t in TIER_WINDOWS) * 1000

_TRAPZ = getattr(np, "trapezoid", np.trapz)


# -------------------------------------------------------------------
# Spectral helpers
# -------------------------------------------------------------------
def lombscargle_psd(t_sec, rr_corr, freqs):
    """Detrended Lomb-Scargle PSD in ms²/Hz (factor 2 → Parseval)."""
    slope, intercept = np.polyfit(t_sec, rr_corr, 1)
    rr_det = rr_corr - (slope * t_sec + intercept)
    pgram = LombScargle(t_sec, rr_det, normalization="psd").power(
        freqs, method="fast",
    )
    return pgram * 2.0


# -------------------------------------------------------------------
# Postgres
# -------------------------------------------------------------------
def connect_pg():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD,
        dbname=PG_DB, sslmode="require",
    )


def ensure_table(pg_conn):
    cols = ',\n            '.join(
        f'"{name}" REAL' for name in BAND_NAMES
    )
    ddl = f'''
        CREATE TABLE IF NOT EXISTS "{PG_SCHEMA}"."{PG_TABLE}" (
            timestamp_ms_at TIMESTAMPTZ NOT NULL PRIMARY KEY,
            "N_BEATS"      SMALLINT NOT NULL,
            {cols}
        )
    '''
    with pg_conn.cursor() as cur:
        cur.execute(ddl)
    pg_conn.commit()


def get_existing_minutes(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute(
            pgsql.SQL(
                'SELECT (EXTRACT(EPOCH FROM timestamp_ms_at) * 1000)::bigint '
                'FROM {}.{}'
            ).format(
                pgsql.Identifier(PG_SCHEMA),
                pgsql.Identifier(PG_TABLE),
            )
        )
        return {int(r[0]) for r in cur.fetchall()}


def load_rr_data(pg_conn, min_ts_ms=None):
    """Load RR samples projected to (epoch-ms, RR_MILLIS).

    HEART_RR_INTERVAL_SAMPLE no longer carries a bigint TIMESTAMP; the
    canonical timestamp is timestamp_at (timestamptz). We project back
    to integer ms for the existing minute-binning logic.
    """
    cur = pg_conn.cursor()
    query = (
        'SELECT (EXTRACT(EPOCH FROM timestamp_at) * 1000)::bigint, '
        '       "RR_MILLIS" '
        'FROM "HEART_RR_INTERVAL_SAMPLE" '
        'WHERE "DEVICE_ID" = %s '
        '  AND "RR_MILLIS" BETWEEN %s AND %s'
    )
    params = [DEVICE_ID, MIN_RR, MAX_RR]
    if min_ts_ms is not None:
        query += ' AND timestamp_at >= to_timestamp(%s)'
        params.append(int(min_ts_ms) / 1000.0)
    query += ' ORDER BY timestamp_at, "SEQ"'
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    if not rows:
        return None, None
    ts = np.fromiter((r[0] for r in rows), dtype=np.int64, count=len(rows))
    rr = np.fromiter((r[1] for r in rows), dtype=np.float64, count=len(rows))

    # Layer 2: exclude sustained corruption blocks (strap slip) before
    # binning; removed beats become gaps, which Lomb-Scargle tolerates.
    keep, info = quality_mask(ts, rr)
    if info["n_removed"]:
        pct = info["n_removed"] / info["n_total"] * 100.0
        print(f"Quality filter: removed {info['n_removed']:,}/{info['n_total']:,} "
              f"beats ({pct:.1f}%) in {info['n_blocks']} block(s)")
    return ts[keep], rr[keep]


# -------------------------------------------------------------------
# Per-minute computation
# -------------------------------------------------------------------
def integrate_band(freqs, psd, f_lo, f_hi):
    mask = (freqs >= f_lo) & (freqs <= f_hi)
    if mask.sum() < 2:
        return None
    return float(_TRAPZ(psd[mask], freqs[mask]))


def compute_minute(ts_all, rr_all, minute_start_ms,
                   tier_freq_grids, tier_band_indices, n_beats_minute):
    """One row of band-power values for the minute starting at
    `minute_start_ms`. Each tier contributes the bands listed in
    TIER_WINDOWS; missing tiers return all-NULL for their bands.
    """
    out = {name: None for name in BAND_NAMES}
    minute_center = minute_start_ms + 30_000
    for (tier_name, win_s, _fmin, _fmax, _nfreq, min_beats, band_names), \
            freqs, band_idx in zip(TIER_WINDOWS,
                                    tier_freq_grids,
                                    tier_band_indices):
        win_ms = win_s * 1000
        win_lo = minute_center - win_ms // 2
        win_hi = minute_center + win_ms // 2
        i_lo = int(np.searchsorted(ts_all, win_lo, side="left"))
        i_hi = int(np.searchsorted(ts_all, win_hi, side="left"))
        n = i_hi - i_lo
        if n < min_beats:
            continue
        # Effective coverage: reject when the central minute has no
        # beats nearby (large gap straddling the minute) by checking
        # that beats exist within ±half-window/4 of the minute center.
        guard = win_ms // 8
        guard_lo = int(np.searchsorted(ts_all, minute_center - guard,
                                        side="left"))
        guard_hi = int(np.searchsorted(ts_all, minute_center + guard,
                                        side="left"))
        if guard_hi - guard_lo < 5:
            continue
        rr_win = rr_all[i_lo:i_hi]
        rr_corr = correct_artifacts(rr_win)
        if rr_corr is None:
            continue
        t_sec = (ts_all[i_lo:i_hi].astype(np.float64) - win_lo) / 1000.0
        try:
            psd = lombscargle_psd(t_sec, rr_corr, freqs)
        except Exception:
            continue
        for bname in band_names:
            f_lo, f_hi = band_idx[bname]
            out[bname] = integrate_band(freqs, psd, f_lo, f_hi)
    return out


def write_rows(pg_conn, rows):
    if not rows:
        return 0
    all_cols = ["timestamp_ms_at", "N_BEATS"] + BAND_NAMES
    col_list = pgsql.SQL(", ").join(pgsql.Identifier(c) for c in all_cols)
    update_cols = [c for c in all_cols if c != "timestamp_ms_at"]
    set_clause = pgsql.SQL(", ").join(
        pgsql.SQL("{c} = EXCLUDED.{c}").format(c=pgsql.Identifier(c))
        for c in update_cols
    )
    insert_stmt = pgsql.SQL(
        "INSERT INTO {}.{} ({}) VALUES %s "
        "ON CONFLICT ({}) DO UPDATE SET {}"
    ).format(
        pgsql.Identifier(PG_SCHEMA),
        pgsql.Identifier(PG_TABLE),
        col_list,
        pgsql.Identifier("timestamp_ms_at"),
        set_clause,
    )

    tuples = []
    for r in rows:
        tup = (
            datetime.fromtimestamp(r["timestamp_ms"] / 1000.0,
                                   tz=timezone.utc),
            r["n_beats"],
            *[r[name] for name in BAND_NAMES],
        )
        tuples.append(tup)
    with pg_conn.cursor() as cur:
        execute_values(cur, insert_stmt, tuples, page_size=2000)
    pg_conn.commit()
    return len(tuples)


# -------------------------------------------------------------------
# Pipeline helpers
# -------------------------------------------------------------------
def build_freq_grids():
    """Precompute per-tier frequency grids and band-edge lookups from constants."""
    band_dict = {b[0]: (b[1], b[2]) for b in BANDS}
    tier_freq_grids = []
    tier_band_indices = []
    for (_, _, fmin, fmax, nfreq, _, band_names) in TIER_WINDOWS:
        tier_freq_grids.append(np.linspace(fmin, fmax, nfreq))
        tier_band_indices.append({n: band_dict[n] for n in band_names})
    return tier_freq_grids, tier_band_indices


def process_minutes(pg, ts, rr, existing, sorted_minutes, minute_counts,
                    tier_freq_grids, tier_band_indices, limit_minutes=None):
    """Compute band power for each new minute and upsert into Postgres.

    Returns (n_done, n_skipped, n_written).
    """
    total_minutes = len(sorted_minutes)
    if limit_minutes:
        total_minutes = min(total_minutes, limit_minutes)
        print(f"NOTE: limited to first {total_minutes} minutes")

    n_effective = sum(1 for i in range(total_minutes)
                      if int(sorted_minutes[i]) not in existing)
    print(f"Processing {n_effective:,} minute bins "
          f"({total_minutes - n_effective:,} skipped)...")

    rows_buffer = []
    n_done = 0
    n_skipped = 0
    n_written = 0
    log_interval = max(1, n_effective // 20)
    t_loop = time.monotonic()

    print(f"  Progress: 0/{n_effective} (0%) | elapsed 0.0s")

    for mi in range(total_minutes):
        minute_start = int(sorted_minutes[mi])
        if minute_start in existing:
            n_skipped += 1
            continue
        n_beats = int(minute_counts[mi])

        band_values = compute_minute(
            ts, rr, minute_start,
            tier_freq_grids, tier_band_indices, n_beats,
        )
        row = {"timestamp_ms": minute_start, "n_beats": n_beats}
        row.update(band_values)
        rows_buffer.append(row)
        n_done += 1

        if n_done % log_interval == 0 or mi == total_minutes - 1:
            elapsed = time.monotonic() - t_loop
            pct = n_done / n_effective * 100 if n_effective else 100.0
            print(f"  Progress: {n_done:,}/{n_effective:,} ({pct:.0f}%) | elapsed {elapsed:.0f}s")

        if len(rows_buffer) >= FLUSH_EVERY:
            n_written += write_rows(pg, rows_buffer)
            rows_buffer = []

    if rows_buffer:
        n_written += write_rows(pg, rows_buffer)

    return n_done, n_skipped, n_written


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit-minutes", type=int, default=None,
                    help="Limit processing to N minute bins (test mode)")
    ap.add_argument("--full", action="store_true",
                    help="Recompute all minutes (ignore existing rows)")
    args = ap.parse_args()

    t_total = time.monotonic()

    pg = connect_pg()
    try:
        ensure_table(pg)
        existing = set() if args.full else get_existing_minutes(pg)
        print(f'Existing rows in "{PG_TABLE}": {len(existing):,}'
              f'{" (ignored, --full)" if args.full else ""}')

        min_ts_ms = None
        if existing:
            min_ts_ms = max(existing) - MAX_WINDOW_MS
            print(f"Incremental load: timestamp_at >= ms {min_ts_ms}")

        t0 = time.monotonic()
        ts, rr = load_rr_data(pg, min_ts_ms=min_ts_ms)
        if ts is None:
            print("No RR samples in range — nothing to do.")
            return
        print(f"Loaded {ts.size:,} RR samples [{time.monotonic()-t0:.1f}s]")
        t_first = datetime.fromtimestamp(int(ts[0]) / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
        t_last  = datetime.fromtimestamp(int(ts[-1]) / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Time range: {t_first} – {t_last}")

        tier_freq_grids, tier_band_indices = build_freq_grids()

        minute_of_beat = (ts // 60_000) * 60_000
        sorted_minutes, _, minute_counts = np.unique(
            minute_of_beat, return_index=True, return_counts=True
        )

        n_done, n_skipped, n_written = process_minutes(
            pg, ts, rr, existing, sorted_minutes, minute_counts,
            tier_freq_grids, tier_band_indices,
            limit_minutes=args.limit_minutes,
        )

        print(f"Wrote {n_written:,} new minute rows  "
              f"[skipped {n_skipped:,} existing]")
    finally:
        pg.close()


if __name__ == "__main__":
    main()
