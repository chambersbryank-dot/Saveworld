#!/usr/bin/env python3
"""Oct 15: interactive World Map (World_Map.html in en + every language folder that exists, e.g. fr/es/ar/it).
Solution pins come from assets/data/map-locations.json (one entry per solution: status active|upcoming, real pins, strip).
Names, hubs and links come from each language's Solutions.html; one-line summaries from each solution page's meta description.
Rocket pins: Launch Library 2 (The Space Devs, the same feed as the Live Launch Tracker), grouped by launch site, with
Russia, China and North Korea excluded (sites and launches). Writes assets/data/map.<lang>.json + assets/data/map-launches.json.
Idempotent. Run after i18n-build/post-processors and before build-ux.py (weekly-sync.sh). --no-fetch skips the launch refresh."""
import re, os, json, html, sys, glob, datetime, urllib.request
SITE = 'https://www.savingplanets.com/'
ASSETV = '20261112sv'  # Nov 12: more legend hubs, title video, satellite view link
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(html.unescape(s), quote=True)
txt = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
LANGS = ['en'] + [l for l in ['fr', 'es', 'ar', 'it'] if os.path.exists(f'{l}/Solutions.html') and os.path.exists(f'{l}/Kids_Map.html')]
d = lambda l: '' if l == 'en' else l + '/'

