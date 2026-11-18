#!/usr/bin/env python3
"""Site-wide structure + accessibility (Oct 13). Idempotent; run BEFORE i18n-build (weekly-sync does).
- Footer matches the homepage (empty site-map block, no donate pitch, footer-v2 assets). Sitemap.html still lists every hub and solution.
- <main id="main"> landmark around page content, skip links pointing at it, aria-labels on <video>.
- extras.css (contrast fixes, footer map, About sources list) linked on every page."""
import re, os, sys, glob, importlib.util, html, json
rd = lambda f: open(f, encoding='utf8').read()
def wr(f, s):
    if rd(f) != s: open(f, 'w', encoding='utf8').write(s); return 1
    return 0
esc = lambda s: html.escape(s, quote=True)
V = '20261014u'
CSS = f'<link rel="stylesheet" href="extras.css?v={V}">'
KEY = [('Solutions.html', 'All Solutions'), ('Search.html', 'Search'), ('Glossary.html', 'Glossary'), ('Teachers.html', 'Teacher Sheets'),
       ('Amazing_Facts.html', 'Amazing Facts'), ('Kids_Map.html', 'Kids Planet Map'), ('World_Map.html', 'World Solutions Map'), ('Lesson_Builder.html', 'Lesson Plan Builder'), ('Satellite_Explorer.html', 'Satellite Explorer'), ('Ways_to_Help.html', 'Ways to Help'), ('About.html', 'About'), ('Press.html', 'Press &amp; media'),
       ('Contact.html', 'Contact'), ('Topics.html', 'Topics A to Z'), ('Privacy.html', 'Privacy'), ('Terms.html', 'Terms of Use'), ('Accessibility.html', 'Accessibility'), ('Editorial_Policy.html', 'Editorial Policy'), ('Corrections.html', 'Corrections'), ('Sitemap.html', 'Site Map')]
UI = {'Topics A to Z': ('Sujets de A à Z', 'Temas de la A a la Z', 'الموضوعات من الألف إلى الياء'), 'Privacy': ('Confidentialité', 'Privacidad', 'الخصوصية'), 'Editorial Policy': ('Politique éditoriale', 'Política editorial', 'السياسة التحريرية'), 'Corrections': ('Corrections', 'Correcciones', 'التصحيحات'),
      'Site map': ('Plan du site', 'Mapa del sitio', 'خريطة الموقع'), 'Site Map': ('Plan du site', 'Mapa del sitio', 'خريطة الموقع'),
      'Hubs': ('Pôles', 'Centros', 'المحاور'), 'Explore': ('Explorer', 'Explorar', 'استكشف'), 'All Solutions': ('Toutes les solutions', 'Todas las soluciones', 'كل الحلول'),
      'Search': ('Rechercher', 'Buscar', 'بحث'), 'Teacher Sheets': ('Fiches enseignants', 'Fichas docentes', 'أوراق المعلمين'),
      'Every hub and solution on Saving Planets, in one list.': ('Tous les pôles et toutes les solutions de Saving Planets, en une seule liste.', 'Todos los centros y soluciones de Saving Planets, en una sola lista.', 'كل المحاور والحلول في Saving Planets في قائمة واحدة.'),
      'Key pages': ('Pages principales', 'Páginas principales', 'الصفحات الرئيسية'),
      'video': ('vidéo', 'video', 'فيديو')}


def write_generated(f, page):
    """Write a generated page only when its generated content changed (keeps later seo-fix/add-gtag edits, so translations stay current)."""
    import hashlib
    sig = hashlib.sha1(page.encode('utf8')).hexdigest()[:12]
    page = page.replace('</body>', f'<!-- GEN {sig} --></body>', 1)
    if os.path.exists(f) and f'<!-- GEN {sig} -->' in open(f, encoding='utf8').read(): return 0
    open(f, 'w', encoding='utf8').write(page); return 1

