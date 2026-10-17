#!/usr/bin/env python3
"""Oct 15 UX pass (all langs, idempotent; run after i18n-build/post-processors in weekly-sync.sh):
grouped nav + sticky Help/Donate, homepage impact strip / domain sections / latest updates, Solutions
domain+hub filter and per-hub 'show more', auto solution counts, lazy images, About video 720p-first
preload=none, canonical / for index pages, distinct FR/ES Hope Spots titles."""
import re, json, glob, os, html
LANGS = ['en', 'fr', 'es', 'ar', 'it']
SITE = 'https://www.savingplanets.com/'
def d(l): return '' if l == 'en' else l + '/'
def rd(p): return open(p, encoding='utf8').read()
def wr(p, s):
    if rd(p) != s: open(p, 'w', encoding='utf8').write(s); return 1
    return 0
def block(s, name, new, anchor_re=None, before=True):
    pat = re.compile(r'<!-- %s:START -->.*?<!-- %s:END -->' % (name, name), re.S)
    new = '<!-- %s:START -->%s<!-- %s:END -->' % (name, new, name)
    if pat.search(s): return pat.sub(lambda m: new, s, 1)
    if anchor_re:
        m = re.search(anchor_re, s, re.S)
        if m: return s[:m.start()] + new + s[m.start():] if before else s[:m.end()] + new + s[m.end():]
    return s

