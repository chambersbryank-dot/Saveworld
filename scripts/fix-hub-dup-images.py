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
# Oct 23 (founder): the other hubs (Oceans, Rivers, Polar, Forests, Earth Observation) repeated card photos too. Each repeat now gets
# its own free-to-use photo from a public agency (NASA, ESA, NOAA, USFWS, USGS, NPS, BLM, US Forest Service), listed in
# assets/data/hub-agency-images.json with the source page, licence and the agency's exact credit line. The full-resolution master is
# on R2 (images/hub/, untouched; WebP srcset from media-manifest.json); assets/hub/<stem>.jpg is the 1920 px repo fallback.
# The card gets 'Image: <credit>' (localized through the 'Image: {x}' i18n template, like the homepage Saturn credit) and never the
# SI tag (scripts/si-credits.py lists these stems in REAL_PHOTOS). Alt text + credit translations are written to i18n/<lang>.json
# here so i18n-build.py carries them to fr/es/ar/it/he. Idempotent.
import json, html as _html
AG = json.load(open('assets/data/hub-agency-images.json', encoding='utf8'))
MAN = json.load(open('assets/data/media-manifest.json', encoding='utf8'))
SIZES = '(max-width:600px) 92vw, (max-width:1100px) 46vw, 380px'
def _master(stem):
    for k, v in MAN.items():
        if k.startswith('images/hub/' + stem + '.'): return v
    return {}
def _img(e):
    from PIL import Image
    f = f"assets/hub/{e['stem']}.jpg"; w, h = Image.open(f).size
    m = _master(e['stem']); ss = f' srcset="{m["srcset"]}" sizes="{SIZES}"' if m.get('srcset') else ''
    return f'<img src="{f}"{ss} alt="{_html.escape(e["alt"]["en"])}" width="{w}" height="{h}" loading="lazy" decoding="async">'
def _credit(e): return f'<p class="photo-credit agency-credit">Image: {_html.escape(e["credit"], quote=False)}</p>'
for e in AG:
    for hub in e['hubs']:
        s = open(hub, encoding='utf8').read(); o = s
        rx = re.compile(r'(<div class="image-container"><a class="photo-link" href="' + re.escape(e['card']) + r'">)<img [^>]*>(?:<span class="si-credit">[^<]*</span>)?(</a></div>)(?:<p class="photo-credit agency-credit">[^<]*</p>)?')
        s = rx.sub(lambda m: m.group(1) + _img(e) + m.group(2) + _credit(e), s, count=1)
        if s != o: open(hub, 'w', encoding='utf8').write(s); print('hub-agency-images:', hub, e['card'], '->', e['stem'])
# translation memory: alt text + localized credit line
for L in ('fr', 'es', 'ar', 'it', 'he'):
    p = f'i18n/{L}.json'; mem = json.load(open(p, encoding='utf8')); n = 0
    tpl = mem.get('Image: {x}', 'Image: {x}')
    for e in AG:
        for k, v in ((e['alt']['en'], e['alt'][L]), ('Image: ' + e['credit'], tpl.replace('{x}', e['credit']))):
            if mem.get(k) != v: mem[k] = v; n += 1
    if n: json.dump(mem, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0); print(f'hub-agency-images: {p} +{n}')
for hub in ('Oceans.html', 'Rivers.html', 'Lakes.html', 'Polar.html', 'Deforestation.html', 'Earth_Observation.html', 'Space.html'):
    if not os.path.exists(hub): continue
    s = open(hub, encoding='utf8').read()
    c = collections.Counter(re.sub(r'[?.][0-9a-f]{12}\.|\?.*', '.', m) for m in re.findall(r'<a class="photo-link" href="[^"]+"><img [^>]*src="([^"]+)"', s))
    d = [k for k, v in c.items() if v > 1]
    if d: print('hub-dup-images WARNING', hub, d)
