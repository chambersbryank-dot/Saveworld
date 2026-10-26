"""Spacecraft Design (AERO 430): mission requirements and systems engineering, orbits and environment, power generation, energy storage, thermal control, structures, propulsion and delta-v budgets, attitude control, communications, and reliability and testing.
Oct 25 2026, founder-approved four-year track, senior course 3. Same module fields as fdc.py / prop.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, log, exp, pi, asin, cos, radians, log10
ID = 'scdesign'
STATUS = 'live'
YEAR = 4
PAGE = 'Spacecraft_Design.html'
CODE = 'AERO 430'
TITLE = 'Spacecraft Design'
LAB_NAME = 'Spacecraft design lab'
TAGLINE = 'Subsystems, power, thermal and mission requirements: systems engineering and budgets, orbits and the space environment, solar arrays and batteries, thermal balance, structures, delta-v, attitude control, communications links and reliability, with six labs. Free, self-paced, and tied to NASA’s Landsat 9, Europa Clipper and small-spacecraft technology.'
DESC = 'Free self-study Spacecraft Design: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and spreadsheet labs, practice exams, tied to Landsat 9 Earth observation, Europa Clipper and NASA small-spacecraft power technology.'
ALT = 'The Landsat 9 satellite launches on an Atlas V rocket from Vandenberg Space Force Base on Sept. 27, 2021'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 16.851 Satellite Engineering (Fall 2003)', 'https://ocw.mit.edu/courses/16-851-satellite-engineering-fall-2003/')
_SEH = ('NASA Systems Engineering Handbook', 'https://www.nasa.gov/reference/systems-engineering-handbook/')
_SOA = ('NASA Small Spacecraft Technology State of the Art', 'https://www.nasa.gov/smallsat-institute/sst-soa/')
_PWR = ('NASA Small Spacecraft Technology State of the Art: 3.0 Power (May 2026)', 'https://www.nasa.gov/smallsat-institute/sst-soa/power-subsystems/')
_THM = ('NASA Small Spacecraft Technology State of the Art: Thermal Control', 'https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/')
_L9 = ('NASA Science: Landsat 9', 'https://landsat.gsfc.nasa.gov/satellites/landsat-9/landsat-9-overview/')
_EC = ('NASA Science: Europa Clipper', 'https://science.nasa.gov/mission/europa-clipper/')
_PACE = ('NASA Science: PACE (Plankton, Aerosol, Cloud, ocean Ecosystem)', 'https://science.nasa.gov/mission/pace/')
BANNER = ['images/Landsat9_Launch_KLS04_0013.jpg', 'images/GOES19_GOESU_KSC.jpg', 'images/JPSS2_Atlas_V_Launch_Pad.jpg', 'images/ISS_Flyaround_2021.jpg']
CREDITS = {'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)', 'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC',
           'images/JPSS2_Atlas_V_Launch_Pad.jpg': 'NASA/Liz Wilk (KSC-20221109-PH-LNW01_0001)', 'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester senior spacecraft design course for aerospace engineers. It is modeled on the topics and depth of MIT 16.851 Satellite Engineering (free on MIT OpenCourseWare), using NASA’s free Systems Engineering Handbook and Small Spacecraft Technology State of the Art report, which we link where they help. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (NASA’s Landsat 9, Europa Clipper and PACE missions and NASA’s small-spacecraft technology survey), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a spreadsheet.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Earth-observing satellites are spacecraft design made useful: power, thermal, pointing and communications all have to work for years so scientists can track forests, water, crops and climate.',
                 'Good design also means long life and less waste in orbit. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Orbital Mechanics: orbits, periods and Δv.', 'Thermodynamics: heat transfer and radiation basics.',
           'Circuits: power, voltage and current.', 'Flight Dynamics & Controls and Aerospace Structures: attitude control, stiffness and loads.']
STUDY = ['Start every design from requirements, and keep a budget (mass, power, Δv, link) for every subsystem.', 'Carry margins and say where they live.',
         'Track units: watts versus watt-hours, kelvin for radiation, decibels for links.', 'Check every answer against a real mission’s order of magnitude.',
         'Sketch the spacecraft and its orbit before computing anything.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Blackbody Spectrum and Circuit Construction Kit simulations.', 'Spreadsheet software (any free one works), or Python.',
            'NASA mission pages and the Small Spacecraft Technology report in a web browser.', 'A calculator.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free simulation or a spreadsheet, so there are no physical hazards. Do not build, charge or modify battery packs for this course. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST: CODATA value, Stefan–Boltzmann constant', 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma')
CONSTANTS = [('Earth μ', '398,600.4418 km³/s²'), ('Earth radius (equatorial)', '6378.137 km'), ('Solar flux at 1 AU (textbook value)', '1361 W/m²'),
             ('Stefan–Boltzmann constant', 'σ = 5.670374419 × 10⁻⁸ W/(m²·K⁴)'), ('Speed of light', '299,792,458 m/s (3 × 10⁸ used in examples)'), ('Standard gravity', 'g₀ = 9.80665 m/s²')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, NASA references and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT satellite engineering lectures.'), (_SEH[0], _SEH[1], 'Free NASA handbook.'), (_SOA[0], _SOA[1], 'Free NASA technology survey.'),
          (_PWR[0], _PWR[1], 'Free NASA power chapter.'), ('PhET: Blackbody Spectrum', _PH + 'blackbody-spectrum', 'Thermal radiation interactively.'), ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc', 'Circuits interactively.')]
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Mission Requirements and Systems Engineering', 'weeks': 'Week 1',
 'summary': 'Mission objectives, requirements, the project life cycle, trade studies, subsystem budgets, and design margins.',
 'objectives': ['Turn mission goals into measurable requirements.', 'Build a mass budget with margin.', 'Run a simple weighted trade study.', 'Explain why margins shrink through a project.'],
 'concepts': ['A mission starts with objectives; requirements make them measurable and verifiable (a number, a unit and a test).',
              'Projects move through phases from concept to operations, with reviews that check requirements are met.',
              'Every resource gets a budget: mass, power, Δv, data, pointing and cost, each with a margin.',
              'Early designs carry large margins (often 20–30%, textbook values) because estimates are uncertain; margins shrink as hardware matures.',
              'Trade studies score options against weighted criteria; the weights matter as much as the scores.'],
 'eqs': [('m_{alloc}=m_{est}(1+M)', 'Mass with margin'), ('S=\\sum w_is_i', 'Weighted trade score'), ('\\text{Margin}=\\frac{\\text{Capability}-\\text{Need}}{\\text{Need}}', 'Performance margin'), ('\\sum w_i=1', 'Weights sum to one')],
 'worked': [
  _w('A dry-mass estimate is 800 kg. Allocate with a 20% margin (sample values).', ['800 × 1.20.'], '960 kg.'),
  _w('NASA says Landsat 9 had to collect at least 400 scenes a day and collects 740. Find the margin.', ['(740 − 400)/400.'], '85% above the requirement (740/400 = 1.85).'),
  _w('Option A scores 8 (cost) and 6 (performance); B scores 5 and 9. Weights 0.4 and 0.6. Which wins?', ['A = 3.2 + 3.6 = 6.8.', 'B = 2.0 + 5.4 = 7.4.'], 'B wins, 7.4 to 6.8.')],
 'practice': [('Allocate 1200 kg at 25% margin.', '1500 kg.'), ('If weights flip to 0.6/0.4, who wins?', 'A: 7.2 vs B: 6.6.'),
              ('What makes a requirement verifiable?', 'A measurable value and a test or analysis to check it.'), ('Why carry margin?', 'Estimates grow as designs mature.')],
 'misc': [('Requirements are wishes.', 'They are measurable and verifiable.'), ('Margins are waste.', 'They absorb growth and surprises.'), ('Trade studies are objective.', 'The weights carry judgment.')],
 'quiz': [_q('800 kg + 20%…', ['960 kg', '820 kg', '1000 kg', '640 kg'], 0, 'Multiply.'), _q('Landsat 9 scenes per day…', ['740', '400', '100', '7400'], 0, 'NASA.'),
          _q('Trade winner…', ['B', 'A', 'tie', 'neither'], 0, '7.4 > 6.8.'), _q('Margins over time…', ['shrink', 'grow', 'vanish at start', 'are fixed'], 0, 'Maturity.')],
 'cards': [('Requirement', 'Measurable, verifiable need.'), ('Budget', 'Allocation of a resource.'), ('Margin', 'Reserve above estimate.'), ('Trade study', 'Weighted comparison.'), ('Life cycle', 'Phases from concept to disposal.'), ('Verification', 'Proof a requirement is met.')],
 'planet': {'text': ['NASA says Landsat 9’s program requirements included collecting at least 400 scenes a day and a 5-year design life; Landsat 9 collects 740 scenes a day, almost double the minimum, and carries enough fuel to operate for at least 10 years.',
                     'Exceeding requirements like these extends a land record that, NASA notes, spans more than five decades and supports deforestation alerts, water-quality monitoring and crop reports.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Solutions', 'Solutions.html')],
            'src': [_L9]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u2', 'title': 'Orbits and the Space Environment', 'weeks': 'Week 2',
 'summary': 'Choosing an orbit, period and speed, sun-synchronous and geostationary orbits, ground tracks and swaths, eclipse, vacuum, radiation and atomic oxygen.',
 'objectives': ['Compute orbital period and speed.', 'Count orbits per day.', 'Estimate eclipse duration in low orbit.', 'List environment hazards by orbit.'],
 'concepts': ['Period T = 2π√(a³/μ); circular speed v = √(μ/a).',
              'Sun-synchronous orbits are near-polar and precess once a year, so the satellite crosses the equator at the same local time each day.',
              'Low orbits pass through Earth’s shadow; the eclipse fraction for a circular orbit with the Sun in the orbit plane is about (2/2π)·asin(R_E/a).',
              'The space environment includes vacuum, extreme temperatures, radiation belts, atomic oxygen in low orbit and debris.',
              'Higher orbits see more of Earth but need bigger optics and antennas for the same resolution and data rate.'],
 'eqs': [('T=2\\pi\\sqrt{a^3/\\mu}', 'Orbital period'), ('v=\\sqrt{\\mu/a}', 'Circular speed'), ('f_e\\approx\\frac{\\sin^{-1}(R_E/a)}{\\pi}', 'Eclipse fraction (worst case)'), ('N=\\frac{86400}{T}', 'Orbits per day')],
 'worked': [
  _w('Landsat 9 flies at 705 km. Find its period.', ['a = 6378.137 + 705 = 7083.1 km.', 'T = 2π√(7083.1³/398,600.4).'], 'T = 98.9 min (NASA lists 99 min).'),
  _w('Find orbits per day and speed.', ['86,400/5932.7 s.', 'v = √(398,600.4/7083.1).'], '14.56 orbits/day; 7.50 km/s.'),
  _w('Estimate the worst-case eclipse.', ['asin(6378.1/7083.1) = 1.121 rad.', 'f = 1.121/π = 0.357.'], 'About 35.3 min per orbit.')],
 'practice': [('Why near-polar?', 'To cover the whole globe.'), ('Inclination of Landsat 9?', '98.2°.'),
              ('Main low-orbit erosion hazard?', 'Atomic oxygen.'), ('Does eclipse shrink at higher altitude?', 'Yes, the fraction drops.')],
 'misc': [('Space is cold, so spacecraft freeze.', 'Sunlit parts can overheat; balance matters.'), ('Higher is always better.', 'Resolution and links suffer.'), ('Sun-synchronous means always sunlit.', 'Only dawn–dusk versions avoid eclipse.')],
 'quiz': [_q('Landsat 9 period…', ['≈99 min', '24 h', '45 min', '12 h'], 0, 'NASA.'), _q('Orbits per day…', ['≈14.5', '1', '100', '3'], 0, '86,400/T.'),
          _q('Worst eclipse at 705 km…', ['≈35 min', '0', '60 min', '5 min'], 0, 'Computed.'), _q('Sun-synchronous gives…', ['same local time', 'no eclipse', 'GEO view', 'zero drag'], 0, 'Precession.')],
 'cards': [('Period', '2π√(a³/μ).'), ('Sun-synchronous', 'Same local crossing time.'), ('Eclipse', 'Time in Earth’s shadow.'), ('Swath', 'Ground width imaged.'), ('Atomic oxygen', 'Erodes LEO surfaces.'), ('Radiation belts', 'Trapped charged particles.')],
 'planet': {'text': ['NASA lists Landsat 9 in a near-polar, sun-synchronous orbit at 705 km with a 98.2° inclination, a 99-minute period, about 14.5 orbits a day, a 185 km swath and an equatorial crossing near 10:12 a.m. local time.',
                     'With Landsat 8, it observes the same place every 8 days. Same-time-of-day lighting is what lets scientists compare images across decades.'],
            'site': [('Orbital Mechanics', 'Orbital_Mechanics.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_L9]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_L9[0], _L9[1], 'NASA mission page.')]})
UNITS.append(
{'id': 'u3', 'title': 'Power Generation: Solar Arrays', 'weeks': 'Week 3',
 'summary': 'Solar flux and distance, cell efficiency, sun angle, beginning- and end-of-life power, array sizing and specific power.',
 'objectives': ['Compute array output per square meter.', 'Apply the cosine and inverse-square laws.', 'Size an array for a load.', 'Compare cell technologies.'],
 'concepts': ['Solar flux near Earth is about 1361 W/m² (textbook value) and falls with the inverse square of distance from the Sun.',
              'Power drops with the cosine of the angle between the array normal and the Sun.',
              'NASA’s small-spacecraft survey reports multi-junction space cells at a nominal 30% efficiency (up to 34%), versus about 20% for single-junction silicon.',
              'Degradation from radiation, contamination and aging lowers end-of-life power, so arrays are sized for EOL.',
              'Specific power (W/kg) often governs feasibility; NASA notes solar-array missions cluster around 30 W/kg.'],
 'eqs': [('P=S\\eta A\\cos\\theta', 'Array power'), ('S(r)=\\frac{1361}{r^2}', 'Inverse square (r in AU)'), ('A=\\frac{P}{S\\eta f_d}', 'Array area'), ('SP=\\frac{P}{m}', 'Specific power')],
 'worked': [
  _w('Find output per m² for 30% cells facing the Sun at 1 AU.', ['1361 × 0.30.'], '408.3 W/m².'),
  _w('Find the area for 2 kW with a 0.85 degradation-and-packing factor (sample value).', ['2000/(1361 × 0.30 × 0.85).'], '5.76 m².'),
  _w('Find solar flux at Jupiter (5.2 AU).', ['1361/5.2².'], '50.3 W/m², 27 times less.')],
 'practice': [('Output per m² tilted 30°?', '353.6 W/m².'), ('Flux at Mars (1.524 AU)?', '586 W/m².'),
              ('Output per m² for 20% silicon?', '272.2 W/m².'), ('Array mass for 2 kW at 30 W/kg?', '66.7 kg.')],
 'misc': [('Distance hardly matters.', 'Flux falls as 1/r².'), ('BOL power is enough.', 'Size for end of life.'), ('Efficiency is all that matters.', 'Mass and stowed volume matter too.')],
 'quiz': [_q('30% at 1 AU per m²…', ['408 W', '1361 W', '136 W', '30 W'], 0, 'Multiply.'), _q('Flux at Jupiter…', ['≈50 W/m²', '1361', '500', '5'], 0, '1/r².'),
          _q('Nominal multi-junction η (NASA)…', ['30%', '10%', '50%', '86%'], 0, 'SOA report.'), _q('Tilt reduces power by…', ['cos θ', 'sin θ', 'θ²', 'nothing'], 0, 'Cosine.')],
 'cards': [('Solar flux', '≈1361 W/m² at 1 AU.'), ('Multi-junction cell', 'Stacked bandgaps, ~30%.'), ('BOL/EOL', 'Beginning/end of life.'), ('Cosine loss', 'P ∝ cos θ.'), ('Inverse square', 'S ∝ 1/r².'), ('Specific power', 'W/kg.')],
 'planet': {'text': ['NASA describes Europa Clipper as a solar-powered spacecraft that, with its solar arrays deployed, spans more than 100 feet (about 30 meters); it launched Oct. 14, 2024, and will travel 1.8 billion miles to reach Jupiter in April 2030.',
                     'At Jupiter, sunlight is about 27 times weaker than at Earth, which is why Clipper’s arrays are so large: this unit’s inverse-square law, at mission scale.'],
            'site': [('Solutions', 'Solutions.html'), ('Orbital Mechanics', 'Orbital_Mechanics.html')],
            'src': [_EC, _PWR]},
 'res': [(_PWR[0], _PWR[1], 'Free NASA power chapter.'), ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc', 'Series and parallel strings.')]})
UNITS.append(
{'id': 'u4', 'title': 'Energy Storage and the Power Budget', 'weeks': 'Week 4',
 'summary': 'Load lists, sunlight and eclipse energy balance, battery sizing with depth of discharge, specific energy, power management and distribution.',
 'objectives': ['Build a load list and orbit-average power.', 'Size a battery for eclipse.', 'Compute battery mass from specific energy.', 'Explain depth-of-discharge limits.'],
 'concepts': ['The power budget sums every load by mode; the array must power loads in sunlight and recharge the battery for eclipse.',
              'Battery energy = load × eclipse time ÷ allowed depth of discharge (DoD).',
              'Shallow DoD extends cycle life; low orbits see about 15 cycles a day, so DoD is often kept low (textbook guidance).',
              'NASA’s survey reports commercial Li-ion cells at about 150–270 Wh/kg and 3.6 V average.',
              'Power management and distribution regulates bus voltage, switches loads and isolates faults.'],
 'eqs': [('E=\\frac{P_et_e}{DoD}', 'Battery energy'), ('m_b=\\frac{E}{e_{sp}}', 'Battery mass'), ('P_{avg}=\\frac{P_dt_d+P_et_e}{T}', 'Orbit-average load'), ('Ah=\\frac{Wh}{V}', 'Capacity')],
 'worked': [
  _w('A 500 W load must ride through the 35.3-minute eclipse from Unit 2. Find the energy used.', ['500 × 35.28/60.'], '294 Wh.'),
  _w('Size the battery for 30% DoD (sample value).', ['294/0.30.'], '980 Wh.'),
  _w('Find battery mass at 150 Wh/kg pack level.', ['980/150.'], '6.53 kg.')],
 'practice': [('Capacity at 28 V?', '35 Ah.'), ('Mass using 260 Wh/kg cells?', '3.77 kg (cells only).'),
              ('Cycles per day at 14.56 orbits/day?', 'About 14.6.'), ('Why not 100% DoD?', 'Cycle life collapses.')],
 'misc': [('Watts and watt-hours are the same.', 'Power vs energy.'), ('Deep discharge is fine.', 'It shortens life.'), ('Cell energy = pack energy.', 'Packs add mass for structure and management.')],
 'quiz': [_q('Eclipse energy…', ['294 Wh', '500 Wh', '35 Wh', '1000 Wh'], 0, 'P × t.'), _q('Battery at 30% DoD…', ['980 Wh', '294 Wh', '88 Wh', '3000 Wh'], 0, 'Divide.'),
          _q('Li-ion cell voltage…', ['3.6 V', '1.5 V', '12 V', '28 V'], 0, 'NASA.'), _q('Battery mass…', ['6.53 kg', '65 kg', '0.65 kg', '1 kg'], 0, '980/150.')],
 'cards': [('Load list', 'Power per subsystem and mode.'), ('DoD', 'Fraction of capacity used.'), ('Specific energy', 'Wh/kg.'), ('PMAD', 'Power management and distribution.'), ('Eclipse', 'No solar power.'), ('Orbit-average power', 'Time-weighted load.')],
 'planet': {'text': ['NASA’s small-spacecraft technology survey lists 18650 lithium-ion cells with flight heritage on NASA missions, including LG Chem INR18650-MJ1 cells at 260 Wh/kg for NASA’s PACE mission and LG Chem ICR18650 B3 cells at 191–205 Wh/kg for Europa Clipper.',
                     'PACE, launched in February 2024, measures phytoplankton, aerosols and clouds to help monitor ocean health, air quality and climate. Its batteries keep it working through every eclipse.'],
            'site': [('Oceans', 'Oceans.html'), ('Circuits', 'Circuits.html')],
            'src': [_PWR, _PACE]},
 'res': [(_PWR[0], _PWR[1], 'Free NASA power chapter.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u5', 'title': 'Thermal Control', 'weeks': 'Week 5',
 'summary': 'Radiation balance, absorptivity and emissivity, equilibrium temperature, radiator sizing, coatings, heaters and multilayer insulation.',
 'objectives': ['Compute an equilibrium temperature.', 'Size a radiator.', 'Choose coatings by α/ε.', 'Explain heaters and insulation.'],
 'concepts': ['In vacuum, heat leaves mainly by radiation: Q = εσAT⁴.',
              'Absorbed sunlight is αSA_proj; the ratio α/ε of a surface sets its equilibrium temperature.',
              'A black sphere at 1 AU with α = ε settles near (S/4σ)^¼ ≈ 278 K.',
              'Radiators reject waste heat; white paints and mirrors have low α/ε, staying cool in sunlight.',
              'Multilayer insulation blocks radiation; heaters keep batteries and propellant warm in eclipse.'],
 'eqs': [('Q=\\varepsilon\\sigma AT^4', 'Radiated heat'), ('T=\\left(\\frac{\\alpha S}{4\\varepsilon\\sigma}\\right)^{1/4}', 'Sphere equilibrium'), ('A_r=\\frac{Q}{\\varepsilon\\sigma T^4}', 'Radiator area'), ('Q_{abs}=\\alpha SA_p', 'Absorbed sunlight')],
 'worked': [
  _w('Find the equilibrium temperature of a sphere at 1 AU with α = ε.', ['T = (1361/(4 × 5.6704 × 10⁻⁸))^¼.'], 'T = 278.3 K (5 °C).'),
  _w('Size a radiator to reject 500 W at 290 K with ε = 0.85 (ignoring absorbed sunlight).', ['A = 500/(0.85 × 5.6704 × 10⁻⁸ × 290⁴).'], 'A = 1.47 m².'),
  _w('How does equilibrium temperature scale with α/ε?', ['T ∝ (α/ε)^¼.'], 'Doubling α/ε raises T by 2^¼ = 1.189.')],
 'practice': [('T for α/ε = 2?', '331 K.'), ('Radiator at 260 K for 500 W?', '2.27 m².'),
              ('What does MLI do?', 'Blocks radiative heat flow.'), ('Why heaters in eclipse?', 'To keep parts above minimum temperatures.')],
 'misc': [('Space conducts heat away.', 'Vacuum: radiation dominates.'), ('Black is always hot.', 'Depends on α/ε.'), ('Thermal is an afterthought.', 'It drives layout and power.')],
 'quiz': [_q('Sphere at 1 AU…', ['278 K', '373 K', '200 K', '0 K'], 0, 'Computed.'), _q('Q = …', ['εσAT⁴', 'hAΔT', 'kAΔT/L', 'mcΔT'], 0, 'Radiation.'),
          _q('Radiator area example…', ['1.47 m²', '14.7 m²', '0.15 m²', '5 m²'], 0, 'Computed.'), _q('Low α/ε surface…', ['stays cool', 'gets hot', 'no effect', 'glows'], 0, 'Balance.')],
 'cards': [('Absorptivity α', 'Fraction of sunlight absorbed.'), ('Emissivity ε', 'Radiating ability.'), ('MLI', 'Multilayer insulation.'), ('Radiator', 'Heat-rejecting surface.'), ('Heater', 'Keeps parts warm.'), ('σ', '5.6704 × 10⁻⁸ W/(m²·K⁴).')],
 'planet': {'text': ['NASA explains that Landsat 9’s Thermal Infrared Sensor measures land surface temperature and contains a cryocooler radiator, an Earth shield, and a blackbody plus deep-space view for calibration.',
                     'Thermal design is the instrument here: TIRS measures heat from Earth, which NASA notes helps track and manage water use, only because its own detectors are kept cold and stable.'],
            'site': [('Thermodynamics', 'Thermodynamics.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_L9]},
 'res': [(_THM[0], _THM[1], 'Free NASA thermal chapter.'), ('PhET: Blackbody Spectrum', _PH + 'blackbody-spectrum', 'Thermal radiation.')]})
UNITS.append(
{'id': 'u6', 'title': 'Structures, Mechanisms and Launch Loads', 'weeks': 'Week 6',
 'summary': 'Launch loads, quasi-static design loads, stiffness and natural frequency requirements, materials, deployables, and heritage buses.',
 'objectives': ['Compute a quasi-static launch load.', 'Compute a natural frequency.', 'Explain stiffness requirements.', 'Weigh heritage versus new design.'],
 'concepts': ['Launch subjects spacecraft to steady acceleration, vibration, acoustics and shock; design starts from quasi-static load factors (often several g, textbook values).',
              'Launch vehicles require the spacecraft’s fundamental frequency to stay above a minimum so it does not couple with the rocket.',
              'For a simple spring-mass model, f = (1/2π)√(k/m): stiffness raises frequency, mass lowers it.',
              'Aluminum honeycomb and composites give stiffness for little mass; mechanisms deploy arrays, antennas and booms.',
              'Reusing a flight-proven bus (heritage) cuts risk and schedule.'],
 'eqs': [('F=n\\,m\\,g_0', 'Quasi-static load'), ('f=\\frac{1}{2\\pi}\\sqrt{k/m}', 'Natural frequency'), ('\\sigma=F/A', 'Stress'), ('k=\\frac{EA}{L}', 'Axial stiffness')],
 'worked': [
  _w('Find the design load for a 1000 kg spacecraft at 6 g (sample values).', ['6 × 1000 × 9.80665.'], '58.8 kN.'),
  _w('A 100 kg instrument on a mount of stiffness 10⁶ N/m (sample values). Find f.', ['(1/2π)√(10⁶/100).'], 'f = 15.9 Hz.'),
  _w('How stiff must the mount be to double f?', ['f ∝ √k.'], '4 × 10⁶ N/m (31.8 Hz).')],
 'practice': [('f if mass doubles?', '11.3 Hz.'), ('Load at 4 g for 500 kg?', '19.6 kN.'),
              ('Why minimum frequency?', 'Avoid coupling with launcher dynamics.'), ('What is a heritage bus?', 'A flight-proven spacecraft platform.')],
 'misc': [('Strength is the only goal.', 'Stiffness often drives design.'), ('Heavier is safer.', 'Mass lowers frequency and costs launch.'), ('Deployables are simple.', 'They are common single points of failure.')],
 'quiz': [_q('6 g on 1000 kg…', ['58.8 kN', '6 kN', '9.8 kN', '588 kN'], 0, 'nmg.'), _q('f example…', ['15.9 Hz', '100 Hz', '1 Hz', '159 Hz'], 0, 'Formula.'),
          _q('Double f needs k ×…', ['4', '2', '√2', '8'], 0, 'f ∝ √k.'), _q('Heritage reduces…', ['risk', 'mass always', 'power', 'orbit'], 0, 'Proven.')],
 'cards': [('Quasi-static load', 'Equivalent steady g.'), ('Natural frequency', '(1/2π)√(k/m).'), ('Honeycomb', 'Light stiff panel.'), ('Deployable', 'Unfolds in orbit.'), ('Heritage', 'Flight-proven design.'), ('Bus', 'Spacecraft platform.')],
 'planet': {'text': ['NASA says Northrop Grumman designed and built the Landsat 9 spacecraft by adapting the LEOStar bus design used for Landsat 8, and integrated both instruments and ran satellite-level testing.',
                     'Reusing a proven bus is a design choice that reduces risk and helps keep the Landsat record continuous, which NASA notes is the longest continuous satellite record of Earth’s land surface.'],
            'site': [('Aerospace Structures', 'Aerospace_Structures.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_L9]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_SOA[0], _SOA[1], 'Free NASA technology survey.')]})
UNITS.append(
{'id': 'u7', 'title': 'Propulsion and the Delta-v Budget', 'weeks': 'Week 7',
 'summary': 'Δv budgets for orbit insertion, station-keeping, attitude and disposal; the rocket equation for propellant mass; gravity assists; and propulsion choices.',
 'objectives': ['Build a Δv budget.', 'Compute propellant mass from Δv.', 'Compute Δv from propellant.', 'Explain gravity assists.'],
 'concepts': ['A Δv budget lists every maneuver: insertion, orbit maintenance, attitude control, collision avoidance and disposal, plus margin.',
              'Propellant needed: m_p = m₀(1 − e^(−Δv/v_e)).',
              'Monopropellant thrusters are simple; bipropellant gives higher Isp; electric gives very high Isp at low thrust.',
              'Gravity assists borrow momentum from a planet to change speed and direction without propellant.',
              'Leftover propellant can extend a mission past its design life.'],
 'eqs': [('m_p=m_0\\left(1-e^{-\\Delta v/v_e}\\right)', 'Propellant mass'), ('\\Delta v=v_e\\ln\\frac{m_0}{m_f}', 'Rocket equation'), ('v_e=I_{sp}g_0', 'Exhaust velocity'), ('\\Delta v_{tot}=\\sum\\Delta v_i(1+M)', 'Budget with margin')],
 'worked': [
  _w('A 1000 kg spacecraft needs 100 m/s with Isp 300 s (sample values). Find propellant.', ['v_e = 2942 m/s.', 'm_p = 1000(1 − e^(−100/2942)).'], '33.4 kg.'),
  _w('What Δv does 50 kg of propellant give?', ['2942 ln(1000/950).'], '150.9 m/s.'),
  _w('Budget: 60 m/s insertion trim, 30 m/s station-keeping, 10 m/s disposal, 20% margin.', ['100 × 1.2.'], '120 m/s.')],
 'practice': [('Propellant for 120 m/s?', '39.9 kg.'), ('v_e for Isp 220 s?', '2157 m/s.'),
              ('What does a gravity assist save?', 'Propellant for the same Δv.'), ('Why budget disposal Δv?', 'To leave orbit responsibly.')],
 'misc': [('Propellant scales linearly with Δv.', 'Exponentially.'), ('Gravity assists are free energy.', 'Momentum is exchanged with the planet.'), ('Disposal is optional.', 'It protects orbits for others.')],
 'quiz': [_q('m_p for 100 m/s…', ['33.4 kg', '100 kg', '3.3 kg', '334 kg'], 0, 'Formula.'), _q('Δv from 50 kg…', ['151 m/s', '50 m/s', '500 m/s', '15 m/s'], 0, 'Rocket eq.'),
          _q('Budget with margin…', ['120 m/s', '100 m/s', '80 m/s', '200 m/s'], 0, '×1.2.'), _q('Clipper’s Dec 2026 Earth pass is a…', ['gravity assist', 'landing', 'refuel', 'launch'], 0, 'NASA.')],
 'cards': [('Δv budget', 'Sum of maneuvers.'), ('Station-keeping', 'Holding an orbit.'), ('Monopropellant', 'Single propellant, simple.'), ('Bipropellant', 'Fuel + oxidizer.'), ('Gravity assist', 'Planetary flyby boost.'), ('Disposal', 'End-of-life deorbit or graveyard.')],
 'planet': {'text': ['NASA says Europa Clipper flew past Mars in 2025 and will swing by Earth again on Dec. 3, 2026, for a gravity assist that gives it a push for the rest of its trip to Jupiter, where it will make 49 close flybys of Europa.',
                     'Gravity assists stretch a fixed propellant load, the same goal this unit’s Δv budget serves for Earth orbiters like Landsat 9, which NASA says carries fuel for at least 10 years.'],
            'site': [('Orbital Mechanics', 'Orbital_Mechanics.html'), ('Propulsion', 'Propulsion.html')],
            'src': [_EC, _L9]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_SOA[0], _SOA[1], 'Free NASA technology survey.')]})
UNITS.append(
{'id': 'u8', 'title': 'Attitude Determination and Control Subsystem', 'weeks': 'Weeks 8–9',
 'summary': 'Pointing requirements from payloads, sensors and actuators, disturbance torques, momentum budgets, and pointing error on the ground.',
 'objectives': ['Derive a pointing requirement from ground resolution.', 'Compute ground error from angle error.', 'Build a momentum budget.', 'Pick sensors and actuators.'],
 'concepts': ['Payloads set pointing: an imager’s pixel subtends an angle of (ground pixel)/(altitude).',
              'Ground error ≈ altitude × angle error (small angles).',
              'Sensors: star trackers, sun sensors, magnetometers, gyros; actuators: reaction wheels, magnetic torquers, thrusters.',
              'Disturbances (gravity gradient, drag, solar pressure, magnetic) build momentum H = τt that wheels must store.',
              'Momentum is dumped with magnetic torquers or thrusters before wheels saturate.'],
 'eqs': [('\\theta=\\frac{x}{h}', 'Pixel angle'), ('e=h\\theta', 'Ground error'), ('H=\\tau t', 'Accumulated momentum'), ('1^{\\prime\\prime}=\\frac{\\pi}{648000}\\,\\text{rad}', 'Arcsecond')],
 'worked': [
  _w('Landsat 9 has 30 m pixels from 705 km. Find the angle per pixel.', ['30/705,000 rad.'], '4.26 × 10⁻⁵ rad = 8.78 arcsec.'),
  _w('A 0.01° pointing error from 705 km shifts the image how far?', ['705,000 × 0.0001745.'], '123 m, about four pixels.'),
  _w('A 10⁻⁵ N·m disturbance acts for a quarter of a 98.9-minute orbit (sample value). Find the momentum.', ['10⁻⁵ × 1483 s.'], '0.0148 N·m·s.')],
 'practice': [('Angle for a 15 m pixel?', '4.39 arcsec.'), ('Ground error for 0.001°?', '12.3 m.'),
              ('Which sensor gives absolute attitude?', 'A star tracker.'), ('How are wheels unloaded in LEO?', 'Magnetic torquers or thrusters.')],
 'misc': [('Pointing knowledge equals control.', 'They are separate budgets.'), ('Wheels can absorb momentum forever.', 'They saturate.'), ('Small angles do not matter.', 'Altitude multiplies them.')],
 'quiz': [_q('Landsat pixel angle…', ['8.78″', '1°', '0.1″', '60″'], 0, '30/705 km.'), _q('0.01° at 705 km…', ['123 m', '12 m', '1.2 km', '1 m'], 0, 'hθ.'),
          _q('H = …', ['τt', 'Iα', 'τ/t', 'mv'], 0, 'Momentum.'), _q('Absolute attitude sensor…', ['star tracker', 'gyro', 'wheel', 'heater'], 0, 'Stars.')],
 'cards': [('Pointing accuracy', 'Control error.'), ('Pointing knowledge', 'Measurement error.'), ('Star tracker', 'Attitude from stars.'), ('Magnetic torquer', 'Coil reacting with Earth’s field.'), ('Gravity gradient', 'Tidal torque.'), ('Momentum dumping', 'Unloading wheels.')],
 'planet': {'text': ['NASA lists Landsat 9’s spatial resolution as 30 m for visible and shortwave infrared bands, 15 m panchromatic and 100 m thermal, from 705 km.',
                     'Holding a 30 m pixel steady from that height takes arcsecond-level control, the reason Landsat images line up across years for change detection.'],
            'site': [('Flight Dynamics & Controls', 'Flight_Dynamics_Controls.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_L9]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_SOA[0], _SOA[1], 'Free NASA technology survey.')]})
UNITS.append(
{'id': 'u9', 'title': 'Communications and Data Handling', 'weeks': 'Weeks 10–11',
 'summary': 'Data volume, downlink rates, the link budget in decibels, free-space path loss, antenna gain, and onboard computing and storage.',
 'objectives': ['Compute free-space path loss.', 'Compute dish antenna gain.', 'Build a simple link budget.', 'Estimate daily data volume.'],
 'concepts': ['Free-space path loss L = 20 log₁₀(4πd/λ) dB grows with distance and frequency.',
              'Dish gain G = η(πD/λ)²; bigger dishes and higher frequencies give narrower, stronger beams.',
              'Link budget: received power = transmit power + gains − losses (all in dB); the margin over what the receiver needs must be positive.',
              'Data volume = images × bits per image; rate × contact time must exceed it.',
              'Command and data handling computers store data, run software and manage faults.'],
 'eqs': [('L=20\\log_{10}\\frac{4\\pi d}{\\lambda}', 'Free-space path loss'), ('G=\\eta\\left(\\frac{\\pi D}{\\lambda}\\right)^2', 'Dish gain'), ('P_r=P_t+G_t+G_r-L', 'Link budget (dB)'), ('\\lambda=c/f', 'Wavelength')],
 'worked': [
  _w('Find the X-band (8.2 GHz) path loss at 2000 km (c = 3 × 10⁸ m/s).', ['λ = 0.03659 m.', '20 log₁₀(4π × 2 × 10⁶/0.03659).'], 'L = 176.7 dB.'),
  _w('Find the gain of a 3 m dish at 8.2 GHz with η = 0.55 (sample value).', ['0.55 × (π × 3/0.03659)².'], 'G = 45.6 dBi.'),
  _w('What happens to path loss if distance doubles?', ['+20 log₁₀ 2.'], '+6.0 dB (182.8 dB at 4000 km).')],
 'practice': [('Wavelength at 8.2 GHz?', '3.66 cm.'), ('Gain change for a 6 m dish?', '+6.0 dB.'),
              ('Landsat 9 scenes per day?', 'About 740.'), ('Bits per pixel for Landsat 9 OLI?', '14.')],
 'misc': [('Decibels add like watts.', 'dB add for products.'), ('Higher frequency is always worse.', 'Loss rises but dish gain rises too.'), ('Data volume is small.', 'It often drives ground-station design.')],
 'quiz': [_q('Path loss 2000 km X-band…', ['176.7 dB', '100 dB', '50 dB', '250 dB'], 0, 'Formula.'), _q('3 m dish gain…', ['45.6 dBi', '10 dBi', '90 dBi', '3 dBi'], 0, 'Formula.'),
          _q('Double distance…', ['+6 dB loss', '+3 dB', '×2 dB', 'none'], 0, '20 log 2.'), _q('Link budget uses…', ['dB sums', 'products of watts only', 'volts', 'joules'], 0, 'Log units.')],
 'cards': [('Path loss', 'Spreading loss in dB.'), ('Antenna gain', 'Beam concentration.'), ('Link margin', 'Received minus required.'), ('X-band', '≈8 GHz.'), ('C&DH', 'Command and data handling.'), ('Data volume', 'Bits per day.')],
 'planet': {'text': ['NASA says Europa Clipper carries nine science instruments plus a gravity experiment that uses its telecommunications system, and shows its 10-foot (3-meter) high-gain antenna installed in August 2023.',
                     'Closer to home, NASA reports Landsat 9 records 14-bit data and collects more than 700 scenes a day. Moving that much data to the ground every day is a communications design problem first.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Circuits', 'Circuits.html')],
            'src': [_EC, _L9]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_SOA[0], _SOA[1], 'Free NASA technology survey.')]})
UNITS.append(
{'id': 'u10', 'title': 'Reliability, Testing and End of Life', 'weeks': 'Weeks 12–13',
 'summary': 'Failure rates and reliability, redundancy, environmental testing, calibration and verification, operations and responsible disposal.',
 'objectives': ['Compute reliability from a failure rate.', 'Compute the benefit of redundancy.', 'Describe environmental tests.', 'Plan end-of-life disposal.'],
 'concepts': ['With a constant failure rate λ, reliability R(t) = e^(−λt) and mean time between failures is 1/λ.',
              'Two units in parallel: R = 1 − (1 − R₁)²; redundancy trades mass and cost for reliability.',
              '“Test like you fly”: vibration, acoustic, shock, thermal-vacuum and electromagnetic tests before launch.',
              'Calibration keeps science data accurate over time; cross-calibration with other satellites ties records together.',
              'At end of life, spacecraft should be deorbited or moved to a disposal orbit to limit debris.'],
 'eqs': [('R(t)=e^{-\\lambda t}', 'Reliability'), ('R_p=1-(1-R)^2', 'Two in parallel'), ('MTBF=1/\\lambda', 'Mean time between failures'), ('R_s=\\prod R_i', 'Series system')],
 'worked': [
  _w('A unit has λ = 10⁻⁵ per hour (sample value). Find its 5-year reliability.', ['t = 43,800 h.', 'e^(−0.438).'], 'R = 0.645.'),
  _w('Add a redundant unit in parallel.', ['1 − 0.355².'], 'R = 0.874.'),
  _w('Find the MTBF.', ['1/10⁻⁵ h.'], '100,000 h = 11.4 years.')],
 'practice': [('10-year reliability of one unit?', '0.416.'), ('Series system of 0.95 and 0.90?', '0.855.'),
              ('Name a pre-launch environmental test.', 'Thermal vacuum or vibration.'), ('Why cross-calibrate?', 'To keep records consistent across satellites.')],
 'misc': [('Redundancy is free.', 'It costs mass, power and money.'), ('Testing proves zero risk.', 'It reduces risk.'), ('Disposal is someone else’s job.', 'It is designed in from the start.')],
 'quiz': [_q('5-year R…', ['0.645', '0.95', '0.5', '0.1'], 0, 'e^(−0.438).'), _q('Parallel pair…', ['0.874', '0.645', '0.416', '1'], 0, '1 − 0.355².'),
          _q('MTBF…', ['100,000 h', '10⁻⁵ h', '1000 h', '1 h'], 0, '1/λ.'), _q('Landsat underfly purpose…', ['cross-calibration', 'refuel', 'docking', 'disposal'], 0, 'NASA.')],
 'cards': [('Reliability', 'Probability of working.'), ('Failure rate λ', 'Failures per hour.'), ('Redundancy', 'Backup units.'), ('Thermal vacuum test', 'Space conditions on the ground.'), ('Calibration', 'Keeping measurements accurate.'), ('Disposal', 'End-of-life deorbit.')],
 'planet': {'text': ['NASA reports that just after launch, Landsat 9 flew directly below Landsat 8 in a once-in-a-mission “underfly,” collecting 2,396 images from November 12–16, 2021, so calibration experts could compare both satellites’ measurements and ensure data continuity.',
                     'NASA notes that onboard calibration and redundancy help Landsat 9 collect accurate, reliable data for its mission life: reliability engineering in service of a planetary record.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Solutions', 'Solutions.html')],
            'src': [_L9]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Mass and power budgets with margin', 'week': 'Week 1',
 'goal': 'Build a spreadsheet mass and power budget for a small Earth-observing satellite and apply margins.',
 'eq': ('m_{alloc}=m_{est}(1+M)', 'Allocation with margin'),
 'steps': ['List subsystems: payload, structure, power, thermal, ADCS, propulsion, comms, C&DH.', 'Enter sample mass estimates totaling 800 kg and power estimates totaling 500 W.', 'Apply 20% margin to each total.', 'Run the two-option weighted trade from Unit 1 and change the weights.'],
 'table': (['Budget', 'Estimate', 'With 20% margin'], [['Dry mass', '800 kg', '960 kg'], ['Power', '500 W', '600 W']]),
 'note': 'Sample values.',
 'calc': ['800 × 1.2 = 960 kg.', '500 × 1.2 = 600 W.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_SEH[0], _SEH[1])],
 'planet': 'NASA: Landsat 9 collects 740 scenes a day against a 400-scene requirement.', 'planet_src': [_L9]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Orbit period and eclipse calculator', 'week': 'Week 2',
 'goal': 'Compute period and worst-case eclipse for several low-orbit altitudes.',
 'eq': ('T=2\\pi\\sqrt{a^3/\\mu}', 'Orbital period'),
 'steps': ['Enter altitudes of 400, 705 and 1000 km.', 'Compute a, T and orbits per day.', 'Compute the eclipse fraction and minutes.', 'Compare 705 km with NASA’s Landsat 9 values.'],
 'table': (['Altitude (km)', 'T (min)', 'Eclipse (min)'], [['400', '92.6', '36.1'], ['705', '98.9', '35.3'], ['1000', '105.1', '34.9']]),
 'note': 'Computed worst-case values (Sun in the orbit plane).',
 'calc': ['T(400) = 2π√(6778.1³/398,600.4) = 92.6 min.', 'Eclipse(705) = 0.357 × 98.9 = 35.3 min.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_L9[0], _L9[1])],
 'planet': 'NASA lists Landsat 9 at 705 km with a 99-minute period.', 'planet_src': [_L9]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Solar cells in series and parallel', 'week': 'Week 3',
 'goal': 'Wire cells as batteries in PhET Circuit Construction Kit to see series and parallel strings, then size arrays across the solar system.',
 'eq': ('A=\\frac{P}{S\\eta f_d}', 'Array area'),
 'steps': ['In PhET Circuit Construction Kit, connect sources in series and in parallel and note voltage and current.', 'In a spreadsheet, compute array area for 500 W with η = 0.30 and f_d = 0.85.', 'Repeat at 1, 1.524 and 5.2 AU.', 'Explain why outer-planet missions need huge arrays.'],
 'table': (['Distance (AU)', 'Area for 500 W (m²)'], [['1', '1.44'], ['1.524', '3.35'], ['5.2', '39.0']]),
 'note': 'Computed sample values.',
 'calc': ['500/(1361 × 0.3 × 0.85) = 1.44 m².', '1.44 × 5.2² = 39.0 m².'],
 'safety': ['Computer only.'], 'home': ['Any browser and spreadsheet work.'],
 'sims': [('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc'), (_PWR[0], _PWR[1])],
 'planet': 'NASA: Europa Clipper’s deployed arrays span more than 30 meters.', 'planet_src': [_EC]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Eclipse battery sizing', 'week': 'Week 4',
 'goal': 'Size batteries for different loads through a 35.3-minute eclipse.',
 'eq': ('E=\\frac{P_et_e}{DoD}', 'Battery energy'),
 'steps': ['Use the 705 km eclipse from Lab B.', 'Enter loads of 300, 500 and 800 W.', 'Compute battery energy at 30% DoD and mass at 150 Wh/kg.', 'Repeat with 20% DoD and discuss cycle life.'],
 'table': (['Load (W)', 'Battery (Wh)', 'Mass (kg)'], [['300', '588', '3.92'], ['500', '980', '6.53'], ['800', '1568', '10.45']]),
 'note': 'Computed sample values.',
 'calc': ['300 × 0.588 h/0.3 = 588 Wh.', '1568/150 = 10.45 kg.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_PWR[0], _PWR[1])],
 'planet': 'NASA lists 260 Wh/kg 18650 cells with heritage on its PACE mission.', 'planet_src': [_PWR]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Radiation balance and radiator sizing', 'week': 'Week 5',
 'goal': 'Explore thermal radiation in PhET Blackbody Spectrum, then compute equilibrium temperatures and radiator areas.',
 'eq': ('T=\\left(\\frac{\\alpha S}{4\\varepsilon\\sigma}\\right)^{1/4}', 'Sphere equilibrium'),
 'steps': ['In PhET Blackbody Spectrum, compare spectra at 250, 290 and 6000 K.', 'Compute sphere temperatures for α/ε = 0.5, 1 and 2.', 'Compute radiator area for 500 W at 250, 290 and 320 K with ε = 0.85.', 'Pick a radiator temperature and explain the trade.'],
 'table': (['Case', 'Result'], [['α/ε = 0.5', '234.0 K'], ['α/ε = 1', '278.3 K'], ['α/ε = 2', '331.0 K'], ['Radiator at 250 K', '2.66 m²'], ['Radiator at 320 K', '0.99 m²']]),
 'note': 'Computed values.',
 'calc': ['T = 278.3 × 0.5^¼ = 234.0 K.', 'A = 500/(0.85σ × 320⁴) = 0.99 m².'],
 'safety': ['Computer only.'], 'home': ['Any browser and spreadsheet work.'],
 'sims': [('PhET: Blackbody Spectrum', _PH + 'blackbody-spectrum'), (_THM[0], _THM[1])],
 'planet': 'NASA: Landsat 9’s TIRS uses a cryocooler radiator and onboard blackbody.', 'planet_src': [_L9]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Downlink link budget', 'week': 'Week 11',
 'goal': 'Build a decibel link budget and see how distance and antenna size change the margin.',
 'eq': ('L=20\\log_{10}\\frac{4\\pi d}{\\lambda}', 'Free-space path loss'),
 'steps': ['Use f = 8.2 GHz and c = 3 × 10⁸ m/s.', 'Compute path loss at 1000, 2000 and 4000 km.', 'Add transmit power, both antenna gains and other losses.', 'Find the dish size that restores margin at 4000 km.'],
 'table': (['Distance (km)', 'Path loss (dB)'], [['1000', '170.7'], ['2000', '176.7'], ['4000', '182.8']]),
 'note': 'Computed values.',
 'calc': ['λ = 0.03659 m.', '20 log₁₀(4π × 10⁶/0.03659) = 170.7 dB.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MIT[0], _MIT[1])],
 'planet': 'NASA: Europa Clipper carries a 3-meter high-gain antenna.', 'planet_src': [_EC]})
SCHEDULE = [(1, 'u1', 'Requirements and budgets; Lab A', 'NASA SE Handbook'), (2, 'u2', 'Orbits and environment; Lab B', 'MIT 16.851'),
            (3, 'u3', 'Solar arrays; Lab C', 'NASA SST SOA'), (4, 'u4', 'Batteries and power budget; Lab D', 'NASA SST SOA'),
            (5, 'u5', 'Thermal control; Lab E', 'MIT 16.851'), (6, 'u6', 'Structures and launch loads', 'MIT 16.851'),
            (7, 'u7', 'Δv budgets; midterm practice', 'MIT 16.851'), (8, 'u8', 'ADCS requirements', 'MIT 16.851'),
            (9, 'u8', 'Sensors, actuators and momentum', 'NASA SST SOA'), (10, 'u9', 'Link budgets', 'MIT 16.851'),
            (11, 'u9', 'Data handling; Lab F', 'NASA Landsat 9'), (12, 'u10', 'Reliability and redundancy', 'NASA SE Handbook'),
            (13, 'u10', 'Testing and calibration', 'NASA Landsat 9'), (14, 'u10', 'Operations and disposal', 'NASA SE Handbook'), (15, 'u10', 'Review; final practice', 'MIT 16.851')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Allocate a 500 kg estimate with 30% margin.', ['500 × 1.3.'], '650 kg.'),
  ('Find the period of a 550 km circular orbit.', ['a = 6928.1 km.', 'T = 2π√(a³/μ).'], '95.6 min.'),
  ('Array area for 1 kW at 1 AU, η = 0.30, f_d = 0.85?', ['1000/(1361 × 0.3 × 0.85).'], '2.88 m².'),
  ('Battery for 400 W over 35 min at 25% DoD?', ['400 × 35/60/0.25.'], '933 Wh.'),
  ('Radiator for 300 W at 300 K, ε = 0.9?', ['300/(0.9σ × 300⁴).'], '0.73 m².')]),
 ('Final practice set (Units 1–10)', [
  ('Natural frequency for k = 4 × 10⁵ N/m, m = 40 kg?', ['(1/2π)√(10⁴).'], '15.9 Hz.'),
  ('Propellant for 200 m/s on 800 kg at Isp 230 s?', ['800(1 − e^(−200/2255.5)).'], '67.9 kg.'),
  ('Ground error for 0.005° from 600 km?', ['600,000 × 8.727 × 10⁻⁵.'], '52.4 m.'),
  ('Path loss at 1500 km, 8.2 GHz?', ['20 log₁₀(4π × 1.5 × 10⁶/0.03659).'], '174.2 dB.'),
  ('Reliability for λ = 2 × 10⁻⁶ /h over 7 years?', ['e^(−0.1226).'], '0.885.'),
  ('Parallel pair of 0.885 units?', ['1 − 0.115².'], '0.987.')])]
FORMULAS = ['m_{alloc}=m_{est}(1+M),\\ S=\\sum w_is_i', 'T=2\\pi\\sqrt{a^3/\\mu},\\ v=\\sqrt{\\mu/a},\\ f_e\\approx\\sin^{-1}(R_E/a)/\\pi', 'P=S\\eta A\\cos\\theta,\\ S=1361/r^2',
            'E=P_et_e/DoD,\\ m_b=E/e_{sp}', 'Q=\\varepsilon\\sigma AT^4,\\ T=(\\alpha S/4\\varepsilon\\sigma)^{1/4}', 'F=nmg_0,\\ f=\\frac{1}{2\\pi}\\sqrt{k/m}',
            'm_p=m_0(1-e^{-\\Delta v/v_e})', '\\theta=x/h,\\ e=h\\theta,\\ H=\\tau t', 'L=20\\log_{10}(4\\pi d/\\lambda),\\ G=\\eta(\\pi D/\\lambda)^2', 'R=e^{-\\lambda t},\\ R_p=1-(1-R)^2']
GLOSSARY = sorted([('ADCS', 'Attitude determination and control subsystem.'), ('Antenna gain', 'Beam concentration relative to isotropic.'), ('Bus', 'Spacecraft platform carrying the payload.'), ('C&DH', 'Command and data handling.'),
    ('Depth of discharge', 'Fraction of battery capacity used.'), ('Eclipse', 'Time in a planet’s shadow.'), ('Emissivity', 'Ability to radiate heat.'), ('End of life', 'Performance after degradation.'),
    ('Gravity assist', 'Planetary flyby that changes velocity.'), ('Heritage', 'Flight-proven design.'), ('Link budget', 'Sum of gains and losses in a radio link.'), ('Margin', 'Reserve above need.'),
    ('Multilayer insulation', 'Thermal blanket that blocks radiation.'), ('Path loss', 'Signal spreading loss.'), ('Payload', 'Instruments the mission exists for.'), ('Redundancy', 'Backup hardware.'),
    ('Requirement', 'Measurable, verifiable need.'), ('Solar flux', 'Sunlight power per area.'), ('Specific power', 'Power per mass.'), ('Sun-synchronous orbit', 'Orbit crossing at the same local time daily.')])
RUBRIC = [('4 · Mastery', 'Starts from requirements, keeps consistent budgets with margins, checks units and orders of magnitude, and explains subsystem trades in plain words.'), ('3 · Proficient', 'Solves the practice problems with occasional slips in units or margins.'),
          ('2 · Developing', 'Follows worked examples but confuses power and energy or dB and linear values.'), ('1 · Beginning', 'Plugs numbers into formulas without a requirement or budget; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    mu = 398600.4418; Re = 6378.137; g0 = 9.80665; sig = 5.670374419e-8; S = 1361
    per = lambda h: 2 * pi * sqrt((Re + h) ** 3 / mu) / 60
    ecl = lambda h: asin(Re / (Re + h)) / pi * per(h)
    area = lambda P, r: P / (S / r ** 2 * .3 * .85)
    teq = lambda k: (k * S / (4 * sig)) ** .25
    rad = lambda Q, T, e=.85: Q / (e * sig * T ** 4)
    lam = 3e8 / 8.2e9
    fspl = lambda d: 20 * log10(4 * pi * d / lam)
    mp = lambda m0, dv, isp: m0 * (1 - exp(-dv / (isp * g0)))
    R5 = exp(-1e-5 * 8760 * 5)
    r = [
     ('u1 m', 800 * 1.2, 960), ('u1 L9', 740 / 400, 1.85), ('u1 L9m', (740 - 400) / 400, .85), ('u1 A', .4 * 8 + .6 * 6, 6.8), ('u1 B', .4 * 5 + .6 * 9, 7.4), ('u1 p1', 1200 * 1.25, 1500),
     ('u1 A2', .6 * 8 + .4 * 6, 7.2), ('u1 B2', .6 * 5 + .4 * 9, 6.6),
     ('u2 a', Re + 705, 7083.1), ('u2 T', per(705), 98.9), ('u2 n', 1440 / per(705), 14.56), ('u2 v', sqrt(mu / (Re + 705)), 7.50), ('u2 rho', asin(Re / (Re + 705)), 1.121), ('u2 f', asin(Re / (Re + 705)) / pi, .357),
     ('u2 ecl', ecl(705), 35.3), ('u2 Ts', per(705) * 60, 5932.7),
     ('u3 Pm', S * .3, 408.3), ('u3 A', area(2000, 1), 5.76), ('u3 J', S / 5.2 ** 2, 50.3), ('u3 Jr', 5.2 ** 2, 27.04), ('u3 tilt', S * .3 * cos(radians(30)), 353.6), ('u3 M', S / 1.524 ** 2, 586),
     ('u3 Si', S * .2, 272.2), ('u3 mass', 2000 / 30, 66.7),
     ('u4 E', 500 * ecl(705) / 60, 294), ('u4 B', 500 * ecl(705) / 60 / .3, 980), ('u4 m', 500 * ecl(705) / 60 / .3 / 150, 6.53), ('u4 Ah', 980 / 28, 35), ('u4 m260', 980 / 260, 3.77), ('u4 cyc', 1440 / per(705), 14.6),
     ('u5 T', teq(1), 278.3), ('u5 A', rad(500, 290), 1.47), ('u5 r', 2 ** .25, 1.189), ('u5 T2', teq(2), 331), ('u5 A260', rad(500, 260), 2.27), ('u5 C', teq(1) - 273.15, 5.2),
     ('u6 F', 6 * 1000 * g0, 58840), ('u6 f', sqrt(1e6 / 100) / (2 * pi), 15.9), ('u6 f2', sqrt(4e6 / 100) / (2 * pi), 31.8), ('u6 fm', sqrt(1e6 / 200) / (2 * pi), 11.3), ('u6 F4', 4 * 500 * g0, 19613),
     ('u7 ve', 300 * g0, 2942), ('u7 mp', mp(1000, 100, 300), 33.4), ('u7 dv', 300 * g0 * log(1000 / 950), 150.9), ('u7 bud', 100 * 1.2, 120), ('u7 mp120', mp(1000, 120, 300), 39.9), ('u7 ve220', 220 * g0, 2157),
     ('u8 th', 30 / 705e3, 4.26e-5), ('u8 as', 30 / 705e3 * 206264.8, 8.78), ('u8 e', 705e3 * radians(.01), 123), ('u8 rad', radians(.01), 1.745e-4), ('u8 qt', per(705) * 60 / 4, 1483), ('u8 H', 1e-5 * per(705) * 60 / 4, .0148),
     ('u8 15', 15 / 705e3 * 206264.8, 4.39), ('u8 e2', 705e3 * radians(.001), 12.3), ('u8 px', 123 / 30, 4.1),
     ('u9 lam', lam, .03659), ('u9 L', fspl(2e6), 176.7), ('u9 G', 10 * log10(.55 * (pi * 3 / lam) ** 2), 45.6), ('u9 d2', 20 * log10(2), 6.02), ('u9 L4', fspl(4e6), 182.8), ('u9 cm', lam * 100, 3.66),
     ('u10 t', 8760 * 5, 43800), ('u10 R', R5, .645), ('u10 Rp', 1 - (1 - R5) ** 2, .874), ('u10 mtbf', 1 / 1e-5, 1e5), ('u10 yr', 1e5 / 8760, 11.4), ('u10 R10', exp(-1e-5 * 87600), .416), ('u10 ser', .95 * .9, .855),
     ('u10 x', 1e-5 * 43800, .438), ('u10 q', 1 - R5, .355),
     ('labA m', 800 * 1.2, 960), ('labA p', 500 * 1.2, 600),
     ('labB 400', per(400), 92.6), ('labB 705', per(705), 98.9), ('labB 1000', per(1000), 105.1), ('labB e400', ecl(400), 36.1), ('labB e705', ecl(705), 35.3), ('labB e1000', ecl(1000), 34.9),
     ('labB a', Re + 400, 6778.1),
     ('labC 1', area(500, 1), 1.44), ('labC M', area(500, 1.524), 3.35), ('labC J', area(500, 5.2), 39.0),
     ('labD 300', 300 * ecl(705) / 60 / .3, 588), ('labD 500', 500 * ecl(705) / 60 / .3, 980), ('labD 800', 800 * ecl(705) / 60 / .3, 1568), ('labD m300', 300 * ecl(705) / 60 / .3 / 150, 3.92),
     ('labD m500', 500 * ecl(705) / 60 / .3 / 150, 6.53), ('labD m800', 800 * ecl(705) / 60 / .3 / 150, 10.45), ('labD h', ecl(705) / 60, .588),
     ('labE .5', teq(.5), 234.0), ('labE 1', teq(1), 278.3), ('labE 2', teq(2), 331.0), ('labE 250', rad(500, 250), 2.66), ('labE 320', rad(500, 320), .99), ('labE r', teq(1) * .5 ** .25, 234.0),
     ('labF 1', fspl(1e6), 170.7), ('labF 2', fspl(2e6), 176.7), ('labF 4', fspl(4e6), 182.8),
     ('mid m', 500 * 1.3, 650), ('mid T', per(550), 95.6), ('mid a', Re + 550, 6928.1), ('mid A', area(1000, 1), 2.88), ('mid B', 400 * 35 / 60 / .25, 933), ('mid R', rad(300, 300, .9), .73),
     ('fin f', sqrt(4e5 / 40) / (2 * pi), 15.9), ('fin mp', mp(800, 200, 230), 67.9), ('fin ve', 230 * g0, 2255.5), ('fin e', 600e3 * radians(.005), 52.4), ('fin r', radians(.005), 8.727e-5), ('fin L', fspl(1.5e6), 174.2),
     ('fin R', exp(-2e-6 * 8760 * 7), .885), ('fin Rp', 1 - (1 - .885) ** 2, .987), ('fin x', 2e-6 * 8760 * 7, .1226),
     ('c mu', mu, 398600.4418), ('c Re', Re, 6378.137), ('c S', S, 1361), ('c sig', sig, 5.670374419e-8), ('c g', g0, 9.80665), ('c c', 3e8, 299792458),
     ('x L9 orb', 1440 / 99, 14.5), ('x L9 i', 98.2, 98.2), ('x L9 sw', 185, 185), ('x L9 ul', 2396 / 5, 479.2), ('x L9 life', 10 / 5, 2), ('x L9 pix', 100 / 30, 3.33), ('x EC span', 100 * .3048, 30.5),
     ('x EC hga', 10 * .3048, 3.05), ('x EC d', 1.8e9 * 1.609344, 2.9e9), ('x EC fb', 49, 49), ('x soa', 34 / 20, 1.7), ('x mj', 30 / 20, 1.5), ('x li', 270 / 150, 1.8), ('x pace', 260 / 150, 1.733),
     ('x u3 r', 2000 / 408.3, 4.9), ('x u4 r', 980 / 294, 3.33), ('x u5 4', 278.3 * 2 ** .25, 331), ('x u6 r', 31.8 / 15.9, 2), ('x u7 r', 150.9 / 50, 3.02), ('x u8 r', 123 / 12.3, 10), ('x u9 r', 182.8 - 176.7, 6.1),
     ('x u10 r', .874 / .645, 1.355), ('x labC r', 39.0 / 1.44, 27.1), ('x labD r', 1568 / 588, 2.667), ('x labE r', 2.66 / .99, 2.69), ('x labF r', 176.7 - 170.7, 6.0), ('x mid r', 2.88 / 1.44, 2),
     ('x u2 deg', 1.121 * 180 / pi, 64.2), ('x u2 h', 705 * .6214, 438), ('x u8 as', 206264.8 / 3600, 57.3), ('x u9 g6', 10 * log10(.55 * (pi * 6 / lam) ** 2), 51.6), ('x u4 v', 980 / 3.6, 272), ('x u1 s', 740 - 400, 340),
     ('y u2 v4', sqrt(mu / (Re + 400)), 7.67), ('y u2 n4', 1440 / per(400), 15.56), ('y u3 Pt', 408.3 * 5.76 * .85, 2000), ('y u3 m', S / 1.524 ** 2 * .3, 175.8), ('y u4 h', 35.28 / 60, .588), ('y u5 Q', .85 * sig * 1.47 * 290 ** 4, 500),
     ('y u6 g', 58840 / 1000, 58.84), ('y u7 m', 1000 - 33.4, 966.6), ('y u7 e', exp(-100 / 2942), .9666), ('y u8 H2', 2 * .0148, .0296), ('y u9 G2', 10 * log10(.55 * (pi * 3 / lam) ** 2) + 6.02, 51.6), ('y u10 s3', .95 * .9 * .9, .7695),
     ('y labB n', 1440 / per(1000), 13.7), ('y labD m2', 500 * ecl(705) / 60 / .2 / 150, 9.8), ('y labE C', 331.0 - 273.15, 57.85), ('y mid v', sqrt(mu / 6928.137), 7.585), ('y fin m', 800 - 67.9, 732.1), ('y fin d', 174.2 - 170.7, 3.5)]
    return r
