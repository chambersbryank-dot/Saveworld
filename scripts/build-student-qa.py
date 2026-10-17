#!/usr/bin/env python3
"""Oct 16: Student questions, answered (the SI Helper Q&A / math pool). Source: assets/data/student-qa.json (approved entries only).
Writes, for each of en/fr/es/ar/it:
  - Student_Questions.html: entries grouped by topic tab (#aero, #orbit, #phys, #all), each with its sources and the SI credit,
    FAQPage JSON-LD. Pagefind + the semantic search index pick the page up in scripts/build-search.mjs.
  - search/student-qa.json: {lang: [{id, topic, q, url}]} for the Search topic tabs (boost / floating questions by topic).
  - sitemap.xml entries (only once at least one entry is approved).
Vectorize: scripts/si-index.py embeds one chunk per entry (question + answer + sources) from the same JSON, so SI Helper can
answer the question next time. Run after build-si-helper.py (weekly-sync.sh); later generators fix nav/footer.
Usage: python3 scripts/build-student-qa.py [--check]   (--check: validate the JSON only)"""
import re, os, sys, json, datetime, importlib.util
sys.path.insert(0, 'scripts')
spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py'); BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
from learn_orbit_math import T
LANGS, d, rd, wr, esc, SITE, href = BL.LANGS, BL.d, BL.rd, BL.wr, BL.esc, BL.SITE, BL.sf.href
DATA, PAGE, TOPICS = 'assets/data/student-qa.json', 'Student_Questions.html', ['aero', 'orbit', 'phys', 'all']
TITLE = T('Student questions, answered', 'Questions d’élèves, avec réponses', 'Preguntas de estudiantes, respondidas', 'أسئلة الطلاب وإجاباتها', 'Domande degli studenti, con risposta')
DESC = T('Sourced answers to questions students asked SI Helper that the site did not cover yet, by topic: aeronautical engineering, orbital mechanics, physics and general science.',
         'Réponses sourcées aux questions que des élèves ont posées à SI Helper et que le site ne traitait pas encore, par sujet : ingénierie aéronautique, mécanique orbitale, physique et sciences générales.',
         'Respuestas con fuentes a preguntas que los estudiantes hicieron a SI Helper y que el sitio aún no cubría, por tema: ingeniería aeronáutica, mecánica orbital, física y ciencia general.',
         'إجابات موثّقة بالمصادر عن أسئلة طرحها الطلاب على SI Helper ولم يكن الموقع يتناولها بعد، حسب الموضوع: هندسة الطيران والميكانيكا المدارية والفيزياء والعلوم العامة.',
         'Risposte con fonti alle domande che gli studenti hanno fatto a SI Helper e che il sito non trattava ancora, per argomento: ingegneria aeronautica, meccanica orbitale, fisica e scienze generali.')
TOP = {'aero': T('Aeronautical Engineering', 'Ingénierie aéronautique', 'Ingeniería aeronáutica', 'هندسة الطيران', 'Ingegneria aeronautica'),
       'orbit': T('Orbital Mechanics', 'Mécanique orbitale', 'Mecánica orbital', 'الميكانيكا المدارية', 'Meccanica orbitale'),
       'phys': T('Physics', 'Physique', 'Física', 'الفيزياء', 'Fisica'),
       'all': T('General science', 'Sciences générales', 'Ciencia general', 'العلوم العامة', 'Scienze generali')}
SRC = T('Sources', 'Sources', 'Fuentes', 'المصادر', 'Fonti')
CREDIT = T('Created by SI and Biological SI Partner, checked against the sources listed.', 'Créé par SI et Biological SI Partner, vérifié avec les sources indiquées.', 'Creado por SI y Biological SI Partner, comprobado con las fuentes indicadas.', 'من إعداد SI وBiological SI Partner، وتم التحقق منه بالمصادر المذكورة.', 'Creato da SI e Biological SI Partner, verificato con le fonti indicate.')
INTRO = T('When SI Helper can’t answer a question from this site, the question is saved anonymously. Each week we research it and add a sourced answer here.',
          'Quand SI Helper ne peut pas répondre à une question à partir du site, la question est enregistrée anonymement. Chaque semaine, nous faisons des recherches et ajoutons ici une réponse sourcée.',
          'Cuando SI Helper no puede responder una pregunta con este sitio, la pregunta se guarda de forma anónima. Cada semana la investigamos y añadimos aquí una respuesta con fuentes.',
          'عندما لا يستطيع SI Helper الإجابة عن سؤال من هذا الموقع، يُحفظ السؤال دون الكشف عن الهوية. وكل أسبوع نبحث فيه ونضيف هنا إجابة موثّقة بالمصادر.',
          'Quando SI Helper non sa rispondere a una domanda con questo sito, la domanda viene salvata in forma anonima. Ogni settimana facciamo ricerche e aggiungiamo qui una risposta con fonti.')
