#!/usr/bin/env python3
"""Printable lesson plan: a teacher picks a grade, a subject, a length, and solution pages.

The plan is assembled from text already on those pages (Explain Like I'm 10, discussion
questions, the first cited source) and from standards already tagged in assets/data/standards.json.
Official standard statements stay in English, as on Teacher Sheets. No new facts.
Does not add Google Analytics.

Writes Lesson_Plan.html, assets/data/lesson-plan.<lang>.json, i18n strings, and a LESSONPLAN
link on Teachers.html. Idempotent. Run after build-kids-world.py."""
import html, json, os, re, importlib.util
from bs4 import BeautifulSoup

PAGE = 'Lesson_Plan.html'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
ASSETV = '20261102b'
GA = re.compile(r"\n?<!-- Google tag \(gtag\.js\) -->.*?<!-- /Google tag -->", re.S)
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)

spec = importlib.util.spec_from_file_location('st', 'scripts/build-standards.py')
st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)

GRADES = ['K-2', '3-5', '6-8', '9-12']
SUBJECTS = ['earth', 'life', 'space', 'literacy']

T = {
 'Printable Lesson Plan': ('Plan de cours imprimable', 'Plan de clase imprimible', 'خطة درس قابلة للطباعة', 'Piano di lezione stampabile', 'מערך שיעור להדפסה'),
 'Teachers pick a grade, a subject, a lesson length, and one or more Saving Planets solutions. The page assembles a printable plan from those pages: objectives from the tagged standards, an activity, the discussion questions, and an assessment.':
 ("L'enseignant choisit un niveau, une matière, une durée et une ou plusieurs solutions Saving Planets. La page assemble un plan imprimable à partir de ces pages : objectifs tirés des normes déjà indiquées, une activité, les questions de discussion et une évaluation.",
  'El docente elige un grado, una materia, una duración y una o más soluciones de Saving Planets. La página arma un plan imprimible con esas páginas: objetivos de los estándares ya marcados, una actividad, las preguntas de debate y una evaluación.',
  'يختار المعلم صفًا ومادة ومدة وحلًا أو أكثر من حلول Saving Planets. تجمع الصفحة خطة قابلة للطباعة من تلك الصفحات: أهداف من المعايير الموسومة أصلًا، ونشاط، وأسئلة نقاش، وتقويم.',
  "L'insegnante sceglie una classe, una materia, una durata e una o più soluzioni di Saving Planets. La pagina compone un piano stampabile da quelle pagine: obiettivi dagli standard già indicati, un'attività, le domande di discussione e una verifica.",
  'המורה בוחר כיתה, מקצוע, משך ופתרון אחד או יותר של Saving Planets. הדף מרכיב מערך להדפסה מהדפים האלה: מטרות מהתקנים שכבר מסומנים, פעילות, שאלות דיון והערכה.'),
 'Pick a grade, a subject, and how long the lesson is. Then tick the solutions you want. The plan uses only text already on those pages and the standards already tagged to them.':
 ('Choisissez un niveau, une matière et la durée. Cochez ensuite les solutions. Le plan n’utilise que le texte déjà présent sur ces pages et les normes déjà indiquées.',
  'Elige un grado, una materia y la duración. Luego marca las soluciones. El plan usa solo el texto que ya está en esas páginas y los estándares ya marcados.',
  'اختر الصف والمادة والمدة، ثم حدّد الحلول. لا تستخدم الخطة إلا النص الموجود أصلًا في تلك الصفحات والمعايير الموسومة بها.',
  'Scegli la classe, la materia e la durata. Poi segna le soluzioni. Il piano usa solo il testo già presente in quelle pagine e gli standard già indicati.',
  'בחרו כיתה, מקצוע ומשך. אחר כך סמנו את הפתרונות. המערך משתמש רק בטקסט שכבר נמצא בדפים האלה ובתקנים שכבר מסומנים עליהם.'),
 'Choose the solutions for this lesson':
 ('Choisissez les solutions pour ce cours', 'Elige las soluciones para esta clase', 'اختر الحلول لهذا الدرس', 'Scegli le soluzioni per questa lezione', 'בחרו את הפתרונות לשיעור הזה'),
 'No solutions on Saving Planets are tagged for this grade and subject.':
 ('Aucune solution Saving Planets n’est indiquée pour ce niveau et cette matière.',
  'Ninguna solución de Saving Planets está marcada para este grado y esta materia.',
  'لا يوجد حل على Saving Planets موسوم لهذا الصف وهذه المادة.',
  'Nessuna soluzione di Saving Planets è indicata per questa classe e questa materia.',
  'אין פתרון ב-Saving Planets שמסומן לכיתה ולמקצוע האלה.'),
 'The plan is built in your browser from the pages you pick. It is not sent to Saving Planets.':
 ('Le plan est créé dans votre navigateur à partir des pages choisies. Il n’est pas envoyé à Saving Planets.',
  'El plan se crea en tu navegador con las páginas que eliges. No se envía a Saving Planets.',
  'تُنشأ الخطة في متصفحك من الصفحات التي تختارها، ولا تُرسل إلى Saving Planets.',
  'Il piano viene creato nel tuo browser dalle pagine che scegli. Non viene inviato a Saving Planets.',
  'המערך נוצר בדפדפן מהדפים שבחרתם. הוא לא נשלח אל Saving Planets.'),
 'This builder needs JavaScript. You can still open Teacher Sheets and print any solution page.':
 ('Ce générateur a besoin de JavaScript. Vous pouvez quand même ouvrir les fiches enseignants et imprimer chaque page de solution.',
  'Este creador necesita JavaScript. Aun así puedes abrir las fichas para docentes e imprimir cualquier página de solución.',
  'يحتاج هذا المنشئ إلى جافاسكربت. ما زال بإمكانك فتح أوراق المعلمين وطباعة أي صفحة حل.',
  'Questo strumento ha bisogno di JavaScript. Puoi comunque aprire le schede per insegnanti e stampare qualsiasi pagina di soluzione.',
  'הכלי הזה צריך JavaScript. עדיין אפשר לפתוח את דפי המורים ולהדפיס כל דף פתרון.'),
}
UI = {
 'en': dict(title='Lesson plan', minutes='{n} minutes', solutions='Solutions', objectives='Objectives', standards='Standards note', activity='Activity', questions='Discussion questions', assessment='Assessment', sources='Sources',
   stdNote='U.S. Next Generation Science Standards (NGSS) and Common Core. Official text, in English.',
   noObj='None of the standards tagged on these pages match both the grade and the subject you picked.',
   timing='Suggested timing for the length you chose. These three parts add up to that length. This is not a researched schedule.',
   read='Read the pages ({n} minutes). The first Explain Like I\'m 10 line from each page is below.',
   talk='Discussion questions ({n} minutes). Use the questions copied from each page.',
   write='Assessment ({n} minutes).',
   assessText='Students answer one discussion question in writing and name the source printed on the solution page next to the fact they use.',
   pick='Tick at least one solution, then build the plan again.'),
 'fr': dict(title='Plan de cours', minutes='{n} minutes', solutions='Solutions', objectives='Objectifs', standards='Note sur les normes', activity='Activité', questions='Questions de discussion', assessment='Évaluation', sources='Sources',
   stdNote='Normes américaines NGSS (Next Generation Science Standards) et Common Core. Texte officiel, en anglais.',
   noObj='Aucune norme indiquée sur ces pages ne correspond à la fois au niveau et à la matière choisis.',
   timing='Découpage suggéré pour la durée choisie. Ces trois parties additionnées donnent cette durée. Ce n’est pas un horaire issu d’une recherche.',
   read='Lire les pages ({n} minutes). La première ligne « Explique-moi comme si j\'avais 10 ans » de chaque page est ci-dessous.',
   talk='Questions de discussion ({n} minutes). Utilisez les questions copiées depuis chaque page.',
   write='Évaluation ({n} minutes).',
   assessText='Les élèves répondent par écrit à une question de discussion et nomment la source imprimée sur la page de la solution, à côté du fait qu’ils utilisent.',
   pick='Cochez au moins une solution, puis créez à nouveau le plan.'),
 'es': dict(title='Plan de clase', minutes='{n} minutos', solutions='Soluciones', objectives='Objetivos', standards='Nota sobre los estándares', activity='Actividad', questions='Preguntas para debatir', assessment='Evaluación', sources='Fuentes',
   stdNote='Estándares de EE. UU.: Next Generation Science Standards (NGSS) y Common Core. Texto oficial, en inglés.',
   noObj='Ningún estándar marcado en estas páginas coincide a la vez con el grado y la materia elegidos.',
   timing='Tiempo sugerido para la duración que elegiste. Estas tres partes suman esa duración. No es un horario investigado.',
   read='Leer las páginas ({n} minutos). Abajo está la primera línea de «Explícamelo como si tuviera 10 años» de cada página.',
   talk='Preguntas para debatir ({n} minutos). Usa las preguntas copiadas de cada página.',
   write='Evaluación ({n} minutos).',
   assessText='El alumnado responde por escrito una pregunta de debate y nombra la fuente impresa en la página de la solución, junto al dato que usa.',
   pick='Marca al menos una solución y vuelve a crear el plan.'),
 'ar': dict(title='خطة الدرس', minutes='{n} دقيقة', solutions='الحلول', objectives='الأهداف', standards='ملاحظة عن المعايير', activity='النشاط', questions='أسئلة النقاش', assessment='التقويم', sources='المصادر',
   stdNote='معايير أمريكية: معايير العلوم للجيل القادم (NGSS) وCommon Core. النص الرسمي باللغة الإنجليزية.',
   noObj='لا يوجد معيار موسوم على هذه الصفحات يطابق الصف والمادة اللذين اخترتهما معًا.',
   timing='توقيت مقترح للمدة التي اخترتها. هذه الأجزاء الثلاثة تساوي تلك المدة. ليس جدولًا ناتجًا عن بحث.',
   read='اقرأ الصفحات ({n} دقيقة). السطر الأول من «اشرحها لي كأن عمري 10 سنوات» في كل صفحة موجود أدناه.',
   talk='أسئلة النقاش ({n} دقيقة). استخدم الأسئلة المنسوخة من كل صفحة.',
   write='التقويم ({n} دقيقة).',
   assessText='يجيب الطلاب كتابة عن سؤال نقاش واحد ويذكرون المصدر المطبوع في صفحة الحل بجانب الحقيقة التي يستخدمونها.',
   pick='حدّد حلًا واحدًا على الأقل ثم أنشئ الخطة من جديد.'),
 'it': dict(title='Piano di lezione', minutes='{n} minuti', solutions='Soluzioni', objectives='Obiettivi', standards='Nota sugli standard', activity='Attività', questions='Domande per la discussione', assessment='Verifica', sources='Fonti',
   stdNote='Standard statunitensi: Next Generation Science Standards (NGSS) e Common Core. Testo ufficiale, in inglese.',
   noObj='Nessuno standard indicato in queste pagine corrisponde sia alla classe sia alla materia scelte.',
   timing='Tempi suggeriti per la durata che hai scelto. Queste tre parti sommate danno quella durata. Non è una scansione ricavata da una ricerca.',
   read='Leggi le pagine ({n} minuti). Sotto c’è la prima riga di «Spiegamelo come se avessi 10 anni» di ogni pagina.',
   talk='Domande per la discussione ({n} minuti). Usa le domande copiate da ogni pagina.',
   write='Verifica ({n} minuti).',
   assessText='Gli studenti rispondono per iscritto a una domanda di discussione e nominano la fonte stampata nella pagina della soluzione, accanto al fatto che usano.',
   pick='Segna almeno una soluzione, poi crea di nuovo il piano.'),
 'he': dict(title='מערך שיעור', minutes='{n} דקות', solutions='פתרונות', objectives='מטרות', standards='הערת תקנים', activity='פעילות', questions='שאלות לדיון', assessment='הערכה', sources='מקורות',
   stdNote='תקני ארה״ב: Next Generation Science Standards (NGSS) ו-Common Core. הטקסט הרשמי באנגלית.',
   noObj='אף תקן שמסומן בדפים האלה לא תואם גם את הכיתה וגם את המקצוע שבחרתם.',
   timing='חלוקת זמן מוצעת למשך שבחרתם. שלושת החלקים יחד שווים למשך הזה. זה אינו לוח זמנים מבוסס מחקר.',
   read='קריאת הדפים ({n} דקות). השורה הראשונה של «הסבירו לי כאילו אני בן 10» מכל דף מופיעה למטה.',
   talk='שאלות לדיון ({n} דקות). השתמשו בשאלות שהועתקו מכל דף.',
   write='הערכה ({n} דקות).',
   assessText='התלמידים עונים בכתב על שאלת דיון אחת ומציינים את המקור המודפס בדף הפתרון ליד העובדה שהם משתמשים בה.',
   pick='סמנו לפחות פתרון אחד, ואז בנו את המערך שוב.'),
}
SUBJ = {l: st.U[l]['subj'] for l in LANGS}
LINK = {
 'en': 'Printable Lesson Plan: pick a grade, a subject, a time, and solutions. The page builds a plan you can print.',
 'fr': 'Plan de cours imprimable : choisissez un niveau, une matière, une durée et des solutions. La page prépare un plan à imprimer.',
 'es': 'Plan de clase imprimible: elige un grado, una materia, un tiempo y soluciones. La página prepara un plan para imprimir.',
 'ar': 'خطة درس قابلة للطباعة: اختر صفًا ومادة ووقتًا وحلولًا. تُجهّز الصفحة خطة يمكن طباعتها.',
 'it': 'Piano di lezione stampabile: scegli classe, materia, tempo e soluzioni. La pagina prepara un piano da stampare.',
 'he': 'מערך שיעור להדפסה: בחרו כיתה, מקצוע, זמן ופתרונות. הדף מרכיב מערך שאפשר להדפיס.',
}

