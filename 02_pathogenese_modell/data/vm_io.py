#!/usr/bin/env python3
"""
Victoria Metrics I/O helper
===========================

Thin client around the Victoria Metrics HTTP API used by the Gadgetbridge
migration (write path) and the aggregation scripts (read path).

Data model conventions
-----------------------
Timestamps are always milliseconds since the Unix epoch (VM's native
JSON import/export unit). Values are float64.

Write:  VMWriter batches samples per (metric, labels) series and POSTs
        newline-delimited JSON to /api/v1/import.
Read:   export() streams series back via /api/v1/export.
        latest_timestamp_ms() returns the newest sample timestamp for a
        PromQL selector (used as an incremental watermark).

Performance
-----------
- All HTTP goes through a single module-level requests.Session so TCP+TLS
  and keep-alive are reused across the many small watermark/flush calls.
- Import payloads are serialized with orjson (bytes, no whitespace).
- export() reads 1 MiB byte chunks and decodes each NDJSON line with
  orjson.loads directly on bytes (no per-line unicode sniffing).
"""

import os
import time

import orjson
import requests

VM_URL = os.environ.get("VM_URL", "http://localhost:8428").rstrip("/")
VM_USER = os.environ.get("VM_USER")
VM_PASSWORD = os.environ.get("VM_PASSWORD")
VM_TOKEN = os.environ.get("VM_TOKEN")

# ~200k samples per import request, memory against HTTP overhead
DEFAULT_BATCH_SAMPLES = 200_000

_HTTP_TIMEOUT = (10, 300)  # (connect, read) seconds

# 1 MiB read chunks for /export: far fewer syscalls than the 512 B default.
_EXPORT_CHUNK = 1 << 20


def _make_session() -> requests.Session:
    s = requests.Session()
    if VM_TOKEN:
        s.headers["Authorization"] = f"Bearer {VM_TOKEN}"
    elif VM_USER is not None:
        s.auth = (VM_USER, VM_PASSWORD or "")
    return s


# Shared keep-alive session for every request in this module.
_SESSION = _make_session()


def import_url() -> str:
    return f"{VM_URL}/api/v1/import"


def _post_import(payload: bytes) -> None:
    resp = _SESSION.post(
        import_url(),
        data=payload,
        headers={"Content-Type": "application/x-ndjson"},
        timeout=_HTTP_TIMEOUT,
    )
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"VM import failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )


class VMWriter:
    """Accumulates samples per series and flushes NDJSON to /api/v1/import.

    Usage:
        w = VMWriter()
        w.add("heart_rate", {"source": "generic"}, ts_ms, 78)
        ...
        w.flush()
    """

    def __init__(self, batch_samples: int = DEFAULT_BATCH_SAMPLES):
        self.batch_samples = batch_samples
        self._buf: dict = {}          # series_key -> {"metric":..,"values":..,"timestamps":..}
        self._pending = 0             # samples buffered but not yet POSTed
        self.total = 0                # samples POSTed over the writer's lifetime

    def add(self, name: str, labels: dict, ts_ms: int, value: float) -> None:
        key = (name, tuple(sorted(labels.items())))
        entry = self._buf.get(key)
        if entry is None:
            metric = {"__name__": name}
            metric.update(labels)
            entry = {"metric": metric, "values": [], "timestamps": []}
            self._buf[key] = entry
        entry["values"].append(value)
        entry["timestamps"].append(int(ts_ms))
        self._pending += 1
        if self._pending >= self.batch_samples:
            self.flush()

    def flush(self) -> None:
        if not self._buf:
            return
        payload = b"\n".join(
            orjson.dumps(entry) for entry in self._buf.values()
        ) + b"\n"
        _post_import(payload)
        self.total += self._pending
        self._buf = {}
        self._pending = 0


