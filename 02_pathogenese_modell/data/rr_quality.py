#!/usr/bin/env python3
"""Shared RR-interval quality filtering for the HRV aggregators.

Two complementary layers, used identically by ``hrv_aggregate.py`` and
``spectral_bands_aggregate.py`` so detection and validation stay in sync:

Layer 1 — point-ectopic correction (``correct_artifacts``)
    Local-median detector (±ARTIFACT_THRESHOLD_MS over a 9-beat window),
    flagged beats linearly interpolated, window rejected above
    MAX_ARTIFACT_FRACTION (ESC/NASPE 1996 Task Force 5 %). Corrects
    *isolated* extra/missed beats. By design it CANNOT handle gross
    blocks: once more than ~50 % of beats in a neighborhood are corrupt
    the local median is itself corrupt, so nothing is flagged. That is
    what Layer 2 is for.

Layer 2 — block exclusion (``quality_mask`` / ``apply_quality_filter``)
    Detects sustained signal corruption (chest-strap slip: only every
    3rd–4th beat measured correctly, the rest collapsing toward the RR
    floor or spiking high). Such a stretch shows a massively elevated
    rolling rate of physiologically implausible beats + large beat-to-beat
    jumps. The detector marks those beats and, after hysteresis
    (drop short blips → leave to Layer 1; close short recoveries; pad
    edges where the corruption ramps), removes the whole block. Removed
    beats simply become time gaps, which every downstream metric already
    tolerates (Lomb-Scargle natively; Welch via cumulative-time splice;
    per-minute basics via the MIN_BEATS threshold).

All thresholds below are calibration points. The block-detector defaults
are anchored to this recording's physiology (HR envelope ~47–160 bpm) and
the observed slip signature; adjust the BLOCK_* constants if real data
shows them firing too eagerly or missing corruption.
"""

import math

import numpy as np
from scipy.ndimage import median_filter

# --- Layer 1: point-ectopic correction (local median) ----------------
ARTIFACT_MEDIAN_HALFWIDTH = 4   # 9-beat window (i-4 .. i+4)
ARTIFACT_THRESHOLD_MS = 500     # |RR - local_median| > this -> artifact
MAX_ARTIFACT_FRACTION = 0.05    # reject window above this (Task Force 5 %)

# --- Layer 2: block exclusion (strap-slip / gross corruption) ---------
# Physiological plausibility band, from this recording's HR envelope:
#   HR 160 bpm -> RR 375 ms ; HR  47 bpm -> RR 1277 ms (both rare extremes).
# A small margin is added so genuine boundary beats are not counted as
# suspicious; isolated near-boundary beats never trigger exclusion on
# their own — only a sustained CLUSTER (rolling fraction) does.
BLOCK_RR_LO_MS = 370            # < this (>162 bpm) is implausible
BLOCK_RR_HI_MS = 1300           # > this (<46 bpm) is implausible
# A beat-to-beat |ΔRR| above this is non-physiological for nocturnal RR
# (RMSSD is typically tens of ms; the slip signature jumps ~600–1000 ms).
BLOCK_DIFF_THRESHOLD_MS = 300
# Rolling window over which the suspicious-beat fraction is evaluated.
BLOCK_WIN_S = 30
# Fraction of suspicious beats in the window that flags it as corrupt.
# The slip signature leaves only every 3rd–4th beat correct (~60–75 %
# suspicious), so 0.40 triggers reliably while staying well above the
# sparse-ectopic background.
BLOCK_BAD_FRACTION = 0.40
# Hysteresis (all in seconds of wall-clock):
BLOCK_MIN_DURATION_S = 60       # ignore bad runs shorter than this (Layer 1's job)
BLOCK_MIN_GOOD_S = 60           # close good "recovery" islands shorter than this
BLOCK_MARGIN_S = 30             # pad each excluded block on both sides

# Beat-to-beat diffs straddling a gap larger than this are not real
# successive intervals and are excluded from the jump test.
GAP_THRESHOLD_MS = 5000

