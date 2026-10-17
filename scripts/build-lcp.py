#!/usr/bin/env python3
"""Oct 16 (user quick win): pages whose LCP is the CSS background of <section class="page-hero [hero-x]"> get a high-priority
preload of the same WebP the stylesheet picks (800 px up to 800 px wide, 1600 px above, matching styles.css). Only the shared
hero classes are covered; space-hero pages have per-page images in the stylesheet and are left as they are. Marker LCPPRE
(ignored by the i18n hash). All languages. Run late in weekly-sync.sh (after i18n-build)."""
import os, re, glob
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
KNOWN = {'hero-kids': 'kids', 'hero-satx': 'satx', 'hero-lesson': 'lesson', 'hero-teach': 'teach', 'hero-about': 'about', 'hero-help': 'help',
         'hero-learn': 'learn', 'hero-mission': 'mission', 'hero-ocean': 'ocean'}
n = 0
for f in glob.glob('*.html') + glob.glob('[a-z][a-z]/*.html'):
    s = open(f, encoding='utf8').read()
    s0 = re.sub(r'<!-- LCPPRE:START -->.*?<!-- LCPPRE:END -->', '', s, flags=re.S)
    m = re.search(r'<section class="page-hero((?: [\w-]+)*)"', s0)
    blk = ''
    if m:
        cls = m.group(1).split()
        stem = next((KNOWN[c] for c in cls if c in KNOWN), None)
        if stem is None and not cls: stem = 'ocean'          # plain .page-hero = ocean image
        if stem:
            pre = '../' if '/' in f else ''
            blk = (f'<!-- LCPPRE:START --><link rel="preload" as="image" type="image/webp" href="{pre}assets/hero/{stem}-800.webp" media="(max-width: 800px)" fetchpriority="high">'
                   f'<link rel="preload" as="image" type="image/webp" href="{pre}assets/hero/{stem}-1600.webp" media="(min-width: 801px)" fetchpriority="high"><!-- LCPPRE:END -->')
    s2 = s0.replace('</head>', blk + '</head>', 1) if blk else s0
    if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
print('build-lcp:', n, 'pages')
