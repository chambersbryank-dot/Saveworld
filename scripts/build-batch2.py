#!/usr/bin/env python3
"""Batch 2: homepage hero video, status/hub badges on solution cards, Press link in footers,
launch .ics files + 'Add to calendar' links. Idempotent (marker blocks / class checks).
Run, then: python3 scripts/i18n-build.py && python3 scripts/i18n-sitemap.py && python3 scripts/seo-audit.py
Launch dates come ONLY from data-launch on each page's mission-widget (sourced on that page); items without an exact
published date (e.g. NEO Surveyor NET Sept 2027, Ramses spring 2028, Artemis III 2027) get no .ics."""
import json, re, os, glob, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)

def put(src, name, inner, after_re):
  b = f'<!-- {name}:START -->{inner}<!-- {name}:END -->'
  pat = re.compile(rf'<!-- {name}:START -->.*?<!-- {name}:END -->', re.S)
  if pat.search(src): return pat.sub(lambda m: b, src, count=1)
  m = re.search(after_re, src, re.S)
  if not m: raise SystemExit(f'anchor not found for {name}')
  return src[:m.end()] + b + src[m.end():]

# 1) Hero video (index only)
HERO = ('<div class="hero-media" aria-hidden="true"><video class="hero-video" autoplay muted loop playsinline preload="metadata" '
        'poster="assets/videos/hero-loop.jpg" width="1280" height="546"><source src="assets/videos/hero-loop.mp4" type="video/mp4"></video>'
        '<div class="hero-overlay"></div></div><p class="hero-video-credit">SI-generated video by Saving Planets.</p>')
s = open('index.html', encoding='utf8').read()
s = put(s, 'HERO-VIDEO', HERO, r'<section class="hero space-hero">')
s = s.replace('<section class="hero space-hero">', '<section class="hero space-hero has-video">', 1) if 'has-video' not in s else s
open('index.html', 'w', encoding='utf8').write(s)

# 2) Badges on solution cards
HUB = {'ocean': ('🌊', 'Ocean'), 'lakes': ('🏞️', 'Lakes'), 'rivers': ('💧', 'Rivers'), 'forests': ('🌳', 'Forests'),
       'space': ('🛰️', 'Space'), 'planetary-defense': ('☄️', 'Planetary Defense'), 'space-weather': ('☀️', 'Space Weather'),
       'earth-observation': ('🌍', 'Earth Observation'), 'project-r': ('🚀', 'Project Rawane')}
data = json.load(open('assets/data/solutions.json', encoding='utf8'))
info = {p['url']: p for p in data['pages'] if not p.get('section') and p['type'] == 'solution'}
def badge(p):
  st = p['status']; ic, hub = HUB[p['category']]
  lab = 'On the horizon' if st == 'horizon' else 'Active'
  return (f'<p class="sol-badges"><span class="status-badge status-{st}">{lab}</span>'
          f'<span class="hub-tag"><span aria-hidden="true">{ic}</span> {hub}</span></p>')
nb = 0
for f in sorted(glob.glob('*.html')):
  s = open(f, encoding='utf8').read(); o = s
  def card(m):
    global nb
    c = re.sub(r'<p class="sol-badges">.*?</p>', '', m.group(0))
    h = re.search(r'<h3><a href="([^"#]+)', c)
    if not h or h.group(1) not in info: return c
    c = re.sub(r'(<h3>.*?) <span class="menu-tag" aria-hidden="true">horizon</span>(.*?</h3>)', r'\1\2', c, flags=re.S)
    nb += 1
    return c.replace('<h3>', badge(info[h.group(1)]) + '<h3>', 1)
  s = re.sub(r'<article class="card"[^>]*>.*?</article>', card, s, flags=re.S)
  # 3) Press link in footer
  if '<footer>' in s and 'href="Press.html"' not in s.split('<footer>', 1)[1]:
    a, b = s.split('<footer>', 1); i = b.find('</p>')
    if i > 0: s = a + '<footer>' + b[:i + 4] + '<p class="footer-links"><a href="Press.html">Press &amp; media</a></p>' + b[i + 4:]
  if s != o: open(f, 'w', encoding='utf8').write(s)
print('badged cards:', nb)

# 4) Launch calendar
SRC = {'MMX.html': 'https://global.jaxa.jp/press/2026/08/20260820-1_e.html', 'Titan.html': 'https://science.nasa.gov/mission/dragonfly/'}
LBL = {'MMX.html': ('MMX launch (JAXA, H3 F10, Tanegashima)', 'mmx-launch', 'Date and time from JAXA.'),
       'Titan.html': ('Dragonfly launch period opens (NASA, Falcon Heavy, Kennedy Space Center)', 'dragonfly-launch', 'Launch period opening date from NASA.')}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
for f in sorted(glob.glob('*.html')):
  s = open(f, encoding='utf8').read()
  m = re.search(r'<section class="mission-widget"[^>]*data-launch="([^"]+)"[^>]*>.*?</section>', s, re.S)
  if not m or f not in LBL: continue
  d = datetime.datetime.fromisoformat(m.group(1).replace('Z', '+00:00'))
  if d < datetime.datetime.now(datetime.timezone.utc): continue
  title, slug, note = LBL[f]
  esc = lambda t: t.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,')
  if d.hour == d.minute == d.second == 0:
    when = f'DTSTART;VALUE=DATE:{d:%Y%m%d}\r\nDTEND;VALUE=DATE:{d + datetime.timedelta(days=1):%Y%m%d}'
  else:
    when = f'DTSTART:{d:%Y%m%dT%H%M%SZ}\r\nDTEND:{d + datetime.timedelta(hours=1):%Y%m%dT%H%M%SZ}'
  ics = ('BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Saving Planets//Launch calendar//EN\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\n'
         f'BEGIN:VEVENT\r\nUID:{slug}-{d:%Y%m%d}@savingplanets.com\r\nDTSTAMP:{now}\r\n{when}\r\nSUMMARY:{esc(title)}\r\n'
         'DESCRIPTION:' + esc(f'{note} Launch dates can slip. Source: {SRC[f]} · More: https://www.savingplanets.com/{f}') + '\r\n'
         f'URL:https://www.savingplanets.com/{f}\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n')
  p = f'assets/calendar/{slug}.ics'
  old = open(p, encoding='utf8', newline='').read() if os.path.exists(p) else ''
  if re.sub(r'DTSTAMP:\S+', '', old) != re.sub(r'DTSTAMP:\S+', '', ics): open(p, 'w', encoding='utf8', newline='').write(ics)
  link = (f'<p class="cal-add"><a class="btn cal-btn" href="{p}" download><span aria-hidden="true">📅</span> Add to calendar</a> '
          f'<span class="cal-note">{note} Launch dates can slip; check the page before launch day.</span></p>')
  s = put(s, 'CAL', link, r'<section class="mission-widget"[^>]*data-launch="[^"]+"[^>]*>.*?</section>')
  open(f, 'w', encoding='utf8').write(s); print('calendar:', f, p, d.isoformat())
