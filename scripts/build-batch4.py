#!/usr/bin/env python3
"""Batch 4: 'Do one thing today' box (index + hubs, DOT marker block, rendered from assets/data/daily-actions.json),
Community.html (reader photo wall; items from assets/data/community.json, rendered by site.js),
Find_a_Cleanup.html (official event finders by region), nav/footer/Ways to Help links, sitemap. Idempotent; runs in weekly-sync.sh."""
import re, html, json, os, importlib.util
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
E = html.escape
spec = importlib.util.spec_from_file_location('c', 'scripts/batch3-content.py'); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
TPL = open('Press.html', encoding='utf8').read()
FOOT = TPL[TPL.index('<footer>'):]
EXT = ' target="_blank" rel="noopener"'

def page(slug, title, h1, sub, desc, body):
    head = TPL[:TPL.index('<section class="page-hero')]
    head = head.replace('Press and media kit for Saving Planets: logo downloads, mission, boilerplate, contact and fact sheets. Everything you need to write about Saving Planets.', E(desc, quote=True))
    head = head.replace('Press and Media | Saving Planets', E(title)).replace('"Press and Media"', json.dumps(h1)).replace('Press.html', slug + '.html')
    head = re.sub(r'"name": "Press and Media"', '"name": ' + json.dumps(h1), head)
    crumbs = f'<nav aria-label="Breadcrumb" class="breadcrumb"><ol><li><a href="index.html">Home</a></li><li><span aria-current="page">{E(h1)}</span></li></ol></nav>'
    hero = f'<section class="page-hero"><div class="page-hero-content"><h1>{E(h1)}</h1><p>{E(sub)}</p></div></section>\n'
    mid = hero + crumbs + '\n' + body + '\n'
    f = slug + '.html'
    if os.path.exists(f):
        cur = open(f, encoding='utf8').read(); a = cur.index('<section class="page-hero'); b = cur.index('<footer>')
        if cur[a:b] == mid: print('unchanged', slug); return
        open(f, 'w', encoding='utf8').write(cur[:a] + mid + cur[b:]); print('updated', slug); return
    open(f, 'w', encoding='utf8').write(head + mid + FOOT); print('wrote', slug)

# ---- Do one thing today
D = json.load(open('assets/data/daily-actions.json', encoding='utf8'))
items = []
for i, a in enumerate(D['actions']):
    ext = EXT if a['url'].startswith('http') else ''
    items.append(f'<li class="dot-item" data-i="{i}"{"" if i == 0 else " hidden"}><p class="dot-text">{E(a["text"])}</p>'
                 f'<p class="dot-link"><a class="btn" href="{E(a["url"])}"{ext}>Do it with {E(a["org"])}</a></p></li>')
DOT = ('<!-- DOT:START --><section class="dot" id="do-one-thing" aria-labelledby="dot-h" data-start="' + D['start'] + '"><div class="dot-card">'
       '<p class="dot-kicker">Today&#x27;s small step</p><h2 id="dot-h">Do One Thing Today</h2>'
       '<ol class="dot-list" role="list">' + ''.join(items) + '</ol>'
       '<p class="dot-foot">A new action every day, each from an official source. <a href="Find_a_Cleanup.html">Find a cleanup near you</a> · <a href="Ways_to_Help.html">Ways to Help</a></p>'
       '</div></section><!-- DOT:END -->')
def put(f, block, tag, before):
    s = open(f, encoding='utf8').read()
    s = re.sub(r'<!-- ' + tag + r':START -->.*?<!-- ' + tag + r':END -->\n?', '', s, flags=re.S)
    for b in before:
        if b in s:
            i = s.index(b); s = s[:i] + block + '\n' + s[i:]; break
    else: raise SystemExit(f'no anchor in {f}')
    open(f, 'w', encoding='utf8').write(s)
