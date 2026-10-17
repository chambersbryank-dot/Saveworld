#!/usr/bin/env python3
"""Batch B learning features (Oct 12). Idempotent; run from repo root.
  python3 scripts/build-batch-b.py             (BEFORE i18n-build) English solution pages get:
       - "Explain Like I'm 10" box (ELI10) built only from the page's own What / Why text (override: assets/data/eli10.json)
       - "For Teachers" box (3 discussion questions + print button) and "Cite This Page" (APA/MLA, filled by batchb.js)
     plus homepage audience paths, Glossary.html, Teachers.html, i18n strings, pages.txt, sitemap.
  python3 scripts/build-batch-b.py --glossary  (AFTER i18n-build) tap/hover definitions for the first occurrence of each
     glossary term on solution pages in en/fr/es/ar, and A-Z sorting of each language's Glossary.html.
     i18n-build.py / i18n-check.js strip this markup before translating/hashing, so it never makes pages stale.
Glossary data: assets/data/glossary.json.  Styles: batchb.css (incl. print sheet).  Script: batchb.js."""
import re, os, sys, json, html, importlib.util
rd = lambda f: open(f, encoding='utf8').read()
def wr(f, s):
    if not os.path.exists(f) or rd(f) != s: open(f, 'w', encoding='utf8').write(s); return 1
    return 0
esc = lambda s: html.escape(html.unescape(s), quote=True)  # idempotent: never double-encode
LANGS = ['fr', 'es', 'ar', 'it']
V = '20261015it'
CSS = f'<link rel="stylesheet" href="batchb.css?v={V}">'
JS = f'<script src="batchb.js?v={V}" defer></script>'
spec = importlib.util.spec_from_file_location('sol', 'scripts/build-solutions-index.py'); SOL = importlib.util.module_from_spec(spec); spec.loader.exec_module(SOL)
GL = json.load(open('assets/data/glossary.json', encoding='utf8'))['terms']


def write_generated(f, page):
    """Write a generated page only when its generated content changed (keeps later seo-fix/add-gtag edits, so translations stay current)."""
    import hashlib
    sig = hashlib.sha1(page.encode('utf8')).hexdigest()[:12]
    page = page.replace('</body>', f'<!-- GEN {sig} --></body>', 1)
    if os.path.exists(f) and f'<!-- GEN {sig} -->' in open(f, encoding='utf8').read(): return 0
    open(f, 'w', encoding='utf8').write(page); return 1

def solution_pages():
    seen, out = set(), []
    for f, name, items in SOL.hubs():
        for h, n in items:
            if h not in seen: seen.add(h); out.append((h, n, f, name))
    return out

