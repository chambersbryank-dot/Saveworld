#!/usr/bin/env python3
"""Oct 18 2026 (owner): Artemis_II.html is now titled with NASA's name for the whole effort, 'Artemis Program'
(fr Programme Artemis, es Programa Artemis, it Programma Artemis, ar برنامج أرتيميس, he תוכנית ארטמיס).
URL/filename unchanged, so no link breaks; the Artemis II mission content stays on the page as a section.
Idempotent EN-source pass before i18n-build: page <title>/og/twitter titles, H1, banner line, meta descriptions;
every card/link label site-wide that points at Artemis_II.html ('Artemis II (NASA / CSA)', 'Artemis II', 'Artemis II: The
Farthest Humans Have Gone'); i18n strings. Banner: Lesson Builder standard size (site-wide hero rule) + slow Ken Burns with a
pause button, still under reduced motion. Facts in the new copy are all on the page: Artemis I Nov-Dec 2022; Artemis II
April 2026, 252,756 miles; Artemis III NASA target 2027."""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
LANGS = ('fr', 'es', 'ar', 'it', 'he')
NAME = ('Artemis Program', 'Programme Artemis', 'Programa Artemis', 'برنامج أرتيميس', 'Programma Artemis', 'תוכנית ארטמיס')
NAME_AG = tuple(n + (' (ناسا)' if i == 3 else ' (NASA)') for i, n in enumerate(NAME))
TITLE = ("Artemis Program: NASA's Return to the Moon", "Programme Artemis : le retour de la NASA sur la Lune",
         "Programa Artemis: el regreso de la NASA a la Luna", "برنامج أرتيميس: عودة ناسا إلى القمر",
         "Programma Artemis: il ritorno della NASA sulla Luna", "תוכנית ארטמיס: החזרה של NASA לירח")
SUB = ("From the first uncrewed test flight in 2022 to Artemis II, the farthest humans have traveled, and the Moon missions still to come.",
       "Du premier vol d'essai sans équipage en 2022 à Artemis II, le plus loin où des humains sont allés, et les missions lunaires à venir.",
       "Desde el primer vuelo de prueba sin tripulación en 2022 hasta Artemis II, lo más lejos que han viajado los humanos, y las misiones lunares que vienen.",
       "من أول رحلة تجريبية دون طاقم عام 2022 إلى Artemis II، أبعد ما وصل إليه البشر، والبعثات القمرية القادمة.",
       "Dal primo volo di prova senza equipaggio nel 2022 ad Artemis II, il punto più lontano mai raggiunto dagli esseri umani, fino alle missioni lunari in arrivo.",
       "מטיסת הניסוי הראשונה ללא צוות ב-2022 ועד Artemis II, הרחוק ביותר שבני אדם הגיעו אליו, והמשימות לירח שעוד יבואו.")
DESC = ("NASA's Artemis program: Artemis I flew in 2022, Artemis II carried four astronauts 252,756 miles from Earth in April 2026, and Artemis III is targeted for 2027.",
        "Le programme Artemis de la NASA : Artemis I a volé en 2022, Artemis II a emmené quatre astronautes à 252 756 miles de la Terre en avril 2026, et Artemis III est prévue pour 2027.",
        "El programa Artemis de la NASA: Artemis I voló en 2022, Artemis II llevó a cuatro astronautas a 252.756 millas de la Tierra en abril de 2026 y Artemis III está prevista para 2027.",
        "برنامج أرتيميس التابع لناسا: حلّقت Artemis I عام 2022، وحملت Artemis II أربعة رواد فضاء إلى مسافة 252,756 ميلًا من الأرض في أبريل 2026، ومن المقرر إطلاق Artemis III عام 2027.",
        "Il programma Artemis della NASA: Artemis I ha volato nel 2022, Artemis II ha portato quattro astronauti a 252.756 miglia dalla Terra nell'aprile 2026 e Artemis III è prevista per il 2027.",
        "תוכנית ארטמיס של NASA: Artemis I טסה ב-2022, Artemis II לקחה ארבעה אסטרונאוטים למרחק 252,756 מייל מכדור הארץ באפריל 2026, ו-Artemis III מתוכננת ל-2027.")
OLD_AG, OLD_TITLE = 'Artemis II (NASA / CSA)', 'Artemis II: The Farthest Humans Have Gone'
BRAND = ' | Saving Planets'
esc = lambda x: x.replace('&', '&amp;').replace('"', '&quot;')
# --- the page itself
P = 'Artemis_II.html'; s = open(P, encoding='utf-8').read(); s0 = s
s = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE[0]}{BRAND}</title>'.replace("'", '&#x27;').replace('&#x27;', "'"), s, count=1)
for attr in ('property="og:title"', 'name="twitter:title"'):
    s = re.sub(r'(<meta ' + attr + r' content=")[^"]*', lambda m: m.group(1) + esc(TITLE[0] + BRAND), s)
for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
    s = re.sub(r'(<meta ' + attr + r' content=")[^"]*', lambda m: m.group(1) + esc(DESC[0]), s)
