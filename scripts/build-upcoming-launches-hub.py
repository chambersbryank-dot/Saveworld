#!/usr/bin/env python3
"""Oct 26 2026 (founder): Upcoming Launches hub page.

Builds Upcoming_Launches.html from the Lakes.html hub chrome (same nav/footer/credits
pattern as Polar / Lakes / Space hubs). Hosts the Live Launch Tracker (assets/launch-tracker.js
from PR #129). WoW canvas hero (assets/launch-hub-hero.js). Artemis_II.html#launches becomes
a short handoff to this hub. Updates nav labels to point here. Idempotent."""
import os, re, html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
E = lambda s, quote=False: html.escape(s, quote=quote)

HUB = 'Upcoming_Launches.html'
HERO_V = '20261027a'
TRACK_V = '20261026d'  # keep in sync with build-launch-tracker.py
IMG = 'RocketLaunch.jpg'  # existing asset; OG card only
HERO_CREDIT = 'Illustration: Saving Planets (canvas animation; no third-party feed)'

TITLE = {
  'en': 'Upcoming Launches | Saving Planets',
  'fr': 'Prochains lancements | Saving Planets',
  'es': 'Próximos lanzamientos | Saving Planets',
  'ar': 'عمليات الإطلاق القادمة | Saving Planets',
  'it': 'Prossimi lanci | Saving Planets',
  'he': 'שיגורים קרובים | Saving Planets',
}
H1 = {
  'en': 'Upcoming Launches',
  'fr': 'Prochains lancements',
  'es': 'Próximos lanzamientos',
  'ar': 'عمليات الإطلاق القادمة',
  'it': 'Prossimi lanci',
  'he': 'שיגורים קרובים',
}
DESC = {
  'en': 'Live upcoming rocket launches with a short note on whether each one directly or indirectly supports Saving Planets solutions — Earth observation, oceans, ice, space weather, planetary defense, and more.',
  'fr': 'Lancements de fusées à venir, en direct, avec une courte note sur le soutien direct ou indirect aux solutions Saving Planets.',
  'es': 'Próximos lanzamientos en vivo, con una nota breve sobre si apoyan de forma directa o indirecta las soluciones de Saving Planets.',
  'ar': 'عمليات إطلاق قادمة مباشرة، مع ملاحظة قصيرة عمّا إذا كانت تدعم حلول Saving Planets مباشرة أو بشكل غير مباشر.',
  'it': 'Prossimi lanci in diretta, con una breve nota sul sostegno diretto o indiretto alle soluzioni Saving Planets.',
  'he': 'שיגורים קרובים בשידור חי, עם הערה קצרה האם הם תומכים ישירות או בעקיפין בפתרונות Saving Planets.',
}
NAV_LABEL = {
  'en': 'Upcoming Launches',
  'fr': 'Prochains lancements',
  'es': 'Próximos lanzamientos',
  'ar': 'عمليات الإطلاق القادمة',
  'it': 'Prossimi lanci',
  'he': 'שיגורים קרובים',
}
HOW_H = {
  'en': 'How each launch saves the world…',
  'fr': 'Comment chaque lancement aide à sauver le monde…',
  'es': 'Cómo cada lanzamiento ayuda a salvar el mundo…',
  'ar': 'كيف يساهم كل إطلاق في إنقاذ العالم…',
  'it': 'Come ogni lancio aiuta a salvare il mondo…',
  'he': 'איך כל שיגור עוזר להציל את העולם…',
}
HOW_LEAD = {
  'en': 'Saving Planets tracks launches so you can see — honestly — which ones feed our work to protect Earth and our solar system, and which do not.',
  'fr': 'Saving Planets suit les lancements pour montrer clairement lesquels alimentent notre travail de protection de la Terre et du système solaire, et lesquels non.',
  'es': 'Saving Planets sigue los lanzamientos para mostrar con claridad cuáles alimentan nuestro trabajo de proteger la Tierra y el sistema solar, y cuáles no.',
  'ar': 'يتتبع Saving Planets الإطلاقات ليبين بوضوح أيّها يغذي عملنا لحماية الأرض ونظامنا الشمسي، وأيّها لا يفعل.',
  'it': 'Saving Planets segue i lanci per mostrare con chiarezza quali alimentano il nostro lavoro per proteggere la Terra e il sistema solare, e quali no.',
  'he': 'Saving Planets עוקב אחר שיגורים כדי להראות בבירור אילו מהם מזינים את עבודתנו להגן על כדור הארץ ועל מערכת השמש, ואילו לא.',
}
HOW_ITEMS = {
  'en': [
    ('Direct', 'Earth observation or planetary / space science that feeds a published solution (oceans, forests, ice, space weather, planetary defense…). We link that exact solution page.'),
    ('Indirect', 'Capacity, communications, emergency alerts, or lower-cost access (for example Starship) that can help the work without being a solution itself. We say so plainly.'),
    ('None', 'Missions that do not support a Saving Planets solution. We note the difference and link the operator when that is allowed.'),
    ('Restricted-led', 'Launches led by Russia, China, North Korea or Iran: when relevant we link our solution only. We never link their operator sites or connect our pages to theirs.'),
  ],
  'fr': [
    ('Direct', 'Observation de la Terre ou science planétaire / spatiale qui alimente une solution publiée. Nous renvoyons à la page exacte de cette solution.'),
    ('Indirect', 'Capacité, communications, alertes d’urgence ou accès moins coûteux (par ex. Starship) qui peuvent aider sans être une solution. Nous le disons clairement.'),
    ('Aucun', 'Missions qui ne soutiennent pas une solution Saving Planets. Nous notons la différence et renvoyons à l’opérateur lorsque c’est autorisé.'),
    ('Opérateur restreint', 'Lancements menés par la Russie, la Chine, la Corée du Nord ou l’Iran : si c’est pertinent, lien vers notre solution uniquement. Jamais vers leurs sites.'),
  ],
  'es': [
    ('Directo', 'Observación de la Tierra o ciencia planetaria / espacial que alimenta una solución publicada. Enlazamos la página exacta de esa solución.'),
    ('Indirecto', 'Capacidad, comunicaciones, alertas de emergencia o acceso más asequible (p. ej. Starship) que pueden ayudar sin ser una solución. Lo decimos con claridad.'),
    ('Ninguno', 'Misiones que no apoyan una solución de Saving Planets. Notamos la diferencia y enlazamos al operador cuando está permitido.'),
    ('Operador restringido', 'Lanzamientos liderados por Rusia, China, Corea del Norte o Irán: si son relevantes, solo enlazamos nuestra solución. Nunca sus sitios.'),
  ],
  'ar': [
    ('مباشر', 'رصد الأرض أو علوم كوكبية / فضائية تغذي حلاً منشورًا. نربط بصفحة ذلك الحل تحديدًا.'),
    ('غير مباشر', 'قدرة أو اتصالات أو تنبيهات طوارئ أو وصول أقل تكلفة (مثل Starship) قد يساعد دون أن يكون حلاً بذاته. نقول ذلك بوضوح.'),
    ('لا يوجد', 'مهام لا تدعم حلاً من Saving Planets. نذكر الفرق ونربط بالمشغّل عندما يُسمح بذلك.'),
    ('مشغّل مقيَّد', 'إطلاقات تقودها روسيا أو الصين أو كوريا الشمالية أو إيران: عند الصلة نربط بحلّنا فقط. لا نربط بمواقعهم أبدًا.'),
  ],
  'it': [
    ('Diretto', 'Osservazione della Terra o scienza planetaria / spaziale che alimenta una soluzione pubblicata. Colleghiamo la pagina esatta di quella soluzione.'),
    ('Indiretto', 'Capacità, comunicazioni, allerte di emergenza o accesso a costi inferiori (es. Starship) che possono aiutare senza essere una soluzione. Lo diciamo chiaramente.'),
    ('Nessuno', 'Missioni che non sostengono una soluzione Saving Planets. Segnaliamo la differenza e colleghiamo l’operatore quando è consentito.'),
    ('Operatore ristretto', 'Lanci guidati da Russia, Cina, Corea del Nord o Iran: se rilevanti, solo il nostro link di soluzione. Mai i loro siti.'),
  ],
  'he': [
    ('ישיר', 'תצפית כדור הארץ או מדע פלנטרי / חלל שמזין פתרון שפורסם. אנו מקשרים לעמוד הפתרון המדויק.'),
    ('עקיף', 'קיבולת, תקשורת, התראות חירום או גישה זולה יותר (למשל Starship) שיכולה לעזור בלי להיות פתרון. אנו מציינים זאת בבירור.'),
    ('אין', 'משימות שאינן תומכות בפתרון של Saving Planets. אנו מציינים את ההבדל ומקשרים למפעיל כשמותר.'),
    ('מפעיל מוגבל', 'שיגורים בהובלת רוסיה, סין, צפון קוריאה או איראן: כשרלוונטי מקשרים רק לפתרון שלנו. לעולם לא לאתריהם.'),
  ],
}
LIVE = {'en': 'Live', 'fr': 'En direct', 'es': 'En vivo', 'ar': 'مباشر', 'it': 'In diretta', 'he': 'חי'}
NOTE = {
  'en': 'Note: Launches shift left and right all the time - stay updated.',
  'fr': 'Remarque : les dates de lancement changent sans cesse — restez informé.',
  'es': 'Nota: las fechas de lanzamiento cambian a menudo — mantente al día.',
  'ar': 'ملاحظة: مواعيد الإطلاق تتغير باستمرار — تابع التحديثات.',
  'it': 'Nota: gli orari di lancio cambiano spesso — resta aggiornato.',
  'he': 'הערה: מועדי שיגור משתנים תדיר — הישארו מעודכנים.',
}
BLURB_NOTE = {
  'en': 'Each launch includes the mission purpose when agencies have published it, plus a short note on whether it supports a Saving Planets solution. Launches that help a solution link to that solution&#x27;s page; others link to the operator&#x27;s official page. If details are not public yet, we say so.',
  'fr': 'Chaque lancement indique l&#x27;objectif de la mission lorsqu&#x27;il est publié, plus une courte note sur son lien avec une solution Saving Planets. Les lancements utiles renvoient à la page de cette solution ; les autres renvoient à la page officielle de l&#x27;opérateur. Si les détails ne sont pas encore publics, nous le disons.',
  'es': 'Cada lanzamiento incluye el propósito de la misión cuando las agencias lo han publicado, más una nota breve sobre si apoya una solución de Saving Planets. Los que ayudan a una solución enlazan a la página de esa solución; los demás enlazan a la página oficial del operador. Si los detalles aún no son públicos, lo decimos.',
  'ar': 'يتضمن كل إطلاق غرض المهمة عندما تنشره الوكالات، مع ملاحظة قصيرة عمّا إذا كان يدعم أحد حلول Saving Planets. الإطلاقات التي تساعد حلاً ترتبط بصفحة ذلك الحل؛ وغيرها ترتبط بالصفحة الرسمية للمشغّل. إن لم تُنشر التفاصيل بعد، نقول ذلك.',
  'it': 'Ogni lancio include lo scopo della missione quando le agenzie lo hanno pubblicato, più una breve nota sul fatto che sostenga o meno una soluzione Saving Planets. I lanci che aiutano una soluzione collegano alla pagina di quella soluzione; gli altri collegano alla pagina ufficiale dell&#x27;operatore. Se i dettagli non sono ancora pubblici, lo diciamo.',
  'he': 'כל שיגור כולל את מטרת המשימה כשהסוכנויות פרסמו אותה, וכן הערה קצרה האם הוא תומך בפתרון של Saving Planets. שיגורים שתומכים בפתרון מקשרים לעמוד הפתרון; אחרים מקשרים לעמוד הרשמי של המפעיל. אם הפרטים עדיין אינם פומביים, אנו מציינים זאת.',
}
MORE = {
  'en': 'Full launch schedule at Next Spaceflight →',
  'fr': 'Calendrier complet des lancements sur Next Spaceflight →',
  'es': 'Calendario completo de lanzamientos en Next Spaceflight →',
  'ar': 'جدول الإطلاق الكامل على Next Spaceflight ←',
  'it': 'Calendario completo dei lanci su Next Spaceflight →',
  'he': 'לוח השיגורים המלא ב-Next Spaceflight ←',
}
DATA_CREDIT = {
  'en': 'Data: The Space Devs Launch Library 2',
  'fr': 'Données : The Space Devs Launch Library 2',
  'es': 'Datos: The Space Devs Launch Library 2',
  'ar': 'البيانات: The Space Devs Launch Library 2',
  'it': 'Dati: The Space Devs Launch Library 2',
  'he': 'נתונים: The Space Devs Launch Library 2',
}
PAUSE = {'en': ('Pause', 'Play'), 'fr': ('Pause', 'Lecture'), 'es': ('Pausa', 'Reproducir'), 'ar': ('إيقاف', 'تشغيل'), 'it': ('Pausa', 'Play'), 'he': ('השהה', 'נגן')}
NEXT_H = {
  'en': 'Next: Explore Another Hub',
  'fr': 'Ensuite : explorer un autre hub',
  'es': 'Siguiente: explorar otro hub',
  'ar': 'التالي: استكشف محورًا آخر',
  'it': 'Avanti: esplora un altro hub',
  'he': 'הבא: חקרו מוקד אחר',
}
ARTEMIS_HANDOFF = {
  'en': ('Live Launch Tracker moved',
         'Upcoming launches — with purpose notes and Saving Planets connections — now live on the Upcoming Launches hub.',
         'Open Upcoming Launches'),
  'fr': ('Suivi des lancements déplacé',
         'Les prochains lancements — avec notes d’objectif et liens Saving Planets — sont sur le hub Prochains lancements.',
         'Ouvrir Prochains lancements'),
  'es': ('Rastreador de lanzamientos trasladado',
         'Los próximos lanzamientos — con notas de propósito y vínculos Saving Planets — están en el hub Próximos lanzamientos.',
         'Abrir Próximos lanzamientos'),
  'ar': ('نُقل متتبع الإطلاقات',
         'عمليات الإطلاق القادمة — مع ملاحظات الغرض وصلات Saving Planets — موجودة الآن في محور عمليات الإطلاق القادمة.',
         'افتح عمليات الإطلاق القادمة'),
  'it': ('Tracker lanci spostato',
         'I prossimi lanci — con note di scopo e legami Saving Planets — sono nel hub Prossimi lanci.',
         'Apri Prossimi lanci'),
  'he': ('מעקב השיגורים הועבר',
         'שיגורים קרובים — עם הערות מטרה וקשרים ל-Saving Planets — נמצאים כעת במוקד השיגורים הקרובים.',
         'פתחו שיגורים קרובים'),
}

