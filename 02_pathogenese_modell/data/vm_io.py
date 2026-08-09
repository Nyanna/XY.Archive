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
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        timeout=_HTTP_TIMEOUT, verify=False
    )
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"VM import failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )


# --- InfluxDB Line Protocol write path --------------------------------
# Used by VMWriter instead of /api/v1/import (JSON): building line-protocol
# text is plain string formatting (no per-sample Python object graph like
# orjson.dumps of nested dict/list), and VM's line-protocol parser is a
# first-class, actively maintained ingestion path (not a JSON round trip).
# A field named exactly "value" is mapped by VM directly to the metric name
# (no "<measurement>_value" suffix), so plain "measurement[,tags] value=X ts"
# round-trips to the same series shape the JSON path produced.

_LP_ESCAPE_COMMA_SPACE = str.maketrans({
    "\\": "\\\\", ",": "\\,", " ": "\\ ",
})
_LP_ESCAPE_KEY = str.maketrans({
    "\\": "\\\\", ",": "\\,", " ": "\\ ", "=": "\\=",
})


def _lp_measurement(name: str) -> str:
    return name.translate(_LP_ESCAPE_COMMA_SPACE)


def _lp_tag_part(k: str, v: str) -> str:
    return f"{k.translate(_LP_ESCAPE_KEY)}={str(v).translate(_LP_ESCAPE_KEY)}"


def _post_write(payload: bytes) -> None:
    resp = _SESSION.post(
        f"{VM_URL}/write",
        params={"precision": "ms"},
        data=payload,
        headers={"Content-Type": "text/plain; charset=utf-8"},
        timeout=_HTTP_TIMEOUT, verify=False
    )
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"VM influx write failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )


class VMWriter:
    """Accumulates samples per series and flushes as InfluxDB Line Protocol
    to /write (precision=ms).

    Usage:
        w = VMWriter()
        w.add("heart_rate", {"source": "generic"}, ts_ms, 78)
        ...
        w.flush()
    """

    def __init__(self, batch_samples: int = DEFAULT_BATCH_SAMPLES):
        self.batch_samples = batch_samples
        self._buf: dict = {}          # series_key -> {"measurement":..,"values":..,"timestamps":..}
        self._pending = 0             # samples buffered but not yet POSTed
        self.total = 0                # samples POSTed over the writer's lifetime

    def add(self, name: str, labels: dict, ts_ms: int, value: float) -> None:
        key = (name, tuple(sorted(labels.items())))
        entry = self._buf.get(key)
        if entry is None:
            tag_str = "".join(
                f",{_lp_tag_part(k, v)}" for k, v in sorted(labels.items())
            )
            entry = {
                "measurement": _lp_measurement(name) + tag_str,
                "values": [], "timestamps": [],
            }
            self._buf[key] = entry
        entry["values"].append(value)
        entry["timestamps"].append(int(ts_ms))
        self._pending += 1
        if self._pending >= self.batch_samples:
            self.flush()

    def flush(self) -> None:
        if not self._buf:
            return
        lines = []
        for entry in self._buf.values():
            prefix = entry["measurement"]
            for ts, val in zip(entry["timestamps"], entry["values"]):
                lines.append(f"{prefix} value={val!r} {ts}")
        payload = ("\n".join(lines) + "\n").encode("utf-8")
        _post_write(payload)
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
            timeout=_HTTP_TIMEOUT, verify=False
        )
        return resp.status_code == 200
    except requests.RequestException:
        raise RuntimeError(
            f"force_flush unavailable"
        )


def _stored_selector(selector: str) -> str:
    """Map a logical metric-name selector to its actual VM series name.

    VMWriter writes every sample as InfluxDB Line Protocol with a field
    literally named "value". Without -influxSkipSingleField (not set on
    this deployment), VM's influx endpoint unconditionally names the
    resulting series "<measurement>_<field>" -- so every metric written
    through this module is physically stored as "<name>_value", never
    "<name>". All read-side lookups therefore need this suffix inserted
    right after the metric name, before any label-matcher braces (e.g.
    "heart_rate{source=\"generic\"}" -> "heart_rate_value{source=\"generic\"}").
    """
    brace = selector.find("{")
    if brace == -1:
        return f"{selector}_value"
    return f"{selector[:brace]}_value{selector[brace:]}"


