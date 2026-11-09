#!/usr/bin/env python3
"""Nov 9 2026 (Bryan): the Before Saving Planets fossil-sites block is removed from Ways to Help.
This script only deletes a leftover <!-- BSP-XSITE --> section if one is still present.
It does not add the block back. Idempotent. Run from the repo root."""
import re, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PAT = re.compile(r'<!-- BSP-XSITE:START -->.*?<!-- BSP-XSITE:END -->', re.S)
for lang in ('en', 'fr', 'es', 'ar', 'it', 'he'):
    f = 'Ways_to_Help.html' if lang == 'en' else f'{lang}/Ways_to_Help.html'
    s = open(f, encoding='utf8').read()
    s2, n = PAT.subn('', s)
    if s2 != s:
        open(f, 'w', encoding='utf8').write(s2)
    print(lang, 'removed' if n else 'already gone')
