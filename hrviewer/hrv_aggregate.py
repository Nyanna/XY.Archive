#!/usr/bin/env python3
"""HRV minute aggregation from Gadgetbridge RR-interval samples.

Reads raw RR intervals from the Gadgetbridge SQLite database and
upserts the derived per-minute metrics into the target.
Only minutes that are not yet
present are computed; RR samples older than the largest
analysis window before the newest stored minute are not loaded from
SQLite to keep incremental runs cheap.
"""

import argparse
import math
import time
from datetime import datetime, timezone
from typing import NamedTuple

import numpy as np
from astropy.timeseries import LombScargle
from scipy.interpolate import CubicSpline
from scipy.signal import butter, csd, filtfilt, hilbert, welch

from rr_quality import correct_artifacts, nn_time_domain, quality_mask
import hive_io as be_io

# --- Hive (DuckDB/Parquet) I/O ------------------------------------
# Source series written by gadgetbridge_migrate.py.
RR_METRIC = "rr_interval_ms"
# Output: one metric per derived column, prefixed hrv_. Every stored
# minute writes hrv_n_beats, so it doubles as the presence marker used by
# the incremental skip-set and watermark logic. Minutes are the series
# timestamp (minute-start ms).
OUT_PREFIX = "hrv_"
PRESENCE_METRIC = OUT_PREFIX + "n_beats"

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


def load_rr_data(min_ts_ms=None):
    """Load RR intervals from Victoria Metrics as (ts_ms, rr) tuples.

    rr_interval_ms is a single series with unique, time-resolved per-beat
    timestamps (gadgetbridge_migrate.py lays each SEQ packet out around its
    device TIMESTAMP), so ascending timestamp order already reproduces the
    original device sequence.
    """
    ts_all, rr_all = be_io.load_rr_intervals(min_ts_ms=min_ts_ms)
    if ts_all.size == 0:
        return []

    sane_mask = (rr_all >= MIN_RR) & (rr_all <= MAX_RR)
    ts_arr = ts_all[sane_mask].astype(np.int64)
    rr_arr = rr_all[sane_mask].astype(np.int64)
    if ts_arr.size == 0:
        return []

    # Layer 2: exclude sustained corruption blocks (strap slip) up front,
    # so every downstream window sees only quality-validated beats. Removed
    # beats become time gaps, which all metrics tolerate.
    keep, info = quality_mask(ts_arr, rr_arr)
    if info["n_removed"]:
        pct = info["n_removed"] / info["n_total"] * 100.0
        print(
            f"  Quality filter: removed {info['n_removed']:,}/{info['n_total']:,} "
            f"beats ({pct:.1f}%) in {info['n_blocks']} block(s)"
        )
    return list(zip(ts_arr[keep].tolist(), rr_arr[keep].tolist()))


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



# Derived per-minute fields, in the row-dict key form produced by
# compute_minute_metrics. Each is written to VM as metric OUT_PREFIX+key
# (e.g. hrv_rmssd_ms) at the minute-start timestamp. None values are not
# written (VM has no NULL; absence = gap). n_beats is always present.
OUT_FIELDS = [
    "n_beats", "hr_bpm", "avg_rr_ms", "min_rr_ms", "max_rr_ms",
    "stddev_rr_ms", "rmssd_ms", "ln_rmssd", "vagal_index", "rmssd_pct",
    "sdnn_ms", "rmssd_sdnn_ratio", "vagal_balance", "pnn50",
    "vlf_ms2", "lf_ms2", "hf_ms2", "ulf_ms2", "ulf1_ms2", "ulf2_ms2",
    "lf_hf_ratio", "b7b8_dom", "b7b8_off", "dfa_alpha1",
    "cpc_lfc_ratio", "hf_peak_stability",
]


def delete_output_series():
    """Wipe all hrv_* output series (used by --full to avoid duplicates)."""
    for field in OUT_FIELDS:
        be_io.delete_series(OUT_PREFIX + field)


def get_max_source_rr_ts():
    """Return the newest RR sample timestamp in VM as ms epoch int, or None."""
    return be_io.latest_timestamp_ms(RR_METRIC)


def get_max_stored_minute():
    """Return MAX stored minute (ms epoch int) from VM, or None if empty."""
    return be_io.latest_timestamp_ms(PRESENCE_METRIC)


def get_existing_minutes(since_ms=None):
    """Return set of minute starts (ms epoch, int) already stored in VM.

    Presence is read from PRESENCE_METRIC (hrv_n_beats), written for every
    stored minute. since_ms restricts the export to the overlap window so
    incremental runs need not read the full history.
    """
    timestamps, _values = be_io.export(PRESENCE_METRIC, start_ms=since_ms)
    return {int(t) for t in timestamps}


def write_results_vm(writer, rows):
    """Emit each row's non-None fields as VM samples at the minute timestamp.

    Returns the number of rows written. None fields are skipped (absence =
    gap in VM). The caller is responsible for never re-writing a minute that
    already exists, since VM does not deduplicate identical timestamps.
    """
    for r in rows:
        ts_ms = r["timestamp_ms"]
        for field in OUT_FIELDS:
            value = r.get(field)
            if value is None:
                continue
            writer.add(OUT_PREFIX + field, ts_ms, float(value))
    return len(rows)


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
             "cutoff) and overwrite all minutes (no skip).",
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


