/* Time / date-range utilities shared across the dashboard renderer.
 * Pure functions only -- no dependency on any other dashboard module. */
"use strict";

export const pad = (n) => String(n).padStart(2, "0");

/* datetime-local <-> epoch ms (local time) */
export function fmtLocal(ms) {
  const d = new Date(ms);
  return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()) +
    "T" + pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds());
}
export const parseLocal = (s) => new Date(s).getTime();

/* Resolve a config time spec ("now" | epoch ms | ISO string) to epoch ms. */
export function resolveTime(v, dflt) {
  if (v == null) return dflt;
  if (v === "now") return Date.now();
  if (typeof v === "number") return v;
  return new Date(v).getTime();
}

/* Fixed per-panel query window -----------------------------------------
 * Panels that aggregate by calendar day need their own, wider window,
 * independent of the (possibly short) global range. Opt in via `cfg.range`:
 *   { days: N }          -> rolling window [now - N days, now]
 *   { from: X, to: Y }   -> absolute bounds; X/Y: "now" | epoch ms | ISO
 * Panels without `cfg.range` fall back to `globalRange` ({start, end} ms). */
export function panelRange(cfg, globalRange) {
  const r = cfg.range;
  if (!r) return globalRange;
  const end = resolveTime(r.to, Date.now());
  const start = r.days != null
    ? end - r.days * 86400000
    : resolveTime(r.from, end - 14 * 86400000);
  return { start, end };
}

/* High-resolution time-axis tick labels: HH:MM (with :SS when relevant),
 * and a bold day marker on midnight boundaries. */
export function axisTimeFormatter(val) {
  const d = new Date(val);
  const H = pad(d.getHours()), M = pad(d.getMinutes()), S = pad(d.getSeconds());
  if (H === "00" && M === "00" && S === "00")
    return "{d|" + pad(d.getDate()) + "." + pad(d.getMonth() + 1) + ".}";
  return S !== "00" ? H + ":" + M + ":" + S : H + ":" + M;
}

export function fmtDateTime(ms) {
  const d = new Date(ms);
  return pad(d.getDate()) + "." + pad(d.getMonth() + 1) + "." + d.getFullYear() + " " +
    pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds());
}
