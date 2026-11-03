#!/usr/bin/env python3
"""Put a real source link on credits that already name a known photo.

Hub cards use the source URL stored in assets/data/hub-agency-images.json.
A credit that already prints a PIA id links to that NASA photojournal page.
SI stills keep the visible line "Created by the Founder and SI" (no invented URL).
Idempotent. Does not change the Saturn hero image files.
"""
import os, re, json, glob, html

os.chdir(os.path.join(os.path.dirname(__file__), '..'))
AG = json.load(open('assets/data/hub-agency-images.json', encoding='utf8'))
PIA = re.compile(r'PIA\d{5}')
CREDIT = re.compile(
    r'<(?:p|span|figcaption)\b[^>]*class="[^"]*(?:photo-credit|agency-credit|sol-credit)[^"]*"[^>]*>.*?</(?:p|span|figcaption)>',
    re.S)

def link_pia_block(block):
    if 'photojournal.jpl.nasa.gov/catalog/PIA' in block:
        return block
    def one(m):
        pid = m.group(0)
        return f'<a href="https://photojournal.jpl.nasa.gov/catalog/{pid}" rel="noopener">{pid}</a>'
    return PIA.sub(one, block)

def link_pias(s):
    return CREDIT.sub(lambda m: link_pia_block(m.group(0)), s)

def link_hubs(s):
    for e in AG:
        url = e.get('source') or ''
        if not url:
            continue
        who = html.escape(e['credit'], quote=False)
        href = html.escape(url, quote=True)
        linked = f'<a href="{href}" rel="noopener">{who}</a>'
        for card in (e['card'],):
            rx = re.compile(
                r'(<a class="photo-link" href="' + re.escape(card) + r'">.*?</a></div>\s*'
                r'<p class="photo-credit agency-credit">)(.*?)(</p>)', re.S)
            def repl(m, who=who, linked=linked):
                inner = m.group(2)
                if '<a ' in inner or who not in inner:
                    return m.group(0)
                return m.group(1) + inner.replace(who, linked, 1) + m.group(3)
            s = rx.sub(repl, s, count=1)
    return s

n = 0
for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
    if os.path.basename(f).startswith('google'):
        continue
    raw = open(f, encoding='utf8').read()
    nxt = link_hubs(link_pias(raw))
    if nxt != raw:
        open(f, 'w', encoding='utf8').write(nxt)
        n += 1
print('link-photo-sources:', n, 'files')
