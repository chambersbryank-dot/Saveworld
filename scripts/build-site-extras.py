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

# English Learn / Courses / Teachers / kids education pages. Their footer matches the homepage
# (empty site map, Pexels copyright line, no donate/idea pitch). Solution pages and translations stay as they are.
# Homepage itself is emptied later by build-home-trim.py. This script only walks the repo root.
EDU_FOOTER = {
    'AP_IB_Physics.html', 'Aero_Guide.html', 'Aero_Lab.html', 'Aero_Math.html', 'Aerodynamics_I.html',
    'Aerospace_Structures.html', 'Aircraft_Performance.html', 'Amazing_Facts.html', 'Avionics_Systems_Engineering.html',
    'Big_Questions.html', 'Boarding_Pass.html', 'Cadets.html', 'Calculators.html', 'Calculus_I.html', 'Calculus_II.html',
    'Calculus_III.html', 'Capstone_Design.html', 'Careers.html', 'Circuits.html', 'Courses.html',
    'Delta_V_Calculator.html', 'Differential_Equations.html', 'Dynamics.html', 'Earth_Satellite_Explorer.html',
    'Engineering_Graphics_CAD.html', 'Flight_Dynamics_Controls.html', 'Fluid_Mechanics.html', 'General_Chemistry_I.html',
    'Glossary.html', 'Heat_Transfer.html', 'Hohmann_Transfer_Calculator.html', 'Homeschool.html',
    'Intro_to_Aerospace_Engineering.html', 'Intro_to_Programming.html', 'Kids_Map.html', 'Kids_World.html',
    'Learn.html', 'Learn_Aero.html', 'Learn_Chemistry.html', 'Learn_Engineering.html', 'Learn_Jet_Propulsion.html',
    'Learn_Math.html', 'Learn_Orbits.html', 'Learn_Physics.html', 'Learn_Rocket_Propulsion.html', 'Lesson_Builder.html',
    'Lesson_Plan.html', 'Lift_Equation_Calculator.html', 'Linear_Algebra.html', 'Mach_Number_Calculator.html',
    'Mechanics_of_Materials.html', 'Myth_or_Fact_Arcade.html', 'Myth_vs_Fact.html', 'Numerical_Methods.html',
    'Orbit_Lab.html', 'Orbit_Math.html', 'Orbital_Mechanics.html', 'Orbital_Period_Calculator.html',
    'Orbital_Velocity_Calculator.html', 'Orbits_Guide.html', 'Pendulum_Period_Calculator.html', 'Physics_Guide.html',
    'Physics_I.html', 'Physics_II.html', 'Physics_Lab.html', 'Physics_Math.html', 'Play_and_Learn.html',
    'Probability_Statistics.html', 'Projectile_Motion_Drag_Calculator.html', 'Propulsion.html',
    'Rotor_Hover_Power_Calculator.html', 'SI_Helper.html', 'Satellite_Explorer.html', 'Space_Passport.html',
    'Spacecraft_Design.html', 'Spot_the_Fire.html', 'Stall_Speed_Calculator.html', 'Statics.html', 'Student_Questions.html',
    'Sustainable_Aviation.html', 'Teacher_Guide.html', 'Teachers.html', 'Thermodynamics.html',
    'Thrust_to_Weight_Calculator.html',
}
EMPTY_FOOTER_MAP = '<!-- FOOTER-MAP:START --><!-- FOOTER-MAP:END -->'
_OLD_COPY = '<p>&copy; 2026 Saving Planets • Positive action for a thriving Earth • Page verified October 2026</p>'
_NEW_COPY = ('<p>&copy; 2026 Saving Planets • Positive action for a thriving Earth • Page verified October 2026. '
             'Lake and river photos: Pexels. <a href="sitemap.xml">Site map</a> • <a href="Contact.html">Contact</a></p>')
_PITCH = re.compile(
    r'<p>Plastic, forests, and energy are problems we can tackle together\. '
    r'<a href="mailto:ideas@savingplanets.com\?subject=Solution%20idea%20for%20Saving%20Planets">Send an idea</a> '
    r'or share a solution you know\.</p>\s*'
    r'<p>If your solution meets our <a href="About.html#criteria">solutions criteria</a>, we will add it to our solutions site\. '
    r"If you'd like to donate, visit our <a href=\"index.html#solutions\">Solutions page</a> and pick one that matches your interest\.</p>")

def education_footer(name, s):
    """Match the homepage footer on English education pages only. Other pages are unchanged."""
    if os.path.basename(name) not in EDU_FOOTER: return s
    m = re.search(r'<footer\b.*?</footer>', s, re.S)
    if not m: return s
    foot = m.group(0)
    rx = re.compile(r'<!-- FOOTER-MAP:START -->[\s\S]*?<!-- FOOTER-MAP:END -->')
    new = rx.sub(EMPTY_FOOTER_MAP, foot, count=1) if rx.search(foot) else foot
    new = new.replace(_OLD_COPY, _NEW_COPY, 1)
    new = _PITCH.sub('', new, count=1)
    return s if new == foot else s[:m.start()] + new + s[m.end():]

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
    # footer site map (education pages then match the homepage: empty map, no donate pitch)
    rx = re.compile(r'<!-- FOOTER-MAP:START -->[\s\S]*?<!-- FOOTER-MAP:END -->')
    s = rx.sub(fm, s) if rx.search(s) else s.replace('<footer>', '<footer>' + fm, 1)
    s = education_footer(f, s)
    return wr(f, s)

def main():
    hl = hubs(); fm = footer_map(hl)
    for i, l in enumerate(['fr', 'es', 'ar', 'it']):
        p = f'i18n/{l}.json'; m = json.load(open(p, encoding='utf8')); n0 = dict(m)
        for k, v in UI.items():
            if i < len(v): m.setdefault(k, v[i])
        if m != n0: json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    write_generated('Sitemap.html', sitemap_page(hl))
    n = sum(fix(f, fm) for f in sorted(os.listdir('.')) if f.endswith('.html') and not f.startswith('google'))
    pl = rd('i18n/pages.txt')
    if 'Sitemap.html' not in pl.split(): open('i18n/pages.txt', 'w', encoding='utf8').write(pl.rstrip('\n') + '\nSitemap.html\n')
    import sitemap_pages
    sitemap_pages.ensure_url('https://www.savingplanets.com/Sitemap.html', '2026-10-13')
    print(f'site-extras: footer map + main landmark on {n} changed pages; Sitemap.html ({sum(len(x[2]) for x in hl)} solutions in {len(hl)} hubs)')

if __name__ == '__main__':
    main()
