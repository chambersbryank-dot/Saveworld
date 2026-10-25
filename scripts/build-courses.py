#!/usr/bin/env python3
"""Oct 24 2026 (founder): free self-study Courses section. Data-driven: every scripts/courses/<id>.py with PAGE + STATUS='live'
becomes one course page; scripts/courses/roadmap.py is the 4-year track on Courses.html. Phase 1 = English only.
Also: anim-banners.json entries (multi-photo banner from each module's BANNER/CREDITS), assets/courses.css + assets/courses.js.
  python3 scripts/build-courses.py           build
  python3 scripts/build-courses.py --check   arithmetic checks (module CHECKS) + every external link must load
Course module fields: see scripts/courses/chem110.py (the template). Optional: LAB_NAME (lab heading) or LAB_TITLE (whole heading), REF_TITLE/REF_INTRO (the reference-links section; default Periodic table). Oct 24: phys110.py = course 2. Idempotent."""
import os, sys, re, json, glob, html, importlib, subprocess, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT); sys.path.insert(0, 'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py'); BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
from courses import roadmap as RM
V = '20261024h'  # > main's 20261024g (courses.css/js changed)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
BUILD_LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']  # languages built and published so far (step 2: all six for hub + chem110). Add one at a time once i18n/courses/*.json has it.
RTL = {'ar', 'he'}  # right-to-left languages: the course wrapper gets dir="rtl"; equations/KaTeX stay LTR (assets/courses.css)
def dir_attr(): return ' dir="rtl"' if LANG in RTL else ''
# Phase 2 (Oct 24): every page is built per language from the same English data. Translations: i18n/courses/_shared.json (hub, roadmap,
# section headings, quiz UI) + i18n/courses/<course ID>.json (that course's text), each {English: {fr, es, ar, it, he}}. A course is built in a
# language only when every one of its strings is translated there (no half-English pages); otherwise that language links the English page
# and the build prints what is missing. New course: add scripts/courses/<id>.py, build (English goes live), then
#   python3 scripts/build-courses.py --missing <ID>   -> /tmp/courses-missing-<ID>.tsv (English + one column per language) to translate
#   python3 scripts/build-courses.py --import <file.tsv> <ID>   -> merges into i18n/courses/<ID>.json (checks numbers + {placeholders})
TR = {}
for _f in sorted(glob.glob('i18n/courses/*.json')):
    for _k, _v in json.load(open(_f, encoding='utf8')).items(): TR.setdefault(_k, {}).update(_v)
LANG = 'en'; MISSING = {}
def _(s):
    if LANG == 'en' or not isinstance(s, str): return s
    t = TR.get(s, {}).get(LANG)
    if t is None:
        if needs_tr(s): MISSING.setdefault(s, None)
        return s
    return t
esc = lambda s: html.escape(_(s), quote=True)
UNITS_RX = r'\b(?:atm|mol|g|L|K|mL|nm|kPa|mmHg|kJ|J|u|M|s|m|cm|mg|kg|Hz|µM|mol⁻¹|M⁻¹|cm⁻¹)\b'
_SHORTW = re.compile(r'(?<![\w^_′])(so|to|of|in|is|or|if|by|as|at|an|on|up|no)(?![\w(′])')
def needs_tr(s):  # words to translate (not a URL, a site page name, or numbers + units). Oct 25: a formula sentence with a short English word ("…, so a = 2") counts too
    if isinstance(s, str) and not re.match(r'(https?:|mailto:|#)', s) and _SHORTW.search(s): return True
    return bool(re.search('[a-z]{3}', s)) and not re.match(r'(https?:|mailto:|#)', s) and not re.fullmatch(r'(\.\./)?[\w-]+\.html(#[\w-]+)?', s) and not same(s)
def same(s):  # numbers + SI units only (e.g. "0.500 mol", "8.314 J/(mol·K)"): identical in every language
    return not re.search('[A-Za-zÀ-ÿ]{2,}', re.sub(UNITS_RX, '', s))
def pre(): return '' if LANG == 'en' else '../'
def loc(p):  # site page link from a course page: stay in the language folder when that page exists there
    if LANG == 'en' or re.match(r'(https?:|mailto:|#)', p): return p
    return p if os.path.exists(LANG + '/' + p.split('#')[0]) or p.split('#')[0] in (HUB,) + tuple(m.PAGE for m in MODS if LANG in DONE.get(m.ID, ())) else '../' + p
def out(p): return p if LANG == 'en' else LANG + '/' + p
HUB = 'Courses.html'
MODS = []
for f in sorted(glob.glob('scripts/courses/*.py')):
    n = os.path.basename(f)[:-3]
    if n in ('__init__', 'roadmap'): continue
    m = importlib.import_module('courses.' + n)
    if getattr(m, 'STATUS', '') == 'live': MODS.append(m)
LIVE = {m.ID: m for m in MODS}
DONE = {}  # course ID -> languages it is fully translated (and built) in

