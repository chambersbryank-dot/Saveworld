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
slug = lambda h: 'hub-' + re.sub(r'[^a-z0-9]+', '-', h.lower()).strip('-')
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
    give, join = int(bool(don) and key != 'sp'), int(bool(hlp))
    hs = slug(hub[2])
    groups.setdefault((hub[1], hub[2]), []).append(
        f'<tr data-hub="{hs}" data-give="{give}" data-join="{join}"><td><a href="{E_(page)}">{E_(title)}</a></td><td>{E_(name)}</td><td>{dc}</td><td>{hc}</td></tr>')
    stats['total'] += 1
if missing: sys.exit('ways-to-help.json has no organization for: ' + ', '.join(missing))
jump = ''.join(f'<li><a href="#{slug(h)}">{E_(h)}</a></li>' for (_, h) in groups)
def summary(rows):  # Oct 25 (founder, upgrade 3): short summary card per hub; counts only, from the same rows
    n = len(rows); g = sum('data-give="1"' in r for r in rows); j = sum('data-join="1"' in r for r in rows)
    return ('<ul class="wth-sum">'
            f'<li><b>{n}</b> <span>Solutions</span></li><li><b>{g}</b> <span>With a donation page</span></li>'
            f'<li><b>{j}</b> <span>With a volunteer page</span></li></ul>')
# Oct 25 (founder, upgrade 3): client-side filters. Hidden without JS (every hub and row stays visible, grouped).
# Only filters the data supports: topic (hub) and Give/Join (official donation / volunteer page present).
# Online-vs-nearby and age are NOT offered: ways-to-help.json has no location or age data (never invented).
tbtn = lambda val, label, on=False: f'<button type="button" class="wth-f" data-val="{val}" aria-pressed="{"true" if on else "false"}">{label}</button>'
FILTERS = ('<div class="wth-filters" id="wth-filters" hidden><div class="wth-frow" role="group" aria-labelledby="wth-ft"><span class="wth-fl" id="wth-ft">Topic</span>'
           + tbtn('all', 'All Topics', True) + ''.join(tbtn(slug(h), E_(h)) for (_, h) in groups) + '</div>'
           '<div class="wth-frow" role="group" aria-labelledby="wth-fw"><span class="wth-fl" id="wth-fw">Way to Help</span>'
           + tbtn('all', 'Any Way', True) + tbtn('give', 'Give (Donate)') + tbtn('join', 'Join (Volunteer)') + '</div>'
           '<p class="wth-count" aria-live="polite" aria-atomic="true"><span>Solutions shown:</span> <b id="wth-n">' + str(sum(len(r) for r in groups.values())) + '</b></p>'
           '<button type="button" class="btn wth-clear" id="wth-clear">Clear Filters</button>'
           '<p class="wth-none" id="wth-none" hidden>No solutions match these filters.</p></div>')
JS = ('<script>(function(){var f=document.getElementById("wth-filters");if(!f)return;f.hidden=false;var st={0:"all",1:"all"},rows=[].slice.call(document.querySelectorAll(".wth-table tbody tr")),'
      'hubs=[].slice.call(document.querySelectorAll(".wth-hub")),grp=f.querySelectorAll(".wth-frow");'
      'function run(){var n=0;rows.forEach(function(r){var ok=(st[0]=="all"||r.getAttribute("data-hub")==st[0])&&(st[1]=="all"||r.getAttribute("data-"+st[1])=="1");r.hidden=!ok;if(ok)n++;});'
      'hubs.forEach(function(h){h.hidden=!h.querySelector("tbody tr:not([hidden])");});document.getElementById("wth-n").textContent=n;document.getElementById("wth-none").hidden=n>0;}'
      '[].forEach.call(grp,function(g,i){g.addEventListener("click",function(e){var b=e.target.closest(".wth-f");if(!b)return;st[i]=b.getAttribute("data-val");'
      '[].forEach.call(g.querySelectorAll(".wth-f"),function(x){x.setAttribute("aria-pressed",x===b?"true":"false");});run();});});'
      'document.getElementById("wth-clear").addEventListener("click",function(){[].forEach.call(grp,function(g,i){st[i]="all";[].forEach.call(g.querySelectorAll(".wth-f"),function(x){x.setAttribute("aria-pressed",x.getAttribute("data-val")=="all"?"true":"false");});});run();});})();</script>')
