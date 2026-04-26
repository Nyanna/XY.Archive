#!/usr/bin/env python3
"""
Individual HRV Frequency Map — One-Shot Spectral Fingerprint (Multi-Tier)
========================================================================

Computes a Lomb-Scargle spectral fingerprint of the entire RR-interval
record (Coospo H9Z, table HEART_RR_INTERVAL_SAMPLE) across THREE
frequency tiers, each with the window length matched to the band of
interest. The three tiers are stitched into a single combined log-log
spectrum so that physiological rhythms from milliseconds to days can
all be inspected on the same plot.

Tiers
-----
    hf_lf       30-min windows, 50 % overlap   0.005  – 0.5    Hz
                  → respiration (RSA), Mayer wave, baroreflex
    vlf_ulf     4-h   windows, 50 % overlap   0.00005 – 0.01   Hz
                  → ULF, hormonal/serotonergic cycles 7-24 min,
                    sub-circadian rhythms
    circadian   single Lomb-Scargle over full record (no windowing)
                  5e-7   – 1e-4   Hz
                  → circadian (24 h), multi-day trends

Method (per tier)
-----------------
- Local-median artifact rejection (±500 ms threshold, 5 % budget,
  ESC/NASPE 1996)
- Linear detrend per window (suppresses baseline drift → spurious LF)
- Lomb-Scargle PSD on the irregular beat times (astropy 'fast' / NUFT)
- Welch-style averaging across windows (single shot for circadian tier)

Peak detection (combined spectrum)
----------------------------------
HRV spectra follow a 1/f^α power law. The combined log10(PSD) is
whitened by subtracting a rolling-median baseline; peak prominence
is then measured in dex on the residual.

Outputs
-------
    data/spectral_fingerprint.csv         (freq_hz, period_s, power_ms2hz, tier)
    data/spectral_fingerprint_peaks.csv   (peaks sorted by prominence)
    data/spectral_fingerprint.png         (3-panel + combined view)
"""

import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np
import psycopg2
from astropy.timeseries import LombScargle
from scipy.ndimage import median_filter
from scipy.signal import find_peaks

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Postgres -------------------------------------------------------
PG_HOST = os.environ["PGHOST"]
PG_PORT = int(os.environ.get("PGPORT", "5432"))
PG_DB = os.environ["PGDATABASE"]
PG_USER = os.environ.get("PGUSER", "gadgetbridge")
PG_PASSWORD = os.environ["PGPASSWORD"]
DEVICE_ID = 2  # H9Z 40647

# --- IBI sanity (matches hrv_aggregate.py) --------------------------
MIN_RR = 300
MAX_RR = 2000

# --- Local-median artifact correction -------------------------------
ARTIFACT_MEDIAN_HALFWIDTH = 4
ARTIFACT_THRESHOLD_MS = 500
MAX_ARTIFACT_FRACTION = 0.05

# --- Tiers ----------------------------------------------------------
# Each tier specifies its own window length, gap tolerance, and
# frequency grid so that resolution is matched to the band. Tiers are
# stitched into one combined spectrum at the chosen split frequencies.
TIERS = [
    {
        "name": "hf_lf",
        "window_s": 30 * 60,
        "overlap": 0.5,
        "gap_ms": 5_000,            # strict — penalize bad windows
        "freq_min": 0.005,
        "freq_max": 0.5,
        "n_freq": 800,
        "min_beats": 200,
    },
    {
        "name": "vlf_ulf",
        "window_s": 4 * 3600,
        "overlap": 0.5,
        "gap_ms": 60_000,           # tolerate brief disconnects
        "freq_min": 5e-5,
        "freq_max": 0.01,
        "n_freq": 800,
        "min_beats": 5_000,
    },
    {
        "name": "circadian",
        "window_s": None,           # single LS over the full record
        "overlap": None,
        "gap_ms": 600_000,          # 10 min — only split on long off-times
        "freq_min": 5e-7,
        "freq_max": 1e-4,
        "n_freq": 800,
        "min_beats": 50_000,
    },
]

