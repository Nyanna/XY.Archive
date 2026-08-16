/* "Flag" panels (momentary binary/status indicators, rendered as plain DOM
 * badges, not an ECharts canvas) and the small per-tile accent-colour +
 * fetch-context helpers used by "tiles" panels' dashboard-specific addons. */
"use strict";
import { seriesData, latestValue } from "./data.js";
import { fmtTip } from "./charts.common.js";
import { getRange, maxPointsOverride } from "./controls.js";

/* Small helper context handed to "tiles" panel addons (see panel.js): lets
 * a dashboard-specific addon -- e.g. a live WebSocket toggle -- reuse the
 * generic query engine for an occasional "latest value" read without the
 * renderer having to know anything about the addon itself. */
export const TILE_CTX = {
  fetchLatest: async (sc) => latestValue(await seriesData(sc, getRange(), maxPointsOverride(3000))),
  fmtTip,
};

/* Deterministic, maintenance-free per-tile colour: derived from a cheap
 * hash of the tile's label, so e.g. "Büro" always gets the same tint on
 * every load without any hand-maintained label -> colour table. Purely a
 * recognition aid (build muscle memory for "my tile lives over there, the
 * reddish one") -- not meant to encode any value/state.
 *   - hue: one hash component, ROUNDED onto a fixed grid of steps (a
 *     discrete "spectrum") so any two tiles land at least one step apart
 *     -- no near-identical, hard-to-tell-apart hues;
 *   - saturation/lightness: two further, independent hash components,
 *     varied continuously (fairly strong/saturated) so tiles that happen
 *     to share a hue step still look distinguishable. */
function labelHash(label) {
  let h = 5381;
  const s = String(label || "");
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0; // djb2
  return h >>> 0;
}
const HUE_STEPS = 18;                    // 360°/18 = 20° apart -> clearly distinct hues
export function tileAccent(label) {
  const h = labelHash(label);
  const hue = (h % HUE_STEPS) * (360 / HUE_STEPS);          // rounded onto the hue grid
  const sat = 58 + (Math.floor(h / HUE_STEPS) % 25);        // 58-82%
  const lit = 68 + (Math.floor(h / (HUE_STEPS * 25)) % 14); // 68-81%
  return {
    background: "linear-gradient(135deg, hsl(" + hue + " " + sat + "% " + lit + "%), hsl(" +
      hue + " " + Math.max(sat - 10, 35) + "% " + Math.min(lit + 13, 97) + "%))",
    borderColor: "hsl(" + hue + " " + Math.min(sat + 12, 92) + "% " + Math.max(lit - 32, 38) + "%)",
  };
}

export function renderFlagPanel(el, cfg, results) {
  const stateFn = (cfg.flag && cfg.flag.state) ||
    ((v) => ({ text: fmtTip(v), color: "#e6e6e6" }));
  const wrap = document.createElement("div");
  wrap.className = "flags";
  results.forEach(({ sc, data }) => {
    const v = latestValue(data);
    const st = v == null ? { text: "—", color: "#eef0f2", fg: "#8b949e" } : stateFn(v);
    const cell = document.createElement("div");
    cell.className = "flag";
    cell.style.background = st.color;
    if (st.fg) cell.style.color = st.fg;
    const name = document.createElement("div");
    name.className = "flag-name";
    name.textContent = sc.label;
    const val = document.createElement("div");
    val.className = "flag-value";
    val.textContent = st.text;
    cell.appendChild(name);
    cell.appendChild(val);
    wrap.appendChild(cell);
  });
  el.innerHTML = "";
  el.appendChild(wrap);
}
