Bei den Apache ECharts ist es so das wenn ich in der Legende über eine Serie Hover, die Linie dazu verschwindet. Der Effekt soll wohl eigentlich die Linie hervorheben. Prüfe das. Die Linie soll beim Hervorheben etwas stärker und oder dunkler werden. 

`/home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.html`
`/home/user/xyan/XY.Archiv/hrviewer/statics/dashboard.config.js`
SystemInit:  id=b805a584-572f-45b6-8c50-b75e65cca19d, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5-5
Control Request:
```yaml
id: 5638-1-0
toolName: ast_retrieve
arguments:
  search:
  - directory:
    - /home/user/xyan/XY.Archiv/hrviewer/statics
    pattern: emphasis|blur|legend|lineStyle|focus|selectedMode
    include:
    - dashboard.html
    - dashboard.config.js
    limit: 50
  reason: "Find legend, emphasis and lineStyle config for ECharts series"
```
/answer 5638-1-0 allow
Control Request:
```yaml
id: 5638-2-1
result:
  structuredContent:
    search:
      results:
      - directory:
        - /home/user/xyan/XY.Archiv/hrviewer/statics
        matches:
        - path: dashboard.config.js
          matches:
          - "* + styling), Y-axes, thresholds and legend behaviour; metrics are rendered"
          - "legend: true,"
          - "axisLeft: { label: \"Σ (value + 0.5)\" }, legend: true,"
          - "axisLeft: { label: \"count\", min: 0, max: 50 }, legend: true,"
```
/answer 5638-2-1 allow
Text:
 Die Chart-Erzeugung steht wohl in der HTML-Datei oder in einem eingebundenen Skript.
