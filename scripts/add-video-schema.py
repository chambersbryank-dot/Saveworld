#!/usr/bin/env python3
"""Oct 14 2026: schema.org VideoObject JSON-LD (with transcript) for every page that has a <!-- VIDEO:START --> block, all langs. Idempotent."""
import re, json, os, subprocess, html, glob, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, 'scripts'); import media as MEDIA  # Oct 16: videos on R2; duration from the manifest, upload date from git history of the original path
SITE = 'https://www.savingplanets.com/'
def clean(s): return html.unescape(re.sub(r'<[^>]+>', ' ', s)).split() and ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', s)).split())
def upload(mp4):
    d = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%aI', '--', mp4], capture_output=True, text=True).stdout.split()
    return d[-1] if d else R2_ONLY.get(os.path.basename(mp4))
# Oct 18: videos uploaded straight to R2 (never committed under assets/videos/) have no git history; their upload dates live here
R2_ONLY = {'savingplanets-about-v4.mp4': '2026-10-18T01:00:00-10:00', 'savingplanets-about-v4-720.mp4': '2026-10-18T01:00:00-10:00', 'savingplanets-promo-v3-1920x1080.mp4': '2026-10-18T01:00:00-10:00',
           'savingplanets-promo-v3-1080x1920.mp4': '2026-10-18T01:00:00-10:00', 'savingplanets-promo-v4-final-1080x1920.mp4': '2026-10-18T17:10:20-10:00'}
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
    if name[:1].islower(): name = name[0].upper() + name[1:]  # Oct 16: 'Video: satelliti che…' -> 'Satelliti che…'
    ld = {'@context': 'https://schema.org', '@type': 'VideoObject', 'name': name, 'description': html.unescape(desc.group(1)) if desc else name,
          'contentUrl': src.group(1) if src.group(1).startswith('http') else SITE + src.group(1), 'inLanguage': lang, 'isFamilyFriendly': True,
          'publisher': {'@type': 'Organization', 'name': 'Saving Planets', 'url': SITE.rstrip('/')}, 'creditText': 'Created by SI and Biological SI Partner'}
    if poster: ld['thumbnailUrl'] = SITE + poster.group(1)
    e = MEDIA.by_url(src.group(1)); u = upload(MEDIA.orig_path(src.group(1)))
    d = f"PT{int(e['duration'] // 60)}M{int(round(e['duration'] % 60))}S" if e and e.get('duration') else dur(src.group(1))
    if u: ld['uploadDate'] = u
    if d: ld['duration'] = d
    if tr: ld['transcript'] = clean(re.sub(r'<summary>.*?</summary>', '', tr.group(1), flags=re.S))
    tag = '<script type="application/ld+json" id="sp-video-ld">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    t = re.sub(r'\n?<script (?:type="application/ld\+json" id="sp-video-ld"|id="sp-video-ld" type="application/ld\+json")>.*?</script>', '', s, flags=re.S)  # Oct 16: either attribute order (i18n-build reorders them; left a stale English copy on translated pages)
    t = t.replace('</head>', tag + '\n</head>', 1)
    if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
print(f'add-video-schema: {n} pages updated')
