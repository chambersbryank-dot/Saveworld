#!/usr/bin/env python3
"""Nov 23, 2026 (Hawaii): Sentinel Asia, JJ-FAST, and DLR ZKI.

Clones the Hawaiian Monk Seal page shell and hand-wires listings.
Does not run the full weekly sync. MOXIE is not in this batch.
"""
import importlib.util, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, 'scripts')
spec = importlib.util.spec_from_file_location('batch1123e', os.path.join(ROOT, 'scripts', 'batch-1123e.py'))
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)

e.TODAY = '2026-11-23'
e.UNTIL = '2026-12-23'
e.OLD_TOTAL = 302
e.TOTAL = 305
e.NEW_COUNTS = {'earth-observation': 52, 'forests': 44}

SA_ABOUT = 'https://sentinel-asia.org/aboutsa/AboutSA.html'
SA_MEM = 'https://sentinel-asia.org/jptmember/JPTMember.html'
SA_JAXA = 'https://earth.jaxa.jp/en/application/disaster/sentinel-asia/index.html'
JICA = 'https://www.jica.go.jp/english/information/topics/2023/p20240201_01.html'
JJ_DATA = 'https://earth.jaxa.jp/en/data/2530/index.html'
ZKI = 'https://www.dlr.de/en/zki/'
ZKI_2013 = 'https://www.dlr.de/en/eoc/latest/news/2013/on-call-satellite-data-for-emergency-response'
ZKI_ACT = 'https://activations.zki.dlr.de/en/activations/items/ACT116/'

