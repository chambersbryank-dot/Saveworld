#!/usr/bin/env python3
"""Oct 15 item 7: a distinct og:image (1200x630 share card) for every page in all 5 languages.
Card = the page's own photo (its existing og:image, else the first content photo, else the logo) + the page title in that
page's language + savingplanets.com. If the photo is SI-generated (si-credits.py SI_IMAGES), the card itself carries the visible
credit 'Created by SI and Biological SI Partner' next to the image (never in meta tags). Writes assets/og/<lang>/<Page>.jpg and
points og:image / twitter:image (+ width/height) at it. Re-renders only when the visible card changes: photo, drawn title lines or SI credit (assets/og/manifest.json)."""
import re, os, json, glob, hashlib, html, importlib.util
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SITE = 'https://www.savingplanets.com/'; W, H = 1200, 630; LANGS = ['en', 'fr', 'es', 'ar', 'it']
spec = importlib.util.spec_from_file_location('sic', 'scripts/si-credits.py'); sic = importlib.util.module_from_spec(spec); spec.loader.exec_module(sic)
SKIP = re.compile(r'^(google[0-9a-f]+|404)\.html$')
LOGO = 'assets/SavePlanetLogo.jpg'
def font(l, size):
    f = ImageFont.truetype('assets/fonts/og/' + ('NotoSansArabic.ttf' if l == 'ar' else 'Montserrat.ttf'), size, layout_engine=ImageFont.Layout.RAQM)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    return f
def d(l): return '' if l == 'en' else l + '/'
def local(u):
    u = html.unescape(u).split('?')[0]
    for pre in (SITE, 'https://savingplanets.com/', '../', '/'):
        if u.startswith(pre): u = u[len(pre):]
    return u if os.path.isfile(u) and u.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) else None
def source(s):
    m = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    cur = local(m.group(1)) if m else None
    if cur and '/og/' not in cur and 'Logo' not in cur: return cur
    h = re.search(r'class="page-hero hero-([a-z0-9-]+)"', s)
    if h and os.path.exists(f'assets/hero/{h.group(1)}-1600.jpg'): return f'assets/hero/{h.group(1)}-1600.jpg'
    main = s[s.find('<main'):] if '<main' in s else s
    for im in re.finditer(r'<img\b[^>]*\bsrc="([^"]+)"', main):
        p = local(im.group(1))
        if p and 'Logo' not in p and 'logo' not in p and os.path.getsize(p) > 15000:
            try:
                with Image.open(p) as i:
                    if i.width >= 600: return p
            except Exception: pass
    m2 = re.search(r'url\([\'"]?((?:\.\./)?assets/[^\'")]+\.(?:jpe?g|png|webp))', s)
    if m2 and local(m2.group(1)): return local(m2.group(1))
    return cur if cur and '/og/' not in cur else LOGO
LANG_TAGS = {'Français', 'Español', 'بالعربية', 'Italiano', 'English', 'Saving Planets'}
def title(s):
    m = re.search(r'<meta property="og:title" content="([^"]+)"', s) or re.search(r'<title>([^<]+)</title>', s)
    t = html.unescape(m.group(1)).strip()
    parts = [x for x in re.split(r'\s+[|·•]\s+', t) if x.strip() not in LANG_TAGS]
    return ' | '.join(parts) if parts else t
def wrap(dr, text, f, maxw):
    words = text.split(); lines = []; cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if dr.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return [x for x in lines if x]
def layout(t, l, logo):
    """Font size and the (at most 3) lines actually drawn on the card: the card's visible text."""
    dr = ImageDraw.Draw(Image.new('RGB', (8, 8))); maxw = W - 2 * 60 - (420 if logo else 0); size = 64
    while True:
        f = font(l, size); lines = wrap(dr, t, f, maxw)
        if len(lines) <= 3 or size <= 40: break
        size -= 4
    return size, lines[:3]
def visible_key(src, t, l, si):
    """Oct 16: re-render only when what the card shows changes (photo bytes, drawn lines, SI credit),
    not when the title changes in ways the card never shows (beyond line 3, or a dropped brand suffix)."""
    size, lines = layout(t, l, src == LOGO)
    return hashlib.sha1(json.dumps([src, os.path.getsize(src), size, lines, si, l, 'v3'], ensure_ascii=False).encode()).hexdigest()[:12]
