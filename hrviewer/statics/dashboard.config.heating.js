/* Heating/climate config: sensor mapping, shared cache, derived metrics,
 * flag panels, and auto-refresh. */
(function () {
  "use strict";

  /* Central sensor mapping (Zigbee id -> friendly label). */
  const SENSORS = {
    "0x00158d00087be14f": "Garten",          // outdoor reference
    "0x00124b00292abb11": "Wohnzimmer",
    "0x00124b00292fc600": "Schlafzimmer",
    "0x44e2f8fffe33bcad": "Bad",
    "0x00124b002a6d6fd8": "Keller",
    "0x00124b0022d5a1f7": "Waschraum",
    "0x00124b00252be376": "Hobby",
    "0x00124b00290fb077": "Büro",
    "0xf0d1b8be2409fc48": "Gasmelder",
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

  const REF = "0x00158d00087be14f";  // outdoor reference for ventilation

  /* Room-climate sensors (outdoor Garten included, drawn dotted). */
  const CLIMATE = [
    REF,
    "0x00124b00292abb11", "0x00124b00292fc600", "0x44e2f8fffe33bcad",
    "0x00124b002a6d6fd8", "0x00124b0022d5a1f7", "0x00124b00252be376",
    "0x00124b00290fb077", "0x00124b002a50c50a",
    "0x00124b00292b470a", "0x00124b002a6d3c44", "0x44e2f8fffe27e73c",
    "0x94deb8fffe41e3c0", "0x00124b00252be456",
  ];
  /* Psychrometric functions (Magnus formula): T in °C, H in %RH. */
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

  /* Series builders: outdoor Garten gets dotted, thicker style. */
  const T = (id) => ({ key: "T", segment: id, metric: "Temperature", agg: "avg" });
  const H = (id) => ({ key: "H", segment: id, metric: "Humidity", agg: "avg" });
  const styleFor = (id) => (id === REF ? { dash: "dotted", width: 3 } : { width: 1 });

  const rawSeries = (ids, metric) => ids.map((id) =>
    Object.assign({ label: label(id), segment: id, metric, agg: "avg" }, styleFor(id)));

  const derivedSeries = (ids, inputsFn, transform) => ids.map((id) =>
    Object.assign({ label: label(id), inputs: inputsFn(id), transform }, styleFor(id)));

  const panelTemp = {
    id: 25, type: "timeseries", title: "Temperatur", height: 340,
    axisLeft: { label: "°C" }, timeAxis: true, legend: true,
    series: rawSeries(CLIMATE, "Temperature"),
  };

  const panelWW = {
    id: 2, type: "timeseries", title: "Warmwasser / Strom", height: 240,
    axisLeft: { label: "°C", min: 20, max: 50 },
    axisRight: { label: "W", min: 0, max: 135, show: true },
    timeAxis: true, legend: true,
    series: [
      { label: "Warmwasser", segment: "0xa4c1383c7d3c4cb5", metric: "Temperature",
        agg: "avg", color: "#e02f44", width: 2 },
      { label: "Strom", segment: "0xa4c138edbd20f773", metric: "Power",
        agg: "avg", color: "#ff9830", width: 1, axis: "right" },
    ],
  };

  const ENERGY_SENSOR = "tasmota_6D858C";
  const panelStrom = {
    id: 40, type: "timeseries", title: "Stromverbrauch", height: 300,
    axisLeft: { label: "W" }, timeAxis: true, legend: true,
    series: [
      { label: "Stromverbrauch", segment: ENERGY_SENSOR, metric: "Power_curr",
        agg: "avg", color: "#fade2a", width: 1, fillOpacity: 25 },
    ],
  };

  const panelRelHum = {
    id: 26, type: "timeseries", title: "Rel. Feuchte", height: 300,
    axisLeft: { label: "%RH", min: 0, max: 100 }, timeAxis: true, legend: true,
    series: rawSeries(CLIMATE, "Humidity"),
  };

  const panelAbsHum = {
    id: 27, type: "timeseries", title: "Abs. Feuchte", height: 300,
    axisLeft: { label: "g/m³" }, timeAxis: true, legend: true,
    series: derivedSeries(CLIMATE, (id) => [T(id), H(id)], (r) => absHumidity(r.T, r.H)),
  };

  const panelEnthalpy = {
    id: 31, type: "timeseries", title: "Enthalpie", height: 300,
    axisLeft: { label: "kJ/kg" }, timeAxis: true, legend: true,
    series: derivedSeries(CLIMATE, (id) => [T(id), H(id)], (r) => enthalpy(r.T, r.H)),
  };

  const panelDewpoint = {
    id: 33, type: "timeseries", title: "Taupunkt", height: 300,
    axisLeft: { label: "°C" }, timeAxis: true, legend: true,
    series: derivedSeries(CLIMATE, (id) => [T(id), H(id)], (r) => dewpoint(r.T, r.H)),
  };

  const panelFenster = {
    id: 22, type: "flag", title: "Fenster", height: 120,
    series: [{ label: "Badfenster", segment: "0xa4c138ef06c68248", metric: "contact", agg: "avg" }],
    flag: {
      state: (v) => v >= 0.5
        ? { text: "Zu", color: "#56a64b", fg: "#ffffff" }
        : { text: "Offen", color: "#e02f44", fg: "#ffffff" },
    },
  };

  const panelLink = {
    id: 17, type: "timeseries", title: "Linkquality", height: 260,
    axisLeft: { label: "LQI", min: 0, max: 160 }, timeAxis: true, legend: true,
    series: rawSeries(Object.keys(SENSORS), "Linkquality"),
  };

  const ventMonth = new Date().getMonth() + 1;
  const showVentilate = ventMonth >= 5 && ventMonth <= 8;

  function ventilateAddon(id) {
    return function (el, ctx) {
      if (!showVentilate) return;
      const badge = document.createElement("span");
      badge.className = "tile-pill";
      badge.textContent = "…";
      el.appendChild(badge);

      const sc = {
        inputs: [T(id), H(id),
          { key: "Tr", segment: REF, metric: "Temperature", agg: "avg" },
          { key: "Hr", segment: REF, metric: "Humidity", agg: "avg" }],
        transform: (r) => ventilate(r.T, r.H, r.Tr, r.Hr),
      };
      const paint = (v) => {
        if (v == null) {
          badge.textContent = "—"; badge.style.background = "#eef0f2"; badge.style.color = "#8b949e";
          return;
        }
        const on = v >= 0.999;
        badge.textContent = on ? "lüften" : "zulassen";
        badge.style.background = on ? "#56a64b" : "#eef0f2";
        badge.style.color = on ? "#ffffff" : "#57606a";
      };
      const refresh = () => ctx.fetchLatest(sc).then(paint).catch(() => paint(null));
      refresh();
      setInterval(refresh, 15000);
    };
  }

  /* Overview tiles: per-room cards + utilities (Wasser/Strom). */
  const tileRooms = CLIMATE.map((id) => {
    const tile = {
      label: label(id),
      series: { segment: id, metric: "Temperature", agg: "avg" },
      unit: "°C",
    };
    if (id !== REF) tile.addon = ventilateAddon(id);   // not for the outdoor reference itself
    return tile;
  });

  /* Strom tile (position 2): current household power draw, same source as
   * the "Strom" row's line chart above. */
  const tileStrom = {
    label: "Strom",
    series: { segment: ENERGY_SENSOR, metric: "Power_curr", agg: "avg" },
    unit: "W",
  };

  /* Zigbee2mqtt MQTT-over-WebSocket bridge: generic ON/OFF toggle, reused for
   * the heater as well as any lamp/socket switch below (device id differs). */
  const HEATER_WS_URL = "ws://dietpi:9090/api";
  const HEATER_ID = "0xa4c138edbd20f773";

  function toggleAddon(deviceId) {
    return function (el) {
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
          if (msg.topic !== deviceId || !msg.payload || typeof msg.payload.state !== "string") return;
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
        ws.send(JSON.stringify({ topic: deviceId + "/set", payload: { state: want ? "ON" : "OFF" } }));
        setText(want);                         // optimistic; reconciled by the next state push
      });
    };
  }

  const tileWasser = {
    label: "Wasser",
    series: { segment: "0xa4c1383c7d3c4cb5", metric: "Temperature", agg: "avg" },
    unit: "°C",
    addon: toggleAddon(HEATER_ID),
  };

  const panelOverview = {
    id: 50, type: "tiles",
    tiles: [tileWasser, tileStrom, ...tileRooms],
  };

  /* ---- Lampen & Steckdosen: label -> zigbee2mqtt device id -------------- */
  const LAMPS = {
    "Wohnzimmer Lampe":  "0xa4c138089de1ffff",
    "Wasserkocher":      "0xa4c138083f13ffff",
    "Schlafzimmer":      "0xa4c1380d4358ffff",
    "Aura Computer":     "0xa4c1380d5aeeffff",
    "Kimi Büro":         "0xa4c138425776c645",
    "Hobbydose":         "0xa4c138db1ba923b1",
    "Wendy Schreibtisch":"0x00124b0026b82cce",
    "Espresso":          "0xa4c1380d85a6455f",
    "Hifi":              "0xa4c1387253897923",
  };
  const panelLampen = {
    id: 51, type: "tiles",
    tiles: Object.entries(LAMPS).map(([lbl, id]) => ({ label: lbl, addon: toggleAddon(id) })),
  };

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
      { title: "Lampen & Steckdosen", type: "grid", collapse: true, panels: [panelLampen] },
      { title: "Allgemein", type: "grid", collapse: true, panels: [panelTemp, panelWW] },
      { title: "Strom",     type: "grid", collapse: true, panels: [panelStrom] },
      { title: "Feuchte",   type: "grid", collapse: true,  panels: [panelRelHum, panelAbsHum, panelFenster] },
      { title: "Enthalpie / Taupunkt", type: "grid", collapse: true, panels: [panelEnthalpy, panelDewpoint] },
      { title: "Sensoren",  type: "grid", collapse: true, panels: [panelLink] },
    ],
  };
})();