# Frequencies at which adjacent tiers are spliced (use the lower-tier
# value below the splice, the higher-tier value above).
TIER_SPLITS = {
    ("circadian", "vlf_ulf"): 1e-4,
    ("vlf_ulf",   "hf_lf"):   0.005,
}

# --- Peak detection on combined whitened spectrum -------------------
BASELINE_WINDOW_BINS = 81
LOG_PROMINENCE_DEX   = 0.08
MIN_PEAK_WIDTH_BINS  = 3
MIN_PEAK_DISTANCE_DEX_OF_FREQ = 0.05    # ~12 % freq separation in log space

# --- Progress -------------------------------------------------------
PROGRESS_EVERY = 25
HISTOGRAM_WIDTH = 70
HISTOGRAM_HEIGHT = 14

OUT_DIR = Path(__file__).parent
OUT_SPECTRUM_CSV = OUT_DIR / "spectral_fingerprint.csv"
OUT_PEAKS_CSV    = OUT_DIR / "spectral_fingerprint_peaks.csv"
OUT_PLOT         = OUT_DIR / "spectral_fingerprint.png"


# -------------------------------------------------------------------
# Data loading
# -------------------------------------------------------------------
def load_rr_data():
    print(f"Connecting to {PG_USER}@{PG_HOST}:{PG_PORT}/{PG_DB} ...")
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, user=PG_USER,
        password=PG_PASSWORD, dbname=PG_DB, sslmode="require",
    )
    try:
        cur = conn.cursor()
        cur.execute(
            'SELECT "TIMESTAMP", "RR_MILLIS" '
            'FROM "HEART_RR_INTERVAL_SAMPLE" '
            'WHERE "DEVICE_ID" = %s '
            '  AND "RR_MILLIS" BETWEEN %s AND %s '
            'ORDER BY "TIMESTAMP", "SEQ"',
            (DEVICE_ID, MIN_RR, MAX_RR),
        )
        rows = cur.fetchall()
    finally:
        conn.close()
    if not rows:
        print("ERROR: no RR data found.")
        sys.exit(1)
    ts = np.fromiter((r[0] for r in rows), dtype=np.int64, count=len(rows))
    rr = np.fromiter((r[1] for r in rows), dtype=np.float64, count=len(rows))
    return ts, rr


def split_into_chunks(ts, gap_ms):
    if ts.size == 0:
        return []
    boundaries = np.flatnonzero(np.diff(ts) > gap_ms) + 1
    starts = np.concatenate(([0], boundaries))
    ends = np.concatenate((boundaries, [ts.size]))
    return list(zip(starts.tolist(), ends.tolist()))


# -------------------------------------------------------------------
# Artifact correction
# -------------------------------------------------------------------
def correct_artifacts(rr):
    n = len(rr)
    if n < 2:
        return None
    rr = rr.astype(float, copy=True)
    win = 2 * ARTIFACT_MEDIAN_HALFWIDTH + 1
    local_median = median_filter(rr, size=win, mode="nearest")
    artifact_mask = np.abs(rr - local_median) > ARTIFACT_THRESHOLD_MS
    if artifact_mask.sum() / n > MAX_ARTIFACT_FRACTION:
        return None
    if artifact_mask.any():
        valid_idx = np.flatnonzero(~artifact_mask)
        if valid_idx.size < 2:
            return None
        all_idx = np.arange(n)
        rr[artifact_mask] = np.interp(
            all_idx[artifact_mask], valid_idx, rr[valid_idx]
        )
    return rr


