"""Oct 18 2026: shared animated page banner (owner: "WOW" opener, smooth on iPad Safari, legible title).
Used by build-top-ten.py; any generator can import it (Solutions.html worker: same component, same CSS block).
- Photo: a high-res original on R2 (assets/data/media-manifest.json entry with srcset/srcset_avif up to 3840 w); the master
  itself is never recompressed. The browser picks the right size (phones get 800-1280 w, iPad/Mac retina 2560-3840 w).
- Motion: CSS only, transform/opacity on composited layers (no JS, no video, no layout work): a slow 4K drift/zoom of the
  photo plus a soft light sweep. prefers-reduced-motion: completely static. Fixed min-height, so no layout shift.
Markup: banner(manifest_entry, alt, h1, sub, credit, h1_id[, pause=True: pause button for the CSS drift]) -> <section class="sp-anim-banner">...</section>
Oct 18 (Solutions.html): optional keyword args, all backwards compatible: h1_html / credit_html (pre-escaped markup, e.g. the live
count in its own span so translations never contain the number), sec_id, and video=[[width, url], ...] (R2 renditions of one
loop, smallest first). With a video, the photo is its frame-0 poster: no drift/sweep (so the hand-off is seamless), and VIDEO_JS
picks the rendition for the banner's rendered size x DPR (phones capped at 1920 w), plays only while on screen, and never
loads under prefers-reduced-motion or Save-Data (the poster stays).
CSS: CSS (written once into styles.css between /* SP-BANNER:START */ markers by write_css())."""
import html, re, json

def _e(x): return html.escape(x, quote=False).replace('"', '&quot;')

def _w(srcset, w):
    for part in (srcset or '').split(','):
        b = part.split()
        if len(b) == 2 and b[1] == f'{w}w': return b[0]
    return ''

def picture(e, alt, sizes='100vw'):
    srcs = ''.join(f'<source type="image/{t}" srcset="{_e(e[k])}" sizes="{sizes}">' for t, k in (('avif', 'srcset_avif'), ('webp', 'srcset')) if e.get(k))
    src = e['url'] if not e['url'].lower().endswith('.png') else (_w(e.get('srcset'), 1920) or e['url'])  # never the PNG master as the fallback
    return (f'<picture class="spb-media">{srcs}<img src="{src}" alt="{_e(alt)}" width="{e["width"]}" height="{e["height"]}" '
            f'fetchpriority="high" decoding="async"></picture>')

# WCAG 2.2.2: moving content longer than 5 s gets a pause control (same label as the Project Rawane banner, already translated)
PAUSE_BTN = '<button type="button" class="spb-pause" aria-pressed="false" aria-label="Pause banner animation">&#10074;&#10074;</button>'
VIDEO_JS = ("<script>(function(){document.querySelectorAll('.sp-anim-banner video[data-srcs]').forEach(function(v){var b=v.closest('.sp-anim-banner');"
    "var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)'),c=navigator.connection;if((rm&&rm.matches)||(c&&c.saveData))return;"
    "var s=JSON.parse(v.getAttribute('data-srcs')),r=b.getBoundingClientRect(),ar=v.videoWidth&&v.videoHeight?v.videoWidth/v.videoHeight:+(v.getAttribute('data-ar')||2.34),"
    "need=Math.max(r.width,r.height*ar)*Math.min(window.devicePixelRatio||1,2),u=s[s.length-1][1];if(innerWidth<=760)need=Math.min(need,1920);"
    "for(var i=0;i<s.length;i++){if(s[i][0]>=need*0.92){u=s[i][1];break}}v.src=u;"
    "v.addEventListener('playing',function(){b.classList.add('is-playing')},{once:true});var held=false,btn=b.querySelector('.spb-pause');"
    "var p=function(){if(held)return;var q=v.play();q&&q.catch&&q.catch(function(){})};"
    "btn&&btn.addEventListener('click',function(){held=btn.getAttribute('aria-pressed')!=='true';btn.setAttribute('aria-pressed',held);btn.innerHTML=held?'&#9654;':'&#10074;&#10074;';held?v.pause():p()});"
    "if('IntersectionObserver' in window){new IntersectionObserver(function(e){e[0].isIntersecting?p():v.pause()}).observe(b)}else p();"
    "rm&&rm.addEventListener&&rm.addEventListener('change',function(e){if(e.matches){v.pause();b.classList.remove('is-playing')}})})})();</script>")

