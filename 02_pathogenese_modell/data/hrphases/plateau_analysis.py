#!/usr/bin/env python3
"""
HR Plateau Analysis Pipeline
=============================
Reads Gadgetbridge SQLite DB and seizures.csv.
Outputs: nadirs.csv, phases.csv, plateaus.csv

Algorithm:
1. MHR10 = 10-min centered rolling mean of HR
2. Nadirs = custom local minima finder (min_depth=0.5, min_dist=10)
3. Phases = segments between consecutive nadirs (duration, HR mean, HR std)
4. Plateaus = two-pass grouping of nadirs by level + water-line connectivity
   - Pass 1: tol=1.0 bpm (greedy temporal)
   - Pass 2: merge singletons within tol=1.3 bpm
5. Plateau boundaries = extend lowest nadir level left/right until MHR10 crosses below
6. Stack depth = count of lower-level plateaus that temporally contain this one
"""

import sqlite3
import sys
from pathlib import Path
from datetime import timedelta
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TZ = ZoneInfo("Europe/Berlin")
NADIR_MIN_DEPTH = 0.5   # bpm
NADIR_MIN_DIST = 10     # minutes
MHR_WINDOW = 10         # minutes
PLATEAU_TOL1 = 1.0      # bpm, pass 1
PLATEAU_TOL2 = 1.3      # bpm, pass 2 (singleton merge)
MIN_SLEEP_DURATION = 60  # minutes


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def ts_to_local(ts_epoch, tz=TZ):
    """Unix epoch (seconds) → tz-aware datetime."""
    return pd.Timestamp(ts_epoch, unit="s", tz="UTC").tz_convert(tz)


