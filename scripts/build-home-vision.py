#!/usr/bin/env python3
"""Oct 30 2026 (founder-approved): Vision strip on the homepage, directly under the locked hero
(before the parked template / numbers strip). English copy is founder text (266 solutions, not 246).
fr/es/ar/it/he are machine-drafted and carry the same reader note as Learn_Rocket_Propulsion
(scripts/rocket_path_text.py UI['mt']).

Writes <!-- VISION:START/END --> on index.html in all 6 languages, mirrors the new strings into
i18n/<lang>.json (so i18n-build can translate the block), then re-stamps each translation's
i18n-source hash. build-home-trim.py keeps this block visible under the hero. Idempotent.
Run after build-home-trim.py and build-home-numbers.py (weekly-sync.sh).
"""
import os, re, json, html, importlib.util
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
E = lambda s: html.escape(s, quote=False)
LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')
# Same machine-draft line as scripts/rocket_path_text.py (empty in English).
MT = {
 'en': '',
 'fr': 'Traduction rédigée par machine, à relire.',
 'es': 'Traducción redactada por máquina, pendiente de revisión.',
 'ar': 'ترجمة آلية بانتظار المراجعة.',
 'it': 'Traduzione redatta a macchina, da rivedere.',
 'he': 'תרגום מכונה, ממתין לבדיקה.',
}
T = {
 'h': {'en': 'Vision', 'fr': 'Vision', 'es': 'Visión', 'ar': 'الرؤية', 'it': 'Visione', 'he': 'חזון'},
 'p': {
  'en': 'A world where every learner can see that people are already healing the planet \u2014 and know exactly how to join in. From Earth\u2019s deep-time story on BeforeSavingPlanets to today\u2019s working solutions here, we turn wonder into clear next steps: learning tracks, teacher and kids\u2019 tools, a world map of real projects, and 266 solutions across 11 hubs in six languages. No doom. Just free, sourced education that showcases what works and points families, classrooms, and communities to trusted ways to help.',
  'fr': 'Un monde où chaque personne qui apprend voit que des gens guérissent déjà la planète \u2014 et sait exactement comment s\u2019y joindre. De l\u2019histoire de la Terre sur le temps long, sur BeforeSavingPlanets, aux solutions qui marchent ici aujourd\u2019hui, nous changeons l\u2019émerveillement en prochaines étapes claires : parcours d\u2019apprentissage, outils pour les enseignants et les enfants, une carte mondiale de projets réels, et 266 solutions dans 11 pôles en six langues. Pas de catastrophisme. Juste une éducation gratuite et sourcée qui montre ce qui fonctionne et oriente les familles, les classes et les communautés vers des façons fiables d\u2019aider.',
  'es': 'Un mundo en el que cada persona que aprende vea que la gente ya está sanando el planeta, y sepa exactamente cómo sumarse. De la historia de la Tierra en el tiempo profundo, en BeforeSavingPlanets, a las soluciones que funcionan hoy aquí, convertimos el asombro en pasos claros: rutas de aprendizaje, herramientas para docentes y niños, un mapa mundial de proyectos reales y 266 soluciones en 11 centros en seis idiomas. Sin fatalismo. Solo educación gratuita y con fuentes, que muestra lo que funciona y señala a familias, aulas y comunidades formas de ayuda de confianza.',
  'ar': 'عالم يرى فيه كل متعلّم أن الناس يشفون الكوكب بالفعل \u2014 ويعرف تمامًا كيف ينضم. من قصة الأرض في الزمن العميق على BeforeSavingPlanets إلى الحلول العاملة هنا اليوم، نحوّل الدهشة إلى خطوات تالية واضحة: مسارات تعلّم، وأدوات للمعلمين والأطفال، وخريطة عالمية لمشاريع حقيقية، و266 حلًا في 11 مركزًا بست لغات. بلا سوداوية. فقط تعليم مجاني وموثّق المصادر يعرض ما ينجح ويوجّه الأسر والصفوف والمجتمعات إلى طرق موثوقة للمساعدة.',
  'it': 'Un mondo in cui ogni persona che impara vede che la gente sta già guarendo il pianeta \u2014 e sa esattamente come unirsi. Dalla storia della Terra nel tempo profondo su BeforeSavingPlanets alle soluzioni che funzionano oggi qui, trasformiamo lo stupore in prossimi passi chiari: percorsi di apprendimento, strumenti per insegnanti e bambini, una mappa mondiale di progetti reali e 266 soluzioni in 11 hub in sei lingue. Niente catastrofismo. Solo educazione gratuita e con fonti, che mostra ciò che funziona e indica a famiglie, classi e comunità modi affidabili per aiutare.',
  'he': 'עולם שבו כל לומד רואה שאנשים כבר מרפאים את כוכב הלכת \u2014 ויודע בדיוק איך להצטרף. מסיפור הזמן העמוק של כדור הארץ ב-BeforeSavingPlanets ועד לפתרונות שעובדים כאן היום, אנחנו הופכים פליאה לצעדים הבאים ברורים: מסלולי למידה, כלים למורים ולילדים, מפת עולם של פרויקטים אמיתיים, ו-266 פתרונות ב-11 מרכזים בשש שפות. בלי ייאוש. רק חינוך חינמי ומבוסס מקורות, שמראה מה עובד ומכוון משפחות, כיתות וקהילות לדרכים מהימנות לעזור.',
 },
 'story': {
  'en': 'Where Earth\u2019s story begins \u2192',
  'fr': 'Là où l\u2019histoire de la Terre commence \u2192',
  'es': 'Donde empieza la historia de la Tierra \u2192',
  'ar': 'حيث تبدأ قصة الأرض \u2192',
  'it': 'Dove inizia la storia della Terra \u2192',
  'he': 'שם מתחיל סיפור כדור הארץ \u2192',
 },
 'explore': {
  'en': 'Explore solutions',
  'fr': 'Explorer les solutions',
  'es': 'Explorar soluciones',
  'ar': 'استكشف الحلول',
  'it': 'Esplora le soluzioni',
  'he': 'לחקור פתרונות',
 },
}
CSS = ('<style>.home-vision{max-width:860px;margin:1.25rem auto 0;padding:0 1rem 1.25rem;text-align:center}'
       '.home-vision h2{margin:0 0 .55rem}.home-vision .hv-p{margin:.35rem auto 0;line-height:1.55;max-width:46rem}'
       '.hv-chips{display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center;margin:.9rem 0 0;padding:0}'
       '.hv-chip{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:.4rem 1rem;border-radius:999px;border:2px solid #0b3d91;font-weight:700;text-decoration:none}'
       '.hv-chip-ext{background:#0b3d91;color:#fff}.hv-chip-ext:hover{background:#009cde;border-color:#009cde}'
       '.hv-mt{font-size:.85rem;opacity:.8;margin:.75rem 0 0}'
       '.hv-chip:focus-visible{outline:3px solid #009cde;outline-offset:2px}</style>')
