#!/usr/bin/env python3
"""Themed page heroes (standing rule, Oct 14 2026): every page hero depicts the page's main theme.
Idempotent post-process for EN/fr/es/ar. Images live in assets/hero/<key>-{800,1600}.{webp,jpg}; CSS in styles.css."""
import re, os
MAP = {'Kids_Map': ('kids', 'NASA EPIC'), 'World_Map': ('kids', 'NASA EPIC'), 'Satellite_Explorer': ('satx', 'NASA/JPL-Caltech'), 'Lesson_Builder': ('lesson', 'USFWS'),
       'Teachers': ('teach', 'USFWS'), 'About': ('about', 'NASA'), 'Contact': ('about', 'NASA'), 'Press': ('about', 'NASA'),
       'Community': ('help', 'NPS'), 'Find_a_Cleanup': ('help', 'NPS'), 'Ways_to_Help': ('help', 'NPS'),
       'Glossary': ('learn', 'NASA'), 'Myth_vs_Fact': ('learn', 'NASA'), 'Sitemap': ('learn', 'NASA'), '404': ('learn', 'NASA'),
       'Rawanes_Mission_Log': ('mission', 'NASA'), 'Privacy': ('about', 'NASA'), 'Editorial_Policy': ('learn', 'NASA'),
       'Corrections': ('learn', 'NASA'), 'Press_Kit': ('about', 'NASA'), 'Topics': ('learn', 'NASA')}
n = 0
for lang in ('', 'fr/', 'es/', 'ar/'):
    for p, (k, c) in MAP.items():
        f = f'{lang}{p}.html'
        if not os.path.exists(f):
            continue
        s = open(f, encoding='utf-8').read()
        s2 = re.sub(r'<section class="page-hero"( id="[^"]*")?>(<div class="page-hero-content">.*?</div>)</section>',
                    lambda m: f'<section class="page-hero hero-{k}"{m.group(1) or ""}>{m.group(2)}<span class="hero-credit">{c}</span></section>',
                    s, count=1, flags=re.S)
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2); n += 1
print(f'apply-heroes: {n} pages updated')

