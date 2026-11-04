#!/usr/bin/env python3
"""Kids World Map (K-5): tap a region, see Saving Planets solutions already pinned there.

Regions are the same buckets as scripts/build-sol-directory.py (map pins, launch sites excluded,
orbit and worldwide strips). Kid text is each page's Explain Like I'm 10 list. Photos and credits
come from the Solutions card. Nothing here is a new fact.

Writes Kids_World.html, assets/data/kids-world.<lang>.json, i18n strings, and a KIDSWORLD link
on Play_and_Learn.html and Teachers.html (all built languages). Does not add Google Analytics.
Idempotent. Run late in weekly-sync.sh (after build-nav, build-kids-p1, build-pwa)."""
import html, json, os, re, importlib.util
from bs4 import BeautifulSoup

PAGE = 'Kids_World.html'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
ASSETV = '20261102a'
GA = re.compile(r"\n?<!-- Google tag \(gtag\.js\) -->.*?<!-- /Google tag -->", re.S)
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    if os.path.exists(p) and rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)

spec = importlib.util.spec_from_file_location('sd', 'scripts/build-sol-directory.py')
sd = importlib.util.module_from_spec(spec); spec.loader.exec_module(sd)

# English UI string -> translations. Merged into i18n/<lang>.json (the site pipeline).
T = {
 'Kids World Map': ('Carte du monde pour les enfants', 'Mapa del mundo para niños', 'خريطة العالم للأطفال', 'Mappa del mondo per bambini', 'מפת העולם לילדים'),
 "A map for kindergarten through grade 5: tap a region to see Saving Planets solutions there, in the same simple words as each page's Explain Like I'm 10 note, with the real photo and its credit.":
 ("Une carte de la maternelle au CM2 : touche une région pour voir les solutions de Saving Planets qui s’y trouvent, avec les mêmes mots simples que la note « Explique-moi comme si j'avais 10 ans », la vraie photo et son crédit.",
  "Un mapa de infantil a 5.º de primaria: toca una región para ver las soluciones de Saving Planets que hay allí, con las mismas palabras sencillas de la nota «Explícamelo como si tuviera 10 años», la foto real y su crédito.",
  "خريطة من الروضة حتى الصف الخامس: المس منطقة لترى حلول Saving Planets هناك، بالكلمات البسيطة نفسها من ملاحظة «اشرحها لي كأن عمري 10 سنوات»، مع الصورة الحقيقية واسم مصدرها.",
  "Una mappa dalla scuola dell'infanzia alla quinta elementare: tocca una regione per vedere le soluzioni di Saving Planets che si trovano lì, con le stesse parole semplici della nota «Spiegamelo come se avessi 10 anni», la foto vera e il suo credito.",
  "מפה מגן עד כיתה ה': הקישו על אזור כדי לראות את פתרונות Saving Planets שם, באותן מילים פשוטות כמו בהערה «הסבירו לי כאילו אני בן 10», עם התמונה האמיתית וקרדיט שלה."),
 "Tap a colored part of the map, or one of the buttons. You will see Saving Planets solutions tagged for kindergarten through grade 5, using the simple words already on each page, plus the real photo and its credit.":
 ("Touche une partie colorée de la carte, ou un des boutons. Tu verras les solutions Saving Planets marquées de la maternelle au CM2, avec les mots simples déjà sur chaque page, la vraie photo et son crédit.",
  "Toca una parte de color del mapa, o uno de los botones. Verás las soluciones de Saving Planets marcadas de infantil a 5.º, con las palabras sencillas que ya están en cada página, la foto real y su crédito.",
  "المس جزءًا ملونًا من الخريطة، أو أحد الأزرار. سترى حلول Saving Planets المخصصة من الروضة حتى الصف الخامس، بالكلمات البسيطة الموجودة أصلًا في كل صفحة، مع الصورة الحقيقية واسم مصدرها.",
  "Tocca una parte colorata della mappa, oppure uno dei pulsanti. Vedrai le soluzioni di Saving Planets indicate dalla scuola dell'infanzia alla quinta, con le parole semplici già presenti in ogni pagina, la foto vera e il suo credito.",
  "הקישו על חלק צבעוני במפה, או על אחד הכפתורים. תראו פתרונות של Saving Planets שמסומנים מגן עד כיתה ה', במילים הפשוטות שכבר נמצאות בכל דף, עם התמונה האמיתית והקרדיט שלה."),
 'A simple drawing of the regions used on our Solutions page. It is not a scale map.':
 ("Un dessin simple des régions utilisées sur notre page Solutions. Ce n'est pas une carte à l'échelle.",
  'Un dibujo sencillo de las regiones de nuestra página de Soluciones. No es un mapa a escala.',
  'رسم بسيط للمناطق المستخدمة في صفحة الحلول. ليست خريطة بمقياس رسم.',
  'Un disegno semplice delle regioni usate nella pagina Soluzioni. Non è una carta in scala.',
  'ציור פשוט של האזורים שבדף הפתרונות. זו אינה מפה בקנה מידה.'),
 'Choose a region': ('Choisis une région', 'Elige una región', 'اختر منطقة', 'Scegli una regione', 'בחרו אזור'),
 'The Americas': ('Les Amériques', 'Las Américas', 'الأمريكتان', 'Le Americhe', 'אמריקה'),
 'Europe and Africa': ("L'Europe et l'Afrique", 'Europa y África', 'أوروبا وأفريقيا', 'Europa e Africa', 'אירופה ואפריקה'),
 'Asia and Oceania': ("L'Asie et l'Océanie", 'Asia y Oceanía', 'آسيا وأوقيانوسيا', 'Asia e Oceania', 'אסיה ואוקיאניה'),
 'From space': ("Depuis l'espace", 'Desde el espacio', 'من الفضاء', 'Dallo spazio', 'מהחלל'),
 'All over the world': ('Partout dans le monde', 'En todo el mundo', 'في كل أنحاء العالم', 'In tutto il mondo', 'בכל העולם'),
 'Map of regions you can tap': ('Carte des régions que tu peux toucher', 'Mapa de regiones que puedes tocar', 'خريطة مناطق يمكن لمسها', 'Mappa delle regioni che puoi toccare', 'מפת אזורים שאפשר להקיש עליהם'),
 'This map needs JavaScript. You can still browse solutions by region on the Solutions page.':
 ('Cette carte a besoin de JavaScript. Tu peux quand même parcourir les solutions par région sur la page Solutions.',
  'Este mapa necesita JavaScript. Aun así puedes explorar las soluciones por región en la página de Soluciones.',
  'تحتاج هذه الخريطة إلى جافاسكربت. ما زال بإمكانك تصفح الحلول حسب المنطقة في صفحة الحلول.',
  'Questa mappa ha bisogno di JavaScript. Puoi comunque sfogliare le soluzioni per regione nella pagina Soluzioni.',
  'המפה הזו צריכה JavaScript. עדיין אפשר לעיין בפתרונות לפי אזור בדף הפתרונות.'),
 'Sorry, the map could not load. Please refresh the page.':
 ("Désolé, la carte n'a pas pu se charger. Actualise la page.",
  'Lo sentimos, el mapa no se pudo cargar. Actualiza la página.',
  'عذرًا، تعذّر تحميل الخريطة. يرجى تحديث الصفحة.',
  'Spiacenti, la mappa non si è caricata. Aggiorna la pagina.',
  'מצטערים, המפה לא נטענה. רעננו את הדף.'),
 'For grown-ups': ('Pour les adultes', 'Para los adultos', 'للكبار', 'Per gli adulti', 'למבוגרים'),
 "Every simple note on this map is copied from that solution's Explain Like I'm 10 section.":
 ("Chaque note simple de cette carte est copiée depuis la partie « Explique-moi comme si j'avais 10 ans » de cette solution.",
  'Cada nota sencilla de este mapa está copiada de la sección «Explícamelo como si tuviera 10 años» de esa solución.',
  'كل ملاحظة بسيطة في هذه الخريطة منسوخة من قسم «اشرحها لي كأن عمري 10 سنوات» في صفحة ذلك الحل.',
  'Ogni nota semplice di questa mappa è copiata dalla sezione «Spiegamelo come se avessi 10 anni» di quella soluzione.',
  'כל הערה פשוטה במפה הזו מועתקת מהקטע «הסבירו לי כאילו אני בן 10» בדף של אותו פתרון.'),
 'Photos use the credit already printed on the Solutions card.':
 ('Les photos gardent le crédit déjà imprimé sur la fiche Solutions.',
  'Las fotos usan el crédito que ya está impreso en la ficha de Soluciones.',
  'الصور تستخدم اسم المصدر المطبوع أصلًا على بطاقة الحلول.',
  'Le foto usano il credito già stampato sulla scheda Soluzioni.',
  'התמונות משתמשות בקרדיט שכבר מודפס בכרטיס הפתרונות.'),
 'Place names are the pins on the':
 ('Les noms de lieux sont les épingles de la',
  'Los nombres de lugares son los pines del',
  'أسماء الأماكن هي دبابيس',
  'I nomi dei luoghi sono gli spilli della',
  'שמות המקומות הם הסיכות של'),
}
REGIONS = ['americas', 'eurafrica', 'asiaoceania', 'orbit', 'world']
LABEL = {'americas': 'The Americas', 'eurafrica': 'Europe and Africa', 'asiaoceania': 'Asia and Oceania', 'orbit': 'From space', 'world': 'All over the world'}
# JSON-only strings (already in the language when the file is written).
UI = {
 'en': dict(more='Show more solutions', less='Show fewer solutions', places='Places named on our map:', source='Source:', read='Read the whole page', eli="Explain Like I'm 10", count='{n} solutions for kindergarten through grade 5', empty='No kindergarten-to-grade-5 solution on Saving Planets is pinned to this region yet.', summary='From the solution card:'),
 'fr': dict(more='Montrer plus de solutions', less='Montrer moins de solutions', places='Lieux indiqués sur notre carte :', source='Source :', read='Lire toute la page', eli="Explique-moi comme si j'avais 10 ans", count='{n} solutions de la maternelle au CM2', empty="Aucune solution de la maternelle au CM2 sur Saving Planets n'est épinglée dans cette région pour le moment.", summary='Depuis la fiche solution :'),
 'es': dict(more='Mostrar más soluciones', less='Mostrar menos soluciones', places='Lugares marcados en nuestro mapa:', source='Fuente:', read='Leer la página completa', eli='Explícamelo como si tuviera 10 años', count='{n} soluciones de infantil a 5.º', empty='Todavía no hay ninguna solución de infantil a 5.º de Saving Planets marcada en esta región.', summary='De la ficha de la solución:'),
 'ar': dict(more='أظهر المزيد من الحلول', less='أظهر حلولًا أقل', places='أماكن مذكورة على خريطتنا:', source='المصدر:', read='اقرأ الصفحة كلها', eli='اشرحها لي كأن عمري 10 سنوات', count='{n} حلًا من الروضة حتى الصف الخامس', empty='لا يوجد بعد حل من الروضة حتى الصف الخامس على Saving Planets مثبت في هذه المنطقة.', summary='من بطاقة الحل:'),
 'it': dict(more='Mostra altre soluzioni', less='Mostra meno soluzioni', places='Luoghi indicati sulla nostra mappa:', source='Fonte:', read='Leggi tutta la pagina', eli='Spiegamelo come se avessi 10 anni', count="{n} soluzioni dalla scuola dell'infanzia alla quinta", empty='Nessuna soluzione di Saving Planets, dalla scuola dell\'infanzia alla quinta, è ancora fissata in questa regione.', summary='Dalla scheda della soluzione:'),
 'he': dict(more='הציגו עוד פתרונות', less='הציגו פחות פתרונות', places='מקומות שמסומנים במפה שלנו:', source='מקור:', read='קראו את כל הדף', eli='הסבירו לי כאילו אני בן 10', count='{n} פתרונות מגן עד כיתה ה\'', empty='עדיין אין פתרון של Saving Planets מגן עד כיתה ה\' שמסומן באזור הזה.', summary='מכרטיס הפתרון:'),
}
LINK = {
 'en': ('Kids World Map', 'Tap a region to see solutions there, told simply, with real photos.', 'Kids World Map: tap a region to see kindergarten-to-grade-5 solutions in simple words, with photos and credits.'),
 'fr': ('Carte du monde pour les enfants', 'Touche une région pour voir les solutions, en mots simples, avec de vraies photos.', 'Carte du monde pour les enfants : touche une région pour voir les solutions de la maternelle au CM2, en mots simples, avec photos et crédits.'),
 'es': ('Mapa del mundo para niños', 'Toca una región para ver las soluciones, con palabras sencillas y fotos reales.', 'Mapa del mundo para niños: toca una región para ver soluciones de infantil a 5.º, con palabras sencillas, fotos y créditos.'),
 'ar': ('خريطة العالم للأطفال', 'المس منطقة لترى الحلول هناك، بكلمات بسيطة وصور حقيقية.', 'خريطة العالم للأطفال: المس منطقة لترى حلول الروضة حتى الصف الخامس بكلمات بسيطة، مع الصور وأسماء المصادر.'),
 'it': ('Mappa del mondo per bambini', 'Tocca una regione per vedere le soluzioni, con parole semplici e foto vere.', 'Mappa del mondo per bambini: tocca una regione per vedere le soluzioni dalla scuola dell\'infanzia alla quinta, con parole semplici, foto e crediti.'),
 'he': ('מפת העולם לילדים', 'הקישו על אזור כדי לראות את הפתרונות שם, במילים פשוטות ועם תמונות אמיתיות.', 'מפת העולם לילדים: הקישו על אזור כדי לראות פתרונות מגן עד כיתה ה\' במילים פשוטות, עם תמונות וקרדיטים.'),
}

