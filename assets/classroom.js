/* Google Classroom share for teachers. The official button script loads only after a teacher
   asks for it, and never on kids' pages. Docs (checked 2026-09-03):
   https://developers.google.com/workspace/classroom/guides/sharebutton
   Share-tag attributes used: url (required), title, body, itemtype, size, theme, locale.
   itemtype is announcement, assignment, material, or question.
   The share URL fallback documented there is https://classroom.google.com/share?url={url}.
   Points, due date, and "Make a copy for each student" can be set in Google's dialog, not by this page. */
(function () {
  var KIDS = /\/(?:Kids|Play_and_Learn|Kids_Map|Kids_World|Amazing_Facts|Space_Passport|Boarding_Pass|Myth_or_Fact_Arcade)\.html$/;
  if (KIDS.test(location.pathname)) return;
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var T = {
    en: { h: 'Google Classroom', type: 'Post as', assignment: 'Assignment', material: 'Material', question: 'Question', announcement: 'Announcement', show: 'Show the Classroom button', student: 'Student view', teacher: 'Teacher view', print: 'Print the answer key', copy: 'For an assignment, open the button, pick the class, and set points and a due date in Google’s dialog. This page cannot set those. To give each student a separate copy, print this page or save it as a PDF, put that file in Google Drive, attach it, and choose Make a copy for each student.', later: 'Not available from a static page: a Classroom quiz assignment, a Google Form, grade passback, and creating the Drive copy without a teacher login. Those need a Classroom add-on or OAuth.', noscript: 'Share to Google Classroom' },
    fr: { h: 'Google Classroom', type: 'Publier comme', assignment: 'Devoir', material: 'Support', question: 'Question', announcement: 'Annonce', show: 'Afficher le bouton Classroom', student: 'Vue élève', teacher: 'Vue enseignant', print: 'Imprimer le corrigé', copy: 'Pour un devoir, ouvrez le bouton, choisissez la classe, puis indiquez les points et la date dans la fenêtre de Google. Cette page ne peut pas les fixer. Pour une copie par élève, imprimez la page ou enregistrez-la en PDF, placez le fichier dans Google Drive, joignez-le et choisissez Créer une copie pour chaque élève.', later: 'Impossible depuis une page statique : un quiz Classroom, un Google Form, le renvoi des notes, et la copie Drive sans connexion de l’enseignant. Il faut un module Classroom ou OAuth.', noscript: 'Partager sur Google Classroom' },
    es: { h: 'Google Classroom', type: 'Publicar como', assignment: 'Tarea', material: 'Material', question: 'Pregunta', announcement: 'Anuncio', show: 'Mostrar el botón de Classroom', student: 'Vista del estudiante', teacher: 'Vista del docente', print: 'Imprimir la clave', copy: 'Para una tarea, abre el botón, elige la clase y pon los puntos y la fecha en la ventana de Google. Esta página no puede fijarlos. Para una copia por estudiante, imprime la página o guárdala como PDF, súbela a Google Drive, adjúntala y elige Hacer una copia para cada alumno.', later: 'No se puede desde una página estática: un cuestionario de Classroom, un Google Form, devolver notas, y crear la copia de Drive sin que el docente inicie sesión. Hace falta un complemento o OAuth.', noscript: 'Compartir en Google Classroom' },
    ar: { h: 'Google Classroom', type: 'انشر كـ', assignment: 'واجب', material: 'مادة', question: 'سؤال', announcement: 'إعلان', show: 'أظهر زر Classroom', student: 'عرض الطالب', teacher: 'عرض المعلّم', print: 'اطبع مفتاح الإجابات', copy: 'للواجب، افتح الزر واختر الصف ثم حدّد الدرجات وموعد التسليم في نافذة Google. لا تستطيع هذه الصفحة ضبطها. لمنح كل طالب نسخته، اطبع الصفحة أو احفظها PDF ثم ضع الملف في Google Drive وأرفقه واختر إنشاء نسخة لكل طالب.', later: 'غير متاح من صفحة ثابتة: اختبار Classroom، ونموذج Google، وإرجاع الدرجات، وإنشاء نسخة Drive بلا دخول المعلّم. يحتاج ذلك إلى إضافة أو OAuth.', noscript: 'شارك في Google Classroom' },
    it: { h: 'Google Classroom', type: 'Pubblica come', assignment: 'Compito', material: 'Materiale', question: 'Domanda', announcement: 'Annuncio', show: 'Mostra il pulsante Classroom', student: 'Vista studente', teacher: 'Vista docente', print: 'Stampa le soluzioni', copy: 'Per un compito, apri il pulsante, scegli la classe e imposta punti e scadenza nella finestra di Google. Questa pagina non può impostarli. Per una copia per ogni studente, stampa la pagina o salvala in PDF, metti il file in Google Drive, allegalo e scegli Crea una copia per ogni studente.', later: 'Non disponibile da una pagina statica: un quiz Classroom, un Google Form, la restituzione dei voti e la copia Drive senza accesso del docente. Servono un componente aggiuntivo o OAuth.', noscript: 'Condividi su Google Classroom' },
    he: { h: 'Google Classroom', type: 'פרסום כ', assignment: 'מטלה', material: 'חומר', question: 'שאלה', announcement: 'הודעה', show: 'הצגת כפתור Classroom', student: 'תצוגת תלמיד', teacher: 'תצוגת מורה', print: 'הדפסת מפתח התשובות', copy: 'למטלה, פתחו את הכפתור, בחרו כיתה וקבעו ניקוד ותאריך הגשה בחלון של Google. העמוד הזה לא יכול לקבוע אותם. כדי שלכל תלמיד יהיה עותק, הדפיסו את העמוד או שמרו PDF, העלו ל-Google Drive, צרפו ובחרו יצירת עותק לכל תלמיד.', later: 'לא זמין מעמוד סטטי: בוחן Classroom, טופס Google, החזרת ציונים, ויצירת עותק ב-Drive בלי כניסת מורה. אלה דורשים תוסף או OAuth.', noscript: 'שיתוף ב-Google Classroom' }
  };
  var L = T[lang] || T.en;
  var LOCALE = { en: 'en-US', fr: 'fr', es: 'es', ar: 'ar', it: 'it', he: 'he' }[lang] || 'en-US';
  var gapiReady = null;
  function loadGapi() {
    if (gapiReady) return gapiReady;
    gapiReady = new Promise(function (resolve) {
      window.___gcfg = { parsetags: 'explicit' };
      var s = document.createElement('script');
      s.src = 'https://apis.google.com/js/platform.js';
      s.onload = function () {
        var n = 0;
        (function wait() {
          if (window.gapi && gapi.sharetoclassroom && gapi.sharetoclassroom.render) resolve();
          else if (n++ < 40) setTimeout(wait, 50);
          else resolve();
        })();
      };
      s.onerror = function () { resolve(); };
      document.head.appendChild(s);
    });
    return gapiReady;
  }
  function shareUrl(url) {
    return 'https://classroom.google.com/share?url=' + encodeURIComponent(url);
  }
  function pageUrl(hash) {
    var u = location.href.split('#')[0];
    return hash ? u + hash : u;
  }
  function renderButton(box, opts) {
    var holder = box.querySelector('.gc-official');
    if (!holder) return;
    holder.innerHTML = '';
    var target = document.createElement('div');
    holder.appendChild(target);
    loadGapi().then(function () {
      if (!(window.gapi && gapi.sharetoclassroom && gapi.sharetoclassroom.render)) return;
      gapi.sharetoclassroom.render(target, {
        url: opts.url, title: opts.title, body: opts.body, itemtype: opts.itemtype,
        size: 32, theme: 'dark', locale: LOCALE
      });
    });
  }
  function panel(opts) {
    var box = document.createElement('div');
    box.className = 'gc-panel no-print';
    var kinds = ['assignment', 'material', 'question', 'announcement'];
    var radios = kinds.map(function (k) {
      return '<label><input type="radio" name="' + opts.name + '" value="' + k + '"' + (k === opts.itemtype ? ' checked' : '') + '> ' + L[k] + '</label>';
    }).join(' ');
    var studentHref = opts.studentHref || (location.pathname + '?view=student' + (opts.hash || ''));
    box.innerHTML = '<p class="gc-h">' + L.h + '</p><fieldset><legend>' + L.type + '</legend>' + radios + '</fieldset>'
      + '<p><button type="button" class="gc-show">' + L.show + '</button> <a class="gc-fallback" href="' + shareUrl(opts.url) + '" rel="noopener">' + L.noscript + '</a></p>'
      + '<div class="gc-official" hidden></div>'
      + '<p class="gc-copy" hidden>' + L.copy + '</p>'
      + '<p class="gc-actions"><a class="gc-student" href="' + studentHref + '">' + L.student + '</a>'
      + (opts.answerKey ? ' <button type="button" class="gc-print">' + L.print + '</button>' : '') + '</p>'
      + '<p class="gc-later">' + L.later + '</p>';
    box.querySelector('.gc-show').addEventListener('click', function () {
      var kind = (box.querySelector('input:checked') || {}).value || opts.itemtype;
      opts.itemtype = kind;
      box.querySelector('.gc-official').hidden = false;
      box.querySelector('.gc-copy').hidden = kind !== 'assignment';
      renderButton(box, opts);
    });
    box.addEventListener('change', function (e) {
      if (e.target.name !== opts.name) return;
      opts.itemtype = e.target.value;
      box.querySelector('.gc-copy').hidden = opts.itemtype !== 'assignment';
      if (!box.querySelector('.gc-official').hidden) renderButton(box, opts);
    });
    var print = box.querySelector('.gc-print');
    if (print) print.addEventListener('click', function () {
      document.querySelectorAll('details').forEach(function (d) { d.open = true; });
      document.body.classList.add('answer-key');
      window.print();
    });
    return box;
  }
  var n = 0;
  function mount(el, opts) {
    if (!el || el.querySelector('.gc-panel')) return;
    opts.name = 'gc' + (++n);
    opts.itemtype = opts.itemtype || 'assignment';
    el.appendChild(panel(opts));
  }
  document.querySelectorAll('.gc-slot').forEach(function (slot) {
    mount(slot, {
      url: slot.getAttribute('data-gc-url'),
      title: slot.getAttribute('data-gc-title') || document.title,
      body: slot.getAttribute('data-gc-body') || '',
      itemtype: slot.getAttribute('data-gc-type') || 'assignment',
      hash: (slot.getAttribute('data-gc-url') || '').indexOf('#') >= 0 ? '#' + slot.getAttribute('data-gc-url').split('#')[1] : '',
      answerKey: !!document.querySelector('.crs'),
      studentHref: location.pathname + '?view=student' + ((slot.getAttribute('data-gc-url') || '').indexOf('#') >= 0 ? '#' + slot.getAttribute('data-gc-url').split('#')[1] : '')
    });
  });
  document.querySelectorAll('.teacher-box').forEach(function (box) {
    var h1 = document.querySelector('h1');
    var title = h1 ? h1.textContent.trim() : document.title;
    mount(box.querySelector('.teacher-actions') || box, {
      url: pageUrl('#teachers'), title: title, hash: '#teachers', itemtype: 'assignment', answerKey: false,
      body: title
    });
  });
  var myths = document.querySelector('section.myths');
  if (myths && !document.querySelector('.gc-slot')) {
    var bar = document.querySelector('.dt-bar') || myths;
    var h = document.querySelector('h1');
    mount(bar, { url: pageUrl(''), title: h ? h.textContent.trim() : document.title, itemtype: 'question', answerKey: true, body: h ? h.textContent.trim() : '' });
  }
  if (new URLSearchParams(location.search).get('view') === 'student') {
    document.documentElement.classList.add('student-view');
    var back = document.createElement('p');
    back.className = 'gc-student-banner no-print';
    var plain = location.pathname + location.hash;
    back.innerHTML = '<a href="' + plain + '">' + L.teacher + '</a>';
    var main = document.getElementById('main') || document.body;
    main.insertBefore(back, main.firstChild);
  }
  window.spClassroom = { mount: mount, shareUrl: shareUrl };
})();
