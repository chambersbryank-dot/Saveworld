/* Earth-centered orbit diagram. Rings follow NASA's LEO / MEO / GEO / HEO order and are not to scale.
   Markers show the orbit type, not a live position. Latest images come from NASA's public image library.
   Follow state stays in localStorage on this browser. No account and no tracker. */
(function () {
  var root = document.querySelector('.sat-view');
  var stage = document.getElementById('sat-stage');
  var card = document.getElementById('sat-card');
  var list = document.getElementById('sat-list-ul');
  if (!root || !stage || !card) return;
  var STORE = 'sp-sat-follow';
  var rtl = (document.documentElement.getAttribute('dir') || '') === 'rtl';
  var SAT = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="6.2" y="6.2" width="3.6" height="3.6" rx=".4" fill="#fff"/><rect x="1" y="7" width="4.2" height="2" rx=".3" fill="#fff"/><rect x="10.8" y="7" width="4.2" height="2" rx=".3" fill="#fff"/></svg>';
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function db() { try { return JSON.parse(localStorage.getItem(STORE) || '{}'); } catch (e) { return {}; } }
  function save(o) { try { localStorage.setItem(STORE, JSON.stringify(o)); } catch (e) {} }
  fetch(root.getAttribute('data-src'), { credentials: 'omit' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(boot).catch(function () {
    stage.innerHTML = '<p class="wm-err">The orbit view could not load. The mission list below still works when data is available.</p>';
  });
  function boot(D) {
    var ui = D.ui || {}, sats = D.sats || [], byId = {}, mode = 'near', cat = 'all', lastBtn = null;
    sats.forEach(function (s) { byId[s.id] = s; });
    var earth = root.getAttribute('data-earth');
    var earthLg = root.getAttribute('data-earth-lg') || earth;
    var moon = root.getAttribute('data-moon') || '';
    var pre = (root.getAttribute('data-src') || '').indexOf('../') === 0 ? '../' : '';
    function show(s) {
      if (cat === 'all') return true;
      if (cat === 'lagrange') return s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5';
      if (cat === 'beyond') return s.regime === 'cruise';
      return s.fn === cat;
    }
    function ringOf(s) {
      if (s.regime === 'sso' || s.regime === 'leo') return 'leo';
      if (s.regime === 'meo' || s.regime === 'geo' || s.regime === 'heo') return s.regime;
      return '';
    }
    function layout(which) {
      var groups = { leo: [], meo: [], geo: [], heo: [], l1: [], l2: [], l5: [], cruise: [], note: [] };
      sats.forEach(function (s) { if (show(s) && groups[s.regime === 'sso' ? 'leo' : s.regime]) groups[s.regime === 'sso' ? 'leo' : s.regime].push(s); });
      var W = 900, H = 520, pts = [];
      function onEllipse(list, cx, cy, rx, ry) {
        var n = list.length;
        list.forEach(function (s, i) {
          var a = -Math.PI / 2 + (i + 0.5) * (2 * Math.PI) / Math.max(n, 1);
          pts.push({ s: s, x: cx + rx * Math.cos(a), y: cy + ry * Math.sin(a) });
        });
      }
      function stack(list, x, y0, gap) {
        var n = list.length, top = y0 - ((n - 1) * gap) / 2;
        list.forEach(function (s, i) { pts.push({ s: s, x: x, y: top + i * gap }); });
      }
      var svg;
      if (which === 'near') {
        var cx = 400, cy = 268;
        onEllipse(groups.leo, cx, cy, 118, 50);
        onEllipse(groups.meo, cx, cy, 178, 74);
        onEllipse(groups.geo, cx, cy, 246, 102);
        onEllipse(groups.heo, cx + 40, cy, 196, 118);
        stack(groups.note, 70, 470, 28);
        svg = '<svg class="orb-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(ui.diagram || '') + '">' +
          '<defs><clipPath id="earth-disc"><circle cx="400" cy="268" r="72"/></clipPath></defs>' +
          '<ellipse cx="400" cy="268" rx="118" ry="50" fill="none" stroke="rgba(186,224,255,.75)" stroke-width="1.4"/>' +
          '<ellipse cx="400" cy="268" rx="178" ry="74" fill="none" stroke="rgba(186,224,255,.55)" stroke-width="1.4"/>' +
          '<ellipse cx="400" cy="268" rx="246" ry="102" fill="none" stroke="rgba(186,224,255,.45)" stroke-width="1.4"/>' +
          '<ellipse cx="440" cy="268" rx="196" ry="118" fill="none" stroke="rgba(255,214,120,.7)" stroke-width="1.4" stroke-dasharray="5 4"/>' +
          '<image href="' + esc(earth) + '" x="328" y="196" width="144" height="144" clip-path="url(#earth-disc)"/>' +
          '<text x="528" y="230" fill="#d7ecff" font-size="13">' + esc(ui.leo) + '</text>' +
          '<text x="588" y="200" fill="#d7ecff" font-size="13">' + esc(ui.meo) + '</text>' +
          '<text x="656" y="168" fill="#d7ecff" font-size="13">' + esc(ui.geo) + '</text>' +
          '<text x="640" y="400" fill="#ffe3a3" font-size="13">' + esc(ui.heo) + '</text>' +
          '</svg>';
      } else {
        W = 1000; H = 640;
        var EX = 620, EY = 330, ER = 108;
        onEllipse(groups.leo.concat(groups.meo, groups.geo, groups.heo), EX, EY, 150, 58);
        stack(groups.l1, 250, 155, 28);
        stack(groups.l2, 900, 155, 28);
        stack(groups.cruise, 900, 470, 30);
        function lab(x, y, title, dist) {
          return '<text x="' + x + '" y="' + y + '" fill="#fff" font-size="15" font-weight="700">' + esc(title) + '</text>' +
            '<text x="' + x + '" y="' + (y + 16) + '" fill="#d7ecff" font-size="11">' + esc(dist) + '</text>';
        }
        svg = '<svg class="orb-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(ui.farDiagram || '') + '">' +
          '<defs>' +
          '<radialGradient id="atmo" cx="50%" cy="50%" r="50%"><stop offset="68%" stop-color="rgba(150,200,255,0)"/><stop offset="80%" stop-color="rgba(150,205,255,.55)"/><stop offset="100%" stop-color="rgba(80,150,255,0)"/></radialGradient>' +
          '<radialGradient id="sunball" cx="40%" cy="40%" r="60%"><stop offset="0%" stop-color="#fff6d0"/><stop offset="55%" stop-color="#ffb020"/><stop offset="100%" stop-color="#c45a00"/></radialGradient>' +
          '<clipPath id="earth-far"><circle cx="' + EX + '" cy="' + EY + '" r="' + ER + '"/></clipPath>' +
          '<clipPath id="moon-far"><circle cx="790" cy="230" r="18"/></clipPath>' +
          '</defs>' +
          '<circle cx="' + EX + '" cy="' + EY + '" r="138" fill="url(#atmo)"/>' +
          '<path d="M120 80 Q 400 40 620 330 Q 400 600 120 560" fill="none" stroke="rgba(186,224,255,.28)" stroke-dasharray="3 6"/>' +
          '<circle cx="78" cy="330" r="26" fill="url(#sunball)"/>' +
          '<text x="78" y="372" text-anchor="middle" fill="#ffe3a3" font-size="12">' + esc(ui.sunNote) + '</text>' +
          '<image href="' + esc(earthLg) + '" x="' + (EX - ER) + '" y="' + (EY - ER) + '" width="' + (ER * 2) + '" height="' + (ER * 2) + '" clip-path="url(#earth-far)"/>' +
          (moon ? '<image href="' + esc(moon) + '" x="772" y="212" width="36" height="36" clip-path="url(#moon-far)"/><text x="790" y="206" text-anchor="middle" fill="#d7ecff" font-size="11">' + esc(ui.moonNote) + '</text>' : '') +
          lab(300, 400, ui.l1, ui.dL12) +
          lab(760, 400, ui.l2, ui.dL12) +
          lab(78, 120, ui.l3, ui.dL3) +
          lab(400, 70, ui.l4, ui.dL4) +
          lab(400, 590, ui.l5, ui.dL5) +
          '<text x="500" y="24" text-anchor="middle" fill="#9fb8cc" font-size="12">' + esc(ui.notScale) + '</text>' +
          '</svg>';
      }
      stage.innerHTML = svg;
      var mem = db();
      pts.forEach(function (p) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'orb-btn' + (mem[p.s.id] && mem[p.s.id].on && mem[p.s.id].latest && mem[p.s.id].latest > (mem[p.s.id].seen || '') ? ' is-new' : '');
        b.style.left = (p.x / W * 100) + '%';
        b.style.top = (p.y / H * 100) + '%';
        b.innerHTML = SAT;
        b.setAttribute('data-id', p.s.id);
        b.id = 'sat-' + p.s.id;
        b.setAttribute('aria-label', p.s.name + '. ' + (ui.rep || ''));
        b.addEventListener('click', function () { openCard(p.s, b); });
        stage.appendChild(b);
      });
    }
    function openCard(s, btn) {
      lastBtn = btn || lastBtn;
      var mem = db();
      if (!mem[s.id]) mem[s.id] = {};
      root.querySelector('.sat-layout').classList.add('has-card');
      card.hidden = false;
      var site = s.page ? '<a href="' + esc(s.page) + '">' + esc(ui.site) + '</a>' : '';
      var official = s.official ? '<a href="' + esc(s.official) + '" rel="noopener">' + esc(ui.official) + '</a>' : '';
      var feed = s.feed ? '<a href="' + esc(s.feed) + '" rel="noopener">' + esc(ui.feed) + '</a>' : '';
      var dsn = s.dsn ? '<p><a href="https://eyes.nasa.gov/apps/dsn-now/" rel="noopener">' + esc(ui.dsn) + '</a> ' + esc(ui.dsnNote) + '</p>' : '';
      var plus = s.nasaPlus ? '<p><a href="https://plus.nasa.gov/" rel="noopener">' + esc(ui.plus) + '</a> ' + esc(ui.plusNote) + '</p>' : '';
      var on = mem[s.id] && mem[s.id].on;
      var photo = '';
      if (s.photo) {
        var b = pre + s.photo;
        photo = '<picture><source type="image/webp" srcset="' + esc(b) + '-480.webp 480w, ' + esc(b) + '-800.webp 800w" sizes="(max-width: 800px) 92vw, 300px">' +
          '<img src="' + esc(b) + '-800.jpg" alt="" width="800" height="450" loading="lazy" decoding="async"></picture>' +
          '<p class="sat-photo-credit">' + esc(s.credit || '') + '</p>';
      }
      card.innerHTML = '<button type="button" class="sat-close">' + esc(ui.close) + '</button>' +
        photo +
        '<h3 id="sat-card-title">' + esc(s.name) + '</h3>' +
        '<p>' + esc(ui.rep) + '</p>' +
        (s.agency ? '<p><span class="sat-k">' + esc(ui.agency) + '</span> ' + esc(s.agency) + '</p>' : '') +
        (s.orbit ? '<p><span class="sat-k">' + esc(ui.orbit) + '</span> ' + esc(s.orbit) + (s.when ? ' · ' + esc(s.when) : '') + '</p>' : '') +
        '<p><span class="sat-k">' + esc(ui.does) + '</span> ' + esc(s.does) + '</p>' +
        '<p class="sat-src">' + esc(s.source || '') + '</p>' +
        '<p class="sat-latest">' + esc(ui.latestWait) + '</p>' +
        '<p>' + [site, official, feed].filter(Boolean).join(' · ') + '</p>' + dsn + plus +
        '<p><button type="button" class="sat-follow" aria-pressed="' + (on ? 'true' : 'false') + '">' + esc(on ? ui.following : ui.follow) + '</button></p>';
      card.querySelector('.sat-close').addEventListener('click', closeCard);
      card.querySelector('.sat-follow').addEventListener('click', function () {
        var m = db(); if (!m[s.id]) m[s.id] = {};
        m[s.id].on = !m[s.id].on;
        if (m[s.id].on) m[s.id].seen = m[s.id].latest || new Date().toISOString();
        save(m);
        this.setAttribute('aria-pressed', m[s.id].on ? 'true' : 'false');
        this.textContent = m[s.id].on ? ui.following : ui.follow;
        draw();
      });
      card.querySelector('.sat-close').focus();
      var box = card.querySelector('.sat-latest');
      if (!s.imageQ) { box.textContent = ui.latestFail; return; }
      fetch('https://images-api.nasa.gov/search?media_type=image&q=' + encodeURIComponent(s.imageQ), { credentials: 'omit' })
        .then(function (r) { if (!r.ok) throw 0; return r.json(); })
        .then(function (j) {
          var item = (((j.collection || {}).items) || [])[0];
          if (!item) throw 0;
          var data = (item.data || [])[0] || {};
          var href = ((item.links || [])[0] || {}).href || '';
          var title = data.title || '';
          if (s.imageMust && title.toLowerCase().indexOf(s.imageMust) === -1) throw 0;
          var day = (data.date_created || '').slice(0, 10);
          box.innerHTML = '<span class="sat-k">' + esc(ui.latest) + '</span> ' + esc(title) + (day ? ' (' + esc(day) + ')' : '') +
            (href ? '<img alt="" width="320" height="180" loading="lazy" src="' + esc(href) + '">' : '');
          var m = db(); if (m[s.id] && m[s.id].on) { m[s.id].latest = data.date_created || ''; m[s.id].seen = m[s.id].latest; save(m); }
        })
        .catch(function () { box.textContent = ui.latestFail; });
    }
    function closeCard() {
      card.hidden = true;
      card.innerHTML = '';
      root.querySelector('.sat-layout').classList.remove('has-card');
      if (lastBtn && lastBtn.focus) lastBtn.focus();
    }
    function draw() {
      mode = (cat === 'lagrange' || cat === 'beyond' || cat === 'science') ? 'far' : 'near';
      layout(mode);
    }
    function setCat(next) {
      cat = next;
      [].forEach.call(root.querySelectorAll('button.wm-cat'), function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-cat') === next ? 'true' : 'false');
      });
      draw();
    }
    [].forEach.call(root.querySelectorAll('button.wm-cat'), function (b, i, all) {
      b.addEventListener('click', function () { setCat(b.getAttribute('data-cat')); });
      b.addEventListener('keydown', function (e) {
        var dir = e.key === 'ArrowDown' ? 1 : e.key === 'ArrowUp' ? -1 : e.key === 'ArrowRight' ? (rtl ? -1 : 1) : e.key === 'ArrowLeft' ? (rtl ? 1 : -1) : 0;
        if (!dir) return;
        e.preventDefault();
        all[(i + dir + all.length) % all.length].focus();
      });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !card.hidden) closeCard(); });
    if (list) {
      sats.forEach(function (s) {
        var li = document.createElement('li');
        var b = document.createElement('button');
        b.type = 'button';
        b.textContent = s.name;
        b.addEventListener('click', function () { openCard(s, b); });
        li.appendChild(b);
        list.appendChild(li);
      });
    }
    var mem0 = db();
    Object.keys(mem0).forEach(function (id) {
      var s = byId[id];
      if (!s || !mem0[id].on || !s.imageQ) return;
      fetch('https://images-api.nasa.gov/search?media_type=image&q=' + encodeURIComponent(s.imageQ), { credentials: 'omit' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) {
          if (!j) return;
          var data = ((((j.collection || {}).items || [])[0] || {}).data || [])[0];
          if (!data || !data.date_created) return;
          var m = db(); if (!m[id]) return;
          m[id].latest = data.date_created;
          save(m);
          draw();
        }).catch(function () {});
    });
    function satFromHash() {
      var h = (location.hash || '').replace(/^#/, '');
      return h.indexOf('sat-') === 0 ? h.slice(4) : '';
    }
    function focusFromHash() {
      var id = satFromHash();
      var s = id && byId[id];
      if (!s) return;
      var next = 'all';
      if (s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5') next = 'lagrange';
      else if (s.regime === 'cruise') next = 'beyond';
      else if (s.fn && s.fn !== 'nav') next = s.fn;
      setCat(next);
      var btn = stage.querySelector('.orb-btn[data-id="' + id + '"]');
      if (btn) btn.classList.add('is-focus');
      var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (root.scrollIntoView) root.scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' });
      openCard(s, btn || null);
    }
    window.addEventListener('hashchange', focusFromHash);
    draw();
    focusFromHash();
  }
})();
