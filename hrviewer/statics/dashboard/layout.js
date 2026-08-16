/* DOM construction from the dashboard config: rows, tabs, panel grids, and
 * the header links list. Also owns the lazy-loading IntersectionObserver
 * that starts a panel loading once it scrolls into view. */
"use strict";
import { Panel } from "./panel.js";
import { panels, registerPanel } from "./controls.js";

/* ---- lazy loading via IntersectionObserver -------------------------- */
const observer = new IntersectionObserver((entries) => {
  entries.forEach((ent) => {
    const p = ent.target.__panel;
    if (!p) return;
    p.visible = ent.isIntersecting && ent.intersectionRatio > 0;
    if (p.visible && p.dirty) p.load();
  });
}, { root: null, threshold: 0.01 });

function buildPanel(cfg) {
  const p = new Panel(cfg);
  registerPanel(p);
  p.host.__panel = p;
  observer.observe(p.host);
  return p;
}

function buildGrid(container, panelCfgs) {
  const grid = document.createElement("div");
  grid.className = "grid";
  panelCfgs.forEach((cfg) => grid.appendChild(buildPanel(cfg).host));
  container.appendChild(grid);
}

/* Tab bar in header; bodies in container. */
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

export function buildRow(rowCfg) {
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

/* Render external links in top bar (config-driven). */
export function renderHeaderLinks() {
  const links = DASHBOARD.links || [];
  const topbar = document.querySelector(".topbar");
  if (!links.length || !topbar) return;
  const nav = document.createElement("nav");
  nav.className = "links";
  links.forEach((l) => {
    const a = document.createElement("a");
    a.href = l.url;
    a.textContent = l.label;
    a.target = l.target || "_blank";
    a.rel = "noopener noreferrer";
    nav.appendChild(a);
  });
  const titleEl = document.getElementById("pageTitle");
  if (titleEl && titleEl.parentNode === topbar) topbar.insertBefore(nav, titleEl.nextSibling);
  else topbar.appendChild(nav);
}
