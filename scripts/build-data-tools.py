#!/usr/bin/env python3
"""Oct 15, 2026 (Top-10 #3): citable, embeddable, downloadable data, all languages. Real site data only.
  - CSVs in assets/data/export/: facts.<l>.csv (Amazing Facts + their cited sources), myths.<l>.csv (Myth vs Fact + sources),
    map.<l>.csv (World Map solutions, status, hub, pins), scoreboard.csv (homepage counts, from assets/data/solutions.json)
  - a 'Use this data' bar (Download CSV · Cite APA/MLA · Embed) on Amazing_Facts, Myth_vs_Fact, World_Map and the homepage
    Scoreboard (marker DATA-TOOLS), and a small per-item Cite button on every fact and myth card (stable ids fact-<slug>).
Idempotent. Run after build-map.py (needs map.<lang>.json) and before build-ux.py."""
import re, os, json, html, csv, io
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if os.path.exists(p) and rd(p) == s: return 0
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True); open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)
txt = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
SITE = 'https://www.savingplanets.com/'
LANGS = ['en'] + [l for l in ['fr', 'es', 'ar', 'it'] if os.path.isdir(l)]
d = lambda l: '' if l == 'en' else l + '/'
U = {'en': dict(use='Use this data', csv='Download CSV', cite='Cite', embed='Embed', copy='Copy', copied='Copied', apa='APA', mla='MLA', note='Free to reuse with a link back. Each row keeps its original source.'),
     'fr': dict(use='Utiliser ces données', csv='Télécharger le CSV', cite='Citer', embed='Intégrer', copy='Copier', copied='Copié', apa='APA', mla='MLA', note='Réutilisation libre avec un lien vers nous. Chaque ligne garde sa source d’origine.'),
     'es': dict(use='Usar estos datos', csv='Descargar CSV', cite='Citar', embed='Insertar', copy='Copiar', copied='Copiado', apa='APA', mla='MLA', note='Libre de reutilizar con un enlace a nosotros. Cada fila conserva su fuente original.'),
     'ar': dict(use='استخدم هذه البيانات', csv='تنزيل CSV', cite='استشهد', embed='تضمين', copy='نسخ', copied='تم النسخ', apa='APA', mla='MLA', note='يمكن إعادة الاستخدام مجانًا مع رابط إلينا. يحتفظ كل صف بمصدره الأصلي.'),
     'it': dict(use='Usa questi dati', csv='Scarica CSV', cite='Cita', embed='Incorpora', copy='Copia', copied='Copiato', apa='APA', mla='MLA', note='Riutilizzo libero con un link a noi. Ogni riga mantiene la sua fonte originale.')}
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60] or 'item'
def to_csv(rows):
    b = io.StringIO(); w = csv.writer(b, lineterminator='\n'); [w.writerow(r) for r in rows]; return '\ufeff' + b.getvalue()
def put(s, name, new, before=None, after=None):
    s = re.sub(r'<!-- %s:START -->.*?<!-- %s:END -->' % (name, name), '', s, flags=re.S)
    if before:
        i = s.find(before)
        if i < 0: i = s.find('</main>')
        return s if i < 0 else s[:i] + new + s[i:]
    i = s.find(after); return s if i < 0 else s[:i + len(after)] + new + s[i + len(after):]
