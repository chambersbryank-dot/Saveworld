#!/usr/bin/env python3
"""Move the Support block above Related Solutions, and add a title Donate button.

Only pages whose #support section already has a Donate button. The title button
uses that same donation URL and data-sp-donate so the existing UET donate_click
listener counts it. Pages without a Donate button are left untouched.
"""
import html
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(ROOT)
LANGS = {'': 'en', 'fr': 'fr', 'es': 'es', 'ar': 'ar', 'it': 'it', 'he': 'he'}
LABEL = {
    'en': 'Donate', 'fr': 'Faire un don', 'es': 'Donar',
    'ar': 'تبرّع', 'it': 'Dona', 'he': 'תרומה',
}
E = lambda s: html.escape(s if s is not None else '', quote=True)
SUPPORT_RE = re.compile(r'<section\b[^>]*\bid="support"[^>]*>.*?</section>', re.S)
H1_RE = re.compile(r'<h1\b[^>]*>.*?</h1>', re.S)
STYLE = (
    '<style id="title-donate-css">'
    '.page-hero-content .hero-title-row{display:inline-flex;flex-wrap:wrap;align-items:center;justify-content:center;'
    'gap:.55rem .9rem;max-width:100%;vertical-align:top}'
    '.page-hero-content .hero-title-row h1{margin:0}'
    '.page-hero a.title-donate{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;'
    'min-height:44px;margin:0;padding:.4rem 1.05rem;font:800 .95rem/1.2 Montserrat,"Segoe UI",sans-serif;'
    'white-space:nowrap;text-align:center;text-decoration:none !important;color:#fff !important;'
    'background-color:#0a4f78 !important;'
    'background-image:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06)),linear-gradient(#0a4f78,#0a4f78) !important;'
    'border:1px solid rgba(160,225,255,.55) !important;border-radius:999px !important;'
    'box-shadow:inset 0 1px 0 rgba(255,255,255,.55),inset 0 -1px 0 rgba(255,255,255,.08),0 6px 20px rgba(0,40,70,.28),0 0 12px rgba(0,156,222,.35) !important;'
    'text-shadow:0 1px 2px rgba(0,0,0,.45)}'
    '.page-hero a.title-donate:hover{background-image:linear-gradient(180deg,rgba(255,255,255,.3),rgba(255,255,255,.1)),linear-gradient(#0a4f78,#0a4f78) !important}'
    '.page-hero a.title-donate:focus-visible{outline:3px solid #fff;outline-offset:3px}'
    '@media (max-width:640px){.page-hero-content .hero-title-row{display:flex;width:100%}'
    '.page-hero-content .hero-title-row h1{flex:1 1 100%;text-align:center}'
    '.page-hero a.title-donate{margin-inline-start:auto}}'
    '</style>'
)


def plain(fragment):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', fragment or '')).strip()


def donate_link(sec, lang):
    label = LABEL[lang]
    for m in re.finditer(r'<a\b([^>]*)>(.*?)</a>', sec, re.S):
        attrs, inner = m.group(1), m.group(2)
        if 'help-btn' not in attrs:
            continue
        text = plain(inner)
        if 'data-sp-donate' not in attrs and text != label:
            continue
        href = re.search(r'\bhref="([^"]+)"', attrs)
        if not href:
            continue
        url = html.unescape(href.group(1))
        if url.startswith('https://') and 'savingplanets.com' not in url.lower():
            return url, label
    return '', ''


def move_support(src, sec, start, end):
    rel = src.find('<!-- RELATED:START -->')
    if rel < 0 or start < rel:
        return src, False
    src = src[:start] + src[end:]
    rel = src.find('<!-- RELATED:START -->')
    src = src[:rel] + sec + src[rel:]
    return src, True


def add_title_button(src, url, label):
    if 'title-donate' in src:
        return src, False
    h1 = H1_RE.search(src)
    if not h1:
        return src, False
    btn = ('<a class="btn help-btn title-donate" data-sp-donate="1" href="%s" target="_blank" rel="noopener">%s</a>'
           % (E(url), E(label)))
    row = STYLE + '<div class="hero-title-row">' + h1.group(0) + btn + '</div>'
    return src[:h1.start()] + row + src[h1.end():], True


def main():
    moved = titled = skipped = 0
    for folder, lang in LANGS.items():
        base = folder or '.'
        prefix = (folder + '/') if folder else ''
        for name in sorted(os.listdir(base)):
            if not name.endswith('.html'):
                continue
            path = prefix + name
            src = open(path, encoding='utf8').read()
            m = SUPPORT_RE.search(src)
            if not m:
                continue
            url, label = donate_link(m.group(0), lang)
            if not url:
                skipped += 1
                continue
            src2, did_move = move_support(src, m.group(0), m.start(), m.end())
            src2, did_title = add_title_button(src2, url, label)
            if src2 != src:
                open(path, 'w', encoding='utf8').write(src2)
            if did_move:
                moved += 1
            if did_title:
                titled += 1
    print('moved support above related:', moved)
    print('title donate buttons:', titled)
    print('support pages without a donate link left alone:', skipped)


if __name__ == '__main__':
    main()