SVG = '''<svg viewBox="0 0 800 460" role="group" aria-label="Map of regions you can tap">
<rect width="800" height="460" fill="#1565c0"/>
<ellipse cx="400" cy="28" rx="360" ry="26" fill="#e3f2fd" opacity=".85"/>
<path data-region="americas" role="button" tabindex="0" aria-pressed="false" aria-label="The Americas" fill="#2e7d32" d="M118 78c28-32 92-38 128-8 24 20 28 58 10 86-8 14-28 22-36 38-6 12 4 22 2 36-4 28-30 48-58 42-22-4-36-24-34-46 2-16-18-24-22-42-6-26 4-48 10-66 8-22-8-28 0-40zM168 214c22 8 36 36 30 68 6 40-8 78-30 108-16 22-36 18-40-6-4-28 8-52 6-84-2-24-14-40-8-62 6-16 24-28 42-24z"/>
<path data-region="eurafrica" role="button" tabindex="0" aria-pressed="false" aria-label="Europe and Africa" fill="#0d47a1" d="M360 86c28-18 78-16 96 12 14 22 8 42-12 54-22 14-58 12-74-6-16-18-22-42-10-60zM372 162c42-16 96 4 108 48 14 52 4 112-28 156-22 30-58 28-70 2-16-36-8-86 4-124 8-28-2-62-14-82z"/>
<path data-region="asiaoceania" role="button" tabindex="0" aria-pressed="false" aria-label="Asia and Oceania" fill="#ef6c00" d="M470 78c62-28 168-10 214 42 36 40 28 86-18 112-40 22-96 18-140-4-28-14-36-36-28-58 6-16-10-28-8-46 4-22-8-36-20-46zM628 268c42-16 96 4 102 40 6 36-24 64-70 62-36-2-62-28-58-54 4-22 8-40 26-48z"/>
<path d="M40 414c120-28 600-28 720 0 0 28-720 28-720 0z" fill="#e3f2fd"/>
</svg>'''