# ---------- UI strings (merged into i18n/<lang>.json) ----------
UI = {
 "Explain Like I'm 10": ("Explique-moi comme si j'avais 10 ans", "Explícamelo como si tuviera 10 años", "اشرحها لي كأن عمري 10 سنوات"),
 "What is it?": ("C'est quoi ?", "¿Qué es?", "ما هو؟"),
 "Why does it matter?": ("Pourquoi c'est important ?", "¿Por qué importa?", "لماذا يهم؟"),
 "How does it help people?": ("Comment cela aide-t-il les gens ?", "¿Cómo ayuda a las personas?", "كيف يساعد الناس؟"),
 "For Teachers": ("Pour les enseignants", "Para docentes", "للمعلمين"),
 "Discussion questions": ("Questions de discussion", "Preguntas para debatir", "أسئلة للنقاش"),
 "Print a one-page teacher sheet": ("Imprimer une fiche enseignant d'une page", "Imprimir una ficha docente de una página", "اطبع ورقة للمعلم من صفحة واحدة"),
 "All teacher sheets": ("Toutes les fiches enseignants", "Todas las fichas docentes", "كل أوراق المعلمين"),
 "Cite This Page": ("Citer cette page", "Citar esta página", "استشهد بهذه الصفحة"),
 "Copy": ("Copier", "Copiar", "نسخ"),
 "Copy APA citation": ("Copier la citation APA", "Copiar la cita APA", "انسخ استشهاد APA"),
 "Copy MLA citation": ("Copier la citation MLA", "Copiar la cita MLA", "انسخ استشهاد MLA"),
 "Sources are listed with each fact in the Five W's above.": ("Les sources figurent avec chaque fait dans les 5 W ci-dessus.", "Las fuentes aparecen con cada dato en las 5 W de arriba.", "المصادر مذكورة مع كل معلومة في الأسئلة الخمسة أعلاه."),
 "Start Here": ("Commencez ici", "Empieza aquí", "ابدأ من هنا"),
 "Kids": ("Enfants", "Niños", "الأطفال"),
 "Amazing facts and simple explanations.": ("Des faits étonnants et des explications simples.", "Datos asombrosos y explicaciones sencillas.", "حقائق مذهلة وشروح بسيطة."),
 "Students & Teachers": ("Élèves et enseignants", "Estudiantes y docentes", "الطلاب والمعلمون"),
 "Printable sheets, a glossary and citations.": ("Fiches imprimables, glossaire et citations.", "Fichas imprimibles, glosario y citas.", "أوراق قابلة للطباعة ومسرد واستشهادات."),
 "Curious Adults": ("Adultes curieux", "Adultos curiosos", "البالغون الفضوليون"),
 "Every solution, searchable in one place.": ("Toutes les solutions, en un seul endroit.", "Todas las soluciones, en un solo lugar.", "كل الحلول في مكان واحد قابل للبحث."),
 "Partners": ("Partenaires", "Socios", "الشركاء"),
 "Sponsor or work with Saving Planets.": ("Sponsoriser Saving Planets ou travailler avec nous.", "Patrocina o colabora con Saving Planets.", "ارعَ Saving Planets أو اعمل معنا."),
 "Glossary": ("Glossaire", "Glosario", "المسرد"),
 "Simple definitions of words used across Saving Planets. On solution pages, tap or hover over a dotted word to see its meaning.": (
   "Des définitions simples des mots utilisés sur Saving Planets. Sur les pages de solutions, touchez ou survolez un mot souligné en pointillés pour voir sa définition.",
   "Definiciones sencillas de palabras usadas en Saving Planets. En las páginas de soluciones, toca o pasa el cursor sobre una palabra punteada para ver su significado.",
   "تعريفات بسيطة لكلمات مستخدمة في Saving Planets. في صفحات الحلول، المس كلمة منقّطة أو مرّر المؤشر فوقها لترى معناها."),
 "Teacher Sheets": ("Fiches enseignants", "Fichas docentes", "أوراق المعلمين"),
 "A printable one-page sheet for every solution: the Five W's, a kid-friendly summary, sources and three discussion questions.": (
   "Une fiche imprimable d'une page pour chaque solution : les 5 W, un résumé adapté aux enfants, les sources et trois questions de discussion.",
   "Una ficha imprimible de una página para cada solución: las 5 W, un resumen para niños, las fuentes y tres preguntas para debatir.",
   "ورقة قابلة للطباعة من صفحة واحدة لكل حل: الأسئلة الخمسة وملخص مناسب للأطفال والمصادر وثلاثة أسئلة للنقاش."),
 "Open": ("Ouvrir", "Abrir", "افتح"),
 "Print": ("Imprimer", "Imprimir", "اطبع"),
 "See also the": ("Voir aussi le", "Consulta también el", "انظر أيضًا"),
 "What is {x}, and what problem does it help solve?": ("Qu'est-ce que {x}, et quel problème aide-t-il à résoudre ?", "¿Qué es {x} y qué problema ayuda a resolver?", "ما هو {x}، وما المشكلة التي يساعد في حلها؟"),
 "Who is behind {x}, and where does the work happen?": ("Qui est derrière {x}, et où le travail a-t-il lieu ?", "¿Quién está detrás de {x} y dónde se realiza el trabajo?", "من يقف وراء {x}، وأين يجري العمل؟"),
 "How does {x} help both people and nature? Use one fact from this page.": ("Comment {x} aide-t-il à la fois les gens et la nature ? Utilisez un fait de cette page.", "¿Cómo ayuda {x} a las personas y a la naturaleza? Usa un dato de esta página.", "كيف يساعد {x} الناس والطبيعة معًا؟ استخدم معلومة واحدة من هذه الصفحة."),
}
GLOSS_LABEL = {'en': 'Glossary', 'fr': 'Glossaire', 'es': 'Glosario', 'ar': 'المسرد', 'it': 'Glossario'}

