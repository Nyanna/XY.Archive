/* HR Viewer dashboard.
 *
 * Posts a query to the DuckDB-backed API and receives the time series as an
 * Apache Arrow IPC stream, decodes it with apache-arrow (vendored globally as
 * `Arrow`) and renders it with ECharts as a line chart. A global selector
 * controls the time range (default: last 24h). The metric is fixed to
 * `heart_rate_generic`.
 */
(function () {
  "use strict";

  const METRIC = "heart_rate_generic";
  const SEGMENT = "raw";

  const chartEl = document.getElementById("chart");
  const rangeSel = document.getElementById("range");
  const reloadBtn = document.getElementById("reload");
  const statusEl = document.getElementById("status");

  const chart = echarts.init(chartEl);
  window.addEventListener("resize", () => chart.resize());

  function setStatus(msg) {
    statusEl.textContent = msg || "";
  }

  /* Decode an Arrow IPC stream into an ECharts `[ [tsMs, value], ... ]` array. */
  function arrowToSeries(buffer) {
    const table = Arrow.tableFromIPC(new Uint8Array(buffer));
    const tsCol = table.getChild("ts");
    const valCol = table.getChild("value");
    const n = table.numRows;
    const data = new Array(n);
    for (let i = 0; i < n; i++) {
      const t = tsCol.get(i); // BigInt (epoch ms)
      const v = valCol.get(i);
      data[i] = [Number(t), v === null ? null : Number(v)];
    }
    return data;
  }

  async function load() {
    const rangeMs = parseInt(rangeSel.value, 10);
    const end = Date.now();
    const start = end - rangeMs;

    setStatus("Loading …");
    const t0 = performance.now();
    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ segment: SEGMENT, metric: METRIC, start, end, format: "arrow" }),
      });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const buf = await res.arrayBuffer();
      const data = arrowToSeries(buf);
      render(METRIC, data);
      const dt = (performance.now() - t0).toFixed(0);
      setStatus(data.length + " points · " + dt + " ms");
    } catch (e) {
      setStatus("Error: " + e.message);
      render(METRIC, []);
    }
  }

  function render(metric, data) {
    chart.setOption(
      {
        backgroundColor: "transparent",
        animation: false,
        textStyle: { color: "#1f2328" },
        title: { text: metric, left: 12, top: 8, textStyle: { fontSize: 13, fontWeight: 600, color: "#656d76" } },
        tooltip: { trigger: "axis", axisPointer: { type: "line" } },
        grid: { left: 56, right: 24, top: 48, bottom: 64 },
        xAxis: {
          type: "time",
          axisLine: { lineStyle: { color: "#d0d7de" } },
          axisLabel: { color: "#656d76" },
        },
        yAxis: {
          type: "value",
          scale: true,
          axisLabel: { color: "#656d76" },
          splitLine: { lineStyle: { color: "#eaecef" } },
        },
        dataZoom: [
          { type: "inside", throttle: 50 },
          { type: "slider", height: 22, bottom: 24 },
        ],
        series: [
          {
            name: metric,
            type: "line",
            showSymbol: false,
            sampling: "lttb",
            lineStyle: { width: 1.5, color: "#0969da" },
            areaStyle: { opacity: 0.06, color: "#0969da" },
            data: data,
          },
        ],
      },
      true
    );
  }

  reloadBtn.addEventListener("click", load);
  rangeSel.addEventListener("change", load);

  load();
})();
