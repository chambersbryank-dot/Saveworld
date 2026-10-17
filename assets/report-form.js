/* Oct 16 2026: "Report a correction" form (Corrections page, 5 languages). Sends page + what's wrong + optional fix to the
   si-helper Worker /report, which emails the site inbox. No name/email fields; emails/phone numbers are refused; nothing stored.
   Turnstile (invisible) loads on first focus. Text only is rendered. */
(function () {
  var f = document.querySelector('.rf-form'); if (!f) return;
  var tr = JSON.parse(f.dataset.t), out = f.querySelector('.rf-out'), btn = f.querySelector('button[type=submit]');
  var pg = f.querySelector('[name=page]'), what = f.querySelector('[name=what]'), fix = f.querySelector('[name=fix]');
  try { var qp = new URLSearchParams(location.search).get('page'); if (qp && /^https:\/\/(www\.)?savingplanets\.com\//.test(qp)) pg.value = qp.slice(0, 200);
    else if (document.referrer && /^https:\/\/(www\.)?savingplanets\.com\//.test(document.referrer)) pg.value = document.referrer.split('?')[0].slice(0, 200); } catch (e) {}
  var PII = /[^\s@]+@[^\s@]+\.[a-z]{2,}|(?:\+?\d[\s.\-()]*){9,}/i;
  var wid = null, pending = null, loaded = false;
  function loadTS() {
    if (loaded) return; loaded = true;
    window.rfTsReady = function () {
      wid = window.turnstile.render(f.querySelector('.rf-ts'), { sitekey: f.dataset.sitekey, size: 'invisible', execution: 'execute', appearance: 'interaction-only', language: f.dataset.lang,
        callback: function (t) { if (pending) { var p = pending; pending = null; p(t); } }, 'error-callback': function () { if (pending) { var p = pending; pending = null; p(''); } } });
    };
    var s = document.createElement('script'); s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=rfTsReady'; s.async = true; document.head.appendChild(s);
  }
  [what, fix, pg].forEach(function (x) { x.addEventListener('focus', loadTS, { once: true }); x.addEventListener('pointerdown', loadTS, { once: true }); });
  function token() { return new Promise(function (res) { var n = 0; (function go() { if (wid === null) { if (++n > 100) return res(''); return setTimeout(go, 100); }
    pending = res; window.turnstile.reset(wid); window.turnstile.execute(wid); setTimeout(function () { if (pending === res) { pending = null; res(''); } }, 15000); })(); }); }
  function say(k, ok) { out.textContent = tr[k] || tr.error; out.className = 'rf-out ' + (ok ? 'rf-ok' : 'rf-err'); }
  f.addEventListener('submit', function (e) {
    e.preventDefault(); var w = what.value.trim(), x = fix.value.trim();
    if (w.length < 10) { what.setAttribute('aria-invalid', 'true'); what.focus(); return say('short'); }
    if (PII.test(w) || PII.test(x)) { return say('pii'); }
    what.removeAttribute('aria-invalid'); loadTS(); btn.disabled = true; out.className = 'rf-out'; out.textContent = tr.wait;
    token().then(function (ts) { return fetch(f.dataset.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ page: pg.value.trim(), what: w, fix: x, lang: f.dataset.lang, ts: ts }) }); })
      .then(function (r) { return r.json(); }).then(function (d) { var ok = d && d.status === 'ok'; say(ok ? 'ok' : (d && d.status) || 'error', ok); if (ok) { what.value = ''; fix.value = ''; } })
      .catch(function () { say('neterr'); }).then(function () { btn.disabled = false; });
  });
})();