e.PAGES = [
 dict(
    file='Sentinel_Asia.html', title='Sentinel Asia', hub='earth-observation',
    hub_file='Earth_Observation.html', anchor='International_Charter.html', hub_anchor='International_Charter.html',
    region='orbit', glass='earth', tint='space', klass='agency',
    img='assets/Sentinel_Asia_Myanmar_Flood.jpg', w=1600, h=1130,
    alt='Copernicus flood map of Monyo, Myanmar, on 1 August 2015, the kind of satellite flood map disaster agencies use',
    credit='Image: European Space Agency / Copernicus Emergency Management Service, CC BY-SA 3.0 IGO. Flood map of Monyo, Myanmar, 1 August 2015.',
    credit_url='https://commons.wikimedia.org/wiki/File:Flooded_Myanmar_ESA345485.jpg',
    blurb='Sentinel Asia shares satellite images with disaster agencies across the Asia-Pacific, and JAXA is its executive secretariat.',
    label='Agency solution · active',
    eli=['Sentinel Asia is a team of space agencies and disaster offices across the Asia-Pacific.',
         'When a disaster hits, a member can ask for satellite pictures, and analysis teams turn them into damage maps.',
         'JAXA runs the secretariat, and the Asian Disaster Reduction Center takes the emergency requests.'],
    who=dict(text=['Sentinel Asia is a voluntary initiative of the Asia-Pacific Regional Space Agency Forum. JAXA is the executive secretariat, and the Asian Disaster Reduction Center is the contact for emergency observation requests. It launched in 2006.'],
             sources=[('JAXA Earth-graphy, Sentinel Asia', SA_JAXA)]),
    what=dict(text=['After an emergency request, member satellites collect images and analysis organizations turn them into damage information. JAXA says it provides the satellite data and the damage information free of charge. The members page counts 130 Joint Project Team members: 109 organizations from 30 countries and regions, and 21 international organizations. That table lists 10 data-provider nodes and 65 data-analysis nodes.'],
              sources=[('JAXA Earth-graphy, Sentinel Asia', SA_JAXA), ('Sentinel Asia, JPT members', SA_MEM)]),
    when=dict(text=['The idea was proposed in November 2004. The technical concept was finished in May 2005 in Kuala Lumpur, and APRSAF-12 in Kitakyushu approved it in October 2005. The first step ran from February 2006 to December 2007.'],
              sources=[('Sentinel Asia, About', SA_ABOUT)]),
    where=dict(text=['The work covers the Asia-Pacific. Joint Project Team members, or member organizations of the Asian Disaster Reduction Center, can request an emergency observation, and the images and maps are shared on the web.'],
               sources=[('Sentinel Asia, About', SA_ABOUT), ('JAXA Earth-graphy, Sentinel Asia', SA_JAXA)]),
    why=dict(text=['The aim is to reduce the harm of floods, earthquakes, landslides, and other disasters by sharing a wide satellite view quickly, so warnings and relief can go to the places the maps show were hit.'],
             sources=[('JAXA Earth-graphy, Sentinel Asia', SA_JAXA), ('Sentinel Asia, About', SA_ABOUT)]),
    impact='An emergency request brings satellite images and damage maps onto a shared system while the disaster is still unfolding, so agencies can see which places are hit and send help there sooner.',
    impact_src=[('JAXA Earth-graphy, Sentinel Asia', SA_JAXA), ('Sentinel Asia, About', SA_ABOUT)],
    people='When a disaster agency requests an emergency observation, member satellites collect images and analysis teams post damage maps, so responders can see which towns and rivers are hit and send warnings and relief there sooner.',
    people_src=('JAXA Earth-graphy, Sentinel Asia', SA_JAXA),
    nature='Those maps show flooded land, burned ground, and landslide scars across a wide area, so the places that need protection are marked from space instead of waiting for a ground survey alone.',
    nature_src=('Sentinel Asia, About', SA_ABOUT),
    official=SA_ABOUT, button='Read the Sentinel Asia page',
    ways='Sentinel Asia shares satellite images and damage maps with disaster agencies across the Asia-Pacific.',
    help='JAXA is the executive secretariat, and the Asian Disaster Reduction Center receives the emergency requests.',
    next=[('International Charter: Space and Major Disasters', 'International_Charter.html'),
          ('Copernicus Emergency Management Service: On-Demand Mapping', 'Copernicus_EMS.html'),
          ('GSMaP Global Rainfall Map (JAXA)', 'GSMaP.html')],
    sources=[('Sentinel Asia, About', SA_ABOUT), ('JAXA Earth-graphy, Sentinel Asia', SA_JAXA), ('Sentinel Asia, JPT members', SA_MEM)],
 ),
 dict(
    file='JJ-FAST.html', title='JJ-FAST', hub='forests',
    hub_file='Deforestation.html', anchor='GEDI.html', hub_anchor='GEDI.html',
    region='orbit', glass='forests', tint='land', klass='agency',
    img='assets/ALOS-2_PALSAR-2_Antenna.jpg', w=1600, h=1067,
    alt="The PALSAR-2 radar antenna of JAXA's ALOS-2 satellite, the instrument JJ-FAST uses to see tropical forest through clouds",
    credit='Photo: テレストレラッソ, CC BY-SA 4.0. PALSAR-2 antenna of the ALOS-2 satellite.',
    credit_url='https://commons.wikimedia.org/wiki/File:ALOS-2-PALSAR-2.jpg',
    blurb="JJ-FAST uses JAXA's ALOS-2 radar to flag tropical deforestation through cloud cover, and it updates about every month and a half.",
    label='Agency solution · active',
    eli=['JJ-FAST is a forest watch run by JICA and JAXA.',
         'It uses the ALOS-2 radar satellite, which can see the ground when clouds cover the trees.',
         'It posts forest-change maps about every month and a half, and officers can download them.'],
    who=dict(text=['JJ-FAST is the JICA-JAXA Forest Early Warning System in the Tropics. JAXA lists JICA as the provider. It is a web system that uses the ALOS-2 satellite to watch tropical forests.'],
             sources=[('JAXA Earth-graphy, JJ-FAST', JJ_DATA)]),
    what=dict(text=['The product is forest-change data from ALOS-2. People can open it as a web map or download KML and shapefiles. JICA describes it as early detection of deforestation with DAICHI-2 data that cloud cover does not block, in 78 countries.'],
              sources=[('JAXA Earth-graphy, JJ-FAST', JJ_DATA), ('JICA, March 6, 2024', JICA)]),
    when=dict(text=['JAXA\'s data page says Brazil has been covered since April 2016, and other tropical regions from April 2016 through March 2024. The maps refresh about every month and a half.'],
              sources=[('JAXA Earth-graphy, JJ-FAST', JJ_DATA)]),
    where=dict(text=['The catalog describes the area as the whole world, with that Brazil and tropical-region window. JICA describes the early-warning work as covering 78 countries.'],
               sources=[('JAXA Earth-graphy, JJ-FAST', JJ_DATA), ('JICA, March 6, 2024', JICA)]),
    why=dict(text=['Radar is used because clouds and rain do not block it the way they block a camera satellite. A forest officer can download a new clearing map and check the ground while the cut is still new, including in the rainy season.'],
             sources=[('JICA, March 6, 2024', JICA), ('JAXA Earth-graphy, JJ-FAST', JJ_DATA)]),
    impact='Clouds do not hide a new clearing from ALOS-2 radar, and the map is refreshed about every month and a half, so a check on the ground can happen in the rainy season instead of waiting for a clear photograph.',
    impact_src=[('JICA, March 6, 2024', JICA), ('JAXA Earth-graphy, JJ-FAST', JJ_DATA)],
    people='ALOS-2 radar marks forest change even when clouds hide the canopy, and a forest officer can download that map and go look while the clearing is still new, including in the rainy season.',
    people_src=('JICA, March 6, 2024', JICA),
    nature='Finding a clearing while it is still new is what the early-warning map is for: it gives forest agencies a chance to act before more tropical forest is cut.',
    nature_src=('JICA, March 6, 2024', JICA),
    official=JJ_DATA, button='Read the JAXA data page',
    ways='JJ-FAST uses ALOS-2 radar to flag tropical deforestation through cloud cover in 78 countries.',
    help='JICA and JAXA run this public system.',
    next=[('GEDI Forest Lidar (NASA)', 'GEDI.html'),
          ('Global Forest Watch (WRI)', 'Global_Forest_Watch.html'),
          ('European Forest Fire Information System (EFFIS)', 'EFFIS.html')],
    sources=[('JAXA Earth-graphy, JJ-FAST', JJ_DATA), ('JICA, March 6, 2024', JICA)],
 ),
 dict(
    file='DLR_ZKI.html', title='DLR ZKI', hub='earth-observation',
    hub_file='Earth_Observation.html', anchor='Copernicus_EMS.html', hub_anchor='Copernicus_EMS.html',
    region='orbit', glass='earth', tint='space', klass='agency',
    img='assets/DLR_TerraSAR-X_Sendai.jpg', w=1500, h=844,
    alt='DLR TerraSAR-X radar view of Sendai port after the March 2011 tsunami, with water and damaged ground shown in color',
    credit='Image: DLR, CC BY 3.0. TerraSAR-X view of Sendai port after the 2011 tsunami.',
    credit_url='https://commons.wikimedia.org/wiki/File:Sendai_port_after_2011_tsunami_seen_by_TerraSAR-X.jpg',
    blurb="DLR's Center for Satellite Based Crisis Information turns satellite images into maps for disaster teams, from Oberpfaffenhofen.",
    label='Agency solution · active',
    eli=['ZKI is the crisis-mapping office of the German Aerospace Center.',
         'It turns satellite, airplane, or drone pictures into maps when a disaster hits.',
         'In the June 2013 floods, the first maps reached Germany\'s situation centre the next morning from a satellite image no more than 10 hours old.'],
    who=dict(text=['The Center for Satellite Based Crisis Information (ZKI) is part of the German Remote Sensing Data Center at the German Aerospace Center (DLR) in Oberpfaffenhofen. The office address is Münchener Straße 20, 82234 Wessling.'],
             sources=[('DLR, Center for Satellite Based Crisis Information', ZKI)]),
    what=dict(text=['ZKI studies satellite, aerial, or drone images and publishes the result as maps, geo-PDF files, web services, or written dossiers, before, during, or after a disaster, and also for planned major events and exercises.'],
              sources=[('DLR, Center for Satellite Based Crisis Information', ZKI)]),
    when=dict(text=['The service was established in 2004. Regular operations with the Federal Ministry of the Interior started on 22 January 2013. DLR said then that the service was on call around the clock and that the maps were free of charge.'],
              sources=[('DLR, on-call satellite data, January 22, 2013', ZKI_2013)]),
    where=dict(text=['The team works in Oberpfaffenhofen, and the maps are made for disasters in Germany and elsewhere. ZKI also works with the International Charter Space and Major Disasters.'],
               sources=[('DLR, Center for Satellite Based Crisis Information', ZKI), ('DLR ZKI, Germany floods, June 2013', ZKI_ACT)]),
    why=dict(text=['In the June 2013 floods, Germany\'s Joint Information and Situation Centre asked ZKI for maps. The first products arrived early on 4 June from a TerraSAR-X image taken no more than 10 hours earlier. DLR\'s 2013 announcement says maps like these show where the risks are, simplify logistics, and save time for rapid-response teams.'],
             sources=[('DLR ZKI, Germany floods, June 2013', ZKI_ACT), ('DLR, on-call satellite data, January 22, 2013', ZKI_2013)]),
    impact='A fresh satellite pass becomes a flood or damage map for civil-protection agencies within hours, so teams can see where the water is and send people and supplies there first.',
    impact_src=[('DLR ZKI, Germany floods, June 2013', ZKI_ACT), ('DLR, on-call satellite data, January 22, 2013', ZKI_2013)],
    people='In the June 2013 floods, the first maps reached Germany\'s situation centre the next morning from a TerraSAR-X image no more than 10 hours old, so teams could see the flood and route people and supplies while the water was still high.',
    people_src=('DLR ZKI, Germany floods, June 2013', ZKI_ACT),
    nature='The same kind of map marks flooded land, collapsed slopes, and damaged ground, so repair starts on the places the satellite shows were hit.',
    nature_src=('DLR, on-call satellite data, January 22, 2013', ZKI_2013),
    official=ZKI, button='Read the DLR page',
    ways='ZKI turns a fresh satellite pass into a flood or damage map for civil-protection agencies.',
    help='ZKI is part of DLR, a German public research center.',
    next=[('International Charter: Space and Major Disasters', 'International_Charter.html'),
          ('Copernicus Emergency Management Service: On-Demand Mapping', 'Copernicus_EMS.html'),
          ('GSMaP Global Rainfall Map (JAXA)', 'GSMaP.html')],
    sources=[('DLR, Center for Satellite Based Crisis Information', ZKI),
             ('DLR, on-call satellite data, January 22, 2013', ZKI_2013),
             ('DLR ZKI, Germany floods, June 2013', ZKI_ACT)],
 ),
]
for p in e.PAGES:
    p['every'] = e.EVERY
    p['showcase'] = e.SHOW
    p['nodeonate'] = e.NODON

