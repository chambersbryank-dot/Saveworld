#!/usr/bin/env python3
"""Oct 16 2026 (user: "alternate the animations [behind the homepage title] on a weekly basis ... switch to beautiful space
animation next. Hi res and 'Wow'. Start one now"). Adds the HEROTHEME block to index.html in en/fr/es/ar/it, right after the
HERO-VIDEO block (build-batch2.py), which is left untouched and stays the 'earth' theme (SI video: Earth sunrise, ocean
shoreline, rainforest canopy).
Rotation: an inline script picks the theme before first paint, deterministically for everyone: weeks elapsed since Monday
12 Oct 2026 00:00 HST (ISO week 2026-W42) index into ROTATION, so space shows W42 and the themes alternate each Monday
00:00 HST. Counting elapsed weeks (not ISO week parity) keeps the alternation correct across 53-week ISO years.
To add a theme: append it to ROTATION, render it in assets/hero-themes.js (or reuse the video kind), add CSS below.
?hero=<name> previews any theme. Non-video themes strip the video's sources before it downloads.
Run after i18n-build.py (the block is excluded from the translation hash, see i18n-build.normalize / i18n-check.js)."""
import re, os, hashlib, json
# Oct 16 8:05 PM: NASA Blue Marble Earth texture (R2, media-manifest.json) for the Earthrise scene; srcset handed to the JS.
MAN = json.load(open('assets/data/media-manifest.json', encoding='utf-8'))
BM = MAN['images/earth-blue-marble-land-ocean-ice-cloud.jpg']['srcset']
# Oct 16 8:16-8:19 PM: pre-rendered ground textures + poster stills (scripts/build-hero-assets.py -> R2). Missing = procedural / no poster.
HS = lambda f: (MAN.get('images/hero-space/' + f) or {}).get('url', '')
def TEXATTR():
    return ''.join(f' {a}="{HS(f)}"' for a, f in (('data-tex-a', 'enceladus-1024.webp'), ('data-tex-a2', 'enceladus-2048.webp'),
                                                 ('data-tex-b', 'moon-1024.webp'), ('data-tex-b2', 'moon-2048.webp')) if HS(f))

def SATATTR():
    # Cassini PIA11141 (NASA/JPL-Caltech/Space Science Institute). Meta = gx,gy,gr (globe center/radius as fractions of image).
    parts = []
    for w in (960, 1280, 1920, 2560, 3840):
        e = MAN.get('images/hero-space/saturn-cassini-%d.webp' % w)
        if e and e.get('url'): parts.append('%s %dw' % (e['url'], w))
    if not parts: return ''
    return ' data-sat="%s" data-sat-meta="0.34751,0.48782,0.13085"' % (','.join(parts),)
