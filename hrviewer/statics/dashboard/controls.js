/* Global time-window state, cross-panel zoom/hover sync, and the range /
 * auto-refresh controls in the top bar. This is the one module allowed to
 * hold mutable "current state" (time window, zoom, panel registry); every
 * other module reads/receives it through the functions exported here. */
"use strict";
import { fmtLocal, parseLocal } from "./time.js";
import { clearQueryCache } from "./data.js";

const statusEl = document.getElementById("status");
const quickSel = document.getElementById("quickRange");
const fromIn = document.getElementById("fromInput");
const toIn = document.getElementById("toInput");
const maxPointsIn = document.getElementById("maxPointsInput");
const autoRefreshIn = document.getElementById("autoRefresh");
const historyBtn = document.getElementById("historyBack");

let fromMs, toMs;
let zoomWindow = null;          // {s,e} in ms -- current synced zoom, or null
let syncing = false;            // re-entrancy guard for zoom broadcasting
let pending = 0;

/* ---- navigation history -----------------------------------------------
 * Every explicit range/resolution/selection-zoom change pushes the state it
 * replaces onto a stack; `historyBack()` pops and restores it. Auto-refresh
 * and the "Reset" zoom button don't push (they're not user navigation). */
const historyStack = [];
let prevSnapshot = null;        // settings as of the last commit(), i.e. "current"

function snapshot() {
  return {
    fromMs, toMs, quick: quickSel.value, maxPoints: maxPointsIn.value,
    zoomWindow: zoomWindow ? { s: zoomWindow.s, e: zoomWindow.e } : null,
  };
}
/* Call once a change has been fully applied, so the next pushHistory() has
 * an accurate "state before this change" to save. */
function commit() { prevSnapshot = snapshot(); }

function updateHistoryButton() {
  if (historyBtn) historyBtn.disabled = historyStack.length === 0;
}

/* Call right before starting a user-triggered range/resolution/zoom change. */
function pushHistory() {
  if (!prevSnapshot) return;
  historyStack.push(prevSnapshot);
  updateHistoryButton();
}

function restoreSnapshot(s) {
  fromMs = s.fromMs; toMs = s.toMs;
  quickSel.value = s.quick;
  maxPointsIn.value = s.maxPoints;
  syncInputs();
  zoomWindow = s.zoomWindow ? { s: s.zoomWindow.s, e: s.zoomWindow.e } : null;
  clearQueryCache();
  panels.forEach((p) => p.markDirty());
  commit();
}

export function historyBack() {
  const s = historyStack.pop();
  if (!s) return;
  updateHistoryButton();
  restoreSnapshot(s);
}

export const panels = [];       // all Panel instances
export function registerPanel(p) { panels.push(p); }

export function getRange() { return { start: fromMs, end: toMs }; }
export function getZoomWindow() { return zoomWindow; }
export function setZoomWindow(w) { zoomWindow = w; }
export function isSyncing() { return syncing; }

export function setStatus(msg) { statusEl.textContent = msg || ""; }
export function bump(d) {
  pending = Math.max(0, pending + d);
  setStatus(pending > 0 ? "Loading … (" + pending + ")" : "Ready");
}

/* Global "max_points" override for all panels; empty leaves each query's default untouched. */
export function maxPointsOverride(dflt) {
  const v = parseInt(maxPointsIn.value, 10);
  return Number.isFinite(v) && v > 0 ? v : dflt;
}

/* ---- cross-panel sync BY AXIS VALUE ----------------------------------
 * `echarts.connect` links by *data index*, which misaligns panels whose
 * series have different point counts. We sync zoom/hover manually instead,
 * by time value. Panels of type "daily" (own X-axis) are excluded. */
const syncable = (p) => p.chart && p.cfg.type !== "daily";

export function broadcastShowAtValue(t) {
  panels.forEach((p) => {
    if (!syncable(p) || !p.loaded) return;
    const x = p.chart.convertToPixel({ xAxisIndex: 0 }, t);
    if (x == null || isNaN(x)) return;
    p.chart.dispatchAction({ type: "showTip", x, y: p.chart.getHeight() / 2 });
  });
}
export function broadcastHide() {
  panels.forEach((p) => { if (syncable(p)) p.chart.dispatchAction({ type: "hideTip" }); });
}
export function broadcastZoom(source) {
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

function syncInputs() {
  fromIn.value = fmtLocal(fromMs);
  toIn.value = fmtLocal(toMs);
}

/* ---- range application ---------------------------------------------- */
export function applyRange() {
  fromMs = parseLocal(fromIn.value);
  toMs = parseLocal(toIn.value);
  if (!(fromMs < toMs)) { setStatus("Invalid range"); return; }
  zoomWindow = null;                       // fresh data -> reset synced zoom
  clearQueryCache();                       // drop shared query results for the old window
  panels.forEach((p) => p.markDirty());    // visible ones reload immediately
  commit();
}

export function setQuickRange(spanMs) {
  toMs = Date.now();
  fromMs = toMs - spanMs;
  syncInputs();
  applyRange();
}

export function shift(dir) {
  const span = toMs - fromMs;
  fromMs += dir * span;
  toMs += dir * span;
  syncInputs();
  applyRange();
}

export function resetZoom() {
  zoomWindow = null;
  panels.forEach((p) => {
    if (p.chart) p.chart.dispatchAction({ type: "dataZoom", start: 0, end: 100 });
  });
  commit();                                // keep bookkeeping accurate, but not a history entry
}

/* Live pan feedback: shift the X window of every synced, loaded panel by an
 * offset (ms) without re-querying -- used while a right-drag is in flight. */
export function livePan(off) {
  panels.forEach((p) => {
    if (syncable(p) && p.loaded)
      p.chart.setOption({ xAxis: { min: fromMs + off, max: toMs + off } });
  });
}

export function adoptWindow(start, end) {
  if (!(end - start > 1000)) return;       // ignore accidental micro-drags
  pushHistory();                           // remember the window this selection-zoom replaces
  fromMs = start; toMs = end;
  syncInputs();
  quickSel.value = "custom";
  applyRange();                            // resets zoom + reloads at new res.
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

/* ---- wire up top-bar controls ---------------------------------------- */
export function initControls() {
  quickSel.addEventListener("change", () => {
    if (quickSel.value === "custom") return;
    pushHistory();
    setQuickRange(parseInt(quickSel.value, 10));
  });
  document.getElementById("apply").addEventListener("click", () => {
    pushHistory();
    quickSel.value = "custom"; applyRange();
  });
  document.getElementById("resetZoom").addEventListener("click", resetZoom);
  if (historyBtn) historyBtn.addEventListener("click", historyBack);
  maxPointsIn.addEventListener("change", () => {
    pushHistory();
    clearQueryCache();                     // resolution changed -> re-query
    panels.forEach((p) => p.markDirty());
    commit();
  });
  document.getElementById("shiftBack").addEventListener("click", () => { pushHistory(); shift(-1); });
  document.getElementById("shiftFwd").addEventListener("click", () => { pushHistory(); shift(1); });
  [fromIn, toIn].forEach((el) => el.addEventListener("change", () => (quickSel.value = "custom")));

  window.addEventListener("resize", () => panels.forEach((p) => p.resize()));

  // Initial window: last 24h.
  setQuickRange(86400000);

  // Keep rolling "Last *" ranges live (every 15s).
  startAutoRefresh();
}
