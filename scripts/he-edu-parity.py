#!/usr/bin/env python3
"""Oct 27 2026: Hebrew education parity blocks on Teachers.html (and Learn hero already via build-learn-hubs).

Several Oct 16 education generators still target en/fr/es/ar/it only. Hebrew Teachers was missing the
STARTHERE, T-BROWSE and LEARNLINK marker blocks that feed Big Questions mining, so he had
67 FAQ items vs ~74 in other languages. This script injects those blocks in Hebrew (facts match EN).
The SI Helper pilot is retired: any SIHELPER block on he/Teachers.html is removed, not re-added.
Idempotent. Run after build-standards.py / before build-question-bank.py. Does not deploy Workers.
"""
import os, re, html

os.chdir(os.path.join(os.path.dirname(__file__), '..'))
esc = lambda s: html.escape(s, quote=False)
escq = lambda s: html.escape(s, quote=True)

START = [
    ('AP_IB_Physics.html', '📘 פיזיקה AP ו-IB'),
]

STARTHERE = (
    '<!-- STARTHERE:START --><h2 id="start-here">התחילו כאן</h2>'
    '<p>בחרו את הדלת שמתאימה לכם. בכל מסלול משתמשים באותם מדריכים, דפי מתמטיקה, מעבדות ומחשבונים בחינם.</p>'
    '<ul class="cxg sh-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:.8rem;list-style:none;padding:0">'
    + ''.join(f'<li><a href="{p}">{esc(t)}</a></li>' for p, t in START)
    + '</ul>'
    '<style>.sh-grid a{display:flex;align-items:center;min-height:56px;padding:.6rem 1rem;border-radius:14px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);font-weight:800;text-decoration:none;color:inherit}.sh-grid a:hover,.sh-grid a:focus-visible{border-color:#ffd54a}</style><!-- STARTHERE:END -->'
)

LEARNLINK = (
    '<!-- LEARNLINK:START --><aside class="learn-link card-band" aria-label="להעמיק: למידה">'
    '<h2>להעמיק: למידה</h2>'
    '<p>שיעורים ברמה אוניברסיטאית עם דוגמאות פתורות, תרגול עם בדיקה אוטומטית והערות למורים: '
    '<a href="Learn.html">🎓 למידה: כל המסלולים</a> · '
    '<a href="Orbits_Guide.html">מסלולים בהסבר</a> · '
    '<a href="Orbit_Lab.html">מעבדת מסלולים</a> · '
    '<a href="Aero_Guide.html">איך טיסה עובדת</a> · '
    '<a href="Aero_Lab.html">מעבדת תעופה</a> · '
    '<a href="Physics_Guide.html">פיזיקה בהסבר</a> · '
    '<a href="Physics_Lab.html">מעבדת פיזיקה</a></p>'
    '</aside><!-- LEARNLINK:END -->'
)


def put(s, mark, blk, before_pat=None):
    rx = re.compile(rf'<!-- {mark}:START -->.*?<!-- {mark}:END -->', re.S)
    if rx.search(s):
        return rx.sub(lambda m: blk, s)
    if before_pat and before_pat in s:
        return s.replace(before_pat, blk + before_pat, 1)
    if '</main>' in s:
        return s.replace('</main>', blk + '</main>', 1)
    return s


def main():
    f = 'he/Teachers.html'
    s = open(f, encoding='utf-8').read()
    o = s
    # The Teachers home owns its own start strip. Do not put the old Start-here block back.
    if '<!-- TEACHHOME:START -->' not in s:
        s = put(s, 'STARTHERE', STARTHERE, '<!-- EDU-LINKS:START -->')
    s = re.sub(r'<!-- SIHELPER:START -->.*?<!-- SIHELPER:END -->', '', s, flags=re.S)
    s = put(s, 'LEARNLINK', LEARNLINK, '<!-- SP-HUBFAQ:START -->')
    # T-BROWSE comes from build-standards.py once he is in LANGS
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
        print('he-edu-parity: Teachers.html updated')
    else:
        print('he-edu-parity: Teachers.html unchanged')


if __name__ == '__main__':
    main()
