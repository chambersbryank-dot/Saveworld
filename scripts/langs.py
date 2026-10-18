#!/usr/bin/env python3
"""Oct 17 2026: one place for the site's language lists.

Hebrew (/he/, right-to-left) is built and deployed but stays UNLINKED until a native Hebrew speaker reviews it.

  >>> TO LAUNCH HEBREW: set HE_PUBLIC = True below (one line), run weekly-sync.sh, commit, post-deploy. <<<

While HE_PUBLIC is False: /he/ pages are built (only the pages listed in i18n/he-pages.txt), carry
<meta name="robots" content="noindex,nofollow">, a self canonical, no hreflang, and are NOT in the language switcher,
the sitemap, seo-fix/seo-lint, the language banner or search. English and the other languages never link to /he/.
"""
import os
HE_PUBLIC = False   # <<< the Hebrew launch switch (see NOTES.md 'Hebrew (/he/)')

PUBLIC = ['fr', 'es', 'ar', 'it'] + (['he'] if HE_PUBLIC else [])   # translated languages shown to visitors / search engines
BUILD = ['fr', 'es', 'ar', 'it', 'he']                               # translated languages i18n-build writes
RTL = {'ar', 'he'}
LOCALE = {'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES', 'ar': 'ar_AR', 'it': 'it_IT', 'he': 'he_IL'}
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def he_pages():
    """English pages that have a Hebrew translation so far (i18n/he-pages.txt; grows batch by batch)."""
    p = os.path.join(_ROOT, 'i18n', 'he-pages.txt')
    return [l.strip() for l in open(p, encoding='utf8') if l.strip() and not l.startswith('#')] if os.path.exists(p) else []

def pages_for(lang, all_pages):
    """Pages i18n-build writes for a language: every page, except Hebrew = only the reviewed-for-translation list."""
    if lang != 'he': return list(all_pages)
    # Oct 17: Hebrew also builds pages that fr/es/ar/it get from their own generators (Learn, calculators, labs...),
    # translated from the English output via i18n/he.json, so every public EN page has a he/ twin.
    hp = he_pages(); return [p for p in all_pages if p in set(hp)] + [p for p in hp if p not in set(all_pages) and os.path.exists(os.path.join(_ROOT, p))]

def is_rtl(lang): return lang in RTL
