#!/usr/bin/env python3
"""Nov 23, 2026 batch 1: five sourced solutions (Lakes, Rivers, Planetary Defense).

Clones the Hawaiian Monk Seal page shell, then translates with i18n-build.
Does not run the full weekly sync. Created by the Founder and SI.
"""
import html, json, os, re, sys, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, 'scripts')
E = lambda s: html.escape(s, quote=True)
TODAY = '2026-11-23'
UNTIL = '2026-12-23'
BADGE = 'background:linear-gradient(135deg,#0077b0,#005f8f);color:#fff;border:1px solid rgba(160,225,255,.6);font-weight:800'
LANGS = ['fr', 'es', 'ar', 'it', 'he']
UI = {
    'en': dict(active='Active', new='✨ New solution', image='Image:', read='Read the official page'),
    'fr': dict(active='Actif', new='✨ Nouvelle solution', image='Image :', read="Lire la page officielle"),
    'es': dict(active='Activo', new='✨ Nueva solución', image='Imagen:', read='Leer la página oficial'),
    'ar': dict(active='نشط', new='✨ حل جديد', image='الصورة:', read='اقرأ الصفحة الرسمية'),
    'it': dict(active='Attiva', new='✨ Nuova soluzione', image='Immagine:', read='Leggi la pagina ufficiale'),
    'he': dict(active='פעיל', new='✨ פתרון חדש', image='תמונה:', read='קראו את העמוד הרשמי'),
}
HUBNAME = {
    'lakes': {'en': 'Lakes', 'fr': 'Lacs', 'es': 'Lagos', 'ar': 'البحيرات', 'it': 'Laghi', 'he': 'אגמים'},
    'rivers': {'en': 'Rivers', 'fr': 'Rivières', 'es': 'Ríos', 'ar': 'الأنهار', 'it': 'Fiumi', 'he': 'נהרות'},
    'planetary-defense': {'en': 'Planetary Defense', 'fr': 'Défense planétaire', 'es': 'Defensa planetaria', 'ar': 'الدفاع الكوكبي', 'it': 'Difesa planetaria', 'he': 'הגנה פלנטרית'},
}
EMOJI = {'lakes': '🏞️', 'rivers': '💧', 'planetary-defense': '☄️'}
STRIP = {
    'en': ('New this week', '{n} new solutions added on November 23. They are already counted in the {t} total.', 'See the full changelog', 'November 23, 2026', 'Solutions added'),
    'fr': ('Nouveau cette semaine', '{n} nouvelles solutions ajoutées le 23 novembre. Elles sont déjà comptées dans le total de {t}.', 'Voir tout le journal des modifications', '23 novembre 2026', 'Solutions ajoutées'),
    'es': ('Novedades de esta semana', '{n} soluciones nuevas añadidas el 23 de noviembre. Ya están incluidas en el total de {t}.', 'Ver el registro de cambios completo', '23 de noviembre de 2026', 'Soluciones añadidas'),
    'ar': ('جديد هذا الأسبوع', 'أُضيفت {n} حلول جديدة في 23 نوفمبر. وهي محسوبة بالفعل ضمن المجموع البالغ {t}.', 'عرض سجل التغييرات كاملًا', '23 نوفمبر 2026', 'حلول مضافة'),
    'it': ('Novità della settimana', '{n} nuove soluzioni aggiunte il 23 novembre. Sono già incluse nel totale di {t}.', 'Vedi il registro completo delle modifiche', '23 novembre 2026', 'Soluzioni aggiunte'),
    'he': ('חדש השבוע', '{n} פתרונות חדשים נוספו ב-23 בנובמבר. הם כבר נכללים בסך של {t}.', 'לרשימת השינויים המלאה', '23 בנובמבר 2026', 'פתרונות שנוספו'),
}

def T(en, **kw):
    """Translation map. Missing languages fall back to English."""
    out = {'en': en}
    out.update(kw)
    return out

# Shared strings
S = {
    'every': T('Every fact on this page comes from one of these public pages.',
        fr='Chaque fait de cette page vient de l’une de ces pages publiques.',
        es='Cada dato de esta página sale de una de estas páginas públicas.',
        ar='كل حقيقة في هذه الصفحة مأخوذة من إحدى هذه الصفحات العامة.',
        it='Ogni fatto di questa pagina viene da una di queste pagine pubbliche.',
        he='כל עובדה בעמוד הזה לקוחה מאחד העמודים הציבוריים האלה.'),
    'showcase': T('Saving Planets is showcasing this work, not partnering with it.',
        fr='Saving Planets présente ce travail. Ce n’est pas un partenariat.',
        es='Saving Planets muestra este trabajo. No es una alianza.',
        ar='Saving Planets تعرض هذا العمل. هذه ليست شراكة.',
        it='Saving Planets presenta questo lavoro. Non è una partnership.',
        he='Saving Planets מציגה את העבודה הזו. זו אינה שותפות.'),
    'nodeonate': T('There is no donate button, because this is a public agency or public body.',
        fr='Il n’y a pas de bouton de don, car il s’agit d’un organisme public.',
        es='No hay botón de donación, porque se trata de un organismo público.',
        ar='لا يوجد زر تبرع، لأن هذه جهة عامة.',
        it='Non c’è un pulsante per donare, perché si tratta di un ente pubblico.',
        he='אין כפתור תרומה, כי זה גוף ציבורי.'),
}

def src(name, url):
    return f'<p class="fact-source">Source: <a href="{E(url)}" target="_blank" rel="noopener">{E(name)}</a></p>'

def page_main(p):
    ws = []
    for key, label in [('who', 'Who'), ('what', 'What'), ('when', 'When'), ('where', 'Where'), ('why', 'Why')]:
        bits = ''.join(f'<p>{E(t)}</p>' for t in p[key]['text']) + ''.join(src(n, u) for n, u in p[key]['sources'])
        ws.append(f'<div class="w-card"><h3>{label}</h3>{bits}</div>')
    eli = ''.join(f'<li>{E(t)}</li>' for t in p['eli'])
    sources = ''.join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(n)}</a></li>' for n, u in p['sources'])
    nsrc = f'{len(p["sources"])} source cited' if len(p['sources']) == 1 else f'{len(p["sources"])} sources cited'
    credit = f'<p class="photo-credit">{E(p["credit"])} <a href="{E(p["credit_url"])}" target="_blank" rel="noopener">Source</a>.</p>'
    return f'''<section class="page-hero space-hero" style="background-image:linear-gradient(rgba(0,20,40,.35),rgba(0,20,40,.62)),url('{p["img"]}');background-size:cover;background-position:center 42%"><div class="page-hero-content"><h1>{E(p["title"])}</h1><p>{E(p["blurb"])}</p></div></section>
{credit}
<nav aria-label="Breadcrumb" class="breadcrumb" hidden><ol><li><a href="index.html">Home</a></li><li><a href="{p["hub_file"]}">{E(HUBNAME[p["hub"]]["en"])}</a></li><li><span aria-current="page">{E(p["title"])}</span></li></ol></nav>
<!-- REVIEWED:START --><p class="page-reviewed" aria-label="Page review and sources" data-pagefind-ignore><span class="rv-label">Last reviewed:</span> <time datetime="2026-11">November 2026</time><span aria-hidden="true"> · </span><a href="#sources">{nsrc}</a></p><!-- REVIEWED:END -->
<!-- ELI10:START --><section class="eli10" id="eli10" aria-labelledby="eli10-h"><h2 id="eli10-h"><span class="eli10-icon" aria-hidden="true">💡</span> Explain Like I'm 10</h2><ul>{eli}</ul></section><!-- ELI10:END -->
<section class="five-ws" id="solution"><h2>The Five W's of {E(p["title"])}</h2><div class="ws-grid">{''.join(ws)}</div></section>
<style>details.src-fold{{max-width:1100px;margin:.4rem auto 0;padding:0 1.5rem}}details.src-fold>summary{{cursor:pointer;font-weight:700;min-height:44px;display:flex;align-items:center;font-size:1.25rem}}details.src-fold ul{{margin:.2rem 0 1rem;padding-inline-start:1.2rem;line-height:1.55}}details.src-fold a{{text-decoration:underline;text-underline-offset:.12em}}details.src-fold>summary:focus-visible{{outline:3px solid #f5b400;outline-offset:3px}}</style>
<details class="src-fold" id="sources"><summary>Sources</summary><p>{E(S["every"]["en"])}</p><ul>{sources}</ul></details>
<section class="impact" id="impact"><h2>Impact Statement</h2><div class="impact-box"><p class="hub-label">{E(p["label"])}</p><p>{E(p["impact"])}</p>{''.join(src(n, u) for n, u in p["impact_src"])}</div></section>
<section class="impact saves-planets" id="saves"><h2>How This Saves People &amp; the Planet</h2><div class="impact-box"><h3 class="mission-title">For People</h3><p>{E(p["people"])}</p>{src(*p["people_src"])}<h3 class="mission-title">For Nature</h3><p>{E(p["nature"])}</p>{src(*p["nature_src"])}</div></section>
<section class="five-ws help-cta" id="support"><h2>Learn About {E(p["title"])}</h2><div class="help-btns"><a class="btn help-btn" href="{E(p["official"])}" target="_blank" rel="noopener">{E(p["button"])}</a></div><p>{E(S["nodeonate"]["en"])} {E(S["showcase"]["en"])}</p></section>
<section class="next-solutions" aria-label="Explore another solution"><h2>Next: Explore Another Solution</h2><ul>{''.join(f'<li><a href="{E(h)}">{E(n)}</a></li>' for n, h in p["next"])}</ul></section>
<section class="help-actions" id="help" aria-label="Ways to help"><h2>Help This Work</h2><p>{E(p["help"])} {E(S["showcase"]["en"])}</p><div class="help-btns"><a class="btn help-btn" href="{E(p["official"])}" target="_blank" rel="noopener">{E(p["button"])}</a><a class="btn help-btn" href="Ways_to_Help.html#roll-up-your-sleeves">Roll up your sleeves</a></div><p class="help-more"><a href="Ways_to_Help.html">See all ways to help</a></p></section>
'''