def hubs():
    spec = importlib.util.spec_from_file_location('sol', 'scripts/build-solutions-index.py'); SOL = importlib.util.module_from_spec(spec); spec.loader.exec_module(SOL)
    hl = SOL.hubs(); seen = set(); out = []
    for f, name, items in hl:
        bc_items = []
        for h, n in items:
            bc = re.findall(r'<nav aria-label="Breadcrumb"[^>]*>.*?</nav>', rd(h), re.S)
            out_hubs = re.findall(r'href="([A-Za-z0-9_.-]+\.html)"', bc[0]) if bc else []
            bc_items.append((h, n, out_hubs))
        out.append((f, name, bc_items))
    # primary hub per solution (same rule as Solutions.html)
    where = {}
    for f, name, items in out:
        for h, n, bch in items: where.setdefault(h, []).append((f, bch))
    prim = {h: next((f for f, bch in v if f in bch), v[0][0]) for h, v in where.items()}
    return [(f, name, [(h, n) for h, n, _ in items if prim[h] == f]) for f, name, items in out]

def footer_map(hl):
    """Hubs/Explore markup. Footers no longer embed it (homepage policy); Sitemap.html lists the pages in the body."""
    hub_links = ''.join(f'<li><a href="{f}">{esc(n)}</a></li>' for f, n, _ in hl)
    key_links = ''.join(f'<li><a href="{f}">{n}</a></li>' for f, n in KEY)
    return ('<!-- FOOTER-MAP:START --><div class="footer-map" role="navigation" aria-label="Site map"><div class="fm-col"><h2 class="fm-h">Hubs</h2><ul>' + hub_links +
            '</ul></div><div class="fm-col"><h2 class="fm-h">Explore</h2><ul>' + key_links + '</ul></div></div><!-- FOOTER-MAP:END -->')

def strip_empty_scripts(s):
    """Drop empty <script ...></script> tags (src-only scripts) without a regex HTML filter."""
    out, i, low = [], 0, s.lower()
    while True:
        j = low.find('<script', i)
        if j < 0: out.append(s[i:]); return ''.join(out)
        k = low.find('>', j); e = low.find('</script', k) if k >= 0 else -1; z = low.find('>', e) if e >= 0 else -1
        if z < 0: out.append(s[i:]); return ''.join(out)
        out.append(s[i:j])
        if s[k + 1:e].strip(): out.append(s[j:z + 1])
        i = z + 1

def sitemap_page(hl):
    tpl = rd('Contact.html'); head, b = tpl.split('<body', 1)
    nav = re.search(r'(<nav id="topnav">.*?</nav>)', b, re.S).group(1)
    footer = strip_empty_scripts(re.search(r'(<footer>.*?</footer>)', b, re.S).group(1))
    jsv = re.search(r'site\.js\?v=([0-9a-z]+)', b).group(1)
    desc = 'Every hub and solution on Saving Planets, in one list.'
    h = head.replace('Contact.html', 'Sitemap.html')  # Oct 16: any Contact title (seo-meta override changed it)
    h = re.sub(r'<title>[^<]*</title>', lambda _m: '<title>Site Map | Saving Planets</title>', h, count=1)
    h = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*"', lambda m: m.group(1) + desc + '"', h)
    h = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*"', r'\1Site Map | Saving Planets"', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    h = h.replace('</head>', '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "WebPage", "name": "Site Map", "description": "' + desc +
                  '", "url": "https://www.savingplanets.com/Sitemap.html", "inLanguage": "en", "datePublished": "2026-10-13", "dateModified": "2026-10-13", "isPartOf": {"@type": "WebSite", "name": "Saving Planets", "url": "https://www.savingplanets.com/"}}</script>\n</head>')
    secs = ''.join(f'<section class="sm-hub"><h2><a href="{f}">{esc(n)}</a></h2><ul>' + ''.join(f'<li><a href="{x}">{esc(y)}</a></li>' for x, y in items) + '</ul></section>' for f, n, items in hl)
    keys = '<section class="sm-hub"><h2>Key pages</h2><ul>' + ''.join(f'<li><a href="{f}">{n}</a></li>' for f, n in KEY if f != 'Sitemap.html') + '</ul></section>'
    return (h + f'<body class="toc-sub sitemap-page"><a class="skip-link" href="#main">Skip to content</a>{nav}\n'
            f'<section class="page-hero"><div class="page-hero-content"><h1>Site Map</h1><p>{desc}</p></div></section>\n'
            f'<main id="main"><div class="sm-grid">{keys}{secs}</div></main>\n{footer}<script src="site.js?v={jsv}"></script></body></html>\n')