def POSTER():  # .hero-space::before = still frame until the live ground is ready; widths up to 6016 (6K Retina @2x)
    sel, out = '.hero[data-hero=space] .hero-space::before', ''
    # three compositions (build-hero-assets.py), each rendered at the CSS size whose text layout it matches:
    # land = 1180x820 (iPad landscape .. 6K desktop), tab = 820x1180 portrait tablets, phone = 390x844 portrait phones
    for key, ws, mq, steps, top in (('land', [1280, 1920, 2560, 3840, 5120, 6016], 'landscape', [0, 1000, 1400, 2000, 2600], 3008),
                                    ('phone', [820, 1240], 'portrait', [0], 600), ('tab', [1640, 2048], 'portrait', [600, 900], 1200)):
        ws = [w for w in ws if HS(f'poster-{key}-{w}.webp')]
        if not ws: continue
        for r, res in ((1, ''), (2, ' and (min-resolution:1.5dppx)'), (3, ' and (min-resolution:2.5dppx)')):  # resolution outer: last match wins
            for n, lo in enumerate(steps):
                hi = steps[n + 1] if n + 1 < len(steps) else top
                w = next((x for x in ws if x >= hi * r * 0.95), ws[-1])  # smallest poster that covers the backing width
                av, wb = HS(f'poster-{key}-{w}.avif'), HS(f'poster-{key}-{w}.webp')
                img = (f'url("{wb}");background-image:image-set(url("{av}") type("image/avif"),url("{wb}") type("image/webp"))' if av else f'url("{wb}")')
                out += f'@media (orientation:{mq}) and (min-width:{lo}px){res}{{{sel}{{background-image:{img}}}}}'
    if out:
        out = (sel + '{content:"";position:absolute;inset:0;z-index:6;pointer-events:none;background:#000 center top/cover no-repeat;'
               'transition:opacity 1.2s ease}.hero[data-hero=space] .hero-space.hs-ready::before{opacity:0}') + out
    return out
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']  # Oct 17: he = Hebrew (built, unlinked until review; skipped if he/index.html is missing)
# Oct 17 2026 — LOCKED / OWNER-APPROVED HERO POSITION (iPad landscape reference).
# Owner: "Excellent. Set distance for future reference." Do not change without her ask.
# Space theme: placeTitleBlock() in assets/hero-themes.js centers the title block (kicker→buttons) between the
#   nav bottom and the scene's fixed horizon hY (equal gaps). Horizon is frozen so moons/planets do not move.
#   Measured gaps: iPad-L 76/76.6, iPad-P 272/271.6, Mac 86/86. Ref shot: /workspace/wow-shots/approved/home-hero-ipad-l-approved.png
# Earth/other themes (no horizon): HERO_OFFSET lifts the flex-centered block. Future themes MUST reuse this rule —
#   with a horizon: center between nav bottom and that horizon; without: use HERO_OFFSET. See NOTES.md.
HERO_OFFSET = '4vh'
ROTATION = ['space', 'earth']          # index 0 = ISO week 2026-W42
ANCHOR_UTC = 'Date.UTC(2026,9,12,10)'  # Mon 12 Oct 2026 00:00 HST
JSV = hashlib.sha1(open('assets/hero-themes.js', 'rb').read()).hexdigest()[:8]  # cache version follows the file

# Scene captions (space theme). Facts: NASA Science "Enceladus" (science.nasa.gov/saturn/moons/enceladus/: geyser-like
# jets of water vapor and ice particles; global subsurface saltwater ocean; jets from the "tiger stripe" fractures) and
# NASA "Apollo 8: Earthrise" (nasa.gov/image-article/apollo-8-earthrise/: Bill Anders, Dec 24 1968, first crewed lunar orbit).
CAPS = {
  'en': ('Enceladus: jets of water vapor and ice from a hidden ocean', 'Earthrise from lunar orbit, first seen by Apollo 8 in 1968'),
  'fr': ("Encelade : des jets de vapeur d'eau et de glace venus d'un océan caché", "Lever de Terre depuis l'orbite lunaire, vu pour la première fois par Apollo 8 en 1968"),
  'es': ('Encélado: chorros de vapor de agua y hielo de un océano oculto', 'Salida de la Tierra desde la órbita lunar, vista por primera vez por el Apolo 8 en 1968'),
  'ar': ('إنسيلادوس: نفثات من بخار الماء والجليد من محيط خفي', 'شروق الأرض من مدار القمر، كما رآه طاقم أبولو 8 لأول مرة عام 1968'),
  'it': ("Encelado: getti di vapore acqueo e ghiaccio da un oceano nascosto", "Il sorgere della Terra dall'orbita lunare, visto per la prima volta dall'Apollo 8 nel 1968"),
  'he': ('אנקלדוס: סילוני אדי מים וקרח מאוקיינוס נסתר', 'זריחת כדור הארץ ממסלול סביב הירח, שנצפתה לראשונה על ידי Apollo 8 ב-1968'),
}
CAP_HREF = ('Enceladus.html', 'Artemis_II.html')  # Oct 16: Enceladus caption -> the Enceladus page; Earthrise -> Artemis II (crewed flight around the Moon)

