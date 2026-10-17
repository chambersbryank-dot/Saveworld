/* Homepage hero themes (Oct 16 2026). Generated alongside scripts/build-hero-themes.py; the theme is chosen inline in the
   hero (weekly rotation, ?hero=<name> override) and this file renders the procedural ones. No libraries, no network.
   Theme "space": layered starfield with depth parallax and twinkle, drifting nebula + galaxy band, shooting stars and a
   distant ocean planet with rim light. Sized by devicePixelRatio (capped by pixel budget). Pauses when the tab is hidden
   or the hero is offscreen; a single static frame under prefers-reduced-motion. */
(function () {
  'use strict';
  var hero = document.querySelector('.hero[data-hero]');
  if (!hero || hero.getAttribute('data-hero') !== 'space') return;
  var box = hero.querySelector('.hero-space');
  if (!box || !window.HTMLCanvasElement) return;
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var reduced = mq.matches;

  // Seeded PRNG so the sky is the same every visit (and for everyone).
  var seed = 0x5a1e42;
  function rnd() { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }

  function mk(cls) { var c = document.createElement('canvas'); c.className = 'hs-layer ' + cls; box.appendChild(c); return c; }
  var cNeb = mk('hs-neb'), cFar = mk('hs-far'), cMid = mk('hs-mid'), cFx = mk('hs-fx');

  var W = 0, H = 0, D = 1, M = 0.06; // CSS size, device scale, parallax margin (fraction)
  var bright = [], shoot = [], nextShoot = 0, sprites = {};

  // ---------- value noise / fbm for the nebula ----------
  var P = new Uint8Array(512); (function () { var p = []; for (var i = 0; i < 256; i++) p[i] = i;
    for (i = 255; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)), t = p[i]; p[i] = p[j]; p[j] = t; }
    for (i = 0; i < 512; i++) P[i] = p[i & 255]; })();
  function fade(t) { return t * t * (3 - 2 * t); }
  function vn(x, y) { var xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi; xi &= 255; yi &= 255;
    var a = P[P[xi] + yi] / 255, b = P[P[xi + 1] + yi] / 255, c = P[P[xi] + yi + 1] / 255, d = P[P[xi + 1] + yi + 1] / 255;
    var u = fade(xf), v = fade(yf); return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v; }
  function fbm(x, y) { var s = 0, a = 0.5; for (var o = 0; o < 5; o++) { s += a * vn(x, y); x = x * 2.03 + 17.1; y = y * 2.01 + 9.7; a *= 0.5; } return s; }

  function fbm6(x, y) { var s = 0, a = 0.5; for (var o = 0; o < 6; o++) { s += a * vn(x, y); x = x * 2.03 + 17.1; y = y * 2.01 + 9.7; a *= 0.5; } return s; }
  // Fill an ImageData in small row slices between frames so the page never janks; tok cancels on resize.
  var tok = 0;
  function chunked(w, h, px, done) { var my = tok, img = new ImageData(w, h), j = 0;
    (function step() { if (my !== tok) return; var t = performance.now();
      while (j < h && performance.now() - t < 6) { for (var i = 0; i < w; i++) px(img.data, (j * w + i) * 4, i, j); j++; }
      if (j < h) setTimeout(step, 0); else done(img); })(); }
  function bandC(u) { return W > H ? 0.12 + u * 0.7 : 0.3 + u * 0.38; }
  function sstep(a, b, x) { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); }
  function nebula() {
    // Low-res procedural nebula (soft by nature), upscaled with smoothing; drawn once per resize.
    var nw = W * D > 1600 ? 560 : 440, nh = Math.max(220, Math.round(nw * H / Math.max(W, 1))), asp = nh / nw;
    chunked(nw, nh, function (d, k, i, j) {
      var u = i / nw, v = j / nh, sc = W > H ? 3.6 : 3.0, sx = u * sc + (W > H ? 1.3 : 0), sy = v * sc * asp;
      var q = fbm(sx + 1.7, sy + 9.2), r = fbm(sx + 3.6 * q + 8.3, sy + 3.6 * q + 2.8);   // domain warp -> wisps
      var bc = bandC(u);                                                                    // diagonal galaxy band
      var band = Math.exp(-Math.pow((v - bc) * (W > H ? 2.6 : 4.2), 2));
      var dens = sstep(0.33, 0.84, r) * (0.5 + 0.95 * band);
      var w = sstep(0.3, 0.75, fbm(sx * 0.7 + 21, sy * 0.7 + 5));                          // colour region
      var dust = sstep(0.5, 0.72, fbm(sx * 2.4 + 3, sy * 2.4 + 7)) * band * 0.8;           // dark lanes in the band
      var core = Math.pow(dens, 3.2), edge = dens * (1 - dens) * 4 * sstep(0.55, 0.9, w);  // coral only on some cloud edges
      // palette: navy base, brand blue/cyan clouds, violet regions, coral rims, cyan-white cores
      dens = Math.min(1, dens * 1.15);
      var R = 2 + dens * (6 * (1 - w) + 120 * w) + edge * 150 + core * 110 + band * 16,
          G = 8 + dens * (128 * (1 - w) + 48 * w) + edge * 40 + core * 190 + band * 24,
          B = 22 + dens * (222 * (1 - w) + 210 * w) + edge * 95 + core * 255 + band * 46;
      var dk = 1 - dust;
      d[k] = R * dk; d[k + 1] = G * dk; d[k + 2] = B * dk; d[k + 3] = 255;
    }, function (img) { cNeb.width = nw; cNeb.height = nh; cNeb.getContext('2d').putImageData(img, 0, 0); box.classList.add('hs-ready'); });
  }

  var pTex = null;
  function planetPx(T) {
    var Lx = -0.62, Ly = -0.55, Lz = 0.56;
    return function (d, o, i, j) {
      var nx = (i + 0.5) / T * 2 - 1, ny = (j + 0.5) / T * 2 - 1, rr = nx * nx + ny * ny;
      if (rr > 1) { d[o + 3] = 0; return; }
      var nz = Math.sqrt(1 - rr), lon = Math.atan2(nx, nz) * 1.6, lat = Math.asin(ny) * 1.6;
      var ln = fbm6(lon + 30, lat + 11), land = sstep(0.56, 0.6, ln), hi = sstep(0.6, 0.75, ln), tone = vn(lon * 6 + 3, lat * 6 + 1);
      var cl = sstep(0.48, 0.8, fbm6(lon * 2.2 + 50 + lat * 0.6, lat * 3.6 + 4)) * 0.95;
      var dif = Math.max(0, nx * Lx + ny * Ly + nz * Lz), lit = sstep(-0.04, 0.32, dif) * (0.22 + 0.78 * dif);
      var rim = Math.pow(1 - nz, 2.4), sh = 0.55 + 0.45 * sstep(0.2, 0.7, ln + (1 - land));    // ocean depth shading
      var oR = 4 + 10 * sh, oG = 34 + 52 * sh, oB = 92 + 70 * sh;                                   // deep blue -> brand-blue shallows
      var gR = 28 + 60 * hi + 30 * tone, gG = 82 + 30 * tone - 10 * hi, gB = 62 - 20 * hi;          // muted greens/tans
      var R = (oR * (1 - land) + gR * land) * (1 - cl) + 236 * cl, G = (oG * (1 - land) + gG * land) * (1 - cl) + 243 * cl, B = (oB * (1 - land) + gB * land) * (1 - cl) + 255 * cl;
      var spec = Math.pow(Math.max(0, 2 * dif * nz - Lz), 28) * (1 - land) * (1 - cl) * 0.75;
      d[o] = R * lit + 255 * spec + rim * 25 * lit; d[o + 1] = G * lit + 250 * spec + rim * 150 * (lit + 0.12); d[o + 2] = B * lit + 245 * spec + rim * 235 * (lit + 0.12); d[o + 3] = 255;
    };
  }
  function toCanvas(img) { var c = document.createElement('canvas'); c.width = img.width; c.height = img.height; c.getContext('2d').putImageData(img, 0, 0); return c; }
  function planetTex() { var T = 160, img = new ImageData(T, T), px = planetPx(T);
    for (var j = 0; j < T; j++) for (var i = 0; i < T; i++) px(img.data, (j * T + i) * 4, i, j); return toCanvas(img); }

  function sprite(r, rgb, spikes) {
    var key = r + rgb + spikes; if (sprites[key]) return sprites[key];
    var s = Math.ceil(r * (spikes ? 9 : 4)) * 2 + 2, c = document.createElement('canvas'); c.width = c.height = s;
    var x = c.getContext('2d'), m = s / 2, g = x.createRadialGradient(m, m, 0, m, m, r * 4);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.18, 'rgba(' + rgb + ',0.9)');
    g.addColorStop(0.45, 'rgba(' + rgb + ',0.22)'); g.addColorStop(1, 'rgba(' + rgb + ',0)');
    x.fillStyle = g; x.beginPath(); x.arc(m, m, r * 4, 0, 7); x.fill();
    if (spikes) { x.globalCompositeOperation = 'lighter';
      [[1, 0], [0, 1]].forEach(function (a) { var lg = x.createLinearGradient(m - a[0] * m, m - a[1] * m, m + a[0] * m, m + a[1] * m);
        lg.addColorStop(0, 'rgba(' + rgb + ',0)'); lg.addColorStop(0.5, 'rgba(255,255,255,0.85)'); lg.addColorStop(1, 'rgba(' + rgb + ',0)');
        x.fillStyle = lg; if (a[0]) x.fillRect(0, m - r * 0.22, s, r * 0.44); else x.fillRect(m - r * 0.22, 0, r * 0.44, s); }); }
    return (sprites[key] = c);
  }
  var TINTS = ['205,225,255', '255,244,232', '170,215,255', '255,214,200', '230,236,255'];

  function stars(c, n, rMin, rMax, alpha, avoid) {
    var cw = W * (1 + 2 * M), ch = H * (1 + 2 * M); c.width = Math.round(cw * D); c.height = Math.round(ch * D);
    c.style.width = cw + 'px'; c.style.height = ch + 'px'; c.style.left = (-W * M) + 'px'; c.style.top = (-H * M) + 'px';
    var x = c.getContext('2d'); x.setTransform(D, 0, 0, D, 0, 0); x.globalCompositeOperation = 'lighter';
    for (var i = 0; i < n; i++) {
      var u = rnd(), v = rnd();
      if (rnd() < 0.45) v = Math.min(1, Math.max(0, bandC(u) + (rnd() + rnd() + rnd() - 1.5) * 0.14)); // denser along the band
      if (avoid && inPlanet(u * cw, v * ch, 6)) continue;
      var r = rMin + Math.pow(rnd(), 3) * (rMax - rMin), sp = sprite(Math.max(0.35, r), TINTS[(rnd() * 5) | 0], false);
      x.globalAlpha = alpha * (0.35 + 0.65 * rnd()); var s = sp.width / D * (r < 0.6 ? 0.8 : 1);
      x.drawImage(sp, u * cw - s / 2, v * ch - s / 2, s, s);
    }
    return x;
  }

  var PL = { cx: 0, cy: 0, R: 0 };  // planet geometry in layer coordinates (layers are offset by -W*M, -H*M)
  function pgeo() { var cw = W * (1 + 2 * M), ch = H * (1 + 2 * M), big = Math.max(W, H);
    PL.R = Math.max(150, big * (W < 900 ? 0.34 : 0.29)); PL.cx = cw * (W < 900 ? 0.97 : 0.92); PL.cy = ch * (W < 900 ? 1.0 : 0.97); }
  function inPlanet(x, y, pad) { var dx = x - PL.cx, dy = y - PL.cy; return dx * dx + dy * dy < Math.pow(PL.R + pad, 2); }
  function planet(x, cw, ch) {
    // Distant ocean world, lower right, partly off-frame, lit from the upper left; crisp limb drawn at full resolution.
    var cx = PL.cx, cy = PL.cy, R = PL.R, lx = -0.74, ly = -0.67;
    var halo = x.createRadialGradient(cx, cy, R * 0.97, cx, cy, R * 1.22);
    halo.addColorStop(0, 'rgba(60,180,240,0.45)'); halo.addColorStop(0.3, 'rgba(0,156,222,0.16)'); halo.addColorStop(1, 'rgba(0,156,222,0)');
    x.globalCompositeOperation = 'source-over'; x.globalAlpha = 1;
    x.fillStyle = halo; x.beginPath(); x.arc(cx, cy, R * 1.25, 0, 7); x.fill();
    if (!pTex) pTex = planetTex();
    x.save(); x.beginPath(); x.arc(cx, cy, R, 0, 7); x.clip(); x.fillStyle = '#01040a'; x.fill();
    x.imageSmoothingQuality = 'high'; x.drawImage(pTex, cx - R, cy - R, 2 * R, 2 * R); x.restore();
    x.save(); x.globalCompositeOperation = 'lighter'; x.lineCap = 'round'; var a0 = Math.atan2(ly, lx);
    for (var w = 0; w < 3; w++) { x.beginPath(); x.arc(cx, cy, R - 0.6 - w * 0.8, a0 - 1.15 + w * 0.12, a0 + 1.15 - w * 0.12);
      x.strokeStyle = ['rgba(190,240,255,0.9)', 'rgba(60,190,250,0.5)', 'rgba(0,156,222,0.25)'][w]; x.lineWidth = [1.4, 3.5, 9][w];
      x.shadowColor = 'rgba(0,156,222,0.9)'; x.shadowBlur = [4, 14, 28][w]; x.stroke(); }
    x.restore();
  }

  function far() { var area = W * H / 1e6; seed = 0x5a1e42;
    planet(stars(cFar, Math.round(1300 * area + 450), 0.3, 0.9, 0.8), W * (1 + 2 * M), H * (1 + 2 * M)); }
  function setup() {
    var r = hero.getBoundingClientRect(); W = Math.max(320, Math.round(r.width)); H = Math.max(480, Math.round(r.height));
    var dpr = Math.min(window.devicePixelRatio || 1, 3), budget = 8.3e6; // ~4K worth of pixels per layer
    D = Math.min(dpr, Math.sqrt(budget / (W * (1 + 2 * M) * H * (1 + 2 * M))));
    tok++; sprites = {}; pTex = null;
    var area = W * H / 1e6;
    pgeo(); far();
    var T = Math.min(900, Math.round(2 * PL.R * D)); // hi-res planet texture once idle (about 1 texel per device pixel)
    chunked(T, T, planetPx(T), function (img) { pTex = toCanvas(img); far(); });
    seed = 0x77e1;
    stars(cMid, Math.round(280 * area + 100), 0.6, 1.5, 0.95, true);
    seed = 0x2b9d;
    cFx.width = Math.round(W * D); cFx.height = Math.round(H * D); cFx.style.width = W + 'px'; cFx.style.height = H + 'px';
    bright = [];
    var nb = Math.round(70 * area + 30);
    for (var i = 0; i < nb; i++) { var big = rnd() < 0.12, bx = rnd() * W, by = rnd() * H;
      if (inPlanet(bx + W * M, by + H * M, 30)) continue;
      bright.push({ x: bx, y: by, r: big ? 1.3 + rnd() * 1.1 : 0.7 + rnd() * 0.8, sp: big,
        c: TINTS[(rnd() * 5) | 0], ph: rnd() * 6.283, f: 0.35 + rnd() * 1.1, z: 0.6 + rnd() * 0.4 }); }
    bright.forEach(function (s) { s.img = sprite(s.r, s.c, s.sp); });
    nebula(); // fills in over the next frames and fades in (stars and planet show at once)
  }

  var px = 0, py = 0, tx = 0, ty = 0; // pointer parallax (desktop), eased
  hero.addEventListener('pointermove', function (e) { if (e.pointerType !== 'mouse') return;
    var r = hero.getBoundingClientRect(); tx = (e.clientX - r.left) / r.width - 0.5; ty = (e.clientY - r.top) / r.height - 0.5; }, { passive: true });

  var t0 = performance.now();
  function frame(now, still) {
    var t = (now - t0) / 1000;
    if (!still) { px += (tx - px) * 0.04; py += (ty - py) * 0.04; }
    // slow drift (periods 70-140 s) + pointer parallax; nearer layers move more
    var dx = Math.sin(t / 140 * 6.283), dy = Math.cos(t / 110 * 6.283);
    function mv(el, k, s, rot) { el.style.transform = 'translate3d(' + ((dx * 0.5 - px) * W * M * k).toFixed(2) + 'px,' + ((dy * 0.5 - py) * H * M * k).toFixed(2) + 'px,0)'
      + (s ? ' scale(' + s.toFixed(4) + ')' : '') + (rot ? ' rotate(' + rot.toFixed(4) + 'deg)' : ''); }
    mv(cNeb, 0.35, 1.12 + 0.03 * Math.sin(t / 90 * 6.283), 1.2 * Math.sin(t / 160 * 6.283));
    mv(cFar, 0.45); mv(cMid, 0.85);
    var x = cFx.getContext('2d'); x.setTransform(D, 0, 0, D, 0, 0); x.clearRect(0, 0, W, H); x.globalCompositeOperation = 'lighter';
    var ox = (dx * 0.5 - px) * W * M, oy = (dy * 0.5 - py) * H * M;
    for (var i = 0; i < bright.length; i++) { var s = bright[i];
      var a = still ? 0.85 : 0.55 + 0.45 * Math.sin(t * s.f * 2.2 + s.ph) * Math.sin(t * s.f * 0.7 + s.ph * 1.7);
      x.globalAlpha = Math.max(0.12, a); var w = s.img.width / D * (s.sp ? 0.85 : 1);
      x.drawImage(s.img, s.x + ox * s.z - w / 2, s.y + oy * s.z - w / 2, w, w); }
    if (!still) {
      if (now > nextShoot) { nextShoot = now + 3500 + rnd() * 6000;
        var ang = 0.35 + rnd() * 0.5, sp = 900 + rnd() * 700; shoot.push({ x: W * (0.05 + rnd() * 0.75), y: H * (0.03 + rnd() * 0.45), vx: Math.cos(ang) * sp, vy: Math.sin(ang) * sp, b: now, life: 650 + rnd() * 500 }); }
      for (i = shoot.length - 1; i >= 0; i--) { var m = shoot[i], age = (now - m.b) / m.life; if (age >= 1) { shoot.splice(i, 1); continue; }
        var hx = m.x + m.vx * age * m.life / 1000, hy = m.y + m.vy * age * m.life / 1000, len = 0.16, ex = hx - m.vx * len, ey = hy - m.vy * len;
        var g = x.createLinearGradient(hx, hy, ex, ey), al = Math.sin(age * Math.PI);
        g.addColorStop(0, 'rgba(255,255,255,' + (0.95 * al) + ')'); g.addColorStop(0.25, 'rgba(160,220,255,' + (0.45 * al) + ')'); g.addColorStop(1, 'rgba(0,156,222,0)');
        x.globalAlpha = 1; x.strokeStyle = g; x.lineWidth = 1.6; x.lineCap = 'round'; x.beginPath(); x.moveTo(hx, hy); x.lineTo(ex, ey); x.stroke(); }
    }
  }

  var raf = 0, onScreen = true;
  var nFrames = 0;
  function loop(now) { raf = 0; nFrames++; frame(now, false); if (running()) raf = requestAnimationFrame(loop); }
  function running() { return !reduced && onScreen && !document.hidden; }
  function kick() { if (running() && !raf) raf = requestAnimationFrame(loop); if (!running() && raf) { cancelAnimationFrame(raf); raf = 0; } }
  document.addEventListener('visibilitychange', kick);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { onScreen = es[0].isIntersecting; kick(); }).observe(hero);
  if (mq.addEventListener) mq.addEventListener('change', function () { reduced = mq.matches; if (reduced) frame(performance.now(), true); kick(); });
  var rt = 0, lastW = 0;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () {
    var w = Math.round(hero.getBoundingClientRect().width); if (Math.abs(w - lastW) < 2 && Math.abs(hero.getBoundingClientRect().height - H) < 80) return; // ignore iOS URL-bar height jitter
    lastW = w; setup(); frame(performance.now(), true); kick(); }, 180); }, { passive: true });
  lastW = Math.round(hero.getBoundingClientRect().width);
  setup(); frame(performance.now(), true); kick();
  window.__heroSpace = { frame: frame, frames: function () { return nFrames; }, size: function () { return { W: W, H: H, D: D }; } };
})();