def norm_src(src):
    src = (src or '').strip()
    while src.startswith('../'): src = src[3:]
    return src

def sanitize(el):
    if el is None: return ''
    parts = []
    for child in el.children:
        if isinstance(child, str):
            parts.append(esc(child))
        elif child.name == 'a':
            href = child.get('href') or ''
            if href.startswith('https://') or href.startswith('http://'):
                parts.append(f'<a href="{esc(href)}" rel="noopener" target="_blank">{esc(child.get_text())}</a>')
            else:
                parts.append(esc(child.get_text()))
        elif child.name in ('bdi', 'span', 'p'):
            parts.append(sanitize(child))
        else:
            parts.append(esc(child.get_text()))
    return re.sub(r'\s+', ' ', ''.join(parts)).strip()

def eli_source(lang, page):
    path = page if lang == 'en' else f'{lang}/{page}'
    if not os.path.exists(path): path = page
    if not os.path.exists(path): return [], None
    soup = BeautifulSoup(rd(path), 'html.parser')
    bullets = []
    sec = soup.select_one('#eli10')
    if sec:
        for li in sec.select('li')[:3]:
            for pop in li.select('.gl-pop'): pop.decompose()
            for b in li.select('button'): b.replace_with(b.get_text())
            t = re.sub(r'\s+', ' ', li.get_text(' ', strip=True))
            if t: bullets.append(t)
    a = soup.select_one('p.fact-source a[href]')
    src = None
    if a and (a['href'].startswith('http://') or a['href'].startswith('https://')):
        src = {'href': a['href'], 'name': re.sub(r'\s+', ' ', a.get_text(' ', strip=True))}
    return bullets, src