# ---- Per-page themed photo heroes (Oct 14 2026) -------------------------------------------------
# Solution/hub pages that would otherwise show a generic background (default Saturn space-hero,
# Nebula hub-hero, default ocean page-hero). Each page gets body class hp-<slug> and a CSS rule in
# styles.css between PAGE-HEROES markers. Pages not listed fall back to their own og:image when it
# is a themed asset (not a generic one); anything left generic is flagged as WARNING in the build.
GENERIC = {'Saturn.jpg', 'Nebula.jpg', 'Nebula2.jpg', 'SavePlanetLogo.jpg'}
NASA = 'NASA'
PAGE_HERO = {  # page: (asset, credit shown only if the page has no photo-credit yet)
    'Deforestation': ('Amazon_Clouds_ISS.jpg', 'NASA (ISS013-E-74843)'),
    'Earth_Observation': ('EPIC_Earth.jpg', 'NASA/NOAA DSCOVR EPIC'),
    'Lakes': ('Great_Lakes_MODIS.jpg', 'NASA GSFC MODIS Land Rapid Response Team'),
    'Oceans': ('North_Pacific_ISS.jpg', 'NASA (iss073e0257194)'),
    'Rivers': ('Mississippi_River_PIA23534.jpg', 'NASA/JPL (PIA23534)'),
    'Planetary_Defense': ('Hera.jpg', 'ESA – Science Office'),
    'Space_Weather': ('SDO_Sun.jpg', 'NASA/SDO'),
    'Space_Disposal': ('Progress_Reentry.jpg', 'NASA, ISS Expedition 29 (iss029e034092)'),
    'Astroscale': ('Satellite_Servicing_Arm_GSFC.jpg', NASA),
    'ClearSpace': ('ATV1_Departure_ISS.jpg', NASA),
    'PRELUDE': ('ATV1_Departure_ISS.jpg', NASA),
    'Ocean_Cleanup': ('theoceancleanup.jpg', 'Created by SI and Biological SI Partner'),
    '4ocean': ('OceanBeach.JPG', 'Created by SI and Biological SI Partner'), 'Plastic_Bank': ('OceanBeach.JPG', 'Created by SI and Biological SI Partner'),
    'Project-Rawane': ('Moon_Crossing_Earth.jpg', 'NASA/NOAA DSCOVR EPIC'),
    'Space': ('ISS_Flyaround_2021.jpg', 'NASA'),
    'Restoring_the_Lake_Depths': ('Lake_Tahoe_ISS.jpg', 'NASA (ISS071-E-14284)'),
    'Terraformation': ('Yishan_Tree.jpg', None), 'Three_Trees': ('ThreeTrees2.jpg', None),
    # Oct 15: new solutions
    'FireSat': ('Rim_Fire_MODIS.jpg', 'NASA (MODIS, Terra satellite)'), 'Eden_People_Planet': ('Kilimanjaro_STS72.jpg', 'NASA (STS-72)'),
    'Waterkeeper_Alliance': ('NYC_Hudson_Harbor.jpg', 'NASA, Space Shuttle'), 'SeaTrees': ('Mangrove_Delta_ISS.jpg', 'NASA, International Space Station'),
    'Living_Lakes': ('Lake_Tahoe_ISS.jpg', 'NASA (ISS071-E-14284)'),
    # Oct 15 (batch 2): 17 new solutions
    'EMIT': ('EMIT_Methane_Fingerprint.jpg', 'NASA/JPL-Caltech'),
    'GEDI': ('ISS_Flyaround_2021.jpg', 'NASA'),
    'OCO-2': ('Global_Plant_Fluorescence.jpg', 'NASA/JPL-Caltech'),
    'Sentinel-5P': ('Clouds_Limb_ISS.jpg', 'NASA'),
    'PREFIRE': ('LEO_View.jpg', 'NASA, ISS Expedition 23 crew (iss023e057948)'),
    'HydroGNSS': ('Danube_Delta_GSFC.jpg', 'NASA'),
    'Sentinel-3': ('Bahamas_Ocean_ISS.jpg', 'NASA, International Space Station'),
    'Libera': ('EPIC_Earth.jpg', 'NASA/NOAA DSCOVR EPIC'),
    'Surfrider_Foundation': ('North_Pacific_ISS.jpg', 'NASA (iss073e0257194)'),
    'Heal_the_Bay': ('Lake_Shore_Cleanup_NPS.jpg', 'NPS photo, Lake Roosevelt National Recreation Area'),
    'Plastic_Odyssey': ('PlasticBank_Indonesia_STS66.jpg', 'NASA (STS-66)'),
    'Trout_Unlimited': ('Klamath_River.jpg', 'NASA (PIA26448)'),
    'Chesapeake_Bay_Foundation': ('Baltimore_DC_Skylab.jpg', 'NASA'),
    'Keep_Tahoe_Blue': ('Lake_Tahoe_ISS.jpg', 'NASA (ISS071-E-14284)'),
    'American_Forests': ('Threetrees3.jpg', 'SI Partner'),
    'Plant-for-the-Planet': ('Yishan_Tree.jpg', 'SI Partner'),
    'Dragonfly': ('Titan.jpg', 'NASA'),
}
SI_T = {'': 'Created by SI and Biological SI Partner', 'fr/': 'Créé par SI et Biological SI Partner', 'es/': 'Creado por SI y Biological SI Partner', 'ar/': 'أُنشئ بواسطة SI وBiological SI Partner'}
IMG_T = {'': 'Image', 'fr/': 'Image', 'es/': 'Imagen', 'ar/': 'الصورة'}
def _slug(p): return re.sub(r'[^a-z0-9]+', '-', p.lower()).strip('-')
def _has_rule(css, s):
    b = re.search(r'<body[^>]*class="([^"]*)"', s)
    return any(c.endswith('-page') and re.search(r'body\.toc-sub\.' + re.escape(c) + r'[^{]*\.page-hero', css) for c in (b.group(1).split() if b else []))
