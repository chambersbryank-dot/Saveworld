/* Physics Lab (Oct 16, Learn Phase 3). Same methods as scripts/phys_calc.py; checked by scripts/test-phys-lab.js. */
(function () {
  var G0 = 9.80665, RHO = 1.225;
  function traj(v0, deg, m, d, cd, dt, keep) { dt = dt || 0.001; var k = 0.5 * RHO * cd * Math.PI * d * d / 4 / m, th = deg * Math.PI / 180;
    function f(s) { var v = Math.hypot(s[2], s[3]); return [s[2], s[3], -k * v * s[2], -G0 - k * v * s[3]]; }
    function add(s, a, h) { return [s[0] + h * a[0], s[1] + h * a[1], s[2] + h * a[2], s[3] + h * a[3]]; }
    var s = [0, 0, v0 * Math.cos(th), v0 * Math.sin(th)], t = 0, top = 0, pts = keep ? [[0, 0]] : null, n = 0;
    while (t < 600) { var a = f(s), b = f(add(s, a, dt / 2)), c = f(add(s, b, dt / 2)), e = f(add(s, c, dt));
      var nx = [0, 1, 2, 3].map(function (i) { return s[i] + dt / 6 * (a[i] + 2 * b[i] + 2 * c[i] + e[i]); }); t += dt; n++; if (nx[1] > top) top = nx[1];
      if (nx[1] < 0) { var fr = s[1] / (s[1] - nx[1]), R = s[0] + fr * (nx[0] - s[0]); if (pts) pts.push([R, 0]); return { R: R, H: top, T: t - dt + fr * dt, pts: pts }; }
      s = nx; if (pts && n % 20 === 0) pts.push([s[0], s[1]]); }
    return null; }
  function vac(v0, deg) { var th = deg * Math.PI / 180; return { R: v0 * v0 * Math.sin(2 * th) / G0, H: Math.pow(v0 * Math.sin(th), 2) / (2 * G0), T: 2 * v0 * Math.sin(th) / G0 }; }
  function osc(wn, z) { var o = { re: -z * wn }; if (z < 1) { o.im = wn * Math.sqrt(1 - z * z); o.r1 = o.r2 = o.re; } else { o.im = 0; var q = wn * Math.sqrt(z * z - 1); o.r1 = o.re + q; o.r2 = o.re - q; } return o; }
  function x_t(wn, z, t) { // x(0)=1, x'(0)=0
    if (z < 1) { var wd = wn * Math.sqrt(1 - z * z); return Math.exp(-z * wn * t) * (Math.cos(wd * t) + z * wn / wd * Math.sin(wd * t)); }
    if (z === 1) return Math.exp(-wn * t) * (1 + wn * t);
    var q = wn * Math.sqrt(z * z - 1), r1 = -z * wn + q, r2 = -z * wn - q; return (r2 * Math.exp(r1 * t) - r1 * Math.exp(r2 * t)) / (r2 - r1); }
  function agm(a, b) { while (Math.abs(a - b) > 1e-15) { var c = (a + b) / 2; b = Math.sqrt(a * b); a = c; } return a; }
  function pend(L, deg) { var T0 = 2 * Math.PI * Math.sqrt(L / G0); return { T0: T0, T: T0 / agm(1, Math.cos(deg * Math.PI / 360)) }; }
  var api = { traj: traj, vac: vac, osc: osc, x_t: x_t, pend: pend, agm: agm };
  if (typeof module !== 'undefined') module.exports = api;
  if (typeof document === 'undefined') return;
  var box = document.getElementById('ol'); if (!box) return;
  var tr = JSON.parse(box.dataset.t), comma = /^(fr|es|it)/.test(document.documentElement.lang);
  var css = getComputedStyle(document.body), fg = css.color || '#e8eefc';
  function f(v, d) { var s = v.toFixed(d); return comma ? s.replace('.', ',') : s; }
  function rd(x) { var s = String(x).trim().replace(/[\u0660-\u0669]/g, function (c) { return c.charCodeAt(0) - 0x660; }).replace(',', '.'); return s === '' ? NaN : Number(s); }
  /* numbers in <bdi dir="ltr"> so signs and "±" keep their order in Arabic */
  function put(el, t, o, plain) { el.textContent = ''; t.split(/(\{\w+\})/).forEach(function (p) { var m = /^\{(\w+)\}$/.exec(p);
    if (!m) { if (p) el.appendChild(document.createTextNode(p)); return; }
    if (plain && plain.indexOf(m[1]) >= 0) { el.appendChild(document.createTextNode(o[m[1]])); return; }
    var b = document.createElement('bdi'); b.dir = 'ltr'; b.textContent = o[m[1]]; el.appendChild(b); }); }
  function ctx(cv) { var c = cv.getContext && cv.getContext('2d'); if (!c) return null; c.fillStyle = '#050b1a'; c.fillRect(0, 0, cv.width, cv.height); return c; }
  function val(form, n) { return rd(form.elements[n].value); }
  // projectile
  var ps = document.getElementById('pl-proj'), pf = ps.querySelector('form'), po = ps.querySelector('.ol-out'), pc = ps.querySelector('canvas');
  function doProj(e) { if (e) e.preventDefault(); var v0 = val(pf, 'v0'), a = val(pf, 'ang'), m = val(pf, 'm'), d = val(pf, 'd'), cd = val(pf, 'cd');
    if (!(v0 > 0 && v0 <= 2000 && a >= 1 && a <= 89 && m > 0 && d > 0 && cd >= 0)) { po.textContent = tr.bad; return; }
    var r = traj(v0, a, m, d, cd, 0.001, true), q = vac(v0, a);
    put(po, tr.proj_out, { r: f(r.R, 1), h: f(r.H, 1), t: f(r.T, 2), r0: f(q.R, 1), h0: f(q.H, 1), t0: f(q.T, 2) });
    var c = ctx(pc); if (!c) return; var W = pc.width, H = pc.height, pad = 30, sx = (W - 2 * pad) / Math.max(q.R, r.R), sy = (H - 2 * pad) / Math.max(q.H, r.H), s = Math.min(sx, sy * 3);
    sy = Math.min(sy, s); sx = Math.min(sx, s * 3);
    c.strokeStyle = 'rgba(255,255,255,.5)'; c.lineWidth = 1; c.setLineDash([]); c.beginPath(); c.moveTo(pad, H - pad); c.lineTo(W - pad, H - pad); c.stroke();
    c.strokeStyle = '#8fd3ff'; c.setLineDash([6, 5]); c.lineWidth = 2; c.beginPath(); var th = a * Math.PI / 180;
    for (var i = 0; i <= 60; i++) { var t = q.T * i / 60, x = v0 * Math.cos(th) * t, y = v0 * Math.sin(th) * t - G0 * t * t / 2; i ? c.lineTo(pad + x * sx, H - pad - y * sy) : c.moveTo(pad + x * sx, H - pad - y * sy); } c.stroke();
    c.strokeStyle = '#ffd54a'; c.setLineDash([]); c.lineWidth = 3; c.beginPath(); r.pts.forEach(function (p, i) { i ? c.lineTo(pad + p[0] * sx, H - pad - p[1] * sy) : c.moveTo(pad + p[0] * sx, H - pad - p[1] * sy); }); c.stroke(); }
  pf.addEventListener('submit', doProj); doProj();
  // oscillator
  var os = document.getElementById('pl-osc'), of = os.querySelector('form'), oo = os.querySelector('.ol-out'), oc = os.querySelector('canvas');
  function doOsc() { var wn = val(of, 'wn'), z = val(of, 'z'); of.querySelectorAll('output').forEach(function (x) { x.textContent = f(rd(document.getElementById(x.getAttribute('for')).value), 2); });
    var o = osc(wn, z), s = o.im ? (f(o.re, 3) + ' \u00b1 ' + f(o.im, 3) + 'i') : (f(o.r1, 3) + (comma ? '; ' : ', ') + f(o.r2, 3));
    var kind = z === 0 ? tr.undamp : z < 1 ? tr.under : z === 1 ? tr.crit : tr.over; put(oo, tr.osc_out, { s: s, kind: kind }, ['kind']);
    var c = ctx(oc); if (!c) return; var W = oc.width, H = oc.height, pad = 20;
    c.strokeStyle = 'rgba(255,255,255,.5)'; c.lineWidth = 1; c.beginPath(); c.moveTo(pad, H / 2); c.lineTo(W - pad, H / 2); c.stroke();
    c.strokeStyle = '#7fdbca'; c.lineWidth = 3; c.beginPath();
    for (var i = 0; i <= 400; i++) { var t = 10 * i / 400, y = x_t(wn, z, t); i ? c.lineTo(pad + (W - 2 * pad) * i / 400, H / 2 - y * (H / 2 - pad)) : c.moveTo(pad, H / 2 - y * (H / 2 - pad)); } c.stroke(); }
  of.addEventListener('input', doOsc); doOsc();
  // pendulum
  var ns = document.getElementById('pl-pend'), nf = ns.querySelector('form'), no = ns.querySelector('.ol-out');
  function doPend(e) { if (e) e.preventDefault(); var L = val(nf, 'L'), a = val(nf, 'a');
    if (!(L > 0 && a >= 1 && a <= 179)) { no.textContent = tr.bad; return; }
    var p = pend(L, a); put(no, tr.pend_out, { t0: f(p.T0, 4), t: f(p.T, 4), pct: f((p.T / p.T0 - 1) * 100, 2) }); }
  nf.addEventListener('submit', doPend); doPend();
})();
