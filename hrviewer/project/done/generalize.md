Prüfe die Generalisierbarkeit und komprimiere die Kommentare.
Die Dashboard-Implementierung soll als Basis für weitere Dashboards dienen. Prüfe daher, ob die Komponenten sauber voneinander isoliert sind. CSS soll für alle zukünftigen gemeinsam verwendet werden können.

* `dashboard.html` soll auf Basis eines URL-Parameters eine andere Config laden können; Default ist die aktuelle config.

- HTML: `/home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html`
- Config: `/home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js`
- Implementierung: `/home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js`
SystemInit:  id=98219d96-91e2-4d36-a120-83cfd3b0f45b, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: 0ffcaa79-ad18-453f-bf62-6215af774f52
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html
  reason: Review dashboard.html
```
/answer 0ffcaa79-ad18-453f-bf62-6215af774f52 allow
Control Request:
```yaml
id: fc86a5dd-73e1-4b1b-9dd8-19344ef3c499
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  reason: Review dashboard.config.js
```
/answer fc86a5dd-73e1-4b1b-9dd8-19344ef3c499 allow
Control Request:
```yaml
id: 9aecc644-a2c0-45b6-8813-ceb8d5d9a566
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  reason: Review dashboard.js
```
/answer 9aecc644-a2c0-45b6-8813-ceb8d5d9a566 allow
ReasoningToken: 12
Control Request:
```yaml
id: acb69fa9-5eba-4570-82e2-b9740985e277
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics
  reason: See all static files
```
/answer acb69fa9-5eba-4570-82e2-b9740985e277 allow
Control Request:
```yaml
id: bb4e3140-b6de-4ec2-bb09-8b8fd4713c5e
result:
  structuredContent:
    entries:
    - Arrow.es2015.min.js
    - app.js
    - dashboard.config.js
    - dashboard.css
    - dashboard.html
    - dashboard.js
    - echarts.min.js
    - index.html
    - style.css
```
/answer bb4e3140-b6de-4ec2-bb09-8b8fd4713c5e allow
Control Request:
```yaml
id: 40cdbbc4-e298-4693-a96b-2c397b43a874
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer
  reason: See project structure for server/static serving
```
/answer 40cdbbc4-e298-4693-a96b-2c397b43a874 deny konzentriere dich allein auf die statics
ReasoningToken: 45
Control Request:
```yaml
id: 54bec96d-da3f-4e35-a7cd-edecdbcd788e
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.css
  reason: Check CSS for generic reusability
```
/answer 54bec96d-da3f-4e35-a7cd-edecdbcd788e allow
ReasoningToken: 49
Control Request:
```yaml
id: 757923a1-a353-40df-8a2a-8ae2baa71ddf
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html
  old_text: |2-
      <header class="topbar">
        <h1>HRV&nbsp;Data</h1>
  new_text: |2-
      <header class="topbar">
        <h1 id="pageTitle">HRV&nbsp;Data</h1>
  reason: Add id so JS can set the title generically per config
```
/answer 757923a1-a353-40df-8a2a-8ae2baa71ddf allow
Control Request:
```yaml
id: f1accbf0-837b-4c8a-83e7-c03073f23f8e
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html
  old_text: |2-
      <script src="dashboard.config.js"></script>
      <script src="dashboard.js"></script>
    </body>
    </html>
  new_text: |2-
      <script>
        /* Pick the dashboard config to load. `?config=<name>` loads
         * "dashboard.config.<name>.js"; with no (or an invalid) parameter, the
         * default "dashboard.config.js" is used. This is how dashboard.js -- a
         * generic renderer -- gets reused for multiple dashboards. */
        (function () {
          "use strict";
          var raw = new URLSearchParams(location.search).get("config");
          var name = raw && /^[a-zA-Z0-9_-]+$/.test(raw) ? raw : null;
          var configSrc = name ? "dashboard.config." + name + ".js" : "dashboard.config.js";

          function loadScript(src) {
            return new Promise(function (resolve, reject) {
              var s = document.createElement("script");
              s.src = src;
              s.onload = resolve;
              s.onerror = function () { reject(new Error("failed to load " + src)); };
              document.head.appendChild(s);
            });
          }

          Promise.resolve()
            .then(function () { return loadScript(configSrc); })
            .catch(function () {
              return configSrc === "dashboard.config.js"
                ? Promise.reject()
                : loadScript("dashboard.config.js"); // unknown config -> fall back to default
            })
            .then(function () { return loadScript("dashboard.js"); })
            .catch(function (e) {
              document.getElementById("status").textContent = "Config error: " + (e && e.message || e);
            });
        })();
      </script>
    </body>
    </html>
  reason: "Load config selected via ?config= URL param, defaulting to dashboard.config.js"
