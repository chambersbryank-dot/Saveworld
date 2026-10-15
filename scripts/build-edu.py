#!/usr/bin/env python3
"""Education features (Oct 14): Kids_Map.html, Lesson_Builder.html, Satellite_Explorer.html + assets/data/edu.<lang>.json.
Data comes from the site itself: Solutions.html (hubs + solution cards), p.amazing-fact on every page (with data-source), Glossary.html.
Also: links from home (Start Here), Amazing Facts (Kid Zone) and Teachers.html; i18n/pages.txt; sitemap.xml; i18n strings (scripts/edu_text.py).
Run after build-site-extras.py and before i18n-build.py (see weekly-sync.sh). Idempotent."""
import json, os, re, sys, html, hashlib, importlib.util
from bs4 import BeautifulSoup
sys.path.insert(0, 'scripts')
import edu_text as X
spec = importlib.util.spec_from_file_location('i18nb', 'scripts/i18n-build.py'); I = importlib.util.module_from_spec(spec); spec.loader.exec_module(I)
SITE = 'https://www.savingplanets.com/'
LANGS = ['fr', 'es', 'ar']
CSSV = '20261014e'
PAGES_NEW = ['Kids_Map.html', 'Lesson_Builder.html', 'Satellite_Explorer.html']
rd = lambda f: open(f, encoding='utf8').read()
esc = lambda s: html.escape(s, quote=True)
txt = lambda el: re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).strip() if el else ''

def write_generated(f, page):
    sig = hashlib.sha1(page.encode('utf8')).hexdigest()[:12]
    page = page.replace('</body>', f'<!-- GEN {sig} --></body>', 1)
    if os.path.exists(f) and f'<!-- GEN {sig} -->' in rd(f): return 0
    open(f, 'w', encoding='utf8').write(page); return 1

# ---------------- data ----------------
def collect():
    sol = BeautifulSoup(rd('Solutions.html'), 'html.parser')
    hubs, page_hub = {}, {}
    for h in sol.select('.sol-hub'):
        hf = h['data-hub']; hs = BeautifulSoup(rd(hf), 'html.parser')
        items = []
        for c in h.select('.sol-card'):
            img = c.select_one('img'); desc = c.select_one('.sol-desc span')
            items.append({'t': txt(c.select_one('h3')), 'u': c['data-url'], 'img': img['src'] if img else '', 'd': txt(desc)})
            page_hub[c['data-url']] = hf
        page_hub[hf] = hf
        hubs[hf] = {'name': txt(hs.select_one('h1')), 'sols': items, 'facts': [], 'text': ' '.join(i['d'] for i in items)}
    for f in sorted(os.listdir('.')):
        if not f.endswith('.html') or f not in page_hub: continue
        s = BeautifulSoup(rd(f), 'html.parser')
        for p in s.select('p.amazing-fact'):
            if not p.get('data-source'): continue
            hubs[page_hub[f]]['facts'].append({'x': txt(p), 'src': p['data-source'], 'sn': p.get('data-source-name') or 'Source', 'page': f})
        if f != page_hub[f]:
            hubs[page_hub[f]]['text'] += ' ' + txt(s.select_one('main'))[:6000]
    g = BeautifulSoup(rd('Glossary.html'), 'html.parser')
    gloss = [{'t': txt(dt), 'id': dt.get('id'), 'd': txt(dt.find_next_sibling('dd'))} for dt in g.select('dt[id]')]
    for hf, h in hubs.items():
        low = h['text'].lower(); scored = []
        for t in gloss:
            n = len(re.findall(r'\b' + re.escape(t['t'].lower()) + r'(s|es)?\b', low))
            if n: scored.append((-n, t['t'], t))
        h['terms'] = [t for _, _, t in sorted(scored)][:12]
        seen = set(); h['facts'] = [f for f in h['facts'] if not (f['x'] in seen or seen.add(f['x']))]
    return hubs