def merge_i18n():
    for i, l in enumerate(LANGS):
        p = f'i18n/{l}.json'; m = json.load(open(p, encoding='utf8')); n0 = json.dumps(m, ensure_ascii=False)
        for k, v in UI.items():
            if i < len(v): m[k] = v[i]
        for t in GL:
            m[t['en']['term']] = t[l]['term']; m[t['en']['def']] = t[l]['def']
        if json.dumps(m, ensure_ascii=False) != n0: json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)

def m1(rx, s):
    m = re.search(rx, s, re.S); return m.group(1).strip() if m else ''

def blocks(page, s, override):
    title = re.sub(r'<[^>]+>', '', m1(r'<h1[^>]*>(.*?)</h1>', s))
    what, why = m1(r'<h3>What</h3><p>(.*?)</p>', s), m1(r'<h3>Why</h3><p>(.*?)</p>', s)
    people = m1(r'<h3 class="mission-title">For People</h3><p>(.*?)</p>', s)
    rows = []
    if page in override:
        rows = [f'<li>{esc(x)}</li>' for x in override[page]]
    else:
        if what: rows.append(f'<li><strong>What is it?</strong> {what}</li>')
        if why: rows.append(f'<li><strong>Why does it matter?</strong> {why}</li>')
        if people and len(re.sub(r"<[^>]+>", "", people)) < 260: rows.append(f'<li><strong>How does it help people?</strong> {people}</li>')
        if not rows:
            d = m1(r'<meta name="description" content="([^"]*)"', s)
            if d: rows.append(f'<li>{d}</li>')
    eli = ('<!-- ELI10:START --><section class="eli10" id="eli10" aria-labelledby="eli10-h"><h2 id="eli10-h">'
           '<span class="eli10-icon" aria-hidden="true">💡</span> Explain Like I&#x27;m 10</h2><ul>' + ''.join(rows) + '</ul></section><!-- ELI10:END -->')
    t = esc(title)
    qs = [f'What is {t}, and what problem does it help solve?', f'Who is behind {t}, and where does the work happen?',
          f'How does {t} help both people and nature? Use one fact from this page.']
    teach = ('<!-- TEACHER:START --><section class="teacher-box" id="teachers" aria-labelledby="teach-h" data-pagefind-ignore>'
             '<h2 id="teach-h">For Teachers</h2><h3>Discussion questions</h3><ol>' + ''.join(f'<li>{q}</li>' for q in qs) + '</ol>'
             '<p class="teacher-src">Sources are listed with each fact in the Five W&#x27;s above.</p>'
             '<p class="teacher-actions"><button type="button" class="btn-nav print-sheet">Print a one-page teacher sheet</button> '
             '<a href="Teachers.html">All teacher sheets</a></p></section><!-- TEACHER:END -->')
    cite = ('<!-- CITE:START --><section class="cite-box" id="cite" aria-labelledby="cite-h" data-pagefind-ignore><h2 id="cite-h">Cite This Page</h2>'
            f'<div class="cite-row"><p class="cite-style">APA</p><p class="cite-text" data-cite="apa">Saving Planets. (n.d.). {t}. https://www.savingplanets.com/{page}</p>'
            '<button type="button" class="cite-copy" aria-label="Copy APA citation">Copy</button></div>'
            f'<div class="cite-row"><p class="cite-style">MLA</p><p class="cite-text" data-cite="mla">&quot;{t}.&quot; Saving Planets, https://www.savingplanets.com/{page}.</p>'
            '<button type="button" class="cite-copy" aria-label="Copy MLA citation">Copy</button></div></section><!-- CITE:END -->')
    return eli, teach, cite

