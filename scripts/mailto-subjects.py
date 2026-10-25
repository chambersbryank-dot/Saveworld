#!/usr/bin/env python3
"""Oct 14 2026: every mailto to a savingplanets.com inbox carries the subject for its purpose (English; subjects route mail).
Runs over HTML (all langs) and generator sources. Idempotent. Run last in weekly-sync."""
import re, glob, os, subprocess
from urllib.parse import quote
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
SUBJ = {'hello': 'Hello from a Saving Planets visitor', 'ideas': 'Solution idea for Saving Planets', 'media': 'Media inquiry',
        'partners': 'Creating Partnership Starts Here', 'teachers': 'Teacher question or lesson plan request',
        'errors': 'Found an error or bug, please fix', 'privacy': 'Privacy or data request', 'translate': 'I can help translate'}
RX = re.compile(r'mailto:(' + '|'.join(SUBJ) + r')@savingplanets\.com(\?[^"\'\s<>)`]*)?')
def fix(m): return f'mailto:{m.group(1)}@savingplanets.com?subject=' + quote(SUBJ[m.group(1)], safe='')
files = [f for f in subprocess.check_output(['git', 'ls-files', '*.html', '*.py', '*.js', '*.mjs', '*.json'], text=True).split()
         if not f.startswith(('pagefind/', 'node_modules/')) and f not in ('scripts/mailto-subjects.py', 'scripts/link-errors.py')]
n = 0; gone = []
for f in files:
    if not os.path.exists(f): gone.append(f); continue  # tracked but deleted by an earlier step (e.g. build-courses dropping an untranslated course page): skip, report below
    s = open(f, encoding='utf-8').read(); t = RX.sub(fix, s)
    if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
print(f'mailto-subjects: {n} files updated')
if gone: print(f'mailto-subjects: WARNING {len(gone)} tracked files missing on disk (skipped):', *gone[:20])