def plain_li(li):
    for pop in li.select('.gl-pop'): pop.decompose()
    for b in li.select('button'): b.replace_with(b.get_text())
    return re.sub(r'\s+', ' ', li.get_text(' ', strip=True))

def page_bits(lang, page):
    path = page if lang == 'en' else f'{lang}/{page}'
    if not os.path.exists(path): path = page
    soup = BeautifulSoup(rd(path), 'html.parser')
    h = soup.select_one('h1')
    name = re.sub(r'\s+', ' ', h.get_text(' ', strip=True)) if h else page
    eli = []
    sec = soup.select_one('#eli10')
    if sec:
        for li in sec.select('li')[:1]:
            t = plain_li(li)
            if t: eli.append(t)
    qs = []
    box = soup.select_one('#teachers')
    if box:
        for li in box.select('ol li')[:3]:
            t = plain_li(li)
            if t: qs.append(t)
    a = soup.select_one('p.fact-source a[href]')
    src = None
    if a and a['href'].startswith('http'):
        src = {'href': a['href'], 'name': re.sub(r'\s+', ' ', a.get_text(' ', strip=True))}
    return name, eli, qs, src

def collect(lang):
    sols = []
    for page in sorted(st.PH):
        codes = st.codes_for(page)
        if not codes or not os.path.exists(page): continue
        info = []
        grades, subjects = [], []
        for c in codes:
            meta = st.D['codes'].get(c)
            if not meta: continue
            info.append({'code': c, 'band': meta['band'], 'subject': meta['subject'], 'url': meta['url'], 'text': meta['text']})
            if meta['band'] not in grades: grades.append(meta['band'])
            if meta['subject'] not in subjects: subjects.append(meta['subject'])
        if not info: continue
        name, eli, qs, src = page_bits(lang, page)
        sols.append({'u': page, 'n': name, 'grades': grades, 'subjects': subjects, 'standards': info, 'eli': eli, 'questions': qs, 'src': src})
    sols.sort(key=lambda x: x['n'].casefold())
    return {'ui': UI[lang], 'subjects': SUBJ[lang], 'solutions': sols}