def cards_for(lang):
    path = 'Solutions.html' if lang == 'en' else f'{lang}/Solutions.html'
    if not os.path.exists(path): path = 'Solutions.html'
    soup = BeautifulSoup(rd(path), 'html.parser')
    out = {}
    for art in soup.select('article.sol-card'):
        u = (art.get('data-url') or '').split('/')[-1]
        img = art.select_one('img')
        if not u or not img: continue
        try: w, h = int(img.get('width') or 0), int(img.get('height') or 0)
        except ValueError: w = h = 0
        out[u] = {'img': norm_src(img.get('src')), 'alt': img.get('alt') or '', 'w': w, 'h': h, 'credit': sanitize(art.select_one('.photo-credit'))}
    return out

def collect(lang):
    mp = json.load(open(f'assets/data/map.{lang}.json', encoding='utf8'))
    by = {s['u']: s for s in mp['sols']}
    photos = cards_for(lang)
    regions = {k: [] for k in REGIONS}
    for u, e in sd.LOC.items():
        if u not in by or not os.path.exists(u): continue
        st, rg, g = sd.attrs(u)
        bands = set(g.split())
        if 'K-2' not in bands and '3-5' not in bands: continue
        eli, src = eli_source(lang, u)
        photo = photos.get(u, {})
        base = {'u': u, 'n': by[u].get('n') or u, 'sum': by[u].get('s') or '', 'eli': eli, 'src': src,
                'img': photo.get('img') or '', 'alt': photo.get('alt') or '', 'w': photo.get('w') or 0, 'h': photo.get('h') or 0,
                'credit': photo.get('credit') or ''}
        pins = [p for p in by[u].get('p') or [] if p.get('basis') != 'launch']
        for key in rg.split():
            if key not in regions: continue
            item = dict(base)
            if key in ('orbit', 'world'):
                item['places'] = []
            else:
                labs = []
                for p in pins:
                    if sd.region(p['lat'], p['lng']) == key and p.get('label') and p['label'] not in labs:
                        labs.append(p['label'])
                item['places'] = labs[:3]
            regions[key].append(item)
    for key in regions:
        regions[key].sort(key=lambda x: x['n'].casefold())
    return {'ui': UI[lang], 'regions': regions}

