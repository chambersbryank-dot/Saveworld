#!/usr/bin/env python3
"""Oct 24 2026 (founder): free self-study Courses section. Data-driven: every scripts/courses/<id>.py with PAGE + STATUS='live'
becomes one course page; scripts/courses/roadmap.py is the 4-year track on Undergraduate_Studies.html. Phase 1 = English only.
Also: anim-banners.json entries (multi-photo banner from each module's BANNER/CREDITS), assets/courses.css + assets/courses.js.
  python3 scripts/build-courses.py           build
  python3 scripts/build-courses.py --check   arithmetic checks (module CHECKS) + every external link must load
Course module fields: see scripts/courses/chem110.py (the template). Optional: LAB_NAME (lab heading) or LAB_TITLE (whole heading), REF_TITLE/REF_INTRO (the reference-links section; default Periodic table). Oct 24: phys110.py = course 2. Idempotent."""
import os, sys, re, json, glob, html, importlib, subprocess, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT); sys.path.insert(0, 'scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py'); BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
from courses import roadmap as RM
from courses import aero101_watch as AW
from courses import aero101_forces as AF
from courses import aero101_review as AR
from courses import aero101_film as A1F
from courses import nasa_film as NF
from courses import aero101_bank as AB
V = '20261102a'  # OCW section tabs (assets/courses.css + courses.js)
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
LECTURES = json.load(open('scripts/courses/lectures.json', encoding='utf8'))  # course id -> unit index -> official lecture (scripts/courses/lectures.json)
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
def credit_p(text):
    # Isolate Latin names so a following colon stays with the Arabic or Hebrew clause.
    t = html.escape(_(text), quote=False)
    t = t.replace('Saving Planets', '<bdi>Saving Planets</bdi>')
    t = re.sub(r'(?<![\w])SI(?![\w])', '<bdi>SI</bdi>', t)
    return f'<p class="crs-note">{t}</p>'
OER_AERO_URL = 'https://oercommons.org/courses/introduction-to-aerospace-engineering-aero-101'
def oer_pub(C):
    # AERO 101 only. A small footer link; scripts/build-published.py writes the same markup.
    if getattr(C, 'ID', '') != 'aero101': return ''
    return (f'<!-- OERPUB:START --><a class="crs-oer" href="{OER_AERO_URL}" target="_blank" rel="noopener">'
            f'<bdi>OER Commons</bdi></a><!-- OERPUB:END -->')
def aero_foot(page, C):
    # The SI disclosure stays, in the license line, once. The OER link sits beside it.
    inner = credit_p(C.CREDIT)[len('<p class="crs-note">'):-len('</p>')]
    policy = html.escape(AERO_POLICY[LANG])
    page = page.replace(f'<p class="crs-note">{inner}</p>', '', 1)
    page = re.sub(r'<!-- OERPUB:START -->.*?<!-- OERPUB:END -->', '', page, count=1, flags=re.S)
    mark = '</p><!-- LICENSE:END -->'
    if mark not in page: return page
    if inner not in page:
        page = page.replace('<p class="lic-foot">', f'<p class="lic-foot">{inner} {policy} ', 1)
    elif policy not in page:
        page = page.replace(inner, inner + ' ' + policy, 1)
    if 'id="founders"' not in page:
        anchor = f'<p class="lic-foot">{inner}'
        if anchor not in page: return page
        page = page.replace(anchor, AR.founders(LANG) + anchor, 1)
    if 'OERPUB:START' not in page:
        page = page.replace(mark, ' ' + oer_pub(C) + mark, 1)
    return page
UNITS_RX = r'\b(?:atm|mol|g|L|K|mL|nm|kPa|mmHg|kJ|J|u|M|s|m|cm|mg|kg|Hz|µM|mol⁻¹|M⁻¹|cm⁻¹)\b'
_CAPW = re.compile(r'[A-Z][a-z]{2,}(?![\w(′.])(?=.*[=≈∇∂Α-Ωα-ω])')
_SHORTW = re.compile(r'(?<![\w^_′])(so|to|of|in|is|or|if|by|as|at|an|on|up|no)(?![\w(′])')
def needs_tr(s):  # words to translate (not a URL, a site page name, or numbers + units). Oct 25: a formula sentence with a short English word ("…, so a = 2") counts too
    if isinstance(s, str) and not re.match(r'(https?:|mailto:|#)', s) and _SHORTW.search(s): return True
    if isinstance(s, str) and not re.match(r'(https?:|mailto:|#)', s) and _CAPW.match(s): return True  # Oct 25: formula sentence opening with a capitalised word ('Use Δv = …', 'Set ΔG = 0: …', 'One τ')
    return bool(re.search('[a-z]{3}', s)) and not re.match(r'(https?:|mailto:|#)', s) and not re.fullmatch(r'(\.\./)?[\w-]+\.html(#[\w-]+)?', s) and not same(s)
def same(s):  # numbers + SI units only (e.g. "0.500 mol", "8.314 J/(mol·K)"): identical in every language
    return not re.search('[A-Za-zÀ-ÿ]{2,}', re.sub(UNITS_RX, '', s))
def pre(): return '' if LANG == 'en' else '../'
def loc(p):  # site page link from a course page: stay in the language folder when that page exists there
    if LANG == 'en' or re.match(r'(https?:|mailto:|#)', p): return p
    return p if os.path.exists(LANG + '/' + p.split('#')[0]) or p.split('#')[0] in (HUB,) + tuple(m.PAGE for m in MODS if LANG in DONE.get(m.ID, ())) else '../' + p
def out(p): return p if LANG == 'en' else LANG + '/' + p
HUB = 'Undergraduate_Studies.html'
MODS = []
for f in sorted(glob.glob('scripts/courses/*.py')):
    n = os.path.basename(f)[:-3]
    if n in ('__init__', 'roadmap', 'aero101_watch'): continue
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
def hero(t, k, extra=''): return f'<section class="page-hero hero-learn" id="top"><div class="page-hero-content"><h1>{esc(t)}</h1><p>{esc(k)}</p>{extra}</div></section>\n'
def head(): return BL.katex_head(LANG) + f'<link rel="stylesheet" href="{pre()}assets/courses.css?v={V}">\n'
def tail(): return f'<script src="{pre()}assets/courses.js?v={V}" defer></script>\n'
def table(headr, rows, cap=''):
    th = ''.join(f'<th scope="col">{esc(x)}</th>' for x in headr)
    return (f'<div class="crs-tw"><table class="crs-tbl">{"<caption>" + esc(cap) + "</caption>" if cap else ""}<thead><tr>{th}</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')
_TEX = [('\\tau', 'τ'), ('\\mu', 'μ'), ('\\rho', 'ρ'), ('\\nu', 'ν'), ('\\theta', 'θ'), ('\\Delta', 'Δ'),
        ('\\pi', 'π'), ('\\sigma', 'σ'), ('\\omega', 'ω'), ('\\alpha', 'α'), ('\\beta', 'β'), ('\\gamma', 'γ'),
        ('\\cdot', '·'), ('\\times', '×'), ('\\leq', '≤'), ('\\geq', '≥'), ('\\approx', '≈'), ('\\infty', '∞'),
        ('\\,', ' '), ('\\ ', ' ')]
def tex_plain(tex):
    """Readable equation text for copy and read-aloud. KaTeX's visual layer copies as broken glyphs."""
    s = tex
    s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)
    s = re.sub(r'\\text\{([^{}]*)\}', r'\1', s)
    for a, b in _TEX:
        s = s.replace(a, b)
    s = s.replace('{', '').replace('}', '')
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    return re.sub(r'\s+', ' ', s).strip()
def eqblock(K, tex, cap):
    plain = html.escape(tex_plain(tex))
    return (f'<figure class="crs-eq"><div class="crs-math">{K[tex]}</div>'
            f'<p class="crs-eqtext" dir="ltr">{plain}</p><figcaption>{esc(cap)}</figcaption></figure>')

def _code(src, out=None):
    """Optional code listing (+ verified output) for programming courses; code is never translated. Inline style so courses.css/V need no change."""
    st = 'style="direction:ltr;text-align:left;overflow-x:auto;padding:.75em;border-radius:6px;background:rgba(127,127,127,.12);font-size:.9em"'
    r = f'<pre class="crs-code" dir="ltr" {st}><code>{html.escape(src)}</code></pre>' if src else ''
    if out is not None: r += f'<p><strong>{esc("Output")}</strong></p><pre class="crs-out" dir="ltr" {st}><code>{html.escape(out)}</code></pre>'
    return r