U = {
 'en': dict(title="Solutions Around the World and in Space Enhancing Our Planet's Health Every Day", desc="Solutions Around the World and in Space Enhancing Our Planet's Health Every Day",
   lead='Tap a pin to see a solution, where it works and a link to its page. Green pins are active now, blue pins are coming soon, and rocket pins list the next launches from that site.',
   active='Active now', upcoming='Coming soon', rocket='Launch site', hub='Hub', allhubs='All hubs', launches='Launches', show='Show',
   orbit='From Orbit', orbitintro='These solutions work in space, so they have no single place on Earth. Pins mark a launch site only when the solution page names it.',
   world='Worldwide', worldintro='These solutions happen all over the planet, with no single place to pin.',
   list='Map as a list', listintro='The same information as the map, for screen readers and keyboards.', read='Read more',
   next='Upcoming launches', none='No launches scheduled', tbd='date to be confirmed', src='Launch data: The Space Devs Launch Library 2 (same feed as our Live Launch Tracker). Launches by Russia, China and North Korea are not shown.',
   basis_hq='headquarters', basis_launch='launch site', pins='{t} solutions: {g} active · {b} coming soon · {r} launch sites', label='Interactive world map of solutions and launch sites',
   h1="Solutions Around the World and in Space Enhancing Our Planet's Health Every Day", spaceJump='Space, Earth-Protecting Satellites', key='Map key', csv='Download the map data (CSV)', listmore='Every solution as a list, including the ones in orbit and worldwide', live='Live Launch Tracker',
   allcat='All', rivers='Rivers', lakes='Lakes', oceans='Oceans', land='Land',
   polar='Polar', defense='Planetary Defense', observe='Earth Observation', weather='Space Weather', disposal='Space Disposal', rawane='Project Rawane', space='Space',
   byline='Created by the Founder and SI.', earthAlt='Photorealistic flat map of Earth, NASA Blue Marble Next Generation',
   zoomIn='Zoom in', zoomOut='Zoom out', zoomFit='Fit the planet', smallerMap='Smaller map', largerMap='Larger map', mapControls='Map size'),
 'fr': dict(title='Des solutions dans le monde et dans l’espace qui améliorent la santé de notre planète chaque jour', desc='Des solutions dans le monde et dans l’espace qui améliorent la santé de notre planète chaque jour',
   lead="Touchez une épingle pour voir une solution, où elle agit et un lien vers sa page. Vert : active ; bleu : bientôt ; fusée : prochains lancements depuis ce site.",
   active='Active', upcoming='Bientôt', rocket='Site de lancement', hub='Pôle', allhubs='Tous les pôles', launches='Lancements', show='Afficher',
   orbit="Depuis l'orbite", orbitintro="Ces solutions agissent dans l'espace et n'ont pas de lieu unique sur Terre. Une épingle marque le site de lancement seulement quand la page le nomme.",
   world='Partout dans le monde', worldintro="Ces solutions agissent sur toute la planète, sans lieu unique à épingler.",
   list='La carte sous forme de liste', listintro="Les mêmes informations que la carte, pour les lecteurs d'écran et le clavier.", read='En savoir plus',
   next='Prochains lancements', none='Aucun lancement prévu', tbd='date à confirmer', src="Données de lancement : The Space Devs Launch Library 2 (la même source que notre suivi des lancements). Les lancements de la Russie, de la Chine et de la Corée du Nord ne sont pas affichés.",
   basis_hq='siège', basis_launch='site de lancement', pins='{t} solutions : {g} actives · {b} bientôt · {r} sites de lancement', label='Carte mondiale interactive des solutions et des sites de lancement',
   h1='Des solutions dans le monde et dans l’espace qui améliorent la santé de notre planète chaque jour', spaceJump='Espace, Satellites qui protègent la Terre', key='Légende', csv='Télécharger les données de la carte (CSV)', listmore="Toutes les solutions sous forme de liste, y compris celles en orbite et partout dans le monde", live='Suivi des lancements en direct',
   allcat='Tout', rivers='Rivières', lakes='Lacs', oceans='Océans', land='Terres',
   polar='Pôles', defense='Défense planétaire', observe='Observation de la Terre', weather='Météo spatiale', disposal='Élimination spatiale', rawane='Projet Rawane', space='Espace',
   byline='Créé par le fondateur et SI.', earthAlt='Carte plate et photoréaliste de la Terre, NASA Blue Marble Next Generation',
   zoomIn='Agrandir', zoomOut='Réduire', zoomFit='Ajuster la planète', smallerMap='Carte plus petite', largerMap='Carte plus grande', mapControls='Taille de la carte'),
 'es': dict(title='Soluciones en todo el mundo y en el espacio que mejoran la salud de nuestro planeta cada día', desc='Soluciones en todo el mundo y en el espacio que mejoran la salud de nuestro planeta cada día',
   lead='Toca un pin para ver una solución, dónde actúa y un enlace a su página. Verde: activa; azul: próximamente; cohete: próximos lanzamientos desde ese sitio.',
   active='Activa', upcoming='Próximamente', rocket='Sitio de lanzamiento', hub='Centro', allhubs='Todos los centros', launches='Lanzamientos', show='Mostrar',
   orbit='Desde la órbita', orbitintro='Estas soluciones actúan en el espacio y no tienen un único lugar en la Tierra. Un pin marca el sitio de lanzamiento solo cuando la página lo nombra.',
   world='En todo el mundo', worldintro='Estas soluciones ocurren en todo el planeta, sin un único lugar que marcar.',
   list='El mapa como lista', listintro='La misma información que el mapa, para lectores de pantalla y teclado.', read='Leer más',
   next='Próximos lanzamientos', none='No hay lanzamientos programados', tbd='fecha por confirmar', src='Datos de lanzamientos: The Space Devs Launch Library 2 (la misma fuente que nuestro rastreador de lanzamientos). No se muestran lanzamientos de Rusia, China ni Corea del Norte.',
   basis_hq='sede', basis_launch='sitio de lanzamiento', pins='{t} soluciones: {g} activas · {b} próximamente · {r} sitios de lanzamiento', label='Mapa mundial interactivo de soluciones y sitios de lanzamiento',
   h1='Soluciones en todo el mundo y en el espacio que mejoran la salud de nuestro planeta cada día', spaceJump='Espacio, Satélites que protegen la Tierra', key='Leyenda', csv='Descargar los datos del mapa (CSV)', listmore='Todas las soluciones en una lista, incluidas las que están en órbita y en todo el mundo', live='Rastreador de lanzamientos en vivo',
   allcat='Todo', rivers='Ríos', lakes='Lagos', oceans='Océanos', land='Tierra',
   polar='Polos', defense='Defensa planetaria', observe='Observación de la Tierra', weather='Clima espacial', disposal='Eliminación espacial', rawane='Proyecto Rawane', space='Espacio',
   byline='Creado por el fundador y SI.', earthAlt='Mapa plano y fotorrealista de la Tierra, NASA Blue Marble Next Generation',
   zoomIn='Acercar', zoomOut='Alejar', zoomFit='Ajustar el planeta', smallerMap='Mapa más pequeño', largerMap='Mapa más grande', mapControls='Tamaño del mapa'),
 'ar': dict(title='حلول حول العالم وفي الفضاء تعزز صحة كوكبنا كل يوم', desc='حلول حول العالم وفي الفضاء تعزز صحة كوكبنا كل يوم',
   lead='اضغط على دبوس لترى الحل ومكان عمله ورابط صفحته. الأخضر: يعمل الآن، الأزرق: قريبًا، الصاروخ: الإطلاقات القادمة من ذلك الموقع.',
   active='يعمل الآن', upcoming='قريبًا', rocket='موقع إطلاق', hub='المركز', allhubs='كل المراكز', launches='الإطلاقات', show='عرض',
   orbit='من المدار', orbitintro='تعمل هذه الحلول في الفضاء، فليس لها مكان واحد على الأرض. يظهر دبوس موقع الإطلاق فقط عندما تذكره صفحة الحل.',
   world='حول العالم', worldintro='تحدث هذه الحلول في كل أنحاء الكوكب، دون مكان واحد لتحديده.',
   list='الخريطة على شكل قائمة', listintro='المعلومات نفسها الموجودة في الخريطة، لقارئات الشاشة ولوحة المفاتيح.', read='اقرأ المزيد',
   next='الإطلاقات القادمة', none='لا توجد إطلاقات مجدولة', tbd='الموعد لم يتأكد بعد', src='بيانات الإطلاق: The Space Devs Launch Library 2 (المصدر نفسه لمتتبع الإطلاقات لدينا). لا تُعرض إطلاقات روسيا والصين وكوريا الشمالية.',
   basis_hq='المقر', basis_launch='موقع الإطلاق', pins='{t} حلًا: {g} يعمل الآن · {b} قريبًا · {r} مواقع إطلاق', label='خريطة عالمية تفاعلية للحلول ومواقع الإطلاق',
   h1='حلول حول العالم وفي الفضاء تعزز صحة كوكبنا كل يوم', spaceJump='الفضاء، أقمار تحمي الأرض', key='مفتاح الخريطة', csv='تنزيل بيانات الخريطة (CSV)', listmore='كل الحلول على شكل قائمة، بما فيها الحلول في المدار وحول العالم', live='متتبع الإطلاقات المباشر',
   allcat='الكل', rivers='الأنهار', lakes='البحيرات', oceans='المحيطات', land='اليابسة',
   polar='القطبان', defense='الدفاع الكوكبي', observe='رصد الأرض', weather='طقس الفضاء', disposal='التخلص من الحطام الفضائي', rawane='مشروع Rawane', space='الفضاء',
   byline='من إعداد المؤسس وSI.', earthAlt='خريطة مسطحة واقعية للأرض، NASA Blue Marble Next Generation',
   zoomIn='تكبير', zoomOut='تصغير', zoomFit='ملاءمة الكوكب', smallerMap='خريطة أصغر', largerMap='خريطة أكبر', mapControls='حجم الخريطة'),
 'it': dict(title='Soluzioni in tutto il mondo e nello spazio che migliorano ogni giorno la salute del nostro pianeta', desc='Soluzioni in tutto il mondo e nello spazio che migliorano ogni giorno la salute del nostro pianeta',
   lead='Tocca uno spillo per vedere una soluzione, dove opera e il link alla sua pagina. Verde: attiva; blu: in arrivo; razzo: prossimi lanci da quel sito.',
   active='Attiva', upcoming='In arrivo', rocket='Sito di lancio', hub='Polo', allhubs='Tutti i poli', launches='Lanci', show='Mostra',
   orbit="Dall'orbita", orbitintro="Queste soluzioni operano nello spazio e non hanno un unico luogo sulla Terra. Uno spillo indica il sito di lancio solo quando la pagina lo nomina.",
   world='In tutto il mondo', worldintro='Queste soluzioni avvengono in tutto il pianeta, senza un unico luogo da segnare.',
   list='La mappa come elenco', listintro='Le stesse informazioni della mappa, per lettori di schermo e tastiera.', read='Scopri di più',
   next='Prossimi lanci', none='Nessun lancio in programma', tbd='data da confermare', src='Dati sui lanci: The Space Devs Launch Library 2 (la stessa fonte del nostro tracker dei lanci). I lanci di Russia, Cina e Corea del Nord non sono mostrati.',
   basis_hq='sede', basis_launch='sito di lancio', pins='{t} soluzioni: {g} attive · {b} in arrivo · {r} siti di lancio', label='Mappa mondiale interattiva di soluzioni e siti di lancio',
   h1='Soluzioni in tutto il mondo e nello spazio che migliorano ogni giorno la salute del nostro pianeta', spaceJump='Spazio, Satelliti che proteggono la Terra', key='Legenda', csv='Scarica i dati della mappa (CSV)', listmore="Tutte le soluzioni in un elenco, comprese quelle in orbita e in tutto il mondo", live='Tracker dei lanci in diretta',
   allcat='Tutte', rivers='Fiumi', lakes='Laghi', oceans='Oceani', land='Terre',
   polar='Poli', defense='Difesa planetaria', observe='Osservazione della Terra', weather='Meteo spaziale', disposal='Smaltimento dei detriti spaziali', rawane='Progetto Rawane', space='Spazio',
   byline='Creato dal fondatore e da SI.', earthAlt='Mappa piatta e fotorealistica della Terra, NASA Blue Marble Next Generation',
   zoomIn='Ingrandisci', zoomOut='Riduci', zoomFit='Adatta il pianeta', smallerMap='Mappa più piccola', largerMap='Mappa più grande', mapControls='Dimensione della mappa'),
}

