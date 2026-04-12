#!/usr/bin/env python3
"""
Statistical Summary
===================
Computes seizure correlations and period comparisons from
night_characteristics.csv and seizures.csv.

Output: statistical_summary.csv (seizure correlation table)
        seizure_cycle_profile.csv (cycle means at day -2, -1, 0 vs baseline)

Usage:
    python3 statistical_summary.py
    python3 statistical_summary.py --data-dir . --seizure-file ../seizures.csv
    python3 statistical_summary.py --pre-end 2025-02-28 --post-start 2026-03-01
"""

import sys
from pathlib import Path
from datetime import date, timedelta

import numpy as np
import pandas as pd
from scipy import stats as sp_stats


# ---------------------------------------------------------------------------
# Config defaults
# ---------------------------------------------------------------------------
DEFAULT_PRE_END = "2025-02-28"
DEFAULT_POST_START = "2026-03-01"

SEIZURE_LAGS = {
    "same": [0],
    "next1": [1],
    "next2": [2],
    "prev1": [-1],
}

PARAMS = [
    "n_plateaus",
    "max_depth",
    "base_level",
    "total_range",
    "dur_cv",
    "count_cv",
    "break_frac",
    "spacing_cv",
    "stack_symmetry",
    "intra_dur_cv",
    "frac_high",
    "frac_vhigh",
    "n_d3",
    "n_phases",
    "mean_phase_dur",
    "phase_dur_cv",
    "mean_phase_std",
    "std_ratio_2nd_1st",
    "dur_ratio_2nd_1st",
    "n_nadirs",
    "nadir_mean",
    "nadir_std",
    "nadir_range",
    "nadir_slope",
]


# ---------------------------------------------------------------------------
# Correlation analysis
# ---------------------------------------------------------------------------
def compute_correlations(df, sz_dates, params, lags, p_threshold=0.15):
    """
    Point-biserial correlation and Mann-Whitney U for each param × lag.
    Returns DataFrame of results.
    """
    # Add seizure lag columns
    for lag_name, lag_days in lags.items():
        df[f"sz_{lag_name}"] = df["night"].apply(
            lambda n: any(
                (n + timedelta(days=d)) in sz_dates for d in lag_days
            )
        )

    results = []
    for lag_name in lags:
        sz_col = f"sz_{lag_name}"
        for param in params:
            v = df.dropna(subset=[param])
            if v[sz_col].nunique() < 2 or v[sz_col].sum() < 3:
                continue
            if v[param].nunique() < 3:
                continue

            r, p_pb = sp_stats.pointbiserialr(
                v[sz_col].astype(int), v[param]
            )
            g0 = v.loc[~v[sz_col], param]
            g1 = v.loc[v[sz_col], param]
            if len(g1) < 3:
                continue
            _, p_mw = sp_stats.mannwhitneyu(
                g0, g1, alternative="two-sided"
            )
            p_min = min(p_pb, p_mw)

            results.append(
                {
                    "lag": lag_name,
                    "param": param,
                    "r": round(r, 3),
                    "p_pointbiserial": round(p_pb, 4),
                    "p_mannwhitney": round(p_mw, 4),
                    "p_min": round(p_min, 4),
                    "median_no_seizure": round(g0.median(), 3),
                    "median_seizure": round(g1.median(), 3),
                    "n_no_seizure": len(g0),
                    "n_seizure": len(g1),
                    "significant": p_min < 0.05,
                    "trend": p_min < p_threshold,
                }
            )

    return pd.DataFrame(results)