```
/answer f1accbf0-837b-4c8a-83e7-c03073f23f8e allow
ReasoningToken: 6622
Control Request:
```yaml
id: c2c13d9d-3635-4a91-a9b4-ec28494aefc8
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |-
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
  new_text: |-
    /* Generic ECharts dashboard renderer, driven entirely by a `window.DASHBOARD`
     * config (see dashboard.config.js). Not tied to any specific metrics or
     * domain -- a new dashboard only needs its own config file, selected via
     * dashboard.html's `?config=` URL parameter.
     *
     * Features: synced zoom/hover cursor across panels (by axis value, not data
     * index, plus late-join replay), a time selector with quick ranges + shift
     * buttons, lazy (visibility-based) panel loading, thresholds, dual Y-axes,
     * a toggleable legend, collapsible rows and a tab layout.
     */
  reason: Compress header comment and state genericity explicitly
```
/answer c2c13d9d-3635-4a91-a9b4-ec28494aefc8 allow
Control Request:
```yaml
id: acad0113-8dcc-490b-bfae-220007992995
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
      /* ---- cross-panel sync BY AXIS VALUE --------------------------------- *
       * `echarts.connect` links the tooltip/axisPointer by *data index*, which
       * misaligns panels whose series have different point counts (dense HR vs.
       * sparse sleep_stage). We therefore sync zoom and the hover cursor manually,
       * by time value. The Overall-tab daily line charts (daily aggregates, own
       * X-axis) are excluded. */
  new_text: |2-
      /* ---- cross-panel sync BY AXIS VALUE ----------------------------------
       * `echarts.connect` links by *data index*, which misaligns panels whose
       * series have different point counts. We sync zoom/hover manually instead,
       * by time value. Panels of type "daily" (own X-axis) are excluded. */
  reason: Compress comment
```
/answer acad0113-8dcc-490b-bfae-220007992995 allow
Control Request:
```yaml
id: 2fdd82d1-8c8e-4b60-9b51-0cfde9cca562
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
      /* ---- fixed per-panel query window ----------------------------------- *
       * The Overall-tab daily panels aggregate by calendar day and therefore need
       * their own, wider time window -- independent of the global range (which may
       * be as short as 1h and would collapse a daily GROUP BY to a single point).
       * A panel opts in via `cfg.range`:
       *   { days: N }            -> rolling window [now - N days, now]
       *   { from: X, to: Y }     -> absolute bounds; each of X/Y may be
       *                             "now", an epoch-ms number, or an ISO string
       *                             (e.g. "2026-01-01T00:00:00Z").
       * Panels without `cfg.range` use the global [fromMs, toMs] window. */
  new_text: |2-
      /* ---- fixed per-panel query window -------------------------------------
       * Panels that aggregate by calendar day need their own, wider window,
       * independent of the (possibly short) global range. Opt in via `cfg.range`:
       *   { days: N }          -> rolling window [now - N days, now]
       *   { from: X, to: Y }   -> absolute bounds; X/Y: "now" | epoch ms | ISO
       * Panels without `cfg.range` use the global [fromMs, toMs]. */
  reason: Compress comment
```
/answer 2fdd82d1-8c8e-4b60-9b51-0cfde9cca562 allow
Control Request:
```yaml
id: 9e18682a-ea48-4f1c-b87b-4f105de322dc
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
      /* The shared time X-axis. Tick labels are only rendered on panels that
       * request them (`cfg.timeAxis`), since every timeseries/state panel is
       * pinned to the exact same window -- one visible axis (Sleep Stage) suffices
       * for the whole stack, with the panels' own Y-axis labels naming each plot. */
  new_text: |2-
      /* Shared time X-axis; tick labels only render where `cfg.timeAxis` is set,
       * since every timeseries/state panel is pinned to the same window. */
  reason: Compress comment
