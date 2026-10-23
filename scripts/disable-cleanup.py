#!/usr/bin/env python3
"""Oct 22 (founder): 'Find a Cleanup' paused, not viable right now (may return in a future revamp).
While CLEANUP_ENABLED is False: strip every link/card/menu entry to Find_a_Cleanup.html in all languages, turn the
page into a noindex redirect stub to Ways_to_Help.html, drop it from sitemap.xml, i18n/pages.txt and the Search
fallback list. Generator kept (build-batch4.py) so it can come back by flipping the flag. Idempotent; run late in
weekly-sync (after build-nav and the final i18n-sitemap, before build-search)."""
import os, re, glob
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
CLEANUP_ENABLED = False
if CLEANUP_ENABLED: raise SystemExit('cleanup enabled: nothing to do')
LANGS = ('', 'fr/', 'es/', 'ar/', 'it/', 'he/')
STUB = ('<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><title>Saving Planets</title>'
        '<meta name="robots" content="noindex"><link rel="canonical" href="https://www.savingplanets.com/{pre}Ways_to_Help.html">'
        '<meta http-equiv="refresh" content="0; url=Ways_to_Help.html"><script>location.replace("Ways_to_Help.html")</script></head>'
        '<body data-pagefind-ignore="all"><p><a href="Ways_to_Help.html">Ways to Help</a></p></body></html>\n')
SEP = r'<span aria-hidden="true">\s*·\s*</span>'
H = r'(?:\.\./)?(?:(?:fr|es|ar|it|he)/)?Find_a_Cleanup\.html(?:#[\w-]*)?'
n = 0
for d in LANGS:
    p = d + 'Find_a_Cleanup.html'
    stub = STUB.format(lang=d[:-1] or 'en', pre=d)
    if os.path.exists(p) and open(p, encoding='utf8').read() != stub: open(p, 'w', encoding='utf8').write(stub)
    for f in glob.glob(d + '*.html'):
        if f == p: continue
        s = open(f, encoding='utf8').read()
        if 'Find_a_Cleanup' not in s: continue
        o = s
        s = re.sub(rf'<li[^>]*><a href="{H}"[^>]*>.*?</a></li>', '', s, flags=re.S)          # nav / footer map / lists
        s = re.sub(SEP + rf'\s*<a href="{H}"[^>]*>[^<]*</a>', '', s)                           # footer / inline rows
        s = re.sub(rf'<a href="{H}"[^>]*>[^<]*</a>\s*' + SEP, '', s)
        s = re.sub(rf'\s*<a class="[^"]*" href="{H}"[^>]*>.*?</a>', '', s, flags=re.S)       # buttons
        s = re.sub(rf'\s*<a href="{H}" class="[^"]*"[^>]*>.*?</a>', '', s, flags=re.S)
        s = re.sub(rf"\n[^\n]*url: '{H}'[^\n]*", '', s)                                       # Search.html fallback list
        s = re.sub(rf'<a href="{H}"[^>]*>(.*?)</a>', r'\1', s, flags=re.S)                     # any remaining in-text link: keep words, drop link
        if s != o: open(f, 'w', encoding='utf8').write(s); n += 1
sm = open('sitemap.xml', encoding='utf8').read()
sm2 = re.sub(r'\s*<url>\s*<loc>https://www\.savingplanets\.com/(?:(?:fr|es|ar|it|he)/)?Find_a_Cleanup\.html</loc>.*?</url>', '', sm, flags=re.S)
sm2 = re.sub(r'\s*<xhtml:link [^>]*href="https://www\.savingplanets\.com/(?:(?:fr|es|ar|it|he)/)?Find_a_Cleanup\.html"\s*/>', '', sm2)
if sm2 != sm: open('sitemap.xml', 'w', encoding='utf8').write(sm2)
pt = open('i18n/pages.txt', encoding='utf8').read()
pt2 = ''.join(l for l in pt.splitlines(True) if l.strip() != 'Find_a_Cleanup.html')
if pt2 != pt: open('i18n/pages.txt', 'w', encoding='utf8').write(pt2)
print('find-a-cleanup DISABLED: pages cleaned', n)
