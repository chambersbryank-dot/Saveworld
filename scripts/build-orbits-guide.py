#!/usr/bin/env python3
"""Replace the body of Orbits_Guide.html with a levelled course. Does not rewrite nav or Learn.html."""
import html, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']

def E(s):
    return html.escape(s, quote=True)

def video(yt, title, cap, watch):
    return (f'<figure class="og-vid"><button type="button" class="ytf" data-yt="{yt}" data-title="{E(title)}">{E(title)}</button>'
            f'<a class="ytf-fallback" href="https://www.youtube.com/watch?v={yt}">{E(watch)}</a>'
            f'<figcaption>{cap}</figcaption></figure>')

def qa(show, q, a):
    return (f'<div class="lbox"><p>{q}</p><details class="oc-ans"><summary>{E(show)}</summary>'
            f'<p class="oc-key">{a}</p></details></div>')

# Shared rounded results. fr/es/it use a decimal comma.
NUM = {
 'en': dict(v300='7.73', v5='5', v9='9', apo='7 718', esc300='10.93', esc0='11.18',
            issV='7.67', issT='92.6', g='8.68', g0='9.80', pct='88.5', day='15.6',
            l9v='7.50', l9t='98.9', gpsV='3.87', gpsT='11.98', geoV='3.07', geoA='35 786',
            dv1='2.43', dv2='1.47', dv='3.89', tof='5.28', p1='3.80', p2='1.51',
            bi='4.06', hoh='4.13', d1='8.1', d2='1.1', eps='−29.40'),
}
for lang in ('ar', 'he'):
    NUM[lang] = dict(NUM['en'])
for lang in ('fr', 'es', 'it'):
    NUM[lang] = {k: v.replace('.', ',') for k, v in NUM['en'].items()}

S = {
'kicker': {
 'en': 'A course from a first picture of an orbit to Kepler, transfers and mission design.',
 'fr': 'Un cours, du premier dessin d’une orbite jusqu’à Kepler, aux transferts et au dessin de mission.',
 'es': 'Un curso desde la primera imagen de una órbita hasta Kepler, las transferencias y el diseño de la misión.',
 'ar': 'مقرر من أول صورة للمدار حتى قوانين كبلر والانتقالات وتصميم المهمة.',
 'it': 'Un corso dal primo disegno di un’orbita fino a Keplero, ai trasferimenti e al progetto di missione.',
 'he': 'קורס מהתמונה הראשונה של מסלול עד קפלר, מעברים ותכנון משימה.',
},
'desc': {
 'en': 'Orbits from a first picture to university mission design: real speeds for the space station, GPS and GEO, a Blue Marble sandbox, and a printable answer key.',
 'fr': 'Les orbites, du premier dessin jusqu’au dessin de mission : vitesses réelles pour la station, le GPS et l’orbite géostationnaire, un bac à sable Blue Marble et un corrigé à imprimer.',
 'es': 'Órbitas desde la primera imagen hasta el diseño de una misión: velocidades reales de la estación, el GPS y la GEO, un banco de pruebas Blue Marble y una clave para imprimir.',
 'ar': 'المدارات من الصورة الأولى حتى تصميم المهمة: سرعات حقيقية للمحطة وGPS والمدار الثابت، وتجربة Blue Marble، ومفتاح إجابات للطباعة.',
 'it': 'Orbite dal primo disegno al progetto di missione: velocità reali per la stazione, il GPS e l’orbita geostazionaria, una sandbox Blue Marble e le soluzioni da stampare.',
 'he': 'מסלולים מהתמונה הראשונה עד תכנון משימה: מהירויות אמיתיות לתחנה, ל-GPS ולמסלול גיאוסטציונרי, ארגז חול של Blue Marble, ומפתח תשובות להדפסה.',
},
'guideName': {
 'en': 'Orbits course', 'fr': 'Cours sur les orbites', 'es': 'Curso de órbitas',
 'ar': 'مقرر المدارات', 'it': 'Corso sulle orbite', 'he': 'קורס מסלולים',
},
}

def n(lang, key):
    return NUM[lang][key]

