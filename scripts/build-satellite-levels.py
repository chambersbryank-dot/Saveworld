#!/usr/bin/env python3
"""Earth Satellite Explorer: pick K-3, grades 4-12, or university, then open a real
Earth-observation satellite that already has a Saving Planets page.

Level text is copied from that page, not rewritten:
  K-3 uses Explain Like I'm 10.
  Grades 4-12 use the What and Why cards.
  University adds the impact statement.
Photos and credits come from the page or its Solutions card.
A page is included when its English What / Who / When / Where / Why text calls it a
satellite, plus GEDI, GRACE-FO and ALOS-4. Services that only mention satellite data
are left out. No Google Analytics.

Writes Earth_Satellite_Explorer.html, assets/data/satellite-levels.<lang>.json,
i18n strings, and an SATEXPL link on Play_and_Learn.html and Teachers.html."""
import html, json, os, re, importlib.util
from bs4 import BeautifulSoup

PAGE = 'Earth_Satellite_Explorer.html'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
ASSETV = '20261102c'
GA = re.compile(r"\n?<!-- Google tag \(gtag\.js\) -->.*?<!-- /Google tag -->", re.S)
ALWAYS = {'GEDI.html', 'GRACE-FO.html', 'ALOS-4.html'}
# These pages mention satellites because they use satellite data or run a service. They are not one satellite mission.
DENY = {'Digital_Earth_Africa.html', 'FIRMS.html', 'Copernicus_EMS.html', 'International_Charter.html', 'Galileo.html', 'GSMaP.html', 'UNEP_MARS.html', 'GLOBE_Program.html', 'Tsunami_Early_Warning.html'}
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)