def put(s, name, block, anchor_rx, before=True):
    rx = re.compile(r'<!-- ' + name + r':START -->[\s\S]*?<!-- ' + name + r':END -->\n?')
    if rx.search(s): return rx.sub(lambda m: block + '\n', s, 1)
    m = re.search(anchor_rx, s)
    if not m: return s
    i = m.start() if before else m.end()
    return s[:i] + block + '\n' + s[i:]

def assets(s):
    if 'batchb.css' not in s: s = s.replace('</head>', CSS + '\n</head>', 1)
    else: s = re.sub(r'batchb\.css\?v=[0-9a-z]+', f'batchb.css?v={V}', s)
    if 'batchb.js' not in s: s = s.replace('</body>', JS + '</body>', 1)
    else: s = re.sub(r'batchb\.js\?v=[0-9a-z]+', f'batchb.js?v={V}', s)
    return s

def shell(fname, title, desc, h1, intro, body, bodyclass):
    tpl = rd('Contact.html'); head, b = tpl.split('<body', 1)
    nav = m1(r'(<nav id="topnav">.*?</nav>)', b); footer = re.sub(r'<script[^>]*></script>', '', m1(r'(<footer>.*?</footer>)', b))
    jsv = m1(r'site\.js\?v=([0-9a-z]+)', b) or '1'
    h = head.replace('Contact.html', fname)  # Oct 16: any Contact title (seo-meta override changed it)
    h = re.sub(r'<title>[^<]*</title>', lambda _m: f'<title>{title} | Saving Planets</title>', h, count=1)
    h = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*"', lambda m: m.group(1) + esc(desc) + '"', h)
    h = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*"', lambda m: m.group(1) + title + ' | Saving Planets"', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    ld = ('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "WebPage", "name": "' + title + '", "description": "' + desc.replace('"', '\\"') +
          '", "url": "https://www.savingplanets.com/' + fname + '", "inLanguage": "en", "datePublished": "2026-10-12", "dateModified": "2026-10-12", "isPartOf": {"@type": "WebSite", "name": "Saving Planets", "url": "https://www.savingplanets.com/"}}</script>\n')
    h = h.replace('</head>', CSS + '\n' + ld + '</head>')
    return (h + f'<body class="toc-sub {bodyclass}"><a class="skip-link" href="#main">Skip to content</a>{nav}\n'
            f'<section class="page-hero"><div class="page-hero-content"><h1>{h1}</h1><p>{intro}</p></div></section>\n'
            f'<main id="main">{body}</main>\n{footer}<script src="site.js?v={jsv}"></script>{JS}</body></html>\n')

def glossary_page():
    terms = sorted(GL, key=lambda t: t['en']['term'].lower())
    body = '<section class="five-ws gloss"><!-- GLOSSARY-LIST:START -->' + gl_list(terms, 'en') + '<!-- GLOSSARY-LIST:END --></section>'
    return shell('Glossary.html', 'Glossary', 'Simple definitions of the science words used on Saving Planets, from orbit and radar to phytoplankton and mangroves.',
                 'Glossary', 'Simple definitions of words used across Saving Planets. On solution pages, tap or hover over a dotted word to see its meaning.', body, 'gloss-page')

def gl_list(terms, lang):
    import unicodedata
    letter = lambda w: unicodedata.normalize('NFD', w)[0].upper()
    out, cur = [], None
    letters = []
    for t in terms:
        L = letter(t[lang]['term'])
        if L != cur:
            if cur is not None: out.append('</dl>')
            cur = L; letters.append(L); out.append(f'<h2 class="gloss-letter" id="letter-{esc(L)}">{esc(L)}</h2><dl>')
        out.append(f'<dt id="{t["id"]}">{esc(t[lang]["term"])}</dt><dd>{esc(t[lang]["def"])}</dd>')
    out.append('</dl>')
    jump = '<p class="gloss-jump">' + ' '.join(f'<a href="#letter-{esc(L)}">{esc(L)}</a>' for L in letters) + '</p>'
    return jump + ''.join(out)

