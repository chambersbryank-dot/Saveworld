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
