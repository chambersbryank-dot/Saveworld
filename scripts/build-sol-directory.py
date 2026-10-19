#!/usr/bin/env python3
"""Oct 15, 2026 (Top-10 #4): Solutions directory filters (all languages). Adds data-status / data-region / data-grades to every
Solutions.html card (from assets/data/map-locations.json and assets/data/standards.json) and a filter row (status, region, grade,
live count, URL state; Oct 18: the name filter box was removed with the page search, owner request) after the existing domain/hub filters (marker SOL-DIR). Regions come only from verified map
pins: Americas, Europe & Africa, Asia & Oceania, plus 'From orbit' and 'Worldwide' for unpinned/space solutions.
Every solution exists in all 5 languages, so language is offered as links (same filters kept), not as a filter.
Idempotent. Run after build-standards.py and before build-ux.py."""
import re, os, json, html
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)
LANGS = ['en'] + [l for l in ['fr', 'es', 'ar', 'it'] if os.path.isdir(l)]
d = lambda l: '' if l == 'en' else l + '/'
LOC = json.load(open('assets/data/map-locations.json', encoding='utf8'))['solutions']
STD = json.load(open('assets/data/standards.json', encoding='utf8'))
BANDS = ['K-2', '3-5', '6-8', '9-12']
def region(lat, lng):
    if lng < -25 and not (lat < 0 and lng < -120): return 'americas'
    if lng < 60 and lng >= -25: return 'eurafrica'
    return 'asiaoceania'
def primary_hubs():
    s = rd('Solutions.html'); out = {}
    for m in re.finditer(r'<section ([^>]*class="card-band sol-hub"[^>]*)>(.*?)</section>', s, re.S):
        h = re.search(r'data-hub="([^"]+)"', m.group(1)).group(1)
        for u in re.findall(r'data-url="([^"#]+)"', m.group(2)): out.setdefault(u, h)
    return out
PH = primary_hubs()
def attrs(u):
    e = LOC.get(u, {}); st = e.get('status', 'active')
    regs = sorted({region(p['lat'], p['lng']) for p in e.get('pins', []) if p.get('basis') != 'launch'})
    if e.get('strip') == 'orbit': regs.append('orbit')
    if e.get('strip') == 'world' or (not regs): regs.append('world')
    cs = STD['pages'].get(u) or STD['hubs'].get(PH.get(u, ''), [])
    g = sorted({STD['codes'][c]['band'] for c in cs}, key=BANDS.index)
    return st, ' '.join(dict.fromkeys(regs)), ' '.join(g)
