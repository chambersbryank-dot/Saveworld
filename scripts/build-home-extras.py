#!/usr/bin/env python3
"""Videos on solution pages, Planet Scoreboard and Solution of the Week on index.html.
Idempotent: each block lives between <!-- NAME:START --> / <!-- NAME:END --> markers.
Run, then: python3 scripts/i18n-build.py && python3 scripts/i18n-sitemap.py && python3 scripts/seo-audit.py
Run weekly (or any time) to refresh the Solution of the Week static fallback."""
import json, re, subprocess, html, datetime, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CAP = 'Created by SI and Biological SI Partner.'

VIDEOS = {  # page: (file, heading, anchor regex to insert AFTER)
  'Great_Bubble_Barrier.html': ('great-bubble-barrier', 'Watch: A Wall of Bubbles Stopping Plastic'),
  'Life_Terra.html': ('life-terra-trees', 'Watch: Millions of Trees, One Seedling at a Time'),
  'GRACE-FO.html': ('grace-fo-satellites', "Watch: Satellites That Weigh Earth's Water"),
  'Artemis_II.html': ('artemis-ii-farthest', 'Watch: The Farthest Humans Have Gone'),
}

def dims(f):
  o = subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',f]).decode().strip().split(',')
  return int(o[0]), int(o[1])

def dims_img(f):
  return dims(f)

def block(name, inner):
  return f'<!-- {name}:START -->{inner}<!-- {name}:END -->'

def put(src, name, inner, after_re):
  b = block(name, inner)
  pat = re.compile(rf'<!-- {name}:START -->.*?<!-- {name}:END -->', re.S)
  if pat.search(src): return pat.sub(lambda m: b, src, count=1)
  m = re.search(after_re, src, re.S)
  if not m: raise SystemExit(f'anchor not found for {name}')
  return src[:m.end()] + '\n' + b + src[m.end():]

def video_html(slug, heading):
  w, h = dims(f'assets/videos/{slug}.mp4')
  return (f'<section class="sp-video" id="video" aria-labelledby="video-title"><h2 id="video-title">{html.escape(heading)}</h2>'
    f'<figure class="sp-video-fig"><video controls playsinline preload="metadata" poster="assets/videos/{slug}.jpg" width="{w}" height="{h}">'
    f'<source src="assets/videos/{slug}.mp4" type="video/mp4"><a href="assets/videos/{slug}.mp4">Download the video</a></video>'
    f'<figcaption class="photo-credit">{CAP}</figcaption></figure></section>')

for page, (slug, heading) in VIDEOS.items():
  s = open(page, encoding='utf-8').read()
  # right after the page hero (first section on the page)
  s = re.sub(r'\n?<!-- VIDEO:START -->.*?<!-- VIDEO:END -->', '', s, flags=re.S)  # re-place each run
  s = put(s, 'VIDEO', video_html(slug, heading), r'<section class="page-hero[^"]*">.*?</section>(\s*<p class="photo-credit">[^<]*</p>)?(\s*<nav aria-label="Breadcrumb".*?</nav>)?')
  open(page, 'w', encoding='utf-8').write(s)

# ---- About: featured 9:16 ad on top, older channel intro lower on the page ----
try: _N = json.load(open('assets/data/solutions.json', encoding='utf8'))['site']['solutions']
except Exception: _N = 120
AD_CAP = f'A 70-second tour: {_N} real solutions, free lesson plans, the Kids Planet Map, the 3D Satellite Explorer, search, Amazing Facts, Myth vs Fact, live launches and five languages.'  # Oct 14: v3 (real site footage + NASA B-roll)
s = open('About.html', encoding='utf-8').read()
s = re.sub(r'\n?<!-- VIDEO:START -->.*?<!-- VIDEO:END -->', '', s, flags=re.S)
s = re.sub(r'<!-- VIDEO2:START -->.*?<!-- VIDEO2:END -->', '', s, flags=re.S)
w, h = dims('assets/videos/savingplanets-about-v3.mp4')
AD = ('<section class="sp-video sp-video-vertical" id="video" aria-labelledby="video-title"><h2 id="video-title">Watch: What Saving Planets Is About</h2>'
  f'<figure class="sp-video-fig"><video controls playsinline preload="metadata" poster="assets/videos/savingplanets-about-v3.jpg" width="{w}" height="{h}">'
  '<source src="assets/videos/savingplanets-about-v3.mp4" type="video/mp4"><source src="assets/videos/savingplanets-about-v3-720.mp4" type="video/mp4"><a href="assets/videos/savingplanets-about-v3.mp4">Download the video</a></video>'
  f'<figcaption><span class="sp-video-cap">{html.escape(AD_CAP)}</span><span class="photo-credit">Created by SI and Biological SI Partner</span> <span class="photo-credit">Footage: NASA</span></figcaption></figure></section>')
