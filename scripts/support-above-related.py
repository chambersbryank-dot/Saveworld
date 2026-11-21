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
    'html body.toc-sub .page-hero.sp-anim-banner .page-hero-content{width:100%;align-self:stretch;box-sizing:border-box}'
    'html body.toc-sub .page-hero .page-hero-content .hero-title-row{display:grid;grid-template-columns:minmax(10rem,1fr) minmax(0,auto) minmax(10rem,1fr);'
    'align-items:center;column-gap:.9rem;width:100%;margin:0 0 .35rem}'
    'html body.toc-sub .page-hero .page-hero-content .hero-title-row h1{grid-column:2;margin:0 !important;'
    'text-align:center !important;line-height:1.15;min-width:0;text-wrap:wrap !important}'
    'html body.toc-sub .page-hero a.title-donate.help-btn{grid-column:3;justify-self:start;'
    'display:inline-flex !important;align-items:center !important;'
    'justify-content:center !important;align-self:center;box-sizing:border-box;min-height:48px;'
    'min-width:7.25rem;margin:0 !important;padding:0 1.15rem !important;line-height:1 !important;'
    'font-family:Montserrat,"Segoe UI",sans-serif;font-size:1rem !important;font-weight:800 !important;'
    'letter-spacing:0;white-space:nowrap;text-align:center;text-decoration:none !important;color:#fff !important;'
    'background-color:#0a4f78 !important;'
    'background-image:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06)),linear-gradient(#0a4f78,#0a4f78) !important;'
    'border:1px solid rgba(160,225,255,.55) !important;border-radius:999px !important;'
    'box-shadow:inset 0 1px 0 rgba(255,255,255,.55),inset 0 -1px 0 rgba(255,255,255,.08),0 6px 20px rgba(0,40,70,.28),0 0 12px rgba(0,156,222,.35) !important;'
    '-webkit-backdrop-filter:blur(14px) saturate(180%);backdrop-filter:blur(14px) saturate(180%);'
    'text-shadow:none}'
    'html body.toc-sub .page-hero a.title-donate.help-btn:hover{background-image:linear-gradient(180deg,rgba(255,255,255,.3),rgba(255,255,255,.1)),linear-gradient(#0a4f78,#0a4f78) !important}'
    'html body.toc-sub .page-hero a.title-donate.help-btn:focus-visible{outline:3px solid #fff;outline-offset:3px}'
    '@media (max-width:640px){html body.toc-sub .page-hero .page-hero-content .hero-title-row{grid-template-columns:1fr;justify-items:center}'
    'html body.toc-sub .page-hero .page-hero-content .hero-title-row h1{grid-column:1;text-align:center !important}'
    'html body.toc-sub .page-hero a.title-donate.help-btn{grid-column:1;justify-self:end}}'
    'html body.toc-sub .review-row{max-width:1100px;margin:.4rem auto 0;padding:0 1.5rem;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;column-gap:1rem;row-gap:.65rem}'
    'html body.toc-sub .review-row>.page-reviewed{max-width:none;margin:0;padding:0;flex:1 1 16rem}'
    'html body.toc-sub a.return-wth.help-btn{flex:0 0 auto;margin:0 !important;margin-inline-start:auto !important;display:inline-flex !important;align-items:center !important;justify-content:center !important;box-sizing:border-box;min-height:44px;padding:0 1.05rem !important;line-height:1 !important;font-family:Montserrat,"Segoe UI",sans-serif;font-size:.95rem !important;font-weight:800 !important;letter-spacing:0;white-space:nowrap;text-align:center;text-decoration:none !important;color:#fff !important;background-color:#0a4f78 !important;background-image:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06)),linear-gradient(#0a4f78,#0a4f78) !important;border:1px solid rgba(160,225,255,.55) !important;border-radius:999px !important;box-shadow:inset 0 1px 0 rgba(255,255,255,.55),inset 0 -1px 0 rgba(255,255,255,.08),0 6px 20px rgba(0,40,70,.28),0 0 12px rgba(0,156,222,.35) !important;-webkit-backdrop-filter:blur(14px) saturate(180%);backdrop-filter:blur(14px) saturate(180%)}'
    'html body.toc-sub a.return-wth.help-btn:hover{background-image:linear-gradient(180deg,rgba(255,255,255,.3),rgba(255,255,255,.1)),linear-gradient(#0a4f78,#0a4f78) !important}'
    'html body.toc-sub a.return-wth.help-btn:focus-visible{outline:3px solid #fff;outline-offset:3px}'
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