# -------------------------------------------------------------------
# Window iteration
# -------------------------------------------------------------------
def iter_windows(ts, rr, chunks, win_seconds, overlap, min_beats):
    win_ms = int(win_seconds * 1000)
    step_ms = max(1, int(win_ms * (1 - overlap)))
    for s, e in chunks:
        if e - s < min_beats:
            continue
        ts_chunk = ts[s:e]
        t0 = int(ts_chunk[0])
        t_end = int(ts_chunk[-1])
        if t_end - t0 < win_ms:
            continue
        anchor = t0
        while anchor + win_ms <= t_end:
            i_lo = int(np.searchsorted(ts_chunk, anchor,          side="left"))
            i_hi = int(np.searchsorted(ts_chunk, anchor + win_ms, side="left"))
            if i_hi - i_lo >= min_beats:
                rr_win = rr[s + i_lo : s + i_hi]
                t_win = (ts_chunk[i_lo:i_hi].astype(np.float64)
                         - anchor) / 1000.0
                yield rr_win, t_win
            anchor += step_ms


def lombscargle_psd(t_sec, rr_corr, freqs):
    """Detrended Lomb-Scargle PSD in ms²/Hz."""
    slope, intercept = np.polyfit(t_sec, rr_corr, 1)
    rr_det = rr_corr - (slope * t_sec + intercept)
    pgram = LombScargle(t_sec, rr_det, normalization="psd").power(
        freqs, method="fast",
    )
    # Match hrv_aggregate.compute_ulf_power: factor 2 -> ms²/Hz so
    # ∫PSD df ≈ var(rr).
    return pgram * 2.0


# -------------------------------------------------------------------
# Tier analysis
# -------------------------------------------------------------------
def analyze_tier(ts, rr, tier, progress_every):
    name      = tier["name"]
    freq_min  = tier["freq_min"]
    freq_max  = tier["freq_max"]
    n_freq    = tier["n_freq"]
    min_beats = tier["min_beats"]
    gap_ms    = tier["gap_ms"]

    chunks = split_into_chunks(ts, gap_ms)
    freqs = np.linspace(freq_min, freq_max, n_freq)

    print(f"\n[tier: {name}]  freq {freq_min:g}–{freq_max:g} Hz  "
          f"(period {1/freq_max:.1f}s – {1/freq_min/3600:.2f}h)")
    print(f"  chunks (gap > {gap_ms/1000:.0f}s): {len(chunks)}")

    psd_sum = np.zeros_like(freqs)
    n_windows = 0
    n_rejected = 0
    t_loop = time.monotonic()

    if tier["window_s"] is None:
        # Circadian tier: one LS over the longest contiguous chunk
        # (multi-day windows mixing recording / off / recording would
        # leak chunk boundaries into the spectrum).
        best = max(chunks, key=lambda se: se[1] - se[0])
        s, e = best
        rr_chunk = rr[s:e]
        ts_chunk = ts[s:e]
        if rr_chunk.size < min_beats:
            print(f"  largest chunk only {rr_chunk.size} beats — skipping")
            return freqs, None, 0
        rr_corr = correct_artifacts(rr_chunk)
        if rr_corr is None:
            print(f"  artifact fraction > {MAX_ARTIFACT_FRACTION*100:.0f}% — skipping")
            return freqs, None, 0
        t_sec = (ts_chunk.astype(np.float64) - float(ts_chunk[0])) / 1000.0
        psd_sum = lombscargle_psd(t_sec, rr_corr, freqs)
        n_windows = 1
        span_h = (ts_chunk[-1] - ts_chunk[0]) / 1000.0 / 3600.0
        print(f"  single LS over {rr_chunk.size:,} beats spanning "
              f"{span_h:.1f} h — done in {time.monotonic()-t_loop:.1f}s")
        return freqs, psd_sum, 1

    for rr_win, t_win in iter_windows(
        ts, rr, chunks,
        tier["window_s"], tier["overlap"], min_beats,
    ):
        rr_corr = correct_artifacts(rr_win)
        if rr_corr is None:
            n_rejected += 1
            continue
        try:
            psd = lombscargle_psd(t_win, rr_corr, freqs)
        except Exception:
            n_rejected += 1
            continue
        psd_sum += psd
        n_windows += 1

        if progress_every and n_windows % progress_every == 0:
            mean_psd = psd_sum / n_windows
            elapsed = time.monotonic() - t_loop
            print(
                f"\n  [{n_windows} windows | {n_rejected} rejected | "
                f"{elapsed:.1f}s]  running mean spectrum:"
            )
            print(render_ascii_histogram(freqs, mean_psd))

    if n_windows == 0:
        print(f"  WARNING: no windows accepted in tier {name}")
        return freqs, None, 0

    print(f"  done: {n_windows} windows accepted, {n_rejected} rejected, "
          f"{time.monotonic()-t_loop:.1f}s")
    return freqs, psd_sum / n_windows, n_windows


