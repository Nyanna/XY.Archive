Prüfe, ob es einfach zu implementiere wäre die Legende Floating auf dem Graphen zu haben, bei dualen Achsen sogar rechts und links oben nach Zugehörigkeit.

- Dashboard: `/home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html`
SystemInit:  id=2d146b2a-7fd4-4667-b4aa-7286303ef9db, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: 40c52b20-afe1-4b4b-a8cb-d1887f831d7b
toolName: file-stats
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html
  reason: Dateigröße/Struktur prüfen vor dem Lesen
```
/answer 40c52b20-afe1-4b4b-a8cb-d1887f831d7b allow
ReasoningToken: 48
Control Request:
```yaml
id: 004c993d-5484-490e-a4ed-92abc6b4608a
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html
  reason: Inhalt der Datei ansehen
```
/answer 004c993d-5484-490e-a4ed-92abc6b4608a allow
Control Request:
```yaml
id: a88564b6-7395-4abf-a408-cb869b9e364e
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics
  reason: Verwandte Dateien im statics-Ordner finden
```
/answer a88564b6-7395-4abf-a408-cb869b9e364e allow
Control Request:
```yaml
id: c366ba99-e052-4fc7-aca2-7b2c70a65f38
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
/answer c366ba99-e052-4fc7-aca2-7b2c70a65f38 allow
ReasoningToken: 26
Control Request:
```yaml
id: 71554fd3-2d1a-445f-ac74-9538c533fda7
toolName: file-stats
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  reason: Größe der Haupt-JS-Datei prüfen
```
/answer 71554fd3-2d1a-445f-ac74-9538c533fda7 allow
Control Request:
```yaml
id: defa20a0-8cb9-4760-ae2a-88ad90e76e67
toolName: file-stats
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  reason: Größe der Config-Datei prüfen
```
/answer defa20a0-8cb9-4760-ae2a-88ad90e76e67 allow
ReasoningToken: 79
Control Request:
```yaml
id: 11e16315-d163-4468-b837-b13242952799
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics
  script: grep -n -i "legend\|yAxis\|grid:\|title:" dashboard.js | head -120
  reason: Legend/Achsen-Konfiguration im JS finden
```
/answer 11e16315-d163-4468-b837-b13242952799 deny lies die Datei komplett ein
Control Request:
```yaml
id: 40137bf3-ba3b-4fe9-9a81-6b59eaaafbb6
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  reason: "Komplette Datei lesen wie angewiesen, um Legend/Achsen-Konfiguration zu finden"
```
/answer 40137bf3-ba3b-4fe9-9a81-6b59eaaafbb6 allow
ReasoningToken: 70
ReasoningToken: 2995
## Kurzfazit
Ja – **das wäre einfach umzusetzen**, weil die dafür nötigen ECharts-Fähigkeiten bereits vorhanden sind und die Code-Basis sauber genug strukturiert ist:

1. **Legende ist in ECharts ein eigenständiges, frei positionierbares Element**, unabhängig vom `grid`. Sie lässt sich per `left/right/top/bottom` (px, %, oder `"auto"`) beliebig platzieren – auch über der Zeichenfläche ("floating"), ohne dass die Grid-Geometrie das erzwingt.
2. **ECharts erlaubt mehrere Legend-Komponenten gleichzeitig** (`legend: [ {...}, {...} ]`), jede mit eigener `data`-Liste. Genau das braucht man für "links oben = linke Achse, rechts oben = rechte Achse".
3. Die **Zuordnung Serie → Achse ist im Code bereits explizit vorhanden** (`sc.axis === "right"` in `buildTimeseries`), man muss also nur die schon vorhandene Information zum Splitten der Legend-`data`-Arrays nutzen statt (wie jetzt) alles in eine gemeinsame `legendData`-Liste zu schreiben.

## Betroffene Stellen (dashboard.js)
Alles konzentriert sich auf 2 Funktionen + 1 Hilfsfunktion:

- **`buildTimeseries(cfg, fetched, legendSelected)`** – aktuell eine `legend:` mit `bottom:0`. Müsste zu:
  ```js
  legend: cfg.legend ? [
    { data: leftNames,  top: 6, left: 8,
      backgroundColor: "rgba(255,255,255,0.75)", padding: [2,6],
      textStyle: {...}, icon: "roundRect" },
    ...(rightAxisVisible ? [{ data: rightNames, top: 6, right: 8,
      backgroundColor: "rgba(255,255,255,0.75)", padding: [2,6],
      textStyle: {...}, icon: "roundRect" }] : []),
  ] : undefined,
  ```
- **`buildDaily(...)`** – analoges Pattern (hat auch schon `axisLeft`/`axisRight`).
- **`grid.top`** ggf. leicht anpassen (statt `GRID_TOP=16` etwas mehr Luft, oder bewusst überlappend lassen – "floating" heißt ja gerade, dass sie über den Linien schwebt; mit halbtransparentem Hintergrund bleibt das lesbar).
- **`legendSelection()`** (liest aktuell `opt.legend[0].selected`) müsste beim Speichern/Restaurieren über beide Legend-Objekte iterieren – trivial, da jede Legende ohnehin nur "ihre" Serien kennt und ECharts pro Legend-Komponente einen eigenen `selected`-State führt (kein Konfliktrisiko, eher ein Vorteil).

## Praktische Stolpersteine (klein, aber erwähnenswert)
- Bei vielen Serien pro Achse kann die floatende Legende breit werden und Daten verdecken → ggf. `type: "scroll"` beibehalten oder Zeilenumbruch (`orient: "vertical"`) bei > 2–3 Einträgen nutzen.
- Halbtransparenter Hintergrund/Padding nötig, damit Text über den Linien lesbar bleibt.
- Bei Panels ohne rechte Achse reicht eine einzelne floatende Legende (z. B. oben mittig oder oben links) statt des Arrays.
- Keine Änderungen an `dashboard.config.js` nötig – die Achszuordnung pro Serie existiert dort schon (`axis: "right"`).

## Aufwandseinschätzung
Klein – reine Config-Änderung in 2 Funktionen plus Kleinanpassung von `legendSelection()`, keine neue Interaktionslogik, kein Eingriff in Datenladen/Sync/Zoom. Grob **1–2 Stunden inkl. Feinschliff** (Padding, Transparenz, Verhalten bei vielen Serien).