def merge_i18n():
    existing = {lang: json.load(open(f'i18n/{lang}.json', encoding='utf8')) for lang in e.LANGS}
    shared = ['Donate', 'How we check a Donate link', 'Last reviewed:', 'November 2026',
              '2 sources cited', '3 sources cited', '4 sources cited', '5 sources cited',
              'Source:', 'Roll up your sleeves']
    for s in list(e.strings_needed()) + shared:
        if s not in e.TR and all(existing[lang].get(s) for lang in e.LANGS):
            e.TR[s] = {lang: existing[lang][s] for lang in e.LANGS}
    spec2 = importlib.util.spec_from_file_location('tr1124', os.path.join(ROOT, 'scripts', 'batch-1124-tr.py'))
    mod = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod)
    for en, tr in mod.EXTRA.items():
        e.TR.setdefault(en, {}).update(tr)
    # Combined paragraphs are one text node on the page, so they need their own key.
    nodon = e.NODON + ' ' + e.SHOW
    e.TR[nodon] = {lang: e.TR[e.NODON][lang] + ' ' + e.TR[e.SHOW][lang] for lang in e.LANGS}
    learn = {'fr': 'En savoir plus sur {x}', 'es': 'Más información sobre {x}', 'ar': 'تعرّف على {x}',
             'it': 'Scopri {x}', 'he': 'מידע על {x}'}
    for p in e.PAGES:
        both = p['help'] + ' ' + e.SHOW
        e.TR[both] = {lang: e.TR[p['help']][lang] + ' ' + e.TR[e.SHOW][lang] for lang in e.LANGS}
        title = e.TR.get(p['title'], {}).get('fr', p['title'])
        e.TR['Learn About ' + p['title']] = {lang: learn[lang].replace('{x}', e.TR.get(p['title'], {}).get(lang, p['title'])) for lang in e.LANGS}
        del title
    if 'Source' not in e.TR:
        e.TR['Source'] = {'fr': 'Source', 'es': 'Fuente', 'ar': 'المصدر', 'it': 'Fonte', 'he': 'מקור'}
    if 'Roll up your sleeves' not in e.TR:
        e.TR['Roll up your sleeves'] = {'fr': 'Retrousser ses manches', 'es': 'Arremángate', 'ar': 'شمّر عن ساعديك', 'it': 'Rimboccati le maniche', 'he': 'הפשילו שרוולים'}
    missing = e.strings_needed()
    if missing:
        print('MISSING', len(missing))
        for s in missing:
            print(' -', s[:180])
        raise SystemExit(1)
    for lang in e.LANGS:
        path = f'i18n/{lang}.json'
        data = json.load(open(path, encoding='utf8'))
        n = 0
        for en, tr in e.TR.items():
            if lang in tr and tr[lang] and data.get(en) != tr[lang]:
                data[en] = tr[lang]
                n += 1
        for p in e.PAGES:
            title = e.TR.get(p['title'], {}).get(lang, p['title'])
            en_apa = f'Saving Planets. (2026). {p["title"]}. https://www.savingplanets.com/{p["file"]}'
            data[en_apa] = f'Saving Planets. (2026). {title}. https://www.savingplanets.com/{lang}/{p["file"]}'
            en_mla = f'"{p["title"]}." Saving Planets, https://www.savingplanets.com/{p["file"]}.'
            q = f'« {title} »' if lang == 'fr' else f'"{title}"'
            data[en_mla] = f'{q}. Saving Planets{"،" if lang == "ar" else ","} https://www.savingplanets.com/{lang}/{p["file"]}.'
        text = json.dumps(data, ensure_ascii=False, indent=0) + '\n'
        open(path, 'w', encoding='utf8').write(text)
        print(lang, 'updated', n)

