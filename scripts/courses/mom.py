"""Mechanics of Materials (ENGR 213): stress, strain, axial load, torsion, bending, shear, stress transformation, pressure vessels, deflection and buckling.
Oct 25 2026, founder-approved four-year track, sophomore course 6. Same module fields as statics.py / dynamics.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, sin, cos, tan, exp, log, atan, atan2, degrees, radians
ID = 'mom'
STATUS = 'live'
YEAR = 2
PAGE = 'Mechanics_of_Materials.html'
CODE = 'ENGR 213'
TITLE = 'Mechanics of Materials'
LAB_NAME = 'Materials lab'
TAGLINE = 'Stress, strain and how parts stretch, twist, bend and fail: axial loads, thermal stress, shafts, beams, shear flow, Mohr’s circle, failure theories, pressure vessels, deflection and buckling, with six labs. Free, self-paced, and tied to wind turbines, lighter cars, mass timber, hydrogen tanks, bridges and rockets.'
DESC = 'Free self-study Mechanics of Materials: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and home labs, practice exams, tied to wind blades, hydrogen tanks and bridges.'
ALT = 'NASA photo of the Space Launch System core stage test firing'
_O = 'https://openstax.org/books/university-physics-volume-1/pages/'
_O2 = 'https://openstax.org/books/university-physics-volume-2/pages/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 2.001 Mechanics and Materials I', 'https://ocw.mit.edu/courses/2-001-mechanics-materials-i-fall-2006/')
_MIT2 = ('MIT OpenCourseWare 2.002 Mechanics and Materials II', 'https://ocw.mit.edu/courses/2-002-mechanics-and-materials-ii-spring-2004/')
_ASCE = ('ASCE Report Card for America’s Infrastructure: Bridges', 'https://infrastructurereportcard.org/cat-item/bridges-infrastructure/')
_LW = ('U.S. DOE: Lightweight materials for cars and trucks', 'https://www.energy.gov/eere/vehicles/lightweight-materials-cars-and-trucks')
_BIG = ('U.S. DOE: Wind turbines, the bigger the better', 'https://www.energy.gov/eere/articles/wind-turbines-bigger-better')
_WIND = ('U.S. DOE: How do wind turbines work?', 'https://www.energy.gov/eere/wind/how-do-wind-turbines-work')
_WTTC = ('NREL: Building state-of-the-art wind technology testing facilities (fact sheet)', 'https://docs.nlr.gov/docs/fy12osti/53581.pdf')
_MT = ('USDA Forest Service: What is the impact of mass timber utilization on climate and forests? (2022)', 'https://research.fs.usda.gov/treesearch/63853')
_H2 = ('U.S. DOE: Hydrogen storage', 'https://www.energy.gov/eere/fuelcells/hydrogen-storage')
_SBKF = ('NASA NESC: Shell Buckling Knockdown Factor project', 'https://www.nasa.gov/centers-and-facilities/nesc/proving-management-skills-on-the-shell-buckling-knockdown-factor-project/')
BANNER = ['images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg', 'images/GOES19_GOESU_KSC.jpg', 'images/Sentinel6B_Launch.jpg', 'images/ISS_Over_Ganges_STS102.jpg']
CREDITS = {'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg': 'NASA/Michael DeMocker (MAF20210116_GR0006)', 'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC',
           'images/Sentinel6B_Launch.jpg': 'NASA/Carla Thomas (AFRC2025-0170-03)', 'images/ISS_Over_Ganges_STS102.jpg': 'NASA (STS102-357-031, March 18, 2001)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester sophomore mechanics of materials (strength of materials) course. It is modeled on the topics and depth of MIT 2.001 Mechanics and Materials I (on MIT OpenCourseWare), Purdue ME 323 Mechanics of Materials and Georgia Tech COE 3001 Mechanics of Deformable Bodies, and on the free OpenStax University Physics, which we link where it helps. None of those authors or schools endorses this page.',
         'What we add: every unit ties to real clean-energy, infrastructure or space work with a cited public source (bridges, lighter cars, wind turbine towers, shafts and blades, mass timber, hydrogen tanks, NASA rocket structures), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a cheap home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Mechanics of materials decides how much material a structure needs. Using just enough steel, aluminum, composite or wood, and no more, makes cars lighter and more efficient, wind turbines taller, buildings lower in carbon, and rockets able to carry more to orbit.',
                 'It is also how we keep what we have built safe: bridges, towers and tanks must carry their loads for decades without yielding, cracking from fatigue or buckling. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values, and material properties are typical textbook values.']
PREREQS = ['Statics: free-body diagrams, equilibrium, centroids and area moments of inertia.', 'Calculus I and II: derivatives and integrals; Unit 9 integrates the beam equation twice.',
           'Physics I helps with springs, energy and units.', 'Dynamics is not required.']
STUDY = ['Start every problem with statics: a free-body diagram and the internal force, torque or moment at the cut.', 'Then ask how the part deforms: stretch, twist or bend, and which formula fits that deformation.',
         'Check that the formula applies: linear elastic, small deformations, thin walls or long slender members where required.', 'Solve with symbols first, then put in SI numbers (N, m, Pa), and check units: 1 MPa = 1 N/mm².',
         'Compare the stress with the material’s allowable stress and state a factor of safety.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET simulations (they run in a browser).', 'Rubber bands, a bag for coins or washers, and a kitchen scale (to know each mass).',
            'A 30 cm plastic ruler, a second ruler or tape measure, and tape or a clamp to hold it to a table edge.', 'A foam rod or pool-noodle offcut and a marker for torsion lines.',
            'Dry spaghetti and small weights for the buckling lab.', 'Safety glasses, a smartphone camera and spreadsheet software for graphs and fits.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab can be done in a free simulation or with household items. Stretched rubber bands and snapping spaghetti can fly: wear glasses, keep loads small, and keep faces away from parts under load.']
SAFETY_SRC = ('OSHA: Hand and power tools', 'https://www.osha.gov/hand-power-tools')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('1 megapascal (MPa)', '10⁶ Pa = 1 N/mm²'), ('1 bar', '10⁵ Pa = 0.1 MPa'), ('1 psi (lbf/in²)', '6894.757 Pa'), ('1 pound-force (lbf)', '4.448222 N'),
             ('1 revolution per minute', '0.1047198 rad/s'), ('Typical steel (textbook values)', 'E = 200 GPa, G = 80 GPa, ν = 0.3, α = 12 × 10⁻⁶/°C, yield about 250 MPa'),
             ('Typical aluminum alloy (textbook values)', 'E = 70 GPa, G = 26 GPa, ν = 0.33, α = 23 × 10⁻⁶/°C')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free textbooks, lectures and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT lecture notes, problem sets and exams.'), (_MIT2[0], _MIT2[1], 'Free MIT follow-on course: plasticity, fracture and fatigue.'),
          ('OpenStax University Physics Volume 1, 12.3 Stress, strain and elastic modulus', _O + '12-3-stress-strain-and-elastic-modulus', 'Free textbook introduction to stress and strain.'),
          ('OpenStax University Physics Volume 1, 12.4 Elasticity and plasticity', _O + '12-4-elasticity-and-plasticity', 'Yield, plastic flow and fracture.'),
          ('PhET: Hooke’s Law', _PH + 'hookes-law', 'Springs, stiffness and energy.'), ('PhET: Masses and Springs', _PH + 'masses-and-springs', 'Stiffness and stretch.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Stress: Normal, Shear and Bearing; Allowable Stress and Factor of Safety', 'weeks': 'Weeks 1–2',
 'summary': 'Internal forces found by cutting a member, average normal stress in rods, average shear stress in pins and bolts (single and double shear), bearing stress, allowable stress design and the factor of safety.',
 'objectives': ['Find internal forces with a free-body diagram of a cut section.', 'Compute average normal, shear and bearing stresses.', 'Tell single shear from double shear in connections.', 'Size a member from an allowable stress and a factor of safety.'],
 'concepts': ['Stress is internal force per unit area. Its SI unit is the pascal (1 Pa = 1 N/m²); engineers use MPa, and 1 MPa = 1 N/mm².', 'Normal stress σ = P/A acts perpendicular to a cut; tension is positive and compression negative.',
              'Average shear stress τ = V/A acts in the plane of the cut. A pin in double shear has two cut planes, so each carries V = P/2.', 'Bearing stress σ_b = P/(td) is the contact pressure between a bolt and the hole in a plate of thickness t.',
              'Factor of safety FS = failure load/allowable load (or failure stress/allowable stress). Design keeps working stress at or below σ_allow = σ_fail/FS.'],
 'eqs': [('\\sigma=\\frac{P}{A}', 'Average normal stress'), ('\\tau_{\\text{avg}}=\\frac{V}{A}', 'Average shear stress'), ('\\sigma_b=\\frac{P}{t\\,d}', 'Bearing stress'), ('FS=\\frac{\\sigma_{\\text{fail}}}{\\sigma_{\\text{allow}}}', 'Factor of safety')],
 'worked': [
  {'q': 'A steel rod of 20 mm diameter carries a tensile load of 50 kN. Find the normal stress.', 'steps': ['A = πd²/4 = π × 20²/4 = 314.2 mm².', 'σ = P/A = 50,000 N/314.2 mm².'], 'a': '159.2 MPa (tension).'},
  {'q': 'A 12 mm pin in double shear carries a 20 kN load. Find the average shear stress in the pin.', 'steps': ['Each of the two shear planes carries V = 10 kN.', 'A = π × 12²/4 = 113.1 mm²; τ = 10,000/113.1.'], 'a': '88.4 MPa.'},
  {'q': 'A round steel hanger must carry 100 kN. The steel yields at 250 MPa and the factor of safety is 2. Find the smallest diameter.', 'steps': ['σ_allow = 250/2 = 125 MPa.', 'A = P/σ_allow = 100,000/125 = 800 mm².', 'd = √(4A/π).'], 'a': 'd = 31.9 mm (use 32 mm).'}],
 'practice': [('A 100 mm × 100 mm square post carries 200 kN in compression. Find the stress.', 'σ = 200,000/10,000 = 20 MPa (compression).'),
              ('A 10 mm bolt in single shear carries 8 kN. Find the average shear stress.', 'A = 78.54 mm²; τ = 101.9 MPa.'),
              ('The same 10 mm bolt passes through a 6 mm thick plate. Find the bearing stress.', 'σ_b = 8000/(6 × 10) = 133 MPa.'),
              ('A link fails at 90 kN and works at 30 kN. Find the factor of safety.', 'FS = 90/30 = 3.')],
 'misc': [('Stress is the same as force.', 'Stress is force per area; a thin wire and a thick bar with the same force have very different stresses.'), ('A pin in double shear carries the full load on each plane.', 'Each of the two planes carries half.'),
          ('A higher factor of safety is always better.', 'It also means heavier, costlier parts; designers choose FS from codes and the uncertainty in loads and materials.')],
 'quiz': [{'q': '1 MPa equals…', 'opts': ['1 N/m²', '1 N/mm²', '1 kN/m²', '1 N/cm²'], 'ok': 1, 'why': '10⁶ N/m² = 1 N/mm².'},
          {'q': 'A pin in double shear has how many shear planes?', 'opts': ['1', '2', '3', '4'], 'ok': 1, 'why': 'Two cut planes share the load.'},
          {'q': 'Doubling a rod’s diameter changes its axial stress (same load) by a factor of…', 'opts': ['½', '¼', '2', '4'], 'ok': 1, 'why': 'A grows with d².'},
          {'q': 'Bearing stress is…', 'opts': ['P/(td)', 'P/A of the bolt', 'V/A', 'Mc/I'], 'ok': 0, 'why': 'Contact pressure on the projected area td.'}],
 'cards': [('Normal stress', 'σ = P/A.'), ('Shear stress', 'τ = V/A.'), ('Double shear', 'Each plane carries P/2.'), ('Bearing stress', 'σ_b = P/(td).'), ('Factor of safety', 'FS = failure/allowable.'), ('MPa', '1 MPa = 1 N/mm².')],
 'planet': {'text': ['Stress limits decide which bridges trucks may cross. The ASCE Report Card for America’s Infrastructure counts 623,218 bridges in the United States, and 63,085 of them were posted for load in 2024, meaning they restrict the weight of vehicles that can safely cross, which is about 10.1% of all bridges. ASCE warns that trucks heavier than bridges were designed for threaten to overstress bridge elements and cause metal fatigue and cracking. Keeping working stress below the allowable stress, as in this unit, is how engineers rate and repair them, and preserving a bridge costs less than replacing it.'],
            'site': [('Statics', 'Statics.html')],
            'src': [_ASCE, ('OpenStax UP1, 12.3 Stress, strain and elastic modulus', _O + '12-3-stress-strain-and-elastic-modulus')]},
 'res': [('OpenStax UP1, 12.3 Stress, strain and elastic modulus', _O + '12-3-stress-strain-and-elastic-modulus', 'Free textbook section.'), (_MIT[0], _MIT[1], 'MIT lecture notes on stress.'), ('PhET: Hooke’s Law', _PH + 'hookes-law', 'Interactive.')]})
UNITS.append(
{'id': 'u2', 'title': 'Strain and Material Behavior: Hooke’s Law, Poisson’s Ratio and the Stress–Strain Curve', 'weeks': 'Week 3',
 'summary': 'Normal and shear strain, the tensile test and the stress–strain diagram, Young’s modulus, yield and ultimate strength, ductility, Poisson’s ratio, the shear modulus, strain energy and specific stiffness.',
 'objectives': ['Compute normal and shear strain from deformations.', 'Read E, yield strength, ultimate strength and ductility from a stress–strain curve.', 'Use Hooke’s law, Poisson’s ratio and G = E/(2(1 + ν)).', 'Compare materials by stiffness and strength per unit mass.'],
 'concepts': ['Normal strain ε = δ/L is a stretch per unit length (dimensionless, often in μm/m). Shear strain γ is the change in a right angle, in radians.',
              'In the linear-elastic range, Hooke’s law holds: σ = Eε and τ = Gγ. E is Young’s modulus, the slope of the stress–strain curve.',
              'Beyond the yield strength, the material deforms plastically and does not spring back; the ultimate strength is the peak engineering stress, and ductile metals neck before they break.',
              'Stretching a bar makes it thinner: lateral strain = −ν × axial strain, with Poisson’s ratio ν about 0.3 for metals. For isotropic materials G = E/(2(1 + ν)).',
              'Specific stiffness E/ρ and specific strength σ/ρ compare materials per kilogram; that is why aluminum, magnesium and carbon fiber can replace steel in light structures.'],
 'eqs': [('\\varepsilon=\\frac{\\delta}{L},\\quad \\sigma=E\\varepsilon', 'Strain and Hooke’s law'), ('\\varepsilon_{\\text{lat}}=-\\nu\\,\\varepsilon_{\\text{axial}}', 'Poisson’s ratio'), ('G=\\frac{E}{2(1+\\nu)}', 'Shear modulus'), ('u_r=\\frac{\\sigma_Y^2}{2E}', 'Modulus of resilience')],
 'worked': [
  {'q': 'A 2 m steel bar stretches 1.2 mm when the stress is 120 MPa. Find the strain and Young’s modulus.', 'steps': ['ε = 1.2/2000 = 6 × 10⁻⁴.', 'E = σ/ε = 120 MPa/0.0006.'], 'a': 'ε = 600 μm/m; E = 200 GPa.'},
  {'q': 'An aluminum alloy has E = 70 GPa and ν = 0.33. Find its shear modulus.', 'steps': ['G = E/(2(1 + ν)) = 70/2.66.'], 'a': 'G = 26.3 GPa.'},
  {'q': 'A 20 mm steel rod (ν = 0.3) has an axial strain of 0.001. How much does its diameter change?', 'steps': ['Lateral strain = −0.3 × 0.001 = −0.0003.', 'Δd = −0.0003 × 20 mm.'], 'a': 'It shrinks by 0.006 mm.'}],
 'practice': [('Typical values: steel has E = 200 GPa and ρ = 7850 kg/m³; aluminum has E = 70 GPa and ρ = 2700 kg/m³. Compare E/ρ.', 'Steel 25.5 × 10⁶ m²/s², aluminum 25.9 × 10⁶ m²/s²: almost the same stiffness per kilogram.'),
              ('A tensile specimen with a 50 mm gauge length measures 62 mm at fracture. Find the elongation at break.', '(62 − 50)/50 = 24%: a ductile metal.'),
              ('Find the modulus of resilience of steel with σ_Y = 250 MPa and E = 200 GPa.', 'u_r = 250²/(2 × 200,000) = 0.156 MPa = 156 kJ/m³.'),
              ('Sample values: a car that gets 30 mpg is made 10% lighter. Using DOE’s 6% to 8% figure, estimate its new fuel economy.', '30 × 1.06 = 31.8 to 30 × 1.08 = 32.4 mpg (sample car).')],
 'misc': [('Stronger means stiffer.', 'Strength (yield) and stiffness (E) are different; most steels share E = 200 GPa whatever their strength.'), ('Strain has units of length.', 'It is length per length, dimensionless.'),
          ('A material breaks at its yield strength.', 'Yield starts permanent deformation; ductile metals carry more load up to the ultimate strength.')],
 'quiz': [{'q': 'Young’s modulus is the slope of…', 'opts': ['load vs time', 'stress vs strain (elastic part)', 'strain vs temperature', 'force vs area'], 'ok': 1, 'why': 'σ = Eε.'},
          {'q': 'Poisson’s ratio for most metals is about…', 'opts': ['0.03', '0.3', '3', '30'], 'ok': 1, 'why': 'About 0.3.'},
          {'q': 'G for E = 200 GPa and ν = 0.25 is…', 'opts': ['50 GPa', '80 GPa', '100 GPa', '160 GPa'], 'ok': 1, 'why': '200/2.5 = 80 GPa.'},
          {'q': 'Permanent deformation starts at the…', 'opts': ['ultimate strength', 'yield strength', 'fracture point', 'proportional limit only for wood'], 'ok': 1, 'why': 'Yield.'}],
 'cards': [('Normal strain', 'ε = δ/L.'), ('Hooke’s law', 'σ = Eε, τ = Gγ.'), ('Poisson’s ratio', 'ε_lat = −νε.'), ('Shear modulus', 'G = E/(2(1 + ν)).'), ('Yield vs ultimate', 'Start of plastic flow vs peak stress.'), ('Specific stiffness', 'E/ρ.')],
 'planet': {'text': ['Choosing materials by stiffness and strength per kilogram saves fuel. The U.S. Department of Energy says a 10% reduction in vehicle weight can result in a 6% to 8% fuel economy improvement, and that replacing cast iron and traditional steel with high-strength steel, magnesium and aluminum alloys, carbon fiber and polymer composites can cut the weight of a vehicle’s body and chassis by up to 50 percent. DOE adds that lightweight materials are especially important for electric vehicles, where they offset the weight of batteries and motors and can increase all-electric range.'],
            'site': [('General Chemistry I', 'General_Chemistry_I.html')],
            'src': [_LW, ('OpenStax UP1, 12.4 Elasticity and plasticity', _O + '12-4-elasticity-and-plasticity')]},
 'res': [('OpenStax UP1, 12.3 Stress, strain and elastic modulus', _O + '12-3-stress-strain-and-elastic-modulus', 'Free textbook section.'), ('OpenStax UP1, 12.4 Elasticity and plasticity', _O + '12-4-elasticity-and-plasticity', 'Stress–strain curves.'), (_MIT[0], _MIT[1], 'MIT lectures.')]})
UNITS.append(
{'id': 'u3', 'title': 'Axially Loaded Members: Deformation, Indeterminate Bars and Thermal Stress', 'weeks': 'Week 4',
 'summary': 'Elongation of bars δ = PL/(AE), bars with several segments, statically indeterminate bars solved with compatibility, thermal strain and thermal stress, and stress concentrations.',
 'objectives': ['Compute the elongation of uniform and stepped bars.', 'Solve statically indeterminate axial problems with equilibrium plus compatibility.', 'Compute thermal expansion and the stress in a restrained bar.', 'Explain stress concentrations at holes and fillets.'],
 'concepts': ['A uniform bar under axial load stretches δ = PL/(AE). For several segments, add the δ of each: δ = Σ PᵢLᵢ/(AᵢEᵢ).', 'If equilibrium alone cannot give the forces (statically indeterminate), add a compatibility equation: how the deformations must fit together.',
              'A temperature change makes a free bar grow δ_T = αΔT L with no stress. If the bar is held, the growth is pushed back and σ = −EαΔT appears.', 'Rails, pipelines, bridges and pavements need expansion gaps or joints for this reason.',
              'Holes, notches and sharp corners raise local stress: σ_max = K σ_avg, where K is the stress concentration factor (often 2 to 3 for a small hole).'],
 'eqs': [('\\delta=\\frac{PL}{AE}', 'Axial deformation'), ('\\delta=\\sum\\frac{P_iL_i}{A_iE_i}', 'Stepped bar'), ('\\delta_T=\\alpha\\,\\Delta T\\,L', 'Thermal expansion'), ('\\sigma=-E\\alpha\\,\\Delta T', 'Fully restrained bar')],
 'worked': [
  {'q': 'A 3 m steel rod (E = 200 GPa) with A = 500 mm² carries 60 kN. Find its elongation.', 'steps': ['δ = PL/(AE) = 60,000 × 3000/(500 × 200,000) in N and mm.'], 'a': '1.8 mm.'},
  {'q': 'A steel bar (E = 200 GPa, α = 12 × 10⁻⁶/°C) is fixed between two rigid walls and heated by 40 °C. Find the stress.', 'steps': ['Free growth would be αΔT L; the walls push it back.', 'σ = −EαΔT = −200,000 × 12 × 10⁻⁶ × 40 MPa.'], 'a': '96 MPa compression.'},
  {'q': 'A uniform bar fixed at both ends carries an axial load P = 30 kN at a point 1 m from end A and 2 m from end B. Find both wall reactions.', 'steps': ['Equilibrium: R_A + R_B = 30 kN.', 'Compatibility: the stretch of segment A equals the shortening of segment B, so R_A × 1 = R_B × 2.'], 'a': 'R_A = 20 kN, R_B = 10 kN.'}],
 'practice': [('A 25 m steel rail warms by 30 °C with nothing holding it. How much does it grow?', 'δ = 12 × 10⁻⁶ × 30 × 25,000 = 9 mm.'),
              ('A bar has an aluminum segment (E = 70 GPa, A = 400 mm², L = 1 m) and a steel segment (A = 200 mm², L = 0.5 m) in series, carrying 20 kN. Find the total stretch.', '0.714 + 0.250 = 0.964 mm.'),
              ('Find the strain in aluminum at 100 MPa (E = 70 GPa).', 'ε = 100/70,000 = 1.43 × 10⁻³.'),
              ('DOE says land-based hub heights reached about 103.4 m in 2023 after growing 83% since 1998–1999. What was the earlier average?', '103.4/1.83 = 56.5 m.')],
 'misc': [('Thermal expansion always causes stress.', 'Only when the expansion is restrained.'), ('An indeterminate bar can be solved with equilibrium alone.', 'You need compatibility (deformation) equations too.'),
          ('A small hole barely matters.', 'It can triple the local stress, which is where fatigue cracks start.')],
 'quiz': [{'q': 'Doubling the length of a bar (same load and area) makes δ…', 'opts': ['half', 'the same', 'double', 'four times'], 'ok': 2, 'why': 'δ ∝ L.'},
          {'q': 'A restrained bar that is heated is in…', 'opts': ['tension', 'compression', 'no stress', 'shear only'], 'ok': 1, 'why': 'The supports push back.'},
          {'q': 'Statically indeterminate problems need…', 'opts': ['only equilibrium', 'compatibility of deformations', 'dynamics', 'no free-body diagram'], 'ok': 1, 'why': 'More unknowns than equilibrium equations.'},
          {'q': 'Thermal stress in a fully restrained bar does not depend on…', 'opts': ['E', 'α', 'ΔT', 'its length'], 'ok': 3, 'why': 'σ = −EαΔT.'}],
 'cards': [('Axial deformation', 'δ = PL/(AE).'), ('Stepped bar', 'Add PL/(AE) for each segment.'), ('Compatibility', 'Deformations must fit together.'), ('Thermal strain', 'αΔT.'), ('Thermal stress', 'σ = −EαΔT if fully held.'), ('Stress concentration', 'σ_max = Kσ_avg.')],
 'planet': {'text': ['Taller wind turbines catch stronger wind but need taller towers. The U.S. Department of Energy reports that the hub height of utility-scale land-based turbines grew 83% since 1998–1999 to about 103.4 meters in 2023, taller than the Statue of Liberty, and that offshore hub heights are projected to reach about 150 meters by 2035. Winds are generally stronger higher up. DOE notes tower diameters are hard to truck under bridges, so it supports towers built on site, including spiral welding to minimize costly steel. Each tower is an axially loaded column that must carry the weight above it within its allowable stress.'],
            'site': [('Physics II', 'Physics_II.html')],
            'src': [_BIG, ('OpenStax UP2, 1.3 Thermal expansion', _O2 + '1-3-thermal-expansion')]},
 'res': [('OpenStax UP2, 1.3 Thermal expansion', _O2 + '1-3-thermal-expansion', 'Free textbook section.'), ('OpenStax UP1, 12.3 Stress, strain and elastic modulus', _O + '12-3-stress-strain-and-elastic-modulus', 'Axial deformation.'), (_MIT[0], _MIT[1], 'MIT lectures.')]})
UNITS.append(
{'id': 'u4', 'title': 'Torsion of Circular Shafts and Power Transmission', 'weeks': 'Weeks 5–6',
 'summary': 'Shear strain and stress in twisted circular shafts, the polar moment of inertia for solid and hollow shafts, angle of twist, power and torque, shaft design, and statically indeterminate shafts.',
 'objectives': ['Compute shear stress with τ = Tρ/J.', 'Compute the angle of twist φ = TL/(GJ).', 'Convert power and speed to torque with P = Tω.', 'Size solid and hollow shafts and explain why hollow shafts save material.'],
 'concepts': ['In a twisted circular shaft, plane sections stay plane and shear strain grows linearly from the center: γ = ρφ/L.', 'Shear stress is τ = Tρ/J, largest at the outer surface: τ_max = Tc/J.',
              'Polar moment of inertia: J = πd⁴/32 for a solid shaft and J = π(d_o⁴ − d_i⁴)/32 for a hollow one.', 'Angle of twist φ = TL/(GJ) in radians; for several segments, add them.',
              'Power P = Tω. Slow shafts carry huge torques for the same power, which is why a gearbox speeds up a wind turbine’s rotation before the generator.'],
 'eqs': [('\\tau=\\frac{T\\rho}{J},\\quad \\tau_{\\max}=\\frac{Tc}{J}', 'Torsion formula'), ('J=\\frac{\\pi d^4}{32},\\quad J=\\frac{\\pi(d_o^4-d_i^4)}{32}', 'Polar moment of inertia'), ('\\phi=\\frac{TL}{GJ}', 'Angle of twist'), ('P=T\\omega', 'Power')],
 'worked': [
  {'q': 'A solid 50 mm steel shaft carries a torque of 1.5 kN·m. Find the maximum shear stress.', 'steps': ['J = π × 0.05⁴/32 = 6.136 × 10⁻⁷ m⁴.', 'τ_max = Tc/J = 1500 × 0.025/6.136 × 10⁻⁷.'], 'a': '61.1 MPa.'},
  {'q': 'The same shaft is 2 m long with G = 80 GPa. Find the angle of twist.', 'steps': ['φ = TL/(GJ) = 1500 × 2/(80 × 10⁹ × 6.136 × 10⁻⁷).'], 'a': '0.0611 rad = 3.50°.'},
  {'q': 'A motor delivers 50 kW at 1,500 rpm. Size a solid shaft for an allowable shear stress of 40 MPa.', 'steps': ['ω = 1500 × 2π/60 = 157.1 rad/s; T = P/ω = 318.3 N·m.', 'τ = 16T/(πd³) gives d = (16T/(πτ))^(1/3).'], 'a': 'd = 34.3 mm (use 35 mm).'}],
 'practice': [('A hollow shaft (d_o = 60 mm, d_i = 40 mm) carries 2 kN·m. Find τ_max.', 'J = 1.021 × 10⁻⁶ m⁴; τ = 2000 × 0.03/J = 58.8 MPa.'),
              ('Compare that hollow shaft with a solid 60 mm shaft: what fraction of the material and of the stiffness J does it keep?', 'Area 1 − (40/60)² = 55.6%; J 1 − (40/60)⁴ = 80.2%.'),
              ('A solid 30 mm shaft carries 500 N·m. Find τ_max.', 'τ = 16T/(πd³) = 94.3 MPa.'),
              ('Sample values: a 3.4 MW wind turbine rotor turns at a sample 12 rpm. Find the torque on its main shaft.', 'ω = 1.257 rad/s; T = P/ω = 2.71 MN·m (sample speed).')],
 'misc': [('Shear stress is uniform across a shaft.', 'It is zero at the center and largest at the surface.'), ('Torque and power are the same.', 'P = Tω: the same power at low speed needs much more torque.'),
          ('A hollow shaft is much weaker.', 'Material near the center carries little stress; removing it saves weight for a small loss in J.')],
 'quiz': [{'q': 'In a solid shaft, maximum shear stress occurs…', 'opts': ['at the center', 'at the outer surface', 'halfway out', 'everywhere equally'], 'ok': 1, 'why': 'τ ∝ ρ.'},
          {'q': 'Doubling a solid shaft’s diameter multiplies J by…', 'opts': ['2', '4', '8', '16'], 'ok': 3, 'why': 'J ∝ d⁴.'},
          {'q': 'Angle of twist is proportional to…', 'opts': ['G', 'J', 'L', '1/L'], 'ok': 2, 'why': 'φ = TL/(GJ).'},
          {'q': 'A gearbox that speeds up a shaft 100 times (no losses) changes torque by a factor of…', 'opts': ['100', '1/100', '1', '10'], 'ok': 1, 'why': 'P = Tω is constant.'}],
 'cards': [('Torsion formula', 'τ = Tρ/J.'), ('Solid J', 'πd⁴/32.'), ('Hollow J', 'π(d_o⁴ − d_i⁴)/32.'), ('Angle of twist', 'φ = TL/(GJ).'), ('Power', 'P = Tω.'), ('Shaft sizing', 'd = (16T/(πτ))^(1/3).')],
 'planet': {'text': ['A wind turbine sends its power through a twisted shaft. The U.S. Department of Energy explains that the rotor connects to the generator either directly, in a direct-drive turbine, or through a shaft and a series of gears that speed up the rotation and allow a physically smaller generator. DOE also reports that the average capacity of newly installed U.S. wind turbines reached 3.4 MW in 2023. Because power is torque times speed, a slow, large rotor puts millions of newton-meters on its main shaft, and the torsion formulas of this unit size it.'],
            'site': [('Dynamics', 'Dynamics.html')],
            'src': [_WIND, _BIG]},
 'res': [(_MIT[0], _MIT[1], 'MIT lectures on torsion.'), ('OpenStax UP1, 10.6 Torque', _O + '10-6-torque', 'Free textbook section on torque.'), ('PhET: Torque', _PH + 'torque', 'Interactive.')]})
UNITS.append(
{'id': 'u5', 'title': 'Shear and Moment Diagrams and Bending Stress', 'weeks': 'Weeks 7–8',
 'summary': 'Internal shear and bending moment in beams, the relations dV/dx = −w and dM/dx = V, shear and moment diagrams, the flexure formula σ = My/I, the section modulus and efficient beam shapes.',
 'objectives': ['Draw shear and moment diagrams for common loads.', 'Use dV/dx = −w and dM/dx = V to check diagrams.', 'Compute bending stress with σ = My/I.', 'Choose efficient cross-sections using the section modulus S = I/c.'],
 'concepts': ['Cut a beam and the internal shear V and moment M hold the piece in equilibrium. Slopes follow dV/dx = −w and dM/dx = V, so M is largest where V crosses zero.',
              'Pure bending keeps plane sections plane; strain and stress grow linearly from the neutral axis, which passes through the centroid.',
              'The flexure formula is σ = −My/I; the largest stress is σ_max = Mc/I = M/S, where S = I/c is the section modulus.',
              'For a rectangle, I = bh³/12, so depth matters much more than width: a plank on edge is far stiffer and stronger than one lying flat.',
              'I-beams and hollow tubes put material far from the neutral axis, giving a large I for little mass.'],
 'eqs': [('\\frac{dV}{dx}=-w,\\quad \\frac{dM}{dx}=V', 'Load, shear and moment'), ('\\sigma=-\\frac{My}{I},\\quad \\sigma_{\\max}=\\frac{Mc}{I}=\\frac{M}{S}', 'Flexure formula'), ('I=\\frac{bh^3}{12},\\quad I=\\frac{\\pi d^4}{64}', 'Rectangle and circle'),
         ('M_{\\max}=\\frac{PL}{4},\\quad M_{\\max}=\\frac{wL^2}{8}', 'Simply supported: center load, uniform load')],
 'worked': [
  {'q': 'A simply supported 4 m beam carries a 10 kN load at midspan. Find the reactions and the maximum moment.', 'steps': ['By symmetry each reaction is 5 kN; V = ±5 kN.', 'M_max = PL/4 at midspan.'], 'a': '10 kN·m.'},
  {'q': 'The beam is a 100 mm wide × 200 mm deep rectangle. Find the maximum bending stress.', 'steps': ['I = 0.1 × 0.2³/12 = 6.667 × 10⁻⁵ m⁴; c = 0.1 m.', 'σ = Mc/I = 10,000 × 0.1/6.667 × 10⁻⁵.'], 'a': '15 MPa (tension at the bottom, compression at the top).'},
  {'q': 'A simply supported 6 m beam carries 5 kN/m along its length. Find V_max and M_max.', 'steps': ['Reactions wL/2 = 15 kN each.', 'M_max = wL²/8 at midspan, where V = 0.'], 'a': 'V_max = 15 kN; M_max = 22.5 kN·m.'}],
 'practice': [('A 2 m cantilever carries 3 kN at its tip. Find the largest moment and where it acts.', 'M = 3 × 2 = 6 kN·m at the wall.'),
              ('A 200 mm × 50 mm plank is used on edge instead of flat. By what factor does I grow?', '(200/50)² = 16 times.'),
              ('A solid 40 mm circular rod carries M = 500 N·m. Find σ_max.', 'σ = 32M/(πd³) = 79.6 MPa.'),
              ('Sample values: NREL’s test center can apply 84 MN·m to a blade root. If a root section had a sample S = 0.4 m³, what bending stress would that cause?', 'σ = M/S = 84/0.4 = 210 MPa (sample section).')],
 'misc': [('Maximum moment is always under the biggest load.', 'It is where V crosses zero, which may be elsewhere.'), ('Bending stress is uniform across the section.', 'It is zero at the neutral axis and largest at the top and bottom.'),
          ('Width and depth help equally.', 'I grows with h³ but only with b.')],
 'quiz': [{'q': 'dM/dx equals…', 'opts': ['w', 'V', 'σ', 'EI'], 'ok': 1, 'why': 'Slope of the moment diagram is the shear.'},
          {'q': 'The neutral axis passes through the…', 'opts': ['top fiber', 'centroid', 'support', 'shear center always'], 'ok': 1, 'why': 'For pure bending of a linear-elastic beam.'},
          {'q': 'Doubling a rectangular beam’s depth multiplies I by…', 'opts': ['2', '4', '8', '16'], 'ok': 2, 'why': 'h³.'},
          {'q': 'M_max for a simply supported beam with uniform load w is…', 'opts': ['wL/2', 'wL²/8', 'wL²/2', 'PL/4'], 'ok': 1, 'why': 'Standard result.'}],
 'cards': [('Shear–moment', 'dM/dx = V; dV/dx = −w.'), ('Flexure formula', 'σ = My/I.'), ('Section modulus', 'S = I/c; σ = M/S.'), ('Rectangle I', 'bh³/12.'), ('Center load', 'M_max = PL/4.'), ('Uniform load', 'M_max = wL²/8.')],
 'planet': {'text': ['Wind turbine blades are huge cantilever beams, and they are bent on purpose before they fly. NREL’s fact sheet on the Wind Technology Testing Center in Boston, built with the U.S. Department of Energy and the Massachusetts Clean Energy Center, describes the only U.S. facility then able to test blades up to 90 meters long. Static tests pull blades horizontally and vertically to measure deflection and strains, applying up to an 84 meganewton-meter bending moment. The flexure formula of this unit turns that moment into the stress that decides whether a blade passes certification.'],
            'site': [('Statics', 'Statics.html')],
            'src': [_WTTC]},
 'res': [(_MIT[0], _MIT[1], 'MIT lectures on beams.'), ('OpenStax UP1, 12.2 Examples of static equilibrium', _O + '12-2-examples-of-static-equilibrium', 'Free textbook section on equilibrium.'), ('PhET: Balancing Act', _PH + 'balancing-act', 'Moments, interactive.')]})
UNITS.append(
{'id': 'u6', 'title': 'Transverse Shear in Beams, Shear Flow and Composite Sections', 'weeks': 'Week 9',
 'summary': 'Shear stress from transverse loads, the shear formula τ = VQ/(It), shear stress in rectangular and circular sections, shear flow in built-up and glued beams, fastener spacing, and beams of two materials.',
 'objectives': ['Compute Q and the shear stress τ = VQ/(It).', 'Use τ_max = 1.5V/A for rectangles and 4V/(3A) for circles.', 'Find shear flow q = VQ/I and the spacing of nails, bolts or glue strength in built-up beams.', 'Explain how layered beams act together.'],
 'concepts': ['A beam with changing moment also carries shear stress on horizontal planes; that is why a stack of loose boards slides and bends much more than one glued block.',
              'The shear formula τ = VQ/(It) uses Q = A′ȳ′, the first moment about the neutral axis of the area beyond the cut.', 'In a rectangle the shear stress is parabolic, zero at the top and bottom and 1.5V/A at the neutral axis.',
              'Shear flow q = VQ/I is the force per unit length that a glue line or a row of fasteners must carry; fastener spacing s = F_fastener/q.', 'In most long beams bending stress governs; in short, deep beams and in wood, shear can govern.'],
 'eqs': [('\\tau=\\frac{VQ}{It},\\quad Q=A\'\\bar y\'', 'Shear formula'), ('\\tau_{\\max}=\\frac{3V}{2A}', 'Rectangle'), ('\\tau_{\\max}=\\frac{4V}{3A}', 'Solid circle'), ('q=\\frac{VQ}{I},\\quad s=\\frac{F}{q}', 'Shear flow and fastener spacing')],
 'worked': [
  {'q': 'A 100 mm × 200 mm rectangular beam carries V = 15 kN. Find the maximum shear stress.', 'steps': ['A = 0.02 m².', 'τ_max = 1.5V/A = 1.5 × 15,000/0.02.'], 'a': '1.125 MPa at the neutral axis.'},
  {'q': 'Two 150 mm × 50 mm boards are glued flat on top of each other to make a 150 mm wide × 100 mm deep beam carrying V = 10 kN. Find the shear stress the glue must carry.', 'steps': ['I = 0.15 × 0.1³/12 = 1.25 × 10⁻⁵ m⁴.', 'Q = 0.15 × 0.05 × 0.025 = 1.875 × 10⁻⁴ m³.', 'q = VQ/I = 150 N/mm; τ = q/b = 150/150.'], 'a': 'τ = 1.0 MPa (the same as 1.5V/A).'},
  {'q': 'The same two boards are nailed instead, under V = 2 kN, and each nail can carry 900 N. Find the nail spacing.', 'steps': ['q = VQ/I = 2000 × 1.875 × 10⁻⁴/1.25 × 10⁻⁵ = 30 N/mm.', 's = F/q = 900/30.'], 'a': '30 mm.'}],
 'practice': [('A solid 50 mm shaft carries V = 10 kN. Find τ_max.', 'A = 1963 mm²; τ = 4V/(3A) = 6.79 MPa.'),
              ('A 50 mm × 100 mm rectangle carries V = 5 kN. Find τ_max.', '1.5 × 5000/5000 = 1.5 MPa.'),
              ('For a simply supported rectangular beam with a center load, show that σ_max/τ_max = 2L/h, and evaluate it for L/h = 10.', 'σ = 1.5PL/(bh²), τ = 0.75P/(bh), ratio 2L/h = 20: bending governs long beams.'),
              ('Sample values: a mid-rise building’s materials carry 1,000 t CO₂e of embodied emissions. Using the 13% to 26.5% range from the Forest Service paper, estimate the saving with mass timber.', '130 to 265 t CO₂e (sample building).')],
 'misc': [('Shear stress is largest at the top and bottom, like bending stress.', 'It is zero there and largest at the neutral axis.'), ('Q is the moment of inertia.', 'Q is a first moment of area (m³); I is a second moment (m⁴).'),
          ('Glue only has to hold the boards together vertically.', 'It must carry the horizontal shear flow q.')],
 'quiz': [{'q': 'For a rectangle, τ_max is…', 'opts': ['V/A', '1.5V/A', '2V/A', '4V/(3A)'], 'ok': 1, 'why': 'Parabolic distribution.'},
          {'q': 'Shear flow has units of…', 'opts': ['N/m²', 'N/m', 'N·m', 'm³'], 'ok': 1, 'why': 'Force per length.'},
          {'q': 'Q is…', 'opts': ['A′ȳ′', 'bh³/12', 'VQ/I', 'Mc/I'], 'ok': 0, 'why': 'First moment of the area beyond the cut.'},
          {'q': 'Halving the nail spacing lets the beam carry how much more shear?', 'opts': ['the same', 'twice', 'four times', 'half'], 'ok': 1, 'why': 'q = F/s doubles.'}],
 'cards': [('Shear formula', 'τ = VQ/(It).'), ('First moment Q', 'A′ȳ′ beyond the cut.'), ('Rectangle', 'τ_max = 1.5V/A.'), ('Circle', 'τ_max = 4V/(3A).'), ('Shear flow', 'q = VQ/I.'), ('Fastener spacing', 's = F/q.')],
 'planet': {'text': ['Glued wood layers that carry shear flow are building a lower-carbon skyline. A 2022 paper published through the USDA Forest Service’s Forest Products Laboratory explains that cross-laminated timber is at the forefront of the mass timber movement, which lets designers build taller wood buildings, and that several studies show substituting mass timber for steel and concrete in mid-rise buildings can reduce the emissions from manufacturing, transporting and installing building materials by 13% to 26.5%. The authors also stress safeguards so that more demand for wood does not harm forest carbon and health. The glue lines between layers must carry the shear flow from this unit.'],
            'site': [('Forests', 'Deforestation.html')],
            'src': [_MT]},
 'res': [(_MIT[0], _MIT[1], 'MIT lectures on beams.'), ('OpenStax UP1, 12.3 Stress, strain and elastic modulus', _O + '12-3-stress-strain-and-elastic-modulus', 'Shear stress and shear modulus.')]})
UNITS.append(
{'id': 'u7', 'title': 'Stress Transformation, Mohr’s Circle, Failure Theories and Fatigue', 'weeks': 'Week 10',
 'summary': 'Plane stress on rotated planes, principal stresses and maximum shear, Mohr’s circle, the Tresca and von Mises yield criteria, and an introduction to fatigue under repeated loading.',
 'objectives': ['Transform plane stress to any angle and find principal stresses and planes.', 'Draw and use Mohr’s circle.', 'Apply the Tresca and von Mises criteria to find a factor of safety.', 'Explain fatigue and why parts can fail far below their static strength.'],
 'concepts': ['The same stress state looks different on different planes. Rotating by θ changes σ and τ, but some planes have zero shear: the principal planes.',
              'Principal stresses are σ₁,₂ = (σx + σy)/2 ± R, with R = √(((σx − σy)/2)² + τxy²). The maximum in-plane shear is R, on planes 45° from the principal planes.',
              'Mohr’s circle plots (σ, τ) for every plane: center at (σx + σy)/2, radius R. An angle θ on the element is 2θ on the circle.',
              'Ductile metals yield by shear. Tresca: the largest shear stress reaches σ_Y/2. Von Mises: σ_vm = √(σ₁² − σ₁σ₂ + σ₂²) reaches σ_Y (it fits test data a little better).',
              'Repeated loading grows cracks from small flaws, so parts can break after millions of cycles at stresses well below yield. Designers use S–N curves and test full parts for their lifetime of cycles.'],
 'eqs': [('\\sigma_{1,2}=\\frac{\\sigma_x+\\sigma_y}{2}\\pm\\sqrt{\\left(\\frac{\\sigma_x-\\sigma_y}{2}\\right)^2+\\tau_{xy}^2}', 'Principal stresses'), ('\\tan2\\theta_p=\\frac{2\\tau_{xy}}{\\sigma_x-\\sigma_y}', 'Principal angle'),
         ('\\sigma_{vm}=\\sqrt{\\sigma_1^2-\\sigma_1\\sigma_2+\\sigma_2^2}', 'Von Mises (plane stress)'), ('\\sigma_{vm}=\\sqrt{\\sigma^2+3\\tau^2}', 'Normal plus shear (shafts, beams)')],
 'worked': [
  {'q': 'A point has σx = 80 MPa, σy = −40 MPa and τxy = 30 MPa. Find the principal stresses, the principal angle and the maximum in-plane shear.', 'steps': ['Center = 20 MPa; R = √(60² + 30²) = 67.1 MPa.', 'σ₁ = 20 + 67.1; σ₂ = 20 − 67.1.', 'tan 2θ_p = 60/120 = 0.5.'], 'a': 'σ₁ = 87.1 MPa, σ₂ = −47.1 MPa, θ_p = 13.3°, τ_max = 67.1 MPa.'},
  {'q': 'For that stress state, find the von Mises stress and the factor of safety for steel with σ_Y = 250 MPa.', 'steps': ['σ_vm = √(87.1² − (87.1)(−47.1) + 47.1²).', 'FS = 250/σ_vm.'], 'a': 'σ_vm = 117.9 MPa; FS = 2.12.'},
  {'q': 'Use Tresca for the same point.', 'steps': ['σ₁ and σ₂ have opposite signs, so τ_abs max = (σ₁ − σ₂)/2 = 67.1 MPa.', 'FS = (σ_Y/2)/τ_max = 125/67.1.'], 'a': 'FS = 1.86 (Tresca is a little more conservative).'}],
 'practice': [('A shaft surface is in pure shear, τ = 50 MPa. Find the principal stresses and their planes.', 'σ₁ = 50 MPa, σ₂ = −50 MPa, on planes at 45°.'),
              ('A bar is in uniaxial tension at 100 MPa. Find the maximum shear stress and its plane.', 'τ_max = 50 MPa on planes at 45°.'),
              ('A shaft carries σ = 60 MPa from bending and τ = 40 MPa from torsion. Find the von Mises stress.', 'σ_vm = √(60² + 3 × 40²) = 91.7 MPa.'),
              ('Sample values: a part cycles once per second for 20 years. How many load cycles is that?', '20 × 365.25 × 86,400 = 6.31 × 10⁸ cycles.')],
 'misc': [('The largest stress is always σx or σy.', 'Principal stresses on rotated planes can be larger.'), ('An angle θ on the element is θ on Mohr’s circle.', 'It is 2θ on the circle.'),
          ('If a part survives one load, it survives that load forever.', 'Repeated loads can grow fatigue cracks far below the static strength.')],
 'quiz': [{'q': 'On principal planes the shear stress is…', 'opts': ['maximum', 'zero', 'equal to σ₁', 'R'], 'ok': 1, 'why': 'Definition.'},
          {'q': 'Maximum in-plane shear planes are at what angle from principal planes?', 'opts': ['30°', '45°', '60°', '90°'], 'ok': 1, 'why': '90° on the circle.'},
          {'q': 'Von Mises for uniaxial stress σ equals…', 'opts': ['σ/2', 'σ', '√3σ', '2σ'], 'ok': 1, 'why': 'σ₂ = 0.'},
          {'q': 'Fatigue failure is driven by…', 'opts': ['one large load', 'repeated cycles of load', 'temperature alone', 'color'], 'ok': 1, 'why': 'Cracks grow cycle by cycle.'}],
 'cards': [('Principal stresses', 'Center ± R.'), ('Mohr’s circle radius', 'R = √(((σx − σy)/2)² + τ²).'), ('Max in-plane shear', 'τ_max = R, at 45°.'), ('Tresca', 'τ_max = σ_Y/2 at yield.'), ('Von Mises', '√(σ₁² − σ₁σ₂ + σ₂²).'), ('Fatigue', 'Failure after many cycles below yield.')],
 'planet': {'text': ['A wind turbine blade must survive decades of bending back and forth. NREL’s fact sheet on the Wind Technology Testing Center explains that fatigue tests cycle blades millions of times to simulate what a blade goes through in its lifetime on a turbine, using NREL’s resonant excitation system with up to 21 meters of tip-to-tip motion to generate 20-plus years of cyclic field loads in a matter of months. Combined stress, failure theories and fatigue, all in this unit, decide whether a blade passes.'],
            'site': [('Statics', 'Statics.html')],
            'src': [_WTTC]},
 'res': [(_MIT[0], _MIT[1], 'MIT lectures on stress transformation.'), (_MIT2[0], _MIT2[1], 'MIT lectures on yield, fracture and fatigue.')]})
UNITS.append(
{'id': 'u8', 'title': 'Thin-Walled Pressure Vessels and Combined Loading', 'weeks': 'Week 11',
 'summary': 'Hoop and axial stress in thin cylinders, stress in thin spheres, required wall thickness, and combining axial, bending, torsion and pressure stresses at a point.',
 'objectives': ['Compute hoop and axial stress in thin-walled cylinders and spheres.', 'Find the required wall thickness for a pressure and allowable stress.', 'Superpose axial, bending, torsion and pressure stresses at a point.', 'Find principal and von Mises stresses for combined loads.'],
 'concepts': ['A vessel is thin-walled when r/t is about 10 or more; then the wall stress is nearly uniform through the thickness.', 'Cylinder: hoop stress σ_h = pr/t, axial stress σ_a = pr/(2t). The hoop stress is twice the axial, so overpressured pipes split lengthwise.',
              'Sphere: σ = pr/(2t) in every direction, so a sphere needs half the wall of a cylinder of the same radius.', 'Under combined loads, add the stresses from each load at a point (superposition), then use Mohr’s circle or a failure criterion.',
              'Units matter: 1 bar = 0.1 MPa and 1 psi = 6894.757 Pa (NIST).'],
 'eqs': [('\\sigma_h=\\frac{pr}{t},\\quad \\sigma_a=\\frac{pr}{2t}', 'Thin cylinder'), ('\\sigma=\\frac{pr}{2t}', 'Thin sphere'), ('\\sigma=\\frac{P}{A}\\pm\\frac{Mc}{I}', 'Axial plus bending'), ('t=\\frac{pr}{\\sigma_{\\text{allow}}}', 'Required cylinder wall')],
 'worked': [
  {'q': 'Sample values: a hydrogen cylinder with inner radius 150 mm and wall 15 mm holds 700 bar (70 MPa). Find the hoop and axial stresses.', 'steps': ['r/t = 10, thin-wall estimate.', 'σ_h = pr/t = 70 × 10; σ_a = σ_h/2.'], 'a': 'σ_h = 700 MPa, σ_a = 350 MPa (sample tank, which is why such tanks use carbon-fiber composite).'},
  {'q': 'A sphere with the same radius, wall and pressure: find the stress.', 'steps': ['σ = pr/(2t).'], 'a': '350 MPa, half the cylinder’s hoop stress.'},
  {'q': 'A solid 100 mm post carries a 10 kN compressive load and a 3 kN·m bending moment. Find the largest compressive and tensile stresses.', 'steps': ['P/A = 10,000/7854 mm² = 1.27 MPa compression.', 'Mc/I = 32M/(πd³) = 30.6 MPa.'], 'a': '31.8 MPa compression on one face; 29.3 MPa tension on the other.'}],
 'practice': [('A tank design is changed from 350 bar to 700 bar at the same radius and allowable stress. How must the wall thickness change?', 't = pr/σ: it doubles.'),
              ('Sample values: a gas cylinder has r = 150 mm, t = 3 mm and p = 2 MPa. Find σ_h and σ_a.', 'σ_h = 100 MPa; σ_a = 50 MPa.'),
              ('Find the wall thickness of a cylinder with p = 35 MPa, r = 200 mm and σ_allow = 600 MPa.', 't = 35 × 200/600 = 11.7 mm.'),
              ('Convert DOE’s 10,000 psi to MPa with NIST’s factor.', '10,000 × 6894.757 Pa = 68.9 MPa, about 700 bar.')],
 'misc': [('Hoop and axial stresses are equal in a cylinder.', 'Hoop stress is twice the axial stress.'), ('Thin-wall formulas work for any vessel.', 'Only when r/t is about 10 or more.'),
          ('You can add stresses from different loads on different points.', 'Superpose at the same point and the same direction.')],
 'quiz': [{'q': 'Hoop stress in a thin cylinder is…', 'opts': ['pr/(2t)', 'pr/t', 'pt/r', '2pr/t'], 'ok': 1, 'why': 'Equilibrium of a half-ring.'},
          {'q': 'A sphere’s wall stress compared with a cylinder’s hoop stress (same p, r, t) is…', 'opts': ['twice', 'equal', 'half', 'a quarter'], 'ok': 2, 'why': 'pr/(2t).'},
          {'q': 'An overpressured pipe usually splits…', 'opts': ['around its circumference', 'lengthwise', 'at the ends only', 'never'], 'ok': 1, 'why': 'Hoop stress is largest.'},
          {'q': '700 bar is about…', 'opts': ['7 MPa', '70 MPa', '700 MPa', '0.7 MPa'], 'ok': 1, 'why': '1 bar = 0.1 MPa.'}],
 'cards': [('Hoop stress', 'σ_h = pr/t.'), ('Axial stress', 'σ_a = pr/(2t).'), ('Sphere', 'σ = pr/(2t).'), ('Thin wall', 'r/t ≳ 10.'), ('Superposition', 'Add stresses at a point.'), ('bar and psi', '1 bar = 0.1 MPa; 1 psi = 6894.757 Pa.')],
 'planet': {'text': ['Hydrogen can power trucks, buses and industry without carbon emissions at the point of use, but it has to be stored. The U.S. Department of Energy explains that hydrogen has the highest energy per mass of any fuel but very low energy per volume, so storing it as a gas typically requires high-pressure tanks at 350–700 bar (5,000–10,000 psi), while storing it as a liquid requires cryogenic temperatures because it boils at −252.8 °C at ambient pressure. The hoop-stress formula of this unit shows why those tanks need very strong, light walls.'],
            'site': [('General Chemistry I', 'General_Chemistry_I.html')],
            'src': [_H2, CONST_SRC]},
 'res': [(_MIT[0], _MIT[1], 'MIT lectures on pressure vessels.'), (_MIT2[0], _MIT2[1], 'MIT follow-on course.')]})
UNITS.append(
{'id': 'u9', 'title': 'Deflection of Beams', 'weeks': 'Weeks 12–13',
 'summary': 'The elastic curve and EI v″ = M, integration with boundary conditions, standard deflection formulas, superposition, serviceability limits and statically indeterminate beams.',
 'objectives': ['Integrate EI v″ = M with boundary conditions to find slope and deflection.', 'Use standard deflection formulas and superposition.', 'Check deflection against a serviceability limit such as L/360.', 'Solve propped cantilevers and other indeterminate beams.'],
 'concepts': ['For small slopes, the elastic curve obeys EI d²v/dx² = M(x). Integrate twice and use the supports to fix the constants (v = 0 at pins; v = 0 and v′ = 0 at a fixed end).',
              'EI is the flexural rigidity: stiffer material (E) or a deeper section (I) gives smaller deflections.', 'Standard results: cantilever with tip load δ = PL³/(3EI); simply supported with center load PL³/(48EI); with uniform load 5wL⁴/(384EI).',
              'Deflections from separate loads add (superposition) while the beam stays linear-elastic.', 'An extra support makes the beam indeterminate; remove it, compute the deflection there, and choose the reaction that cancels it.'],
 'eqs': [('EI\\frac{d^2v}{dx^2}=M(x)', 'Elastic curve'), ('\\delta=\\frac{PL^3}{3EI},\\quad \\delta=\\frac{wL^4}{8EI}', 'Cantilever: tip load, uniform load'),
         ('\\delta=\\frac{PL^3}{48EI},\\quad \\delta=\\frac{5wL^4}{384EI}', 'Simply supported: center load, uniform load'), ('R_B=\\frac{3wL}{8}', 'Propped cantilever, uniform load')],
 'worked': [
  {'q': 'A 2 m steel cantilever (E = 200 GPa, I = 8 × 10⁻⁶ m⁴) carries 1 kN at its tip. Find the tip deflection.', 'steps': ['δ = PL³/(3EI) = 1000 × 8/(3 × 200 × 10⁹ × 8 × 10⁻⁶).'], 'a': '1.67 mm.'},
  {'q': 'A simply supported 6 m steel beam (I = 1 × 10⁻⁴ m⁴) carries 10 kN/m. Find the midspan deflection and compare with L/360.', 'steps': ['δ = 5wL⁴/(384EI) = 5 × 10,000 × 1296/(384 × 200 × 10⁹ × 10⁻⁴).', 'L/360 = 16.7 mm.'], 'a': '8.44 mm, within the limit.'},
  {'q': 'The same beam is fixed at A and propped at B. Find the prop reaction.', 'steps': ['Remove the prop: cantilever tip deflection wL⁴/(8EI).', 'The prop force R_B gives R_BL³/(3EI) upward; set them equal.'], 'a': 'R_B = 3wL/8 = 22.5 kN.'}],
 'practice': [('A cantilever’s length is doubled with the same tip load. By what factor does the tip deflection grow?', '2³ = 8 times.'),
              ('A simply supported wood beam (E = 10 GPa, I = 5 × 10⁻⁵ m⁴, L = 4 m) carries 5 kN at midspan. Find δ.', 'PL³/(48EI) = 13.3 mm.'),
              ('A 3 m steel cantilever (I = 1 × 10⁻⁵ m⁴) carries 2 kN/m. Find the tip deflection.', 'wL⁴/(8EI) = 10.1 mm.'),
              ('DOE says rotor swept areas have grown about 670% since 1998–1999. If swept area grows as diameter squared, by what factor did the average diameter grow?', 'Swept area ×7.7, so diameter × √7.7 = 2.77.')],
 'misc': [('Deflection grows in step with length.', 'It grows with L³ or L⁴.'), ('A stronger steel deflects less.', 'Deflection depends on E, which is about the same for all steels.'),
          ('If a beam is strong enough, it is good enough.', 'It must also be stiff enough: floors that bounce or blades that hit the tower fail in service.')],
 'quiz': [{'q': 'Tip deflection of a cantilever with an end load:', 'opts': ['PL³/(3EI)', 'PL³/(48EI)', 'PL²/(2EI)', '5wL⁴/(384EI)'], 'ok': 0, 'why': 'Standard result.'},
          {'q': 'EI is called the…', 'opts': ['section modulus', 'flexural rigidity', 'polar moment', 'shear flow'], 'ok': 1, 'why': 'Resistance to bending deformation.'},
          {'q': 'At a fixed support…', 'opts': ['v = 0 only', 'v = 0 and v′ = 0', 'M = 0', 'V = 0'], 'ok': 1, 'why': 'No deflection and no rotation.'},
          {'q': 'Doubling the span of a simply supported beam with uniform load multiplies δ by…', 'opts': ['4', '8', '16', '2'], 'ok': 2, 'why': 'L⁴.'}],
 'cards': [('Elastic curve', 'EIv″ = M.'), ('Cantilever tip load', 'PL³/(3EI).'), ('Simply supported center load', 'PL³/(48EI).'), ('Simply supported uniform load', '5wL⁴/(384EI).'), ('Superposition', 'Add deflections from each load.'), ('Serviceability', 'Limit such as L/360.')],
 'planet': {'text': ['Longer blades catch more wind, but they also deflect more. The U.S. Department of Energy reports that the average rotor diameter of newly installed U.S. turbines was over 133.8 meters in 2023, that 98% of new turbines that year had rotors of 115 meters or more, and that rotor swept areas have grown around 670% since 1998–1999, letting turbines produce more electricity even where winds are lighter. DOE notes blades cannot be folded or bent once built, which limits trucking, and it is researching more slender and flexible blades. Beam-deflection theory is how designers keep a flexible blade from striking the tower.'],
            'site': [('Physics II', 'Physics_II.html')],
            'src': [_BIG]},
 'res': [(_MIT[0], _MIT[1], 'MIT lectures on beam deflection.'), ('OpenStax Calculus Volume 1, 5.5 Substitution', 'https://openstax.org/books/calculus-volume-1/pages/5-5-substitution', 'Free calculus review for integrating the elastic curve.')]})
UNITS.append(
{'id': 'u10', 'title': 'Buckling of Columns', 'weeks': 'Week 14',
 'summary': 'Stability and the critical load, Euler’s formula for pinned columns, effective length for other end conditions, slenderness ratio and critical stress, inelastic buckling, imperfections, and thin shells with knockdown factors.',
 'objectives': ['Explain stable, neutral and unstable equilibrium in columns.', 'Compute Euler critical loads with effective length factors.', 'Use the slenderness ratio to tell buckling from yielding.', 'Explain why imperfections and knockdown factors matter for thin shells such as rocket tanks.'],
 'concepts': ['A slender column can fail suddenly by bending sideways at a load far below the crushing load. That load is the critical load P_cr.',
              'Euler: P_cr = π²EI/(KL)². K = 1 for pinned–pinned, 2 for fixed–free, 0.5 for fixed–fixed and about 0.7 for fixed–pinned.', 'Buckling uses the smallest I of the section: a column buckles about its weak axis.',
              'Critical stress σ_cr = π²E/(KL/r)², with radius of gyration r = √(I/A). If σ_cr exceeds the yield strength, the short column yields first; between the two, inelastic buckling applies.',
              'Thin cylindrical shells, like rocket tanks, are very sensitive to tiny imperfections, so designers multiply the ideal buckling load by a knockdown factor taken from tests.'],
 'eqs': [('P_{cr}=\\frac{\\pi^2EI}{(KL)^2}', 'Euler critical load'), ('\\sigma_{cr}=\\frac{\\pi^2E}{(KL/r)^2},\\quad r=\\sqrt{I/A}', 'Critical stress'), ('K=1,\\ 2,\\ 0.5,\\ 0.7', 'Pinned, fixed–free, fixed–fixed, fixed–pinned')],
 'worked': [
  {'q': 'A pinned–pinned steel column (E = 200 GPa) is 3 m long with I = 2 × 10⁻⁶ m⁴. Find P_cr.', 'steps': ['P_cr = π² × 200 × 10⁹ × 2 × 10⁻⁶/3².'], 'a': '438.6 kN.'},
  {'q': 'The same column is fixed at the base and free at the top. Find P_cr.', 'steps': ['K = 2, so KL = 6 m and P_cr drops by 4.'], 'a': '109.7 kN.'},
  {'q': 'A solid 50 mm steel rod, 2 m long and pinned at both ends, has σ_Y = 250 MPa. Does it buckle or yield first?', 'steps': ['r = d/4 = 12.5 mm; KL/r = 2000/12.5 = 160.', 'σ_cr = π² × 200,000/160² MPa.'], 'a': 'σ_cr = 77.1 MPa < 250 MPa: it buckles first.'}],
 'practice': [('A column’s length is doubled. What happens to P_cr?', 'It drops to a quarter.'),
              ('How does a fixed–fixed column compare with a pinned–pinned one of the same length?', 'K = 0.5, so P_cr is 4 times larger.'),
              ('NASA describes a test load of up to 750,000 pounds. Convert to meganewtons with NIST’s factor.', '750,000 × 4.448222 N = 3.34 MN.'),
              ('Sample values: NASA found removing weld lands can raise load capacity by up to 28%. What would a sample 10 MN cylinder carry?', '10 × 1.28 = 12.8 MN (sample cylinder).')],
 'misc': [('Columns fail when the stress reaches yield.', 'Slender columns buckle at much lower stress.'), ('A column buckles about its strong axis.', 'It buckles about the axis with the smallest I.'),
          ('The Euler load is what a real column will carry.', 'Imperfections and eccentric loads lower it, especially for thin shells.')],
 'quiz': [{'q': 'Euler’s P_cr is proportional to…', 'opts': ['L', '1/L', '1/L²', 'L²'], 'ok': 2, 'why': 'π²EI/(KL)².'},
          {'q': 'K for a fixed–free (flagpole) column:', 'opts': ['0.5', '0.7', '1', '2'], 'ok': 3, 'why': 'Effective length 2L.'},
          {'q': 'Slenderness ratio is…', 'opts': ['KL/r', 'r/L', 'I/A', 'E/σ_Y'], 'ok': 0, 'why': 'Effective length over radius of gyration.'},
          {'q': 'A knockdown factor accounts for…', 'opts': ['temperature', 'imperfection sensitivity of thin shells', 'paint', 'gravity'], 'ok': 1, 'why': 'Real shells buckle below ideal theory.'}],
 'cards': [('Euler load', 'P_cr = π²EI/(KL)².'), ('Effective length', 'K = 1, 2, 0.5, 0.7.'), ('Radius of gyration', 'r = √(I/A).'), ('Critical stress', 'π²E/(KL/r)².'), ('Weak axis', 'Smallest I governs.'), ('Knockdown factor', 'Test-based reduction for thin shells.')],
 'planet': {'text': ['Lighter rockets launch the satellites that watch Earth’s climate, and buckling sets how light their tanks can be. NASA’s Engineering and Safety Center reports that its Shell Buckling Knockdown Factor team re-examined knockdown factors that had not been updated since the Apollo era of the 1960s. Eight subscale and two full-scale metallic cylinder tests led to new knockdown factors that are used on the Space Launch System core stage, giving both mass and cost savings. In one test, an 8-foot-diameter cylinder loaded up to 750,000 pounds buckled within 2.5% of the engineer’s prediction, and early results showed that removing weld lands can raise load capacity by up to 28%.'],
            'site': [('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html')],
            'src': [_SBKF]},
 'res': [(_MIT[0], _MIT[1], 'MIT lectures on buckling.'), (_SBKF[0], _SBKF[1], 'How NASA tests buckling of rocket cylinders.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Hooke’s law and stiffness', 'week': 'Week 2',
 'goal': 'Load a spring (or rubber band) in steps, show that stretch grows in proportion to force, and find the stiffness k.',
 'eq': ('F=kx,\\quad U=\\tfrac12kx^2', 'Linear spring and stored energy'),
 'steps': ['Open PhET Hooke’s Law, choose one spring and set its constant; apply forces in equal steps and record the displacement.', 'Home: hang a bag from a rubber band and add coins of known mass (F = mg), measuring the stretch with a ruler each time.',
           'Plot F against x and fit a line through the origin; the slope is k.', 'Unload step by step and note whether the rubber band returns to its starting length.'],
 'table': (['F (N)', 'x (mm) for k = 50 N/m'], [['0.5', '10'], ['1.0', '20'], ['1.5', '30'], ['2.0', '40']]),
 'note': 'Sample values for a spring with k = 50 N/m; your own spring sets your slope.',
 'calc': ['k = F/x = 0.5 N/0.010 m = 50 N/m in every row.', 'Stored energy at 2 N: U = ½ × 50 × 0.04² = 0.04 J.'],
 'safety': ['Wear glasses; a stretched rubber band can snap back.'], 'home': ['The rubber-band step is the home version.'],
 'sims': [('PhET: Hooke’s Law', _PH + 'hookes-law')],
 'planet': 'Stiffness tests like this one, scaled up, are how engineers qualify every bolt, cable and bridge member.', 'planet_src': [_ASCE]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Stress, strain and the modulus of a rubber band', 'week': 'Week 3',
 'goal': 'Turn force and stretch into stress and strain, estimate a modulus, and see where the response stops being linear.',
 'eq': ('\\sigma=\\frac{F}{A},\\quad \\varepsilon=\\frac{\\delta}{L_0},\\quad E=\\frac{\\sigma}{\\varepsilon}', 'Engineering stress and strain'),
 'steps': ['Measure a flat rubber band’s width and thickness with a ruler (or count layers of a known thickness) and its unstretched length L₀.', 'Hang known masses and record the stretch δ for each.',
           'Compute σ and ε and plot σ against ε. Fit the straight early part to estimate E.', 'Keep adding small masses and note where the curve bends: rubber is not linear at large strain.'],
 'table': (['F (N)', 'δ (mm)', 'σ (MPa)', 'ε'], [['1', '8', '0.667', '0.10'], ['2', '16', '1.333', '0.20'], ['3', '24', '2.000', '0.30']]),
 'note': 'Sample values for a band with A = 1.5 mm² and L₀ = 80 mm in its near-linear range.',
 'calc': ['σ = 1 N/1.5 mm² = 0.667 MPa; ε = 8/80 = 0.10.', 'E = 0.667/0.10 = 6.67 MPa, about 30,000 times less stiff than steel (200 GPa).'],
 'safety': ['Wear glasses and keep the band pointed away from faces; stop before it breaks.'], 'home': ['The whole lab is a home lab.'],
 'sims': [('PhET: Masses and Springs', _PH + 'masses-and-springs')],
 'planet': 'Knowing stiffness and strength per kilogram is how lighter car bodies are chosen, and DOE links a 10% weight cut to 6% to 8% better fuel economy.', 'planet_src': [_LW]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Twisting a foam rod', 'week': 'Week 6',
 'goal': 'Twist a foam rod with a known torque, measure the angle of twist, and check that φ grows in proportion to T as in φ = TL/(GJ).',
 'eq': ('\\phi=\\frac{TL}{GJ},\\quad J=\\frac{\\pi d^4}{32}', 'Angle of twist of a solid rod'),
 'steps': ['Draw a straight line along a solid foam rod and mark two rings 0.5 m apart.', 'Hold one end fixed and apply a torque with a lever arm and a known weight (T = F × arm).',
           'Photograph the line and read the twist angle between the rings; repeat for three torques.', 'Plot φ against T; the slope is L/(GJ). Note the spiral the straight line becomes: that is shear strain.'],
 'table': (['T (N·m)', 'φ (°)'], [['0.1', '4.67'], ['0.2', '9.34'], ['0.3', '14.0']]),
 'note': 'Values computed for a sample rod with d = 50 mm, L = 0.5 m and G = 1 MPa.',
 'calc': ['J = π × 0.05⁴/32 = 6.136 × 10⁻⁷ m⁴.', 'φ = 0.2 × 0.5/(10⁶ × 6.136 × 10⁻⁷) = 0.163 rad = 9.34°.', 'Surface shear strain γ = cφ/L = 0.025 × 0.163/0.5 = 0.00815.'],
 'safety': ['Keep weights small and low over a soft surface.'], 'home': ['The whole lab is a home lab.'],
 'sims': [('PhET: Torque', _PH + 'torque')],
 'planet': 'Wind turbine shafts carry the same kind of twisting load, millions of times larger.', 'planet_src': [_WIND]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Shape matters, a ruler flat and on edge', 'week': 'Week 8',
 'goal': 'Load a ruler as a cantilever lying flat and then on edge and compare deflection and stress with I = bh³/12.',
 'eq': ('I=\\frac{bh^3}{12},\\quad \\delta=\\frac{PL^3}{3EI},\\quad \\sigma=\\frac{Mc}{I}', 'Section shape and cantilever bending'),
 'steps': ['Clamp a 30 mm × 3 mm plastic ruler flat to a table with 250 mm sticking out.', 'Hang a 0.5 N load (about 51 g) from the tip and measure the deflection against a second ruler.',
           'Turn the ruler on edge (clamp it between two books) and repeat with the same load.', 'Compare the ratio of deflections with the ratio of I values.'],
 'table': (['Orientation', 'I (m⁴)', 'δ at 0.5 N (mm)', 'σ_max (MPa)'], [['Flat (h = 3 mm)', '6.75 × 10⁻¹¹', '12.9', '2.78'], ['On edge (h = 30 mm)', '6.75 × 10⁻⁹', '0.129', '0.278']]),
 'note': 'Values computed for a sample plastic ruler with E = 3 GPa.',
 'calc': ['I ratio = (30/3)² = 100, so the edge deflection is 100 times smaller.', 'M = 0.5 × 0.25 = 0.125 N·m; flat σ = 0.125 × 0.0015/6.75 × 10⁻¹¹ = 2.78 MPa.'],
 'safety': ['Do not overload the ruler; plastic can snap.'], 'home': ['The whole lab is a home lab.'],
 'sims': [('PhET: Balancing Act', _PH + 'balancing-act')],
 'planet': 'Putting material far from the neutral axis is how blades, beams and towers save material.', 'planet_src': [_WTTC]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Cantilever deflection and Young’s modulus', 'week': 'Week 12',
 'goal': 'Measure tip deflection against load for a flat ruler cantilever and back out Young’s modulus from δ = PL³/(3EI).',
 'eq': ('E=\\frac{L^3}{3I\\,(\\delta/P)}', 'From the slope of δ against P'),
 'steps': ['Use the flat ruler from Lab D with 250 mm overhang.', 'Hang 0.25, 0.5 and 1.0 N at the tip and record the deflection each time.',
           'Plot δ against P and fit a line through the origin.', 'Compute E from the slope and compare with a typical value for the plastic.'],
 'table': (['P (N)', 'δ (mm)'], [['0.25', '6.43'], ['0.50', '12.9'], ['1.00', '25.7']]),
 'note': 'Values computed for a sample plastic ruler with E = 3 GPa, b = 30 mm, h = 3 mm.',
 'calc': ['Slope δ/P = 25.7 mm/N.', 'E = 0.25³/(3 × 6.75 × 10⁻¹¹ × 0.0257) = 3.0 GPa.'],
 'safety': ['Keep loads small and catch them if they slip.'], 'home': ['The whole lab is a home lab.'],
 'sims': [('PhET: Hooke’s Law', _PH + 'hookes-law')],
 'planet': 'Longer, more flexible wind blades are designed with the same deflection formula.', 'planet_src': [_BIG]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Buckling spaghetti', 'week': 'Week 14',
 'goal': 'Find the load that buckles strands of dry spaghetti of different lengths and check that P_cr falls as 1/L².',
 'eq': ('P_{cr}=\\frac{\\pi^2EI}{L^2},\\quad I=\\frac{\\pi d^4}{64}', 'Pinned–pinned column'),
 'steps': ['Cut strands to 100, 150 and 200 mm. Stand each upright on a kitchen scale and press down slowly on top with a flat object.', 'Record the highest scale reading just as the strand bows sideways (convert grams to newtons).',
           'Repeat three times per length and average.', 'Plot P_cr against 1/L²; the line should pass near the origin.'],
 'table': (['L (mm)', 'P_cr (N)'], [['100', '1.526'], ['150', '0.678'], ['200', '0.381']]),
 'note': 'Values computed for a sample strand with d = 1.8 mm and E = 3 GPa; real spaghetti varies.',
 'calc': ['I = π × 1.8⁴/64 = 0.515 mm⁴ = 5.153 × 10⁻¹³ m⁴.', 'P_cr at 0.1 m = π² × 3 × 10⁹ × 5.153 × 10⁻¹³/0.01 = 1.526 N (about 156 g on the scale).', 'Doubling L from 100 to 200 mm cuts P_cr by 4.'],
 'safety': ['Wear glasses; spaghetti snaps into sharp pieces.'], 'home': ['The whole lab is a home lab.'],
 'sims': [('OpenStax UP1, 12.4 Elasticity and plasticity', _O + '12-4-elasticity-and-plasticity')],
 'planet': 'NASA tests full-size rocket cylinders to buckling to set knockdown factors that save mass.', 'planet_src': [_SBKF]})
SCHEDULE = [(1, 'u1', 'Internal forces, normal and shear stress', 'MIT 2.001; OpenStax UP1 12.3'), (2, 'u1', 'Bearing stress, allowable stress, factor of safety; Lab A', 'MIT 2.001'),
            (3, 'u2', 'Strain, stress–strain curve, Hooke’s law, Poisson’s ratio; Lab B', 'UP1 12.3–12.4'), (4, 'u3', 'Axial deformation, indeterminate bars, thermal stress', 'UP2 1.3'),
            (5, 'u4', 'Torsion formula, polar moment, angle of twist', 'MIT 2.001'), (6, 'u4', 'Power transmission, shaft design; Lab C', 'MIT 2.001'),
            (7, 'u5', 'Shear and moment diagrams', 'MIT 2.001; UP1 12.2'), (8, 'u5', 'Flexure formula, section modulus; Lab D; midterm practice', 'MIT 2.001'),
            (9, 'u6', 'Transverse shear, shear flow, built-up beams', 'MIT 2.001'), (10, 'u7', 'Stress transformation, Mohr’s circle, failure theories, fatigue', 'MIT 2.001, 2.002'),
            (11, 'u8', 'Pressure vessels and combined loading', 'MIT 2.001'), (12, 'u9', 'Elastic curve, integration, standard formulas; Lab E', 'MIT 2.001'),
            (13, 'u9', 'Superposition and indeterminate beams', 'MIT 2.001'), (14, 'u10', 'Column buckling and knockdown factors; Lab F', 'MIT 2.001'),
            (15, 'exam', 'Review and final practice set', 'All units')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('A 16 mm steel rod carries 30 kN in tension. Find the stress.', ['A = π × 16²/4 = 201.1 mm².'], '149.2 MPa.'),
  ('An aluminum bar (E = 70 GPa) 1.5 m long with A = 300 mm² carries 12 kN. Find its elongation.', ['δ = PL/(AE).'], '0.857 mm.'),
  ('A steel bar (E = 200 GPa, α = 12 × 10⁻⁶/°C) is held between rigid walls and heated 25 °C. Find the stress.', ['σ = EαΔT.'], '60 MPa compression.'),
  ('A solid 40 mm shaft carries 800 N·m. Find τ_max.', ['τ = 16T/(πd³).'], '63.7 MPa.'),
  ('A simply supported 5 m beam, 120 mm wide × 240 mm deep, carries 4 kN/m. Find σ_max.', ['M = wL²/8 = 12.5 kN·m; I = 1.382 × 10⁻⁴ m⁴.'], '10.9 MPa.')]),
 ('Final practice set (all units)', [
  ('An 80 mm × 160 mm rectangular beam carries V = 12 kN. Find τ_max.', ['τ = 1.5V/A.'], '1.41 MPa.'),
  ('Find the principal stresses for σx = 50 MPa, σy = 10 MPa, τxy = 15 MPa.', ['Center 30 MPa; R = √(20² + 15²) = 25 MPa.'], 'σ₁ = 55 MPa, σ₂ = 5 MPa.'),
  ('A thin cylinder has r = 0.5 m, t = 10 mm and p = 2 MPa. Find σ_h and σ_a.', ['pr/t and pr/(2t).'], '100 MPa and 50 MPa.'),
  ('A 1.5 m steel cantilever (I = 4 × 10⁻⁶ m⁴) carries 2 kN at its tip. Find the tip deflection.', ['δ = PL³/(3EI).'], '2.81 mm.'),
  ('A pinned steel column 4 m long has I = 5 × 10⁻⁶ m⁴. Find P_cr.', ['π²EI/L².'], '616.9 kN.'),
  ('A shaft point has σ = 80 MPa and τ = 30 MPa. Find the von Mises stress.', ['√(σ² + 3τ²).'], '95.4 MPa.')])]
FORMULAS = ['\\sigma=P/A,\\ \\tau=V/A,\\ \\sigma_b=P/(td)', '\\varepsilon=\\delta/L,\\ \\sigma=E\\varepsilon,\\ G=E/(2(1+\\nu))', '\\delta=PL/(AE),\\ \\delta_T=\\alpha\\Delta TL', '\\tau=T\\rho/J,\\ \\phi=TL/(GJ),\\ J=\\pi d^4/32',
            'P=T\\omega', 'dM/dx=V,\\ dV/dx=-w', '\\sigma=My/I,\\ I=bh^3/12', '\\tau=VQ/(It),\\ q=VQ/I', '\\sigma_{1,2}=\\tfrac{\\sigma_x+\\sigma_y}{2}\\pm\\sqrt{(\\tfrac{\\sigma_x-\\sigma_y}{2})^2+\\tau_{xy}^2}',
            '\\sigma_{vm}=\\sqrt{\\sigma_1^2-\\sigma_1\\sigma_2+\\sigma_2^2}', '\\sigma_h=pr/t,\\ \\sigma_a=pr/(2t)', 'EIv\'\'=M', '\\delta=PL^3/(3EI),\\ PL^3/(48EI),\\ 5wL^4/(384EI)', 'P_{cr}=\\pi^2EI/(KL)^2']
GLOSSARY = sorted([('Bearing stress', 'Contact pressure between a fastener and a plate, P/(td).'), ('Elastic curve', 'Deflected shape of a beam’s neutral axis.'), ('Factor of safety', 'Failure load divided by allowable load.'),
    ('Fatigue', 'Failure from repeated loading, often below yield.'), ('Flexural rigidity', 'EI, a beam’s resistance to bending deformation.'), ('Hoop stress', 'Circumferential stress pr/t in a pressurized cylinder.'),
    ('Knockdown factor', 'Test-based reduction of the ideal buckling load of thin shells.'), ('Neutral axis', 'Line of zero bending stress through the centroid.'), ('Poisson’s ratio', 'Ratio of lateral to axial strain, with a minus sign.'),
    ('Polar moment of inertia', 'J, a shaft’s resistance to twisting.'), ('Principal stresses', 'Normal stresses on planes with zero shear.'), ('Section modulus', 'S = I/c.'),
    ('Shear flow', 'Shear force per unit length, VQ/I.'), ('Slenderness ratio', 'KL/r of a column.'), ('Strain', 'Deformation per unit length.'), ('Stress', 'Internal force per unit area.'),
    ('Von Mises stress', 'Equivalent stress compared with the yield strength.'), ('Yield strength', 'Stress at which permanent deformation begins.'), ('Young’s modulus', 'E, slope of the elastic stress–strain line.')])
RUBRIC = [('4 · Mastery', 'Finds internal loads with a free-body diagram, picks the right deformation model, checks assumptions (elastic, thin-walled, slender), and reports stresses with a factor of safety.'), ('3 · Proficient', 'Solves the practice problems with occasional unit or sign slips.'),
          ('2 · Developing', 'Follows worked examples but mixes up I, J and Q or forgets compatibility.'), ('1 · Beginning', 'Plugs numbers into formulas without diagrams; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '25%'), ('Labs', '20%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    g = 9.81; E = 200e9; G = 80e9
    Ac = lambda d: pi * d**2 / 4
    Js = lambda d: pi * d**4 / 32
    Ir = lambda b, h: b * h**3 / 12
    J50 = Js(.05); T50 = 50e3 / (1500 * 2 * pi / 60)
    sx, sy, txy = 80, -40, 30; R = sqrt(60**2 + 30**2); s1, s2 = 20 + R, 20 - R
    vm = lambda a, b: sqrt(a * a - a * b + b * b)
    Iflat = Ir(.03, .003); Iedge = Ir(.003, .03); Isp = pi * 1.8e-3**4 / 64
    cant = lambda P, L, EI: P * L**3 / (3 * EI)
    r = [
     ('u1 A20', Ac(20), 314.2), ('u1 s', 50e3 / Ac(20), 159.2), ('u1 A12', Ac(12), 113.1), ('u1 tau', 10e3 / Ac(12), 88.4), ('u1 sall', 250 / 2, 125), ('u1 Areq', 100e3 / 125, 800), ('u1 d', sqrt(4 * 800 / pi), 31.9),
     ('u1 post', 200e3 / 1e4, 20), ('u1 A10', Ac(10), 78.54), ('u1 bolt', 8e3 / Ac(10), 101.9), ('u1 bear', 8e3 / 60, 133), ('u1 FS', 90 / 30, 3), ('u1 posted', 63085 / 623218, .101),
     ('u2 eps', 1.2 / 2000, 6e-4), ('u2 E', 120 / 6e-4, 200e3), ('u2 G', 70 / 2.66, 26.3), ('u2 lat', .3 * .001, .0003), ('u2 dd', .0003 * 20, .006), ('u2 Est', 200e9 / 7850, 25.5e6), ('u2 Eal', 70e9 / 2700, 25.9e6),
     ('u2 elong', 12 / 50, .24), ('u2 ur', 250**2 / (2 * 200e3), .156), ('u2 mpg lo', 30 * 1.06, 31.8), ('u2 mpg hi', 30 * 1.08, 32.4), ('u2 quizG', 200 / 2.5, 80),
     ('u3 d', 60e3 * 3000 / (500 * 200e3), 1.8), ('u3 th', 200e3 * 12e-6 * 40, 96), ('u3 RA', 30 * 2 / 3, 20), ('u3 RB', 30 * 1 / 3, 10), ('u3 rail', 12e-6 * 30 * 25000, 9),
     ('u3 al', 20e3 * 1000 / (400 * 70e3), .714), ('u3 st', 20e3 * 500 / (200 * 200e3), .250), ('u3 tot', 20e3 * 1000 / (400 * 70e3) + 20e3 * 500 / (200 * 200e3), .964), ('u3 eps', 100 / 70e3, 1.43e-3), ('u3 hub', 103.4 / 1.83, 56.5),
     ('u4 J', J50, 6.136e-7), ('u4 tau', 1500 * .025 / J50, 61.1e6), ('u4 phi', 1500 * 2 / (G * J50), .0611), ('u4 phideg', degrees(1500 * 2 / (G * J50)), 3.50), ('u4 w', 1500 * 2 * pi / 60, 157.1), ('u4 T', T50, 318.3),
     ('u4 d', (16 * T50 / (pi * 40e6))**(1 / 3), .0343), ('u4 Jh', pi * (.06**4 - .04**4) / 32, 1.021e-6), ('u4 tauh', 2000 * .03 / (pi * (.06**4 - .04**4) / 32), 58.8e6), ('u4 area', 1 - (40 / 60)**2, .556), ('u4 Jr', 1 - (40 / 60)**4, .802),
     ('u4 t30', 16 * 500 / (pi * .03**3), 94.3e6), ('u4 w12', 12 * 2 * pi / 60, 1.257), ('u4 Twind', 3.4e6 / (12 * 2 * pi / 60), 2.71e6),
     ('u5 M', 10 * 4 / 4, 10), ('u5 I', Ir(.1, .2), 6.667e-5), ('u5 s', 10e3 * .1 / Ir(.1, .2), 15e6), ('u5 R', 5 * 6 / 2, 15), ('u5 Mu', 5 * 36 / 8, 22.5), ('u5 cant', 3 * 2, 6), ('u5 plank', (200 / 50)**2, 16),
     ('u5 rod', 32 * 500 / (pi * .04**3), 79.6e6), ('u5 blade', 84 / .4, 210),
     ('u6 tmax', 1.5 * 15e3 / .02, 1.125e6), ('u6 I', Ir(.15, .1), 1.25e-5), ('u6 Q', .15 * .05 * .025, 1.875e-4), ('u6 q', 10e3 * 1.875e-4 / 1.25e-5 / 1000, 150), ('u6 tg', 150 / 150, 1.0), ('u6 tchk', 1.5 * 10e3 / .015, 1e6),
     ('u6 q2', 2e3 * 1.875e-4 / 1.25e-5 / 1000, 30), ('u6 s', 900 / 30, 30), ('u6 Acirc', Ac(50), 1963), ('u6 circ', 4 * 10e3 / (3 * Ac(50)), 6.79), ('u6 rect', 1.5 * 5e3 / 5e3, 1.5), ('u6 ratio', 2 * 10, 20),
     ('u6 lo', 1000 * .13, 130), ('u6 hi', 1000 * .265, 265),
     ('u7 R', R, 67.1), ('u7 s1', s1, 87.1), ('u7 s2', s2, -47.1), ('u7 th', degrees(atan(.5)) / 2, 13.3), ('u7 vm', vm(s1, s2), 117.9), ('u7 FS', 250 / vm(s1, s2), 2.12), ('u7 tres', 125 / R, 1.86),
     ('u7 vm2', sqrt(60**2 + 3 * 40**2), 91.7), ('u7 cyc', 20 * 365.25 * 86400, 6.31e8),
     ('u8 sh', 70 * 150 / 15, 700), ('u8 sa', 70 * 150 / 30, 350), ('u8 A', Ac(100), 7854), ('u8 PA', 10e3 / Ac(100), 1.27), ('u8 Mc', 32 * 3e6 / (pi * 100**3), 30.6),
     ('u8 comp', 10e3 / Ac(100) + 32 * 3e6 / (pi * 100**3), 31.8), ('u8 ten', 32 * 3e6 / (pi * 100**3) - 10e3 / Ac(100), 29.3), ('u8 gh', 2 * 150 / 3, 100), ('u8 ga', 2 * 150 / 6, 50), ('u8 t', 35 * 200 / 600, 11.7),
     ('u8 psi', 1e4 * 6894.757, 68.9e6), ('u8 bar', 700 * 1e5, 70e6),
     ('u9 cant', cant(1000, 2, E * 8e-6), 1.67e-3), ('u9 ss', 5 * 1e4 * 6**4 / (384 * E * 1e-4), 8.44e-3), ('u9 lim', 6000 / 360, 16.7), ('u9 RB', 3 * 10 * 6 / 8, 22.5), ('u9 x8', 2**3, 8),
     ('u9 wood', 5000 * 64 / (48 * 10e9 * 5e-5), 13.3e-3), ('u9 cudl', 2000 * 81 / (8 * E * 1e-5), 10.1e-3), ('u9 swept', sqrt(7.7), 2.77),
     ('u10 P', pi**2 * E * 2e-6 / 9, 438.6e3), ('u10 Pff', pi**2 * E * 2e-6 / 36, 109.7e3), ('u10 Lr', 2000 / 12.5, 160), ('u10 scr', pi**2 * 200e3 / 160**2, 77.1), ('u10 lb', 750000 * 4.448222, 3.34e6), ('u10 28', 10 * 1.28, 12.8),
     ('A k', .5 / .01, 50), ('A U', .5 * 50 * .04**2, .04),
     ('B s1', 1 / 1.5, .667), ('B s2', 2 / 1.5, 1.333), ('B s3', 3 / 1.5, 2.0), ('B e', 8 / 80, .10), ('B E', (1 / 1.5) / .1, 6.67), ('B ratio', 200e3 / 6.67, 30000),
     ('C J', J50, 6.136e-7), ('C 1', degrees(.1 * .5 / (1e6 * J50)), 4.67), ('C 2', degrees(.2 * .5 / (1e6 * J50)), 9.34), ('C 3', degrees(.3 * .5 / (1e6 * J50)), 14.0), ('C rad', .2 * .5 / (1e6 * J50), .163),
     ('C gam', .025 * .2 * .5 / (1e6 * J50) / .5, .00815),
     ('D If', Iflat, 6.75e-11), ('D Ie', Iedge, 6.75e-9), ('D df', cant(.5, .25, 3e9 * Iflat), 12.9e-3), ('D de', cant(.5, .25, 3e9 * Iedge), .129e-3), ('D sf', .125 * .0015 / Iflat, 2.78e6), ('D se', .125 * .015 / Iedge, .278e6),
     ('D ratio', (30 / 3)**2, 100), ('D 51g', .5 / g * 1000, 51),
     ('E .25', cant(.25, .25, 3e9 * Iflat), 6.43e-3), ('E .5', cant(.5, .25, 3e9 * Iflat), 12.9e-3), ('E 1', cant(1, .25, 3e9 * Iflat), 25.7e-3), ('E E', .25**3 / (3 * Iflat * cant(1, .25, 3e9 * Iflat)), 3.0e9),
     ('F I', Isp, 5.153e-13), ('F Imm', Isp * 1e12, .515), ('F 100', pi**2 * 3e9 * Isp / .01, 1.526), ('F 150', pi**2 * 3e9 * Isp / .0225, .678), ('F 200', pi**2 * 3e9 * Isp / .04, .381), ('F g', pi**2 * 3e9 * Isp / .01 / g * 1000, 156),
     ('M1 A', Ac(16), 201.1), ('M1', 30e3 / Ac(16), 149.2), ('M2', 12e3 * 1500 / (300 * 70e3), .857), ('M3', 200e3 * 12e-6 * 25, 60), ('M4', 16 * 800 / (pi * .04**3), 63.7e6),
     ('M5 M', 4 * 25 / 8, 12.5), ('M5 I', Ir(.12, .24), 1.382e-4), ('M5', 12.5e3 * .12 / Ir(.12, .24), 10.9e6),
     ('F1', 1.5 * 12e3 / (.08 * .16), 1.41e6), ('F2 R', sqrt(400 + 225), 25), ('F2 s1', 30 + 25, 55), ('F2 s2', 30 - 25, 5), ('F3 h', 2 * 500 / 10, 100), ('F3 a', 2 * 500 / 20, 50),
     ('u7 uni', 100 / 2, 50), ('u8 sph', 70 * 150 / 30, 350), ('u10 ff', (1 / .5)**2, 4), ('u4 J16', 2**4, 16), ('u5 h3', 2**3, 8), ('u9 L4', 2**4, 16), ('u8 dbl', 700 / 350, 2), ('A 40', 2 / 50 * 1000, 40),
     ('F4', cant(2000, 1.5, E * 4e-6), 2.81e-3), ('F5', pi**2 * E * 5e-6 / 16, 616.9e3), ('F6', sqrt(80**2 + 3 * 30**2), 95.4)]
    return r
