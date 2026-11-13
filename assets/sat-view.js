/* Earth-centered orbit diagram. Rings follow NASA's LEO / MEO / GEO / HEO order.
   Markers show the orbit type, not a live position. No account and no tracker. */
(function () {
  var root = document.querySelector('.sat-view');
  var stage = document.getElementById('sat-stage');
  var card = document.getElementById('sat-card');
  var list = document.getElementById('sat-list-ul');
  if (!root || !stage || !card) return;
  var rtl = (document.documentElement.getAttribute('dir') || '') === 'rtl';
  var SAT = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="6.2" y="6.2" width="3.6" height="3.6" rx=".4" fill="#fff"/><rect x="1" y="7" width="4.2" height="2" rx=".3" fill="#fff"/><rect x="10.8" y="7" width="4.2" height="2" rx=".3" fill="#fff"/></svg>';
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  fetch(root.getAttribute('data-src'), { credentials: 'omit' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(boot).catch(function () {
    stage.innerHTML = '<p class="wm-err">The orbit view could not load. The mission list below still works when data is available.</p>';
  });
  function boot(D) {
    var ui = D.ui || {}, sats = D.sats || [], byId = {}, mode = '', cat = 'all', lastBtn = null;
    var geom = null, zoomT = 0, selectedLg = '';
    sats.forEach(function (s) { byId[s.id] = s; });
    var earth = root.getAttribute('data-earth');
    var earthLg = root.getAttribute('data-earth-lg') || earth;
    var moon = root.getAttribute('data-moon') || '';
    var pre = (root.getAttribute('data-src') || '').indexOf('../') === 0 ? '../' : '';
    var sun = root.getAttribute('data-sun') || (pre + 'assets/earth/sdo-aia304.jpg');
    var canvas = document.createElement('div');
    canvas.className = 'sat-canvas';
    stage.appendChild(canvas);

    function craft(s) { return s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5' || s.regime === 'cruise'; }
    function kindWord(s) { return craft(s) ? (ui.kindCraft || 'Spacecraft') : (ui.kindSat || 'Satellite'); }
    function labelText(s) {
      var k = kindWord(s), n = s.name || '';
      if (n.toLowerCase().indexOf(String(k).toLowerCase()) >= 0) return n;
      return (n + ' ' + k).trim();
    }
    function show(s) {
      if (cat === 'all') return true;
      if (cat === 'lagrange' || cat === 'beyond') return s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5' || s.regime === 'cruise';
      return s.fn === cat;
    }
    function stageAspect() {
      var r = stage.getBoundingClientRect();
      return Math.max(0.45, (r.width || 800) / Math.max(r.height || 520, 1));
    }
    function earthView() {
      var aspect = stageAspect(), span = geom.r * 2 / 0.92, vw, vh;
      if (aspect >= 1) { vh = span; vw = vh * aspect; }
      else { vw = span; vh = vw / aspect; }
      return { x: geom.cx - vw / 2, y: geom.cy - vh / 2, w: vw, h: vh };
    }
    function allView() {
      var aspect = stageAspect(), pad = 18;
      var bw = geom.W + pad * 2, bh = geom.H + pad * 2, box = bw / bh, vw, vh;
      if (aspect > box) { vh = bh; vw = vh * aspect; }
      else { vw = bw; vh = vw / aspect; }
      return { x: geom.W / 2 - vw / 2, y: geom.H / 2 - vh / 2, w: vw, h: vh };
    }
    function currentView() {
      var a = earthView(), b = allView(), t = Math.max(0, Math.min(1, zoomT));
      return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, w: a.w + (b.w - a.w) * t, h: a.h + (b.h - a.h) * t };
    }
    function applyView() {
      if (!geom) return;
      var view = currentView();
      var svg = canvas.querySelector('svg');
      if (svg) svg.setAttribute('viewBox', view.x + ' ' + view.y + ' ' + view.w + ' ' + view.h);
      [].forEach.call(canvas.querySelectorAll('.orb-btn,.lag-pt,.orb-lab'), function (el) {
        var x = +el.getAttribute('data-x'), y = +el.getAttribute('data-y');
        el.style.left = ((x - view.x) / view.w * 100) + '%';
        el.style.top = ((y - view.y) / view.h * 100) + '%';
      });
      requestAnimationFrame(uncollide);
    }
    function uncollide() {
      var labs = [].slice.call(canvas.querySelectorAll('.orb-lab'));
      labs.forEach(function (el) { el.style.marginTop = '0px'; });
      labs.sort(function (a, b) { return a.getBoundingClientRect().top - b.getBoundingClientRect().top || a.getBoundingClientRect().left - b.getBoundingClientRect().left; });
      for (var i = 1; i < labs.length; i++) {
        var guard = 0;
        while (guard < 8) {
          var prev = labs[i - 1].getBoundingClientRect();
          var cur = labs[i].getBoundingClientRect();
          var hOverlap = !(prev.right < cur.left + 2 || cur.right < prev.left + 2);
          var overlap = prev.bottom + 2 - cur.top;
          if (!(hOverlap && overlap > 0)) break;
          labs[i].style.marginTop = ((parseFloat(labs[i].style.marginTop) || 0) + overlap) + 'px';
          guard++;
        }
      }
    }
    function addLabel(x, y, text) {
      var lab = document.createElement('span');
      lab.className = 'orb-lab';
      lab.textContent = text;
      lab.setAttribute('data-x', x);
      lab.setAttribute('data-y', y);
      canvas.appendChild(lab);
    }
    function layout(which) {
      var groups = { leo: [], meo: [], geo: [], heo: [], l1: [], l2: [], l5: [], cruise: [] };
      sats.forEach(function (s) { if (show(s) && groups[s.regime === 'sso' ? 'leo' : s.regime]) groups[s.regime === 'sso' ? 'leo' : s.regime].push(s); });
      var W = 900, H = 520, pts = [], cx = 400, cy = 268, er = 72;
      function onEllipse(list, ecx, ecy, rx, ry) {
        var n = list.length;
        list.forEach(function (s, i) {
          var a = -Math.PI / 2 + (i + 0.5) * (2 * Math.PI) / Math.max(n, 1);
          pts.push({ s: s, x: ecx + rx * Math.cos(a), y: ecy + ry * Math.sin(a) });
        });
      }
      function stack(list, x, y0, gap) {
        var n = list.length, top = y0 - ((n - 1) * gap) / 2;
        list.forEach(function (s, i) { pts.push({ s: s, x: x, y: top + i * gap }); });
      }
      var svg, lgs = [];
      if (which === 'near') {
        onEllipse(groups.leo, cx, cy, 118, 50);
        onEllipse(groups.meo, cx, cy, 178, 74);
        onEllipse(groups.geo, cx, cy, 246, 102);
        onEllipse(groups.heo, cx + 40, cy, 196, 118);
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
        var EX = 620, EY = 330, ER = 148, SR = 72, SX = 108, SY = 300;
        cx = EX; cy = EY; er = ER;
        onEllipse(groups.leo.concat(groups.meo, groups.geo, groups.heo), EX, EY, 230, 86);
        stack(groups.l1, 250, 150, 36);
        stack(groups.l2, 900, 150, 36);
        stack(groups.cruise, 900, 470, 36);
        lgs = [
          { id: 'l1', x: 250, y: 78, name: 'L1' },
          { id: 'l2', x: 860, y: 78, name: 'L2' },
          { id: 'l3', x: 108, y: 150, name: 'L3' },
          { id: 'l4', x: 500, y: 48, name: 'L4' },
          { id: 'l5', x: 500, y: 600, name: 'L5' }
        ];
        function dist(x, y, text) {
          return '<text x="' + x + '" y="' + y + '" fill="#d7ecff" font-size="11">' + esc(text || '') + '</text>';
        }
        svg = '<svg class="orb-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(ui.farDiagram || '') + '">' +
          '<defs>' +
          '<radialGradient id="sun-glow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(255,170,60,.0)"/><stop offset="55%" stop-color="rgba(255,120,40,.45)"/><stop offset="100%" stop-color="rgba(255,60,20,0)"/></radialGradient>' +
          '<clipPath id="sun-disc"><circle cx="' + SX + '" cy="' + SY + '" r="' + SR + '"/></clipPath>' +
          '<clipPath id="sun-flare"><circle cx="' + SX + '" cy="' + SY + '" r="' + (SR + 10) + '"/></clipPath>' +
          '<clipPath id="earth-far"><circle cx="' + EX + '" cy="' + EY + '" r="' + ER + '"/></clipPath>' +
          '<clipPath id="moon-far"><circle cx="790" cy="214" r="32"/></clipPath>' +
          '</defs>' +
          '<circle class="sun-glow" cx="' + SX + '" cy="' + SY + '" r="' + (SR + 28) + '" fill="url(#sun-glow)"/>' +
          '<image class="sun-base" href="' + esc(sun) + '" x="' + (SX - SR) + '" y="' + (SY - SR) + '" width="' + (SR * 2) + '" height="' + (SR * 2) + '" clip-path="url(#sun-disc)" preserveAspectRatio="xMidYMid slice"/>' +
          '<image class="sun-flare" href="' + esc(sun) + '" x="' + (SX - SR - 8) + '" y="' + (SY - SR - 8) + '" width="' + ((SR + 8) * 2) + '" height="' + ((SR + 8) * 2) + '" clip-path="url(#sun-flare)" preserveAspectRatio="xMidYMid slice"/>' +
          '<circle cx="' + EX + '" cy="' + EY + '" r="' + (ER + 28) + '" fill="rgba(150,205,255,.18)"/>' +
          '<image href="' + esc(earthLg) + '" x="' + (EX - ER) + '" y="' + (EY - ER) + '" width="' + (ER * 2) + '" height="' + (ER * 2) + '" clip-path="url(#earth-far)"/>' +
          (moon ? '<image href="' + esc(moon) + '" x="758" y="182" width="64" height="64" clip-path="url(#moon-far)" preserveAspectRatio="xMidYMid slice"/>' : '') +
          dist(250, 248, ui.dL12) + dist(860, 248, ui.dL12) + dist(108, 188, ui.dL3) + dist(500, 86, ui.dL4) + dist(500, 624, ui.dL5) +
          '</svg>';
      }
      geom = { W: W, H: H, cx: cx, cy: cy, r: er };
      canvas.innerHTML = svg;
      pts.forEach(function (p) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'orb-btn';
        b.innerHTML = SAT;
        b.setAttribute('data-id', p.s.id);
        b.setAttribute('data-x', p.x);
        b.setAttribute('data-y', p.y);
        b.id = 'sat-' + p.s.id;
        b.setAttribute('aria-label', labelText(p.s));
        b.addEventListener('click', function () { openCard(p.s, b); });
        canvas.appendChild(b);
        addLabel(p.x, p.y, labelText(p.s));
      });
      lgs.forEach(function (g) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'lag-pt' + (selectedLg === g.id ? ' is-on' : '');
        b.setAttribute('data-lg', g.id);
        b.setAttribute('data-x', g.x);
        b.setAttribute('data-y', g.y);
        b.setAttribute('aria-pressed', selectedLg === g.id ? 'true' : 'false');
        b.setAttribute('aria-label', g.name);
        b.addEventListener('click', function () {
          selectedLg = selectedLg === g.id ? '' : g.id;
          [].forEach.call(canvas.querySelectorAll('.lag-pt'), function (el) {
            var on = el.getAttribute('data-lg') === selectedLg;
            el.classList.toggle('is-on', on);
            el.setAttribute('aria-pressed', on ? 'true' : 'false');
          });
        });
        canvas.appendChild(b);
        addLabel(g.x, g.y, g.name);
      });
      applyView();
    }
    function openCard(s, btn) {
      lastBtn = btn || lastBtn;
      root.querySelector('.sat-layout').classList.add('has-card');
      card.hidden = false;
      var photo = '';
      if (s.photo) {
        var b = pre + s.photo;
        photo = '<img class="sat-shot" src="' + esc(b) + '-800.jpg" alt="" width="800" height="450" loading="lazy" decoding="async">' +
          '<p class="sat-photo-credit">' + esc(s.credit || '') + '</p>';
      } else if (s.shot) {
        photo = '<img class="sat-shot" src="' + esc(pre + s.shot) + '" alt="" loading="lazy" decoding="async">' +
          '<p class="sat-photo-credit">' + esc(s.credit || '') + '</p>';
      }
      var brief = (s.brief || []).slice(0, 4).map(function (line) { return '<p>' + esc(line) + '</p>'; }).join('');
      var more = s.official ? '<p class="sat-more-row"><a class="sat-more" href="' + esc(s.official) + '" target="_blank" rel="noopener">' + esc(ui.more || 'Click here for more') + '</a></p>' : '';
      card.innerHTML = '<button type="button" class="sat-close" aria-label="' + esc(ui.close || 'Close') + '">×</button>' +
        '<h3 id="sat-card-title" class="sat-title">' + esc(s.name) + '</h3>' + photo + brief + more;
      card.querySelector('.sat-close').addEventListener('click', closeCard);
      card.querySelector('.sat-close').focus();
    }
    function closeCard() {
      card.hidden = true;
      card.innerHTML = '';
      root.querySelector('.sat-layout').classList.remove('has-card');
      if (lastBtn && lastBtn.focus) lastBtn.focus();
    }
    function draw() {
      var next = (cat === 'lagrange' || cat === 'beyond' || cat === 'science') ? 'far' : 'near';
      if (next !== mode) zoomT = next === 'near' ? 0 : 1;
      mode = next;
      layout(mode);
    }
    function setCat(next) {
      cat = next === 'lagrange' ? 'beyond' : next;
      [].forEach.call(root.querySelectorAll('button.wm-cat'), function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-cat') === cat ? 'true' : 'false');
      });
      var cruise = document.getElementById('sat-cruise');
      if (cruise) cruise.hidden = cat !== 'beyond';
      draw();
    }
    var zbar = document.createElement('div');
    zbar.className = 'wm-zoom';
    zbar.setAttribute('role', 'group');
    function zbtn(label, aria) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = label;
      b.setAttribute('aria-label', aria);
      return b;
    }
    var zin = zbtn('+', ui.zoomIn || 'Zoom in');
    var zout = zbtn('−', ui.zoomOut || 'Zoom out');
    var zfit = zbtn('⌂', ui.zoomFit || 'Fit the planet');
    [zin, zout, zfit].forEach(function (b) { zbar.appendChild(b); });
    stage.appendChild(zbar);
    zin.addEventListener('click', function () { zoomT = Math.max(0, zoomT - 0.22); applyView(); });
    zout.addEventListener('click', function () { zoomT = Math.min(1, zoomT + 0.22); applyView(); });
    zfit.addEventListener('click', function () { zoomT = 0; applyView(); });
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
    var rz;
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(applyView, 80); });
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
    function satFromHash() {
      var h = (location.hash || '').replace(/^#/, '');
      return h.indexOf('sat-') === 0 ? h.slice(4) : '';
    }
    function focusFromHash() {
      var h = (location.hash || '').replace(/^#/, '');
      if (h === 'lagrange' || h === 'beyond') { setCat('beyond'); return; }
      var id = satFromHash();
      var s = id && byId[id];
      if (!s) return;
      var next = 'all';
      if (s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5' || s.regime === 'cruise') next = 'beyond';
      else if (s.fn && s.fn !== 'nav') next = s.fn;
      setCat(next);
      var btn = canvas.querySelector('.orb-btn[data-id="' + id + '"]');
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