def unit(C, K, i, u):
    uid = u['id']
    film = ''
    more = ''
    if C.ID == 'aero101' and uid.startswith('u') and uid[1:].isdigit() and 1 <= int(uid[1:]) <= 10:
        n = int(uid[1:])
        film = A1F.figure(LANG) if n == 1 else AW.feature(LANG, n)
        more = AW.more(LANG, n)
    o = [f'<section class="crs-unit" id="{uid}" data-unit="{uid}" aria-labelledby="{uid}-h">',
         f'<p class="crs-kicker">{esc("Unit {n}").replace("{n}", str(i))}' + ('' if C.ID == 'aero101' else ' · ' + esc(u["weeks"])) + f'</p><h2 id="{uid}-h">{esc(u["title"])}</h2>' + film + more + f'<p class="crs-lead">{esc(u["summary"])}</p>']
    o.append(f'<h3>{esc("Learning objectives")}</h3><p>{esc("By the end of this unit you can:")}</p>' + ul(u['objectives'], 'crs-obj'))
    o.append(f'<h3>{esc("Key concepts")}</h3>' + ul(u['concepts'], 'crs-key'))
    if C.ID == 'aero101' and uid == 'u1':
        o.append(AF.figure(LANG))
    o.append(f'<h3>{esc("Key equations")}</h3>' + ''.join(eqblock(K, t, c) for t, c in u['eqs']))
    o.append(f'<h3>{esc("Worked examples, step by step")}</h3>')
    for j, w in enumerate(u['worked'], 1):
        o.append(f'<div class="crs-card crs-worked"><p class="crs-q"><strong>{esc("Example {n}").replace("{n}", f"{i}.{j}")}</strong> {esc(w["q"])}</p>' + _code(w.get('code')) +
                 f'<details><summary>{esc("Show the steps")}</summary><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in w['steps']) + '</ol>' + _code(None, w.get('out')) + f'<p class="crs-ans"><strong>{esc("Answer:")}</strong> {esc(w["a"])}</p></details></div>')
    o.append(f'<h3>{esc("Practice problems")}</h3><p>{esc("Work each on paper first, then check.")}</p><ol class="crs-prac">' + ''.join(
        f'<li><p>{esc(q)}</p><details><summary>{esc("Show answer")}</summary><p>{esc(a)}</p></details></li>' for q, a in u['practice']) + '</ol>')
    o.append(f'<h3>{esc("Common misconceptions")}</h3><ul class="crs-mis">' + ''.join(
        f'<li><p><span class="crs-x">{esc("Myth:")}</span> {esc(m)}</p><p><span class="crs-ok">{esc("Actually:")}</span> {esc(f)}</p></li>' for m, f in u['misc']) + '</ul>')
    if C.ID == 'aero101' and uid.startswith('u') and uid[1:].isdigit() and 1 <= int(uid[1:]) <= 10:
        keep = ''
        if uid == 'u3':
            keep = f'<ul class="crs-force-keep">{AF.force_cards(LANG)}</ul>'
        elif uid == 'u1':
            keep = f'<ul class="crs-force-keep"><li>{AF.stage(LANG, "all")}</li></ul>'
        bank = os.path.join(ROOT, 'assets', 'courses', 'aero101', f'{uid}.{LANG}.json')
        n_q, n_c = 20, 24
        if os.path.exists(bank):
            data = json.load(open(bank, encoding='utf-8'))
            n_q, n_c = len(data['quiz']), len(data['cards'])
        deck, quiz = AB.mount(LANG, uid, n_q, n_c)
        o.append(f'{keep}<h3>{esc("Flashcards")}</h3>{deck}')
        o.append(f'<h3>{esc("Self-check quiz")}</h3>{quiz}')
    else:
        cards = ''.join(f'<li><p class="crs-fc-f">{esc(a)}</p><p class="crs-fc-b">{esc(b)}</p></li>' for a, b in u['cards'])
        o.append(f'<h3>{esc("Flashcards")}</h3><div class="crs-fc" data-fc="{uid}"><ul class="crs-fc-list">{cards}</ul></div>')
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
    res = ''.join(f'<li>{ext(t, h)}: {esc(d)}</li>' for t, h, d in u['res'])
    if C.ID != 'aero101':
        o.append(f'<h3>{esc("Free learning resources")}</h3><ul class="crs-res">{res}</ul>')
    if C.ID == 'aero101':
        # The featured film and any Watch and Learn films are already at the top of the unit.
        o.append(AF.deeper(LANG, res))
        lec = None
    else:
        lec = LECTURES.get(C.ID, {}).get(str(i - 1))  # plain link; embeds stay off until Bryan approves that course
    if lec:
        lic = {'CC BY-NC-SA 4.0': ('https://creativecommons.org/licenses/by-nc-sa/4.0/', 'https://ocw.mit.edu/pages/privacy-and-terms-of-use/'),
               'CC BY-NC-SA 3.0 US': ('https://creativecommons.org/licenses/by-nc-sa/3.0/us/', 'https://oyc.yale.edu/terms')}[lec['license']]
        o.append(f'<div class="crs-lec"><h3>{esc("Watch the lecture")}</h3><p><a href="{html.escape(lec["url"])}" rel="noopener" lang="en">{html.escape(lec["title"])}</a> ({esc("in English")})</p>'
                 f'<p class="crs-src"><span lang="en">{html.escape(lec["course"])}, {html.escape(lec["provider"])}</span>. {esc("License:")} <a href="{lic[0]}" rel="noopener license">{lec["license"]}</a> · <a href="{lic[1]}" rel="noopener">{esc("Terms of use")}</a>. '
                 f'{esc("Linked for free study only; Saving Planets is not affiliated with or endorsed by this university.")}</p></div>')
    o.append(gc_slot(abs_page(C.PAGE, f'#{uid}'), _('Unit {n}').replace('{n}', str(i)) + ': ' + _(u['title']),
                     _('Free Saving Planets lesson. No university credit. Listing a source is not an endorsement.'), 'assignment'))
    if C.ID != 'aero101':
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
         +(f'<p class="crs-done"><label><input type="checkbox" data-done="{L["id"]}"> {esc("I completed this lab (wet or virtual)")}</label></p>' if C.ID != 'aero101' else '') + '</div>']
    return ''.join(o)

def pdf_key(C, l): return 'courses/' + C.PAGE[:-5] + '_Study_Guide' + ('' if l == 'en' else '_' + l) + '.pdf'
def pdf_link(C):
    # PDF study guide on R2 (made with --pdf: every answer open, print styles). Key = courses/<PAGE stem>_Study_Guide[_<lang>].pdf; English PDF as fallback
    MF = json.load(open('assets/data/media-manifest.json')); k = pdf_key(C, LANG)
    docx = AR.guide_link(LANG) if getattr(C, 'ID', '') == 'aero101' else ''
    if k in MF: return f' <a class="btn crs-btn" href="{MF[k]["url"]}" download>{esc("Download the PDF study guide")}</a>' + docx
    k = pdf_key(C, 'en')
    docx = AR.guide_link(LANG) if getattr(C, 'ID', '') == 'aero101' else ''
    return (f' <a class="btn crs-btn" href="{MF[k]["url"]}" hreflang="en" download>{esc("Download the PDF study guide")}{"" if LANG == "en" else " (" + esc("English") + ")"}</a>' + docx) if k in MF else docx

def make_pdf(C, l='en'):
    """Print the course page to a tagged PDF. Equation text (.crs-eqtext) stays selectable.
    Arabic and Hebrew pages already set dir=rtl and lang, so Chrome writes /Lang and right-to-left text.
    Chrome 156 writes a structure tree (tagged). Headless Chrome often does not exit after the file
    is written, so we stop it once the PDF is on disk."""
    import time, tempfile, shutil
    out = '/tmp/' + C.PAGE[:-5] + '_Study_Guide' + ('' if l == 'en' else '_' + l) + '.pdf'
    src = (l + '/' if l != 'en' else '') + C.PAGE
    folder = os.path.dirname(src) or '.'
    tmp = os.path.join(folder, '_pdf_' + C.PAGE)
    html = open(src, encoding='utf8').read().replace('<details', '<details open')
    # Keep the plain equation line in the print (it is the selectable text layer).
    html = html.replace('</head>', '<style>@media print{.crs-eqtext{display:block!important;visibility:visible!important}}</style></head>', 1)
    open(tmp, 'w', encoding='utf8').write(html)
    if os.path.exists(out): os.remove(out)
    cmd = ['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
           '--no-first-run', '--no-pdf-header-footer',  # --user-data-dir and --virtual-time-budget made Chrome hang (Nov 1)
           f'--print-to-pdf={os.path.abspath(out)}', 'file://' + os.path.abspath(tmp)]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(200):
            if os.path.exists(out) and os.path.getsize(out) > 2000:
                time.sleep(0.4)
                break
            if proc.poll() is not None:
                break
            time.sleep(0.25)
    finally:
        proc.kill(); proc.wait(timeout=5)
        os.remove(tmp)
    if not os.path.exists(out) or os.path.getsize(out) < 2000:
        raise SystemExit(f'PDF failed for {src}')
    return out

