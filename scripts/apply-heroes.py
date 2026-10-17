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
for lang in ('', 'fr/', 'es/', 'ar/', 'it/'):  # Oct 16: + Italian (its MAP pages showed the default ocean hero)
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
    # Oct 16: the hero is the page's Ryugu photo; the line under it named an EPIC Earth image
    'Hayabusa2_Torifune': ('Ryugu_Hayabusa2.jpg', 'JAXA Hayabusa2 ONC data, processed by Anonymsiy (CC BY 4.0)'),
    # Oct 17: approved batch (A, B, D, G, H, N)
    'Parker_Solar_Probe': ('SDO_Sun.jpg', 'NASA/SDO'), 'SOHO': ('SDO_Sun.jpg', 'NASA/SDO'),
    'CryoSat': ('Labrador_Sea_Ice_ISS.jpg', 'NASA (ISS070-E-086805, Feb. 3, 2024)'),
    'International_Coastal_Cleanup': ('Bahamas_Ocean_ISS.jpg', 'NASA, International Space Station'),
    'The_SeaCleaners': ('PlasticBank_Indonesia_STS66.jpg', 'NASA (STS-66)'),
    'WeForest': ('Kilimanjaro_STS72.jpg', 'NASA (STS-72)'),
    'Enceladus': ('Enceladus_Geyser_Basin.jpg', 'NASA/JPL/Space Science Institute (PIA11688)'),
    # Oct 16 (agency batch): 20 new solutions, public-domain NASA/NOAA images
    'International_Charter': ('Missouri_Flood_Hamburg_EO1.jpg', 'NASA Earth Observatory (EO-1 ALI, July 17, 2011)'),
    'Copernicus_EMS': ('Canada_Wildfires_ISS_2025b.jpg', 'NASA (ISS073-E-0420617, Aug. 3, 2025)'),
    'FIRMS': ('Canada_Wildfires_ISS_2025.jpg', 'NASA (ISS073-E-0420604, Aug. 3, 2025)'),
    'UNEP_MARS': ('EMIT_Methane_Plumes_Uzbekistan.jpg', 'NASA/JPL-Caltech (PIA26113)'),
    'GLOBE_Program': ('Pacific_Clouds_Sunset_ISS.jpg', 'NASA (ISS074-E-0046371, Jan. 3, 2026)'),
    'Argo': ('NOAA_Deep_SOLO_Float_2018.jpg', 'NOAA (Deep SOLO float deployment from R/V Kaʻimikai-O-Kanaloa, 2018)'),
    'Argos': ('Loggerhead_Release_MINWR.jpg', 'NASA (2010-5237)'),
    'Coral_Reef_Watch': ('Great_Barrier_Reef_ISS_2022.jpg', 'NASA (ISS068-E-004262, Sept. 30, 2022)'),
    'RCM': ('Labrador_Sea_Ice_ISS.jpg', 'NASA (ISS070-E-086805, Feb. 3, 2024)'),
    'ATLAS': ('Hawaii_Island_ISS_2024.jpg', 'NASA (ISS072-E-421839, Dec. 28, 2024)'),
    'Pan-STARRS': ('Comet_PANSTARRS_ISS_2026.jpg', 'NASA (ISS074-E-0480485, April 17, 2026)'),
    'Catalina_Sky_Survey': ('Asteroid_2018LA_CSS.jpg', 'NASA/JPL-Caltech/CSS-Univ. of Arizona (PIA22468)'),
    'ESA_NEOCC': ('Goldstone_Radar_2011UL21.jpg', 'NASA/JPL-Caltech (PIA26384)'),
    'EFFIS': ('Portugal_Wildfires_ISS_2018.jpg', 'NASA (ISS056-E-127068, Aug. 6, 2018)'),
    'JPSS': ('JPSS2_Atlas_V_Launch_Pad.jpg', 'NASA/Liz Wilk (KSC-20221109-PH-LNW01_0001)'),
    'GSMaP': ('GPM_Core_Observatory_GMI.jpg', 'NASA/Goddard (GPM Core Observatory)'),
    'CAMS': ('Sumatra_Smoke_Singapore_MODIS.jpg', 'NASA Earth Observatory (Aqua MODIS, June 19, 2013)'),
    'GloFAS': ('Pakistan_Flood_Kheshgi_2010.jpg', 'NASA Earth Observatory (ASTER on Terra, Aug. 4, 2010)'),
    'Copernicus_Marine': ('North_Atlantic_Bloom_MODIS.jpg', 'NASA/GSFC/Jeff Schmaltz/MODIS Land Rapid Response Team'),
    'OpenET': ('Garden_City_Kansas_Landsat.jpg', 'NASA/GSFC/Landsat (Sept. 25, 2000)'),
}
SI_T = {'': 'Created by SI and Biological SI Partner', 'fr/': 'Créé par SI et Biological SI Partner', 'es/': 'Creado por SI y Biological SI Partner', 'ar/': 'أُنشئ بواسطة SI وBiological SI Partner', 'it/': 'Creato da SI e Biological SI Partner'}
IMG_T = {'': 'Image', 'fr/': 'Image', 'es/': 'Imagen', 'ar/': 'الصورة', 'it/': 'Immagine'}
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
for lang in ('', 'fr/', 'es/', 'ar/', 'it/'):
    for p, (img, credit) in chosen.items():
        f = f'{lang}{p}.html'
        if not os.path.exists(f): continue
        s = open(f, encoding='utf-8').read(); cls = 'hp-' + _slug(p)
        s2 = s if re.search(r'<body[^>]*class="[^"]*\b' + cls + r'\b', s) else re.sub(r'(<body[^>]*class=")', r'\g<1>' + cls + ' ', s, count=1)
        if not re.search(r'<body[^>]*class=', s2): s2 = re.sub(r'<body', f'<body class="{cls}"', s2, count=1)
        if credit:  # the credit line right under the hero must name this hero's image
            txt = SI_T[lang] if credit.startswith('Created by SI') else f'{IMG_T[lang]}: {credit}'
            # keep an existing (possibly translated) credit that already names the same image: every acronym / ID matches
            keys = re.findall(r'[A-Z][A-Z0-9-]+|[\w-]*\d[\w-]*', credit)
            cur = re.search(r'<section class="page-hero[^"]*"[^>]*>.*?</section>\s*<p class="photo-credit">([^<]*)', s2, flags=re.S)
            if not (cur and keys and all(k in cur.group(1) for k in keys)):
                s2 = re.sub(r'(<section class="page-hero[^"]*"[^>]*>.*?</section>\s*<p class="photo-credit">)[^<]*', lambda mm: mm.group(1) + txt + '.', s2, count=1, flags=re.S)
        if credit and not re.search(r'<section class="page-hero[^"]*"[^>]*>.*?</section>\s*<p class="photo-credit">', s2, flags=re.S) and 'class="hero-credit"' not in s2:
            s2 = re.sub(r'(<section class="page-hero[^"]*"[^>]*>.*?)(</section>)', lambda mm: mm.group(1) + f'<span class="hero-credit">{SI_T[lang] if credit.startswith("Created by SI") else credit}</span>' + mm.group(2), s2, count=1, flags=re.S)
        if lang: s2 = s2.replace('<span class="hero-credit">Created by SI and Biological SI Partner</span>', f'<span class="hero-credit">{SI_T[lang]}</span>')
        if s2 != s: open(f, 'w', encoding='utf-8').write(s2); m += 1