T = {
 'Earth Satellite Explorer': ('Explorateur de satellites d’observation de la Terre', 'Explorador de satélites de observación de la Tierra', 'مستكشف أقمار رصد الأرض', 'Esploratore di satelliti per l’osservazione della Terra', 'סייר לווייני תצפית על כדור הארץ'),
 'Pick a level, then pick a real Earth-observation satellite that already has a Saving Planets page. K-3 shows that page’s Explain Like I’m 10 note. Grades 4-12 show What and Why. University also shows the impact statement. Photos keep the credit from the page.':
 ("Choisis un niveau, puis un vrai satellite d’observation de la Terre qui a déjà une page Saving Planets. Le niveau K-3 montre la note « Explique-moi comme si j'avais 10 ans ». Les classes 4 à 12 montrent Quoi et Pourquoi. L’université ajoute aussi l’énoncé d’impact. Les photos gardent le crédit de la page.",
  'Elige un nivel y luego un satélite real de observación de la Tierra que ya tiene una página en Saving Planets. K-3 muestra la nota «Explícamelo como si tuviera 10 años». Los grados 4 a 12 muestran Qué y Por qué. La universidad añade también la declaración de impacto. Las fotos conservan el crédito de la página.',
  'اختر مستوى ثم قمرًا حقيقيًا لرصد الأرض له صفحة أصلًا في Saving Planets. مستوى الروضة حتى الثالث يعرض ملاحظة «اشرحها لي كأن عمري 10 سنوات». الصفوف 4–12 تعرض ماذا ولماذا. الجامعة تضيف أيضًا بيان الأثر. الصور تحتفظ باسم المصدر الموجود في الصفحة.',
  'Scegli un livello, poi un vero satellite di osservazione della Terra che ha già una pagina su Saving Planets. K-3 mostra la nota «Spiegamelo come se avessi 10 anni». Le classi 4-12 mostrano Che cosa e Perché. L’università aggiunge anche la dichiarazione di impatto. Le foto tengono il credito della pagina.',
  'בחרו רמה ואז לוויין אמיתי לתצפית על כדור הארץ שכבר יש לו דף ב-Saving Planets. גן עד כיתה ג\' מציג את ההערה «הסבירו לי כאילו אני בן 10». כיתות ד\'–י״ב מציגות מה ולמה. האוניברסיטה מוסיפה גם את הצהרת ההשפעה. התמונות שומרות על הקרדיט מהדף.'),
 'K-3': ('Maternelle à CE2', 'Infantil a 3.º', 'الروضة حتى الصف الثالث', 'K-3', 'גן–כיתה ג\''),
 'Grades 4-12': ('CM1 à Terminale', '4.º a Bachillerato', 'الصف الرابع حتى الثاني عشر', 'Classi 4-12', 'כיתות ד\'–י״ב'),
 'Choose a satellite': ('Choisis un satellite', 'Elige un satélite', 'اختر قمرًا صناعيًا', 'Scegli un satellite', 'בחרו לוויין'),
 'This explorer needs JavaScript. You can still open each satellite page below.':
 ('Cet explorateur a besoin de JavaScript. Tu peux quand même ouvrir chaque page de satellite ci-dessous.',
  'Este explorador necesita JavaScript. Aun así puedes abrir cada página de satélite aquí abajo.',
  'يحتاج هذا المستكشف إلى جافاسكربت. ما زال بإمكانك فتح صفحة كل قمر في الأسفل.',
  'Questo esploratore ha bisogno di JavaScript. Puoi comunque aprire ogni pagina di satellite qui sotto.',
  'הסייר הזה צריך JavaScript. עדיין אפשר לפתוח כל דף לוויין למטה.'),
 'Sorry, the satellite explorer could not load. Please refresh the page.':
 ("Désolé, l’explorateur n’a pas pu se charger. Actualise la page.",
  'Lo sentimos, el explorador no se pudo cargar. Actualiza la página.',
  'عذرًا، تعذّر تحميل المستكشف. يرجى تحديث الصفحة.',
  'Spiacenti, l’esploratore non si è caricato. Aggiorna la pagina.',
  'מצטערים, הסייר לא נטען. רעננו את הדף.'),
}
UI = {
 'en': dict(source='Source:', eli="Explain Like I'm 10", what='What it measures', why='Why it matters', impact='Impact statement', read='Read the whole page'),
 'fr': dict(source='Source :', eli="Explique-moi comme si j'avais 10 ans", what='Ce qu’il mesure', why='Pourquoi c’est important', impact='Énoncé d’impact', read='Lire toute la page'),
 'es': dict(source='Fuente:', eli='Explícamelo como si tuviera 10 años', what='Qué mide', why='Por qué importa', impact='Declaración de impacto', read='Leer la página completa'),
 'ar': dict(source='المصدر:', eli='اشرحها لي كأن عمري 10 سنوات', what='ماذا يقيس', why='لماذا يهم', impact='بيان الأثر', read='اقرأ الصفحة كلها'),
 'it': dict(source='Fonte:', eli='Spiegamelo come se avessi 10 anni', what='Che cosa misura', why='Perché è importante', impact='Dichiarazione di impatto', read='Leggi tutta la pagina'),
 'he': dict(source='מקור:', eli='הסבירו לי כאילו אני בן 10', what='מה הוא מודד', why='למה זה חשוב', impact='הצהרת השפעה', read='קראו את כל הדף'),
}
LINK = {
 'en': ('Earth Satellite Explorer', 'Pick a level and see what real Earth satellites measure.'),
 'fr': ('Explorateur de satellites d’observation', 'Choisis un niveau et vois ce que mesurent de vrais satellites.'),
 'es': ('Explorador de satélites de la Tierra', 'Elige un nivel y mira qué miden satélites reales.'),
 'ar': ('مستكشف أقمار رصد الأرض', 'اختر مستوى وانظر ماذا تقيس الأقمار الحقيقية.'),
 'it': ('Esploratore di satelliti della Terra', 'Scegli un livello e guarda che cosa misurano i satelliti veri.'),
 'he': ('סייר לווייני תצפית על כדור הארץ', 'בחרו רמה וראו מה מודדים לוויינים אמיתיים.'),
}

