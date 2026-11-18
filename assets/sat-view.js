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
  var started = false;
  function wantNow() {
    var h = (location.hash || '').replace(/^#/, '');
    return h === 'satmap' || h === 'beyond' || h === 'lagrange' || h.indexOf('sat-') === 0;
  }
  function start() {
    if (started) return;
    started = true;
    fetch(root.getAttribute('data-src'), { credentials: 'omit' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(boot).catch(function () {
      stage.innerHTML = '<p class="wm-err">The orbit view could not load. The mission list below still works when data is available.</p>';
    });
  }
  root.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button[data-cat]');
    if (!b || !root.contains(b)) return;
    root.setAttribute('data-pending-cat', b.getAttribute('data-cat') || '');
    start();
  });
  if (wantNow()) start();
  else if (window.IntersectionObserver) {
    var io = new IntersectionObserver(function (ents) {
      if (ents.some(function (en) { return en.isIntersecting; })) { io.disconnect(); start(); }
    }, { rootMargin: '240px 0px' });
    io.observe(root);
  } else start();
  window.addEventListener('hashchange', function () { if (wantNow()) start(); });
  function boot(D) {
    var ui = D.ui || {}, sats = D.sats || [], byId = {}, mode = '', cat = 'weather', lastBtn = null;
    var geom = null, zoomT = 0, selectedLg = '', orbitFilter = '';
    sats.forEach(function (s) { byId[s.id] = s; });
    var pre = (root.getAttribute('data-src') || '').indexOf('../') === 0 ? '../' : '';
    var cut = pre + 'assets/earth/cut/';
    var earth = cut + 'earth.webp';
    var earthLg = earth;
    var openId = '';
    var canvas = document.createElement('div');
    canvas.className = 'sat-canvas';
    stage.appendChild(canvas);

    function craft(s) { return s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5' || s.regime === 'cruise'; }
    function kindWord(s) { return craft(s) ? (ui.kindCraft || 'Spacecraft') : (ui.kindSat || 'Satellite'); }
    function shortName(s) {
      var n = String(s.name || '').replace(/\s*\([^)]*\)/g, ' ').replace(/\s+/g, ' ').trim();
      n = n.replace(/\s+(Space Telescope|Satellite|Spacecraft)$/i, '').trim();
      return n || s.name || '';
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
    function contentBox() {
      var minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9, n = 0;
      function add(x, y) { minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y); n++; }
      [].forEach.call(canvas.querySelectorAll('.orb-btn,.lag-pt'), function (el) { add(+el.getAttribute('data-x'), +el.getAttribute('data-y')); });
      if (mode === 'near') {
        add(328, 196); add(472, 340);
        add(400 - 178, 268 - 74); add(400 + 178, 268 + 74);
        if (cat === 'all' || orbitFilter === 'geo' || selectedBand === 'geo') {
          add(400 - 246, 268 - 102); add(400 + 246, 268 + 102);
        }
        if (cat === 'all' || orbitFilter === 'heo' || selectedBand === 'heo') {
          add(440 - 196, 268 - 118); add(440 + 196, 268 + 118);
        }
      }
      if (!n) { minX = 0; minY = 0; maxX = geom.W; maxY = geom.H; }
      return { minX: minX, minY: minY, maxX: maxX, maxY: maxY };
    }
    function mapRect(W, H) {
      return { x: gut.l, y: gut.t, w: Math.max(48, W - gut.l - gut.r), h: Math.max(48, H - gut.t - gut.b) };
    }
    function viewFrom(cx, cy, bw, bh, map, W, H) {
      var scale = Math.max(bw / map.w, bh / map.h);
      var viewW = scale * W, viewH = scale * H;
      var mx = map.x + map.w / 2, my = map.y + map.h / 2;
      return { x: cx - mx * scale, y: cy - my * scale, w: viewW, h: viewH };
    }
    function fitView(W, H) {
      if (mode === 'near' && geom) {
        var reach = 190, outer = cat === 'all' || orbitFilter === 'geo' || orbitFilter === 'heo' || selectedBand === 'geo' || selectedBand === 'heo';
        if (!outer) {
          var nodes = canvas.querySelectorAll('.orb-btn');
          for (var i = 0; i < nodes.length; i++) {
            var reg = nodes[i].getAttribute('data-reg');
            if (reg === 'geo' || reg === 'heo') { outer = true; break; }
          }
        }
        if (outer) reach = 268;
        var side = W < 560 ? 8 : Math.min(Math.max(gut.l, gut.r, 8), W * 0.24);
        var lane = W < 560 ? Math.max(48, W - 16) : Math.max(W * 0.52, W - side * 2);
        lane = Math.min(lane, W - 12);
        var map = { x: (W - lane) / 2, y: Math.max(10, gut.t), w: lane, h: Math.max(48, H - Math.max(10, gut.t) - Math.max(10, gut.b)) };
        var bw = reach * 2;
        return viewFrom(geom.cx, geom.cy, bw, bw * (map.h / map.w), map, W, H);
      }
      var b = contentBox(), map2 = mapRect(W, H);
      var bw2 = Math.max(40, (b.maxX - b.minX) * 1.08), bh2 = Math.max(40, (b.maxY - b.minY) * 1.08);
      return viewFrom((b.minX + b.maxX) / 2, (b.minY + b.maxY) / 2, bw2, bh2, map2, W, H);
    }
    function closeView(W, H) {
      var map = mapRect(W, H), span = geom.r * 2 / 0.725, aspect = map.w / map.h, vw, vh;
      if (aspect >= 1) { vh = span; vw = vh * aspect; }
      else { vw = span; vh = vw / aspect; }
      return viewFrom(geom.cx, geom.cy, vw, vh, map, W, H);
    }
    function currentView() {
      var box = canvas.getBoundingClientRect();
      var W = box.width || 800, H = box.height || 520;
      var a = fitView(W, H), b = closeView(W, H), t = Math.max(0, Math.min(1, zoomT));
      return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, w: a.w + (b.w - a.w) * t, h: a.h + (b.h - a.h) * t };
    }
    var gut = { l: 8, r: 8, t: 8, b: 8 };
    function applyView() {
      if (!geom) return;
      placeLabels();
    }
    function regimeOf(s) { return !s ? '' : (s.regime === 'sso' ? 'leo' : s.regime); }
    function placeLabels() {
      var box = canvas.getBoundingClientRect();
      var W = box.width, H = box.height;
      if (W < 80 || H < 80) return;
      var labs = [].slice.call(canvas.querySelectorAll('.orb-lab'));
      var maxW = Math.max(72, Math.min(W * 0.34, 168));
      labs.forEach(function (el) {
        el.hidden = false;
        el.style.maxWidth = maxW + 'px';
        el.style.position = 'absolute';
        el.style.margin = '0';
        el.style.transform = 'none';
        el.style.left = '0px';
        el.style.top = '0px';
      });
      var view0 = (function () {
        var b = contentBox();
        var bw = Math.max(40, b.maxX - b.minX), bh = Math.max(40, b.maxY - b.minY);
        return { cx: (b.minX + b.maxX) / 2, cy: (b.minY + b.maxY) / 2, bw: bw, bh: bh };
      })();
      function anchor(el) {
        var x = +el.getAttribute('data-x'), y = +el.getAttribute('data-y');
        var mid = geom ? geom.cx : view0.cx;
        return { el: el, x: x, y: y, side: x < mid ? 'l' : 'r', ny: y };
      }
      var items = labs.map(anchor);
      function pack(list, avail) {
        var gap = 3, guard = 0;
        while (guard < 4) {
          var h = 0;
          list.forEach(function (it) { h += it.el.offsetHeight; });
          h += Math.max(0, list.length - 1) * gap;
          if (h <= avail || guard === 3) return { h: h, gap: gap };
          gap = 1;
          canvas.style.setProperty('--lab-size', (0.74 - guard * 0.04) + 'rem');
          guard++;
        }
        return { h: avail, gap: 1 };
      }
      var left = items.filter(function (it) { return it.side === 'l'; }).sort(function (a, b) { return a.ny - b.ny; });
      var right = items.filter(function (it) { return it.side === 'r'; }).sort(function (a, b) { return a.ny - b.ny; });
      var avail = H - 8;
      pack(left, avail); pack(right, avail);
      var lw = 0, rw = 0;
      left.forEach(function (it) { lw = Math.max(lw, it.el.offsetWidth); });
      right.forEach(function (it) { rw = Math.max(rw, it.el.offsetWidth); });
      lw = Math.min(maxW, Math.max(lw, left.length ? 48 : 0));
      rw = Math.min(maxW, Math.max(rw, right.length ? 48 : 0));
      function colsFor(list) {
        var h = 0;
        list.forEach(function (it) { h += it.el.offsetHeight; });
        h += Math.max(0, list.length - 1) * 2;
        return h > H - 4 ? 2 : 1;
      }
      var nL = left.length ? colsFor(left) : 0, nR = right.length ? colsFor(right) : 0;
      gut.l = nL ? nL * lw + Math.max(0, nL - 1) * 4 + 18 : 8;
      gut.r = nR ? nR * rw + Math.max(0, nR - 1) * 4 + 18 : 8;
      gut.t = 18; gut.b = 18;
      if (W < 560 && labs.length) {
        var phoneCol = Math.max(100, Math.floor((W - 16) / 2));
        labs.forEach(function (el) { el.style.maxWidth = phoneCol + 'px'; });
        var rowH = 44;
        labs.forEach(function (el) { rowH = Math.max(rowH, el.offsetHeight); });
        var nrows = Math.ceil(labs.length / 2);
        gut.l = 8; gut.r = 8; gut.t = 8;
        gut.b = nrows * rowH + Math.max(0, nrows - 1) * 4 + 10;
      }
      var capG = W * (W < 560 ? 0.3 : 0.28);
      if (gut.l > capG) gut.l = capG;
      if (gut.r > capG) gut.r = capG;
      if (gut.l + gut.r > W * 0.78) {
        var share = W * 0.78, scale = share / (gut.l + gut.r);
        gut.l *= scale; gut.r *= scale;
        lw = nL ? Math.max(36, (gut.l - 18 - Math.max(0, nL - 1) * 4) / nL) : lw;
        rw = nR ? Math.max(36, (gut.r - 18 - Math.max(0, nR - 1) * 4) / nR) : rw;
        labs.forEach(function (el) { el.style.maxWidth = Math.min(lw, rw) + 'px'; });
      }
      var view = currentView();
      var svg = canvas.querySelector('svg.orb-svg');
      if (svg) {
        svg.setAttribute('viewBox', view.x + ' ' + view.y + ' ' + view.w + ' ' + view.h);
        svg.setAttribute('preserveAspectRatio', 'none');
      }
      [].forEach.call(canvas.querySelectorAll('.orb-btn,.lag-pt,.sso-mark'), function (el) {
        var x = +el.getAttribute('data-x'), y = +el.getAttribute('data-y');
        var px = (x - view.x) / view.w * W, py = (y - view.y) / view.h * H;
        el.style.left = px + 'px';
        el.style.top = py + 'px';
        var bottomLimit = W < 560 ? H - gut.b + 6 : H + 8;
        var inside = px >= (W < 560 ? -8 : gut.l - 20) && px <= (W < 560 ? W + 8 : W - gut.r + 20) && py >= -8 && py <= bottomLimit;
        if (!el.classList.contains('sso-mark')) el.classList.toggle('is-off', !inside);
      });
      function placeCol(list, side, slot, slots, colW) {
        var gap = 2, heights = list.map(function (it) { return it.el.offsetHeight; });
        var total = heights.reduce(function (s, h) { return s + h; }, 0) + Math.max(0, list.length - 1) * gap;
        var y = Math.max(3, (H - total) / 2);
        if (y + total > H - 2) y = 3;
        list.forEach(function (it, i) {
          var w = it.el.offsetWidth;
          var x = side === 'l' ? 3 + slot * (colW + 4) : W - 3 - (slot + 1) * colW - slot * 4 + (colW - w);
          it.el.style.left = x + 'px';
          it.el.style.top = y + 'px';
          it.el.hidden = false;
          it.box = { x: x, y: y, w: w, h: heights[i] };
          y += heights[i] + gap;
        });
      }
      function stack(list, side, colW) {
        if (!list.length) return;
        var gap = 2, heights = list.map(function (it) { return it.el.offsetHeight; });
        var total = heights.reduce(function (s, h) { return s + h; }, 0) + Math.max(0, list.length - 1) * gap;
        if (total <= H - 4) { placeCol(list, side, 0, 1, colW); return; }
        var mid = Math.ceil(list.length / 2);
        placeCol(list.slice(0, mid), side, 0, 2, colW);
        placeCol(list.slice(mid), side, 1, 2, colW);
      }
      if (W < 560 && labs.length) {
        var pCol = Math.max(100, Math.floor((W - 16) / 2));
        var pH = 44, pGap = 4;
        labs.forEach(function (el) { pH = Math.max(pH, el.offsetHeight); });
        var pRows = Math.ceil(items.length / 2);
        var pBlock = pRows * pH + Math.max(0, pRows - 1) * pGap + 10;
        items.forEach(function (it, i) {
          var col = i % 2, row = Math.floor(i / 2);
          var w = Math.min(it.el.offsetWidth, pCol);
          var x = 4 + col * (pCol + 4);
          var y = H - pBlock + 4 + row * (pH + pGap);
          it.el.style.left = x + 'px';
          it.el.style.top = y + 'px';
          it.el.hidden = false;
          it.side = col === 0 ? 'l' : 'r';
          it.box = { x: x, y: y, w: w, h: it.el.offsetHeight };
        });
      } else {
        stack(left, 'l', lw); stack(right, 'r', rw);
      }
      if (mode === 'near' && geom) {
        var ecx = (geom.cx - view.x) / view.w * W, ecy = (geom.cy - view.y) / view.h * H;
        var earthR = 78 * (W / view.w);
        items.forEach(function (it) {
          var b = it.box;
          if (!b) return;
          var cx0 = Math.max(b.x, Math.min(ecx, b.x + b.w));
          var cy0 = Math.max(b.y, Math.min(ecy, b.y + b.h));
          var dx = cx0 - ecx, dy = cy0 - ecy;
          if (dx * dx + dy * dy >= (earthR + 8) * (earthR + 8)) return;
          var nx = it.side === 'l' ? Math.max(2, ecx - earthR - 10 - b.w) : Math.min(W - b.w - 2, ecx + earthR + 10);
          it.el.style.left = nx + 'px';
          b.x = nx;
        });
      }
      var lead = canvas.querySelector('.sat-leaders');
      if (!lead) {
        lead = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        lead.setAttribute('class', 'sat-leaders');
        lead.setAttribute('aria-hidden', 'true');
        canvas.appendChild(lead);
      }
      lead.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      lead.innerHTML = '';
      items.forEach(function (it) {
        var px = (it.x - view.x) / view.w * W, py = (it.y - view.y) / view.h * H;
        var b = it.box;
        if (!b) return;
        var tx = it.side === 'l' ? b.x + b.w : b.x;
        var ty = b.y + b.h / 2;
        var reg = it.el.getAttribute('data-reg') || '';
        var ln = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        ln.setAttribute('x1', px); ln.setAttribute('y1', py); ln.setAttribute('x2', tx); ln.setAttribute('y2', ty);
        ln.setAttribute('class', 'sat-leader');
        ln.setAttribute('data-reg', reg);
        lead.appendChild(ln);
      });
      applyDim();
    }
    function bandCopy(id) {
      var bands = D.bands || {};
      return bands[id] || null;
    }
        var selectedBand = '';
    var bandBox = document.createElement('div');
    bandBox.id = 'sat-band';
    bandBox.className = 'sat-band';
    bandBox.hidden = true;
    bandBox.setAttribute('role', 'dialog');
    stage.appendChild(bandBox);
    function edge(svg, cx, cy, rx, ry, label, lx, ly) {
      var el = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
      el.setAttribute('class', 'band-edge');
      el.setAttribute('cx', cx); el.setAttribute('cy', cy); el.setAttribute('rx', rx); el.setAttribute('ry', ry);
      svg.appendChild(el);
      if (!label) return;
      var t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      t.setAttribute('class', 'band-edge-label');
      t.setAttribute('x', lx); t.setAttribute('y', ly);
      t.textContent = label;
      svg.appendChild(t);
    }
    function paintBand(id) {
      var svg = canvas.querySelector('svg');
      if (!svg) return;
      [].forEach.call(svg.querySelectorAll('.band-edge,.band-edge-label'), function (n) { n.remove(); });
      var mark = {
        leo: [[400,268,96,40,'180 km',400,228],[400,268,136,62,'2,000 km',400,206]],
        sso: [[400,268,108,46,'600 km',330,250],[400,268,124,54,'800 km',330,214]],
        meo: [[400,268,150,64,'2,000 km',560,230],[400,268,220,92,'35,786 km',620,176]],
        geo: [[400,268,246,102,'35,786 km',620,150],[400,268,246,102,'35,786 km',180,380]],
        heo: [[440,268,196,118,'',0,0]]
      }[id];
      if (!mark) return;
      mark.forEach(function (e) { edge(svg, e[0], e[1], e[2], e[3], e[4], e[5], e[6]); });
    }
    function selectBand(id) {
      if (selectedBand === id) { selectedBand = ''; bandBox.hidden = true; paintBand(''); }
      else {
        selectedBand = id;
        if (!bandCopy(id)) { bandBox.hidden = true; return; }
        bandBox.hidden = true;
        paintBand(id);
      }
      [].forEach.call(canvas.querySelectorAll('.band-btn'), function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-band') === selectedBand ? 'true' : 'false');
      });
      showOrbitNote();
    }
    function addBand(x, y, id, label) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'band-btn';
      b.textContent = label;
      b.setAttribute('data-band', id);
      b.setAttribute('data-x', x);
      b.setAttribute('data-y', y);
      b.setAttribute('aria-pressed', selectedBand === id ? 'true' : 'false');
      b.addEventListener('click', function () { selectBand(id); });
      canvas.appendChild(b);
    }
    function addLabel(x, y, text, reg, onClick) {
      var lab = document.createElement('button');
      lab.type = 'button';
      lab.className = 'orb-lab is-' + (reg || 'x');
      lab.textContent = text;
      lab.setAttribute('data-x', x);
      lab.setAttribute('data-y', y);
      lab.setAttribute('data-reg', reg || '');
      lab.setAttribute('aria-label', text);
      if (onClick) lab.addEventListener('click', function () { onClick(lab); });
      canvas.appendChild(lab);
    }
    function applyDim() {
      var on = orbitFilter;
      [].forEach.call(canvas.querySelectorAll('.orb-btn,.orb-lab'), function (el) {
        var reg = el.getAttribute('data-reg') || '';
        el.classList.toggle('is-hot', !!(on && reg === on));
        el.classList.toggle('is-dim', !!(on && reg && reg !== on));
      });
      var svg = canvas.querySelector('svg.orb-svg');
      if (svg) svg.setAttribute('data-orbit', on || '');
      [].forEach.call(canvas.querySelectorAll('.sat-leader'), function (ln) {
        var dim = !!(on && ln.getAttribute('data-reg') !== on);
        ln.classList.toggle('is-dim', dim);
      });
    }
    function showBandInfo(id) {
      bandBox.hidden = true;
      if (!bandCopy(id)) return;
    }
    function syncOrbit() {
      [].forEach.call(root.querySelectorAll('.sat-orbits button'), function (b) {
        var id = b.getAttribute('data-band');
        var pressed = (id === 'leo' || id === 'meo' || id === 'geo') ? orbitFilter === id : selectedBand === id;
        b.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      });
      var badge = canvas.querySelector('.sso-mark');
      if (badge) badge.setAttribute('aria-pressed', selectedBand === 'sso' ? 'true' : 'false');
    }
    function clearOrbit() {
      orbitFilter = '';
      selectedBand = '';
      bandBox.hidden = true;
      paintBand('');
      syncOrbit();
      applyDim();
      showOrbitNote();
    }
    function toggleOrbit(id) {
      if (orbitFilter === id) { clearOrbit(); return; }
      orbitFilter = id;
      selectedBand = id;
      showBandInfo(id);
      paintBand(id);
      syncOrbit();
      applyDim();
      showOrbitNote();
      if (id === 'meo' && byId.galileo) openCard(byId.galileo);
    }
    function pickBand(id) {
      if (id === 'leo' || id === 'meo' || id === 'geo') { toggleOrbit(id); return; }
      if (selectedBand === id) { selectedBand = ''; bandBox.hidden = true; paintBand(''); syncOrbit(); showOrbitNote(); return; }
      selectedBand = id;
      showBandInfo(id);
      paintBand(id);
      syncOrbit();
      showOrbitNote();
    }
    function layout(which) {
      var poster = document.getElementById('sat-poster');
      if (poster) poster.remove();
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
          '<defs></defs>' +
          '<ellipse class="ring-hit" data-band="leo" cx="400" cy="268" rx="118" ry="50" fill="none" stroke="transparent" stroke-width="18"/>' +
          '<ellipse class="ring-hit" data-band="meo" cx="400" cy="268" rx="178" ry="74" fill="none" stroke="transparent" stroke-width="18"/>' +
          '<ellipse class="ring-hit" data-band="geo" cx="400" cy="268" rx="246" ry="102" fill="none" stroke="transparent" stroke-width="18"/>' +
          '<ellipse class="ring-hit" data-band="heo" cx="440" cy="268" rx="196" ry="118" fill="none" stroke="transparent" stroke-width="18"/>' +
          '<ellipse class="ring ring-leo" cx="400" cy="268" rx="118" ry="50" fill="none" stroke="#7ad7ff" stroke-width="3"/>' +
          '<ellipse class="ring ring-meo" cx="400" cy="268" rx="178" ry="74" fill="none" stroke="#ffb703" stroke-width="3"/>' +
          '<ellipse class="ring ring-geo" cx="400" cy="268" rx="246" ry="102" fill="none" stroke="#e2b6ff" stroke-width="3"/>' +
          '<ellipse class="ring ring-heo" cx="440" cy="268" rx="196" ry="118" fill="none" stroke="#ffd166" stroke-width="2" stroke-dasharray="5 4"/>' +
          '<image href="' + esc(earth) + '" x="328" y="196" width="144" height="144"/>' +
          '</svg>';
        /* band names are the buttons added after the svg */
      } else {
        W = 1000; H = 640;
        var EX = 620, EY = 330, ER = 148, SR = 72, SX = 108, SY = 300;
        cx = EX; cy = EY; er = ER;
        onEllipse(groups.leo.concat(groups.meo, groups.geo, groups.heo), EX, EY, 230, 86);
        stack(groups.l1, 250, 150, 36);
        stack(groups.l2, 900, 150, 36);
        stack(groups.cruise, 900, 470, 36);
        var moon = cut + 'moon.webp';
        var sun = cut + 'sun.webp';
        lgs = [
          { id: 'l1', x: 250, y: 78, name: 'L1' },
          { id: 'l2', x: 860, y: 78, name: 'L2' },
          { id: 'l3', x: 108, y: 150, name: 'L3' },
          { id: 'l4', x: 500, y: 48, name: 'L4' },
          { id: 'l5', x: 500, y: 600, name: 'L5' }
        ];
        svg = '<svg class="orb-svg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(ui.farDiagram || '') + '">' +
          '<defs>' +
          '<radialGradient id="sun-glow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(255,170,60,0)"/><stop offset="42%" stop-color="rgba(255,120,40,.28)"/><stop offset="100%" stop-color="rgba(255,60,20,0)"/></radialGradient>' +
          '<radialGradient id="earth-air" cx="50%" cy="50%" r="50%"><stop offset="72%" stop-color="rgba(150,205,255,0)"/><stop offset="88%" stop-color="rgba(150,205,255,.2)"/><stop offset="100%" stop-color="rgba(150,205,255,0)"/></radialGradient>' +
          '</defs>' +
          '<circle class="sun-glow" cx="' + SX + '" cy="' + SY + '" r="' + (SR + 46) + '" fill="url(#sun-glow)"/>' +
          '<image class="sun-base" href="' + esc(sun) + '" x="' + (SX - SR - 18) + '" y="' + (SY - SR - 18) + '" width="' + ((SR + 18) * 2) + '" height="' + ((SR + 18) * 2) + '"/>' +
          '<circle class="earth-air" cx="' + EX + '" cy="' + EY + '" r="' + (ER + 22) + '" fill="url(#earth-air)"/>' +
          '<image href="' + esc(earthLg) + '" x="' + (EX - ER) + '" y="' + (EY - ER) + '" width="' + (ER * 2) + '" height="' + (ER * 2) + '"/>' +
          (moon ? '<image href="' + esc(moon) + '" x="758" y="182" width="64" height="64"/>' : '') +
          '</svg>';
      }
      geom = { W: W, H: H, cx: cx, cy: cy, r: er };
      canvas.innerHTML = svg;
      [].forEach.call(canvas.querySelectorAll('.ring-hit'), function (el) {
        var id = el.getAttribute('data-band');
        var info = bandCopy(id) || {};
        el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'button');
        el.setAttribute('aria-label', info.t || id.toUpperCase());
        function go(ev) {
          if (ev.type === 'keydown' && ev.key !== 'Enter' && ev.key !== ' ') return;
          ev.preventDefault();
          pickBand(id);
        }
        el.addEventListener('click', go);
        el.addEventListener('keydown', go);
      });
      if (which === 'near') {
        var badge = document.createElement('button');
        badge.type = 'button';
        badge.className = 'sso-mark';
        badge.textContent = 'SSO';
        badge.setAttribute('data-x', '400');
        badge.setAttribute('data-y', '210');
        badge.setAttribute('aria-pressed', selectedBand === 'sso' ? 'true' : 'false');
        var ssoInfo = bandCopy('sso') || {};
        badge.setAttribute('aria-label', (ui.ssoMark || 'SSO') + (ssoInfo.t ? '. ' + ssoInfo.t : ''));
        badge.addEventListener('click', function () { pickBand('sso'); });
        canvas.appendChild(badge);
      }
      pts.forEach(function (p) {
        var b = document.createElement('button');
        b.type = 'button';
        var reg = regimeOf(p.s);
        b.className = 'orb-btn is-' + reg;
        b.innerHTML = SAT;
        b.setAttribute('data-id', p.s.id);
        b.setAttribute('data-reg', reg);
        b.setAttribute('data-x', p.x);
        b.setAttribute('data-y', p.y);
        b.id = 'sat-' + p.s.id;
        b.setAttribute('aria-label', shortName(p.s) + '. ' + (p.s.regime === 'sso' ? (ui.ssoMark || 'SSO') + '. ' : '') + kindWord(p.s));
        b.setAttribute('aria-pressed', openId === p.s.id ? 'true' : 'false');
        b.addEventListener('click', function () { openCard(p.s, b); });
        canvas.appendChild(b);
        if (which !== 'far') addLabel(p.x, p.y, shortName(p.s), reg, function () { openCard(p.s, b); });
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
          selectedLg = g.id;
          [].forEach.call(canvas.querySelectorAll('.lag-pt'), function (el) {
            var on = el.getAttribute('data-lg') === selectedLg;
            el.classList.toggle('is-on', on);
            el.setAttribute('aria-pressed', on ? 'true' : 'false');
          });
          selectBand(g.id);
        });
        canvas.appendChild(b);
        if (which !== 'far') addLabel(g.x, g.y, g.name, g.id, function () { b.click(); });
      });
      applyView();
      if (selectedBand) paintBand(selectedBand);
    }
    function markLagrange(s) {
      var id = (s && (s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5')) ? s.regime : '';
      selectedLg = id;
      [].forEach.call(canvas.querySelectorAll('.lag-pt'), function (el) {
        var on = !!(id && el.getAttribute('data-lg') === id);
        el.classList.toggle('is-sat', on);
        el.classList.toggle('is-on', on);
        el.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }
    function eyesUrl(s) {
      var u = s && s.eyes;
      return (typeof u === 'string' && u.indexOf('https://eyes.nasa.gov/') === 0) ? u : '';
    }
    function openCard(s, btn) {
      lastBtn = btn || lastBtn;
      openId = s.id;
      markLagrange(s);
      [].forEach.call(canvas.querySelectorAll('.orb-btn'), function (el) {
        el.setAttribute('aria-pressed', el.getAttribute('data-id') === s.id ? 'true' : 'false');
      });
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
      var brief = (s.brief || []).slice(0, 5).map(function (line) { return '<p>' + esc(line) + '</p>'; }).join('');
      var whyInfo = bandCopy(s.regime);
      var why = whyInfo ? '<p class="sat-why"><strong>' + esc(whyInfo.t) + '.</strong> ' + esc(whyInfo.alt) + ' ' + esc(whyInfo.use) +
        ' <a href="' + esc(whyInfo.url) + '" target="_blank" rel="noopener">' + esc(whyInfo.src) + '</a></p>' : '';
      var more = s.official ? '<p class="sat-more-row"><a class="sat-more" href="' + esc(s.official) + '" target="_blank" rel="noopener">' + esc(ui.more || 'Click here for more information') + '</a></p>' : '';
      var eyes = eyesUrl(s);
      if (eyes) more += '<p class="sat-more-row"><a class="sat-more" href="' + esc(eyes) + '" target="_blank" rel="noopener">' + esc(ui.eyes || 'NASA Eyes') + '</a></p>';
      var kind = s.regime === 'sso' ? (ui.ssoMark || 'SSO') : kindWord(s);
      card.innerHTML = '<button type="button" class="sat-close" aria-label="' + esc(ui.close || 'Close') + '">×</button>' +
        '<h3 id="sat-card-title" class="sat-title">' + esc(shortName(s)) + '</h3>' +
        '<p class="sat-kind">' + esc(kind) + '</p>' + photo + brief + why + more;
      card.querySelector('.sat-close').addEventListener('click', closeCard);
      card.querySelector('.sat-close').focus();
    }
    function closeCard() {
      card.hidden = true;
      card.innerHTML = '';
      openId = '';
      root.querySelector('.sat-layout').classList.remove('has-card');
      markLagrange(null);
      [].forEach.call(canvas.querySelectorAll('.orb-btn'), function (el) { el.setAttribute('aria-pressed', 'false'); });
      if (lastBtn && lastBtn.focus) lastBtn.focus();
    }
    function draw() {
      var next = (cat === 'lagrange' || cat === 'beyond' || cat === 'science') ? 'far' : 'near';
      if (next !== mode) zoomT = 0;
      mode = next;
      layout(mode);
    }
    function showOrbitNote() {
      var note = document.getElementById('sat-orbit-note');
      if (!note) return;
      var order = ['leo', 'sso', 'meo', 'geo', 'heo', 'l1', 'l2'];
      var near = !(cat === 'lagrange' || cat === 'beyond' || cat === 'science');
      var drawn = near ? { leo: 1, sso: 1, meo: 1, geo: 1, heo: 1 } : { leo: 1, sso: 1, meo: 1, geo: 1, heo: 1, l1: 1, l2: 1, l5: 1 };
      var seen = [];
      sats.forEach(function (s) {
        if (!show(s)) return;
        var r = s.regime || '';
        if (drawn[r] && order.indexOf(r) >= 0 && seen.indexOf(r) < 0) seen.push(r);
      });
      var focusId = selectedBand || orbitFilter || '';
      if (focusId && seen.indexOf(focusId) < 0 && bandCopy(focusId)) seen.unshift(focusId);
      seen.sort(function (a, b) { return (a === focusId ? -1 : order.indexOf(a)) - (b === focusId ? -1 : order.indexOf(b)); });
      note.innerHTML = seen.map(function (id) {
        var info = bandCopy(id);
        if (!info) return '';
        return '<p><strong>' + esc(info.t) + '.</strong> ' + esc(info.alt) + ' ' + esc(info.use) +
          ' <a href="' + esc(info.url) + '" target="_blank" rel="noopener">' + esc(info.src) + '</a></p>';
      }).join('');
      if (!near && (ui.dL12 || ui.dL3 || ui.dL4 || ui.dL5)) {
        var missions = sats.filter(show);
        note.innerHTML += '<ul class="sat-legend">' +
          '<li>L1 / L2. ' + esc(ui.dL12 || '') + '</li>' +
          '<li>L3. ' + esc(ui.dL3 || '') + '</li>' +
          '<li>L4. ' + esc(ui.dL4 || '') + '</li>' +
          '<li>L5. ' + esc(ui.dL5 || '') + '</li></ul>' +
          '<div class="sat-mission-list">' + missions.map(function (s) {
            return '<button type="button" class="sat-mission" data-id="' + esc(s.id) + '">' + esc(shortName(s)) + '</button>';
          }).join('') + '</div>';
        [].forEach.call(note.querySelectorAll('.sat-mission'), function (b) {
          b.addEventListener('click', function () {
            var s = byId[b.getAttribute('data-id')];
            if (!s) return;
            var icon = canvas.querySelector('.orb-btn[data-id="' + s.id + '"]');
            openCard(s, icon || b);
          });
        });
      }
      note.hidden = !note.innerHTML;
    }
    function setCat(next) {
      cat = next === 'lagrange' ? 'beyond' : (next === 'all' ? 'weather' : next);
      if (cat === 'all') clearOrbit();
      [].forEach.call(root.querySelectorAll('button.wm-cat'), function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-cat') === cat ? 'true' : 'false');
      });
      var cruise = document.getElementById('sat-cruise');
      if (cruise) cruise.hidden = cat !== 'beyond';
      draw();
      showOrbitNote();
      announce();
    }
    function announce() {
      var live = document.getElementById('sat-count');
      if (!live) return;
      var n = 0;
      sats.forEach(function (s) { if (show(s)) n++; });
      live.textContent = String(ui.count || '{n}').replace('{n}', String(n));
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
    stage.parentNode.insertBefore(zbar, stage);
    zin.addEventListener('click', function () { zoomT = Math.min(1, zoomT + 0.22); applyView(); });
    zout.addEventListener('click', function () { zoomT = Math.max(0, zoomT - 0.22); applyView(); });
    zfit.addEventListener('click', function () { zoomT = 0; applyView(); });
    var orbits = document.getElementById('sat-orbits');
    if (!orbits) {
      orbits = document.createElement('div');
      orbits.className = 'sat-orbits';
      orbits.setAttribute('role', 'group');
      orbits.setAttribute('aria-label', 'LEO MEO GEO');
      stage.parentNode.insertBefore(orbits, stage);
    }
    ['leo', 'meo', 'geo', 'heo', 'sso'].forEach(function (id, i, all) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'band-btn is-' + id;
      b.textContent = id.toUpperCase();
      if (id === 'sso') b.setAttribute('aria-label', (ui.ssoMark || 'SSO') + '. SSO');
      b.setAttribute('data-band', id);
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () { pickBand(id); });
      b.addEventListener('keydown', function (e) {
        var dir = e.key === 'ArrowRight' ? (rtl ? -1 : 1) : e.key === 'ArrowLeft' ? (rtl ? 1 : -1) : 0;
        if (!dir) return;
        e.preventDefault();
        all[(i + dir + all.length) % all.length] && orbits.querySelectorAll('button')[(i + dir + all.length) % all.length].focus();
      });
      orbits.appendChild(b);
    });
    stage.parentNode.insertBefore(orbits, stage);
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
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(function () { applyView(); });
      ro.observe(stage);
    }
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
      var next = 'weather';
      if (s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5' || s.regime === 'cruise') next = 'beyond';
      else if (s.fn && s.fn !== 'nav') next = s.fn;
      setCat(next);
      if (s.regime === 'meo' && orbitFilter !== 'meo') toggleOrbit('meo');
      var btn = canvas.querySelector('.orb-btn[data-id="' + id + '"]');
      if (btn) { btn.classList.add('is-focus'); btn.focus(); }
      var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (root.scrollIntoView) root.scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' });
      openCard(s, btn || null);
    }
    window.addEventListener('hashchange', focusFromHash);
    var pend = root.getAttribute('data-pending-cat');
    root.removeAttribute('data-pending-cat');
    if (pend) setCat(pend);
    else { draw(); showOrbitNote(); announce(); }
    focusFromHash();
  }
})();