def katex(texs):
    texs = list(dict.fromkeys(texs))
    out = json.loads(subprocess.run(['node', 'scripts/katex-render.cjs'], input=json.dumps(texs), capture_output=True, text=True, check=True).stdout)
    return dict(zip(texs, out))

def ext(label, url): return f'<a href="{esc(url)}" rel="noopener">{esc(label)}</a>'
def top(): return f'<p class="crs-top"><a href="#top"><span aria-hidden="true">&#8593;</span> {esc("Back to top")}</a></p>'
def ul(items, cls=''): return f'<ul{" class=" + chr(34) + cls + chr(34) if cls else ""}>' + ''.join(f'<li>{esc(x)}</li>' for x in items) + '</ul>'
def hero(t, k): return f'<section class="page-hero hero-learn" id="top"><div class="page-hero-content"><h1>{esc(t)}</h1><p>{esc(k)}</p></div></section>\n'
def head(): return BL.katex_head(LANG) + f'<link rel="stylesheet" href="{pre()}assets/courses.css?v={V}">\n'
def tail(): return f'<script src="{pre()}assets/courses.js?v={V}" defer></script>\n'
def table(headr, rows, cap=''):
    th = ''.join(f'<th scope="col">{esc(x)}</th>' for x in headr)
    return (f'<div class="crs-tw"><table class="crs-tbl">{"<caption>" + esc(cap) + "</caption>" if cap else ""}<thead><tr>{th}</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')
def eqblock(K, tex, cap): return f'<figure class="crs-eq"><div class="crs-math">{K[tex]}</div><figcaption>{esc(cap)}</figcaption></figure>'

def _code(src, out=None):
    """Optional code listing (+ verified output) for programming courses; code is never translated. Inline style so courses.css/V need no change."""
    st = 'style="direction:ltr;text-align:left;overflow-x:auto;padding:.75em;border-radius:6px;background:rgba(127,127,127,.12);font-size:.9em"'
    r = f'<pre class="crs-code" dir="ltr" {st}><code>{html.escape(src)}</code></pre>' if src else ''
    if out is not None: r += f'<p><strong>{esc("Output")}</strong></p><pre class="crs-out" dir="ltr" {st}><code>{html.escape(out)}</code></pre>'
    return r

