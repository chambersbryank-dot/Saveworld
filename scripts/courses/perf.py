"""Aircraft Performance (AERO 320): the standard atmosphere, the drag polar, thrust and power required, climb, glide, range and endurance, takeoff, landing, turning flight and the V-n diagram, and the performance of electric and sustainable aircraft.
Oct 25 2026, founder-approved four-year track, junior course 4. Same module fields as fluids.py / thermo.py / aero1.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, log, exp, cos, tan, sin, asin, atan, radians, degrees
ID = 'perf'
STATUS = 'live'
YEAR = 3
PAGE = 'Aircraft_Performance.html'
CODE = 'AERO 320'
TITLE = 'Aircraft Performance'
LAB_NAME = 'Flight performance lab'
TAGLINE = 'Range, endurance, climb and takeoff: the standard atmosphere and density altitude, the drag polar and best lift-to-drag ratio, thrust and power required, rate of climb, gliding flight, the Breguet range and endurance equations, takeoff and landing distances, turns and the V-n diagram, and how electric, hybrid and sustainable-fuel aircraft change the numbers, with six labs. Free, self-paced, and tied to NASA and DOE work on cleaner flight.'
DESC = 'Free self-study Aircraft Performance: 10 units, worked examples, solved practice, quizzes, flashcards, 6 simulation, spreadsheet and home labs, practice exams, tied to fuel-saving wings and sustainable aviation fuel.'
ALT = 'The International Space Station seen from a departing spacecraft above Earth'
_G = 'https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 16.01–16.04 Unified Engineering (2005–2006)', 'https://ocw.mit.edu/courses/16-01-unified-engineering-i-ii-iii-iv-fall-2005-spring-2006/')
_MITA = ('MIT OpenCourseWare 16.100 Aerodynamics (Fall 2005)', 'https://ocw.mit.edu/courses/16-100-aerodynamics-fall-2005/')
_MITS = ('MIT OpenCourseWare 16.885J Aircraft Systems Engineering (Fall 2005)', 'https://ocw.mit.edu/courses/16-885j-aircraft-systems-engineering-fall-2005/')
_PHAK = ('FAA Pilot’s Handbook of Aeronautical Knowledge (FAA-H-8083-25C)', 'https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak')
_CH11 = ('FAA PHAK Chapter 11: Aircraft Performance (PDF)', 'https://www.faa.gov/sites/faa.gov/files/13_phak_ch11.pdf')
_CH10 = ('FAA PHAK Chapter 10: Weight and Balance (PDF)', 'https://www.faa.gov/sites/faa.gov/files/12_phak_ch10.pdf')
_AFH = ('FAA Airplane Flying Handbook', 'https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/airplane_handbook')
_SUS = ('NASA: Sustainable Aviation', 'https://www.nasa.gov/directorates/armd/sustainable-aviation/')
_CAT = ('NASA: NASA Tests Technology Offering Potential Fuel Savings for Commercial Aviation (Jan. 21, 2026)', 'https://www.nasa.gov/centers-and-facilities/armstrong/nasa-tests-technology-offering-potential-fuel-savings-for-commercial-aviation/')
_CATF = ('NASA: NASA Completes First Flight of Laminar Flow Scaled Wing Design (Feb. 11, 2026)', 'https://www.nasa.gov/image-article/nasa-completes-first-flight-of-laminar-flow-scaled-wing-design/')
_HYB = ('NASA: NASA, GE Aerospace Hybrid Engine System Marks Successful Test (Jan. 26, 2026)', 'https://www.nasa.gov/aeronautics/hybrid-engine-tested/')
_TBW = ('NASA: NASA, Boeing Advance Truss-Braced Wing Research in Test (Apr. 29, 2026)', 'https://www.nasa.gov/image-article/nasa-boeing-advance-truss-braced-wing-research-in-test/')
_SAF = ('U.S. DOE: Sustainable Aviation Fuels', 'https://www.energy.gov/eere/bioenergy/sustainable-aviation-fuels')
_EIA = ('U.S. EIA: Use of energy for transportation', 'https://www.eia.gov/energyexplained/use-of-energy/transportation.php')
_GLD = ('NASA Glenn Beginner’s Guide: Glide angle', _G + 'glide-angle/')
BANNER = ['images/ISS_Flyaround_2021.jpg', 'images/ISS_Over_Ganges_STS102.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg']
CREDITS = {'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)', 'images/ISS_Over_Ganges_STS102.jpg': 'NASA (STS102-357-031, March 18, 2001)',
           'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester junior aircraft performance course. It is modeled on the topics and depth of the performance parts of MIT 16.01–16.04 Unified Engineering and MIT 16.885J Aircraft Systems Engineering (free on MIT OpenCourseWare), on courses such as Purdue AAE 251 and Georgia Tech AE 3310, and on the FAA Pilot’s Handbook of Aeronautical Knowledge, Chapter 11, which we link where they help. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (laminar-flow wings, truss-braced wings, hybrid engines, sustainable aviation fuel and transportation energy), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation, a spreadsheet or a safe home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Performance is where aircraft design meets fuel burn. Every percent of drag removed, every kilogram saved and every better climb or cruise profile shows up directly in the Breguet range equation, and so in fuel use and emissions.',
                 'NASA lists three main ways to make aviation sustainable: efficient aircraft technology, sustainable aviation fuel, and operations and infrastructure. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values.']
PREREQS = ['Aerodynamics I: lift and drag coefficients, the drag polar and induced drag.', 'Dynamics: Newton’s laws, work and energy.',
           'Calculus II: integrals and natural logarithms (for range and endurance).', 'Thermodynamics helps with engines and the atmosphere but is not required.']
STUDY = ['Start every problem with a free-body diagram: lift, weight, thrust and drag, and the flight-path angle.', 'Write down the atmosphere first: altitude, density, temperature and speed of sound.',
         'Keep weight in newtons and mass in kilograms; most errors in performance come from mixing them.', 'Know the key speeds by heart: stall, minimum drag, minimum power, best climb and approach.',
         'Check limits: zero excess thrust means zero climb; heavier aircraft need more runway, roughly as weight squared.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free NASA FoilSim and PhET Projectile Motion simulations.', 'Spreadsheet software for the atmosphere, drag-polar, range and takeoff labs.',
            'Printer paper, a ruler or tape measure, paper clips and a stopwatch or phone timer.', 'A safe open indoor space or a calm outdoor space for glider flights.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab can be done in a free simulation, a spreadsheet, or with paper and a tape measure. Fly paper gliders only in a clear space away from people’s faces, stairs and traffic, and keep walkways free of trip hazards.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('International Standard Atmosphere, sea level (textbook values)', 'ρ₀ = 1.225 kg/m³, T₀ = 288.15 K, p₀ = 101,325 Pa, lapse rate 0.0065 K/m to 11 km'), ('Air', 'R = 287 J/(kg·K), γ = 1.4'), ('Gravity', 'g = 9.81 m/s²'),
             ('Sample airliner used throughout (sample values)', 'm = 60,000 kg, W = 588.6 kN, S = 120 m², C_D0 = 0.020, K = 0.045'), ('Jet fuel (textbook values)', 'about 43 MJ/kg; about 3.16 kg CO₂ per kg burned'), ('1 m/s', '196.85 ft/min')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, handbooks and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT lecture notes, including aircraft performance.'), (_MITS[0], _MITS[1], 'Free MIT course on aircraft systems.'), (_MITA[0], _MITA[1], 'Free MIT aerodynamics course.'),
          (_PHAK[0], _PHAK[1], 'Free FAA handbook; Chapter 11 covers performance.'), (_AFH[0], _AFH[1], 'Free FAA handbook on takeoff, landing and maneuvers.'),
          ('NASA Glenn: Beginner’s Guide to Aeronautics', _G, 'Free NASA explanations of lift, drag and gliding.'), ('NASA Glenn: FoilSim', _G + 'foilsim/', 'Free wing simulation.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'The Standard Atmosphere, Airspeeds and Density Altitude', 'weeks': 'Week 1',
 'summary': 'Why performance depends on the air, the International Standard Atmosphere (ISA), temperature, pressure and density with altitude, the speed of sound and Mach number, indicated, calibrated, equivalent and true airspeed, and pressure and density altitude.',
 'objectives': ['Compute ISA temperature, pressure and density in the troposphere.', 'Find the speed of sound and Mach number.', 'Convert between equivalent and true airspeed.', 'Explain why hot, high airports hurt performance.'],
 'concepts': ['Lift, drag and engine thrust all depend on air density, so performance is always quoted for a stated atmosphere. The ISA is a reference: 288.15 K, 101,325 Pa and 1.225 kg/m³ at sea level.',
              'In the troposphere (up to 11 km) temperature falls 6.5 K per km: T = T₀ − 0.0065h. Hydrostatics plus the ideal-gas law give p/p₀ = (T/T₀)^5.26 and ρ/ρ₀ = (T/T₀)^4.26. Above 11 km temperature is constant at 216.65 K and density falls exponentially.',
              'The speed of sound is a = √(γRT); Mach number M = V/a. Because a depends only on temperature, it is lower at cruise altitude.',
              'An airspeed indicator senses dynamic pressure ½ρV². Equivalent airspeed EAS = V√σ, with density ratio σ = ρ/ρ₀; true airspeed is higher than EAS at altitude.',
              'Pressure altitude is the ISA altitude with the measured pressure; density altitude is the ISA altitude with the actual density. High density altitude (a high, hot or humid airfield) means thinner air, so less lift at a given speed and less engine thrust: takeoff gets longer and climb gets weaker.'],
 'eqs': [('T=T_0-0.0065h', 'Troposphere temperature'), ('\\frac{\\rho}{\\rho_0}=\\left(\\frac{T}{T_0}\\right)^{4.26}', 'Troposphere density'), ('a=\\sqrt{\\gamma RT},\\ M=\\frac{V}{a}', 'Speed of sound and Mach'), ('V_E=V\\sqrt{\\sigma}', 'Equivalent airspeed')],
 'worked': [
  {'q': 'Find the ISA temperature, pressure and density at 3000 m.', 'steps': ['T = 288.15 − 0.0065 × 3000 = 268.65 K.', 'p = 101,325 × (268.65/288.15)^5.26 = 70.1 kPa.', 'ρ = 1.225 × (268.65/288.15)^4.26 = 0.909 kg/m³.'], 'a': 'T = 268.65 K, p = 70.1 kPa, ρ = 0.909 kg/m³ (σ = 0.742).'},
  {'q': 'Find the speed of sound at sea level and at 11 km (216.65 K).', 'steps': ['a₀ = √(1.4 × 287 × 288.15).', 'a = √(1.4 × 287 × 216.65).'], 'a': 'a₀ = 340.3 m/s; a = 295.0 m/s.'},
  {'q': 'Find the ISA density and pressure at 11 km.', 'steps': ['T/T₀ = 216.65/288.15.', 'ρ = 1.225 × (0.7519)^4.26; p = 101,325 × (0.7519)^5.26.'], 'a': 'ρ = 0.364 kg/m³ and p = 22.6 kPa: less than a third of sea-level density.'}],
 'practice': [('Find ISA density at 5000 m.', '0.736 kg/m³.'), ('What Mach number is 250 m/s at sea level?', '250/340.3 = 0.735.'),
              ('Find the exponent g/(aR) − 1 for density.', '9.81/(0.0065 × 287) − 1 = 4.26.'), ('An airport at 1500 m on a hot day: is its density altitude above or below 1500 m?', 'Above: hot air is thinner.')],
 'misc': [('True airspeed equals indicated airspeed.', 'Only at sea-level standard conditions.'), ('The speed of sound depends on pressure.', 'For an ideal gas it depends only on temperature.'),
          ('Density altitude is the airport elevation.', 'It also depends on temperature, pressure and humidity.')],
 'quiz': [{'q': 'ISA sea-level density is…', 'opts': ['1.000 kg/m³', '1.225 kg/m³', '0.364 kg/m³', '101.3 kg/m³'], 'ok': 1, 'why': 'Standard value.'},
          {'q': 'Troposphere lapse rate is…', 'opts': ['6.5 K/km', '9.8 K/km', '0', '2 K/km'], 'ok': 0, 'why': 'ISA definition.'},
          {'q': 'The speed of sound depends on…', 'opts': ['pressure', 'temperature', 'density only', 'airspeed'], 'ok': 1, 'why': 'a = √(γRT).'},
          {'q': 'High density altitude makes takeoff…', 'opts': ['shorter', 'longer', 'unchanged', 'impossible'], 'ok': 1, 'why': 'Less lift and thrust.'}],
 'cards': [('ISA', '288.15 K, 101,325 Pa, 1.225 kg/m³.'), ('Lapse rate', '0.0065 K/m.'), ('Density ratio', 'σ = ρ/ρ₀.'), ('Speed of sound', '√(γRT).'), ('EAS', 'V√σ.'), ('Density altitude', 'ISA altitude with the actual density.')],
 'planet': {'text': ['EIA reports that about 29% of total U.S. energy use in 2025 went to transporting people and goods, that petroleum products supplied about 89% of transportation energy, and that jet fuel alone was 13% of transportation energy use.',
                     'EIA also notes that jet fuel powers jet airplanes and some helicopters, and that biofuels may be blended into jet fuel. Every one of those gallons is burned in the atmosphere modeled in this unit; where an aircraft flies in that atmosphere decides how much it burns.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_EIA]},
 'res': [(_CH11[0], _CH11[1], 'Free FAA chapter on density altitude and performance.'), ('NASA Glenn: Dynamic pressure', _G + 'dynamic-pressure/', 'Free NASA page.'),
         (_MIT[0], _MIT[1], 'MIT notes on the atmosphere.'), (_PHAK[0], _PHAK[1], 'Full FAA handbook.')]})
UNITS.append(
{'id': 'u2', 'title': 'Forces in Flight and the Drag Polar', 'weeks': 'Week 2',
 'summary': 'The four forces, steady level flight, lift and drag coefficients, parasite and induced drag, the parabolic drag polar C_D = C_D0 + KC_L², Oswald efficiency and aspect ratio, maximum lift-to-drag ratio, and drag in cruise.',
 'objectives': ['Write the equations of steady level flight.', 'Use the parabolic drag polar.', 'Find (L/D)max and the lift coefficient where it occurs.', 'Compute cruise drag for an airliner.'],
 'concepts': ['In steady level flight lift equals weight and thrust equals drag: L = W = ½ρV²SC_L and T = D = ½ρV²SC_D.',
              'Drag has two parts. Parasite (zero-lift) drag C_D0 comes from skin friction and pressure drag; induced drag KC_L² is the price of making lift, with K = 1/(πeAR) for aspect ratio AR and Oswald efficiency e.',
              'The drag polar C_D = C_D0 + KC_L² sets almost every performance number in this course.',
              'Lift-to-drag ratio L/D = C_L/C_D is the aircraft’s aerodynamic efficiency. It is largest when induced drag equals parasite drag: C_L* = √(C_D0/K) and (L/D)max = 1/(2√(KC_D0)).',
              'At (L/D)max the drag is smallest for a given weight: D_min = W/(L/D)max. Long thin wings (high AR) lower K, which is why gliders and the most efficient airliners have them.'],
 'eqs': [('L=W=\\tfrac12\\rho V^2SC_L', 'Level-flight lift'), ('C_D=C_{D0}+KC_L^2', 'Parabolic drag polar'), ('K=\\frac{1}{\\pi eAR}', 'Induced-drag factor'), ('\\left(\\frac LD\\right)_{max}=\\frac{1}{2\\sqrt{KC_{D0}}}', 'Best lift-to-drag ratio')],
 'worked': [
  {'q': 'The sample airliner has m = 60,000 kg, S = 120 m², C_D0 = 0.020 and K = 0.045. Find W, (L/D)max, C_L* and the minimum drag.', 'steps': ['W = 60,000 × 9.81 = 588.6 kN.', '(L/D)max = 1/(2√(0.045 × 0.020)) = 16.67.', 'C_L* = √(0.020/0.045) = 0.667.', 'D_min = 588,600/16.67.'], 'a': '(L/D)max = 16.67 at C_L = 0.667; D_min = 35.3 kN.'},
  {'q': 'The airliner cruises at 11 km (ρ = 0.364 kg/m³) at 230 m/s. Find q, C_L, C_D and drag.', 'steps': ['q = ½ × 0.3636 × 230² = 9618 Pa.', 'C_L = 588,600/(9618 × 120) = 0.510.', 'C_D = 0.020 + 0.045 × 0.510² = 0.0317.', 'D = 9618 × 120 × 0.0317.'], 'a': 'D = 36.6 kN; L/D = 16.1, close to the maximum.'},
  {'q': 'What is the cruise Mach number?', 'steps': ['M = 230/295.0.'], 'a': 'M = 0.780.'}],
 'practice': [('Halve C_D0 with K unchanged. How does (L/D)max change?', 'Rises by √2: 23.6.'), ('Find K for AR = 9 and e = 0.8.', '1/(π × 0.8 × 9) = 0.0442.'),
              ('At C_L*, what fraction of drag is induced?', 'Half.'), ('Find the cruise L/D above.', '0.510/0.0317 = 16.1.')],
 'misc': [('Drag always grows with speed.', 'Induced drag falls with speed; total drag has a minimum.'), ('Bigger wings always mean less drag.', 'They add parasite drag.'),
          ('L/D is fixed for an aircraft.', 'It depends on C_L, so on speed, weight and altitude.')],
 'quiz': [{'q': 'In steady level flight…', 'opts': ['L = W, T = D', 'L = T', 'D = W', 'L = 0'], 'ok': 0, 'why': 'Force balance.'},
          {'q': '(L/D)max occurs when…', 'opts': ['induced = parasite drag', 'C_L = 0', 'C_L = C_Lmax', 'V is maximum'], 'ok': 0, 'why': 'Minimize C_D/C_L.'},
          {'q': 'Raising aspect ratio…', 'opts': ['raises K', 'lowers K', 'raises C_D0', 'has no effect'], 'ok': 1, 'why': 'K = 1/(πeAR).'},
          {'q': 'D_min equals…', 'opts': ['W(L/D)max', 'W/(L/D)max', 'T_max', 'qS'], 'ok': 1, 'why': 'D = W/(L/D).'}],
 'cards': [('Level flight', 'L = W, T = D.'), ('Drag polar', 'C_D0 + KC_L².'), ('K', '1/(πeAR).'), ('C_L*', '√(C_D0/K).'), ('(L/D)max', '1/(2√(KC_D0)).'), ('D_min', 'W/(L/D)max.')],
 'planet': {'text': ['NASA describes the truss-braced wing as a long, thin wing with aerodynamically shaped structural supports that could reduce fuel and operating costs for future airliners. In December 2025, NASA and Boeing tested a semispan model of Boeing’s Subsonic Ultra Green Aircraft Research (SUGAR) concept in a large pressurized wind tunnel in Farnborough, England.',
                     'A long, thin wing is a high-aspect-ratio wing: it lowers K in the drag polar and raises (L/D)max. The struts carry the loads that would make such a wing too heavy on its own.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Mechanics of Materials', 'Mechanics_of_Materials.html')],
            'src': [_TBW]},
 'res': [('NASA Glenn: The drag equation', _G + 'drag-equation/', 'Free NASA page.'), ('NASA Glenn: Induced drag coefficient', _G + 'induced-drag-coefficient/', 'Free NASA page.'),
         ('NASA Glenn: Lift-to-drag ratio', _G + 'lift-to-drag-ratio/', 'Free NASA page.'), (_MITA[0], _MITA[1], 'MIT aerodynamics.')]})
UNITS.append(
{'id': 'u3', 'title': 'Thrust and Power Required', 'weeks': 'Week 3',
 'summary': 'Thrust required versus speed, the minimum-drag speed, power required and the minimum-power speed, thrust and power available from jets and propellers, maximum and minimum level speeds, and the effect of altitude and weight.',
 'objectives': ['Plot thrust and power required against speed.', 'Find the minimum-drag and minimum-power speeds.', 'Explain how altitude changes these speeds.', 'Find maximum level speed from thrust available.'],
 'concepts': ['Thrust required equals drag: T_R = ½ρV²SC_D0 + 2KW²/(ρV²S). The first term grows with V², the second falls as 1/V², so T_R has a minimum.',
              'The minimum-drag speed is V_md = √(2W/(ρS)) (K/C_D0)^¼. It is the speed for (L/D)max.',
              'Power required is P_R = T_R V. It is least at V_mp = V_md/3^¼ = 0.760 V_md, where induced drag is three times parasite drag and L/D = 0.866(L/D)max.',
              'At altitude, all speeds scale as 1/√σ at the same weight: the true speed for best L/D rises, but the drag is unchanged.',
              'Jet thrust is roughly constant with speed and falls with density; propeller power is roughly constant, so propeller thrust falls with speed. Maximum level speed is where available thrust (or power) meets required.'],
 'eqs': [('T_R=\\tfrac12\\rho V^2SC_{D0}+\\frac{2KW^2}{\\rho V^2S}', 'Thrust required'), ('V_{md}=\\sqrt{\\frac{2W}{\\rho S}}\\left(\\frac{K}{C_{D0}}\\right)^{1/4}', 'Minimum-drag speed'), ('V_{mp}=\\frac{V_{md}}{3^{1/4}}', 'Minimum-power speed'), ('P_R=T_RV', 'Power required')],
 'worked': [
  {'q': 'Find V_md for the sample airliner at sea level.', 'steps': ['√(2 × 588,600/(1.225 × 120)) = 89.5 m/s.', '(0.045/0.020)^¼ = 1.225.', 'V_md = 89.5 × 1.225.'], 'a': 'V_md = 109.6 m/s.'},
  {'q': 'Find V_md at 11 km and the speed ratio.', 'steps': ['Ratio = √(1.225/0.3636) = 1.835.', 'V_md = 109.6 × 1.835.'], 'a': 'V_md = 201.2 m/s at the same 35.3 kN drag.'},
  {'q': 'Find V_mp at sea level and the power required at V_md.', 'steps': ['V_mp = 109.6/1.316 = 83.3 m/s.', 'P_R(V_md) = 35,316 × 109.6.'], 'a': 'V_mp = 83.3 m/s; P_R at V_md = 3.87 MW.'}],
 'practice': [('Find the drag at V_mp.', 'W/(0.866 × 16.67) = 40.8 kN.'), ('Find q at 100 m/s at sea level.', '½ × 1.225 × 100² = 6125 Pa.'),
              ('If weight rises 21%, how does V_md change?', 'By √1.21 = 1.1 times.'), ('Below V_md, is the aircraft speed-stable?', 'No: slowing raises drag (the back side of the drag curve).')],
 'misc': [('Minimum drag and minimum power happen at the same speed.', 'V_mp is 24% slower.'), ('Flying higher lowers drag at best L/D.', 'Drag is the same; only the speed is higher.'),
          ('Thrust required is the same as power required.', 'Power = thrust × speed.')],
 'quiz': [{'q': 'Thrust required is lowest at…', 'opts': ['V_md', 'V_mp', 'V_stall', 'V_max'], 'ok': 0, 'why': 'Minimum drag.'},
          {'q': 'V_mp/V_md equals…', 'opts': ['0.760', '1.316', '1', '0.5'], 'ok': 0, 'why': '3^(−¼).'},
          {'q': 'At altitude, V_md (true) is…', 'opts': ['higher', 'lower', 'the same', 'zero'], 'ok': 0, 'why': '∝ 1/√ρ.'},
          {'q': 'Propeller thrust with speed…', 'opts': ['falls', 'rises', 'is constant', 'is zero'], 'ok': 0, 'why': 'Constant power.'}],
 'cards': [('Thrust required', 'Equals drag.'), ('V_md', 'Speed for (L/D)max.'), ('V_mp', '0.760 V_md.'), ('Power required', 'T_R V.'), ('Altitude', 'Speeds ∝ 1/√σ.'), ('Back side', 'Below V_md, drag rises as speed falls.')],
 'planet': {'text': ['NASA explains that during flight a thin layer of air, the boundary layer, forms very near an aircraft’s surface, and that on most aircraft it becomes turbulent, increasing friction drag and fuel use. NASA’s Crossflow Attenuated Natural Laminar Flow (CATNLF) design aims to keep that flow laminar on large swept wings.',
                     'A NASA computational study from 2014 to 2017 estimated that a CATNLF wing on a large, long-range aircraft like the Boeing 777 could save up to 10% of fuel a year. In this unit’s terms, laminar flow lowers C_D0, which lowers thrust and power required at every speed.'],
            'site': [('Fluid Mechanics', 'Fluid_Mechanics.html'), ('Aerodynamics I', 'Aerodynamics_I.html')],
            'src': [_CAT]},
 'res': [('NASA Glenn: What is drag?', _G + 'what-is-drag/', 'Free NASA page.'), ('NASA Glenn: Thrust-to-weight ratio', _G + 'thrust-to-weight-ratio/', 'Free NASA page.'),
         (_MIT[0], _MIT[1], 'MIT performance notes.'), (_CH11[0], _CH11[1], 'FAA chapter on thrust and power curves.')]})
UNITS.append(
{'id': 'u4', 'title': 'Climb Performance', 'weeks': 'Weeks 4–5',
 'summary': 'Forces in a steady climb, climb angle and rate of climb, excess thrust and excess power, best-angle and best-rate speeds, specific excess power, time to climb, and absolute and service ceilings.',
 'objectives': ['Write the force balance in a steady climb.', 'Compute rate and angle of climb.', 'Distinguish best-angle and best-rate speeds.', 'Estimate time to climb and ceilings.'],
 'concepts': ['In a steady climb at flight-path angle γ: T − D − W sin γ = 0 and L = W cos γ. So sin γ = (T − D)/W: excess thrust sets the climb angle.',
              'Rate of climb RC = V sin γ = (T − D)V/W = (P_avail − P_req)/W: excess power sets the climb rate.',
              'The best-angle speed (V_x) maximizes excess thrust and is used to clear obstacles; the best-rate speed (V_y) maximizes excess power and gets to altitude soonest.',
              'Specific excess power P_s = (T − D)V/W combines climb and acceleration: it is the rate at which energy height h + V²/(2g) can grow.',
              'Excess power falls with altitude. The absolute ceiling is where maximum RC is zero; the service ceiling is where it is 0.5 m/s (100 ft/min).'],
 'eqs': [('\\sin\\gamma=\\frac{T-D}{W}', 'Climb angle'), ('RC=\\frac{(T-D)V}{W}', 'Rate of climb'), ('P_s=\\frac{(T-D)V}{W}', 'Specific excess power'), ('h_E=h+\\frac{V^2}{2g}', 'Energy height')],
 'worked': [
  {'q': 'The sample airliner climbs at 130 m/s at sea level with 120 kN of thrust. Find C_L and drag.', 'steps': ['q = ½ × 1.225 × 130² = 10,351 Pa.', 'C_L = 588,600/(10,351 × 120) = 0.474.', 'D = 10,351 × 120 × (0.020 + 0.045 × 0.474²).'], 'a': 'C_L = 0.474; D = 37.4 kN (taking L ≈ W).'},
  {'q': 'Find the rate and angle of climb.', 'steps': ['RC = (120,000 − 37,394) × 130/588,600.', 'sin γ = 82,606/588,600.'], 'a': 'RC = 18.2 m/s (3590 ft/min); γ = 8.07°.'},
  {'q': 'At an average 10 m/s, how long does a climb to 10,000 m take?', 'steps': ['t = 10,000/10 = 1000 s.'], 'a': 't = 16.7 min.'}],
 'practice': [('Convert 18.2 m/s to ft/min.', '18.2 × 196.85 = 3590 ft/min.'), ('Which speed clears an obstacle best?', 'V_x, best angle.'),
              ('What is RC at the absolute ceiling?', 'Zero.'), ('Why does climb fall with altitude?', 'Thrust and excess power fall with density.')],
 'misc': [('Climb comes from extra lift.', 'It comes from excess thrust or power; in a climb L < W.'), ('V_x and V_y are the same.', 'V_x is slower.'),
          ('Climb rate is independent of weight.', 'RC ∝ 1/W.')],
 'quiz': [{'q': 'Climb angle depends on…', 'opts': ['excess thrust', 'excess lift', 'wing area only', 'Mach'], 'ok': 0, 'why': 'sin γ = (T − D)/W.'},
          {'q': 'Rate of climb depends on…', 'opts': ['excess power', 'drag only', 'C_Lmax', 'K only'], 'ok': 0, 'why': 'RC = ΔP/W.'},
          {'q': 'Service ceiling RC is…', 'opts': ['0', '0.5 m/s', '5 m/s', '10 m/s'], 'ok': 1, 'why': '100 ft/min.'},
          {'q': 'In a steady climb, lift is…', 'opts': ['W cos γ', 'W', 'W sin γ', 'T'], 'ok': 0, 'why': 'Normal balance.'}],
 'cards': [('Climb angle', 'sin γ = (T − D)/W.'), ('Rate of climb', '(T − D)V/W.'), ('V_x', 'Best angle.'), ('V_y', 'Best rate.'), ('P_s', 'Specific excess power.'), ('Ceilings', 'Absolute: RC = 0; service: 0.5 m/s.')],
 'planet': {'text': ['NASA’s sustainable aviation page notes that needing less energy to fly means using less fuel or, for electric aircraft, less power that must be generated elsewhere, which lowers lifecycle emissions for the whole time an aircraft is in use.',
                     'Climb is the most energy-hungry part of a short flight. Specific excess power shows why: every kilogram of weight saved and every newton of drag removed raises the climb rate and shortens the high-thrust phase.'],
            'site': [('Dynamics', 'Dynamics.html'), ('Solutions', 'Solutions.html')],
            'src': [_SUS]},
 'res': [(_CH11[0], _CH11[1], 'FAA chapter on climb performance.'), (_AFH[0], _AFH[1], 'FAA handbook on climbs.'),
         (_MIT[0], _MIT[1], 'MIT climb notes.'), ('NASA Glenn: Thrust-to-weight ratio', _G + 'thrust-to-weight-ratio/', 'Free NASA page.')]})
UNITS.append(
{'id': 'u5', 'title': 'Gliding Flight', 'weeks': 'Week 6',
 'summary': 'Forces in an unpowered glide, glide angle and glide ratio, distance from a given height, sink rate and minimum sink, the effect of weight and wind, and engine-out planning.',
 'objectives': ['Relate glide angle to L/D.', 'Find glide distance from a height.', 'Compute sink rate.', 'Explain the effects of weight and wind.'],
 'concepts': ['In a steady glide, thrust is zero: D = W sin γ and L = W cos γ, so tan γ = D/L = 1/(L/D).',
              'Glide distance from height h is d = h(L/D). The flattest glide is at (L/D)max, so at V_md.',
              'Sink rate V_s = V sin γ ≈ V/(L/D). Minimum sink occurs at the minimum-power speed V_mp, best for staying up longest.',
              'Weight does not change the best glide ratio, only the speed at which it happens (heavier gliders fly faster at the same angle). Headwind shortens the distance over the ground; tailwind lengthens it.',
              'NASA notes that the Wright brothers measured their gliders’ performance by flying parallel to a dune slope, so the glide angle equalled the slope of the hill.'],
 'eqs': [('\\tan\\gamma=\\frac{1}{L/D}', 'Glide angle'), ('d=h\\,(L/D)', 'Glide distance'), ('V_s\\approx\\frac{V}{L/D}', 'Sink rate'), ('D=W\\sin\\gamma', 'Glide force balance')],
 'worked': [
  {'q': 'The sample airliner loses all engines at 10 km. How far can it glide at (L/D)max = 16.67 in still air?', 'steps': ['d = 10,000 × 16.67.'], 'a': 'd = 166.7 km.'},
  {'q': 'A sailplane with L/D = 40 is 1000 m up. Find its glide distance and angle.', 'steps': ['d = 1000 × 40 = 40 km.', 'γ = arctan(1/40).'], 'a': '40 km at 1.43°.'},
  {'q': 'Find the sailplane’s sink rate at 30 m/s.', 'steps': ['V_s = 30/40.'], 'a': '0.75 m/s.'}],
 'practice': [('Find the sink rate at 25 m/s with L/D = 35.', '25/35 = 0.714 m/s.'), ('Does adding water ballast change the best glide ratio?', 'No, only the best-glide speed.'),
              ('Glide for longest time or farthest distance: which speed is which?', 'V_mp for time, V_md for distance.'), ('Glide angle with L/D = 10?', 'arctan(0.1) = 5.71°.')],
 'misc': [('Heavier gliders glide less far.', 'Same distance in still air, just faster.'), ('Pull the nose up to stretch a glide.', 'Below best-glide speed the glide gets steeper.'),
          ('Minimum sink and best glide are the same speed.', 'Minimum sink is slower.')],
 'quiz': [{'q': 'tan γ in a glide equals…', 'opts': ['L/D', 'D/L', 'W/L', 'T/W'], 'ok': 1, 'why': 'Force balance.'},
          {'q': 'Best glide distance is at…', 'opts': ['(L/D)max', 'C_Lmax', 'V_max', 'V_mp'], 'ok': 0, 'why': 'Flattest angle.'},
          {'q': 'Longest time aloft is at…', 'opts': ['V_mp', 'V_md', 'V_stall', 'V_max'], 'ok': 0, 'why': 'Minimum sink.'},
          {'q': 'Extra weight changes…', 'opts': ['best glide ratio', 'best glide speed', 'both equally', 'nothing'], 'ok': 1, 'why': 'Speed ∝ √W.'}],
 'cards': [('Glide angle', 'tan γ = 1/(L/D).'), ('Glide distance', 'h(L/D).'), ('Sink rate', 'V/(L/D).'), ('Best glide', 'At V_md.'), ('Minimum sink', 'At V_mp.'), ('Weight', 'Changes speed, not ratio.')],
 'planet': {'text': ['NASA’s Beginner’s Guide explains that the smaller the glide angle, the farther an aircraft can fly for a given change in altitude, so the glide angle is a measure of flying efficiency. The Wright brothers used gliders between 1900 and 1902 to learn aerodynamics and piloting before powered flight.',
                     'The glide ratio is just L/D, the same number that sets fuel burn in cruise. An aircraft that glides well also cruises on less fuel.'],
            'site': [('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html'), ('Aerodynamics I', 'Aerodynamics_I.html')],
            'src': [_GLD]},
 'res': [(_GLD[0], _GLD[1], 'Free NASA page.'), ('NASA Glenn: Lift-to-drag ratio', _G + 'lift-to-drag-ratio/', 'Free NASA page.'),
         (_AFH[0], _AFH[1], 'FAA handbook on emergency glides.'), (_MIT[0], _MIT[1], 'MIT notes.')]})
UNITS.append(
{'id': 'u6', 'title': 'Range and Endurance: the Breguet Equations', 'weeks': 'Weeks 7–8',
 'summary': 'Specific fuel consumption for jets and propellers, fuel weight fractions, the Breguet range and endurance equations, best-range and best-endurance speeds, cruise-climb, payload–range trade-offs and reserves.',
 'objectives': ['Use thrust- and power-specific fuel consumption.', 'Apply the Breguet range equation for jets and propeller aircraft.', 'Compute endurance.', 'Identify which design changes extend range.'],
 'concepts': ['A jet’s thrust-specific fuel consumption c is fuel weight burned per unit thrust per unit time (1/s). A piston or turboprop’s power-specific consumption is fuel per unit power per unit time.',
              'Integrating dW/dt = −cT with T = W/(L/D) at constant V and L/D gives the Breguet range for jets: R = (V/c)(L/D) ln(W_i/W_f).',
              'For propeller aircraft, with propeller efficiency η and power-specific consumption c_p (1/m): R = (η/c_p)(L/D) ln(W_i/W_f). Endurance for jets is E = (1/c)(L/D) ln(W_i/W_f).',
              'Range grows with three groups: engine efficiency (V/c or η/c_p), aerodynamics (L/D) and structures (the weight ratio). That is why the equation guides almost every aircraft improvement.',
              'Jets fly for best range a little faster than V_md (maximizing V·L/D) and for best endurance at V_md. Propeller aircraft fly for range at V_md and for endurance at V_mp.'],
 'eqs': [('R=\\frac{V}{c}\\frac{L}{D}\\ln\\frac{W_i}{W_f}', 'Breguet range, jet'), ('R=\\frac{\\eta}{c_p}\\frac{L}{D}\\ln\\frac{W_i}{W_f}', 'Breguet range, propeller'), ('E=\\frac{1}{c}\\frac{L}{D}\\ln\\frac{W_i}{W_f}', 'Endurance, jet'), ('c_p=\\frac{\\text{SFC}\\cdot g}{3.6\\times10^6}', 'SFC in kg/kWh to 1/m')],
 'worked': [
  {'q': 'A jet cruises at 230 m/s with c = 0.6 per hour and L/D = 16, burning fuel equal to 25% of its starting weight (W_f/W_i = 0.75). Find the range.', 'steps': ['c = 0.6/3600 = 1.667 × 10⁻⁴ s⁻¹.', 'ln(1/0.75) = 0.2877.', 'R = (230/1.667 × 10⁻⁴) × 16 × 0.2877.'], 'a': 'R = 6352 km.'},
  {'q': 'Find the endurance for the same aircraft.', 'steps': ['E = (1/1.667 × 10⁻⁴) × 16 × 0.2877 = 27,618 s.'], 'a': 'E = 7.67 h.'},
  {'q': 'A turboprop has η = 0.8, SFC = 0.3 kg/kWh, L/D = 15 and burns 15% of its weight (W_f/W_i = 0.85). Find the range.', 'steps': ['c_p = 0.3 × 9.81/3.6 × 10⁶ = 8.175 × 10⁻⁷ m⁻¹.', 'ln(1/0.85) = 0.1625.', 'R = (0.8/8.175 × 10⁻⁷) × 15 × 0.1625.'], 'a': 'R = 2386 km.'}],
 'practice': [('Raise L/D from 16 to 18 in the jet example. New range?', '7146 km (12.5% more).'), ('Burn 30% of the weight instead of 25%. Range?', 'ln(1/0.7) = 0.3567: 7875 km.'),
              ('Which term does a laminar-flow wing improve?', 'L/D.'), ('Which term does a lighter structure improve?', 'The weight ratio.')],
 'misc': [('Range is proportional to fuel carried.', 'It grows with the log of the weight ratio.'), ('Best range and best endurance are the same speed.', 'Endurance is flown slower.'),
          ('Breguet needs constant altitude.', 'It assumes constant V and L/D, which means a slow cruise-climb.')],
 'quiz': [{'q': 'Jet range is proportional to…', 'opts': ['V(L/D)/c', 'c/V', 'L/D only', 'W_f'], 'ok': 0, 'why': 'Breguet.'},
          {'q': 'The weight term in Breguet is…', 'opts': ['W_i − W_f', 'ln(W_i/W_f)', 'W_i/W_f', 'W_f/W_i'], 'ok': 1, 'why': 'Integration of dW/W.'},
          {'q': 'Jet endurance is best at…', 'opts': ['V_md', 'V_mp', 'V_max', 'V_stall'], 'ok': 0, 'why': 'Minimum drag = minimum fuel flow.'},
          {'q': 'Propeller range is best at…', 'opts': ['V_md', 'V_mp', 'V_max', 'Mach 1'], 'ok': 0, 'why': '(L/D)max.'}],
 'cards': [('TSFC', 'Fuel weight per thrust per time.'), ('Breguet jet', '(V/c)(L/D) ln(W_i/W_f).'), ('Breguet prop', '(η/c_p)(L/D) ln(W_i/W_f).'), ('Endurance', '(1/c)(L/D) ln(W_i/W_f).'), ('Three levers', 'Engine, aerodynamics, structures.'), ('Cruise-climb', 'Constant V and L/D as fuel burns.')],
 'planet': {'text': ['NASA and GE Aerospace tested an integrated hybrid-electric jet engine, a modified GE Passport, in December 2025 at GE Aerospace’s Peebles Test Operation site in Ohio. NASA’s Hybrid Thermally Efficient Core (HyTEC) project aims for a hybrid engine that burns up to 10% less fuel than today’s best-in-class engines.',
                     'In Breguet terms, a 10% lower fuel burn means a smaller c: the same flight on less fuel, or a longer flight on the same fuel. The engine term, the aerodynamics term and the structures term each give engineers a lever.'],
            'site': [('Thermodynamics', 'Thermodynamics.html'), ('Solutions', 'Solutions.html')],
            'src': [_HYB]},
 'res': [(_MIT[0], _MIT[1], 'MIT notes on the Breguet equation.'), (_MITS[0], _MITS[1], 'MIT aircraft systems.'),
         (_CH11[0], _CH11[1], 'FAA chapter on range and endurance.'), ('NASA Glenn: Lift-to-drag ratio', _G + 'lift-to-drag-ratio/', 'Free NASA page.')]})
UNITS.append(
{'id': 'u7', 'title': 'Takeoff Performance', 'weeks': 'Weeks 9–10',
 'summary': 'Stall speed and C_Lmax, high-lift devices, the takeoff ground roll, liftoff speed, the effect of weight, density altitude, wind and runway slope, the airborne segment over an obstacle, and balanced field length.',
 'objectives': ['Find stall and liftoff speeds.', 'Estimate takeoff ground roll.', 'Show how weight and density altitude lengthen takeoff.', 'Explain balanced field length.'],
 'concepts': ['Stall speed is the slowest steady flight speed: V_s = √(2W/(ρSC_Lmax)). Flaps and slats raise C_Lmax for takeoff and landing.',
              'Liftoff speed is typically V_LOF ≈ 1.2V_s, giving a margin above stall.',
              'With thrust much larger than drag and friction, the ground roll is about s_g ≈ 1.44W²/(gρSC_LmaxT).',
              'Takeoff distance therefore grows roughly with W², and with 1/ρ twice over for jets (through V_s and through lower thrust). A 10 kt headwind shortens the roll; a tailwind lengthens it a lot.',
              'Balanced field length is where, if an engine fails at the decision speed V₁, stopping and continuing need the same distance.'],
 'eqs': [('V_s=\\sqrt{\\frac{2W}{\\rho SC_{L,max}}}', 'Stall speed'), ('V_{LOF}\\approx1.2V_s', 'Liftoff speed'), ('s_g\\approx\\frac{1.44W^2}{g\\rho SC_{L,max}T}', 'Ground roll'), ('\\frac{s_2}{s_1}=\\left(\\frac{W_2}{W_1}\\right)^2', 'Weight effect')],
 'worked': [
  {'q': 'The sample airliner has C_Lmax = 2.4 with takeoff flaps at sea level. Find V_s and V_LOF.', 'steps': ['V_s = √(2 × 588,600/(1.225 × 120 × 2.4)).', 'V_LOF = 1.2 × 57.8.'], 'a': 'V_s = 57.8 m/s; V_LOF = 69.3 m/s.'},
  {'q': 'Estimate the ground roll with 180 kN thrust.', 'steps': ['s_g = 1.44 × 588,600²/(9.81 × 1.225 × 120 × 2.4 × 180,000).'], 'a': 's_g = 801 m.'},
  {'q': 'Repeat at a 1500 m airport (ISA ρ = 1.058 kg/m³), same thrust.', 'steps': ['s_g = 801 × 1.225/1.058.'], 'a': 's_g = 927 m, 1.158 times longer (more with the real thrust loss).'}],
 'practice': [('The aircraft is loaded to 70,000 kg. Ratio of ground rolls?', '(70/60)² = 1.361.'), ('Stall speed ratio at 70,000 kg?', '√(70/60) = 1.080.'),
              ('Why do flaps shorten takeoff?', 'Higher C_Lmax, lower V_s.'), ('What is V₁?', 'The decision speed for a rejected or continued takeoff.')],
 'misc': [('Takeoff distance is proportional to weight.', 'Closer to weight squared.'), ('A hot day only affects engines.', 'It also lowers lift at a given speed.'),
          ('Liftoff happens at stall speed.', 'A margin above stall, about 1.2V_s.')],
 'quiz': [{'q': 'Stall speed scales with…', 'opts': ['√W', 'W', 'W²', '1/W'], 'ok': 0, 'why': 'V_s ∝ √(W/ρ).'},
          {'q': 'Ground roll scales roughly with…', 'opts': ['W', 'W²', '√W', '1/W'], 'ok': 1, 'why': 's_g ∝ W²/(ρT).'},
          {'q': 'Flaps raise…', 'opts': ['C_Lmax', 'C_D0 only', 'Mach', 'K only'], 'ok': 0, 'why': 'High-lift devices.'},
          {'q': 'Balanced field length equalizes…', 'opts': ['stop and go distances', 'V₁ and V₂', 'thrust and drag', 'L and W'], 'ok': 0, 'why': 'Definition.'}],
 'cards': [('Stall speed', '√(2W/(ρSC_Lmax)).'), ('V_LOF', '≈ 1.2V_s.'), ('Ground roll', '1.44W²/(gρSC_LmaxT).'), ('Weight effect', '∝ W².'), ('Density altitude', 'Longer roll.'), ('V₁', 'Decision speed.')],
 'planet': {'text': ['NASA and Boeing’s truss-braced wing model included slats, flaps and other moving surfaces so the team could set it to the low-speed, high-lift settings of takeoff and landing. NASA notes that the pressurized QinetiQ tunnel is used to predict airplane behavior in takeoff and landing conditions.',
                     'A very efficient cruise wing still has to meet this unit’s stall and runway numbers, which is why high-lift performance is tested as early as cruise drag.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Statics', 'Statics.html')],
            'src': [_TBW]},
 'res': [(_AFH[0], _AFH[1], 'FAA handbook on takeoffs.'), (_CH11[0], _CH11[1], 'FAA chapter on takeoff performance charts.'),
         (_CH10[0], _CH10[1], 'FAA chapter on weight and balance.'), ('NASA Glenn: The lift equation', _G + 'lift-equation/', 'Free NASA page.')]})
UNITS.append(
{'id': 'u8', 'title': 'Landing Performance', 'weeks': 'Week 11',
 'summary': 'The approach, flare and ground roll, approach speed, braking, reverse thrust and spoilers, runway condition, landing distance estimates and the energy that must be removed.',
 'objectives': ['Find approach speed from stall speed.', 'Estimate landing ground roll from deceleration.', 'Explain how runway condition and spoilers matter.', 'Compute the kinetic energy at touchdown.'],
 'concepts': ['Landing has three segments: the approach over a 15 m (50 ft) obstacle, the flare and the ground roll.',
              'Approach speed is typically V_app ≈ 1.3V_s in the landing configuration.',
              'With an average deceleration a, the ground roll is s = V²/(2a). Brakes, spoilers (which dump lift so the wheels can brake) and reverse thrust all raise a.',
              'Wet or icy runways lower friction and can greatly lengthen the roll; performance charts give corrections.',
              'The kinetic energy at touchdown ½mV² must be absorbed, mostly as heat in the brakes.'],
 'eqs': [('V_{app}\\approx1.3V_s', 'Approach speed'), ('s=\\frac{V^2}{2a}', 'Ground roll'), ('E_k=\\tfrac12mV^2', 'Kinetic energy'), ('a=\\mu g', 'Ideal braking deceleration')],
 'worked': [
  {'q': 'With landing flaps, C_Lmax = 2.8. Find V_s and V_app for the sample airliner at sea level.', 'steps': ['V_s = √(2 × 588,600/(1.225 × 120 × 2.8)) = 53.5 m/s.', 'V_app = 1.3 × 53.5.'], 'a': 'V_s = 53.5 m/s; V_app = 69.5 m/s.'},
  {'q': 'Estimate the ground roll from 69.5 m/s at an average 0.4g.', 'steps': ['s = 69.5²/(2 × 0.4 × 9.81).'], 'a': 's = 616 m.'},
  {'q': 'Find the kinetic energy at 69.5 m/s.', 'steps': ['E = ½ × 60,000 × 69.5².'], 'a': 'E = 145 MJ.'}],
 'practice': [('Halve the deceleration. New ground roll?', 'Doubles: 1232 m.'), ('Why deploy spoilers at touchdown?', 'They dump lift so the brakes work.'),
              ('Approach 10% fast: change in roll?', '1.1² = 1.21, 21% longer.'), ('What is the approach obstacle height?', '15 m (50 ft).')],
 'misc': [('Landing distance is just the ground roll.', 'It includes the approach and flare.'), ('A few knots fast doesn’t matter.', 'Roll grows with V².'),
          ('Brakes work fully at touchdown.', 'Not until lift is dumped.')],
 'quiz': [{'q': 'V_app is about…', 'opts': ['1.3V_s', 'V_s', '2V_s', '0.8V_s'], 'ok': 0, 'why': 'Margin above stall.'},
          {'q': 'Ground roll with deceleration a is…', 'opts': ['V²/(2a)', 'Va', 'V/a', '2aV'], 'ok': 0, 'why': 'Kinematics.'},
          {'q': 'Spoilers help braking by…', 'opts': ['dumping lift', 'adding thrust', 'raising C_Lmax', 'cooling brakes'], 'ok': 0, 'why': 'More weight on wheels.'},
          {'q': '10% faster approach lengthens roll by…', 'opts': ['10%', '21%', '5%', '0%'], 'ok': 1, 'why': 'V².'}],
 'cards': [('V_app', '≈ 1.3V_s.'), ('Ground roll', 'V²/(2a).'), ('Spoilers', 'Dump lift.'), ('Reverse thrust', 'Extra deceleration.'), ('Wet runway', 'Longer roll.'), ('Brake energy', '½mV².')],
 'planet': {'text': ['NASA lists operations and infrastructure as one of the three main ways to make aviation sustainable: using less energy on the ground or by choice of flight path reduces fuel burned and saves money.',
                     'Approach and landing are part of that. A well-planned continuous descent and a landing at the right speed use less fuel and less braking energy than a rushed, fast approach.'],
            'site': [('Dynamics', 'Dynamics.html'), ('Solutions', 'Solutions.html')],
            'src': [_SUS]},
 'res': [(_AFH[0], _AFH[1], 'FAA handbook on approaches and landings.'), (_CH11[0], _CH11[1], 'FAA chapter on landing performance charts.'),
         (_MIT[0], _MIT[1], 'MIT notes.'), ('PhET: Projectile Motion', _PH + 'projectile-motion', 'Kinematics interactively.')]})
UNITS.append(
{'id': 'u9', 'title': 'Turning Flight and the V-n Diagram', 'weeks': 'Weeks 12–13',
 'summary': 'Level coordinated turns, bank angle and load factor, turn radius and rate, stall speed in a turn, maneuvering speed, the V-n diagram with limit load factors and gust loads, and pull-ups.',
 'objectives': ['Relate bank angle to load factor.', 'Compute turn radius and rate.', 'Find stall speed in a turn and maneuvering speed.', 'Read a V-n diagram.'],
 'concepts': ['In a level coordinated turn, lift tilts with the bank angle φ: L cos φ = W and L sin φ = mV²/R. The load factor n = L/W = 1/cos φ.',
              'Turn radius R = V²/(g√(n² − 1)) = V²/(g tan φ); turn rate ω = V/R.',
              'Stall speed rises with load factor: V_s,turn = V_s√n. At 60° bank, n = 2 and stall speed is 41% higher.',
              'Maneuvering speed V_A = V_s√n_limit is the speed at which full control deflection stalls the wing before the limit load is reached.',
              'The V-n diagram plots allowed load factor against speed: stall curves bound the left, limit load factors the top and bottom, and dive speed the right. Gust lines add the loads from turbulence.'],
 'eqs': [('n=\\frac{1}{\\cos\\phi}', 'Load factor in a level turn'), ('R=\\frac{V^2}{g\\tan\\phi}', 'Turn radius'), ('\\omega=\\frac{V}{R}', 'Turn rate'), ('V_{s,n}=V_s\\sqrt n', 'Stall speed under load')],
 'worked': [
  {'q': 'Find n, turn radius and turn rate at 100 m/s for 30°, 45° and 60° bank.', 'steps': ['n = 1/cos φ = 1.155, 1.414, 2.00.', 'R = 100²/(9.81 tan φ) = 1766 m, 1019 m, 589 m.', 'ω = V/R.'], 'a': 'Turn rates 3.25°/s, 5.62°/s and 9.74°/s.'},
  {'q': 'How much does stall speed rise at 30°, 45° and 60° bank?', 'steps': ['√n = 1.075, 1.189, 1.414.'], 'a': '7.5%, 18.9% and 41.4%.'},
  {'q': 'A light aircraft has V_s = 50 m/s and n_limit = 2.5. Find V_A.', 'steps': ['V_A = 50 × √2.5.'], 'a': 'V_A = 79.1 m/s.'}],
 'practice': [('Find the turn radius at 60 m/s and 30° bank.', '60²/(9.81 × tan 30°) = 636 m.'), ('Bank angle for n = 2?', '60°.'),
              ('Why do airliners use about 25–30° bank?', 'Comfortable load factor, small stall-speed rise.'), ('What bounds the left of the V-n diagram?', 'The stall curve n = (V/V_s)².')],
 'misc': [('A steeper bank makes a tighter turn at no cost.', 'It raises load factor and stall speed.'), ('Maneuvering speed is a maximum cruise speed.', 'It protects against full control inputs.'),
          ('Load factor depends only on speed.', 'It depends on bank angle in a level turn.')],
 'quiz': [{'q': 'Load factor at 60° bank is…', 'opts': ['1.15', '1.41', '2', '3'], 'ok': 2, 'why': '1/cos 60°.'},
          {'q': 'Turn radius is…', 'opts': ['V²/(g tan φ)', 'gV', 'V/g', 'V tan φ'], 'ok': 0, 'why': 'Centripetal balance.'},
          {'q': 'Stall speed in a turn is…', 'opts': ['V_s√n', 'V_s n', 'V_s/n', 'V_s'], 'ok': 0, 'why': 'More lift needed.'},
          {'q': 'The V-n diagram shows…', 'opts': ['allowed loads vs speed', 'drag vs speed', 'range vs fuel', 'altitude vs time'], 'ok': 0, 'why': 'Flight envelope.'}],
 'cards': [('Load factor', 'n = L/W = 1/cos φ.'), ('Turn radius', 'V²/(g tan φ).'), ('Turn rate', 'V/R.'), ('Stall in turn', 'V_s√n.'), ('V_A', 'V_s√n_limit.'), ('V-n diagram', 'Flight envelope.')],
 'planet': {'text': ['NASA’s 2026 CATNLF flight tests mounted a roughly 3-foot (40-inch) scale wing model vertically under an F-15B research jet. The first flight, on January 29, 2026, lasted 75 minutes and confirmed the aircraft could maneuver safely with the test article attached.',
                     'NASA says the first flight focused on envelope expansion, with turns, steady holds and gentle pitch changes between about 20,000 and nearly 34,000 feet, and that it was the first of up to 15 planned flights. Expanding an envelope step by step is the V-n diagram of this unit put into practice.'],
            'site': [('Dynamics', 'Dynamics.html'), ('Mechanics of Materials', 'Mechanics_of_Materials.html')],
            'src': [_CATF]},
 'res': [(_AFH[0], _AFH[1], 'FAA handbook on turns and maneuvers.'), (_CH11[0], _CH11[1], 'FAA chapter on load factors.'),
         (_MIT[0], _MIT[1], 'MIT notes.'), (_MITS[0], _MITS[1], 'MIT aircraft systems.')]})
UNITS.append(
{'id': 'u10', 'title': 'Performance of Electric, Hybrid and Sustainable-Fuel Aircraft', 'weeks': 'Weeks 14–15',
 'summary': 'Range of battery-electric aircraft, why weight does not fall as batteries discharge, specific energy of batteries versus jet fuel, hybrid-electric engines, sustainable aviation fuel, CO₂ from fuel burn, and putting all the performance levers together.',
 'objectives': ['Derive the range equation for a battery-electric aircraft.', 'Compare the specific energy of batteries and jet fuel.', 'Compute CO₂ from fuel burned.', 'Rank technologies by which Breguet term they improve.'],
 'concepts': ['A battery-electric aircraft does not get lighter as it flies, so there is no logarithm: R = (e_b η/g)(L/D)(m_b/m), with battery specific energy e_b (J/kg), total efficiency η and battery mass fraction m_b/m.',
              'Jet fuel holds about 43 MJ/kg (about 11,900 Wh/kg, a textbook value). Batteries of about 250 Wh/kg (a sample value) hold roughly 48 times less per kilogram, which is why electric aircraft today are small and short-range.',
              'Hybrid-electric engines use electric motors to help a jet engine run more efficiently, lowering the specific fuel consumption c.',
              'Burning a kilogram of jet fuel makes about 3.16 kg of CO₂ (a textbook value). Fuel saved by better L/D, lighter structures or better engines cuts CO₂ in direct proportion.',
              'Sustainable aviation fuel (SAF) has properties similar to conventional jet fuel, so it does not change the performance equations; it changes where the carbon comes from.'],
 'eqs': [('R=\\frac{e_b\\eta}{g}\\frac{L}{D}\\frac{m_b}{m}', 'Battery-electric range'), ('m_{CO_2}\\approx3.16\\,m_{fuel}', 'CO₂ from jet fuel'), ('\\frac{e_{fuel}}{e_b}=\\frac{43\\ \\text{MJ/kg}}{e_b}', 'Specific-energy ratio'), ('R=\\frac{V}{c}\\frac{L}{D}\\ln\\frac{W_i}{W_f}', 'Breguet, for comparison')],
 'worked': [
  {'q': 'An electric aircraft has 250 Wh/kg batteries (sample value), η = 0.8, L/D = 15 and a 30% battery fraction. Find its range.', 'steps': ['e_b = 250 × 3600 = 900,000 J/kg.', 'R = (900,000 × 0.8/9.81) × 15 × 0.3.'], 'a': 'R = 330 km.'},
  {'q': 'How much more energy per kilogram does jet fuel hold?', 'steps': ['43 × 10⁶/3600 = 11,944 Wh/kg.', '11,944/250.'], 'a': 'About 47.8 times.'},
  {'q': 'How much CO₂ comes from burning 1000 kg of jet fuel?', 'steps': ['3.16 × 1000.'], 'a': '3160 kg.'}],
 'practice': [('Repeat the electric range with 400 Wh/kg cells.', '528 km.'), ('An aircraft burns 2500 kg of fuel per hour. CO₂ per hour?', '7900 kg.'),
              ('Which Breguet term does a hybrid engine improve?', 'c, the fuel consumption.'), ('Why is there no logarithm in the battery range equation?', 'Mass stays constant.')],
 'misc': [('Electric aircraft get lighter as they fly.', 'Battery mass stays the same.'), ('SAF needs new engines.', 'It is designed to work in existing aircraft.'),
          ('Only engines matter for emissions.', 'Aerodynamics, weight and operations all count.')],
 'quiz': [{'q': 'Battery-electric range is proportional to…', 'opts': ['e_b(L/D)(m_b/m)', 'ln(W_i/W_f)', 'c', 'V/c'], 'ok': 0, 'why': 'Constant mass.'},
          {'q': 'Jet fuel vs 250 Wh/kg battery holds about…', 'opts': ['2×', '10×', '48×', '500×'], 'ok': 2, 'why': '11,944/250.'},
          {'q': 'CO₂ per kg of jet fuel is about…', 'opts': ['1 kg', '3.16 kg', '10 kg', '0.5 kg'], 'ok': 1, 'why': 'Carbon plus oxygen.'},
          {'q': 'SAF changes…', 'opts': ['the carbon source', 'L/D', 'stall speed', 'K'], 'ok': 0, 'why': 'Similar fuel properties.'}],
 'cards': [('Electric range', '(e_bη/g)(L/D)(m_b/m).'), ('Jet fuel', '≈ 43 MJ/kg.'), ('Battery', '≈ 250 Wh/kg (sample).'), ('CO₂', '≈ 3.16 kg per kg fuel.'), ('Hybrid engine', 'Lowers c.'), ('SAF', 'Drop-in fuel from biomass and wastes.')],
 'planet': {'text': ['DOE says sustainable aviation fuel made from biomass and waste resources can deliver performance similar to petroleum jet fuel. DOE’s 2023 Billion-Ton Report concluded that the United States could triple its biomass production to more than 1 billion tons a year, producing an estimated 60 billion gallons of liquid biofuels, enough feedstock to meet the projected fuel demand of U.S. aviation.',
                     'NASA notes that SAF does not release new CO₂ into the environment and has been shown to reduce contrails that can trap heat in Earth’s atmosphere. NASA also estimates that with today’s fleet and efficiency, worldwide air traffic in 2050 would need more than 620 megatons of fuel and produce close to 2,000 megatons of CO₂; the United States has committed to net-zero greenhouse gas emissions from U.S. aviation by 2050.'],
            'site': [('Solutions', 'Solutions.html'), ('Thermodynamics', 'Thermodynamics.html')],
            'src': [_SAF, _SUS]},
 'res': [(_SAF[0], _SAF[1], 'DOE overview of SAF.'), (_SUS[0], _SUS[1], 'NASA overview of sustainable aviation.'),
         (_HYB[0], _HYB[1], 'NASA hybrid engine test.'), (_MITS[0], _MITS[1], 'MIT aircraft systems.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Build a standard-atmosphere calculator', 'week': 'Week 1',
 'goal': 'Build a spreadsheet of ISA temperature, density and speed of sound from sea level to 11 km.',
 'eq': ('T=T_0-0.0065h,\\ \\ \\rho=\\rho_0(T/T_0)^{4.26},\\ \\ a=\\sqrt{\\gamma RT}', 'Troposphere model'),
 'steps': ['Make a column of altitudes every 500 m from 0 to 11,000 m.', 'Compute T, then ρ with the exponent 9.81/(0.0065 × 287) − 1.', 'Compute a = √(1.4 × 287 × T).', 'Plot ρ and a against altitude and compare with the values in Unit 1.'],
 'table': (['Altitude (m)', 'T (K)', 'ρ (kg/m³)', 'a (m/s)'], [['0', '288.15', '1.225', '340.3'], ['3000', '268.65', '0.909', '328.5'], ['5000', '255.65', '0.736', '320.5'], ['11,000', '216.65', '0.364', '295.0']]),
 'note': 'Computed ISA values.',
 'calc': ['ρ(3000) = 1.225 × (268.65/288.15)^4.26 = 0.909 kg/m³.', 'a(5000) = √(1.4 × 287 × 255.65) = 320.5 m/s.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('NASA Glenn: Dynamic pressure', _G + 'dynamic-pressure/'), (_MIT[0], _MIT[1])],
 'planet': 'EIA reports jet fuel was 13% of U.S. transportation energy use in 2025.', 'planet_src': [_EIA]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Paper glider glide ratio', 'week': 'Week 6',
 'goal': 'Measure the glide ratio of a paper glider from its launch height and flight distance, and find its glide angle and sink rate.',
 'eq': ('\\frac LD=\\frac dh,\\ \\ \\gamma=\\arctan\\frac hd', 'Glide ratio and angle'),
 'steps': ['Fold a simple glider from printer paper; add a paper clip at the nose to trim it.', 'In a clear space, release it gently (no throw) from a measured height, about 1.5 m.', 'Measure where it lands and time the flight; repeat five times and average.', 'Move the paper clip and see how the glide ratio changes.'],
 'table': (['Quantity', 'Value'], [['Release height', '1.5 m'], ['Distance', '6.0 m'], ['Glide ratio', '4.0'], ['Glide angle', '14.0°'], ['Flight time', '2.0 s'], ['Average speed', '3.09 m/s']]),
 'note': 'Sample values; real paper gliders have far lower L/D than sailplanes.',
 'calc': ['L/D = 6.0/1.5 = 4.0; γ = arctan(1.5/6.0) = 14.0°.', 'Speed along the path = √(6² + 1.5²)/2.0 = 3.09 m/s; sink rate = 1.5/2.0 = 0.75 m/s.'],
 'safety': ['Fly only in a clear space, never toward people’s faces; keep walkways clear.', 'Do not stand on chairs or stairs to launch; use your standing height.'], 'home': ['This is a home lab.'],
 'sims': [(_GLD[0], _GLD[1]), ('PhET: Projectile Motion', _PH + 'projectile-motion')],
 'planet': 'NASA notes the Wright brothers studied gliders from 1900 to 1902 and used glide angle to measure performance.', 'planet_src': [_GLD]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Measuring a drag polar in FoilSim', 'week': 'Week 2',
 'goal': 'Collect lift and drag coefficients at several angles of attack, fit a parabolic drag polar and find (L/D)max.',
 'eq': ('C_D=C_{D0}+KC_L^2', 'Parabolic drag polar'),
 'steps': ['Open NASA FoilSim and choose a wing shape and speed.', 'Record C_L and C_D at five angles of attack.', 'Plot C_D against C_L² and fit a straight line: the intercept is C_D0 and the slope is K.', 'Compute (L/D)max = 1/(2√(KC_D0)).'],
 'table': (['C_L', 'C_D', 'L/D'], [['0.2', '0.0218', '9.17'], ['0.6', '0.0362', '16.6'], ['1.0', '0.0650', '15.4']]),
 'note': 'Sample values generated from the course polar (C_D0 = 0.020, K = 0.045); your FoilSim numbers will differ.',
 'calc': ['C_D(0.6) = 0.020 + 0.045 × 0.36 = 0.0362.', '(L/D)max = 1/(2√(0.045 × 0.020)) = 16.67 at C_L = 0.667.'],
 'safety': ['Computer only.'], 'home': ['Any browser works.'],
 'sims': [('NASA Glenn: FoilSim', _G + 'foilsim/'), ('NASA Glenn: Induced drag coefficient', _G + 'induced-drag-coefficient/')],
 'planet': 'NASA’s CATNLF wing aims to keep laminar flow on swept wings, lowering C_D0.', 'planet_src': [_CAT]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Breguet range trade study', 'week': 'Week 8',
 'goal': 'Use a spreadsheet to see how L/D, fuel consumption and fuel fraction change a jet’s range.',
 'eq': ('R=\\frac{V}{c}\\frac{L}{D}\\ln\\frac{W_i}{W_f}', 'Breguet range'),
 'steps': ['Enter V = 230 m/s, c = 0.6 per hour and W_f/W_i = 0.75.', 'Compute range for L/D = 14, 16 and 18.', 'Then cut c by 10% and compare.', 'Rank the changes by kilometres gained.'],
 'table': (['L/D', 'Range (km)'], [['14', '5558'], ['16', '6352'], ['18', '7146']]),
 'note': 'Computed values for a sample jet.',
 'calc': ['R(14) = (230/1.667 × 10⁻⁴) × 14 × 0.2877 = 5558 km.', 'Cutting c by 10% multiplies range by 1/0.9 = 1.111.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MIT[0], _MIT[1])],
 'planet': 'NASA’s HyTEC project targets a hybrid engine burning up to 10% less fuel than today’s best engines.', 'planet_src': [_HYB]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Takeoff distance and density altitude', 'week': 'Week 10',
 'goal': 'Compute how takeoff ground roll grows with airport elevation and aircraft weight.',
 'eq': ('s_g\\approx\\frac{1.44W^2}{g\\rho SC_{L,max}T}', 'Ground roll'),
 'steps': ['Use the sample airliner: W = 588.6 kN, S = 120 m², C_Lmax = 2.4, T = 180 kN.', 'Compute s_g at 0, 1500 and 3000 m ISA density, holding thrust constant.', 'Repeat at 70,000 kg.', 'Discuss why real jets lose even more because thrust also falls.'],
 'table': (['Elevation (m)', 'ρ (kg/m³)', 'Ground roll (m)'], [['0', '1.225', '801'], ['1500', '1.058', '927'], ['3000', '0.909', '1079']]),
 'note': 'Computed values with constant thrust (a simplification).',
 'calc': ['s_g(0) = 1.44 × 588,600²/(9.81 × 1.225 × 120 × 2.4 × 180,000) = 801 m.', 's_g(3000) = 801 × 1.225/0.909 = 1079 m.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_CH11[0], _CH11[1]), (_AFH[0], _AFH[1])],
 'planet': 'NASA notes truss-braced wing models are tested in takeoff and landing high-lift settings.', 'planet_src': [_TBW]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Turn performance table', 'week': 'Week 13',
 'goal': 'Build a table of load factor, turn radius and stall-speed increase against bank angle.',
 'eq': ('n=\\frac{1}{\\cos\\phi},\\ \\ R=\\frac{V^2}{g\\tan\\phi}', 'Level-turn relations'),
 'steps': ['Set V = 100 m/s.', 'Compute n and R for bank angles from 15° to 60°.', 'Add √n for the stall-speed increase.', 'Mark the bank angle where stall speed rises 10%.'],
 'table': (['Bank', 'n', 'R (m)'], [['15°', '1.035', '3804'], ['30°', '1.155', '1766'], ['45°', '1.414', '1019'], ['60°', '2.000', '589']]),
 'note': 'Computed values.',
 'calc': ['R(15°) = 100²/(9.81 × tan 15°) = 3804 m.', 'n(60°) = 1/cos 60° = 2.000.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_AFH[0], _AFH[1])],
 'planet': 'NASA’s first CATNLF flight included turns and holds from about 20,000 to nearly 34,000 feet.', 'planet_src': [_CATF]})
SCHEDULE = [(1, 'u1', 'Standard atmosphere, airspeeds, density altitude; Lab A', 'FAA PHAK Ch. 11'), (2, 'u2', 'Forces in flight and the drag polar; Lab C', 'NASA Glenn; MIT 16.01'),
            (3, 'u3', 'Thrust and power required', 'MIT 16.01'), (4, 'u4', 'Climb angle and rate', 'FAA PHAK Ch. 11'),
            (5, 'u4', 'Specific excess power, ceilings, time to climb', 'MIT 16.01'), (6, 'u5', 'Gliding flight; Lab B', 'NASA Glenn'),
            (7, 'u6', 'Fuel consumption and the Breguet range equation', 'MIT 16.885J'), (8, 'u6', 'Endurance, payload–range; Lab D; midterm practice', 'MIT 16.885J'),
            (9, 'u7', 'Stall speed, high lift, ground roll', 'FAA Airplane Flying Handbook'), (10, 'u7', 'Density altitude, wind, balanced field; Lab E', 'FAA PHAK Ch. 11'),
            (11, 'u8', 'Approach and landing distance', 'FAA Airplane Flying Handbook'), (12, 'u9', 'Turns, load factor, turn radius', 'FAA Airplane Flying Handbook'),
            (13, 'u9', 'Maneuvering speed and the V-n diagram; Lab F', 'MIT 16.01'), (14, 'u10', 'Electric and hybrid aircraft performance', 'NASA HyTEC'),
            (15, 'u10', 'Sustainable fuel, CO₂ and the full performance picture; final practice', 'DOE SAF; NASA')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Find the ISA temperature at 2000 m.', ['288.15 − 0.0065 × 2000.'], '275.15 K.'),
  ('Find the ISA density at 2000 m.', ['1.225 × (275.15/288.15)^4.26.'], '1.006 kg/m³.'),
  ('Find (L/D)max for C_D0 = 0.025 and K = 0.040.', ['1/(2√(0.04 × 0.025)).'], '15.81.'),
  ('An aircraft weighing 500 kN has 50 kN excess thrust at 120 m/s. Find the rate of climb.', ['50,000 × 120/500,000.'], '12.0 m/s.'),
  ('How far can an aircraft with L/D = 12 glide from 2000 m?', ['2000 × 12.'], '24 km.')]),
 ('Final practice set (all units)', [
  ('Find the range of a jet with V = 240 m/s, c = 0.55 per hour, L/D = 17 and W_f/W_i = 0.8.', ['(240/(0.55/3600)) × 17 × ln 1.25.'], '5959 km.'),
  ('Find the sea-level stall speed for W = 100 kN, S = 30 m², C_Lmax = 1.8.', ['√(2 × 100,000/(1.225 × 30 × 1.8)).'], '55.0 m/s.'),
  ('Takeoff weight rises 20%. Ratio of ground rolls?', ['1.2².'], '1.44.'),
  ('Find the landing roll from 60 m/s at 3 m/s².', ['60²/(2 × 3).'], '600 m.'),
  ('Find the turn radius at 80 m/s and 45° bank.', ['80²/(9.81 × tan 45°).'], '652 m.'),
  ('Find the range of an electric aircraft with 300 Wh/kg, η = 0.85, L/D = 18 and a 35% battery fraction.', ['(300 × 3600 × 0.85/9.81) × 18 × 0.35.'], '590 km.')])]
FORMULAS = ['T=T_0-0.0065h,\\ \\rho/\\rho_0=(T/T_0)^{4.26},\\ a=\\sqrt{\\gamma RT}', 'L=W=\\tfrac12\\rho V^2SC_L,\\ C_D=C_{D0}+KC_L^2,\\ K=1/(\\pi eAR)', '(L/D)_{max}=1/(2\\sqrt{KC_{D0}}),\\ C_L^*=\\sqrt{C_{D0}/K}',
            'V_{md}=\\sqrt{2W/(\\rho S)}(K/C_{D0})^{1/4},\\ V_{mp}=V_{md}/3^{1/4}', '\\sin\\gamma=(T-D)/W,\\ RC=(T-D)V/W', '\\tan\\gamma_{glide}=1/(L/D),\\ d=h(L/D)',
            'R=(V/c)(L/D)\\ln(W_i/W_f),\\ E=(1/c)(L/D)\\ln(W_i/W_f)', 'V_s=\\sqrt{2W/(\\rho SC_{L,max})},\\ s_g\\approx1.44W^2/(g\\rho SC_{L,max}T)', 's=V^2/(2a),\\ V_{app}\\approx1.3V_s',
            'n=1/\\cos\\phi,\\ R=V^2/(g\\tan\\phi),\\ V_A=V_s\\sqrt{n_{lim}}', 'R_{elec}=(e_b\\eta/g)(L/D)(m_b/m)']
GLOSSARY = sorted([('Absolute ceiling', 'Altitude where the maximum rate of climb is zero.'), ('Balanced field length', 'Runway length where stopping and continuing after an engine failure need the same distance.'),
    ('Breguet equation', 'Range or endurance from engine efficiency, L/D and weight ratio.'), ('Density altitude', 'ISA altitude with the same air density as the actual air.'), ('Drag polar', 'Relation between drag and lift coefficients.'),
    ('Equivalent airspeed', 'True airspeed times √σ.'), ('Glide ratio', 'Horizontal distance per unit of height lost; equal to L/D.'), ('Induced drag', 'Drag caused by producing lift.'), ('Load factor', 'Lift divided by weight.'),
    ('Maneuvering speed', 'Speed at which full control input stalls the wing before limit load.'), ('Parasite drag', 'Drag not due to lift.'), ('Rate of climb', 'Vertical speed in a climb.'), ('Service ceiling', 'Altitude where maximum climb rate is 0.5 m/s.'),
    ('Specific excess power', 'Excess power per unit weight.'), ('Specific fuel consumption', 'Fuel used per unit thrust or power per unit time.'), ('Stall speed', 'Slowest steady flight speed, at C_Lmax.'),
    ('Standard atmosphere', 'Reference model of temperature, pressure and density with altitude.'), ('Sustainable aviation fuel', 'Jet fuel made from biomass and wastes.'), ('V-n diagram', 'Allowed load factor against airspeed.'), ('Wing loading', 'Weight divided by wing area.')])
RUBRIC = [('4 · Mastery', 'Starts from the atmosphere and the force balance, picks the right speed (V_md, V_mp, V_x, V_y, V_s), keeps weight and mass straight, and explains which design lever changes the answer.'), ('3 · Proficient', 'Solves the practice problems with occasional unit slips.'),
          ('2 · Developing', 'Follows worked examples but mixes up range and endurance speeds or forgets density.'), ('1 · Beginning', 'Plugs numbers into formulas without a diagram; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    g = 9.81; R = 287; r0 = 1.225; T0 = 288.15; L = 0.0065; p0 = 101325
    ex = g / (L * R)
    T = lambda h: T0 - L * h
    rho = lambda h: r0 * (T(h) / T0) ** (ex - 1)
    pr = lambda h: p0 * (T(h) / T0) ** ex
    a = lambda t: sqrt(1.4 * R * t)
    W = 60000 * g; S = 120; C0 = .02; K = .045
    LDm = 1 / (2 * sqrt(K * C0)); CLs = sqrt(C0 / K); Dmin = W / LDm
    r11 = rho(11000); q = .5 * r11 * 230 ** 2; CL = W / (q * S); CD = C0 + K * CL ** 2
    Vmd = lambda rr: sqrt(2 * W / (rr * S)) * (K / C0) ** .25
    qc = .5 * r0 * 130 ** 2; CLc = W / (qc * S); Dc = qc * S * (C0 + K * CLc ** 2); RC = (120000 - Dc) * 130 / W
    c = .6 / 3600; ln75 = log(1 / .75)
    Rj = lambda ld, lnw=ln75: 230 / c * ld * lnw
    cp = .3 * g / 3.6e6
    Vs = sqrt(2 * W / (r0 * S * 2.4)); sg = lambda rr: 1.44 * W ** 2 / (g * rr * S * 2.4 * 180000)
    Vsl = sqrt(2 * W / (r0 * S * 2.8)); Va = 1.3 * Vsl
    n = lambda p: 1 / cos(radians(p)); Rt = lambda V, p: V * V / (g * tan(radians(p))); wr = lambda V, p: degrees(V / Rt(V, p))
    Re = lambda eb, eta, ld, fb: eb * 3600 * eta / g * ld * fb
    r = [
     ('u1 T3000', T(3000), 268.65), ('u1 p3000', pr(3000), 70.1e3), ('u1 r3000', rho(3000), .909), ('u1 sig', rho(3000) / r0, .742), ('u1 a0', a(T0), 340.3), ('u1 a11', a(216.65), 295.0),
     ('u1 TT', 216.65 / T0, .7519), ('u1 r11', r11, .364), ('u1 p11', pr(11000), 22.6e3), ('u1 r5000', rho(5000), .736), ('u1 M', 250 / a(T0), .735), ('u1 ex', ex - 1, 4.26), ('u1 ex2', ex, 5.26),
     ('u2 W', W, 588.6e3), ('u2 LD', LDm, 16.67), ('u2 CL*', CLs, .667), ('u2 Dmin', Dmin, 35.3e3), ('u2 q', q, 9618), ('u2 CL', CL, .510), ('u2 CD', CD, .0317), ('u2 D', q * S * CD, 36.6e3),
     ('u2 LDc', CL / CD, 16.1), ('u2 M', 230 / a(216.65), .780), ('u2 LD half', 1 / (2 * sqrt(K * C0 / 2)), 23.6), ('u2 K', 1 / (pi * .8 * 9), .0442),
     ('u3 sq', sqrt(2 * W / (r0 * S)), 89.5), ('u3 kc', (K / C0) ** .25, 1.225), ('u3 Vmd', Vmd(r0), 109.6), ('u3 ratio', sqrt(r0 / r11), 1.835), ('u3 Vmd11', Vmd(r11), 201.2), ('u3 3q', 3 ** .25, 1.316),
     ('u3 Vmp', Vmd(r0) / 3 ** .25, 83.3), ('u3 PR', Dmin * Vmd(r0), 3.87e6), ('u3 Dmp', W / (sqrt(3) / 2 * LDm), 40.8e3), ('u3 q100', .5 * r0 * 100 ** 2, 6125), ('u3 w', sqrt(1.21), 1.1), ('u3 760', 3 ** -.25, .760), ('u3 866', sqrt(3) / 2, .866),
     ('u4 qc', qc, 10351), ('u4 CL', CLc, .474), ('u4 D', Dc, 37.4e3), ('u4 RC', RC, 18.2), ('u4 fpm', RC * 196.85, 3590), ('u4 g', degrees(asin((120000 - Dc) / W)), 8.07), ('u4 t', 10000 / 10 / 60, 16.7), ('u4 ex', 120000 - Dc, 82606),
     ('u5 d', 10000 * LDm, 166.7e3), ('u5 d40', 1000 * 40, 40e3), ('u5 ang', degrees(atan(1 / 40)), 1.43), ('u5 sink', 30 / 40, .75), ('u5 s35', 25 / 35, .714), ('u5 a10', degrees(atan(.1)), 5.71),
     ('u6 c', c, 1.667e-4), ('u6 ln', ln75, .2877), ('u6 R', Rj(16), 6352e3), ('u6 E', 1 / c * 16 * ln75, 27618), ('u6 Eh', 1 / c * 16 * ln75 / 3600, 7.67), ('u6 cp', cp, 8.175e-7), ('u6 ln85', log(1 / .85), .1625),
     ('u6 Rp', .8 / cp * 15 * log(1 / .85), 2386e3), ('u6 R18', Rj(18), 7146e3), ('u6 pct', 18 / 16, 1.125), ('u6 ln7', log(1 / .7), .3567), ('u6 R7', Rj(16, log(1 / .7)), 7875e3),
     ('u7 Vs', Vs, 57.8), ('u7 VLO', 1.2 * Vs, 69.3), ('u7 sg', sg(r0), 801), ('u7 r1500', rho(1500), 1.058), ('u7 sg15', sg(rho(1500)), 927), ('u7 rat', sg(rho(1500)) / sg(r0), 1.158), ('u7 W2', (70 / 60) ** 2, 1.361), ('u7 Vs2', sqrt(70 / 60), 1.080),
     ('u8 Vs', Vsl, 53.5), ('u8 Va', Va, 69.5), ('u8 s', Va ** 2 / (2 * .4 * g), 616), ('u8 E', .5 * 60000 * Va ** 2, 145e6), ('u8 s2', Va ** 2 / (.4 * g), 1232), ('u8 11', 1.1 ** 2, 1.21),
     ('u9 n30', n(30), 1.155), ('u9 n45', n(45), 1.414), ('u9 n60', n(60), 2.00), ('u9 R30', Rt(100, 30), 1766), ('u9 R45', Rt(100, 45), 1019), ('u9 R60', Rt(100, 60), 589), ('u9 w30', wr(100, 30), 3.25),
     ('u9 w45', wr(100, 45), 5.62), ('u9 w60', wr(100, 60), 9.74), ('u9 s30', sqrt(n(30)), 1.075), ('u9 s45', sqrt(n(45)), 1.189), ('u9 s60', sqrt(n(60)), 1.414), ('u9 VA', 50 * sqrt(2.5), 79.1), ('u9 R60b', Rt(60, 30), 636),
     ('u10 eb', 250 * 3600, 900000), ('u10 R', Re(250, .8, 15, .3), 330e3), ('u10 Wh', 43e6 / 3600, 11944), ('u10 rat', 43e6 / 3600 / 250, 47.8), ('u10 CO2', 3.16 * 1000, 3160), ('u10 R400', Re(400, .8, 15, .3), 528e3), ('u10 h', 3.16 * 2500, 7900),
     ('A r3000', rho(3000), .909), ('A a3000', a(268.65), 328.5), ('A r5000', rho(5000), .736), ('A a5000', a(255.65), 320.5), ('A T5000', T(5000), 255.65), ('A r11', r11, .364), ('A a11', a(216.65), 295.0),
     ('B LD', 6 / 1.5, 4.0), ('B ang', degrees(atan(1.5 / 6)), 14.0), ('B V', sqrt(36 + 2.25) / 2, 3.09), ('B sink', 1.5 / 2, .75),
     ('C CD2', C0 + K * .04, .0218), ('C CD6', C0 + K * .36, .0362), ('C CD10', C0 + K, .0650), ('C LD2', .2 / (C0 + K * .04), 9.17), ('C LD6', .6 / (C0 + K * .36), 16.6), ('C LD10', 1 / (C0 + K), 15.4),
     ('D R14', Rj(14), 5558e3), ('D R16', Rj(16), 6352e3), ('D R18', Rj(18), 7146e3), ('D c', 1 / .9, 1.111),
     ('E 0', sg(r0), 801), ('E 1500', sg(rho(1500)), 927), ('E r3000', rho(3000), .909), ('E 3000', sg(rho(3000)), 1079),
     ('F n15', n(15), 1.035), ('F R15', Rt(100, 15), 3804), ('F n30', n(30), 1.155), ('F R30', Rt(100, 30), 1766), ('F R45', Rt(100, 45), 1019), ('F R60', Rt(100, 60), 589), ('F n60', n(60), 2.000),
     ('M1', T(2000), 275.15), ('M2', rho(2000), 1.006), ('M3', 1 / (2 * sqrt(.04 * .025)), 15.81), ('M4', 50000 * 120 / 500000, 12.0), ('M5', 2000 * 12, 24e3),
     ('F1', 240 / (.55 / 3600) * 17 * log(1.25), 5959e3), ('F2', sqrt(2 * 100000 / (r0 * 30 * 1.8)), 55.0), ('F3', 1.2 ** 2, 1.44), ('F4', 60 ** 2 / 6, 600), ('F5', Rt(80, 45), 652), ('F6', Re(300, .85, 18, .35), 590e3)]
    r += [('x u1 dT', .0065 * 3000, 19.5), ('x u1 TT3', 268.65 / T0, .9323), ('x u1 2000', .0065 * 2000, 13), ('x u2 CL2', CL ** 2, .260), ('x u2 KC', K * C0, .0009), ('x u2 q11', .5 * r11, .1818),
          ('x u2 qS', q * S, 1.154e6), ('x u3 WS', W / S, 4905), ('x u3 KC', K / C0, 2.25), ('x u3 r', r0 / r11, 3.369), ('x u4 v2', 130 ** 2, 16900), ('x u4 CLc2', CLc ** 2, .2245), ('x u4 sin', (120000 - Dc) / W, .1403),
          ('x u5 tan', 1 / 40, .025), ('x u5 h', 10000 / 1000, 10), ('x u6 Vc', 230 / c, 1.38e6), ('x u6 1c', 1 / c, 6000), ('x u6 ec', .8 / cp, 978593), ('x u6 r85', 1 / .85, 1.1765), ('x u6 r75', 1 / .75, 1.3333),
          ('x u7 den', r0 * S * 2.4, 352.8), ('x u7 W2', W ** 2, 3.4645e11), ('x u7 r', r0 / rho(1500), 1.158), ('x u7 T1500', T(1500), 278.4), ('x u8 den', r0 * S * 2.8, 411.6), ('x u8 a', .4 * g, 3.924),
          ('x u8 V2', Va ** 2, 4833), ('x u9 t30', tan(radians(30)), .577), ('x u9 c60', cos(radians(60)), .5), ('x u9 n2', sqrt(n(30) ** 2 - 1), .577), ('x u10 J', 3600, 3600), ('x u10 e', 900000 * .8 / g, 73394),
          ('x u10 fb', 15 * .3, 4.5), ('x A 500', T(500), 284.9), ('x B dist', sqrt(36 + 2.25), 6.185), ('x C 36', .6 ** 2, .36), ('x D 1c', 230 * 6000, 1.38e6), ('x E r', r0 / rho(3000), 1.348),
          ('x F t15', tan(radians(15)), .268), ('x M2 r', 275.15 / T0, .9549), ('x F1 c', 3600 / .55, 6545), ('x F2 den', r0 * 30 * 1.8, 66.15), ('x F6 eb', 300 * 3600 * .85, 918000), ('x u9 V2', 100 ** 2, 10000)]
    return r
