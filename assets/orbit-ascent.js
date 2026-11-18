/* Teaching ascent on a real Blue Marble, drawn to scale.
   Pitch program (stated on the page, not a flown guidance law):
   flight-path angle goes from 90° (straight up) to 0° (horizontal) while
   speed goes from 0 to circular speed at 400 km. Path length is chosen so
   the end radius is 6 778 km. Density and dynamic pressure use U.S. Standard
   Atmosphere, 1976, below its 86 km top. */
(function (root) {
  'use strict';
  if (typeof document !== 'undefined') {
    document.addEventListener('click', function (ev) {
      var node = ev.target;
      var btn = node && node.closest ? node.closest('button.ytf') : null;
      if (!btn) return;
      var key = btn.getAttribute('data-yt');
      var src, title;
      if (key === 'aWCCNYJV3Zw') {
        src = 'https://www.youtube-nocookie.com/embed/aWCCNYJV3Zw?autoplay=1&playsinline=1&rel=0&enablejsapi=1';
        title = "Slow Motion Liftoff of NASA's Artemis I Moon Rocket";
      } else if (key === 'FSyfFrMcuQI') {
        src = 'https://www.youtube-nocookie.com/embed/FSyfFrMcuQI?autoplay=1&playsinline=1&rel=0&enablejsapi=1';
        title = 'Artemis I Launching to the Moon: Official NASA Launch Trailer';
      } else return;
      var frame = document.createElement('iframe');
      frame.className = 'oc-frame';
      frame.src = src;
      frame.title = title;
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      frame.allowFullscreen = true;
      btn.replaceWith(frame);
    });
  }
  var MU = 398600.4418, RE = 6378.137, HORB = 400;
  var RSTAR = 8314.32, M0 = 28.9644, G0 = 9.80665, R0 = 6356766;
  var T0 = 288.15, P0 = 101325;
  var H0 = (RSTAR / M0) * T0 / G0 / 1000;
  var BREAKS = [0, 11000, 20000, 32000, 47000, 51000, 71000, 84852];
  var LAPSE = [-0.0065, 0, 0.001, 0.0028, 0, -0.0028, -0.002];
  function bases() {
    var T = [T0], P = [P0];
    for (var i = 0; i < LAPSE.length; i++) {
      var dH = BREAKS[i + 1] - BREAKS[i], L = LAPSE[i];
      if (Math.abs(L) < 1e-15) {
        T.push(T[i]);
        P.push(P[i] * Math.exp(-G0 * M0 * dH / (RSTAR * T[i])));
      } else {
        var T2 = T[i] + L * dH;
        T.push(T2);
        P.push(P[i] * Math.pow(T2 / T[i], -G0 * M0 / (RSTAR * L)));
      }
    }
    return { T: T, P: P };
  }
  var BASE = bases();
  function ussa(zM) {
    if (zM < 0) zM = 0;
    var H = R0 * zM / (R0 + zM);
    if (H >= 84852) return null;
    var i = 0;
    while (i < LAPSE.length - 1 && H >= BREAKS[i + 1]) i++;
    var L = LAPSE[i], T = BASE.T[i], P = BASE.P[i], dH = H - BREAKS[i];
    if (Math.abs(L) < 1e-15) P = P * Math.exp(-G0 * M0 * dH / (RSTAR * T));
    else { T = T + L * dH; P = BASE.P[i] * Math.pow(T / BASE.T[i], -G0 * M0 / (RSTAR * L)); }
    return { T: T, P: P, rho: P * M0 / (RSTAR * T) };
  }
  function gammaOf(u) { return Math.PI / 2 * Math.pow(1 - u, 2.4); }
  function radiusAt(S) {
    var r = RE, th = 0, n = 600, ds = S / n;
    for (var i = 0; i < n; i++) {
      var gamma = gammaOf((i + 0.5) / n);
      r += Math.sin(gamma) * ds;
      th += Math.cos(gamma) / Math.max(r, 1) * ds;
    }
    return r;
  }
  function solveS() {
    var lo = 100, hi = 20000, target = RE + HORB;
    for (var k = 0; k < 40; k++) {
      var mid = (lo + hi) / 2;
      if (radiusAt(mid) < target) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  }
  function build() {
    var S = solveS();
    var vC = Math.sqrt(MU / (RE + HORB));
    var n = 500, pts = [], qMax = -1, qAt = 0;
    var r = RE, th = 0;
    for (var i = 0; i <= n; i++) {
      var u = i / n;
      var gamma = gammaOf(u);
      var v = vC * Math.pow(u, 0.55);
      var h = r - RE;
      var atm = h * 1000 < 84852 ? ussa(h * 1000) : null;
      var q = atm ? 0.5 * atm.rho * (v * 1000) * (v * 1000) : null;
      if (q != null && q > qMax) { qMax = q; qAt = i; }
      pts.push({ u: u, r: r, th: th, h: h, v: v, gamma: gamma, q: q, rho: atm ? atm.rho : null });
      if (i === n) break;
      var ds = S / n;
      r += Math.sin(gamma) * ds;
      th += Math.cos(gamma) / Math.max(r, 1) * ds;
    }
    function atH(km) {
      for (var j = 1; j < pts.length; j++) if (pts[j].h >= km) return j;
      return pts.length - 1;
    }
    function atGamma(deg) {
      var g = deg * Math.PI / 180;
      for (var j = 1; j < pts.length; j++) if (pts[j].gamma <= g) return j;
      return pts.length - 1;
    }
    var stages = [
      { id: 'liftoff', i: 0 },
      { id: 'maxq', i: qAt },
      { id: 'turn', i: atGamma(45) },
      { id: 'sep', i: atH(80.5) },
      { id: 'fairing', i: atH(100) },
      { id: 'burn2', i: atGamma(20) },
      { id: 'seco', i: n }
    ];
    return { pts: pts, stages: stages, vC: vC, H0: H0, qMax: qMax };
  }
  root.OrbitAscent = { build: build, ussa: ussa, H0: H0, RE: RE, MU: MU };
  if (typeof document === 'undefined') return;

  document.addEventListener('DOMContentLoaded', function () {
    var app = document.getElementById('ascent-app');
    if (!app) return;
    var ui = {};
    try { ui = JSON.parse(app.getAttribute('data-ui')); } catch (e) { return; }
    var model = build();
    var cv = document.getElementById('ascent-c');
    var ctx = cv.getContext('2d');
    var scrub = document.getElementById('ascent-scrub');
    var read = document.getElementById('ascent-read');
    var cap = document.getElementById('ascent-cap');
    var sky = document.getElementById('ascent-sky');
    var play = document.getElementById('ascent-play');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var level = 'k';
    var playing = false, raf = 0;
    var lang = document.documentElement.lang || 'en';
    var nf = function (x, d) { return new Intl.NumberFormat(lang, { maximumFractionDigits: d, minimumFractionDigits: d }).format(x); };
    function layerName(h) {
      if (h < 12) return 'tropo';
      if (h < 50) return 'strato';
      if (h < 80) return 'meso';
      if (h < 700) return 'thermo';
      return 'exo';
    }
    function skyColor(h) {
      var f = Math.exp(-Math.min(h, 60) / model.H0);
      var r = Math.round(140 * f), g = Math.round(196 * f), b = Math.round(232 * f);
      return 'rgb(' + r + ',' + g + ',' + b + ')';
    }
    var chart = document.createElement('canvas');
    chart.className = 'ascent-c';
    chart.style.aspectRatio = '16 / 5';
    chart.setAttribute('aria-hidden', 'true');
    cv.insertAdjacentElement('afterend', chart);
    function drawChart(q) {
      var ic = chart.getContext('2d');
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = chart.clientWidth || 960;
      var h = Math.round(w * 5 / 16);
      chart.width = Math.round(w * dpr);
      chart.height = Math.round(h * dpr);
      ic.setTransform(dpr, 0, 0, dpr, 0, 0);
      ic.fillStyle = '#07101f';
      ic.fillRect(0, 0, w, h);
      var end0 = model.pts[model.pts.length - 1];
      var maxX = Math.max(1, (RE + end0.h) * Math.sin(end0.th) * 1.05);
      var maxY = 460;
      var L = 36, R = 12, T = 22, B = 28;
      function X(th, alt) { return L + ((RE + alt) * Math.sin(th)) / maxX * (w - L - R); }
      function Y(alt) { return h - B - alt / maxY * (h - T - B); }
      ic.strokeStyle = 'rgba(255,255,255,.35)';
      ic.beginPath();
      ic.moveTo(L, T); ic.lineTo(L, h - B); ic.lineTo(w - R, h - B);
      ic.stroke();
      ic.strokeStyle = '#ffd54a';
      ic.lineWidth = 2.5;
      ic.beginPath();
      for (var i = 0; i < model.pts.length; i += 2) {
        var p = model.pts[i];
        var x = X(p.th, p.h), y = Y(p.h);
        if (i) ic.lineTo(x, y); else ic.moveTo(x, y);
        if (p.u > q.u) break;
      }
      ic.stroke();
      ic.fillStyle = '#fff';
      ic.beginPath();
      ic.arc(X(q.th, q.h), Y(q.h), 5, 0, Math.PI * 2);
      ic.fill();
      ic.fillStyle = '#f4f7fb';
      ic.font = '600 13px Montserrat, Segoe UI, sans-serif';
      ic.fillText(ui.chart || 'Altitude vs downrange, kilometres', L, 16);
      ic.fillText('0', L - 4, h - 8);
      ic.fillText('400 km', 4, Y(400) + 4);
    }
    function draw(idx) {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var cssW = cv.clientWidth || 960;
      var cssH = Math.round(cssW * 9 / 16);
      cv.width = Math.round(cssW * dpr);
      cv.height = Math.round(cssH * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = skyColor(model.pts[idx].h);
      ctx.fillRect(0, 0, cssW, cssH);
      var Rpx = Math.min(cssW, cssH) * 1.35;
      var cx = cssW * 0.46, cy = cssH * 0.58 + Rpx * 0.72;
      var sc = Rpx / RE;
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, Rpx, 0, Math.PI * 2);
      ctx.clip();
      if (window.SPGlobe) ctx.drawImage(window.SPGlobe, cx - Rpx, cy - Rpx, Rpx * 2, Rpx * 2);
      else { ctx.fillStyle = '#071018'; ctx.fillRect(cx - Rpx, cy - Rpx, Rpx * 2, Rpx * 2); }
      ctx.restore();
      ctx.beginPath();
      ctx.arc(cx, cy, Rpx, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255,255,255,.45)';
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.beginPath();
      ctx.strokeStyle = '#ffd54a';
      ctx.lineWidth = 2.5;
      for (var i = 0; i <= idx; i += 2) {
        var p = model.pts[i];
        var ang = -Math.PI / 2 + p.th;
        var rr = p.r * sc;
        var x = cx + rr * Math.cos(ang), y = cy + rr * Math.sin(ang);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
      var q = model.pts[idx];
      var ang2 = -Math.PI / 2 + q.th;
      var x2 = cx + q.r * sc * Math.cos(ang2), y2 = cy + q.r * sc * Math.sin(ang2);
      ctx.fillStyle = '#fff';
      ctx.beginPath();
      ctx.arc(x2, y2, 5, 0, Math.PI * 2);
      ctx.fill();
      var radx = Math.cos(ang2), rady = Math.sin(ang2);
      var horx = -Math.sin(ang2), hory = Math.cos(ang2);
      var vx = Math.cos(q.gamma) * horx + Math.sin(q.gamma) * radx;
      var vy = Math.cos(q.gamma) * hory + Math.sin(q.gamma) * rady;
      ctx.strokeStyle = '#ff8a80';
      ctx.beginPath();
      ctx.moveTo(x2, y2);
      ctx.lineTo(x2 + vx * 28, y2 + vy * 28);
      ctx.stroke();
      var end = model.pts[model.pts.length - 1];
      drawChart(q);
      var ae = -Math.PI / 2 + end.th;
      ctx.fillStyle = '#f4f7fb';
      ctx.font = '600 14px Montserrat, Segoe UI, sans-serif';
      ctx.fillText(ui.sideways || 'Sideways', cx + end.r * sc * Math.cos(ae) + 10, cy + end.r * sc * Math.sin(ae) - 8);
      var line = (ui.read || '{h} km, {v} km/s')
        .replace('{h}', nf(q.h, q.h < 20 ? 2 : 1))
        .replace('{v}', nf(q.v, 2))
        .replace('{layer}', ui[layerName(q.h)] || '')
        .replace('{g}', nf(q.gamma * 180 / Math.PI, 0));
      if (read) read.textContent = line;
      cv.setAttribute('aria-label', line);
      if (sky) sky.style.background = skyColor(q.h);
      var st = model.stages[0];
      for (var s = 0; s < model.stages.length; s++) {
        if (model.stages[s].i <= idx && model.stages[s].i >= st.i) st = model.stages[s];
      }
      if (cap) cap.textContent = (ui.caps && ui.caps[st.id] && ui.caps[st.id][level]) || '';
      app.querySelectorAll('[data-stage]').forEach(function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-stage') === st.id ? 'true' : 'false');
      });
    }
    function go(idx) {
      idx = Math.max(0, Math.min(model.pts.length - 1, idx | 0));
      if (scrub) scrub.value = String(Math.round(1000 * idx / (model.pts.length - 1)));
      draw(idx);
    }
    if (scrub) scrub.addEventListener('input', function () {
      playing = false;
      go(Math.round((+scrub.value) / 1000 * (model.pts.length - 1)));
    });
    app.querySelectorAll('[data-stage]').forEach(function (b) {
      b.addEventListener('click', function () {
        playing = false;
        var id = b.getAttribute('data-stage');
        for (var i = 0; i < model.stages.length; i++) if (model.stages[i].id === id) go(model.stages[i].i);
      });
    });
    app.querySelectorAll('[data-lv]').forEach(function (b) {
      b.addEventListener('click', function () {
        level = b.getAttribute('data-lv');
        app.querySelectorAll('[data-lv]').forEach(function (x) {
          var on = x === b;
          x.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        go(Math.round((+scrub.value) / 1000 * (model.pts.length - 1)));
      });
    });
    function tick() {
      if (!playing) return;
      var idx = Math.round((+scrub.value) / 1000 * (model.pts.length - 1)) + 2;
      if (idx >= model.pts.length) { playing = false; if (play) play.textContent = ui.play || 'Play'; return; }
      go(idx);
      raf = requestAnimationFrame(tick);
    }
    if (play) {
      if (reduce) play.hidden = true;
      play.addEventListener('click', function () {
        playing = !playing;
        play.textContent = playing ? (ui.pause || 'Pause') : (ui.play || 'Play');
        if (playing) raf = requestAnimationFrame(tick);
      });
    }
    window.addEventListener('sp-globe', function () { go(Math.round((+scrub.value) / 1000 * (model.pts.length - 1))); });
    window.addEventListener('resize', function () { go(Math.round((+scrub.value) / 1000 * (model.pts.length - 1))); });
    go(0);
  });
})(typeof window !== 'undefined' ? window : globalThis);
