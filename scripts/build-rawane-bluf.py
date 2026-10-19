#!/usr/bin/env python3
"""Oct 18 2026 (owner, iPad review): Project Rawane clean-up. Idempotent; runs before i18n-build in weekly-sync.
1) Impact Statement rewritten as a BLUF (bold hook, one sourced WOW, why it matters to people and nature, one next step).
   Facts: ESA Space Debris Office statistics (MASTER-8, 02/2026 population: 1.5 million objects 1-10 cm + 68,450 > 10 cm)
   and NASA HQ Library 'Space Debris' (debris can reach 18,000 mph, almost seven times faster than a bullet).
   The old four paragraphs repeated the cards below and the Five W's, so they are gone; the Errol Scales credit stays as one line.
2) Title banner: same size as the other hub pages (CSS lives in scripts/apply-heroes.py), with a slow Blue Marble pan;
   this file adds the pause button (WCAG 2.2.2), same pattern as Amazing Facts.
3) Hand translations of the new strings into i18n/<lang>.json (fr, es, ar, it, he)."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
PAGE = 'Project-Rawane.html'
ESA = 'https://sdup.esoc.esa.int/discosweb/statistics/'
NASA = 'https://www.nasa.gov/headquarters/library/find/bibliographies/space-debris/'
S = {  # English -> fr, es, ar, it, he
 'hook': ("Earth's orbit has become a junkyard, and real teams are now cleaning it up.",
   "L'orbite terrestre est devenue une décharge, et de vraies équipes commencent à la nettoyer.",
   "La órbita de la Tierra se ha convertido en un basurero, y equipos reales ya la están limpiando.",
   "أصبح مدار الأرض مكبًّا للنفايات، وفرق حقيقية بدأت بالفعل في تنظيفه.",
   "L'orbita terrestre è diventata una discarica, e squadre vere la stanno già ripulendo.",
   "המסלול סביב כדור הארץ הפך למזבלה, וצוותים אמיתיים כבר מנקים אותו."),
 'wow1': ("More than 1.5 million pieces of debris bigger than a centimeter circle Earth (",
   "Plus de 1,5 million de débris de plus d'un centimètre tournent autour de la Terre (",
   "Más de 1,5 millones de fragmentos de basura espacial de más de un centímetro giran alrededor de la Tierra (",
   "تدور حول الأرض أكثر من 1.5 مليون قطعة حطام يزيد حجمها على سنتيمتر واحد (",
   "Più di 1,5 milioni di detriti più grandi di un centimetro orbitano intorno alla Terra (",
   "יותר מ-1.5 מיליון שברי פסולת גדולים מסנטימטר מקיפים את כדור הארץ ("),
 'wow2': ("), and some reach 18,000 miles per hour, almost seven times faster than a bullet (",
   "), et certains atteignent près de 29 000 km/h, presque sept fois plus vite qu'une balle (",
   "), y algunos alcanzan casi 29.000 km/h, casi siete veces más rápido que una bala (",
   ")، وبعضها يبلغ نحو 29,000 كم في الساعة، أي أسرع من الرصاصة بنحو سبع مرات (",
   "), e alcuni raggiungono quasi 29.000 km/h, quasi sette volte più veloci di un proiettile (",
   "), וחלקם מגיעים לכ-29,000 קמ\"ש, כמעט פי שבעה ממהירות של קליע ("),
 'why': ("That junk threatens the satellites behind weather forecasts, GPS and the missions that watch forests, oceans and ice, so a cleaner orbit protects people and nature alike.",
   "Ces débris menacent les satellites dont dépendent les prévisions météo, le GPS et les missions qui surveillent les forêts, les océans et les glaces : une orbite plus propre protège à la fois les humains et la nature.",
   "Esa basura amenaza los satélites de los que dependen el pronóstico del tiempo, el GPS y las misiones que vigilan bosques, océanos y hielo, así que una órbita más limpia protege a las personas y a la naturaleza.",
   "يهدد هذا الحطام الأقمار الصناعية التي نعتمد عليها في التنبؤ بالطقس وتحديد المواقع (GPS) والبعثات التي ترصد الغابات والمحيطات والجليد، لذا فإن مدارًا أنظف يحمي البشر والطبيعة معًا.",
   "Questi detriti minacciano i satelliti da cui dipendono le previsioni meteo, il GPS e le missioni che osservano foreste, oceani e ghiacci: un'orbita più pulita protegge le persone e la natura.",
   "הפסולת הזו מאיימת על הלוויינים שעליהם נשענים תחזיות מזג האוויר, ה-GPS והמשימות שעוקבות אחר יערות, אוקיינוסים וקרח, ולכן מסלול נקי יותר מגן גם על בני האדם וגם על הטבע."),
 'cta': ("See the fixes below: debris removal, asteroid defense, solar storm warnings and voyages outward",
   "Découvrez les solutions ci-dessous : retrait des débris, défense contre les astéroïdes, alertes aux tempêtes solaires et voyages vers l'extérieur",
   "Descubre las soluciones abajo: retirada de basura espacial, defensa contra asteroides, alertas de tormentas solares y viajes hacia el exterior",
   "اكتشف الحلول أدناه: إزالة الحطام، والدفاع ضد الكويكبات، والإنذار بالعواصف الشمسية، والرحلات إلى الفضاء البعيد",
   "Scopri le soluzioni qui sotto: rimozione dei detriti, difesa dagli asteroidi, allerte per le tempeste solari e viaggi verso lo spazio profondo",
   "גלו את הפתרונות למטה: פינוי פסולת, הגנה מפני אסטרואידים, התרעות על סערות שמש ומסעות אל החלל העמוק"),
 'credit': ("Inspired by Errol Scales' work on orbital debris removal.",
   "Inspiré par les travaux d'Errol Scales sur le retrait des débris orbitaux.",
   "Inspirado en el trabajo de Errol Scales sobre la retirada de basura orbital.",
   "مستوحى من أعمال إيرول سكيلز في إزالة الحطام المداري.",
   "Ispirato al lavoro di Errol Scales sulla rimozione dei detriti orbitali.",
   "בהשראת העבודה של ארול סקיילס על פינוי פסולת מסלולית."),
 'pause': ("Pause banner animation", None, None, None, "Metti in pausa l'animazione del banner", None),
}
LANGS = ('fr', 'es', 'ar', 'it', 'he')
ext = 'target="_blank" rel="noreferrer"'
E = {k: v[0] for k, v in S.items()}
BLUF = ('<section class="impact pr-bluf"><h2>Impact Statement</h2><div class="impact-box">'
        f'<p class="bluf-hook"><strong>{E["hook"]}</strong></p>'
        f'<p class="bluf-wow">{E["wow1"]}<a href="{ESA}" {ext}>ESA</a>{E["wow2"]}<a href="{NASA}" {ext}>NASA</a>).</p>'
        f'<p class="bluf-why">{E["why"]}</p>'
        f'<p class="bluf-cta"><a href="#group-space-disposal">{E["cta"]}</a><span class="bluf-arrow" aria-hidden="true">→</span></p>'
        f'<p class="bluf-credit">{E["credit"]}</p>'
        '</div></section>').replace("'", '&#x27;').replace('&#x27;', "'")
s = open(PAGE, encoding='utf-8').read()
s2 = re.sub(r'<section class="impact(?: pr-bluf)?">.*?</section>', lambda m: BLUF, s, count=1, flags=re.S)
# pause button for the animated title banner (label stays constant; aria-pressed carries the state)
BTN = ('<button type="button" class="pr-motion-toggle" aria-pressed="false" aria-label="Pause banner animation">&#10074;&#10074;</button>'
       '<script>(function(){var b=document.querySelector(\'.pr-motion-toggle\'),h=b&&b.closest(\'.pr-hero\');if(!h)return;'
       'b.addEventListener(\'click\',function(){var p=b.getAttribute(\'aria-pressed\')!==\'true\';b.setAttribute(\'aria-pressed\',p);'
       'h.classList.toggle(\'pr-paused\',p);b.innerHTML=p?\'&#9654;\':\'&#10074;&#10074;\';});})();</script>')
s2 = re.sub(r'<button type="button" class="pr-motion-toggle".*?</script>', '', s2, flags=re.S)
s2 = re.sub(r'(<section class="page-hero pr-hero">.*?)(</section>)', lambda m: m.group(1) + BTN + m.group(2), s2, count=1, flags=re.S)
if s2 != s: open(PAGE, 'w', encoding='utf-8').write(s2)
n = 0
for i, lang in enumerate(LANGS, 1):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf-8')); before = dict(m)
    for k, v in S.items():
        if v[i]: m[v[0]] = v[i]
    if m != before: json.dump(m, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0); n += 1
print(f'build-rawane-bluf: page {"updated" if s2 != s else "unchanged"}, {n} i18n files updated')

# 4) Page CSS (one generated block in styles.css): BLUF look, centred section titles like the other hubs,
#    Five W's and Artemis cards in centred rows (no lone orphan card), banner pause button clear of the credit.
CSS = '''/* RAWANE-TIDY:START (generated by scripts/build-rawane-bluf.py) */
body.pr-page .impact > h2, body.pr-page .five-ws > h2 { text-align: center; }
body.toc-sub.pr-page .page-hero.pr-hero p.pr-dedication { margin-top: .35rem; line-height: 1.4; }
body.pr-page .pr-bluf .impact-box { max-width: 880px; margin: 0 auto; padding: 1.5rem 1.8rem; }
body.pr-page .pr-bluf .impact-box p { margin: 0 0 .7rem; line-height: 1.55; }
body.pr-page .pr-bluf .bluf-hook { font-size: clamp(1.2rem, 2.1vw, 1.5rem); line-height: 1.3; }
body.pr-page .pr-bluf .bluf-wow, body.pr-page .pr-bluf .bluf-why { font-size: 1.05rem; }
body.pr-page .pr-bluf .bluf-cta { margin-top: 1rem; font-weight: 700; }
body.pr-page .pr-bluf .bluf-cta a { color: #8fd3ff; }
body.pr-page .pr-bluf .bluf-arrow { display: inline-block; margin-inline-start: .35rem; color: #8fd3ff; }
[dir="rtl"] body.pr-page .pr-bluf .bluf-arrow, body.pr-page[dir="rtl"] .pr-bluf .bluf-arrow { transform: scaleX(-1); }
body.pr-page .pr-bluf .impact-box p.bluf-credit { margin: .9rem 0 0; font-size: .82rem; opacity: .75; }
body.pr-page .ws-grid { display: flex; flex-wrap: wrap; justify-content: center; }
body.pr-page .ws-grid > .w-card { flex: 0 1 calc((100% - 2rem) / 3); min-width: 0; box-sizing: border-box; }
@media (max-width: 900px) { body.pr-page .ws-grid > .w-card { flex-basis: calc((100% - 1rem) / 2); } }
@media (max-width: 600px) { body.pr-page .ws-grid > .w-card { flex-basis: 100%; } }
.pr-motion-toggle { position: absolute; left: .75rem; bottom: .55rem; z-index: 2; width: 2rem; height: 2rem; padding: 0; border: 1px solid rgba(255,255,255,.5); border-radius: 50%; background: rgba(0,20,40,.55); color: #fff; font-size: .7rem; line-height: 1; cursor: pointer; opacity: .8; }
[dir="rtl"] .pr-motion-toggle { left: auto; right: .75rem; }
.pr-motion-toggle:hover, .pr-motion-toggle:focus-visible { opacity: 1; }
.pr-motion-toggle:focus-visible { outline: 2px solid #8fd3ff; outline-offset: 2px; }
/* RAWANE-TIDY:END */'''
css = open('styles.css', encoding='utf-8').read()
css2 = re.sub(r'/\* RAWANE-TIDY:START.*?RAWANE-TIDY:END \*/', lambda m: CSS, css, flags=re.S) if 'RAWANE-TIDY:START' in css else css.rstrip('\n') + '\n' + CSS + '\n'
if css2 != css: open('styles.css', 'w', encoding='utf-8').write(css2); print('build-rawane-bluf: styles.css block updated')