DESC = "Teachers pick a grade, a subject, a lesson length, and one or more Saving Planets solutions. The page assembles a printable plan from those pages: objectives from the tagged standards, an activity, the discussion questions, and an assessment."
# Meta only. The visible hero stays DESC. This stays inside the 120-155 description window so seo-fix does not pad it.
META = "Teachers pick a grade, subject, lesson length, and solutions. The printable plan has objectives, an activity, discussion questions, and an assessment."
LEAD = "Pick a grade, a subject, and how long the lesson is. Then tick the solutions you want. The plan uses only text already on those pages and the standards already tagged to them."
OPTS_G = ''.join(f'<option value="{g}">{g}</option>' for g in GRADES)
OPTS_S = ''.join(f'<option value="{s}">{esc(SUBJ["en"][s])}</option>' for s in SUBJECTS)
OPTS_M = ''.join(f'<option value="{n}">{n} minutes</option>' for n in (30, 45, 60, 90))
MAIN = f'''<section class="page-hero hero-teach"><div class="page-hero-content"><h1>Printable Lesson Plan</h1><p>{esc(DESC)}</p></div></section>
<div class="lp-wrap" id="lp">
<p class="lp-lead">{esc(LEAD)}</p>
<form id="lp-form" class="lp-form">
<div class="lp-field"><label for="lp-grade">Grade</label><select id="lp-grade" name="grade">{OPTS_G}</select></div>
<div class="lp-field"><label for="lp-subject">Subject</label><select id="lp-subject" name="subject">{OPTS_S}</select></div>
<div class="lp-field"><label for="lp-min">Lesson length</label><select id="lp-min" name="minutes">{OPTS_M}</select></div>
<fieldset class="lp-field"><legend>Choose the solutions for this lesson</legend>
<div class="lp-sols" id="lp-sols"></div>
<p id="lp-none" hidden>No solutions on Saving Planets are tagged for this grade and subject.</p>
</fieldset>
<div class="lp-actions"><button type="submit">Build my lesson plan</button>
<button type="button" id="lp-print" hidden>Print plan</button></div>
</form>
<p class="lp-note">The plan is built in your browser from the pages you pick. It is not sent to Saving Planets.</p>
<article class="lp-plan" id="lp-plan" aria-live="polite" hidden></article>
<template class="lp-error-tpl"><p role="alert">Sorry, the lesson builder could not load. Please refresh the page.</p></template>
<noscript><p>This builder needs JavaScript. You can still open <a href="Teachers.html">Teacher Sheets</a> and print any solution page.</p></noscript>
</div>
'''

