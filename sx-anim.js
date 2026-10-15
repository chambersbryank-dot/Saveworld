/* Satellite Explorer animations (Oct 14): docking bursts + starfield parallax, launch-to-orbit mission, orbit types + Kepler overlay,
   laser vs radio links with ground-station handoff, onboard SI cloud filter + water savings. Vanilla Canvas 2D, no libraries.
   Respects prefers-reduced-motion (static frames) and has a Pause control (WCAG 2.2.2). Strings come from hidden [data-s] spans (translated). */
(function () {
  'use strict';
  var root = document.getElementById('sx'); if (!root || !window.requestAnimationFrame) return;
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)');
  var reduced = !!(RM && RM.matches), paused = false;
  var RTL = document.documentElement.dir === 'rtl';
  var S = {}; [].forEach.call(document.querySelectorAll('[data-s]'), function (e) { S[e.dataset.s] = e.textContent.trim(); });
  function s(k) { return S[k] || k; }
  var MU = 398600.4418, RE = 6371; // km^3/s^2, km
  function period(h) { return 2 * Math.PI * Math.sqrt(Math.pow(RE + h, 3) / MU); } // s (Kepler's third law)
  function speed(h) { return Math.sqrt(MU / (RE + h)); } // km/s (circular)
  function level() { var r = document.querySelector('input[name="sx-level"]:checked'); return r ? +r.value : 1; }
  function nf(x, d) { try { return x.toLocaleString(document.documentElement.lang || 'en', { maximumFractionDigits: d, minimumFractionDigits: d }); } catch (_) { return x.toFixed(d); } }
  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function ease(x) { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); }
  function rnd(a, b) { return a + Math.random() * (b - a); }
  var DPR = Math.min(window.devicePixelRatio || 1, 2);

  /* ---------- scene manager: one rAF, only visible scenes draw ---------- */
  var scenes = [];
  function Scene(cv, draw) {
    var sc = { cv: cv, ctx: cv.getContext('2d'), draw: draw, vis: false, t: 0, W: 0, H: 0 };
    function fit() { var r = cv.getBoundingClientRect(); sc.W = r.width; sc.H = r.height; cv.width = Math.round(r.width * DPR); cv.height = Math.round(r.height * DPR); sc.ctx.setTransform(DPR, 0, 0, DPR, 0, 0); once(sc); }
    sc.fit = fit; fit();
    if (window.ResizeObserver) new ResizeObserver(fit).observe(cv); else addEventListener('resize', fit);
    if (window.IntersectionObserver) new IntersectionObserver(function (es) { sc.vis = es[0].isIntersecting; kick(); }, { rootMargin: '80px' }).observe(cv); else sc.vis = true;
    scenes.push(sc); return sc;
  }
  function once(sc) { if (sc.W) { sc.ctx.clearRect(0, 0, sc.W, sc.H); sc.draw(sc, 0); } }
  var running = false, last = 0;
  function kick() { if (!running && !reduced && !paused && scenes.some(function (x) { return x.vis; })) { running = true; last = performance.now(); requestAnimationFrame(frame); } if (reduced || paused) scenes.forEach(once); }
  function frame(now) {
    var dt = Math.min((now - last) / 1000, 0.05); last = now;
    var any = false;
    scenes.forEach(function (sc) { if (sc.vis && sc.W) { any = true; sc.t += dt; sc.ctx.clearRect(0, 0, sc.W, sc.H); sc.draw(sc, dt); } });
    if (any && !paused && !reduced) requestAnimationFrame(frame); else running = false;
  }
  if (RM && RM.addEventListener) RM.addEventListener('change', function () { reduced = RM.matches; kick(); });

  /* ---------- shared drawing ---------- */
  function stars(n, seed) { var a = [], x = seed || 7; function r() { x = (x * 16807) % 2147483647; return x / 2147483647; } for (var i = 0; i < n; i++) a.push({ x: r(), y: r(), z: 0.3 + r() * 0.7, p: r() * 6.28 }); return a; }
  function drawStars(c, st, W, H, t, ox, oy, alpha) {
    for (var i = 0; i < st.length; i++) { var q = st[i], tw = reduced ? 1 : 0.6 + 0.4 * Math.sin(t * 2 + q.p);
      var x = ((q.x * W + (ox || 0) * q.z) % W + W) % W, y = ((q.y * H + (oy || 0) * q.z) % H + H) % H;
      c.globalAlpha = (alpha == null ? 1 : alpha) * tw * q.z; c.fillStyle = q.z > 0.85 ? '#cfe6ff' : '#fff'; c.fillRect(x, y, q.z * 1.6, q.z * 1.6); }
    c.globalAlpha = 1;
  }
  var LAND = [[-0.3, 0.9, 0.5], [0.2, 0.7, 0.35], [0.5, 2.2, 0.55], [-0.5, 2.6, 0.3], [0.1, 3.9, 0.45], [-0.35, 4.6, 0.3], [0.6, 5.4, 0.4], [-0.75, 1.8, 0.25], [0.35, -0.5, 0.3]];
  function drawEarth(c, cx, cy, R, rot) {
    var g = c.createRadialGradient(cx - R * 0.35, cy - R * 0.35, R * 0.1, cx, cy, R);
    g.addColorStop(0, '#4fb3ff'); g.addColorStop(0.6, '#1565c0'); g.addColorStop(1, '#0a2d6b');
    c.save(); c.beginPath(); c.arc(cx, cy, R, 0, 6.2832); c.fillStyle = g; c.fill(); c.clip();
    for (var i = 0; i < LAND.length; i++) { var L = LAND[i];
      for (var k = 0; k < 5; k++) { var lon = L[1] + rot + k * 0.12, lat = L[0] + Math.sin(k * 2.1) * 0.12, cz = Math.cos(lon) * Math.cos(lat); if (cz < -0.05) continue;
        var x = cx + R * Math.sin(lon) * Math.cos(lat), y = cy - R * Math.sin(lat), rr = R * L[2] * 0.32 * (0.4 + 0.6 * Math.max(cz, 0));
        c.fillStyle = Math.abs(L[0]) > 0.7 ? '#e8f4ff' : (k % 2 ? '#3f9b4f' : '#5aa85a'); c.beginPath(); c.ellipse(x, y, rr * Math.max(cz, 0.15), rr, 0, 0, 6.2832); c.fill(); } }
    // clouds
    c.globalAlpha = 0.35; c.fillStyle = '#fff';
    for (var j = 0; j < 12; j++) { var lo = j * 0.53 + rot * 1.3, la = Math.sin(j * 1.7) * 0.9, z = Math.cos(lo) * Math.cos(la); if (z < 0) continue;
      c.beginPath(); c.ellipse(cx + R * Math.sin(lo) * Math.cos(la), cy - R * Math.sin(la), R * 0.16 * z, R * 0.04, 0, 0, 6.2832); c.fill(); }
    c.globalAlpha = 1;
    // night side (sun from the left) + city lights
    var n = c.createLinearGradient(cx - R * 0.15, 0, cx + R * 0.45, 0); n.addColorStop(0, 'rgba(2,6,25,0)'); n.addColorStop(1, 'rgba(2,6,25,.82)');
    c.fillStyle = n; c.fillRect(cx - R, cy - R, 2 * R, 2 * R);
    c.fillStyle = '#ffd36b';
    for (i = 0; i < LAND.length; i++) { L = LAND[i]; for (k = 0; k < 6; k++) { lon = L[1] + rot + k * 0.09; lat = L[0] + Math.cos(k * 3.3) * 0.1; cz = Math.cos(lon) * Math.cos(lat);
      x = cx + R * Math.sin(lon) * Math.cos(lat); if (cz < 0.1 || x < cx + R * 0.2 || Math.abs(L[0]) > 0.7) continue; c.globalAlpha = 0.5 + 0.5 * Math.sin(k + i); c.fillRect(x, cy - R * Math.sin(lat), 1.6, 1.6); } }
    c.globalAlpha = 1; c.restore();
    var a = c.createRadialGradient(cx, cy, R * 0.9, cx, cy, R * 1.14); a.addColorStop(0, 'rgba(120,200,255,0)'); a.addColorStop(0.42, 'rgba(120,200,255,.5)'); a.addColorStop(1, 'rgba(120,200,255,0)');
    c.fillStyle = a; c.beginPath(); c.arc(cx, cy, R * 1.12, 0, 6.2832); c.fill();
  }
  // satellite sprite: unfold 0..1 (solar wings), ant 0..1 (dish)
  function drawSat(c, x, y, sz, unfold, ant, ang, glow) {
    c.save(); c.translate(x, y); c.rotate(ang || 0); var u = sz;
    if (glow) { var g = c.createRadialGradient(0, 0, 0, 0, 0, u * 3); g.addColorStop(0, 'rgba(190,170,255,.45)'); g.addColorStop(1, 'rgba(190,170,255,0)'); c.fillStyle = g; c.fillRect(-u * 3, -u * 3, u * 6, u * 6); }
    var wl = u * (0.3 + 2.1 * unfold), segs = Math.max(1, Math.round(1 + 3 * unfold));
    [-1, 1].forEach(function (side) {
      c.strokeStyle = '#cfd8dc'; c.lineWidth = Math.max(1, u * 0.08); c.beginPath(); c.moveTo(side * u * 0.5, 0); c.lineTo(side * (u * 0.62), 0); c.stroke();
      var x0 = side > 0 ? u * 0.62 : -u * 0.62 - wl, sg = c.createLinearGradient(x0, -u * 0.4, x0 + wl, u * 0.4);
      sg.addColorStop(0, '#1a237e'); sg.addColorStop(0.5, '#3949ab'); sg.addColorStop(1, '#1e88e5');
      c.fillStyle = sg; c.fillRect(x0, -u * 0.38, wl, u * 0.76);
      c.strokeStyle = 'rgba(200,220,255,.75)'; c.lineWidth = Math.max(0.5, u * 0.03); c.strokeRect(x0, -u * 0.38, wl, u * 0.76);
      for (var i = 1; i < segs * 2; i++) { var xx = x0 + wl * i / (segs * 2); c.beginPath(); c.moveTo(xx, -u * 0.38); c.lineTo(xx, u * 0.38); c.stroke(); }
      c.beginPath(); c.moveTo(x0, 0); c.lineTo(x0 + wl, 0); c.stroke();
    });
    var bg = c.createLinearGradient(-u * 0.5, -u * 0.5, u * 0.5, u * 0.5); bg.addColorStop(0, '#ffe08a'); bg.addColorStop(0.5, '#c9962b'); bg.addColorStop(1, '#8a5d12');
    c.fillStyle = bg; c.fillRect(-u * 0.5, -u * 0.55, u, u * 1.1);
    c.strokeStyle = 'rgba(255,240,200,.6)'; c.lineWidth = Math.max(0.5, u * 0.04); c.strokeRect(-u * 0.5, -u * 0.55, u, u * 1.1);
    c.fillStyle = '#263238'; c.beginPath(); c.arc(0, u * 0.62, u * 0.2, 0, 6.2832); c.fill(); c.strokeStyle = '#90a4ae'; c.stroke();
    // antenna boom + dish
    var a = ant || 0; c.save(); c.translate(0, -u * 0.55); c.rotate(-1.4 * (1 - a));
    c.strokeStyle = '#eceff1'; c.lineWidth = Math.max(1, u * 0.07); c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -u * 0.5 * (0.3 + 0.7 * a)); c.stroke();
    c.fillStyle = '#eceff1'; c.beginPath(); c.ellipse(0, -u * 0.5 * (0.3 + 0.7 * a) - u * 0.12, u * 0.32 * (0.3 + 0.7 * a), u * 0.14, 0, 3.1416, 6.2832); c.fill();
    c.restore(); c.restore();
  }
  function label(c, txt, x, y, col, size, align, maxW) { c.font = '700 ' + size + 'px Montserrat,system-ui,sans-serif';
    if (maxW) { var mw = c.measureText(txt).width; if (mw > maxW) { size = Math.max(8, size * maxW / mw); c.font = '700 ' + size + 'px Montserrat,system-ui,sans-serif'; } } c.textAlign = align || 'center'; c.textBaseline = 'middle';
    c.lineWidth = 4; c.strokeStyle = 'rgba(5,8,30,.85)'; c.strokeText(txt, x, y); c.fillStyle = col || '#fff'; c.fillText(txt, x, y); }
  function arrow(c, x1, y1, x2, y2, col) { var a = Math.atan2(y2 - y1, x2 - x1); c.strokeStyle = c.fillStyle = col; c.lineWidth = 2.5; c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke();
    c.beginPath(); c.moveTo(x2, y2); c.lineTo(x2 - 10 * Math.cos(a - 0.4), y2 - 10 * Math.sin(a - 0.4)); c.lineTo(x2 - 10 * Math.cos(a + 0.4), y2 - 10 * Math.sin(a + 0.4)); c.fill(); }

  /* ---------- 1. Build stage: starfield parallax, tilt, docking bursts ---------- */
  var stage = root.querySelector('.sx-stage'), svg = stage && stage.querySelector('svg');
  if (stage) {
    var bgc = document.createElement('canvas'); bgc.className = 'sx-stars'; bgc.setAttribute('aria-hidden', 'true'); stage.insertBefore(bgc, stage.firstChild);
    var fx = document.createElement('canvas'); fx.className = 'sx-fx'; fx.setAttribute('aria-hidden', 'true'); stage.appendChild(fx);
    var st1 = stars(110, 11), px = 0, py = 0, tx = 0, ty = 0, parts = [];
    stage.addEventListener('pointermove', function (e) { var r = stage.getBoundingClientRect(); tx = (e.clientX - r.left) / r.width - 0.5; ty = (e.clientY - r.top) / r.height - 0.5; });
    stage.addEventListener('pointerleave', function () { tx = ty = 0; });
    Scene(bgc, function (sc, dt) { var c = sc.ctx; px += (tx - px) * 0.06; py += (ty - py) * 0.06;
      drawStars(c, st1, sc.W, sc.H, sc.t, -px * 40 - sc.t * 6, -py * 40, 1);
      if (svg && !reduced) svg.style.transform = 'perspective(800px) rotateY(' + (px * 10).toFixed(2) + 'deg) rotateX(' + (-py * 10).toFixed(2) + 'deg) translateY(' + (Math.sin(sc.t * 1.2) * 1.2).toFixed(2) + '%)'; });
    var fxs = Scene(fx, function (sc, dt) { var c = sc.ctx; c.globalCompositeOperation = 'lighter';
      for (var i = parts.length - 1; i >= 0; i--) { var p = parts[i]; p.life -= dt; if (p.life <= 0) { parts.splice(i, 1); continue; }
        var k = p.life / p.max;
        if (p.ring) { c.strokeStyle = 'rgba(255,213,74,' + k + ')'; c.lineWidth = 3 * k; c.beginPath(); c.arc(p.x, p.y, (1 - k) * p.r, 0, 6.2832); c.stroke(); continue; }
        p.x += p.vx * dt; p.y += p.vy * dt; p.vx *= 0.94; p.vy *= 0.94;
        c.fillStyle = 'hsla(' + p.h + ',100%,70%,' + k + ')'; c.beginPath(); c.arc(p.x, p.y, p.s * (0.5 + k), 0, 6.2832); c.fill(); }
      c.globalCompositeOperation = 'source-over'; });
    root.addEventListener('sx:dock', function (e) {
      var slot = e.detail.slot, r = stage.getBoundingClientRect(), b = slot.getBoundingClientRect(), x = b.left - r.left + b.width / 2, y = b.top - r.top + b.height / 2;
      var g = svg && svg.querySelector('[data-p="' + e.detail.part + '"]'); if (g) g.classList.add('on');
      slot.classList.remove('sx-pop'); void slot.offsetWidth; slot.classList.add('sx-pop');
      try { if (navigator.vibrate) navigator.vibrate(e.detail.left ? 15 : [20, 40, 20, 40, 60]); } catch (_) {}
      if (reduced) return;
      var n = e.detail.left ? 26 : 70;
      for (var i = 0; i < n; i++) { var a = rnd(0, 6.2832), v = rnd(60, e.detail.left ? 220 : 380); parts.push({ x: x, y: y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, s: rnd(1.5, 3.5), h: rnd(35, 60) + (i % 3) * 80, life: rnd(0.5, 1.1), max: 1.1 }); }
      parts.push({ ring: 1, x: x, y: y, r: e.detail.left ? 70 : 160, life: 0.6, max: 0.6 });
      fxs.vis = true; kick();
      if (!e.detail.left) { stage.classList.add('sx-complete'); var lb = document.getElementById('sx-launch'); if (lb) lb.classList.add('sx-ready'); }
    });
    root.addEventListener('sx:reset', function () { if (svg) [].forEach.call(svg.querySelectorAll('[data-p]'), function (g) { g.classList.remove('on'); }); stage.classList.remove('sx-complete'); var lb = document.getElementById('sx-launch'); if (lb) lb.classList.remove('sx-ready'); mission.lt = -1; mission.cap = ''; setCap(s('idle')); });
  }

  /* ---------- 2. Mission: launch -> orbit, plus level overlays ---------- */
  var mcv = document.getElementById('sx-cv-mission'), capEl = document.getElementById('sx-cap'), alt = document.getElementById('sx-alt'), out = document.getElementById('sx-readout');
  var mission = { lt: -1, cap: '', smoke: [], st: stars(160, 3) };
  function setCap(t) { if (capEl && capEl.textContent !== t) capEl.textContent = t; }
  function readout() { if (!alt || !out) return; var h = +alt.value, T = period(h) / 60;
    out.textContent = s('altitude') + ' ' + nf(h, 0) + ' ' + s('km') + ' · ' + s('speed') + ' ' + nf(speed(h), 2) + ' ' + s('kms') + ' · ' + s('period') + ' ' + (T < 600 ? nf(T, 1) + ' ' + s('min') : nf(T / 60, 2) + ' ' + s('h')); }
  if (alt) { alt.addEventListener('input', function () { readout(); kick(); }); readout(); }
  var TL = [[0, 'count3'], [1, 'count2'], [2, 'count1'], [3, 'liftoff'], [5, 'maxq'], [7, 'staging'], [9.5, 'fairing'], [11.5, 'orbit'], [12.5, 'arrays'], [14, 'antenna'], [15.5, 'ready']];
  var END = 16;
  function capFor(t) { var k = 'idle'; for (var i = 0; i < TL.length; i++) if (t >= TL[i][0]) k = TL[i][1]; return s(k); }
  function drawRocket(c, x, y, u, t, sep, fair) {
    // y = base of 2nd stage; stage 1 hangs below until sep
    var fo = fair ? ease(fair) : 0;
    // fairing halves (open around the satellite)
    if (fo > 0) drawSat(c, x, y - u * 62, u * 7, 0, 0, 0, fo > 0.5);
    [-1, 1].forEach(function (sd) { c.save(); c.translate(x + sd * fo * u * 34, y - u * 50 + fo * u * 26); c.rotate(sd * fo * 1.1); c.globalAlpha = 1 - fo * 0.6;
      var fg = c.createLinearGradient(0, 0, sd * u * 9, 0); fg.addColorStop(0, '#ffffff'); fg.addColorStop(1, '#b0bec5'); c.fillStyle = fg;
      c.beginPath(); c.moveTo(0, 0); c.lineTo(sd * u * 9, 0); c.lineTo(sd * u * 9, -u * 16); c.quadraticCurveTo(sd * u * 8, -u * 34, 0, -u * 40); c.closePath(); c.fill();
      c.strokeStyle = 'rgba(120,140,160,.6)'; c.lineWidth = 1; c.stroke(); c.restore(); });
    c.globalAlpha = 1;
    var g = c.createLinearGradient(x - u * 9, 0, x + u * 9, 0); g.addColorStop(0, '#b0bec5'); g.addColorStop(0.45, '#ffffff'); g.addColorStop(1, '#90a4ae');
    c.fillStyle = g; c.fillRect(x - u * 7, y - u * 50, u * 14, u * 50); // 2nd stage
    c.fillStyle = '#ff8a65'; c.fillRect(x - u * 7, y - u * 12, u * 14, u * 2);
    c.fillStyle = '#37474f'; c.beginPath(); c.moveTo(x - u * 4, y); c.lineTo(x + u * 4, y); c.lineTo(x + u * 6, y + u * 7); c.lineTo(x - u * 6, y + u * 7); c.fill();
    if (!sep) { c.fillStyle = g; c.fillRect(x - u * 9, y + u * 2, u * 18, u * 90); c.fillStyle = '#1e3a5f'; c.fillRect(x - u * 9, y + u * 30, u * 18, u * 4);
      label(c, 'SP', x, y + u * 50, '#1e3a5f', u * 7); c.fillStyle = '#37474f'; c.fillRect(x - u * 10, y + u * 88, u * 20, u * 6); }
  }
  function plume(c, x, y, u, pow, t) { if (pow <= 0) return; c.save(); c.globalCompositeOperation = 'lighter';
    var L = u * (30 + 25 * pow + Math.sin(t * 40) * 3), g = c.createLinearGradient(0, y, 0, y + L); g.addColorStop(0, 'rgba(255,255,220,.95)'); g.addColorStop(0.3, 'rgba(255,170,60,.8)'); g.addColorStop(1, 'rgba(255,80,20,0)');
    c.fillStyle = g; c.beginPath(); c.moveTo(x - u * 6, y); c.quadraticCurveTo(x, y + L * 1.2, x + u * 6, y); c.fill(); c.restore(); }
  function missionDraw(sc, dt) {
    var c = sc.ctx, W = sc.W, H = sc.H, lv = level(), t = mission.lt, u = H / 300;
    if (reduced && t >= 0) t = END + 2;
    if (t >= 0 && !reduced) mission.lt += dt;
    if (t < 0 || t >= 11) { // orbit view (idle shows orbit too, with stowed satellite)
      var f = t < 0 ? 1 : ease((t - 11) / 0.8), ot = sc.t;
      c.fillStyle = '#030619'; c.fillRect(0, 0, W, H); drawStars(c, mission.st, W, H, ot, -ot * 3, 0, 1);
      var m = Math.min(W, H), cx = W / 2, cy = H / 2 + (lv === 1 ? H * 0.08 : 0);
      var Rp = lv === 1 ? m * 0.3 : m * 0.16; c.globalAlpha = f;
      drawEarth(c, cx, cy, Rp, ot * 0.08);
      var unf = t < 0 ? 0 : ease((t - 12.5) / 1.5), ant = t < 0 ? 0 : ease((t - 14) / 1.2);
      if (t < 0 && stage && stage.classList.contains('sx-complete')) unf = ant = 0;
      function rpx(h) { return Rp * (1 + 0.745 * Math.sqrt(h / RE)); }
      var SC = 5552 / 6; // time sped up so LEO laps in about 6 s
      if (lv === 1) {
        var A = ot * 0.5, ox = Math.cos(A) * Rp * 1.45, oy = Math.sin(A) * Rp * 0.42, behind = Math.sin(A) < 0;
        c.strokeStyle = 'rgba(190,170,255,.35)'; c.lineWidth = 2; c.setLineDash([4, 6]); c.beginPath(); c.ellipse(cx, cy, Rp * 1.45, Rp * 0.42, 0, 0, 6.2832); c.stroke(); c.setLineDash([]);
        if (behind) { drawEarth(c, cx, cy, Rp, ot * 0.08); }
        if (!behind || Math.abs(ox) > Rp) drawSat(c, cx + ox, cy - Rp * 0.1 + oy, m * 0.045 * (behind ? 0.8 : 1.1), unf, ant, Math.sin(A) * 0.2, true);
        for (var k = 1; k < 8 && !reduced; k++) { var B = A - k * 0.06; c.globalAlpha = f * (0.5 - k * 0.06); c.fillStyle = '#ffd54a'; c.beginPath(); c.arc(cx + Math.cos(B) * Rp * 1.45, cy - Rp * 0.1 + Math.sin(B) * Rp * 0.42, 3 - k * 0.3, 0, 6.2832); c.fill(); }
        c.globalAlpha = f;
      } else {
        var orbs = [['leo', 400, '#7fe3ff'], ['meo', 20200, '#ffd54a'], ['geo', 35786, '#ff9eb3']];
        if (lv === 3 && alt) orbs = [['you', +alt.value, '#b9f6ca']].concat(orbs.map(function (o) { return [o[0], o[1], 'rgba(255,255,255,.35)']; }));
        orbs.forEach(function (o, i) { var r = rpx(o[1]), w = 2 * Math.PI / period(o[1]) * SC, a = -ot * w + i * 1.3;
          c.strokeStyle = o[2]; c.globalAlpha = f * (o[0] === 'you' || lv === 2 ? 0.8 : 0.35); c.lineWidth = o[0] === 'you' ? 2.5 : 1.5; c.setLineDash(o[0] === 'you' ? [] : [3, 5]);
          c.beginPath(); c.arc(cx, cy, r, 0, 6.2832); c.stroke(); c.setLineDash([]); c.globalAlpha = f;
          var x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r;
          if (o[0] === 'you' || lv === 2) drawSat(c, x, y, m * (o[0] === 'you' ? 0.025 : 0.018), lv === 2 ? 1 : unf || 1, 1, a + 1.57, false);
          else { c.fillStyle = o[2]; c.beginPath(); c.arc(x, y, 3, 0, 6.2832); c.fill(); }
          if (lv === 2) { var T = period(o[1]) / 60; label(c, s(o[0]) + ' · ' + (T < 600 ? nf(T, 0) + ' ' + s('min') : nf(T / 60, 1) + ' ' + s('h')), cx, cy - r - 9, o[2], Math.max(11, m * 0.028)); }
          if (o[0] === 'you') { var v = speed(o[1]), L = 18 + v * 5; // velocity vector, tangent to orbit
            arrow(c, x, y, x + Math.sin(a) * L, y - Math.cos(a) * L, '#b9f6ca'); // tangent, direction of travel
            arrow(c, x, y, x + (cx - x) * 0.25, y + (cy - y) * 0.25, '#ff8a80');
            label(c, 'v = ' + nf(v, 2) + ' ' + s('kms'), x, y - 22, '#b9f6ca', Math.max(11, m * 0.028)); }
        });
        if (lv === 3) { var fs = Math.max(11, m * 0.027), x0 = RTL ? W - 12 : 12, al = RTL ? 'right' : 'left';
          label(c, 'T = 2π √(a³ / μ)', x0, 18, '#fff', fs, al); label(c, 'v = √(μ / a)', x0, 18 + fs * 1.5, '#fff', fs, al);
          label(c, 'μ = 398,600 km³/s² · R⊕ = 6,371 km', x0, 18 + fs * 3, 'rgba(255,255,255,.8)', fs * 0.85, al);
          label(c, s('gravity'), x0, H - 14, '#ff8a80', fs * 0.9, al); }
        label(c, s('notscale'), RTL ? 12 : W - 12, H - 14, 'rgba(255,255,255,.75)', Math.max(10, m * 0.024), RTL ? 'left' : 'right');
      }
      // day / night labels
      if (lv !== 3) { label(c, '☀ ' + s('day'), cx - Rp * 0.55, cy + Rp + 18, '#ffe082', Math.max(11, m * 0.028)); label(c, '🌙 ' + s('night'), cx + Rp * 0.55, cy + Rp + 18, '#b3c7ff', Math.max(11, m * 0.028)); }
      c.globalAlpha = 1;
      if (t >= 11 && t < 11.8) { c.fillStyle = 'rgba(255,255,255,' + (1 - f) + ')'; c.fillRect(0, 0, W, H); }
      setCap(t < 0 ? (stage && stage.classList.contains('sx-complete') ? s('built') : s('idle')) : reduced ? s('reducedsum') : capFor(t));
      return;
    }
    // launch view: camera follows the rocket
    var asc = t < 3 ? 0 : Math.pow(t - 3, 2) * 18, sky = clamp(asc / 900, 0, 1);
    var gr = c.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, 'rgb(' + Math.round(70 * (1 - sky) + 3) + ',' + Math.round(140 * (1 - sky) + 6) + ',' + Math.round(220 * (1 - sky) + 25) + ')');
    gr.addColorStop(1, 'rgb(' + Math.round(170 * (1 - sky) + 5) + ',' + Math.round(210 * (1 - sky) + 10) + ',' + Math.round(250 * (1 - sky) + 40) + ')'); c.fillStyle = gr; c.fillRect(0, 0, W, H);
    drawStars(c, mission.st, W, H, sc.t, 0, asc * 0.05, sky);
    var rx = W / 2, ry = H * 0.62 - Math.min(asc, H * 0.12), shake = t > 2.6 && t < 7 && !reduced ? Math.sin(t * 90) * u * 0.8 : 0;
    // clouds and ground (parallax)
    c.fillStyle = 'rgba(255,255,255,' + 0.8 * (1 - sky) + ')';
    [[0.15, 0.25], [0.75, 0.1], [0.4, -0.4], [0.85, -0.8], [0.2, -1.3]].forEach(function (q) { var y = H * q[1] + asc * 0.6; if (y > -40 && y < H + 40) { c.beginPath(); c.ellipse(W * q[0], y, W * 0.16, H * 0.03, 0, 0, 6.2832); c.ellipse(W * q[0] + W * 0.06, y - H * 0.02, W * 0.09, H * 0.03, 0, 0, 6.2832); c.fill(); } });
    var gy = H * 0.62 + u * 98 + asc; if (gy < H + 10) { c.fillStyle = '#2e5d34'; c.fillRect(0, gy, W, H); c.fillStyle = '#546e7a'; c.fillRect(rx + u * 22, gy - u * 150, u * 8, u * 150); c.fillRect(rx + u * 9, gy - u * 120, u * 14, u * 3); }
    // smoke + sparks
    var sm = mission.smoke, pow = t < 3 ? (t > 2.4 ? (t - 2.4) * 1.5 : 0) : t < 7 ? 1 : t < 7.6 ? 0 : t < 11 ? 0.6 : 0;
    var sep = t >= 7, nozzle = sep ? ry + u * 7 : ry + u * 94;
    if (!reduced && pow > 0) for (var i = 0; i < (t < 5 ? 6 : 3); i++) sm.push({ x: rx + rnd(-u * 5, u * 5), y: nozzle + u * 20, vx: rnd(-40, 40) * (t < 4 ? 3 : 1), vy: rnd(120, 260), r: rnd(u * 4, u * 9), life: 1.6 });
    for (i = sm.length - 1; i >= 0; i--) { var p = sm[i]; p.life -= dt; if (p.life <= 0 || sm.length > 400) { sm.splice(i, 1); continue; } p.x += p.vx * dt; p.y += p.vy * dt; p.r += dt * u * 14;
      c.fillStyle = 'rgba(' + (220 - sky * 120) + ',' + (220 - sky * 120) + ',' + (225 - sky * 110) + ',' + (p.life / 1.6) * 0.5 + ')'; c.beginPath(); c.arc(p.x, p.y, p.r, 0, 6.2832); c.fill(); }
    // spent first stage tumbling away
    if (sep) { var st = t - 7; c.save(); c.translate(rx - st * u * 6, ry + u * 48 + st * st * u * 30); c.rotate(st * 0.6); c.globalAlpha = clamp(1 - st / 3, 0, 1);
      c.fillStyle = '#cfd8dc'; c.fillRect(-u * 9, -u * 45, u * 18, u * 90); c.fillStyle = '#1e3a5f'; c.fillRect(-u * 9, -u * 17, u * 18, u * 4); c.restore();
      if (st < 0.35) { c.fillStyle = 'rgba(255,240,200,' + (1 - st / 0.35) * 0.8 + ')'; c.beginPath(); c.arc(rx, ry + u * 5, u * 30 * (st / 0.35 + 0.3), 0, 6.2832); c.fill(); } }
    plume(c, rx + shake, nozzle, u * (sep ? 0.7 : 1.2), pow, sc.t);
    drawRocket(c, rx + shake, ry, u, t, sep, t >= 9.5 ? (t - 9.5) / 1.4 : 0);
    if (t < 3) { var n = 3 - Math.floor(t), k2 = t % 1; c.globalAlpha = 1 - k2 * 0.7; label(c, String(n), W / 2, H * 0.22, '#ffd54a', H * (0.16 + k2 * 0.05)); c.globalAlpha = 1; }
    // HUD: altitude readout (illustrative)
    if (lv > 1 && t >= 3) label(c, 'T+' + nf(t - 3, 1) + ' s', RTL ? W - 12 : 12, 18, '#fff', Math.max(11, H * 0.04), RTL ? 'right' : 'left');
    setCap(capFor(t));
  }
  if (mcv) { var ms = Scene(mcv, missionDraw);
    var lb = document.getElementById('sx-launch');
    if (lb) lb.addEventListener('click', function () {
      if (stage && !stage.classList.contains('sx-complete')) { var a = document.getElementById('sx-auto'); if (a) a.click(); }
      mission.lt = 0; mission.smoke = []; mcv.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
      if (reduced) setCap(s('reducedsum')); ms.vis = true; kick(); once(ms); });
    [].forEach.call(document.querySelectorAll('input[name="sx-level"]'), function (r) { r.addEventListener('change', function () { scenes.forEach(once); }); });
    setCap(s('idle'));
  }

  /* ---------- 3. Laser vs radio + ground-station handoff ---------- */
  var ccv = document.getElementById('sx-cv-comm');
  if (ccv) { var cst = stars(60, 5), pk = [[], []], sent = [0, 0];
    Scene(ccv, function (sc, dt) { var c = sc.ctx, W = sc.W, H = sc.H, half = W / 2, m = Math.min(half, H), fs = Math.max(11, m * 0.055);
      c.fillStyle = '#050a24'; c.fillRect(0, 0, W, H); drawStars(c, cst, W, H * 0.6, sc.t, 0, 0, 0.8);
      c.fillStyle = 'rgba(255,255,255,.18)'; c.fillRect(half - 1, 0, 2, H);
      for (var lane = 0; lane < 2; lane++) { var laser = lane === 1, x0 = (RTL ? 1 - lane : lane) * half, t = sc.t, loop = 12, ph = (t % loop) / loop;
        var sx = x0 + half * (0.1 + 0.8 * ph), sy = H * 0.2, gy = H * 0.86, gs = [x0 + half * 0.28, x0 + half * 0.72];
        c.fillStyle = '#123b1d'; c.fillRect(x0, gy + 8, half, H - gy); c.fillStyle = '#1b5e20'; c.beginPath(); c.ellipse(x0 + half / 2, gy + 8, half * 0.7, 10, 0, 3.1416, 6.2832); c.fill();
        // drifting cloud blocks the laser at the station under it
        var cloudX = x0 + half * ((t * 0.035 + 0.6) % 1.2 - 0.1), cloudy = function (g) { return laser && Math.abs(cloudX - g) < half * 0.12; };
        c.fillStyle = 'rgba(230,236,245,.85)'; c.beginPath(); c.ellipse(cloudX, H * 0.62, half * 0.13, H * 0.05, 0, 0, 6.2832); c.ellipse(cloudX + half * 0.05, H * 0.58, half * 0.08, H * 0.05, 0, 0, 6.2832); c.fill();
        var best = -1, bd = 1e9; gs.forEach(function (g, i) { var d = Math.abs(g - sx); if (!cloudy(g) && d < bd && d < half * 0.42) { bd = d; best = i; } });
        gs.forEach(function (g, i) { c.fillStyle = i === best ? '#ffd54a' : '#90a4ae'; c.beginPath(); c.moveTo(g - 9, gy + 8); c.lineTo(g + 9, gy + 8); c.lineTo(g, gy - 6); c.fill();
          c.strokeStyle = c.fillStyle; c.lineWidth = 2; c.beginPath(); c.arc(g, gy - 10, 8, 3.6, 5.8); c.stroke(); });
        if (best >= 0) { var g = gs[best], tgy = gy - 12;
          if (laser) { c.save(); c.globalCompositeOperation = 'lighter'; c.strokeStyle = 'rgba(80,255,170,.35)'; c.lineWidth = 6; c.beginPath(); c.moveTo(sx, sy); c.lineTo(g, tgy); c.stroke(); c.strokeStyle = '#b9ffde'; c.lineWidth = 1.5; c.stroke(); c.restore(); }
          else { var gg = c.createLinearGradient(0, sy, 0, tgy); gg.addColorStop(0, 'rgba(120,180,255,.35)'); gg.addColorStop(1, 'rgba(120,180,255,.05)'); c.fillStyle = gg; c.beginPath(); c.moveTo(sx, sy); c.lineTo(g - half * 0.2, tgy + 14); c.lineTo(g + half * 0.2, tgy + 14); c.fill(); }
          var rate = laser ? 28 : 3; if (!reduced && Math.random() < rate * dt) pk[lane].push({ k: 0, g: g });
          if (reduced && !pk[lane].length) for (var q = 0; q < (laser ? 9 : 2); q++) pk[lane].push({ k: q / (laser ? 9 : 2), g: g });
        }
        var P = pk[lane]; for (var i = P.length - 1; i >= 0; i--) { var p = P[i]; if (!reduced) p.k += dt * (laser ? 1.6 : 0.7); if (p.k >= 1) { P.splice(i, 1); sent[lane]++; continue; }
          var px = sx + (p.g - sx) * p.k, py = sy + (gy - 12 - sy) * p.k; c.fillStyle = laser ? '#7dffc0' : '#9cc7ff'; c.fillRect(px - 3, py - 3, 6, 6); }
        drawSat(c, sx, sy, m * 0.07, 1, 1, 0, laser);
        label(c, laser ? s('laser') : s('radio'), x0 + half / 2, 16, laser ? '#7dffc0' : '#9cc7ff', fs * 1.1);
        var bw = half * 0.6, bx = x0 + half * 0.2, by = 34, fill = reduced ? (laser ? 1 : 0.15) : Math.min(1, (sent[lane] % (laser ? 400 : 400)) / 400);
        c.fillStyle = 'rgba(255,255,255,.15)'; c.fillRect(bx, by, bw, 8); c.fillStyle = laser ? '#7dffc0' : '#9cc7ff'; c.fillRect(RTL ? bx + bw * (1 - fill) : bx, by, bw * fill, 8);
        if (best >= 0 && laser && Math.abs(sx - (gs[0] + gs[1]) / 2) < half * 0.04) label(c, s('handoff'), x0 + half / 2, H * 0.45, '#ffd54a', fs * 0.9, 'center', half * 0.95);
        if (laser && gs.some(cloudy)) label(c, '☁ ' + s('blocked'), x0 + half / 2, H * 0.74, '#fff', fs * 0.8, 'center', half * 0.95);
      }
      label(c, s('illustrative'), W / 2, H - 10, 'rgba(255,255,255,.8)', fs * 0.8, 'center', W * 0.95);
    }); }

  /* ---------- 4. Onboard SI: discard cloudy images; water drops ---------- */
  var acv = document.getElementById('sx-cv-ai');
  if (acv) { var tiles = [], spawn = 0, cnt = [0, 0], seq = 0;
    Scene(acv, function (sc, dt) { var c = sc.ctx, W = sc.W, H = sc.H, m = Math.min(W, H), fs = clamp(W * 0.03, 10, 17), dir = RTL ? -1 : 1;
      var bg = c.createLinearGradient(0, 0, W, H); bg.addColorStop(0, '#0b1240'); bg.addColorStop(1, '#14063a'); c.fillStyle = bg; c.fillRect(0, 0, W, H);
      var top = H * 0.52, X = function (f) { return RTL ? W * (1 - f) : W * f; }, chipX = X(0.5), chipY = top * 0.5, ts = Math.max(22, m * 0.11);
      // camera, chip, downlink
      label(c, '🛰️', X(0.07), chipY, '#fff', ts); label(c, '📡', X(0.93), chipY, '#fff', ts);
      spawn -= dt; if (!reduced && spawn <= 0) { spawn = 0.75; tiles.push({ f: 0.12, cloud: [1, 0, 1, 1, 0, 1, 0, 0][seq++ % 8] === 1, y: 0, vy: 0, a: 1 }); }
      if (reduced && !tiles.length) tiles = [{ f: 0.3, cloud: false, y: 0, vy: 0, a: 1 }, { f: 0.5, cloud: true, y: ts * 0.9, vy: 0, a: 0.6 }, { f: 0.72, cloud: false, y: 0, vy: 0, a: 1 }];
      for (i = tiles.length - 1; i >= 0; i--) { var p = tiles[i];
        if (!reduced) { if (p.cloud && p.f >= 0.5) { p.vy += 500 * dt; p.y += p.vy * dt; p.a -= dt * 1.2; } else p.f += dt * 0.16; }
        if (p.a <= 0) { tiles.splice(i, 1); cnt[1]++; continue; } if (p.f > 0.9) { tiles.splice(i, 1); cnt[0]++; continue; }
        var x = X(p.f), y = chipY + p.y, w = ts * 0.75; c.globalAlpha = Math.max(p.a, 0);
        if (p.cloud) { c.fillStyle = '#cfd8dc'; c.fillRect(x - w / 2, y - w / 2, w, w); c.fillStyle = '#fff'; c.beginPath(); c.arc(x - w * 0.15, y, w * 0.25, 0, 6.2832); c.arc(x + w * 0.15, y - w * 0.05, w * 0.3, 0, 6.2832); c.fill();
          if (p.f >= 0.5) label(c, '✕', x, y, '#ff5252', w * 0.8); }
        else { c.fillStyle = '#1565c0'; c.fillRect(x - w / 2, y - w / 2, w, w); c.fillStyle = '#43a047'; c.beginPath(); c.ellipse(x - w * 0.1, y + w * 0.05, w * 0.3, w * 0.22, 0.4, 0, 6.2832); c.fill();
          if (p.f > 0.5) { c.strokeStyle = '#7dffc0'; c.lineWidth = 2; c.strokeRect(x - w / 2, y - w / 2, w, w); } }
        c.globalAlpha = 1; }
      var pulse = 0.5 + 0.5 * Math.sin(sc.t * 6), cg = c.createRadialGradient(chipX, chipY, 0, chipX, chipY, ts * 1.6); cg.addColorStop(0, 'rgba(190,170,255,' + (0.35 + 0.3 * pulse) + ')'); cg.addColorStop(1, 'rgba(190,170,255,0)');
      c.fillStyle = cg; c.fillRect(chipX - ts * 2, chipY - ts * 2, ts * 4, ts * 4);
      c.fillStyle = '#2a1f6e'; c.strokeStyle = '#d1c4ff'; c.lineWidth = 2; c.fillRect(chipX - ts * 0.6, chipY - ts * 0.6, ts * 1.2, ts * 1.2); c.strokeRect(chipX - ts * 0.6, chipY - ts * 0.6, ts * 1.2, ts * 1.2);
      for (var i = -2; i <= 2; i++) { c.fillStyle = '#d1c4ff'; c.fillRect(chipX + i * ts * 0.22 - 1.5, chipY - ts * 0.75, 3, ts * 0.15); c.fillRect(chipX + i * ts * 0.22 - 1.5, chipY + ts * 0.6, 3, ts * 0.15); }
      label(c, 'SI', chipX, chipY, '#fff', ts * 0.45); label(c, s('chip'), chipX, chipY - ts * 1.05, '#d1c4ff', fs * 0.9);
      label(c, '✓ ' + s('clear'), X(0.75), top * 0.12, '#7dffc0', fs * 0.9, 'center', W * 0.46); label(c, '✕ ' + s('cloudy'), X(0.3), top * 0.9, '#ff8a80', fs * 0.9, 'center', W * 0.5);
      // bottom: water use of US data centers (LBNL 2024) vs radiating heat in orbit
      c.fillStyle = 'rgba(255,255,255,.12)'; c.fillRect(0, top + 4, W, 1);
      var by = top + (H - top) * 0.58, mx = Math.max(by - top - fs * 2.2, 10), grow = reduced ? 1 : ease((sc.t % 10) / 3);
      function drop(cx, r, val, txt, col) { var rr = r * grow; c.fillStyle = col; c.beginPath(); c.moveTo(cx, by - rr * 2.4); c.bezierCurveTo(cx + rr * 1.2, by - rr * 0.9, cx + rr, by + rr, cx, by + rr); c.bezierCurveTo(cx - rr, by + rr, cx - rr * 1.2, by - rr * 0.9, cx, by - rr * 2.4); c.fill();
        label(c, val, cx, by + r + fs * 0.9, '#fff', fs * 0.95, 'center', W * 0.22); label(c, txt, cx, by + r + fs * 2.1, 'rgba(255,255,255,.85)', fs * 0.75); }
      var r66 = Math.min(mx / 3.4, W * 0.07), r21 = r66 * Math.sqrt(21 / 66); // area in proportion to volume
      label(c, s('waterh'), W / 2, top + fs * 1.1, '#9cd3ff', fs * 0.9, 'center', W * 0.94);
      drop(X(0.13), r21, s('w2014'), '2014', '#4fc3f7'); drop(X(0.37), r66, s('w2023'), '2023', '#0288d1');
      // radiator in orbit
      var rx = X(0.78), rw = W * 0.13, rh = Math.min(mx, H * 0.2), hot = 0.5 + 0.5 * Math.sin(sc.t * 3);
      c.fillStyle = 'rgba(255,140,60,' + (0.5 + 0.3 * hot) + ')'; c.fillRect(rx - rw / 2, by - rh * 0.8, rw, rh); c.strokeStyle = '#ffcc80'; c.strokeRect(rx - rw / 2, by - rh * 0.8, rw, rh);
      for (i = 0; i < 4; i++) { var wy = by - rh * 0.8 - 6 - ((sc.t * 20 + i * 9) % 30); c.strokeStyle = 'rgba(255,200,140,' + (1 - ((sc.t * 20 + i * 9) % 30) / 30) + ')'; c.beginPath();
        for (var k = 0; k <= 8; k++) c.lineTo(rx - rw / 2 + rw * k / 8, wy + Math.sin(k + sc.t * 4) * 2); c.stroke(); }
      label(c, s('heat'), rx, by + rh * 0.2 + fs * 0.9, '#ffcc80', fs * 0.8, 'center', W * 0.4); label(c, s('nowater'), rx, by + rh * 0.2 + fs * 2.1, 'rgba(255,255,255,.85)', fs * 0.75, 'center', W * 0.4);
      void dir;
    }); }

  /* ---------- pause control ---------- */
  var pb = document.getElementById('sx-pause');
  if (pb) { if (reduced) pb.hidden = true; pb.addEventListener('click', function () { paused = !paused; pb.setAttribute('aria-pressed', paused ? 'true' : 'false');
    var lab = pb.querySelector('.lab'); if (lab) lab.textContent = paused ? s('play') : s('pause'); var em = pb.querySelector('.em'); if (em) em.textContent = paused ? '▶️' : '⏸️'; kick(); }); }
  document.addEventListener('visibilitychange', function () { if (!document.hidden) kick(); });
  kick();
})();