def body(lang):
    N = lambda k: n(lang, k)
    T = {
'en': dict(
 show='Show the answer', outcomes='What you can do after this part', worked='Worked example',
 check='Misconception check', practice='Practice', planet='How this helps the planet',
 sources='Sources for the numbers',
 intro='Orbits 101 stays open. Then pick Kids, Middle school, High school, or University. The same ideas return in sharper form. Every speed below is a two-body circle or transfer from μ = 398 600.4418 km³/s² and the WGS-84 radius 6 378.137 km, unless a NASA, GPS.gov, USGS, or STScI page is named as the source.',
 links='See the same story as a launch in the <a href="Orbit_Lab.html">Orbit Lab</a>, the algebra in <a href="Orbit_Math.html">Orbit Math</a>, the university course <a href="Orbital_Mechanics.html">Orbital Mechanics</a>, and <a href="Earth_Observation.html">Earth observation</a>.',
 h101='Orbits 101',
 p101=f'An orbit is a fall that keeps missing the ground. Gravity stays on. At the International Space Station’s altitude, about 400 km, the pull is still {N("g")} m/s², which is {N("pct")}% of the {N("g0")} m/s² you get from μ/R² at the surface. The circular speed there is {N("issV")} km/s, and one loop takes {N("issT")} minutes. A day of 1 440 minutes holds {N("day")} of those loops. NASA describes about 16 sunrises a day on the station.',
 m101q='“There is no gravity in space.”',
 m101a='If gravity were zero, the station would fly in a straight line and leave. It stays because gravity bends that straight line into a closed curve. NASA classroom notes put the pull at station altitude near 90% of the surface value. This page’s two-body number is 88.5%.',
 q101='The station is 400 km up and suddenly its sideways speed becomes zero. What happens?',
 a101='It falls. Height is not what holds it up. Without the sideways speed, 400 km is only a long drop.',
 e101='Weather, ice, and forest satellites stay up for the same reason, so they can look at the same places again and again.',
 hk='Kids',
 ok='Say what an orbit is. Name the sideways speed, not the height, as the thing that keeps a satellite up. Name one way a satellite helps people on Earth.',
 pk='Newton’s picture, told without a cartoon Earth: a ball thrown from a high mountain. Thrown gently, it lands nearby. Thrown harder, it lands farther away. Thrown at circular speed, the ground curves away as fast as the ball falls, so the ball keeps going around. Thrown faster than escape speed, it leaves and does not come back.',
 wk=f'From 300 km up, the radius is 6 678 km. Circular speed is √(μ/r) = {N("v300")} km/s. A sideways throw at {N("v5")} km/s falls back, because the low point of that path is inside the Earth. A throw at {N("v9")} km/s makes a long oval whose high point is about {N("apo")} km above the ground. Escape speed from 300 km is {N("esc300")} km/s. From the surface, ignoring air, it is {N("esc0")} km/s.',
 mkq='“The engine must stay on, or the satellite falls.”',
 mka='The engine is for getting the sideways speed. After the last cutoff, gravity does the curving. The engine comes on again only for a change of orbit, or for a reboost when thin air has slowed the craft.',
 qk='Which is an orbit: hovering with the engine pushing up, or coasting with the engine off after you already have the sideways speed?',
 ak='Coasting with the engine off. Hovering spends fuel to fight gravity. An orbit spends the fuel once, to get the speed, and then falls around the Earth.',
 ek='A weather satellite watches clouds so people can warn a town before a storm arrives.',
 vk='NASA Johnson’s STEMonstrations: Newton’s first law. A force changes motion. Staying in orbit does not need a force along the track. Credit: NASA Johnson.',
 hm='Middle school',
 om='Use gravity as the force that keeps a satellite falling around Earth. Compare the station, a GPS satellite, and geostationary orbit. Explain why a higher circle is slower.',
 pm=f'This part lines up with the gravity-and-motion idea in NGSS MS-ESS1-2, using Earth satellites as the near example. The acceleration at distance r from Earth’s center is μ/r². At the surface that is {N("g0")} m/s². At 400 km it is {N("g")} m/s². Farther out, the pull is weaker, so the speed that matches a circle is smaller, and the path is longer, so the period is much longer.',
 wm=f'The station at 400 km: {N("issV")} km/s, {N("issT")} min. Landsat 9 flies near 705 km at an inclination of 98.2°, with a period of about 99 minutes (NASA and USGS). A two-body circle at 705 km gives {N("l9v")} km/s and {N("l9t")} min. GPS satellites fly near 20 200 km, a period of about 12 hours, and an inclination of 55° (GPS.gov). The circle at 20 200 km gives {N("gpsV")} km/s and {N("gpsT")} h. Geostationary radius is 42 164 km, altitude {N("geoA")} km, speed {N("geoV")} km/s, period one sidereal day (86 164 s).',
 mmq='“Higher means faster.”',
 mma='GPS is much higher than the station and much slower: about 3.87 km/s against 7.67 km/s. The higher circle is a bigger path with a weaker pull.',
 qm='Why does a satellite in a higher circle both move slower and take longer to go around?',
 am='Gravity is weaker farther from Earth, so the matching circular speed is smaller. The path is also longer. Both effects stretch the period.',
 em='Landsat watches forests, farms, and water. Its near-polar, sun-synchronous tilt passes over the ground at a similar local time, which makes pictures from different years easier to compare.',
 vm='NASA eClips, archived: Real World — Keeping the International Space Station in Orbit. Gravity still pulls. Thin air drags the station down, and crews reboost it. Credit: NASA eClips archive.',
 hh='High school',
 oh='State Kepler’s three laws. Compute a circular speed and a period. Compute one Hohmann transfer. Connect the pull to g = μ/r².',
 ph='Kepler’s first law: ellipses, with the central body at one focus. For these satellites the focus is Earth’s center. Second law: equal areas in equal times, so the craft moves faster when it is closer. Third law: T² is proportional to a³, or T = 2π √(a³/μ). The standards this part serves are HS-ESS1-4 and HS-PS2-4, and the orbit portion of AP Physics C Mechanics. PhET’s Gravity and Orbits simulation is a useful extra model; this page links it and does not embed it.',
 wh=f'Hohmann transfer from 300 km to geostationary orbit. r₁ = 6 678 km, r₂ = 42 164 km, transfer semi-major axis = 24 421 km. Circular speed on the low orbit is {N("v300")} km/s. The burn raises speed to 10.15 km/s, so Δv₁ = {N("dv1")} km/s. At the high end the transfer speed is 1.61 km/s and circular speed is {N("geoV")} km/s, so Δv₂ = {N("dv2")} km/s. The total is {N("dv")} km/s. The coast takes {N("tof")} hours. A plane change of 28.5° costs {N("p1")} km/s at 300 km and {N("p2")} km/s at geostationary speed, because Δv = 2 v sin(Δi/2). The lowest inclination a launch can reach, without a later plane change, is the latitude of the launch site. Do the turn where the craft is slow.',
 hhq='“Weightlessness means gravity is gone, and orbits are circles.”',
 hha='Most orbits are ellipses. You feel weightless because you and the spacecraft fall together. A scale in free fall reads zero even though μ/r² is still there.',
 qh=f'A craft at 300 km has a sideways speed of {N("v9")} km/s. Circle, ellipse, or escape?',
 ah=f'An ellipse. Circular speed there is {N("v300")} km/s and escape speed is {N("esc300")} km/s. The high point of this ellipse is about {N("apo")} km above the ground.',
 eh='A sun-synchronous orbit keeps Earth-observing cameras in similar sunlight from pass to pass. ESA’s Cheops uses a related polar orbit, near 700 km, so its view of stars stays stable.',
 vh1='Open Yale PHYS 200, lecture 7, Kepler’s laws. The lecture is CC BY-NC-SA. Credit: YaleCourses.',
 vh2='ESA: Cheops observing in space. A sun-synchronous orbit near 700 km. Credit: European Space Agency.',
 hu='University',
 ou='Write the two-body equation and the conic from specific energy. Name the classical elements. Use vis-viva. Compare Hohmann and bi-elliptic transfers. Estimate a plane change. Say what J₂ and drag do. Place the Lagrange points and say what a patched-conic plan is.',
 pu='The two-body equation is r̈ = −μ r / r³. Specific energy ε = v²/2 − μ/r. A circle or ellipse has ε &lt; 0, a parabola ε = 0, a hyperbola ε &gt; 0. Vis-viva is v = √(μ (2/r − 1/a)). The classical elements are a, e, i, Ω, ω, and a position angle (true anomaly or mean anomaly). J₂ for Earth is 1.0826×10⁻³. It makes the node and the argument of perigee drift, and sun-synchronous designers use that drift. Drag at station altitude removes energy, so the low point sinks until a reboost.',
 wu=f'From a radius r to 20r, a Hohmann transfer costs {N("hoh")} km/s and the coast is about {N("d2")} days. A bi-elliptic transfer that climbs out to 40r, then comes down to 20r, costs {N("bi")} km/s and the coasts add up to about {N("d1")} days. You save a little speed and spend a lot of time. It wins only for a large radius ratio. The circular restricted three-body problem has five Lagrange points. A Hill estimate puts the Sun–Earth L2 point about 1.50 million km from Earth, using GM☉ = 1.327 124 400 18×10¹¹ km³/s² and 1 AU = 149 597 870.7 km. STScI: JWST orbits around Sun–Earth L2, about 1.5 million km from Earth. It does not sit on the point. Its distance from L2 runs from 250 000 km to 832 000 km, the period is about six months, and station-keeping burns are scheduled about every 42 days. A patched-conic sketch uses Earth’s μ near Earth and the Sun’s μ farther out. The sphere of influence is the patch. It is a plan, not an n-body integration.',
 muq='“A bi-elliptic transfer is always cheaper, and L2 is a place you can park with the engines off.”',
 mua='The bi-elliptic transfer saves speed only for a large jump in radius, and it costs days of coasting. Sun–Earth L2 is unstable along the Sun–Earth line, which is why JWST keeps doing station-keeping.',
 qu='Compute the specific energy of the station’s circle at 400 km.',
 au=f'ε = −μ/(2r) = {N("eps")} km²/s². Negative energy means the path is bound.',
 eu='Drag brings low-orbit debris down, so operators plan an end of life. Debris near geostationary orbit stays for a very long time, which is why graveyard orbits exist. Earth observation needs the orbit and a sky that is not full of fragments.',
 vu1='ESA: Space debris — a journey to Earth. Orbital regimes and what happens to debris. Credit: European Space Agency.',
 vu2='ESA: Gaia, launch to orbit. The transfer toward a Sun–Earth L2 Lissajous orbit. Credit: European Space Agency.',
 vu3='MIT OpenCourseWare 16.346, Fall 2008: A Funny Thing Happened on the Way to the Moon. This lecture is a history of Apollo guidance. It is not a derivation of the Hohmann transfer. Credit: MIT OpenCourseWare.',
 sand='Try three pictures',
 slead='The globe is a NASA Blue Marble photograph, drawn to scale with the path. The 5, 7.73, 9, and 11.2 km/s buttons all start 300 km up, moving sideways. 11.2 km/s is above escape speed at that altitude, so the path leaves.',
 cannon='Launch speed', area='Equal areas', hoh='Hohmann',
 speed='Sideways speed, km/s', outer='Outer altitude, km',
 play='Play', pause='Pause',
 fall='falls back', circle='circle', ellipse='ellipse', leave='leaves Earth',
 circ='circular', esc='escape',
 areaRead='The two shaded wedges are equal times, and so equal areas. Near the low point the craft sweeps a wider angle. Near the high point it sweeps a narrow one.',
 phet='PhET Gravity and Orbits (linked, not embedded)',
),
    }
    # The other languages are full translations of the same claims.
    T['fr'] = dict(T['en'])
    T['es'] = dict(T['en'])
    T['ar'] = dict(T['en'])
    T['it'] = dict(T['en'])
    T['he'] = dict(T['en'])
    # Fill translations below by key groups so a missing key cannot silently stay English
    # unless it is a proper name we chose to keep.
    TR = translations()
    for lg, pack in TR.items():
        T[lg].update(pack)
    for lg in ('fr', 'es', 'ar', 'it', 'he'):
        for key in PROSE:
            if T[lg].get(key) == T['en'].get(key):
                raise SystemExit(f'untranslated {lg} {key}')
    t = T[lang]
    ui = {k: t[k] for k in ('play','pause','fall','circle','ellipse','leave','circ','esc','areaRead')}
    pre_note = t['slead']
    watch = {'en': 'Watch on YouTube', 'fr': 'Regarder sur YouTube', 'es': 'Ver en YouTube', 'ar': 'شاهد على يوتيوب', 'it': 'Guarda su YouTube', 'he': 'צפייה ב-YouTube'}[lang]
    vids_k = video('-luKN6mad5w', 'STEMonstrations: Newton’s First Law of Motion', t['vk'], watch)
    vids_m = video('NpHOlmNtFTQ', 'Real World: Keeping the International Space Station in Orbit', t['vm'], watch)
    vids_h = video('KTaIPz6oC9U', '7. Kepler’s Laws', t['vh1'], watch) + video('gXS0nXgSXJc', 'Cheops observing in space', t['vh2'], watch)
    vids_u = (video('zT7typHkpVg', 'Space debris — a journey to Earth', t['vu1'], watch)
              + video('9XcJ1wFRCk8', 'Gaia: launch to orbit', t['vu2'], watch)
              + video('SJI-SAs1Rnk', 'A Funny Thing Happened on the Way to the Moon', t['vu3'], watch))
    def level(i, h, outcomes, prose, worked, mq, ma, q, a, earth, vids=''):
        return f'''<section class="og-panel" id="{i}"><h2>{h}</h2>
<p class="lbox obj"><strong>{t["outcomes"]}</strong> {outcomes}</p>
<p>{prose}</p>
<div class="lbox ex"><strong>{t["worked"]}</strong> {worked}</div>
<div class="lbox mist"><strong>{t["check"]}</strong> {mq} {ma}</div>
{qa(t["show"], "<strong>"+t["practice"]+"</strong> "+q, a)}
<p class="lbox pre"><strong>{t["planet"]}</strong> {earth}</p>
{vids}</section>'''
    sand = f'''<section id="sandbox"><h2>{t["sand"]}</h2><p>{pre_note}</p>
<div id="og-app" data-ui="{E(json.dumps(ui, ensure_ascii=False))}">
<canvas id="og-c" class="og-c" width="640" height="400" role="img" aria-label="{E(t["sand"])}"></canvas>
<div class="og-controls" role="tablist" aria-label="{E(t["sand"])}">
<button type="button" role="tab" data-mode="cannon" aria-selected="true">{t["cannon"]}</button>
<button type="button" role="tab" data-mode="area" aria-selected="false">{t["area"]}</button>
<button type="button" role="tab" data-mode="hoh" aria-selected="false">{t["hoh"]}</button>
</div>
<div class="og-controls"><button type="button" id="og-play" aria-pressed="false">{t["play"]}</button></div>
<div data-for="cannon"><label>{t["speed"]} <input id="og-v" type="range" min="3" max="12" step="0.01" value="7.73"></label>
<div class="og-controls">
<button type="button" data-v="5">5 km/s</button>
<button type="button" data-v="7.73">{N("v300")} km/s</button>
<button type="button" data-v="9">{N("v9")} km/s</button>
<button type="button" data-v="11.2">11.2 km/s</button>
</div></div>
<div data-for="area" hidden><p>{t["areaRead"]}</p></div>
<div data-for="hoh" hidden><label>{t["outer"]} <input id="og-h" type="range" min="1000" max="36000" step="50" value="35786"></label></div>
<p id="og-read" aria-live="polite"></p>
</div></section>'''
    levels = (
      level('og-kids', t['hk'], t['ok'], t['pk'], t['wk'], t['mkq'], t['mka'], t['qk'], t['ak'], t['ek'], vids_k)
      + level('og-mid', t['hm'], t['om'], t['pm'], t['wm'], t['mmq'], t['mma'], t['qm'], t['am'], t['em'], vids_m)
      + level('og-high', t['hh'], t['oh'], t['ph'], t['wh'], t['hhq'], t['hha'], t['qh'], t['ah'], t['eh'], vids_h)
      + level('og-uni', t['hu'], t['ou'], t['pu'], t['wu'], t['muq'], t['mua'], t['qu'], t['au'], t['eu'], vids_u)
    )
    tabs = f'''<div class="og-tabs" role="tablist">
<button type="button" role="tab" aria-selected="true" aria-controls="og-kids">{t["hk"]}</button>
<button type="button" role="tab" aria-selected="false" aria-controls="og-mid">{t["hm"]}</button>
<button type="button" role="tab" aria-selected="false" aria-controls="og-high">{t["hh"]}</button>
<button type="button" role="tab" aria-selected="false" aria-controls="og-uni">{t["hu"]}</button>
</div>'''
    src = sources(lang, t['sources'], t['phet'])
    return f'''<p class="lbox pre">{t["intro"]}</p><p>{t["links"]}</p>
<section id="og101"><h2>{t["h101"]}</h2><p>{t["p101"]}</p>
<div class="lbox mist"><strong>{t["check"]}</strong> {t["m101q"]} {t["m101a"]}</div>
{qa(t["show"], "<strong>"+t["practice"]+"</strong> "+t["q101"], t["a101"])}
<p class="lbox pre"><strong>{t["planet"]}</strong> {t["e101"]}</p></section>
{sand}
{tabs}
{levels}
{src}
<div class="gc-slot" data-gc-url="https://www.savingplanets.com/{'' if lang=='en' else lang+'/'}Orbits_Guide.html" data-gc-title="{E(S['guideName'][lang])}" data-gc-body="{E(S['desc'][lang])}"></div>
<div class="crs" data-course="orbits-guide" hidden></div>'''