def unit(C, K, i, u):
    uid = u['id']; o = [f'<section class="crs-unit" id="{uid}" data-unit="{uid}" aria-labelledby="{uid}-h">',
         f'<p class="crs-kicker">{esc("Unit {n}").replace("{n}", str(i))} · {esc(u["weeks"])}</p><h2 id="{uid}-h">{esc(u["title"])}</h2><p class="crs-lead">{esc(u["summary"])}</p>']
    o.append(f'<h3>{esc("Learning objectives")}</h3><p>{esc("By the end of this unit you can:")}</p>' + ul(u['objectives'], 'crs-obj'))
    o.append(f'<h3>{esc("Key concepts")}</h3>' + ul(u['concepts'], 'crs-key'))
    o.append(f'<h3>{esc("Key equations")}</h3>' + ''.join(eqblock(K, t, c) for t, c in u['eqs']))
    o.append(f'<h3>{esc("Worked examples, step by step")}</h3>')
    for j, w in enumerate(u['worked'], 1):
        o.append(f'<div class="crs-card crs-worked"><p class="crs-q"><strong>{esc("Example {n}").replace("{n}", f"{i}.{j}")}</strong> {esc(w["q"])}</p>' + _code(w.get('code')) +
                 f'<details><summary>{esc("Show the steps")}</summary><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in w['steps']) + '</ol>' + _code(None, w.get('out')) + f'<p class="crs-ans"><strong>{esc("Answer:")}</strong> {esc(w["a"])}</p></details></div>')
    o.append(f'<h3>{esc("Practice problems")}</h3><p>{esc("Work each on paper first, then check.")}</p><ol class="crs-prac">' + ''.join(
        f'<li><p>{esc(q)}</p><details><summary>{esc("Show answer")}</summary><p>{esc(a)}</p></details></li>' for q, a in u['practice']) + '</ol>')
    o.append(f'<h3>{esc("Common misconceptions")}</h3><ul class="crs-mis">' + ''.join(
        f'<li><p><span class="crs-x">{esc("Myth:")}</span> {esc(m)}</p><p><span class="crs-ok">{esc("Actually:")}</span> {esc(f)}</p></li>' for m, f in u['misc']) + '</ul>')
    o.append(f'<h3>{esc("Flashcards")}</h3><div class="crs-fc" data-fc="{uid}"><ul class="crs-fc-list">' + ''.join(
        f'<li><p class="crs-fc-f">{esc(a)}</p><p class="crs-fc-b">{esc(b)}</p></li>' for a, b in u['cards']) + '</ul></div>')
    o.append(f'<h3>{esc("Self-check quiz")}</h3><form class="crs-quiz" data-quiz="{uid}" onsubmit="return false"><p class="crs-qs" aria-live="polite"></p>')
    for j, q in enumerate(u['quiz']):
        nm = f'{uid}q{j}'
        o.append(f'<fieldset data-ok="{q["ok"]}"><legend>{j + 1}. {esc(q["q"])}</legend>' + ''.join(
            f'<label><input type="radio" name="{nm}" value="{k}"> {esc(x)}</label>' for k, x in enumerate(q['opts']))
            + f'<p class="crs-fb" aria-live="polite"></p><details class="crs-nojs"><summary>{esc("Show answer")}</summary><p>{esc(q["opts"][q["ok"]])}. {esc(q["why"])}</p></details>'
            + f'<p class="crs-why" hidden>{esc(q["why"])}</p></fieldset>')
    o.append('</form>')
    p = u['planet']
    o.append(f'<div class="crs-planet"><h3>{esc("How this helps save the planet")}</h3>' + ''.join(f'<p>{esc(t)}</p>' for t in p['text'])
             + f'<p class="crs-src">{esc("On Saving Planets:")} ' + ' · '.join(f'<a href="{esc(loc(h))}">{esc(t)}</a>' for t, h in p['site'])
             + f'</p><p class="crs-src">{esc("Sources:")} ' + ' · '.join(ext(t, h) for t, h in p['src']) + '</p></div>')
    o.append(f'<h3>{esc("Free learning resources")}</h3><ul class="crs-res">' + ''.join(f'<li>{ext(t, h)}: {esc(d)}</li>' for t, h, d in u['res']) + '</ul>')
    o.append(f'<p class="crs-done"><label><input type="checkbox" data-done="{uid}"> {esc("I finished this unit")}</label></p>')
    o.append(top() + '</section>')
    return ''.join(o)

def lab(C, K, L):
    hd, rows = L['table']
    o = [f'<div class="crs-card crs-lab" id="{L["id"]}"><h3>{esc(L["title"])}</h3><p class="crs-kicker">{esc(L["week"])}</p><p><strong>{esc("Goal:")}</strong> {esc(L["goal"])}</p>',
         eqblock(K, *L['eq']), f'<h4>{esc("Procedure")}</h4><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in L['steps']) + '</ol>' + _code(L.get('code'), L.get('out')),
         f'<h4>{esc("Data table")}</h4>' + table(hd, rows) + f'<p class="crs-note">{esc(L["note"])}</p>',
         f'<h4>{esc("Sample calculation")}</h4><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in L['calc']) + '</ol>',
         f'<div class="crs-safe"><h4>{esc("Safety")}</h4>' + ul(L['safety']) + '</div>',
         f'<h4>{esc("Home or virtual alternative")}</h4>' + ul(L['home']) + '<p>' + ' · '.join(ext(t, h) for t, h in L['sims']) + '</p>',
         f'<p class="crs-planet-s"><strong>{esc("Planet link:")}</strong> {esc(L["planet"])}' + (' ' + ' · '.join(ext(t, h) for t, h in L['planet_src']) if L['planet_src'] else '') + '</p>',
         f'<p class="crs-done"><label><input type="checkbox" data-done="{L["id"]}"> {esc("I completed this lab (wet or virtual)")}</label></p></div>']
    return ''.join(o)

def pdf_key(C, l): return 'courses/' + C.PAGE[:-5] + '_Study_Guide' + ('' if l == 'en' else '_' + l) + '.pdf'
def pdf_link(C):
    # PDF study guide on R2 (made with --pdf: every answer open, print styles). Key = courses/<PAGE stem>_Study_Guide[_<lang>].pdf; English PDF as fallback
    MF = json.load(open('assets/data/media-manifest.json')); k = pdf_key(C, LANG)
    if k in MF: return f' <a class="crs-btn" href="{MF[k]["url"]}" download>{esc("Download the PDF study guide")}</a>'
    k = pdf_key(C, 'en')
    return f' <a class="crs-btn" href="{MF[k]["url"]}" hreflang="en" download>{esc("Download the PDF study guide")}{"" if LANG == "en" else " (" + esc("English") + ")"}</a>' if k in MF else ''

def make_pdf(C, l='en'):
    out = '/tmp/' + C.PAGE[:-5] + '_Study_Guide' + ('' if l == 'en' else '_' + l) + '.pdf'; src = (l + '/' if l != 'en' else '') + C.PAGE
    tmp = os.path.join(os.path.dirname(src), '_pdf_' + C.PAGE)
    open(tmp, 'w', encoding='utf8').write(open(src, encoding='utf8').read().replace('<details', '<details open'))
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8799'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        import time; time.sleep(1)
        subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=8000',
                        f'--print-to-pdf={out}', f'http://localhost:8799/{tmp}'], check=True, capture_output=True)
    finally:
        srv.kill(); os.remove(tmp)
    return out

UI = ['Score: {r} of {n}', ' (answered {a})', 'Correct. ', 'Not quite. The answer is: {x}. ', 'Try this quiz again', 'Answer: ', 'Card {i} of {n}: ', '. Activate to flip.',
      'Previous', 'Flip', 'Next', 'Shuffle', 'Show all', 'Clear your saved progress and quiz scores for this course?', '{d} of {n} units and labs done ({p}%).', ' Best quiz scores: {q}.']
