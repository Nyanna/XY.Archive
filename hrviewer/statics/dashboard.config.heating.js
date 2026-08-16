/* Heating / indoor-climate dashboard config, consumed by the generic renderer
 * in dashboard.js. Select it via dashboard.html's `?config=heating` URL
 * parameter (-> this file, dashboard.config.heating.js).
 *
 * This is the port of the Grafana/VictoriaMetrics dashboard
 * `project/dashboard_vm.json` ("Heating"). It exercises several generic base
 * features:
 *   - a central sensor-id -> label mapping (SENSORS), one query == one sensor;
 *   - a shared query cache: the raw Temperature/Humidity series of a sensor
 *     are fetched only once even though five panels build on them;
 *   - transformed series: absolute/relative humidity, dew point, enthalpy and
 *     the "ventilate now" value are all derived point-by-point from the same
 *     raw T/H via a `transform` function (no extra backend queries);
 *   - a "flag" panel type: the ventilation recommendation and the window
 *     contact are shown as a momentary binary badge from the latest sample;
 *   - global header links (DASHBOARD.links);
 *   - auto-refresh while on a rolling "Last *" range (handled by the base).
 */
(function () {
  "use strict";

  /* ---- central sensor mapping (Zigbee id -> friendly label) -------------
   * In this domain one metric query == one sensor (segment = sensor id,
   * metric = the measured field, e.g. "Temperature"). This map is the single
   * place that names the sensors; panels reference the ids below. Add/rename
   * sensors here only. */
  const SENSORS = {
    "0x00158d00087be14f": "Garten",          // outdoor reference
    "0x00124b00292abb11": "Wohnzimmer",
    "0x00124b00292fc600": "Schlafzimmer",
    "0x44e2f8fffe33bcad": "Bad",
    "0x00124b002a6d6fd8": "Keller",
    "0x00124b0022d5a1f7": "Waschraum",
    "0x00124b00252be376": "Hobby",
    "0x00124b00290fb077": "Büro",
    "0xf0d1b8be2409fc48": "Werkstatt",
    "0x00124b002a50c50a": "Gästebad",
    "0x00124b00292b470a": "Kira",
    "0x00124b002a6d3c44": "Yuna",
    "0x44e2f8fffe27e73c": "Aura",
    "0x94deb8fffe41e3c0": "Kimi",
    // --- non-climate / special-purpose sensors (used by dedicated panels) ---
    "0xa4c1383c7d3c4cb5": "WW Tank",         // hot-water tank temperature
    "0xa4c138edbd20f773": "Heizung",         // heating power draw
    "0xa4c138ef06c68248": "Badfenster",      // window contact
    "0x60a423fffe803811": "Büroschalter",
    "0x60a423fffe833581": "Garderobenschalter",
    "0xa4c138a66cdb21ae": "Garage Wendy",
    "0xa4c1387253897923": "Kimi Hifi",
    "0x00124b00292afee5": "Yuna Alt",
    "0x00124b00292f6152": "Aura Alt",
    "0xa4c1384225a2fdc6": "Bad Alt",
    "0xa4c1380d85a6455f": "Espresso",
    "0xbc33acfffe5d27d5": "Fernbedienung",
    "0x00124b0026b82cce": "Netzwerk",
    "0x001788010ea481b2": "Philips",
    "0x00124b00252be456": "Xyan",
    "0x00124b002a50c346": "Kellerfenster",
  };
  const label = (id) => SENSORS[id] || id;

  /* Outdoor reference sensor used by the ventilation calculation. */
  const REF = "0x00158d00087be14f";

  /* Room-climate sensors that report Temperature + Humidity. The order here is
   * the plot/legend order. Garten (outdoor) is included and drawn dotted. */
  const CLIMATE = [
    REF,
    "0x00124b00292abb11", "0x00124b00292fc600", "0x44e2f8fffe33bcad",
    "0x00124b002a6d6fd8", "0x00124b0022d5a1f7", "0x00124b00252be376",
    "0x00124b00290fb077", "0xf0d1b8be2409fc48", "0x00124b002a50c50a",
    "0x00124b00292b470a", "0x00124b002a6d3c44", "0x44e2f8fffe27e73c",
    "0x94deb8fffe41e3c0",
  ];
  /* Indoor sensors only (for the ventilation flag): all climate minus outdoor. */
  const INDOOR = CLIMATE.filter((id) => id !== REF);

  /* ---- psychrometrics (Magnus formula, mirrors the VM PromQL exprs) -----
   * T in °C, H in %RH. */
  const satP = (T) => 6.112 * Math.exp((17.67 * T) / (T + 243.5)); // sat. vapour pressure [hPa]
  const vapP = (T, H) => satP(T) * H / 100;                        // actual vapour pressure [hPa]
  const absHumidity = (T, H) => (satP(T) * H * 2.1674) / (273.15 + T); // [g/m³]
  const enthalpy = (T, H) => {                                     // moist-air enthalpy [kJ/kg]
    const pv = vapP(T, H);
    return 1.006 * T + 0.62198 * pv / (1013.25 - pv) * (2501 + 1.86 * T);
  };
  const dewpoint = (T, H) => {                                     // dew point [°C]
    const g = Math.log(H / 100) + (17.67 * T) / (T + 243.5);
    return 243.5 * g / (17.67 - g);
  };
  const clampMax = (x, m) => (x > m ? m : x);
  /* Ventilation benefit vs. the outdoor reference: product of three ratios,
   * each capped at 1 (matches panel 34's PromQL verbatim). Value == 1 means
   * opening the window would improve humidity, enthalpy *and* temperature. */
  const ventilate = (Ts, Hs, Tr, Hr) =>
    clampMax(satP(Ts) / (satP(Tr) * Hr / 100), 1) *
    clampMax(enthalpy(Ts, Hs) / enthalpy(Tr, Hr), 1) *
    clampMax((Ts + 273.15) / (Tr + 273.15), 1);

  /* ---- series builders --------------------------------------------------
   * Garten (the outdoor reference) is emphasised: dotted, thicker line. */
  const T = (id) => ({ key: "T", segment: id, metric: "Temperature", agg: "avg" });
  const H = (id) => ({ key: "H", segment: id, metric: "Humidity", agg: "avg" });
  const styleFor = (id) => (id === REF ? { dash: "dotted", width: 3 } : { width: 1 });

  const rawSeries = (ids, metric) => ids.map((id) =>
    Object.assign({ label: label(id), segment: id, metric, agg: "avg" }, styleFor(id)));

  const derivedSeries = (ids, inputsFn, transform) => ids.map((id) =>
    Object.assign({ label: label(id), inputs: inputsFn(id), transform }, styleFor(id)));

  /* ---- Panels ----------------------------------------------------------- */

  /* Temperature -- one raw series per climate sensor (this panel renders the
   * shared time axis; the rest inherit the same window). */
  const panelTemp = {
    id: 25, type: "timeseries", title: "Temperatur", height: 340,
    axisLeft: { label: "°C" }, timeAxis: true, legend: true,
    series: rawSeries(CLIMATE, "Temperature"),
  };

  /* Warm water tank temperature + heating power draw (dual axis). */
  const panelWW = {
    id: 2, type: "timeseries", title: "Warmwasser / Strom", height: 240,
    axisLeft: { label: "°C", min: 20, max: 50 },
    axisRight: { label: "W", min: 0, max: 135, show: true },
    timeAxis: true, legend: true,
    series: [
      { label: "Warmwasser", segment: "0xa4c1383c7d3c4cb5", metric: "Temperature",
        agg: "avg", color: "#e02f44", width: 2 },
      { label: "Strom", segment: "0xa4c138edbd20f773", metric: "power",
        agg: "avg", color: "#ff9830", width: 1, axis: "right" },
    ],
  };

  const ENERGY_SENSOR = "tasmota_6D858C";
  const panelStrom = {
    id: 40, type: "timeseries", title: "Stromverbrauch", height: 300,
    axisLeft: { label: "W" }, timeAxis: true, legend: true,
    series: [
      { label: "Stromverbrauch", segment: ENERGY_SENSOR, metric: "Power_curr",
        agg: "avg", color: "#fade2a", width: 1 },
    ],
  };

  /* Relative humidity -- raw Humidity per sensor. */
  const panelRelHum = {
    id: 26, type: "timeseries", title: "Rel. Feuchte", height: 300,
    axisLeft: { label: "%RH", min: 0, max: 100 }, timeAxis: true, legend: true,
    series: rawSeries(CLIMATE, "Humidity"),
  };

  /* Absolute humidity -- derived from the (cached) raw T/H of each sensor. */
  const panelAbsHum = {
    id: 27, type: "timeseries", title: "Abs. Feuchte", height: 300,
    axisLeft: { label: "g/m³" }, timeAxis: true, legend: true,
    series: derivedSeries(CLIMATE, (id) => [T(id), H(id)], (r) => absHumidity(r.T, r.H)),
  };

  /* Enthalpy -- derived from the same cached raw T/H. */
  const panelEnthalpy = {
    id: 31, type: "timeseries", title: "Enthalpie", height: 300,
    axisLeft: { label: "kJ/kg" }, timeAxis: true, legend: true,
    series: derivedSeries(CLIMATE, (id) => [T(id), H(id)], (r) => enthalpy(r.T, r.H)),
  };

  /* Dew point -- derived from the same cached raw T/H. */
  const panelDewpoint = {
    id: 33, type: "timeseries", title: "Taupunkt", height: 300,
    axisLeft: { label: "°C" }, timeAxis: true, legend: true,
    series: derivedSeries(CLIMATE, (id) => [T(id), H(id)], (r) => dewpoint(r.T, r.H)),
  };

  /* Ventilation -- momentary binary flag per indoor sensor, from the LATEST
   * sample of the (derived) ventilation-benefit series. Reuses the same cached
   * raw T/H plus the shared outdoor reference series. */
  const panelLuften = {
    id: 34, type: "flag", title: "Lüften", height: 150,
    series: derivedSeries(
      INDOOR,
      (id) => [T(id), H(id),
        { key: "Tr", segment: REF, metric: "Temperature", agg: "avg" },
        { key: "Hr", segment: REF, metric: "Humidity", agg: "avg" }],
      (r) => ventilate(r.T, r.H, r.Tr, r.Hr)),
    flag: {
      state: (v) => v >= 0.999
        ? { text: "lüften", color: "#56a64b", fg: "#ffffff" }
        : { text: "zulassen", color: "#eef0f2", fg: "#57606a" },
    },
  };

  /* Window contact -- binary flag (raw contact metric). 1 = closed, 0 = open. */
  const panelFenster = {
    id: 22, type: "flag", title: "Fenster", height: 120,
    series: [{ label: "Badfenster", segment: "0xa4c138ef06c68248", metric: "contact", agg: "avg" }],
    flag: {
      state: (v) => v >= 0.5
        ? { text: "Zu", color: "#56a64b", fg: "#ffffff" }
        : { text: "Offen", color: "#e02f44", fg: "#ffffff" },
    },
  };

  /* Link quality -- raw LQI per sensor (all sensors). */
  const panelLink = {
    id: 17, type: "timeseries", title: "Linkquality", height: 260,
    axisLeft: { label: "LQI", min: 0, max: 160 }, timeAxis: true, legend: true,
    series: rawSeries(Object.keys(SENSORS), "Linkquality"),
  };

  /* ---- Übersicht: per-room overview tiles + Wasser/Strom -----------------
   * Uses the generic "tiles" panel type (dashboard.js): the renderer only
   * owns the card shell + the "latest value of a series" read-out; anything
   * dashboard-specific is injected via a tile's `addon(el, ctx)` hook.
   * Room tiles: name + current temperature (indoor sensors only, same
   * order as the Temperature panel, outdoor "Garten" excluded -- it's not a
   * room). */
  const tileRooms = INDOOR.map((id) => ({
    label: label(id),
    series: { segment: id, metric: "Temperature", agg: "avg" },
    unit: "°C",
  }));

  /* Strom tile (position 2): current household power draw, same source as
   * the "Strom" row's line chart above. */
  const tileStrom = {
    label: "Strom",
    series: { segment: ENERGY_SENSOR, metric: "Power_curr", agg: "avg" },
    unit: "W",
  };

  /* ---- Wasser tile (position 1): current hot-water tank temperature, plus
   * a live ON/OFF toggle for the heating's operating state -----------------
   * The toggle is the "addon": dashboard-specific content mounted into an
   * otherwise generic tile, driven by zigbee2mqtt's raw MQTT-over-WebSocket
   * bridge (ws://dietpi:9090/api) instead of the historical query engine
   * every other panel/tile uses, since it needs to be live and writable.
   *
   * Wire protocol, as observed against the live bridge (no formal docs were
   * available):
   *   - right after connecting, the bridge replays the full retained state
   *     of every zigbee2mqtt entity as individual {topic, payload} messages,
   *     `topic` being the *bare* entity id (no "zigbee2mqtt/" prefix) -- so
   *     no explicit "get" request is needed, the current state arrives
   *     unprompted, and every later state change is pushed the same way;
   *   - to control a device, send {topic: "<id>/set", payload: {...}}, with
   *     `payload` as a genuine JSON *object* (not a JSON-encoded string),
   *     and again without the "zigbee2mqtt/" prefix on `topic`. */
  const HEATER_WS_URL = "ws://dietpi:9090/api";
  // NOTE: id as specified for this toggle; currently resolves to "Aura
  // Computer" in zigbee2mqtt, not the actual boiler switch -- to be swapped
  // for the real device id once available.
  const HEATER_ID = "0xa4c1380d5aeeffff";

  function heaterToggleAddon(el) {
    const wrap = document.createElement("label");
    wrap.className = "toggle-switch";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.disabled = true;                 // enabled once the real state is known
    const slider = document.createElement("span");
    slider.className = "toggle-slider";
    wrap.appendChild(input);
    wrap.appendChild(slider);
    const text = document.createElement("span");
    text.className = "toggle-label";
    text.textContent = "…";
    el.appendChild(wrap);
    el.appendChild(text);

    let ws = null, known = null;
    const setText = (on) => { text.textContent = on == null ? "—" : (on ? "An" : "Aus"); };

    function connect() {
      try { ws = new WebSocket(HEATER_WS_URL); } catch (e) { setText(null); return; }
      ws.addEventListener("open", () => { input.disabled = false; });
      ws.addEventListener("message", (ev) => {
        let msg;
        try { msg = JSON.parse(ev.data); } catch (e) { return; }
        if (msg.topic !== HEATER_ID || !msg.payload || typeof msg.payload.state !== "string") return;
        known = msg.payload.state.toUpperCase() === "ON";
        input.checked = known;
        setText(known);
      });
      ws.addEventListener("close", () => {
        input.disabled = true;
        setText(null);
        setTimeout(connect, 5000);          // auto-reconnect
      });
      ws.addEventListener("error", () => { try { ws.close(); } catch (_) { /* ignore */ } });
    }
    connect();

    input.addEventListener("change", () => {
      const want = input.checked;
      if (!ws || ws.readyState !== WebSocket.OPEN) { input.checked = !!known; return; }
      ws.send(JSON.stringify({ topic: HEATER_ID + "/set", payload: { state: want ? "ON" : "OFF" } }));
      setText(want);                         // optimistic; reconciled by the next state push
    });
  }

  const tileWasser = {
    label: "Wasser",
    series: { segment: "0xa4c1383c7d3c4cb5", metric: "Temperature", agg: "avg" },
    unit: "°C",
    addon: heaterToggleAddon,
  };

  const panelOverview = {
    id: 50, type: "tiles",
    tiles: [tileWasser, tileStrom, ...tileRooms],
  };

  /* ---- season: the "Lüften" row is only expanded in summer (May–Sep) ----- */
  const month = new Date().getMonth() + 1;
  const isSummer = month >= 5 && month <= 9;

  /* ---- Dashboard layout ------------------------------------------------- */
  window.DASHBOARD = {
    title: "Heizung",
    /* Global header links (formerly the Grafana "Links" text panel). */
    links: [
      { label: "Zigbee", url: "http://dietpi:9090" },
      { label: "IOBroker", url: "http://dietpi:8081" },
      { label: "Fritz!Box", url: "http://fritz.box" },
    ],
    rows: [
      { title: "Übersicht", type: "grid", collapse: false, panels: [panelOverview] },
      { title: "Allgemein", type: "grid", collapse: true, panels: [panelTemp, panelWW] },
      { title: "Strom",     type: "grid", collapse: true, panels: [panelStrom] },
      { title: "Feuchte",   type: "grid", collapse: true,  panels: [panelRelHum, panelAbsHum, panelFenster] },
      { title: "Lüften",    type: "grid", collapse: !isSummer, panels: [panelLuften] },
      { title: "Enthalpie / Taupunkt", type: "grid", collapse: true, panels: [panelEnthalpy, panelDewpoint] },
      { title: "Sensoren",  type: "grid", collapse: true, panels: [panelLink] },
    ],
  };
})();