def teachers_page():
    secs = []
    for f, name, items in SOL.hubs():
        lis = ''.join(f'<li><a href="{h}#teachers">{esc(n)}</a> <span class="t-actions"><a class="t-print" href="{h}?print=1" rel="nofollow">Print</a></span></li>' for h, n in items)
        secs.append(f'<section class="five-ws t-hub"><h2><a href="{f}">{esc(name)}</a></h2><ul class="t-list">{lis}</ul></section>')
    body = ('<p class="t-intro">See also the <a href="Glossary.html">Glossary</a></p>' + ''.join(secs))
    return shell('Teachers.html', 'Teacher Sheets', 'A printable one-page sheet for every Saving Planets solution: the Five W\'s, a kid-friendly summary, sources and three discussion questions.',
                 'Teacher Sheets', "A printable one-page sheet for every solution: the Five W&#x27;s, a kid-friendly summary, sources and three discussion questions.", body, 'teachers-page')

AUD = ('<!-- AUDIENCE:START --><section class="audience" aria-labelledby="aud-h"><h2 id="aud-h">Start Here</h2><div class="aud-grid">'
       '<a class="aud-card" href="Amazing_Facts.html"><span class="aud-icon" aria-hidden="true">🧒</span><span class="aud-title">Kids</span><span class="aud-text">Amazing facts and simple explanations.</span></a>'
       '<a class="aud-card" href="Teachers.html"><span class="aud-icon" aria-hidden="true">🎓</span><span class="aud-title">Students &amp; Teachers</span><span class="aud-text">Printable sheets, a glossary and citations.</span></a>'
       '<a class="aud-card" href="Solutions.html"><span class="aud-icon" aria-hidden="true">🔭</span><span class="aud-title">Curious Adults</span><span class="aud-text">Every solution, searchable in one place.</span></a>'
       '<a class="aud-card" href="mailto:partners@savingplanets.com?subject=Creating%20Partnership%20Starts%20Here"><span class="aud-icon" aria-hidden="true">🤝</span><span class="aud-title">Partners</span><span class="aud-text">Sponsor or work with Saving Planets.</span></a>'
       '<a class="aud-card" href="Press.html"><span class="aud-icon" aria-hidden="true">📰</span><span class="aud-title">Press</span><span class="aud-text">Press kit, logos, fact sheets and contacts.</span></a><a class="aud-card" href="Topics.html"><span class="aud-icon" aria-hidden="true">🧭</span><span class="aud-title">Explore A to Z</span><span class="aud-text">Every solution and science word, from A to Z.</span></a>'  # Oct 14: Press + Explore tiles
       '</div></section><!-- AUDIENCE:END -->')

def pre():
    merge_i18n()
    ov = json.load(open('assets/data/eli10.json', encoding='utf8')) if os.path.exists('assets/data/eli10.json') else {}
    ov = {k: v for k, v in ov.items() if not k.startswith('_')}
    n = 0
    for page, *_ in solution_pages():
        s = rd(page); eli, teach, cite = blocks(page, s, ov)
        s = put(s, 'ELI10', eli, r'<section class="five-ws" id="solution">')
        s = put(s, 'TEACHER', teach, r'<footer>')
        s = put(s, 'CITE', cite, r'<footer>')
        n += wr(page, assets(s))
    s = rd('index.html'); s = assets(put(s, 'AUDIENCE', AUD, r'<!-- SOTW:START -->')); wr('index.html', s)
    write_generated('Glossary.html', glossary_page()); write_generated('Teachers.html', teachers_page())
    pl = rd('i18n/pages.txt')
    for p in ('Glossary.html', 'Teachers.html'):
        if p not in pl.split(): pl = pl.rstrip('\n') + '\n' + p + '\n'
    wr('i18n/pages.txt', pl)
    sm = rd('sitemap.xml')
    for p in ('Glossary.html', 'Teachers.html'):
        if f'savingplanets.com/{p}<' not in sm:
            sm = sm.replace('  <url><loc>https://www.savingplanets.com/Contact.html</loc>', f'  <url><loc>https://www.savingplanets.com/{p}</loc><lastmod>2026-10-12</lastmod></url>\n  <url><loc>https://www.savingplanets.com/Contact.html</loc>', 1)
    wr('sitemap.xml', sm)
    print(f'batch-b: {len(solution_pages())} solution pages ({n} changed); Glossary {len(GL)} terms; Teachers.html; homepage audience row')