def ui_attr(): return '' if LANG == 'en' else ' data-ui="' + html.escape(json.dumps({k: _(k) for k in UI}, ensure_ascii=False), quote=True) + '"'

def course_page(C):
    texs = [t for u in C.UNITS for t, _c in u['eqs']] + [L['eq'][0] for L in C.LABS] + C.FORMULAS
    K = katex(texs)
    toc = [('about', 'About this course'), ('start', 'Before you start'), ('schedule', '15-week schedule'), ('progress', 'Your progress')] + \
          [(u['id'], _('Unit {n}').replace('{n}', str(i)) + ': ' + _(u['title'])) for i, u in enumerate(C.UNITS, 1)] + \
          [('lab', 'Lab'), ('exam', 'Exam prep'), ('formulas', 'Formula sheet'), ('ptable', getattr(C, 'REF_TITLE', 'Periodic table')), ('glossary', 'Glossary'), ('rubric', 'Self-assessment')]
    names0 = {u['id'] for u in C.UNITS}
    o = [hero(C.TITLE, C.TAGLINE), f'<div class="crs" data-course="{C.ID}"{ui_attr()}{dir_attr()}>',
         f'<p class="crs-crumb"><a href="{HUB}">{esc("Courses")}</a> › {esc(C.CODE)}</p>',
         f'<div class="crs-toc" role="navigation" aria-label="{esc("On this page")}"><ul>' + ''.join(f'<li><a href="#{a}">{html.escape(b if a in names0 else _(b))}</a></li>' for a, b in toc) + '</ul></div>',
         f'<p class="crs-tools"><button type="button" class="crs-btn" data-print>{esc("Print this page")}</button>' + pdf_link(C) + '</p>']
    o.append(f'<section id="about"><h2>{esc("About this course")}</h2><div class="crs-disc">' + ''.join(f'<p>{esc(x)}</p>' for x in C.ABOUT) + '</div>'
             f'<div class="crs-planet"><h3>{esc("How this course helps save the planet")}</h3>' + ''.join(f'<p>{esc(x)}</p>' for x in C.COURSE_PLANET) + '</div>' + top() + '</section>')
    o.append(f'<section id="start"><h2>{esc("Before you start")}</h2><h3>{esc("Prerequisites")}</h3>' + ul(C.PREREQS) + f'<h3>{esc("How to study")}</h3>' + ul(C.STUDY)
             + f'<h3>{esc("Lab equipment (for the wet labs)")}</h3>' + ul(C.LAB_GEAR) + top() + '</section>')
    names = {u['id']: u['title'] for u in C.UNITS}; names['exam'] = 'Review'
    o.append(f'<section id="schedule"><h2>{esc("Suggested 15-week schedule")}</h2><p>{esc("About 6 to 9 hours a week: reading, practice problems and, in lab weeks, the lab.")}</p>'
             + table(['Week', 'Unit', 'Topics', 'Reading'], [[str(w), names[u], t, r] for w, u, t, r in C.SCHEDULE]) + top() + '</section>')
    o.append(f'<section id="progress"><h2>{esc("Your progress")}</h2><p>{esc("Tick units and labs as you finish them, and take the quizzes. Progress and quiz scores are saved only in this browser, never sent to us.")}</p>'
             f'<div class="crs-prog" aria-live="polite"><progress max="100" value="0"></progress><p class="crs-prog-t">{esc("Turn on JavaScript to track progress.")}</p></div>'
             f'<p><button type="button" class="crs-btn crs-reset" data-reset>{esc("Reset my progress")}</button></p>' + top() + '</section>')
    o += [unit(C, K, i, u) for i, u in enumerate(C.UNITS, 1)]
    o.append(f'<section id="lab"><h2>{esc(C.LAB_TITLE) if getattr(C, "LAB_TITLE", None) else html.escape(_("The lab ({code})").replace("{code}", getattr(C, "LAB_NAME", C.CODE.split(" + ")[-1])))}</h2>' + ''.join(f'<p>{esc(x)}</p>' for x in C.LAB_INTRO)
             + f'<p class="crs-src">{esc("Safety reference:")} {ext(*C.SAFETY_SRC)}</p>' + ''.join(lab(C, K, L) for L in C.LABS) + top() + '</section>')
    ex = [f'<section id="exam"><h2>{esc("Exam prep practice sets")}</h2><p>{esc("Time yourself: about 10 minutes per problem. Then compare with the full solutions.")}</p>']
    for t, probs in C.EXAMS:
        ex.append(f'<h3>{esc(t)}</h3><ol class="crs-prac">' + ''.join(
            f'<li><p>{esc(q)}</p><details><summary>{esc("Show full solution")}</summary><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in st) + f'</ol><p class="crs-ans"><strong>{esc("Answer:")}</strong> {esc(a)}</p></details></li>'
            for q, st, a in probs) + '</ol>')
    o.append(''.join(ex) + top() + '</section>')
    o.append(f'<section id="formulas"><h2>{esc("Formula sheet")}</h2><div class="crs-fs">' + ''.join(f'<div class="crs-math">{K[t]}</div>' for t in C.FORMULAS) + '</div>'
             f'<h3>{esc("Constants")}</h3>' + table(['Constant', 'Value'], C.CONSTANTS) + f'<p class="crs-src">{esc("Source:")} {ext(*C.CONST_SRC)}</p>' + top() + '</section>')
    o.append(f'<section id="ptable"><h2>{esc(getattr(C, "REF_TITLE", "Periodic table"))}</h2><p>{esc(getattr(C, "REF_INTRO", "Use one of these free interactive tables alongside the course."))}</p><ul class="crs-res">'
             + ''.join(f'<li>{ext(t, h)}: {esc(d)}</li>' for t, h, d in C.PTABLE) + '</ul>' + top() + '</section>')
    o.append(f'<section id="glossary"><h2>{esc("Glossary")}</h2><dl class="crs-gl">' + ''.join(f'<dt>{esc(a)}</dt><dd>{esc(b)}</dd>' for a, b in C.GLOSSARY) + '</dl>' + top() + '</section>')
    o.append(f'<section id="rubric"><h2>{esc("Self-assessment rubric")}</h2><p>{esc("No grade or credit is given. Use this to judge honestly where you are in each unit.")}</p>'
             + table(['Level', 'What it looks like'], C.RUBRIC) + f'<h3>{esc("Suggested weighting if you want a score")}</h3>' + table(['Part', 'Weight'], C.WEIGHTS)
             + f'<p>{esc("Aim for level 3 or better in every unit before moving to the next course.")}</p>' + top() + '</section>')
    o.append(related(C))
    o.append('</div>')
    return BL.shell(LANG, C.PAGE, _(C.TITLE) + ' (' + C.CODE + ')', _(C.DESC), ''.join(o), extra_head=head(), ld_type='Course', tail=tail())