def compute_mhr10(hr_values, window=MHR_WINDOW):
    """Centered rolling mean."""
    return (
        pd.Series(hr_values)
        .rolling(window, center=True, min_periods=window // 2 + 1)
        .mean()
        .values
    )


# ---------------------------------------------------------------------------
# 1. Nadir detection
# ---------------------------------------------------------------------------
def find_nadirs(mhr, min_depth=NADIR_MIN_DEPTH, min_dist=NADIR_MIN_DIST):
    """
    Custom local-minimum finder.
    Handles flat bottoms, enforces minimum depth and inter-nadir distance.
    """
    n = len(mhr)
    nadirs = []
    i = 1
    while i < n - 1:
        if np.isnan(mhr[i]):
            i += 1
            continue
        if mhr[i] <= mhr[i - 1]:
            # Walk forward through flat/descending region
            j = i
            while j < n - 1 and mhr[j + 1] <= mhr[j] + 0.1:
                j += 1
            # Find actual minimum in neighbourhood
            seg_start = max(0, i - 1)
            seg_end = min(n, j + 2)
            seg = mhr[seg_start:seg_end]
            if len(seg) == 0:
                i = j + 1
                continue
            min_pos = seg_start + int(np.nanargmin(seg))
            # Compute depth (prominence-like)
            left_seg = mhr[max(0, min_pos - min_dist) : min_pos]
            left_seg = left_seg[~np.isnan(left_seg)]
            left_max = np.max(left_seg) if len(left_seg) > 0 else mhr[min_pos]
            right_seg = mhr[min_pos + 1 : min(n, min_pos + min_dist + 1)]
            right_seg = right_seg[~np.isnan(right_seg)]
            right_max = np.max(right_seg) if len(right_seg) > 0 else mhr[min_pos]
            depth = min(left_max, right_max) - mhr[min_pos]
            if depth >= min_depth and (
                not nadirs or min_pos - nadirs[-1] >= min_dist
            ):
                nadirs.append(int(min_pos))
            i = j + 1
        else:
            i += 1
    return nadirs


# ---------------------------------------------------------------------------
# 2. Phase computation
# ---------------------------------------------------------------------------
def compute_phases(hr_raw, mhr, nadir_indices, timestamps):
    """
    Phases = segments between consecutive nadirs.
    Returns list of dicts.
    """
    phases = []
    # Add implicit boundaries at start and end
    boundaries = [0] + nadir_indices + [len(hr_raw) - 1]
    for k in range(len(boundaries) - 1):
        s, e = boundaries[k], boundaries[k + 1]
        if e <= s:
            continue
        seg = hr_raw[s:e]
        phases.append(
            {
                "start_idx": s,
                "end_idx": e,
                "start_ts": timestamps[s],
                "end_ts": timestamps[e],
                "duration_min": e - s,
                "hr_mean": float(np.mean(seg)),
                "hr_std": float(np.std(seg)),
            }
        )
    return phases


# ---------------------------------------------------------------------------
# 3. Plateau detection
# ---------------------------------------------------------------------------
def water_connects(a_idx, b_idx, level, mhr, tolerance=0.5):
    """Check if MHR10 stays >= level between two indices."""
    lo, hi = min(a_idx, b_idx), max(a_idx, b_idx)
    return np.nanmin(mhr[lo : hi + 1]) >= level - tolerance


def group_plateaus(nadir_indices, nadir_values, mhr):
    """
    Two-pass plateau grouping.
    Pass 1: greedy temporal, tol=PLATEAU_TOL1
    Pass 2: merge singletons, tol=PLATEAU_TOL2
    """
    n = len(nadir_indices)
    if n == 0:
        return []

    # --- Pass 1: greedy temporal grouping ---
    groups = []  # list of lists of nadir-list-indices (0..n-1)
    for ni in range(n):
        best_group = None
        best_dist = float("inf")
        for gi, group in enumerate(groups):
            gmean = np.mean([nadir_values[i] for i in group])
            dist = abs(nadir_values[ni] - gmean)
            if dist > PLATEAU_TOL1:
                continue
            level = min(nadir_values[ni], min(nadir_values[i] for i in group))
            connected = any(
                water_connects(nadir_indices[ni], nadir_indices[m], level, mhr)
                for m in group
            )
            if connected and dist < best_dist:
                best_group = gi
                best_dist = dist
        if best_group is not None:
            groups[best_group].append(ni)
        else:
            groups.append([ni])

    # --- Pass 2: merge singletons ---
    merged = True
    while merged:
        merged = False
        for i in range(len(groups)):
            if len(groups[i]) > 1:
                continue
            for j in range(i + 1, len(groups)):
                if len(groups[j]) > 1:
                    continue
                gmean_i = nadir_values[groups[i][0]]
                gmean_j = nadir_values[groups[j][0]]
                if abs(gmean_i - gmean_j) > PLATEAU_TOL2:
                    continue
                level = min(gmean_i, gmean_j)
                if water_connects(
                    nadir_indices[groups[i][0]],
                    nadir_indices[groups[j][0]],
                    level,
                    mhr,
                ):
                    groups[i].extend(groups[j])
                    groups.pop(j)
                    merged = True
                    break
            if merged:
                break

    return groups


def plateau_boundaries(nadir_indices, nadir_values, group, mhr):
    """
    Compute plateau start/end by extending the lowest nadir's level
    left and right until MHR10 crosses below it.
    Returns (level, start_idx, end_idx).
    """
    # Find lowest nadir in group
    min_ni = min(group, key=lambda i: nadir_values[i])
    level = nadir_values[min_ni]
    pos = nadir_indices[min_ni]
    n = len(mhr)
    # Extend left
    left = pos
    while left > 0 and mhr[left - 1] >= level - 0.5:
        left -= 1
    # Extend right
    right = pos
    while right < n - 1 and mhr[right + 1] >= level - 0.5:
        right += 1
    return level, left, right


def compute_stack_depth(plateaus):
    """
    For each plateau, count how many other plateaus with LOWER level
    temporally contain it (start <= this.start AND end >= this.end).
    """
    for i, p in enumerate(plateaus):
        depth = 0
        for j, q in enumerate(plateaus):
            if i == j:
                continue
            if (
                q["level"] < p["level"]
                and q["start_idx"] <= p["start_idx"]
                and q["end_idx"] >= p["end_idx"]
            ):
                depth += 1
        p["stack_depth"] = depth
    return plateaus


# ---------------------------------------------------------------------------
# Main pipeline: process one night
# ---------------------------------------------------------------------------
def process_night(hr_raw, timestamps, night_date):
    """
    Full pipeline for one night.
    Returns (nadirs_list, phases_list, plateaus_list).
    """
    mhr = compute_mhr10(hr_raw)
    nadir_indices = find_nadirs(mhr)

    if len(nadir_indices) == 0:
        return [], [], []

    nadir_values = [float(mhr[i]) for i in nadir_indices]

    # --- Nadirs ---
    nadirs_out = []
    for idx, val in zip(nadir_indices, nadir_values):
        nadirs_out.append(
            {
                "night_date": night_date,
                "time": ts_to_local(timestamps[idx]).strftime("%H:%M"),
                "timestamp": int(timestamps[idx]),
                "mhr10": round(val, 1),
            }
        )

    # --- Phases ---
    phases_raw = compute_phases(hr_raw, mhr, nadir_indices, timestamps)
    phases_out = []
    for p in phases_raw:
        phases_out.append(
            {
                "night_date": night_date,
                "start_time": ts_to_local(p["start_ts"]).strftime("%H:%M"),
                "end_time": ts_to_local(p["end_ts"]).strftime("%H:%M"),
                "duration_min": p["duration_min"],
                "hr_mean": round(p["hr_mean"], 1),
                "hr_std": round(p["hr_std"], 1),
            }
        )

    # --- Plateaus ---
    groups = group_plateaus(nadir_indices, nadir_values, mhr)
    plateaus_out = []
    for g in groups:
        level, s_idx, e_idx = plateau_boundaries(
            nadir_indices, nadir_values, g, mhr
        )
        n_nadirs = len(g)
        plateaus_out.append(
            {
                "night_date": night_date,
                "start_time": ts_to_local(timestamps[s_idx]).strftime("%H:%M"),
                "end_time": ts_to_local(timestamps[e_idx]).strftime("%H:%M"),
                "start_idx": s_idx,
                "end_idx": e_idx,
                "duration_min": e_idx - s_idx,
                "level": round(level, 1),
                "n_nadirs": n_nadirs,
                "stack_depth": 0,  # computed after all plateaus collected
            }
        )

    plateaus_out = compute_stack_depth(plateaus_out)

    # Remove internal index columns
    for p in plateaus_out:
        del p["start_idx"]
        del p["end_idx"]

    return nadirs_out, phases_out, plateaus_out


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_data(db_path, seizure_path):
    """Load sleep sessions, HR data, and seizure dates."""
    con = sqlite3.connect(db_path)

    # Sleep sessions
    sleep = pd.read_sql(
        "SELECT TIMESTAMP/1000 as sleep_start, WAKEUP_TIME/1000 as sleep_end, "
        "TOTAL_DURATION FROM XIAOMI_SLEEP_TIME_SAMPLE WHERE TOTAL_DURATION > %d"
        % MIN_SLEEP_DURATION,
        con,
    )
    sleep["start_dt"] = pd.to_datetime(
        sleep["sleep_start"], unit="s", utc=True
    ).dt.tz_convert(TZ)
    sleep["end_dt"] = pd.to_datetime(
        sleep["sleep_end"], unit="s", utc=True
    ).dt.tz_convert(TZ)
    # Night date = wake-up date
    sleep["night_date"] = sleep["end_dt"].dt.date
    # Keep longest session per night
    sleep = (
        sleep.sort_values("TOTAL_DURATION", ascending=False)
        .drop_duplicates("night_date", keep="first")
        .sort_values("night_date")
        .reset_index(drop=True)
    )

    # HR activity data
    act = pd.read_sql(
        "SELECT TIMESTAMP, HEART_RATE FROM XIAOMI_ACTIVITY_SAMPLE "
        "WHERE HEART_RATE > 0 AND HEART_RATE < 200",
        con,
    )
    act = act.sort_values("TIMESTAMP").reset_index(drop=True)
    con.close()

    # Seizures
    seiz = pd.read_csv(seizure_path)
    seiz["date"] = pd.to_datetime(
        seiz["Date"], format="%d/%m/%Y %H:%M:%S"
    ).dt.date

    return sleep, act, seiz


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # Resolve paths
    script_dir = Path(__file__).parent
    # Try common locations for input files
    for candidate_db in [
        script_dir / "Gadgetbridge",
        script_dir / "gb" / "Gadgetbridge",
        Path("/mnt/user-data/uploads/Gadgetbridge"),
        Path("/home/claude/gb/Gadgetbridge"),
    ]:
        if candidate_db.exists():
            db_path = candidate_db
            break
    else:
        print("ERROR: Gadgetbridge DB not found", file=sys.stderr)
        sys.exit(1)

    for candidate_csv in [
        script_dir / "seizures.csv",
        Path("/mnt/user-data/uploads/seizures.csv"),
    ]:
        if candidate_csv.exists():
            seizure_path = candidate_csv
            break
    else:
        print("ERROR: seizures.csv not found", file=sys.stderr)
        sys.exit(1)

    print(f"DB: {db_path}")
    print(f"Seizures: {seizure_path}")

    sleep, act, seiz = load_data(str(db_path), str(seizure_path))
    print(f"Sleep sessions: {len(sleep)}")
    print(f"HR samples: {len(act)}")
    print(f"Seizure dates: {len(seiz)}")

    all_nadirs = []
    all_phases = []
    all_plateaus = []

    for _, srow in sleep.iterrows():
        ts_start = srow["sleep_start"]
        ts_end = srow["sleep_end"]
        night_date = srow["night_date"]

        mask = (act["TIMESTAMP"] >= ts_start) & (act["TIMESTAMP"] <= ts_end)
        hr_night = act.loc[mask, ["TIMESTAMP", "HEART_RATE"]].copy()

        if len(hr_night) < 30:
            continue

        hr_raw = hr_night["HEART_RATE"].values.astype(float)
        timestamps = hr_night["TIMESTAMP"].values.astype(float)

        nadirs, phases, plateaus = process_night(hr_raw, timestamps, night_date)
        all_nadirs.extend(nadirs)
        all_phases.extend(phases)
        all_plateaus.extend(plateaus)

    # Write CSVs
    out_dir = script_dir
    
    df_nadirs = pd.DataFrame(all_nadirs)
    df_nadirs.to_csv(out_dir / "nadirs.csv", index=False)
    print(f"\nNadirs: {len(df_nadirs)} → nadirs.csv")

    df_phases = pd.DataFrame(all_phases)
    df_phases.to_csv(out_dir / "phases.csv", index=False)
    print(f"Phases: {len(df_phases)} → phases.csv")

    df_plateaus = pd.DataFrame(all_plateaus)
    df_plateaus.to_csv(out_dir / "plateaus.csv", index=False)
    print(f"Plateaus: {len(df_plateaus)} → plateaus.csv")

    # Summary
    nights = df_nadirs["night_date"].nunique() if len(df_nadirs) > 0 else 0
    print(f"\nProcessed {nights} nights")
    if len(df_nadirs) > 0:
        print(f"Nadirs/night:   {len(df_nadirs)/nights:.1f} avg")
    if len(df_phases) > 0:
        print(f"Phases/night:   {len(df_phases)/nights:.1f} avg")
    if len(df_plateaus) > 0:
        print(f"Plateaus/night: {len(df_plateaus)/nights:.1f} avg")
        depth_dist = df_plateaus["stack_depth"].value_counts().sort_index()
        print(f"Stack depth distribution: {dict(depth_dist)}")


if __name__ == "__main__":
    main()
