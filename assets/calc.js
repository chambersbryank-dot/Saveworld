/* Search-named calculators (Oct 16 2026). Same formulas and constants as scripts/learn_calc.py, aero_calc.py and phys_calc.py;
   checked against textbook values by scripts/calc_check.py and scripts/test-calcs.js (weekly sync). Text only, no network calls. */
(function (root) {
  var G0 = 9.80665, MU = 398600.4418, RE = 6378.137, R = 287.05287, T0 = 288.15, P0 = 101325, GAM = 1.4;
  function isa(h) { var T, p; if (h <= 11000) { T = T0 - 0.0065 * h; p = P0 * Math.pow(T / T0, G0 / (0.0065 * R)); }
    else { T = 216.65; p = P0 * Math.pow(216.65 / T0, G0 / (0.0065 * R)) * Math.exp(-G0 * (h - 11000) / (R * T)); } return { T: T, p: p, rho: p / (R * T) }; }
  function vv(r, a) { return Math.sqrt(MU * (2 / r - 1 / a)); }
  function agm(a, b) { for (var i = 0; i < 60 && Math.abs(a - b) > 1e-15; i++) { var x = (a + b) / 2; b = Math.sqrt(a * b); a = x; } return a; }
  function proj(v0, deg, m, d, cd, dt) {
    dt = dt || 0.001; var k = 0.5 * 1.225 * cd * Math.PI * d * d / 4 / m, th = deg * Math.PI / 180, s = [0, 0, v0 * Math.cos(th), v0 * Math.sin(th)], t = 0, top = 0;
    function f(q) { var v = Math.hypot(q[2], q[3]); return [q[2], q[3], -k * v * q[2], -G0 - k * v * q[3]]; }
    function add(q, a, h) { return [q[0] + h * a[0], q[1] + h * a[1], q[2] + h * a[2], q[3] + h * a[3]]; }
    for (var n = 0; n < 2e6; n++) {
      var a = f(s), b = f(add(s, a, dt / 2)), c = f(add(s, b, dt / 2)), e = f(add(s, c, dt)), nx = [];
      for (var i = 0; i < 4; i++) nx.push(s[i] + dt / 6 * (a[i] + 2 * b[i] + 2 * c[i] + e[i]));
      t += dt; top = Math.max(top, nx[1]);
      if (nx[1] < 0) { var fr = s[1] / (s[1] - nx[1]); return { range: s[0] + fr * (nx[0] - s[0]), top: top, time: t - dt + fr * dt }; }
      s = nx;
    }
    return null;
  }
  var C = {
    dv: function (x) { if (!(x.m0 > x.mf && x.mf > 0 && x.isp > 0)) return null; var mr = x.m0 / x.mf; return { dv: x.isp * G0 * Math.log(mr), mr: mr, pf: (1 - x.mf / x.m0) * 100 }; },
    hohmann: function (x) { if (!(x.h1 >= 0 && x.h2 >= 0)) return null; var r1 = RE + x.h1, r2 = RE + x.h2, at = (r1 + r2) / 2;
      var d1 = Math.abs(vv(r1, at) - Math.sqrt(MU / r1)), d2 = Math.abs(Math.sqrt(MU / r2) - vv(r2, at));
      return { dv1: d1, dv2: d2, dv: d1 + d2, tof: Math.PI * Math.sqrt(at * at * at / MU) / 3600 }; },
    period: function (x) { if (!(x.h >= 0)) return null; var a = RE + x.h, T = 2 * Math.PI * Math.sqrt(a * a * a / MU); return { tmin: T / 60, th: T / 3600, v: Math.sqrt(MU / a) }; },
    vel: function (x) { if (!(x.h >= 0)) return null; var r = RE + x.h; return { vc: Math.sqrt(MU / r), ve: Math.sqrt(2 * MU / r) }; },
    stall: function (x) { if (!(x.m > 0 && x.S > 0 && x.cl > 0 && x.alt >= 0 && x.alt <= 20000 && x.bank >= 0 && x.bank < 85)) return null;
      var rho = isa(x.alt).rho, vs = Math.sqrt(2 * x.m * G0 / (rho * x.S * x.cl)), n = 1 / Math.cos(x.bank * Math.PI / 180);
      return { rho: rho, vs: vs, kn: vs / 0.514444, kmh: vs * 3.6, n: n, vb: vs * Math.sqrt(n) }; },
    lift: function (x) { if (!(x.alt >= 0 && x.alt <= 20000 && x.V >= 0 && x.S > 0)) return null; var rho = isa(x.alt).rho, q = 0.5 * rho * x.V * x.V, L = q * x.S * x.cl;
      return { rho: rho, q: q, L: L, kg: L / G0 }; },
    mach: function (x) { if (!(x.alt >= 0 && x.alt <= 20000 && x.V >= 0)) return null; var T = isa(x.alt).T, a = Math.sqrt(GAM * R * T);
      return { T: T, TC: T - 273.15, a: a, akmh: a * 3.6, M: x.V / a }; },
    tw: function (x) { if (!(x.F > 0 && x.m > 0 && x.g > 0)) return null; var W = x.m * x.g; return { tw: x.F * 1000 / W, a: x.F * 1000 / x.m - x.g }; },
    rotor: function (x) { if (!(x.m > 0 && x.R > 0 && x.FM > 0 && x.FM <= 1 && x.alt >= 0 && x.alt <= 6000)) return null;
      var rho = isa(x.alt).rho, T = x.m * G0, A = Math.PI * x.R * x.R, vi = Math.sqrt(T / (2 * rho * A)), P = T * vi / 1000;
      return { T: T / 1000, A: A, DL: T / A, vi: vi, Pi: P, Pa: P / x.FM }; },
    proj: function (x) { if (!(x.v0 > 0 && x.v0 <= 200 && x.ang > 0 && x.ang < 90 && x.m > 0 && x.d > 0 && x.cd >= 0)) return null;
      var r = proj(x.v0, x.ang, x.m, x.d, x.cd), th = x.ang * Math.PI / 180;
      return { range: r.range, top: r.top, time: r.time, r0: x.v0 * x.v0 * Math.sin(2 * th) / G0, top0: Math.pow(x.v0 * Math.sin(th), 2) / (2 * G0) }; },
    pend: function (x) { if (!(x.L > 0 && x.a > 0 && x.a < 180)) return null; var T0 = 2 * Math.PI * Math.sqrt(x.L / G0), T = T0 / agm(1, Math.cos(x.a * Math.PI / 360));
      return { T0: T0, T: T, pct: (T / T0 - 1) * 100 }; }
  };
  var api = { C: C, isa: isa };
  if (typeof module !== 'undefined') module.exports = api;
  if (typeof document === 'undefined') return;
  var box = document.querySelector('.cx'); if (!box) return;
  var id = box.getAttribute('data-calc'), outs = box.querySelectorAll('[data-out]'), msg = box.querySelector('.cx-msg'), comma = /^(fr|es|it)/.test(document.documentElement.lang), used = false;
  function rd(v) { var s = String(v).trim().replace(/[\u0660-\u0669]/g, function (c) { return c.charCodeAt(0) - 0x660; }).replace(/\u066b/g, '.').replace(',', '.'); return s === '' ? NaN : Number(s); }
  function fmt(v, d) { var s = v.toFixed(d); if (/^-0(\.0+)?$/.test(s)) s = s.slice(1); return comma ? s.replace('.', ',') : s; }
  function run(user) {
    var x = {}; [].forEach.call(box.querySelectorAll('input[name],select[name]'), function (el) { x[el.name] = rd(el.value); });
    var r = C[id](x);
    if (!r) { msg.textContent = box.getAttribute('data-bad'); [].forEach.call(outs, function (o) { o.textContent = '\u2014'; }); return; }
    msg.textContent = '';
    [].forEach.call(outs, function (o) { var k = o.getAttribute('data-out'); o.textContent = fmt(r[k], +o.getAttribute('data-d')); });
    if (user && !used) { used = true; try { if (window.spTrack) window.spTrack('calc', { tool: id }); } catch (e) {} }
  }
  box.addEventListener('input', function () { run(true); });
  box.addEventListener('change', function () { run(true); });
  box.addEventListener('submit', function (e) { e.preventDefault(); run(true); });
  run(false);
})(this);