U = {
 'en': dict(status='Status', all='All', active='Active now', upcoming='Coming soon', region='Region', americas='Americas', eurafrica='Europe & Africa', asiaoceania='Asia & Oceania', orbit='From orbit', world='Worldwide', grade='Grade', name='Filter by name', count='{n} solutions shown', none='No solutions match these filters.', reset='Reset filters', lang='Also in'),
 'fr': dict(status='Statut', all='Tout', active='Actives', upcoming='Bientôt', region='Région', americas='Amériques', eurafrica='Europe et Afrique', asiaoceania='Asie et Océanie', orbit="Depuis l'orbite", world='Partout dans le monde', grade='Niveau', name='Filtrer par nom', count='{n} solutions affichées', none='Aucune solution ne correspond à ces filtres.', reset='Réinitialiser', lang='Aussi en'),
 'es': dict(status='Estado', all='Todo', active='Activas', upcoming='Próximamente', region='Región', americas='Américas', eurafrica='Europa y África', asiaoceania='Asia y Oceanía', orbit='Desde la órbita', world='En todo el mundo', grade='Grado', name='Filtrar por nombre', count='{n} soluciones mostradas', none='Ninguna solución coincide con estos filtros.', reset='Restablecer', lang='También en'),
 'ar': dict(status='الحالة', all='الكل', active='تعمل الآن', upcoming='قريبًا', region='المنطقة', americas='الأمريكتان', eurafrica='أوروبا وأفريقيا', asiaoceania='آسيا وأوقيانوسيا', orbit='من المدار', world='حول العالم', grade='الصف', name='تصفية حسب الاسم', count='عدد الحلول المعروضة: {n}', none='لا توجد حلول تطابق هذه التصفية.', reset='إعادة الضبط', lang='متاح أيضًا بـ'),
 'it': dict(status='Stato', all='Tutto', active='Attive', upcoming='In arrivo', region='Regione', americas='Americhe', eurafrica='Europa e Africa', asiaoceania='Asia e Oceania', orbit="Dall'orbita", world='In tutto il mondo', grade='Classe', name='Filtra per nome', count='{n} soluzioni mostrate', none='Nessuna soluzione corrisponde a questi filtri.', reset='Reimposta', lang='Anche in'),
}
NAMES = {'en': 'English', 'fr': 'Français', 'es': 'Español', 'ar': 'العربية', 'it': 'Italiano'}
JS = """<script>document.addEventListener('DOMContentLoaded',function(){var w=document.querySelector('.sol-dir');if(!w)return;var cards=[].slice.call(document.querySelectorAll('.sol-card[data-status]')),hubs=[].slice.call(document.querySelectorAll('.sol-hub')),S={status:'all',region:'all',grade:'all',q:''},cnt=w.querySelector('.sd-count'),none=w.querySelector('.sd-none'),inp=w.querySelector('input');
function has(a,v){return (' '+(a||'')+' ').indexOf(' '+v+' ')>-1}
function run(){var on=S.status!=='all'||S.region!=='all'||S.grade!=='all'||S.q,n=0,q=S.q.toLowerCase();document.body.classList.toggle('sd-on',!!on);
cards.forEach(function(c){var ok=(S.status==='all'||c.dataset.status===S.status)&&(S.region==='all'||has(c.dataset.region,S.region))&&(S.grade==='all'||has(c.dataset.grades,S.grade))&&(!q||c.textContent.toLowerCase().indexOf(q)>-1);c.classList.toggle('sd-off',!ok);if(ok&&c.closest('.sol-hub').style.display!=='none')n++});
hubs.forEach(function(h){h.classList.toggle('sd-empty',!!on&&!h.querySelector('.sol-card:not(.sd-off)'))});cnt.textContent=cnt.dataset.t.replace('{n}',n);none.hidden=n>0;
var p=new URLSearchParams(location.search);['status','region','grade','q'].forEach(function(k){S[k]&&S[k]!=='all'?p.set(k,S[k]):p.delete(k)});history.replaceState(null,'',location.pathname+(p.toString()?'?'+p:'')+location.hash);
w.querySelectorAll('.sd-lang a').forEach(function(a){a.search=p.toString()?'?'+p:''})}
w.addEventListener('change',function(e){if(e.target.name&&S.hasOwnProperty(e.target.name)){S[e.target.name]=e.target.value;run()}});
if(inp)inp.addEventListener('input',function(){S.q=inp.value.trim();run()});
w.querySelector('.sd-reset').addEventListener('click',function(){S={status:'all',region:'all',grade:'all',q:''};w.querySelectorAll('select').forEach(function(s){s.value='all'});if(inp)inp.value='';run()});
document.querySelectorAll('.sol-filters button,.sol-filters select').forEach(function(b){b.addEventListener(b.tagName==='SELECT'?'change':'click',function(){setTimeout(run,0)})});
function init(){var p=new URLSearchParams(location.search);['status','region','grade'].forEach(function(k){var v=p.get(k),s=w.querySelector('select[name='+k+']');if(v&&s&&[].some.call(s.options,function(o){return o.value===v})){s.value=v;S[k]=v}});if(inp&&p.get('q')){S.q=inp.value=p.get('q')}run()}
if(document.readyState==='complete')setTimeout(init,0);else addEventListener('load',function(){setTimeout(init,0)})});</script>"""
CSS = """/* SD:START */
.sol-dir{display:flex;flex-wrap:wrap;gap:.6rem 1rem;align-items:flex-end;margin:.8rem auto 1rem;max-width:1200px;padding:0 1rem}
.sol-dir label{display:flex;flex-direction:column;font-size:.85rem;gap:.2rem;font-weight:600}
.sol-dir select,.sol-dir input{font:inherit;font-size:1rem;min-height:44px;border-radius:12px;padding:.35rem .7rem;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);color:inherit}
.sol-dir select option{color:#003755}.sol-dir input{min-width:12rem}.sd-reset{min-height:44px;border-radius:999px;padding:.35rem 1rem;font:inherit;border:1px solid rgba(255,255,255,.35);background:transparent;color:inherit;cursor:pointer}
.sd-meta{flex-basis:100%;display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;font-size:.9rem}.sd-lang a{margin-inline-end:.5rem}
.sol-card.sd-off,.sol-hub.sd-empty{display:none !important}
body.sd-on .sp-collapsed .grid>.sol-card:not(.sd-off){display:block !important}body.sd-on .sp-more{display:none}
/* SD:END */"""
def ui(l):
    u = U[l]
    sel = lambda name, lab, opts: f'<label>{esc(lab)}<select name="{name}"><option value="all">{esc(u["all"])}</option>' + ''.join(f'<option value="{v}">{esc(t)}</option>' for v, t in opts) + '</select></label>'
    langs = ''.join(f'<a href="{("../" if l != "en" else "") + (x + "/" if x != "en" else "")}Solutions.html" hreflang="{x}" lang="{x}">{NAMES[x]}</a>' for x in LANGS if x != l)
    return (f'<!-- SOL-DIR:START --><div class="sol-dir" role="search">'
            + sel('status', u['status'], [('active', u['active']), ('upcoming', u['upcoming'])])
            + sel('region', u['region'], [(k, u[k]) for k in ('americas', 'eurafrica', 'asiaoceania', 'orbit', 'world')])
            + sel('grade', u['grade'], [(b, b) for b in BANDS])
            + f'<button type="button" class="sd-reset">{esc(u["reset"])}</button>'
            f'<p class="sd-meta"><span class="sd-count" role="status" aria-live="polite" data-t="{esc(u["count"])}"></span><span class="sd-lang">{esc(u["lang"])}: {langs}</span></p>'
            f'<p class="sd-none" hidden>{esc(u["none"])}</p></div>{JS}<!-- SOL-DIR:END -->')
def main():
    n = 0
    for l in LANGS:
        p = d(l) + 'Solutions.html'; s = rd(p)
        def card(m):
            t = re.sub(r' data-(?:status|region|grades)="[^"]*"', '', m.group(0)); u = re.search(r'data-url="(?:\.\./)?([^"#]+)"', t).group(1)
            st, rg, g = attrs(u); return t[:-1] + f' data-status="{st}" data-region="{rg}" data-grades="{g}">'
        s = re.sub(r'<article class="card sol-card"[^>]*>', card, s)
        s = re.sub(r'<!-- SOL-DIR:START -->.*?<!-- SOL-DIR:END -->', '', s, flags=re.S)
        s = s.replace('<!-- SOL-FILTERS:END -->', '<!-- SOL-FILTERS:END -->' + ui(l), 1)
        n += wr(p, s)
    css = rd('styles.css'); css = re.sub(r'\n?/\* SD:START \*/.*?/\* SD:END \*/', '', css, flags=re.S).rstrip('\n') + '\n' + CSS + '\n'
    if css != rd('styles.css'): open('styles.css', 'w', encoding='utf8').write(css)
    print(f'build-sol-directory: {n} pages')
if __name__ == '__main__': main()