# -------------------------------------------------------------------
# ASCII histogram
# -------------------------------------------------------------------
def render_ascii_histogram(freqs, psd, width=HISTOGRAM_WIDTH,
                           height=HISTOGRAM_HEIGHT):
    pos = psd > 0
    if not np.any(pos):
        return "  (all-zero spectrum)"
    log_f = np.log10(freqs[pos])
    log_p = np.log10(psd[pos])
    f_min, f_max = float(log_f.min()), float(log_f.max())
    p_min, p_max = float(log_p.min()), float(log_p.max())
    if f_max == f_min or p_max == p_min:
        return "  (degenerate range)"
    bin_idx = np.clip(
        ((log_f - f_min) / (f_max - f_min) * (width - 1)).astype(int),
        0, width - 1,
    )
    bin_max = np.full(width, -np.inf)
    np.maximum.at(bin_max, bin_idx, log_p)
    bin_max = np.where(np.isfinite(bin_max), bin_max, p_min)
    norm = (bin_max - p_min) / (p_max - p_min)
    rows = []
    for h in range(height, 0, -1):
        thresh = (h - 0.5) / height
        line = "".join("█" if v >= thresh else " " for v in norm)
        rows.append(f"  {line}")
    rows.append(
        f"  freq  10^{f_min:+.2f} .. 10^{f_max:+.2f} Hz  "
        f"|  PSD  10^{p_min:+.2f} .. 10^{p_max:+.2f} ms²/Hz"
    )
    return "\n".join(rows)


# -------------------------------------------------------------------
# Tier stitching
# -------------------------------------------------------------------
def stitch_tiers(tier_results):
    """Concatenate per-tier (freqs, psd) into one log-spaced spectrum.

    For overlapping ranges the lower-frequency tier wins below the
    splice frequency and the higher-frequency tier wins above; this
    avoids double-counting where window lengths differ.
    """
    ordered = sorted(
        ((t["name"], t, tier_results[t["name"]]) for t in TIERS),
        key=lambda x: x[1]["freq_min"],
    )
    pieces = []
    for i, (name, tier, (freqs, psd, n)) in enumerate(ordered):
        if psd is None:
            continue
        f_lo = tier["freq_min"]
        f_hi = tier["freq_max"]
        # Trim against splice with neighbors
        if i > 0:
            prev_name = ordered[i - 1][0]
            split = TIER_SPLITS.get((prev_name, name)) \
                or TIER_SPLITS.get((name, prev_name))
            if split is not None:
                f_lo = max(f_lo, split)
        if i + 1 < len(ordered):
            next_name = ordered[i + 1][0]
            split = TIER_SPLITS.get((name, next_name)) \
                or TIER_SPLITS.get((next_name, name))
            if split is not None:
                f_hi = min(f_hi, split)
        mask = (freqs >= f_lo) & (freqs <= f_hi)
        if not mask.any():
            continue
        pieces.append((name, freqs[mask], psd[mask]))
    if not pieces:
        return None, None, None

    all_freqs = np.concatenate([p[1] for p in pieces])
    all_psd   = np.concatenate([p[2] for p in pieces])
    all_tier  = np.concatenate([
        np.full(p[1].size, p[0], dtype=object) for p in pieces
    ])
    order = np.argsort(all_freqs)
    return all_freqs[order], all_psd[order], all_tier[order]


