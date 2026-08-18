/* Shared ECharts building blocks used by all panel-type renderers
 * (timeseries/state-line, categorical state band, daily). Kept
 * dependency-free w.r.t. the dashboard's live state -- callers pass in
 * whatever time range they need, so these functions stay pure. */
"use strict";
import { pad, axisTimeFormatter, fmtDateTime, resolveTime } from "./time.js";

export const AXIS = "#656d76", GRID = "#eaecef", BORDER = "#d0d7de";

/* ---- shared plot geometry --------------------------------------------- */
export const GRID_TOP = 16, GRID_BOTTOM = 44, GRID_BOTTOM_NOAXIS = 10;

/* Bottom grid margin: only the one panel per group that actually renders
 * the shared x-axis tick labels (`cfg.timeAxis`) needs the full margin;
 * every other panel would otherwise carry that space as dead padding
 * (the legend no longer lives down there -- it floats over the plot). */
export const gridBottom = (cfg) => (cfg.timeAxis ? GRID_BOTTOM : GRID_BOTTOM_NOAXIS);

/* Tooltip value formatter: show at most 2 decimals for non-zero values
 * (integers and 0 stay unchanged, e.g. 0, 72, 72.53). */
export function fmtTip(v) {
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
 * since every timeseries/state panel is pinned to the same window.
 * `range` = { start, end } in epoch ms. */
export function timeXAxis(cfg, range) {
  const show = !!cfg.timeAxis;
  return {
    type: "time", min: range.start, max: range.end,
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
export const insideZoom = () => [{
  type: "inside", throttle: 60,
  zoomOnMouseWheel: true, moveOnMouseMove: false, moveOnMouseWheel: false,
}];

export function baseYAxis(cfg) {
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

export function thresholdMarkLine(sc) {
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

/* Static annotations: labelled vertical lines at fixed times (config-driven).
 * `range` = { start, end } in epoch ms, used to drop out-of-window entries. */
const ANNOTATION_COLOR = "#8250df";
function resolvedAnnotations(range) {
  return (DASHBOARD.annotations || [])
    .map((a) => ({ t: resolveTime(a.time, NaN), label: a.label, color: a.color }))
    .filter((a) => isFinite(a.t) && a.t >= range.start && a.t <= range.end);
}
function annotationMarkLine(range) {
  const list = resolvedAnnotations(range);
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
export function annotationSeries(range) {
  const markLine = annotationMarkLine(range);
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
export function floatingLegend(leftNames, rightNames, selected) {
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

/* Default palette mirrors ECharts theme; allows custom tooltip handling. */
export const DEFAULT_PALETTE = [
  "#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de",
  "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc", "#37a2da",
  "#32c5e9", "#67e0e3", "#9fe6b8", "#ffdb5c", "#ff9f7f",
  "#fb7293", "#e7bcf3", "#8378ea",
];

/* Tooltip vertical position is pinned */
export function tooltipPosition(bottomMargin) {
  return function (point, params, dom, rect, size) {
    const pad = 10;
    const cw = size.contentSize[0], ch = size.contentSize[1];
    const vw = size.viewSize[0], vh = size.viewSize[1];
    let left = point[0] + 14;
    if (left + cw + pad > vw) left = point[0] - cw - 14;
    left = Math.max(pad, Math.min(left, vw - cw - pad));
    let top = vh - bottomMargin - ch - pad;
    top = Math.max(pad, top);
    return [left, top];
  };
}

/* Current legend on/off selection read live off the chart instance*/
export function legendSelectedMap(chart) {
  if (!chart) return null;
  const opt = chart.getOption();
  const legends = (opt && opt.legend) || [];
  let merged;
  legends.forEach((lg) => {
    if (lg && lg.selected) merged = Object.assign(merged || {}, lg.selected);
  });
  return merged;
}

/* Custom tooltip formatter*/
export function axisTooltipFormatter(seriesInfo, chart) {
  return (params) => {
    if (!Array.isArray(params) || !params.length) return "";
    const t = params[0].axisValue;
    const selected = legendSelectedMap(chart);
    const rows = [];
    seriesInfo.forEach(({ data, color }, name) => {
      if (selected && selected[name] === false) return;
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