def render(src, t, l, si, out):
    im = Image.open(src).convert('RGB'); logo = src == LOGO
    if logo:
        bg = Image.new('RGB', (W, H), (0, 32, 58)); lg = im.copy(); lg.thumbnail((360, 360)); bg.paste(lg, ((W - lg.width) // 2 if False else 70, (H - lg.height) // 2 - 40)); im = bg
    else:
        r = max(W / im.width, H / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        x, y = (im.width - W) // 2, (im.height - H) // 2; im = im.crop((x, y, x + W, y + H))
    grad = Image.new('L', (1, H)); [grad.putpixel((0, i), int(235 * max(0, (i - H * .35) / (H * .65)) ** 1.3)) for i in range(H)]
    im = Image.composite(Image.new('RGB', (W, H), (0, 14, 30)), im, grad.resize((W, H)))
    dr = ImageDraw.Draw(im); rtl = l == 'ar'; M = 60
    size, lines = layout(t, l, logo); f = font(l, size); lh = int(size * 1.22); y = H - 92 - lh * len(lines)
    for ln in lines:
        kw = dict(font=f, fill='white', direction='rtl') if rtl else dict(font=f, fill='white')
        w = dr.textlength(ln, font=f, direction='rtl') if rtl else dr.textlength(ln, font=f)
        dr.text((W - M - w if rtl else M + (420 if logo else 0), y), ln, **kw); y += lh
    fb = font('en', 26); brand = 'savingplanets.com'
    dr.rounded_rectangle((M - 4 if not rtl else W - M - dr.textlength(brand, font=fb) - 26, H - 70, (M + dr.textlength(brand, font=fb) + 22) if not rtl else W - M + 4, H - 28), 20, fill=(0, 95, 150))
    dr.text((M + 9 if not rtl else W - M - dr.textlength(brand, font=fb) - 13, H - 66), brand, font=fb, fill='white')
    if si:
        fc = font(l, 22); c = sic.SI_T[l]; cw = dr.textlength(c, font=fc, direction='rtl') if rtl else dr.textlength(c, font=fc)
        cx = M if rtl else W - M - cw
        dr.rounded_rectangle((cx - 12, H - 66, cx + cw + 12, H - 30), 14, fill=(0, 0, 0))
        dr.text((cx, H - 63), c, font=fc, fill='white', **({'direction': 'rtl'} if rtl else {}))
    os.makedirs(os.path.dirname(out), exist_ok=True); im.save(out, 'JPEG', quality=64, optimize=True, progressive=True)
def setmeta(s, url):
    s = re.sub(r'(<meta property="og:image" content=")[^"]*(")', r'\g<1>' + url + r'\2', s)
    s = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', r'\g<1>' + url + r'\2', s)
    s = re.sub(r'\s*<meta property="og:image:(?:width|height|type)" content="[^"]*">', '', s)
    s = s.replace(f'<meta property="og:image" content="{url}">', f'<meta property="og:image" content="{url}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:type" content="image/jpeg">', 1)
    return s
def main():
    mf = 'assets/og/manifest.json'; man = json.load(open(mf)) if os.path.exists(mf) else {}
    nimg = npg = 0; srcs = {}
    for k, v in man.items():  # remembered photo per page (og:image now points at our card)
        if k.startswith('src:'): srcs[k[4:]] = v
    srcs = {k: v for k, v in srcs.items() if os.path.exists(v)}
    for l in LANGS:
        for p in sorted(glob.glob(d(l) + '*.html')):
            b = os.path.basename(p)
            if SKIP.match(b): continue
            s = open(p, encoding='utf8').read()
            if 'http-equiv="refresh"' in s or '<meta property="og:image"' not in s: continue
            en = open(b, encoding='utf8').read() if l != 'en' and os.path.exists(b) else s
            src = srcs.get(b) or source(en); srcs[b] = src; t = title(s); si = sic.is_si(src)
            out = f'assets/og/{l}/{b[:-5]}.jpg'; vis = visible_key(src, t, l, si)
            old = hashlib.sha1(f'{src}|{os.path.getsize(src)}|{t}|{si}|v2'.encode()).hexdigest()[:12]  # pre-Oct-16 key (full title)
            if os.path.exists(out) and man.get('vis:' + out) == vis: pass  # visible card unchanged: keep the file (and its ?v=)
            elif os.path.exists(out) and 'vis:' + out not in man and man.get(out) == old: man['vis:' + out] = vis  # one-time migration, no re-render
            else: render(src, t, l, si, out); man[out] = vis; man['vis:' + out] = vis; nimg += 1
            url = f'{SITE}{out}?v={man[out][:8]}'; n = setmeta(s, url)
            if n != s: open(p, 'w', encoding='utf8').write(n); npg += 1
    for k, v in srcs.items(): man['src:' + k] = v
    json.dump(man, open(mf, 'w'), indent=0, sort_keys=True)
    print(f'build-og: {nimg} cards rendered, {npg} pages updated')
if __name__ == '__main__': main()
