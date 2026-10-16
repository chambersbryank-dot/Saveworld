#!/usr/bin/env python3
"""Oct 15 item 6: Liquid Glass hardening + flat icons.
Liquid Glass stays ONLY on primary action buttons (Explore All Solutions, See Solutions on the World Map,
Help/Donate, Ways to Help Donate/Join) and the nav / dropdown panels. Every other small icon/chip gets a
clean flat style tinted with the per-page --lg-solid variable (set by build-ux.py apply_tint), same size, no blur.
Adds @supports fallbacks and honours prefers-reduced-transparency / prefers-contrast. Idempotent (LG-HARDEN markers)."""
import re
GLASS_BTNS = '.hero-ctas .hero-cta,.wm-cta .btn,.nav-help a,.sticky-help,a.help-btn'
PANELS = 'body.toc-home nav,body.toc-sub nav,body.toc-home nav.scrolled,body.toc-sub nav.scrolled,.nav-sub,.dropdown-menu,body.toc-home .nav-links,body.toc-sub .nav-links'
FLAT = '.aud-icon,.eli10-icon,.share-btn,.nav-toggle,.edu-bubble.glass,.t-chip,.dt-btn'
CSS = f"""/* LG-HARDEN:START */
/* Flat icons: per-page tint, consistent size, no blur (overrides extras.css/edu.css glass) */
{FLAT}{{background:var(--lg-solid,#1d3f73) !important;-webkit-backdrop-filter:none !important;backdrop-filter:none !important;color:#fff !important;border:1px solid rgba(255,255,255,.28) !important;box-shadow:0 2px 6px rgba(0,0,0,.18) !important;background-image:none !important}}
.aud-icon,.eli10-icon{{width:2.75rem !important;height:2.75rem !important;border-radius:50% !important;font-size:1.2rem !important}}
.partner-cta .btn-nav::before{{width:2rem !important;height:2rem !important;border-radius:50% !important;font-size:1rem !important;background:rgba(255,255,255,.18) !important;-webkit-backdrop-filter:none !important;backdrop-filter:none !important;border:1px solid rgba(255,255,255,.35) !important;box-shadow:none !important;color:#fff !important}}
.nav-toggle{{border-radius:10px !important;min-width:44px;min-height:44px}}.nav-toggle span,nav.scrolled .nav-toggle span{{background:#fff !important}}
.t-chip,.dt-btn{{border-radius:999px !important;min-height:40px}}
.t-chip[aria-pressed=true]{{background:#fff !important;color:var(--lg-solid,#1d3f73) !important;border-color:#fff !important;font-weight:700}}
.edu-bubble.glass{{border-radius:18px !important}}
.edu-bubble.glass .lb-small{{color:rgba(255,255,255,.9) !important}}
.share-btn:hover,.share-btn:focus-visible,.dt-btn:hover,.dt-btn:focus-visible,.t-chip:hover,.edu-bubble.glass:hover{{filter:brightness(1.12)}}
.sx-slot,.az-nav,#actions .mission-block{{-webkit-backdrop-filter:none !important;backdrop-filter:none !important}}
html.dark .az-nav{{background:rgba(11,18,32,.95) !important}}.az-nav{{background:rgba(255,255,255,.96) !important}}
/* No backdrop-filter support: make glass surfaces opaque enough to read */
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){{
 body.toc-home nav,body.toc-sub nav{{background:rgba(0,20,40,.92) !important}}
 body.toc-home nav.scrolled,body.toc-sub nav.scrolled{{background:#fff !important}}
 .nav-sub,.dropdown-menu{{background:#fff !important}}html.dark .nav-sub{{background:#0f1b26 !important}}
 {GLASS_BTNS}{{background:var(--lg-solid,#1d3f73) !important}}
}}
/* User asked for less transparency, or more contrast: drop glass everywhere, solid colours */
@media (prefers-reduced-transparency:reduce),(prefers-contrast:more){{
 {PANELS},{GLASS_BTNS},.glass,#actions .mission-block{{-webkit-backdrop-filter:none !important;backdrop-filter:none !important}}
 body.toc-home nav,body.toc-sub nav{{background:#001428 !important}}
 body.toc-home nav.scrolled,body.toc-sub nav.scrolled{{background:#fff !important}}
 .nav-sub,.dropdown-menu{{background:#fff !important}}html.dark .nav-sub{{background:#0f1b26 !important}}
 {GLASS_BTNS}{{background:var(--lg-solid,#1d3f73) !important;background-image:none !important;color:#fff !important}}
 .glass,#actions .mission-block{{background:var(--glass-solid,#003755) !important;background-image:none !important}}
}}
@media (prefers-contrast:more){{
 {GLASS_BTNS},{FLAT}{{border:2px solid #fff !important;box-shadow:none !important}}
 .nav-sub,.dropdown-menu{{border:2px solid currentColor !important}}
}}
@media (forced-colors:active){{{GLASS_BTNS},{FLAT}{{border:1px solid ButtonText !important;forced-color-adjust:auto}}}}
/* LG-HARDEN:END */
"""
def main():
    p = 'styles.css'; s = open(p, encoding='utf8').read()
    n = re.sub(r'\n?/\* LG-HARDEN:START \*/.*?/\* LG-HARDEN:END \*/\n?', '', s, flags=re.S).rstrip('\n') + '\n' + CSS
    # pair every unprefixed backdrop-filter declaration in the site CSS with -webkit- (Safari/iPad)
    ch = 0
    for f in ['styles.css', 'extras.css', 'edu.css', 'batchb.css', 'batch-a.css', 'map.css', 'solutions.css']:
        src = n if f == p else open(f, encoding='utf8').read(); out = src
        def pair(m):
            blk = m.group(0)
            if 'backdrop-filter' not in blk or '-webkit-backdrop-filter' in blk: return blk
            return re.sub(r'(?<![-\w])backdrop-filter\s*:\s*([^;}]+)', r'-webkit-backdrop-filter:\1;backdrop-filter:\1', blk)
        out = re.sub(r'\{[^{}]*\}', pair, out)
        if f == p: n = out
        elif out != src: open(f, 'w', encoding='utf8').write(out); ch += 1
    if n != s: open(p, 'w', encoding='utf8').write(n); ch += 1
    print(f'build-glass: {ch} files')
if __name__ == '__main__': main()
