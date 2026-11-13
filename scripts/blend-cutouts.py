#!/usr/bin/env python3
"""Feathered transparent cutouts shared by the satellite map and Voyages.

Planets and moons become circular cutouts. A disc already on black keeps its
limb and loses the square. Spacecraft on a dark field lose that field.
Anything left with a hard photo edge fades out so it does not sit in a box.
"""
import os
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'earth', 'cut')


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    im.save(path, 'WEBP', quality=86, method=6)
    print(name, im.size)


def disc(src, name, feather=0.045, fill=0.96):
    im = Image.open(os.path.join(ROOT, src)).convert('RGBA')
    w, h = im.size
    side = min(w, h)
    left, top = (w - side) // 2, (h - side) // 2
    im = im.crop((left, top, left + side, top + side))
    if side > 900:
        im = im.resize((900, 900), Image.Resampling.LANCZOS)
        side = 900
    px = im.load()
    r = side * 0.5 * fill
    fade = max(2.0, side * feather)
    for y in range(side):
        for x in range(side):
            d = ((x + 0.5 - side / 2) ** 2 + (y + 0.5 - side / 2) ** 2) ** 0.5
            a = 255 if d <= r - fade else 0 if d >= r else int(255 * (r - d) / fade)
            p = px[x, y]
            px[x, y] = (p[0], p[1], p[2], min(p[3], a))
    save(im, name)


def sun(src, name):
    im = Image.open(os.path.join(ROOT, src)).convert('RGBA')
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side))
    if side > 900:
        im = im.resize((900, 900), Image.Resampling.LANCZOS)
        side = 900
    px = im.load()
    cx = cy = side / 2
    limit = side * 0.49
    for y in range(side):
        for x in range(side):
            p = px[x, y]
            # Black sky becomes transparent. The red corona stays, then fades.
            glow = max(p[0], p[1], p[2])
            a = 0 if glow < 12 else min(255, int((glow - 12) * 3.2))
            d = ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5
            if d > limit:
                a = int(a * max(0, 1 - (d - limit) / (side * 0.04)))
            px[x, y] = (p[0], p[1], p[2], a)
    save(im.filter(ImageFilter.GaussianBlur(0.4)), name)


def key_dark(src, name, thresh=28):
    im = Image.open(os.path.join(ROOT, src)).convert('RGBA')
    if max(im.size) > 1000:
        im.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            m = max(p[0], p[1], p[2])
            a = 0 if m < thresh else min(255, int((m - thresh) * 8))
            px[x, y] = (p[0], p[1], p[2], min(p[3], a))
    # Soften the last few pixels at the file edge so no rectangle remains.
    edge = max(8, int(min(w, h) * 0.04))
    for y in range(h):
        for x in range(w):
            inset = min(x, y, w - 1 - x, h - 1 - y)
            if inset < edge:
                p = px[x, y]
                px[x, y] = (p[0], p[1], p[2], int(p[3] * inset / edge))
    save(im, name)


def vignette(src, name, inner=0.42):
    im = Image.open(os.path.join(ROOT, src)).convert('RGBA')
    im.thumbnail((900, 900), Image.Resampling.LANCZOS)
    w, h = im.size
    px = im.load()
    cx, cy = w / 2, h / 2
    r = min(w, h) * 0.5
    for y in range(h):
        for x in range(w):
            d = ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5 / r
            a = 255 if d <= inner else 0 if d >= 1 else int(255 * (1 - d) / (1 - inner))
            p = px[x, y]
            px[x, y] = (p[0], p[1], p[2], min(p[3], a))
    save(im, name)


def main():
    disc('assets/earth/blue-marble-disc-lg.webp', 'earth.webp', fill=0.98)
    sun('assets/earth/sdo-aia304.jpg', 'sun.webp')
    disc('assets/earth/lro-moon.jpg', 'moon.webp', fill=0.97)
    disc('assets/earth/europa-galileo.jpg', 'europa.webp', fill=0.97)
    disc('assets/earth/ganymede-galileo.jpg', 'ganymede.webp', fill=0.90)
    disc('assets/Jupiter_Cassini_Portrait.jpg', 'jupiter.webp', fill=0.92)
    disc('assets/Mercury_MESSENGER.jpg', 'mercury.webp', fill=0.96)
    key_dark('assets/Psyche_Illustration.jpg', 'psyche.webp', 18)
    key_dark('assets/sat/hera-800.jpg', 'hera.webp', 22)
    key_dark('assets/earth/juno-concept.jpg', 'juno.webp', 16)
    vignette('assets/sat/psyche-800.jpg', 'psyche-craft.webp', 0.34)
    vignette('assets/Lucy_KSC.jpg', 'lucy.webp', 0.3)
    vignette('assets/Solar_Orbiter_Astrotech.jpg', 'solar-orbiter.webp', 0.3)
    key_dark('assets/earth/europa-craft-src.jpg', 'europa-craft.webp', 14)
    print('cutouts in', OUT)


if __name__ == '__main__':
    main()
