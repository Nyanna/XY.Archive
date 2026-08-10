#!/usr/bin/env python3
"""
Victoria Metrics I/O helper.

Thin client around the VM HTTP API (write: Gadgetbridge migration,
read: aggregation scripts). Timestamps are ms since epoch, values float64.

All read/write paths are chunk-wise: streamed HTTP (stream=True,
bounded iter_lines chunks), no resp.content full-body buffering, no
unbounded client-side accumulation beyond one write batch or read chunk.
"""

import os
import re
import time

import orjson
import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VM_URL = os.environ.get("VM_URL", "http://localhost:8428").rstrip("/")
VM_USER = os.environ.get("VM_USER")
VM_PASSWORD = os.environ.get("VM_PASSWORD")
VM_TOKEN = os.environ.get("VM_TOKEN")

DEFAULT_BATCH_SAMPLES = 50_000

_HTTP_TIMEOUT = (60, 600)  # (connect, read) seconds
_EXPORT_CHUNK = 1 << 20    # /export read chunk size, bytes

_WRITE_RETRY = Retry(
    total=5,
    connect=5,
    read=5,
    status=5,
    backoff_factor=2.0,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset({"POST"}),
    raise_on_status=False,
)


def _make_session(retries=None, pool_size: int = 1) -> requests.Session:
    s = requests.Session()
    if VM_TOKEN:
        s.headers["Authorization"] = f"Bearer {VM_TOKEN}"
    elif VM_USER is not None:
        s.auth = (VM_USER, VM_PASSWORD or "")
    adapter = HTTPAdapter(
        pool_connections=pool_size,
        pool_maxsize=pool_size,
        max_retries=retries or 0,
    )
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


_SESSION = _make_session()
_WRITE_SESSION = _make_session(retries=_WRITE_RETRY)
_WRITE_HEADERS_EXTRA = {"Connection": "close"}  # fresh socket per write, works with _WRITE_RETRY


def _raise_for_status(resp: requests.Response, what: str) -> None:
    """Like resp.raise_for_status(), but includes the response body."""
    if resp.ok:
        return
    body = resp.text[:500]
    raise requests.exceptions.HTTPError(
        f"{what} failed: HTTP {resp.status_code} for {resp.url!r}: {body}",
        response=resp,
    )


def import_url() -> str:
    return f"{VM_URL}/api/v1/import"


def _post_import(payload: bytes) -> None:
    resp = _WRITE_SESSION.post(
        import_url(),
        data=payload,
        headers={"Content-Type": "application/x-ndjson", **_WRITE_HEADERS_EXTRA},
        timeout=_HTTP_TIMEOUT, verify=False
    )
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"VM import failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )


# InfluxDB Line Protocol write path (VMWriter -> /write). A field named
# "value" is mapped by VM directly to the metric name, so a plain
# "measurement[,tags] value=X ts" line round-trips to the same series
# shape the JSON /api/v1/import path would produce.

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
    resp = _WRITE_SESSION.post(
        f"{VM_URL}/write",
        params={"precision": "ms"},
        data=payload,
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            **_WRITE_HEADERS_EXTRA,
        },
        timeout=_HTTP_TIMEOUT, verify=False
    )
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"VM influx write failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )


class VMWriter:
    """Buffers samples per series, flushes as Line Protocol to /write.

        w = VMWriter()
        w.add("heart_rate", {"source": "generic"}, ts_ms, 78)
        w.flush()
    """

    def __init__(self, batch_samples: int = DEFAULT_BATCH_SAMPLES):
        self.batch_samples = batch_samples
        self._buf: dict = {}
        self._pending = 0
        self.total = 0

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
    """Best-effort: make freshly imported samples immediately queryable."""
    try:
        resp = _WRITE_SESSION.get(
            f"{VM_URL}/internal/force_flush",
            headers=_WRITE_HEADERS_EXTRA,
            timeout=_HTTP_TIMEOUT, verify=False
        )
        return resp.status_code == 200
    except requests.RequestException:
        raise RuntimeError("force_flush unavailable")


def _stored_selector(selector: str) -> str:
    """Map a logical metric name to its VM series name ("<name>_value").

    VMWriter's Line Protocol field is literally named "value"; without
    -influxSkipSingleField VM stores it as "<measurement>_value".
    """
    brace = selector.find("{")
    if brace == -1:
        return f"{selector}_value"
    return f"{selector[:brace]}_value{selector[brace:]}"


_DURATION_RE = re.compile(r"(\d+(?:\.\d+)?)(ms|s|m|h|d|w|y)")
_DURATION_UNIT_SECONDS = {
    "ms": 0.001, "s": 1, "m": 60, "h": 3600,
    "d": 86400, "w": 7 * 86400, "y": 365 * 86400,
}