CSS = ('<style>.hero .hero-space,.hero .hs-caps{display:none}.hero[data-hero=space] .hero-media{display:none}'
       '.hero[data-hero=space] .hero-space{display:block;position:absolute;inset:0;z-index:-1;overflow:hidden;contain:strict;background:#000}'
       '.hs-layer{position:absolute;left:0;top:0;pointer-events:none;will-change:transform,opacity;backface-visibility:hidden}'
       '.hs-ground{opacity:0;transition:opacity 1.2s ease}.hs-ready .hs-ground{opacity:1}'
       '.hero-space::after{content:"";position:absolute;inset:0;pointer-events:none;'
       'background:radial-gradient(46% 38% at 50% 42%,rgba(0,4,12,.6) 0%,rgba(0,4,12,.34) 60%,rgba(0,4,12,0) 100%),'
       'linear-gradient(180deg,rgba(0,12,26,.5) 0%,rgba(0,12,26,0) 20%,rgba(0,12,26,0) 80%,rgba(0,8,18,.5) 100%)}'
       '.hero[data-hero=space] .hero-welcome,.hero[data-hero=space] .hero-kicker{text-shadow:0 2px 18px rgba(0,0,0,.8)}'
       '.hero[data-hero=space] .hero-example,.hero[data-hero=space] .hero-email{text-shadow:0 1px 10px rgba(0,0,0,.85)}'
       # Oct 16 7:05 PM: SI credit at the hero's inline-start corner (bottom-left LTR, bottom-right RTL), away from the
       # floating Help / Donate button (.sticky-help sits at inset-inline-end), on a dark pill so it reads on any frame.
       '.hero .hero-video-credit{right:auto;left:auto;inset-inline-start:.8rem;inset-inline-end:auto;bottom:.75rem;z-index:1;'
       'max-width:calc(100% - 13rem);padding:.22rem .6rem;border-radius:999px;background:rgba(0,10,22,.74);'
       'color:rgba(255,255,255,.94);font-size:.75rem;line-height:1.3;text-shadow:none}'
       # Oct 16 7:12 PM: scene caption, stacked above the credit at the same inline-start corner; fades with the scenes.
       '.hero[data-hero=space] .hs-caps{display:block;position:absolute;inset-inline-start:.8rem;bottom:2.8rem;z-index:2;width:min(30rem,calc(100% - 13rem));height:44px}'
       '.hs-cap{position:absolute;inset-inline-start:0;bottom:0;display:inline-flex;align-items:center;gap:.5rem;min-height:44px;box-sizing:border-box;'
       'width:max-content;max-width:100%;padding:.5rem .95rem;border-radius:22px;background:rgba(0,10,22,.78);border:1px solid rgba(255,255,255,.22);'
       'color:#fff!important;font-size:.88rem;font-weight:600;line-height:1.25;text-decoration:none!important;'
       'opacity:0;visibility:hidden;transform:translateY(6px);transition:opacity .9s ease,transform .9s ease,visibility 0s linear .9s}'
       '.hs-cap.on{opacity:1;visibility:visible;transform:none;transition:opacity .9s ease,transform .9s ease,visibility 0s}'
       '.hs-cap:hover{background:rgba(0,30,56,.88);border-color:rgba(143,211,255,.6)}'
       '.hs-cap:focus-visible{outline:3px solid #fff;outline-offset:3px}'
       '.hs-cap .hs-arr{color:#8fd3ff;flex:none}[dir=rtl] .hs-cap .hs-arr{transform:scaleX(-1)}'
       '.hero[data-hero=space].hs-lowsky .hero-email{background:rgba(0,8,18,.72);border-radius:12px;box-shadow:0 0 0 .4rem rgba(0,8,18,.72)}'
       '.hs-caps{visibility:hidden}.hero:not(.hs-placed) .hs-cap{visibility:hidden!important}'  # hidden until placed, so moving it is not a layout shift
       '.hero[data-hero=space].hs-captop .hs-caps{bottom:auto;top:var(--hs-captop,96px)}.hs-captop .hs-cap{bottom:auto;top:0}'
       '@media (max-width:600px){.hero[data-hero=space] .hs-caps{bottom:5rem;width:calc(100% - 1.6rem)}}'
       # Oct 16 7:57 PM (user: 'move everything up, the animation is cut off at the bottom'): the hero is framed by the visible
       # viewport (svh, so Safari's toolbar never crops it) and, in the space theme, the text block sits just under the nav.
       '.hero[data-hero],body.toc-home .hero.space-hero[data-hero]{height:100vh;height:100svh}'
       # 8:03 PM (user: 'move the text up several spaces, close under the nav, I want to see more moons'): text block starts
       # ~1rem under the nav (56px single row < 992px, 92px two rows from 992px) with tighter spacing between its lines.
       '.hero[data-hero=space] .hero-content{padding-top:calc(56px + .9rem);padding-bottom:1rem}'
       '@media (min-width:1140px){.hero[data-hero=space] .hero-content{padding-top:calc(92px + 1rem)}}'
       # Oct 17 6:15 PM: line spacing shared by every theme (was space-only) so the title block is identical on any background.
       '.hero[data-hero] .hero-kicker{margin-top:0;margin-bottom:1.1rem}.hero[data-hero] .hero-welcome{margin-bottom:.6rem}'
       '.hero[data-hero] .hero-ctas{margin:.8rem 0 .4rem}.hero[data-hero] .hero-email{margin-top:.7rem}'
       '.hero.hs-capoff .hs-cap{visibility:hidden!important}'
       # 8:06 PM: the taller plumes rise behind the title: a soft dark scrim + tighter shadow keep the text >= 4.5:1
       '.hero[data-hero=space] .hero-content{background:radial-gradient(closest-side,rgba(0,8,20,.42),rgba(0,8,20,.18) 70%,rgba(0,8,20,0))}'
       '.hero[data-hero=space] .hero-welcome,.hero[data-hero=space] .hero-kicker,.hero[data-hero=space] .hero-example,.hero[data-hero=space] .hero-email{text-shadow:0 0 3px rgba(0,0,0,.9),0 2px 18px rgba(0,0,0,.85)}'
       # Oct 17 2:13 PM (owner): title block centered horizontally and vertically over the hero scene (overlap OK).
       # Oct 17 6:15 PM (owner: 'so close... move it up half'): APPROVED HERO POSITION. One shared value, HERO_OFFSET (top of
       # this file) -> CSS var --hero-offset on .hero[data-hero], used by EVERY theme (space, earth, any future one), so
       # swapping backgrounds never moves the title. Base = flex-centered block with nav-room padding; the offset lifts it.
       '.hero[data-hero]{--hero-offset:' + HERO_OFFSET + ';display:flex!important;flex-direction:column;align-items:center!important;justify-content:center!important}'
       '.hero[data-hero] .hero-content{margin:auto!important;padding-top:calc(56px - var(--hero-offset));padding-bottom:calc(3.5rem + var(--hero-offset));position:relative;z-index:2}'
       '@media (min-width:1140px){.hero[data-hero] .hero-content{padding-top:calc(92px - var(--hero-offset));padding-bottom:calc(2rem + var(--hero-offset))}}'
       '.hero[data-hero] .hero-ctas{display:flex;flex-wrap:wrap;justify-content:center}'
       # Oct 17: space theme — title block top set by JS (--hero-block-top) so it sits centered between nav and horizon
       '.hero[data-hero=space]{justify-content:flex-start!important}'
       '.hero[data-hero=space] .hero-content{position:absolute;left:0;right:0;top:var(--hero-block-top,18%);margin:0 auto!important;padding-top:0!important;padding-bottom:1rem!important;width:min(46rem,62vw);max-width:46rem}'
       '@media (max-width:1100px){.hero[data-hero=space] .hero-content{width:min(46rem,88vw)}}'
       # Oct 16 7:36 PM: on phones the Help / Donate pill is ~13rem wide, so the credit keeps a wider gap (it may wrap to 2 lines).
       '@media (max-width:480px){.hero .hero-video-credit{max-width:calc(100% - 16rem)}}'
       '@media (prefers-reduced-motion:reduce){.hs-ground,.hs-cap,.hs-cap.on{transition:none;transform:none}}</style>')