s = put(s, 'VIDEO', AD, r'<section class="page-hero[^"]*">.*?</section>(\s*<p class="photo-credit">[^<]*</p>)?(\s*<nav aria-label="Breadcrumb".*?</nav>)?')
# (Oct 12) older channel intro removed from About; VIDEO2 block intentionally no longer rebuilt.
open('About.html', 'w', encoding='utf-8').write(s)

# ---- Planet Scoreboard (figures already on the site, each verified at its source) ----
data = json.load(open('assets/data/solutions.json'))
eo = [p for p in data['pages'] if p.get('category') == 'earth-observation' and p.get('type') != 'hub' and p.get('status') == 'active']
COUNTERS = [
  (36000000, '+', 'trees planted by Life Terra and its partners', 'Life_Terra.html',
   'Life Terra (company figure)', 'https://pr.euractiv.com/?q=node%2F276414', 'May 2026'),
  (65000000, '+ kg', 'trash removed from rivers and the ocean by The Ocean Cleanup', 'Ocean_Cleanup.html',
   'The Ocean Cleanup (company figure)', 'https://theoceancleanup.com/', 'October 2026'),
  (252756, '', 'miles from Earth: the farthest humans have traveled, on Artemis II', 'Artemis_II.html',
   'NASA', 'https://www.nasa.gov/news-release/nasas-artemis-ii-crew-eclipses-record-for-farthest-human-spaceflight/', 'April 2026'),
  (len(eo), '', 'active Earth-watching missions and satellites on this site', 'Earth_Observation.html',
   'Each mission page, sourced to NASA, ESA, JAXA, ISRO, NOAA or the operator', 'Earth_Observation.html', 'October 11, 2026'),
]
cells = []
for n, suf, label, page, src, url, asof in COUNTERS:
  ext = url.startswith('http')
  a = f' target="_blank" rel="noreferrer"' if ext else ''
  cells.append(f'<div class="sb-item"><a class="sb-link" href="{page}"><span class="sb-num" data-count="{n}" data-suffix="{html.escape(suf)}">{n:,}{html.escape(suf)}</span>'
    f'<span class="sb-label">{html.escape(label)}</span></a>'
    f'<p class="sb-src fact-source">Source: <a href="{url}"{a}>{html.escape(src)}</a> · As of {asof}</p></div>')
SB = ('<section class="scoreboard" id="scoreboard" aria-labelledby="sb-title"><h2 id="sb-title"><span class="brand-blue">Planet</span> Scoreboard</h2>'
      '<p class="sb-intro">Running totals from the solutions on this site. Tap a number to see the solution behind it.</p>'
      '<div class="sb-grid">' + ''.join(cells) + '</div></section>')

# ---- Solution of the Week ----
sw = json.load(open('assets/data/solution-of-week.json'))
start = datetime.date.fromisoformat(sw['start'])
today = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) - datetime.timedelta(hours=10)).date()  # HST
e = sw['rotation'][((today - start).days // 7) % len(sw['rotation'])]
href = e['page'] + ('#video' if e.get('video') else '')
SW = (f'<section class="sotw" id="solution-of-the-week" aria-labelledby="sotw-title" data-sotw-page="{e["page"]}"><div class="sotw-card">'
      f'<a class="sotw-img" href="{href}"><img src="{e["image"]}" alt="{html.escape(e["imageAlt"])}" width="{dims_img(e["image"])[0]}" height="{dims_img(e["image"])[1]}" loading="lazy" decoding="async"></a>'
      f'<div class="sotw-body"><p class="sotw-kicker">Solution of the Week</p><h2 id="sotw-title"><a href="{e["page"]}">{html.escape(e["title"])}</a></h2>'
      f'<p class="sotw-blurb">{html.escape(e["blurb"])}</p><p class="sotw-actions"><a class="btn" href="{href}">{"Watch and Learn More" if e.get("video") else "Learn More"}</a></p>'
      f'<p class="photo-credit">Created by SI and Biological SI Partner.</p></div></div></section>')

s = open('index.html', encoding='utf-8').read()
s = put(s, 'SOTW', SW, r'<section class="mission-block">.*?</section>')
s = put(s, 'SCOREBOARD', SB, r'<section class="impact-bar">.*?</section>')
open('index.html', 'w', encoding='utf-8').write(s)
print('SOTW:', e['page'], '| EO active:', len(eo))
