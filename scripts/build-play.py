#!/usr/bin/env python3
"""Oct 15 item 9: Kids "Play & Learn" hub (Play_and_Learn.html, en/fr/es/ar/it): big touch tiles for the games and kid tools
(Kids Planet Map, Spot the Fire, Satellite Explorer, Amazing Facts, Myth vs Fact, Glossary) with progress badges.
Progress is kept only in this browser (localStorage 'sp-play-v1'); a PLAY block in site.js records a visit when a tile's page is opened.
Also points the homepage "Kids" Start Here card at the hub. Nav link lives in build-ux.py GROUPS. Run after build-spotfire.py. Idempotent."""
import re, os, json, html, datetime, importlib.util
spec = importlib.util.spec_from_file_location('sf', 'scripts/build-spotfire.py'); sf = importlib.util.module_from_spec(spec); spec.loader.exec_module(sf)
SITE, LANGS, d, rd, wr, esc = sf.SITE, sf.LANGS, sf.d, sf.rd, sf.wr, sf.esc
PAGE = 'Play_and_Learn.html'
TILES = [('Kids_Map.html', '🗺️'), ('Spot_the_Fire.html', '🔥'), ('Satellite_Explorer.html', '🛰️'), ('Amazing_Facts.html', '🤩'), ('Myth_vs_Fact.html', '🕵️'), ('Glossary.html', '📖')]
T = {
 'en': dict(title='Play & Learn', nav='Play & Learn', kicker='Games, maps and facts about our planet. Tap a tile to start.',
   desc='Kids games and activities about our planet: Kids Planet Map, Spot the Fire from Space, Satellite Explorer, Amazing Facts, Myth vs Fact and the Glossary.',
   tiles=[('Kids Planet Map', 'Tap a bubble, get a wow fact.'), ('Spot the Fire', 'How big is a pixel? Find the fire from space.'),
          ('Satellite Explorer', 'Drag the parts, build a satellite.'), ('Amazing Facts', 'Real facts that will surprise you.'),
          ('Myth vs Fact', 'Bust scary myths with real evidence.'), ('Glossary', 'Big words, made simple.')],
   done='Explored', todo='Not yet', prog='You have explored {n} of {t}.', levels=['Start exploring!', 'Explorer badge', 'Ranger badge', 'Planet Hero badge'],
   note='Your badges are saved only on this device. Nothing is sent to us.', reset='Start over', kids='Games, maps and amazing facts.'),
 'fr': dict(title='Jouer et apprendre', nav='Jouer et apprendre', kicker='Des jeux, des cartes et des faits sur notre planète. Touche une tuile pour commencer.',
   desc='Jeux et activités pour enfants sur notre planète : carte de la planète, Repère le feu depuis l’espace, Explorateur de satellites, Faits étonnants, Mythe ou réalité et Glossaire.',
   tiles=[('Carte de la planète', 'Touche une bulle, découvre un fait étonnant.'), ('Repère le feu', 'Quelle taille fait un pixel ? Trouve le feu depuis l’espace.'),
          ('Explorateur de satellites', 'Fais glisser les pièces, construis un satellite.'), ('Faits étonnants', 'Des faits réels qui vont te surprendre.'),
          ('Mythe ou réalité', 'Démonte les mythes effrayants avec des preuves.'), ('Glossaire', 'Les mots difficiles, expliqués simplement.')],
   done='Exploré', todo='Pas encore', prog='Tu as exploré {n} sur {t}.', levels=['Commence l’exploration !', 'Badge Explorateur', 'Badge Ranger', 'Badge Héros de la planète'],
   note='Tes badges sont enregistrés seulement sur cet appareil. Rien ne nous est envoyé.', reset='Recommencer', kids='Jeux, cartes et faits étonnants.'),
 'es': dict(title='Juega y aprende', nav='Juega y aprende', kicker='Juegos, mapas y datos sobre nuestro planeta. Toca una tarjeta para empezar.',
   desc='Juegos y actividades para niños sobre nuestro planeta: Mapa del Planeta, Encuentra el fuego desde el espacio, Explorador de satélites, Datos asombrosos, Mito o realidad y Glosario.',
   tiles=[('Mapa del Planeta', 'Toca una burbuja y descubre un dato asombroso.'), ('Encuentra el fuego', '¿Qué tamaño tiene un píxel? Encuentra el fuego desde el espacio.'),
          ('Explorador de satélites', 'Arrastra las piezas y construye un satélite.'), ('Datos asombrosos', 'Datos reales que te sorprenderán.'),
          ('Mito o realidad', 'Desmonta mitos que dan miedo con pruebas reales.'), ('Glosario', 'Palabras difíciles, explicadas fácil.')],
   done='Explorado', todo='Todavía no', prog='Has explorado {n} de {t}.', levels=['¡Empieza a explorar!', 'Insignia de Explorador', 'Insignia de Guardabosques', 'Insignia de Héroe del Planeta'],
   note='Tus insignias se guardan solo en este dispositivo. No se nos envía nada.', reset='Empezar de nuevo', kids='Juegos, mapas y datos asombrosos.'),
 'ar': dict(title='العب وتعلّم', nav='العب وتعلّم', kicker='ألعاب وخرائط وحقائق عن كوكبنا. المس بطاقة للبدء.',
   desc='ألعاب وأنشطة للأطفال عن كوكبنا: خريطة الكوكب، اكتشف الحريق من الفضاء، مستكشف الأقمار الصناعية، حقائق مذهلة، خرافة أم حقيقة، والمسرد.',
   tiles=[('خريطة الكوكب', 'المس فقاعة واكتشف حقيقة مدهشة.'), ('اكتشف الحريق', 'ما حجم البكسل؟ اعثر على الحريق من الفضاء.'),
          ('مستكشف الأقمار الصناعية', 'اسحب القطع وابنِ قمرًا صناعيًا.'), ('حقائق مذهلة', 'حقائق حقيقية ستدهشك.'),
          ('خرافة أم حقيقة', 'افضح الخرافات المخيفة بالأدلة.'), ('المسرد', 'كلمات صعبة بشرح بسيط.')],
   done='تم الاستكشاف', todo='ليس بعد', prog='استكشفت {n} من {t}.', levels=['ابدأ الاستكشاف!', 'شارة المستكشف', 'شارة الحارس', 'شارة بطل الكوكب'],
   note='تُحفظ شاراتك على هذا الجهاز فقط. لا يُرسل إلينا أي شيء.', reset='ابدأ من جديد', kids='ألعاب وخرائط وحقائق مذهلة.'),
 'it': dict(title='Gioca e impara', nav='Gioca e impara', kicker='Giochi, mappe e fatti sul nostro pianeta. Tocca una tessera per iniziare.',
   desc='Giochi e attività per bambini sul nostro pianeta: Mappa del pianeta, Trova l’incendio dallo spazio, Esploratore di satelliti, Fatti incredibili, Mito o realtà e Glossario.',
   tiles=[('Mappa del pianeta', 'Tocca una bolla, scopri un fatto incredibile.'), ('Trova l’incendio', 'Quanto è grande un pixel? Trova l’incendio dallo spazio.'),
          ('Esploratore di satelliti', 'Trascina i pezzi, costruisci un satellite.'), ('Fatti incredibili', 'Fatti veri che ti sorprenderanno.'),
          ('Mito o realtà', 'Smonta i miti che fanno paura con prove vere.'), ('Glossario', 'Parole difficili, spiegate in modo semplice.')],
   done='Esplorato', todo='Non ancora', prog='Hai esplorato {n} su {t}.', levels=['Inizia a esplorare!', 'Distintivo Esploratore', 'Distintivo Ranger', 'Distintivo Eroe del pianeta'],
   note='I tuoi distintivi sono salvati solo su questo dispositivo. Non ci viene inviato nulla.', reset='Ricomincia', kids='Giochi, mappe e fatti incredibili.')}
