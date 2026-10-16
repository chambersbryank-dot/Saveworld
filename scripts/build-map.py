#!/usr/bin/env python3
"""Oct 15: interactive World Map (World_Map.html in en + every language folder that exists, e.g. fr/es/ar/it).
Solution pins come from assets/data/map-locations.json (one entry per solution: status active|upcoming, real pins, strip).
Names, hubs and links come from each language's Solutions.html; one-line summaries from each solution page's meta description.
Rocket pins: Launch Library 2 (The Space Devs, the same feed as the Live Launch Tracker), grouped by launch site, with
Russia, China and North Korea excluded (sites and launches). Writes assets/data/map.<lang>.json + assets/data/map-launches.json.
Idempotent. Run after i18n-build/post-processors and before build-ux.py (weekly-sync.sh). --no-fetch skips the launch refresh."""
import re, os, json, html, sys, glob, datetime, urllib.request
SITE = 'https://www.savingplanets.com/'
ASSETV = '20261015n'
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(html.unescape(s), quote=True)
txt = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
LANGS = ['en'] + [l for l in ['fr', 'es', 'ar', 'it'] if os.path.exists(f'{l}/Solutions.html') and os.path.exists(f'{l}/Kids_Map.html')]
d = lambda l: '' if l == 'en' else l + '/'