# ---------- launches (Launch Library 2, same feed as the Live Launch Tracker) ----------
EXCL_COUNTRY = {'RUS', 'CHN', 'PRK'}
EXCL_RX = re.compile(r'roscosmos|russia|china|chinese|baikonur|plesetsk|vostochny|jiuquan|wenchang|xichang|taiyuan|haiyang|dongfeng|sohae|tonghae|korean committee|nada|korean people.s|landspace|galactic energy|i-space|orienspace|deep blue aero|space pioneer|cas space|expace|casc|casic|khrunichev|progress rocket', re.I)
SITES = [  # included active launch sites (fallback pins with 'No launches scheduled'); names as Launch Library 2 lists them
 ('Kennedy Space Center, FL, USA', 28.573, -80.649), ('Cape Canaveral SFS, FL, USA', 28.489, -80.578), ('Vandenberg SFB, CA, USA', 34.742, -120.572),
 ('SpaceX Starbase, TX, USA', 25.997, -97.157), ('Wallops Flight Facility, Virginia, USA', 37.833, -75.488), ('Pacific Spaceport Complex, Alaska', 57.435, -152.337),
 ('Guiana Space Centre, French Guiana', 5.239, -52.768), ('Rocket Lab Launch Complex 1, Mahia Peninsula, New Zealand', -39.261, 177.865),
 ('Tanegashima Space Center, Japan', 30.401, 130.975), ('Uchinoura Space Center, Japan', 31.251, 131.079), ('Satish Dhawan Space Centre, India', 13.72, 80.23),
 ('Andøya Spaceport', 69.108, 15.589), ('SaxaVord Spaceport', 60.818, -0.766), ('Esrange Space Center', 67.877, 21.06), ('Naro Space Center, South Korea', 34.432, 127.535)]
