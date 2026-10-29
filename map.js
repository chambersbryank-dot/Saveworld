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
  var I = { a: icon('#2e9e4f'), u: icon('#2f7fd1'), r: icon('#ffffff', '🚀') };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function boot(D) {
    var ui = D.ui || {}, lang = D.lang || 'en';
    var map = L.map(mapEl, { scrollWheelZoom: false, tapTolerance: 20, worldCopyJump: true, minZoom: 1, zoomSnap: 0.25, zoomControl: false, attributionControl: false });
    window.wmMap = map; // Oct 28: polar-mascots.js pans to the poles
    // controls away from the floating Help button (bottom inline-end) and the map key (top inline-end)
    L.control.zoom({ position: rtl ? 'topright' : 'topleft' }).addTo(map);
    L.control.attribution({ position: rtl ? 'bottomright' : 'bottomleft', prefix: false }).addTo(map);
    var WORLD = L.latLngBounds([-50, -165], [72, 180]), moved = false;
    function fit() { map.invalidateSize(); if (!moved) map.fitBounds(WORLD, { padding: [8, 8], animate: false }); }
    fit();
    map.on('dragstart zoomstart', function (e) { if (e && e.hard !== true && map._loaded && !fitting) moved = true; });
    var fitting = false, rz;
    window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { fitting = true; fit(); fitting = false; }, 200); });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> · ' + esc(ui.launches || 'Launches') + ': <a href="https://thespacedevs.com/llapi">The Space Devs</a>',
      subdomains: 'abc', maxZoom: 19 }).addTo(map);
    mapEl.addEventListener('click', function () { map.scrollWheelZoom.enable(); });
    mapEl.addEventListener('mouseleave', function () { map.scrollWheelZoom.disable(); });
    var groups = { a: L.layerGroup().addTo(map), u: L.layerGroup().addTo(map), r: L.layerGroup().addTo(map) }, all = [];
    (D.sols || []).forEach(function (s) {
      var k = s.st === 'upcoming' ? 'u' : 'a';
      (s.p || []).forEach(function (p) {
        var basis = p.basis === 'hq' ? ' (' + (ui.basis_hq || 'HQ') + ')' : '';
        var m = L.marker([p.lat, p.lng], { icon: I[k], title: s.n, alt: s.n });
        m.bindPopup('<div class="wm-pop"><p class="wm-pop-h">' + esc(s.n) + '</p><p class="wm-pop-hub"><span class="wm-badge wm-' + (k === 'a' ? 'active' : 'upcoming') + '">' + esc(k === 'a' ? ui.active : ui.upcoming) + '</span> ' + esc(s.hn) + '</p><p>' + esc(s.s) + '</p><p class="wm-pop-loc">📍 ' + esc(p.label) + esc(basis) + '</p><p><a href="' + esc(s.u) + '">' + esc(ui.read || 'Read more') + ' →</a></p></div>');
        m._k = k; m._h = s.h; all.push(m); groups[k].addLayer(m);
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
    function apply() {
      var hub = document.getElementById('wm-hub').value;
      var on = { a: document.getElementById('wm-a').checked, u: document.getElementById('wm-u').checked, r: document.getElementById('wm-r').checked };
      all.forEach(function (m) { var ok = on[m._k] && (hub === 'all' || m._h === hub); if (ok) groups[m._k].addLayer(m); else groups[m._k].removeLayer(m); });
      if (on.r) map.addLayer(groups.r); else map.removeLayer(groups.r);
      document.querySelectorAll('.wm-chips li[data-hub], .wm-list li[data-hub]').forEach(function (li) { li.hidden = hub !== 'all' && li.getAttribute('data-hub') !== hub; });
    }
    ['wm-hub', 'wm-a', 'wm-u', 'wm-r'].forEach(function (id) { document.getElementById(id).addEventListener('change', apply); });
    window.spWorldMap = { map: map, count: function () { var c = { a: 0, u: 0, r: 0 }; ['a', 'u', 'r'].forEach(function (k) { c[k] = groups[k].getLayers().length; }); return c; } };
    setTimeout(function () { fitting = true; fit(); fitting = false; }, 250);
  }
})();
