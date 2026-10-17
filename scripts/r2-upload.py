#!/usr/bin/env python3
"""Oct 16 2026: upload full-resolution media to Cloudflare R2 (bucket savingplanets-media, served at https://media.savingplanets.com).
Runs on the box only. Reads the API token from /home/box/.cloudflare_token (never printed) and the account id from /home/box/.cloudflare_account_id.

Every object gets a content-hashed, versioned name (stem.<sha12>.ext), so it can be cached forever:
  Cache-Control: public, max-age=31536000, immutable
Re-uploading an unchanged file is a no-op (same name). A changed file gets a new name, so no cache purge is ever needed.
Results go into assets/data/media-manifest.json (keyed by "<prefix><original name>"), which the generators read.

Usage:
  python3 scripts/r2-upload.py --prefix videos/ path/to/clip.mp4 [...]
  python3 scripts/r2-upload.py --prefix images/ --srcset path/to/photo.jpg [...]
     --srcset: also make responsive WebP widths (480..3840, never upscaled, quality 90) and record a srcset string.
               Oct 16: also AVIF widths (quality 70, near-lossless visually) recorded as srcset_avif, plus width/height.
               The original file is uploaded untouched as the full-resolution master. Videos are never re-encoded.
  --dry-run   show what would be uploaded
Quality rule (owner): images and videos stay extra high-res. Don't recompress originals."""
import sys, os, json, hashlib, mimetypes, subprocess, argparse, urllib.request, urllib.error, io, tempfile

BUCKET = 'savingplanets-media'
PUBLIC = 'https://media.savingplanets.com/'
CACHE = 'public, max-age=31536000, immutable'
WIDTHS = [480, 800, 1280, 1920, 2560, 3840]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'assets', 'data', 'media-manifest.json')
TYPES = {'.mp4': 'video/mp4', '.m4v': 'video/mp4', '.webm': 'video/webm', '.mov': 'video/quicktime', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
         '.png': 'image/png', '.webp': 'image/webp', '.avif': 'image/avif', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.vtt': 'text/vtt; charset=utf-8',
         '.json': 'application/json', '.pdf': 'application/pdf', '.mp3': 'audio/mpeg', '.m4a': 'audio/mp4'}

def _tok(): return open('/home/box/.cloudflare_token').read().strip()
def _acc(): return open('/home/box/.cloudflare_account_id').read().strip()

def api(method, key, data=None, headers=None):
    url = f'https://api.cloudflare.com/client/v4/accounts/{_acc()}/r2/buckets/{BUCKET}/objects/{urllib.request.quote(key)}'
    h = {'Authorization': 'Bearer ' + _tok()}; h.update(headers or {})
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=600) as r: return r.status, r.read() if method != 'HEAD' else b''
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:300]

def exists(key):
    # Ask the R2 API, never the public URL: requesting a not-yet-uploaded key through media.savingplanets.com can leave a
    # cached 404 at the edge (it happened on Oct 16 while the custom domain was still being provisioned).
    url = f'https://api.cloudflare.com/client/v4/accounts/{_acc()}/r2/buckets/{BUCKET}/objects?prefix={urllib.request.quote(key)}'
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + _tok()})
    with urllib.request.urlopen(req, timeout=60) as r: res = json.loads(r.read()).get('result') or []
    return any(o.get('key') == key for o in res)

def ctype(path):
    ext = os.path.splitext(path)[1].lower()
    return TYPES.get(ext) or mimetypes.guess_type(path)[0] or 'application/octet-stream'

def put(key, data, ct, dry=False):
    if dry: print(f'  would upload {key} ({len(data)/1e6:.1f} MB, {ct})'); return
    if exists(key): print(f'  exists  {key}'); return
    st, body = api('PUT', key, data, {'Content-Type': ct, 'Cache-Control': CACHE})
    if st != 200: sys.exit(f'upload failed for {key}: HTTP {st} {body!r}')
    print(f'  uploaded {key} ({len(data)/1e6:.1f} MB)')

def probe(path):
    try:
        o = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration', '-of', 'json', path])
        j = json.loads(o); s = j['streams'][0]; d = float(j['format'].get('duration') or 0)
        return {'width': s['width'], 'height': s['height'], **({'duration': round(d, 2)} if d > 0.5 else {})}
    except Exception: return {}

def versioned(prefix, name, data):
    stem, ext = os.path.splitext(name)
    return f'{prefix}{stem}.{hashlib.sha256(data).hexdigest()[:12]}{ext.lower()}'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('files', nargs='+'); ap.add_argument('--prefix', default='media/')
    ap.add_argument('--srcset', action='store_true'); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args(); pre = a.prefix.strip('/') + '/'
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    for f in a.files:
        data = open(f, 'rb').read(); name = os.path.basename(f); key = versioned(pre, name, data); ct = ctype(f)
        print(name); put(key, data, ct, a.dry_run)
        e = {'url': PUBLIC + key, 'key': key, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'type': ct, **probe(f)}
        if a.srcset and ct.startswith('image/') and ct != 'image/svg+xml':
            from PIL import Image
            im = Image.open(f); im.load(); W = im.width; parts = []
            if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA' if 'A' in im.mode else 'RGB')
            for w in [x for x in WIDTHS if x < W] + [min(W, 3840)]:
                r = im if w == W else im.resize((w, round(im.height * w / W)), Image.LANCZOS)
                b = io.BytesIO(); r.save(b, 'WEBP', quality=90, method=6); b = b.getvalue()
                k = versioned(pre, f'{os.path.splitext(name)[0]}-{w}.webp', b); put(k, b, 'image/webp', a.dry_run)
                parts.append(f'{PUBLIC}{k} {w}w')
            e['srcset'] = ', '.join(dict.fromkeys(parts))
            e['width'], e['height'] = W, im.height
            av = []
            for w in [x for x in WIDTHS if x < W] + [min(W, 3840)]:
                r = im if w == W else im.resize((w, round(im.height * w / W)), Image.LANCZOS)
                b = io.BytesIO(); r.convert('RGB').save(b, 'AVIF', quality=70, speed=4); b = b.getvalue()
                k = versioned(pre, f'{os.path.splitext(name)[0]}-{w}.avif', b); put(k, b, 'image/avif', a.dry_run)
                av.append(f'{PUBLIC}{k} {w}w')
            e['srcset_avif'] = ', '.join(dict.fromkeys(av))
        man[pre + name] = e
    if not a.dry_run:
        os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
        json.dump(dict(sorted(man.items())), open(MANIFEST, 'w'), indent=1, ensure_ascii=False); open(MANIFEST, 'a').write('\n')
        print('manifest:', os.path.relpath(MANIFEST, ROOT))

if __name__ == '__main__': main()
