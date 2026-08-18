/* Chart-option builder for type "daily": pre-aggregated daily data with
 * visible points, own (unsynced) X-axis. */
"use strict";
import { toXY } from "./data.js";
import { AXIS, BORDER, baseYAxis, insideZoom, thresholdMarkLine, floatingLegend, fmtTip, tooltipPosition } from "./charts.common.js";

export function buildDaily(cfg, table, legendSelected) {
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
    tooltip: {
      trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip,
      position: tooltipPosition(44),
    },
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
