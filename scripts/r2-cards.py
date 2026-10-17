#!/usr/bin/env python3
"""Oct 16 (user: fast, quality first): responsive sizes for card images built from the 1200x630 share cards (assets/og/<lang>/*.jpg):
  - homepage domain cards (.dom-img, written by build-ux.py mini())
  - Related Solutions cards (.rel-card, build-batch-a.py) on every page, all languages
  - Solutions.html directory cards (.sol-card .photo-link, added Oct 16 ~9:30 PM)
Uploads any card image not yet in assets/data/media-manifest.json to R2 with scripts/r2-upload.py --srcset (WebP q90 at
480/800/1200; the sources are 1200 px so nothing larger exists), then adds srcset/sizes to those <img> tags. The repo JPEG stays
the src fallback, untouched. Idempotent. Runs late in weekly-sync.sh (after i18n-build). Replaces r2-home-cards.py."""
import os, re, json, glob, subprocess, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
MF = 'assets/data/media-manifest.json'
SIZES = {'dom': '(max-width:700px) 92vw, (max-width:1100px) 46vw, 380px', 'rel': '(max-width:520px) 46vw, (max-width:900px) 30vw, 260px', 'sol': '(max-width:600px) 90vw, 260px'}
CARD = re.compile(r'(<a class="dom-img"[^>]*>|<li class="rel-card"><a [^>]*>|<article class="card sol-card"[^>]*><div class="image-container"><a class="photo-link"[^>]*>)(<img\b[^>]*>)')
SRC = re.compile(r'\ssrc="(?:\.\./)?(assets/og/([a-z]{2})/([^"?]+\.jpg))')
pages = sorted(glob.glob('*.html') + glob.glob('[a-z][a-z]/*.html'))
man = json.load(open(MF)) if os.path.exists(MF) else {}
todo = {}
for f in pages:
    for _, img in CARD.findall(open(f, encoding='utf8').read()):
        m = SRC.search(img)
        if m and f'images/og/{m.group(2)}/{m.group(3)}' not in man and os.path.exists(m.group(1)): todo.setdefault(m.group(2), set()).add(m.group(1))
for lang, files in sorted(todo.items()):
    files = sorted(files)
    for i in range(0, len(files), 25):
        subprocess.run([sys.executable, 'scripts/r2-upload.py', '--prefix', f'images/og/{lang}/', '--srcset', *files[i:i + 25]], check=True, stdout=subprocess.DEVNULL)
man = json.load(open(MF)) if os.path.exists(MF) else {}
n = 0
for f in pages:
    s = open(f, encoding='utf8').read()
    def fix(mm):
        a, img = mm.group(1), mm.group(2); m = SRC.search(img)
        e = man.get(f'images/og/{m.group(2)}/{m.group(3)}') if m else None
        if not e or not e.get('srcset') or 'srcset=' in img: return mm.group(0)
        return a + img.replace('<img', f'<img srcset="{e["srcset"]}" sizes="{SIZES["dom" if "dom-img" in a else "sol" if "sol-card" in a else "rel"]}"', 1)
    s2 = CARD.sub(fix, s)
    if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
print('r2-cards:', sum(map(len, todo.values())), 'images uploaded,', n, 'pages updated')
