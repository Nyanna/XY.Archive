#!/usr/bin/env python3
"""HRV minute aggregation from Gadgetbridge RR-interval samples.

Reads raw RR intervals from the Gadgetbridge SQLite database and
upserts the derived per-minute metrics into the target Postgres
database (HRV_MINUTE_AGGREGATED). Only minutes that are not yet
present in Postgres are computed; RR samples older than the largest
analysis window before the newest stored minute are not loaded from
SQLite to keep incremental runs cheap.
"""

import argparse
import math
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import psycopg2
from astropy.timeseries import LombScargle
from psycopg2 import sql as pgsql
from psycopg2.extras import execute_values
from scipy.interpolate import CubicSpline
from scipy.ndimage import median_filter
from scipy.signal import welch

DB_PATH = Path(__file__).parent / "Gadgetbridge"

# Postgres target (mirrors cleanup_gadgetbridge.py)
PG_HOST = os.environ["PGHOST"]
PG_PORT = int(os.environ.get("PGPORT", "5432"))
PG_DB = os.environ["PGDATABASE"]
PG_USER = os.environ.get("PGUSER", "gadgetbridge")
PG_PASSWORD = os.environ["PGPASSWORD"]
PG_SCHEMA = "public"
PG_TABLE = "HRV_MINUTE_AGGREGATED"

MIN_RR = 300
MAX_RR = 2000
GAP_THRESHOLD_MS = 5000
MIN_BEATS_PER_MINUTE = 15
LFHF_MIN_BEATS = 150
LFHF_WINDOW_MS = 5 * 60 * 1000
VLF_MIN_BEATS = 300
VLF_WINDOW_MS = 15 * 60 * 1000
ULF_WINDOW_MS = 120 * 60 * 1000
ULF_MIN_BEATS = 3600
ULF1_BAND = (0.0005, 0.0033)
ULF2_BAND = (0.0001, 0.0005)
ULF_BAND = (0.0001, 0.0033)
ULF_FREQ_MIN = 0.00005
ULF_FREQ_MAX = 0.005
ULF_N_FREQ = 512
DFA_WINDOW = 200
DFA_BOXES_ALL = [4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64]
DFA_BOXES_ALPHA1 = {4, 6, 8, 10, 12, 16}

# Artifact correction (PSD path and VAGAL_BALANCE; base metrics such as
# RMSSD/pNN50/SDNN stay on the raw gap-filtered values to preserve
# comparability with existing queries).
#
# Local-median detector (not Malik): ESC/NASPE 1996 Task Force leaves the
# detection rule open, only the 5% window-reject and the interpolation
# requirement are fixed. Nearest-neighbor rules (Malik) misclassify
# physiological RSA swings -- especially during REM-dominated second half
# of night -- as artifacts. A local median smooths across RSA oscillations
# so only true spikes (ectopics / missed beats) produce a large deviation.
ARTIFACT_MEDIAN_HALFWIDTH = 4   # 9-beat window (i-4 .. i+4)
ARTIFACT_THRESHOLD_MS = 500     # |RR - local_median| > 500 ms -> artifact
MAX_ARTIFACT_FRACTION = 0.05    # reject window if exceeded (Task Force 5%)

# VAGAL_BALANCE normalization: RMSSD/SDNN of healthy adults at rest
# (Shaffer & Ginsberg 2017, Front Public Health, 5-min windows).
# VAGAL_BALANCE = (RMSSD_nn / SDNN_nn) / VAGAL_BALANCE_REF, so >1 = vagotonic,
# <1 = sympathicotonic relative to the healthy-adult reference.
VAGAL_BALANCE_REF = 0.50

# B7/B8 state classification (see temp/command.md). Two axes from LF/HF/VLF:
#   B7B8_DOM = (HF - LF) / (HF + LF)   in [-1, +1]   B8-vs-B7 dominance
#   B7B8_OFF = VLF / (LF + HF + VLF)   in [ 0,  1]   congruence-vs-divergence
# Both NULL when Total < TOTAL_MIN (too little spectral power to classify).
# Scale-dependent: Coospo/App N1-N3 ~3.0 ms²; N4 needs proportional scaling.
TOTAL_MIN = 3.0


