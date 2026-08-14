/* HRV Data dashboard -- reproduction of the Grafana dashboard.
 *
 * Implemented features:
 *   - globally synchronised zoom and hover cursor across all panels, matched
 *     by axis value (not data index) so panels with differing point densities
 *     stay aligned, plus late-join zoom replay,
 *   - a time selector with start/end date+time inputs and shift buttons that
 *     move the selected window backward/forward by its own span,
 *   - lazy panel loading: a panel only queries data once it becomes visible
 *     (collapsed groups and inactive tabs stay unloaded),
 *   - selectable aggregate per query (avg / none / relative spread),
 *   - thresholds drawn as marker lines,
 *   - dual Y-axes with independent min/max (and transparent stacked fills),
 *   - a legend to toggle individual metric series,
 *   - collapsible panel groups and a combined tab-panel,
 *   - metrics shown under their short label, with axis labels.
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

  /* ---- cross-panel sync BY AXIS VALUE --------------------------------- *
   * `echarts.connect` links the tooltip/axisPointer by *data index*, which
   * misaligns panels whose series have different point counts (dense HR vs.
   * sparse sleep_stage). We therefore sync zoom and the hover cursor manually,
   * by time value. The Overall-tab bar charts (daily aggregates, own X-axis)
   * are excluded. */
  const syncable = (p) => p.chart && p.cfg.type !== "bar";

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

  function syncInputs() {
    fromIn.value = fmtLocal(fromMs);
    toIn.value = fmtLocal(toMs);
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
      axisLabel: { color: AXIS }, splitLine: { lineStyle: { color: GRID } },
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

  /* Build the ECharts option for a timeseries / state panel from fetched data.
   * `fetched` maps a series config -> its [[ts,val], ...] array. */
  function buildTimeseries(cfg, fetched) {
    const legendData = [];
    const series = [];
    cfg.series.forEach((sc) => {
      const yIdx = sc.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
      const data = fetched.get(sc);
      const step = cfg.type === "state" ? "end" : false;
      legendData.push(sc.label);
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
        legendData.push(m.label);
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
    return {
      backgroundColor: "transparent", animation: false,
      textStyle: { color: "#1f2328" },
      tooltip: { trigger: "axis", axisPointer: { type: "line" } },
      legend: cfg.legend ? {
        type: "scroll", bottom: 0, data: legendData, textStyle: { color: AXIS },
        icon: "roundRect",
      } : undefined,
      // Keep the plot geometry identical across every timeseries/state panel
      // (constant left/right margins) so that, with the shared X-axis range,
      // a given timestamp maps to the same pixel X in every panel. Otherwise
      // panels without a right axis (HR, Sleep Stage) would be wider than the
      // rest and the connected hover axisPointer/tooltip would be offset.
      grid: { left: 64, right: 64, top: 16, bottom: 52 },
      xAxis: {
        // Pin the axis to the selected query window so every timeseries/state
        // panel shares the exact same X-axis (e.g. the sparse `sleep_stage`
        // data no longer auto-scales to its own narrow span and stays aligned
        // with the other panels). The Overall-tab bar charts use `buildBar`
        // and keep their own daily-aggregate X-axis.
        type: "time", min: fromMs, max: toMs,
        axisLine: { lineStyle: { color: BORDER } },
        axisLabel: { color: AXIS },
      },
      yAxis: baseYAxis(cfg),
      dataZoom: [
        { type: "inside", throttle: 60 },
        { type: "slider", height: 16, bottom: 30 },
      ],
      series,
    };
  }

  /* ---- Sleep-stage state band (Grafana-style state timeline) ---------- *
   * `sleep_stage` is a categorical signal. Instead of a step line we render a
   * single-row colour band: runs of the same stage become coloured rectangles
   * that span their time range, each labelled with the stage name.
   * Value mapping mirrors the Grafana dashboard (grafana-dashboard.duckdb.json);
   * the four "Awake" codes (1/5/6, and transparent 0) are unified, code 0
   * ("not asleep") is left blank. */
  const STAGE = {
    0: null,                                             // Awake / transparent -> blank
    1: { label: "Awake", color: "#fff899", text: "#5a4b00" },
    2: { label: "Deep",  color: "#1f60c4", text: "#ffffff" },
    3: { label: "Light", color: "#c0d8ff", text: "#1f2328" },
    4: { label: "REM",   color: "#ffa6b0", text: "#7a0010" },
    5: { label: "Awake", color: "#fff899", text: "#5a4b00" },
    6: { label: "Awake", color: "#fff899", text: "#5a4b00" },
  };

  /* Collapse the [ts,value] points into [start, end, code] segments, breaking
   * runs across long gaps (e.g. between separate nights) so no rectangle is
   * stretched over daytime with no data. */
  function buildStageSegments(xy) {
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
      if (STAGE[code] && end > start) segs.push([start, end, code]);
      i = j;
    }
    return segs;
  }

  /* Custom renderItem: draw one clipped, labelled rectangle per stage run. */
  function renderStageItem(params, api) {
    const m = STAGE[api.value(2)];
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
  }

  function buildStateBand(cfg, xy) {
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
          const v = it.value, m = STAGE[v[2]];
          const dur = Math.round((v[1] - v[0]) / 60000);
          return "<b>" + (m ? m.label : v[2]) + "</b><br/>" +
            fmt(v[0]) + " – " + fmt(v[1]) + " · " + dur + " min";
        },
      },
      grid: { left: 64, right: 64, top: 16, bottom: 52 },
      xAxis: {
        type: "time", min: fromMs, max: toMs,
        axisLine: { lineStyle: { color: BORDER } },
        axisLabel: { color: AXIS },
      },
      yAxis: {
        type: "value", min: 0, max: 1,
        name: (cfg.axisLeft && cfg.axisLeft.label) || "",
        nameLocation: "middle", nameGap: 42, nameTextStyle: { color: AXIS },
        axisLine: { show: false }, axisTick: { show: false },
        axisLabel: { show: false }, splitLine: { show: false },
      },
      dataZoom: [
        { type: "inside", throttle: 60 },
        { type: "slider", height: 16, bottom: 30 },
      ],
      series: [{
        type: "custom", renderItem: renderStageItem,
        encode: { x: [0, 1] }, clip: true,
        data: buildStageSegments(xy),
      }],
    };
  }

  function buildBar(cfg, table) {
    const legendData = [], series = [];
    cfg.series.forEach((sc) => {
      legendData.push(sc.label);
      series.push({
        name: sc.label, type: "bar", data: toXY(table, sc.column),
        itemStyle: { color: sc.color }, barMaxWidth: 14,
        markLine: thresholdMarkLine(sc),
      });
    });
    return {
      backgroundColor: "transparent", animation: false,
      tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
      legend: cfg.legend ? { bottom: 0, data: legendData, textStyle: { color: AXIS } } : undefined,
      grid: { left: 56, right: 24, top: 16, bottom: 52 },
      xAxis: { type: "time", axisLabel: { color: AXIS }, axisLine: { lineStyle: { color: BORDER } } },
      yAxis: baseYAxis(cfg),
      dataZoom: [
        { type: "inside", throttle: 60 },
        { type: "slider", height: 16, bottom: 30 },
      ],
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
      const title = document.createElement("div");
      title.className = "panel-title";
      title.textContent = cfg.title || "";
      const chartEl = document.createElement("div");
      chartEl.className = "panel-chart";
      host.appendChild(title);
      host.appendChild(chartEl);
      this.host = host;
      this.chartEl = chartEl;
    }

    ensureChart() {
      if (this.chart) return;
      this.chart = echarts.init(this.chartEl);

      // The Overall-tab bar charts keep their own independent X-axis and are
      // not part of the cross-panel cursor/zoom synchronisation.
      if (this.cfg.type === "bar") return;

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
    }

    markDirty() {
      this.dirty = true;
      if (this.visible) this.load();
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
        if (cfg.type === "bar") {
          const table = await fetchTable({
            kind: cfg.kind, session: cfg.session,
            start: fromMs, end: toMs, max_points: 2000,
          });
          this.chart.setOption(buildBar(cfg, table), true);
        } else {
          const map = new Map();
          await Promise.all(cfg.series.map(async (sc) => {
            const table = await fetchTable({
              kind: "series", segment: sc.segment, metric: sc.metric,
              agg: sc.agg || "avg", start: fromMs, end: toMs, max_points: 3000,
            });
            map.set(sc, toXY(table, "value"));
          }));
          if (cfg.type === "state") {
            this.chart.setOption(buildStateBand(cfg, map.get(cfg.series[0])), true);
          } else {
            this.chart.setOption(buildTimeseries(cfg, { get: (k) => map.get(k) }), true);
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

  function buildTabs(container, tabs) {
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
      btn.addEventListener("click", () => {
        bar.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        bodies.forEach((b) => (b.style.display = "none"));
        body.style.display = "";
        // Panels in the newly shown tab become visible -> observer loads them.
        requestAnimationFrame(() => panels.forEach((p) => p.resize()));
      });
      bar.appendChild(btn);
      bodies.push(body);
    });
    container.appendChild(bar);
    bodies.forEach((b) => container.appendChild(b));
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
    if (rowCfg.type === "tabs") buildTabs(content, rowCfg.tabs);
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

  /* ---- wire up -------------------------------------------------------- */
  function init() {
    document.title = DASHBOARD.title;
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
    document.getElementById("shiftBack").addEventListener("click", () => shift(-1));
    document.getElementById("shiftFwd").addEventListener("click", () => shift(1));
    [fromIn, toIn].forEach((el) => el.addEventListener("change", () => (quickSel.value = "custom")));

    window.addEventListener("resize", () => panels.forEach((p) => p.resize()));

    // Initial window: last 24h.
    setQuickRange(86400000);
  }

  init();
})();