JS = """<script>(function(){if(window.__dt)return;window.__dt=1;function m(){return new Date().toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'})}
function cites(t,u){var y=new Date().toISOString().slice(0,10);return{apa:'Saving Planets. (n.d.). '+t+'. Retrieved '+m()+', from '+u,mla:'"'+t+'." Saving Planets, '+u+'. Accessed '+new Date().toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'})+'.'}}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-dt]');if(!b)return;var w=b.closest('[data-dt-title]'),t=w.getAttribute('data-dt-title'),u=w.getAttribute('data-dt-url'),o=w.querySelector('.dt-out');
if(b.dataset.dt==='cite'||b.dataset.dt==='embed'){var c=cites(t,u),v=b.dataset.dt==='cite'?('APA: '+c.apa+'\\nMLA: '+c.mla):'<iframe src="'+u.split('#')[0]+'" title="'+t.replace(/"/g,'&quot;')+'" width="100%" height="600" loading="lazy" style="border:0"></iframe>';o.hidden=false;o.querySelector('textarea').value=v;o.querySelector('textarea').focus();o.querySelector('textarea').select()}
if(b.dataset.dt==='copy'){var ta=o.querySelector('textarea');(navigator.clipboard?navigator.clipboard.writeText(ta.value):Promise.reject()).then(function(){b.textContent=b.dataset.ok},function(){ta.select();document.execCommand&&document.execCommand('copy');b.textContent=b.dataset.ok})}})})();</script>"""
CSS = """/* DT:START */
.dt-bar{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:1rem auto;max-width:1200px;padding:.6rem 1rem}
.dt-bar h2{font-size:1rem;margin:0 .4rem 0 0}.dt-note{flex-basis:100%;font-size:.82rem;opacity:.8;margin:0}
.dt-btn{display:inline-flex;align-items:center;gap:.3rem;border-radius:999px;border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.08);color:inherit !important;padding:.4rem .85rem;font:inherit;font-size:.9rem;cursor:pointer;text-decoration:none !important;min-height:40px;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.dt-mini{display:inline-flex;gap:.4rem;margin-top:.4rem}.dt-mini .dt-btn{font-size:.78rem;padding:.2rem .6rem;min-height:32px}
.dt-out{flex-basis:100%;margin-top:.4rem}.dt-out textarea{width:100%;min-height:5.5em;font:inherit;font-size:.82rem;border-radius:10px;padding:.5rem;background:rgba(0,0,0,.25);color:inherit;border:1px solid rgba(255,255,255,.25)}
@media print{.dt-bar,.dt-mini{display:none}}
/* DT:END */"""
def bar(l, title, url, csvhref):
    u = U[l]
    return (f'<!-- DATA-TOOLS:START --><section class="dt-bar" aria-label="{esc(u["use"])}" data-dt-title="{esc(title)}" data-dt-url="{esc(url)}"><h2>{esc(u["use"])}</h2>'
            + (f'<a class="dt-btn" href="{csvhref}" download>⬇ {esc(u["csv"])}</a>' if csvhref else '')
            + f'<button type="button" class="dt-btn" data-dt="cite">❝ {esc(u["cite"])}</button><button type="button" class="dt-btn" data-dt="embed">&lt;/&gt; {esc(u["embed"])}</button>'
            f'<div class="dt-out" hidden><textarea readonly dir="ltr" aria-label="{esc(u["cite"])} / {esc(u["embed"])}"></textarea><button type="button" class="dt-btn" data-dt="copy" data-ok="{esc(u["copied"])}">{esc(u["copy"])}</button></div>'
            f'<p class="dt-note">{esc(u["note"])}</p></section>{JS}<!-- DATA-TOOLS:END -->')
def mini(l, title, url):
    u = U[l]
    return (f'<span class="dt-mini" data-dt-title="{esc(title)}" data-dt-url="{esc(url)}"><button type="button" class="dt-btn" data-dt="cite">❝ {esc(u["cite"])}</button>'
            f'<span class="dt-out" hidden><textarea readonly dir="ltr" aria-label="{esc(u["cite"])}"></textarea><button type="button" class="dt-btn" data-dt="copy" data-ok="{esc(u["copied"])}">{esc(u["copy"])}</button></span></span>')
