#!/usr/bin/env python3
"""Oct 16 (user-approved speed item): load site.js with `defer` on every page (all langs). site.js already sits at the end of
<body> and every block waits for DOMContentLoaded/readyState or load, so defer only moves execution to after parsing (before
DOMContentLoaded) and keeps document order with the other deferred/module scripts (batchb.js, share.js, solutions.js, search-ui.js).
Skipped (NODEFER): pages whose inline scripts after site.js call its globals (window.sp*) — Artemis_II (spRenderMission).
Idempotent; --revert removes the attribute. Runs late in weekly-sync.sh, before build-critical.py."""
import os, re, glob, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
NODEFER = {'Artemis_II.html'}
SKIP = {'index.html'}  # homepage belongs to the hero worker; never edited here
TAG = re.compile(r'<script src="((?:\.\./)?site\.js\?v=[\w.-]+)"( defer)?>')
INL = re.compile(r'<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>(.*?)</script>', re.S)
rev = '--revert' in sys.argv; n = 0; skipped = []
for f in sorted(glob.glob('*.html') + glob.glob('[a-z][a-z]/*.html')):
    s = open(f, encoding='utf8').read(); m = TAG.search(s)
    if not m: continue
    en = f.split('/', 1)[-1]
    if en in SKIP: continue
    unsafe = en in NODEFER or any(re.search(r'\bwindow\.sp[A-Z]\w*|\bspnLang\b', x) for x in INL.findall(s[m.end():]))
    want = '' if (rev or unsafe) else ' defer'
    if unsafe and not rev: skipped.append(f)
    s2 = TAG.sub(lambda mm: f'<script src="{mm.group(1)}"{want}>', s, count=1)
    if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
print('defer-sitejs:', n, 'pages updated; kept blocking:', ', '.join(skipped) or 'none')
