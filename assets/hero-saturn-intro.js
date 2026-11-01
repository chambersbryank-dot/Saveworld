/* Oct 28 2026 (founder): Saturn intro on the home hero (space theme). A real Cassini Saturn (PIA11141, NASA/JPL-Caltech/
   Space Science Institute) rises from below behind the title, then the view zooms into the right ring arm and crossfades to a
   real Cassini natural-color ring mosaic (PIA06175, same credit) that keeps zooming slowly; after a hold it fades back to the
   Enceladus scene. Both images are fetched and decoded before the clock starts so nothing pops in; GPU-only translate3d/scale + opacity (no layout shift). prefers-reduced-motion = no intro (static scene).
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
    var ended = false, fire = function (n) { try { window.dispatchEvent(new Event(n)); } catch (e) {} };
    // Oct 29 2026: the live scene (hero-themes.js) stays frozen during the intro; it builds itself at 13.2 s, when the ring
    // close-up fully covers the hero, and resumes on sp-intro-end.
    var idleT = setTimeout(function () { fire('sp-intro-idle'); }, 13200);
    var end = function () { if (ended) return; ended = true; clearTimeout(idleT); hero.classList.add('hs-titlewait'); setTimeout(function () { hero.classList.remove('hs-titlewait'); }, 9000); box.classList.remove('run'); hero.classList.remove('hs-introing'); box.hidden = true; fire('sp-intro-end'); };
    box.addEventListener('animationend', function (ev) { if (ev.target === box) end(); });
    setTimeout(end, 26000); // safety net if animationend never fires
  }
  function one() { if (--left <= 0) go(); }
  imgs.forEach(function (im) {
    im.onload = function () { (im.decode ? im.decode() : Promise.resolve()).then(one, one); };
    im.onerror = function () { if (done) return; done = true; box.hidden = true; try { window.dispatchEvent(new Event('sp-intro-end')); } catch (e) {} };
    im.sizes = im.getAttribute('data-sizes') || '100vw';
    im.srcset = im.getAttribute('data-srcset');
  });
  if (mq.addEventListener) mq.addEventListener('change', function () { if (mq.matches) { box.classList.remove('run'); hero.classList.remove('hs-introing'); box.hidden = true; try { window.dispatchEvent(new Event('sp-intro-end')); } catch (e) {} } });
})();
