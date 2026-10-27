#!/usr/bin/env python3
"""Oct 26 2026: Polished Big_Questions.html UI in all 6 languages.
Treasure-trove FAQ: clean hero, topic chips, client-side search, accordion answers
(crisp lead + Go deeper + source), Did-you-know highlights, Myth vs Fact tie-ins,
shareable anchors, related questions, Ways to Help CTA. One H1, FAQPage JSON-LD,
RTL for ar/he, accessible. Facts only from question-bank.csv + Myth/Solutions pages.
Usage: python3 scripts/build-big-questions-ui.py
Run after build-question-bank.py. Replaces prior Big_Questions body (keeps site chrome).
"""
import csv, html, json, os, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
BANK = ROOT / 'assets/data/question-bank.csv'
PAGE = 'Big_Questions.html'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
RTL = {'ar', 'he'}
LOCALE = {'en':'en_US','fr':'fr_FR','es':'es_ES','ar':'ar_AR','it':'it_IT','he':'he_IL'}
SITE = 'https://www.savingplanets.com/'

# Chip order (cluster id → label). "planet" = core doom/hope/climate from myth + polar/space-weather mix
CHIPS = [
    ('all', {'en':'All','fr':'Tout','es':'Todo','ar':'الكل','it':'Tutto','he':'הכל'}),
    ('planet', {'en':'Planet','fr':'Planète','es':'Planeta','ar':'الكوكب','it':'Pianeta','he':'כדור הארץ'}),
    ('oceans', {'en':'Oceans','fr':'Océans','es':'Océanos','ar':'المحيطات','it':'Oceani','he':'אוקיינוסים'}),
    ('rivers', {'en':'Rivers','fr':'Rivières','es':'Ríos','ar':'الأنهار','it':'Fiumi','he':'נהרות'}),
    ('lakes', {'en':'Lakes','fr':'Lacs','es':'Lagos','ar':'البحيرات','it':'Laghi','he':'אגמים'}),
    ('forests', {'en':'Forests','fr':'Forêts','es':'Bosques','ar':'الغابات','it':'Foreste','he':'יערות'}),
    ('space', {'en':'Space','fr':'Espace','es':'Espacio','ar':'الفضاء','it':'Spazio','he':'חלל'}),
    ('learning', {'en':'Learning','fr':'Apprendre','es':'Aprender','ar':'التعلّم','it':'Apprendimento','he':'למידה'}),
    ('teachers', {'en':'Teachers','fr':'Enseignants','es':'Docentes','ar':'المعلمون','it':'Insegnanti','he':'מורים'}),
    ('kids', {'en':'Kids','fr':'Enfants','es':'Niños','ar':'الأطفال','it':'Bambini','he':'ילדים'}),
    ('ways-to-help', {'en':'How to Help','fr':'Comment aider','es':'Cómo ayudar','ar':'كيف أساعد','it':'Come aiutare','he':'איך לעזור'}),
]

# Map bank clusters → chip id
CHIP_OF = {
    'myth': 'planet', 'polar': 'planet', 'space-weather': 'planet',
    'planetary-defense': 'space', 'earth-observation': 'space', 'launches': 'space',
    'solutions': 'all',  # distributed; also shown under all
    'oceans': 'oceans', 'rivers': 'rivers', 'lakes': 'lakes', 'forests': 'forests',
    'space': 'space', 'learning': 'learning', 'teachers': 'teachers', 'kids': 'kids',
    'ways-to-help': 'ways-to-help', 'big-questions': 'planet',
}

