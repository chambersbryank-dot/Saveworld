/* Live voyages. Ranges come only from data/voyages.json (NASA/JPL Horizons). */
(function () {
  var root = document.getElementById('voy-app');
  if (!root) return;
  var I = {};
  try { I = JSON.parse(document.getElementById('voy-i18n').textContent); } catch (e) { return; }
  var pre = root.getAttribute('data-pre') || '';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var switcher = document.getElementById('voy-switch');
  var scene = document.getElementById('voy-scene');
  var live = I.live || [];
  var data = { missions: {} };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function globe(canvas, url) {
    if (!canvas) return;
    var img = new Image();
    var lon = 0.4, pixels = null, running = false;
    img.onload = function () {
      var c = document.createElement('canvas');
      c.width = img.naturalWidth; c.height = img.naturalHeight;
      var g = c.getContext('2d');
      g.drawImage(img, 0, 0);
      pixels = g.getImageData(0, 0, c.width, c.height).data;
      draw();
      if (!reduce) loop();
    };
    img.src = url;
    function sample(u, v) {
      var x = Math.max(0, Math.min(img.naturalWidth - 1, Math.floor(u * img.naturalWidth)));
      var y = Math.max(0, Math.min(img.naturalHeight - 1, Math.floor(v * img.naturalHeight)));
      var i = (y * img.naturalWidth + x) * 4;
      return [pixels[i], pixels[i + 1], pixels[i + 2]];
    }
    function draw() {
      if (!pixels) return;
      var ctx = canvas.getContext('2d');
      var w = canvas.width, h = canvas.height, r = Math.min(w, h) / 2 - 2, cx = w / 2, cy = h / 2;
      var out = ctx.createImageData(w, h), d = out.data, step = w > 300 ? 2 : 3;
      for (var y = 0; y < h; y += step) {
        var dy = (cy - (y + step / 2)) / r;
        if (dy < -1 || dy > 1) continue;
        var lat = Math.asin(Math.max(-1, Math.min(1, dy))), v = 0.5 - lat / Math.PI;
        for (var x = 0; x < w; x += step) {
          var dx = ((x + step / 2) - cx) / r;
          var rr = dx * dx + dy * dy;
          if (rr > 1) continue;
          var edge = Math.sqrt(rr);
          var fade = edge > 0.96 ? Math.max(0, (1 - edge) / 0.04) : 1;
          var uu = (lon + Math.asin(Math.max(-1, Math.min(1, dx)))) / (Math.PI * 2);
          uu = uu - Math.floor(uu);
          var rgb = sample(uu, v);
          var shade = 0.45 + 0.55 * Math.sqrt(Math.max(0, 1 - rr));
          for (var yy = y; yy < y + step && yy < h; yy++) {
            for (var xx = x; xx < x + step && xx < w; xx++) {
              var p = (yy * w + xx) * 4;
              d[p] = rgb[0] * shade; d[p + 1] = rgb[1] * shade; d[p + 2] = rgb[2] * shade; d[p + 3] = 255 * fade;
            }
          }
        }
      }
      ctx.clearRect(0, 0, w, h);
      ctx.putImageData(out, 0, 0);
    }
    function loop() {
      if (running) return;
      running = true;
      (function frame() { lon += 0.006; draw(); if (!reduce) requestAnimationFrame(frame); })();
    }
  }
  function km(n) {
    if (n == null) return '';
    var m = n / 1e6;
    var digits = m >= 100 ? 1 : 2;
    var f = Math.pow(10, digits);
    return (Math.round(m * f) / f).toLocaleString(I.locale || 'en') + ' ' + (I.millionKm || 'million km');
  }
  function show(id) {
    var m = null;
    live.forEach(function (x) { if (x.id === id) m = x; });
    if (!m) m = live[0];
    [].forEach.call(switcher.querySelectorAll('button'), function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-id') === m.id ? 'true' : 'false');
    });
    if (history.replaceState) history.replaceState(null, '', '#' + m.id);
    var row = (data.missions || {})[m.id] || {};
    var along = null;
    if (m.mode === 'cruise' && row.ok && row.earthKm && row.destKm) along = 100 * row.earthKm / (row.earthKm + row.destKm);
    else if (m.mode === 'there') along = 92;
    else if (m.mode === 'out') along = 84;
    var nums = '';
    if (row.ok && row.earthKm != null) {
      nums = '<p>' + esc(I.asOf) + ' ' + esc(String(row.asOf || '').slice(0, 10)) + ' (' + esc(I.sourceName) + '). ' +
        esc(I.fromEarth) + ' <b>' + esc(km(row.earthKm)) + '</b>';
      if (row.destKm != null && m.distLabel) nums += '. ' + esc(m.distLabel) + ' <b>' + esc(km(row.destKm)) + '</b>';
      nums += '.</p>';
    } else nums = '<p>' + esc(m.noRange || I.noRange) + '</p>';
    var far = '';
    if (m.globe) far = '<canvas id="voy-dest" width="420" height="420" aria-label="' + esc(m.destLabel) + '"></canvas>';
    else if (m.dest) far = '<img class="voy-cut" src="' + esc(pre + m.dest) + '" alt="' + esc(m.destAlt || m.destLabel) + '">';
    if (m.companion) far += '<img class="voy-moon" src="' + esc(pre + m.companion) + '" alt="' + esc(m.companionAlt || '') + '">';
    var craft = m.craft ? '<img src="' + esc(pre + m.craft) + '" alt="' + esc(m.craftAlt || m.name) + '">' : '';
    scene.innerHTML =
      '<h2 id="voy-h">' + esc(m.name) + '</h2>' +
      '<p class="voy-status">' + esc(m.status) + '</p>' +
      '<div class="voy-row">' +
        '<figure class="voy-earth"><canvas id="voy-earth" width="180" height="180" aria-label="' + esc(I.earth) + '"></canvas><figcaption>' + esc(I.earth) + '</figcaption></figure>' +
        '<div class="voy-track"><span class="voy-line"></span><figure class="voy-craft"' + (along == null ? '' : ' style="inset-inline-start:' + along.toFixed(2) + '%"') + '>' +
          craft + '<figcaption>' + esc(m.craftLabel || '') + '</figcaption></figure></div>' +
        '<figure class="voy-far">' + far + '<figcaption>' + esc(m.destLabel) + '</figcaption></figure>' +
      '</div>' + nums +
      '<p>' + esc(m.arrival) + '</p>' +
      (m.sentences || []).map(function (s) { return '<p>' + esc(s) + '</p>'; }).join('') +
      '<p class="sat-photo-credit">' + esc(m.credit) + '</p>' +
      '<p class="sat-more-row"><a class="sat-more" href="' + esc(m.official) + '" target="_blank" rel="noopener">' + esc(I.more) + '</a></p>';
    globe(document.getElementById('voy-earth'), pre + 'assets/earth/blue-marble-1920.jpg');
    if (m.globe) globe(document.getElementById('voy-dest'), pre + m.globe);
  }
  live.forEach(function (item) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'sat-more voy-tab';
    b.setAttribute('data-id', item.id);
    b.textContent = item.name;
    b.setAttribute('aria-pressed', 'false');
    b.addEventListener('click', function () { show(item.id); });
    switcher.appendChild(b);
  });
  fetch(root.getAttribute('data-src'), { credentials: 'omit' }).then(function (r) {
    return r.ok ? r.json() : { missions: {} };
  }).catch(function () { return { missions: {} }; }).then(function (j) {
    data = j || { missions: {} };
    var h = (location.hash || '').replace(/^#/, '');
    show(h || (live[0] && live[0].id));
  });
  window.addEventListener('hashchange', function () { show((location.hash || '').replace(/^#/, '')); });
})();