CSS = ('.pl-wrap{max-width:1100px;margin:0 auto;padding:1rem 1.25rem 2rem}.pl-prog{display:flex;flex-wrap:wrap;align-items:center;gap:.6rem 1rem;margin:.5rem 0 1.2rem}'
       '.pl-level{display:inline-flex;align-items:center;gap:.4rem;font-weight:800;padding:.45rem .9rem;border-radius:999px;background:var(--lg-solid,#4a3aa8);color:#fff}'
       '.pl-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:1.1rem;list-style:none;padding:0;margin:0}'
       '.pl-tile{display:flex;flex-direction:column;gap:.45rem;min-height:190px;padding:1.3rem 1.2rem;border-radius:22px;text-decoration:none;color:#fff !important;'
       'background:var(--lg-solid,#4a3aa8);border:2px solid rgba(255,255,255,.25);box-shadow:0 6px 18px rgba(0,0,0,.25);transition:transform .15s}'
       '.pl-tile:hover,.pl-tile:focus-visible{transform:translateY(-3px);outline:3px solid #ffd54a;outline-offset:3px}'
       '.pl-emoji{font-size:3rem;line-height:1}.pl-name{font-size:1.45rem;font-weight:800}.pl-text{font-size:1.02rem;line-height:1.4;opacity:.95}'
       '.pl-badge{margin-top:auto;align-self:flex-start;font-size:.9rem;font-weight:700;padding:.25rem .7rem;border-radius:999px;background:rgba(0,0,0,.28)}'
       '.pl-tile.is-done .pl-badge{background:#ffd54a;color:#1a1300}.pl-note{font-size:.88rem;opacity:.85}.pl-reset{min-height:44px;border-radius:999px;padding:.4rem 1rem;font:inherit;cursor:pointer}'
       '@media (prefers-reduced-motion:reduce){.pl-tile{transition:none}.pl-tile:hover{transform:none}}')