def excluded(r):
    p = r.get('pad') or {}; loc = (p.get('location') or {}).get('name', '')
    cc = ((p.get('country') or {}).get('alpha_3_code') or '')
    prov = (r.get('launch_service_provider') or {}).get('name', '')
    return cc in EXCL_COUNTRY or bool(EXCL_RX.search(loc + ' | ' + prov)) or 'Kazakhstan' in loc
def fetch_launches():
    url = 'https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=100&mode=normal'
    req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'savingplanets-map'})
    return json.load(urllib.request.urlopen(req, timeout=30))['results']
def group_launches(results):
    sites, dropped = {}, []
    for name, la, ln in SITES: sites[name] = dict(name=name, lat=la, lng=ln, pads={}, launches=[])
    for r in results:
        p = r.get('pad') or {}; loc = (p.get('location') or {}).get('name') or ''
        if excluded(r): dropped.append(loc); continue
        try: la, ln = float(p['latitude']), float(p['longitude'])
        except Exception: continue
        # Match only by Launch Library location name (never by proximity across different named sites)
        if loc in sites: key = loc
        else:
            key = next((k for k, v in sites.items() if abs(v['lat'] - la) < .08 and abs(v['lng'] - ln) < .08), None)
            if key is None: key = loc
        s = sites.setdefault(key, dict(name=key, lat=la, lng=ln, pads={}, launches=[]))
        nm = r.get('name', ''); mission = nm.split('|', 1)[1].strip() if '|' in nm else nm
        prec = ((r.get('net_precision') or {}).get('abbrev') or '')
        s['launches'].append(dict(net=r.get('net'), exact=prec in ('', 'SEC', 'MIN', 'HR', 'DAY', 'SEC1', 'MIN15'), prec=prec,
            provider=(r.get('launch_service_provider') or {}).get('name', ''), rocket=nm.split('|')[0].strip(), mission=mission, pad=p.get('name', '')))
    for s in sites.values(): s.pop('pads', None)
    return sorted(sites.values(), key=lambda s: s['name']), sorted(set(dropped))

