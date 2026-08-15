/* Default dashboard config, consumed by the generic renderer in dashboard.js.
 * Loaded by default; select an alternate config via dashboard.html's
 * `?config=<name>` URL parameter (-> dashboard.config.<name>.js).
 *
 * Layout: rows are collapsible panel groups; a row of type "tabs" combines
 * panels into a tab strip. Each panel declares its series (metric + aggregate
 * + styling), Y-axes, thresholds and legend behaviour; metrics are rendered
 * under their short label (HR, RR, RMSSD, ...).
 *
 * This particular config reproduces the Grafana dashboard
 * `grafana-dashboard.duckdb.json` ("HRV Data").
 */
(function () {
  "use strict";

  /* Grafana named colours -> hex (approximate palette). */
  const C = {
    "dark-red": "#b30000",
    "red": "#e02f44",
    "super-light-red": "#ffa6b0",
    "light-red": "#ff7383",
    "super-light-blue": "#c0d8ff",
    "light-blue": "#6ed0e0",
    "blue": "#3274d9",
    "dark-blue": "#1f60c4",
    "green": "#56a64b",
    "dark-green": "#37872d",
    "yellow": "#fade2a",
    "super-light-yellow": "#fff899",
    "dark-yellow": "#e0b400",
    "orange": "#ff9830",
    "dark-purple": "#8f3bb8",
    "purple": "#a352cc",
    "transparent": "transparent",
  };
  const col = (c) => C[c] || c;

  const HRV = "hrv";
  const RAW = "raw";

  /* ---- Panel 1 -- Heart rate (dual axis, thresholds, moving average) ---- */
  const panel1 = {
    id: 1, type: "timeseries", title: "Heart Rate", height: 300,
    axisLeft: { label: "HR / BMP", min: 40 },
    axisRight: { label: "", min: 0, max: 1, show: false },
    legend: true,
    series: [
      { label: "HR", segment: RAW, metric: "heart_rate_generic", agg: "avg",
        color: col("super-light-red"), width: 1,
        movavg: { size: 10, label: "HR AVG 10", color: col("dark-red"), width: 2 },
        thresholds: { style: "line", steps: [
          { value: 50,  color: col("super-light-blue") },
          { value: 100, color: col("super-light-yellow") },
          { value: 150, color: col("super-light-red") },
        ] } },
      { label: "HRX", segment: RAW, metric: "heart_rate_xiaomi_activity", agg: "avg",
        color: col("super-light-red"), width: 1,
        movavg: { size: 10, label: "HRX AVG 10", color: col("light-red"), width: 1.5 } },
    ],
  };

  /* ---- Panel 2 -- Sleep stage (coloured state band) ----
   * `states` maps the raw `sleep_stage` codes to label/color/text for the
   * "state" panel renderer; code 0 ("not asleep") is left out -> blank.
   * The three "Awake" codes (1/5/6) are unified under one label/colour. */
  const AWAKE = { label: "Awake", color: "#fff899", text: "#5a4b00" };
  const panel2 = {
    id: 2, type: "state", title: "Sleep Stage", height: 120,
    axisLeft: { label: "STAGE" },
    timeAxis: true,          // only this panel renders the (shared) X time axis
    legend: true,
    series: [
      { label: "STAGE", segment: RAW, metric: "sleep_stage", agg: "none",
        color: col("dark-purple"), width: 1, fillOpacity: 40,
        states: {
          1: AWAKE, 5: AWAKE, 6: AWAKE,
          2: { label: "Deep",  color: "#1f60c4", text: "#ffffff" },
          3: { label: "Light", color: "#c0d8ff", text: "#1f2328" },
          4: { label: "REM",   color: "#ffa6b0", text: "#7a0010" },
        } },
    ],
  };

  /* ---- Panel 3 -- Dominance / Interference (dual axis, smooth) ---- */
  const panel3 = {
    id: 3, type: "timeseries", title: "Autonomic Balance", height: 240,
    axisLeft:  { label: "< Sympathikus | Vagal >", min: -1, max: 1 },
    axisRight: { label: "Interference Level", min: 0, max: 1, show: true },
    legend: true,
    series: [
      { label: "Dominance", segment: HRV, metric: "hrv_b7b8_dom", agg: "avg",
        color: col("super-light-blue"), width: 1, smooth: true,
        movavg: { size: 10, label: "Dom. AVG 10", color: col("dark-purple"),
                  width: 2, fillOpacity: 20 },
        thresholds: { style: "line", steps: [ { value: 0, color: col("green") } ] } },
      { label: "Interference", segment: HRV, metric: "hrv_b7b8_off", agg: "avg",
        color: col("yellow"), width: 1, smooth: true, axis: "right",
        movavg: { size: 10, label: "Inter. AVG 10", color: col("dark-yellow"),
                  width: 2, axis: "right" } },
    ],
  };

  /* ---- Panel 14 -- Vagal tone (dual axis, thresholds) ---- */
  const panel14 = {
    id: 14, type: "timeseries", title: "Vagal Tone", height: 260,
    axisLeft:  { label: "RMSSD / SDNN" },
    axisRight: { label: "PNN50", show: true },
    legend: true,
    series: [
      { label: "RMSSD", segment: HRV, metric: "hrv_rmssd_ms", agg: "avg",
        color: col("green"), width: 2,
        thresholds: { style: "line", steps: [
          { value: 25, color: col("yellow") },
          { value: 50, color: col("orange") },
        ] } },
      { label: "SDNN", segment: HRV, metric: "hrv_sdnn_ms", agg: "avg",
        color: col("blue"), width: 2 },
      { label: "PNN50", segment: HRV, metric: "hrv_pnn50", agg: "avg",
        color: col("super-light-red"), width: 1, axis: "right",
        movavg: { size: 10, label: "PNN50 AVG 10", color: col("red"),
                  width: 2, axis: "right" } },
    ],
  };

  /* ---- Panel 4 -- Frequency bands + DFA (dual axis, thresholds) ---- */
  const panel4 = {
    id: 4, type: "timeseries", title: "Frequency Power / DFA", height: 320,
    axisLeft:  { label: "VLF | LF | HF - ms²", abbrev: true },
    axisRight: { label: "DFA_a1", min: 0.6, max: 1.6, show: true },
    legend: true,
    series: [
      { label: "HF",   segment: HRV, metric: "hrv_hf_ms2",   agg: "avg", color: col("green") },
      { label: "LF",   segment: HRV, metric: "hrv_lf_ms2",   agg: "avg", color: col("orange") },
      { label: "VLF",  segment: HRV, metric: "hrv_vlf_ms2",  agg: "avg", color: col("super-light-blue") },
      { label: "ULF1", segment: HRV, metric: "hrv_ulf1_ms2", agg: "avg", color: col("blue") },
      { label: "ULF2", segment: HRV, metric: "hrv_ulf2_ms2", agg: "avg", color: col("dark-blue") },
      { label: "DFA",  segment: HRV, metric: "hrv_dfa_alpha1", agg: "avg",
        color: col("yellow"), width: 1, axis: "right",
        movavg: { size: 10, label: "DFA AVG", color: col("dark-yellow"), width: 2, axis: "right" },
        thresholds: { style: "line", steps: [
          { value: 0.8, color: col("red") },
          { value: 1.0, color: col("yellow") },
          { value: 1.3, color: col("light-blue") },
        ] } },
    ],
  };

  /* ---- Panel 9 -- Band circadian power (many series, HR on right) ---- */
  const bands = [
    ["CIRC24", "hrv_band_circ_24h"], ["CIRC11", "hrv_band_circ_11h"],
    ["CIRC6", "hrv_band_circ_6h"],   ["CIRC5", "hrv_band_circ_5h"],
    ["CIRC4", "hrv_band_circ_4h"],   ["ULF22", "hrv_band_ulf_22min"],
    ["ULF10", "hrv_band_ulf_10min"], ["ULF8", "hrv_band_ulf_8min"],
    ["VLF5", "hrv_band_vlf_5min"],   ["VLF4", "hrv_band_vlf_4min"],
    ["LF_MAYER", "hrv_band_lf_mayer_10s"],
    ["HF5", "hrv_band_hf_breath_5s"], ["HF4", "hrv_band_hf_breath_4s"],
    ["HF3", "hrv_band_hf_breath_3s"], ["HF2", "hrv_band_hf_breath_2s"],
  ];
  const panel9 = {
    id: 9, type: "timeseries", title: "Circadian Band Power", height: 340,
    axisLeft:  { label: "Power" },
    axisRight: { label: "N Beats", show: true },
    legend: true,
    series: [
      { label: "N Beats", segment: HRV, metric: "hrv_n_beats", agg: "avg",
        color: "#fdced4", width: 0.5, axis: "right" },
    ].concat(bands.map(([label, metric]) => ({
      label, segment: HRV, metric, agg: "avg", width: 1,
    }))),
  };

  /* ---- Panel 15 -- CPC / HF-Peak (dual axis, thresholds, moving average) ---- */
  const panel15 = {
    id: 15, type: "timeseries", title: "Cardiopulmonary Coupling", height: 320,
    axisLeft:  { label: "CPC" },
    axisRight: { label: "HF Peak", show: true },
    legend: true,
    series: [
      { label: "CPC", segment: HRV, metric: "hrv_cpc_lfc_ratio", agg: "avg",
        color: col("super-light-blue"), width: 1,
        movavg: { size: 5, label: "CPC AVR 5", color: col("blue"), width: 2 },
        thresholds: { style: "line", steps: [
          { value: 0.3, color: col("light-blue") },
          { value: 0.5, color: col("yellow") },
          { value: 0.8, color: col("red") },
        ] } },
      { label: "HF Peak", segment: HRV, metric: "hrv_hf_peak_stability", agg: "avg",
        color: col("super-light-red"), width: 1, axis: "right",
        movavg: { size: 5, label: "HF Peak AVR 5", color: col("red"), width: 2, axis: "right" } },
    ],
  };

  /* ---- Panel 16 -- RR interval + relative spread (dual axis, thresholds) ---- */
  const panel16 = {
    id: 16, type: "timeseries", title: "RR Interval", height: 320,
    axisLeft:  { label: "RR", min: 400, max: 1800 },
    axisRight: { label: "Spread Rel", min: 0, max: 5, show: true },
    legend: true,
    series: [
      { label: "RR", segment: RAW, metric: "rr_interval_ms", agg: "avg",
        color: col("dark-red"), width: 1,
        thresholds: { style: "dashed", steps: [
          { value: 500,  color: col("red") },
          { value: 1700, color: col("red") },
        ] } },
      { label: "Spread Rel", segment: RAW, metric: "rr_interval_ms", agg: "spread",
        color: col("super-light-red"), width: 1, axis: "right" },
    ],
  };

  /* ---- Panels 6/7/8 -- daily line charts (pre-aggregated backend queries) */
  const panel6 = {
    id: 6, type: "daily", title: "Sympathic Dominance Time under threshold",
    height: 320, kind: "dominance_daily",
    range: { days: 14 },      // rolling last 14 days, independent of the global range
    axisLeft: { label: "Σ (value + 0.5)" }, legend: true,
    series: [
      { label: "Dominance Time", column: "value", color: col("green"),
        thresholds: { style: "line", steps: [ { value: -80, color: col("red") } ] } },
    ],
  };
  const sleepSeries = [
    { label: "phases", column: "phases", color: col("green"), max: 50 },
    { label: "deep",   column: "deep",   color: col("blue"),  max: 50 },
    { label: "rem",    column: "rem",    color: col("red"),   max: 50 },
  ];
  const panel7 = {
    id: 7, type: "daily", title: "Sleep Phases (bed < 2026-01-01)",
    height: 320, kind: "sleep_daily", session: "before",
    // Own fixed window: all sleep sessions up to the 2026-01-01 split.
    range: { from: "2000-01-01T00:00:00Z", to: "2026-01-01T00:00:00Z" },
    axisLeft: { label: "count", min: 0, max: 50 }, legend: true,
    series: sleepSeries,
  };
  const panel8 = {
    id: 8, type: "daily", title: "Sleep Phases (bed > 2026-01-01)",
    height: 320, kind: "sleep_daily", session: "after",
    // Own fixed window: all sleep sessions from the 2026-01-01 split onward.
    range: { from: "2026-01-01T00:00:00Z", to: "now" },
    axisLeft: { label: "count", min: 0, max: 50 }, legend: true,
    series: sleepSeries,
  };

  /* ---- Dashboard layout (rows + tabs) ---- */
  window.DASHBOARD = {
    title: "HRV Data",
    rows: [
      { title: "Main",     type: "grid", collapse: false, panels: [panel1, panel2] },
      { title: "Typical",  type: "grid", collapse: false, panels: [panel3, panel14] },
      { title: "Extended", type: "tabs", collapse: false, tabs: [
        { title: "DFA",         panels: [panel4] },
        { title: "Frequencies", panels: [panel9] },
        { title: "Overall",     panels: [panel6, panel7, panel8] },
        { title: "REM",         panels: [panel15] },
        { title: "RR",          panels: [panel16] },
      ] },
    ],
  };
})();