U = {
 'en': dict(title='World Solutions Map', desc='An interactive world map of every Saving Planets solution: green pins are working now, blue pins are coming soon, and rocket pins show upcoming launches.',
   lead='Tap a pin to see a solution, where it works and a link to its page. Green pins are active now, blue pins are coming soon, and rocket pins list the next launches from that site.',
   active='Active now', upcoming='Coming soon', rocket='Launch site', hub='Hub', allhubs='All hubs', launches='Launches', show='Show',
   orbit='From Orbit', orbitintro='These solutions work in space, so they have no single place on Earth. Pins mark a launch site only when the solution page names it.',
   world='Worldwide', worldintro='These solutions happen all over the planet, with no single place to pin.',
   list='Map as a list', listintro='The same information as the map, for screen readers and keyboards.', read='Read more',
   next='Upcoming launches', none='No launches scheduled', tbd='date to be confirmed', src='Launch data: The Space Devs Launch Library 2 (same feed as our Live Launch Tracker). Launches by Russia, China and North Korea are not shown.',
   basis_hq='headquarters', basis_launch='launch site', pins='{t} solutions: {g} active · {b} coming soon · {r} launch sites', label='Interactive world map of solutions and launch sites', live='Live Launch Tracker'),
 'fr': dict(title='Carte mondiale des solutions', desc="Une carte interactive de toutes les solutions de Saving Planets : épingles vertes pour celles qui agissent déjà, bleues pour celles à venir, et fusées pour les prochains lancements.",
   lead="Touchez une épingle pour voir une solution, où elle agit et un lien vers sa page. Vert : active ; bleu : bientôt ; fusée : prochains lancements depuis ce site.",
   active='Active', upcoming='Bientôt', rocket='Site de lancement', hub='Pôle', allhubs='Tous les pôles', launches='Lancements', show='Afficher',
   orbit="Depuis l'orbite", orbitintro="Ces solutions agissent dans l'espace et n'ont pas de lieu unique sur Terre. Une épingle marque le site de lancement seulement quand la page le nomme.",
   world='Partout dans le monde', worldintro="Ces solutions agissent sur toute la planète, sans lieu unique à épingler.",
   list='La carte sous forme de liste', listintro="Les mêmes informations que la carte, pour les lecteurs d'écran et le clavier.", read='En savoir plus',
   next='Prochains lancements', none='Aucun lancement prévu', tbd='date à confirmer', src="Données de lancement : The Space Devs Launch Library 2 (la même source que notre suivi des lancements). Les lancements de la Russie, de la Chine et de la Corée du Nord ne sont pas affichés.",
   basis_hq='siège', basis_launch='site de lancement', pins='{t} solutions : {g} actives · {b} bientôt · {r} sites de lancement', label='Carte mondiale interactive des solutions et des sites de lancement', live='Suivi des lancements en direct'),
 'es': dict(title='Mapa mundial de soluciones', desc='Un mapa interactivo de todas las soluciones de Saving Planets: pines verdes para las que ya funcionan, azules para las que llegan pronto y cohetes para los próximos lanzamientos.',
   lead='Toca un pin para ver una solución, dónde actúa y un enlace a su página. Verde: activa; azul: próximamente; cohete: próximos lanzamientos desde ese sitio.',
   active='Activa', upcoming='Próximamente', rocket='Sitio de lanzamiento', hub='Centro', allhubs='Todos los centros', launches='Lanzamientos', show='Mostrar',
   orbit='Desde la órbita', orbitintro='Estas soluciones actúan en el espacio y no tienen un único lugar en la Tierra. Un pin marca el sitio de lanzamiento solo cuando la página lo nombra.',
   world='En todo el mundo', worldintro='Estas soluciones ocurren en todo el planeta, sin un único lugar que marcar.',
   list='El mapa como lista', listintro='La misma información que el mapa, para lectores de pantalla y teclado.', read='Leer más',
   next='Próximos lanzamientos', none='No hay lanzamientos programados', tbd='fecha por confirmar', src='Datos de lanzamientos: The Space Devs Launch Library 2 (la misma fuente que nuestro rastreador de lanzamientos). No se muestran lanzamientos de Rusia, China ni Corea del Norte.',
   basis_hq='sede', basis_launch='sitio de lanzamiento', pins='{t} soluciones: {g} activas · {b} próximamente · {r} sitios de lanzamiento', label='Mapa mundial interactivo de soluciones y sitios de lanzamiento', live='Rastreador de lanzamientos en vivo'),
 'ar': dict(title='خريطة الحلول حول العالم', desc='خريطة تفاعلية لكل حلول Saving Planets: الدبابيس الخضراء لحلول تعمل الآن، والزرقاء لحلول قادمة قريبًا، والصواريخ لعمليات الإطلاق القادمة.',
   lead='اضغط على دبوس لترى الحل ومكان عمله ورابط صفحته. الأخضر: يعمل الآن، الأزرق: قريبًا، الصاروخ: الإطلاقات القادمة من ذلك الموقع.',
   active='يعمل الآن', upcoming='قريبًا', rocket='موقع إطلاق', hub='المركز', allhubs='كل المراكز', launches='الإطلاقات', show='عرض',
   orbit='من المدار', orbitintro='تعمل هذه الحلول في الفضاء، فليس لها مكان واحد على الأرض. يظهر دبوس موقع الإطلاق فقط عندما تذكره صفحة الحل.',
   world='حول العالم', worldintro='تحدث هذه الحلول في كل أنحاء الكوكب، دون مكان واحد لتحديده.',
   list='الخريطة على شكل قائمة', listintro='المعلومات نفسها الموجودة في الخريطة، لقارئات الشاشة ولوحة المفاتيح.', read='اقرأ المزيد',
   next='الإطلاقات القادمة', none='لا توجد إطلاقات مجدولة', tbd='الموعد لم يتأكد بعد', src='بيانات الإطلاق: The Space Devs Launch Library 2 (المصدر نفسه لمتتبع الإطلاقات لدينا). لا تُعرض إطلاقات روسيا والصين وكوريا الشمالية.',
   basis_hq='المقر', basis_launch='موقع الإطلاق', pins='{t} حلًا: {g} يعمل الآن · {b} قريبًا · {r} مواقع إطلاق', label='خريطة عالمية تفاعلية للحلول ومواقع الإطلاق', live='متتبع الإطلاقات المباشر'),
 'it': dict(title='Mappa mondiale delle soluzioni', desc='Una mappa interattiva di tutte le soluzioni di Saving Planets: spilli verdi per quelle già attive, blu per quelle in arrivo e razzi per i prossimi lanci.',
   lead='Tocca uno spillo per vedere una soluzione, dove opera e il link alla sua pagina. Verde: attiva; blu: in arrivo; razzo: prossimi lanci da quel sito.',
   active='Attiva', upcoming='In arrivo', rocket='Sito di lancio', hub='Polo', allhubs='Tutti i poli', launches='Lanci', show='Mostra',
   orbit="Dall'orbita", orbitintro="Queste soluzioni operano nello spazio e non hanno un unico luogo sulla Terra. Uno spillo indica il sito di lancio solo quando la pagina lo nomina.",
   world='In tutto il mondo', worldintro='Queste soluzioni avvengono in tutto il pianeta, senza un unico luogo da segnare.',
   list='La mappa come elenco', listintro='Le stesse informazioni della mappa, per lettori di schermo e tastiera.', read='Scopri di più',
   next='Prossimi lanci', none='Nessun lancio in programma', tbd='data da confermare', src='Dati sui lanci: The Space Devs Launch Library 2 (la stessa fonte del nostro tracker dei lanci). I lanci di Russia, Cina e Corea del Nord non sono mostrati.',
   basis_hq='sede', basis_launch='sito di lancio', pins='{t} soluzioni: {g} attive · {b} in arrivo · {r} siti di lancio', label='Mappa mondiale interattiva di soluzioni e siti di lancio', live='Tracker dei lanci in diretta'),
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

def build_data(l, LOC, launches):
    sols = lang_solutions(l); items = []
    for u, v in sols.items():
        e = LOC.get(u)
        if not e: continue
        href = u if l == 'en' or os.path.exists(d(l) + u) else '../' + u
        items.append(dict(u=href, n=v['name'], h=v['hub'], hn=v['hubname'], s=summary(l, u), st=e['status'], p=e['pins'], x=e.get('strip', '')))
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
    def li(s):
        places = '; '.join(p['label'] for p in s['p'])
        badge = u['active'] if s['st'] == 'active' else u['upcoming']
        return f'<li data-hub="{s["h"]}"><a href="{s["u"]}">{esc(s["n"])}</a> <span class="wm-badge wm-{s["st"]}">{esc(badge)}</span> <span class="wm-hubn">{esc(s["hn"])}</span>{" — " + esc(places) if places else ""}</li>'
    strip = lambda key: ''.join(f'<li data-hub="{s["h"]}"><a href="{s["u"]}"><span class="wm-dot wm-{s["st"]}" aria-hidden="true"></span>{esc(s["n"])}</a></li>' for s in data['sols'] if s['x'] == key)
    bylist = ''
    for h in data['hubs']:
        bylist += f'<h3>{esc(h["n"])}</h3><ul>' + ''.join(li(s) for s in data['sols'] if s['h'] == h['f']) + '</ul>'
    sites_list = ''.join(f'<li><strong>{esc(s["name"])}</strong>: ' + (', '.join(esc(x["provider"] + " " + x["mission"]) + (f' ({x["net"][:10]})' if x["exact"] else '') for x in s['launches'][:3]) or esc(u['none'])) + '</li>' for s in data['sites'])
    main = f'''<main id="main">
<section class="page-hero hero-kids"><div class="page-hero-content"><h1>{esc(u["title"])}</h1><p>{esc(u["desc"])}</p></div><span class="hero-credit">NASA EPIC</span></section>
<div class="wm-wrap" data-lang="{l}" data-src="{pre}assets/data/map.{l}.json?v={ASSETV}">
<p class="wm-lead">{esc(u["lead"])}</p>
<div class="wm-controls" role="group" aria-label="{esc(u["show"])}">
<label class="wm-hubsel"><span>{esc(u["hub"])}</span> <select id="wm-hub">{opts}</select></label>
<label class="wm-tog"><input type="checkbox" id="wm-a" checked> <span class="wm-dot wm-active" aria-hidden="true"></span>{esc(u["active"])}</label>
<label class="wm-tog"><input type="checkbox" id="wm-u" checked> <span class="wm-dot wm-upcoming" aria-hidden="true"></span>{esc(u["upcoming"])}</label>
<label class="wm-tog"><input type="checkbox" id="wm-r" checked> <span class="wm-rk" aria-hidden="true">🚀</span>{esc(u["launches"])}</label>
</div>
<p class="wm-count" aria-live="polite">{esc(u["pins"].format(t=len(LOC), g=sum(1 for e in LOC.values() if e["status"] == "active"), b=sum(1 for e in LOC.values() if e["status"] == "upcoming"), r=rk))}</p>
<div id="wm" class="wm-map" dir="ltr" role="region" aria-label="{esc(u["label"])}"></div>
<p class="wm-src">{esc(u["src"])} <a href="{pre if l != "en" and not os.path.exists(d(l) + "Artemis_II.html") else ""}Artemis_II.html#launches">{esc(u["live"])}</a></p>
<section class="wm-strip" id="from-orbit"><h2>🛰️ {esc(u["orbit"])}</h2><p>{esc(u["orbitintro"])}</p><ul class="wm-chips">{strip("orbit")}</ul></section>
<section class="wm-strip" id="worldwide"><h2>🌍 {esc(u["world"])}</h2><p>{esc(u["worldintro"])}</p><ul class="wm-chips">{strip("world")}</ul></section>
<details class="wm-list" id="map-list"><summary>{esc(u["list"])}</summary><p>{esc(u["listintro"])}</p>{bylist}<h3>🚀 {esc(u["next"])}</h3><ul>{sites_list}</ul></details>
</div>
'''
    scripts = f'<script src="{pre}assets/leaflet/leaflet.js?v=1.9.4" defer></script><script src="{pre}map.js?v={ASSETV}" defer></script>'
    foot = foot.replace('</body>', scripts + '</body>', 1)
    return head + '</head>\n' + body_open + nav + main + foot

def link_in(l):
    """Link from Solutions page and homepage (idempotent marker blocks)."""
    n = 0
    lab = {'en': 'See every solution on the World Map', 'fr': 'Voir toutes les solutions sur la carte du monde', 'es': 'Ver todas las soluciones en el mapa mundial',
           'ar': 'شاهد كل الحلول على خريطة العالم', 'it': 'Guarda tutte le soluzioni sulla mappa del mondo'}[l]
    blk = f'<!-- WMAP-LINK:START --><p class="wm-cta"><a class="btn" href="World_Map.html">🗺️ {esc(lab)}</a></p><!-- WMAP-LINK:END -->'
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
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        loc = f'{SITE}{d(l)}World_Map.html'
        if f'<loc>{loc}</loc>' not in s:
            s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>\n</urlset>')
    wr('sitemap.xml', s)

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
        ch += wr(d(l) + 'World_Map.html', page_html(l, data, None))
        ch += link_in(l)
    sitemap()
    act = [u for u, e in LOC.items() if e['status'] == 'active']; up = [u for u, e in LOC.items() if e['status'] == 'upcoming']
    print(f"build-map: langs={','.join(LANGS)} solutions={len(LOC)} active={len(act)} upcoming={len(up)} "
          f"green_pins={sum(len(LOC[u]['pins']) for u in act)} blue_pins={sum(len(LOC[u]['pins']) for u in up)} rocket_sites={len(L['sites'])} "
          f"no_pin={sum(1 for e in LOC.values() if not e['pins'])} excluded_sites={L.get('excluded_sites')} writes={ch}")