GLASS_CAT = {'ocean': 'ocean', 'oceans': 'ocean', 'lakes': 'lakes', 'rivers': 'rivers', 'forests': 'forests', 'earth-observation': 'earth',
             'space': 'space', 'project-r': 'space', 'planetary-defense': 'defense', 'space-weather': 'sun', 'polar': 'earth'}
GLASS_PAGE = {'Titan.html': 'titan', 'ExoMars_Rosalind_Franklin.html': 'mars', 'ESCAPADE.html': 'mars', 'MMX.html': 'mars',
              'Oceans.html': 'ocean', 'Lakes.html': 'lakes', 'Polar.html': 'earth', 'Rivers.html': 'rivers', 'Deforestation.html': 'forests', 'Space.html': 'space',
              'Earth_Observation.html': 'earth', 'Planetary_Defense.html': 'defense', 'Space_Weather.html': 'sun', 'Space_Disposal.html': 'space', 'Kids_Map.html': 'ocean', 'Lesson_Builder.html': 'earth', 'Satellite_Explorer.html': 'space'}
def set_glass(f, s):
    m = re.search(r'<meta name="sp:category" content="([^"]+)"', s)
    t = GLASS_PAGE.get(os.path.basename(f)) or (m and GLASS_CAT.get(m.group(1)))
    s = re.sub(r'(<body[^>]*?) data-glass="[^"]*"', r'\1', s, count=1)
    return re.sub(r'<body\b', f'<body data-glass="{t}"', s, count=1) if t else s

# Every page with a footer uses the homepage footer: empty site-map block, no donate/idea pitch,
# and footer-v2.css / footer-v2.js (compact columns, language pills, X credit).
# footer-v2.js folds the existing tagline, credits, and licence into "Credits & licence".
# site.js already adds the "How to cite" line (page title + accessed date). Kids.html redirects have no footer.
# Translated pages keep their own tagline, credits, licence, and department lines. The generic copyright
# sentence is swapped for the one already on that language's homepage. Photo-specific copyright lines stay.
EMPTY_FOOTER_MAP = '<!-- FOOTER-MAP:START --><!-- FOOTER-MAP:END -->'
FOOT_LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')
FV2_VER = '20261103a'
_MAP_RX = re.compile(r'<!-- FOOTER-MAP:START -->[\s\S]*?<!-- FOOTER-MAP:END -->')
_P_RX = re.compile(r'<p\b[^>]*>.*?</p>\s*', re.S)
# Short copyright line (no Pexels / site-map links). The homepage line is this sentence plus the Pexels clause.
_GENERIC_COPY = {
    'en': ('<p>&copy; 2026 Saving Planets • Positive action for a thriving Earth • Page verified October 2026</p>',
           '<p>&copy; 2026 Saving Planets • Positive action for a thriving Earth</p>'),
    'fr': ('<p>© 2026 Saving Planets • Agir positivement pour une Terre florissante • Page vérifiée en octobre 2026</p>',
           '<p>© 2026 Saving Planets • Agir positivement pour une Terre florissante</p>'),
    'es': ('<p>© 2026 Saving Planets • Acción positiva por una Tierra próspera • Página verificada en octubre de 2026</p>',
           '<p>© 2026 Saving Planets • Acción positiva por una Tierra próspera</p>'),
    'ar': ('<p>© 2026 Saving Planets • عمل إيجابي من أجل أرض مزدهرة • تم التحقق من الصفحة في أكتوبر 2026</p>',
           '<p>© 2026 Saving Planets • عمل إيجابي من أجل أرض مزدهرة</p>'),
    'it': ('<p>© 2026 Saving Planets • Azione positiva per una Terra in salute • Pagina verificata a ottobre 2026</p>',
           '<p>© 2026 Saving Planets • Azione positiva per una Terra in salute</p>'),
    'he': ('<p>© 2026 Saving Planets • פעולה חיובית למען כדור ארץ משגשג • הדף אומת באוקטובר 2026</p>',
           '<p>© 2026 Saving Planets • פעולה חיובית למען כדור ארץ משגשג</p>'),
}

