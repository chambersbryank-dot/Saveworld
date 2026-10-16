#!/usr/bin/env python3
"""Oct 15, 2026 (Top-10 #1): curriculum standards + grade/subject browsing. Data: assets/data/standards.json (real NGSS and
Common Core codes, official English text, tagged per hub with page overrides). Renders, in en/fr/es/ar/it:
  - a 'Standards Alignment' block inside every solution page's For Teachers box (marker STANDARDS)
  - grade/subject filter chips + data attributes on Teachers.html (marker T-BROWSE)
  - a 'Standards by hub' table on Lesson_Builder.html (marker LB-STD)
Idempotent. Run after i18n-build (all languages), before build-ux.py."""
import re, os, json, html, glob
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)
D = json.load(open('assets/data/standards.json', encoding='utf8'))
LANGS = ['en'] + [l for l in ['fr', 'es', 'ar', 'it'] if os.path.isdir(l)]
d = lambda l: '' if l == 'en' else l + '/'
U = {
 'en': dict(h='Standards Alignment', note='U.S. Next Generation Science Standards (NGSS) and Common Core. Official text, in English.', grade='Grade', subject='Subject', all='All',
   subj=dict(earth='Earth & Human Activity', life='Life Science', space='Space Science', literacy='Reading (Common Core)'), browse='Browse by grade and subject', none='No sheets match this filter.', lb='Standards by hub', hub='Hub', codes='Standards'),
 'fr': dict(h='Alignement sur les programmes', note='Normes américaines NGSS (Next Generation Science Standards) et Common Core. Texte officiel, en anglais.', grade='Niveau', subject='Matière', all='Tout',
   subj=dict(earth='La Terre et les activités humaines', life='Sciences de la vie', space="Sciences de l'espace", literacy='Lecture (Common Core)'), browse='Parcourir par niveau et matière', none='Aucune fiche ne correspond à ce filtre.', lb='Normes par pôle', hub='Pôle', codes='Normes'),
 'es': dict(h='Alineación con estándares', note='Estándares de EE. UU.: Next Generation Science Standards (NGSS) y Common Core. Texto oficial, en inglés.', grade='Grado', subject='Materia', all='Todo',
   subj=dict(earth='La Tierra y la actividad humana', life='Ciencias de la vida', space='Ciencias del espacio', literacy='Lectura (Common Core)'), browse='Explorar por grado y materia', none='Ninguna ficha coincide con este filtro.', lb='Estándares por centro', hub='Centro', codes='Estándares'),
 'ar': dict(h='التوافق مع المعايير', note='معايير أمريكية: معايير العلوم للجيل القادم (NGSS) وCommon Core. النص الرسمي باللغة الإنجليزية.', grade='الصف', subject='المادة', all='الكل',
   subj=dict(earth='الأرض والنشاط البشري', life='علوم الحياة', space='علوم الفضاء', literacy='القراءة (Common Core)'), browse='تصفح حسب الصف والمادة', none='لا توجد أوراق تطابق هذا التصفية.', lb='المعايير حسب المركز', hub='المركز', codes='المعايير'),
 'it': dict(h='Allineamento agli standard', note='Standard statunitensi: Next Generation Science Standards (NGSS) e Common Core. Testo ufficiale, in inglese.', grade='Classe', subject='Materia', all='Tutto',
   subj=dict(earth="La Terra e l'attività umana", life='Scienze della vita', space='Scienze dello spazio', literacy='Lettura (Common Core)'), browse='Sfoglia per classe e materia', none='Nessuna scheda corrisponde a questo filtro.', lb='Standard per hub', hub='Hub', codes='Standard'),
}
BANDS = ['K-2', '3-5', '6-8', '9-12']
def primary_hubs():
    s = rd('Solutions.html'); out = {}
    for m in re.finditer(r'<section ([^>]*class="card-band sol-hub"[^>]*)>(.*?)</section>', s, re.S):
        h = re.search(r'data-hub="([^"]+)"', m.group(1)).group(1)
        for u in re.findall(r'data-url="([^"#]+)"', m.group(2)): out.setdefault(u, h)
    return out
PH = primary_hubs()
def codes_for(page):
    return D['pages'].get(page) or D['hubs'].get(PH.get(page, ''), [])
