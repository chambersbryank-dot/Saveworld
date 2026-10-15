#!/usr/bin/env python3
"""Themed page heroes (standing rule, Oct 14 2026): every page hero depicts the page's main theme.
Idempotent post-process for EN/fr/es/ar. Images live in assets/hero/<key>-{800,1600}.{webp,jpg}; CSS in styles.css."""
import re, os
MAP = {'Kids_Map': ('kids', 'NASA EPIC'), 'Satellite_Explorer': ('satx', 'NASA/JPL-Caltech'), 'Lesson_Builder': ('lesson', 'USFWS'),
       'Teachers': ('teach', 'USFWS'), 'About': ('about', 'NASA'), 'Contact': ('about', 'NASA'), 'Press': ('about', 'NASA'),
       'Community': ('help', 'NPS'), 'Find_a_Cleanup': ('help', 'NPS'), 'Ways_to_Help': ('help', 'NPS'),
       'Glossary': ('learn', 'NASA'), 'Myth_vs_Fact': ('learn', 'NASA'), 'Sitemap': ('learn', 'NASA'), '404': ('learn', 'NASA'),
       'Rawanes_Mission_Log': ('mission', 'NASA'), 'Privacy': ('about', 'NASA'), 'Editorial_Policy': ('learn', 'NASA'),
       'Corrections': ('learn', 'NASA'), 'Press_Kit': ('about', 'NASA'), 'Topics': ('learn', 'NASA')}
n = 0
for lang in ('', 'fr/', 'es/', 'ar/'):
    for p, (k, c) in MAP.items():
        f = f'{lang}{p}.html'
        if not os.path.exists(f):
            continue
        s = open(f, encoding='utf-8').read()
        s2 = re.sub(r'<section class="page-hero"( id="[^"]*")?>(<div class="page-hero-content">.*?</div>)</section>',
                    lambda m: f'<section class="page-hero hero-{k}"{m.group(1) or ""}>{m.group(2)}<span class="hero-credit">{c}</span></section>',
                    s, count=1, flags=re.S)
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2); n += 1
print(f'apply-heroes: {n} pages updated')
