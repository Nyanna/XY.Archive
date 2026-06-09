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
import time
from datetime import datetime, timezone
from typing import NamedTuple

import numpy as np
import psycopg2
from astropy.timeseries import LombScargle
from psycopg2 import sql as pgsql
from psycopg2.extras import execute_values
from scipy.interpolate import CubicSpline
from scipy.signal import butter, csd, filtfilt, hilbert, welch

from rr_quality import correct_artifacts, nn_time_domain, quality_mask

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

FS_CPC = 2.0         # Hz for CPC resampling (Thomas et al. 2005)
CPC_MIN_BEATS = 60  # minimum beats required in CPC window
CPC_NPERSEG = 256              # Welch segment length (128 s at 2 Hz)
CPC_GAP_THRESHOLD_MS = 2000    # gaps > 2 s get linear (not cubic) interpolation
CPC_MAX_GAP_FRACTION = 0.30    # reject window if >30% of duration is in gaps
CPC_WINDOW_MS = 7 * 60 * 1000       # total CPC analysis window
CPC_HALF_WIN_STABILITY_MS = 150_000  # ±2.5 min for HF_PEAK_STABILITY rolling SD
# Minutes of forward context needed before a row's HF_PEAK_STABILITY can be
# finalized (= half-window rounded up to whole minutes). Drives both the
# per-batch deferred tail and the cross-run boundary correction.
STABILITY_OVERLAP = max(1, CPC_HALF_WIN_STABILITY_MS // 60000 + 1)

# Artifact handling lives in the shared rr_quality module:
#   Layer 1 (correct_artifacts): local-median point-ectopic correction,
#     now applied to the time-domain base metrics (RMSSD/pNN50/SDNN) as
#     well, not only the PSD path.
#   Layer 2 (apply_quality_filter, in load_rr_data): block exclusion of
#     sustained signal corruption (strap slip) before any binning.
# The local-median detector (not Malik) is deliberate: ESC/NASPE 1996
# leaves the detection rule open; nearest-neighbor (Malik) rules misclassify
# physiological RSA swings -- especially in the REM-dominated second half of
# night -- as artifacts, whereas a local median smooths across RSA so only
# true spikes (ectopics / missed beats) deviate.

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


def load_rr_data(pg_conn, min_ts_ms=None):
    with pg_conn.cursor() as cur:
        query = (
            'SELECT (EXTRACT(EPOCH FROM "timestamp_at") * 1000)::bigint, "RR_MILLIS" '
            'FROM "HEART_RR_INTERVAL_SAMPLE"'
        )
        params = []
        if min_ts_ms is not None:
            query += ' WHERE "timestamp_at" >= %s'
            params.append(datetime.fromtimestamp(min_ts_ms / 1000.0, tz=timezone.utc))
        query += ' ORDER BY "timestamp_at", "SEQ"'

        cur.execute(query, params)
        raw = cur.fetchall()

    sane = [(int(ts), int(rr)) for ts, rr in raw if MIN_RR <= int(rr) <= MAX_RR]
    if not sane:
        return sane

    # Layer 2: exclude sustained corruption blocks (strap slip) up front,
    # so every downstream window sees only quality-validated beats. Removed
    # beats become time gaps, which all metrics tolerate.
    ts_arr = np.fromiter((s[0] for s in sane), dtype=np.int64, count=len(sane))
    rr_arr = np.fromiter((s[1] for s in sane), dtype=np.int64, count=len(sane))
    keep, info = quality_mask(ts_arr, rr_arr)
    if info["n_removed"]:
        pct = info["n_removed"] / info["n_total"] * 100.0
        print(
            f"  Quality filter: removed {info['n_removed']:,}/{info['n_total']:,} "
            f"beats ({pct:.1f}%) in {info['n_blocks']} block(s)"
        )
    ts_k = ts_arr[keep].tolist()
    rr_k = rr_arr[keep].tolist()
    return list(zip(ts_k, rr_k))


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


def _resample_rr_2hz(ts_ms, rr_ms):
    """Resample artifact-corrected RR series to FS_CPC Hz uniform grid.

    Returns (t_uniform_s, y_uniform) or None if window is degenerate.
    Large gaps (> CPC_GAP_THRESHOLD_MS) are filled with linear interpolation;
    the window is rejected if gaps exceed CPC_MAX_GAP_FRACTION of duration.
    """
    ts = np.asarray(ts_ms, dtype=np.float64)
    rr = np.asarray(rr_ms, dtype=np.float64)

    rr = correct_artifacts(rr)
    if rr is None or len(rr) < 20:
        return None

    t_rel = (ts - ts[0]) / 1000.0
    duration = float(t_rel[-1])
    if duration < 30.0:
        return None

    ts_diffs_ms = np.diff(ts)
    gap_mask = ts_diffs_ms > CPC_GAP_THRESHOLD_MS
    if gap_mask.any():
        gap_s = float(ts_diffs_ms[gap_mask].sum()) / 1000.0
        if gap_s / duration > CPC_MAX_GAP_FRACTION:
            return None

    n_uniform = max(2, int(duration * FS_CPC))
    t_uniform = np.linspace(0.0, duration, n_uniform)
    y_linear = np.interp(t_uniform, t_rel, rr)

    try:
        cs = CubicSpline(t_rel, rr)
        y = cs(t_uniform)
    except Exception:
        return t_uniform, y_linear

    if gap_mask.any():
        for gi in np.flatnonzero(gap_mask):
            g_start = t_rel[gi]
            g_end = t_rel[gi + 1]
            in_gap = (t_uniform > g_start) & (t_uniform < g_end)
            if in_gap.any():
                y[in_gap] = y_linear[in_gap]

    return t_uniform, y


def compute_cpc_metrics(ts_ms, rr_ms):
    """Compute CPC LFC-ratio and HF peak frequency from an RR window.

    Cardiopulmonary Coupling per Thomas et al. 2005, with RSA amplitude
    envelope as EDR surrogate (Pinna et al. 2007).

    Returns (cpc_lfc_ratio, hf_peak_freq_hz):
      cpc_lfc_ratio: LFC/(LFC+HFC) in [0,1]; high=REM/unstable, low=stable NREM.
      hf_peak_freq_hz: dominant 0.15–0.4 Hz peak with parabolic interpolation;
          used by caller to build HF_PEAK_STABILITY rolling SD.
    Both None on degenerate input; cpc_lfc_ratio may be None even when
    hf_peak_freq_hz is valid (degenerate CPC but valid spectrum).
    """
    result = _resample_rr_2hz(ts_ms, rr_ms)
    if result is None:
        return None, None
    _t, r = result
    n = len(r)

    nyq = FS_CPC / 2.0
    bp_lo = 0.15 / nyq
    bp_hi = min(0.40 / nyq, 0.999)
    try:
        b, a = butter(3, [bp_lo, bp_hi], btype='bandpass')
        r_bp = filtfilt(b, a, r)
        e = np.abs(hilbert(r_bp))
    except Exception:
        return None, None

    nperseg = min(CPC_NPERSEG, n // 4)
    if nperseg < 32:
        return None, None

    try:
        f, srr = welch(r, fs=FS_CPC, nperseg=nperseg, window='hann',
                       scaling='density', detrend='constant')
        _, see = welch(e, fs=FS_CPC, nperseg=nperseg, window='hann',
                       scaling='density', detrend='constant')
        _, sre = csd(r, e, fs=FS_CPC, nperseg=nperseg, window='hann',
                     scaling='density', detrend='constant')
    except Exception:
        return None, None

    with np.errstate(divide='ignore', invalid='ignore'):
        denom = srr * see
        gamma2 = np.where(denom > 0.0, np.abs(sre) ** 2 / denom, 0.0)

    cpc_f = gamma2 * np.abs(sre)

    lfc_mask = (f >= 0.01) & (f <= 0.10)
    hfc_mask = (f >= 0.10) & (f <= 0.40)
    lfc = float(_TRAPZ(cpc_f[lfc_mask], f[lfc_mask])) if lfc_mask.any() else 0.0
    hfc = float(_TRAPZ(cpc_f[hfc_mask], f[hfc_mask])) if hfc_mask.any() else 0.0

    total_cpc = lfc + hfc
    cpc_lfc_ratio = lfc / total_cpc if total_cpc > 0.0 else None

    # HF peak with parabolic interpolation for sub-bin resolution
    hf_peak_freq = None
    hf_mask = (f >= 0.15) & (f <= 0.40)
    if hf_mask.any():
        hf_srr = srr[hf_mask]
        hf_f = f[hf_mask]
        peak_i = int(np.argmax(hf_srr))
        if 0 < peak_i < len(hf_srr) - 1:
            y0 = hf_srr[peak_i - 1]
            y1 = hf_srr[peak_i]
            y2 = hf_srr[peak_i + 1]
            df_bin = (hf_f[-1] - hf_f[0]) / max(len(hf_f) - 1, 1)
            denom2 = y0 + y2 - 2.0 * y1
            if denom2 != 0.0 and df_bin > 0.0:
                delta = 0.5 * (y0 - y2) / denom2
                hf_peak_freq = float(hf_f[peak_i] + delta * df_bin)
            else:
                hf_peak_freq = float(hf_f[peak_i])
        else:
            hf_peak_freq = float(hf_f[peak_i])

    return cpc_lfc_ratio, hf_peak_freq


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


def _compute_basic(rr: np.ndarray, ts_minute: np.ndarray) -> dict:
    """Time-domain and vagal metrics for one minute slice.

    rr: float array of RR intervals (ms) for the minute
    ts_minute: int64 array of beat timestamps (ms) for the minute
    """
    mean_rr = float(rr.mean())
    rmssd, sdnn, pnn50 = nn_time_domain(ts_minute, rr)

    if rmssd is not None:
        ln_rmssd = math.log(rmssd) if rmssd > 0 else None
        vagal_index = (
            ln_rmssd / math.log(mean_rr)
            if (ln_rmssd is not None and mean_rr > 1) else None
        )
        rmssd_pct = rmssd / mean_rr * 100.0 if mean_rr > 0 else None
        rmssd_sdnn_ratio = rmssd / sdnn if sdnn and sdnn > 0 else None
        vagal_balance = (
            (rmssd / sdnn) / VAGAL_BALANCE_REF
            if (sdnn and sdnn > 0 and rmssd > 0) else None
        )
    else:
        ln_rmssd = vagal_index = rmssd_pct = rmssd_sdnn_ratio = vagal_balance = None

    return {
        "hr_bpm":          60000.0 / mean_rr if mean_rr > 0 else None,
        "avg_rr_ms":       mean_rr,
        "min_rr_ms":       int(rr.min()),
        "max_rr_ms":       int(rr.max()),
        "stddev_rr_ms":    float(rr.std(ddof=0)),
        "rmssd_ms":        rmssd,
        "ln_rmssd":        ln_rmssd,
        "vagal_index":     vagal_index,
        "rmssd_pct":       rmssd_pct,
        "sdnn_ms":         sdnn,
        "rmssd_sdnn_ratio": rmssd_sdnn_ratio,
        "vagal_balance":   vagal_balance,
        "pnn50":           pnn50,
    }


def _compute_spectral(
    all_ts: np.ndarray,
    all_rr: np.ndarray,
    minute_start: int,
    lf_hf_win_ms: int,
    vlf_win_ms: int,
) -> tuple:
    """LF, HF, VLF band power + LF/HF ratio + B7B8 axes.

    LF and HF share one Welch PSD on lf_hf_win_ms (centered at T+30s,
    i.e. 2/5 before, 3/5 after minute_start). VLF uses vlf_win_ms with
    the same T+30s convention (7/15 before, 8/15 after). B7B8 axes are
    derived from the three bands internally.

    Returns (lf, hf, vlf, lfhf, b7b8_dom, b7b8_off) — all may be None.
    """
    lf_hf_before = lf_hf_win_ms * 2 // 5
    i_lo = int(np.searchsorted(all_ts, minute_start - lf_hf_before, side="left"))
    i_hi = int(np.searchsorted(all_ts, minute_start + (lf_hf_win_ms - lf_hf_before), side="left"))

    lf = hf = lfhf = None
    if (i_hi - i_lo) >= LFHF_MIN_BEATS:
        bands = compute_band_power(
            all_rr[i_lo:i_hi], [('lf', 0.04, 0.15), ('hf', 0.15, 0.40)]
        )
        lf, hf = bands['lf'], bands['hf']
        lfhf = lf / hf if (lf is not None and hf is not None and hf > 0) else None

    vlf_before = vlf_win_ms * 7 // 15
    i15_lo = int(np.searchsorted(all_ts, minute_start - vlf_before, side="left"))
    i15_hi = int(np.searchsorted(all_ts, minute_start + (vlf_win_ms - vlf_before), side="left"))

    vlf = None
    if (i15_hi - i15_lo) >= VLF_MIN_BEATS:
        vlf = compute_band_power(
            all_rr[i15_lo:i15_hi], [('vlf', 0.0033, 0.04)], detrend="linear"
        )['vlf']

    b7b8_dom = b7b8_off = None
    if lf is not None and hf is not None and vlf is not None:
        total_power = lf + hf + vlf
        if total_power >= TOTAL_MIN:
            lf_plus_hf = lf + hf
            b7b8_dom = 0.0 if lf_plus_hf == 0 else (hf - lf) / lf_plus_hf
            b7b8_off = vlf / total_power

    return lf, hf, vlf, lfhf, b7b8_dom, b7b8_off


def _compute_ulf(
    all_ts: np.ndarray,
    all_rr: np.ndarray,
    minute_start: int,
    win_ms: int,
) -> tuple:
    """ULF band powers from a symmetric window around minute_start.

    Returns (ulf_ms2, ulf1_ms2, ulf2_ms2) — all may be None.
    """
    half = win_ms // 2
    i_lo = int(np.searchsorted(all_ts, minute_start - half, side="left"))
    i_hi = int(np.searchsorted(all_ts, minute_start + half, side="left"))

    if (i_hi - i_lo) < ULF_MIN_BEATS:
        return None, None, None

    res = compute_ulf_power(
        all_ts[i_lo:i_hi].astype(np.int64),
        all_rr[i_lo:i_hi].astype(float),
    )
    if res is None:
        return None, None, None
    return res["ulf_ms2"], res["ulf1_ms2"], res["ulf2_ms2"]


def _compute_dfa(all_rr: np.ndarray, hi: int, win_beats: int) -> float | None:
    """DFA alpha1 from the last win_beats RR intervals ending at index hi."""
    start = hi - win_beats if hi >= win_beats else 0
    return compute_dfa_alpha1(all_rr[start:hi])


def _compute_cpc_minute(
    all_ts: np.ndarray,
    all_rr: np.ndarray,
    minute_start: int,
    win_ms: int,
) -> tuple:
    """CPC LFC-ratio and HF peak frequency from a window centered at T+30s.

    Window placement: 3/7 before, 4/7 after minute_start.
    Returns (cpc_lfc_ratio, hf_peak_freq) — both may be None.
    """
    before = win_ms * 3 // 7
    i_lo = int(np.searchsorted(all_ts, minute_start - before, side="left"))
    i_hi = int(np.searchsorted(all_ts, minute_start + (win_ms - before), side="left"))

    if (i_hi - i_lo) < CPC_MIN_BEATS:
        return None, None
    return compute_cpc_metrics(all_ts[i_lo:i_hi], all_rr[i_lo:i_hi])


def _finalize_hf_peak_stability(
    target_rows: list,
    peak_context: list,
    half_win_ms: int,
) -> None:
    """Compute HF_PEAK_STABILITY in-place for target_rows.

    peak_context: list of (timestamp_ms, hf_peak_freq|None) tuples covering
        the full window range including any lookahead. Reads _hf_peak_freq from
        target_rows, fills hf_peak_stability, and removes _hf_peak_freq.
    """
    ts_ctx = np.array([t for t, _ in peak_context], dtype=np.int64)
    peak_arr = np.array(
        [f if f is not None else np.nan for _, f in peak_context],
        dtype=float,
    )
    for r in target_rows:
        in_win = np.abs(ts_ctx - r["timestamp_ms"]) <= half_win_ms
        valid = peak_arr[in_win]
        valid = valid[~np.isnan(valid)]
        r["hf_peak_stability"] = float(np.std(valid, ddof=0)) if len(valid) >= 2 else None
        del r["_hf_peak_freq"]


def compute_minute_metrics(
    all_ts, all_rr,
    sorted_minutes, minute_lo, minute_hi, minute_counts,
    skip_minutes=None,
):
    """Process a slice of minute bins. Returns (rows, perf_dict).

    all_ts/all_rr: full RR arrays (needed for windowed spectral/ULF/CPC).
    sorted_minutes/minute_lo/minute_hi/minute_counts: pre-sliced index arrays.
    Rows are returned with _hf_peak_freq populated and hf_peak_stability=None;
    the caller is responsible for running _finalize_hf_peak_stability.
    skip_minutes: set of minute-start timestamps (ms) to skip.
    """
    skip_minutes = skip_minutes or set()
    t0 = time.monotonic()
    t_basic = t_spectral = t_ulf = t_dfa = t_cpc = 0.0
    n_skipped = 0
    results = []

    n_bins = len(sorted_minutes)
    for mi in range(n_bins):
        minute_start = int(sorted_minutes[mi])
        if minute_start in skip_minutes:
            n_skipped += 1
            continue

        n_beats = int(minute_counts[mi])
        if n_beats < MIN_BEATS_PER_MINUTE:
            continue

        lo = int(minute_lo[mi])
        hi = int(minute_hi[mi])

        t = time.monotonic()
        basic = _compute_basic(all_rr[lo:hi].astype(float), all_ts[lo:hi])
        t_basic += time.monotonic() - t

        t = time.monotonic()
        lf, hf, vlf, lfhf, b7b8_dom, b7b8_off = _compute_spectral(
            all_ts, all_rr, minute_start, LFHF_WINDOW_MS, VLF_WINDOW_MS
        )
        t_spectral += time.monotonic() - t

        t = time.monotonic()
        ulf_ms2, ulf1_ms2, ulf2_ms2 = _compute_ulf(
            all_ts, all_rr, minute_start, ULF_WINDOW_MS
        )
        t_ulf += time.monotonic() - t

        t = time.monotonic()
        dfa_alpha1 = _compute_dfa(all_rr, hi, DFA_WINDOW)
        t_dfa += time.monotonic() - t

        t = time.monotonic()
        cpc_lfc_ratio, hf_peak_freq = _compute_cpc_minute(
            all_ts, all_rr, minute_start, CPC_WINDOW_MS
        )
        t_cpc += time.monotonic() - t

        results.append({
            "timestamp_ms":   minute_start,
            "n_beats":        n_beats,
            **basic,
            "vlf_ms2":        vlf,
            "lf_ms2":         lf,
            "hf_ms2":         hf,
            "ulf_ms2":        ulf_ms2,
            "ulf1_ms2":       ulf1_ms2,
            "ulf2_ms2":       ulf2_ms2,
            "lf_hf_ratio":    lfhf,
            "b7b8_dom":       b7b8_dom,
            "b7b8_off":       b7b8_off,
            "dfa_alpha1":     dfa_alpha1,
            "cpc_lfc_ratio":  cpc_lfc_ratio,
            "hf_peak_stability": None,
            "_hf_peak_freq":  hf_peak_freq,
        })

    perf = {
        "t_basic":    t_basic,
        "t_spectral": t_spectral,
        "t_ulf":      t_ulf,
        "t_dfa":      t_dfa,
        "t_cpc":      t_cpc,
        "t_loop":     time.monotonic() - t0,
        "n_skipped":  n_skipped,
    }
    return results, perf



PG_COLUMNS = [
    "N_BEATS", "HR_BPM", "AVG_RR_MS", "MIN_RR_MS", "MAX_RR_MS",
    "STDDEV_RR_MS", "RMSSD_MS", "LN_RMSSD", "VAGAL_INDEX", "RMSSD_PCT", "SDNN_MS",
    "RMSSD_SDNN_RATIO", "VAGAL_BALANCE", "PNN50",
    "VLF_MS2", "LF_MS2", "HF_MS2", "ULF_MS2", "ULF1_MS2", "ULF2_MS2",
    "LF_HF_RATIO", "B7B8_DOM", "B7B8_OFF", "DFA_ALPHA1",
    "CPC_LFC_RATIO", "HF_PEAK_STABILITY",
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
            {PG_AT_COLUMN}     TIMESTAMPTZ NOT NULL PRIMARY KEY,
            "N_BEATS"          SMALLINT NOT NULL,
            "HR_BPM"           REAL,
            "AVG_RR_MS"        REAL,
            "MIN_RR_MS"        SMALLINT,
            "MAX_RR_MS"        SMALLINT,
            "STDDEV_RR_MS"     REAL,
            "RMSSD_MS"         REAL,
            "LN_RMSSD"         REAL,
            "VAGAL_INDEX"      REAL,
            "RMSSD_PCT"        REAL,
            "SDNN_MS"          REAL,
            "RMSSD_SDNN_RATIO" REAL,
            "VAGAL_BALANCE"    REAL,
            "PNN50"            REAL,
            "VLF_MS2"          REAL,
            "LF_MS2"           REAL,
            "HF_MS2"           REAL,
            "ULF_MS2"          REAL,
            "ULF1_MS2"         REAL,
            "ULF2_MS2"         REAL,
            "LF_HF_RATIO"      REAL,
            "B7B8_DOM"         REAL,
            "B7B8_OFF"         REAL,
            "DFA_ALPHA1"       REAL,
            "CPC_LFC_RATIO"    REAL,
            "HF_PEAK_STABILITY" REAL
        )
    '''
    with pg_conn.cursor() as cur:
        cur.execute(ddl)
        # Migrate existing tables: idempotent column additions
        cur.execute(
            f'ALTER TABLE "{PG_SCHEMA}"."{PG_TABLE}" '
            f'ADD COLUMN IF NOT EXISTS "CPC_LFC_RATIO" REAL'
        )
        cur.execute(
            f'ALTER TABLE "{PG_SCHEMA}"."{PG_TABLE}" '
            f'ADD COLUMN IF NOT EXISTS "HF_PEAK_STABILITY" REAL'
        )
    pg_conn.commit()


def get_max_source_rr_ts(pg_conn):
    """Return MAX(timestamp_at) of the source RR table as ms epoch int."""
    with pg_conn.cursor() as cur:
        cur.execute('SELECT MAX("timestamp_at") FROM "HEART_RR_INTERVAL_SAMPLE"')
        row = cur.fetchone()
    if row and row[0] is not None:
        return int(row[0].timestamp() * 1000)
    return None


def get_max_stored_minute(pg_conn):
    """Return the MAX timestamp_ms_at as an int (ms epoch), or None if table empty."""
    with pg_conn.cursor() as cur:
        cur.execute(
            pgsql.SQL('SELECT MAX({}) FROM {}.{}').format(
                pgsql.Identifier(PG_AT_COLUMN),
                pgsql.Identifier(PG_SCHEMA),
                pgsql.Identifier(PG_TABLE),
            )
        )
        row = cur.fetchone()
    if row and row[0] is not None:
        return int(row[0].timestamp() * 1000)
    return None


def get_existing_minutes(pg_conn, since_ms=None):
    """Return set of minute starts (ms epoch, int) already stored.

    since_ms: if given, only return minutes >= that timestamp (ms epoch).
    For incremental runs pass the RR load cutoff so the result set covers
    only the overlap window (≤ largest analysis window), not the full history.

    Internal logic still keys minutes by integer ms; the on-disk PK is a
    timestamptz, so we project epoch-ms via EXTRACT.
    """
    with pg_conn.cursor() as cur:
        if since_ms is not None:
            cur.execute(
                pgsql.SQL(
                    'SELECT (EXTRACT(EPOCH FROM {col}) * 1000)::bigint '
                    'FROM {schema}.{table} WHERE {col} >= %s'
                ).format(
                    col=pgsql.Identifier(PG_AT_COLUMN),
                    schema=pgsql.Identifier(PG_SCHEMA),
                    table=pgsql.Identifier(PG_TABLE),
                ),
                (datetime.fromtimestamp(since_ms / 1000.0, tz=timezone.utc),),
            )
        else:
            cur.execute(
                pgsql.SQL(
                    'SELECT (EXTRACT(EPOCH FROM {col}) * 1000)::bigint '
                    'FROM {schema}.{table}'
                ).format(
                    col=pgsql.Identifier(PG_AT_COLUMN),
                    schema=pgsql.Identifier(PG_SCHEMA),
                    table=pgsql.Identifier(PG_TABLE),
                )
            )
        return {int(r[0]) for r in cur.fetchall()}


def write_results_pg(pg_conn, rows):
    if not rows:
        return 0, None

    all_cols = [PG_AT_COLUMN] + PG_COLUMNS
    col_list = pgsql.SQL(", ").join(pgsql.Identifier(c) for c in all_cols)
    update_cols = [c for c in all_cols if c != PG_AT_COLUMN]
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
        pgsql.Identifier(PG_AT_COLUMN),
        set_clause,
    )

    tuples = [
        (
            datetime.fromtimestamp(r["timestamp_ms"] / 1000.0, tz=timezone.utc),
            r["n_beats"], r["hr_bpm"], r["avg_rr_ms"],
            r["min_rr_ms"], r["max_rr_ms"], r["stddev_rr_ms"], r["rmssd_ms"],
            r["ln_rmssd"], r["vagal_index"], r["rmssd_pct"], r["sdnn_ms"],
            r["rmssd_sdnn_ratio"], r["vagal_balance"], r["pnn50"],
            r["vlf_ms2"], r["lf_ms2"], r["hf_ms2"],
            r["ulf_ms2"], r["ulf1_ms2"], r["ulf2_ms2"],
            r["lf_hf_ratio"], r["b7b8_dom"], r["b7b8_off"], r["dfa_alpha1"],
            r.get("cpc_lfc_ratio"), r.get("hf_peak_stability"),
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
                'SELECT {}, "N_BEATS", "HR_BPM", "RMSSD_MS", '
                '"LF_HF_RATIO", "DFA_ALPHA1" '
                'FROM {}.{} WHERE "RMSSD_MS" IS NOT NULL '
                'ORDER BY "RMSSD_MS" DESC LIMIT 1'
            ).format(
                pgsql.Identifier(PG_AT_COLUMN),
                pgsql.Identifier(PG_SCHEMA),
                pgsql.Identifier(PG_TABLE),
            )
        )
        sample = cur.fetchone()
    pg_conn.commit()
    return total, sample


def update_hf_peak_stability_pg(pg_conn, updates):
    """UPDATE hf_peak_stability for a list of (timestamp_ms, value) pairs.

    Used to correct boundary rows from a previous run without overwriting
    the other columns (which are not available for already-skipped minutes).
    """
    if not updates:
        return
    stmt = pgsql.SQL(
        'UPDATE {}.{} SET "HF_PEAK_STABILITY" = %s WHERE {} = %s'
    ).format(
        pgsql.Identifier(PG_SCHEMA),
        pgsql.Identifier(PG_TABLE),
        pgsql.Identifier(PG_AT_COLUMN),
    )
    with pg_conn.cursor() as cur:
        cur.executemany(
            stmt,
            [
                (stab, datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc))
                for ts_ms, stab in updates
            ],
        )
    pg_conn.commit()


class MinuteBins(NamedTuple):
    """RR samples grouped into per-minute bins for windowed processing.

    all_ts/all_rr: full int64 RR arrays (windowed metrics index into them).
    sorted_minutes: unique minute-start timestamps (ms), ascending.
    minute_lo/minute_hi: [lo, hi) slice bounds into all_ts/all_rr per bin.
    minute_counts: beat count per bin.
    total_minutes: number of bins to process (after any --limit-minutes cap).
    """
    all_ts: np.ndarray
    all_rr: np.ndarray
    sorted_minutes: np.ndarray
    minute_lo: np.ndarray
    minute_hi: np.ndarray
    minute_counts: np.ndarray
    total_minutes: int


def parse_args():
    parser = argparse.ArgumentParser(description="HRV minute aggregation")
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full recompute: load all RR data from SQLite (no incremental "
             "cutoff) and overwrite all minutes in Postgres (no skip).",
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
    return parser.parse_args()


def plan_incremental_load(pg_conn, full):
    """Decide the RR-load cutoff and skip-set for this run.

    Returns (min_ts_ms, existing_minutes), where min_ts_ms is the SQLite load
    cutoff (None = load everything) and existing_minutes is the set of minute
    starts already stored within the overlap window. Returns None when the
    source RR table holds no minutes newer than what is already stored
    (caller should treat None as "nothing to do").
    """
    t0 = time.monotonic()
    max_stored_ms = get_max_stored_minute(pg_conn)

    min_ts_ms = None
    if full or max_stored_ms is None:
        existing_minutes = set()
    else:
        max_source_ms = get_max_source_rr_ts(pg_conn)
        if max_source_ms is not None and (max_source_ms // 60000) * 60000 <= max_stored_ms:
            print(
                f"Max stored HRV minute: "
                f"{datetime.fromtimestamp(max_stored_ms / 1000.0, tz=timezone.utc).isoformat()} | "
                f"source up to date, nothing to do [{time.monotonic() - t0:.2f}s]"
            )
            return None
        min_ts_ms = max_stored_ms - ULF_WINDOW_MS
        existing_minutes = get_existing_minutes(pg_conn, since_ms=min_ts_ms)

    max_stored_str = (
        datetime.fromtimestamp(max_stored_ms / 1000.0, tz=timezone.utc).isoformat()
        if max_stored_ms is not None else "none"
    )
    print(
        f"Max stored HRV minute: {max_stored_str} | "
        f"overlap window skip-set: {len(existing_minutes)} minutes [{time.monotonic() - t0:.2f}s]"
    )
    return min_ts_ms, existing_minutes


def load_rr_window(pg_conn, min_ts_ms):
    """Load RR intervals (incremental cutoff applied) and report the range.

    Returns the rr_data list of (ts_ms, rr_ms) tuples; empty if there is
    nothing new to process.
    """
    t0 = time.monotonic()
    rr_data = load_rr_data(pg_conn, min_ts_ms=min_ts_ms)
    if not rr_data:
        print("No new RR intervals to process.")
        return rr_data

    span = f" (from ts >= {min_ts_ms})" if min_ts_ms is not None else ""
    print(f"Loaded {len(rr_data)} RR intervals{span} [{time.monotonic() - t0:.2f}s]")
    t_start = datetime.fromtimestamp(rr_data[0][0] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
    t_end = datetime.fromtimestamp(rr_data[-1][0] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
    print(f"Time range: {t_start} - {t_end}")
    return rr_data


def build_minute_bins(rr_data, n_existing=0, limit_minutes=None) -> MinuteBins:
    """Bin loaded RR samples by minute. See MinuteBins for the fields.

    n_existing is only used for the progress line (count already in target).
    """
    t0 = time.monotonic()
    n_rr = len(rr_data)
    all_ts = np.fromiter((r[0] for r in rr_data), dtype=np.int64, count=n_rr)
    all_rr = np.fromiter((r[1] for r in rr_data), dtype=np.int64, count=n_rr)
    minute_of_beat = (all_ts // 60000) * 60000
    sorted_minutes, minute_lo, minute_counts = np.unique(
        minute_of_beat, return_index=True, return_counts=True
    )
    minute_hi = minute_lo + minute_counts
    total_minutes = len(sorted_minutes)
    if limit_minutes and limit_minutes > 0:
        total_minutes = min(total_minutes, limit_minutes)
        print(f"  NOTE: processing limited to first {total_minutes} minute bins (--limit-minutes)")
    print(
        f"Minute binning done ({total_minutes} bins, "
        f"{n_existing} already in target -> skipped) "
        f"[{time.monotonic() - t0:.2f}s]"
    )
    return MinuteBins(
        all_ts, all_rr, sorted_minutes, minute_lo, minute_hi, minute_counts, total_minutes
    )


def compute_cross_run_peaks(bins: MinuteBins, existing_minutes):
    """CPC HF-peak frequencies for stored boundary minutes inside the loaded
    RR range.

    These are the last STABILITY_OVERLAP already-stored minutes that overlap
    the freshly loaded RR data; their HF_PEAK_STABILITY was computed in a
    prior run without forward context and is corrected once the first batch
    provides it. Returns a list of (timestamp_ms, hf_peak_freq) tuples.
    """
    rr_min_ms = int(bins.all_ts[0])
    boundary = sorted(m for m in existing_minutes if m >= rr_min_ms)[-STABILITY_OVERLAP:]
    peaks = []
    for minute_ms in boundary:
        _, hf_peak_freq = _compute_cpc_minute(
            bins.all_ts, bins.all_rr, minute_ms, CPC_WINDOW_MS
        )
        peaks.append((minute_ms, hf_peak_freq))
    if peaks:
        print(f"  Cross-run boundary: {len(peaks)} minutes queued for stability update")
    return peaks


def process_batches(pg_conn, bins: MinuteBins, existing_minutes, cross_run_peaks):
    """Run the batched compute -> finalize -> write pipeline.

    HF_PEAK_STABILITY needs forward context, so each batch's tail
    (STABILITY_OVERLAP minutes) is deferred and written only once the next
    batch has extended peak_context. cross_run_peaks are corrected after the
    first batch. Returns a stats dict for print_summary.
    """
    total_minutes = bins.total_minutes
    all_ts, all_rr = bins.all_ts, bins.all_rr
    batch_size = max(1, total_minutes // 20)

    acc_perf = {"t_basic": 0.0, "t_spectral": 0.0, "t_ulf": 0.0,
                "t_dfa": 0.0, "t_cpc": 0.0, "t_loop": 0.0}
    n_skipped_total = 0
    t_db_total = 0.0
    total_rows = 0
    last_total_db = 0
    last_sample = None
    # (timestamp_ms, hf_peak_freq) tuples — grows across all batches; seeded
    # with the cross-run boundary peaks so their stability can be recomputed.
    peak_context = list(cross_run_peaks)
    # Unfinalized rows from the previous batch (written only after the next
    # batch extends peak_context with future values)
    prev_tail = []
    t_outer_start = time.monotonic()

    print(f"  Progress: 0/{total_minutes} (0%) | elapsed 0.0s | db 0.0s")

    for batch_start in range(0, total_minutes, batch_size):
        batch_end = min(batch_start + batch_size, total_minutes)

        rows, perf = compute_minute_metrics(
            all_ts, all_rr,
            bins.sorted_minutes[batch_start:batch_end],
            bins.minute_lo[batch_start:batch_end],
            bins.minute_hi[batch_start:batch_end],
            bins.minute_counts[batch_start:batch_end],
            skip_minutes=existing_minutes,
        )

        # Extend context before finalizing prev_tail so it sees current batch
        peak_context.extend((r["timestamp_ms"], r["_hf_peak_freq"]) for r in rows)

        t_db = time.monotonic()

        # Finalize and write the previous batch's deferred tail now that
        # current batch rows are in peak_context
        if prev_tail:
            _finalize_hf_peak_stability(prev_tail, peak_context, CPC_HALF_WIN_STABILITY_MS)
            last_total_db, sample = write_results_pg(pg_conn, prev_tail)
            total_rows += len(prev_tail)
            if sample:
                last_sample = sample

        # Correct cross-run boundary rows using the now-extended context
        if cross_run_peaks:
            cr_rows = [{"timestamp_ms": ts, "_hf_peak_freq": f}
                       for ts, f in cross_run_peaks]
            _finalize_hf_peak_stability(cr_rows, peak_context, CPC_HALF_WIN_STABILITY_MS)
            update_hf_peak_stability_pg(
                pg_conn,
                [(r["timestamp_ms"], r["hf_peak_stability"]) for r in cr_rows],
            )
            cross_run_peaks = []

        t_db = time.monotonic() - t_db

        # Split current batch: finalize core now, defer tail to next iteration
        tail_size = min(STABILITY_OVERLAP, len(rows))
        core_rows = rows[:len(rows) - tail_size]
        prev_tail = rows[len(rows) - tail_size:]

        if core_rows:
            _finalize_hf_peak_stability(core_rows, peak_context, CPC_HALF_WIN_STABILITY_MS)
            t_db_core = time.monotonic()
            last_total_db, sample = write_results_pg(pg_conn, core_rows)
            t_db += time.monotonic() - t_db_core
            total_rows += len(core_rows)
            if sample:
                last_sample = sample

        t_db_total += t_db
        n_skipped_total += perf["n_skipped"]
        for k in acc_perf:
            acc_perf[k] += perf[k]

        elapsed = time.monotonic() - t_outer_start
        pct = batch_end / total_minutes * 100
        print(
            f"  Progress: {batch_end}/{total_minutes} ({pct:.0f}%) | "
            f"elapsed {elapsed:.1f}s | db {t_db:.1f}s"
        )

    # Finalize the last batch's tail — no future context available
    if prev_tail:
        _finalize_hf_peak_stability(prev_tail, peak_context, CPC_HALF_WIN_STABILITY_MS)
        t_db = time.monotonic()
        last_total_db, sample = write_results_pg(pg_conn, prev_tail)
        t_db = time.monotonic() - t_db
        t_db_total += t_db
        total_rows += len(prev_tail)
        if sample:
            last_sample = sample

    return {
        "acc_perf":        acc_perf,
        "n_skipped_total": n_skipped_total,
        "t_db_total":      t_db_total,
        "total_rows":      total_rows,
        "last_total_db":   last_total_db,
        "last_sample":     last_sample,
        "t_outer_start":   t_outer_start,
    }


def print_summary(stats):
    """Print the timing summary and upsert sample from a process_batches result."""
    acc_perf = stats["acc_perf"]
    print(f"  --- Timing summary ---")
    print(f"  Basic metrics:            {acc_perf['t_basic']:.2f}s")
    print(f"  Spectral (LF/HF/VLF):    {acc_perf['t_spectral']:.2f}s")
    print(f"  ULF (Lomb-Scargle, 2h):  {acc_perf['t_ulf']:.2f}s")
    print(f"  DFA alpha1:               {acc_perf['t_dfa']:.2f}s")
    print(f"  CPC (7-min win, 2 Hz):    {acc_perf['t_cpc']:.2f}s")
    print(f"  Compute total:            {acc_perf['t_loop']:.2f}s")
    print(f"  DB write total:           {stats['t_db_total']:.2f}s")
    if stats["n_skipped_total"]:
        print(f"  Skipped (already in target): {stats['n_skipped_total']}")
    print(
        f"Upserted {stats['total_rows']} rows into {PG_SCHEMA}.\"{PG_TABLE}\" "
        f"(total now {stats['last_total_db']}) [{time.monotonic() - stats['t_outer_start']:.2f}s]"
    )
    last_sample = stats["last_sample"]
    if last_sample:
        ts, n, hr, rmssd, lfhf, dfa = last_sample
        hr_str = f"{hr:.1f}" if hr is not None else "None"
        rmssd_str = f"{rmssd:.1f}" if rmssd is not None else "None"
        print(
            f"Sample (max RMSSD): ts={ts} n_beats={n} hr={hr_str} "
            f"rmssd={rmssd_str} lf_hf={lfhf} dfa_alpha1={dfa}"
        )


def main():
    args = parse_args()

    pg_conn = connect_pg()
    try:
        ensure_hrv_table(pg_conn)

        plan = plan_incremental_load(pg_conn, args.full)
        if plan is None:
            return
        min_ts_ms, existing_minutes = plan

        rr_data = load_rr_window(pg_conn, min_ts_ms)
        if not rr_data:
            return

        bins = build_minute_bins(
            rr_data, n_existing=len(existing_minutes), limit_minutes=args.limit_minutes
        )

        cross_run_peaks = compute_cross_run_peaks(bins, existing_minutes)
        stats = process_batches(pg_conn, bins, existing_minutes, cross_run_peaks)
        print_summary(stats)
    finally:
        pg_conn.close()


if __name__ == "__main__":
    main()