MAIN = f'''<section class="page-hero hero-kids"><div class="page-hero-content"><h1>Kids World Map</h1><p>{esc("A map for kindergarten through grade 5: tap a region to see Saving Planets solutions there, in the same simple words as each page's Explain Like I'm 10 note, with the real photo and its credit.")}</p></div></section>
<div class="kw-wrap" id="kw">
<p class="kw-lead">{esc("Tap a colored part of the map, or one of the buttons. You will see Saving Planets solutions tagged for kindergarten through grade 5, using the simple words already on each page, plus the real photo and its credit.")}</p>
<p class="kw-note">{esc("A simple drawing of the regions used on our Solutions page. It is not a scale map.")}</p>
<div class="kw-stage">{SVG}
<button type="button" class="kw-space" data-region="orbit" aria-pressed="false">From space</button></div>
<div class="kw-pins" role="group" aria-label="Choose a region">
<button type="button" class="kw-pin" data-region="americas" aria-pressed="false">The Americas</button>
<button type="button" class="kw-pin" data-region="eurafrica" aria-pressed="false">Europe and Africa</button>
<button type="button" class="kw-pin" data-region="asiaoceania" aria-pressed="false">Asia and Oceania</button>
<button type="button" class="kw-pin" data-region="orbit" aria-pressed="false">From space</button>
<button type="button" class="kw-pin" data-region="world" aria-pressed="false">All over the world</button>
</div>
<section class="kw-panel" id="kw-panel" aria-live="polite" hidden></section>
<template class="kw-error-tpl"><p class="kw-error" role="alert">Sorry, the map could not load. Please refresh the page.</p></template>
<noscript><p>This map needs JavaScript. You can still browse solutions by region on the Solutions page.</p><ul>
<li><a href="Solutions.html?region=americas">The Americas</a></li>
<li><a href="Solutions.html?region=eurafrica">Europe and Africa</a></li>
<li><a href="Solutions.html?region=asiaoceania">Asia and Oceania</a></li>
<li><a href="Solutions.html?region=orbit">From space</a></li>
<li><a href="Solutions.html?region=world">All over the world</a></li>
</ul></noscript>
<h2>For grown-ups</h2>
<p>Every simple note on this map is copied from that solution's Explain Like I'm 10 section.</p>
<p>Photos use the credit already printed on the Solutions card.</p>
<p>Place names are the pins on the <a href="World_Map.html">World Solutions Map</a>.</p>
</div>
'''