UI = {
  'title': {
    'en':'Big Questions About Our Planet | Saving Planets',
    'fr':'Grandes questions sur notre planète | Saving Planets',
    'es':'Grandes preguntas sobre nuestro planeta | Saving Planets',
    'ar':'أسئلة كبيرة عن كوكبنا | Saving Planets',
    'it':'Le grandi domande sul nostro pianeta | Saving Planets',
    'he':'שאלות גדולות על כדור הארץ שלנו | Saving Planets'},
  'desc': {
    'en':'Searchable, sourced answers to questions about Earth, oceans, forests, space, learning and how to help — drawn from Saving Planets pages and NASA, NOAA, IPCC and ESA sources.',
    'fr':'Réponses sourcées et recherchables sur la Terre, les océans, les forêts, l’espace, l’apprentissage et comment aider — tirées des pages Saving Planets et de sources NASA, NOAA, GIEC et ESA.',
    'es':'Respuestas con fuentes y buscables sobre la Tierra, océanos, bosques, espacio, aprendizaje y cómo ayudar, tomadas de Saving Planets y de NASA, NOAA, IPCC y ESA.',
    'ar':'إجابات موثّقة وقابلة للبحث عن الأرض والمحيطات والغابات والفضاء والتعلّم وكيف تساعد — من صفحات Saving Planets ومصادر ناسا وNOAA والهيئة الحكومية الدولية المعنية بتغير المناخ ووكالة الفضاء الأوروبية.',
    'it':'Risposte con fonti e ricercabili su Terra, oceani, foreste, spazio, apprendimento e come aiutare — dalle pagine Saving Planets e da NASA, NOAA, IPCC ed ESA.',
    'he':'תשובות מבוססות מקורות וניתנות לחיפוש על כדור הארץ, אוקיינוסים, יערות, חלל, למידה ואיך לעזור — מדפי Saving Planets וממקורות NASA, NOAA, IPCC ו-ESA.'},
  'h1': {
    'en':'Big Questions About Our Planet','fr':'Grandes questions sur notre planète',
    'es':'Grandes preguntas sobre nuestro planeta','ar':'أسئلة كبيرة عن كوكبنا',
    'it':'Le grandi domande sul nostro pianeta','he':'שאלות גדולות על כדור הארץ שלנו'},
  'purpose': {
    'en':'One place to ask what Saving Planets already answers — with sources, not doom.',
    'fr':'Un seul endroit pour les questions auxquelles Saving Planets répond déjà — avec des sources, sans fatalisme.',
    'es':'Un solo lugar para lo que Saving Planets ya responde: con fuentes, sin catastrofismo.',
    'ar':'مكان واحد لما يجيب عنه Saving Planets بالفعل — بمصادر، بلا تهويل.',
    'it':'Un solo posto per ciò a cui Saving Planets risponde già — con fonti, senza catastrofismo.',
    'he':'מקום אחד לשאלות ש-Saving Planets כבר עונה עליהן — עם מקורות, בלי אבדון.'},
  'search_label': {'en':'Search questions','fr':'Rechercher des questions','es':'Buscar preguntas','ar':'ابحث في الأسئلة','it':'Cerca domande','he':'חיפוש בשאלות'},
  'search_ph': {'en':'Type a word…','fr':'Tapez un mot…','es':'Escribe una palabra…','ar':'اكتب كلمة…','it':'Scrivi una parola…','he':'הקלידו מילה…'},
  'filter': {'en':'Topics','fr':'Thèmes','es':'Temas','ar':'المواضيع','it':'Argomenti','he':'נושאים'},
  'go': {'en':'Go deeper','fr':'Aller plus loin','es':'Profundizar','ar':'تعمّق أكثر','it':'Approfondisci','he':'להעמיק'},
  'src': {'en':'Source','fr':'Source','es':'Fuente','ar':'المصدر','it':'Fonte','he':'מקור'},
  'share': {'en':'Copy link','fr':'Copier le lien','es':'Copiar enlace','ar':'نسخ الرابط','it':'Copia link','he':'העתקת קישור'},
  'related': {'en':'Related','fr':'Liées','es':'Relacionadas','ar':'ذات صلة','it':'Correlate','he':'קשורות'},
  'dyk': {'en':'Did you know?','fr':'Le saviez-vous ?','es':'¿Sabías que…?','ar':'هل تعلم؟','it':'Lo sapevi?','he':'הידעתם?'},
  'myth': {'en':'Myth or fact?','fr':'Mythe ou réalité ?','es':'¿Mito o realidad?','ar':'خرافة أم حقيقة؟','it':'Mito o realtà?','he':'מיתוס או עובדה?'},
  'myth_cta': {'en':'Browse Myth vs Fact','fr':'Voir Mythe ou réalité','es':'Ver Mito o realidad','ar':'تصفّح خرافة أم حقيقة','it':'Vedi Mito o realtà','he':'עיינו במיתוס מול עובדה'},
  'help_h': {'en':'Ready to help?','fr':'Prêt·e à aider ?','es':'¿Listo para ayudar?','ar':'مستعد للمساعدة؟','it':'Pronto ad aiutare?','he':'מוכנים לעזור?'},
  'help_p': {
    'en':'Ways to Help links you to donate or join the groups doing the work. Saving Planets does not take a cut.',
    'fr':'Comment aider vous mène aux dons et aux engagements des groupes qui font le travail. Saving Planets ne prend aucune commission.',
    'es':'Formas de ayudar te lleva a donar o unirte a quienes hacen el trabajo. Saving Planets no se queda con nada.',
    'ar':'طرق المساعدة توصلك للتبرع أو الانضمام لمن يقومون بالعمل. Saving Planets لا يأخذ عمولة.',
    'it':'Come aiutare ti porta a donare o unirti a chi fa il lavoro. Saving Planets non trattiene nulla.',
    'he':'«דרכים לעזור» מוביל לתרומה או הצטרפות לקבוצות שעושות את העבודה. Saving Planets לא לוקח עמלה.'},
  'help_btn': {'en':'Ways to Help','fr':'Comment aider','es':'Formas de ayudar','ar':'طرق المساعدة','it':'Come aiutare','he':'דרכים לעזור'},
  'count': {'en':'{n} questions','fr':'{n} questions','es':'{n} preguntas','ar':'{n} سؤالًا','it':'{n} domande','he':'{n} שאלות'},
  'empty': {'en':'No questions match. Try another word or topic.','fr':'Aucune question ne correspond. Essayez un autre mot ou thème.','es':'Ninguna pregunta coincide. Prueba otra palabra o tema.','ar':'لا أسئلة مطابقة. جرّب كلمة أو موضوعًا آخر.','it':'Nessuna domanda corrisponde. Prova un’altra parola o argomento.','he':'אין שאלות תואמות. נסו מילה או נושא אחר.'},
  'credit': {'en':'Created by SI and Biological SI Partner','fr':'Créé par SI et Biological SI Partner','es':'Creado por SI y Biological SI Partner','ar':'من إعداد SI وBiological SI Partner','it':'Creato da SI e Biological SI Partner','he':'נוצר על ידי SI ו-Biological SI Partner'},
  'results': {'en':'Questions','fr':'Questions','es':'Preguntas','ar':'الأسئلة','it':'Domande','he':'שאלות'},
}

