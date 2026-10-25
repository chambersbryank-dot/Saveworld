#!/usr/bin/env python3
"""Ways_to_Help.html: every solution on the site (live from Solutions.html, grouped by hub in the same order), each row with
(1) a link to its solution page, (2) Donate = the organization's official donation page, (3) Offer to Help = its official
volunteer / get-involved / careers page. Oct 24 2026 (founder): 'ensure Ways to Help includes all solutions we offer'.
If an organization has no donation or volunteer page, the cell links to its official contact page and says so.
Data: assets/data/ways-to-help.json (orgs + page -> org). A solution missing from the data fails the build (no silent gaps).
Writes the block between <!-- WTH-ALL:START/END --> (English); i18n-build.py translates it. Idempotent. Run from repo root."""
import re, os, json, html, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
E_ = lambda s: html.escape(s, quote=True)
D = json.load(open('assets/data/ways-to-help.json', encoding='utf8'))
O, P = D['orgs'], D['pages']
sol = open('Solutions.html', encoding='utf8').read()
hubs = [(m.start(), m.group(1), html.unescape(m.group(2))) for m in re.finditer(r'<h2[^>]*><a href="([^"]+)">(.*?)</a></h2>', sol)]
cards = [(m.start(), m.group(1), html.unescape(m.group(2))) for m in
         re.finditer(r'<article class="card sol-card" data-url="([^"]+)".*?<h3><a href="[^"]+">(.*?)</a></h3>', sol, re.S)]
EXT = ' target="_blank" rel="noopener"'
def btn(url, label, join=False):
    ext = EXT if url.startswith('http') else ''
    return f'<a class="btn help-btn{" help-btn-join" if join else ""}" href="{E_(url)}"{ext}>{label}</a>'
def note(t): return f'<span class="help-note">{t}</span>'
missing, groups, stats = [], {}, {'total': 0, 'no_donate': [], 'no_help': []}
for pos, page, title in cards:
    hub = [h for h in hubs if h[0] < pos][-1]
    key = P.get(page[:-5])
    if not key or key not in O: missing.append(page); continue
    name, don, hlp, con = O[key]
    if key == 'sp':
        dc = note('Saving Planets Doesn&#x27;t Take Donations')
    elif don: dc = btn(don, 'Donate')
    elif con: dc = btn(con, 'Contact') + note('No Donation Page'); stats['no_donate'].append(page)
    else: dc = note('No Donation Page'); stats['no_donate'].append(page)
    if hlp: hc = btn(hlp, 'Offer to Help', True)
    elif con: hc = btn(con, 'Contact', True) + note('No Volunteer Page'); stats['no_help'].append(page)
    else: hc = note('No Volunteer Page'); stats['no_help'].append(page)
    groups.setdefault((hub[1], hub[2]), []).append(
        f'<tr><td><a href="{E_(page)}">{E_(title)}</a></td><td>{E_(name)}</td><td>{dc}</td><td>{hc}</td></tr>')
    stats['total'] += 1
if missing: sys.exit('ways-to-help.json has no organization for: ' + ', '.join(missing))
slug = lambda h: 'hub-' + re.sub(r'[^a-z0-9]+', '-', h.lower()).strip('-')
jump = ''.join(f'<li><a href="#{slug(h)}">{E_(h)}</a></li>' for (_, h) in groups)
secs = ''.join(
    f'<div class="wth-hub" id="{slug(h)}"><h3><a href="{E_(hp)}">{E_(h)}</a></h3><table class="help-table wth-table"><thead><tr>'
    '<th scope="col">Solution</th><th scope="col">Organization</th><th scope="col">Donate</th><th scope="col">Offer to Help</th></tr></thead>'
    f'<tbody>{"".join(rows)}</tbody></table></div>' for (hp, h), rows in groups.items())
N = stats['total']
BLOCK = ('<!-- WTH-ALL:START -->' + '<style>.help-note{display:block;font-size:.85rem;opacity:.85;text-decoration:none;margin:.15rem 0 0}.wth-jump ul{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem 1rem;padding:0;margin:1rem 0 1.5rem}.wth-hub{scroll-margin-top:90px}.wth-hub h3{margin:2rem 0 .4rem}.wth-table td:first-child{min-width:12rem}.help-table th{text-decoration:none}</style>' + '<section class="five-ws" id="donate"><h2>Every Solution, Every Way to Help</h2>'
         '<p>Every solution on Saving Planets, grouped by hub. Each row links to the solution&#x27;s page, the organization&#x27;s official donation page and its official volunteer, get-involved or careers page.</p>'
         f'<nav class="wth-jump" aria-label="Jump to a hub"><ul>{jump}</ul></nav>{secs}</section>\n'
         '<section class="impact" id="solution"><h2>How This Works</h2><div class="impact-box"><p>Saving Planets doesn&#x27;t take donations and doesn&#x27;t receive any of the money. Every Donate button goes straight to the organization&#x27;s own official page, and every Offer to Help button goes to its own volunteer, get-involved or careers page. When an organization has no donation or volunteer page, the button goes to its official contact page instead, and the row says so. Many space agencies don&#x27;t take donations, but NASA invites anyone to help with real research through its citizen science projects.</p></div></section><!-- WTH-ALL:END -->')
f = 'Ways_to_Help.html'; s = open(f, encoding='utf8').read(); o = s
if '<!-- WTH-ALL:START -->' in s:
    s = re.sub(r'<!-- WTH-ALL:START -->.*?<!-- WTH-ALL:END -->', lambda m: BLOCK, s, flags=re.S)
else:  # first run: replace the old Donate or Volunteer / How This Works / Join the Team / Citizen Science sections
    a = s.index('<section class="five-ws" id="donate">'); b = s.index('<!-- B4-WTH:START -->')
    s = s[:a] + BLOCK + '\n' + s[b:]
if s != o: open(f, 'w', encoding='utf8').write(s)
print(f'ways to help: {N} solutions, {len(groups)} hubs; no donate page: {len(stats["no_donate"])}; no volunteer page: {len(stats["no_help"])}', 'updated' if s != o else 'unchanged')
