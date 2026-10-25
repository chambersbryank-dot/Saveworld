"""Fluid Mechanics (ENGR 330): fluid properties, statics and buoyancy, Bernoulli and the energy equation, integral momentum, differential analysis and exact viscous flows, dimensional analysis and similitude, pipe flow, pumps and pump systems, external flow and drag, and open-channel flow.
Oct 25 2026, founder-approved four-year track, junior course 3. Same module fields as thermo.py / aero1.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, log10, cos, radians
ID = 'fluids'
STATUS = 'live'
YEAR = 3
PAGE = 'Fluid_Mechanics.html'
CODE = 'ENGR 330'
TITLE = 'Fluid Mechanics'
LAB_NAME = 'Fluid mechanics lab'
TAGLINE = 'How liquids and gases flow: fluid properties and viscosity, pressure and buoyancy, Bernoulli and the energy equation with head, momentum on jets, vanes and turbines, the Navier–Stokes equations and exact flows, dimensional analysis and model testing, pipe friction and losses, pumps and system curves, drag on bodies, and open-channel flow, with six labs. Free, self-paced, and tied to hydropower, pumped storage, marine energy, water leaks, ocean currents and wind turbines.'
DESC = 'Free self-study Fluid Mechanics: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and home labs, practice exams, tied to hydropower, pumped storage and saving water.'
ALT = 'Illustration of the SWOT satellite measuring Earth’s surface water'
_O = 'https://openstax.org/books/university-physics-volume-1/pages/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_G = 'https://www.grc.nasa.gov/www/k-12/airplane/'
_MIT = ('MIT OpenCourseWare 2.06 Fluid Dynamics (Spring 2013)', 'https://ocw.mit.edu/courses/2-06-fluid-dynamics-spring-2013/')
_MITC = ('MIT OpenCourseWare 1.060 Engineering Mechanics II (Spring 2006)', 'https://ocw.mit.edu/courses/1-060-engineering-mechanics-ii-spring-2006/')
_MIT25 = ('MIT OpenCourseWare 2.25 Advanced Fluid Mechanics (Fall 2013)', 'https://ocw.mit.edu/courses/2-25-advanced-fluid-mechanics-fall-2013/')
_HYD = ('U.S. DOE: How hydropower works', 'https://www.energy.gov/eere/water/how-hydropower-works')
_TYP = ('U.S. DOE: Types of hydropower plants', 'https://www.energy.gov/eere/water/types-hydropower-plants')
_PSH = ('U.S. DOE: Pumped storage hydropower', 'https://www.energy.gov/eere/water/pumped-storage-hydropower')
_MAR = ('U.S. DOE: Marine energy basics', 'https://www.energy.gov/eere/water/marine-energy-basics')
_LEAK = ('U.S. EPA WaterSense: Fix a Leak Week', 'https://www.epa.gov/watersense/fix-leak-week')
_PUMP = ('U.S. DOE: Pump systems', 'https://www.energy.gov/eere/iedo/pump-systems')
_THC = ('NOAA National Ocean Service: Thermohaline circulation', 'https://oceanservice.noaa.gov/education/tutorial_currents/05conveyor1.html')
_WIND = ('U.S. DOE: How do wind turbines work?', 'https://www.energy.gov/eere/wind/how-do-wind-turbines-work')
BANNER = ['images/SWOT_Orbit_Illustration.jpg', 'images/ISS_Over_Ganges_STS102.jpg', 'images/GRACE_FO_Orbit.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg']
CREDITS = {'images/SWOT_Orbit_Illustration.jpg': 'CNES (PIA25623)', 'images/ISS_Over_Ganges_STS102.jpg': 'NASA (STS102-357-031, March 18, 2001)',
           'images/GRACE_FO_Orbit.jpg': 'NASA/JPL-Caltech (PIA22431)', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester junior fluid mechanics course. It is modeled on the topics and depth of MIT 2.06 Fluid Dynamics and MIT 1.060 Engineering Mechanics II (both free on MIT OpenCourseWare), and on courses such as Purdue ME 309 and Georgia Tech CEE 3040, using the free OpenStax University Physics fluids chapter and PhET simulations, which we link where they help. None of those authors or schools endorses this page.',
         'What we add: every unit ties to real work with a cited public source (hydropower, pumped storage, marine energy, household water leaks, ocean circulation and wind turbines), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a safe home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Moving water and air carries most of the world’s renewable energy: rivers through hydropower turbines, wind across turbine blades, tides and waves into marine energy devices. Fluid mechanics also decides how much energy it takes to pump water to cities and farms, and how much is lost to leaks and friction.',
                 'Ocean currents move heat around the planet and shape the climate. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values.']
PREREQS = ['Calculus III: partial derivatives, divergence and multiple integrals.', 'Differential Equations: first- and second-order ODEs.',
           'Statics and Dynamics: free-body diagrams, Newton’s laws and momentum.', 'Thermodynamics helps with the energy equation but is not required.']
STUDY = ['Start every problem with a sketch: control volume, streamline, or free-body diagram of the fluid.', 'Write the governing equation in words first (mass, momentum or energy), then cancel terms you can justify.',
         'Work in heads (metres of fluid) for liquid systems; they make pumps, pipes and turbines easy to compare.', 'Compute the Reynolds number before choosing a friction or drag correlation.',
         'Check units and limits: zero flow means zero loss; doubling speed roughly quadruples turbulent losses.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Density, Buoyancy, Under Pressure and Fluid Pressure and Flow simulations.', 'A clear plastic bottle, a nail or skewer, a ruler and tape.',
            'A kitchen scale, a measuring jug, a bucket and a stopwatch.', 'A garden hose or a sink tap.', 'Spreadsheet software for the pipe and pump labs.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab can be done in a free simulation or with kitchen and garden items. Work over a sink or outdoors, wipe up spills at once to avoid slips, use cold tap water only, and keep water away from electrical outlets and devices.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('Water at 20 °C (textbook values)', 'ρ = 998 kg/m³, μ = 1.002 × 10⁻³ kg/(m·s), ν = 1.004 × 10⁻⁶ m²/s, surface tension σ = 0.0728 N/m'), ('Air at 15 °C (textbook values)', 'ρ = 1.225 kg/m³, μ = 1.789 × 10⁻⁵ kg/(m·s)'),
             ('Seawater and ice (textbook values)', 'ρ_sea = 1025 kg/m³, ρ_ice = 917 kg/m³'), ('Mercury (textbook value)', 'ρ = 13,600 kg/m³'), ('Gravity', 'g = 9.81 m/s²'), ('1 U.S. gallon', '3.785 L')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, textbook sections and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT lecture notes and problem sets.'), (_MITC[0], _MITC[1], 'Free MIT civil-engineering fluids course.'), (_MIT25[0], _MIT25[1], 'Deeper MIT treatment.'),
          ('OpenStax University Physics Volume 1, Chapter 14: Fluid mechanics', _O + '14-1-fluids-density-and-pressure', 'Free textbook chapter.'), ('PhET: Fluid Pressure and Flow', _PH + 'fluid-pressure-and-flow', 'Pressure and flow interactively.'),
          ('PhET: Buoyancy', _PH + 'buoyancy', 'Buoyancy interactively.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Fluid Properties: Density, Viscosity and Surface Tension', 'weeks': 'Week 1',
 'summary': 'What makes a fluid, the continuum assumption, density and specific gravity, pressure, viscosity and Newton’s law of viscosity, kinematic viscosity, non-Newtonian fluids, surface tension and capillary rise, and vapor pressure and cavitation.',
 'objectives': ['Define a fluid and use the continuum assumption.', 'Use Newton’s law of viscosity to find shear stress.', 'Compute capillary rise from surface tension.', 'Explain how density differences drive flows.'],
 'concepts': ['A fluid deforms continuously under any shear stress, however small. Treating it as a continuum lets us define density, velocity and pressure at every point.',
              'Density ρ (kg/m³) and specific gravity SG = ρ/ρ_water. Water at 20 °C has ρ = 998 kg/m³; air at 15 °C has 1.225 kg/m³.',
              'Newton’s law of viscosity: shear stress τ = μ du/dy. Dynamic viscosity μ measures resistance to shearing; kinematic viscosity ν = μ/ρ. Water is about 56 times more viscous than air but has about 15 times lower ν.',
              'Non-Newtonian fluids (paint, blood, toothpaste) have a viscosity that changes with shear rate.',
              'Surface tension σ pulls liquid surfaces tight; in a thin tube water rises h = 4σ cos θ/(ρgD). If local pressure drops to the vapor pressure, the liquid boils: cavitation, which damages pumps and propellers.'],
 'eqs': [('\\tau=\\mu\\frac{du}{dy}', 'Newton’s law of viscosity'), ('\\nu=\\frac{\\mu}{\\rho}', 'Kinematic viscosity'), ('SG=\\frac{\\rho}{\\rho_{water}}', 'Specific gravity'), ('h=\\frac{4\\sigma\\cos\\theta}{\\rho gD}', 'Capillary rise')],
 'worked': [
  {'q': 'Water (μ = 1.002 × 10⁻³ kg/(m·s)) fills a 1 mm gap between a fixed plate and one moving at 2 m/s. Find the shear stress.', 'steps': ['du/dy = 2/0.001 = 2000 s⁻¹.', 'τ = 1.002 × 10⁻³ × 2000.'], 'a': 'τ = 2.00 Pa.'},
  {'q': 'Find the capillary rise of water (σ = 0.0728 N/m, θ = 0) in a 1 mm glass tube.', 'steps': ['h = 4 × 0.0728/(998 × 9.81 × 0.001).'], 'a': 'h = 29.7 mm.'},
  {'q': 'Find ν for water at 20 °C.', 'steps': ['ν = 1.002 × 10⁻³/998.'], 'a': 'ν = 1.004 × 10⁻⁶ m²/s.'}],
 'practice': [('Find the SG of seawater (1025 kg/m³).', '1025/998 = 1.027.'), ('Find the capillary rise in a 0.5 mm tube.', 'Twice as much: 59.5 mm.'),
              ('Find μ_water/μ_air.', '1.002 × 10⁻³/1.789 × 10⁻⁵ = 56.0.'), ('What fraction of an iceberg floats below seawater?', '917/1025 = 89.5%.')],
 'misc': [('Viscosity and density are the same thing.', 'Honey is viscous; mercury is dense but not very viscous.'), ('Fluids resist shear like solids.', 'They flow under any shear stress.'),
          ('Cavitation needs high temperature.', 'Low pressure is enough.')],
 'quiz': [{'q': 'Shear stress in a Newtonian fluid is…', 'opts': ['μ du/dy', 'ρgh', 'ρV²', 'σ/D'], 'ok': 0, 'why': 'Newton’s law of viscosity.'},
          {'q': 'Kinematic viscosity is…', 'opts': ['μρ', 'μ/ρ', 'ρ/μ', 'τ/μ'], 'ok': 1, 'why': 'ν = μ/ρ.'},
          {'q': 'Capillary rise grows when the tube is…', 'opts': ['wider', 'narrower', 'longer', 'heavier'], 'ok': 1, 'why': 'h ∝ 1/D.'},
          {'q': 'Cavitation occurs when pressure drops to…', 'opts': ['zero gauge', 'the vapor pressure', 'atmospheric', 'stagnation'], 'ok': 1, 'why': 'Local boiling.'}],
 'cards': [('Fluid', 'Deforms continuously under shear.'), ('Viscosity', 'τ = μ du/dy.'), ('Kinematic viscosity', 'ν = μ/ρ.'), ('Specific gravity', 'ρ/ρ_water.'), ('Capillary rise', '4σ cos θ/(ρgD).'), ('Cavitation', 'Boiling at low pressure.')],
 'planet': {'text': ['NOAA explains that winds drive ocean currents in the upper 100 meters, but deep-ocean currents thousands of meters down are driven by differences in water density, controlled by temperature and salinity: thermohaline circulation.',
                     'In polar regions, sea ice forms and leaves salt behind, so the surrounding water becomes saltier and denser and sinks; surface water flows in to replace it, starting the global conveyor belt. Density, the first property in this unit, moves heat around the whole planet.'],
            'site': [('Oceans', 'Oceans.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_THC]},
 'res': [('OpenStax UP1, 14.1 Fluids, density and pressure', _O + '14-1-fluids-density-and-pressure', 'Free textbook section.'), ('OpenStax UP1, 14.7 Viscosity and turbulence', _O + '14-7-viscosity-and-turbulence', 'Free textbook section.'),
         (_MIT[0], _MIT[1], 'MIT fluid properties notes.'), ('PhET: Density', _PH + 'density', 'Density interactively.')]})
UNITS.append(
{'id': 'u2', 'title': 'Fluid Statics, Manometers and Buoyancy', 'weeks': 'Weeks 2–3',
 'summary': 'Pressure at a point, the hydrostatic equation, gauge and absolute pressure, manometers, hydrostatic forces on plane submerged surfaces and the center of pressure, forces on curved surfaces, Archimedes’ principle, and stability of floating bodies.',
 'objectives': ['Compute pressure at depth and read manometers.', 'Find the resultant force and center of pressure on a submerged gate.', 'Apply Archimedes’ principle.', 'Judge whether a floating body is stable.'],
 'concepts': ['Pressure at a point acts equally in all directions. In a static fluid dp/dz = −ρg, so with constant density p = p₀ + ρgh at depth h. Gauge pressure is measured relative to the atmosphere.',
              'Manometers balance columns of fluid: move through the tube adding ρgh going down and subtracting going up.',
              'On a plane surface the resultant force is F = ρg h_c A (h_c = depth of the centroid). It acts at the center of pressure, below the centroid: y_cp = y_c + I_xc/(y_c A).',
              'On curved surfaces, find the horizontal component as the force on the vertical projection and the vertical component as the weight of fluid above.',
              'Archimedes: the buoyant force equals the weight of displaced fluid, F_B = ρ_fluid g V_displaced. A floating body is stable if its metacenter lies above its center of gravity.'],
 'eqs': [('p=p_0+\\rho gh', 'Hydrostatic pressure'), ('F=\\rho g h_cA', 'Force on a plane surface'), ('y_{cp}=y_c+\\frac{I_{xc}}{y_cA}', 'Center of pressure'), ('F_B=\\rho_f gV_{disp}', 'Buoyant force')],
 'worked': [
  {'q': 'Find the gauge pressure 10 m below the surface of fresh water (ρ = 998 kg/m³).', 'steps': ['p = 998 × 9.81 × 10.'], 'a': 'p = 97.9 kPa (about one atmosphere).'},
  {'q': 'A vertical rectangular gate 2 m wide and 3 m tall has its top edge at the water surface. Find the force and the depth of the center of pressure.', 'steps': ['h_c = 1.5 m; A = 6 m².', 'F = 998 × 9.81 × 1.5 × 6 = 88.1 kN.', 'I_xc = 2 × 3³/12 = 4.5 m⁴; y_cp = 1.5 + 4.5/(1.5 × 6).'], 'a': 'F = 88.1 kN acting 2.0 m below the surface (two-thirds of the depth).'},
  {'q': 'A mercury manometer (ρ = 13,600 kg/m³) connected across a water pipe shows a 0.1 m difference. Find the pressure difference.', 'steps': ['Δp = (13,600 − 1000) × 9.81 × 0.1 (water above the mercury, ρ_water ≈ 1000 kg/m³).'], 'a': 'Δp = 12.4 kPa.'}],
 'practice': [('Find the buoyant force on a fully submerged 2 L object in water (ρ ≈ 1000 kg/m³).', '1000 × 9.81 × 0.002 = 19.6 N.'), ('What is the absolute pressure 10 m down if p_atm = 101.3 kPa?', '199.2 kPa.'),
              ('Does the force on a dam depend on how long the reservoir is?', 'No; only depth and wall area.'), ('Why is the center of pressure below the centroid?', 'Pressure grows with depth.')],
 'misc': [('Pressure depends on container shape.', 'Only on depth (the hydrostatic paradox).'), ('Buoyancy depends on the object’s weight.', 'It depends on displaced volume.'),
          ('The force on a gate acts at its center.', 'It acts at the center of pressure, lower down.')],
 'quiz': [{'q': 'Pressure at depth h is…', 'opts': ['ρgh', 'ρV²/2', 'μ du/dy', 'mg/A'], 'ok': 0, 'why': 'Hydrostatics (gauge).'},
          {'q': 'Buoyant force equals…', 'opts': ['object weight', 'displaced fluid weight', 'object mass', 'zero'], 'ok': 1, 'why': 'Archimedes.'},
          {'q': 'For a vertical gate from the surface, the center of pressure is at…', 'opts': ['half depth', 'two-thirds depth', 'the surface', 'the bottom'], 'ok': 1, 'why': 'Triangular load.'},
          {'q': 'A floating body is stable if…', 'opts': ['G above M', 'M above G', 'B = G', 'it is heavy'], 'ok': 1, 'why': 'Metacenter.'}],
 'cards': [('Hydrostatic', 'p = p₀ + ρgh.'), ('Gauge pressure', 'Relative to atmosphere.'), ('Plane force', 'ρg h_c A.'), ('Center of pressure', 'y_c + I/(y_c A).'), ('Archimedes', 'F_B = ρgV.'), ('Stability', 'Metacenter above G.')],
 'planet': {'text': ['DOE notes that the United States has more than 90,000 dams, and that less than 3% of them produce power; the rest serve recreation, farm ponds, flood control, water supply and irrigation. Every one of them is designed with this unit’s equations: the water load on a dam grows with the square of the depth and acts low on the wall.',
                     'DOE describes the most common hydropower plant, an impoundment facility, as a dam that stores river water in a reservoir; water released through a turbine spins a generator, and releases can also serve flood control, recreation, fish passage and water quality. The stored water’s pressure on the dam and its head at the turbine both come straight from p = ρgh.'],
            'site': [('Statics', 'Statics.html'), ('Oceans', 'Oceans.html')],
            'src': [_TYP]},
 'res': [('OpenStax UP1, 14.2 Measuring pressure', _O + '14-2-measuring-pressure', 'Free textbook section.'), ('OpenStax UP1, 14.4 Archimedes’ principle and buoyancy', _O + '14-4-archimedes-principle-and-buoyancy', 'Free textbook section.'),
         ('PhET: Under Pressure', _PH + 'under-pressure', 'Hydrostatics interactively.'), ('PhET: Buoyancy', _PH + 'buoyancy', 'Buoyancy interactively.')]})
UNITS.append(
{'id': 'u3', 'title': 'Bernoulli, Heads and the Energy Equation', 'weeks': 'Week 4',
 'summary': 'Streamlines and flow visualization, continuity Q = AV, Bernoulli’s equation and its limits, pressure, velocity and elevation heads, the energy grade line, Torricelli’s law, the steady-flow energy equation with pump, turbine and loss heads, and hydropower output.',
 'objectives': ['Apply continuity and Bernoulli along a streamline.', 'Work in heads: pressure, velocity and elevation.', 'Use the energy equation with pump, turbine and loss heads.', 'Compute hydropower and pumping power.'],
 'concepts': ['For incompressible steady flow, volume flow Q = AV is the same at every section of a pipe (continuity).',
              'Bernoulli along a streamline (steady, inviscid, incompressible): p/(ρg) + V²/(2g) + z = constant. Each term is a head in metres.',
              'Torricelli: a jet leaving a tank at depth h has speed V = √(2gh).',
              'Real systems add pumps and turbines and lose energy to friction: p₁/(ρg) + V₁²/(2g) + z₁ + h_pump = p₂/(ρg) + V₂²/(2g) + z₂ + h_turbine + h_L.',
              'Power from a head: P = ρgQH. Turbines deliver P = ηρgQH; pumps need P = ρgQH/η. DOE notes that hydropower output depends on flow and head.'],
 'eqs': [('Q=A_1V_1=A_2V_2', 'Continuity'), ('\\frac{p}{\\rho g}+\\frac{V^2}{2g}+z=\\text{const}', 'Bernoulli in heads'), ('V=\\sqrt{2gh}', 'Torricelli'), ('P=\\eta\\rho gQH', 'Hydropower')],
 'worked': [
  {'q': 'Find the jet speed from a hole 5 m below a tank’s surface.', 'steps': ['V = √(2 × 9.81 × 5).'], 'a': 'V = 9.90 m/s.'},
  {'q': 'A hydropower plant has Q = 50 m³/s, head H = 100 m and overall efficiency 0.9 (sample values; ρ = 1000 kg/m³). Find the power.', 'steps': ['P = 0.9 × 1000 × 9.81 × 50 × 100.'], 'a': 'P = 44.1 MW, a “large” plant by DOE’s 30 MW definition.'},
  {'q': 'A pump lifts 0.05 m³/s of water 20 m with 5 m of pipe losses at 75% efficiency. Find the power input.', 'steps': ['h_pump = 20 + 5 = 25 m.', 'P = 1000 × 9.81 × 0.05 × 25/0.75.'], 'a': 'P = 16.4 kW.'}],
 'practice': [('A hose carries 0.4 L/s through a 20 mm bore into a 10 mm nozzle. Find both speeds.', '1.27 m/s and 5.09 m/s.'), ('Convert 200 kPa to metres of water head.', '200,000/(1000 × 9.81) = 20.4 m.'),
              ('Double the head of a hydropower plant at the same Q. Power?', 'Doubles.'), ('Why does a pitot tube read higher than a static tap?', 'It adds the velocity head.')],
 'misc': [('Bernoulli applies across a pump.', 'Use the energy equation with h_pump.'), ('Faster flow means higher pressure.', 'Along a streamline, faster means lower static pressure.'),
          ('Head is a pressure.', 'It is energy per unit weight, in metres.')],
 'quiz': [{'q': 'Velocity head is…', 'opts': ['V²/(2g)', 'p/ρg', 'z', 'ρV²'], 'ok': 0, 'why': 'Kinetic energy per unit weight.'},
          {'q': 'Halving pipe area doubles…', 'opts': ['pressure', 'velocity', 'flow rate', 'head loss'], 'ok': 1, 'why': 'Continuity.'},
          {'q': 'Hydropower is proportional to…', 'opts': ['Q only', 'H only', 'Q × H', 'Q/H'], 'ok': 2, 'why': 'P = ηρgQH.'},
          {'q': 'Torricelli’s jet speed is…', 'opts': ['gh', '√(2gh)', '2gh', '√(gh)'], 'ok': 1, 'why': 'Bernoulli tank-to-jet.'}],
 'cards': [('Continuity', 'Q = AV.'), ('Bernoulli', 'p/ρg + V²/2g + z = const.'), ('Torricelli', 'V = √(2gh).'), ('Energy equation', 'Adds h_pump, h_turbine, h_L.'), ('Hydropower', 'P = ηρgQH.'), ('Pump power', 'ρgQH/η.')],
 'planet': {'text': ['DOE explains that hydropower is powered by the kinetic energy of flowing water, and that the energy available depends on both the volume of flow and the change in elevation, the head: the greater the flow and the higher the head, the more electricity can be generated. Water flows through a penstock and spins a turbine connected to a generator.',
                     'DOE classes plants by size: large hydropower above 30 MW, small hydropower from 100 kW to 10 MW, and micro hydropower up to 100 kW, enough for a single home, farm or village. P = ηρgQH lets you size any of them from a flow measurement and a survey of the drop.'],
            'site': [('Solutions', 'Solutions.html'), ('Thermodynamics', 'Thermodynamics.html')],
            'src': [_HYD, _TYP]},
 'res': [('OpenStax UP1, 14.5 Fluid dynamics', _O + '14-5-fluid-dynamics', 'Free textbook section.'), ('OpenStax UP1, 14.6 Bernoulli’s equation', _O + '14-6-bernoullis-equation', 'Free textbook section.'),
         ('PhET: Fluid Pressure and Flow', _PH + 'fluid-pressure-and-flow', 'Bernoulli interactively.'), (_MITC[0], _MITC[1], 'Energy equation notes.')]})
UNITS.append(
{'id': 'u4', 'title': 'Integral Momentum: Jets, Vanes, Bends and Turbines', 'weeks': 'Week 5',
 'summary': 'Reynolds transport theorem, the linear momentum equation for control volumes, forces of jets on plates and vanes, forces on pipe bends and nozzles, moving control volumes, impulse turbines (Pelton wheels), and the angular momentum equation for turbomachines.',
 'objectives': ['State the Reynolds transport theorem.', 'Apply the momentum equation to jets and vanes.', 'Analyze a moving vane and a Pelton wheel.', 'Use angular momentum for turbine and pump torque.'],
 'concepts': ['Reynolds transport theorem: the rate of change of a property of a fluid system = rate of change inside a control volume + net outflow across its surface.',
              'Steady linear momentum: ΣF = Σṁ_out V_out − Σṁ_in V_in (vectors). Include pressure forces on cut sections and the support force.',
              'A jet of speed V and flow Q hitting a flat plate head-on exerts F = ρQV. A vane turning the jet through angle θ exerts F = ρQV(1 − cos θ) along the jet.',
              'For a vane moving at speed U, use the relative speed (V − U). A Pelton wheel’s buckets turn the jet nearly 180°; power F·U is largest at U = V/2.',
              'Angular momentum: torque = ṁ(r₂V_θ2 − r₁V_θ1) (Euler turbomachine equation), the basis of pump and turbine design.'],
 'eqs': [('\\sum\\mathbf F=\\sum\\dot m\\mathbf V_{out}-\\sum\\dot m\\mathbf V_{in}', 'Steady momentum'), ('F=\\rho QV(1-\\cos\\theta)', 'Force of a turned jet'), ('F=\\rho Q(V-U)(1-\\cos\\beta)', 'Moving vane'), ('T=\\dot m(r_2V_{\\theta2}-r_1V_{\\theta1})', 'Euler turbomachine equation')],
 'worked': [
  {'q': 'A 50 mm water jet at 20 m/s hits a flat plate head-on. Find the force.', 'steps': ['A = π × 0.05²/4 = 1.963 × 10⁻³ m².', 'F = ρAV² = 1000 × 1.963 × 10⁻³ × 400.'], 'a': 'F = 785 N.'},
  {'q': 'The same jet is turned 120° by a fixed vane. Find the force along the jet.', 'steps': ['F = ρAV²(1 − cos 120°) = 785 × 1.5.'], 'a': 'F = 1178 N.'},
  {'q': 'A Pelton bucket moving at 15 m/s receives a 0.01 m³/s jet at 30 m/s and turns it 165°. Find the force and power.', 'steps': ['F = 1000 × 0.01 × (30 − 15)(1 − cos 165°) = 294.9 N.', 'P = F × U.'], 'a': 'F = 294.9 N; P = 4.42 kW (the jet carries ½ρQV² = 4.5 kW).'}],
 'practice': [('At what bucket speed does a Pelton wheel give the most power?', 'Half the jet speed.'), ('Double jet speed at the same area. Force on a plate?', '4 times.'),
              ('Name the forces in a pipe-bend momentum balance.', 'Inlet and outlet pressure forces, weight, and the support force.'), ('Why are Pelton buckets split in the middle?', 'To turn the jet nearly 180° without it hitting the next bucket.')],
 'misc': [('The plate force depends on the plate size.', 'For a jet fully deflected, only on ρQV.'), ('A moving vane sees the full jet speed.', 'It sees V − U.'),
          ('Momentum is a scalar.', 'It is a vector; resolve components.')],
 'quiz': [{'q': 'Force of a jet on a flat plate is…', 'opts': ['ρQV', 'ρgQH', '½ρV²', 'QV'], 'ok': 0, 'why': 'Momentum flux.'},
          {'q': 'Turning a jet 180° gives a force of…', 'opts': ['ρQV', '2ρQV', '0', 'ρQV/2'], 'ok': 1, 'why': '1 − cos 180° = 2.'},
          {'q': 'Pelton wheel best U/V is…', 'opts': ['0.25', '0.5', '1', '2'], 'ok': 1, 'why': 'Maximizes (V − U)U.'},
          {'q': 'The Euler equation gives turbomachine…', 'opts': ['torque', 'drag', 'buoyancy', 'viscosity'], 'ok': 0, 'why': 'Angular momentum.'}],
 'cards': [('RTT', 'System rate = CV rate + net outflow.'), ('Momentum', 'ΣF = Σṁ V_out − Σṁ V_in.'), ('Plate', 'ρQV.'), ('Vane', 'ρQV(1 − cos θ).'), ('Pelton', 'Best at U = V/2.'), ('Euler turbine', 'T = ṁ Δ(rV_θ).')],
 'planet': {'text': ['DOE explains that pumped storage hydropower works like a giant battery: when demand is low it pumps water to an upper reservoir, and when demand is high the water flows back down through a turbine. DOE reports that pumped storage accounts for 88% of all utility-scale energy storage in the United States, at 43 plants, with room to more than double capacity.',
                     'Each pump-turbine is designed with the momentum and angular-momentum equations in this unit: the runner’s blade angles set how much torque the water gives up or receives. Storing solar and wind power this way depends on getting those blades right.'],
            'site': [('Solutions', 'Solutions.html'), ('Dynamics', 'Dynamics.html')],
            'src': [_PSH]},
 'res': [(_MIT[0], _MIT[1], 'Control-volume momentum.'), (_MITC[0], _MITC[1], 'Momentum notes.'), ('NASA Glenn: Conservation of momentum', _G + 'conmo.html', 'Free NASA page.'), (_MIT25[0], _MIT25[1], 'Deeper treatment.')]})
UNITS.append(
{'id': 'u5', 'title': 'Differential Analysis: Continuity, Navier–Stokes and Exact Flows', 'weeks': 'Weeks 6–7',
 'summary': 'Fluid kinematics (velocity field, acceleration, vorticity, strain), the differential continuity equation, the stream function, Euler and Navier–Stokes equations, boundary conditions, and exact laminar solutions: Couette flow, plane Poiseuille flow and Hagen–Poiseuille pipe flow.',
 'objectives': ['Compute the material acceleration of a velocity field.', 'Check continuity and find a stream function.', 'State the Navier–Stokes equations and their boundary conditions.', 'Solve Couette and Hagen–Poiseuille flows.'],
 'concepts': ['In the Eulerian view, acceleration has a local part ∂V/∂t and a convective part (V·∇)V; the sum is the material derivative DV/Dt.',
              'Incompressible continuity: ∇·V = ∂u/∂x + ∂v/∂y + ∂w/∂z = 0. In 2D, a stream function ψ with u = ∂ψ/∂y, v = −∂ψ/∂x satisfies it automatically.',
              'Navier–Stokes (incompressible, Newtonian): ρ DV/Dt = −∇p + ρg + μ∇²V. With no-slip at walls, it governs nearly every flow in this course; only a few cases solve exactly.',
              'Couette flow between a fixed and a moving plate: linear velocity profile, shear τ = μU/h.',
              'Hagen–Poiseuille flow in a pipe: parabolic profile, u_max = 2V_avg, and Q = πR⁴Δp/(8μL). It holds while the flow stays laminar (Re below about 2300).'],
 'eqs': [('\\frac{D\\mathbf V}{Dt}=\\frac{\\partial\\mathbf V}{\\partial t}+(\\mathbf V\\cdot\\nabla)\\mathbf V', 'Material acceleration'), ('\\nabla\\cdot\\mathbf V=0', 'Incompressible continuity'), ('\\rho\\frac{D\\mathbf V}{Dt}=-\\nabla p+\\rho\\mathbf g+\\mu\\nabla^2\\mathbf V', 'Navier–Stokes'), ('Q=\\frac{\\pi R^4\\Delta p}{8\\mu L}', 'Hagen–Poiseuille')],
 'worked': [
  {'q': 'Water flows in a 4 mm diameter tube with Δp/L = 100 Pa/m. Find Q, V_avg, u_max and Re.', 'steps': ['Q = π × 0.002⁴ × 100/(8 × 1.002 × 10⁻³) = 6.27 × 10⁻⁷ m³/s.', 'V = Q/(π × 0.002²) = 0.0499 m/s; u_max = 2V.', 'Re = 998 × 0.0499 × 0.004/1.002 × 10⁻³.'], 'a': 'Q = 6.27 × 10⁻⁷ m³/s, V = 0.0499 m/s, u_max = 0.0998 m/s, Re = 199 (laminar).'},
  {'q': 'A plate moves at 1 m/s over a 2 mm water film. Find the shear stress.', 'steps': ['τ = μU/h = 1.002 × 10⁻³ × 1/0.002.'], 'a': 'τ = 0.501 Pa.'},
  {'q': 'Is V = (2x, −2y) incompressible, and what is its acceleration at (1, 1)?', 'steps': ['∂u/∂x + ∂v/∂y = 2 − 2 = 0.', 'a_x = u ∂u/∂x = 2x × 2 = 4x; a_y = v ∂v/∂y = (−2y)(−2) = 4y.'], 'a': 'Yes; a = (4, 4) m/s².'}],
 'practice': [('Halve the pipe radius at the same Δp/L. Q?', '1/16 as much.'), ('Find ψ for u = 1, v = 0.', 'ψ = y.'),
              ('Where is shear largest in Poiseuille flow?', 'At the wall.'), ('Name the boundary condition at a solid wall.', 'No slip: fluid velocity equals wall velocity.')],
 'misc': [('Steady flow has zero acceleration.', 'Convective acceleration can be nonzero.'), ('Navier–Stokes has many exact solutions.', 'Only a few simple geometries.'),
          ('Poiseuille’s law works for any pipe flow.', 'Only laminar flow.')],
 'quiz': [{'q': 'Hagen–Poiseuille Q scales with radius as…', 'opts': ['R', 'R²', 'R³', 'R⁴'], 'ok': 3, 'why': 'πR⁴Δp/(8μL).'},
          {'q': 'In Couette flow the profile is…', 'opts': ['parabolic', 'linear', 'uniform', 'logarithmic'], 'ok': 1, 'why': 'No pressure gradient.'},
          {'q': 'The convective acceleration is…', 'opts': ['∂V/∂t', '(V·∇)V', '∇p', 'μ∇²V'], 'ok': 1, 'why': 'Spatial change.'},
          {'q': 'u_max/V_avg in laminar pipe flow is…', 'opts': ['1', '1.5', '2', '4'], 'ok': 2, 'why': 'Parabolic.'}],
 'cards': [('Material derivative', '∂/∂t + V·∇.'), ('Continuity', '∇·V = 0.'), ('Stream function', 'u = ∂ψ/∂y, v = −∂ψ/∂x.'), ('Navier–Stokes', 'ρDV/Dt = −∇p + ρg + μ∇²V.'), ('Couette', 'τ = μU/h.'), ('Poiseuille', 'Q = πR⁴Δp/8μL.')],
 'planet': {'text': ['EPA reports that household leaks can waste nearly 1 trillion gallons of water a year nationwide, that the average household’s leaks can waste more than 9,300 gallons a year, and that 9% of homes have leaks wasting 50 gallons or more per day.',
                     'Small leaks through worn seals and fittings are often slow, laminar flows through tiny gaps, where the R⁴ law above shows why a small widening of a crack makes a big difference. EPA says fixing easily corrected household leaks can save about 10% on water bills.'],
            'site': [('Differential Equations', 'Differential_Equations.html'), ('Calculus III', 'Calculus_III.html')],
            'src': [_LEAK]},
 'res': [(_MIT[0], _MIT[1], 'Navier–Stokes lectures.'), (_MIT25[0], _MIT25[1], 'Exact solutions.'), ('OpenStax UP1, 14.7 Viscosity and turbulence', _O + '14-7-viscosity-and-turbulence', 'Poiseuille’s law.'), (_MITC[0], _MITC[1], 'Kinematics notes.')]})
UNITS.append(
{'id': 'u6', 'title': 'Dimensional Analysis, Similitude and Model Testing', 'weeks': 'Week 8',
 'summary': 'Dimensional homogeneity, the Buckingham Pi theorem, common dimensionless groups (Reynolds, Froude, Mach, Weber, Euler), geometric, kinematic and dynamic similarity, model laws and scale effects, and nondimensionalizing the governing equations.',
 'objectives': ['Find dimensionless groups with the Pi theorem.', 'Name what Re, Fr, Ma and We compare.', 'Scale model test results to full size with Froude or Reynolds similarity.', 'Explain why full similarity is often impossible.'],
 'concepts': ['Every valid equation is dimensionally homogeneous. The Buckingham Pi theorem says a problem with n variables and k basic dimensions has n − k independent dimensionless groups.',
              'Common groups: Re = ρVL/μ (inertia/viscous), Fr = V/√(gL) (inertia/gravity), Ma = V/a (compressibility), We = ρV²L/σ (inertia/surface tension), Eu = Δp/(ρV²) (pressure).',
              'Dynamic similarity: if the model and prototype have the same geometry and the same governing dimensionless groups, their dimensionless results (C_D, C_p, efficiency) match.',
              'Free-surface flows (ships, spillways, waves) use Froude scaling: V_m = V_p√(L_m/L_p); forces scale with the length scale cubed and power with it to the 3.5 power.',
              'Matching Re and Fr together usually needs an impossible fluid, so engineers match the dominant group and correct for the other (scale effects).'],
 'eqs': [('\\Pi\\text{ groups}=n-k', 'Buckingham Pi theorem'), ('Re=\\frac{\\rho VL}{\\mu},\\ Fr=\\frac{V}{\\sqrt{gL}}', 'Reynolds and Froude numbers'), ('V_m=V_p\\sqrt{L_m/L_p}', 'Froude scaling'), ('\\frac{F_p}{F_m}=\\left(\\frac{L_p}{L_m}\\right)^3', 'Force scale (Froude, same fluid)')],
 'worked': [
  {'q': 'Drag F on a sphere depends on ρ, V, D and μ. How many Pi groups, and what are they?', 'steps': ['n = 5 variables, k = 3 dimensions (M, L, T).', 'Groups: F/(ρV²D²) and ρVD/μ.'], 'a': '2 groups: C_D = f(Re).'},
  {'q': 'A 1:20 wave-energy model is tested with Froude scaling. The full-size wave speed is 10 m/s. Find the model speed.', 'steps': ['V_m = 10/√20.'], 'a': 'V_m = 2.24 m/s.'},
  {'q': 'For that model, how do forces and power scale?', 'steps': ['F_p/F_m = 20³.', 'P_p/P_m = 20^3.5.'], 'a': 'Forces × 8000; power × 35,777.'}],
 'practice': [('Which group matters most for a ship’s waves?', 'Froude number.'), ('Which for flow in a small pipe?', 'Reynolds number.'),
              ('A 1:10 model in the same fluid must match Re. Model speed vs full size?', '10 times faster.'), ('What does We compare?', 'Inertia to surface tension.')],
 'misc': [('Model tests use the same speed as full size.', 'They use scaled speeds.'), ('Dimensionless means unimportant.', 'Dimensionless groups control the physics.'),
          ('Any model gives exact full-scale results.', 'Scale effects remain when not all groups match.')],
 'quiz': [{'q': 'Froude number compares inertia to…', 'opts': ['viscosity', 'gravity', 'surface tension', 'compressibility'], 'ok': 1, 'why': 'V/√(gL).'},
          {'q': 'With 6 variables and 3 dimensions there are…', 'opts': ['2', '3', '6', '9'], 'ok': 1, 'why': 'n − k.'},
          {'q': 'Froude-scaled forces (same fluid) scale with length to the…', 'opts': ['1st', '2nd', '3rd', '3.5th'], 'ok': 2, 'why': 'L³.'},
          {'q': 'C_D of a smooth sphere depends mainly on…', 'opts': ['Fr', 'Re', 'We', 'Ma'], 'ok': 1, 'why': 'Viscous effects.'}],
 'cards': [('Pi theorem', 'n − k groups.'), ('Reynolds', 'Inertia/viscous.'), ('Froude', 'Inertia/gravity.'), ('Weber', 'Inertia/surface tension.'), ('Similarity', 'Same groups, same coefficients.'), ('Froude scaling', 'V ∝ √L.')],
 'planet': {'text': ['DOE describes marine energy as power harnessed from waves, tides, and river and ocean currents, and from ocean temperature differences. It says the total U.S. marine energy resource is equivalent to about 57% of all U.S. power generation in 2019, and that these resources are highly predictable.',
                     'DOE notes that researchers are testing and deploying new technologies to harness that resource. Wave-energy converters and tidal turbines are developed with scaled models in wave tanks and flumes long before full-size devices go to sea, using the Froude and Reynolds scaling in this unit.'],
            'site': [('Oceans', 'Oceans.html'), ('Solutions', 'Solutions.html')],
            'src': [_MAR]},
 'res': [(_MIT[0], _MIT[1], 'Dimensional analysis lectures.'), (_MITC[0], _MITC[1], 'Similitude notes.'), ('NASA Glenn: Similarity parameters', _G + 'airsim.html', 'Free NASA page.'), (_MIT25[0], _MIT25[1], 'Scaling.')]})
UNITS.append(
{'id': 'u7', 'title': 'Pipe Flow: Friction, the Moody Chart and Minor Losses', 'weeks': 'Weeks 9–10',
 'summary': 'Laminar and turbulent pipe flow, entrance length, the Darcy–Weisbach equation, laminar friction factor 64/Re, the Moody chart and Colebrook and Haaland correlations, minor losses, noncircular ducts and hydraulic diameter, and series, parallel and network piping.',
 'objectives': ['Decide whether pipe flow is laminar or turbulent.', 'Compute friction losses with Darcy–Weisbach and the Haaland formula.', 'Add minor losses from fittings and valves.', 'Solve simple series and parallel pipe problems.'],
 'concepts': ['In pipes, flow is laminar below Re ≈ 2300, turbulent above about 4000. Turbulent flow mixes momentum strongly and has a flatter profile.',
              'Darcy–Weisbach: h_L = f(L/D)(V²/2g). For laminar flow f = 64/Re.',
              'For turbulent flow f depends on Re and relative roughness ε/D (Moody chart). The Haaland formula is explicit: 1/√f = −1.8 log₁₀[(ε/D/3.7)^1.11 + 6.9/Re].',
              'Fittings, valves, bends and entrances add minor losses h_m = K V²/(2g). In long pipelines friction dominates; in household plumbing fittings matter.',
              'Noncircular ducts use the hydraulic diameter D_h = 4A/P. Pipes in series share Q and add losses; in parallel they share head loss and add flows.'],
 'eqs': [('Re=\\frac{\\rho VD}{\\mu}', 'Pipe Reynolds number'), ('h_L=f\\frac{L}{D}\\frac{V^2}{2g}', 'Darcy–Weisbach'), ('\\frac{1}{\\sqrt f}=-1.8\\log_{10}\\left[\\left(\\frac{\\varepsilon/D}{3.7}\\right)^{1.11}+\\frac{6.9}{Re}\\right]', 'Haaland'), ('h_m=K\\frac{V^2}{2g}', 'Minor loss')],
 'worked': [
  {'q': 'Water flows at 2 m/s in a 50 mm commercial steel pipe (ε = 0.045 mm). Find Re and f.', 'steps': ['Re = 998 × 2 × 0.05/1.002 × 10⁻³ = 99,600.', 'ε/D = 0.0009; Haaland gives f.'], 'a': 'Re = 9.96 × 10⁴ (turbulent); f = 0.0216.'},
  {'q': 'Find the friction head loss over 100 m of that pipe.', 'steps': ['h_L = 0.0216 × (100/0.05) × 2²/(2 × 9.81).'], 'a': 'h_L = 8.82 m.'},
  {'q': 'Find the laminar friction factor at Re = 1500, and the loss of a sharp entrance (K = 0.5) at 2 m/s.', 'steps': ['f = 64/1500.', 'h_m = 0.5 × 4/19.62.'], 'a': 'f = 0.0427; h_m = 0.102 m.'}],
 'practice': [('Find D_h for a 0.2 m × 0.1 m duct.', '4 × 0.02/0.6 = 0.133 m.'), ('Double V in fully rough turbulent flow. h_L?', 'About 4 times.'),
              ('Two identical pipes in parallel carry total Q. Flow in each?', 'Q/2, with the same head loss.'), ('Is Re = 3000 laminar or turbulent?', 'Transitional.')],
 'misc': [('Friction factor is constant.', 'It depends on Re and roughness.'), ('Minor losses are always minor.', 'Not in short pipes with many fittings.'),
          ('Laminar flow has higher losses.', 'At the same Re range it has lower f, but laminar flow happens only at low speeds.')],
 'quiz': [{'q': 'Laminar friction factor is…', 'opts': ['64/Re', '0.316/Re^0.25', '0.02', 'Re/64'], 'ok': 0, 'why': 'Poiseuille.'},
          {'q': 'Darcy–Weisbach loss scales with…', 'opts': ['V', 'V²', 'V³', '1/V'], 'ok': 1, 'why': 'At fixed f.'},
          {'q': 'Hydraulic diameter is…', 'opts': ['4A/P', 'A/P', 'P/A', '2A/P'], 'ok': 0, 'why': 'Definition.'},
          {'q': 'Parallel pipes share the same…', 'opts': ['flow', 'head loss', 'diameter', 'velocity'], 'ok': 1, 'why': 'Common end points.'}],
 'cards': [('Transition', 'Re ≈ 2300–4000.'), ('Darcy–Weisbach', 'f(L/D)V²/2g.'), ('Laminar f', '64/Re.'), ('Haaland', 'Explicit f.'), ('Minor loss', 'KV²/2g.'), ('Hydraulic diameter', '4A/P.')],
 'planet': {'text': ['EPA notes that a faucet dripping once per second can waste more than 3,000 gallons a year, enough for more than 180 showers, and that a showerhead leaking 10 drips per minute wastes more than 500 gallons a year. An irrigation leak 1/32 of an inch across can waste about 6,300 gallons a month.',
                     'Every gallon delivered also has to be pumped through miles of pipe, against the friction losses in this unit. Fixing leaks saves the water and the pumping energy together; 3,000 gallons is about 11,355 L, or 31.1 L every day.'],
            'site': [('Solutions', 'Solutions.html'), ('Mechanics of Materials', 'Mechanics_of_Materials.html')],
            'src': [_LEAK]},
 'res': [(_MITC[0], _MITC[1], 'Pipe-flow notes.'), (_MIT[0], _MIT[1], 'Internal flow lectures.'), ('OpenStax UP1, 14.7 Viscosity and turbulence', _O + '14-7-viscosity-and-turbulence', 'Laminar and turbulent flow.'), (_MIT25[0], _MIT25[1], 'Turbulence.')]})
UNITS.append(
{'id': 'u8', 'title': 'Pumps, Turbines and Pump Systems', 'weeks': 'Week 11',
 'summary': 'Centrifugal and axial pumps, pump head, power and efficiency, pump performance curves, system curves and the operating point, pumps in series and parallel, affinity laws and variable-speed drives, cavitation and NPSH, and hydraulic turbines (Pelton, Francis, Kaplan).',
 'objectives': ['Read a pump curve and find the operating point with a system curve.', 'Compute pump power and efficiency.', 'Apply the affinity laws to speed changes.', 'Explain NPSH and how to avoid cavitation.'],
 'concepts': ['A pump adds head h_p to the flow; water power is ρgQh_p and shaft power is ρgQh_p/η.',
              'The pump curve (head falling as flow rises) meets the system curve (static lift plus losses rising with Q²) at the operating point.',
              'Affinity laws for the same pump at a new speed N: Q ∝ N, H ∝ N², P ∝ N³. Slowing a pump with a variable-speed drive instead of throttling a valve saves a lot of energy.',
              'Cavitation starts when inlet pressure falls near vapor pressure. The available net positive suction head (NPSH_A) must exceed what the pump requires (NPSH_R).',
              'Hydraulic turbines are pumps in reverse: Pelton (impulse) for high head, Francis for medium head, Kaplan (propeller) for low head and large flow; many pumped-storage units are reversible pump-turbines.'],
 'eqs': [('P_{shaft}=\\frac{\\rho gQh_p}{\\eta}', 'Pump power'), ('H_{sys}=H_{static}+kQ^2', 'System curve'), ('\\frac{Q_2}{Q_1}=\\frac{N_2}{N_1},\\ \\frac{H_2}{H_1}=\\left(\\frac{N_2}{N_1}\\right)^2,\\ \\frac{P_2}{P_1}=\\left(\\frac{N_2}{N_1}\\right)^3', 'Affinity laws'), ('NPSH_A>NPSH_R', 'No cavitation')],
 'worked': [
  {'q': 'A pump curve is H = 40 − 7000Q² and the system curve is H = 10 + 5000Q² (H in m, Q in m³/s). Find the operating point.', 'steps': ['40 − 7000Q² = 10 + 5000Q², so Q² = 30/12,000.', 'Q = 0.05 m³/s; H = 10 + 5000 × 0.0025.'], 'a': 'Q = 0.05 m³/s, H = 22.5 m.'},
  {'q': 'Find the shaft power at that point with η = 0.75 (ρ = 1000 kg/m³).', 'steps': ['P = 1000 × 9.81 × 0.05 × 22.5/0.75.'], 'a': 'P = 14.7 kW.'},
  {'q': 'A pump delivering 0.05 m³/s at 30 m head is slowed from 1800 to 1500 rpm. Find the new flow, head and power ratio.', 'steps': ['Q = 0.05 × 1500/1800.', 'H = 30 × (1500/1800)².', 'P ratio = (1500/1800)³.'], 'a': 'Q = 0.0417 m³/s, H = 20.8 m, power 57.9% of the original.'}],
 'practice': [('Two identical pumps in series: what adds?', 'Heads at the same flow.'), ('Two in parallel?', 'Flows at the same head.'),
              ('Cut speed by 20%. Power?', '0.8³ = 51.2%.'), ('Which turbine suits a 500 m head?', 'Pelton.')],
 'misc': [('Throttling a valve is an efficient way to cut flow.', 'It wastes head; slowing the pump is better.'), ('A bigger pump is always better.', 'Oversized pumps run off their best-efficiency point.'),
          ('Cavitation only makes noise.', 'It erodes impellers and cuts performance.')],
 'quiz': [{'q': 'Pump power scales with speed as…', 'opts': ['N', 'N²', 'N³', '√N'], 'ok': 2, 'why': 'Affinity laws.'},
          {'q': 'The operating point is where…', 'opts': ['pump curve meets system curve', 'efficiency is zero', 'Q = 0', 'H = 0'], 'ok': 0, 'why': 'Balance.'},
          {'q': 'To avoid cavitation…', 'opts': ['NPSH_A > NPSH_R', 'NPSH_A < NPSH_R', 'raise speed', 'lower inlet pressure'], 'ok': 0, 'why': 'Margin.'},
          {'q': 'Low head, high flow suits a…', 'opts': ['Pelton', 'Francis', 'Kaplan', 'piston pump'], 'ok': 2, 'why': 'Propeller turbine.'}],
 'cards': [('Pump power', 'ρgQh/η.'), ('System curve', 'H_static + kQ².'), ('Operating point', 'Curves cross.'), ('Affinity', 'Q ∝ N, H ∝ N², P ∝ N³.'), ('NPSH', 'Avoid cavitation.'), ('Turbines', 'Pelton, Francis, Kaplan.')],
 'planet': {'text': ['DOE’s industrial efficiency office states that dramatic energy and cost savings can be achieved in pump systems by applying best energy-management practices and buying energy-efficient equipment, and it offers the free Pumping System Assessment Tool (PSAT) and MEASUR software to find them.',
                     'The affinity laws show where much of that saving comes from: a pump slowed by 20% with a variable-speed drive needs only about half the power. DOE’s pumped storage page adds that pump-turbines move water uphill when power is cheap and generate when it is needed.'],
            'site': [('Solutions', 'Solutions.html'), ('Circuits', 'Circuits.html')],
            'src': [_PUMP, _PSH]},
 'res': [(_MITC[0], _MITC[1], 'Pump notes.'), (_MIT[0], _MIT[1], 'Turbomachinery lectures.'), (_PUMP[0], _PUMP[1], 'Free DOE pump tools.'), (_MIT25[0], _MIT25[1], 'Deeper treatment.')]})
UNITS.append(
{'id': 'u9', 'title': 'External Flow: Boundary Layers, Drag and Lift', 'weeks': 'Weeks 12–13',
 'summary': 'Flow past bodies, boundary layers on flat plates, friction and pressure drag, drag coefficients of spheres, cylinders and streamlined bodies, the drag crisis, Stokes flow and settling, lift, and the power available in a wind or water stream.',
 'objectives': ['Compute drag from a drag coefficient.', 'Explain the roles of friction and pressure drag.', 'Use Stokes’ law for small particles.', 'Find the power in a wind stream and the Betz limit.'],
 'concepts': ['Drag F_D = C_D ½ρV²A and lift F_L = C_L ½ρV²A, with A a reference area. C_D depends on shape and Re.',
              'Streamlined bodies have mostly friction drag; bluff bodies (spheres, cylinders, trucks) have mostly pressure drag from a separated wake.',
              'For a smooth sphere C_D ≈ 0.47 for 10³ < Re < 2 × 10⁵; around Re ≈ 3 × 10⁵ the boundary layer turns turbulent, separates later, and C_D drops sharply (the drag crisis).',
              'At very low Re (Re < 1), Stokes drag F = 3πμVD; a small particle settles at V = (ρ_p − ρ)gD²/(18μ).',
              'A stream of area A carries power ½ρAV³. No turbine can capture more than 16/27 ≈ 59.3% of it (the Betz limit).'],
 'eqs': [('F_D=C_D\\tfrac12\\rho V^2A', 'Drag'), ('F=3\\pi\\mu VD', 'Stokes drag'), ('V_s=\\frac{(\\rho_p-\\rho)gD^2}{18\\mu}', 'Settling speed'), ('P=\\tfrac12\\rho AV^3,\\ \\ C_{P,max}=\\frac{16}{27}', 'Wind power and Betz limit')],
 'worked': [
  {'q': 'A 0.22 m ball moves at 20 m/s in air (C_D = 0.47, sample value). Find Re and drag.', 'steps': ['Re = 1.225 × 20 × 0.22/1.789 × 10⁻⁵ = 3.01 × 10⁵.', 'F = 0.47 × ½ × 1.225 × 400 × π × 0.11².'], 'a': 'Re = 3.01 × 10⁵ (near the drag crisis); F = 4.38 N.'},
  {'q': 'Find the settling speed of a 50 µm sand grain (ρ_p = 2500 kg/m³) in water.', 'steps': ['V = (2500 − 998) × 9.81 × (50 × 10⁻⁶)²/(18 × 1.002 × 10⁻³).', 'Check Re = 998 × 0.00204 × 50 × 10⁻⁶/1.002 × 10⁻³ = 0.102.'], 'a': 'V = 2.04 mm/s; Re < 1, so Stokes’ law holds.'},
  {'q': 'Find the wind power through a 100 m diameter rotor at 10 m/s, and the Betz maximum.', 'steps': ['A = π × 50² = 7854 m².', 'P = ½ × 1.225 × 7854 × 1000.', 'P_max = P × 16/27.'], 'a': 'P = 4.81 MW; Betz maximum 2.85 MW.'}],
 'practice': [('Double wind speed. Power in the wind?', '8 times.'), ('Why do trucks use fairings?', 'To cut pressure drag from the wake.'),
              ('Halve a particle’s diameter. Stokes settling speed?', '1/4.'), ('What is the drag crisis?', 'The sudden fall in C_D when the boundary layer turns turbulent.')],
 'misc': [('Drag is always proportional to V².', 'At very low Re it is proportional to V.'), ('A turbine can extract all the wind’s power.', 'Betz limits it to 59.3%.'),
          ('Rough surfaces always increase drag.', 'On spheres they can trigger the drag crisis earlier.')],
 'quiz': [{'q': 'Wind power scales with V as…', 'opts': ['V', 'V²', 'V³', 'V⁴'], 'ok': 2, 'why': '½ρAV³.'},
          {'q': 'The Betz limit is about…', 'opts': ['30%', '45%', '59%', '100%'], 'ok': 2, 'why': '16/27.'},
          {'q': 'Stokes drag applies when Re is…', 'opts': ['< 1', '≈ 10³', '> 10⁵', 'any'], 'ok': 0, 'why': 'Creeping flow.'},
          {'q': 'Bluff-body drag is mostly…', 'opts': ['friction', 'pressure', 'induced', 'wave'], 'ok': 1, 'why': 'Separated wake.'}],
 'cards': [('Drag', 'C_D ½ρV²A.'), ('Pressure drag', 'Wake behind bluff bodies.'), ('Drag crisis', 'C_D drops near Re 3 × 10⁵.'), ('Stokes', 'F = 3πμVD.'), ('Wind power', '½ρAV³.'), ('Betz', '59.3%.')],
 'planet': {'text': ['DOE explains that wind turbine blades work like an airplane wing or helicopter rotor: the pressure difference across a blade creates lift and drag, and because the lift is stronger than the drag the rotor spins a generator. DOE notes land-based turbines range from 100 kilowatts to several megawatts.',
                     'The ½ρAV³ law explains why turbines keep getting taller and wider: doubling the rotor diameter quadruples the area, and higher hub heights reach faster winds, with power rising as the cube of speed. The Betz limit sets the target every blade designer chases.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Solutions', 'Solutions.html')],
            'src': [_WIND]},
 'res': [('NASA Glenn: Drag of a sphere', _G + 'dragsphere.html', 'Free NASA page.'), ('NASA Glenn: Boundary layer', _G + 'boundlay.html', 'Free NASA page.'), (_MIT[0], _MIT[1], 'External flow lectures.'), ('OpenStax UP1, 14.7 Viscosity and turbulence', _O + '14-7-viscosity-and-turbulence', 'Free textbook section.')]})
UNITS.append(
{'id': 'u10', 'title': 'Open-Channel Flow: Rivers, Canals and Hydraulic Jumps', 'weeks': 'Weeks 14–15',
 'summary': 'Open channels, hydraulic radius, the Froude number and subcritical, critical and supercritical flow, specific energy and critical depth, uniform flow and Manning’s equation, hydraulic jumps and energy dissipation, and weirs for flow measurement.',
 'objectives': ['Classify channel flow with the Froude number.', 'Find critical depth and specific energy.', 'Use Manning’s equation for uniform flow.', 'Compute the depth after and energy lost in a hydraulic jump.'],
 'concepts': ['In open channels gravity drives the flow and the free surface is at atmospheric pressure. The hydraulic radius is R_h = A/P (wetted perimeter).',
              'Froude number Fr = V/√(gy): Fr < 1 subcritical (slow, deep), Fr = 1 critical, Fr > 1 supercritical (fast, shallow). Surface waves can travel upstream only in subcritical flow.',
              'Specific energy E = y + V²/(2g). For flow per unit width q, the minimum E occurs at critical depth y_c = (q²/g)^(1/3).',
              'Uniform flow (Manning, SI): V = (1/n) R_h^(2/3) S^(1/2), with roughness n (about 0.013 for finished concrete) and bed slope S.',
              'A hydraulic jump turns supercritical flow subcritical: y₂/y₁ = ½(√(1 + 8Fr₁²) − 1), and dissipates head h_L = (y₂ − y₁)³/(4y₁y₂). Spillways use jumps to protect riverbeds below dams.'],
 'eqs': [('Fr=\\frac{V}{\\sqrt{gy}}', 'Froude number'), ('E=y+\\frac{V^2}{2g},\\ \\ y_c=\\left(\\frac{q^2}{g}\\right)^{1/3}', 'Specific energy and critical depth'), ('V=\\frac1n R_h^{2/3}S^{1/2}', 'Manning’s equation (SI)'), ('\\frac{y_2}{y_1}=\\tfrac12\\left(\\sqrt{1+8Fr_1^2}-1\\right)', 'Hydraulic jump')],
 'worked': [
  {'q': 'A 2 m wide concrete channel (n = 0.013) flows 1 m deep on a slope of 0.001. Find V and Q.', 'steps': ['A = 2 m², P = 4 m, R_h = 0.5 m.', 'V = (1/0.013) × 0.5^(2/3) × 0.001^0.5.', 'Q = VA.'], 'a': 'V = 1.53 m/s; Q = 3.06 m³/s.'},
  {'q': 'Water flows 0.5 m deep at 6 m/s below a spillway. Find Fr, the depth after a hydraulic jump and the head lost.', 'steps': ['Fr = 6/√(9.81 × 0.5) = 2.71.', 'y₂ = 0.25 × (√(1 + 8 × 2.71²) − 1).', 'h_L = (y₂ − y₁)³/(4y₁y₂).'], 'a': 'Fr = 2.71; y₂ = 1.68 m; h_L = 0.491 m.'},
  {'q': 'Find the critical depth for q = 2 m²/s.', 'steps': ['y_c = (4/9.81)^(1/3).'], 'a': 'y_c = 0.742 m.'}],
 'practice': [('Is V = 3 m/s at 1 m depth sub- or supercritical?', 'Fr = 0.958, subcritical.'), ('Find E for y = 1 m, V = 3 m/s.', '1 + 9/19.62 = 1.459 m.'),
              ('What depth would carry q = 2 m²/s at V = 1.53 m/s?', '2/1.532 = 1.31 m.'), ('Why build a stilling basin below a dam?', 'To force a jump that dissipates energy.')],
 'misc': [('Fast flow is always supercritical.', 'Compare V with √(gy).'), ('A jump gains energy.', 'It loses energy.'),
          ('Manning’s n is the same everywhere.', 'It depends on the surface.')],
 'quiz': [{'q': 'Supercritical flow has…', 'opts': ['Fr < 1', 'Fr = 1', 'Fr > 1', 'Fr = 0'], 'ok': 2, 'why': 'Fast, shallow.'},
          {'q': 'Hydraulic radius is…', 'opts': ['A/P', 'P/A', '4A/P', 'y'], 'ok': 0, 'why': 'Definition.'},
          {'q': 'Specific energy is minimum at…', 'opts': ['critical depth', 'zero depth', 'normal depth', 'any depth'], 'ok': 0, 'why': 'dE/dy = 0.'},
          {'q': 'A hydraulic jump…', 'opts': ['dissipates energy', 'adds energy', 'is reversible', 'speeds up flow'], 'ok': 0, 'why': 'Turbulent mixing.'}],
 'cards': [('Froude', 'V/√(gy).'), ('Hydraulic radius', 'A/P.'), ('Specific energy', 'y + V²/2g.'), ('Critical depth', '(q²/g)^(1/3).'), ('Manning', '(1/n)R^(2/3)S^(1/2).'), ('Jump', 'y₂/y₁ = ½(√(1 + 8Fr²) − 1).')],
 'planet': {'text': ['DOE describes a diversion, or run-of-river, hydropower facility as one that channels part of a river through a canal and/or a penstock, using the natural decline of the riverbed to produce energy, sometimes without a dam. Designing that canal is an open-channel problem: Manning’s equation sizes it for the flow, and the drop sets the head.',
                     'DOE adds that impoundment releases can serve fish passage and water-quality needs. Engineers use the Froude number and hydraulic jumps to shape spillways and channels that protect riverbeds and keep flows safe for wildlife.'],
            'site': [('Oceans', 'Oceans.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_TYP, _HYD]},
 'res': [(_MITC[0], _MITC[1], 'Open-channel notes.'), (_MIT[0], _MIT[1], 'Free-surface flows.'), ('NOAA: Currents tutorial', _THC[1], 'Free NOAA tutorial.'), (_MIT25[0], _MIT25[1], 'Deeper treatment.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Density and buoyancy by weighing', 'week': 'Week 3',
 'goal': 'Find an object’s volume and density from its weight in air and its apparent weight in water, using Archimedes’ principle.',
 'eq': ('V=\\frac{m_{air}-m_{water}}{\\rho_w},\\ \\ \\rho=\\frac{m_{air}}{V}', 'Archimedes’ principle'),
 'steps': ['Explore PhET Buoyancy: change object density and fluid density and watch the forces.', 'Home: weigh a small dense object (a stone or metal spoon) on a kitchen scale.', 'Hang it by a thread fully under water in a jug resting on the scale (tare first), or use a hanging luggage scale; record the apparent mass.', 'Compute volume and density.'],
 'table': (['Quantity', 'Value'], [['Mass in air', '200 g'], ['Apparent mass in water', '120 g'], ['Volume', '80 cm³'], ['Density', '2500 kg/m³']]),
 'note': 'Sample values (typical of stone or glass).',
 'calc': ['V = (200 − 120)/1.00 = 80 cm³.', 'ρ = 200/80 = 2.50 g/cm³ = 2500 kg/m³.'],
 'safety': ['Wipe up spills at once.'], 'home': ['This is a home lab.'],
 'sims': [('PhET: Buoyancy', _PH + 'buoyancy'), ('PhET: Density', _PH + 'density')],
 'planet': 'NOAA explains that density differences from temperature and salinity drive the deep-ocean conveyor belt.', 'planet_src': [_THC]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Torricelli’s bottle', 'week': 'Week 4',
 'goal': 'Check Torricelli’s law by measuring how far a water jet travels from a hole in a bottle.',
 'eq': ('V=\\sqrt{2gh},\\ \\ x=2\\sqrt{hY}', 'Jet speed and range from height Y'),
 'steps': ['Poke a small hole in the side of a plastic bottle near the bottom; tape over it.', 'Fill the bottle and set it on a box over a sink or outdoors, with the hole Y = 0.3 m above the landing surface.', 'Remove the tape; when the water level is h = 0.2 m above the hole, mark where the jet lands.', 'Compare with the prediction; repeat at other depths.'],
 'table': (['Quantity', 'Value'], [['Head h', '0.20 m'], ['Jet speed', '1.98 m/s'], ['Drop height Y', '0.30 m'], ['Predicted range', '0.49 m']]),
 'note': 'Predicted values; real jets land a little short because of losses at the hole.',
 'calc': ['V = √(2 × 9.81 × 0.2) = 1.98 m/s.', 'x = 2√(0.2 × 0.3) = 0.49 m.'],
 'safety': ['Do it over a sink or outdoors; wipe up water to avoid slips.', 'Use a skewer carefully, pointing away from your hand.'], 'home': ['This is a home lab.'],
 'sims': [('PhET: Fluid Pressure and Flow', _PH + 'fluid-pressure-and-flow'), ('PhET: Under Pressure', _PH + 'under-pressure')],
 'planet': 'DOE notes hydropower output grows with head; the bottle’s jet speed grows with √h for the same reason.', 'planet_src': [_HYD]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Measuring flow rate and Reynolds number', 'week': 'Week 7',
 'goal': 'Measure a tap or hose flow rate with a bucket and stopwatch and decide whether the flow inside is laminar or turbulent.',
 'eq': ('Q=\\frac{V_{bucket}}{t},\\ \\ Re=\\frac{\\rho VD}{\\mu}', 'Flow rate and Reynolds number'),
 'steps': ['Time how long a hose or tap takes to fill 10 L.', 'Measure the inner diameter of the hose or tap outlet.', 'Compute Q, the mean speed and Re.', 'Turn the tap down until the stream looks smooth and glassy, and repeat.'],
 'table': (['Quantity', 'Value'], [['10 L in', '25 s'], ['Q', '0.4 L/s'], ['Hose bore', '16 mm'], ['V', '1.99 m/s'], ['Re', '31,700']]),
 'note': 'Sample values; Re far above 4000 means turbulent flow inside the hose.',
 'calc': ['V = 0.0004/(π × 0.008²) = 1.99 m/s.', 'Re = 998 × 1.99 × 0.016/1.002 × 10⁻³ = 31,700.'],
 'safety': ['Turn off the tap when done; watch for slippery ground.'], 'home': ['This is a home lab.'],
 'sims': [('PhET: Fluid Pressure and Flow', _PH + 'fluid-pressure-and-flow')],
 'planet': 'EPA suggests checking your water meter over two hours with no water in use; any change means a leak.', 'planet_src': [_LEAK]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Pipe friction spreadsheet', 'week': 'Week 10',
 'goal': 'Build a spreadsheet of Reynolds number, friction factor and head loss against speed, and see how losses grow.',
 'eq': ('h_L=f\\frac{L}{D}\\frac{V^2}{2g}', 'Darcy–Weisbach'),
 'steps': ['Set D = 50 mm, L = 100 m, ε = 0.045 mm, water at 20 °C.', 'Compute Re and the Haaland f for V from 0.5 to 3 m/s.', 'Compute h_L and plot it against V.', 'Fit h_L ∝ V^n and find n.'],
 'table': (['V (m/s)', 'Re', 'f', 'h_L (m)'], [['1', '49,800', '0.0235', '2.39'], ['2', '99,600', '0.0216', '8.82'], ['3', '149,400', '0.0209', '19.2']]),
 'note': 'Computed values; n comes out a little under 2 because f falls slowly as Re rises.',
 'calc': ['h_L(2 m/s) = 0.0216 × 2000 × 4/19.62 = 8.82 m.', 'Tripling V raises h_L by 19.2/2.39 = 8.0 times.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MITC[0], _MITC[1])],
 'planet': 'DOE says best practices in pump systems save dramatic energy; lower losses mean smaller pumps.', 'planet_src': [_PUMP]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Settling of sand in water', 'week': 'Week 13',
 'goal': 'Watch fine and coarse sand settle in a tall glass of water and compare with Stokes’ law.',
 'eq': ('V_s=\\frac{(\\rho_p-\\rho)gD^2}{18\\mu}', 'Stokes settling'),
 'steps': ['Fill a tall clear glass or bottle with water.', 'Drop a pinch of fine sand and time how long the grains take to fall 0.2 m.', 'Repeat with coarser sand.', 'Compare the speeds with Stokes’ law and note when it stops applying.'],
 'table': (['Grain diameter', 'Stokes speed', 'Re'], [['50 µm', '2.04 mm/s', '0.102'], ['100 µm', '8.17 mm/s', '0.81']]),
 'note': 'Computed for quartz-like grains (ρ = 2500 kg/m³); coarser grains with Re above about 1 fall slower than Stokes predicts.',
 'calc': ['V(50 µm) = 1502 × 9.81 × 2.5 × 10⁻⁹/(18 × 1.002 × 10⁻³) = 2.04 mm/s.', 'Doubling D gives 4 times the speed.'],
 'safety': ['Use clean play sand; wash hands afterward.'], 'home': ['This is a home lab.'],
 'sims': [('NASA Glenn: Drag of a sphere', _G + 'dragsphere.html')],
 'planet': 'DOE notes impoundment releases serve water-quality needs; sediment settling decides how reservoirs fill and rivers carry silt.', 'planet_src': [_TYP]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Pump system and variable speed', 'week': 'Week 11',
 'goal': 'Find a pump’s operating point and use the affinity laws to compare throttling with slowing the pump.',
 'eq': ('\\frac{P_2}{P_1}=\\left(\\frac{N_2}{N_1}\\right)^3', 'Affinity law for power'),
 'steps': ['Enter the pump curve H = 40 − 7000Q² and system curve H = 10 + 5000Q².', 'Find the operating point and shaft power.', 'Apply the affinity laws at 1500 and 1200 rpm to the 1800 rpm point (0.05 m³/s, 30 m).', 'Compare power needs.'],
 'table': (['N (rpm)', 'Q (m³/s)', 'H (m)', 'Power ratio'], [['1800', '0.050', '30.0', '1.000'], ['1500', '0.0417', '20.8', '0.579'], ['1200', '0.0333', '13.3', '0.296']]),
 'note': 'Ideal affinity scaling; static lift in the system limits how far a real pump can be slowed.',
 'calc': ['Q(1200) = 0.05 × 2/3 = 0.0333 m³/s.', 'Power ratio = (2/3)³ = 0.296.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_PUMP[0], _PUMP[1])],
 'planet': 'DOE’s free PSAT and MEASUR tools help plants find exactly these pump savings.', 'planet_src': [_PUMP]})
SCHEDULE = [(1, 'u1', 'Fluid properties, viscosity, surface tension', 'OpenStax UP1 14.1, 14.7'), (2, 'u2', 'Hydrostatics and manometers', 'UP1 14.2'),
            (3, 'u2', 'Forces on submerged surfaces, buoyancy, stability; Lab A', 'UP1 14.4'), (4, 'u3', 'Continuity, Bernoulli, heads, energy equation; Lab B', 'UP1 14.5–14.6'),
            (5, 'u4', 'Reynolds transport theorem, momentum, jets, vanes, Pelton', 'MIT 2.06'), (6, 'u5', 'Kinematics, continuity, stream function', 'MIT 2.06'),
            (7, 'u5', 'Navier–Stokes, Couette and Poiseuille; Lab C; midterm practice', 'MIT 2.25'), (8, 'u6', 'Dimensional analysis and similitude', 'MIT 1.060'),
            (9, 'u7', 'Laminar and turbulent pipe flow, Moody chart', 'MIT 1.060'), (10, 'u7', 'Minor losses, networks; Lab D', 'MIT 1.060'),
            (11, 'u8', 'Pumps, system curves, affinity laws, turbines; Lab F', 'DOE pump systems'), (12, 'u9', 'Boundary layers, drag, Stokes flow', 'NASA Glenn'),
            (13, 'u9', 'Lift, wind power, Betz limit; Lab E', 'NASA Glenn; DOE wind'), (14, 'u10', 'Open channels, Froude number, Manning', 'MIT 1.060'),
            (15, 'u10', 'Specific energy, hydraulic jumps, weirs; final practice', 'MIT 1.060')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Find the shear stress in water between plates 0.5 mm apart when one moves at 1 m/s.', ['τ = 1.002 × 10⁻³ × 1/0.0005.'], '2.00 Pa.'),
  ('Find the gauge pressure 25 m deep in seawater (1025 kg/m³).', ['1025 × 9.81 × 25.'], '251.4 kPa.'),
  ('Find the power of a hydro plant with Q = 20 m³/s, H = 40 m, η = 0.88 (ρ = 1000).', ['0.88 × 1000 × 9.81 × 20 × 40.'], '6.91 MW.'),
  ('A 0.01 m³/s water jet at 25 m/s is turned 180° by a fixed vane. Force?', ['2ρQV = 2 × 1000 × 0.01 × 25.'], '500 N.'),
  ('Find laminar Q in a 2 mm radius tube, Δp/L = 200 Pa/m, water.', ['π × 0.002⁴ × 200/(8 × 1.002 × 10⁻³).'], '1.25 × 10⁻⁶ m³/s.')]),
 ('Final practice set (all units)', [
  ('A 1:25 ship model is Froude-scaled. Full speed 10 m/s. Model speed?', ['10/5.'], '2 m/s.'),
  ('Find h_L in 200 m of 0.1 m pipe with f = 0.02 at 1.5 m/s.', ['0.02 × 2000 × 2.25/19.62.'], '4.59 m.'),
  ('A pump at 1200 rpm gives 25 m head. Head at 1500 rpm?', ['25 × (1.25)².'], '39.1 m.'),
  ('Find the wind power through a 80 m rotor at 8 m/s (ρ = 1.225).', ['½ × 1.225 × π × 40² × 512.'], '1.58 MW.'),
  ('Find Fr for 4 m/s flow 0.4 m deep.', ['4/√(9.81 × 0.4).'], '2.02, supercritical.'),
  ('Find y_c for q = 3 m²/s.', ['(9/9.81)^(1/3).'], '0.972 m.')])]
FORMULAS = ['\\tau=\\mu\\,du/dy,\\ \\nu=\\mu/\\rho', 'p=p_0+\\rho gh,\\ F=\\rho gh_cA,\\ F_B=\\rho gV', 'Q=AV,\\ p/\\rho g+V^2/2g+z=\\text{const}', 'P=\\eta\\rho gQH,\\ V=\\sqrt{2gh}',
            '\\sum F=\\sum\\dot mV_{out}-\\sum\\dot mV_{in},\\ F=\\rho QV(1-\\cos\\theta)', '\\nabla\\cdot\\mathbf V=0,\\ Q=\\pi R^4\\Delta p/(8\\mu L)', 'Re=\\rho VL/\\mu,\\ Fr=V/\\sqrt{gL}',
            'h_L=f(L/D)V^2/2g,\\ f_{lam}=64/Re', 'h_m=KV^2/2g,\\ D_h=4A/P', 'P=\\rho gQh/\\eta,\\ Q\\propto N,\\ H\\propto N^2,\\ P\\propto N^3', 'F_D=C_D\\tfrac12\\rho V^2A,\\ P_{wind}=\\tfrac12\\rho AV^3',
            'V=(1/n)R_h^{2/3}S^{1/2},\\ y_c=(q^2/g)^{1/3}', 'y_2/y_1=\\tfrac12(\\sqrt{1+8Fr_1^2}-1)']
GLOSSARY = sorted([('Boundary layer', 'Thin layer near a wall where viscosity matters.'), ('Buoyancy', 'Upward force equal to the weight of displaced fluid.'), ('Cavitation', 'Vapor bubbles forming where pressure falls to vapor pressure.'),
    ('Continuity', 'Conservation of mass in a flow.'), ('Drag coefficient', 'Drag divided by ½ρV²A.'), ('Froude number', 'V/√(gL), inertia over gravity.'), ('Head', 'Energy per unit weight of fluid, in metres.'),
    ('Head loss', 'Mechanical energy lost to friction, per unit weight.'), ('Hydraulic jump', 'Sudden change from supercritical to subcritical flow.'), ('Hydraulic radius', 'Flow area over wetted perimeter.'),
    ('Laminar flow', 'Smooth, layered flow at low Reynolds number.'), ('Manometer', 'Tube of liquid used to measure pressure differences.'), ('Navier–Stokes equations', 'Momentum equations for a viscous fluid.'),
    ('Operating point', 'Where a pump curve meets the system curve.'), ('Reynolds number', 'ρVL/μ, inertia over viscous forces.'), ('Specific gravity', 'Density relative to water.'),
    ('Stokes flow', 'Creeping flow at Re much less than 1.'), ('Surface tension', 'Force per length along a liquid surface.'), ('Turbulent flow', 'Chaotic, mixing flow at high Reynolds number.'), ('Viscosity', 'Resistance of a fluid to shearing.')])
RUBRIC = [('4 · Mastery', 'Sketches control volumes, picks the right law (hydrostatics, Bernoulli, energy, momentum, Navier–Stokes), checks Re and Fr, keeps units straight, and runs labs safely.'), ('3 · Proficient', 'Solves the practice problems with occasional unit or sign slips.'),
          ('2 · Developing', 'Follows worked examples but applies Bernoulli across pumps or ignores losses.'), ('1 · Beginning', 'Plugs numbers into formulas without a sketch; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    g = 9.81; rw = 998; mu = 1.002e-3; ra = 1.225; mua = 1.789e-5
    hf = lambda V, D=.05, e=.045e-3: (-1.8 * log10(((e / D) / 3.7) ** 1.11 + 6.9 / (rw * V * D / mu))) ** -2
    hl = lambda V: hf(V) * (100 / .05) * V * V / (2 * g)
    QP = lambda R, dpl: pi * R ** 4 * dpl / (8 * mu)
    Fr = 6 / sqrt(g * .5); y2 = .25 * (sqrt(1 + 8 * Fr ** 2) - 1)
    Vm = 1 / .013 * .5 ** (2 / 3) * .001 ** .5
    Aj = pi * .05 ** 2 / 4
    Qo = sqrt(30 / 12000)
    Pw = .5 * ra * pi * 50 ** 2 * 1000
    vs = lambda D: (2500 - rw) * g * D * D / (18 * mu)
    r = [
     ('u1 tau', mu * 2 / .001, 2.00), ('u1 cap', 4 * .0728 / (rw * g * .001), .0297), ('u1 nu', mu / rw, 1.004e-6), ('u1 SG', 1025 / rw, 1.027), ('u1 cap2', 4 * .0728 / (rw * g * .0005), .0595), ('u1 mu', mu / mua, 56.0),
     ('u1 ice', 917 / 1025, .895), ('u1 nur', (mua / ra) / (mu / rw), 14.5),
     ('u2 p10', rw * g * 10, 97.9e3), ('u2 F', rw * g * 1.5 * 6, 88.1e3), ('u2 I', 2 * 27 / 12, 4.5), ('u2 ycp', 1.5 + 4.5 / 9, 2.0), ('u2 man', (13600 - 1000) * g * .1, 12.4e3), ('u2 FB', 1000 * g * .002, 19.6),
     ('u2 abs', 101.3e3 + rw * g * 10, 199.2e3),
     ('u3 V', sqrt(2 * g * 5), 9.90), ('u3 P', .9 * 1000 * g * 50 * 100, 44.1e6), ('u3 pump', 1000 * g * .05 * 25 / .75, 16.4e3), ('u3 v1', .0004 / (pi * .01 ** 2), 1.27), ('u3 v2', .0004 / (pi * .005 ** 2), 5.09),
     ('u3 head', 200000 / (1000 * g), 20.4),
     ('u4 A', Aj, 1.963e-3), ('u4 F', 1000 * Aj * 400, 785), ('u4 vane', 1000 * Aj * 400 * (1 - cos(radians(120))), 1178), ('u4 pel', 1000 * .01 * 15 * (1 - cos(radians(165))), 294.9),
     ('u4 P', 1000 * .01 * 15 * (1 - cos(radians(165))) * 15, 4.42e3), ('u4 jetP', .5 * 1000 * .01 * 900, 4.5e3),
     ('u5 Q', QP(.002, 100), 6.27e-7), ('u5 V', QP(.002, 100) / (pi * .002 ** 2), .0499), ('u5 um', 2 * QP(.002, 100) / (pi * .002 ** 2), .0998), ('u5 Re', rw * QP(.002, 100) / (pi * .002 ** 2) * .004 / mu, 199),
     ('u5 tau', mu * 1 / .002, .501), ('u5 R4', .5 ** 4, 1 / 16),
     ('u6 Vm', 10 / sqrt(20), 2.24), ('u6 F', 20 ** 3, 8000), ('u6 P', 20 ** 3.5, 35777), ('u6 pi', 5 - 3, 2),
     ('u7 Re', rw * 2 * .05 / mu, 99600), ('u7 f', hf(2), .0216), ('u7 hL', hl(2), 8.82), ('u7 flam', 64 / 1500, .0427), ('u7 hm', .5 * 4 / (2 * g), .102), ('u7 Dh', 4 * .02 / .6, .133),
     ('u7 L', 3000 * 3.785, 11355), ('u7 day', 3000 * 3.785 / 365, 31.1),
     ('u8 Q', Qo, .05), ('u8 H', 10 + 5000 * Qo ** 2, 22.5), ('u8 P', 1000 * g * Qo * 22.5 / .75, 14.7e3), ('u8 Q2', .05 * 1500 / 1800, .0417), ('u8 H2', 30 * (1500 / 1800) ** 2, 20.8), ('u8 Pr', (1500 / 1800) ** 3, .579),
     ('u8 cut', .8 ** 3, .512),
     ('u9 Re', ra * 20 * .22 / mua, 3.01e5), ('u9 F', .47 * .5 * ra * 400 * pi * .11 ** 2, 4.38), ('u9 vs', vs(50e-6), 2.04e-3), ('u9 Res', rw * vs(50e-6) * 50e-6 / mu, .102), ('u9 A', pi * 2500, 7854),
     ('u9 Pw', Pw, 4.81e6), ('u9 Betz', Pw * 16 / 27, 2.85e6), ('u9 b', 16 / 27, .593),
     ('u10 V', Vm, 1.53), ('u10 Q', 2 * Vm, 3.06), ('u10 Fr', Fr, 2.71), ('u10 y2', y2, 1.68), ('u10 hL', (y2 - .5) ** 3 / (4 * .5 * y2), .491), ('u10 yc', (4 / g) ** (1 / 3), .742), ('u10 Fr2', 3 / sqrt(g), .958),
     ('u10 E', 1 + 9 / (2 * g), 1.459), ('u10 y', 2 / Vm, 1.31),
     ('A V', (200 - 120) / 1.0, 80), ('A rho', 200 / 80 * 1000, 2500),
     ('B V', sqrt(2 * g * .2), 1.98), ('B x', 2 * sqrt(.2 * .3), .49),
     ('C Q', 10 / 25, .4), ('C V', .0004 / (pi * .008 ** 2), 1.99), ('C Re', rw * .0004 / (pi * .008 ** 2) * .016 / mu, 31700),
     ('D Re1', rw * 1 * .05 / mu, 49800), ('D f1', hf(1), .0235), ('D h1', hl(1), 2.39), ('D f2', hf(2), .0216), ('D h2', hl(2), 8.82), ('D Re3', rw * 3 * .05 / mu, 149400), ('D f3', hf(3), .0209), ('D h3', hl(3), 19.2),
     ('D r', hl(3) / hl(1), 8.0),
     ('E v1', vs(50e-6), 2.04e-3), ('E v2', vs(100e-6), 8.17e-3), ('E Re2', rw * vs(100e-6) * 1e-4 / mu, .81),
     ('F Q15', .05 * 1500 / 1800, .0417), ('F H15', 30 * (5 / 6) ** 2, 20.8), ('F P15', (5 / 6) ** 3, .579), ('F Q12', .05 * 2 / 3, .0333), ('F H12', 30 * (2 / 3) ** 2, 13.3), ('F P12', (2 / 3) ** 3, .296),
     ('M1', mu / .0005, 2.00), ('M2', 1025 * g * 25, 251.4e3), ('M3', .88 * 1000 * g * 800, 6.91e6), ('M4', 2 * 1000 * .01 * 25, 500), ('M5', QP(.002, 200), 1.25e-6),
     ('F1', 10 / 5, 2), ('F2', .02 * 2000 * 2.25 / (2 * g), 4.59), ('F3', 25 * 1.25 ** 2, 39.1), ('F4', .5 * ra * pi * 1600 * 512, 1.58e6), ('F5', 4 / sqrt(g * .4), 2.02), ('F6', (9 / g) ** (1 / 3), .972)]
    r += [('x u1 dudy', 2 / .001, 2000), ('x u2 hc', 3 / 2, 1.5), ('x u2 23', 2.0 / 3, .667), ('x u3 ratio', (.01 / .005) ** 2, 4), ('x u4 15', 1 - cos(radians(120)), 1.5), ('x u4 165', 1 - cos(radians(165)), 1.966),
          ('x u5 a', 2 * 2, 4), ('x u6 s20', sqrt(20), 4.472), ('x u7 eD', .045 / 50, .0009), ('x u7 LD', 100 / .05, 2000), ('x u8 Q2', 30 / 12000, .0025), ('x u8 r', 1500 / 1800, .833),
          ('x u9 Ab', pi * .11 ** 2, .038), ('x u9 V3', 10 ** 3, 1000), ('x u10 Rh', 2 / 4, .5), ('x u10 F2', 8 * Fr ** 2, 58.7), ('x u10 q', 2 ** 2 / g, .408), ('x A dm', 200 - 120, 80),
          ('x B t', sqrt(2 * .3 / g), .247), ('x C r', .008, .008), ('x D Vs', 2 ** 2 / (2 * g), .204), ('x E dr', 2500 - rw, 1502), ('x F r', 1200 / 1800, .667), ('x M2', 1025 * g, 10055),
          ('x v2', 1.27 * 4, 5.09), ('x u1 gap', .0005 / .001, .5), ('x u2 rhogh', 1000 * g * .1, 981), ('x u2 Hg', 13600 * g * .1, 13342), ('x u3 rgQ', 1000 * g * 50, 490500), ('x u3 kin', 9.90 ** 2 / (2 * g), 5.0),
          ('x u4 rQ', 1000 * .01, 10), ('x u4 VU', 30 - 15, 15), ('x u5 R4', .002 ** 4, 1.6e-11), ('x u5 8mu', 8 * mu, 8.016e-3), ('x u6 n', 6 - 3, 3), ('x u6 1to25', sqrt(25), 5),
          ('x u7 Re15', 64 / .0427, 1500), ('x u7 dsh', 180 / 3000 * 3000, 180), ('x u8 P51', .8 ** 3 * 100, 51.2), ('x u8 s', 1 + 1, 2), ('x u9 dD', (100 / 50) ** 2, 4), ('x u9 Ad', pi * 50 ** 2 * 4 / (pi * 50 ** 2), 4),
          ('x u10 ar', 2 * 1, 2), ('x u10 per', 2 + 2 * 1, 4), ('x u10 Fy', sqrt(g * .5), 2.215), ('x u10 E2', 9 / (2 * g), .459), ('x C L', 10 / 1000, .01), ('x B Y', 2 * .3 / g, .0612),
          ('x M3 h', 20 * 40, 800), ('x M5 R', .002 ** 4 * 200, 3.2e-9), ('x F3 r', 1500 / 1200, 1.25), ('x F5 s', sqrt(g * .4), 1.981), ('x E 18', 18 * mu, .018036), ('x D 3', 3 ** 2 / 1, 9),
          ('x A g', 200 / 1000, .2), ('x u9 rho', .5 * ra, .6125), ('x u9 16', 16 / 27 * 100, 59.3), ('x u7 hm2', 4 / (2 * g), .204), ('x u2 dp', 13600 - 1000, 12600),
          ('x F4 A', pi * 40 ** 2, 5027), ('x F4 V', 8 ** 3, 512), ('x F2 V', 1.5 ** 2, 2.25), ('x F6 q', 3 ** 2, 9), ('x u3 H', 20 + 5, 25), ('x u9 k', 4 * 16 / 27, 2.37)]
    return r