# Cap per chip for page weight (all = sum of caps with dedupe)
CAP = {
    'planet': 14, 'oceans': 10, 'rivers': 8, 'lakes': 8, 'forests': 10,
    'space': 12, 'learning': 10, 'teachers': 10, 'kids': 8, 'ways-to-help': 8,
}
# Prefer hub-level answering pages when picking
HUB_PREF = {
    'Myth_vs_Fact.html','Oceans.html','Rivers.html','Lakes.html','Deforestation.html','Space.html',
    'Learn.html','Teachers.html','Play_and_Learn.html','Ways_to_Help.html','Artemis_II.html',
    'Earth_Observation.html','Planetary_Defense.html','Solutions.html','Amazing_Facts.html',
    'Polar.html','Space_Weather.html','Space_Disposal.html','Big_Questions.html',
}

def esc(s): return html.escape(s or '', quote=False)
def escq(s): return html.escape(s or '', quote=True)
def d(lang): return '' if lang == 'en' else lang + '/'
def url(lang): return SITE + d(lang) + PAGE

def crisp(text, max_sent=2, max_len=220):
    text = re.sub(r'\s+', ' ', (text or '')).strip()
    if not text: return ''
    parts = re.split(r'(?<=[.!?؟])\s+', text)
    out = ' '.join(parts[:max_sent]).strip()
    if len(out) > max_len:
        out = out[:max_len-1].rstrip() + '…'
    return out

def slug(q, i):
    s = re.sub(r'[^a-z0-9\u0600-\u06ff\u0590-\u05ff]+', '-', q.lower())
    s = re.sub(r'-+', '-', s).strip('-')[:48] or 'q'
    return f'q-{i}-{s}'

def load_bank(lang):
    rows = []
    with open(BANK, encoding='utf8') as f:
        for r in csv.DictReader(f):
            if r['language'] != lang: continue
            chip = CHIP_OF.get(r['cluster'], 'all')
            if chip == 'all' and r['cluster'] == 'solutions':
                # map solution category-ish from answering path — keep under oceans/forests if name hints else planet
                chip = 'planet'
            r = dict(r); r['chip'] = chip if chip != 'all' else CHIP_OF.get(r['cluster'], 'planet')
            if r['cluster'] == 'solutions':
                # leave solutions mostly out of UI caps except a few via oceans etc already in bank by category
                pass
            rows.append(r)
    return rows

