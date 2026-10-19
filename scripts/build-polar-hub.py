#!/usr/bin/env python3
"""Oct 18 2026 (owner-approved 11:57 AM HST): POLAR hub (Antarctica, the Arctic, Greenland, Iceland), hub 11. Idempotent.
Builds Polar.html from the Lakes.html hub template (head + chrome; <main> replaced), with cards for the ice/polar pages.
Primary members (breadcrumb + sp:category polar): CryoSat, CRISTAL, CIMR, ICESat-2, PREFIRE. Cross-listed (primary hub unchanged): RCM.
Earth Observation keeps its cards for all of them, so Solutions.html shows 'Also in' instead of duplicates; hub sums stay exact.
Facts are the member pages' own sourced facts (ESA / NASA / NASA JPL / CSA). CIMR + CRISTAL hubs are set in batch-1018-content.py."""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
E = lambda s, quote=False: html.escape(s, quote=quote)
HUB = 'Polar.html'; NAME = 'Polar'; ICON = '🧊'
PRIMARY = ['CryoSat', 'CRISTAL', 'CIMR', 'ICESat-2', 'PREFIRE']
CROSS = ['RCM']
IMG = 'Greenland_IceBridge_2015.jpg'; CREDIT = 'NASA GSFC, Operation IceBridge (2015)'
DESC = 'Satellites that watch the ice of Antarctica, the Arctic, Greenland and Iceland, from sea-ice thickness to hidden lakes under the ice sheets.'
TITLE = 'Polar Solutions: Watching the Ice of Antarctica, the Arctic, Greenland and Iceland'
def src(url, label, kind='Source'):
    return f'<p class="fact-source">{kind}: <a href="{url}" target="_blank" rel="noreferrer">{label}</a></p>'
S_LAKES = ('https://www.esa.int/Applications/Observing_the_Earth/FutureEO/CryoSat/85_new_subglacial_lakes_detected_below_Antarctica', 'ESA, 85 new subglacial lakes detected below Antarctica')
S_CIMR = ('https://www.esa.int/Applications/Observing_the_Earth/Copernicus/CIMR/CIMR_facts_and_figures', 'ESA, CIMR facts and figures')
S_PREF = ('https://www.jpl.nasa.gov/news/nasas-prefire-cubesat-mission-extended/', 'NASA JPL, PREFIRE mission extended')
S_IS2 = ('https://icesat-2.gsfc.nasa.gov/', 'NASA, ICESat-2')
S_CRI = ('https://www.esa.int/Applications/Observing_the_Earth/Copernicus/CRISTAL_prepares_to_sparkle', 'ESA, CRISTAL prepares to sparkle')
IMPACT = ('<section class="impact" id="impact"><h2>Impact Statement</h2><div class="impact-box">'
    '<p>A decade of CryoSat data revealed 85 unknown lakes under Antarctica, raising the known active subglacial lakes by more than half, to 231 (ESA).</p>' + src(*S_LAKES) +
    '<p>CIMR will measure 95% of the globe every day, with sub-daily coverage of the polar regions (ESA).</p>' + src(*S_CIMR) +
    '<p>Heat absorbed in the tropics flows to the poles and escapes to space there. PREFIRE measures that far-infrared heat (NASA JPL).</p>' + src(*S_PREF) +
    '</div></section>')
WS = ('<section class="five-ws" id="solution"><h2>The Five W\'s of Polar Solutions</h2><div class="ws-grid">'
    '<div class="w-card"><h3>Who</h3><p>The European Space Agency (ESA), NASA and the Canadian Space Agency, with their partners.</p></div>'
    '<div class="w-card"><h3>What</h3><p>Satellites that measure polar ice from space: sea-ice thickness, the height of ice sheets and glaciers, lakes hidden under the ice, and the heat the poles send to space.</p></div>'
    '<div class="w-card"><h3>When</h3><p>Now and next: ICESat-2 has measured ice since its launch on September 15, 2018 (NASA), and CRISTAL will continue CryoSat\'s ice record (ESA).</p>' + src(*S_IS2) + src(*S_CRI) + '</div>'
    '<div class="w-card"><h3>Where</h3><p>The polar regions, including Antarctica, the Arctic Ocean, Greenland and Iceland, seen from satellites in polar orbits.</p></div>'
    '<div class="w-card"><h3>Why</h3><p>Lakes under the ice affect how fast glaciers move and so influence global sea level rise (ESA). Daily sea-ice data also support safer work and travel in polar seas (ESA).</p>' + src(*S_LAKES) + src(*S_CIMR) + '</div>'
    '</div></section>')

