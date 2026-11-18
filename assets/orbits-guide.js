/* Orbit sandbox for the Orbits Guide. Earth is a NASA Blue Marble disc.
   Two-body motion uses μ = 398600.4418 km³/s² and R_E = 6378.137 km. */
(function () {
  if (typeof document === 'undefined') return;
  var app = document.getElementById('og-app');
  var c = document.getElementById('og-c');
  if (!app || !c) return;
  var ui = {};
  try { ui = JSON.parse(app.getAttribute('data-ui') || '{}'); } catch (e) { ui = {}; }
  var MU = 398600.4418, RE = 6378.137, R0 = RE + 300;
  var g = c.getContext('2d');
  var mode = 'cannon';
  var speed = 7.73;
  var alt = 35786;
  var playing = false;
  var playT = 0;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pre = /\/(fr|es|ar|it|he)\//.test(location.pathname) ? '../' : '';
  var earth = new Image();
  earth.decoding = 'async';
  if ('fetchPriority' in earth) earth.fetchPriority = 'low';
  earth.onload = function () { draw(); };
  earth.src = pre + 'assets/earth/blue-marble-disc.webp';
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var fmt = new Intl.NumberFormat(lang === 'en' ? 'en' : lang, { maximumFractionDigits: 2, minimumFractionDigits: 0 });
  function n(x, d) {
    return new Intl.NumberFormat(lang === 'en' ? 'en' : lang, { maximumFractionDigits: d, minimumFractionDigits: d }).format(x);
  }
  function t(k, fallback) { return ui[k] || fallback || k; }

  function accel(x, y) {
    var r2 = x * x + y * y;
    var r = Math.sqrt(r2);
    var k = -MU / (r2 * r);
    return [k * x, k * y];
  }
  function deriv(s) {
    var a = accel(s[0], s[1]);
    return [s[2], s[3], a[0], a[1]];
  }
  function add(s, k, h) {
    return [s[0] + h * k[0], s[1] + h * k[1], s[2] + h * k[2], s[3] + h * k[3]];
  }
  function rk4(s, dt) {
    var k1 = deriv(s);
    var k2 = deriv(add(s, k1, dt / 2));
    var k3 = deriv(add(s, k2, dt / 2));
    var k4 = deriv(add(s, k3, dt));
    return [
      s[0] + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
      s[1] + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]),
      s[2] + dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]),
      s[3] + dt / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
    ];
  }
  var pathCache = {};
  function pathFor(v) {
    var key = v.toFixed(2);
    if (pathCache[key]) return pathCache[key];
    var s = [R0, 0, 0, v];
    var dt = 15;
    var pts = [[s[0], s[1]]];
    var hit = false;
    var esc = Math.sqrt(2 * MU / R0);
    var circ = Math.sqrt(MU / R0);
    for (var i = 0; i < 6000; i++) {
      s = rk4(s, dt);
      var r = Math.hypot(s[0], s[1]);
      if (i % 2 === 0) pts.push([s[0], s[1]]);
      if (r < RE) { hit = true; break; }
      if (r > R0 * 6) break;
      if (i > 80 && Math.hypot(s[0] - R0, s[1]) < 40 && s[3] > 0 && s[0] > 0) break;
    }
    var kind = 'ellipse';
    if (v + 0.02 >= esc) kind = 'leave';
    else if (Math.abs(v - circ) < 0.08) kind = 'circle';
    else if (hit) kind = 'fall';
    var out = { pts: pts, kind: kind, circ: circ, esc: esc };
    pathCache[key] = out;
    return out;
  }

  function keplerNu(M, e) {
    var E = M;
    for (var i = 0; i < 12; i++) E = E - (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
    var nu = 2 * Math.atan2(Math.sqrt(1 + e) * Math.sin(E / 2), Math.sqrt(1 - e) * Math.cos(E / 2));
    return nu;
  }
  function sector(a, e, M0, M1, steps) {
    var pts = [[0, 0]];
    for (var i = 0; i <= steps; i++) {
      var M = M0 + (M1 - M0) * i / steps;
      var nu = keplerNu(M, e);
      var r = a * (1 - e * e) / (1 + e * Math.cos(nu));
      pts.push([r * Math.cos(nu), r * Math.sin(nu)]);
    }
    return pts;
  }

  function hohmann(h2) {
    var r1 = R0, r2 = RE + h2, at = (r1 + r2) / 2;
    var vc1 = Math.sqrt(MU / r1);
    var vp = Math.sqrt(MU * (2 / r1 - 1 / at));
    var va = Math.sqrt(MU * (2 / r2 - 1 / at));
    var vc2 = Math.sqrt(MU / r2);
    var tof = Math.PI * Math.sqrt(at * at * at / MU) / 3600;
    return { r1: r1, r2: r2, dv1: vp - vc1, dv2: vc2 - va, tof: tof, vc1: vc1, vc2: vc2 };
  }

  function resize() {
    var w = c.clientWidth || 640;
    var h = Math.round(w * 0.62);
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    c.width = Math.round(w * dpr);
    c.height = Math.round(h * dpr);
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }

  function disc(cx, cy, rad) {
    g.save();
    g.beginPath();
    g.arc(cx, cy, rad, 0, Math.PI * 2);
    g.clip();
    if (earth.complete && earth.naturalWidth) g.drawImage(earth, cx - rad, cy - rad, rad * 2, rad * 2);
    else { g.fillStyle = '#16324f'; g.fill(); }
    g.restore();
    g.beginPath();
    g.arc(cx, cy, rad, 0, Math.PI * 2);
    g.strokeStyle = 'rgba(255,255,255,.35)';
    g.lineWidth = 1;
    g.stroke();
  }

  function poly(pts, cx, cy, scale) {
    g.beginPath();
    for (var i = 0; i < pts.length; i++) {
      var x = cx + pts[i][0] * scale, y = cy - pts[i][1] * scale;
      if (i === 0) g.moveTo(x, y); else g.lineTo(x, y);
    }
  }

  function draw() {
    var w = c.clientWidth || 640, h = (c.height / (c.width || 1)) * w;
    g.clearRect(0, 0, w, h);
    g.fillStyle = '#071018';
    g.fillRect(0, 0, w, h);
    var cx = w * 0.5, cy = h * 0.52;
    var read = '';
    if (mode === 'cannon') {
      var path = pathFor(speed);
      var maxR = R0 * 1.35;
      for (var i = 0; i < path.pts.length; i++) maxR = Math.max(maxR, Math.hypot(path.pts[i][0], path.pts[i][1]));
      maxR = Math.min(Math.max(maxR * 1.08, R0 * 1.35), R0 * 3.2);
      var scale = Math.min(w, h) * 0.46 / maxR;
      disc(cx, cy, RE * scale);
      g.beginPath();
      for (i = 0; i < path.pts.length; i++) {
        var x = cx + path.pts[i][0] * scale, y = cy - path.pts[i][1] * scale;
        if (i === 0) g.moveTo(x, y); else g.lineTo(x, y);
      }
      g.strokeStyle = '#ffd54a';
      g.lineWidth = 2;
      g.stroke();
      var dot = path.pts[Math.min(path.pts.length - 1, Math.floor(playT * path.pts.length))];
      g.fillStyle = '#fff';
      g.beginPath();
      g.arc(cx + dot[0] * scale, cy - dot[1] * scale, 4, 0, Math.PI * 2);
      g.fill();
      var labels = { fall: t('fall'), circle: t('circle'), ellipse: t('ellipse'), leave: t('leave') };
      read = n(speed, 2) + ' km/s · ' + (labels[path.kind] || path.kind) + ' · ' + t('circ') + ' ' + n(path.circ, 2) + ' km/s · ' + t('esc') + ' ' + n(path.esc, 2) + ' km/s';
    } else if (mode === 'area') {
      var a = 16000, e = 0.55;
      var scaleA = Math.min(w, h) * 0.42 / (a * (1 + e));
      disc(cx, cy, RE * scaleA);
      g.beginPath();
      for (var k = 0; k <= 180; k++) {
        var nu = -Math.PI + 2 * Math.PI * k / 180;
        var r = a * (1 - e * e) / (1 + e * Math.cos(nu));
        var x = cx + r * Math.cos(nu) * scaleA, y = cy - r * Math.sin(nu) * scaleA;
        if (k === 0) g.moveTo(x, y); else g.lineTo(x, y);
      }
      g.closePath();
      g.strokeStyle = '#8fd3ff';
      g.lineWidth = 1.5;
      g.stroke();
      var dM = 0.45;
      var wedges = [[-dM, dM, 'rgba(255,213,74,.55)'], [Math.PI - dM, Math.PI + dM, 'rgba(124,252,152,.45)']];
      for (var wj = 0; wj < wedges.length; wj++) {
        var sec = sector(a, e, wedges[wj][0], wedges[wj][1], 16);
        poly(sec, cx, cy, scaleA);
        g.closePath();
        g.fillStyle = wedges[wj][2];
        g.fill();
      }
      read = t('areaRead');
    } else {
      var H = hohmann(alt);
      var scaleH = Math.min(w, h) * 0.44 / H.r2;
      disc(cx, cy, RE * scaleH);
      g.strokeStyle = 'rgba(143,211,255,.8)';
      g.lineWidth = 1.5;
      g.beginPath(); g.arc(cx, cy, H.r1 * scaleH, 0, Math.PI * 2); g.stroke();
      g.beginPath(); g.arc(cx, cy, H.r2 * scaleH, 0, Math.PI * 2); g.stroke();
      var at = (H.r1 + H.r2) / 2, cE = at - H.r1;
      g.beginPath();
      g.ellipse(cx - cE * scaleH, cy, at * scaleH, Math.sqrt(Math.max(0, at * at - cE * cE)) * scaleH, 0, 0, Math.PI, true);
      g.strokeStyle = '#ffd54a';
      g.lineWidth = 2;
      g.stroke();
      read = 'Δv₁ ' + n(H.dv1, 2) + ' km/s · Δv₂ ' + n(H.dv2, 2) + ' km/s · Δv ' + n(H.dv1 + H.dv2, 2) + ' km/s · ' + n(H.tof, 2) + ' h';
    }
    var live = document.getElementById('og-read');
    if (live) live.textContent = read;
  }

  function showMode(next) {
    mode = next;
    app.querySelectorAll('[data-mode]').forEach(function (b) {
      var on = b.getAttribute('data-mode') === mode;
      b.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    app.querySelectorAll('[data-for]').forEach(function (p) {
      p.hidden = p.getAttribute('data-for') !== mode;
    });
    draw();
  }

  app.addEventListener('click', function (ev) {
    var b = ev.target.closest('button');
    if (!b) return;
    if (b.hasAttribute('data-mode')) showMode(b.getAttribute('data-mode'));
    if (b.hasAttribute('data-v')) {
      speed = parseFloat(b.getAttribute('data-v'));
      var slider = document.getElementById('og-v');
      if (slider) slider.value = String(speed);
      draw();
    }
    if (b.id === 'og-play') {
      playing = !playing;
      b.setAttribute('aria-pressed', playing ? 'true' : 'false');
      b.textContent = playing ? t('pause', 'Pause') : t('play', 'Play');
      if (playing) tick();
    }
  });
  var vEl = document.getElementById('og-v');
  if (vEl) vEl.addEventListener('input', function () { speed = parseFloat(vEl.value); draw(); });
  var hEl = document.getElementById('og-h');
  if (hEl) hEl.addEventListener('input', function () { alt = parseFloat(hEl.value); draw(); });

  function tick() {
    if (!playing) return;
    playT += 0.004;
    if (playT > 1) playT = 0;
    draw();
    requestAnimationFrame(tick);
  }

  var tabs = document.querySelectorAll('.og-tabs button');
  tabs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('aria-controls');
      tabs.forEach(function (o) { o.setAttribute('aria-selected', o === btn ? 'true' : 'false'); });
      document.querySelectorAll('.og-panel').forEach(function (p) { p.classList.toggle('is-on', p.id === id); });
    });
  });
  document.documentElement.classList.add('og-ready');

  if (reduce) {
    var play = document.getElementById('og-play');
    if (play) play.hidden = true;
  }
  window.addEventListener('resize', resize);
  showMode('cannon');
  resize();

  document.querySelectorAll('.ytf').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var key = btn.getAttribute('data-yt');
      var frame = document.createElement('iframe');
      if (key === '-luKN6mad5w') {
        frame.src = 'https://www.youtube-nocookie.com/embed/-luKN6mad5w?autoplay=1';
        frame.title = "STEMonstrations: Newton's First Law of Motion";
      } else if (key === 'NpHOlmNtFTQ') {
        frame.src = 'https://www.youtube-nocookie.com/embed/NpHOlmNtFTQ?autoplay=1';
        frame.title = 'Real World: Keeping the International Space Station in Orbit';
      } else if (key === 'KTaIPz6oC9U') {
        frame.src = 'https://www.youtube-nocookie.com/embed/KTaIPz6oC9U?autoplay=1';
        frame.title = "7. Kepler's Laws";
      } else if (key === 'gXS0nXgSXJc') {
        frame.src = 'https://www.youtube-nocookie.com/embed/gXS0nXgSXJc?autoplay=1';
        frame.title = 'Cheops observing in space';
      } else if (key === 'zT7typHkpVg') {
        frame.src = 'https://www.youtube-nocookie.com/embed/zT7typHkpVg?autoplay=1';
        frame.title = 'Space debris — a journey to Earth';
      } else if (key === '9XcJ1wFRCk8') {
        frame.src = 'https://www.youtube-nocookie.com/embed/9XcJ1wFRCk8?autoplay=1';
        frame.title = 'Gaia: launch to orbit';
      } else if (key === 'SJI-SAs1Rnk') {
        frame.src = 'https://www.youtube-nocookie.com/embed/SJI-SAs1Rnk?autoplay=1';
        frame.title = 'A Funny Thing Happened on the Way to the Moon';
      } else return;
      frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      frame.allowFullscreen = true;
      frame.width = 560;
      frame.height = 315;
      var box = btn.parentNode;
      box.replaceChild(frame, btn);
    });
  });
})();