def foot_lang(path):
    d = os.path.dirname(path).replace('\\', '/')
    return d if d in FOOT_LANGS else 'en'

def homepage_copyright(lang):
    """The copyright paragraph already published on that language's homepage."""
    path = 'index.html' if lang == 'en' else f'{lang}/index.html'
    foot = re.search(r'<footer\b.*?</footer>', rd(path), re.S)
    if not foot: raise SystemExit('no footer on ' + path)
    for para in re.findall(r'<p\b[^>]*>.*?</p>', foot.group(0), re.S):
        if 'Pexels' in para and 'sitemap.xml' in para: return para
    raise SystemExit('no homepage copyright paragraph on ' + path)

def _strip_pitch(foot):
    """Drop the donate/idea paragraphs. Match the mailto and the criteria/donate links, in any language."""
    def repl(m):
        para = m.group(0)
        if 'mailto:ideas@savingplanets.com?subject=Solution' in para: return ''
        if 'About.html#criteria' in para and 'index.html#solutions' in para: return ''
        return para
    return _P_RX.sub(repl, foot)

def _fv2_block(path):
    pre = '' if foot_lang(path) == 'en' else '../'
    return (f'<!-- FV2:START --><link rel="stylesheet" href="{pre}footer-v2.css?v={FV2_VER}">'
            f'<script src="{pre}footer-v2.js?v={FV2_VER}" defer></script><!-- FV2:END -->')

def _ensure_fv2(s, path):
    """Load the same footer-v2 assets as the homepage. Leave a page that already loads them (including the critical-CSS preload form) alone."""
    if 'footer-v2.css' in s and 'footer-v2.js' in s: return s
    block = _fv2_block(path)
    if '<!-- PWA-JS:START -->' in s: return s.replace('<!-- PWA-JS:START -->', block + '<!-- PWA-JS:START -->', 1)
    if '</body>' in s: return s.replace('</body>', block + '</body>', 1)
    return s

def apply_footer_html(path, s, home_copy):
    """Empty the site-map block, remove the donate pitch, and use the homepage copyright when the page still has the short generic line."""
    if os.path.basename(path) == 'Kids.html': return s
    m = re.search(r'<footer\b.*?</footer>', s, re.S)
    if not m: return s
    foot = m.group(0)
    if foot.startswith('<footer class="sp-mini-foot"'): return s  # Search is copied from Contact in a second pass
    new = _MAP_RX.sub(EMPTY_FOOTER_MAP, foot, count=1) if _MAP_RX.search(foot) else foot.replace('<footer>', '<footer>' + EMPTY_FOOTER_MAP, 1)
    new = _strip_pitch(new)
    lang = foot_lang(path)
    for old in _GENERIC_COPY[lang]:
        if old in new:
            new = new.replace(old, home_copy[lang], 1)
            break
    s = s if new == foot else s[:m.start()] + new + s[m.end():]
    return _ensure_fv2(s, path)

def apply_search_footer(path, s):
    """Search kept a one-line legal footer. Use the same footer as Contact in that language (localized, already cleaned)."""
    lang = foot_lang(path)
    donor_path = 'Contact.html' if lang == 'en' else f'{lang}/Contact.html'
    donor = re.search(r'<footer\b.*?</footer>', rd(donor_path), re.S)
    if not donor: return s
    m = re.search(r'<footer\b.*?</footer>', s, re.S)
    if not m: return s
    s = s[:m.start()] + donor.group(0) + s[m.end():]
    return _ensure_fv2(s, path)

def apply_footers():
    """Homepage footer policy on every page that has a footer, in en/fr/es/ar/it/he. Does not rewrite the English homepage."""
    home_copy = {lang: homepage_copyright(lang) for lang in FOOT_LANGS}
    n = 0
    files = []
    for lang in FOOT_LANGS:
        files.extend(sorted(glob.glob('*.html' if lang == 'en' else f'{lang}/*.html')))
    for f in files:
        if os.path.basename(f) == 'Search.html' or f == 'index.html': continue
        s = rd(f)
        s2 = apply_footer_html(f, s, home_copy)
        if s2 != s: wr(f, s2); n += 1
    for lang in FOOT_LANGS:
        f = 'Search.html' if lang == 'en' else f'{lang}/Search.html'
        if not os.path.exists(f): continue
        s = rd(f); s2 = apply_search_footer(f, s)
        if s2 != s: wr(f, s2); n += 1
    home = rd('index.html')
    if apply_footer_html('index.html', home, home_copy) != home:
        raise SystemExit('footer policy would have changed the English homepage')
    return n