css = open('styles.css', encoding='utf-8').read()
chosen, flagged = {}, []
for f in sorted(os.listdir('.')):
    if not f.endswith('.html') or f.startswith('google'): continue
    s = open(f, encoding='utf-8').read()
    h = re.search(r'<section class="(page-hero[^"]*)"', s)
    if not h: continue
    p = f[:-5]; hc = h.group(1).split()
    if p in PAGE_HERO: chosen[p] = PAGE_HERO[p]; continue
    if any(c.startswith('hero-') or c in ('af-hero', 'sol-hero') for c in hc) or p in MAP: continue  # af/sol heroes carry their own themed banners
    if 'hub-hero' not in hc and _has_rule(css, s): continue
    og = re.search(r'og:image" content="[^"]*/assets/([^"/]+)"', s)
    if not og:  # Oct 16: build-og swaps og:image to assets/og/<lang>/<page>.jpg share cards; keep the photo hero already chosen for this page
        prev = re.search(r'\.hp-' + re.escape(_slug(p)) + r" \.page-hero\[class\]\{[^}]*url\('assets/([^'/]+)'\)", css)
        if prev and os.path.exists('assets/' + prev.group(1)): chosen[p] = (prev.group(1), None); continue
    if og and og.group(1) not in GENERIC and os.path.exists('assets/' + og.group(1)) and '<p class="photo-credit">' in s:
        chosen[p] = (og.group(1), None)
    else:
        flagged.append(f)
rules = ''.join(f"body.toc-sub[class].hp-{_slug(p)} .page-hero[class]{{background:linear-gradient(180deg,rgba(0,20,40,.35),rgba(0,20,40,.6)),url('assets/{img}') center/cover no-repeat}}\n" for p, (img, _) in sorted(chosen.items()))
block = '/* PAGE-HEROES:START (generated by scripts/apply-heroes.py) */\n' + rules + '/* PAGE-HEROES:END */'
css2 = re.sub(r'/\* PAGE-HEROES:START.*?PAGE-HEROES:END \*/', lambda m: block, css, flags=re.S) if 'PAGE-HEROES:START' in css else css.rstrip('\n') + '\n' + block + '\n'
if css2 != css: open('styles.css', 'w', encoding='utf-8').write(css2)
m = 0
for lang in ('', 'fr/', 'es/', 'ar/'):
    for p, (img, credit) in chosen.items():
        f = f'{lang}{p}.html'
        if not os.path.exists(f): continue
        s = open(f, encoding='utf-8').read(); cls = 'hp-' + _slug(p)
        s2 = s if re.search(r'<body[^>]*class="[^"]*\b' + cls + r'\b', s) else re.sub(r'(<body[^>]*class=")', r'\g<1>' + cls + ' ', s, count=1)
        if not re.search(r'<body[^>]*class=', s2): s2 = re.sub(r'<body', f'<body class="{cls}"', s2, count=1)
        if credit:  # the credit line right under the hero must name this hero's image
            txt = SI_T[lang] if credit.startswith('Created by SI') else f'{IMG_T[lang]}: {credit}'
            s2 = re.sub(r'(<section class="page-hero[^"]*"[^>]*>.*?</section>\s*<p class="photo-credit">)[^<]*', lambda mm: mm.group(1) + txt + '.', s2, count=1, flags=re.S)
        if credit and not re.search(r'<section class="page-hero[^"]*"[^>]*>.*?</section>\s*<p class="photo-credit">', s2, flags=re.S) and 'class="hero-credit"' not in s2:
            s2 = re.sub(r'(<section class="page-hero[^"]*"[^>]*>.*?)(</section>)', lambda mm: mm.group(1) + f'<span class="hero-credit">{SI_T[lang] if credit.startswith("Created by SI") else credit}</span>' + mm.group(2), s2, count=1, flags=re.S)
        if lang: s2 = s2.replace('<span class="hero-credit">Created by SI and Biological SI Partner</span>', f'<span class="hero-credit">{SI_T[lang]}</span>')
        if s2 != s: open(f, 'w', encoding='utf-8').write(s2); m += 1
print(f'apply-heroes: {len(chosen)} per-page photo heroes, {m} files updated')
for f in flagged: print(f'WARNING apply-heroes: {f} has no themed hero; add it to PAGE_HERO or MAP')
