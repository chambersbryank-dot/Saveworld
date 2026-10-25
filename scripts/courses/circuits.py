"""Circuits (ENGR 214 + ENGR 214L): DC and AC circuit analysis: Ohm's and Kirchhoff's laws, nodal and mesh analysis, Thevenin and Norton, op amps, capacitors and inductors, first- and second-order transients, phasors, AC power and three-phase.
Oct 25 2026, founder-approved four-year track, sophomore course 8 (last sophomore course). Same module fields as statics.py / linalg.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, exp, log, atan, atan2, degrees, radians, cos, sin
ID = 'circuits'
STATUS = 'live'
YEAR = 2
PAGE = 'Circuits.html'
CODE = 'ENGR 214 + ENGR 214L'
TITLE = 'Circuits'
LAB_NAME = 'Circuits lab'
TAGLINE = 'DC and AC circuit analysis: Ohm’s and Kirchhoff’s laws, nodal and mesh analysis, Thevenin and Norton, op amps, capacitors and inductors, RC, RL and RLC transients, phasors, AC power, power factor and three-phase, with six labs. Free, self-paced, and tied to LED lighting, solar panels, batteries, EV charging and the power grid.'
DESC = 'Free self-study Circuits: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and safe low-voltage home labs, practice exams, tied to solar, EV charging and the grid.'
ALT = 'NASA photo of the International Space Station and its solar arrays'
_O2 = 'https://openstax.org/books/university-physics-volume-2/pages/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 6.002 Circuits and Electronics (Spring 2007)', 'https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/')
_LED = ('U.S. DOE: Guide to energy-efficient lighting (PDF)', 'https://www.energy.gov/sites/prod/files/guide_to_energy_efficient_lighting.pdf')
_PV = ('U.S. EIA: Photovoltaics and electricity', 'https://www.eia.gov/energyexplained/solar/photovoltaics-and-electricity.php')
_GRID = ('U.S. EIA: Delivery to consumers (the electric power grid)', 'https://www.eia.gov/energyexplained/electricity/delivery-to-consumers.php')
_TD = ('U.S. EIA: How much electricity is lost in transmission and distribution?', 'https://www.eia.gov/tools/faqs/faq.php?id=105&t=3')
_EV = ('U.S. DOE Alternative Fuels Data Center: Electric vehicle charging stations', 'https://afdc.energy.gov/fuels/electricity-stations')
_BAT = ('U.S. EIA: Battery storage capacity averaged 70% growth over the last three years (Aug. 7, 2026)', 'https://www.eia.gov/todayinenergy/detail.php?id=67925')
_DC = ('Berkeley Lab: Report evaluates increase in electricity demand from data centers (Jan. 2025)', 'https://newscenter.lbl.gov/2025/01/15/berkeley-lab-report-evaluates-increase-in-electricity-demand-from-data-centers/')
BANNER = ['images/ISS_Flyaround_2021.jpg', 'images/SDO_Sun.jpg', 'images/Aurora_Borealis_ISS072-E-159172.jpg', 'images/GOES19_GOESU_KSC.jpg']
CREDITS = {'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)', 'images/SDO_Sun.jpg': 'NASA/SDO',
           'images/Aurora_Borealis_ISS072-E-159172.jpg': 'NASA (ISS072-E-159172)', 'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester sophomore circuit analysis course with a lab. It is modeled on the topics and depth of MIT 6.002 Circuits and Electronics (free on MIT OpenCourseWare), Georgia Tech ECE 2040 Circuit Analysis and Purdue ECE 20001 Electrical Engineering Fundamentals I, and on the free OpenStax University Physics Volume 2 and PhET simulations, which we link where they help. None of those authors or schools endorses this page.',
         'What we add: every unit ties to real clean-energy work with a cited public source (LED lighting, solar panels and inverters, battery storage, EV charging, data centers and the power grid), every number on the page is re-computed by a checking script before it goes live, and every lab has a free PhET simulation or a safe low-voltage home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Circuits are how clean energy reaches people. Solar panels make direct current that inverters turn into alternating current, batteries store it, transformers and power lines carry it, and efficient lights, motors and chargers use it.',
                 'Every percent of loss in a wire, transformer or converter is energy that had to be generated somewhere. The analysis in this course is what engineers use to cut those losses. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values.']
PREREQS = ['Physics II: charge, electric field, potential, current, resistance, capacitance, inductance and Faraday’s law.', 'Calculus I and II: derivatives and integrals; Units 7 and 8 solve first- and second-order differential equations.',
           'Complex numbers (reviewed in Unit 9) for phasors; Linear Algebra helps with nodal and mesh equations.', 'Differential Equations can be taken alongside this course.']
STUDY = ['Draw and label the circuit first: node voltages, branch currents with arrows, and polarity marks on every element.', 'Use the passive sign convention: current entering the + terminal means the element absorbs power.',
         'Write KCL at nodes or KVL around meshes, count unknowns and equations, then solve (by hand for 2 × 2, by matrix for more).', 'Check every answer: power absorbed must equal power supplied, and limits (t = 0, t → ∞, ω → 0 or ∞) must make sense.',
         'Keep units in SI: V, A, Ω, W, F, H, s, and watch prefixes (mA, kΩ, µF, mH).', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET simulations (they run in a browser).', 'A digital multimeter (inexpensive models measure V, A and Ω).',
            'A solderless breadboard, jumper wires, a 2 × AA battery holder (3 V) and AA batteries.', 'Resistors (100 Ω, 1 kΩ, 10 kΩ), a 1000 µF capacitor rated at least 6.3 V, and LEDs.',
            'Optional: a plug-in power meter for comparing light bulbs and appliances (it plugs into the wall; do not open it).', 'Safety glasses, a stopwatch or phone, and spreadsheet software.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab can be done in a free PhET simulation or with a 3 V battery pack. Never work on household wiring or wall outlets: mains voltage can kill. Do not short a battery, and put electrolytic capacitors in the right way round.']
SAFETY_SRC = ('OpenStax University Physics Volume 2, 10.6 Household wiring and electrical safety', _O2 + '10-6-household-wiring-and-electrical-safety')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('1 kilowatt-hour (kWh)', '3.6 × 10⁶ J'), ('1 horsepower (electric)', '746 W'), ('Elementary charge e', '1.602 × 10⁻¹⁹ C'),
             ('U.S. household service', '120 V and 240 V at 60 Hz'), ('RMS of a sine wave', 'V_rms = V_peak/√2 ≈ 0.7071 V_peak'), ('1 ampere-hour (Ah)', '3600 C')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free textbooks, lectures and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT lecture videos, notes, problem sets and labs.'), ('OpenStax University Physics Volume 2, 10.3 Kirchhoff’s rules', _O2 + '10-3-kirchhoffs-rules', 'Free textbook chapter on DC circuits.'),
          ('OpenStax University Physics Volume 2, 15.3 RLC series circuits with AC', _O2 + '15-3-rlc-series-circuits-with-ac', 'Free textbook chapter on AC circuits.'),
          ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc', 'Build and measure DC circuits.'), ('PhET: Circuit Construction Kit: AC', _PH + 'circuit-construction-kit-ac', 'Capacitors, inductors and AC sources.'),
          ('PhET: Ohm’s Law', _PH + 'ohms-law', 'V = IR interactively.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Circuit Variables and Elements: Charge, Current, Voltage, Power, Energy and Ohm’s Law', 'weeks': 'Weeks 1–2',
 'summary': 'Charge and current, voltage as energy per charge, power and energy, the passive sign convention, ideal independent and dependent sources, resistance and resistivity, Ohm’s law, and power in resistors.',
 'objectives': ['Relate charge, current, voltage, power and energy with correct units.', 'Apply the passive sign convention to decide whether an element absorbs or delivers power.', 'Use Ohm’s law and R = ρL/A.', 'Compute energy use in kWh and compare devices.'],
 'concepts': ['Current is the rate of charge flow, i = dq/dt, in amperes (1 A = 1 C/s). Voltage is energy per unit charge between two points, in volts (1 V = 1 J/C).',
              'Power p = vi. With the passive sign convention (current enters the + terminal), p > 0 means the element absorbs power and p < 0 means it delivers power. In any circuit, total power absorbed = total power delivered.',
              'An ideal voltage source holds its voltage whatever the current; an ideal current source holds its current whatever the voltage. Dependent sources are controlled by a voltage or current elsewhere and model transistors and amplifiers.',
              'Ohm’s law v = iR. A resistor always absorbs power p = i²R = v²/R. Resistance of a wire R = ρL/A grows with length and falls with cross-section; conductance G = 1/R in siemens.',
              'Energy w = ∫p dt; at constant power w = Pt. Utilities bill in kilowatt-hours: 1 kWh = 3.6 MJ.'],
 'eqs': [('i=\\frac{dq}{dt}', 'Current'), ('p=vi', 'Power'), ('v=iR,\\ \\ p=i^2R=\\frac{v^2}{R}', 'Ohm’s law and resistor power'), ('R=\\frac{\\rho L}{A}', 'Resistance of a conductor')],
 'worked': [
  {'q': 'A 4 Ω heater is connected to 12 V. Find the current and power.', 'steps': ['i = v/R = 12/4 = 3 A.', 'p = vi = 12 × 3.'], 'a': 'i = 3 A, p = 36 W.'},
  {'q': 'Find the resistance of 10 m of copper wire with a 1 mm² cross-section (ρ = 1.68 × 10⁻⁸ Ω·m).', 'steps': ['A = 1 mm² = 1 × 10⁻⁶ m².', 'R = ρL/A = 1.68 × 10⁻⁸ × 10/10⁻⁶.'], 'a': 'R = 0.168 Ω.'},
  {'q': 'A 60 W incandescent bulb is replaced by an LED that uses 75% less energy. Both run 3 hours a day for a year. Find the energy saved.', 'steps': ['LED power = 0.25 × 60 = 15 W.', 'Incandescent: 60 × 3 × 365 = 65,700 Wh = 65.7 kWh; LED: 16.4 kWh.'], 'a': 'About 49.3 kWh saved per bulb per year.'}],
 'practice': [('A 2 A current flows for 30 s. How much charge passes?', 'q = it = 60 C.'), ('A lamp draws 0.5 A from 120 V. Find its power and resistance.', 'p = 60 W, R = 240 Ω.'),
              ('An element has v = 5 V and i = −2 A entering its + terminal. Does it absorb or deliver power?', 'p = −10 W: it delivers 10 W.'), ('How many joules are in 2 kWh?', '7.2 × 10⁶ J.')],
 'misc': [('Current is used up by a resistor.', 'Charge is conserved; the same current leaves as enters. Energy is converted, not current.'), ('Voltage exists at a point.', 'Voltage is always between two points; a “node voltage” is measured from a chosen ground.'),
          ('Power is always vi with a plus sign.', 'Use the passive sign convention to get the sign right.')],
 'quiz': [{'q': '1 A equals…', 'opts': ['1 J/s', '1 C/s', '1 V/s', '1 W/V²'], 'ok': 1, 'why': 'Charge per second.'},
          {'q': 'Doubling the voltage across a resistor multiplies its power by…', 'opts': ['1', '2', '4', '½'], 'ok': 2, 'why': 'p = v²/R.'},
          {'q': 'Doubling a wire’s length (same area) changes its resistance by…', 'opts': ['½', '1', '2', '4'], 'ok': 2, 'why': 'R = ρL/A.'},
          {'q': '1 kWh equals…', 'opts': ['1000 J', '3600 J', '3.6 MJ', '60 kJ'], 'ok': 2, 'why': '1000 W × 3600 s.'}],
 'cards': [('Current', 'i = dq/dt, in A.'), ('Voltage', 'Energy per charge, in V = J/C.'), ('Power', 'p = vi.'), ('Passive sign convention', 'Current into + terminal: p > 0 absorbs.'), ('Ohm’s law', 'v = iR.'), ('kWh', '3.6 MJ.')],
 'planet': {'text': ['Lighting is the simplest place to see power and energy at work. The U.S. Department of Energy’s guide to energy-efficient lighting says LEDs use at least 75 percent less energy than incandescent bulbs, emit virtually no heat, and last 25 times longer.',
                     'With p = vi and w = Pt, the worked example shows what that means for one bulb: replacing a 60 W incandescent with a 15 W LED, used 3 hours a day, saves about 49.3 kWh a year. Multiply by the dozens of bulbs in a home and the millions of homes in a country and the power plants that never have to run become visible.'],
            'site': [('Physics II', 'Physics_II.html'), ('Solutions', 'Solutions.html')],
            'src': [_LED, ('OpenStax UP2, 9.4 Ohm’s law', _O2 + '9-4-ohms-law')]},
 'res': [('OpenStax UP2, 9.4 Ohm’s law', _O2 + '9-4-ohms-law', 'Free textbook section.'), (_MIT[0], _MIT[1], 'Lectures on the circuit abstraction and Ohm’s law.'),
         ('PhET: Ohm’s Law', _PH + 'ohms-law', 'Interactive.'), ('OpenStax UP2, 10.1 Electromotive force', _O2 + '10-1-electromotive-force', 'Sources and internal resistance.')]})
UNITS.append(
{'id': 'u2', 'title': 'Kirchhoff’s Laws, Series and Parallel Resistors, and Voltage and Current Dividers', 'weeks': 'Week 3',
 'summary': 'Nodes, branches and loops, Kirchhoff’s current and voltage laws, series and parallel combinations, equivalent resistance, voltage and current dividers, delta–wye conversions, and measuring with voltmeters and ammeters.',
 'objectives': ['Write KCL and KVL for any circuit.', 'Reduce series–parallel networks to an equivalent resistance.', 'Use voltage and current dividers.', 'Explain how meters are connected and how they load a circuit.'],
 'concepts': ['KCL: the sum of currents leaving any node is zero (charge is conserved). KVL: the sum of voltages around any closed loop is zero (energy is conserved).',
              'Series elements carry the same current; resistances add: R_eq = R₁ + R₂ + …. Parallel elements share the same voltage; conductances add: 1/R_eq = 1/R₁ + 1/R₂ + …; for two resistors R₁R₂/(R₁ + R₂).',
              'Voltage divider: v₂ = v·R₂/(R₁ + R₂). Current divider (two resistors): i₁ = i·R₂/(R₁ + R₂); the larger share goes through the smaller resistor.',
              'Delta–wye (Δ–Y) conversion handles bridges that are neither series nor parallel: R_Y = (product of the two adjacent Δ resistors)/(sum of all three).',
              'A voltmeter goes in parallel and should have very high resistance; an ammeter goes in series and should have very low resistance.'],
 'eqs': [('\\sum i_{\\text{out}}=0', 'KCL'), ('\\sum v=0\\ \\text{around a loop}', 'KVL'), ('R_s=R_1+R_2,\\ \\ R_p=\\frac{R_1R_2}{R_1+R_2}', 'Series and parallel'), ('v_2=v\\frac{R_2}{R_1+R_2},\\ \\ i_1=i\\frac{R_2}{R_1+R_2}', 'Voltage and current dividers')],
 'worked': [
  {'q': 'Resistors of 100, 200 and 300 Ω are in series across 12 V. Find the current and the voltage across the 200 Ω resistor.', 'steps': ['R_eq = 600 Ω; i = 12/600 = 0.02 A.', 'v = 0.02 × 200.'], 'a': 'i = 20 mA, v₂₀₀ = 4 V.'},
  {'q': 'A 9 V source feeds a divider with R₁ = 10 kΩ on top and R₂ = 5 kΩ on the bottom. Find v_out across R₂.', 'steps': ['v_out = 9 × 5/(10 + 5).'], 'a': 'v_out = 3 V.'},
  {'q': 'A 6 A current splits between 2 Ω and 4 Ω in parallel. Find each current.', 'steps': ['i₂Ω = 6 × 4/(2 + 4) = 4 A.', 'i₄Ω = 6 × 2/6 = 2 A; check 4 + 2 = 6.'], 'a': '4 A through 2 Ω and 2 A through 4 Ω.'}],
 'practice': [('Find 6 Ω ∥ 3 Ω.', '18/9 = 2 Ω.'), ('Three 30 Ω resistors are in parallel. Find R_eq.', '10 Ω.'), ('Find R_eq of 10 Ω in series with (20 Ω ∥ 20 Ω).', '10 + 10 = 20 Ω.'),
              ('Three currents enter a node: 2 A, 3 A and −1 A. What current leaves?', '4 A.')],
 'misc': [('Parallel resistance is larger than the smallest resistor.', 'It is always smaller than the smallest one.'), ('A voltage divider works with any load.', 'A load across R₂ is in parallel with it and lowers v_out unless its resistance is much larger.'),
          ('An ammeter goes across the element.', 'Across a low-resistance ammeter is nearly a short circuit; it goes in series.')],
 'quiz': [{'q': 'KCL expresses conservation of…', 'opts': ['energy', 'charge', 'power', 'flux'], 'ok': 1, 'why': 'Charge cannot pile up at a node.'},
          {'q': 'Two equal resistors R in parallel give…', 'opts': ['2R', 'R', 'R/2', 'R²'], 'ok': 2, 'why': 'R·R/(2R).'},
          {'q': 'Series elements share the same…', 'opts': ['voltage', 'current', 'power', 'resistance'], 'ok': 1, 'why': 'One path.'},
          {'q': 'An ideal voltmeter has resistance…', 'opts': ['zero', 'infinite', '1 Ω', 'equal to the load'], 'ok': 1, 'why': 'It must draw no current.'}],
 'cards': [('KCL', 'Currents out of a node sum to 0.'), ('KVL', 'Voltages around a loop sum to 0.'), ('Series', 'R adds; same current.'), ('Parallel', 'G adds; same voltage.'), ('Voltage divider', 'v₂ = vR₂/(R₁ + R₂).'), ('Current divider', 'i₁ = iR₂/(R₁ + R₂).')],
 'planet': {'text': ['Solar panels are series and parallel circuits. The U.S. Energy Information Administration explains that one PV cell can only produce 1 or 2 watts, so cells are electrically connected in weather-tight panels, panels are connected into arrays of two to hundreds of panels, and the number of panels sets how much electricity an array can generate. Cells make direct current, and inverters convert it to the alternating current used on the grid.',
                     'Series connection adds voltages and parallel connection adds currents. As a sample, cells making 0.5 V and 3 A (1.5 W, within EIA’s 1–2 W range) give 30 V at 3 A, or 90 W, when 60 are wired in series. KCL and KVL also explain why one shaded cell in a series string can drag down the whole string, which is why panels include bypass diodes.'],
            'site': [('Physics II', 'Physics_II.html'), ('Parker Solar Probe', 'Parker_Solar_Probe.html')],
            'src': [_PV, ('OpenStax UP2, 10.2 Resistors in series and parallel', _O2 + '10-2-resistors-in-series-and-parallel')]},
 'res': [('OpenStax UP2, 10.2 Resistors in series and parallel', _O2 + '10-2-resistors-in-series-and-parallel', 'Free textbook section.'), ('OpenStax UP2, 10.3 Kirchhoff’s rules', _O2 + '10-3-kirchhoffs-rules', 'KCL and KVL.'),
         (_MIT[0], _MIT[1], 'Lectures on basic circuit analysis.'), ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc', 'Interactive.')]})
UNITS.append(
{'id': 'u3', 'title': 'Systematic Analysis: Node-Voltage and Mesh-Current Methods', 'weeks': 'Weeks 4–5',
 'summary': 'Choosing a reference node, writing KCL in terms of node voltages, supernodes, mesh currents and KVL, supermeshes, circuits with dependent sources, and solving the resulting linear systems by hand and with matrices.',
 'objectives': ['Write and solve node-voltage equations, including supernodes.', 'Write and solve mesh-current equations, including supermeshes.', 'Handle dependent sources in both methods.', 'Choose the method that gives fewer equations.'],
 'concepts': ['Node-voltage method: pick a ground node, name the other node voltages, write KCL at each non-reference node using Ohm’s law (current from a to b through R is (v_a − v_b)/R), and solve.',
              'A voltage source between two non-reference nodes makes a supernode: write one KCL for the combined region plus the source equation v_a − v_b = V_s.',
              'Mesh-current method (planar circuits): assign a clockwise current to each window, write KVL around each mesh; a shared resistor carries the difference of the two mesh currents.',
              'A current source shared by two meshes makes a supermesh: one KVL around the combined loop plus the source equation.',
              'An N-node circuit needs N − 1 node equations; a circuit with M meshes needs M mesh equations. Choose the smaller set. The equations form Gv = i or Ri = v, a linear system.'],
 'eqs': [('\\sum_{\\text{branches}}\\frac{v_n-v_k}{R_{nk}}=i_{\\text{source into }n}', 'KCL at node n'), ('\\sum_{\\text{mesh}} R\\,(i_m-i_{\\text{adj}})=\\sum v_{\\text{sources}}', 'KVL around mesh m'), ('G\\mathbf{v}=\\mathbf{i}', 'Nodal matrix form'), ('R\\mathbf{i}=\\mathbf{v}', 'Mesh matrix form')],
 'worked': [
  {'q': 'A 10 V source feeds node 1 through 2 Ω. Node 1 has 4 Ω to ground and 2 Ω to node 2; node 2 has 4 Ω to ground and a 1 A source flowing into it. Find v₁ and v₂.', 'steps': ['Node 1 (×4): 2(v₁ − 10) + v₁ + 2(v₁ − v₂) = 0, so 5v₁ − 2v₂ = 20.', 'Node 2 (×4): 2(v₂ − v₁) + v₂ − 4 = 0, so −2v₁ + 3v₂ = 4.', 'det = 15 − 4 = 11; v₁ = (60 + 8)/11, v₂ = (20 + 40)/11.'], 'a': 'v₁ = 6.182 V, v₂ = 5.455 V.'},
  {'q': 'Mesh 1 has a 10 V source and 2 Ω; mesh 2 has 6 Ω; the meshes share 4 Ω. Find the mesh currents and the current in the shared resistor.', 'steps': ['Mesh 1: 6i₁ − 4i₂ = 10. Mesh 2: −4i₁ + 10i₂ = 0.', 'det = 60 − 16 = 44; i₁ = 100/44, i₂ = 40/44.'], 'a': 'i₁ = 2.273 A, i₂ = 0.909 A; shared resistor carries 1.364 A.'},
  {'q': 'A 5 V source sits between nodes a and b (v_a − v_b = 5). Node a has 1 Ω to ground, node b has 4 Ω to ground, and 2 A is injected into the supernode. Find v_a and v_b.', 'steps': ['Supernode KCL: v_a/1 + v_b/4 = 2.', 'Substitute v_a = v_b + 5: v_b + 5 + v_b/4 = 2, so 1.25v_b = −3.'], 'a': 'v_b = −2.4 V, v_a = 2.6 V.'}],
 'practice': [('How many node equations does a circuit with 5 nodes need?', '4.'), ('A single node at v connects through 2 Ω to 6 V and through 2 Ω to ground. Find v.', '(v − 6)/2 + v/2 = 0: v = 3 V.'),
              ('Two meshes share a 3 Ω resistor; i₁ = 2 A and i₂ = 0.5 A, both clockwise. Find the current in the shared resistor.', '1.5 A in the direction of i₁.'), ('Write 5v₁ − 2v₂ = 20, −2v₁ + 3v₂ = 4 as Gv = i.', 'G = [[5, −2], [−2, 3]], i = (20, 4).')],
 'misc': [('KCL can be written at the reference node too.', 'It gives a dependent equation; use N − 1 nodes.'), ('Mesh currents are the branch currents.', 'Only on outer branches; shared branches carry differences.'),
          ('A voltage source current is zero because it has no resistance.', 'Its current is set by the rest of the circuit; that is why supernodes are used.')],
 'quiz': [{'q': 'A circuit with 4 nodes needs how many node-voltage equations?', 'opts': ['2', '3', '4', '5'], 'ok': 1, 'why': 'N − 1.'},
          {'q': 'A voltage source between two non-reference nodes calls for…', 'opts': ['a supermesh', 'a supernode', 'a short circuit', 'superposition'], 'ok': 1, 'why': 'Combine the two nodes.'},
          {'q': 'The current in a resistor shared by meshes 1 and 2 is…', 'opts': ['i₁ + i₂', 'i₁ − i₂', 'i₁i₂', 'zero'], 'ok': 1, 'why': 'Both flow clockwise in their own mesh.'},
          {'q': 'Node equations form…', 'opts': ['a differential equation', 'a linear system Gv = i', 'a quadratic', 'a determinant only'], 'ok': 1, 'why': 'Linear resistive circuits are linear systems.'}],
 'cards': [('Reference node', 'Ground, v = 0.'), ('Node-voltage method', 'KCL at N − 1 nodes.'), ('Supernode', 'Voltage source between two nodes.'), ('Mesh-current method', 'KVL around each window.'), ('Supermesh', 'Current source shared by two meshes.'), ('Gv = i', 'Nodal equations in matrix form.')],
 'planet': {'text': ['The power grid is one enormous nodal-analysis problem. EIA explains that the U.S. grid is made up of thousands of miles of high-voltage lines and millions of miles of low-voltage lines connecting thousands of power plants to hundreds of millions of customers. At the start of the 20th century more than 4,000 isolated utilities operated; today the Lower 48 run as three main interconnections, Eastern, Western and ERCOT, linked to provide multiple paths for power to flow.',
                     'EIA notes that supply must match demand at every moment and that balancing authorities keep them matched. Grid operators do that with power-flow models whose equations are the AC version of the node-voltage method in this unit, solved for thousands of buses, and the same analysis tells planners where new lines are needed to connect wind and solar far from cities.'],
            'site': [('Linear Algebra', 'Linear_Algebra.html'), ('Solutions', 'Solutions.html')],
            'src': [_GRID, ('OpenStax UP2, 10.3 Kirchhoff’s rules', _O2 + '10-3-kirchhoffs-rules')]},
 'res': [(_MIT[0], _MIT[1], 'Lectures on the node method and superposition.'), ('OpenStax UP2, 10.3 Kirchhoff’s rules', _O2 + '10-3-kirchhoffs-rules', 'Multi-loop circuits.'),
         ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc', 'Check your node voltages.'), ('Interactive Linear Algebra (Georgia Tech)', 'https://textbooks.math.gatech.edu/ila/', 'Solving the linear systems.')]})
UNITS.append(
{'id': 'u4', 'title': 'Circuit Theorems: Linearity, Superposition, Source Transformation, Thevenin, Norton and Maximum Power Transfer', 'weeks': 'Week 6',
 'summary': 'Linearity and superposition, source transformations, Thevenin and Norton equivalent circuits, finding R_Th by deactivating sources or with a test source, and the maximum power transfer theorem.',
 'objectives': ['Use superposition to analyze circuits with several sources.', 'Convert between voltage and current sources.', 'Find Thevenin and Norton equivalents.', 'Choose a load for maximum power transfer and compute that power.'],
 'concepts': ['Linearity: in a circuit of resistors and sources, every voltage and current is a linear combination of the source values. Superposition: find the response to each independent source alone (other voltage sources shorted, current sources opened) and add.',
              'Source transformation: a voltage source V in series with R is equivalent, at its terminals, to a current source V/R in parallel with R.',
              'Thevenin’s theorem: any linear two-terminal network looks like a source V_Th in series with R_Th. V_Th is the open-circuit voltage; R_Th is the resistance seen with independent sources turned off (or V_oc/i_sc).',
              'Norton’s theorem: the same network is a current source I_N = i_sc in parallel with R_N = R_Th; V_Th = I_N R_Th.',
              'Maximum power transfer: a load receives the most power when R_L = R_Th, and then P_max = V_Th²/(4R_Th). The efficiency at that point is only 50%, so power systems are designed for R_L ≫ R_source instead.'],
 'eqs': [('v=\\sum_k v^{(k)}', 'Superposition'), ('V_{Th}=v_{oc},\\ \\ R_{Th}=\\frac{v_{oc}}{i_{sc}}', 'Thevenin equivalent'), ('I_N=\\frac{V_{Th}}{R_{Th}}', 'Norton current'), ('P_{\\max}=\\frac{V_{Th}^2}{4R_{Th}}\\ \\text{at}\\ R_L=R_{Th}', 'Maximum power transfer')],
 'worked': [
  {'q': 'A 12 V source in series with 4 Ω feeds terminals a–b, with 12 Ω across a–b. Find the Thevenin and Norton equivalents.', 'steps': ['V_Th = 12 × 12/(4 + 12) = 9 V (divider).', 'R_Th = 4 ∥ 12 = 48/16 = 3 Ω (source shorted).', 'I_N = 9/3.'], 'a': 'V_Th = 9 V, R_Th = 3 Ω; I_N = 3 A.'},
  {'q': 'For that circuit, find the power to a 6 Ω load and the maximum possible load power.', 'steps': ['i = 9/(3 + 6) = 1 A; P = 1² × 6 = 6 W.', 'Maximum at R_L = 3 Ω: P_max = 9²/(4 × 3).'], 'a': '6 W; P_max = 6.75 W at 3 Ω.'},
  {'q': 'A node connects to a 10 V source through 5 Ω, to ground through 5 Ω, and receives a 2 A current source. Find the node voltage by superposition.', 'steps': ['10 V alone (2 A opened): divider gives 5 V.', '2 A alone (10 V shorted): 2 × (5 ∥ 5) = 5 V.', 'Add the two.'], 'a': 'v = 10 V. Check KCL: (10 − 10)/5 + 2 = 10/5.'}],
 'practice': [('Convert a 6 V source in series with 2 Ω to a Norton form.', '3 A in parallel with 2 Ω.'), ('A network has v_oc = 15 V and i_sc = 5 A. Find R_Th.', '3 Ω.'),
              ('What load gets maximum power from V_Th = 20 V, R_Th = 5 Ω, and how much?', 'R_L = 5 Ω, P = 400/20 = 20 W.'), ('Can superposition add powers?', 'No: power is not linear; add voltages or currents, then compute power.')],
 'misc': [('Turning off a voltage source means removing it.', 'Replace it with a short circuit; a current source becomes an open circuit.'), ('Maximum power transfer means maximum efficiency.', 'At R_L = R_Th half the power is lost in R_Th.'),
          ('Dependent sources are turned off for R_Th.', 'Keep dependent sources; use a test source to find R_Th.')],
 'quiz': [{'q': 'To find R_Th, independent voltage sources are replaced by…', 'opts': ['opens', 'shorts', 'resistors', 'current sources'], 'ok': 1, 'why': 'Zero volts is a short.'},
          {'q': 'V_Th is the…', 'opts': ['short-circuit current', 'open-circuit voltage', 'source voltage always', 'load voltage'], 'ok': 1, 'why': 'Measured with nothing connected.'},
          {'q': 'Maximum power transfer occurs when…', 'opts': ['R_L = 0', 'R_L = R_Th', 'R_L → ∞', 'R_L = 2R_Th'], 'ok': 1, 'why': 'Matched load.'},
          {'q': 'Efficiency at maximum power transfer is…', 'opts': ['25%', '50%', '75%', '100%'], 'ok': 1, 'why': 'Equal power in R_Th and R_L.'}],
 'cards': [('Superposition', 'Add responses to each source alone.'), ('Source transformation', 'V in series R ↔ V/R in parallel R.'), ('Thevenin', 'V_Th in series with R_Th.'), ('Norton', 'I_N in parallel with R_N.'), ('R_Th', 'v_oc/i_sc.'), ('Max power', 'V_Th²/(4R_Th) at R_L = R_Th.')],
 'planet': {'text': ['Solar cells behave like sources whose Thevenin-style operating point changes with sunlight and temperature, so their electronics constantly hunt for the load that draws the most power. How much of the sunlight they turn into electricity has improved steadily: EIA reports that commercially available PV panels averaged less than 10% efficiency in the mid-1980s, about 15% by 2015, and are now approaching 25% for state-of-the-art modules, while experimental and space cells have reached nearly 50%.',
                     'EIA also reports that U.S. utility-scale PV plants generated about 292 billion kWh in 2025, up from 6 million kWh in 2004, and small-scale rooftop systems about 93 billion kWh. Matching each panel string to its best operating point, the idea behind maximum power transfer, is part of how those kilowatt-hours are squeezed out of every square meter.'],
            'site': [('Physics II', 'Physics_II.html'), ('Space', 'Space.html')],
            'src': [_PV, (_MIT[0], _MIT[1])]},
 'res': [(_MIT[0], _MIT[1], 'Lectures on Thevenin and Norton equivalents.'), ('OpenStax UP2, 10.1 Electromotive force', _O2 + '10-1-electromotive-force', 'Internal resistance and terminal voltage.'),
         ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc', 'Measure v_oc and i_sc.'), ('OpenStax UP2, 10.2 Resistors in series and parallel', _O2 + '10-2-resistors-in-series-and-parallel', 'Equivalent resistance.')]})
UNITS.append(
{'id': 'u5', 'title': 'Operational Amplifiers', 'weeks': 'Week 7',
 'summary': 'The ideal op amp and its two rules, inverting and non-inverting amplifiers, voltage followers, summing and difference amplifiers, saturation, cascaded stages, and op amps in sensors and measurement.',
 'objectives': ['Apply the ideal op-amp rules with negative feedback.', 'Analyze inverting, non-inverting, follower, summing and difference circuits.', 'Recognize saturation and its limits.', 'Design a simple amplifier for a sensor signal.'],
 'concepts': ['An op amp amplifies the difference between its inputs by a very large gain. With negative feedback, the ideal rules are: no current flows into either input, and the two input voltages are equal (v₊ = v₋).',
              'Inverting amplifier: v_o = −(R_f/R_in)v_in. Non-inverting amplifier: v_o = (1 + R_f/R_g)v_in. Voltage follower (buffer): v_o = v_in with almost no current drawn from the source.',
              'Summing amplifier: v_o = −R_f(v₁/R₁ + v₂/R₂ + …). Difference amplifier with matched ratios: v_o = (R₂/R₁)(v₂ − v₁).',
              'The output cannot exceed the supply rails; beyond them the op amp saturates and the linear rules stop applying.',
              'Cascaded stages multiply their gains, and because an op-amp output acts like an ideal voltage source, a stage is not loaded by the next.'],
 'eqs': [('v_+=v_-,\\ \\ i_+=i_-=0', 'Ideal op-amp rules (negative feedback)'), ('v_o=-\\frac{R_f}{R_{in}}v_{in}', 'Inverting amplifier'), ('v_o=\\left(1+\\frac{R_f}{R_g}\\right)v_{in}', 'Non-inverting amplifier'), ('v_o=-R_f\\sum_k\\frac{v_k}{R_k}', 'Summing amplifier')],
 'worked': [
  {'q': 'An inverting amplifier has R_in = 10 kΩ and R_f = 100 kΩ. Find the gain and v_o for v_in = 0.2 V.', 'steps': ['Gain = −100/10 = −10.', 'v_o = −10 × 0.2.'], 'a': 'Gain −10, v_o = −2 V.'},
  {'q': 'Design a non-inverting amplifier with a gain of 10 using R_g = 1 kΩ.', 'steps': ['1 + R_f/R_g = 10, so R_f/R_g = 9.'], 'a': 'R_f = 9 kΩ.'},
  {'q': 'A summing amplifier has R_f = R₁ = R₂ = 10 kΩ, v₁ = 1 V and v₂ = 2 V. Find v_o. What if the supply rails are ±12 V and the gain is raised so the ideal answer is −15 V?', 'steps': ['v_o = −10k(1/10k + 2/10k) = −3 V.', 'The output cannot go below the −12 V rail.'], 'a': 'v_o = −3 V; at the higher gain it saturates near −12 V.'}],
 'practice': [('Find the gain of an inverting amplifier with R_f = 47 kΩ and R_in = 4.7 kΩ.', '−10.'), ('A voltage follower has v_in = 1.5 V. Find v_o.', '1.5 V.'),
              ('Two stages with gains −10 and 5 are cascaded. Find the overall gain.', '−50.'), ('A difference amplifier with R₂/R₁ = 4 has v₂ = 1.2 V and v₁ = 1.0 V. Find v_o.', '4 × 0.2 = 0.8 V.')],
 'misc': [('The op amp inputs draw the circuit current.', 'Ideally no current enters the inputs; it flows through R_f.'), ('v₊ = v₋ always.', 'Only with negative feedback and when not saturated.'),
          ('Gain can be as large as you like.', 'The output is limited by the supply rails and real op-amp bandwidth.')],
 'quiz': [{'q': 'With negative feedback, an ideal op amp makes…', 'opts': ['v₊ = 0', 'v₊ = v₋', 'v_o = 0', 'i_o = 0'], 'ok': 1, 'why': 'Virtual short.'},
          {'q': 'An inverting amplifier with R_f = 20 kΩ, R_in = 5 kΩ has gain…', 'opts': ['4', '−4', '5', '−5'], 'ok': 1, 'why': '−R_f/R_in.'},
          {'q': 'A voltage follower is used to…', 'opts': ['add signals', 'buffer a source', 'invert', 'integrate'], 'ok': 1, 'why': 'Gain 1, no loading.'},
          {'q': 'The minimum gain of a non-inverting amplifier is…', 'opts': ['0', '1', '−1', '10'], 'ok': 1, 'why': '1 + R_f/R_g ≥ 1.'}],
 'cards': [('Ideal op amp', 'v₊ = v₋, no input current.'), ('Inverting', '−R_f/R_in.'), ('Non-inverting', '1 + R_f/R_g.'), ('Follower', 'Gain 1 buffer.'), ('Summing', '−R_f Σ v_k/R_k.'), ('Saturation', 'Output limited by the rails.')],
 'planet': {'text': ['A smarter grid starts with measurement, and measuring small signals is the op amp’s job. EIA explains that the smart grid combines digital technology with the traditional electrical system so utilities and customers can send and receive information, helping utilities reduce electricity losses and detect and fix problems faster, and that smart devices on power lines and at substations let utilities manage voltage more efficiently and quickly pinpoint where an outage is.',
                     'Every smart meter and line sensor scales a tiny current-sensor or voltage-divider signal up to a range a digital converter can read, using exactly the inverting, non-inverting and difference amplifiers in this unit. EIA adds that smart devices can tell customers when prices are high so they can shift use away from times of very high demand.'],
            'site': [('Intro to Programming', 'Intro_to_Programming.html'), ('Solutions', 'Solutions.html')],
            'src': [_GRID, (_MIT[0], _MIT[1])]},
 'res': [(_MIT[0], _MIT[1], 'Lectures on the operational amplifier abstraction.'), ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc', 'Resistor networks for gain setting.'),
         ('OpenStax UP2, 10.2 Resistors in series and parallel', _O2 + '10-2-resistors-in-series-and-parallel', 'Dividers used in feedback.'), ('OpenStax UP2, 9.4 Ohm’s law', _O2 + '9-4-ohms-law', 'Review.')]})
UNITS.append(
{'id': 'u6', 'title': 'Capacitors and Inductors', 'weeks': 'Week 8',
 'summary': 'Capacitance and inductance, their current–voltage relations, stored energy, continuity of capacitor voltage and inductor current, series and parallel combinations, DC steady-state behavior, and op-amp integrators and differentiators.',
 'objectives': ['Use i = C dv/dt and v = L di/dt.', 'Compute energy stored in capacitors and inductors.', 'Combine capacitors and inductors in series and parallel.', 'Find DC steady-state voltages and currents in circuits with C and L.'],
 'concepts': ['A capacitor stores energy in an electric field: q = Cv, i = C dv/dt, w = ½Cv². Its voltage cannot jump instantly; at DC steady state it acts as an open circuit.',
              'An inductor stores energy in a magnetic field: v = L di/dt, w = ½Li². Its current cannot jump instantly; at DC steady state it acts as a short circuit.',
              'Capacitors in parallel add; in series they combine like resistors in parallel. Inductors combine like resistors: series add, parallel combine as reciprocals.',
              'An op amp with a capacitor as feedback integrates: v_o = −(1/RC)∫v_in dt. Swapping R and C gives a differentiator.',
              'Ideal capacitors and inductors store and return energy without loss; real ones have small resistance and leakage.'],
 'eqs': [('i=C\\frac{dv}{dt},\\ \\ w=\\tfrac12Cv^2', 'Capacitor'), ('v=L\\frac{di}{dt},\\ \\ w=\\tfrac12Li^2', 'Inductor'), ('C_p=C_1+C_2,\\ \\ \\frac{1}{C_s}=\\frac{1}{C_1}+\\frac{1}{C_2}', 'Capacitor combinations'), ('v_o=-\\frac{1}{RC}\\int v_{in}\\,dt', 'Op-amp integrator')],
 'worked': [
  {'q': 'A 10 µF capacitor’s voltage rises at 2 V/ms. Find its current.', 'steps': ['dv/dt = 2000 V/s.', 'i = 10 × 10⁻⁶ × 2000.'], 'a': 'i = 20 mA.'},
  {'q': 'Find the energy in a 1000 µF capacitor at 3 V and in a 0.2 H inductor carrying 3 A.', 'steps': ['w_C = ½ × 10⁻³ × 3² = 4.5 × 10⁻³ J.', 'w_L = ½ × 0.2 × 3².'], 'a': '4.5 mJ and 0.9 J.'},
  {'q': 'A 12 V DC source feeds 2 Ω in series with an inductor, with a 4 Ω resistor in parallel with a capacitor across the output (steady state). Find the inductor current and capacitor voltage.', 'steps': ['At DC the inductor is a short and the capacitor is open.', 'i = 12/(2 + 4) = 2 A; v_C = 2 × 4.'], 'a': 'i_L = 2 A, v_C = 8 V.'}],
 'practice': [('Find 6 µF and 3 µF in series.', '2 µF.'), ('A 50 mH inductor’s current changes at 100 A/s. Find its voltage.', '5 V.'),
              ('Find 4 mH and 6 mH in series.', '10 mH.'), ('How much charge does 100 µF hold at 9 V?', 'q = 0.9 mC.')],
 'misc': [('A capacitor passes DC.', 'At DC steady state it blocks current (open circuit).'), ('Inductor current can change instantly.', 'That would need infinite voltage; current is continuous.'),
          ('Capacitors combine like resistors.', 'They combine the opposite way: parallel add.')],
 'quiz': [{'q': 'At DC steady state an inductor acts as…', 'opts': ['an open', 'a short', 'a resistor', 'a source'], 'ok': 1, 'why': 'di/dt = 0 so v = 0.'},
          {'q': 'Doubling a capacitor’s voltage multiplies its energy by…', 'opts': ['2', '4', '½', '1'], 'ok': 1, 'why': 'w ∝ v².'},
          {'q': 'Which cannot change instantly?', 'opts': ['capacitor current', 'capacitor voltage', 'inductor voltage', 'resistor current'], 'ok': 1, 'why': 'It would need infinite current.'},
          {'q': 'Two 10 µF capacitors in parallel give…', 'opts': ['5 µF', '10 µF', '20 µF', '100 µF'], 'ok': 2, 'why': 'Parallel capacitors add.'}],
 'cards': [('Capacitor', 'i = C dv/dt.'), ('Inductor', 'v = L di/dt.'), ('Capacitor energy', '½Cv².'), ('Inductor energy', '½Li².'), ('DC steady state', 'C open, L short.'), ('Integrator', 'v_o = −(1/RC)∫v_in dt.')],
 'planet': {'text': ['Storing energy is what lets solar and wind power be used after sunset or when the wind drops. EIA reported in August 2026 that U.S. utility-scale battery storage capacity grew at an average 70% a year over the last three years, reaching 43.6 GW by the end of 2025, and that operators added another 8.3 GW in the first half of 2026, reaching nearly 52 GW, with about 54 GW more planned over the next two and a half years.',
                     'EIA notes that solar plants host the largest battery units and that solar-plus-storage lets operators store power when prices are low and discharge it when prices are high. Batteries store energy chemically, but the capacitors and inductors of this unit sit in every battery inverter and charger, smoothing currents and storing energy for microseconds at a time as power is converted between DC and AC.'],
            'site': [('Physics II', 'Physics_II.html'), ('Solutions', 'Solutions.html')],
            'src': [_BAT, ('OpenStax UP2, 8.1 Capacitors and capacitance', _O2 + '8-1-capacitors-and-capacitance')]},
 'res': [('OpenStax UP2, 8.1 Capacitors and capacitance', _O2 + '8-1-capacitors-and-capacitance', 'Free textbook section.'), ('OpenStax UP2, 14.2 Self-inductance and inductors', _O2 + '14-2-self-inductance-and-inductors', 'Inductance.'),
         ('PhET: Capacitor Lab: Basics', _PH + 'capacitor-lab-basics', 'Interactive.'), (_MIT[0], _MIT[1], 'Lectures on capacitors and first-order systems.')]})
UNITS.append(
{'id': 'u7', 'title': 'First-Order Circuits: RC and RL Transients', 'weeks': 'Weeks 9–10',
 'summary': 'Natural and step responses of RC and RL circuits, the time constant, the general solution x(t) = x(∞) + [x(0) − x(∞)]e^(−t/τ), switching problems, and energy in digital switching.',
 'objectives': ['Find initial and final values across a switching event.', 'Compute time constants τ = RC and τ = L/R.', 'Write and use the general first-order solution.', 'Estimate switching energy and power in digital circuits.'],
 'concepts': ['A circuit with one capacitor or one inductor (plus resistors and DC sources) obeys a first-order differential equation. Its response moves exponentially from an initial value to a final value.',
              'Time constant: τ = R_Th C for an RC circuit and τ = L/R_Th for an RL circuit, where R_Th is the resistance seen by the C or L.',
              'General solution: x(t) = x(∞) + [x(0⁺) − x(∞)] e^(−t/τ). After one τ the change is 63.2% complete; after 5τ it is 99.3% complete.',
              'Use continuity: v_C(0⁺) = v_C(0⁻) and i_L(0⁺) = i_L(0⁻). Find x(∞) from the DC steady state (C open, L short).',
              'Charging a capacitance C to V through a resistor takes CV² from the source: ½CV² is stored and ½CV² is lost as heat. Digital chips charge tiny capacitances billions of times a second, so their dynamic power is about P = αCV²f.'],
 'eqs': [('\\tau=RC,\\ \\ \\tau=\\frac{L}{R}', 'Time constants'), ('x(t)=x(\\infty)+[x(0^+)-x(\\infty)]e^{-t/\\tau}', 'General first-order response'), ('v_C(t)=V\\left(1-e^{-t/RC}\\right)', 'RC charging from zero'), ('P_{dyn}\\approx\\alpha CV^2f', 'Digital switching power')],
 'worked': [
  {'q': 'A 1000 µF capacitor charges through 10 kΩ from a 3 V source, starting at 0 V. Find τ, v_C at t = τ and the time to reach 99.3% of 3 V.', 'steps': ['τ = 10⁴ × 10⁻³ = 10 s.', 'v_C(τ) = 3(1 − e⁻¹) = 3 × 0.632.', '99.3% takes 5τ.'], 'a': 'τ = 10 s, v_C(τ) = 1.90 V, about 50 s.'},
  {'q': 'A 0.5 H inductor in series with 10 Ω is switched onto 20 V at t = 0. Find τ, the final current and i(0.1 s).', 'steps': ['τ = 0.5/10 = 0.05 s; i(∞) = 20/10 = 2 A.', 'i(0.1) = 2(1 − e^(−0.1/0.05)) = 2(1 − e⁻²).'], 'a': 'τ = 50 ms, i(∞) = 2 A, i(0.1 s) = 1.73 A.'},
  {'q': 'A charged capacitor discharges through a resistor with τ = 10 s. When does its voltage reach half its starting value?', 'steps': ['V₀e^(−t/τ) = V₀/2 gives t = τ ln 2.'], 'a': 't = 6.93 s.'}],
 'practice': [('Find τ for 2 kΩ and 50 µF.', '0.1 s.'), ('After 3τ, what fraction of the change is complete?', '1 − e⁻³ = 95.0%.'),
              ('Find τ for 20 mH and 4 Ω.', '5 ms.'), ('Sample chip: effective switched C = 1 nF, V = 1 V, f = 1 GHz, α = 1. Find P, and P at 0.8 V.', '1 W; 0.64 W, 36% less.')],
 'misc': [('The capacitor voltage jumps when the switch closes.', 'Capacitor voltage is continuous; its current may jump.'), ('The response is complete after one time constant.', 'One τ is 63.2%; use about 5τ for “done”.'),
          ('τ uses the source resistance only.', 'Use the Thevenin resistance seen by the capacitor or inductor.')],
 'quiz': [{'q': 'τ for an RC circuit is…', 'opts': ['R/C', 'RC', '1/RC', '√(RC)'], 'ok': 1, 'why': 'Units of seconds.'},
          {'q': 'After one time constant a charging capacitor reaches about…', 'opts': ['37%', '50%', '63%', '99%'], 'ok': 2, 'why': '1 − e⁻¹.'},
          {'q': 'Lowering a chip’s supply voltage by 20% cuts dynamic power by about…', 'opts': ['20%', '36%', '50%', '64%'], 'ok': 1, 'why': '0.8² = 0.64.'},
          {'q': 'Inductor current at t = 0⁺ equals…', 'opts': ['zero always', 'its value at 0⁻', 'the final value', 'V/R'], 'ok': 1, 'why': 'Continuity.'}],
 'cards': [('RC time constant', 'τ = RC.'), ('RL time constant', 'τ = L/R.'), ('General solution', 'x(∞) + [x(0) − x(∞)]e^(−t/τ).'), ('One τ', '63.2% of the change.'), ('Five τ', '99.3%.'), ('Switching power', 'P ≈ αCV²f.')],
 'planet': {'text': ['Every bit a computer flips charges and discharges a tiny capacitance through a resistance, which is why computing uses so much electricity. A Berkeley Lab report for the U.S. Department of Energy found that data centers consumed about 4.4% of total U.S. electricity in 2023, that their use climbed from 58 TWh in 2014 to 176 TWh in 2023, and that they are expected to use 325 to 580 TWh, or 6.7% to 12% of U.S. electricity, by 2028, with growth driven largely by AI servers.',
                     'The switching-power formula from this unit shows the main lever chip designers have: power grows with the square of the supply voltage, so a 20% lower voltage cuts dynamic power by 36% (sample example). The report’s lead researcher says knowing what drives the growth helps identify opportunities for efficiency.'],
            'site': [('Intro to Programming', 'Intro_to_Programming.html'), ('Differential Equations', 'Differential_Equations.html')],
            'src': [_DC, ('OpenStax UP2, 10.5 RC circuits', _O2 + '10-5-rc-circuits')]},
 'res': [('OpenStax UP2, 10.5 RC circuits', _O2 + '10-5-rc-circuits', 'Free textbook section.'), ('OpenStax UP2, 14.4 RL circuits', _O2 + '14-4-rl-circuits', 'Inductor transients.'),
         (_MIT[0], _MIT[1], 'Lectures on first-order transients and digital circuit energy.'), ('PhET: Circuit Construction Kit: AC', _PH + 'circuit-construction-kit-ac', 'Watch capacitors charge.')]})
UNITS.append(
{'id': 'u8', 'title': 'Second-Order Circuits: RLC Natural and Step Responses', 'weeks': 'Week 11',
 'summary': 'Series and parallel RLC circuits, the characteristic equation, the neper frequency α and resonant frequency ω₀, overdamped, critically damped and underdamped responses, quality factor, and LC energy exchange.',
 'objectives': ['Write the second-order equation for series and parallel RLC circuits.', 'Compute α, ω₀ and ω_d and classify the damping.', 'Find the response form and its constants from initial conditions.', 'Relate Q to ringing and energy loss.'],
 'concepts': ['A circuit with an inductor and a capacitor obeys a second-order equation. For a series RLC: α = R/(2L), ω₀ = 1/√(LC). For a parallel RLC: α = 1/(2RC), same ω₀.',
              'Roots s = −α ± √(α² − ω₀²). Overdamped (α > ω₀): two real roots, no oscillation. Critically damped (α = ω₀): fastest return without overshoot. Underdamped (α < ω₀): decaying oscillation at ω_d = √(ω₀² − α²).',
              'An ideal LC circuit (R = 0) swaps energy between the capacitor’s electric field and the inductor’s magnetic field forever at ω₀.',
              'Quality factor for a series RLC: Q = ω₀L/R = (1/R)√(L/C). High Q means sharp resonance and long ringing.',
              'Critical resistance for a series RLC: R = 2√(L/C).'],
 'eqs': [('\\alpha=\\frac{R}{2L},\\ \\ \\omega_0=\\frac{1}{\\sqrt{LC}}', 'Series RLC parameters'), ('s_{1,2}=-\\alpha\\pm\\sqrt{\\alpha^2-\\omega_0^2}', 'Characteristic roots'), ('\\omega_d=\\sqrt{\\omega_0^2-\\alpha^2}', 'Damped frequency'), ('Q=\\frac{\\omega_0L}{R}', 'Quality factor (series)')],
 'worked': [
  {'q': 'A series RLC has R = 10 Ω, L = 10 mH and C = 10 µF. Find ω₀, f₀, α and the damping type.', 'steps': ['ω₀ = 1/√(10⁻² × 10⁻⁵) = 1/√10⁻⁷ = 3162 rad/s; f₀ = ω₀/2π.', 'α = 10/(2 × 0.01) = 500 s⁻¹ < ω₀.'], 'a': 'ω₀ = 3162 rad/s, f₀ = 503.3 Hz, α = 500 s⁻¹: underdamped.'},
  {'q': 'For the same circuit find ω_d and Q.', 'steps': ['ω_d = √(3162² − 500²) = √(10⁷ − 2.5 × 10⁵).', 'Q = 3162 × 0.01/10.'], 'a': 'ω_d = 3122.5 rad/s, Q = 3.16.'},
  {'q': 'What resistance would make that circuit critically damped?', 'steps': ['R = 2√(L/C) = 2√(0.01/10⁻⁵) = 2√1000.'], 'a': 'R = 63.2 Ω.'}],
 'practice': [('A series RLC has α = 200 s⁻¹ and ω₀ = 100 rad/s. Classify it.', 'Overdamped.'), ('Find ω₀ for L = 1 mH, C = 1 µF.', '31,623 rad/s (5.03 kHz).'),
              ('A parallel RLC has R = 1 kΩ and C = 1 µF. Find α.', '1/(2 × 10³ × 10⁻⁶) = 500 s⁻¹.'), ('Doubling R in a series RLC changes Q by…', 'A factor of ½.')],
 'misc': [('α has the same formula for series and parallel RLC.', 'Series α = R/2L; parallel α = 1/(2RC).'), ('Critically damped means oscillating.', 'It is the boundary: no oscillation, fastest settling.'),
          ('ω_d equals ω₀.', 'ω_d is lower whenever there is damping.')],
 'quiz': [{'q': 'Underdamped means…', 'opts': ['α > ω₀', 'α = ω₀', 'α < ω₀', 'R = 0 only'], 'ok': 2, 'why': 'Complex roots.'},
          {'q': 'ω₀ for an LC circuit is…', 'opts': ['LC', '1/LC', '1/√(LC)', '√(L/C)'], 'ok': 2, 'why': 'Resonant frequency.'},
          {'q': 'Raising R in a series RLC makes the response…', 'opts': ['more oscillatory', 'more damped', 'unchanged', 'unstable'], 'ok': 1, 'why': 'α grows.'},
          {'q': 'In an ideal LC circuit energy…', 'opts': ['is lost as heat', 'swaps between C and L', 'stays in C', 'grows'], 'ok': 1, 'why': 'No resistance.'}],
 'cards': [('Neper frequency', 'α = R/2L (series).'), ('Resonant frequency', 'ω₀ = 1/√(LC).'), ('Overdamped', 'α > ω₀.'), ('Underdamped', 'α < ω₀, rings at ω_d.'), ('Critical R', '2√(L/C) (series).'), ('Q', 'ω₀L/R.')],
 'planet': {'text': ['Resonant circuits are how electric vehicles can charge without a cord. The U.S. Department of Energy’s Alternative Fuels Data Center explains that inductive charging uses an electromagnetic field to transfer electricity to an EV, that some wireless stations already operate at power levels comparable to Level 2, that it is more common for transit and fleets at higher power, and that DOE is researching high-powered wireless charging.',
                     'Wireless chargers tune a coil (L) and a capacitor (C) on each side to the same ω₀ = 1/√(LC) so that energy swaps efficiently across the air gap, and a high Q keeps losses low. That is the circuit idea behind the transit and fleet wireless chargers AFDC describes.'],
            'site': [('Physics II', 'Physics_II.html'), ('Differential Equations', 'Differential_Equations.html')],
            'src': [_EV, ('OpenStax UP2, 14.6 RLC series circuits', _O2 + '14-6-rlc-series-circuits')]},
 'res': [('OpenStax UP2, 14.5 Oscillations in an LC circuit', _O2 + '14-5-oscillations-in-an-lc-circuit', 'Free textbook section.'), ('OpenStax UP2, 14.6 RLC series circuits', _O2 + '14-6-rlc-series-circuits', 'Damped oscillations.'),
         (_MIT[0], _MIT[1], 'Lectures on second-order systems.'), ('PhET: Circuit Construction Kit: AC', _PH + 'circuit-construction-kit-ac', 'Build an LC circuit.')]})
UNITS.append(
{'id': 'u9', 'title': 'Sinusoidal Steady State: Phasors and Impedance', 'weeks': 'Weeks 12–13',
 'summary': 'Sinusoids, amplitude, frequency, phase and RMS values, complex numbers, phasors, impedance and admittance of R, L and C, AC circuit analysis with Ohm’s law, KCL, KVL, nodal and Thevenin methods in phasor form, and frequency response basics.',
 'objectives': ['Convert between time-domain sinusoids and phasors.', 'Compute impedances of R, L and C at a given frequency.', 'Analyze AC circuits with phasor versions of the DC methods.', 'Describe how impedance changes with frequency in simple filters.'],
 'concepts': ['A sinusoid v(t) = V_m cos(ωt + φ) has amplitude V_m, angular frequency ω = 2πf and phase φ. Its RMS value is V_m/√2; U.S. household 120 V is an RMS value at 60 Hz, a peak of about 170 V.',
              'A phasor is the complex number V = V_m∠φ that carries amplitude and phase. In sinusoidal steady state, d/dt becomes multiplication by jω.',
              'Impedance Z = V/I: Z_R = R, Z_L = jωL, Z_C = 1/(jωC) = −j/(ωC). Inductors look like shorts at low frequency and opens at high frequency; capacitors do the opposite.',
              'All the DC tools (series/parallel, dividers, nodal and mesh analysis, Thevenin and Norton) work with impedances and complex arithmetic.',
              'An RC low-pass filter passes low frequencies and attenuates high ones; its cutoff (half-power) frequency is ω_c = 1/(RC).'],
 'eqs': [('V_{rms}=\\frac{V_m}{\\sqrt2}', 'RMS value of a sinusoid'), ('Z_R=R,\\ Z_L=j\\omega L,\\ Z_C=\\frac{1}{j\\omega C}', 'Impedances'), ('\\mathbf{V}=\\mathbf{I}Z', 'Phasor Ohm’s law'), ('\\omega_c=\\frac{1}{RC}', 'RC filter cutoff')],
 'worked': [
  {'q': 'Express v(t) = 170 cos(377t) V as a phasor and find its RMS value and frequency.', 'steps': ['V = 170∠0° V (peak).', 'V_rms = 170/√2; f = 377/(2π).'], 'a': 'V_rms = 120.2 V at f = 60.0 Hz.'},
  {'q': 'At 60 Hz find the impedance of a 0.1 H inductor and a 100 µF capacitor.', 'steps': ['ω = 2π × 60 = 377.0 rad/s.', 'Z_L = j × 377.0 × 0.1; Z_C = −j/(377.0 × 10⁻⁴).'], 'a': 'Z_L = j37.70 Ω, Z_C = −j26.53 Ω.'},
  {'q': 'A 120 V (RMS), 60 Hz source drives 30 Ω in series with 0.1 H. Find the current and its phase.', 'steps': ['Z = 30 + j37.70 Ω; |Z| = √(30² + 37.70²) = 48.18 Ω, ∠51.49°.', 'I = 120/48.18 at −51.49°.'], 'a': 'I = 2.491 A RMS, lagging the voltage by 51.49°.'}],
 'practice': [('Find the RMS value of a sinusoid with 10 V peak.', '7.071 V.'), ('Find the impedance of 1 µF at ω = 1000 rad/s.', '−j1000 Ω.'),
              ('Find the cutoff frequency of an RC filter with R = 1 kΩ and C = 1 µF.', 'ω_c = 1000 rad/s (159.2 Hz).'), ('Convert 3 + j4 to polar form.', '5∠53.13°.')],
 'misc': [('120 V AC means a 120 V peak.', 'It is the RMS value; the peak is about 170 V.'), ('Impedances add like magnitudes.', 'Add complex numbers: 30 + j40 has magnitude 50, not 70.'),
          ('Phasors work for any waveform.', 'They apply to sinusoidal steady state at one frequency.')],
 'quiz': [{'q': 'The impedance of an inductor is…', 'opts': ['jωL', '1/(jωL)', 'ωL', 'L/ω'], 'ok': 0, 'why': 'v = L di/dt → jωL.'},
          {'q': 'At very high frequency a capacitor acts like…', 'opts': ['an open', 'a short', 'a resistor', 'an inductor'], 'ok': 1, 'why': '|Z_C| = 1/(ωC) → 0.'},
          {'q': 'The RMS value of a sine wave is its peak times…', 'opts': ['0.5', '0.637', '0.707', '1.414'], 'ok': 2, 'why': '1/√2.'},
          {'q': 'In an RL circuit the current…', 'opts': ['leads the voltage', 'lags the voltage', 'is in phase', 'is zero'], 'ok': 1, 'why': 'Inductive phase angle.'}],
 'cards': [('Phasor', 'V_m∠φ.'), ('RMS', 'V_m/√2.'), ('Z_L', 'jωL.'), ('Z_C', '1/(jωC).'), ('Phasor Ohm’s law', 'V = IZ.'), ('RC cutoff', 'ω_c = 1/RC.')],
 'planet': {'text': ['Home EV charging is an AC circuit problem. The Alternative Fuels Data Center explains that AC Level 1 charging uses a 120 V plug, assumes about 1.9 kW, and adds about 5 miles of range per hour, so 8 hours can replenish about 40 miles for a mid-size EV. AC Level 2 uses 240 V (homes) or 208 V (commercial); most residential Level 2 chargers run at up to 30 A, delivering 7.2 kW and about 25 miles of range per hour, and need a dedicated 40 A circuit under National Electrical Code Article 625.',
                     'Those are RMS values: 1.9 kW at 120 V means about 15.8 A, and 7.2 kW at 240 V is 30 A. AFDC adds that as of 2023 nearly 80% of public charging ports were Level 2, and that Level 2 units range from 2.9 to 19.2 kW. Most EV owners do most of their charging at home.'],
            'site': [('Physics II', 'Physics_II.html'), ('Solutions', 'Solutions.html')],
            'src': [_EV, ('OpenStax UP2, 15.2 Simple AC circuits', _O2 + '15-2-simple-ac-circuits')]},
 'res': [('OpenStax UP2, 15.2 Simple AC circuits', _O2 + '15-2-simple-ac-circuits', 'Free textbook section.'), ('OpenStax UP2, 15.3 RLC series circuits with AC', _O2 + '15-3-rlc-series-circuits-with-ac', 'Impedance and phase.'),
         (_MIT[0], _MIT[1], 'Lectures on sinusoidal steady state and impedance.'), ('PhET: Circuit Construction Kit: AC', _PH + 'circuit-construction-kit-ac', 'Interactive.')]})
UNITS.append(
{'id': 'u10', 'title': 'AC Power, Power Factor, Resonance, Transformers and Three-Phase Systems', 'weeks': 'Week 14',
 'summary': 'Instantaneous and average power, real, reactive and apparent power, the power triangle, power factor and its correction, series resonance and bandwidth, ideal transformers, balanced three-phase systems, and why the grid transmits at high voltage.',
 'objectives': ['Compute real, reactive and apparent power and the power factor.', 'Size a capacitor for power-factor correction.', 'Analyze ideal transformers and balanced three-phase loads.', 'Explain transmission losses with I²R.'],
 'concepts': ['Average (real) power P = V_rms I_rms cos θ in watts, where θ is the angle between voltage and current. Reactive power Q = V_rms I_rms sin θ in VAR. Apparent power S = V_rms I_rms in VA, and S² = P² + Q².',
              'Power factor pf = cos θ = P/S. Motors are inductive (lagging pf). A parallel capacitor supplies reactive power locally, raising pf and cutting the current the utility must deliver: C = Q/(ωV²) for full correction.',
              'At series resonance ω₀ = 1/√(LC) the reactances cancel, the impedance is just R and current is largest; the bandwidth is ω₀/Q.',
              'An ideal transformer with turns ratio N₁:N₂ has V₂/V₁ = N₂/N₁ and I₂/I₁ = N₁/N₂, so power in equals power out.',
              'Balanced three-phase: three sinusoids 120° apart. Total power P = √3 V_L I_L cos θ, constant in time. Line losses are I²R, so raising voltage by k for the same power cuts current by k and losses by k².'],
 'eqs': [('P=V_{rms}I_{rms}\\cos\\theta,\\ \\ Q=V_{rms}I_{rms}\\sin\\theta', 'Real and reactive power'), ('S^2=P^2+Q^2,\\ \\ \\text{pf}=\\frac{P}{S}', 'Power triangle'), ('\\frac{V_2}{V_1}=\\frac{N_2}{N_1}=\\frac{I_1}{I_2}', 'Ideal transformer'), ('P_{3\\phi}=\\sqrt3\\,V_LI_L\\cos\\theta', 'Balanced three-phase power')],
 'worked': [
  {'q': 'A motor draws 20 A RMS from 240 V RMS at a power factor of 0.8 lagging. Find S, P and Q.', 'steps': ['S = 240 × 20 = 4800 VA.', 'P = 4800 × 0.8; sin θ = 0.6, so Q = 4800 × 0.6.'], 'a': 'S = 4.8 kVA, P = 3.84 kW, Q = 2.88 kVAR.'},
  {'q': 'What capacitor in parallel would correct that motor to unity power factor at 60 Hz?', 'steps': ['The capacitor must supply Q = 2880 VAR.', 'C = Q/(ωV²) = 2880/(377.0 × 240²).'], 'a': 'C = 132.6 µF; the line current falls from 20 A to 16 A.'},
  {'q': 'A line with 5 Ω resistance delivers 10 MW. Compare the I²R loss at 100 kV and at 20 kV (unity power factor, single-phase sample).', 'steps': ['At 100 kV: I = 10⁷/10⁵ = 100 A, loss = 100² × 5 = 50 kW (0.5%).', 'At 20 kV: I = 500 A, loss = 500² × 5 = 1.25 MW (12.5%).'], 'a': '5 times the voltage cuts losses 25 times.'}],
 'practice': [('A load has P = 6 kW and Q = 8 kVAR. Find S and pf.', 'S = 10 kVA, pf = 0.6.'), ('A transformer steps 7200 V down to 240 V. Find N₁:N₂.', '30:1.'),
              ('Find the power of a balanced 480 V three-phase load drawing 100 A at pf 0.9.', '√3 × 480 × 100 × 0.9 = 74.8 kW.'), ('A series RLC has ω₀ = 1000 rad/s and Q = 20. Find the bandwidth.', '50 rad/s.')],
 'misc': [('Reactive power does no work, so it does not matter.', 'It still raises the current, and current causes I²R losses in wires and transformers.'), ('A transformer works on DC.', 'It needs a changing flux; DC gives none.'),
          ('Three-phase power is three times single-phase with the line voltage.', 'P = √3 V_L I_L cos θ.')],
 'quiz': [{'q': 'Power factor equals…', 'opts': ['Q/S', 'P/S', 'S/P', 'P/Q'], 'ok': 1, 'why': 'cos θ.'},
          {'q': 'Raising transmission voltage 10 times (same power) cuts I²R losses by…', 'opts': ['10×', '100×', '√10×', 'none'], 'ok': 1, 'why': 'Current falls 10×; loss ∝ I².'},
          {'q': 'An inductive load is corrected with a…', 'opts': ['series resistor', 'parallel capacitor', 'parallel inductor', 'transformer'], 'ok': 1, 'why': 'Capacitors supply reactive power.'},
          {'q': 'A step-down transformer with 10:1 turns makes the secondary current…', 'opts': ['10× smaller', '10× larger', 'equal', '100× larger'], 'ok': 1, 'why': 'Power is conserved.'}],
 'cards': [('Real power', 'P = VI cos θ (W).'), ('Reactive power', 'Q = VI sin θ (VAR).'), ('Apparent power', 'S = VI (VA).'), ('Power factor', 'P/S.'), ('Transformer', 'V₂/V₁ = N₂/N₁.'), ('Three-phase', 'P = √3 V_L I_L cos θ.')],
 'planet': {'text': ['The grid moves power at high voltage to keep I²R losses down. EIA explains that high-voltage transmission lines carry electricity over long distances because higher voltage makes long-distance transmission more efficient and less expensive, lower-voltage distribution lines deliver it to customers, and transformers at substations step voltages up and down between the stages. EIA estimates that transmission and distribution losses averaged about 5% of the electricity transmitted and distributed in the United States in 2018 through 2022.',
                     'The worked example shows the physics: five times the voltage cuts losses twenty-five times. Power-factor correction, efficient transformers and new long-distance lines to reach wind and solar resources, which EIA lists among the grid’s challenges, all chip away at that 5%. AFDC notes that common U.S. three-phase voltages are 208/120 V and 480/277 V, common at commercial and industrial sites, and that DC fast chargers typically take a three-phase AC input.'],
            'site': [('Solutions', 'Solutions.html'), ('Physics II', 'Physics_II.html')],
            'src': [_GRID, _TD, ('OpenStax UP2, 15.6 Transformers', _O2 + '15-6-transformers')]},
 'res': [('OpenStax UP2, 15.4 Power in an AC circuit', _O2 + '15-4-power-in-an-ac-circuit', 'Free textbook section.'), ('OpenStax UP2, 15.5 Resonance in an AC circuit', _O2 + '15-5-resonance-in-an-ac-circuit', 'Resonance and bandwidth.'),
         ('OpenStax UP2, 15.6 Transformers', _O2 + '15-6-transformers', 'Transformers and transmission.'), ('PhET: Faraday’s Law', _PH + 'faradays-law', 'Induction behind transformers.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Ohm’s law and the multimeter', 'week': 'Week 2',
 'goal': 'Measure voltage, current and resistance correctly, show that current is proportional to voltage for a resistor, and find R from the slope.',
 'eq': ('v=iR,\\quad p=vi', 'Ohm’s law and power'),
 'steps': ['Open PhET Ohm’s Law and Circuit Construction Kit: DC; build a battery and resistor and add a voltmeter (in parallel) and ammeter (in series).', 'Home: on a breadboard, connect a 1 kΩ resistor to one AA cell (1.5 V) and then to two (3 V). Measure v across the resistor and i in series with the meter on its mA range.',
           'Measure the resistor alone with the Ω range (power disconnected) and compare with v/i.', 'Plot i against v; the slope is 1/R. Compute the power in each case.'],
 'table': (['v (V)', 'i (mA) for 1 kΩ', 'p (mW)'], [['1.5', '1.5', '2.25'], ['3.0', '3.0', '9.0']]),
 'note': 'Ideal values for a 1 kΩ resistor; fresh cells read a little above 1.5 V each and resistors are within their tolerance (often ±5%).',
 'calc': ['R = v/i = 3.0/0.003 = 1000 Ω.', 'p = vi = 3.0 × 0.003 = 9 mW, far below a ¼ W resistor rating.'],
 'safety': ['Use only 1.5–3 V battery packs; never connect to a wall outlet.', 'Never connect the meter on its current range directly across a battery: it is a short circuit.'], 'home': ['The breadboard version is the home lab.'],
 'sims': [('PhET: Ohm’s Law', _PH + 'ohms-law'), ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc')],
 'planet': 'The same v·i measurement is what a plug-in meter or smart meter does to show where energy goes; DOE says LEDs use at least 75% less than incandescents.', 'planet_src': [_LED]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Kirchhoff’s laws, series and parallel, and dividers', 'week': 'Week 3',
 'goal': 'Verify KVL and KCL by measurement, check series and parallel equivalent resistance, and see a voltage divider sag under load.',
 'eq': ('\\sum v=0,\\quad \\sum i=0,\\quad v_2=v\\frac{R_2}{R_1+R_2}', 'KVL, KCL and the divider'),
 'steps': ['Build 1 kΩ and 2 kΩ in series across 3 V (PhET or breadboard). Measure the current and each voltage; check that the voltages add to the source.', 'Rebuild two 1 kΩ resistors in parallel across 3 V. Measure the current in each branch and in the source lead; check KCL.',
           'Treat the series pair as a divider and measure v across the 2 kΩ resistor.', 'Connect a 2 kΩ “load” across the 2 kΩ resistor and measure again; explain the drop with the parallel combination.'],
 'table': (['Circuit', 'Current', 'Voltages'], [['1 kΩ + 2 kΩ series', '1.0 mA', '1.0 V and 2.0 V'], ['1 kΩ ∥ 1 kΩ', '3.0 mA each, 6.0 mA total', '3.0 V'], ['Divider loaded by 2 kΩ', '1.5 mA from source', '1.5 V out']]),
 'note': 'Ideal values for a 3 V source.',
 'calc': ['Series: i = 3/3000 = 1 mA; 1 V + 2 V = 3 V (KVL).', 'Loaded divider: 2 kΩ ∥ 2 kΩ = 1 kΩ, so v_out = 3 × 1/(1 + 1) = 1.5 V instead of 2 V.'],
 'safety': ['Low-voltage battery packs only; remove the battery before rewiring.'], 'home': ['The breadboard version is the home lab.'],
 'sims': [('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc')],
 'planet': 'EIA explains that PV cells are wired into panels and arrays; series strings add voltage and parallel strings add current, as here.', 'planet_src': [_PV]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: A battery’s Thevenin equivalent and maximum power', 'week': 'Week 6',
 'goal': 'Model a real battery as V_Th in series with R_Th by measuring its open-circuit and loaded voltage, then predict the load for maximum power.',
 'eq': ('R_{Th}=\\frac{v_{oc}-v_L}{i_L},\\quad P_{\\max}=\\frac{V_{Th}^2}{4R_{Th}}', 'Thevenin from two measurements'),
 'steps': ['In PhET Circuit Construction Kit: DC, give the battery an internal resistance and measure its voltage with no load and with a load resistor.', 'Home: measure a 2 × AA pack’s open-circuit voltage. Then connect a 22 Ω resistor rated at least 1 W for a few seconds only and read the voltage.',
           'Compute i_L = v_L/22 Ω and R_Th, and predict P_max.', 'In PhET, sweep the load resistance and confirm the power peaks when R_L = R_Th.'],
 'table': (['Quantity', 'Sample value'], [['v_oc', '3.20 V'], ['v_L (22 Ω)', '3.10 V'], ['i_L', '0.141 A'], ['R_Th', '0.71 Ω']]),
 'note': 'Sample values for fresh alkaline cells; worn cells show a much larger R_Th.',
 'calc': ['i_L = 3.10/22 = 0.1409 A; R_Th = 0.10/0.1409 = 0.71 Ω.', 'Load power = 3.10 × 0.1409 = 0.437 W, so use a 1 W resistor. Matching R_L = 0.71 Ω would be close to a short and heat the cells: do not try it at home, only in PhET.'],
 'safety': ['Connect the 22 Ω load only for a few seconds; the resistor and cells get warm.', 'Never short the battery terminals.'], 'home': ['The two-measurement step is the home lab; the power sweep is PhET only.'],
 'sims': [('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc'), ('OpenStax UP2, 10.1 Electromotive force', _O2 + '10-1-electromotive-force')],
 'planet': 'EIA reports PV module efficiency rising from under 10% in the mid-1980s to nearly 25% now; operating each panel at its best load is part of using that output.', 'planet_src': [_PV]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: RC charging and the time constant', 'week': 'Week 10',
 'goal': 'Watch a capacitor charge through a resistor, measure the time constant, and compare with τ = RC.',
 'eq': ('v_C(t)=V\\left(1-e^{-t/RC}\\right)', 'RC charging'),
 'steps': ['In PhET Circuit Construction Kit: AC, build a battery, resistor, capacitor and switch; use the voltage chart to watch v_C.', 'Home: put a 1000 µF capacitor (rated 6.3 V or more, negative lead to battery −) in series with 10 kΩ across 3 V. Read v_C with the multimeter every 10 s.',
           'Find the time at which v_C reaches 63.2% of the final voltage; that is τ.', 'Plot ln(1 − v_C/V) against t; the slope is −1/τ. Discharge the capacitor through the resistor before storing it.'],
 'table': (['t (s)', '0', '10', '20', '30', '50'], [['v_C (V)', '0', '1.90', '2.59', '2.85', '2.98']]),
 'note': 'Ideal values for R = 10 kΩ, C = 1000 µF and V = 3 V. Electrolytic capacitors are often within ±20%, and the meter itself loads the circuit slightly.',
 'calc': ['τ = 10⁴ × 10⁻³ = 10 s.', 'v_C(10 s) = 3(1 − e⁻¹) = 1.90 V; v_C(50 s) = 3(1 − e⁻⁵) = 2.98 V.'],
 'safety': ['Insert electrolytic capacitors with the correct polarity and below their voltage rating; reversed ones can burst. Wear glasses.'], 'home': ['The breadboard version is the home lab.'],
 'sims': [('PhET: Circuit Construction Kit: AC', _PH + 'circuit-construction-kit-ac'), ('PhET: Capacitor Lab: Basics', _PH + 'capacitor-lab-basics')],
 'planet': 'Berkeley Lab reports data centers used about 4.4% of U.S. electricity in 2023; every logic switch inside them is a tiny RC charge like this one.', 'planet_src': [_DC]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: RLC resonance', 'week': 'Week 13',
 'goal': 'Drive a series RLC circuit with an AC source at different frequencies, find the resonant peak, and compare with ω₀ = 1/√(LC).',
 'eq': ('|I|=\\frac{V}{\\sqrt{R^2+(\\omega L-1/\\omega C)^2}}', 'Series RLC current'),
 'steps': ['In PhET Circuit Construction Kit: AC (or its Virtual Lab), build an AC source, resistor, inductor and capacitor in series with an ammeter.', 'Set R = 10 Ω, L = 10 mH and C = 10 µF if available, or note the values PhET uses, and compute f₀.',
           'Step the source frequency through f₀ and record the current amplitude.', 'Plot |I| against f, find the peak and the half-power points, and compare the bandwidth with ω₀/Q.'],
 'table': (['f (Hz)', '400', '503', '600'], [['|I| (A) for 10 V', '0.563', '1.000', '0.667']]),
 'note': 'Calculated values for R = 10 Ω, L = 10 mH, C = 10 µF and a 10 V amplitude source.',
 'calc': ['f₀ = 1/(2π√(10⁻² × 10⁻⁵)) = 503.3 Hz; at f₀, |Z| = R = 10 Ω, so |I| = 1 A.', 'At 400 Hz: X_L = 25.13 Ω, X_C = 39.79 Ω, |Z| = 17.76 Ω, |I| = 0.563 A.'],
 'safety': ['Simulation only: do not build AC circuits from wall power.'], 'home': ['This lab is PhET-only for safety; no home wiring.'],
 'sims': [('PhET: Circuit Construction Kit: AC', _PH + 'circuit-construction-kit-ac'), ('PhET: Circuit Construction Kit: AC – Virtual Lab', _PH + 'circuit-construction-kit-ac-virtual-lab')],
 'planet': 'AFDC says inductive EV chargers transfer power through an electromagnetic field; tuned LC circuits like this one make that transfer efficient.', 'planet_src': [_EV]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Measuring real power at home and transformers in PhET', 'week': 'Week 14',
 'goal': 'Use a plug-in power meter to compare the real power of light bulbs and appliances, estimate annual energy, and explore transformer voltage ratios in PhET.',
 'eq': ('w=Pt,\\quad \\frac{V_2}{V_1}=\\frac{N_2}{N_1}', 'Energy and the ideal transformer'),
 'steps': ['Plug a power meter into a wall outlet and plug a lamp into the meter (never open the meter or the lamp). Record watts with an incandescent or halogen bulb and then with an LED of similar brightness.', 'If the meter shows VA and power factor, record them for a phone charger and a fan too.',
           'Estimate annual kWh at 3 hours a day and compare.', 'In PhET Faraday’s Law, change the number of coil turns and the magnet speed, and relate the induced voltage to N and the rate of change of flux.'],
 'table': (['Bulb', 'P (W)', 'kWh/yr at 3 h/day'], [['Incandescent', '60', '65.7'], ['LED (similar light)', '9', '9.9']]),
 'note': 'Sample readings; DOE’s guide says LEDs use at least 75% less energy than incandescents. Your bulbs set your numbers.',
 'calc': ['60 W × 3 h × 365 = 65.7 kWh; 9 W gives 9.86 kWh.', 'Savings = 85% for this sample LED, consistent with “at least 75%”.'],
 'safety': ['Use only a commercial plug-in meter and plug-in appliances; never touch outlet contacts or open devices. Let hot bulbs cool before handling.'], 'home': ['The plug-in meter step is the home lab; transformers are explored in PhET.'],
 'sims': [('PhET: Faraday’s Law', _PH + 'faradays-law'), ('OpenStax UP2, 15.6 Transformers', _O2 + '15-6-transformers')],
 'planet': 'EIA estimates transmission and distribution losses at about 5%; every watt saved at the bulb also avoids those losses upstream.', 'planet_src': [_LED, _TD]})
SCHEDULE = [(1, 'u1', 'Charge, current, voltage, power, sign convention, sources', 'MIT 6.002; OpenStax UP2 9.4'), (2, 'u1', 'Ohm’s law, resistivity, energy in kWh; Lab A', 'UP2 9.4, 10.1'),
            (3, 'u2', 'KCL, KVL, series and parallel, dividers, meters; Lab B', 'UP2 10.2–10.3'), (4, 'u3', 'Node-voltage method and supernodes', 'MIT 6.002'),
            (5, 'u3', 'Mesh-current method, supermeshes, dependent sources', 'MIT 6.002; UP2 10.3'), (6, 'u4', 'Superposition, source transformation, Thevenin, Norton, maximum power; Lab C', 'MIT 6.002'),
            (7, 'u5', 'Operational amplifiers; midterm practice', 'MIT 6.002'), (8, 'u6', 'Capacitors, inductors, energy, integrators', 'UP2 8.1, 14.2'),
            (9, 'u7', 'RC and RL natural and step responses', 'UP2 10.5, 14.4'), (10, 'u7', 'Switching problems and digital switching energy; Lab D', 'MIT 6.002'),
            (11, 'u8', 'Series and parallel RLC, damping, LC oscillation', 'UP2 14.5–14.6'), (12, 'u9', 'Sinusoids, phasors, impedance', 'UP2 15.2–15.3'),
            (13, 'u9', 'AC nodal, mesh and Thevenin analysis, filters; Lab E', 'MIT 6.002; UP2 15.3, 15.5'), (14, 'u10', 'AC power, power factor, transformers, three-phase; Lab F', 'UP2 15.4–15.6'),
            (15, 'exam', 'Review and final practice set', 'All units')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Find the equivalent resistance of 12 Ω in parallel with (4 Ω + 2 Ω).', ['12 × 6/(12 + 6).'], '4 Ω.'),
  ('A 24 V source feeds 3 kΩ and 1 kΩ in series. Find the voltage across 1 kΩ.', ['Divider: 24 × 1/4.'], '6 V.'),
  ('A node connects to 12 V through 4 Ω, to ground through 12 Ω, and receives 2 A from a current source. Find its voltage.', ['(v − 12)/4 + v/12 = 2, so 4v = 60.'], '15 V.'),
  ('A network has v_oc = 18 V and i_sc = 6 A. Find R_Th and the maximum power it can deliver.', ['R_Th = 3 Ω; P = 18²/(4 × 3).'], '3 Ω and 27 W.'),
  ('An inverting amplifier has R_f = 33 kΩ and R_in = 3.3 kΩ. Find v_o for v_in = −0.4 V.', ['Gain = −10.'], '+4 V.')]),
 ('Final practice set (all units)', [
  ('A 20 µF capacitor charges from 0 V through 5 kΩ toward 10 V. Find τ and v_C at 0.2 s.', ['τ = 0.1 s; 10(1 − e⁻²).'], 'τ = 0.1 s, v_C = 8.65 V.'),
  ('A series RLC has R = 40 Ω, L = 0.1 H and C = 100 µF. Classify the response and find ω_d if it rings.', ['α = 200 s⁻¹; ω₀ = 316.2 rad/s.'], 'Underdamped, ω_d = 244.9 rad/s.'),
  ('Find the impedance of 20 Ω in series with 100 µF at 60 Hz.', ['Z_C = −j26.53 Ω.'], 'Z = 20 − j26.53 Ω = 33.22∠−52.99° Ω.'),
  ('A load draws 12 A RMS from 120 V RMS at pf 0.85 lagging. Find P and Q.', ['S = 1440 VA; sin θ = 0.5268.'], 'P = 1224 W, Q = 758.6 VAR.'),
  ('A 20:1 transformer has 2400 V on its primary and a 10 A secondary load. Find V₂ and I₁.', ['V₂ = 2400/20; I₁ = 10/20.'], '120 V and 0.5 A.'),
  ('Find the power of a balanced 208 V three-phase load drawing 50 A at unity power factor.', ['√3 × 208 × 50.'], '18.01 kW.')])]
FORMULAS = ['i=dq/dt,\\ p=vi,\\ v=iR', 'R=\\rho L/A,\\ p=i^2R=v^2/R', '\\sum i=0,\\ \\sum v=0', 'R_s=\\sum R,\\ 1/R_p=\\sum 1/R', 'v_2=vR_2/(R_1+R_2)',
            'V_{Th}=v_{oc},\\ R_{Th}=v_{oc}/i_{sc},\\ P_{\\max}=V_{Th}^2/(4R_{Th})', 'v_o=-(R_f/R_{in})v_{in},\\ v_o=(1+R_f/R_g)v_{in}', 'i=C\\,dv/dt,\\ v=L\\,di/dt,\\ w=\\tfrac12Cv^2,\\ \\tfrac12Li^2',
            '\\tau=RC,\\ L/R;\\ x(t)=x(\\infty)+[x(0)-x(\\infty)]e^{-t/\\tau}', '\\alpha=R/2L,\\ \\omega_0=1/\\sqrt{LC},\\ \\omega_d=\\sqrt{\\omega_0^2-\\alpha^2}', 'Z_L=j\\omega L,\\ Z_C=1/(j\\omega C),\\ V_{rms}=V_m/\\sqrt2',
            'P=VI\\cos\\theta,\\ Q=VI\\sin\\theta,\\ S^2=P^2+Q^2', 'V_2/V_1=N_2/N_1,\\ P_{3\\phi}=\\sqrt3V_LI_L\\cos\\theta']
GLOSSARY = sorted([('Apparent power', 'S = V_rms I_rms, in VA.'), ('Capacitor', 'Element with i = C dv/dt that stores energy in an electric field.'), ('Impedance', 'Complex ratio V/I in sinusoidal steady state.'),
    ('Inductor', 'Element with v = L di/dt that stores energy in a magnetic field.'), ('KCL', 'Currents leaving a node sum to zero.'), ('KVL', 'Voltages around a loop sum to zero.'),
    ('Mesh', 'A loop that contains no other loop.'), ('Node', 'A point where two or more elements connect.'), ('Norton equivalent', 'Current source I_N in parallel with R_N.'),
    ('Op amp', 'High-gain differential amplifier used with feedback.'), ('Passive sign convention', 'Current enters the + terminal of an element that absorbs power.'), ('Phasor', 'Complex number giving a sinusoid’s amplitude and phase.'),
    ('Power factor', 'cos θ = P/S.'), ('Quality factor', 'Q = ω₀L/R, sharpness of resonance.'), ('Reactive power', 'Q = V_rms I_rms sin θ, in VAR.'), ('RMS', 'Root-mean-square value; V_m/√2 for a sinusoid.'),
    ('Supernode', 'Two nodes joined by a voltage source, treated together in KCL.'), ('Thevenin equivalent', 'Voltage source V_Th in series with R_Th.'), ('Time constant', 'τ = RC or L/R.'),
    ('Transformer', 'Coupled coils that change AC voltage by the turns ratio.')])
RUBRIC = [('4 · Mastery', 'Labels circuits fully, chooses an efficient method (dividers, nodal, mesh, Thevenin, phasors), checks power balance and limiting cases, and works safely in the lab.'), ('3 · Proficient', 'Solves the practice problems with occasional sign or unit slips.'),
          ('2 · Developing', 'Follows worked examples but mixes up series and parallel, or the sign convention.'), ('1 · Beginning', 'Plugs numbers into formulas without a labeled diagram; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    par = lambda *r: 1 / sum(1 / x for x in r)
    w60 = 2 * pi * 60
    d2 = lambda a, b, c, d: a * d - b * c
    zmag = lambda r, x: sqrt(r * r + x * x)
    zang = lambda r, x: degrees(atan2(x, r))
    v1 = (20 * 3 + 2 * 4) / 11; v2 = (5 * 4 + 2 * 20) / 11
    i1 = 100 / 44; i2 = 40 / 44
    vb = -3 / 1.25
    w0 = 1 / sqrt(1e-2 * 1e-5); al = 10 / (2 * .01); wd = sqrt(w0**2 - al**2)
    XL = lambda f, L: 2 * pi * f * L
    XC = lambda f, C: 1 / (2 * pi * f * C)
    Ie = lambda f: 10 / zmag(10, XL(f, .01) - XC(f, 1e-5))
    Z9 = zmag(30, w60 * .1)
    r = [
     ('u1 i', 12 / 4, 3), ('u1 p', 12 * 3, 36), ('u1 R', 1.68e-8 * 10 / 1e-6, .168), ('u1 led', .25 * 60, 15), ('u1 inc', 60 * 3 * 365 / 1000, 65.7), ('u1 ledkwh', 15 * 3 * 365 / 1000, 16.4),
     ('u1 save', 45 * 3 * 365 / 1000, 49.3), ('u1 q', 2 * 30, 60), ('u1 p2', 120 * .5, 60), ('u1 R2', 120 / .5, 240), ('u1 pd', 5 * -2, -10), ('u1 2kWh', 2 * 3.6e6, 7.2e6), ('u1 kwh', 1000 * 3600, 3.6e6),
     ('u2 Req', 100 + 200 + 300, 600), ('u2 i', 12 / 600, .02), ('u2 v', .02 * 200, 4), ('u2 div', 9 * 5 / 15, 3), ('u2 cd1', 6 * 4 / 6, 4), ('u2 cd2', 6 * 2 / 6, 2), ('u2 p63', par(6, 3), 2),
     ('u2 p30', par(30, 30, 30), 10), ('u2 mix', 10 + par(20, 20), 20), ('u2 kcl', 2 + 3 - 1, 4), ('u2 pv V', 60 * .5, 30), ('u2 pv P', 30 * 3, 90), ('u2 cell', .5 * 3, 1.5),
     ('u3 det', d2(5, -2, -2, 3), 11), ('u3 v1', v1, 6.182), ('u3 v2', v2, 5.455), ('u3 kcl1', (v1 - 10) / 2 + v1 / 4 + (v1 - v2) / 2 + 1, 1), ('u3 kcl2', (v2 - v1) / 2 + v2 / 4, 1),
     ('u3 mdet', d2(6, -4, -4, 10), 44), ('u3 i1', i1, 2.273), ('u3 i2', i2, .909), ('u3 sh', i1 - i2, 1.364), ('u3 vb', vb, -2.4), ('u3 va', vb + 5, 2.6), ('u3 sn', (vb + 5) / 1 + vb / 4, 2),
     ('u3 n5', 5 - 1, 4), ('u3 v3', 6 / 2, 3), ('u3 sh2', 2 - .5, 1.5),
     ('u4 vth', 12 * 12 / 16, 9), ('u4 rth', par(4, 12), 3), ('u4 IN', 9 / 3, 3), ('u4 iL', 9 / (3 + 6), 1), ('u4 PL', 1 * 6, 6), ('u4 pmax', 81 / 12, 6.75), ('u4 sp1', 10 * 5 / 10, 5), ('u4 sp2', 2 * par(5, 5), 5),
     ('u4 st', 6 / 2, 3), ('u4 rth2', 15 / 5, 3), ('u4 pm2', 400 / 20, 20),
     ('u5 g', -100 / 10, -10), ('u5 vo', -10 * .2, -2), ('u5 rf', 9 * 1, 9), ('u5 sum', -10e3 * (1 / 10e3 + 2 / 10e3), -3), ('u5 g2', -47 / 4.7, -10), ('u5 cas', -10 * 5, -50), ('u5 diff', 4 * (1.2 - 1.0), .8), ('u5 g3', -20 / 5, -4),
     ('u6 i', 10e-6 * 2000, .02), ('u6 wC', .5 * 1e-3 * 9, 4.5e-3), ('u6 wL', .5 * .2 * 9, .9), ('u6 iL', 12 / 6, 2), ('u6 vC', 2 * 4, 8), ('u6 Cs', par(6, 3), 2), ('u6 vL', 50e-3 * 100, 5), ('u6 Ls', 4 + 6, 10),
     ('u6 q', 100e-6 * 9, .9e-3), ('u6 bat', 43.6 + 8.3, 51.9), ('u6 Cp', 10 + 10, 20),
     ('u7 tau', 1e4 * 1e-3, 10), ('u7 v1', 3 * (1 - exp(-1)), 1.90), ('u7 63', 1 - exp(-1), .632), ('u7 5t', 1 - exp(-5), .993), ('u7 tl', .5 / 10, .05), ('u7 iinf', 20 / 10, 2), ('u7 i01', 2 * (1 - exp(-2)), 1.73),
     ('u7 half', 10 * log(2), 6.93), ('u7 t2', 2e3 * 50e-6, .1), ('u7 3t', 1 - exp(-3), .950), ('u7 t3', 20e-3 / 4, 5e-3), ('u7 P', 1e-9 * 1 * 1e9, 1), ('u7 P8', 1e-9 * .64 * 1e9, .64),
     ('u8 w0', w0, 3162), ('u8 f0', w0 / (2 * pi), 503.3), ('u8 al', al, 500), ('u8 wd', wd, 3122.5), ('u8 Q', w0 * .01 / 10, 3.16), ('u8 Rc', 2 * sqrt(.01 / 1e-5), 63.2), ('u8 w0b', 1 / sqrt(1e-3 * 1e-6), 31623),
     ('u8 f0b', 1 / sqrt(1e-9) / (2 * pi), 5033), ('u8 alp', 1 / (2 * 1e3 * 1e-6), 500),
     ('u9 rms', 170 / sqrt(2), 120.2), ('u9 f', 377 / (2 * pi), 60.0), ('u9 w', w60, 377.0), ('u9 XL', w60 * .1, 37.70), ('u9 XC', 1 / (w60 * 1e-4), 26.53), ('u9 Z', Z9, 48.18), ('u9 ang', zang(30, w60 * .1), 51.49),
     ('u9 I', 120 / Z9, 2.491), ('u9 rms10', 10 / sqrt(2), 7.071), ('u9 zc', 1 / (1000 * 1e-6), 1000), ('u9 wc', 1 / (1e3 * 1e-6), 1000), ('u9 fc', 1000 / (2 * pi), 159.2), ('u9 34', zmag(3, 4), 5), ('u9 34a', zang(3, 4), 53.13),
     ('u9 L1', 1900 / 120, 15.8), ('u9 L2', 7200 / 240, 30), ('u9 rng', 5 * 8, 40), ('u9 L2max', 19200 / 240, 80), ('u9 pk', 120 * sqrt(2), 170),
     ('u10 S', 240 * 20, 4800), ('u10 P', 4800 * .8, 3840), ('u10 Q', 4800 * .6, 2880), ('u10 C', 2880 / (w60 * 240**2), 132.6e-6), ('u10 Inew', 3840 / 240, 16), ('u10 I100', 1e7 / 1e5, 100), ('u10 L100', 100**2 * 5, 50e3),
     ('u10 L100p', 50e3 / 1e7, .005), ('u10 I20', 1e7 / 2e4, 500), ('u10 L20', 500**2 * 5, 1.25e6), ('u10 L20p', 1.25e6 / 1e7, .125), ('u10 ratio', 1.25e6 / 50e3, 25), ('u10 S2', zmag(6, 8), 10), ('u10 pf', 6 / 10, .6),
     ('u10 tr', 7200 / 240, 30), ('u10 3ph', sqrt(3) * 480 * 100 * .9, 74.8e3), ('u10 bw', 1000 / 20, 50),
     ('A i', 3 / 1000, .003), ('A p', 3 * .003, .009), ('A p15', 1.5 * .0015, .00225),
     ('B i', 3 / 3000, .001), ('B v1', .001 * 1000, 1), ('B v2', .001 * 2000, 2), ('B par', 3 / 1000, .003), ('B tot', 2 * .003, .006), ('B load', 3 * par(2, 2) / (1 + par(2, 2)), 1.5), ('B iload', 3 / (1e3 + 1e3), .0015),
     ('C iL', 3.10 / 22, .141), ('C r', .10 / (3.10 / 22), .71), ('C P', 3.10 * 3.10 / 22, .437),
     ('D 10', 3 * (1 - exp(-1)), 1.90), ('D 20', 3 * (1 - exp(-2)), 2.59), ('D 30', 3 * (1 - exp(-3)), 2.85), ('D 50', 3 * (1 - exp(-5)), 2.98),
     ('E f0', 1 / (2 * pi * sqrt(1e-7)), 503.3), ('E 400', Ie(400), .563), ('E 503', Ie(1 / (2 * pi * sqrt(1e-7))), 1.0), ('E 600', Ie(600), .667), ('E XL', XL(400, .01), 25.13), ('E XC', XC(400, 1e-5), 39.79),
     ('E Z', zmag(10, XL(400, .01) - XC(400, 1e-5)), 17.76),
     ('F inc', 60 * 3 * 365 / 1000, 65.7), ('F led', 9 * 3 * 365 / 1000, 9.86), ('F led2', 9 * 3 * 365 / 1000, 9.9), ('F save', 1 - 9 / 60, .85),
     ('M1', par(12, 6), 4), ('M2', 24 / 4, 6), ('M3', 60 / 4, 15), ('M4 R', 18 / 6, 3), ('M4 P', 18**2 / 12, 27), ('M5', -10 * -.4, 4),
     ('F1 tau', 5e3 * 20e-6, .1), ('F1 v', 10 * (1 - exp(-2)), 8.65), ('F2 a', 40 / .2, 200), ('F2 w0', 1 / sqrt(1e-5), 316.2), ('F2 wd', sqrt(1e5 - 4e4), 244.9), ('F3 zc', 1 / (w60 * 1e-4), 26.53),
     ('F3 Z', zmag(20, 1 / (w60 * 1e-4)), 33.22), ('F3 a', zang(20, 1 / (w60 * 1e-4)), 52.99), ('F4 P', 1440 * .85, 1224), ('F4 s', sqrt(1 - .85**2), .5268), ('F4 Q', 1440 * sqrt(1 - .85**2), 758.6),
     ('F5 V', 2400 / 20, 120), ('F5 I', 10 / 20, .5), ('F6', sqrt(3) * 208 * 50, 18.01e3)]
    return r
