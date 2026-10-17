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

CSS = ('<style>.hero .hero-space{display:none}.hero[data-hero=space] .hero-media{display:none}'
       '.hero[data-hero=space] .hero-space{display:block;position:absolute;inset:0;z-index:-1;overflow:hidden;contain:strict;'
       'background:radial-gradient(120% 90% at 30% 22%,#0c2c4d 0%,#05132a 42%,#01050d 100%)}'
       '.hs-layer{position:absolute;left:0;top:0;pointer-events:none;will-change:transform;backface-visibility:hidden}'
       '.hs-neb{left:-8%!important;top:-8%!important;width:116%;height:116%;opacity:0;transition:opacity 1.8s ease}'
       '.hs-ready .hs-neb{opacity:.88}'
       '.hero-space::after{content:"";position:absolute;inset:0;pointer-events:none;'
       'background:radial-gradient(60% 46% at 50% 50%,rgba(1,6,16,.62) 0%,rgba(1,6,16,.38) 55%,rgba(1,6,16,0) 100%),'
       'linear-gradient(180deg,rgba(0,20,40,.45) 0%,rgba(0,20,40,0) 22%,rgba(0,20,40,0) 78%,rgba(0,20,40,.55) 100%)}'
       '.hero[data-hero=space] .hero-welcome,.hero[data-hero=space] .hero-kicker{text-shadow:0 2px 18px rgba(0,0,0,.75)}'
       # Oct 16 7:05 PM: SI credit at the hero's inline-start corner (bottom-left LTR, bottom-right RTL), away from the
       # floating Help / Donate button (.sticky-help sits at inset-inline-end), on a dark pill so it reads on any frame.
       '.hero .hero-video-credit{right:auto;left:auto;inset-inline-start:.8rem;inset-inline-end:auto;bottom:.75rem;z-index:1;'
       'max-width:calc(100% - 13rem);padding:.22rem .6rem;border-radius:999px;background:rgba(0,10,22,.74);'
       'color:rgba(255,255,255,.94);font-size:.75rem;line-height:1.3;text-shadow:none}'
       '@media (prefers-reduced-motion:reduce){.hs-neb{transition:none}}</style>')

def chooser():
    rot = ','.join(f"'{t}'" for t in ROTATION)
    return ('<script>(function(){var h=document.currentScript&&document.currentScript.closest(".hero");if(!h)return;'
            f'var T=[{rot}],K={{earth:"video",space:"canvas"}},n=Math.floor((Date.now()-{ANCHOR_UTC})/6048e5),'
            'name=T[(n%T.length+T.length)%T.length],m=/[?&]hero=([a-z-]+)/.exec(location.search);'
            'if(m&&K[m[1]])name=m[1];h.setAttribute("data-hero",name);'
            'if(K[name]!=="video"){var v=h.querySelector("video.hero-video");if(v){v.removeAttribute("autoplay");v.preload="none";'
            'v.removeAttribute("poster");v.className="hero-video-off";[].forEach.call(v.querySelectorAll("source"),function(s){s.remove()});v.load()}}'
            '})();</script>')

def block(pre):
    return (f'<!-- HEROTHEME:START -->{CSS}<div class="hero-space" aria-hidden="true"></div>{chooser()}'
            f'<script src="{pre}assets/hero-themes.js?v={JSV}" defer></script><!-- HEROTHEME:END -->')

for l in LANGS:
    p = 'index.html' if l == 'en' else f'{l}/index.html'
    s = open(p, encoding='utf8').read(); o = s
    b = block('' if l == 'en' else '../')
    pat = re.compile(r'<!-- HEROTHEME:START -->.*?<!-- HEROTHEME:END -->', re.S)
    if pat.search(s): s = pat.sub(lambda m: b, s, count=1)
    else:
        i = s.find('<!-- HERO-VIDEO:END -->')
        if i < 0: raise SystemExit(f'{p}: HERO-VIDEO block not found')
        i += len('<!-- HERO-VIDEO:END -->'); s = s[:i] + b + s[i:]
    if s != o: open(p, 'w', encoding='utf8').write(s)
    print(p, 'updated' if s != o else 'unchanged')
