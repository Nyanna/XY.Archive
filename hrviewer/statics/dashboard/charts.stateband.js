/* Categorical state band renderer: converts a series into time-range
 * segments and draws them as clipped, labelled rectangles via a custom
 * ECharts series (`type: "custom"`). */
"use strict";
import { pad } from "./time.js";
import { AXIS, GRID_TOP, gridBottom, timeXAxis, insideZoom, annotationSeries } from "./charts.common.js";

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

/* `range` = { start, end } in epoch ms (the panel's current query window). */
export function buildStateBand(cfg, xy, range) {
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
    xAxis: timeXAxis(cfg, range),
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
    }, ...annotationSeries(range)],
  };
}
