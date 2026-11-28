/* Homepage only. The hero loop is Earth (about 0–3.2s), beach, then forest
   (docs/notes-archive-2026-10-12.md: Earth 0.2–3.4s, beach 4.0–6.6s, forest 7.0–9.8s,
   0.6s crossfades, 7.4s out). Beach and forest play. Earth is held as a still frame.
   The moon / Earthrise canvas is kept still by hero-themes.js on body.toc-home. */
(function () {
  if (!document.body || !document.body.classList.contains('toc-home')) return;
  var v = document.querySelector('video.hero-video');
  if (!v || v.classList.contains('hero-video-off') || v.getAttribute('data-home-cut') !== 'beach') return;
  var EARTH = 1.15, BEACH = 3.2, FOREST_END = 7.35, HOLD = 4500;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var holdTimer = 0;
  v.loop = false;
  v.removeAttribute('loop');
  function at(t) {
    try { if (Math.abs(v.currentTime - t) > 0.08) v.currentTime = t; } catch (e) {}
  }
  function showEarth() {
    v.pause();
    at(EARTH);
    if (reduce) return;
    clearTimeout(holdTimer);
    holdTimer = setTimeout(playCoast, HOLD);
  }
  function playCoast() {
    if (reduce || document.hidden) return;
    at(BEACH);
    var p = v.play && v.play();
    if (p && p.catch) p.catch(function () {});
  }
  v.addEventListener('timeupdate', function () {
    if (v.paused) return;
    var end = (v.duration && isFinite(v.duration)) ? Math.min(FOREST_END, v.duration - 0.05) : FOREST_END;
    if (v.currentTime >= end || (v.currentTime > 0.05 && v.currentTime < BEACH - 0.2)) showEarth();
  });
  v.addEventListener('ended', showEarth);
  function boot() { showEarth(); }
  if (v.readyState >= 1) boot();
  else v.addEventListener('loadedmetadata', boot, { once: true });
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden && !reduce && v.paused && v.currentTime >= BEACH - 0.05) playCoast();
  });
})();
