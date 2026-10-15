#!/usr/bin/env python3
"""Oct 14: Community Wall paused (saved copy: branch archive/community-wall, _archive/community/; see docs/community-archive.md). While COMMUNITY_ENABLED is False:
strip every link to Community.html in en/fr/es/ar, keep redirect stubs at the old URLs, drop it from sitemap.xml + pages.txt. Idempotent."""
import os, re, glob
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
COMMUNITY_ENABLED = False
if COMMUNITY_ENABLED: raise SystemExit('community enabled: nothing to do')
STUB = ('<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><title>Saving Planets</title>'
        '<meta name="robots" content="noindex"><link rel="canonical" href="https://www.savingplanets.com/{pre}Find_a_Cleanup.html">'
        '<meta http-equiv="refresh" content="0; url=Find_a_Cleanup.html"><script>location.replace("Find_a_Cleanup.html")</script></head>'
        '<body><p><a href="Find_a_Cleanup.html">Find a Cleanup</a></p></body></html>\n')
SEP = r'<span aria-hidden="true"> · </span>'
n = 0
for d in ('', 'fr/', 'es/', 'ar/'):
    stub = STUB.format(lang=d[:-1] or 'en', pre=d)
    p = d + 'Community.html'
    if not os.path.exists(p) or open(p, encoding='utf8').read() != stub: open(p, 'w', encoding='utf8').write(stub)
    for f in glob.glob(d + '*.html'):
        if f == p: continue
        s = open(f, encoding='utf8').read(); o = s
        s = re.sub(r'<li><a href="Community\.html">[^<]*</a></li>', '', s)                       # nav / footer map
        s = re.sub(SEP + r'<a href="Community\.html">[^<]*</a>', '', s)                          # footer row
        s = re.sub(r'<a href="Community\.html">[^<]*</a>' + SEP, '', s)
        s = re.sub(r'\s*<a class="btn[^"]*" href="Community\.html">[^<]*</a>', '', s)            # buttons
        s = re.sub(r"\n[^\n]*url: 'Community\.html'[^\n]*", '', s)                     # Search.html fallback list
        if s != o: open(f, 'w', encoding='utf8').write(s); n += 1
sm = open('sitemap.xml', encoding='utf8').read()
sm2 = re.sub(r'\s*<url><loc>https://www\.savingplanets\.com/(?:(?:fr|es|ar)/)?Community\.html</loc>.*?</url>', '', sm, flags=re.S)
sm2 = re.sub(r'<xhtml:link [^>]*href="https://www\.savingplanets\.com/(?:(?:fr|es|ar)/)?Community\.html"/>', '', sm2)
if sm2 != sm: open('sitemap.xml', 'w', encoding='utf8').write(sm2)
pt = open('i18n/pages.txt', encoding='utf8').read()
pt2 = ''.join(l for l in pt.splitlines(True) if l.strip() != 'Community.html')
if pt2 != pt: open('i18n/pages.txt', 'w', encoding='utf8').write(pt2)
print('community DISABLED: pages cleaned', n)