def chooser():
    rot = ','.join(f"'{t}'" for t in ROTATION)
    return ('<script>(function(){var h=document.currentScript&&document.currentScript.closest(".hero");if(!h)return;'
            f'var T=[{rot}],K={{earth:"video",space:"canvas"}},n=Math.floor((Date.now()-{ANCHOR_UTC})/6048e5),'
            'name=T[(n%T.length+T.length)%T.length],m=/[?&]hero=([a-z-]+)/.exec(location.search);'
            'if(m&&K[m[1]])name=m[1];h.setAttribute("data-hero",name);'
            # the video ships inert (see lazy_video): only the video theme gives it its poster + source and starts it
            'var v=h.querySelector("video.hero-video");if(v){if(K[name]==="video"){if(v.dataset.poster)v.poster=v.dataset.poster;'
            '[].forEach.call(v.querySelectorAll("source[data-src]"),function(s){s.src=s.dataset.src});v.autoplay=true;v.load();'
            'var pp=v.play&&v.play();if(pp&&pp.catch)pp.catch(function(){})}else v.className="hero-video-off"}'
            '})();</script>')

def caps(l):
    import html as H
    a = ''.join(f'<a class="hs-cap{" on" if i == 0 else ""}" href="{CAP_HREF[i]}" data-scene="{i}"><span>{H.escape(t)}</span>'
                f'<span class="hs-arr" aria-hidden="true">→</span></a>' for i, t in enumerate(CAPS[l]))
    return f'<div class="hs-caps">{a}</div>'