NASA_CONFIRM = 'https://www.nasa.gov/news-release/nasa-confirms-dart-mission-impact-changed-asteroids-motion-in-space/'
NASA_2024 = 'https://www.nasa.gov/missions/dart/nasa-study-asteroids-orbit-shape-changed-after-dart-impact/'
DEC_PDF = 'https://extapps.dec.ny.gov/data/der/factsheet/olprogress1017.pdf'
EPA_REUSE = 'https://semspub.epa.gov/work/HQ/100002042.pdf'
EGLV_2022 = 'https://www.eglv.de/medien/ziel-erreicht-emscher-ist-jetzt-komplett-abwasserfrei/'
EGLV_2024 = 'https://www.eglv.de/medien/125-jahre-emschergenossenschaft/'
CIPEL = 'https://www.cipel.org/wp-content/uploads/2026/03/cp2026-resultats-etat-de-sante-du-leman-cipel.pdf'
EPA_HUDSON = 'https://www.epa.gov/hudsonriverpcbs/hudson-river-cleanup'

PAGES = [
 dict(
    file='DART.html', title='DART (NASA)', hub='planetary-defense', hub_file='Planetary_Defense.html',
    anchor='Hayabusa2_Torifune.html', region='orbit', glass='defense', tint='space', klass='agency',
    img='assets/DART_Dimorphos_Impact_NASA.jpg', w=985, h=985,
    alt='The boulder-covered surface of asteroid Dimorphos, photographed by NASA\'s DART spacecraft seconds before impact',
    credit='Photo: NASA/Johns Hopkins Applied Physics Laboratory, public domain.',
    credit_url='https://commons.wikimedia.org/wiki/File:Footprint_of_DART_spacecraft_over_the_spot_where_it_impacted_asteroid_Dimorphos.jpg',
    blurb='NASA\'s DART spacecraft shortened the orbit of asteroid Dimorphos by 33 minutes and 15 seconds.',
    label='Agency solution · active',
    eli=["DART was a NASA spacecraft sent to hit a small asteroid on purpose.",
         "It struck Dimorphos on September 26, 2022, and the orbit got shorter.",
         "The final measurement is 33 minutes and 15 seconds shorter. It was the first time people changed an asteroid's path."],
    who=dict(text=["NASA ran the Double Asteroid Redirection Test with the Johns Hopkins Applied Physics Laboratory. The spacecraft was a kinetic impactor: it hit an asteroid to change the asteroid's path."],
             sources=[('NASA, DART changed an asteroid\'s motion', NASA_CONFIRM)]),
    what=dict(text=["On September 26, 2022, DART hit Dimorphos, a moon about 170 meters wide that orbits the larger asteroid Didymos. Before the hit, one loop around Didymos took 11 hours and 55 minutes."],
              sources=[('NASA, asteroid orbit and shape after DART', NASA_2024)]),
    when=dict(text=["On October 11, 2022, NASA said the orbit was about 32 minutes shorter, with an uncertainty of about 2 minutes. That was more than 25 times the 73-second change NASA had set as the minimum for success. A 2024 study measured the final change at 33 minutes and 15 seconds."],
              sources=[('NASA, DART changed an asteroid\'s motion', NASA_CONFIRM), ('NASA, asteroid orbit and shape after DART', NASA_2024)]),
    where=dict(text=["Dimorphos orbits Didymos. NASA says neither asteroid is a threat to Earth. The test used a safe target so the team could measure the method."],
               sources=[('NASA, DART changed an asteroid\'s motion', NASA_CONFIRM)]),
    why=dict(text=["If a dangerous asteroid were ever found on a path toward Earth, a measured kinetic impactor is one way to nudge it while a small push can still matter."],
             sources=[('NASA, DART changed an asteroid\'s motion', NASA_CONFIRM)]),
    impact="DART was the first time people purposely changed the motion of a celestial object. Dimorphos's orbit ended 33 minutes and 15 seconds shorter.",
    impact_src=[('NASA, DART changed an asteroid\'s motion', NASA_CONFIRM), ('NASA, asteroid orbit and shape after DART', NASA_2024)],
    people="Planetary-defense teams now have a measured result: a spacecraft can move an asteroid moon by far more than the 73-second minimum NASA set before launch.",
    people_src=('NASA, DART changed an asteroid\'s motion', NASA_CONFIRM),
    nature="Dimorphos and Didymos do not threaten Earth. Hitting a safe pair let NASA learn the method away from any city.",
    nature_src=('NASA, DART changed an asteroid\'s motion', NASA_CONFIRM),
    official=NASA_CONFIRM, button='Read the NASA results',
    help='This is a finished NASA test, so there is no donate button.',
    ways='NASA\'s DART shortened Dimorphos\'s orbit by 33 minutes and 15 seconds, the first time a spacecraft changed an asteroid\'s path on purpose.',
    next=[('Hera', 'Hera.html'), ('IAU Minor Planet Center', 'Minor_Planet_Center.html'), ('Planetary Defense', 'Planetary_Defense.html')],
    sources=[('NASA, DART changed an asteroid\'s motion', NASA_CONFIRM), ('NASA, asteroid orbit and shape after DART', NASA_2024)],
 ),
 dict(
    file='Onondaga_Lake_Cleanup.html', title='Onondaga Lake Cleanup', hub='lakes', hub_file='Lakes.html',
    anchor='Restoring_the_Lake_Depths.html', region='americas', glass='lakes', tint='water', klass='government',
    img='assets/Onondaga_Lake_Willow_Bay.jpg', w=1600, h=960,
    alt='The shoreline of Onondaga Lake at Willow Bay, looking northwest across the water',
    credit='Photo: Andre Carrotflower, CC BY-SA 4.0.',
    credit_url='https://commons.wikimedia.org/wiki/File:Onondaga_Lake_Park_-_20220506_-_05_-_Shoreline_looking_northwest_from_Willow_Bay.jpg',
    blurb='By October 2017, 89 acres of wetlands had been created or enhanced at Onondaga Lake, with nearly 780,000 native plants.',
    label='Government solution · active',
    eli=['Onondaga Lake in Syracuse, New York, was polluted by industry and sewage.',
         'Crews dredged and capped the lake bottom, then restored the shore.',
         'By October 2017, New York reported 89 acres of wetlands and nearly 780,000 native plants.'],
    who=dict(text=['The cleanup is a U.S. Superfund project. The U.S. Environmental Protection Agency and the New York State Department of Environmental Conservation oversee it. Honeywell did the lake-bottom work under that plan.'],
             sources=[('U.S. EPA, Onondaga Lake reuse report (September 2018)', EPA_REUSE), ('New York State DEC, Onondaga Lake cleanup progress (October 2017)', DEC_PDF)]),
    what=dict(text=['As of October 2017, New York reported that 89 acres of wetlands had been created or enhanced, with nearly 780,000 native trees, plants, and shrubs along the shore and tributaries.'],
              sources=[('New York State DEC, Onondaga Lake cleanup progress (October 2017)', DEC_PDF)]),
    when=dict(text=['New York\'s October 2017 fact sheet said nitrate addition in the deep water began in 2012, and that habitat restoration was scheduled to finish in fall 2017. EPA reported in September 2018 that dredging was completed in 2014, capping in 2016, and habitat restoration in 2017.'],
              sources=[('New York State DEC, Onondaga Lake cleanup progress (October 2017)', DEC_PDF), ('U.S. EPA, Onondaga Lake reuse report (September 2018)', EPA_REUSE)]),
    where=dict(text=['Onondaga Lake is in Syracuse, Onondaga County, New York. The 2017 fact sheet lists shoreline work at Geddes Brook, Ninemile Creek, Harbor Brook, and parts of the western shore.'],
               sources=[('New York State DEC, Onondaga Lake cleanup progress (October 2017)', DEC_PDF)]),
    why=dict(text=['Mercury in the sediments can become methylmercury, which builds up in fish. The deep-water nitrate addition is meant to slow that process. EPA\'s 2018 report still noted a fish-consumption advisory.'],
             sources=[('New York State DEC, Onondaga Lake cleanup progress (October 2017)', DEC_PDF), ('U.S. EPA, Onondaga Lake reuse report (September 2018)', EPA_REUSE)]),
    impact='By October 2017 the state counted 89 acres of created or enhanced wetlands and nearly 780,000 native plants. EPA later recorded the dredging, the cap, and the habitat work as complete.',
    impact_src=[('New York State DEC, Onondaga Lake cleanup progress (October 2017)', DEC_PDF), ('U.S. EPA, Onondaga Lake reuse report (September 2018)', EPA_REUSE)],
    people='Long-term monitoring covers fish, water, and the cap, with New York and EPA oversight, on a lake people already use for trails and boating.',
    people_src=('U.S. EPA, Onondaga Lake reuse report (September 2018)', EPA_REUSE),
    nature='The wetland and shoreline plantings are habitat along the lake and its creeks. The nitrate addition targets methylmercury in deep water.',
    nature_src=('New York State DEC, Onondaga Lake cleanup progress (October 2017)', DEC_PDF),
    official=DEC_PDF, button='Read the New York fact sheet',
    help='This is a government cleanup, so there is no donate button.',
    ways='By October 2017, New York reported 89 acres of wetlands and nearly 780,000 native plants restored at Onondaga Lake.',
    next=[('Lake Washington Cleanup (Seattle)', 'Lake_Washington_Cleanup.html'), ('Lakes', 'Lakes.html')],
    sources=[('New York State DEC, Onondaga Lake cleanup progress (October 2017)', DEC_PDF), ('U.S. EPA, Onondaga Lake reuse report (September 2018)', EPA_REUSE)],
 ),
 dict(
    file='Emscher_River_Restoration.html', title='Emscher River Restoration', hub='rivers', hub_file='Rivers.html',
    anchor='FreshWater_Watch.html', region='eurafrica', glass='rivers', tint='water', klass='government',
    img='assets/Emscher_Phoenix_See.jpg', w=1600, h=1067,
    alt='The restored Emscher flowing beside Phoenix See in Dortmund, Germany',
    credit='Photo: Frank Vincentz, CC BY-SA 3.0.',
    credit_url='https://commons.wikimedia.org/wiki/File:Dortmund_-_PO-Emscher_%2B_Phoenix-See_%2B_H%C3%B6rde_01_ies.jpg',
    blurb='By the end of 2021 the Emscher carried no wastewater for the first time in about 170 years, after more than 430 kilometers of new sewers.',
    label='Government solution · active',
    eli=['The Emscher, in Germany\'s Ruhr region, was an open sewer for about 170 years.',
         'The Emschergenossenschaft built underground sewers and treatment plants to take the wastewater out.',
         'At the end of 2021, the river was free of wastewater.'],
    who=dict(text=['The Emschergenossenschaft is a public-law water association, founded on December 14, 1899. It handles wastewater, flood protection, and the restoration of the Emscher and its tributaries.'],
             sources=[('Emschergenossenschaft, 125 years (June 20, 2024)', EGLV_2024)]),
    what=dict(text=['From 1992 through 2021 the association built more than 430 kilometers of new underground sewers and four large treatment plants. On the last day of 2021, wastewater that still needed treatment stopped flowing into the Emscher.'],
              sources=[('Emschergenossenschaft, the Emscher is wastewater-free (January 3, 2022)', EGLV_2022)]),
    when=dict(text=['The conversion took 30 years and finished at the end of 2021, on the schedule set at the start. The association announced it on January 3, 2022. It put the cost at about 5.5 billion euros.'],
              sources=[('Emschergenossenschaft, the Emscher is wastewater-free (January 3, 2022)', EGLV_2022)]),
    where=dict(text=['The Emscher is the central river of Germany\'s Ruhr region. The sewers and the restoration cover the river and its tributaries.'],
               sources=[('Emschergenossenschaft, the Emscher is wastewater-free (January 3, 2022)', EGLV_2022)]),
    why=dict(text=['For about 170 years, untreated wastewater flowed in the open river. By the 2022 announcement, about 150 kilometers of waterways had been reshaped and the association said species diversity had tripled. In June 2024 it said more than 170 kilometers had been restored.'],
             sources=[('Emschergenossenschaft, the Emscher is wastewater-free (January 3, 2022)', EGLV_2022), ('Emschergenossenschaft, 125 years (June 20, 2024)', EGLV_2024)]),
    impact='The Emscher has carried no untreated wastewater since the end of 2021. More than 430 kilometers of new sewers made that possible, and more than 170 kilometers of waterways had been reshaped by June 2024.',
    impact_src=[('Emschergenossenschaft, the Emscher is wastewater-free (January 3, 2022)', EGLV_2022), ('Emschergenossenschaft, 125 years (June 20, 2024)', EGLV_2024)],
    people='The 2022 announcement included about 130 kilometers of new cycle and walking paths along the cleaner water.',
    people_src=('Emschergenossenschaft, the Emscher is wastewater-free (January 3, 2022)', EGLV_2022),
    nature='The association said species diversity along the Emscher tripled over 30 years, and that kingfishers were breeding on the river again.',
    nature_src=('Emschergenossenschaft, the Emscher is wastewater-free (January 3, 2022)', EGLV_2022),
    official=EGLV_2022, button='Read the Emschergenossenschaft account',
    help='The Emschergenossenschaft is a public water association, so there is no donate button.',
    ways='By the end of 2021 the Emscher carried no wastewater for the first time in about 170 years, after more than 430 kilometers of new sewers.',
    next=[('Cuyahoga River Cleanup (Ohio)', 'Cuyahoga_River_Cleanup.html'), ('Rivers', 'Rivers.html')],
    sources=[('Emschergenossenschaft, the Emscher is wastewater-free (January 3, 2022)', EGLV_2022), ('Emschergenossenschaft, 125 years (June 20, 2024)', EGLV_2024)],
 ),
 dict(
    file='Lake_Geneva_CIPEL.html', title='Lake Geneva Phosphorus Cleanup', hub='lakes', hub_file='Lakes.html',
    anchor='Lake_Plastic_Recovery.html', region='eurafrica', glass='lakes', tint='water', klass='government',
    img='assets/Lake_Geneva_NASA.jpg', w=1280, h=795,
    alt='Lake Geneva between France and Switzerland, seen from a NASA satellite',
    credit='Photo: NASA, public domain.',
    credit_url='https://commons.wikimedia.org/wiki/File:Genfersee_satellit.jpg',
    blurb='Total phosphorus in Lake Geneva fell from nearly 100 micrograms per liter in 1978 to 15.6 in 2024.',
    label='Government solution · active',
    eli=['Too much phosphorus turned Lake Geneva green with algae in the 1970s.',
         'France and Switzerland, through CIPEL, cut phosphorus from sewage, detergents, and farms.',
         'In 2024 the average through the whole water column was 15.6 micrograms per liter, the lowest since 1970.'],
    who=dict(text=['CIPEL, the International Commission for the Protection of the Waters of Lake Geneva, is the France–Switzerland body that tracks the lake and recommends how to protect it.'],
             sources=[('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL)]),
    what=dict(text=['Treatment plants were built and improved, phosphates in detergents were restricted, and farm inputs were reduced. CIPEL says those steps cut total phosphorus from nearly 100 micrograms per liter in 1978 to 15.6 in 2024.'],
              sources=[('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL)]),
    when=dict(text=['The high levels were in the 1970s. The 15.6 figure is the 2024 annual average, weighted through the water column, in CIPEL\'s March 30, 2026 release. CIPEL calls 10 to 15 micrograms per liter its long-standing goal.'],
              sources=[('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL)]),
    where=dict(text=['Lake Geneva, also called Lac Léman, lies between France and Switzerland. The cleanup was done on both shores.'],
               sources=[('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL)]),
    why=dict(text=['Phosphorus feeds algae. Cutting it reduced algal blooms and improved water used for drinking, fishing, and swimming. CIPEL also says the lake still needs watching because of a warming climate, invasive species, and micropollutants.'],
             sources=[('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL)]),
    impact='The 2024 average of 15.6 micrograms of total phosphorus per liter is the lowest since 1970, down from nearly 100 in 1978, and it sits near CIPEL\'s goal of 10 to 15.',
    impact_src=[('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL)],
    people='Clearer water supports drinking water, fishing, and recreation on a lake shared by France and Switzerland.',
    people_src=('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL),
    nature='Less phosphorus means fewer algal blooms. CIPEL says winter mixing of the lake is now weaker, so the phosphorus drop does not end the need to watch the lake.',
    nature_src=('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL),
    official=CIPEL, button='Read the CIPEL release',
    help='CIPEL is an intergovernmental commission, so there is no donate button.',
    ways='Total phosphorus in Lake Geneva fell from nearly 100 micrograms per liter in 1978 to 15.6 in 2024, CIPEL reports.',
    next=[('Lake Washington Cleanup (Seattle)', 'Lake_Washington_Cleanup.html'), ('Lakes', 'Lakes.html')],
    sources=[('CIPEL, Lake Geneva health results (March 30, 2026)', CIPEL)],
 ),
 dict(
    file='Hudson_River_PCB_Cleanup.html', title='Hudson River PCB Cleanup', hub='rivers', hub_file='Rivers.html',
    anchor='Kissimmee_River_Restoration.html', region='americas', glass='rivers', tint='water', klass='government',
    img='assets/Hudson_River_Aerial.jpg', w=1600, h=1200,
    alt='An aerial view of the Hudson River between Westchester and Rockland Counties, New York',
    credit='Photo: Jessica Spengler, CC BY 2.0.',
    credit_url='https://commons.wikimedia.org/wiki/File:Aerial_view_of_the_Hudson_River.jpg',
    blurb='About 2.75 million cubic yards of PCB-contaminated sediment were dredged from the Upper Hudson River between 2009 and 2015.',
    label='Government solution · active',
    eli=['Factories left PCBs, a long-lasting industrial chemical, in the mud of the Hudson River.',
         'The U.S. EPA required dredges to dig out the most contaminated mud.',
         'About 2.75 million cubic yards were removed from 2009 through 2015.'],
    who=dict(text=['The U.S. Environmental Protection Agency leads the Hudson River PCBs Superfund site. General Electric carried out the dredging required by EPA\'s cleanup decision.'],
             sources=[('U.S. EPA, Hudson River cleanup', EPA_HUDSON)]),
    what=dict(text=['EPA\'s 2002 decision called for dredging about 2.65 million cubic yards of PCB-contaminated sediment. Across six seasons, about 2.75 million cubic yards were removed.'],
              sources=[('U.S. EPA, Hudson River cleanup', EPA_HUDSON)]),
    when=dict(text=['Dredging began in 2009 and finished in fall 2015. Phase 1, in 2009, removed about 283,000 cubic yards. Phase 2 removed about 2.5 million cubic yards.'],
              sources=[('U.S. EPA, Hudson River cleanup', EPA_HUDSON)]),
    where=dict(text=['The work was on the Upper Hudson River in New York, a 40-mile stretch from Fort Edward to Troy.'],
               sources=[('U.S. EPA, Hudson River cleanup', EPA_HUDSON)]),
    why=dict(text=['PCBs stay in river mud and can build up in fish. Removing the targeted sediment is the dredging part of the remedy. EPA says sampling of water, sediment, and fish continues.'],
             sources=[('U.S. EPA, Hudson River cleanup', EPA_HUDSON)]),
    impact='Over six seasons, from 2009 to 2015, about 2.75 million cubic yards of PCB-contaminated sediment were taken off the Upper Hudson river bottom.',
    impact_src=[('U.S. EPA, Hudson River cleanup', EPA_HUDSON)],
    people='The dredging targets a river people fish. EPA says water, sediment, and fish are still sampled after the digging ended.',
    people_src=('U.S. EPA, Hudson River cleanup', EPA_HUDSON),
    nature='Removing PCB-contaminated mud from a 40-mile reach takes out contamination that can move through the river food web.',
    nature_src=('U.S. EPA, Hudson River cleanup', EPA_HUDSON),
    official=EPA_HUDSON, button='Read the EPA cleanup page',
    help='This is a federal Superfund cleanup, so there is no donate button.',
    ways='About 2.75 million cubic yards of PCB-contaminated sediment were dredged from the Upper Hudson River between 2009 and 2015.',
    next=[('Cuyahoga River Cleanup (Ohio)', 'Cuyahoga_River_Cleanup.html'), ('Rivers', 'Rivers.html')],
    sources=[('U.S. EPA, Hudson River cleanup', EPA_HUDSON)],
 ),
]

# Titles and blurbs that must be translated. Paragraphs below are translated as whole strings.
TR = {}

def add_tr(en, fr, es, ar, it, he):
    TR[en] = {'fr': fr, 'es': es, 'ar': ar, 'it': it, 'he': he}

# Titles
add_tr('DART (NASA)', 'DART (NASA)', 'DART (NASA)', 'DART (ناسا)', 'DART (NASA)', 'DART (NASA)')
add_tr('Onondaga Lake Cleanup', 'Dépollution du lac Onondaga', 'Limpieza del lago Onondaga', 'تنظيف بحيرة أونونداغا', 'Bonifica del lago Onondaga', 'ניקוי אגם אונונדאגה')
add_tr('Emscher River Restoration', 'Restauration de la rivière Emscher', 'Restauración del río Emscher', 'ترميم نهر الإمشِر', 'Ripristino del fiume Emscher', 'שיקום נהר האמשר')
add_tr('Lake Geneva Phosphorus Cleanup', 'Réduction du phosphore dans le Léman', 'Limpieza del fósforo en el lago Lemán', 'خفض الفوسفور في بحيرة جنيف', 'Riduzione del fosforo nel Lago di Ginevra', 'הפחתת הזרחן באגם ז\'נבה')
add_tr('Hudson River PCB Cleanup', 'Dépollution des PCB de l’Hudson', 'Limpieza de PCB del río Hudson', 'تنظيف مركبات PCB في نهر هدسون', 'Bonifica dei PCB del fiume Hudson', 'ניקוי PCB בנהר ההדסון')
# Blurbs (also hero, meta, ways)
add_tr("NASA's DART spacecraft shortened the orbit of asteroid Dimorphos by 33 minutes and 15 seconds.",
      "La sonde DART de la NASA a raccourci l’orbite de l’astéroïde Dimorphos de 33 minutes et 15 secondes.",
      "La nave DART de la NASA acortó la órbita del asteroide Dimorphos en 33 minutos y 15 segundos.",
      "قصّرت مركبة DART التابعة لناسا مدار الكويكب ديمورفوس بمقدار 33 دقيقة و15 ثانية.",
      "La sonda DART della NASA ha accorciato l’orbita dell’asteroide Dimorphos di 33 minuti e 15 secondi.",
      "החללית DART של נאס\"א קיצרה את מסלול האסטרואיד דימורפוס ב-33 דקות ו-15 שניות.")
add_tr('By October 2017, 89 acres of wetlands had been created or enhanced at Onondaga Lake, with nearly 780,000 native plants.',
      "En octobre 2017, 89 acres de zones humides avaient été créés ou améliorés au lac Onondaga, avec près de 780 000 plantes indigènes.",
      "En octubre de 2017 se habían creado o mejorado 89 acres de humedales en el lago Onondaga, con casi 780.000 plantas nativas.",
      "بحلول أكتوبر 2017، أُنشئت أو حُسّنت 89 فدانًا من الأراضي الرطبة في بحيرة أونونداغا، مع ما يقرب من 780 ألف نبتة محلية.",
      "Entro ottobre 2017 erano stati creati o migliorati 89 acri di zone umide al lago Onondaga, con quasi 780.000 piante autoctone.",
      "עד אוקטובר 2017 נוצרו או שופרו 89 אקרים של ביצות באגם אונונדאגה, עם כמעט 780,000 צמחים מקומיים.")
add_tr('By the end of 2021 the Emscher carried no wastewater for the first time in about 170 years, after more than 430 kilometers of new sewers.',
      "Fin 2021, l’Emscher ne charriait plus d’eaux usées pour la première fois en environ 170 ans, après plus de 430 kilomètres de nouveaux égouts.",
      "A finales de 2021 el Emscher ya no llevaba aguas residuales por primera vez en unos 170 años, tras más de 430 kilómetros de nuevas alcantarillas.",
      "بنهاية عام 2021 لم يعد نهر الإمشِر يحمل مياه صرف للمرة الأولى منذ نحو 170 عامًا، بعد مدّ أكثر من 430 كيلومترًا من المجاري الجديدة.",
      "Alla fine del 2021 l’Emscher non trasportava più acque reflue per la prima volta in circa 170 anni, dopo oltre 430 chilometri di nuove fognature.",
      "בסוף 2021 נהר האמשר לא נשא עוד שפכים בפעם הראשונה מזה כ-170 שנה, אחרי יותר מ-430 קילומטרים של ביוב חדש.")
add_tr('Total phosphorus in Lake Geneva fell from nearly 100 micrograms per liter in 1978 to 15.6 in 2024.',
      "Le phosphore total du Léman est passé de près de 100 microgrammes par litre en 1978 à 15,6 en 2024.",
      "El fósforo total del lago Lemán bajó de casi 100 microgramos por litro en 1978 a 15,6 en 2024.",
      "انخفض الفوسفور الكلي في بحيرة جنيف من نحو 100 ميكروغرام لكل لتر عام 1978 إلى 15.6 عام 2024.",
      "Il fosforo totale del Lago di Ginevra è sceso da quasi 100 microgrammi per litro nel 1978 a 15,6 nel 2024.",
      "הזרחן הכולל באגם ז'נבה ירד מכמעט 100 מיקרוגרם לליטר ב-1978 ל-15.6 ב-2024.")
add_tr('About 2.75 million cubic yards of PCB-contaminated sediment were dredged from the Upper Hudson River between 2009 and 2015.',
      "Environ 2,75 millions de yards cubes de sédiments contaminés aux PCB ont été dragués dans le Haut-Hudson entre 2009 et 2015.",
      "Unos 2,75 millones de yardas cúbicas de sedimento contaminado con PCB se dragaron del Alto Hudson entre 2009 y 2015.",
      "جُرف نحو 2.75 مليون ياردة مكعبة من الرواسب الملوثة بمركبات PCB من أعالي نهر هدسون بين 2009 و2015.",
      "Circa 2,75 milioni di iarde cubiche di sedimenti contaminati da PCB sono stati dragati dall’Alto Hudson tra il 2009 e il 2015.",
      "כ-2.75 מיליון יארד מעוקב של משקע מזוהם ב-PCB נחפרו מההדסון העליון בין 2009 ל-2015.")

def collect_strings(p):
    out = [p['title'], p['blurb'], p['alt'], p['credit'], p['impact'], p['people'], p['nature'], p['help'], p['button'], p['ways'], p['label']]
    out += p['eli']
    for key in ('who', 'what', 'when', 'where', 'why'):
        out += p[key]['text']
        out += [n for n, u in p[key]['sources']]
    out += [n for n, u in p['sources']]
    out += [n for n, u in p['next']]
    return out

# Hand translations for the longer paragraphs live in i18n/batch-1123.json if present.
# The strings not listed in TR stay English until merge_tr fills them from BATCH_TR below.
BATCH_TR_PATH = 'i18n/batch-1123.json'

def strings_needed():
    need = []
    for p in PAGES:
        for s in collect_strings(p):
            if s not in TR and s not in need:
                need.append(s)
    for key in ('every', 'showcase', 'nodeonate'):
        if S[key]['en'] not in TR:
            need.append(S[key]['en'])
    return need

def write_english():
    shell = open('Hawaiian_Monk_Seal_Recovery.html', encoding='utf8').read()
    a, b = shell.find('<section class="page-hero'), shell.find('</main>')
    assert a > 0 and b > a
    for p in PAGES:
        page = shell[:a] + page_main(p) + shell[b:]
        page = page.replace('Hawaiian_Monk_Seal_Recovery.html', p['file'])
        page = page.replace('href="fr/index.html"', f'href="fr/{p["file"]}"')
        page = page.replace('href="es/index.html"', f'href="es/{p["file"]}"')
        page = page.replace('href="ar/index.html"', f'href="ar/{p["file"]}"')
        page = page.replace('href="it/index.html"', f'href="it/{p["file"]}"')
        page = page.replace('href="he/index.html"', f'href="he/{p["file"]}"')
        old_title = 'Hawaiian Monk Seal Recovery'
        page = page.replace(f'<title>{old_title} | Saving Planets</title>', f'<title>{E(p["title"])} | Saving Planets</title>')
        page = page.replace(f'content="{old_title} | Saving Planets"', f'content="{E(p["title"])} | Saving Planets"')
        old_desc = 'NOAA Fisheries estimates about 1,600 Hawaiian monk seals, and up to 30 percent of those alive today are alive because of direct recovery work.'
        page = page.replace(old_desc, E(p['blurb']))
        page = page.replace('content="Hawaiian, Monk, Seal, Recovery, NOAA, Fisheries, estimates, about"',
                            f'content="{E(p["title"])}, Saving Planets"')
        page = page.replace('https://www.savingplanets.com/assets/Hawaiian_Monk_Seal_NOAA.jpg',
                            'https://www.savingplanets.com/' + p['img'])
        page = page.replace('content="750"', f'content="{p["w"]}"')
        page = page.replace('content="500"', f'content="{p["h"]}"')
        page = page.replace('A Hawaiian monk seal and her pup resting on a sandy beach beside the ocean', E(p['alt']))
        page = page.replace('content="ocean"', f'content="{p["hub"]}"')
        page = page.replace('content="agency"', f'content="{p["klass"]}"')
        page = page.replace('content="2026-11-09"', f'content="{TODAY}"')
        page = page.replace('hp-hawaiian-monk-seal-recovery toc-sub hawaiian-monk-seal-recovery-page',
                            f'hp-{p["file"][:-5].lower().replace("_", "-")} toc-sub')
        page = page.replace('data-glass="ocean"', f'data-glass="{p["glass"]}"')
        page = page.replace('data-glass-tint="water"', f'data-glass-tint="{p["tint"]}"')
        # Article JSON-LD headline still says the old name if the script used it. Replace leftover name.
        page = page.replace(old_title, p['title'])
        page = page.replace('Hawaiian%20Monk%20Seal%20Recovery', urllib.parse.quote(p['title'], safe=''))
        cites = ','.join('{"@type": "CreativeWork", "url": "%s"}' % u for n, u in p['sources'])
        page = re.sub(r'"citation": \[.*?\]', '"citation": [' + cites + ']', page, count=1, flags=re.S)
        # hreflang for the five languages (the shell only had en and x-default)
        if 'hreflang="fr"' not in page:
            block = '\n'.join(
                f'<link rel="alternate" hreflang="{lang}" href="https://www.savingplanets.com/{lang}/{p["file"]}">'
                for lang in LANGS)
            page = page.replace(
                f'<link rel="alternate" hreflang="x-default" href="https://www.savingplanets.com/{p["file"]}">',
                block + '\n<link rel="alternate" hreflang="x-default" href="https://www.savingplanets.com/' + p['file'] + '">')
        # Teacher questions: use the auto-translated patterns.
        page = page.replace(
            'What is ' + p['title'] + ', and what problem does it work on?',
            'What is ' + p['title'] + ', and what problem does it help solve?')
        page = page.replace(
            'Which number on this page surprised you, and which source supports it?',
            'Who is behind ' + p['title'] + ', and where does the work happen?')
        page = page.replace(
            'How does this work help people, and how does it help nature?',
            'How does ' + p['title'] + ' help both people and nature? Use one fact from this page.')
        # Cite lines
        page = page.replace(
            f'Saving Planets. (2026). {p["title"]}. https://www.savingplanets.com/{p["file"]}',
            f'Saving Planets. (2026). {E(p["title"])}. https://www.savingplanets.com/{p["file"]}')
        open(p['file'], 'w', encoding='utf8').write(page)
        print('wrote', p['file'], 'leftover monk', page.lower().count('monk'))

def card_sol(p, lang):
    ui = UI[lang]
    pre = '' if lang == 'en' else '../'
    title = TR.get(p['title'], {}).get(lang, p['title']) if lang != 'en' else p['title']
    blurb = TR.get(p['blurb'], {}).get(lang, p['blurb']) if lang != 'en' else p['blurb']
    alt = TR.get(p['alt'], {}).get(lang, p['alt']) if lang != 'en' else p['alt']
    credit = TR.get(p['credit'], {}).get(lang, p['credit']) if lang != 'en' else p['credit']
    return (f'<article class="card sol-card" data-url="{p["file"]}" data-new="{TODAY}" data-status="active" data-region="{p["region"]}" data-grades="6-8">'
            f'<div class="image-container"><a class="photo-link" href="{p["file"]}"><img width="{p["w"]}" height="{p["h"]}" src="{pre}{p["img"]}" alt="{E(alt)}" loading="lazy" decoding="async"></a></div>'
            f'<p class="photo-credit sol-credit"><span>{ui["image"]}</span> <bdi>{E(credit)}</bdi></p>'
            f'<p class="sol-badges"><span class="status-badge status-new" data-new-until="{UNTIL}" style="{BADGE}">{ui["new"]}</span></p>'
            f'<h3><a href="{p["file"]}">{E(title)}</a></h3><p class="sol-desc"><span>{E(blurb)}</span></p></article>')

def card_hub(p, lang):
    ui = UI[lang]
    pre = '' if lang == 'en' else '../'
    title = TR.get(p['title'], {}).get(lang, p['title']) if lang != 'en' else p['title']
    blurb = TR.get(p['blurb'], {}).get(lang, p['blurb']) if lang != 'en' else p['blurb']
    alt = TR.get(p['alt'], {}).get(lang, p['alt']) if lang != 'en' else p['alt']
    hub = HUBNAME[p['hub']][lang]
    return (f'<article class="card"><div class="image-container"><a class="photo-link" href="{p["file"]}"><img src="{pre}{p["img"]}" alt="{E(alt)}" width="{p["w"]}" height="{p["h"]}" loading="lazy" decoding="async"></a></div>'
            f'<p class="sol-badges"><span class="status-badge status-active">{ui["active"]}</span>'
            f'<span class="status-badge status-new" data-new-until="{UNTIL}" style="{BADGE}">{ui["new"]}</span>'
            f'<span class="hub-tag"><span aria-hidden="true">{EMOJI[p["hub"]]}</span> {E(hub)}</span></p>'
            f'<h3><a href="{p["file"]}">{E(title)}</a></h3><p class="card-blurb">{E(blurb)}</p></article>')

def card_ways(p, lang):
    title = TR.get(p['title'], {}).get(lang, p['title']) if lang != 'en' else p['title']
    blurb = TR.get(p['ways'], {}).get(lang, p['ways']) if lang != 'en' else p['ways']
    btn = TR.get(p['button'], {}).get(lang, p['button']) if lang != 'en' else p['button']
    return (f'<li class="wh-card"><h3>{E(title)}</h3><p>{E(blurb)}</p>'
            f'<a class="wh-s" href="{p["file"]}">{E(title)}</a>'
            f'<a class="btn help-btn wh-c" href="{E(p["official"])}" target="_blank" rel="noopener">{E(btn)}'
            f'<span class="sr-only"> – {E(title)}</span></a></li>')

def insert_before(html, anchor_file, snippet, marker):
    if f'href="{marker}"' in html or f'data-url="{marker}"' in html:
        return html
    i = html.find(f'href="{anchor_file}"')
    if i < 0:
        raise SystemExit('anchor missing ' + anchor_file)
    j = html.rfind('<article', 0, i)
    if j < 0:
        raise SystemExit('article missing before ' + anchor_file)
    return html[:j] + snippet + html[j:]

def bump_sol_c(html, hub_id, new_n):
    return re.sub(r'(href="#' + hub_id + r'">[^<]*<span class="sol-c">)\d+(</span>)',
                  lambda m: m.group(1) + str(new_n) + m.group(2), html, count=1)

def add_ways(html, hub_id, snippet, add_n, marker):
    if f'href="{marker}"' in html[html.find(f'id="{hub_id}"'):html.find(f'id="{hub_id}"') + 80000]:
        return html
    i = html.find(f'id="{hub_id}"')
    if i < 0:
        raise SystemExit('ways hub missing ' + hub_id)
    j = html.find('<ul class="wh-grid">', i)
    chunk = html[i:j]
    chunk2, n = re.subn(r'(<span class="wh-n">)(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + add_n), chunk, count=1)
    if n != 1:
        raise SystemExit('wh-n missing ' + hub_id)
    html = html[:i] + chunk2 + html[j:]
    j = html.find('<ul class="wh-grid">', i)
    k = j + len('<ul class="wh-grid">')
    return html[:k] + snippet + html[k:]

HUB_ID = {'lakes': 'hub-lakes', 'rivers': 'hub-rivers', 'planetary-defense': 'hub-planetary-defense'}
VOL_ID = {'lakes': 'vol-hub-lakes', 'rivers': 'vol-hub-rivers', 'planetary-defense': 'vol-hub-planetary-defense'}
NEW_COUNTS = {'lakes': 19, 'rivers': 27, 'planetary-defense': 16}  # 17+2, 25+2, 15+1
TOTAL = 292  # 287 listing cards plus these five

def wire_listings():
    by_hub = {}
    for p in PAGES:
        by_hub.setdefault(p['hub'], []).append(p)
    for lang in [None] + LANGS:
        pref = '' if lang is None else lang + '/'
        code = 'en' if lang is None else lang
        # Solutions.html
        path = pref + 'Solutions.html'
        s = open(path, encoding='utf8').read()
        for p in PAGES:
            s = insert_before(s, p['anchor'], card_sol(p, code), p['file'])
        for hub, n in NEW_COUNTS.items():
            s = bump_sol_c(s, HUB_ID[hub], n)
        s = re.sub(r'(?<![\d,])286(?!\d)', str(TOTAL), s)
        open(path, 'w', encoding='utf8').write(s)
        print('solutions', path)
        # hub pages
        for hub, items in by_hub.items():
            hf = {'lakes': 'Lakes.html', 'rivers': 'Rivers.html', 'planetary-defense': 'Planetary_Defense.html'}[hub]
            path = pref + hf
            s = open(path, encoding='utf8').read()
            for p in items:
                s = insert_before(s, p['anchor'], card_hub(p, code), p['file'])
            open(path, 'w', encoding='utf8').write(s)
            print('hub', path)
        # ways
        path = pref + 'Ways_to_Help.html'
        s = open(path, encoding='utf8').read()
        for hub, items in by_hub.items():
            snip = ''.join(card_ways(p, code) for p in items if f'href="{p["file"]}"' not in s)
            if snip:
                s = add_ways(s, VOL_ID[hub], snip, snip.count('class="wh-card"'), items[0]['file'])
        open(path, 'w', encoding='utf8').write(s)
        print('ways', path)

def wire_counts_and_home():
    # homepage counter + new strip
    for lang in [None] + LANGS:
        pref = '' if lang is None else lang + '/'
        code = 'en' if lang is None else lang
        path = pref + 'index.html'
        s = open(path, encoding='utf8').read()
        s = s.replace('class="imp-num">286<', f'class="imp-num">{TOTAL}<')
        s = re.sub(r'(?<![\d,])286(?!\d)', str(TOTAL), s, count=3)
        h, summary, all_, date, _sols = STRIP[code]
        pre = '' if lang is None else '../'
        items = ''.join(
            f'<li><time datetime="{TODAY}">{date}</time> <a href="{pre}{p["file"]}">{E(TR.get(p["title"], {}).get(code, p["title"]) if code != "en" else p["title"])}</a></li>'
            for p in PAGES)
        arrow = '←' if code in ('ar', 'he') else '→'
        strip = (f'<!-- NEW-STRIP:START --><section class="new-strip" aria-labelledby="new-h"><h2 id="new-h">🆕 {E(h)}</h2>'
                 f'<p class="ns-sum">{E(summary.format(n=len(PAGES), t=TOTAL))}</p><ul class="ns-list">{items}</ul>'
                 f'<p class="ns-all"><a href="{pre}Changelog.html">{E(all_)} {arrow}</a></p></section><!-- NEW-STRIP:END -->')
        anchor = '<section class="news-briefs"'
        if anchor not in s:
            print('no news-briefs', path)
        else:
            s = s.replace(anchor, strip + anchor, 1)
        open(path, 'w', encoding='utf8').write(s)
        # changelog day
        cpath = pref + 'Changelog.html'
        if os.path.exists(cpath):
            c = open(cpath, encoding='utf8').read()
            _h, _sum, _all, date, sols = STRIP[code]
            lis = ''.join(f'<li><a href="{pre}{p["file"]}">{E(TR.get(p["title"], {}).get(code, p["title"]) if code != "en" else p["title"])}</a></li>' for p in PAGES)
            block = f'<section class="cl-day"><h2><time datetime="{TODAY}">{E(date)}</time></h2><h3>{E(sols)} ({len(PAGES)})</h3><ul>{lis}</ul></section>'
            mark = '</p><section class="cl-day">'
            if mark in c and f'datetime="{TODAY}"' not in c:
                c = c.replace(mark, '</p>' + block + '<section class="cl-day">', 1)
                open(cpath, 'w', encoding='utf8').write(c)

def wire_data():
    # solution-added
    added = json.load(open('assets/data/solution-added.json', encoding='utf8'))
    for p in PAGES:
        added[p['file']] = TODAY
    json.dump(added, open('assets/data/solution-added.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    # solutions.json surgical
    s = open('assets/data/solutions.json', encoding='utf8').read()
    s = s.replace('"solutions": 286,', f'"solutions": {TOTAL},', 1)
    s = s.replace('"taggedSolutions": 286', f'"taggedSolutions": {TOTAL}', 1)
    s = s.replace('"name": "Lakes",\n   "solutions": 17,', '"name": "Lakes",\n   "solutions": 19,')
    s = s.replace('"name": "Rivers",\n   "solutions": 25,', '"name": "Rivers",\n   "solutions": 27,')
    s = s.replace('"name": "Planetary Defense",\n   "solutions": 15,', '"name": "Planetary Defense",\n   "solutions": 16,')
    pairs = [
        ('Hayabusa2_Torifune.html', 'DART.html', 'DART (NASA)'),
        ('Restoring_the_Lake_Depths.html', 'Onondaga_Lake_Cleanup.html', 'Onondaga Lake Cleanup'),
        ('Lake_Plastic_Recovery.html', 'Lake_Geneva_CIPEL.html', 'Lake Geneva Phosphorus Cleanup'),
        ('FreshWater_Watch.html', 'Emscher_River_Restoration.html', 'Emscher River Restoration'),
        ('Kissimmee_River_Restoration.html', 'Hudson_River_PCB_Cleanup.html', 'Hudson River PCB Cleanup'),
    ]
    for anchor, href, name in pairs:
        if '"href": "%s"' % href in s:
            continue
        needle = '    {\n     "href": "%s",' % anchor
        ins = '    {\n     "href": "%s",\n     "name": "%s"\n    },\n    {\n     "href": "%s",' % (href, name, anchor)
        if s.count(needle) == 0:
            raise SystemExit('menu anchor missing ' + anchor)
        s = s.replace(needle, ins)
    objs = []
    for p in PAGES:
        objs.append('''  {
   "url": "%s",
   "title": "%s",
   "category": "%s",
   "type": "solution",
   "classification": "%s",
   "status": "active",
   "stats": [],
   "missions": [],
   "added": "%s"
  }''' % (p['file'], p['title'], p['hub'], p['klass'], TODAY))
    if '"url": "DART.html"' not in s:
        s = s.replace('''   "missions": []
  }
 ]
}''', '''   "missions": []
  },
''' + ',\n'.join(objs) + '''
 ]
}''')
    json.loads(s)  # validate
    open('assets/data/solutions.json', 'w', encoding='utf8').write(s)
    # pages lists
    for fn in ('i18n/pages.txt', 'i18n/he-pages.txt'):
        lines = open(fn, encoding='utf8').read().splitlines()
        for p in PAGES:
            if p['file'] not in lines:
                lines.append(p['file'])
        open(fn, 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    # sitemap
    block_src = open('sitemap-en.xml', encoding='utf8').read()
    i = block_src.find('<url><loc>https://www.savingplanets.com/Lake_Washington_Cleanup.html</loc>')
    j = block_src.find('</url>', i) + len('</url>')
    sample = block_src[i:j]
    for lang, prefix in [('en', ''), ('fr', 'fr/'), ('es', 'es/'), ('ar', 'ar/'), ('it', 'it/'), ('he', 'he/')]:
        path = f'sitemap-{lang}.xml'
        sm = open(path, encoding='utf8').read()
        for p in PAGES:
            if p['file'] in sm:
                continue
            entry = sample.replace('Lake_Washington_Cleanup.html', p['file']).replace('2026-11-19', TODAY)
            if lang != 'en':
                # the sample's loc is the English URL; point loc at this language
                entry = entry.replace(
                    f'<loc>https://www.savingplanets.com/{p["file"]}</loc>',
                    f'<loc>https://www.savingplanets.com/{prefix}{p["file"]}</loc>', 1)
            sm = sm.replace('</urlset>', '  ' + entry + '\n</urlset>')
        open(path, 'w', encoding='utf8').write(sm)
    # glossary
    g = json.load(open('assets/data/glossary.json', encoding='utf8'))
    g['terms'].append({
        'id': 'kinetic-impactor',
        'en': {'term': 'Kinetic impactor', 'match': ['kinetic impactor'], 'def': 'A spacecraft that hits an asteroid on purpose to change the asteroid\'s path.'},
        'fr': {'term': 'Impacteur cinétique', 'match': ['impacteur cinétique'], 'def': 'Une sonde qui frappe un astéroïde volontairement pour changer sa trajectoire.'},
        'es': {'term': 'Impactador cinético', 'match': ['impactador cinético'], 'def': 'Una nave que choca a propósito con un asteroide para cambiar su trayectoria.'},
        'ar': {'term': 'مصادم حركي', 'match': ['مصادم حركي'], 'def': 'مركبة فضائية تصطدم بكويكب عن قصد لتغيير مساره.'},
        'it': {'term': 'Impattatore cinetico', 'match': ['impattatore cinetico'], 'def': 'Una sonda che colpisce di proposito un asteroide per cambiarne la traiettoria.'},
        'he': {'term': 'פגיעה קינטית', 'match': ['פגיעה קינטית'], 'def': 'חללית שפוגעת באסטרואיד בכוונה כדי לשנות את מסלולו.'},
        'source': NASA_CONFIRM,
    })
    g['terms'].append({
        'id': 'superfund',
        'en': {'term': 'Superfund', 'match': ['Superfund'], 'def': 'The U.S. program that cleans the country\'s most contaminated sites and holds polluters to the cleanup.'},
        'fr': {'term': 'Superfund', 'match': ['Superfund'], 'def': 'Le programme américain qui nettoie les sites les plus contaminés du pays et demande des comptes aux pollueurs.'},
        'es': {'term': 'Superfund', 'match': ['Superfund'], 'def': 'El programa de Estados Unidos que limpia los sitios más contaminados del país y exige cuentas a quien contaminó.'},
        'ar': {'term': 'سوبرفَند', 'match': ['سوبرفَند', 'Superfund'], 'def': 'البرنامج الأمريكي الذي ينظّف أكثر المواقع تلوثًا في البلاد ويُلزم الملوّثين بالتنظيف.'},
        'it': {'term': 'Superfund', 'match': ['Superfund'], 'def': 'Il programma degli Stati Uniti che ripulisce i siti più contaminati del paese e chiama i responsabili a risponderne.'},
        'he': {'term': 'סופרפאנד', 'match': ['סופרפאנד', 'Superfund'], 'def': 'התוכנית של ארצות הברית שמנקה את האתרים המזוהמים ביותר במדינה ומחייבת את המזהמים לנקות.'},
        'source': 'https://www.epa.gov/superfund',
    })
    g['terms'].append({
        'id': 'pcb',
        'en': {'term': 'PCBs', 'match': ['PCBs', 'PCB'], 'def': 'A group of industrial chemicals that stay in water, mud, and animals for a long time.'},
        'fr': {'term': 'PCB', 'match': ['PCB'], 'def': 'Une famille de produits chimiques industriels qui restent longtemps dans l’eau, la vase et les animaux.'},
        'es': {'term': 'PCB', 'match': ['PCB'], 'def': 'Un grupo de sustancias industriales que permanecen mucho tiempo en el agua, el lodo y los animales.'},
        'ar': {'term': 'مركبات PCB', 'match': ['مركبات PCB', 'PCB'], 'def': 'مجموعة من المواد الكيميائية الصناعية تبقى طويلًا في الماء والطين والحيوانات.'},
        'it': {'term': 'PCB', 'match': ['PCB'], 'def': 'Un gruppo di sostanze industriali che restano a lungo nell’acqua, nel fango e negli animali.'},
        'he': {'term': 'PCB', 'match': ['PCB'], 'def': 'קבוצה של חומרים תעשייתיים שנשארים זמן רב במים, בבוץ ובבעלי חיים.'},
        'source': EPA_HUDSON,
    })
    json.dump(g, open('assets/data/glossary.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dumps  # keep import used

def merge_i18n():
    import importlib.util
    spec = importlib.util.spec_from_file_location('tr1123', 'scripts/batch-1123-tr.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for en, tr in mod.EXTRA.items():
        TR.setdefault(en, {}).update(tr)
    # shared
    for key in ('every', 'showcase', 'nodeonate'):
        en = S[key]['en']
        TR[en] = {lang: S[key][lang] for lang in LANGS}
    # buttons and credits and alts and labels and paragraphs: load optional json overlay
    if os.path.exists(BATCH_TR_PATH):
        extra = json.load(open(BATCH_TR_PATH, encoding='utf8'))
        for en, tr in extra.items():
            TR.setdefault(en, {}).update(tr)
    missing = [s for p in PAGES for s in collect_strings(p) if s not in TR]
    # Also translate buttons that are not the blurb
    for p in PAGES:
        for s in (p['button'], p['credit'], p['alt'], p['label'], p['help'], p['impact'], p['people'], p['nature'], p['ways']):
            if s not in TR and s not in missing:
                missing.append(s)
    if missing:
        json.dump({s: {} for s in missing}, open('/tmp/batch-1123-missing.json', 'w', encoding='utf8'), ensure_ascii=False, indent=2)
        print('MISSING translations', len(missing))
        for s in missing:
            print(' -', s[:110])
    for lang in LANGS:
        path = f'i18n/{lang}.json'
        data = json.load(open(path, encoding='utf8'))
        n = 0
        for en, tr in TR.items():
            if lang in tr and tr[lang] and data.get(en) != tr[lang]:
                data[en] = tr[lang]
                n += 1
        # cite lines
        for p in PAGES:
            title = TR.get(p['title'], {}).get(lang, p['title'])
            en_apa = f'Saving Planets. (2026). {p["title"]}. https://www.savingplanets.com/{p["file"]}'
            data[en_apa] = f'Saving Planets. (2026). {title}. https://www.savingplanets.com/{lang}/{p["file"]}'
            en_mla = f'"{p["title"]}." Saving Planets, https://www.savingplanets.com/{p["file"]}.'
            q = f'« {title} »' if lang == 'fr' else f'"{title}"'
            data[en_mla] = f'{q}. Saving Planets{"،" if lang == "ar" else ","} https://www.savingplanets.com/{lang}/{p["file"]}.'
        text = json.dumps(data, ensure_ascii=False, indent=0) + '\n'
        open(path, 'w', encoding='utf8').write(text)
        print(lang, 'i18n keys added/updated', n)

def translate():
    import importlib.util
    spec = importlib.util.spec_from_file_location('i18n_build', 'scripts/i18n-build.py')
    i18n_build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(i18n_build)
    i18n_build.PAGES = [l.strip() for l in open('i18n/pages.txt', encoding='utf8') if l.strip() and not l.startswith('#')]
    files = [p['file'] for p in PAGES]
    for lang in LANGS:
        m = json.load(open(f'i18n/{lang}.json', encoding='utf8'))
        i18n_build.CUR_PAGES = i18n_build.L10N.pages_for(lang, i18n_build.PAGES)
        for f in files:
            i18n_build.build(f, lang, m)
        print('built', lang)

def main():
    write_english()
    merge_i18n()
    translate()
    wire_listings()
    wire_counts_and_home()
    wire_data()
    print('done', TOTAL)

if __name__ == '__main__':
    main()