def fix_english():
    for p in e.PAGES:
        s = open(p['file'], encoding='utf8').read()
        hub = e.HUBNAME[p['hub']]['en']
        s = s.replace('"name": "Ocean", "item": "https://www.savingplanets.com/Oceans.html"',
                      f'"name": "{hub}", "item": "https://www.savingplanets.com/{p["hub_file"]}"')
        s = s.replace('"datePublished": "2026-11-09"', f'"datePublished": "{e.TODAY}"')
        s = s.replace('"dateModified": "2026-11-09"', f'"dateModified": "{e.TODAY}"')
        if 'Oceans.html' in s or 'monk seal' in s.lower():
            print('LEFTOVER', p['file'], 'oceans', s.count('Oceans.html'), 'monk', s.lower().count('monk seal'))
        if 'rel="preload" as="style"' not in s or 'crit-ns' not in s:
            raise SystemExit('preload missing ' + p['file'])
        open(p['file'], 'w', encoding='utf8').write(s)

def wire_home():
    """Append these three to the November 23 strip, pill, and changelog. 15 -> 18, 302 -> 305."""
    bumps = [
        ('15 new solutions', '18 new solutions'),
        ('15 nouvelles solutions', '18 nouvelles solutions'),
        ('15 soluciones nuevas', '18 soluciones nuevas'),
        ('أُضيفت 15 حلول', 'أُضيفت 18 حلول'),
        ('15 nuove soluzioni', '18 nuove soluzioni'),
        ('15 פתרונות', '18 פתרונות'),
    ]
    for lang in [None] + e.LANGS:
        pref = '' if lang is None else lang + '/'
        code = 'en' if lang is None else lang
        pre = '' if lang is None else '../'
        path = pref + 'index.html'
        s = open(path, encoding='utf8').read()
        s = re.sub(r'(?<![\d,])' + str(e.OLD_TOTAL) + r'(?!\d)', str(e.TOTAL), s)
        i = s.find('<!-- NEW-STRIP:START -->')
        j = s.find('<!-- NEW-STRIP:END -->')
        if i < 0 or j < 0:
            raise SystemExit('strip missing ' + path)
        block = s[i:j]
        for a, b in bumps:
            block = block.replace(a, b)
        def title(p, code=code):
            return p['title'] if code == 'en' else e.TR.get(p['title'], {}).get(code, p['title'])
        m = re.search(r'<time datetime="2026-11-23">([^<]+)</time>', block)
        date = m.group(1) if m else e.TODAY
        if f'href="{pre}Sentinel_Asia.html"' not in block:
            extra = ''.join(f'<li><time datetime="{e.TODAY}">{date}</time> <a href="{pre}{p["file"]}">{e.E(title(p))}</a></li>' for p in e.PAGES)
            block = block.replace('</ul>', extra + '</ul>', 1)
        s = s[:i] + block + s[j:]
        open(path, 'w', encoding='utf8').write(s)
        cpath = pref + 'Changelog.html'
        c = open(cpath, encoding='utf8').read()
        c = c.replace(' (15)</h3>', ' (18)</h3>', 1)
        if f'href="{pre}Sentinel_Asia.html"' not in c:
            lis = ''.join(f'<li><a href="{pre}{p["file"]}">{e.E(title(p))}</a></li>' for p in e.PAGES)
            k = c.find(f'datetime="{e.TODAY}">')
            ul = c.find('<ul>', k)
            c = c[:ul + 4] + lis + c[ul + 4:]
        open(cpath, 'w', encoding='utf8').write(c)
        spath = pref + 'Solutions.html'
        sol = open(spath, encoding='utf8').read()
        mark = '<!-- NEWSOL:END -->'
        if f'href="Sentinel_Asia.html"' not in sol[sol.find('NEWSOL:START'):sol.find(mark) + 20]:
            items = ''.join(f'<li style="margin:0"><a href="{p["file"]}" style="font-size:.92rem">{e.E(title(p))}</a></li>' for p in e.PAGES)
            sol = sol.replace('</ul></div><!-- NEWSOL:END -->', items + '</ul></div><!-- NEWSOL:END -->', 1)
            open(spath, 'w', encoding='utf8').write(sol)
        print('home', code)