def shell():
    s = rd('Teachers.html')
    s = re.sub(r'<main id="main">.*?</main>', '<main id="main">\n' + MAIN + '\n</main>', s, count=1, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>Printable Lesson Plan | Saving Planets</title>', s, count=1, flags=re.S)
    desc = esc(META)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {attr} content=")[^"]*"', lambda m: m.group(1) + desc + '"', s, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {attr} content=")[^"]*"', r'\1Printable Lesson Plan | Saving Planets"', s, count=1)
    s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', r'\1Printable Lesson Plan"', s, count=1)
    old = "A printable one-page sheet for every Saving Planets solution: the Five W's, a kid-friendly summary, sources and three discussion questions."
    s = s.replace(old, DESC)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: m.group(0).replace('Teacher Sheets', 'Printable Lesson Plan'), s, flags=re.S)
    for folder in ('', 'fr/', 'es/', 'ar/', 'it/', 'he/'):
        s = s.replace(f'https://www.savingplanets.com/{folder}Teachers.html', f'https://www.savingplanets.com/{folder}{PAGE}')
        if folder:
            s = s.replace(f'href="{folder}Teachers.html"', f'href="{folder}{PAGE}"')
    s = s.replace('href="Teachers.html" hreflang="en"', f'href="{PAGE}" hreflang="en"')
    s = s.replace(' aria-current="page"', '')
    s = s.replace('teachers-page', 'lesson-plan-page')
    s = GA.sub('', s)
    if 'lesson-plan.css' not in s:
        s = s.replace('</head>', f'<link rel="stylesheet" href="lesson-plan.css?v={ASSETV}">\n</head>', 1)
    if 'lesson-plan.js' not in s:
        s = s.replace('</body>', f'<script src="lesson-plan.js?v={ASSETV}" defer></script>\n</body>', 1)
    if 'gtag' in s or 'googletagmanager' in s:
        raise SystemExit('lesson plan: refused to keep a Google Analytics tag')
    return s

