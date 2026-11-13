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
    var geom = null, zoomT = 0, selectedLg = '', orbitFilter = '';
    sats.forEach(function (s) { byId[s.id] = s; });
    var pre = (root.getAttribute('data-src') || '').indexOf('../') === 0 ? '../' : '';
    var cut = pre + 'assets/earth/cut/';
    var earth = cut + 'earth.webp';
    var earthLg = earth;
    var moon = cut + 'moon.webp';
    var sun = cut + 'sun.webp';
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
        add(400 - 246, 268 - 102); add(400 + 246, 268 + 102);
        add(440 - 196, 268 - 118); add(440 + 196, 268 + 118);
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
      var b = contentBox(), map = mapRect(W, H);
      var bw = Math.max(40, (b.maxX - b.minX) * 1.08), bh = Math.max(40, (b.maxY - b.minY) * 1.08);
      return viewFrom((b.minX + b.maxX) / 2, (b.minY + b.maxY) / 2, bw, bh, map, W, H);
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
      if (W < 40 || H < 40) return;
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
        var nx = (x - view0.cx) / Math.max(view0.bw, 1);
        return { el: el, x: x, y: y, side: nx < 0 ? 'l' : 'r', ny: y };
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
      if (gut.l + gut.r > W * 0.78) {
        var share = W * 0.78, scale = share / (gut.l + gut.r);
        gut.l *= scale; gut.r *= scale;
        lw = nL ? Math.max(36, (gut.l - 18 - Math.max(0, nL - 1) * 4) / nL) : lw;
        rw = nR ? Math.max(36, (gut.r - 18 - Math.max(0, nR - 1) * 4) / nR) : rw;
        labs.forEach(function (el) { el.style.maxWidth = Math.min(lw, rw) + 'px'; });
      }
      var view = currentView();
      var svg = canvas.querySelector('svg.orb-svg');
      if (svg) svg.setAttribute('viewBox', view.x + ' ' + view.y + ' ' + view.w + ' ' + view.h);
      [].forEach.call(canvas.querySelectorAll('.orb-btn,.lag-pt'), function (el) {
        var x = +el.getAttribute('data-x'), y = +el.getAttribute('data-y');
        var px = (x - view.x) / view.w * W, py = (y - view.y) / view.h * H;
        el.style.left = px + 'px';
        el.style.top = py + 'px';
        var inside = px >= gut.l - 20 && px <= W - gut.r + 20 && py >= -8 && py <= H + 8;
        el.classList.toggle('is-off', !inside);
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
      stack(left, 'l', lw); stack(right, 'r', rw);
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
    var BAND = ({
      en: {
        leo: {t:'LEO: Low Earth orbit', alt:'About 180 km to 2,000 km above Earth.', use:'ESA says this closeness is useful for satellite imaging, because it allows higher-resolution images.', src:'ESA, Types of orbits', url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
        meo: {t:'MEO: Medium Earth orbit', alt:'Above about 2,000 km and below the geostationary height of 35,786 km.', use:'ESA says this range is very commonly used by navigation satellites, such as Galileo.', src:'ESA, Types of orbits', url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
        geo: {t:'GEO: Geostationary orbit', alt:'35,786 km above the equator. The start and the end of this band are the same height.', use:'ESA says these satellites appear stationary over one fixed spot.', src:'ESA, Types of orbits', url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
        heo: {t:'HEO: Highly eccentric orbit', alt:'No single height. The satellite moves closer to Earth and then farther away.', use:'ESA says the distance from Earth’s surface changes during one orbit.', src:'ESA, Types of orbits', url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
        sso: {t:'SSO: Sun-synchronous orbit', alt:'Usually 600 km to 800 km, inside low Earth orbit.', use:'ESA says the satellite usually crosses at a steady local time, so the lighting stays consistent.', src:'ESA, Types of orbits', url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
        l1: {t:'L1: Sun–Earth Lagrange point', alt:'About 1.5 million km from Earth. It does not orbit Earth directly.', use:'ESA says a spacecraft can stay near this point with little effort, anchored relative to Earth.', src:'ESA, Types of orbits', url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
        l2: {t:'L2: Sun–Earth Lagrange point', alt:'About 1.5 million km from Earth, on the night side. It does not orbit Earth directly.', use:'ESA says a spacecraft can stay near this point with little effort, anchored relative to Earth.', src:'ESA, Types of orbits', url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
        l3: {t:'L3: Sun–Earth Lagrange point', alt:'About 2 AU from Earth, on the far side of the Sun.', use:'NASA says L3 sits on the Sun–Earth line and is unstable.', src:'NASA, What is a Lagrange Point?', url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
        l4: {t:'L4: Sun–Earth Lagrange point', alt:'About 1 AU from Earth, 60 degrees ahead.', use:'NASA says L4 is at the tip of an equilateral triangle and is stable.', src:'NASA, What is a Lagrange Point?', url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
        l5: {t:'L5: Sun–Earth Lagrange point', alt:'About 1 AU from Earth, 60 degrees behind.', use:'NASA says L5 is at the tip of an equilateral triangle and is stable.', src:'NASA, What is a Lagrange Point?', url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'}
      }
    })[D.lang] || null;
    var BAND_EN = null;
    if (!BAND) BAND = {
      leo:{t:'LEO: Low Earth orbit',alt:'About 180 km to 2,000 km above Earth.',use:'ESA says this closeness is useful for satellite imaging, because it allows higher-resolution images.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'}
    };
    var BANDS = {
      en: null
    };
    function bandCopy(id) {
      var pack = ({
        fr: {
          leo:{t:'LEO : orbite terrestre basse',alt:'Environ 180 km à 2 000 km au-dessus de la Terre.',use:'L’ESA dit que cette proximité sert à l’imagerie, car elle permet une résolution plus fine.',src:'ESA, Types d’orbites',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          meo:{t:'MEO : orbite terrestre moyenne',alt:'Au-dessus d’environ 2 000 km et sous l’altitude géostationnaire de 35 786 km.',use:'L’ESA dit que cette plage sert très souvent aux satellites de navigation, comme Galileo.',src:'ESA, Types d’orbites',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          geo:{t:'GEO : orbite géostationnaire',alt:'35 786 km au-dessus de l’équateur. Le début et la fin de cette bande sont la même altitude.',use:'L’ESA dit que ces satellites paraissent fixes au-dessus d’un seul endroit.',src:'ESA, Types d’orbites',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          heo:{t:'HEO : orbite très excentrique',alt:'Pas une seule altitude. Le satellite se rapproche de la Terre, puis s’en éloigne.',use:'L’ESA dit que la distance à la surface change au cours d’une orbite.',src:'ESA, Types d’orbites',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          sso:{t:'SSO : orbite héliosynchrone',alt:'En général 600 km à 800 km, dans l’orbite basse.',use:'L’ESA dit que le satellite passe d’habitude à une heure locale stable, donc l’éclairage reste semblable.',src:'ESA, Types d’orbites',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l1:{t:'L1 : point de Lagrange Soleil–Terre',alt:'Environ 1,5 million de km de la Terre. Il n’orbite pas la Terre directement.',use:'L’ESA dit qu’un engin peut rester près de ce point avec peu d’effort, ancré par rapport à la Terre.',src:'ESA, Types d’orbites',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l2:{t:'L2 : point de Lagrange Soleil–Terre',alt:'Environ 1,5 million de km de la Terre, du côté nuit. Il n’orbite pas la Terre directement.',use:'L’ESA dit qu’un engin peut rester près de ce point avec peu d’effort, ancré par rapport à la Terre.',src:'ESA, Types d’orbites',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l3:{t:'L3 : point de Lagrange Soleil–Terre',alt:'Environ 2 UA de la Terre, de l’autre côté du Soleil.',use:'La NASA dit que L3 est sur la ligne Soleil–Terre et qu’il est instable.',src:'NASA, Qu’est-ce qu’un point de Lagrange ?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l4:{t:'L4 : point de Lagrange Soleil–Terre',alt:'Environ 1 UA de la Terre, 60 degrés devant.',use:'La NASA dit que L4 est au sommet d’un triangle équilatéral et qu’il est stable.',src:'NASA, Qu’est-ce qu’un point de Lagrange ?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l5:{t:'L5 : point de Lagrange Soleil–Terre',alt:'Environ 1 UA de la Terre, 60 degrés derrière.',use:'La NASA dit que L5 est au sommet d’un triangle équilatéral et qu’il est stable.',src:'NASA, Qu’est-ce qu’un point de Lagrange ?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'}
        },
        es: {
          leo:{t:'LEO: órbita terrestre baja',alt:'Unos 180 km a 2.000 km sobre la Tierra.',use:'La ESA dice que esta cercanía sirve para las imágenes, porque permite más resolución.',src:'ESA, Tipos de órbitas',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          meo:{t:'MEO: órbita terrestre media',alt:'Por encima de unos 2.000 km y por debajo de la altura geoestacionaria de 35.786 km.',use:'La ESA dice que esta franja se usa mucho para satélites de navegación, como Galileo.',src:'ESA, Tipos de órbitas',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          geo:{t:'GEO: órbita geoestacionaria',alt:'35.786 km sobre el ecuador. El inicio y el final de esta banda son la misma altura.',use:'La ESA dice que estos satélites parecen quietos sobre un solo lugar.',src:'ESA, Tipos de órbitas',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          heo:{t:'HEO: órbita muy excéntrica',alt:'No hay una sola altura. El satélite se acerca a la Tierra y luego se aleja.',use:'La ESA dice que la distancia a la superficie cambia durante una órbita.',src:'ESA, Tipos de órbitas',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          sso:{t:'SSO: órbita heliosíncrona',alt:'Por lo general de 600 km a 800 km, dentro de la órbita baja.',use:'La ESA dice que el satélite suele cruzar a una hora local fija, así que la luz se mantiene parecida.',src:'ESA, Tipos de órbitas',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l1:{t:'L1: punto de Lagrange Sol–Tierra',alt:'Unos 1,5 millones de km de la Tierra. No orbita la Tierra directamente.',use:'La ESA dice que una nave puede quedarse cerca de este punto con poco esfuerzo, anclada respecto a la Tierra.',src:'ESA, Tipos de órbitas',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l2:{t:'L2: punto de Lagrange Sol–Tierra',alt:'Unos 1,5 millones de km de la Tierra, en el lado de noche. No orbita la Tierra directamente.',use:'La ESA dice que una nave puede quedarse cerca de este punto con poco esfuerzo, anclada respecto a la Tierra.',src:'ESA, Tipos de órbitas',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l3:{t:'L3: punto de Lagrange Sol–Tierra',alt:'Unas 2 UA de la Tierra, al otro lado del Sol.',use:'La NASA dice que L3 está en la línea Sol–Tierra y que es inestable.',src:'NASA, ¿Qué es un punto de Lagrange?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l4:{t:'L4: punto de Lagrange Sol–Tierra',alt:'Cerca de 1 UA de la Tierra, 60 grados por delante.',use:'La NASA dice que L4 está en la punta de un triángulo equilátero y que es estable.',src:'NASA, ¿Qué es un punto de Lagrange?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l5:{t:'L5: punto de Lagrange Sol–Tierra',alt:'Cerca de 1 UA de la Tierra, 60 grados por detrás.',use:'La NASA dice que L5 está en la punta de un triángulo equilátero y que es estable.',src:'NASA, ¿Qué es un punto de Lagrange?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'}
        },
        ar: {
          leo:{t:'LEO: مدار أرضي منخفض',alt:'نحو 180 كم إلى 2000 كم فوق الأرض.',use:'تقول وكالة الفضاء الأوروبية إن هذا القرب مفيد لتصوير الأرض، لأنه يتيح صورة أوضح.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          meo:{t:'MEO: مدار أرضي متوسط',alt:'فوق نحو 2000 كم وتحت الارتفاع الثابت جغرافيًا البالغ 35786 كم.',use:'تقول وكالة الفضاء الأوروبية إن هذا المدى يُستخدم كثيرًا لأقمار الملاحة، مثل غاليليو.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          geo:{t:'GEO: مدار ثابت جغرافيًا',alt:'35786 كم فوق خط الاستواء. بداية هذا النطاق ونهايته الارتفاع نفسه.',use:'تقول وكالة الفضاء الأوروبية إن هذه الأقمار تبدو ثابتة فوق مكان واحد.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          heo:{t:'HEO: مدار شديد الإهليلجية',alt:'ليس ارتفاعًا واحدًا. يقترب القمر من الأرض ثم يبتعد.',use:'تقول وكالة الفضاء الأوروبية إن البعد عن السطح يتغير خلال مدار واحد.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          sso:{t:'SSO: مدار متزامن مع الشمس',alt:'عادة من 600 كم إلى 800 كم، داخل المدار المنخفض.',use:'تقول وكالة الفضاء الأوروبية إن القمر يمر عادة في وقت محلي ثابت، فيبقى الضوء متشابهًا.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l1:{t:'L1: نقطة لاغرانج الشمس–الأرض',alt:'نحو 1.5 مليون كم من الأرض. لا يدور حول الأرض مباشرة.',use:'تقول وكالة الفضاء الأوروبية إن مركبة يمكن أن تبقى قرب هذه النقطة بجهد قليل، مثبتة بالنسبة إلى الأرض.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l2:{t:'L2: نقطة لاغرانج الشمس–الأرض',alt:'نحو 1.5 مليون كم من الأرض، في جهة الليل. لا يدور حول الأرض مباشرة.',use:'تقول وكالة الفضاء الأوروبية إن مركبة يمكن أن تبقى قرب هذه النقطة بجهد قليل، مثبتة بالنسبة إلى الأرض.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l3:{t:'L3: نقطة لاغرانج الشمس–الأرض',alt:'نحو 2 وحدة فلكية من الأرض، خلف الشمس.',use:'تقول ناسا إن L3 على خط الشمس–الأرض وإنها غير مستقرة.',src:'NASA, What is a Lagrange Point?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l4:{t:'L4: نقطة لاغرانج الشمس–الأرض',alt:'نحو 1 وحدة فلكية من الأرض، بزاوية 60 درجة أمامها.',use:'تقول ناسا إن L4 عند رأس مثلث متساوي الأضلاع وإنها مستقرة.',src:'NASA, What is a Lagrange Point?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l5:{t:'L5: نقطة لاغرانج الشمس–الأرض',alt:'نحو 1 وحدة فلكية من الأرض، بزاوية 60 درجة خلفها.',use:'تقول ناسا إن L5 عند رأس مثلث متساوي الأضلاع وإنها مستقرة.',src:'NASA, What is a Lagrange Point?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'}
        },
        it: {
          leo:{t:'LEO: orbita terrestre bassa',alt:'Circa 180 km fino a 2.000 km sopra la Terra.',use:'L’ESA dice che questa vicinanza serve alle immagini, perché permette una risoluzione più fine.',src:'ESA, Tipi di orbite',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          meo:{t:'MEO: orbita terrestre media',alt:'Sopra circa 2.000 km e sotto la quota geostazionaria di 35.786 km.',use:'L’ESA dice che questa fascia è usata molto spesso dai satelliti di navigazione, come Galileo.',src:'ESA, Tipi di orbite',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          geo:{t:'GEO: orbita geostazionaria',alt:'35.786 km sopra l’equatore. L’inizio e la fine di questa fascia sono la stessa quota.',use:'L’ESA dice che questi satelliti sembrano fermi sopra un solo punto.',src:'ESA, Tipi di orbite',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          heo:{t:'HEO: orbita molto eccentrica',alt:'Non una sola quota. Il satellite si avvicina alla Terra e poi si allontana.',use:'L’ESA dice che la distanza dalla superficie cambia durante un’orbita.',src:'ESA, Tipi di orbite',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          sso:{t:'SSO: orbita eliosincrona',alt:'Di solito da 600 km a 800 km, dentro l’orbita bassa.',use:'L’ESA dice che il satellite di solito attraversa a un’ora locale stabile, così la luce resta simile.',src:'ESA, Tipi di orbite',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l1:{t:'L1: punto di Lagrange Sole–Terra',alt:'Circa 1,5 milioni di km dalla Terra. Non orbita la Terra direttamente.',use:'L’ESA dice che un veicolo può restare vicino a questo punto con poco sforzo, ancorato rispetto alla Terra.',src:'ESA, Tipi di orbite',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l2:{t:'L2: punto di Lagrange Sole–Terra',alt:'Circa 1,5 milioni di km dalla Terra, sul lato notte. Non orbita la Terra direttamente.',use:'L’ESA dice che un veicolo può restare vicino a questo punto con poco sforzo, ancorato rispetto alla Terra.',src:'ESA, Tipi di orbite',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l3:{t:'L3: punto di Lagrange Sole–Terra',alt:'Circa 2 UA dalla Terra, oltre il Sole.',use:'La NASA dice che L3 sta sulla linea Sole–Terra ed è instabile.',src:'NASA, Che cos’è un punto di Lagrange?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l4:{t:'L4: punto di Lagrange Sole–Terra',alt:'Circa 1 UA dalla Terra, 60 gradi davanti.',use:'La NASA dice che L4 è al vertice di un triangolo equilatero ed è stabile.',src:'NASA, Che cos’è un punto di Lagrange?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l5:{t:'L5: punto di Lagrange Sole–Terra',alt:'Circa 1 UA dalla Terra, 60 gradi dietro.',use:'La NASA dice che L5 è al vertice di un triangolo equilatero ed è stabile.',src:'NASA, Che cos’è un punto di Lagrange?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'}
        },
        he: {
          leo:{t:'LEO: מסלול ארצי נמוך',alt:'כ-180 ק״מ עד 2,000 ק״מ מעל כדור הארץ.',use:'סוכנות החלל האירופית אומרת שהקרבה הזו מועילה לצילום, כי היא מאפשרת תמונה חדה יותר.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          meo:{t:'MEO: מסלול ארצי בינוני',alt:'מעל כ-2,000 ק״מ ומתחת לגובה הגיאוסטציונרי של 35,786 ק״מ.',use:'סוכנות החלל האירופית אומרת שהטווח הזה משמש הרבה לווייני ניווט, כמו גלילאו.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          geo:{t:'GEO: מסלול גיאוסטציונרי',alt:'35,786 ק״מ מעל קו המשווה. ההתחלה והסוף של הרצועה הם אותו גובה.',use:'סוכנות החלל האירופית אומרת שהלוויינים האלה נראים קבועים מעל מקום אחד.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          heo:{t:'HEO: מסלול אליפטי מאוד',alt:'אין גובה אחד. הלוויין מתקרב לכדור הארץ ואז מתרחק.',use:'סוכנות החלל האירופית אומרת שהמרחק מהקרקע משתנה במהלך מסלול אחד.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          sso:{t:'SSO: מסלול מסונכרן-שמש',alt:'בדרך כלל 600 עד 800 ק״מ, בתוך המסלול הנמוך.',use:'סוכנות החלל האירופית אומרת שהלוויין חוצה בדרך כלל בשעה מקומית קבועה, ולכן התאורה נשארת דומה.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l1:{t:'L1: נקודת לגראנז׳ שמש–ארץ',alt:'כ-1.5 מיליון ק״מ מכדור הארץ. היא לא מקיפה את כדור הארץ ישירות.',use:'סוכנות החלל האירופית אומרת שחללית יכולה להישאר ליד הנקודה במעט מאמץ, מעוגנת ביחס לכדור הארץ.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l2:{t:'L2: נקודת לגראנז׳ שמש–ארץ',alt:'כ-1.5 מיליון ק״מ מכדור הארץ, בצד הלילה. היא לא מקיפה את כדור הארץ ישירות.',use:'סוכנות החלל האירופית אומרת שחללית יכולה להישאר ליד הנקודה במעט מאמץ, מעוגנת ביחס לכדור הארץ.',src:'ESA, Types of orbits',url:'https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits'},
          l3:{t:'L3: נקודת לגראנז׳ שמש–ארץ',alt:'כ-2 יחידות אסטרונומיות מכדור הארץ, מעבר לשמש.',use:'נאס״א אומרת ש-L3 יושבת על קו השמש–ארץ ואינה יציבה.',src:'NASA, What is a Lagrange Point?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l4:{t:'L4: נקודת לגראנז׳ שמש–ארץ',alt:'כ-1 יחידה אסטרונומית מכדור הארץ, 60 מעלות לפניו.',use:'נאס״א אומרת ש-L4 בקודקוד של משולש שווה צלעות והיא יציבה.',src:'NASA, What is a Lagrange Point?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'},
          l5:{t:'L5: נקודת לגראנז׳ שמש–ארץ',alt:'כ-1 יחידה אסטרונומית מכדור הארץ, 60 מעלות אחריו.',use:'נאס״א אומרת ש-L5 בקודקוד של משולש שווה צלעות והיא יציבה.',src:'NASA, What is a Lagrange Point?',url:'https://science.nasa.gov/resource/what-is-a-lagrange-point/'}
        }
      })[D.lang];
      if (pack && pack[id]) return pack[id];
      return (BAND && BAND[id]) ? BAND[id] : null;
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
        var info = bandCopy(id);
        if (!info) { bandBox.hidden = true; return; }
        bandBox.hidden = false;
        bandBox.innerHTML = '<button type="button" class="sat-close" aria-label="' + esc(ui.close || 'Close') + '">×</button>' +
          '<h3 id="sat-band-h">' + esc(info.t) + '</h3><p>' + esc(info.alt) + '</p><p>' + esc(info.use) + '</p>' +
          '<p class="sat-photo-credit"><a href="' + esc(info.url) + '" target="_blank" rel="noopener">' + esc(info.src) + '</a></p>';
        bandBox.querySelector('button').addEventListener('click', function () { selectedBand = ''; bandBox.hidden = true; paintBand(''); });
        paintBand(id);
      }
      [].forEach.call(canvas.querySelectorAll('.band-btn'), function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-band') === selectedBand ? 'true' : 'false');
      });
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
    function addLabel(x, y, text, reg) {
      var lab = document.createElement('span');
      lab.className = 'orb-lab is-' + (reg || 'x');
      lab.textContent = text;
      lab.setAttribute('data-x', x);
      lab.setAttribute('data-y', y);
      lab.setAttribute('data-reg', reg || '');
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
      var info = bandCopy(id);
      if (!info) { bandBox.hidden = true; return; }
      bandBox.hidden = false;
      bandBox.innerHTML = '<button type="button" class="sat-close" aria-label="' + esc(ui.close || 'Close') + '">×</button>' +
        '<h3 id="sat-band-h">' + esc(info.t) + '</h3><p>' + esc(info.alt) + '</p><p>' + esc(info.use) + '</p>' +
        '<p class="sat-photo-credit"><a href="' + esc(info.url) + '" target="_blank" rel="noopener">' + esc(info.src) + '</a></p>';
      bandBox.querySelector('button').addEventListener('click', function () {
        if (id === 'leo' || id === 'meo' || id === 'geo') toggleOrbit(id);
        else { selectedBand = ''; bandBox.hidden = true; paintBand(''); syncOrbit(); }
      });
    }
    function syncOrbit() {
      [].forEach.call(root.querySelectorAll('.sat-orbits button'), function (b) {
        var id = b.getAttribute('data-band');
        var pressed = (id === 'leo' || id === 'meo' || id === 'geo') ? orbitFilter === id : selectedBand === id;
        b.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      });
    }
    function clearOrbit() {
      orbitFilter = '';
      selectedBand = '';
      bandBox.hidden = true;
      paintBand('');
      syncOrbit();
      applyDim();
    }
    function toggleOrbit(id) {
      if (orbitFilter === id) { clearOrbit(); return; }
      orbitFilter = id;
      selectedBand = id;
      showBandInfo(id);
      paintBand(id);
      syncOrbit();
      applyDim();
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
          '<defs></defs>' +
          '<ellipse class="ring ring-leo" cx="400" cy="268" rx="118" ry="50" fill="none" stroke="#7ad7ff" stroke-width="2"/>' +
          '<ellipse class="ring ring-meo" cx="400" cy="268" rx="178" ry="74" fill="none" stroke="#ffb703" stroke-width="2"/>' +
          '<ellipse class="ring ring-geo" cx="400" cy="268" rx="246" ry="102" fill="none" stroke="#e2b6ff" stroke-width="2"/>' +
          '<ellipse class="ring ring-heo" cx="440" cy="268" rx="196" ry="118" fill="none" stroke="#ffd166" stroke-width="1.6" stroke-dasharray="5 4"/>' +
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
          '<radialGradient id="sun-glow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(255,170,60,0)"/><stop offset="42%" stop-color="rgba(255,120,40,.28)"/><stop offset="100%" stop-color="rgba(255,60,20,0)"/></radialGradient>' +
          '<radialGradient id="earth-air" cx="50%" cy="50%" r="50%"><stop offset="72%" stop-color="rgba(150,205,255,0)"/><stop offset="88%" stop-color="rgba(150,205,255,.2)"/><stop offset="100%" stop-color="rgba(150,205,255,0)"/></radialGradient>' +
          '</defs>' +
          '<circle class="sun-glow" cx="' + SX + '" cy="' + SY + '" r="' + (SR + 46) + '" fill="url(#sun-glow)"/>' +
          '<image class="sun-base" href="' + esc(sun) + '" x="' + (SX - SR - 18) + '" y="' + (SY - SR - 18) + '" width="' + ((SR + 18) * 2) + '" height="' + ((SR + 18) * 2) + '"/>' +
          '<circle class="earth-air" cx="' + EX + '" cy="' + EY + '" r="' + (ER + 22) + '" fill="url(#earth-air)"/>' +
          '<image href="' + esc(earthLg) + '" x="' + (EX - ER) + '" y="' + (EY - ER) + '" width="' + (ER * 2) + '" height="' + (ER * 2) + '"/>' +
          (moon ? '<image href="' + esc(moon) + '" x="758" y="182" width="64" height="64"/>' : '') +
          dist(250, 248, ui.dL12) + dist(860, 248, ui.dL12) + dist(108, 188, ui.dL3) + dist(500, 86, ui.dL4) + dist(500, 624, ui.dL5) +
          '</svg>';
      }
      geom = { W: W, H: H, cx: cx, cy: cy, r: er };
      canvas.innerHTML = svg;
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
        b.setAttribute('aria-label', shortName(p.s) + '. ' + kindWord(p.s));
        b.addEventListener('click', function () { openCard(p.s, b); });
        canvas.appendChild(b);
        addLabel(p.x, p.y, shortName(p.s), reg);
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
        addLabel(g.x, g.y, g.name, g.id);
      });
      applyView();
      if (selectedBand) paintBand(selectedBand);
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
      var brief = (s.brief || []).slice(0, 5).map(function (line) { return '<p>' + esc(line) + '</p>'; }).join('');
      var more = s.official ? '<p class="sat-more-row"><a class="sat-more" href="' + esc(s.official) + '" target="_blank" rel="noopener">' + esc(ui.more || 'Click here for more information') + '</a></p>' : '';
      card.innerHTML = '<button type="button" class="sat-close" aria-label="' + esc(ui.close || 'Close') + '">×</button>' +
        '<h3 id="sat-card-title" class="sat-title">' + esc(shortName(s)) + '</h3>' +
        '<p class="sat-kind">' + esc(kindWord(s)) + '</p>' + photo + brief + more;
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
      if (next !== mode) zoomT = 0;
      mode = next;
      layout(mode);
    }
    function setCat(next) {
      cat = next === 'lagrange' ? 'beyond' : next;
      if (cat === 'all') clearOrbit();
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
    stage.parentNode.insertBefore(zbar, stage);
    zin.addEventListener('click', function () { zoomT = Math.min(1, zoomT + 0.22); applyView(); });
    zout.addEventListener('click', function () { zoomT = Math.max(0, zoomT - 0.22); applyView(); });
    zfit.addEventListener('click', function () { zoomT = 0; applyView(); });
    var orbits = document.createElement('div');
    orbits.className = 'sat-orbits';
    orbits.setAttribute('role', 'group');
    orbits.setAttribute('aria-label', 'LEO MEO GEO');
    ['leo', 'meo', 'geo', 'heo', 'sso'].forEach(function (id, i, all) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'band-btn is-' + id;
      b.textContent = id.toUpperCase();
      b.setAttribute('data-band', id);
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () {
        if (id === 'leo' || id === 'meo' || id === 'geo') toggleOrbit(id);
        else {
          if (selectedBand === id) { selectedBand = ''; bandBox.hidden = true; paintBand(''); syncOrbit(); }
          else { selectedBand = id; showBandInfo(id); paintBand(id); syncOrbit(); }
        }
      });
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
