#!/usr/bin/env python3
"""Oct 18: site-wide animated page banners at the Lesson_Builder standard, built from scripts/sp_banner.py.
Every <section class="page-hero ..."> whose page is listed in assets/data/anim-banners.json ("pages": EN file -> the image it
rendered before, measured from the live computed style) and whose image has an R2 original ("images": asset -> R2 manifest key +
exact credit) gets: picture.spb-media (R2 WebP/AVIF srcset from the untouched master) with the slow sp_banner drift + light sweep,
a pause button (WCAG 2.2.2), prefers-reduced-motion = still image, and the accurate credit. The section keeps its page-hero
classes, so size and the vertically centred title stay the Lesson_Builder standard (styles.css 'min-height:max(34vh,260px)').
All languages (en fr es ar it + hidden he); pause label and SI credit come from the i18n memories. Injected markup sits in
ANIMBAN markers (ignored by the i18n hash), so the pass is idempotent. Skips: index (homepage hero locked), Artemis_II (own
worker), Project-Rawane (page-scoped), Solutions / Top_Ten (already sp_banner), Amazing_Facts (af-hero already animated).
Run late in weekly-sync.sh (after apply-heroes and build-lcp, before build-tight-cards / build-critical)."""
import os, re, glob, json, sys, html, zlib
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, 'scripts')
import sp_banner as SPB
import sp_slides as SPX

SKIP = {'index.html', 'Artemis_II.html', 'Project-Rawane.html', 'Solutions.html', 'Top_Ten.html', 'Amazing_Facts.html'}
CFG = json.load(open('assets/data/anim-banners.json', encoding='utf8'))
MF = json.load(open('assets/data/media-manifest.json', encoding='utf8'))
TM = {l: json.load(open(f'i18n/{l}.json', encoding='utf8')) for l in ('fr', 'es', 'ar', 'it', 'he') if os.path.exists(f'i18n/{l}.json')}
PAUSE_LABEL = 'Pause banner animation'
MK = lambda x: f'<!-- ANIMBAN:START -->{x}<!-- ANIMBAN:END -->'
ADD = ['sp-anim-banner', 'has-pause', 'pg-anim']
STRIPC = ADD + ['pg-long', 'pg-xlong'] + [f'spx-n{i}' for i in range(2, SPX.NMAX + 1)]

CSS = (# one size everywhere (the Lesson_Builder standard), also over the compact Oct 17 hero-about / hero-help first-screen rule
       'html body.toc-sub[class] .page-hero[class].pg-anim{height:auto!important;min-height:max(34vh,260px)!important;padding:calc(var(--nav-height,88px) + 1.5rem) 1.25rem 3.4rem!important;box-sizing:border-box}'  # bottom room for pause + credit
       '@media (min-width:761px){html body.toc-sub[class] .page-hero[class].pg-anim{padding-bottom:2rem!important}}'  # same title centring as Lesson_Builder (pause/credit sit in the corners)
       'html body.toc-sub[class] .page-hero[class].pg-anim h1{font-size:clamp(2rem,5vw,3.2rem);margin:0 0 .5rem}'
       'html body.toc-sub[class] .page-hero[class].pg-anim.pg-long h1{font-size:clamp(1.5rem,2.9vw,2.4rem)}'
       'html body.toc-sub[class] .page-hero[class].pg-anim.pg-xlong h1{font-size:clamp(1.25rem,2vw,1.8rem)}'
       'html body.toc-sub[class] .page-hero[class].pg-anim h1{text-wrap:balance}'
       'html body.toc-sub[class] .page-hero[class].pg-anim .page-hero-content p{max-width:56rem;margin-left:auto;margin-right:auto;text-wrap:balance}'
       'html body.toc-sub .page-hero.pg-anim[class]{background:#02060c!important;position:relative;overflow:hidden;isolation:isolate;contain:paint}'
       'html body.toc-sub .page-hero.pg-anim::after{background:linear-gradient(180deg,rgba(0,20,40,.38),rgba(0,20,40,.58))}'
       'html body.toc-sub .page-hero.pg-anim .page-hero-content{position:relative;z-index:1}'
       'html body.toc-sub .page-hero.pg-anim .page-hero-content p{animation:spb-in 1.1s .25s cubic-bezier(.2,.7,.2,1) both}'
       'html body.toc-sub .page-hero.pg-anim .hero-credit{z-index:2}'
       '@media (prefers-reduced-motion:reduce){html body.toc-sub .page-hero.pg-anim .page-hero-content p{animation:none!important}}')