R = re.compile(r'<!-- VISION:START -->.*?<!-- VISION:END -->', re.S)

def section_end(s, i):
    d, j = 0, i
    while True:
        a, b = s.find('<section', j), s.find('</section>', j)
        if a != -1 and a < b:
            d += 1; j = a + 8
        else:
            d -= 1; j = b + len('</section>')
            if d == 0: return j

def block(l):
    note = f'<p class="hv-mt" role="note"><small>\U0001f916 {E(MT[l])}</small></p>' if MT[l] else ''
    return ('<!-- VISION:START -->' + CSS +
            f'<section class="home-vision" id="vision" aria-labelledby="vision-h"><h2 id="vision-h">{E(T["h"][l])}</h2>'
            f'<p class="hv-p">{E(T["p"][l])}</p>'
            f'<p class="hv-chips"><a class="hv-chip hv-chip-ext" href="https://www.beforesavingplanets.com/" target="_blank" rel="noopener noreferrer">{E(T["story"][l])}</a>'
            f'<a class="hv-chip" href="Solutions.html">{E(T["explore"][l])}</a></p>{note}</section><!-- VISION:END -->')

def put(s, l):
    b = block(l)
    if R.search(s): return R.sub(lambda m: b, s, count=1)
    m = re.search(r'<section class="hero[ "]', s)
    if not m: raise SystemExit('no homepage hero')
    i = section_end(s, m.start())
    return s[:i] + b + s[i:]

def upsert_i18n():
    """Append or replace the Vision strings in i18n/<lang>.json without rewriting the rest of the file."""
    keys = ('h', 'p', 'story', 'explore')
    for lang in LANGS:
        if lang == 'en': continue
        path = f'i18n/{lang}.json'
        raw = open(path, encoding='utf8').read()
        data = json.loads(raw)
        pairs = [(T[k]['en'], T[k][lang]) for k in keys]
        missing, stale = [], []
        for k, v in pairs:
            if k not in data: missing.append((k, v))
            elif data[k] != v: stale.append((k, v))
        if not missing and not stale: continue
        for k, v in stale:
            key = json.dumps(k, ensure_ascii=False)
            line = key + ': ' + json.dumps(v, ensure_ascii=False)
            pat = re.compile('^' + re.escape(key) + r': .*', re.M)
            raw2, n = pat.subn(line, raw, count=1)
            if n != 1: raise SystemExit(f'{path}: could not replace {k[:40]!r}')
            raw = raw2
        if missing:
            body = raw.rstrip()
            end = body.rfind('}')
            head = body[:end].rstrip()
            if not head.endswith(','): head += ','
            extra = ',\n'.join(json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) for k, v in missing)
            raw = head + '\n' + extra + '\n}\n'
        json.loads(raw)
        open(path, 'w', encoding='utf8').write(raw if raw.endswith('\n') else raw + '\n')
        print(lang, 'i18n vision strings', len(missing), 'added', len(stale), 'updated')

s = put(open('index.html', encoding='utf8').read(), 'en')
open('index.html', 'w', encoding='utf8').write(s)
sp = importlib.util.spec_from_file_location('ib', 'scripts/i18n-build.py')
ib = importlib.util.module_from_spec(sp); sp.loader.exec_module(ib)
H = ib.src_hash('index.html')
for l in ('fr', 'es', 'ar', 'it', 'he'):
    f = l + '/index.html'
    s = put(open(f, encoding='utf8').read(), l)
    s = re.sub(r'(<meta content="index\.html )[0-9a-f]{12}(" name="i18n-source"/?>)', lambda m: m.group(1) + H + m.group(2), s, count=1)
    open(f, 'w', encoding='utf8').write(s)
upsert_i18n()
# English paragraph must stay the founder string, including 266.
assert '266 solutions across 11 hubs' in open('index.html', encoding='utf8').read()
assert 'https://www.beforesavingplanets.com/' in open('index.html', encoding='utf8').read()
assert '246 solutions across 11 hubs' not in T['p']['en']
print('home vision: 6 languages, i18n-source', H)
