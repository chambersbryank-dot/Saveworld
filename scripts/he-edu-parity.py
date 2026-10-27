#!/usr/bin/env python3
"""Oct 27 2026: Hebrew education parity blocks on Teachers.html (and Learn hero already via build-learn-hubs).

Several Oct 16 education generators still target en/fr/es/ar/it only. Hebrew Teachers was missing the
STARTHERE, SIHELPER, T-BROWSE and LEARNLINK marker blocks that feed Big Questions mining, so he had
67 FAQ items vs ~74 in other languages. This script injects those blocks in Hebrew (facts match EN).
Idempotent. Run after build-standards.py / before build-question-bank.py. Does not deploy Workers.
"""
import os, re, html

os.chdir(os.path.join(os.path.dirname(__file__), '..'))
esc = lambda s: html.escape(s, quote=False)
escq = lambda s: html.escape(s, quote=True)

START = [
    ('Cadets.html', '🎖️ התחילו כאן: JROTC ו-CAP'),
    ('Homeschool.html', '🏡 התחילו כאן: חינוך ביתי'),
    ('AP_IB_Physics.html', '📘 התחילו כאן: פיזיקה AP ו-IB'),
    ('Careers.html', '🚀 קריירה ומסלולים'),
]

STARTHERE = (
    '<!-- STARTHERE:START --><h2 id="start-here">התחילו כאן</h2>'
    '<p>בחרו את הדלת שמתאימה לכם. בכל מסלול משתמשים באותם מדריכים, דפי מתמטיקה, מעבדות ומחשבונים בחינם.</p>'
    '<ul class="cxg sh-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:.8rem;list-style:none;padding:0">'
    + ''.join(f'<li><a href="{p}">{esc(t)}</a></li>' for p, t in START)
    + '</ul>'
    '<style>.sh-grid a{display:flex;align-items:center;min-height:56px;padding:.6rem 1rem;border-radius:14px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);font-weight:800;text-decoration:none;color:inherit}.sh-grid a:hover,.sh-grid a:focus-visible{border-color:#ffd54a}</style><!-- STARTHERE:END -->'
)

# Text + form chrome matching other langs (same public endpoint/sitekey as build-si-helper.py).
SIHELPER = (
    '<!-- SIHELPER:START --><style>'
    '.si-help{max-width:900px;margin:1.2rem auto;padding:1.1rem 1.25rem;border-radius:18px;border:1px solid rgba(124,170,255,.5);background:rgba(124,170,255,.08)}'
    '.si-help h2{margin:.1rem 0 .4rem}.si-pilot{font-size:.78rem;font-weight:800;padding:.1rem .55rem;border-radius:999px;background:#ffd54a;color:#1a1300;vertical-align:middle}'
    '.si-form{display:grid;gap:.5rem}.si-form label{font-weight:700}.si-form textarea{font:inherit;font-size:1rem;min-height:5.5rem;padding:.6rem .7rem;border-radius:12px;width:100%;box-sizing:border-box;resize:vertical}'
    '.si-form button{justify-self:start;min-height:44px;padding:.45rem 1.3rem;border-radius:999px;font:inherit;font-weight:800;cursor:pointer;background:#ffd54a;color:#1a1300;border:0}'
    '.si-help :focus-visible{outline:3px solid #ffd54a;outline-offset:2px}</style>'
    '<section class="si-help" id="ask-si" aria-labelledby="si-h">'
    '<h2 id="si-h">שאלו את SI Helper (פיילוט) <span class="si-pilot">SI</span></h2>'
    '<p>מצאו שיעורים, עובדות ופעילויות באתר הזה. SI עונה רק מדפי Saving Planets ומקשר לדפים שמהם לקח.</p>'
    '<form class="si-form" novalidate data-endpoint="https://si-helper.chambersbryank.workers.dev/ask" '
    'data-sitekey="0x4AAAAAAFY9fV0YboAn4sqm" data-lang="he" data-hosts="">'
    '<label for="si-q">השאלה שלכם</label>'
    '<textarea id="si-q" name="q" required maxlength="500" placeholder="לדוגמה: אילו שיעורים על שוניות אלמוגים מתאימים לכיתות ג–ה?"></textarea>'
    '<button type="submit">שאלו את SI</button>'
    '<p class="si-note">SI עלול לטעות. בדקו את הדף המקושר.</p>'
    '<div class="si-out" aria-live="polite"></div></form></section>'
    '<script src="../assets/si-helper.js?v=20261016V" defer></script><!-- SIHELPER:END -->'
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
    # Order similar to EN: STARTHERE early, SI after EDU-LINKS, LEARNLINK before footer FAQ
    s = put(s, 'STARTHERE', STARTHERE, '<!-- EDU-LINKS:START -->')
    s = put(s, 'SIHELPER', SIHELPER, '<!-- COURSELINK:START -->')
    s = put(s, 'LEARNLINK', LEARNLINK, '<!-- SP-HUBFAQ:START -->')
    # T-BROWSE comes from build-standards.py once he is in LANGS
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
        print('he-edu-parity: Teachers.html updated')
    else:
        print('he-edu-parity: Teachers.html unchanged')


if __name__ == '__main__':
    main()