# Oct 14: "Do One Thing Today" disabled (revive later by setting DOT_ENABLED = True; data kept in daily-actions.json).
DOT_ENABLED = False
def strip(f, tag):
    s = open(f, encoding='utf8').read()
    n = re.sub(r'<!-- ' + tag + r':START -->.*?<!-- ' + tag + r':END -->\n?', '', s, flags=re.S)
    if n != s: open(f, 'w', encoding='utf8').write(n)
if DOT_ENABLED:
    put('index.html', DOT, 'DOT', ['<section id="actions">'])
    for hub in C.QUIZZES: put(hub + '.html', DOT, 'DOT', ['<!-- QUIZ:START -->'])
else:
    import glob
    for f in glob.glob('*.html') + glob.glob('fr/*.html') + glob.glob('es/*.html') + glob.glob('ar/*.html'): strip(f, 'DOT')
print('dot enabled' if DOT_ENABLED else 'dot DISABLED', 'dot: index +', len(C.QUIZZES), 'hubs,', len(items), 'actions')

# ---- Community.html
MAIL = 'mailto:ideas@savingplanets.com?subject=Community%20photo&amp;body=First%20name%20or%20alias%3A%0APlace%20(city%20or%20beach)%3A%0AWhat%20happened%3A%0A%0AI%20took%20this%20photo%2C%20I%20agree%20to%20the%20guidelines%2C%20and%20Saving%20Planets%20may%20publish%20it.'
G = ['Send photos you took yourself. Please don&#x27;t send photos from the internet or someone else&#x27;s camera.',
     'Use your first name or an alias only. We never publish last names, emails or addresses.',
     'No faces of children or teens. Hands, gear, bags of trash and the beach are perfect.',
     'Tell us where and when (city or beach is enough) and what you did.',
     'By sending, you agree that Saving Planets may publish your photo, name or alias and caption on this site and our social accounts. Ask us any time and we&#x27;ll take it down.',
     'We read every email, but we may decline a photo or edit a caption for length or clarity.']
body = ('<section class="impact" id="intro"><h2>Show Us Your Cleanup</h2><div class="impact-box"><p>Picked up trash on a beach, planted a tree, or joined a citizen-science project? Send us a photo and we may feature it here, so others can see real people doing the work.</p>'
        '<p><a class="btn" href="' + MAIL + '">Email your photo</a></p><p class="comm-addr">Email <a href="' + MAIL + '">ideas@savingplanets.com</a> with the subject <strong>Community photo</strong>.</p></div></section>\n'
        '<section class="five-ws" id="guidelines"><h2>Guidelines</h2><ul class="comm-rules">' + ''.join(f'<li>{g}</li>' for g in G) + '</ul></section>\n'
        '<section class="comm-wall" id="wall" aria-labelledby="wall-h"><h2 id="wall-h">Community Wall</h2><div class="comm-grid" data-community="assets/data/community.json"></div>'
        '<div class="comm-empty"><p class="comm-empty-icon" aria-hidden="true">🌍</p><h3>Be the first</h3><p>No photos yet. Yours could be the first one on the wall.</p><p><a class="btn" href="' + MAIL + '">Send a photo</a> <a class="btn help-btn" href="Find_a_Cleanup.html">Find a cleanup</a></p></div></section>')
page('Community', 'Community Wall: Reader Cleanup Photos | Saving Planets', 'Community Wall', 'Real people, real cleanups. Send us yours.',
     'Send Saving Planets a photo of your cleanup, tree planting or citizen-science project. Guidelines, consent, and the community wall.', body)