Control Request:
```yaml
id: 5638-3-0
toolName: ast_retrieve
arguments:
  search:
  - directory:
    - /home/user/xyan/XY.Archiv/hrviewer/statics
    pattern: echarts|setOption|series
    include:
    - '*.html'
    - '*.js'
    exclude:
    - echarts*.js
    - '*.min.js'
    limit: 40
  reason: Locate where ECharts options/series are built
```
/answer 5638-3-0 allow
Control Request:
```yaml
id: 5638-4-3
result:
  structuredContent:
    search:
      results:
      - directory:
        - /home/user/xyan/XY.Archiv/hrviewer/statics
        matches:
        - path: dashboard.config.js
          matches:
          - '* panels into a tab strip. Each panel declares its series (metric + aggregate'
          - "id: 1, type: \"timeseries\", title: \"Heart Rate\", height: 300,"
          - "series: ["
          - "id: 3, type: \"timeseries\", title: \"Autonomic Balance\", height: 240,"
          - "id: 14, type: \"timeseries\", title: \"Vagal Tone\", height: 260,"
          - "id: 4, type: \"timeseries\", title: \"Frequency Power / DFA\", height: 320,"
          - "id: 9, type: \"timeseries\", title: \"Circadian Band Power\", height: 340,"
          - "id: 15, type: \"timeseries\", title: \"Cardiopulmonary Coupling\", height: 320,"
          - "id: 16, type: \"timeseries\", title: \"RR Interval\", height: 320,"
          - "series: sleepSeries,"
        - path: dashboard/panels.flags.js
          matches:
          - "import { seriesData, latestValue } from \"./data.js\";"
          - "fetchLatest: async (sc) => latestValue(await seriesData(sc, getRange(), maxPointsOverride(3000))),"
          - "/* Line colour for chart series: the tile's border colour, so a series has"
          - "export function seriesColor(label) {"
        - path: dashboard/data.js
          matches:
          - "* moving average, derived/\"transformed\" series). Fully parametrized --"
          - "function seriesQueryBody(q, range, maxPoints) {"
          - "kind: \"series\", segment: q.segment, metric: q.metric,"
          - "/* Fetch metric; missing data yields empty series (not cached, so retried later). */"
          - "return toXY(await cachedFetchTable(seriesQueryBody(q, range, maxPoints)), \"value\");"
          - "console.warn(\"query failed (treated as empty series):\","
          - "export async function seriesData(sc, range, maxPoints) {"
          - '* Reduces a fetched series to its most recent (last non-null) value. */'
        - path: dashboard/charts.daily.js
          matches:
          - "const legendData = [], series = [];"
          - "cfg.series.forEach((sc) => {"
          - "series.push({"
          - if (cfg.legend) series.push(...legendAllGhostSeries());
          - "series,"
        - path: dashboard/charts.common.js
          matches:
          - "* (timeseries/state-line, categorical state band, daily). Kept"
          - '* since every timeseries/state panel is pinned to the same window.'
          - /* Empty series to host annotation markLines. */
          - /* ECharts drops any legend.data entry that has no matching series */
        warnings:
        - "Limit of 40 matches reached (total 119); narrow pattern, directory or include/exclude filters, or raise limit (max 50)."
```
/answer 5638-4-3 allow
Control Request:
```yaml
id: 5638-5-0
toolName: ast_retrieve
arguments:
  search:
  - directory:
    - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard
    pattern: "emphasis|blur|focus|lineStyle|width:|opacity|series.push|type: \"line\""
    include:
    - '*.js'
    limit: 50
  reason: Find line series definitions and emphasis settings
```
/answer 5638-5-0 allow
Control Request:
```yaml
id: 5638-6-5
result:
  structuredContent:
    search:
      results:
      - directory:
        - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard
        matches:
        - path: charts.daily.js
          matches:
          - "series.push({"
          - "name: sc.label, type: \"line\", data: toXY(table, sc.column),"
          - "lineStyle: { width: 2, color: sc.color },"
          - "areaStyle: { opacity: 0.5, color: sc.color },"
          - if (cfg.legend) series.push(...legendAllGhostSeries());
          - "trigger: \"axis\", axisPointer: { type: \"line\" }, valueFormatter: fmtTip,"
          - "axisLine: { lineStyle: { color: BORDER } },"
        - path: charts.common.js
          matches:
          - "axisLine: { lineStyle: { color: BORDER } },"
          - "splitLine: { lineStyle: { color: GRID } },"
          - "lineStyle: { type: dashed ? \"dashed\" : \"solid\", width: 1 },"
          - "yAxis: st.value, lineStyle: { color: st.color },"
          - "lineStyle: { type: \"dashed\", width: 1, color: ANNOTATION_COLOR },"
          - "lineStyle: { color: a.color || ANNOTATION_COLOR },"
          - "? [{ type: \"line\", data: [], silent: true, showSymbol: false, markLine }]"
          - "name: ALL_LEGEND_LABEL, type: \"line\", data: [], showSymbol: false,"
          - "lineStyle: { color: \"#8b949e\" }, itemStyle: { color: \"#8b949e\" },"
          - '"width:9px;height:9px;border-radius:50%;background:" + color + '';"></span>'';'
        - path: charts.stateband.js
          matches:
          - "shape: { x: x0, y: cs.y, width: w, height: cs.height },"
          - "fill: m.text, fontSize: 10, width: w - 6,"
          - "trigger: \"axis\", axisPointer: { type: \"line\" },"
        - path: charts.timeseries.js
          matches:
          - "series.push({"
          - "name: sc.label, type: \"line\", yAxisIndex: yIdx,"
          - "lineStyle: { width: sc.width == null ? 1 : sc.width, color, type: sc.dash || \"solid\" },"
          - "areaStyle: sc.fillOpacity ? { opacity: sc.fillOpacity / 100, color } : undefined,"
          - "name: m.label, type: \"line\", yAxisIndex: mIdx,"
          - "lineStyle: { width: m.width || 2, color: mColor },"
          - "areaStyle: m.fillOpacity ? { opacity: m.fillOpacity / 100, color: mColor } : undefined,"
          - series.push(...annotationSeries(range));
          - if (cfg.legend) series.push(...legendAllGhostSeries());
          - "trigger: \"axis\", axisPointer: { type: \"line\", snap: false },"
```
/answer 5638-6-5 allow
ReasoningToken: 133
Control Request:
```yaml
id: 5638-7-0
toolName: ast_retrieve
arguments:
  find:
  - paths:
    - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.timeseries.js
    text: "series.push({"
  - paths:
    - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.common.js
    text: legendAllGhostSeries
  reason: Read series construction and ghost legend series
```
/answer 5638-7-0 allow
Control Request:
```yaml
id: 5638-8-7
result:
  structuredContent:
    find:
      results:
      - path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.timeseries.js
        nodes:
        - id: buildTimeseries
          code: |-
            export function buildTimeseries(cfg, fetched, legendSelected, range, chart) {
              const leftNames = [], rightNames = [];
              const series = [];
              const seriesInfo = new Map();
              let paletteIdx = 0;
              const nextColor = () => DEFAULT_PALETTE[paletteIdx++ % DEFAULT_PALETTE.length];
              cfg.series.forEach((sc) => {
                const yIdx = sc.axis === "right" && cfg.axisRight && cfg.axisRight.show ? 1 : 0;
                const data = fetched.get(sc);
                const step = cfg.type === "state" ? "end" : false;
                const color = sc.color || seriesColor(sc.label);
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
              if (cfg.legend) series.push(...legendAllGhostSeries());
              return {
                backgroundColor: "transparent", animation: false,
                textStyle: { color: "#1f2328" },
                // snap: false -- ECharts snaps the axis pointer (and thus `axisValue`
                // in the tooltip formatter) to the nearest *data point* by default on
                // a continuous time axis; that defeats the whole point of computing
                // our own interpolated/held value below the actual cursor position.
                tooltip: {
                  trigger: "axis", axisPointer: { type: "line", snap: false },
                  position: tooltipPosition(gridBottom(cfg)),
                  formatter: axisTooltipFormatter(seriesInfo, chart),
                },
                legend: cfg.legend
                  ? floatingLegend(leftNames, rightNames, legendSelectedWithAll(leftNames.concat(rightNames), legendSelected))
                  : undefined,
                // Fixed margins for synced hover cursor alignment across panels
                grid: { left: 64, right: 64, top: GRID_TOP, bottom: gridBottom(cfg) },
                xAxis: timeXAxis(cfg, range),
                yAxis: baseYAxis(cfg),
                dataZoom: insideZoom(),
                series,
              };
            }
      - path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.common.js
        nodes:
        - id: legendAllGhostSeries
          code: |-
            export function legendAllGhostSeries() {
              return [{
                name: ALL_LEGEND_LABEL, type: "line", data: [], showSymbol: false,
                silent: true, legendHoverLink: false, animation: false,
                lineStyle: { color: "#8b949e" }, itemStyle: { color: "#8b949e" },
              }];
            }
```
/answer 5638-8-7 allow
ReasoningToken: 120
Control Request:
```yaml
id: 5638-9-0
toolName: ast_retrieve
arguments:
  search:
  - directory:
    - /home/user/xyan/XY.Archiv/hrviewer/statics
    pattern: highlight|downplay|legendhover|legendHover|inactiveColor|floatingLegend
    include:
    - '*.js'
    - '*.html'
    exclude:
    - echarts*.js
    - '*.min.js'
    limit: 30
  reason: Check for custom legend hover handling
```
/answer 5638-9-0 allow
Control Request:
```yaml
id: 5638-a-9
result:
  structuredContent:
    search:
      results:
      - directory:
        - /home/user/xyan/XY.Archiv/hrviewer/statics
        matches:
        - path: dashboard/charts.daily.js
          matches:
          - "import { AXIS, BORDER, baseYAxis, insideZoom, thresholdMarkLine, floatingLegend, legendSelectedWithAll, legendAllGhostSeries, fmtTip, tooltipPosition } from \"./charts.common.js\";"
          - "? floatingLegend(legendData, [], legendSelectedWithAll(legendData, legendSelected))"
        - path: dashboard/charts.common.js
          matches:
          - "silent: true, legendHoverLink: false, animation: false,"
          - "export function floatingLegend(leftNames, rightNames, selected) {"
        - path: dashboard/charts.timeseries.js
          matches:
          - "thresholdMarkLine, annotationSeries, floatingLegend, legendSelectedWithAll, legendAllGhostSeries,"
          - "? floatingLegend(leftNames, rightNames, legendSelectedWithAll(leftNames.concat(rightNames), legendSelected))"
        - path: blockly/blockly_compressed.js
          matches:
          - "ui=function(){var a=x.registry.createSerializedKey(L.ENTER,[L.CTRL_CMD]),b=x.registry.createSerializedKey(L.F10,[L.SHIFT]);x.registry.register({name:K…textMenu(d);let e;(e=Dg)==null||e.highlightNext();return!0}return!1},keyCodes:[a,b,L.CONTEXT_MENU],displayText:()=>$.C.SHORTCUTS_SHOW_CONTEXT_MENU})};"
          - /* The selection ring is a decorative highlight that can also be the workspace's
          - "\"translate(0, \"+e+\")\"))}else{f=this.zoomResetControl?this.LARGE_SPACING+this.HEIGHT:0;let h;(h=this.zoomInControl)==null||h.getFocusableElement().setA…enabled?\"\":\"blocklyMenuItemDisabled \")+(this.checked?\"blocklyMenuItemSelected \":\"\")+(this.highlight?\"blocklyMenuItemHighlight \":\"\")+(this.rightToLeft?"
          - "this.checked),l(a,p.SELECTED,this.checked)}setHighlighted(a){this.highlight=a;if(this.isEnabled()){let b;(b=this.getElement())==null||b.classList.togg…ction(a){this.isEnabled()&&this.actionHandler&&this.actionHandler(this,a)}onAction(a,b){this.actionHandler=a.bind(b)}toggleHasCheckbox(a){if(a){let d;"
          - "if((d=this.getElement())==null||!d.querySelector(\".blocklyMenuItemContent .blocklyMenuItemCheckbox\")){a=document.createElement(\"div\");l(a,p.HIDDEN,!0)….getId();this.roleName&&ya(b,this.roleName);this.element=b;for(let c=0,d;d=this.menuItems[c];c++)b.appendChild(d.createDom());this.pointerMoveHandler="
          - "this.getElement();a&&a!==b;){if(a.classList.contains(\"blocklyMenuItem\")){let c=this.getMenuItems();for(let d=0,e;e=c[d];d++)if(e.getElement()===a)retu…ent();b&&c&&(fc(c,b),l(b,p.ACTIVEDESCENDANT,a.getId()))}}highlightNext(){var a=this.highlightedItem?this.getMenuItems().indexOf(this.highlightedItem):"
          - "-1;this.highlightHelper(a,1)}highlightPrevious(){var a=this.highlightedItem?this.getMenuItems().indexOf(this.highlightedItem):-1;this.highlightHelper(…)){this.setHighlighted(c);break}a+=b}}handlePointerMove(a){Math.max(Math.abs(a.movementX),Math.abs(a.movementY))!==0&&(a=this.getMenuItem(a.target))&&"
          - "(a.isEnabled()?this.highlightedItem!==a&&this.setHighlighted(a):this.setHighlighted(null))}handleClick(a){var b=this.openingCoords;this.openingCoords=…nt()&&this.setHighlighted(null)}handleKeyEvent(a){if(this.menuItems.length&&!(a.shiftKey||a.ctrlKey||a.metaKey||a.altKey)){var b=this.highlightedItem;"
          - "switch(a.key){case \"Enter\":case \" \":b&&b.performAction(a);break;case \"ArrowUp\":this.highlightPrevious();break;case \"ArrowDown\":this.highlightNext();br…ast\";b=f.appendChild(document.createElement(\"div\"));b.className=\"blocklyToastMessage\";b.innerText=c;b=f.appendChild(document.createElement(\"button\"));"
          - "`${a}`);this.icon.setAttribute(\"x\",`${b.width-this.getSize(!0).getWidth()}`)}performAction(a){ha=null;a&&a instanceof PointerEvent&&na(a)?a.stopPropag…able\"});ya(this.svgRoot,Ka.BUTTON);l(this.svgRoot,p.ROLEDESCRIPTION,$.C.ARIA_LABEL_COMMENT);this.highlightRect=this.createHighlightRect(this.svgRoot);"
          - "b&&(c+=4);return new hc(c,a.height+20)}updateHighlightRect(a){this.highlightRect.setAttribute(\"height\",`${a.height}`);this.highlightRect.setAttribute(….height)/2;var d=this.foldoutButton.getSize(!0),e=this.deleteButton.getSize(!0);a=a.width-d.getWidth()-e.getWidth();this.textPreview.setAttribute(\"x\","
          - "Hh(a,b);)if(a=c.targetBlock(),!a||a.isShadow()){b=c;break a}b=null}return b}a=a.lastConnectionInStack(!0);c=b.getConnectionChecker();return a&&c.canCo…nectionHighlight)==null||b.call(a,this)}getSourceBlock(){return super.getSourceBlock()}targetBlock(){return super.targetBlock()}distanceFrom(a){var b="
          - "var b,c,d,e=(d=this.getParentInput())!=null?d:(b=this.getSourceBlock().getTopStackBlock().previousConnection)==null?void 0:(c=b.targetConnection)==nul…e l(a,p.LABEL,$.C.INPUT_LABEL_EMPTY)}highlight(){this.highlighted=!0;var a=this.findHighlightSvg();a&&(n(a,\"blocklyHighlightedConnectionPathVisible\"),"
          - "requestAnimationFrame(()=>{var b=a.parentElement;if(b)for(;a.nextSibling;)b.insertBefore(a.nextSibling,a)}),this.recomputeAriaContext(a))}unhighlight(…kedState===Mi.TrackedState.UNTRACKED||this.sourceBlock_.isInFlyout||(a?(this.db.addConnection(this,this.y),this.trackedState=Mi.TrackedState.TRACKED):"
          - "a);if(b.length){var c=this.getSourceBlock(),d=c.workspace;if(a instanceof PointerEvent)var e=new D(a.clientX,a.clientY);else e=new D(this.x,this.y),e=…Tree(){return this.getSourceBlock().workspace}onNodeFocus(){this.highlight();var a=this.getSourceBlock();a.workspace.isFlyout||a.moveSvgRootToFront();"
          - "a.workspace.scrollBoundsIntoView(a.getBoundingRectangleWithoutChildren())}onNodeBlur(){this.unhighlight()}canBeFocused(){return this.findHighlightSvg(…r=void 0}getInsertionMarker(){return this.insertionMarker}},Hn=Mi||(Mi={}),In=Hn.TrackedState||(Hn.TrackedState={});In[In.WILL_TRACK=-1]=\"WILL_TRACK\";"
          - "a)+c;this.descenderHeight=c;this.widthWithConnectedBlocks=this.width}startsWithElemSpacer(){return!1}endsWithElemSpacer(){return!1}};var Qo=class exte…nnectedBlock.getHeightWidth(),this.connectedBlockWidth=b.width,this.connectedBlockHeight=b.height);a&&(a=a.getHeightWidth(),this.connectedBlockWidth+="
          - "c&&(b.connectionModel.setAriaRole(c),c.classList.toggle(\"blocklyHighlightedConnectionPathVisible\",b.highlighted))}}drawConnectionHighlightPath(a){var …addConnectionHighlight)==null?void 0:e.call(d,b,a,b.getOffsetInBlock(),c.RTL)}getExpressionConnectionHighlightPath(a){var b=\"\";if(a.shape.isDynamic)b="
          - "this.startY=this.topRow.capline;this.bottomRow.baseline=b-this.bottomRow.descenderHeight}getMeasureableForConnection(a){var b;if(((b=this.outputConnec….svgPath.setAttribute(\"stroke\",this.style.colourTertiary);this.svgPath.setAttribute(\"fill\",this.style.colourPrimary);this.updateShadow_(a.isShadow());"
          - "a}getMuted(){return this.muted}};var vp=class{constructor(a,b){this.workspace=a;this.element=b}getFocusableElement(){return this.element}getFocusableT…his.injectionDiv=this.currentGesture_=this.toolbox=this.flyout=this.scrollbar=this.trashcan=null;this.inverseScreenCTMDirty=!0;this.highlightedBlocks="
          - "b.getDescendants(!1)).filter(b=>b.isInsertionMarker()).forEach(b=>b.queueRender())}highlightBlock(a,b){if(b===void 0){for(let c=0,d;d=this.highlighted…(a.type){case v.VAR_CREATE:case v.VAR_DELETE:case v.VAR_RENAME:case v.VAR_TYPE_CHANGE:this.refreshToolboxSelection()}}refreshToolboxSelection(){var a="
          - "b&&a.nextConnection.tightenEfficiently()}};var Gp=class extends lp{constructor(){super();this.FIELD_TEXT_BASELINE_CENTER=!1;this.DARK_PATH_OFFSET=1;th…ghtConstants_.INSIDE_CORNER;this.puzzleTabPaths_=this.highlightConstants_.PUZZLE_TAB;this.notchPaths_=this.highlightConstants_.NOTCH;this.startPaths_="
          - "this.highlightConstants_.START_HAT;this.jaggedTeethPaths_=this.highlightConstants_.JAGGED_TEETH}getPath(){return this.steps_+\"\\n\"+this.inlineSteps_}dr…erPaths_.topLeft(this.RTL_):Q.isPreviousConnection(c)?this.steps_+=this.notchPaths_.pathLeft:Q.isHat(c)?this.steps_+=this.startPaths_.path(this.RTL_):"
          - "Q.isSpacer(c)&&c.width!==0&&(this.steps_+=I(\"H\",c.xPos+c.width-this.highlightOffset));this.steps_+=I(\"H\",a.xPos+a.width-this.highlightOffset)}drawJagg…ht-b.connectionHeight;this.steps_+=Ch(b.xPos+b.width-this.highlightOffset,a.yPos)+this.puzzleTabPaths_.pathDown(this.RTL_)+I(\"v\",c)}else this.steps_+="
        warnings:
        - "Limit of 30 matches reached (total 40); narrow pattern, directory or include/exclude filters, or raise limit (max 50)."
        - 23 match line(s) exceeded 300 characters and were shortened in the middle.
```
/answer 5638-a-9 allow
ReasoningToken: 209
Control Request:
```yaml
id: 5638-b-0
toolName: ast_retrieve
arguments:
  find:
  - paths:
    - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.common.js
    name: floatingLegend
  reason: Inspect legend config
```
/answer 5638-b-0 allow
Control Request:
```yaml
id: 5638-c-b
result:
  structuredContent:
    find:
      results:
      - path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.common.js
        nodes:
        - id: floatingLegend
          code: |-
            export function floatingLegend(leftNames, rightNames, selected) {
              // "All" rides along with whichever side actually has entries (left
              // preferred), toggling every series across both sides.
              if (leftNames.length || rightNames.length) {
                (leftNames.length ? leftNames : rightNames).push(ALL_LEGEND_LABEL);
              }
              const pieces = [
                legendPiece(leftNames, "left", selected),
                legendPiece(rightNames, "right", selected),
              ].filter(Boolean);
              return pieces.length ? pieces : undefined;
            }
```
/answer 5638-c-b allow
Control Request:
```yaml
id: 5638-d-0
toolName: ast_retrieve
arguments:
  find:
  - paths:
    - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.common.js
    name: legendPiece
  reason: Inspect legendPiece
```
/answer 5638-d-0 allow
Control Request:
```yaml
id: 5638-e-d
result:
  structuredContent:
    find:
      results:
      - path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.common.js
        nodes:
        - id: legendPiece
          code: |-
            function legendPiece(names, side, selected) {
              if (!names.length) return null;
              return {
                data: names, selected, top: 4, [side]: 8,
                backgroundColor: LEGEND_BG, borderRadius: 4, padding: [3, 8],
                textStyle: { color: AXIS, fontWeight: "bold" }, icon: "roundRect",
              };
            }
```
/answer 5638-e-d allow
Control Request:
```yaml
id: 5638-f-0
toolName: ast_retrieve
arguments:
  find:
  - paths:
    - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.daily.js
    text: "series.push({"
  reason: Read daily series block
```
/answer 5638-f-0 allow
Control Request:
```yaml
id: 5638-10-f
result:
  structuredContent:
    find:
      results:
      - path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.daily.js
        nodes:
        - id: buildDaily
          code: |-
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
              if (cfg.legend) series.push(...legendAllGhostSeries());
              return {
                backgroundColor: "transparent", animation: false,
                tooltip: {
                  trigger: "axis", axisPointer: { type: "line" }, valueFormatter: fmtTip,
                  position: tooltipPosition(44),
                },
                legend: cfg.legend
                  ? floatingLegend(legendData, [], legendSelectedWithAll(legendData, legendSelected))
                  : undefined,
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
```
/answer 5638-10-f allow
ReasoningToken: 304
Control Request:
```yaml
id: 5638-11-0
toolName: ast_retrieve
arguments:
  search:
  - directory:
    - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard
    pattern: ^import .*charts.common|^export function legendPiece|^function legendPiece
    include:
    - charts.timeseries.js
    - charts.common.js
    limit: 5
  reason: Check imports
```
/answer 5638-11-0 allow
Control Request:
```yaml
id: 5638-12-11
result:
  structuredContent:
    search:
      results:
      - directory:
        - /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard
        matches:
        - path: charts.common.js
          matches:
          - "function legendPiece(names, side, selected) {"
```
/answer 5638-12-11 allow
ReasoningToken: 29
Control Request:
```yaml
id: 5638-13-0
toolName: ast_edit
arguments:
  insert:
  - id: legendAllGhostSeries
    path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.common.js
    position: before
    source: |+
      /* Legend/series hover: thicken the hovered line and fade the others. Explicit
       * widths -- ECharts' default "bolder" can make thin lines vanish. */
      export function lineEmphasis(width) {
        return {
          focus: "series", blurScope: "coordinateSystem",
          lineStyle: { width: Math.max(width, 1) + 2 },
        };
      }

  edit_block:
  - id: buildTimeseries
    path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.timeseries.js
    old_text: |2-
            itemStyle: { color },
            areaStyle: sc.fillOpacity
    new_text: |2-
            itemStyle: { color },
            emphasis: lineEmphasis(sc.width == null ? 1 : sc.width),
            areaStyle: sc.fillOpacity
  - id: buildTimeseries
    path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.timeseries.js
    old_text: |2
              itemStyle: { color: mColor },
    new_text: |2
              itemStyle: { color: mColor },
              emphasis: lineEmphasis(m.width || 2),
  - id: buildDaily
    path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.daily.js
    old_text: |2
            itemStyle: { color: sc.color },
    new_text: |2
            itemStyle: { color: sc.color },
            emphasis: lineEmphasis(2),
  reason: "Add explicit emphasis (thicker line, dim others) to line series"
```
/answer 5638-13-0 allow
Text:
 Jetzt die Imports ergänzen.