def pick_for_chip(rows, chip, limit):
    pool = [r for r in rows if (chip == 'all' or r['chip'] == chip or (chip=='planet' and r['cluster'] in ('myth','polar','space-weather')))]
    if chip == 'space':
        pool = [r for r in rows if r['chip'] == 'space' or r['cluster'] in ('space','earth-observation','planetary-defense','launches')]
    hub, rest = [], []
    for r in pool:
        ap = r['answering_page'].split('#')[0]
        (hub if ap in HUB_PREF else rest).append(r)
    out, seen = [], set()
    for r in hub + rest:
        k = r['question']
        if k in seen: continue
        seen.add(k); out.append(r)
        if len(out) >= limit: break
    return out

def select_questions(rows):
    """Build deduped list tagged with chips; enforce caps."""
    chosen = []
    seen = set()
    for chip, _ in CHIPS:
        if chip == 'all': continue
        lim = CAP.get(chip, 8)
        for r in pick_for_chip(rows, chip, lim):
            if r['question'] in seen: continue
            seen.add(r['question'])
            r = dict(r); r['chip'] = chip
            chosen.append(r)
    return chosen

def dyk_items(rows, lang, n=4):
    """Did-you-know from myth/ocean/space excerpts with external sources."""
    out = []
    for r in rows:
        if not (r.get('source_url') or '').startswith('http'): continue
        if r['cluster'] not in ('myth','oceans','earth-observation','planetary-defense','forests','polar'): continue
        lead = crisp(r['answer_excerpt'], 1, 160)
        if len(lead) < 40: continue
        out.append((lead, r['source_label'], r['source_url'], r['answering_page']))
        if len(out) >= n: break
    return out

def related_map(items):
    by_chip = defaultdict(list)
    for it in items:
        by_chip[it['chip']].append(it['id'])
    rel = {}
    for it in items:
        others = [x for x in by_chip[it['chip']] if x != it['id']][:3]
        rel[it['id']] = others
    return rel

CSS = r'''
.bq{--bq-accent:#8fd3ff;--bq-line:rgba(124,170,255,.35);--bq-bg:rgba(124,170,255,.07);max-width:880px;margin:0 auto;padding:0 clamp(12px,3vw,1.25rem) 3rem}
.bq-hero-purpose{font-size:1.15rem;line-height:1.45;margin:.35rem 0 0;opacity:.95}
.bq-toolbar{position:sticky;top:64px;z-index:5;padding:.65rem 0 .5rem;background:linear-gradient(180deg,rgba(7,16,24,.97),rgba(7,16,24,.92));backdrop-filter:blur(8px);margin:0 -4px;padding-inline:4px}
.bq-search{display:flex;flex-direction:column;gap:.35rem;margin-bottom:.65rem}
.bq-search input{width:100%;box-sizing:border-box;min-height:48px;border-radius:12px;border:1px solid var(--bq-line);background:rgba(0,20,40,.55);color:#e8eef5;padding:.65rem .9rem;font-size:1rem}
.bq-search input:focus{outline:2px solid var(--bq-accent);outline-offset:2px}
.bq-chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:0;padding:0;list-style:none}
.bq-chips button{appearance:none;border:1px solid var(--bq-line);background:transparent;color:#e8eef5;border-radius:999px;padding:.4rem .85rem;min-height:44px;font:inherit;font-size:.9rem;font-weight:600;cursor:pointer}
.bq-chips button[aria-pressed=true]{background:rgba(0,156,222,.28);border-color:#009cde;color:#fff}
.bq-chips button:focus-visible{outline:2px solid var(--bq-accent);outline-offset:2px}
.bq-count{font-size:.9rem;opacity:.85;margin:.5rem 0 .75rem}
.bq-list{display:flex;flex-direction:column;gap:.55rem}
.bq-item{border:1px solid var(--bq-line);border-radius:14px;background:var(--bq-bg);padding:.15rem .2rem}
.bq-item[hidden]{display:none !important}
.bq-item summary{cursor:pointer;font-weight:650;font-size:1.02rem;line-height:1.35;padding:.75rem .9rem;list-style:none;display:flex;gap:.5rem;align-items:flex-start}
.bq-item summary::-webkit-details-marker{display:none}
.bq-item summary::before{content:"+";flex:none;width:1.25rem;color:var(--bq-accent);font-weight:700}
.bq-item[open] summary::before{content:"–"}
.bq-body{padding:0 1rem 1rem}
.bq-lead{margin:.1rem 0 .65rem;line-height:1.55}
.bq-actions{display:flex;flex-wrap:wrap;gap:.5rem .85rem;align-items:center;font-size:.92rem}
.bq-actions a,.bq-link{color:var(--bq-accent)}
.bq-src{opacity:.9}
.bq-rel{margin:.7rem 0 0;font-size:.9rem}
.bq-rel ul{margin:.25rem 0 0;padding-inline-start:1.2rem}
.bq-dyk,.bq-myth,.bq-cta{margin:1.75rem 0;padding:1rem 1.1rem;border-radius:16px;border:1px solid var(--bq-line);background:rgba(0,156,222,.1)}
.bq-dyk h2,.bq-myth h2,.bq-cta h2{margin:0 0 .55rem;font-size:1.15rem}
.bq-dyk ul{margin:.3rem 0;padding-inline-start:1.2rem;line-height:1.5}
.bq-empty{display:none;padding:1rem;opacity:.9}
.bq-empty.show{display:block}
.bq-meta{font-size:.85rem;opacity:.85;margin-top:1.5rem}
@media (max-width:640px){.bq-toolbar{top:56px}}
'''

