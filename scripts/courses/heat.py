"""Heat Transfer (AERO 440): modes and energy balances, steady conduction and thermal resistance, cylinders and fins, transient conduction, forced convection, internal flow and heat exchangers, natural convection, radiation fundamentals, radiation exchange and shields, and heat transfer for buildings and climate.
Oct 25 2026, founder-approved four-year track, senior course 4. Same module fields as scdesign.py / fdc.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, log, exp, tanh, pi
ID = 'heat'
STATUS = 'live'
YEAR = 4
PAGE = 'Heat_Transfer.html'
CODE = 'AERO 440'
TITLE = 'Heat Transfer'
LAB_NAME = 'Heat transfer lab'
TAGLINE = 'Conduction, convection and radiation: thermal resistance and insulation, fins, transient cooling, forced and natural convection, heat exchangers, blackbody radiation, radiation shields, and heat pumps, with six labs. Free, self-paced, and tied to NASA’s view of Earth’s energy budget, Parker Solar Probe’s heat shield and efficient home heating.'
DESC = 'Free self-study Heat Transfer: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and spreadsheet labs, practice exams, tied to Earth’s energy budget, Parker Solar Probe and heat pumps.'
ALT = 'Earth’s full disk in NASA’s Blue Marble image, showing land, ocean, ice and clouds'
_PH = 'https://phet.colorado.edu/en/simulations/'
_AHTT = ('J. H. Lienhard IV and J. H. Lienhard V, A Heat Transfer Textbook (free online edition)', 'https://ahtt.mit.edu/')
_MIT = ('MIT OpenCourseWare 2.51 Intermediate Heat and Mass Transfer (Fall 2008)', 'https://ocw.mit.edu/courses/2-51-intermediate-heat-and-mass-transfer-fall-2008/')
_EB = ('NASA Earth Observatory: Climate and Earth’s Energy Budget', 'https://earthobservatory.nasa.gov/features/EnergyBalance')
_PSP = ('NASA Science: Parker Solar Probe', 'https://science.nasa.gov/mission/parker-solar-probe/')
_ES = ('ENERGY STAR: Air-Source Heat Pumps', 'https://www.energystar.gov/products/air_source_heat_pumps')
_CER = ('NASA Langley: CERES (Clouds and the Earth’s Radiant Energy System)', 'https://ceres.larc.nasa.gov/')
BANNER = ['images/earth-blue-marble-land-ocean-ice-cloud.jpg', 'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg', 'images/GOES19_GOESU_KSC.jpg', 'images/ISS_Over_Ganges_STS102.jpg']
CREDITS = {'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA', 'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg': 'NASA/Michael DeMocker (MAF20210116_GR0006)',
           'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC', 'images/ISS_Over_Ganges_STS102.jpg': 'NASA (STS102-357-031, March 18, 2001)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester senior heat transfer course for engineers. It is modeled on the topics and depth of the free online A Heat Transfer Textbook by Lienhard and Lienhard and MIT 2.51 Intermediate Heat and Mass Transfer (free on MIT OpenCourseWare), which we link where they help. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (NASA’s Earth energy budget, Parker Solar Probe and ENERGY STAR heat pumps), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a spreadsheet.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Earth’s climate is a heat transfer problem: sunlight in, thermal infrared out, with convection and evaporation moving heat in between. The same physics decides how much energy our buildings, engines and electronics waste.',
                 'Insulation, heat pumps and efficient heat exchangers are some of the cheapest climate solutions. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Thermodynamics: energy balances and the first and second laws.', 'Fluid Mechanics: boundary layers, Reynolds number and pipe flow.',
           'Differential Equations: first-order ODEs and separation of variables.', 'Calculus III: gradients and integrals over areas and volumes.']
STUDY = ['Draw the system and every heat flow arrow before writing an equation.', 'Use kelvin for radiation and temperature differences for conduction and convection.',
         'Turn every problem into a thermal-resistance network when you can.', 'Check dimensionless numbers (Bi, Re, Pr, Nu, Ra) to pick the right correlation.',
         'Compare answers with everyday experience: a warm house, a cooling cup, a hot pan.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Energy Forms and Changes, Blackbody Spectrum and Greenhouse Effect simulations.', 'Spreadsheet software (any free one works), or Python.',
            'The free online A Heat Transfer Textbook in a web browser.', 'A calculator.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free simulation or a spreadsheet, so there are no burn or electrical hazards. Do not heat, boil or ignite anything for this course. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST: CODATA value, Stefan–Boltzmann constant', 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma')
CONSTANTS = [('Stefan–Boltzmann constant', 'σ = 5.670374419 × 10⁻⁸ W/(m²·K⁴)'), ('Wien’s constant (textbook value)', '2898 µm·K'), ('Standard gravity', 'g = 9.80665 m/s²'),
             ('Air near 300 K (textbook values)', 'k = 0.026 W/(m·K), ν = 1.5 × 10⁻⁵ m²/s, Pr = 0.71'), ('Aluminum (textbook values)', 'k = 237 W/(m·K), ρ = 2700 kg/m³, c = 900 J/(kg·K)'), ('Earth’s surface area (textbook value)', '5.1 × 10¹⁴ m²')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free texts, lectures and simulations alongside the course.'
PTABLE = [(_AHTT[0], _AHTT[1], 'Free complete heat transfer textbook.'), (_MIT[0], _MIT[1], 'Free MIT lectures and problems.'), (_EB[0], _EB[1], 'Free NASA explainer.'),
          ('PhET: Energy Forms and Changes', _PH + 'energy-forms-and-changes', 'Heat flow interactively.'), ('PhET: Blackbody Spectrum', _PH + 'blackbody-spectrum', 'Thermal radiation.'), ('PhET: Greenhouse Effect', _PH + 'greenhouse-effect', 'Radiation balance.')]
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Modes of Heat Transfer and Energy Balances', 'weeks': 'Week 1',
 'summary': 'Conduction, convection and radiation, their rate equations, and surface and control-volume energy balances.',
 'objectives': ['Name the three modes and their rate laws.', 'Compute conduction, convection and radiation rates.', 'Write a surface energy balance.', 'Read Earth’s energy budget as a heat balance.'],
 'concepts': ['Heat transfer is energy in transit because of a temperature difference; thermodynamics says how much, heat transfer says how fast.',
              'Conduction moves energy through a solid or still fluid by molecular contact (Fourier’s law).',
              'Convection moves energy between a surface and a moving fluid (Newton’s law of cooling, with a heat transfer coefficient h).',
              'Radiation moves energy by electromagnetic waves, needs no medium, and grows with T⁴ in kelvin (Stefan–Boltzmann law).',
              'A surface stores no energy, so what arrives by one mode must leave by the others.'],
 'eqs': [('q=kA\\frac{\\Delta T}{L}', 'Fourier’s law, plane wall'), ('q=hA(T_s-T_\\infty)', 'Newton’s law of cooling'), ('q=\\varepsilon\\sigma A(T_s^4-T_{sur}^4)', 'Net radiation to large surroundings'), ('\\dot E_{in}-\\dot E_{out}+\\dot E_g=\\dot E_{st}', 'Energy balance')],
 'worked': [
  _w('A 0.2 m concrete wall (k = 1.4 W/(m·K), sample) of area 10 m² has a 15 K difference across it. Find q.', ['q = 1.4 × 10 × 15/0.2.'], '1050 W.'),
  _w('A plate with ε = 0.9 at 400 K sits in 300 K surroundings. Net radiation per m²?', ['0.9σ(400⁴ − 300⁴) = 0.9 × 5.670374419 × 10⁻⁸ × 1.75 × 10¹⁰.'], '893 W/m².'),
  _w('NASA says about 29% of incoming sunlight is reflected and the global average is about 340 W/m². How much is absorbed?', ['Reflected: 0.29 × 340 = 98.6 W/m².', 'Absorbed: 340 − 98.6.'], '241.4 W/m², matching NASA’s roughly 240 W/m².')],
 'practice': [('Repeat the wall example with k = 0.04 W/(m·K).', '30 W.'), ('Convection with h = 25 W/(m²·K), A = 2 m², ΔT = 40 K?', '2000 W.'),
              ('Why must radiation use kelvin?', 'T⁴ depends on absolute temperature.'), ('Why is 1360/4 the global average sunlight?', 'A sphere’s area is 4 times its shadow disk: 1360/4 = 340 W/m².')],
 'misc': [('Heat and temperature are the same.', 'Temperature is a state; heat is energy in transit.'), ('Radiation needs air.', 'It travels through vacuum.'), ('h is a material property.', 'It depends on flow and geometry.')],
 'quiz': [_q('Concrete wall q…', ['1050 W', '105 W', '4200 W', '210 W'], 0, '1.4 × 10 × 15/0.2.'), _q('Radiation scales with…', ['T⁴ (K)', 'T (°C)', 'T²', '√T'], 0, 'Stefan–Boltzmann.'),
          _q('Earth absorbs about…', ['240 W/m²', '1360 W/m²', '29 W/m²', '0.8 W/m²'], 0, 'NASA.'), _q('Mode needing no medium…', ['radiation', 'conduction', 'convection', 'boiling'], 0, 'Waves.')],
 'cards': [('Conduction', 'Molecular energy transfer through matter.'), ('Convection', 'Surface-to-moving-fluid transfer.'), ('Radiation', 'Electromagnetic energy exchange.'), ('h', 'Convection coefficient, W/(m²·K).'), ('k', 'Thermal conductivity, W/(m·K).'), ('Surface balance', 'In = out at a surface.')],
 'planet': {'text': ['NASA’s Earth Observatory says total solar irradiance is about 1,360 W/m², averaging about 340 W/m² over the globe; about 29% is reflected, 23% is absorbed by the atmosphere and 48% by the surface, so Earth absorbs about 240 W/m².',
                     'For a stable temperature, Earth must radiate the same 240 W/m² back to space as thermal infrared, the heat balance this course returns to in Unit 10.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Thermodynamics', 'Thermodynamics.html')],
            'src': [_EB]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapter 1.'), (_EB[0], _EB[1], 'NASA explainer.')]})
UNITS.append(
{'id': 'u2', 'title': 'Steady Conduction and Thermal Resistance', 'weeks': 'Week 2',
 'summary': 'The heat equation, one-dimensional steady conduction, thermal-resistance networks, composite walls and insulation.',
 'objectives': ['State the heat equation and its 1D steady form.', 'Build series and parallel resistance networks.', 'Compute heat loss through a composite wall.', 'Quantify the savings from insulation.'],
 'concepts': ['The heat equation balances conduction, generation and storage; at steady state with no generation, a plane wall has a linear temperature profile.',
              'Each layer acts like an electrical resistor: R = L/(kA) for conduction, 1/(hA) for convection.',
              'Series resistances add; heat flow equals overall ΔT divided by total resistance, like current.',
              'The largest resistance controls the heat flow, which is why insulation (low k) matters most.',
              'Contact resistance between layers can add surprising resistance in electronics and joints.'],
 'eqs': [('\\nabla\\cdot(k\\nabla T)+\\dot q=\\rho c\\frac{\\partial T}{\\partial t}', 'Heat equation'), ('R_{cond}=\\frac{L}{kA}', 'Conduction resistance'), ('R_{conv}=\\frac{1}{hA}', 'Convection resistance'), ('q=\\frac{T_{\\infty,1}-T_{\\infty,2}}{\\sum R}', 'Series network')],
 'worked': [
  _w('A wall has inside air (h = 8), 0.1 m insulation (k = 0.04), 0.1 m brick (k = 0.7) and outside air (h = 25), all sample values. Find the resistance per m².', ['1/8 + 0.1/0.04 + 0.1/0.7 + 1/25 = 0.125 + 2.5 + 0.1429 + 0.04.'], '2.808 m²·K/W.'),
  _w('With 20 K between inside and outside, find the heat flux and the loss through 100 m².', ['q″ = 20/2.808 = 7.12 W/m².', 'q = 100 × 7.12.'], '712 W.'),
  _w('Remove the insulation. How much does the loss grow?', ['R″ = 0.3079 m²·K/W.', 'q″ = 20/0.3079 = 64.97 W/m².'], 'About 9.1 times; insulation cuts the loss by 89.0%.')],
 'practice': [('Double the insulation to 0.2 m. New q″?', 'R″ = 5.308, q″ = 3.77 W/m².'), ('Which layer dominates the original wall?', 'The insulation, 2.5 of 2.808 m²·K/W.'),
              ('Write R for two layers in parallel.', '1/R = 1/R₁ + 1/R₂.'), ('Shape of T(x) in a plane wall at steady state?', 'Linear.')],
 'misc': [('Thin layers never matter.', 'A low-k thin layer can dominate.'), ('Resistances in series multiply.', 'They add.'), ('Air films add nothing.', 'Convection resistance is real.')],
 'quiz': [_q('Total R″…', ['2.808 m²·K/W', '2.5', '0.308', '28.08'], 0, 'Sum the layers.'), _q('Heat loss through 100 m²…', ['712 W', '71 W', '6497 W', '2000 W'], 0, '100 × 7.12.'),
          _q('Insulation savings…', ['89.0%', '50%', '9.1%', '25%'], 0, '1 − 0.3079/2.808.'), _q('Series resistances…', ['add', 'multiply', 'average', 'cancel'], 0, 'Circuit analogy.')],
 'cards': [('Thermal resistance', 'ΔT per unit heat flow.'), ('Heat equation', 'Energy balance in a solid.'), ('Composite wall', 'Layers in series.'), ('Insulation', 'Low-k material.'), ('Contact resistance', 'Resistance at an interface.'), ('U-value', 'Overall coefficient, 1/R″.')],
 'planet': {'text': ['ENERGY STAR says a typical U.S. household energy bill is around $1,900 a year and almost half of that goes to heating and cooling.',
                     'This unit’s sample wall shows why sealing and insulating comes first: adding insulation cut the conduction loss by about 89%, so any heating system has far less heat to replace.'],
            'site': [('Solutions', 'Solutions.html'), ('Thermodynamics', 'Thermodynamics.html')],
            'src': [_ES]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapter 2.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u3', 'title': 'Cylinders, Spheres and Fins', 'weeks': 'Weeks 3–4',
 'summary': 'Radial conduction, pipe insulation and the critical radius, extended surfaces, fin efficiency and electronics cooling.',
 'objectives': ['Compute radial conduction resistance.', 'Find the critical insulation radius.', 'Compute fin parameter m and fin efficiency.', 'Estimate heat from a fin.'],
 'concepts': ['In a cylinder, area grows with radius, so the temperature profile is logarithmic and R = ln(r₂/r₁)/(2πkL).',
              'Adding insulation to a small wire can increase heat loss until the outer radius passes the critical radius k/h.',
              'Fins add area where h is low (usually gases), as on engine cylinders, heat sinks and radiators.',
              'The fin parameter m = √(hP/(kA_c)) sets how fast the fin temperature decays from its base.',
              'Fin efficiency compares actual heat to the heat if the whole fin were at the base temperature.'],
 'eqs': [('R_{cyl}=\\frac{\\ln(r_2/r_1)}{2\\pi kL}', 'Radial resistance'), ('r_{cr}=\\frac{k}{h}', 'Critical radius (cylinder)'), ('m=\\sqrt{\\frac{hP}{kA_c}}', 'Fin parameter'), ('\\eta_f=\\frac{\\tanh(mL_c)}{mL_c}', 'Fin efficiency')],
 'worked': [
  _w('Pipe insulation from r = 0.05 to 0.1 m, k = 0.04 W/(m·K), 1 m long, 100 K across it (sample values). Find R and q.', ['R = ln 2/(2π × 0.04) = 2.758 K/W.', 'q = 100/2.758.'], '36.3 W per meter.'),
  _w('An aluminum pin fin (k = 200) is 5 mm across with h = 50 W/(m²·K) and a 20 mm effective length. Find η.', ['m = √(4h/(kD)) = √(200/1) = 14.14 m⁻¹.', 'mL = 0.2828.', 'η = tanh(0.2828)/0.2828.'], '0.974.'),
  _w('Heat from that fin with a 50 K base excess?', ['A_f = πDL = 3.142 × 10⁻⁴ m².', 'q = ηhA_fθ = 0.974 × 50 × 3.142 × 10⁻⁴ × 50.'], '0.765 W.')],
 'practice': [('Critical radius for k = 0.04 and h = 8?', '5 mm.'), ('Fin efficiency at L = 40 mm?', 'mL = 0.566, η = 0.905.'),
              ('Why do fins suit air more than water?', 'Air’s low h makes area the bottleneck.'), ('Profile shape in a cylinder wall?', 'Logarithmic.')],
 'misc': [('More insulation always helps.', 'Not below the critical radius.'), ('Longer fins always help a lot.', 'Efficiency drops with length.'), ('Fins work in any medium.', 'They pay off where h is low.')],
 'quiz': [_q('Pipe R…', ['2.758 K/W', '0.276', '27.6', '1.0'], 0, 'ln 2/(2π × 0.04).'), _q('Critical radius…', ['5 mm', '50 mm', '0.5 mm', '200 mm'], 0, 'k/h.'),
          _q('Fin efficiency…', ['0.974', '0.5', '0.283', '1.2'], 0, 'tanh(mL)/mL.'), _q('Fin heat…', ['0.765 W', '7.65 W', '76.5 W', '0.0765 W'], 0, 'ηhAθ.')],
 'cards': [('Critical radius', 'k/h for cylinders.'), ('Fin', 'Extended surface.'), ('Fin efficiency', 'Actual over ideal fin heat.'), ('m', 'Fin decay parameter.'), ('Heat sink', 'Array of fins.'), ('Log profile', 'Cylinder steady temperature.')],
 'planet': {'text': ['Heat moves the same way in a pipe wall as in a planet’s crust: from hot to cold, through resistances in series.',
                     'Insulating hot-water and steam pipes is one of the simplest efficiency steps in buildings and industry. All values in this unit are sample textbook values.'],
            'site': [('Solutions', 'Solutions.html'), ('Circuits', 'Circuits.html')],
            'src': [_AHTT]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapter 4.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u4', 'title': 'Transient Conduction', 'weeks': 'Week 5',
 'summary': 'The Biot number, the lumped-capacitance model, time constants, and when spatial temperature gradients matter.',
 'objectives': ['Compute the Biot number.', 'Use the lumped model when Bi < 0.1.', 'Compute a thermal time constant.', 'Find the time to reach a target temperature.'],
 'concepts': ['The Biot number compares internal conduction resistance to external convection resistance.',
              'When Bi < 0.1, the body is nearly uniform in temperature and the lumped model works.',
              'In the lumped model, the temperature excess decays exponentially with time constant τ = ρcV/(hA).',
              'For larger Bi, use one-term series solutions or charts (Heisler) or a numerical method.',
              'High heat capacity slows response: oceans and thick walls are thermal flywheels.'],
 'eqs': [('Bi=\\frac{hL_c}{k},\\ L_c=V/A', 'Biot number'), ('\\tau=\\frac{\\rho cV}{hA}', 'Time constant'), ('\\frac{T-T_\\infty}{T_i-T_\\infty}=e^{-t/\\tau}', 'Lumped response'), ('t=\\tau\\ln\\frac{\\theta_i}{\\theta}', 'Time to a target')],
 'worked': [
  _w('A 10 mm aluminum sphere (k = 237, ρ = 2700, c = 900) cools in air with h = 50. Find Bi.', ['L_c = D/6 = 1.667 × 10⁻³ m.', 'Bi = 50 × 1.667 × 10⁻³/237.'], '3.52 × 10⁻⁴, so the lumped model works.'),
  _w('Find τ for that sphere.', ['τ = 2700 × 900 × 1.667 × 10⁻³/50.'], '81 s.'),
  _w('How long to cool from 300 °C to 50 °C in 20 °C air?', ['θ_i = 280 K, θ = 30 K.', 't = 81 ln(280/30) = 81 × 2.234.'], '181 s.')],
 'practice': [('Fraction of the excess left after one τ?', 'e⁻¹ = 0.368.'), ('Time to halve the excess?', 'τ ln 2 = 56.1 s.'),
              ('Bi = 0.5. Is lumped valid?', 'No; use series or numerical solutions.'), ('Double h. What happens to τ?', 'It halves to 40.5 s.')],
 'misc': [('Bi is the Nusselt number.', 'Bi uses the solid’s k; Nu uses the fluid’s.'), ('Lumped works for any size.', 'Only when Bi < 0.1.'), ('Cooling is linear in time.', 'It is exponential.')],
 'quiz': [_q('Time constant…', ['81 s', '8.1 s', '810 s', '181 s'], 0, 'ρcV/(hA).'), _q('Cooling time to 50 °C…', ['181 s', '81 s', '56 s', '300 s'], 0, 'τ ln(280/30).'),
          _q('Lumped valid when…', ['Bi < 0.1', 'Bi > 1', 'Re > 5 × 10⁵', 'Nu < 1'], 0, 'Uniform body.'), _q('After one τ…', ['36.8% left', '50% left', '0% left', '63.2% left'], 0, 'e⁻¹.')],
 'cards': [('Biot number', 'Internal over external resistance.'), ('Lumped capacitance', 'Uniform-temperature model.'), ('Time constant', 'ρcV/(hA).'), ('Heisler chart', 'One-term transient solution chart.'), ('Thermal mass', 'Heat capacity that slows change.'), ('L_c', 'V/A characteristic length.')],
 'planet': {'text': ['NASA’s Earth Observatory notes that Earth’s surface averages about 15 °C, more than 30 °C warmer than it would be with no atmosphere.',
                     'In this unit’s language, a large heat capacity means a long time constant; the oceans’ heat capacity gives Earth’s climate a slow response (a textbook idea, not a NASA figure).'],
            'site': [('Oceans', 'Oceans.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_EB]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapter 5.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u5', 'title': 'External Forced Convection', 'weeks': 'Weeks 6–7',
 'summary': 'Boundary layers, Reynolds, Prandtl and Nusselt numbers, flat-plate correlations and flow over cylinders.',
 'objectives': ['Compute Re, Pr and Nu.', 'Use the laminar flat-plate correlation.', 'Find h and the heat rate.', 'Check transition at Re ≈ 5 × 10⁵.'],
 'concepts': ['Velocity and thermal boundary layers form on a surface; heat crosses the thin layer of slow fluid by conduction.',
              'The Nusselt number Nu = hL/k is the dimensionless heat transfer coefficient.',
              'The Prandtl number compares momentum and thermal diffusivity (about 0.7 for air, about 7 for water near room temperature, textbook values).',
              'On a flat plate, flow is usually laminar below Re ≈ 5 × 10⁵; turbulence raises h.',
              'Correlations are fits to experiments; use them inside their stated ranges.'],
 'eqs': [('Re_L=\\frac{VL}{\\nu}', 'Reynolds number'), ('Nu_L=\\frac{\\bar hL}{k}', 'Nusselt number'), ('\\overline{Nu}_L=0.664Re_L^{1/2}Pr^{1/3}', 'Laminar flat plate (average)'), ('\\overline{Nu}_L=0.037Re_L^{4/5}Pr^{1/3}', 'Turbulent flat plate (average)')],
 'worked': [
  _w('Air (ν = 1.5 × 10⁻⁵, k = 0.026, Pr = 0.71) flows at 5 m/s over a 0.5 m plate. Find Re.', ['Re = 5 × 0.5/1.5 × 10⁻⁵.'], '166,667, laminar.'),
  _w('Find the average Nu and h.', ['Nu = 0.664 × 166,667^½ × 0.71^⅓ = 0.664 × 408.2 × 0.892 = 241.8.', 'h = 241.8 × 0.026/0.5.'], '12.6 W/(m²·K).'),
  _w('Heat from a 0.5 × 1 m plate 30 K above the air?', ['q = 12.58 × 0.5 × 30.'], '189 W.')],
 'practice': [('Repeat h at 10 m/s.', 'Re = 333,333, h = 17.8 W/(m²·K) (√2 times higher).'), ('Re at 1 m/s?', '33,333.'),
              ('Name the dimensionless h.', 'Nusselt number.'), ('Why does turbulence raise h?', 'Mixing thins the slow near-wall layer.')],
 'misc': [('Nu uses the solid’s k.', 'It uses the fluid’s k.'), ('One correlation fits all flows.', 'Check range and geometry.'), ('h is constant along a plate.', 'Local h falls as the layer grows.')],
 'quiz': [_q('Re at 5 m/s…', ['166,667', '16,667', '1.67 × 10⁶', '6000'], 0, 'VL/ν.'), _q('Average h…', ['12.6 W/(m²·K)', '126', '1.26', '242'], 0, 'Nu k/L.'),
          _q('Heat rate…', ['189 W', '18.9 W', '377 W', '63 W'], 0, 'hAΔT.'), _q('Transition near…', ['5 × 10⁵', '2300', '10³', '10⁹'], 0, 'Flat plate.')],
 'cards': [('Reynolds number', 'Inertia over viscosity.'), ('Prandtl number', 'ν/α.'), ('Nusselt number', 'hL/k.'), ('Boundary layer', 'Thin near-wall region.'), ('Correlation', 'Fit to experiments.'), ('Transition', 'Laminar to turbulent.')],
 'planet': {'text': ['NASA’s Earth Observatory says convection carries about 5% of incoming solar energy from the surface into the atmosphere, while evaporation carries about 25%.',
                     'Wind speed sets h over oceans and land just as velocity sets h on this unit’s plate, which is why winds shape how fast the surface sheds heat.'],
            'site': [('Fluid Mechanics', 'Fluid_Mechanics.html'), ('Oceans', 'Oceans.html')],
            'src': [_EB]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapters 6–7.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u6', 'title': 'Internal Flow and Heat Exchangers', 'weeks': 'Weeks 8–9',
 'summary': 'Pipe-flow convection, mean temperature, the Dittus–Boelter correlation, heat exchanger types, LMTD and effectiveness–NTU.',
 'objectives': ['Use laminar and turbulent pipe correlations.', 'Compute a log-mean temperature difference.', 'Size a heat exchanger with UA and LMTD.', 'Use effectiveness–NTU.'],
 'concepts': ['In a pipe, the bulk (mean) temperature changes along the length as heat enters or leaves.',
              'Fully developed laminar flow with constant wall temperature has Nu = 3.66; turbulent flow uses Dittus–Boelter (textbook correlations).',
              'Counterflow exchangers beat parallel flow because the temperature difference stays more even.',
              'The LMTD method suits sizing when all four temperatures are known.',
              'The ε-NTU method suits rating when outlet temperatures are unknown.'],
 'eqs': [('Nu_D=0.023Re_D^{4/5}Pr^{0.4}', 'Dittus–Boelter (heating)'), ('\\Delta T_{lm}=\\frac{\\Delta T_1-\\Delta T_2}{\\ln(\\Delta T_1/\\Delta T_2)}', 'Log-mean temperature difference'), ('q=UA\\Delta T_{lm}', 'Exchanger heat rate'), ('\\varepsilon=1-e^{-NTU}\\ (C_r=0)', 'Effectiveness, condenser or evaporator')],
 'worked': [
  _w('Water (k = 0.6, Pr = 7, textbook values) flows at Re = 20,000 in a 20 mm tube. Find h.', ['Nu = 0.023 × 20,000^0.8 × 7^0.4 = 138.2.', 'h = 138.2 × 0.6/0.02.'], 'About 4150 W/(m²·K).'),
  _w('Counterflow: hot 90 → 50 °C, cold 20 → 40 °C. Find the LMTD.', ['ΔT₁ = 90 − 40 = 50 K; ΔT₂ = 50 − 20 = 30 K.', 'LMTD = 20/ln(50/30).'], '39.15 K.'),
  _w('With U = 500 W/(m²·K) and A = 2 m², find q.', ['q = 500 × 2 × 39.15.'], '39.2 kW.')],
 'practice': [('ε for NTU = 2 when one stream condenses (C_r = 0)?', '1 − e⁻² = 0.865.'), ('Laminar Nu for constant wall temperature?', '3.66.'),
              ('Why prefer counterflow?', 'More even ΔT, more heat per area.'), ('Dittus–Boelter Nu for Pr = 0.7, Re = 20,000?', '55.0.')],
 'misc': [('Use the arithmetic mean ΔT.', 'Use the log mean.'), ('ε can exceed 1.', 'It cannot.'), ('Laminar correlations work for turbulent flow.', 'Check Re first.')],
 'quiz': [_q('LMTD…', ['39.15 K', '40 K', '30 K', '50 K'], 0, '20/ln(5/3).'), _q('Exchanger q…', ['39.2 kW', '3.92 kW', '20 kW', '78 kW'], 0, 'UA LMTD.'),
          _q('ε at NTU 2…', ['0.865', '0.5', '0.98', '2'], 0, '1 − e⁻².'), _q('Water h…', ['≈ 4150 W/(m²·K)', '≈ 41', '≈ 415,000', '≈ 1.4'], 0, 'Nu k/D.')],
 'cards': [('LMTD', 'Log-mean ΔT.'), ('NTU', 'UA/C_min.'), ('Effectiveness', 'Actual over maximum heat.'), ('Counterflow', 'Opposite stream directions.'), ('Fouling', 'Deposits that add resistance.'), ('Dittus–Boelter', 'Turbulent pipe correlation.')],
 'planet': {'text': ['ENERGY STAR explains that an air-source heat pump moves heat between indoor and outdoor air instead of making it from fuel, using heat exchangers (coils) on both sides.',
                     'Better exchangers need a smaller temperature difference to move the same heat, which is one reason modern heat pumps deliver more heat per unit of electricity.'],
            'site': [('Solutions', 'Solutions.html'), ('Thermodynamics', 'Thermodynamics.html')],
            'src': [_ES]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapters 3 and 7.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u7', 'title': 'Natural Convection and Boiling', 'weeks': 'Week 10',
 'summary': 'Buoyancy-driven flow, Grashof and Rayleigh numbers, vertical-plate correlations, and an introduction to boiling and condensation.',
 'objectives': ['Compute the Rayleigh number.', 'Use a vertical-plate correlation.', 'Compare natural and forced h.', 'Describe the boiling curve.'],
 'concepts': ['Warm fluid is lighter and rises; buoyancy, not a fan, drives the flow.',
              'The Rayleigh number Ra = gβΔTL³/(να) plays the role Re plays in forced flow.',
              'On a vertical plate, flow is laminar below about Ra = 10⁹ (textbook value).',
              'Natural-convection h in air is only a few W/(m²·K), so radiation is often comparable.',
              'Boiling and condensation move large heat at small ΔT because of latent heat.'],
 'eqs': [('Ra_L=\\frac{g\\beta\\Delta TL^3}{\\nu\\alpha}', 'Rayleigh number'), ('\\overline{Nu}_L=0.59Ra_L^{1/4}', 'Laminar vertical plate'), ('\\beta=1/T', 'Ideal-gas expansion coefficient'), ('Gr=Ra/Pr', 'Grashof number')],
 'worked': [
  _w('A 0.3 m vertical plate is 30 K above air (β = 1/300 K⁻¹, ν = 1.6 × 10⁻⁵, α = 2.2 × 10⁻⁵, sample values). Find Ra.', ['Ra = 9.80665 × (1/300) × 30 × 0.3³/(1.6 × 10⁻⁵ × 2.2 × 10⁻⁵).'], '7.52 × 10⁷, laminar.'),
  _w('Find Nu and h with k = 0.026.', ['Nu = 0.59 × (7.52 × 10⁷)^¼ = 54.9.', 'h = 54.9 × 0.026/0.3.'], '4.76 W/(m²·K).'),
  _w('Heat from a 0.3 × 1 m plate?', ['q = 4.76 × 0.3 × 30.'], '42.9 W.')],
 'practice': [('Compare with Unit 5’s forced h of 12.6.', 'Forced is about 2.64 times higher.'), ('Laminar limit on Ra?', 'About 10⁹.'),
              ('Why is boiling so effective?', 'Latent heat moves energy at small ΔT.'), ('β for an ideal gas at 300 K?', '1/300 K⁻¹ = 3.33 × 10⁻³.')],
 'misc': [('Natural convection is negligible.', 'It often matches radiation.'), ('Ra uses velocity.', 'It uses buoyancy.'), ('Boiling h is low.', 'It is among the highest.')],
 'quiz': [_q('Ra…', ['7.52 × 10⁷', '7.52 × 10⁹', '752', '5 × 10⁵'], 0, 'gβΔTL³/(να).'), _q('h…', ['4.76 W/(m²·K)', '47.6', '0.476', '12.6'], 0, 'Nu k/L.'),
          _q('Heat…', ['42.9 W', '429 W', '4.29 W', '189 W'], 0, 'hAΔT.'), _q('Driver of natural convection…', ['buoyancy', 'a pump', 'radiation', 'pressure drop'], 0, 'Density difference.')],
 'cards': [('Rayleigh number', 'Buoyancy strength.'), ('Grashof number', 'Buoyancy over viscosity.'), ('β', 'Expansion coefficient.'), ('Boiling curve', 'Heat flux vs wall superheat.'), ('Critical heat flux', 'Peak nucleate boiling flux.'), ('Condensation', 'Vapor to liquid on a cold wall.')],
 'planet': {'text': ['NASA’s Earth Observatory says evaporation removes about 25% of incoming solar energy from the surface and convection about 5%; the latent heat is released when water vapor condenses into clouds.',
                     'At 340 W/m² average sunlight, those shares are about 85 and 17 W/m², the same phase-change and buoyancy processes this unit treats.'],
            'site': [('Oceans', 'Oceans.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_EB]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapters 8–9.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u8', 'title': 'Radiation Fundamentals', 'weeks': 'Week 11',
 'summary': 'Blackbodies, Planck’s law, Wien’s law, the Stefan–Boltzmann law, emissivity, absorptivity and Kirchhoff’s law.',
 'objectives': ['Find a blackbody’s peak wavelength.', 'Compute emissive power.', 'Use emissivity and absorptivity.', 'Find a planet’s effective temperature.'],
 'concepts': ['A blackbody absorbs all radiation and emits the most possible at each temperature and wavelength.',
              'Wien’s law: peak wavelength is inversely proportional to absolute temperature.',
              'Total emissive power grows as σT⁴, so doubling temperature multiplies emission by 16.',
              'Real surfaces emit a fraction ε of blackbody power; for a gray surface α = ε (Kirchhoff).',
              'Solar radiation is short-wave; Earth’s emission is long-wave infrared, which is why gases like CO₂ and water vapor matter.'],
 'eqs': [('\\lambda_{max}T=2898\\ \\mu m\\cdot K', 'Wien’s displacement law'), ('E_b=\\sigma T^4', 'Stefan–Boltzmann'), ('E=\\varepsilon\\sigma T^4', 'Real surface'), ('T_e=\\left(\\frac{\\bar S(1-a)}{\\sigma}\\right)^{1/4}', 'Effective temperature')],
 'worked': [
  _w('NASA gives the Sun about 5,800 K. Find its peak wavelength.', ['2898/5800.'], '0.500 µm, visible light.'),
  _w('Earth absorbs about 240 W/m² (NASA). Find its effective temperature.', ['T = (240/5.670374419 × 10⁻⁸)^¼.'], '255.1 K, about −18 °C (NASA rounds to about −20 °C).'),
  _w('Blackbody emission from a 288 K surface?', ['σ × 288⁴.'], '390 W/m².')],
 'practice': [('Peak wavelength at 288 K?', '10.06 µm, thermal infrared.'), ('Emission ratio when T doubles?', '2⁴ = 16.'),
              ('Peak for a 3000 K lamp filament?', '0.966 µm, near infrared.'), ('Gray surface with ε = 0.8: α?', '0.8.')],
 'misc': [('Hot means visible.', 'Room-temperature objects glow in infrared.'), ('Use °C in σT⁴.', 'Use kelvin.'), ('Shiny means cold.', 'Low ε means it emits and absorbs little.')],
 'quiz': [_q('Sun peak…', ['0.500 µm', '10 µm', '5 µm', '0.05 µm'], 0, '2898/5800.'), _q('Earth effective temperature…', ['255 K', '288 K', '300 K', '5800 K'], 0, '(240/σ)^¼.'),
          _q('Double T, emission…', ['×16', '×2', '×4', '×8'], 0, 'T⁴.'), _q('288 K blackbody…', ['390 W/m²', '240 W/m²', '1360 W/m²', '39 W/m²'], 0, 'σT⁴.')],
 'cards': [('Blackbody', 'Perfect absorber and emitter.'), ('Wien’s law', 'λ_max T = 2898 µm·K.'), ('Emissivity', 'Emission relative to blackbody.'), ('Kirchhoff’s law', 'α = ε for gray surfaces.'), ('Planck’s law', 'Spectral blackbody emission.'), ('Effective temperature', 'Blackbody-equivalent T.')],
 'planet': {'text': ['NASA’s Earth Observatory says the Sun’s surface is about 5,800 K, Earth’s effective radiating temperature is about −20 °C, and doubling an object’s temperature multiplies its radiated energy by 16.',
                     'NASA also notes that water vapor lets most infrared escape between 8 and 14 µm, while carbon dioxide absorbs at wavelengths beyond about 12–13 µm, near the edge of that window.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Solutions', 'Solutions.html')],
            'src': [_EB]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapter 10.'), ('PhET: Blackbody Spectrum', _PH + 'blackbody-spectrum', 'Free simulation.')]})
UNITS.append(
{'id': 'u9', 'title': 'Radiation Exchange and Shields', 'weeks': 'Weeks 12–13',
 'summary': 'View factors, reciprocity, gray-surface networks, parallel plates, radiation shields and thermal protection in space.',
 'objectives': ['Use view-factor reciprocity.', 'Compute net exchange between parallel plates.', 'Show how a shield cuts heat flow.', 'Estimate radiation from a hot shield.'],
 'concepts': ['The view factor F₁₂ is the fraction of radiation leaving surface 1 that reaches surface 2.',
              'Reciprocity: A₁F₁₂ = A₂F₂₁; summation: the view factors from a surface add to 1.',
              'Gray surfaces exchange heat through surface resistances (1 − ε)/(εA) and space resistances 1/(A₁F₁₂).',
              'A thin low-ε shield between two plates adds resistances and cuts exchange sharply; multilayer insulation stacks many.',
              'A heat shield facing the Sun gets hot, reradiates, and protects what lies in its shadow.'],
 'eqs': [('A_1F_{12}=A_2F_{21}', 'Reciprocity'), ('q^{\\prime\\prime}=\\frac{\\sigma(T_1^4-T_2^4)}{1/\\varepsilon_1+1/\\varepsilon_2-1}', 'Parallel plates'), ('R_{surf}=\\frac{1-\\varepsilon}{\\varepsilon A}', 'Surface resistance'), ('R_{space}=\\frac{1}{A_1F_{12}}', 'Space resistance')],
 'worked': [
  _w('Large parallel plates at 400 K and 300 K, both ε = 0.8. Net flux?', ['Denominator: 1.25 + 1.25 − 1 = 1.5.', 'q″ = σ(400⁴ − 300⁴)/1.5.'], '662 W/m².'),
  _w('Insert a shield with ε = 0.05 on both sides.', ['Resistance: 2 × (1.25 + 20 − 1) = 40.5.', 'q″ = σ × 1.75 × 10¹⁰/40.5.'], '24.5 W/m², 27 times less.'),
  _w('A small sphere (A₁ = 1 m²) sits inside a shell of area 4 m². Find F₂₁.', ['F₁₂ = 1.', 'F₂₁ = A₁F₁₂/A₂.'], '0.25.')],
 'practice': [('Blackbody flux at Parker’s 1,377 °C shield limit?', 'σ × 1650.15⁴ = 4.20 × 10⁵ W/m².'), ('Why does one shield with ε = 0.05 work so well?', 'Its two surface resistances add about 39.'),
              ('Sum of view factors from an enclosure surface?', '1.'), ('What is MLI?', 'Many thin low-ε shields in a stack.')],
 'misc': [('View factors are symmetric.', 'Only A₁F₁₂ = A₂F₂₁.'), ('Shields must be thick.', 'Low ε matters, not thickness.'), ('Black surfaces make good shields.', 'Shields need low ε.')],
 'quiz': [_q('Plate flux…', ['662 W/m²', '993 W/m²', '24.5 W/m²', '1000 W/m²'], 0, 'σΔT⁴/1.5.'), _q('With shield…', ['24.5 W/m²', '331 W/m²', '66 W/m²', '2.45 W/m²'], 0, '÷ 40.5.'),
          _q('F₂₁…', ['0.25', '1', '4', '0.5'], 0, 'Reciprocity.'), _q('Good shields have…', ['low ε', 'high ε', 'high k', 'high h'], 0, 'Weak emitters.')],
 'cards': [('View factor', 'Fraction of radiation intercepted.'), ('Reciprocity', 'A₁F₁₂ = A₂F₂₁.'), ('Radiosity', 'All radiation leaving a surface.'), ('Radiation shield', 'Low-ε barrier.'), ('MLI', 'Multilayer insulation.'), ('Gray surface', 'ε independent of wavelength.')],
 'planet': {'text': ['NASA says Parker Solar Probe, launched August 12, 2018, is protected by a 4.5-inch (11.43 cm) carbon-composite shield that withstands nearly 2,500 °F (1,377 °C) as the spacecraft passes about 3.9 million miles (6.2 million km) from the Sun.',
                     'In 2021 Parker became the first spacecraft to fly through the Sun’s corona; its shield keeps the instruments behind it in shadow, the same idea as this unit’s radiation shield.'],
            'site': [('Spacecraft Design', 'Spacecraft_Design.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_PSP]},
 'res': [(_AHTT[0], _AHTT[1], 'Free textbook, Chapter 10.'), (_PSP[0], _PSP[1], 'NASA mission page.')]})
UNITS.append(
{'id': 'u10', 'title': 'Heat Pumps, Buildings and Earth’s Energy Balance', 'weeks': 'Weeks 14–15',
 'summary': 'Heat-pump COP, Carnot limits, whole-building heat loss, and the planetary energy imbalance measured from space.',
 'objectives': ['Compute heat-pump COP and its Carnot limit.', 'Size electricity for a heating load.', 'Convert a flux imbalance to total power.', 'Connect all three modes in one system.'],
 'concepts': ['A heat pump moves heat from cold to hot using work; its heating COP is heat delivered divided by work.',
              'The Carnot COP, T_h/(T_h − T_c), is an upper limit that falls as the outdoor temperature drops.',
              'A building’s heat loss is its UA times the indoor–outdoor difference; insulation lowers UA before you buy equipment.',
              'Earth’s energy imbalance is a small difference between two large flows, measured by satellites such as NASA’s CERES instruments.',
              'Every system in this course combines conduction, convection and radiation in a resistance network.'],
 'eqs': [('COP_h=\\frac{Q_h}{W}', 'Heating COP'), ('COP_{Carnot}=\\frac{T_h}{T_h-T_c}', 'Carnot limit'), ('Q=UA\\Delta T', 'Building heat loss'), ('P=\\Delta F\\cdot A_E', 'Planetary imbalance power')],
 'worked': [
  _w('ENERGY STAR says a heat pump can deliver up to three times more heat than the electricity it uses. Electricity for 9 kW of heat?', ['W = 9/3.'], '3 kW.'),
  _w('Carnot heating COP with 35 °C (308 K) delivery and 0 °C (273 K) outdoors?', ['308/(308 − 273).'], '8.8; real units reach about a third of that.'),
  _w('NASA says the imbalance is a little over 0.8 W/m². With Earth’s area 5.1 × 10¹⁴ m² (textbook value), total power?', ['0.8 × 5.1 × 10¹⁴.'], 'About 4.1 × 10¹⁴ W.')],
 'practice': [('Half of a $1,900 yearly energy bill?', 'About $950 for heating and cooling.'), ('Carnot COP at −10 °C (263 K) outdoors, 308 K delivery?', '6.84.'),
              ('Why insulate before buying a heat pump?', 'Lower UA means a smaller, cheaper unit.'), ('What does CERES measure?', 'Earth’s radiant energy from space.')],
 'misc': [('COP above 1 breaks energy conservation.', 'Heat is moved, not created.'), ('Turn heat pumps way down at night.', 'ENERGY STAR advises a steady setting.'), ('0.8 W/m² is negligible.', 'Over Earth it is about 4 × 10¹⁴ W.')],
 'quiz': [_q('Electricity for 9 kW at COP 3…', ['3 kW', '27 kW', '9 kW', '1 kW'], 0, '9/3.'), _q('Carnot COP…', ['8.8', '3', '1.13', '35'], 0, '308/35.'),
          _q('Imbalance power…', ['≈ 4.1 × 10¹⁴ W', '≈ 4 × 10⁹ W', '≈ 0.8 W', '≈ 10²⁰ W'], 0, '0.8 × 5.1 × 10¹⁴.'), _q('Lower UA by…', ['insulating', 'raising COP', 'adding fins', 'painting black'], 0, 'Resistance.')],
 'cards': [('COP', 'Heat delivered per unit work.'), ('Carnot COP', 'Ideal limit.'), ('UA', 'Overall conductance.'), ('Energy imbalance', 'Absorbed minus emitted.'), ('CERES', 'NASA radiation-budget instruments.'), ('Heat pump', 'Moves heat with work.')],
 'planet': {'text': ['ENERGY STAR says an air-source heat pump can deliver up to three times more heat energy than the electrical energy it uses, because it moves heat instead of making it.',
                     'NASA’s Earth Observatory says Earth is absorbing a little more than 0.8 W/m² more than it emits; NASA’s CERES instruments measure the radiation budget from orbit.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_ES, _EB, _CER]},
 'res': [(_ES[0], _ES[1], 'ENERGY STAR guide.'), (_CER[0], _CER[1], 'NASA CERES.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Heat flow and a wall-insulation calculator', 'week': 'Week 2',
 'goal': 'Watch heat flow between objects in PhET Energy Forms and Changes, then compute wall heat flux for several insulation thicknesses.',
 'eq': ('q^{\\prime\\prime}=\\Delta T/R^{\\prime\\prime}', 'Series wall'),
 'steps': ['In PhET Energy Forms and Changes, heat a block and watch energy flow to its neighbor and the air.', 'In a spreadsheet, enter Unit 2’s wall without insulation: R″ = 0.3079 m²·K/W.', 'Add insulation layers of 0.05, 0.1 and 0.2 m (k = 0.04) and compute q″ for ΔT = 20 K.', 'Plot q″ against thickness and note the diminishing returns.'],
 'table': (['Insulation (m)', 'R″ (m²·K/W)', 'q″ (W/m²)'], [['0', '0.3079', '64.96'], ['0.05', '1.558', '12.84'], ['0.1', '2.808', '7.12'], ['0.2', '5.308', '3.77']]),
 'note': 'Computed sample values.',
 'calc': ['R″(0.05) = 0.3079 + 0.05/0.04 = 1.558.', 'q″ = 20/1.558 = 12.84 W/m².'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('PhET: Energy Forms and Changes', _PH + 'energy-forms-and-changes')],
 'planet': 'ENERGY STAR: almost half of a typical $1,900 household energy bill goes to heating and cooling.', 'planet_src': [_ES]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Fin efficiency explorer', 'week': 'Week 4',
 'goal': 'Compute pin-fin efficiency for several lengths and see where adding length stops paying off.',
 'eq': ('\\eta_f=\\tanh(mL)/(mL)', 'Fin efficiency'),
 'steps': ['Enter Unit 3’s fin: k = 200, D = 5 mm, h = 50, so m = 14.14 m⁻¹.', 'Compute η for L = 10, 20 and 40 mm.', 'Compute fin heat for a 50 K base excess.', 'Change h to 200 and repeat.'],
 'table': (['L (mm)', 'mL', 'η'], [['10', '0.1414', '0.993'], ['20', '0.2828', '0.974'], ['40', '0.5657', '0.905']]),
 'note': 'Computed sample values.',
 'calc': ['m = √(4 × 50/(200 × 0.005)) = 14.14 m⁻¹.', 'η(40 mm) = tanh(0.5657)/0.5657 = 0.905.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_AHTT[0], _AHTT[1])],
 'planet': 'Efficient fins and exchangers let heat pumps move more heat per unit of electricity (ENERGY STAR).', 'planet_src': [_ES]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Lumped cooling curve', 'week': 'Week 5',
 'goal': 'Model Unit 4’s aluminum sphere cooling in a spreadsheet and compare an exact curve with a step-by-step (Euler) solution.',
 'eq': ('T=T_\\infty+(T_i-T_\\infty)e^{-t/\\tau}', 'Lumped response'),
 'steps': ['Enter T_i = 300 °C, T∞ = 20 °C, τ = 81 s.', 'Compute T every τ out to 3τ.', 'Add an Euler column with a 5 s step and compare.', 'Double h and repeat.'],
 'table': (['t (s)', 'T (°C)'], [['0', '300'], ['81', '123.0'], ['162', '57.9'], ['243', '33.9']]),
 'note': 'Computed sample values.',
 'calc': ['T(81) = 20 + 280e⁻¹ = 123.0 °C.', 'T(243) = 20 + 280e⁻³ = 33.9 °C.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('PhET: Energy Forms and Changes', _PH + 'energy-forms-and-changes')],
 'planet': 'NASA: Earth’s surface averages about 15 °C, more than 30 °C warmer than with no atmosphere.', 'planet_src': [_EB]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Flat-plate convection calculator', 'week': 'Week 7',
 'goal': 'Compute Re and average h for air over a 0.5 m plate at several speeds.',
 'eq': ('\\bar h=0.664\\frac{k}{L}Re_L^{1/2}Pr^{1/3}', 'Laminar plate'),
 'steps': ['Enter air properties: ν = 1.5 × 10⁻⁵, k = 0.026, Pr = 0.71.', 'Compute Re and h at 1, 5 and 10 m/s.', 'Check each Re is below 5 × 10⁵.', 'Plot h against √V.'],
 'table': (['V (m/s)', 'Re', 'h (W/(m²·K))'], [['1', '33,333', '5.62'], ['5', '166,667', '12.58'], ['10', '333,333', '17.78']]),
 'note': 'Computed sample values.',
 'calc': ['Re(1) = 1 × 0.5/1.5 × 10⁻⁵ = 33,333.', 'h(10) = 0.664 × 577.4 × 0.892 × 0.052 = 17.78.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MIT[0], _MIT[1])],
 'planet': 'NASA: convection carries about 5% of incoming solar energy from the surface.', 'planet_src': [_EB]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Blackbody spectra', 'week': 'Week 11',
 'goal': 'Use PhET Blackbody Spectrum to see Wien’s law, then check peaks in a spreadsheet.',
 'eq': ('\\lambda_{max}=2898/T', 'Wien’s law'),
 'steps': ['In PhET Blackbody Spectrum, set the Sun, a lamp and Earth.', 'Read the peak wavelength from the graph.', 'Compute 2898/T for 288, 3000 and 5800 K.', 'Compute σT⁴ for each.'],
 'table': (['T (K)', 'λ_max (µm)', 'σT⁴ (W/m²)'], [['288', '10.06', '390'], ['3000', '0.966', '4.59 × 10⁶'], ['5800', '0.500', '6.42 × 10⁷']]),
 'note': 'Computed values.',
 'calc': ['2898/288 = 10.06 µm.', 'σ × 5800⁴ = 6.42 × 10⁷ W/m².'],
 'safety': ['Computer only.'], 'home': ['Runs in a browser.'],
 'sims': [('PhET: Blackbody Spectrum', _PH + 'blackbody-spectrum')],
 'planet': 'NASA: the Sun is about 5,800 K.', 'planet_src': [_EB]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Greenhouse effect and energy balance', 'week': 'Week 14',
 'goal': 'Explore PhET Greenhouse Effect, then compute Earth’s effective temperature for several albedos.',
 'eq': ('T_e=\\left(\\frac{S(1-a)}{4\\sigma}\\right)^{1/4}', 'Effective temperature'),
 'steps': ['In PhET Greenhouse Effect, add and remove clouds and greenhouse gases and watch the temperature.', 'In a spreadsheet, use S = 1360 W/m² (NASA).', 'Compute T_e for albedo 0.25, 0.29 and 0.35.', 'Explain why T_e is below NASA’s 15 °C surface average.'],
 'table': (['Albedo', 'T_e (K)'], [['0.25', '259.0'], ['0.29', '255.4'], ['0.35', '249.9']]),
 'note': 'Computed values.',
 'calc': ['(1360 × 0.71/(4σ))^¼ = 255.4 K.', '255.4 − 273.15 = −17.7 °C.'],
 'safety': ['Computer only.'], 'home': ['Runs in a browser.'],
 'sims': [('PhET: Greenhouse Effect', _PH + 'greenhouse-effect')],
 'planet': 'NASA: about 29% of sunlight is reflected and Earth absorbs about 240 W/m².', 'planet_src': [_EB]})
SCHEDULE = [(1, 'u1', 'Modes and energy balances', 'Lienhard AHTT'), (2, 'u2', 'Thermal resistance; Lab A', 'Lienhard AHTT'),
            (3, 'u3', 'Cylinders and critical radius', 'Lienhard AHTT'), (4, 'u3', 'Fins; Lab B', 'MIT 2.51'),
            (5, 'u4', 'Transient conduction; Lab C', 'Lienhard AHTT'), (6, 'u5', 'Boundary layers', 'MIT 2.51'),
            (7, 'u5', 'Flat-plate correlations; Lab D; midterm practice', 'Lienhard AHTT'), (8, 'u6', 'Internal flow', 'MIT 2.51'),
            (9, 'u6', 'Heat exchangers', 'Lienhard AHTT'), (10, 'u7', 'Natural convection and boiling', 'Lienhard AHTT'),
            (11, 'u8', 'Radiation fundamentals; Lab E', 'NASA Earth Observatory'), (12, 'u9', 'View factors', 'Lienhard AHTT'),
            (13, 'u9', 'Shields and Parker Solar Probe', 'NASA Parker Solar Probe'), (14, 'u10', 'Heat pumps and Earth’s balance; Lab F', 'ENERGY STAR'), (15, 'u10', 'Review; final practice', 'MIT 2.51')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Convection from 3 m² at h = 15 W/(m²·K), ΔT = 20 K?', ['15 × 3 × 20.'], '900 W.'),
  ('Heat flux through 0.15 m of insulation (k = 0.04) plus 0.3079 m²·K/W of other layers at ΔT = 20 K?', ['R″ = 0.3079 + 3.75 = 4.058.', '20/4.058.'], '4.93 W/m².'),
  ('Critical radius for k = 0.1 and h = 10?', ['k/h.'], '10 mm.'),
  ('τ for a 20 mm aluminum sphere, h = 50?', ['2700 × 900 × (0.02/6)/50.'], '162 s.'),
  ('Re for air at 2 m/s over 0.5 m?', ['2 × 0.5/1.5 × 10⁻⁵.'], '66,667.')]),
 ('Final practice set (Units 1–10)', [
  ('LMTD for ΔT₁ = 60 K and ΔT₂ = 20 K?', ['40/ln 3.'], '36.4 K.'),
  ('ε for NTU = 1, C_r = 0?', ['1 − e⁻¹.'], '0.632.'),
  ('Ra for Unit 7’s plate at L = 0.6 m?', ['7.52 × 10⁷ × 8.'], '6.02 × 10⁸.'),
  ('Peak wavelength at 1000 K?', ['2898/1000.'], '2.90 µm.'),
  ('Parallel plates 500 K and 300 K, ε = 0.9 both?', ['σ(500⁴ − 300⁴)/(2/0.9 − 1).'], '2524 W/m².'),
  ('Carnot heating COP, 318 K delivery, 268 K outdoors?', ['318/50.'], '6.36.')])]
FORMULAS = ['q=kA\\Delta T/L,\\ q=hA\\Delta T,\\ q=\\varepsilon\\sigma A(T_s^4-T_{sur}^4)', 'R=L/(kA),\\ R=1/(hA),\\ q=\\Delta T/\\sum R', 'R_{cyl}=\\ln(r_2/r_1)/(2\\pi kL),\\ r_{cr}=k/h',
            'm=\\sqrt{hP/(kA_c)},\\ \\eta_f=\\tanh(mL)/(mL)', 'Bi=hL_c/k,\\ \\tau=\\rho cV/(hA),\\ \\theta/\\theta_i=e^{-t/\\tau}', 'Re=VL/\\nu,\\ Nu=hL/k,\\ Nu=0.664Re^{1/2}Pr^{1/3}',
            'Nu=0.023Re^{0.8}Pr^{0.4},\\ \\Delta T_{lm}=(\\Delta T_1-\\Delta T_2)/\\ln(\\Delta T_1/\\Delta T_2)', 'Ra=g\\beta\\Delta TL^3/(\\nu\\alpha),\\ Nu=0.59Ra^{1/4}',
            '\\lambda_{max}T=2898,\\ E_b=\\sigma T^4,\\ A_1F_{12}=A_2F_{21}', 'COP=Q_h/W,\\ COP_C=T_h/(T_h-T_c),\\ P=\\Delta F A_E']
GLOSSARY = sorted([('Albedo', 'Fraction of sunlight reflected.'), ('Biot number', 'Internal over external thermal resistance.'), ('Blackbody', 'Perfect absorber and emitter.'), ('Boundary layer', 'Thin near-wall flow region.'),
    ('COP', 'Heat moved per unit work.'), ('Critical radius', 'Radius of maximum heat loss from an insulated cylinder.'), ('Effectiveness', 'Actual over maximum exchanger heat.'), ('Emissivity', 'Emission relative to a blackbody.'),
    ('Energy imbalance', 'Absorbed minus emitted planetary energy.'), ('Fin efficiency', 'Actual over ideal fin heat.'), ('Fourier’s law', 'Conduction rate law.'), ('Heat exchanger', 'Device moving heat between fluids.'),
    ('LMTD', 'Log-mean temperature difference.'), ('Lumped capacitance', 'Uniform-temperature transient model.'), ('Nusselt number', 'Dimensionless convection coefficient.'), ('Prandtl number', 'Momentum over thermal diffusivity.'),
    ('Radiation shield', 'Low-emissivity barrier.'), ('Rayleigh number', 'Buoyancy-flow strength.'), ('Thermal resistance', 'Temperature difference per heat flow.'), ('View factor', 'Fraction of radiation one surface intercepts.')])
RUBRIC = [('4 · Mastery', 'Draws the system and resistance network, checks dimensionless numbers before choosing a correlation, uses kelvin for radiation, and explains results in plain words.'),
          ('3 · Proficient', 'Solves the practice and exam sets with minor slips and checks units.'),
          ('2 · Developing', 'Follows worked examples but mixes up k of the solid and fluid, or uses °C in σT⁴.'),
          ('1 · Beginning', 'Plugs numbers into formulas without a sketch or energy balance; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    sig = 5.670374419e-8; g0 = 9.80665
    wall = lambda L: 1 / 8 + L / .04 + .1 / .7 + 1 / 25
    m = sqrt(4 * 50 / (200 * .005)); eta = lambda L: tanh(m * L) / (m * L)
    tau = 2700 * 900 * (.01 / 6) / 50
    Re = lambda V: V * .5 / 1.5e-5
    hp = lambda V: .664 * Re(V) ** .5 * .71 ** (1 / 3) * .026 / .5
    lm = lambda a, b: (a - b) / log(a / b)
    Ra = g0 * (1 / 300) * 30 * .3 ** 3 / (1.6e-5 * 2.2e-5); hn = .59 * Ra ** .25 * .026 / .3
    pp = lambda T1, T2, e1, e2: sig * (T1 ** 4 - T2 ** 4) / (1 / e1 + 1 / e2 - 1)
    sh = sig * (400 ** 4 - 300 ** 4) / (2 * (1 / .8 + 1 / .05 - 1))
    Te = lambda a: (1360 * (1 - a) / (4 * sig)) ** .25
    Rc = log(2) / (2 * pi * .04); Af = pi * .005 * .02
    nu = lambda Re_, Pr: .023 * Re_ ** .8 * Pr ** .4
    r = [
     ('u1 cond', 1.4 * 10 * 15 / .2, 1050), ('u1 rad', .9 * sig * (400 ** 4 - 300 ** 4), 893), ('u1 refl', .29 * 340, 98.6), ('u1 abs', 340 - .29 * 340, 241.4), ('u1 p1', .04 * 10 * 15 / .2, 30),
     ('u1 p2', 25 * 2 * 40, 2000), ('u1 avg', 1360 / 4, 340), ('u1 d', 400 ** 4 - 300 ** 4, 1.75e10), ('u1 sh', .23 + .48, .71), ('u1 tot', .29 + .23 + .48, 1),
     ('u2 R', wall(.1), 2.808), ('u2 q', 20 / wall(.1), 7.12), ('u2 Q', 100 * 20 / wall(.1), 712), ('u2 R0', wall(0), .3079), ('u2 q0', 20 / wall(0), 64.97), ('u2 x', wall(.1) / wall(0), 9.1),
     ('u2 sav', 1 - wall(0) / wall(.1), .89), ('u2 R2', wall(.2), 5.308), ('u2 q2', 20 / wall(.2), 3.77), ('u2 ins', .1 / .04, 2.5), ('u2 brick', .1 / .7, .1429), ('u2 hi', 1 / 8, .125), ('u2 ho', 1 / 25, .04),
     ('u3 R', Rc, 2.758), ('u3 q', 100 / Rc, 36.3), ('u3 m', m, 14.14), ('u3 mL', m * .02, .2828), ('u3 eta', eta(.02), .974), ('u3 Af', Af, 3.142e-4), ('u3 qf', eta(.02) * 50 * Af * 50, .765),
     ('u3 rcr', .04 / 8, .005), ('u3 eta40', eta(.04), .905), ('u3 mL40', m * .04, .566),
     ('u4 Lc', .01 / 6, 1.667e-3), ('u4 Bi', 50 * (.01 / 6) / 237, 3.52e-4), ('u4 tau', tau, 81), ('u4 t', tau * log(280 / 30), 181), ('u4 ln', log(280 / 30), 2.234), ('u4 e', exp(-1), .368),
     ('u4 half', tau * log(2), 56.1), ('u4 tau2', tau / 2, 40.5),
     ('u5 Re', Re(5), 166667), ('u5 sq', Re(5) ** .5, 408.2), ('u5 Pr', .71 ** (1 / 3), .892), ('u5 Nu', .664 * Re(5) ** .5 * .71 ** (1 / 3), 241.8), ('u5 h', hp(5), 12.6), ('u5 q', 12.58 * .5 * 30, 189),
     ('u5 h10', hp(10), 17.8), ('u5 Re10', Re(10), 333333), ('u5 Re1', Re(1), 33333), ('u5 r', hp(10) / hp(5), sqrt(2)),
     ('u6 Nu', nu(2e4, 7), 138.2), ('u6 h', nu(2e4, 7) * .6 / .02, 4150), ('u6 lm', lm(50, 30), 39.15), ('u6 q', 500 * 2 * lm(50, 30), 39200), ('u6 eps', 1 - exp(-2), .865), ('u6 Nu7', nu(2e4, .7), 55.0),
     ('u6 d1', 90 - 40, 50), ('u6 d2', 50 - 20, 30),
     ('u7 Ra', Ra, 7.52e7), ('u7 Nu', .59 * Ra ** .25, 54.9), ('u7 h', hn, 4.76), ('u7 q', hn * .3 * 30, 42.9), ('u7 r', hp(5) / hn, 2.64), ('u7 b', 1 / 300, 3.33e-3), ('u7 ev', .25 * 340, 85), ('u7 cv', .05 * 340, 17),
     ('u8 sun', 2898 / 5800, .5), ('u8 Te', (240 / sig) ** .25, 255.1), ('u8 TeC', (240 / sig) ** .25 - 273.15, -18), ('u8 E288', sig * 288 ** 4, 390), ('u8 w288', 2898 / 288, 10.06), ('u8 16', 2 ** 4, 16),
     ('u8 lamp', 2898 / 3000, .966),
     ('u9 q', pp(400, 300, .8, .8), 662), ('u9 den', 1 / .8 + 1 / .8 - 1, 1.5), ('u9 sh', sh, 24.5), ('u9 R', 2 * (1 / .8 + 1 / .05 - 1), 40.5), ('u9 x', pp(400, 300, .8, .8) / sh, 27), ('u9 F21', 1 * 1 / 4, .25),
     ('u9 PSP', sig * (1377 + 273.15) ** 4, 4.20e5), ('u9 in', 4.5 * 2.54, 11.43), ('u9 F', (2500 - 32) / 1.8, 1371), ('u9 cm', 11.43 / 2.54, 4.5), ('u9 add', 1 / .05 - 1 + 1 / .05 - 1 + 1, 39),
     ('u10 W', 9 / 3, 3), ('u10 C', 308 / (308 - 273), 8.8), ('u10 P', .8 * 5.1e14, 4.1e14), ('u10 half', 1900 / 2, 950), ('u10 C2', 308 / (308 - 263), 6.84), ('u10 third', 8.8 / 3, 2.93),
     ('labA 0', wall(0), .3079), ('labA q0', 20 / wall(0), 64.96), ('labA 5', wall(.05), 1.558), ('labA q5', 20 / wall(.05), 12.84), ('labA 10', wall(.1), 2.808), ('labA q10', 20 / wall(.1), 7.12),
     ('labA 20', wall(.2), 5.308), ('labA q20', 20 / wall(.2), 3.77),
     ('labB m1', m * .01, .1414), ('labB e1', eta(.01), .993), ('labB m2', m * .02, .2828), ('labB e2', eta(.02), .974), ('labB m4', m * .04, .5657), ('labB e4', eta(.04), .905), ('labB m', m, 14.14),
     ('labC 81', 20 + 280 * exp(-1), 123.0), ('labC 162', 20 + 280 * exp(-2), 57.9), ('labC 243', 20 + 280 * exp(-3), 33.9), ('labC 0', 20 + 280, 300),
     ('labD R1', Re(1), 33333), ('labD h1', hp(1), 5.62), ('labD R5', Re(5), 166667), ('labD h5', hp(5), 12.58), ('labD R10', Re(10), 333333), ('labD h10', hp(10), 17.78), ('labD sq', Re(10) ** .5, 577.4),
     ('labE 288', 2898 / 288, 10.06), ('labE 3000', 2898 / 3000, .966), ('labE 5800', 2898 / 5800, .5), ('labE E288', sig * 288 ** 4, 390), ('labE E3000', sig * 3000 ** 4, 4.59e6), ('labE E5800', sig * 5800 ** 4, 6.42e7),
     ('labF 25', Te(.25), 259.0), ('labF 29', Te(.29), 255.4), ('labF 35', Te(.35), 249.9), ('labF C', Te(.29) - 273.15, -17.7),
     ('mid conv', 15 * 3 * 20, 900), ('mid R', wall(.15), 4.058), ('mid q', 20 / wall(.15), 4.93), ('mid rcr', .1 / 10, .01), ('mid tau', 2700 * 900 * (.02 / 6) / 50, 162), ('mid Re', Re(2), 66667),
     ('fin lm', lm(60, 20), 36.4), ('fin eps', 1 - exp(-1), .632), ('fin Ra', Ra * 8, 6.02e8), ('fin wien', 2898 / 1000, 2.9), ('fin pp', pp(500, 300, .9, .9), 2524), ('fin C', 318 / 50, 6.36),
     ('c sig', sig, 5.670374419e-8), ('c g', g0, 9.80665), ('c w', 2898, 2898), ('c k', .026, .026), ('c AE', 4 * pi * 6.371e6 ** 2, 5.1e14), ('c Al', 237, 237),
     ('x EB 240', 340 * .71, 241.4), ('x EB ir', 117 - 100, 17), ('x EB s', .25 + .05 + .17, .47), ('x EB 15', 15 + 273.15, 288.15), ('x EB 30', 288.15 - 30, 258.15), ('x PSP v', 430000 * 1.609344, 692000),
     ('x PSP yr', 24 / 7, 3.43), ('x PSP kg', 685, 685), ('x ES 3', 3, 3), ('x u2 9', 64.97 / 7.12, 9.1), ('x u3 l', 2 * pi * .04, .2513), ('x u5 ratio', 17.78 / 5.62, 3.16), ('x u6 n', 1 - exp(-3), .95),
     ('x u7 Pr', 1.6e-5 / 2.2e-5, .727), ('x u8 4', (2 * 288) ** 4 / 288 ** 4, 16), ('x u9 r', 662 / 24.5, 27), ('x u10 r', 8.8 / 6.84, 1.287), ('x labC r', 123.0 - 20, 103), ('x labF d', 259.0 - 249.9, 9.1),
     ('y u1 h', 2000 / 80, 25), ('y u2 U', 1 / wall(.1), .356), ('y u3 T', 36.26 * Rc, 100), ('y u4 c', 2700 * 900, 2.43e6), ('y u5 L', 241.8 * .026, 6.29), ('y u6 C', 39150 / 1000, 39.15),
     ('y u7 Gr', Ra / (1.6e-5 / 2.2e-5), 1.034e8), ('y u8 r', 5800 / 288, 20.1), ('y u9 e', .8 * .8, .64), ('y u10 kW', 3 * 3, 9), ('y labB d', eta(.01) - eta(.04), .088), ('y mid d', 7.12 - 4.93, 2.19)]
    return r
