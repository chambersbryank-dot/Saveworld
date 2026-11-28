/* Unit quiz and flashcards. The question file loads on Start. Nothing is sent off this browser. */
(function () {
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var rtl = lang === 'ar' || lang === 'he';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var UI = {
    en: {
      start: 'Start', flip: 'Flip', know: 'Know it', learn: 'Still learning',
      review: 'Review missed only', restart: 'Restart shuffled',
      retry: 'Retry missed only', retake: 'Retake, shuffled',
      next: 'Next', check: 'Check', truth: 'True', fals: 'False',
      correct: 'Correct.', wrong: 'Not quite. The answer is: {x}.',
      yours: 'Your answer', right: 'Correct answer', score: 'Score', time: 'Time',
      topics: 'By topic', known: 'Known', learning: 'Still learning', pct: 'Percent',
      save: 'Print / Save results', none: 'Nothing missed.',
      all: 'Every card is known.', err: 'This check could not be loaded.',
      num: 'Type a number', qlead: '{n} questions · about {m} minutes',
      clead: '{n} cards · about {m} minutes', prog: '{i} / {n}'
    },
    fr: {
      start: 'Commencez', flip: 'Retournez', know: 'Je la sais', learn: 'À revoir',
      review: 'Revoir seulement celles à revoir', restart: 'Recommencer, mélangé',
      retry: 'Reprendre seulement les erreurs', retake: 'Recommencer, mélangé',
      next: 'Suivante', check: 'Vérifier', truth: 'Vrai', fals: 'Faux',
      correct: 'Juste.', wrong: 'Pas tout à fait. La réponse est : {x}.',
      yours: 'Votre réponse', right: 'Bonne réponse', score: 'Score', time: 'Temps',
      topics: 'Par sujet', known: 'Sues', learning: 'À revoir', pct: 'Pourcentage',
      save: 'Imprimer / enregistrer les résultats', none: 'Aucune erreur.',
      all: 'Toutes les cartes sont sues.', err: 'Ce contrôle n’a pas pu se charger.',
      num: 'Écrivez un nombre', qlead: '{n} questions · environ {m} minutes',
      clead: '{n} cartes · environ {m} minutes', prog: '{i} / {n}'
    },
    es: {
      start: 'Empieza', flip: 'Voltea', know: 'La sé', learn: 'Aún la estudio',
      review: 'Repasa solo las que faltan', restart: 'Vuelve a empezar, barajado',
      retry: 'Repite solo los fallos', retake: 'Repite, barajado',
      next: 'Siguiente', check: 'Comprueba', truth: 'Verdadero', fals: 'Falso',
      correct: 'Correcto.', wrong: 'Casi. La respuesta es: {x}.',
      yours: 'Tu respuesta', right: 'Respuesta correcta', score: 'Puntuación', time: 'Tiempo',
      topics: 'Por tema', known: 'Sabidas', learning: 'Aún por aprender', pct: 'Porcentaje',
      save: 'Imprimir / guardar los resultados', none: 'Ningún fallo.',
      all: 'Todas las tarjetas están sabidas.', err: 'Esta comprobación no se pudo cargar.',
      num: 'Escribe un número', qlead: '{n} preguntas · unos {m} minutos',
      clead: '{n} tarjetas · unos {m} minutos', prog: '{i} / {n}'
    },
    ar: {
      start: 'ابدأ', flip: 'اقلب', know: 'أعرفها', learn: 'ما زلت أتعلمها',
      review: 'راجع ما لم يُتقن فقط', restart: 'أعد البدء مع الخلط',
      retry: 'أعد الأخطاء فقط', retake: 'أعد الاختبار مع الخلط',
      next: 'التالية', check: 'تحقق', truth: 'صواب', fals: 'خطأ',
      correct: 'صحيح.', wrong: 'ليس تمامًا. الإجابة هي: {x}.',
      yours: 'إجابتك', right: 'الإجابة الصحيحة', score: 'النتيجة', time: 'الوقت',
      topics: 'حسب الموضوع', known: 'معروفة', learning: 'ما زلت أتعلمها', pct: 'النسبة',
      save: 'اطبع / احفظ النتائج', none: 'لا أخطاء.',
      all: 'كل البطاقات معروفة.', err: 'تعذّر تحميل هذا الاختبار.',
      num: 'اكتب عددًا', qlead: '{n} أسئلة · نحو {m} دقائق',
      clead: '{n} بطاقات · نحو {m} دقائق', prog: '{i} / {n}'
    },
    it: {
      start: 'Inizia', flip: 'Gira', know: 'La so', learn: 'Ancora da imparare',
      retry: 'Ripeti solo gli errori', retake: 'Rifai, mescolato',
      review: 'Ripassa solo quelle da imparare', restart: 'Ricomincia, mescolato',
      next: 'Successiva', check: 'Controlla', truth: 'Vero', fals: 'Falso',
      correct: 'Giusto.', wrong: 'Non proprio. La risposta è: {x}.',
      yours: 'La tua risposta', right: 'Risposta corretta', score: 'Punteggio', time: 'Tempo',
      topics: 'Per argomento', known: 'Imparate', learning: 'Ancora da imparare', pct: 'Percentuale',
      save: 'Stampa / salva i risultati', none: 'Nessun errore.',
      all: 'Tutte le carte sono imparate.', err: 'Questo controllo non si è caricato.',
      num: 'Scrivi un numero', qlead: '{n} domande · circa {m} minuti',
      clead: '{n} carte · circa {m} minuti', prog: '{i} / {n}'
    },
    he: {
      start: 'התחילו', flip: 'הפכו', know: 'יודעים', learn: 'עדיין לומדים',
      review: 'חזרו רק על מה שעדיין לומדים', restart: 'התחילו מחדש, מעורבב',
      retry: 'נסו שוב רק את הטעויות', retake: 'נסו שוב, מעורבב',
      next: 'הבא', check: 'בדקו', truth: 'אמת', fals: 'שקר',
      correct: 'נכון.', wrong: 'לא בדיוק. התשובה היא: {x}.',
      yours: 'התשובה שלכם', right: 'התשובה הנכונה', score: 'ציון', time: 'זמן',
      topics: 'לפי נושא', known: 'ידועים', learning: 'עדיין לומדים', pct: 'אחוז',
      save: 'הדפסה / שמירת התוצאות', none: 'אין טעויות.',
      all: 'כל הכרטיסים ידועים.', err: 'לא ניתן היה לטעון את הבדיקה הזו.',
      num: 'כתבו מספר', qlead: '{n} שאלות · כ-{m} דקות',
      clead: '{n} כרטיסים · כ-{m} דקות', prog: '{i} / {n}'
    }
  };
  var T = UI[lang] || UI.en;
  var cache = {};
  var course = ((document.querySelector('.crs[data-course]') || {}).dataset || {}).course || 'aero101';
  var storeKey = 'sp-check:' + course;

  function fill(s, o) {
    for (var k in o) s = s.split('{' + k + '}').join(o[k]);
    return s;
  }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function btn(label, fn) {
    var b = el('button', 'crs-btn', label);
    b.type = 'button';
    b.addEventListener('click', fn);
    return b;
  }
  function shuffle(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function load(src) {
    if (!cache[src]) {
      cache[src] = fetch(src).then(function (r) {
        if (!r.ok) throw new Error('load');
        return r.json();
      });
    }
    return cache[src];
  }
  function parseNum(s) {
    s = String(s).trim().replace(/\s/g, '');
    if (/^-?\d{1,3}([.,]\d{3})+$/.test(s)) s = s.replace(/[.,]/g, '');
    else s = s.replace(',', '.');
    return parseFloat(s);
  }
  function clock(ms) {
    var s = Math.round(ms / 1000);
    var m = Math.floor(s / 60);
    s = s % 60;
    return m + ':' + (s < 10 ? '0' : '') + s;
  }
  function remember(unit, kind, rec) {
    var all = {};
    try { all = JSON.parse(localStorage.getItem(storeKey) || '{}'); } catch (e) { all = {}; }
    all[unit] = all[unit] || {};
    all[unit][kind] = rec;
    try { localStorage.setItem(storeKey, JSON.stringify(all)); } catch (e) {}
  }
  function saveText(name, text) {
    var blob = new Blob([text], { type: 'text/plain' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1500);
  }
  function bar(i, n) {
    var wrap = el('div', 'crs-check-bar');
    var p = document.createElement('progress');
    p.max = n; p.value = i;
    p.setAttribute('aria-label', fill(T.prog, { i: i, n: n }));
    var lab = el('span', 'crs-check-pos', fill(T.prog, { i: i, n: n }));
    if (rtl) lab.dir = 'ltr';
    wrap.appendChild(p);
    wrap.appendChild(lab);
    return wrap;
  }
  function focus(node) {
    if (!node) return;
    if (!node.hasAttribute('tabindex')) node.tabIndex = -1;
    node.focus();
  }

  function runQuiz(box, data, only) {
    var items = shuffle(only || data.quiz.slice()).map(function (q) {
      var src = q.raw || q;
      var copy = {
        type: src.type, topic: src.topic, q: src.q, why: src.why, src: src.src, srcName: src.srcName,
        ok: src.ok, tol: src.tol, unit: src.unit || '', raw: src
      };
      if (src.type === 'tf') {
        copy.opts = shuffle([{ t: T.truth, v: src.ok === true }, { t: T.fals, v: src.ok === false }]);
      } else if (src.type === 'mc') {
        copy.opts = shuffle(src.opts.map(function (t, i) { return { t: t, v: i === src.ok }; }));
      }
      return copy;
    });
    var i = 0, right = 0, missed = [], topics = {}, t0 = Date.now(), timer = 0;
    box.innerHTML = '';
    var live = el('p', 'crs-live');
    live.setAttribute('aria-live', 'polite');
    var stage = el('div', 'crs-stage');
    box.appendChild(live);
    box.appendChild(stage);

    function show() {
      stage.innerHTML = '';
      if (i >= items.length) return finish();
      var q = items[i];
      stage.appendChild(bar(i + 1, items.length));
      var fs = document.createElement('fieldset');
      fs.className = 'crs-q';
      var lg = document.createElement('legend');
      lg.textContent = q.q;
      lg.dir = 'auto';
      fs.appendChild(lg);
      if (q.type === 'num') {
        var inp = document.createElement('input');
        inp.type = 'text';
        inp.inputMode = 'decimal';
        inp.className = 'crs-num';
        inp.setAttribute('aria-label', T.num);
        inp.autocomplete = 'off';
        inp.dir = 'ltr';
        fs.appendChild(inp);
        fs.appendChild(btn(T.check, function () { grade(q, inp.value, inp); }));
        inp.addEventListener('keydown', function (e) {
          if (e.key === 'Enter') { e.preventDefault(); grade(q, inp.value, inp); }
        });
      } else {
        var name = 'q' + i + '-' + Math.random().toString(36).slice(2, 7);
        q.opts.forEach(function (o) {
          var lab = document.createElement('label');
          var input = document.createElement('input');
          input.type = 'radio';
          input.name = name;
          input.value = o.t;
          input.dataset.ok = o.v ? '1' : '0';
          lab.appendChild(input);
          lab.appendChild(document.createTextNode(' ' + o.t));
          fs.appendChild(lab);
        });
        fs.appendChild(btn(T.check, function () {
          var picked = fs.querySelector('input:checked');
          if (!picked) return;
          grade(q, picked, picked);
        }));
      }
      stage.appendChild(fs);
      var fb = el('p', 'crs-fb');
      fb.setAttribute('aria-live', 'polite');
      stage.appendChild(fb);
      focus(lg);
    }

    function expected(q) {
      if (q.type === 'num') return String(q.ok) + (q.unit ? ' ' + q.unit : '');
      if (q.type === 'tf') return q.ok ? T.truth : T.fals;
      var hit = q.opts.filter(function (o) { return o.v; })[0];
      return hit ? hit.t : '';
    }
    function answered(q, value) {
      if (q.type === 'num') {
        var n = parseFloat(String(value).replace(',', '.'));
        return isNaN(n) ? String(value) : String(value);
      }
      if (q.type === 'tf') return value ? T.truth : T.fals;
      var hit = q.opts.filter(function (o) { return !!o.v === !!value; })[0];
      return hit ? hit.t : '';
    }
    function grade(q, value, node) {
      if (stage.querySelector('.crs-fb.ok, .crs-fb.no')) return;
      var ok = false, yours = '';
      if (q.type === 'num') {
        var n = parseNum(value);
        ok = !isNaN(n) && Math.abs(n - Number(q.ok)) <= Number(q.tol);
        yours = (isNaN(n) ? String(value) : String(n)) + (q.unit ? ' ' + q.unit : '');
      } else {
        ok = value.dataset.ok === '1';
        yours = value.value;
      }
      topics[q.topic] = topics[q.topic] || { ok: 0, n: 0 };
      topics[q.topic].n++;
      if (ok) { right++; topics[q.topic].ok++; }
      else missed.push({ q: q, yours: yours, expect: expected(q) });
      var fb = stage.querySelector('.crs-fb');
      fb.className = 'crs-fb ' + (ok ? 'ok' : 'no');
      var line = ok ? T.correct : fill(T.wrong, { x: expected(q) });
      fb.textContent = line + ' ' + q.why;
      stage.querySelectorAll('input, button').forEach(function (n) { n.disabled = true; });
      var next = btn(T.next, function () { go(); });
      stage.appendChild(next);
      focus(next);
      live.textContent = fb.textContent;
      if (!reduce) {
        timer = window.setTimeout(go, 3200);
        next.addEventListener('focus', function () {});
        fb.addEventListener('mouseenter', function () { window.clearTimeout(timer); });
      }
      node.disabled = true;
    }
    function go() {
      window.clearTimeout(timer);
      var fade = function () { i++; show(); };
      if (reduce) { fade(); return; }
      stage.classList.add('is-out');
      window.setTimeout(function () { stage.classList.remove('is-out'); fade(); }, 180);
    }
    function finish() {
      var n = items.length, pct = n ? Math.round(100 * right / n) : 0, ms = Date.now() - t0;
      stage.appendChild(el('h3', 'crs-end-h', T.score));
      var sum = el('p', 'crs-end-sum');
      sum.textContent = right + ' / ' + n + ' · ' + pct + '% · ' + clock(ms);
      if (rtl) sum.dir = 'ltr';
      stage.appendChild(sum);
      stage.appendChild(el('h3', null, T.topics));
      var ul = el('ul', 'crs-topics');
      Object.keys(topics).forEach(function (name) {
        var row = topics[name];
        ul.appendChild(el('li', null, name + ': ' + row.ok + ' / ' + row.n));
      });
      stage.appendChild(ul);
      stage.appendChild(el('h3', null, T.learning));
      if (!missed.length) stage.appendChild(el('p', null, T.none));
      var ol = el('ol', 'crs-miss');
      missed.forEach(function (m) {
        var li = document.createElement('li');
        li.appendChild(el('p', null, m.q.q));
        li.appendChild(el('p', null, T.yours + ': ' + m.yours));
        li.appendChild(el('p', null, T.right + ': ' + m.expect));
        li.appendChild(el('p', null, m.q.why));
        if (m.q.src) {
          var a = document.createElement('a');
          a.href = m.q.src;
          a.rel = 'noopener';
          a.textContent = m.q.srcName || m.q.src;
          li.appendChild(a);
        }
        ol.appendChild(li);
      });
      stage.appendChild(ol);
      var actions = el('div', 'crs-check-actions');
      var missedQs = missed.map(function (m) { return m.q.raw; });
      var again = btn(T.retry, function () { if (missedQs.length) runQuiz(box, data, missedQs); });
      again.disabled = !missedQs.length;
      actions.appendChild(again);
      actions.appendChild(btn(T.retake, function () { runQuiz(box, data); }));
      actions.appendChild(btn(T.save, function () {
        var lines = [sum.textContent, ''];
        missed.forEach(function (m) {
          lines.push(m.q.q, T.yours + ': ' + m.yours, T.right + ': ' + m.expect, m.q.why, m.q.src || '', '');
        });
        saveText('aero101-' + (box.dataset.unit || 'quiz') + '.txt', lines.join('\n'));
        window.print();
      }));
      stage.appendChild(actions);
      remember(box.dataset.unit, 'quiz', { score: right, n: n, pct: pct, ms: ms });
      focus(sum);
    }
    show();
  }

  function runCards(box, data, only) {
    var items = shuffle(only || data.cards.slice());
    var i = 0, known = 0, learning = [], flipped = false;
    box.innerHTML = '';
    var live = el('p', 'crs-live');
    live.setAttribute('aria-live', 'polite');
    var stage = el('div', 'crs-stage');
    box.appendChild(live);
    box.appendChild(stage);
    function show() {
      stage.innerHTML = '';
      if (i >= items.length) return finish();
      flipped = false;
      stage.appendChild(bar(i + 1, items.length));
      var card = el('button', 'crs-card', items[i].f);
      card.type = 'button';
      card.dir = 'auto';
      var mark = el('div', 'crs-check-actions');
      mark.hidden = true;
      function flip() {
        flipped = !flipped;
        card.textContent = flipped ? items[i].b : items[i].f;
        card.classList.toggle('is-back', flipped);
        mark.hidden = !flipped;
        live.textContent = card.textContent;
        if (flipped) focus(mark.querySelector('button'));
      }
      card.addEventListener('click', flip);
      var know = btn(T.know, function () { known++; i++; show(); });
      var still = btn(T.learn, function () { learning.push(items[i]); i++; show(); });
      mark.appendChild(know);
      mark.appendChild(still);
      var flipb = btn(T.flip, flip);
      stage.appendChild(card);
      stage.appendChild(flipb);
      stage.appendChild(mark);
      focus(card);
    }
    function finish() {
      var n = items.length, pct = n ? Math.round(100 * known / n) : 0;
      stage.appendChild(el('h3', null, T.known));
      var sum = el('p', 'crs-end-sum');
      sum.textContent = T.known + ' ' + known + ' · ' + T.learning + ' ' + learning.length + ' · ' + pct + '%';
      stage.appendChild(sum);
      stage.appendChild(el('h3', null, T.learning));
      if (!learning.length) stage.appendChild(el('p', null, T.all));
      var ol = el('ol', 'crs-miss');
      learning.forEach(function (c) {
        var li = document.createElement('li');
        li.appendChild(el('p', null, c.f));
        li.appendChild(el('p', null, c.b));
        ol.appendChild(li);
      });
      stage.appendChild(ol);
      var actions = el('div', 'crs-check-actions');
      var missed = learning.slice();
      var again = btn(T.review, function () { if (missed.length) runCards(box, data, missed); });
      again.disabled = !missed.length;
      actions.appendChild(again);
      actions.appendChild(btn(T.restart, function () { runCards(box, data); }));
      stage.appendChild(actions);
      remember(box.dataset.unit, 'cards', { known: known, n: n, pct: pct });
      focus(sum);
    }
    show();
  }

  document.querySelectorAll('.crs-deck, .crs-quizapp').forEach(function (box) {
    var go = box.querySelector('.crs-go');
    if (!go) return;
    go.addEventListener('click', function () {
      go.disabled = true;
      load(box.dataset.src).then(function (data) {
        if (box.classList.contains('crs-deck')) runCards(box, data);
        else runQuiz(box, data);
      }).catch(function () {
        go.disabled = false;
        var p = box.querySelector('.crs-live') || el('p', 'crs-live');
        p.textContent = T.err;
        if (!p.parentNode) box.appendChild(p);
      });
    });
  });
})();
