#!/usr/bin/env python3
"""Nov 3 (founder): no visible breadcrumb trail ("Home > Ways to Help") on any page, all langs.
The <nav class="breadcrumb"> stays in the source with the `hidden` attribute, so generators that
anchor on it and seo-jsonld (BreadcrumbList JSON-LD for search engines) keep working, but nobody sees it.
Run after every page generator. Idempotent."""
import re, glob
RX = re.compile(r'<nav ((?:(?!hidden)[^>])*class="breadcrumb"(?:(?!hidden)[^>])*)>')
n = 0
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith(('node_modules/', '.git/')): continue
    s = open(p, encoding='utf-8').read()
    t = RX.sub(r'<nav \1 hidden>', s)
    if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1
print(f'hide-breadcrumbs: {n} pages')
