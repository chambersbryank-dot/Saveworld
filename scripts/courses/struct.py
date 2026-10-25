"""Aerospace Structures (AERO 330): flight loads and materials, wing shear and bending, thin-walled beam bending, torsion and shear flow in closed sections, open sections and the shear center, buckling of columns and plates, pressurized fuselages, composite materials, fatigue and damage tolerance, and lightweight design.
Oct 25 2026, founder-approved four-year track, junior course 5. Same module fields as perf.py / fluids.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, exp
ID = 'struct'
STATUS = 'live'
YEAR = 3
PAGE = 'Aerospace_Structures.html'
CODE = 'AERO 330'
TITLE = 'Aerospace Structures'
LAB_NAME = 'Structures lab'
TAGLINE = 'Light, strong structures for flight: flight loads, safety factors and material choice, wing shear and bending, thin-walled beams, torsion and shear flow in wing boxes, the shear center, column and plate buckling, pressurized fuselages, composites, fatigue and cracks, and how every kilogram saved cuts fuel, with six labs. Free, self-paced, and tied to NASA and DOE work on lightweight structures.'
DESC = 'Free self-study Aerospace Structures: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET, spreadsheet and home labs, practice exams, tied to composite wings and lightweight design.'
ALT = 'The International Space Station over the Ganges valley, seen from the Space Shuttle'
_PH = 'https://phet.colorado.edu/en/simulations/'
_O = 'https://openstax.org/books/university-physics-volume-1/pages/'
_MIT = ('MIT OpenCourseWare 16.20 Structural Mechanics (Fall 2002)', 'https://ocw.mit.edu/courses/16-20-structural-mechanics-fall-2002/')
_MITU = ('MIT OpenCourseWare 16.01–16.04 Unified Engineering (2005–2006)', 'https://ocw.mit.edu/courses/16-01-unified-engineering-i-ii-iii-iv-fall-2005-spring-2006/')
_MITC = ('MIT OpenCourseWare 3.032 Mechanical Behavior of Materials (Fall 2007)', 'https://ocw.mit.edu/courses/3-032-mechanical-behavior-of-materials-fall-2007/')
_CH3 = ('FAA PHAK Chapter 3: Aircraft Construction (PDF)', 'https://www.faa.gov/sites/faa.gov/files/05_phak_ch3.pdf')
_PHAK = ('FAA Pilot’s Handbook of Aeronautical Knowledge (FAA-H-8083-25C)', 'https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak')
_SWT = ('NASA: NASA Pushes New Wing Design to Find Structural Limits (Jul. 17, 2026)', 'https://www.nasa.gov/centers-and-facilities/armstrong/nasa-pushes-new-wing-design-to-find-structural-limits/')
_HIC = ('NASA: HiCAM Project Overview (Feb. 15, 2026)', 'https://www.nasa.gov/directorates/armd/aavp/hicam/about-hicam/')
_HICR = ('NASA: NASA Hosts 2026 Review on Advanced Composite Manufacturing (Jun. 4, 2026)', 'https://www.nasa.gov/directorates/armd/aavp/hicam/nasa-hosts-2026-review-on-advanced-composite-manufacturing/')
_TBW = ('NASA: NASA, Boeing Advance Truss-Braced Wing Research in Test (Apr. 29, 2026)', 'https://www.nasa.gov/image-article/nasa-boeing-advance-truss-braced-wing-research-in-test/')
_SUS = ('NASA: Sustainable Aviation', 'https://www.nasa.gov/directorates/armd/sustainable-aviation/')
_LW = ('U.S. DOE: Lightweight materials for cars and trucks', 'https://www.energy.gov/eere/vehicles/lightweight-materials-cars-and-trucks')
BANNER = ['images/ISS_Over_Ganges_STS102.jpg', 'images/ISS_Flyaround_2021.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg']
CREDITS = {'images/ISS_Over_Ganges_STS102.jpg': 'NASA (STS102-357-031, March 18, 2001)', 'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)',
           'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester junior aerospace structures course. It is modeled on the topics and depth of MIT 16.20 Structural Mechanics and the structures parts of MIT 16.01–16.04 Unified Engineering (free on MIT OpenCourseWare), and on courses such as Purdue AAE 352 and Georgia Tech AE 3140, using the FAA Pilot’s Handbook chapter on aircraft construction and PhET simulations, which we link where they help. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (composite truss-braced wings, high-rate composite manufacturing and lightweight materials), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation, a spreadsheet or a safe home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['An aircraft carries its own structure on every flight, so every kilogram of structure costs fuel for the aircraft’s whole life. Lighter wings and fuselages, made possible by better analysis and better materials, are one of the main levers for cleaner flight.',
                 'NASA lists efficient aircraft technology as one of the three main ways to make aviation sustainable. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Mechanics of Materials: stress, strain, bending, torsion and buckling basics.', 'Statics: free-body diagrams, shear and moment diagrams.',
           'Calculus II and Linear Algebra: integrals and matrices.', 'Aircraft Performance helps with load factors but is not required.']
STUDY = ['Start every problem with a free-body diagram and the load path: where does the load enter, and how does it reach the supports?', 'Keep limit and ultimate loads separate, and write the safety factor explicitly.',
         'For thin walls, think in shear flow q (N/m) first, then divide by thickness.', 'Check stiffness and buckling, not just strength: light structures usually fail by buckling.',
         'Compare materials per kilogram (specific stiffness and strength), not per cubic metre.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Hooke’s Law simulation.', 'A wooden or plastic ruler, a table edge, coins or small weights, tape and a second ruler for measuring.',
            'Dry spaghetti, a kitchen scale, paper clips and safety glasses.', 'Spreadsheet software for the materials, fuselage and composites labs.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab can be done in a free simulation, a spreadsheet, or with household items. Wear safety glasses when bending or breaking anything that can snap, keep loads small and close to the floor, and keep the work area clear of trip hazards.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('Aluminum 7075-T6 (textbook values)', 'E = 71.7 GPa, σ_y = 503 MPa, ρ = 2810 kg/m³, G = 27 GPa, ν = 0.33'), ('Titanium Ti-6Al-4V (textbook values)', 'E = 114 GPa, σ_y = 880 MPa, ρ = 4430 kg/m³'),
             ('Steel 4130 (textbook values)', 'E = 205 GPa, σ_y = 435 MPa, ρ = 7850 kg/m³'), ('Quasi-isotropic carbon/epoxy laminate (sample values)', 'E = 70 GPa, strength 600 MPa, ρ = 1600 kg/m³'),
             ('Sample airliner (sample values)', 'W = 588.6 kN, semispan 17 m, limit load factor 2.5, safety factor 1.5'), ('Gravity', 'g = 9.81 m/s²')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, handbooks and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT structures lectures and problem sets.'), (_MITU[0], _MITU[1], 'Free MIT notes on beams and materials.'), (_MITC[0], _MITC[1], 'Free MIT course on fatigue and fracture.'),
          (_CH3[0], _CH3[1], 'Free FAA chapter on aircraft structures.'), ('OpenStax University Physics Volume 1, 12.3 Stress, strain and elastic modulus', _O + '12-3-stress-strain-and-elastic-modulus', 'Free textbook section.'),
          ('PhET: Hooke’s Law', _PH + 'hookes-law', 'Stiffness interactively.')]
UNITS = []
_R12 = ('OpenStax UP1, 12.3 Stress, strain and elastic modulus', _O + '12-3-stress-strain-and-elastic-modulus', 'Free textbook section.')
_RS = ('OpenStax UP1, 12.2 Examples of static equilibrium', _O + '12-2-examples-of-static-equilibrium', 'Free textbook section.')
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS.append(
{'id': 'u1', 'title': 'Flight Loads, Safety Factors and Materials', 'weeks': 'Week 1',
 'summary': 'The structural parts of an aircraft and their load paths, load factors, limit and ultimate loads, the 1.5 safety factor, margin of safety, and choosing materials by specific stiffness and specific strength.',
 'objectives': ['Trace the load path through wing, fuselage and tail.', 'Compute limit and ultimate loads from a load factor.', 'Compute a margin of safety.', 'Compare materials by specific stiffness and strength.'],
 'concepts': ['Lift on the wing skins goes into stringers and ribs, then into spars, then through the wing box into the fuselage. Every part of an aircraft is sized by following that load path.',
              'Loads scale with load factor n = L/W. The limit load is the largest load expected in service (for example n = 2.5 for many transports); the structure must carry it without permanent deformation.',
              'The ultimate load is the limit load times a safety factor, traditionally 1.5 in aviation; the structure must carry it without failing, if only for a few seconds.',
              'Margin of safety MS = allowable/actual − 1. A positive margin passes; aircraft designers aim for small positive margins because extra margin means extra weight.',
              'Because weight matters, materials are compared per kilogram: specific stiffness E/ρ and specific strength σ/ρ. Aluminum, titanium and steel have almost the same E/ρ; carbon composites beat all three.'],
 'eqs': [('n=\\frac{L}{W}', 'Load factor'), ('P_{ult}=1.5\\,P_{limit}', 'Ultimate load'), ('MS=\\frac{\\sigma_{allow}}{\\sigma}-1', 'Margin of safety'), ('\\frac{E}{\\rho},\\ \\frac{\\sigma}{\\rho}', 'Specific stiffness and strength')],
 'worked': [
  _w('The sample airliner weighs 588.6 kN and has a limit load factor of 2.5. Find the limit and ultimate wing loads.', ['Limit = 2.5 × 588.6 = 1471.5 kN.', 'Ultimate = 1.5 × 1471.5.'], 'Limit 1471.5 kN; ultimate 2207 kN.'),
  _w('A 7075 part (σ_y = 503 MPa) sees 400 MPa at limit load. Find the margin of safety on yield.', ['MS = 503/400 − 1.'], 'MS = 0.258 (positive, so it passes).'),
  _w('Compare the specific stiffness of 7075 aluminum and the sample carbon laminate.', ['Al: 71.7 × 10⁹/2810 = 25.5 MJ/kg.', 'CFRP: 70 × 10⁹/1600 = 43.75 MJ/kg.'], 'The laminate is 1.71 times stiffer per kilogram.')],
 'practice': [('Find the specific strength of 7075 aluminum.', '503 × 10⁶/2810 = 179 kN·m/kg.'), ('Find the specific strength of Ti-6Al-4V.', '880 × 10⁶/4430 = 199 kN·m/kg.'),
              ('Find E/ρ for 4130 steel.', '205 × 10⁹/7850 = 26.1 MJ/kg, almost the same as aluminum.'), ('What does MS = −0.1 mean?', 'The part fails the requirement; redesign.')],
 'misc': [('A bigger safety factor is always better.', 'It adds weight and fuel burn for life.'), ('Steel is stiffer, so it makes stiffer aircraft.', 'Per kilogram it is no stiffer than aluminum.'),
          ('Ultimate load is the expected load.', 'Limit load is the expected maximum; ultimate is 1.5 times it.')],
 'quiz': [_q('Ultimate load equals…', ['1.5 × limit', 'limit', '2 × limit', 'limit/1.5'], 0, 'Aviation safety factor.'), _q('Specific stiffness is…', ['E/ρ', 'Eρ', 'σ/E', 'ρ/E'], 0, 'Per unit mass.'),
          _q('A positive margin of safety means…', ['the part passes', 'it fails', 'it is too light', 'nothing'], 0, 'Allowable exceeds actual.'), _q('Lift reaches the fuselage mainly through…', ['the spars and wing box', 'the windows', 'the engines', 'the landing gear'], 0, 'Load path.')],
 'cards': [('Load factor', 'n = L/W.'), ('Limit load', 'Largest expected in service.'), ('Ultimate load', '1.5 × limit.'), ('Margin of safety', 'σ_allow/σ − 1.'), ('Specific stiffness', 'E/ρ.'), ('Specific strength', 'σ/ρ.')],
 'planet': {'text': ['DOE’s lightweight-materials program reports that for cars and trucks a 10% cut in vehicle weight can improve fuel economy by 6% to 8%, because it takes less energy to accelerate a lighter object. DOE lists typical mass reductions of 50–70% for carbon fiber composites, 30–60% for aluminum and 40–55% for titanium when they replace conventional steel parts.',
                     'Aircraft gain even more than cars from weight savings, because they must also hold their weight up for the whole flight. Choosing materials by specific stiffness and strength is where that saving starts.'],
            'site': [('Mechanics of Materials', 'Mechanics_of_Materials.html'), ('Solutions', 'Solutions.html')],
            'src': [_LW]},
 'res': [(_CH3[0], _CH3[1], 'FAA chapter on airframe parts.'), _R12, (_MIT[0], _MIT[1], 'MIT structures notes.'), ('PhET: Hooke’s Law', _PH + 'hookes-law', 'Stiffness interactively.')]})
UNITS.append(
{'id': 'u2', 'title': 'Wing Shear and Bending Loads', 'weeks': 'Week 2',
 'summary': 'The wing as a cantilever beam, spanwise lift distributions, shear force and bending moment diagrams, root loads, relief from wing weight and fuel, and how load factor scales everything.',
 'objectives': ['Model a wing as a cantilever.', 'Draw shear and bending moment diagrams for a distributed lift.', 'Compute root shear and root bending moment.', 'Explain bending relief from fuel and engines on the wing.'],
 'concepts': ['Each wing half carries half the lift and acts as a cantilever clamped at the fuselage. Shear and moment are largest at the root.',
              'For a uniform lift w (N/m) on a semispan s, the root shear is V = ws and the root moment is M = ws²/2.',
              'An elliptical lift distribution puts the half-lift’s centroid at 4s/(3π) from the root, a little inboard of the uniform case’s s/2, so the root moment is lower.',
              'Wing structure and fuel weigh down on the wing, opposite to lift. This bending relief is why airliners carry fuel in the wings and why wing-mounted engines help.',
              'All loads scale with load factor: at n = 2.5 the root moment is 2.5 times its 1-g value.'],
 'eqs': [('V(y)=\\int_y^s w\\,dy', 'Shear from distributed load'), ('M(y)=\\int_y^s V\\,dy', 'Moment from shear'), ('M_{root}=\\tfrac12ws^2', 'Uniform lift'), ('M_{root}=\\tfrac{L}{2}\\cdot\\tfrac{4s}{3\\pi}', 'Elliptical lift')],
 'worked': [
  _w('The sample airliner (588.6 kN) has a 17 m semispan. Assuming uniform lift at 1 g, find w, root shear and root moment for one wing.', ['Half-lift = 294.3 kN; w = 294,300/17 = 17.31 kN/m.', 'V = 294.3 kN.', 'M = 17,312 × 17²/2.'], 'w = 17.31 kN/m; V = 294.3 kN; M = 2.50 MN·m.'),
  _w('Repeat the moment for the elliptical distribution.', ['M = 294,300 × 4 × 17/(3π).'], 'M = 2.12 MN·m, 15.1% lower.'),
  _w('Find the uniform-lift root moment at limit (n = 2.5) and ultimate (×1.5).', ['Limit: 2.5 × 2.50 = 6.25 MN·m.', 'Ultimate: 1.5 × 6.25.'], 'Limit 6.25 MN·m; ultimate 9.38 MN·m.')],
 'practice': [('Halve the semispan at the same lift. Root moment?', 'Halves (M = Ls/4 for uniform lift).'), ('Find the moment ratio, elliptical to uniform.', '8/(3π) = 0.849.'),
              ('Why do airliners use wing fuel first or last?', 'Fuel in the wing relieves bending; keeping it longer helps.'), ('Root shear at n = 2.5?', '2.5 × 294.3 = 735.8 kN.')],
 'misc': [('The wing tip carries the biggest loads.', 'The root does.'), ('Wing weight adds to the bending moment.', 'It relieves it.'), ('Moment scales with the semispan.', 'At fixed w it scales with s².')],
 'quiz': [_q('Root moment for uniform lift w on span s is…', ['ws²/2', 'ws', 'ws³', 'w/s'], 0, 'Cantilever.'), _q('Elliptical lift centroid is at…', ['4s/(3π)', 's/2', 's', 's/3'], 0, 'From the root.'),
          _q('Fuel in the wing…', ['relieves bending', 'adds bending', 'does nothing', 'adds torsion only'], 0, 'Acts against lift.'), _q('Doubling n doubles…', ['all loads', 'only shear', 'only weight', 'nothing'], 0, 'Linear.')],
 'cards': [('Cantilever wing', 'Clamped at the root.'), ('Root shear', 'Half-lift.'), ('Uniform root moment', 'ws²/2.'), ('Elliptical centroid', '4s/(3π).'), ('Bending relief', 'Wing weight and fuel.'), ('Load factor', 'Scales all loads.')],
 'planet': {'text': ['NASA’s SWEET-15 test article is a 15-foot composite wing supported by an aerodynamic strut, based on NASA’s Transonic Truss-Braced Wing concept. A strut takes part of the bending load near mid-span, so the wing can be long and thin without a huge root moment.',
                     'NASA engineers bent the test wing for several months in the Flight Loads Laboratory at Armstrong, using numerous strain and load sensors including fiber-optic strain sensors. The data confirmed the computer models’ predictions and showed the wing withstood the anticipated in-flight forces.'],
            'site': [('Statics', 'Statics.html'), ('Aircraft Performance', 'Aircraft_Performance.html')],
            'src': [_SWT]},
 'res': [_RS, (_MITU[0], _MITU[1], 'MIT beam notes.'), (_MIT[0], _MIT[1], 'MIT structures.'), (_CH3[0], _CH3[1], 'FAA chapter on wings.')]})
UNITS.append(
{'id': 'u3', 'title': 'Bending of Thin-Walled Beams', 'weeks': 'Weeks 3–4',
 'summary': 'Bending stress σ = My/I, idealizing a wing box as flanges and skins, second moment of area, flange forces, unsymmetric bending, and sizing spar caps for ultimate load.',
 'objectives': ['Compute bending stress from M, y and I.', 'Idealize a box beam as concentrated flange areas.', 'Size spar caps for an ultimate moment.', 'Recognize unsymmetric bending.'],
 'concepts': ['In bending, σ = My/I: stress grows linearly from the neutral axis. Material far from the neutral axis does most of the work.',
              'Wing boxes are idealized as concentrated flange (boom) areas carrying direct stress, joined by thin skins carrying shear.',
              'For two flanges of area A a depth h apart, I = 2A(h/2)² = Ah²/2 and the flange force is F = M/h.',
              'Deeper wing boxes need smaller flanges for the same moment. That is why thick wing roots save weight, and why thin, high-aspect-ratio wings need help such as struts.',
              'If the section is not symmetric, or the moment is not about a principal axis, bending about one axis causes deflection about the other (unsymmetric bending).'],
 'eqs': [('\\sigma=\\frac{My}{I}', 'Bending stress'), ('I=\\sum A_iy_i^2', 'Idealized boom section'), ('F=\\frac{M}{h}', 'Flange force'), ('A=\\frac{M}{\\sigma_{allow}h}', 'Required flange area')],
 'worked': [
  _w('The ultimate root moment is 9.38 MN·m and the wing box is 0.6 m deep. Find the flange force.', ['F = 9.38 × 10⁶/0.6.'], 'F = 15.6 MN.'),
  _w('Size each flange for 400 MPa allowable stress.', ['A = 9.38 × 10⁶/(400 × 10⁶ × 0.6).'], 'A = 0.0391 m² (391 cm²) per flange.'),
  _w('Find I for two 0.0391 m² flanges 0.6 m apart, and check σ.', ['I = 0.0391 × 0.6²/2 = 0.00704 m⁴.', 'σ = 9.38 × 10⁶ × 0.3/0.00704.'], 'σ = 400 MPa, as designed.')],
 'practice': [('Double the box depth. Required flange area?', 'Halves.'), ('Where is bending stress zero?', 'At the neutral axis.'),
              ('Find I for flanges of 0.01 m² at ±0.25 m.', '2 × 0.01 × 0.25² = 0.00125 m⁴.'), ('Why are spar caps placed at the top and bottom?', 'Largest y gives the most I per kilogram.')],
 'misc': [('Thin skins carry most of the bending.', 'In the idealization, flanges and stringers carry direct stress; skins carry shear.'), ('Stress is uniform across a beam.', 'It varies linearly with y.'),
          ('A deeper beam is heavier.', 'It usually needs less flange material.')],
 'quiz': [_q('Bending stress is…', ['My/I', 'M/A', 'VQ/It', 'Tr/J'], 0, 'Flexure formula.'), _q('Flange force for depth h is…', ['M/h', 'Mh', 'M/h²', 'Vh'], 0, 'Couple.'),
          _q('Deeper boxes need…', ['smaller flanges', 'larger flanges', 'the same', 'no flanges'], 0, 'A ∝ 1/h.'), _q('In idealized boxes, skins carry…', ['shear', 'direct stress only', 'nothing', 'torsion only'], 0, 'Shear panels.')],
 'cards': [('Flexure', 'σ = My/I.'), ('Boom idealization', 'Flanges carry σ, skins carry q.'), ('Two-flange I', 'Ah²/2.'), ('Flange force', 'M/h.'), ('Depth', 'Deeper is lighter.'), ('Unsymmetric bending', 'Coupled deflections.')],
 'planet': {'text': ['NASA describes the truss-braced wing as a long, thin wing with aerodynamically shaped structural supports that could cut fuel and operating costs for future airliners. NASA and Boeing tested a semispan model of the concept in a large pressurized wind tunnel in December 2025.',
                     'A thin wing has a shallow wing box, so by F = M/h its flanges would need to be heavy. The strut lowers M, which lets the wing stay thin without growing heavy.'],
            'site': [('Mechanics of Materials', 'Mechanics_of_Materials.html'), ('Aerodynamics I', 'Aerodynamics_I.html')],
            'src': [_TBW]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on beam bending.'), (_MITU[0], _MITU[1], 'MIT notes.'), _R12, (_CH3[0], _CH3[1], 'FAA chapter on spars.')]})
UNITS.append(
{'id': 'u4', 'title': 'Torsion and Shear Flow in Closed Sections', 'weeks': 'Week 5',
 'summary': 'Shear flow q, Bredt–Batho torsion of thin-walled closed sections, skin shear stress, the rate of twist, multi-cell boxes, and why wings are built as closed boxes.',
 'objectives': ['Use shear flow q = τt.', 'Apply Bredt–Batho: T = 2Aq.', 'Compute the rate of twist of a closed section.', 'Explain why closed sections resist torsion so well.'],
 'concepts': ['In a thin wall, shear stress times thickness is the shear flow q = τt (N/m). Around a closed section carrying pure torque, q is constant.',
              'Bredt–Batho: T = 2A_e q, where A_e is the area enclosed by the wall’s midline.',
              'The rate of twist is dθ/dz = (T/(4A_e²G)) ∮ds/t.',
              'Closed boxes are far stiffer in torsion than open sections of the same material, which is why wings are built as torsion boxes from spars and skins.',
              'Wing torsion comes from lift acting ahead of or behind the shear center, and from ailerons and engines. Too little torsional stiffness can cause aileron reversal or flutter.'],
 'eqs': [('q=\\tau t', 'Shear flow'), ('T=2A_eq', 'Bredt–Batho'), ('\\frac{d\\theta}{dz}=\\frac{T}{4A_e^2G}\\oint\\frac{ds}{t}', 'Rate of twist'), ('\\tau=\\frac{T}{2A_et}', 'Skin shear stress')],
 'worked': [
  _w('A 2.0 m × 0.6 m wing box carries a 500 kN·m torque. Find the shear flow.', ['A_e = 1.2 m².', 'q = 500,000/(2 × 1.2).'], 'q = 208.3 kN/m.'),
  _w('Find the skin shear stress for 4 mm skins.', ['τ = 208,333/0.004.'], 'τ = 52.1 MPa.'),
  _w('Find the rate of twist (G = 27 GPa, uniform 4 mm wall).', ['∮ds/t = 5.2/0.004 = 1300.', 'dθ/dz = 500,000 × 1300/(4 × 1.2² × 27 × 10⁹).'], 'dθ/dz = 4.18 × 10⁻³ rad/m.')],
 'practice': [('A thin tube of radius 0.1 m and wall 2 mm carries 10 kN·m. Find τ.', 'T/(2πr²t) = 79.6 MPa.'), ('Find J for that tube.', '2πr³t = 1.257 × 10⁻⁵ m⁴.'),
              ('Double the enclosed area at the same torque. Shear flow?', 'Halves.'), ('Why does cutting a slit in a tube ruin its torsional stiffness?', 'It becomes an open section.')],
 'misc': [('Shear flow varies around a closed section in pure torsion.', 'It is constant.'), ('Thicker skins always help torsion most.', 'Enclosed area matters more.'), ('Open and closed sections are similar in torsion.', 'Closed ones are many times stiffer.')],
 'quiz': [_q('Bredt–Batho gives T =…', ['2Aq', 'Aq', 'qt', 'q/A'], 0, 'Closed section.'), _q('Shear flow is…', ['τt', 'τ/t', 'σt', 'T/A'], 0, 'Definition.'),
          _q('Wings are built as closed boxes for…', ['torsional stiffness', 'looks', 'fuel only', 'lift'], 0, 'Torsion box.'), _q('In pure torsion q is…', ['constant', 'zero', 'largest at corners', 'random'], 0, 'Equilibrium.')],
 'cards': [('Shear flow', 'q = τt.'), ('Bredt–Batho', 'T = 2A_e q.'), ('Twist rate', 'T∮ds/t/(4A_e²G).'), ('Torsion box', 'Closed spars and skins.'), ('Thin tube', 'τ = T/(2πr²t).'), ('Flutter', 'Needs torsional stiffness.')],
 'planet': {'text': ['NASA reports that SWEET-15 combined five advanced composite manufacturing and assembly technologies, and that the manufacturing approach, developed at Langley with the Integrated Structural Assembly of Advanced Composites robot, aims to produce lighter and stronger composite structures for aerospace vehicles.',
                     'A composite wing box still has to satisfy Bredt–Batho: the joints between skins and spars carry the shear flow that keeps the box from twisting.'],
            'site': [('Mechanics of Materials', 'Mechanics_of_Materials.html'), ('Dynamics', 'Dynamics.html')],
            'src': [_SWT]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on torsion.'), (_MITU[0], _MITU[1], 'MIT notes.'), (_CH3[0], _CH3[1], 'FAA chapter on wing structure.'), _R12]})
UNITS.append(
{'id': 'u5', 'title': 'Shear in Open Sections and the Shear Center', 'weeks': 'Week 6',
 'summary': 'Shear stress in beams τ = VQ/(It), shear flow in open thin-walled sections, the shear center, why channel sections twist under load, and shear lag.',
 'objectives': ['Use τ = VQ/(It).', 'Find shear flow in an open thin-walled section.', 'Locate the shear center qualitatively.', 'Explain why loads off the shear center cause twist.'],
 'concepts': ['Transverse shear produces shear stress τ = VQ/(It), where Q is the first moment of area beyond the cut.',
              'In open thin-walled sections, shear flow starts at zero at a free edge and builds up along the wall: q = VQ/I.',
              'The shear center is the point where a transverse load causes bending without twist. For symmetric I-beams and closed boxes it is on the symmetry axis; for a channel it lies outside the web.',
              'Loads applied away from the shear center twist the section. Designers place spars and stringers so the wing’s shear center sits where aerodynamic loads act, or provide enough torsional stiffness.',
              'Shear lag: in wide flanges, direct stress is highest near the webs and lower in between, so not all of the flange is fully effective.'],
 'eqs': [('\\tau=\\frac{VQ}{It}', 'Beam shear stress'), ('q=\\frac{VQ}{I}', 'Shear flow'), ('Q=\\int y\\,dA', 'First moment of area'), ('\\tau_{max}=\\frac{3V}{2A}', 'Rectangle, maximum')],
 'worked': [
  _w('A solid rectangular beam 20 mm wide and 60 mm deep carries 6 kN of shear. Find the maximum shear stress.', ['A = 1200 mm².', 'τ_max = 1.5 × 6000/1200.'], 'τ_max = 7.5 MPa at the neutral axis.'),
  _w('An I-beam web is 4 mm thick; at the neutral axis Q = 50 × 10³ mm³ and I = 20 × 10⁶ mm⁴. Find τ for V = 40 kN.', ['τ = 40,000 × 50,000/(20 × 10⁶ × 4).'], 'τ = 25 MPa.'),
  _w('Find the shear flow there.', ['q = τt = 25 × 4.'], 'q = 100 N/mm (100 kN/m).')],
 'practice': [('Where is shear flow zero in an open section?', 'At free edges.'), ('Shear center of a closed symmetric box under symmetric load?', 'On the symmetry axis.'),
              ('Why does a channel twist when loaded through its web?', 'The shear center lies outside the web.'), ('Double V on the rectangle. τ_max?', '15 MPa.')],
 'misc': [('Shear stress is largest at the outer fibres.', 'It is largest at the neutral axis.'), ('The shear center is the centroid.', 'Only for doubly symmetric sections.'), ('Wide flanges are fully effective.', 'Shear lag reduces effectiveness.')],
 'quiz': [_q('Beam shear stress is…', ['VQ/(It)', 'My/I', 'Tr/J', 'P/A'], 0, 'Shear formula.'), _q('At a free edge, open-section shear flow is…', ['zero', 'maximum', 'constant', 'negative'], 0, 'Boundary.'),
          _q('Loading through the shear center causes…', ['no twist', 'twist', 'buckling', 'yield'], 0, 'Definition.'), _q('τ_max in a rectangle is…', ['1.5V/A', 'V/A', '2V/A', '3V/A'], 0, 'Parabolic.')],
 'cards': [('Shear formula', 'τ = VQ/(It).'), ('Open section', 'q starts at zero at free edges.'), ('Shear center', 'No-twist load point.'), ('Channel', 'Shear center outside web.'), ('Rectangle', 'τ_max = 1.5V/A.'), ('Shear lag', 'Uneven flange stress.')],
 'planet': {'text': ['NASA’s SWEET-15 test ended with a deliberate test to failure. The wing failed at roughly 127% of its design limit load, with visible damage near the back edge of the wing and in the upper wing cover, giving insight into how the joints to the main strut and the jury strut behave beyond the flight envelope.',
                     'NASA notes this was the first time a representative composite truss-braced wing configuration had undergone this type of structural evaluation. Tests like this check exactly the shear and torsion predictions in Units 4 and 5.'],
            'site': [('Mechanics of Materials', 'Mechanics_of_Materials.html'), ('Statics', 'Statics.html')],
            'src': [_SWT]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on shear flow.'), (_MITU[0], _MITU[1], 'MIT notes.'), _RS, _R12]})
UNITS.append(
{'id': 'u6', 'title': 'Buckling of Columns, Stringers and Plates', 'weeks': 'Weeks 7–8',
 'summary': 'Euler column buckling and end conditions, slenderness, stringers as columns, plate buckling of skin panels, post-buckling strength of stiffened panels, and why light structures are usually sized by stability.',
 'objectives': ['Compute Euler buckling loads with end-fixity factors.', 'Compute the buckling stress of a skin panel.', 'Explain why stiffened panels carry load after skin buckling.', 'Recognize when buckling, not yield, governs.'],
 'concepts': ['A slender column buckles at P_cr = π²EI/(KL)², where K = 1 for pinned ends, 0.5 for fixed ends and 2 for a cantilever.',
              'Buckling depends on stiffness E and geometry, not strength, so high-strength materials do not help a slender column.',
              'A thin flat plate in compression buckles at σ_cr = kπ²E/(12(1 − ν²)) (t/b)², with k = 4 for a long simply supported panel.',
              'Aircraft skins are allowed to buckle in shear or compression at loads well below ultimate; the stringers and spars then carry the load (tension-field and post-buckling behavior).',
              'Because light structures are thin, buckling usually sets the size of compression skins, stringers and spar webs.'],
 'eqs': [('P_{cr}=\\frac{\\pi^2EI}{(KL)^2}', 'Euler buckling'), ('\\sigma_{cr}=\\frac{k\\pi^2E}{12(1-\\nu^2)}\\left(\\frac tb\\right)^2', 'Plate buckling'), ('\\lambda=\\frac{KL}{r}', 'Slenderness'), ('r=\\sqrt{I/A}', 'Radius of gyration')],
 'worked': [
  _w('An aluminum stringer (E = 71.7 GPa, I = 2 × 10⁻⁸ m⁴) spans 0.5 m between ribs, pinned. Find P_cr.', ['P_cr = π² × 71.7 × 10⁹ × 2 × 10⁻⁸/0.5².'], 'P_cr = 56.6 kN.'),
  _w('Repeat with fixed ends (K = 0.5).', ['Four times the pinned value.'], 'P_cr = 226 kN.'),
  _w('Find the buckling stress of a 2 mm skin panel 150 mm wide (k = 4, ν = 0.33).', ['σ_cr = 4π² × 71.7 × 10⁹/(12 × 0.891) × (0.002/0.15)².'], 'σ_cr = 47.1 MPa, far below the 503 MPa yield.')],
 'practice': [('Halve the rib spacing. Stringer buckling load?', 'Four times.'), ('Double the skin thickness. σ_cr?', 'Four times: 188 MPa.'),
              ('Does a stronger alloy with the same E raise P_cr?', 'No.'), ('K for a flagpole (cantilever)?', '2.')],
 'misc': [('Buckling is a strength failure.', 'It is a stiffness (stability) failure.'), ('A buckled skin means a failed wing.', 'Stiffened panels carry load after skin buckling.'), ('Longer columns buckle at proportionally lower load.', 'At 1/L², much lower.')],
 'quiz': [_q('Euler load scales with…', ['1/L²', '1/L', 'L', 'L²'], 0, 'π²EI/L².'), _q('Fixed ends multiply P_cr by…', ['4', '2', '0.5', '1'], 0, 'K = 0.5.'),
          _q('Plate buckling stress scales with…', ['(t/b)²', 't/b', 'b/t', 't'], 0, 'Plate formula.'), _q('Buckling depends on…', ['E and geometry', 'yield strength', 'density', 'color'], 0, 'Stability.')],
 'cards': [('Euler', 'π²EI/(KL)².'), ('K', 'Pinned 1, fixed 0.5, cantilever 2.'), ('Plate', 'kπ²E(t/b)²/(12(1 − ν²)).'), ('k', '4 for a long supported plate.'), ('Post-buckling', 'Stiffeners carry load.'), ('Slenderness', 'KL/r.')],
 'planet': {'text': ['NASA’s HiCAM project lists resin infusion among the technologies it is evaluating: liquid molding that can make large, integrated structures with fewer fasteners, and thermoplastics that can be melted and welded for rapid joining.',
                     'Integrated stiffened panels, where stringers and skin are made as one piece, resist buckling without the weight of fasteners and splices. That is one route to the lighter composite airframes HiCAM aims for.'],
            'site': [('Mechanics of Materials', 'Mechanics_of_Materials.html'), ('Linear Algebra', 'Linear_Algebra.html')],
            'src': [_HIC]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on buckling.'), (_MITU[0], _MITU[1], 'MIT notes.'), (_CH3[0], _CH3[1], 'FAA chapter on stringers and skins.'), _R12]})
UNITS.append(
{'id': 'u7', 'title': 'Pressurized Fuselages and Thin Shells', 'weeks': 'Week 9',
 'summary': 'Cabin pressurization, hoop and axial stresses in thin cylinders, spherical bulkheads, combined pressure and bending, cutouts and stress concentrations around windows and doors, and fatigue from pressure cycles.',
 'objectives': ['Compute hoop and axial stress in a pressurized cylinder.', 'Find the skin thickness needed for a given stress.', 'Explain why windows are rounded.', 'Relate pressure cycles to fatigue.'],
 'concepts': ['A thin cylinder of radius r and wall t under pressure difference Δp has hoop stress σ_h = Δp r/t and axial stress σ_a = Δp r/(2t): the hoop stress is twice the axial.',
              'A spherical shell has σ = Δp r/(2t), so domed pressure bulkheads can be thinner than the cylinder.',
              'The fuselage also bends under its own weight and tail loads, adding to the axial stress on top or bottom.',
              'Cutouts for windows and doors concentrate stress; rounded corners and doublers keep the concentration low. Sharp corners can concentrate stress by a factor of three or more.',
              'Each flight is one pressure cycle. Over tens of thousands of flights, these cycles drive fatigue cracking, the subject of Unit 9.'],
 'eqs': [('\\sigma_h=\\frac{\\Delta p\\,r}{t}', 'Hoop stress'), ('\\sigma_a=\\frac{\\Delta p\\,r}{2t}', 'Axial stress'), ('\\sigma_{sphere}=\\frac{\\Delta p\\,r}{2t}', 'Spherical shell'), ('t=\\frac{\\Delta p\\,r}{\\sigma_{allow}}', 'Required thickness')],
 'worked': [
  _w('A fuselage of radius 2 m with 1.6 mm skin has a 55 kPa cabin pressure difference (sample value). Find the hoop and axial stresses.', ['σ_h = 55,000 × 2/0.0016.', 'σ_a = σ_h/2.'], 'σ_h = 68.75 MPa; σ_a = 34.4 MPa.'),
  _w('What thickness keeps the hoop stress at 100 MPa?', ['t = 55,000 × 2/100 × 10⁶.'], 't = 1.1 mm (before fatigue and damage-tolerance allowances).'),
  _w('Find the stress in a hemispherical bulkhead of the same radius and 1.6 mm thickness.', ['σ = 55,000 × 2/(2 × 0.0016).'], 'σ = 34.4 MPa.')],
 'practice': [('Double the fuselage radius at the same skin. Hoop stress?', 'Doubles.'), ('Why do fuselage cracks often run lengthwise?', 'Hoop stress, which opens them, is twice the axial.'),
              ('Why are airliner windows rounded?', 'To lower stress concentration.'), ('Lower the cabin pressure difference by 20%. Stress?', '20% lower.')],
 'misc': [('Axial and hoop stresses are equal.', 'Hoop is twice axial.'), ('A bigger fuselage can use the same skin.', 'Stress grows with radius.'), ('Pressure only matters at cruise.', 'Each cycle adds fatigue damage.')],
 'quiz': [_q('Hoop stress is…', ['Δp r/t', 'Δp r/(2t)', 'Δp t/r', 'Δp/t'], 0, 'Thin cylinder.'), _q('Hoop/axial ratio is…', ['2', '1', '0.5', '4'], 0, 'Cylinder.'),
          _q('Rounded windows reduce…', ['stress concentration', 'weight only', 'pressure', 'drag'], 0, 'Geometry.'), _q('Each flight is one…', ['pressure cycle', 'buckling event', 'yield', 'nothing'], 0, 'Fatigue.')],
 'cards': [('Hoop stress', 'Δp r/t.'), ('Axial stress', 'Δp r/(2t).'), ('Sphere', 'Δp r/(2t).'), ('Cutouts', 'Round corners, doublers.'), ('Pressure cycle', 'One per flight.'), ('Thickness', 'Δp r/σ.')],
 'planet': {'text': ['NASA’s HiCAM project is working toward large-scale manufacturing demonstrations of a composite fuselage barrel and wing box in 2028 and 2029. NASA notes that composite materials are already used in major portions of modern aircraft, including fuselage and wing sections of aircraft such as the Boeing 787.',
                     'A composite fuselage barrel carries the same hoop and axial stresses as a metal one; the gain is that composites carry them with less mass and do not corrode in the same way.'],
            'site': [('Mechanics of Materials', 'Mechanics_of_Materials.html'), ('Thermodynamics', 'Thermodynamics.html')],
            'src': [_HICR]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on shells.'), (_CH3[0], _CH3[1], 'FAA chapter on fuselages.'), _R12, (_MITU[0], _MITU[1], 'MIT notes.')]})
UNITS.append(
{'id': 'u8', 'title': 'Composite Materials and Laminates', 'weeks': 'Weeks 10–11',
 'summary': 'Fibers and matrices, fiber volume fraction, the rule of mixtures for stiffness and density, transverse stiffness, ply orientation and laminates, quasi-isotropic layups, and composite manufacturing.',
 'objectives': ['Use the rule of mixtures for longitudinal stiffness and density.', 'Estimate transverse stiffness.', 'Explain why laminates use several ply angles.', 'Compare composite and metal panels at equal stiffness.'],
 'concepts': ['A composite ply is stiff fibers (carbon, glass) in a softer matrix (epoxy or a thermoplastic). Fibers carry the load; the matrix holds them together and transfers load.',
              'Along the fibers the rule of mixtures holds: E₁ = E_fV_f + E_mV_m, and density ρ = ρ_fV_f + ρ_mV_m.',
              'Across the fibers the inverse rule applies: 1/E₂ = V_f/E_f + V_m/E_m, so a ply is many times less stiff transversely.',
              'Laminates stack plies at 0°, ±45° and 90° so the part is stiff in every direction it is loaded. A quasi-isotropic layup behaves almost like a metal sheet in-plane, but lighter.',
              'For a panel in bending at equal stiffness, mass scales as ρ/E^(1/3), which is why low-density materials win for skins.'],
 'eqs': [('E_1=E_fV_f+E_mV_m', 'Rule of mixtures'), ('\\frac{1}{E_2}=\\frac{V_f}{E_f}+\\frac{V_m}{E_m}', 'Inverse rule'), ('\\rho=\\rho_fV_f+\\rho_mV_m', 'Density'), ('\\frac{m_2}{m_1}=\\frac{\\rho_2}{\\rho_1}\\left(\\frac{E_1}{E_2}\\right)^{1/3}', 'Equal-stiffness panel mass')],
 'worked': [
  _w('Carbon fibers (E = 230 GPa, ρ = 1800 kg/m³) in epoxy (E = 3.5 GPa, ρ = 1200 kg/m³) at V_f = 0.6 (textbook values). Find E₁ and ρ.', ['E₁ = 230 × 0.6 + 3.5 × 0.4.', 'ρ = 1800 × 0.6 + 1200 × 0.4.'], 'E₁ = 139.4 GPa; ρ = 1560 kg/m³.'),
  _w('Find E₂.', ['1/E₂ = 0.6/230 + 0.4/3.5.'], 'E₂ = 8.55 GPa, 16.3 times lower than E₁.'),
  _w('A 7075 skin panel is replaced by the sample laminate (E = 70 GPa, ρ = 1600) at equal bending stiffness. Mass ratio?', ['m₂/m₁ = (1600/2810) × (71.7/70)^(1/3).'], 'm₂/m₁ = 0.574: 42.6% lighter.')],
 'practice': [('Find E₁ at V_f = 0.5.', '230 × 0.5 + 3.5 × 0.5 = 116.8 GPa.'), ('Why not make every ply 0°?', 'It would be weak and floppy in other directions.'),
              ('Find the specific stiffness of the unidirectional ply above.', '139.4 × 10⁹/1560 = 89.4 MJ/kg.'), ('What does the matrix do?', 'Holds fibers and transfers load.')],
 'misc': [('Composites are stiff in every direction.', 'Only along the fibers; layups fix this.'), ('More fiber is always better.', 'Too little matrix leaves dry spots.'), ('A composite is just light metal.', 'It is anisotropic and fails differently.')],
 'quiz': [_q('Longitudinal modulus follows…', ['the rule of mixtures', 'the inverse rule', 'Euler', 'Hooke only'], 0, 'Parallel springs.'), _q('Transverse modulus follows…', ['the inverse rule', 'the rule of mixtures', 'Bredt', 'Paris'], 0, 'Series springs.'),
          _q('±45° plies mainly carry…', ['shear', 'axial load only', 'pressure', 'heat'], 0, 'Shear directions.'), _q('Panel mass at equal stiffness scales as…', ['ρ/E^(1/3)', 'ρE', 'E/ρ', 'ρ'], 0, 'Bending.')],
 'cards': [('Fiber', 'Carries load.'), ('Matrix', 'Holds and transfers.'), ('Rule of mixtures', 'E_fV_f + E_mV_m.'), ('Inverse rule', '1/E₂ = V_f/E_f + V_m/E_m.'), ('Quasi-isotropic', '0/±45/90 layup.'), ('Panel index', 'ρ/E^(1/3).')],
 'planet': {'text': ['NASA says HiCAM aims to meet the demand to replace older, heavier transports with lightweight composite aircraft that reduce fuel consumption and carbon emissions. With its partners in the Advanced Composites Consortium, NASA is working to raise the production rate of composite aircraft.',
                     'NASA’s 2026 HiCAM spring review, held May 5–7 at Langley, brought together about 150 people from the consortium, a 22-member public-private partnership, and selected the technologies with the greatest impact on manufacturing rate for the next airplane program.'],
            'site': [('General Chemistry I', 'General_Chemistry_I.html'), ('Solutions', 'Solutions.html')],
            'src': [_HIC, _HICR]},
 'res': [(_MITC[0], _MITC[1], 'MIT materials course.'), (_MIT[0], _MIT[1], 'MIT notes on composites.'), (_CH3[0], _CH3[1], 'FAA chapter on composite construction.'), _R12]})
UNITS.append(
{'id': 'u9', 'title': 'Fatigue, Fracture and Damage Tolerance', 'weeks': 'Weeks 12–13',
 'summary': 'S-N curves and endurance, Miner’s rule for cumulative damage, stress concentrations, the stress intensity factor, fracture toughness and critical crack length, crack growth and the Paris law, and damage-tolerant design and inspection.',
 'objectives': ['Use Miner’s rule.', 'Compute the stress intensity factor for a crack.', 'Find a critical crack length.', 'Explain safe-life, fail-safe and damage-tolerant design.'],
 'concepts': ['Repeated loads well below yield can grow cracks until a part fails: fatigue. S-N curves give cycles to failure at each stress amplitude.',
              'Miner’s rule adds damage from different stress levels: D = Σ nᵢ/Nᵢ, with failure predicted at D = 1.',
              'A crack of length a under stress σ has stress intensity K = σ√(πa) (times a geometry factor). Fracture happens when K reaches the material’s fracture toughness K_IC.',
              'So the critical crack length is a_c = (K_IC/σ)²/π. Cracks grow per cycle as da/dN = C(ΔK)^m (Paris law), so inspection intervals are set to find cracks long before a_c.',
              'Modern aircraft are damage tolerant: they are designed to carry limit load with a crack or damage present until the next inspection finds it.'],
 'eqs': [('D=\\sum\\frac{n_i}{N_i}', 'Miner’s rule'), ('K=\\sigma\\sqrt{\\pi a}', 'Stress intensity'), ('a_c=\\frac{1}{\\pi}\\left(\\frac{K_{IC}}{\\sigma}\\right)^2', 'Critical crack length'), ('\\frac{da}{dN}=C(\\Delta K)^m', 'Paris law')],
 'worked': [
  _w('A part sees 10⁴ cycles at a level with N = 10⁵, and 2 × 10⁵ cycles at a level with N = 10⁶. Find the Miner damage.', ['D = 10⁴/10⁵ + 2 × 10⁵/10⁶.'], 'D = 0.30: 30% of life used.'),
  _w('Find K for a 10 mm crack under 100 MPa.', ['K = 100 × √(π × 0.01).'], 'K = 17.7 MPa√m.'),
  _w('Find the critical crack length at 100 MPa for an alloy with K_IC = 37 MPa√m (sample value).', ['a_c = (37/100)²/π.'], 'a_c = 43.6 mm.')],
 'practice': [('Double the stress. Critical crack length?', 'Quarter: 10.9 mm.'), ('What D does Miner predict at failure?', '1.'),
              ('Why do aircraft get scheduled inspections?', 'To find cracks before they reach a_c.'), ('Find K for a 40 mm crack at 50 MPa.', '50√(π × 0.04) = 17.7 MPa√m.')],
 'misc': [('Fatigue needs stress above yield.', 'It happens well below yield.'), ('A crack means the part must fail.', 'Damage-tolerant parts carry load until inspection.'), ('Miner’s rule is exact.', 'It is an estimate; load order matters.')],
 'quiz': [_q('Miner failure at…', ['D = 1', 'D = 0', 'D = 0.5', 'D = 2'], 0, 'Cumulative damage.'), _q('K scales with…', ['σ√a', 'σa', 'σ/a', 'a²'], 0, 'σ√(πa).'),
          _q('a_c scales with…', ['(K_IC/σ)²', 'K_IC/σ', 'σ', 'K_IC'], 0, 'Fracture.'), _q('Paris law describes…', ['crack growth', 'buckling', 'yield', 'creep'], 0, 'da/dN.')],
 'cards': [('Fatigue', 'Failure under repeated loads.'), ('S-N curve', 'Cycles to failure vs stress.'), ('Miner', 'Σ n/N = 1.'), ('Stress intensity', 'σ√(πa).'), ('Critical crack', '(K_IC/σ)²/π.'), ('Damage tolerance', 'Safe until found.')],
 'planet': {'text': ['NASA’s HiCAM portfolio includes automated inspection: robotic systems that find defects during the build, reducing time-consuming quality checks and repairs after production, and digital engineering models that predict structural performance and manufacturing defects before assembly.',
                     'Finding flaws early and predicting how they grow is the heart of damage tolerance. It lets designers use thinner, lighter structure with confidence.'],
            'site': [('Mechanics of Materials', 'Mechanics_of_Materials.html'), ('Statics', 'Statics.html')],
            'src': [_HIC]},
 'res': [(_MITC[0], _MITC[1], 'MIT course on fatigue and fracture.'), (_MIT[0], _MIT[1], 'MIT notes.'), (_CH3[0], _CH3[1], 'FAA chapter on construction.'), _R12]})
UNITS.append(
{'id': 'u10', 'title': 'Lightweight Design and Sustainable Structures', 'weeks': 'Weeks 14–15',
 'summary': 'Weight breakdowns, the snowball effect of weight growth, structural weight and fuel via the Breguet equation, material indices for lightweight design, multi-material and integrated structures, recycling and life-cycle thinking.',
 'objectives': ['Estimate fuel saved by removing structural weight.', 'Explain the weight snowball.', 'Use material indices to choose materials.', 'Discuss recycling and life-cycle trade-offs.'],
 'concepts': ['Structure is typically about a quarter to a third of an airliner’s takeoff weight (a textbook range), so structural weight is a major lever on fuel.',
              'Weight snowballs: extra structure needs more lift, more fuel and bigger engines, which add more structure. Savings snowball the same way in reverse.',
              'From the Breguet equation at fixed range, fuel burned = W_landing (e^(Rc/(V·L/D)) − 1), so fuel scales with landing weight; every kilogram saved cuts fuel in proportion.',
              'Material indices pick the lightest material for each job: E/ρ for ties, E^(1/2)/ρ for beams and E^(1/3)/ρ for panels in bending.',
              'Lifecycle matters too: manufacturing energy, repairability and recycling of composites and alloys all count alongside in-service fuel.'],
 'eqs': [('m_{fuel}=m_{land}\\left(e^{Rc/(V\\,L/D)}-1\\right)', 'Fuel at fixed range'), ('\\Delta m_{fuel}=\\Delta m\\left(e^{Rc/(V\\,L/D)}-1\\right)', 'Fuel saved per kilogram'), ('\\frac{E^{1/2}}{\\rho}', 'Beam index'), ('\\frac{E^{1/3}}{\\rho}', 'Panel index')],
 'worked': [
  _w('A jet lands at 45,000 kg after a flight whose Breguet exponent is 0.2877 (e^0.2877 = 1.333; sample values). How much fuel did it burn?', ['m_fuel = 45,000 × (1.3333 − 1).'], 'm_fuel = 15,000 kg.'),
  _w('Composite parts save 600 kg of structure. How much fuel is saved per flight?', ['Δm_fuel = 600 × 0.3333.'], 'About 200 kg per flight.'),
  _w('Rank aluminum, titanium, steel and the sample laminate by panel index E^(1/3)/ρ (GPa-based).', ['Al: 71.7^(1/3)/2810 × 1000 = 1.48.', 'Ti: 1.09; steel: 0.75; laminate: 2.58.'], 'Laminate first, then aluminum, titanium, steel.')],
 'practice': [('At 1000 flights a year, how much fuel does 200 kg per flight save?', '200 tonnes a year.'), ('Using 3.16 kg CO₂ per kg of fuel (a textbook value), CO₂ saved per year?', '632 tonnes.'),
              ('Which index applies to a wing spar in bending?', 'E^(1/2)/ρ (beam).'), ('Why can saving weight on a new design save more than its own mass?', 'The snowball effect.')],
 'misc': [('Only engines decide fuel burn.', 'Weight and drag matter as much.'), ('Composites are always greener.', 'Manufacturing and recycling also count.'), ('A kilogram saved saves a kilogram of fuel.', 'It saves a fraction per flight, over thousands of flights.')],
 'quiz': [_q('Fuel at fixed range scales with…', ['landing weight', 'wing color', 'altitude only', 'nothing'], 0, 'Breguet.'), _q('Panel index is…', ['E^(1/3)/ρ', 'E/ρ', 'Eρ', 'σ/E'], 0, 'Bending panel.'),
          _q('Weight snowball means…', ['savings compound', 'nothing', 'weight is fixed', 'only fuel changes'], 0, 'Resizing.'), _q('Beam index is…', ['E^(1/2)/ρ', 'E/ρ', 'E^(1/3)/ρ', 'ρ/E'], 0, 'Bending beam.')],
 'cards': [('Snowball', 'Weight changes compound.'), ('Fuel and weight', 'Fuel ∝ landing weight.'), ('Tie index', 'E/ρ.'), ('Beam index', 'E^(1/2)/ρ.'), ('Panel index', 'E^(1/3)/ρ.'), ('Lifecycle', 'Make, use, recycle.')],
 'planet': {'text': ['DOE estimates that using lightweight components and high-efficiency engines in one quarter of the U.S. vehicle fleet could save more than 5 billion gallons of fuel a year by 2030, and notes that lightweight materials are especially important for electric vehicles, where they offset battery weight and extend range.',
                     'NASA notes that needing less energy to fly means less fuel or, for electric aircraft, less power generated elsewhere, lowering lifecycle emissions for the whole time an aircraft is in use. Lightweight structure is how designers make that happen.'],
            'site': [('Aircraft Performance', 'Aircraft_Performance.html'), ('Solutions', 'Solutions.html')],
            'src': [_LW, _SUS]},
 'res': [(_MITC[0], _MITC[1], 'MIT materials course.'), (_MIT[0], _MIT[1], 'MIT structures.'), (_MITU[0], _MITU[1], 'MIT notes.'), (_LW[0], _LW[1], 'DOE lightweight materials.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Material selection by specific properties', 'week': 'Week 1',
 'goal': 'Build a spreadsheet of specific stiffness and strength for aerospace materials and rank them for ties, beams and panels.',
 'eq': ('\\frac{E}{\\rho},\\ \\frac{\\sigma}{\\rho},\\ \\frac{E^{1/3}}{\\rho}', 'Material indices'),
 'steps': ['Enter E, σ and ρ for 7075 aluminum, Ti-6Al-4V, 4130 steel and the sample carbon laminate.', 'Compute E/ρ and σ/ρ.', 'Add the beam and panel indices.', 'Rank the materials for each job.'],
 'table': (['Material', 'E/ρ (MJ/kg)', 'σ/ρ (kN·m/kg)'], [['7075 Al', '25.5', '179'], ['Ti-6Al-4V', '25.7', '199'], ['4130 steel', '26.1', '55.4'], ['Carbon laminate', '43.75', '375']]),
 'note': 'Computed from textbook and sample values.',
 'calc': ['Al: 71.7 × 10⁹/2810 = 25.5 MJ/kg.', 'Laminate: 600 × 10⁶/1600 = 375 kN·m/kg.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('PhET: Hooke’s Law', _PH + 'hookes-law'), (_MITC[0], _MITC[1])],
 'planet': 'DOE lists 50–70% mass reductions for carbon fiber composites replacing steel parts.', 'planet_src': [_LW]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Ruler cantilever deflection', 'week': 'Week 3',
 'goal': 'Measure how a ruler clamped at a table edge deflects under a small weight and compare with beam theory.',
 'eq': ('\\delta=\\frac{PL^3}{3EI},\\ \\ I=\\frac{bt^3}{12}', 'Cantilever tip deflection'),
 'steps': ['Explore stiffness in PhET Hooke’s Law.', 'Tape a ruler flat to a table so 0.25 m overhangs.', 'Hang a 100 g bag of coins (about 1 N) at the tip; measure the tip drop against a second ruler.', 'Repeat at 0.20 m overhang and compare with δ ∝ L³.'],
 'table': (['Overhang', 'Load', 'Predicted deflection'], [['0.25 m', '1 N', '7.72 mm'], ['0.20 m', '1 N', '3.95 mm']]),
 'note': 'Predicted for a wooden ruler 30 mm × 3 mm with E = 10 GPa (sample values); your ruler will differ.',
 'calc': ['I = 0.03 × 0.003³/12 = 6.75 × 10⁻¹¹ m⁴.', 'δ = 1 × 0.25³/(3 × 10 × 10⁹ × 6.75 × 10⁻¹¹) = 7.72 mm.'],
 'safety': ['Keep loads small; a snapping ruler can fling coins. Wear safety glasses.'], 'home': ['This is a home lab.'],
 'sims': [('PhET: Hooke’s Law', _PH + 'hookes-law')],
 'planet': 'NASA bent the SWEET-15 wing for months while fiber-optic sensors tracked strain.', 'planet_src': [_SWT]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Spaghetti column buckling', 'week': 'Week 8',
 'goal': 'Load single strands of dry spaghetti end-on on a kitchen scale and check Euler’s 1/L² law.',
 'eq': ('P_{cr}=\\frac{\\pi^2EI}{L^2},\\ \\ I=\\frac{\\pi d^4}{64}', 'Euler buckling, pinned ends'),
 'steps': ['Cut strands to 0.20 m and 0.10 m.', 'Stand one strand on a tared kitchen scale and press down gently with a flat object until it bows; note the peak reading.', 'Repeat five times for each length and average.', 'Compare the ratio with the predicted factor of 4.'],
 'table': (['Length', 'Predicted P_cr', 'Scale reading'], [['0.20 m', '0.381 N', '38.9 g'], ['0.10 m', '1.53 N', '155.5 g']]),
 'note': 'Predicted for 1.8 mm strands with E = 3 GPa (sample values); real pasta varies.',
 'calc': ['I = π × 0.0018⁴/64 = 5.15 × 10⁻¹³ m⁴.', 'P_cr(0.20) = π² × 3 × 10⁹ × 5.15 × 10⁻¹³/0.04 = 0.381 N.'],
 'safety': ['Wear safety glasses; snapped pasta flies.', 'Press gently with a book, not your palm.'], 'home': ['This is a home lab.'],
 'sims': [(_MIT[0], _MIT[1])],
 'planet': 'NASA HiCAM evaluates resin infusion for large integrated structures with fewer fasteners.', 'planet_src': [_HIC]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Fuselage pressure stress spreadsheet', 'week': 'Week 9',
 'goal': 'Compute hoop stress for fuselages of different sizes and find the skin needed for a target stress.',
 'eq': ('\\sigma_h=\\frac{\\Delta p\\,r}{t}', 'Hoop stress'),
 'steps': ['Set Δp = 55 kPa and t = 1.6 mm.', 'Compute σ_h for radii of 1.5, 2.0 and 3.0 m.', 'Find the skin thickness for 100 MPa at each radius.', 'Discuss why wide-body skins are thicker.'],
 'table': (['Radius', 'Hoop stress'], [['1.5 m', '51.6 MPa'], ['2.0 m', '68.75 MPa'], ['3.0 m', '103.1 MPa']]),
 'note': 'Computed values with a sample pressure difference.',
 'calc': ['σ_h(3.0) = 55,000 × 3/0.0016 = 103.1 MPa.', 't for 100 MPa at 3.0 m = 1.65 mm.'],
 'safety': ['Computer only. Never pressurize bottles or cans to test this.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_CH3[0], _CH3[1])],
 'planet': 'NASA HiCAM plans a composite fuselage barrel demonstration in 2028–2029.', 'planet_src': [_HICR]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Composite ply calculator', 'week': 'Week 11',
 'goal': 'Compute longitudinal and transverse stiffness of a carbon/epoxy ply against fiber volume fraction.',
 'eq': ('E_1=E_fV_f+E_mV_m,\\ \\ \\frac{1}{E_2}=\\frac{V_f}{E_f}+\\frac{V_m}{E_m}', 'Micromechanics'),
 'steps': ['Enter E_f = 230 GPa and E_m = 3.5 GPa.', 'Compute E₁ and E₂ for V_f = 0.4, 0.5 and 0.6.', 'Plot both against V_f.', 'Explain why E₂ barely changes.'],
 'table': (['V_f', 'E₁ (GPa)', 'E₂ (GPa)'], [['0.4', '94.1', '5.77'], ['0.5', '116.8', '6.90'], ['0.6', '139.4', '8.55']]),
 'note': 'Computed from textbook fiber and matrix values.',
 'calc': ['E₁(0.5) = 230 × 0.5 + 3.5 × 0.5 = 116.8 GPa.', 'E₂(0.4) = 1/(0.4/230 + 0.6/3.5) = 5.77 GPa.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MITC[0], _MITC[1])],
 'planet': 'NASA says HiCAM aims to replace older, heavier transports with lightweight composite aircraft.', 'planet_src': [_HIC]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Paper clip fatigue and Miner’s rule', 'week': 'Week 13',
 'goal': 'Bend paper clips back and forth to failure at two bend angles and test Miner’s rule.',
 'eq': ('D=\\sum\\frac{n_i}{N_i}', 'Miner’s rule'),
 'steps': ['Straighten several identical paper clips.', 'Bend one through ±90° until it breaks; count cycles. Repeat for ±45°.', 'On a fresh clip, do half the ±90° life, then bend at ±45° to failure.', 'Compare the second-stage cycles with Miner’s prediction.'],
 'table': (['Bend', 'Cycles to failure'], [['±90°', '12'], ['±45°', '30'], ['6 at ±90°, then ±45°', '15 predicted']]),
 'note': 'Sample values; your clips will differ, and load order changes the result.',
 'calc': ['6/12 = 0.5 of the life used at ±90°.', 'Remaining 0.5 × 30 = 15 cycles at ±45°.'],
 'safety': ['Wear safety glasses; broken ends are sharp and the wire gets hot.', 'Dispose of pieces safely.'], 'home': ['This is a home lab.'],
 'sims': [(_MITC[0], _MITC[1])],
 'planet': 'NASA HiCAM develops automated inspection to catch defects during the build.', 'planet_src': [_HIC]})
SCHEDULE = [(1, 'u1', 'Load paths, load factors, safety factors, materials; Lab A', 'FAA PHAK Ch. 3'), (2, 'u2', 'Wing shear and bending diagrams', 'MIT 16.01'),
            (3, 'u3', 'Bending stress and idealized sections; Lab B', 'MIT 16.20'), (4, 'u3', 'Spar cap sizing, unsymmetric bending', 'MIT 16.20'),
            (5, 'u4', 'Torsion and shear flow in closed sections', 'MIT 16.20'), (6, 'u5', 'Open sections and the shear center', 'MIT 16.20'),
            (7, 'u6', 'Column buckling; midterm practice', 'MIT 16.20'), (8, 'u6', 'Plate buckling and stiffened panels; Lab C', 'MIT 16.20'),
            (9, 'u7', 'Pressurized fuselages; Lab D', 'FAA PHAK Ch. 3'), (10, 'u8', 'Fibers, matrices, rule of mixtures', 'MIT 3.032'),
            (11, 'u8', 'Laminates and manufacturing; Lab E', 'NASA HiCAM'), (12, 'u9', 'Fatigue and Miner’s rule', 'MIT 3.032'),
            (13, 'u9', 'Fracture and damage tolerance; Lab F', 'MIT 3.032'), (14, 'u10', 'Weight, fuel and material indices', 'DOE lightweight materials'),
            (15, 'u10', 'Lifecycle and sustainable structures; final practice', 'NASA; DOE')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('A 10 kN aircraft has a limit load factor of 3.8. Find the ultimate load.', ['1.5 × 3.8 × 10.'], '57 kN.'),
  ('Find the root moment for uniform lift of 2 kN/m on a 5 m semispan.', ['2 × 5²/2.'], '25 kN·m.'),
  ('Find the flange force for 25 kN·m on a 0.1 m deep box.', ['25/0.1.'], '250 kN.'),
  ('A closed section encloses 0.05 m² and carries 20 kN·m. Find q.', ['20,000/(2 × 0.05).'], '200 kN/m.'),
  ('Find τ_max in a rectangular section of 600 mm² under 3 kN.', ['1.5 × 3000/600.'], '7.5 MPa.')]),
 ('Final practice set (all units)', [
  ('Find the Euler load of a 1 m pinned column with E = 70 GPa and I = 10⁻⁸ m⁴.', ['π² × 70 × 10⁹ × 10⁻⁸/1.'], '6909 N.'),
  ('Find the hoop stress for r = 1.8 m, Δp = 60 kPa, t = 1.5 mm.', ['60,000 × 1.8/0.0015.'], '72 MPa.'),
  ('Find E₁ for V_f = 0.55 (E_f = 230, E_m = 3.5 GPa).', ['230 × 0.55 + 3.5 × 0.45.'], '128.1 GPa.'),
  ('Find a_c for K_IC = 30 MPa√m at 150 MPa.', ['(30/150)²/π.'], '12.7 mm.'),
  ('Find Miner damage for 2 × 10⁴ of 10⁵ and 5 × 10⁵ of 10⁶ cycles.', ['0.2 + 0.5.'], '0.7.'),
  ('With a fuel factor of 0.25 per kilogram, how much fuel does 300 kg of saved structure save per flight?', ['300 × 0.25.'], '75 kg.')])]
FORMULAS = ['n=L/W,\\ P_{ult}=1.5P_{lim},\\ MS=\\sigma_{allow}/\\sigma-1', 'M_{root}=ws^2/2,\\ M_{ell}=(L/2)(4s/3\\pi)', '\\sigma=My/I,\\ F=M/h', 'q=\\tau t,\\ T=2A_eq,\\ d\\theta/dz=T\\oint ds/t/(4A_e^2G)',
            '\\tau=VQ/(It),\\ \\tau_{max}=3V/(2A)', 'P_{cr}=\\pi^2EI/(KL)^2,\\ \\sigma_{cr}=k\\pi^2E(t/b)^2/(12(1-\\nu^2))', '\\sigma_h=\\Delta pr/t,\\ \\sigma_a=\\Delta pr/(2t)',
            'E_1=E_fV_f+E_mV_m,\\ 1/E_2=V_f/E_f+V_m/E_m', 'D=\\sum n_i/N_i,\\ K=\\sigma\\sqrt{\\pi a},\\ a_c=(K_{IC}/\\sigma)^2/\\pi', 'E/\\rho,\\ E^{1/2}/\\rho,\\ E^{1/3}/\\rho']
GLOSSARY = sorted([('Buckling', 'Sudden sideways instability of a compressed member.'), ('Damage tolerance', 'Ability to carry load safely with cracks until inspection finds them.'), ('Fatigue', 'Failure under repeated loading below yield.'),
    ('Fracture toughness', 'Stress intensity at which a crack runs.'), ('Hoop stress', 'Circumferential stress in a pressurized cylinder.'), ('Laminate', 'Stack of composite plies at chosen angles.'), ('Limit load', 'Largest load expected in service.'),
    ('Load factor', 'Lift divided by weight.'), ('Margin of safety', 'Allowable over actual, minus one.'), ('Miner’s rule', 'Cumulative fatigue damage sum.'), ('Rib', 'Chordwise member that shapes the wing and supports stringers.'),
    ('Shear center', 'Point where a transverse load causes no twist.'), ('Shear flow', 'Shear force per unit length along a thin wall.'), ('Spar', 'Main spanwise beam of a wing.'), ('Specific stiffness', 'Elastic modulus divided by density.'),
    ('Stress intensity factor', 'Measure of stress near a crack tip.'), ('Stringer', 'Spanwise stiffener attached to the skin.'), ('Torsion box', 'Closed wing box resisting twist.'), ('Ultimate load', 'Limit load times the safety factor.'), ('Wing box', 'Spars and skins forming the main wing structure.')])
RUBRIC = [('4 · Mastery', 'Follows the load path, separates limit and ultimate loads, checks strength, stiffness, buckling and fatigue, and chooses materials by specific properties.'), ('3 · Proficient', 'Solves the practice problems with occasional unit slips.'),
          ('2 · Developing', 'Follows worked examples but checks only strength, not buckling.'), ('1 · Beginning', 'Plugs numbers into formulas without a load path; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    W = 588.6e3; s = 17; w = W / 2 / s
    Mu = 1.5 * 2.5 * w * s ** 2 / 2; Af = Mu / (400e6 * .6); I = Af * .6 ** 2 / 2
    pl = lambda t, b: 4 * pi ** 2 * 71.7e9 / (12 * (1 - .33 ** 2)) * (t / b) ** 2
    eu = lambda E, I_, L: pi ** 2 * E * I_ / L ** 2
    E1 = lambda v: 230 * v + 3.5 * (1 - v); E2 = lambda v: 1 / (v / 230 + (1 - v) / 3.5)
    Ip = pi * .0018 ** 4 / 64; Ir = .03 * .003 ** 3 / 12
    pi3 = lambda E, r: E ** (1 / 3) / r * 1000
    r = [
     ('u1 lim', 2.5 * W, 1471.5e3), ('u1 ult', 3.75 * W, 2207e3), ('u1 MS', 503 / 400 - 1, .258), ('u1 Ea', 71.7e9 / 2810, 25.5e6), ('u1 Ec', 70e9 / 1600, 43.75e6), ('u1 rat', 43.75 / 25.516, 1.71),
     ('u1 sa', 503e6 / 2810, 179e3), ('u1 st', 880e6 / 4430, 199e3), ('u1 Es', 205e9 / 7850, 26.1e6),
     ('u2 half', W / 2, 294.3e3), ('u2 w', w, 17.31e3), ('u2 M', w * s ** 2 / 2, 2.50e6), ('u2 Me', W / 2 * 4 * s / (3 * pi), 2.12e6), ('u2 pct', 1 - 8 / (3 * pi), .151), ('u2 Ml', 2.5 * w * s ** 2 / 2, 6.25e6), ('u2 Mu', Mu, 9.38e6),
     ('u2 rat', 8 / (3 * pi), .849), ('u2 V25', 2.5 * W / 2, 735.8e3),
     ('u3 F', Mu / .6, 15.6e6), ('u3 A', Af, .0391), ('u3 I', I, .00704), ('u3 s', Mu * .3 / I, 400e6), ('u3 I2', 2 * .01 * .25 ** 2, .00125),
     ('u4 q', 500e3 / 2.4, 208.3e3), ('u4 tau', 500e3 / 2.4 / .004, 52.1e6), ('u4 ds', 5.2 / .004, 1300), ('u4 tw', 500e3 * 1300 / (4 * 1.2 ** 2 * 27e9), 4.18e-3), ('u4 tube', 10e3 / (2 * pi * .1 ** 2 * .002), 79.6e6), ('u4 J', 2 * pi * .1 ** 3 * .002, 1.257e-5),
     ('u5 A', 20 * 60, 1200), ('u5 tm', 1.5 * 6000 / 1200, 7.5), ('u5 tau', 40000 * 50000 / (20e6 * 4), 25), ('u5 q', 25 * 4, 100), ('u5 t2', 1.5 * 12000 / 1200, 15),
     ('u6 P', eu(71.7e9, 2e-8, .5), 56.6e3), ('u6 Pf', eu(71.7e9, 2e-8, .25), 226e3), ('u6 nu', 1 - .33 ** 2, .891), ('u6 pl', pl(.002, .15), 47.1e6), ('u6 pl2', pl(.004, .15), 188e6),
     ('u7 h', 55e3 * 2 / .0016, 68.75e6), ('u7 a', 55e3 * 2 / .0032, 34.4e6), ('u7 t', 55e3 * 2 / 100e6, 1.1e-3), ('u7 sph', 55e3 * 2 / (2 * .0016), 34.4e6),
     ('u8 E1', E1(.6), 139.4), ('u8 rho', 1800 * .6 + 1200 * .4, 1560), ('u8 E2', E2(.6), 8.55), ('u8 r', E1(.6) / E2(.6), 16.3), ('u8 m', 1600 / 2810 * (71.7 / 70) ** (1 / 3), .574), ('u8 pct', 1 - 1600 / 2810 * (71.7 / 70) ** (1 / 3), .426),
     ('u8 E5', E1(.5), 116.8), ('u8 sp', 139.4e9 / 1560, 89.4e6),
     ('u9 D', 1e4 / 1e5 + 2e5 / 1e6, .30), ('u9 K', 100 * sqrt(pi * .01), 17.7), ('u9 ac', (37 / 100) ** 2 / pi, .0436), ('u9 ac2', (37 / 200) ** 2 / pi, .0109), ('u9 K2', 50 * sqrt(pi * .04), 17.7),
     ('u10 e', exp(.2877), 1.333), ('u10 f', 45000 * (exp(.2877) - 1), 15000), ('u10 s', 600 * (exp(.2877) - 1), 200), ('u10 Al', pi3(71.7, 2810), 1.48), ('u10 Ti', pi3(114, 4430), 1.09), ('u10 St', pi3(205, 7850), .75),
     ('u10 C', pi3(70, 1600), 2.58), ('u10 yr', 200 * 1000 / 1000, 200), ('u10 co2', 200 * 3.16, 632),
     ('A Ea', 71.7e9 / 2810, 25.5e6), ('A Et', 114e9 / 4430, 25.7e6), ('A Es', 205e9 / 7850, 26.1e6), ('A Ec', 70e9 / 1600, 43.75e6), ('A sa', 503e6 / 2810, 179e3), ('A st', 880e6 / 4430, 199e3), ('A ss', 435e6 / 7850, 55.4e3), ('A sc', 600e6 / 1600, 375e3),
     ('B I', Ir, 6.75e-11), ('B d25', .25 ** 3 / (3 * 10e9 * Ir), 7.72e-3), ('B d20', .2 ** 3 / (3 * 10e9 * Ir), 3.95e-3),
     ('C I', Ip, 5.15e-13), ('C P20', eu(3e9, Ip, .2), .381), ('C P10', eu(3e9, Ip, .1), 1.53), ('C g20', eu(3e9, Ip, .2) / 9.81 * 1000, 38.9), ('C g10', eu(3e9, Ip, .1) / 9.81 * 1000, 155.5),
     ('D 15', 55e3 * 1.5 / .0016, 51.6e6), ('D 20', 55e3 * 2 / .0016, 68.75e6), ('D 30', 55e3 * 3 / .0016, 103.1e6), ('D t', 55e3 * 3 / 100e6, 1.65e-3),
     ('E 41', E1(.4), 94.1), ('E 42', E2(.4), 5.77), ('E 51', E1(.5), 116.8), ('E 52', E2(.5), 6.90), ('E 61', E1(.6), 139.4), ('E 62', E2(.6), 8.55),
     ('F D', 6 / 12, .5), ('F n', .5 * 30, 15),
     ('M1', 1.5 * 3.8 * 10, 57), ('M2', 2 * 5 ** 2 / 2, 25), ('M3', 25 / .1, 250), ('M4', 20000 / (2 * .05), 200e3), ('M5', 1.5 * 3000 / 600, 7.5),
     ('F1', eu(70e9, 1e-8, 1), 6909), ('F2', 60e3 * 1.8 / .0015, 72e6), ('F3', E1(.55), 128.1), ('F4', (30 / 150) ** 2 / pi, .0127), ('F5', 2e4 / 1e5 + 5e5 / 1e6, .7), ('F6', 300 * .25, 75)]
    r += [('x u1 25', 2.5, 2.5), ('x u2 s2', s ** 2, 289), ('x u2 4s', 4 * s / (3 * pi), 7.215), ('x u3 h2', .6 ** 2, .36), ('x u3 y', .6 / 2, .3), ('x u4 Ae', 2 * .6, 1.2), ('x u4 per', 2 * (2 + .6), 5.2),
          ('x u4 A2', 1.2 ** 2, 1.44), ('x u5 Qr', 50000 / 20e6, .0025), ('x u6 L2', .5 ** 2, .25), ('x u6 tb', .002 / .15, .01333), ('x u6 k', 4 * pi ** 2, 39.48), ('x u7 r', 2 / .0016, 1250),
          ('x u8 vm', 1 - .6, .4), ('x u8 c', (71.7 / 70) ** (1 / 3), 1.008), ('x u8 d', 1600 / 2810, .569), ('x u9 pa', pi * .01, .0314), ('x u9 r', 37 / 100, .37), ('x u10 f', exp(.2877) - 1, .3333),
          ('x A dE', 43.75 - 25.5, 18.25), ('x B L3', .25 ** 3, .015625), ('x B r', (.2 / .25) ** 3, .512), ('x C d4', .0018 ** 4, 1.05e-11), ('x C r', eu(3e9, Ip, .1) / eu(3e9, Ip, .2), 4),
          ('x D r', 3 / 1.5, 2), ('x E r', E1(.6) / E1(.4), 1.481), ('x M4', 2 * .05, .1), ('x F1 p', pi ** 2, 9.87), ('x F2 r', 1.8 / .0015, 1200), ('x F4 r', 30 / 150, .2),
          ('x u2 n', 2.5 * 1.5, 3.75), ('x u1 rr', 2810 / 1600, 1.756), ('x u7 a', 2 / .0032, 625), ('x u3 Mh', 9.38e6 / .6, 15.63e6), ('x u6 4', eu(1, 1, .25) / eu(1, 1, .5), 4),
          ('x u9 ac', (37 / 100) ** 2, .1369), ('x u10 m', 600 / 15000, .04), ('x u5 ratio', 15 / 7.5, 2), ('x u8 f', 230 * .6, 138), ('x u8 m', 3.5 * .4, 1.4), ('x E 5', 230 * .5, 115),
          ('x u4 1', 500e3 / 2, 250e3), ('x u2 L', 294300 * 17 / 2, 2.50e6), ('x u7 c', 2 * 55e3, 110e3), ('x D 1', 55e3 * 1.5, 82500), ('x A 3', 205 / 71.7, 2.859), ('x C L', .2 ** 2, .04), ('x u1 lim', 1471.5 * 1.5, 2207), ('x u1 sf', 1.5, 1.5), ('x u2 w2', 294300 / 17, 17312), ('x u3 Af', .0391 * 1e4, 391), ('x u4 qt', 208333 * .004 / .004, 208333), ('x u4 G', 27e9 * 4 * 1.44, 1.5552e11), ('x u5 Qt', 20e6 * 4, 8e7), ('x u6 r', eu(71.7e9, 2e-8, .25) / 1000, 226), ('x u6 y', 47.1 / 503, .0936), ('x u7 h2', 68.75 / 34.375, 2), ('x u8 r2', 1800 * .6, 1080), ('x u8 r3', 1200 * .4, 480), ('x u9 D', 1 - .3, .7), ('x u9 sq', sqrt(pi * .01), .1772), ('x u10 a', 1000 * 200, 200000), ('x u10 c', 3.16 * 200, 632), ('x A t', 114 / 71.7, 1.59), ('x B E', 10e9 * Ir, .675), ('x E 6', 3.5 * .4, 1.4), ('x F1 E', 70e9 * 1e-8, 700), ('x F3 m', 3.5 * .45, 1.575)]
    return r