def data_for(lang, hubs, PL):
    m = {} if lang == 'en' else json.load(open(f'i18n/{lang}.json', encoding='utf8'))
    T = (lambda s: s) if lang == 'en' else (lambda s: I.lookup(m, s) or s)
    li = {'en': 0, 'fr': 1, 'es': 2, 'ar': 3}[lang]
    def url(u):  # links from a page in the language folder
        if lang == 'en' or re.match(r'^(https?:|#)', u): return u
        return u if u.split('#')[0] in PL else '../' + u
    out = {'ui': X.UI[lang], 'lesson': X.LESSON[lang], 'hubs': {}}
    for hf, h in hubs.items():
        em, glass = X.BLURB[hf][0], X.BLURB[hf][1]
        blurb = X.BLURB[hf][2 + li]
        out['hubs'][hf] = {'name': T(h['name']), 'emoji': em, 'glass': glass, 'blurb': blurb, 'url': url(hf),
            'sols': [{'t': T(s['t']), 'u': url(s['u']), 'abs': SITE + ('' if lang == 'en' else lang + '/') + s['u'] if s['u'] in PL or lang == 'en' else SITE + s['u'],
                      'img': ('' if lang == 'en' else '../') + s['img'], 'd': T(s['d'])} for s in h['sols']],
            'facts': [{'x': T(f['x']), 'src': f['src'], 'sn': f['sn'], 'page': url(f['page'])} for f in h['facts']],
            'terms': [{'t': T(t['t']), 'd': T(t['d']), 'u': url('Glossary.html#' + t['id'])} for t in h['terms']]}
    return out

# ---------------- page shell ----------------
def shell(page, title, desc, body_class, glass, main, rtype='LearningResource'):
    t = rd('Teachers.html')
    head = t[:t.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} | Saving Planets</title>', head, flags=re.S)
    for k in ('description', 'twitter:description'):
        head = re.sub(rf'<meta name="{k}" content="[^"]*">', f'<meta name="{k}" content="{esc(desc)}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(desc)}">', head)
    head = re.sub(r'<meta (name="twitter:title"|property="og:title") content="[^"]*">', lambda mm: f'<meta {mm.group(1)} content="{esc(title)} | Saving Planets">', head)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    head = re.sub(r'\n?<meta name="i18n-source"[^>]*>', '', head)
    head = head.replace('Teachers.html', page)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    lr = {"@type": rtype, "name": title, "description": desc, "url": SITE + page, "inLanguage": "en", "isAccessibleForFree": True,
          "learningResourceType": "Interactive resource", "publisher": {"@type": "Organization", "name": "Saving Planets", "url": "https://www.savingplanets.com"}}
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": SITE + page, "inLanguage": "en",
          "datePublished": "2026-10-14", "dateModified": "2026-10-14", "isPartOf": {"@type": "WebSite", "name": "Saving Planets", "url": SITE}, "mainEntity": lr}
    head += f'<link rel="stylesheet" href="edu.css?v={CSSV}">\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    nav = re.search(r'<nav id="topnav">.*?</nav>', t, re.S).group(0)
    nav = re.sub(r'<li class="lang-switch".*?</li>', I.switcher(page, 'en', ''), nav, flags=re.S)
    foot = t[t.index('<footer>'):t.index('</footer>') + len('</footer>')]
    scripts = re.findall(r'<script src="site\.js[^"]*"></script>', t)[0]
    return (head + '</head>\n' + f'<body class="toc-sub {body_class}" data-glass="{glass}"><a class="skip-link" href="#main">Skip to content</a>{nav}<main id="main">\n'
            + f'<section class="page-hero"><div class="page-hero-content"><h1>{esc(title)}</h1><p>{esc(desc)}</p></div></section>\n'
            + main + '</main>\n' + foot + scripts + f'<script src="edu.js?v={CSSV}" defer></script></body></html>\n')

MAP_POS = {  # hub: (label, x, y, mobile x, mobile y)
 'Space_Weather.html': ('Space Weather', 86, 12, 72, 6), 'Planetary_Defense.html': ('Asteroids', 60, 10, 28, 13),
 'Space.html': ('Space', 20, 12, 72, 20), 'Space_Disposal.html': ('Space Junk', 38, 27, 28, 28),
 'Project-Rawane.html': ('Earth + Space', 13, 38, 72, 36), 'Earth_Observation.html': ('Satellites', 82, 38, 28, 45),
 'Deforestation.html': ('Forests', 56, 56, 72, 56), 'Oceans.html': ('Oceans', 24, 66, 28, 65),
 'Lakes.html': ('Lakes', 78, 72, 72, 75), 'Rivers.html': ('Rivers', 46, 85, 28, 86)}

