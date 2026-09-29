/* Writes --scroll-progress (0..1) onto <html> as the reader scrolls, driving
   the CSS-only night-to-dawn transition of the .sky-dawn layer. */
(function () {
  "use strict";

  var root = document.documentElement;
  var ticking = false;

  function updateScrollProgress() {
    var scrollable = root.scrollHeight - window.innerHeight;
    var progress = scrollable > 0 ? window.scrollY / scrollable : 0;
    progress = Math.min(1, Math.max(0, progress));
    root.style.setProperty("--scroll-progress", progress.toFixed(3));
    ticking = false;
  }

  function requestUpdate() {
    if (!ticking) {
      window.requestAnimationFrame(updateScrollProgress);
      ticking = true;
    }
  }

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate);
  updateScrollProgress();
})();