def shell():
    s = rd('Kids_Map.html')
    s = re.sub(r'<main id="main">.*?</main>', '<main id="main">\n' + MAIN + '\n</main>', s, count=1, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>Kids World Map | Saving Planets</title>', s, count=1, flags=re.S)
    desc = esc("A map for kindergarten through grade 5: tap a region to see Saving Planets solutions there, in the same simple words as each page's Explain Like I'm 10 note, with the real photo and its credit.")
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {attr} content=")[^"]*"', lambda m, a=attr: m.group(1) + desc + '"', s, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {attr} content=")[^"]*"', r'\1Kids World Map | Saving Planets"', s, count=1)
    s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', r'\1Kids World Map"', s, count=1)
    for lang, folder in (('en', ''), ('fr', 'fr/'), ('es', 'es/'), ('ar', 'ar/'), ('it', 'it/'), ('he', 'he/')):
        s = s.replace(f'https://www.savingplanets.com/{folder}Kids_Map.html', f'https://www.savingplanets.com/{folder}{PAGE}')
        if folder:
            s = s.replace(f'href="{folder}Kids_Map.html"', f'href="{folder}{PAGE}"')
    s = s.replace('href="Kids_Map.html" hreflang="en"', f'href="{PAGE}" hreflang="en"')
    s = s.replace('assets/og/en/Kids_Map.jpg', 'assets/og/en/World_Map.jpg')
    s = s.replace('kids-map-page', 'kids-world-page')
    s = re.sub(r'<script src="edu\.js[^"]*" defer></script>\s*', '', s)
    s = re.sub(r'<script src="edu-extras\.js[^"]*" defer></script>\s*', '', s)
    s = GA.sub('', s)
    if 'kids-world.css' not in s:
        s = s.replace('</head>', f'<link rel="stylesheet" href="kids-world.css?v={ASSETV}">\n</head>', 1)
    if 'kids-world.js' not in s:
        s = s.replace('</body>', f'<script src="kids-world.js?v={ASSETV}" defer></script>\n</body>', 1)
    if 'gtag' in s or 'googletagmanager' in s:
        raise SystemExit('kids world: refused to keep a Google Analytics tag')
    return s

