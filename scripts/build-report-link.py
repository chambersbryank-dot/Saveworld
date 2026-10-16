#!/usr/bin/env python3
"""Oct 15: 'Report a correction' link in every page footer (all 5 languages), right after the footer's Corrections link.
Links to the GitHub issue form .github/ISSUE_TEMPLATE/correction.yml with the page URL and language prefilled.
Idempotent (li.fm-report is replaced). Run late in weekly-sync.sh, after the footer generators."""
import re, glob, os, urllib.parse
SITE = 'https://www.savingplanets.com/'; REPO = 'https://github.com/chambersbryank-dot/Saveworld/issues/new'
L = {'en': ('Report a correction', 'English'), 'fr': ('Signaler une correction', 'Français'), 'es': ('Informar de una corrección', 'Español'),
     'ar': ('الإبلاغ عن تصحيح', 'العربية'), 'it': ('Segnala una correzione', 'Italiano')}
def main():
    n = 0
    for f in sorted(glob.glob('*.html') + glob.glob('*/*.html')):
        l = f.split('/')[0] if '/' in f else 'en'
        if l not in L: continue
        s = open(f, encoding='utf8').read()
        if '<footer' not in s: continue
        s2 = re.sub(r'<li class="fm-report">.*?</li>', '', s)
        url = SITE + ('' if l == 'en' else l + '/') + os.path.basename(f)
        q = urllib.parse.urlencode({'template': 'correction.yml', 'page': url, 'language': L[l][1]})
        li = f'<li class="fm-report"><a href="{REPO}?{q.replace("&", "&amp;")}" rel="noopener" target="_blank">{L[l][0]}</a></li>'
        m = re.search(r'<li><a href="(?:\.\./)?Corrections\.html">[^<]*</a></li>', s2)
        if m: s2 = s2[:m.end()] + li + s2[m.end():]
        elif '<!-- FOOTER-MAP:END -->' in s2: s2 = s2.replace('</ul></div></div><!-- FOOTER-MAP:END -->', li + '</ul></div></div><!-- FOOTER-MAP:END -->', 1)
        if s2 != s: open(f, 'w', encoding='utf8').write(s2); n += 1
    print(f'build-report-link: {n} pages')
if __name__ == '__main__': main()