def card_from_eo(slug, eo):
    m = re.search(r'<article class="card">(?:(?!</article>).)*?href="' + re.escape(slug) + r'\.html".*?</article>', eo, re.S)
    if not m: raise SystemExit(f'polar: no Earth Observation card for {slug}')
    c = m.group(0)
    return re.sub(r'<span class="hub-tag">(?:<span aria-hidden="true">[^<]*</span>)?[^<]*</span>', f'<span class="hub-tag"><span aria-hidden="true">{ICON}</span> {NAME}</span>', c, count=1)

def main():
    eo = open('Earth_Observation.html', encoding='utf8').read()
    cards = ''.join(card_from_eo(s, eo) for s in PRIMARY + CROSS)
    tpl = open('Lakes.html', encoding='utf8').read()
    m = re.search(r'<main id="main">.*?</main>', tpl, re.S)
    lm = m.group(0)
    bottom = re.search(r'<section class="donate-banner bottom-link".*?</section>', lm, re.S).group(0)
    bottom = re.sub(r'<p>.*?</p>', '<p>Want to go deeper? ESA tracks the polar ice from space.</p>', bottom, count=1)
    bottom = re.sub(r'href="[^"]*"', 'href="https://www.esa.int/Applications/Observing_the_Earth/FutureEO/CryoSat"', bottom, count=1)
    bottom = re.sub(r'<img[^>]*>', f'<img src="assets/{IMG}" alt="Ice sheet in northeast Greenland seen from a NASA Operation IceBridge flight" width="400" height="400" loading="lazy" decoding="async">', bottom, count=1)
    nxt = ('<section class="next-solutions" aria-label="Explore another hub"><h2>Next: Explore Another Hub</h2><ul>'
           '<li><a href="Earth_Observation.html">Earth Observation</a></li><li><a href="Oceans.html">Ocean</a></li>'
           '<li><a href="Lakes.html">Lakes</a></li><li><a href="Solutions.html">All Solutions</a></li></ul></section>')
    main_html = ('<main id="main">\n'
        f'<section class="page-hero hub-hero"><div class="page-hero-content"><h1>{NAME}</h1></div><span class="hero-credit">{CREDIT}</span></section>\n'
        + IMPACT + '\n' + WS + '\n'
        f'<section class="card-band hub-cards" id="missions"><h2>Missions and Solutions</h2><div class="grid">{cards}</div></section>\n'
        '<section class="page-stats" data-stats-category="polar" data-stats-page="Polar.html" aria-label="Solution stats" hidden></section>\n'
        + bottom + '\n' + nxt + '\n</main>')
    head, body = tpl.split('<body', 1)
    head = head.replace('Lakes.html', HUB)
    head = re.sub(r'<title>[^<]*</title>', f'<title>{E(TITLE)}</title>', head)
    head = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m.group(1) + E(DESC, True), head)
    head = re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*', lambda m: m.group(1) + E(TITLE, True), head)
    head = re.sub(r'(<meta (?:property|name)="(?:og:image|twitter:image)" content=")[^"]*', lambda m: m.group(1) + 'https://www.savingplanets.com/assets/' + IMG, head)
    head = re.sub(r'(sp:category" content=")[^"]*', r'\1polar', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    body = '<body' + body
    body = re.sub(r'<body[^>]*>', '<body data-glass="earth" class="hp-polar toc-sub" data-glass-tint="water">', body, count=1)
    body = body.replace(lm, main_html)
    body = re.sub(r'<!-- (QUIZ|SHARE|TEACHER|CITE):START -->.*?<!-- \1:END -->\n?', '', body, flags=re.S)
    open(HUB, 'w', encoding='utf8').write(head + body)
    # primary members: breadcrumb hub + sp:category
    for s in PRIMARY:
        f = s + '.html'; t = open(f, encoding='utf8').read(); o = t
        t = re.sub(r'(sp:category" content=")[^"]*', r'\1polar', t, count=1)
        t = re.sub(r'(<nav aria-label="Breadcrumb"[^>]*>.*?<li><a href=")Earth_Observation\.html(">)Earth Observation(</a>)', r'\g<1>Polar.html\g<2>Polar\g<3>', t, count=1, flags=re.S)
        if t != o: open(f, 'w', encoding='utf8').write(t)
    print(f'polar: {HUB} with {len(PRIMARY)} primary + {len(CROSS)} cross-listed cards')

if __name__ == '__main__':
    main()
