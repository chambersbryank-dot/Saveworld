#!/usr/bin/env python3
"""Oct 19 2026: SI-translated reader note on every /he/ page (Hebrew only, owner-approved launch text).
Idempotent (HE-SI-NOTE markers), inserted just before <footer>. Runs late in weekly-sync, after every page generator."""
import glob, os, re
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
MAIL = 'mailto:translate@savingplanets.com?subject=%D7%AA%D7%99%D7%A7%D7%95%D7%9F%20%D7%AA%D7%A8%D7%92%D7%95%D7%9D'  # subject: תיקון תרגום
NOTE = ('<!-- HE-SI-NOTE:START --><aside class="he-si-note" role="note" lang="he" dir="rtl" data-pagefind-ignore '
        'style="max-width:60rem;margin:1.5rem auto;padding:.75rem 1rem;border-radius:10px;background:rgba(255,255,255,.06);font-size:.95rem;line-height:1.6">'
        '<p style="margin:0">דף זה תורגם מאנגלית על ידי SI. מצאתם טעות או ניסוח טוב יותר? כתבו לנו ל-'
        f'<a href="{MAIL}"><bdi>translate@savingplanets.com</bdi></a>. '
        'אנחנו קוראים כל הודעה, ובאישורכם נודה לכם בניוזלטר שלנו.</p></aside><!-- HE-SI-NOTE:END -->')
RX = re.compile(r'<!-- HE-SI-NOTE:START -->.*?<!-- HE-SI-NOTE:END -->', re.S)
n = 0
for p in sorted(glob.glob('he/*.html')):
    s = open(p, encoding='utf-8').read(); o = s
    if RX.search(s): s = RX.sub(lambda m: NOTE, s)
    elif '<footer' in s:
        i = s.rfind('<footer'); s = s[:i] + NOTE + '\n' + s[i:]
    if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print(f'he-si-note: {n} pages updated')
