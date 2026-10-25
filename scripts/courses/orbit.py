"""Orbital Mechanics (AERO 340): the two-body problem, conic orbits and orbital elements, Kepler’s equation and time of flight, orbit transfers, plane changes, the rocket equation, perturbations and sun-synchronous orbits, ground tracks and coverage, interplanetary transfers, and space sustainability.
Oct 25 2026, founder-approved four-year track, junior course 6. Same module fields as struct.py / perf.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, sin, cos, tan, atan, log, exp, radians, degrees, acos
ID = 'orbit'
STATUS = 'live'
YEAR = 3
PAGE = 'Orbital_Mechanics.html'
CODE = 'AERO 340'
TITLE = 'Orbital Mechanics'
LAB_NAME = 'Astrodynamics lab'
TAGLINE = 'Orbits, transfers and mission design: Newton’s gravity and the two-body problem, ellipses and orbital elements, Kepler’s equation, Hohmann transfers, plane changes, the rocket equation, the Earth’s bulge and sun-synchronous orbits, ground tracks, trips to Mars, and keeping orbits clean of debris, with six labs. Free, self-paced, and tied to Landsat, GOES weather satellites, NASA’s DART asteroid test and orbital-debris rules.'
DESC = 'Free self-study Orbital Mechanics: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET, NASA Eyes and spreadsheet labs, practice exams, tied to Earth-observing satellites and space sustainability.'
ALT = 'An Atlas V rocket lifts off carrying the Landsat 9 Earth-observing satellite'
_PH = 'https://phet.colorado.edu/en/simulations/'
_O = 'https://openstax.org/books/university-physics-volume-1/pages/'
_MIT = ('MIT OpenCourseWare 16.346 Astrodynamics (Fall 2008)', 'https://ocw.mit.edu/courses/16-346-astrodynamics-fall-2008/')
_MITD = ('MIT OpenCourseWare 16.07 Dynamics (Fall 2009)', 'https://ocw.mit.edu/courses/16-07-dynamics-fall-2009/')
_BSF = ('NASA: Basics of Space Flight', 'https://science.nasa.gov/learn/basics-of-space-flight/')
_BSF5 = ('NASA Basics of Space Flight, Chapter 5: Planetary orbits', 'https://science.nasa.gov/learn/basics-of-space-flight/chapter5-1/')
_EYES = ('NASA’s Eyes on the Solar System', 'https://eyes.nasa.gov/apps/solar-system/')
_ODPO = ('NASA Orbital Debris Program Office', 'https://orbitaldebris.jsc.nasa.gov/')
_L9 = ('NASA Science: Landsat 9', 'https://landsat.gsfc.nasa.gov/satellites/landsat-9/landsat-9-overview/')
_GOES = ('NOAA NESDIS: GOES-R Series mission', 'https://www.goes-r.gov/mission/mission.html')
_DEB = ('NASA Headquarters Library: Space Debris', 'https://www.nasa.gov/headquarters/library/find/bibliographies/space-debris/')
_FCC = ('FCC: FCC Adopts New ‘5-Year Rule’ for Deorbiting Satellites (Report and Order FCC-22-74)', 'https://www.fcc.gov/document/fcc-adopts-new-5-year-rule-deorbiting-satellites-0')
_DART = ('NASA Science: Double Asteroid Redirection Test (DART)', 'https://science.nasa.gov/mission/dart/')
_DARTR = ('NASA: NASA Confirms DART Mission Impact Changed Asteroid’s Motion in Space (Oct. 11, 2022)', 'https://www.nasa.gov/news-release/nasa-confirms-dart-mission-impact-changed-asteroids-motion-in-space/')
BANNER = ['images/Landsat9_Launch_KLS04_0013.jpg', 'images/ISS_Flyaround_2021.jpg', 'images/JPSS2_Atlas_V_Launch_Pad.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg']
CREDITS = {'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)', 'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)',
           'images/JPSS2_Atlas_V_Launch_Pad.jpg': 'NASA/Liz Wilk (KSC-20221109-PH-LNW01_0001)', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester junior orbital mechanics course. It is modeled on the topics and depth of MIT 16.346 Astrodynamics and the orbital parts of MIT 16.07 Dynamics (free on MIT OpenCourseWare), and on courses such as Purdue AAE 340 and Georgia Tech AE 3330, using NASA’s free Basics of Space Flight and OpenStax University Physics, which we link where they help. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (Landsat, GOES weather satellites, NASA’s DART planetary-defense test and orbital-debris rules), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a spreadsheet.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Orbits are how we watch our planet: Earth-observing satellites in low orbits map forests, crops and water, and geostationary weather satellites watch storms around the clock. Choosing those orbits is pure orbital mechanics.',
                 'Orbits are also a shared, limited resource. Debris left in space threatens the satellites we rely on, so responsible mission design now includes a plan to leave orbit. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Dynamics: Newton’s laws, angular momentum and energy.', 'Calculus III and Differential Equations: vectors, gradients and ODEs.',
           'Linear Algebra: vectors, rotations and coordinate frames.', 'Physics I: universal gravitation.']
STUDY = ['Start every problem with a sketch of the orbit: central body, periapsis, apoapsis and the spacecraft’s position.', 'Write the vis-viva equation first; it answers most speed questions.',
         'Keep units in metres and seconds, and μ in m³/s²; convert to km only at the end.', 'Draw each maneuver as a velocity triangle before computing Δv.',
         'Check limits: a circular orbit has e = 0; escape has zero total energy.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Gravity and Orbits, Kepler’s Laws and My Solar System simulations.', 'NASA’s Eyes on the Solar System in a web browser.',
            'Spreadsheet software for the transfer, rocket-equation and ground-track labs.', 'A calculator with trigonometric functions.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free simulation or a spreadsheet, so there are no physical hazards. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('Earth (textbook values)', 'μ = 3.986 × 10¹⁴ m³/s², R = 6378 km, J₂ = 1.0826 × 10⁻³, sidereal day 86,164.1 s'), ('Sun (textbook value)', 'μ = 1.327 × 10²⁰ m³/s², 1 AU = 1.496 × 10¹¹ m'),
             ('Mars orbit (textbook value)', 'a = 1.524 AU'), ('Standard gravity', 'g₀ = 9.80665 m/s²'), ('1 mile', '1.609344 km'), ('1 mph', '0.44704 m/s')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, NASA guides and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT astrodynamics lectures and problem sets.'), (_MITD[0], _MITD[1], 'Free MIT dynamics notes on orbits.'), (_BSF[0], _BSF[1], 'Free NASA guide to orbits and missions.'),
          ('OpenStax University Physics Volume 1, 13.5 Kepler’s laws', _O + '13-5-keplers-laws-of-planetary-motion', 'Free textbook section.'), ('PhET: Gravity and Orbits', _PH + 'gravity-and-orbits', 'Orbits interactively.'),
          (_EYES[0], _EYES[1], 'Real spacecraft trajectories in 3D.')]
UNITS = []
_RK = ('OpenStax UP1, 13.5 Kepler’s laws of planetary motion', _O + '13-5-keplers-laws-of-planetary-motion', 'Free textbook section.')
_RE = ('OpenStax UP1, 13.4 Satellite orbits and energy', _O + '13-4-satellite-orbits-and-energy', 'Free textbook section.')
_RR = ('OpenStax UP1, 9.7 Rocket propulsion', _O + '9-7-rocket-propulsion', 'Free textbook section.')
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS.append(
{'id': 'u1', 'title': 'Gravity, the Two-Body Problem and Circular Orbits', 'weeks': 'Week 1',
 'summary': 'Newton’s law of gravitation, the gravitational parameter μ, the two-body equation of motion, circular orbit speed and period, escape speed, Kepler’s three laws, and low, medium and geostationary orbits.',
 'objectives': ['Write the two-body equation of motion.', 'Compute circular orbit speed and period.', 'Compute escape speed.', 'Find the geostationary radius.'],
 'concepts': ['Newton’s gravity gives the two-body equation r̈ = −μr/r³, with μ = GM. For Earth μ = 3.986 × 10¹⁴ m³/s².',
              'A circular orbit has speed v = √(μ/r) and period T = 2π√(r³/μ): higher orbits are slower and take longer.',
              'Escape speed is √2 times circular speed at the same radius: v_esc = √(2μ/r).',
              'Kepler’s laws: orbits are ellipses with the central body at a focus; the radius sweeps equal areas in equal times; and T² is proportional to a³.',
              'A geostationary orbit has a period of one sidereal day (86,164.1 s) and lies over the equator, so the satellite stays over the same spot.'],
 'eqs': [('\\ddot{\\mathbf r}=-\\frac{\\mu}{r^3}\\mathbf r', 'Two-body equation'), ('v_c=\\sqrt{\\frac{\\mu}{r}}', 'Circular speed'), ('T=2\\pi\\sqrt{\\frac{a^3}{\\mu}}', 'Period'), ('v_{esc}=\\sqrt{\\frac{2\\mu}{r}}', 'Escape speed')],
 'worked': [
  _w('Find the speed and period of a circular orbit 400 km up.', ['r = 6378 + 400 = 6778 km.', 'v = √(3.986 × 10¹⁴/6.778 × 10⁶).', 'T = 2π√(r³/μ).'], 'v = 7.67 km/s; T = 92.6 min.'),
  _w('Find escape speed from that altitude.', ['v_esc = √2 × 7.669.'], 'v_esc = 10.85 km/s.'),
  _w('Find the geostationary radius and altitude.', ['r = (μT²/(4π²))^(1/3) with T = 86,164.1 s.', 'Altitude = 42,164 − 6378.'], 'r = 42,164 km; altitude 35,786 km (22,236 miles); v = 3.07 km/s.')],
 'practice': [('Find the period of a circular orbit 705 km up.', '98.9 min.'), ('Find the speed there.', '7.50 km/s.'),
              ('How many orbits a day is that?', '1440/98.87 = 14.56.'), ('Convert 7.67 km/s to mph.', '17,154 mph.')],
 'misc': [('Higher orbits are faster.', 'They are slower.'), ('Astronauts float because there is no gravity.', 'They are in free fall around Earth.'), ('A geostationary orbit can be over any city.', 'It must be over the equator.')],
 'quiz': [_q('Circular speed is…', ['√(μ/r)', 'μ/r', '√(2μ/r)', 'μr'], 0, 'Gravity = centripetal.'), _q('Escape speed is … times circular.', ['√2', '2', '1', '½'], 0, 'Energy.'),
          _q('Kepler’s third law relates…', ['T² and a³', 'T and a', 'v and r', 'e and a'], 0, 'Harmonic law.'), _q('GEO period is…', ['one sidereal day', '12 h', '90 min', '1 year'], 0, 'Matches rotation.')],
 'cards': [('μ', 'GM = 3.986 × 10¹⁴ m³/s².'), ('Circular speed', '√(μ/r).'), ('Period', '2π√(a³/μ).'), ('Escape', '√(2μ/r).'), ('Kepler 3', 'T² ∝ a³.'), ('GEO', '42,164 km radius.')],
 'planet': {'text': ['NOAA explains that GOES weather satellites orbit 22,236 miles above Earth’s equator at speeds equal to Earth’s rotation, so they stay over the same regions and give continuous coverage. Together, GOES East and GOES West watch over more than half the globe, from the west coast of Africa to New Zealand.',
                     'The GOES-R series imager can image storms as often as every 30 seconds, and the series carries the first operational lightning mapper in geostationary orbit. The 22,236-mile altitude is exactly this unit’s geostationary radius minus Earth’s radius.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Physics I', 'Physics_I.html')],
            'src': [_GOES]},
 'res': [_RK, _RE, (_BSF5[0], _BSF5[1], 'Free NASA chapter.'), ('PhET: Gravity and Orbits', _PH + 'gravity-and-orbits', 'Orbits interactively.')]})
UNITS.append(
{'id': 'u2', 'title': 'Conic Sections, Energy and Orbital Elements', 'weeks': 'Weeks 2–3',
 'summary': 'Conservation of energy and angular momentum, the orbit equation, ellipses, parabolas and hyperbolas, eccentricity, the vis-viva equation, periapsis and apoapsis speeds, and the six classical orbital elements.',
 'objectives': ['Use vis-viva to find speeds.', 'Relate eccentricity to periapsis and apoapsis.', 'Compute specific energy and angular momentum.', 'Name and interpret the six orbital elements.'],
 'concepts': ['Specific energy ε = v²/2 − μ/r = −μ/(2a) is constant: negative for ellipses, zero for parabolas and positive for hyperbolas.',
              'Specific angular momentum h = r × v is constant, so the orbit lies in a fixed plane.',
              'The orbit equation r = (h²/μ)/(1 + e cos ν) gives the radius at true anomaly ν. Eccentricity e = (r_a − r_p)/(r_a + r_p) for an ellipse.',
              'The vis-viva equation v² = μ(2/r − 1/a) gives the speed anywhere on any orbit.',
              'Six classical elements fix an orbit: semi-major axis a, eccentricity e, inclination i, right ascension of the ascending node Ω, argument of periapsis ω and true anomaly ν.'],
 'eqs': [('\\varepsilon=\\frac{v^2}{2}-\\frac{\\mu}{r}=-\\frac{\\mu}{2a}', 'Specific energy'), ('v^2=\\mu\\left(\\frac2r-\\frac1a\\right)', 'Vis-viva'), ('r=\\frac{h^2/\\mu}{1+e\\cos\\nu}', 'Orbit equation'), ('e=\\frac{r_a-r_p}{r_a+r_p}', 'Eccentricity')],
 'worked': [
  _w('An orbit has perigee radius 6778 km and apogee radius 42,164 km. Find a and e.', ['a = (6778 + 42,164)/2 = 24,471 km.', 'e = (42,164 − 6778)/(42,164 + 6778).'], 'a = 24,471 km; e = 0.723.'),
  _w('Find its specific energy.', ['ε = −3.986 × 10¹⁴/(2 × 2.4471 × 10⁷).'], 'ε = −8.14 MJ/kg.'),
  _w('Find the speeds at perigee and apogee.', ['v_p = √(μ(2/r_p − 1/a)).', 'v_a = √(μ(2/r_a − 1/a)).'], 'v_p = 10.07 km/s; v_a = 1.62 km/s.')],
 'practice': [('Find h at perigee.', 'r_p v_p = 6.778 × 10⁶ × 10,066 = 6.82 × 10¹⁰ m²/s.'), ('What is e for a circle?', '0.'),
              ('What sign is ε for an escape trajectory?', 'Zero or positive.'), ('Find the period of the orbit above.', '2π√(a³/μ) = 10.58 h.')],
 'misc': [('The satellite moves at constant speed on an ellipse.', 'Fastest at periapsis, slowest at apoapsis.'), ('Inclination is measured from the North Pole.', 'From the equator plane.'), ('Energy depends on eccentricity.', 'Only on a.')],
 'quiz': [_q('Vis-viva gives…', ['speed', 'period', 'inclination', 'node'], 0, 'v² = μ(2/r − 1/a).'), _q('An ellipse has…', ['ε < 0', 'ε = 0', 'ε > 0', 'e > 1'], 0, 'Bound orbit.'),
          _q('Speed is highest at…', ['periapsis', 'apoapsis', 'the node', 'everywhere'], 0, 'Angular momentum.'), _q('How many classical elements?', ['6', '3', '4', '9'], 0, 'a, e, i, Ω, ω, ν.')],
 'cards': [('Energy', '−μ/(2a).'), ('Vis-viva', 'v² = μ(2/r − 1/a).'), ('Angular momentum', 'h = r × v.'), ('Orbit equation', 'r = (h²/μ)/(1 + e cos ν).'), ('Eccentricity', '(r_a − r_p)/(r_a + r_p).'), ('Elements', 'a, e, i, Ω, ω, ν.')],
 'planet': {'text': ['NASA lists Landsat 9’s orbit as near-polar and sun-synchronous, at 705 km altitude and 98.2° inclination, with a period of 99 minutes, about 14.5 orbits a day, and a nominal equator crossing at 10:12 a.m. local time on the descending pass.',
                     'Those few numbers are orbital elements: a from the altitude, e near zero, i = 98.2°, and a node chosen to fix the local crossing time. The steady geometry is what lets Landsat compare images across more than five decades of its record.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Calculus III', 'Calculus_III.html')],
            'src': [_L9]},
 'res': [_RE, (_MIT[0], _MIT[1], 'MIT notes on conics.'), (_BSF5[0], _BSF5[1], 'Free NASA chapter.'), ('PhET: Kepler’s Laws', _PH + 'keplers-laws', 'Ellipses interactively.')]})
UNITS.append(
{'id': 'u3', 'title': 'Kepler’s Equation and Time of Flight', 'weeks': 'Week 4',
 'summary': 'Mean motion, mean, eccentric and true anomaly, Kepler’s equation M = E − e sin E, solving it with Newton’s method, time of flight between two points, and position at a given time.',
 'objectives': ['Relate mean, eccentric and true anomaly.', 'Solve Kepler’s equation iteratively.', 'Find the time to fly between two true anomalies.', 'Predict a satellite’s position at a later time.'],
 'concepts': ['Mean motion n = √(μ/a³) is the average angular rate. Mean anomaly M = n(t − t_p) grows uniformly with time.',
              'Kepler’s equation links time to geometry: M = E − e sin E, where E is the eccentric anomaly.',
              'True anomaly follows from tan(ν/2) = √((1 + e)/(1 − e)) tan(E/2).',
              'Kepler’s equation has no closed-form solution for E; Newton’s method, E ← E − (E − e sin E − M)/(1 − e cos E), converges in a few steps.',
              'Time of flight from ν₁ to ν₂: find E₁, E₂, then M₁, M₂, and divide the difference by n.'],
 'eqs': [('n=\\sqrt{\\frac{\\mu}{a^3}}', 'Mean motion'), ('M=E-e\\sin E', 'Kepler’s equation'), ('\\tan\\frac\\nu2=\\sqrt{\\frac{1+e}{1-e}}\\tan\\frac E2', 'True anomaly'), ('t-t_p=\\frac Mn', 'Time since periapsis')],
 'worked': [
  _w('For e = 0.3, find M when E = π/2.', ['M = 1.5708 − 0.3 × 1.']  , 'M = 1.271 rad.'),
  _w('For e = 0.3 and M = 1 rad, solve Kepler’s equation.', ['Start E = 1; apply Newton’s method until it settles.'], 'E = 1.288 rad.'),
  _w('Find the true anomaly for that E.', ['tan(ν/2) = √(1.3/0.7) × tan(0.644).'], 'ν = 1.594 rad (91.3°).')],
 'practice': [('How long does a LEO-to-GEO transfer take (half of a 10.58 h orbit)?', '5.29 h.'), ('For a circle, how are M, E and ν related?', 'They are equal.'),
              ('Why can’t we solve for E directly?', 'Kepler’s equation is transcendental.'), ('What is the mean motion of a 92.6 min orbit in rev/day?', '1440/92.56 = 15.56.')],
 'misc': [('True anomaly grows uniformly with time.', 'Mean anomaly does.'), ('Kepler’s equation applies to hyperbolas unchanged.', 'Hyperbolas use a hyperbolic form.'), ('Newton’s method needs many iterations.', 'Usually 3–5.')],
 'quiz': [_q('Kepler’s equation is…', ['M = E − e sin E', 'M = E + e', 'E = ν', 'n = M/E'], 0, 'Definition.'), _q('Mean motion is…', ['√(μ/a³)', 'μ/a', '√(μa)', 'a/μ'], 0, '2π/T.'),
          _q('Which anomaly grows uniformly?', ['mean', 'true', 'eccentric', 'none'], 0, 'M = nt.'), _q('Kepler’s equation is solved…', ['iteratively', 'directly', 'graphically only', 'never'], 0, 'Newton’s method.')],
 'cards': [('Mean motion', 'n = √(μ/a³).'), ('Mean anomaly', 'M = n(t − t_p).'), ('Kepler’s equation', 'M = E − e sin E.'), ('True anomaly', 'From tan(ν/2).'), ('Newton step', 'E − f/f′.'), ('Time of flight', 'ΔM/n.')],
 'planet': {'text': ['NASA reports that before DART’s impact, the moonlet Dimorphos took 11 hours and 55 minutes to orbit its parent asteroid Didymos, and that after the impact on September 26, 2022 the period was 11 hours and 23 minutes, a change of 32 minutes (uncertainty about ±2 minutes).',
                     'Astronomers measured that change by timing the moonlet’s orbit from telescopes on Earth: Kepler’s laws turn a small timing shift into proof that the orbit had changed.'],
            'site': [('Calculus II', 'Calculus_II.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_DARTR]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on Kepler’s equation.'), _RK, (_BSF5[0], _BSF5[1], 'Free NASA chapter.'), (_MITD[0], _MITD[1], 'MIT dynamics notes.')]})
UNITS.append(
{'id': 'u4', 'title': 'Orbit Transfers: Hohmann and Beyond', 'weeks': 'Weeks 5–6',
 'summary': 'Impulsive maneuvers and Δv, the Hohmann transfer between circular orbits, transfer time, bi-elliptic transfers, phasing and rendezvous, and raising and lowering orbits.',
 'objectives': ['Compute Δv for a Hohmann transfer.', 'Find the transfer time.', 'Explain when bi-elliptic transfers save Δv.', 'Plan a simple phasing maneuver.'],
 'concepts': ['An impulsive burn changes velocity instantly by Δv; the orbit after the burn follows from vis-viva.',
              'The Hohmann transfer uses an ellipse tangent to both circles: burn at the inner orbit to enter the ellipse, and burn again at apoapsis to circularize.',
              'Transfer time is half the period of the transfer ellipse.',
              'For very large radius ratios (above about 11.9), a three-burn bi-elliptic transfer can use less Δv, at the cost of much more time.',
              'Phasing: to catch a target in the same orbit, enter a slightly smaller or larger orbit for one or more revolutions, then return.'],
 'eqs': [('\\Delta v_1=\\sqrt{\\mu\\left(\\frac2{r_1}-\\frac1a\\right)}-\\sqrt{\\frac\\mu{r_1}}', 'First burn'), ('\\Delta v_2=\\sqrt{\\frac\\mu{r_2}}-\\sqrt{\\mu\\left(\\frac2{r_2}-\\frac1a\\right)}', 'Second burn'), ('a=\\frac{r_1+r_2}{2}', 'Transfer ellipse'), ('t=\\pi\\sqrt{\\frac{a^3}{\\mu}}', 'Transfer time')],
 'worked': [
  _w('Find the Δv for a Hohmann transfer from a 400 km circular orbit to GEO (in the same plane).', ['Δv₁ = 10.066 − 7.669 = 2.398 km/s.', 'Δv₂ = 3.075 − 1.618 = 1.456 km/s.'], 'Total Δv = 3.85 km/s.'),
  _w('Find the transfer time.', ['t = π√(24,471,000³/μ).'], 't = 5.29 h.'),
  _w('A deorbit burn at 700 km lowers perigee to 200 km. Find Δv.', ['v_c = √(μ/7078 km).', 'v_a on the 7078 × 6578 km ellipse from vis-viva.'], 'Δv = 139 m/s.')],
 'practice': [('Which burn is larger in the LEO-to-GEO Hohmann?', 'The first, 2.40 km/s.'), ('Above what radius ratio can bi-elliptic win?', 'About 11.9.'),
              ('To catch up to a target ahead in the same orbit, go higher or lower?', 'Lower (shorter period).'), ('Which way do you burn to lower an orbit?', 'Retrograde.')],
 'misc': [('To speed up in orbit, burn forward and stay faster.', 'Raising the orbit makes you slower overall.'), ('Hohmann is always the cheapest.', 'Not for very large ratios.'), ('Transfer time is a full period.', 'Half a period.')],
 'quiz': [_q('Hohmann uses … burns.', ['2', '1', '3', '4'], 0, 'Tangent burns.'), _q('Transfer time is…', ['half the transfer period', 'full period', 'zero', 'one day'], 0, 'Periapsis to apoapsis.'),
          _q('To catch a target ahead, go…', ['lower', 'higher', 'polar', 'nowhere'], 0, 'Shorter period.'), _q('Transfer ellipse a is…', ['(r₁ + r₂)/2', 'r₁r₂', 'r₂ − r₁', '√(r₁r₂)'], 0, 'Tangent ellipse.')],
 'cards': [('Δv', 'Velocity change.'), ('Hohmann', 'Two tangent burns.'), ('Transfer a', '(r₁ + r₂)/2.'), ('Transfer time', 'π√(a³/μ).'), ('Bi-elliptic', 'Three burns, large ratios.'), ('Phasing', 'Lower to catch up.')],
 'planet': {'text': ['The FCC adopted a rule in September 2022 requiring satellite operators in low Earth orbit to dispose of their satellites within 5 years of completing their missions (Report and Order FCC-22-74).',
                     'A deorbit burn is just a Hohmann-style half maneuver: lower the perigee into the upper atmosphere so drag finishes the job. From 700 km, lowering perigee to 200 km takes only about 139 m/s in this unit’s example.'],
            'site': [('Dynamics', 'Dynamics.html'), ('Solutions', 'Solutions.html')],
            'src': [_FCC]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on transfers.'), (_BSF[0], _BSF[1], 'Free NASA guide.'), _RE, (_EYES[0], _EYES[1], 'Real trajectories.')]})
UNITS.append(
{'id': 'u5', 'title': 'Plane Changes and Combined Maneuvers', 'weeks': 'Week 7',
 'summary': 'Inclination and node changes, the simple plane-change Δv, why plane changes are expensive in low orbit, combining a plane change with a Hohmann burn, and launch site latitude.',
 'objectives': ['Compute a simple plane-change Δv.', 'Combine a plane change with a circularization burn.', 'Explain why plane changes are done at high altitude.', 'Relate launch latitude to the minimum inclination.'],
 'concepts': ['Rotating the orbit plane by Δi at speed v costs Δv = 2v sin(Δi/2), with no change in speed.',
              'Because the cost scales with speed, plane changes are cheapest where the spacecraft is slowest: at apoapsis or in high orbits.',
              'Combining a plane change with a speed change in one burn uses the law of cosines: Δv = √(v₁² + v₂² − 2v₁v₂ cos Δi), which is cheaper than doing them separately.',
              'A direct launch reaches an inclination no lower than the launch site’s latitude, so GEO satellites launched from mid-latitudes must remove inclination later.',
              'Node changes and combined inclination-and-node changes use the same velocity-triangle idea with spherical trigonometry.'],
 'eqs': [('\\Delta v=2v\\sin\\frac{\\Delta i}{2}', 'Simple plane change'), ('\\Delta v=\\sqrt{v_1^2+v_2^2-2v_1v_2\\cos\\Delta i}', 'Combined maneuver'), ('i_{min}=\\phi_{launch}', 'Minimum direct inclination'), ('\\cos i=\\cos\\phi\\sin\\beta', 'Launch azimuth β')],
 'worked': [
  _w('Find the Δv to remove 28.5° of inclination at GEO (v = 3.075 km/s).', ['Δv = 2 × 3.075 × sin 14.25°.'], 'Δv = 1.51 km/s.'),
  _w('Combine that plane change with the GEO circularization burn (v_a = 1.618 km/s).', ['Δv = √(1.618² + 3.075² − 2 × 1.618 × 3.075 × cos 28.5°).'], 'Δv = 1.82 km/s, saving 1.15 km/s over separate burns (1.51 + 1.46).'),
  _w('Find the cost of a 10° plane change in a 400 km orbit.', ['Δv = 2 × 7.669 × sin 5°.'], 'Δv = 1.34 km/s.')],
 'practice': [('Total LEO-to-GEO Δv with the combined final burn?', '2.40 + 1.82 = 4.22 km/s.'), ('Where is the cheapest place to change planes on an ellipse?', 'Apoapsis.'),
              ('A 60° plane change costs how many times v?', '2 sin 30° = 1 × v.'), ('Can a direct launch from 28.5° latitude reach 0° inclination?', 'No.')],
 'misc': [('Plane changes are cheap.', 'In LEO, 10° costs 1.34 km/s.'), ('Separate burns are as good as combined.', 'Combined burns save Δv.'), ('Any launch site can reach any inclination directly.', 'Not below its latitude.')],
 'quiz': [_q('Simple plane change costs…', ['2v sin(Δi/2)', 'vΔi²', 'v cos Δi', '0'], 0, 'Velocity triangle.'), _q('Best place for a plane change…', ['apoapsis', 'periapsis', 'node only', 'anywhere'], 0, 'Lowest speed.'),
          _q('Combined burns are…', ['cheaper', 'costlier', 'the same', 'impossible'], 0, 'Law of cosines.'), _q('Minimum direct inclination equals…', ['launch latitude', '0', '90°', 'longitude'], 0, 'Geometry.')],
 'cards': [('Plane change', '2v sin(Δi/2).'), ('Combined', 'Law of cosines.'), ('Where', 'At low speed.'), ('Launch latitude', 'Minimum inclination.'), ('Node change', 'Spherical trig.'), ('GEO', 'Remove inclination at apogee.')],
 'planet': {'text': ['NASA’s Landsat 9 page notes that the satellite was launched into Landsat 7’s orbit to keep 8-day repeat coverage together with Landsat 8, and that the spacecraft carries enough fuel to operate for at least 10 years against a 5-year design life.',
                     'Placing a satellite precisely in another’s orbit plane, and keeping it there, is plane-change and phasing work. Fuel saved by good maneuver planning becomes extra years of free Earth data.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Linear Algebra', 'Linear_Algebra.html')],
            'src': [_L9]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on plane changes.'), (_BSF[0], _BSF[1], 'Free NASA guide.'), (_MITD[0], _MITD[1], 'MIT dynamics.'), _RE]})
UNITS.append(
{'id': 'u6', 'title': 'Rockets, Δv Budgets and Staging', 'weeks': 'Week 8',
 'summary': 'The Tsiolkovsky rocket equation, specific impulse and exhaust speed, mass ratio and propellant fraction, thrust, staging, gravity and drag losses on ascent, and building a mission Δv budget.',
 'objectives': ['Apply the rocket equation.', 'Relate specific impulse, exhaust speed and thrust.', 'Show why staging helps.', 'Build a simple Δv budget.'],
 'concepts': ['The rocket equation: Δv = I_sp g₀ ln(m₀/m_f), where m₀/m_f is the mass ratio. Exhaust speed v_e = I_sp g₀.',
              'Thrust F = ṁ v_e = ṁ I_sp g₀.',
              'Because Δv grows only with the log of the mass ratio, a single stage to orbit needs most of its mass to be propellant. Staging drops empty tanks and engines so later stages push less dead mass.',
              'Reaching low orbit takes about 9.3–10 km/s of Δv in practice (a textbook range): about 7.7–7.8 km/s of orbital speed plus gravity and drag losses, less a boost from Earth’s rotation for eastward launches.',
              'A mission Δv budget adds every maneuver: launch, transfers, plane changes, station-keeping and disposal, plus margin.'],
 'eqs': [('\\Delta v=I_{sp}g_0\\ln\\frac{m_0}{m_f}', 'Rocket equation'), ('v_e=I_{sp}g_0', 'Exhaust speed'), ('F=\\dot m\\,I_{sp}g_0', 'Thrust'), ('\\frac{m_0}{m_f}=e^{\\Delta v/(I_{sp}g_0)}', 'Required mass ratio')],
 'worked': [
  _w('A stage with I_sp = 300 s has a mass ratio of 4. Find Δv.', ['Δv = 300 × 9.80665 × ln 4.'], 'Δv = 4.08 km/s.'),
  _w('What mass ratio gives 9.4 km/s with I_sp = 350 s in one stage?', ['m₀/m_f = exp(9400/(350 × 9.80665)).'], '15.5, so 93.5% of liftoff mass is propellant.'),
  _w('Two stages, each I_sp = 300 s and mass ratio 3. Total Δv?', ['Δv = 2 × 300 × 9.80665 × ln 3.'], 'Δv = 6.46 km/s.')],
 'practice': [('Find the thrust for ṁ = 100 kg/s at I_sp = 300 s.', '294 kN.'), ('Find v_e for I_sp = 450 s.', '4.41 km/s.'),
              ('Double the mass ratio from 4 to 8. Δv?', 'Rises by 300 × 9.807 × ln 2 = 2.04 km/s, not doubled.'), ('Why does staging help?', 'Later stages do not carry empty tanks.')],
 'misc': [('Doubling propellant doubles Δv.', 'Δv grows with the log of mass ratio.'), ('I_sp is measured in m/s.', 'In seconds; v_e = I_spg₀.'), ('Orbit needs only 7.7 km/s.', 'Losses add 1.5–2 km/s.')],
 'quiz': [_q('Δv = …', ['I_sp g₀ ln(m₀/m_f)', 'I_sp m₀', 'g₀ m_f', 'm₀/m_f'], 0, 'Tsiolkovsky.'), _q('Thrust = …', ['ṁ I_sp g₀', 'm g₀', 'I_sp/ṁ', 'Δv/t'], 0, 'Momentum flux.'),
          _q('Staging helps by…', ['dropping dead mass', 'adding fuel', 'raising g₀', 'nothing'], 0, 'Mass ratio.'), _q('Low-orbit Δv is about…', ['9.4 km/s', '3 km/s', '20 km/s', '1 km/s'], 0, 'With losses.')],
 'cards': [('Rocket equation', 'Δv = v_e ln(m₀/m_f).'), ('I_sp', 'Seconds; v_e/g₀.'), ('Thrust', 'ṁ v_e.'), ('Mass ratio', 'm₀/m_f.'), ('Staging', 'Drop empty mass.'), ('Δv budget', 'Sum of all maneuvers + margin.')],
 'planet': {'text': ['NASA reports that DART launched on November 24, 2021 (EST) on a SpaceX Falcon 9 from Vandenberg Space Force Base in California, and struck Dimorphos, a moonlet just 160 meters across orbiting the 780-meter asteroid Didymos, on September 26, 2022.',
                     'NASA notes the collision happened at roughly 22,530 km/h. Getting a spacecraft there at that speed and on the right path started with this unit’s Δv budget.'],
            'site': [('Thermodynamics', 'Thermodynamics.html'), ('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html')],
            'src': [_DART, _DARTR]},
 'res': [_RR, ('NASA Glenn: Rocket thrust', 'https://www.grc.nasa.gov/www/k-12/rocket/rktpow.html', 'Free NASA page.'), (_BSF[0], _BSF[1], 'Free NASA guide.'), (_MIT[0], _MIT[1], 'MIT notes.')]})
UNITS.append(
{'id': 'u7', 'title': 'Perturbations: Earth’s Bulge, Drag and Sun-Synchronous Orbits', 'weeks': 'Weeks 9–10',
 'summary': 'Why real orbits drift, Earth’s oblateness and J₂, regression of the node and rotation of periapsis, sun-synchronous orbits, frozen and critically inclined orbits, atmospheric drag and orbit decay, and third-body and solar pressure effects.',
 'objectives': ['Compute nodal regression from J₂.', 'Find the inclination for a sun-synchronous orbit.', 'Explain orbit decay from drag.', 'Name other perturbations.'],
 'concepts': ['Earth bulges at the equator. Its J₂ term (1.0826 × 10⁻³) makes the orbit plane precess: dΩ/dt = −1.5 n J₂ (R/p)² cos i, with p = a(1 − e²).',
              'Prograde orbits (i < 90°) regress westward; retrograde orbits (i > 90°) advance eastward.',
              'A sun-synchronous orbit picks i so the plane advances 360° per year, about 0.9856° per day, keeping the same local solar time at each pass.',
              'In low orbit, atmospheric drag slowly removes energy, lowering the orbit until the spacecraft reenters. Drag grows sharply when solar activity heats the upper atmosphere.',
              'Other perturbations: Moon and Sun gravity (important for GEO), solar radiation pressure, and higher gravity harmonics.'],
 'eqs': [('\\dot\\Omega=-\\frac32nJ_2\\left(\\frac Rp\\right)^2\\cos i', 'Nodal regression'), ('\\dot\\Omega_{SS}=\\frac{360°}{365.2422\\ \\text{d}}', 'Sun-synchronous rate'), ('\\cos i=-\\frac{\\dot\\Omega_{SS}}{1.5nJ_2(R/p)^2}', 'Sun-synchronous inclination'), ('n=\\sqrt{\\mu/a^3}', 'Mean motion')],
 'worked': [
  _w('Find the inclination for a sun-synchronous circular orbit at 705 km.', ['r = 7083 km; n = √(μ/r³).', 'Required rate 0.9856°/day = 1.991 × 10⁻⁷ rad/s.', 'cos i = −rate/(1.5nJ₂(R/r)²).'], 'i = 98.2°, exactly Landsat 9’s inclination.'),
  _w('Check the nodal rate for Landsat 9 (705 km, 98.2°).', ['dΩ/dt = −1.5nJ₂(R/r)² cos 98.2°.'], '+0.985° per day, matching the 0.9856° per day the Sun moves.'),
  _w('Find the nodal regression of a 400 km orbit at 51.6°.', ['Same formula with r = 6778 km and cos 51.6°.'], '−5.00° per day (westward).')],
 'practice': [('Is a sun-synchronous orbit prograde or retrograde?', 'Slightly retrograde (i > 90°).'), ('What does J₂ do to a polar orbit (i = 90°)?', 'Nothing to the node: cos 90° = 0.'),
              ('Why do low satellites need reboosts?', 'Drag lowers them.'), ('Which perturbation matters most for GEO inclination?', 'Moon and Sun gravity.')],
 'misc': [('Orbit planes are fixed in space.', 'J₂ makes them precess.'), ('Sun-synchronous means the satellite sees the Sun all the time.', 'It means the same local solar time each pass.'), ('Drag only matters below 100 km.', 'It shapes orbits up to several hundred km.')],
 'quiz': [_q('J₂ causes…', ['nodal precession', 'escape', 'more mass', 'nothing'], 0, 'Oblateness.'), _q('Sun-synchronous node rate…', ['0.9856°/day', '0', '360°/day', '1°/hour'], 0, 'One cycle per year.'),
          _q('Sun-synchronous inclinations are…', ['slightly over 90°', 'near 0°', '45°', '28.5°'], 0, 'cos i < 0.'), _q('Drag makes LEO orbits…', ['decay', 'grow', 'stay', 'tilt'], 0, 'Energy loss.')],
 'cards': [('J₂', '1.0826 × 10⁻³.'), ('Nodal rate', '−1.5nJ₂(R/p)² cos i.'), ('Sun-synchronous', '+0.9856°/day.'), ('Retrograde node', 'Advances east.'), ('Drag', 'Decay and reentry.'), ('GEO perturbation', 'Sun and Moon.')],
 'planet': {'text': ['NASA lists Landsat 9 in a near-polar, sun-synchronous orbit at 705 km and 98.2° inclination, crossing the equator at about 10:12 a.m. local time. Landsat 9 and Landsat 8 together image the same place every 8 days, enabling near-weekly deforestation alerts, water-quality monitoring and crop reports.',
                     'NASA notes that Landsat’s free, public data contributed an estimated $25.6 billion to the U.S. economy in 2023. The steady morning light that makes those images comparable comes straight from J₂ and this unit’s sun-synchronous condition.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Oceans', 'Oceans.html')],
            'src': [_L9]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on perturbations.'), (_BSF5[0], _BSF5[1], 'Free NASA chapter.'), (_L9[0], _L9[1], 'Landsat 9 orbit facts.'), (_MITD[0], _MITD[1], 'MIT dynamics.')]})
UNITS.append(
{'id': 'u8', 'title': 'Ground Tracks, Coverage and Constellations', 'weeks': 'Week 11',
 'summary': 'Ground tracks and the westward shift per orbit, repeat-ground-track orbits, swath width and revisit time, coverage from GEO, and designing constellations for revisit and coverage.',
 'objectives': ['Compute the ground-track shift per orbit.', 'Find orbits per repeat cycle.', 'Relate swath width to revisit.', 'Explain why two satellites halve revisit time.'],
 'concepts': ['As Earth turns beneath an orbit, each ground track shifts west by Δλ = 360° × T/T_sidereal per orbit.',
              'A repeat-ground-track orbit makes a whole number of orbits in a whole number of days, so the pattern repeats exactly.',
              'A sensor with swath width w covers the equator in roughly (circumference)/w passes, which sets the minimum repeat cycle.',
              'Adding satellites in the same orbit, evenly spaced, divides the revisit time.',
              'A single GEO satellite sees roughly 40% of Earth’s surface (a textbook value), but at low resolution near the edges; a few spaced around the equator cover all longitudes except the polar regions.'],
 'eqs': [('\\Delta\\lambda=360°\\frac{T}{T_{sid}}', 'Ground-track shift'), ('kT=jT_{day}', 'Repeat condition'), ('N_{pass}\\approx\\frac{2\\pi R}{w}', 'Passes to cover the equator'), ('t_{revisit}=\\frac{t_{repeat}}{N_{sat}}', 'Constellation revisit')],
 'worked': [
  _w('Find the ground-track shift per orbit for a 98.87 min orbit.', ['Δλ = 360 × 98.87 × 60/86,164.1.'], 'Δλ = 24.8°, about 2760 km at the equator.'),
  _w('How many orbits does that satellite make in 16 days?', ['16 × 14.564.'], 'About 233 orbits, so a 16-day repeat cycle fits.'),
  _w('Two identical satellites share a 16-day repeat orbit, evenly spaced. Revisit?', ['16/2.'], '8 days, as NASA reports for Landsat 8 and 9.')],
 'practice': [('How many 185 km swaths span the equator (40,075 km)?', '40,075/185 = 216.6, so about 217.'), ('Why do ground tracks shift west?', 'Earth rotates east under the orbit.'),
              ('What does a GEO ground track look like?', 'A point (or small figure-eight if inclined).'), ('How would three satellites change the 16-day revisit?', 'About 5.33 days.')],
 'misc': [('Ground tracks repeat every orbit.', 'Only after a whole repeat cycle.'), ('More altitude always means better coverage.', 'Resolution falls with altitude.'), ('GEO sees the whole Earth.', 'About 40%, poorly near the poles.')],
 'quiz': [_q('Ground tracks shift…', ['west', 'east', 'north', 'not at all'], 0, 'Earth rotates east.'), _q('Shift per orbit is…', ['360°T/T_sid', 'T/360', '0', '15°'], 0, 'Earth rotation.'),
          _q('Two evenly spaced satellites…', ['halve revisit', 'double revisit', 'no change', 'quadruple'], 0, 'Spacing.'), _q('A repeat orbit has…', ['whole orbits in whole days', 'e = 1', 'i = 0', 'T = 1 day only'], 0, 'Definition.')],
 'cards': [('Track shift', '360°T/T_sid.'), ('Repeat orbit', 'kT = jT_day.'), ('Swath', 'Width imaged.'), ('Revisit', 'Repeat/N_sat.'), ('GEO view', '≈ 40% of Earth.'), ('Constellation', 'Spaced satellites.')],
 'planet': {'text': ['NASA reports that Landsat 9 has a 16-day repeat cycle with a 185 km swath, collects about 740 scenes a day (almost double its 400-scene requirement), and together with Landsat 8 observes the same location every 8 days.',
                     'NOAA notes that GOES East and GOES West together cover more than half the globe from geostationary orbit. Low polar orbits give sharp, repeated maps; GEO gives constant watch. Good Earth monitoring uses both.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Oceans', 'Oceans.html')],
            'src': [_L9, _GOES]},
 'res': [(_L9[0], _L9[1], 'Landsat 9 coverage facts.'), (_GOES[0], _GOES[1], 'NOAA GOES-R facts.'), (_BSF[0], _BSF[1], 'Free NASA guide.'), (_MIT[0], _MIT[1], 'MIT notes.')]})
UNITS.append(
{'id': 'u9', 'title': 'Interplanetary Transfers and Patched Conics', 'weeks': 'Weeks 12–13',
 'summary': 'Heliocentric Hohmann transfers, transfer time to Mars, departure v∞ and C₃, the patched-conic method, spheres of influence, escape from a parking orbit, synodic periods and launch windows, and gravity assists.',
 'objectives': ['Compute an Earth–Mars Hohmann transfer.', 'Find v∞ and C₃.', 'Find the Δv to depart from low Earth orbit.', 'Compute synodic periods and explain launch windows.'],
 'concepts': ['Far from planets, a spacecraft follows a heliocentric conic with μ_Sun = 1.327 × 10²⁰ m³/s². An Earth–Mars Hohmann transfer is an ellipse from 1 AU to 1.524 AU.',
              'Patched conics: near each planet, use a hyperbola relative to the planet; far away, use the heliocentric ellipse; match velocities at the sphere of influence.',
              'The departure hyperbolic excess speed v∞ is the heliocentric speed needed minus Earth’s orbital speed. C₃ = v∞² is the launch energy.',
              'From a circular parking orbit, the departure burn is Δv = √(v∞² + 2μ/r) − √(μ/r), using the Oberth effect of burning deep in the gravity well.',
              'Launch windows repeat every synodic period, 1/(1/T₁ − 1/T₂): about 2.1 years for Mars. Gravity assists change a spacecraft’s heliocentric speed for free by flying past a planet.'],
 'eqs': [('t=\\pi\\sqrt{\\frac{a^3}{\\mu_\\odot}}', 'Transfer time'), ('v_\\infty=\\sqrt{\\mu_\\odot\\left(\\frac2{r_1}-\\frac1a\\right)}-\\sqrt{\\frac{\\mu_\\odot}{r_1}}', 'Departure excess speed'), ('\\Delta v=\\sqrt{v_\\infty^2+\\frac{2\\mu}{r}}-\\sqrt{\\frac\\mu r}', 'Departure burn'), ('S=\\frac{1}{1/T_1-1/T_2}', 'Synodic period')],
 'worked': [
  _w('Find the Earth–Mars Hohmann transfer time.', ['a = (1 + 1.524)/2 AU = 1.888 × 10¹¹ m.', 't = π√(a³/μ_Sun).'], 't = 259 days.'),
  _w('Find v∞ and C₃ at departure.', ['Earth’s speed √(μ_Sun/1 AU) = 29.78 km/s.', 'Transfer perihelion speed from vis-viva.'], 'v∞ = 2.95 km/s; C₃ = 8.68 km²/s².'),
  _w('Find the departure burn from a 400 km parking orbit.', ['Δv = √(2946² + 2μ/6.778 × 10⁶) − 7669.'], 'Δv = 3.57 km/s.')],
 'practice': [('Find Mars’s orbital period from Kepler’s third law.', '1.524^1.5 = 1.88 years.'), ('Find the Earth–Mars synodic period.', '1/(1 − 1/1.881) = 2.13 years.'),
              ('Why burn deep in a gravity well?', 'The Oberth effect: more kinetic energy per Δv.'), ('Does a gravity assist change speed relative to the planet?', 'No, only relative to the Sun.')],
 'misc': [('You can launch to Mars any time cheaply.', 'Only in windows every 2.1 years.'), ('v∞ equals the burn Δv.', 'The burn from LEO is larger.'), ('Gravity assists break energy conservation.', 'The planet loses a tiny amount.')],
 'quiz': [_q('Earth–Mars Hohmann takes about…', ['259 days', '30 days', '3 years', '1 day'], 0, 'Half the ellipse period.'), _q('C₃ is…', ['v∞²', 'v∞', 'Δv²', 'μ/r'], 0, 'Launch energy.'),
          _q('Mars windows repeat every…', ['2.1 years', '1 year', '6 months', '10 years'], 0, 'Synodic period.'), _q('Patched conics switch frames at…', ['the sphere of influence', 'apoapsis', 'the Moon', 'random'], 0, 'Definition.')],
 'cards': [('Heliocentric', 'μ_Sun = 1.327 × 10²⁰.'), ('Patched conics', 'Hyperbola + ellipse.'), ('v∞', 'Excess speed.'), ('C₃', 'v∞².'), ('Synodic period', '1/(1/T₁ − 1/T₂).'), ('Gravity assist', 'Free heliocentric Δv.')],
 'planet': {'text': ['NASA calls DART the first-ever mission dedicated to demonstrating asteroid deflection by changing an asteroid’s motion through kinetic impact. Before the encounter, NASA defined success as a change in Dimorphos’ orbit period of 73 seconds or more; the measured change of 32 minutes exceeded that by more than 25 times.',
                     'NASA notes that neither Dimorphos nor Didymos posed any hazard to Earth before or after the test. Planetary defense depends on exactly the interplanetary trajectory tools in this unit.'],
            'site': [('Physics I', 'Physics_I.html'), ('Solutions', 'Solutions.html')],
            'src': [_DARTR]},
 'res': [(_BSF[0], _BSF[1], 'Free NASA guide to interplanetary trajectories.'), (_EYES[0], _EYES[1], 'Real interplanetary paths.'), (_MIT[0], _MIT[1], 'MIT notes.'), ('PhET: My Solar System', _PH + 'my-solar-system', 'Multi-body orbits.')]})
UNITS.append(
{'id': 'u10', 'title': 'Space Sustainability: Debris, Disposal and Planetary Defense', 'weeks': 'Weeks 14–15',
 'summary': 'The orbital debris environment, collision speeds and energies, the Kessler cascade, end-of-life disposal and deorbit Δv, graveyard orbits for GEO, conjunction screening and collision avoidance, and kinetic-impact planetary defense.',
 'objectives': ['Compute the energy of a debris impact.', 'Size a deorbit burn.', 'Explain the Kessler cascade.', 'Quantify the DART result.'],
 'concepts': ['Low Earth orbit holds millions of pieces of debris: dead satellites, rocket parts, fragments and paint flecks. At orbital speeds even tiny pieces carry enormous energy.',
              'Kinetic energy ½mv² grows with the square of speed: a 1 g fragment at 10 km/s (a sample relative speed) carries 50 kJ.',
              'Collisions make more fragments, which cause more collisions: the Kessler cascade. Limiting new debris is far cheaper than removing it.',
              'Disposal: LEO satellites lower their perigee so drag brings them down; GEO satellites are raised to a graveyard orbit a few hundred kilometres higher.',
              'Operators screen for close approaches (conjunctions) and make small avoidance burns when the collision probability is too high.'],
 'eqs': [('E_k=\\tfrac12mv^2', 'Impact energy'), ('\\Delta v_{deorbit}=v_c-v_a', 'Perigee-lowering burn'), ('\\frac{\\Delta T}{T}', 'Fractional period change'), ('v_a=\\sqrt{\\mu\\left(\\frac2{r}-\\frac1a\\right)}', 'Vis-viva after the burn')],
 'worked': [
  _w('Convert NASA’s 18,000 mph debris speed to km/s.', ['18,000 × 0.44704 m/s.'], '8.05 km/s.'),
  _w('Find the kinetic energy of a 1 g fragment at a 10 km/s relative speed (sample value).', ['E = ½ × 0.001 × 10,000².'], 'E = 50 kJ from a fragment the mass of a paper clip.'),
  _w('DART shortened Dimorphos’ 11 h 55 min (715 min) orbit by 32 minutes. Find the fractional change and the margin over NASA’s 73 s success threshold.', ['32/715.', '1920 s/73 s.'], '4.48% shorter; 26.3 times the threshold.')],
 'practice': [('Find the deorbit Δv from 700 km to a 200 km perigee.', '139 m/s (Unit 4).'), ('Within how many years must LEO satellites be disposed of under the FCC rule?', '5 years after mission end.'),
              ('Why is preventing debris cheaper than removing it?', 'Removal needs a dedicated spacecraft for each object.'), ('Where do GEO satellites go at end of life?', 'A graveyard orbit above GEO.')],
 'misc': [('Space is too big to fill up.', 'Useful orbits are limited and crowded.'), ('Small debris is harmless.', 'Energy grows with v².'), ('Deorbiting needs huge burns.', 'Lowering perigee from 700 km takes about 139 m/s.')],
 'quiz': [_q('Debris energy grows with…', ['v²', 'v', '√v', '1/v'], 0, '½mv².'), _q('The Kessler cascade is…', ['collisions making more debris', 'a launch', 'a transfer', 'drag'], 0, 'Chain reaction.'),
          _q('FCC LEO disposal rule…', ['5 years', '25 years', '1 year', 'none'], 0, 'FCC-22-74.'), _q('DART changed the period by…', ['32 min', '73 s', '12 h', '0'], 0, 'NASA result.')],
 'cards': [('Debris', 'Millions of pieces in LEO.'), ('Impact energy', '½mv².'), ('Kessler', 'Cascade of collisions.'), ('Deorbit', 'Lower perigee.'), ('Graveyard', 'Above GEO.'), ('DART', '32-minute period change.')],
 'planet': {'text': ['NASA’s Headquarters Library notes that there are millions of pieces of space junk in low Earth orbit, moving as fast as 18,000 miles per hour, almost seven times faster than a bullet, with close to 6,000 tons of material in low Earth orbit. NASA’s Orbital Debris Program began in 1979 at Johnson Space Center.',
                     'The FCC’s 2022 rule requires low-Earth-orbit operators to dispose of satellites within 5 years of completing their missions. Planning that disposal burn from day one is now part of responsible mission design.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_DEB, _FCC]},
 'res': [(_ODPO[0], _ODPO[1], 'NASA Orbital Debris Program Office.'), (_DEB[0], _DEB[1], 'NASA debris reading list.'), (_DARTR[0], _DARTR[1], 'NASA DART result.'), (_MIT[0], _MIT[1], 'MIT notes.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Circular orbits in PhET', 'week': 'Week 1',
 'goal': 'Explore how orbit speed and period change with distance in PhET Gravity and Orbits, then compute real Earth orbits.',
 'eq': ('v_c=\\sqrt{\\mu/r},\\ \\ T=2\\pi\\sqrt{r^3/\\mu}', 'Circular orbits'),
 'steps': ['Open PhET Gravity and Orbits; launch the satellite at different distances and speeds.', 'Find the speed that gives a circle at each distance.', 'Compute v and T for a 400 km orbit, Landsat’s 705 km orbit and GEO.', 'Compare the trend with the simulation.'],
 'table': (['Orbit', 'v (km/s)', 'T'], [['400 km', '7.67', '92.6 min'], ['705 km', '7.50', '98.9 min'], ['GEO (35,786 km)', '3.07', '23.93 h']]),
 'note': 'Computed values.',
 'calc': ['v(705 km) = √(3.986 × 10¹⁴/7.083 × 10⁶) = 7.50 km/s.', 'T(GEO) = 86,164 s = 23.93 h.'],
 'safety': ['Computer only.'], 'home': ['Any browser works.'],
 'sims': [('PhET: Gravity and Orbits', _PH + 'gravity-and-orbits')],
 'planet': 'NOAA notes GOES satellites orbit 22,236 miles above the equator.', 'planet_src': [_GOES]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Kepler’s third law with real planets', 'week': 'Week 3',
 'goal': 'Check T² ∝ a³ for planets and explore elliptical orbits in PhET Kepler’s Laws.',
 'eq': ('T_{yr}=a_{AU}^{3/2}', 'Kepler’s third law (Sun)'),
 'steps': ['Explore PhET Kepler’s Laws: change eccentricity and watch equal areas swept in equal times.', 'Enter planet semi-major axes in AU.', 'Compute T = a^1.5 in years.', 'Plot log T against log a and find the slope.'],
 'table': (['Planet', 'a (AU)', 'T (years)'], [['Earth', '1.000', '1.000'], ['Mars', '1.524', '1.881'], ['Jupiter', '5.203', '11.87']]),
 'note': 'Semi-major axes are textbook values; the slope of log T against log a is 1.5.',
 'calc': ['T(Mars) = 1.524^1.5 = 1.881 years.', 'T(Jupiter) = 5.203^1.5 = 11.87 years.'],
 'safety': ['Computer only.'], 'home': ['Any browser and spreadsheet work.'],
 'sims': [('PhET: Kepler’s Laws', _PH + 'keplers-laws'), ('PhET: My Solar System', _PH + 'my-solar-system')],
 'planet': 'NASA timed Dimorphos’ orbit before and after DART to measure a 32-minute change.', 'planet_src': [_DARTR]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Hohmann transfer calculator', 'week': 'Week 6',
 'goal': 'Build a spreadsheet that computes both burns, total Δv and transfer time for any pair of circular orbits.',
 'eq': ('a=\\frac{r_1+r_2}{2},\\ \\ v^2=\\mu\\left(\\frac2r-\\frac1a\\right)', 'Hohmann transfer'),
 'steps': ['Enter μ and the two radii.', 'Compute circular speeds, transfer-orbit speeds, both burns and the transfer time.', 'Run LEO (400 km) to GEO and LEO to a 20,200 km medium orbit.', 'Add a plane-change option for the second burn.'],
 'table': (['Transfer', 'Δv₁ (km/s)', 'Δv₂ (km/s)', 'Total', 'Time (h)'], [['400 km → GEO', '2.398', '1.456', '3.854', '5.29'], ['400 km → 20,200 km', '2.012', '1.404', '3.416', '2.98']]),
 'note': 'Computed values, coplanar.',
 'calc': ['Δv₁(GEO) = 10.066 − 7.669 = 2.398 km/s.', 'Time(20,200 km) = π√(a³/μ) = 2.98 h.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_EYES[0], _EYES[1])],
 'planet': 'The FCC requires LEO satellites to be disposed of within 5 years of mission end.', 'planet_src': [_FCC]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Rocket equation and staging', 'week': 'Week 8',
 'goal': 'See how Δv grows with mass ratio and how staging beats a single stage.',
 'eq': ('\\Delta v=I_{sp}g_0\\ln\\frac{m_0}{m_f}', 'Rocket equation'),
 'steps': ['Set I_sp = 300 s.', 'Compute Δv for mass ratios 2, 4 and 8.', 'Compare one stage of ratio 9 with two stages of ratio 3.', 'Find the mass ratio for 9.4 km/s at I_sp = 350 s.'],
 'table': (['Mass ratio', 'Δv (km/s)'], [['2', '2.04'], ['4', '4.08'], ['8', '6.12']]),
 'note': 'Computed values; one stage of ratio 9 and two stages of ratio 3 give the same ideal Δv (6.46 km/s), but the staged rocket needs far less structure per stage.',
 'calc': ['Δv(8) = 300 × 9.80665 × ln 8 = 6.12 km/s.', 'Two stages of 3: 2 × 300 × 9.80665 × ln 3 = 6.46 km/s.'],
 'safety': ['Computer only. Do not build or fly propellant rockets for this lab.'], 'home': ['Any spreadsheet works.'],
 'sims': [('NASA Glenn: Rocket thrust', 'https://www.grc.nasa.gov/www/k-12/rocket/rktpow.html')],
 'planet': 'NASA’s DART launched on a Falcon 9 from Vandenberg in November 2021.', 'planet_src': [_DART]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Designing a sun-synchronous orbit', 'week': 'Week 10',
 'goal': 'Compute the sun-synchronous inclination for several altitudes and check it against Landsat 9.',
 'eq': ('\\cos i=-\\frac{\\dot\\Omega_{SS}}{1.5nJ_2(R/r)^2}', 'Sun-synchronous condition'),
 'steps': ['Enter μ, R, J₂ and the required 0.9856°/day.', 'Compute i for circular orbits at 500, 705 and 800 km.', 'Compare 705 km with Landsat 9’s published 98.2°.', 'Plot i against altitude.'],
 'table': (['Altitude (km)', 'i (deg)'], [['500', '97.40'], ['705', '98.21'], ['800', '98.60']]),
 'note': 'Computed values; Landsat 9’s published inclination is 98.2°.',
 'calc': ['n(705 km) = √(μ/7.083³ × 10¹⁸) = 1.059 × 10⁻³ rad/s.', 'i(705) = 98.21°.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_L9[0], _L9[1])],
 'planet': 'NASA says Landsat 9 crosses the equator at about 10:12 a.m. local time.', 'planet_src': [_L9]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Ground tracks in NASA’s Eyes', 'week': 'Week 11',
 'goal': 'Watch real Earth-observing satellites in NASA’s Eyes and compute their ground-track shift and repeat cycle.',
 'eq': ('\\Delta\\lambda=360°\\frac{T}{T_{sid}}', 'Ground-track shift'),
 'steps': ['Open NASA’s Eyes and follow an Earth-observing satellite for a few orbits.', 'Note how each track lands west of the last.', 'Compute the shift for a 98.87 min orbit.', 'Find how many orbits fit in 16 days.'],
 'table': (['Quantity', 'Value'], [['Period', '98.87 min'], ['Shift per orbit', '24.8°'], ['Shift at equator', '2760 km'], ['Orbits in 16 days', '233']]),
 'note': 'Computed for a 705 km circular orbit.',
 'calc': ['Δλ = 360 × 5932/86,164 = 24.8°.', '16 × 14.564 = 233 orbits.'],
 'safety': ['Computer only.'], 'home': ['Any browser works.'],
 'sims': [(_EYES[0], _EYES[1])],
 'planet': 'NASA reports Landsat 8 and 9 together revisit every place every 8 days.', 'planet_src': [_L9]})
SCHEDULE = [(1, 'u1', 'Gravity, two-body problem, circular orbits; Lab A', 'OpenStax UP1 13.4–13.5'), (2, 'u2', 'Energy, angular momentum, conics', 'MIT 16.346'),
            (3, 'u2', 'Vis-viva and orbital elements; Lab B', 'NASA Basics of Space Flight'), (4, 'u3', 'Kepler’s equation and time of flight', 'MIT 16.346'),
            (5, 'u4', 'Impulsive maneuvers and Hohmann transfers', 'MIT 16.346'), (6, 'u4', 'Bi-elliptic, phasing, deorbit; Lab C', 'MIT 16.346'),
            (7, 'u5', 'Plane changes and combined burns; midterm practice', 'MIT 16.346'), (8, 'u6', 'Rocket equation, staging, Δv budgets; Lab D', 'OpenStax UP1 9.7'),
            (9, 'u7', 'J₂ and nodal regression', 'MIT 16.346'), (10, 'u7', 'Sun-synchronous orbits and drag; Lab E', 'NASA Landsat 9'),
            (11, 'u8', 'Ground tracks, coverage, constellations; Lab F', 'NASA Eyes'), (12, 'u9', 'Heliocentric transfers and patched conics', 'NASA Basics of Space Flight'),
            (13, 'u9', 'Launch windows and gravity assists', 'NASA Basics of Space Flight'), (14, 'u10', 'Debris, disposal and collision avoidance', 'NASA ODPO; FCC'),
            (15, 'u10', 'Planetary defense; final practice', 'NASA DART')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Find the circular speed 1000 km above Earth.', ['√(3.986 × 10¹⁴/7.378 × 10⁶).'], '7.35 km/s.'),
  ('Find the period of that orbit.', ['2π√(r³/μ).'], '105.1 min.'),
  ('An orbit has r_p = 7000 km and r_a = 14,000 km. Find e.', ['7000/21,000.'], '0.333.'),
  ('Find the speed at perigee of that orbit.', ['√(μ(2/7 × 10⁶ − 1/1.05 × 10⁷)).'], '8.71 km/s.'),
  ('Find the Δv to change inclination by 5° at 7.5 km/s.', ['2 × 7.5 × sin 2.5°.'], '0.654 km/s.')]),
 ('Final practice set (all units)', [
  ('Find Δv for I_sp = 320 s and mass ratio 5.', ['320 × 9.80665 × ln 5.'], '5.05 km/s.'),
  ('Find the nodal rate at 600 km, i = 97.8°.', ['−1.5nJ₂(R/r)² cos i.'], '+0.987°/day.'),
  ('Find the ground-track shift per orbit for a 100 min orbit.', ['360 × 6000/86,164.1.'], '25.1°.'),
  ('Find the Earth–Venus Hohmann transfer time (Venus at 0.723 AU).', ['π√(a³/μ_Sun) with a = 0.8615 AU.'], '146 days.'),
  ('Find the energy of a 10 g fragment at 8 km/s.', ['½ × 0.01 × 8000².'], '320 kJ.'),
  ('Find the synodic period of Earth and Jupiter (11.87 years).', ['1/(1 − 1/11.87).'], '1.092 years.')])]
FORMULAS = ['v_c=\\sqrt{\\mu/r},\\ T=2\\pi\\sqrt{a^3/\\mu},\\ v_{esc}=\\sqrt{2\\mu/r}', '\\varepsilon=-\\mu/(2a),\\ v^2=\\mu(2/r-1/a)', 'r=(h^2/\\mu)/(1+e\\cos\\nu),\\ e=(r_a-r_p)/(r_a+r_p)', 'M=E-e\\sin E,\\ n=\\sqrt{\\mu/a^3}',
            '\\Delta v_{Hohmann}=(v_{p}-v_{c1})+(v_{c2}-v_{a})', '\\Delta v=2v\\sin(\\Delta i/2),\\ \\Delta v^2=v_1^2+v_2^2-2v_1v_2\\cos\\Delta i', '\\Delta v=I_{sp}g_0\\ln(m_0/m_f)',
            '\\dot\\Omega=-\\tfrac32nJ_2(R/p)^2\\cos i', '\\Delta\\lambda=360°T/T_{sid}', 'v_\\infty=v_{transfer}-v_{planet},\\ C_3=v_\\infty^2,\\ S=1/(1/T_1-1/T_2)', 'E_k=\\tfrac12mv^2']
GLOSSARY = sorted([('Apoapsis', 'Farthest point of an orbit.'), ('C₃', 'Launch energy, the square of v∞.'), ('Conjunction', 'Close approach between two space objects.'), ('Δv', 'Change in velocity a maneuver requires.'),
    ('Eccentricity', 'How stretched an orbit is.'), ('Geostationary orbit', 'Equatorial orbit with a one-sidereal-day period.'), ('Ground track', 'Path of the point directly below a satellite.'), ('Hohmann transfer', 'Two-burn transfer on a tangent ellipse.'),
    ('Inclination', 'Tilt of the orbit plane from the equator.'), ('J₂', 'Earth’s oblateness term.'), ('Kepler’s equation', 'M = E − e sin E.'), ('Kessler cascade', 'Chain reaction of debris collisions.'), ('Mean anomaly', 'Angle that grows uniformly with time.'),
    ('Patched conics', 'Joining planet-centered and Sun-centered conics.'), ('Periapsis', 'Closest point of an orbit.'), ('Specific impulse', 'Thrust per propellant weight flow, in seconds.'), ('Sun-synchronous orbit', 'Orbit whose plane keeps a fixed angle to the Sun.'),
    ('Synodic period', 'Time between repeat alignments of two orbiting bodies.'), ('True anomaly', 'Angle from periapsis to the spacecraft.'), ('Vis-viva equation', 'v² = μ(2/r − 1/a).')])
RUBRIC = [('4 · Mastery', 'Sketches the orbit and maneuvers, picks vis-viva, Kepler or the rocket equation correctly, keeps units in SI, and checks answers against limits.'), ('3 · Proficient', 'Solves the practice problems with occasional unit slips.'),
          ('2 · Developing', 'Follows worked examples but mixes up circular and transfer speeds.'), ('1 · Beginning', 'Plugs numbers into formulas without a sketch; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    mu = 3.986e14; R = 6378e3; g0 = 9.80665; J2 = 1.08263e-3; Ts = 86164.1; mus = 1.327e20; AU = 1.496e11
    vc = lambda r: sqrt(mu / r); T = lambda a: 2 * pi * sqrt(a ** 3 / mu); vv = lambda r, a: sqrt(mu * (2 / r - 1 / a))
    r4 = R + 400e3; r7 = R + 705e3; rg = (mu * (Ts / (2 * pi)) ** 2) ** (1 / 3); at = (r4 + rg) / 2
    d1 = vv(r4, at) - vc(r4); d2 = vc(rg) - vv(rg, at); tt = pi * sqrt(at ** 3 / mu)
    def kep(M, e):
        E = M
        for _ in range(50): E -= (E - e * sin(E) - M) / (1 - e * cos(E))
        return E
    E1 = kep(1, .3); nu1 = 2 * atan(sqrt(1.3 / .7) * tan(E1 / 2))
    req = radians(360 / 365.2422) / 86400
    node = lambda r, i: -1.5 * sqrt(mu / r ** 3) * J2 * (R / r) ** 2 * cos(radians(i))
    iss = lambda r: degrees(acos(-req / (1.5 * sqrt(mu / r ** 3) * J2 * (R / r) ** 2)))
    aM = (1 + 1.524) / 2 * AU; vE = sqrt(mus / AU); vinf = sqrt(mus * (2 / AU - 1 / aM)) - vE
    ve3 = 300 * g0
    hm = lambda h1, h2: (lambda a1, a2, at_: (vv(a1, at_) - vc(a1), vc(a2) - vv(a2, at_), pi * sqrt(at_ ** 3 / mu)))(R + h1, R + h2, (2 * R + h1 + h2) / 2)
    m1, m2, mt = hm(400e3, 20200e3)
    rk = R + 1000e3; r6 = R + 600e3
    r = [
     ('u1 v4', vc(r4), 7668.6), ('u1 T4', T(r4) / 60, 92.6), ('u1 esc4', sqrt(2) * vc(r4), 10.85e3),
     ('u1 rg', rg / 1e3, 42164), ('u1 hg', rg / 1e3 - 6378, 35786), ('u1 mi', (rg / 1e3 - 6378) / 1.609344, 22236), ('u1 vg', vc(rg), 3074.7),
     ('u1 T7', T(r7) / 60, 98.87), ('u1 v7', vc(r7), 7.50e3), ('u1 opd', 1440 / (T(r7) / 60), 14.56), ('u1 Tg', T(rg) / 3600, 23.93),
     ('u3 M', pi / 2 - .3, 1.271), ('u3 E', E1, 1.288), ('u3 nu', nu1, 1.594), ('u3 nud', degrees(nu1), 91.3), ('u3 tt', tt / 3600, 5.29), ('u3 rev', 1440 / 92.56, 15.56),
     ('u4 d1', d1, 2398), ('u4 d2', d2, 1456), ('u4 tot', d1 + d2, 3850), ('u4 t', tt / 3600, 5.29),
     ('u5 pc', 2 * vc(rg) * sin(radians(14.25)), 1513.7), ('u5 comb', sqrt(vv(rg, at) ** 2 + vc(rg) ** 2 - 2 * vv(rg, at) * vc(rg) * cos(radians(28.5))), 1824.1),
     ('u5 sav', 1513.7 + 1456 - 1824.1, 1145.6), ('u5 l10', 2 * vc(r4) * sin(radians(5)), 1336.7), ('u5 60', 2 * sin(radians(30)), 1),
     ('u6 dv', ve3 * log(4), 4078.5), ('u6 mr', exp(9.4e3 / (350 * g0)), 15.466), ('u6 mrp', 1 - 1 / 15.466, .935),
     ('u6 two', 2 * ve3 * log(3), 6464.2), ('u6 ve450', 450 * g0, 4.41e3), ('u6 ln2', ve3 * log(2), 2.04e3),
     ('u7 i', iss(r7), 98.208), ('u7 req', req * 86400 * 180 / pi, .9856), ('u7 reqr', req, 1.991e-7), ('u7 L9', degrees(node(r7, 98.2)) * 86400, .98467), ('u7 iss', degrees(node(r4, 51.6)) * 86400, -5.00),
     ('u8 sh', 360 * T(r7) / Ts, 24.786), ('u8 km', 40075 * T(r7) / Ts, 2759.2), ('u8 233', 16 * 86400 / T(r7), 233.02), ('u8 sw', 40075 / 185, 216.6), ('u8 rv', 16 / 2, 8), ('u8 3s', 16 / 3, 5.33),
     ('u9 t', pi * sqrt(aM ** 3 / mus) / 86400, 258.93), ('u9 vinf', vinf, 2945.9), ('u9 C3', (vinf / 1e3) ** 2, 8.68), ('u9 vE', vE, 29.78e3),
     ('u9 dep', sqrt(vinf ** 2 + 2 * mu / r4) - vc(r4), 3569.4), ('u9 TM', 1.524 ** 1.5, 1.8814), ('u9 syn', 1 / (1 - 1 / 1.8814), 2.1346),
     ('u10 v', 18000 * .44704, 8046.7), ('u10 E', .5 * .001 * 10e3 ** 2, 50e3), ('u10 pc', 32 / 715, .0448), ('u10 x', 1920 / 73, 26.3),
     ('labA v4', vc(r4), 7.67e3), ('labA T4', T(r4) / 60, 92.6), ('labA v7', vc(r7), 7.50e3), ('labA T7', T(r7) / 60, 98.9), ('labA vg', vc(rg), 3.07e3), ('labA Tg', T(rg) / 3600, 23.93), ('labA r7', r7, 7.083e6),
     ('labB E', 1.0 ** 1.5, 1.0), ('labB M', 1.524 ** 1.5, 1.881), ('labB J', 5.203 ** 1.5, 11.87),
     ('labC d1', d1, 2398), ('labC d2', d2, 1456), ('labC t', d1 + d2, 3854), ('labC tt', tt / 3600, 5.29), ('labC m1', m1, 2012), ('labC m2', m2, 1404), ('labC mt', m1 + m2, 3416), ('labC mtt', mt / 3600, 2.98),
     ('labC vp', vv(r4, at), 10066), ('labC vc', vc(r4), 7669),
     ('labD 2', ve3 * log(2), 2.04e3), ('labD 4', ve3 * log(4), 4.08e3), ('labD 8', ve3 * log(8), 6.12e3), ('labD 9', ve3 * log(9), 6.46e3), ('labD 33', 2 * ve3 * log(3), 6.46e3),
     ('labE 500', iss(R + 500e3), 97.40), ('labE 705', iss(r7), 98.21), ('labE 800', iss(R + 800e3), 98.60), ('labE n', sqrt(mu / r7 ** 3), 1.059e-3),
     ('labF T', T(r7) / 60, 98.87), ('labF sh', 360 * T(r7) / Ts, 24.8), ('labF km', 40075 * T(r7) / Ts, 2760), ('labF n', 16 * 86400 / T(r7), 233), ('labF Ts', T(r7), 5932),
     ('mid v', vc(rk), 7.35e3), ('mid T', T(rk) / 60, 105.1), ('mid e', 7000 / 21000, .333), ('mid vp', vv(7e6, 10.5e6), 8.71e3), ('mid pc', 2 * 7.5 * sin(radians(2.5)), .654),
     ('fin dv', 320 * g0 * log(5), 5.05e3), ('fin node', degrees(node(r6, 97.8)) * 86400, .987), ('fin sh', 360 * 6000 / Ts, 25.1),
     ('fin ven', pi * sqrt((.8615 * AU) ** 3 / mus) / 86400, 146), ('fin E', .5 * .01 * 8000 ** 2, 320e3), ('fin syn', 1 / (1 - 1 / 11.87), 1.092),
     ('x a', (1 + .723) / 2, .8615), ('x g0', g0, 9.80665), ('x day', 360 / 365.2422, .9856), ('x 1440', 24 * 60, 1440), ('x mi', 1.609344 * 22236, 35785),
     ('x sp', 2 * pi * 42164 / 23.934, 11069), ('x esc', sqrt(2), 1.414), ('x l2', log(2), .693), ('x l4', log(4), 1.386), ('x l3', log(3), 1.0986),
     ('x s14', sin(radians(14.25)), .2462), ('x s5', sin(radians(5)), .08716), ('x c28', cos(radians(28.5)), .8788), ('x DT', 715 - 32, 683),
     ('x AUkm', AU / 1e3, 1.496e8), ('x J2', J2, 1.08263e-3), ('x Re', R / 1e3, 6378), ('x mu', mu, 3.986e14), ('x mus', mus, 1.327e20),
     ('x rp', 7000 + 14000, 21000), ('x a2', (7000 + 14000) / 2, 10500), ('x vt', 7.5 * 2, 15), ('x g', 6000 / 60, 100), ('x 16d', 16 * 14.564, 233), ('x 1/T', 1 / 11.87, .08425)]
    rp = 6778e3; ra = 42164e3; a2 = (rp + ra) / 2; vp = vv(rp, a2); va = vv(ra, a2); rd = 7078e3; ad = (rd + 6578e3) / 2
    r += [('u2 a', a2 / 1e3, 24471), ('u2 e', (ra - rp) / (ra + rp), .723), ('u2 eps', -mu / (2 * a2), -8.14e6), ('u2 vp', vp, 10.07e3), ('u2 va', va, 1.62e3),
     ('u2 h', rp * vp, 6.82e10), ('u2 h2', 6.778e6 * 10066, 6.82e10), ('u2 T', T(a2) / 3600, 10.58), ('u2 0', 0, 0), ('u2 n6', 6, 6),
     ('u1 r4', 6378 + 400, 6778), ('u1 mph', 7670 * 2.236936, 17154), ('u1 esc7', sqrt(2) * 7.669, 10.85), ('u1 alt', 42164 - 6378, 35786),
     ('u3 M2', 1.5708 - .3, 1.271), ('u3 hf', 10.58 / 2, 5.29), ('u3 E2', E1 / 2, .644), ('u3 n', 1440 / (T(r4) / 60), 15.56),
     ('u4 d1b', 10.066 - 7.669, 2.397), ('u4 d2b', 3.075 - 1.618, 1.457), ('u4 vp', vp, 10066), ('u4 va', va, 1618.2), ('u4 vc', vc(rg), 3074.7), ('u4 de', vc(rd) - vv(rd, ad), 138.66),
     ('u4 first', d1, 2.40e3), ('u4 n2', 2, 2),
     ('u5 pc2', 2 * 3.075 * sin(radians(14.25)), 1.51), ('u5 c2', sqrt(1.618 ** 2 + 3.075 ** 2 - 2 * 1.618 * 3.075 * cos(radians(28.5))), 1.82), ('u5 sep', 1.51 + 1.46, 2.97),
     ('u5 s2', 2.97 - 1.82, 1.15), ('u5 tot', 2.40 + 1.82, 4.22), ('u5 l2', 2 * 7.669 * sin(radians(5)), 1.34), ('u5 h', 28.5 / 2, 14.25),
     ('u6 F', 100 * 300 * g0, 294199.5), ('u6 mr2', exp(9400 / (350 * g0)), 15.5), ('u6 d2', ve3 * log(8) - ve3 * log(4), 2.04e3), ('u6 v', 9.4, 9.4),
     ('u7 r', r7 / 1e3, 7083), ('u7 i2', iss(r7), 98.2), ('u7 L2', degrees(node(r7, 98.2)) * 86400, .985), ('u7 pol', 90, 90),
     ('u8 s2', 360 * 98.87 * 60 / Ts, 24.8), ('u8 n2', 16 * 14.564, 233), ('u8 s3', 40075 / 185, 216.6), ('u8 1440', 1440 / 98.87, 14.56),
     ('u9 a', aM, 1.888e11), ('u9 t2', pi * sqrt(aM ** 3 / mus) / 86400, 259), ('u9 v2', vinf, 2.95e3), ('u9 d2', sqrt(2946 ** 2 + 2 * mu / 6.778e6) - 7669, 3.57e3),
     ('u9 T2', 1.524 ** 1.5, 1.88), ('u9 s2', 1 / (1 - 1 / 1.881), 2.13),
     ('u10 E2', .5 * .001 * 10000 ** 2, 5e4), ('u10 v2', 18000 * .44704 / 1e3, 8.05), ('u10 m', 11 * 60 + 55, 715), ('u10 s', 32 * 60, 1920), ('u10 5', 5, 5)]
    return r