def clean(node):
    for pop in node.select('.gl-pop'): pop.decompose()
    for b in node.select('button'): b.replace_with(b.get_text())

def blocks(node):
    if node is None: return []
    clean(node)
    out = []
    for p in node.select('p'):
        if 'hub-label' in (p.get('class') or []):
            continue
        if 'fact-source' in (p.get('class') or []):
            a = p.select_one('a[href]')
            if a and a['href'].startswith('http'):
                out.append({'href': a['href'], 'name': re.sub(r'\s+', ' ', a.get_text(' ', strip=True))})
        else:
            t = re.sub(r'\s+', ' ', p.get_text(' ', strip=True))
            if t: out.append({'t': t})
    return out

def w_index(soup):
    """Return {What, Why} blocks by English card order: Who, What, When, Where, Why."""
    cards = soup.select('#solution .w-card')
    keys = ['Who', 'What', 'When', 'Where', 'Why']
    out = {}
    for i, card in enumerate(cards):
        if i < len(keys): out[keys[i]] = blocks(card)
    return out

def eli(soup):
    sec = soup.select_one('#eli10')
    if not sec: return []
    clean(sec)
    rows = []
    for li in sec.select('li'):
        t = re.sub(r'\s+', ' ', li.get_text(' ', strip=True))
        if t: rows.append({'t': t})
    return rows

def impact(soup):
    box = soup.select_one('#impact .impact-box') or soup.select_one('#impact')
    return blocks(box) if box else []

def norm_src(src):
    src = (src or '').strip()
    while src.startswith('../'): src = src[3:]
    return src

def sanitize(el):
    if el is None: return ''
    parts = []
    for child in el.children:
        if isinstance(child, str): parts.append(esc(child))
        elif child.name == 'a':
            href = child.get('href') or ''
            if href.startswith('http://') or href.startswith('https://'):
                parts.append(f'<a href="{esc(href)}" rel="noopener" target="_blank">{esc(child.get_text())}</a>')
            else: parts.append(esc(child.get_text()))
        elif child.name in ('bdi', 'span', 'p'): parts.append(sanitize(child))
        else: parts.append(esc(child.get_text()))
    return re.sub(r'\s+', ' ', ''.join(parts)).strip()

def agency(text):
    return bool(re.search(r'NASA|ESA|JAXA|ISRO|NOAA|CNES|EUMETSAT|USGS|DLR', text or '', re.I))

def photo(lang, page, soup):
    card = None
    sol = 'Solutions.html' if lang == 'en' else f'{lang}/Solutions.html'
    if os.path.exists(sol):
        s = BeautifulSoup(rd(sol), 'html.parser')
        for art in s.select('article.sol-card'):
            if (art.get('data-url') or '').endswith(page):
                card = art
                break
    img = soup.select_one('main img')
    credit_el = None
    for p in soup.select('main p.photo-credit'):
        if agency(p.get_text(' ', strip=True)):
            credit_el = p
            break
    if credit_el is None:
        credit_el = soup.select_one('main p.photo-credit')
    if (credit_el is None or not agency(credit_el.get_text())) and card is not None:
        c = card.select_one('.photo-credit')
        if c and (credit_el is None or agency(c.get_text())):
            credit_el = c
            im = card.select_one('img')
            if im: img = im
    if img is None and card is not None: img = card.select_one('img')
    if img is None: return {}
    try: w, h = int(img.get('width') or 0), int(img.get('height') or 0)
    except ValueError: w = h = 0
    return {'img': norm_src(img.get('src')), 'alt': img.get('alt') or '', 'w': w, 'h': h, 'credit': sanitize(credit_el)}

def eo_pages():
    s = rd('Solutions.html')
    m = re.search(r'data-hub="Earth_Observation.html".*?</section>', s, re.S)
    return re.findall(r'data-url="([^"]+)"', m.group(0)) if m else []

