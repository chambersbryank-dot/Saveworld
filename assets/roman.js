/* Nancy_Grace_Roman.html: daily distance + newest NASA image from assets/data/roman.json (built by scripts/build-roman.py), countdown. */
(function () {
  var pre = /\/(fr|es|ar|it|he)\//.test(location.pathname) ? '../' : '';
  var loc = document.documentElement.lang || 'en';
  function set(id, v) { var e = document.getElementById(id); if (e && v != null) e.textContent = v; }
  fetch(pre + 'assets/data/roman.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
    if (d.distance) {
      set('roman-km', d.distance.km.toLocaleString(loc)); set('roman-mi', d.distance.mi.toLocaleString(loc));
      var p = d.distance.date.split('-');
      set('roman-asof', new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])).toLocaleDateString(loc, { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }));
    }
    if (d.webb_km) set('webb-km', d.webb_km.toLocaleString(loc));
    if (d.image) {
      var img = document.getElementById('roman-latest-img');
      /* Oct 18: the page already carries the self-hosted newest image (build-roman.py); only swap if the JSON is newer than the page */
      if (img && d.image.thumb && img.getAttribute('data-id') !== (d.image.local_id || d.image.nasa_id)) { img.src = d.image.local_id ? pre + 'assets/roman-latest.jpg?v=' + d.image.local_id : d.image.thumb; img.parentNode.href = d.image.url; img.setAttribute('data-id', d.image.local_id || d.image.nasa_id); }
      set('roman-latest-title', d.image.title); set('roman-latest-date', d.image.date); set('roman-latest-credit', d.image.credit);
    }
  }).catch(function () {});
  var cd = document.getElementById('roman-cd');
  if (cd) {
    var days = Math.ceil((Date.parse(cd.getAttribute('data-target')) - Date.now()) / 864e5);
    if (days > 0) cd.textContent = days.toLocaleString(loc) + ' ' + (cd.getAttribute('data-days') || 'days');
  }
})();