T = {
 'en': dict(sol='Solutions', kt='Kids &amp; Teachers', sl='Space &amp; Launches', gi='Get Involved', ab='About', help='Help / Donate',
   items={'Solutions.html':'All Solutions','World_Map.html':'World Map','Oceans.html':'Ocean','Rivers.html':'Rivers','Lakes.html':'Lakes','Deforestation.html':'Forests','Earth_Observation.html':'Earth Observation','Search.html':'Search','Topics.html':'Topics A to Z',
     'Kids_Map.html':'Kids Planet Map','Amazing_Facts.html':'Amazing Facts','Satellite_Explorer.html':'Satellite Explorer','Lesson_Builder.html':'Lesson Plan Builder','Teachers.html':'Teacher Sheets','Myth_vs_Fact.html':'Myth vs Fact','Glossary.html':'Glossary',
     'Space.html':'Space','Artemis_II.html#launches':'Live Launch Tracker','Planetary_Defense.html':'Planetary Defense','Space_Weather.html':'Space Weather','Space_Disposal.html':'Space Disposal','Project-Rawane.html':'Project Rawane','Rawanes_Mission_Log.html':"Rawane's Mission Log",
     'Ways_to_Help.html':'Ways to Help','Find_a_Cleanup.html':'Find a Cleanup','index.html#newsletter':'Weekly Brief','Contact.html':'Contact',
     'About.html':'About Us','Editorial_Policy.html':'Editorial Policy','Corrections.html':'Corrections','Press.html':'Press &amp; Media','Privacy.html':'Privacy'},
   cta1='Explore All Solutions', cta2='Ways to help', imp=['real, sourced solutions','solution hubs','languages','learning tools for kids and teachers'],
   dom=[('Water','Oceans, rivers and lakes'),('Land','Forests and the people who live with them'),('Space','Satellites, missions and keeping orbit clean')],
   seeall='See all {n} {d} solutions', news='Latest Updates', newsintro='What changed on the site recently. Sign up for the Weekly Brief to get it every week.',
   kidsh='Kids &amp; Teachers', filt='Show', all='All', more='Show all {n}', less='Show fewer', hub='Hub', allhubs='All hubs', menu='Menu'),
 'fr': dict(sol='Solutions', kt='Enfants et enseignants', sl='Espace et lancements', gi='Agir', ab='À propos', help='Aider / Faire un don',
   items={'Solutions.html':'Toutes les solutions','World_Map.html':'Carte du monde','Oceans.html':'Océan','Rivers.html':'Rivières','Lakes.html':'Lacs','Deforestation.html':'Forêts','Earth_Observation.html':'Observation de la Terre','Search.html':'Recherche','Topics.html':'Sujets de A à Z',
     'Kids_Map.html':'Carte de la planète pour enfants','Amazing_Facts.html':'Faits étonnants','Satellite_Explorer.html':'Explorateur de satellites','Lesson_Builder.html':'Générateur de plans de cours','Teachers.html':'Fiches enseignants','Myth_vs_Fact.html':'Mythe ou réalité','Glossary.html':'Glossaire',
     'Space.html':'Espace','Artemis_II.html#launches':'Suivi des lancements en direct','Planetary_Defense.html':'Défense planétaire','Space_Weather.html':'Météo spatiale','Space_Disposal.html':'Élimination des débris spatiaux','Project-Rawane.html':'Projet Rawane','Rawanes_Mission_Log.html':'Journal de mission de Rawane',
     'Ways_to_Help.html':'Comment aider','Find_a_Cleanup.html':'Trouver un nettoyage','index.html#newsletter':'Bulletin hebdomadaire','Contact.html':'Contact',
     'About.html':'Qui sommes-nous','Editorial_Policy.html':'Politique éditoriale','Corrections.html':'Corrections','Press.html':'Presse et médias','Privacy.html':'Confidentialité'},
   cta1='Explorer toutes les solutions', cta2='Comment aider', imp=['solutions réelles et sourcées','pôles de solutions','langues','outils pour enfants et enseignants'],
   dom=[('Eau','Océans, rivières et lacs'),('Terre','Les forêts et les personnes qui y vivent'),('Espace','Satellites, missions et une orbite plus propre')],
   seeall='Voir les {n} solutions : {d}', news='Dernières nouveautés', newsintro='Ce qui a changé récemment sur le site. Abonnez-vous au bulletin hebdomadaire pour le recevoir chaque semaine.',
   kidsh='Enfants et enseignants', filt='Afficher', all='Tout', more='Tout afficher ({n})', less='Afficher moins', hub='Pôle', allhubs='Tous les pôles', menu='Menu'),
 'es': dict(sol='Soluciones', kt='Niños y docentes', sl='Espacio y lanzamientos', gi='Participa', ab='Acerca de', help='Ayudar / Donar',
   items={'Solutions.html':'Todas las soluciones','World_Map.html':'Mapa mundial','Oceans.html':'Océano','Rivers.html':'Ríos','Lakes.html':'Lagos','Deforestation.html':'Bosques','Earth_Observation.html':'Observación de la Tierra','Search.html':'Buscar','Topics.html':'Temas de la A a la Z',
     'Kids_Map.html':'Mapa del Planeta para niños','Amazing_Facts.html':'Datos asombrosos','Satellite_Explorer.html':'Explorador de satélites','Lesson_Builder.html':'Creador de planes de clase','Teachers.html':'Fichas para docentes','Myth_vs_Fact.html':'Mito o realidad','Glossary.html':'Glosario',
     'Space.html':'Espacio','Artemis_II.html#launches':'Rastreador de lanzamientos en vivo','Planetary_Defense.html':'Defensa planetaria','Space_Weather.html':'Clima espacial','Space_Disposal.html':'Retiro de basura espacial','Project-Rawane.html':'Proyecto Rawane','Rawanes_Mission_Log.html':'Bitácora de Rawane',
     'Ways_to_Help.html':'Formas de ayudar','Find_a_Cleanup.html':'Encuentra una limpieza','index.html#newsletter':'Boletín semanal','Contact.html':'Contacto',
     'About.html':'Quiénes somos','Editorial_Policy.html':'Política editorial','Corrections.html':'Correcciones','Press.html':'Prensa','Privacy.html':'Privacidad'},
   cta1='Explorar todas las soluciones', cta2='Formas de ayudar', imp=['soluciones reales y con fuentes','centros de soluciones','idiomas','herramientas para niños y docentes'],
   dom=[('Agua','Océanos, ríos y lagos'),('Tierra','Los bosques y las personas que viven en ellos'),('Espacio','Satélites, misiones y una órbita más limpia')],
   seeall='Ver las {n} soluciones de {d}', news='Últimas novedades', newsintro='Lo que cambió recientemente en el sitio. Suscríbete al boletín semanal para recibirlo cada semana.',
   kidsh='Niños y docentes', filt='Mostrar', all='Todo', more='Ver todas ({n})', less='Ver menos', hub='Centro', allhubs='Todos los centros', menu='Menú'),
 'ar': dict(sol='الحلول', kt='الأطفال والمعلمون', sl='الفضاء والإطلاقات', gi='شارك', ab='من نحن', help='ساعد / تبرّع',
   items={'Solutions.html':'كل الحلول','World_Map.html':'خريطة العالم','Oceans.html':'المحيط','Rivers.html':'الأنهار','Lakes.html':'البحيرات','Deforestation.html':'الغابات','Earth_Observation.html':'رصد الأرض','Search.html':'بحث','Topics.html':'المواضيع من الألف إلى الياء',
     'Kids_Map.html':'خريطة الكوكب للأطفال','Amazing_Facts.html':'حقائق مذهلة','Satellite_Explorer.html':'مستكشف الأقمار الصناعية','Lesson_Builder.html':'منشئ خطط الدروس','Teachers.html':'أوراق المعلمين','Myth_vs_Fact.html':'خرافة أم حقيقة','Glossary.html':'المسرد',
     'Space.html':'الفضاء','Artemis_II.html#launches':'متتبع الإطلاقات المباشر','Planetary_Defense.html':'الدفاع الكوكبي','Space_Weather.html':'طقس الفضاء','Space_Disposal.html':'التخلص من الحطام الفضائي','Project-Rawane.html':'مشروع Rawane','Rawanes_Mission_Log.html':'سجل مهمة Rawane',
     'Ways_to_Help.html':'طرق المساعدة','Find_a_Cleanup.html':'ابحث عن حملة تنظيف','index.html#newsletter':'النشرة الأسبوعية','Contact.html':'اتصل بنا',
     'About.html':'من نحن','Editorial_Policy.html':'السياسة التحريرية','Corrections.html':'التصحيحات','Press.html':'الصحافة والإعلام','Privacy.html':'الخصوصية'},
   cta1='استكشف كل الحلول', cta2='طرق المساعدة', imp=['حلًا حقيقيًا موثقًا','مراكز حلول','لغات','أدوات للأطفال والمعلمين'],
   dom=[('الماء','المحيطات والأنهار والبحيرات'),('اليابسة','الغابات والناس الذين يعيشون فيها'),('الفضاء','الأقمار الصناعية والبعثات ومدار أنظف')],
   seeall='عرض كل الحلول ({n}): {d}', news='آخر المستجدات', newsintro='ما تغيّر مؤخرًا في الموقع. اشترك في النشرة الأسبوعية لتصلك كل أسبوع.',
   kidsh='الأطفال والمعلمون', filt='عرض', all='الكل', more='عرض الكل ({n})', less='عرض أقل', hub='المركز', allhubs='كل المراكز', menu='القائمة'),
 'it': dict(sol='Soluzioni', kt='Bambini e insegnanti', sl='Spazio e lanci', gi='Partecipa', ab='Chi siamo', help='Aiuta / Dona',
   items={'Solutions.html':'Tutte le soluzioni','World_Map.html':'Mappa del mondo','Oceans.html':'Oceano','Rivers.html':'Fiumi','Lakes.html':'Laghi','Deforestation.html':'Foreste','Earth_Observation.html':'Osservazione della Terra','Search.html':'Cerca','Topics.html':'Argomenti dalla A alla Z',
     'Kids_Map.html':'Mappa del pianeta per bambini','Amazing_Facts.html':'Fatti incredibili','Satellite_Explorer.html':'Esploratore di satelliti','Lesson_Builder.html':'Generatore di piani di lezione','Teachers.html':'Schede per insegnanti','Myth_vs_Fact.html':'Mito o realtà','Glossary.html':'Glossario',
     'Space.html':'Spazio','Artemis_II.html#launches':'Lanci in diretta','Planetary_Defense.html':'Difesa planetaria','Space_Weather.html':'Meteo spaziale','Space_Disposal.html':'Smaltimento dei detriti spaziali','Project-Rawane.html':'Progetto Rawane','Rawanes_Mission_Log.html':'Diario di missione di Rawane',
     'Ways_to_Help.html':'Come aiutare','Find_a_Cleanup.html':'Trova un evento di pulizia','index.html#newsletter':'Notiziario settimanale','Contact.html':'Contatti',
     'About.html':'Chi siamo','Editorial_Policy.html':'Politica editoriale','Corrections.html':'Correzioni','Press.html':'Stampa e media','Privacy.html':'Privacy'},
   cta1='Esplora tutte le soluzioni', cta2='Come aiutare', imp=['soluzioni reali e con fonti','hub di soluzioni','lingue','strumenti per bambini e insegnanti'],
   dom=[('Acqua','Oceani, fiumi e laghi'),('Terra','Le foreste e le persone che ci vivono'),('Spazio','Satelliti, missioni e un’orbita più pulita')],
   seeall='Vedi tutte le {n} soluzioni: {d}', news='Ultime novità', newsintro='Cosa è cambiato di recente sul sito. Iscriviti al Notiziario settimanale per riceverle ogni settimana.',
   kidsh='Bambini e insegnanti', filt='Mostra', all='Tutto', more='Mostra tutte ({n})', less='Mostra meno', hub='Hub', allhubs='Tutti gli hub', menu='Menu'),
}
# Oct 15 item 5: 5 doors, no duplicates. World Map + Mission Log live only under Project Rawane;
# Education has its own Kids & Teachers door; About folded into Get Involved (policy pages stay in the footer).
GROUPS = [('sol', ['Solutions.html','Oceans.html','Rivers.html','Lakes.html','Deforestation.html','Earth_Observation.html','Search.html','Topics.html']),
  ('kt', ['Play_and_Learn.html','Kids_Map.html','Amazing_Facts.html','Satellite_Explorer.html','Lesson_Builder.html','Teachers.html','Myth_vs_Fact.html','Glossary.html']),
  ('le', ['Learn.html','Orbits_Guide.html','Orbit_Math.html','Orbit_Lab.html','Aero_Guide.html','Aero_Math.html','Aero_Lab.html','Physics_Guide.html','Physics_Math.html','Physics_Lab.html','Calculators.html','Cadets.html','Homeschool.html','AP_IB_Physics.html','Careers.html']),  # Oct 16: Learn door (3 tracks; labels from learn_text.py)
  ('sl', ['Space.html','Artemis_II.html#launches','Planetary_Defense.html','Space_Weather.html','Space_Disposal.html']),
  ('pr', ['Project-Rawane.html','Rawanes_Mission_Log.html','World_Map.html']),
  ('gi', ['Ways_to_Help.html','Find_a_Cleanup.html','index.html#newsletter','Contact.html','About.html'])]
