#!/usr/bin/env python3
"""Build Voyages.html in six languages from each language's Space.html shell.

The page name lives only in TITLE. Change it here if the name changes.
"""
import html, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
V = '20261113z'

# Change the page name here. Bryan may still pick a different one.
TITLE = {
 'en': ('Voyages Beyond Earth', 'Live journeys to neighboring planets, moons and asteroids'),
 'fr': ('Voyages au-delà de la Terre', 'Voyages en direct vers les planètes, les lunes et les astéroïdes voisins'),
 'es': ('Viajes más allá de la Tierra', 'Viajes en vivo hacia planetas, lunas y asteroides vecinos'),
 'ar': ('رحلات ما وراء الأرض', 'رحلات مباشرة إلى الكواكب والأقمار والكويكبات المجاورة'),
 'it': ('Viaggi oltre la Terra', 'Viaggi dal vivo verso pianeti, lune e asteroidi vicini'),
 'he': ('מסעות מעבר לכדור הארץ', 'מסעות חיים אל כוכבי לכת, ירחים ואסטרואידים שכנים'),
}
UI = {
 'en': dict(earth='Earth', asOf='Ranges as of', sourceName='NASA/JPL Horizons', fromEarth='Distance from Earth:',
            millionKm='million km', more='Click here for more information',
            noRange='Horizons did not return a range for this mission, so no distance is shown.',
            videoCredit='Title video: the site space loop. Created by the Founder and SI.'),
 'fr': dict(earth='Terre', asOf='Distances au', sourceName='NASA/JPL Horizons', fromEarth='Distance depuis la Terre :',
            millionKm='millions de km', more='Cliquez ici pour en savoir plus',
            noRange='Horizons n’a pas renvoyé de distance pour cette mission, donc aucune distance n’est affichée.',
            videoCredit='Vidéo de titre : la boucle spatiale du site. Créé par le fondateur et SI.'),
 'es': dict(earth='Tierra', asOf='Distancias al', sourceName='NASA/JPL Horizons', fromEarth='Distancia desde la Tierra:',
            millionKm='millones de km', more='Haga clic aquí para más información',
            noRange='Horizons no devolvió una distancia para esta misión, así que no se muestra ninguna.',
            videoCredit='Vídeo del título: el bucle espacial del sitio. Creado por el fundador y SI.'),
 'ar': dict(earth='الأرض', asOf='المسافات في', sourceName='NASA/JPL Horizons', fromEarth='المسافة من الأرض:',
            millionKm='مليون كم', more='انقر هنا لمزيد من المعلومات',
            noRange='لم يُرجع Horizons مسافة لهذه المهمة، لذلك لا تُعرض أي مسافة.',
            videoCredit='فيديو العنوان: حلقة الفضاء في الموقع. من إعداد المؤسس وSI.'),
 'it': dict(earth='Terra', asOf='Distanze al', sourceName='NASA/JPL Horizons', fromEarth='Distanza dalla Terra:',
            millionKm='milioni di km', more='Fai clic qui per maggiori informazioni',
            noRange='Horizons non ha restituito una distanza per questa missione, quindi non ne viene mostrata nessuna.',
            videoCredit='Video del titolo: il ciclo spaziale del sito. Creato dal fondatore e da SI.'),
 'he': dict(earth='כדור הארץ', asOf='טווחים נכון ל-', sourceName='NASA/JPL Horizons', fromEarth='מרחק מכדור הארץ:',
            millionKm='מיליון ק״מ', more='לחצו כאן למידע נוסף',
            noRange='Horizons לא החזיר טווח למשימה הזו, ולכן לא מוצג מרחק.',
            videoCredit='סרטון הכותרת: לולאת החלל של האתר. נוצר על ידי המייסד ו-SI.'),
}

# Facts below were read from the official mission pages on 13 Nov 2026, plus the Horizons body list.
# mode: cruise (still traveling), there (already at the body), out (no single arrival).
def M(i, **k):
    k['id'] = i
    return k