def how_html(lang):
    items = ''.join(
        f'<li>{E(lab)} — {E(txt)}</li>' for lab, txt in HOW_ITEMS[lang]
    )
    return (
        f'<section class="impact ul-how" id="how"><h2>{E(HOW_H[lang])}</h2>'
        f'<div class="impact-box"><p>{E(HOW_LEAD[lang])}</p>'
        f'<ul class="ul-how-list">{items}</ul></div></section>'
    )


def tracker_html(lang, pre=''):
    return f'''<section class="launch-widget" id="launches" aria-labelledby="launches-title"><div class="lw-box">
<div class="lw-head"><h2 id="launches-title">{E(H1[lang])}</h2><span class="lw-live" aria-hidden="true"><span class="lw-dot"></span>{E(LIVE[lang])}</span></div>
<div class="lw-next" id="lw-next" aria-live="polite"><p class="lw-loading">…</p></div>
<ul class="lw-list" id="lw-list"></ul>
<p class="lw-note">{NOTE[lang]}</p>
<p class="lw-blurb-note">{BLURB_NOTE[lang]}</p>
<p class="lw-more"><a href="https://www.nextspaceflight.com/" target="_blank" rel="noreferrer">{MORE[lang]}</a></p>
<p class="lw-credit">{DATA_CREDIT[lang]}</p>
</div></section>
<script src="{pre}assets/launch-tracker.js?v={TRACK_V}" defer></script>
<script src="{pre}assets/launch-actions.js?v=20261024a" defer></script>'''