PR = {'en': ('Project Rawane', ['About Project Rawane', "Rawane&#x27;s Mission Log", 'Solutions Pinned to the World']),
      'fr': ('Projet Rawane', ['À propos du projet Rawane', 'Journal de mission de Rawane', 'Solutions épinglées sur le monde']),
      'es': ('Proyecto Rawane', ['Acerca del Proyecto Rawane', 'Bitácora de Rawane', 'Soluciones fijadas en el mundo']),
      'ar': ('مشروع Rawane', ['عن مشروع Rawane', 'سجل مهمة Rawane', 'حلول مثبتة على العالم']),
      'it': ('Progetto Rawane', ['Il Progetto Rawane', 'Diario di missione di Rawane', 'Soluzioni fissate nel mondo'])}
DOMAINS = [['Oceans.html','Rivers.html','Lakes.html'], ['Deforestation.html'],
           ['Space.html','Project-Rawane.html','Earth_Observation.html','Planetary_Defense.html','Space_Weather.html','Space_Disposal.html']]
DOMAIN_IMG = ['assets/videos/great-bubble-barrier.jpg', None, None]

PLAYL = {'en': '🎮 Play &amp; Learn', 'fr': '🎮 Jouer et apprendre', 'es': '🎮 Juega y aprende', 'ar': '🎮 العب وتعلّم', 'it': '🎮 Gioca e impara'}  # Oct 15 item 9
import sys as _sys; _sys.path.insert(0, 'scripts'); import learn_text as _LT  # Oct 16 Learn door labels
def nav_html(l, page):
    t = T[l]; out = []
    for key, items in GROUPS:
        cur = any(page == i.split('#')[0] for i in items if '#' not in i)
        def hr(i): return i if l == 'en' or os.path.exists(d(l) + i.split('#')[0]) else '../' + i
        lab = (lambda i: PR[l][1][items.index(i)]) if key == 'pr' else (lambda i: _LT.NAV_ITEMS[i][l]) if key == 'le' else (lambda i: PLAYL[l] if i == 'Play_and_Learn.html' else t["items"][i])
        lis = ''.join(f'<li><a href="{hr(i)}"{" aria-current=\"page\"" if i == page else ""}>{lab(i)}</a></li>' for i in items)
        name = PR[l][0] if key == 'pr' else _LT.NAV[l] if key == 'le' else t[key]
        if key == 'pr': cur = page in ('Project-Rawane.html', 'Rawanes_Mission_Log.html', 'World_Map.html')
        out.append(f'<li class="nav-group nav-{key}{" is-current" if cur else ""}"><details><summary aria-haspopup="true" aria-expanded="false">{name}</summary><ul class="nav-sub">{lis}</ul></details></li>')
    return ''.join(out)