# ---- Find_a_Cleanup.html
R = [('Worldwide', [
        ('Ocean Conservancy: International Coastal Cleanup map', 'https://oceanconservancy.org/work/plastics/cleanups-icc/map/', 'Find cleanups near coasts and waterways around the world.'),
        ('Clean Swell app (Ocean Conservancy)', 'https://oceanconservancy.org/work/plastics/cleanups-icc/clean-swell-app/', 'Free app to join cleanups and log what you collect.'),
        ('World Cleanup Day', 'https://www.worldcleanupday.org/', 'A yearly global cleanup day with events in many countries.'),
        ('Marine Debris Tracker', 'https://debristracker.org/', 'Log litter you pick up anywhere and add it to open data.')]),
     ('United States', [
        ('Surfrider Foundation beach cleanups', 'https://cleanups.surfrider.org/', 'Beach cleanups run by local Surfrider chapters.'),
        ('Keep America Beautiful: Great American Cleanup', 'https://kab.org/our-signature-programs/great-american-cleanup/', 'Community cleanups across the country, mostly in spring.'),
        ('California Coastal Cleanup Day', 'https://www.coastal.ca.gov/publiced/ccd/ccd.html', 'California Coastal Commission cleanup sites along the state&#x27;s coast and inland waterways.'),
        ('NOAA Marine Debris Program', 'https://marinedebris.noaa.gov/our-work/prevention', 'Learn how debris starts and how to prevent it.')]),
     ('Great Lakes', [
        ('Alliance for the Great Lakes: Adopt-a-Beach', 'https://greatlakes.org/adopt-a-beach/', 'Join or lead cleanups on Great Lakes beaches.'),
        ('Great Lakes Plastic Cleanup', 'https://greatlakesplasticcleanup.org/get-involved/', 'Ways to help capture plastic in Great Lakes marinas.')]),
     ('United Kingdom', [
        ('Marine Conservation Society: beach cleans', 'https://www.mcsuk.org/what-you-can-do/beach-clean/', 'Find or organize a beach clean around the UK.')]),
     ('Australia', [
        ('Clean Up Australia', 'https://www.cleanup.org.au/', 'Join or register a cleanup anywhere in Australia.')])]
secs = []
for reg, links in R:
    li = ''.join(f'<li><a href="{u}"{EXT}>{n}</a><span class="fc-desc">{d}</span></li>' for n, u, d in links)
    secs.append(f'<div class="fc-region"><h3>{reg}</h3><ul class="fc-list">{li}</ul></div>')
body = ('<section class="impact" id="intro"><h2>How This Works</h2><div class="impact-box"><p>We don&#x27;t run cleanups or keep our own list of events. Instead, we link to official event finders run by the organizations that do. Pick your region, open the finder, and look for an event near you.</p></div></section>\n'
        '<section class="fc-regions" id="regions" aria-label="Cleanup finders by region">' + ''.join(secs) + '</section>\n'
        '<section class="five-ws" id="none-near"><h2>No Event Near You?</h2><p>Start your own small cleanup with <a href="https://oceanconservancy.org/work/plastics/cleanups-icc/start-a-cleanup/"' + EXT + '>Ocean Conservancy&#x27;s free guide</a>, and log what you find in the <a href="https://oceanconservancy.org/work/plastics/cleanups-icc/clean-swell-app/"' + EXT + '>Clean Swell app</a>.</p></section>\n'
        '<section class="five-ws" id="safety"><h2>Stay Safe</h2><ul class="comm-rules"><li>Wear gloves and closed shoes.</li><li>Don&#x27;t pick up needles, sharp metal or broken glass by hand. Tell the organizer.</li><li>Kids should always clean up with an adult.</li><li>Watch the tide, the sun and the weather.</li></ul></section>\n'
        '<section class="help-actions" id="share"><h2>Share Your Cleanup</h2><p>Send us a photo for the Community Wall, or find more ways to give and volunteer.</p><p><a class="btn" href="Community.html">Community Wall</a> <a class="btn help-btn" href="Ways_to_Help.html">Ways to Help</a></p></section>')
page('Find_a_Cleanup', 'Find a Cleanup Near You | Saving Planets', 'Find a Cleanup', 'Official cleanup event finders, sorted by region.',
     'Find a beach, river or lake cleanup near you. Links to official event finders from Ocean Conservancy, Surfrider, Keep America Beautiful, Alliance for the Great Lakes and more.', body)

# ---- Ways to Help link
WB = ('<!-- B4-WTH:START --><section class="help-actions" id="cleanups"><h2>Join a Cleanup</h2><p>Want to help with your own hands? Find an official cleanup near you, then send us a photo for the Community Wall.</p>'
      '<p><a class="btn" href="Find_a_Cleanup.html">Find a Cleanup</a> <a class="btn help-btn" href="Community.html">Community Wall</a></p></section><!-- B4-WTH:END -->')