def kids_map(hubs):
    svg = ('<svg viewBox="0 0 160 110" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
           + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".7"/>' for x, y, r in [(8,6,.5),(30,4,.4),(45,18,.5),(70,5,.4),(100,20,.5),(120,8,.4),(150,30,.5),(5,60,.4),(140,55,.4),(20,30,.3),(110,40,.3),(90,8,.3)])
           + '<circle cx="138" cy="13" r="10" fill="#ffcc4d"/><circle cx="138" cy="13" r="14" fill="#ffcc4d" opacity=".25"/>'
           + '<circle cx="96" cy="11" r="3" fill="#8a7a6a"/><circle cx="95" cy="10" r=".8" fill="#6d5f52"/>'
           + '<circle cx="18" cy="52" r="5" fill="#d9d9e3"/><circle cx="17" cy="51" r="1" fill="#b9b9c8"/>'
           + '<g transform="translate(128 52) rotate(-20)"><rect x="-2" y="-1.5" width="4" height="3" fill="#cfd8dc"/><rect x="-8" y="-1" width="5" height="2" fill="#4f7fd8"/><rect x="3" y="-1" width="5" height="2" fill="#4f7fd8"/></g>'
           + '<circle cx="80" cy="128" r="62" fill="#1e88e5"/><circle cx="80" cy="128" r="64" fill="none" stroke="#8fd3ff" stroke-width="1.5" opacity=".5"/>'
           + '<path d="M50 80c8-6 20-4 24 2s-2 12-10 12-8 6-16 4-6-12 2-18z" fill="#43a047"/><path d="M88 74c10-4 22 0 24 8s-8 10-14 8-16-10-10-16z" fill="#2e7d32"/>'
           + '<path d="M100 96c6-2 12 2 12 6s-8 6-12 2z" fill="#66bb6a"/><ellipse cx="116" cy="104" rx="4" ry="2.4" fill="#4dd0e1"/>'
           + '<path d="M58 112c6-8 14-6 22-10" stroke="#4dd0e1" stroke-width="1.6" fill="none"/></svg>')
    btns = ''.join(f'<button type="button" class="edu-bubble glass" data-tint="{X.BLURB[h][1]}" data-hub="{h}" aria-pressed="false" '
                   f'style="left:{x}%;top:{y}%;--mx:{mx}%;--my:{my}%"><span class="em" aria-hidden="true">{X.BLURB[h][0]}</span>{lab}</button>'
                   for h, (lab, x, y, mx, my) in MAP_POS.items() if h in hubs)
    nos = ''.join(f'<li><a href="{h}">{esc(hubs[h]["name"])}</a></li>' for h in MAP_POS if h in hubs)
    main = ('<div class="edu-wrap">'
            '<p class="edu-lead">Tap a bubble to explore a part of our planet. Every bubble has a wow fact and real solutions that help both people and nature.</p>'
            '<p class="km-tools"><button type="button" class="edu-bubble glass" data-tint="sun" id="km-surprise"><span class="em" aria-hidden="true">🎲</span>Surprise me!</button></p>'
            f'<div class="km-stage" id="km" role="group" aria-label="Map of our planet with bubbles to tap">{svg}{btns}</div>'
            '<p class="edu-error" hidden>Sorry, the map could not load. Please refresh the page.</p>'
            '<noscript><div class="km-noscript"><p>The map needs JavaScript. You can still visit every part of the planet here:</p><ul>' + nos + '</ul></div></noscript>'
            '<section class="km-panel" id="km-panel" aria-live="polite" hidden></section>'
            '<h2>For grown-ups</h2><p>Every fact on this map comes from a Saving Planets page and links to its original source. Teachers can turn any part of the map into a lesson with the <a href="Lesson_Builder.html">Lesson Plan Builder</a>.</p>'
            '<p><a class="edu-bubble glass" data-tint="space" href="Satellite_Explorer.html"><span class="em" aria-hidden="true">🛰️</span>Satellite Explorer</a> '
            '<a class="edu-bubble glass" data-tint="ocean" href="Amazing_Facts.html"><span class="em" aria-hidden="true">✨</span>Amazing Facts</a></p></div>\n')
    return shell('Kids_Map.html', 'Kids Planet Map', 'A playful map of our planet for kids: tap Oceans, Forests, Lakes, Rivers, Space and more to get a wow fact and real solutions that help people and nature.', 'kids-map-page', 'ocean', main)