def sol_cards(l):
    s = rd(d(l) + 'Solutions.html'); hubs = {}
    for m in re.finditer(r'<section ([^>]*class="card-band sol-hub"[^>]*)>(.*?)</section>', s, re.S):
        a = m.group(1); hid = re.search(r'\bid="([^"]+)"', a).group(1); hub = re.search(r'data-hub="([^"]+)"', a).group(1)
        m = type('M', (), {'group': lambda self, i, _v=(None, hid, hub, m.group(2)): _v[i]})()
        name = re.search(r'<h2><a[^>]*>(.*?)</a>', m.group(3)).group(1)
        cards = re.findall(r'<article class="card sol-card".*?</article>', m.group(3), re.S)
        hubs[m.group(2)] = dict(id=m.group(1), name=name, cards=cards)
    return hubs

def count_solutions():
    return len(re.findall(r'<article class="card sol-card"', rd('Solutions.html')))

MEDIA = json.load(open('assets/data/media-manifest.json')) if os.path.exists('assets/data/media-manifest.json') else {}
def mini(card):
    url = re.search(r'data-url="([^"]+)"', card).group(1)
    img = re.search(r'<img[^>]*>', card).group(0)
    img = re.sub(r'\sloading="[^"]*"', '', img).replace('<img', '<img loading="lazy"', 1)
    # Oct 16: responsive card images (scripts/r2-cards.py puts WebP widths on R2); the repo JPEG stays the src fallback
    m = re.search(r'\ssrc="(?:\.\./)?assets/og/([a-z]{2})/([^"?]+)', img)
    e = MEDIA.get(f'images/og/{m.group(1)}/{m.group(2)}') if m else None
    if e and e.get('srcset') and 'srcset=' not in img:
        img = img.replace('<img', f'<img srcset="{e["srcset"]}" sizes="(max-width:700px) 92vw, (max-width:1100px) 46vw, 380px"', 1)
    h3 = re.search(r'<h3>.*?</h3>', card, re.S).group(0)
    desc = re.search(r'<p class="sol-desc"><span>(.*?)</span>', card, re.S)
    return f'<article class="dom-card"><a class="dom-img" href="{url}">{img}</a>{h3}<p>{desc.group(1) if desc else ""}</p></article>'

def home(l, n, hubs):
    t = T[l]; p = d(l) + 'index.html'; s = rd(p); pre = '' if l == 'en' else '../'
    imp = [n, len(hubs), len(LANGS), 3]  # EN+FR+ES+AR+IT
    strip = '<section class="impact-strip" aria-label="Saving Planets">' + ''.join(
        f'<div class="imp-item"><span class="imp-num">{v}</span><span class="imp-label">{lab}</span></div>' for v, lab in zip(imp, t['imp'])) + '</section>'
    s = block(s, 'IMPACT', strip, r'<!-- DIFF:START -->')
    s = re.sub(r'<!-- DIFF:START -->.*?<!-- DIFF:END -->\n?', '', s, flags=re.S)  # replaced by the impact strip (hard-coded count)
    cta = f'<p class="hero-ctas"><a class="btn hero-cta" href="Solutions.html">{DROP}{t["cta1"]}</a><a class="btn hero-cta2" href="Ways_to_Help.html">{t["cta2"]}</a></p>'
    s = block(s, 'HERO-CTA', cta, r'<p class="hero-email">')
    secs = []
    for i, (hs, (dn, dd)) in enumerate(zip(DOMAINS, t['dom'])):
        cards = [c for h in hs if h in hubs for c in hubs[h]['cards']]
        if not cards: continue
        rr = [c for i in range(6) for h in hs if h in hubs and len(hubs[h]['cards']) > i for c in [hubs[h]['cards'][i]]]
        feat = ''.join(mini(c) for c in rr[:3])
        chips = ''.join(f'<a class="dom-chip" href="Solutions.html#{hubs[h]["id"]}">{hubs[h]["name"]} ({len(hubs[h]["cards"])})</a>' for h in hs if h in hubs)
        cls = ['water', 'land', 'space'][i]
        secs.append(f'<section class="domain domain-{cls}" aria-labelledby="dom-{cls}"><div class="dom-head"><h2 id="dom-{cls}">{dn}</h2>{"" if cls == "water" else f"<p>{dd}</p>"}<div class="dom-chips">{chips}</div></div><div class="dom-grid">{feat}</div>'
                    f'<p class="dom-all"><a class="btn" href="Solutions.html?domain={cls}">{t["seeall"].format(n=len(cards), d=dn)}</a></p></section>')
    s = block(s, 'DOMAINS', ''.join(secs), r'<!-- AUDIENCE:START -->')
    try:
        ent = json.load(open('scripts/newsletter-updates.json', encoding='utf8'))['entries']
        ent = sorted(ent, key=lambda e: e['date'], reverse=True)[:5]
        lis = ''.join(f'<li><time datetime="{e["date"]}">{e["date"]}</time> <a href="{e["page"]}">{e["what"].get(l) or e["what"]["en"]}</a></li>' for e in ent)
    except Exception: lis = ''
    news = f'<section class="news-briefs" aria-labelledby="news-h"><h2 id="news-h">{t["news"]}</h2><p>{t["newsintro"]}</p><ul class="news-list">{lis}</ul></section>'
    s = block(s, 'NEWS', news, r'<section [^>]*newsletter-band')
    if 'id="newsletter"' not in s: s = re.sub(r'<section ([^>]*newsletter-band)', r'<section id="newsletter" \1', s, count=1)
    return wr(p, s)

