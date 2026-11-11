/* Teachers catalog: chips, standards select, collapsed hubs, paged "browse all".
   Core sheet links live in <details>, so they work with JavaScript off. */
(function () {
  var root = document.getElementById('t-home');
  if (!root) return;
  var grid = document.getElementById('t-topic-grid');
  var more = document.getElementById('t-more-all');
  var live = document.getElementById('t-live');
  var none = root.querySelector('.t-none');
  var allBtn = document.getElementById('t-browse-all');
  var sel = document.getElementById('t-std');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var grade = 'all', subject = 'all', std = 'all', browseAll = false, shown = 24;
  var cssEsc = (window.CSS && CSS.escape) ? function (s) { return CSS.escape(s); } : function (s) { return String(s).replace(/"/g, '\\"'); };

  function hubs() { return [].slice.call(grid.querySelectorAll(':scope > details.t-topic')); }
  function cards() { return [].slice.call(grid.querySelectorAll('.t-card')); }
  function has(card, attr, value, sep) {
    if (value === 'all') return true;
    return (card.getAttribute(attr) || '').split(sep).indexOf(value) !== -1;
  }
  function matches(card) {
    return has(card, 'data-grades', grade, ' ') && has(card, 'data-subjects', subject, ' ') && has(card, 'data-codes', std, '|');
  }
  function filtering() { return browseAll || grade !== 'all' || subject !== 'all' || std !== 'all'; }
  function sync(d) {
    var s = d.querySelector(':scope > summary');
    if (s) s.setAttribute('aria-expanded', d.open ? 'true' : 'false');
  }
  root.querySelectorAll('details').forEach(function (d) {
    sync(d);
    d.addEventListener('toggle', function () { sync(d); });
  });
  /* Some browsers open <details> without a toggle event. Sync after the click. */
  root.addEventListener('click', function (e) {
    var summary = e.target.closest && e.target.closest('summary');
    if (!summary || !root.contains(summary)) return;
    var d = summary.parentElement;
    setTimeout(function () { if (d && d.tagName === 'DETAILS') sync(d); }, 0);
  });
  root.querySelectorAll('.t-years').forEach(function (box) {
    box.addEventListener('toggle', function (e) {
      var d = e.target;
      if (!d.open || d.parentElement !== box) return;
      [].forEach.call(box.children, function (other) { if (other !== d && other.open) other.open = false; });
    }, true);
  });

  function setPressed(k, v) {
    root.querySelectorAll('.t-chip[data-k="' + k + '"]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false');
    });
  }
  function known(k, v) {
    return !!root.querySelector('.t-chip[data-k="' + k + '"][data-v="' + cssEsc(v) + '"]');
  }
  function writeUrl() {
    try {
      var q = new URLSearchParams(location.search);
      grade === 'all' ? q.delete('grade') : q.set('grade', grade);
      subject === 'all' ? q.delete('subject') : q.set('subject', subject);
      std === 'all' ? q.delete('std') : q.set('std', std);
      browseAll ? q.set('all', '1') : q.delete('all');
      history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : '') + location.hash);
    } catch (e) {}
  }
  function resetOpen() {
    browseAll = false;
    if (allBtn) allBtn.setAttribute('aria-expanded', 'false');
    hubs().forEach(function (h) { h.open = false; sync(h); });
  }
  function paint() {
    var matched = cards().filter(matches);
    if (!filtering()) {
      cards().forEach(function (c) { c.hidden = false; });
      hubs().forEach(function (h) { h.hidden = false; });
      if (more) more.hidden = true;
      if (none) none.hidden = true;
      if (live) live.textContent = '';
      return;
    }
    var limit = shown;
    matched.forEach(function (c, i) { c.hidden = i >= limit; });
    cards().forEach(function (c) { if (matched.indexOf(c) === -1) c.hidden = true; });
    hubs().forEach(function (h) {
      var vis = !!h.querySelector('.t-card:not([hidden])');
      h.hidden = !vis;
      h.open = vis;
      sync(h);
    });
    if (more) {
      var left = Math.max(0, matched.length - limit);
      more.hidden = left === 0;
      if (!more.hidden) more.textContent = (more.getAttribute('data-more') || 'Show more').replace('{n}', String(Math.min(24, left)));
    }
    if (none) none.hidden = matched.length !== 0;
    if (live) {
      var full = live.getAttribute('data-tpl') || '{n}';
      var part = live.getAttribute('data-partial') || full;
      var tpl = matched.length > limit ? part : full;
      live.textContent = tpl.replace('{shown}', String(Math.min(limit, matched.length))).replace('{n}', String(matched.length));
    }
    if (allBtn) allBtn.setAttribute('aria-expanded', browseAll ? 'true' : 'false');
  }

  root.addEventListener('click', function (e) {
    var chip = e.target.closest && e.target.closest('.t-chip[data-k]');
    if (!chip || !root.contains(chip)) return;
    var k = chip.getAttribute('data-k'), v = chip.getAttribute('data-v');
    if (k === 'g') grade = v; else if (k === 's') subject = v;
    setPressed(k, v);
    shown = 24;
    if (grade === 'all' && subject === 'all' && std === 'all') resetOpen();
    paint();
    writeUrl();
  });
  if (sel) sel.addEventListener('change', function () {
    std = sel.value || 'all';
    shown = 24;
    if (grade === 'all' && subject === 'all' && std === 'all') resetOpen();
    paint();
    writeUrl();
  });
  if (allBtn) allBtn.addEventListener('click', function (e) {
    e.preventDefault();
    browseAll = allBtn.getAttribute('aria-expanded') !== 'true';
    shown = 24;
    if (!browseAll) hubs().forEach(function (h) { h.open = false; });
    paint();
    writeUrl();
    if (browseAll) grid.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  });
  if (more) more.addEventListener('click', function () { shown += 24; paint(); });

  function init() {
    var q;
    try { q = new URLSearchParams(location.search); } catch (e) { return; }
    if (q.get('grade') && known('g', q.get('grade'))) { grade = q.get('grade'); setPressed('g', grade); }
    if (q.get('subject') && known('s', q.get('subject'))) { subject = q.get('subject'); setPressed('s', subject); }
    if (q.get('std') && sel) {
      var want = q.get('std'), ok = false;
      [].forEach.call(sel.options, function (o) { if (o.value === want) ok = true; });
      if (ok) { std = want; sel.value = want; }
    }
    if (q.get('all') === '1') browseAll = true;
    if (filtering()) paint();
    var hub = q.get('hub');
    if (hub) {
      var d = grid.querySelector('details.t-topic[data-hub="' + cssEsc(hub) + '"]');
      if (d) {
        d.hidden = false;
        d.open = true;
        d.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      }
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
