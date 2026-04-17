#!/usr/bin/env python3
"""HRV minute aggregation from Gadgetbridge RR-interval samples."""

import argparse
import math
import sqlite3
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.signal import lombscargle

DB_PATH = Path(__file__).parent / "Gadgetbridge"

MIN_RR = 300
MAX_RR = 2000
GAP_THRESHOLD_MS = 5000
MIN_BEATS_PER_MINUTE = 15
LF_HF_MIN_BEATS = 150
LF_HF_WINDOW_MS = 5 * 60 * 1000
DFA_WINDOW = 200
DFA_BOXES_ALL = [4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64]
DFA_BOXES_ALPHA1 = {4, 6, 8, 10, 12, 16}


def load_rr_data(db_path, device_id=None):
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

    cur.execute(
        "SELECT TIMESTAMP, RR_MILLIS FROM HEART_RR_INTERVAL_SAMPLE "
        "WHERE DEVICE_ID = ? ORDER BY TIMESTAMP, SEQ",
        (device_id,),
    )
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


def compute_lf_hf(timestamps_ms, rr_values):
    if len(rr_values) < LF_HF_MIN_BEATS:
        return None, None, None
    rr = np.asarray(rr_values, dtype=float)
    t_sec = np.cumsum(rr) / 1000.0
    y = rr - rr.mean()

    if t_sec[-1] - t_sec[0] <= 0:
        return None, None, None

    freqs = np.linspace(0.001, 0.5, 1000)
    angular = 2 * np.pi * freqs
    try:
        pgram = lombscargle(t_sec, y, angular, normalize=False)
    except Exception:
        return None, None, None

    # scipy lombscargle returns (A^2 * N / 4); for power density in ms^2/Hz
    # we use a common normalization: 2 * P / N
    power = 2.0 * pgram / len(y)

    lf_mask = (freqs >= 0.04) & (freqs <= 0.15)
    hf_mask = (freqs >= 0.15) & (freqs <= 0.40)

    trap = getattr(np, "trapezoid", np.trapz)
    lf = float(trap(power[lf_mask], freqs[lf_mask])) if lf_mask.any() else None
    hf = float(trap(power[hf_mask], freqs[hf_mask])) if hf_mask.any() else None
    ratio = lf / hf if (lf is not None and hf is not None and hf > 0) else None
    return lf, hf, ratio


