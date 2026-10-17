/* Learn pages (Oct 16 2026): auto-checked numeric practice (accepts "." or ","; relative tolerance), progressive hints,
   multiple-choice "Check your understanding" with feedback. Strings come from data-* attributes (all 5 languages). */
(function () {
  'use strict';
  function parse(s) { s = String(s).trim().replace(/\s|\u202f|\u00a0/g, '').replace(/[\u0660-\u0669]/g, function (c) { return c.charCodeAt(0) - 0x660; });
    if (/^-?\d+,\d+$/.test(s)) s = s.replace(',', '.'); else s = s.replace(/,/g, ''); return s === '' ? NaN : Number(s); }
  document.addEventListener('DOMContentLoaded', function () {
    [].forEach.call(document.querySelectorAll('.lnp'), function (b) {
      var inp = b.querySelector('input'), out = b.querySelector('.lnp-fb'), ans = +b.dataset.ans, tol = +b.dataset.tol;
      b.querySelector('.lnp-check').addEventListener('click', function () {
        var v = parse(inp.value);
        if (isNaN(v)) { out.textContent = b.dataset.nan; out.className = 'lnp-fb'; return; }
        var ok = Math.abs(v - ans) <= Math.abs(ans) * tol; out.textContent = ok ? b.dataset.ok : b.dataset.no; out.className = 'lnp-fb ' + (ok ? 'is-ok' : 'is-no');
        inp.setAttribute('aria-invalid', ok ? 'false' : 'true');
      });
      inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); b.querySelector('.lnp-check').click(); } });
      var hb = b.querySelector('.lnp-hint'), hs = b.querySelectorAll('.lnp-hints li'), shown = 0;
      if (hb) hb.addEventListener('click', function () { if (shown < hs.length) { hs[shown].hidden = false; shown++; } if (shown >= hs.length) hb.disabled = true; });
    });
    [].forEach.call(document.querySelectorAll('.lmcq'), function (q) {
      q.querySelector('button').addEventListener('click', function () {
        var c = q.querySelector('input:checked'), fb = q.querySelector('.lnp-fb');
        if (!c) return; var ok = c.value === q.dataset.ans;
        fb.textContent = (ok ? q.dataset.ok : q.dataset.no) + ' ' + q.dataset.why; fb.className = 'lnp-fb ' + (ok ? 'is-ok' : 'is-no');
      });
    });
  });
})();
/* Kepler stepper + Hohmann calculator (same constants as scripts/learn_calc.py) */
(function () {
  'use strict';
  var MU = 398600.4418, RE = 6378.137;
  function num(s) { s = String(s).trim().replace(',', '.'); return s === '' ? NaN : Number(s); }
  document.addEventListener('DOMContentLoaded', function () {
    var lang = document.documentElement.lang || 'en';
    var nf = function (x, d) { return new Intl.NumberFormat(lang === 'ar' ? 'en' : lang, { minimumFractionDigits: d, maximumFractionDigits: d }).format(x); };
    var k = document.querySelector('.wk'); if (k) {
      var tb = k.querySelector('tbody'), out = k.querySelector('.lnp-fb'), E = null, n = 0, done = false;
      var reset = function () { E = null; n = 0; done = false; tb.innerHTML = ''; out.textContent = ''; };
      k.querySelector('.wk-step').addEventListener('click', function () {
        var M = num(k.querySelector('[name=M]').value), e = num(k.querySelector('[name=e]').value);
        if (!(e >= 0 && e < 1) || isNaN(M)) { out.textContent = k.dataset.bad; return; }
        if (done) return; if (E === null) E = e > 0.8 ? Math.PI : M;
        var dE = (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E)); E -= dE; n++;
        tb.insertAdjacentHTML('beforeend', '<tr><td>' + n + '</td><td>' + E.toFixed(10) + '</td><td>' + Math.abs(dE).toExponential(2) + '</td></tr>');
        out.textContent = 'E = ' + E.toFixed(10) + ' rad'; if (Math.abs(dE) < 1e-10 || n > 40) { done = true; out.textContent += ' \u2014 ' + k.dataset.done; }
      });
      k.querySelector('.wk-reset').addEventListener('click', reset);
      [].forEach.call(k.querySelectorAll('input'), function (i) { i.addEventListener('input', reset); });
    }
    var h = document.querySelector('.wh'); if (h) {
      h.querySelector('button').addEventListener('click', function () {
        var a1 = num(h.querySelector('[name=h1]').value), a2 = num(h.querySelector('[name=h2]').value), o = h.querySelector('.lnp-fb');
        if (!(a1 >= 160 && a1 <= 400000 && a2 >= 160 && a2 <= 400000)) { o.textContent = h.dataset.bad; return; }
        var r1 = RE + a1, r2 = RE + a2, at = (r1 + r2) / 2, vv = function (r) { return Math.sqrt(MU * (2 / r - 1 / at)); };
        var d1 = Math.abs(vv(r1) - Math.sqrt(MU / r1)), d2 = Math.abs(Math.sqrt(MU / r2) - vv(r2)), t = Math.PI * Math.sqrt(at * at * at / MU) / 3600;
        o.textContent = h.dataset.res.replace('{a}', nf(d1, 4)).replace('{b}', nf(d2, 4)).replace('{c}', nf(d1 + d2, 4)).replace('{t}', nf(t, 2));
      });
    }
  });
})();