def wire_data():
    added = json.load(open('assets/data/solution-added.json', encoding='utf8'))
    for p in e.PAGES:
        added[p['file']] = e.TODAY
    json.dump(added, open('assets/data/solution-added.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    s = open('assets/data/solutions.json', encoding='utf8').read()
    s = s.replace('  "solutions": 302,', '  "solutions": 305,', 1)
    s = s.replace('"taggedSolutions": 302', '"taggedSolutions": 305', 1)
    s = s.replace('   "agency": 130,', '   "agency": 133,', 1)
    s = s.replace('   "name": "Earth Observation",\n   "solutions": 50,', '   "name": "Earth Observation",\n   "solutions": 52,', 1)
    s = s.replace('   "name": "Forests",\n   "solutions": 43,', '   "name": "Forests",\n   "solutions": 44,', 1)
    s = s.replace('''  "forests": {
   "name": "Forests",
   "solutions": 44,''', '''  "forests": {
   "name": "Forests",
   "solutions": 44,''')
    # forests agency 3 -> 4, earth-observation agency 47 -> 49, using the following unique lines
    s = s.replace('''    "natural": 5,
    "government": 7,
    "agency": 3,''', '''    "natural": 5,
    "government": 7,
    "agency": 4,''', 1)
    s = s.replace('''   "byClassification": {
    "agency": 47,''', '''   "byClassification": {
    "agency": 49,''', 1)
    for p in e.PAGES:
        if '"href": "%s"' % p['file'] in s:
            continue
        needle = '    {\n     "href": "%s",' % p['anchor']
        ins = '    {\n     "href": "%s",\n     "name": "%s"\n    },\n    {\n     "href": "%s",' % (p['file'], p['title'].replace('"', ''), p['anchor'])
        if needle not in s:
            raise SystemExit('menu anchor missing ' + p['anchor'])
        s = s.replace(needle, ins, 1)
    objs = []
    for p in e.PAGES:
        if '"url": "%s"' % p['file'] in s:
            continue
        objs.append('''  {
   "url": "%s",
   "title": "%s",
   "category": "%s",
   "type": "solution",
   "classification": "%s",
   "status": "active",
   "stats": [],
   "missions": [],
   "added": "%s"
  }''' % (p['file'], p['title'], p['hub'], p['klass'], e.TODAY))
    if objs:
        end = '''   "url": "Solar_Dynamics_Observatory.html",
   "title": "Solar Dynamics Observatory",
   "category": "space-weather",
   "type": "solution",
   "classification": "agency",
   "status": "active",
   "stats": [],
   "missions": [],
   "added": "2026-11-23"
  }
 ]
}'''
        if end not in s:
            raise SystemExit('solutions.json tail changed')
        s = s.replace(end, end.replace('\n ]\n}', ',\n' + ',\n'.join(objs) + '\n ]\n}'), 1)
    json.loads(s)
    open('assets/data/solutions.json', 'w', encoding='utf8').write(s)
    for fn in ('i18n/pages.txt', 'i18n/he-pages.txt'):
        lines = open(fn, encoding='utf8').read().splitlines()
        for p in e.PAGES:
            if p['file'] not in lines:
                lines.append(p['file'])
        open(fn, 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    wh = open('assets/data/ways-to-help.json', encoding='utf8').read()
    jaxa_block = '''  "jaxa": [
   "JAXA",
   null,
   "https://global.jaxa.jp/about/employ/",
   "https://global.jaxa.jp/activity/pr/inquiries/"
  ],'''
    if '"jica"' not in wh:
        wh = wh.replace(jaxa_block, jaxa_block + '''
  "jica": [
   "JICA",
   null,
   "https://www.jica.go.jp/english/",
   "''' + JICA + '''"
  ],
  "dlr-zki": [
   "German Aerospace Center (DLR)",
   null,
   "''' + ZKI + '''",
   "''' + ZKI + '''"
  ],''', 1)
    if '"Sentinel_Asia"' not in wh:
        wh = wh.replace('  "SMOS": "esa"\n }',
                        '  "SMOS": "esa",\n  "Sentinel_Asia": "jaxa",\n  "JJ-FAST": "jica",\n  "DLR_ZKI": "dlr-zki"\n }', 1)
    json.loads(wh)
    open('assets/data/ways-to-help.json', 'w', encoding='utf8').write(wh)
    block_src = open('sitemap-en.xml', encoding='utf8').read()
    i = block_src.find('<url><loc>https://www.savingplanets.com/Lake_Washington_Cleanup.html</loc>')
    j = block_src.find('</url>', i) + len('</url>')
    sample = block_src[i:j]
    for lang, prefix in [('en', ''), ('fr', 'fr/'), ('es', 'es/'), ('ar', 'ar/'), ('it', 'it/'), ('he', 'he/')]:
        path = f'sitemap-{lang}.xml'
        sm = open(path, encoding='utf8').read()
        for p in e.PAGES:
            loc = f'https://www.savingplanets.com/{prefix}{p["file"]}'
            if f'<loc>{loc}</loc>' in sm:
                continue
            entry = sample.replace('Lake_Washington_Cleanup.html', p['file'])
            entry = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{e.TODAY}</lastmod>', entry, count=1)
            if lang != 'en':
                entry = entry.replace(f'<loc>https://www.savingplanets.com/{p["file"]}</loc>', f'<loc>{loc}</loc>', 1)
            sm = sm.replace('</urlset>', '  ' + entry + '\n</urlset>')
        open(path, 'w', encoding='utf8').write(sm)
    print('data wired')

def main():
    if '--strings' in sys.argv:
        for s in e.strings_needed():
            print(s)
        return
    merge_i18n()
    e.write_english()
    fix_english()
    e.translate()
    e.wire_listings()
    wire_home()
    wire_data()
    e.tooltips()
    print('done', e.TOTAL)

if __name__ == '__main__':
    main()
