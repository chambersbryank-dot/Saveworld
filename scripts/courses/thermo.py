"""Thermodynamics (ENGR 320): systems and properties, pure substances and property tables, work and heat, the first law for closed systems and control volumes, the second law, entropy, exergy, gas power cycles, and vapor power and refrigeration cycles.
Oct 25 2026, founder-approved four-year track, junior course 2. Same module fields as aero1.py / circuits.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, log, exp
ID = 'thermo'
STATUS = 'live'
YEAR = 3
PAGE = 'Thermodynamics.html'
CODE = 'ENGR 320'
TITLE = 'Thermodynamics'
LAB_NAME = 'Thermodynamics lab'
TAGLINE = 'Energy, entropy, cycles and engines: systems and properties, steam and ideal-gas tables, work and heat, the first law for closed systems and flowing devices, the second law and Carnot limits, entropy and isentropic efficiency, exergy, Otto, Diesel and Brayton cycles, and Rankine and refrigeration cycles, with six labs. Free, self-paced, and tied to power plants, heat pumps, combined heat and power, concentrating solar and geothermal energy.'
DESC = 'Free self-study Thermodynamics: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and home labs, practice exams, tied to heat pumps, power-plant efficiency and geothermal energy.'
ALT = 'NASA photo of the SLS core stage Green Run hot fire test'
_O = 'https://openstax.org/books/university-physics-volume-2/pages/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_G = 'https://www.grc.nasa.gov/www/k-12/airplane/'
_MIT = ('MIT OpenCourseWare 16.050 Thermal Energy (Fall 2002)', 'https://ocw.mit.edu/courses/16-050-thermal-energy-fall-2002/')
_MITU = ('MIT OpenCourseWare 16.01–16.04 Unified Engineering (2005–2006)', 'https://ocw.mit.edu/courses/16-01-unified-engineering-i-ii-iii-iv-fall-2005-spring-2006/')
_NIST = ('NIST Chemistry WebBook: Thermophysical properties of fluid systems', 'https://webbook.nist.gov/chemistry/fluid/')
_EIA = ('U.S. EIA: What is the efficiency of different types of power plants?', 'https://www.eia.gov/tools/faqs/faq.php?id=107&t=3')
_NUC = ('U.S. DOE: Nuclear 101: How does a nuclear reactor work? (May 2025)', 'https://www.energy.gov/ne/articles/nuclear-101-how-does-nuclear-reactor-work')
_CSP = ('U.S. DOE: Concentrating solar-thermal power basics', 'https://www.energy.gov/eere/solar/concentrating-solar-thermal-power-basics')
_HP = ('U.S. DOE: Pump up your savings with heat pumps (May 30, 2023)', 'https://www.energy.gov/articles/pump-your-savings-heat-pumps')
_CHP = ('U.S. DOE: Combined heat and power basics', 'https://www.energy.gov/eere/amo/combined-heat-and-power-basics')
_GEO = ('U.S. DOE: Geothermal basics', 'https://www.energy.gov/eere/geothermal/geothermal-basics')
_BRAY = ('NASA Glenn: Turbine engine thermodynamic cycle (Brayton cycle)', _G + 'brayton.html')
BANNER = ['images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg', 'images/SDO_Sun.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg']
CREDITS = {'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg': 'NASA/Michael DeMocker (MAF20210116_GR0006)', 'images/SDO_Sun.jpg': 'NASA/SDO',
           'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester junior engineering thermodynamics course. It is modeled on the topics and depth of MIT 16.050 Thermal Energy and the thermodynamics parts of MIT Unified Engineering (both free on MIT OpenCourseWare), and on courses such as Purdue ME 200 and Georgia Tech ME 3322, using the free OpenStax University Physics Volume 2 chapters on heat and the laws of thermodynamics and NIST’s free fluid property data, which we link where they help. None of those authors or schools endorses this page.',
         'What we add: every unit ties to real work with a cited public source (power-plant efficiency, nuclear and concentrating solar plants, heat pumps, combined heat and power and geothermal energy), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a safe home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Almost all electricity from fuel, uranium, concentrated sunlight or Earth’s heat comes from a thermodynamic cycle, and almost all heating and cooling runs on one too. The first law says energy is conserved; the second law says how much of it can become useful work. Between them they decide how much fuel the world burns.',
                 'Better cycles, recovered waste heat and heat pumps are some of the fastest ways to cut emissions. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values.']
PREREQS = ['Calculus II and III: integrals, partial derivatives and natural logarithms.', 'Physics I and General Chemistry I: energy, work, ideal gases and heat.',
           'Differential Equations is helpful but not required.', 'Comfort with spreadsheets for tables and interpolation.']
STUDY = ['Start every problem by drawing the system or control volume and saying whether it is closed or open, steady or not.', 'List the known states and look up properties before writing any balance.',
         'Write the energy balance in words first (energy in − energy out = change in stored energy), then cancel terms you can justify.', 'Keep units consistent: kJ, kPa, m³, kg and kelvin; never use °C inside a ratio of temperatures.',
         'Sketch every process on a T–s or p–v diagram; cycles become much easier to follow.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Gas Properties, Energy Forms and Changes and States of Matter simulations.', 'A kitchen thermometer (or a cheap digital probe), a measuring cup and a kitchen scale.',
            'An electric kettle with a known power rating, ice cubes, an insulated mug or foam cup.', 'A phone stopwatch.', 'Spreadsheet software for the cycle labs.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab can be done in a free simulation or with kitchen items. Hot water and steam scald: use oven mitts, keep the kettle on a stable counter, pour away from yourself, and keep children and pets clear. Never heat a sealed container.']
SAFETY_SRC = ('NFPA: Burn awareness information', 'https://www.nfpa.org/education-and-research/home-fire-safety/burns')
CONST_SRC = ('NIST: CODATA value of the molar gas constant', 'https://physics.nist.gov/cgi-bin/cuu/Value?r')
CONSTANTS = [('Universal gas constant', 'R_u = 8.314 kJ/(kmol·K)'), ('Air (ideal gas, room temperature, textbook values)', 'R = 0.287 kJ/(kg·K), c_p = 1.005, c_v = 0.718 kJ/(kg·K), k = 1.4'),
             ('Liquid water (textbook value)', 'c = 4.18 kJ/(kg·K)'), ('Latent heats (textbook values)', 'fusion of ice 334 kJ/kg; vaporization at 100 °C 2257 kJ/kg'),
             ('Energy units', '1 kWh = 3600 kJ; 1 Btu = 1.055 kJ; 1 kWh = 3412 Btu'), ('Absolute temperature', 'T(K) = T(°C) + 273.15')]
REF_TITLE = 'Free texts, data and simulations'
REF_INTRO = 'Use these free lectures, property data and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT lecture notes and problems.'), (_MITU[0], _MITU[1], 'Free MIT thermodynamics notes.'), ('OpenStax University Physics Volume 2, Chapter 3: The first law of thermodynamics', _O + '3-introduction', 'Free textbook chapter.'),
          ('OpenStax University Physics Volume 2, Chapter 4: The second law of thermodynamics', _O + '4-introduction', 'Free textbook chapter.'), (_NIST[0], _NIST[1], 'Free steam and refrigerant property tables.'),
          ('PhET: Gas Properties', _PH + 'gas-properties', 'Pressure, volume, temperature interactively.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Systems, Properties, Energy and Efficiency', 'weeks': 'Week 1',
 'summary': 'Closed systems, control volumes and surroundings, properties and states, equilibrium and quasi-equilibrium processes, temperature scales and the zeroth law, pressure, forms of energy, energy units, and efficiency as useful output over required input.',
 'objectives': ['Choose a system or control volume and its boundary.', 'Tell intensive from extensive properties, and state from path.', 'Convert between kJ, kWh and Btu, and between °C and K.', 'Compute an efficiency and a power plant’s efficiency from its heat rate.'],
 'concepts': ['A system is the region we study; a closed system exchanges energy but not mass with its surroundings, while a control volume (open system) lets mass cross its boundary.',
              'Properties such as pressure p, temperature T and specific volume v = V/m describe the state. Intensive properties (p, T, v) do not depend on size; extensive ones (V, m, E) do. Two independent intensive properties fix the state of a simple compressible substance.',
              'The zeroth law: two bodies each in thermal equilibrium with a third are in equilibrium with each other; it is why thermometers work. Absolute temperature T(K) = T(°C) + 273.15 must be used in every ratio and every gas law.',
              'Energy is stored as internal energy U, kinetic energy ½mV² and potential energy mgz, and it crosses a boundary only as heat Q or work W.',
              'Efficiency = useful output ÷ required input. For power plants, the U.S. EIA uses heat rate: Btu of fuel per kWh of electricity, with 1 kWh = 3412 Btu.'],
 'eqs': [('v=\\frac{V}{m},\\ \\ \\rho=\\frac1v', 'Specific volume and density'), ('T(\\mathrm K)=T(^\\circ\\mathrm C)+273.15', 'Absolute temperature'), ('E=U+\\tfrac12mV^2+mgz', 'Total stored energy'), ('\\eta=\\frac{3412\\ \\text{Btu/kWh}}{\\text{heat rate}}', 'Power-plant efficiency from heat rate (EIA)')],
 'worked': [
  {'q': 'EIA gives heat rates of 10,500 Btu/kWh and 7,500 Btu/kWh as examples. Find each efficiency.', 'steps': ['η = 3412/10,500.', 'η = 3412/7500.'], 'a': '32.5% and 45.5% (EIA rounds these to 33% and 45%).'},
  {'q': 'A tank holds 2 kg of gas in 0.5 m³. Find v and ρ.', 'steps': ['v = 0.5/2.', 'ρ = 1/v.'], 'a': 'v = 0.25 m³/kg, ρ = 4 kg/m³.'},
  {'q': 'A 1000 kg car at 30 m/s brakes to a stop. How much kinetic energy becomes internal energy of the brakes, in kJ and kWh?', 'steps': ['KE = ½ × 1000 × 30² = 450,000 J.', '450 kJ ÷ 3600 kJ/kWh.'], 'a': '450 kJ = 0.125 kWh.'}],
 'practice': [('Convert 25 °C to kelvin.', '298.15 K.'), ('Is temperature intensive or extensive?', 'Intensive.'),
              ('A plant has a heat rate of 9000 Btu/kWh. Find its efficiency.', '3412/9000 = 37.9%.'), ('Convert 1 MWh to GJ.', '3600 MJ = 3.6 GJ.')],
 'misc': [('Heat and temperature are the same thing.', 'Temperature is a property; heat is energy in transit.'), ('A system “contains heat.”', 'It contains internal energy; heat exists only crossing a boundary.'),
          ('Ratios can use °C.', 'Gas laws and efficiencies need kelvin.')],
 'quiz': [{'q': 'A control volume allows…', 'opts': ['mass to cross its boundary', 'no energy transfer', 'only heat', 'nothing'], 'ok': 0, 'why': 'Open system.'},
          {'q': 'Which is intensive?', 'opts': ['volume', 'mass', 'pressure', 'energy'], 'ok': 2, 'why': 'Independent of size.'},
          {'q': 'A heat rate of 6824 Btu/kWh means efficiency of…', 'opts': ['25%', '50%', '68%', '100%'], 'ok': 1, 'why': '3412/6824.'},
          {'q': 'Energy crosses a closed-system boundary as…', 'opts': ['mass', 'heat and work', 'temperature', 'pressure'], 'ok': 1, 'why': 'Only two ways.'}],
 'cards': [('System', 'Region under study.'), ('Control volume', 'Mass can cross.'), ('Specific volume', 'v = V/m.'), ('Zeroth law', 'Basis of thermometers.'), ('Heat rate', 'Btu per kWh.'), ('1 kWh', '3600 kJ = 3412 Btu.')],
 'planet': {'text': ['The U.S. Energy Information Administration measures power-plant efficiency with the heat rate: the fuel energy a plant uses to deliver one kilowatthour to the grid, counting the electricity the plant itself uses for fuel feeding, boiler pumps, cooling and pollution control. Dividing 3,412 Btu (the energy in one kWh) by the heat rate gives efficiency; EIA’s examples are a 10,500 Btu plant at about 33% and a 7,500 Btu plant at about 45%.',
                     'That gap is the whole point of this course. For the same electricity, the 7,500 Btu plant burns 7,500/10,500 = 71.4% as much fuel, so about 28.6% less fuel and CO₂. The laws of thermodynamics explain where the rest of the energy goes and how engineers claw some of it back.'],
            'site': [('Solutions', 'Solutions.html'), ('Circuits', 'Circuits.html')],
            'src': [_EIA]},
 'res': [('OpenStax UP2, 1.1 Temperature and thermal equilibrium', _O + '1-1-temperature-and-thermal-equilibrium', 'Free textbook section.'), ('OpenStax UP2, 3.1 Thermodynamic systems', _O + '3-1-thermodynamic-systems', 'Free textbook section.'),
         (_MIT[0], _MIT[1], 'MIT thermal energy notes.'), ('NASA Glenn: First law of thermodynamics', _G + 'thermo1.html', 'Free NASA page.')]})
UNITS.append(
{'id': 'u2', 'title': 'Pure Substances, Phase Change and Property Tables', 'weeks': 'Weeks 2–3',
 'summary': 'Phases and phase change, saturation temperature and pressure, compressed liquid, saturated mixture and superheated vapor, quality, T–v and p–v diagrams, steam tables and interpolation, the ideal-gas equation and when it applies, and the compressibility factor.',
 'objectives': ['Identify the phase from p and T using saturation data.', 'Use quality to find v, u and h of a saturated mixture.', 'Interpolate in property tables.', 'Use the ideal-gas law and know when it fails.'],
 'concepts': ['A pure substance has a fixed chemical makeup. At a given pressure, water boils at one saturation temperature (99.61 °C at 100 kPa); while it boils, p and T stay fixed and the mixture’s quality x = m_vapor/m_total grows from 0 to 1.',
              'For a saturated mixture any specific property is y = y_f + x(y_g − y_f) = y_f + x·y_fg, using saturated-liquid (f) and saturated-vapor (g) values from the tables.',
              'If T is below the saturation temperature at that pressure, the water is a compressed liquid (approximately saturated liquid at T); if above, it is superheated vapor, found in separate tables.',
              'Linear interpolation: y = y₁ + (x − x₁)(y₂ − y₁)/(x₂ − x₁). NIST’s free WebBook gives the same data for water and many refrigerants.',
              'At low pressure and high temperature relative to the critical point, gases obey pv = RT with R = R_u/M; for air R = 0.287 kJ/(kg·K). Near saturation (steam in a boiler) use the tables instead.'],
 'eqs': [('x=\\frac{m_g}{m_f+m_g}', 'Quality'), ('y=y_f+x\\,y_{fg}', 'Saturated-mixture property'), ('pv=RT,\\ \\ R=\\frac{R_u}{M}', 'Ideal-gas law'), ('y=y_1+\\frac{x-x_1}{x_2-x_1}(y_2-y_1)', 'Linear interpolation')],
 'worked': [
  {'q': 'At 100 kPa, h_f = 417.51 and h_fg = 2257.5 kJ/kg, v_f = 0.001043 and v_g = 1.6941 m³/kg (steam tables). Find h and v at quality 0.6.', 'steps': ['h = 417.51 + 0.6 × 2257.5.', 'v = 0.001043 + 0.6 × (1.6941 − 0.001043).'], 'a': 'h = 1772.0 kJ/kg; v = 1.0169 m³/kg.'},
  {'q': 'Find the mass of air in a 0.5 m³ tank at 100 kPa and 300 K.', 'steps': ['m = pV/(RT) = 100 × 0.5/(0.287 × 300).'], 'a': 'm = 0.581 kg.'},
  {'q': 'Find the pressure of 2 kg of air in 0.5 m³ at 400 K.', 'steps': ['p = mRT/V = 2 × 0.287 × 400/0.5.'], 'a': 'p = 459.2 kPa.'}],
 'practice': [('Water at 100 kPa and 80 °C is…', 'Compressed liquid (80 °C < 99.61 °C).'), ('Water at 100 kPa and 150 °C is…', 'Superheated vapor.'),
              ('Interpolate h at 25 °C if h = 83.9 at 20 °C and 125.7 at 30 °C (kJ/kg, saturated liquid).', '83.9 + 0.5 × 41.8 = 104.8 kJ/kg.'), ('Find R for helium (M = 4.003 kg/kmol).', '8.314/4.003 = 2.077 kJ/(kg·K).')],
 'misc': [('Temperature rises while water boils.', 'At constant pressure it stays at T_sat until all the liquid is gone.'), ('Steam in a boiler is an ideal gas.', 'Near saturation it is not; use steam tables.'),
          ('Quality applies to superheated vapor.', 'Only to saturated mixtures, 0 ≤ x ≤ 1.')],
 'quiz': [{'q': 'Quality is…', 'opts': ['vapor mass over total mass', 'liquid mass over total', 'temperature ratio', 'pressure ratio'], 'ok': 0, 'why': 'x = m_g/m.'},
          {'q': 'Water at 100 kPa and 120 °C is…', 'opts': ['compressed liquid', 'saturated mixture', 'superheated vapor', 'solid'], 'ok': 2, 'why': 'Above T_sat.'},
          {'q': 'R for air is about…', 'opts': ['8.314', '0.287', '1.005', '4.18'], 'ok': 1, 'why': 'kJ/(kg·K).'},
          {'q': 'During boiling at constant p, T…', 'opts': ['rises', 'falls', 'stays constant', 'oscillates'], 'ok': 2, 'why': 'Saturation.'}],
 'cards': [('Saturation', 'Liquid and vapor coexist at T_sat(p).'), ('Quality', 'x = m_g/m.'), ('Mixture property', 'y_f + x y_fg.'), ('Compressed liquid', 'T < T_sat.'), ('Superheated', 'T > T_sat.'), ('Ideal gas', 'pv = RT.')],
 'planet': {'text': ['The U.S. Department of Energy explains that nuclear reactors use fission heat to make steam that spins a turbine. All U.S. commercial reactors are light-water reactors: more than 65% are pressurized-water reactors, which keep core water under high pressure so it does not boil and make steam in a separate heat exchanger, and roughly a third are boiling-water reactors, which make steam directly in the vessel.',
                     'Both designs are exercises in this unit: raising the pressure raises the saturation temperature so water stays liquid, and the steam’s quality and enthalpy set how much work the turbine gets. DOE counts more than 400 commercial reactors worldwide, including 94 in the United States, all built on steam tables.'],
            'site': [('Solutions', 'Solutions.html'), ('General Chemistry I', 'General_Chemistry_I.html')],
            'src': [_NUC, _NIST]},
 'res': [(_NIST[0], _NIST[1], 'Free steam tables.'), ('OpenStax UP2, 1.5 Phase changes', _O + '1-5-phase-changes', 'Free textbook section.'), ('OpenStax UP2, 2.1 Molecular model of an ideal gas', _O + '2-1-molecular-model-of-an-ideal-gas', 'Free textbook section.'),
         ('PhET: States of Matter', _PH + 'states-of-matter', 'Phase change interactively.')]})
UNITS.append(
{'id': 'u3', 'title': 'Energy Transfer by Work and Heat', 'weeks': 'Week 4',
 'summary': 'Sign conventions, boundary work and its area on a p–V diagram, constant-pressure, isothermal and polytropic processes, shaft and electrical work, and the three modes of heat transfer: conduction, convection and radiation.',
 'objectives': ['Compute boundary work for common processes.', 'Show that work and heat are path functions.', 'Compute shaft and electrical work and power.', 'Estimate conduction and convection heat rates.'],
 'concepts': ['Sign convention: heat into the system and work done by the system are positive (Q_in, W_out). Both are path functions: they depend on the process, not just the end states.',
              'Boundary work W_b = ∫p dV is the area under the process curve on a p–V diagram. At constant pressure W_b = p(V₂ − V₁).',
              'For an ideal gas at constant temperature, W_b = mRT ln(V₂/V₁). For a polytropic process pVⁿ = constant (n ≠ 1), W_b = (p₂V₂ − p₁V₁)/(1 − n).',
              'Shaft work: power = torque × angular speed, Ẇ = 2πṅT. Electrical work: W = VIΔt = PΔt.',
              'Heat moves by conduction (Q̇ = kAΔT/L through a wall), convection (Q̇ = hAΔT to a moving fluid) and radiation (Q̇ = εσA(T_s⁴ − T_surr⁴)). Insulation lowers k; this is why building envelopes matter.'],
 'eqs': [('W_b=\\int_1^2 p\\,dV', 'Boundary work'), ('W_b=mRT\\ln\\frac{V_2}{V_1}', 'Isothermal ideal gas'), ('W_b=\\frac{p_2V_2-p_1V_1}{1-n}', 'Polytropic process'), ('\\dot Q=\\frac{kA\\,\\Delta T}{L},\\ \\ \\dot Q=hA\\,\\Delta T', 'Conduction and convection')],
 'worked': [
  {'q': '1 kg of air expands isothermally at 300 K to twice its volume. Find the work.', 'steps': ['W = 1 × 0.287 × 300 × ln 2.'], 'a': 'W = 59.7 kJ (done by the gas).'},
  {'q': 'Air is compressed polytropically (n = 1.3) from 100 kPa and 0.2 m³ to 0.1 m³. Find p₂ and the work.', 'steps': ['p₂ = 100 × 2^1.3 = 246.2 kPa.', 'W = (246.2 × 0.1 − 100 × 0.2)/(1 − 1.3).'], 'a': 'p₂ = 246.2 kPa; W = −15.4 kJ (work done on the gas).'},
  {'q': 'A wall of area 10 m², thickness 0.1 m and k = 0.04 W/(m·K) (sample insulation) has 20 K across it. Find the heat loss.', 'steps': ['Q̇ = 0.04 × 10 × 20/0.1.'], 'a': 'Q̇ = 80 W.'}],
 'practice': [('Gas expands at a constant 200 kPa from 0.5 to 0.8 m³. Work?', '200 × 0.3 = 60 kJ.'), ('A shaft delivers 50 N·m at 3000 rpm. Power?', '2π × 50 × 50 = 15.7 kW.'),
              ('A 1500 W heater runs 10 minutes. Electrical work?', '1500 × 600 = 900 kJ.'), ('Convection: h = 10 W/(m²·K), A = 2 m², ΔT = 30 K. Heat rate?', '600 W.')],
 'misc': [('Work is a property of the state.', 'It depends on the path.'), ('A rigid tank can do boundary work.', 'No; dV = 0.'),
          ('Doubling insulation thickness halves the temperature.', 'It halves the conduction heat rate at the same ΔT.')],
 'quiz': [{'q': 'Boundary work equals…', 'opts': ['∫V dp', '∫p dV', 'pV', 'mRT'], 'ok': 1, 'why': 'Area under p–V curve.'},
          {'q': 'Isothermal ideal-gas work is…', 'opts': ['mRT ln(V₂/V₁)', 'p ΔV', 'mc_vΔT', '0'], 'ok': 0, 'why': 'pV = const.'},
          {'q': 'Heat and work are…', 'opts': ['properties', 'path functions', 'always equal', 'intensive'], 'ok': 1, 'why': 'Depend on the process.'},
          {'q': 'Conduction heat rate is proportional to…', 'opts': ['1/k', 'L', 'ΔT/L', 'T⁴'], 'ok': 2, 'why': 'kAΔT/L.'}],
 'cards': [('Sign convention', 'Q in, W out positive.'), ('Boundary work', '∫p dV.'), ('Isothermal', 'mRT ln(V₂/V₁).'), ('Polytropic', '(p₂V₂ − p₁V₁)/(1 − n).'), ('Shaft power', '2πṅT.'), ('Conduction', 'kAΔT/L.')],
 'planet': {'text': ['The U.S. Department of Energy explains that concentrating solar-thermal power uses mirrors to concentrate sunlight onto a receiver, heating a high-temperature fluid. That heat spins a turbine or powers an engine to make electricity, and it can also serve industry, from desalination to food processing and chemical production.',
                     'DOE notes that utility-scale plants use power towers or rows of linear mirrors, while single dish/engine systems produce 5 to 25 kilowatts each. Every one of them is a heat-transfer and work problem: absorb concentrated radiation, limit conduction and convection losses from the receiver, and turn the heat into shaft work.'],
            'site': [('Solutions', 'Solutions.html'), ('Physics II', 'Physics_II.html')],
            'src': [_CSP]},
 'res': [('OpenStax UP2, 3.2 Work, heat and internal energy', _O + '3-2-work-heat-and-internal-energy', 'Free textbook section.'), ('OpenStax UP2, 1.6 Mechanisms of heat transfer', _O + '1-6-mechanisms-of-heat-transfer', 'Free textbook section.'),
         (_MIT[0], _MIT[1], 'Work and heat lectures.'), ('PhET: Energy Forms and Changes', _PH + 'energy-forms-and-changes', 'Energy transfer interactively.')]})
UNITS.append(
{'id': 'u4', 'title': 'The First Law for Closed Systems', 'weeks': 'Week 5',
 'summary': 'Energy balance for closed systems, internal energy and enthalpy, specific heats of ideal gases, liquids and solids, constant-volume and constant-pressure heating, latent heat, and energy balances for cycles.',
 'objectives': ['Write and apply Q − W = ΔU + ΔKE + ΔPE.', 'Use c_v and c_p for ideal gases, and c for liquids and solids.', 'Include latent heat in phase-change problems.', 'Show that for a cycle the net heat equals the net work.'],
 'concepts': ['First law for a closed system: Q − W = ΔE = ΔU + ΔKE + ΔPE. Usually ΔKE and ΔPE are negligible, so Q − W = ΔU.',
              'Enthalpy h = u + pv. At constant pressure, the heat added equals the enthalpy change: Q = m(h₂ − h₁), because the boundary work is already included.',
              'For ideal gases u and h depend only on T: Δu = c_vΔT, Δh = c_pΔT, with c_p − c_v = R and k = c_p/c_v (1.4 for air).',
              'For liquids and solids c_p ≈ c_v = c, so Q = mcΔT. Melting or boiling at constant T needs latent heat: Q = m h_if or m h_fg.',
              'Over a full cycle the system returns to its starting state, so ΔU = 0 and Q_net = W_net. This is the basis of every engine and refrigerator.'],
 'eqs': [('Q-W=\\Delta U+\\Delta KE+\\Delta PE', 'First law, closed system'), ('h=u+pv', 'Enthalpy'), ('\\Delta u=c_v\\Delta T,\\ \\Delta h=c_p\\Delta T,\\ c_p-c_v=R', 'Ideal-gas specific heats'), ('Q=mc\\Delta T,\\ \\ Q=m\\,h_{fg}', 'Sensible and latent heat')],
 'worked': [
  {'q': '2 kg of air in a rigid tank is heated from 300 K to 400 K. Find Q.', 'steps': ['W = 0 (rigid).', 'Q = m c_v ΔT = 2 × 0.718 × 100.'], 'a': 'Q = 143.6 kJ.'},
  {'q': 'The same air is heated at constant pressure (100 kPa) from 300 to 400 K. Find Q and the boundary work.', 'steps': ['Q = m c_p ΔT = 2 × 1.005 × 100.', 'W = mRΔT = 2 × 0.287 × 100.'], 'a': 'Q = 201.0 kJ; W = 57.4 kJ; ΔU = 143.6 kJ either way.'},
  {'q': 'Find the heat to warm 1 kg of water from 20 °C to 100 °C, and then to boil 0.1 kg of it away.', 'steps': ['Q₁ = 1 × 4.18 × 80.', 'Q₂ = 0.1 × 2257.'], 'a': 'Q₁ = 334.4 kJ; Q₂ = 225.7 kJ.'}],
 'practice': [('Melt 0.2 kg of ice at 0 °C. Heat?', '0.2 × 334 = 66.8 kJ.'), ('Find c_p − c_v for air.', '1.005 − 0.718 = 0.287 kJ/(kg·K) = R.'),
              ('A cycle receives 500 kJ of heat and rejects 300 kJ. Net work?', '200 kJ.'), ('Find k for air.', '1.005/0.718 = 1.40.')],
 'misc': [('Heat added always raises temperature.', 'During phase change it does not.'), ('Q = mc_pΔT works for a rigid tank.', 'Use c_v when volume is constant.'),
          ('Enthalpy is a form of heat.', 'It is a property, u + pv.')],
 'quiz': [{'q': 'For a rigid closed tank, Q equals…', 'opts': ['ΔH', 'ΔU', 'W', '0'], 'ok': 1, 'why': 'No boundary work.'},
          {'q': 'c_p − c_v for an ideal gas is…', 'opts': ['k', 'R', '1', 'c_v'], 'ok': 1, 'why': 'Mayer’s relation.'},
          {'q': 'Over a cycle, ΔU is…', 'opts': ['positive', 'negative', 'zero', 'Q'], 'ok': 2, 'why': 'Same start and end state.'},
          {'q': 'At constant pressure, Q equals…', 'opts': ['ΔU', 'ΔH', 'W', 'pV'], 'ok': 1, 'why': 'h = u + pv.'}],
 'cards': [('First law', 'Q − W = ΔU.'), ('Enthalpy', 'h = u + pv.'), ('Ideal gas Δu', 'c_vΔT.'), ('Ideal gas Δh', 'c_pΔT.'), ('Latent heat', 'Q = m h_fg.'), ('Cycle', 'Q_net = W_net.')],
 'planet': {'text': ['DOE reports that heat pumps are growing fast: as of 2020 over 17 million U.S. housing units had them, and they now account for more than half of all residential heating equipment sales in the United States. They work like a refrigerator, using electricity to move heat from a cool space to a warm one rather than making heat.',
                     'The first law is why that matters: an electric resistance heater turns each kWh of electricity into exactly one kWh of heat, but a heat pump delivers the electricity plus the heat it pulls from outside. DOE says modern air-source heat pumps can cut electricity use by 50% compared with furnaces and baseboard heaters, and that switching could save up to 7.6 tons of carbon emissions a year depending on the equipment replaced.'],
            'site': [('Solutions', 'Solutions.html'), ('Calculus II', 'Calculus_II.html')],
            'src': [_HP]},
 'res': [('OpenStax UP2, 3.3 First law of thermodynamics', _O + '3-3-first-law-of-thermodynamics', 'Free textbook section.'), ('OpenStax UP2, 3.5 Heat capacities of an ideal gas', _O + '3-5-heat-capacities-of-an-ideal-gas', 'Free textbook section.'),
         ('NASA Glenn: First law of thermodynamics', _G + 'thermo1.html', 'Free NASA page.'), (_MITU[0], _MITU[1], 'First-law notes.')]})
UNITS.append(
{'id': 'u5', 'title': 'The First Law for Control Volumes: Steady-Flow Devices', 'weeks': 'Weeks 6–7',
 'summary': 'Mass and energy balances for control volumes, flow work and enthalpy, steady-flow devices (nozzles and diffusers, turbines and compressors, pumps, throttling valves, mixing chambers and heat exchangers), and an introduction to unsteady filling.',
 'objectives': ['Write steady-flow mass and energy balances.', 'Explain why enthalpy appears for flowing streams.', 'Analyze nozzles, turbines, compressors, throttles and heat exchangers.', 'Choose which terms can be neglected for each device.'],
 'concepts': ['Mass balance: in steady flow, Σṁ_in = Σṁ_out, with ṁ = ρAV.',
              'Pushing fluid across a boundary takes flow work pv per unit mass; adding it to u gives enthalpy h, which is why open-system balances use h.',
              'Steady-flow energy equation, one inlet and one outlet: Q̇ − Ẇ = ṁ[(h₂ − h₁) + (V₂² − V₁²)/2 + g(z₂ − z₁)].',
              'Device shortcuts: nozzles trade enthalpy for speed (Q̇ = Ẇ = 0); turbines and compressors are near adiabatic with Ẇ = ṁ(h₁ − h₂); throttling valves keep h₁ = h₂; heat exchangers have Ẇ = 0 and the heat lost by one stream equals that gained by the other.',
              'Remember the units: kinetic energy in J/kg must be divided by 1000 to add to kJ/kg enthalpy.'],
 'eqs': [('\\sum\\dot m_{in}=\\sum\\dot m_{out}', 'Steady mass balance'), ('\\dot Q-\\dot W=\\dot m\\left[\\Delta h+\\frac{\\Delta V^2}{2}+g\\Delta z\\right]', 'Steady-flow energy equation'), ('\\dot W_{turb}=\\dot m(h_1-h_2)', 'Adiabatic turbine'), ('h_1=h_2', 'Throttling valve')],
 'worked': [
  {'q': 'Air enters an adiabatic nozzle slowly at 400 K and leaves at 350 K. Find the exit speed.', 'steps': ['Δh = c_pΔT = 1.005 × 50 = 50.25 kJ/kg = 50,250 J/kg.', 'V₂ = √(2 × 50,250).'], 'a': 'V₂ = 317.0 m/s.'},
  {'q': 'Steam flows at 5 kg/s through an adiabatic turbine from h₁ = 3116.1 to h₂ = 2403.0 kJ/kg. Find the power.', 'steps': ['Ẇ = 5 × (3116.1 − 2403.0).'], 'a': 'Ẇ = 3565.5 kW ≈ 3.57 MW.'},
  {'q': 'An adiabatic compressor takes 1.2 kg/s of air from 300 K to 450 K. Find the power input.', 'steps': ['Ẇ_in = ṁc_pΔT = 1.2 × 1.005 × 150.'], 'a': '180.9 kW.'}],
 'practice': [('Water at 0.5 kg/s is heated from 15 to 45 °C in a heat exchanger. Heat rate?', '0.5 × 4.18 × 30 = 62.7 kW.'), ('Steam is throttled from h = 2800 kJ/kg. Exit h?', '2800 kJ/kg.'),
              ('Convert a speed change from 0 to 100 m/s into kJ/kg.', '100²/2 = 5000 J/kg = 5 kJ/kg.'), ('A pipe has ṁ = 2 kg/s at inlet. Outlet in steady flow?', '2 kg/s.')],
 'misc': [('Turbine power uses u.', 'Flowing streams use h, which includes flow work.'), ('A throttle lowers enthalpy.', 'h stays constant; p and usually T drop.'),
          ('Kinetic energy is always negligible.', 'Not in nozzles and diffusers.')],
 'quiz': [{'q': 'For a throttling valve…', 'opts': ['h₁ = h₂', 'T₁ = T₂', 'p₁ = p₂', 'W > 0'], 'ok': 0, 'why': 'No work, no heat, small ΔKE.'},
          {'q': 'Enthalpy appears in open systems because of…', 'opts': ['flow work', 'friction', 'gravity', 'radiation'], 'ok': 0, 'why': 'h = u + pv.'},
          {'q': 'A nozzle converts…', 'opts': ['speed into enthalpy', 'enthalpy into speed', 'work into heat', 'mass into energy'], 'ok': 1, 'why': 'Accelerates flow.'},
          {'q': 'Adiabatic turbine power is…', 'opts': ['ṁ(h₁ − h₂)', 'ṁ(h₂ − h₁)', 'Q̇', '0'], 'ok': 0, 'why': 'Enthalpy drop.'}],
 'cards': [('Steady mass', 'ṁ in = ṁ out.'), ('Flow work', 'pv per kg.'), ('SFEE', 'Q̇ − Ẇ = ṁΔ(h + V²/2 + gz).'), ('Turbine', 'ṁ(h₁ − h₂).'), ('Throttle', 'h₁ = h₂.'), ('Heat exchanger', 'Heat lost = heat gained.')],
 'planet': {'text': ['DOE describes the core of a nuclear plant as a chain of steady-flow devices: fission heats water, a heat exchanger (in pressurized-water reactors) makes steam in a separate loop, the steam spins a turbine connected to a generator, and leftover steam is condensed back to water and pumped back to be reheated.',
                     'Each box is one steady-flow energy equation. Geothermal plants, which DOE says draw hot fluid up through wells and convert its heat to steam that drives turbines, use the same devices with Earth’s heat as the source. Getting a few more kJ per kg out of every turbine stage is how plant efficiency climbs.'],
            'site': [('Solutions', 'Solutions.html'), ('Aerodynamics I', 'Aerodynamics_I.html')],
            'src': [_NUC, _GEO]},
 'res': [('OpenStax UP2, 3.4 Thermodynamic processes', _O + '3-4-thermodynamic-processes', 'Free textbook section.'), (_MIT[0], _MIT[1], 'Control-volume lectures.'), (_NIST[0], _NIST[1], 'Steam data.'), (_MITU[0], _MITU[1], 'Steady-flow notes.')]})
UNITS.append(
{'id': 'u6', 'title': 'The Second Law: Heat Engines, Refrigerators and Carnot Limits', 'weeks': 'Week 8',
 'summary': 'Thermal reservoirs, heat engines and thermal efficiency, refrigerators, heat pumps and COP, the Kelvin–Planck and Clausius statements, reversible and irreversible processes, the Carnot cycle, and the Carnot limits on efficiency and COP.',
 'objectives': ['Compute thermal efficiency and COP.', 'State the Kelvin–Planck and Clausius statements.', 'Identify sources of irreversibility.', 'Use Carnot limits to judge whether a claimed device is possible.'],
 'concepts': ['A heat engine takes Q_H from a hot reservoir, rejects Q_L to a cold one, and produces W = Q_H − Q_L. Thermal efficiency η = W/Q_H = 1 − Q_L/Q_H.',
              'Kelvin–Planck: no cycle can turn all the heat from a single reservoir into work, so η < 100%. Clausius: heat does not flow from cold to hot by itself; a refrigerator or heat pump needs work input.',
              'COP_R = Q_L/W for a refrigerator; COP_HP = Q_H/W = COP_R + 1 for a heat pump. COP can be well above 1, which is why heat pumps beat resistance heaters.',
              'Irreversibilities (friction, heat transfer across a finite ΔT, unrestrained expansion, mixing) reduce performance. A reversible cycle between two reservoirs, the Carnot cycle, is the best possible.',
              'Carnot limits use absolute temperatures: η_Carnot = 1 − T_L/T_H, COP_R,Carnot = T_L/(T_H − T_L), COP_HP,Carnot = T_H/(T_H − T_L).'],
 'eqs': [('\\eta=\\frac{W}{Q_H}=1-\\frac{Q_L}{Q_H}', 'Thermal efficiency'), ('COP_R=\\frac{Q_L}{W},\\ COP_{HP}=\\frac{Q_H}{W}', 'Coefficients of performance'), ('\\eta_{Carnot}=1-\\frac{T_L}{T_H}', 'Carnot efficiency'), ('COP_{HP,Carnot}=\\frac{T_H}{T_H-T_L}', 'Carnot heat pump')],
 'worked': [
  {'q': 'An engine takes 1000 kJ of heat and produces 350 kJ of work. Find η and Q_L.', 'steps': ['η = 350/1000.', 'Q_L = 1000 − 350.'], 'a': 'η = 35%; Q_L = 650 kJ.'},
  {'q': 'Find the Carnot efficiency between 800 K and 300 K, and between 1073 K and 293 K.', 'steps': ['1 − 300/800.', '1 − 293/1073.'], 'a': '62.5% and 72.7%.'},
  {'q': 'A heat pump keeps a house at 294 K when it is 273 K outside. Find the Carnot COP, and the heat delivered by a real unit with COP = 3 (sample value) using 3 kWh.', 'steps': ['COP = 294/(294 − 273).', 'Q_H = 3 × 3.'], 'a': 'COP_Carnot = 14.0; the real unit delivers 9 kWh of heat.'}],
 'practice': [('A fridge has COP_R = 2.5 and removes 500 kJ. Work?', '200 kJ.'), ('Find COP_HP if COP_R = 2.5.', '3.5.'),
              ('A fridge works between 275 K and 298 K. Carnot COP_R?', '275/23 = 11.96.'), ('An inventor claims 70% efficiency between 600 K and 300 K. Possible?', 'No: Carnot limit is 50%.')],
 'misc': [('COP above 1 breaks energy conservation.', 'The heat pump moves heat; it does not create it.'), ('Carnot efficiency can use °C.', 'It must use kelvin.'),
          ('Better engineering can reach 100% efficiency.', 'Kelvin–Planck forbids it.')],
 'quiz': [{'q': 'Carnot efficiency between 600 K and 300 K is…', 'opts': ['25%', '50%', '75%', '100%'], 'ok': 1, 'why': '1 − 0.5.'},
          {'q': 'COP_HP − COP_R equals…', 'opts': ['0', '1', 'η', 'T_H'], 'ok': 1, 'why': 'Q_H = Q_L + W.'},
          {'q': 'Which statement forbids a 100% efficient engine?', 'opts': ['Clausius', 'Kelvin–Planck', 'Zeroth law', 'First law'], 'ok': 1, 'why': 'Single-reservoir statement.'},
          {'q': 'Which is an irreversibility?', 'opts': ['friction', 'quasi-equilibrium compression', 'isentropic expansion', 'none'], 'ok': 0, 'why': 'Dissipation.'}],
 'cards': [('Efficiency', 'W/Q_H.'), ('COP_R', 'Q_L/W.'), ('COP_HP', 'Q_H/W.'), ('Kelvin–Planck', 'No 100% engine.'), ('Clausius', 'No cold-to-hot without work.'), ('Carnot', '1 − T_L/T_H.')],
 'planet': {'text': ['DOE describes heat pumps as moving heat rather than generating it, which makes them significantly more efficient than traditional heating. Modern air-source heat pumps can cut electricity use by 50% compared with furnaces and baseboard heaters, and geothermal heat pumps, which use the steady temperature of the shallow ground, can reduce energy use by 30% to 60%.',
                     'The Carnot COP explains both claims: the smaller the temperature lift T_H − T_L, the higher the COP. The ground stays milder than winter air, so a ground-source heat pump lifts heat across a smaller gap. DOE’s geothermal office sees potential for up to 28 million geothermal heat pumps by 2050.'],
            'site': [('Solutions', 'Solutions.html'), ('Oceans', 'Oceans.html')],
            'src': [_HP, _GEO]},
 'res': [('OpenStax UP2, 4.2 Heat engines', _O + '4-2-heat-engines', 'Free textbook section.'), ('OpenStax UP2, 4.3 Refrigerators and heat pumps', _O + '4-3-refrigerators-and-heat-pumps', 'Free textbook section.'),
         ('OpenStax UP2, 4.5 The Carnot cycle', _O + '4-5-the-carnot-cycle', 'Free textbook section.'), ('NASA Glenn: Carnot cycle', _G + 'carnot.html', 'Free NASA page.')]})
UNITS.append(
{'id': 'u7', 'title': 'Entropy and Isentropic Efficiency', 'weeks': 'Weeks 9–10',
 'summary': 'The Clausius inequality, entropy as a property, the increase-of-entropy principle and entropy generation, the T ds relations, entropy change of liquids, solids and ideal gases, isentropic processes, T–s diagrams, and isentropic efficiencies of turbines, compressors and nozzles.',
 'objectives': ['Compute entropy changes for liquids, solids and ideal gases.', 'Find entropy generation and decide if a process is possible.', 'Use isentropic relations for ideal gases.', 'Apply isentropic efficiencies to real devices.'],
 'concepts': ['Entropy S is a property defined by dS = δQ_rev/T. For any process, S₂ − S₁ ≥ ∫δQ/T; the difference is the entropy generated, S_gen ≥ 0 (zero only if reversible).',
              'Increase-of-entropy principle: the entropy of an isolated system (system plus surroundings) never decreases. A process with S_gen < 0 is impossible.',
              'T ds relations: T ds = du + p dv = dh − v dp. For liquids and solids Δs = c ln(T₂/T₁); for ideal gases Δs = c_p ln(T₂/T₁) − R ln(p₂/p₁).',
              'An isentropic (reversible adiabatic) ideal-gas process with constant specific heats has T₂/T₁ = (p₂/p₁)^((k−1)/k). On a T–s diagram it is a vertical line, and the area under a reversible process is the heat transferred.',
              'Real devices are compared with isentropic ones: η_T = (h₁ − h₂a)/(h₁ − h₂s) for turbines and η_C = (h₂s − h₁)/(h₂a − h₁) for compressors.'],
 'eqs': [('dS=\\frac{\\delta Q_{rev}}{T},\\ \\ S_{gen}\\ge0', 'Entropy and the second law'), ('\\Delta s=c\\ln\\frac{T_2}{T_1}', 'Liquids and solids'), ('\\Delta s=c_p\\ln\\frac{T_2}{T_1}-R\\ln\\frac{p_2}{p_1}', 'Ideal gas'), ('\\frac{T_2}{T_1}=\\left(\\frac{p_2}{p_1}\\right)^{(k-1)/k}', 'Isentropic ideal gas')],
 'worked': [
  {'q': 'Find the entropy change of 2 kg of water heated from 293 K to 353 K.', 'steps': ['ΔS = 2 × 4.18 × ln(353/293).'], 'a': 'ΔS = 1.557 kJ/K.'},
  {'q': 'Air goes from 300 K and 100 kPa to 500 K and 400 kPa. Find Δs.', 'steps': ['Δs = 1.005 ln(500/300) − 0.287 ln(400/100).'], 'a': 'Δs = 0.1155 kJ/(kg·K).'},
  {'q': 'Air at 300 K is compressed through a pressure ratio of 8. Find the isentropic exit temperature and the actual one if η_C = 0.85.', 'steps': ['T₂s = 300 × 8^(0.4/1.4) = 543.4 K.', 'T₂a = 300 + (543.4 − 300)/0.85.'], 'a': 'T₂s = 543.4 K; T₂a = 586.4 K.'}],
 'practice': [('1000 kJ of heat flows from an 800 K reservoir to a 300 K one. S_gen?', '1000/300 − 1000/800 = 2.083 kJ/K.'), ('Isentropic T₂ for a pressure ratio of 10 from 300 K?', '579.2 K.'),
              ('Can S_gen be negative?', 'No; that process is impossible.'), ('What does area under a reversible T–s curve represent?', 'Heat transferred.')],
 'misc': [('Entropy can never decrease.', 'A system’s entropy can fall if it rejects heat; the total for an isolated system cannot.'), ('Adiabatic means isentropic.', 'Only if also reversible.'),
          ('Isentropic efficiency can exceed 1.', 'Not for turbines or compressors.')],
 'quiz': [{'q': 'S_gen for a reversible process is…', 'opts': ['positive', 'zero', 'negative', 'infinite'], 'ok': 1, 'why': 'No irreversibility.'},
          {'q': 'An isentropic process on a T–s diagram is…', 'opts': ['horizontal', 'vertical', 'diagonal', 'circular'], 'ok': 1, 'why': 's constant.'},
          {'q': 'Δs for a liquid heated is…', 'opts': ['c ln(T₂/T₁)', 'cΔT', 'R ln(p₂/p₁)', '0'], 'ok': 0, 'why': 'Incompressible.'},
          {'q': 'Compressor isentropic efficiency is…', 'opts': ['(h₂s − h₁)/(h₂a − h₁)', '(h₂a − h₁)/(h₂s − h₁)', 'h₂/h₁', '1'], 'ok': 0, 'why': 'Ideal work over actual.'}],
 'cards': [('Entropy', 'dS = δQ_rev/T.'), ('S_gen', '≥ 0.'), ('Liquid Δs', 'c ln(T₂/T₁).'), ('Ideal gas Δs', 'c_p ln(T₂/T₁) − R ln(p₂/p₁).'), ('Isentropic T', 'T₂/T₁ = (p₂/p₁)^((k−1)/k).'), ('η_T', '(h₁ − h₂a)/(h₁ − h₂s).')],
 'planet': {'text': ['NASA Glenn’s Brayton-cycle page walks through a gas turbine on a T–s diagram: ideally the compressor raises pressure and temperature isentropically, a vertical line, but in reality the compression line leans to the right because entropy increases in the flow. Combustion happens at constant pressure, and the turbine, on the same shaft, drives the compressor.',
                     'NASA notes that the area enclosed on the T–s diagram is proportional to the useful work. Every bit of entropy generated in a compressor or turbine shrinks that area, so higher isentropic efficiencies mean more electricity or thrust from the same fuel, and less CO₂.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Calculus III', 'Calculus_III.html')],
            'src': [_BRAY]},
 'res': [('OpenStax UP2, 4.6 Entropy', _O + '4-6-entropy', 'Free textbook section.'), ('OpenStax UP2, 4.7 Entropy on a microscopic scale', _O + '4-7-entropy-on-a-microscopic-scale', 'Free textbook section.'),
         ('NASA Glenn: Entropy', _G + 'entropy.html', 'Free NASA page.'), ('OpenStax UP2, 3.6 Adiabatic processes for an ideal gas', _O + '3-6-adiabatic-processes-for-an-ideal-gas', 'Free textbook section.')]})
UNITS.append(
{'id': 'u8', 'title': 'Exergy: How Much Energy Is Useful', 'weeks': 'Week 11',
 'summary': 'Dead state and surroundings, exergy (availability) of heat and of flowing streams, reversible work and irreversibility, exergy destruction I = T₀S_gen, second-law efficiency, and why matching energy quality to use matters.',
 'objectives': ['Compute the exergy of heat from a reservoir.', 'Relate exergy destroyed to entropy generated.', 'Compute second-law efficiency.', 'Explain why combined heat and power and heat pumps use exergy well.'],
 'concepts': ['Exergy is the maximum useful work obtainable as a system comes to equilibrium with its surroundings (the dead state, T₀ and p₀). Energy is conserved; exergy is destroyed by irreversibility.',
              'Heat Q from a reservoir at T has exergy X = Q(1 − T₀/T): heat at high temperature is valuable, heat near room temperature is almost worthless for work.',
              'Exergy of a flowing stream per unit mass: ψ = (h − h₀) − T₀(s − s₀) + V²/2 + gz.',
              'Exergy destroyed (irreversibility) I = T₀S_gen (Gouy–Stodola). Every irreversibility costs useful work.',
              'Second-law efficiency η_II = η_th/η_rev for engines, or COP/COP_rev for heat pumps. Burning fuel at 2000 K just to heat water to 60 °C wastes most of the exergy; using the waste heat of a power plant for that job does not.'],
 'eqs': [('X_Q=Q\\left(1-\\frac{T_0}{T}\\right)', 'Exergy of heat'), ('\\psi=(h-h_0)-T_0(s-s_0)+\\frac{V^2}{2}+gz', 'Flow exergy'), ('I=T_0S_{gen}', 'Exergy destroyed'), ('\\eta_{II}=\\frac{\\eta_{th}}{\\eta_{rev}}', 'Second-law efficiency')],
 'worked': [
  {'q': 'Find the exergy of 100 kJ of heat from a 600 K source with T₀ = 300 K.', 'steps': ['X = 100 × (1 − 300/600).'], 'a': '50 kJ.'},
  {'q': '1000 kJ flows from 800 K to 300 K (T₀ = 300 K). Find the exergy destroyed.', 'steps': ['S_gen = 1000/300 − 1000/800 = 2.083 kJ/K.', 'I = 300 × 2.083.'], 'a': 'I = 625 kJ, all the exergy the heat had at 800 K.'},
  {'q': 'An engine with η = 35% runs between 800 K and 300 K. Find η_II.', 'steps': ['η_rev = 62.5%.', 'η_II = 0.35/0.625.'], 'a': 'η_II = 56%.'}],
 'practice': [('Exergy of 100 kJ at 330 K with T₀ = 300 K?', '100 × (1 − 300/330) = 9.09 kJ.'), ('A heat pump has COP 3; COP_rev = 14. η_II?', '3/14 = 21.4%.'),
              ('Why is room-temperature heat nearly worthless for work?', 'Its exergy factor 1 − T₀/T is near zero.'), ('What destroys exergy?', 'Every irreversibility: friction, mixing, heat transfer across finite ΔT.')],
 'misc': [('Energy and exergy are the same.', 'Energy is conserved; exergy is destroyed.'), ('High first-law efficiency means a good process.', 'A 95% efficient gas boiler can have a low second-law efficiency.'),
          ('Exergy depends only on the system.', 'It depends on the surroundings (T₀, p₀) too.')],
 'quiz': [{'q': 'Exergy destroyed equals…', 'opts': ['T₀S_gen', 'Q', 'W', 'ΔU'], 'ok': 0, 'why': 'Gouy–Stodola.'},
          {'q': 'Exergy of heat at T = T₀ is…', 'opts': ['Q', 'zero', 'infinite', 'Q/2'], 'ok': 1, 'why': '1 − T₀/T = 0.'},
          {'q': 'η_II compares actual performance with…', 'opts': ['the reversible limit', 'zero', '100%', 'the first law'], 'ok': 0, 'why': 'Second-law efficiency.'},
          {'q': 'The dead state is…', 'opts': ['equilibrium with surroundings', 'absolute zero', 'the critical point', 'vacuum'], 'ok': 0, 'why': 'T₀, p₀.'}],
 'cards': [('Exergy', 'Maximum useful work.'), ('Heat exergy', 'Q(1 − T₀/T).'), ('Dead state', 'T₀, p₀.'), ('Irreversibility', 'I = T₀S_gen.'), ('η_II', 'η/η_rev.'), ('Energy quality', 'High T is valuable.')],
 'planet': {'text': ['DOE explains that combined heat and power (cogeneration) produces electricity and useful heating or cooling from a single fuel at or near where it is used, recovering heat that would otherwise be lost in power generation. DOE says CHP can reasonably operate at 65% to 75% efficiency, versus a national average of about 50% when electricity and heat are produced separately.',
                     'Exergy explains the win: the high-temperature part of the fuel’s exergy makes electricity, and the low-grade heat that a power plant would throw away meets heating needs that only ever required low-exergy energy. Going from 50% to 75% means the same services from two-thirds of the fuel.'],
            'site': [('Solutions', 'Solutions.html'), ('Space Weather', 'Space_Weather.html')],
            'src': [_CHP]},
 'res': [(_MIT[0], _MIT[1], 'Availability lectures.'), ('OpenStax UP2, 4.1 Reversible and irreversible processes', _O + '4-1-reversible-and-irreversible-processes', 'Free textbook section.'),
         ('OpenStax UP2, 4.4 Statements of the second law', _O + '4-4-statements-of-the-second-law-of-thermodynamics', 'Free textbook section.'), (_MITU[0], _MITU[1], 'Second-law notes.')]})
UNITS.append(
{'id': 'u9', 'title': 'Gas Power Cycles: Otto, Diesel and Brayton', 'weeks': 'Weeks 12–13',
 'summary': 'Air-standard assumptions, mean effective pressure, the Otto cycle (spark ignition), the Diesel cycle (compression ignition), the Brayton cycle for gas turbines and jet engines, back-work ratio, regeneration, intercooling and reheat, and combined cycles.',
 'objectives': ['Analyze ideal Otto and Diesel cycles.', 'Analyze the ideal Brayton cycle, including back-work ratio.', 'Explain how compression ratio and pressure ratio raise efficiency.', 'Describe regeneration and combined cycles.'],
 'concepts': ['Air-standard assumptions: the working fluid is air, an ideal gas, in a closed cycle; combustion is replaced by heat addition and exhaust by heat rejection. Cold-air-standard adds constant specific heats at room temperature.',
              'Otto cycle: isentropic compression, constant-volume heat addition, isentropic expansion, constant-volume heat rejection. η_Otto = 1 − 1/r^(k−1), with compression ratio r = V_max/V_min.',
              'Diesel cycle: heat is added at constant pressure; with cutoff ratio r_c, η_Diesel = 1 − (1/r^(k−1))·(r_c^k − 1)/(k(r_c − 1)). Diesels run at higher r, so they are more efficient in practice.',
              'Brayton cycle (gas turbines): isentropic compression, constant-pressure heat addition, isentropic expansion, constant-pressure heat rejection. η_Brayton = 1 − 1/r_p^((k−1)/k). A large share of turbine work drives the compressor (the back-work ratio).',
              'Regeneration uses hot exhaust to preheat compressed air; intercooling and reheat move the cycle toward Carnot. A combined cycle feeds gas-turbine exhaust to a steam (Rankine) cycle.'],
 'eqs': [('\\eta_{Otto}=1-\\frac{1}{r^{k-1}}', 'Otto cycle'), ('\\eta_{Diesel}=1-\\frac{1}{r^{k-1}}\\frac{r_c^k-1}{k(r_c-1)}', 'Diesel cycle'), ('\\eta_{Brayton}=1-\\frac{1}{r_p^{(k-1)/k}}', 'Brayton cycle'), ('r_{bw}=\\frac{w_{comp}}{w_{turb}}', 'Back-work ratio')],
 'worked': [
  {'q': 'Find the cold-air-standard efficiency of Otto cycles with r = 8 and r = 10.', 'steps': ['1 − 8^(−0.4).', '1 − 10^(−0.4).'], 'a': '56.5% and 60.2%.'},
  {'q': 'A Diesel cycle has r = 18 and r_c = 2. Find η.', 'steps': ['1/r^0.4 = 0.3147.', '(2^1.4 − 1)/(1.4 × 1) = 1.1703.', 'η = 1 − 0.3147 × 1.1703.'], 'a': 'η = 63.2%.'},
  {'q': 'An ideal Brayton cycle has r_p = 8, inlet 300 K and turbine inlet 1300 K. Find T₂, T₄, compressor and turbine work, back-work ratio, net work and η.', 'steps': ['T₂ = 300 × 8^0.2857 = 543.4 K; T₄ = 1300/1.8114 = 717.7 K.', 'w_c = 1.005 × 243.4 = 244.7 kJ/kg; w_t = 1.005 × 582.3 = 585.3 kJ/kg.', 'r_bw = 244.7/585.3; w_net = 340.6 kJ/kg; η = 1 − 8^(−0.2857).'], 'a': 'r_bw = 0.418, w_net = 340.6 kJ/kg, η = 44.8%.'}],
 'practice': [('Brayton efficiency at r_p = 12?', '1 − 12^(−0.2857) = 50.8%.'), ('Why are Diesel engines more efficient than gasoline ones in practice?', 'They run at much higher compression ratios.'),
              ('Raising r in an Otto cycle from 8 to 10 adds how many points?', '60.2 − 56.5 = 3.7 points.'), ('What does regeneration do?', 'Uses exhaust heat to preheat compressor air, cutting fuel needed.')],
 'misc': [('Higher compression always means more efficient real engines.', 'Knock limits spark-ignition engines.'), ('Back work is negligible in gas turbines.', 'Often 40–80% of turbine work.'),
          ('Air-standard efficiency is the real efficiency.', 'Real engines are much lower due to friction, heat loss and real gases.')],
 'quiz': [{'q': 'Otto efficiency depends on…', 'opts': ['compression ratio', 'fuel type only', 'speed', 'cutoff ratio'], 'ok': 0, 'why': '1 − 1/r^(k−1).'},
          {'q': 'Brayton heat addition is at constant…', 'opts': ['volume', 'pressure', 'temperature', 'entropy'], 'ok': 1, 'why': 'Combustor.'},
          {'q': 'Back-work ratio is…', 'opts': ['w_c/w_t', 'w_t/w_c', 'η', 'r_p'], 'ok': 0, 'why': 'Compressor over turbine.'},
          {'q': 'A combined cycle pairs Brayton with…', 'opts': ['Otto', 'Rankine', 'Diesel', 'Carnot'], 'ok': 1, 'why': 'Steam bottoming cycle.'}],
 'cards': [('Air standard', 'Air, ideal gas, closed cycle.'), ('Otto', '1 − 1/r^(k−1).'), ('Diesel', 'Constant-p heat addition.'), ('Brayton', '1 − 1/r_p^((k−1)/k).'), ('Back work', 'w_c/w_t.'), ('Regeneration', 'Exhaust preheats air.')],
 'planet': {'text': ['NASA Glenn explains that the Brayton cycle is used in all gas turbine engines, whether turbojets, turbofans or turboprops, and that all share a compressor, a combustion section and a turbine that drives the compressor. NASA’s EngineSim program uses Brayton-cycle analysis to predict an engine’s thrust and fuel flow.',
                     'Ground-based gas turbines run the same cycle. EIA’s heat-rate examples show why cycle design matters: 7,500 Btu/kWh is about 45% efficient versus about 33% at 10,500 Btu/kWh. Raising pressure ratio and turbine temperature, and recovering exhaust heat, are how plants move toward the better number.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html')],
            'src': [_BRAY, _EIA]},
 'res': [('NASA Glenn: Brayton cycle', _G + 'brayton.html', 'Free NASA page.'), ('NASA Glenn: Otto cycle', _G + 'otto.html', 'Free NASA page.'), (_MIT[0], _MIT[1], 'Cycle lectures.'), (_MITU[0], _MITU[1], 'Propulsion cycle notes.')]})
UNITS.append(
{'id': 'u10', 'title': 'Vapor Power and Refrigeration Cycles', 'weeks': 'Weeks 14–15',
 'summary': 'The ideal Rankine cycle and its four devices, pump work, raising efficiency (higher boiler pressure and temperature, lower condenser pressure, reheat, regeneration), the vapor-compression refrigeration cycle and heat pumps, refrigerants, and cogeneration.',
 'objectives': ['Analyze an ideal Rankine cycle with steam tables.', 'Explain how pressure, superheat and reheat change efficiency.', 'Analyze an ideal vapor-compression refrigeration cycle.', 'Relate cycle COP to heat pump performance.'],
 'concepts': ['Ideal Rankine cycle: pump (isentropic compression of liquid), boiler (constant-pressure heating to superheated steam), turbine (isentropic expansion), condenser (constant-pressure condensation).',
              'Pump work is small because liquid has small v: w_p ≈ v(p₂ − p₁). Net work = w_turb − w_pump; η = w_net/q_in.',
              'Efficiency rises with higher average heat-addition temperature (higher boiler pressure, more superheat, reheat) and lower condenser pressure. Regeneration with feedwater heaters preheats the water using steam bled from the turbine.',
              'Vapor-compression refrigeration: compressor (to superheated vapor), condenser (rejects Q_H), expansion valve (throttle, h₃ = h₄), evaporator (absorbs Q_L). COP_R = (h₁ − h₄)/(h₂ − h₁).',
              'A heat pump is the same cycle used for heating, with COP_HP = (h₂ − h₃)/(h₂ − h₁). Refrigerants are chosen for their saturation properties, safety and low global-warming potential.'],
 'eqs': [('w_p=v(p_2-p_1)', 'Pump work'), ('\\eta=\\frac{w_t-w_p}{q_{in}}', 'Rankine efficiency'), ('COP_R=\\frac{h_1-h_4}{h_2-h_1}', 'Refrigerator COP'), ('h_3=h_4', 'Expansion valve')],
 'worked': [
  {'q': 'An ideal Rankine cycle runs between 3 MPa/350 °C and 75 kPa. Steam tables: h₁ = 384.44, v₁ = 0.001037 m³/kg, h₃ = 3116.1, h₄ = 2403.0 kJ/kg. Find w_p, q_in, w_net and η.', 'steps': ['w_p = 0.001037 × (3000 − 75) = 3.03 kJ/kg; h₂ = 387.47.', 'q_in = 3116.1 − 387.47 = 2728.6 kJ/kg.', 'w_net = (3116.1 − 2403.0) − 3.03 = 710.1 kJ/kg; η = 710.1/2728.6.'], 'a': 'w_p = 3.03 kJ/kg, q_in = 2728.6 kJ/kg, w_net = 710.1 kJ/kg, η = 26.0%.'},
  {'q': 'A vapor-compression cycle has h₁ = 244.5, h₂ = 275.4 and h₃ = h₄ = 95.5 kJ/kg (sample values). Find q_L, w_in and COP_R.', 'steps': ['q_L = 244.5 − 95.5 = 149.0 kJ/kg.', 'w = 275.4 − 244.5 = 30.9 kJ/kg.', 'COP = 149.0/30.9.'], 'a': 'q_L = 149.0 kJ/kg, w = 30.9 kJ/kg, COP_R = 4.82.'},
  {'q': 'For that cycle used as a heat pump, find COP_HP.', 'steps': ['q_H = 275.4 − 95.5 = 179.9 kJ/kg.', 'COP_HP = 179.9/30.9.'], 'a': 'COP_HP = 5.82 (= COP_R + 1).'}],
 'practice': [('In the Rankine example, what is the heat rejected?', '2403.0 − 384.44 = 2018.6 kJ/kg.'), ('What fraction of turbine work does the pump use?', '3.03/713.1 = 0.425%.'),
              ('Find the steam flow for 100 MW net in the example.', '100,000/710.1 = 140.8 kg/s.'), ('Why does lowering condenser pressure help?', 'It lowers the heat-rejection temperature.')],
 'misc': [('Pump work in a Rankine cycle is large.', 'It is tiny because liquid is nearly incompressible.'), ('The expansion valve does work.', 'It is a throttle: h constant, no work.'),
          ('More superheat always helps with no limit.', 'Turbine materials limit temperature.')],
 'quiz': [{'q': 'In a Rankine cycle, heat is added in the…', 'opts': ['pump', 'boiler', 'turbine', 'condenser'], 'ok': 1, 'why': 'Constant pressure.'},
          {'q': 'Pump work is about…', 'opts': ['v Δp', 'c_pΔT', 'h_fg', 'zero exactly'], 'ok': 0, 'why': 'Incompressible liquid.'},
          {'q': 'In refrigeration, Q_L is absorbed in the…', 'opts': ['condenser', 'evaporator', 'compressor', 'valve'], 'ok': 1, 'why': 'Cold side.'},
          {'q': 'COP_HP minus COP_R is…', 'opts': ['0', '1', 'η', '2'], 'ok': 1, 'why': 'q_H = q_L + w.'}],
 'cards': [('Rankine', 'Pump, boiler, turbine, condenser.'), ('Pump work', 'v(p₂ − p₁).'), ('Reheat', 'Raises mean heat-addition T, drier exhaust.'), ('Vapor compression', 'Compressor, condenser, valve, evaporator.'), ('COP_R', '(h₁ − h₄)/(h₂ − h₁).'), ('Throttle', 'h₃ = h₄.')],
 'planet': {'text': ['DOE’s geothermal office explains that geothermal plants bring hot fluid up through wells and convert its heat to steam that drives turbines, a Rankine-family cycle with Earth as the boiler. Geothermal plants can run essentially 24 hours a day regardless of weather, and DOE’s analysis sees potential for 90 gigawatts of U.S. geothermal electricity by 2050 if enhanced geothermal costs fall.',
                     'Nuclear plants use the same Rankine cycle, and DOE’s heat pump article describes the vapor-compression cycle in reverse: moving heat into homes in winter and out in summer. Better Rankine and refrigeration cycles are where much of the world’s clean electricity and efficient heating will come from.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_GEO, _NUC, _HP]},
 'res': [(_NIST[0], _NIST[1], 'Steam and refrigerant tables.'), ('OpenStax UP2, 4.3 Refrigerators and heat pumps', _O + '4-3-refrigerators-and-heat-pumps', 'Free textbook section.'), (_MIT[0], _MIT[1], 'Vapor cycle lectures.'), ('NASA Glenn: Second law of thermodynamics', _G + 'thermo2.html', 'Free NASA page.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: The ideal-gas law in PhET Gas Properties', 'week': 'Week 2',
 'goal': 'Show that pressure is proportional to absolute temperature at fixed volume and amount, and that pV/T stays constant.',
 'eq': ('\\frac{p_1}{T_1}=\\frac{p_2}{T_2}\\ \\ (V,\\ m\\ \\text{fixed})', 'Ideal-gas law at constant volume'),
 'steps': ['Open PhET Gas Properties, Ideal tab; pump in gas and hold volume constant.', 'Heat the gas in steps and record T and p.', 'Plot p against T in kelvin; extend the line to p = 0.', 'Repeat at constant pressure and record volume.'],
 'table': (['T (K)', 'p (kPa), starting 100 kPa at 300 K'], [['300', '100'], ['400', '133.3'], ['600', '200']]),
 'note': 'Ideal-gas values; the simulator’s numbers fluctuate a little because it counts particle collisions.',
 'calc': ['p₂ = 100 × 400/300 = 133.3 kPa.', 'The line through the data passes through p = 0 at T = 0 K.'],
 'safety': ['Computer only.'], 'home': ['Gas Properties runs in a browser.'],
 'sims': [('PhET: Gas Properties', _PH + 'gas-properties'), ('PhET: States of Matter', _PH + 'states-of-matter')],
 'planet': 'DOE says reactor designers pressurize water so it does not boil; the same state relationships set every boiler and tank design.', 'planet_src': [_NUC]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Kettle energy balance and efficiency', 'week': 'Week 5',
 'goal': 'Apply the first law to heating water and find how much of a kettle’s electrical energy reaches the water.',
 'eq': ('\\eta=\\frac{mc\\Delta T}{P\\,t}', 'Kettle efficiency'),
 'steps': ['Weigh 1.00 kg (1 L) of tap water and measure its temperature.', 'Read the kettle’s power rating from its label.', 'Time how long it takes to reach boiling (the kettle switches off).', 'Compute the heat absorbed and the electrical energy used.'],
 'table': (['Quantity', 'Value'], [['Water heat, 1 kg 20→100 °C (kJ)', '334.4'], ['Electrical energy, 1500 W × 250 s (kJ)', '375.0'], ['Efficiency', '89.2%']]),
 'note': 'Sample values; your kettle’s time depends on its power, the water’s starting temperature and your altitude.',
 'calc': ['Q = 1 × 4.18 × 80 = 334.4 kJ.', 'η = 334.4/375 = 89.2%.'],
 'safety': ['Steam and boiling water scald: keep the lid closed, pour away from yourself, and keep children and pets away.', 'Do not touch the kettle body while hot.'], 'home': ['This is a home lab.'],
 'sims': [('PhET: Energy Forms and Changes', _PH + 'energy-forms-and-changes')],
 'planet': 'DOE notes resistance heating turns 1 kWh into 1 kWh of heat, while heat pumps cut electricity use by about 50%.', 'planet_src': [_HP]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Melting ice and latent heat', 'week': 'Week 5',
 'goal': 'Use a heat balance to predict the final temperature when ice melts in warm water, and compare with measurement.',
 'eq': ('m_wc(T_w-T_f)=m_i h_{if}+m_ic\\,T_f', 'Heat lost by water = heat gained by ice'),
 'steps': ['Put 300 g of 40 °C water in an insulated cup.', 'Add 50 g of ice at 0 °C (pat it dry).', 'Stir gently until all the ice has melted and record the lowest temperature.', 'Compare with the predicted final temperature.'],
 'table': (['Quantity', 'Value'], [['Water', '0.300 kg at 40 °C'], ['Ice', '0.050 kg at 0 °C'], ['Predicted final T', '22.9 °C']]),
 'note': 'Sample values; heat gained from the cup and air makes the measured value a little higher.',
 'calc': ['0.3 × 4.18 × (40 − T) = 0.05 × 334 + 0.05 × 4.18 × T.', 'T = 33.46/1.463 = 22.9 °C.'],
 'safety': ['Use warm tap water, not boiling.'], 'home': ['This is a home lab.'],
 'sims': [('PhET: States of Matter', _PH + 'states-of-matter'), ('PhET: Energy Forms and Changes', _PH + 'energy-forms-and-changes')],
 'planet': 'Latent heat is how thermal storage works; DOE notes geothermal energy can also support thermal energy storage.', 'planet_src': [_GEO]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Insulation and cooling rate', 'week': 'Week 4',
 'goal': 'Compare how fast hot water cools in a plain and an insulated mug, and find each cooling constant.',
 'eq': ('\\frac{T-T_\\infty}{T_0-T_\\infty}=e^{-kt}', 'Newton’s law of cooling'),
 'steps': ['Fill two mugs, one plain and one insulated (or wrapped in a towel), with water at about 80 °C.', 'Record temperature every 2 minutes for 20 minutes; note room temperature.', 'Compute k = ln[(T₀ − T∞)/(T − T∞)]/t for each.', 'Compare the heat-loss rates.'],
 'table': (['Mug', 'T after 20 min (°C)', 'k (1/min)'], [['Plain', '60', '0.0203'], ['Insulated', '70', '0.00912']]),
 'note': 'Sample values with room at 20 °C.',
 'calc': ['Plain: k = ln(60/40)/20 = 0.0203 per minute.', 'Insulated: k = ln(60/50)/20 = 0.00912 per minute, less than half.'],
 'safety': ['Hot water scalds: use oven mitts and keep mugs on a stable surface away from edges.'], 'home': ['This is a home lab.'],
 'sims': [('PhET: Energy Forms and Changes', _PH + 'energy-forms-and-changes')],
 'planet': 'DOE advises weatherizing before installing a heat pump, because insulation cuts the heat a home must replace.', 'planet_src': [_HP]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Carnot limits for a heat pump', 'week': 'Week 8',
 'goal': 'Build a spreadsheet of the Carnot COP of a heat pump against outdoor temperature and compare with a real unit’s rated COP.',
 'eq': ('COP_{HP,Carnot}=\\frac{T_H}{T_H-T_L}', 'Carnot heat pump'),
 'steps': ['Set indoor T_H = 294 K.', 'List outdoor temperatures from 253 K to 288 K.', 'Compute the Carnot COP for each.', 'Look up the rated efficiency of any heat pump on its label or ENERGY STAR listing and compare.'],
 'table': (['T_L (K)', 'COP_Carnot'], [['263', '9.48'], ['273', '14.0'], ['283', '26.7']]),
 'note': 'Ideal limits; real heat pumps reach a fraction of these.',
 'calc': ['COP = 294/(294 − 263) = 9.48.', 'Colder outdoor air means a lower limit.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('OpenStax UP2, 4.3 Refrigerators and heat pumps', _O + '4-3-refrigerators-and-heat-pumps')],
 'planet': 'DOE says geothermal heat pumps, using steady ground temperatures, can cut energy use by 30% to 60%.', 'planet_src': [_HP]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Rankine cycle spreadsheet', 'week': 'Week 15',
 'goal': 'Compute an ideal Rankine cycle from steam-table values and see how the turbine, pump and boiler terms set efficiency.',
 'eq': ('\\eta=\\frac{(h_3-h_4)-v_1(p_2-p_1)}{h_3-h_2}', 'Ideal Rankine efficiency'),
 'steps': ['Look up the four states in NIST’s WebBook (or use the values given).', 'Compute pump work, heat in, turbine work, net work and η.', 'Change the condenser pressure or boiler temperature using new table values and recompute.', 'Find the steam flow for a 100 MW plant.'],
 'table': (['Quantity', 'Value'], [['w_pump (kJ/kg)', '3.03'], ['q_in (kJ/kg)', '2728.6'], ['w_net (kJ/kg)', '710.1'], ['η', '26.0%']]),
 'note': 'Steam-table values for 3 MPa/350 °C and 75 kPa.',
 'calc': ['η = 710.1/2728.6 = 26.0%.', 'Steam flow for 100 MW = 100,000/710.1 = 140.8 kg/s.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_NIST[0], _NIST[1])],
 'planet': 'DOE says nuclear and geothermal plants both turn heat into steam that spins turbines, the cycle in this lab.', 'planet_src': [_NUC, _GEO]})
SCHEDULE = [(1, 'u1', 'Systems, properties, temperature, energy units, heat rate', 'OpenStax UP2 1.1, 3.1; EIA'), (2, 'u2', 'Phases, saturation, quality; Lab A', 'UP2 1.5, 2.1; NIST WebBook'),
            (3, 'u2', 'Steam tables, interpolation, ideal gas', 'NIST WebBook'), (4, 'u3', 'Boundary, shaft and electrical work; heat transfer modes; Lab D', 'UP2 3.2, 1.6'),
            (5, 'u4', 'First law for closed systems, specific heats, latent heat; Labs B and C', 'UP2 3.3, 3.5'), (6, 'u5', 'Mass and energy for control volumes; nozzles, turbines, compressors', 'MIT 16.050'),
            (7, 'u5', 'Throttles, mixing, heat exchangers; midterm practice', 'MIT 16.050'), (8, 'u6', 'Second law, engines, heat pumps, Carnot; Lab E', 'UP2 4.2–4.5'),
            (9, 'u7', 'Entropy, Clausius inequality, entropy generation', 'UP2 4.6–4.7'), (10, 'u7', 'Isentropic processes and efficiencies', 'UP2 3.6; NASA Glenn'),
            (11, 'u8', 'Exergy, irreversibility, second-law efficiency', 'MIT 16.050'), (12, 'u9', 'Otto and Diesel cycles', 'NASA Glenn'),
            (13, 'u9', 'Brayton cycle, regeneration, combined cycles', 'NASA Glenn; MIT Unified'), (14, 'u10', 'Rankine cycle and improvements', 'NIST WebBook'),
            (15, 'u10', 'Refrigeration and heat pumps; Lab F; final practice', 'UP2 4.3')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('A plant has a heat rate of 8530 Btu/kWh. Find its efficiency.', ['3412/8530.'], '40.0%.'),
  ('Find the mass of air in a 2 m³ tank at 200 kPa and 350 K.', ['m = 200 × 2/(0.287 × 350).'], '3.98 kg.'),
  ('Find h at 100 kPa and quality 0.9 (h_f = 417.51, h_fg = 2257.5 kJ/kg).', ['417.51 + 0.9 × 2257.5.'], '2449.3 kJ/kg.'),
  ('3 kg of water is heated from 15 °C to 65 °C. Find Q.', ['3 × 4.18 × 50.'], '627 kJ.'),
  ('Steam at 10 kg/s drops 800 kJ/kg in an adiabatic turbine. Find the power.', ['10 × 800.'], '8000 kW.')]),
 ('Final practice set (all units)', [
  ('Find the Carnot efficiency between 900 K and 300 K.', ['1 − 300/900.'], '66.7%.'),
  ('A heat pump delivers 12 kW with COP 4. Find the electrical power and the heat taken from outside.', ['W = 12/4; Q_L = 12 − 3.'], '3 kW and 9 kW.'),
  ('Find Δs of 1 kg of air from 300 K, 100 kPa to 600 K, 100 kPa.', ['1.005 ln 2.'], '0.697 kJ/(kg·K).'),
  ('Find the exergy of 500 kJ of heat at 1000 K with T₀ = 300 K.', ['500 × 0.7.'], '350 kJ.'),
  ('Find the Otto efficiency at r = 9.', ['1 − 9^(−0.4).'], '58.5%.'),
  ('A refrigeration cycle has q_L = 150 kJ/kg and w = 37.5 kJ/kg. Find COP_R and COP_HP.', ['150/37.5.'], '4.0 and 5.0.')])]
FORMULAS = ['\\eta=3412/\\text{heat rate},\\ v=V/m', 'pv=RT,\\ y=y_f+x\\,y_{fg}', 'W_b=\\int p\\,dV,\\ W=mRT\\ln(V_2/V_1)', 'Q-W=\\Delta U,\\ h=u+pv', '\\Delta u=c_v\\Delta T,\\ \\Delta h=c_p\\Delta T,\\ Q=mc\\Delta T',
            '\\dot Q-\\dot W=\\dot m(\\Delta h+\\Delta V^2/2+g\\Delta z)', '\\eta=W/Q_H,\\ COP_R=Q_L/W,\\ COP_{HP}=Q_H/W', '\\eta_{Carnot}=1-T_L/T_H', '\\Delta s=c_p\\ln(T_2/T_1)-R\\ln(p_2/p_1)',
            'T_2/T_1=(p_2/p_1)^{(k-1)/k}', 'X_Q=Q(1-T_0/T),\\ I=T_0S_{gen}', '\\eta_{Otto}=1-r^{1-k},\\ \\eta_{Brayton}=1-r_p^{(1-k)/k}', 'w_p=v\\Delta p,\\ COP_R=(h_1-h_4)/(h_2-h_1)']
GLOSSARY = sorted([('Adiabatic', 'No heat transfer.'), ('Back-work ratio', 'Compressor work over turbine work.'), ('Carnot cycle', 'Reversible cycle between two reservoirs; the best possible.'),
    ('COP', 'Coefficient of performance of a refrigerator or heat pump.'), ('Control volume', 'Region in space that mass can cross.'), ('Dead state', 'Equilibrium with the surroundings.'),
    ('Enthalpy', 'h = u + pv.'), ('Entropy', 'Property with dS = δQ_rev/T; measures irreversibility.'), ('Exergy', 'Maximum useful work obtainable.'), ('Heat engine', 'Device that converts heat to work in a cycle.'),
    ('Heat pump', 'Device that moves heat from cold to hot using work.'), ('Heat rate', 'Fuel Btu per kWh generated.'), ('Isentropic', 'Constant entropy; reversible and adiabatic.'),
    ('Latent heat', 'Energy for phase change at constant temperature.'), ('Quality', 'Vapor mass fraction of a saturated mixture.'), ('Rankine cycle', 'Steam power cycle: pump, boiler, turbine, condenser.'),
    ('Reversible process', 'Idealized process with no entropy generation.'), ('Saturation', 'State where liquid and vapor coexist.'), ('Specific heat', 'Energy to raise 1 kg by 1 K.'), ('Throttling', 'Pressure drop at constant enthalpy.')])
RUBRIC = [('4 · Mastery', 'Draws systems and diagrams, looks up states correctly, writes complete mass, energy and entropy balances, checks against Carnot limits, and runs labs safely.'), ('3 · Proficient', 'Solves the practice problems with occasional table or unit slips.'),
          ('2 · Developing', 'Follows worked examples but mixes up open and closed systems, or uses °C in ratios.'), ('1 · Beginning', 'Plugs numbers into formulas without a system sketch; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    R = .287; cp = 1.005; cv = .718; k = 1.4; cw = 4.18
    t8 = 8 ** ((k - 1) / k)
    T2 = 300 * t8; T4 = 1300 / t8; wc = cp * (T2 - 300); wt = cp * (1300 - T4)
    dsl = lambda r, rc: 1 - (1 / r ** (k - 1)) * (rc ** k - 1) / (k * (rc - 1))
    wnet = (3116.1 - 2403.0) - .001037 * (3000 - 75)
    qin = 3116.1 - (384.44 + .001037 * (3000 - 75))
    Tf = (.3 * cw * 40 - .05 * 334) / (.3 * cw + .05 * cw)
    sg = 1000 / 300 - 1000 / 800
    r = [
     ('u1 e1', 3412 / 10500, .325), ('u1 e2', 3412 / 7500, .455), ('u1 v', .5 / 2, .25), ('u1 rho', 2 / .5, 4), ('u1 KE', .5 * 1000 * 900 / 1000, 450), ('u1 kWh', 450 / 3600, .125),
     ('u1 K', 25 + 273.15, 298.15), ('u1 e9', 3412 / 9000, .379), ('u1 GJ', 3600 / 1000, 3.6), ('u1 q', 3412 / 6824, .5), ('u1 fuel', 7500 / 10500, .714), ('u1 less', 1 - 7500 / 10500, .286),
     ('u2 h', 417.51 + .6 * 2257.5, 1772.0), ('u2 v', .001043 + .6 * (1.6941 - .001043), 1.0169), ('u2 m', 100 * .5 / (R * 300), .581), ('u2 p', 2 * R * 400 / .5, 459.2), ('u2 int', 83.9 + .5 * (125.7 - 83.9), 104.8),
     ('u2 He', 8.314 / 4.003, 2.077),
     ('u3 iso', R * 300 * log(2), 59.7), ('u3 p2', 100 * 2 ** 1.3, 246.2), ('u3 poly', (100 * 2 ** 1.3 * .1 - 100 * .2) / (1 - 1.3), -15.4), ('u3 cond', .04 * 10 * 20 / .1, 80), ('u3 cp', 200 * .3, 60),
     ('u3 shaft', 2 * 3.14159265 * 50 * 50 / 1000, 15.7), ('u3 elec', 1500 * 600 / 1000, 900), ('u3 conv', 10 * 2 * 30, 600),
     ('u4 Qv', 2 * cv * 100, 143.6), ('u4 Qp', 2 * cp * 100, 201.0), ('u4 W', 2 * R * 100, 57.4), ('u4 dU', 2 * cp * 100 - 2 * R * 100, 143.6), ('u4 Q1', 1 * cw * 80, 334.4), ('u4 Q2', .1 * 2257, 225.7),
     ('u4 ice', .2 * 334, 66.8), ('u4 R', cp - cv, .287), ('u4 net', 500 - 300, 200), ('u4 k', cp / cv, 1.40),
     ('u5 dh', cp * 50, 50.25), ('u5 V', sqrt(2 * cp * 1000 * 50), 317.0), ('u5 turb', 5 * (3116.1 - 2403.0), 3565.5), ('u5 comp', 1.2 * cp * 150, 180.9), ('u5 hx', .5 * cw * 30, 62.7), ('u5 ke', 100 ** 2 / 2 / 1000, 5),
     ('u6 eta', 350 / 1000, .35), ('u6 QL', 1000 - 350, 650), ('u6 c1', 1 - 300 / 800, .625), ('u6 c2', 1 - 293 / 1073, .727), ('u6 cop', 294 / 21, 14.0), ('u6 QH', 3 * 3, 9), ('u6 W', 500 / 2.5, 200),
     ('u6 hp', 2.5 + 1, 3.5), ('u6 copr', 275 / 23, 11.96), ('u6 lim', 1 - 300 / 600, .5),
     ('u7 ds', 2 * cw * log(353 / 293), 1.557), ('u7 dsg', cp * log(5 / 3) - R * log(4), .1155), ('u7 T2s', T2, 543.4), ('u7 T2a', 300 + (T2 - 300) / .85, 586.4), ('u7 sg', sg, 2.083), ('u7 T10', 300 * 10 ** (.4 / 1.4), 579.2),
     ('u8 X', 100 * (1 - 300 / 600), 50), ('u8 I', 300 * sg, 625), ('u8 II', .35 / .625, .56), ('u8 X330', 100 * (1 - 300 / 330), 9.09), ('u8 hp', 3 / 14, .214), ('u8 chp', .5 / .75, .667),
     ('u9 o8', 1 - 8 ** -.4, .565), ('u9 o10', 1 - 10 ** -.4, .602), ('u9 r18', 1 / 18 ** .4, .3147), ('u9 rc', (2 ** 1.4 - 1) / 1.4, 1.1703), ('u9 dsl', dsl(18, 2), .632), ('u9 T2', T2, 543.4), ('u9 t8', t8, 1.8114),
     ('u9 T4', T4, 717.7), ('u9 wc', wc, 244.7), ('u9 wt', wt, 585.3), ('u9 bw', wc / wt, .418), ('u9 wn', wt - wc, 340.6), ('u9 b8', 1 - 1 / t8, .448), ('u9 b12', 1 - 12 ** (-.4 / 1.4), .508), ('u9 d', 60.2 - 56.5, 3.7),
     ('u9 dT', T2 - 300, 243.4), ('u9 dT2', 1300 - T4, 582.3),
     ('u10 wp', .001037 * (3000 - 75), 3.03), ('u10 h2', 384.44 + 3.03, 387.47), ('u10 qin', qin, 2728.6), ('u10 wn', wnet, 710.1), ('u10 eta', wnet / qin, .260), ('u10 qL', 244.5 - 95.5, 149.0), ('u10 w', 275.4 - 244.5, 30.9),
     ('u10 cop', 149 / 30.9, 4.82), ('u10 qH', 275.4 - 95.5, 179.9), ('u10 hp', 179.9 / 30.9, 5.82), ('u10 qout', 2403.0 - 384.44, 2018.6), ('u10 frac', 3.03 / 713.1, .00425), ('u10 m', 100000 / wnet, 140.8), ('u10 wt', 3116.1 - 2403.0, 713.1),
     ('A 400', 100 * 400 / 300, 133.3), ('A 600', 100 * 600 / 300, 200),
     ('B Q', 1 * cw * 80, 334.4), ('B E', 1500 * 250 / 1000, 375.0), ('B eta', 334.4 / 375, .892),
     ('C T', Tf, 22.9), ('C lhs', .3 * cw * 40 - .05 * 334, 33.46), ('C den', .3 * cw + .05 * cw, 1.463),
     ('D k1', log(60 / 40) / 20, .0203), ('D k2', log(60 / 50) / 20, .00912),
     ('E 263', 294 / 31, 9.48), ('E 273', 294 / 21, 14.0), ('E 283', 294 / 11, 26.7),
     ('F wp', .001037 * 2925, 3.03), ('F q', qin, 2728.6), ('F wn', wnet, 710.1), ('F eta', wnet / qin, .260), ('F m', 100000 / wnet, 140.8),
     ('M1', 3412 / 8530, .400), ('M2', 200 * 2 / (R * 350), 3.98), ('M3', 417.51 + .9 * 2257.5, 2449.3), ('M4', 3 * cw * 50, 627), ('M5', 10 * 800, 8000),
     ('F1', 1 - 300 / 900, .667), ('F2 W', 12 / 4, 3), ('F2 QL', 12 - 3, 9), ('F3', cp * log(2), .697), ('F4', 500 * (1 - 300 / 1000), 350), ('F5', 1 - 9 ** -.4, .585), ('F6 R', 150 / 37.5, 4.0), ('F6 HP', 150 / 37.5 + 1, 5.0)]
    return r

_CHECKS_MAIN = CHECKS

def CHECKS():
    """Main checks plus cross-checks of intermediate values printed in steps, tables, quizzes and labs."""
    R = .287; cp = 1.005; cv = .718; cw = 4.18
    extra = [
     ('x u1 kWhBtu', 3600 / 1.055, 3412), ('x u1 vel', .5 * 1000 * 30 ** 2, 450000), ('x u2 Tsat', 99.61, 99.61), ('x u2 dv', 1.6941 - .001043, 1.693), ('x u2 RT', R * 300, 86.1),
     ('x u3 ln2', log(2), .6931), ('x u3 2n', 2 ** 1.3, 2.462), ('x u3 rps', 3000 / 60, 50), ('x u3 sec', 10 * 60, 600), ('x u4 dT', 400 - 300, 100), ('x u4 cpv', 2 * cv, 1.436),
     ('x u5 J', cp * 50 * 1000, 50250), ('x u5 MW', 5 * (3116.1 - 2403.0) / 1000, 3.57), ('x u5 dT', 450 - 300, 150), ('x u6 lift', 294 - 273, 21), ('x u6 TL', 298 - 275, 23),
     ('x u7 ln', log(353 / 293), .1863), ('x u7 lnT', log(5 / 3), .5108), ('x u7 lnp', log(4), 1.386), ('x u7 s1', 1000 / 300, 3.333), ('x u7 s2', 1000 / 800, 1.25), ('x u7 exp', .4 / 1.4, .2857),
     ('x u8 f', 1 - 300 / 1000, .7), ('x u8 two3', .5 / .75, .667), ('x u9 b', 8 ** -.4, .4353), ('x u9 2k', 2 ** 1.4, 2.639), ('x u9 c12', 12 ** (.4 / 1.4), 2.034),
     ('x u10 dp', 3000 - 75, 2925), ('x u10 sum', 2018.6 + 710.1, 2728.7), ('x u10 HP', 179.9 / 30.9 - 149 / 30.9, 1.0), ('x A lin', 300 / 300, 1),
     ('x B J', 1500 * 250, 375000), ('x B dT', 100 - 20, 80), ('x C ml', .05 * 334, 16.7), ('x C w', .3 * cw * 40, 50.16), ('x C a', .3 * cw, 1.254), ('x C b', .05 * cw, .209),
     ('x D r1', 60 / 40, 1.5), ('x D r2', 60 / 50, 1.2), ('x D ratio', (log(60 / 50) / 20) / (log(60 / 40) / 20), .45), ('x E d1', 294 - 263, 31), ('x E d3', 294 - 283, 11),
     ('x M2 RT', R * 350, 100.45), ('x F2 sum', 3 + 9, 12), ('x F3 ln', log(2), .693), ('x F5 p', 9 ** -.4, .4152), ('x quiz q', 1 - 300 / 600, .5), ('x quiz hr', 3412 / 6824, .5)]
    return _CHECKS_MAIN() + extra