def force_flush() -> bool:
    """Best-effort: make freshly imported samples immediately queryable.

    Victoria Metrics buffers incoming samples in memory and only makes them
    searchable after -inmemoryDataFlushInterval (default 5s).
    """
    try:
        resp = _SESSION.get(
            f"{VM_URL}/internal/force_flush",
            timeout=_HTTP_TIMEOUT,
        )
        return resp.status_code == 200
    except requests.RequestException:
        raise RuntimeError(
            f"force_flush unavailable"
        )


def latest_timestamp_ms(selector: str, lookback: str = "3650d") -> int | None:
    """Newest sample timestamp (ms) matching a PromQL selector, or None.

    Implemented via MetricsQL tlast_over_time(<selector>[lookback]), which
    yields the timestamp (seconds) of each series' last raw sample; the max
    across the returned per-series scalars is the watermark.
    """
    query = f"tlast_over_time({selector}[{lookback}])"
    resp = _SESSION.get(
        f"{VM_URL}/api/v1/query",
        params={"query": query, "time": str(int(time.time()))},
        timeout=_HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise RuntimeError(f"VM query failed: {data}")
    results = data["data"]["result"]
    if not results:
        return None
    # value = [eval_ts, "<scalar>"]; the scalar is the sample ts in seconds.
    max_sec = max(float(r["value"][1]) for r in results)
    return int(round(max_sec * 1000))


def delete_series(match: str) -> None:
    """Delete every series matching a selector (whole series, no time range).

    Used by the aggregators for --full recomputes: since VM does not
    deduplicate samples with identical (series, timestamp) unless
    -dedup.minScrapeInterval is set, output series must be wiped before a
    full re-write to avoid duplicate points.
    """
    resp = _SESSION.post(
        f"{VM_URL}/api/v1/admin/tsdb/delete_series",
        params={"match[]": match},
        timeout=_HTTP_TIMEOUT,
    )
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"VM delete_series failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )


def load_rr_intervals(min_ts_ms: int | None = None, max_ts_ms: int | None = None):
    """Load rr_interval_ms globally ordered by timestamp.

    Returns (ts_ms, rr) as numpy arrays. RR intervals are now stored as a
    single series with a unique, physically-reconstructed per-beat
    timestamp (see gadgetbridge_migrate.py), so the device ordering is the
    plain ascending-timestamp order — no seq merge required. VM may split a
    large series across several export blocks, so the concatenation is
    stable-sorted by timestamp to be safe. Empty arrays when the range
    holds no samples.
    """
    import numpy as np

    ts_chunks, rr_chunks = [], []
    for _labels, timestamps, values in export(
        "rr_interval_ms", start_ms=min_ts_ms, end_ms=max_ts_ms
    ):
        if not timestamps:
            continue
        ts_chunks.append(np.asarray(timestamps, dtype=np.int64))
        rr_chunks.append(np.asarray(values, dtype=np.float64))

    if not ts_chunks:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.float64)

    ts = np.concatenate(ts_chunks)
    rr = np.concatenate(rr_chunks)
    order = np.argsort(ts, kind="stable")
    return ts[order], rr[order]


def export(match: str, start_ms: int | None = None, end_ms: int | None = None):
    """Stream series from /api/v1/export.

    Yields (labels_dict, timestamps_ms_list, values_list) per series. The
    series ordering and intra-series sample ordering follow VM's export
    (ascending timestamps); callers needing a global order across series
    must merge/sort themselves.
    """
    params = {"match[]": match}
    if start_ms is not None:
        params["start"] = str(int(start_ms))
    if end_ms is not None:
        params["end"] = str(int(end_ms))
    with _SESSION.get(
        f"{VM_URL}/api/v1/export",
        params=params,
        stream=True,
        timeout=_HTTP_TIMEOUT,
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(chunk_size=_EXPORT_CHUNK):
            if not line:
                continue
            obj = orjson.loads(line)
            metric = obj.get("metric", {})
            labels = {k: v for k, v in metric.items() if k != "__name__"}
            yield labels, obj.get("timestamps", []), obj.get("values", [])