CSS = r"""
/* UX-OCT15:START */
.nav-links{gap:1.1rem}
.nav-group details{position:relative}
.nav-group summary{list-style:none;cursor:pointer;color:#fff;font-weight:600;font-size:1.05rem;padding:.3rem 0;white-space:nowrap}
html.dark nav.scrolled .nav-group summary{color:#fff}
.nav-group summary::-webkit-details-marker{display:none}
.nav-group summary::after{content:" ▾";font-size:.8em}
nav.scrolled .nav-group summary{color:#003755}
.nav-group.is-current summary{text-decoration:underline;text-underline-offset:6px}
.nav-sub{position:absolute;top:100%;inset-inline-start:0;min-width:230px;background:#fff;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.18);padding:.5rem;list-style:none;margin:.4rem 0 0;z-index:1200}
.nav-sub a{display:block;color:#003755 !important;font-size:1rem;padding:.55rem .7rem;border-radius:8px}
.nav-sub a:hover,.nav-sub a[aria-current]{background:#e6f5fc;color:#0b3a53 !important}
.nav-help a{background:#2e9e4f !important;color:#fff !important;border:0 !important;padding:.5rem .9rem;border-radius:999px;white-space:nowrap}
.sticky-help{position:fixed;inset-inline-end:16px;bottom:16px;z-index:1100;background:#2e9e4f;color:#fff;font-weight:700;padding:.75rem 1.1rem;border-radius:999px;box-shadow:0 6px 18px rgba(0,0,0,.25);text-decoration:none}
.sticky-help:hover{background:#23803f;color:#fff}
@media (min-width:901px){nav .nav-container{padding-inline:clamp(10px,1.6vw,40px) !important;max-width:1500px !important}nav .brand-word{font-size:clamp(.72rem,1vw,1.05rem) !important;white-space:nowrap;flex:none;margin-inline-end:clamp(.4rem,1vw,1rem)}.nav-links{gap:clamp(.3rem,.9vw,.9rem) !important;flex-wrap:nowrap}.nav-group summary{font-size:clamp(.7rem,1vw,1.02rem) !important}nav .nav-links .lang-switch,nav .nav-links .lang-switch *{font-size:clamp(.62rem,.8vw,.88rem) !important;white-space:nowrap;letter-spacing:0}nav .nav-links .lang-switch{gap:.15rem}nav .nav-links .nav-help a{font-size:clamp(.68rem,.9vw,.98rem) !important;padding:.35em .75em !important}}
@media (min-width:901px) and (max-width:1100px){nav .nav-sub{position:absolute !important;min-width:250px !important;padding:.5rem !important;box-shadow:0 10px 30px rgba(0,0,0,.35) !important}nav .nav-sub a{font-size:.95rem !important;white-space:normal}}
html.dark nav.open .nav-group summary,html.dark nav .nav-links .nav-group summary{color:#fff}
@media (min-width:901px) and (max-width:1000px){nav .nav-links{gap:.22rem !important}nav .nav-group summary{font-size:.64rem !important}nav .brand-word{font-size:.66rem !important;margin-inline-end:.3rem}nav .nav-links .lang-switch,nav .nav-links .lang-switch *{font-size:.58rem !important}nav .nav-links .nav-help a{font-size:.62rem !important;padding:.3em .55em !important}}
@media (max-width:1100px){.nav-sub{position:static;box-shadow:none;padding:0 0 0 .8rem;min-width:0}
 nav.open .nav-group summary{color:#003755;padding:.6rem 0;font-size:1.1rem}}
html.dark .nav-sub{background:#0f1b26}@supports ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){@media (min-width:1101px){html.dark .nav-sub{background:linear-gradient(180deg,rgba(255,255,255,.12),rgba(255,255,255,.03)),rgba(15,27,38,.82);-webkit-backdrop-filter:blur(16px) saturate(180%);backdrop-filter:blur(16px) saturate(180%);border:1px solid rgba(255,255,255,.22);box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 10px 30px rgba(0,0,0,.35)}}} html.dark .nav-sub a{color:#e8eef5 !important}
.hero-ctas{display:flex;flex-wrap:wrap;gap:.8rem;margin:1.2rem 0 .6rem}
.hero-ctas .btn{font-size:1.1rem;padding:.8rem 1.4rem}
.hero-cta{display:inline-flex;align-items:center;gap:.45rem}/* Liquid Glass: translucent, page background shows through; solid fallback without backdrop-filter */
.hero-ctas .hero-cta,.wm-cta .btn,.nav-help a,.sticky-help{border-radius:999px !important;color:#fff !important;background:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06)),var(--lg-tint) !important;border:1px solid rgba(255,255,255,.35) !important;box-shadow:inset 0 1px 0 rgba(255,255,255,.55),inset 0 -1px 0 rgba(255,255,255,.08),0 6px 20px rgba(0,0,0,.28) !important;-webkit-backdrop-filter:blur(14px) saturate(180%);backdrop-filter:blur(14px) saturate(180%);text-shadow:0 1px 2px rgba(0,0,0,.45)}
.hero-ctas .hero-cta:hover,.wm-cta .btn:hover,.nav-help a:hover,.sticky-help:hover{background:linear-gradient(180deg,rgba(255,255,255,.3),rgba(255,255,255,.1)),var(--lg-tint) !important}
.hero-ctas .hero-cta:focus-visible,.wm-cta .btn:focus-visible,.nav-help a:focus-visible,.sticky-help:focus-visible{outline:3px solid #fff;outline-offset:3px}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.hero-ctas .hero-cta,.wm-cta .btn,.nav-help a,.sticky-help{background:var(--lg-solid) !important}}
body{--lg-tint:rgba(12,28,56,.55);--lg-solid:#1d3f73}body[data-glass-tint=water]{--lg-tint:rgba(0,95,150,.55);--lg-solid:#005f96}body[data-glass-tint=land]{--lg-tint:rgba(38,110,42,.55);--lg-solid:#26702a}body[data-glass-tint=space]{--lg-tint:rgba(74,58,168,.55);--lg-solid:#4a3aa8}body[data-glass-tint=help]{--lg-tint:rgba(30,110,70,.55);--lg-solid:#1e6e46}
/* Ways to Help: Donate / Join buttons in Liquid Glass (Donate = page tint, Join = teal tint) */
.help-btns .help-btn,.help-table .help-btn,.help-actions .help-btn,a.help-btn{border-radius:999px !important;color:#fff !important;text-decoration:none !important;background:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06)),var(--lg-tint) !important;border:1px solid rgba(255,255,255,.35) !important;box-shadow:inset 0 1px 0 rgba(255,255,255,.55),0 4px 14px rgba(0,0,0,.25) !important;-webkit-backdrop-filter:blur(12px) saturate(180%);backdrop-filter:blur(12px) saturate(180%);text-shadow:0 1px 2px rgba(0,0,0,.45)}
a.help-btn.help-btn-join{background:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06)),rgba(0,120,105,.6) !important}
a.help-btn:hover{filter:brightness(1.15)}a.help-btn:focus-visible{outline:3px solid #fff;outline-offset:3px}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){a.help-btn{background:var(--lg-solid) !important}a.help-btn.help-btn-join{background:#00695c !important}}
.hero-cta2{background:transparent !important;border:2px solid #fff;color:#fff !important}
.impact-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;max-width:1100px;margin:1.5rem auto;padding:1.2rem;background:#003755;color:#fff;border-radius:16px;text-align:center}
.imp-num{display:block;font-size:2.4rem;font-weight:800;color:#7fd3ff}
.imp-label{font-size:.95rem}
.domain{max-width:1150px;margin:2.5rem auto;padding:0 1rem}
.dom-head h2{margin:0 0 .2rem;font-size:2rem}
.domain-water .dom-head h2{color:#0077b6}.domain-land .dom-head h2{color:#2e7d32}.domain-space .dom-head h2{color:#4a3aa8}
.dom-chips{display:flex;flex-wrap:wrap;gap:.5rem;margin:.6rem 0 1rem}
.dom-chip{border:1px solid #9cc;border-radius:999px;padding:.35rem .8rem;text-decoration:none;font-size:.95rem}
.dom-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem}
.dom-card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,.08)}
.dom-card img{width:100%;height:190px;object-fit:cover;display:block}
.dom-card h3{font-size:1.15rem;margin:.8rem 1rem .3rem}.dom-card p{margin:0 1rem 1rem;font-size:.97rem}
html.dark .dom-card{background:#13232f}
.dom-all{text-align:center;margin-top:1.2rem}
.news-briefs{max-width:1000px;margin:2.5rem auto;padding:0 1rem}
.news-list{list-style:none;padding:0}.news-list li{padding:.7rem 0;border-bottom:1px solid #dde}
.news-list time{font-weight:700;color:#0077b6;margin-inline-end:.5rem}
@media (max-width:900px){.dom-grid{grid-template-columns:1fr 1fr}.impact-strip{grid-template-columns:1fr 1fr}}
@media (max-width:600px){.dom-grid{grid-template-columns:1fr}}
.sol-filters{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin:1rem 0}
.sol-filters button{border:1px solid #0077b6;background:#fff;color:#0077b6;border-radius:999px;padding:.45rem .9rem;font-weight:600;cursor:pointer;min-height:44px}
.sol-filters button[aria-pressed="true"]{background:#0077b6;color:#fff}
.sol-filters select{min-height:44px;border-radius:10px;padding:0 .6rem;font-size:1rem}
.sol-hub.sp-collapsed .grid>.sol-card:nth-child(n+7){display:none}
.sp-more{display:block;margin:1rem auto 0;min-height:44px;padding:.5rem 1.2rem;border-radius:999px;border:0;background:#003755;color:#fff;font-weight:600;cursor:pointer}
/* UX-OCT15:END */
"""
JS = r"""
/* UX-OCT15:START */
(function(){
  document.addEventListener('click',function(e){document.querySelectorAll('.nav-group details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});
  document.querySelectorAll('.nav-group details').forEach(function(d){var sm=d.querySelector('summary');d.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.open){d.removeAttribute('open');sm.focus()}});d.addEventListener('toggle',function(){if(sm)sm.setAttribute('aria-expanded',d.open?'true':'false');if(d.open)document.querySelectorAll('.nav-group details[open]').forEach(function(o){if(o!==d)o.removeAttribute('open')})})});
  var f=document.querySelector('.sol-filters');if(!f)return;
  var L=JSON.parse(f.getAttribute('data-i18n'));
  var hubs=[].slice.call(document.querySelectorAll('.sol-hub'));
  hubs.forEach(function(h){var n=h.querySelectorAll('.sol-card').length;if(n<=6)return;h.classList.add('sp-collapsed');
    var b=document.createElement('button');b.type='button';b.className='sp-more';b.textContent=L.more.replace('{n}',n);
    b.onclick=function(){var c=h.classList.toggle('sp-collapsed');b.textContent=c?L.more.replace('{n}',n):L.less};h.appendChild(b)});
  var dom='all',hub='all',sel=f.querySelector('select');
  function apply(){hubs.forEach(function(h){var ok=(dom==='all'||h.getAttribute('data-domain')===dom)&&(hub==='all'||h.id===hub);h.style.display=ok?'':'none'});
    f.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.value===dom)})}
  f.querySelectorAll('button').forEach(function(b){b.onclick=function(){dom=b.value;hub='all';sel.value='all';apply()}});
  sel.onchange=function(){hub=sel.value;dom='all';apply();if(hub!=='all'){var t=document.getElementById(hub);t&&t.scrollIntoView({behavior:'smooth'})}};
  var q=new URLSearchParams(location.search).get('domain');if(q){dom=q;}apply();
  var inp=document.querySelector('.sol-search-form input');if(inp)inp.addEventListener('input',function(){hubs.forEach(function(h){h.classList.remove('sp-collapsed');var b=h.querySelector('.sp-more');b&&b.remove()})});
})();
/* UX-OCT15:END */
"""
# Oct 15: Liquid Glass buttons (CSS below): Explore All Solutions, See Solutions on the World Map, nav Help/Donate
DROP = ''  # Oct 15: teardrop reverted (user asked for Liquid Glass styling instead)
STYLEV = '20261016zb'  # bump when styles.css changes
def bump_styles():
    for f in glob.glob('*.html') + glob.glob('*/*.html'):
        s = rd(f); s2 = re.sub(r'styles\.css\?v=[\w.-]+', 'styles.css?v=' + STYLEV, s)
        s2 = re.sub(r'(?<![\w-])site\.js\?v=[\w.-]+', 'site.js?v=' + STYLEV, s2)  # Oct 15: nav JS (aria-expanded) ships with the CSS
        if s2 != s: wr(f, s2)
