#!/usr/bin/env python3
"""Oct 16 (user quick win): responsive sizes for the homepage domain-card images. Finds the card images (assets/og/<lang>/*.jpg)
used by .dom-img on each language's index.html and uploads any not yet in assets/data/media-manifest.json to R2 with
scripts/r2-upload.py --srcset (WebP q90 at 480/800/1200, original JPEG stays in the repo as the src fallback, untouched).
build-ux.py mini() then writes srcset/sizes from the manifest. Run after build-ux.py, then build-ux.py again (weekly-sync.sh)."""
import os, re, json, subprocess, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
man = json.load(open('assets/data/media-manifest.json')) if os.path.exists('assets/data/media-manifest.json') else {}
todo = {}
for l in ['en', 'fr', 'es', 'ar', 'it']:
    f = 'index.html' if l == 'en' else l + '/index.html'
    for src in re.findall(r'<a class="dom-img"[^>]*><img[^>]*\ssrc="(?:\.\./)?(assets/og/[a-z]{2}/[^"?]+)', open(f, encoding='utf8').read()):
        lang = src.split('/')[2]
        if f'images/og/{lang}/{os.path.basename(src)}' not in man and os.path.exists(src): todo.setdefault(lang, set()).add(src)
for lang, files in sorted(todo.items()):
    subprocess.run([sys.executable, 'scripts/r2-upload.py', '--prefix', f'images/og/{lang}/', '--srcset', *sorted(files)], check=True, stdout=subprocess.DEVNULL)
print('r2-home-cards:', sum(map(len, todo.values())), 'card images uploaded')
