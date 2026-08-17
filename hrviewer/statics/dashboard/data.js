/* Generic data-fetch / query layer: talks to the Arrow-over-HTTP `/api/query`
 * endpoint, shares identical in-flight/completed query results across
 * panels, and offers a couple of small array transforms (XY conversion,
 * moving average, derived/"transformed" series). Fully parametrized --
 * range and max_points are passed in by callers -- so this module holds no
 * reference to the dashboard's live time window and has no dependency on
 * controls.js. */
"use strict";

const ARROW_MIME = "application/vnd.apache.arrow.stream";

async function fetchTable(body) {
  const res = await fetch("api/query", {
    method: "POST",
    headers: { "Content-Type": "application/json", "Accept": ARROW_MIME },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error("HTTP " + res.status);
  const buf = await res.arrayBuffer();
  return Arrow.tableFromIPC(new Uint8Array(buf));
}

/* Shared query cache: identical queries are fetched once, with results
 * shared across panels. Cleared explicitly (see clearQueryCache) whenever
 * the global range/resolution changes. */
const queryCache = new Map();
export function clearQueryCache() { queryCache.clear(); }
export function cachedFetchTable(body) {
  const key = JSON.stringify(body);
  let p = queryCache.get(key);
  if (!p) {
    p = fetchTable(body).catch((e) => { queryCache.delete(key); throw e; });
    queryCache.set(key, p);
  }
  return p;
}

export function toXY(table, valueName) {
  const tsCol = table.getChild("ts");
  const vCol = table.getChild(valueName);
  const n = table.numRows, out = new Array(n);
  for (let i = 0; i < n; i++) {
    const v = vCol.get(i);
    out[i] = [Number(tsCol.get(i)), v === null ? null : Number(v)];
  }
  return out;
}

/* Centered moving average over a fixed window, ignoring nulls. */
export function movingAverage(xy, size) {
  const n = xy.length, half = Math.floor(size / 2), out = new Array(n);
  for (let i = 0; i < n; i++) {
    let sum = 0, cnt = 0;
    for (let j = i - half; j <= i + half; j++) {
      if (j < 0 || j >= n) continue;
      const v = xy[j][1];
      if (v != null) { sum += v; cnt++; }
    }
    out[i] = [xy[i][0], cnt ? sum / cnt : null];
  }
  return out;
}

/* Series resolution: raw (simple query) or transformed (derived from inputs).
 * Transformed inputs are aligned to first input's timestamps.
 * `range` = { start, end } in epoch ms; `maxPoints` = server-side point cap. */
function seriesQueryBody(q, range, maxPoints) {
  return {
    kind: "series", segment: q.segment, metric: q.metric,
    agg: q.agg || "avg", start: range.start, end: range.end,
    max_points: maxPoints,
  };
}
function applyTransform(fn, keys, arrays) {
  const n = arrays.length;
  if (!n) return [];
  const base = arrays[0];
  const ptr = new Array(n).fill(0), cur = new Array(n).fill(null);
  const out = new Array(base.length);
  for (let bi = 0; bi < base.length; bi++) {
    const ts = base[bi][0];
    for (let k = 0; k < n; k++) {
      const a = arrays[k];
      while (ptr[k] < a.length && a[ptr[k]][0] <= ts) { cur[k] = a[ptr[k]][1]; ptr[k]++; }
    }
    let v = null;
    if (cur.every((x) => x != null)) {
      const row = {};
      for (let k = 0; k < n; k++) row[keys[k]] = cur[k];
      const r = Number(fn(row));
      v = isFinite(r) ? r : null;
    }
    out[bi] = [ts, v];
  }
  return out;
}
/* Fetch metric; missing data yields empty series (not cached, so retried later). */
async function fetchSeriesXY(q, range, maxPoints) {
  try {
    return toXY(await cachedFetchTable(seriesQueryBody(q, range, maxPoints)), "value");
  } catch (e) {
    console.warn("query failed (treated as empty series):",
      q.segment, q.metric, (e && e.message) || e);
    return [];
  }
}
export async function seriesData(sc, range, maxPoints) {
  if (sc.transform && sc.inputs) {
    const keys = sc.inputs.map((q) => q.key);
    const arrays = await Promise.all(sc.inputs.map((q) => fetchSeriesXY(q, range, maxPoints)));
    return applyTransform(sc.transform, keys, arrays);
  }
  return fetchSeriesXY(sc, range, maxPoints);
}

/* ---- "flag"/"tiles" panel value reduction -----------------------------
 * Reduces a fetched series to its most recent (last non-null) value. */
export function latestValue(xy) {
  for (let i = xy.length - 1; i >= 0; i--) if (xy[i][1] != null) return xy[i][1];
  return null;
}
