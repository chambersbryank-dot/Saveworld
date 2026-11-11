/* Space Map draft. Lazy-loads three.js and satellite.js. Orbit data: assets/data/space-map.json
   (cached CelesTrak TLEs, plus approximate placements where no Earth TLE exists).
   Add a satellite in scripts/build-space-map.py, then rerun that script. */
(function () {
  var root = document.getElementById('sm-app');
  if (!root) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var RE = 6371;
  var VIS = { l1: 8.15, l2: 8.7, l5: 9.25 };
  var byId = {};
  var dlg = document.getElementById('sm-dialog');
  var statusEl = document.getElementById('sm-status');
  var lastFocus = null;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function say(t) { if (statusEl) statusEl.textContent = t; }
  function cardHtml(s) {
    return '<div class="card-band sm-cardwrap"><button type="button" class="sm-close" data-sm-close>Close</button>' +
      '<article class="card sol-card">' +
      '<div class="image-container"><a class="photo-link" href="' + esc(s.page) + '"><img alt="' + esc(s.alt) + '" width="640" height="400" src="' + esc(s.img) + '"></a></div>' +
      '<p class="photo-credit sol-credit">' + s.creditHtml + '</p>' +
      '<h3><a href="' + esc(s.page) + '">' + esc(s.pageName) + '</a></h3>' +
      '<p class="sol-desc"><span>' + esc(s.desc) + '</span></p>' +
      '<p class="sm-orbit">' + esc(s.source) + '</p>' +
      (s.globeHtml ? '<p class="sm-globe">' + s.globeHtml + '</p>' : '') +
      '<p class="sm-more"><a href="' + esc(s.page) + '">Read the solution page</a></p>' +
      '</article></div>';
  }
  function openCard(s, opener) {
    if (!dlg || !s) return;
    lastFocus = opener || document.activeElement;
    dlg.innerHTML = cardHtml(s);
    if (typeof dlg.showModal === 'function' && !dlg.open) dlg.showModal();
    else { dlg.hidden = false; dlg.setAttribute('open', ''); }
    var c = dlg.querySelector('.sm-close');
    if (c) c.focus();
  }
  if (dlg) {
    dlg.addEventListener('click', function (e) {
      if (e.target === dlg || e.target.closest('[data-sm-close]')) {
        if (dlg.open && dlg.close) dlg.close();
        else dlg.hidden = true;
      }
    });
    dlg.addEventListener('close', function () { if (lastFocus && lastFocus.focus) lastFocus.focus(); });
  }

  var dataP = fetch(root.getAttribute('data-src')).then(function (r) {
    if (!r.ok) throw 0;
    return r.json();
  }).then(function (data) {
    (data.sats || []).forEach(function (s) { byId[s.id] = s; });
    return data;
  });
  dataP.catch(function () { say('Satellite data could not load. The table below still lists every satellite.'); });

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-sm-open]');
    if (!b) return;
    e.preventDefault();
    dataP.then(function () { openCard(byId[b.getAttribute('data-sm-open')], b); });
  });

  var on = { leo: true, sso: true, meo: true, geo: true, beyond: true };
  document.querySelectorAll('.sm-legend button[data-regime]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var k = btn.getAttribute('data-regime');
      on[k] = !on[k];
      btn.setAttribute('aria-pressed', on[k] ? 'true' : 'false');
      btn.classList.toggle('is-on', on[k]);
    });
  });

  if (reduce) {
    say('Animation is off. The table below has the same satellites.');
    return;
  }

  var view = document.getElementById('sm-view');
  var canvas = document.getElementById('sm-canvas');
  var layer = document.getElementById('sm-markers');
  if (!view || !canvas || !window.WebGLRenderingContext) {
    say('This browser cannot draw the 3D Earth. The table below has every satellite.');
    return;
  }

  function loadScript(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.onload = function () { res(); };
      s.onerror = function () { rej(new Error(src)); };
      document.head.appendChild(s);
    });
  }

  dataP.then(function (data) {
    var base = root.getAttribute('data-lib') || 'assets/space-map/vendor/';
    return Promise.all([
      loadScript(base + 'satellite.min.js?v=4.1.4'),
      loadScript(base + 'three.min.js?v=0.160.1')
    ]).then(function () { boot(data); });
  }).catch(function () {
    say('The 3D view could not load. The table below has every satellite.');
  });

  function regimeKey(s) {
    return (s.regime === 'l1' || s.regime === 'l2' || s.regime === 'l5') ? 'beyond' : s.regime;
  }
  function shown(s) { return !!on[regimeKey(s)]; }

  function boot(data) {
    var THREE = window.THREE;
    var sat = window.satellite;
    if (!THREE || !sat) { say('The 3D view could not load. The table below has every satellite.'); return; }
    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false, powerPreference: 'low-power' });
    } catch (e) {
      say('This browser cannot draw the 3D Earth. The table below has every satellite.');
      return;
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
    var scene = new THREE.Scene();
    scene.background = new THREE.Color('#02060c');
    var camera = new THREE.PerspectiveCamera(35, 1, 0.05, 200);
    var dist = 15, rotX = 0.35, rotY = 0.8;
    function applyCam() {
      var cx = Math.cos(rotX);
      camera.position.set(dist * cx * Math.sin(rotY), dist * Math.sin(rotX), dist * cx * Math.cos(rotY));
      camera.lookAt(0, 0, 0);
    }
    applyCam();

    var stars = new Float32Array(600);
    for (var i = 0; i < 200; i++) {
      var r = 50 + Math.random() * 30;
      var th = Math.random() * Math.PI * 2;
      var ph = Math.acos(2 * Math.random() - 1);
      stars[i * 3] = r * Math.sin(ph) * Math.cos(th);
      stars[i * 3 + 1] = r * Math.cos(ph);
      stars[i * 3 + 2] = r * Math.sin(ph) * Math.sin(th);
    }
    var sg = new THREE.BufferGeometry();
    sg.setAttribute('position', new THREE.BufferAttribute(stars, 3));
    scene.add(new THREE.Points(sg, new THREE.PointsMaterial({ color: 0xffffff, size: 0.12, sizeAttenuation: true })));

    var earthGeo = new THREE.SphereGeometry(1, 64, 48);
    var earthMat = new THREE.MeshBasicMaterial({ color: 0x1a4c7c });
    var earth = new THREE.Mesh(earthGeo, earthMat);
    scene.add(earth);
    new THREE.TextureLoader().load(data.earth.src, function (tex) {
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.anisotropy = Math.min(4, renderer.capabilities.getMaxAnisotropy());
      earthMat.map = tex;
      earthMat.color.set(0xffffff);
      earthMat.needsUpdate = true;
    });

    var lineMat = {};
    function mat(color) {
      if (!lineMat[color]) lineMat[color] = new THREE.LineBasicMaterial({ color: color, transparent: true, opacity: 0.45 });
      return lineMat[color];
    }
    var bodies = [];
    (data.sats || []).forEach(function (s) {
      var el = document.createElement('button');
      el.type = 'button';
      el.className = 'sm-pin';
      el.style.setProperty('--c', s.color);
      el.setAttribute('data-sm-open', s.id);
      el.setAttribute('aria-label', s.label + ', ' + s.regimeName + (s.approx ? ', approximate orbit' : '') + '. Open the solution card.');
      el.innerHTML = '<img alt="" width="46" height="46" src="' + esc(s.thumb) + '">' +
        (s.approx ? '<span class="sm-approx" aria-hidden="true">≈</span>' : '') +
        '<span class="sm-tip">' + esc(s.label) + '</span>';
      layer.appendChild(el);
      var rec = null;
      if (s.tle && s.tle.length === 2) {
        try { rec = sat.twoline2satrec(s.tle[0], s.tle[1]); } catch (e) { rec = null; }
      }
      var line = new THREE.LineLoop(new THREE.BufferGeometry(), mat(s.color));
      scene.add(line);
      bodies.push({ s: s, el: el, rec: rec, line: line, pos: new THREE.Vector3() });
    });

    function sunThree(date) {
      var n = (Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()) - Date.UTC(date.getUTCFullYear(), 0, 0)) / 86400000;
      var L = (280.46 + 0.9856474 * n) % 360;
      var g = (357.528 + 0.9856003 * n) * Math.PI / 180;
      var lam = (L + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * Math.PI / 180;
      var eps = 23.439 * Math.PI / 180;
      var x = Math.cos(lam), y = Math.cos(eps) * Math.sin(lam), z = Math.sin(eps) * Math.sin(lam);
      var gmst = sat.gstime(date);
      var xe = x * Math.cos(gmst) + y * Math.sin(gmst);
      var ye = -x * Math.sin(gmst) + y * Math.cos(gmst);
      return new THREE.Vector3(xe, z, -ye).normalize();
    }
    function approxAt(s, date) {
      var a = s.fallback || {};
      if (a.kind === 'l1' || a.kind === 'l2' || a.kind === 'l5') {
        var sun = sunThree(date);
        var v = sun.clone();
        if (a.kind === 'l2') v.negate();
        if (a.kind === 'l5') v.applyAxisAngle(new THREE.Vector3(0, 1, 0), -Math.PI / 3);
        return v.multiplyScalar(VIS[a.kind] || 8.2);
      }
      var period = (a.periodMin || 100) * 60;
      var th = (a.phase || 0) + ((date.getTime() / 1000) % period) / period * Math.PI * 2;
      if (s.regime === 'geo' && a.fixed) th = (a.lon || 0) * Math.PI / 180;
      var inc = (a.inc || 0) * Math.PI / 180;
      var raan = (a.raan || 0) * Math.PI / 180;
      var r = (RE + (a.altKm || 700)) / RE;
      var x = r * Math.cos(th), y = r * Math.sin(th);
      var y1 = y * Math.cos(inc), z1 = y * Math.sin(inc);
      var x2 = x * Math.cos(raan) - y1 * Math.sin(raan);
      var y2 = x * Math.sin(raan) + y1 * Math.cos(raan);
      if (s.regime === 'geo' && a.fixed) {
        var lon = (a.lon || 0) * Math.PI / 180;
        return new THREE.Vector3(r * Math.cos(lon), 0, -r * Math.sin(lon));
      }
      return new THREE.Vector3(x2, z1, -y2);
    }
    function fromRec(rec, date) {
      var pv = sat.propagate(rec, date);
      if (!pv || !pv.position || !isFinite(pv.position.x)) return null;
      var ecf = sat.eciToEcf(pv.position, sat.gstime(date));
      if (!ecf || !isFinite(ecf.x)) return null;
      var v = new THREE.Vector3(ecf.x / RE, ecf.z / RE, -ecf.y / RE);
      var len = v.length();
      if (len < 0.95 || len > 12) return null;
      return v;
    }
    function placeOne(b, date) {
      var v = b.rec ? fromRec(b.rec, date) : null;
      if (!v) v = approxAt(b.s, date);
      b.pos.copy(v);
    }
    function drawOrbits(date) {
      bodies.forEach(function (b) {
        var pts = [];
        var a = b.s.fallback || {};
        var steps = 72;
        if (b.s.regime === 'geo' || a.kind === 'l1' || a.kind === 'l2' || a.kind === 'l5') {
          if (a.kind) {
            pts = [new THREE.Vector3(0, 0, 0), b.pos.clone()];
            b.line.geometry.dispose();
            b.line.geometry = new THREE.BufferGeometry().setFromPoints(pts);
            b.line.visible = shown(b.s);
            return;
          }
          var r = b.pos.length();
          for (var k = 0; k < steps; k++) {
            var lon = k / steps * Math.PI * 2;
            pts.push(new THREE.Vector3(r * Math.cos(lon), 0, -r * Math.sin(lon)));
          }
        } else if (b.rec) {
          var no = b.rec.no || (Math.PI * 2 / 90);
          var stepMin = (Math.PI * 2 / no) / steps;
          for (var j = 0; j < steps; j++) {
            var d = new Date(date.getTime() + j * stepMin * 60000);
            var p = fromRec(b.rec, d);
            if (p) pts.push(p);
          }
        } else {
          var period = ((a.periodMin || 100) * 60000);
          for (var n = 0; n < steps; n++) {
            pts.push(approxAt(b.s, new Date(date.getTime() + n / steps * period)));
          }
        }
        b.line.geometry.dispose();
        b.line.geometry = new THREE.BufferGeometry().setFromPoints(pts);
        b.line.visible = shown(b.s);
      });
    }

    var now = new Date();
    bodies.forEach(function (b) { placeOne(b, now); });
    drawOrbits(now);
    var orbitAt = now.getTime();

    function occluded(p) {
      var cam = camera.position;
      var d = p.clone().sub(cam);
      var a = d.lengthSq();
      var b2 = 2 * cam.dot(d);
      var c = cam.lengthSq() - 1.04;
      var disc = b2 * b2 - 4 * a * c;
      if (disc < 0) return false;
      var t = (-b2 - Math.sqrt(disc)) / (2 * a);
      return t > 0.001 && t < 0.999;
    }
    function layout() {
      var w = view.clientWidth, h = view.clientHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      var date = new Date();
      if (date.getTime() - orbitAt > 60000) { drawOrbits(date); orbitAt = date.getTime(); }
      bodies.forEach(function (b) {
        placeOne(b, date);
        var vis = shown(b.s);
        b.line.visible = vis;
        if (!vis) { b.el.hidden = true; return; }
        var p = b.pos.clone().project(camera);
        var hide = p.z > 1 || occluded(b.pos);
        b.el.hidden = hide;
        if (hide) return;
        var x = (p.x * 0.5 + 0.5) * w + (b.s.nudge || 0);
        var y = (-p.y * 0.5 + 0.5) * h;
        b.el.style.transform = 'translate(' + x + 'px,' + y + 'px) translate(-50%,-50%)';
      });
    }

    var dragging = null;
    canvas.addEventListener('pointerdown', function (e) {
      dragging = { x: e.clientX, y: e.clientY, rx: rotX, ry: rotY, id: e.pointerId };
      canvas.setPointerCapture(e.pointerId);
    });
    canvas.addEventListener('pointermove', function (e) {
      if (!dragging || e.pointerId !== dragging.id) return;
      rotY = dragging.ry - (e.clientX - dragging.x) * 0.005;
      rotX = Math.max(-1.2, Math.min(1.2, dragging.rx + (e.clientY - dragging.y) * 0.005));
      applyCam();
    });
    function endDrag(e) { if (dragging && e.pointerId === dragging.id) dragging = null; }
    canvas.addEventListener('pointerup', endDrag);
    canvas.addEventListener('pointercancel', endDrag);
    canvas.addEventListener('wheel', function (e) {
      e.preventDefault();
      dist = Math.max(2.4, Math.min(26, dist * (e.deltaY > 0 ? 1.08 : 0.92)));
      applyCam();
    }, { passive: false });
    document.getElementById('sm-zin').addEventListener('click', function () { dist = Math.max(2.4, dist * 0.85); applyCam(); });
    document.getElementById('sm-zout').addEventListener('click', function () { dist = Math.min(26, dist / 0.85); applyCam(); });
    document.getElementById('sm-reset').addEventListener('click', function () { dist = 15; rotX = 0.35; rotY = 0.8; applyCam(); });

    var running = true;
    document.addEventListener('visibilitychange', function () { running = !document.hidden; });
    function frame() {
      requestAnimationFrame(frame);
      if (!running) return;
      layout();
      renderer.render(scene, camera);
    }
    frame();
    say('Drag to turn Earth. Orbits are moving.');
    refreshTles(bodies);
  }

  function refreshTles(bodies) {
    var queue = bodies.filter(function (b) { return b.s.norad && b.s.tle; });
    var i = 0, fails = 0, updated = 0;
    function next() {
      if (i >= queue.length || fails > 2) {
        if (updated) say('Orbits updated from CelesTrak for ' + updated + ' satellite' + (updated === 1 ? '' : 's') + '. The rest use the saved copy.');
        else say('Using saved CelesTrak orbits. A live refresh did not answer.');
        return;
      }
      var b = queue[i++];
      fetch('https://celestrak.org/NORAD/elements/gp.php?CATNR=' + b.s.norad + '&FORMAT=tle')
        .then(function (r) { if (!r.ok) throw 0; return r.text(); })
        .then(function (t) {
          var lines = t.split(/\r?\n/).map(function (x) { return x.trim(); }).filter(Boolean);
          var l1 = null, l2 = null;
          for (var k = 0; k < lines.length; k++) {
            if (lines[k].charAt(0) === '1' && lines[k].length > 60) l1 = lines[k];
            if (lines[k].charAt(0) === '2' && lines[k].length > 60) l2 = lines[k];
          }
          if (!l1 || !l2 || parseInt(l1.slice(2, 7), 10) !== b.s.norad) throw 0;
          var rec = window.satellite.twoline2satrec(l1, l2);
          if (!rec) throw 0;
          b.rec = rec;
          b.s.tle = [l1, l2];
          updated++;
          fails = 0;
          setTimeout(next, 180);
        })
        .catch(function () { fails++; setTimeout(next, 180); });
    }
    next();
  }
})();
