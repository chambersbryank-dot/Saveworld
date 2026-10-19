#!/usr/bin/env python3
"""Oct 19 2026 batch (owner approved all 17, A-Q, Oct 19): Svalbard Global Seed Vault, International Thwaites Glacier
Collaboration, Carbfix, African Parks, Digital Earth Africa, Emirates Mars Mission (Hope), Abu Dhabi mangroves, Gaganyaan G1,
NEWater, Cheonggyecheon, Palau National Marine Sanctuary, Papahanaumokuakea, Predator Free 2050, Galapagos giant tortoises,
MAAP, Mesoamerican Reef insurance, Costa Rica PES. Same writer as batch-1018-content.py (Surfrider_Foundation.html skeleton,
Five W's, widgets after the Five W's, Connected Solutions, XLINK blocks on existing pages) plus a BLUF box (hook + one
sourced wow fact) right after the breadcrumb, styled by the BLUF1019 block in styles.css (written here, idempotent).
Shipped in small batches: SHIP below lists the slugs written so far (A-C, D-H, I-M, N-Q). Every fact is from the cited page
(fetched 2026-10-19); org/company/government figures are labeled as theirs. Re-runnable: overwrites only these pages,
their hub cards (added once) and the XLINK1019 blocks."""
import json, html, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
spec = importlib.util.spec_from_file_location('b18', os.path.join(ROOT, 'scripts/batch-1018-content.py'))
b18 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b18)
src, W, see_block = b18.b17.src, b18.W, b18.see_block
ADDED = '2026-10-19'
SHIP = ['Svalbard_Global_Seed_Vault', 'Thwaites_Glacier_Collaboration', 'Carbfix']

SV = ('https://www.seedvault.no/', 'Svalbard Global Seed Vault')
SVD = ('https://www.seedvault.no/2026/10/14/thousands-of-seeds-deposited-in-svalbard-as-global-cooperation-safeguards-food-security/', 'Svalbard Global Seed Vault, October 2026 deposit')
CROP = 'https://donate.croptrust.org/'
TGF = ('https://thwaitesglacier.org/about/facts', 'International Thwaites Glacier Collaboration, Facts')
TGR = ('https://thwaitesglacier.org/findings', 'International Thwaites Glacier Collaboration, Findings')
BAS = ('https://www.bas.ac.uk/project/international-thwaites-glacier-collaboration/', 'British Antarctic Survey, International Thwaites Glacier Collaboration')
CF = ('https://www.carbfix.com/our-story', 'Carbfix, Our story')
SCI = ('https://www.science.org/doi/10.1126/science.aad8132', 'Matter et al., Science (2016)')