Soll ich das direkt umsetzen?
Halb Tranparent klingt gut und die Legende braucht nicht umgebrochen zu werden. Die views sind breit genug.
SystemInit:  id=2d146b2a-7fd4-4667-b4aa-7286303ef9db, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: e7780819-bd8e-4023-b99f-cbc967aaa9e2
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  reason: "Prüfen, welche Panels axisRight/axis:'right' nutzen (auch bei type 'daily')"
```
/answer e7780819-bd8e-4023-b99f-cbc967aaa9e2 allow
ReasoningToken: 4007
Control Request:
```yaml
id: af325245-1918-4891-94ef-b8c68c4fe223
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
      /* Build the ECharts option for a timeseries / state panel from fetched data.
       * `fetched` maps a series config -> its [[ts,val], ...] array. */
      function buildTimeseries(cfg, fetched, legendSelected) {
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
          tooltip: { trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip },
          legend: cfg.legend ? {
            type: "scroll", bottom: 0, data: legendData,
            selected: legendSelected,
            textStyle: { color: AXIS, fontWeight: "bold" }, icon: "roundRect",
          } : undefined,
          // Fixed left/right margins on every timeseries/state panel, so a given
          // timestamp maps to the same pixel X everywhere (needed for the synced
          // hover cursor), regardless of whether a panel has a right axis.
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
          xAxis: timeXAxis(cfg),
          yAxis: baseYAxis(cfg),
          dataZoom: insideZoom(),
          series,
        };
      }
  new_text: |2-
      /* Floating, semi-transparent legend(s), drawn directly over the plot area
       * instead of taking up their own row. With a right Y-axis in play, series
       * are split into two legend components by axis affiliation: left-axis
       * series top-left, right-axis series top-right. `selected` is shared --
       * each piece only looks up the names it owns, so toggling one doesn't
       * touch the other. No wrapping/scrolling: panels are wide enough. */
      const LEGEND_BG = "rgba(255,255,255,0.72)";
      function legendPiece(names, side, selected) {
        if (!names.length) return null;
        return {
          data: names, selected, top: 4, [side]: 8,
          backgroundColor: LEGEND_BG, borderRadius: 4, padding: [3, 8],
          textStyle: { color: AXIS, fontWeight: "bold" }, icon: "roundRect",
        };
      }
      function floatingLegend(leftNames, rightNames, selected) {
        const pieces = [
          legendPiece(leftNames, "left", selected),
          legendPiece(rightNames, "right", selected),
        ].filter(Boolean);
        return pieces.length ? pieces : undefined;
      }

      /* Build the ECharts option for a timeseries / state panel from fetched data.
       * `fetched` maps a series config -> its [[ts,val], ...] array. */
      function buildTimeseries(cfg, fetched, legendSelected) {
        const leftNames = [], rightNames = [];
        const series = [];
        cfg.series.forEach((sc) => {
          const yIdx = sc.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
          const data = fetched.get(sc);
          const step = cfg.type === "state" ? "end" : false;
          (yIdx ? rightNames : leftNames).push(sc.label);
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
            (mIdx ? rightNames : leftNames).push(m.label);
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
          tooltip: { trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip },
          legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
          // Fixed left/right margins on every timeseries/state panel, so a given
          // timestamp maps to the same pixel X everywhere (needed for the synced
          // hover cursor), regardless of whether a panel has a right axis.
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
          xAxis: timeXAxis(cfg),
          yAxis: baseYAxis(cfg),
          dataZoom: insideZoom(),
          series,
        };
      }
  reason: "Floating, halbtransparente Legende(n) für buildTimeseries einbauen, nach Achszugehörigkeit links/rechts oben getrennt"
```
/answer af325245-1918-4891-94ef-b8c68c4fe223 allow
Control Request:
```yaml
id: c13374ba-3d07-4215-ad2e-6d8fcac984f3
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
          legend: cfg.legend
            ? {
                type: "scroll", bottom: 0, data: legendData, selected: legendSelected,
                textStyle: { color: AXIS, fontWeight: "bold" }, icon: "roundRect",
              }
            : undefined,
          grid: { left: 56, right: 24, top: 16, bottom: 44 },
  new_text: |2-
          legend: cfg.legend ? floatingLegend(legendData, [], legendSelected) : undefined,
          grid: { left: 56, right: 24, top: 16, bottom: 44 },
  reason: Floating Legende auch für die daily-Panels verwenden
```
/answer c13374ba-3d07-4215-ad2e-6d8fcac984f3 allow
Control Request:
```yaml
id: de7d2b10-53b3-4c29-95c0-314dc1cab5d1
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
        legendSelection() {
          if (!this.chart) return undefined;
          const opt = this.chart.getOption();
          const lg = opt && opt.legend && opt.legend[0];
          return lg && lg.selected ? lg.selected : undefined;
        }
  new_text: |2-
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
  reason: Legend-Auswahlstatus über mehrere Legend-Komponenten hinweg zusammenführen (persistiert Toggle-State bei Reload)
```
/answer de7d2b10-53b3-4c29-95c0-314dc1cab5d1 allow
Control Request:
```yaml
id: a4b8a8be-2739-468a-a3af-79ff6a9522b4
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics
  script: node --check dashboard.js && echo OK
  reason: Syntax der geänderten Datei prüfen
```
/answer a4b8a8be-2739-468a-a3af-79ff6a9522b4 allow
Control Request:
```yaml
id: c3fd8516-0af7-4e36-bbe7-28aabcccafcb
result:
  structuredContent:
    stdout: |
      OK
```
/answer c3fd8516-0af7-4e36-bbe7-28aabcccafcb allow
Control Request:
```yaml
id: be9c5fc7-8702-4c0c-b7a9-8f15d02415cf
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: /* Build the ECharts option for a timeseries
  end: "const legendData = [], series = [];"
  reason: Ergebnis der Änderungen final durchsehen
```
/answer be9c5fc7-8702-4c0c-b7a9-8f15d02415cf allow
Control Request:
```yaml
id: b9dc7315-d429-44b4-962e-59dcad18af4e
result:
  structuredContent:
    checksum: d8d4f59ca46f086aa3869de2139b25976cd50e3435759f9faa835c391339e092
    content: |-
      /* Build the ECharts option for a timeseries / state panel from fetched data.
         * `fetched` maps a series config -> its [[ts,val], ...] array. */
        function buildTimeseries(cfg, fetched, legendSelected) {
          const leftNames = [], rightNames = [];
          const series = [];
          cfg.series.forEach((sc) => {
            const yIdx = sc.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
            const data = fetched.get(sc);
            const step = cfg.type === "state" ? "end" : false;
            (yIdx ? rightNames : leftNames).push(sc.label);
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
              (mIdx ? rightNames : leftNames).push(m.label);
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
            tooltip: { trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip },
            legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
            // Fixed left/right margins on every timeseries/state panel, so a given
            // timestamp maps to the same pixel X everywhere (needed for the synced
            // hover cursor), regardless of whether a panel has a right axis.
            grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
            xAxis: timeXAxis(cfg),
            yAxis: baseYAxis(cfg),
            dataZoom: insideZoom(),
            series,
          };
        }

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

        /* Type "daily" panels: line charts with visible points and a translucent
         * area fill, plotted from a pre-aggregated table (own time X-axis). */
        function buildDaily(cfg, table, legendSelected) {
          const legendData = [], series = [];
```
/answer b9dc7315-d429-44b4-962e-59dcad18af4e allow
ReasoningToken: 6746
Text:
 Jetzt `buildDaily` und `legendSelection()` anpassen:
ReasoningToken: 22
ReasoningToken: 57
Text:
 Syntax ist sauber. Kurzer Blick auf das Ergebnis:
Sieht korrekt aus. Änderungen sind syntaktisch valide und logisch konsistent umgesetzt.

**Was geändert wurde (`dashboard.js`):**

1. Neuer Helper `floatingLegend(leftNames, rightNames, selected)` + `legendPiece(...)`: erzeugt pro Achse eine eigene Legend-Komponente mit `top`/`left`/`right`-Positionierung, halbtransparentem, abgerundetem Hintergrund (`rgba(255,255,255,0.72)`), ohne `type: "scroll"` (kein Umbruch/Scrollen mehr – wie gewünscht).
2. `buildTimeseries`: Serien werden jetzt nach `sc.axis`/`m.axis` in `leftNames`/`rightNames` einsortiert; bei aktiver rechter Achse entstehen zwei floatende Legenden oben links/rechts, sonst nur eine oben links.
3. `buildDaily`: nutzt denselben Helper (dort gibt's keine Achstrennung, da diese Panels keine rechte Achse verwenden – bleibt eine Legende oben links).
4. `Panel.legendSelection()`: liest/merged jetzt den Selected-Status über **alle** Legend-Komponenten (statt nur `legend[0]`), damit das Ein-/Ausblenden von Serien beim Reload (Zeitfenster ändern etc.) weiterhin erhalten bleibt.

Betroffene Panels: 1 (Heart Rate), 3 (Autonomic Balance), 14 (Vagal Tone), 4 (Frequency Power/DFA), 9 (Circadian Band Power), 15 (Cardiopulmonary Coupling), 16 (RR Interval) sowie 6/7/8 (Daily) – alle mit `legend: true`. Panel 2 (Sleep Stage) hat ohnehin nie eine Legende gerendert (unverändert, kein Regression).

`node --check` bestätigt syntaktisch korrektes JS. Falls du magst, kann ich als Nächstes den Server starten und mir das visuell im Browser/Screenshot anschauen, um Padding/Kontrast zu verifizieren.
Funktioniert gut. Ich bemerke jetzt das, nach deaktivierter X-Achse, in allen außer dem sleep stage Panel ein pading bottom im canvas ist. Lässt sich das reduzieren?
SystemInit:  id=2d146b2a-7fd4-4667-b4aa-7286303ef9db, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: 32662d24-cfda-4eef-8115-2491252624e7
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: /* ---- shared plot geometry & axis helpers
  max_line: 100
  reason: Exakten Kontext von GRID_TOP/GRID_BOTTOM für die Anpassung sehen
```
/answer 32662d24-cfda-4eef-8115-2491252624e7 allow
Control Request:
```yaml
id: b4055e66-fd2f-4441-bb07-455ecb93c7fe
result:
  structuredContent:
    checksum: 3a94a99f3301872fadffd273a4aac039f2d8632b42067db08ebbdbc127faf4a3
    content: |
      /* ---- shared plot geometry & axis helpers ---------------------------- */
        const GRID_TOP = 16, GRID_BOTTOM = 44;

        /* High-resolution time-axis tick labels: HH:MM (with :SS when relevant),
```
/answer b4055e66-fd2f-4441-bb07-455ecb93c7fe allow
ReasoningToken: 2355
Control Request:
```yaml
id: 020c7090-0b6f-4f85-9a10-b876aa20df75
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
      /* ---- shared plot geometry & axis helpers ---------------------------- */
      const GRID_TOP = 16, GRID_BOTTOM = 44;
  new_text: |2-
      /* ---- shared plot geometry & axis helpers ---------------------------- */
      const GRID_TOP = 16, GRID_BOTTOM = 44, GRID_BOTTOM_NOAXIS = 10;

      /* Bottom grid margin: only the one panel per group that actually renders
       * the shared x-axis tick labels (`cfg.timeAxis`) needs the full margin;
       * every other panel would otherwise carry that space as dead padding
       * (the legend no longer lives down there -- it floats over the plot). */
      const gridBottom = (cfg) => (cfg.timeAxis ? GRID_BOTTOM : GRID_BOTTOM_NOAXIS);
  reason: Helper zur bedingten Bottom-Margin je nach sichtbarer X-Achse ergänzen
```
/answer 020c7090-0b6f-4f85-9a10-b876aa20df75 allow
ReasoningToken: 11
Control Request:
```yaml
id: 22fd54a5-4b77-4673-976b-354fb8443d81
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
          legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
          // Fixed left/right margins on every timeseries/state panel, so a given
          // timestamp maps to the same pixel X everywhere (needed for the synced
          // hover cursor), regardless of whether a panel has a right axis.
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
  new_text: |2-
          legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
          // Fixed left/right margins on every timeseries/state panel, so a given
          // timestamp maps to the same pixel X everywhere (needed for the synced
          // hover cursor), regardless of whether a panel has a right axis.
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: gridBottom(cfg) },
  reason: Bottom-Margin für Timeseries-Panels ohne sichtbare X-Achse reduzieren
```
/answer 22fd54a5-4b77-4673-976b-354fb8443d81 allow
Control Request:
```yaml
id: 8e2acc30-567a-43ae-a157-25dc2fc1844c
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: GRID_BOTTOM },
          xAxis: timeXAxis(cfg),
          yAxis: {
            type: "value", min: 0, max: 1,
  new_text: |2-
          grid: { left: 64, right: 64, top: GRID_TOP, bottom: gridBottom(cfg) },
          xAxis: timeXAxis(cfg),
          yAxis: {
            type: "value", min: 0, max: 1,
  reason: Gleiche Bottom-Margin-Reduktion für die State-Band-Panels
```
/answer 8e2acc30-567a-43ae-a157-25dc2fc1844c allow
Control Request:
```yaml
id: c02674cd-2d14-42ac-a46d-526005d1b035
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: sel.style.top = GRID_TOP + "px";
  max_line: 470
  reason: "Stelle finden, an der die Drag-Select-Overlay-Höhe berechnet wird"
```
/answer c02674cd-2d14-42ac-a46d-526005d1b035 allow
Control Request:
```yaml
id: b00917c6-0dc2-40e8-b46a-ad22f065a410
result:
  content:
  - type: text
    text: Resolved end position must not lie before the resolved start position.
  isError: true
```
/answer b00917c6-0dc2-40e8-b46a-ad22f065a410 allow
ReasoningToken: 1072
Control Request:
```yaml
id: 51e957b2-4a06-4add-a009-37e4e827add1
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: sel.style.top = GRID_TOP + "px";
  end: sel.style.display = "block";
  reason: "Stelle finden, an der die Drag-Select-Overlay-Höhe berechnet wird"
```
/answer 51e957b2-4a06-4add-a009-37e4e827add1 allow
Control Request:
```yaml
id: a6ee6233-9dc3-478d-8b2d-2ffbbd432980
result:
  structuredContent:
    checksum: 0585b107064fc169a8d21ac4accf4422a545eb8c108964cc74172049efaf1ac4
    content: |-
      sel.style.top = GRID_TOP + "px";
                sel.style.width = "0px";
                sel.style.height = Math.max(0, chart.getHeight() - GRID_TOP - GRID_BOTTOM) + "px";
                sel.style.display = "block";
```
/answer a6ee6233-9dc3-478d-8b2d-2ffbbd432980 allow
Text:
 Auch die Höhe des Drag-Selektions-Overlays hängt noch am festen `GRID_BOTTOM` – das würde jetzt für Panels ohne sichtbare X-Achse zu hoch gezeichnet. Fixe ich gleich mit:
Control Request:
```yaml
id: 207310e7-1d7a-4e32-9da1-c531a701f6ac
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
              sel.style.top = GRID_TOP + "px";
              sel.style.width = "0px";
              sel.style.height = Math.max(0, chart.getHeight() - GRID_TOP - GRID_BOTTOM) + "px";
              sel.style.display = "block";
  new_text: |2-
              sel.style.top = GRID_TOP + "px";
              sel.style.width = "0px";
              sel.style.height = Math.max(0, chart.getHeight() - GRID_TOP - gridBottom(this.cfg)) + "px";
              sel.style.display = "block";
  reason: Drag-Select-Overlay-Höhe an die tatsächliche (variable) Bottom-Margin des Panels anpassen
```
/answer 207310e7-1d7a-4e32-9da1-c531a701f6ac allow
Control Request:
```yaml
id: 7a115835-cf6f-41e6-a7d0-1e61ce15cf0d
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: "attachDragZoom() {"
  end: "try { el.setPointerCapture(e.pointerId); } catch (_) {}"
  reason: "Verifizieren, dass this innerhalb des pointerdown-Handlers korrekt die Panel-Instanz referenziert"
```
/answer 7a115835-cf6f-41e6-a7d0-1e61ce15cf0d allow
Control Request:
```yaml
id: d030bad4-d2e4-4052-830e-17052d10d3f4
result:
  structuredContent:
    checksum: 2de6d93f807942c189656326b447167aef28c23d9d225f6a1442c837d55791f3
    content: |-
      attachDragZoom() {
            const chart = this.chart, el = this.chartEl;
            el.addEventListener("contextmenu", (e) => e.preventDefault());

            const sel = document.createElement("div");
            sel.className = "zoom-select";
            sel.style.display = "none";
            el.appendChild(sel);

            const pxOf = (e) => e.clientX - el.getBoundingClientRect().left;
            let drag = null, raf = 0;

            // Pointer Events + pointer capture: once the drag starts, every
            // pointermove/pointerup is delivered to this element even when the cursor
            // leaves it, so we never lose the move/up phase (which was the bug with
            // document-level mouse listeners on top of the ECharts canvas).
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
              if (e.button === 0) {
                sel.style.left = startPx + "px";
                sel.style.top = GRID_TOP + "px";
                sel.style.width = "0px";
                sel.style.height = Math.max(0, chart.getHeight() - GRID_TOP - gridBottom(this.cfg)) + "px";
                sel.style.display = "block";
              }
              try { el.setPointerCapture(e.pointerId); } catch (_) {}
```
/answer d030bad4-d2e4-4052-830e-17052d10d3f4 allow
ReasoningToken: 136
Text:
 Gut, arrow function → `this` referenziert korrekt die Panel-Instanz. Syntax-Check zur Sicherheit:
Control Request:
```yaml
id: 3ff0d67f-8ef7-4cf1-993c-0629cc1eacbb
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics
  script: node --check dashboard.js && echo OK
  reason: Syntax nach den Änderungen prüfen
```
/answer 3ff0d67f-8ef7-4cf1-993c-0629cc1eacbb allow
Control Request:
```yaml
id: 6ec3e970-b733-4f13-8f07-6b770290bb36
result:
  structuredContent:
    stdout: |
      OK
```
/answer 6ec3e970-b733-4f13-8f07-6b770290bb36 allow
**Erledigt.** Ursache: `GRID_BOTTOM = 44` war fix für jedes Timeseries-/State-Panel gesetzt – ursprünglich Platz für X-Achsen-Ticks *und* die alte Bottom-Legende. Da nur das Sleep-Stage-Panel (`timeAxis: true`) die Achsenbeschriftung tatsächlich zeigt, blieb bei allen anderen dieser Bereich jetzt als leerer Rand übrig, seit die Legende nach oben gewandert ist.

**Änderungen:**
- Neuer Helper `gridBottom(cfg)`: liefert `GRID_BOTTOM` (44px) nur, wenn `cfg.timeAxis` gesetzt ist, sonst `GRID_BOTTOM_NOAXIS` (10px, etwas Restluft).
- In `buildTimeseries` und `buildStateBand` wird `grid.bottom` jetzt darüber bestimmt statt fix.
- Das Drag-Select-Overlay (blaue Auswahlbox beim Ziehen) berechnete seine Höhe ebenfalls über die feste `GRID_BOTTOM` – angepasst auf `gridBottom(this.cfg)`, sonst wäre die Auswahlbox bei den kleineren Panels zu hoch gezeichnet worden.

`daily`-Panels sind unverändert (zeigen ihre X-Achse immer, brauchen weiterhin die volle Marge). Syntax geprüft, `node --check` läuft durch.
"Extended" ist ein Row mit Tab-Panel. Kannst du die Tabs in den Row Header integrieren, um den vertikalen Platz besser zu nutzen?
SystemInit:  id=2d146b2a-7fd4-4667-b4aa-7286303ef9db, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: e20e8e45-7d4a-449a-8294-cb1bf65164aa
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.css
  reason: CSS-Struktur für Row-Header und Tabs verstehen
```
/answer e20e8e45-7d4a-449a-8294-cb1bf65164aa allow
Control Request:
```yaml
id: 72a4aa8f-b07a-4d1c-ab24-fa4028055069
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: "function buildTabs(container, tabs) {"
  end: "function buildRow(rowCfg) {"
  reason: buildTabs und buildRow Implementierung ansehen
```
/answer 72a4aa8f-b07a-4d1c-ab24-fa4028055069 allow
Control Request:
```yaml
id: 8d18a4f4-8b07-4fc7-befe-cfe31958a794
result:
  structuredContent:
    checksum: d518f45e957e507b75c2005ac8a6db95c82e6d7f9cd110ddd2bc7138b7ff4ca7
    content: |-
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
```
/answer 8d18a4f4-8b07-4fc7-befe-cfe31958a794 allow
ReasoningToken: 93
Control Request:
```yaml
id: 10f3755c-bd38-43b2-a36b-ad617249df81
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: "function buildRow(rowCfg) {"
  end: /* ---- lazy loading via IntersectionObserver
  reason: buildRow Implementierung vollständig ansehen
```
/answer 10f3755c-bd38-43b2-a36b-ad617249df81 allow
Control Request:
```yaml
id: 91360174-e136-4dda-b3c5-3c516c732ba2
result:
  structuredContent:
    checksum: 3bf9094cdd5d848c2c0892ec0ebcaba36a69649ae6326119ec5bd8550df1363d
    content: |-
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

        /* ---- lazy loading via IntersectionObserver
```
/answer 91360174-e136-4dda-b3c5-3c516c732ba2 allow
ReasoningToken: 14
Control Request:
```yaml
id: 53666a81-dfe4-43e8-b9cc-eda22b48087f
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
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
  new_text: |2-
      /* The tab bar itself lives in the row header (next to the title), so it
       * doesn't cost its own vertical row above the panel grid; only the tab
       * bodies go into `bodyContainer`. Clicks on tabs stop propagating so they
       * don't also trigger the header's collapse toggle. */
      function buildTabs(headEl, bodyContainer, tabs) {
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
          btn.addEventListener("click", (e) => {
            e.stopPropagation();
            bar.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
            bodies.forEach((b) => (b.style.display = "none"));
            body.style.display = "";
            // Panels in the newly shown tab become visible -> observer loads them.
            requestAnimationFrame(() => panels.forEach((p) => p.resize()));
          });
          bar.appendChild(btn);
          bodyContainer.appendChild(body);
          bodies.push(body);
        });
        headEl.appendChild(bar);
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
        if (rowCfg.type === "tabs") buildTabs(head, content, rowCfg.tabs);
        else buildGrid(content, rowCfg.panels);
  reason: Tabbar in den Row-Header verschieben statt in den Row-Content
```
/answer 53666a81-dfe4-43e8-b9cc-eda22b48087f allow
Control Request:
```yaml
id: 5a8813f1-ea32-4580-a003-1ed4d6c75bc9
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.css
  old_text: |-
    .row-head {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.35rem 0.4rem;
      cursor: pointer;
      user-select: none;
      border-bottom: 1px solid var(--border);
    }
  new_text: |-
    .row-head {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.35rem 0.4rem;
      cursor: pointer;
      user-select: none;
      border-bottom: 1px solid var(--border);
      flex-wrap: wrap;
    }
  reason: "Row-Header darf bei schmalem Viewport umbrechen, wenn Tabs dort andocken"
```
/answer 5a8813f1-ea32-4580-a003-1ed4d6c75bc9 allow
Control Request:
```yaml
id: 999016a0-b667-4424-b38d-9be95df5f79f
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.css
  old_text: |-
    /* ---- tabs ------------------------------------------------------------ */
    .tabbar {
      display: flex;
      gap: 0.35rem;
      flex-wrap: wrap;
      margin-bottom: 0.75rem;
    }
    .tab {
      padding: 0.35rem 0.9rem;
      border-radius: 6px 6px 0 0;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--muted);
    }
    .tab.active {
      background: var(--panel);
      color: var(--accent);
      border-bottom-color: var(--panel);
      font-weight: 600;
    }
  new_text: |-
    /* ---- tabs --------------------------------------------------------------
     * Sits inline in the row header (right of the title), not above the panel
     * grid, so it doesn't cost its own vertical row. */
    .tabbar {
      display: flex;
      gap: 0.3rem;
      flex-wrap: wrap;
      margin-left: auto;
    }
    .tab {
      padding: 0.25rem 0.75rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: var(--panel);
      color: var(--muted);
      font-size: 0.82rem;
    }
    .tab:hover { border-color: var(--accent); color: var(--accent); }
    .tab.active {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
      font-weight: 600;
    }
  reason: Tab-Optik von Aktenreiter auf Segmented-Control im Header umstellen
```
/answer 999016a0-b667-4424-b38d-9be95df5f79f allow
Control Request:
```yaml
id: 4a4de48c-dd58-4fef-a293-5488ee2bc876
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics
  script: node --check dashboard.js && echo OK
  reason: Syntax nach den Änderungen prüfen
```
/answer 4a4de48c-dd58-4fef-a293-5488ee2bc876 allow
Control Request:
```yaml
id: 81b76441-123e-4518-a826-1f8dda933197
result:
  structuredContent:
    stdout: |
      OK
```
/answer 81b76441-123e-4518-a826-1f8dda933197 allow
ReasoningToken: 4698
Text:
 Jetzt das CSS anpassen (Tabbar in den Header integrieren, rechtsbündig, Segmented-Control-Optik statt Aktenreiter-Look):
**Erledigt.**

**Änderungen:**
- `buildTabs(headEl, bodyContainer, tabs)`: Tabbar wird jetzt in den Row-Header gehängt, nur die Tab-Inhalte (`.tab-body`) landen im `row-content`. Klicks auf einen Tab-Button stoppen die Propagation, damit sie nicht zusätzlich das Collapse-Toggle des Headers auslösen.
- `buildRow`: ruft bei `type === "tabs"` jetzt `buildTabs(head, content, ...)` statt `buildTabs(content, ...)` auf.
- CSS: `.row-head` bekommt `flex-wrap: wrap` (für schmale Viewports). `.tabbar` sitzt per `margin-left: auto` rechtsbündig neben dem Titel, kein eigener vertikaler Block mehr. `.tab`/`.tab.active` von "Aktenreiter"-Optik (die nur Sinn ergab, wenn der Content direkt darunter saß) auf ein kompaktes Segmented-Control umgestylt.

Ergebnis: bei "Extended" steht der Tabtitel-Wechsel ("DFA / Frequencies / Overall / REM / RR") jetzt in derselben Zeile wie "Extended" + Caret, die vorherige eigene Tabbar-Zeile über der Panel-Grid fällt weg → ein vertikaler Block weniger pro Tab-Row. Verhalten (aktiver Tab, Lazy-Loading via Resize, Collapse) bleibt unverändert, nur die Platzierung hat sich geändert.
Ich benötige noch die Fähigkeit einen Zeitpunkt mit einem Label versehen zu können (Annotation). Entsprechend soll dann eine Verticale Linie das Label in allen Pannels anzeigen.
SystemInit:  id=2d146b2a-7fd4-4667-b4aa-7286303ef9db, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5
Control Request:
```yaml
id: 9198b751-14f0-427b-8b0e-0b5b37b0066b
toolName: list
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer
  reason: Projektstruktur verstehen (Backend vorhanden? DB? API?)
```
/answer 9198b751-14f0-427b-8b0e-0b5b37b0066b deny Dass soll rein im der Dashbaord config Annotiert werden und ist statisch.
ReasoningToken: 674
Control Request:
```yaml
id: 1fd081d7-5582-4c63-ad3a-dc8f85a4fc75
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: "function thresholdMarkLine(sc) {"
  end: "const LEGEND_BG = \"rgba(255,255,255,0.72)\";"
  reason: Exakten Text um thresholdMarkLine für den nächsten Einfügepunkt holen
```
/answer 1fd081d7-5582-4c63-ad3a-dc8f85a4fc75 allow
Control Request:
```yaml
id: c6588663-8761-4f51-8127-1b03de106f7b
result:
  structuredContent:
    checksum: 8ef4b3db5ca93765223f20641cbf04f6747a95046b68d9ad6aa7bd7a9092c4e5
    content: |-
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

        /* Floating, semi-transparent legend(s), drawn directly over the plot area
         * instead of taking up their own row. With a right Y-axis in play, series
         * are split into two legend components by axis affiliation: left-axis
         * series top-left, right-axis series top-right. `selected` is shared --
         * each piece only looks up the names it owns, so toggling one doesn't
         * touch the other. No wrapping/scrolling: panels are wide enough. */
        const LEGEND_BG = "rgba(255,255,255,0.72)";
```
/answer c6588663-8761-4f51-8127-1b03de106f7b allow
Control Request:
```yaml
id: 976ea8cf-eb3d-44bb-9af7-0bdc39d7839f
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: "function buildStateBand(cfg, xy) {"
  end: "/* Type \"daily\" panels:"
  reason: buildStateBand exakt für Annotation-Integration lesen
```
/answer 976ea8cf-eb3d-44bb-9af7-0bdc39d7839f allow
Control Request:
```yaml
id: f7c1a0c9-1b7b-474a-a5a2-932a929806ab
result:
  structuredContent:
    checksum: b2c1e4a5f3f95dd9ed1e1fc02f5a543b90ef005826b73aa7f2cb06360efac50c
    content: |-
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
            grid: { left: 64, right: 64, top: GRID_TOP, bottom: gridBottom(cfg) },
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

        /* Type "daily" panels:
```
/answer f7c1a0c9-1b7b-474a-a5a2-932a929806ab allow
ReasoningToken: 6042
Text:
 Jetzt die Annotation-Helper einfügen und in beiden Renderern (`buildTimeseries`, `buildStateBand`) verankern:
Control Request:
```yaml
id: c3b72389-1a02-45c4-b357-0e79a11f750b
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
      /* Floating, semi-transparent legend(s), drawn directly over the plot area
       * instead of taking up their own row. With a right Y-axis in play, series
       * are split into two legend components by axis affiliation: left-axis
       * series top-left, right-axis series top-right. `selected` is shared --
       * each piece only looks up the names it owns, so toggling one doesn't
       * touch the other. No wrapping/scrolling: panels are wide enough. */
      const LEGEND_BG = "rgba(255,255,255,0.72)";
  new_text: |2-
      /* ---- static annotations (config-driven, `DASHBOARD.annotations`) -----
       * A labelled, dashed vertical line drawn at a fixed point in time, on
       * every synced timeseries/state panel (not on "daily" panels, which run
       * on their own independent, day-aggregated time axis). Purely declarative
       * -- set in the dashboard config, see dashboard.config.js; there's no
       * interactive "add annotation" UI. */
      const ANNOTATION_COLOR = "#8250df";
      function resolvedAnnotations() {
        return (DASHBOARD.annotations || [])
          .map((a) => ({ t: resolveTime(a.time, NaN), label: a.label, color: a.color }))
          .filter((a) => isFinite(a.t) && a.t >= fromMs && a.t <= toMs);
      }
      function annotationMarkLine() {
        const list = resolvedAnnotations();
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
      /* An invisible, empty carrier series purely to host the annotation
       * markLine -- works uniformly regardless of a panel's own series (e.g. a
       * "state" panel's single custom-rendered band). */
      function annotationSeries() {
        const markLine = annotationMarkLine();
        return markLine
          ? [{ type: "line", data: [], silent: true, showSymbol: false, markLine }]
          : [];
      }

      /* Floating, semi-transparent legend(s), drawn directly over the plot area
       * instead of taking up their own row. With a right Y-axis in play, series
       * are split into two legend components by axis affiliation: left-axis
       * series top-left, right-axis series top-right. `selected` is shared --
       * each piece only looks up the names it owns, so toggling one doesn't
       * touch the other. No wrapping/scrolling: panels are wide enough. */
      const LEGEND_BG = "rgba(255,255,255,0.72)";
  reason: Annotation-Helper (Zeitmarken aus DASHBOARD.annotations als Trage-Serie mit markLine) ergänzen
```
/answer c3b72389-1a02-45c4-b357-0e79a11f750b allow
Control Request:
```yaml
id: 8c7cc21f-c421-409c-b492-0aad71d4313c
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: |2-
        return {
          backgroundColor: "transparent", animation: false,
          textStyle: { color: "#1f2328" },
          tooltip: { trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip },
          legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
  end: |2-
          dataZoom: insideZoom(),
          series,
        };
      }
  reason: Exakten Rückgabeblock von buildTimeseries für die Erweiterung um annotationSeries() holen
```
/answer 8c7cc21f-c421-409c-b492-0aad71d4313c allow
Control Request:
```yaml
id: 6db043e0-62fe-4f16-bee4-d788a8734392
result:
  content:
  - type: text
    text: End marker is ambiguous – found 2 occurrences in file.
  isError: true
```
/answer 6db043e0-62fe-4f16-bee4-d788a8734392 allow
Control Request:
```yaml
id: 0e41175f-4b86-4e42-9dd3-17274ff591d3
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: "function buildTimeseries(cfg, fetched, legendSelected) {"
  max_line: 330
  reason: buildTimeseries komplett nach den letzten Änderungen sehen für präzisen Insert-Punkt
```
/answer 0e41175f-4b86-4e42-9dd3-17274ff591d3 allow
Control Request:
```yaml
id: 3636e91f-0b77-4cd7-a264-a8e95054be43
result:
  structuredContent:
    checksum: 103b93702438a499bd27f2ae27a05fa51e5295d5a945595b0537a99467dede4d
    content: |
      function buildTimeseries(cfg, fetched, legendSelected) {
          const leftNames = [], rightNames = [];
          const series = [];
          cfg.series.forEach((sc) => {
            const yIdx = sc.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
            const data = fetched.get(sc);
            const step = cfg.type === "state" ? "end" : false;
            (yIdx ? rightNames : leftNames).push(sc.label);
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
              (mIdx ? rightNames : leftNames).push(m.label);
              series.push({
                name: m.label, type: "line", yAxisIndex: mIdx,
                showSymbol: false, smooth: true,
                lineStyle: { width: m.width || 2, color: m.color },
```
/answer 3636e91f-0b77-4cd7-a264-a8e95054be43 allow
Control Request:
```yaml
id: f0712c0f-9f9b-4430-b622-b402209b7dd6
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
              data: movingAverage(data, m.size),
            });
          }
        });
        return {
          backgroundColor: "transparent", animation: false,
          textStyle: { color: "#1f2328" },
          tooltip: { trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip },
          legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
  new_text: |2-
              data: movingAverage(data, m.size),
            });
          }
        });
        series.push(...annotationSeries());
        return {
          backgroundColor: "transparent", animation: false,
          textStyle: { color: "#1f2328" },
          tooltip: { trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip },
          legend: cfg.legend ? floatingLegend(leftNames, rightNames, legendSelected) : undefined,
  reason: Annotation-Trage-Serie zu buildTimeseries hinzufügen
```
/answer f0712c0f-9f9b-4430-b622-b402209b7dd6 allow
ReasoningToken: 66
ReasoningToken: 463
Control Request:
```yaml
id: f04210e5-4f72-45a0-87b9-7cd441338ec2
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
          dataZoom: insideZoom(),
          series: [{
            type: "custom", renderItem: makeStageRenderer(states),
            encode: { x: [0, 1] }, clip: true,
            data: buildStageSegments(xy, states),
          }],
        };
      }
  new_text: |2-
          dataZoom: insideZoom(),
          series: [{
            type: "custom", renderItem: makeStageRenderer(states),
            encode: { x: [0, 1] }, clip: true,
            data: buildStageSegments(xy, states),
          }, ...annotationSeries()],
        };
      }
  reason: Annotation-Trage-Serie auch für State-Band-Panels hinzufügen
