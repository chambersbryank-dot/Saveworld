"""Capstone Design (AERO 490): a full aircraft or CubeSat design project from requirements to review: mission and requirements, concept selection, aircraft weight sizing and range, aircraft constraint sizing, CubeSat sizing and orbit, CubeSat power and link budgets, structural and thermal checks, cost, schedule and risk, prototyping and test, and design reviews.
Oct 25 2026, founder-approved four-year track, senior course 6. Same module fields as avionics.py / heat.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, log, log10, pi, asin
ID = 'capstone'
STATUS = 'live'
YEAR = 4
PAGE = 'Capstone_Design.html'
CODE = 'AERO 490'
TITLE = 'Capstone Design (Aircraft or CubeSat)'
LAB_NAME = 'Design studio'
TAGLINE = 'A full design project from requirements to review: pick an electric drone or a 3U CubeSat track, write requirements, select a concept, size it, close power, link, structural and thermal budgets, plan cost, schedule and risk, test, and present at a design review, with six spreadsheet labs. Free, self-paced, and tied to NASA’s CubeSat Launch Initiative, the PREFIRE CubeSats and NASA’s Sustainable Flight National Partnership.'
DESC = 'Free self-study Capstone Design: 10 units, worked examples, solved practice, quizzes, flashcards, 6 spreadsheet design labs, practice exams, tied to NASA CubeSats, PREFIRE and sustainable flight.'
ALT = 'The International Space Station seen from a departing spacecraft during a 2021 flyaround'
_SEH = ('NASA Systems Engineering Handbook', 'https://www.nasa.gov/reference/systems-engineering-handbook/')
_MIT = ('MIT OpenCourseWare 16.83X Space Systems Engineering (Spring 2002 – Spring 2003)', 'https://ocw.mit.edu/courses/16-83x-space-systems-engineering-spring-2002-spring-2003/')
_CSLI = ('NASA: CubeSat Launch Initiative', 'https://www.nasa.gov/kennedy/launch-services-program/cubesat-launch-initiative/')
_PRE = ('NASA Science: PREFIRE (Polar Radiant Energy in the Far-InfraRed Experiment)', 'https://science.nasa.gov/mission/prefire/')
_SOA = ('NASA Small Spacecraft Technology State of the Art', 'https://www.nasa.gov/smallsat-institute/sst-soa/')
_SFNP = ('NASA Aeronautics: Sustainable Flight National Partnership', 'https://www.nasa.gov/aeronautics/sustainable-flight-national-partnership/')
BANNER = ['images/ISS_Flyaround_2021.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg', 'images/JPSS2_Atlas_V_Launch_Pad.jpg', 'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg']
CREDITS = {'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)', 'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)',
           'images/JPSS2_Atlas_V_Launch_Pad.jpg': 'NASA/Liz Wilk (KSC-20221109-PH-LNW01_0001)', 'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg': 'NASA/Michael DeMocker (MAF20210116_GR0006)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester senior aerospace capstone. It is modeled on the conceive-design-implement-operate approach of MIT 16.83X Space Systems Engineering (free on MIT OpenCourseWare) and on the NASA Systems Engineering Handbook, which we link where they help. Neither MIT nor NASA endorses this page.',
         'What we add: two parallel tracks (a small electric drone or a 3U CubeSat), every unit tied to real work with a cited public source, every number on the page re-computed by a checking script before it goes live, and every lab in a free spreadsheet.',
         'Work through it in order, alone or with a team. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Capstone teams build the satellites and aircraft that measure and protect the planet: student CubeSats fly through NASA’s CubeSat Launch Initiative, and small satellites like PREFIRE study how the Arctic sheds heat.',
                 'On the aircraft side, NASA’s Sustainable Flight National Partnership aims for 25–30% energy-efficiency gains. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Avionics & Systems Engineering: requirements, reliability and verification.', 'Spacecraft Design: power, thermal and link budgets.',
           'Aircraft Performance: lift, drag, range and climb.', 'Aerospace Structures: stress, safety factors and margins.']
STUDY = ['Keep one design notebook or spreadsheet that every number flows from.', 'Trace every design choice to a requirement.',
         'Close budgets with margin before adding detail.', 'Hold short weekly reviews, even when working alone.',
         'Write as you go: every unit adds a section to your final report.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['Spreadsheet software (any free one works), or Python.', 'The free NASA Systems Engineering Handbook in a web browser.',
            'Free slide software for your design reviews.', 'A calculator.']
LAB_INTRO = ['The design studio is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab is a spreadsheet design tool, so there are no hazards. Do not build or fly a real drone, charge lithium batteries or handle launch hardware for this course without qualified supervision and local rules. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST: CODATA value, speed of light in vacuum', 'https://physics.nist.gov/cgi-bin/cuu/Value?c')
CONSTANTS = [('Earth’s gravitational parameter (textbook value)', 'μ = 398,600.4418 km³/s²'), ('Earth’s equatorial radius (textbook value)', '6378.137 km'), ('Standard gravity', 'g = 9.80665 m/s²'),
             ('Solar constant (textbook value)', '1361 W/m²'), ('Sea-level air density (textbook value)', '1.225 kg/m³'), ('Speed of light', 'c = 299,792,458 m/s (exact)')]
REF_TITLE = 'Free texts and resources'
REF_INTRO = 'Use these free handbooks, lectures and mission pages alongside the course.'
PTABLE = [(_SEH[0], _SEH[1], 'Free NASA handbook.'), (_MIT[0], _MIT[1], 'Free MIT capstone materials.'), (_SOA[0], _SOA[1], 'Free NASA small-spacecraft report.'),
          (_CSLI[0], _CSLI[1], 'NASA launch opportunities.'), (_PRE[0], _PRE[1], 'NASA CubeSat mission.'), (_SFNP[0], _SFNP[1], 'NASA sustainable aviation.')]
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Mission, Stakeholders and Requirements', 'weeks': 'Week 1',
 'summary': 'Choosing a track, defining the mission, identifying stakeholders, writing verifiable requirements and setting allocations with margin.',
 'objectives': ['Write a one-sentence mission statement.', 'List stakeholders and their needs.', 'Write verifiable requirements.', 'Compute margin against an allocation.'],
 'concepts': ['Pick one track: a small electric drone that carries a sensor, or a 3U CubeSat that observes Earth.',
              'A mission statement says who needs what and why; requirements make it measurable.',
              'Stakeholders include users, funders, launch or airspace authorities, and the team itself.',
              'Each requirement has a number, a unit and a verification method (test, analysis, inspection or demonstration).',
              'Allocations carry margin early, because estimates grow as designs mature.'],
 'eqs': [('\\text{Margin}=\\frac{A-E}{E}', 'Margin of allocation over estimate'), ('m_{alloc}=m_{est}(1+M)', 'Allocation with margin'), ('m_{3U}\\approx3\\times1.33\\ \\text{kg}', 'Textbook 3U mass allowance'), ('\\sum w_i=1', 'Weights sum to one')],
 'worked': [
  _w('A 3U CubeSat has a 4.0 kg allocation (textbook value) and a 3.4 kg estimate. Margin?', ['(4.0 − 3.4)/3.4.'], '17.6%.'),
  _w('A drone sensor estimate is 0.8 kg. Allocate with 25% margin (sample values).', ['0.8 × 1.25.'], '1.0 kg.'),
  _w('Write a verifiable requirement for drone endurance.', ['Number, unit, method.'], '“The drone shall fly at least 30 minutes at 15 m/s, verified by flight test.”')],
 'practice': [('Margin if the estimate grows to 3.8 kg?', '5.26%.'), ('Three textbook 1.33 kg units?', '3.99 kg, about 4 kg.'),
              ('Name four stakeholders for a student CubeSat.', 'For example: science users, the university, the launch provider and the radio regulator.'), ('Is “the CubeSat shall be reliable” verifiable?', 'No; add a number and a method.')],
 'misc': [('Requirements describe the design.', 'They state needs, not solutions.'), ('Margin can be added later.', 'It is cheapest to hold early.'), ('One stakeholder is enough.', 'Missed stakeholders cause late surprises.')],
 'quiz': [_q('Mass margin…', ['17.6%', '15%', '0.6%', '85%'], 0, '(4.0 − 3.4)/3.4.'), _q('0.8 kg + 25%…', ['1.0 kg', '0.85 kg', '1.25 kg', '0.6 kg'], 0, 'Multiply.'),
          _q('Verification methods…', ['test, analysis, inspection, demonstration', 'guess, hope, wait, ship', 'cost, schedule, risk, scope', 'PDR, CDR, TRR, FRR'], 0, 'Four methods.'), _q('Mission statement says…', ['who needs what and why', 'the bolt sizes', 'the budget only', 'the launch date only'], 0, 'Purpose.')],
 'cards': [('Mission statement', 'Who needs what and why.'), ('Stakeholder', 'Anyone with a need or say.'), ('Requirement', 'Verifiable need.'), ('Allocation', 'Budgeted share.'), ('Margin', 'Reserve over estimate.'), ('Track', 'Drone or CubeSat project path.')],
 'planet': {'text': ['NASA’s CubeSat Launch Initiative provides opportunities for CubeSats built by U.S. educational institutions and non-profit organizations, including museums and science centers, to fly on upcoming launches; NASA says it has launched over 150 CubeSats.',
                     'NASA says its Announcement of Partnership Opportunity is typically released each August with proposals due in November, so a capstone can be shaped like a real proposal.'],
            'site': [('Spacecraft Design', 'Spacecraft_Design.html'), ('Avionics & Systems Engineering', 'Avionics_Systems_Engineering.html')],
            'src': [_CSLI]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook.'), (_CSLI[0], _CSLI[1], 'NASA CSLI.')]})
UNITS.append(
{'id': 'u2', 'title': 'Concept Generation and Selection', 'weeks': 'Week 2',
 'summary': 'Brainstorming, morphological charts, Pugh matrices, weighted decision matrices and sensitivity to weights.',
 'objectives': ['Generate several concepts.', 'Build a morphological chart.', 'Score concepts in a weighted matrix.', 'Test sensitivity to weights.'],
 'concepts': ['Generate many concepts before judging any; quantity first, quality later.',
              'A morphological chart lists options for each function and combines them into concepts.',
              'A Pugh matrix compares concepts to a datum with +, 0 and −.',
              'A weighted decision matrix multiplies scores by weights and sums them.',
              'If small weight changes flip the winner, the decision needs more data.'],
 'eqs': [('S=\\sum w_is_i', 'Weighted score'), ('N=\\prod n_i', 'Morphological combinations'), ('P=n_+-n_-', 'Pugh net score'), ('\\sum w_i=1', 'Normalized weights')],
 'worked': [
  _w('Concept A scores 6 (cost), 9 (performance), 5 (risk); B scores 8, 6, 8. Weights 0.3, 0.5, 0.2. Winner?', ['A = 1.8 + 4.5 + 1.0 = 7.3.', 'B = 2.4 + 3.0 + 1.6 = 7.0.'], 'A, 7.3 to 7.0.'),
  _w('Change weights to 0.4, 0.3, 0.3.', ['A = 2.4 + 2.7 + 1.5 = 6.6.', 'B = 3.2 + 1.8 + 2.4 = 7.4.'], 'B wins: the choice is sensitive to weights.'),
  _w('A chart has 3 power options, 2 structures and 4 sensors. Combinations?', ['3 × 2 × 4.'], '24.')],
 'practice': [('Pugh: 4 pluses, 1 minus. Net?', '+3.'), ('Combinations for 2 × 3 × 3 × 2?', '36.'),
              ('Why test weight sensitivity?', 'To see if the winner is robust.'), ('Why brainstorm before scoring?', 'Early judging kills good ideas.')],
 'misc': [('The highest score is always right.', 'Check sensitivity and assumptions.'), ('Weights are objective.', 'They encode judgment.'), ('One concept is enough.', 'Compare several.')],
 'quiz': [_q('A’s score…', ['7.3', '7.0', '6.6', '20'], 0, 'Weighted sum.'), _q('B’s score…', ['7.0', '7.3', '7.4', '22'], 0, 'Weighted sum.'),
          _q('After reweighting…', ['B wins', 'A wins', 'tie', 'neither'], 0, '7.4 > 6.6.'), _q('Combinations…', ['24', '9', '12', '48'], 0, '3 × 2 × 4.')],
 'cards': [('Morphological chart', 'Options per function.'), ('Pugh matrix', 'Compare to a datum.'), ('Datum', 'Reference concept.'), ('Weighted matrix', 'Scores times weights.'), ('Sensitivity', 'How results change with inputs.'), ('Down-select', 'Choosing a concept.')],
 'planet': {'text': ['NASA’s Sustainable Flight National Partnership works in three areas: advanced vehicle technologies, efficient airline operations and sustainable aviation fuels.',
                     'Weighing options across areas like these is a concept-selection problem: the right weights depend on what the stakeholders value, including emissions.'],
            'site': [('Solutions', 'Solutions.html'), ('Aircraft Performance', 'Aircraft_Performance.html')],
            'src': [_SFNP]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT capstone materials.'), (_SEH[0], _SEH[1], 'Free NASA handbook.')]})
UNITS.append(
{'id': 'u3', 'title': 'Aircraft Track: Weight Sizing and Range', 'weeks': 'Weeks 3–4',
 'summary': 'Takeoff-weight estimation from weight fractions, the Breguet range equation, and how efficiency gains change range and fuel.',
 'objectives': ['Estimate takeoff weight from fractions.', 'Apply the Breguet range equation.', 'Show how L/D changes range.', 'Iterate a sizing loop.'],
 'concepts': ['Takeoff weight equals payload divided by one minus the empty and energy fractions.',
              'If the empty plus energy fractions approach 1, the design does not close.',
              'For jet aircraft, Breguet range is (V/c)(L/D) ln(W_i/W_f).',
              'Range is proportional to L/D, so a 30% L/D gain gives 30% more range at the same fuel fraction.',
              'Sizing is iterative: estimate, compute, update fractions, repeat until the weight converges.'],
 'eqs': [('W_0=\\frac{W_{pay}}{1-W_e/W_0-W_f/W_0}', 'Takeoff weight'), ('R=\\frac{V}{c}\\frac{L}{D}\\ln\\frac{W_i}{W_f}', 'Breguet range (jet)'), ('R\\propto L/D', 'Range scales with L/D'), ('W=mg', 'Weight')],
 'worked': [
  _w('A drone carries 1 kg payload with empty fraction 0.5 and battery fraction 0.3 (sample values). Takeoff mass?', ['1/(1 − 0.5 − 0.3).'], '5 kg.'),
  _w('A transport flies at 230 m/s with c = 0.6 per hour, L/D = 17 and W_i/W_f = 1.25 (textbook values). Range?', ['c = 1.667 × 10⁻⁴ s⁻¹.', 'R = (230/1.667 × 10⁻⁴) × 17 × ln 1.25 = 1.38 × 10⁶ × 17 × 0.2231.'], 'About 5235 km.'),
  _w('Raise L/D by 30%.', ['Range scales with L/D.'], 'About 6805 km.')],
 'practice': [('Takeoff mass if the battery fraction rises to 0.35?', '6.67 kg.'), ('Weight of the 5 kg drone?', '49.0 N.'),
              ('Why can’t fractions sum to 1?', 'Nothing would be left for payload.'), ('ln 1.25?', '0.223.')],
 'misc': [('More battery always means more range.', 'It also raises weight; the fraction matters.'), ('Breguet fits electric aircraft.', 'Batteries don’t get lighter; use an energy form.'), ('One pass is enough.', 'Iterate until weight converges.')],
 'quiz': [_q('Drone takeoff mass…', ['5 kg', '2 kg', '1.25 kg', '10 kg'], 0, '1/0.2.'), _q('Transport range…', ['≈ 5235 km', '≈ 523 km', '≈ 52,000 km', '≈ 1380 km'], 0, 'Breguet.'),
          _q('With +30% L/D…', ['≈ 6805 km', '≈ 5235 km', '≈ 4027 km', '≈ 10,470 km'], 0, '× 1.3.'), _q('Range scales with…', ['L/D', 'c', 'W_f', 'drag'], 0, 'Breguet.')],
 'cards': [('Empty fraction', 'Empty over takeoff weight.'), ('Fuel fraction', 'Fuel over takeoff weight.'), ('Breguet', 'Range equation.'), ('L/D', 'Lift-to-drag ratio.'), ('TSFC', 'Thrust-specific fuel consumption.'), ('Sizing loop', 'Iterate to convergence.')],
 'planet': {'text': ['NASA says the Sustainable Flight National Partnership aims to enable 25–30% energy-efficiency improvements in next-generation transports that can use 100% sustainable aviation fuel and fly optimal trajectories.',
                     'Its centerpiece is a full-scale X-plane demonstrator testing an ultra-efficient aerodynamic design, with first flight no earlier than late 2026; higher L/D is exactly the lever this unit’s Breguet equation rewards.'],
            'site': [('Aircraft Performance', 'Aircraft_Performance.html'), ('Solutions', 'Solutions.html')],
            'src': [_SFNP]},
 'res': [(_SFNP[0], _SFNP[1], 'NASA SFNP.'), (_MIT[0], _MIT[1], 'Free MIT capstone materials.')]})
UNITS.append(
{'id': 'u4', 'title': 'Aircraft Track: Wing Loading and Power', 'weeks': 'Week 5',
 'summary': 'Constraint sizing: wing loading from stall speed, wing area, and climb power for a small electric aircraft.',
 'objectives': ['Find wing loading from stall speed.', 'Size the wing area.', 'Compute climb power.', 'Draw a simple constraint diagram.'],
 'concepts': ['Stall speed sets the maximum wing loading: W/S = ½ρV_s²C_Lmax.',
              'Wing area follows from weight divided by wing loading.',
              'Shaft power for climb covers drag (W V/(L/D)) plus the climb term (W × rate of climb), divided by propulsive efficiency.',
              'Each requirement draws a line on a W/S versus power-to-weight plot; the design point lies in the region meeting all.',
              'Small drones fly at low Reynolds numbers, so check airfoil data for small scales.'],
 'eqs': [('\\frac{W}{S}=\\tfrac12\\rho V_s^2C_{L,max}', 'Stall wing loading'), ('S=\\frac{W}{W/S}', 'Wing area'), ('P=\\frac{W}{\\eta}\\left(\\frac{V}{L/D}+RC\\right)', 'Climb power'), ('q=\\tfrac12\\rho V^2', 'Dynamic pressure')],
 'worked': [
  _w('Stall at 12 m/s, C_Lmax = 1.2, sea level. Wing loading?', ['½ × 1.225 × 144 × 1.2.'], '105.8 N/m².'),
  _w('Wing area for the 5 kg drone?', ['49.03/105.84.'], '0.463 m².'),
  _w('Climb power at 15 m/s, L/D = 10, 2 m/s climb, η = 0.7?', ['49.03 × (1.5 + 2) = 171.6 W.', '171.6/0.7.'], '245 W.')],
 'practice': [('Wing loading for a 10 m/s stall?', '73.5 N/m².'), ('Power without the climb term?', '105.1 W.'),
              ('Dynamic pressure at 15 m/s?', '137.8 Pa.'), ('Why does stall set a maximum W/S?', 'Higher W/S needs higher stall speed.')],
 'misc': [('Bigger wings are always better.', 'They add weight and drag.'), ('Climb power is small.', 'It can dominate small drones.'), ('η = 1.', 'Propellers and motors lose energy.')],
 'quiz': [_q('W/S…', ['105.8 N/m²', '88.2', '1058', '10.6'], 0, '½ρV²C_L.'), _q('Wing area…', ['0.463 m²', '4.63 m²', '0.0463 m²', '1 m²'], 0, 'W/(W/S).'),
          _q('Climb power…', ['245 W', '171.6 W', '49 W', '490 W'], 0, 'Divide by η.'), _q('Design point lies…', ['where all constraints are met', 'on any line', 'at the origin', 'outside'], 0, 'Feasible region.')],
 'cards': [('Wing loading', 'Weight per wing area.'), ('C_Lmax', 'Maximum lift coefficient.'), ('Constraint diagram', 'Requirements on one plot.'), ('Rate of climb', 'Vertical speed.'), ('Propulsive efficiency', 'Useful power fraction.'), ('Stall speed', 'Minimum steady speed.')],
 'planet': {'text': ['NASA’s Sustainable Flight National Partnership also targets efficient airline operations and optimal trajectories, where power and climb choices meet fuel use.',
                     'Small electric drones sized well in this unit are already used for crop, forest and coastline surveys. Values in this unit are sample values.'],
            'site': [('Aircraft Performance', 'Aircraft_Performance.html'), ('Aerodynamics I', 'Aerodynamics_I.html')],
            'src': [_SFNP]},
 'res': [(_SFNP[0], _SFNP[1], 'NASA SFNP.'), (_MIT[0], _MIT[1], 'Free MIT capstone materials.')]})
UNITS.append(
{'id': 'u5', 'title': 'CubeSat Track: Sizing and Orbit', 'weeks': 'Week 6',
 'summary': 'CubeSat form factors, mass allowance, orbit period, passes per day and eclipse fraction for a low Earth orbit.',
 'objectives': ['Size a 3U CubeSat mass budget.', 'Compute orbit period.', 'Compute orbits per day.', 'Compute the worst-case eclipse.'],
 'concepts': ['CubeSats come in 10 cm units (U); a 3U is about 10 × 10 × 34 cm (textbook value).',
              'Mass allowance is roughly 1.33 kg per U (textbook value); confirm with the launch provider.',
              'Orbit period depends only on the semi-major axis: T = 2π√(a³/μ).',
              'In the worst case (Sun in the orbit plane), eclipse fraction is asin(R_E/a)/π.',
              'Low orbits decay faster from drag; most student CubeSats re-enter within years.'],
 'eqs': [('T=2\\pi\\sqrt{a^3/\\mu}', 'Orbital period'), ('f_e=\\frac{1}{\\pi}\\sin^{-1}\\frac{R_E}{a}', 'Worst-case eclipse fraction'), ('n=1440/T', 'Orbits per day (T in min)'), ('a=R_E+h', 'Semi-major axis')],
 'worked': [
  _w('Period at 500 km altitude?', ['a = 6878.1 km.', 'T = 2π√(6878.1³/398,600.4).'], '94.6 min.'),
  _w('Orbits per day?', ['1440/94.6.'], '15.2.'),
  _w('Worst-case eclipse?', ['asin(6378.1/6878.1)/π = 0.378.', '0.378 × 94.6.'], '35.8 min.')],
 'practice': [('3U mass allowance at 1.33 kg/U?', '3.99 kg.'), ('Sunlit time per orbit?', '58.9 min.'),
              ('Does period depend on CubeSat mass?', 'No.'), ('Why do low orbits decay?', 'Atmospheric drag.')],
 'misc': [('Heavier satellites orbit slower.', 'Period depends only on a.'), ('Eclipse is always 50%.', 'It depends on altitude and Sun angle.'), ('Use altitude in Kepler’s law.', 'Use a = R_E + h.')],
 'quiz': [_q('Period…', ['94.6 min', '90 min', '100 min', '84.4 min'], 0, '2π√(a³/μ).'), _q('Orbits per day…', ['15.2', '14.5', '16', '24'], 0, '1440/T.'),
          _q('Eclipse…', ['35.8 min', '47 min', '20 min', '0 min'], 0, '0.378 × 94.6.'), _q('3U mass…', ['≈ 4 kg', '≈ 1.33 kg', '≈ 12 kg', '≈ 40 kg'], 0, '3 × 1.33.')],
 'cards': [('CubeSat', 'Standard small satellite in 10 cm units.'), ('3U', 'Three-unit CubeSat.'), ('Period', 'Time per orbit.'), ('Eclipse fraction', 'Share of orbit in shadow.'), ('Semi-major axis', 'R_E + h for circular orbits.'), ('Decay', 'Orbit loss from drag.')],
 'planet': {'text': ['NASA says PREFIRE uses a pair of tiny satellites, CubeSats launched in May 2024, to measure a little-studied part of the radiant energy Earth emits, for clues about sea ice loss, ice-sheet melting and a warming Arctic.',
                     'NASA calls the Arctic the region that behaves like our planet’s thermostat, venting excess energy received in the tropics, which is why a pair of small satellites there matters.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Orbital Mechanics', 'Orbital_Mechanics.html')],
            'src': [_PRE]},
 'res': [(_PRE[0], _PRE[1], 'NASA PREFIRE.'), (_SOA[0], _SOA[1], 'Free NASA report.')]})
UNITS.append(
{'id': 'u6', 'title': 'CubeSat Track: Power and Link Budgets', 'weeks': 'Week 7',
 'summary': 'Solar-array output, orbit-average power, battery sizing for eclipse, UHF link path loss and daily data volume.',
 'objectives': ['Compute array output in sunlight.', 'Compute orbit-average power.', 'Size a battery for eclipse.', 'Estimate path loss and data per day.'],
 'concepts': ['Array power is solar flux × cell efficiency × area × cos(angle).',
              'Orbit-average generation is reduced by the eclipse fraction (and by pointing in practice).',
              'The battery covers the eclipse load; limiting depth of discharge extends cycle life.',
              'Free-space path loss grows as 20 log₁₀(4πd/λ); UHF amateur bands are common for student CubeSats.',
              'Data volume per day is bit rate × pass time × passes.'],
 'eqs': [('P=S\\eta A\\cos\\theta', 'Array output'), ('\\bar P=P(1-f_e)', 'Orbit-average generation'), ('E=\\frac{P_et_e}{DoD}', 'Battery capacity'), ('L=20\\log_{10}\\frac{4\\pi d}{\\lambda}', 'Path loss')],
 'worked': [
  _w('Panels of 0.06 m² with 28% cells face the Sun (sample values). Output?', ['1361 × 0.28 × 0.06.'], '22.9 W.'),
  _w('Orbit average with Unit 5’s eclipse fraction of 0.378?', ['22.86 × 0.622.'], '14.2 W.'),
  _w('Battery for 8 W through a 35.8 min eclipse at 30% depth of discharge?', ['8 × 35.75/60 = 4.77 Wh.', '4.77/0.3.'], '15.9 Wh.')],
 'practice': [('Path loss at 437 MHz over 1000 km?', 'λ = 0.686 m; L = 145.3 dB.'), ('Data per day at 9600 bit/s, four 10-minute passes?', '23.04 Mbit = 2.88 MB.'),
              ('Output at a 60° Sun angle?', '11.4 W.'), ('Why limit depth of discharge?', 'More cycles before the battery wears out.')],
 'misc': [('Sun power is constant around the orbit.', 'Eclipse and pointing cut it.'), ('Battery = eclipse energy.', 'Divide by DoD.'), ('More bits per second is free.', 'It needs more link margin.')],
 'quiz': [_q('Array output…', ['22.9 W', '2.29 W', '229 W', '38 W'], 0, 'SηA.'), _q('Orbit average…', ['14.2 W', '22.9 W', '8.6 W', '11.4 W'], 0, '× 0.622.'),
          _q('Battery…', ['15.9 Wh', '4.77 Wh', '47.7 Wh', '8 Wh'], 0, '÷ 0.3.'), _q('Path loss…', ['145.3 dB', '125 dB', '165 dB', '14.5 dB'], 0, '20 log₁₀(4πd/λ).')],
 'cards': [('Orbit-average power', 'Generation over a full orbit.'), ('DoD', 'Depth of discharge.'), ('Path loss', 'Spreading loss.'), ('UHF', 'Ultra-high-frequency band.'), ('Pass', 'Time a ground station sees the satellite.'), ('Data volume', 'Bits downlinked per day.')],
 'planet': {'text': ['NASA’s small spacecraft report says that when its first edition was published in 2013, 247 CubeSats and 105 other small spacecraft under 50 kg had been launched worldwide, less than 2% of the mass launched to orbit.',
                     'NASA says small spacecraft have since become the primary means for commercial, government, private and academic institutions to access space, so careful power and link budgets now support a large share of Earth observation.'],
            'site': [('Spacecraft Design', 'Spacecraft_Design.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_SOA]},
 'res': [(_SOA[0], _SOA[1], 'Free NASA report.'), (_MIT[0], _MIT[1], 'Free MIT capstone materials.')]})
UNITS.append(
{'id': 'u7', 'title': 'Structural and Thermal Checks', 'weeks': 'Week 8',
 'summary': 'Load factors, margins of safety, launch and flight loads, and a first thermal equilibrium estimate for both tracks.',
 'objectives': ['Compute a design load from a load factor.', 'Compute a margin of safety.', 'Estimate equilibrium temperature.', 'Decide what needs detailed analysis.'],
 'concepts': ['Design loads are weight times a load factor (launch or maneuver), times a factor of safety.',
              'Margin of safety MS = allowable/(FS × applied) − 1 must be positive.',
              'Aluminum 6061-T6 yields near 276 MPa (textbook value), a common choice for both drones and CubeSat frames.',
              'A first thermal estimate balances absorbed sunlight with emitted infrared; for α = ε a sunlit body near Earth sits near 278 K on average.',
              'Hand checks find the critical cases; finite-element and thermal models then refine them.'],
 'eqs': [('F=nmg', 'Load from load factor'), ('MS=\\frac{\\sigma_{allow}}{FS\\cdot\\sigma}-1', 'Margin of safety'), ('T=\\left(\\frac{\\alpha S}{4\\varepsilon\\sigma}\\right)^{1/4}', 'Average equilibrium temperature'), ('\\sigma=F/A', 'Normal stress')],
 'worked': [
  _w('A 4 kg CubeSat sees 10 g (sample load factor). Load?', ['10 × 4 × 9.80665.'], '392 N.'),
  _w('A rail sees 80 MPa; yield is 276 MPa; FS = 1.25. MS?', ['276/(1.25 × 80) − 1.'], '1.76, positive.'),
  _w('Average equilibrium temperature with α = ε?', ['(1361/(4 × 5.670374419 × 10⁻⁸))^¼.'], '278 K.')],
 'practice': [('MS if stress rises to 200 MPa?', '0.10.'), ('Load at 6 g on 5 kg?', '294 N.'),
              ('In °C, 278.3 K is?', '5.2 °C.'), ('Why a factor of safety?', 'Uncertain loads, materials and analysis.')],
 'misc': [('MS = 0 is fine.', 'Keep it positive.'), ('Space is cold, so no thermal problem.', 'Sunlit parts can overheat.'), ('Hand checks replace analysis.', 'They guide it.')],
 'quiz': [_q('Load…', ['392 N', '39 N', '3920 N', '40 N'], 0, 'nmg.'), _q('MS…', ['1.76', '2.76', '0.76', '−0.24'], 0, '276/100 − 1.'),
          _q('Equilibrium T…', ['278 K', '255 K', '300 K', '373 K'], 0, '(S/4σ)^¼.'), _q('MS must be…', ['positive', 'negative', 'zero', 'above 10'], 0, 'Definition.')],
 'cards': [('Load factor', 'Multiple of weight.'), ('Factor of safety', 'Multiplier on loads.'), ('Margin of safety', 'Allowable over required minus one.'), ('Yield strength', 'Stress for permanent set.'), ('Equilibrium temperature', 'Absorbed = emitted.'), ('FEA', 'Finite element analysis.')],
 'planet': {'text': ['NASA says PREFIRE’s twin CubeSats measure far-infrared emission from Earth, the same radiation this unit balances in its thermal estimate.',
                     'NASA reports the PREFIRE mission was extended so the twin satellites operate through at least September 2026, expanding focus from the poles to the whole planet, a payoff of a design that survived launch and orbit.'],
            'site': [('Aerospace Structures', 'Aerospace_Structures.html'), ('Heat Transfer', 'Heat_Transfer.html')],
            'src': [_PRE]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT capstone materials.'), (_SEH[0], _SEH[1], 'Free NASA handbook.')]})
UNITS.append(
{'id': 'u8', 'title': 'Cost, Schedule and Risk', 'weeks': 'Weeks 9–10',
 'summary': 'Work breakdown structures, critical-path schedules, earned value, risk matrices and mitigation plans.',
 'objectives': ['Build a work breakdown structure.', 'Find the critical path.', 'Compute CPI, SPI and estimate at completion.', 'Score and mitigate risks.'],
 'concepts': ['A work breakdown structure splits the project into deliverable pieces that can be estimated and assigned.',
              'The critical path is the longest chain of dependent tasks; any delay on it delays the project.',
              'Earned value compares planned value, earned value and actual cost.',
              'CPI = EV/AC and SPI = EV/PV; values under 1 mean over budget or behind schedule.',
              'Risks are scored likelihood × consequence and tracked with owners and mitigations.'],
 'eqs': [('CPI=EV/AC', 'Cost performance index'), ('SPI=EV/PV', 'Schedule performance index'), ('EAC=BAC/CPI', 'Estimate at completion'), ('R=L\\times C', 'Risk score')],
 'worked': [
  _w('PV = $50k, EV = $45k, AC = $48k (sample values). CPI and SPI?', ['CPI = 45/48.', 'SPI = 45/50.'], 'CPI = 0.9375, SPI = 0.90.'),
  _w('Budget at completion is $100k. EAC?', ['100/0.9375.'], '$106.7k.'),
  _w('Tasks in sequence take 3, 4, 5 and 2 weeks in a 15-week term. Slack?', ['Path = 14 weeks.', '15 − 14.'], '1 week.')],
 'practice': [('Risk score for likelihood 4, consequence 5?', '20 of 25.'), ('CPI = 1.1 means?', 'Under budget.'),
              ('Variance at completion for EAC $106.7k?', '−$6.7k.'), ('What is a WBS?', 'Work breakdown structure.')],
 'misc': [('Spending on plan means on schedule.', 'Compare earned value, not spend.'), ('Every task is critical.', 'Only the longest path is.'), ('Risks disappear when listed.', 'They need owners and actions.')],
 'quiz': [_q('CPI…', ['0.9375', '0.90', '1.067', '0.96'], 0, 'EV/AC.'), _q('SPI…', ['0.90', '0.9375', '1.11', '0.96'], 0, 'EV/PV.'),
          _q('EAC…', ['$106.7k', '$100k', '$93.8k', '$111k'], 0, 'BAC/CPI.'), _q('Slack…', ['1 week', '0 weeks', '14 weeks', '3 weeks'], 0, '15 − 14.')],
 'cards': [('WBS', 'Work breakdown structure.'), ('Critical path', 'Longest dependent chain.'), ('Earned value', 'Value of work done.'), ('CPI', 'EV/AC.'), ('SPI', 'EV/PV.'), ('Risk matrix', 'Likelihood × consequence.')],
 'planet': {'text': ['NASA’s Systems Engineering Handbook includes a full section on crosscutting technical management, alongside system design and product realization.',
                     'Projects that stay on budget and schedule launch sooner, and Earth-observing data starts flowing sooner. Cost values in this unit are sample values.'],
            'site': [('Solutions', 'Solutions.html'), ('Avionics & Systems Engineering', 'Avionics_Systems_Engineering.html')],
            'src': [_SEH]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook, Section 6.'), (_MIT[0], _MIT[1], 'Free MIT capstone materials.')]})
UNITS.append(
{'id': 'u9', 'title': 'Prototype, Test and Verification', 'weeks': 'Weeks 11–13',
 'summary': 'Verification matrices, test planning, measurement statistics, comparing results with predictions, and closing requirements.',
 'objectives': ['Build a verification matrix.', 'Compute mean and standard deviation.', 'Compare a measurement with an allocation.', 'Close or waive a requirement.'],
 'concepts': ['A verification matrix lists each requirement, its method, the test or analysis, and the result.',
              'Repeat measurements to estimate the mean and spread; report both.',
              'Compare results with predictions; large differences reveal model errors early.',
              'Test as you fly: use flight-like configurations and procedures.',
              'MIT’s 16.83X follows conceive, design, implement and operate phases, ending with testing in the intended environment.'],
 'eqs': [('\\bar x=\\frac1n\\sum x_i', 'Mean'), ('s=\\sqrt{\\frac{\\sum(x_i-\\bar x)^2}{n-1}}', 'Sample standard deviation'), ('\\text{Margin}=\\frac{A-\\bar x}{\\bar x}', 'Measured margin'), ('e=\\frac{x_m-x_p}{x_p}', 'Prediction error')],
 'worked': [
  _w('Five mass measurements: 3.38, 3.42, 3.40, 3.45, 3.35 kg. Mean?', ['Sum 17.00/5.'], '3.40 kg.'),
  _w('Sample standard deviation?', ['Deviations −0.02, 0.02, 0, 0.05, −0.05.', '√(0.0058/4).'], '0.038 kg.'),
  _w('Margin against the 4.0 kg allocation?', ['(4.0 − 3.40)/3.40.'], '17.6%: the requirement closes.')],
 'practice': [('Predicted 3.30 kg, measured 3.40 kg. Error?', '+3.03%.'), ('Why repeat measurements?', 'To estimate spread and catch mistakes.'),
              ('What does “test as you fly” mean?', 'Use flight-like hardware and procedures.'), ('Who approves a waiver?', 'The project’s review board or customer.')],
 'misc': [('One measurement is enough.', 'Report mean and spread.'), ('Tests prove a design perfect.', 'They show it meets requirements under test conditions.'), ('Disagreeing data is bad.', 'It teaches you about the model.')],
 'quiz': [_q('Mean…', ['3.40 kg', '3.38 kg', '3.45 kg', '17 kg'], 0, 'Sum/n.'), _q('Std dev…', ['0.038 kg', '0.38 kg', '0.0058 kg', '0.1 kg'], 0, 'Sample formula.'),
          _q('Margin…', ['17.6%', '15%', '0.6%', '−15%'], 0, '(4 − 3.4)/3.4.'), _q('Prediction error…', ['+3.03%', '−3.03%', '+0.1%', '+30%'], 0, '0.1/3.3.')],
 'cards': [('Verification matrix', 'Requirement-to-evidence table.'), ('Mean', 'Average.'), ('Standard deviation', 'Spread.'), ('Test as you fly', 'Flight-like testing.'), ('Waiver', 'Approved exception.'), ('CDIO', 'Conceive, design, implement, operate.')],
 'planet': {'text': ['MIT OpenCourseWare describes 16.83X as following a conceive-design-implement-operate model, with a final phase in which the system is tested and readied for its intended environment.',
                     'NASA’s CubeSat Launch Initiative flies student satellites that pass this kind of testing, turning capstones into working instruments in orbit.'],
            'site': [('Avionics & Systems Engineering', 'Avionics_Systems_Engineering.html'), ('Probability & Statistics', 'Probability_Statistics.html')],
            'src': [_MIT, _CSLI]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT capstone materials.'), (_SEH[0], _SEH[1], 'Free NASA handbook, Section 5.')]})
UNITS.append(
{'id': 'u10', 'title': 'Design Reviews and the Final Report', 'weeks': 'Weeks 14–15',
 'summary': 'Preliminary and critical design reviews, presenting trades and budgets, answering questions, and writing the final report.',
 'objectives': ['Plan a design review.', 'Present budgets with margins.', 'Track review action items.', 'Write a clear final report.'],
 'concepts': ['A preliminary design review shows the concept meets requirements with margin; a critical design review shows the detailed design is ready to build.',
              'Lead with requirements, then the design, then budgets, risks, test plans and open issues.',
              'Every review produces action items with owners and due dates.',
              'The final report tells the story from need to verified design, with numbers that trace to the spreadsheet.',
              'Honest discussion of what didn’t work is part of good engineering.'],
 'eqs': [('t_{talk}=n_{slides}\\times t_{slide}', 'Talk length'), ('\\text{Closure}=\\frac{n_{closed}}{n_{total}}', 'Action-item closure'), ('\\text{Margin}=\\frac{A-E}{E}', 'Budget margin'), ('\\text{Coverage}=\\frac{n_{verified}}{n_{req}}', 'Verification coverage')],
 'worked': [
  _w('A 20-minute review at 1.5 minutes per slide. Slides?', ['20/1.5.'], 'About 13.'),
  _w('A review leaves 12 action items; 9 are closed. Closure?', ['9/12.'], '75%.'),
  _w('30 of 32 requirements are verified. Coverage?', ['30/32.'], '93.75%.')],
 'practice': [('Slides for a 30-minute review at 2 min each?', '15.'), ('What follows PDR?', 'CDR.'),
              ('Closure with 11 of 12 closed?', '91.7%.'), ('Why show open issues?', 'Reviewers can help, and it builds trust.')],
 'misc': [('Reviews are exams.', 'They help the project.'), ('More slides is better.', 'Clarity beats volume.'), ('Hide problems.', 'Show them with plans.')],
 'quiz': [_q('Slides…', ['≈ 13', '20', '30', '5'], 0, '20/1.5.'), _q('Closure…', ['75%', '9%', '25%', '133%'], 0, '9/12.'),
          _q('Coverage…', ['93.75%', '30%', '96%', '6.25%'], 0, '30/32.'), _q('CDR shows…', ['design ready to build', 'first idea', 'launch done', 'budget only'], 0, 'Critical design.')],
 'cards': [('PDR', 'Preliminary design review.'), ('CDR', 'Critical design review.'), ('Action item', 'Task from a review.'), ('Final report', 'Need-to-verification story.'), ('Coverage', 'Share of verified requirements.'), ('Lessons learned', 'What to do differently.')],
 'planet': {'text': ['NASA says its Sustainable Flight National Partnership supports the aviation community’s goal of net-zero carbon emissions by 2050.',
                     'NASA says PREFIRE’s extended mission now looks at the whole planet; strong reviews and reports are how student and professional designs reach that kind of impact.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_SFNP, _PRE]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook.'), (_MIT[0], _MIT[1], 'Free MIT capstone materials.')]})
def _lab(i, t, wk, goal, eq, steps, table, calc, src, planet, psrc):
    return {'id': i, 'title': t, 'week': wk, 'goal': goal, 'eq': eq, 'steps': steps, 'table': table, 'note': 'Computed sample values.', 'calc': calc,
            'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'], 'sims': [src], 'planet': planet, 'planet_src': [psrc]}
LABS = [
 _lab('labA', 'Lab A: Requirements and margin tracker', 'Week 1', 'Build the requirements spreadsheet your whole project will use, with live margins.',
      ('\\text{Margin}=(A-E)/E', 'Margin'), ['List 10–20 requirements with number, unit and verification method.', 'Enter a 4.0 kg mass allocation (textbook 3U value) or a 5 kg drone allocation.', 'Enter estimates of 3.4, 3.6 and 3.8 kg and compute margin.', 'Color margins under 10% red.'],
      (['Estimate (kg)', 'Margin'], [['3.4', '17.6%'], ['3.6', '11.1%'], ['3.8', '5.26%']]), ['(4.0 − 3.6)/3.6 = 11.1%.', '(4.0 − 3.8)/3.8 = 5.26%.'],
      (_SEH[0], _SEH[1]), 'NASA’s CubeSat Launch Initiative has launched over 150 CubeSats.', _CSLI),
 _lab('labB', 'Lab B: Concept-selection matrix with sensitivity', 'Week 2', 'Score two concepts and test how weights change the winner.',
      ('S=\\sum w_is_i', 'Weighted score'), ['Enter Unit 2’s scores: A (6, 9, 5), B (8, 6, 8).', 'Score with three weight sets.', 'Plot the winner against the performance weight.', 'Write one paragraph defending your choice.'],
      (['Weights (cost, perf., risk)', 'A', 'B'], [['0.3, 0.5, 0.2', '7.3', '7.0'], ['0.4, 0.3, 0.3', '6.6', '7.4'], ['0.2, 0.6, 0.2', '7.6', '6.8']]), ['A = 0.2 × 6 + 0.6 × 9 + 0.2 × 5 = 7.6.', 'B = 0.2 × 8 + 0.6 × 6 + 0.2 × 8 = 6.8.'],
      (_MIT[0], _MIT[1]), 'NASA’s SFNP works across vehicles, operations and sustainable fuels.', _SFNP),
 _lab('labC', 'Lab C: Drone sizing loop', 'Week 4', 'Size the drone track’s takeoff mass for several battery fractions.',
      ('W_0=W_{pay}/(1-f_e-f_b)', 'Takeoff mass'), ['Enter 1 kg payload and empty fraction 0.5.', 'Compute takeoff mass for battery fractions 0.25, 0.30 and 0.35.', 'Add wing area from W/S = 105.84 N/m².', 'Pick a design point and justify it.'],
      (['Battery fraction', 'Takeoff mass (kg)'], [['0.25', '4.0'], ['0.30', '5.0'], ['0.35', '6.67']]), ['1/(1 − 0.5 − 0.25) = 4.0 kg.', '1/(1 − 0.5 − 0.35) = 6.67 kg.'],
      (_MIT[0], _MIT[1]), 'NASA’s SFNP targets 25–30% energy-efficiency gains.', _SFNP),
 _lab('labD', 'Lab D: CubeSat orbit and eclipse', 'Week 6', 'Compute period and worst-case eclipse for candidate altitudes.',
      ('T=2\\pi\\sqrt{a^3/\\mu}', 'Period'), ['Enter altitudes 400, 500 and 600 km.', 'Compute T and orbits per day.', 'Compute worst-case eclipse minutes.', 'Choose an altitude and note the drag-lifetime trade.'],
      (['Altitude (km)', 'T (min)', 'Eclipse (min)'], [['400', '92.6', '36.1'], ['500', '94.6', '35.8'], ['600', '96.7', '35.5']]), ['T(600) = 2π√(6978.1³/398,600.4) = 96.7 min.', 'Eclipse(400) = 0.390 × 92.6 = 36.1 min.'],
      (_SOA[0], _SOA[1]), 'NASA: PREFIRE’s CubeSats launched in May 2024.', _PRE),
 _lab('labE', 'Lab E: Power and data budget', 'Week 7', 'Close the CubeSat power and data budgets with margin.',
      ('V=R_bt_pn_p', 'Daily data volume'), ['Enter array output 22.9 W and orbit average 14.2 W.', 'List loads and compare with the orbit average.', 'Compute data per day at 9600 bit/s for 2, 4 and 6 ten-minute passes.', 'Compare with your payload’s daily data.'],
      (['Passes per day', 'Data (Mbit)'], [['2', '11.52'], ['4', '23.04'], ['6', '34.56']]), ['9600 × 600 × 2 = 11.52 Mbit.', '9600 × 600 × 6 = 34.56 Mbit.'],
      (_SOA[0], _SOA[1]), 'NASA: small spacecraft are now the primary means for many groups to access space.', _SOA),
 _lab('labF', 'Lab F: Earned-value tracker', 'Week 10', 'Track cost and schedule performance across three status dates.',
      ('CPI=EV/AC,\\ SPI=EV/PV', 'Performance indices'), ['Enter PV, EV and AC for three dates.', 'Compute CPI and SPI.', 'Compute EAC with BAC = $100k.', 'Write a one-line status for each date.'],
      (['PV, EV, AC ($k)', 'CPI', 'SPI'], [['20, 20, 22', '0.909', '1.00'], ['50, 45, 48', '0.9375', '0.90'], ['80, 76, 80', '0.95', '0.95']]), ['20/22 = 0.909.', '76/80 = 0.95.'],
      (_SEH[0], _SEH[1]), 'NASA’s handbook covers crosscutting technical management.', _SEH)]
SCHEDULE = [(1, 'u1', 'Mission and requirements; Lab A', 'NASA SE Handbook'), (2, 'u2', 'Concept selection; Lab B', 'MIT 16.83X'),
            (3, 'u3', 'Aircraft weight sizing', 'NASA SFNP'), (4, 'u3', 'Range and sizing loop; Lab C', 'MIT 16.83X'),
            (5, 'u4', 'Wing loading and power', 'NASA SFNP'), (6, 'u5', 'CubeSat sizing and orbit; Lab D', 'NASA PREFIRE'),
            (7, 'u6', 'Power and link budgets; Lab E; midterm practice', 'NASA SST SOA'), (8, 'u7', 'Structural and thermal checks', 'MIT 16.83X'),
            (9, 'u8', 'WBS and schedule', 'NASA SE Handbook'), (10, 'u8', 'Earned value and risk; Lab F', 'NASA SE Handbook'),
            (11, 'u9', 'Prototype planning', 'MIT 16.83X'), (12, 'u9', 'Testing', 'NASA CSLI'),
            (13, 'u9', 'Verification closure', 'NASA SE Handbook'), (14, 'u10', 'Critical design review', 'MIT 16.83X'), (15, 'u10', 'Final report; final practice', 'NASA SE Handbook')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Margin of a 4.0 kg allocation over a 3.6 kg estimate?', ['0.4/3.6.'], '11.1%.'),
  ('Takeoff mass for 2 kg payload, empty 0.45, battery 0.3?', ['2/0.25.'], '8 kg.'),
  ('Wing loading for a 14 m/s stall, C_Lmax 1.3?', ['½ × 1.225 × 196 × 1.3.'], '156.1 N/m².'),
  ('Period at 400 km?', ['a = 6778.1 km.'], '92.6 min.'),
  ('Breguet range with L/D = 20 instead of 17 (Unit 3 values)?', ['5235 × 20/17.'], '6159 km.')]),
 ('Final practice set (Units 1–10)', [
  ('Array of 0.09 m² at 30% efficiency?', ['1361 × 0.3 × 0.09.'], '36.7 W.'),
  ('Battery for 10 W over 36 min at 25% DoD?', ['10 × 0.6/0.25.'], '24 Wh.'),
  ('MS for 100 MPa, yield 276 MPa, FS 1.4?', ['276/140 − 1.'], '0.971.'),
  ('EAC with BAC $200k, EV 60, AC 64?', ['CPI = 0.9375.', '200/0.9375.'], '$213.3k.'),
  ('Mean and sample std dev of 2, 4, 6?', ['Mean 4.', '√(8/2).'], '4 and 2.'),
  ('Verification coverage, 45 of 50?', ['45/50.'], '90%.')])]
FORMULAS = ['\\text{Margin}=(A-E)/E,\\ m_{alloc}=m_{est}(1+M)', 'S=\\sum w_is_i,\\ N=\\prod n_i', 'W_0=W_{pay}/(1-f_e-f_b),\\ R=(V/c)(L/D)\\ln(W_i/W_f)',
            'W/S=\\tfrac12\\rho V_s^2C_{L,max},\\ P=W(V/(L/D)+RC)/\\eta', 'T=2\\pi\\sqrt{a^3/\\mu},\\ f_e=\\sin^{-1}(R_E/a)/\\pi', 'P=S\\eta A\\cos\\theta,\\ E=P_et_e/DoD,\\ L=20\\log_{10}(4\\pi d/\\lambda)',
            'F=nmg,\\ MS=\\sigma_{allow}/(FS\\,\\sigma)-1', 'CPI=EV/AC,\\ SPI=EV/PV,\\ EAC=BAC/CPI', '\\bar x=\\sum x_i/n,\\ s=\\sqrt{\\sum(x_i-\\bar x)^2/(n-1)}', '\\text{Coverage}=n_{verified}/n_{req}']
GLOSSARY = sorted([('Action item', 'Task assigned at a review.'), ('Allocation', 'Budgeted share of a resource.'), ('Breguet equation', 'Aircraft range equation.'), ('CDR', 'Critical design review.'),
    ('Constraint diagram', 'Requirements plotted against wing loading.'), ('CPI', 'Cost performance index.'), ('Critical path', 'Longest chain of dependent tasks.'), ('CubeSat', 'Small satellite built in 10 cm units.'),
    ('Depth of discharge', 'Share of battery capacity used.'), ('Earned value', 'Budgeted value of work done.'), ('Eclipse fraction', 'Share of an orbit in shadow.'), ('Margin of safety', 'Allowable over required minus one.'),
    ('Morphological chart', 'Options for each function.'), ('PDR', 'Preliminary design review.'), ('Pugh matrix', 'Comparison against a datum concept.'), ('Requirement', 'Verifiable statement of need.'),
    ('SPI', 'Schedule performance index.'), ('Verification matrix', 'Requirement-to-evidence table.'), ('Wing loading', 'Weight per wing area.'), ('Work breakdown structure', 'Project split into deliverables.')])
RUBRIC = [('4 · Mastery', 'Delivers a design that traces every number to a requirement, closes all budgets with margin, verifies requirements with evidence, and presents trades, risks and lessons clearly.'),
          ('3 · Proficient', 'Closes most budgets with margin and presents a clear design with minor gaps.'),
          ('2 · Developing', 'Has a concept and some budgets but weak requirement tracing or missing margins.'),
          ('1 · Beginning', 'Presents a design without requirements, budgets or verification; needs to revisit the units.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    mu = 398600.4418; Re = 6378.137; g0 = 9.80665; sig = 5.670374419e-8; S = 1361; c = 299792458
    per = lambda h: 2 * pi * sqrt((Re + h) ** 3 / mu) / 60
    fe = lambda h: asin(Re / (Re + h)) / pi
    W0 = lambda p, e, b: p / (1 - e - b)
    br = lambda LD: 230 / (.6 / 3600) * LD * log(1.25) / 1000
    ws = lambda V, C: .5 * 1.225 * V ** 2 * C
    lam = c / 437e6
    P = S * .28 * .06
    r = [
     ('u1 m', (4 - 3.4) / 3.4, .176), ('u1 a', .8 * 1.25, 1), ('u1 m38', (4 - 3.8) / 3.8, .0526), ('u1 3U', 3 * 1.33, 3.99), ('u1 x', 4 / 3, 1.333),
     ('u2 A', .3 * 6 + .5 * 9 + .2 * 5, 7.3), ('u2 B', .3 * 8 + .5 * 6 + .2 * 8, 7.0), ('u2 A2', .4 * 6 + .3 * 9 + .3 * 5, 6.6), ('u2 B2', .4 * 8 + .3 * 6 + .3 * 8, 7.4), ('u2 N', 3 * 2 * 4, 24),
     ('u2 N2', 2 * 3 * 3 * 2, 36), ('u2 P', 4 - 1, 3),
     ('u3 W0', W0(1, .5, .3), 5), ('u3 c', .6 / 3600, 1.667e-4), ('u3 Vc', 230 / (.6 / 3600), 1.38e6), ('u3 ln', log(1.25), .2231), ('u3 R', br(17), 5235), ('u3 R13', br(17) * 1.3, 6805),
     ('u3 W35', W0(1, .5, .35), 6.67), ('u3 W', 5 * g0, 49.0), ('u3 ln2', log(1.25), .223),
     ('u4 ws', ws(12, 1.2), 105.8), ('u4 S', 5 * g0 / ws(12, 1.2), .463), ('u4 Pc', 5 * g0 * (15 / 10 + 2), 171.6), ('u4 P', 5 * g0 * 3.5 / .7, 245), ('u4 ws10', ws(10, 1.2), 73.5), ('u4 P0', 5 * g0 * 1.5 / .7, 105.1),
     ('u4 q', .5 * 1.225 * 225, 137.8), ('u4 W', 5 * g0, 49.03),
     ('u5 a', Re + 500, 6878.1), ('u5 T', per(500), 94.6), ('u5 n', 1440 / per(500), 15.2), ('u5 f', fe(500), .378), ('u5 e', fe(500) * per(500), 35.8), ('u5 sun', per(500) * (1 - fe(500)), 58.9), ('u5 3U', 3 * 1.33, 3.99),
     ('u6 P', P, 22.9), ('u6 avg', P * (1 - fe(500)), 14.2), ('u6 E', 8 * fe(500) * per(500) / 60, 4.77), ('u6 B', 8 * fe(500) * per(500) / 60 / .3, 15.9), ('u6 lam', lam, .686),
     ('u6 L', 20 * log10(4 * pi * 1e6 / lam), 145.3), ('u6 D', 9600 * 600 * 4 / 1e6, 23.04), ('u6 MB', 9600 * 600 * 4 / 8e6, 2.88), ('u6 60', P * .5, 11.4), ('u6 1-f', 1 - fe(500), .622),
     ('u7 F', 10 * 4 * g0, 392), ('u7 MS', 276 / (1.25 * 80) - 1, 1.76), ('u7 T', (S / (4 * sig)) ** .25, 278), ('u7 MS2', 276 / (1.25 * 200) - 1, .104), ('u7 F6', 6 * 5 * g0, 294), ('u7 C', 278.32 - 273.15, 5.2),
     ('u8 CPI', 45 / 48, .9375), ('u8 SPI', 45 / 50, .9), ('u8 EAC', 100 / (45 / 48), 106.7), ('u8 path', 3 + 4 + 5 + 2, 14), ('u8 slack', 15 - 14, 1), ('u8 R', 4 * 5, 20), ('u8 VAC', 100 - 106.67, -6.7),
     ('u9 mean', (3.38 + 3.42 + 3.40 + 3.45 + 3.35) / 5, 3.40), ('u9 ss', .02 ** 2 * 2 + .05 ** 2 * 2, .0058), ('u9 s', sqrt(.0058 / 4), .038), ('u9 m', (4 - 3.4) / 3.4, .176), ('u9 e', (3.4 - 3.3) / 3.3, .0303), ('u9 sum', 3.38 + 3.42 + 3.40 + 3.45 + 3.35, 17),
     ('u10 sl', 20 / 1.5, 13.3), ('u10 cl', 9 / 12, .75), ('u10 cov', 30 / 32, .9375), ('u10 s30', 30 / 2, 15), ('u10 cl11', 11 / 12, .917),
     ('labA 34', (4 - 3.4) / 3.4, .176), ('labA 36', (4 - 3.6) / 3.6, .111), ('labA 38', (4 - 3.8) / 3.8, .0526),
     ('labB A1', .3 * 6 + .5 * 9 + .2 * 5, 7.3), ('labB B1', .3 * 8 + .5 * 6 + .2 * 8, 7.0), ('labB A2', .4 * 6 + .3 * 9 + .3 * 5, 6.6), ('labB B2', .4 * 8 + .3 * 6 + .3 * 8, 7.4), ('labB A3', .2 * 6 + .6 * 9 + .2 * 5, 7.6), ('labB B3', .2 * 8 + .6 * 6 + .2 * 8, 6.8),
     ('labC 25', W0(1, .5, .25), 4.0), ('labC 30', W0(1, .5, .3), 5.0), ('labC 35', W0(1, .5, .35), 6.67), ('labC ws', ws(12, 1.2), 105.84),
     ('labD T4', per(400), 92.6), ('labD T5', per(500), 94.6), ('labD T6', per(600), 96.7), ('labD e4', fe(400) * per(400), 36.1), ('labD e5', fe(500) * per(500), 35.8), ('labD e6', fe(600) * per(600), 35.5),
     ('labD f4', fe(400), .390), ('labD a6', Re + 600, 6978.1),
     ('labE 2', 9600 * 600 * 2 / 1e6, 11.52), ('labE 4', 9600 * 600 * 4 / 1e6, 23.04), ('labE 6', 9600 * 600 * 6 / 1e6, 34.56), ('labE P', P, 22.9), ('labE avg', P * (1 - fe(500)), 14.2),
     ('labF c1', 20 / 22, .909), ('labF s1', 20 / 20, 1), ('labF c2', 45 / 48, .9375), ('labF s2', 45 / 50, .9), ('labF c3', 76 / 80, .95), ('labF s3', 76 / 80, .95),
     ('mid m', .4 / 3.6, .111), ('mid W', W0(2, .45, .3), 8), ('mid ws', ws(14, 1.3), 156.1), ('mid T', per(400), 92.6), ('mid a', Re + 400, 6778.1), ('mid R', br(20), 6159),
     ('fin P', S * .3 * .09, 36.7), ('fin B', 10 * .6 / .25, 24), ('fin MS', 276 / 140 - 1, .971), ('fin CPI', 60 / 64, .9375), ('fin EAC', 200 / (60 / 64), 213.3), ('fin s', sqrt(8 / 2), 2), ('fin cov', 45 / 50, .9),
     ('c mu', mu, 398600.4418), ('c Re', Re, 6378.137), ('c g', g0, 9.80665), ('c S', S, 1361), ('c rho', 1.225, 1.225), ('c c', c, 299792458),
     ('x CSLI', 150, 150), ('x PRE', 2026 - 2024, 2), ('x SFNP lo', 1.25, 1.25), ('x SFNP hi', 1.30, 1.30), ('x SFNP y', 2050 - 2026, 24), ('x SOA', 247 + 105, 352), ('x SOA kg', 50, 50),
     ('x u3 r', 6805 / 5235, 1.3), ('x u4 r', 245 / 171.6, 1.428), ('x u5 r', 35.8 / 94.6, .378), ('x u6 r', 15.9 / 4.77, 3.33), ('x u7 r', 276 / 80, 3.45), ('x u8 r', 106.7 / 100, 1.067), ('x u10 r', 32 - 30, 2),
     ('x labC r', 6.67 / 4, 1.667), ('x labD r', 96.7 - 92.6, 4.1), ('x labE r', 34.56 / 11.52, 3), ('x mid r', 6159 / 5235, 1.176), ('x fin r', 213.3 - 200, 13.3),
     ('y u3 km', 5235 * .621371, 3253), ('y u4 lb', 5 * 2.20462, 11.02), ('y u5 s', per(500) * 60, 5677), ('y u6 dB', 20 * log10(2), 6.02), ('y u8 k', 106.67 - 100, 6.67),
     ('y u9 d', 3.45 - 3.35, .1), ('y u2 d', 7.4 - 6.6, .8), ('y labF d', .95 - .909, .041), ('y u1 d', 4 - 3.4, .6), ('y u5 h', 500 * .621371, 310.7), ('y u6 W', 22.86 - 14.22, 8.64),
     ('z u2 A1', .3 * 6, 1.8), ('z u2 A2', .5 * 9, 4.5), ('z u2 B1', .3 * 8, 2.4), ('z u2 B2', .5 * 6, 3.0), ('z u2 B3', .2 * 8, 1.6), ('z u3 f', 1 - .5 - .3, .2), ('z u4 V', 15 / 10, 1.5),
     ('z u4 V2', 12 ** 2, 144), ('z u5 sq', 6878.137 ** 3, 3.254e11), ('z u6 h', fe(500) * per(500) / 60, .596), ('z u6 sec', 600 * 4, 2400), ('z u7 FS', 1.25 * 80, 100), ('z u8 d', 50 - 45, 5),
     ('z u9 n', 5, 5), ('z u10 m', 20 / 1.5 * 1.5, 20), ('z mid f', 1 - .45 - .3, .25), ('z mid V', 14 ** 2, 196), ('z fin h', 36 / 60, .6), ('z fin MSd', 1.4 * 100, 140), ('z fin ss', 2 ** 2 * 2, 8),
     ('z labC f', 1 - .5 - .25, .25), ('z labE s', 600 * 2, 1200)]
    return r
