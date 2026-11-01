/* Homepage hero themes (Oct 16 2026). The theme is chosen inline in the hero (weekly rotation, ?hero=<name> override,
   scripts/build-hero-themes.py); this file renders the procedural ones. No libraries. Starts only after load + idle;
   the ground textures (pre-rendered by scripts/build-hero-assets.py from the same code), the poster still and NASA's Blue
   Marble Earth come from R2 (media.savingplanets.com) via data attributes; the procedural generators remain as fallback.
   Theme "space" = a seamless ~48 s two-scene loop (all procedural, scientifically grounded; facts in NOTES.md):
     A. Low glide over Enceladus's south polar terrain: bright white ice, blue-tinted "tiger stripe" fractures, fine
        water-ice jets rising from the stripes, side-lit by the low Sun; Saturn half-set on the horizon (Enceladus is
        tidally locked, so from the south pole Saturn sits on the horizon), drawn from Cassini PIA11141 (NASA/JPL-Caltech/
        Space Science Institute, public domain) at up to 3840px for Retina; rings nearly edge-on (equinox view matches
        Enceladus's ring-plane orbit). Procedural Saturn remains the fallback.
     B. Low glide over the cratered Moon from lunar orbit (Earthrise is only seen from orbit), Earth rising, Sun at right.
   Transition: the camera pulls up and away (ground recedes) while the scenes cross-fade.
   Ground = WebGL perspective plane (mipmapped, anisotropic, repeat-tiled procedural textures); sky/planets/jets = 2D
   canvases sized by devicePixelRatio. Pauses when hidden/offscreen; prefers-reduced-motion = one still frame. */
