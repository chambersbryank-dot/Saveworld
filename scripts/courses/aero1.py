"""Aerodynamics I (AERO 310): the standard atmosphere, fluid statics and Bernoulli, conservation laws and momentum theory, potential flow, airfoils and circulation, thin airfoil theory, finite wings and induced drag, viscous flow and boundary layers, compressible flow and shocks, and aircraft performance.
Oct 25 2026, founder-approved four-year track, junior course 1. Same module fields as statics.py / circuits.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, exp, log, atan, degrees, radians, sin, cos
ID = 'aero1'
STATUS = 'live'
YEAR = 3
PAGE = 'Aerodynamics_I.html'
CODE = 'AERO 310'
TITLE = 'Aerodynamics I'
LAB_NAME = 'Aerodynamics lab'
TAGLINE = 'Lift, drag and airflow over wings: the standard atmosphere, Bernoulli and pitot tubes, conservation laws and rotor momentum theory, potential flow, airfoils and the Kutta–Joukowski theorem, thin airfoil theory, finite wings and induced drag, boundary layers, compressible flow and shocks, and aircraft performance, with six labs. Free, self-paced, and tied to winglets, supercritical wings, truss-braced wings, wind turbines and flight on Mars.'
DESC = 'Free self-study Aerodynamics I: 10 units, worked examples, solved practice, quizzes, flashcards, 6 NASA FoilSim and home labs, practice exams, tied to winglets, efficient wings and wind turbines.'
ALT = 'NASA photo of the Artemis II launch'
_G = 'https://www.grc.nasa.gov/www/k-12/airplane/'
_O = 'https://openstax.org/books/university-physics-volume-1/pages/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_FS = ('NASA Glenn: FoilSim interactive airfoil simulator', 'https://www.grc.nasa.gov/www/k-12/FoilSim/index.html')
_MIT = ('MIT OpenCourseWare 16.100 Aerodynamics (Fall 2005)', 'https://ocw.mit.edu/courses/16-100-aerodynamics-fall-2005/')
_MITU = ('MIT OpenCourseWare 16.01–16.04 Unified Engineering (2005–2006)', 'https://ocw.mit.edu/courses/16-01-unified-engineering-i-ii-iii-iv-fall-2005-spring-2006/')
_BG = ('NASA Glenn: Beginner’s Guide to Aeronautics', _G + 'short.html')
_ATM = ('NASA Glenn: Earth atmosphere model (metric units)', _G + 'atmosmet.html')
_ING = ('NASA Science: Ingenuity Mars Helicopter', 'https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/')
_EPA = ('U.S. EPA: Regulations for greenhouse gas emissions from aircraft', 'https://www.epa.gov/regulations-emissions-vehicles-and-engines/regulations-greenhouse-gas-emissions-aircraft')
_WIND = ('U.S. DOE: How do wind turbines work?', 'https://www.energy.gov/eere/wind/how-do-wind-turbines-work')
_SC = ('NASA: How a NASA engineer created the modern airplane wing (2016)', 'https://www.nasa.gov/aeronautics/how-a-nasa-engineer-created-the-modern-airplane-wing/')
_WL = ('NASA Armstrong: On the winglets of innovation (2023)', 'https://www.nasa.gov/centers-and-facilities/armstrong/on-the-winglets-of-innovation-with-nasa-armstrong-2/')
_TTBW = ('NASA: NASA issues award for greener, more fuel-efficient airliner of future (Jan. 18, 2023)', 'https://www.nasa.gov/news-release/nasa-issues-award-for-greener-more-fuel-efficient-airliner-of-future/')
BANNER = ['images/ArtemisII_Launch_KSC_Hancock.jpg', 'images/ISS_Over_Ganges_STS102.jpg', 'images/JPSS2_Atlas_V_Launch_Pad.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg']
CREDITS = {'images/ArtemisII_Launch_KSC_Hancock.jpg': 'NASA', 'images/ISS_Over_Ganges_STS102.jpg': 'NASA (STS102-357-031, March 18, 2001)',
           'images/JPSS2_Atlas_V_Launch_Pad.jpg': 'NASA/Liz Wilk (KSC-20221109-PH-LNW01_0001)', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester junior aerodynamics course. It is modeled on the topics and depth of MIT 16.100 Aerodynamics and the fluids parts of MIT Unified Engineering (both free on MIT OpenCourseWare), and on junior aerodynamics courses such as Purdue AAE 333 and Georgia Tech AE 3030, using NASA Glenn’s free Beginner’s Guide to Aeronautics and FoilSim simulator, which we link where they help. None of those authors or schools endorses this page.',
         'What we add: every unit ties to real work with a cited public source (NASA winglets, supercritical and truss-braced wings, wind turbines, aircraft emissions rules and flight on Mars), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a safe home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Aerodynamics decides how much fuel an airplane burns and how much electricity a wind turbine makes. Every bit of drag removed from a wing is fuel not burned and carbon not emitted, and every improvement in a blade’s lift-to-drag ratio is more clean power from the same wind.',
                 'The same equations fly helicopters on Mars and bring spacecraft safely through Earth’s atmosphere. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values.']
PREREQS = ['Calculus III: partial derivatives, gradient, divergence, curl and line integrals.', 'Differential Equations: first- and second-order ODEs.',
           'Dynamics and Physics I: Newton’s laws, momentum and energy; Physics II helps with fields.', 'Intro to Aerospace Engineering gives the vocabulary of lift, drag and the atmosphere.']
STUDY = ['Start every problem by naming the flow regime: incompressible or compressible (Mach number), inviscid or viscous (Reynolds number).', 'Draw a control volume or a streamline before writing an equation, and say which conservation law you are using.',
         'Non-dimensionalize: work in coefficients (C_L, C_D, C_p) and similarity parameters (Re, M), then return to forces.', 'Check limits: at zero angle of attack a symmetric airfoil has zero lift; as aspect ratio grows, induced drag falls.',
         'Keep SI units: Pa, kg/m³, m/s, N; convert knots and feet at the start.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for NASA FoilSim and the free PhET fluid simulations (they run in a browser).', 'Printer paper, tape, paper clips, scissors and a ruler for paper gliders.',
            'Paper coffee filters (cone or basket style) and a tape measure for drag tests.', 'A phone with a stopwatch and slow-motion video.', 'Spreadsheet software for the atmosphere, drag-polar and performance labs.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab can be done in a free simulation or with paper and household items. Throw gliders only in open spaces, never toward people, and keep away from roads and power lines; use a sturdy step stool, not a chair, for drop tests.']
SAFETY_SRC = ('OSHA: Fall protection', 'https://www.osha.gov/fall-protection')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('Sea-level standard air (textbook values)', 'p = 101,325 Pa, T = 288.15 K, ρ = 1.225 kg/m³, μ = 1.789 × 10⁻⁵ kg/(m·s), a = 340.3 m/s'),
             ('Gas constant for air', 'R = 287 J/(kg·K); γ = 1.4'), ('1 knot', '0.514444 m/s'), ('1 foot', '0.3048 m'), ('1 mile per hour', '0.44704 m/s'), ('Gravity on Mars (textbook value)', 'g = 3.71 m/s²')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, NASA pages and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT lecture notes and problem sets.'), (_MITU[0], _MITU[1], 'Free MIT fluids and thermodynamics notes.'), (_BG[0], _BG[1], 'Hundreds of free NASA pages on lift, drag and compressible flow.'),
          (_FS[0], _FS[1], 'Change airfoil shape, speed and altitude and see lift and drag.'), ('OpenStax University Physics Volume 1, 14.6 Bernoulli’s equation', _O + '14-6-bernoullis-equation', 'Free textbook section.'),
          ('PhET: Fluid Pressure and Flow', _PH + 'fluid-pressure-and-flow', 'Pressure, flow and Bernoulli.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Fluid Properties and the Standard Atmosphere', 'weeks': 'Week 1',
 'summary': 'Air as a continuum, pressure, density, temperature and viscosity, the ideal-gas law, the speed of sound, hydrostatics in the atmosphere, the standard atmosphere and its layers, and why aerodynamic forces depend on density.',
 'objectives': ['Use the ideal-gas law to relate p, ρ and T.', 'Compute the speed of sound and the Mach number.', 'Use the standard atmosphere model to find properties at altitude.', 'Explain how density changes lift and drag with altitude.'],
 'concepts': ['Air behaves as a continuum when the flow scale is much larger than the distance between molecules. Its state is set by pressure p, density ρ and temperature T, linked by the ideal-gas law p = ρRT with R = 287 J/(kg·K).',
              'Viscosity μ measures internal friction; it matters near surfaces (Unit 8). Kinematic viscosity is ν = μ/ρ.',
              'Speed of sound a = √(γRT) depends only on temperature for a given gas; Mach number M = V/a.',
              'Hydrostatics: dp/dh = −ρg. Pressure falls with altitude because there is less air above. In the standard troposphere (0–11 km) temperature falls linearly with a lapse rate of about 6.5 K/km; in the lower stratosphere it is nearly constant.',
              'Aerodynamic forces scale with density, so an aircraft at altitude must fly faster, or at a higher lift coefficient, to make the same lift.'],
 'eqs': [('p=\\rho RT', 'Ideal-gas law'), ('a=\\sqrt{\\gamma RT},\\ \\ M=\\frac{V}{a}', 'Speed of sound and Mach number'), ('\\frac{dp}{dh}=-\\rho g', 'Hydrostatic equation'), ('T=T_0-\\lambda h', 'Troposphere temperature (lapse rate λ)')],
 'worked': [
  {'q': 'Find the density of air at sea level with p = 101,325 Pa and T = 288.15 K.', 'steps': ['ρ = p/(RT) = 101,325/(287 × 288.15).'], 'a': 'ρ = 1.225 kg/m³.'},
  {'q': 'Use NASA Glenn’s metric atmosphere model to find T, p and ρ at 11,000 m.', 'steps': ['T = 15.04 − 0.00649 × 11,000 = −56.35 °C.', 'p = 101.29 × [(T + 273.1)/288.08]^5.256 = 22.71 kPa.', 'ρ = p/[0.2869 × (T + 273.1)].'], 'a': 'T = −56.35 °C, p = 22.71 kPa, ρ = 0.3652 kg/m³, about 29.8% of sea-level density.'},
  {'q': 'Find the speed of sound at sea level (288.15 K) and at 11 km (216.8 K), and the Mach number of a jet flying 250 m/s at 11 km.', 'steps': ['a₀ = √(1.4 × 287 × 288.15).', 'a = √(1.4 × 287 × 216.8).', 'M = 250/a.'], 'a': 'a₀ = 340.3 m/s, a = 295.1 m/s, M = 0.847.'}],
 'practice': [('Find ρ for p = 80 kPa and T = 270 K.', 'ρ = 80,000/(287 × 270) = 1.032 kg/m³.'), ('Convert 450 knots to m/s.', '450 × 0.514444 = 231.5 m/s.'),
              ('Find ν at sea level.', 'ν = 1.789 × 10⁻⁵/1.225 = 1.460 × 10⁻⁵ m²/s.'), ('What is the temperature at 5,000 m in the NASA model?', '15.04 − 32.45 = −17.41 °C.')],
 'misc': [('Air pressure falls because air gets colder.', 'It falls because there is less air above; temperature affects how fast.'), ('The speed of sound depends on pressure.', 'For an ideal gas it depends only on temperature.'),
          ('Density is the same at all altitudes for low-speed flow.', 'Low-speed flow is incompressible locally, but density still changes with altitude.')],
 'quiz': [{'q': 'The ideal-gas law is…', 'opts': ['p = ρRT', 'p = ρgh', 'p = ½ρV²', 'p = RT/ρ'], 'ok': 0, 'why': 'Equation of state.'},
          {'q': 'The speed of sound depends on…', 'opts': ['pressure', 'temperature', 'density only', 'velocity'], 'ok': 1, 'why': 'a = √(γRT).'},
          {'q': 'In the lower stratosphere the standard temperature is…', 'opts': ['rising fast', 'nearly constant', 'falling fast', 'zero'], 'ok': 1, 'why': 'NASA model: −56.46 °C from 11 to 25 km.'},
          {'q': 'At half the density, the same lift at the same C_L needs a speed higher by…', 'opts': ['2×', '√2×', '4×', '½×'], 'ok': 1, 'why': 'L ∝ ρV².'}],
 'cards': [('Ideal gas', 'p = ρRT.'), ('Speed of sound', 'a = √(γRT).'), ('Mach number', 'M = V/a.'), ('Hydrostatics', 'dp/dh = −ρg.'), ('Lapse rate', 'About 6.5 K/km in the troposphere.'), ('Kinematic viscosity', 'ν = μ/ρ.')],
 'planet': {'text': ['NASA Glenn’s Beginner’s Guide explains that the atmosphere is an extremely thin sheet of air, that pressure falls with altitude because there is always less air above, and that aerodynamic forces depend directly on air density. Its standard atmosphere model, used in the FoilSim simulator, has a troposphere from the surface to 11,000 m where temperature falls linearly, a lower stratosphere from 11,000 to 25,000 m at a constant −56.46 °C, and an upper stratosphere above.',
                     'Airliners cruise near the top of the troposphere, where the density is only about 30% of sea level, so drag at a given speed is much lower; that is a big reason cruise altitude matters for fuel burn. The same model, with Mars values, explains why NASA’s Ingenuity helicopter had to spin its rotors so fast: NASA notes the Martian atmosphere is less than 1 percent as dense as Earth’s.'],
            'site': [('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_ATM, _ING]},
 'res': [(_ATM[0], _ATM[1], 'Standard atmosphere curve fits.'), (_BG[0], _BG[1], 'Free NASA guide.'), (_MITU[0], _MITU[1], 'Fluid properties and thermodynamics notes.'),
         ('PhET: Under Pressure', _PH + 'under-pressure', 'Hydrostatic pressure interactively.')]})
UNITS.append(
{'id': 'u2', 'title': 'Fluid Statics, Bernoulli’s Equation and Airspeed Measurement', 'weeks': 'Week 2',
 'summary': 'Static, dynamic and total pressure, Bernoulli’s equation and its assumptions, the venturi, pitot-static tubes and airspeed (indicated, equivalent and true), manometers, and the pressure coefficient.',
 'objectives': ['State when Bernoulli’s equation applies.', 'Compute dynamic pressure and airspeed from a pitot-static reading.', 'Analyze a venturi with continuity and Bernoulli.', 'Use the pressure coefficient C_p.'],
 'concepts': ['Along a streamline in steady, inviscid, incompressible flow, p + ½ρV² = p₀ is constant: static pressure plus dynamic pressure equals total (stagnation) pressure.',
              'Dynamic pressure q = ½ρV² sets the scale of every aerodynamic force; forces are written as coefficient × q × area.',
              'A pitot-static tube measures p₀ − p, so V = √(2(p₀ − p)/ρ). Airspeed indicators assume sea-level density and read equivalent airspeed; true airspeed is higher at altitude by √(ρ₀/ρ).',
              'Continuity A₁V₁ = A₂V₂ plus Bernoulli explains the venturi: where the area shrinks the speed rises and the pressure drops.',
              'Pressure coefficient C_p = (p − p∞)/q∞ = 1 − (V/V∞)² for incompressible flow; C_p = 1 at a stagnation point.'],
 'eqs': [('p+\\tfrac12\\rho V^2=p_0', 'Bernoulli’s equation'), ('q=\\tfrac12\\rho V^2', 'Dynamic pressure'), ('V=\\sqrt{\\frac{2(p_0-p)}{\\rho}}', 'Pitot-static airspeed'), ('C_p=\\frac{p-p_\\infty}{q_\\infty}=1-\\left(\\frac{V}{V_\\infty}\\right)^2', 'Pressure coefficient')],
 'worked': [
  {'q': 'A pitot-static tube at sea level reads p₀ − p = 1500 Pa. Find the airspeed.', 'steps': ['V = √(2 × 1500/1.225).'], 'a': 'V = 49.5 m/s.'},
  {'q': 'A venturi in a wind tunnel halves the area. Upstream V₁ = 10 m/s at sea level. Find V₂ and the pressure drop.', 'steps': ['V₂ = 2 × 10 = 20 m/s (continuity).', 'Δp = ½ × 1.225 × (20² − 10²).'], 'a': 'V₂ = 20 m/s, Δp = 183.8 Pa.'},
  {'q': 'An airliner flies with an equivalent airspeed of 140 m/s at 11 km (ρ = 0.3652 kg/m³). Find the dynamic pressure and the true airspeed.', 'steps': ['q = ½ × 1.225 × 140² (equivalent airspeed uses sea-level density).', 'V_true = 140 × √(1.225/0.3652).'], 'a': 'q = 12.0 kPa, V_true = 256.4 m/s.'}],
 'practice': [('Find q at 100 m/s at sea level.', '6125 Pa.'), ('Find C_p where the local speed is 1.5 V∞.', '1 − 2.25 = −1.25.'),
              ('A water manometer shows 50 mm. Find the pressure difference (ρ_water = 1000 kg/m³).', '1000 × 9.81 × 0.05 = 490.5 Pa.'), ('What C_p does a stagnation point have?', '1.')],
 'misc': [('Bernoulli applies everywhere in any flow.', 'It needs steady, inviscid, incompressible flow along a streamline (or irrotational flow).'), ('Lift happens because air takes equal time over the top and bottom.', 'There is no equal-transit rule; the top flow is faster still, and circulation explains lift (Unit 5).'),
          ('Indicated airspeed equals true airspeed.', 'At altitude true airspeed is much higher.')],
 'quiz': [{'q': 'Total pressure equals…', 'opts': ['p − q', 'p + q', 'q only', 'ρRT'], 'ok': 1, 'why': 'Static plus dynamic.'},
          {'q': 'A pitot tube measures…', 'opts': ['static pressure only', 'total pressure', 'temperature', 'density'], 'ok': 1, 'why': 'It faces the flow.'},
          {'q': 'Doubling airspeed multiplies q by…', 'opts': ['2', '4', '√2', '8'], 'ok': 1, 'why': 'q ∝ V².'},
          {'q': 'C_p at a stagnation point is…', 'opts': ['0', '1', '−1', '2'], 'ok': 1, 'why': 'V = 0.'}],
 'cards': [('Bernoulli', 'p + ½ρV² = p₀.'), ('Dynamic pressure', 'q = ½ρV².'), ('Pitot-static', 'V = √(2Δp/ρ).'), ('Venturi', 'Smaller area, higher speed, lower pressure.'), ('C_p', '(p − p∞)/q∞.'), ('True airspeed', 'V_e √(ρ₀/ρ).')],
 'planet': {'text': ['Dynamic pressure is why flying on Mars is so hard. NASA reports that Ingenuity flew in an atmosphere less than 1 percent as dense as Earth’s, with rotors just under 1.2 m tip to tip and a mass of 1.8 kg. At 1% of Earth’s density, the same dynamic pressure needs √100 = 10 times the speed.',
                     'NASA says Ingenuity completed 72 flights between April 19, 2021 and January 18, 2024, logging 128.8 minutes in the air, covering 17.0 km and reaching altitudes of up to 24.0 m. Getting there meant understanding q = ½ρV² better than ever, which is also what lets Earth aircraft and wind turbines be designed for thinner air at altitude.'],
            'site': [('Space', 'Space.html'), ('Rotor Hover Power Calculator', 'Rotor_Hover_Power_Calculator.html')],
            'src': [_ING, ('NASA Glenn: Pitot-static tube', _G + 'pitot.html')]},
 'res': [('NASA Glenn: Bernoulli’s equation', _G + 'bern.html', 'Free NASA page.'), ('NASA Glenn: Pitot-static tube', _G + 'pitot.html', 'How airspeed is measured.'),
         ('OpenStax UP1, 14.6 Bernoulli’s equation', _O + '14-6-bernoullis-equation', 'Free textbook section.'), ('PhET: Fluid Pressure and Flow', _PH + 'fluid-pressure-and-flow', 'Interactive.')]})
UNITS.append(
{'id': 'u3', 'title': 'Conservation Laws: Mass, Momentum and Energy; Control Volumes and Momentum Theory', 'weeks': 'Weeks 3–4',
 'summary': 'Lagrangian and Eulerian descriptions, the substantial derivative, integral conservation of mass, momentum and energy for a control volume, differential continuity, Euler’s equation, drag from a wake survey, and actuator-disk momentum theory for propellers and rotors.',
 'objectives': ['Apply integral mass and momentum conservation to a control volume.', 'Derive the continuity and Euler equations in differential form.', 'Find drag from a wake velocity profile.', 'Use momentum theory to estimate rotor thrust and hover power.'],
 'concepts': ['Mass: ∂/∂t∫ρ dV + ∮ρV·dA = 0. For steady flow, mass in = mass out: ṁ = ρAV is constant through a stream tube.',
              'Momentum: the net force on a control volume (pressure, body and surface forces) equals the net momentum flux out plus the rate of change inside: ΣF = ∮(ρV·dA)V for steady flow.',
              'Differential forms: ∂ρ/∂t + ∇·(ρV) = 0; for incompressible flow ∇·V = 0. Euler’s equation ρ DV/Dt = −∇p + ρg is Newton’s law for an inviscid fluid particle; integrating it along a streamline gives Bernoulli.',
              'Drag from a wake: a body slows the air behind it; the momentum deficit in the wake equals the drag, D′ = ρ∫u(V∞ − u) dy per unit span.',
              'Actuator-disk (momentum) theory: a rotor of area A producing thrust T induces velocity v = √(T/(2ρA)) at the disk; the ideal hover power is P = T^(3/2)/√(2ρA). Real rotors need more; the ratio is the figure of merit.'],
 'eqs': [('\\dot m=\\rho AV=\\text{const}', 'Steady mass conservation'), ('\\sum\\mathbf F=\\oint(\\rho\\mathbf V\\cdot d\\mathbf A)\\mathbf V', 'Steady momentum (control volume)'), ('\\nabla\\cdot\\mathbf V=0', 'Incompressible continuity'), ('P_{ideal}=\\frac{T^{3/2}}{\\sqrt{2\\rho A}}', 'Ideal hover power (momentum theory)')],
 'worked': [
  {'q': 'Air at 1.225 kg/m³ flows at 20 m/s through a 0.5 m² duct. Find the mass flow and the speed where the duct narrows to 0.2 m².', 'steps': ['ṁ = 1.225 × 0.5 × 20 = 12.25 kg/s.', 'V₂ = 20 × 0.5/0.2.'], 'a': 'ṁ = 12.25 kg/s, V₂ = 50 m/s.'},
  {'q': 'A helicopter of 1000 kg hovers at sea level with a 10 m diameter rotor. Find the induced velocity and the ideal hover power.', 'steps': ['T = 9810 N; A = π × 5² = 78.54 m².', 'v = √(9810/(2 × 1.225 × 78.54)) = 7.14 m/s.', 'P = Tv.'], 'a': 'v = 7.14 m/s, P = 70.0 kW (ideal).'},
  {'q': 'A wake survey behind a 2D body (sea level, V∞ = 30 m/s) finds a deficit equivalent to ∫u(V∞ − u)dy = 6 m³/s². Find the drag per unit span.', 'steps': ['D′ = ρ∫u(V∞ − u) dy = 1.225 × 6.'], 'a': 'D′ = 7.35 N/m.'}],
 'practice': [('Is V = (x, −y) incompressible?', 'Yes: ∂u/∂x + ∂v/∂y = 1 − 1 = 0.'), ('A rotor’s thrust doubles. By how much does ideal hover power grow?', '2^1.5 = 2.83 times.'),
              ('Doubling rotor area at fixed thrust changes ideal hover power by…', '1/√2 = 0.707 times.'), ('A jet of water (ρ = 1000) with A = 0.01 m² and V = 10 m/s hits a wall head-on. Find the force.', 'F = ρAV² = 1000 N.')],
 'misc': [('Momentum conservation ignores pressure.', 'Pressure forces on the control-volume surface must be included.'), ('A bigger rotor needs more power to hover.', 'At the same thrust, a bigger disk needs less induced power.'),
          ('Steady flow means the fluid is not accelerating.', 'Particles can accelerate (convective acceleration) even when the field does not change in time.')],
 'quiz': [{'q': 'For incompressible flow, continuity becomes…', 'opts': ['∇·V = 0', '∇×V = 0', 'ρ = 0', 'p = const'], 'ok': 0, 'why': 'Density is constant.'},
          {'q': 'Drag from a wake survey comes from…', 'opts': ['the energy in the wake', 'the momentum deficit', 'temperature', 'lift'], 'ok': 1, 'why': 'Momentum balance.'},
          {'q': 'Ideal hover power scales with thrust as…', 'opts': ['T', 'T^1.5', 'T²', '√T'], 'ok': 1, 'why': 'P = T^(3/2)/√(2ρA).'},
          {'q': 'Euler’s equation is Newton’s law for…', 'opts': ['a viscous fluid', 'an inviscid fluid particle', 'a rigid body', 'a shock'], 'ok': 1, 'why': 'Pressure and gravity only.'}],
 'cards': [('Mass flow', 'ṁ = ρAV.'), ('Continuity', '∇·V = 0 (incompressible).'), ('Euler equation', 'ρDV/Dt = −∇p + ρg.'), ('Wake drag', 'D′ = ρ∫u(V∞ − u)dy.'), ('Induced velocity', 'v = √(T/2ρA).'), ('Hover power', 'T^(3/2)/√(2ρA).')],
 'planet': {'text': ['Momentum theory shows why Ingenuity was a feat. NASA lists its mass as 1.8 kg, its rotors as about 1.2 m tip to tip, and its average flight power as about 350 W, from a solar panel charging lithium-ion batteries for one 90-second flight per Martian day. With Mars gravity (3.71 m/s², a textbook value), the thrust needed is 6.68 N.',
                     'Taking a sample Mars density of 0.0115 kg/m³ (within NASA’s “less than 1 percent” of Earth’s) and one 1.2 m disk, momentum theory gives an ideal hover power of about 107 W; the 350 W NASA reports also covers real rotor losses (profile drag, tip losses, non-uniform inflow), climbing and onboard systems. The same equation sizes rotors for electric air taxis and drones on Earth, and it is behind this site’s rotor hover power calculator.'],
            'site': [('Rotor Hover Power Calculator', 'Rotor_Hover_Power_Calculator.html'), ('Dynamics', 'Dynamics.html')],
            'src': [_ING, (_MITU[0], _MITU[1])]},
 'res': [('NASA Glenn: Conservation of mass', _G + 'mass.html', 'Free NASA page.'), ('OpenStax UP1, 14.5 Fluid dynamics', _O + '14-5-fluid-dynamics', 'Flow rate and continuity.'),
         (_MITU[0], _MITU[1], 'Control volumes and momentum theory.'), (_MIT[0], _MIT[1], 'Conservation laws in differential form.')]})
UNITS.append(
{'id': 'u4', 'title': 'Potential Flow and the Kutta–Joukowski Theorem', 'weeks': 'Weeks 5–6',
 'summary': 'Vorticity and circulation, irrotational flow, the velocity potential and stream function, Laplace’s equation and superposition, uniform flow, sources, sinks, doublets and vortices, flow over a cylinder with and without circulation, d’Alembert’s paradox, and the Kutta–Joukowski lift theorem.',
 'objectives': ['Relate vorticity, circulation and irrotational flow.', 'Build flows by superposing elementary solutions of Laplace’s equation.', 'Find the pressure distribution on a cylinder.', 'Apply L′ = ρ∞V∞Γ.'],
 'concepts': ['Vorticity ω = ∇ × V is twice the local rotation rate. Circulation Γ = −∮V·ds around a closed curve equals the vorticity flux through it (Stokes’ theorem; aerodynamics uses the clockwise-positive sign).',
              'If ω = 0 the flow is irrotational and V = ∇φ. With ∇·V = 0, φ satisfies Laplace’s equation ∇²φ = 0, which is linear, so solutions add (superposition). In 2D the stream function ψ has u = ∂ψ/∂y, v = −∂ψ/∂x, and lines of constant ψ are streamlines.',
              'Elementary flows: uniform flow φ = V∞x; source of strength Λ, V_r = Λ/(2πr); doublet, the limit of a source–sink pair; point vortex, V_θ = −Γ/(2πr).',
              'Uniform flow plus a doublet gives flow over a cylinder of radius R: surface speed V_θ = −2V∞ sin θ, so C_p = 1 − 4 sin²θ. The pressure is symmetric, so there is no drag (d’Alembert’s paradox) and no lift.',
              'Adding a vortex makes the flow asymmetric and produces lift per unit span L′ = ρ∞V∞Γ, the Kutta–Joukowski theorem. It holds for any 2D body: lift is always tied to circulation.'],
 'eqs': [('\\omega=\\nabla\\times\\mathbf V,\\ \\ \\Gamma=-\\oint\\mathbf V\\cdot d\\mathbf s', 'Vorticity and circulation'), ('\\nabla^2\\phi=0', 'Laplace’s equation'), ('C_p=1-4\\sin^2\\theta', 'Surface pressure on a non-lifting cylinder'), ('L\'=\\rho_\\infty V_\\infty\\Gamma', 'Kutta–Joukowski theorem')],
 'worked': [
  {'q': 'Find the maximum surface speed and the minimum C_p on a non-lifting cylinder in a 20 m/s stream.', 'steps': ['|V_θ| = 2V∞|sin θ| is largest at θ = 90°.', 'C_p = 1 − 4 × 1.'], 'a': 'V_max = 40 m/s; C_p,min = −3.'},
  {'q': 'A spinning cylinder at sea level in a 50 m/s stream has circulation Γ = 20 m²/s. Find the lift per metre of span.', 'steps': ['L′ = 1.225 × 50 × 20.'], 'a': 'L′ = 1225 N/m.'},
  {'q': 'Find the speed induced by a point vortex of Γ = 20 m²/s at a distance of 1 m.', 'steps': ['V_θ = Γ/(2πr) = 20/(2π).'], 'a': '3.183 m/s.'}],
 'practice': [('Where on a non-lifting cylinder is C_p = 0?', 'sin²θ = 0.25, so θ = 30°, 150°, 210°, 330°.'), ('Is φ = x² − y² a valid potential?', 'Yes: ∇²φ = 2 − 2 = 0.'),
              ('What lift does a 2 m span spinning cylinder of the worked example make?', '2450 N.'), ('What drag does potential flow predict on a cylinder?', 'Zero, d’Alembert’s paradox; real drag comes from viscosity.')],
 'misc': [('Potential flow is useless because it predicts no drag.', 'It predicts lift and pressure well wherever the boundary layer stays attached.'), ('Circulation means air is going around the wing in circles.', 'It is a net value of the line integral; particles do not orbit the wing.'),
          ('Superposition works for any flow equation.', 'It works because Laplace’s equation is linear.')],
 'quiz': [{'q': 'Irrotational flow means…', 'opts': ['ω = 0', 'Γ = 0 everywhere', '∇·V = 0', 'no viscosity'], 'ok': 0, 'why': 'Zero vorticity.'},
          {'q': 'Lift per unit span equals…', 'opts': ['ρV²Γ', 'ρVΓ', '½ρV²', 'Γ/ρV'], 'ok': 1, 'why': 'Kutta–Joukowski.'},
          {'q': 'Minimum C_p on a non-lifting cylinder is…', 'opts': ['−1', '−3', '0', '−4'], 'ok': 1, 'why': '1 − 4.'},
          {'q': 'Uniform flow plus a doublet models…', 'opts': ['an airfoil', 'a cylinder', 'a sphere', 'a vortex'], 'ok': 1, 'why': 'Non-lifting cylinder.'}],
 'cards': [('Vorticity', 'ω = ∇ × V.'), ('Circulation', 'Γ = −∮V·ds.'), ('Laplace', '∇²φ = 0.'), ('Point vortex', 'V_θ = Γ/2πr.'), ('Cylinder C_p', '1 − 4 sin²θ.'), ('Kutta–Joukowski', 'L′ = ρVΓ.')],
 'planet': {'text': ['The U.S. Department of Energy explains that wind turbine blades work much like an airplane wing or helicopter rotor blade: air pressure on one side of the blade drops, and the pressure difference across the blade creates both lift and drag. Because the lift is stronger than the drag, the rotor spins, turning a generator.',
                     'DOE notes that land-based turbines range from 100 kilowatts to several megawatts and that offshore turbines are typically larger, taller than the Statue of Liberty. Blade designers use the circulation and lift ideas from this unit, with blade-element momentum theory built on Unit 3, to shape each section of a blade so it extracts as much power from the wind as possible.'],
            'site': [('Solutions', 'Solutions.html'), ('Physics II', 'Physics_II.html')],
            'src': [_WIND]},
 'res': [(_MIT[0], _MIT[1], 'Potential flow lectures.'), (_FS[0], _FS[1], 'See circulation and lift.'), ('NASA Glenn: Lift from flow turning', _G + 'foil2.html', 'Why the flow turns.'),
         ('NASA Glenn: Incorrect lift theory (equal transit)', _G + 'foil3.html', 'Common misconceptions.')]})
UNITS.append(
{'id': 'u5', 'title': 'Airfoils, Lift, Drag and Moment Coefficients', 'weeks': 'Week 7',
 'summary': 'Airfoil geometry and NACA designations, angle of attack, the lift, drag and moment coefficients, the lift curve and stall, center of pressure and aerodynamic center, the Kutta condition, and how pressure distributions make lift.',
 'objectives': ['Describe airfoil geometry: chord, camber and thickness.', 'Compute forces from L = qSC_L and D = qSC_D.', 'Read a lift curve: slope, zero-lift angle and stall.', 'Find the stall speed and the required lift coefficient.'],
 'concepts': ['An airfoil has a chord c from leading to trailing edge, a mean camber line and a thickness distribution. In a NACA 4-digit name such as 2412, the first digit is max camber (2% of chord), the second is its location (40% of chord) and the last two are thickness (12%).',
              'Forces are made dimensionless: C_L = L/(qS), C_D = D/(qS), C_M = M/(qSc). For a 2D section use lowercase c_l, c_d, c_m per unit span.',
              'The lift curve c_l(α) is nearly a straight line up to stall, where the boundary layer separates from the upper surface and lift falls. Cambered airfoils make lift at zero angle of attack, so their zero-lift angle α_L=0 is negative.',
              'The Kutta condition says the flow leaves the sharp trailing edge smoothly; it fixes the circulation and hence the lift.',
              'The center of pressure moves with α; the aerodynamic center (near quarter chord at low speed) is the point where the moment does not change with α, which makes it useful for stability.'],
 'eqs': [('L=\\tfrac12\\rho V^2SC_L', 'Lift equation'), ('D=\\tfrac12\\rho V^2SC_D', 'Drag equation'), ('V_{stall}=\\sqrt{\\frac{2W}{\\rho SC_{L,max}}}', 'Stall speed'), ('C_M=\\frac{M}{qSc}', 'Moment coefficient')],
 'worked': [
  {'q': 'A wing of S = 16 m² flies at 60 m/s at sea level with C_L = 0.5. Find the lift.', 'steps': ['q = ½ × 1.225 × 60² = 2205 Pa.', 'L = 2205 × 16 × 0.5.'], 'a': 'L = 17,640 N.'},
  {'q': 'A 1000 kg airplane with S = 16 m² flies level at 50 m/s at sea level. Find the C_L needed.', 'steps': ['W = 9810 N; q = 1531.25 Pa.', 'C_L = 9810/(1531.25 × 16).'], 'a': 'C_L = 0.400.'},
  {'q': 'The same airplane has C_L,max = 1.6. Find the sea-level stall speed.', 'steps': ['V = √(2 × 9810/(1.225 × 16 × 1.6)).'], 'a': 'V_stall = 25.0 m/s (about 48.6 knots).'}],
 'practice': [('What thickness does a NACA 0012 have?', '12% of chord, symmetric (no camber).'), ('Lift at 1.5× the speed, same C_L?', '2.25 times.'),
              ('Stall speed of the worked example at 11 km (ρ = 0.3652)?', '25.0 × √(1.225/0.3652) = 45.8 m/s.'), ('What happens to lift past stall?', 'It drops as the flow separates; drag rises sharply.')],
 'misc': [('Higher angle of attack always gives more lift.', 'Only up to stall.'), ('Symmetric airfoils cannot make lift.', 'They make lift at positive angle of attack.'),
          ('The center of pressure is a fixed point.', 'It moves with α; the aerodynamic center does not.')],
 'quiz': [{'q': 'C_L is defined as…', 'opts': ['L/q', 'L/(qS)', 'qS/L', 'L/S'], 'ok': 1, 'why': 'Lift over q times area.'},
          {'q': 'NACA 2412 has max camber of…', 'opts': ['2%', '4%', '12%', '24%'], 'ok': 0, 'why': 'First digit.'},
          {'q': 'Stall is caused by…', 'opts': ['shock waves', 'flow separation', 'low density', 'high Re'], 'ok': 1, 'why': 'Boundary layer separates.'},
          {'q': 'The Kutta condition fixes…', 'opts': ['drag', 'circulation', 'Mach number', 'thickness'], 'ok': 1, 'why': 'Smooth flow off the trailing edge.'}],
 'cards': [('Lift', 'L = qSC_L.'), ('Drag', 'D = qSC_D.'), ('Stall speed', '√(2W/ρSC_Lmax).'), ('NACA 4-digit', 'Camber, location, thickness.'), ('Kutta condition', 'Smooth trailing-edge flow.'), ('Aerodynamic center', 'Moment independent of α.')],
 'planet': {'text': ['NASA tells how its engineer Richard Whitcomb created the supercritical airfoil: nearly flat on top, rounded on the bottom, thicker, with a blunt leading edge. Near the speed of sound, around 660 mph at cruise altitude, a conventional wing forms a standing shock wave that adds drag; the new shape minimized that shock.',
                     'NASA reports that supercritical wings increased efficiency by as much as 15%, also work better at slower speeds, and allow a lighter wing. They became the industry standard, and NASA says they save billions of dollars in fuel each year. Shaping a section’s pressure distribution, as in this unit, is how fuel and emissions are cut.'],
            'site': [('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html'), ('Solutions', 'Solutions.html')],
            'src': [_SC]},
 'res': [('NASA Glenn: The lift equation', _G + 'lifteq.html', 'Free NASA page.'), ('NASA Glenn: The drag equation', _G + 'drageq.html', 'Free NASA page.'), (_FS[0], _FS[1], 'Explore lift curves.'), (_MIT[0], _MIT[1], 'Airfoil lectures.')]})
UNITS.append(
{'id': 'u6', 'title': 'Thin Airfoil Theory', 'weeks': 'Week 8',
 'summary': 'Vortex sheets, modeling the camber line with a vortex sheet, the Kutta condition, the Fourier-series solution, the lift slope of 2π per radian, the zero-lift angle of cambered airfoils, the quarter-chord aerodynamic center, and panel methods.',
 'objectives': ['Model an airfoil by a vortex sheet on its camber line.', 'Derive c_l = 2πα for a symmetric thin airfoil.', 'Find the lift coefficient of a cambered airfoil from α and α_L=0.', 'Explain why the aerodynamic center is at quarter chord.'],
 'concepts': ['A vortex sheet of strength γ(s) per unit length creates a jump in tangential velocity across it. Placing one on the camber line and requiring the camber line to be a streamline gives an integral equation for γ.',
              'With the Kutta condition γ(TE) = 0 and a Fourier series in θ (x = c(1 − cos θ)/2), the solution gives c_l = 2π(α − α_L=0): the lift slope is 2π per radian (about 0.11 per degree) for every thin airfoil.',
              'For a symmetric airfoil α_L=0 = 0, c_m,c/4 = 0 and c_m,LE = −c_l/4, so the center of pressure is at quarter chord. Camber shifts α_L=0 negative and adds a constant nose-down c_m,c/4, but the aerodynamic center stays at quarter chord.',
              'Real airfoils of moderate thickness have lift slopes close to 2π until the boundary layer begins to separate; thin airfoil theory does not predict stall or drag.',
              'Panel methods cover the real surface with many source and vortex panels and solve for their strengths numerically; they are how designers compute pressure on any shape, from blades to wings.'],
 'eqs': [('c_l=2\\pi(\\alpha-\\alpha_{L=0})', 'Thin airfoil lift'), ('c_{m,c/4}=0\\ \\text{(symmetric)}', 'Quarter-chord moment'), ('c_{m,LE}=-\\frac{c_l}{4}', 'Leading-edge moment (symmetric)'), ('x=\\tfrac c2(1-\\cos\\theta)', 'Glauert transformation')],
 'worked': [
  {'q': 'Find c_l for a symmetric thin airfoil at α = 5°.', 'steps': ['α = 0.08727 rad.', 'c_l = 2π × 0.08727.'], 'a': 'c_l = 0.548.'},
  {'q': 'A cambered airfoil has α_L=0 = −2° (sample value). Find c_l at α = 4°.', 'steps': ['α − α_L=0 = 6° = 0.10472 rad.', 'c_l = 2π × 0.10472.'], 'a': 'c_l = 0.658.'},
  {'q': 'For the symmetric airfoil at α = 5°, find c_m about the leading edge and the center of pressure.', 'steps': ['c_m,LE = −c_l/4 = −0.548/4.', 'x_cp = −c_m,LE c/c_l = c/4.'], 'a': 'c_m,LE = −0.137; x_cp = 0.25c.'}],
 'practice': [('What angle gives c_l = 0.5 on a symmetric thin airfoil?', '0.5/(2π) = 0.0796 rad = 4.56°.'), ('Lift slope per degree?', '2π × π/180 = 0.1097 per degree.'),
              ('Does thin airfoil theory predict stall?', 'No; it is inviscid and linear.'), ('Where is the aerodynamic center of a cambered thin airfoil?', 'At quarter chord.')],
 'misc': [('Camber changes the lift slope.', 'In thin airfoil theory it shifts the curve; the slope stays 2π.'), ('The center of pressure is always at quarter chord.', 'Only for a symmetric airfoil; cambered airfoils have a moving c.p.'),
          ('2π is per degree.', 'It is per radian.')],
 'quiz': [{'q': 'Thin airfoil lift slope is…', 'opts': ['2π per degree', '2π per radian', 'π per radian', '4π'], 'ok': 1, 'why': 'c_l = 2πα.'},
          {'q': 'Camber makes α_L=0…', 'opts': ['positive', 'negative', 'zero', 'undefined'], 'ok': 1, 'why': 'Lift at zero angle.'},
          {'q': 'The aerodynamic center of a thin airfoil is at…', 'opts': ['leading edge', 'quarter chord', 'half chord', 'trailing edge'], 'ok': 1, 'why': 'Theory result.'},
          {'q': 'Thin airfoil theory models the airfoil with…', 'opts': ['sources only', 'a vortex sheet', 'shocks', 'boundary layers'], 'ok': 1, 'why': 'On the camber line.'}],
 'cards': [('Vortex sheet', 'Jump in tangential velocity.'), ('Lift', 'c_l = 2π(α − α_L0).'), ('Symmetric moment', 'c_m,c/4 = 0.'), ('Leading-edge moment', '−c_l/4.'), ('Glauert', 'x = c(1 − cos θ)/2.'), ('Panel method', 'Numerical source/vortex panels.')],
 'planet': {'text': ['DOE explains that a turbine blade, like an airplane wing, makes lift from a pressure difference, and that lift stronger than drag is what turns the rotor. Each blade section sees a local angle of attack set by the wind speed and its own rotational speed, so blades are twisted so that every section works near its best lift-to-drag angle.',
                     'Thin airfoil theory gives the first estimate of that section lift: c_l = 2π(α − α_L=0). Panel methods and wind-tunnel data refine it. DOE notes that land-based turbines run from 100 kilowatts to several megawatts, so a few percent better section lift-to-drag ratio means a lot of extra clean energy over a turbine’s life.'],
            'site': [('Solutions', 'Solutions.html'), ('Linear Algebra', 'Linear_Algebra.html')],
            'src': [_WIND]},
 'res': [(_MIT[0], _MIT[1], 'Thin airfoil theory lectures.'), (_FS[0], _FS[1], 'Compare theory with the simulator.'), ('NASA Glenn: Lift from flow turning', _G + 'foil2.html', 'Free NASA page.'), (_MITU[0], _MITU[1], 'Unified Engineering fluids.')]})
UNITS.append(
{'id': 'u7', 'title': 'Finite Wings and Induced Drag', 'weeks': 'Weeks 9–10',
 'summary': 'Wingtip vortices and downwash, the induced angle of attack, Prandtl’s lifting-line theory, elliptic lift distribution, span efficiency, induced drag C_Di = C_L²/(πeAR), the finite-wing lift slope, aspect ratio, winglets and truss-braced wings.',
 'objectives': ['Explain how tip vortices create downwash and induced drag.', 'Compute induced drag with the span efficiency factor.', 'Find the finite-wing lift slope.', 'Explain how aspect ratio and winglets reduce induced drag.'],
 'concepts': ['On a finite wing, high-pressure air below curls around the tips to the low-pressure top, forming trailing vortices. They induce a downward velocity (downwash) at the wing, tilting the local flow by the induced angle α_i.',
              'Tilting the lift vector back by α_i creates a drag component: induced drag, the price of making lift with a finite span. It is largest at low speed and high C_L.',
              'Prandtl’s lifting-line theory models the wing as a bound vortex with a sheet of trailing vortices. An elliptic lift distribution gives uniform downwash, α_i = C_L/(πAR), and the minimum induced drag C_Di = C_L²/(πAR).',
              'Real wings have span efficiency e < 1: C_Di = C_L²/(πeAR). Aspect ratio AR = b²/S is the key lever: doubling AR halves induced drag.',
              'The finite-wing lift slope is lower than 2π: a = a₀/(1 + a₀/(πeAR)). Winglets and long, thin truss-braced wings both cut induced drag by weakening or spreading the tip vortices.'],
 'eqs': [('AR=\\frac{b^2}{S}', 'Aspect ratio'), ('\\alpha_i=\\frac{C_L}{\\pi AR}', 'Induced angle (elliptic)'), ('C_{D_i}=\\frac{C_L^2}{\\pi eAR}', 'Induced drag'), ('a=\\frac{a_0}{1+a_0/(\\pi eAR)}', 'Finite-wing lift slope')],
 'worked': [
  {'q': 'A wing with AR = 8 and e = 0.9 flies at C_L = 0.5. Find C_Di.', 'steps': ['C_Di = 0.25/(π × 0.9 × 8).'], 'a': 'C_Di = 0.01105.'},
  {'q': 'Find the lift slope of that wing if a₀ = 2π per radian.', 'steps': ['a = 2π/(1 + 2π/(π × 0.9 × 8)) = 6.2832/1.2778.'], 'a': 'a = 4.917 per radian (0.0858 per degree).'},
  {'q': 'Find the induced angle of an elliptic wing (AR = 8) at C_L = 0.5.', 'steps': ['α_i = 0.5/(π × 8) rad.'], 'a': 'α_i = 0.01989 rad = 1.14°.'}],
 'practice': [('A wing has b = 30 m and S = 100 m². Find AR.', '900/100 = 9.'), ('Raise AR from 8 to 12 at the same e and C_L. New C_Di?', '0.01105 × 8/12 = 0.00737.'),
              ('When is induced drag largest?', 'At low speed and high C_L, e.g. take-off and climb.'), ('What e does an elliptic wing have?', 'e = 1.')],
 'misc': [('Induced drag comes from skin friction.', 'It is the backward tilt of lift from downwash, an inviscid effect.'), ('A finite wing has the same lift slope as its airfoil.', 'It is lower because of downwash.'),
          ('Winglets work by adding wing area.', 'They mainly weaken tip vortices and their downwash.')],
 'quiz': [{'q': 'Induced drag coefficient is…', 'opts': ['C_L/(πeAR)', 'C_L²/(πeAR)', 'πeAR/C_L²', 'C_L²AR'], 'ok': 1, 'why': 'Lifting-line result.'},
          {'q': 'Doubling aspect ratio changes induced drag by…', 'opts': ['×2', '×½', '×4', 'none'], 'ok': 1, 'why': 'C_Di ∝ 1/AR.'},
          {'q': 'Minimum induced drag comes from a…', 'opts': ['rectangular lift distribution', 'elliptic lift distribution', 'triangular', 'tip-loaded'], 'ok': 1, 'why': 'Uniform downwash.'},
          {'q': 'Aspect ratio is…', 'opts': ['S/b', 'b²/S', 'c/b', 'b/c²'], 'ok': 1, 'why': 'Span squared over area.'}],
 'cards': [('Downwash', 'Induced by trailing vortices.'), ('Aspect ratio', 'b²/S.'), ('Induced drag', 'C_L²/(πeAR).'), ('Induced angle', 'C_L/(πAR).'), ('Span efficiency', 'e ≤ 1.'), ('Finite-wing slope', 'a₀/(1 + a₀/πeAR).')],
 'planet': {'text': ['NASA Armstrong recounts that winglets first flew on a KC-135 on July 24, 1979; over 48 test flights they raised fuel efficiency by 6 to 7 percent and reduced drag by as much as 7 percent. NASA says winglets are now on roughly 10,000 jets, saving more than 10 billion gallons of jet fuel and over 130 million tons of carbon dioxide.',
                     'The next step pushes aspect ratio further. NASA’s 2023 Sustainable Flight Demonstrator award (NASA $425 million over seven years, partners about $725 million) is for a transonic truss-braced wing: extra-long, thin wings braced by struts, which NASA says means less drag and, combined with other advances, up to 30% less fuel use and emissions. That is C_Di = C_L²/(πeAR) at work.'],
            'site': [('Solutions', 'Solutions.html'), ('Statics', 'Statics.html')],
            'src': [_WL, _TTBW]},
 'res': [('NASA Glenn: Induced drag', _G + 'induced.html', 'Free NASA page.'), ('NASA Glenn: Lift to drag ratio', _G + 'ldrat.html', 'Free NASA page.'), (_MIT[0], _MIT[1], 'Lifting-line lectures.'), (_FS[0], _FS[1], 'Simulator.')]})
UNITS.append(
{'id': 'u8', 'title': 'Viscous Flow, Reynolds Number and Boundary Layers', 'weeks': 'Week 11',
 'summary': 'The no-slip condition, the Reynolds number and similarity, the Navier–Stokes equations in words, laminar and turbulent boundary layers, the Blasius flat-plate solution, skin friction, transition, separation and pressure drag, and the drag breakdown of an aircraft.',
 'objectives': ['Compute the Reynolds number and use it for similarity.', 'Find boundary-layer thickness and skin-friction drag on a flat plate.', 'Distinguish laminar and turbulent boundary layers.', 'Explain separation, pressure drag and the total drag breakdown.'],
 'concepts': ['Viscous fluid sticks to a surface (no slip), so a thin boundary layer forms where speed rises from zero to the outer flow. Outside it, the inviscid theory of Units 4–7 works well.',
              'The Reynolds number Re = ρVL/μ compares inertial to viscous forces. Two geometrically similar flows with equal Re (and Mach number) have the same coefficients; that is why wind-tunnel tests work.',
              'The Navier–Stokes equations add viscous stresses to Euler’s equation. Prandtl’s boundary-layer simplification and the Blasius solution give, for a laminar flat plate, δ = 5.0x/√Re_x and C_f = 1.328/√Re_L.',
              'Above a transition Reynolds number (about 5 × 10⁵ on a smooth flat plate) the layer becomes turbulent: thicker, with more skin friction, C_f ≈ 0.074/Re_L^0.2, but more resistant to separation.',
              'In an adverse pressure gradient the boundary layer can separate, leaving a wide wake and pressure drag. Total drag = skin friction + pressure (form) drag + induced drag + wave drag (Unit 9).'],
 'eqs': [('Re=\\frac{\\rho VL}{\\mu}', 'Reynolds number'), ('\\delta=\\frac{5.0x}{\\sqrt{Re_x}}', 'Laminar boundary-layer thickness'), ('C_f=\\frac{1.328}{\\sqrt{Re_L}}', 'Laminar skin friction (Blasius)'), ('C_f=\\frac{0.074}{Re_L^{0.2}}', 'Turbulent skin friction (flat plate)')],
 'worked': [
  {'q': 'Find the Reynolds number of a wing with chord 1.5 m at 70 m/s at sea level.', 'steps': ['Re = 1.225 × 70 × 1.5/1.789 × 10⁻⁵.'], 'a': 'Re = 7.19 × 10⁶ (turbulent over most of the chord).'},
  {'q': 'Compare laminar and turbulent skin-friction coefficients at Re_L = 10⁶, and the boundary-layer thickness at x = 1 m.', 'steps': ['Laminar C_f = 1.328/1000; turbulent C_f = 0.074/15.85.', 'δ_lam = 5.0/1000; δ_turb = 0.37/15.85.'], 'a': 'C_f = 0.00133 vs 0.00467; δ = 5.0 mm vs 23.3 mm.'},
  {'q': 'A 1 m × 1 m flat plate at 30 m/s at sea level stays laminar (Re = 2.05 × 10⁶, assumed). Find the skin-friction drag on one side.', 'steps': ['q = ½ × 1.225 × 900 = 551.25 Pa.', 'C_f = 1.328/√(2.054 × 10⁶) = 0.000927.', 'D = qSC_f.'], 'a': 'D = 0.511 N.'}],
 'practice': [('A model at 1/10 scale must match Re in the same air. What speed?', '10 times the full-scale speed (often impossible, so pressurized or cryogenic tunnels are used).'), ('Does C_f grow or shrink as Re rises?', 'It shrinks for both laminar and turbulent layers.'),
              ('Why do golf balls have dimples?', 'A turbulent boundary layer separates later, cutting pressure drag.'), ('Name four drag components.', 'Skin friction, pressure, induced, wave.')],
 'misc': [('Turbulent flow always means more drag.', 'More skin friction, but often less pressure drag if separation is delayed.'), ('The boundary layer is thick.', 'It is millimetres to centimetres on a wing.'),
          ('Reynolds number depends only on speed.', 'It depends on density, speed, length and viscosity.')],
 'quiz': [{'q': 'Reynolds number compares…', 'opts': ['inertia to viscosity', 'pressure to gravity', 'speed to sound', 'lift to drag'], 'ok': 0, 'why': 'Re = ρVL/μ.'},
          {'q': 'Laminar flat-plate C_f is…', 'opts': ['0.074/Re^0.2', '1.328/√Re', '5/√Re', '2π'], 'ok': 1, 'why': 'Blasius.'},
          {'q': 'Separation is promoted by…', 'opts': ['favorable pressure gradient', 'adverse pressure gradient', 'high density', 'shocks only'], 'ok': 1, 'why': 'Rising pressure slows the layer.'},
          {'q': 'No-slip means…', 'opts': ['air speed at the wall is zero', 'no friction', 'inviscid flow', 'no pressure'], 'ok': 0, 'why': 'Fluid sticks to the wall.'}],
 'cards': [('No slip', 'Zero velocity at the wall.'), ('Reynolds number', 'ρVL/μ.'), ('Laminar δ', '5.0x/√Re_x.'), ('Laminar C_f', '1.328/√Re_L.'), ('Turbulent C_f', '0.074/Re_L^0.2.'), ('Separation', 'Adverse gradient, wake, pressure drag.')],
 'planet': {'text': ['Skin friction is a large share of an airliner’s cruise drag, which is why engineers work so hard on smooth surfaces and on keeping boundary layers laminar longer. Every unit of drag removed is fuel and carbon not burned.',
                     'EPA reports that the aircraft covered by its greenhouse gas standards account for 10 percent of U.S. transportation greenhouse gas emissions and 3 percent of total U.S. emissions, and that its 2020 standards align with the International Civil Aviation Organization’s CO₂ standards. Boundary-layer engineering, from riblets to laminar-flow wings, is one route to meeting those rules.'],
            'site': [('Solutions', 'Solutions.html'), ('Differential Equations', 'Differential_Equations.html')],
            'src': [_EPA, ('NASA Glenn: Boundary layer', _G + 'boundlay.html')]},
 'res': [('NASA Glenn: Boundary layer', _G + 'boundlay.html', 'Free NASA page.'), ('NASA Glenn: Reynolds number', _G + 'reynolds.html', 'Free NASA page.'), ('OpenStax UP1, 14.7 Viscosity and turbulence', _O + '14-7-viscosity-and-turbulence', 'Free textbook section.'), (_MIT[0], _MIT[1], 'Viscous flow lectures.')]})
UNITS.append(
{'id': 'u9', 'title': 'Compressible Flow: Isentropic Relations and Shock Waves', 'weeks': 'Weeks 12–13',
 'summary': 'When compressibility matters, stagnation properties, isentropic relations, area–velocity relation and nozzles, normal shocks, oblique shocks and expansion waves in brief, the critical Mach number, drag divergence, wave drag and supercritical airfoils.',
 'objectives': ['Use isentropic relations to find stagnation properties.', 'Explain the area–velocity relation and choked nozzles.', 'Compute properties across a normal shock.', 'Explain critical Mach number and why supercritical airfoils delay drag rise.'],
 'concepts': ['Below about M = 0.3 density changes are under 5% and flow can be treated as incompressible. Above that, energy and density changes must be included.',
              'Stagnation properties for adiabatic, isentropic flow: T₀/T = 1 + (γ − 1)M²/2, p₀/p = (T₀/T)^(γ/(γ−1)), ρ₀/ρ = (T₀/T)^(1/(γ−1)).',
              'Area–velocity: dA/A = (M² − 1)dV/V. Subsonic flow speeds up in a converging duct; supersonic flow speeds up in a diverging one. Sonic flow occurs at a throat; A/A* sets the Mach number.',
              'A normal shock is a thin, irreversible jump: supersonic flow becomes subsonic, and pressure, density and temperature jump while total pressure falls. For γ = 1.4 and M₁ = 2, M₂ = 0.577 and p₂/p₁ = 4.5.',
              'On a wing at high subsonic speed, the flow over the top reaches M = 1 first, at the critical Mach number. Beyond it a shock forms and drag rises sharply (drag divergence). Supercritical airfoils and wing sweep push this rise to higher speeds.'],
 'eqs': [('\\frac{T_0}{T}=1+\\frac{\\gamma-1}{2}M^2', 'Stagnation temperature'), ('\\frac{p_0}{p}=\\left(\\frac{T_0}{T}\\right)^{\\gamma/(\\gamma-1)}', 'Isentropic pressure ratio'), ('M_2^2=\\frac{1+\\frac{\\gamma-1}{2}M_1^2}{\\gamma M_1^2-\\frac{\\gamma-1}{2}}', 'Normal-shock Mach number'), ('\\frac{p_2}{p_1}=1+\\frac{2\\gamma}{\\gamma+1}(M_1^2-1)', 'Normal-shock pressure ratio')],
 'worked': [
  {'q': 'An airliner flies at M = 0.85. Find T₀/T and p₀/p.', 'steps': ['T₀/T = 1 + 0.2 × 0.7225 = 1.1445.', 'p₀/p = 1.1445^3.5.'], 'a': 'T₀/T = 1.1445; p₀/p = 1.604.'},
  {'q': 'Find M₂, p₂/p₁, ρ₂/ρ₁ and T₂/T₁ across a normal shock with M₁ = 2.', 'steps': ['M₂ = √(1.8/5.4).', 'p₂/p₁ = 1 + (2.8/2.4)(3).', 'ρ₂/ρ₁ = 2.4 × 4/(2 + 0.4 × 4) = 2.667.', 'T₂/T₁ = (p₂/p₁)/(ρ₂/ρ₁).'], 'a': 'M₂ = 0.577, p₂/p₁ = 4.5, ρ₂/ρ₁ = 2.667, T₂/T₁ = 1.688.'},
  {'q': 'NASA puts the speed of sound at cruise altitude at around 660 mph. Convert it to m/s and compare with the standard-atmosphere value at 11 km (295.1 m/s).', 'steps': ['660 × 0.44704 = 295.0 m/s.'], 'a': '295.0 m/s, within 0.1% of the standard-atmosphere value.'}],
 'practice': [('Find p₀/p at M = 2.', '1.8^3.5 = 7.82.'), ('Find A/A* at M = 2.', '1.688.'),
              ('Below what Mach number can density changes usually be ignored?', 'About 0.3.'), ('Across a normal shock, does total pressure rise or fall?', 'It falls (entropy rises).')],
 'misc': [('A shock speeds up the flow.', 'A normal shock makes supersonic flow subsonic.'), ('Wave drag only matters above M = 1.', 'It starts above the critical Mach number, below M = 1 on a wing.'),
          ('A diverging duct always slows the flow.', 'It speeds up supersonic flow.')],
 'quiz': [{'q': 'T₀/T at M = 1 is…', 'opts': ['1.0', '1.2', '1.4', '2.0'], 'ok': 1, 'why': '1 + 0.2.'},
          {'q': 'Supersonic flow speeds up in a…', 'opts': ['converging duct', 'diverging duct', 'constant duct', 'no duct'], 'ok': 1, 'why': 'dA/A = (M² − 1)dV/V.'},
          {'q': 'p₂/p₁ across a normal shock at M₁ = 2 is…', 'opts': ['2', '4.5', '7.8', '1.7'], 'ok': 1, 'why': 'Normal-shock relation.'},
          {'q': 'Supercritical airfoils…', 'opts': ['raise the drag-divergence Mach number', 'eliminate lift', 'add camber only at the nose', 'work only at Mach 2'], 'ok': 0, 'why': 'Weaker shock.'}],
 'cards': [('Incompressible limit', 'M < 0.3.'), ('T₀/T', '1 + 0.2M².'), ('p₀/p', '(T₀/T)^3.5.'), ('Area–velocity', 'dA/A = (M² − 1)dV/V.'), ('Normal shock M=2', 'M₂ = 0.577, p₂/p₁ = 4.5.'), ('Critical Mach', 'Local M = 1 on the wing.')],
 'planet': {'text': ['NASA explains that as airliners approach the speed of sound, about 660 mph at cruise altitude, a standing shock wave forms on a conventional wing and adds drag. Whitcomb’s supercritical airfoil, flatter on top and rounded on the bottom, minimized that shock, raising efficiency by as much as 15% according to NASA.',
                     'That is the critical-Mach and drag-divergence story from this unit. NASA says the design became the industry standard and saves billions of dollars in fuel a year; less fuel burned at cruise means less CO₂ from the flights that make up a large share of aviation emissions.'],
            'site': [('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html'), ('Space Weather', 'Space_Weather.html')],
            'src': [_SC, ('NASA Glenn: Normal shock wave', _G + 'normal.html')]},
 'res': [('NASA Glenn: Isentropic flow', _G + 'isentrop.html', 'Free NASA page.'), ('NASA Glenn: Normal shock wave', _G + 'normal.html', 'Free NASA page.'), ('NASA Glenn: Mach number', _G + 'mach.html', 'Free NASA page.'), (_MIT[0], _MIT[1], 'Compressible flow lectures.')]})
UNITS.append(
{'id': 'u10', 'title': 'Aircraft Performance: Drag Polar, Glide, Range and Endurance', 'weeks': 'Weeks 14–15',
 'summary': 'The drag polar C_D = C_D0 + KC_L², thrust and power required, minimum-drag speed, maximum lift-to-drag ratio, gliding flight, the Breguet range and endurance equations, and how aerodynamic efficiency translates into fuel and emissions.',
 'objectives': ['Build a drag polar and find (L/D)max.', 'Find the minimum-drag speed and glide distance.', 'Use the Breguet range equation.', 'Connect drag reductions to fuel burn.'],
 'concepts': ['The drag polar C_D = C_D0 + KC_L² with K = 1/(πeAR) combines zero-lift (parasite) drag and induced drag.',
              'In level flight L = W and T = D. Drag is lowest where parasite and induced drag are equal: C_L* = √(C_D0/K), giving (L/D)max = 1/(2√(KC_D0)).',
              'Gliding: with no thrust, the glide ratio equals L/D, so the best glide distance from height h is h(L/D)max.',
              'Breguet range for a jet: R = (V/c)(L/D) ln(W_i/W_f), with c the thrust-specific fuel consumption. Range grows directly with L/D, so aerodynamic efficiency multiplies with engine efficiency and weight.',
              'For a fixed trip, raising L/D lowers the fuel needed; that is why winglets, supercritical airfoils and high-aspect-ratio wings all cut CO₂.'],
 'eqs': [('C_D=C_{D0}+KC_L^2,\\ K=\\frac{1}{\\pi eAR}', 'Drag polar'), ('\\left(\\frac LD\\right)_{max}=\\frac{1}{2\\sqrt{KC_{D0}}}', 'Maximum lift-to-drag ratio'), ('C_L^*=\\sqrt{C_{D0}/K}', 'Lift coefficient for minimum drag'), ('R=\\frac{V}{c}\\frac{L}{D}\\ln\\frac{W_i}{W_f}', 'Breguet range (jet)')],
 'worked': [
  {'q': 'A wing has AR = 8, e = 0.9 and C_D0 = 0.02. Find K, (L/D)max and C_L*.', 'steps': ['K = 1/(π × 0.9 × 8) = 0.04421.', '(L/D)max = 1/(2√(0.04421 × 0.02)).', 'C_L* = √(0.02/0.04421).'], 'a': 'K = 0.04421, (L/D)max = 16.81, C_L* = 0.673.'},
  {'q': 'For that airplane (W = 9810 N, S = 16 m², sea level), find the minimum-drag speed and the best glide distance from 1000 m.', 'steps': ['V = √(2W/(ρSC_L*)) = √(19,620/(1.225 × 16 × 0.6726)).', 'Glide = 1000 × 16.81.'], 'a': 'V = 38.6 m/s; glide distance 16.8 km.'},
  {'q': 'A jet (sample values) cruises at V = 230 m/s with c = 1.6 × 10⁻⁴ s⁻¹, L/D = 17 and W_i/W_f = 1.25. Find the range.', 'steps': ['R = (230/1.6 × 10⁻⁴) × 17 × ln 1.25.'], 'a': 'R = 5453 km.'}],
 'practice': [('Raise L/D from 17 to 18 in the Breguet example. New range?', '5453 × 18/17 = 5774 km.'), ('What C_D does the polar give at C_L*?', '2C_D0 = 0.04.'),
              ('What is L/D at C_L = 1.0 for the worked polar?', '1.0/0.06421 = 15.57.'), ('A glider has L/D = 40. How far from 2 km?', '80 km.')],
 'misc': [('The best glide is at the slowest speed.', 'It is at the minimum-drag speed, faster than stall.'), ('Range depends only on fuel carried.', 'It depends on L/D, engine efficiency and the weight ratio.'),
          ('Parasite drag is always the largest part.', 'At low speed induced drag dominates.')],
 'quiz': [{'q': 'At minimum drag…', 'opts': ['parasite = induced', 'induced = 0', 'C_L = 0', 'V = stall'], 'ok': 0, 'why': 'Derivative of D is zero.'},
          {'q': 'Glide ratio equals…', 'opts': ['L/D', 'D/L', 'C_L', 'W/S'], 'ok': 0, 'why': 'No thrust.'},
          {'q': 'Breguet range is proportional to…', 'opts': ['D/L', 'L/D', 'C_D0', 'K'], 'ok': 1, 'why': 'R ∝ L/D.'},
          {'q': 'K in the polar is…', 'opts': ['1/(πeAR)', 'πeAR', 'C_D0', '2π'], 'ok': 0, 'why': 'Induced-drag factor.'}],
 'cards': [('Drag polar', 'C_D0 + KC_L².'), ('K', '1/(πeAR).'), ('(L/D)max', '1/(2√(KC_D0)).'), ('C_L*', '√(C_D0/K).'), ('Glide', 'Distance = h · L/D.'), ('Breguet', 'R = (V/c)(L/D) ln(W_i/W_f).')],
 'planet': {'text': ['NASA’s 2023 release on the Sustainable Flight Demonstrator says single-aisle aircraft account for nearly half of worldwide aviation emissions, and that the truss-braced-wing design, combined with other advances, could reduce fuel consumption and emissions by up to 30%. It ties this to the goal of net-zero aviation emissions by 2050.',
                     'The Breguet equation shows why: range and fuel efficiency scale with L/D. EPA notes that covered aircraft are 10 percent of U.S. transportation greenhouse gas emissions, so a few points of L/D, multiplied across thousands of flights a day, matter for the climate.'],
            'site': [('Solutions', 'Solutions.html'), ('Calculus I', 'Calculus_I.html')],
            'src': [_TTBW, _EPA]},
 'res': [('NASA Glenn: Lift to drag ratio', _G + 'ldrat.html', 'Free NASA page.'), ('NASA Glenn: Induced drag', _G + 'induced.html', 'Free NASA page.'), (_MITU[0], _MITU[1], 'Performance lectures.'), (_MIT[0], _MIT[1], 'MIT aerodynamics.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: The standard atmosphere spreadsheet', 'week': 'Week 1',
 'goal': 'Build NASA Glenn’s standard atmosphere model in a spreadsheet and see how temperature, pressure and density fall with altitude.',
 'eq': ('T=15.04-0.00649h,\\ \\ p=101.29\\left[\\frac{T+273.1}{288.08}\\right]^{5.256},\\ \\ \\rho=\\frac{p}{0.2869(T+273.1)}', 'NASA Glenn troposphere model (h in m, T in °C, p in kPa)'),
 'steps': ['Make a column of altitudes from 0 to 11,000 m in 500 m steps.', 'Add columns for T, p and ρ using NASA’s metric formulas.', 'Add the speed of sound a = √(1.4 × 287 × (T + 273.15)).', 'Plot ρ/ρ₀ against altitude and compare with FoilSim’s altitude setting.'],
 'table': (['h (m)', 'T (°C)', 'p (kPa)', 'ρ (kg/m³)'], [['0', '15.04', '101.40', '1.2266'], ['5,000', '−17.41', '54.11', '0.7377'], ['11,000', '−56.35', '22.71', '0.3652']]),
 'note': 'Values from NASA Glenn’s curve fits; textbook standard-atmosphere tables differ slightly (for example 1.225 kg/m³ at sea level).',
 'calc': ['ρ(11 km)/ρ(0) = 0.3652/1.2266 = 0.298.', 'a(11 km) = √(1.4 × 287 × 216.8) = 295.1 m/s.'],
 'safety': ['Computer only.'], 'home': ['Any free spreadsheet works.'],
 'sims': [(_FS[0], _FS[1]), (_ATM[0], _ATM[1])],
 'planet': 'Cruise altitude sits near the top of this table, where low density cuts drag; NASA’s model is the one used in FoilSim.', 'planet_src': [_ATM]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Bernoulli, the venturi and the pitot tube', 'week': 'Week 2',
 'goal': 'See pressure fall where flow speeds up, and turn a pitot-static pressure reading into airspeed.',
 'eq': ('V=\\sqrt{2(p_0-p)/\\rho}', 'Pitot-static airspeed'),
 'steps': ['Open PhET Fluid Pressure and Flow, Flow tab; narrow the pipe and read pressure and speed at both sections.', 'Check continuity A₁V₁ = A₂V₂ and Bernoulli’s pressure drop.', 'Home: hold a strip of paper below your lips and blow across the top; it rises. Hang two sheets of paper 3 cm apart and blow between them; they move together.', 'Fill the table for a pitot tube at sea level.'],
 'table': (['p₀ − p (Pa)', 'V (m/s)'], [['100', '12.8'], ['500', '28.6'], ['1500', '49.5']]),
 'note': 'Computed for ρ = 1.225 kg/m³; the paper demos show the effect, not exact numbers (the strip also rises because the jet follows the curved paper).',
 'calc': ['V = √(2 × 500/1.225) = 28.6 m/s.', 'Doubling V needs 4 times the pressure difference.'],
 'safety': ['Blow gently; stop if you feel dizzy.'], 'home': ['The paper demos are the home lab.'],
 'sims': [('PhET: Fluid Pressure and Flow', _PH + 'fluid-pressure-and-flow'), ('PhET: Under Pressure', _PH + 'under-pressure')],
 'planet': 'NASA notes Mars air is less than 1% as dense as Earth’s, so the same pitot reading on Mars would mean about 10 times the speed.', 'planet_src': [_ING]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: The lift curve in NASA FoilSim', 'week': 'Week 8',
 'goal': 'Measure lift coefficient against angle of attack, find the lift slope and zero-lift angle, and compare with thin airfoil theory.',
 'eq': ('c_l=2\\pi(\\alpha-\\alpha_{L=0})', 'Thin airfoil theory'),
 'steps': ['Open NASA FoilSim, choose a symmetric airfoil, set speed and altitude.', 'Record lift at α = 0°, 2°, 4°, 6°, … up to 10°, and convert to c_l = L/(qS).', 'Repeat with camber; find α_L=0.', 'Plot both curves and compare with the theory table.'],
 'table': (['α (°)', 'c_l theory (symmetric)'], [['0', '0'], ['2', '0.219'], ['4', '0.439'], ['6', '0.658']]),
 'note': 'Theory values; FoilSim includes thickness and other corrections, so your slope may differ by a few percent.',
 'calc': ['Slope = 0.658/6 = 0.110 per degree = 2π per radian.', 'c_l at 5° = 2π × 0.08727 = 0.548.'],
 'safety': ['Computer only.'], 'home': ['FoilSim runs in a browser.'],
 'sims': [(_FS[0], _FS[1])],
 'planet': 'DOE says turbine blades make lift like wings; blade designers use lift curves like this to set each section’s angle.', 'planet_src': [_WIND]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Paper gliders, aspect ratio and glide ratio', 'week': 'Week 10',
 'goal': 'Measure the glide ratio (L/D) of paper gliders with different aspect ratios and see induced drag in action.',
 'eq': ('\\frac LD=\\frac{\\text{distance}}{\\text{height}},\\ \\ AR=\\frac{b^2}{S}', 'Glide ratio and aspect ratio'),
 'steps': ['Build two simple gliders from printer paper with the same wing area: one short and wide, one long and narrow. Add a paper clip at the nose for balance.', 'Launch gently, level, from a fixed height (for example 1.5 m) in a large room or a calm outdoor space.', 'Measure horizontal distance for 5 flights each and average.', 'Compute AR and L/D for each and compare.'],
 'table': (['Glider', 'b (m)', 'S (m²)', 'AR', 'Distance from 1.5 m (m)', 'L/D'], [['Short wing', '0.20', '0.010', '4', '6.0', '4.0'], ['Long wing', '0.30', '0.010', '9', '9.0', '6.0']]),
 'note': 'Sample values to show the method; your results depend on folding, balance and launch.',
 'calc': ['AR = 0.30²/0.010 = 9.', 'L/D = 9.0/1.5 = 6.0.'],
 'safety': ['Never throw toward people or faces; clear the area first.', 'Launch from the floor or a sturdy step stool, not a chair (OSHA fall-protection guidance).'], 'home': ['This is a home lab.'],
 'sims': [(_FS[0], _FS[1]), ('NASA Glenn: Induced drag', _G + 'induced.html')],
 'planet': 'NASA’s truss-braced wing uses extra-long, thin wings for the same reason the long glider flies farther: less drag.', 'planet_src': [_TTBW]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Coffee-filter drag and terminal velocity', 'week': 'Week 11',
 'goal': 'Measure terminal velocity, find a drag coefficient, and show that drag grows with the square of speed.',
 'eq': ('mg=\\tfrac12\\rho V_t^2C_DA', 'Drag equals weight at terminal velocity'),
 'steps': ['Drop one paper coffee filter from about 2 m and film it in slow motion next to a tape measure.', 'Find the terminal speed from the last metre of fall.', 'Stack 2 and then 4 filters (same shape, more weight) and repeat.', 'Compute C_D and check that V_t grows as √m.'],
 'table': (['Filters', 'm (g)', 'V_t (m/s)', 'C_D'], [['1', '1.0', '1.20', '0.98'], ['2', '2.0', '1.70', '0.98']]),
 'note': 'Sample values with a 12 cm diameter filter; weigh your own filters on a kitchen scale.',
 'calc': ['C_D = 2 × 0.00981/(1.225 × 1.20² × π × 0.06²) = 0.98.', 'V_t(2 filters) = 1.20 × √2 = 1.70 m/s.'],
 'safety': ['Drop from standing height or a sturdy step stool only.', 'Keep the area clear of tripping hazards.'], 'home': ['This is a home lab.'],
 'sims': [('NASA Glenn: The drag equation', _G + 'drageq.html'), ('PhET: Fluid Pressure and Flow', _PH + 'fluid-pressure-and-flow')],
 'planet': 'EPA notes covered aircraft are 3% of total U.S. greenhouse gas emissions; drag is what their engines burn fuel to overcome.', 'planet_src': [_EPA]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Drag polar and range spreadsheet', 'week': 'Week 15',
 'goal': 'Build a drag polar, find (L/D)max, and use the Breguet equation to see how drag reductions change range and fuel.',
 'eq': ('C_D=C_{D0}+\\frac{C_L^2}{\\pi eAR}', 'Drag polar'),
 'steps': ['Set C_D0 = 0.02, e = 0.9 and AR = 8 (sample values).', 'Compute C_D and L/D for C_L from 0.1 to 1.2.', 'Find the maximum L/D and compare with 1/(2√(KC_D0)).', 'Change AR to 12, and total drag by −7% (NASA’s winglet drag figure), and see how range changes.'],
 'table': (['C_L', 'C_D', 'L/D'], [['0.2', '0.0218', '9.19'], ['0.673', '0.0400', '16.81'], ['1.0', '0.0642', '15.57']]),
 'note': 'Computed from the sample polar.',
 'calc': ['K = 0.04421; (L/D)max = 16.81 at C_L = 0.673.', 'Breguet range ∝ L/D, so +10% L/D gives +10% range.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('NASA Glenn: Lift to drag ratio', _G + 'ldrat.html'), (_FS[0], _FS[1])],
 'planet': 'NASA says winglets cut drag by as much as 7% and are now on about 10,000 jets, saving over 10 billion gallons of fuel.', 'planet_src': [_WL]})
SCHEDULE = [(1, 'u1', 'Fluid properties, ideal gas, speed of sound, standard atmosphere; Lab A', 'NASA Glenn atmosphere; MIT Unified'), (2, 'u2', 'Bernoulli, dynamic pressure, venturi, pitot-static; Lab B', 'NASA Glenn; OpenStax UP1 14.6'),
            (3, 'u3', 'Control volumes: mass and momentum; wake drag', 'MIT 16.100; UP1 14.5'), (4, 'u3', 'Differential equations of motion; rotor momentum theory', 'MIT Unified'),
            (5, 'u4', 'Vorticity, circulation, potential and stream function, elementary flows', 'MIT 16.100'), (6, 'u4', 'Cylinder flow, d’Alembert, Kutta–Joukowski', 'MIT 16.100'),
            (7, 'u5', 'Airfoil geometry, coefficients, lift curve, stall; midterm practice', 'NASA Glenn; FoilSim'), (8, 'u6', 'Thin airfoil theory and panel methods; Lab C', 'MIT 16.100; FoilSim'),
            (9, 'u7', 'Downwash, lifting-line theory, elliptic wings', 'MIT 16.100; NASA Glenn'), (10, 'u7', 'Induced drag, aspect ratio, winglets; Lab D', 'NASA Glenn'),
            (11, 'u8', 'Reynolds number, boundary layers, skin friction, separation; Lab E', 'NASA Glenn; UP1 14.7'), (12, 'u9', 'Isentropic flow and nozzles', 'NASA Glenn'),
            (13, 'u9', 'Normal shocks, critical Mach, supercritical airfoils', 'NASA Glenn; MIT 16.100'), (14, 'u10', 'Drag polar, glide, minimum drag', 'MIT Unified'),
            (15, 'u10', 'Breguet range and endurance; Lab F; final practice', 'MIT Unified')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Find the density of air at 60 kPa and 250 K.', ['ρ = 60,000/(287 × 250).'], '0.836 kg/m³.'),
  ('A pitot-static tube reads 800 Pa where ρ = 0.9 kg/m³. Find the true airspeed.', ['V = √(2 × 800/0.9).'], '42.2 m/s.'),
  ('Find the ideal hover power of a 500 kg helicopter with an 8 m rotor at sea level.', ['T = 4905 N; A = 50.27 m².', 'P = T^1.5/√(2ρA).'], '31.0 kW.'),
  ('Find C_p at θ = 45° on a non-lifting cylinder.', ['1 − 4 × 0.5.'], '−1.'),
  ('A body at sea level in a 40 m/s stream has Γ = 15 m²/s. Find L′.', ['1.225 × 40 × 15.'], '735 N/m.')]),
 ('Final practice set (all units)', [
  ('Find c_l for a symmetric thin airfoil at 3°.', ['2π × 0.05236.'], '0.329.'),
  ('Find C_Di for C_L = 0.6, AR = 10, e = 0.85.', ['0.36/(π × 8.5).'], '0.0135.'),
  ('Find Re for a 2 m chord at 50 m/s at sea level.', ['1.225 × 50 × 2/1.789 × 10⁻⁵.'], '6.85 × 10⁶.'),
  ('Find M₂ and p₂/p₁ across a normal shock at M₁ = 3.', ['M₂ = √(2.8/12.4); p₂/p₁ = 1 + (2.8/2.4) × 8.'], 'M₂ = 0.475, p₂/p₁ = 10.33.'),
  ('Find T₀/T and p₀/p at M = 0.8.', ['1 + 0.2 × 0.64 = 1.128; 1.128^3.5.'], '1.128 and 1.524.'),
  ('Find (L/D)max for C_D0 = 0.025, AR = 10, e = 0.85.', ['K = 0.03745.'], '16.34.')])]
FORMULAS = ['p=\\rho RT,\\ a=\\sqrt{\\gamma RT},\\ M=V/a', 'p+\\tfrac12\\rho V^2=p_0,\\ q=\\tfrac12\\rho V^2', 'C_p=1-(V/V_\\infty)^2', '\\dot m=\\rho AV,\\ \\nabla\\cdot\\mathbf V=0',
            'P_{ideal}=T^{3/2}/\\sqrt{2\\rho A}', 'L\'=\\rho_\\infty V_\\infty\\Gamma,\\ C_p=1-4\\sin^2\\theta', 'L=qSC_L,\\ D=qSC_D', 'c_l=2\\pi(\\alpha-\\alpha_{L=0})',
            'C_{D_i}=C_L^2/(\\pi eAR),\\ AR=b^2/S', 'Re=\\rho VL/\\mu,\\ C_f=1.328/\\sqrt{Re}', 'T_0/T=1+\\tfrac{\\gamma-1}2M^2', 'p_2/p_1=1+\\tfrac{2\\gamma}{\\gamma+1}(M_1^2-1)',
            '(L/D)_{max}=1/(2\\sqrt{KC_{D0}}),\\ R=\\tfrac Vc\\tfrac LD\\ln\\tfrac{W_i}{W_f}']
GLOSSARY = sorted([('Angle of attack', 'Angle between the chord and the oncoming flow.'), ('Aspect ratio', 'b²/S, span squared over wing area.'), ('Boundary layer', 'Thin layer near a surface where viscosity slows the flow.'),
    ('Camber', 'Curvature of an airfoil’s mean line.'), ('Circulation', 'Line integral of velocity around a closed curve; tied to lift.'), ('Critical Mach number', 'Free-stream Mach at which local flow first reaches M = 1.'),
    ('Downwash', 'Downward flow induced by trailing vortices.'), ('Drag polar', 'C_D as a function of C_L.'), ('Dynamic pressure', 'q = ½ρV².'), ('Induced drag', 'Drag from tilting lift by downwash.'),
    ('Kutta condition', 'Flow leaves a sharp trailing edge smoothly.'), ('Mach number', 'Flow speed over the speed of sound.'), ('Normal shock', 'Thin jump that turns supersonic flow subsonic.'),
    ('Reynolds number', 'ρVL/μ, inertia over viscosity.'), ('Separation', 'Boundary layer leaving the surface.'), ('Stagnation pressure', 'Pressure if flow is brought to rest isentropically.'),
    ('Stall', 'Loss of lift when flow separates at high angle of attack.'), ('Supercritical airfoil', 'Flat-topped airfoil that weakens shocks near M = 1.'), ('Vorticity', '∇ × V, twice the local rotation rate.'),
    ('Winglet', 'Near-vertical tip surface that reduces induced drag.')])
RUBRIC = [('4 · Mastery', 'Identifies the flow regime, chooses the right model (Bernoulli, momentum, potential flow, lifting line, boundary layer, isentropic, shock), checks units and limits, and runs labs safely.'), ('3 · Proficient', 'Solves the practice problems with occasional unit or density slips.'),
          ('2 · Developing', 'Follows worked examples but mixes up 2D and 3D coefficients, or degrees and radians.'), ('1 · Beginning', 'Plugs numbers into formulas without a sketch; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    R = 287; g = 1.4; r0 = 1.225; mu = 1.789e-5
    nT = lambda h: 15.04 - .00649 * h
    nP = lambda h: 101.29 * ((nT(h) + 273.1) / 288.08) ** 5.256
    nR = lambda h: nP(h) / (.2869 * (nT(h) + 273.1))
    snd = lambda T: sqrt(g * R * T)
    hp = lambda T, rho, A: T ** 1.5 / sqrt(2 * rho * A)
    cl = lambda a: 2 * pi * radians(a)
    K = 1 / (pi * .9 * 8)
    shM = lambda M: sqrt((1 + .2 * M * M) / (g * M * M - .2))
    shP = lambda M: 1 + 2 * g / (g + 1) * (M * M - 1)
    shR = lambda M: (g + 1) * M * M / (2 + (g - 1) * M * M)
    AAs = lambda M: (1 / M) * ((2 / (g + 1)) * (1 + .2 * M * M)) ** ((g + 1) / (2 * (g - 1)))
    Kf = 1 / (pi * 8.5)
    ldm = lambda k, c0: 1 / (2 * sqrt(k * c0))
    vt = lambda T, rho, A: sqrt(T / (2 * rho * A))
    brg = 230 / 1.6e-4 * 17 * log(1.25) / 1000
    r = [
     ('u1 rho0', 101325 / (R * 288.15), 1.225), ('u1 T11', nT(11000), -56.35), ('u1 p11', nP(11000), 22.71), ('u1 r11', nR(11000), .3652), ('u1 ratio', nR(11000) / r0, .298),
     ('u1 a0', snd(288.15), 340.3), ('u1 a11', snd(216.8), 295.1), ('u1 M', 250 / snd(216.8), .847), ('u1 rho80', 80000 / (R * 270), 1.032), ('u1 kn', 450 * .514444, 231.5), ('u1 nu', mu / r0, 1.460e-5),
     ('u1 T5', nT(5000), -17.41), ('u1 lapse', .00649 * 5000, 32.45),
     ('u2 V', sqrt(2 * 1500 / r0), 49.5), ('u2 V2', 20 * 1, 20), ('u2 dp', .5 * r0 * (400 - 100), 183.8), ('u2 q', .5 * r0 * 140**2, 12.0e3), ('u2 Vt', 140 * sqrt(r0 / .3652), 256.4), ('u2 q100', .5 * r0 * 1e4, 6125),
     ('u2 cp', 1 - 1.5**2, -1.25), ('u2 man', 1000 * 9.81 * .05, 490.5), ('u2 mars', sqrt(100), 10),
     ('u3 mdot', r0 * .5 * 20, 12.25), ('u3 V2', 20 * .5 / .2, 50), ('u3 A', pi * 25, 78.54), ('u3 v', vt(9810, r0, pi * 25), 7.14), ('u3 P', 9810 * vt(9810, r0, pi * 25), 70.0e3), ('u3 wake', r0 * 6, 7.35),
     ('u3 T2', 2 ** 1.5, 2.83), ('u3 A2', 1 / sqrt(2), .707), ('u3 jet', 1000 * .01 * 100, 1000), ('u3 ingT', 1.8 * 3.71, 6.68), ('u3 ingP', hp(1.8 * 3.71, .0115, pi * .36), 107),
     ('u4 vmax', 2 * 20, 40), ('u4 cpmin', 1 - 4, -3), ('u4 L', r0 * 50 * 20, 1225), ('u4 vort', 20 / (2 * pi), 3.183), ('u4 cp0', degrees(asin_(.5)), 30), ('u4 L2', 2 * 1225, 2450),
     ('u5 q', .5 * r0 * 3600, 2205), ('u5 L', 2205 * 16 * .5, 17640), ('u5 q50', .5 * r0 * 2500, 1531.25), ('u5 CL', 9810 / (1531.25 * 16), .400), ('u5 Vs', sqrt(2 * 9810 / (r0 * 16 * 1.6)), 25.0),
     ('u5 kn', sqrt(2 * 9810 / (r0 * 16 * 1.6)) / .514444, 48.6), ('u5 L15', 1.5**2, 2.25), ('u5 Vs11', sqrt(2 * 9810 / (r0 * 16 * 1.6)) * sqrt(r0 / .3652), 45.8),
     ('u6 a5', radians(5), .08727), ('u6 cl5', cl(5), .548), ('u6 cl6', cl(6), .658), ('u6 r6', radians(6), .10472), ('u6 cm', -cl(5) / 4, -.137), ('u6 a05', .5 / (2 * pi), .0796), ('u6 a05d', degrees(.5 / (2 * pi)), 4.56),
     ('u6 slope', 2 * pi * pi / 180, .1097),
     ('u7 CDi', .25 / (pi * .9 * 8), .01105), ('u7 den', 1 + 2 * pi / (pi * 7.2), 1.2778), ('u7 a', 2 * pi / (1 + 2 / 7.2), 4.917), ('u7 adeg', 2 * pi / (1 + 2 / 7.2) * pi / 180, .0858), ('u7 ai', .5 / (pi * 8), .01989),
     ('u7 aid', degrees(.5 / (pi * 8)), 1.14), ('u7 AR', 900 / 100, 9), ('u7 CDi12', .25 / (pi * .9 * 12), .00737),
     ('u8 Re', r0 * 70 * 1.5 / mu, 7.19e6), ('u8 cfl', 1.328 / 1000, .00133), ('u8 cft', .074 / 1e6**.2, .00467), ('u8 pow', 1e6**.2, 15.85), ('u8 dl', 5.0 / 1000, .005), ('u8 dt', .37 / 1e6**.2, .0233),
     ('u8 q', .5 * r0 * 900, 551.25), ('u8 Re2', r0 * 30 / mu, 2.05e6), ('u8 cf2', 1.328 / sqrt(r0 * 30 / mu), .000927), ('u8 D', 551.25 * 1.328 / sqrt(r0 * 30 / mu), .511),
     ('u9 T0', 1 + .2 * .85**2, 1.1445), ('u9 p0', (1 + .2 * .85**2) ** 3.5, 1.604), ('u9 M2', shM(2), .577), ('u9 p2', shP(2), 4.5), ('u9 r2', shR(2), 2.667), ('u9 T2', shP(2) / shR(2), 1.688),
     ('u9 mph', 660 * .44704, 295.0), ('u9 p0M2', 1.8**3.5, 7.82), ('u9 AAs', AAs(2), 1.688), ('u9 T0M1', 1.2, 1.2),
     ('u10 K', K, .04421), ('u10 LD', ldm(K, .02), 16.81), ('u10 CLs', sqrt(.02 / K), .673), ('u10 V', sqrt(2 * 9810 / (r0 * 16 * sqrt(.02 / K))), 38.6), ('u10 gl', 1000 * ldm(K, .02) / 1000, 16.8),
     ('u10 R', brg, 5453), ('u10 R18', brg * 18 / 17, 5774), ('u10 CDs', .02 + K * .02 / K, .04), ('u10 LD1', 1 / (.02 + K), 15.57), ('u10 gl40', 2 * 40, 80),
     ('A T0', nT(0), 15.04), ('A p0', nP(0), 101.40), ('A r0', nR(0), 1.2266), ('A T5', nT(5000), -17.41), ('A p5', nP(5000), 54.11), ('A r5', nR(5000), .7377), ('A rat', nR(11000) / nR(0), .298), ('A a', snd(216.8), 295.1),
     ('B 100', sqrt(200 / r0), 12.8), ('B 500', sqrt(1000 / r0), 28.6), ('B 1500', sqrt(3000 / r0), 49.5),
     ('C 2', cl(2), .219), ('C 4', cl(4), .439), ('C 6', cl(6), .658), ('C sl', cl(6) / 6, .110),
     ('D AR1', .2**2 / .01, 4), ('D AR2', .3**2 / .01, 9), ('D LD1', 6 / 1.5, 4), ('D LD2', 9 / 1.5, 6),
     ('E CD', 2 * .00981 / (r0 * 1.44 * pi * .06**2), .98), ('E v2', 1.2 * sqrt(2), 1.70),
     ('F cd2', .02 + K * .04, .0218), ('F ld2', .2 / (.02 + K * .04), 9.19), ('F cd6', .02 + K * .6726**2, .0400), ('F ld6', .6726 / (.02 + K * .6726**2), 16.81), ('F cd1', .02 + K, .0642), ('F ld1', 1 / (.02 + K), 15.57),
     ('M1', 60000 / (R * 250), .836), ('M2', sqrt(1600 / .9), 42.2), ('M3 A', pi * 16, 50.27), ('M3 P', hp(4905, r0, pi * 16), 31.0e3), ('M4', 1 - 4 * .5, -1), ('M5', r0 * 40 * 15, 735),
     ('F1', cl(3), .329), ('F2', .36 / (pi * 8.5), .0135), ('F3', r0 * 100 / mu, 6.85e6), ('F4 M', shM(3), .475), ('F4 p', shP(3), 10.33), ('F5 T', 1 + .2 * .64, 1.128), ('F5 p', 1.128**3.5, 1.524),
     ('F6 K', Kf, .03745), ('F6 LD', ldm(Kf, .025), 16.34)]
    return r

def asin_(x):
    from math import asin
    return asin(x)

_CHECKS_MAIN = CHECKS

def CHECKS():
    """Main checks plus cross-checks of intermediate values printed in steps, tables and labs."""
    R = 287; r0 = 1.225; mu = 1.789e-5
    K = 1 / (pi * .9 * 8)
    nT = lambda h: 15.04 - .00649 * h
    extra = [
     ('x u1 T11K', nT(11000) + 273.15, 216.8), ('x u1 rsl', 1.225, 1.225), ('x u1 Mars', .01 * r0, .01225), ('x u1 qual', sqrt(2), 1.414), ('x u1 a0kn', sqrt(1.4 * R * 288.15) / .514444, 661.4),
     ('x u2 q20', .5 * r0 * 400, 245), ('x u2 q10', .5 * r0 * 100, 61.25), ('x u2 rat', sqrt(r0 / .3652), 1.8315), ('x u2 V4', 4, 4), ('x u2 cpst', 1 - 0, 1),
     ('x u3 Aing', pi * .6**2, 1.131), ('x u3 r', 1.2 / 2, .6), ('x u3 tv', 9810 / (2 * r0 * pi * 25), 50.98), ('x u3 Ting', 1.8 * 3.71 * 1, 6.678), ('x u3 ingr', 350 / hp_(6.678, .0115, pi * .36), 3.27),
     ('x u3 dens', .0115 / r0, .00939),
     ('x u4 V45', 2 * 20 * sin(radians(45)), 28.28), ('x u4 cp90', 1 - 4 * sin(radians(90))**2, -3), ('x u4 cp30', round(1 - 4 * sin(radians(30))**2, 12), 0), ('x u4 v2', 20 / (2 * pi * 2), 1.592),
     ('x u5 W', 1000 * 9.81, 9810), ('x u5 q60', .5 * r0 * 60**2, 2205), ('x u5 Vs2', 2 * 9810 / (r0 * 16 * 1.6), 625.6), ('x u5 CLmax', 9810 / (.5 * r0 * 25.0**2 * 16), 1.6),
     ('x u6 cl10', 2 * pi * radians(10), 1.097), ('x u6 xcp', .137 / .548, .25), ('x u6 rad', pi / 180, .017453),
     ('x u7 pieAR', pi * .9 * 8, 22.62), ('x u7 piAR', pi * 8, 25.13), ('x u7 r', 8 / 12, .6667), ('x u7 CDi2', .25 / (pi * .9 * 16), .005526),
     ('x u8 sqrt', sqrt(1e6), 1000), ('x u8 Re30', r0 * 30 * 1 / mu, 2.054e6), ('x u8 ratio', (.074 / 1e6**.2) / (1.328 / 1000), 3.52),
     ('x u9 p11', .2 * 4, .8), ('x u9 M2sq', 1.8 / 5.4, .3333), ('x u9 Ma', 660 * .44704 / sqrt(1.4 * R * 216.8), 1.0), ('x u9 T0M2', 1 + .2 * 4, 1.8),
     ('x u10 CD0K', K * .02, .000884), ('x u10 ln', log(1.25), .2231), ('x u10 Vc', 230 / 1.6e-4, 1.4375e6), ('x u10 2cd0', 2 * .02, .04),
     ('x E A', pi * .06**2, .01131), ('x E W', .001 * 9.81, .00981), ('x F R12', (1 / (2 * sqrt(.02 / (pi * .9 * 12)))), 20.59)]
    return _CHECKS_MAIN() + extra

def hp_(T, rho, A):
    return T ** 1.5 / sqrt(2 * rho * A)