def lesson_builder(hubs):
    bands = [('k3', 'K-3 (ages 5-8)'), ('g45', 'Grades 4-5'), ('g68', 'Grades 6-8'), ('g912', 'Grades 9-12'), ('uni', 'University')]
    opts = lambda xs, sel=None: ''.join(f'<option value="{v}"' + (' selected' if v == sel else '') + f'>{esc(l)}</option>' for v, l in xs)
    hub_opts = sorted(((h, v['name']) for h, v in hubs.items()), key=lambda x: x[1])
    main = ('<div class="edu-wrap">'
            '<p class="edu-lead">Pick a grade band, a topic and a lesson length. We build a printable plan from Saving Planets pages: objectives, activities, Amazing Facts, solution pages, vocabulary and citations.</p>'
            '<form id="lb" class="lb-form glass" data-tint="earth">'
            f'<div><label for="lb-band">Grade band</label><select id="lb-band" name="band">{opts(bands, "g45")}</select></div>'
            f'<div><label for="lb-hub">Topic</label><select id="lb-hub" name="hub">{opts(hub_opts, "Oceans.html")}</select></div>'
            f'<div><label for="lb-min">Lesson length</label><select id="lb-min" name="min">{opts([("30", "30 minutes"), ("45", "45 minutes"), ("60", "60 minutes"), ("90", "90 minutes")], "45")}</select></div>'
            '<div><button type="submit" class="edu-bubble glass" data-tint="sun"><span class="em" aria-hidden="true">📝</span>Build my lesson plan</button></div></form>'
            '<div class="lb-actions"><button type="button" id="lb-print" class="edu-bubble glass" data-tint="earth" hidden><span class="em" aria-hidden="true">🖨️</span>Print plan</button></div>'
            '<p class="lb-small no-print">Tip: the link in your address bar saves your choices, so you can share the plan with a colleague.</p>'
            '<p class="edu-error" hidden>Sorry, the lesson builder could not load. Please refresh the page.</p>'
            '<article class="lb-plan" id="lb-plan" aria-live="polite" hidden></article>'
            '<p class="no-print"><a href="Teachers.html">Teacher Sheets</a> · <a href="Glossary.html">Glossary</a> · <a href="Kids_Map.html">Kids Planet Map</a> · <a href="Satellite_Explorer.html">Satellite Explorer</a></p></div>\n')
    return shell('Lesson_Builder.html', 'Lesson Plan Builder', 'Free printable lesson plans for K-3 to university, built from real environmental and space solutions that help both people and nature.', 'lesson-builder-page', 'earth', main)

PARTS = [  # id, emoji, name, slot label, x, y, [L1, L2, L3], extra L3 html
 ('bus', '📦', 'Bus', 'Spot for the bus', 50, 50),
 ('payload', '🔭', 'Payload', 'Spot for the payload', 50, 80),
 ('sensors', '🧭', 'Pointing sensors', 'Spot for the sensors', 50, 20),
 ('solar', '☀️', 'Solar arrays', 'Spot for the solar arrays', 16, 50),
 ('propulsion', '🔥', 'Propulsion', 'Spot for propulsion', 84, 74),
 ('antennas', '📡', 'Antennas', 'Spot for the antennas', 84, 26)]
