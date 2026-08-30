/* Panel -- one dashboard card with lazy (visibility-based) loading, the
 * drag-zoom/pan interaction, and dispatch to the right chart-option builder
 * (or plain-DOM renderer, for "flag"/"tiles") based on the panel's
 * `cfg.type`. */
"use strict";
import {
  bump, getRange, getZoomWindow, setZoomWindow, isSyncing,
  broadcastZoom, broadcastShowAtValue, broadcastHide,
  adoptWindow, livePan, maxPointsOverride,
} from "./controls.js";
import { seriesData, cachedFetchTable, latestValue } from "./data.js";
import { panelRange } from "./time.js";
import { GRID_TOP, gridBottom, fmtTip, ALL_LEGEND_LABEL } from "./charts.common.js";
import { buildTimeseries } from "./charts.timeseries.js";
import { buildStateBand } from "./charts.stateband.js";
import { buildDaily } from "./charts.daily.js";
import { renderFlagPanel, tileAccent, TILE_CTX } from "./panels.flags.js";

/* max_points default for regular (non-daily) series queries. */
const DEFAULT_MAX_POINTS = 3000;

export class Panel {
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

    this.chart.on("legendselectchanged", (params) => this.syncAllLegendEntry(params));

    if (this.cfg.type === "daily") return;  // keep own X-axis

    this.chart.on("datazoom", () => {
      if (isSyncing()) return;
      const dz = (this.chart.getOption().dataZoom || [])[0];
      if (!(dz && dz.startValue != null && dz.endValue != null)) return;
      setZoomWindow({ s: dz.startValue, e: dz.endValue });
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

  /* Two-way sync for the pseudo "All" legend */
  syncAllLegendEntry(params) {
    if (this._legendSyncing) return;
    const names = [];
    (this.chart.getOption().legend || []).forEach((lg) =>
      (lg.data || []).forEach((n) => { if (n !== ALL_LEGEND_LABEL) names.push(n); }));
    if (!names.length) return;
    this._legendSyncing = true;
    try {
      if (params.name === ALL_LEGEND_LABEL) {
        const turnOn = params.selected[ALL_LEGEND_LABEL];
        names.forEach((n) => {
          if ((params.selected[n] !== false) !== turnOn) {
            this.chart.dispatchAction({ type: turnOn ? "legendSelect" : "legendUnSelect", name: n });
          }
        });
      } else if (ALL_LEGEND_LABEL in params.selected) {
        const allOn = names.every((n) => params.selected[n] !== false);
        if ((params.selected[ALL_LEGEND_LABEL] !== false) !== allOn) {
          this.chart.dispatchAction({ type: allOn ? "legendSelect" : "legendUnSelect", name: ALL_LEGEND_LABEL });
        }
      }
    } finally {
      this._legendSyncing = false;
    }
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

    const finishDrag = (e) => {
      if (!drag) return;
      const d = drag; drag = null;
      try { el.releasePointerCapture(e.pointerId); } catch (_) {}
      sel.style.display = "none";
      if (!d.moved) return;
      const { start: rangeStart, end: rangeEnd } = getRange();
      if (d.button === 0) {         // adopt selected span
        const a = chart.convertFromPixel({ xAxisIndex: 0 }, Math.min(d.startPx, d.curPx));
        const b = chart.convertFromPixel({ xAxisIndex: 0 }, Math.max(d.startPx, d.curPx));
        adoptWindow(Math.max(rangeStart, Math.min(a, b)), Math.min(rangeEnd, Math.max(a, b)));
      } else if (d.off) {           // adopt panned window
        adoptWindow(rangeStart + d.off, rangeEnd + d.off);
      }
    };
    el.addEventListener("pointerup", finishDrag);
    el.addEventListener("pointercancel", finishDrag);
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
      const range = getRange();
      if (cfg.type === "flag") {
        const maxPoints = maxPointsOverride(DEFAULT_MAX_POINTS);
        const results = await Promise.all(cfg.series.map(async (sc) =>
          ({ sc, data: await seriesData(sc, range, maxPoints) })));
        renderFlagPanel(this.chartEl, cfg, results);
      } else if (cfg.type === "tiles") {
        await this.loadTiles();
      } else if (cfg.type === "daily") {
        const { start, end } = panelRange(cfg, range);
        const table = await cachedFetchTable({
          kind: cfg.kind, session: cfg.session,
          start, end, max_points: maxPointsOverride(2000),
        });
        this.chart.setOption(buildDaily(cfg, table, legendSel), true);
      } else {
        const maxPoints = maxPointsOverride(DEFAULT_MAX_POINTS);
        const map = new Map();
        await Promise.all(cfg.series.map(async (sc) => {
          map.set(sc, await seriesData(sc, range, maxPoints));
        }));
        if (cfg.type === "state") {
          this.chart.setOption(buildStateBand(cfg, map.get(cfg.series[0]), range), true);
        } else {
          this.chart.setOption(
            buildTimeseries(cfg, { get: (k) => map.get(k) }, legendSel, range, this.chart), true);
        }
      }
      this.loaded = true;
      // Replay the current synced zoom onto this freshly-loaded panel.
      const zoomWindow = getZoomWindow();
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
    const range = getRange();
    const maxPoints = maxPointsOverride(DEFAULT_MAX_POINTS);
    await Promise.all(this.cfg.tiles.map(async (t, i) => {
      const valueEl = this.tileEls[i].valueEl;
      if (!valueEl) return;
      try {
        const v = latestValue(await seriesData(t.series, range, maxPoints));
        valueEl.textContent = v == null ? "—" :
          (t.format ? t.format(v) : fmtTip(v) + (t.unit ? " " + t.unit : ""));
      } catch (e) {
        valueEl.textContent = "—";
      }
    }));
  }

  resize() { if (this.chart) this.chart.resize(); }
}