def block(pre, l):
    return (f'<!-- HEROTHEME:START -->{CSS.replace("</style>", POSTER() + "</style>")}<div class="hero-space" aria-hidden="true" data-bm="{BM}"{TEXATTR()}{SATATTR()}></div>{caps(l)}{chooser()}'
            f'<script src="{pre}assets/hero-themes.js?v={JSV}" defer></script><!-- HEROTHEME:END -->')

# Oct 16 2026 (Lighthouse): the hero video (1.1 MB, HERO-VIDEO block from build-batch2.py) used to start downloading
# at parse time even in weeks when the space theme hides it. Ship it inert; chooser() activates it for the video theme.
def lazy_video(s):
    def fix(m):
        t = m.group(0)
        t = re.sub(r'(<video\b[^>]*?) autoplay(="[^"]*")?(?=[\s>])', r'\1', t)
        t = re.sub(r'(<video\b[^>]*?)\bpreload="[^"]*"', r'\1preload="none"', t)
        t = re.sub(r'(<video\b[^>]*?) poster="', r'\1 data-poster="', t)
        return re.sub(r'<source src="', '<source data-src="', t)
    return re.sub(r'<!-- HERO-VIDEO:START -->.*?<!-- HERO-VIDEO:END -->', fix, s, count=1, flags=re.S)

for l in LANGS:
    p = 'index.html' if l == 'en' else f'{l}/index.html'
    if not os.path.exists(p): continue
    s = open(p, encoding='utf8').read(); o = s
    b = block('' if l == 'en' else '../', l)
    pat = re.compile(r'<!-- HEROTHEME:START -->.*?<!-- HEROTHEME:END -->', re.S)
    if pat.search(s): s = pat.sub(lambda m: b, s, count=1)
    else:
        i = s.find('<!-- HERO-VIDEO:END -->')
        if i < 0: raise SystemExit(f'{p}: HERO-VIDEO block not found')
        i += len('<!-- HERO-VIDEO:END -->'); s = s[:i] + b + s[i:]
    s = lazy_video(s)
    if s != o: open(p, 'w', encoding='utf8').write(s)
    print(p, 'updated' if s != o else 'unchanged')