def plan_incremental_load(full):
    """Decide the RR-load cutoff and skip-set for this run.

    Returns (min_ts_ms, existing_minutes), where min_ts_ms is the VM load
    cutoff (None = load everything) and existing_minutes is the set of minute
    starts already stored within the overlap window. Returns None when the
    source RR series holds no minutes newer than what is already stored
    (caller should treat None as "nothing to do").
    """
    t0 = time.monotonic()
    max_stored_ms = get_max_stored_minute()

    min_ts_ms = None
    if full or max_stored_ms is None:
        existing_minutes = set()
    else:
        max_source_ms = get_max_source_rr_ts()
        if max_source_ms is not None and (max_source_ms // 60000) * 60000 <= max_stored_ms:
            print(
                f"Max stored HRV minute: "
                f"{datetime.fromtimestamp(max_stored_ms / 1000.0, tz=timezone.utc).isoformat()} | "
                f"source up to date, nothing to do [{time.monotonic() - t0:.2f}s]"
            )
            return None
        min_ts_ms = max_stored_ms - ULF_WINDOW_MS
        existing_minutes = get_existing_minutes(since_ms=min_ts_ms)

    max_stored_str = (
        datetime.fromtimestamp(max_stored_ms / 1000.0, tz=timezone.utc).isoformat()
        if max_stored_ms is not None else "none"
    )
    print(
        f"Max stored HRV minute: {max_stored_str} | "
        f"overlap window skip-set: {len(existing_minutes)} minutes [{time.monotonic() - t0:.2f}s]"
    )
    return min_ts_ms, existing_minutes


def load_rr_window(min_ts_ms):
    """Load RR intervals (incremental cutoff applied) and report the range.

    Returns the rr_data list of (ts_ms, rr_ms) tuples; empty if there is
    nothing new to process.
    """
    t0 = time.monotonic()
    rr_data = load_rr_data(min_ts_ms=min_ts_ms)
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


def process_batches(writer, bins: MinuteBins, existing_minutes):
    """Run the batched compute -> finalize -> write pipeline.

    HF_PEAK_STABILITY needs forward context, so each batch's tail
    (STABILITY_OVERLAP minutes) is deferred and written only once the next
    batch has extended peak_context. The very last tail of the run has no
    forward context and is therefore *held back* (not written): VM does not
    deduplicate identical (series, timestamp) samples, so these minutes must
    not be written now and re-written later. The next incremental run
    reloads the surrounding RR and computes them with full context.

    Returns a stats dict for print_summary.
    """
    total_minutes = bins.total_minutes
    all_ts, all_rr = bins.all_ts, bins.all_rr
    batch_size = max(1, total_minutes // 20)

    acc_perf = {"t_basic": 0.0, "t_spectral": 0.0, "t_ulf": 0.0,
                "t_dfa": 0.0, "t_cpc": 0.0, "t_loop": 0.0}
    n_skipped_total = 0
    total_rows = 0
    n_held_back = 0
    # (timestamp_ms, hf_peak_freq) tuples — grows across all batches.
    peak_context = []
    # Unfinalized rows from the previous batch (written only after the next
    # batch extends peak_context with future values)
    prev_tail = []
    t_outer_start = time.monotonic()

    print(f"  Progress: 0/{total_minutes} (0%) | elapsed 0.0s")

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

        # Finalize and write the previous batch's deferred tail now that
        # current batch rows are in peak_context
        if prev_tail:
            _finalize_hf_peak_stability(prev_tail, peak_context, CPC_HALF_WIN_STABILITY_MS)
            total_rows += write_results_vm(writer, prev_tail)

        # Split current batch: finalize core now, defer tail to next iteration
        tail_size = min(STABILITY_OVERLAP, len(rows))
        core_rows = rows[:len(rows) - tail_size]
        prev_tail = rows[len(rows) - tail_size:]

        if core_rows:
            _finalize_hf_peak_stability(core_rows, peak_context, CPC_HALF_WIN_STABILITY_MS)
            total_rows += write_results_vm(writer, core_rows)

        n_skipped_total += perf["n_skipped"]
        for k in acc_perf:
            acc_perf[k] += perf[k]

        elapsed = time.monotonic() - t_outer_start
        pct = batch_end / total_minutes * 100
        print(
            f"  Progress: {batch_end}/{total_minutes} ({pct:.0f}%) | "
            f"elapsed {elapsed:.1f}s"
        )

    # The last tail has no forward context — hold it back so it is not
    # written with an incomplete HF_PEAK_STABILITY (and never rewritten).
    if prev_tail:
        n_held_back = len(prev_tail)
        print(
            f"  Held back {n_held_back} boundary minute(s) awaiting forward "
            f"context (recomputed next run)"
        )

    writer.flush()

    return {
        "acc_perf":        acc_perf,
        "n_skipped_total": n_skipped_total,
        "total_rows":      total_rows,
        "n_held_back":     n_held_back,
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
    if stats["n_skipped_total"]:
        print(f"  Skipped (already in target): {stats['n_skipped_total']}")
    if stats["n_held_back"]:
        print(f"  Held back (awaiting context): {stats['n_held_back']}")
    print(
        f"Wrote {stats['total_rows']} minute(s) to the local Hive "
        f"({OUT_PREFIX}* series) [{time.monotonic() - stats['t_outer_start']:.2f}s]"
    )


def main():
    args = parse_args()

    if args.full:
        print("Full recompute: deleting existing hrv_* output series in the Hive...")
        delete_output_series()

    plan = plan_incremental_load(args.full)
    if plan is None:
        return
    min_ts_ms, existing_minutes = plan

    rr_data = load_rr_window(min_ts_ms)
    if not rr_data:
        return

    bins = build_minute_bins(
        rr_data, n_existing=len(existing_minutes), limit_minutes=args.limit_minutes
    )

    writer = be_io.VMWriter()
    stats = process_batches(writer, bins, existing_minutes)
    print_summary(stats)

    be_io.force_flush()


if __name__ == "__main__":
    main()