def related(C):  # Oct 25 2026 (founder, upgrade 4): 'Related' block, 3-4 links from the roadmap (no new data):
    # the live courses just before and after this one in roadmap order, then other live courses from the same year, then the hub.
    order = [(yi, c) for yi, (_y, cs) in enumerate(RM.YEARS) for c, _t, _d in cs]
    title = {c: t for _y, cs in RM.YEARS for c, t, _d in cs}
    live = [(yi, c) for yi, c in order if c in LIVE]
    i = next(k for k, (_yi, c) in enumerate(live) if c == C.ID); yr = live[i][0]
    pick = [live[k][1] for k in (i - 1, i + 1) if 0 <= k < len(live)]
    pick += [c for y, c in live if y == yr and c != C.ID and c not in pick]
    def a(c):
        m = LIVE[c]
        if LANG == 'en' or LANG in DONE.get(c, ()): return f'<a href="{m.PAGE}">{esc(title[c])}</a> <span class="crs-kicker">{esc(m.CODE)}</span>'
        return f'<a href="../{m.PAGE}" hreflang="en">{esc(title[c])}</a> <span lang="en">(English)</span>'
    lis = [a(c) for c in pick[:3]] + [f'<a href="{HUB}">{esc("All courses")}</a>']
    return ('<!-- CRSREL:START --><aside class="crs-related" aria-labelledby="crs-rel-h" data-pagefind-ignore><h2 id="crs-rel-h">' + esc('Related courses') + '</h2><ul>'
            + ''.join(f'<li>{x}</li>' for x in lis) + '</ul></aside><!-- CRSREL:END -->')

def en_only(h):
    # alternates only for languages whose page exists on disk (all six once phase 2 is built)
    h = re.sub(r'\n?<link rel="alternate" hreflang="(?!en"|x-default")[^"]+" href="[^"]+">', lambda m: m.group(0) if os.path.exists(m.group(0).split('savingplanets.com/')[1].split('"')[0]) else '', h)
    return fix_switch(he_card(bidi(h)))

