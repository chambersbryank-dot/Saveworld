#!/usr/bin/env python3
"""Oct 24 2026 (founder): free self-study Courses section. Data-driven: every scripts/courses/<id>.py with PAGE + STATUS='live'
becomes one course page; scripts/courses/roadmap.py is the 4-year track on Courses.html. Phase 1 = English only.
Also: anim-banners.json entries (multi-photo banner from each module's BANNER/CREDITS), assets/courses.css + assets/courses.js.
  python3 scripts/build-courses.py           build
  python3 scripts/build-courses.py --check   arithmetic checks (module CHECKS) + every external link must load
Course module fields: see scripts/courses/chem110.py (the template). Optional: LAB_NAME (lab heading), REF_TITLE/REF_INTRO (the reference-links section; default Periodic table). Oct 24: phys110.py = course 2. Idempotent."""
import os, sys, re, json, glob, html, importlib, subprocess, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT); sys.path.insert(0, 'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py'); BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
from courses import roadmap as RM
V = '20261024g'
esc = lambda s: html.escape(s, quote=True)
HUB = 'Courses.html'
MODS = []
for f in sorted(glob.glob('scripts/courses/*.py')):
    n = os.path.basename(f)[:-3]
    if n in ('__init__', 'roadmap'): continue
    m = importlib.import_module('courses.' + n)
    if getattr(m, 'STATUS', '') == 'live': MODS.append(m)
LIVE = {m.ID: m for m in MODS}

def katex(texs):
    texs = list(dict.fromkeys(texs))
    out = json.loads(subprocess.run(['node', 'scripts/katex-render.cjs'], input=json.dumps(texs), capture_output=True, text=True, check=True).stdout)
    return dict(zip(texs, out))

def ext(label, url): return f'<a href="{esc(url)}" rel="noopener">{esc(label)}</a>'
def top(): return '<p class="crs-top"><a href="#top"><span aria-hidden="true">&#8593;</span> Back to top</a></p>'
def ul(items, cls=''): return f'<ul{" class=" + chr(34) + cls + chr(34) if cls else ""}>' + ''.join(f'<li>{esc(x)}</li>' for x in items) + '</ul>'
def hero(t, k): return f'<section class="page-hero hero-learn" id="top"><div class="page-hero-content"><h1>{esc(t)}</h1><p>{esc(k)}</p></div></section>\n'
def head(): return BL.katex_head('en') + f'<link rel="stylesheet" href="assets/courses.css?v={V}">\n'
def tail(): return f'<script src="assets/courses.js?v={V}" defer></script>\n'
def table(headr, rows, cap=''):
    th = ''.join(f'<th scope="col">{esc(x)}</th>' for x in headr)
    return (f'<div class="crs-tw"><table class="crs-tbl">{"<caption>" + esc(cap) + "</caption>" if cap else ""}<thead><tr>{th}</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')
def eqblock(K, tex, cap): return f'<figure class="crs-eq"><div class="crs-math">{K[tex]}</div><figcaption>{esc(cap)}</figcaption></figure>'

