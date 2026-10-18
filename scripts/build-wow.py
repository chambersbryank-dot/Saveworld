#!/usr/bin/env python3
"""Oct 17 2026 'every page is real estate' rule (owner): the first screen of the top pages shows the wow.
English source moves (i18n-build carries them to fr/es/ar/it; idempotent) + a WOW CSS block in styles.css.
- index: the 'Please email ideas@' line leaves the hero for 'Be Part of the Fix' (hero = title + CTAs only).
- Ways_to_Help: top Home/About buttons dropped (the same links stay at the bottom); 'How This Works' moves below the
  Donate or Volunteer table, which now starts the page. Hero shorter.
- About: the mission ('Saving Planets, Minus the Doom') + 175-solutions strip come first; the video moves after them.
- Solutions / Amazing Facts: shorter heroes and tighter intro so cards/facts start on the first screen (data tools and
  learning-tool tiles are moved by build-data-tools.py / build-edu.py)."""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
def rd(p): return open(p, encoding='utf8').read()
def wr(p, s0, s):
    if s != s0: open(p, 'w', encoding='utf8').write(s); return 1
    return 0
def cut(s, pat):
    m = re.search(pat, s, re.S)
    if not m: return s, ''
    return s[:m.start()] + s[m.end():], m.group(0)
n = 0
# index.html
s0 = s = rd('index.html')
s, email = cut(s, r'<p class="hero-email">.*?</p>')
if email:
    s = re.sub(r'(<section id="actions">.*?<p class="join-lead">.*?</p>)', lambda m: m.group(1) + email, s, count=1, flags=re.S)
n += wr('index.html', s0, s)
# Ways_to_Help.html
s0 = s = rd('Ways_to_Help.html')
s, _ = cut(s, r'<div class="help-pagelinks">.*?</div>\s*')
if s.find('<section class="impact" id="solution"') < s.find('<section class="five-ws" id="donate"'):
    s, how = cut(s, r'<section class="impact" id="solution">.*?</section>\s*')
    i = s.find('<section class="five-ws" id="donate"'); j = s.find('</section>', i) + len('</section>')
    s = s[:j] + '\n' + how.strip() + s[j:]
n += wr('Ways_to_Help.html', s0, s)
# About.html: the video placement now lives in build-home-extras.py (VIDEO marker block). The old move here cut the
# section out of its markers, so each sync re-added it: duplicate videos (fixed Oct 17, caught by SI Partner).

CSS = """/* WOW:START (scripts/build-wow.py, Oct 17: first screen = the best content) */
html body.sol-page .sol-hero .sol-hero-title{font-size:clamp(1.5rem,3.2vw,2.2rem);margin:0 0 .4rem}
html .sol-intro{padding-top:1rem}html .sol-intro h1{font-size:clamp(1.4rem,2.6vw,2rem);margin:0 0 .4rem}
html .sol-intro .sol-filters{margin:.4rem 0;justify-content:center}
@media (min-width:700px){html .sol-jump ul{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;scrollbar-width:thin;padding-bottom:.3rem}html .sol-jump li{flex:0 0 auto}}
html .sol-hub>h2{margin-top:1rem}
html body[class] .page-hero[class].sol-hero,html body[class] .page-hero[class].af-hero,html body[class] .page-hero[class].hero-help,html body[class] .page-hero[class].hero-about{min-height:200px!important;padding:calc(var(--nav-height,88px) + .5rem) 1.25rem 1rem!important}
html body.toc-sub .page-hero.af-hero h1,html body.toc-sub .page-hero.hero-help h1,html body.toc-sub .page-hero.hero-about h1{font-size:clamp(1.6rem,3.4vw,2.4rem);margin-bottom:.3rem}
html body.toc-sub .page-hero.af-hero p.af-hero-credit{margin-top:.3rem}
/* WOW:END */"""
s0 = s = rd('styles.css')
s = re.sub(r'/\* WOW:START.*?WOW:END \*/', '', s, flags=re.S).rstrip('\n') + '\n' + CSS + '\n'
n += wr('styles.css', s0, s)
print('build-wow:', n, 'files updated')