def sources(lang, heading, phet):
    items = [
        ('μ and the two-body constants used here follow Vallado’s standard gravitational parameter and the WGS-84 radius.',
         'https://earth-info.nga.mil/'),
    ]
    # Keep the list explicit and short. Labels are language-specific in the caller via a fixed English credit line plus the org name, which is the citation.
    rows = [
        ('NASA, About the International Space Station', 'https://www.nasa.gov/international-space-station/'),
        ('NASA, Basics of Space Flight, chapter 3', 'https://science.nasa.gov/learn/basics-of-space-flight/chapter3-4/'),
        ('NASA / USGS, Landsat 9', 'https://science.nasa.gov/mission/landsat-9/'),
        ('GPS.gov, Space segment', 'https://www.gps.gov/space-segment'),
        ('STScI, JWST orbit', 'https://jwst-docs.stsci.edu/jwst-observatory-characteristics/jwst-orbit'),
        ('NASA Glenn, nozzle design (thrust equation)', 'https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/nozzle-design/'),
        ('U.S. Standard Atmosphere, 1976 (NOAA / NASA / USAF)', 'https://ntrs.nasa.gov/citations/19770009539'),
        ('MIT OpenCourseWare 16.346 Astrodynamics, Fall 2008', 'https://ocw.mit.edu/courses/16-346-astrodynamics-fall-2008/'),
        ('Open Yale Courses, PHYS 200, lecture 7', 'https://oyc.yale.edu/physics/phys-200/lecture-7'),
        ('PhET, Gravity and Orbits', 'https://phet.colorado.edu/en/simulations/gravity-and-orbits'),
        ('NASA Blue Marble Next Generation', 'https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/base-topography-bathymetry'),
        ('NGSS MS-ESS1-2, HS-ESS1-4, HS-PS2-4', 'https://www.nextgenscience.org/'),
    ]
    # The first tuple was a mistake leftover. Do not emit it.
    lis = ''.join(f'<li><a href="{u}">{html.escape(name)}</a></li>' for name, u in rows)
    note = {
        'en': 'Speeds and transfer costs on this page were computed from those constants. Altitudes and inclinations that come from a mission page are named in the lesson. PhET is a link, not an embedded frame.',
        'fr': 'Les vitesses et les coûts de transfert de cette page sont calculés à partir de ces constantes. Les altitudes et inclinaisons tirées d’une page de mission sont nommées dans la leçon. PhET est un lien, pas un cadre intégré.',
        'es': 'Las velocidades y los costes de transferencia de esta página se calculan con esas constantes. Las altitudes e inclinaciones que vienen de una página de misión se nombran en la lección. PhET es un enlace, no un marco incrustado.',
        'ar': 'حُسبت السرعات وتكاليف الانتقال في هذه الصفحة من تلك الثوابت. الارتفاعات والميل المأخوذة من صفحة مهمة مذكورة في الدرس. PhET رابط وليس إطارًا مضمّنًا.',
        'it': 'Le velocità e i costi di trasferimento in questa pagina sono calcolati da quelle costanti. Quote e inclinazioni prese da una pagina di missione sono nominate nella lezione. PhET è un collegamento, non un riquadro incorporato.',
        'he': 'המהירויות ועלויות המעבר בעמוד הזה מחושבות מהקבועים האלה. גבהים ונטיות שמגיעים מעמוד משימה נקראים בשמם בשיעור. PhET הוא קישור, לא מסגרת מוטמעת.',
    }[lang]
    return f'<section id="og-src"><h2>{heading}</h2><p class="og-src">{note}</p><ul class="og-src">{lis}</ul><p class="og-src">{phet}: <a href="https://phet.colorado.edu/en/simulations/gravity-and-orbits">phet.colorado.edu</a></p></section>'