secs = ''.join(
    f'<div class="wth-hub" id="{slug(h)}"><h3><a href="{E_(hp)}">{E_(h)}</a></h3>{summary(rows)}<table class="help-table wth-table"><thead><tr>'
    '<th scope="col">Solution</th><th scope="col">Organization</th><th scope="col">Donate</th><th scope="col">Offer to Help</th></tr></thead>'
    f'<tbody>{"".join(rows)}</tbody></table></div>' for (hp, h), rows in groups.items())
N = stats['total']
BLOCK = ('<!-- WTH-ALL:START -->' + '<style>.help-note{display:block;font-size:.85rem;opacity:.85;text-decoration:none;margin:.15rem 0 0}.wth-jump ul{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem 1rem;padding:0;margin:1rem 0 1.5rem}.wth-hub{scroll-margin-top:90px}.wth-hub h3{margin:2rem 0 .4rem}.wth-table td:first-child{min-width:12rem}.help-table th{text-decoration:none}.wth-sum{list-style:none;display:flex;flex-wrap:wrap;gap:.5rem;padding:0;margin:.2rem 0 .8rem}.wth-sum li{border:1px solid rgba(127,127,127,.35);border-radius:10px;padding:.35rem .7rem;font-size:.9rem}.wth-sum b{font-size:1.1rem;margin-inline-end:.25rem}.wth-filters{border:1px solid rgba(127,127,127,.35);border-radius:12px;padding:.8rem 1rem;margin:0 0 1.5rem}.wth-frow{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem;margin:.3rem 0}.wth-fl{font-weight:700;margin-inline-end:.4rem}.wth-f{font:inherit;font-size:.9rem;padding:.35rem .75rem;border-radius:999px;border:1px solid currentColor;background:transparent;color:inherit;cursor:pointer;min-height:36px}.wth-f[aria-pressed=true]{background:#1b6e4b;border-color:#1b6e4b;color:#fff}.wth-f:focus-visible,.wth-clear:focus-visible{outline:3px solid #f5b400;outline-offset:2px}.wth-count{margin:.6rem 0 .3rem;font-weight:600}.wth-hub[hidden],.wth-table tr[hidden],[hidden].wth-none,.wth-filters[hidden]{display:none}</style>' + '<section class="five-ws" id="donate"><h2>Every Solution, Every Way to Help</h2>'
         '<p>Every solution on Saving Planets, grouped by hub. Each row links to the solution&#x27;s page, the organization&#x27;s official donation page and its official volunteer, get-involved or careers page.</p>'
         f'<nav class="wth-jump" aria-label="Jump to a hub"><ul>{jump}</ul></nav>{FILTERS}{secs}{JS}</section>\n'
         '<section class="impact" id="solution"><h2>How This Works</h2><div class="impact-box"><p>Saving Planets doesn&#x27;t take donations and doesn&#x27;t receive any of the money. Every Donate button goes straight to the organization&#x27;s own official page, and every Offer to Help button goes to its own volunteer, get-involved or careers page. When an organization has no donation or volunteer page, the button goes to its official contact page instead, and the row says so. Many space agencies don&#x27;t take donations, but NASA invites anyone to help with real research through its citizen science projects.</p></div></section><!-- WTH-ALL:END -->')
f = 'Ways_to_Help.html'; s = open(f, encoding='utf8').read(); o = s
if '<!-- WTH-ALL:START -->' in s:
    s = re.sub(r'<!-- WTH-ALL:START -->.*?<!-- WTH-ALL:END -->', lambda m: BLOCK, s, flags=re.S)
else:  # first run: replace the old Donate or Volunteer / How This Works / Join the Team / Citizen Science sections
    a = s.index('<section class="five-ws" id="donate">'); b = s.index('<!-- B4-WTH:START -->')
    s = s[:a] + BLOCK + '\n' + s[b:]
if s != o: open(f, 'w', encoding='utf8').write(s)
print(f'ways to help: {N} solutions, {len(groups)} hubs; no donate page: {len(stats["no_donate"])}; no volunteer page: {len(stats["no_help"])}', 'updated' if s != o else 'unchanged')