PAGES = [
 dict(slug='Svalbard_Global_Seed_Vault', title='Svalbard Global Seed Vault', short='the Seed Vault', cat='polar',
  hub=('Polar.html', 'Polar'), cls='government', status='active', glass='earth', label='Government solution · active',
  img=('Svalbard_Nordaustlandet_Landsat9_2022.jpg', 1920, 2072, 'Glaciers, sea ice and dark Arctic water around Nordaustlandet, Svalbard, seen by Landsat 9'),
  credit='NASA Earth Observatory image by Joshua Stevens, using Landsat 9 data from the USGS (Nordaustlandet, Svalbard, July 29, 2022)',
  hook="Deep inside an Arctic mountain, the world keeps a spare copy of its crops.",
  wow=("The Seed Vault holds 1,417,799 seed samples of 6,587 species, sent by about 135 genebanks and institutions (Seed Vault figures).", SV),
  lead='The Svalbard Global Seed Vault stores backup copies of the world\'s crop seeds free of charge, more than 100 metres inside an Arctic mountain (Seed Vault).',
  eli=['Farmers and scientists keep seeds of thousands of crops in places called genebanks.',
       'The Seed Vault on Svalbard keeps a spare copy of those seeds deep inside a frozen mountain.',
       'If a genebank loses its seeds to war or disaster, it can take its copies back and grow them again.'],
  ws=[('Who', 'Norway, through its Ministry of Agriculture and Food, runs the vault with NordGen and the Crop Trust.', SV),
      ('What', 'A long-term backup store for duplicate seed samples from genebanks around the world, free of charge.', SV),
      ('When', 'Opened on Feb. 26, 2008. On Oct. 13, 2026, it received 16,676 samples from 21 institutions.', SVD),
      ('Where', 'More than 100 metres inside a mountain near Longyearbyen on Svalbard, Norway, in the Arctic.', SV),
      ('Why', 'Genebanks can lose seeds to war, disaster or failing equipment. The vault keeps a safe copy for them.', SV)],
  impact=('ICARDA became the first depositor to take seeds back out, to rebuild its genebank collection (Seed Vault).', SV),
  fact=('Ukraine\'s Seeds Are Safe', 'The October 2026 deposit included 773 samples from Ukraine\'s national genebank and 8,917 from CGIAR genebanks (Seed Vault).', SVD),
  people=('The vault is part of the global community\'s joint effort to ensure the world\'s future food supply (Seed Vault).', SV),
  nature=('Seeds of 6,587 species are stored there, so the diversity of the world\'s crops has a safe backup (Seed Vault figures).', SV),
  support_h='Support the Seed Vault', donate_alt='Donate to the Crop Trust',
  btns=[('Donate to the Crop Trust', CROP), ('Learn About the Seed Vault', SV[0])],
  bottom=('The Crop Trust, a partner of the vault, takes donations for crop diversity.', CROP, 'Donate'),
  widget=None, see=[('Biomass.html', 'Biomass Forest Mission (ESA)', 'Measures the forests that hold much of the planet\'s plant life.')],
  pin={'status': 'active', 'pins': [{'lat': 78.2357, 'lng': 15.4913, 'label': 'Svalbard Global Seed Vault, near Longyearbyen, Svalbard, Norway', 'basis': 'page'}]}),
 dict(slug='Thwaites_Glacier_Collaboration', title='International Thwaites Glacier Collaboration', short='the Thwaites Collaboration', cat='polar',
  hub=('Polar.html', 'Polar'), cls='agency', status='active', glass='earth', label='Agency solution · active',
  img=('Thwaites_Glacier_Landsat8_2019.jpg', 1920, 1467, 'The cracked ice front of Thwaites Glacier in West Antarctica meeting the sea, seen by Landsat 8'),
  credit='NASA Earth Observatory image by Lauren Dauphin, using Landsat 8 data from the USGS (Thwaites Glacier, Dec. 28, 2019)',
  hook="About 100 scientists spent years on the glacier that could change every coastline.",
  wow=("If Thwaites Glacier were lost completely, it would raise global sea level by 65 cm (ITGC).", TGF),
  lead='About 100 scientists from the UK, US, South Korea, Germany and Sweden are working out how fast Antarctica\'s Thwaites Glacier could raise sea levels (ITGC).',
  eli=['Thwaites is a giant glacier in Antarctica, the widest on Earth.',
       'It is melting and sliding into the sea, which makes the oceans rise a little.',
       'Scientists went there to find out how fast it could change, so coastal towns can plan.'],
  ws=[('Who', 'The UK\'s Natural Environment Research Council (NERC) and the US National Science Foundation (NSF), with about 100 scientists.', BAS),
      ('What', 'The largest UK-US Antarctic research collaboration in over 70 years, studying how Thwaites is changing and what could happen next.', BAS),
      ('When', 'From April 2018. The programme runs until Dec. 1, 2026 (British Antarctic Survey).', BAS),
      ('Where', 'Thwaites Glacier in West Antarctica, about 120 km wide, draining a basin of 192,000 square kilometres.', TGF),
      ('Why', 'Thwaites accounts for about 4% of global sea-level rise, a rate that has trebled since the mid-1990s (British Antarctic Survey).', BAS)],
  impact=('ITGC findings say Thwaites will keep retreating, further and faster, through the 21st and 22nd centuries; cutting emissions is the best hope of slowing it (ITGC).', TGR),
  fact=('50 Billion Tonnes a Year', 'Each year Thwaites loses about 50 billion tonnes more ice than it gains from snowfall (ITGC).', TGF),
  people=('Understanding the glacier\'s future is critical for planning and adapting to climate change, including on the world\'s coasts (British Antarctic Survey).', BAS),
  nature=('Understanding Thwaites shows how Antarctic ice, the ocean beneath it and the climate are linked (ITGC).', TGF),
  support_h='Learn More About Thwaites',
  btns=[('Read the Findings', TGR[0]), ('Thwaites Facts', TGF[0])],
  bottom=('Want to go deeper? The collaboration shares its findings in plain language.', TGR[0], 'For Further Information'),
  widget=W('International Thwaites Glacier Collaboration', 'Research programme from April 2018 to Dec. 1, 2026, funded by NERC and NSF (British Antarctic Survey).', BAS, 'British Antarctic Survey',
           arrival='2026-12-01T00:00:00Z', arrival_label='programme end, Dec. 1, 2026',
           milestones=[('2018-04-01', 'Programme begins'), ('2026-12-01', 'Programme ends')]),
  see=[('CryoSat.html', 'CryoSat Ice Mission (ESA)', 'Measures how the polar ice sheets are changing from orbit.')],
  pin={'status': 'active', 'pins': [{'lat': -75.5, 'lng': -106.75, 'label': 'Thwaites Glacier, West Antarctica', 'basis': 'page'}]}),
 dict(slug='Carbfix', title='Carbfix: Turning CO2 Into Stone', short='Carbfix', cat='polar',
  hub=('Polar.html', 'Polar'), cls='corporate', status='active', glass='earth', label='Company solution · active',
  img=('Iceland_Volcanic_Landscape_jsc2026e406058.jpg', 1920, 1144, 'Two people crossing a dark volcanic lava plain in Iceland'),
  credit='NASA/James Blair (jsc2026e406058, volcanic landscape in Iceland)',
  hook="In Iceland, carbon dioxide is being turned into rock.",
  wow=("In a 2012 test, over 95% of the injected CO2 turned to stone in less than two years (Science, 2016).", SCI),
  lead='Carbfix dissolves carbon dioxide in water and injects it into basalt rock, where it turns into stone (company).',
  eli=['Carbon dioxide is a gas that warms the planet.',
       'Carbfix mixes it with water, like fizzy water, and pumps it deep into volcanic rock.',
       'There the gas reacts with the rock and becomes solid stone that stays put.'],
  ws=[('Who', 'Carbfix, a subsidiary of Reykjavík Energy (OR) that began operating as its own company on Jan. 1, 2020. It began as a project of Reykjavík Energy, the University of Iceland, CNRS and Columbia University\'s Earth Institute.', CF),
      ('What', 'CO2 is dissolved in water and injected underground, where it reacts with basalt and turns into carbonate minerals.', CF),
      ('When', 'Started in 2006 and formalized in 2007. Injection at industrial scale at Hellisheiði has run since 2014.', CF),
      ('Where', 'At the Hellisheiði geothermal power plant in Iceland, in basalt rock.', CF),
      ('Why', 'Rock storage keeps CO2 out of the atmosphere for good. The company\'s goal is to store 1 billion tonnes of CO2.', CF)],
  impact=('In the 2012 pilot, 175 tonnes of CO2 were injected at about 500 m depth, and over 95% mineralized in less than two years (Science, 2016).', SCI),
  fact=('About $25 a Tonne', 'Carbfix puts its on-site cost at about US $24.8 per tonne of CO2 (company figure).', CF),
  people=('At Hellisheiði, CO2 and hydrogen sulphide are captured from a geothermal power plant\'s emissions and stored as rock (Carbfix).', CF),
  nature=('Carbfix copies a natural process: CO2 and rock form stable carbonate minerals, a permanent and environmentally benign store (Carbfix).', CF),
  support_h='Learn More About Carbfix',
  btns=[('Carbfix\'s Story', CF[0]), ('Read the Science Study', SCI[0])],
  bottom=('Want to go deeper? Carbfix explains how CO2 turns to stone.', CF[0], 'For Further Information'),
  widget=None, see=[],
  pin={'status': 'active', 'pins': [{'lat': 64.037, 'lng': -21.40, 'label': 'Hellisheiði geothermal power plant, Iceland', 'basis': 'page'}]}),
]

