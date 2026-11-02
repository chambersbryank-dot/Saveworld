/* Printable lesson plan. Data: assets/data/lesson-plan.<lang>.json. No analytics. */
(function () {
  var root = document.getElementById('lp');
  if (!root) return;
  var form = document.getElementById('lp-form');
  var list = document.getElementById('lp-sols');
  var plan = document.getElementById('lp-plan');
  var printBtn = document.getElementById('lp-print');
  var lang = document.documentElement.lang || 'en';
  var bits = location.pathname.split('/').filter(Boolean);
  var nested = bits.length >= 2 && /^(fr|es|ar|it|he)$/.test(bits[bits.length - 2]);
  var data = null;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function fail() {
    var tpl = document.querySelector('.lp-error-tpl');
    if (tpl && plan) { plan.hidden = false; plan.textContent = ''; plan.appendChild(tpl.content.cloneNode(true)); }
  }
  function selected() {
    return [].slice.call(list.querySelectorAll('input:checked')).map(function (i) { return i.value; });
  }
  function byUrl(u) {
    for (var i = 0; i < data.solutions.length; i++) if (data.solutions[i].u === u) return data.solutions[i];
  }
  function split(min) {
    var read = Math.max(5, Math.round(min * 0.4 / 5) * 5);
    var talk = Math.max(5, Math.round(min * 0.4 / 5) * 5);
    var write = min - read - talk;
    if (write < 5) { write = 5; talk = Math.max(5, min - read - write); }
    if (read + talk + write !== min) write = min - read - talk;
    return [read, talk, write];
  }
  function fill() {
    var g = form.grade.value, s = form.subject.value;
    var keep = {};
    selected().forEach(function (u) { keep[u] = 1; });
    list.textContent = '';
    var n = 0;
    data.solutions.forEach(function (sol) {
      if (sol.grades.indexOf(g) < 0 || sol.subjects.indexOf(s) < 0) return;
      n++;
      var lab = document.createElement('label');
      var box = document.createElement('input');
      box.type = 'checkbox';
      box.value = sol.u;
      box.name = 'sol';
      if (keep[sol.u]) box.checked = true;
      lab.appendChild(box);
      lab.appendChild(document.createTextNode(sol.n));
      list.appendChild(lab);
    });
    var empty = document.getElementById('lp-none');
    if (empty) empty.hidden = n > 0;
  }
  function build(e) {
    if (e) e.preventDefault();
    var ui = data.ui;
    var ids = selected();
    plan.hidden = false;
    plan.textContent = '';
    if (!ids.length) { plan.appendChild(el('p', null, ui.pick)); printBtn.hidden = true; return; }
    var sols = ids.map(byUrl).filter(Boolean);
    var g = form.grade.value, sub = form.subject.value, min = +form.minutes.value;
    var gLabel = form.grade.selectedOptions[0].textContent;
    var sLabel = form.subject.selectedOptions[0].textContent;
    var tm = split(min);
    plan.appendChild(el('h2', null, ui.title));
    plan.appendChild(el('p', 'lp-meta', gLabel + ' · ' + sLabel + ' · ' + ui.minutes.replace('{n}', String(min))));
    plan.appendChild(el('h3', null, ui.solutions));
    var ul = document.createElement('ul');
    sols.forEach(function (sol) {
      var li = document.createElement('li');
      var a = el('a', null, sol.n);
      a.href = sol.u;
      li.appendChild(a);
      ul.appendChild(li);
    });
    plan.appendChild(ul);
    plan.appendChild(el('h3', null, ui.objectives));
    var seen = {}, objs = [];
    sols.forEach(function (sol) {
      (sol.standards || []).forEach(function (c) {
        if (c.band !== g || c.subject !== sub || seen[c.code]) return;
        seen[c.code] = 1; objs.push(c);
      });
    });
    if (!objs.length) plan.appendChild(el('p', null, ui.noObj));
    else {
      var ou = document.createElement('ul');
      objs.forEach(function (c) {
        var li = document.createElement('li');
        li.appendChild(el('span', null, c.code + '. '));
        var tx = el('span', null, c.text);
        tx.lang = 'en';
        li.appendChild(tx);
        ou.appendChild(li);
      });
      plan.appendChild(ou);
    }
    plan.appendChild(el('h3', null, ui.standards));
    plan.appendChild(el('p', 'lp-note', ui.stdNote));
    var su = el('ul', 'lp-std');
    var codes = objs.length ? objs : [];
    if (!codes.length) plan.appendChild(el('p', null, ui.noObj));
    codes.forEach(function (c) {
      var li = document.createElement('li');
      var a = el('a', null, c.code);
      a.href = c.url; a.target = '_blank'; a.rel = 'noopener';
      li.appendChild(a);
      li.appendChild(document.createTextNode(' (' + c.band + '). '));
      var tx = el('span', null, c.text);
      tx.lang = 'en';
      li.appendChild(tx);
      su.appendChild(li);
    });
    if (codes.length) plan.appendChild(su);
    plan.appendChild(el('h3', null, ui.activity));
    plan.appendChild(el('p', 'lp-note', ui.timing));
    var ol = document.createElement('ol');
    var steps = [
      [ui.read.replace('{n}', String(tm[0])), 'eli'],
      [ui.talk.replace('{n}', String(tm[1])), 'q'],
      [ui.write.replace('{n}', String(tm[2])), 'a']
    ];
    steps.forEach(function (step) {
      var li = document.createElement('li');
      li.appendChild(el('strong', null, step[0]));
      if (step[1] === 'eli') {
        sols.forEach(function (sol) {
          if (!sol.eli || !sol.eli.length) return;
          var p = el('p', null, sol.n + ' — ');
          p.appendChild(document.createTextNode(sol.eli[0]));
          li.appendChild(p);
        });
      }
      ol.appendChild(li);
    });
    plan.appendChild(ol);
    plan.appendChild(el('h3', null, ui.questions));
    var qo = document.createElement('ol');
    sols.forEach(function (sol) {
      (sol.questions || []).forEach(function (q) {
        qo.appendChild(el('li', null, sol.n + ': ' + q));
      });
    });
    plan.appendChild(qo);
    plan.appendChild(el('h3', null, ui.assessment));
    plan.appendChild(el('p', null, ui.assessText));
    plan.appendChild(el('h3', null, ui.sources));
    var src = document.createElement('ul');
    sols.forEach(function (sol) {
      var li = document.createElement('li');
      li.appendChild(document.createTextNode(sol.n + '. '));
      if (sol.src && sol.src.href) {
        var a = el('a', null, sol.src.name || sol.src.href);
        a.href = sol.src.href; a.target = '_blank'; a.rel = 'noopener';
        li.appendChild(a);
      }
      src.appendChild(li);
    });
    plan.appendChild(src);
    printBtn.hidden = false;
    var url = new URL(location.href);
    url.searchParams.set('grade', g);
    url.searchParams.set('subject', sub);
    url.searchParams.set('min', String(min));
    url.searchParams.set('sols', ids.join(','));
    history.replaceState(null, '', url);
  }
  fetch((nested ? '../' : '') + 'assets/data/lesson-plan.' + lang + '.json')
    .then(function (r) { if (!r.ok) throw new Error('load'); return r.json(); })
    .then(function (j) {
      data = j;
      var q = new URLSearchParams(location.search);
      if (q.get('grade')) form.grade.value = q.get('grade');
      if (q.get('subject')) form.subject.value = q.get('subject');
      if (q.get('min')) form.minutes.value = q.get('min');
      fill();
      (q.get('sols') || '').split(',').forEach(function (u) {
        var box = list.querySelector('input[value="' + CSS.escape(u) + '"]');
        if (box) box.checked = true;
      });
      form.grade.addEventListener('change', fill);
      form.subject.addEventListener('change', fill);
      form.addEventListener('submit', build);
      printBtn.addEventListener('click', function () { window.print(); });
      if (q.get('sols')) build();
    })
    .catch(fail);
})();
