"""Oct 16 2026: full-resolution media lives on Cloudflare R2 (https://media.savingplanets.com), not in the repo.
assets/data/media-manifest.json (written by scripts/r2-upload.py) maps "videos/<original name>" to its versioned public URL
plus width/height/duration, so generators never need the file locally. Posters (.jpg/.webp) stay in assets/videos/."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(ROOT, 'assets', 'data', 'media-manifest.json'), encoding='utf-8'))
def video(name):
    """name like 'hero-loop.mp4' -> manifest entry (url, width, height, duration, ...)"""
    return M['videos/' + name]
def vurl(name): return video(name)['url']
def dims(name): e = video(name); return e['width'], e['height']
# matches a video reference old (assets/videos/x.mp4) or new (media.savingplanets.com/videos/x.<hash10>.mp4); group 1 = slug
VID_RE = r'(?:assets|media\.savingplanets\.com)/videos/([\w-]+?)(?:\.[0-9a-f]{8,16})?\.mp4'
def by_url(u):
    """public URL or repo path -> manifest entry (or None)"""
    for k, e in M.items():
        if e['url'] == u or u.endswith('assets/' + k): return e
    return None
def orig_path(u):
    for k, e in M.items():
        if e['url'] == u: return 'assets/' + k
    return u