# Oct 18 (Top Ten): pause=True on a photo banner (no video) shows the same pause button; it freezes the CSS drift/sweep
PAUSE_JS = ("<script>(function(){document.querySelectorAll('.sp-anim-banner.has-pause .spb-pause').forEach(function(btn){var b=btn.closest('.sp-anim-banner');"
    "btn.addEventListener('click',function(){var held=btn.getAttribute('aria-pressed')!=='true';btn.setAttribute('aria-pressed',held);"
    "btn.innerHTML=held?'&#9654;':'&#10074;&#10074;';b.classList.toggle('spb-paused',held)})})})();</script>")

def banner(e, alt, h1, sub, credit, h1_id='spb-h', extra_class='', h1_html=None, credit_html=None, sec_id=None, video=None, video_ar=None, pause=False):
    pause = pause and not video  # a video banner always has its own pause button
    cls = 'sp-anim-banner' + (' has-video' if video else '') + (' has-pause' if pause else '') + ((' ' + extra_class) if extra_class else '')
    vid = (f'<video class="spb-video" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1" disablepictureinpicture'
           + (f' data-ar="{video_ar}"' if video_ar else '') + f' data-srcs="{_e(json.dumps(video))}"></video>') if video else ''
    sizes = f'(max-aspect-ratio: 1/1) {round(100 * (video_ar or 2.34) * 0.4)}vh, 100vw' if video else '100vw'
    return (f'<section class="{cls}"' + (f' id="{sec_id}"' if sec_id else '') + f' aria-labelledby="{h1_id}">{picture(e, alt, sizes)}{vid}'
            + ('' if video else '<span class="spb-sweep" aria-hidden="true"></span>')
            + f'<div class="spb-text"><h1 id="{h1_id}">{h1_html if h1_html is not None else _e(h1)}</h1>' + (f'<p>{_e(sub)}</p>' if sub else '') + '</div>'
            f'<span class="spb-credit">{credit_html if credit_html is not None else _e(credit)}</span>'
            + (PAUSE_BTN if (video or pause) else '') + '</section>' + (VIDEO_JS if video else '') + (PAUSE_JS if pause else ''))

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
 '.sp-anim-banner .spb-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;opacity:0;transition:opacity 1.2s ease}'
 '.sp-anim-banner.is-playing .spb-video{opacity:1}'
 '.sp-anim-banner.has-video .spb-media img{animation:none;transform:none;will-change:auto}'
 '.sp-anim-banner .spb-credit span{unicode-bidi:isolate}'
 '.sp-anim-banner .spb-pause{position:absolute;z-index:2;left:.6rem;bottom:.4rem;width:2.75rem;height:2.75rem;border-radius:50%;border:1px solid rgba(255,255,255,.45);'
 'background:rgba(2,6,12,.45);color:#fff;font-size:.8rem;line-height:1;cursor:pointer;display:none}'
 '.sp-anim-banner.is-playing .spb-pause,.sp-anim-banner .spb-pause[aria-pressed=true]{display:block}'
 '.sp-anim-banner .spb-pause:focus-visible{outline:2px solid #4da3ff;outline-offset:2px}'
 '[dir=rtl] .sp-anim-banner .spb-pause{left:auto;right:.6rem}'
 '.sp-anim-banner.has-pause .spb-pause{display:block}.sp-anim-banner.spb-paused .spb-media img,.sp-anim-banner.spb-paused .spb-sweep{animation-play-state:paused}'
 '@media (prefers-reduced-motion:reduce){.sp-anim-banner .spb-video,.sp-anim-banner .spb-pause{display:none !important}}'
 '@media (prefers-reduced-motion:reduce){.sp-anim-banner .spb-media img,.sp-anim-banner .spb-sweep,.sp-anim-banner h1,.sp-anim-banner .spb-text p{animation:none !important}.sp-anim-banner .spb-sweep{display:none}}')

def write_css(path='styles.css'):
    s = open(path, encoding='utf-8').read()
    s2 = re.sub(r'\n?/\* SP-BANNER:START \*/.*?/\* SP-BANNER:END \*/\n?', '\n', s, flags=re.S).rstrip('\n') + '\n/* SP-BANNER:START */\n' + CSS + '\n/* SP-BANNER:END */\n'
    if s2 != s: open(path, 'w', encoding='utf-8').write(s2); return 1
    return 0