s = re.sub(r'(<section class="page-hero space-hero"><div class="page-hero-content"><h1>)[^<]*(</h1><p>)[^<]*(</p>)',
           lambda m: m.group(1) + NAME[0] + m.group(2) + SUB[0] + m.group(3), s, count=1)
# Oct 18 (owner: 'an animated rocket slowly launching up'): the banner is NASA's own Artemis II launch footage
# (images.nasa.gov KSC-04012026-C4829, 'Artemis II Launch from OSB II Balcony - Slo Mo', 3840x2160 59.94 fps, public domain).
# Cut 41-56.5 s, played at 0.5x (every native frame, no interpolation), a gentle tilt that follows the rocket, 2 s crossfade loop.
# Three crops for the banner shapes (wide 4:1, iPad-portrait 2.13:1, phone 1.35:1); the original 4K segment is the master on R2.
# The poster is a full-quality 4K frame from the same footage (CSS background, also what reduced-motion users see).
_mv = json.load(open('assets/data/media-manifest.json', encoding='utf-8'))
_V = {k: _mv['videos/artemis-launch-' + f + '.mp4']['url'] for k, f in
      [('w3840', 'wide-3840'), ('w2560', 'wide-2560'), ('w1920', 'wide-1920'), ('med', 'med-1920'), ('phone', 'phone-1280')]}
CREDIT_TXT = 'Video: NASA, Artemis II launch, April 1, 2026'
CREDIT = f'<span class="hero-credit">{CREDIT_TXT}</span>'
BTN = (CREDIT + '<button type="button" class="pr-motion-toggle" aria-pressed="false" aria-label="Pause banner animation">&#10074;&#10074;</button>'
       '<script>(function(){var b=document.querySelector(\'.pr-motion-toggle\'),h=b&&b.closest(\'.page-hero\');if(!h)return;'
       'var V=' + json.dumps(_V, separators=(',', ':')) + ',v=null,mq=window.matchMedia&&matchMedia(\'(prefers-reduced-motion: reduce)\');'
       'function st(p){b.setAttribute(\'aria-pressed\',p);b.innerHTML=p?\'&#9654;\':\'&#10074;&#10074;\';h.classList.toggle(\'pr-paused\',p);}'
       'function pick(){var w=window.innerWidth,d=window.devicePixelRatio||1;if(w<=600)return V.phone;if(w<=900)return V.med;w*=d;return w>2600?V.w3840:w>1920?V.w2560:V.w1920;}'
       'function go(){if((mq&&mq.matches)||(navigator.connection&&navigator.connection.saveData))return;'
       'v=document.createElement(\'video\');v.muted=true;v.defaultMuted=true;v.setAttribute(\'muted\',\'\');v.setAttribute(\'playsinline\',\'\');'
       'v.setAttribute(\'autoplay\',\'\');v.setAttribute(\'loop\',\'\');v.setAttribute(\'aria-hidden\',\'true\');v.setAttribute(\'tabindex\',\'-1\');'
       'v.setAttribute(\'disablepictureinpicture\',\'\');v.preload=\'auto\';v.className=\'art-hero-video\';v.src=pick();'
       'v.addEventListener(\'playing\',function(){h.classList.add(\'art-video-on\');});h.insertBefore(v,h.firstChild);'
       'if(h.classList.contains(\'pr-paused\'))return;var r=v.play();if(r&&r.catch)r.catch(function(){st(true);});}'
       'b.addEventListener(\'click\',function(){var p=b.getAttribute(\'aria-pressed\')!==\'true\';st(p);if(v){if(p)v.pause();else v.play();}});'
       'if(document.readyState===\'complete\')go();else window.addEventListener(\'load\',go);})();</script>')
