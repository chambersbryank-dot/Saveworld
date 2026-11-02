/* Kids World Map. Reads assets/data/kids-world.<lang>.json. No analytics. */
(function () {
  var root = document.getElementById('kw');
  if (!root) return;
  var panel = document.getElementById('kw-panel');
  var lang = document.documentElement.lang || 'en';
  var bits = location.pathname.split('/').filter(Boolean);
  var nested = bits.length >= 2 && /^(fr|es|ar|it|he)$/.test(bits[bits.length - 2]);
  var prefix = nested ? '../' : '';
  var data = null;
  var open = null;

  function $(sel, base) { return (base || document).querySelector(sel); }
  function $all(sel) { return [].slice.call(document.querySelectorAll(sel)); }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function fail() {
    var tpl = document.querySelector('.kw-error-tpl');
    if (tpl && panel) { panel.hidden = false; panel.textContent = ''; panel.appendChild(tpl.content.cloneNode(true)); }
  }
  function setPressed(id) {
    $all('[data-region]').forEach(function (n) {
      if (!n.hasAttribute('aria-pressed')) return;
      n.setAttribute('aria-pressed', n.getAttribute('data-region') === id ? 'true' : 'false');
    });
  }
  function card(item, ui) {
    var art = el('article', 'kw-card');
    if (item.img && item.credit) {
      var img = document.createElement('img');
      img.src = prefix + item.img;
      img.alt = item.alt || '';
      if (item.w) img.width = item.w;
      if (item.h) img.height = item.h;
      img.loading = 'lazy';
      img.decoding = 'async';
      art.appendChild(img);
      var cred = el('p', 'kw-credit');
      cred.innerHTML = item.credit;
      art.appendChild(cred);
    }
    var h = el('h3');
    var a = el('a', null, item.n || item.u);
    a.href = item.u;
    h.appendChild(a);
    art.appendChild(h);
    if (item.places && item.places.length) {
      art.appendChild(el('p', 'kw-where', ui.places + ' ' + item.places.join(' · ')));
    }
    if (item.eli && item.eli.length) {
      art.appendChild(el('h4', null, ui.eli));
      var ul = document.createElement('ul');
      item.eli.forEach(function (t) { ul.appendChild(el('li', null, t)); });
      art.appendChild(ul);
    } else if (item.sum) {
      art.appendChild(el('p', null, item.sum));
    }
    if (item.src && item.src.href) {
      var p = el('p', 'kw-src');
      p.appendChild(document.createTextNode(ui.source + ' '));
      var s = el('a', null, item.src.name || item.src.href);
      s.href = item.src.href;
      s.target = '_blank';
      s.rel = 'noopener';
      p.appendChild(s);
      art.appendChild(p);
    }
    var more = el('p');
    var r = el('a', null, ui.read);
    r.href = item.u;
    more.appendChild(r);
    art.appendChild(more);
    return art;
  }
  function show(id, scroll) {
    if (!data) return;
    open = id;
    setPressed(id);
    var items = data.regions[id] || [];
    var ui = data.ui;
    panel.hidden = false;
    panel.textContent = '';
    var title = '';
    $all('.kw-pin[data-region="' + id + '"], .kw-space[data-region="' + id + '"]').forEach(function (b) { if (!title) title = b.textContent; });
    panel.appendChild(el('h2', null, title));
    panel.appendChild(el('p', 'kw-count', ui.count.replace('{n}', String(items.length))));
    if (!items.length) {
      panel.appendChild(el('p', null, ui.empty));
    } else {
      var grid = el('div', 'kw-grid');
      var first = items.slice(0, 6);
      var rest = items.slice(6);
      first.forEach(function (it) { grid.appendChild(card(it, ui)); });
      panel.appendChild(grid);
      if (rest.length) {
        var btn = el('button', 'kw-more', ui.more);
        btn.type = 'button';
        btn.setAttribute('aria-expanded', 'false');
        btn.addEventListener('click', function () {
          var on = btn.getAttribute('aria-expanded') === 'true';
          if (on) {
            rest.forEach(function (it) {
              var node = grid.querySelector('[data-u="' + CSS.escape(it.u) + '"]');
              if (node) node.remove();
            });
            btn.textContent = ui.more;
            btn.setAttribute('aria-expanded', 'false');
          } else {
            rest.forEach(function (it) {
              var node = card(it, ui);
              node.setAttribute('data-u', it.u);
              grid.appendChild(node);
            });
            btn.textContent = ui.less;
            btn.setAttribute('aria-expanded', 'true');
          }
        });
        panel.appendChild(btn);
      }
    }
    if (scroll) {
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      panel.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }
    if (history.replaceState) {
      var url = location.pathname + location.search + '#' + id;
      if (location.hash !== '#' + id) history.replaceState(null, '', url);
    }
  }
  function activate(id) { if (data && data.regions && id in data.regions) show(id, true); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-region]');
    if (!b || !root.contains(b)) return;
    activate(b.getAttribute('data-region'));
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var b = e.target.closest('path[data-region]');
    if (!b) return;
    e.preventDefault();
    activate(b.getAttribute('data-region'));
  });
  fetch(prefix + 'assets/data/kids-world.' + lang + '.json')
    .then(function (r) { if (!r.ok) throw new Error('load'); return r.json(); })
    .then(function (j) {
      data = j;
      var id = (location.hash || '').replace('#', '');
      if (id && j.regions && id in j.regions) show(id, false);
    })
    .catch(fail);
})();