# ---------- solutions ----------
def lang_solutions(l):
    s = rd(d(l) + 'Solutions.html'); out = {}
    for m in re.finditer(r'<section ([^>]*class="card-band sol-hub"[^>]*)>(.*?)</section>', s, re.S):
        hub = re.search(r'data-hub="([^"]+)"', m.group(1)).group(1)
        hname = txt(re.search(r'<h2><a[^>]*>(.*?)</a>', m.group(2)).group(1))
        for c in re.findall(r'<article class="card sol-card".*?</article>', m.group(2), re.S):
            u = re.search(r'data-url="([^"]+)"', c).group(1)
            out.setdefault(u, dict(name=txt(re.search(r'<h3>(.*?)</h3>', c, re.S).group(1)), hub=hub, hubname=hname))
    return out
def summary(l, page):
    f = d(l) + page if os.path.exists(d(l) + page) else page
    m = re.search(r'<meta name="description" content="([^"]*)"', rd(f))
    s = html.unescape(m.group(1)) if m else ''
    s = re.sub(r'\s+', ' ', s).strip()
    if len(s) > 170:
        cut = max(s.rfind('. ', 0, 170), s.rfind('。', 0, 170))
        s = s[:cut + 1] if cut > 60 else s[:167].rsplit(' ', 1)[0] + '…'
    return s

# Earth categories use the hub the solution already belongs to. Land is the Forests hub (data-domain="land").
CATS = {'Rivers.html': 'river', 'Lakes.html': 'lake', 'Oceans.html': 'ocean', 'Deforestation.html': 'land',
        'Polar.html': 'polar', 'Planetary_Defense.html': 'defense', 'Earth_Observation.html': 'observe',
        'Space_Weather.html': 'weather', 'Space_Disposal.html': 'disposal', 'Project-Rawane.html': 'rawane', 'Space.html': 'space'}
def build_data(l, LOC, launches):
    sols = lang_solutions(l); items = []
    for u, v in sols.items():
        e = LOC.get(u)
        if not e: continue
        href = u if l == 'en' or os.path.exists(d(l) + u) else '../' + u
        items.append(dict(u=href, n=v['name'], h=v['hub'], hn=v['hubname'], s=summary(l, u), st=e['status'], p=e['pins'], x=e.get('strip', ''), c=CATS.get(v['hub'], '')))
    items.sort(key=lambda i: i['n'].lower())
    hubs = sorted({(i['h'], i['hn']) for i in items}, key=lambda h: h[1].lower())
    return dict(ui=U[l], lang=l, hubs=[dict(f=f, n=n) for f, n in hubs], sols=items, sites=launches)