put('Ways_to_Help.html', WB, 'B4-WTH', ['<section class="help-actions">'])

# ---- Footer + nav (English pages; translations regenerate)
OLDF = '<a href="Rawanes_Mission_Log.html">Rawane&#x27;s Mission Log</a></p>'
NEWF = '<a href="Rawanes_Mission_Log.html">Rawane&#x27;s Mission Log</a><span aria-hidden="true"> · </span><a href="Community.html">Community Wall</a><span aria-hidden="true"> · </span><a href="Find_a_Cleanup.html">Find a Cleanup</a></p>'
NAVC = '<li><a href="Community.html">Community</a></li>'
NAVO = '<li><a href="Search.html">Search</a></li>'
NAVN = NAVC + NAVO
nf = nn = 0
for f in sorted(os.listdir('.')):
    if not f.endswith('.html'): continue
    s = open(f, encoding='utf8').read(); o = s
    if NEWF not in s and OLDF in s: s = s.replace(OLDF, NEWF); nf += 1
    if NAVN not in s and NAVO in s and 'class="nav-links"' in s: s = s.replace(NAVC, '').replace(NAVO, NAVN, 1); nn += 1
    if s != o: open(f, 'w', encoding='utf8').write(s)
print('footers:', nf, 'nav:', nn)

# ---- sitemap, pages.txt, build-stats SKIP
sm = open('sitemap.xml', encoding='utf8').read()
for p in ('Community.html', 'Find_a_Cleanup.html'):
    loc = f'<loc>https://www.savingplanets.com/{p}</loc>'
    if loc not in sm:
        anchor = sm.index('<url><loc>https://www.savingplanets.com/Ways_to_Help.html</loc>')
        sm = sm[:anchor] + f'<url>{loc}<lastmod>2026-10-11</lastmod></url>\n  ' + sm[anchor:]
open('sitemap.xml', 'w', encoding='utf8').write(sm)
pt = open('i18n/pages.txt', encoding='utf8').read()
for p in ('Community.html', 'Find_a_Cleanup.html'):
    if p not in pt.split(): pt = pt.rstrip('\n') + '\n' + p + '\n'
open('i18n/pages.txt', 'w', encoding='utf8').write(pt)
bs = open('build-stats.js', encoding='utf8').read()
if "'Community.html'" not in bs:
    bs = bs.replace("'Rawanes_Mission_Log.html'];", "'Rawanes_Mission_Log.html', 'Community.html', 'Find_a_Cleanup.html'];")
    open('build-stats.js', 'w', encoding='utf8').write(bs)

# ---- 'New' callout (assets/data/new-callout.json), placed right under the page hero
N = json.load(open('assets/data/new-callout.json', encoding='utf8'))
f = N['page']; s = open(f, encoding='utf8').read()
s = re.sub(r'<!-- NEW-CALLOUT:START -->.*?<!-- NEW-CALLOUT:END -->\n?', '', s, flags=re.S)
if N.get('enabled'):
    dt = f' <time class="new-date" datetime="{N["date"]}">{E(N["date_label"])}</time>' if N.get('date') and N.get('date_label') else ''
    blk = (f'<!-- NEW-CALLOUT:START --><aside class="new-callout" aria-label="{E(N["badge"])}"><a href="{E(N["link"])}"><span class="new-badge">{E(N["badge"])}</span>'
           f'<span class="new-text">{E(N["text"])}{dt}</span><span class="new-cta">{E(N["link_text"])} <span aria-hidden="true">→</span></span></a></aside><!-- NEW-CALLOUT:END -->')
    i = s.index('</section>', s.index('<section class="page-hero')) + len('</section>\n')
    s = s[:i] + blk + '\n' + s[i:]
open(f, 'w', encoding='utf8').write(s); print('new-callout:', f, N.get('enabled'))