# ---------------------------------------------------------------------------
# Seizure cycle profile
# ---------------------------------------------------------------------------
def compute_cycle_profile(df, sz_dates, params):
    """
    For each seizure, collect nights at lag 0, -1, -2 and baseline.
    Returns DataFrame with mean/std/n per category per param.
    """
    # Tag each night
    categories = []
    for _, row in df.iterrows():
        n = row["night"]
        if n in sz_dates:
            categories.append("day_0")
        elif (n + timedelta(days=1)) in sz_dates:
            categories.append("day_minus1")
        elif (n + timedelta(days=2)) in sz_dates:
            categories.append("day_minus2")
        else:
            categories.append("baseline")
    df = df.copy()
    df["cycle_position"] = categories

    rows = []
    for cat in ["baseline", "day_minus2", "day_minus1", "day_0"]:
        subset = df[df["cycle_position"] == cat]
        for param in params:
            vals = subset[param].dropna()
            rows.append(
                {
                    "cycle_position": cat,
                    "param": param,
                    "mean": round(vals.mean(), 3) if len(vals) > 0 else np.nan,
                    "std": round(vals.std(), 3) if len(vals) > 1 else np.nan,
                    "median": round(vals.median(), 3) if len(vals) > 0 else np.nan,
                    "n": len(vals),
                }
            )

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    script_dir = Path(__file__).parent
    data_dir = script_dir
    out_dir = script_dir
    seizure_file = None
    pre_end = DEFAULT_PRE_END
    post_start = DEFAULT_POST_START

    # Parse args
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--data-dir":
            data_dir = Path(args[i + 1]); i += 2
        elif args[i] == "--out-dir":
            out_dir = Path(args[i + 1]); i += 2
        elif args[i] == "--seizure-file":
            seizure_file = Path(args[i + 1]); i += 2
        elif args[i] == "--pre-end":
            pre_end = args[i + 1]; i += 2
        elif args[i] == "--post-start":
            post_start = args[i + 1]; i += 2
        else:
            i += 1

    out_dir.mkdir(parents=True, exist_ok=True)

    # Find seizure file
    if seizure_file is None:
        for candidate in [
            data_dir / "seizures.csv",
            data_dir / ".." / "seizures.csv",
            Path("/mnt/user-data/uploads/seizures.csv"),
        ]:
            if candidate.exists():
                seizure_file = candidate
                break
    if seizure_file is None or not seizure_file.exists():
        print("ERROR: seizures.csv not found", file=sys.stderr)
        sys.exit(1)

    # Load data
    chars = pd.read_csv(
        data_dir / "night_characteristics.csv", dtype={"night_date": str}
    )
    chars["night"] = chars["night_date"].apply(date.fromisoformat)

    seiz = pd.read_csv(str(seizure_file))
    seiz["date"] = pd.to_datetime(
        seiz["Date"], format="%d/%m/%Y %H:%M:%S"
    ).dt.date
    sz_dates = set(seiz["date"])

    # Period assignment
    chars["period"] = chars["night_date"].apply(
        lambda n: "PRE" if n <= pre_end
        else ("POST" if n >= post_start else "GAP")
    )

    print(f"Nights: {len(chars)}")
    print(f"  PRE:  {len(chars[chars.period == 'PRE'])}")
    print(f"  POST: {len(chars[chars.period == 'POST'])}")
    print(f"  GAP:  {len(chars[chars.period == 'GAP'])}")
    print(f"Seizure dates: {len(sz_dates)}")
    print(f"Period split: PRE <= {pre_end}, POST >= {post_start}")

    # --- 1. Correlations: all data ---
    print(f"\n{'='*70}")
    print("CORRELATIONS — ALL DATA")
    print(f"{'='*70}")
    corr_all = compute_correlations(
        chars.copy(), sz_dates, PARAMS, SEIZURE_LAGS
    )
    sig_all = corr_all[corr_all["trend"]]
    for _, row in sig_all.sort_values("p_min").iterrows():
        marker = "**" if row["significant"] else "* "
        print(
            f"  {marker} {row['lag']:<6s} {row['param']:<25s} "
            f"r={row['r']:+.3f}  p={row['p_min']:.3f}  "
            f"no_sz={row['median_no_seizure']:.2f}  "
            f"sz={row['median_seizure']:.2f}"
        )

    # --- 2. Correlations: PRE only ---
    pre_data = chars[chars["period"] == "PRE"].copy()
    if len(pre_data) > 10:
        print(f"\n{'='*70}")
        print(f"CORRELATIONS — PRE (n={len(pre_data)})")
        print(f"{'='*70}")
        corr_pre = compute_correlations(
            pre_data, sz_dates, PARAMS, SEIZURE_LAGS
        )
        sig_pre = corr_pre[corr_pre["trend"]]
        for _, row in sig_pre.sort_values("p_min").iterrows():
            marker = "**" if row["significant"] else "* "
            print(
                f"  {marker} {row['lag']:<6s} {row['param']:<25s} "
                f"r={row['r']:+.3f}  p={row['p_min']:.3f}  "
                f"no_sz={row['median_no_seizure']:.2f}  "
                f"sz={row['median_seizure']:.2f}"
            )

    # --- 3. Correlations: POST only ---
    post_data = chars[chars["period"] == "POST"].copy()
    if len(post_data) > 10:
        print(f"\n{'='*70}")
        print(f"CORRELATIONS — POST (n={len(post_data)})")
        print(f"{'='*70}")
        corr_post = compute_correlations(
            post_data, sz_dates, PARAMS, SEIZURE_LAGS
        )
        sig_post = corr_post[corr_post["trend"]]
        for _, row in sig_post.sort_values("p_min").iterrows():
            marker = "**" if row["significant"] else "* "
            print(
                f"  {marker} {row['lag']:<6s} {row['param']:<25s} "
                f"r={row['r']:+.3f}  p={row['p_min']:.3f}  "
                f"no_sz={row['median_no_seizure']:.2f}  "
                f"sz={row['median_seizure']:.2f}"
            )

    # --- 4. Cycle profiles ---
    print(f"\n{'='*70}")
    print("SEIZURE CYCLE PROFILE")
    print(f"{'='*70}")

    cycle_rows = []
    for period_name, period_data in [
        ("ALL", chars.copy()),
        ("PRE", pre_data),
        ("POST", post_data),
    ]:
        if len(period_data) < 5:
            continue
        profile = compute_cycle_profile(period_data, sz_dates, PARAMS)
        profile["period"] = period_name
        cycle_rows.append(profile)

        # Print key metrics
        print(f"\n  {period_name}:")
        for param in [
            "nadir_slope", "break_frac", "spacing_cv",
            "stack_symmetry", "base_level", "phase_dur_cv",
        ]:
            p_data = profile[profile["param"] == param]
            vals = {
                row["cycle_position"]: f"{row['mean']:.3f}(n={row['n']})"
                if not np.isnan(row["mean"])
                else "n/a"
                for _, row in p_data.iterrows()
            }
            print(
                f"    {param:<20s}  "
                f"base={vals.get('baseline','n/a'):>14s}  "
                f"d-2={vals.get('day_minus2','n/a'):>14s}  "
                f"d-1={vals.get('day_minus1','n/a'):>14s}  "
                f"d0={vals.get('day_0','n/a'):>14s}"
            )

    # --- Save outputs ---
    corr_all.to_csv(out_dir / "statistical_summary.csv", index=False)
    print(f"\n→ {out_dir / 'statistical_summary.csv'}")

    if cycle_rows:
        cycle_df = pd.concat(cycle_rows, ignore_index=True)
        cycle_df.to_csv(out_dir / "seizure_cycle_profile.csv", index=False)
        print(f"→ {out_dir / 'seizure_cycle_profile.csv'}")

    # PRE/POST period comparison
    if len(pre_data) > 5 and len(post_data) > 5:
        print(f"\n{'='*70}")
        print("PRE vs POST COMPARISON")
        print(f"{'='*70}")
        compare_rows = []
        for param in PARAMS:
            pre_vals = pre_data[param].dropna()
            post_vals = post_data[param].dropna()
            if len(pre_vals) < 3 or len(post_vals) < 3:
                continue
            _, p_mw = sp_stats.mannwhitneyu(
                pre_vals, post_vals, alternative="two-sided"
            )
            compare_rows.append(
                {
                    "param": param,
                    "pre_median": round(pre_vals.median(), 3),
                    "post_median": round(post_vals.median(), 3),
                    "delta": round(post_vals.median() - pre_vals.median(), 3),
                    "p_mannwhitney": round(p_mw, 4),
                    "n_pre": len(pre_vals),
                    "n_post": len(post_vals),
                }
            )
            if p_mw < 0.1:
                d = "↑" if post_vals.median() > pre_vals.median() else "↓"
                sig = "**" if p_mw < 0.05 else "* "
                print(
                    f"  {sig} {param:<25s} PRE={pre_vals.median():.3f}  "
                    f"POST={post_vals.median():.3f}  p={p_mw:.3f} {d}"
                )
        compare_df = pd.DataFrame(compare_rows)
        compare_df.to_csv(out_dir / "pre_post_comparison.csv", index=False)
        print(f"\n→ {out_dir / 'pre_post_comparison.csv'}")


if __name__ == "__main__":
    main()
