"""Propulsion (AERO 410): thrust and efficiency, the Brayton cycle, inlets and nozzles, turbojets and turbofans, fuel use, rocket fundamentals, rocket nozzles and propellants, electric propulsion, and sustainable propulsion.
Oct 25 2026, founder-approved four-year track, senior course 1. Same module fields as probstat.py / orbit.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, log
ID = 'prop'
STATUS = 'live'
YEAR = 4
PAGE = 'Propulsion.html'
CODE = 'AERO 410'
TITLE = 'Propulsion'
LAB_NAME = 'Propulsion lab'
TAGLINE = 'Jet engines and rockets: the thrust equation, propulsive and thermal efficiency, the Brayton cycle, inlets and nozzles, turbojets and turbofans, fuel burn and emissions, rocket engines and propellants, electric thrusters, and cleaner fuels, with six labs. Free, self-paced, and tied to NASA’s RS-25 engines, NASA engine-core research and sustainable aviation fuel.'
DESC = 'Free self-study Propulsion: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and spreadsheet labs, practice exams, tied to rocket engines, efficient jet engines and sustainable aviation fuel.'
ALT = 'NASA’s SLS core stage fires its four RS-25 engines during the Green Run hot-fire test at Stennis Space Center'
_PH = 'https://phet.colorado.edu/en/simulations/'
_G = 'https://www.grc.nasa.gov/www/k-12/'
_MIT = ('MIT OpenCourseWare 16.50 Introduction to Propulsion Systems (Spring 2012)', 'https://ocw.mit.edu/courses/16-50-introduction-to-propulsion-systems-spring-2012/')
_MITR = ('MIT OpenCourseWare 16.512 Rocket Propulsion (Fall 2005)', 'https://ocw.mit.edu/courses/16-512-rocket-propulsion-fall-2005/')
_GTF = ('NASA Glenn Beginner’s Guide: Turbofan thrust', _G + 'airplane/turbfan.html')
_GBR = ('NASA Glenn Beginner’s Guide: Brayton cycle', _G + 'airplane/brayton.html')
_GSI = ('NASA Glenn Beginner’s Guide: Specific impulse', _G + 'airplane/specimp.html')
_GRT = ('NASA Glenn Beginner’s Guide: Rocket thrust summary', _G + 'rocket/rktthsum.html')
_RS25 = ('NASA: SLS (Space Launch System) RS-25 Core Stage Engine', 'https://www.nasa.gov/reference/space-launch-system-rs-25-core-stage-engine/')
_SAF = ('U.S. Department of Energy: Sustainable Aviation Fuels', 'https://www.energy.gov/eere/bioenergy/sustainable-aviation-fuels')
_HY = ('NASA Aeronautics: Hybrid Thermally Efficient Core (HyTEC) project', 'https://www.nasa.gov/directorates/armd/aavp/hytec/')
_DART = ('NASA Science: Double Asteroid Redirection Test (DART)', 'https://science.nasa.gov/mission/dart/')
BANNER = ['images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg', 'images/ArtemisII_Launch_KSC_Hancock.jpg', 'images/JPSS2_Atlas_V_Launch_Pad.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg']
CREDITS = {'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg': 'NASA/Michael DeMocker (MAF20210116_GR0006)', 'images/ArtemisII_Launch_KSC_Hancock.jpg': 'NASA',
           'images/JPSS2_Atlas_V_Launch_Pad.jpg': 'NASA/Liz Wilk (KSC-20221109-PH-LNW01_0001)', 'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester senior propulsion course for aerospace engineers. It is modeled on the topics and depth of MIT 16.50 Introduction to Propulsion Systems and MIT 16.512 Rocket Propulsion (free on MIT OpenCourseWare), using NASA Glenn’s free Beginner’s Guide to Propulsion, which we link where it helps. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (NASA’s RS-25 engines, NASA engine-core research and the U.S. Department of Energy’s sustainable aviation fuel work), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a spreadsheet.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Propulsion is where aviation’s fuel burn and emissions are decided: every point of engine efficiency is fuel not burned, and new fuels can cut the carbon in what is burned.',
                 'Rockets carry Earth-observing satellites to orbit, and cleaner, more efficient engines make that access more sustainable. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Thermodynamics: the first and second laws, ideal gases and cycles.', 'Fluid Mechanics: control volumes, compressible flow basics.',
           'Aerodynamics I and Aircraft Performance: drag, thrust required and range.', 'Orbital Mechanics: the rocket equation and Δv.']
STUDY = ['Draw a control volume around the engine and mark inflow and outflow before writing any equation.', 'Keep temperatures in kelvin and use stagnation (total) values where the flow is fast.',
         'Separate thermal efficiency (heat to kinetic energy) from propulsive efficiency (kinetic energy to useful thrust power).', 'Check every answer against a real engine’s order of magnitude.',
         'Track units: thrust in newtons, mass flow in kg/s, specific impulse in seconds.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Gas Properties and Energy Skate Park simulations.', 'Spreadsheet software (any free one works), or Python.',
            'NASA Glenn’s Beginner’s Guide to Propulsion pages in a web browser.', 'A calculator.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free simulation or a spreadsheet, so there are no physical hazards. Do not mix, make or burn propellants or build engines for this course. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('Air (textbook values)', 'γ = 1.4, c_p = 1005 J/(kg·K)'), ('Standard gravity', 'g₀ = 9.80665 m/s²'), ('1 lbf', '4.44822 N'),
             ('Jet fuel (textbook values)', 'heating value 43 MJ/kg; 3.16 kg CO₂ per kg burned'), ('Liquid hydrogen (textbook value)', 'heating value 120 MJ/kg'), ('Universal gas constant', '8314 J/(kmol·K)')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, NASA guides and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT propulsion lectures and problem sets.'), (_MITR[0], _MITR[1], 'Free MIT rocket propulsion course.'), (_GTF[0], _GTF[1], 'Free NASA explainer.'),
          (_GSI[0], _GSI[1], 'Free NASA explainer.'), (_GBR[0], _GBR[1], 'Free NASA explainer.'), ('PhET: Gas Properties', _PH + 'gas-properties', 'Gas laws interactively.')]
UNITS = []
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS.append(
{'id': 'u1', 'title': 'Thrust, Momentum and Propulsive Efficiency', 'weeks': 'Week 1',
 'summary': 'The control-volume thrust equation, pressure thrust, specific thrust, thrust power, jet power, propulsive efficiency, and why big slow jets are efficient.',
 'objectives': ['Derive thrust from momentum flux.', 'Compute specific thrust and thrust power.', 'Compute propulsive efficiency.', 'Explain why high bypass saves fuel.'],
 'concepts': ['Thrust is the net momentum flux out of the engine plus a pressure term: F = ṁ_eV_e − ṁ_0V_0 + (p_e − p_0)A_e.',
              'For an air-breathing engine with small fuel flow and a matched nozzle, F ≈ ṁ(V_e − V_0).',
              'Specific thrust F/ṁ (N·s/kg) tells you how much thrust each kilogram per second of air gives.',
              'Propulsive efficiency η_p = 2/(1 + V_e/V_0) is the share of jet kinetic power that becomes useful thrust power F·V_0.',
              'Accelerating a lot of air a little (V_e close to V_0) is efficient but needs a big engine; that is the turbofan’s trade.'],
 'eqs': [('F=\\dot m_eV_e-\\dot m_0V_0+(p_e-p_0)A_e', 'Thrust equation'), ('F\\approx\\dot m(V_e-V_0)', 'Simple thrust'), ('\\eta_p=\\frac{2}{1+V_e/V_0}', 'Propulsive efficiency'), ('P_{thrust}=FV_0', 'Thrust power')],
 'worked': [
  _w('An engine moves 100 kg/s of air from 250 m/s to 600 m/s (sample values). Find the thrust.', ['F = 100 × (600 − 250).'], 'F = 35 kN.'),
  _w('Find its propulsive efficiency.', ['η_p = 2/(1 + 600/250).'], 'η_p = 0.588.'),
  _w('Check that efficiency with powers.', ['Thrust power = 35,000 × 250 = 8.75 MW.', 'Jet power = ½ × 100 × (600² − 250²) = 14.875 MW.'], '8.75/14.875 = 0.588.')],
 'practice': [('Specific thrust of that engine?', '350 N·s/kg.'), ('η_p if V_e = 300 m/s at V₀ = 250 m/s?', '0.909.'),
              ('Why do fighters use small, fast jets?', 'High specific thrust at the cost of efficiency.'), ('When does pressure thrust matter?', 'When the nozzle exit pressure differs from ambient, as in many rockets.')],
 'misc': [('More exhaust speed always means more efficiency.', 'Propulsive efficiency falls as V_e/V₀ grows.'), ('Thrust pushes on the air behind.', 'It is the reaction to accelerating the flow.'), ('Pressure thrust is always zero.', 'Only for a perfectly expanded nozzle.')],
 'quiz': [_q('η_p = …', ['2/(1 + V_e/V₀)', 'V_e/V₀', '1 − V₀/V_e', 'FV_e'], 0, 'Froude.'), _q('Specific thrust units…', ['N·s/kg', 'N', 'kg/s', 's'], 0, 'F/ṁ.'),
          _q('Efficient engines move…', ['lots of air slowly', 'little air fast', 'no air', 'only fuel'], 0, 'Low V_e/V₀.'), _q('Thrust power is…', ['FV₀', 'FV_e', 'ṁV_e²', 'F/ṁ'], 0, 'Useful power.')],
 'cards': [('Thrust', 'Net momentum flux + pressure term.'), ('Specific thrust', 'F/ṁ.'), ('η_p', '2/(1 + V_e/V₀).'), ('Thrust power', 'F·V₀.'), ('Jet power', '½ṁ(V_e² − V₀²).'), ('Matched nozzle', 'p_e = p₀.')],
 'planet': {'text': ['NASA Glenn’s guide explains that most modern airliners use turbofans because of their high thrust and good fuel efficiency, and that high-bypass turbofans are nearly as fuel efficient as turboprops.',
                     'That efficiency comes straight from this unit’s equation: moving more air at a speed closer to flight speed raises propulsive efficiency, which means less fuel burned and less CO₂ for the same trip.'],
            'site': [('Aircraft Performance', 'Aircraft_Performance.html'), ('Solutions', 'Solutions.html')],
            'src': [_GTF]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_GSI[0], _GSI[1], 'Free NASA explainer.')]})
UNITS.append(
{'id': 'u2', 'title': 'The Brayton Cycle and Thermal Efficiency', 'weeks': 'Week 2',
 'summary': 'The ideal Brayton cycle, isentropic compression and expansion, thermal efficiency versus pressure ratio, compressor and turbine work, component efficiencies, and overall efficiency.',
 'objectives': ['Compute ideal Brayton efficiency from pressure ratio.', 'Find temperatures after isentropic compression.', 'Compute compressor work.', 'Combine thermal and propulsive efficiency.'],
 'concepts': ['A gas turbine runs the Brayton cycle: isentropic compression, constant-pressure heat addition, isentropic expansion and heat rejection.',
              'Ideal thermal efficiency depends only on the pressure ratio: η_th = 1 − π^(−(γ−1)/γ).',
              'Isentropic compression raises temperature by T₂/T₁ = π^((γ−1)/γ).',
              'Compressor work per kg is c_p(T₂ − T₁); the turbine must supply it before any is left for the jet.',
              'Overall efficiency η₀ = η_th × η_p: heat to useful thrust power.'],
 'eqs': [('\\eta_{th}=1-\\pi^{-(\\gamma-1)/\\gamma}', 'Ideal Brayton efficiency'), ('\\frac{T_2}{T_1}=\\pi^{(\\gamma-1)/\\gamma}', 'Isentropic compression'), ('w_c=c_p(T_2-T_1)', 'Compressor work'), ('\\eta_0=\\eta_{th}\\eta_p', 'Overall efficiency')],
 'worked': [
  _w('Find the ideal Brayton efficiency for pressure ratios 10 and 30 (γ = 1.4).', ['1 − 10^(−0.2857); 1 − 30^(−0.2857).'], '48.2% and 62.2%.'),
  _w('Air at 288 K is compressed by a ratio of 30. Find T₂.', ['T₂ = 288 × 30^0.2857 = 288 × 2.643.'], 'T₂ = 761 K.'),
  _w('Find the compressor work per kg.', ['1005 × (761 − 288).'], 'w_c = 475 kJ/kg.')],
 'practice': [('Efficiency at π = 20?', '57.5%.'), ('Efficiency at π = 40?', '65.1%.'),
              ('Overall efficiency for η_th = 0.5 and η_p = 0.8?', '0.40.'), ('Why not raise π forever?', 'Compressor exit gets too hot and heavy; turbine limits.')],
 'misc': [('Brayton efficiency depends on peak temperature.', 'Ideal efficiency depends only on π.'), ('All compressor work is lost.', 'The turbine recovers it from the hot gas.'), ('Thermal efficiency is the whole story.', 'Multiply by propulsive efficiency.')],
 'quiz': [_q('Ideal Brayton η depends on…', ['pressure ratio', 'fuel', 'size', 'altitude only'], 0, 'Formula.'), _q('Heat is added at…', ['constant pressure', 'constant volume', 'constant T', 'zero pressure'], 0, 'Burner.'),
          _q('η₀ = …', ['η_th × η_p', 'η_th + η_p', 'η_p/η_th', '1'], 0, 'Chain.'), _q('Compressing air…', ['heats it', 'cools it', 'nothing', 'liquefies it'], 0, 'Isentropic.')],
 'cards': [('Brayton cycle', 'Compress, burn, expand.'), ('Pressure ratio π', 'p₂/p₁.'), ('η_th', '1 − π^(−0.2857).'), ('Compressor work', 'c_pΔT.'), ('Overall efficiency', 'η_th η_p.'), ('Isentropic', 'Reversible and adiabatic.')],
 'planet': {'text': ['NASA’s Hybrid Thermally Efficient Core (HyTEC) project worked with industry to develop small-core engine technologies that enable fuel-burn reductions, more electric power extraction for aircraft systems, and better compatibility with sustainable aviation fuels. NASA notes the project has concluded.',
                     'Smaller, hotter, higher-pressure cores are this unit’s efficiency formula in hardware: raising the pressure ratio raises thermal efficiency, and every percent saves fuel on every flight.'],
            'site': [('Thermodynamics', 'Thermodynamics.html'), ('Solutions', 'Solutions.html')],
            'src': [_HY]},
 'res': [(_GBR[0], _GBR[1], 'Free NASA explainer.'), ('PhET: Gas Properties', _PH + 'gas-properties', 'Compression heating interactively.')]})
UNITS.append(
{'id': 'u3', 'title': 'Compressible Flow: Inlets and Nozzles', 'weeks': 'Weeks 3–4',
 'summary': 'Stagnation temperature and pressure, isentropic relations with Mach number, choked flow, area–Mach relations, converging and converging-diverging nozzles, and inlet pressure recovery.',
 'objectives': ['Use stagnation-to-static ratios.', 'Find the critical (sonic) conditions.', 'Use the area–Mach relation.', 'Compute ideal nozzle exit velocity.'],
 'concepts': ['Stagnation temperature T₀ = T(1 + (γ − 1)M²/2); stagnation pressure follows by the isentropic power γ/(γ − 1).',
              'At the throat of a choked nozzle M = 1, with T*/T₀ = 0.833 and p*/p₀ = 0.528 for air.',
              'Subsonic flow speeds up in a converging duct; supersonic flow speeds up in a diverging one. A/A* gives the area needed for each Mach number.',
              'Ideal exit velocity: V_e = √(2c_pT₀(1 − (p_e/p₀)^((γ−1)/γ))).',
              'Inlets slow air to subsonic speed for the compressor; losses in stagnation pressure cut thrust and efficiency.'],
 'eqs': [('\\frac{T_0}{T}=1+\\frac{\\gamma-1}{2}M^2', 'Stagnation temperature'), ('\\frac{p_0}{p}=\\left(\\frac{T_0}{T}\\right)^{\\gamma/(\\gamma-1)}', 'Stagnation pressure'), ('\\frac{A}{A^*}=\\frac1M\\left[\\frac{2}{\\gamma+1}\\left(1+\\frac{\\gamma-1}{2}M^2\\right)\\right]^{\\frac{\\gamma+1}{2(\\gamma-1)}}', 'Area–Mach relation'), ('V_e=\\sqrt{2c_pT_0\\left[1-(p_e/p_0)^{(\\gamma-1)/\\gamma}\\right]}', 'Ideal exit velocity')],
 'worked': [
  _w('Find T₀/T and p₀/p at Mach 0.8.', ['T₀/T = 1 + 0.2 × 0.64.', 'p₀/p = 1.128^3.5.'], 'T₀/T = 1.128; p₀/p = 1.524.'),
  _w('Find A/A* for Mach 2.', ['Area–Mach relation with γ = 1.4.'], 'A/A* = 1.6875.'),
  _w('Gas at T₀ = 1000 K expands to half its stagnation pressure (sample values). Find V_e.', ['V_e = √(2 × 1005 × 1000 × (1 − 0.5^0.2857)).'], 'V_e = 601 m/s.')],
 'practice': [('Critical pressure ratio for air?', 'p*/p₀ = 0.528.'), ('T*/T₀?', '0.833.'),
              ('A/A* at Mach 1.5?', '1.176.'), ('A/A* at Mach 3?', '4.235.')],
 'misc': [('Nozzles always converge.', 'Supersonic exits need a diverging section.'), ('Static and stagnation values are the same.', 'They differ at speed.'), ('Choking stops all flow.', 'It caps the mass flow for given upstream conditions.')],
 'quiz': [_q('At a choked throat M = …', ['1', '0', '2', '0.5'], 0, 'Sonic.'), _q('Supersonic flow accelerates in a…', ['diverging duct', 'converging duct', 'constant duct', 'none'], 0, 'Area–Mach.'),
          _q('p*/p₀ for air…', ['0.528', '0.833', '1', '0.1'], 0, 'γ = 1.4.'), _q('T₀/T at M = 0.8…', ['1.128', '1.8', '1', '0.8'], 0, 'Formula.')],
 'cards': [('Stagnation temperature', 'T(1 + 0.2M²) for air.'), ('Choked', 'M = 1 at the throat.'), ('A/A*', 'Area for a Mach number.'), ('p*/p₀', '0.528.'), ('Converging–diverging', 'For supersonic exits.'), ('Pressure recovery', 'Inlet p₀ kept.')],
 'planet': {'text': ['NASA’s RS-25 page notes that during Artemis I, engine thrust and mixture-ratio control valves were within 0.5 percent of pre-flight predicted values and internal pressures and temperatures were within two percent.',
                     'Predictions that close come from the isentropic-flow relations in this unit, refined by test data: getting nozzle and chamber conditions right is what makes an engine perform as designed.'],
            'site': [('Fluid Mechanics', 'Fluid_Mechanics.html'), ('Artemis II', 'Artemis_II.html')],
            'src': [_RS25]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_GRT[0], _GRT[1], 'Free NASA explainer.')]})
UNITS.append(
{'id': 'u4', 'title': 'Turbojets: Components and Cycle Analysis', 'weeks': 'Weeks 5–6',
 'summary': 'Inlet, compressor, burner, turbine and nozzle; work balance between compressor and turbine; turbine inlet temperature limits; afterburners; and real component efficiencies.',
 'objectives': ['Trace stations through a turbojet.', 'Balance compressor and turbine work.', 'Explain turbine temperature limits.', 'Describe how afterburning trades fuel for thrust.'],
 'concepts': ['Stations: free stream, inlet, compressor exit, burner exit (turbine inlet), turbine exit and nozzle exit.',
              'The turbine drives the compressor on a shared shaft: c_p(T₄ − T₅) = c_p(T₃ − T₂) for ideal flow with equal c_p.',
              'Higher turbine inlet temperature gives more specific thrust and efficiency, limited by blade materials and cooling.',
              'Real compressors and turbines have isentropic efficiencies below 1, so more work is needed and less is recovered.',
              'Afterburners add fuel after the turbine for extra thrust at a large fuel cost.'],
 'eqs': [('T_4-T_5=T_3-T_2', 'Shaft work balance'), ('\\eta_c=\\frac{T_{3s}-T_2}{T_3-T_2}', 'Compressor efficiency'), ('\\eta_t=\\frac{T_4-T_5}{T_4-T_{5s}}', 'Turbine efficiency'), ('F=\\dot m(V_e-V_0)', 'Thrust')],
 'worked': [
  _w('With a 475 kJ/kg compressor (Unit 2) and turbine inlet 1600 K (sample value), find the turbine exit temperature.', ['ΔT = 475,440/1005 = 473 K.'], 'T₅ = 1127 K.'),
  _w('A real compressor with η_c = 0.85 needs how much work for the same pressure ratio?', ['475/0.85.'], '559 kJ/kg.'),
  _w('Find the thrust of a turbojet moving 100 kg/s from 250 to 450 m/s.', ['100 × 200.'], '20 kN.')],
 'practice': [('Temperature rise of that real compressor?', '559,341/1005 = 557 K.'), ('Why cool turbine blades?', 'Gas is hotter than the metal can survive.'),
              ('What does an afterburner raise?', 'V_e and thrust.'), ('What does it lower?', 'Propulsive efficiency and range.')],
 'misc': [('The turbine makes the thrust.', 'It mainly drives the compressor; the nozzle makes thrust.'), ('Hotter is always possible.', 'Materials limit T₄.'), ('Afterburners are efficient.', 'They burn fuel at low pressure.')],
 'quiz': [_q('Turbine work equals…', ['compressor work', 'thrust', 'fuel energy', 'zero'], 0, 'Shared shaft.'), _q('T₄ is limited by…', ['materials', 'Mach', 'fuel color', 'altitude'], 0, 'Blades.'),
          _q('η_c < 1 means…', ['more work needed', 'less work', 'no change', 'free work'], 0, 'Losses.'), _q('Afterburners raise…', ['thrust', 'efficiency', 'range', 'bypass'], 0, 'Extra heat.')],
 'cards': [('Turbojet', 'Compressor–burner–turbine–nozzle.'), ('T₄', 'Turbine inlet temperature.'), ('Work balance', 'Turbine = compressor.'), ('η_c', 'Ideal/actual ΔT.'), ('Afterburner', 'Burn after the turbine.'), ('Station numbers', '0 free stream to 9 nozzle exit.')],
 'planet': {'text': ['NASA Glenn’s guide notes that low-bypass turbofans are still more fuel efficient than basic turbojets, and that many modern fighters use low-bypass turbofans with afterburners so they can cruise efficiently but still have high thrust when needed.',
                     'The pure turbojet survives mainly as a teaching model: its simple work balance shows why later engines added a fan to cut fuel burn.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Thermodynamics', 'Thermodynamics.html')],
            'src': [_GTF]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_GBR[0], _GBR[1], 'Free NASA explainer.')]})
UNITS.append(
{'id': 'u5', 'title': 'Turbofans and Turboprops', 'weeks': 'Week 7',
 'summary': 'Bypass ratio, core and fan streams, the turbofan thrust equation, propulsive efficiency of the fan stream, turboprops and open rotors, and the size and weight trade.',
 'objectives': ['Apply the turbofan thrust equation.', 'Compute bypass ratio and total flow.', 'Compare turbofan and turbojet thrust for the same core.', 'Explain the limits of very high bypass.'],
 'concepts': ['Bypass ratio bpr = ṁ_fan/ṁ_core; total flow ṁ₀ = ṁ_fan + ṁ_core.',
              'NASA Glenn’s turbofan thrust: F = (ṁV)_e + bpr·ṁ_c·V_f − ṁ₀V₀.',
              'The fan accelerates lots of air a little, so its stream has high propulsive efficiency.',
              'Turboprops and open rotors push bypass even higher, efficient at lower speeds.',
              'Bigger fans add weight, drag and noise and need slower fan speeds, often with a gearbox.'],
 'eqs': [('bpr=\\frac{\\dot m_f}{\\dot m_c}', 'Bypass ratio'), ('\\dot m_0=\\dot m_f+\\dot m_c', 'Total flow'), ('F=\\dot m_cV_e+bpr\\,\\dot m_cV_f-\\dot m_0V_0', 'Turbofan thrust'), ('\\eta_{p,f}=\\frac{2}{1+V_f/V_0}', 'Fan-stream efficiency')],
 'worked': [
  _w('A turbofan has core flow 100 kg/s and bpr = 10, with V_e = 450 m/s, V_f = 300 m/s and V₀ = 250 m/s (sample values). Find the total flow and thrust.', ['ṁ₀ = 100 + 1000 = 1100 kg/s.', 'F = 100 × 450 + 1000 × 300 − 1100 × 250.'], 'F = 70 kN.'),
  _w('Compare with a turbojet using the same core flow and exit speed.', ['F = 100 × (450 − 250).'], '20 kN: the fan multiplies thrust by 3.5.'),
  _w('Find the fan stream’s propulsive efficiency.', ['2/(1 + 300/250).'], 'η_p = 0.909.')],
 'practice': [('Core-stream η_p (450 at 250 m/s)?', '0.714.'), ('Thrust ratio turbofan/turbojet?', '3.5.'),
              ('Why gear the fan?', 'So the fan turns slower than the low-pressure turbine.'), ('Why are props used on slow aircraft?', 'Efficient at low speed; tips go supersonic at high speed.')],
 'misc': [('The fan makes little thrust.', 'In high-bypass engines it makes most of it.'), ('Higher bypass is always better.', 'Weight and drag grow with fan size.'), ('Turbofans burn more fuel than turbojets.', 'They burn less for the same thrust.')],
 'quiz': [_q('bpr = …', ['ṁ_f/ṁ_c', 'ṁ_c/ṁ_f', 'V_f/V_e', 'F/ṁ'], 0, 'Definition.'), _q('High-bypass fans…', ['move lots of air slowly', 'are supersonic', 'add no thrust', 'burn fuel'], 0, 'Efficiency.'),
          _q('Turboprops suit…', ['low speeds', 'Mach 2', 'rockets', 'space'], 0, 'Prop limits.'), _q('Same core, add a fan: thrust…', ['rises', 'falls', 'same', 'zero'], 0, 'More air.')],
 'cards': [('Bypass ratio', 'Fan flow/core flow.'), ('Turbofan thrust', 'Core + fan − inlet momentum.'), ('Fan stream', 'High η_p.'), ('Turboprop', 'Very high bypass via propeller.'), ('Geared fan', 'Slower fan, faster turbine.'), ('Open rotor', 'Unducted fan.')],
 'planet': {'text': ['NASA Glenn explains that because the core’s fuel flow changes only a small amount when a fan is added, a turbofan generates more thrust for nearly the same fuel, which is why it is very fuel efficient.',
                     'This unit’s example shows the effect: the same 100 kg/s core makes 20 kN as a turbojet and 70 kN with a bypass-ratio-10 fan, for nearly the same core fuel flow.'],
            'site': [('Aircraft Performance', 'Aircraft_Performance.html'), ('Solutions', 'Solutions.html')],
            'src': [_GTF]},
 'res': [(_GTF[0], _GTF[1], 'Free NASA explainer.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u6', 'title': 'Fuel Burn, TSFC and Emissions', 'weeks': 'Week 8',
 'summary': 'Fuel heating value, overall efficiency, thrust-specific fuel consumption, CO₂ from burning jet fuel, and how engine efficiency links to range and climate impact.',
 'objectives': ['Compute overall efficiency from fuel flow.', 'Compute TSFC.', 'Estimate CO₂ emissions from fuel burn.', 'Link TSFC to range.'],
 'concepts': ['Fuel power is ṁ_f × LHV; jet fuel’s lower heating value is about 43 MJ/kg (textbook value).',
              'Overall efficiency η₀ = F·V₀/(ṁ_f·LHV).',
              'Thrust-specific fuel consumption TSFC = ṁ_f/F; lower is better.',
              'Burning 1 kg of jet fuel makes about 3.16 kg of CO₂ (textbook value), since carbon picks up oxygen from the air.',
              'In the Breguet range equation, range grows with η₀ × LHV, so a better engine flies farther or burns less fuel.'],
 'eqs': [('\\eta_0=\\frac{FV_0}{\\dot m_f\\,LHV}', 'Overall efficiency'), ('TSFC=\\frac{\\dot m_f}{F}', 'TSFC'), ('\\dot m_{CO_2}=3.16\\,\\dot m_f', 'CO₂ rate (textbook)'), ('R=\\frac{\\eta_0 LHV}{g}\\frac{L}{D}\\ln\\frac{W_i}{W_f}', 'Breguet range')],
 'worked': [
  _w('The Unit 5 turbofan (70 kN at 250 m/s) burns 1.2 kg/s of fuel with LHV 43 MJ/kg (sample values). Find η₀.', ['η₀ = 70,000 × 250/(1.2 × 43 × 10⁶).'], 'η₀ = 0.339.'),
  _w('Find its TSFC.', ['1.2/70,000 kg/(N·s).'], 'TSFC = 17.14 mg/(N·s).'),
  _w('Find CO₂ per hour.', ['Fuel = 1.2 × 3600 = 4320 kg.', 'CO₂ = 4320 × 3.16.'], '13,651 kg of CO₂ per hour.')],
 'practice': [('CO₂ rate per second?', '3.792 kg/s.'), ('Thermal efficiency if η₀ = 0.339 and η_p = 0.8?', '0.424.'),
              ('Fuel saved per hour by a 10% lower TSFC at the same thrust?', '432 kg.'), ('Does cutting fuel cut CO₂ in proportion?', 'Yes, for the same fuel.')],
 'misc': [('Fuel weighs more than its CO₂.', 'CO₂ is about 3.16 times the fuel mass.'), ('TSFC higher is better.', 'Lower is better.'), ('Efficiency only affects cost.', 'It cuts emissions too.')],
 'quiz': [_q('TSFC = …', ['ṁ_f/F', 'F/ṁ_f', 'FV₀', 'LHV/F'], 0, 'Definition.'), _q('CO₂ per kg jet fuel (textbook)…', ['≈3.16 kg', '1 kg', '0.3 kg', '10 kg'], 0, 'Chemistry.'),
          _q('Range grows with…', ['η₀ × LHV', 'TSFC', 'weight', 'drag'], 0, 'Breguet.'), _q('η₀ example…', ['0.339', '0.9', '0.05', '1.2'], 0, 'Worked.')],
 'cards': [('LHV', 'Fuel energy per kg.'), ('η₀', 'FV₀/(ṁ_f LHV).'), ('TSFC', 'Fuel per thrust.'), ('CO₂ factor', '≈3.16 (textbook).'), ('Breguet', 'Range equation.'), ('Fuel power', 'ṁ_f × LHV.')],
 'planet': {'text': ['NASA’s HyTEC project aimed at small-core engine technologies to enable fuel-burn reductions and better compatibility with sustainable aviation fuels.',
                     'This unit’s numbers show why that matters: one large engine at cruise in our example emits about 13.7 tonnes of CO₂ per hour, so even small TSFC gains add up across a fleet.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_HY]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_HY[0], _HY[1], 'NASA project page.')]})
UNITS.append(
{'id': 'u7', 'title': 'Rocket Fundamentals and Specific Impulse', 'weeks': 'Weeks 9–10',
 'summary': 'Rocket thrust, effective exhaust velocity, specific impulse, total impulse, mass flow, and real numbers from NASA’s RS-25 engine.',
 'objectives': ['Use F = ṁV_eq.', 'Convert between Isp and exhaust velocity.', 'Compute total impulse.', 'Work with RS-25 thrust data.'],
 'concepts': ['A rocket carries all its propellant, so thrust is F = ṁV_e + (p_e − p₀)A_e = ṁV_eq.',
              'NASA Glenn defines specific impulse Isp = F/(ṁg₀), in seconds; V_eq = Isp × g₀.',
              'Total impulse I = F × Δt measures what a motor delivers overall.',
              'Higher Isp means less propellant for the same impulse.',
              'Thrust is often quoted as a percent of a rated level, as with the RS-25.'],
 'eqs': [('F=\\dot mV_{eq}', 'Rocket thrust'), ('I_{sp}=\\frac{F}{\\dot m g_0}', 'Specific impulse'), ('V_{eq}=I_{sp}g_0', 'Equivalent velocity'), ('I=F\\Delta t', 'Total impulse')],
 'worked': [
  _w('NASA says shuttle RS-25s ran at 104.5% of rated thrust, about 491,000 lbf. Convert to newtons and find 100% thrust.', ['491,000 × 4.448 N.', '491,000/1.045.'], '2.184 MN; about 469,856 lbf.'),
  _w('Using a textbook vacuum Isp of 452 s, find V_eq.', ['452 × 9.80665.'], 'V_eq = 4433 m/s.'),
  _w('Find the propellant flow at 2.184 MN.', ['ṁ = 2.184 × 10⁶/4433.'], 'ṁ = 492.7 kg/s (textbook-based).')],
 'practice': [('Four engines at 491,000 lbf?', '1.964 million lbf.'), ('Four at 109% of rated?', 'About 2.049 million lbf.'),
              ('Total impulse of a 1000 N motor for 20 s?', '20,000 N·s.'), ('V_eq for Isp 300 s?', '2942 m/s.')],
 'misc': [('Isp is a time the engine runs.', 'It is thrust per weight flow of propellant.'), ('Rockets need air to push on.', 'They work best in vacuum.'), ('Percent thrust above 100 is impossible.', 'It is relative to a historic rated level.')],
 'quiz': [_q('Isp = …', ['F/(ṁg₀)', 'ṁ/F', 'Fg₀', 'V/F'], 0, 'Glenn.'), _q('V_eq for Isp 452 s…', ['4433 m/s', '452 m/s', '9.8 km/s', '300 m/s'], 0, 'Multiply.'),
          _q('Total impulse units…', ['N·s', 'N', 's', 'kg'], 0, 'F × t.'), _q('RS-25 shuttle level…', ['104.5%', '50%', '200%', '10%'], 0, 'NASA.')],
 'cards': [('Isp', 'F/(ṁg₀), seconds.'), ('V_eq', 'Isp × g₀.'), ('Total impulse', 'F × Δt.'), ('RS-25', 'SLS core stage engine.'), ('Rated thrust', '100% reference level.'), ('g₀', '9.80665 m/s².')],
 'planet': {'text': ['NASA’s RS-25 page reports that the engines flew 135 Space Shuttle missions, with more than 3,000 starts and over 1 million seconds of total ground and flight firing; the SLS Block 1 rocket uses four RS-25s and two solid rocket boosters to send 27 metric tons to the Moon.',
                     'The same page notes that during Artemis I in November 2022 the engines produced over 2 million pounds of vacuum thrust. Reusing proven engines is one way NASA builds Earth-observing and exploration capability.'],
            'site': [('Artemis II', 'Artemis_II.html'), ('Orbital Mechanics', 'Orbital_Mechanics.html')],
            'src': [_RS25, _GSI]},
 'res': [(_GSI[0], _GSI[1], 'Free NASA explainer.'), (_MITR[0], _MITR[1], 'Free MIT rocket course.')]})
UNITS.append(
{'id': 'u8', 'title': 'Rocket Nozzles, Propellants and Throttling', 'weeks': 'Week 11',
 'summary': 'Chamber conditions, nozzle expansion, exit velocity from the isentropic relations, expansion ratio and altitude, propellant choices and throttling.',
 'objectives': ['Compute ideal rocket exhaust velocity.', 'Explain over- and under-expansion.', 'Compare propellant properties.', 'Relate throttle settings to thrust.'],
 'concepts': ['Ideal exit velocity: V_e = √(2γRT₀/(γ − 1) × (1 − (p_e/p₀)^((γ−1)/γ))), with R the gas constant per kg of exhaust.',
              'Hot, light exhaust (high T₀/M) gives high V_e: hydrogen–oxygen engines lead chemical Isp.',
              'Bigger expansion ratios lower p_e and raise V_e, but a nozzle sized for vacuum overexpands at sea level.',
              'Thrust coefficient and chamber pressure link nozzle size to thrust.',
              'Throttling varies propellant flow and chamber pressure; NASA quotes RS-25 power levels as percent of rated thrust.'],
 'eqs': [('V_e=\\sqrt{\\frac{2\\gamma}{\\gamma-1}\\frac{R_uT_0}{\\mathcal M}\\left[1-(p_e/p_0)^{(\\gamma-1)/\\gamma}\\right]}', 'Ideal rocket exit velocity'), ('I_{sp}=V_e/g_0', 'Isp (matched)'), ('F=\\dot mV_e+(p_e-p_a)A_e', 'Thrust with pressure term'), ('F_{\\%}=\\frac{F}{F_{100}}', 'Power level')],
 'worked': [
  _w('Exhaust with γ = 1.2, molar mass 13 g/mol and T₀ = 3500 K (sample values) expands to p_e/p₀ = 0.001. Find V_e and Isp.', ['V_e = √(12 × 8.314 × 3500/0.013 × (1 − 0.001^0.1667)).'], 'V_e = 4286 m/s; Isp = 437 s.'),
  _w('Repeat for p_e/p₀ = 0.01.', ['Smaller expansion.'], 'V_e = 3794 m/s.'),
  _w('NASA says new RS-25s run at 111% and were tested up to 113%. Find 113% in lbf from 469,856 lbf rated.', ['469,856 × 1.13.'], '530,937 lbf.')],
 'practice': [('111% of rated?', 'About 521,540 lbf (NASA: about 522,000).'), ('Isp at p_e/p₀ = 0.01?', '387 s.'),
              ('Why does T₀/M matter?', 'V_e scales with √(T₀/M).'), ('What happens to a vacuum nozzle at sea level?', 'Overexpansion; lower thrust and flow separation risk.')],
 'misc': [('Heavier exhaust is better.', 'Lighter exhaust gives higher V_e.'), ('Bigger nozzles always help.', 'Not at sea level.'), ('Throttle only changes flow.', 'Chamber pressure changes too.')],
 'quiz': [_q('V_e scales with…', ['√(T₀/M)', 'M', 'T₀²', '1/T₀'], 0, 'Formula.'), _q('Highest chemical Isp…', ['H₂/O₂', 'gunpowder', 'water', 'kerosene only'], 0, 'Light exhaust.'),
          _q('Lower p_e/p₀ gives…', ['higher V_e', 'lower V_e', 'same', 'zero'], 0, 'More expansion.'), _q('RS-25 tests reached…', ['113%', '50%', '150%', '200%'], 0, 'NASA.')],
 'cards': [('Expansion ratio', 'A_e/A*.'), ('Overexpanded', 'p_e < p_a.'), ('Underexpanded', 'p_e > p_a.'), ('Molar mass', 'Lighter exhaust, faster jet.'), ('Power level', 'Percent of rated thrust.'), ('Chamber pressure', 'Sets thrust for a nozzle size.')],
 'planet': {'text': ['NASA reports that RS-25s flew at 104.5% on the shuttle and were tested to 111%; SLS uses 109% for its first four flights, new production engines operate at 111%, and testing has reached 113%. L3Harris is building 24 new engines with modern methods such as selective laser melting.',
                     'Each added percent of thrust follows from chamber and nozzle physics in this unit, and lets the same engine lift more mass to orbit.'],
            'site': [('Artemis II', 'Artemis_II.html'), ('GOES-19', 'GOES-19.html')],
            'src': [_RS25]},
 'res': [(_MITR[0], _MITR[1], 'Free MIT rocket course.'), (_GRT[0], _GRT[1], 'Free NASA explainer.')]})
UNITS.append(
{'id': 'u9', 'title': 'The Rocket Equation and Electric Propulsion', 'weeks': 'Week 12',
 'summary': 'The Tsiolkovsky equation, mass ratio, staging, electric thrusters, power-limited thrust, and the trade between Isp and thrust.',
 'objectives': ['Use the rocket equation.', 'Compare chemical and electric Δv for the same propellant.', 'Compute power-limited thrust.', 'Explain why electric thrusters are low thrust.'],
 'concepts': ['Tsiolkovsky: Δv = V_e ln(m₀/m_f).',
              'Staging drops empty mass so later stages see better mass ratios.',
              'Electric thrusters (ion, Hall) reach very high Isp but are limited by power.',
              'Jet power ½ṁV_e² = ηP, so thrust F = 2ηP/V_e: higher V_e means less thrust for the same power.',
              'Electric propulsion suits long, patient missions; chemical rockets suit launch and quick maneuvers.'],
 'eqs': [('\\Delta v=V_e\\ln\\frac{m_0}{m_f}', 'Rocket equation'), ('F=\\frac{2\\eta P}{V_e}', 'Power-limited thrust'), ('V_e=I_{sp}g_0', 'Exhaust velocity'), ('\\frac{m_0}{m_f}=e^{\\Delta v/V_e}', 'Mass ratio')],
 'worked': [
  _w('A Hall thruster has Isp 1800 s (sample value). Find V_e.', ['1800 × 9.80665.'], 'V_e = 17,652 m/s.'),
  _w('With 4.5 kW and efficiency 0.5 (sample values), find thrust.', ['F = 2 × 0.5 × 4500/17,652.'], 'F = 0.255 N.'),
  _w('A 1000 kg craft uses 100 kg of propellant. Compare Δv with this thruster and with a 300 s chemical engine.', ['17,652 ln(1000/900); 2942 ln(1000/900).'], 'About 1860 m/s versus 310 m/s.')],
 'practice': [('Mass ratio for Δv = V_e?', 'e = 2.718.'), ('Thrust if power doubles?', '0.51 N.'),
              ('Why not launch with Hall thrusters?', 'Thrust is far below weight.'), ('Why stage?', 'Drop dead mass.')],
 'misc': [('High Isp means high thrust.', 'Power limits thrust.'), ('Δv is linear in propellant.', 'It is logarithmic.'), ('Electric engines need no propellant.', 'They still expel mass.')],
 'quiz': [_q('Δv = …', ['V_e ln(m₀/m_f)', 'V_e m₀', 'F/m', 'Isp'], 0, 'Tsiolkovsky.'), _q('Power-limited F = …', ['2ηP/V_e', 'PV_e', 'P/η', 'ṁg'], 0, 'Energy.'),
          _q('Hall V_e at 1800 s…', ['17.65 km/s', '1.8 km/s', '300 m/s', '100 km/s'], 0, 'Multiply.'), _q('Staging helps by…', ['dropping empty mass', 'adding fuel', 'raising g', 'nothing'], 0, 'Mass ratio.')],
 'cards': [('Rocket equation', 'Δv = V_e ln(m₀/m_f).'), ('Mass ratio', 'm₀/m_f.'), ('Staging', 'Discard empty tanks.'), ('Hall thruster', 'Electric, high Isp.'), ('Power-limited', 'F = 2ηP/V_e.'), ('Δv', 'Velocity change budget.')],
 'planet': {'text': ['NASA’s DART mission, a planetary-defense test, launched on November 24, 2021 aboard a Falcon 9 from Vandenberg Space Force Base and impacted the asteroid moonlet Dimorphos, about 160 meters across, on September 26, 2022.',
                     'Getting there took the rocket-equation budgeting of this unit: launch Δv from a chemical rocket, then precise in-space propulsion to steer into a small target.'],
            'site': [('Orbital Mechanics', 'Orbital_Mechanics.html'), ('Solutions', 'Solutions.html')],
            'src': [_DART]},
 'res': [(_MITR[0], _MITR[1], 'Free MIT rocket course.'), (_GSI[0], _GSI[1], 'Free NASA explainer.')]})
UNITS.append(
{'id': 'u10', 'title': 'Sustainable Propulsion: SAF, Hydrogen and Electric Flight', 'weeks': 'Week 13',
 'summary': 'Sustainable aviation fuels, energy density per kilogram, hydrogen and batteries compared with jet fuel, and what the numbers mean for future aircraft.',
 'objectives': ['Compare specific energies of fuels and batteries.', 'Describe SAF feedstocks and pathways.', 'Estimate fuel energy changes.', 'Weigh hydrogen’s mass and volume trade.'],
 'concepts': ['Specific energy (MJ/kg) sets how far an aircraft can fly per kilogram carried; jet fuel ≈ 43 MJ/kg, liquid hydrogen ≈ 120 MJ/kg and good batteries ≈ 0.25 MJ/kg (textbook values).',
              'SAF is made from biomass, wastes or captured carbon and can drop into existing engines with blending limits.',
              'Hydrogen has high energy per kilogram but very low density, so tanks are large and heavy.',
              'Batteries suit short flights and small aircraft; their low specific energy limits range.',
              'Life-cycle emissions depend on how the fuel is made, not just what comes out of the engine.'],
 'eqs': [('\\frac{e_{fuel}}{e_{batt}}=\\frac{43}{0.25}', 'Fuel vs battery (textbook)'), ('\\frac{e_{H_2}}{e_{jet}}=\\frac{120}{43}', 'Hydrogen vs jet fuel (textbook)'), ('m_{fuel}=\\frac{E}{e}', 'Mass for an energy'), ('E=m\\,LHV', 'Fuel energy')],
 'worked': [
  _w('How many times more energy per kg does jet fuel hold than a battery (textbook values)?', ['43/0.25.'], '172 times.'),
  _w('How does liquid hydrogen compare with jet fuel per kg?', ['120/43.'], '2.79 times.'),
  _w('DOE says a LANL bio-acetone SAF has 12% more energy than conventional jet fuel. Using 43 MJ/kg as the base (textbook value), estimate its energy.', ['1.12 × 43.'], 'About 48.2 MJ/kg.')],
 'practice': [('Battery mass to store the energy in 1 kg of jet fuel?', '172 kg.'), ('Hydrogen mass for the energy of 1000 kg of jet fuel?', '358 kg.'),
              ('Name a SAF feedstock.', 'Biomass, wet waste or waste CO.'), ('Why is hydrogen hard to store?', 'Very low density; cryogenic tanks.')],
 'misc': [('Hydrogen is energy-poor.', 'Per kilogram it beats jet fuel; per liter it does not.'), ('Batteries will soon match jet fuel.', 'The gap is over 100×.'), ('SAF needs new engines.', 'It is designed to work in existing ones.')],
 'quiz': [_q('Jet fuel vs battery (textbook)…', ['172×', '2×', '10×', '1000×'], 0, '43/0.25.'), _q('Hydrogen’s weak point…', ['volume', 'mass', 'energy', 'color'], 0, 'Density.'),
          _q('DOE biomass potential…', ['>1 billion tons a year', '1 ton', '1 million tons', 'none'], 0, 'Billion-Ton Report.'), _q('LANL SAF energy vs jet fuel…', ['+12%', '−50%', 'same', '+100%'], 0, 'DOE.')],
 'cards': [('SAF', 'Sustainable aviation fuel.'), ('Specific energy', 'MJ/kg.'), ('LH₂', 'Liquid hydrogen.'), ('Drop-in fuel', 'Works in current engines.'), ('Life cycle', 'Production to combustion.'), ('Billion-Ton Report', 'DOE biomass study.')],
 'planet': {'text': ['The U.S. Department of Energy says its 2023 Billion-Ton Report found the United States could produce more than 1 billion tons of biomass a year, enough for about 60 billion gallons of biofuels, and that a LANL bio-acetone SAF has 12% more energy than conventional jet fuel.',
                     'DOE also describes SAF from wet waste and from waste CO through alcohol-to-jet routes. Combined with efficient engines from earlier units, cleaner fuel is a direct route to lower aviation emissions.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_SAF]},
 'res': [(_SAF[0], _SAF[1], 'DOE explainer.'), (_HY[0], _HY[1], 'NASA project page.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Thrust and propulsive efficiency sweep', 'week': 'Week 1',
 'goal': 'Build a spreadsheet that sweeps exhaust velocity at fixed flight speed and finds thrust, specific thrust and propulsive efficiency.',
 'eq': ('\\eta_p=\\frac{2}{1+V_e/V_0}', 'Propulsive efficiency'),
 'steps': ['Set ṁ = 100 kg/s and V₀ = 250 m/s.', 'Sweep V_e from 300 to 900 m/s.', 'Compute F, F/ṁ and η_p in each row.', 'Plot η_p against specific thrust and describe the trade.'],
 'table': (['V_e (m/s)', 'F (kN)', 'η_p'], [['300', '5', '0.909'], ['450', '20', '0.714'], ['600', '35', '0.588'], ['900', '65', '0.435']]),
 'note': 'Computed sample values.',
 'calc': ['F = 100 × (600 − 250) = 35 kN.', 'η_p = 2/(1 + 900/250) = 0.435.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_GTF[0], _GTF[1])],
 'planet': 'NASA Glenn notes high-bypass turbofans are nearly as fuel efficient as turboprops.', 'planet_src': [_GTF]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Compression heating and Brayton efficiency', 'week': 'Week 2',
 'goal': 'Watch gas heat when compressed in PhET Gas Properties, then tabulate ideal Brayton efficiency versus pressure ratio.',
 'eq': ('\\eta_{th}=1-\\pi^{-0.2857}', 'Ideal Brayton efficiency (γ = 1.4)'),
 'steps': ['In PhET Gas Properties, insulate the box (hold heat constant) and push the wall in quickly; note the temperature rise.', 'In a spreadsheet, list π = 10, 20, 30, 40.', 'Compute η_th and T₂ from 288 K.', 'Plot η_th against π and note diminishing returns.'],
 'table': (['π', 'η_th', 'T₂ (K)'], [['10', '0.482', '556'], ['20', '0.575', '678'], ['30', '0.622', '761'], ['40', '0.651', '825']]),
 'note': 'Computed ideal values.',
 'calc': ['η = 1 − 30^(−0.2857) = 0.622.', 'T₂ = 288 × 40^0.2857 = 825 K.'],
 'safety': ['Computer only.'], 'home': ['Any browser and spreadsheet work.'],
 'sims': [('PhET: Gas Properties', _PH + 'gas-properties'), (_GBR[0], _GBR[1])],
 'planet': 'NASA’s HyTEC project developed small-core engine technologies for fuel-burn reductions.', 'planet_src': [_HY]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Building isentropic flow tables', 'week': 'Week 4',
 'goal': 'Compute T₀/T, p₀/p and A/A* versus Mach number for air and find where the area is smallest.',
 'eq': ('\\frac{A}{A^*}=\\frac1M\\left[\\frac{2}{\\gamma+1}\\left(1+\\frac{\\gamma-1}{2}M^2\\right)\\right]^{3}', 'Area–Mach relation (γ = 1.4)'),
 'steps': ['List M from 0.2 to 3 in steps of 0.1.', 'Compute T₀/T, p₀/p and A/A*.', 'Plot A/A* and confirm its minimum of 1 at M = 1.', 'Read off the area ratio a Mach 2 nozzle needs.'],
 'table': (['M', 'p₀/p', 'A/A*'], [['0.8', '1.524', '1.038'], ['1.0', '1.893', '1.000'], ['2.0', '7.824', '1.688'], ['3.0', '36.73', '4.235']]),
 'note': 'Computed values for γ = 1.4.',
 'calc': ['p₀/p at M = 2: 1.8^3.5 = 7.824.', 'A/A* at M = 0.8: (1/0.8)(1.128/1.2)³ = 1.038.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MIT[0], _MIT[1])],
 'planet': 'NASA reports Artemis I RS-25 valves within 0.5% of predicted values.', 'planet_src': [_RS25]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: The turbofan bypass trade', 'week': 'Week 7',
 'goal': 'Sweep bypass ratio for a fixed core and fan speed and compare thrust and fan-stream efficiency.',
 'eq': ('F=\\dot m_cV_e+bpr\\,\\dot m_cV_f-\\dot m_0V_0', 'Turbofan thrust'),
 'steps': ['Fix ṁ_c = 100 kg/s, V_e = 450, V_f = 300, V₀ = 250 m/s.', 'Sweep bpr from 0 to 12.', 'Compute F and the thrust ratio to bpr = 0.', 'Discuss why real engines stop near today’s bypass ratios.'],
 'table': (['bpr', 'F (kN)', 'Ratio'], [['0', '20', '1.0'], ['5', '45', '2.25'], ['10', '70', '3.5'], ['12', '80', '4.0']]),
 'note': 'Computed sample values.',
 'calc': ['F(5) = 45,000 + 150,000 − 150,000 = 45 kN.', 'Each unit of bpr adds 100 × 50 = 5 kN.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_GTF[0], _GTF[1])],
 'planet': 'NASA Glenn: a turbofan makes more thrust for nearly the same core fuel flow.', 'planet_src': [_GTF]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Rocket nozzle expansion and Isp', 'week': 'Week 11',
 'goal': 'Compute ideal rocket exhaust velocity and Isp as the nozzle pressure ratio changes, then relate RS-25 power levels to thrust.',
 'eq': ('V_e=\\sqrt{\\frac{2\\gamma}{\\gamma-1}\\frac{R_uT_0}{\\mathcal M}\\left[1-(p_e/p_0)^{(\\gamma-1)/\\gamma}\\right]}', 'Ideal exit velocity'),
 'steps': ['Use γ = 1.2, molar mass 13 g/mol and T₀ = 3500 K (sample values).', 'Sweep p_e/p₀ from 0.1 to 0.0001.', 'Compute V_e and Isp.', 'Tabulate RS-25 thrust at 104.5%, 109%, 111% and 113% of 469,856 lbf.'],
 'table': (['p_e/p₀', 'V_e (m/s)', 'Isp (s)'], [['0.01', '3794', '387'], ['0.001', '4286', '437']]),
 'note': 'Computed sample values; RS-25 levels from NASA.',
 'calc': ['V_e = √(12 × 639.5 × 3500 × (1 − 0.001^0.1667)) = 4286 m/s.', '109% × 469,856 = 512,143 lbf.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_GRT[0], _GRT[1]), (_GSI[0], _GSI[1])],
 'planet': 'NASA says new RS-25s operate at 111% and testing reached 113%.', 'planet_src': [_RS25]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Energy density and the SAF question', 'week': 'Week 13',
 'goal': 'Compare the mass needed to carry the same energy as jet fuel, liquid hydrogen, a battery and a higher-energy SAF.',
 'eq': ('m=E/e', 'Mass for an energy'),
 'steps': ['Set E = 43,000 MJ (1000 kg of jet fuel, textbook value).', 'Compute mass for each energy carrier.', 'Plot the masses on a log axis.', 'Write a paragraph on where each option fits.'],
 'table': (['Carrier', 'MJ/kg', 'Mass (kg)'], [['Jet fuel', '43', '1000'], ['Liquid hydrogen', '120', '358'], ['Battery', '0.25', '172,000'], ['SAF (+12%)', '48.16', '893']]),
 'note': 'Textbook specific energies; SAF energy gain from DOE.',
 'calc': ['43,000/0.25 = 172,000 kg.', '43,000/48.16 = 893 kg.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_SAF[0], _SAF[1])],
 'planet': 'DOE says the US could produce more than 1 billion tons of biomass a year.', 'planet_src': [_SAF]})
SCHEDULE = [(1, 'u1', 'Thrust and propulsive efficiency; Lab A', 'NASA Glenn'), (2, 'u2', 'Brayton cycle; Lab B', 'NASA Glenn'),
            (3, 'u3', 'Stagnation properties and choking', 'MIT 16.50'), (4, 'u3', 'Nozzles and inlets; Lab C', 'MIT 16.50'),
            (5, 'u4', 'Turbojet stations and work balance', 'MIT 16.50'), (6, 'u4', 'Component efficiency and afterburners', 'NASA Glenn'),
            (7, 'u5', 'Turbofans; Lab D; midterm practice', 'NASA Glenn'), (8, 'u6', 'Fuel burn, TSFC and CO₂', 'NASA HyTEC'),
            (9, 'u7', 'Rocket thrust and Isp', 'NASA Glenn'), (10, 'u7', 'RS-25 case study', 'NASA RS-25'),
            (11, 'u8', 'Rocket nozzles and throttling; Lab E', 'MIT 16.512'), (12, 'u9', 'Rocket equation and electric propulsion', 'MIT 16.512'),
            (13, 'u10', 'SAF, hydrogen and batteries; Lab F', 'DOE SAF'), (14, 'u10', 'Electric aircraft and review', 'DOE SAF'), (15, 'u10', 'Review; final practice', 'MIT 16.50')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('An engine moves 80 kg/s from 200 to 500 m/s. Find thrust and η_p.', ['F = 80 × 300.', 'η_p = 2/(1 + 2.5).'], '24 kN; 0.571.'),
  ('Find ideal Brayton efficiency at π = 25.', ['1 − 25^(−0.2857).'], '60.1%.'),
  ('Find T₀/T at Mach 2.', ['1 + 0.2 × 4.'], '1.8.'),
  ('Find the compressor exit temperature for π = 20 from 288 K.', ['288 × 20^0.2857.'], '678 K.'),
  ('A turbofan has ṁ_c = 50 kg/s, bpr = 8, V_e = 400, V_f = 280, V₀ = 240 m/s. Find thrust.', ['50 × 400 + 400 × 280 − 450 × 240.'], '24 kN.')]),
 ('Final practice set (Units 1–10)', [
  ('An engine makes 50 kN at 240 m/s burning 0.9 kg/s of 43 MJ/kg fuel. Find η₀ and TSFC.', ['50,000 × 240/(0.9 × 43 × 10⁶).', '0.9/50,000.'], '0.310; 18 mg/(N·s).'),
  ('Find CO₂ per hour for 0.9 kg/s of fuel (3.16 kg/kg, textbook).', ['0.9 × 3600 × 3.16.'], '10,238 kg.'),
  ('Find V_eq for Isp 350 s.', ['350 × 9.80665.'], '3432 m/s.'),
  ('Find Δv for V_e = 3432 m/s and mass ratio 5.', ['3432 ln 5.'], '5524 m/s.'),
  ('A 2 kW ion thruster (η = 0.6) has V_e = 30 km/s. Find thrust.', ['2 × 0.6 × 2000/30,000.'], '0.08 N.'),
  ('How much liquid hydrogen (120 MJ/kg) matches 500 kg of jet fuel (43 MJ/kg)?', ['500 × 43/120.'], '179 kg.')])]
FORMULAS = ['F=\\dot m(V_e-V_0)+(p_e-p_0)A_e,\\ \\eta_p=2/(1+V_e/V_0)', '\\eta_{th}=1-\\pi^{-(\\gamma-1)/\\gamma},\\ T_2/T_1=\\pi^{(\\gamma-1)/\\gamma}',
            'T_0/T=1+\\frac{\\gamma-1}2M^2,\\ p_0/p=(T_0/T)^{\\gamma/(\\gamma-1)}', 'w_c=c_p(T_3-T_2)=c_p(T_4-T_5)', 'F=\\dot m_cV_e+bpr\\,\\dot m_cV_f-\\dot m_0V_0',
            '\\eta_0=FV_0/(\\dot m_fLHV),\\ TSFC=\\dot m_f/F', 'I_{sp}=F/(\\dot mg_0),\\ I=F\\Delta t', 'V_e=\\sqrt{\\frac{2\\gamma}{\\gamma-1}\\frac{R_uT_0}{\\mathcal M}[1-(p_e/p_0)^{(\\gamma-1)/\\gamma}]}',
            '\\Delta v=V_e\\ln(m_0/m_f),\\ F=2\\eta P/V_e', 'm=E/e']
GLOSSARY = sorted([('Afterburner', 'Burner after the turbine for extra thrust.'), ('Area ratio', 'A/A*, nozzle area over throat area.'), ('Bypass ratio', 'Fan flow over core flow.'), ('Brayton cycle', 'Gas-turbine thermodynamic cycle.'),
    ('Choked flow', 'Sonic flow at a throat that caps mass flow.'), ('Compressor', 'Raises air pressure.'), ('Hall thruster', 'Electric thruster using crossed fields.'), ('Isentropic', 'Reversible and adiabatic.'),
    ('Mach number', 'Speed over sound speed.'), ('Overall efficiency', 'Thrust power over fuel power.'), ('Pressure ratio', 'Compressor exit over inlet pressure.'), ('Propulsive efficiency', 'Thrust power over jet power.'),
    ('Rocket equation', 'Δv = V_e ln(m₀/m_f).'), ('SAF', 'Sustainable aviation fuel.'), ('Specific impulse', 'Thrust per weight flow of propellant.'), ('Specific thrust', 'Thrust per unit air flow.'),
    ('Stagnation temperature', 'Temperature if flow is brought to rest adiabatically.'), ('TSFC', 'Fuel flow per thrust.'), ('Turbine', 'Extracts work to drive the compressor.'), ('Turbofan', 'Gas turbine with a bypass fan.')])
RUBRIC = [('4 · Mastery', 'Sets up control volumes and stations, picks the right relations, checks units and explains efficiency and emissions trades in plain words.'), ('3 · Proficient', 'Solves the practice problems with occasional slips in units or stations.'),
          ('2 · Developing', 'Follows worked examples but mixes stagnation and static values or Isp and exhaust velocity.'), ('1 · Beginning', 'Plugs numbers into formulas without a station diagram; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    k = 0.4 / 1.4; g0 = 9.80665; cp = 1005
    bt = lambda p: 1 - p ** -k
    ep = lambda ve, v0: 2 / (1 + ve / v0)
    t0 = lambda M: 1 + 0.2 * M * M
    aa = lambda M: (1 / M) * ((2 / 2.4) * t0(M)) ** 3
    vr = lambda r: sqrt(2 * 1.2 / 0.2 * 8.314 / 0.013 * 3500 * (1 - r ** (0.2 / 1.2)))
    tf = lambda b: 100 * 450 + b * 100 * 300 - (100 + 100 * b) * 250
    wc = cp * (288 * 30 ** k - 288)
    r = [
     ('u1 F', 100 * 350, 35000), ('u1 ep', ep(600, 250), .588), ('u1 sp', 350, 35000 / 100), ('u1 Pt', 35000 * 250, 8.75e6), ('u1 Pj', .5 * 100 * (600 ** 2 - 250 ** 2), 14.875e6),
     ('u1 rat', 8.75 / 14.875, .588), ('u1 ep300', ep(300, 250), .909), ('u1 q', ep(600, 250), .588),
     ('u2 10', bt(10), .482), ('u2 20', bt(20), .575), ('u2 30', bt(30), .622), ('u2 40', bt(40), .651), ('u2 T2', 288 * 30 ** k, 761), ('u2 pr', 30 ** k, 2.643), ('u2 wc', wc, 475e3),
     ('u2 eo', .5 * .8, .40),
     ('u3 t0', t0(.8), 1.128), ('u3 p0', t0(.8) ** 3.5, 1.524), ('u3 a2', aa(2), 1.6875), ('u3 a15', aa(1.5), 1.176), ('u3 a3', aa(3), 4.235), ('u3 ps', (1 / 1.2) ** 3.5, .528),
     ('u3 ts', 1 / 1.2, .833), ('u3 ve', sqrt(2 * cp * 1000 * (1 - .5 ** k)), 601),
     ('u4 dT', wc / cp, 473), ('u4 T5', 1600 - wc / cp, 1127), ('u4 real', wc / .85, 559e3), ('u4 rdT', wc / .85 / cp, 557), ('u4 F', 100 * 200, 20000), ('u4 b', ep(450, 250), .714),
     ('u5 m0', 100 + 1000, 1100), ('u5 F', tf(10), 70000), ('u5 tj', tf(0), 20000), ('u5 rat', tf(10) / tf(0), 3.5), ('u5 epf', ep(300, 250), .909), ('u5 epc', ep(450, 250), .714),
     ('u6 eo', 70000 * 250 / (1.2 * 43e6), .339), ('u6 ts', 1.2 / 70000 * 1e6, 17.14), ('u6 fh', 1.2 * 3600, 4320), ('u6 co', 4320 * 3.16, 13651), ('u6 cos', 1.2 * 3.16, 3.792),
     ('u6 th', .339 / .8, .424), ('u6 sav', 4320 * .1, 432), ('u6 t', 13651 / 1000, 13.7),
     ('u7 N', 491000 * 4.44822, 2.184e6), ('u7 rated', 491000 / 1.045, 469856), ('u7 4', 4 * 491000, 1.964e6), ('u7 109', 4 * 1.09 * 491000 / 1.045, 2.049e6), ('u7 ve', 452 * g0, 4433),
     ('u7 md', 491000 * 4.44822 / (452 * g0), 492.7), ('u7 I', 1000 * 20, 20000), ('u7 v300', 300 * g0, 2942), ('u7 111', 1.11 * 491000 / 1.045, 522000),
     ('u8 v3', vr(.001), 4286), ('u8 isp3', vr(.001) / g0, 437), ('u8 v2', vr(.01), 3794), ('u8 isp2', vr(.01) / g0, 387), ('u8 113', 469856 * 1.13, 530937), ('u8 111', 469856 * 1.11, 521540),
     ('u8 R', 8.314 / .013, 639.5),
     ('u9 ve', 1800 * g0, 17652), ('u9 F', 2 * .5 * 4500 / (1800 * g0), .255), ('u9 dv', 1800 * g0 * log(1000 / 900), 1860), ('u9 dvc', 300 * g0 * log(1000 / 900), 310), ('u9 e', 2.718281828, 2.718),
     ('u9 F2', 2 * .5 * 9000 / (1800 * g0), .51),
     ('u10 bat', 43 / .25, 172), ('u10 h2', 120 / 43, 2.79), ('u10 saf', 1.12 * 43, 48.2), ('u10 bm', 43 / .25, 172), ('u10 hm', 1000 * 43 / 120, 358),
     ('labA 300', 100 * 50, 5000), ('labA 450', 100 * 200, 20000), ('labA 600', 100 * 350, 35000), ('labA 900', 100 * 650, 65000), ('labA e300', ep(300, 250), .909), ('labA e450', ep(450, 250), .714),
     ('labA e600', ep(600, 250), .588), ('labA e900', ep(900, 250), .435),
     ('labB 10', bt(10), .482), ('labB 20', bt(20), .575), ('labB 30', bt(30), .622), ('labB 40', bt(40), .651), ('labB T10', 288 * 10 ** k, 556), ('labB T20', 288 * 20 ** k, 678),
     ('labB T30', 288 * 30 ** k, 761), ('labB T40', 288 * 40 ** k, 825),
     ('labC p8', t0(.8) ** 3.5, 1.524), ('labC a8', aa(.8), 1.038), ('labC p1', t0(1) ** 3.5, 1.893), ('labC a1', aa(1), 1.0), ('labC p2', t0(2) ** 3.5, 7.824), ('labC a2', aa(2), 1.688),
     ('labC p3', t0(3) ** 3.5, 36.73), ('labC a3', aa(3), 4.235),
     ('labD 0', tf(0), 20000), ('labD 5', tf(5), 45000), ('labD 10', tf(10), 70000), ('labD 12', tf(12), 80000), ('labD r5', tf(5) / tf(0), 2.25), ('labD r10', tf(10) / tf(0), 3.5),
     ('labD r12', tf(12) / tf(0), 4.0), ('labD step', 100 * 50, 5000),
     ('labE v2', vr(.01), 3794), ('labE i2', vr(.01) / g0, 387), ('labE v3', vr(.001), 4286), ('labE i3', vr(.001) / g0, 437), ('labE 109', 469856 * 1.09, 512143), ('labE R', 8.314 / .013, 639.5),
     ('labF jet', 43000 / 43, 1000), ('labF h2', 43000 / 120, 358), ('labF bat', 43000 / .25, 172000), ('labF saf', 43000 / 48.16, 893), ('labF s', 1.12 * 43, 48.16),
     ('mid F', 80 * 300, 24000), ('mid ep', ep(500, 200), .571), ('mid bt', bt(25), .601), ('mid t0', t0(2), 1.8), ('mid T2', 288 * 20 ** k, 678), ('mid tf', 50 * 400 + 400 * 280 - 450 * 240, 24000),
     ('fin eo', 50000 * 240 / (.9 * 43e6), .310), ('fin ts', .9 / 50000 * 1e6, 18), ('fin co', .9 * 3600 * 3.16, 10238), ('fin ve', 350 * g0, 3432), ('fin dv', 350 * g0 * log(5), 5524),
     ('fin ion', 2 * .6 * 2000 / 30000, .08), ('fin h2', 500 * 43 / 120, 179),
     ('c g0', g0, 9.80665), ('c lbf', 4.44822, 4.448), ('c k', k, .2857), ('c cp', cp, 1005), ('c R', 8.314, 8.314), ('c co2', 44 / 12 * .862, 3.16),
     ('x rs starts', 135, 135), ('x sls t', 59525 * .4536, 27000), ('x 1b', 38, 38), ('x b2', 43, 43), ('x sl', 69, 69), ('x bt', 1e9, 1e9), ('x gal', 60e9, 60e9),
     ('x dart', 160, 160), ('x art', 2e6, 2e6), ('x pr', 491000 / 469856, 1.045), ('x 104', 1.045 * 469856, 491000), ('x 111b', 1.11 * 469856, 522000),
     ('x u1 dv', 600 - 250, 350), ('x u2 d', bt(40) - bt(10), .169), ('x u3 r', 1 / t0(.8), .887), ('x u5 bypass', 1000 / 100, 10), ('x u6 kg', 1.2 * 60, 72), ('x u7 Mlbf', 2.184e6 / 4.44822, 491000),
     ('x u9 r', 1000 / 900, 1.111), ('x u10 d', 48.16 - 43, 5.16), ('x labF r', 1000 / 893, 1.12), ('x labE r', 4286 / 3794, 1.13), ('x fin ln', log(5), 1.609), ('x mid r', 500 / 200, 2.5),
     ('x u4 eta', .85, 475 / 559), ('x u8 sq', sqrt(3500 / .013), 518.9), ('x u9 ln', log(1000 / 900), .1054), ('x u6 tsfc g', 17.14e-6 * 3600 * 70000, 4320), ('x u2 w', wc / 1000, 475.4),
     ('x labC m1', t0(1), 1.2), ('x labB d', bt(40) - bt(30), .0299), ('x u7 4m', 4 * 2.184, 8.736), ('x u5 core', 100, 100), ('x labA sp', 65000 / 100, 650), ('x labD ad', tf(12) - tf(10), 10000),
     ('y u3 p2', t0(2) ** 3.5, 7.824), ('y u5 m', 1100 * 250, 275000), ('y u7 ve300', 2942 * log(1000 / 900), 310), ('y u9 F', 2 * .5 * 4500, 4500 * 2 * .5), ('y labC a15', aa(1.5), 1.176), ('y u2 eo2', bt(30) * ep(450, 250), .444),
     ('y fin eo2', .9 * 43e6, 3.87e7), ('y mid m', 50 * 9, 450)]
    return r