def translations():
    """Non-English strings keyed like the English dict. Proper names stay."""
    # Built as overlays. English remains the fallback only if a key is absent,
    # and the checker below rejects an overlay that leaves lesson prose in English.
    fr = {}
    es = {}
    ar = {}
    it = {}
    he = {}
    def put(key, a, b, c, d, e):
        fr[key], es[key], ar[key], it[key], he[key] = a, b, c, d, e
    put('show', 'Voir la réponse', 'Ver la respuesta', 'أظهر الإجابة', 'Mostra la risposta', 'הצגת התשובה')
    put('outcomes', 'Ce que vous savez faire après cette partie', 'Qué sabrás hacer después de esta parte', 'ما تستطيع فعله بعد هذا الجزء', 'Che cosa sai fare dopo questa parte', 'מה תוכלו לעשות אחרי החלק הזה')
    put('worked', 'Exemple chiffré', 'Ejemplo resuelto', 'مثال محلول', 'Esempio svolto', 'דוגמה פתורה')
    put('check', 'Contrôle d’une idée fausse', 'Comprobación de una idea falsa', 'فحص فكرة خاطئة', 'Controllo di un’idea sbagliata', 'בדיקת טעות נפוצה')
    put('practice', 'Entraînement', 'Práctica', 'تدريب', 'Esercizio', 'תרגול')
    put('planet', 'En quoi cela aide la planète', 'Cómo ayuda esto al planeta', 'كيف يساعد هذا الكوكب', 'Come questo aiuta il pianeta', 'איך זה עוזר לכוכב הלכת')
    put('sources', 'Sources des nombres', 'Fuentes de las cifras', 'مصادر الأرقام', 'Fonti dei numeri', 'מקורות המספרים')
    put('sand', 'Trois images à essayer', 'Tres imágenes para probar', 'ثلاث صور للتجربة', 'Tre immagini da provare', 'שלוש תמונות לניסיון')
    put('cannon', 'Vitesse de lancement', 'Velocidad de lanzamiento', 'سرعة الإطلاق', 'Velocità di lancio', 'מהירות שיגור')
    put('area', 'Aires égales', 'Áreas iguales', 'مساحات متساوية', 'Aree uguali', 'שטחים שווים')
    put('hoh', 'Hohmann', 'Hohmann', 'هومان', 'Hohmann', 'הומן')
    put('speed', 'Vitesse de côté, km/s', 'Velocidad lateral, km/s', 'السرعة الجانبية، كم/ث', 'Velocità laterale, km/s', 'מהירות הצידה, ק״מ/ש׳')
    put('outer', 'Altitude d’arrivée, km', 'Altitud de llegada, km', 'ارتفاع الوصول، كم', 'Quota di arrivo, km', 'גובה היעד, ק״מ')
    put('play', 'Lire', 'Reproducir', 'تشغيل', 'Avvia', 'הפעלה')
    put('pause', 'Pause', 'Pausa', 'إيقاف', 'Pausa', 'השהיה')
    put('fall', 'retombe', 'cae de vuelta', 'يسقط عائدًا', 'ricade', 'נופל בחזרה')
    put('circle', 'cercle', 'círculo', 'دائرة', 'cerchio', 'מעגל')
    put('ellipse', 'ellipse', 'elipse', 'قطع ناقص', 'ellisse', 'אליפסה')
    put('leave', 'quitte la Terre', 'se marcha de la Tierra', 'يغادر الأرض', 'lascia la Terra', 'עוזב את כדור הארץ')
    put('circ', 'circulaire', 'circular', 'دائرية', 'circolare', 'מעגלית')
    put('esc', 'libération', 'escape', 'إفلات', 'fuga', 'בריחה')
    put('h101', 'Orbites 101', 'Órbitas 101', 'مدارات 101', 'Orbite 101', 'מסלולים 101')
    put('hk', 'Enfants', 'Infancia', 'أطفال', 'Bambini', 'ילדים')
    put('hm', 'Collège', 'Secundaria', 'إعدادي', 'Scuola media', 'חטיבת ביניים')
    put('hh', 'Lycée', 'Bachillerato', 'ثانوي', 'Scuola superiore', 'תיכון')
    put('hu', 'Université', 'Universidad', 'جامعة', 'Università', 'אוניברסיטה')
    put('phet', 'PhET Gravité et orbites (lien, pas d’intégration)', 'PhET Gravedad y órbitas (enlace, sin incrustar)', 'PhET الجاذبية والمدارات (رابط بلا تضمين)', 'PhET Gravità e orbite (collegamento, non incorporato)', 'PhET כבידה ומסלולים (קישור, בלי הטמעה)')
    # Long prose is loaded from orbits_guide_i18n.json so this file stays reviewable.
    return overlay_from_json(fr, es, ar, it, he)

