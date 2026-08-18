/* Generic ECharts dashboard renderer, driven entirely by a `window.DASHBOARD`
 * config (see dashboard.config.js). Not tied to any specific metrics or
 * domain -- a new dashboard only needs its own config file, selected via
 * dashboard.html's `?config=` URL parameter.
 *
 * Features: synced zoom/hover cursor across panels (by axis value, not data
 * index, plus late-join replay), a time selector with quick ranges + shift
 * buttons, lazy (visibility-based) panel loading, thresholds, dual Y-axes,
 * a toggleable legend, collapsible rows, a tab layout and labelled, static
 * time annotations shown across all synced panels.
 *
 * Implementation is grouped under ./dashboard/ (time utils, the query/data
 * layer, ECharts option builders, the Panel class, DOM layout, and the
 * global time-window/zoom-sync controls); this file only wires it together.
 */
"use strict";
import { initControls } from "./dashboard/controls.js";
import { buildRow, renderHeaderLinks } from "./dashboard/layout.js";

const boardEl = document.getElementById("board");

function init() {
  document.title = DASHBOARD.title;
  // The logo image lives inside #pageTitle (see dashboard.html); prefer the
  // dedicated text span so it's updated without clobbering the logo. Falls
  // back to the heading itself for older/plain markup.
  const titleTextEl = document.getElementById("pageTitleText") || document.getElementById("pageTitle");
  if (titleTextEl) titleTextEl.textContent = DASHBOARD.title;
  renderHeaderLinks();
  DASHBOARD.rows.forEach((r) => boardEl.appendChild(buildRow(r)));
  initControls();   // wires range/zoom/auto-refresh controls, sets initial window
}

init();