# RTL pages (ar, he): plain-text formulas inside RTL sentences (e.g. "f(x) = x² + 1", "∫ 2x dx") get <bdi dir="ltr"> so the
# bidi algorithm cannot reorder their operators. Text nodes only, inside the course/hub body; KaTeX blocks (.crs-math), script/style/pre/code skipped.
_FTOK = r"(?:&(?:lt|gt|amp|#x27|quot);|[A-Za-z0-9()\[\]{}+\-−–×÷·*/=<>≤≥≈≠^_.,:;′'|!√∫∑∏∂∞→←↔∈≡%°\u0370-\u03ff\u00c0-\u00ff\u0100-\u024f\u1e00-\u1eff⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾ⁿ₀₁₂₃₄₅₆₇₈₉₊₋ₙₓᵢₘₖₐₑₒₗₛ±⌀∓µ‰Å\u02b0-\u02ff\u1d2c-\u1dbf\u2070-\u209f½¼¾⅓⅔⅛ ])"
_FRUN = re.compile(_FTOK + '+')
_FOP = re.compile(r"&lt;|&gt;|[=+−×÷/^<>≤≥≈≠√∫∑∏∂∞→⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ₀₁₂₃₄₅₆₇₈₉ₙₓᵢ′½±⌀∓Ø\u02b0-\u02ff]|\w\(|\w\[|[*%]|\d\s*[-–]\s*\d|\d\s?(?:µm|nm|mm|km|kΩ|µF|µT|µC|°C|%)")
def _wrap_run(m):
    t = m.group(0); a = len(t) - len(t.lstrip(" ,.;:")); b = len(t.rstrip(" ,.;:"))
    f = re.search(r':\.\d+[a-z%]', t)  # Python format specs (:.2f, :.1%) in prose
    if f and not t.strip(' ,.;()-').replace(f.group(0), ''): return t[:f.start()] + '<bdi dir="ltr">' + f.group(0) + '</bdi>' + t[f.end():]
    core = t[a:b]
    while core and core[-1] in '( ' : core = core[:-1]; b -= 1
    while core.endswith(')') and core.count('(') < core.count(')'): core = core[:-1]; b -= 1
    while core.startswith('(') and core.count('(') > core.count(')'): core = core[1:]; a += 1
    if core.startswith('-−'): core = core[1:]; a += 1
    pos = m.start() + a
    if core.startswith('-') and pos > 0 and '\u05d0' <= m.string[pos - 1] <= '\u05ea': core = core[1:]; a += 1  # Hebrew prefix ב-30%  # Hebrew prefix hyphen (ו-) before a minus sign stays outside
    for q in ('&#x27;', "'"):  # Hebrew geresh (פלנג'): stays with its word, then the colon after it stays outside too
        if core.startswith(q) and pos > 0 and '\u05d0' <= m.string[pos - 1] <= '\u05ea':
            n = len(q) + len(core[len(q):]) - len(core[len(q):].lstrip(' ,.;:')); core = core[n:]; a += n
    if not re.search(r'[A-Za-z0-9]', core) and re.search(r'[=!*/%^]', core):  # operators only, e.g. "//, %" in prose: wrap each one
        return t[:a] + re.sub(r'==|!=|\+=|-=|\*\*|//|%|\*|=|(?:&lt;|&gt;)=?', lambda o: '<bdi dir="ltr">' + o.group(0) + '</bdi>', core) + t[b:]
    if re.fullmatch(r'==|!=|\+=|-=|\*=|/=|\*\*|//|%|\*|=|(?:&lt;|&gt;)=?|\^', core): return t[:a] + '<bdi dir="ltr">' + core + '</bdi>' + t[b:]  # lone operators (% ** == +=) in prose
    if len(core) == 2 and re.fullmatch(r'[Ø⌀±+−][0-9]', core): return t[:a] + '<bdi dir="ltr">' + core + '</bdi>' + t[b:]  # Ø6, +5
    if len(core) < 3 or not re.search(r'[A-Za-z0-9]', core) or not _FOP.search(core): return t
    return t[:a] + _balanced(core) + t[b:]
def _balanced(core):
    # Oct 25: a run cut by RTL text can hold an unmatched "(" or ")" (e.g. "T = 20 + 0.1x (°C" + Arabic). Leave unmatched brackets outside
    # the isolate so they pair with their partner across the RTL text, and wrap each piece on its own.
    st, bad = [], set()
    for k, ch in enumerate(core):
        if ch == '(': st.append(k)
        elif ch == ')':
            if st: st.pop()
            else: bad.add(k)
    bad |= set(st)
    if not bad: return '<bdi dir="ltr">' + core + '</bdi>'
    out, piece = [], ''
    def flush(x):
        y = x.strip(' ,;:')  # punctuation left over next to an unpaired bracket stays outside the isolate
        if not y: return x
        lead, trail = x[:len(x) - len(x.lstrip(' ,;:'))], x[len(x.rstrip(' ,;:')):]
        return lead + ('<bdi dir="ltr">' + y + '</bdi>' if re.search(r'[A-Za-z0-9\u0370-\u03ff]', y) else y) + trail
    for k, ch in enumerate(core):
        if k in bad: out.append(flush(piece)); out.append(ch); piece = ''
        else: piece += ch
    out.append(flush(piece))
    return ''.join(out)
def bidi(h):
    if LANG not in RTL or '<div class="crs"' not in h: return h
    i = h.index('<div class="crs"'); j = h.rindex('</main>')
    body = h[i:j]; keep = []
    def hold(m): keep.append(m.group(0)); return f'\x00{len(keep) - 1}\x00'
    body = re.sub(r'<div class="crs-math">.*?</div>|<(script|style|pre|code)\b.*?</\1>|<bdi\b.*?</bdi>', hold, body, flags=re.S)
    body = re.sub(r'>([^<\x00]+)<', lambda m: '>' + _FRUN.sub(_wrap_run, m.group(1)) + '<', body)
    body = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], body)
    return h[:i] + body + h[j:]

