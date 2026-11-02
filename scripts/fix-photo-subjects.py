#!/usr/bin/env python3
"""Keep each named solution on its own photo, and describe that photo once.

Astroscale, GEDI, ALOS-4 and Eden were sharing pictures or repeating the page name
in the alt. Kilimanjaro (NASA STS-72) stays on Eden only. Justdiggit, Trees for the
Future and WeForest use the photos already on their solution cards. GEDI's further-info
link and amazing-fact use the Kibo instrument photo, not the station flyaround.
Idempotent. Run after apply-anim-banners.
"""
import glob, html, json, os, re

os.chdir(os.path.join(os.path.dirname(__file__), '..'))

KILI = 'Mount Kilimanjaro and the surrounding highlands in Tanzania, seen from the Space Shuttle'
GEDI = 'The GEDI forest-mapping laser mounted outside the Kibo module on the International Space Station'
KENYA = 'Southeast Kenya seen by the Copernicus Sentinel-2 satellite, with green vegetated land along the coast and drier land inland'
TANA = 'The Tana River winding across the land in Kenya, seen by the Copernicus Sentinel-2 satellite'
SEED = 'A tree seedling being planted on the Sioux Ranger District of Custer Gallatin National Forest'
ASTRO = "Artist's illustration of Astroscale's ADRAS-J spacecraft approaching a spent H-IIA rocket upper stage in orbit"
ALOS = "JAXA's 1/50 scale model of ALOS-4, with its PALSAR-3 radar antenna and solar arrays, at Tsukuba Space Center"

# Banner map. apply-anim-banners reads this. A full dump is a stable round-trip (indent=1).
CFG = 'assets/data/anim-banners.json'
cfg = json.load(open(CFG, encoding='utf8'))
cfg['images'].setdefault('assets/Kilimanjaro_STS72.jpg', {})['alt'] = KILI
cfg['images']['assets/hub/ESA_S2_Southeast_Kenya.jpg'] = {
    'credit': 'contains modified Copernicus Sentinel data (2023), processed by ESA',
    'alt': KENYA, 'pos': '50% 50%', 'r2': 'images/hub/ESA_S2_Southeast_Kenya.jpg',
}
cfg['images']['assets/hub/ESA_S2_Tana_River_Kenya.jpg'] = {
    'credit': 'contains modified Copernicus Sentinel data (2020), processed by ESA',
    'alt': TANA, 'pos': '50% 50%', 'r2': 'images/hub/ESA_S2_Tana_River_Kenya.jpg',
}
cfg['images']['assets/hub/USFS_Seedling_Planting_Custer_Gallatin.jpg'] = {
    'credit': 'U.S. Forest Service', 'alt': SEED, 'pos': '50% 40%',
    'r2': 'images/hub/USFS_Seedling_Planting_Custer_Gallatin.jpg',
}
cfg['pages']['Justdiggit.html'] = 'assets/hub/ESA_S2_Southeast_Kenya.jpg'
cfg['pages']['Trees_for_the_Future.html'] = 'assets/hub/ESA_S2_Tana_River_Kenya.jpg'
cfg['pages']['WeForest.html'] = 'assets/hub/USFS_Seedling_Planting_Custer_Gallatin.jpg'
for page in ('Justdiggit.html', 'Trees_for_the_Future.html', 'WeForest.html'):
    cfg['slides'].setdefault('curated', {})[page] = []