PROSE = ['intro','links','p101','m101q','m101a','q101','a101','e101','ok','pk','wk','mkq','mka','qk','ak','ek','vk','om','pm','wm','mmq','mma','qm','am','em','vm','oh','ph','wh','hhq','hha','qh','ah','eh','vh1','vh2','ou','pu','wu','muq','mua','qu','au','eu','vu1','vu2','vu3','slead','areaRead']

def overlay_from_json(fr, es, ar, it, he):
    path = pathlib.Path(__file__).with_name('orbits_guide_i18n.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    missing = [k for k in PROSE if k not in data]
    if missing:
        raise SystemExit('i18n missing ' + ', '.join(missing))
    out = {'fr': fr, 'es': es, 'ar': ar, 'it': it, 'he': he}
    for key, pack in data.items():
        for lg in out:
            if lg not in pack:
                raise SystemExit(f'missing {lg} for {key}')
            out[lg][key] = pack[lg]
    return out

CSS = '''.og-tabs{display:flex;flex-wrap:wrap;gap:.4rem;margin:1rem 0}.og-tabs button,.og-controls button{font:inherit;font-weight:700;padding:.35rem .7rem;border-radius:999px;border:1px solid rgba(124,170,255,.5);background:rgba(124,170,255,.12);color:inherit;cursor:pointer}.og-tabs button[aria-selected="true"]{border-color:#7cfc98}.og-controls{display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;margin:.5rem 0}.og-controls label{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}.og-c{width:100%;height:auto;background:#071018;border-radius:12px}.ytf{display:flex;align-items:center;justify-content:center;width:100%;min-height:4.2rem;margin:.4rem 0;border:0;border-radius:12px;background:#102033;color:#fff;font:inherit;font-weight:700;cursor:pointer;text-align:center;padding:.6rem}.ytf-fallback{display:inline-block;margin:.15rem 0 .7rem;font-weight:700}.og-vid iframe{width:100%;max-width:100%;aspect-ratio:16/9;height:auto;border:0;border-radius:12px}.og-src{font-size:.95rem}html.og-ready .og-panel{display:none}html.og-ready .og-panel.is-on{display:block}@media print{html.og-ready .og-panel{display:block !important}.ytf{display:none}}@media (prefers-reduced-motion:reduce){#og-play{display:none}}'''

def splice(path, lang):
    s = path.read_text(encoding='utf-8')
    inner = body(lang)
    i = s.find('<div class="lw">')
    k = s.find('</main>')
    if i < 0 or k < 0:
        raise SystemExit('markers missing ' + str(path))
    j = s.rfind('</div>', i, k)
    s = s[:i] + '<div class="lw">' + inner + '</div>' + s[j+6:]
    old = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not old:
        raise SystemExit('no description ' + str(path))
    s = s.replace(old.group(1), S['desc'][lang])
    s = re.sub(r'(<div class="page-hero-content"><h1>[^<]*</h1><p>)(.*?)(</p>)',
               lambda m: m.group(1) + S['kicker'][lang] + m.group(3), s, count=1)
    if '.og-tabs{' not in s:
        anchor = s.find('.lw{max-width')
        end = s.find('</style>', anchor)
        s = s[:end] + CSS + s[end:]
    pre = '' if lang == 'en' else '../'
    tag = f'<script src="{pre}assets/orbits-guide.js?v=20261118e" defer></script>'
    if 'orbits-guide.js' not in s:
        s = s.replace('</body>', tag + '</body>', 1)
    css = f'{pre}assets/classroom.css'
    js = f'<script src="{pre}assets/classroom.js" defer></script>'
    if 'classroom.js' not in s:
        link = (f'<link rel="preload" as="style" href="{css}" onload="this.onload=null;this.rel=\'stylesheet\'">'
                f'<noscript class="crit-ns"><link rel="stylesheet" href="{css}"></noscript>')
        s = s.replace('</head>', link + '</head>', 1)
        s = s.replace('</body>', js + '</body>', 1)
    # first level visible once the script marks the document ready
    s = s.replace('id="og-kids"', 'id="og-kids" class="og-panel is-on"', 1)
    s = s.replace('<section class="og-panel" id="og-kids" class="og-panel is-on">',
                  '<section class="og-panel is-on" id="og-kids">', 1)
    path.write_text(s, encoding='utf-8')
    print('wrote', path)

def retitle_links():
    for lang in LANGS:
        pre = ROOT if lang == 'en' else ROOT / lang
        learn = pre / 'Learn_Orbits.html'
        s = learn.read_text(encoding='utf-8')
        name = S['guideName'][lang]
        s2 = s.replace('>Orbits_Guide.html</a>', f'>{name}</a>', 1)
        if s2 == s and f'>{name}</a>' not in s:
            raise SystemExit('guide link missing ' + str(learn))
        learn.write_text(s2, encoding='utf-8')
        courses = pre / 'Undergraduate_Studies.html'
        c = courses.read_text(encoding='utf-8')
        old = {
            'en': '<p>Orbits, transfers and mission design.</p>',
            'fr': '<p>Orbites, transferts et conception de missions.</p>',
            'es': '<p>Órbitas, transferencias y diseño de misiones.</p>',
            'ar': '<p>المدارات والانتقالات وتصميم البعثات.</p>',
            'it': '<p>Orbite, trasferimenti e progettazione di missioni.</p>',
            'he': '<p>מסלולים, מעברים ותכנון משימות.</p>',
        }[lang]
        extra = f' <a href="Orbits_Guide.html">{S["guideName"][lang]}</a>'
        if extra in c:
            continue
        if old not in c:
            raise SystemExit('course blurb missing ' + str(courses))
        courses.write_text(c.replace(old, old.replace('</p>', extra + '</p>'), 1), encoding='utf-8')
        print('linked', lang)

def dedupe_orbit_lab():
    for lang in LANGS:
        p = ROOT / ('Orbit_Lab.html' if lang == 'en' else f'{lang}/Orbit_Lab.html')
        s = p.read_text(encoding='utf-8')
        seen = set()
        def repl(m):
            t = m.group(0)
            if 'rel="preload"' in t and t in seen:
                return ''
            seen.add(t)
            return t
        n = re.sub(r'<link\b[^>]*>', repl, s)
        if n != s:
            p.write_text(n, encoding='utf-8')
            print('deduped', p)

if __name__ == '__main__':
    for lang in LANGS:
        p = ROOT / ('Orbits_Guide.html' if lang == 'en' else f'{lang}/Orbits_Guide.html')
        splice(p, lang)
    retitle_links()
    dedupe_orbit_lab()