def unit(C, K, i, u):
    uid = u['id']; o = [f'<section class="crs-unit" id="{uid}" data-unit="{uid}" aria-labelledby="{uid}-h">',
         f'<p class="crs-kicker">Unit {i} · {esc(u["weeks"])}</p><h2 id="{uid}-h">{esc(u["title"])}</h2><p class="crs-lead">{esc(u["summary"])}</p>']
    o.append('<h3>Learning objectives</h3><p>By the end of this unit you can:</p>' + ul(u['objectives'], 'crs-obj'))
    o.append('<h3>Key concepts</h3>' + ul(u['concepts'], 'crs-key'))
    o.append('<h3>Key equations</h3>' + ''.join(eqblock(K, t, c) for t, c in u['eqs']))
    o.append('<h3>Worked examples, step by step</h3>')
    for j, w in enumerate(u['worked'], 1):
        o.append(f'<div class="crs-card crs-worked"><p class="crs-q"><strong>Example {i}.{j}</strong> {esc(w["q"])}</p>'
                 f'<details><summary>Show the steps</summary><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in w['steps']) + f'</ol><p class="crs-ans"><strong>Answer:</strong> {esc(w["a"])}</p></details></div>')
    o.append('<h3>Practice problems</h3><p>Work each on paper first, then check.</p><ol class="crs-prac">' + ''.join(
        f'<li><p>{esc(q)}</p><details><summary>Show answer</summary><p>{esc(a)}</p></details></li>' for q, a in u['practice']) + '</ol>')
    o.append('<h3>Common misconceptions</h3><ul class="crs-mis">' + ''.join(
        f'<li><p><span class="crs-x">Myth:</span> {esc(m)}</p><p><span class="crs-ok">Actually:</span> {esc(f)}</p></li>' for m, f in u['misc']) + '</ul>')
    o.append(f'<h3>Flashcards</h3><div class="crs-fc" data-fc="{uid}"><ul class="crs-fc-list">' + ''.join(
        f'<li><p class="crs-fc-f">{esc(a)}</p><p class="crs-fc-b">{esc(b)}</p></li>' for a, b in u['cards']) + '</ul></div>')
    o.append(f'<h3>Self-check quiz</h3><form class="crs-quiz" data-quiz="{uid}" onsubmit="return false"><p class="crs-qs" aria-live="polite"></p>')
    for j, q in enumerate(u['quiz']):
        nm = f'{uid}q{j}'
        o.append(f'<fieldset data-ok="{q["ok"]}"><legend>{j + 1}. {esc(q["q"])}</legend>' + ''.join(
            f'<label><input type="radio" name="{nm}" value="{k}"> {esc(x)}</label>' for k, x in enumerate(q['opts']))
            + f'<p class="crs-fb" aria-live="polite"></p><details class="crs-nojs"><summary>Show answer</summary><p>{esc(q["opts"][q["ok"]])}. {esc(q["why"])}</p></details>'
            + f'<p class="crs-why" hidden>{esc(q["why"])}</p></fieldset>')
    o.append('</form>')
    p = u['planet']
    o.append('<div class="crs-planet"><h3>How this helps save the planet</h3>' + ''.join(f'<p>{esc(t)}</p>' for t in p['text'])
             + '<p class="crs-src">On Saving Planets: ' + ' · '.join(f'<a href="{esc(h)}">{esc(t)}</a>' for t, h in p['site'])
             + '</p><p class="crs-src">Sources: ' + ' · '.join(ext(t, h) for t, h in p['src']) + '</p></div>')
    o.append('<h3>Free learning resources</h3><ul class="crs-res">' + ''.join(f'<li>{ext(t, h)}: {esc(d)}</li>' for t, h, d in u['res']) + '</ul>')
    o.append(f'<p class="crs-done"><label><input type="checkbox" data-done="{uid}"> I finished this unit</label></p>')
    o.append(top() + '</section>')
    return ''.join(o)

def lab(C, K, L):
    hd, rows = L['table']
    o = [f'<div class="crs-card crs-lab" id="{L["id"]}"><h3>{esc(L["title"])}</h3><p class="crs-kicker">{esc(L["week"])}</p><p><strong>Goal:</strong> {esc(L["goal"])}</p>',
         eqblock(K, *L['eq']), '<h4>Procedure</h4><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in L['steps']) + '</ol>',
         '<h4>Data table</h4>' + table(hd, rows) + f'<p class="crs-note">{esc(L["note"])}</p>',
         '<h4>Sample calculation</h4><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in L['calc']) + '</ol>',
         '<div class="crs-safe"><h4>Safety</h4>' + ul(L['safety']) + '</div>',
         '<h4>Home or virtual alternative</h4>' + ul(L['home']) + '<p>' + ' · '.join(ext(t, h) for t, h in L['sims']) + '</p>',
         f'<p class="crs-planet-s"><strong>Planet link:</strong> {esc(L["planet"])}' + (' ' + ' · '.join(ext(t, h) for t, h in L['planet_src']) if L['planet_src'] else '') + '</p>',
         f'<p class="crs-done"><label><input type="checkbox" data-done="{L["id"]}"> I completed this lab (wet or virtual)</label></p></div>']
    return ''.join(o)

def pdf_link(C):
    # PDF study guide on R2 (made with --pdf: every answer open, print styles). Key = courses/<PAGE stem>_Study_Guide.pdf
    MF = json.load(open('assets/data/media-manifest.json')); k = 'courses/' + C.PAGE[:-5] + '_Study_Guide.pdf'
    return f' <a class="crs-btn" href="{MF[k]["url"]}" download>Download the PDF study guide</a>' if k in MF else ''

def make_pdf(C):
    out = '/tmp/' + C.PAGE[:-5] + '_Study_Guide.pdf'; tmp = '_pdf_' + C.PAGE
    open(tmp, 'w', encoding='utf8').write(open(C.PAGE, encoding='utf8').read().replace('<details', '<details open'))
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8799'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        import time; time.sleep(1)
        subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=8000',
                        f'--print-to-pdf={out}', f'http://localhost:8799/{tmp}'], check=True, capture_output=True)
    finally:
        srv.kill(); os.remove(tmp)
    return out