PART_TEXT = {
 'bus': ['The bus is the satellite’s body. It holds everything together, like a backpack that carries all the tools.', 'The bus gives the satellite its structure, shares out electricity, keeps parts at safe temperatures, runs the onboard computer and controls which way the satellite points. Engineers often reuse one bus design for many different missions.', 'Bus subsystems: structure, electrical power, thermal control, command and data handling, attitude determination and control, and communications. Designers trade the mass, power and volume budgets against what the payload needs.'],
 'payload': ['The payload is the satellite’s job tool, like a camera that takes pictures of forests from space!', 'The payload is the reason the satellite exists: cameras, radar or instruments that measure air, ice, forests or oceans. Everything else on board is there to help the payload do its job.', 'Payload requirements (resolution, spectral bands, revisit time, data volume) drive the choice of orbit and the size of the power, pointing and downlink systems. Radar payloads need large antennas and high power; optical payloads need very stable pointing.'],
 'sensors': ['Satellites use star cameras to see which way they are pointing, like sailors using the stars to find their way.', 'Star trackers, sun sensors and gyroscopes tell the satellite which way it is facing. A GPS receiver tells it where it is in orbit.', 'Attitude determination fuses star tracker, gyroscope, sun sensor and magnetometer data, often with a Kalman filter. Reaction wheels, magnetorquers or thrusters then turn the spacecraft to keep instruments and antennas on target.'],
 'solar': ['Solar panels are the satellite’s lunch. They turn sunlight into electricity!', 'Solar arrays turn sunlight into electricity, and batteries store some of it for when the satellite passes through Earth’s shadow.', 'Array sizing accounts for the time spent in eclipse, cell efficiency, the sun angle and the slow loss of output from radiation over the mission. Satellites commonly use multi-junction cells, which convert more sunlight per square meter than typical rooftop panels.'],
 'propulsion': ['Little rocket thrusters give gentle pushes so the satellite stays in the right place.', 'Thrusters raise or adjust the orbit and help dodge space junk. At the end of the mission they can push the satellite down to burn up, so it does not become debris.', 'Chemical thrusters give high thrust; electric thrusters (ion or Hall-effect) use far less propellant but push gently for a long time. Planning end-of-life disposal is part of space sustainability, as in the'],
 'antennas': ['Antennas let the satellite talk to Earth, sending pictures home through the air!', 'Antennas send data down and receive commands. Ground stations around the world catch the signals as the satellite flies overhead.', 'Link budgets balance transmitter power, antenna gain, distance, frequency and noise. Radio spectrum is limited and licensed, one reason missions are turning to laser links and to processing data on board.']}