def compute_minute_metrics(rr_data, enable_lf_hf=False, enable_dfa=False):
    if not rr_data:
        return []

    t0 = time.monotonic()

    # Sukzessive Differenzen (mit Gap-Filter)
    diffs_for_ts = {}  # timestamp -> diff (diff belongs to beat at index i)
    for i in range(1, len(rr_data)):
        ts_prev, rr_prev = rr_data[i - 1]
        ts_curr, rr_curr = rr_data[i]
        if (ts_curr - ts_prev) <= GAP_THRESHOLD_MS:
            diffs_for_ts[i] = rr_curr - rr_prev

    print(f"  Successive diffs computed: {time.monotonic() - t0:.2f}s")

    # Minute binning
    minute_indices = defaultdict(list)
    for idx, (ts, _rr) in enumerate(rr_data):
        minute_start = (ts // 60000) * 60000
        minute_indices[minute_start].append(idx)

    sorted_minutes = sorted(minute_indices.keys())
    all_ts = np.array([r[0] for r in rr_data])
    all_rr = np.array([r[1] for r in rr_data])

    print(f"  Minute binning done ({len(sorted_minutes)} bins): {time.monotonic() - t0:.2f}s")

    results = []
    total_minutes = len(sorted_minutes)
    time_basic = 0.0
    time_lfhf = 0.0
    time_dfa = 0.0
    t_loop_start = time.monotonic()
    log_interval = max(1, total_minutes // 20)  # ~20 progress updates

    for mi, minute_start in enumerate(sorted_minutes):
        idxs = minute_indices[minute_start]
        if len(idxs) < MIN_BEATS_PER_MINUTE:
            continue

        t_step = time.monotonic()
        rr = all_rr[idxs].astype(float)
        n_beats = len(rr)
        mean_rr = float(rr.mean())
        hr_bpm = 60000.0 / mean_rr if mean_rr > 0 else None
        min_rr = int(rr.min())
        max_rr = int(rr.max())
        std_rr = float(rr.std(ddof=0))  # population stddev

        minute_diffs = [diffs_for_ts[i] for i in idxs if i in diffs_for_ts]
        if minute_diffs:
            d = np.asarray(minute_diffs, dtype=float)
            rmssd = float(math.sqrt(np.mean(d ** 2)))
            pnn50 = float(np.sum(np.abs(d) > 50) / len(d) * 100.0)
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

        time_basic += time.monotonic() - t_step

        # LF/HF: 5-min window centered on minute (optional)
        lf, hf, lfhf = None, None, None
        if enable_lf_hf:
            t_lfhf = time.monotonic()
            window_start = minute_start - 2 * 60 * 1000
            window_end = minute_start + 3 * 60 * 1000  # inclusive of minute M itself (M + 2min)
            mask = (all_ts >= window_start) & (all_ts < window_end)
            win_count = int(mask.sum())
            if win_count < LF_HF_MIN_BEATS:
                # asymmetric fallback near edges: take nearest 5min worth
                center_idx = np.searchsorted(all_ts, minute_start)
                half = LF_HF_MIN_BEATS  # expand search
                lo = max(0, center_idx - half * 2)
                hi = min(len(all_ts), center_idx + half * 2)
                # fall back: use as-is if still too few
                if hi - lo >= LF_HF_MIN_BEATS:
                    win_ts = all_ts[lo:hi]
                    win_rr = all_rr[lo:hi]
                    # restrict to 5 minutes around minute_start
                    span_mask = (win_ts >= minute_start - LF_HF_WINDOW_MS) & (
                        win_ts <= minute_start + LF_HF_WINDOW_MS
                    )
                    win_ts = win_ts[span_mask]
                    win_rr = win_rr[span_mask]
                    if len(win_rr) >= LF_HF_MIN_BEATS:
                        lf, hf, lfhf = compute_lf_hf(win_ts, win_rr)
            else:
                lf, hf, lfhf = compute_lf_hf(all_ts[mask], all_rr[mask])

            time_lfhf += time.monotonic() - t_lfhf

        # DFA: letzte 200 RR VOR dem Ende der Minute (optional)
        dfa_alpha1 = None
        if enable_dfa:
            t_dfa = time.monotonic()
            minute_end = minute_start + 60000
            end_idx = np.searchsorted(all_ts, minute_end, side="left")
            start_idx = max(0, end_idx - DFA_WINDOW)
            dfa_values = all_rr[start_idx:end_idx]
            dfa_alpha1 = compute_dfa_alpha1(list(dfa_values))

            time_dfa += time.monotonic() - t_dfa

        if (mi + 1) % log_interval == 0 or mi == total_minutes - 1:
            elapsed = time.monotonic() - t_loop_start
            pct = (mi + 1) / total_minutes * 100
            print(
                f"  Progress: {mi + 1}/{total_minutes} ({pct:.0f}%) | "
                f"elapsed {elapsed:.1f}s | "
                f"basic {time_basic:.1f}s  lf/hf {time_lfhf:.1f}s  dfa {time_dfa:.1f}s"
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
            "pnn50": pnn50,
            "lf_ms2": lf,
            "hf_ms2": hf,
            "lf_hf_ratio": lfhf,
            "dfa_alpha1": dfa_alpha1,
        })

    elapsed_total = time.monotonic() - t0
    print(f"  --- Timing summary ---")
    print(f"  Prep (diffs + binning):  included above")
    print(f"  Basic metrics total:     {time_basic:.2f}s")
    if enable_lf_hf:
        print(f"  LF/HF (Lomb-Scargle):   {time_lfhf:.2f}s")
    else:
        print(f"  LF/HF (Lomb-Scargle):   disabled")
    if enable_dfa:
        print(f"  DFA alpha1:              {time_dfa:.2f}s")
    else:
        print(f"  DFA alpha1:              disabled")
    print(f"  Loop total:              {time.monotonic() - t_loop_start:.2f}s")
    print(f"  compute_minute_metrics:  {elapsed_total:.2f}s")

    return results


def write_results(db_path, rows):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS HRV_MINUTE_AGGREGATED")
    cur.execute("""
        CREATE TABLE HRV_MINUTE_AGGREGATED (
            TIMESTAMP_MS INTEGER NOT NULL PRIMARY KEY,
            N_BEATS INTEGER NOT NULL,
            HR_BPM REAL,
            AVG_RR_MS REAL,
            MIN_RR_MS INTEGER,
            MAX_RR_MS INTEGER,
            STDDEV_RR_MS REAL,
            RMSSD_MS REAL,
            LN_RMSSD REAL,
            VAGAL_INDEX REAL,
            RMSSD_PCT REAL,
            SDNN_MS REAL,
            RMSSD_SDNN_RATIO REAL,
            PNN50 REAL,
            LF_MS2 REAL,
            HF_MS2 REAL,
            LF_HF_RATIO REAL,
            DFA_ALPHA1 REAL
        )
    """)
    cur.executemany(
        "INSERT INTO HRV_MINUTE_AGGREGATED VALUES "
        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                r["timestamp_ms"], r["n_beats"], r["hr_bpm"], r["avg_rr_ms"],
                r["min_rr_ms"], r["max_rr_ms"], r["stddev_rr_ms"], r["rmssd_ms"],
                r["ln_rmssd"], r["vagal_index"], r["rmssd_pct"], r["sdnn_ms"],
                r["rmssd_sdnn_ratio"], r["pnn50"], r["lf_ms2"], r["hf_ms2"],
                r["lf_hf_ratio"], r["dfa_alpha1"],
            )
            for r in rows
        ],
    )
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM HRV_MINUTE_AGGREGATED")
    total = cur.fetchone()[0]

    cur.execute(
        "SELECT TIMESTAMP_MS, N_BEATS, HR_BPM, RMSSD_MS, LF_HF_RATIO, DFA_ALPHA1 "
        "FROM HRV_MINUTE_AGGREGATED WHERE RMSSD_MS IS NOT NULL "
        "ORDER BY RMSSD_MS DESC LIMIT 1"
    )
    sample = cur.fetchone()
    conn.close()
    return total, sample

