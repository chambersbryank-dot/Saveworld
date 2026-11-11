(function (root) {
  function helpOk(s, helps) {
    var m = helps.filter(function (h) { return h !== 'email'; });
    if (!m.length) return true;
    if (m.indexOf('learn') !== -1) return true;
    if (m.indexOf('money') !== -1 && s.give) return true;
    if (m.indexOf('time') !== -1 && s.time) return true;
    return false;
  }
  function score(s, helps) {
    var n = 0;
    if (helps.indexOf('money') !== -1 && s.give) n += 3;
    if (helps.indexOf('time') !== -1 && s.time) n += 3;
    if (helps.indexOf('learn') !== -1) n += 1;
    return n;
  }
  function rank(all, causes, helps, lang) {
    var list = all.filter(function (s) {
      return causes.indexOf(s.theme) !== -1 && helpOk(s, helps);
    });
    var bands = {};
    list.forEach(function (s) {
      var n = score(s, helps);
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
    return { list: ordered.slice(0, 10), matched: ordered.length };
  }
  root.SP9rank = rank;
  if (!root.document) return;

  var form = document.getElementById('match-form');
  if (!form) return;
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var pre = location.pathname.indexOf('/' + lang + '/') > -1 ? '../' : '';
  var T = root.SP9MATCH || {};
  var last = [];

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
  var URL_MAX = 1900;
  function buildBody(list) {
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
    return lines.join('\n');
  }
  function composeUrls(subject, body) {
    var su = encodeURIComponent(subject);
    var bo = encodeURIComponent(body);
    return {
      gmail: 'https://mail.google.com/mail/?view=cm&fs=1&su=' + su + '&body=' + bo,
      outlook: 'https://outlook.live.com/mail/0/deeplink/compose?subject=' + su + '&body=' + bo,
      mailto: 'mailto:?subject=' + su + '&body=' + bo
    };
  }
  function mailPack(list) {
    var subject = T.subject || 'A Saving Planets page to look at together';
    var full = (list || []).slice();
    var use = full.slice();
    var body = buildBody(use);
    var urls = composeUrls(subject, body);
    while (use.length && (urls.gmail.length > URL_MAX || urls.outlook.length > URL_MAX || urls.mailto.length > URL_MAX)) {
      use.pop();
      body = buildBody(use);
      urls = composeUrls(subject, body);
    }
    var fullBody = buildBody(full);
    return { subject: subject, body: fullBody, urls: urls, text: subject + '\n\n' + fullBody };
  }
  function emailOn() {
    return !!form.querySelector('input[name="help"][value="email"]:checked');
  }
  function applyMail(pack) {
    var g = document.getElementById('match-gmail');
    var o = document.getElementById('match-outlook');
    var a = document.getElementById('match-mailto');
    if (g) g.href = pack.urls.gmail;
    if (o) o.href = pack.urls.outlook;
    if (a) a.href = pack.urls.mailto;
  }
  function syncMail() {
    var on = emailOn();
    var box = document.getElementById('match-mail');
    var toggle = document.getElementById('help-email');
    if (box) box.hidden = !on;
    if (toggle) toggle.setAttribute('aria-expanded', on ? 'true' : 'false');
    applyMail(mailPack(on ? last : []));
    if (!on) {
      var status = document.getElementById('match-copied');
      var ta = document.getElementById('match-mail-text');
      var copyBtn = document.getElementById('match-copy');
      if (copiedTimer) { clearTimeout(copiedTimer); copiedTimer = 0; }
      if (status) status.hidden = true;
      if (ta) ta.hidden = true;
      if (copyBtn && copyBtn.getAttribute('data-label')) copyBtn.textContent = copyBtn.getAttribute('data-label');
    }
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
  form.addEventListener('reset', function () {
    setTimeout(function () {
      last = [];
      var out = document.getElementById('match-out');
      var note = document.getElementById('match-note');
      var grid = document.getElementById('match-list');
      var causes = form.querySelectorAll('input[name="cause"]');
      var helps = form.querySelectorAll('input[name="help"]');
      [].forEach.call(causes, function (el) { el.setCustomValidity(''); });
      [].forEach.call(helps, function (el) { el.setCustomValidity(''); });
      if (grid) grid.textContent = '';
      if (note) note.textContent = '';
      if (out) out.hidden = true;
      syncMail();
    }, 0);
  });

  var copyBtn = document.getElementById('match-copy');
  var copiedNode = document.getElementById('match-copied');
  var copiedLabel = copiedNode ? copiedNode.textContent : 'Copied';
  if (copyBtn) copyBtn.setAttribute('data-label', copyBtn.textContent);
  var copiedTimer = 0;
  function showCopied(ok) {
    if (copiedNode) copiedNode.hidden = !ok;
    if (!copyBtn) return;
    var label = copyBtn.getAttribute('data-label') || '';
    if (copiedTimer) clearTimeout(copiedTimer);
    copyBtn.textContent = ok ? copiedLabel : label;
    if (ok) copiedTimer = setTimeout(function () { copyBtn.textContent = label; }, 4000);
  }
  function copyMail(text) {
    var ta = document.getElementById('match-mail-text');
    function legacy() {
      if (ta) {
        ta.hidden = false;
        ta.value = text;
        ta.focus();
        ta.select();
      }
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
      showCopied(!!ok);
      if (ok && ta) ta.hidden = true;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        if (ta) ta.hidden = true;
        showCopied(true);
      }, legacy);
    } else legacy();
  }
  function shareMail(pack) {
    if (typeof navigator.share !== 'function') return;
    navigator.share({ title: pack.subject, text: pack.text, url: absUrl('Match.html') }).catch(function () {});
  }
  var shareBtn = document.getElementById('match-share');
  if (shareBtn && typeof navigator.share === 'function') shareBtn.hidden = false;
  var mailBox = document.getElementById('match-mail');
  if (mailBox) {
    mailBox.addEventListener('click', function (e) {
      var el = e.target && e.target.closest ? e.target.closest('a, button') : null;
      if (!el || !mailBox.contains(el)) return;
      var pack = mailPack(emailOn() ? last : []);
      applyMail(pack);
      if (el.id === 'match-copy') {
        e.preventDefault();
        copyMail(pack.text);
      } else if (el.id === 'match-share') {
        e.preventDefault();
        shareMail(pack);
      }
    });
  }
  syncMail();

  function safePage(url) {
    return typeof url === 'string' && /^[A-Za-z0-9_./-]+\.html$/.test(url) ? url : '';
  }
  function safeImage(url) {
    return typeof url === 'string' && /^(\.\.\/)?assets\/[A-Za-z0-9_./-]+$/.test(url) ? url : '';
  }
  function decodeAttr(s) {
    return String(s).replace(/&(?:amp|quot|lt|gt|#x27|#39);/g, function (ent) {
      if (ent === '&quot;') return '"';
      if (ent === '&lt;') return '<';
      if (ent === '&gt;') return '>';
      if (ent === '&amp;') return '&';
      return "'";
    });
  }
  function addCredit(parent, html) {
    var re = /<(\/?)(span|bdi|a)\b([^>]*)>|([^<]+)/g;
    var stack = [parent];
    var m;
    while ((m = re.exec(html))) {
      if (m[4] != null) {
        stack[stack.length - 1].appendChild(document.createTextNode(decodeAttr(m[4])));
        continue;
      }
      var tag = m[2];
      if (m[1] === '/') {
        if (stack.length > 1 && stack[stack.length - 1].tagName.toLowerCase() === tag) stack.pop();
        continue;
      }
      var el = document.createElement(tag);
      if (tag === 'a') {
        var href = /href="([^"]*)"/.exec(m[3] || '');
        var url = href ? decodeAttr(href[1]) : '';
        if (url.indexOf('https://') !== 0) continue;
        el.setAttribute('href', url);
        el.rel = 'noopener';
        if ((m[3] || '').indexOf('target="_blank"') !== -1) el.target = '_blank';
      }
      stack[stack.length - 1].appendChild(el);
      stack.push(el);
    }
  }
  function card(s, i, cards) {
    var info = cards[s.url] || {};
    var page = safePage(s.url);
    var image = safeImage(info.src);
    var art = document.createElement('article');
    art.className = 'card sol-card tt-card' + (image ? '' : ' no-photo');
    var num = document.createElement('span');
    num.className = 'tt-num';
    num.setAttribute('aria-hidden', 'true');
    num.textContent = String(i + 1);
    if (image) {
      var wrap = document.createElement('div');
      wrap.className = 'image-container';
      var link = document.createElement('a');
      link.className = 'photo-link';
      link.href = page || '#';
      var img = document.createElement('img');
      img.src = image;
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
      addCredit(credit, info.credit);
      art.appendChild(credit);
    }
    var h = document.createElement('h3');
    var a = document.createElement('a');
    a.href = page || '#';
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
    var causes = vals('cause'), helps = vals('help');
    var ranked = rank(model.all, causes, helps, lang);
    last = ranked.list;
    var out = document.getElementById('match-out');
    var note = document.getElementById('match-note');
    var h2 = document.getElementById('match-out-h');
    var grid = document.getElementById('match-list');
    var n = ranked.list.length;
    var msg;
    if (!n) msg = T.none;
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