def merge_i18n():
    order = ['fr', 'es', 'ar', 'it', 'he']
    for i, lang in enumerate(order):
        p = f'i18n/{lang}.json'
        m = json.load(open(p, encoding='utf8')); n0 = json.dumps(m, ensure_ascii=False)
        for k, vals in T.items():
            if i < len(vals): m[k] = vals[i]
        if json.dumps(m, ensure_ascii=False) != n0:
            json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
            open(p, 'a', encoding='utf8').write('\n')

def ensure_lists():
    pl = rd('i18n/pages.txt')
    if PAGE not in pl.split():
        open('i18n/pages.txt', 'w', encoding='utf8').write(pl.rstrip('\n') + '\n' + PAGE + '\n')
    hp = 'i18n/he-pages.txt'
    h = rd(hp)
    if PAGE not in [ln.strip() for ln in h.splitlines()]:
        open(hp, 'w', encoding='utf8').write(h.rstrip('\n') + '\n' + PAGE + '\n')

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
        name, blurb, teach = LINK[lang]
        rest = teach.split(': ', 1)[1] if ': ' in teach else teach
        css = ('../' if lang != 'en' else '') + f'kids-world.css?v={ASSETV}'
        play = pre + 'Play_and_Learn.html'
        teachers = pre + 'Teachers.html'
        if os.path.exists(play):
            block = ('<!-- KIDSWORLD:START --><link rel="stylesheet" href="' + css + '">'
                     '<p class="kw-jump"><a class="pl-tile" href="Kids_World.html">'
                     f'<span class="pl-emoji" aria-hidden="true">🌍</span><span class="pl-name">{esc(name)}</span>'
                     f'<span class="pl-text">{esc(blurb)}</span></a></p><!-- KIDSWORLD:END -->')
            s = re.sub(r'<!-- KIDSWORLD:START -->.*?<!-- KIDSWORLD:END -->', '', rd(play), flags=re.S)
            s = re.sub(r'\n?<link rel="stylesheet" href="(?:\.\./)?kids-world\.css\?v=[^"]+">', '', s)
            anchor = '<!-- KIDSP1:START -->' if '<!-- KIDSP1:START -->' in s else '</main>'
            s = s.replace(anchor, block + anchor, 1)
            n += wr(play, s)
        if os.path.exists(teachers):
            block = ('<!-- KIDSWORLD:START --><link rel="stylesheet" href="' + css + '">'
                     f'<p class="kw-teach"><a href="Kids_World.html">{esc(name)}</a>: {esc(rest)}</p><!-- KIDSWORLD:END -->')
            s = re.sub(r'<!-- KIDSWORLD:START -->.*?<!-- KIDSWORLD:END -->', '', rd(teachers), flags=re.S)
            s = re.sub(r'\n?<link rel="stylesheet" href="(?:\.\./)?kids-world\.css\?v=[^"]+">', '', s)
            anchor = '<!-- EDU-LINKS:END -->' if '<!-- EDU-LINKS:END -->' in s else '</main>'
            s = s.replace(anchor, anchor + block, 1)
            n += wr(teachers, s)
    return n

def sitemap():
    import sitemap_pages
    if sitemap_pages.english_has(PAGE): return
    import subprocess
    subprocess.check_call(['python3', 'scripts/i18n-sitemap.py'])

def main():
    merge_i18n(); ensure_lists()
    os.makedirs('assets/data', exist_ok=True)
    counts = {}
    for lang in LANGS:
        data = collect(lang)
        counts[lang] = {k: len(v) for k, v in data['regions'].items()}
        json.dump(data, open(f'assets/data/kids-world.{lang}.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
        open(f'assets/data/kids-world.{lang}.json', 'a', encoding='utf8').write('\n')
    wr(PAGE, shell())
    translate()
    k = links()
    sitemap()
    print('kids-world:', counts['en'], 'link writes', k)

if __name__ == '__main__':
    main()
