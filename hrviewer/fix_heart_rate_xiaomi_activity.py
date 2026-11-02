"""#!/usr/bin/env python3"""
'\nRepair gaps in the Hive series `heart_rate_xiaomi_activity` only.\n\ngadgetbridge_migrate.py imports incrementally (source TIMESTAMP >= newest\nstored ts). Rows that the band synced late with older timestamps are below\nthat watermark and never imported. This script compares the complete source\ntable against the Hive and writes the missing (or differing) samples.\n\nDefault is a dry run; pass --apply to write.\n'
import argparse
import sqlite3
from pathlib import Path
import pandas as pd
import hive_io
from hive_io import HiveWriter
METRIC = 'heart_rate_xiaomi_activity'
TABLE = 'XIAOMI_ACTIVITY_SAMPLE'
HR_MIN_VALID = 30
DEFAULT_DB_PATH = Path(__file__).parent / 'Gadgetbridge'

def load_source(db_path: Path) -> pd.DataFrame:
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    try:
        df = pd.read_sql_query(
            f'SELECT [TIMESTAMP] AS ts_s, [HEART_RATE] AS value FROM [{TABLE}] WHERE [TIMESTAMP] IS NOT NULL AND [HEART_RATE] IS NOT NULL AND [HEART_RATE] >= ?',
            conn,
            params=(
                HR_MIN_VALID,
            ))
    finally:
        conn.close()
    df['ts'] = df['ts_s'].astype('int64') * 1000
    df['value'] = df['value'].astype('float64')
    '# Same (ts) twice in the source: last row wins, like the Hive merge.'
    return df.drop_duplicates('ts', keep='last')[['ts', 'value']]

def load_hive() -> pd.DataFrame:
    if not hive_io._has_files(METRIC):
        return pd.DataFrame({'ts': pd.Series(dtype='int64'), 'value': pd.Series(dtype='float64')})
    glob = hive_io._metric_glob(METRIC)
    return hive_io._connect().execute(f"SELECT ts, value FROM read_parquet('{glob}')").df()

def main() -> None:
    parser = argparse.ArgumentParser(description='Repair gaps in heart_rate_xiaomi_activity.')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB_PATH, metavar='DB_FILE',
                        help='Source Gadgetbridge SQLite file (default: %(default)s).')
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Write missing/differing samples to the Hive (default: dry run).')
    args, _ = parser.parse_known_args()
    if not args.db.exists():
        raise SystemExit(f'ERROR: source database not found: {args.db}')
    src = load_source(args.db)
    hive = load_hive()
    merged = src.merge(hive, on='ts', how='left', suffixes=('', '_hive'))
    missing = merged[merged['value_hive'].isna()]
    differing = merged[merged['value_hive'].notna() & (merged['value'] != merged['value_hive'])]
    only_hive = len(hive) - (len(src) - len(missing))
    print(f'Source samples (valid): {len(src):,}')
    print(f'Hive samples:           {len(hive):,}')
    print(f'Missing in Hive:        {len(missing):,}')
    print(f'Differing value:        {len(differing):,}')
    print(f'Only in Hive:           {only_hive:,} (left untouched)')
    if len(missing):
        days = pd.to_datetime(missing['ts'], unit='ms', utc=True).dt.strftime('%Y-%m-%d').value_counts().sort_index()
        print(f'\nAffected days: {len(days)}')
        for day, n in days.items():
            print(f'  {day}  {n:>6,}')
    todo = pd.concat([missing, differing])[['ts', 'value']]
    if todo.empty:
        print('\nNo gaps found.')
        return
    if not args.apply:
        print('\nDry run. Re-run with --apply to write.')
        return
    writer = HiveWriter()
    for ts, value in todo.itertuples(index=False):
        writer.add(METRIC, int(ts), float(value))
    writer.flush()
    print(f'\nWrote {writer.total:,} samples to the Hive.')
    print('Re-run hrv_aggregate.py / spectral_bands_aggregate.py with --full if they depend on this series.')
if __name__ == '__main__':
    main()