ADDED = T('Added', 'Ajouté le', 'Añadido el', 'أضيف في', 'Aggiunto il')
ASK = T('Ask SI Helper', 'Demander à SI Helper', 'Pregunta a SI Helper', 'اسأل SI Helper', 'Chiedi a SI Helper')
CSS = ('.sq-top{margin:1.4rem 0 .4rem}.sq{margin:.7rem 0;padding:.8rem 1rem;border-radius:14px;border:1px solid rgba(124,170,255,.45);background:rgba(124,170,255,.07)}'
       '.sq h3{margin:.1rem 0 .4rem;font-size:1.05rem}.sq p{margin:.3rem 0;line-height:1.55}.sq ol{margin:.2rem 0;padding-inline-start:1.3rem;font-size:.92rem}'
       '.sq a{word-break:break-word}.sq .sq-meta{font-size:.82rem;opacity:.85}')
def load():
    doc = json.load(open(DATA, encoding='utf8')); ok, seen = [], set()
    for e in doc.get('entries', []):
        i = e.get('id', '?')
        assert re.fullmatch(r'[a-z0-9-]{3,60}', i) and i not in seen, f'bad/duplicate id {i}'; seen.add(i)
        assert e.get('topic') in TOPICS, f'{i}: topic must be one of {TOPICS}'
        for k in ('q', 'a'):
            assert all(str(e.get(k, {}).get(l, '')).strip() for l in LANGS), f'{i}: {k} needs all 5 languages'
        assert e.get('sources') and all(re.match(r'^https://', s.get('url', '')) and s.get('title') for s in e['sources']), f'{i}: needs https sources with titles'
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', e.get('added', '')), f'{i}: added YYYY-MM-DD'
        if e.get('approved') is True: ok.append(e)
    return ok
def page(l, es):
    secs = ''
    for t in TOPICS:
        xs = [e for e in es if e['topic'] == t]
        if not xs: continue
        secs += f'<h2 class="sq-top" id="{t}">{esc(TOP[t][l])}</h2>'
        for e in xs:
            src = ''.join(f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a></li>' for s in e['sources'])
            secs += (f'<article class="sq" id="{e["id"]}" data-topic="{t}"><h3 dir="auto">{esc(e["q"][l])}</h3>'
                     + ''.join(f'<p dir="auto">{esc(p)}</p>' for p in str(e['a'][l]).split('\n\n') if p.strip())
                     + f'<p class="sq-meta">{esc(SRC[l])}:</p><ol>{src}</ol><p class="sq-meta">{esc(CREDIT[l])} {esc(ADDED[l])} {e["added"]}.</p></article>')
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": l, "url": f'{SITE}{d(l)}{PAGE}',
           "mainEntity": [{"@type": "Question", "name": e['q'][l], "acceptedAnswer": {"@type": "Answer", "text": e['a'][l]}} for e in es]}
    main = (BL.hero(TITLE[l], DESC[l]) + f'<style>{CSS}</style><div class="lw"><p>{esc(INTRO[l])} <a href="{href(l, "Teachers.html")}#ask-si">{esc(ASK[l])}</a></p>{secs}</div>\n')
    head = f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>\n'
    return BL.shell(l, PAGE, TITLE[l], DESC[l], main, extra_head=head, ld_type='WebPage')
if __name__ == '__main__':
    es = load()
    if '--check' in sys.argv: print(f'build-student-qa: {len(es)} approved entries, JSON ok'); sys.exit(0)
    if not es: print('build-student-qa: no approved entries yet, nothing to build'); sys.exit(0)
    ch = sum(wr(d(l) + PAGE, page(l, es)) for l in LANGS)
    idx = {l: [{'id': e['id'], 'topic': e['topic'], 'q': e['q'][l], 'url': f'{d(l)}{PAGE}#{e["id"]}'} for e in es] for l in LANGS}
    ch += wr('search/student-qa.json', json.dumps(idx, ensure_ascii=False, indent=0) + '\n')
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        loc = f'{SITE}{d(l)}{PAGE}'
        if f'<loc>{loc}</loc>' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s); print(f'build-student-qa: {len(es)} entries, writes={ch}')
