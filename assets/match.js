(function (root) {
  function modes(helps) {
    var m = helps.filter(function (h) { return h !== 'email'; });
    return m.length ? m : ['learn'];
  }
  function placeExact(s, where, helps) {
    var near = !!(s.local || s.where === 'local');
    if (where === 'near') return near;
    return modes(helps).some(function (h) {
      if (h === 'money' || h === 'learn') return true;
      if (s.where === 'remote') return true;
      if (s.where === 'local') return false;
      return !!s.remote;
    });
  }
  function helpOk(s, helps) {
    var m = helps.filter(function (h) { return h !== 'email'; });
    if (!m.length) return true;
    if (m.indexOf('learn') !== -1) return true;
    if (m.indexOf('money') !== -1 && s.give) return true;
    if (m.indexOf('time') !== -1 && s.time) return true;
    return false;
  }
  function score(s, where, helps) {
    var n = placeExact(s, where, helps) ? 4 : 0;
    if (helps.indexOf('money') !== -1 && s.give) n += 3;
    if (helps.indexOf('time') !== -1 && s.time) n += 3;
    if (helps.indexOf('learn') !== -1) n += 1;
    return n;
  }
  function rank(all, causes, helps, where, lang) {
    var pool = all.filter(function (s) {
      return causes.indexOf(s.theme) !== -1 && helpOk(s, helps);
    });
    var exact = pool.filter(function (s) { return placeExact(s, where, helps); });
    var relaxed = exact.length < 10 && pool.length > exact.length;
    var list = exact.length >= 10 ? exact : pool;
    var bands = {};
    list.forEach(function (s) {
      var n = score(s, where, helps);
      (bands[n] = bands[n] || []).push(s);
    });
    var levels = Object.keys(bands).map(Number).sort(function (a, b) { return b - a; });
    var ordered = [];
    levels.forEach(function (n) {
      var by = {};
      bands[n].forEach(function (s) { (by[s.theme] = by[s.theme] || []).push(s); });
      Object.keys(by).forEach(function (theme) {
        by[theme].sort(function (a, b) {
          return String(a.title).localeCompare(String(b.title), lang || undefined);
        });
      });
      var order = causes.filter(function (c) { return by[c] && by[c].length; });
      while (order.length) {
        var next = [];
        order.forEach(function (c) {
          ordered.push(by[c].shift());
          if (by[c].length) next.push(c);
        });
        order = next;
      }
    });
    return { list: ordered.slice(0, 10), matched: ordered.length, relaxed: relaxed };
  }
  root.SP9rank = rank;
  if (!root.document) return;

  var form = document.getElementById('match-form');
  if (!form) return;
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var pre = location.pathname.indexOf('/' + lang + '/') > -1 ? '../' : '';
  var T = root.SP9MATCH || {};
  var last = [];

  var video = document.querySelector('.match-video');
  if (video) {
    var reduce = root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)');
    var saveData = navigator.connection && navigator.connection.saveData;
    var pauseBtn = document.querySelector('.match-pause');
    var held = false;
    function arm() {
      if ((reduce && reduce.matches) || saveData) {
        video.pause();
        video.removeAttribute('autoplay');
        video.preload = 'none';
        return;
      }
      var src = video.querySelector('source[data-src]');
      if (src && !src.getAttribute('src')) {
        src.src = src.getAttribute('data-src');
        video.load();
      }
      if (!held) {
        var p = video.play && video.play();
        if (p && p.catch) p.catch(function () {});
      }
    }
    arm();
    if (reduce && reduce.addEventListener) reduce.addEventListener('change', arm);
    if (pauseBtn) {
      pauseBtn.addEventListener('click', function () {
        held = pauseBtn.getAttribute('aria-pressed') !== 'true';
        pauseBtn.setAttribute('aria-pressed', held ? 'true' : 'false');
        pauseBtn.setAttribute('aria-label', held ? (pauseBtn.getAttribute('data-play') || 'Play') : (pauseBtn.getAttribute('data-pause') || 'Pause'));
        if (held) video.pause();
        else arm();
      });
    }
  }

  function vals(name) {
    return [].filter.call(form.querySelectorAll('input[name="' + name + '"]'), function (el) { return el.checked; })
      .map(function (el) { return el.value; });
  }
  function fill(s, n) { return String(s || '').replace(/\{n\}/g, String(n)); }
  function absUrl(url) {
    if (/^https?:/.test(url)) return url;
    var origin = 'https://www.savingplanets.com';
    var dir = location.pathname.replace(/[^/]*$/, '');
    return origin + dir + url;
  }
  function mailHref(list) {
    var lines = [];
    lines.push(T.intro_mail || 'I was on Saving Planets and thought of you.');
    lines.push('');
    lines.push((T.match_link || 'Match page') + ': ' + absUrl('Match.html'));
    lines.push((T.home_link || 'Saving Planets') + ': https://www.savingplanets.com/');
    if (list && list.length) {
      lines.push('');
      lines.push(T.matched || 'These solutions matched:');
      list.forEach(function (s, i) {
        lines.push((i + 1) + '. ' + s.title + ' — ' + absUrl(s.url));
      });
    } else {
      lines.push('');
      lines.push(T.no_list || 'Open the Match page to see solutions already on the site.');
    }
    lines.push('');
    lines.push(T.privacy || 'Saving Planets does not ask for a name, a school, or a location, and it does not save these answers.');
    return 'mailto:?subject=' + encodeURIComponent(T.subject || 'A Saving Planets page to look at together') + '&body=' + encodeURIComponent(lines.join('\n'));
  }
  function syncMail() {
    var on = !!form.querySelector('input[name="help"][value="email"]:checked');
    var box = document.getElementById('match-mail');
    var a = document.getElementById('match-mailto');
    if (box) box.hidden = !on;
    if (a) a.href = mailHref(on ? last : []);
  }
  function syncValidity() {
    var causes = form.querySelectorAll('input[name="cause"]');
    var helps = form.querySelectorAll('input[name="help"]');
    var cOk = [].some.call(causes, function (el) { return el.checked; });
    var hOk = [].some.call(helps, function (el) { return el.checked; });
    if (causes[0]) causes[0].setCustomValidity(cOk ? '' : (T.need || 'Choose at least one cause and one way to help.'));
    if (helps[0]) helps[0].setCustomValidity(hOk ? '' : (T.need || 'Choose at least one cause and one way to help.'));
  }
  form.addEventListener('change', function () { syncValidity(); syncMail(); });

  function card(s, i, cards) {
    var info = cards[s.url] || {};
    var art = document.createElement('article');
    art.className = 'card sol-card tt-card' + (info.src ? '' : ' no-photo');
    var num = document.createElement('span');
    num.className = 'tt-num';
    num.setAttribute('aria-hidden', 'true');
    num.textContent = String(i + 1);
    if (info.src) {
      var wrap = document.createElement('div');
      wrap.className = 'image-container';
      var link = document.createElement('a');
      link.className = 'photo-link';
      link.href = s.url;
      var img = document.createElement('img');
      img.src = info.src;
      img.alt = info.alt || '';
      if (info.w) img.width = info.w;
      if (info.h) img.height = info.h;
      img.loading = 'lazy';
      img.decoding = 'async';
      link.appendChild(img);
      wrap.appendChild(num);
      wrap.appendChild(link);
      art.appendChild(wrap);
    } else {
      art.appendChild(num);
    }
    if (info.credit) {
      var credit = document.createElement('p');
      credit.className = 'photo-credit sol-credit';
      credit.innerHTML = info.credit;
      art.appendChild(credit);
    }
    var h = document.createElement('h3');
    var a = document.createElement('a');
    a.href = s.url;
    a.textContent = s.title;
    h.appendChild(a);
    art.appendChild(h);
    if (s.blurb) {
      var desc = document.createElement('p');
      desc.className = 'sol-desc';
      var span = document.createElement('span');
      span.textContent = s.blurb;
      desc.appendChild(span);
      art.appendChild(desc);
    }
    return art;
  }

  function getJSON(url) {
    return fetch(url).then(function (r) { if (!r.ok) throw new Error(url); return r.json(); });
  }
  var model = null;
  var queued = false;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!model) { queued = true; return; }
    show();
  });
  getJSON(pre + 'assets/data/match.' + lang + '.json').then(function (data) {
    getJSON(pre + 'assets/data/match-cards.' + lang + '.json').then(function (cards) {
      boot(data, cards || {});
    }, function () { boot(data, {}); });
  });

  function boot(data, cards) {
    model = { all: data.solutions || [], cards: cards || {} };
    syncMail();
    if (queued) show();
  }
  function show() {
    syncValidity();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var causes = vals('cause'), helps = vals('help'), where = (form.querySelector('input[name="where"]:checked') || {}).value;
    var ranked = rank(model.all, causes, helps, where, lang);
    last = ranked.list;
    var out = document.getElementById('match-out');
    var note = document.getElementById('match-note');
    var h2 = document.getElementById('match-out-h');
    var grid = document.getElementById('match-list');
    var n = ranked.list.length;
    var msg;
    if (!n) msg = T.none;
    else if (ranked.relaxed) msg = fill(T.relaxed, n);
    else if (n < 10) msg = fill(T.short, n);
    else msg = fill(T.exact, n);
    if (h2) h2.textContent = T.out || h2.textContent;
    if (note) note.textContent = msg || '';
    grid.textContent = '';
    ranked.list.forEach(function (s, i) { grid.appendChild(card(s, i, model.cards)); });
    out.hidden = false;
    syncMail();
    if (h2) { h2.tabIndex = -1; h2.focus(); }
  }
})(typeof window !== 'undefined' ? window : globalThis);
