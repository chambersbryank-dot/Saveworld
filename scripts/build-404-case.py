#!/usr/bin/env python3
"""Oct 25 2026 (founder, upgrade 1): 404 pages send mistyped-case and old addresses to the right page.
/courses.html, /courses, /solutions.html, /COURSES, /ways-to-help ... -> the real page (match ignores case, '-', '_' and .html),
inside the visitor's language folder when that page exists there, else the English page. Aliases cover addresses with no page
of their own (launch schedule -> Upcoming_Launches.html, the Live Launch Tracker). Only a single unambiguous match redirects;
anything else keeps the normal Page Not Found. No server, DNS or Cloudflare change. Writes the block between
<!-- CASE404:START/END --> in 404.html of every language (after i18n-build). Idempotent. Run from repo root."""
import os, re, json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LANGS = ['fr', 'es', 'ar', 'it', 'he']
key = lambda p: re.sub(r'[-_ ]', '', p[:-5].lower())
stub = lambda f: 'http-equiv="refresh"' in open(f, encoding='utf8').read(3000)   # existing redirect stubs (ways-to-help.html ...) are not targets
en = sorted(f for f in os.listdir('.') if f.endswith('.html') and f not in ('404.html', 'googlea5d3cc0c785fec04.html') and not stub(f))
ks = {}
for f in en: ks.setdefault(key(f), []).append(f)
pages = {k: v[0] for k, v in ks.items() if len(v) == 1}          # ambiguous keys never redirect
missing = {l: sorted(f for f in en if not os.path.exists(f'{l}/{f}')) for l in LANGS}
ALIAS = {'launchschedule': 'Upcoming_Launches.html', 'launches': 'Upcoming_Launches.html',
         'launchtracker': 'Upcoming_Launches.html', 'home': 'index.html'}
DATA = json.dumps({'p': pages, 'a': ALIAS, 'm': missing, 'l': LANGS}, separators=(',', ':'), sort_keys=True)
JS = ('(function(){var D=' + DATA + ';var s=location.pathname.split("/").filter(Boolean),l="";'
      'if(s.length>1&&D.l.indexOf(s[0])>=0)l=s.shift();if(s.length!==1)return;var k;'
      'try{k=decodeURIComponent(s[0])}catch(e){return}k=k.toLowerCase().replace(/\\.html?$/,"").replace(/[-_ ]/g,"");'
      'var t=D.a[k]||D.p[k];if(!t)return;var f=t.split("#")[0];if(l&&D.m[l].indexOf(f)>=0)l="";'
      'var u="/"+(l?l+"/":"")+t;if(u.split("#")[0]===location.pathname)return;location.replace(u+(t.indexOf("#")<0?location.hash:""));})();')
BLOCK = '<!-- CASE404:START --><script>' + JS + '</script><!-- CASE404:END -->'
R = re.compile(r'<!-- CASE404:START -->.*?<!-- CASE404:END -->', re.S)
for f in ['404.html'] + [f'{l}/404.html' for l in LANGS]:
    s = open(f, encoding='utf8').read(); o = s
    s = R.sub(lambda m: BLOCK, s) if R.search(s) else s.replace('</head>', BLOCK + '\n</head>', 1)
    if f == '404.html': open(f, 'w', encoding='utf8').write(s); import importlib.util as U; sp = U.spec_from_file_location('ib', 'scripts/i18n-build.py'); ib = U.module_from_spec(sp); sp.loader.exec_module(ib); H = ib.src_hash('404.html')
    else: s = re.sub(r'(<meta content="404\.html )[0-9a-f]{12}(" name="i18n-source"/?>)', lambda m: m.group(1) + H + m.group(2), s)  # block is language-neutral: re-stamp, no rebuild
    if s != o: open(f, 'w', encoding='utf8').write(s)
    print(f, 'updated' if s != o else 'unchanged')
print('404 case map:', len(pages), 'pages,', len(ks) - len(pages), 'ambiguous keys skipped,', len(ALIAS), 'aliases')