def he_card(h):
    # he/ has no share cards of its own (build-og: fr/es/ar/it); its Kids_Map template carries en/Contact.jpg, so use this page's English card
    # (version hash from assets/og/manifest.json, the same ?v= build-og puts on the English page)
    if LANG != 'he': return h
    m = re.search(r'<link rel="canonical" href="[^"]*/he/([\w-]+)\.html"', h)
    if not m: return h
    k = 'assets/og/en/' + m.group(1) + '.jpg'; v = json.load(open('assets/og/manifest.json')).get(k)
    if not v: return h
    url = 'https://www.savingplanets.com/' + k + '?v=' + v[:8]
    return re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*"', lambda x: x.group(1) + url + '"', h)

def fix_switch(h):
    # language switcher: a language whose version of this page is not built yet goes to that language's home page (never a 404)
    def one(m):
        href, lg = m.group(1), m.group(2)
        f = re.sub(r'^(\.\./)+', '', href.split('#')[0])
        if os.path.exists(f): return m.group(0)
        home = ('../' if LANG != 'en' else '') + ('' if lg == 'en' else lg + '/') + 'index.html'
        return m.group(0).replace(f'href="{href}"', f'href="{home}"')
    return re.sub(r'<li class="lang-switch".*?</li>', lambda b: re.sub(r'<a class="spn-ls"[^>]*?href="([^"]+)" hreflang="(\w+)"', one, b.group(0)), h, flags=re.S)

def hub_page():
    o = [hero('Courses', 'A free four-year aerospace and STEM study track, built one course at a time.'), f'<div class="crs"{dir_attr()}>',
         f'<div class="crs-disc"><p>{esc("These are free self-study courses written by Saving Planets. They follow the scope of first- to fourth-year college courses using open materials, but they are not university courses, carry no academic credit, and no school is involved.")}</p>'
         f'<p>{esc("Every course ties its subject to real work that helps people and nature, and links to free, reputable resources.")}</p></div>',
         f'<div class="crs-toc" role="navigation" aria-label="{esc("Years")}"><ul>' + ''.join(f'<li><a href="#y{i}">{html.escape(_(y).split(" · ")[0])}</a></li>' for i, (y, _c) in enumerate(RM.YEARS, 1)) + '</ul></div>']
    for i, (y, cs) in enumerate(RM.YEARS, 1):
        o.append(f'<section id="y{i}"><h2>{esc(y)}</h2><ul class="crs-grid">')
        for cid, t, d in cs:
            m = LIVE.get(cid)
            if m and (LANG == 'en' or LANG in DONE.get(cid, ())): o.append(f'<li class="crs-c live"><span class="crs-badge">{esc("Live")}</span><h3><a href="{m.PAGE}">{esc(t)}</a></h3><p>{esc(d)}</p><p class="crs-kicker">{esc(m.CODE)}</p></li>')
            elif m: o.append(f'<li class="crs-c live"><span class="crs-badge">{esc("Live")}</span><h3><a href="../{m.PAGE}" hreflang="en">{esc(t)}</a> <span lang="en">(English)</span></h3><p>{esc(d)}</p><p class="crs-kicker">{esc(m.CODE)}</p></li>')
            else: o.append(f'<li class="crs-c"><span class="crs-badge soon">{esc("Coming soon")}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>')
        o.append('</ul>' + top() + '</section>')
    o.append('</div>')
    return BL.shell(LANG, HUB, _('Courses: free aerospace and STEM study track'), _('Free self-study courses on Saving Planets: a four-year aerospace and STEM track with labs, quizzes and study guides. No credit, no cost.'),
                    ''.join(o), extra_head=head(), ld_type='CollectionPage', tail='')

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
        first = next((LIVE[c] for _y, cs in RM.YEARS for c, _t, _d in cs if c in LIVE), MODS[0])  # first live course in roadmap order (not file order)
        global LANG; LANG = l
        if l == 'en' or l in DONE.get(first.ID, ()):  # phase 2: the translated course pages exist, link them in this language
            lk = f'<a href="{first.PAGE}">{esc(first.TITLE)}</a> · <a href="{HUB}">{html.escape(a)}</a>'
        else:
            lk = f'<a href="{pre}{first.PAGE}" hreflang="en">{html.escape(first.TITLE)}</a> (English) · <a href="{pre}{HUB}" hreflang="en">{html.escape(a)}</a>'
        LANG = 'en'
        blk = (f'<!-- COURSELINK:START --><aside class="learn-link card-band" aria-label="{html.escape(h)}"><h2>{html.escape(h)}</h2><p>{html.escape(t)} '
               + lk + '</p></aside><!-- COURSELINK:END -->')
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

def strings_of(cid):  # English strings a course (or '_shared' = hub + headings + UI) looks up, in page order
    global LANG; seen = {}; old = _orig = globals()['_']
    def rec(x):
        if isinstance(x, str) and needs_tr(x): seen.setdefault(x, None)
        return _orig(x)
    LANG = 'fr'; globals()['_'] = rec
    try:
        hub_page(); [_orig and rec(k) for k in UI]; sh = dict(seen)
        if cid == '_shared': return list(sh)
        seen.clear(); course_page(LIVE[cid]); return [k for k in seen if k not in sh]
    finally: globals()['_'] = _orig; LANG = 'en'

