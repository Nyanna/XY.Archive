#!/usr/bin/env python3
"""Gibt Zeilenanzahl und belegten Speicher je Tabelle einer SQLite-DB aus.

Tatsächliche Bytes kommen aus der dbstat-Virtual-Table (Page-genau, inkl.
Overflow- und Index-Pages). Ist dbstat nicht verfügbar, wird auf eine
Abschätzung per length()-Summe zurückgefallen.
"""
import sqlite3
import sys


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def has_dbstat(con: sqlite3.Connection) -> bool:
    try:
        con.execute("SELECT * FROM dbstat LIMIT 1")
        return True
    except sqlite3.OperationalError:
        return False


def sizes_via_dbstat(con: sqlite3.Connection) -> dict[str, int]:
    # Bytes je logischem Namen (Tabelle/Index). Tabellenname per
    # name-Spalte; Indizes werden über tbl_name dem Owner zugeordnet.
    idx_owner = dict(
        con.execute(
            "SELECT name, tbl_name FROM sqlite_master WHERE type='index'"
        ).fetchall()
    )
    out: dict[str, int] = {}
    rows = con.execute(
        "SELECT name, SUM(pgsize) FROM dbstat GROUP BY name"
    ).fetchall()
    for name, pgsize in rows:
        owner = idx_owner.get(name, name)  # Index -> Tabelle
        out[owner] = out.get(owner, 0) + (pgsize or 0)
    return out


def sizes_via_length(con: sqlite3.Connection, tables: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for t in tables:
        cols = [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]
        if not cols:
            out[t] = 0
            continue
        expr = " + ".join(f'COALESCE(LENGTH("{c}"),0)' for c in cols)
        out[t] = con.execute(f'SELECT COALESCE(SUM({expr}),0) FROM "{t}"').fetchone()[0]
    return out


def main(path: str) -> None:
    con = sqlite3.connect(path)
    con.execute("PRAGMA page_size")  # nur zur Sicherheit geöffnet

    tables = [
        r[0]
        for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]

    counts = {t: con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in tables}

    if has_dbstat(con):
        sizes = sizes_via_dbstat(con)
        size_label = "Bytes (dbstat, exakt)"
    else:
        sizes = sizes_via_length(con, tables)
        size_label = "Bytes (length-Schätzung)"

    rows = sorted(tables, key=lambda t: sizes.get(t, 0), reverse=True)
    w = max((len(t) for t in tables), default=5)

    print(f"{'Tabelle':<{w}}  {'Zeilen':>12}  {'Größe':>12}   ({size_label})")
    print("-" * (w + 45))
    total = 0
    for t in rows:
        s = sizes.get(t, 0)
        total += s
        print(f"{t:<{w}}  {counts[t]:>12,}  {human(s):>12}")
    print("-" * (w + 45))
    print(f"{'SUMME':<{w}}  {sum(counts.values()):>12,}  {human(total):>12}")
    con.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Aufruf: python3 sqlite_table_sizes.py <pfad.sqlite>")
    main(sys.argv[1])
