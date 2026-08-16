/* Generic ECharts dashboard renderer, driven entirely by a `window.DASHBOARD`
 * config (see dashboard.config.js). Not tied to any specific metrics or
 * domain -- a new dashboard only needs its own config file, selected via
 * dashboard.html's `?config=` URL parameter.
 *
 * Features: synced zoom/hover cursor across panels (by axis value, not data
 * index, plus late-join replay), a time selector with quick ranges + shift
 * buttons, lazy (visibility-based) panel loading, thresholds, dual Y-axes,
 * a toggleable legend, collapsible rows, a tab layout and labelled, static
 * time annotations shown across all synced panels.
 */
(function () {
  "use strict";

  const ARROW_MIME = "application/vnd.apache.arrow.stream";
  const AXIS = "#656d76", GRID = "#eaecef", BORDER = "#d0d7de";

  const boardEl = document.getElementById("board");
  const statusEl = document.getElementById("status");
  const quickSel = document.getElementById("quickRange");
  const fromIn = document.getElementById("fromInput");
  const toIn = document.getElementById("toInput");
  const maxPointsIn = document.getElementById("maxPointsInput");
  const autoRefreshIn = document.getElementById("autoRefresh");

  /* ---- global time window state --------------------------------------- */
  let fromMs, toMs;
  let zoomWindow = null;          // {s,e} in ms -- current synced zoom, or null
  const panels = [];             // all Panel instances
  let pending = 0;
  let syncing = false;           // re-entrancy guard for zoom broadcasting

  function setStatus(msg) { statusEl.textContent = msg || ""; }
  function bump(d) {
    pending = Math.max(0, pending + d);
    setStatus(pending > 0 ? "Loading … (" + pending + ")" : "Ready");
  }

  /* ---- cross-panel sync BY AXIS VALUE ----------------------------------
   * `echarts.connect` links by *data index*, which misaligns panels whose
   * series have different point counts. We sync zoom/hover manually instead,
   * by time value. Panels of type "daily" (own X-axis) are excluded. */
  const syncable = (p) => p.chart && p.cfg.type !== "daily";

  function broadcastShowAtValue(t) {
    panels.forEach((p) => {
      if (!syncable(p) || !p.loaded) return;
      const x = p.chart.convertToPixel({ xAxisIndex: 0 }, t);
      if (x == null || isNaN(x)) return;
      p.chart.dispatchAction({ type: "showTip", x, y: p.chart.getHeight() / 2 });
    });
  }
  function broadcastHide() {
    panels.forEach((p) => { if (syncable(p)) p.chart.dispatchAction({ type: "hideTip" }); });
  }
  function broadcastZoom(source) {
    if (!zoomWindow) return;
    syncing = true;
    panels.forEach((p) => {
      if (syncable(p) && p.chart !== source) {
        p.chart.dispatchAction({
          type: "dataZoom", startValue: zoomWindow.s, endValue: zoomWindow.e,
        });
      }
    });
    syncing = false;
  }

  /* ---- datetime-local <-> epoch ms (local time) ----------------------- */
  const pad = (n) => String(n).padStart(2, "0");
  function fmtLocal(ms) {
    const d = new Date(ms);
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()) +
      "T" + pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds());
  }
  const parseLocal = (s) => new Date(s).getTime();

  /* ---- fixed per-panel query window -------------------------------------
   * Panels that aggregate by calendar day need their own, wider window,
   * independent of the (possibly short) global range. Opt in via `cfg.range`:
   *   { days: N }          -> rolling window [now - N days, now]
   *   { from: X, to: Y }   -> absolute bounds; X/Y: "now" | epoch ms | ISO
   * Panels without `cfg.range` use the global [fromMs, toMs]. */
  function resolveTime(v, dflt) {
    if (v == null) return dflt;
    if (v === "now") return Date.now();
    if (typeof v === "number") return v;
    return new Date(v).getTime();
  }
  function panelRange(cfg) {
    const r = cfg.range;
    if (!r) return { start: fromMs, end: toMs };
    const end = resolveTime(r.to, Date.now());
    const start = r.days != null
      ? end - r.days * 86400000
      : resolveTime(r.from, end - 14 * 86400000);
    return { start, end };
  }

  /* ---- shared plot geometry & axis helpers ---------------------------- */
  const GRID_TOP = 16, GRID_BOTTOM = 44, GRID_BOTTOM_NOAXIS = 10;

  /* Bottom grid margin: only the one panel per group that actually renders
   * the shared x-axis tick labels (`cfg.timeAxis`) needs the full margin;
   * every other panel would otherwise carry that space as dead padding
   * (the legend no longer lives down there -- it floats over the plot). */
  const gridBottom = (cfg) => (cfg.timeAxis ? GRID_BOTTOM : GRID_BOTTOM_NOAXIS);

  /* High-resolution time-axis tick labels: HH:MM (with :SS when relevant),
   * and a bold day marker on midnight boundaries. */
  function axisTimeFormatter(val) {
    const d = new Date(val);
    const H = pad(d.getHours()), M = pad(d.getMinutes()), S = pad(d.getSeconds());
    if (H === "00" && M === "00" && S === "00")
      return "{d|" + pad(d.getDate()) + "." + pad(d.getMonth() + 1) + ".}";
    return S !== "00" ? H + ":" + M + ":" + S : H + ":" + M;
  }

  /* Tooltip value formatter: show at most 2 decimals for non-zero values
   * (integers and 0 stay unchanged, e.g. 0, 72, 72.53). */
  function fmtTip(v) {
    if (v == null || v === "") return "";
    const n = Number(v);
    if (!isFinite(n)) return String(v);
    if (n === 0) return "0";
    return String(Math.round(n * 100) / 100);
  }

  /* Abbreviate large axis numbers, e.g. 1000 -> "1k", 2_500_000 -> "2.5M". */
  const trimNum = (x) => String(Math.round(x * 100) / 100);
  function abbrevNum(v) {
    const a = Math.abs(v);
    if (a >= 1e9) return trimNum(v / 1e9) + "G";
    if (a >= 1e6) return trimNum(v / 1e6) + "M";
    if (a >= 1e3) return trimNum(v / 1e3) + "k";
    return trimNum(v);
  }

  /* Shared time X-axis; tick labels only render where `cfg.timeAxis` is set,
   * since every timeseries/state panel is pinned to the same window. */
  function timeXAxis(cfg) {
    const show = !!cfg.timeAxis;
    return {
      type: "time", min: fromMs, max: toMs,
      axisLine: { lineStyle: { color: BORDER } },
      axisTick: { show },
      splitNumber: 12,
      axisLabel: show ? {
        color: AXIS, hideOverlap: true, showMinLabel: false, showMaxLabel: false,
        formatter: axisTimeFormatter,
        rich: { d: { fontWeight: "bold", color: AXIS } },
      } : { show: false },
    };
  }

  /* Inside-only zoom: the slider overview bar is intentionally omitted; wheel
   * zoom stays, drag-pan is handled by our own right-drag interaction. */
  const insideZoom = () => [{
    type: "inside", throttle: 60,
    zoomOnMouseWheel: true, moveOnMouseMove: false, moveOnMouseWheel: false,
  }];

  function syncInputs() {
    fromIn.value = fmtLocal(fromMs);
    toIn.value = fmtLocal(toMs);
  }

  /* Global "max_points" override for all panels; empty leaves each query's default untouched. */
  function maxPointsOverride(dflt) {
    const v = parseInt(maxPointsIn.value, 10);
    return Number.isFinite(v) && v > 0 ? v : dflt;
  }

  async function fetchTable(body) {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": ARROW_MIME },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const buf = await res.arrayBuffer();
    return Arrow.tableFromIPC(new Uint8Array(buf));
  }

  /* Shared query cache: identical queries are fetched once, with results
   * shared across panels. Cache is cleared when range/resolution changes. */
  const queryCache = new Map();
  function cachedFetchTable(body) {
    const key = JSON.stringify(body);
    let p = queryCache.get(key);
    if (!p) {
      p = fetchTable(body).catch((e) => { queryCache.delete(key); throw e; });
      queryCache.set(key, p);
    }
    return p;
  }
  function toXY(table, valueName) {
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
  function movingAverage(xy, size) {
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
   * Transformed inputs are aligned to first input's timestamps. */
  function seriesQueryBody(q) {
    return {
      kind: "series", segment: q.segment, metric: q.metric,
      agg: q.agg || "avg", start: fromMs, end: toMs,
      max_points: maxPointsOverride(3000),
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
  async function fetchSeriesXY(q) {
    try {
      return toXY(await cachedFetchTable(seriesQueryBody(q)), "value");
    } catch (e) {
      console.warn("query failed (treated as empty series):",
        q.segment, q.metric, (e && e.message) || e);
      return [];
    }
  }
  async function seriesData(sc) {
    if (sc.transform && sc.inputs) {
      const keys = sc.inputs.map((q) => q.key);
      const arrays = await Promise.all(sc.inputs.map(fetchSeriesXY));
      return applyTransform(sc.transform, keys, arrays);
    }
    return fetchSeriesXY(sc);
  }

  /* ---- "flag" panel: momentary binary indicator ------------------------
   * A flag panel does not plot a line. It reduces each series to its most
   * recent (last non-null) value and renders it as a labelled badge. The
   * mapping value -> { text, color, fg } is domain-specific and supplied by
   * the panel config as `cfg.flag.state(value)`, keeping the renderer generic
   * (e.g. a window contact "open/closed", or a computed "ventilate now" flag
   * derived from the latest sample of a transformed series). */
  function latestValue(xy) {
    for (let i = xy.length - 1; i >= 0; i--) if (xy[i][1] != null) return xy[i][1];
    return null;
  }

  /* Small helper context handed to "tiles" panel addons (see the Panel class
   * below): lets a dashboard-specific addon -- e.g. a live WebSocket toggle
   * -- reuse the generic query engine for an occasional "latest value" read
   * without the renderer having to know anything about the addon itself. */
  const TILE_CTX = {
    fetchLatest: async (sc) => latestValue(await seriesData(sc)),
    fmtTip,
  };

  /* Deterministic, maintenance-free per-tile colour: derived from a cheap
   * hash of the tile's label, so e.g. "Büro" always gets the same tint on
   * every load without any hand-maintained label -> colour table. Purely a
   * recognition aid (build muscle memory for "my tile lives over there, the
   * reddish one") -- not meant to encode any value/state.
   *   - hue: one hash component, ROUNDED onto a fixed grid of steps (a
   *     discrete "spectrum") so any two tiles land at least one step apart
   *     -- no near-identical, hard-to-tell-apart hues;
   *   - saturation/lightness: two further, independent hash components,
   *     varied continuously (fairly strong/saturated) so tiles that happen
   *     to share a hue step still look distinguishable. */
  function labelHash(label) {
    let h = 5381;
    const s = String(label || "");
    for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0; // djb2
    return h >>> 0;
  }
  const HUE_STEPS = 18;                    // 360°/18 = 20° apart -> clearly distinct hues
  function tileAccent(label) {
    const h = labelHash(label);
    const hue = (h % HUE_STEPS) * (360 / HUE_STEPS);          // rounded onto the hue grid
    const sat = 58 + (Math.floor(h / HUE_STEPS) % 25);        // 58-82%
    const lit = 68 + (Math.floor(h / (HUE_STEPS * 25)) % 14); // 68-81%
    return {
      background: "linear-gradient(135deg, hsl(" + hue + " " + sat + "% " + lit + "%), hsl(" +
        hue + " " + Math.max(sat - 10, 35) + "% " + Math.min(lit + 13, 97) + "%))",
      borderColor: "hsl(" + hue + " " + Math.min(sat + 12, 92) + "% " + Math.max(lit - 32, 38) + "%)",
    };
  }

  function renderFlagPanel(el, cfg, results) {
    const stateFn = (cfg.flag && cfg.flag.state) ||
      ((v) => ({ text: fmtTip(v), color: "#e6e6e6" }));
    const wrap = document.createElement("div");
    wrap.className = "flags";
    results.forEach(({ sc, data }) => {
      const v = latestValue(data);
      const st = v == null ? { text: "—", color: "#eef0f2", fg: "#8b949e" } : stateFn(v);
      const cell = document.createElement("div");
      cell.className = "flag";
      cell.style.background = st.color;
      if (st.fg) cell.style.color = st.fg;
      const name = document.createElement("div");
      name.className = "flag-name";
      name.textContent = sc.label;
      const val = document.createElement("div");
      val.className = "flag-value";
      val.textContent = st.text;
      cell.appendChild(name);
      cell.appendChild(val);
      wrap.appendChild(cell);
    });
    el.innerHTML = "";
    el.appendChild(wrap);
  }

  /* ---- ECharts option builders ---------------------------------------- */
  function baseYAxis(cfg) {
    const y = [{
      type: "value", scale: true, position: "left",
      name: cfg.axisLeft && cfg.axisLeft.label || "",
      nameLocation: "middle", nameGap: 42, nameTextStyle: { color: AXIS },
      min: cfg.axisLeft && cfg.axisLeft.min, max: cfg.axisLeft && cfg.axisLeft.max,
      axisLabel: {
        color: AXIS,
        formatter: cfg.axisLeft && cfg.axisLeft.abbrev ? abbrevNum : undefined,
      },
      splitLine: { lineStyle: { color: GRID } },
    }];
    if (cfg.axisRight && cfg.axisRight.show) {
      y.push({
        type: "value", scale: true, position: "right",
        name: cfg.axisRight.label || "",
        nameLocation: "middle", nameGap: 42, nameTextStyle: { color: AXIS },
        min: cfg.axisRight.min, max: cfg.axisRight.max,
        axisLabel: { color: AXIS }, splitLine: { show: false },
      });
    }
    return y;
  }

  function thresholdMarkLine(sc) {
    if (!sc.thresholds) return undefined;
    const dashed = sc.thresholds.style === "dashed";
    return {
      symbol: "none", silent: true,
      label: { formatter: "{c}", position: "insideEndTop", color: AXIS, fontSize: 10 },
      lineStyle: { type: dashed ? "dashed" : "solid", width: 1 },
      data: sc.thresholds.steps.map((st) => ({
        yAxis: st.value, lineStyle: { color: st.color },
      })),
    };
  }

  /* Static annotations: labelled vertical lines at fixed times (config-driven). */
  const ANNOTATION_COLOR = "#8250df";
  function resolvedAnnotations() {
    return (DASHBOARD.annotations || [])
      .map((a) => ({ t: resolveTime(a.time, NaN), label: a.label, color: a.color }))
      .filter((a) => isFinite(a.t) && a.t >= fromMs && a.t <= toMs);
  }
  function annotationMarkLine() {
    const list = resolvedAnnotations();
    if (!list.length) return undefined;
    return {
      symbol: "none", silent: true, animation: false,
      label: {
        formatter: "{b}", position: "insideEndTop",
        color: "#ffffff", fontSize: 10, fontWeight: "bold",
        backgroundColor: ANNOTATION_COLOR, padding: [2, 5], borderRadius: 3,
      },
      lineStyle: { type: "dashed", width: 1, color: ANNOTATION_COLOR },
      data: list.map((a) => ({
        name: a.label, xAxis: a.t,
        lineStyle: { color: a.color || ANNOTATION_COLOR },
        label: { backgroundColor: a.color || ANNOTATION_COLOR },
      })),
    };
  }
  /* Empty series to host annotation markLines. */
  function annotationSeries() {
    const markLine = annotationMarkLine();
    return markLine
      ? [{ type: "line", data: [], silent: true, showSymbol: false, markLine }]
      : [];
  }

  /* Floating legend(s) over plot area; split by axis with dual Y-axes. */
  const LEGEND_BG = "rgba(255,255,255,0.72)";
  function legendPiece(names, side, selected) {
    if (!names.length) return null;
    return {
      data: names, selected, top: 4, [side]: 8,
      backgroundColor: LEGEND_BG, borderRadius: 4, padding: [3, 8],
      textStyle: { color: AXIS, fontWeight: "bold" }, icon: "roundRect",
    };
  }
  function floatingLegend(leftNames, rightNames, selected) {
    const pieces = [
      legendPiece(leftNames, "left", selected),
      legendPiece(rightNames, "right", selected),
    ].filter(Boolean);
    return pieces.length ? pieces : undefined;
  }

  /* Interpolate value at exact hovered time (not nearest data point). */
  function valueAt(xy, t) {
    if (!xy || !xy.length) return null;
    const n = xy.length;
    if (t <= xy[0][0]) return xy[0][1];
    if (t >= xy[n - 1][0]) return xy[n - 1][1];
    let lo = 0, hi = n - 1;
    while (hi - lo > 1) {
      const mid = (lo + hi) >> 1;
      if (xy[mid][0] <= t) lo = mid; else hi = mid;
    }
    const [t0, v0] = xy[lo], [t1, v1] = xy[hi];
    if (v0 == null || v1 == null) return v0 != null ? v0 : v1; // hold the known side
    if (t1 === t0) return v0;
    return v0 + (v1 - v0) * ((t - t0) / (t1 - t0));
  }
  function fmtDateTime(ms) {
    const d = new Date(ms);
    return pad(d.getDate()) + "." + pad(d.getMonth() + 1) + "." + d.getFullYear() + " " +
      pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds());
  }
  /* Default palette mirrors ECharts theme; allows custom tooltip handling. */
  const DEFAULT_PALETTE = [
    "#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de",
    "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc", "#37a2da",
    "#32c5e9", "#67e0e3", "#9fe6b8", "#ffdb5c", "#ff9f7f",
    "#fb7293", "#e7bcf3", "#8378ea",
  ];

  /* Custom tooltip formatter: shows every configured series with interpolated values. */
  function axisTooltipFormatter(seriesInfo) {
    return (params) => {
      if (!Array.isArray(params) || !params.length) return "";
      const t = params[0].axisValue;
      const rows = [];
      seriesInfo.forEach(({ data, color }, name) => {
        const v = valueAt(data, t);
        const marker = '<span style="display:inline-block;margin-right:6px;' +
          "width:9px;height:9px;border-radius:50%;background:" + color + ';"></span>';
        rows.push('<div style="display:flex;justify-content:space-between;gap:14px;">' +
          "<span>" + marker + name + "</span>" +
          '<span style="font-weight:600;margin-left:auto">' + fmtTip(v) + "</span></div>");
      });
      if (!rows.length) return "";
      return '<div style="font-weight:600;margin-bottom:3px;">' + fmtDateTime(t) + "</div>" + rows.join("");
    };
  }

  /* Build the ECharts option for a timeseries / state panel from fetched data.
   * `fetched` maps a series config -> its [[ts,val], ...] array. */
  function buildTimeseries(cfg, fetched, legendSelected) {
    const leftNames = [], rightNames = [];
    const series = [];
    const seriesInfo = new Map();
    let paletteIdx = 0;
    const nextColor = () => DEFAULT_PALETTE[paletteIdx++ % DEFAULT_PALETTE.length];
    cfg.series.forEach((sc) => {
      const yIdx = sc.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
      const data = fetched.get(sc);
      const step = cfg.type === "state" ? "end" : false;
      const color = sc.color || nextColor();
      (yIdx ? rightNames : leftNames).push(sc.label);
      seriesInfo.set(sc.label, { data, color });
      series.push({
        name: sc.label, type: "line", yAxisIndex: yIdx,
        showSymbol: false, sampling: "lttb", smooth: !!sc.smooth, step,
        connectNulls: false,
        lineStyle: { width: sc.width == null ? 1 : sc.width, color, type: sc.dash || "solid" },
        itemStyle: { color },
        areaStyle: sc.fillOpacity ? { opacity: sc.fillOpacity / 100, color } : undefined,
        markLine: thresholdMarkLine(sc),
        data,
      });
      if (sc.movavg) {
        const m = sc.movavg;
        const mIdx = m.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
        const mColor = m.color || nextColor();
        (mIdx ? rightNames : leftNames).push(m.label);
        const mData = movingAverage(data, m.size);
        seriesInfo.set(m.label, { data: mData, color: mColor });
        series.push({
          name: m.label, type: "line", yAxisIndex: mIdx,
          showSymbol: false, smooth: true,
          lineStyle: { width: m.width || 2, color: mColor },
          itemStyle: { color: mColor },
          areaStyle: m.fillOpacity ? { opacity: m.fillOpacity / 100, color: mColor } : undefined,
          data: mData,
        });
      }
    });
    series.push(...annotationSeries());
    return {
      backgroundColor: "transparent", animation: false,
      textStyle: { color: "#1f2328" },
      // snap: false -- ECharts snaps the axis pointer (and thus `axisValue`
      // in the tooltip formatter) to the nearest *data point* by default on
      // a continuous time axis; that defeats the whole point of computing
      // our own interpolated/held value below the actual cursor position.
      tooltip: {
        trigger: "axis", axisPointer: { type: "line", snap: false },
        formatter: axisTooltipFormatter(seriesInfo),
      },
      legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
      // Fixed margins for synced hover cursor alignment across panels
      grid: { left: 64, right: 64, top: GRID_TOP, bottom: gridBottom(cfg) },
      xAxis: timeXAxis(cfg),
      yAxis: baseYAxis(cfg),
      dataZoom: insideZoom(),
      series,
    };
  }

  /* Categorical state band renderer: converts series to time-range segments. */

  /* Collapse runs of same value into segments, breaking across data gaps. */
  function buildStageSegments(xy, states) {
    const pts = (xy || []).filter((p) => p[1] != null);
    const n = pts.length;
    if (!n) return [];
    const deltas = [];
    for (let i = 1; i < n; i++) {
      const d = pts[i][0] - pts[i - 1][0];
      if (d > 0) deltas.push(d);
    }
    deltas.sort((a, b) => a - b);
    const med = deltas.length ? deltas[Math.floor(deltas.length / 2)] : 60000;
    const gapCap = Math.max(med * 4, 5 * 60000);   // max width a single step may span
    const segs = [];
    let i = 0;
    while (i < n) {
      const code = Math.round(pts[i][1]);
      let j = i + 1;
      while (j < n && Math.round(pts[j][1]) === code &&
             (pts[j][0] - pts[j - 1][0]) <= gapCap) j++;
      const start = pts[i][0];
      const lastTs = pts[j - 1][0];
      const nextTs = j < n ? pts[j][0] : lastTs + med;
      const end = Math.min(nextTs, lastTs + gapCap);
      if (states[code] && end > start) segs.push([start, end, code]);
      i = j;
    }
    return segs;
  }

  /* Custom renderItem: clipped, labelled rectangles per segment. */
  function makeStageRenderer(states) {
    return function renderStageItem(params, api) {
      const m = states[api.value(2)];
      if (!m) return;
      const cs = params.coordSys;                   // { x, y, width, height }
      const left = cs.x, right = cs.x + cs.width;
      let x0 = api.coord([api.value(0), 0])[0];
      let x1 = api.coord([api.value(1), 0])[0];
      x0 = Math.max(x0, left); x1 = Math.min(x1, right);
      const w = x1 - x0;
      if (w <= 0) return;
      const children = [{
        type: "rect",
        shape: { x: x0, y: cs.y, width: w, height: cs.height },
        style: { fill: m.color, stroke: "#ffffff", lineWidth: 0.5 },
      }];
      if (w >= 34) {
        children.push({
          type: "text",
          style: {
            text: m.label, x: x0 + w / 2, y: cs.y + cs.height / 2,
            textAlign: "center", textVerticalAlign: "middle",
            fill: m.text, fontSize: 10, width: w - 6,
            overflow: "truncate", ellipsis: "",
          },
        });
      }
      return { type: "group", children };
    };
  }

  function buildStateBand(cfg, xy) {
    const states = (cfg.series[0] && cfg.series[0].states) || {};
    const fmt = (ms) => {
      const d = new Date(ms);
      return pad(d.getHours()) + ":" + pad(d.getMinutes());
    };
    return {
      backgroundColor: "transparent", animation: false,
      textStyle: { color: "#1f2328" },
      tooltip: {
        trigger: "axis", axisPointer: { type: "line" },
        formatter: (ps) => {
          const it = ps && ps[0];
          if (!it || !it.value) return "";
          const v = it.value, m = states[v[2]];
          const dur = Math.round((v[1] - v[0]) / 60000);
          return "<b>" + (m ? m.label : v[2]) + "</b><br/>" +
            fmt(v[0]) + " – " + fmt(v[1]) + " · " + dur + " min";
        },
      },
      grid: { left: 64, right: 64, top: GRID_TOP, bottom: gridBottom(cfg) },
      xAxis: timeXAxis(cfg),
      yAxis: {
        type: "value", min: 0, max: 1,
        name: (cfg.axisLeft && cfg.axisLeft.label) || "",
        nameLocation: "middle", nameGap: 42, nameTextStyle: { color: AXIS },
        axisLine: { show: false }, axisTick: { show: false },
        axisLabel: { show: false }, splitLine: { show: false },
      },
      dataZoom: insideZoom(),
      series: [{
        type: "custom", renderItem: makeStageRenderer(states),
        encode: { x: [0, 1] }, clip: true,
        data: buildStageSegments(xy, states),
      }, ...annotationSeries()],
    };
  }

  /* Type "daily": pre-aggregated daily data with visible points. */
  function buildDaily(cfg, table, legendSelected) {
    const legendData = [], series = [];
    cfg.series.forEach((sc) => {
      legendData.push(sc.label);
      series.push({
        name: sc.label, type: "line", data: toXY(table, sc.column),
        showSymbol: true, symbol: "circle", symbolSize: 6,
        lineStyle: { width: 2, color: sc.color },
        itemStyle: { color: sc.color },
        areaStyle: { opacity: 0.5, color: sc.color },
        markLine: thresholdMarkLine(sc),
      });
    });
    return {
      backgroundColor: "transparent", animation: false,
      tooltip: { trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip },
      legend: cfg.legend ? floatingLegend(legendData, [], legendSelected) : undefined,
      grid: { left: 56, right: 24, top: 16, bottom: 44 },
      xAxis: {
        type: "time", axisLabel: { color: AXIS },
        axisLine: { lineStyle: { color: BORDER } },
        splitLine: { show: false },
      },
      yAxis: baseYAxis(cfg),
      dataZoom: insideZoom(),
      series,
    };
  }

  /* ---- Panel -- one card with lazy loading ---------------------------- */
  class Panel {
    constructor(cfg) {
      this.cfg = cfg;
      this.chart = null;
      this.loaded = false;
      this.dirty = true;
      this.visible = false;
      this.tileEls = null;   // "tiles" panels: persistent per-tile DOM refs, survive reloads

      const host = document.createElement("div");
      host.className = "panel" + (cfg.type === "tiles" ? " panel-tiles" : "");
      // "tiles" panels size to their content (a wrapping row of cards)
      // instead of the fixed chart height every other panel type uses.
      host.style.height = cfg.type === "tiles" ? "auto" : (cfg.height || 280) + "px";
      // No panel heading -- each plot's Y-axis label already names its content.
      const chartEl = document.createElement("div");
      chartEl.className = "panel-chart";
      chartEl.style.position = "relative";   // anchor for the drag-select overlay
      host.appendChild(chartEl);
      this.host = host;
      this.chartEl = chartEl;
    }

    ensureChart() {
      if (this.chart) return;
      this.chart = echarts.init(this.chartEl);

      if (this.cfg.type === "daily") return;  // keep own X-axis
      
      this.chart.on("datazoom", () => {
        if (syncing) return;
        const dz = (this.chart.getOption().dataZoom || [])[0];
        if (!(dz && dz.startValue != null && dz.endValue != null)) return;
        zoomWindow = { s: dz.startValue, e: dz.endValue };
        broadcastZoom(this.chart);
      });

      const zr = this.chart.getZr();
      zr.on("mousemove", (ev) => {
        if (!this.chart.containPixel("grid", [ev.offsetX, ev.offsetY])) {
          broadcastHide();
          return;
        }
        const t = this.chart.convertFromPixel({ xAxisIndex: 0 }, ev.offsetX);
        broadcastShowAtValue(t);
      });
      zr.on("mouseout", broadcastHide);

      this.attachDragZoom();
    }

    /* LEFT drag: zoom to region; RIGHT drag: pan window. */
    attachDragZoom() {
      const chart = this.chart, el = this.chartEl;
      el.addEventListener("contextmenu", (e) => e.preventDefault());

      const sel = document.createElement("div");
      sel.className = "zoom-select";
      sel.style.display = "none";
      el.appendChild(sel);

      const pxOf = (e) => e.clientX - el.getBoundingClientRect().left;
      let drag = null, raf = 0;

      el.addEventListener("pointerdown", (e) => {
        if (e.button !== 0 && e.button !== 2) return;
        const rect = el.getBoundingClientRect();
        const startPx = e.clientX - rect.left, startPy = e.clientY - rect.top;
        if (!chart.containPixel("grid", [startPx, startPy])) return;
        drag = {
          button: e.button, startPx, curPx: startPx,
          startT: chart.convertFromPixel({ xAxisIndex: 0 }, startPx),
          moved: false, off: 0,
        };
        if (e.button === 0) {  // left: show selection band
          sel.style.left = startPx + "px";
          sel.style.top = GRID_TOP + "px";
          sel.style.width = "0px";
          sel.style.height = Math.max(0, chart.getHeight() - GRID_TOP - gridBottom(this.cfg)) + "px";
          sel.style.display = "block";
        }
        try { el.setPointerCapture(e.pointerId); } catch (_) {}
        e.preventDefault();
      });

      el.addEventListener("pointermove", (e) => {
        if (!drag) return;
        const px = pxOf(e);
        drag.curPx = px;
        if (Math.abs(px - drag.startPx) > 2) drag.moved = true;
        if (drag.button === 0) {  // left: grow selection
          sel.style.left = Math.min(drag.startPx, px) + "px";
          sel.style.width = Math.abs(px - drag.startPx) + "px";
        } else {                  // right: live-pan
          drag.off = drag.startT - chart.convertFromPixel({ xAxisIndex: 0 }, px);
          if (!raf) raf = requestAnimationFrame(() => {
            raf = 0;
            if (drag && drag.button === 2) livePan(drag.off);
          });
        }
      });

      const end = (e) => {
        if (!drag) return;
        const d = drag; drag = null;
        try { el.releasePointerCapture(e.pointerId); } catch (_) {}
        sel.style.display = "none";
        if (!d.moved) return;
        if (d.button === 0) {         // adopt selected span
          const a = chart.convertFromPixel({ xAxisIndex: 0 }, Math.min(d.startPx, d.curPx));
          const b = chart.convertFromPixel({ xAxisIndex: 0 }, Math.max(d.startPx, d.curPx));
          adoptWindow(Math.max(fromMs, Math.min(a, b)), Math.min(toMs, Math.max(a, b)));
        } else if (d.off) {           // adopt panned window
          adoptWindow(fromMs + d.off, toMs + d.off);
        }
      };
      el.addEventListener("pointerup", end);
      el.addEventListener("pointercancel", end);
    }

    markDirty() {
      this.dirty = true;
      if (this.visible) this.load();
    }

    /* Current legend on/off selection of the live chart, so it survives a
     * reload (e.g. when only the time range changes). */
    legendSelection() {
      if (!this.chart) return undefined;
      const opt = this.chart.getOption();
      const legends = (opt && opt.legend) || [];
      let merged;
      legends.forEach((lg) => {
        if (lg && lg.selected) merged = Object.assign(merged || {}, lg.selected);
      });
      return merged;
    }

    async load() {
      if (!this.dirty || this._busy) return;
      this._busy = true;
      this.dirty = false;
      const cfg = this.cfg;
      // A "flag" or "tiles" panel renders plain DOM, not an ECharts canvas.
      if (cfg.type !== "flag" && cfg.type !== "tiles") { this.ensureChart(); this.chart.resize(); }
      bump(1);
      try {
        // Remember the legend on/off state so toggles persist across reloads.
        const legendSel = this.chart ? this.legendSelection() : undefined;
        if (cfg.type === "flag") {
          const results = await Promise.all(cfg.series.map(async (sc) =>
            ({ sc, data: await seriesData(sc) })));
          renderFlagPanel(this.chartEl, cfg, results);
        } else if (cfg.type === "tiles") {
          await this.loadTiles();
        } else if (cfg.type === "daily") {
          const { start, end } = panelRange(cfg);
          const table = await cachedFetchTable({
            kind: cfg.kind, session: cfg.session,
            start, end, max_points: maxPointsOverride(2000),
          });
          this.chart.setOption(buildDaily(cfg, table, legendSel), true);
        } else {
          const map = new Map();
          await Promise.all(cfg.series.map(async (sc) => {
            map.set(sc, await seriesData(sc));
          }));
          if (cfg.type === "state") {
            this.chart.setOption(buildStateBand(cfg, map.get(cfg.series[0])), true);
          } else {
            this.chart.setOption(
              buildTimeseries(cfg, { get: (k) => map.get(k) }, legendSel), true);
          }
        }
        this.loaded = true;
        // Replay the current synced zoom onto this freshly-loaded panel.
        if (zoomWindow && this.chart) {
          this.chart.dispatchAction({
            type: "dataZoom", startValue: zoomWindow.s, endValue: zoomWindow.e,
          });
        }
      } catch (e) {
        if (this.chart) {
          this.chart.setOption({ title: { text: "Error: " + e.message, left: "center", top: "middle", textStyle: { color: "#e02f44", fontSize: 12 } } });
        } else {
          this.chartEl.innerHTML = '<div class="flag-error">Error: ' + e.message + "</div>";
        }
      } finally {
        bump(-1);
        this._busy = false;
        if (this.dirty && this.visible) this.load();
      }
    }

    /* Build tile cards; addons mounted once and reused across reloads. */
    buildTilesShell() {
      const wrap = document.createElement("div");
      wrap.className = "tiles";
      this.tileEls = this.cfg.tiles.map((t) => {
        const card = document.createElement("div");
        card.className = "tile";
        const accent = tileAccent(t.label);
        card.style.background = accent.background;
        card.style.borderColor = accent.borderColor;
        const name = document.createElement("div");
        name.className = "tile-name";
        name.textContent = t.label;
        card.appendChild(name);
        let valueEl = null;
        if (t.series) {
          valueEl = document.createElement("div");
          valueEl.className = "tile-value";
          valueEl.textContent = "…";
          card.appendChild(valueEl);
        }
        if (t.addon) {
          const addonEl = document.createElement("div");
          addonEl.className = "tile-addon";
          card.appendChild(addonEl);
          try { t.addon(addonEl, TILE_CTX); } catch (e) { console.warn("tile addon failed:", e); }
        }
        wrap.appendChild(card);
        return { valueEl };
      });
      this.chartEl.innerHTML = "";
      this.chartEl.appendChild(wrap);
    }
    async loadTiles() {
      if (!this.tileEls) this.buildTilesShell();
      await Promise.all(this.cfg.tiles.map(async (t, i) => {
        const valueEl = this.tileEls[i].valueEl;
        if (!valueEl) return;
        try {
          const v = latestValue(await seriesData(t.series));
          valueEl.textContent = v == null ? "—" :
            (t.format ? t.format(v) : fmtTip(v) + (t.unit ? " " + t.unit : ""));
        } catch (e) {
          valueEl.textContent = "—";
        }
      }));
    }

    resize() { if (this.chart) this.chart.resize(); }
  }

  /* ---- DOM construction from the dashboard config --------------------- */
  function buildPanel(cfg) {
    const p = new Panel(cfg);
    panels.push(p);
    return p;
  }

  function buildGrid(container, panelCfgs) {
    const grid = document.createElement("div");
    grid.className = "grid";
    panelCfgs.forEach((cfg) => grid.appendChild(buildPanel(cfg).host));
    container.appendChild(grid);
  }

  /* Tab bar in header; bodies in container. */
  function buildTabs(headEl, bodyContainer, tabs) {
    const bar = document.createElement("div");
    bar.className = "tabbar";
    const bodies = [];
    tabs.forEach((tab, i) => {
      const btn = document.createElement("button");
      btn.className = "tab" + (i === 0 ? " active" : "");
      btn.textContent = tab.title;
      const body = document.createElement("div");
      body.className = "tab-body";
      body.style.display = i === 0 ? "" : "none";
      buildGrid(body, tab.panels);
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        bar.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        bodies.forEach((b) => (b.style.display = "none"));
        body.style.display = "";
        // Panels in the newly shown tab become visible -> observer loads them.
        requestAnimationFrame(() => panels.forEach((p) => p.resize()));
      });
      bar.appendChild(btn);
      bodyContainer.appendChild(body);
      bodies.push(body);
    });
    headEl.appendChild(bar);
  }

  function buildRow(rowCfg) {
    const row = document.createElement("section");
    row.className = "row";
    const head = document.createElement("div");
    head.className = "row-head";
    const caret = document.createElement("span");
    caret.className = "caret";
    caret.textContent = "▾";
    const h = document.createElement("h2");
    h.textContent = rowCfg.title;
    head.appendChild(caret);
    head.appendChild(h);

    const content = document.createElement("div");
    content.className = "row-content";
    if (rowCfg.type === "tabs") buildTabs(head, content, rowCfg.tabs);
    else buildGrid(content, rowCfg.panels);

    head.addEventListener("click", () => {
      const collapsed = row.classList.toggle("collapsed");
      content.style.display = collapsed ? "none" : "";
      caret.textContent = collapsed ? "▸" : "▾";
      if (!collapsed) requestAnimationFrame(() => panels.forEach((p) => p.resize()));
    });

    if (rowCfg.collapse) {
      row.classList.add("collapsed");
      content.style.display = "none";
      caret.textContent = "▸";
    }

    row.appendChild(head);
    row.appendChild(content);
    return row;
  }

  /* ---- lazy loading via IntersectionObserver -------------------------- */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((ent) => {
      const p = ent.target.__panel;
      if (!p) return;
      p.visible = ent.isIntersecting && ent.intersectionRatio > 0;
      if (p.visible && p.dirty) p.load();
    });
  }, { root: null, threshold: 0.01 });

  /* ---- range application ---------------------------------------------- */
  function applyRange() {
    fromMs = parseLocal(fromIn.value);
    toMs = parseLocal(toIn.value);
    if (!(fromMs < toMs)) { setStatus("Invalid range"); return; }
    zoomWindow = null;                       // fresh data -> reset synced zoom
    queryCache.clear();                      // drop shared query results for the old window
    panels.forEach((p) => p.markDirty());    // visible ones reload immediately
  }

  function setQuickRange(spanMs) {
    toMs = Date.now();
    fromMs = toMs - spanMs;
    syncInputs();
    applyRange();
  }

  function shift(dir) {
    const span = toMs - fromMs;
    fromMs += dir * span;
    toMs += dir * span;
    syncInputs();
    applyRange();
  }

  function resetZoom() {
    zoomWindow = null;
    panels.forEach((p) => {
      if (p.chart) p.chart.dispatchAction({ type: "dataZoom", start: 0, end: 100 });
    });
  }

  /* Live pan feedback: shift the X window of every synced, loaded panel by an
   * offset (ms) without re-querying -- used while a right-drag is in flight. */
  function livePan(off) {
    panels.forEach((p) => {
      if (syncable(p) && p.loaded)
        p.chart.setOption({ xAxis: { min: fromMs + off, max: toMs + off } });
    });
  }

  function adoptWindow(start, end) {
    if (!(end - start > 1000)) return;       // ignore accidental micro-drags
    fromMs = start; toMs = end;
    syncInputs();
    quickSel.value = "custom";
    applyRange();                            // resets zoom + reloads at new res.
  }



  /* Render external links in top bar (config-driven). */
  function renderHeaderLinks() {
    const links = DASHBOARD.links || [];
    const topbar = document.querySelector(".topbar");
    if (!links.length || !topbar) return;
    const nav = document.createElement("nav");
    nav.className = "links";
    links.forEach((l) => {
      const a = document.createElement("a");
      a.href = l.url;
      a.textContent = l.label;
      a.target = l.target || "_blank";
      a.rel = "noopener noreferrer";
      nav.appendChild(a);
    });
    const titleEl = document.getElementById("pageTitle");
    if (titleEl && titleEl.parentNode === topbar) topbar.insertBefore(nav, titleEl.nextSibling);
    else topbar.appendChild(nav);
  }

  /* Auto-refresh: advance rolling windows on interval; skips when tab hidden. */
  const AUTO_REFRESH_MS = 15000;
  function startAutoRefresh() {
    setInterval(() => {
      if (autoRefreshIn && !autoRefreshIn.checked) return;
      if (document.hidden) return;
      if (quickSel.value === "custom") return;
      setQuickRange(parseInt(quickSel.value, 10));
    }, AUTO_REFRESH_MS);
  }

  /* ---- wire up -------------------------------------------------------- */
  function init() {
    document.title = DASHBOARD.title;
    const titleEl = document.getElementById("pageTitle");
    if (titleEl) titleEl.textContent = DASHBOARD.title;
    renderHeaderLinks();
    DASHBOARD.rows.forEach((r) => boardEl.appendChild(buildRow(r)));
    panels.forEach((p) => { p.host.__panel = p; observer.observe(p.host); });

    quickSel.addEventListener("change", () => {
      if (quickSel.value === "custom") return;
      setQuickRange(parseInt(quickSel.value, 10));
    });
    document.getElementById("apply").addEventListener("click", () => {
      quickSel.value = "custom"; applyRange();
    });
    document.getElementById("resetZoom").addEventListener("click", resetZoom);
    maxPointsIn.addEventListener("change", () => {
      queryCache.clear();                    // resolution changed -> re-query
      panels.forEach((p) => p.markDirty());
    });
    document.getElementById("shiftBack").addEventListener("click", () => shift(-1));
    document.getElementById("shiftFwd").addEventListener("click", () => shift(1));
    [fromIn, toIn].forEach((el) => el.addEventListener("change", () => (quickSel.value = "custom")));

    window.addEventListener("resize", () => panels.forEach((p) => p.resize()));

    // Initial window: last 24h.
    setQuickRange(86400000);

    // Keep rolling "Last *" ranges live (every 15s).
    startAutoRefresh();
  }

  init();
})();