(function () {
  'use strict';
  var hero = document.querySelector('.hero[data-hero]');
  if (!hero || hero.getAttribute('data-hero') !== 'space') return;
  var box = hero.querySelector('.hero-space');
  if (!box || !window.HTMLCanvasElement) return;
  var credit = hero.querySelector('.hero-video-credit');
  if (credit) credit.textContent = 'Created by SI and Biological SI Partner · Saturn: NASA/JPL-Caltech/Space Science Institute';
  var caps = [].slice.call(hero.querySelectorAll('.hs-cap'));
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var reduced = mq.matches;

  var seed = 1;
  function rnd() { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }
  function hash(a, b) { var h = Math.imul(a | 0, 374761393) + Math.imul(b | 0, 668265263) | 0; h = Math.imul(h ^ h >>> 13, 1274126177); return ((h ^ h >>> 16) >>> 0) / 4294967296; }
  function sstep(a, b, x) { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); }

  function mk(cls, tag) { var c = document.createElement(tag || 'canvas'); c.className = 'hs-layer ' + cls; if (!tag) c.width = c.height = 0; box.appendChild(c); return c; } // 0x0 until sized at idle start (no layout shift)
  var cStars = mk('hs-stars'), cSkyA = mk('hs-skya'), cSkyB = mk('hs-skyb'), cEarth = mk('hs-earth'), cGround = mk('hs-ground'), cFx = mk('hs-fx');

  // ---------- periodic value noise (tiles seamlessly) ----------
  var P = new Uint8Array(512); seed = 0x5a1e42; (function () { var p = []; for (var i = 0; i < 256; i++) p[i] = i;
    for (i = 255; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)), t = p[i]; p[i] = p[j]; p[j] = t; } for (i = 0; i < 512; i++) P[i] = p[i & 255]; })();
  function fade(t) { return t * t * (3 - 2 * t); }
  function vnp(x, y, N) { var xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
    var x0 = ((xi % N) + N) % N, y0 = ((yi % N) + N) % N, x1 = (x0 + 1) % N, y1 = (y0 + 1) % N;
    var a = P[P[x0] + y0] / 255, b = P[P[x1] + y0] / 255, c = P[P[x0] + y1] / 255, d = P[P[x1] + y1] / 255, u = fade(xf), v = fade(yf);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v; }
  function fbmp(u, v, N, oct) { var s = 0, a = 0.5, f = 1; for (var o = 0; o < oct; o++) { s += a * vnp(u * N * f + o * 17, v * N * f + o * 31, N * f); a *= 0.5; f *= 2; } return s; }
  function vn(x, y) { return vnp(x, y, 256); }

  // Run work in ~6 ms slices between frames; tok cancels stale jobs after a resize.
  var tok = 0;
  function slices(n, fn, done, keep) { var my = tok, i = 0; (function step() { if (!keep && my !== tok) return; var t = performance.now();
    while (i < n && performance.now() - t < 6) fn(i++); if (i < n) setTimeout(step, 0); else done(); })(); }

  // ---------- ground textures (T x T, power of two, seamless) ----------
  var T = 512, STRIPE_C = 1.5, TILE = 12;          // world units per tile; 4 stripes per tile, 3 units apart
  function wob(u, k) { return 0.012 * Math.sin(6.2832 * 2 * u + k * 1.7); }
  function shadeTex(h, alb, L, amb, relief, done) {
    var img = new ImageData(T, T), d = img.data, ln = Math.sqrt(L[0] * L[0] + L[1] * L[1] + L[2] * L[2]);
    var lx = L[0] / ln, ly = L[1] / ln, lz = L[2] / ln;
    slices(T, function (j) { var jm = ((j - 1 + T) % T) * T, jp = ((j + 1) % T) * T, jr = j * T;
      for (var i = 0; i < T; i++) { var im = (i - 1 + T) % T, ip = (i + 1) % T;
        var gx = (h[jr + ip] - h[jr + im]) * relief, gy = (h[jp + i] - h[jm + i]) * relief, nl = Math.sqrt(gx * gx + gy * gy + 1);
        var s = Math.max(0, (-gx * lx - gy * ly + lz) / nl), o = (jr + i) * 4, k = (jr + i) * 3;
        var b = amb + (1 - amb) * s;
        d[o] = Math.min(255, alb[k] * b); d[o + 1] = Math.min(255, alb[k + 1] * b); d[o + 2] = Math.min(255, alb[k + 2] * b); d[o + 3] = 255; } },
      function () { done(img); }, true);
  }
  function enceladusTex(done) {
    var h = new Float32Array(T * T), alb = new Float32Array(T * T * 3);
    slices(T, function (j) { var v = j / T;
      for (var i = 0; i < T; i++) { var u = i / T, k = j * T + i;
        var base = 0.6 * fbmp(u, v, 8, 5) + 0.4 * fbmp(u + 0.13, v + 0.71, 32, 3), r = 1 - Math.abs(2 * fbmp(u + 0.31, v + 0.17, 16, 4) - 1), crack = Math.pow(r, 10);
        var st = 0, tint = 0;
        for (var s = 0; s < 4; s++) { var c = (s * 3 + STRIPE_C) / TILE + wob(u, s), dd = v - c; dd -= Math.round(dd);
          var w = 0.0075 * (0.8 + 0.5 * vnp(u * 32 + s * 9, 0.5, 32));
          var tr = Math.exp(-(dd * dd) / (w * w)), rg = Math.exp(-Math.pow((Math.abs(dd) - 1.9 * w) / (0.8 * w), 2));
          st += -0.55 * tr + 0.32 * rg; tint += tr + 0.35 * rg; }
        h[k] = 0.16 * base + 0.05 * crack + st * 0.45;
        var a = 0.93 + 0.07 * fbmp(u + 0.5, v + 0.5, 16, 3), tt = Math.min(1, tint);
        alb[k * 3] = 255 * a * (1 - 0.2 * tt); alb[k * 3 + 1] = 255 * a * (1 - 0.09 * tt); alb[k * 3 + 2] = 255 * Math.min(1, a * 1.02); } },
      function () { shadeTex(h, alb, [0.9, 0.05, 0.42], 0.52, 16 * T / 512, done); }, true);
  }
  function moonTex(done) {
    var h = new Float32Array(T * T), alb = new Float32Array(T * T * 3); seed = 0x3b11;
    slices(T, function (j) { var v = j / T;
      for (var i = 0; i < T; i++) { var u = i / T, k = j * T + i, m = sstep(0.45, 0.62, fbmp(u + 0.2, v + 0.7, 4, 4));
        h[k] = 0.035 * fbmp(u, v, 32, 4); var a = (0.62 - 0.2 * m) * (0.9 + 0.1 * fbmp(u, v, 32, 3));
        alb[k * 3] = 255 * a * 1.02; alb[k * 3 + 1] = 255 * a; alb[k * 3 + 2] = 255 * a * 0.95; } },
      function () { // craters (power-law sizes), wrapped across tile edges
        var n = 1160; slices(n, function (ci) { var cx = rnd() * T, cy = rnd() * T, r0 = rnd(), r = ci < 260 ? T * (0.006 + 0.11 * Math.pow(r0, 2.6)) : T * (0.0022 + 0.0055 * r0), dep = 0.8 + rnd() * 0.4; // + 900 small craters for close-up detail
          var R = Math.ceil(r * 1.4);
          for (var y = -R; y <= R; y++) for (var x = -R; x <= R; x++) { var q = Math.sqrt(x * x + y * y) / r; if (q > 1.4) continue;
            var ii = ((Math.round(cx) + x) % T + T) % T, jj = ((Math.round(cy) + y) % T + T) % T, k = jj * T + ii;
            var bowl = q < 1 ? (q * q - 1) * 0.5 * dep : 0, rim = 0.22 * dep * Math.exp(-Math.pow((q - 1) / 0.16, 2));
            h[k] += (bowl + rim) * r / T * 6; if (q < 1.15) { var e = 1 + 0.06 * (1 - q); alb[k * 3] *= e; alb[k * 3 + 1] *= e; alb[k * 3 + 2] *= e; } } },
          function () { shadeTex(h, alb, [0.96, 0.0, 0.32], 0.16, 26 * T / 512, done); }, true); }, true);
  }

  // ---------- WebGL ground ----------
  var gl = null, prog = null, U = {}, texA = null, texB = null, glOk = false;
  function initGL() {
    try { gl = cGround.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false, depth: false, powerPreference: 'default' }); } catch (e) { gl = null; }
    if (!gl) return false;
    var vs = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
    var fs = '#ifdef GL_FRAGMENT_PRECISION_HIGH\nprecision highp float;\n#else\nprecision mediump float;\n#endif\n' +
      'uniform sampler2D tA,tB;uniform vec2 res;uniform float mixT,hY,f,camH,scroll,curv,tile,dpr,top;' +
      'void main(){vec2 q=gl_FragCoord.xy;float y=top+(res.y-q.y);float dx=q.x-res.x*.5;float yh=hY+curv*dx*dx;float dy=y-yh;' +
      'if(dy<=0.){gl_FragColor=vec4(0.);return;}float z=camH*f/dy;vec2 uv=vec2(dx*z/f,z+scroll)/tile;' +
      'vec3 c=mix(texture2D(tA,uv).rgb,texture2D(tB,uv).rgb,mixT);' +
      // near-field detail: the same seamless texture at 4.7x frequency modulates brightness close to the camera, so the
      // foreground ice / regolith stays crisp at full DPR instead of showing magnified texels
      'vec2 u2=uv*4.7+vec2(.31,.57);vec3 dt=mix(texture2D(tA,u2).rgb,texture2D(tB,u2).rgb,mixT);' +
      'float dl=dot(dt,vec3(.299,.587,.114))/mix(.86,.42,mixT);c*=mix(1.,clamp(dl,.55,1.4),.5*smoothstep(12.,2.5,z));' +
      'float lim=smoothstep(0.,28.*dpr,dy);c*=mix(.82,1.,lim);' +           // slight darkening right at the airless limb
      'float a=clamp(dy,0.,1.);gl_FragColor=vec4(c*a,a);}';
    function sh(t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; }
    var v = sh(gl.VERTEX_SHADER, vs), fr = sh(gl.FRAGMENT_SHADER, fs); if (!v || !fr) return false;
    prog = gl.createProgram(); gl.attachShader(prog, v); gl.attachShader(prog, fr); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return false;
    gl.useProgram(prog);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    ['tA', 'tB', 'res', 'mixT', 'hY', 'f', 'camH', 'scroll', 'curv', 'tile', 'dpr', 'top'].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
    gl.uniform1i(U.tA, 0); gl.uniform1i(U.tB, 1);
    texA = mkTex([238, 242, 248]); texB = mkTex([120, 118, 114]);
    return true;
  }
  var aniso = null;
  function mkTex(rgb) { var t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([rgb[0], rgb[1], rgb[2], 255]));
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); return t; }
  function upTex(t, img) { gl.bindTexture(gl.TEXTURE_2D, t); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    aniso = aniso || gl.getExtension('EXT_texture_filter_anisotropic') || gl.getExtension('WEBKIT_EXT_texture_filter_anisotropic');
    if (aniso) gl.texParameterf(gl.TEXTURE_2D, aniso.TEXTURE_MAX_ANISOTROPY_EXT, Math.min(8, gl.getParameter(aniso.MAX_TEXTURE_MAX_ANISOTROPY_EXT)));
    gl.generateMipmap(gl.TEXTURE_2D); }

  // ---------- layout ----------
  var W = 0, H = 0, D = 1, hY = 0, FOC = 0, sprites = {};
  var SAT = {}, EAR = {}, SUN = {};
  // Adaptive quality (battery saver): QL rises 0 -> 1 -> 2 only when the smoothed frame time stays above 40 ms for 3 s.
  // Level 1/2 render the ground and ice-jet canvases at 70% / 50% of the device pixel ratio (never below 0.75) and draw
  // 60% / 40% of the jet particles. Fast devices never leave level 0, so they keep full quality.
  var QL = 0, QS = [1, 0.7, 0.5], QN = [1, 0.6, 0.4];
  function ED() { return Math.min(window.devicePixelRatio || 1, 3); } // small sprites (Earth): always full DPR, never budget-capped
  function qd() { return Math.max(0.75, D * QS[QL]); }
  function sizeCanvas(c, w, h, x, y) { var k = (c === cGround || c === cFx) ? qd() : c === cEarth ? ED() : D; c.width = Math.round(w * k); c.height = Math.round(h * k); c.style.width = w + 'px'; c.style.height = h + 'px';
    c.style.left = (x || 0) + 'px'; c.style.top = (y || 0) + 'px'; if (c === cGround) return null; var g = c.getContext('2d'); g.setTransform(k, 0, 0, k, 0, 0); return g; }
  function sprite(r, rgb) { var key = r + rgb; if (sprites[key]) return sprites[key];
    var s = Math.ceil(r * 4) * 2 + 2, c = document.createElement('canvas'); c.width = c.height = s;
    var x = c.getContext('2d'), m = s / 2, g = x.createRadialGradient(m, m, 0, m, m, r * 4);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.2, 'rgba(' + rgb + ',0.85)'); g.addColorStop(0.5, 'rgba(' + rgb + ',0.18)'); g.addColorStop(1, 'rgba(' + rgb + ',0)');
    x.fillStyle = g; x.beginPath(); x.arc(m, m, r * 4, 0, 7); x.fill(); return (sprites[key] = c); }
  var TINTS = ['205,225,255', '255,244,232', '170,215,255', '255,226,210', '230,236,255'];

  function drawStars() {
    var x = sizeCanvas(cStars, W, H); x.globalCompositeOperation = 'lighter'; seed = 0x77e1;
    var n = Math.round(W * H / 1e6 * 1500 + 300);
    for (var i = 0; i < n; i++) { var u = rnd() * W, v = rnd() * hY * 1.05, r = 0.3 + Math.pow(rnd(), 4) * 1.4, sp = sprite(Math.max(0.35, r * D) / D, TINTS[(rnd() * 5) | 0]);
      x.globalAlpha = 0.25 + 0.75 * rnd(); var s = sp.width / D * (r < 0.6 ? 0.8 : 1); x.drawImage(sp, u - s / 2, v - s / 2, s, s); }
  }

  // Saturn seen from Enceladus (3.95 Saturn radii out): angular radius asin(1/3.95) = 14.7 deg; ring edge (A ring
  // outer edge, 2.27 Rs) appears atan(2.27/3.95) = 29.9 deg from the centre, i.e. about 2.0 apparent radii.
  // Saturn: Cassini PIA11141 natural-color equinox mosaic (NASA/JPL-Caltech/Space Science Institute, public domain).
  // Served from R2 up to 3840px WebP; meta gx,gy,gr map the globe center/radius so on-screen size stays SAT.R.
  var SATIMG = null, satTried = false, satMeta = { gx: 0.34751, gy: 0.48782, gr: 0.13085 };
  function loadSat() {
    if (satTried) return; satTried = true;
    var raw = (box.getAttribute('data-sat-meta') || '').split(',');
    if (raw.length >= 3) { satMeta.gx = +raw[0] || satMeta.gx; satMeta.gy = +raw[1] || satMeta.gy; satMeta.gr = +raw[2] || satMeta.gr; }
    var need = (2 * SAT.R / Math.max(0.05, satMeta.gr)) * Math.min(window.devicePixelRatio || 1, 3);
    var set = (box.getAttribute('data-sat') || '').split(',').map(function (t) {
      var p = t.trim().split(/\s+/); return { u: p[0], w: parseInt(p[1], 10) || 0 };
    }).filter(function (e) { return e.u && e.w >= 640; }).sort(function (a, b) { return a.w - b.w; });
    if (!set.length) return;
    var pick = set[set.length - 1]; for (var k = 0; k < set.length; k++) if (set[k].w >= need) { pick = set[k]; break; }
    var im = new Image(); im.crossOrigin = 'anonymous'; im.decoding = 'async';
    im.onload = function () { SATIMG = im; drawSaturn(); }; im.onerror = function () { SATIMG = null; }; im.src = pick.u;
  }
  function drawSaturn() {
    var x = sizeCanvas(cSkyA, W, H), R = SAT.R, cx = SAT.x, cy = SAT.y, roll = -0.1, flat = 0.902;
    var ang = function (r) { return Math.atan(r / 3.95) / Math.asin(1 / 3.95) * R; };
    // E ring: faint broad band along the ring plane across the whole sky (Enceladus orbits inside it)
    x.save(); x.translate(cx, cy); x.rotate(roll);
    var eg = x.createLinearGradient(0, -R * 0.5, 0, R * 0.5); eg.addColorStop(0, 'rgba(160,200,255,0)'); eg.addColorStop(0.5, 'rgba(170,205,255,0.10)'); eg.addColorStop(1, 'rgba(160,200,255,0)');
    x.fillStyle = eg; x.fillRect(-W * 2, -R * 0.5, W * 4, R); x.restore();
    if (SATIMG && satMeta.gr > 0) {
      var imgW = R / satMeta.gr, imgH = imgW * (SATIMG.naturalHeight / SATIMG.naturalWidth);
      x.save(); x.translate(cx, cy); x.rotate(roll);
      x.drawImage(SATIMG, -satMeta.gx * imgW, -satMeta.gy * imgH, imgW, imgH);
      x.restore(); return;
    }
    // procedural fallback (banded globe + edge-on rings) until the Cassini texture arrives
    var S = Math.ceil(2 * R * D), img = new ImageData(S, Math.ceil(2 * R * flat * D) + 2), d = img.data, L = [0.82, -0.12, 0.56];
    var ih = img.height;
    for (var j = 0; j < ih; j++) for (var i = 0; i < S; i++) {
      var nx = (i + 0.5) / S * 2 - 1, ny = ((j + 0.5) / ih * 2 - 1), rr = nx * nx + ny * ny, o = (j * S + i) * 4; if (rr > 1) continue;
      var nz = Math.sqrt(1 - rr), lat = ny, w = 0.5 + 0.5 * Math.sin(lat * 23 + 1.3 * Math.sin(lat * 7)) * 0.6 + 0.25 * vn(lat * 40, nx * 2);
      var dif = Math.max(0, nx * L[0] + ny * L[1] / flat + nz * L[2]), lit = sstep(-0.03, 0.25, dif) * (0.12 + 0.88 * dif) * (0.72 + 0.28 * nz);
      var rs = (lat > 0.035 && lat < 0.075) ? 0.45 : 1;
      d[o] = Math.min(255, (226 + 30 * w) * lit * rs * 1.08); d[o + 1] = Math.min(255, (196 + 30 * w) * lit * rs * 1.08); d[o + 2] = Math.min(255, (146 + 24 * w) * lit * rs * 1.08); d[o + 3] = 255; }
    var g = document.createElement('canvas'); g.width = S; g.height = ih; g.getContext('2d').putImageData(img, 0, 0);
    x.save(); x.translate(cx, cy); x.rotate(roll); x.drawImage(g, -R, -R * flat, 2 * R, 2 * R * flat);
    x.globalCompositeOperation = 'lighter'; x.lineCap = 'butt';
    [[1.24, 1.53, 0.22], [1.53, 1.95, 0.95], [1.95, 2.03, 0.08], [2.03, 2.27, 0.7]].forEach(function (b) {
      [-1, 1].forEach(function (sg) { var a0 = ang(b[0]) * sg, a1 = ang(b[1]) * sg;
        x.strokeStyle = 'rgba(255,240,215,' + b[2] + ')'; x.lineWidth = 1.2; x.beginPath(); x.moveTo(a0, 0); x.lineTo(a1, 0); x.stroke();
        x.strokeStyle = 'rgba(255,235,205,' + (b[2] * 0.18) + ')'; x.lineWidth = 4; x.beginPath(); x.moveTo(a0, 0); x.lineTo(a1, 0); x.stroke(); }); });
    x.restore();
  }

  // Earth texture: NASA Blue Marble (land, ocean, ice and clouds; NASA Goddard / Visible Earth, public domain) from R2, fetched
  // lazily after the first frames; until it arrives (or if it fails) the procedural Earth below is used.
  var BM = null, bmTried = false;
  function loadBM() { if (bmTried) return; bmTried = true;
    var need = 2 * Math.PI * EAR.R * ED(), im = new Image(); im.crossOrigin = 'anonymous'; im.decoding = 'async';
    im.onload = function () { try { var c = document.createElement('canvas'); c.width = im.naturalWidth; c.height = im.naturalHeight;
        var g = c.getContext('2d'); g.drawImage(im, 0, 0); BM = { d: g.getImageData(0, 0, c.width, c.height).data, w: c.width, h: c.height };
        drawEarth(true); } catch (e) { BM = null; } };
    var set = (box.getAttribute('data-bm') || '').split(',').map(function (t) { var p = t.trim().split(/\s+/); return { u: p[0], w: parseInt(p[1], 10) || 0 }; })
      .filter(function (e) { return e.u && e.w >= 1280; }).sort(function (a, b) { return a.w - b.w; });
    if (!set.length) return; var pick = set[set.length - 1]; for (var k = 0; k < set.length; k++) if (set[k].w >= need * 2.5) { pick = set[k]; break; } // 2.5x oversampled (Oct 17: Earth is 2x larger; prefer crisp Retina)
    im.src = pick.u; }
  function bmAt(lon, lat, out) { // bilinear sample, lon/lat in radians
    var u = ((lon / 6.28319 + 0.5) % 1 + 1) % 1 * BM.w - 0.5, v = (0.5 - lat / 3.14159) * BM.h - 0.5;
    var i0 = Math.floor(u), j0 = Math.max(0, Math.min(BM.h - 2, Math.floor(v))), fu = u - i0, fv = Math.max(0, Math.min(1, v - j0));
    var i1 = (i0 + 1) % BM.w; i0 = (i0 + BM.w) % BM.w;
    var a = (j0 * BM.w + i0) * 4, b = (j0 * BM.w + i1) * 4, c = ((j0 + 1) * BM.w + i0) * 4, e = ((j0 + 1) * BM.w + i1) * 4, d = BM.d;
    for (var k = 0; k < 3; k++) out[k] = (d[a + k] * (1 - fu) + d[b + k] * fu) * (1 - fv) + (d[c + k] * (1 - fu) + d[e + k] * fu) * fv; }
  function planetPx(T2, L) {
    var rgb = [0, 0, 0], tilt = 0.41, ct = Math.cos(tilt), st = Math.sin(tilt), lon0 = 0.35; // Atlantic / Africa facing us, axis tilted
    return function (d, o, i, j) {
      var nx = (i + 0.5) / T2 * 2 - 1, ny = (j + 0.5) / T2 * 2 - 1, rr = nx * nx + ny * ny; if (rr > 1) { d[o + 3] = 0; return; }
      var nz = Math.sqrt(1 - rr);
      if (BM) { // orthographic globe: rotate view vector by the tilt, then lon/lat on the texture
        var X = nx * ct - ny * st, Y = nx * st + ny * ct, la = Math.asin(Math.max(-1, Math.min(1, -Y))), lo = Math.atan2(X, nz) + lon0;
        bmAt(lo, la, rgb);
        var dif0 = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]), lit0 = sstep(-0.035, 0.18, dif0) * (0.1 + 0.9 * Math.pow(dif0, 0.8));
        var blu = Math.max(0, Math.min(1, (rgb[2] - Math.max(rgb[0], rgb[1])) / 40)), sp0 = Math.pow(Math.max(0, 2 * dif0 * nz - L[2]), 30) * blu * 0.5;
        var rim0 = Math.pow(1 - nz, 3);
        d[o] = Math.min(255, rgb[0] * lit0 * 1.05 + 255 * sp0 + rim0 * 30 * lit0); d[o + 1] = Math.min(255, rgb[1] * lit0 * 1.05 + 250 * sp0 + rim0 * 120 * lit0);
        d[o + 2] = Math.min(255, rgb[2] * lit0 * 1.08 + 245 * sp0 + rim0 * 210 * lit0); d[o + 3] = 255; return; }
      var lon = Math.atan2(nx, nz) * 1.6, lat = Math.asin(ny) * 1.6;
      var ln = fb(lon + 30, lat + 11), land = sstep(0.56, 0.6, ln), hi = sstep(0.6, 0.75, ln), tone = vn(lon * 6 + 3, lat * 6 + 1);
      var cl = sstep(0.48, 0.8, fb(lon * 2.2 + 50 + lat * 0.6, lat * 3.6 + 4)) * 0.95;
      var dif = Math.max(0, nx * L[0] + ny * L[1] + nz * L[2]), lit = sstep(-0.04, 0.3, dif) * (0.2 + 0.8 * dif);
      var rim = Math.pow(1 - nz, 2.4), sh = 0.55 + 0.45 * sstep(0.2, 0.7, ln + (1 - land));
      var oR = 4 + 10 * sh, oG = 34 + 52 * sh, oB = 92 + 70 * sh, gR = 28 + 60 * hi + 30 * tone, gG = 82 + 30 * tone - 10 * hi, gB = 62 - 20 * hi;
      var R = (oR * (1 - land) + gR * land) * (1 - cl) + 236 * cl, G = (oG * (1 - land) + gG * land) * (1 - cl) + 243 * cl, B = (oB * (1 - land) + gB * land) * (1 - cl) + 255 * cl;
      var spec = Math.pow(Math.max(0, 2 * dif * nz - L[2]), 28) * (1 - land) * (1 - cl) * 0.7;
      d[o] = R * lit + 255 * spec + rim * 25 * lit; d[o + 1] = G * lit + 250 * spec + rim * 150 * lit; d[o + 2] = B * lit + 245 * spec + rim * 235 * lit; d[o + 3] = 255;
    };
  }
  function fb(x, y) { var s = 0, a = 0.5; for (var o = 0; o < 6; o++) { s += a * vn(x, y); x = x * 2.03 + 17.1; y = y * 2.01 + 9.7; a *= 0.5; } return s; }

  // Earth from lunar orbit (telephoto framing like Apollo 8's 250 mm "Earthrise"); Sun/Earth size ratio 0.28 is real.
  function drawEarth(hi) {
    var R = EAR.R, pad = Math.ceil(R * 0.35), S = 2 * (R + pad), x = sizeCanvas(cEarth, S, S, 0, 0);
    var T2 = hi ? Math.min(1400, Math.round(2 * R * ED())) : 128, img = new ImageData(T2, T2), px = planetPx(T2, [0.88, -0.18, 0.44]);
    var fin = function () { var t = document.createElement('canvas'); t.width = t.height = T2; t.getContext('2d').putImageData(img, 0, 0);
      x.clearRect(0, 0, S, S); var c = S / 2, h = x.createRadialGradient(c, c, R * 0.985, c, c, R * 1.12);
      h.addColorStop(0, 'rgba(90,190,255,0.45)'); h.addColorStop(0.3, 'rgba(0,156,222,0.14)'); h.addColorStop(1, 'rgba(0,156,222,0)');
      x.fillStyle = h; x.beginPath(); x.arc(c, c, R * 1.14, 0, 7); x.fill();
      x.save(); x.beginPath(); x.arc(c, c, R, 0, 7); x.clip(); x.fillStyle = '#01040a'; x.fill(); x.drawImage(t, c - R, c - R, 2 * R, 2 * R); x.restore();
      x.save(); x.globalCompositeOperation = 'lighter'; x.beginPath(); x.arc(c, c, R - 0.6, -1.15, 1.0); x.strokeStyle = 'rgba(170,230,255,0.75)'; x.lineWidth = 1;
      x.stroke(); x.restore(); };
    if (!hi) { for (var j = 0; j < T2; j++) for (var i = 0; i < T2; i++) px(img.data, (j * T2 + i) * 4, i, j); fin(); }
    else slices(T2, function (j) { for (var i = 0; i < T2; i++) px(img.data, (j * T2 + i) * 4, i, j); }, fin);
  }
  function drawSun() {
    var x = sizeCanvas(cSkyB, W, H), cx = SUN.x, cy = SUN.y, r = SUN.R;
    var g = x.createRadialGradient(cx, cy, 0, cx, cy, r * 14); g.addColorStop(0, 'rgba(255,250,240,0.55)'); g.addColorStop(0.08, 'rgba(255,244,225,0.22)');
    g.addColorStop(0.3, 'rgba(255,236,210,0.06)'); g.addColorStop(1, 'rgba(255,236,210,0)'); x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.globalCompositeOperation = 'lighter';
    [[0, 1], [1, 0]].forEach(function (a) { var lg = x.createLinearGradient(cx - a[0] * r * 8, cy - a[1] * r * 8, cx + a[0] * r * 8, cy + a[1] * r * 8);
      lg.addColorStop(0, 'rgba(255,245,230,0)'); lg.addColorStop(0.5, 'rgba(255,250,240,0.35)'); lg.addColorStop(1, 'rgba(255,245,230,0)'); x.fillStyle = lg;
      if (a[0]) x.fillRect(cx - r * 8, cy - r * 0.1, r * 16, r * 0.2); else x.fillRect(cx - r * 0.1, cy - r * 8, r * 0.2, r * 16); });
    x.globalCompositeOperation = 'lighter'; var cg = x.createRadialGradient(cx, cy, 0, cx, cy, r * 3); cg.addColorStop(0, 'rgba(255,252,245,1)'); cg.addColorStop(0.33, 'rgba(255,250,240,0.9)'); cg.addColorStop(1, 'rgba(255,240,215,0)');
    x.fillStyle = cg; x.beginPath(); x.arc(cx, cy, r * 3, 0, 7); x.fill(); x.globalCompositeOperation = 'source-over'; x.fillStyle = '#ffffff'; x.shadowColor = 'rgba(255,245,225,1)'; x.shadowBlur = r * 1.5;
    x.beginPath(); x.arc(cx, cy, r, 0, 7); x.fill();
  }

  var curvA = 0, curvB = 0, gTop = 0;
  // Caption goes at the inline-start bottom corner above the credit; if that would touch the hero text, the Help button
  // or the language banner (short landscape screens), it moves to the inline-start top corner just under the nav.
  function hit(a, b) { return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top; }
  var capKey = '';
  function placeCaption() {
    if (!caps.length) return; hero.classList.remove('hs-captop', 'hs-capoff');
    var q0 = [].slice.call(hero.querySelectorAll('.hero-content > *, .sticky-help')).concat([].slice.call(document.querySelectorAll('.sp-lb-in')));
    var obs = q0.map(function (e) { return e.getBoundingClientRect(); }).filter(function (q) { return q.width > 0; });
    var bad = function () { return caps.some(function (c) { var q = c.getBoundingClientRect(); return obs.some(function (o) { return hit(q, o); }); }); };
    var key = 'b', top = 0;
    if (bad()) { var hr = hero.getBoundingClientRect();
      [].forEach.call(document.querySelectorAll('#topnav, .sp-lb-in'), function (e) { var q = e.getBoundingClientRect(); if (q.height) top = Math.max(top, q.bottom - hr.top); });
      key = 't' + Math.round(top + 12); hero.style.setProperty('--hs-captop', Math.round(top + 12) + 'px'); hero.classList.add('hs-captop');
      if (bad()) { key = 'off'; hero.classList.remove('hs-captop'); } } // no free spot (tiny/short screens): no caption, never over the text
    hero.classList.toggle('hs-capoff', key === 'off');
    // A caption that is already showing and has to move (e.g. the language banner appeared under the nav) is hidden for
    // two frames while it moves, so the move is never a layout shift (CLS stays 0).
    if (hero.classList.contains('hs-placed') && key !== capKey) { hero.classList.remove('hs-placed');
      requestAnimationFrame(function () { requestAnimationFrame(function () { hero.classList.add('hs-placed'); }); }); }
    else hero.classList.add('hs-placed');
    capKey = key;
  }

  // Oct 17: center the whole title block (kicker → buttons) in the empty band between the nav and the moon horizon,
  // equal gap above and below (owner, iPad landscape reference). Moons stay put; only the text moves.
  function placeTitleBlock(hr) {
    var content = hero.querySelector('.hero-content'); if (!content) return;
    var nav = document.getElementById('topnav') || document.querySelector('nav');
    var navBottom = 56;
    if (nav) { var nb = nav.getBoundingClientRect(); navBottom = Math.max(0, Math.round(nb.bottom - hr.top)); }
    else if (W >= 1140) navBottom = 92;
    hero.style.setProperty('--hero-block-top', navBottom + 'px'); // measure block height at a known top
    var kicker = content.querySelector('.hero-kicker'), end = content.querySelector('.hero-email') || content.querySelector('.hero-ctas');
    if (!kicker || !end) return;
    var blockH = end.getBoundingClientRect().bottom - kicker.getBoundingClientRect().top;
    if (!(blockH > 0) || !(hY > navBottom + 40)) return;
    var top = navBottom + (hY - navBottom - blockH) / 2;
    top = Math.max(navBottom + 4, Math.min(top, hY - blockH - 8));
    hero.style.setProperty('--hero-block-top', Math.round(top) + 'px');
  }

  function setup() {
    tok++; sprites = {};
    var r = hero.getBoundingClientRect(); W = Math.max(320, Math.round(r.width)); H = Math.max(480, Math.round(r.height));
    var big = /[?&]hero-poster=1/.test(location.search); // poster builder only: native 6K stills
    var dpr = Math.min(window.devicePixelRatio || 1, big ? 6 : 3); D = Math.min(dpr, Math.sqrt((big ? 40e6 : 21e6) / (W * H))); // full DPR up to ~6K-wide backing (6016x3384 = 6K Retina @2x); slow devices step down via QL
    // Oct 17 ~7:10 PM: FREEZE horizon/Saturn/Enceladus/Earth to the viewport so raising the title never moves the moons.
    // layoutCb matches the 4vh title-bottom fractions (iPad-L 605/820, iPad-P 680/1180). Title is then recentered in JS
    // between the nav and this fixed horizon (equal gaps). Plumes grow upward to meet the title.
    var port0 = W < H, last = hero.querySelector('.hero-email') || hero.querySelector('.hero-ctas');
    var layoutCb = Math.round(H * (port0 ? 0.576 : 0.738));
    hY = Math.round(Math.min(H * 0.8, Math.max(H * 0.5, layoutCb + Math.max(36, H * (port0 ? 0.17 : 0.05)))));
    placeTitleBlock(r); // sets --hero-block-top so the text sits centered between nav bottom and hY
    var cb = last ? last.getBoundingClientRect().bottom - r.top : H * 0.6;
    hero.classList.toggle('hs-lowsky', cb > hY - 8); // short screens: the last text line overlaps the horizon -> give it a backdrop
    FOC = Math.max(W, H) * 0.9; curvA = (H * 0.045) / Math.pow(W / 2, 2); curvB = (H * 0.022) / Math.pow(W / 2, 2);
    var port = W < H;
    // Saturn: in portrait it sits low, between the text and the horizon; in landscape it hangs beside the text column
    // (from ~65 deg S on Enceladus, Saturn stands about 25 deg above the horizon, its rings an edge-on line).
    var tr = 0; TXT = [1e9, 1e9, -1e9, -1e9]; [].forEach.call(hero.querySelectorAll('.hero-content > *'), function (e) { var q = e.getBoundingClientRect(); if (!q.width) return;
      if (e.tagName === 'H1') TXH = [q.left - r.left - 16, q.top - r.top - 14, q.right - r.left + 16, q.bottom - r.top + 14];
      tr = Math.max(tr, q.right - r.left); TXT = [Math.min(TXT[0], q.left - r.left - 12), Math.min(TXT[1], q.top - r.top - 10), Math.max(TXT[2], q.right - r.left + 12), Math.max(TXT[3], q.bottom - r.top + 10)]; });
    if (port) { SAT = { R: Math.round(Math.max(56, Math.min(W * 0.17, (hY - cb - 24) / 1.6))), x: W * 0.78 };
      SAT.y = Math.max(cb + 16 + SAT.R, hY - 0.75 * SAT.R) + curvA * Math.pow((SAT.x - W / 2), 2); }
    else { SAT = { R: Math.round(Math.max(90, Math.min(W * 0.15, (W - tr - 30) / 2, H * 0.27))) }; SAT.x = Math.max(W * 0.8, Math.min(W - SAT.R * 1.05, tr + 20 + SAT.R));
      SAT.y = Math.min(hY - 1.15 * SAT.R, H * 0.42); }
    // Oct 17: Cassini PIA11141 sprite is wider to the RIGHT of the globe (gx≈0.35). Without this, the right ring
    // ansa is clipped by the canvas edge on iPad landscape — looked like "part of the ring disappeared".
    // Globe radius unchanged; only SAT.x shifts left enough for the full ring to fit. Ring shadow on the globe in
    // the photo is real Cassini imagery (kept). Portrait uses the same clamp.
    (function () {
      var ringRight = SAT.R * (1 - satMeta.gx) / Math.max(0.05, satMeta.gr);
      var ringLeft = SAT.R * satMeta.gx / Math.max(0.05, satMeta.gr);
      SAT.x = Math.min(SAT.x, W - ringRight - 6);
      if (port) SAT.x = Math.min(SAT.x, W - ringRight - 6);
      // keep Saturn on the right half when possible; left ansa may hang off-screen (OK)
      SAT.x = Math.max(SAT.x, Math.min(W * 0.62, W - ringRight - 6));
    })();
    // Oct 17 (owner: Earthrise Earth TWICE as big). Diameter 2x; Saturn/Enceladus/moons unchanged.
    EAR = { R: Math.round(Math.min(W, H) * (port ? 0.19 : 0.17)), x: W * (port ? 0.18 : 0.08) };
    // Earth clears the horizon (centre ~2.1 R above it). With 2x size, nudge left (x) so the disk stays mostly
    // off the title column; portrait still never climbs into the text block.
    EAR.peak = hY - 2.1 * EAR.R; if (port) EAR.peak = Math.max(EAR.peak, Math.min(hY - 1.2 * EAR.R, cb + 14 + EAR.R));
    // Keep the larger Earth from covering the title: hang it partly off the left edge when it would overlap.
    if (TXT[0] < 1e8 && EAR.x + EAR.R > TXT[0] - 16) {
      EAR.x = Math.max(EAR.R * 0.5, TXT[0] - EAR.R - 24);
    }
    if (!port && TXT[3] < 1e8 && (EAR.peak - EAR.R) < TXT[3] && (EAR.x + EAR.R) > TXT[0]) {
      // last resort: lower the rise peak so the disk sits under the title block
      EAR.peak = Math.min(hY - 1.15 * EAR.R, TXT[3] + EAR.R + 20);
    }
    SUN = { R: Math.max(7, Math.round(EAR.R * 0.28)), x: W * (port ? 0.86 : 0.9) };
    // the Sun never sits behind the text block: portrait -> between the text and the horizon; landscape -> beside the text column
    SUN.y = port ? cb + (hY - cb) * 0.32 : Math.max(hY * 0.3, 170);
    drawStars(); loadSat(); drawSaturn(); drawSun(); drawEarth(false); drawEarth(true);
    gTop = Math.max(0, hY - 2); sizeCanvas(cGround, W, H - gTop, 0, gTop);
    sizeCanvas(cFx, W, H); placeCaption();
    if (!glOk) glOk = initGL();
    if (glOk) { gl.viewport(0, 0, cGround.width, cGround.height);
      if (!texReady) { texReady = true; // pre-rendered 1024^2 textures (scripts/build-hero-assets.py); procedural only as a fallback
        texFile('data-tex-a', enceladusTex, function (img) { safeTex(texA, img, enceladusTex); box.classList.add('hs-ready'); if (!running()) frame(true);
          texFile('data-tex-b', moonTex, function (img2) { safeTex(texB, img2, moonTex); if (!running()) frame(true); }); }); } }
    else box.classList.add('hs-ready', 'hs-nogl');
  }
  var texReady = false;
  function safeTex(t, img, gen) { try { upTex(t, img); } catch (e) { gen(function (c) { upTex(t, c); }); } } // CORS/decode failure -> procedural
  function texFile(attr, gen, done) { // 2048^2 on large / high-DPR screens (iPad, Retina desktop), 1024^2 on small ones
    var u = (W * D > 1500 && box.getAttribute(attr + '2')) || box.getAttribute(attr); if (!u) { gen(done); return; }
    var im = new Image(); im.crossOrigin = 'anonymous'; im.decoding = 'async'; im.onload = function () { done(im); }; im.onerror = function () { gen(done); }; im.src = u; }

  // ---------- timeline ----------
  var A_LEN = 20, X_LEN = 4, B_LEN = 20, LOOP = A_LEN + X_LEN + B_LEN + X_LEN; // 48 s
  function sceneMix(t) { t %= LOOP; if (t < A_LEN) return 0; if (t < A_LEN + X_LEN) return sstep(0, 1, (t - A_LEN) / X_LEN);
    if (t < A_LEN + X_LEN + B_LEN) return 1; return 1 - sstep(0, 1, (t - A_LEN - X_LEN - B_LEN) / X_LEN); }
  function lift(t) { t %= LOOP; var p = -1; if (t >= A_LEN && t < A_LEN + X_LEN) p = (t - A_LEN) / X_LEN; else if (t >= LOOP - X_LEN) p = (t - LOOP + X_LEN) / X_LEN;
    return p < 0 ? 0 : Math.sin(Math.PI * p); }
  function earthRise(t) { t %= LOOP; var s = A_LEN, e = A_LEN + X_LEN + B_LEN + X_LEN * 0.5, p = (t - s) / (e - s); if (t < s) p = 0; return Math.min(1, Math.max(0, p)); }

  var SPEED = 1.15; // world units per second (camera height = 1)
  var jetSprite = null, glint = null, haze = null, TXT = [0, 0, 0, 0], TXH = [0, 0, 0, 0];
  // Oct 16 8:06 PM (user): taller, glowing, sparkling plumes that rise up through and behind the title. Science: the jets
  // leave the four south-polar "tiger stripe" fractures (~400 m/s) and merge into one broad plume that fans out and fades
  // with height. Grains drawn over the text block are dimmed (and the text has a shadow) so the title keeps >= 4.5:1.
  function drawJets(x, scroll, camH, alpha, now) {
    if (alpha <= 0.01) return;
    if (!jetSprite) { jetSprite = sprite(1.6, '200,228,255'); glint = sprite(0.9, '255,255,255');
      haze = document.createElement('canvas'); haze.width = haze.height = 64; var hg = haze.getContext('2d'), rg = hg.createRadialGradient(32, 32, 0, 32, 32, 32);
      rg.addColorStop(0, 'rgba(215,236,255,1)'); rg.addColorStop(0.45, 'rgba(205,230,255,.35)'); rg.addColorStop(1, 'rgba(200,226,255,0)'); hg.fillStyle = rg; hg.fillRect(0, 0, 64, 64); }
    var cx = W / 2, nMin = Math.floor((scroll + 4) / 3) - 1, nMax = Math.floor((scroll + 56) / 3) + 1;
    var inR = function (q, px, py) { return px > q[0] && px < q[2] && py > q[1] && py < q[3]; };
    var inT = function (px, py) { return inR(TXH, px, py) ? 0.06 : inR(TXT, px, py) ? 0.3 : 1; }; // title: plume only a whisper (coloured title >= 4.5:1)
    x.globalCompositeOperation = 'lighter';
    for (var n = nMin; n <= nMax; n++) {
      for (var m = 0; m < 2; m++) {
        if (hash(n, m) < 0.5) continue;
        var u = hash(n, m + 7), xw = (u - 0.5) * TILE * 1.6, s = ((n % 4) + 4) % 4;
        var zw = n * 3 + STRIPE_C + wob(((xw / TILE) % 1 + 1) % 1, s) * TILE - scroll; if (zw < 5 || zw > 56) continue;
        var fz = FOC / zw, bx = cx + xw * fz, by = hY + curvA * (bx - cx) * (bx - cx) + camH * fz;
        if (bx < -300 || bx > W + 300) continue;
        var big = hash(n, m + 11) > 0.55, Hj = big ? 16 + 14 * hash(n, m + 3) : 6 + 6 * hash(n, m + 3);
        // Oct 17: extend plumes so their tops meet the raised title (moons/horizon stay fixed)
        if (TXT[1] < 1e8) { var need = Math.max(0, (by - TXT[1] + 12) / Math.max(8, fz)); Hj = Math.max(Hj, need * (big ? 1.25 : 0.95)); }
        var fa = alpha * sstep(56, 40, zw) * sstep(7, 12, zw), N = Math.round((big ? 96 : 50) * QN[QL]), rate = (big ? 0.07 : 0.12) + 0.05 * hash(n, m + 5);
        // soft glowing plume: overlapping soft blobs that widen and fade with height (no hard-edged cone)
        var K = big ? 34 : 18, Hp = Hj * fz;
        for (var k = 0; k < K; k++) { var t = (k + 0.5) / K, yy = by - Math.pow(t, 0.9) * Hp, rr = Math.max(3, (0.06 + 0.32 * t) * Hj * fz * 0.5);
          var ov = function (q) { return bx + rr > q[0] && bx - rr < q[2] && yy + rr * 2 > q[1] && yy - rr * 2 < q[3]; };
          var aa = fa * (big ? 0.24 : 0.2) * Math.pow(1 - t, 1.25) * (ov(TXH) ? 0.06 : ov(TXT) ? 0.3 : 1);
          x.globalAlpha = Math.min(1, aa); x.drawImage(haze, bx - rr, yy - rr * 2, rr * 2, rr * 4); }
        for (var i = 0; i < N; i++) {
          var ph = (now * rate + i / N + hash(n * 7 + i, m)) % 1, hh = Math.pow(ph, 0.75) * Hj, sp = (hash(i, n * 3 + m) - 0.5) * 0.4 * hh;
          var px = bx + sp * fz, py = by - hh * fz; if (py < -10) continue;
          var a = fa * Math.pow(1 - ph, 1.1) * (0.7 + 0.5 * hash(i + 99, n)) * inT(px, py);
          var tw = 0.6 + 0.4 * Math.sin(now * 9 + i * 2.3 + n);                // sunlit ice grains twinkle
          var sz = Math.max(1, (0.04 + 0.07 * ph) * fz) * (0.7 + 0.6 * hash(i, m + 50));
          x.globalAlpha = Math.min(1, 1.5 * a * tw); x.drawImage(jetSprite, px - sz, py - sz, sz * 2, sz * 2);
          var gl1 = Math.sin(now * 5.3 + i * 7.1 + n * 3.7); // occasional sharp sparkle
          if (gl1 > 0.93) { var gs = Math.max(1.2, sz * 0.7); x.globalAlpha = Math.min(1, a * 1.6 * (gl1 - 0.93) / 0.07); x.drawImage(glint, px - gs, py - gs, gs * 2, gs * 2); }
        }
      }
    }
    x.globalAlpha = 1; x.globalCompositeOperation = 'source-over';
  }


  var tScene = 0, tGlide = 0, last = 0, hold = false;
  function frame(still) {
    var mixT = sceneMix(tScene), lf = lift(tScene), camH = 1 + 2.6 * lf, scroll = (tGlide * SPEED) % (TILE * 1e3);
    cSkyA.style.opacity = (1 - mixT).toFixed(3); cSkyB.style.opacity = mixT.toFixed(3); cStars.style.opacity = (1 - 0.55 * mixT).toFixed(3);
    var er = earthRise(tScene), ey = hY + EAR.R * 0.9 - er * (hY + EAR.R * 0.9 - EAR.peak), S = parseFloat(cEarth.style.width) || 0;
    cEarth.style.opacity = mixT.toFixed(3);
    cEarth.style.transform = 'translate3d(' + (EAR.x - S / 2).toFixed(1) + 'px,' + (ey - S / 2 - lf * 18).toFixed(1) + 'px,0)';
    cSkyA.style.transform = 'translate3d(0,' + (-lf * 14).toFixed(1) + 'px,0)';
    if (glOk) {
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, texA); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, texB);
      var G = cGround.width / W;
      gl.uniform2f(U.res, cGround.width, cGround.height); gl.uniform1f(U.mixT, mixT); gl.uniform1f(U.hY, hY * G); gl.uniform1f(U.f, FOC * G);
      gl.uniform1f(U.camH, camH); gl.uniform1f(U.scroll, scroll % TILE); gl.uniform1f(U.curv, (curvA + (curvB - curvA) * mixT) / G);
      gl.uniform1f(U.tile, TILE); gl.uniform1f(U.dpr, G); gl.uniform1f(U.top, gTop * G);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    var x = cFx.getContext('2d'), F = cFx.width / W; x.setTransform(F, 0, 0, F, 0, 0); x.clearRect(0, 0, W, H);
    drawJets(x, scroll, camH, (1 - mixT) * (glOk ? 1 : 0), tGlide);
    var sc = mixT < 0.5 ? 0 : 1;
    caps.forEach(function (c, i) { var on = i === sc; if (c.classList.contains('on') !== on) c.classList.toggle('on', on); });
  }

  var raf = 0, onScreen = true, nFrames = 0, ema = 0, slowT = 0, warm = 0;
  function quality(rawDt) { // rawDt in s; skip the first 2 s after (re)start (texture build, tab resume)
    if ((warm += rawDt) < 2 || QL >= 2 || /[?&]hero-poster=1/.test(location.search)) return; ema = ema ? ema * 0.9 + rawDt * 0.1 : rawDt;
    slowT = ema > 0.04 ? slowT + rawDt : 0;
    if (slowT >= 3) { QL++; slowT = 0; ema = 0;
      sizeCanvas(cGround, W, H - gTop, 0, gTop); sizeCanvas(cFx, W, H); if (glOk) gl.viewport(0, 0, cGround.width, cGround.height); } }
  function loop(now) { raf = 0; nFrames++; var raw = (now - last) / 1000, dt = Math.min(0.1, raw); last = now; tGlide += dt; quality(Math.min(raw, 0.25));
    var m = sceneMix(tScene); if (m > 0.98 && hero.classList.contains('hs-titlewait')) hero.classList.remove('hs-titlewait'); if (!hold || (m > 0 && m < 1)) tScene += dt; frame(false); if (running()) raf = requestAnimationFrame(loop); }
  function running() { return !reduced && onScreen && !document.hidden && !intro(); }
  // Oct 29 2026 (founder: Saturn intro start choppy): while the Saturn intro covers the hero the live scene is frozen (no frame
  // loop, scene clock held at the Saturn/Enceladus start) and its heavy setup waits until the intro's ring close-up is fully
  // opaque (event sp-intro-idle), so WebGL/texture work never competes with the opening rise; sp-intro-end resumes the loop.
  function intro() { return hero.classList.contains('hs-introing') && !introIdle; }
  function kick() { if (running() && !raf) { last = performance.now(); warm = 0; slowT = 0; ema = 0; raf = requestAnimationFrame(loop); } if (!running() && raf) { cancelAnimationFrame(raf); raf = 0; } }
  // Keep the current scene (and its caption) while a caption is hovered or focused, so it never vanishes under the pointer or focus.
  caps.forEach(function (c) { ['mouseenter', 'focus'].forEach(function (e) { c.addEventListener(e, function () { hold = true; }); });
    ['mouseleave', 'blur'].forEach(function (e) { c.addEventListener(e, function () { hold = false; }); }); });
  document.addEventListener('visibilitychange', kick);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { onScreen = es[0].isIntersecting; kick(); }).observe(hero);
  if (mq.addEventListener) mq.addEventListener('change', function () { reduced = mq.matches; if (reduced) { tScene = 8; frame(true); } kick(); });
  var rt = 0, lastW = 0;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () {
    var b = hero.getBoundingClientRect(); if (Math.abs(b.width - lastW) < 2 && Math.abs(b.height - H) < 80) return; // ignore iOS URL-bar jitter
    lastW = b.width; setup(); frame(true); kick(); }, 180); }, { passive: true });
  lastW = hero.getBoundingClientRect().width;
  var q = /[?&]hero-t=(\d+(?:\.\d+)?)/.exec(location.search); // preview a moment of the loop, e.g. ?hero=space&hero-t=30
  tScene = q ? +q[1] : (reduced ? 8 : 0); tGlide = tScene;
  // Oct 16 8:16 PM (Lighthouse): nothing runs before the page has loaded and the main thread is idle; until then the
  // pre-rendered poster (CSS, .hero-space::before) is the hero background, and it fades out once the live ground is ready.
  var started = false;
  // Oct 16 2026 (Lighthouse + battery): the live scene needs a hardware GPU. Where the browser would fall back to software
  // rendering (failIfMajorPerformanceCaveat) or the user asked to save data, the hi-res poster stays as the hero and no
  // frame loop runs at all. ?hero-gpu=1 forces the live scene (tests, the poster builder).
  function hwGL() { if (/[?&]hero-gpu=1/.test(location.search)) return true;
    try { var c = document.createElement('canvas'), g = c.getContext('webgl', { failIfMajorPerformanceCaveat: true }); if (!g) return false;
      var di = g.getExtension('WEBGL_debug_renderer_info'), rn = di ? String(g.getParameter(di.UNMASKED_RENDERER_WEBGL)) : '';
      var sw = /swiftshader|llvmpipe|softpipe|software|basic render/i.test(rn); // CPU rasterizers
      var x = g.getExtension('WEBGL_lose_context'); if (x) x.loseContext(); return !sw; } catch (e) { return false; } }
  var introIdle = false;
  window.addEventListener('sp-intro-idle', function () { introIdle = true; if (deferred) { deferred = false; start(); }
    // Oct 29 2026 (founder): after the intro, Earth rises first, then the title fades in (hs-titlewait cleared in loop()).
    tScene = tGlide = A_LEN - 1.5; if (started && !box.classList.contains('hs-static')) frame(true); introIdle = false; });
  window.addEventListener('sp-intro-end', function () { if (deferred) { deferred = false; start(); } kick(); });
  var deferred = false;
  function start() { if (started) return; if (hero.classList.contains('hs-introing') && !introIdle) { deferred = true; return; } started = true;
    if ((navigator.connection && navigator.connection.saveData) || !hwGL()) { box.classList.add('hs-static'); return; }
    setup(); frame(true); kick();
    setTimeout(loadBM, 2500); // Earth texture after first paint (it is first seen ~20 s into the loop)
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { var o = hY; setup(); if (hY !== o || !running()) frame(true); }); }
  function idle() { (window.requestIdleCallback || function (f) { return setTimeout(f, 50); })(start, { timeout: 2500 }); }
  if (document.readyState === 'complete') setTimeout(idle, 200); else window.addEventListener('load', function () { setTimeout(idle, 200); });
  window.addEventListener('sp-lb', function () { setTimeout(placeCaption, 50); }); // language banner shown/closed
  setTimeout(placeCaption, 1500);
  window.__heroSpace = { start: start, procTex: function (name, size, cb) { var o = T; T = size; (name === 'moon' ? moonTex : enceladusTex)(function (img) { T = o; cb(img); }); }, frames: function () { return nFrames; }, quality: function () { return { level: QL, ground: cGround.width + "x" + cGround.height, fx: cFx.width + "x" + cFx.height }; }, size: function () { return { W: W, H: H, D: D, hY: hY, gl: glOk }; },
    seek: function (t) { tScene = tGlide = t; frame(true); }, scene: function () { return sceneMix(tScene); } };
})();