```
/answer 9e18682a-ea48-4f1c-b87b-4f105de322dc allow
ReasoningToken: 16
Text:
 Jetzt `dashboard.js`: Kommentare komprimieren und die hartkodierte `STAGE`-Map (Sleep-spezifisch) generisch machen, damit der Renderer wirklich domänenneutral ist.
Control Request:
```yaml
id: 24f2f07c-c076-404b-8fd8-6e5ff09001c8
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
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
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
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
            type: "custom", renderItem: renderStageItem,
            encode: { x: [0, 1] }, clip: true,
            data: buildStageSegments(xy),
          }],
        };
      }
  new_text: |2-
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
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
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
          }],
        };
      }
  reason: Move sleep-specific STAGE map into config to keep the renderer domain-generic
```
/answer 24f2f07c-c076-404b-8fd8-6e5ff09001c8 allow
Control Request:
```yaml
id: 9caa9790-d1c2-4164-87ac-ef2281055008
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  reason: Find remaining verbose comments to compress
```
/answer 9caa9790-d1c2-4164-87ac-ef2281055008 allow
Control Request:
```yaml
id: 50c67431-87f0-4cc7-af25-ad1e961119b2
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
          } : undefined,
          // Keep the plot geometry identical across every timeseries/state panel
          // (constant left/right margins) so that, with the shared X-axis range,
          // a given timestamp maps to the same pixel X in every panel. Otherwise
          // panels without a right axis (HR, Sleep Stage) would be wider than the
          // rest and the connected hover axisPointer/tooltip would be offset.
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
          // Pin the axis to the selected query window so every timeseries/state
          // panel shares the exact same X-axis; tick labels only render on the
          // panel that requests them (`cfg.timeAxis`).
          xAxis: timeXAxis(cfg),
  new_text: |2-
          } : undefined,
          // Fixed left/right margins on every timeseries/state panel, so a given
          // timestamp maps to the same pixel X everywhere (needed for the synced
          // hover cursor), regardless of whether a panel has a right axis.
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
          xAxis: timeXAxis(cfg),
  reason: Compress grid-geometry comment
```
/answer 50c67431-87f0-4cc7-af25-ad1e961119b2 allow
Control Request:
```yaml
id: 11f12b5f-588d-4f4f-bdd6-130664d9d198
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
      /* The Overall-tab daily panels are Grafana `xychart` visualisations with
       * `show: "points+lines"` -- i.e. line charts with visible points and a
       * translucent area fill (fillOpacity 50), time on the X-axis. They are
       * rendered as line charts (not bars). */
      function buildDaily(cfg, table, legendSelected) {
  new_text: |2-
      /* Type "daily" panels: line charts with visible points and a translucent
       * area fill, plotted from a pre-aggregated table (own time X-axis). */
      function buildDaily(cfg, table, legendSelected) {
  reason: Compress and de-reference Grafana-specific wording
```
/answer 11f12b5f-588d-4f4f-bdd6-130664d9d198 allow
Control Request:
```yaml
id: 526b7b16-df8f-4578-a4be-8dcf56e3ccef
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
          // The Overall-tab daily line charts keep their own independent X-axis and
          // are not part of the cross-panel cursor/zoom synchronisation.
          if (this.cfg.type === "daily") return;
  new_text: |2-
          // "daily" panels keep their own X-axis, outside the cross-panel sync.
          if (this.cfg.type === "daily") return;
  reason: Compress and de-reference tab-specific wording
```
/answer 526b7b16-df8f-4578-a4be-8dcf56e3ccef allow
Control Request:
```yaml
id: 2765205a-018c-4291-b441-3bd9a70afcff
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
          // --- Grafana-style drag interaction ---
          this.attachDragZoom();
        }

        /* Grafana-like mouse interaction on the plot:
         *   - LEFT button + drag  -> highlight a region; on release its time span
         *     becomes the new query window (data is re-fetched, i.e. the zoom comes
         *     with a genuine resolution increase, not just a visual rescale),
         *   - RIGHT button + drag -> pan the currently shown window; the view
         *     follows live and the panned window is re-fetched on release. */
  new_text: |2-
          this.attachDragZoom();
        }

        /* Mouse interaction on the plot:
         *   - LEFT + drag  -> highlight a region; on release it becomes the new
         *     query window (re-fetched at full resolution, not just rescaled),
         *   - RIGHT + drag -> live-pan the current window; re-fetched on release. */
  reason: Compress drag-interaction comment