```
/answer f04210e5-4f72-45a0-87b9-7cd441338ec2 allow
Control Request:
```yaml
id: 06d21549-e620-47d6-8b28-7cf873adf6ec
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  max_line: 10
  reason: Feature-Kommentar am Dateianfang lesen
```
/answer 06d21549-e620-47d6-8b28-7cf873adf6ec allow
Control Request:
```yaml
id: 0cc1fe53-d5e0-4583-83ec-ff4aadffb86f
result:
  structuredContent:
    checksum: df702eeb2d967ba431781ba8c8b1bb58eb899458ea7d2d2946cc014a9c871273
    content: |
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
```
/answer 0cc1fe53-d5e0-4583-83ec-ff4aadffb86f allow
ReasoningToken: 32
Text:
 Jetzt `buildStateBand`:
Control Request:
```yaml
id: f6f6f0ac-4385-4a74-b123-a017f9fab6f1
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  old_text: |2-
     * Features: synced zoom/hover cursor across panels (by axis value, not data
     * index, plus late-join replay), a time selector with quick ranges + shift
     * buttons, lazy (visibility-based) panel loading, thresholds, dual Y-axes,
     * a toggleable legend, collapsible rows and a tab layout.
     */
  new_text: |2-
     * Features: synced zoom/hover cursor across panels (by axis value, not data
     * index, plus late-join replay), a time selector with quick ranges + shift
     * buttons, lazy (visibility-based) panel loading, thresholds, dual Y-axes,
     * a toggleable legend, collapsible rows, a tab layout and labelled, static
     * time annotations shown across all synced panels.
     */
  reason: Feature-Liste im Kopfkommentar um Annotationen ergänzen
