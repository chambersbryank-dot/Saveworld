/* Earth satellite explorer. Data: assets/data/satellite-levels.<lang>.json. No analytics. */
(function () {
  var root = document.getElementById('se');
  if (!root) return;
  var list = document.getElementById('se-list');
  var detail = document.getElementById('se-detail');
  var lang = document.documentElement.lang || 'en';
  var bits = location.pathname.split('/').filter(Boolean);
  var nested = bits.length >= 2 && /^(fr|es|ar|it|he)$/.test(bits[bits.length - 2]);
  var data = null, current = null;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function level() {
    var r = document.querySelector('input[name="se-level"]:checked');
    return r ? r.value : 'k3';
  }
  function blocks(items, host) {
    (items || []).forEach(function (b) {
      if (b.t) host.appendChild(el('p', null, b.t));
      if (b.href) {
        var p = el('p', 'se-src');
        p.appendChild(document.createTextNode(data.ui.source + ' '));
        var a = el('a', null, b.name || b.href);
        a.href = b.href; a.target = '_blank'; a.rel = 'noopener';
        p.appendChild(a);
        host.appendChild(p);
      }
    });
  }
  function section(title, items) {
    if (!items || !items.length) return;
    detail.appendChild(el('h3', null, title));
    blocks(items, detail);
  }
  function show(id) {
    current = id;
    var sat = null;
    data.sats.forEach(function (s) { if (s.u === id) sat = s; });
    if (!sat) return;
    [].forEach.call(list.querySelectorAll('.se-sat'), function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-u') === id ? 'true' : 'false');
    });
    var ui = data.ui, lv = level();
    detail.hidden = false;
    detail.textContent = '';
    detail.appendChild(el('h2', null, sat.n));
    if (sat.img && sat.credit) {
      var img = document.createElement('img');
      img.src = /^https?:/.test(sat.img) ? sat.img : (nested ? '../' : '') + sat.img;
      img.alt = sat.alt || '';
      if (sat.w) img.width = sat.w;
      if (sat.h) img.height = sat.h;
      img.decoding = 'async';
      detail.appendChild(img);
      var cred = el('p', 'se-credit');
      cred.innerHTML = sat.credit;
      detail.appendChild(cred);
    }
    if (lv === 'k3') section(ui.eli, sat.k3);
    if (lv === 'mid' || lv === 'uni') {
      section(ui.what, sat.what);
      section(ui.why, sat.why);
    }
    if (lv === 'uni') section(ui.impact, sat.impact);
    var more = el('p');
    var a = el('a', null, ui.read);
    a.href = sat.u;
    more.appendChild(a);
    detail.appendChild(more);
    if (history.replaceState) {
      var url = new URL(location.href);
      url.searchParams.set('sat', id);
      url.searchParams.set('level', lv);
      history.replaceState(null, '', url);
    }
  }
  function fail() {
    var tpl = document.querySelector('.se-error-tpl');
    if (tpl) { detail.hidden = false; detail.textContent = ''; detail.appendChild(tpl.content.cloneNode(true)); }
  }
  fetch((nested ? '../' : '') + 'assets/data/satellite-levels.' + lang + '.json')
    .then(function (r) { if (!r.ok) throw new Error('load'); return r.json(); })
    .then(function (j) {
      data = j;
      var q = new URLSearchParams(location.search);
      if (q.get('level')) {
        var radio = document.querySelector('input[name="se-level"][value="' + q.get('level') + '"]');
        if (radio) radio.checked = true;
      }
      j.sats.forEach(function (s) {
        var b = el('button', 'se-sat', s.n);
        b.type = 'button';
        b.setAttribute('data-u', s.u);
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () { show(s.u); });
        list.appendChild(b);
      });
      document.querySelectorAll('input[name="se-level"]').forEach(function (r) {
        r.addEventListener('change', function () { if (current) show(current); });
      });
      var start = q.get('sat');
      if (!start || !j.sats.some(function (s) { return s.u === start; })) start = j.sats[0] && j.sats[0].u;
      if (start) show(start);
    })
    .catch(fail);
})();