_WATERMARK_MIN_WINDOW_S = 300      # first probe window for latest_timestamp_ms
_WATERMARK_GROWTH_FACTOR = 8       # widen factor per empty probe, up to the cap
_WATERMARK_MAX_WINDOW_S = 5 * 86400  # hard cap on any single probe's window


def _parse_duration_seconds(duration: str) -> float:
    """Parse a MetricsQL-style duration ("3650d", "1h30m", ...) to seconds."""
    total = sum(
        float(value) * _DURATION_UNIT_SECONDS[unit]
        for value, unit in _DURATION_RE.findall(duration)
    )
    if total <= 0:
        raise ValueError(f"cannot parse duration: {duration!r}")
    return total


def _tlast_over_time(selector: str, window_s: float, eval_ts: int) -> float | None:
    """One tlast_over_time probe; returns the max last-sample-ts in seconds."""
    query = f"tlast_over_time({selector}[{int(window_s)}s])"
    resp = _SESSION.get(
        f"{VM_URL}/api/v1/query",
        params={"query": query, "time": str(eval_ts)},
        timeout=_HTTP_TIMEOUT, verify=False
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise RuntimeError(f"VM query failed: {data}")
    results = data["data"]["result"]
    if not results:
        return None
    return max(float(r["value"][1]) for r in results)


def latest_timestamp_ms(selector: str, lookback: str = "3650d") -> int | None:
    """Newest sample timestamp (ms) matching a PromQL selector, or None.

    tlast_over_time has to read every raw sample in its window (no index
    jumps straight to the last one), so querying `lookback` in one shot
    OOMs VM on high-frequency series. Every probe's window is therefore
    capped at _WATERMARK_MAX_WINDOW_S: first grow it (anchored at "now")
    from _WATERMARK_MIN_WINDOW_S up to that cap, then keep sliding a
    cap-sized window back through time until `lookback` is covered or a
    sample is found.
    """
    selector = _stored_selector(selector)
    max_window_s = _parse_duration_seconds(lookback)
    now = int(time.time())
    probe_cap = min(_WATERMARK_MAX_WINDOW_S, max_window_s)

    # Phase 1: grow the window, anchored at "now", up to probe_cap.
    end = now
    covered_s = 0.0
    window_s = min(_WATERMARK_MIN_WINDOW_S, probe_cap)
    while True:
        max_sec = _tlast_over_time(selector, window_s, end)
        if max_sec is not None:
            return int(round(max_sec * 1000))
        covered_s = window_s
        if covered_s >= probe_cap:
            break
        window_s = min(window_s * _WATERMARK_GROWTH_FACTOR, probe_cap)

    # Phase 2: slide a probe_cap-sized window backward until lookback is covered.
    end = now - covered_s
    while covered_s < max_window_s:
        window_s = min(probe_cap, max_window_s - covered_s)
        max_sec = _tlast_over_time(selector, window_s, end)
        if max_sec is not None:
            return int(round(max_sec * 1000))
        end -= window_s
        covered_s += window_s
    return None


def delete_series(match: str) -> None:
    """Delete every series matching a selector (whole series, no time range)."""
    resp = _WRITE_SESSION.post(
        f"{VM_URL}/api/v1/admin/tsdb/delete_series",
        params={"match[]": _stored_selector(match)},
        headers=_WRITE_HEADERS_EXTRA,
        timeout=_HTTP_TIMEOUT, verify=False
    )
    if resp.status_code not in (200, 204):
        raise RuntimeError(
            f"VM delete_series failed: HTTP {resp.status_code}: {resp.text[:500]}"
        )


DEFAULT_CSV_CHUNK_ROWS = 200_000

_MAX_SAMPLES_MARKER = "-search.maxSamplesPerQuery"


def _export_csv_range_rows(match: str, start_ms: int, end_ms: int):
    """Yield (ts_ms, value) for one /export/csv call over [start_ms, end_ms).

    On VM's "cannot select more than -search.maxSamplesPerQuery" 400,
    bisect the range and recurse -- the exact split point doesn't matter,
    only that each half eventually fits the server-side limit.
    """
    params = {
        "match[]": _stored_selector(match),
        "format": "__timestamp__:unix_ms,__value__",
        "start": str(start_ms),
        "end": str(end_ms),
    }
    with _SESSION.get(
        f"{VM_URL}/api/v1/export/csv", params=params,
        stream=True, timeout=_HTTP_TIMEOUT, verify=False,
    ) as resp:
        if not resp.ok:
            body = resp.text
            mid = (start_ms + end_ms) // 2
            if _MAX_SAMPLES_MARKER not in body or mid <= start_ms:
                _raise_for_status(resp, "VM export/csv")
            split = True
        else:
            split = False
            header_skipped = False
            for line in resp.iter_lines(chunk_size=_EXPORT_CHUNK):
                if not line:
                    continue
                if not header_skipped:
                    header_skipped = True  # VM echoes the `format` string as header
                    continue
                ts_str, val_str = line.split(b",", 1)
                yield int(ts_str), float(val_str)

    if split:
        mid = (start_ms + end_ms) // 2
        yield from _export_csv_range_rows(match, start_ms, mid)
        yield from _export_csv_range_rows(match, mid, end_ms)


def export_csv_series_chunks(
    match: str,
    start_ms: int | None = None,
    end_ms: int | None = None,
    chunk_rows: int = DEFAULT_CSV_CHUNK_ROWS,
):
    """Stream one unlabeled metric as (ts_ms, values) numpy chunks via /export/csv.

    Only meaningful for a metric with no relevant labels (rr_interval_ms):
    the requested columns are __timestamp__/__value__ only. Chunks are
    yielded in the ascending timestamp order VM streams them in. start_ms/
    end_ms default to epoch/now so the range is always bisectable (see
    _export_csv_range_rows).
    """
    import numpy as np

    resolved_start = 0 if start_ms is None else int(start_ms)
    resolved_end = int(time.time() * 1000) if end_ms is None else int(end_ms)

    ts_buf: list = []
    val_buf: list = []
    for ts, val in _export_csv_range_rows(match, resolved_start, resolved_end):
        ts_buf.append(ts)
        val_buf.append(val)
        if len(ts_buf) >= chunk_rows:
            yield (
                np.array(ts_buf, dtype=np.int64),
                np.array(val_buf, dtype=np.float64),
            )
            ts_buf = []
            val_buf = []
    if ts_buf:
        yield (
            np.array(ts_buf, dtype=np.int64),
            np.array(val_buf, dtype=np.float64),
        )


def export_csv_series(match: str, start_ms: int | None = None, end_ms: int | None = None):
    """Full-series convenience wrapper around export_csv_series_chunks()."""
    import numpy as np

    chunks = list(export_csv_series_chunks(match, start_ms=start_ms, end_ms=end_ms))
    if not chunks:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.float64)
    ts = np.concatenate([c[0] for c in chunks])
    vals = np.concatenate([c[1] for c in chunks])
    return ts, vals


