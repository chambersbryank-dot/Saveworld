#!/usr/bin/env python3
"""Oct 22 (founder): Lakes hub showed the same photo twice (Keep Tahoe Blue + Living Lakes both Lake_Tahoe_ISS,
Adopt-a-Beach + Lake Erie forecast both Great_Lakes_GSFC). Swap the second card of each pair to a different real,
credited photo already in assets/. English source; translations follow via i18n-build. Idempotent; reports any
other hub page that still repeats a card image."""
import os, re, glob, collections
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
SWAP = {  # (hub page, solution card href): (new src, w, h, alt)
 ('Lakes.html', 'Living_Lakes.html'): ('assets/NZ_Southern_Lakes_ISS_2024.jpg', 1920, 1280,
   'Lakes Tekapo, Pukaki and Ōhau, bright blue among snowy mountains near the Southern Alps of New Zealand, seen from the International Space Station'),
 ('Lakes.html', 'Alliance_for_the_Great_Lakes_Adopt_a_Beach.html'): ('assets/Lake_Shore_Cleanup_NPS.jpg', 1200, 900,
   'A volunteer in a life vest pulling trash from a shoreline into a canoe'),
}
for (hub, href), (src, w, h, alt) in SWAP.items():
    s = open(hub, encoding='utf8').read()
    rx = re.compile(r'(<a class="photo-link" href="' + re.escape(href) + r'">)<img [^>]*>')
    s2 = rx.sub(lambda m: m.group(1) + f'<img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">', s, count=1)
    if s2 != s and src not in rx.search(s).group(0): open(hub, 'w', encoding='utf8').write(s2); print('hub-dup-images:', hub, href, '->', src)
for hub in ('Oceans.html', 'Rivers.html', 'Lakes.html', 'Polar.html', 'Deforestation.html', 'Earth_Observation.html', 'Space.html'):
    if not os.path.exists(hub): continue
    s = open(hub, encoding='utf8').read()
    c = collections.Counter(re.sub(r'[?.][0-9a-f]{12}\.|\?.*', '.', m) for m in re.findall(r'<a class="photo-link" href="[^"]+"><img [^>]*src="([^"]+)"', s))
    d = [k for k, v in c.items() if v > 1]
    if d: print('hub-dup-images WARNING', hub, d)