def hero_html(lang):
    pause, play = PAUSE[lang]
    return f'''<section class="page-hero hub-hero ul-hero" id="ul-hero" aria-label="{E(H1[lang])}">
<canvas class="ul-hero-canvas" width="1200" height="480" aria-hidden="true"></canvas>
<div class="page-hero-content ul-hero-copy"><h1>{E(H1[lang])}</h1>
<p class="ul-hero-tag">{E(HOW_LEAD[lang])}</p></div>
<button type="button" class="ul-hero-pause" data-pause="{E(pause)}" data-play="{E(play)}" aria-pressed="false">{E(pause)}</button>
<span class="hero-credit">{E(HERO_CREDIT)}</span>
</section>
<script src="assets/launch-hub-hero.js?v={HERO_V}" defer></script>'''

def next_html(lang):
    return (
        f'<section class="next-solutions" aria-label="{E(NEXT_H[lang])}"><h2>{E(NEXT_H[lang])}</h2><ul>'
        '<li><a href="Space.html">Space</a></li>'
        '<li><a href="Earth_Observation.html">Earth Observation</a></li>'
        '<li><a href="Artemis_II.html">Artemis Program</a></li>'
        '<li><a href="Solutions.html">All Solutions</a></li>'
        '</ul></section>'
    )