def merge_i18n():
    order = ['fr', 'es', 'ar', 'it', 'he']
    for i, lang in enumerate(order):
        p = f'i18n/{lang}.json'
        m = json.load(open(p, encoding='utf8'))
        n0 = json.dumps(m, ensure_ascii=False)
        for k, vals in T.items():
            if i < len(vals): m[k] = vals[i]
        # subject labels used as option text
        for key, en in SUBJ['en'].items():
            m.setdefault(en, SUBJ[lang][key])
        if json.dumps(m, ensure_ascii=False) != n0:
            json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
            open(p, 'a', encoding='utf8').write('\n')

def ensure_lists():
    pl = rd('i18n/pages.txt')
    if PAGE not in pl.split():
        open('i18n/pages.txt', 'w', encoding='utf8').write(pl.rstrip('\n') + '\n' + PAGE + '\n')
    hp = rd('i18n/he-pages.txt')
    if PAGE not in [ln.strip() for ln in hp.splitlines()]:
        open('i18n/he-pages.txt', 'w', encoding='utf8').write(hp.rstrip('\n') + '\n' + PAGE + '\n')

def translate():
    import sys
    sys.path.insert(0, 'scripts')
    import langs as L
    spec = importlib.util.spec_from_file_location('i18nb', 'scripts/i18n-build.py')
    I = importlib.util.module_from_spec(spec); spec.loader.exec_module(I)
    I.english_head(PAGE)
    for lang in I.LANGS:
        m = json.load(open(f'i18n/{lang}.json', encoding='utf8'))
        I.CUR_PAGES = L.pages_for(lang, I.PAGES)
        if PAGE in I.CUR_PAGES: I.build(PAGE, lang, m)
    I.CUR_PAGES = None

