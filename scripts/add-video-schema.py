#!/usr/bin/env python3
"""Oct 14 2026: schema.org VideoObject JSON-LD (with transcript) for every page that has a <!-- VIDEO:START --> block, all langs. Idempotent."""
import re, json, os, subprocess, html, glob
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
SITE = 'https://www.savingplanets.com/'
def clean(s): return html.unescape(re.sub(r'<[^>]+>', ' ', s)).split() and ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).split())
def upload(mp4):
    d = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%aI', '--', mp4], capture_output=True, text=True).stdout.split()
    return d[-1] if d else None
def dur(mp4):
    try:
        s = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4], capture_output=True, text=True).stdout.strip())
        return f'PT{int(s // 60)}M{int(round(s % 60))}S'
    except Exception: return None
n = 0
for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
    if f.startswith('pagefind'): continue
    s = open(f, encoding='utf-8').read()
    m = re.search(r'<!-- VIDEO:START -->(.*?)<!-- VIDEO:END -->', s, re.S)
    if not m: continue
    b = m.group(1)
    src = re.search(r'<source[^>]*src="(?:\.\./)?([^"]+\.mp4)"', b); poster = re.search(r'poster="(?:\.\./)?([^"]+)"', b)
    h2 = re.search(r'<h2[^>]*>(.*?)</h2>', b, re.S)
    if not (src and h2): continue
    lang = (re.search(r'<html[^>]*lang="([a-z]{2})', s) or [None, 'en'])[1]
    tr = re.search(r'<details class="video-transcript">(.*?)</details>', b, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    name = re.sub(r'^[^:：]{2,12}[:：]\s*', '', clean(h2.group(1)))
    ld = {'@context': 'https://schema.org', '@type': 'VideoObject', 'name': name, 'description': html.unescape(desc.group(1)) if desc else name,
          'contentUrl': SITE + src.group(1), 'inLanguage': lang, 'isFamilyFriendly': True,
          'publisher': {'@type': 'Organization', 'name': 'Saving Planets', 'url': SITE.rstrip('/')}, 'creditText': 'Created by SI and Biological SI Partner'}
    if poster: ld['thumbnailUrl'] = SITE + poster.group(1)
    u = upload(src.group(1)); d = dur(src.group(1))
    if u: ld['uploadDate'] = u
    if d: ld['duration'] = d
    if tr: ld['transcript'] = clean(re.sub(r'<summary>.*?</summary>', '', tr.group(1), flags=re.S))
    tag = '<script type="application/ld+json" id="sp-video-ld">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    t = re.sub(r'\n?<script type="application/ld\+json" id="sp-video-ld">.*?</script>', '', s, flags=re.S)
    t = t.replace('</head>', tag + '\n</head>', 1)
    if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
print(f'add-video-schema: {n} pages updated')