def load_rr_data(db_path, device_id=None, min_ts_ms=None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='HEART_RR_INTERVAL_SAMPLE'"
    )
    if cur.fetchone() is None:
        print("ERROR: HEART_RR_INTERVAL_SAMPLE table not found", file=sys.stderr)
        sys.exit(1)

    if device_id is None:
        cur.execute(
            "SELECT DEVICE_ID, COUNT(*) FROM HEART_RR_INTERVAL_SAMPLE "
            "GROUP BY DEVICE_ID ORDER BY COUNT(*) DESC"
        )
        rows = cur.fetchall()
        if not rows:
            print("ERROR: HEART_RR_INTERVAL_SAMPLE is empty", file=sys.stderr)
            sys.exit(1)
        device_id = rows[0][0]

    cur.execute("SELECT NAME FROM DEVICE WHERE _id = ?", (device_id,))
    dev_row = cur.fetchone()
    device_name = dev_row[0] if dev_row else f"id={device_id}"

    query = (
        "SELECT TIMESTAMP, RR_MILLIS FROM HEART_RR_INTERVAL_SAMPLE "
        "WHERE DEVICE_ID = ?"
    )
    params = [device_id]
    if min_ts_ms is not None:
        query += " AND TIMESTAMP >= ?"
        params.append(int(min_ts_ms))
    query += " ORDER BY TIMESTAMP, SEQ"

    cur.execute(query, params)
    raw = cur.fetchall()
    conn.close()

    data = [(ts, rr) for ts, rr in raw if MIN_RR <= rr <= MAX_RR]
    return data, device_id, device_name


def compute_dfa_alpha1(rr_values):
    if len(rr_values) < DFA_WINDOW:
        return None
    rr = np.asarray(rr_values[-DFA_WINDOW:], dtype=float)
    y = np.cumsum(rr - rr.mean())
    N = len(y)

    logs_n = []
    logs_F = []
    for n in DFA_BOXES_ALL:
        if n > N // 4:
            continue
        if n not in DFA_BOXES_ALPHA1:
            continue
        n_segments = N // n
        if n_segments < 1:
            continue
        residuals_sq = []
        x = np.arange(n)
        for s in range(n_segments):
            seg = y[s * n:(s + 1) * n]
            coef = np.polyfit(x, seg, 1)
            trend = np.polyval(coef, x)
            residuals_sq.append(np.mean((seg - trend) ** 2))
        F = math.sqrt(np.mean(residuals_sq))
        if F <= 0:
            continue
        logs_n.append(math.log(n))
        logs_F.append(math.log(F))

    if len(logs_n) < 2:
        return None
    slope, _ = np.polyfit(logs_n, logs_F, 1)
    return float(slope)


FS_RESAMPLE = 4.0  # Hz, Task Force (1996) recommendation for RR-tachogram resampling
_TRAPZ = getattr(np, "trapezoid", np.trapz)


def correct_artifacts(rr: np.ndarray) -> np.ndarray | None:
    """Local-median artifact correction with linear interpolation.

    For each beat i, compute the median over a 9-beat window centered on i
    and flag the beat as artifactual when |RR[i] - local_median| exceeds
    ARTIFACT_THRESHOLD_MS (300 ms). Flagged beats are replaced by linear
    interpolation between the nearest non-artifactual neighbors. The window
    is rejected entirely if the artifact fraction exceeds
    MAX_ARTIFACT_FRACTION (5%), per ESC/NASPE 1996 Task Force.

    Rationale: the nearest-neighbor (Malik) rule conflates physiological
    RSA swings with ectopic beats -- especially in REM-dominated sleep,
    where beat-to-beat changes of >20% can be normal. A local median is
    insensitive to smooth RSA oscillations but still isolates true spikes
    (PVC, missed beat, compensatory pause).

    PSD path only; base metrics (RMSSD, pNN50, ...) keep the raw
    gap-filtered values.
    """
    n = len(rr)
    if n < 2:
        return rr.astype(float, copy=True)
    rr = rr.astype(float, copy=True)

    window_size = 2 * ARTIFACT_MEDIAN_HALFWIDTH + 1
    local_median = median_filter(rr, size=window_size, mode="nearest")
    artifact_mask = np.abs(rr - local_median) > ARTIFACT_THRESHOLD_MS

    n_artifacts = int(artifact_mask.sum())
    if n_artifacts / n > MAX_ARTIFACT_FRACTION:
        return None
    if n_artifacts == 0:
        return rr

    valid_idx = np.flatnonzero(~artifact_mask)
    if valid_idx.size < 2:
        return None
    all_idx = np.arange(n)
    rr[artifact_mask] = np.interp(all_idx[artifact_mask], valid_idx, rr[valid_idx])
    return rr


