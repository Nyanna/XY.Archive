/* Devices dashboard config: endpoint, section layout and tile content. */
(function () {
  "use strict";

  const dash = (v) => (v == null || v === "" ? null : v);
  const fmtTime = (iso) => {
    if (!iso) return null;
    const d = new Date(iso);
    return isNaN(d) ? null : d.toLocaleString("de-DE", {
      day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit",
    });
  };
  const fmtDuration = (s) => {
    if (s == null) return null;
    if (s < 60) return s + " s";
    if (s < 3600) return Math.round(s / 60) + " min";
    if (s < 86400) return (s / 3600).toFixed(1).replace(".", ",") + " h";
    return (s / 86400).toFixed(1).replace(".", ",") + " d";
  };

  const fmtAgo = (iso) => {
    if (!iso) return null;
    const s = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 1000));
    if (isNaN(s)) return null;
    if (s < 60) return "gerade eben";
    if (s < 3600) return "seit " + Math.round(s / 60) + " Min";
    if (s < 86400) return "seit " + Math.round(s / 3600) + " Std";
    return "seit " + Math.round(s / 86400) + " Tg";
  };

  window.DEVICES = {
    title: "Geräte",
    endpoint: "api/smarthome/devices",
    refreshMs: 15000,
    links: [
      { label: "SmartHome", url: "smarthome.html" },
      { label: "Heizung", url: "dashboard.html?config=heating" },
      { label: "Fritz!Box", url: "http://fritz.box" },
    ],

    /* Section order: access points first (as returned by the API), LAN last. */
    lan: { key: "lan", title: "LAN" },
    collapse: false,

    apTitle: (ap) => [ap.name || ap.ip, ap.room].filter(Boolean).join(" · "),
    apSubtitle: (ap) => [ap.floor, ap.ip, ap.mac].filter(Boolean).join(" · "),

    /* Rows per tile: [label, (device) => text|null]; null rows are hidden.
     * `summary` is always visible, `details` only once the tile is expanded. */
    summary: [
      ["Entfernung", (d) => {
        const l = d.location;
        if (!l || l.distance_m == null) return null;
        return (l.distance_is_upper_bound ? "≤ " : "≈ ") + l.distance_m.toFixed(1).replace(".", ",") + " m";
      }],
      ["Inaktiv", (d) => fmtDuration(d.idle_s)],
      ["Zuletzt gesehen", (d) => fmtAgo(d.last_seen)],
    ],
    details: [
      ["IP", (d) => dash(d.ip)],
      ["MAC", (d) => (d.display_name !== d.mac ? d.mac : null)],
      ["Hostname", (d) => (d.hostname && d.hostname !== d.display_name ? d.hostname : null)],
      ["Band", (d) => dash(d.location && d.location.band)],
      ["WLAN-Standard", (d) => dash(d.location && d.location.wifi_standard)],
      ["Signal", (d) => {
        const l = d.location;
        if (!l || (l.signal_pct == null && l.rssi == null)) return null;
        return [l.signal_pct != null ? l.signal_pct + " %" : null,
                l.rssi != null ? l.rssi + " dBm" : null].filter(Boolean).join(" / ");
      }],
      ["Link-Rate", (d) => d.location && d.location.link_rate_mbps != null
        ? d.location.link_rate_mbps + " Mbit/s" : null],
      ["Zuletzt gesehen am", (d) => fmtTime(d.last_seen)],
      ["Getrennt seit", (d) => (d.connected === false ? fmtTime(d.disconnected_at) : null)],
      ["Erstmals gesehen", (d) => fmtTime(d.first_seen)],
      ["Roaming", (d) => (d.movement && d.movement.roam_count ? d.movement.roam_count + "×" : null)],
      ["Letzter Wechsel", (d) => fmtTime(d.movement && d.movement.last_moved)],
    ],
  };
})();