def sat_explorer():
    svg = ('<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">'
           + ''.join(f'<circle cx="{x}" cy="{y}" r=".5" fill="#fff" opacity=".7"/>' for x, y in [(8,8),(25,92),(70,6),(92,90),(40,4),(96,45),(4,70)])
           + '<rect x="34" y="36" width="32" height="28" rx="3" fill="#b0bec5" stroke="#eceff1" stroke-width=".8"/>'
           + '<rect x="2" y="42" width="28" height="16" fill="#3f51b5" stroke="#c5cae9" stroke-width=".6"/><path d="M9 42v16M16 42v16M23 42v16M2 50h28" stroke="#c5cae9" stroke-width=".4"/><path d="M30 50h4" stroke="#eceff1" stroke-width="1.2"/>'
           + '<path d="M66 40 78 30" stroke="#eceff1" stroke-width="1"/><path d="M74 22a10 10 0 0 1 12 12z" fill="#eceff1"/>'
           + '<path d="M66 60 76 68l6 10h-8z" fill="#78909c"/><path d="M76 80l3 6 3-6" fill="#ff8a65"/>'
           + '<rect x="44" y="64" width="12" height="8" fill="#546e7a"/><circle cx="50" cy="75" r="4" fill="#263238" stroke="#90a4ae"/>'
           + '<rect x="46" y="28" width="8" height="8" fill="#90a4ae"/><circle cx="50" cy="26" r="2.5" fill="#263238"/></svg>')
    slots = ''.join(f'<button type="button" class="sx-slot" data-part="{p}" aria-label="{lab}" style="left:{x}%;top:{y}%">?</button>' for p, e, n, lab, x, y in PARTS)
    tray = ''.join(f'<li><button type="button" class="sx-part edu-bubble glass" data-tint="space" data-part="{p}" data-em="{e}" data-name="{n}" aria-pressed="false"><span class="em" aria-hidden="true">{e}</span>{n}</button></li>' for p, e, n, lab, x, y in PARTS)
    # data-name must be translated too: use title attribute trick -> keep visible text; JS reads data-name. Translations: handled in post step.
    cards = ''
    for p, e, n, lab, x, y in PARTS:
        L = PART_TEXT[p]
        extra = ' <a href="Zero_Debris_Charter.html">Zero Debris Charter</a>.' if p == 'propulsion' else ''
        cards += (f'<article class="sx-card" id="part-{p}"><h3><span aria-hidden="true">{e}</span> {n}</h3>'
                  f'<p data-level="1">{L[0]}</p><p data-level="2">{L[1]}</p><p data-level="3">{L[2]}{extra}</p></article>')
    msgs = ''.join(f'<span hidden data-msg="{k}">{v}</span>' for k, v in [('wrong', 'Try another spot!'), ('right', 'Nice!'), ('done', 'You built a satellite! Read about each part below.'),
                    ('pick', 'Now tap its spot on the satellite:'), ('first', 'Pick a part first.'), ('drop', 'Drop it on a dashed spot.'), ('reset', 'Satellite cleared. Ready to build again!')])
    lv = lambda v, lab, chk='': f'<label><input type="radio" name="sx-level" value="{v}"{chk}><span class="edu-bubble glass" data-tint="space">{lab}</span></label>'
    src = lambda u, t: f'<li><a href="{u}" rel="noopener">{t}</a></li>'
    main = ('<div class="edu-wrap">'
            '<p class="edu-lead">Build a satellite! Drag each part onto its spot (or tap a part, then tap its spot). Then pick a level to go from a K-3 wow to university detail.</p>'
            '<fieldset class="sx-levels"><legend>Choose your level</legend>' + lv(1, 'Wow (K-3)', ' checked') + lv(2, 'Explorer (grades 4-12)') + lv(3, 'University') + '</fieldset>'
            f'<div id="sx">{msgs}<div class="sx-lab"><div class="sx-stage" role="group" aria-label="Satellite drawing with spots for each part">{svg}{slots}</div>'
            f'<div><h2 id="sx-tray-h" style="margin-top:0">Satellite parts</h2><ul class="sx-tray" aria-labelledby="sx-tray-h">{tray}</ul>'
            '<p style="margin-top:.8rem"><button type="button" id="sx-auto" class="edu-bubble glass" data-tint="sun"><span class="em" aria-hidden="true">🪄</span>Build it for me</button> '
            '<button type="button" id="sx-reset" class="edu-bubble glass" data-tint="earth"><span class="em" aria-hidden="true">🔄</span>Start over</button></p></div></div>'
            '<p class="sx-status" id="sx-status" role="status" aria-live="polite"></p></div>'
            '<div id="sx-body" class="lvl-1">'
            f'<h2>What each part does</h2><div class="sx-info">{cards}</div>'
            '<section class="sx-deep" id="laser"><h2>Laser communication: talking with light</h2>'
            '<p data-level="1">Some satellites send messages with invisible laser light instead of radio. It is like sending a whole library home in minutes!</p>'
            '<p data-level="2">Laser (optical) links pack information into infrared light. The beam is very narrow, so it can carry far more data than radio, but the satellite must point it very precisely, and clouds can block it.</p>'
            '<p data-level="3">Laser (optical) links pack information into infrared light. The beam is very narrow, so it can carry far more data than radio, but the satellite must point it very precisely, and clouds can block it.</p>'
            '<p>In 2023, NASA’s TBIRD CubeSat sent 4.8 terabytes of error-free data to the ground in under five minutes at 200 gigabits per second, the fastest satellite-to-ground data link on record.</p>'
            '<p data-level="3">Optical terminals need extremely precise pointing, ground stations at clear-sky sites, and error-recovery protocols (TBIRD used automatic repeat request) to survive atmospheric fading.</p>'
            '<p><b>How it helps people and nature: faster downlinks get flood, fire and forest data to the people who need it sooner.</b></p></section>'
            '<section class="sx-deep" id="orbit-compute"><h2>Computing in orbit (SI in space)</h2>'
            '<p data-level="1">Some satellites have a tiny SI brain that throws away cloudy pictures before sending them home!</p>'
            '<p>In 2020, ESA’s Φ-sat-1 became the first European satellite to run a deep-learning SI model on board. It sorted cloudy images from clear ones, so only useful pictures were sent to the ground.</p>'
            '<p>On the ground, many data centers use water for cooling. Lawrence Berkeley National Laboratory estimated that US data centers directly consumed about 66 billion liters of water in 2023 (about 17 billion gallons), up from about 21 billion liters in 2014.</p>'
            '<p>In orbit, waste heat is radiated into space, so a data center there would not need cooling water. The EU-funded ASCEND study, led by Thales Alenia Space (2024), found space data centers could be feasible, but would only cut carbon emissions if launchers became about ten times less emitting over their whole life cycle.</p>'
            '<p>Early flights are already testing chips in orbit. See our <a href="Orbital_Data_Centers.html">Orbital Data Centers</a> page.</p>'
            '<p data-level="3">Trade-offs to weigh: radiation hardening, radiator mass and area, launch emissions, debris risk, repair, and the delay of sending results down. Honest comparisons count the whole life cycle, not just cooling water.</p>'
            '<p><b>How it helps people and nature: less water drawn from rivers and lakes for cooling, and quicker answers from satellite data.</b></p></section>'
            '<section class="sx-deep sx-cite"><h2>Sources</h2><ul>'
            + src('https://science.nasa.gov/learn/basics-of-space-flight/chapter11-1/', 'NASA, Basics of Space Flight: Typical Onboard Systems')
            + src('https://www.nasa.gov/smallsat-institute/sst-soa/', 'NASA, State-of-the-Art of Small Spacecraft Technology')
            + src('https://www.nasa.gov/centers-and-facilities/goddard/nasa-partners-achieve-fastest-space-to-ground-laser-comms-link/', 'NASA, NASA and partners achieve fastest space-to-ground laser comms link (TBIRD)')
            + src('https://www.esa.int/Applications/Observing_the_Earth/Ph-sat', 'ESA, Φ-sat')
            + src('https://indico.esa.int/event/338/contributions/5692/', 'ESA ADCSS 2020, PhiSat-1 applies AI to Earth observation imagery in flight')
            + src('https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report_1.pdf', 'Lawrence Berkeley National Laboratory, 2024 United States Data Center Energy Usage Report')
            + src('https://www.thalesaleniaspace.com/en/press-releases/thales-alenia-space-reveals-results-ascend-feasibility-study-space-data-centers-0', 'Thales Alenia Space, Results of the ASCEND feasibility study on space data centers (2024)')
            + '</ul></section></div>'
            '<p><a class="edu-bubble glass" data-tint="earth" href="Lesson_Builder.html"><span class="em" aria-hidden="true">📝</span>Make a lesson plan</a> '
            '<a class="edu-bubble glass" data-tint="ocean" href="Kids_Map.html"><span class="em" aria-hidden="true">🗺️</span>Kids Planet Map</a></p></div>\n')
    return shell('Satellite_Explorer.html', 'Satellite Explorer', 'An interactive satellite explorer: drag the parts of a satellite into place, then learn about laser communication and computing in orbit, from K-3 to university.', 'satellite-explorer-page', 'space', main)

