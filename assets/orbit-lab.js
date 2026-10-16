/* Orbit Lab (Oct 16 2026): Earth-only, circular start orbit, Hohmann transfer / altitude raise with real vis-viva.
   Physics core is exported for tests (node scripts/test-orbit-lab.js). Strings come from data-t (JSON) on #ol. */
(function (root) {
  'use strict';
  var MU = 398600.4418, RE = 6378.137;  // km^3/s^2, km (same constants as scripts/learn_calc.py)
  function vc(r) { return Math.sqrt(MU / r); }
  function vv(r, a) { return Math.sqrt(MU * (2 / r - 1 / a)); }
  function T(a) { return 2 * Math.PI * Math.sqrt(a * a * a / MU); }
  // mode 'alt': target altitude h2; mode 'dv': first burn dv1 (km/s, + prograde, - retrograde)
  function solve(h1, mode, x) {
    var r1 = RE + h1, v1 = vc(r1), out = { r1: r1, v1: v1 };
    if (mode === 'alt') {
      var r2 = RE + x; out.r2 = r2;
    } else {
      var vp = v1 + x; out.vAfter = vp;
      if (vp >= Math.sqrt(2) * v1) { out.escape = true; out.vesc = Math.sqrt(2) * v1; out.dv1 = x; return out; }
      if (vp <= 0) { out.crash = true; out.dv1 = x; return out; }
      var a = 1 / (2 / r1 - vp * vp / MU); out.r2 = 2 * a - r1;
    }
    var at = (out.r1 + out.r2) / 2; out.at = at; out.e = Math.abs(out.r2 - out.r1) / (out.r1 + out.r2);
    out.dv1 = vv(out.r1, at) - v1; out.v2 = vc(out.r2); out.dv2 = out.v2 - vv(out.r2, at);
    out.dv = Math.abs(out.dv1) + Math.abs(out.dv2); out.tof = T(at) / 2;
    out.reentry = Math.min(out.r1, out.r2) < RE + 100;  // perigee below ~100 km (Karman line): atmosphere, not a stable orbit
    return out;
  }
  root.OrbitLab = { solve: solve, MU: MU, RE: RE };
  if (typeof document === 'undefined') return;
  document.addEventListener('DOMContentLoaded', function () {
    var w = document.getElementById('ol'); if (!w) return;
    var t = JSON.parse(w.dataset.t), lang = document.documentElement.lang || 'en';
    var nf = function (x, d) { return new Intl.NumberFormat(lang, { maximumFractionDigits: d, minimumFractionDigits: d }).format(x); };
    var f = w.querySelector('form'), out = w.querySelector('.ol-out'), tb = w.querySelector('.ol-table tbody'), cv = w.querySelector('canvas'), ctx = cv.getContext('2d');
    var playBtn = w.querySelector('.ol-play'), reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches, res = null, t0 = 0, raf = 0, playing = false;
    function modeSel() { return f.querySelector('input[name=mode]:checked').value; }
    function sync() { var m = modeSel(); w.querySelector('.ol-f-alt').hidden = m !== 'alt'; w.querySelector('.ol-f-dv').hidden = m !== 'dv'; }
    function row(k, v) { return '<tr><th scope="row">' + k + '</th><td>' + v + '</td></tr>'; }
    function compute() {
      var h1 = +f.h1.value, m = modeSel(), x = m === 'alt' ? +f.h2.value : +f.dv.value;
      if (!(h1 >= 160 && h1 <= 100000)) { out.textContent = t.badh1; return; }
      res = solve(h1, m, x); var s = '';
      if (res.escape) { out.textContent = t.escape.replace('{v}', nf(res.vesc - res.v1, 3)); tb.innerHTML = row(t.v1, nf(res.v1, 3) + ' km/s'); draw(0); return; }
      if (res.crash) { out.textContent = t.crash; tb.innerHTML = ''; draw(0); return; }
      s = t.result.replace('{dv1}', nf(res.dv1, 3)).replace('{dv2}', nf(res.dv2, 3)).replace('{dv}', nf(res.dv, 3)).replace('{tof}', nf(res.tof / 3600, 2)).replace('{h2}', nf(res.r2 - RE, 0));
      if (res.reentry) s += ' ' + t.reentry;
      out.textContent = s;
      tb.innerHTML = row(t.v1, nf(res.v1, 3) + ' km/s') + row(t.dv1, nf(res.dv1, 3) + ' km/s') + row(t.at, nf(res.at, 1) + ' km') + row(t.ecc, nf(res.e, 4)) +
        row(t.dv2, nf(res.dv2, 3) + ' km/s') + row(t.dv, nf(res.dv, 3) + ' km/s') + row(t.tof, nf(res.tof / 3600, 2) + ' h') + row(t.v2, nf(res.v2, 3) + ' km/s');
      t0 = performance.now(); if (reduce) { draw(0.5); } else { play(true); }
    }
    function draw(p) {  // p: 0..1 fraction of the transfer (half ellipse)
      var W = cv.width = cv.clientWidth * (window.devicePixelRatio || 1), H = cv.height = Math.round(W * 0.62); ctx.clearRect(0, 0, W, H);
      if (!res || !res.r2) return;
      var rmax = Math.max(res.r1, res.r2), sc = Math.min(W, H) * 0.46 / rmax, cx = W / 2 + (res.r2 > res.r1 ? (res.r2 - res.r1) / 2 * sc : -(res.r1 - res.r2) / 2 * sc) * 0.0, cy = H / 2;
      var rtl = document.documentElement.dir === 'rtl', sgn = rtl ? -1 : 1;
      ctx.lineWidth = Math.max(1.5, W / 400);
      ctx.fillStyle = '#2b7bd6'; ctx.beginPath(); ctx.arc(cx, cy, RE * sc, 0, 7); ctx.fill();
      ctx.setLineDash([6, 6]); ctx.strokeStyle = '#8fd3ff'; ctx.beginPath(); ctx.arc(cx, cy, res.r1 * sc, 0, 7); ctx.stroke();
      ctx.strokeStyle = '#7CFC98'; ctx.beginPath(); ctx.arc(cx, cy, res.r2 * sc, 0, 7); ctx.stroke(); ctx.setLineDash([]);
      // transfer ellipse: focus at Earth, periapsis on +x (raise) or apoapsis on +x (lower)
      var a = res.at, e = res.e, raise = res.r2 >= res.r1;
      ctx.strokeStyle = '#ffd54a'; ctx.beginPath();
      for (var k = 0; k <= 200; k++) { var nu = Math.PI * k / 200, rr = a * (1 - e * e) / (1 + e * Math.cos(nu)); var ang = raise ? nu : nu + Math.PI; var px = cx + sgn * rr * Math.cos(ang) * sc * (raise ? 1 : -1) * (raise ? 1 : -1), py = cy - rr * Math.sin(ang) * sc; k ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }
      ctx.stroke();
      // rocket position: solve Kepler's equation for time fraction p of the half orbit (M from 0 to pi)
      var M = Math.PI * p, E = M; for (var i = 0; i < 30; i++) E -= (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
      var nu2 = 2 * Math.atan2(Math.sqrt(1 + e) * Math.sin(E / 2), Math.sqrt(1 - e) * Math.cos(E / 2)), r = a * (1 - e * Math.cos(E)), an = raise ? nu2 : nu2 + Math.PI;
      var x = cx + sgn * r * Math.cos(an) * sc, y = cy - r * Math.sin(an) * sc;
      ctx.fillStyle = '#ff6b6b'; ctx.beginPath(); ctx.arc(x, y, Math.max(5, W / 90), 0, 7); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.font = Math.round(W / 45) + 'px system-ui,sans-serif'; ctx.fillText('🚀', x + 8, y - 8);
    }
    function loop(now) { var p = Math.min(1, (now - t0) / 6000); draw(p); if (p < 1 && playing) raf = requestAnimationFrame(loop); else { playing = false; playBtn.textContent = t.play; } }
    function play(on) { playing = on; playBtn.textContent = on ? t.pause : t.play; if (on) { cancelAnimationFrame(raf); raf = requestAnimationFrame(loop); } }
    f.addEventListener('change', sync); f.addEventListener('submit', function (ev) { ev.preventDefault(); compute(); });
    playBtn.addEventListener('click', function () { if (playing) { play(false); } else { t0 = performance.now(); play(true); } });
    window.addEventListener('resize', function () { if (!playing) draw(reduce ? 0.5 : 1); });
    sync(); compute();
  });
})(typeof window !== 'undefined' ? window : globalThis);