JS = """/* PLAY:START */
(function(){var K='sp-play-v1',P=['Kids_Map','Spot_the_Fire','Satellite_Explorer','Amazing_Facts','Myth_vs_Fact','Glossary'];
function get(){try{return JSON.parse(localStorage.getItem(K))||{}}catch(e){return {}}}
function put(o){try{localStorage.setItem(K,JSON.stringify(o))}catch(e){}}
var pg=(location.pathname.split('/').pop()||'').replace(/\\.html$/,'');if(P.indexOf(pg)>-1){var o=get();if(!o[pg]){o[pg]=Date.now();put(o)}}
function draw(){var g=document.querySelector('.pl-grid');if(!g)return;var o=get(),n=0,w=document.querySelector('.pl-wrap'),L=JSON.parse(w.dataset.levels);
[].forEach.call(g.querySelectorAll('.pl-tile'),function(a){var on=!!o[a.dataset.page];if(on)n++;a.classList.toggle('is-done',on);a.querySelector('.pl-badge').textContent=on?'⭐ '+w.dataset.done:w.dataset.todo});
var t=P.length,lv=n>=t?3:n>=3?2:n>=1?1:0;w.querySelector('.pl-count').textContent=w.dataset.prog.replace('{n}',n).replace('{t}',t);w.querySelector('.pl-level').textContent=(lv?'🏅 ':'🚀 ')+L[lv]}
document.addEventListener('DOMContentLoaded',function(){draw();var r=document.querySelector('.pl-reset');if(r)r.addEventListener('click',function(){put({});draw()})});
window.addEventListener('pageshow',draw)})();
/* PLAY:END */
"""
def page_html(l):
    t = T[l]; shell = rd(d(l) + 'Kids_Map.html')
    head = shell[:shell.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(t["title"])} | Saving Planets</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + esc(t['desc']) + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + esc(t['title']) + ' | Saving Planets"', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'\n?<link rel="alternate" hreflang="[^"]+" href="[^"]+">', '', head)
    head = head.replace('Kids_Map.html', PAGE).replace('assets/og/' + l + '/Kids_Map.jpg', 'assets/og/' + l + '/Play_and_Learn.jpg')
    alts = ''.join(f'\n<link rel="alternate" hreflang="{x}" href="{SITE}{d(x)}{PAGE}">' for x in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{PAGE}">'
    head = re.sub(r'(<link rel="canonical"[^>]*>)', lambda m: m.group(1) + alts, head, count=1)
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": t['title'], "description": t['desc'], "url": f"{SITE}{d(l)}{PAGE}", "inLanguage": l,
          "audience": {"@type": "EducationalAudience", "educationalRole": "student"}, "isAccessibleForFree": True,
          "hasPart": [{"@type": "WebPage", "name": n, "url": f"{SITE}{d(l)}{p}"} for (p, _), (n, _x) in zip(TILES, t['tiles'])]}
    head += f'<style>{CSS}</style>\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
    body_open = re.sub(r'class="[^"]*"', 'class="toc-sub play-page"', re.search(r'<body[^>]*>', shell).group(0), count=1)
    body_open = re.sub(r' data-glass-tint="[^"]*"', '', body_open)[:-1] + ' data-glass-tint="space">'
    nav = re.search(r'<a class="skip-link".*?</nav>', shell, re.S).group(0)
    nav = re.sub(r'(<li class="lang-switch".*?</li>)', lambda m: m.group(1).replace('Kids_Map.html', PAGE), nav, flags=re.S)
    foot = shell[shell.index('</main>'):]
    foot = re.sub(r'<script src="(?:\.\./)?(?:edu|edu-extras)\.js[^"]*"[^>]*></script>', '', foot)
    foot = re.sub(r'<!-- GEN [0-9a-f]+ -->', '', foot)
    tiles = ''.join(f'<li><a class="pl-tile" data-page="{p[:-5]}" href="{sf.href(l, p)}"><span class="pl-emoji" aria-hidden="true">{e}</span>'
                    f'<span class="pl-name">{esc(n)}</span><span class="pl-text">{esc(x)}</span><span class="pl-badge">{esc(t["todo"])}</span></a></li>'
                    for (p, e), (n, x) in zip(TILES, t['tiles']))
    main = (f'<main id="main">\n<section class="page-hero hero-kids"><div class="page-hero-content"><h1>{esc(t["title"])}</h1><p>{esc(t["kicker"])}</p></div></section>\n'
            f'<div class="pl-wrap" data-done="{esc(t["done"])}" data-todo="{esc(t["todo"])}" data-prog="{esc(t["prog"])}" data-levels="{esc(json.dumps(t["levels"], ensure_ascii=False))}">'
            f'<div class="pl-prog" role="status" aria-live="polite"><span class="pl-level">🚀 {esc(t["levels"][0])}</span><span class="pl-count">{esc(t["prog"].replace("{n}", "0").replace("{t}", str(len(TILES))))}</span>'
            f'<button type="button" class="pl-reset">{esc(t["reset"])}</button></div>\n<ul class="pl-grid">{tiles}</ul>\n<p class="pl-note">{esc(t["note"])}</p></div>\n')
    return head + '</head>\n' + body_open + nav + main + foot
def home(l):
    p = d(l) + 'index.html'; s = rd(p)
    rx = r'(<a class="aud-card" href=")(?:(?:\.\./)?Amazing_Facts\.html|' + re.escape(PAGE) + r')(">\s*<span [^>]*>🧒</span>\s*<span class="aud-title">[^<]*</span>\s*<span class="aud-text">)[^<]*(</span>)'
    return wr(p, re.sub(rx, lambda m: m.group(1) + PAGE + m.group(2) + esc(T[l]['kids']) + m.group(3), s))
def sitejs():
    s = rd('site.js'); s2 = re.sub(r'\n?/\* PLAY:START \*/.*?/\* PLAY:END \*/\n?', '', s, flags=re.S).rstrip('\n') + '\n' + JS
    return wr('site.js', s2)
if __name__ == '__main__':
    ch = sitejs()
    for l in LANGS: ch += wr(d(l) + PAGE, page_html(l)); ch += home(l)
    s = rd('sitemap.xml'); today = datetime.date.today().isoformat()
    for l in LANGS:
        loc = f'{SITE}{d(l)}{PAGE}'
        if f'<loc>{loc}</loc>' not in s: s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
    ch += wr('sitemap.xml', s)
    print(f'build-play: writes={ch}')
