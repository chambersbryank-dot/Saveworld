#!/usr/bin/env python3
"""Site-wide structure + accessibility (Oct 13). Idempotent; run BEFORE i18n-build (weekly-sync does).
- Footer site map (all 10 hubs + key pages) on every English page, and Sitemap.html (every hub + solution).
- <main id="main"> landmark around page content, skip links pointing at it, aria-labels on <video>.
- extras.css (contrast fixes, footer map, About sources list) linked on every page."""
import re, os, importlib.util, html, json
rd = lambda f: open(f, encoding='utf8').read()
def wr(f, s):
    if rd(f) != s: open(f, 'w', encoding='utf8').write(s); return 1
    return 0
esc = lambda s: html.escape(s, quote=True)
V = '20261014u'
CSS = f'<link rel="stylesheet" href="extras.css?v={V}">'
spec = importlib.util.spec_from_file_location('sol', 'scripts/build-solutions-index.py'); SOL = importlib.util.module_from_spec(spec); spec.loader.exec_module(SOL)
KEY = [('Solutions.html', 'All Solutions'), ('Search.html', 'Search'), ('Glossary.html', 'Glossary'), ('Teachers.html', 'Teacher Sheets'),
       ('Amazing_Facts.html', 'Amazing Facts'), ('Kids_Map.html', 'Kids Planet Map'), ('Lesson_Builder.html', 'Lesson Plan Builder'), ('Satellite_Explorer.html', 'Satellite Explorer'), ('Ways_to_Help.html', 'Ways to Help'), ('About.html', 'About'), ('Press.html', 'Press &amp; media'),
       ('Contact.html', 'Contact'), ('Topics.html', 'Topics A to Z'), ('Privacy.html', 'Privacy'), ('Editorial_Policy.html', 'Editorial Policy'), ('Corrections.html', 'Corrections'), ('Sitemap.html', 'Site Map')]
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
    hub_links = ''.join(f'<li><a href="{f}">{esc(n)}</a></li>' for f, n, _ in hl)
    key_links = ''.join(f'<li><a href="{f}">{n}</a></li>' for f, n in KEY)
    return ('<!-- FOOTER-MAP:START --><div class="footer-map" role="navigation" aria-label="Site map"><div class="fm-col"><h2 class="fm-h">Hubs</h2><ul>' + hub_links +
            '</ul></div><div class="fm-col"><h2 class="fm-h">Explore</h2><ul>' + key_links + '</ul></div></div><!-- FOOTER-MAP:END -->')

def sitemap_page(hl):
    tpl = rd('Contact.html'); head, b = tpl.split('<body', 1)
    nav = re.search(r'(<nav id="topnav">.*?</nav>)', b, re.S).group(1)
    footer = re.sub(r'<script[^>]*></script>', '', re.search(r'(<footer>.*?</footer>)', b, re.S).group(1))
    jsv = re.search(r'site\.js\?v=([0-9a-z]+)', b).group(1)
    desc = 'Every hub and solution on Saving Planets, in one list.'
    h = head.replace('Contact.html', 'Sitemap.html').replace('<title>Contact | Saving Planets</title>', '<title>Site Map | Saving Planets</title>')
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
             'space': 'space', 'project-r': 'space', 'planetary-defense': 'defense', 'space-weather': 'sun'}
GLASS_PAGE = {'Titan.html': 'titan', 'ExoMars_Rosalind_Franklin.html': 'mars', 'ESCAPADE.html': 'mars', 'MMX.html': 'mars',
              'Oceans.html': 'ocean', 'Lakes.html': 'lakes', 'Rivers.html': 'rivers', 'Deforestation.html': 'forests', 'Space.html': 'space',
              'Earth_Observation.html': 'earth', 'Planetary_Defense.html': 'defense', 'Space_Weather.html': 'sun', 'Space_Disposal.html': 'space', 'Kids_Map.html': 'ocean', 'Lesson_Builder.html': 'earth', 'Satellite_Explorer.html': 'space'}
def set_glass(f, s):
    m = re.search(r'<meta name="sp:category" content="([^"]+)"', s)
    t = GLASS_PAGE.get(os.path.basename(f)) or (m and GLASS_CAT.get(m.group(1)))
    s = re.sub(r'(<body[^>]*?) data-glass="[^"]*"', r'\1', s, count=1)
    return re.sub(r'<body\b', f'<body data-glass="{t}"', s, count=1) if t else s

def fix(f, fm):
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
    mm = re.search(r'<main id="[^"]+">', s)
    if mm.start() > j and re.search(r'<(section|p|div)\b', s[j:mm.start()]):
        tag = mm.group(0); s = s[:mm.start()] + s[mm.end():]; s = s[:j] + tag + s[j:]
    mid = re.search(r'<main id="([^"]+)"', s).group(1)
    # skip link -> existing target
    m = re.search(r'<a class="skip-link" href="#([^"]+)"', s)
    if m and not re.search(r'id="' + re.escape(m.group(1)) + '"', s): s = s.replace(m.group(0), f'<a class="skip-link" href="#{mid}"', 1)
    # video labels
    h1 = re.sub(r'<[^>]+>', '', (re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S) or re.search(r'<title>([^|<]*)', s)).group(1)).strip()
    s = re.sub(r'<video (?![^>]*aria-label)(?![^>]*class="hero-video")', lambda _: f'<video aria-label="{esc(html.unescape(h1))} video" ', s)
    # footer site map
    rx = re.compile(r'<!-- FOOTER-MAP:START -->[\s\S]*?<!-- FOOTER-MAP:END -->')
    s = rx.sub(fm, s) if rx.search(s) else s.replace('<footer>', '<footer>' + fm, 1)
    return wr(f, s)

def main():
    hl = hubs(); fm = footer_map(hl)
    for i, l in enumerate(['fr', 'es', 'ar']):
        p = f'i18n/{l}.json'; m = json.load(open(p, encoding='utf8')); n0 = dict(m)
        for k, v in UI.items(): m.setdefault(k, v[i])
        if m != n0: json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    write_generated('Sitemap.html', sitemap_page(hl))
    n = sum(fix(f, fm) for f in sorted(os.listdir('.')) if f.endswith('.html') and not f.startswith('google'))
    pl = rd('i18n/pages.txt')
    if 'Sitemap.html' not in pl.split(): open('i18n/pages.txt', 'w', encoding='utf8').write(pl.rstrip('\n') + '\nSitemap.html\n')
    sm = rd('sitemap.xml')
    if 'savingplanets.com/Sitemap.html<' not in sm:
        open('sitemap.xml', 'w', encoding='utf8').write(sm.replace('  <url><loc>https://www.savingplanets.com/Contact.html</loc>', '  <url><loc>https://www.savingplanets.com/Sitemap.html</loc><lastmod>2026-10-13</lastmod></url>\n  <url><loc>https://www.savingplanets.com/Contact.html</loc>', 1))
    print(f'site-extras: footer map + main landmark on {n} changed pages; Sitemap.html ({sum(len(x[2]) for x in hl)} solutions in {len(hl)} hubs)')

if __name__ == '__main__':
    main()