def build_en():
    tpl = (ROOT / 'Lakes.html').read_text(encoding='utf-8')
    m = re.search(r'<main id="main">.*?</main>', tpl, re.S)
    if not m:
        raise SystemExit('Lakes.html main missing')
    lm = m.group(0)
    main_html = (
        '<main id="main">\n'
        + hero_html('en') + '\n'
        + how_html('en') + '\n'
        + tracker_html('en') + '\n'
        + next_html('en') + '\n</main>'
    )
    head, body = tpl.split('<body', 1)
    head = head.replace('Lakes.html', HUB)
    head = re.sub(r'<title>[^<]*</title>', f'<title>{E(TITLE["en"])}</title>', head)
    head = re.sub(
        r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*',
        lambda m: m.group(1) + E(DESC['en'], True), head)
    head = re.sub(
        r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*',
        lambda m: m.group(1) + E(TITLE['en'], True), head)
    head = re.sub(
        r'(<meta (?:property|name)="(?:og:image|twitter:image)" content=")[^"]*',
        lambda m: m.group(1) + 'https://www.savingplanets.com/assets/' + IMG, head)
    head = re.sub(r'(sp:category" content=")[^"]*', r'\1space', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    # lightweight WebPage JSON-LD
    ld = {
        '@context': 'https://schema.org', '@type': 'WebPage',
        'name': H1['en'], 'description': DESC['en'],
        'url': f'https://www.savingplanets.com/{HUB}',
        'inLanguage': 'en', 'isPartOf': {'@type': 'WebSite', 'name': 'Saving Planets', 'url': 'https://www.savingplanets.com'},
    }
    head = head.replace('</head>', f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n</head>')
    # CSS for hero (scoped)
    css = '''<style id="ul-hero-css">
.ul-hero{position:relative;overflow:hidden;isolation:isolate;min-height:min(52vh,420px)!important;display:flex;align-items:center;justify-content:center;background:#050b18;color:#fff}
.ul-hero-canvas{position:absolute;inset:0;width:100%;height:100%;z-index:0;display:block}
.ul-hero-copy{position:relative;z-index:1;text-align:center;padding:1rem 1.25rem;max-width:900px;margin:0 auto;text-shadow:0 2px 18px rgba(0,0,0,.65)}
.ul-hero-copy h1{color:#fff!important;margin:0 0 .5rem;font-size:clamp(2rem,5vw,3.2rem)}
.ul-hero-tag{margin:0;font-size:clamp(1rem,2.2vw,1.2rem);color:rgba(232,241,255,.92);line-height:1.45}
.ul-hero-pause{position:absolute;left:.75rem;bottom:.55rem;z-index:2;min-height:44px;min-width:44px;padding:.35rem .75rem;border-radius:999px;border:1px solid rgba(255,255,255,.5);background:rgba(0,20,40,.55);color:#fff;font:700 .8rem/1 Montserrat,"Segoe UI",sans-serif;cursor:pointer}
.ul-hero-pause:focus-visible{outline:2px solid #8fd3ff;outline-offset:2px}
.ul-hero .hero-credit{position:absolute;right:.6rem;bottom:.4rem;z-index:2;font-size:.7rem;color:rgba(255,255,255,.8)}
.ul-how .ul-how-list{margin:.75rem 0 0;padding-inline-start:1.2rem}
.ul-how .ul-how-list li{margin:.45rem 0;line-height:1.45}
@media (prefers-reduced-motion:reduce){.ul-hero-pause{display:none}}
</style>
'''
    head = head.replace('</head>', css + '</head>')
    body = '<body' + body
    body = re.sub(r'<body[^>]*>', '<body data-glass="space" class="toc-sub ul-hub-page" data-glass-tint="space">', body, count=1)
    body = body.replace(lm, main_html)
    body = re.sub(r'<!-- (QUIZ|SHARE|TEACHER|CITE):START -->.*?<!-- \1:END -->\n?', '', body, flags=re.S)
    (ROOT / HUB).write_text(head + body, encoding='utf-8')
    print('wrote', HUB)

def patch_artemis():
    """Replace the live widget on Artemis with a handoff to the hub; keep id=launches."""
    for lang, folder in [('en', ''), ('fr', 'fr'), ('es', 'es'), ('ar', 'ar'), ('it', 'it'), ('he', 'he')]:
        path = ROOT / HUB if False else (ROOT / 'Artemis_II.html' if lang == 'en' else ROOT / folder / 'Artemis_II.html')
        if not path.exists():
            continue
        h = path.read_text(encoding='utf-8')
        title, lead, cta = ARTEMIS_HANDOFF[lang]
        pre = '' if lang == 'en' else '../'
        handoff = (
            f'<section class="launch-widget" id="launches" aria-labelledby="launches-title">'
            f'<div class="lw-box"><div class="lw-head"><h2 id="launches-title">{E(title)}</h2>'
            f'<span class="lw-live" aria-hidden="true"><span class="lw-dot"></span>{E(LIVE[lang])}</span></div>'
            f'<p class="lw-blurb-note" style="margin-top:.5rem">{E(lead)}</p>'
            f'<p class="lw-more"><a href="{pre}{HUB}#launches">{E(cta)} →</a></p>'
            f'<p class="lw-credit">{DATA_CREDIT[lang]}</p></div></section>'
        )
        # Remove tracker/actions scripts for this page's widget (hub hosts them)
        h2 = re.sub(
            r'<section class="launch-widget" id="launches"[^>]*>.*?</section>\s*(?:<!-- EMBED:START -->.*?</section>\s*<!-- EMBED:END -->\s*)?',
            handoff,
            h, count=1, flags=re.S)
        # Some pages nest embed inside section — try alternate if unchanged
        if h2 == h:
            h2 = re.sub(
                r'<section[^>]*id="launches"[^>]*>.*?<!-- EMBED:END -->\s*</section>',
                handoff,
                h, count=1, flags=re.S)
        h2 = re.sub(r'<script src="(?:\.\./)?assets/launch-tracker\.js\?v=[^"]*" defer></script>\n?', '', h2)
        # Keep launch-actions only if lw-next remains (it won't)
        h2 = re.sub(r'<script src="(?:\.\./)?assets/launch-actions\.js\?v=[^"]*" defer></script>\n?', '', h2)
        if h2 != h:
            path.write_text(h2, encoding='utf-8')
            print('artemis handoff', path.relative_to(ROOT))
        elif f'{HUB}#launches' in h:
            print('artemis handoff already', path.relative_to(ROOT))
        else:
            print('WARN: could not patch', path)

def patch_nav_labels():
    """Point Live Launch Tracker nav entries at Upcoming_Launches.html."""
    # build-nav SPACE_KIDS
    nav = (ROOT / 'scripts/build-nav.py').read_text(encoding='utf-8')
    nav2 = nav.replace(
        "SPACE_KIDS = ['Artemis_II.html#launches', 'Enceladus.html',",
        "SPACE_KIDS = ['Upcoming_Launches.html', 'Enceladus.html',",
    )
    if nav2 == nav:
        # already or different formatting
        nav2 = re.sub(
            r"SPACE_KIDS = \['Artemis_II\.html#launches'",
            "SPACE_KIDS = ['Upcoming_Launches.html'",
            nav, count=1)
    (ROOT / 'scripts/build-nav.py').write_text(nav2, encoding='utf-8')

    ux = (ROOT / 'scripts/build-ux.py').read_text(encoding='utf-8')
    # Replace Artemis_II.html#launches keys with Upcoming_Launches.html in items dicts
    for lang, lab in NAV_LABEL.items():
        if lang == 'he':
            continue
        # replace key in items
        ux = ux.replace("'Artemis_II.html#launches'", "'Upcoming_Launches.html'")
    # Also the sl list
    ux = ux.replace("'Artemis_II.html#launches'", "'Upcoming_Launches.html'")
    (ROOT / 'scripts/build-ux.py').write_text(ux, encoding='utf-8')

    # Hebrew / other JSON UI if any
    print('nav labels -> Upcoming_Launches.html')

def ensure_pages_lists():
    for fname in ('i18n/pages.txt', 'i18n/he-pages.txt'):
        p = ROOT / fname
        lines = p.read_text(encoding='utf-8').splitlines()
        if HUB not in lines:
            # insert near Space / Artemis
            out = []
            inserted = False
            for line in lines:
                out.append(line)
                if not inserted and line.strip() in ('Space.html', 'Artemis_II.html'):
                    out.append(HUB)
                    inserted = True
            if not inserted:
                out.append(HUB)
            p.write_text('\n'.join(out) + '\n', encoding='utf-8')
            print('added to', fname)

def seed_i18n():
    """Seed translation memory for hub chrome strings (per-lang pairs; no cross-lang leak)."""
    for lang in ('fr', 'es', 'ar', 'it', 'he'):
        pairs = [
            (HOW_H['en'], HOW_H[lang]),
            (HOW_LEAD['en'], HOW_LEAD[lang]),
            (H1['en'], H1[lang]),
            (DESC['en'], DESC[lang]),
            (TITLE['en'], TITLE[lang]),
            (ARTEMIS_HANDOFF['en'][0], ARTEMIS_HANDOFF[lang][0]),
            (ARTEMIS_HANDOFF['en'][1], ARTEMIS_HANDOFF[lang][1]),
            (ARTEMIS_HANDOFF['en'][2], ARTEMIS_HANDOFF[lang][2]),
        ]
        for (ke, ve), (kt, vt) in zip(HOW_ITEMS['en'], HOW_ITEMS[lang]):
            pairs.append((ke, kt))
            pairs.append((ve, vt))
            pairs.append((f'{ke} — {ve}', f'{kt} — {vt}'))
        jp = ROOT / 'i18n' / f'{lang}.json'
        raw = jp.read_text(encoding='utf-8')
        d = json.loads(raw)
        added = []
        for en, tr in pairs:
            if en not in d:
                added.append(f'{json.dumps(en, ensure_ascii=False)}: {json.dumps(tr, ensure_ascii=False)},')
            elif d.get(en) != tr and en in (
                TITLE['en'], H1['en'], HOW_H['en'], HOW_LEAD['en'], DESC['en'],
                ARTEMIS_HANDOFF['en'][0], ARTEMIS_HANDOFF['en'][1], ARTEMIS_HANDOFF['en'][2],
            ) or any(en == f'{ke} — {ve}' for ke, ve in HOW_ITEMS['en']):
                # keep existing unless we want to force — skip force to avoid churn
                pass
        if added:
            k = raw.index('\n') + 1
            raw = raw[:k] + '\n'.join(added) + '\n' + raw[k:]
            json.loads(raw)
            jp.write_text(raw, encoding='utf-8')
            print('i18n', lang, '+', len(added))


def patch_404_aliases():
    p = ROOT / 'scripts/build-404-case.py'
    s = p.read_text(encoding='utf-8')
    if 'Upcoming_Launches' not in s:
        s2 = s.replace(
            "Artemis_II.html#launches",
            "Upcoming_Launches.html",
        )
        # keep a comment about old alias
        if s2 != s:
            p.write_text(s2, encoding='utf-8')
            print('404 aliases -> Upcoming_Launches.html')

def patch_launch_tracker_builder():
    """Also stamp tracker script onto the hub page."""
    p = ROOT / 'scripts/build-launch-tracker.py'
    s = p.read_text(encoding='utf-8')
    if 'Upcoming_Launches.html' in s:
        print('build-launch-tracker already knows hub')
        return
    # After EN Artemis handling, also ensure hub has script tag — simpler: document in comment
    # Hub embeds script itself; build-launch-actions already globs all #lw-next pages.
    print('hub embeds tracker directly; launch-actions will pick up #lw-next')

def notes():
    p = ROOT / 'NOTES.md'
    s = p.read_text(encoding='utf-8')
    entry = (
        '- Oct 26 (~7:55 PM HST, founder): **Upcoming Launches hub** (`Upcoming_Launches.html`, 6 langs). '
        'Same hub chrome as Lakes/Polar (nav/footer/credits). WoW canvas hero (rocket arc → orbit over rotating Earth; '
        'prefers-reduced-motion + Pause). Section “How each launch saves the world…” (direct / indirect / none / restricted). '
        'Live tracker + PR #129 blurbs live here; Artemis_II.html#launches handoff link; nav “Upcoming Launches”. '
        'Generator: scripts/build-upcoming-launches-hub.py. PR open — do not merge until approved.\n\n'
    )
    if 'Upcoming Launches hub' in s:
        return
    lines = s.splitlines(True)
    for i, line in enumerate(lines[:40]):
        if line.startswith('- '):
            lines.insert(i, entry)
            break
    p.write_text(''.join(lines), encoding='utf-8')
    print('NOTES updated')

def sync_hero_script_version():
    """Keep launch-hub-hero.js?v= in sync on every language hub (i18n copies lag build_en)."""
    rx = re.compile(r'launch-hub-hero\.js\?v=[^"\']+')
    n = 0
    for lang in LANGS:
        path = ROOT / ('Upcoming_Launches.html' if lang == 'en' else f'{lang}/Upcoming_Launches.html')
        if not path.exists():
            continue
        raw = path.read_text(encoding='utf-8')
        new = rx.sub(f'launch-hub-hero.js?v={HERO_V}', raw)
        # also ensure relative prefix for non-en
        if lang != 'en':
            new = new.replace('src="assets/launch-hub-hero.js', 'src="../assets/launch-hub-hero.js')
            new = new.replace("src='assets/launch-hub-hero.js", "src='../assets/launch-hub-hero.js")
        if new != raw:
            path.write_text(new, encoding='utf-8')
            n += 1
    print(f'sync_hero_script_version: {n} pages')

def main():
    build_en()
    patch_nav_labels()
    ensure_pages_lists()
    seed_i18n()
    patch_404_aliases()
    patch_launch_tracker_builder()
    # Artemis EN first; translations rebuilt by i18n later — still patch all existing lang copies
    patch_artemis()
    notes()
    print('done')

if __name__ == '__main__':
    main()
