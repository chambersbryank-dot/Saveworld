/* Launch tracker actions: "Ask about this launch" (mailto) + "Add to my calendar" (.ics / Google).
   Enhances the Launch Library 2 widget (#lw-next, #lw-list; assets/launch-tracker.js) without replacing blurbs:
   reads the same sessionStorage cache (sp-ll2-upcoming) and re-attaches on every re-render. */
(function () {
  var nextEl = document.getElementById('lw-next');
  var listEl = document.getElementById('lw-list');
  if (!nextEl || !listEl) return;
  var MAIL = 'hello@savingplanets.com';
  var lang = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase();
  var T = {
    en: { ask: 'Ask about this launch', cal: 'Add to my calendar', gcal: 'Google Calendar', subj: 'Launch question', body: 'Hi Saving Planets team,\n\nI have a question about this launch:\n\n', may: 'Time may change', askL: 'Email a question about {m}', calL: 'Download a calendar file for {m}', gcalL: 'Add {m} to Google Calendar (opens in a new tab)', note: 'Launch times shift often. Re-add this event to update it. Schedule:', net: 'NET' },
    fr: { ask: 'Poser une question sur ce lancement', cal: 'Ajouter à mon agenda', gcal: 'Google Agenda', subj: 'Question sur un lancement', body: 'Bonjour l\u2019équipe Saving Planets,\n\nJ\u2019ai une question sur ce lancement :\n\n', may: 'L\u2019heure peut changer', askL: 'Envoyer une question sur {m}', calL: 'Télécharger un fichier agenda pour {m}', gcalL: 'Ajouter {m} à Google Agenda (nouvel onglet)', note: 'Les horaires de lancement changent souvent. Ajoutez à nouveau cet événement pour le mettre à jour. Calendrier :', net: 'Pas avant' },
    es: { ask: 'Preguntar por este lanzamiento', cal: 'Añadir a mi calendario', gcal: 'Google Calendar', subj: 'Pregunta sobre un lanzamiento', body: 'Hola, equipo de Saving Planets:\n\nTengo una pregunta sobre este lanzamiento:\n\n', may: 'La hora puede cambiar', askL: 'Enviar una pregunta sobre {m}', calL: 'Descargar un archivo de calendario para {m}', gcalL: 'Añadir {m} a Google Calendar (nueva pestaña)', note: 'Los horarios de lanzamiento cambian a menudo. Vuelve a añadir este evento para actualizarlo. Calendario:', net: 'No antes de' },
    it: { ask: 'Chiedi di questo lancio', cal: 'Aggiungi al mio calendario', gcal: 'Google Calendar', subj: 'Domanda su un lancio', body: 'Ciao team di Saving Planets,\n\nho una domanda su questo lancio:\n\n', may: 'L\u2019orario può cambiare', askL: 'Invia una domanda su {m}', calL: 'Scarica un file calendario per {m}', gcalL: 'Aggiungi {m} a Google Calendar (nuova scheda)', note: 'Gli orari di lancio cambiano spesso. Aggiungi di nuovo questo evento per aggiornarlo. Calendario:', net: 'Non prima del' },
    ar: { ask: 'اسأل عن هذا الإطلاق', cal: 'أضف إلى تقويمي', gcal: 'تقويم Google', subj: 'سؤال عن إطلاق', body: 'مرحبًا فريق Saving Planets،\n\nلدي سؤال عن هذا الإطلاق:\n\n', may: 'قد يتغير الموعد', askL: 'أرسل سؤالًا عن {m}', calL: 'نزّل ملف تقويم لـ {m}', gcalL: 'أضف {m} إلى تقويم Google (علامة تبويب جديدة)', note: 'تتغير مواعيد الإطلاق كثيرًا. أعد إضافة هذا الحدث لتحديثه. الجدول:', net: 'ليس قبل' },
    he: { ask: 'שאלו על השיגור הזה', cal: 'הוסיפו ליומן שלי', gcal: 'יומן Google', subj: 'שאלה על שיגור', body: 'שלום צוות Saving Planets,\n\nיש לי שאלה על השיגור הזה:\n\n', may: 'השעה עשויה להשתנות', askL: 'שלחו שאלה על {m}', calL: 'הורידו קובץ יומן עבור {m}', gcalL: 'הוסיפו את {m} ליומן Google (כרטיסייה חדשה)', note: 'מועדי שיגור משתנים לעיתים קרובות. הוסיפו את האירוע שוב כדי לעדכן אותו. לוח השיגורים:', net: 'לא לפני' }
  };
  var t = T[lang] || T.en;
  var PAGE = location.origin + location.pathname + '#launches';

  if (!document.getElementById('la-style')) {
    var st = document.createElement('style'); st.id = 'la-style';
    st.textContent = '.la-acts{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 4px;align-items:center}' +
      '.la-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;padding:8px 14px;border-radius:10px;border:1px solid rgba(143,211,255,.55);background:rgba(143,211,255,.10);color:#cfeaff;font:600 .9rem/1.2 inherit;text-decoration:none;cursor:pointer;box-sizing:border-box}' +
      '.la-btn:hover{background:rgba(143,211,255,.22)}.la-btn:focus-visible{outline:3px solid #ffd166;outline-offset:2px}' +
      '.la-may{font-size:.8rem;color:#ffd166;font-weight:700}' +
      '#lw-list li.la-row{flex-wrap:wrap}#lw-list li .la-acts{flex-basis:100%}';
    document.head.appendChild(st);
  }

  function data() { try { var c = JSON.parse(sessionStorage.getItem('sp-ll2-upcoming')); return c && c.d && c.d.results ? c.d.results : null; } catch (e) { return null; } }
  function launches() {
    var now = Date.now(), r = data();
    if (!r) return null;
    return r.filter(function (l) {
      var ab = l.status && l.status.abbrev ? String(l.status.abbrev).toLowerCase() : '';
      if (ab === 'success' || ab === 'failure' || ab === 'partial failure') return false;
      var x = new Date(l.net).getTime(); return isNaN(x) || x > now;
    });
  }
  function mission(l) { if (l.mission && l.mission.name) return l.mission.name; var p = String(l.name || '').split('|'); return (p[1] || p[0] || 'Launch').trim(); }
  function rocket(l) { return (l.rocket && l.rocket.configuration && l.rocket.configuration.name) || ''; }
  function where(l) { var p = l.pad || {}; return [p.name, p.location && p.location.name].filter(Boolean).join(', '); }
  function uncertain(l) {
    var ab = l.status && l.status.abbrev ? String(l.status.abbrev).toUpperCase() : '';
    var prec = l.net_precision && l.net_precision.name ? String(l.net_precision.name).toLowerCase() : '';
    return ab === 'TBD' || ab === 'TBC' || (prec && prec !== 'second' && prec !== 'minute');
  }
  function stamp(d) { return d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, ''); }
  function times(l) {
    var s = new Date(l.window_start || l.net), e = new Date(l.window_end || l.net);
    if (isNaN(s)) return null;
    if (isNaN(e) || e - s < 30 * 60000) e = new Date(s.getTime() + 60 * 60000); /* zero/instantaneous window: show 1 hour */
    return { s: s, e: e };
  }
  function icsEsc(s) { return String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n'); }
  function fold(line) { var o = '', b = 0; for (var i = 0; i < line.length; i++) { if (b >= 70) { o += '\r\n '; b = 0; } o += line[i]; b++; } return o; }
  function title(l) { return mission(l) + (rocket(l) ? ' \u2013 ' + rocket(l) : '') + (uncertain(l) ? ' (' + t.may + ')' : ''); }
  function desc(l) { return (uncertain(l) ? t.may + '. ' : '') + t.note + ' ' + PAGE; }
  function ics(l, tm) {
    var uid = 'll2-' + (l.id || mission(l).replace(/\W+/g, '-')) + '@savingplanets.com';
    var seq = Math.floor(new Date(l.last_updated || Date.now()).getTime() / 1000) % 2147483647;
    var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Saving Planets//Launch Tracker//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
      'BEGIN:VEVENT', 'UID:' + uid, 'SEQUENCE:' + seq, 'DTSTAMP:' + stamp(new Date()), 'LAST-MODIFIED:' + stamp(new Date(l.last_updated || Date.now())),
      'DTSTART:' + stamp(tm.s), 'DTEND:' + stamp(tm.e), 'SUMMARY:' + icsEsc(title(l)), 'LOCATION:' + icsEsc(where(l)),
      'DESCRIPTION:' + icsEsc(desc(l)), 'URL:' + PAGE, 'STATUS:' + (uncertain(l) ? 'TENTATIVE' : 'CONFIRMED'), 'END:VEVENT', 'END:VCALENDAR'];
    return L.map(fold).join('\r\n') + '\r\n';
  }
  function dateStr(l) { var d = new Date(l.net); return isNaN(d) ? 'TBD' : d.toISOString().slice(0, 10) + (uncertain(l) ? ' (' + t.net + ')' : ' ' + d.toISOString().slice(11, 16) + ' UTC'); }
  function lab(s, l) { return s.replace('{m}', mission(l)); }
  function el(tag, cls, txt, attrs) { var e = document.createElement(tag); e.className = cls; if (txt) e.textContent = txt; for (var k in attrs || {}) e.setAttribute(k, attrs[k]); return e; }
  var urls = [];
  function actions(l) {
    var box = el('div', 'la-acts', '', { 'data-la': l.id || mission(l) });
    var subj = t.subj + ': ' + mission(l) + ' \u2013 ' + (rocket(l) || '?') + ' \u2013 ' + dateStr(l);
    var body = t.body + mission(l) + ' / ' + rocket(l) + ' / ' + dateStr(l) + '\n' + PAGE + '\n\n';
    box.appendChild(el('a', 'la-btn la-ask', t.ask, { href: 'mailto:' + MAIL + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(body), 'aria-label': lab(t.askL, l) }));
    var tm = times(l);
    if (tm) {
      var blob = new Blob([ics(l, tm)], { type: 'text/calendar;charset=utf-8' }), u = URL.createObjectURL(blob); urls.push(u);
      var fn = ('launch-' + mission(l)).replace(/[^\w-]+/g, '-').replace(/-+/g, '-').slice(0, 60) + '.ics';
      box.appendChild(el('a', 'la-btn la-ics', t.cal, { href: u, download: fn, type: 'text/calendar', 'aria-label': lab(t.calL, l) }));
      var g = 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + encodeURIComponent(title(l)) + '&dates=' + stamp(tm.s) + '/' + stamp(tm.e) +
        '&details=' + encodeURIComponent(desc(l)) + '&location=' + encodeURIComponent(where(l));
      box.appendChild(el('a', 'la-btn la-gcal', t.gcal, { href: g, target: '_blank', rel: 'noopener noreferrer', 'aria-label': lab(t.gcalL, l) }));
    }
    if (uncertain(l)) box.appendChild(el('span', 'la-may', t.may));
    return box;
  }
  var busy = false;
  function attach() {
    if (busy) return; var r = launches(); if (!r || !r.length) return;
    busy = true;
    try {
      if (nextEl.querySelector('.lw-mission') && !nextEl.querySelector('.la-acts')) {
        var cd = nextEl.querySelector('.lw-countdown'), a = actions(r[0]);
        cd && cd.parentNode === nextEl ? nextEl.insertBefore(a, cd.nextSibling) : nextEl.appendChild(a);
      }
      var lis = listEl.children, rest = r.slice(1, 20);
      if (lis.length && !listEl.querySelector('.la-acts')) {
        urls.forEach(function (u) { if (!document.querySelector('a[href="' + u + '"]')) URL.revokeObjectURL(u); });
        for (var i = 0; i < lis.length && i < rest.length; i++) { lis[i].classList.add('la-row'); lis[i].appendChild(actions(rest[i])); }
      }
    } finally { busy = false; }
  }
  if (window.MutationObserver) { var mo = new MutationObserver(attach); mo.observe(nextEl, { childList: true }); mo.observe(listEl, { childList: true }); }
  attach();
})();