def links():
    n = 0
    for lang in LANGS:
        pre = '' if lang == 'en' else lang + '/'
        path = pre + 'Teachers.html'
        if not os.path.exists(path): continue
        name, rest = LINK[lang].split(': ', 1)
        css = ('../' if lang != 'en' else '') + f'lesson-plan.css?v={ASSETV}'
        block = ('<!-- LESSONPLAN:START --><link rel="stylesheet" href="' + css + '">'
                 f'<p class="lp-teach"><a href="Lesson_Plan.html">{esc(name)}</a>: {esc(rest)}</p><!-- LESSONPLAN:END -->')
        s = re.sub(r'<!-- LESSONPLAN:START -->.*?<!-- LESSONPLAN:END -->', '', rd(path), flags=re.S)
        s = re.sub(r'\n?<link rel="stylesheet" href="(?:\.\./)?lesson-plan\.css\?v=[^"]+">', '', s)
        anchor = '<!-- KIDSWORLD:START -->' if '<!-- KIDSWORLD:START -->' in s else ('<!-- EDU-LINKS:END -->' if '<!-- EDU-LINKS:END -->' in s else '</main>')
        s = s.replace(anchor, block + anchor, 1)
        n += wr(path, s)
    return n

def sitemap():
    import sitemap_pages
    if sitemap_pages.english_has(PAGE): return
    import subprocess
    subprocess.check_call(['python3', 'scripts/i18n-sitemap.py'])

def main():
    merge_i18n(); ensure_lists()
    os.makedirs('assets/data', exist_ok=True)
    en = collect('en')
    json.dump(en, open('assets/data/lesson-plan.en.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    open('assets/data/lesson-plan.en.json', 'a', encoding='utf8').write('\n')
    for lang in LANGS:
        if lang == 'en': continue
        data = collect(lang)
        json.dump(data, open(f'assets/data/lesson-plan.{lang}.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
        open(f'assets/data/lesson-plan.{lang}.json', 'a', encoding='utf8').write('\n')
    wr(PAGE, shell())
    translate()
    k = links()
    sitemap()
    print('lesson-plan:', len(en['solutions']), 'solutions; link writes', k)

if __name__ == '__main__':
    main()
