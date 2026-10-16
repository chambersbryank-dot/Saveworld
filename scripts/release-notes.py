#!/usr/bin/env python3
"""Release notes for one month (YYYY-MM) from Changelog.html: the dated solution batches released that month. Used by release.yml."""
import re, sys, html
m = sys.argv[1]; s = open('Changelog.html', encoding='utf8').read(); out = []
for sec in re.findall(r'<section class="cl-day">(.*?)</section>', s, re.S):
    d = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})">([^<]*)</time>', sec)
    if not d or not d.group(1).startswith(m): continue
    items = [(html.unescape(t), u) for u, t in re.findall(r'<li><a href="([^"]+)">([^<]*)</a></li>', sec)]
    out.append(f'### {html.unescape(d.group(2))}: {len(items)} new solutions\n' + '\n'.join(f'- [{t}](https://www.savingplanets.com/{u})' for t, u in items))
print(f'Monthly release of [savingplanets.com](https://www.savingplanets.com/) for {m}.\n')
print('\n\n'.join(out) if out else 'No new solution batches were released this month; see the site changelog for details.')
print('\nFull changelog: https://www.savingplanets.com/Changelog.html')