def load_rr_intervals_chunks(
    min_ts_ms: int | None = None,
    max_ts_ms: int | None = None,
    chunk_rows: int = DEFAULT_CSV_CHUNK_ROWS,
):
    """Stream rr_interval_ms as (ts_ms, rr) numpy chunks, in device order.

    rr_interval_ms has unique, physically-reconstructed per-beat
    timestamps (gadgetbridge_migrate.py), so VM's ascending-timestamp
    export order already reproduces device order.
    """
    yield from export_csv_series_chunks(
        "rr_interval_ms", start_ms=min_ts_ms, end_ms=max_ts_ms, chunk_rows=chunk_rows,
    )


def load_rr_intervals(min_ts_ms: int | None = None, max_ts_ms: int | None = None):
    """Full-series convenience wrapper around load_rr_intervals_chunks()."""
    import numpy as np

    chunks = list(load_rr_intervals_chunks(min_ts_ms=min_ts_ms, max_ts_ms=max_ts_ms))
    if not chunks:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.float64)
    ts = np.concatenate([c[0] for c in chunks])
    rr = np.concatenate([c[1] for c in chunks])
    if ts.size and not np.all(ts[:-1] <= ts[1:]):
        order = np.argsort(ts, kind="stable")
        ts = ts[order]
        rr = rr[order]
    return ts, rr


def export(match: str, start_ms: int | None = None, end_ms: int | None = None):
    """Stream series from /api/v1/export.

    Yields (labels_dict, timestamps_ms_list, values_list) per NDJSON line.
    reduce_mem_usage=1 makes VM split long series into multiple smaller
    lines instead of one giant line per series; ordering is then only
    ascending *within* a chunk, callers needing a global order must
    merge/sort themselves.
    """
    params = {"match[]": _stored_selector(match), "reduce_mem_usage": "1"}
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
        if not resp.ok:
            _ = resp.content  # read body now, stream=True defers it
            _raise_for_status(resp, "VM export")
        for line in resp.iter_lines(chunk_size=_EXPORT_CHUNK):
            if not line:
                continue
            obj = orjson.loads(line)
            metric = obj.get("metric", {})
            labels = {k: v for k, v in metric.items() if k != "__name__"}
            yield labels, obj.get("timestamps", []), obj.get("values", [])