def short(c): return c.replace('CCSS.ELA-LITERACY.', 'CCSS ')
def block(l, page):
    cs = codes_for(page)
    if not cs: return ''
    u = U[l]
    lis = ''.join(f'<li><a href="{D["codes"][c]["url"]}" target="_blank" rel="noopener"><strong>{esc(short(c))}</strong></a> <span class="std-band">({u["grade"]} {D["codes"][c]["band"]})</span> <span lang="en">{esc(D["codes"][c]["text"])}</span></li>' for c in cs)
    return f'<!-- STANDARDS:START --><div class="std-box"><h3>{esc(u["h"])}</h3><p class="std-note">{esc(u["note"])}</p><ul class="std-list">{lis}</ul></div><!-- STANDARDS:END -->'
def put(s, name, new, before):
    s = re.sub(r'<!-- %s:START -->.*?<!-- %s:END -->' % (name, name), '', s, flags=re.S)
    if not new: return s
    i = s.find(before)
    return s if i < 0 else s[:i] + new + s[i:]
CSS = """/* STD:START */
.std-box{margin:1rem 0;padding:.9rem 1rem;border-radius:14px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.05)}
.std-box h3{margin:.1rem 0 .3rem}.std-note{font-size:.85rem;opacity:.85;margin:.2rem 0 .5rem}.std-list{margin:0;padding-inline-start:1.1rem}.std-list li{margin:.35rem 0}.std-band{opacity:.8;font-size:.9em}
.t-browse{margin:1rem auto 1.4rem;padding-inline:1.3rem;max-width:1200px}.t-browse fieldset{border:0;padding:0;margin:.4rem 0;display:flex;flex-wrap:wrap;gap:.45rem;align-items:center}.t-browse legend{font-weight:700;margin-inline-end:.4rem;float:inline-start}
.t-chip{border-radius:999px;border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.08);color:inherit;padding:.4rem .85rem;font:inherit;cursor:pointer;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.t-chip[aria-pressed=true]{background:#0b6fa4;border-color:#7fd0ff;color:#fff}.t-codes{display:block;font-size:.8rem;opacity:.8}.t-none{font-style:italic}
.lb-std table{width:100%;border-collapse:collapse}.lb-std th,.lb-std td{border-bottom:1px solid rgba(255,255,255,.15);padding:.45rem;text-align:start;vertical-align:top}
@media print{.t-browse{display:none}}
/* STD:END */"""
JS = """<script>(function(){var b=document.querySelector('.t-browse');if(!b)return;var g='all',s='all';
function run(){var any=0;document.querySelectorAll('.t-list li').forEach(function(li){var ok=(g==='all'||(' '+li.getAttribute('data-grades')+' ').indexOf(' '+g+' ')>-1)&&(s==='all'||(' '+li.getAttribute('data-subjects')+' ').indexOf(' '+s+' ')>-1);li.hidden=!ok;if(ok)any=1});
document.querySelectorAll('.t-hub').forEach(function(h){h.hidden=!h.querySelector('.t-list li:not([hidden])')});var n=document.querySelector('.t-none');if(n)n.hidden=!!any;
var q=new URLSearchParams(location.search);g==='all'?q.delete('grade'):q.set('grade',g);s==='all'?q.delete('subject'):q.set('subject',s);history.replaceState(null,'',location.pathname+(q.toString()?'?'+q:'')+location.hash)}
b.addEventListener('click',function(e){var c=e.target.closest('.t-chip');if(!c)return;var k=c.getAttribute('data-k');b.querySelectorAll('.t-chip[data-k="'+k+'"]').forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false')});if(k==='g')g=c.getAttribute('data-v');else s=c.getAttribute('data-v');run()});
function init(){var q=new URLSearchParams(location.search);['grade','subject'].forEach(function(p,i){var v=q.get(p);if(!v)return;var c=b.querySelector('.t-chip[data-k="'+(i?'s':'g')+'"][data-v="'+v+'"]');if(c)c.click()})}if(document.readyState==='complete')setTimeout(init,0);else window.addEventListener('load',function(){setTimeout(init,0)})})();</script>"""
def teachers(l):
    p = d(l) + 'Teachers.html'
    if not os.path.exists(p): return 0
    s = rd(p); u = U[l]
    def li(m):
        t = m.group(0); href = re.search(r'<a href="([^"#]+)#teachers"', t)
        t = re.sub(r'^<li[^>]*>', '<li>', t); t = re.sub(r'<span class="t-codes">.*?</span>', '', t)
        if not href: return t
        cs = codes_for(href.group(1)); g = sorted({D['codes'][c]['band'] for c in cs}, key=BANDS.index); sj = sorted({D['codes'][c]['subject'] for c in cs})
        t = t.replace('<li>', f'<li data-grades="{" ".join(g)}" data-subjects="{" ".join(sj)}">', 1)
        return t[:-5] + (f'<span class="t-codes">{esc(", ".join(short(c) for c in cs))}</span>' if cs else '') + '</li>'
    s = re.sub(r'<li>(?:(?!</li>).)*?#teachers".*?</li>|<li data-grades[^>]*>.*?</li>', li, s, flags=re.S)
    chips = lambda k, vals: ''.join(f'<button type="button" class="t-chip" data-k="{k}" data-v="{v}" aria-pressed="{"true" if v == "all" else "false"}">{esc(lab)}</button>' for v, lab in vals)
    ui = (f'<!-- T-BROWSE:START --><section class="t-browse" aria-labelledby="tb-h"><h2 id="tb-h">{esc(u["browse"])}</h2>'
          f'<fieldset><legend>{esc(u["grade"])}</legend>{chips("g", [("all", u["all"])] + [(b, b) for b in BANDS])}</fieldset>'
          f'<fieldset><legend>{esc(u["subject"])}</legend>{chips("s", [("all", u["all"])] + list(u["subj"].items()))}</fieldset>'
          f'<p class="std-note">{esc(u["note"])}</p><p class="t-none" hidden>{esc(u["none"])}</p></section>{JS}<!-- T-BROWSE:END -->')
    s = put(s, 'T-BROWSE', ui, '<section class="five-ws t-hub">')
    return wr(p, s)
