"""Oct 24 2026 (owner standard): every title banner is a slow multi-photo slideshow of topic-matched photos.
'Slow, but not boring slow': ~6 s per photo, 1.2 s crossfade, gentle visible zoom/pan (scale 1.0 -> 1.08).
Pure CSS. Slide 0 is the base layer (always painted, so the first frame is never black); slides 1..N-1 fade in on top in turn.
Each slide has its own credit that shows only while that photo is on screen. Pause button and prefers-reduced-motion
(static first photo, first credit only) are honoured. Used by apply-anim-banners.py."""
import html
D, F, Z = 6.0, 1.2, 1.08   # seconds per photo, crossfade seconds, end zoom
NMAX = 5

def _p(x, T): return f'{max(0.0, min(100.0, x / T * 100)):.3f}%'

def css():
    out = ['.pg-anim .spx-slide{position:absolute;inset:0;overflow:hidden;z-index:0}',
           '.pg-anim .spx-slide .spb-media img{animation:none;transform-origin:50% 50%}',
           '.pg-anim .spx-slide:not(.spx-0),.pg-anim .spx-cred:not(.spx-c0){opacity:0}',
           '.pg-anim.spb-paused .spx-slide,.pg-anim.spb-paused .spx-slide img,.pg-anim.spb-paused .spx-cred{animation-play-state:paused!important}',
           '@media (prefers-reduced-motion:reduce){.pg-anim .spx-slide,.pg-anim .spx-slide img,.pg-anim .spx-cred{animation:none!important}'
           '.pg-anim .spx-slide:not(.spx-0),.pg-anim .spx-cred:not(.spx-c0){display:none}.pg-anim .spx-cred.spx-c0{opacity:1!important}}']
    for n in range(2, NMAX + 1):
        T = n * D
        # base photo: zoom while visible, reset to 1.0 while fully covered by photo 1, then zoom again from the moment it is revealed
        out.append(f'@keyframes spx{n}z0{{0%{{transform:scale(1) translate3d(0,0,0)}}{_p(D+F,T)}{{transform:scale({Z}) translate3d(-1.5%,-1%,0)}}'
                   f'{_p(D+F+0.05,T)}{{transform:scale(1) translate3d(0,0,0)}}100%{{transform:scale(1) translate3d(0,0,0)}}}}')
        out.append(f'@keyframes spx{n}c0{{0%,{_p(D+F/2,T)}{{opacity:1}}{_p(D+F/2+0.01,T)},{_p(T-F/2-0.01,T)}{{opacity:0}}{_p(T-F/2,T)},100%{{opacity:1}}}}')
        out.append(f'.pg-anim.spx-n{n} .spx-0 img{{animation:spx{n}z0 {T:g}s linear infinite}}.pg-anim.spx-n{n} .spx-c0{{animation:spx{n}c0 {T:g}s linear infinite}}')
        for i in range(1, n):
            a, last = i * D, i == n - 1
            end = T if last else a + D + F          # last photo fades back to the base at the end of the cycle
            fade = (f'{_p(T-F,T)}{{opacity:1}}100%{{opacity:0}}' if last else f'{_p(end,T)}{{opacity:1}}{_p(end+0.01,T)},100%{{opacity:0}}')
            out.append(f'@keyframes spx{n}f{i}{{0%,{_p(a,T)}{{opacity:0}}{_p(a+F,T)}{{opacity:1}}{fade}}}')
            dx = '1.5%' if i % 2 else '-1.5%'
            out.append(f'@keyframes spx{n}z{i}{{0%,{_p(a,T)}{{transform:scale(1) translate3d(0,0,0)}}{_p(end,T)},100%{{transform:scale({Z}) translate3d({dx},-1%,0)}}}}')
            ce = T - F / 2 if last else a + D + F / 2
            out.append(f'@keyframes spx{n}c{i}{{0%,{_p(a+F/2-0.01,T)}{{opacity:0}}{_p(a+F/2,T)},{_p(ce,T)}{{opacity:1}}{_p(ce+0.01,T)},100%{{opacity:0}}}}')
            out.append(f'.pg-anim.spx-n{n} .spx-{i}{{animation:spx{n}f{i} {T:g}s linear infinite}}.pg-anim.spx-n{n} .spx-{i} img{{animation:spx{n}z{i} {T:g}s linear infinite}}'
                       f'.pg-anim.spx-n{n} .spx-c{i}{{animation:spx{n}c{i} {T:g}s linear infinite}}')
    return ''.join(out)