UI = ['Score: {r} of {n}', ' (answered {a})', 'Correct. ', 'Not quite. The answer is: {x}. ', 'Try this quiz again', 'Answer: ', 'Card {i} of {n}: ', '. Activate to flip.',
      'Previous', 'Flip', 'Next', 'Shuffle', 'Show all', 'Clear your saved progress and quiz scores for this course?', '{d} of {n} units and labs done ({p}%).', ' Best quiz scores: {q}.']
def ui_attr(): return '' if LANG == 'en' else ' data-ui="' + html.escape(json.dumps({k: _(k) for k in UI}, ensure_ascii=False), quote=True) + '"'

WET_IDS = {'chem110', 'phys110'}  # only these lists real wet-lab glassware; every other course is a computer or home lab
GEAR_T = {'en': 'What you need', 'fr': 'Ce qu’il vous faut', 'es': 'Qué necesitas', 'ar': 'ماذا تحتاج', 'it': 'Che cosa ti serve', 'he': 'מה צריך'}
UPD_T = {'en': 'Last updated', 'fr': 'Dernière mise à jour', 'es': 'Última actualización', 'ar': 'آخر تحديث', 'it': 'Ultimo aggiornamento', 'he': 'עודכן לאחרונה'}
VER_T = {'en': 'Version', 'fr': 'Version', 'es': 'Versión', 'ar': 'الإصدار', 'it': 'Versione', 'he': 'גרסה'}
CHK_T = {
 'en': 'A check is one number or code result on a course page that a script recomputes before the page is published. The printed number and the recomputed number have to match.',
 'fr': 'Un contrôle est un nombre ou un résultat de code sur une page de cours qu’un script recalcule avant publication. Le nombre affiché et le nombre recalculé doivent correspondre.',
 'es': 'Una comprobación es un número o un resultado de código en una página de curso que un script vuelve a calcular antes de publicar. El número impreso y el recalculado tienen que coincidir.',
 'ar': 'التحقق هو رقم أو نتيجة برمجية في صفحة مقرر يعيد سكربت حسابها قبل النشر. يجب أن يطابق الرقم المعروض الرقم المعاد حسابه.',
 'it': 'Un controllo è un numero o un risultato di codice in una pagina del corso che uno script ricalcola prima della pubblicazione. Il numero stampato e quello ricalcolato devono coincidere.',
 'he': 'בדיקה היא מספר או תוצאת קוד בעמוד קורס שסקריפט מחשב מחדש לפני הפרסום. המספר המודפס והמספר שחושב מחדש חייבים להתאים.',
}
SCOPE_T = {
 'en': 'This free course has {n} units and {m} labs. Those are the real counts, not a longer syllabus cut short.',
 'fr': 'Ce cours gratuit compte {n} unités et {m} travaux pratiques. Ce sont les vrais totaux, pas un programme plus long raccourci.',
 'es': 'Este curso gratuito tiene {n} unidades y {m} laboratorios. Son los totales reales, no un programa más largo recortado.',
 'ar': 'يتضمن هذا المقرر المجاني {n} وحدات و{m} مختبرات. هذه الأعداد الحقيقية وليست منهجًا أطول جرى اختصاره.',
 'it': 'Questo corso gratuito ha {n} unità e {m} laboratori. Sono i totali reali, non un programma più lungo accorciato.',
 'he': 'לקורס החינמי הזה יש {n} יחידות ו-{m} מעבדות. אלה המספרים האמיתיים, לא תוכנית ארוכה יותר שקוצרה.',
}
# AERO 101 pilot labels. SI drafts: no native speaker has reviewed these six-language strings.
AERO_UI = {
 'en': {'line': 'Description'},
 'fr': {'line': 'Description'},
 'es': {'line': 'Descripción'},
 'ar': {'line': 'الوصف'},
 'it': {'line': 'Descrizione'},
 'he': {'line': 'תיאור'},
}
AERO_NEED = {
 'en': 'Prerequisites: Algebra, trigonometry, Physics I mechanics; Calculus I is recommended.',
 'fr': 'Prérequis : algèbre, trigonométrie, mécanique de Physique I ; Analyse I est recommandée.',
 'es': 'Requisitos previos: álgebra, trigonometría, mecánica de Física I; se recomienda Cálculo I.',
 'ar': 'المتطلبات السابقة: الجبر، وحساب المثلثات، وميكانيكا الفيزياء I؛ يُستحسَن حساب التفاضل والتكامل I.',
 'it': 'Prerequisiti: algebra, trigonometria, meccanica di Fisica I; si consiglia Analisi I.',
 'he': 'ידע מוקדם: אלגברה, טריגונומטריה, מכניקה של פיזיקה I; מומלץ חדו״א I.',
}
AERO_POLICY = {
 'en': 'This is not a university course, it carries no academic credit, no school is involved, and no organization named here endorses this page.',
 'fr': 'Ce n’est pas un cours universitaire : il ne donne aucun crédit académique, aucun établissement n’y participe, et aucune organisation citée ici ne cautionne cette page.',
 'es': 'No es un curso universitario, no otorga créditos académicos, ninguna institución participa, y ninguna organización nombrada aquí respalda esta página.',
 'ar': 'هذا ليس مقررًا جامعيًا، ولا يمنح ساعات معتمدة، ولا تشارك فيه أي مؤسسة تعليمية، ولا تتبنى أي منظمة مذكورة هنا هذه الصفحة.',
 'it': 'Non è un corso universitario, non dà crediti accademici, nessuna scuola è coinvolta, e nessuna organizzazione citata qui approva questa pagina.',
 'he': 'זה אינו קורס אוניברסיטאי, אינו מעניק נקודות זכות אקדמיות, אף מוסד לימודים אינו מעורב בו, ואף ארגון המוזכר כאן אינו ממליץ על דף זה.',
}
AERO_SAVED = {
 'en': ' Your progress is saved only in this browser.',
 'fr': ' Votre progression est enregistrée uniquement dans ce navigateur.',
 'es': ' Tu progreso se guarda solo en este navegador.',
 'ar': ' يُحفظ تقدّمك في هذا المتصفح فقط.',
 'it': ' I tuoi progressi sono salvati solo in questo browser.',
 'he': ' ההתקדמות שלכם נשמרת רק בדפדפן הזה.',
}
GLANCE_CSS = ('<style id="aero101-glance">.crs-need{margin:.2rem 0 .75rem;padding:.45rem .8rem;border-radius:14px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.05);font-size:.95rem;line-height:1.35}'
              '.crs-need b{font-weight:800}.crs-unitscan{margin:0 0 1.1rem}</style>')
UPDATED = '2026-11-01'
VERSION = '2026.11.01'
DATE_LABEL = {
 '2026-11-01': {'en': 'November 1, 2026', 'fr': '1er novembre 2026', 'es': '1 de noviembre de 2026', 'ar': '1 نوفمبر 2026', 'it': '1 novembre 2026', 'he': '1 בנובמבר 2026'},
 '2026-11-18': {'en': 'November 18, 2026', 'fr': '18 novembre 2026', 'es': '18 de noviembre de 2026', 'ar': '18 نوفمبر 2026', 'it': '18 novembre 2026', 'he': '18 בנובמבר 2026'},
 '2026-11-21': {'en': 'November 21, 2026', 'fr': '21 novembre 2026', 'es': '21 de noviembre de 2026', 'ar': '21 نوفمبر 2026', 'it': '21 novembre 2026', 'he': '21 בנובמבר 2026'},
 '2026-11-25': {'en': 'November 25, 2026', 'fr': '25 novembre 2026', 'es': '25 de noviembre de 2026', 'ar': '25 نوفمبر 2026', 'it': '25 novembre 2026', 'he': '25 בנובמבר 2026'},
}
FACT_NOTE = {
 'recheck': {
  'en': 'Worked numbers on this page were rechecked November 18, 2026.',
  'fr': 'Les nombres calculés de cette page ont été revérifiés le 18 novembre 2026.',
  'es': 'Los números resueltos de esta página se volvieron a comprobar el 18 de noviembre de 2026.',
  'ar': 'أُعيد التحقق من الأرقام المحلولة في هذه الصفحة في 18 نوفمبر 2026.',
  'it': 'I numeri svolti in questa pagina sono stati ricontrollati il 18 novembre 2026.',
  'he': 'המספרים הפתורים בעמוד זה נבדקו מחדש ב-18 בנובמבר 2026.',
 },
 'recheck21': {
  'en': 'Worked numbers on this page were rechecked November 21, 2026.',
  'fr': 'Les nombres calculés de cette page ont été revérifiés le 21 novembre 2026.',
  'es': 'Los números resueltos de esta página se volvieron a comprobar el 21 de noviembre de 2026.',
  'ar': 'أُعيد التحقق من الأرقام المحلولة في هذه الصفحة في 21 نوفمبر 2026.',
  'it': 'I numeri svolti in questa pagina sono stati ricontrollati il 21 novembre 2026.',
  'he': 'המספרים הפתורים בעמוד זה נבדקו מחדש ב-21 בנובמבר 2026.',
 },
 'map': {
  'en': 'Outcomes map and readings list added November 18, 2026. Worked numbers on this page were last checked November 1, 2026.',
  'fr': 'La carte des objectifs et la liste de lectures ont été ajoutées le 18 novembre 2026. Les nombres calculés de cette page ont été vérifiés pour la dernière fois le 1er novembre 2026.',
  'es': 'El mapa de resultados y la lista de lecturas se añadieron el 18 de noviembre de 2026. Los números resueltos de esta página se comprobaron por última vez el 1 de noviembre de 2026.',
  'ar': 'أُضيفت خريطة النواتج وقائمة القراءات في 18 نوفمبر 2026. آخر تحقق من الأرقام المحلولة في هذه الصفحة كان في 1 نوفمبر 2026.',
  'it': 'La mappa degli obiettivi e l’elenco delle letture sono stati aggiunti il 18 novembre 2026. I numeri svolti in questa pagina sono stati controllati l’ultima volta il 1 novembre 2026.',
  'he': 'מפת התוצרים ורשימת הקריאה נוספו ב-18 בנובמבר 2026. המספרים הפתורים בעמוד זה נבדקו לאחרונה ב-1 בנובמבר 2026.',
 },
}
def stamp_of(C):
    updated = getattr(C, 'UPDATED', UPDATED)
    version = getattr(C, 'VERSION', VERSION)
    return updated, version, DATE_LABEL[updated][LANG]