def lesson(l):
    p = d(l) + 'Lesson_Builder.html'
    if not os.path.exists(p): return 0
    s = rd(p); u = U[l]
    names = {}
    for m in re.finditer(r'<section ([^>]*class="card-band sol-hub"[^>]*)>.*?<h2><a[^>]*>(.*?)</a>', rd(d(l) + 'Solutions.html'), re.S):
        names[re.search(r'data-hub="([^"]+)"', m.group(1)).group(1)] = re.sub('<[^>]+>', '', m.group(2))
    rows = ''.join(f'<tr><td><a href="{h}">{names.get(h, h)}</a></td><td>' + ', '.join(f'<a href="{D["codes"][c]["url"]}" target="_blank" rel="noopener" title="{esc(D["codes"][c]["text"])}">{esc(short(c))}</a>' for c in cs) + '</td></tr>'
                   for h, cs in sorted(D['hubs'].items(), key=lambda x: names.get(x[0], x[0]).lower()))
    blk = (f'<!-- LB-STD:START --><section class="five-ws lb-std" aria-labelledby="lbs-h"><h2 id="lbs-h">{esc(u["lb"])}</h2><p class="std-note">{esc(u["note"])}</p>'
           f'<table><thead><tr><th scope="col">{esc(u["hub"])}</th><th scope="col">{esc(u["codes"])}</th></tr></thead><tbody>{rows}</tbody></table></section><!-- LB-STD:END -->')
    return wr(p, put(s, 'LB-STD', blk, '</main>'))
def main():
    n = 0
    for l in LANGS:
        for p in glob.glob(d(l) + '*.html'):
            s = rd(p)
            if '<!-- TEACHER:END -->' not in s: continue
            page = os.path.basename(p)
            s2 = put(s, 'STANDARDS', block(l, page), '</section><!-- TEACHER:END -->')
            n += wr(p, s2)
        n += teachers(l) + lesson(l)
    css = rd('styles.css'); css = re.sub(r'\n?/\* STD:START \*/.*?/\* STD:END \*/', '', css, flags=re.S).rstrip('\n') + '\n' + CSS + '\n'
    if css != rd('styles.css'): open('styles.css', 'w', encoding='utf8').write(css)
    tagged = sum(1 for u in PH if codes_for(u))
    print(f'build-standards: {n} page writes; {tagged}/{len(PH)} solutions tagged')
if __name__ == '__main__': main()
