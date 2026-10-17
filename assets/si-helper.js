/* SI Helper pilot widget (Oct 16 2026). Sends the question to the si-helper Worker; renders text only (no HTML from the
   server) and links only to www.savingplanets.com pages, plus (when SI can't answer) the trusted outside hosts listed in data-hosts (from assets/data/trusted-sources.json).
   Topic tab: data-topic on the form, or ?topic= in the page URL (all|aero|orbit|phys), sent with the question. Turnstile (invisible) loads on first focus, not on page load. */
(function () {
  var f = document.querySelector('.si-form'); if (!f) return;
  var tr = JSON.parse(f.dataset.t), out = document.querySelector('.si-out'), q = f.querySelector('textarea'), btn = f.querySelector('button');
  var wid = null, pending = null, loaded = false;
  function loadTS() {
    if (loaded) return; loaded = true;
    window.siTsReady = function () {
      wid = window.turnstile.render(f.querySelector('.si-ts'), { sitekey: f.dataset.sitekey, size: 'invisible', execution: 'execute', appearance: 'interaction-only',
        language: f.dataset.lang, callback: function (tok) { if (pending) { var p = pending; pending = null; p(tok); } },
        'error-callback': function () { if (pending) { var p = pending; pending = null; p(''); } } });
    };
    var s = document.createElement('script'); s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=siTsReady'; s.async = true; s.defer = true; document.head.appendChild(s);
  }
  q.addEventListener('focus', loadTS, { once: true }); q.addEventListener('pointerdown', loadTS, { once: true });
  function token() { return new Promise(function (res) { var tries = 0; (function go() {
    if (wid === null) { if (++tries > 100) return res(''); return setTimeout(go, 100); }
    pending = res; window.turnstile.reset(wid); window.turnstile.execute(wid); setTimeout(function () { if (pending === res) { pending = null; res(''); } }, 15000); })(); }); }
  function topic() { var t = f.dataset.topic || new URLSearchParams(location.search).get('topic') || ''; return /^(all|aero|orbit|phys)$/.test(t) ? t : ''; }
  function el(tag, txt) { var e = document.createElement(tag); if (txt != null) e.textContent = txt; return e; }
  function show(data) {
    out.textContent = ''; var a = el('div', data.answer || ''); a.className = 'si-ans'; a.setAttribute('dir', 'auto'); out.appendChild(a);
    var hs = data.status === 'none' ? (f.dataset.hosts || '').split(' ') : [];  // trusted outside hosts (assets/data/trusted-sources.json)
    var src = (data.sources || []).filter(function (s) { var m = /^https:\/\/([^\/?#]+)[\/?#]?/.exec(s.url || ''); return m && (m[1] === 'www.savingplanets.com' || hs.indexOf(m[1]) > -1); });
    if (src.length) { out.appendChild(el('h3', data.status === 'none' ? (tr.ext || tr.src) : tr.src)); var ol = el('ol'); src.forEach(function (s) { var li = el('li'), x = el('a', s.title || s.url); x.href = s.url; li.appendChild(x); ol.appendChild(li); if (!/^https:\/\/www\.savingplanets\.com\//.test(s.url)) { x.rel = 'noopener'; x.target = '_blank'; } }); out.appendChild(ol); }
  }
  f.addEventListener('submit', function (e) {
    e.preventDefault(); var text = q.value.replace(/\s+/g, ' ').trim();
    if (text.length < 3 || text.length > 400) { out.textContent = tr.short; return; }
    loadTS(); btn.disabled = true; out.textContent = tr.wait;
    token().then(function (ts) {
      return fetch(f.dataset.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ q: text, lang: f.dataset.lang, ts: ts, topic: topic() }) });
    }).then(function (r) { return r.json(); }).then(show).catch(function () { out.textContent = tr.neterr; }).then(function () { btn.disabled = false; });
  });
})();
