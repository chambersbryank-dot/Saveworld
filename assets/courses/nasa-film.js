/* Hub film player. Plyr and the YouTube iframe load only after the page is idle,
   or when the poster is chosen. The film file itself is not changed. */
(function () {
  var figs = document.querySelectorAll('figure.crs-film');
  if (!figs.length) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function loadCss(href, done) {
    var existing = document.querySelector('link[data-nasa-plyr]');
    if (existing) {
      if (existing.sheet) done();
      else existing.addEventListener('load', done, { once: true });
      return;
    }
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    link.setAttribute('data-nasa-plyr', '');
    link.addEventListener('load', done, { once: true });
    link.addEventListener('error', done, { once: true });
    document.head.appendChild(link);
  }

  function loadScript(src, done) {
    if (window.Plyr) { done(); return; }
    var s = document.createElement('script');
    s.src = src;
    s.async = true;
    s.onload = function () { done(); };
    s.onerror = function () { done(new Error('plyr')); };
    document.head.appendChild(s);
  }

  function clock(sec) {
    sec = Math.floor(Number(sec));
    var m = Math.floor(sec / 60);
    var s = sec % 60;
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  function esc(text) {
    return String(text).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function boot(fig) {
    if (fig.getAttribute('data-booted')) return;
    fig.setAttribute('data-booted', '1');
    var poster = fig.querySelector('.crs-film-poster');
    var frame = fig.querySelector('.crs-film-frame');
    var id = fig.getAttribute('data-id') || '';
    if (!/^[A-Za-z0-9_-]{11}$/.test(id) || !poster || !frame) return;
    loadCss(fig.getAttribute('data-plyr-css'), function () {
      loadScript(fig.getAttribute('data-plyr'), function (err) {
        if (err || !window.Plyr) {
          fig.removeAttribute('data-booted');
          return;
        }
        var holder = document.createElement('div');
        holder.setAttribute('data-plyr-provider', 'youtube');
        holder.setAttribute('data-plyr-embed-id', id);
        poster.replaceWith(holder);
        var i18n = {};
        var raw = fig.getAttribute('data-i18n');
        if (!raw) {
          var donor = document.querySelector('figure.crs-film[data-i18n]');
          raw = donor ? donor.getAttribute('data-i18n') : '';
        }
        try { i18n = JSON.parse(raw || '{}'); } catch (e) {}
        var markers = [];
        fig.querySelectorAll('.crs-film-chapters button').forEach(function (b) {
          var span = b.querySelector('span');
          if (!span) return;
          markers.push({ time: Number(b.getAttribute('data-t')), label: span.textContent });
        });
        var titleEl = fig.querySelector('.crs-film-title');
        var player = new window.Plyr(holder, {
          autoplay: false,
          clickToPlay: true,
          playsinline: true,
          keyboard: { focused: true, global: false },
          tooltips: { controls: true, seek: true },
          ratio: '16:9',
          settings: ['speed'],
          speed: { selected: 1, options: [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2] },
          markers: { enabled: true, points: markers },
          youtube: { noCookie: true, rel: 0, showinfo: 0, iv_load_policy: 3, modestbranding: 1 },
          urls: { youtube: { api: fig.getAttribute('data-meta') } },
          title: titleEl ? titleEl.textContent.trim() : '',
          i18n: i18n,
        });
        fig._player = player;
        player.on('ready', function () {
          var speed = fig.querySelector('.crs-film-speed');
          if (speed) player.speed = Number(speed.value) || 1;
          if (fig._seek != null) player.currentTime = fig._seek;
          if (fig._sound) {
            player.volume = 1;
            player.muted = false;
          } else {
            player.volume = 1;
            player.muted = true;
          }
          var ret = player.play();
          if (ret && ret.catch) ret.catch(function () {});
          syncMute();
        });
        player.on('timeupdate', follow);
        player.on('seeked', follow);
        player.on('ratechange', function () {
          var speed = fig.querySelector('.crs-film-speed');
          if (!speed) return;
          var v = String(player.speed);
          if (speed.querySelector('option[value="' + v + '"]')) speed.value = v;
        });
        player.on('volumechange', syncMute);
        function syncMute() {
          var btn = fig.querySelector('.crs-film-unmute');
          if (!btn) return;
          var muted = !!(player.muted || player.volume === 0);
          if (muted) btn.removeAttribute('hidden');
          else btn.setAttribute('hidden', '');
        }
        function follow() {
          var t = Number(player.currentTime) || 0;
          var buttons = fig.querySelectorAll('.crs-film-lines button');
          var current = null;
          for (var i = 0; i < buttons.length; i++) {
            if (Number(buttons[i].getAttribute('data-t')) <= t + 0.2) current = buttons[i];
            else break;
          }
          buttons.forEach(function (b) { b.removeAttribute('aria-current'); });
          var cc = fig.querySelector('.crs-film-cc');
          if (!current) {
            if (cc) cc.textContent = '';
            return;
          }
          current.setAttribute('aria-current', 'true');
          var line = current.querySelector('.crs-film-line');
          if (cc && line) {
            cc.textContent = line.textContent;
            cc.lang = fig.querySelector('.crs-film-lines').lang || '';
            cc.dir = (cc.lang === 'ar' || cc.lang === 'he') ? 'rtl' : 'ltr';
          }
          reveal(current);
        }
      });
    });
  }

  function reveal(btn) {
    var ol = btn.closest('ol');
    if (!ol) return;
    var top = btn.offsetTop - ol.offsetTop;
    var bottom = top + btn.offsetHeight;
    if (top < ol.scrollTop) ol.scrollTop = top;
    else if (bottom > ol.scrollTop + ol.clientHeight) ol.scrollTop = bottom - ol.clientHeight;
  }

  function paint(fig, rows, lang) {
    var ol = fig.querySelector('.crs-film-lines');
    if (!ol) return;
    var html = rows.map(function (row) {
      return '<li><button type="button" data-t="' + row.t + '"><bdi class="crs-film-timeb" dir="ltr">' +
        clock(row.t) + '</bdi> <span class="crs-film-line">' + esc(row[lang]) + '</span></button></li>';
    }).join('');
    ol.innerHTML = html;
    ol.lang = lang;
    ol.dir = (lang === 'ar' || lang === 'he') ? 'rtl' : 'ltr';
    var note = fig.querySelector('.crs-film-script .crs-film-note');
    if (note) note.textContent = lang === 'en' ? note.getAttribute('data-note-en') : note.getAttribute('data-note-tr');
  }

  figs.forEach(function (fig) {
    var pageLang = fig.getAttribute('data-lang') || 'en';
    var linesEl = fig.querySelector('.crs-film-lines');
    var original = linesEl ? linesEl.innerHTML : '';
    var poster = fig.querySelector('.crs-film-poster');
    if (poster) {
      poster.addEventListener('click', function (e) {
        e.preventDefault();
        if (fig.getAttribute('data-autoplay') !== '1') fig._sound = true;
        boot(fig);
      });
    }
    fig.addEventListener('click', function (e) {
      var line = e.target.closest('.crs-film-lines button, .crs-film-chapters button');
      if (line && fig.contains(line)) {
        fig._seek = Number(line.getAttribute('data-t'));
        if (fig._player) {
          fig._player.currentTime = fig._seek;
          var ret = fig._player.play();
          if (ret && ret.catch) ret.catch(function () {});
        } else boot(fig);
        return;
      }
      var copy = e.target.closest('[data-copy]');
      if (copy && fig.contains(copy)) {
        var node = document.getElementById(copy.getAttribute('data-copy'));
        if (!node) return;
        var text = node.textContent;
        var label = copy.textContent;
        function done() {
          copy.textContent = copy.getAttribute('data-copied') || label;
          window.setTimeout(function () { copy.textContent = label; }, 1600);
        }
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(text).then(done, fallback);
        } else fallback();
        function fallback() {
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.setAttribute('readonly', '');
          ta.style.position = 'fixed';
          ta.style.insetInlineStart = '0';
          ta.style.top = '0';
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand('copy'); done(); } catch (err) {}
          ta.remove();
        }
      }
    });
    var unmute = fig.querySelector('.crs-film-unmute');
    if (unmute) {
      unmute.addEventListener('click', function () {
        fig._sound = true;
        if (!fig._player) { boot(fig); return; }
        fig._player.volume = 1;
        fig._player.muted = false;
      });
    }
    var speed = fig.querySelector('.crs-film-speed');
    if (speed) {
      speed.addEventListener('change', function () {
        if (fig._player) fig._player.speed = Number(speed.value) || 1;
      });
    }
    var select = fig.querySelector('.crs-film-cc-lang');
    if (select) {
      select.addEventListener('change', function () {
        var lang = select.value;
        if (lang === pageLang) {
          var ol = fig.querySelector('.crs-film-lines');
          if (!ol) return;
          ol.innerHTML = original;
          ol.lang = pageLang;
          ol.dir = (pageLang === 'ar' || pageLang === 'he') ? 'rtl' : 'ltr';
          var note = fig.querySelector('.crs-film-script .crs-film-note');
          if (note) note.textContent = pageLang === 'en' ? note.getAttribute('data-note-en') : note.getAttribute('data-note-tr');
          return;
        }
        var apply = function (rows) { paint(fig, rows, lang); };
        if (fig._cues) { apply(fig._cues); return; }
        fetch(fig.getAttribute('data-cues')).then(function (r) { return r.json(); }).then(function (rows) {
          fig._cues = rows;
          apply(rows);
        }).catch(function () { select.value = pageLang; });
      });
    }
    var script = fig.querySelector('.crs-film-script');
    if (script) {
      script.addEventListener('toggle', function () {
        if (!script.open) return;
        var current = fig.querySelector('.crs-film-lines button[aria-current="true"]');
        if (current) reveal(current);
      });
    }
    if (!reduce && fig.getAttribute('data-autoplay') === '1') {
      // The YouTube frame shifts inside itself as its player draws. Starting it
      // a few seconds after load keeps that shift out of the first paint.
      // Only the featured film autoplays. Every other film waits for a click.
      var kick = function () { window.setTimeout(function () { boot(fig); }, 5000); };
      if (document.readyState === 'complete') kick();
      else window.addEventListener('load', kick);
    }
  });
})();