print(f'apply-heroes: {len(chosen)} per-page photo heroes, {m} files updated')
# Oct 16 (user): the credit right under a banner must name what the banner actually shows. A page left on the shared
# space hero (styles.css: body.toc-sub .page-hero.space-hero -> assets/Saturn.jpg, NASA's Cassini) gets that credit
# instead of its own photo's (that photo is credited where it appears further down the page).
SHARED_SPACE = 'NASA (Cassini)'
for f in flagged:
    print(f'WARNING apply-heroes: {f} has no themed hero; add it to PAGE_HERO or MAP')
    if 'space-hero' not in re.search(r'<section class="(page-hero[^"]*)"', open(f, encoding='utf-8').read()).group(1).split(): continue
    for lang in ('', 'fr/', 'es/', 'ar/', 'it/'):
        g = lang + f
        if not os.path.exists(g): continue
        s = open(g, encoding='utf-8').read()
        s2 = re.sub(r'(<section class="page-hero[^"]*"[^>]*>.*?</section>\s*<p class="photo-credit">)[^<]*(?=</p>)',
                    lambda mm: mm.group(1) + f'{IMG_T[lang]}: {SHARED_SPACE}.', s, count=1, flags=re.S)
        if s2 != s: open(g, 'w', encoding='utf-8').write(s2); print(f'apply-heroes: {g} credit -> shared space hero')