def course_page(C):
    texs = [t for u in C.UNITS for t, _ in u['eqs']] + [L['eq'][0] for L in C.LABS] + C.FORMULAS
    K = katex(texs)
    toc = [('about', 'About this course'), ('start', 'Before you start'), ('schedule', '15-week schedule'), ('progress', 'Your progress')] + \
          [(u['id'], f'Unit {i}: {u["title"]}') for i, u in enumerate(C.UNITS, 1)] + \
          [('lab', 'Lab'), ('exam', 'Exam prep'), ('formulas', 'Formula sheet'), ('ptable', getattr(C, 'REF_TITLE', 'Periodic table')), ('glossary', 'Glossary'), ('rubric', 'Self-assessment')]
    o = [hero(C.TITLE, C.TAGLINE), '<div class="crs" data-course="' + C.ID + '">',
         f'<p class="crs-crumb"><a href="{HUB}">Courses</a> › {esc(C.CODE)}</p>',
         '<div class="crs-toc" role="navigation" aria-label="On this page"><ul>' + ''.join(f'<li><a href="#{a}">{esc(b)}</a></li>' for a, b in toc) + '</ul></div>',
         '<p class="crs-tools"><button type="button" class="crs-btn" data-print>Print this page</button>' + pdf_link(C) + '</p>']
    o.append('<section id="about"><h2>About this course</h2><div class="crs-disc">' + ''.join(f'<p>{esc(x)}</p>' for x in C.ABOUT) + '</div>'
             '<div class="crs-planet"><h3>How this course helps save the planet</h3>' + ''.join(f'<p>{esc(x)}</p>' for x in C.COURSE_PLANET) + '</div>' + top() + '</section>')
    o.append('<section id="start"><h2>Before you start</h2><h3>Prerequisites</h3>' + ul(C.PREREQS) + '<h3>How to study</h3>' + ul(C.STUDY)
             + '<h3>Lab equipment (for the wet labs)</h3>' + ul(C.LAB_GEAR) + top() + '</section>')
    names = {u['id']: u['title'] for u in C.UNITS}; names['exam'] = 'Review'
    o.append('<section id="schedule"><h2>Suggested 15-week schedule</h2><p>About 6 to 9 hours a week: reading, practice problems and, in lab weeks, the lab.</p>'
             + table(['Week', 'Unit', 'Topics', 'Reading'], [[str(w), names[u], t, r] for w, u, t, r in C.SCHEDULE]) + top() + '</section>')
    o.append('<section id="progress"><h2>Your progress</h2><p>Tick units and labs as you finish them, and take the quizzes. Progress and quiz scores are saved only in this browser, never sent to us.</p>'
             '<div class="crs-prog" aria-live="polite"><progress max="100" value="0"></progress><p class="crs-prog-t">Turn on JavaScript to track progress.</p></div>'
             '<p><button type="button" class="crs-btn crs-reset" data-reset>Reset my progress</button></p>' + top() + '</section>')
    o += [unit(C, K, i, u) for i, u in enumerate(C.UNITS, 1)]
    o.append(f'<section id="lab"><h2>The lab ({esc(getattr(C, "LAB_NAME", C.CODE.split(" + ")[-1]))})</h2>' + ''.join(f'<p>{esc(x)}</p>' for x in C.LAB_INTRO)
             + f'<p class="crs-src">Safety reference: {ext(*C.SAFETY_SRC)}</p>' + ''.join(lab(C, K, L) for L in C.LABS) + top() + '</section>')
    ex = ['<section id="exam"><h2>Exam prep practice sets</h2><p>Time yourself: about 10 minutes per problem. Then compare with the full solutions.</p>']
    for t, probs in C.EXAMS:
        ex.append(f'<h3>{esc(t)}</h3><ol class="crs-prac">' + ''.join(
            f'<li><p>{esc(q)}</p><details><summary>Show full solution</summary><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in st) + f'</ol><p class="crs-ans"><strong>Answer:</strong> {esc(a)}</p></details></li>'
            for q, st, a in probs) + '</ol>')
    o.append(''.join(ex) + top() + '</section>')
    o.append('<section id="formulas"><h2>Formula sheet</h2><div class="crs-fs">' + ''.join(f'<div class="crs-math">{K[t]}</div>' for t in C.FORMULAS) + '</div>'
             '<h3>Constants</h3>' + table(['Constant', 'Value'], C.CONSTANTS) + f'<p class="crs-src">Source: {ext(*C.CONST_SRC)}</p>' + top() + '</section>')
    o.append(f'<section id="ptable"><h2>{esc(getattr(C, "REF_TITLE", "Periodic table"))}</h2><p>{esc(getattr(C, "REF_INTRO", "Use one of these free interactive tables alongside the course."))}</p><ul class="crs-res">'
             + ''.join(f'<li>{ext(t, h)}: {esc(d)}</li>' for t, h, d in C.PTABLE) + '</ul>' + top() + '</section>')
    o.append('<section id="glossary"><h2>Glossary</h2><dl class="crs-gl">' + ''.join(f'<dt>{esc(a)}</dt><dd>{esc(b)}</dd>' for a, b in C.GLOSSARY) + '</dl>' + top() + '</section>')
    o.append('<section id="rubric"><h2>Self-assessment rubric</h2><p>No grade or credit is given. Use this to judge honestly where you are in each unit.</p>'
             + table(['Level', 'What it looks like'], C.RUBRIC) + '<h3>Suggested weighting if you want a score</h3>' + table(['Part', 'Weight'], C.WEIGHTS)
             + '<p>Aim for level 3 or better in every unit before moving to the next course.</p>' + top() + '</section>')
    o.append('</div>')
    return BL.shell('en', C.PAGE, C.TITLE + ' (' + C.CODE + ')', C.DESC, ''.join(o), extra_head=head(), ld_type='Course', tail=tail())