```
/answer f6f6f0ac-4385-4a74-b123-a017f9fab6f1 allow
Control Request:
```yaml
id: 6a222342-930c-4df3-a3f6-925fa171a645
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  start: /* ---- Dashboard layout (rows + tabs) ---- */
  reason: "Ende der Config lesen, um annotations-Array einzufügen"
```
/answer 6a222342-930c-4df3-a3f6-925fa171a645 allow
Control Request:
```yaml
id: 5fe2313c-7a54-49d8-8355-669b8ed79471
result:
  structuredContent:
    checksum: 2f706da5eb874a67f538b1c9ea08a441783f6e2d2f83ea890145041d6d6618f2
    content: |
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
```
/answer 5fe2313c-7a54-49d8-8355-669b8ed79471 allow
Text:
 Jetzt den Feature-Kommentar am Dateianfang ergänzen und die Config um das `annotations`-Schema erweitern:
ReasoningToken: 60
Control Request:
```yaml
id: 03da2076-f78f-4bd2-9218-3bb11f246a11
toolName: replace-block
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js
  old_text: |-
    /* ---- Dashboard layout (rows + tabs) ---- */
      window.DASHBOARD = {
        title: "HRV Data",
        rows: [
  new_text: |-
    /* ---- Static time annotations --------------------------------------------
       * A labelled, dashed vertical line drawn at a fixed point in time, on
       * every synced timeseries/state panel (not on the "daily" panels, which
       * run on their own independent, day-aggregated time axis).
       *   time:  "now" | epoch ms | ISO/parseable date string (local, no "Z" ->
       *          interpreted in the browser's local time zone)
       *   label: short text shown on the line
       *   color: optional, defaults to a shared purple */
      const annotations = [
        // { time: "2026-08-14T22:00:00", label: "Bed" },
        // { time: "2026-08-15T07:30:00", label: "Coffee", color: "#e02f44" },
      ];

      /* ---- Dashboard layout (rows + tabs) ---- */
      window.DASHBOARD = {
        title: "HRV Data",
        annotations,
        rows: [
  reason: Annotations-Schema und Beispiel in die Dashboard-Config aufnehmen
```
/answer 03da2076-f78f-4bd2-9218-3bb11f246a11 allow
Text:
 Jetzt die Config um das `annotations`-Array erweitern:
Control Request:
```yaml
id: 26a64be2-a21f-43a0-9ba7-811b822e1920
toolName: bash
arguments:
  cwd: /home/user/xyan/XY.Archiv/hrviewer/statics
  script: node --check dashboard.js && node --check dashboard.config.js && echo OK
  reason: Syntax beider geänderter Dateien prüfen
```
/answer 26a64be2-a21f-43a0-9ba7-811b822e1920 allow
Control Request:
```yaml
id: 31c30cb6-3324-4d35-bdbf-7fea7d1e23ab
result:
  structuredContent:
    stdout: |
      OK
```
/answer 31c30cb6-3324-4d35-bdbf-7fea7d1e23ab allow
Control Request:
```yaml
id: 10e5548c-5426-416a-91a3-d0790b35cd06
toolName: read-file
arguments:
  path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.js
  start: /* ---- static annotations
  end: |-
    function annotationSeries() {
        const markLine = annotationMarkLine();
        return markLine
          ? [{ type: "line", data: [], silent: true, showSymbol: false, markLine }]
          : [];
      }
  reason: Finalen Annotation-Codeblock zur Kontrolle lesen
```
/answer 10e5548c-5426-416a-91a3-d0790b35cd06 allow
Control Request:
```yaml
id: 968c4db2-04fd-4beb-b9e7-68087cb45fd2
result:
  structuredContent:
    checksum: 13b46537f18aa7b9066d96a36fc9ee70385ec78bbf974e172548654190b42e19
    content: |-
      /* ---- static annotations (config-driven, `DASHBOARD.annotations`) -----
         * A labelled, dashed vertical line drawn at a fixed point in time, on
         * every synced timeseries/state panel (not on "daily" panels, which run
         * on their own independent, day-aggregated time axis). Purely declarative
         * -- set in the dashboard config, see dashboard.config.js; there's no
         * interactive "add annotation" UI. */
        const ANNOTATION_COLOR = "#8250df";
        function resolvedAnnotations() {
          return (DASHBOARD.annotations || [])
            .map((a) => ({ t: resolveTime(a.time, NaN), label: a.label, color: a.color }))
            .filter((a) => isFinite(a.t) && a.t >= fromMs && a.t <= toMs);
        }
        function annotationMarkLine() {
          const list = resolvedAnnotations();
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
        /* An invisible, empty carrier series purely to host the annotation
         * markLine -- works uniformly regardless of a panel's own series (e.g. a
         * "state" panel's single custom-rendered band). */
        function annotationSeries() {
          const markLine = annotationMarkLine();
          return markLine
            ? [{ type: "line", data: [], silent: true, showSymbol: false, markLine }]
            : [];
        }
```
/answer 968c4db2-04fd-4beb-b9e7-68087cb45fd2 allow
ReasoningToken: 14
ReasoningToken: 405
**Erledigt.** Neue Fähigkeit: statische Zeit-Annotationen (Label + vertikale Linie) über `dashboard.config.js`, sichtbar in allen synchronisierten Panels.

**Wie es funktioniert:**

- **`dashboard.config.js`**: neues `annotations`-Array, das an `window.DASHBOARD.annotations` gehängt wird:
  ```js
  const annotations = [
    // { time: "2026-08-14T22:00:00", label: "Bed" },
    // { time: "2026-08-15T07:30:00", label: "Coffee", color: "#e02f44" },
  ];
  ```
  `time` akzeptiert dasselbe Format wie `range.from/to` (ISO-String lokal, `"now"` oder Epoch-ms), `label` ist der angezeigte Text, `color` optional (Standard: Lila `#8250df`).

- **`dashboard.js`**: neue Helper `resolvedAnnotations()`, `annotationMarkLine()`, `annotationSeries()`:
  - Annotationen werden auf das aktuell geladene Zeitfenster (`fromMs`/`toMs`) gefiltert.
  - Pro Panel wird eine unsichtbare, leere "Trage-Serie" mit einer `markLine` (gestrichelt, mit Label-Chip in Annotation-Farbe) angehängt – dadurch funktioniert es unabhängig davon, ob das Panel eigene Serien hat.
  - Eingebunden in `buildTimeseries` (alle Timeseries-Panels) **und** `buildStateBand` (Sleep-Stage-Panel).
  - Bewusst **nicht** in `buildDaily`, da die Daily-Panels eine eigene, tagesaggregierte Zeitachse mit eigenem Fenster haben und nicht Teil der Synchronisations-Gruppe sind (`syncable` schließt `type: "daily"` konsequent aus).

- Rein deklarativ/statisch, keine Interaktions-UI zum Hinzufügen – wie gewünscht.

Trage z.B. so ein:
```js
const annotations = [
  { time: "2026-08-14T21:30:00", label: "Bed" },
];
```
und die Linie erscheint in allen Panels des sichtbaren Zeitfensters. `node --check` auf beiden Dateien ist grün.