def latest_timestamp_ms(selector: str, lookback: str = "3650d") -> int | None:
    """Newest sample timestamp (ms) matching a PromQL selector, or None.

    Implemented via MetricsQL tlast_over_time(<selector>[lookback]), which
    yields the timestamp (seconds) of each series' last raw sample; the max
    across the returned per-series scalars is the watermark.
    """
    selector = _stored_selector(selector)
    query = f"tlast_over_time({selector}[{lookback}])"
    resp = _SESSION.get(
        f"{VM_URL}/api/v1/query",
        params={"query": query, "time": str(int(time.time()))},
        timeout=_HTTP_TIMEOUT, verify=False
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
        params={"match[]": _stored_selector(match)},
        timeout=_HTTP_TIMEOUT, verify=False
    )
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"VM delete_series failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )


def export_csv_series(match: str, start_ms: int | None = None, end_ms: int | None = None):
    """Export one unlabeled metric as (timestamps_ms, values) via /export/csv.

    Only meaningful for a metric with no relevant labels (rr_interval_ms has
    none): the requested CSV columns are just __timestamp__/__value__, so
    labels are not represented. This avoids the JSON round trip of
    /api/v1/export (VM formatting every raw float as JSON text, client
    orjson-decoding + boxing every value back into a Python object) --
    CSV is parsed straight into a numpy array in C via np.loadtxt.

    VM always emits one header line (the echoed `format` string) before the
    data rows; that line is skipped. Returns empty int64/float64 arrays if
    the range holds no samples.
    """
    import io
    import numpy as np

    params = {
        "match[]": _stored_selector(match),
        "format": "__timestamp__:unix_ms,__value__",
    }
    if start_ms is not None:
        params["start"] = str(int(start_ms))
    if end_ms is not None:
        params["end"] = str(int(end_ms))

    resp = _SESSION.get(
        f"{VM_URL}/api/v1/export/csv", params=params, timeout=_HTTP_TIMEOUT, verify=False
    )
    resp.raise_for_status()

    data = np.loadtxt(
        io.BytesIO(resp.content), delimiter=",", skiprows=1, dtype=np.float64,
    )
    if data.size == 0:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.float64)
    data = data.reshape(-1, 2)
    return data[:, 0].astype(np.int64), data[:, 1]


def load_rr_intervals(min_ts_ms: int | None = None, max_ts_ms: int | None = None):
    """Load rr_interval_ms globally ordered by timestamp.

    Returns (ts_ms, rr) as numpy arrays. RR intervals are now stored as a
    single series with a unique, physically-reconstructed per-beat
    timestamp (see gadgetbridge_migrate.py), so the device ordering is the
    plain ascending-timestamp order — no seq merge required. Uses the CSV
    export path (see export_csv_series) since this is the highest-volume
    read in the pipeline. Sorted by timestamp to be safe. Empty arrays when
    the range holds no samples.
    """
    import numpy as np

    ts, rr = export_csv_series("rr_interval_ms", start_ms=min_ts_ms, end_ms=max_ts_ms)
    if ts.size == 0:
        return ts, rr
    order = np.argsort(ts, kind="stable")
    return ts[order], rr[order]


def export(match: str, start_ms: int | None = None, end_ms: int | None = None):
    """Stream series from /api/v1/export.

    Yields (labels_dict, timestamps_ms_list, values_list) per series. The
    series ordering and intra-series sample ordering follow VM's export
    (ascending timestamps); callers needing a global order across series
    must merge/sort themselves.
    """
    params = {"match[]": _stored_selector(match)}
    if start_ms is not None:
        params["start"] = str(int(start_ms))
    if end_ms is not None:
        params["end"] = str(int(end_ms))
    with _SESSION.get(
        f"{VM_URL}/api/v1/export",
        params=params,
        stream=True,
        timeout=_HTTP_TIMEOUT, verify=False
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(chunk_size=_EXPORT_CHUNK):
            if not line:
                continue
            obj = orjson.loads(line)
            metric = obj.get("metric", {})
            labels = {k: v for k, v in metric.items() if k != "__name__"}
            yield labels, obj.get("timestamps", []), obj.get("values", [])