def en_only(h):
    # Phase 1: English only, so no fr/es/ar/it/he alternates until the translated pages exist
    return re.sub(r'\n?<link rel="alternate" hreflang="(?!en"|x-default")[^"]+" href="[^"]+">', lambda m: m.group(0) if os.path.exists(m.group(0).split('savingplanets.com/')[1].split('"')[0]) else '', h)

def hub_page():
    o = [hero('Courses', 'A free four-year aerospace and STEM study track, built one course at a time.'), '<div class="crs">',
         '<div class="crs-disc"><p>These are free self-study courses written by Saving Planets. They follow the scope of first- to fourth-year college courses using open materials, but they are not university courses, carry no academic credit, and no school is involved.</p>'
         '<p>Every course ties its subject to real work that helps people and nature, and links to free, reputable resources.</p></div>',
         '<div class="crs-toc" role="navigation" aria-label="Years"><ul>' + ''.join(f'<li><a href="#y{i}">{esc(y.split(" · ")[0])}</a></li>' for i, (y, _) in enumerate(RM.YEARS, 1)) + '</ul></div>']
    for i, (y, cs) in enumerate(RM.YEARS, 1):
        o.append(f'<section id="y{i}"><h2>{esc(y)}</h2><ul class="crs-grid">')
        for cid, t, d in cs:
            m = LIVE.get(cid)
            if m: o.append(f'<li class="crs-c live"><span class="crs-badge">Live</span><h3><a href="{m.PAGE}">{esc(t)}</a></h3><p>{esc(d)}</p><p class="crs-kicker">{esc(m.CODE)}</p></li>')
            else: o.append(f'<li class="crs-c"><span class="crs-badge soon">Coming soon</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>')
        o.append('</ul>' + top() + '</section>')
    o.append('</div>')
    return BL.shell('en', HUB, 'Courses: free aerospace and STEM study track', 'Free self-study courses on Saving Planets: a four-year aerospace and STEM track with labs, quizzes and study guides. No credit, no cost.',
                    ''.join(o), extra_head=head(), ld_type='ItemList', tail='')

def banners():
    p = 'assets/data/anim-banners.json'; cfg = json.load(open(p, encoding='utf8')); MF = json.load(open('assets/data/media-manifest.json'))
    for m in MODS + [None]:
        page, keys = (m.PAGE, m.BANNER) if m else (HUB, [k for mm in MODS for k in mm.BANNER][:1] + ['images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg', 'images/Chem_GCMS_KSC-20210707-PH-FMX01_0262.jpg'])
        creds = {k: v for mm in MODS for k, v in mm.CREDITS.items()}
        for k in keys:
            assert k in MF, k
            if not any(v['r2'] == k for v in cfg['images'].values()):
                cfg['images']['r2:' + k] = {'credit': creds[k], 'pos': '50% 40%', 'r2': k}
        first = next(a for a, v in cfg['images'].items() if v['r2'] == keys[0])
        cfg['pages'][page] = first
        cfg['slides'].setdefault('curated', {})[page] = keys[1:]
    json.dump(cfg, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1); open(p, 'a').write('\n')