Control Request:
```yaml
id: 5638-14-0
toolName: ast_edit
arguments:
  edit_block:
  - id: imp1
    path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.daily.js
    old_text: "legendAllGhostSeries, fmtTip, tooltipPosition }"
    new_text: "legendAllGhostSeries, lineEmphasis, fmtTip, tooltipPosition }"
  - id: imp2
    path: /home/user/xyan/XY.Archiv/hrviewer/statics/dashboard/charts.timeseries.js
    old_text: "floatingLegend, legendSelectedWithAll, legendAllGhostSeries,"
    new_text: "floatingLegend, legendSelectedWithAll, legendAllGhostSeries, lineEmphasis,"
  reason: Import lineEmphasis
```
/answer 5638-14-0 allow
Result Stats: id=b805a584-572f-45b6-8c50-b75e65cca19d, total: 19066, in: 22, out: 4341, reason: 0, read: 125224, write: 14703, start: 1795423884555, end: 1795423890108, time: 5489, total: 38427, io: 0, control: 64, sent: 0, recv: 147
Ich habe die Hervorhebung beim Legenden-Hover geändert. Getestet habe ich es nicht, weil ich den Dashboard-Code nicht im Browser ausgeführt habe.

**Befund:** Weder `dashboard.html` noch `dashboard.config.js` enthalten `emphasis`-Einstellungen. Die Charts entstehen in `statics/dashboard/charts.timeseries.js` und `charts.daily.js`. Dort gab es keine eigene Hover-Logik, und `emphasis` war nirgends gesetzt. Beim Hover griff deshalb nur das ECharts-Standardverhalten. Es verbreitert die Linie relativ ("bolder"). Bei den dünnen Linien (Standardbreite 1) kann das so ausfallen, dass sie verschwinden. Das ist eine Vermutung, ich habe es nicht nachgestellt.

**Änderung:**
- `charts.common.js`: neuer Helfer `lineEmphasis(width)`. Er macht die Linie beim Hover um 2 px breiter als normal. Außerdem setzt er `focus: "series"`, damit die übrigen Serien abgeblendet werden.
- `charts.timeseries.js`: Der Helfer ist bei den Serien und bei den gleitenden Mittelwerten eingetragen, jeweils mit deren eigener Breite.
- `charts.daily.js`: Der Helfer ist bei den Serien des Tagesdiagramms eingetragen. Die Imports habe ich in beiden Dateien ergänzt.

Dunkler wird die Linie nicht. ECharts hebt Farben beim Hover nicht von selbst an. Das Abblenden der anderen Linien verstärkt den Kontrast aber. Wenn du zusätzlich eine dunklere Farbe willst, kann ich sie über `emphasis.lineStyle.color` ergänzen.

Bitte lade das Dashboard neu und teste den Hover. Wenn die Linie weiter verschwindet, sag mir Bescheid. Dann liegt die Ursache an anderer Stelle, etwa in der ECharts-Version.