JS = r'''
(function(){
  var root=document.getElementById('bq-app'); if(!root) return;
  var q=root.querySelector('[data-bq-search]');
  var chips=root.querySelectorAll('[data-bq-chip]');
  var items=[].slice.call(root.querySelectorAll('[data-bq-item]'));
  var count=root.querySelector('[data-bq-count]');
  var empty=root.querySelector('[data-bq-empty]');
  var tpl=root.getAttribute('data-count-tpl')||'{n}';
  var chip='all';
  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');}
  function apply(){
    var needle=norm(q&&q.value);
    var n=0;
    items.forEach(function(el){
      var hay=norm(el.getAttribute('data-text'));
      var c=el.getAttribute('data-chip');
      var okChip=(chip==='all'||c===chip);
      var okQ=!needle||hay.indexOf(needle)!==-1;
      var show=okChip&&okQ;
      if(show){el.removeAttribute('hidden'); n++;} else el.setAttribute('hidden','');
    });
    if(count) count.textContent=tpl.replace('{n}', String(n));
    if(empty){ if(n) empty.classList.remove('show'); else empty.classList.add('show'); }
  }
  chips.forEach(function(btn){
    btn.addEventListener('click', function(){
      chip=btn.getAttribute('data-bq-chip')||'all';
      chips.forEach(function(b){ b.setAttribute('aria-pressed', b===btn ? 'true':'false'); });
      apply();
    });
  });
  if(q){ q.addEventListener('input', apply); }
  root.querySelectorAll('[data-bq-copy]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var id=btn.getAttribute('data-bq-copy');
      var u=location.origin+location.pathname+'#'+id;
      if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(u); }
      else { var i=document.createElement('input'); i.value=u; document.body.appendChild(i); i.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(i); }
      btn.setAttribute('data-copied','1');
      setTimeout(function(){ btn.removeAttribute('data-copied'); }, 1200);
    });
  });
  apply();
  if(location.hash){
    var t=document.getElementById(location.hash.slice(1));
    if(t&&t.tagName==='DETAILS'){ t.open=true; t.scrollIntoView({block:'start'}); }
  }
})();
'''