def fix(f):
    s = rd(f)
    if '<nav id="topnav">' not in s or '<footer>' not in s: return 0
    # extras.css
    if 'extras.css' not in s: s = s.replace('</head>', CSS + '\n</head>', 1)
    else: s = re.sub(r'extras\.css\?v=[0-9a-z]+', f'extras.css?v={V}', s)
    # glass theme tint (Oct 14): data-glass on <body> from page/category
    s = set_glass(f, s)
    # <main> landmark
    if '<main' not in s:
        i = s.index('<nav id="topnav">'); j = s.index('</nav>', i) + len('</nav>')
        s = s[:j] + '<main id="main">' + s[j:]
        k = s.index('<footer>'); s = s[:k] + '</main>\n' + s[k:]
    # landmark must start right after the top nav (hero banners included)
    i = s.index('<nav id="topnav">'); j = s.index('</nav>', i) + len('</nav>')
    mm = re.search(r'<main id="[^"]+"[^>]*>', s)  # Oct 17: World_Map has class=wm-main
    if mm.start() > j and re.search(r'<(section|p|div)\b', s[j:mm.start()]):
        tag = mm.group(0); s = s[:mm.start()] + s[mm.end():]; s = s[:j] + tag + s[j:]
    mid = re.search(r'<main id="([^"]+)"', s).group(1)
    # skip link -> existing target
    m = re.search(r'<a class="skip-link" href="#([^"]+)"', s)
    if m and not re.search(r'id="' + re.escape(m.group(1)) + '"', s): s = s.replace(m.group(0), f'<a class="skip-link" href="#{mid}"', 1)
    # video labels
    h1 = re.sub(r'<[^>]+>', '', (re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S) or re.search(r'<title>([^|<]*)', s)).group(1)).strip()
    s = re.sub(r'<video (?![^>]*aria-label)(?![^>]*class="hero-video")', lambda _: f'<video aria-label="{esc(html.unescape(h1))} video" ', s)
    # Footer site map stays empty, matching the homepage. Sitemap.html is the directory.
    # apply_footers() (called from main) also strips the donate pitch and adds footer-v2.
    rx = re.compile(r'<!-- FOOTER-MAP:START -->[\s\S]*?<!-- FOOTER-MAP:END -->')
    s = rx.sub(EMPTY_FOOTER_MAP, s) if rx.search(s) else s.replace('<footer>', '<footer>' + EMPTY_FOOTER_MAP, 1)
    return wr(f, s)

def main():
    hl = hubs()
    for i, l in enumerate(['fr', 'es', 'ar', 'it']):
        p = f'i18n/{l}.json'; m = json.load(open(p, encoding='utf8')); n0 = dict(m)
        for k, v in UI.items():
            if i < len(v): m.setdefault(k, v[i])
        if m != n0: json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    write_generated('Sitemap.html', sitemap_page(hl))
    n = sum(fix(f) for f in sorted(os.listdir('.')) if f.endswith('.html') and not f.startswith('google'))
    n += apply_footers()
    pl = rd('i18n/pages.txt')
    if 'Sitemap.html' not in pl.split(): open('i18n/pages.txt', 'w', encoding='utf8').write(pl.rstrip('\n') + '\nSitemap.html\n')
    import sitemap_pages
    sitemap_pages.ensure_url('https://www.savingplanets.com/Sitemap.html', '2026-10-13')
    print(f'site-extras: footer map + main landmark on {n} changed pages; Sitemap.html ({sum(len(x[2]) for x in hl)} solutions in {len(hl)} hubs)')

if __name__ == '__main__':
    if '--footer-only' in sys.argv:
        print(f'site-extras: homepage footer policy on {apply_footers()} pages')
    else:
        main()