# Oct 24 2026 (owner standard): several topic-matched photos per title banner. anim-banners.json "slides":
#   "pools": topic -> [R2 manifest keys]; "pages": EN file -> topic. Credits come from the "images" entries with the same R2 key
#   (every photo is already licensed + credited there; no ESA non-commercial, no JAXA, no RU/CN/KP/IR-led sources).
SL = CFG.get('slides', {})
CREDIT = {}
for _a, _i in CFG['images'].items(): CREDIT.setdefault(_i['r2'], _i)
CUR = {'page': None}
#   "curated": EN file -> exact photo list (wins); otherwise the page's topic pool is rotated by a stable per-page offset so
#   neighbouring pages in a hub do not all show the same photos. "per_page": photos per banner (incl. the page's own photo).
def extra_slides(img):
    pg = CUR['page'] or ''
    cur = SL.get('curated', {}).get(pg)
    pool = cur or SL.get('pools', {}).get(SL.get('pages', {}).get(pg, ''), [])
    pool = [k for k in pool if k != img['r2'] and k in CREDIT and k in MF]
    want = (len(pool) if cur else SL.get('per_page', 4) - 1)
    if not cur and pool:
        o = zlib.crc32(pg.encode()) % len(pool); pool = pool[o:] + pool[:o]
    return [CREDIT[k] for k in pool[:min(want, SPX.NMAX - 1)]]

def t(lang, s): return TM.get(lang, {}).get(s) or s

def strip(s):
    s = re.sub(r'<!-- ANIMBAN:START -->[\s\S]*?<!-- ANIMBAN:END -->', '', s)
    # Oct 24 fix: only sections this pass styled (class pg-anim) lose its classes; before, every <section> on a page that merely
    # mentioned 'pg-anim' lost 'sp-anim-banner' too, which un-centred the Solutions / Top Ten banners (their sp_banner layout).
    return re.sub(r'(<section class=")([^"]*\bpg-anim\b[^"]*)"', lambda m: m.group(1) + ' '.join(c for c in m.group(2).split() if c not in STRIPC) + '"', s, count=0) if 'pg-anim' in s else s

def apply(s, lang, img):
    m = re.search(r'<section class="(page-hero(?: [\w-]+)*)"([^>]*)>', s)
    if not m: return s
    end = s.find('</section>', m.end())
    if end < 0: return s
    slides = [img] + extra_slides(img)
    pics, creds = [], []
    for i, sl in enumerate(slides):
        p = SPB.picture(MF[sl['r2']], '').replace('<img ', f'<img style="object-position:{sl.get("pos", "50% 50%")}" ', 1)
        if i: p = p.replace('fetchpriority="high"', 'fetchpriority="low" loading="lazy"')
        pics.append(f'<div class="spx-slide spx-{i}" aria-hidden="true">{p}</div>' if len(slides) > 1 else p)
        creds.append(f'<span class="hero-credit spx-cred spx-c{i}">{SPB._e(t(lang, sl["credit"]))}</span>' if len(slides) > 1 else
                     f'<span class="hero-credit">{SPB._e(t(lang, sl["credit"]))}</span>')
    pic = ''.join(pics)
    nslide = f' spx-n{len(slides)}' if len(slides) > 1 else ''
    body = re.sub(r'<span class="hero-credit">[\s\S]*?</span>', '', s[m.end():end])
    # Oct 18: long titles step down so the h1 stays on one line and the band keeps the Lesson_Builder height (279/261/306)
    hm = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', body); n = len(html.unescape(re.sub(r'<[^>]+>', '', hm.group(1))).strip()) if hm else 0
    size = ' pg-xlong' if n > 44 else ' pg-long' if n > 26 else ''
    btn = SPB.PAUSE_BTN.replace(PAUSE_LABEL, t(lang, PAUSE_LABEL))
    cred = ''.join(creds)
    return (s[:m.start()] + f'<section class="{m.group(1)} {" ".join(ADD)}{size}{nslide}"{m.group(2)}>' + MK(pic + '<span class="spb-sweep" aria-hidden="true"></span>')
            + body + MK(cred + btn) + '</section>' + MK(SPB.PAUSE_JS) + s[end + len('</section>'):])

n = 0
for f in sorted(glob.glob('*.html') + glob.glob('[a-z][a-z]/*.html')):
    base, lang = os.path.basename(f), (f.split('/')[0] if '/' in f else 'en')
    s = open(f, encoding='utf8').read()
    s2 = strip(s) if 'ANIMBAN' in s or 'pg-anim' in s else s
    asset = CFG['pages'].get(base)
    img = CFG['images'].get(asset) if asset else None
    if base not in SKIP and img and img['r2'] in MF and re.search(r'<section class="page-hero', s2):
        s2 = re.sub(r'<!-- LCPPRE:START -->[\s\S]*?<!-- LCPPRE:END -->', '', s2)  # the CSS background is no longer used
        CUR['page'] = base; s2 = apply(s2, lang, img)
    if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1

css = open('styles.css', encoding='utf8').read()
css2 = re.sub(r'\n?/\* ANIMBAN:START \*/.*?/\* ANIMBAN:END \*/\n?', '\n', css, flags=re.S).rstrip('\n') + '\n/* ANIMBAN:START */\n' + CSS + SPX.css() + '\n/* ANIMBAN:END */\n'
if css2 != css: open('styles.css', 'w', encoding='utf8').write(css2)
SPB.write_css('styles.css')
print('apply-anim-banners:', n, 'pages updated,', sum(1 for p, a in CFG['pages'].items() if a in CFG['images']), 'EN pages mapped')