def build_body(lang, items, dyk):
    u = UI
    chips_html = ''.join(
        f'<li><button type="button" data-bq-chip="{cid}" aria-pressed="{"true" if cid=="all" else "false"}">{esc(labels[lang])}</button></li>'
        for cid, labels in CHIPS
    )
    # assign ids
    for i, it in enumerate(items):
        it['id'] = slug(it['question'], i)
    rel = related_map(items)
    id_to_q = {it['id']: it['question'] for it in items}

    cards = []
    ents = []
    for it in items:
        lead = crisp(it['answer_excerpt'])
        deeper = it['answering_page']
        src_u, src_l = it['source_url'], it['source_label']
        rel_ids = rel.get(it['id'], [])
        rel_html = ''
        if rel_ids:
            lis = ''.join(f'<li><a href="#{rid}">{esc(id_to_q[rid])}</a></li>' for rid in rel_ids if rid in id_to_q)
            rel_html = f'<div class="bq-rel"><strong>{esc(u["related"][lang])}</strong><ul>{lis}</ul></div>'
        text_attr = escq((it['question'] + ' ' + lead).lower())
        cards.append(
            f'<details class="bq-item" id="{it["id"]}" data-bq-item data-chip="{it["chip"]}" data-text="{text_attr}">'
            f'<summary>{esc(it["question"])}</summary>'
            f'<div class="bq-body"><p class="bq-lead">{esc(lead)}</p>'
            f'<div class="bq-actions">'
            f'<a class="bq-link" href="{escq(deeper)}">{esc(u["go"][lang])}</a>'
            f'<span class="bq-src">{esc(u["src"][lang])}: <a href="{escq(src_u)}" target="_blank" rel="noopener noreferrer">{esc(src_l)}</a></span>'
            f'<button type="button" class="bq-link" data-bq-copy="{it["id"]}" style="background:none;border:0;padding:0;color:inherit;font:inherit;cursor:pointer;color:var(--bq-accent)">{esc(u["share"][lang])}</button>'
            f'</div>{rel_html}</div></details>'
        )
        ents.append({'@type':'Question','name':it['question'],
                     'acceptedAnswer':{'@type':'Answer','text':lead}})

    dyk_html = ''
    if dyk:
        lis = ''.join(
            f'<li>{esc(text)} <a href="{escq(src_u)}" target="_blank" rel="noopener noreferrer">{esc(lab)}</a></li>'
            for text, lab, src_u, _ in dyk
        )
        dyk_html = f'<section class="bq-dyk" aria-labelledby="bq-dyk-h"><h2 id="bq-dyk-h">{esc(u["dyk"][lang])}</h2><ul>{lis}</ul></section>'

    myth_html = (
        f'<section class="bq-myth" aria-labelledby="bq-myth-h"><h2 id="bq-myth-h">{esc(u["myth"][lang])}</h2>'
        f'<p><a class="bq-link" href="Myth_vs_Fact.html">{esc(u["myth_cta"][lang])}</a></p></section>'
    )
    cta = (
        f'<section class="bq-cta" aria-labelledby="bq-cta-h"><h2 id="bq-cta-h">{esc(u["help_h"][lang])}</h2>'
        f'<p>{esc(u["help_p"][lang])}</p>'
        f'<p><a class="bq-link" href="Ways_to_Help.html"><strong>{esc(u["help_btn"][lang])}</strong></a></p></section>'
    )

    count0 = u['count'][lang].replace('{n}', str(len(items)))
    return f'''
<div class="bq" id="bq-app" data-count-tpl="{escq(u['count'][lang])}">
  <p class="bq-hero-purpose">{esc(u['purpose'][lang])}</p>
  <div class="bq-toolbar">
    <div class="bq-search">
      <label for="bq-q">{esc(u['search_label'][lang])}</label>
      <input id="bq-q" data-bq-search type="search" autocomplete="off" placeholder="{escq(u['search_ph'][lang])}" />
    </div>
    <p class="bq-count" id="bq-filter-label"><span class="visually-hidden">{esc(u['filter'][lang])}: </span></p>
    <ul class="bq-chips" role="list" aria-label="{escq(u['filter'][lang])}">{chips_html}</ul>
    <p class="bq-count" data-bq-count>{esc(count0)}</p>
  </div>
  <h2 class="visually-hidden">{esc(u['results'][lang])}</h2>
  <div class="bq-list">{''.join(cards)}</div>
  <p class="bq-empty" data-bq-empty role="status">{esc(u['empty'][lang])}</p>
  {dyk_html}
  {myth_html}
  {cta}
  <p class="bq-meta">{esc(u['credit'][lang])}</p>
</div>
<style id="bq-ui-css">{CSS}
.visually-hidden{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
</style>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"FAQPage","url":url(lang),"inLanguage":lang,"mainEntity":ents}, ensure_ascii=False)}</script>
<script id="bq-ui-js">{JS}</script>
'''