# Existing pages that link back (idempotent XLINK1019 block). Only entries whose new page is in SHIP are written.
XBACK = {
 'CryoSat.html': [('Thwaites_Glacier_Collaboration.html', 'International Thwaites Glacier Collaboration', 'About 100 scientists studying how fast Thwaites could raise sea levels.')],
}

CSS = '''/* BLUF1019:START (generated by scripts/batch-1019-content.py) */
body.toc-sub .sol-bluf-box{margin:1rem auto .5rem;max-width:960px;padding:0 1rem}
body.toc-sub .sol-bluf-box .impact-box{max-width:880px;margin:0 auto;padding:1.1rem 1.4rem}
body.toc-sub .sol-bluf-box .impact-box p{margin:0 0 .55rem;line-height:1.5}
body.toc-sub .sol-bluf-box .bluf-hook{font-size:clamp(1.15rem,2vw,1.4rem);line-height:1.3}
body.toc-sub .sol-bluf-box .bluf-wow{font-size:1.05rem}
body.toc-sub .sol-bluf-box .impact-box p.fact-source{margin:0;font-size:.85rem}
@media (max-width:600px){body.toc-sub .sol-bluf-box .impact-box{padding:.9rem 1rem}}
/* BLUF1019:END */'''

def bluf(p):
    t, c = p['wow']
    return (f'<section class="impact sol-bluf-box" id="bluf" aria-label="The bottom line"><div class="impact-box">'
            f'<p class="bluf-hook"><strong>{E(p["hook"])}</strong></p><p class="bluf-wow">{E(t)}</p>{src(*c)}</div></section>')

