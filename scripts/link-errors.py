#!/usr/bin/env python3
"""Oct 14 2026: error/bug reports go to errors@savingplanets.com (subject "Found an error or bug, please fix").
Post-process (all langs, after i18n-build): repoint old correction mailtos and linkify plain errors@ mentions. Idempotent.
media@ stays for press, partners@ for partnerships, ideas@ for new solutions."""
import re, glob, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
ERR = 'mailto:errors@savingplanets.com?subject=Found%20an%20error%20or%20bug%2C%20please%20fix'
n = 0
for f in glob.glob('*.html') + glob.glob('*/*.html'):
    if f.startswith('pagefind'): continue
    s = open(f, encoding='utf-8').read(); o = s
    # old "Spot an error?" links (ideas@ ... subject=Correction)
    s = re.sub(r'<a href="mailto:ideas@savingplanets\.com\?subject=Correction"([^>]*)>ideas@savingplanets\.com</a>', lambda m: f'<a href="{ERR}"{m.group(1)}>errors@savingplanets.com</a>', s)
    s = s.replace('href="mailto:ideas@savingplanets.com?subject=Correction"', f'href="{ERR}"')
    # linkify plain-text errors@ inside <p>/<li> body text (not inside tags, anchors, head or scripts)
    head, sep, body = s.partition('<body')
    def link(seg):
        for box, href in (('errors', ERR), ('privacy', 'mailto:privacy@savingplanets.com?subject=Privacy%20request')):
            seg = re.sub(r'(?<![">/=@\w.])' + box + r'@savingplanets\.com', f'<a href="{href}">{box}@savingplanets.com</a>', seg)
        return seg
    parts = re.split(r'(<script.*?</script>|<a\b.*?</a>|<[^>]+>)', body, flags=re.S)
    body = ''.join(p if (i % 2) else link(p) for i, p in enumerate(parts))
    s = head + sep + body
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print(f'link-errors: {n} pages updated')