def shell(lang):
    p = ROOT / 'Glossary.html' if lang == 'en' else ROOT / lang / 'Glossary.html'
    if not p.exists():
        p = ROOT / 'Big_Questions.html' if lang == 'en' else ROOT / lang / 'Big_Questions.html'
    return p.read_text(encoding='utf8')

def write_lang(lang):
    raw = shell(lang)
    # strip prior BQ injectors / body main content we'll replace
    title, desc = UI['title'][lang], UI['desc'][lang]
    rows = load_bank(lang)
    items = select_questions(rows)
    dyk = dyk_items(rows, lang)

    head_end = raw.index('</head>')
    head = raw[:head_end]
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'Glossary\.html', PAGE, head)
    head = re.sub(r'Big_Questions\.html', PAGE, head)
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', head)
    for attr, val in (
        ('name="description" content="', desc),
        ('property="og:description" content="', desc),
        ('name="twitter:description" content="', desc),
        ('property="og:title" content="', title),
        ('name="twitter:title" content="', title),
    ):
        head = re.sub(re.escape(attr) + r'[^"]*', attr + escq(val), head, count=1)
    alts = ''.join(f'<link rel="alternate" hreflang="{x}" href="{url(x)}">\n' for x in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{url("en")}">\n'
    if re.search(r'rel="alternate" hreflang=', head):
        head = re.sub(r'(<link rel="alternate" hreflang="en"[^>]*>\n(?:<link rel="alternate" hreflang="[^"]+"[^>]*>\n)*)', alts, head, count=1)
    else:
        head = head.replace('<link rel="canonical"', alts + '<link rel="canonical"', 1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\1' + url(lang), head, count=1)
    head = re.sub(r'(property="og:url" content=")[^"]*', r'\1' + url(lang), head, count=1)
    head = re.sub(r'(property="og:locale" content=")[^"]*', r'\1' + LOCALE[lang], head, count=1)

    crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":{"en":"Home","fr":"Accueil","es":"Inicio","ar":"الرئيسية","it":"Home","he":"דף הבית"}[lang],"item":SITE+d(lang)},
        {"@type":"ListItem","position":2,"name":UI['h1'][lang],"item":url(lang)}]}
    head += f'<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script>\n'

    bodym = re.search(r'<body[^>]*>', raw).group(0)
    navm = re.search(r'<a class="skip-link".*?</nav>', raw, re.S)
    nav = navm.group(0) if navm else ''
    nav = re.sub(r'Glossary\.html|Big_Questions\.html', PAGE, nav)
    foot = raw[raw.index('</main>'):] if '</main>' in raw else raw[raw.index('<footer>'):]

    hero = (
        f'<section class="page-hero learn-hero"><div class="page-hero-content">'
        f'<h1>{esc(UI["h1"][lang])}</h1></div></section>'
    )
    main = f'<main id="main">{hero}{build_body(lang, items, dyk)}</main>'

    page = f'<!DOCTYPE html>\n<html lang="{lang}"'
    if lang in RTL:
        page += ' dir="rtl"'
    page += ' class="dark">\n<head>\n'
    inner = head.split('<head>',1)[1] if '<head>' in head else head
    page += inner + '</head>\n' + bodym + '\n' + nav + '\n' + main + '\n' + foot

    out = ROOT / PAGE if lang == 'en' else ROOT / lang / PAGE
    out.parent.mkdir(parents=True, exist_ok=True)
    # strip old markers if foot somehow duplicated
    page = re.sub(r'<!-- SP-BQ-CLUSTERS:START -->.*?<!-- SP-BQ-CLUSTERS:END -->', '', page, flags=re.S)
    page = re.sub(r'<!-- SP-HUBFAQ:START -->.*?<!-- SP-HUBFAQ:END -->', '', page, flags=re.S)
    out.write_text(page, encoding='utf8')
    return len(items)

def main():
    if not BANK.exists():
        raise SystemExit('run build-question-bank.py first')
    total = 0
    for lang in LANGS:
        n = write_lang(lang)
        total += n
        print(f'  {lang}: {n} questions')
    print(f'build-big-questions-ui: done ({total} question-slots across langs)')

if __name__ == '__main__':
    main()