# ---------------- links into existing pages ----------------
def strip_links(s):
    return re.sub(r'<!-- EDU-LINKS:START -->[\s\S]*?<!-- EDU-LINKS:END -->', '', s)
def edu_links(which, prefix=''):
    items = {'map': ('ocean', '🗺️', 'Kids_Map.html', 'Kids Planet Map', 'Tap a bubble, get a wow fact.'),
             'lesson': ('earth', '📝', 'Lesson_Builder.html', 'Lesson Plan Builder', 'Build a printable plan in seconds.'),
             'sat': ('space', '🛰️', 'Satellite_Explorer.html', 'Satellite Explorer', 'Drag the parts, build a satellite.')}
    return ('<!-- EDU-LINKS:START --><nav class="edu-links" aria-label="Learning tools">' + ''.join(
        f'<a class="edu-bubble glass" data-tint="{t}" href="{u}"><span class="em" aria-hidden="true">{e}</span><span>{n}<span class="lb-small" style="display:block;color:inherit;font-weight:500">{d}</span></span></a>'
        for t, e, u, n, d in (items[w] for w in which)) + '</nav><!-- EDU-LINKS:END -->')
def ensure_css(s):
    if 'edu.css' in s: return re.sub(r'edu\.css\?v=[0-9a-z]+', f'edu.css?v={CSSV}', s)
    return s.replace('</head>', f'<link rel="stylesheet" href="edu.css?v={CSSV}">\n</head>', 1)
