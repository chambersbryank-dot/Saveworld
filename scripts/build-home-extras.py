#!/usr/bin/env python3
"""Videos on solution pages, Planet Scoreboard and Solution of the Week on index.html.
Idempotent: each block lives between <!-- NAME:START --> / <!-- NAME:END --> markers.
Run, then: python3 scripts/i18n-build.py && python3 scripts/i18n-sitemap.py && python3 scripts/seo-audit.py
Run weekly (or any time) to refresh the Solution of the Week static fallback."""
import json, re, subprocess, html, datetime, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CAP = 'Created by SI and Biological SI Partner.'
sys.path.insert(0, os.path.join(ROOT, 'scripts')); import media as MEDIA  # Oct 16: videos served from R2 (media.savingplanets.com)

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
  w, h = MEDIA.dims(f'{slug}.mp4'); u = MEDIA.vurl(f'{slug}.mp4')
  return (f'<section class="sp-video" id="video" aria-labelledby="video-title"><h2 id="video-title">{html.escape(heading)}</h2>'
    f'<figure class="sp-video-fig"><video controls playsinline preload="metadata" poster="assets/videos/{slug}.jpg" width="{w}" height="{h}">'
    f'<source src="{u}" type="video/mp4"><a href="{u}">Download the video</a></video>'
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
# Oct 17: the recorded narration says 120 (pinned in assets/data/a11y.json), so the caption says when it was recorded instead of the live count.
# Oct 18: About v4 (88 s, new clear narration recorded at 175 solutions; cues pinned in a11y.json). Old v3 (70 s, 120) retired and deleted from R2.
AD_CAP = "An 88-second tour: 175 real solutions across 10 hubs, each explained with the Five W's, plus Ways to Help, free lesson plans, the Kids Planet Map, the Satellite Explorer, Myth vs Fact, Amazing Facts, live launches and five languages."
s = open('About.html', encoding='utf-8').read()
s = re.sub(r'\n?<!-- VIDEO:START -->.*?<!-- VIDEO:END -->', '', s, flags=re.S)
s = re.sub(r'<!-- PROMO:START -->.*?<!-- PROMO:END -->', '', s, flags=re.S)  # Oct 20: promo now lives in the VIDEO block
s = re.sub(r'<!-- VIDEO2:START -->.*?<!-- VIDEO2:END -->', '', s, flags=re.S)
# Oct 17 fix (dup video): drop any unmarked copy left by the old build-wow.py move, so exactly one video remains.
s = re.sub(r'\s*<section class="sp-video sp-video-vertical" id="video".*?</section>', '', s, flags=re.S)
# Oct 20 (founder): About keeps ONE video, promo v6 (built below, placed after the DIFF strip in the VIDEO block). About v4 retired.
# (Oct 12) older channel intro removed from About; VIDEO2 block intentionally no longer rebuilt.
open('About.html', 'w', encoding='utf-8').write(s)

# ---- Planet Scoreboard (figures already on the site, each verified at its source) ----
data = json.load(open('assets/data/solutions.json'))
eo = [p for p in data['pages'] if p.get('category') == 'earth-observation' and p.get('type') != 'hub' and p.get('status') == 'active']
COUNTERS = [
  (36000000, '+', 'trees planted by Life Terra and its partners', 'Life_Terra.html',
   'Life Terra (company figure)', 'https://web.archive.org/web/20260613124357/http://pr.euractiv.com/?q=node%2F276414', 'May 2026'),
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
# ---- Oct 18: promo v3 just below the hero + impact strip (hero position is LOCKED; this block only sits after it) ----
# Wide 16:9 master for landscape/desktop/iPad, 9:16 master for narrow portrait phones (CSS picks one; preload=metadata, no autoplay).
# Oct 18 3:45 PM HST (owner): promo v4 (148 s, 191 solutions / 11 hubs; caption-fixed cut, 5:17 PM) replaces v3. One 9:16 master only (no 16:9 cut), so one centred player at every width.
# Oct 20 (founder): promo v6 (2:21, 231 solutions, six languages incl. Hebrew) replaces v4 on the homepage and About; 720p fallback source.
VW, VH = MEDIA.dims('savingplanets-promo-v6-1080x1920.mp4'); VU = MEDIA.vurl('savingplanets-promo-v6-1080x1920.mp4'); VU7 = MEDIA.vurl('savingplanets-promo-v6-1080x1920-720.mp4')
PROMO_H = "Watch: What's New on Saving Planets"
# Oct 18: 191 solutions now; the promo was recorded at 175 and is not edited, so the caption says so
PROMO_CAP = "A 2-minute tour of Saving Planets today: 231 real solutions in 11 hubs, the new homepage, six languages, the interactive World Map and Myth vs Fact."
PROMO_SRC = "Earth: NASA Blue Marble and Black Marble · Saturn: NASA/JPL-Caltech/Space Science Institute · Myth vs Fact: NOAA, NASA, NASA DART · Map: © OpenStreetMap · Launches: The Space Devs · Site screens: Saving Planets"
try: PROMO_X = json.load(open('assets/data/promo-links.json', encoding='utf-8')).get('x_post', '')
except Exception: PROMO_X = ''
PX = f'<p class="promo-x"><a href="{html.escape(PROMO_X)}" target="_blank" rel="noopener">See our new milestone on X →</a></p>' if PROMO_X else ''
PROMO = ('<section class="sp-video sp-promo" id="whats-new-video" aria-labelledby="promo-title">'
  f'<h2 id="promo-title">{html.escape(PROMO_H, quote=False)}</h2><figure class="sp-video-fig">'
  f'<video class="promo-v4 promo-v6" controls playsinline preload="metadata" poster="assets/videos/savingplanets-promo-v6-tall.jpg" width="{VW}" height="{VH}" aria-label="{html.escape(PROMO_H, quote=False)}">'
  f'<source src="{VU}" type="video/mp4"><source src="{VU7}" type="video/mp4"><a href="{VU}">Download the video</a></video>'
  f'<figcaption><span class="sp-video-cap">{html.escape(PROMO_CAP, quote=False)}</span><span class="photo-credit">Created by SI and Biological SI Partner</span> '
  f'<span class="photo-credit">{html.escape(PROMO_SRC, quote=False)}</span></figcaption></figure>{PX}</section>')
# Oct 20: the HOMEPAGE promo stays v4 (founder approved v6 for About only; homepage layout is under review in PR #16)
W4, H4 = MEDIA.dims('savingplanets-promo-v4-final-1080x1920.mp4'); U4 = MEDIA.vurl('savingplanets-promo-v4-final-1080x1920.mp4')
PROMO_HOME = (PROMO.replace('class="promo-v4 promo-v6"', 'class="promo-v4"').replace('savingplanets-promo-v6-tall.jpg', 'savingplanets-promo-v4-tall.jpg')
  .replace(f'<source src="{VU7}" type="video/mp4">', '').replace(VU, U4).replace(f'width="{VW}" height="{VH}"', f'width="{W4}" height="{H4}"')
  .replace(html.escape(PROMO_CAP, quote=False), html.escape("A 2½-minute tour of Saving Planets today: 191 real solutions in 11 hubs, the new homepage, the interactive World Map and Myth vs Fact.", quote=False)))
s = put(s, 'PROMO', PROMO_HOME, r'<!-- IMPACT:START -->.*?<!-- IMPACT:END -->')
open('index.html', 'w', encoding='utf-8').write(s)
# Oct 18 (owner request): the same promo on About, directly below the 'From the ocean floor…' strip. Oct 20: it is now the ONLY About video.
s = open('About.html', encoding='utf-8').read()
PROMO_ABOUT = re.sub(r'<figcaption>.*?</figcaption>', '', PROMO.replace('class="sp-video sp-promo"', 'class="sp-video sp-promo sp-promo-about"', 1), flags=re.S)
# Oct 20: keep the visible SI credit under the About video (founder); transcript stays screen-reader text (data-transcript="sr")
PROMO_ABOUT = PROMO_ABOUT.replace('</video>', '</video><figcaption class="photo-credit">Created by SI and Biological SI Partner</figcaption>', 1)
PROMO_ABOUT = PROMO_ABOUT.replace('<figure class="sp-video-fig">', '<figure class="sp-video-fig" data-transcript="sr">', 1)
s = re.sub(r'<!-- PROMO:START -->.*?<!-- PROMO:END -->', '', s, flags=re.S)
s = put(s, 'VIDEO', PROMO_ABOUT, r'<!-- DIFF:START -->.*?<!-- DIFF:END -->')
open('About.html', 'w', encoding='utf-8').write(s)
print('SOTW:', e['page'], '| EO active:', len(eo))