TL = {'en': ('Free self-study courses', 'A four-year aerospace and STEM study track with labs, quizzes and printable study guides. Start with', 'All courses'),
      'fr': ('Cours gratuits en autonomie', 'Un parcours de quatre ans en aérospatiale et STEM, avec travaux pratiques, quiz et guides imprimables. Commencez par', 'Tous les cours'),
      'es': ('Cursos gratuitos de autoestudio', 'Un itinerario de cuatro años de ingeniería aeroespacial y STEM con laboratorios, cuestionarios y guías imprimibles. Empieza con', 'Todos los cursos'),
      'ar': ('دورات مجانية للتعلّم الذاتي', 'مسار دراسي لأربع سنوات في هندسة الطيران والفضاء والعلوم والتكنولوجيا، مع مختبرات واختبارات وأدلة دراسة قابلة للطباعة. ابدأ بـ', 'كل الدورات'),
      'it': ('Corsi gratuiti di autoapprendimento', 'Un percorso di quattro anni in ingegneria aerospaziale e STEM con laboratori, quiz e guide stampabili. Inizia con', 'Tutti i corsi'),
      'he': ('קורסים חינמיים ללימוד עצמי', 'מסלול לימודים של ארבע שנים בהנדסת אווירונאוטיקה וחלל ומדעים, עם מעבדות, בחנים ומדריכי לימוד להדפסה. התחילו עם', 'כל הקורסים')}
def teachers_links():
    for l, (h, t, a) in TL.items():
        f = 'Teachers.html' if l == 'en' else f'{l}/Teachers.html'
        if not os.path.exists(f): continue
        s = open(f, encoding='utf8').read(); pre = '' if l == 'en' else '../'
        s = re.sub(r'<!-- COURSELINK:START -->[\s\S]*?<!-- COURSELINK:END -->', '', s)
        first = MODS[0]
        blk = (f'<!-- COURSELINK:START --><aside class="learn-link card-band" aria-label="{esc(h)}"><h2>{esc(h)}</h2><p>{esc(t)} '
               f'<a href="{pre}{first.PAGE}" hreflang="en">{esc(first.TITLE)}</a> (English) · <a href="{pre}{HUB}" hreflang="en">{esc(a)}</a></p></aside><!-- COURSELINK:END -->')
        if '<!-- LEARNLINK:START -->' in s: s = s.replace('<!-- LEARNLINK:START -->', blk + '<!-- LEARNLINK:START -->', 1)
        else: s = s.replace('</main>', blk + '</main>', 1)
        open(f, 'w', encoding='utf8').write(s)

def check():
    bad = []
    for m in MODS:
        for n, a, b in m.CHECKS():
            if abs(a - b) > 0.006 * abs(b): bad.append((m.ID, n, a, b))
    print('arithmetic:', 'OK' if not bad else bad)
    urls = set()
    for f in [HUB] + [m.PAGE for m in MODS]:
        urls |= set(re.findall(r'href="(https?://[^"]+)"', open(f, encoding='utf8').read()))
    fail = []
    for u in sorted(u for u in urls if 'savingplanets.com' not in u):
        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-L', '-m', '25', '-A', 'Mozilla/5.0 (X11; Linux x86_64) Chrome/120', '-w', '%{http_code}', u], capture_output=True, text=True).stdout
        if r != '200': fail.append((r, u))
    print('links:', len(urls), 'checked;', 'not 200 from this box (check by browser):', fail)
    return not bad

if __name__ == '__main__':
    if '--check' in sys.argv: sys.exit(0 if check() else 1)
    if '--pdf' in sys.argv:
        for m in MODS: print(make_pdf(m))
        sys.exit(0)
    banners()
    for m in MODS: open(m.PAGE, 'w', encoding='utf8').write(en_only(course_page(m)))
    open(HUB, 'w', encoding='utf8').write(en_only(hub_page()))
    teachers_links()
    print('build-courses:', HUB, '+', [m.PAGE for m in MODS])
