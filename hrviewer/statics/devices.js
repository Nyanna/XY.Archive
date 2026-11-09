/* Renders the devices endpoint as one section per access point plus LAN,
 * one tile per device. Driven by window.DEVICES (devices.config.js). */
"use strict";
(function () {
  const CFG = window.DEVICES;
  const boardEl = document.getElementById("board");
  const statusEl = document.getElementById("status");
  const filterEl = document.getElementById("filter");
  const onlyConnEl = document.getElementById("onlyConnected");
  const autoEl = document.getElementById("autoRefresh");

  /* Section collapse state survives re-renders. */
  const collapsed = new Map();
  const expanded = new Set();
  let snapshot = null;
  let timer = null;

  /* Deterministic per-name tint, same idea as the heating tiles. */
  function accent(label) {
    let h = 5381;
    for (const c of String(label)) h = ((h << 5) + h + c.charCodeAt(0)) >>> 0;
    const hue = (h % 18) * 20;
    return {
      background: `linear-gradient(135deg, hsl(${hue} 70% 80%), hsl(${hue} 55% 94%))`,
      borderColor: `hsl(${hue} 70% 45%)`,
    };
  }

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function pill(text, cls) {
    return el("span", "tile-pill" + (cls ? " " + cls : ""), text);
  }

  function signalBar(pct) {
    const bar = el("div", "signal");
    const fill = el("span");
    fill.style.width = Math.max(0, Math.min(100, pct)) + "%";
    fill.style.background = pct >= 60 ? "#56a64b" : pct >= 30 ? "#ff9830" : "#e02f44";
    bar.appendChild(fill);
    return bar;
  }

  function buildTile(d) {
    const tile = el("div", "dev-tile" + (d.connected === false ? " offline" : ""));
    const a = accent(d.display_name);
    tile.style.background = a.background;
    tile.style.borderColor = a.borderColor;

    const head = el("div", "dev-head");
    head.appendChild(el("span", "dev-dot" + (d.connected === true ? " on" : d.connected === false ? " off" : "")));
    const name = el("span", "dev-name", d.display_name);
    name.title = d.display_name;
    head.appendChild(name);
    tile.appendChild(head);
    if (d.owner) tile.appendChild(el("div", "dev-owner", d.owner));

    const pills = el("div", "dev-pills");
    if (d.interface) pills.appendChild(pill(d.interface.toUpperCase()));
    if (d.connected === false) pills.appendChild(pill("getrennt", "warn"));
    if (d.movement && d.movement.moving) pills.appendChild(pill("bewegt sich", "moving"));
    else if (d.movement && d.movement.recently_moved) pills.appendChild(pill("kürzlich bewegt"));
    if (pills.children.length) tile.appendChild(pills);

    const pct = d.location && d.location.signal_pct;
    if (pct != null) tile.appendChild(signalBar(pct));

    const addRows = (rows, parent) => {
      const dl = el("dl", "dev-props");
      rows.forEach(([label, fn]) => {
        const v = fn(d);
        if (v == null) return;
        dl.appendChild(el("dt", null, label));
        const dd = el("dd", null, v);
        dd.title = v;
        dl.appendChild(dd);
      });
      if (dl.children.length) parent.appendChild(dl);
    };
    addRows(CFG.summary, tile);
    const details = el("div", "dev-details");
    addRows(CFG.details, details);
    if (details.children.length) {
      tile.appendChild(details);
      tile.classList.add("expandable");
      const apply = () => tile.classList.toggle("expanded", expanded.has(d.mac));
      tile.addEventListener("click", () => {
        if (!expanded.delete(d.mac)) expanded.add(d.mac);
        apply();
      });
      apply();
    }
    return tile;
  }

  function buildSection(key, title, subtitle, devices) {
    const row = el("section", "row");
    const head = el("div", "row-head");
    const caret = el("span", "caret");
    head.appendChild(caret);
    head.appendChild(el("h2", null, title));
    head.appendChild(el("span", "count", `${devices.filter((d) => d.connected).length} / ${devices.length}`));
    if (subtitle) head.appendChild(el("span", "sub", subtitle));

    const content = el("div", "row-content");
    if (devices.length) {
      const wrap = el("div", "dev-tiles");
      devices.forEach((d) => wrap.appendChild(buildTile(d)));
      content.appendChild(wrap);
    } else {
      content.appendChild(el("div", "empty", "Keine Geräte"));
    }

    const apply = () => {
      const c = collapsed.get(key) ?? CFG.collapse;
      content.style.display = c ? "none" : "";
      caret.textContent = c ? "▸" : "▾";
    };
    head.addEventListener("click", () => {
      collapsed.set(key, !(collapsed.get(key) ?? CFG.collapse));
      apply();
    });
    apply();
    row.appendChild(head);
    row.appendChild(content);
    return row;
  }

  function matches(d, q) {
    if (onlyConnEl.checked && d.connected !== true) return false;
    if (!q) return true;
    return [d.display_name, d.mac, d.ip, d.hostname, d.owner]
      .some((v) => v && String(v).toLowerCase().includes(q));
  }

    /* Stable ordering: initial order is "first seen"; a device that changes
   * section gets a fresh sequence number and therefore moves to the end. */
  const placement = new Map();
  const sequence = new Map();
  let seqCounter = 0;

  function sectionKey(d) {
    const apIp = d.location && d.location.ap_ip;
    return apIp && d.interface !== "lan" ? apIp : null;
  }

  function applyDelta(devices) {
    const firstSeen = (d) => {
      const t = d.first_seen ? new Date(d.first_seen).getTime() : NaN;
      return isNaN(t) ? Infinity : t;
    };
    const present = new Set();
    [...devices]
      .sort((a, b) => firstSeen(a) - firstSeen(b) || a.display_name.localeCompare(b.display_name, "de"))
      .forEach((d) => {
        present.add(d.mac);
        const key = sectionKey(d);
        if (!sequence.has(d.mac) || placement.get(d.mac) !== key) {
          placement.set(d.mac, key);
          sequence.set(d.mac, ++seqCounter);
        }
      });
    for (const mac of [...sequence.keys()]) {
      if (!present.has(mac)) {
        sequence.delete(mac);
        placement.delete(mac);
      }
    }
  }

  function render() {
    if (!snapshot) return;
    const q = filterEl.value.trim().toLowerCase();
    const devices = snapshot.devices.filter((d) => matches(d, q));

    const byAp = new Map();
    snapshot.access_points.forEach((ap) => byAp.set(ap.ip, { ap, devices: [] }));
    const lan = [];
    devices.forEach((d) => {
      const apIp = sectionKey(d);
      if (apIp) {
        if (!byAp.has(apIp)) {
          const l = d.location;
          byAp.set(apIp, { ap: { ip: apIp, mac: l.ap_mac, name: l.ap_name, floor: l.floor, room: l.room }, devices: [] });
        }
        byAp.get(apIp).devices.push(d);
      } else {
        lan.push(d);
      }
    });

    const byName = (a, b) => sequence.get(a.mac) - sequence.get(b.mac);
    const frag = document.createDocumentFragment();
    byAp.forEach(({ ap, devices: list }) => {
      frag.appendChild(buildSection("ap:" + ap.ip, CFG.apTitle(ap), CFG.apSubtitle(ap), list.sort(byName)));
    });
    frag.appendChild(buildSection(CFG.lan.key, CFG.lan.title, null, lan.sort(byName)));
    boardEl.replaceChildren(frag);
  }

  async function load() {
    try {
      const r = await fetch(CFG.endpoint, { cache: "no-store" });
      if (!r.ok) throw new Error("HTTP " + r.status);
            snapshot = await r.json();
      applyDelta(snapshot.devices);
      statusEl.classList.remove("error");
      statusEl.textContent = "Stand " + new Date(snapshot.generated_at).toLocaleTimeString("de-DE");
      render();
    } catch (e) {
      statusEl.classList.add("error");
      statusEl.textContent = "Fehler: " + e.message;
    }
  }

  function schedule() {
    clearInterval(timer);
    if (autoEl.checked) timer = setInterval(load, CFG.refreshMs);
  }

  function renderLinks() {
    const topbar = document.querySelector(".topbar");
    const nav = el("nav", "links");
    CFG.links.forEach((l) => {
      const a = el("a", null, l.label);
      a.href = l.url;
      nav.appendChild(a);
    });
    topbar.insertBefore(nav, topbar.querySelector(".controls"));
  }

  document.title = CFG.title;
  document.getElementById("pageTitleText").textContent = CFG.title;
  renderLinks();
  filterEl.addEventListener("input", render);
  onlyConnEl.addEventListener("change", render);
  autoEl.addEventListener("change", schedule);
  document.getElementById("reload").addEventListener("click", load);
  load();
  schedule();
})();
