/* Oct 28 2026 (founder): Saturn intro on the home hero (space theme). A real Cassini Saturn (PIA11141, NASA/JPL-Caltech/
   Space Science Institute) rises from below behind the title, then the view zooms into the right ring arm and crossfades to a
   real Cassini natural-color ring mosaic (PIA06175, same credit) that keeps zooming slowly; after a hold it fades back to the
   Enceladus scene. Transform/opacity only (no layout shift). prefers-reduced-motion = no intro (static scene).
   Plays once per browser session; ?hero-intro=1 forces it. Markup + CSS: scripts/build-hero-themes.py (HEROTHEME block). */
(function () {
  'use strict';
  var hero = document.querySelector('.hero[data-hero]');
  if (!hero || hero.getAttribute('data-hero') !== 'space') return;
  var box = hero.querySelector('.hs-intro');
  if (!box) return;
  var force = /[?&]hero-intro=1/.test(location.search);
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  if (mq.matches && !force) return;
  try { if (!force && sessionStorage.getItem('spSatIntro')) return; } catch (e) {}
  var imgs = [].slice.call(box.querySelectorAll('img[data-srcset]')), left = imgs.length, done = false;
  function go() {
    if (done) return; done = true;
    try { sessionStorage.setItem('spSatIntro', '1'); } catch (e) {}
    hero.classList.add('hs-introing'); box.classList.add('run');
    var end = function () { box.classList.remove('run'); hero.classList.remove('hs-introing'); box.hidden = true; };
    box.addEventListener('animationend', function (ev) { if (ev.target === box) end(); });
    setTimeout(end, 26000); // safety net if animationend never fires
  }
  function one() { if (--left <= 0) go(); }
  imgs.forEach(function (im) {
    im.onload = function () { (im.decode ? im.decode() : Promise.resolve()).then(one, one); };
    im.onerror = function () { done = true; box.hidden = true; };
    im.sizes = im.getAttribute('data-sizes') || '100vw';
    im.srcset = im.getAttribute('data-srcset');
  });
  if (mq.addEventListener) mq.addEventListener('change', function () { if (mq.matches) { box.classList.remove('run'); hero.classList.remove('hs-introing'); box.hidden = true; } });
})();
