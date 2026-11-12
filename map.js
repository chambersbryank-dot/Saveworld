/* World Map (Leaflet 1.9.4, self-hosted): solution + rocket pins. Data: assets/data/map.<lang>.json (scripts/build-map.py).
   Rocket pop-ups refresh live from Launch Library 2 (same feed as the Live Launch Tracker); falls back to the built data. */
(function () {
  var wrap = document.querySelector('.wm-wrap');
  if (!wrap || !window.L) return;
  var mapEl = document.getElementById('wm');
  var rtl = (document.documentElement.getAttribute('dir') || '') === 'rtl';
  // Oct 17: map fills the viewport below the fixed nav; measure the real nav height (CSS has 92/56 px fallbacks)
  var nav = document.getElementById('topnav') || document.querySelector('body > nav');
  function navh() { if (nav && nav.offsetHeight) document.body.style.setProperty('--wm-navh', nav.offsetHeight + 'px'); }
  navh(); window.addEventListener('resize', navh);
  var EXCL = /roscosmos|russia|china|chinese|baikonur|plesetsk|vostochny|jiuquan|wenchang|xichang|taiyuan|haiyang|dongfeng|sohae|tonghae|korean committee|nada|korean people.s|landspace|galactic energy|i-space|orienspace|deep blue aero|space pioneer|cas space|expace|casc|casic|kazakhstan/i;
  var EXCC = { RUS: 1, CHN: 1, PRK: 1 };
  fetch(wrap.getAttribute('data-src')).then(function (r) { return r.json(); }).then(boot).catch(function () {
    mapEl.innerHTML = '<p class="wm-err">Map data could not load. The list below the map has everything.</p>';
  });
  function icon(c, g) {
    return L.divIcon({ className: 'wm-pin', html: '<span class="wm-m" style="--c:' + c + '"><i>' + (g || '') + '</i></span>', iconSize: [26, 26], iconAnchor: [13, 26], popupAnchor: [0, -22] });
  }
  var GLYPH = {
    river: '<svg viewBox="0 0 24 12" aria-hidden="true"><path d="M1 7c2-3 3.2-3 5.2 0s3.2 3 5.2 0 3.2-3 5.2 0 3.4 3 6.4 0" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round"/></svg>',
    lake: '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3" fill="#fff"/></svg>',
    ocean: '<svg viewBox="0 0 24 16" aria-hidden="true"><path d="M1 5.5c1.6-1.6 2.6-1.6 4.2 0s2.6 1.6 4.2 0 2.6-1.6 4.2 0 2.6 1.6 4.2 0 2.8-1.6 4.2 0M1 10.5c1.6-1.6 2.6-1.6 4.2 0s2.6 1.6 4.2 0 2.6-1.6 4.2 0 2.6 1.6 4.2 0 2.8-1.6 4.2 0" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/></svg>',
    land: '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.2 13.2 13.2H2.8z" fill="#fff"/></svg>'
  };
  var CATBOX = { river: [28, 16, 14, 8], lake: [22, 22, 11, 11], ocean: [26, 18, 13, 9], land: [22, 22, 11, 11] };
  function catIcon(cat) {
    var b = CATBOX[cat];
    return L.divIcon({ className: 'wm-pin', html: '<span class="wm-m wm-c wm-' + cat + '"><i>' + GLYPH[cat] + '</i></span>', iconSize: [b[0], b[1]], iconAnchor: [b[2], b[3]], popupAnchor: [0, -b[3]] });
  }
  var I = { a: icon('#2e9e4f'), u: icon('#2f7fd1'), r: icon('#ffffff', '🚀') };
  var IC = { river: catIcon('river'), lake: catIcon('lake'), ocean: catIcon('ocean'), land: catIcon('land') };
  var CN = { river: 'rivers', lake: 'lakes', ocean: 'oceans', land: 'land' };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function boot(D) {
    var ui = D.ui || {}, lang = D.lang || 'en';
    var map = L.map(mapEl, { crs: L.CRS.EPSG4326, scrollWheelZoom: false, tapTolerance: 20, worldCopyJump: false, minZoom: -2, maxZoom: 5, zoomSnap: 0.25, zoomControl: false, attributionControl: false, maxBounds: [[-90, -180], [90, 180]], maxBoundsViscosity: 0.9 });
    window.wmMap = map; // Oct 28: polar-mascots.js pans to the poles
    // controls away from the floating Help button (bottom inline-end)
    L.control.zoom({ position: rtl ? 'topright' : 'topleft' }).addTo(map);
    L.control.attribution({ position: rtl ? 'bottomright' : 'bottomleft', prefix: false })
      .addAttribution('<a href="https://visibleearth.nasa.gov/images/73909/december-blue-marble-next-generation-w-topography-and-bathymetry">NASA Visible Earth / Blue Marble</a>').addTo(map);
    var WORLD = L.latLngBounds([-90, -180], [90, 180]), moved = false;
    function fit() { map.invalidateSize(); if (!moved) map.fitBounds(WORLD, { padding: [8, 8], animate: false }); }
    fit();
    map.on('dragstart zoomstart', function (e) { if (e && e.hard !== true && map._loaded && !fitting) moved = true; });
    var fitting = false, rz;
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { fitting = true; fit(); fitting = false; }, 200); });
    var pre = (wrap.getAttribute('data-src') || '').indexOf('../') === 0 ? '../' : '';
    var SIZES = [480, 800, 1280, 1920, 4096];
    function earthFile(ext, w) { return pre + 'assets/earth/blue-marble-' + w + '.' + ext; }
    var webpOk = false;
    try { webpOk = document.createElement('canvas').toDataURL('image/webp').indexOf('data:image/webp') === 0; } catch (e) {}
    var earth = L.imageOverlay(earthFile('jpg', 1280), WORLD, { alt: ui.earthAlt || 'Earth', interactive: false, className: 'wm-earth' }).addTo(map);
    function tuneEarth() {
      var img = earth.getElement(); if (!img) return;
      var ext = webpOk ? 'webp' : 'jpg';
      img.setAttribute('srcset', SIZES.map(function (n) { return earthFile(ext, n) + ' ' + n + 'w'; }).join(', '));
      img.setAttribute('sizes', Math.max(1, Math.round(mapEl.clientWidth || 800)) + 'px');
      img.decoding = 'async';
      img.loading = 'lazy';
      if (ui.earthAlt) img.alt = ui.earthAlt;
    }
    earth.on('add', tuneEarth);
    tuneEarth();
    map.on('resize', tuneEarth);
    mapEl.addEventListener('click', function () { map.scrollWheelZoom.enable(); });
    mapEl.addEventListener('mouseleave', function () { map.scrollWheelZoom.disable(); });
    var groups = { a: L.layerGroup().addTo(map), u: L.layerGroup().addTo(map), r: L.layerGroup().addTo(map) }, all = [];
    (D.sols || []).forEach(function (s) {
      var k = s.st === 'upcoming' ? 'u' : 'a';
      (s.p || []).forEach(function (p) {
        var basis = p.basis === 'hq' ? ' (' + (ui.basis_hq || 'HQ') + ')' : '';
        var m = L.marker([p.lat, p.lng], { icon: (s.c && IC[s.c]) || I[k], title: s.n, alt: s.n });
        var catLine = s.c && ui[CN[s.c]] ? '<p class="wm-pop-cat">' + esc(ui[CN[s.c]]) + '</p>' : '';
        m.bindPopup('<div class="wm-pop"><p class="wm-pop-h">' + esc(s.n) + '</p><p class="wm-pop-hub"><span class="wm-badge wm-' + (k === 'a' ? 'active' : 'upcoming') + '">' + esc(k === 'a' ? ui.active : ui.upcoming) + '</span> ' + esc(s.hn) + '</p>' + catLine + '<p>' + esc(s.s) + '</p><p class="wm-pop-loc">📍 ' + esc(p.label) + esc(basis) + '</p><p><a href="' + esc(s.u) + '">' + esc(ui.read || 'Read more') + ' →</a></p></div>');
        m._k = k; m._h = s.h; m._c = s.c || ''; all.push(m); groups[k].addLayer(m);
      });
    });
    var sites = D.sites || [], rmk = [];
    function drawRockets() {
      rmk.forEach(function (m) { groups.r.removeLayer(m); }); rmk = [];
      sites.forEach(function (st) {
        var m = L.marker([st.lat, st.lng], { icon: I.r, title: st.name, alt: st.name, zIndexOffset: 500 });
        m.bindPopup(function () { return rocketHtml(st); }); m._k = 'r'; rmk.push(m); groups.r.addLayer(m);
      });
    }
    function rocketHtml(st) {
      var li = (st.launches || []).slice(0, 8).map(function (x) {
        return '<li><strong>' + esc(fmt(x)) + ':</strong> ' + esc(x.provider) + ' – ' + esc(x.mission) + '</li>';
      }).join('');
      return '<div class="wm-pop wm-rocket"><p class="wm-pop-h">🚀 ' + esc(st.name) + '</p><p class="wm-pop-hub">' + esc(ui.next) + '</p>' + (li ? '<ul>' + li + '</ul>' : '<p>' + esc(ui.none) + '</p>') + '</div>';
    }
    function fmt(x) {
      var d = new Date(x.net); if (!x.net || isNaN(d)) return ui.tbd;
      if (x.exact) return d.toLocaleDateString(lang, { month: 'short', day: 'numeric' });
      return d.toLocaleDateString(lang, { month: 'long', year: 'numeric' }) + ' (' + ui.tbd + ')';
    }
    drawRockets();
    // live refresh (same Launch Library 2 feed as the Live Launch Tracker); keep built data if it fails or is rate-limited
    fetch('https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=100&mode=normal', { headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
        var by = {}; sites.forEach(function (s) { s.launches = []; by[s.name] = s; });
        (j.results || []).forEach(function (r) {
          var p = r.pad || {}, loc = (p.location || {}).name || '', cc = (p.country || {}).alpha_3_code || '', prov = (r.launch_service_provider || {}).name || '';
          if (EXCC[cc] || EXCL.test(loc + ' | ' + prov)) return;
          var la = +p.latitude, ln = +p.longitude; if (isNaN(la)) return;
          var s = by[loc];
          if (!s) sites.forEach(function (q) { if (!s && Math.abs(q.lat - la) < .08 && Math.abs(q.lng - ln) < .08) s = q; });
          if (!s) { s = { name: loc, lat: la, lng: ln, launches: [] }; sites.push(s); by[loc] = s; }
          var nm = r.name || '', pr = (r.net_precision || {}).abbrev || '';
          s.launches.push({ net: r.net, exact: !pr || /^(SEC|MIN|HR|DAY)/.test(pr), provider: prov, mission: nm.indexOf('|') > -1 ? nm.split('|')[1].trim() : nm });
        });
        drawRockets(); apply();
      }).catch(function () {});
    var cat = 'all';
    function apply() {
      var hub = document.getElementById('wm-hub').value;
      var on = { a: document.getElementById('wm-a').checked, u: document.getElementById('wm-u').checked, r: document.getElementById('wm-r').checked };
      all.forEach(function (m) {
        var catOk = cat === 'all' || m._c === cat;
        var ok = on[m._k] && (hub === 'all' || m._h === hub) && catOk;
        if (ok) groups[m._k].addLayer(m); else groups[m._k].removeLayer(m);
      });
      if (on.r && cat === 'all') map.addLayer(groups.r); else map.removeLayer(groups.r);
      document.querySelectorAll('.wm-chips li[data-hub], .wm-list li[data-cat], .wm-list li[data-hub]').forEach(function (li) {
        var hubOk = !li.getAttribute('data-hub') || hub === 'all' || li.getAttribute('data-hub') === hub;
        var c = li.getAttribute('data-cat') || '';
        var catOk = cat === 'all' || (c && c !== 'launch' && c === cat);
        if (c === 'launch') catOk = cat === 'all';
        li.hidden = !(hubOk && catOk);
      });
    }
    var catBtns = [].slice.call(document.querySelectorAll('.wm-cat'));
    function setCat(next) {
      cat = next;
      catBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-cat') === next ? 'true' : 'false'); });
      apply();
    }
    catBtns.forEach(function (b, i) {
      b.addEventListener('click', function () { setCat(b.getAttribute('data-cat')); });
      b.addEventListener('keydown', function (e) {
        var dir = 0, k = e.key;
        if (k === 'ArrowDown') dir = 1;
        else if (k === 'ArrowUp') dir = -1;
        else if (k === 'ArrowRight') dir = rtl ? -1 : 1;
        else if (k === 'ArrowLeft') dir = rtl ? 1 : -1;
        else if (k === 'Home') { e.preventDefault(); catBtns[0].focus(); return; }
        else if (k === 'End') { e.preventDefault(); catBtns[catBtns.length - 1].focus(); return; }
        if (!dir) return;
        e.preventDefault();
        catBtns[(i + dir + catBtns.length) % catBtns.length].focus();
      });
    });
    ['wm-hub', 'wm-a', 'wm-u', 'wm-r'].forEach(function (id) { document.getElementById(id).addEventListener('change', apply); });
    window.spWorldMap = { map: map, count: function () { var c = { a: 0, u: 0, r: 0 }; ['a', 'u', 'r'].forEach(function (k) { c[k] = groups[k].getLayers().length; }); return c; } };
    setTimeout(function () { fitting = true; fit(); fitting = false; }, 250);
  }
})();