# -------------------------------------------------------------------
# Band labels (extended for ULF / circadian)
# -------------------------------------------------------------------
def band_label(f):
    if f < 1.5e-5:    return "circadian"   # < ~18 h period
    if f < 1e-4:      return "ultraslow"   # 2.8 h - 18 h
    if f < 0.0007:    return "sub-ULF"     # 24 min - 2.8 h
    if f < 0.0033:    return "ULF"         # 5 - 24 min  (incl. serotonin window)
    if f < 0.04:      return "VLF"
    if f < 0.15:      return "LF"
    if f <= 0.40:     return "HF"
    return "supra-HF"


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--progress-every", type=int, default=PROGRESS_EVERY,
                    help=f"Print histogram every N windows (default "
                         f"{PROGRESS_EVERY}); 0 disables")
    ap.add_argument("--log-prominence-dex", type=float,
                    default=LOG_PROMINENCE_DEX,
                    help=f"Peak prominence threshold on whitened "
                         f"log10(PSD) [dex] (default {LOG_PROMINENCE_DEX})")
    ap.add_argument("--skip-tier", action="append", default=[],
                    choices=[t["name"] for t in TIERS],
                    help="Skip a tier (repeatable)")
    args = ap.parse_args()

    t_total = time.monotonic()
    ts, rr = load_rr_data()
    span_h = (ts[-1] - ts[0]) / 1000.0 / 3600.0
    print(f"Loaded {ts.size:,} RR samples spanning {span_h:.1f} h "
          f"(~{span_h/24:.1f} d)")

    tier_results = {}
    for tier in TIERS:
        if tier["name"] in args.skip_tier:
            print(f"\n[tier: {tier['name']}]  skipped")
            tier_results[tier["name"]] = (
                np.linspace(tier["freq_min"], tier["freq_max"],
                            tier["n_freq"]),
                None, 0,
            )
            continue
        tier_results[tier["name"]] = analyze_tier(
            ts, rr, tier, args.progress_every,
        )

    # Stitch tiers into one combined spectrum
    freqs_c, psd_c, tier_c = stitch_tiers(tier_results)
    if freqs_c is None:
        print("ERROR: no tier produced a spectrum.")
        sys.exit(2)

    # Whiten and detect peaks on the COMBINED spectrum
    log_psd = np.log10(np.maximum(psd_c, 1e-30))
    baseline = median_filter(log_psd, size=BASELINE_WINDOW_BINS,
                             mode="nearest")
    whitened = log_psd - baseline

    # Distance constraint in LOG-FREQ space (so the same fractional
    # separation applies across the 6 decades the combined spectrum
    # covers); convert to bin distance via local log-freq spacing.
    log_f = np.log10(freqs_c)
    dlog = np.median(np.diff(log_f))
    distance_bins = max(1, int(round(MIN_PEAK_DISTANCE_DEX_OF_FREQ / dlog)))

    peak_idx, props = find_peaks(
        whitened,
        prominence=args.log_prominence_dex,
        width=MIN_PEAK_WIDTH_BINS,
        distance=distance_bins,
    )

    # Reject peaks too close to a tier-splice frequency: the PSD
    # normalization differs between tiers (window length differs), so
    # the discontinuity at the splice can register as a spurious peak.
    splice_freqs = list(TIER_SPLITS.values())
    splice_log = np.array([np.log10(f) for f in splice_freqs])
    keep = []
    for k in peak_idx:
        d = np.min(np.abs(np.log10(freqs_c[k]) - splice_log))
        if d > MIN_PEAK_DISTANCE_DEX_OF_FREQ:
            keep.append(k)
    keep = np.array(keep, dtype=int) if keep else np.array([], dtype=int)
    keep_mask = np.isin(peak_idx, keep)
    n_dropped = peak_idx.size - keep.size
    peak_idx = peak_idx[keep_mask]
    props = {k: v[keep_mask] for k, v in props.items()}

    print(f"\nDetected {peak_idx.size} peaks on combined whitened spectrum "
          f"(prominence ≥ {args.log_prominence_dex:.3f} dex, "
          f"width ≥ {MIN_PEAK_WIDTH_BINS} bins, "
          f"distance ≥ {distance_bins} bins; "
          f"{n_dropped} dropped near tier splice)")

    # --- CSV: spectrum -------------------------------------------
    with OUT_SPECTRUM_CSV.open("w") as f:
        f.write("freq_hz,period_s,power_ms2hz,tier\n")
        for fr, p, t in zip(freqs_c, psd_c, tier_c):
            f.write(f"{fr:.8e},{1.0/fr:.4e},{p:.6e},{t}\n")
    print(f"Wrote {OUT_SPECTRUM_CSV}  ({freqs_c.size} bins)")

    # --- CSV: peaks ----------------------------------------------
    with OUT_PEAKS_CSV.open("w") as f:
        f.write("rank,freq_hz,period_s,period_human,power_ms2hz,"
                "log_prominence_dex,fwhm_hz,canonical_band,tier\n")
        order = np.argsort(props["prominences"])[::-1]
        for rank, k in enumerate(order, 1):
            i = peak_idx[k]
            fr = freqs_c[i]
            per = 1.0 / fr
            if per >= 86400:    per_h = f"{per/86400:.2f}d"
            elif per >= 3600:   per_h = f"{per/3600:.2f}h"
            elif per >= 60:     per_h = f"{per/60:.2f}min"
            else:               per_h = f"{per:.2f}s"
            f.write(
                f"{rank},{fr:.8e},{per:.4e},{per_h},{psd_c[i]:.6e},"
                f"{props['prominences'][k]:.4f},"
                f"{props['widths'][k] * dlog * fr * np.log(10):.6e},"
                f"{band_label(fr)},{tier_c[i]}\n"
            )
    print(f"Wrote {OUT_PEAKS_CSV}  ({peak_idx.size} peaks)")

    # --- Plot: 4 panels (3 tiers + combined whitened) ------------
    fig, axes = plt.subplots(4, 1, figsize=(13, 12), dpi=150)
    tier_colors = {
        "circadian": "#7B3F99",
        "vlf_ulf":   "#1F77B4",
        "hf_lf":     "#2CA02C",
    }
    for ax, tier in zip(axes[:3], TIERS):
        f_t, psd_t, n_t = tier_results[tier["name"]]
        ax.set_xscale("log")
        ax.set_yscale("log")
        if psd_t is not None:
            ax.plot(f_t, psd_t, color=tier_colors[tier["name"]], lw=1.0)
            for k in peak_idx:
                if tier_c[k] != tier["name"]:
                    continue
                fr = freqs_c[k]
                # Find PSD value in this tier's grid
                j = int(np.argmin(np.abs(f_t - fr)))
                ax.plot(fr, psd_t[j], "rv", ms=6)
                per = 1.0 / fr
                lbl = (f"{per/3600:.1f}h" if per >= 3600 else
                       f"{per/60:.1f}m"  if per >= 60   else
                       f"{per:.1f}s")
                ax.annotate(
                    f"{fr:.2e} Hz\n({lbl})",
                    xy=(fr, psd_t[j]),
                    xytext=(3, 8), textcoords="offset points",
                    fontsize=7, color="darkred",
                )
        win_label = (f"single LS, full record"
                     if tier["window_s"] is None else
                     f"{tier['window_s']//60} min wins, "
                     f"{int(tier['overlap']*100)}% overlap, n={n_t}")
        ax.set_title(f"Tier: {tier['name']}    "
                     f"({tier['freq_min']:g}–{tier['freq_max']:g} Hz, "
                     f"{win_label})", fontsize=10)
        ax.set_xlabel("Frequency [Hz]")
        ax.set_ylabel("PSD [ms²/Hz]")
        ax.grid(True, which="both", ls=":", alpha=0.3)
        ax.set_xlim(tier["freq_min"], tier["freq_max"])

    # Combined whitened panel
    ax = axes[3]
    ax.set_xscale("log")
    for tname in tier_colors:
        m = tier_c == tname
        if m.any():
            ax.plot(freqs_c[m], whitened[m],
                    color=tier_colors[tname], lw=0.8, label=tname)
    ax.axhline(0, color="grey", lw=0.5)
    ax.axhline(args.log_prominence_dex, color="red", ls=":", lw=0.7,
               label=f"prominence {args.log_prominence_dex:.2f} dex")
    for k in peak_idx:
        ax.plot(freqs_c[k], whitened[k], "rv", ms=5)
    ax.set_title("Combined whitened spectrum (log10 PSD − rolling-median "
                 "baseline)", fontsize=10)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("whitened log10(PSD) [dex]")
    ax.grid(True, which="both", ls=":", alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xlim(freqs_c.min(), freqs_c.max())

    # Add reference markers for canonical and circadian/serotonin freqs
    REF_LINES = [
        (1 / 86400,        "24h",         "#7B3F99"),
        (1 / (12 * 3600),  "12h",         "#7B3F99"),
        (1 / (90 * 60),    "90min REM",   "#888888"),
        (1 / (24 * 60),    "24min sero",  "#FF8800"),
        (1 / (7  * 60),    "7min sero",   "#FF8800"),
        (0.0033,           "VLF",         "#444444"),
        (0.04,             "LF",          "#444444"),
        (0.15,             "HF",          "#444444"),
    ]
    for f_ref, lbl, col in REF_LINES:
        for ax_ in axes:
            xl = ax_.get_xlim()
            if xl[0] <= f_ref <= xl[1]:
                ax_.axvline(f_ref, color=col, ls="--", lw=0.4, alpha=0.6)
                ax_.text(f_ref, ax_.get_ylim()[1], lbl,
                         color=col, fontsize=6,
                         ha="center", va="top", rotation=0)

    fig.suptitle(
        f"HRV spectral fingerprint (multi-tier Lomb-Scargle)  "
        f"|  {ts.size:,} beats over {span_h/24:.1f} d",
        fontsize=11, y=0.995,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.99))
    fig.savefig(OUT_PLOT)
    print(f"Wrote {OUT_PLOT}")

    # --- Summary stdout -----------------------------------------
    if peak_idx.size:
        order = np.argsort(props["prominences"])[::-1]
        print("\nTop peaks (sorted by prominence above 1/f baseline):")
        print(f"  {'rank':>4}  {'freq_hz':>11}  {'period':>10}  "
              f"{'log_prom':>9}  {'PSD':>11}  band              tier")
        for rank, k in enumerate(order, 1):
            i = peak_idx[k]
            fr = freqs_c[i]
            per = 1.0 / fr
            if   per >= 86400: per_s = f"{per/86400:6.2f}d "
            elif per >= 3600:  per_s = f"{per/3600:6.2f}h "
            elif per >= 60:    per_s = f"{per/60:6.2f}min"
            else:              per_s = f"{per:6.2f}s "
            print(f"  {rank:>4}  {fr:>11.4e}  {per_s:>10}  "
                  f"{props['prominences'][k]:>9.3f}  "
                  f"{psd_c[i]:>11.3e}  {band_label(fr):<17} {tier_c[i]}")

    print(f"\nTotal runtime: {time.monotonic() - t_total:.1f}s")


if __name__ == "__main__":
    main()