# ---------- page ----------
def page_html(l, data, n_by):
    u = U[l]; shell = rd(d(l) + 'Kids_Map.html')
    head = shell[:shell.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(u["title"])} | Saving Planets</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + esc(u['desc']) + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + esc(u['title']) + ' | Saving Planets"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'\n?<link rel="stylesheet" href="(?:\.\./)?edu\.css[^"]*">', '', head)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    head = head.replace('Kids_Map.html', 'World_Map.html')
    alts = ''.join(f'\n<link rel="alternate" hreflang="{x}" href="{SITE}{d(x)}World_Map.html">' for x in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}World_Map.html">'
    pre = '' if l == 'en' else '../'
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": u['title'], "description": u['desc'], "url": f"{SITE}{d(l)}World_Map.html", "inLanguage": l,
          "datePublished": "2026-10-15", "dateModified": datetime.date.today().isoformat(), "isPartOf": {"@type": "WebSite", "name": "Saving Planets", "url": SITE}}
    head = re.sub(r'(<link rel="canonical"[^>]*>)', lambda m: m.group(1) + alts, head, count=1)
    head += (f'<link rel="stylesheet" href="{pre}assets/leaflet/leaflet.css?v=1.9.4">\n<link rel="stylesheet" href="{pre}map.css?v={ASSETV}">\n'
             f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    body_open = re.search(r'<body[^>]*>', shell).group(0)
    body_open = re.sub(r'class="[^"]*"', 'class="toc-sub world-map-page"', body_open)
    nav = re.search(r'<a class="skip-link".*?</nav>', shell, re.S).group(0)
    nav = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Kids_Map.html', 'World_Map.html'), nav, flags=re.S)
    foot = shell[shell.index('</main>'):]
    foot = re.sub(r'<script src="(?:\.\./)?(?:edu|edu-extras)\.js[^"]*"[^>]*></script>', '', foot)
    foot = re.sub(r'<!-- GEN [0-9a-f]+ -->', '', foot)
    g = sum(1 for s in data['sols'] if s['st'] == 'active' and s['p']); b = sum(1 for s in data['sols'] if s['st'] == 'upcoming' and s['p'])
    gp = sum(len(s['p']) for s in data['sols'] if s['st'] == 'active'); bp = sum(len(s['p']) for s in data['sols'] if s['st'] == 'upcoming')
    rk = len(data['sites'])
    opts = f'<option value="all">{esc(u["allhubs"])}</option>' + ''.join(f'<option value="{h["f"]}">{esc(h["n"])}</option>' for h in data['hubs'])
    def cat_btn(key, name):
        sw = '' if key == 'all' else f'<span class="wm-swatch wm-{key}" aria-hidden="true"></span>'
        pressed = 'true' if key == 'all' else 'false'
        return f'<button type="button" class="wm-cat" data-cat="{key}" aria-pressed="{pressed}">{sw}{esc(u[name])}</button>'
    cat_btns = ''.join(cat_btn(k, n) for k, n in (
        ('all', 'allcat'), ('river', 'rivers'), ('lake', 'lakes'), ('ocean', 'oceans'), ('land', 'land'),
        ('polar', 'polar'), ('observe', 'observe'), ('weather', 'weather'), ('defense', 'defense'),
        ('disposal', 'disposal'), ('rawane', 'rawane'))) + f'<a class="wm-cat wm-cat-link" href="Space.html#satmap"><span class="wm-swatch wm-space" aria-hidden="true"></span>{esc(u["space"])}</a>'
    def li(s):
        places = '; '.join(p['label'] for p in s['p'])
        badge = u['active'] if s['st'] == 'active' else u['upcoming']
        return f'<li data-cat="{s.get("c","")}" data-hub="{s["h"]}"><a href="{s["u"]}">{esc(s["n"])}</a> <span class="wm-badge wm-{s["st"]}">{esc(badge)}</span> <span class="wm-hubn">{esc(s["hn"])}</span>{" — " + esc(places) if places else ""}</li>'
    strip = lambda key: ''.join(f'<li data-cat="{s.get("c","")}" data-hub="{s["h"]}"><a href="{s["u"]}"><span class="wm-dot wm-{s["st"]}" aria-hidden="true"></span>{esc(s["n"])}</a></li>' for s in data['sols'] if s['x'] == key)
    bylist = ''
    for h in data['hubs']:
        bylist += f'<h3>{esc(h["n"])}</h3><ul>' + ''.join(li(s) for s in data['sols'] if s['h'] == h['f']) + '</ul>'
    sites_list = ''.join(f'<li data-cat="launch"><strong>{esc(s["name"])}</strong>: ' + (', '.join(esc(x["provider"] + " " + x["mission"]) + (f' ({x["net"][:10]})' if x["exact"] else '') for x in s['launches'][:3]) or esc(u['none'])) + '</li>' for s in data['sites'])
    n_sol = len(n_by) if n_by else len(data['sols'])
    rtl = l == 'ar'
    csv = f'{pre}assets/data/export/map.{l}.csv'
    # Oct 17 (user: "remove noise and center map on page"): map-first layout. One short h1 + the map, centred in the viewport below the
    # fixed nav; legend/filters sit on the map as a small key; everything else (orbit/worldwide strips, full list, launch credit, CSV) is
    # in one collapsed "list" section under the map. Hero, lead, count line, data-tools bar and New-this-week strip were removed.
    main = f'''<main id="main" class="wm-main">
<div class="wm-wrap" data-lang="{l}" data-src="{pre}assets/data/map.{l}.json?v={ASSETV}">
<div class="wm-screen">
<section class="wm-hero has-video">
<div class="wm-hero-media" aria-hidden="true"><img class="wm-hero-still" src="{pre}assets/earth/world-map-hero.jpg" alt="" width="1920" height="1080"><video class="wm-hero-video" autoplay muted loop playsinline poster="{pre}assets/earth/world-map-hero.jpg" width="1920" height="1080" preload="auto"><source src="{pre}assets/earth/world-map-hero-2560.mp4" type="video/mp4" media="(min-width: 1600px)"><source src="{pre}assets/earth/world-map-hero-1920.mp4" type="video/mp4"><source src="{pre}assets/earth/world-map-hero-2560.webm" type="video/webm" media="(min-width: 1600px)"><source src="{pre}assets/earth/world-map-hero-1920.webm" type="video/webm"></video><div class="wm-hero-shade"></div></div>
<div class="wm-hero-content"><h1 class="wm-title">{esc(u["h1"].format(n=n_sol))}</h1></div>
<p class="hero-video-credit"><a href="https://sdo.gsfc.nasa.gov/">NASA/SDO</a> / <a href="https://visibleearth.nasa.gov/images/73909/december-blue-marble-next-generation-w-topography-and-bathymetry">NASA Visible Earth</a> / <a href="https://svs.gsfc.nasa.gov/4720/">NASA LRO-SVS</a>; {esc(u["byline"])}</p>
</section>
<p class="wm-space-jump-wrap"><a class="wm-space-jump" href="Space.html#satmap" aria-label="{esc(u["spaceJump"])}">{esc(u["space"])}</a></p>
<script>(function(){{var root=document.documentElement;var cols=[[70,170,255],[255,118,36],[190,208,232]];var keys=[[0,0],[0.35,0],[1.5,1],[2.55,1],[3.4,0],[3.65,0],[4.3,2],[4.65,2],[5,0]];function sm(a,b,t){{var u=(t-a)/(b-a);if(u<0)u=0;else if(u>1)u=1;return u*u*(3-2*u);}}function glow(t){{t=((t%5)+5)%5;var i=0;for(var k=0;k<keys.length-1;k++)if(t>=keys[k][0])i=k;var a=keys[i],b=keys[Math.min(i+1,keys.length-1)],u=sm(a[0],b[0],t),c1=cols[a[1]],c2=cols[b[1]];root.style.setProperty("--wm-glow","rgba("+Math.round(c1[0]+(c2[0]-c1[0])*u)+","+Math.round(c1[1]+(c2[1]-c1[1])*u)+","+Math.round(c1[2]+(c2[2]-c1[2])*u)+",.78)");}}glow(0);var v=document.querySelector(".wm-hero-video");if(!v)return;var rm=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)");function kick(){{if(v.paused){{var p=v.play();if(p&&p.catch)p.catch(function(){{}});}}}}if(rm&&rm.matches){{v.removeAttribute("autoplay");v.autoplay=false;v.pause();[].forEach.call(v.querySelectorAll("source"),function(s){{s.removeAttribute("src");}});v.load();return;}}v.addEventListener("timeupdate",function(){{glow(v.currentTime);}});v.addEventListener("seeked",function(){{glow(v.currentTime);}});v.addEventListener("playing",function(){{var s=document.querySelector(".wm-hero-still");if(s)s.style.visibility="hidden";}});v.addEventListener("canplay",function(){{kick();}});document.addEventListener("visibilitychange",function(){{if(!document.hidden)kick();}});document.addEventListener("DOMContentLoaded",function(){{kick();}});kick();}})();</script>
<div class="wm-key" role="group" aria-label="{esc(u["key"])}">
<div class="wm-cats" role="group" aria-label="{esc(u["show"])}">{cat_btns}</div>
<label class="wm-tog"><input type="checkbox" id="wm-a" checked> <span class="wm-dot wm-active" aria-hidden="true"></span>{esc(u["active"])}</label>
<label class="wm-tog"><input type="checkbox" id="wm-u" checked> <span class="wm-dot wm-upcoming" aria-hidden="true"></span>{esc(u["upcoming"])}</label>
<label class="wm-tog"><input type="checkbox" id="wm-r" checked> <span class="wm-rk" aria-hidden="true">🚀</span>{esc(u["launches"])}</label>
<label class="wm-hubsel"><span class="wm-vh">{esc(u["hub"])}</span><select id="wm-hub">{opts}</select></label>
</div>
<div class="wm-stage">
<div id="wm" class="wm-map" dir="ltr" role="region" aria-label="{esc(u["label"])}"></div>
</div>
<p class="wm-credit"><a href="https://visibleearth.nasa.gov/images/73909/december-blue-marble-next-generation-w-topography-and-bathymetry">NASA Visible Earth / Blue Marble</a>. {esc(u["byline"])}</p>
</div>
<details class="wm-list" id="map-list"><summary>{esc(u["listmore"])}</summary>
<p>{esc(u["listintro"])} <a href="{csv}" download>⬇ {esc(u["csv"])}</a></p>
<section class="wm-strip" id="from-orbit"><h2>🛰️ {esc(u["orbit"])}</h2><p>{esc(u["orbitintro"])}</p><ul class="wm-chips">{strip("orbit")}</ul></section>
<section class="wm-strip" id="worldwide"><h2>🌍 {esc(u["world"])}</h2><p>{esc(u["worldintro"])}</p><ul class="wm-chips">{strip("world")}</ul></section>
{bylist.replace('<h3>', '<h3 class="wm-hubh">')}<h3>🚀 {esc(u["next"])}</h3><ul>{sites_list}</ul>
<p class="wm-src">{esc(u["src"])} <a href="{pre if l != "en" and not os.path.exists(d(l) + "Artemis_II.html") else ""}Artemis_II.html#launches">{esc(u["live"])}</a></p>
</details>
</div>
'''
    scripts = f'<script src="{pre}assets/leaflet/leaflet.js?v=1.9.4" defer></script><script src="{pre}map.js?v={ASSETV}" defer></script>'
    foot = foot.replace('</body>', scripts + '</body>', 1)
    return head + '</head>\n' + body_open + nav + main + foot

DROP = ''  # Oct 15: teardrop reverted; Liquid Glass styling lives in build-ux.py CSS
def link_in(l):
    """Link from Solutions page and homepage (idempotent marker blocks)."""
    n = 0
    lab = {'en': 'See Solutions on the World Map', 'fr': 'Voir les solutions sur la carte du monde', 'es': 'Ver las soluciones en el mapa mundial',
           'ar': 'شاهد كل الحلول على خريطة العالم', 'it': 'Guarda le soluzioni sulla mappa del mondo'}[l]
    blk = f'<!-- WMAP-LINK:START --><p class="wm-cta"><a class="btn hero-cta" href="World_Map.html">{DROP}{esc(lab)}</a></p><!-- WMAP-LINK:END -->'
    for page, anchor in (('Solutions.html', r'<!-- SOL-FILTERS:START -->'), ('index.html', r'<!-- DOMAINS:START -->')):
        p = d(l) + page
        if not os.path.exists(p): continue
        s = rd(p)
        if 'WMAP-LINK:START' in s: s2 = re.sub(r'<!-- WMAP-LINK:START -->.*?<!-- WMAP-LINK:END -->', lambda m: blk, s, flags=re.S)
        else:
            m = re.search(anchor, s)
            s2 = s[:m.start()] + blk + s[m.start():] if m else s
        n += wr(p, s2)
    return n

def sitemap():
    import sitemap_pages
    today = datetime.date.today().isoformat()
    for l in LANGS:
        sitemap_pages.ensure_url(f'{SITE}{d(l)}World_Map.html', today, 'daily', '0.8')

if __name__ == '__main__':
    LOC = json.load(open('assets/data/map-locations.json', encoding='utf8'))['solutions']
    lp = 'assets/data/map-launches.json'
    try:
        if '--no-fetch' in sys.argv: raise RuntimeError('skipped')
        sites, dropped = group_launches(fetch_launches())
        json.dump(dict(generated=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), source='https://ll.thespacedevs.com/2.3.0/launches/upcoming/', excluded_sites=dropped, sites=sites),
                  open(lp, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    except Exception as e:
        print('launch refresh skipped (kept previous):', e)
    L = json.load(open(lp, encoding='utf8')) if os.path.exists(lp) else dict(sites=[], excluded_sites=[])
    en = lang_solutions('en')
    missing = [u for u in en if u not in LOC]
    if missing: print('WARNING: solutions without map-locations.json entry:', ', '.join(missing))
    ch = 0
    for l in LANGS:
        data = build_data(l, LOC, L['sites'])
        ch += wr(f'assets/data/map.{l}.json', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        ch += wr(d(l) + 'World_Map.html', page_html(l, data, en))  # en: solution count for the h1 (same 163 as Solutions.html)
        ch += link_in(l)
    sitemap()
    act = [u for u, e in LOC.items() if e['status'] == 'active']; up = [u for u, e in LOC.items() if e['status'] == 'upcoming']
    print(f"build-map: langs={','.join(LANGS)} solutions={len(LOC)} active={len(act)} upcoming={len(up)} "
          f"green_pins={sum(len(LOC[u]['pins']) for u in act)} blue_pins={sum(len(LOC[u]['pins']) for u in up)} rocket_sites={len(L['sites'])} "
          f"no_pin={sum(1 for e in LOC.values() if not e['pins'])} excluded_sites={L.get('excluded_sites')} writes={ch}")