# --- Time-domain (RMSSD/pNN50/SDNN) per-minute quality gate ------------
# RMSSD/pNN50/SDNN are pathologically sensitive to residual corruption
# that survives Layer 2 (a degraded "tail" below the block-fraction, or
# drops of ~400-480 ms that the ±500 ms median rule never flags). They are
# therefore computed on normal-to-normal intervals: beats marked suspicious
# (implausible RR or a non-physiological >300 ms beat-to-beat jump) and the
# successive-difference pairs touching them are excluded. If a minute is too
# corrupt to trust even on its surviving beats, the metrics are NULLed.
#
# A >300 ms jump rule would be too aggressive for the SPECTRAL path (it
# could clip genuine REM RSA, which is why that path keeps median-only
# correction), but for TIME-DOMAIN NN intervals excluding ectopic-adjacent
# differences is the textbook method (ESC/NASPE 1996) and 300 ms is well
# above any physiological beat-to-beat step.
TIME_DOMAIN_MAX_SUSPECT_FRACTION = 0.15  # minute NULLed above this
TIME_DOMAIN_MIN_VALID_PAIRS = 10         # need at least this many NN pairs


def correct_artifacts(rr):
    """Layer-1 local-median artifact correction with linear interpolation.

    Returns a float copy of ``rr`` with flagged beats interpolated, or
    ``None`` if the artifact fraction exceeds MAX_ARTIFACT_FRACTION or the
    series is too short / degenerate to correct.
    """
    rr = np.asarray(rr, dtype=float)
    n = rr.size
    if n < 2:
        return None
    rr = rr.copy()

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


def suspicious_mask(ts_ms, rr_ms, gap_threshold_ms=GAP_THRESHOLD_MS):
    """Per-beat suspicion flag, shared by the block detector and the
    time-domain quality gate so both use identical criteria.

    A beat is suspicious if its RR is physiologically implausible
    (outside [BLOCK_RR_LO_MS, BLOCK_RR_HI_MS]) or if it is one end of a
    non-physiological beat-to-beat jump (|ΔRR| > BLOCK_DIFF_THRESHOLD_MS
    within a contiguous stretch, i.e. not across a gap).
    """
    ts = np.asarray(ts_ms, dtype=np.int64)
    rr = np.asarray(rr_ms, dtype=np.float64)
    susp = (rr < BLOCK_RR_LO_MS) | (rr > BLOCK_RR_HI_MS)
    if rr.size >= 2:
        dt = np.diff(ts)
        drr = np.abs(np.diff(rr))
        big_jump = (drr > BLOCK_DIFF_THRESHOLD_MS) & (dt <= gap_threshold_ms)
        susp[:-1] |= big_jump
        susp[1:] |= big_jump
    return susp


def nn_time_domain(ts_ms, rr_ms, gap_threshold_ms=GAP_THRESHOLD_MS):
    """Time-domain HRV metrics on normal-to-normal intervals.

    Returns ``(rmssd, sdnn, pnn50)`` in ms / ms / %, or ``(None, None,
    None)`` when the segment is too corrupt to yield a trustworthy value
    (suspicious fraction > TIME_DOMAIN_MAX_SUSPECT_FRACTION, or fewer than
    TIME_DOMAIN_MIN_VALID_PAIRS surviving NN pairs). Suspicious beats and
    the successive-difference pairs touching them (or straddling a gap) are
    excluded; SDNN is the SD of the surviving (normal) beats.
    """
    ts = np.asarray(ts_ms, dtype=np.int64)
    rr = np.asarray(rr_ms, dtype=np.float64)
    n = rr.size
    if n < 3:
        return None, None, None

    susp = suspicious_mask(ts, rr, gap_threshold_ms)
    if susp.mean() > TIME_DOMAIN_MAX_SUSPECT_FRACTION:
        return None, None, None

    normal = rr[~susp]
    if normal.size < 3:
        return None, None, None
    sdnn = float(normal.std(ddof=0))

    d = np.diff(rr)
    pair_bad = susp[:-1] | susp[1:] | (np.diff(ts) > gap_threshold_ms)
    dv = d[~pair_bad]
    if dv.size < TIME_DOMAIN_MIN_VALID_PAIRS:
        return None, None, None
    rmssd = float(math.sqrt(np.mean(dv ** 2)))
    pnn50 = float(np.sum(np.abs(dv) > 50) / dv.size * 100.0)
    return rmssd, sdnn, pnn50


