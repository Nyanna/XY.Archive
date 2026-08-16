/* ECharts option builder for "timeseries" panels (plain line/area charts,
 * optionally with a step-line "state" variant, on the shared synced time
 * axis). */
"use strict";
import { movingAverage } from "./data.js";
import {
  GRID_TOP, gridBottom, timeXAxis, insideZoom, baseYAxis,
  thresholdMarkLine, annotationSeries, floatingLegend,
  DEFAULT_PALETTE, axisTooltipFormatter,
} from "./charts.common.js";

/* Build the ECharts option for a timeseries / state panel from fetched data.
 * `fetched.get(sc)` returns the [[ts,val], ...] array for a series config;
 * `range` = { start, end } in epoch ms (the panel's current query window). */
export function buildTimeseries(cfg, fetched, legendSelected, range) {
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
  series.push(...annotationSeries(range));
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
    xAxis: timeXAxis(cfg, range),
    yAxis: baseYAxis(cfg),
    dataZoom: insideZoom(),
    series,
  };
}