# Oct 15: per-page glass tint. data-glass-tint on <body> = the page's domain colour (water/land/space, same as the homepage domain
# headings); everything else keeps the site navy. CSS reads it as --lg-tint.
def apply_tint(hubs):
    dom = {}
    for i, hs in enumerate(DOMAINS):
        for h in hs: dom[h] = ['water', 'land', 'space'][i]
    for h, v in hubs.items():
        for c in v['cards']:
            u = re.search(r'data-url="([^"#]+)', c)
            if u and h in dom: dom.setdefault(u.group(1), dom[h])
    n = 0
    for f in glob.glob('*.html') + glob.glob('*/*.html'):
        s = rd(f); m = re.search(r'<body\b[^>]*>', s)
        if not m: continue
        t = 'help' if os.path.basename(f) == 'Ways_to_Help.html' else dom.get(os.path.basename(f), 'site')
        b = re.sub(r' data-(?:glass-)?tint="(?:site|water|land|space|help)"', '', m.group(0)); b = b[:-1] + f' data-glass-tint="{t}">'
        if b != m.group(0): wr(f, s[:m.start()] + b + s[m.end():]); n += 1
    return n
def asset(path, txt):
    s = rd(path); s = re.sub(r'\n?/\* UX-OCT15:START \*/.*?/\* UX-OCT15:END \*/\n?', '', s, flags=re.S)
    wr(path, s.rstrip('\n') + '\n' + txt)