def include(page):
    if page in DENY: return False
    if page in ALWAYS: return True
    if page not in eo_pages() and page not in ALWAYS: return False
    soup = BeautifulSoup(rd(page), 'html.parser')
    text = []
    for card in soup.select('#solution .w-card'):
        clean(card)
        text.append(card.get_text(' ', strip=True))
    return bool(re.search(r'\bsatellite\b', ' '.join(text), re.I))

def record(lang, page):
    path = page if lang == 'en' else f'{lang}/{page}'
    if not os.path.exists(path): path = page
    soup = BeautifulSoup(rd(path), 'html.parser')
    h = soup.select_one('h1')
    name = re.sub(r'\s+', ' ', h.get_text(' ', strip=True)) if h else page
    w = w_index(soup)
    ph = photo(lang, page, soup)
    return {'u': page, 'n': name, 'img': ph.get('img') or '', 'alt': ph.get('alt') or '', 'w': ph.get('w') or 0, 'h': ph.get('h') or 0,
            'credit': ph.get('credit') or '', 'k3': eli(soup), 'what': w.get('What') or [], 'why': w.get('Why') or [], 'impact': impact(soup)}

DESC = "Pick a level, then pick a real Earth-observation satellite that already has a Saving Planets page. K-3 shows that page's Explain Like I'm 10 note. Grades 4-12 show What and Why. University also shows the impact statement. Photos keep the credit from the page."
MAIN_HEAD = '''<section class="page-hero hero-space"><div class="page-hero-content"><h1>Earth Satellite Explorer</h1><p>''' + esc(DESC) + '''</p></div></section>
<div class="se-wrap" id="se">
<p class="se-lead">''' + esc(DESC) + '''</p>
<fieldset class="se-levels"><legend>Choose your level</legend>
<label><input type="radio" name="se-level" value="k3" checked> K-3</label>
<label><input type="radio" name="se-level" value="mid"> Grades 4-12</label>
<label><input type="radio" name="se-level" value="uni"> University</label>
</fieldset>
<div class="se-layout">
<div class="se-list" id="se-list" role="listbox" aria-label="Choose a satellite"></div>
<article class="se-card" id="se-detail" aria-live="polite" hidden></article>
</div>
<template class="se-error-tpl"><p role="alert">Sorry, the satellite explorer could not load. Please refresh the page.</p></template>
<noscript><p>This explorer needs JavaScript. You can still open each satellite page below.</p><ul id="se-noscript"></ul></noscript>
</div>
'''

def shell(records):
    s = rd('Satellite_Explorer.html')
    s = re.sub(r'<main id="main">.*?</main>', '<main id="main">\n' + MAIN_HEAD + '\n</main>', s, count=1, flags=re.S)
    items = ''.join(f'<li><a href="{esc(r["u"])}">{esc(r["n"])}</a></li>' for r in records)
    s = s.replace('<ul id="se-noscript"></ul>', '<ul>' + items + '</ul>')
    s = re.sub(r'<title>.*?</title>', '<title>Earth Satellite Explorer | Saving Planets</title>', s, count=1, flags=re.S)
    desc = esc(DESC)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {attr} content=")[^"]*"', lambda m: m.group(1) + desc + '"', s, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {attr} content=")[^"]*"', r'\1Earth Satellite Explorer | Saving Planets"', s, count=1)
    s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', r'\1Earth Satellite Explorer"', s, count=1)
    for folder in ('', 'fr/', 'es/', 'ar/', 'it/', 'he/'):
        s = s.replace(f'https://www.savingplanets.com/{folder}Satellite_Explorer.html', f'https://www.savingplanets.com/{folder}{PAGE}')
        if folder:
            s = s.replace(f'href="{folder}Satellite_Explorer.html"', f'href="{folder}{PAGE}"')
    s = s.replace('href="Satellite_Explorer.html" hreflang="en"', f'href="{PAGE}" hreflang="en"')
    s = s.replace(' aria-current="page"', '')
    s = s.replace('satellite-explorer-page', 'earth-satellite-page')
    s = re.sub(r'<script src="edu\.js[^"]*" defer></script>\s*', '', s)
    s = re.sub(r'<script src="edu-extras\.js[^"]*" defer></script>\s*', '', s)
    s = re.sub(r'<script src="sx-anim\.js[^"]*" defer></script>\s*', '', s)
    s = GA.sub('', s)
    if 'satellite-levels.css' not in s:
        s = s.replace('</head>', f'<link rel="stylesheet" href="satellite-levels.css?v={ASSETV}">\n</head>', 1)
    if 'satellite-levels.js' not in s:
        s = s.replace('</body>', f'<script src="satellite-levels.js?v={ASSETV}" defer></script>\n</body>', 1)
    if 'gtag' in s or 'googletagmanager' in s:
        raise SystemExit('satellite explorer: refused to keep a Google Analytics tag')
    return s