def inject():
    n = 0
    for f, anchor, which, where in [('index.html', '<!-- AUDIENCE:END -->', ['map', 'lesson', 'sat'], 'after'),
                                    ('Amazing_Facts.html', '<!-- FACTS:START -->', ['map', 'sat'], 'before'),
                                    ('Teachers.html', '<p class="t-intro">', ['lesson', 'map', 'sat'], 'before')]:
        s0 = rd(f); s = strip_links(s0)
        if anchor not in s: print('edu: anchor missing in', f); continue
        blk = edu_links(which)
        s = s.replace(anchor, anchor + blk, 1) if where == 'after' else s.replace(anchor, blk + anchor, 1)
        s = ensure_css(s)
        if s != s0: open(f, 'w', encoding='utf8').write(s); n += 1
    return n

def main():
    hubs = collect()
    # pages.txt + translations
    pl = rd('i18n/pages.txt'); PL = set(pl.split())
    add = [p for p in PAGES_NEW if p not in PL]
    if add: open('i18n/pages.txt', 'w', encoding='utf8').write(pl.rstrip('\n') + '\n' + '\n'.join(add) + '\n'); PL |= set(add)
    T = dict(X.T)
    for i, l in enumerate(LANGS):
        p = f'i18n/{l}.json'; m = json.load(open(p, encoding='utf8')); n0 = dict(m)
        for k, v in T.items(): m[k] = v[i]
        for lab, *_ in MAP_POS.values(): pass
        if m != n0: json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    os.makedirs('assets/data', exist_ok=True)
    for l in ['en'] + LANGS:
        json.dump(data_for(l, hubs, PL), open(f'assets/data/edu.{l}.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    w = write_generated('Kids_Map.html', kids_map(hubs)) + write_generated('Lesson_Builder.html', lesson_builder(hubs)) + write_generated('Satellite_Explorer.html', sat_explorer())
    k = inject()
    sm = rd('sitemap.xml'); sm0 = sm
    for p in PAGES_NEW:
        if f'savingplanets.com/{p}<' not in sm:
            sm = sm.replace('  <url><loc>https://www.savingplanets.com/Teachers.html</loc>', f'  <url><loc>https://www.savingplanets.com/{p}</loc><lastmod>2026-10-14</lastmod></url>\n  <url><loc>https://www.savingplanets.com/Teachers.html</loc>', 1)
    if sm != sm0: open('sitemap.xml', 'w', encoding='utf8').write(sm)
    print(f'edu: {w} pages written, {k} pages linked, {len(hubs)} hubs, {sum(len(h["sols"]) for h in hubs.values())} solutions, {sum(len(h["facts"]) for h in hubs.values())} facts')

def post_translate():
    """After i18n-build: translate data-name on satellite parts (attribute not in the pipeline's list)."""
    for l in LANGS:
        f = f'{l}/Satellite_Explorer.html'
        if not os.path.exists(f): continue
        m = json.load(open(f'i18n/{l}.json', encoding='utf8')); s0 = rd(f)
        s = re.sub(r'data-name="([^"]+)"', lambda mm: 'data-name="' + esc(m.get(html.unescape(mm.group(1)), html.unescape(mm.group(1)))) + '"', s0)
        if s != s0: open(f, 'w', encoding='utf8').write(s)

if __name__ == '__main__':
    post_translate() if '--translated' in sys.argv else main()