def solutions_filters(l, hubs):
    t = T[l]; p = d(l) + 'Solutions.html'; s = rd(p)
    dmap = {h: ['water', 'land', 'space'][i] for i, hs in enumerate(DOMAINS) for h in hs}
    for h, v in hubs.items():
        s = re.sub(r'<section ((?:[^>](?!data-domain))*?class="card-band sol-hub"[^>]*\bid="%s"[^>]*?)(?: data-domain="[^"]*")?>' % v['id'], lambda mm: '<section %s data-domain="%s">' % (re.sub(r' data-domain="[^"]*"', '', mm.group(1)), dmap.get(h, 'space')), s)
    i18n = html.escape(json.dumps({'more': t['more'], 'less': t['less']}, ensure_ascii=False))
    btns = f'<button type="button" value="all">{t["all"]}</button>' + ''.join(f'<button type="button" value="{k}">{dn}</button>' for k, (dn, _) in zip(['water','land','space'], t['dom']))
    opts = f'<option value="all">{t["allhubs"]}</option>' + ''.join(f'<option value="{v["id"]}">{v["name"]} ({len(v["cards"])})</option>' for v in hubs.values())
    fb = f'<div class="sol-filters" role="group" aria-label="{t["filt"]}" data-i18n="{i18n}">{btns}<label><span class="visually-hidden">{t["hub"]}</span><select aria-label="{t["hub"]}">{opts}</select></label></div>'
    s = block(s, 'SOL-FILTERS', fb, r'<div [^>]*sol-jump')
    return wr(p, s)