def _bool_runs(mask):
    """Return [(start, end_exclusive), ...] for each True run in mask."""
    if mask.size == 0:
        return []
    m = mask.astype(np.int8)
    edges = np.diff(np.concatenate(([0], m, [0])))
    starts = np.flatnonzero(edges == 1)
    ends = np.flatnonzero(edges == -1)
    return list(zip(starts.tolist(), ends.tolist()))


def quality_mask(ts_ms, rr_ms,
                 gap_threshold_ms=GAP_THRESHOLD_MS):
    """Layer-2 block detector.

    Returns ``(keep_mask, info)`` where ``keep_mask`` is a boolean array
    (True = beat survives) over the input beats, and ``info`` is a dict
    with ``n_total``, ``n_removed`` and ``n_blocks`` for logging.

    ``ts_ms`` must be sorted ascending (as loaded). The detector is local
    (rolling ±BLOCK_WIN_S/2 plus a few minutes of hysteresis margin), so it
    is safe to run on the tail-only arrays of an incremental run.
    """
    ts = np.asarray(ts_ms, dtype=np.int64)
    rr = np.asarray(rr_ms, dtype=np.float64)
    n = ts.size
    info = {"n_total": n, "n_removed": 0, "n_blocks": 0}
    if n < 5:
        return np.ones(n, dtype=bool), info

    # --- per-beat suspicion (shared criteria) ------------------------
    susp = suspicious_mask(ts, rr, gap_threshold_ms)

    # --- rolling suspicious fraction over a ±BLOCK_WIN_S/2 time window -
    half_w = BLOCK_WIN_S * 1000 // 2
    csum = np.concatenate(([0], np.cumsum(susp.astype(np.int64))))
    lo = np.searchsorted(ts, ts - half_w, side="left")
    hi = np.searchsorted(ts, ts + half_w, side="right")
    cnt = np.maximum(hi - lo, 1)
    frac = (csum[hi] - csum[lo]) / cnt
    bad = frac > BLOCK_BAD_FRACTION

    # --- hysteresis ---------------------------------------------------
    # 1) open: drop bad runs shorter than BLOCK_MIN_DURATION_S (point
    #    ectopics / brief blips are Layer 1's responsibility).
    min_dur_ms = BLOCK_MIN_DURATION_S * 1000
    for s, e in _bool_runs(bad):
        if ts[e - 1] - ts[s] < min_dur_ms:
            bad[s:e] = False

    # 2) close: fill internal good islands shorter than BLOCK_MIN_GOOD_S
    #    (brief apparent recovery inside a slip episode).
    min_good_ms = BLOCK_MIN_GOOD_S * 1000
    for s, e in _bool_runs(~bad):
        if s > 0 and e < n and (ts[e - 1] - ts[s] < min_good_ms):
            bad[s:e] = True

    # 3) margin: extend each block by BLOCK_MARGIN_S on both sides, where
    #    the corruption typically ramps in/out.
    margin_ms = BLOCK_MARGIN_S * 1000
    bad_final = bad.copy()
    blocks = _bool_runs(bad)
    for s, e in blocks:
        a = int(np.searchsorted(ts, ts[s] - margin_ms, side="left"))
        b = int(np.searchsorted(ts, ts[e - 1] + margin_ms, side="right"))
        bad_final[a:b] = True

    keep = ~bad_final
    info["n_removed"] = int(bad_final.sum())
    info["n_blocks"] = len(_bool_runs(bad_final))
    return keep, info


def apply_quality_filter(ts_ms, rr_ms, gap_threshold_ms=GAP_THRESHOLD_MS):
    """Convenience wrapper: return ``(ts_kept, rr_kept, info)``."""
    ts = np.asarray(ts_ms, dtype=np.int64)
    rr = np.asarray(rr_ms, dtype=np.float64)
    keep, info = quality_mask(ts, rr, gap_threshold_ms=gap_threshold_ms)
    return ts[keep], rr[keep], info