def merge_i18n():
    order = ['fr', 'es', 'ar', 'it', 'he']
    for i, lang in enumerate(order):
        p = f'i18n/{lang}.json'
        m = json.load(open(p, encoding='utf8'))
        n0 = json.dumps(m, ensure_ascii=False)
        for k, vals in T.items():
            if i < len(vals): m[k] = vals[i]
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
        name, blurb = LINK[lang]
        css = ('../' if lang != 'en' else '') + f'satellite-levels.css?v={ASSETV}'
        for fname, anchor in (('Play_and_Learn.html', '<!-- KIDSP1:START -->'), ('Teachers.html', '<!-- LESSONPLAN:START -->')):
            path = pre + fname
            if not os.path.exists(path): continue
            if fname.startswith('Play'):
                block = ('<!-- SATEXPL:START --><link rel="stylesheet" href="' + css + '">'
                         f'<p class="se-jump"><a class="pl-tile" href="{PAGE}"><span class="pl-emoji" aria-hidden="true">🛰️</span>'
                         f'<span class="pl-name">{esc(name)}</span><span class="pl-text">{esc(blurb)}</span></a></p><!-- SATEXPL:END -->')
            else:
                block = ('<!-- SATEXPL:START --><link rel="stylesheet" href="' + css + '">'
                         f'<p class="se-teach"><a href="{PAGE}">{esc(name)}</a>: {esc(blurb)}</p><!-- SATEXPL:END -->')
            s = re.sub(r'<!-- SATEXPL:START -->.*?<!-- SATEXPL:END -->', '', rd(path), flags=re.S)
            s = re.sub(r'\n?<link rel="stylesheet" href="(?:\.\./)?satellite-levels\.css\?v=[^"]+">', '', s)
            use = anchor if anchor in s else '</main>'
            s = s.replace(use, block + use, 1)
            n += wr(path, s)
    return n

def sitemap():
    if os.path.exists('sitemap.xml') and f'savingplanets.com/{PAGE}' in rd('sitemap.xml'): return
    import subprocess
    subprocess.check_call(['python3', 'scripts/i18n-sitemap.py'])

def main():
    pages = [p for p in sorted(set(eo_pages()) | ALWAYS) if include(p)]
    # Keep the three named examples first, then the rest by title.
    pages.sort(key=lambda p: (p not in ALWAYS, p))
    merge_i18n(); ensure_lists()
    os.makedirs('assets/data', exist_ok=True)
    for lang in LANGS:
        data = {'ui': UI[lang], 'sats': [record(lang, p) for p in pages]}
        json.dump(data, open(f'assets/data/satellite-levels.{lang}.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
        open(f'assets/data/satellite-levels.{lang}.json', 'a', encoding='utf8').write('\n')
    en_recs = [record('en', p) for p in pages]
    wr(PAGE, shell(en_recs))
    translate()
    k = links()
    sitemap()
    print('satellites', len(pages))
    print('\n'.join(pages))
    print('link writes', k)

if __name__ == '__main__':
    main()
