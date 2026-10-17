#!/usr/bin/env python3
"""Oct 16 2026 (Lighthouse fix): pre-render the homepage space hero's heavy assets once, so phones never compute them.
  {enceladus,moon}-{2048,1024}.webp - the seamless ground textures, rendered by the SAME procedural
      code as assets/hero-themes.js (__heroSpace.procTex) at 2048^2 (4x the old runtime size) and 1024^2 for small screens. Uploaded to R2 (media.savingplanets.com).
  poster-{land,tab,phone}-<w>.{avif,webp}           - a still of the Enceladus scene (no text), the hero background
      until the live canvas is ready (it fades out), and the LCP-safe first paint.
Run on the box after changing the scene code:  python3 scripts/build-hero-assets.py  then  python3 scripts/r2-upload.py --prefix images/hero-space/ /tmp/hero-space-assets/*  then  python3 scripts/build-hero-themes.py
Needs Playwright + Chrome (box only; not part of weekly-sync). Serves the repo on a local port while it runs."""
import asyncio, base64, io, os, subprocess, sys, time
from PIL import Image
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.environ.get('HERO_ASSETS_OUT', '/tmp/hero-space-assets');  # not in the repo: upload with r2-upload.py --prefix images/hero-space/
PORT = 8799
# each composition is laid out at the CSS size it is shown at (text block, horizon, Saturn, plume dimming all match), and
# rendered natively at the largest width it ships at (no upscaling): 1180x820 @5.1 = 6016 px wide
POSTERS = {'land': ((1180, 820), [1280, 1920, 2560, 3840, 5120, 6016]), 'tab': ((820, 1180), [1640, 2048]), 'phone': ((390, 844), [820, 1240])}
HIDE = ('.hero-content,#topnav,.hs-caps,.hs-cap,.hs-cap.on,.hero-video-credit,.sticky-help,.sp-lb,.hero-space::before{visibility:hidden!important}'
        '.hero-space::before{display:none!important}')
async def cors(route):
    r = await route.fetch(); h = dict(r.headers); h['access-control-allow-origin'] = '*'
    await route.fulfill(response=r, headers=h)
async def main():
    os.makedirs(OUT, exist_ok=True)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
            pg = await b.new_page(viewport={'width': 800, 'height': 600})
            await pg.goto(f'http://localhost:{PORT}/index.html?hero=space&hero-gpu=1', wait_until='load'); await pg.wait_for_function('window.__heroSpace')
            for name, size in (('enceladus', 2048), ('moon', 2048), ('enceladus', 1024), ('moon', 1024)):
                url = await pg.evaluate('''([n, z]) => new Promise(res => __heroSpace.procTex(n, z, img => { const c = document.createElement('canvas');
                    c.width = img.width; c.height = img.height; c.getContext('2d').putImageData(img, 0, 0); res(c.toDataURL('image/png')); }))''', [name, size])
                im = Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB')
                f = os.path.join(OUT, f'{name}-{size}.webp'); im.save(f, 'WEBP', quality=95, method=6)  # visually lossless
                print('texture', name, size, os.path.getsize(f) // 1024, 'KB')
            await pg.close()
            for key, ((w, h), widths) in POSTERS.items():
                ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=max(widths) / w); pg = await ctx.new_page()
                await pg.route('https://media.savingplanets.com/**', cors)  # R2 only allows the live origin; mirror its CORS for localhost
                await pg.goto(f'http://localhost:{PORT}/index.html?hero=space&hero-gpu=1&hero-poster=1&hero-t=9', wait_until='load')
                await pg.wait_for_function("document.querySelector('.hero-space.hs-ready')", timeout=240000)
                await pg.evaluate('__heroSpace.seek(9)'); await pg.add_style_tag(content=HIDE); await pg.wait_for_timeout(2500)
                await pg.evaluate('__heroSpace.seek(9)'); await pg.wait_for_timeout(300)
                im = Image.open(io.BytesIO(await pg.screenshot(clip={'x': 0, 'y': 0, 'width': w, 'height': h}))).convert('RGB')
                for ww in widths:
                    f = os.path.join(OUT, f'poster-{key}-{ww}.webp')
                    r = im.resize((ww, round(ww * h / w)), Image.LANCZOS)
                    r.save(f, 'WEBP', quality=92, method=6); r.save(f[:-5] + '.avif', 'AVIF', quality=88, speed=4)  # visually lossless
                    print('poster', key, ww, os.path.getsize(f) // 1024, 'KB webp', os.path.getsize(f[:-5] + '.avif') // 1024, 'KB avif')
                await ctx.close()
            await b.close()
    finally:
        srv.terminate()
asyncio.run(main())