# ---------- post-i18n glossary tooltips ----------
GL_RE = re.compile(r'<span class="gl"><button[^>]*>(.*?)</button><span class="gl-pop"[^>]*>.*?</span></span>', re.S)
SECTION_RE = re.compile(r'(<section [^>]*class="(?:eli10|five-ws|impact[^"]*)"[^>]*>)(.*?)(</section>)', re.S)

def tooltipify(s, lang):
    s = GL_RE.sub(r'\1', s)
    done = set(); k = [0]
    terms = sorted(((t, w) for t in GL for w in t[lang]['match']), key=lambda x: -len(x[1]))
    pre = '' if lang == 'en' else ''
    def fix_text(txt):
        # txt: a plain text run (no tags)
        for t, w in terms:
            if t['id'] in done: continue
            if lang == 'ar': rx = re.compile(r'(?<![\w])(?:[وفبلك]?)(' + re.escape(w) + r')(?![\w])')
            else: rx = re.compile(r'(?<![\w-])(' + re.escape(w) + r')(?![\w-])', re.I)
            m = rx.search(txt)
            if not m: continue
            done.add(t['id']); k[0] += 1; pid = f'gl-{t["id"]}'
            tip = (f'<span class="gl"><button type="button" class="gl-term" aria-expanded="false" aria-controls="{pid}">{m.group(1)}</button>'
                   f'<span class="gl-pop" id="{pid}" role="tooltip" data-pagefind-ignore hidden>{esc(t[lang]["def"])} <a href="Glossary.html#{t["id"]}">{GLOSS_LABEL[lang]}</a></span></span>')
            return fix_text(txt[:m.start(1)]) + tip + fix_text(txt[m.end(1):])
        return txt
    def fix_p(pm):
        inner = pm.group(2); out = []; depth = 0
        for part in re.split(r'(<[^>]+>)', inner):
            if part.startswith('<'):
                if re.match(r'<(a|button|strong)\b', part): depth += 1
                elif re.match(r'</(a|button|strong)>', part): depth = max(0, depth - 1)
                out.append(part)
            else: out.append(part if depth else fix_text(part))
        return pm.group(1) + ''.join(out) + pm.group(3)
    def fix_sec(sm):
        body = re.sub(r'(<(?:p|li)(?: [^>]*)?>)(.*?)(</(?:p|li)>)', lambda pm: pm.group(0) if 'fact-source' in pm.group(1) or 'hub-label' in pm.group(1) else fix_p(pm), sm.group(2), flags=re.S)
        return sm.group(1) + body + sm.group(3)
    return SECTION_RE.sub(fix_sec, s), k[0]

def post():
    tot = 0
    pages = [p for p, *_ in solution_pages()]
    for lang in ['en'] + LANGS:
        for p in pages:
            f = p if lang == 'en' else f'{lang}/{p}'
            if not os.path.exists(f): continue
            s, n = tooltipify(rd(f), lang); tot += n; wr(f, s)
        g = 'Glossary.html' if lang == 'en' else f'{lang}/Glossary.html'
        if os.path.exists(g):
            terms = sorted(GL, key=lambda t: t[lang]['term'].lower())
            s = re.sub(r'<!-- GLOSSARY-LIST:START -->[\s\S]*?<!-- GLOSSARY-LIST:END -->', lambda m: '<!-- GLOSSARY-LIST:START -->' + gl_list(terms, lang) + '<!-- GLOSSARY-LIST:END -->', rd(g))
            if lang != 'en':  # bs4 output may have stripped the comment markers; fall back to the section
                if 'GLOSSARY-LIST:START' not in s:
                    s = re.sub(r'(<section class="five-ws gloss">)[\s\S]*?(</section>)', lambda m: m.group(1) + gl_list(terms, lang) + m.group(2), s, 1)
            wr(g, s)
    print(f'batch-b glossary: {tot} tap/hover definitions across en/fr/es/ar solution pages')

if __name__ == '__main__':
    post() if '--glossary' in sys.argv else pre()