def body(p):
    b, srcs = b18.body(p)
    b = b.replace('<!-- REVIEWED:START --><!-- REVIEWED:END -->', '<!-- REVIEWED:START --><!-- REVIEWED:END -->\n' + bluf(p), 1)
    return b, sorted(set(srcs) | {p['wow'][1][0]})

def main():
    pages = [p for p in PAGES if p['slug'] in SHIP]
    tpl = open(os.path.join(ROOT, 'Surfrider_Foundation.html'), encoding='utf8').read()
    eli = json.load(open(os.path.join(ROOT, 'assets/data/eli10.json'), encoding='utf8'))
    ml = json.load(open(os.path.join(ROOT, 'assets/data/map-locations.json'), encoding='utf8'))
    for p in pages:
        s = p['slug']; im = p['img'][0]
        out = tpl.replace('Surfrider_Foundation', s)
        b, srcs = body(p)
        out = re.sub(r'<main id="main">.*?</main>', lambda m: b, out, count=1, flags=re.S)
        desc = E(p['lead'], quote=True)
        out = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m.group(1) + desc, out)
        out = re.sub(r'<title>[^<]*</title>', f'<title>{E(p["title"])} | Saving Planets</title>', out)
        out = re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*', lambda m: m.group(1) + E(p['title']) + ' | Saving Planets', out)
        out = re.sub(r'(<meta (?:property|name)="(?:og:image|twitter:image)" content=")[^"]*', lambda m: m.group(1) + 'https://www.savingplanets.com/assets/' + im, out)
        out = re.sub(r'(sp:category" content=")[^"]*', lambda m: m.group(1) + p['cat'], out)
        out = re.sub(r'(sp:classification" content=")[^"]*', lambda m: m.group(1) + p['cls'], out)
        out = re.sub(r'(sp:status" content=")[^"]*', lambda m: m.group(1) + p['status'], out)
        out = re.sub(r'(sp:added" content=")[^"]*', lambda m: m.group(1) + ADDED, out)
        sl = s.lower().replace('_', '-')
        out = re.sub(r'<body[^>]*>', f'<body data-glass="{p["glass"]}" class="hp-{sl} toc-sub {sl}-page">', out, count=1)
        out = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', out, flags=re.S)
        out = re.sub(r'<!-- (TEACHER|CITE|SHARE):START -->.*?<!-- \1:END -->\n?', '', out, flags=re.S)
        out = out.replace('Surfrider Foundation', p['title']).replace('Surfrider', p['short'])
        open(os.path.join(ROOT, s + '.html'), 'w', encoding='utf8').write(out)
        eli[s + '.html'] = p['eli']
        pin = dict(p['pin'])
        if pin.get('strip') is None: pin.pop('strip', None)
        ml['solutions'][s + '.html'] = pin
    ICON = {'Polar.html': '🧊', 'Earth_Observation.html': '🌍', 'Oceans.html': '🌊', 'Deforestation.html': '🌳', 'Rivers.html': '💧', 'Space.html': '🛰️'}
    for p in pages:
        hf, hn = p['hub']; s = p['slug']; im, w, h, alt = p['img']
        fp = os.path.join(ROOT, hf); t = open(fp, encoding='utf8').read()
        if f'class="photo-link" href="{s}.html"' in t: continue
        card = (f'<article class="card"><div class="image-container"><a class="photo-link" href="{s}.html"><img src="assets/{im}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a></div>'
                f'<p class="sol-badges"><span class="status-badge status-active">Active</span><span class="hub-tag"><span aria-hidden="true">{ICON[hf]}</span> {hn}</span></p>'
                f'<h3><a href="{s}.html">{E(p["title"])}</a></h3><p class="card-blurb">{E(p["lead"])}</p></article>')
        i = t.find('id="missions"'); j = t.find('</div></section>', i)
        k = t.rfind('</article>', i, j) + len('</article>')
        t = t[:k] + card + t[k:]
        open(fp, 'w', encoding='utf8').write(t)
    for f, items in XBACK.items():
        items = [x for x in items if x[0][:-5] in SHIP]
        if not items: continue
        fp = os.path.join(ROOT, f); t = open(fp, encoding='utf8').read()
        blk = '<!-- XLINK1019:START -->' + see_block(items, 'connected-1019') + '<!-- XLINK1019:END -->'
        if '<!-- XLINK1019:START -->' in t:
            t = re.sub(r'<!-- XLINK1019:START -->.*?<!-- XLINK1019:END -->', lambda m: blk, t, flags=re.S)
        else:
            i = t.find('<section class="page-stats"')
            if i < 0: i = t.find('<section class="donate-banner')
            t = t[:i] + blk + '\n' + t[i:]
        open(fp, 'w', encoding='utf8').write(t)
    cp = os.path.join(ROOT, 'styles.css'); css = open(cp, encoding='utf8').read()
    css2 = re.sub(r'/\* BLUF1019:START.*?BLUF1019:END \*/', lambda m: CSS, css, flags=re.S) if 'BLUF1019:START' in css else css.rstrip('\n') + '\n' + CSS + '\n'
    if css2 != css: open(cp, 'w', encoding='utf8').write(css2)
    json.dump(eli, open(os.path.join(ROOT, 'assets/data/eli10.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump(ml, open(os.path.join(ROOT, 'assets/data/map-locations.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('wrote', len(pages), 'pages')

if __name__ == '__main__':
    main()
