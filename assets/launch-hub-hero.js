/* Upcoming Launches hub hero: rocket arc to orbit over a rotating Earth + star field.
   Canvas 2D only (no WebGL). Pauses on prefers-reduced-motion / offscreen / Pause control.
   No external assets or network. */
(function () {
  var root = document.getElementById('ul-hero');
  if (!root) return;
  var canvas = root.querySelector('canvas.ul-hero-canvas');
  var btn = root.querySelector('.ul-hero-pause');
  if (!canvas) return;
  var ctx = canvas.getContext('2d', { alpha: false });
  if (!ctx) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var paused = reduce;
  var running = false;
  var raf = 0;
  var t0 = performance.now();
  var stars = [];
  var sats = [];
  var dpr = 1;
  var W = 0, H = 0;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var r = root.getBoundingClientRect();
    W = Math.max(320, Math.floor(r.width));
    H = Math.max(220, Math.floor(r.height));
    canvas.width = Math.floor(W * dpr);
    canvas.height = Math.floor(H * dpr);
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed();
  }

  function seed() {
    stars = [];
    var n = Math.min(140, Math.floor((W * H) / 4500));
    for (var i = 0; i < n; i++) {
      stars.push({ x: Math.random() * W, y: Math.random() * H, r: Math.random() * 1.4 + 0.3, a: Math.random() * 0.7 + 0.25 });
    }
    sats = [];
    for (var j = 0; j < 7; j++) {
      sats.push({ a: Math.random() * Math.PI * 2, r: 0.42 + Math.random() * 0.28, s: 0.15 + Math.random() * 0.25 });
    }
  }

  function draw(now) {
    var t = (now - t0) / 1000;
    ctx.fillStyle = '#050b18';
    ctx.fillRect(0, 0, W, H);

    // soft nebula
    var g = ctx.createRadialGradient(W * 0.7, H * 0.25, 10, W * 0.7, H * 0.25, W * 0.55);
    g.addColorStop(0, 'rgba(40,80,160,0.35)');
    g.addColorStop(1, 'rgba(5,11,24,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    for (var i = 0; i < stars.length; i++) {
      var s = stars[i];
      ctx.globalAlpha = s.a * (0.75 + 0.25 * Math.sin(t * 1.3 + i));
      ctx.fillStyle = '#e8f1ff';
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    var cx = W * 0.38, cy = H * 0.62, R = Math.min(W, H) * 0.28;
    var spin = reduce ? 0.4 : t * 0.22;

    // Earth
    var eg = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.35, R * 0.1, cx, cy, R);
    eg.addColorStop(0, '#5ec8ff');
    eg.addColorStop(0.45, '#1a7fbf');
    eg.addColorStop(1, '#0a3a62');
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.fillStyle = eg;
    ctx.fill();

    // simple continent bands (rotating)
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.clip();
    ctx.translate(cx, cy);
    ctx.rotate(spin);
    ctx.fillStyle = 'rgba(46,140,70,0.55)';
    for (var k = -2; k <= 2; k++) {
      ctx.beginPath();
      ctx.ellipse(k * R * 0.55, Math.sin(k) * R * 0.2, R * 0.28, R * 0.14, k * 0.4, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.fillStyle = 'rgba(255,255,255,0.55)';
    ctx.beginPath();
    ctx.ellipse(0, -R * 0.78, R * 0.35, R * 0.14, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(0, R * 0.82, R * 0.4, R * 0.12, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // atmosphere rim
    ctx.strokeStyle = 'rgba(143,211,255,0.55)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, R + 1.5, 0, Math.PI * 2);
    ctx.stroke();

    // satellites
    for (var j = 0; j < sats.length; j++) {
      var sat = sats[j];
      var ang = sat.a + t * sat.s;
      var sx = cx + Math.cos(ang) * R * (1.25 + sat.r * 0.35);
      var sy = cy + Math.sin(ang) * R * (0.55 + sat.r * 0.2);
      ctx.fillStyle = '#ffd166';
      ctx.fillRect(sx - 2, sy - 2, 4, 4);
      ctx.strokeStyle = 'rgba(255,209,102,0.35)';
      ctx.beginPath();
      ctx.moveTo(sx - 6, sy);
      ctx.lineTo(sx + 6, sy);
      ctx.stroke();
    }

    // rocket arc (bezier from ground to orbit)
    var prog = reduce ? 0.72 : ((t * 0.12) % 1.15);
    if (prog > 1) prog = 1;
    var p0x = cx - R * 0.15, p0y = cy + R * 0.95;
    var p1x = cx + R * 0.9, p1y = cy - R * 0.1;
    var p2x = cx + R * 1.55, p2y = cy - R * 1.05;
    function bez(u) {
      var u1 = 1 - u;
      return {
        x: u1 * u1 * p0x + 2 * u1 * u * p1x + u * u * p2x,
        y: u1 * u1 * p0y + 2 * u1 * u * p1y + u * u * p2y
      };
    }
    ctx.strokeStyle = 'rgba(143,211,255,0.45)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 6]);
    ctx.beginPath();
    for (var u = 0; u <= prog; u += 0.02) {
      var pt = bez(u);
      if (u === 0) ctx.moveTo(pt.x, pt.y); else ctx.lineTo(pt.x, pt.y);
    }
    ctx.stroke();
    ctx.setLineDash([]);

    var rk = bez(Math.min(prog, 1));
    var rk2 = bez(Math.max(0, Math.min(prog, 1) - 0.02));
    var angR = Math.atan2(rk.y - rk2.y, rk.x - rk2.x);
    ctx.save();
    ctx.translate(rk.x, rk.y);
    ctx.rotate(angR);
    // body
    ctx.fillStyle = '#f4f7fb';
    ctx.fillRect(-10, -3, 18, 6);
    ctx.fillStyle = '#009cde';
    ctx.beginPath();
    ctx.moveTo(8, 0);
    ctx.lineTo(14, -4);
    ctx.lineTo(14, 4);
    ctx.closePath();
    ctx.fill();
    // flame
    if (!reduce && prog < 1) {
      var flick = 0.7 + 0.3 * Math.sin(t * 30);
      ctx.fillStyle = 'rgba(255,160,40,' + flick + ')';
      ctx.beginPath();
      ctx.moveTo(-10, -2);
      ctx.lineTo(-18 - 4 * flick, 0);
      ctx.lineTo(-10, 2);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();

    // vignette for title contrast
    var vg = ctx.createLinearGradient(0, 0, 0, H);
    vg.addColorStop(0, 'rgba(5,11,24,0.55)');
    vg.addColorStop(0.45, 'rgba(5,11,24,0.15)');
    vg.addColorStop(1, 'rgba(5,11,24,0.65)');
    ctx.fillStyle = vg;
    ctx.fillRect(0, 0, W, H);
  }

  function frame(now) {
    if (!running) return;
    draw(now);
    if (!paused) raf = requestAnimationFrame(frame);
  }

  function start() {
    if (running) return;
    running = true;
    if (!paused) raf = requestAnimationFrame(frame);
    else draw(performance.now());
  }
  function stop() {
    running = false;
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
  }

  function setPaused(p) {
    paused = p || reduce;
    if (btn) {
      btn.setAttribute('aria-pressed', paused ? 'true' : 'false');
      btn.textContent = paused ? (btn.getAttribute('data-play') || 'Play') : (btn.getAttribute('data-pause') || 'Pause');
    }
    if (!paused && running) raf = requestAnimationFrame(frame);
    else if (paused) draw(performance.now());
  }

  if (btn) {
    if (reduce) { btn.hidden = true; }
    btn.addEventListener('click', function () { setPaused(!paused); });
  }

  resize();
  draw(performance.now());
  start();
  window.addEventListener('resize', function () {
    resize();
    draw(performance.now());
  }, { passive: true });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (ents) {
      if (ents[0].isIntersecting) start(); else stop();
    }, { threshold: 0.05 });
    io.observe(root);
  }
})();
