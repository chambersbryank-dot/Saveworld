"""Oct 18 2026: shared animated page banner (owner: "WOW" opener, smooth on iPad Safari, legible title).
Used by build-top-ten.py; any generator can import it (Solutions.html worker: same component, same CSS block).
- Photo: a high-res original on R2 (assets/data/media-manifest.json entry with srcset/srcset_avif up to 3840 w); the master
  itself is never recompressed. The browser picks the right size (phones get 800-1280 w, iPad/Mac retina 2560-3840 w).
- Motion: CSS only, transform/opacity on composited layers (no JS, no video, no layout work): a slow 4K drift/zoom of the
  photo plus a soft light sweep. prefers-reduced-motion: completely static. Fixed min-height, so no layout shift.
Markup: banner(manifest_entry, alt, h1, sub, credit, h1_id) -> <section class="sp-anim-banner">...</section>
CSS: CSS (written once into styles.css between /* SP-BANNER:START */ markers by write_css())."""
import html, re

def _e(x): return html.escape(x, quote=False).replace('"', '&quot;')

def picture(e, alt):
    srcs = ''.join(f'<source type="image/{t}" srcset="{_e(e[k])}" sizes="100vw">' for t, k in (('avif', 'srcset_avif'), ('webp', 'srcset')) if e.get(k))
    return (f'<picture class="spb-media">{srcs}<img src="{e["url"]}" alt="{_e(alt)}" width="{e["width"]}" height="{e["height"]}" '
            f'fetchpriority="high" decoding="async"></picture>')

def banner(e, alt, h1, sub, credit, h1_id='spb-h', extra_class=''):
    return (f'<section class="sp-anim-banner{(" " + extra_class) if extra_class else ""}" aria-labelledby="{h1_id}">{picture(e, alt)}'
            f'<span class="spb-sweep" aria-hidden="true"></span>'
            f'<div class="spb-text"><h1 id="{h1_id}">{_e(h1)}</h1>' + (f'<p>{_e(sub)}</p>' if sub else '') + '</div>'
            f'<span class="spb-credit">{_e(credit)}</span></section>')

CSS = ('.sp-anim-banner{position:relative;isolation:isolate;min-height:min(62vh,560px);display:flex;align-items:flex-end;overflow:hidden;background:#02060c;contain:paint}'
 '.sp-anim-banner .spb-media,.sp-anim-banner .spb-media img{position:absolute;inset:0;width:100%;height:100%}'
 '.sp-anim-banner .spb-media img{object-fit:cover;object-position:50% 38%;transform:scale(1.06);transform-origin:50% 45%;will-change:transform;backface-visibility:hidden;'
 'animation:spb-drift 34s ease-in-out infinite alternate}'
 '@keyframes spb-drift{0%{transform:scale(1.06) translate3d(0,0,0)}100%{transform:scale(1.16) translate3d(-2.2%,-1.6%,0)}}'
 '.sp-anim-banner .spb-sweep{position:absolute;inset:-10% -30%;z-index:0;pointer-events:none;mix-blend-mode:screen;opacity:.0;'
 'background:radial-gradient(38% 22% at 50% 52%,rgba(255,196,120,.55),rgba(255,160,80,.18) 45%,transparent 70%),radial-gradient(30% 18% at 50% 36%,rgba(140,210,255,.35),transparent 70%);'
 'will-change:transform,opacity;animation:spb-sweep 16s ease-in-out infinite}'
 '@keyframes spb-sweep{0%{transform:translate3d(-28%,0,0);opacity:0}25%{opacity:.85}50%{transform:translate3d(0,0,0);opacity:1}75%{opacity:.85}100%{transform:translate3d(28%,0,0);opacity:0}}'
 '.sp-anim-banner::after{content:"";position:absolute;inset:0;z-index:0;background:linear-gradient(180deg,rgba(2,6,12,0) 35%,rgba(2,6,12,.55) 70%,rgba(2,6,12,.92) 100%)}'
 '.sp-anim-banner .spb-text{position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:7rem 1.5rem 2.6rem;text-align:center;width:100%}'
 '.sp-anim-banner h1{margin:0;font-size:clamp(2rem,4.6vw,3.6rem);line-height:1.08;letter-spacing:-.01em;text-shadow:0 3px 18px rgba(0,0,0,.6);animation:spb-in 1.1s cubic-bezier(.2,.7,.2,1) both}'
 '.sp-anim-banner .spb-text p{margin:.8rem auto 0;max-width:640px;font-size:clamp(1rem,1.6vw,1.2rem);opacity:.95;animation:spb-in 1.1s .25s cubic-bezier(.2,.7,.2,1) both}'
 '@keyframes spb-in{from{opacity:0;transform:translate3d(0,14px,0)}to{opacity:1;transform:none}}'
 '.sp-anim-banner .spb-credit{position:absolute;z-index:1;right:.8rem;bottom:.45rem;font-size:.72rem;opacity:.75}[dir=rtl] .sp-anim-banner .spb-credit{right:auto;left:.8rem}'
 '@media (max-width:760px){.sp-anim-banner{min-height:52vh}}'
 '@media (prefers-reduced-motion:reduce){.sp-anim-banner .spb-media img,.sp-anim-banner .spb-sweep,.sp-anim-banner h1,.sp-anim-banner .spb-text p{animation:none !important}.sp-anim-banner .spb-sweep{display:none}}')

def write_css(path='styles.css'):
    s = open(path, encoding='utf-8').read()
    s2 = re.sub(r'\n?/\* SP-BANNER:START \*/.*?/\* SP-BANNER:END \*/\n?', '\n', s, flags=re.S).rstrip('\n') + '\n/* SP-BANNER:START */\n' + CSS + '\n/* SP-BANNER:END */\n'
    if s2 != s: open(path, 'w', encoding='utf-8').write(s2); return 1
    return 0
