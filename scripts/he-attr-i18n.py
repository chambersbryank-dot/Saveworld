#!/usr/bin/env python3
"""Oct 17: Hebrew pages built by i18n-build from English output (labs, calculators...) keep some UI text in attributes:
data-t='{json}' string tables and plain data-* messages (data-bad ...). Translate those through i18n/he.json.
Run after i18n-build.py he. `--missing` prints untranslated attribute strings."""
import json, re, os, sys, html, glob
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
M = json.load(open('i18n/he.json', encoding='utf8')); miss = set()
ONLY = {'data-open', 'data-close', 'data-ok', 'data-name', 'data-todo', 'data-prog', 'data-bad', 'data-done', 'data-copied', 'data-msg', 'data-err'}
def tr(v):
    if v in M: return M[v]
    if re.search(r'[A-Za-z]{2,}', v): miss.add(v)
    return v
def fix(s):
    def jt(m):
        raw = html.unescape(m.group(2))
        try: d = json.loads(raw)
        except Exception: return m.group(0)
        d = {k: (tr(v) if isinstance(v, str) else v) for k, v in d.items()}
        if m.group(0)[len(m.group(1)) + 1] == "'": return m.group(1) + "='" + json.dumps(d, ensure_ascii=False).replace("'", '&#x27;') + "'"
        return m.group(1) + '="' + html.escape(json.dumps(d, ensure_ascii=False), quote=True) + '"'
    s = re.sub(r'(data-t)="(\{[^"]*\})"', jt, s)
    s = re.sub(r"(data-t)='(\{[^']*\})'", jt, s)
    def at(m):
        if m.group(1) not in ONLY: return m.group(0)
        v = html.unescape(m.group(2)); t = tr(v)
        return m.group(0) if t == v else f'{m.group(1)}="{html.escape(t, quote=True)}"'
    return re.sub(r'(data-[a-z][a-z0-9-]*)="([^"{][^"]*)"', at, s)
n = 0
for f in glob.glob('he/*.html'):
    s = open(f, encoding='utf8').read(); t = fix(s)
    if t != s and '--missing' not in sys.argv: open(f, 'w', encoding='utf8').write(t); n += 1
if '--missing' in sys.argv: print('\n'.join(sorted(miss)))
else: print('he-attr-i18n:', n, 'pages,', len(miss), 'missing')