def main():
    parser = argparse.ArgumentParser(description="HRV minute aggregation")
    parser.add_argument("--device-id", type=int, default=None)
    parser.add_argument(
        "--lf-hf",
        action="store_true",
        help="Enable LF/HF Lomb-Scargle computation (default: off, slow)",
    )
    parser.add_argument(
        "--dfa",
        action="store_true",
        help="Enable DFA alpha1 computation (default: off)",
    )
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"Fehler: Datenbank nicht gefunden: {DB_PATH}")
        sys.exit(1)

    t_total = time.monotonic()

    t0 = time.monotonic()
    rr_data, device_id, device_name = load_rr_data(DB_PATH, args.device_id)
    if not rr_data:
        print("ERROR: No RR data after filtering", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(rr_data)} RR intervals from device {device_id} ({device_name}) [{time.monotonic() - t0:.2f}s]")
    print(f"Time range: {rr_data[0][0]} - {rr_data[-1][0]}")

    minute_count = len({(ts // 60000) for ts, _ in rr_data})
    print(f"Processing {minute_count} minutes...")

    t0 = time.monotonic()
    rows = compute_minute_metrics(rr_data, enable_lf_hf=args.lf_hf, enable_dfa=args.dfa)
    print(f"Minute metrics computed: {len(rows)} rows [{time.monotonic() - t0:.2f}s]")

    t0 = time.monotonic()
    total, sample = write_results(DB_PATH, rows)
    print(f"Written {total} rows to HRV_MINUTE_AGGREGATED [{time.monotonic() - t0:.2f}s]")
    print(f"Total runtime: {time.monotonic() - t_total:.2f}s")

    if sample:
        ts, n, hr, rmssd, lfhf, dfa = sample
        print(
            f"Sample (max RMSSD): ts={ts} n_beats={n} hr={hr:.1f} "
            f"rmssd={rmssd:.1f} lf_hf={lfhf} dfa_alpha1={dfa}"
        )


if __name__ == "__main__":
    main()