NUM_RX = r'\d+(?:[.,]\d+)*'
def nums(x): return sorted(n.replace(',', '') for n in re.findall(NUM_RX, x))
def export_missing(cid):
    ks = [k for k in strings_of(cid) if any(l not in TR.get(k, {}) for l in LANGS[1:])]
    f = f'/tmp/courses-missing-{cid}.tsv'
    with open(f, 'w', encoding='utf8') as o:
        o.write('en\t' + '\t'.join(LANGS[1:]) + '\n')
        for k in ks: o.write(k.replace('\t', ' ') + '\t' + '\t'.join(TR.get(k, {}).get(l, '') for l in LANGS[1:]) + '\n')
    print(f, len(ks), 'strings')

def import_tsv(path, cid):
    p = f'i18n/courses/{cid}.json'; d = json.load(open(p, encoding='utf8')) if os.path.exists(p) else {}
    rows = [r.rstrip('\n').split('\t') for r in open(path, encoding='utf8')]; hdr = rows[0]; bad = []
    for r in rows[1:]:
        en = r[0]
        for l, t in zip(hdr[1:], r[1:]):
            if not t: continue
            if nums(en) != nums(t) or sorted(re.findall(r'\{\w+\}', en)) != sorted(re.findall(r'\{\w+\}', t)): bad.append((l, en[:60], t[:60])); continue
            d.setdefault(en, {})[l] = t
    json.dump(dict(sorted(d.items())), open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1); open(p, 'a').write('\n')
    print(p, len(d), 'strings;', len(bad), 'rejected (numbers or {placeholders} differ):', *bad[:20], sep='\n')

def relink(langs, gaps):
    # every page of a translated language links its own copy of the hub/course (nav "Courses" item, Teachers, Learn...) instead of ../English.
    # Same result build-nav.py gives on the next full weekly-sync; done here so a course language goes live in one step.
    for l in langs[1:]:
        pages = ([HUB] if not gaps.get('_hub', {}).get(l) else []) + [m.PAGE for m in MODS if l in DONE.get(m.ID, ())]
        if not pages: continue
        rx = re.compile(r'href="\.\./(' + '|'.join(map(re.escape, pages)) + r')([#"])(?! hreflang=)')  # never the language switcher (its links carry hreflang)
        for f in glob.glob(l + '/*.html'):
            s = open(f, encoding='utf8').read(); n = rx.sub(r'href="\1\2', s)
            if n != s: open(f, 'w', encoding='utf8').write(n)

if __name__ == '__main__':
    if '--check' in sys.argv: sys.exit(0 if check() else 1)
    if '--pdf' in sys.argv:
        for m in MODS:
            for l in [x for x in LANGS if x == 'en' or os.path.exists(x + '/' + m.PAGE)]: print(make_pdf(m, l))
        sys.exit(0)
    if '--pdf' in sys.argv: pass
    if '--missing' in sys.argv: export_missing(sys.argv[sys.argv.index('--missing') + 1]); sys.exit(0)
    if '--import' in sys.argv: a = sys.argv.index('--import'); import_tsv(sys.argv[a + 1], sys.argv[a + 2]); sys.exit(0)
    banners()
    langs = [l for l in LANGS if l in BUILD_LANGS and (l == 'en' or os.path.exists(l + '/Kids_Map.html'))]
    gaps = {}
    for l in langs[1:]:  # which courses are complete in which language (shared strings count for every course)
        LANG = l; MISSING.clear(); hub_page(); shared = set(MISSING)
        if shared: gaps.setdefault('_hub', {})[l] = sorted(shared)
        for m in MODS:
            MISSING.clear(); course_page(m); miss = set(MISSING) | shared
            if miss: gaps.setdefault(m.ID, {})[l] = sorted(miss)
            else: DONE.setdefault(m.ID, set()).add(l)
    for _pass in (1, 2):  # second pass: hreflang alternates see every language's file
        for LANG in langs:
            for m in MODS:
                f = out(m.PAGE)
                if LANG == 'en' or LANG in DONE.get(m.ID, ()): open(f, 'w', encoding='utf8').write(en_only(course_page(m)))
                elif os.path.exists(f): os.remove(f)  # never leave a stale half-translated page
            if LANG == 'en' or not gaps.get('_hub', {}).get(LANG): open(out(HUB), 'w', encoding='utf8').write(en_only(hub_page()))
    LANG = 'en'
    for cid, g in gaps.items():
        print(f'build-courses: {cid} not translated yet in', {l: len(v) for l, v in g.items()}, f'(English only there; run --missing {cid})')
    if '--strict' in sys.argv and gaps: raise SystemExit(1)
    teachers_links()
    relink(langs, gaps)
    print('build-courses:', HUB, '+', [m.PAGE for m in MODS])