```
/answer 2765205a-018c-4291-b441-3bd9a70afcff allow
Control Request:
```yaml
id: 4aa0cf00-bc7d-4134-adb7-dbff6d7dc4e3
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
      /* ---- wire up -------------------------------------------------------- */
      function init() {
        document.title = DASHBOARD.title;
        DASHBOARD.rows.forEach((r) => boardEl.appendChild(buildRow(r)));
  new_text: |2-
      /* ---- wire up -------------------------------------------------------- */
      function init() {
        document.title = DASHBOARD.title;
        const titleEl = document.getElementById("pageTitle");
        if (titleEl) titleEl.textContent = DASHBOARD.title;
        DASHBOARD.rows.forEach((r) => boardEl.appendChild(buildRow(r)));
  reason: "Reflect the loaded config's title in the header, not just document.title"
```
/answer 4aa0cf00-bc7d-4134-adb7-dbff6d7dc4e3 allow
Control Request:
```yaml
id: 6e507f78-8ee2-4ca1-a928-fa6567dbf6df
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics
  script: grep -n -i "grafana\|overall-tab" dashboard.js
  reason: Check for remaining domain-specific references in the generic renderer
```
/answer 6e507f78-8ee2-4ca1-a928-fa6567dbf6df allow
Control Request:
```yaml
id: df4f0ff0-b80b-450e-9ca6-98dcc6cfa213
result:
  structuredContent:
    exit_code: 1
    stdout: ""
```
/answer df4f0ff0-b80b-450e-9ca6-98dcc6cfa213 allow
Control Request:
```yaml
id: 932b637c-edfc-4742-a566-1b298c40c7ad
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  old_text: |-
    /* Dashboard configuration -- a faithful reproduction of the Grafana dashboard
     * `grafana-dashboard.duckdb.json` (\"HRV Data\").
     *
     * The layout mirrors the Grafana RowsLayout / TabsLayout / GridLayout:
     *   - rows are collapsible panel groups,
     *   - a row of type "tabs" combines panels into a tab-panel,
     *   - each panel declares its series (metric + aggregate + styling),
     *     dual Y-axes, min/max, thresholds, axis labels and legend behaviour.
     *
     * Metrics are rendered under their short label (HR, RR, RMSSD, ...).
     */
  new_text: |-
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
  reason: "Compress header comment, document config-selection contract, keep Grafana provenance note"
```
/answer 932b637c-edfc-4742-a566-1b298c40c7ad allow
Control Request:
```yaml
id: 5268d7a0-429c-4bdd-b53e-24e40a942221
result:
  content:
  - type: text
    text: Text not found in file.
  isError: true
```
/answer 5268d7a0-429c-4bdd-b53e-24e40a942221 allow
Control Request:
```yaml
id: c9e8deee-59f8-46c5-9759-0aa2d7285129
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  old_text: |2-
      /* ---- Panel 2 -- Sleep stage (Grafana-style coloured state band) ---- */
      const panel2 = {
        id: 2, type: "state", title: "Sleep Stage", height: 120,
        axisLeft: { label: "STAGE" },
        timeAxis: true,          // only this panel renders the (shared) X time axis
        legend: true,
        series: [
          { label: "STAGE", segment: RAW, metric: "sleep_stage", agg: "none",
            color: col("dark-purple"), width: 1, fillOpacity: 40 },
        ],
      };
  new_text: |2-
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
  reason: "Move sleep-stage coding map from dashboard.js into config, generic renderer contract"
```
/answer c9e8deee-59f8-46c5-9759-0aa2d7285129 allow
Control Request:
```yaml
id: 35c9e357-24e9-4ebb-9146-bb8468917e25
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  max_line: 15
  reason: Check current header text after failed edit
```
/answer 35c9e357-24e9-4ebb-9146-bb8468917e25 allow
Control Request:
```yaml
id: 0340556b-4058-4785-a4d9-9de798eb4344
result:
  structuredContent:
    checksum: 8196920ef2cb59ccf8e27533c05eb698ce7d7b54ca45f67f151cddcd72c8fe4e
    content: |
      /* Dashboard configuration -- a faithful reproduction of the Grafana dashboard
       * `grafana-dashboard.duckdb.json` ("HRV Data").
       *
       * The layout mirrors the Grafana RowsLayout / TabsLayout / GridLayout:
       *   - rows are collapsible panel groups,
       *   - a row of type "tabs" combines panels into a tab-panel,
       *   - each panel declares its series (metric + aggregate + styling),
       *     dual Y-axes, min/max, thresholds, axis labels and legend behaviour.
       *
       * Metrics are rendered under their short label (HR, RR, RMSSD, ...).
       */
      (function () {
        "use strict";

        /* Grafana named colours -> hex (approximate palette). */
```
/answer 0340556b-4058-4785-a4d9-9de798eb4344 allow
Control Request:
```yaml
id: 944a2bad-bf85-4dcb-9b3b-2e0ca119f54d
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  old_text: |-
    /* Dashboard configuration -- a faithful reproduction of the Grafana dashboard
     * `grafana-dashboard.duckdb.json` ("HRV Data").
     *
     * The layout mirrors the Grafana RowsLayout / TabsLayout / GridLayout:
     *   - rows are collapsible panel groups,
     *   - a row of type "tabs" combines panels into a tab-panel,
     *   - each panel declares its series (metric + aggregate + styling),
     *     dual Y-axes, min/max, thresholds, axis labels and legend behaviour.
     *
     * Metrics are rendered under their short label (HR, RR, RMSSD, ...).
     */
  new_text: |-
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
  reason: "Compress header comment, document config-selection contract, keep Grafana provenance note"
```
/answer 944a2bad-bf85-4dcb-9b3b-2e0ca119f54d allow
Control Request:
```yaml
id: 99a9c73d-e245-43ae-ab35-065d7a23c936
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  reason: Review remaining comments for compression
```
/answer 99a9c73d-e245-43ae-ab35-065d7a23c936 allow
Control Request:
```yaml
id: 363b185b-02a2-4728-a4a3-719cdcccce9d
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  old_text: |2-
      /* ---- Panels 6/7/8 -- daily line charts (special backend queries) ----
       * Grafana `xychart` panels with `show: "points+lines"`: line charts with
       * visible points and a translucent area fill over a daily time X-axis. */
      const panel6 = {
        id: 6, type: "daily", title: "Sympathic Dominance Time under threshold",
        height: 320, kind: "dominance_daily",
        // Own fixed window: Grafana `timeFrom: "14d"` (rolling last 14 days).
        range: { days: 14 },
  new_text: |2-
      /* ---- Panels 6/7/8 -- daily line charts (pre-aggregated backend queries) */
      const panel6 = {
        id: 6, type: "daily", title: "Sympathic Dominance Time under threshold",
        height: 320, kind: "dominance_daily",
        range: { days: 14 },      // rolling last 14 days, independent of the global range
  reason: Compress comment
```
/answer 363b185b-02a2-4728-a4a3-719cdcccce9d allow
Control Request:
```yaml
id: c33afb61-d023-4cec-b981-7e2497c2dc2c
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics
  script: |-
    set -e
    node --check dashboard.js && echo "dashboard.js OK"
    node --check dashboard.config.js && echo "dashboard.config.js OK"
    grep -n "STAGE\b" dashboard.js || echo "no leftover STAGE refs"
    grep -n "config=" dashboard.html
    python3 -c "import re; print('html looks fine')" 2>/dev/null || true
  reason: Syntax-check JS files and confirm loader wiring
```
/answer c33afb61-d023-4cec-b981-7e2497c2dc2c allow
Control Request:
```yaml
id: f801a911-ddda-4eeb-b38a-2c40a3a1318c
result:
  structuredContent:
    stdout: |
      dashboard.js OK
      dashboard.config.js OK
      no leftover STAGE refs
      46:    /* Pick the dashboard config to load. `?config=<name>` loads
      html looks fine
```
/answer f801a911-ddda-4eeb-b38a-2c40a3a1318c allow
Control Request:
```yaml
id: 4a8cb9da-89ef-4ad6-a45e-6205d9ae20f4
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html
  reason: Final review of dashboard.html
```
/answer 4a8cb9da-89ef-4ad6-a45e-6205d9ae20f4 allow
ReasoningToken: 161
ReasoningToken: 802
ReasoningToken: 27
Text:
 Gut, keine Referenzen mehr. Jetzt `dashboard.config.js`: Kommentare komprimieren und die `states`-Map für den Sleep-Stage-Panel ergänzen (da `dashboard.js` sie jetzt aus der Config erwartet).
ReasoningToken: 36
ReasoningToken: 124
Text:
 Nun noch weitere Kommentare in der Config komprimieren (verbleibende ausführliche Blöcke).
ReasoningToken: 171
Text:
 Jetzt teste ich beide Dateien auf Syntaxfehler und prüfe die HTML-Loader-Logik.
ReasoningToken: 104
Alles sauber. Zusammenfassung meiner Prüfung und Änderungen:

## Generalisierbarkeit – gefundene Probleme & Fixes

1. **`dashboard.js` enthielt eine hartkodierte, domänenspezifische `STAGE`-Map** (Sleep-Stage-Codes → Label/Farbe) direkt im generischen Renderer. Das war die einzige echte Isolationsverletzung: Ein künftiges Dashboard mit einem anderen `"state"`-Panel (andere Kategorien) hätte den Renderer selbst ändern müssen. → Verschoben nach `dashboard.config.js` als `series[0].states`; `dashboard.js` liest die Map jetzt generisch aus der Config (`buildStageSegments`, `makeStageRenderer` als Factory statt globaler Konstante).
2. Diverse Kommentare in `dashboard.js` referenzierten Config-spezifische Details ("Overall-tab", "Grafana-style") statt allgemeiner Konzepte – neutralisiert.
3. Die `<h1>` im Header war fest auf "HRV Data" verdrahtet, unabhängig vom geladenen `DASHBOARD.title`. → jetzt `id="pageTitle"`, wird in `init()` gesetzt.
4. **CSS** (`dashboard.css`) war bereits sauber generisch (keine domänenspezifischen Klassennamen, nur `--vars`, `.panel`, `.grid`, `.row`, `.tabbar` …) – hier war keine Änderung nötig, es kann unverändert für weitere Dashboards mitverwendet werden.
5. Alle sonstigen Config-Parameter (Metriken, `segment`, `kind`, Farben, Schwellwerte) waren bereits sauber aus `dashboard.js` in `dashboard.config.js` ausgelagert.

## URL-Parameter für Config-Auswahl

`dashboard.html` lädt jetzt Skripte dynamisch statt statisch:
- `?config=<name>` → lädt `dashboard.config.<name>.js`
- kein/ungültiger Parameter → Default `dashboard.config.js` (aktuelle Config)
- Fehlschlag beim Laden eines benannten Configs → Fallback auf Default, Fehler wird sonst im Status-Feld angezeigt
- `dashboard.js` wird erst nach erfolgreichem Config-Laden nachgeladen

Neue Dashboards brauchen künftig nur eine Datei `dashboard.config.<name>.js` nach demselben Schema (inkl. `window.DASHBOARD = {...}`).

## Kommentare komprimiert
In `dashboard.js` und `dashboard.config.js` wurden mehrzeilige, teils redundante Blockkommentare gekürzt (Header, Sync-Logik, Zeitachsen-Helfer, Drag-Interaktion, Panel-Kommentare), ohne fachlich relevante Erklärungen zu verlieren.

Syntaxprüfung (`node --check`) für beide JS-Dateien erfolgreich; keine verbleibenden Grafana-/Tab-spezifischen Referenzen im generischen Renderer.
