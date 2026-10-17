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
import re, os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
LANGS = ['en', 'fr', 'es', 'ar', 'it']
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
}
CAP_HREF = ('Space.html', 'Artemis_II.html')  # no Enceladus page yet -> Space hub; Earthrise -> Artemis II (crewed flight around the Moon)

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
       '@media (prefers-reduced-motion:reduce){.hs-ground,.hs-cap,.hs-cap.on{transition:none;transform:none}}</style>')

def chooser():
    rot = ','.join(f"'{t}'" for t in ROTATION)
    return ('<script>(function(){var h=document.currentScript&&document.currentScript.closest(".hero");if(!h)return;'
            f'var T=[{rot}],K={{earth:"video",space:"canvas"}},n=Math.floor((Date.now()-{ANCHOR_UTC})/6048e5),'
            'name=T[(n%T.length+T.length)%T.length],m=/[?&]hero=([a-z-]+)/.exec(location.search);'
            'if(m&&K[m[1]])name=m[1];h.setAttribute("data-hero",name);'
            'if(K[name]!=="video"){var v=h.querySelector("video.hero-video");if(v){v.removeAttribute("autoplay");v.preload="none";'
            'v.removeAttribute("poster");v.className="hero-video-off";[].forEach.call(v.querySelectorAll("source"),function(s){s.remove()});v.load()}}'
            '})();</script>')

def caps(l):
    import html as H
    a = ''.join(f'<a class="hs-cap{" on" if i == 0 else ""}" href="{CAP_HREF[i]}" data-scene="{i}"><span>{H.escape(t)}</span>'
                f'<span class="hs-arr" aria-hidden="true">→</span></a>' for i, t in enumerate(CAPS[l]))
    return f'<div class="hs-caps">{a}</div>'

def block(pre, l):
    return (f'<!-- HEROTHEME:START -->{CSS}<div class="hero-space" aria-hidden="true"></div>{caps(l)}{chooser()}'
            f'<script src="{pre}assets/hero-themes.js?v={JSV}" defer></script><!-- HEROTHEME:END -->')

for l in LANGS:
    p = 'index.html' if l == 'en' else f'{l}/index.html'
    s = open(p, encoding='utf8').read(); o = s
    b = block('' if l == 'en' else '../', l)
    pat = re.compile(r'<!-- HEROTHEME:START -->.*?<!-- HEROTHEME:END -->', re.S)
    if pat.search(s): s = pat.sub(lambda m: b, s, count=1)
    else:
        i = s.find('<!-- HERO-VIDEO:END -->')
        if i < 0: raise SystemExit(f'{p}: HERO-VIDEO block not found')
        i += len('<!-- HERO-VIDEO:END -->'); s = s[:i] + b + s[i:]
    if s != o: open(p, 'w', encoding='utf8').write(s)
    print(p, 'updated' if s != o else 'unchanged')
