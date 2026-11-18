/* Orthographic globe from NASA Blue Marble (equirectangular WebP already on the site).
   One image, decoded off the first screen. Large viewports use the 1920px source.
   Phones use 1280px so the lab stays light. The 4096px master is linked, not preloaded. */
(function () {
  if (window.SPGlobe) return;
  var pre = /\/(fr|es|ar|it|he)\//.test(location.pathname) ? '../' : '';
  var wide = window.matchMedia && window.matchMedia('(min-width: 1000px)').matches;
  var save = navigator.connection && navigator.connection.saveData;
  var src = pre + (wide && !save ? 'assets/earth/blue-marble-1920.webp' : 'assets/earth/blue-marble-800.webp');
  var img = new Image();
  img.decoding = 'async';
  if ('fetchPriority' in img) img.fetchPriority = 'low';
  img.onload = function () {
    var size = wide && !save ? 720 : 360;
    var c = document.createElement('canvas');
    c.width = c.height = size;
    var g = c.getContext('2d', { willReadFrequently: true });
    var sc = document.createElement('canvas');
    sc.width = img.width;
    sc.height = img.height;
    var sg = sc.getContext('2d', { willReadFrequently: true });
    sg.drawImage(img, 0, 0);
    var sp = sg.getImageData(0, 0, img.width, img.height).data;
    var w = img.width, h = img.height, r = size / 2;
    var out = g.createImageData(size, size);
    var d = out.data;
    function rows(y0) {
      var y1 = Math.min(size, y0 + 24);
      for (var y = y0; y < y1; y++) {
        var dy = (y + 0.5) - r;
        for (var x = 0; x < size; x++) {
          var dx = (x + 0.5) - r;
          var i = (y * size + x) * 4;
          var rr = Math.sqrt(dx * dx + dy * dy);
          if (rr > r) { d[i + 3] = 0; continue; }
          var z = Math.sqrt(r * r - rr * rr);
          var nx = dx / r, ny = dy / r, nz = z / r;
          var lat = Math.asin(-ny);
          var lon = Math.atan2(nx, nz);
          var u = (lon / (2 * Math.PI) + 0.5) * w;
          var v = (0.5 - lat / Math.PI) * h;
          var sx = Math.max(0, Math.min(w - 1, u | 0));
          var sy = Math.max(0, Math.min(h - 1, v | 0));
          var si = (sy * w + sx) * 4;
          var light = 0.62 + 0.38 * nz;
          d[i] = sp[si] * light;
          d[i + 1] = sp[si + 1] * light;
          d[i + 2] = sp[si + 2] * light;
          d[i + 3] = 255;
        }
      }
      if (y1 < size) setTimeout(function () { rows(y1); }, 0);
      else {
        g.putImageData(out, 0, 0);
        window.SPGlobe = c;
        window.dispatchEvent(new Event('sp-globe'));
      }
    }
    rows(0);
  };
  function kick() { img.src = src; }
  window.addEventListener('load', function () { setTimeout(kick, 50); });
})();