MISSIONS = [
 M('europa-clipper', mode='cruise', craft='assets/earth/cut/europa-craft.webp', dest='assets/earth/cut/europa.webp',
   companion='assets/earth/cut/jupiter.webp', official='https://science.nasa.gov/mission/europa-clipper/'),
 M('juice', mode='cruise', dest='assets/earth/cut/ganymede.webp', official='https://www.esa.int/Science_Exploration/Space_Science/Juice'),
 M('juno', mode='there', globe='assets/earth/jupiter-cassini-map.jpg', craft='assets/earth/cut/juno.webp',
   official='https://science.nasa.gov/mission/juno/'),
 M('psyche', mode='cruise', dest='assets/earth/cut/psyche.webp', official='https://science.nasa.gov/mission/psyche/'),
 M('lucy', mode='out', craft='assets/earth/cut/lucy.webp', official='https://science.nasa.gov/mission/lucy/'),
 M('bepicolombo', mode='cruise', dest='assets/earth/cut/mercury.webp', official='https://www.esa.int/Science_Exploration/Space_Science/BepiColombo'),
 M('hera', mode='there', dest='assets/earth/cut/hera.webp', official='https://www.esa.int/Space_Safety/Hera'),
 M('parker-solar-probe', mode='out', dest='assets/earth/cut/sun.webp', official='https://science.nasa.gov/mission/parker-solar-probe/'),
 M('solar-orbiter', mode='out', dest='assets/earth/cut/sun.webp', craft='assets/earth/cut/solar-orbiter.webp',
   official='https://www.esa.int/Science_Exploration/Space_Science/Solar_Orbiter'),
 M('new-horizons', mode='out', official='https://science.nasa.gov/mission/new-horizons/'),
 M('voyager-1', mode='out', official='https://science.nasa.gov/mission/voyager/voyager-1/'),
 M('voyager-2', mode='out', official='https://science.nasa.gov/mission/voyager/voyager-2/'),
]

# Per-language display copy. Keys match mission ids.
COPY = json.load(open('scripts/voyage-copy.json', encoding='utf-8'))


def main_html(lang, ui, title, subtitle):
    pre = '' if lang == 'en' else '../'
    live = []
    for m in MISSIONS:
        c = COPY[m['id']][lang]
        item = dict(m)
        item.update(c)
        live.append(item)
    payload = dict(ui, locale=lang, live=live)
    poster = pre + 'assets/videos/hero-loop.jpg'
    video = 'https://media.savingplanets.com/videos/hero-loop.97191e628115.mp4'
    return f'''<main id="main">
<section class="voy-hero">
<img class="voy-still" src="{poster}" alt="" width="1280" height="546">
<video muted loop playsinline preload="none" poster="{poster}" width="1280" height="546"><source data-src="{video}" type="video/mp4"></video>
<div class="voy-shade" aria-hidden="true"></div>
<div class="page-hero-content"><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>
<p class="hero-video-credit">{html.escape(ui["videoCredit"])}</p>
</section>
<script>(function(){{var v=document.querySelector(".voy-hero video");if(!v)return;var mq=window.matchMedia("(prefers-reduced-motion: reduce)");if(mq.matches)return;var s=v.querySelector("source");if(s&&s.getAttribute("data-src"))s.src=s.getAttribute("data-src");v.load();v.play&&v.play().catch(function(){{}});}})();</script>
<div class="voy-wrap" id="voy-app" data-pre="{pre}" data-src="{pre}data/voyages.json">
<div class="voy-switch" id="voy-switch" role="group" aria-label="{html.escape(title)}"></div>
<div id="voy-scene" aria-live="polite"></div>
</div>
<script type="application/json" id="voy-i18n">{json.dumps(payload, ensure_ascii=False)}</script>
</main>
'''


def build(lang):
    src = 'Space.html' if lang == 'en' else f'{lang}/Space.html'
    t = open(src, encoding='utf-8').read()
    for code in LANGS:
        old = 'https://www.savingplanets.com/' + ('' if code == 'en' else code + '/') + 'Space.html'
        new = 'https://www.savingplanets.com/' + ('' if code == 'en' else code + '/') + 'Voyages.html'
        t = t.replace(old, new)
    title, subtitle = TITLE[lang]
    desc = title + '. ' + subtitle
    t = re.sub(r'<title>[^<]*</title>', f'<title>{html.escape(title)} | Saving Planets</title>', t, count=1)
    t = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + html.escape(desc, quote=True) + '"', t, count=1)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + html.escape(title + ' | Saving Planets', quote=True) + '"', t, count=1)
    t = re.sub(r'(<meta name="twitter:title" content=")[^"]*"', lambda m: m.group(1) + html.escape(title + ' | Saving Planets', quote=True) + '"', t, count=1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + html.escape(desc, quote=True) + '"', t, count=1)
    t = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', lambda m: m.group(1) + html.escape(title, quote=True) + '"', t, count=1)
    i, j = t.find('<main'), t.find('<footer')
    if i < 0 or j < 0:
        raise SystemExit('shell missing main/footer ' + src)
    pre = '' if lang == 'en' else '../'
    links = f'<link rel="stylesheet" href="{pre}voyages.css?v={V}">\n<script src="{pre}assets/voyages.js?v={V}" defer></script>\n'
    if 'voyages.css' not in t:
        t = t.replace('</body>', links + '</body>', 1)
    open('Voyages.html' if lang == 'en' else f'{lang}/Voyages.html', 'w', encoding='utf-8').write(t[:i] + main_html(lang, UI[lang], title, subtitle) + '\n' + t[j:])
    print(lang)


if __name__ == '__main__':
    for lang in LANGS:
        build(lang)
