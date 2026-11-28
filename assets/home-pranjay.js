/* Homepage only. While HOME_THEMES is false the weekly rotation is paused and
   this page shows the beach and forest portion of the hero loop.
   Timeline (docs/notes-archive-2026-10-12.md): Earth 0–3.2s, beach 3.2–5.2s,
   forest 5.2–7.4s. Earth, the moon, and Saturn stay out of the picture.
   Reduced motion holds one beach frame. */
(function () {
  if (!document.body || !document.body.classList.contains('toc-home')) return;
  var v = document.querySelector('video.hero-video');
  if (!v || v.classList.contains('hero-video-off') || v.getAttribute('data-home-cut') !== 'beach') return;
  var BEACH = 3.45, FOREST_END = 7.35;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  v.loop = false;
  v.removeAttribute('loop');
  v.pause();
  function at(t) {
    try { if (Math.abs(v.currentTime - t) > 0.05) v.currentTime = t; } catch (e) {}
  }
  function arm() {
    v.classList.add('is-coast');
  }
  function showBeach() {
    v.pause();
    at(BEACH);
    arm();
    if (reduce) return;
    var p = v.play && v.play();
    if (p && p.catch) p.catch(function () {});
  }
  v.addEventListener('timeupdate', function () {
    if (v.paused) return;
    var end = (v.duration && isFinite(v.duration)) ? Math.min(FOREST_END, v.duration - 0.05) : FOREST_END;
    if (v.currentTime >= end || (v.currentTime > 0.04 && v.currentTime < BEACH - 0.12)) showBeach();
  });
  v.addEventListener('seeked', arm);
  v.addEventListener('ended', showBeach);
  function boot() { showBeach(); }
  if (v.readyState >= 1) boot();
  else v.addEventListener('loadedmetadata', boot, { once: true });
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden && !reduce && v.paused) showBeach();
  });
})();
