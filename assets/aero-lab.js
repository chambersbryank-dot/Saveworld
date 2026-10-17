/* Aero Lab (Oct 16, Learn Phase 2). Same formulas as scripts/aero_calc.py; checked by scripts/test-aero-lab.js. */
(function (root) {
  var G0 = 9.80665, R = 287.053, T0 = 288.15, P0 = 101325, GAM = 1.4;
  function isa(h) { var T, p; if (h <= 11000) { T = T0 - 0.0065 * h; p = P0 * Math.pow(T / T0, G0 / (0.0065 * R)); }
    else { T = 216.65; p = P0 * Math.pow(216.65 / T0, G0 / (0.0065 * R)) * Math.exp(-G0 * (h - 11000) / (R * T)); } return { T: T, p: p, rho: p / (R * T) }; }
  function stall(m, S, cl, rho) { return Math.sqrt(2 * m * G0 / (rho * S * cl)); }
  function sp(ZaV, Mq, Mad, Ma) { var b = -(ZaV + Mq + Mad), c = ZaV * Mq - Ma, disc = b * b - 4 * c, re = -b / 2;
    var o = { b: b, c: c, re: re }; if (disc < 0) { o.im = Math.sqrt(-disc) / 2; o.r1 = re; o.r2 = re; } else { o.im = 0; o.r1 = re + Math.sqrt(disc) / 2; o.r2 = re - Math.sqrt(disc) / 2; }
    if (c > 0) { o.wn = Math.sqrt(c); o.z = b / (2 * o.wn); } return o; }
  function hover(m, Rr, FM, rho) { rho = rho || 1.225; var T = m * G0, A = Math.PI * Rr * Rr, vi = Math.sqrt(T / (2 * rho * A)), P = T * vi;
    return { T: T, A: A, DL: T / A, vi: vi, Pi: P / 1000, Pa: P / 1000 / FM }; }
  var api = { isa: isa, stall: stall, sp: sp, hover: hover };
  if (typeof module !== 'undefined') module.exports = api;
  if (typeof document === 'undefined') return;
  var box = document.getElementById('ol'); if (!box) return;
  var tr = JSON.parse(box.dataset.t), comma = /^(fr|es|it)/.test(document.documentElement.lang);
  function f(v, d) { var s = v.toFixed(d); return comma ? s.replace('.', ',') : s; }
  function rd(x) { var s = String(x).trim().replace(/[\u0660-\u0669]/g, function (c) { return c.charCodeAt(0) - 0x660; }).replace(',', '.'); return s === '' ? NaN : Number(s); }
  function fmt(t, o) { return t.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }
  function val(form, n) { return rd(form.elements[n].value); }
  var st = box.querySelector('#al-stall'), sf = st.querySelector('form'), so = st.querySelector('.ol-out');
  function doStall(e) { if (e) e.preventDefault(); var h = val(sf, 'alt'), m = val(sf, 'm'), S = val(sf, 'S'), cl = val(sf, 'cl');
    if (!(h >= 0 && h <= 20000 && m > 0 && S > 0 && cl > 0)) { so.textContent = tr.bad; return; }
    var a = isa(h), v = stall(m, S, cl, a.rho); so.textContent = fmt(tr.stall_out, { T: f(a.T, 2), rho: f(a.rho, 4), vs: f(v, 2), kn: f(v / 0.514444, 1) }); }
  sf.addEventListener('submit', doStall); doStall();
  var ss = box.querySelector('#al-sp'), spf = ss.querySelector('form'), spo = ss.querySelector('.ol-out'), cv = ss.querySelector('canvas');
  function draw(o) { var c = cv.getContext && cv.getContext('2d'); if (!c) return; var W = cv.width, H = cv.height, cx = W * 0.7, cy = H / 2, k = 40;
    c.fillStyle = '#050b1a'; c.fillRect(0, 0, W, H);
    c.fillStyle = 'rgba(124,252,152,.18)';
    var a1 = Math.acos(0.35); c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx - 400 * Math.cos(a1), cy - 400 * Math.sin(a1)); c.lineTo(cx - 400, cy); c.lineTo(cx - 400 * Math.cos(a1), cy + 400 * Math.sin(a1)); c.closePath(); c.fill();
    c.strokeStyle = 'rgba(255,255,255,.5)'; c.lineWidth = 1; c.beginPath(); c.moveTo(0, cy); c.lineTo(W, cy); c.moveTo(cx, 0); c.lineTo(cx, H); c.stroke();
    c.fillStyle = '#e8eefc'; c.font = '14px sans-serif'; c.fillText('Re', W - 28, cy - 6); c.fillText('Im', cx + 6, 16);
    c.fillStyle = '#ffd54a'; [[o.r1, o.im], [o.r2, -o.im]].forEach(function (p) { var x = cx + p[0] * k, y = cy - p[1] * k; c.beginPath(); c.moveTo(x - 7, y - 7); c.lineTo(x + 7, y + 7); c.moveTo(x + 7, y - 7); c.lineTo(x - 7, y + 7); c.strokeStyle = '#ffd54a'; c.lineWidth = 3; c.stroke(); }); }
  function doSp() { var Ma = val(spf, 'Ma'), Mq = val(spf, 'Mq'); spf.querySelectorAll('output').forEach(function (x) { x.textContent = f(rd(document.getElementById(x.getAttribute('for')).value), 1); });
    var o = sp(-1.0, Mq, -0.3, Ma), s = o.im ? (f(o.re, 3) + ' \u00b1 ' + f(o.im, 3) + 'i') : (f(o.r1, 3) + ', ' + f(o.r2, 3));
    var unstable = o.r1 > 0 || o.r2 > 0 || !(o.c > 0);
    var lvl = unstable ? tr.unst : (o.z >= 0.35 && o.z <= 1.3 ? tr.lvl1 : tr.lvlx);
    spo.textContent = fmt(tr.sp_out, { s: s, wn: o.wn ? f(o.wn, 3) : '\u2014', z: o.wn ? f(o.z, 3) : '\u2014', lvl: lvl }); draw(o); }
  spf.addEventListener('input', doSp); doSp();
  var rs = box.querySelector('#al-rot'), rf = rs.querySelector('form'), ro = rs.querySelector('.ol-out');
  function doRot() { rf.querySelectorAll('output').forEach(function (x) { var i = document.getElementById(x.getAttribute('for')); x.textContent = f(rd(i.value), i.step < 1 ? 2 : 0); });
    var o = hover(val(rf, 'm'), val(rf, 'R'), val(rf, 'FM')); ro.textContent = fmt(tr.rot_out, { dl: f(o.DL, 0), vi: f(o.vi, 2), pi: f(o.Pi, 1), pa: f(o.Pa, 1) }); }
  rf.addEventListener('input', doRot); doRot();
})(this);