COUNT_RE = re.compile(r'\b1[0-9]{2}(?=(\+)? (real|soluciones|solutions|soluzioni|حل))')
def page_pass(p, l, n):
    s = rd(p); o = s
    page = os.path.basename(p)
    # nav
    m = re.search(r'(<ul class="nav-links">)(.*?)(</ul></div></nav>)', s, re.S)
    if m and 'lang-switch' in m.group(2):
        ls = re.search(r'<li[^>]*class="lang-switch".*?</li>', m.group(2), re.S).group(0)
        inner = nav_html(l, page) + ls + f'<li class="nav-help"><a href="Ways_to_Help.html">{DROP}{T[l]["help"]}</a></li>'
        s = s[:m.start()] + m.group(1) + inner + m.group(3) + s[m.end():]
    # Oct 15: translated pages inherit the English sticky button from i18n-build; always set this language's label.
    s = re.sub(r'(<a class="sticky-help" href="Ways_to_Help.html">)(?:<svg class="cta-drop".*?</svg>)?[^<]*(</a>)', lambda mm: mm.group(1) + DROP + T[l]["help"] + mm.group(2), s)
    if 'class="sticky-help"' not in s and '</main>' in s:
        s = s.replace('</main>', f'</main><a class="sticky-help" href="Ways_to_Help.html">{DROP}{T[l]["help"]}</a>', 1)
    # lazy images below the hero
    def lazy(mm):
        tag = mm.group(0)
        return tag if 'loading=' in tag else tag.replace('<img', '<img loading="lazy"', 1)
    parts = s.split('</section>', 1)
    if len(parts) == 2: s = parts[0] + '</section>' + re.sub(r'<img\b[^>]*>', lazy, parts[1])
    # auto counts in visible text (not inside dates)
    s = re.sub(r'(?<![\d,.])1[0-9]{2}(?=\+? (real|sourced|soluciones|solutions|soluzioni|حل|حلًا))', str(n), s)
    s = re.sub(r'(?<![\d,.])1[0-9]{2}(?=\+? (حلول|حلا))', str(n), s)
    # canonical/og for index pages
    if page == 'index.html':
        s = s.replace(f'{SITE}{d(l)}index.html"', f'{SITE}{d(l)}"')
    s = re.sub(r'(href="%s(?:(?:fr|es|ar|it)/)?)index\.html"' % re.escape(SITE), r'\1"', s)
    if page == 'About.html':
        def about_vid(m):
            tag = m.group(0)
            tag = re.sub(r'\bpreload="[^"]*"', 'preload="none"', tag)
            if 'preload=' not in tag: tag = tag.replace('<video', '<video preload="none"', 1)
            srcs = re.findall(r'<source[^>]*>', tag)
            if len(srcs) >= 2:
                full = next((x for x in srcs if 'about-v3' in x and '720' not in x), None)
                small = next((x for x in srcs if '720' in x), None)
                if full and small and tag.find(small) > tag.find(full):
                    tag = tag.replace(full, '@@FULL@@', 1).replace(small, full, 1).replace('@@FULL@@', small, 1)
            return tag
        s = re.sub(r'<video\b[^>]*>.*?</video>', about_vid, s, count=1, flags=re.S)
    if page == 'Mission_Blue_Hope_Spots.html' and l in ('fr', 'es'):
        tt = {'fr': "Hope Spots de Mission Blue : protéger l'océan | Saving Planets", 'es': 'Hope Spots de Mission Blue: proteger el océano | Saving Planets'}[l]
        s = re.sub(r'<title>[^<]*</title>', f'<title>{html.escape(tt, quote=False)}</title>', s, count=1)
    return wr(p, s)

def sitemap():
    s = rd('sitemap.xml'); o = s
    s = re.sub(r'\s*<url><loc>[^<]*404\.html</loc>.*?</url>', '', s, flags=re.S)
    s = re.sub(r'(%s(?:(?:fr|es|ar|it)/)?)index\.html' % re.escape(SITE), r'\1', s)
    wr('sitemap.xml', s)

if __name__ == '__main__':
    n = count_solutions(); ch = 0
    hubs_by = {l: sol_cards(l) for l in LANGS}
    for l in LANGS:
        for p in sorted(glob.glob(d(l) + '*.html')): ch += page_pass(p, l, n)
        ch += home(l, n, hubs_by[l]); ch += solutions_filters(l, hubs_by[l])
    asset('styles.css', CSS); asset('site.js', JS); sitemap(); bump_styles(); ch += apply_tint(hubs_by['en'])
    print(f'build-ux: {n} solutions, {ch} page writes')
