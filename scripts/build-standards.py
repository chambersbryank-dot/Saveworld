#!/usr/bin/env python3
"""Oct 15, 2026 (Top-10 #1): curriculum standards + grade/subject browsing. Data: assets/data/standards.json (real NGSS and
Common Core codes, official English text, tagged per hub with page overrides). Renders, in en/fr/es/ar/it/he:
  - a 'Standards Alignment' block inside every solution page's For Teachers box (marker STANDARDS)
  - grade/subject filter chips + data attributes on Teachers.html (marker T-BROWSE)
  - a 'Standards by hub' picker on Lesson_Builder.html (marker LB-STD): one hub at a time, plus a Search prompt
Idempotent. Run after i18n-build (all languages), before build-ux.py."""
import re, os, json, html, glob
rd = lambda f: open(f, encoding='utf8').read()
def wr(p, s):
    if rd(p) == s: return 0
    open(p, 'w', encoding='utf8').write(s); return 1
esc = lambda s: html.escape(s, quote=True)
D = json.load(open('assets/data/standards.json', encoding='utf8'))
LANGS = ['en'] + [l for l in ['fr', 'es', 'ar', 'it', 'he'] if os.path.isdir(l)]
d = lambda l: '' if l == 'en' else l + '/'
U = {
 'en': dict(h='Standards Alignment', note='U.S. Next Generation Science Standards (NGSS) and Common Core. Official text, in English.', grade='Grade', subject='Subject', all='All',
   subj=dict(earth='Earth & Human Activity', life='Life Science', space='Space Science', literacy='Reading (Common Core)'), browse='Browse by grade and subject', none='No sheets match this filter.', lb='Standards by hub', hub='Hub', codes='Standards', pick='Show standards for', search='Search the site', searchNote='Another tool while you build a plan. Use it to discover a related page, or a connection you did not expect across topics and solutions.', empty='No standards are listed for {name}.'),
 'fr': dict(h='Alignement sur les programmes', note='Normes américaines NGSS (Next Generation Science Standards) et Common Core. Texte officiel, en anglais.', grade='Niveau', subject='Matière', all='Tout',
   subj=dict(earth='La Terre et les activités humaines', life='Sciences de la vie', space="Sciences de l'espace", literacy='Lecture (Common Core)'), browse='Parcourir par niveau et matière', none='Aucune fiche ne correspond à ce filtre.', lb='Normes par pôle', hub='Pôle', codes='Normes', pick='Afficher les normes pour', search='Rechercher dans le site', searchNote='Un autre outil pendant que vous préparez un plan. Servez-vous-en pour découvrir une page liée, ou un lien inattendu entre des thèmes et des solutions.', empty="Aucune norme n'est indiquée pour {name}."),
 'es': dict(h='Alineación con estándares', note='Estándares de EE. UU.: Next Generation Science Standards (NGSS) y Common Core. Texto oficial, en inglés.', grade='Grado', subject='Materia', all='Todo',
   subj=dict(earth='La Tierra y la actividad humana', life='Ciencias de la vida', space='Ciencias del espacio', literacy='Lectura (Common Core)'), browse='Explorar por grado y materia', none='Ninguna ficha coincide con este filtro.', lb='Estándares por centro', hub='Centro', codes='Estándares', pick='Ver los estándares de', search='Buscar en el sitio', searchNote='Otra herramienta mientras preparas un plan. Úsala para descubrir una página relacionada, o una conexión inesperada entre temas y soluciones.', empty='No hay estándares listados para {name}.'),
 'ar': dict(h='التوافق مع المعايير', note='معايير أمريكية: معايير العلوم للجيل القادم (NGSS) وCommon Core. النص الرسمي باللغة الإنجليزية.', grade='الصف', subject='المادة', all='الكل',
   subj=dict(earth='الأرض والنشاط البشري', life='علوم الحياة', space='علوم الفضاء', literacy='القراءة (Common Core)'), browse='تصفح حسب الصف والمادة', none='لا توجد أوراق تطابق هذا التصفية.', lb='المعايير حسب المركز', hub='المركز', codes='المعايير', pick='اختر المركز', search='ابحث في الموقع', searchNote='أداة أخرى أثناء إعداد الخطة. استخدمها لاكتشاف صفحة ذات صلة، أو صلة لم تكن تتوقعها بين المواضيع والحلول.', empty='{name}: لا توجد معايير مدرجة.'),
 'it': dict(h='Allineamento agli standard', note='Standard statunitensi: Next Generation Science Standards (NGSS) e Common Core. Testo ufficiale, in inglese.', grade='Classe', subject='Materia', all='Tutto',
   subj=dict(earth="La Terra e l'attività umana", life='Scienze della vita', space='Scienze dello spazio', literacy='Lettura (Common Core)'), browse='Sfoglia per classe e materia', none='Nessuna scheda corrisponde a questo filtro.', lb='Standard per hub', hub='Hub', codes='Standard', pick='Mostra gli standard per', search='Cerca nel sito', searchNote='Un altro strumento mentre prepari un piano. Usala per scoprire una pagina collegata, o un collegamento inatteso tra argomenti e soluzioni.', empty='Nessuno standard è indicato per {name}.'),
 'he': dict(h='התאמה לתקנים', note='תקני ארה״ב: Next Generation Science Standards (NGSS) ו-Common Core. הטקסט הרשמי באנגלית.', grade='כיתה', subject='מקצוע', all='הכול',
   subj=dict(earth='כדור הארץ ופעילות האדם', life='מדעי החיים', space='מדעי החלל', literacy='קריאה (Common Core)'), browse='עיון לפי כיתה ומקצוע', none='אין דפים שתואמים לסינון הזה.', lb='תקנים לפי מרכז', hub='מרכז', codes='תקנים', pick='הצגת תקנים עבור', search='חיפוש באתר', searchNote='כלי נוסף בזמן בניית תוכנית. השתמשו בו כדי לגלות עמוד קשור, או קשר לא צפוי בין נושאים לפתרונות.', empty='אין תקנים רשומים עבור {name}.'),
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
.lb-std-pick{box-sizing:border-box;display:flex;flex-direction:column;align-items:stretch;gap:.35rem;max-width:28rem;margin:.75rem 0 .9rem;padding:1rem 1.1rem;border-radius:20px}
.lb-std-pick label{font-weight:700}.lb-std-pick select{width:100%;min-height:44px;font:inherit;font-size:1rem;border-radius:12px;padding:.4rem .6rem;border:1px solid #9bb;background:#fff;color:#10243a}
.lb-std-pick select:focus-visible,.lb-std a:focus-visible{outline:3px solid #ffd54a;outline-offset:3px}
.lb-std-search{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem 1rem;margin:.15rem 0 1rem;max-width:72ch;line-height:1.5}.lb-std-search span{flex:1 1 18rem}
.lb-std-panel h3{margin:.15rem 0 .4rem}.lb-std-panel .std-list{margin:.2rem 0 0}.lb-std-panel .std-list li{margin:.5rem 0;line-height:1.45}.lb-std-panel .std-list a{font-weight:700;text-decoration:underline}.std-line{unicode-bidi:isolate}
.lb-std-empty{font-style:italic;margin:.3rem 0}
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
    # Nov 11: the Teachers catalog is owned by scripts/build-teachers-home.py (collapsed hubs, no repeated code strings).
    if '<!-- TEACHHOME:START -->' in s:
        return 0
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
def swap(s, name, new, before):
    """Replace a marker block where it already sits. Fall back to inserting before `before`."""
    pat = re.compile(r'<!-- %s:START -->.*?<!-- %s:END -->' % (name, name), re.S)
    if pat.search(s): return pat.sub(lambda m: new, s, count=1)
    return put(s, name, new, before)
def form_hubs(s):
    m = re.search(r'<select id="lb-hub" name="hub">(.*?)</select>', s, re.S)
    out, sel = [], None
    if not m: return out, 'Oceans.html'
    for attrs, text in re.findall(r'<option([^>]*)>([^<]*)</option>', m.group(1)):
        vm = re.search(r'value="([^"]+)"', attrs)
        if not vm: continue
        out.append((vm.group(1), html.unescape(text)))
        if re.search(r'(^|\s)selected(?:=|\s|$)', attrs): sel = vm.group(1)
    return out, sel or (out[0][0] if out else 'Oceans.html')
def sol_names(l):
    names = {}
    p = d(l) + 'Solutions.html'
    if not os.path.exists(p): return names
    for m in re.finditer(r'<section ([^>]*class="card-band sol-hub"[^>]*)>.*?<h2><a[^>]*>(.*?)</a>', rd(p), re.S):
        hm = re.search(r'data-hub="([^"]+)"', m.group(1))
        if hm: names[hm.group(1)] = re.sub('<[^>]+>', '', m.group(2))
    return names
LB_JS = """<script>(function(){var sel=document.getElementById('lb-std-hub'),topic=document.getElementById('lb-hub'),box=document.getElementById('lb-std-panels');if(!sel||!box)return;
var panels=[].slice.call(box.querySelectorAll('.lb-std-panel'));
function has(v){return [].some.call(sel.options,function(o){return o.value===v})}
function show(v){if(!has(v))return;sel.value=v;panels.forEach(function(p){p.hidden=p.getAttribute('data-hub')!==v})}
function fromTopic(){if(topic&&has(topic.value))show(topic.value)}
var q=new URLSearchParams(location.search).get('hub');
if(q&&has(q))show(q);else fromTopic();
sel.addEventListener('change',function(){show(sel.value)});
if(topic)topic.addEventListener('change',fromTopic);
})();</script>"""
def lesson(l):
    p = d(l) + 'Lesson_Builder.html'
    if not os.path.exists(p): return 0
    s = rd(p); u = U[l]
    names = sol_names(l)
    form, selected = form_hubs(s)
    seen = {h for h, _ in form}
    labels = list(form)
    for h in D['hubs']:
        if h not in seen: labels.append((h, names.get(h, h)))
    if not any(h == selected for h, _ in labels):
        selected = 'Oceans.html' if any(h == 'Oceans.html' for h, _ in labels) else labels[0][0]
    def pid(h): return 'lbs-' + re.sub(r'[^A-Za-z0-9]+', '-', h).strip('-')
    def empty_p(name): return f'<p class="lb-std-empty">{esc(u["empty"].replace("{name}", name))}</p>'
    def code_bits(c):
        o = D['codes'][c]
        return (f'<a href="{o["url"]}" dir="ltr" target="_blank" rel="noopener" title="{esc(o["text"])}">{esc(short(c))}</a>'
                f' <span class="std-official" lang="en" dir="ltr">{esc(o["text"])}</span>')
    def panel(h, name):
        cs = D['hubs'].get(h) or []
        body = f'<ul class="std-list">{"".join(f"<li><span class=\"std-line\" dir=\"ltr\">{code_bits(c)}</span></li>" for c in cs)}</ul>' if cs else empty_p(name)
        hidden = '' if h == selected else ' hidden'
        return (f'<div class="lb-std-panel" data-hub="{esc(h)}" role="region" aria-labelledby="{pid(h)}"{hidden}>'
                f'<h3 id="{pid(h)}">{esc(name)}</h3>{body}</div>')
    opts = ''.join(f'<option value="{esc(h)}"' + (' selected' if h == selected else '') + f'>{esc(name)}</option>' for h, name in labels)
    rows = ''.join(f'<tr><td><a href="{h}">{names.get(h, h)}</a></td><td>' + ', '.join(f'<a href="{D["codes"][c]["url"]}" target="_blank" rel="noopener" title="{esc(D["codes"][c]["text"])}">{esc(short(c))}</a>' for c in cs) + '</td></tr>'
                   for h, cs in sorted(D['hubs'].items(), key=lambda x: names.get(x[0], x[0]).lower()))
    missing = ''.join(empty_p(name) for h, name in labels if not D['hubs'].get(h))
    search = (f'<p class="lb-std-search"><a class="edu-bubble glass" data-tint="ocean" href="Search.html">{esc(u["search"])}</a> '
              f'<span>{esc(u["searchNote"])}</span></p>')
    blk = (f'<!-- LB-STD:START --><section class="five-ws lb-std" aria-labelledby="lbs-h"><h2 id="lbs-h">{esc(u["lb"])}</h2><p class="std-note" id="lbs-note">{esc(u["note"])}</p>'
           f'<div id="lb-std-app"><div class="lb-std-pick glass" data-tint="earth"><label for="lb-std-hub">{esc(u["pick"])}</label>'
           f'<select id="lb-std-hub" aria-describedby="lbs-note">{opts}</select></div>{search}'
           f'<div id="lb-std-panels" aria-live="polite" aria-atomic="true">{"".join(panel(h, n) for h, n in labels)}</div></div>'
           f'<noscript><style>#lb-std-app{{display:none !important}}</style>{search}'
           f'<table><thead><tr><th scope="col">{esc(u["hub"])}</th><th scope="col">{esc(u["codes"])}</th></tr></thead><tbody>{rows}</tbody></table>{missing}</noscript>'
           f'{LB_JS}</section><!-- LB-STD:END -->')
    return wr(p, swap(s, 'LB-STD', blk, '</main>'))
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
    css = rd('styles.css'); pat = re.compile(r'/\* STD:START \*/.*?/\* STD:END \*/', re.S); block_css = CSS.strip('\n')
    css2 = pat.sub(lambda m: block_css, css, count=1) if pat.search(css) else css.rstrip('\n') + '\n' + CSS + '\n'
    if css2 != css: open('styles.css', 'w', encoding='utf8').write(css2)
    tagged = sum(1 for u in PH if codes_for(u))
    print(f'build-standards: {n} page writes; {tagged}/{len(PH)} solutions tagged')
if __name__ == '__main__': main()
