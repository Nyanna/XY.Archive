// SmartHome editor: inject the workspace, load the single native script from
// the backend, and save it back (native XML + generated Python) on demand.
(function () {
  "use strict";

  var ENDPOINT = "/api/smarthome/script";
  var STATUS_ENDPOINT = "/api/smarthome/status";
  var ws = null;

  function refreshStatus() {
    fetch(STATUS_ENDPOINT)
      .then(function (r) { return r.json(); })
      .then(function (m) {
        document.getElementById("mTriggers").textContent = m.triggers_registered;
        document.getElementById("mSchedules").textContent = m.schedules_registered;
        document.getElementById("mTimers").textContent = m.active_timers;
        document.getElementById("mqttDot").className = "dot" + (m.mqtt_connected ? " on" : "");
      })
      .catch(function () { /* transient network hiccup, next poll retries */ });
  }

  function xmlTextToDom(text) {
    if (Blockly.utils && Blockly.utils.xml && Blockly.utils.xml.textToDom) {
      return Blockly.utils.xml.textToDom(text);
    }
    return Blockly.Xml.textToDom(text);
  }

  function status(msg, isError) {
    var el = document.getElementById("status");
    el.textContent = msg || "";
    el.className = "status" + (isError ? " error" : "");
  }

  function load() {
    fetch(ENDPOINT)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        ws.clear();
        var xml = (data.xml || "").trim();
        if (xml) {
          Blockly.Xml.domToWorkspace(xmlTextToDom(xml), ws);
        }
        if (data.error) {
          status("Loaded (last run had a script error - see server log)", true);
        } else {
          status("Loaded");
        }
      })
      .catch(function (e) { status("Load failed: " + e, true); });
  }

  function save() {
    var dom = Blockly.Xml.workspaceToDom(ws);
    var xml = Blockly.Xml.domToText(dom);
    var python;
    try {
      python = Blockly.Python.workspaceToCode(ws);
    } catch (e) {
      status("Python generation failed: " + e, true);
      return;
    }
    status("Saving...");
    fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ xml: xml, python: python }),
    })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.ok) status("Saved & reloaded");
        else status("Saved, but script error: " + (res.error || "unknown"), true);
      })
      .catch(function (e) { status("Save failed: " + e, true); });
  }

  window.addEventListener("load", function () {
    ws = Blockly.inject("blocklyDiv", {
      toolbox: document.getElementById("toolbox"),
      theme: window.SMARTHOME_THEME,
      trashcan: true,
      zoom: { controls: true, wheel: true, startScale: 0.9 },
      grid: { spacing: 20, length: 3, colour: "#d0d7de", snap: true },
    });
    document.getElementById("save").addEventListener("click", save);
    document.getElementById("reload").addEventListener("click", load);
    load();
    refreshStatus();
    setInterval(refreshStatus, 5000);
  });
})();