s = re.sub(r'<span class="hero-credit">[^<]*</span>(?=<button type="button" class="pr-motion-toggle")', '', s)
s = re.sub(r'(</section>)\s*<p class="photo-credit">Image: NASA, Artemis II launch\.</p>', r'\1', s, count=1)  # superseded by the hero credit
s = re.sub(r'<button type="button" class="pr-motion-toggle".*?</script>', '', s, flags=re.S)
s = re.sub(r'(<section class="page-hero space-hero">.*?)(</section>)', lambda m: m.group(1) + BTN + m.group(2), s, count=1, flags=re.S)
if s != s0: open(P, 'w', encoding='utf-8').write(s)
# Italian SEO override pointed at the old Artemis II-only description
sm = json.load(open('i18n/seo-meta.json', encoding='utf-8'))
if sm.get(P, {}).get('it', {}).get('description') not in (None, DESC[4]):
    sm[P]['it']['description'] = DESC[4]; json.dump(sm, open('i18n/seo-meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# --- labels site-wide (English sources; translations follow through i18n-build)
LBL = {OLD_AG: NAME_AG[0], 'Artemis II': NAME[0], OLD_TITLE: NAME[0]}
n = 0
for f in glob.glob('*.html'):
    t = open(f, encoding='utf-8').read(); t0 = t
    t = re.sub(r'(<a [^>]*href="Artemis_II\.html"[^>]*>)(Artemis II \(NASA / CSA\)|Artemis II|Artemis II: The Farthest Humans Have Gone)(</a>)',
               lambda m: m.group(1) + LBL[m.group(2)] + m.group(3), t)
    t = t.replace(OLD_AG, NAME_AG[0])  # card image alts / data labels that carry the card name
    if t != t0: open(f, 'w', encoding='utf-8').write(t); n += 1
# --- i18n
for i, lang in enumerate(LANGS, 1):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf-8')); before = dict(m)
    m[NAME[0]] = NAME[i]; m[NAME_AG[0]] = NAME_AG[i]; m[TITLE[0]] = TITLE[i]; m[SUB[0]] = SUB[i]; m[DESC[0]] = DESC[i]
    m[CREDIT_TXT] = ['Vidéo : NASA, lancement d\u2019Artemis II, 1er avril 2026', 'Video: NASA, lanzamiento de Artemis II, 1 de abril de 2026',
                     'فيديو: ناسا، إطلاق Artemis II، 1 أبريل 2026', 'Video: NASA, lancio di Artemis II, 1 aprile 2026',
                     'וידאו: NASA, שיגור Artemis II, 1 באפריל 2026'][i - 1]
    for k in [k for k in before if OLD_AG in k and k != OLD_AG]:  # e.g. 'Artemis II (NASA / CSA): <image alt>'
        v = before[k]; v2 = v.replace(OLD_AG, NAME_AG[i])
        if v2 == v: v2 = re.sub(r'^Artemis II \([^)]*\)', NAME_AG[i], v)
        m[k.replace(OLD_AG, NAME_AG[0])] = v2
    if m != before: json.dump(m, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
# --- banner CSS (Lesson Builder size comes from the site-wide hero rule; this adds the motion)
def _ims(key):
    e = _mv[key]
    w = {int(x[:-1]): u for u, x in (t.strip().rsplit(' ', 1) for t in e['srcset'].split(','))}
    a = {int(x[:-1]): u for u, x in (t.strip().rsplit(' ', 1) for t in e['srcset_avif'].split(','))}
    return w, a
def _set(key, lo, hi):
    w, a = _ims(key); hi = min(hi, max(w))
    return (f"url('{w[lo]}');background-image:image-set(url('{a[lo]}') 1x type('image/avif'),url('{w[lo]}') 1x type('image/webp'),"
            f"url('{a[hi]}') 2x type('image/avif'),url('{w[hi]}') 2x type('image/webp'))")
_H = 'body.toc-sub.artemis-page .page-hero.space-hero'
CSS = ('/* ARTEMIS-PROGRAM:START (generated by scripts/build-artemis-program.py) */\n'
 f'{_H} {{ position: relative; overflow: hidden; isolation: isolate; background: #001428; }}\n'
 f'{_H}::before {{ content: ""; position: absolute; inset: 0; z-index: -3; background: #001428 center/cover no-repeat; background-image: {_set("images/ArtemisII_Launch_banner_wide.jpg", 1920, 3840)}; }}\n'
 f'@media (max-width: 900px) {{ {_H}::before {{ background-image: {_set("images/ArtemisII_Launch_banner_med.jpg", 1280, 2560)}; }} }}\n'
 f'@media (max-width: 600px) {{ {_H}::before {{ background-image: {_set("images/ArtemisII_Launch_banner_phone.jpg", 800, 1920)}; }} }}\n'
 f'{_H} > .art-hero-video {{ position: absolute; inset: 0; z-index: -2; width: 100%; height: 100%; object-fit: cover; object-position: 50% 50%; pointer-events: none; opacity: 0; transition: opacity .6s ease; }}\n'
 f'{_H}.art-video-on > .art-hero-video {{ opacity: 1; }}\n'
 f'{_H}::after {{ content: ""; position: absolute; inset: 0; z-index: -1; background: radial-gradient(ellipse 46% 62% at 50% 50%, rgba(0,20,40,.42) 0%, rgba(0,20,40,0) 100%), linear-gradient(180deg, rgba(0,20,40,.38) 0%, rgba(0,20,40,.55) 100%); }}\n'
 f'{_H} .page-hero-content h1, {_H} .page-hero-content p {{ text-shadow: 0 1px 3px rgba(0,0,0,.75), 0 0 18px rgba(0,0,0,.45); }}\n'
 f'@media (prefers-reduced-motion: reduce) {{ {_H} > .art-hero-video {{ display: none; }} {_H} .pr-motion-toggle {{ display: none; }} }}\n'
 '/* ARTEMIS-PROGRAM:END */')
css = open('styles.css', encoding='utf-8').read()
css2 = re.sub(r'/\* ARTEMIS-PROGRAM:START.*?ARTEMIS-PROGRAM:END \*/', lambda m: CSS, css, flags=re.S) if 'ARTEMIS-PROGRAM:START' in css else css.rstrip('\n') + '\n' + CSS + '\n'
if css2 != css: open('styles.css', 'w', encoding='utf-8').write(css2)
print(f'build-artemis-program: page {"updated" if s != s0 else "unchanged"}, labels in {n} files')
