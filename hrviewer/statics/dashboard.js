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

  /* ---- global "max_points" override -------------------------------------
   * Overrides the per-query aggregation resolution sent to the API for
   * *every* panel. Empty (default) leaves each query's own default (see
   * `dflt` fallback below) untouched. */
  function maxPointsOverride(dflt) {
    const v = parseInt(maxPointsIn.value, 10);
    return Number.isFinite(v) && v > 0 ? v : dflt;
  }

  /* ---- Apache Arrow decoding ------------------------------------------ */
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
  /* Build [[tsMs, value], ...] from an Arrow table's `ts` + value column. */
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

  /* ---- static annotations (config-driven, `DASHBOARD.annotations`) -----
   * A labelled, dashed vertical line drawn at a fixed point in time, on
   * every synced timeseries/state panel (not on "daily" panels, which run
   * on their own independent, day-aggregated time axis). Purely declarative
   * -- set in the dashboard config, see dashboard.config.js; there's no
   * interactive "add annotation" UI. */
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
  /* An invisible, empty carrier series purely to host the annotation
   * markLine -- works uniformly regardless of a panel's own series (e.g. a
   * "state" panel's single custom-rendered band). */
  function annotationSeries() {
    const markLine = annotationMarkLine();
    return markLine
      ? [{ type: "line", data: [], silent: true, showSymbol: false, markLine }]
      : [];
  }

  /* Floating, semi-transparent legend(s), drawn directly over the plot area
   * instead of taking up their own row. With a right Y-axis in play, series
   * are split into two legend components by axis affiliation: left-axis
   * series top-left, right-axis series top-right. `selected` is shared --
   * each piece only looks up the names it owns, so toggling one doesn't
   * touch the other. No wrapping/scrolling: panels are wide enough. */
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

  /* Build the ECharts option for a timeseries / state panel from fetched data.
   * `fetched` maps a series config -> its [[ts,val], ...] array. */
  function buildTimeseries(cfg, fetched, legendSelected) {
    const leftNames = [], rightNames = [];
    const series = [];
    cfg.series.forEach((sc) => {
      const yIdx = sc.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
      const data = fetched.get(sc);
      const step = cfg.type === "state" ? "end" : false;
      (yIdx ? rightNames : leftNames).push(sc.label);
      series.push({
        name: sc.label, type: "line", yAxisIndex: yIdx,
        showSymbol: false, sampling: "lttb", smooth: !!sc.smooth, step,
        connectNulls: false,
        lineStyle: { width: sc.width == null ? 1 : sc.width, color: sc.color },
        itemStyle: { color: sc.color },
        areaStyle: sc.fillOpacity ? { opacity: sc.fillOpacity / 100, color: sc.color } : undefined,
        markLine: thresholdMarkLine(sc),
        data,
      });
      if (sc.movavg) {
        const m = sc.movavg;
        const mIdx = m.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
        (mIdx ? rightNames : leftNames).push(m.label);
        series.push({
          name: m.label, type: "line", yAxisIndex: mIdx,
          showSymbol: false, smooth: true,
          lineStyle: { width: m.width || 2, color: m.color },
          itemStyle: { color: m.color },
          areaStyle: m.fillOpacity ? { opacity: m.fillOpacity / 100, color: m.color } : undefined,
          data: movingAverage(data, m.size),
        });
      }
    });
    series.push(...annotationSeries());
    return {
      backgroundColor: "transparent", animation: false,
      textStyle: { color: "#1f2328" },
      tooltip: { trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip },
      legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
      // Fixed left/right margins on every timeseries/state panel, so a given
      // timestamp maps to the same pixel X everywhere (needed for the synced
      // hover cursor), regardless of whether a panel has a right axis.
      grid: { left: 64, right: 64, top: GRID_TOP, bottom: gridBottom(cfg) },
      xAxis: timeXAxis(cfg),
      yAxis: baseYAxis(cfg),
      dataZoom: insideZoom(),
      series,
    };
  }

  /* ---- categorical "state" band (e.g. sleep stage) ----------------------
   * Renders a categorical series as a single-row colour band: runs of the
   * same value become labelled, coloured rectangles spanning their time
   * range. The code -> { label, color, text } mapping is domain-specific, so
   * it comes from the panel config (`cfg.series[0].states`), keeping this
   * renderer generic; a missing code renders as a gap. */

  /* Collapse [ts,value] points into [start, end, code] segments, breaking
   * runs across long gaps (e.g. between separate nights) so no rectangle is
   * stretched over a period with no data. */
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

  /* Custom renderItem factory: draw one clipped, labelled rectangle per run,
   * coloured/labelled via the panel's `states` map. */
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

  /* Type "daily" panels: line charts with visible points and a translucent
   * area fill, plotted from a pre-aggregated table (own time X-axis). */
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

      const host = document.createElement("div");
      host.className = "panel";
      host.style.height = (cfg.height || 280) + "px";
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

      // "daily" panels keep their own X-axis, outside the cross-panel sync.
      if (this.cfg.type === "daily") return;

      // --- zoom sync (by axis value) ---
      // Capture zoom changes, remember them (to replay onto panels that load
      // later) and broadcast them to the other panels.
      this.chart.on("datazoom", () => {
        if (syncing) return;
        const dz = (this.chart.getOption().dataZoom || [])[0];
        if (!(dz && dz.startValue != null && dz.endValue != null)) return;
        zoomWindow = { s: dz.startValue, e: dz.endValue };
        broadcastZoom(this.chart);
      });

      // --- hover cursor sync (by axis value) ---
      // Convert the pointer to a time value on this panel and re-project it to
      // each other panel's pixel position, so the vertical hover line lines up
      // regardless of differing point densities.
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

    /* Mouse interaction on the plot:
     *   - LEFT + drag  -> highlight a region; on release it becomes the new
     *     query window (re-fetched at full resolution, not just rescaled),
     *   - RIGHT + drag -> live-pan the current window; re-fetched on release. */
    attachDragZoom() {
      const chart = this.chart, el = this.chartEl;
      el.addEventListener("contextmenu", (e) => e.preventDefault());

      const sel = document.createElement("div");
      sel.className = "zoom-select";
      sel.style.display = "none";
      el.appendChild(sel);

      const pxOf = (e) => e.clientX - el.getBoundingClientRect().left;
      let drag = null, raf = 0;

      // Pointer Events + pointer capture: once the drag starts, every
      // pointermove/pointerup is delivered to this element even when the cursor
      // leaves it, so we never lose the move/up phase (which was the bug with
      // document-level mouse listeners on top of the ECharts canvas).
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
        if (e.button === 0) {
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
        if (drag.button === 0) {                 // left: grow the selection band
          sel.style.left = Math.min(drag.startPx, px) + "px";
          sel.style.width = Math.abs(px - drag.startPx) + "px";
        } else {                                 // right: live-pan the window
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
        if (d.button === 0) {                    // adopt the selected span
          const a = chart.convertFromPixel({ xAxisIndex: 0 }, Math.min(d.startPx, d.curPx));
          const b = chart.convertFromPixel({ xAxisIndex: 0 }, Math.max(d.startPx, d.curPx));
          adoptWindow(Math.max(fromMs, Math.min(a, b)), Math.min(toMs, Math.max(a, b)));
        } else if (d.off) {                      // adopt the panned window
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
      this.ensureChart();
      this.chart.resize();
      bump(1);
      try {
        const cfg = this.cfg;
        // Remember the legend on/off state so toggles persist across reloads.
        const legendSel = this.legendSelection();
        if (cfg.type === "daily") {
          const { start, end } = panelRange(cfg);
          const table = await fetchTable({
            kind: cfg.kind, session: cfg.session,
            start, end, max_points: maxPointsOverride(2000),
          });
          this.chart.setOption(buildDaily(cfg, table, legendSel), true);
        } else {
          const map = new Map();
          await Promise.all(cfg.series.map(async (sc) => {
            const table = await fetchTable({
              kind: "series", segment: sc.segment, metric: sc.metric,
              agg: sc.agg || "avg", start: fromMs, end: toMs,
              max_points: maxPointsOverride(3000),
            });
            map.set(sc, toXY(table, "value"));
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
        if (zoomWindow) {
          this.chart.dispatchAction({
            type: "dataZoom", startValue: zoomWindow.s, endValue: zoomWindow.e,
          });
        }
      } catch (e) {
        this.chart.setOption({ title: { text: "Error: " + e.message, left: "center", top: "middle", textStyle: { color: "#e02f44", fontSize: 12 } } });
      } finally {
        bump(-1);
        this._busy = false;
        if (this.dirty && this.visible) this.load();
      }
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

  /* The tab bar itself lives in the row header (next to the title), so it
   * doesn't cost its own vertical row above the panel grid; only the tab
   * bodies go into `bodyContainer`. Clicks on tabs stop propagating so they
   * don't also trigger the header's collapse toggle. */
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

  /* Adopt a new [start,end] window (ms) as the query range and re-fetch. */
  function adoptWindow(start, end) {
    if (!(end - start > 1000)) return;       // ignore accidental micro-drags
    fromMs = start; toMs = end;
    syncInputs();
    quickSel.value = "custom";
    applyRange();                            // resets zoom + reloads at new res.
  }



  /* ---- wire up -------------------------------------------------------- */
  function init() {
    document.title = DASHBOARD.title;
    const titleEl = document.getElementById("pageTitle");
    if (titleEl) titleEl.textContent = DASHBOARD.title;
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
      panels.forEach((p) => p.markDirty());
    });
    document.getElementById("shiftBack").addEventListener("click", () => shift(-1));
    document.getElementById("shiftFwd").addEventListener("click", () => shift(1));
    [fromIn, toIn].forEach((el) => el.addEventListener("change", () => (quickSel.value = "custom")));

    window.addEventListener("resize", () => panels.forEach((p) => p.resize()));

    // Initial window: last 24h.
    setQuickRange(86400000);
  }

  init();
})();