def compute_band_power(rr_values, freq_ranges, detrend="constant"):
    """Compute integrated band power via cubic-spline resampling + Welch PSD.

    Task-Force-compliant (ESC/NASPE 1996): RR tachogram → cubic spline → 4 Hz
    uniform grid → Welch PSD (Hann window, single segment). Welch's
    scaling='density' returns PSD in ms²/Hz such that ∫ PSD df ≈ variance(y),
    so band power = ∫_band PSD df directly in ms² — no manual Parseval
    normalization required.

    Args:
        rr_values: array of RR intervals in ms
        freq_ranges: list of (name, f_low, f_high) tuples
        detrend: 'constant' (mean removal, default for LF/HF 5-min windows)
            or 'linear' (drift removal, recommended for VLF 15-min windows
            because otherwise linear drift shows up as spurious VLF power).

    Returns:
        dict of {name: power_ms2}
    """
    none_result = {name: None for name, _, _ in freq_ranges}
    if len(rr_values) < 30:
        return none_result

    rr = np.asarray(rr_values, dtype=float)
    rr = correct_artifacts(rr)
    if rr is None or len(rr) < 30:
        return none_result
    t_sec = np.cumsum(rr) / 1000.0
    t_sec = t_sec - t_sec[0]
    duration = float(t_sec[-1])
    if duration <= 0:
        return none_result

    try:
        cs = CubicSpline(t_sec, rr, extrapolate=False)
    except Exception:
        return none_result

    n_uniform = int(duration * FS_RESAMPLE)
    if n_uniform < 64:
        return none_result
    t_uniform = np.linspace(0.0, duration, n_uniform)
    y = cs(t_uniform)

    try:
        f, pxx = welch(
            y, fs=FS_RESAMPLE, nperseg=n_uniform,
            window="hann", scaling="density", detrend=detrend,
        )
    except Exception:
        return none_result

    result = {}
    for name, f_low, f_high in freq_ranges:
        mask = (f >= f_low) & (f <= f_high)
        if mask.any() and f_high > f_low:
            result[name] = float(_TRAPZ(pxx[mask], f[mask]))
        else:
            result[name] = None
    return result


def compute_ulf_power(t_ms: np.ndarray, rr: np.ndarray) -> dict | None:
    """Lomb-Scargle ULF power on irregularly-sampled RR with gaps.

    Operates directly on the irregular beat timestamps (no spline
    interpolation) so that multi-minute gaps reduce SNR instead of
    producing spurious low-frequency power. Literature-conform for
    gappy HRV (Laguna et al. 1998; Clifford & Tarassenko 2005).

    Returns {'ulf_ms2', 'ulf1_ms2', 'ulf2_ms2'} in ms², or the same
    dict with None values if artefact fraction > 5 % or the window
    is too short / degenerate.
    """
    none_result = {"ulf_ms2": None, "ulf1_ms2": None, "ulf2_ms2": None}
    if rr.size < 30:
        return none_result

    rr_corr = correct_artifacts(rr)
    if rr_corr is None or rr_corr.size < 30:
        return none_result

    t_sec = (t_ms.astype(np.float64) - float(t_ms[0])) / 1000.0
    T = float(t_sec[-1] - t_sec[0])
    if T <= 0:
        return none_result

    slope, intercept = np.polyfit(t_sec, rr_corr, 1)
    rr_detrended = rr_corr - (slope * t_sec + intercept)

    freqs = np.linspace(ULF_FREQ_MIN, ULF_FREQ_MAX, ULF_N_FREQ)

    # astropy's method='fast' uses a non-uniform FFT (Press & Rybicki 1989),
    # O(N_beats × log N_freq) instead of scipy's O(N_beats × N_freq).
    # Requires uniform freq grid with samples_per_peak = 1/(df×T) >= 5,
    # which is satisfied here (~14).
    try:
        pgram = LombScargle(
            t_sec, rr_detrended, normalization='psd',
        ).power(freqs, method='fast')
    except Exception:
        return none_result

    # Parseval-konform mit Welch scaling='density': ∫ PSD df ≈ var(rr).
    # LombScargle(normalization='psd') integriert zu var/2 über das ganze
    # Band (empirisch am Sinus-Test verifiziert), Faktor 2 → ms²/Hz.
    psd = pgram * 2.0

    def _band(f_lo, f_hi):
        mask = (freqs >= f_lo) & (freqs <= f_hi)
        if not mask.any():
            return None
        return float(_TRAPZ(psd[mask], freqs[mask]))

    return {
        "ulf_ms2":  _band(*ULF_BAND),
        "ulf1_ms2": _band(*ULF1_BAND),
        "ulf2_ms2": _band(*ULF2_BAND),
    }