def pagetitle(s): return txt(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
def facts(l):
    p = d(l) + 'Amazing_Facts.html'
    if not os.path.exists(p): return 0
    s = rd(p); rows = [['title', 'fact', 'source_name', 'source_url', 'saving_planets_page', 'permalink']]; seen = {}
    s = re.sub(r'<span class="dt-mini".*?</span></span>', '', s, flags=re.S)
    def card(m):
        c = m.group(0); t = txt(re.search(r'<h3>(.*?)</h3>', c, re.S).group(1)); k = slug(t); seen[k] = seen.get(k, 0) + 1
        if seen[k] > 1: k = f'{k}-{seen[k]}'
        c = re.sub(r' id="fact-[^"]*"', '', c, count=1).replace('<div class="w-card"', f'<div class="w-card" id="fact-{k}"', 1)
        body = next((txt(x) for x in re.findall(r'<p>(.*?)</p>', c, re.S)), '')
        src = re.findall(r'<p class="fact-source">[^<]*<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', c, re.S)
        sp = re.search(r'<p class="fact-source">[^<]*<a href="([^"h][^"]*\.html)"', c)
        url = f'{SITE}{d(l)}Amazing_Facts.html#fact-{k}'
        for su, sn in (src or [('', '')]): rows.append([t, body, txt(sn), su, (SITE + d(l) + sp.group(1)) if sp else '', url])
        i = c.rfind('</div>'); return c[:i] + mini(l, t, url) + c[i:]
    s = re.sub(r'<div class="w-card"[^>]*>.*?</div>(?=\s*(?:<div class="w-card"|<!-- FACTS:END|</div>))', card, s, flags=re.S)
    n = wr(f'assets/data/export/facts.{l}.csv', to_csv(rows))
    s = put(s, 'DATA-TOOLS', bar(l, pagetitle(s), f'{SITE}{d(l)}Amazing_Facts.html', ('' if l == 'en' else '../') + f'assets/data/export/facts.{l}.csv'), before='<section class="five-ws" id="solution"')
    return n + wr(p, s)
def myths(l):
    p = d(l) + 'Myth_vs_Fact.html'
    if not os.path.exists(p): return 0
    s = rd(p); rows = [['myth', 'fact', 'source_name', 'source_url', 'permalink']]
    s = re.sub(r'<span class="dt-mini".*?</span></span>', '', s, flags=re.S)
    def card(m):
        c = m.group(0); mid = re.search(r'id="([^"]+)"', c).group(1); my = txt(re.search(r'<h2>(.*?)</h2>', c, re.S).group(1))
        fa = txt(re.search(r'myth-tag-fact">[^<]*</p>\s*<p>(.*?)</p>', c, re.S).group(1)) if re.search(r'myth-tag-fact">[^<]*</p>\s*<p>', c) else ''
        url = f'{SITE}{d(l)}Myth_vs_Fact.html#{mid}'
        for su, sn in (re.findall(r'<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', re.search(r'<p class="myth-source">.*?</p>', c, re.S).group(0)) if 'myth-source' in c else [('', '')]):
            rows.append([my, fa, txt(sn), su, url])
        return c.replace('</article>', mini(l, my, url) + '</article>', 1)
    s = re.sub(r'<article class="myth-card".*?</article>', card, s, flags=re.S)
    if len(rows) == 1: return 0  # page has no myth cards in this language yet (not translated); no empty CSV
    n = wr(f'assets/data/export/myths.{l}.csv', to_csv(rows))
    s = put(s, 'DATA-TOOLS', bar(l, pagetitle(s), f'{SITE}{d(l)}Myth_vs_Fact.html', ('' if l == 'en' else '../') + f'assets/data/export/myths.{l}.csv'), before='<article class="myth-card"')
    return n + wr(p, s)
def worldmap(l):
    p = d(l) + 'World_Map.html'; j = f'assets/data/map.{l}.json'
    if not (os.path.exists(p) and os.path.exists(j)): return 0
    data = json.load(open(j, encoding='utf8')); rows = [['solution', 'status', 'hub', 'place', 'lat', 'lng', 'basis', 'page']]
    for x in data['sols']:
        page = SITE + d(l) + re.sub(r'^\.\./', '', x['u']) if l != 'en' and not x['u'].startswith('../') else SITE + re.sub(r'^\.\./', '', x['u'])
        for pin in (x['p'] or [None]):
            rows.append([x['n'], x['st'], x['hn'], pin['label'] if pin else ({'orbit': 'From orbit', 'world': 'Worldwide'}.get(x['x'], '')), pin['lat'] if pin else '', pin['lng'] if pin else '', pin.get('basis', '') if pin else '', page])
    n = wr(f'assets/data/export/map.{l}.csv', to_csv(rows))
    # Oct 17: map-first World Map (user: "remove noise"): no data bar on the page; the CSV is linked from the page's list section instead
    s = rd(p); s = re.sub(r'<!-- DATA-TOOLS:START -->.*?<!-- DATA-TOOLS:END -->', '', s, flags=re.S)
    return n + wr(p, s)
def home(l):
    p = d(l) + 'index.html'; s = rd(p)
    m = re.search(r'<!-- IMPACT:START -->(.*?)<!-- IMPACT:END -->', s, re.S)
    if not m: return 0
    rows = [['figure', 'value', 'source']] + [[txt(b), txt(a), SITE + 'assets/data/solutions.json'] for a, b in re.findall(r'<span class="imp-num">(.*?)</span><span class="imp-label">(.*?)</span>', m.group(1))]
    n = wr(f'assets/data/export/scoreboard.{l}.csv', to_csv(rows))
    t = 'Saving Planets Scoreboard'
    s = put(s, 'DATA-TOOLS', bar(l, t, f'{SITE}{d(l)}index.html', ('' if l == 'en' else '../') + f'assets/data/export/scoreboard.{l}.csv'), after='<!-- IMPACT:END -->')
    return n + wr(p, s)
def main():
    n = 0
    for l in LANGS: n += facts(l) + myths(l) + worldmap(l) + home(l)
    css = rd('styles.css'); css = re.sub(r'\n?/\* DT:START \*/.*?/\* DT:END \*/', '', css, flags=re.S).rstrip('\n') + '\n' + CSS + '\n'
    if css != rd('styles.css'): open('styles.css', 'w', encoding='utf8').write(css)
    print(f'build-data-tools: {n} writes')
if __name__ == '__main__': main()
