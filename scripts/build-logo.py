#!/usr/bin/env python3
"""Oct 20 (founder approved logo v2): the text-free Saving Planets globe icon (water / leaf / space arrows) in the header nav,
favicons and apple-touch icon, on every page in en/fr/es/ar/it/he. Idempotent; run late in weekly-sync.sh (after build-nav and
he-si-note, before build-critical, which inlines the LOGO CSS for the first paint).
- Nav: <picture> (WebP + PNG, 1x/2x/3x) inside a.spn-brand, before the 'Home' text, so it stays the homepage link. It is a little
  taller than the bar and bleeds above/below via negative margins (layout height unchanged, so the nav text never moves).
  RTL (ar/he): flex order puts it on the 'Home' side automatically. Alt text translated.
- Head: favicon.ico (16/32/48) + 32px PNG replace favicon.svg (old logo); apple-touch-icon.png = icon on #071018 (iOS fills alpha black).
- Footer: visible 'Logo created by SI and Biological SI Partner' line (standing SI credit rule), translated.
Web sizes live in assets/brand/ (made from the founder's 512 px master); 2048/4096 Real-ESRGAN masters are on R2 (media-manifest:
brand/sp-logo-*). The homepage hero is not touched."""
import re, glob, os
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
ALT = {'en': 'Saving Planets logo', 'fr': 'Logo de Saving Planets', 'es': 'Logotipo de Saving Planets', 'ar': 'شعار Saving Planets',
       'it': 'Logo di Saving Planets', 'he': 'הלוגו של Saving Planets'}
CREDIT = {'en': 'Logo created by SI and Biological SI Partner', 'fr': 'Logo créé par SI et Biological SI Partner',
          'es': 'Logotipo creado por SI y Biological SI Partner', 'ar': 'الشعار من إنشاء SI وBiological SI Partner',
          'it': 'Logo creato da SI e Biological SI Partner', 'he': 'הלוגו נוצר על ידי SI ושותף SI ביולוגי'}
V = '20261020'
CSS = r"""
/* LOGO:START */
/* Oct 20 logo v2 (scripts/build-logo.py): icon left of 'Home' (right in RTL), bleeds a little above/below the bar; negative margins keep the row height */
#topnav .spn-brand{gap:.55rem;overflow:visible;position:relative;z-index:2}
#topnav .spn-logo{display:block;flex:none;line-height:0}
#topnav .spn-logo img{display:block;width:100%;height:100%;filter:drop-shadow(0 2px 6px rgba(0,0,0,.55));transition:transform .25s ease}
#topnav .spn-brand:hover .spn-logo img{transform:scale(1.06) rotate(-4deg)}
@media (min-width:1140px){#topnav .spn-logo{width:64px;height:64px;margin:-16px 0}#topnav.spn-solid .spn-logo{width:52px;height:52px;margin:-10px 0}html[lang=fr] #topnav .spn-logo,html[lang=es] #topnav .spn-logo{width:44px;height:44px;margin:-6px 0}}
/* fr/es: the long main menu row reaches under the brand, so the icon stays in row 1 there */
@media (max-width:1139px){#topnav .spn-logo,#topnav.spn-solid .spn-logo{width:54px;height:54px;margin:-5px 0}#topnav .spn-brand{gap:.4rem;min-width:0}}
@media (max-width:380px){#topnav .spn-logo,#topnav.spn-solid .spn-logo{width:46px;height:46px;margin:-1px 0}#topnav .spn-brand{font-size:1rem}}
@media (prefers-reduced-motion:reduce){#topnav .spn-logo img{transition:none}#topnav .spn-brand:hover .spn-logo img{transform:none}}
.logo-credit{font-size:.75rem;opacity:.8;font-style:italic;margin:.4rem 0 0}
/* LOGO:END */
"""
def pre(p): return '../' if os.sep in p or '/' in p else ''
def pic(p, l):
    b = pre(p) + 'assets/brand/sp-logo-'
    ss = lambda e: f'{b}72.{e}?v={V} 1x, {b}144.{e}?v={V} 2x, {b}216.{e}?v={V} 3x'
    return (f'<span class="spn-logo"><picture><source type="image/webp" srcset="{ss("webp")}">'
            f'<img src="{b}72.png?v={V}" srcset="{ss("png")}" width="72" height="72" alt="{ALT[l]}" decoding="async" fetchpriority="high"></picture></span>')
def fix(s, p, l):
    s = re.sub(r'<span class="spn-logo">.*?</span>', '', s, flags=re.S)
    s = re.sub(r'(<a class="spn-brand" href="[^"]*">)', lambda m: m.group(1) + pic(p, l), s, count=1)
    r = pre(p)
    icons = (f'<link rel="icon" href="{r}favicon.ico?v={V}" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="{r}assets/brand/favicon-32.png?v={V}">'
             f'<link rel="apple-touch-icon" href="{r}apple-touch-icon.png?v={V}">')
    s = re.sub(r'<link[^>]*rel="icon"[^>]*>\s*|<link[^>]*rel="apple-touch-icon"[^>]*>\s*', '', s)
    s = re.sub(r'(<link[^>]*href="[^"]*favicon\.svg"[^>]*>\s*)', '', s)
    s = s.replace('</title>', '</title>' + icons, 1) if '</title>' in s else s
    s = re.sub(r'<!-- LOGO-CREDIT -->.*?<!-- /LOGO-CREDIT -->', '', s, flags=re.S)
    if '</footer>' in s:
        s = s.replace('</footer>', f'<!-- LOGO-CREDIT --><p class="logo-credit">{CREDIT[l]}</p><!-- /LOGO-CREDIT --></footer>', 1)
    return s
if __name__ == '__main__':
    n = 0
    for l in LANGS:
        for p in sorted(glob.glob('*.html' if l == 'en' else f'{l}/*.html')):
            s = open(p, encoding='utf-8').read()
            if 'id="topnav"' not in s and 'rel="icon"' not in s: continue
            s2 = fix(s, p, l)
            if s2 != s: open(p, 'w', encoding='utf-8').write(s2); n += 1
    st = open('styles.css', encoding='utf-8').read()
    st = re.sub(r'\n?/\* LOGO:START \*/.*?/\* LOGO:END \*/\n?', '', st, flags=re.S).rstrip('\n') + '\n' + CSS.strip('\n') + '\n'
    open('styles.css', 'w', encoding='utf-8').write(st)
    print(f'build-logo: {n} page writes')