json.dump(cfg, open(CFG, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
open(CFG, 'a').write('\n')

# CSS hero fallbacks (related cards and the next solutions index read these).
css = open('styles.css', encoding='utf8').read()
css2 = css.replace(
    "body.toc-sub.trees-for-the-future-page .page-hero.space-hero { background: linear-gradient(180deg, rgba(0,20,40,0.35) 0%, rgba(0,20,40,0.6) 100%), url('assets/Kilimanjaro_STS72.jpg') center/cover no-repeat; }",
    "body.toc-sub.trees-for-the-future-page .page-hero.space-hero { background: linear-gradient(180deg, rgba(0,20,40,0.35) 0%, rgba(0,20,40,0.6) 100%), url('assets/hub/ESA_S2_Tana_River_Kenya.jpg') center/cover no-repeat; }",
).replace(
    "hp-justdiggit .page-hero[class]{background:linear-gradient(180deg,rgba(0,20,40,.35),rgba(0,20,40,.6)),url('assets/Kilimanjaro_STS72.jpg') center/cover no-repeat}",
    "hp-justdiggit .page-hero[class]{background:linear-gradient(180deg,rgba(0,20,40,.35),rgba(0,20,40,.6)),url('assets/hub/ESA_S2_Southeast_Kenya.jpg') center/cover no-repeat}",
).replace(
    "hp-weforest .page-hero[class]{background:linear-gradient(180deg,rgba(0,20,40,.35),rgba(0,20,40,.6)),url('assets/Kilimanjaro_STS72.jpg') center/cover no-repeat}",
    "hp-weforest .page-hero[class]{background:linear-gradient(180deg,rgba(0,20,40,.35),rgba(0,20,40,.6)),url('assets/hub/USFS_Seedling_Planting_Custer_Gallatin.jpg') center/cover no-repeat}",
)
if css2 != css:
    open('styles.css', 'w', encoding='utf8').write(css2)

TM = {
    'fr': {
        KILI: 'Le mont Kilimandjaro et les hautes terres alentour en Tanzanie, vus depuis la navette spatiale',
        GEDI: 'Le laser GEDI de cartographie des forêts, monté à l’extérieur du module Kibo sur la Station spatiale internationale',
        ASTRO: 'Illustration du vaisseau ADRAS-J approchant un étage supérieur usagé de fusée H-IIA en orbite',
        ALOS: 'Maquette au 1/50 d’ALOS-4 par la JAXA, avec l’antenne radar PALSAR-3 et les panneaux solaires, au centre spatial de Tsukuba',
    },
    'es': {
        KILI: 'El monte Kilimanjaro y las tierras altas de alrededor en Tanzania, vistos desde el transbordador espacial',
        GEDI: 'El láser GEDI de cartografía forestal, montado fuera del módulo Kibo en la Estación Espacial Internacional',
        ASTRO: 'Ilustración de la nave ADRAS-J acercándose a una etapa superior usada de un cohete H-IIA en órbita',
        ALOS: 'Modelo a escala 1/50 de ALOS-4 de la JAXA, con la antena de radar PALSAR-3 y los paneles solares, en el Centro Espacial de Tsukuba',
    },
    'ar': {
        KILI: 'جبل كليمنجارو والمرتفعات المحيطة به في تنزانيا، كما يُرى من مكوك الفضاء',
        GEDI: 'ليزر GEDI لرسم خرائط الغابات، المثبَّت خارج وحدة كيبو على محطة الفضاء الدولية',
        ASTRO: 'رسم توضيحي لمركبة ADRAS-J وهي تقترب من مرحلة عليا مستهلكة لصاروخ H-IIA في المدار',
        ALOS: 'نموذج بمقياس 1/50 للقمر ALOS-4 من JAXA، بهوائي الرادار PALSAR-3 وألواح الطاقة الشمسية، في مركز تسوكوبا الفضائي',
    },
    'it': {
        KILI: 'Il monte Kilimangiaro e gli altopiani circostanti in Tanzania, visti dallo Space Shuttle',
        GEDI: 'Il laser GEDI per la mappatura delle foreste, montato fuori dal modulo Kibo sulla Stazione Spaziale Internazionale',
        ASTRO: 'Illustrazione della sonda ADRAS-J che si avvicina a uno stadio superiore esausto di un razzo H-IIA in orbita',
        ALOS: 'Modello in scala 1/50 di ALOS-4 della JAXA, con l’antenna radar PALSAR-3 e i pannelli solari, al centro spaziale di Tsukuba',
    },
    'he': {
        KILI: 'הר קילימנג׳רו והרמות שסביבו בטנזניה, כפי שנראו ממעבורת החלל',
        GEDI: 'לייזר GEDI למיפוי יערות, המותקן מחוץ למודול קיבו בתחנת החלל הבינלאומית',
        ASTRO: 'איור של החללית ADRAS-J מתקרבת לשלב עליון משומש של רקטת H-IIA במסלול',
        ALOS: 'דגם בקנה מידה 1/50 של ALOS-4 של JAXA, עם אנטנת המכ״ם PALSAR-3 ומערכי השמש, במרכז החלל צוקובה',
    },
}
# Kenya, Tana and the seedling already have translation-memory entries.
mem = {}
for lang in ('fr', 'es', 'ar', 'it', 'he'):
    path = f'i18n/{lang}.json'
    m = json.load(open(path, encoding='utf8'))
    mem[lang] = m
    added = False
    for k, v in {**TM[lang], KENYA: m.get(KENYA, KENYA), TANA: m.get(TANA, TANA), SEED: m.get(SEED, SEED)}.items():
        if k not in m:
            m[k] = v
            added = True
    if added:
        raw = open(path, encoding='utf8').read().rstrip()
        if not raw.endswith('}'):
            raise SystemExit('bad json ' + path)
        body = raw[:-1].rstrip()
        if not body.endswith(','):
            body += ','
        extra = []
        for k, v in TM[lang].items():
            if k not in json.loads(raw):
                extra.append(json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False))
        open(path, 'w', encoding='utf8').write(body + '\n' + ',\n'.join(extra) + '\n}\n')
        mem[lang] = json.load(open(path, encoding='utf8'))

def tr(lang, en):
    if lang == 'en':
        return en
    return mem[lang].get(en, en)

def esc(v):
    return html.escape(v, quote=True)

def set_attr(tag, name, value):
    e = esc(value)
    if re.search(rf'\b{name}="[^"]*"', tag):
        return re.sub(rf'\b{name}="[^"]*"', f'{name}="{e}"', tag, count=1)
    if re.search(rf"\b{name}='[^']*'", tag):
        return re.sub(rf"\b{name}='[^']*'", f'{name}="{e}"', tag, count=1)
    return tag[:-1] + f' {name}="{e}">' if tag.endswith('>') else tag

def set_img(tag, src, alt, w, h):
    tag = re.sub(r'\bsrc="[^"]*"', f'src="{src}"', tag, count=1)
    tag = set_attr(tag, 'alt', alt)
    if re.search(r'\bwidth="\d+"', tag):
        tag = re.sub(r'\bwidth="\d+"', f'width="{w}"', tag, count=1)
    if re.search(r'\bheight="\d+"', tag):
        tag = re.sub(r'\bheight="\d+"', f'height="{h}"', tag, count=1)
    return tag

# page -> (filename, alt english, width, height) for the further-info image and any fact that still shows the wrong photo
BOTTOM = {
    'GEDI.html': ('GEDI_on_ISS.jpg', GEDI, 1280, 853),
    'Eden_People_Planet.html': ('Kilimanjaro_STS72.jpg', KILI, 1200, 1200),
    'Justdiggit.html': ('hub/ESA_S2_Southeast_Kenya.jpg', KENYA, 1602, 1920),
    'Trees_for_the_Future.html': ('hub/ESA_S2_Tana_River_Kenya.jpg', TANA, 1920, 1920),
    'WeForest.html': ('hub/USFS_Seedling_Planting_Custer_Gallatin.jpg', SEED, 1280, 1920),
    'Astroscale.html': ('Astroscale_ADRAS-J_H-IIA_Stage.jpg', ASTRO, 1200, 675),
    'ALOS-4.html': ('ALOS-4_Model_Tsukuba.jpg', ALOS, 1280, 964),
}
REL = {
    'Justdiggit.html': ('hub/ESA_S2_Southeast_Kenya.jpg', 1602, 1920),
    'Trees_for_the_Future.html': ('hub/ESA_S2_Tana_River_Kenya.jpg', 1920, 1920),
    'WeForest.html': ('hub/USFS_Seedling_Planting_Custer_Gallatin.jpg', 1280, 1920),
}

CRIT_BG = {
    'Justdiggit.html': 'hub/ESA_S2_Southeast_Kenya.jpg',
    'Trees_for_the_Future.html': 'hub/ESA_S2_Tana_River_Kenya.jpg',
    'WeForest.html': 'hub/USFS_Seedling_Planting_Custer_Gallatin.jpg',
}

def fix(s, page, lang):
    pre = '' if lang == 'en' else '../'
    if page in CRIT_BG:
        dest = 'assets/' + CRIT_BG[page]
        s = s.replace('assets/Kilimanjaro_STS72.jpg', dest)
    if page == 'GEDI.html':
        # Inlined critical CSS still painted the whole-station flyaround behind the instrument photo.
        s = s.replace('assets/ISS_Flyaround_2021.jpg', 'assets/GEDI_on_ISS.jpg')
    if page in BOTTOM:
        fn, alt, w, h = BOTTOM[page]
        src = pre + 'assets/' + fn
        def bottom(m):
            return re.sub(r'<img\b[^>]*>', lambda im: set_img(im.group(0), src, tr(lang, alt), w, h), m.group(0), count=1)
        s2, n = re.subn(r'<section class="donate-banner bottom-link".*?</section>', bottom, s, count=1, flags=re.S)
        if n:
            s = s2
        # The banner pass writes the English alt. Show it in the page language.
        def hero(m, alt=tr(lang, alt)):
            img = re.search(r'<img\b[^>]*>', m.group(0))
            return m.group(1) + set_attr(img.group(0), 'alt', alt)
        s = re.sub(r'(class="spb-media">(?:<source\b[^>]*>)*)<img\b[^>]*>', hero, s, count=1)
        # Amazing-fact popup: same subject as the page, not a shared mountain or the whole station.
        if page in ('GEDI.html', 'Justdiggit.html', 'WeForest.html', 'Eden_People_Planet.html'):
            def fact(m):
                tag = m.group(0)
                if 'data-image=' not in tag:
                    return tag
                tag = re.sub(r'\bdata-image="(?:\.\./)?assets/[^"]+"', f'data-image="{src}"', tag, count=1)
                return set_attr(tag, 'data-image-alt', tr(lang, alt))
            s = re.sub(r'<p class="amazing-fact[^"]*"[^>]*>', fact, s)
    for href, (fn, w, h) in REL.items():
        src = pre + 'assets/' + fn
        def one(m, src=src, w=w, h=h):
            block = m.group(0)
            if 'Kilimanjaro_STS72' not in block:
                return block
            def img(im):
                tag = re.sub(r'\bsrc="(?:\.\./)?assets/Kilimanjaro_STS72\.jpg"', f'src="{src}"', im.group(0), count=1)
                if re.search(r'\bwidth="\d+"', tag):
                    tag = re.sub(r'\bwidth="\d+"', f'width="{w}"', tag, count=1)
                if re.search(r'\bheight="\d+"', tag):
                    tag = re.sub(r'\bheight="\d+"', f'height="{h}"', tag, count=1)
                return tag
            return re.sub(r'<img\b[^>]*>', img, block, count=1)
        s = re.sub(r'<a href="' + re.escape(href) + r'">.*?</a>', one, s, flags=re.S)
    return s

n = 0
for f in sorted(glob.glob('*.html') + glob.glob('[a-z][a-z]/*.html')):
    if os.path.basename(f).startswith('google'):
        continue
    lang = f.split('/')[0] if '/' in f else 'en'
    if lang not in ('en', 'fr', 'es', 'ar', 'it', 'he'):
        lang = 'en'
    page = os.path.basename(f)
    s = open(f, encoding='utf8').read()
    s2 = fix(s, page, lang)
    if s2 != s:
        open(f, 'w', encoding='utf8').write(s2)
        n += 1
print('fix-photo-subjects', n, 'html files')