def abs_page(page, frag=''):
    return 'https://www.savingplanets.com/' + ('' if LANG == 'en' else LANG + '/') + page + frag
def gc_slot(url, title, body, kind='assignment'):
    return (f'<div class="gc-slot" data-gc-type="{html.escape(kind)}" data-gc-url="{html.escape(url, quote=True)}" '
            f'data-gc-title="{html.escape(title, quote=True)}" data-gc-body="{html.escape(body, quote=True)}"></div>')
def gear_heading(C):
    return 'Lab equipment (for the wet labs)' if C.ID in WET_IDS else None
def outcomes_block(C):
    # Cells are translated once here. table() would translate them again.
    # AERO 101 says the practice sentence once. Other courses keep it in every row.
    practiced = _('Practice and quiz in this unit. The exam sets are at the end of the course.')
    aero = getattr(C, 'ID', '') == 'aero101'
    cols = ['Outcome', 'Taught in'] if aero else ['Outcome', 'Taught in', 'Practiced in']
    head = ''.join(f'<th scope="col">{esc(x)}</th>' for x in cols)
    body = []
    for i, u in enumerate(C.UNITS, 1):
        where = _('Unit {n}').replace('{n}', str(i)) if aero else _('Unit {n}').replace('{n}', str(i)) + ': ' + _(u['title'])
        for obj in u['objectives']:
            cells = (_(obj), where) if aero else (_(obj), where, practiced)
            body.append('<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in cells) + '</tr>')
    intro = html.escape(practiced) if aero else esc('This table maps each outcome to the unit that teaches it and to the practice on this page.')
    return (f'<section id="outcomes"><h2>{esc("Learning outcomes")}</h2>'
            f'<p>{intro}</p>'
            f'<div class="crs-tw"><table class="crs-tbl"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'
            + (AR.alignment(LANG) if aero else '')
            + top() + '</section>')
def readings_block(C):
    lead = AF.readings_inner(LANG) if getattr(C, 'ID', '') == 'aero101' else ''
    parts = [f'<section id="readings"><h2>{esc("Readings")}</h2>{lead}<p>{esc("Each link is a free public source already used in this course. Listing a source is not an endorsement.")}</p>']
    # AERO 101 keeps only the textbook here. Each unit's own list lives in that unit, under Go Deeper.
    if getattr(C, 'ID', '') != 'aero101':
        for i, u in enumerate(C.UNITS, 1):
            title = _('Unit {n}').replace('{n}', str(i)) + ': ' + _(u['title'])
            parts.append(f'<h3>{html.escape(title)}</h3><ul class="crs-res">' + ''.join(f'<li>{ext(t, h)}: {esc(d)}</li>' for t, h, d in u['res']) + '</ul>')
    # AERO 101 already lists these four links under #ptable. Other courses keep the copy in Readings.
    if getattr(C, 'PTABLE', None) and getattr(C, 'ID', '') != 'aero101':
        parts.append(f'<h3>{esc(getattr(C, "REF_TITLE", "Periodic table"))}</h3><ul class="crs-res">' + ''.join(f'<li>{ext(t, h)}: {esc(d)}</li>' for t, h, d in C.PTABLE) + '</ul>')
    parts.append(top() + '</section>')
    return ''.join(parts)
def notes_block(C):
    notes = getattr(C, 'SESSION_NOTES', None)
    if not notes: return ''
    items = []
    for unit, topic, url in notes:
        label = _('Unit {n}').replace('{n}', str(next(i for i, u in enumerate(C.UNITS, 1) if u['id'] == unit)))
        items.append(f'<li><a href="#{html.escape(unit)}">{html.escape(label)}: {html.escape(_("Session notes on this page"))}</a>. '
                     f'<a href="{html.escape(url)}" rel="noopener" lang="en">{html.escape(topic)}</a></li>')
    return (f'<section id="notes"><h2>{esc("Lecture notes by session")}</h2>'
            f'<p>{esc("The notes for each unit are on this page. Where MIT OpenCourseWare published a matching note, it is linked. Those notes are CC BY-NC-SA 4.0. Saving Planets is not affiliated with or endorsed by MIT.")}</p>'
            f'<ul class="crs-res">{"".join(items)}</ul>' + top() + '</section>')
def psets_block(C):
    parts = [f'<section id="psets"><h2>{esc("Problem sets with solutions")}</h2>'
             f'<p>{esc("These are the practice problems from each unit, with the solution. Every number is recomputed by the course check before the page is published. The step-by-step worked examples sit in the unit notes.")}</p>']
    gc_body = _('Free Saving Planets problem set. No university credit. Listing a source is not an endorsement.')
    for i, u in enumerate(C.UNITS, 1):
        title = _('Problem set {n}').replace('{n}', str(i)) + ': ' + _(u['title'])
        parts.append(f'<h3 id="{u["id"]}-ps">{html.escape(title)}</h3><ol class="crs-prac">' + ''.join(
            f'<li><p>{esc(q)}</p><details><summary>{esc("Show full solution")}</summary><p class="crs-ans"><strong>{esc("Answer:")}</strong> {esc(a)}</p></details></li>'
            for q, a in u['practice']) + '</ol>')
        parts.append(f'<p><a href="#{u["id"]}">{esc("Worked examples for this set")}</a></p>')
        parts.append(gc_slot(abs_page(C.PAGE, f'#{u["id"]}-ps'), title, gc_body, 'assignment'))
    parts.append(top() + '</section>')
    return ''.join(parts)
FURTHER_T = {
 'en': {'h': 'Go further: university resources', 'p': 'These cover topics beyond or newer than this course.'},
 'fr': {'h': 'Aller plus loin : ressources universitaires', 'p': 'Ces pages couvrent des sujets au-delà de ce cours, ou plus récents.'},
 'es': {'h': 'Ve más allá: recursos universitarios', 'p': 'Estas páginas cubren temas más allá de este curso, o más recientes.'},
 'ar': {'h': 'تعمّق: مصادر جامعية', 'p': 'تغطي هذه الصفحات موضوعات أبعد من هذا المقرر، أو أحدث منه.'},
 'it': {'h': 'Vai oltre: risorse universitarie', 'p': 'Queste pagine coprono argomenti oltre questo corso, o più recenti.'},
 'he': {'h': 'להעמיק: מקורות אוניברסיטאיים', 'p': 'העמודים האלה מכסים נושאים מעבר לקורס הזה, או חדשים יותר.'},
}
def further_block(C):
    items = getattr(C, 'FURTHER', None)
    if not items: return ''
    t = FURTHER_T[LANG]
    lis = ''.join(f'<li><a href="{html.escape(url, quote=True)}" rel="noopener">{html.escape(label)}</a></li>' for label, url in items)
    return (f'<!-- FURTHER:START --><section id="further"><h2>{html.escape(t["h"])}</h2><p>{html.escape(t["p"])}</p>'
            f'<ul class="crs-res">{lis}</ul>' + top() + '</section><!-- FURTHER:END -->')
def glance_block(C):
    label, rest = AERO_NEED[LANG].split(':', 1)
    return (GLANCE_CSS + f'<p class="crs-need" id="glance"><b>{html.escape(label)}:</b>{html.escape(rest)}</p>')
def _week_num(label):
    m = re.search(r'\d+(?:–\d+)?', label)
    num = m.group(0) if m else label
    if '–' in num:
        return f'<bdi dir="ltr">{html.escape(num)}</bdi>'
    return html.escape(num)
def unit_index(C):
    t = AERO_UI[LANG]
    week, unit, desc = esc('Week'), esc('Unit'), html.escape(t['line'])
    head = f'<th scope="col">{week}</th><th scope="col">{unit}</th><th scope="col">{desc}</th>'
    rows = []
    for u in C.UNITS:
        rows.append(
            f'<tr><td data-label="{week}">{_week_num(_(u["weeks"]))}</td>'
            f'<td data-label="{unit}"><a href="#{u["id"]}">{esc(u["title"])}</a></td>'
            f'<td data-label="{desc}">{esc(u["summary"])}</td></tr>')
    return (f'<details class="crs-units" id="unit-index"><summary><h2 class="crs-ocw-h">{esc("Units")}</h2></summary>'
            f'<div class="crs-tw"><table class="crs-tbl"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></details>')
def course_page(C):
    texs = [t for u in C.UNITS for t, _c in u['eqs']] + [L['eq'][0] for L in C.LABS] + C.FORMULAS
    K = katex(texs)
    toc = [('about', 'About this course'), ('start', 'Before you start'), ('schedule', '15-week schedule'), ('outcomes', 'Learning outcomes'), ('readings', 'Readings')]
    if getattr(C, 'SESSION_NOTES', None): toc.append(('notes', 'Lecture notes by session'))
    toc += [('progress', 'Your progress')] + \
          [(u['id'], _('Unit {n}').replace('{n}', str(i)) + ': ' + _(u['title'])) for i, u in enumerate(C.UNITS, 1)] + \
          [('psets', 'Problem sets with solutions'), ('lab', 'Lab'), ('exam', 'Exams with solutions'), ('formulas', 'Formula sheet'), ('ptable', getattr(C, 'REF_TITLE', 'Periodic table')), ('glossary', 'Glossary'), ('rubric', 'Self-assessment')]
    if getattr(C, 'FURTHER', None): toc.append(('further', FURTHER_T[LANG]['h']))
    names0 = {u['id'] for u in C.UNITS}
    quiet = getattr(C, 'ID', '') == 'aero101'
    o = [hero(C.TITLE, C.TAGLINE, AR.box(LANG, quality=True) if quiet else ''), f'<div class="crs" data-course="{C.ID}"{ui_attr()}{dir_attr()}>']
    if not quiet:
        updated, version, when = stamp_of(C)
        note_key = 'recheck21' if updated == '2026-11-21' else 'recheck' if updated == '2026-11-18' else 'map'
        o += [f'<p class="crs-crumb"><a href="{HUB}">{esc("Undergraduate Studies")}</a> › {esc(C.CODE)}</p>',
              f'<p class="crs-updated">{html.escape(UPD_T[LANG])}: <time datetime="{updated}">{html.escape(when)}</time> · {html.escape(VER_T[LANG])} {html.escape(version)}</p>',
              f'<p class="crs-check">{html.escape(FACT_NOTE[note_key][LANG])}</p>']
        if getattr(C, 'CREDIT', None): o.append(credit_p(C.CREDIT))
        o.append(AR.box(LANG, when_iso=updated, when_label=when))
    else:
        o.append(glance_block(C))
    if not quiet:
        o.append(f'<div class="crs-toc" role="navigation" aria-label="{esc("On this page")}"><ul>' + ''.join(f'<li><a href="#{a}">{html.escape(b if a in names0 or a == "further" else _(b))}</a></li>' for a, b in toc) + '</ul></div>')
    o.append(f'<p class="crs-tools"><button type="button" class="btn crs-btn" data-print>{esc("Print this page")}</button>' + pdf_link(C) + '</p>')
    scope = SCOPE_T[LANG].replace('{n}', str(len(C.UNITS))).replace('{m}', str(len(C.LABS)))
    about = [_(x) for x in C.ABOUT]
    if getattr(C, 'ID', '') == 'aero101' and about:
        about[-1] = about[-1].replace(AERO_SAVED[LANG], '')
    scope_p = '' if quiet else f'<p class="crs-scope">{html.escape(scope)}</p>'
    if quiet:
        o.append('<span id="about"></span>')
    else:
        o.append(f'<section id="about"><h2>{esc("About this course")}</h2><div class="crs-disc">' + ''.join(f'<p>{html.escape(x)}</p>' for x in about)
                 + scope_p + f'<p class="crs-check">{html.escape(CHK_T[LANG])}</p></div>'
                 f'<div class="crs-planet"><h3>{esc("How this course helps save the planet")}</h3>' + ''.join(f'<p>{esc(x)}</p>' for x in C.COURSE_PLANET) + '</div>' + top() + '</section>')
    if quiet:
        o.append('<span id="start"></span><span id="schedule"></span>')
    else:
        pre = f'<h3>{esc("Prerequisites")}</h3>' + ul(C.PREREQS)
        o.append(f'<section id="start"><h2>{esc("Before you start")}</h2>' + pre + f'<h3>{esc("How to study")}</h3>' + ul(C.STUDY)
                 + (f'<h3>{esc(gear_heading(C))}</h3>' if gear_heading(C) else f'<h3>{html.escape(GEAR_T[LANG])}</h3>')
                 + ul(C.LAB_GEAR) + top() + '</section>')
        names = {u['id']: u['title'] for u in C.UNITS}; names['exam'] = 'Review'
        sched_lead = f'<p>{esc("About 6 to 9 hours a week: reading, practice problems and, in lab weeks, the lab.")}</p><p>{esc("This table is the course calendar.")}</p>'
        o.append(f'<section id="schedule"><h2>{esc("Suggested 15-week schedule")}</h2>' + sched_lead
                 + table(['Week', 'Unit', 'Topics', 'Reading'], [[str(w), names[u], t, r] for w, u, t, r in C.SCHEDULE]) + top() + '</section>')
    if quiet:
        names = {u['id']: u['title'] for u in C.UNITS}; names['exam'] = 'Review'
    o.append(outcomes_block(C))
    o.append(readings_block(C))
    o.append(notes_block(C))
    if quiet:
        o.append('<span id="progress"></span>')
    else:
        o.append(f'<section id="progress"><h2>{esc("Your progress")}</h2><p>{esc("Tick units and labs as you finish them, and take the quizzes. Progress and quiz scores are saved only in this browser, never sent to us.")}</p>'
                 f'<div class="crs-prog" aria-live="polite"><progress max="100" value="0"></progress><p class="crs-prog-t">{esc("Turn on JavaScript to track progress.")}</p></div>'
                 f'<p><button type="button" class="btn crs-btn crs-reset" data-reset>{esc("Reset my progress")}</button></p>' + top() + '</section>')
    if getattr(C, 'ID', '') == 'aero101': o.append(unit_index(C))
    o += [unit(C, K, i, u) for i, u in enumerate(C.UNITS, 1)]
    o.append(psets_block(C))
    o.append(f'<section id="lab"><h2>{esc(C.LAB_TITLE) if getattr(C, "LAB_TITLE", None) else html.escape(_("The lab ({code})").replace("{code}", getattr(C, "LAB_NAME", C.CODE.split(" + ")[-1])))}</h2>' + ''.join(f'<p>{esc(x)}</p>' for x in C.LAB_INTRO)
             + f'<p class="crs-src">{esc("Safety reference:")} {ext(*C.SAFETY_SRC)}</p>' + ''.join(lab(C, K, L) for L in C.LABS) + top() + '</section>')
    ex = [f'<section id="exam"><h2>{esc("Exams with solutions")}</h2><p>{esc("Time yourself: about 10 minutes per problem. Then compare with the full solutions.")}</p>',
          gc_slot(abs_page(C.PAGE, '#exam'), _(C.TITLE) + ' — ' + _('Exams with solutions'),
                  _('Free Saving Planets exam. No university credit. Listing a source is not an endorsement.'), 'assignment')]
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
    o.append(further_block(C))
    o.append('</div>')
    extra = head()
    if getattr(C, 'ID', '') == 'aero101':
        # Same column rules as courses.css, in the head, so the deferred stylesheet does not shift the page.
        extra += ('<style id="aero101-lock">.crs{max-width:980px;margin:0 auto;padding:1rem 1.25rem 2.5rem;line-height:1.65}'
                  '.crs h2{margin-top:2.4rem}.crs h3{margin:1.4rem 0 .45rem;font-size:1.12rem}'
                  '.crs-note{font-size:.9rem;font-style:italic}.crs-crumb{font-size:.9rem}'
                  '.crs-card{border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:1rem 1.2rem;margin:1rem 0;background:rgba(255,255,255,.05)}'
                  '.crs-toc ul{display:flex;flex-wrap:wrap;gap:.45rem;list-style:none;padding:0;margin:1rem 0}'
                  '.crs-toc a{display:inline-flex;align-items:center;min-height:44px;padding:0 .9rem;border:1px solid rgba(255,255,255,.28);border-radius:999px;text-decoration:none;color:inherit;background:rgba(255,255,255,.05)}'
                  + AW.CSS + AF.CSS + AR.CSS + NF.CSS + AB.CHECK_CSS + '</style>\n' + AW.JS + '\n'
                  + f'<script src="{pre()}{NF.JS}" defer></script>\n'
                  + f'<script src="{pre()}assets/courses/check.js?v=20261128d" defer></script>\n')
    page = BL.shell(LANG, C.PAGE, _(C.TITLE) + ' (' + C.CODE + ')', _(C.DESC), ''.join(o), extra_head=extra, ld_type='Course', tail=tail())
    return aero_foot(page, C) if quiet else page

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

def keep_head(new, path, alt, page):
    """A rebuild starts from the Kids Map head. Put back this page's critical CSS, Hebrew alternate, and share-card alt."""
    old = open(path, encoding='utf8').read() if os.path.exists(path) else ''
    crit = re.search(r'<!-- CRIT:START -->.*?<!-- CRIT:END -->', old, re.S)
    if crit:
        if '<!-- CRIT:START -->' in new:
            new = re.sub(r'<!-- CRIT:START -->.*?<!-- CRIT:END -->', lambda _m: crit.group(0), new, count=1, flags=re.S)
        else:
            new = new.replace('</head>', crit.group(0) + '\n</head>', 1)
    head, sep, rest = new.partition('</head>')
    if sep and 'hreflang="he"' not in head and (LANG == 'he' or os.path.exists('he/' + page)):
        link = f'\n<link rel="alternate" hreflang="he" href="https://www.savingplanets.com/he/{page}">'
        head = head.replace('<link rel="alternate" hreflang="x-default"', link + '\n<link rel="alternate" hreflang="x-default"', 1)
        new = head + sep + rest
    alt_esc = html.escape(alt, quote=True)
    if 'property="og:image:alt"' in new:
        new = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', lambda m: m.group(1) + alt_esc + '"', new, count=1)
    else:
        new = re.sub(r'(<meta property="og:image" content="[^"]*">)', lambda m: m.group(1) + '\n<meta property="og:image:alt" content="' + alt_esc + '">', new, count=1)
    return new

# RTL pages (ar, he): plain-text formulas inside RTL sentences (e.g. "f(x) = x² + 1", "∫ 2x dx") get <bdi dir="ltr"> so the
# bidi algorithm cannot reorder their operators. Text nodes only, inside the course/hub body; KaTeX blocks (.crs-math), script/style/pre/code skipped.
_FTOK = r"(?:&(?:lt|gt|amp|#x27|quot);|[A-Za-z0-9()\[\]{}+\-−–×÷·*/=<>≤≥≈≠^_.,:;′'|!√∫∑∏∂∞→←↔∈≡%°\u0370-\u03ff\u00c0-\u00ff\u0100-\u024f\u1e00-\u1eff⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾ⁿ₀₁₂₃₄₅₆₇₈₉₊₋ₙₓᵢₘₖₐₑₒₗₛ±⌀∓µ‰Å\u02b0-\u02ff\u1d2c-\u1dbf\u2070-\u209f½¼¾⅓⅔⅛ ])"
_FRUN = re.compile(_FTOK + '+')
_FOP = re.compile(r"&lt;|&gt;|[=+−×÷/^<>≤≥≈≠√∫∑∏∂∞→⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ₀₁₂₃₄₅₆₇₈₉ₙₓᵢ′½±⌀∓Ø\u02b0-\u02ff]|\w\(|\w\[|[*%]|\d\s*[-–]\s*\d|\d\s?(?:µm|nm|mm|km|kΩ|µF|µT|µC|°C|kHz|MHz|Hz|%)|\d\s?[A-Za-zµΩ°Å][A-Za-z]*(?:[/·][A-Za-zµΩ°]+)*[²³]?(?![A-Za-z\d])")  # number + unit (50000 h, 8760 h, 1.225 kg/m³): RTL must not flip it to "h 50000"
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

COMPARE = {
 'h': {'en': 'How this track compares', 'fr': 'Comment ce parcours se compare', 'es': 'Cómo se compara este itinerario', 'ar': 'كيف يُقارَن هذا المسار', 'it': 'Come si confronta questo percorso', 'he': 'איך המסלול הזה משתווה'},
 'p1': {
  'en': 'This note compares our free four-year track with the Bachelor of Science in Aerospace Engineering at Embry-Riddle Aeronautical University, Daytona Beach, using that university’s public department page and catalog. Saving Planets is not part of Embry-Riddle, is not affiliated with it, and is not endorsed by it. This track gives no Embry-Riddle credit and no credit at any school.',
  'fr': 'Cette note compare notre parcours gratuit de quatre ans avec le Bachelor of Science in Aerospace Engineering d’Embry-Riddle Aeronautical University, à Daytona Beach, d’après la page du département et le catalogue publics de cette université. Saving Planets ne fait pas partie d’Embry-Riddle, n’y est pas affilié et n’est pas approuvé par elle. Ce parcours ne donne aucun crédit Embry-Riddle ni aucun crédit dans une école.',
  'es': 'Esta nota compara nuestro itinerario gratuito de cuatro años con el Bachelor of Science in Aerospace Engineering de Embry-Riddle Aeronautical University, en Daytona Beach, según la página del departamento y el catálogo públicos de esa universidad. Saving Planets no forma parte de Embry-Riddle, no está afiliado a ella y no cuenta con su aval. Este itinerario no da crédito de Embry-Riddle ni crédito en ninguna escuela.',
  'ar': 'تقارن هذه الملاحظة مسارنا المجاني لأربع سنوات ببكالوريوس هندسة الطيران والفضاء في جامعة إمبري-ريدل للطيران، حرم دايتونا بيتش، بالاعتماد على صفحة القسم والفهرس العامين للجامعة. Saving Planets ليست جزءًا من إمبري-ريدل، وغير تابعة لها، وغير مزكّاة منها. لا يمنح هذا المسار أي ساعات من إمبري-ريدل ولا أي ساعات في أي مدرسة.',
  'it': 'Questa nota confronta il nostro percorso gratuito di quattro anni con il Bachelor of Science in Aerospace Engineering della Embry-Riddle Aeronautical University, a Daytona Beach, usando la pagina del dipartimento e il catalogo pubblici di quell’università. Saving Planets non fa parte di Embry-Riddle, non è affiliata e non è approvata da essa. Questo percorso non dà crediti Embry-Riddle né crediti in alcuna scuola.',
  'he': 'ההערה הזו משווה את המסלול החינמי שלנו לארבע שנים לתואר הראשון בהנדסת אווירונאוטיקה וחלל באוניברסיטת אמברי-רידל לאווירונאוטיקה, דייטונה ביץ׳, לפי עמוד המחלקה והקטלוג הפומביים שלה. Saving Planets אינה חלק מאמברי-רידל, אינה מסונפת אליה ואינה מאושרת על ידה. המסלול הזה אינו נותן נקודות זכות של אמברי-רידל ואינו נותן נקודות זכות בשום מוסד.',
 },
 'p2': {
  'en': 'The Daytona Beach department says it is the largest of its kind in the country, with more than 2,400 students in its B.S., M.S. and Ph.D. programs, and that students use labs, design projects and a year-long capstone.',
  'fr': 'Le département de Daytona Beach indique qu’il est le plus grand du pays dans son domaine, avec plus de 2 400 étudiants dans ses programmes de B.S., M.S. et Ph.D., et que les étudiants utilisent des laboratoires, des projets de conception et un projet de fin d’études sur un an.',
  'es': 'El departamento de Daytona Beach dice que es el más grande de su tipo en el país, con más de 2,400 estudiantes en sus programas de B.S., M.S. y Ph.D., y que el alumnado usa laboratorios, proyectos de diseño y un proyecto final de un año.',
  'ar': 'يقول قسم دايتونا بيتش إنه الأكبر من نوعه في البلاد، مع أكثر من 2,400 طالب في برامج البكالوريوس والماجستير والدكتوراه، وإن الطلاب يستخدمون المختبرات ومشاريع التصميم ومشروع تخرج يمتد عامًا.',
  'it': 'Il dipartimento di Daytona Beach scrive di essere il più grande del paese nel suo campo, con più di 2.400 studenti nei programmi di B.S., M.S. e Ph.D., e che gli studenti usano laboratori, progetti di progettazione e un progetto finale di un anno.',
  'he': 'המחלקה בדייטונה ביץ׳ כותבת שהיא הגדולה מסוגה במדינה, עם יותר מ-2,400 סטודנטים בתוארי B.S.‏, M.S. ו-Ph.D.‏, ושהסטודנטים עובדים במעבדות, בפרויקטי תכנון ובפרויקט גמר של שנה.',
 },
 'p3': {
  'en': 'The Daytona Beach catalog lists that degree as 129 credits: general education 42, core 47, and a concentration of 40. It says a student must earn a cumulative GPA of 2.5 or higher and complete required courses with a grade of C or better to remain on track.',
  'fr': 'Le catalogue de Daytona Beach indique ce diplôme à 129 crédits : formation générale 42, tronc commun 47 et une concentration de 40. Il précise qu’un étudiant doit obtenir une moyenne cumulative d’au moins 2,5 et réussir les cours requis avec une note de C ou mieux pour rester dans le parcours.',
  'es': 'El catálogo de Daytona Beach indica ese grado con 129 créditos: educación general 42, núcleo 47 y una concentración de 40. Dice que un estudiante debe obtener un promedio acumulado de 2.5 o más y aprobar los cursos requeridos con una nota de C o mejor para seguir en el plan.',
  'ar': 'يذكر فهرس دايتونا بيتش أن الدرجة 129 ساعة: التعليم العام 42، والمتطلبات الأساسية 47، والتخصص 40. ويقول إن على الطالب تحقيق معدل تراكمي 2.5 أو أعلى وإكمال المقررات المطلوبة بدرجة C أو أفضل ليبقى على المسار.',
  'it': 'Il catalogo di Daytona Beach indica quel titolo a 129 crediti: formazione generale 42, nucleo 47 e un indirizzo di 40. Dice che uno studente deve avere una media cumulativa di almeno 2,5 e completare i corsi richiesti con un voto di C o superiore per restare in regola.',
  'he': 'הקטלוג של דייטונה ביץ׳ מציין את התואר כ-129 נקודות זכות: השכלה כללית 42, ליבה 47 והתמחות 40. הוא כותב שסטודנט צריך ממוצע מצטבר של 2.5 לפחות וציון C או יותר בקורסי החובה כדי להישאר במסלול.',
 },
 'p4': {
  'en': 'On the Aeronautics concentration, the catalog lists AERO 307 Incompressible Aerodynamics, AERO 308 Compressible Aerodynamics, AERO 314 Experimental Aerodynamics with AERO 314L, AERO 403 Jet Propulsion, AERO 413 Airplane Stability and Control, AERO 432 Flight Dynamics and Control, and the design pair AERO 420 Aircraft Preliminary Design and AERO 421 Aircraft Detail Design. On the Astronautics concentration it lists AERO 414 Space Propulsion, AERO 426 Spacecraft Attitude Dynamics, and the design pair AERO 427 and AERO 445. General education includes COMM 122 English Composition, COMM 221 Technical Communication and COMM 219 Speech.',
  'fr': 'Dans la concentration Aéronautique, le catalogue indique AERO 307 Incompressible Aerodynamics, AERO 308 Compressible Aerodynamics, AERO 314 Experimental Aerodynamics avec AERO 314L, AERO 403 Jet Propulsion, AERO 413 Airplane Stability and Control, AERO 432 Flight Dynamics and Control, et la paire de conception AERO 420 Aircraft Preliminary Design et AERO 421 Aircraft Detail Design. Dans la concentration Astronautique, il indique AERO 414 Space Propulsion, AERO 426 Spacecraft Attitude Dynamics, et la paire AERO 427 et AERO 445. La formation générale comprend COMM 122 English Composition, COMM 221 Technical Communication et COMM 219 Speech.',
  'es': 'En la concentración de Aeronáutica, el catálogo incluye AERO 307 Incompressible Aerodynamics, AERO 308 Compressible Aerodynamics, AERO 314 Experimental Aerodynamics con AERO 314L, AERO 403 Jet Propulsion, AERO 413 Airplane Stability and Control, AERO 432 Flight Dynamics and Control, y el par de diseño AERO 420 Aircraft Preliminary Design y AERO 421 Aircraft Detail Design. En Astronáutica incluye AERO 414 Space Propulsion, AERO 426 Spacecraft Attitude Dynamics y el par AERO 427 y AERO 445. La educación general incluye COMM 122 English Composition, COMM 221 Technical Communication y COMM 219 Speech.',
  'ar': 'في تركيز الطيران، يذكر الفهرس AERO 307 وAERO 308 وAERO 314 مع مختبر AERO 314L وAERO 403 Jet Propulsion وAERO 413 وAERO 432 وزوج التصميم AERO 420 وAERO 421. وفي تركيز الملاحة الفضائية يذكر AERO 414 Space Propulsion وAERO 426 وزوج التصميم AERO 427 وAERO 445. ويشمل التعليم العام COMM 122 وCOMM 221 Technical Communication وCOMM 219 Speech.',
  'it': 'Nell’indirizzo Aeronautics il catalogo elenca AERO 307 Incompressible Aerodynamics, AERO 308 Compressible Aerodynamics, AERO 314 Experimental Aerodynamics con AERO 314L, AERO 403 Jet Propulsion, AERO 413 Airplane Stability and Control, AERO 432 Flight Dynamics and Control, e la coppia di progetto AERO 420 Aircraft Preliminary Design e AERO 421 Aircraft Detail Design. Nell’indirizzo Astronautics elenca AERO 414 Space Propulsion, AERO 426 Spacecraft Attitude Dynamics e la coppia AERO 427 e AERO 445. La formazione generale include COMM 122 English Composition, COMM 221 Technical Communication e COMM 219 Speech.',
  'he': 'במסלול האווירונאוטיקה הקטלוג מונה את AERO 307,‏ AERO 308,‏ AERO 314 עם המעבדה AERO 314L,‏ AERO 403 Jet Propulsion,‏ AERO 413,‏ AERO 432, ואת זוג התכן AERO 420 ו-AERO 421. במסלול האסטרונאוטיקה הוא מונה את AERO 414 Space Propulsion,‏ AERO 426, ואת זוג התכן AERO 427 ו-AERO 445. ההשכלה הכללית כוללת את COMM 122,‏ COMM 221 Technical Communication ו-COMM 219 Speech.',
 },
 'p5': {
  'en': 'Our Propulsion course (AERO 410) covers jet and rocket topics that the catalog splits into AERO 403 Jet Propulsion and AERO 414 Space Propulsion. Aerodynamics I follows the topics of AERO 307 and AERO 308. We do not have an experimental aerodynamics lab matching AERO 314 and AERO 314L. Flight Dynamics and Controls follows the topics of AERO 413 and AERO 432. Our capstone is one self-study course, not the catalog’s year-long pair AERO 420 and AERO 421. We have no course matching COMM 122, COMM 221 or COMM 219, so technical writing and speech are a gap. Use this track as free practice beside a degree, not as a replacement for one.',
  'fr': 'Notre cours de propulsion (AERO 410) couvre des sujets de jets et de fusées que le catalogue sépare en AERO 403 Jet Propulsion et AERO 414 Space Propulsion. L’aérodynamique I suit les sujets d’AERO 307 et d’AERO 308. Nous n’avons pas de laboratoire d’aérodynamique expérimentale correspondant à AERO 314 et AERO 314L. Dynamique du vol et commandes suit les sujets d’AERO 413 et d’AERO 432. Notre projet de fin d’études est un seul cours en autonomie, pas la paire annuelle AERO 420 et AERO 421 du catalogue. Nous n’avons pas de cours correspondant à COMM 122, COMM 221 ou COMM 219 : la rédaction technique et l’expression orale sont donc un manque. Utilisez ce parcours comme une pratique gratuite à côté d’un diplôme, pas à la place d’un diplôme.',
  'es': 'Nuestro curso de propulsión (AERO 410) trata temas de motores a reacción y cohetes que el catálogo separa en AERO 403 Jet Propulsion y AERO 414 Space Propulsion. Aerodinámica I sigue los temas de AERO 307 y AERO 308. No tenemos un laboratorio de aerodinámica experimental equivalente a AERO 314 y AERO 314L. Dinámica y control de vuelo sigue los temas de AERO 413 y AERO 432. Nuestro proyecto final es un solo curso de autoestudio, no el par de un año AERO 420 y AERO 421 del catálogo. No tenemos un curso equivalente a COMM 122, COMM 221 o COMM 219, así que la redacción técnica y la expresión oral son una laguna. Usa este itinerario como práctica gratuita junto a un grado, no como sustituto.',
  'ar': 'يغطي مقرر الدفع لدينا (AERO 410) موضوعات المحركات النفاثة والصواريخ التي يفصلها الفهرس إلى AERO 403 وAERO 414. ويتبع مقرر الديناميكا الهوائية الأول موضوعات AERO 307 وAERO 308. وليس لدينا مختبر ديناميكا هوائية تجريبي يقابل AERO 314 وAERO 314L. ويتبع مقرر ديناميكا الطيران والتحكم موضوعات AERO 413 وAERO 432. ومشروع التخرج لدينا مقرر واحد للتعلم الذاتي، وليس زوج العام AERO 420 وAERO 421. وليس لدينا مقرر يقابل COMM 122 أو COMM 221 أو COMM 219، لذا تبقى الكتابة التقنية والخطابة فجوة. استخدم هذا المسار تدريبًا مجانيًا إلى جانب درجة، لا بدلًا منها.',
  'it': 'Il nostro corso di propulsione (AERO 410) tratta argomenti di getti e razzi che il catalogo divide in AERO 403 Jet Propulsion e AERO 414 Space Propulsion. Aerodinamica I segue gli argomenti di AERO 307 e AERO 308. Non abbiamo un laboratorio di aerodinamica sperimentale corrispondente ad AERO 314 e AERO 314L. Dinamica e controllo del volo segue gli argomenti di AERO 413 e AERO 432. Il nostro progetto finale è un solo corso di autoapprendimento, non la coppia annuale AERO 420 e AERO 421 del catalogo. Non abbiamo un corso corrispondente a COMM 122, COMM 221 o COMM 219: scrittura tecnica e discorso restano quindi un vuoto. Usa questo percorso come pratica gratuita accanto a un titolo, non al posto di un titolo.',
  'he': 'קורס ההנעה שלנו (AERO 410) מכסה נושאי סילון ורקטות שהקטלוג מפצל ל-AERO 403 Jet Propulsion ול-AERO 414 Space Propulsion. אווירודינמיקה א׳ עוקבת אחרי הנושאים של AERO 307 ו-AERO 308. אין לנו מעבדת אווירודינמיקה ניסויית שמקבילה ל-AERO 314 ול-AERO 314L. דינמיקת טיסה ובקרה עוקבת אחרי הנושאים של AERO 413 ו-AERO 432. פרויקט הגמר שלנו הוא קורס לימוד עצמי אחד, לא הזוג השנתי AERO 420 ו-AERO 421. אין לנו קורס שמקביל ל-COMM 122, ל-COMM 221 או ל-COMM 219, ולכן כתיבה טכנית ודיבור הם פער. השתמשו במסלול הזה כתרגול חינמי לצד תואר, לא במקום תואר.',
 },
}
def compare_block():
    L = LANG
    src1 = 'https://erau.edu/academics/colleges/daytona-beach-college-of-engineering/aerospace-engineering'
    src2 = 'https://catalog.erau.edu/programs/undergraduate/bachelors/aerospace-engineering/'
    return (f'<section id="compare"><h2>{html.escape(COMPARE["h"][L])}</h2>'
            f'<div class="crs-disc"><p>{html.escape(COMPARE["p1"][L])}</p></div>'
            f'<p>{html.escape(COMPARE["p2"][L])}</p><p>{html.escape(COMPARE["p3"][L])}</p><p>{html.escape(COMPARE["p4"][L])}</p><p>{html.escape(COMPARE["p5"][L])}</p>'
            f'<p class="crs-src"><a href="{src1}" rel="noopener">Embry-Riddle Daytona Beach Department of Aerospace Engineering</a> · '
            f'<a href="{src2}" rel="noopener">Daytona Beach aerospace engineering catalog</a></p>' + top() + '</section>')
def hub_body():
    # Nov 24 2026: one B.S. path, four tracks. New chrome strings live in study_aero_text (not _()).
    from study_hub import fragment, live_card
    missing = [cid for _y, cs in RM.YEARS for cid, _t, _d in cs if cid not in RM.ROLE]
    if missing: raise SystemExit('roadmap ROLE missing ' + ', '.join(missing))
    def live_for(cid, title, desc):
        m = LIVE.get(cid)
        if not m:
            return (f'<li class="crs-c"><span class="crs-badge soon">{esc("Coming soon")}</span>'
                    f'<h3>{esc(title)}</h3><p>{esc(desc)}</p></li>')
        if os.path.exists(out(m.PAGE)):
            return live_card(LANG, cid, title, desc, esc, m, m.PAGE, False)
        return live_card(LANG, cid, title, desc, esc, m, '../' + m.PAGE, True)
    return fragment(LANG, esc, live_for)

def hub_page():
    # The translation scan walks this. The published hub is spliced by install_hub so the existing head stays.
    return hub_body()

def install_hub():
    from study_hub import install, prepare_shell, retarget_page
    from study_aero_text import T as STUDY
    S = STUDY[LANG]
    prepare_shell(LANG)
    install(out(HUB), LANG, hub_body(), _('Back to top'), S['title'], S['desc'])
    retarget_page(out(HUB))

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
    new = json.dumps(cfg, ensure_ascii=False, indent=1) + '\n'
    old = open(p, encoding='utf8').read()
    if json.loads(new) != json.loads(old):
        open(p, 'w', encoding='utf8').write(new)

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
    if '--missing' in sys.argv: export_missing(sys.argv[sys.argv.index('--missing') + 1]); sys.exit(0)
    if '--import' in sys.argv: a = sys.argv.index('--import'); import_tsv(sys.argv[a + 1], sys.argv[a + 2]); sys.exit(0)
    if '--hub-only' in sys.argv:
        # Splice the study hub into the six Undergraduate_Studies.html files. Does not rebuild course pages and does not touch Propulsion.html.
        from study_hub import ensure_courses_css
        ensure_courses_css()
        langs = [l for l in LANGS if l in BUILD_LANGS and (l == 'en' or os.path.exists(l + '/Kids_Map.html'))]
        for LANG in langs:
            install_hub()
        _cat = importlib.util.spec_from_file_location('course_catalog', 'scripts/build-course-catalog.py')
        _catm = importlib.util.module_from_spec(_cat); _cat.loader.exec_module(_catm)
        _catm.apply()
        from study_hub import write_redirects
        write_redirects()
        print('hub only:', langs)
        sys.exit(0)
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
                if m.PAGE == 'Propulsion.html':
                    continue  # AERO 410 stays frozen while OER Commons review is open
                f = out(m.PAGE)
                if LANG == 'en' or LANG in DONE.get(m.ID, ()):
                    title = _(m.TITLE) + ' (' + m.CODE + ')'
                    open(f, 'w', encoding='utf8').write(keep_head(en_only(course_page(m)), f, title, m.PAGE))
                elif os.path.exists(f): os.remove(f)  # never leave a stale half-translated page
            if LANG == 'en' or not gaps.get('_hub', {}).get(LANG):
                install_hub()
    LANG = 'en'
    for cid, g in gaps.items():
        print(f'build-courses: {cid} not translated yet in', {l: len(v) for l, v in g.items()}, f'(English only there; run --missing {cid})')
    if '--strict' in sys.argv and gaps: raise SystemExit(1)
    teachers_links()
    relink(langs, gaps)
    import importlib.util as _iu
    _tg = _iu.spec_from_file_location('teacher_guide', 'scripts/build-teacher-guide.py')
    _tgm = _iu.module_from_spec(_tg); _tg.loader.exec_module(_tgm)
    _tgm.apply()
    _oc = _iu.spec_from_file_location('course_ocw', 'scripts/build-course-ocw.py')
    _ocm = _iu.module_from_spec(_oc); _oc.loader.exec_module(_ocm)
    _ocm.apply()
    _cat = _iu.spec_from_file_location('course_catalog', 'scripts/build-course-catalog.py')
    _catm = _iu.module_from_spec(_cat); _cat.loader.exec_module(_catm)
    _catm.apply()
    from study_hub import write_redirects
    write_redirects()
    _ex = _iu.spec_from_file_location('course_exports', 'scripts/build-course-exports.py')
    _exm = _iu.module_from_spec(_ex); _ex.loader.exec_module(_exm)
    _exm.apply()
    _fd = _iu.spec_from_file_location('course_folds', 'scripts/build-course-folds.py')
    _fdm = _iu.module_from_spec(_fd); _fd.loader.exec_module(_fdm)
    _fdm.apply()
    print('build-courses:', HUB, '+', [m.PAGE for m in MODS])