def compute_minute_metrics(rr_data, enable_lf_hf=False, enable_dfa=False, enable_ulf=False, limit_minutes=None, skip_minutes=None):
    """Aggregate HRV metrics per minute.

    limit_minutes: if set, only the first N minute bins are processed.
    Purpose: performance and integrity test runs on a small slice of the
    data, without having to crunch through the full dataset. Production: None.

    skip_minutes: optional set of minute-start timestamps (ms) already
    present in the target; those bins are skipped so the script only
    recomputes new minutes.
    """
    if not rr_data:
        return []
    skip_minutes = skip_minutes or set()

    t0 = time.monotonic()

    n_total = len(rr_data)
    all_ts = np.fromiter((r[0] for r in rr_data), dtype=np.int64, count=n_total)
    all_rr = np.fromiter((r[1] for r in rr_data), dtype=np.int64, count=n_total)

    # Successive differences (vectorized, with gap filter)
    # diff at index k = rr[k+1] - rr[k], belongs to the beat at index k+1
    ts_gaps = np.diff(all_ts)
    rr_diffs = np.diff(all_rr).astype(float)
    valid_diff_mask = ts_gaps <= GAP_THRESHOLD_MS

    print(f"  Successive diffs computed: {time.monotonic() - t0:.2f}s")

    # Minute binning: data is sorted by TIMESTAMP -> contiguous slices per minute
    minute_of_beat = (all_ts // 60000) * 60000
    sorted_minutes, minute_lo, minute_counts = np.unique(
        minute_of_beat, return_index=True, return_counts=True
    )
    minute_hi = minute_lo + minute_counts

    print(f"  Minute binning done ({len(sorted_minutes)} bins): {time.monotonic() - t0:.2f}s")

    results = []
    total_minutes = len(sorted_minutes)
    if limit_minutes is not None and limit_minutes > 0:
        total_minutes = min(total_minutes, int(limit_minutes))
        print(f"  NOTE: processing limited to first {total_minutes} minute bins (--limit-minutes)")
    time_basic = 0.0
    time_lf = 0.0
    time_hf = 0.0
    time_vlf = 0.0
    time_ulf = 0.0
    time_dfa = 0.0
    t_loop_start = time.monotonic()
    log_interval = max(1, total_minutes // 20)  # ~20 progress updates

    n_skipped = 0
    for mi in range(total_minutes):
        minute_start = int(sorted_minutes[mi])
        if minute_start in skip_minutes:
            n_skipped += 1
            continue

        n_beats = int(minute_counts[mi])
        if n_beats < MIN_BEATS_PER_MINUTE:
            continue

        lo = int(minute_lo[mi])
        hi = int(minute_hi[mi])

        t_step = time.monotonic()
        rr = all_rr[lo:hi].astype(float)
        mean_rr = float(rr.mean())
        hr_bpm = 60000.0 / mean_rr if mean_rr > 0 else None
        min_rr = int(rr.min())
        max_rr = int(rr.max())
        std_rr = float(rr.std(ddof=0))  # population stddev

        # Diffs for beats in [lo, hi): diff array indices [max(0, lo-1), hi-1)
        diff_lo = lo - 1 if lo > 0 else 0
        diff_hi = hi - 1
        if diff_hi > diff_lo:
            valid = valid_diff_mask[diff_lo:diff_hi]
            d = rr_diffs[diff_lo:diff_hi][valid]
            if d.size:
                rmssd = float(math.sqrt(np.mean(d ** 2)))
                pnn50 = float(np.sum(np.abs(d) > 50) / d.size * 100.0)
            else:
                rmssd = 0.0
                pnn50 = None
        else:
            rmssd = 0.0
            pnn50 = None

        ln_rmssd = math.log(rmssd) if rmssd > 0 else None
        vagal_index = (
            ln_rmssd / math.log(mean_rr)
            if (ln_rmssd is not None and mean_rr > 1)
            else None
        )
        rmssd_pct = rmssd / mean_rr * 100.0 if mean_rr > 0 else None
        sdnn = std_rr  # equivalent to population stddev
        rmssd_sdnn_ratio = rmssd / sdnn if sdnn > 0 else None

        # VAGAL_BALANCE: Task-Force-konform auf NN-Intervallen nach Artefakt-
        # Korrektur. NULL bei RR-Gap > GAP_THRESHOLD_MS in der Minute, bei
        # Artefakt-Anteil > 5% (correct_artifacts liefert dann None) oder bei
        # degenerierten RMSSD/SDNN.
        vagal_balance = None
        ts_minute = all_ts[lo:hi]
        has_gap = ts_minute.size > 1 and int(np.diff(ts_minute).max()) > GAP_THRESHOLD_MS
        if not has_gap:
            rr_nn = correct_artifacts(rr)
            if rr_nn is not None and rr_nn.size >= 2:
                d_nn = np.diff(rr_nn)
                if d_nn.size > 0:
                    rmssd_nn = float(math.sqrt(np.mean(d_nn ** 2)))
                    sdnn_nn = float(rr_nn.std(ddof=0))
                    if rmssd_nn > 0 and sdnn_nn > 0:
                        vagal_balance = (rmssd_nn / sdnn_nn) / VAGAL_BALANCE_REF

        time_basic += time.monotonic() - t_step

        # LF/HF: 5-min window; VLF: 15-min window (band-specific resolution)
        vlf, lf, hf, lfhf = None, None, None, None
        if enable_lf_hf:
            # --- LF from 5-min window (searchsorted: O(log N) instead of O(N) mask) ---
            win5_start = minute_start - 2 * 60 * 1000
            win5_end = minute_start + 3 * 60 * 1000
            i5_lo = int(np.searchsorted(all_ts, win5_start, side="left"))
            i5_hi = int(np.searchsorted(all_ts, win5_end, side="left"))
            win5_ok = (i5_hi - i5_lo) >= LFHF_MIN_BEATS
            rr_5min = all_rr[i5_lo:i5_hi] if win5_ok else None

            t_lf = time.monotonic()
            if win5_ok:
                lf = compute_band_power(rr_5min, [('lf', 0.04, 0.15)])['lf']
            time_lf += time.monotonic() - t_lf

            t_hf = time.monotonic()
            if win5_ok:
                hf = compute_band_power(rr_5min, [('hf', 0.15, 0.40)])['hf']
            time_hf += time.monotonic() - t_hf

            # --- VLF from 15-min window ---
            t_vlf = time.monotonic()
            win15_start = minute_start - 7 * 60 * 1000
            win15_end = minute_start + 8 * 60 * 1000
            i15_lo = int(np.searchsorted(all_ts, win15_start, side="left"))
            i15_hi = int(np.searchsorted(all_ts, win15_end, side="left"))
            if (i15_hi - i15_lo) >= VLF_MIN_BEATS:
                vlf = compute_band_power(
                    all_rr[i15_lo:i15_hi], [('vlf', 0.0033, 0.04)],
                    detrend="linear",
                )['vlf']
            time_vlf += time.monotonic() - t_vlf

            lfhf = lf / hf if (lf is not None and hf is not None and hf > 0) else None

        # B7/B8 state axes (from existing 5-min LF/HF + 15-min VLF window).
        # Both NULL if any band missing or total power below TOTAL_MIN.
        b7b8_dom, b7b8_off = None, None
        if lf is not None and hf is not None and vlf is not None:
            total_power = lf + hf + vlf
            if total_power >= TOTAL_MIN:
                lf_plus_hf = lf + hf
                b7b8_dom = 0.0 if lf_plus_hf == 0 else (hf - lf) / lf_plus_hf
                b7b8_off = vlf / total_power

        # ULF: 120-min sliding window, Lomb-Scargle on irregular RR samples
        ulf_ms2, ulf1_ms2, ulf2_ms2 = None, None, None
        if enable_ulf:
            t_ulf = time.monotonic()
            win_ulf_start = minute_start - 60 * 60 * 1000
            win_ulf_end = minute_start + 60 * 60 * 1000
            i_ulf_lo = int(np.searchsorted(all_ts, win_ulf_start, side="left"))
            i_ulf_hi = int(np.searchsorted(all_ts, win_ulf_end, side="left"))
            if (i_ulf_hi - i_ulf_lo) >= ULF_MIN_BEATS:
                ulf_res = compute_ulf_power(
                    all_ts[i_ulf_lo:i_ulf_hi].astype(np.int64),
                    all_rr[i_ulf_lo:i_ulf_hi].astype(float),
                )
                if ulf_res is not None:
                    ulf_ms2 = ulf_res["ulf_ms2"]
                    ulf1_ms2 = ulf_res["ulf1_ms2"]
                    ulf2_ms2 = ulf_res["ulf2_ms2"]
            time_ulf += time.monotonic() - t_ulf

        # DFA: last 200 RR before the end of the minute (optional)
        dfa_alpha1 = None
        if enable_dfa:
            t_dfa = time.monotonic()
            start_idx = hi - DFA_WINDOW if hi >= DFA_WINDOW else 0
            dfa_alpha1 = compute_dfa_alpha1(all_rr[start_idx:hi])

            time_dfa += time.monotonic() - t_dfa

        if (mi + 1) % log_interval == 0 or mi == total_minutes - 1:
            elapsed = time.monotonic() - t_loop_start
            pct = (mi + 1) / total_minutes * 100
            print(
                f"  Progress: {mi + 1}/{total_minutes} ({pct:.0f}%) | "
                f"elapsed {elapsed:.1f}s | "
                f"basic {time_basic:.1f}s  lf {time_lf:.1f}s  hf {time_hf:.1f}s  "
                f"vlf {time_vlf:.1f}s  ulf {time_ulf:.1f}s  dfa {time_dfa:.1f}s"
            )

        results.append({
            "timestamp_ms": int(minute_start),
            "n_beats": int(n_beats),
            "hr_bpm": hr_bpm,
            "avg_rr_ms": mean_rr,
            "min_rr_ms": min_rr,
            "max_rr_ms": max_rr,
            "stddev_rr_ms": std_rr,
            "rmssd_ms": rmssd,
            "ln_rmssd": ln_rmssd,
            "vagal_index": vagal_index,
            "rmssd_pct": rmssd_pct,
            "sdnn_ms": sdnn,
            "rmssd_sdnn_ratio": rmssd_sdnn_ratio,
            "vagal_balance": vagal_balance,
            "pnn50": pnn50,
            "vlf_ms2": vlf,
            "lf_ms2": lf,
            "hf_ms2": hf,
            "ulf_ms2": ulf_ms2,
            "ulf1_ms2": ulf1_ms2,
            "ulf2_ms2": ulf2_ms2,
            "lf_hf_ratio": lfhf,
            "b7b8_dom": b7b8_dom,
            "b7b8_off": b7b8_off,
            "dfa_alpha1": dfa_alpha1,
        })

    elapsed_total = time.monotonic() - t0
    print(f"  --- Timing summary ---")
    print(f"  Prep (diffs + binning):  included above")
    print(f"  Basic metrics total:     {time_basic:.2f}s")
    if enable_lf_hf:
        print(f"  LF  (Welch, 5-min win):  {time_lf:.2f}s")
        print(f"  HF  (Welch, 5-min win):  {time_hf:.2f}s")
        print(f"  VLF (Welch, 15-min win): {time_vlf:.2f}s")
    else:
        print(f"  LF/HF/VLF (Welch):       disabled")
    if enable_ulf:
        print(f"  ULF (Lomb-Scargle, 2h):  {time_ulf:.2f}s")
    else:
        print(f"  ULF (Lomb-Scargle):      disabled")
    if enable_dfa:
        print(f"  DFA alpha1:              {time_dfa:.2f}s")
    else:
        print(f"  DFA alpha1:              disabled")
    print(f"  Loop total:              {time.monotonic() - t_loop_start:.2f}s")
    print(f"  compute_minute_metrics:  {elapsed_total:.2f}s")
    if n_skipped:
        print(f"  Skipped (already in target): {n_skipped}")

    return results


PG_COLUMNS = [
    "TIMESTAMP_MS", "N_BEATS", "HR_BPM", "AVG_RR_MS", "MIN_RR_MS", "MAX_RR_MS",
    "STDDEV_RR_MS", "RMSSD_MS", "LN_RMSSD", "VAGAL_INDEX", "RMSSD_PCT", "SDNN_MS",
    "RMSSD_SDNN_RATIO", "VAGAL_BALANCE", "PNN50",
    "VLF_MS2", "LF_MS2", "HF_MS2", "ULF_MS2", "ULF1_MS2", "ULF2_MS2",
    "LF_HF_RATIO", "B7B8_DOM", "B7B8_OFF", "DFA_ALPHA1",
]
PG_AT_COLUMN = "timestamp_ms_at"


def connect_pg():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD,
        dbname=PG_DB, sslmode="require",
    )


def ensure_hrv_table(pg_conn):
    ddl = f'''
        CREATE TABLE IF NOT EXISTS "{PG_SCHEMA}"."{PG_TABLE}" (
            "TIMESTAMP_MS"     BIGINT NOT NULL PRIMARY KEY,
            "N_BEATS"          BIGINT NOT NULL,
            "HR_BPM"           DOUBLE PRECISION,
            "AVG_RR_MS"        DOUBLE PRECISION,
            "MIN_RR_MS"        BIGINT,
            "MAX_RR_MS"        BIGINT,
            "STDDEV_RR_MS"     DOUBLE PRECISION,
            "RMSSD_MS"         DOUBLE PRECISION,
            "LN_RMSSD"         DOUBLE PRECISION,
            "VAGAL_INDEX"      DOUBLE PRECISION,
            "RMSSD_PCT"        DOUBLE PRECISION,
            "SDNN_MS"          DOUBLE PRECISION,
            "RMSSD_SDNN_RATIO" DOUBLE PRECISION,
            "VAGAL_BALANCE"    DOUBLE PRECISION,
            "PNN50"            DOUBLE PRECISION,
            "VLF_MS2"          DOUBLE PRECISION,
            "LF_MS2"           DOUBLE PRECISION,
            "HF_MS2"           DOUBLE PRECISION,
            "ULF_MS2"          DOUBLE PRECISION,
            "ULF1_MS2"         DOUBLE PRECISION,
            "ULF2_MS2"         DOUBLE PRECISION,
            "LF_HF_RATIO"      DOUBLE PRECISION,
            "B7B8_DOM"         DOUBLE PRECISION,
            "B7B8_OFF"         DOUBLE PRECISION,
            "DFA_ALPHA1"       DOUBLE PRECISION,
            {PG_AT_COLUMN}     TIMESTAMPTZ
        )
    '''
    with pg_conn.cursor() as cur:
        cur.execute(ddl)
    pg_conn.commit()


def get_existing_minutes(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute(
            pgsql.SQL('SELECT "TIMESTAMP_MS" FROM {}.{}').format(
                pgsql.Identifier(PG_SCHEMA),
                pgsql.Identifier(PG_TABLE),
            )
        )
        return {int(r[0]) for r in cur.fetchall()}


def write_results_pg(pg_conn, rows):
    if not rows:
        return 0, None

    all_cols = PG_COLUMNS + [PG_AT_COLUMN]
    col_list = pgsql.SQL(", ").join(pgsql.Identifier(c) for c in all_cols)
    update_cols = [c for c in all_cols if c != "TIMESTAMP_MS"]
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
        pgsql.Identifier("TIMESTAMP_MS"),
        set_clause,
    )

    tuples = [
        (
            r["timestamp_ms"], r["n_beats"], r["hr_bpm"], r["avg_rr_ms"],
            r["min_rr_ms"], r["max_rr_ms"], r["stddev_rr_ms"], r["rmssd_ms"],
            r["ln_rmssd"], r["vagal_index"], r["rmssd_pct"], r["sdnn_ms"],
            r["rmssd_sdnn_ratio"], r["vagal_balance"], r["pnn50"],
            r["vlf_ms2"], r["lf_ms2"], r["hf_ms2"],
            r["ulf_ms2"], r["ulf1_ms2"], r["ulf2_ms2"],
            r["lf_hf_ratio"], r["b7b8_dom"], r["b7b8_off"], r["dfa_alpha1"],
            datetime.fromtimestamp(r["timestamp_ms"] / 1000.0, tz=timezone.utc),
        )
        for r in rows
    ]

    with pg_conn.cursor() as cur:
        execute_values(cur, insert_stmt, tuples, page_size=5000)

        cur.execute(
            pgsql.SQL('SELECT COUNT(*) FROM {}.{}').format(
                pgsql.Identifier(PG_SCHEMA),
                pgsql.Identifier(PG_TABLE),
            )
        )
        total = cur.fetchone()[0]

        cur.execute(
            pgsql.SQL(
                'SELECT "TIMESTAMP_MS", "N_BEATS", "HR_BPM", "RMSSD_MS", '
                '"LF_HF_RATIO", "DFA_ALPHA1" '
                'FROM {}.{} WHERE "RMSSD_MS" IS NOT NULL '
                'ORDER BY "RMSSD_MS" DESC LIMIT 1'
            ).format(
                pgsql.Identifier(PG_SCHEMA),
                pgsql.Identifier(PG_TABLE),
            )
        )
        sample = cur.fetchone()
    pg_conn.commit()
    return total, sample

def main():
    parser = argparse.ArgumentParser(description="HRV minute aggregation")
    parser.add_argument("--device-id", type=int, default=None)
    parser.add_argument(
        "--lf-hf",
        action="store_true",
        help="Enable LF/HF/VLF spectral analysis via cubic-spline resampling + Welch PSD (default: off, slow)",
    )
    parser.add_argument(
        "--dfa",
        action="store_true",
        help="Enable DFA alpha1 computation (default: off)",
    )
    parser.add_argument(
        "--ulf",
        action="store_true",
        help="Enable ULF spectral analysis (2 h sliding window, Lomb-Scargle on "
             "irregular RR samples). Outputs ULF_MS2 + ULF1_MS2 + ULF2_MS2. "
             "Default: off (very slow).",
    )
    parser.add_argument(
        "--limit-minutes",
        type=int,
        default=None,
        help=(
            "Limit processing to the first N minute bins. "
            "Intended for performance and integrity test runs on a small "
            "slice of the data; omit for full production runs."
        ),
    )
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"ERROR: database not found: {DB_PATH}")
        sys.exit(1)

    t_total = time.monotonic()

    pg_conn = connect_pg()
    try:
        ensure_hrv_table(pg_conn)
        existing_minutes = get_existing_minutes(pg_conn)
        print(f"Existing HRV minutes in Postgres: {len(existing_minutes)}")

        # Incremental RR load: when the target already has data, only
        # read beats within one ULF window (2 h) before the newest stored
        # minute. Backward-looking windows for any genuinely new minute
        # still find the beats they need, while SQLite does not have to
        # return the full history on every run.
        min_ts_ms = None
        if existing_minutes:
            min_ts_ms = max(existing_minutes) - ULF_WINDOW_MS

        t0 = time.monotonic()
        rr_data, device_id, device_name = load_rr_data(
            DB_PATH, args.device_id, min_ts_ms=min_ts_ms,
        )
        if not rr_data:
            print("No new RR intervals to process.")
            print(f"Total runtime: {time.monotonic() - t_total:.2f}s")
            return

        span = f" (from ts >= {min_ts_ms})" if min_ts_ms is not None else ""
        print(
            f"Loaded {len(rr_data)} RR intervals{span} from device "
            f"{device_id} ({device_name}) [{time.monotonic() - t0:.2f}s]"
        )
        t_start = datetime.fromtimestamp(rr_data[0][0] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
        t_end = datetime.fromtimestamp(rr_data[-1][0] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Time range: {t_start} - {t_end}")

        minute_count = len({(ts // 60000) for ts, _ in rr_data})
        print(f"Processing up to {minute_count} minute bins "
              f"({len(existing_minutes)} already in target -> skipped)...")

        t0 = time.monotonic()
        rows = compute_minute_metrics(
            rr_data,
            enable_lf_hf=args.lf_hf,
            enable_dfa=args.dfa,
            enable_ulf=args.ulf,
            limit_minutes=args.limit_minutes,
            skip_minutes=existing_minutes,
        )
        print(f"Minute metrics computed: {len(rows)} rows [{time.monotonic() - t0:.2f}s]")

        t0 = time.monotonic()
        total, sample = write_results_pg(pg_conn, rows)
        print(
            f"Upserted {len(rows)} rows into {PG_SCHEMA}.\"{PG_TABLE}\" "
            f"(total now {total}) [{time.monotonic() - t0:.2f}s]"
        )
        print(f"Total runtime: {time.monotonic() - t_total:.2f}s")

        if sample:
            ts, n, hr, rmssd, lfhf, dfa = sample
            hr_str = f"{hr:.1f}" if hr is not None else "None"
            rmssd_str = f"{rmssd:.1f}" if rmssd is not None else "None"
            print(
                f"Sample (max RMSSD): ts={ts} n_beats={n} hr={hr_str} "
                f"rmssd={rmssd_str} lf_hf={lfhf} dfa_alpha1={dfa}"
            )
    finally:
        pg_conn.close()


if __name__ == "__main__":
    main()