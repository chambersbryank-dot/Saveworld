"""Dynamics (ENGR 212): kinematics and kinetics of particles and rigid bodies, energy, momentum and vibration.
Oct 25 2026, founder-approved four-year track, sophomore course 5. Same module fields as phys2.py / statics.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, sin, cos, tan, exp, log, atan, atan2, degrees, radians
ID = 'dynamics'
STATUS = 'live'
YEAR = 2
PAGE = 'Dynamics.html'
CODE = 'ENGR 212'
TITLE = 'Dynamics'
LAB_NAME = 'Dynamics lab'
TAGLINE = 'Motion of particles and rigid bodies: kinematics in straight and curved paths, Newton’s second law, work and energy, impulse and momentum, impacts, rockets, rotating machines, rolling, and vibration, with six labs. Free, self-paced, and tied to electric cars, orbits, asteroid deflection, hydropower and earthquake-safe buildings.'
DESC = 'Free self-study Dynamics: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and home labs, practice exams, tied to orbits, DART, hydropower and EVs.'
ALT = 'NASA photo of a rocket launch'
_O = 'https://openstax.org/books/university-physics-volume-1/pages/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 2.003SC Engineering Dynamics', 'https://ocw.mit.edu/courses/2-003sc-engineering-dynamics-fall-2011/')
_MIT8 = ('MIT OpenCourseWare 8.01SC Classical Mechanics', 'https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/')
_EV = ('FuelEconomy.gov (DOE/EPA): All-electric vehicles', 'https://www.fueleconomy.gov/feg/evtech.shtml')
_ISS = ('NASA: International Space Station facts and figures', 'https://www.nasa.gov/international-space-station/space-station-facts-and-figures/')
_GFO = ('NASA JPL: GRACE-FO mission overview', 'https://gracefo.jpl.nasa.gov/mission/overview/')
_PSH = ('U.S. DOE: Pumped storage hydropower', 'https://www.energy.gov/eere/water/pumped-storage-hydropower')
_DART = ('NASA: DART impact changed asteroid’s motion in space', 'https://www.nasa.gov/news-release/nasa-confirms-dart-mission-impact-changed-asteroids-motion-in-space/')
_GRC = ('NASA Glenn: Rocket thrust equation', 'https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/rocket-thrust-equation/')
_WIND = ('U.S. DOE: How do wind turbines work?', 'https://www.energy.gov/eere/wind/how-do-wind-turbines-work')
_HT = ('U.S. DOE: Types of hydropower turbines', 'https://www.energy.gov/eere/water/types-hydropower-turbines')
_HYDRO = ('U.S. DOE: How hydropower works', 'https://www.energy.gov/eere/water/how-hydropower-works')
_BLDG = ('USGS: Natural periods and damping of tall buildings (Çelebi, 2022)', 'https://www.usgs.gov/publications/preliminary-study-correlation-natural-periods-and-damping-percentages-tall-buildings')
_IRIS = ('IRIS/EarthScope: Building resonance', 'https://www.iris.edu/hq/inclass/animation/224')
BANNER = ['images/Landsat9_Launch_KLS04_0013.jpg', 'images/ISS_Flyaround_2021.jpg', 'images/ArtemisII_Launch_KSC_Hancock.jpg', 'images/JPSS2_Atlas_V_Launch_Pad.jpg']
CREDITS = {'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)', 'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)',
           'images/ArtemisII_Launch_KSC_Hancock.jpg': 'NASA', 'images/JPSS2_Atlas_V_Launch_Pad.jpg': 'NASA/Liz Wilk (KSC-20221109-PH-LNW01_0001)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester sophomore engineering dynamics course. It is modeled on the topics and depth of MIT 2.003 Engineering Dynamics and MIT 8.01 Classical Mechanics (both on MIT OpenCourseWare), Purdue ME 274 and Georgia Tech dynamics, and on the free OpenStax University Physics Volume 1, which we link throughout. None of those authors or schools endorses this page.',
         'What we add: every unit ties to real clean-energy, Earth-observation or planetary-defense work with a cited public source (electric cars, the space station, GRACE-FO, pumped storage, NASA’s DART asteroid test, rockets, wind and hydro turbines, earthquake-safe buildings), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a cheap home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Dynamics is the physics of every machine that moves energy around. Electric cars turn battery energy into motion and win some of it back, hydro and wind turbines are spinning rigid bodies, pumped-storage plants bank energy by lifting water, and satellites that watch Earth’s water and climate stay up because they keep falling around it.',
                 'It is also how we protect the planet: NASA’s DART mission used momentum to change an asteroid’s orbit, and engineers use vibration theory to keep buildings standing in earthquakes. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values.']
PREREQS = ['Statics: free-body diagrams, moments and centroids.', 'Physics I: Newton’s laws, energy and momentum.', 'Calculus I and II: derivatives, integrals and simple differential equations.',
           'Differential Equations helps with Unit 10 (vibration) but is not required; the needed solutions are given.']
STUDY = ['Start with kinematics: what is known about position, velocity and acceleration, and in which coordinates?', 'Draw a free-body diagram and a kinetic diagram (ma and Iα) side by side.',
         'Choose the method that fits: F = ma for accelerations, work-energy for speeds between two positions, impulse-momentum for forces over time and impacts.', 'Solve with symbols first, then put in SI numbers, and check units and limiting cases.',
         'Do every practice problem on paper before opening the answer.', 'Retake the quizzes a few days later; spaced practice beats one long session.']
LAB_GEAR = ['A computer or tablet for the free PhET simulations (they run in a browser).', 'A smartphone with a slow-motion video camera or a free sensor app (accelerometer, stopwatch).',
            'A board or long book to make a ramp, a tape measure, and a ball, a can of soup, an empty can and a ring or hoop to roll.', 'String, a small weight (a nut or washers) and a ruler for a pendulum.',
            'A few rubber bands or a soft spring and small masses (coins in a bag) for a spring-mass oscillator.', 'Spreadsheet software for graphs and fits.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab can be done in a free PhET simulation or with household items. Roll and drop only soft, light objects, keep the floor clear, and never launch anything toward people, pets or windows.']
SAFETY_SRC = ('OSHA: Hand and power tools', 'https://www.osha.gov/hand-power-tools')
CONST_SRC = ('NIST: Standard acceleration of gravity', 'https://physics.nist.gov/cgi-bin/cuu/Value?gn')
CONSTANTS = [('Standard acceleration of gravity, g', '9.80665 m/s² (we use 9.81 m/s²)'), ('Earth’s gravitational parameter, GM (rounded)', '3.986 × 10¹⁴ m³/s²'), ('Mean Earth radius (rounded)', '6371 km'),
             ('1 revolution per minute', '2π/60 = 0.1047 rad/s'), ('1 kilowatt-hour', '3.6 × 10⁶ J'), ('1 mile', '1.609 km')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free textbooks, lectures and simulations alongside the course.'
PTABLE = [('OpenStax University Physics Volume 1', _O + '3-1-position-displacement-and-average-velocity', 'Free textbook for the physics side of the course.'), (_MIT[0], _MIT[1], 'Free MIT lectures, problem sets and exams.'),
          (_MIT8[0], _MIT8[1], 'Free MIT mechanics lectures.'), ('PhET: Projectile Motion', _PH + 'projectile-motion', 'Trajectories.'), ('PhET: Collision Lab', _PH + 'collision-lab', 'Momentum and impacts.'),
          ('PhET: Masses and Springs', _PH + 'masses-and-springs', 'Vibration and damping.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Kinematics of Particles in a Straight Line', 'weeks': 'Weeks 1–2',
 'summary': 'Position, velocity and acceleration as derivatives, constant acceleration, acceleration given as a function of time, speed or position, and distance versus displacement.',
 'objectives': ['Relate x, v and a by differentiation and integration.', 'Use the constant-acceleration equations correctly.', 'Solve a(x) problems with v dv = a dx.', 'Tell total distance from displacement.'],
 'concepts': ['Velocity is v = dx/dt and acceleration is a = dv/dt = d²x/dt². Integrating goes the other way.', 'Only when a is constant do v = v₀ + at, x = x₀ + v₀t + ½at² and v² = v₀² + 2a(x − x₀) hold.',
              'If a is given as a function of position, use a dx = v dv; if a function of speed, use dt = dv/a(v).', 'Distance traveled counts every leg; split the motion where v = 0 and add the lengths.',
              'Signs matter: pick a positive direction and keep it; slowing down means a and v have opposite signs.'],
 'eqs': [('v=\\frac{dx}{dt},\\quad a=\\frac{dv}{dt}', 'Definitions'), ('v=v_0+at,\\quad x=x_0+v_0t+\\tfrac12at^2', 'Constant acceleration'), ('v^2=v_0^2+2a(x-x_0)', 'Constant acceleration, no time'), ('a\\,dx=v\\,dv', 'Acceleration as a function of position')],
 'worked': [
  {'q': 'A particle moves with x = t³ − 6t² + 9t (m, s). Find when it stops, v and a at t = 2 s, and the distance traveled from 0 to 4 s.', 'steps': ['v = 3t² − 12t + 9 = 0 at t = 1 s and t = 3 s; a = 6t − 12.', 'At t = 2 s: v = −3 m/s, a = 0.', 'x(0) = 0, x(1) = 4, x(3) = 0, x(4) = 4, so legs of 4 + 4 + 4 m.'], 'a': 'Stops at 1 s and 3 s; v = −3 m/s, a = 0 at 2 s; 12 m traveled (displacement 4 m).'},
  {'q': 'A car starts from rest and accelerates at 3 m/s² for 8 s. Find its speed and distance.', 'steps': ['v = at = 3 × 8.', 'x = ½at² = ½ × 3 × 64.'], 'a': '24 m/s and 96 m.'},
  {'q': 'A car at 30 m/s brakes at 6 m/s². Find the stopping distance and time.', 'steps': ['x = v₀²/(2a) = 900/12.', 't = v₀/a.'], 'a': '75 m in 5 s.'}],
 'practice': [('A ball is thrown straight up at 15 m/s. Find its maximum height and the time to reach it.', 'h = v²/(2g) = 11.47 m; t = v/g = 1.529 s.'),
              ('A particle starts at rest at x = 0 with a = 2x (m/s²). Find v at x = 3 m.', 'v dv = 2x dx gives v² = 2x², v = √2 × 3 = 4.24 m/s.'),
              ('Sample values: an electric car goes from 0 to 27 m/s (about 100 km/h) in 6 s. Find its average acceleration.', 'a = 27/6 = 4.5 m/s² (sample values).'),
              ('A stone dropped into a well hits the water after 2.5 s. How deep is the water surface (ignore sound travel time)?', 'h = ½gt² = 30.7 m.')],
 'misc': [('Zero velocity means zero acceleration.', 'At the top of a throw v = 0 but a = −g.'), ('Distance and displacement are the same.', 'Not when the particle reverses; split at v = 0.'),
          ('The constant-acceleration formulas always work.', 'Only for constant a; otherwise integrate.')],
 'quiz': [{'q': 'Acceleration is the derivative of…', 'opts': ['position', 'velocity', 'distance', 'force'], 'ok': 1, 'why': 'a = dv/dt.'},
          {'q': 'At the top of a vertical throw, the acceleration is…', 'opts': ['0', 'g downward', 'g upward', 'maximum speed'], 'ok': 1, 'why': 'Gravity never switches off.'},
          {'q': 'Doubling speed multiplies braking distance (same a) by…', 'opts': ['2', '4', '√2', '1'], 'ok': 1, 'why': 'x = v²/(2a).'},
          {'q': 'If a is given as a function of x, use…', 'opts': ['v = at', 'a dx = v dv', 'x = vt', 'F = ma only'], 'ok': 1, 'why': 'Chain rule.'}],
 'cards': [('Velocity', 'v = dx/dt.'), ('Acceleration', 'a = dv/dt.'), ('Constant a', 'v = v₀ + at; x = v₀t + ½at².'), ('No-time equation', 'v² = v₀² + 2aΔx.'), ('a(x)', 'a dx = v dv.'), ('Distance', 'Split the motion where v = 0.')],
 'planet': {'text': ['Every speed change costs energy, and where that energy comes from matters. FuelEconomy.gov (DOE/EPA) says electric vehicles convert over 77% of the electrical energy from the grid to power at the wheels, while conventional gasoline vehicles convert only about 12% to 30% of the energy in gasoline. The kinematics in this unit, how fast a car speeds up and how far it brakes, is the starting point for the drive-cycle models used to rate vehicle efficiency.'],
            'site': [('Physics I', 'Physics_I.html')],
            'src': [_EV, ('OpenStax UP1, 3.4 Motion with constant acceleration', _O + '3-4-motion-with-constant-acceleration')]},
 'res': [('OpenStax UP1, 3.1 Position, displacement and average velocity', _O + '3-1-position-displacement-and-average-velocity', 'Free textbook section.'), ('OpenStax UP1, 3.4 Motion with constant acceleration', _O + '3-4-motion-with-constant-acceleration', 'Constant-a equations.'),
         (_MIT[0], _MIT[1], 'MIT lectures and problems.')]})
UNITS.append(
{'id': 'u2', 'title': 'Curvilinear Motion: Projectiles, Normal–Tangential and Polar Coordinates', 'weeks': 'Week 3',
 'summary': 'Motion in a plane: rectangular components and projectiles, normal and tangential components on curved paths, polar coordinates for rotating arms, and relative motion.',
 'objectives': ['Solve projectile problems with independent x and y motions.', 'Find tangential and normal acceleration on a curved path.', 'Use polar components for motion along a rotating arm.', 'Add relative velocities.'],
 'concepts': ['A projectile has a_x = 0 and a_y = −g (no air drag); time links the two directions.', 'On a curved path, a_t = dv/dt changes the speed and a_n = v²/ρ points toward the center of curvature and changes the direction.',
              'In polar coordinates, a_r = r̈ − rθ̇² and a_θ = rθ̈ + 2ṙθ̇; the 2ṙθ̇ term is the Coriolis part.', 'Relative motion: v_A = v_B + v_A/B, and the same for accelerations (for translating frames).',
              'A satellite in a circular orbit has only normal acceleration: it falls toward Earth at v²/r while moving sideways fast enough to miss it.'],
 'eqs': [('x=v_0\\cos\\theta\\,t,\\quad y=v_0\\sin\\theta\\,t-\\tfrac12gt^2', 'Projectile'), ('R=\\frac{v_0^2\\sin2\\theta}{g}', 'Range on level ground'), ('a_t=\\dot v,\\quad a_n=\\frac{v^2}{\\rho}', 'Normal–tangential'),
         ('a_r=\\ddot r-r\\dot\\theta^2,\\quad a_\\theta=r\\ddot\\theta+2\\dot r\\dot\\theta', 'Polar components')],
 'worked': [
  {'q': 'A ball is launched at 20 m/s and 30° above level ground. Find the range, maximum height and flight time.', 'steps': ['v_x = 17.32 m/s, v_y = 10 m/s.', 'Time = 2v_y/g; height = v_y²/(2g); R = v₀² sin 60°/g.'], 'a': 'R = 35.3 m, h = 5.10 m, t = 2.04 s.'},
  {'q': 'A car at 25 m/s on a curve of radius 100 m is slowing at 2 m/s². Find its total acceleration.', 'steps': ['a_n = 25²/100 = 6.25 m/s²; a_t = −2 m/s².', '|a| = √(6.25² + 2²).'], 'a': '6.56 m/s².'},
  {'q': 'A collar slides out along an arm at 0.3 m/s (constant) while the arm turns at a constant 2 rad/s. Find its acceleration when r = 0.5 m.', 'steps': ['a_r = 0 − 0.5 × 2² = −2.0 m/s².', 'a_θ = 0 + 2 × 0.3 × 2 = 1.2 m/s².'], 'a': '|a| = 2.33 m/s².'}],
 'practice': [('NASA says the station orbits Earth about every 90 minutes. Using a sample orbit radius of 6,791 km (420 km altitude), find its speed and normal acceleration.', 'v = 2πr/T = 7,902 m/s (NASA quotes about 5 miles per second, 8.0 km/s); a_n = v²/r = 9.19 m/s².'),
              ('A boat heads north at 4 m/s in a current flowing east at 3 m/s. Find its velocity over the ground.', '5 m/s at 36.9° east of north.'),
              ('Which launch angle gives the longest range on level ground (no drag)?', '45°, where sin 2θ = 1.'),
              ('Find the normal acceleration of a car at 15 m/s on a curve of radius 50 m.', 'a_n = 225/50 = 4.5 m/s².')],
 'misc': [('A body moving at constant speed has no acceleration.', 'On a curve it has a_n = v²/ρ.'), ('Horizontal speed of a projectile drops during flight.', 'Without drag, v_x stays constant.'),
          ('Astronauts float because there is no gravity in orbit.', 'Gravity there is still strong: (6371/6791)² = 88% of surface gravity at a sample 420 km altitude. They float because they are in free fall with the station.')],
 'quiz': [{'q': 'For a projectile without drag, a_x is…', 'opts': ['g', '0', '−g', 'v²/r'], 'ok': 1, 'why': 'Only gravity acts, vertically.'},
          {'q': 'Normal acceleration on a curve is…', 'opts': ['dv/dt', 'v²/ρ', 'rθ̈', '0'], 'ok': 1, 'why': 'Changes direction.'},
          {'q': 'The term 2ṙθ̇ in polar coordinates is the…', 'opts': ['centripetal term', 'Coriolis term', 'drag term', 'tangential term'], 'ok': 1, 'why': 'Coriolis.'},
          {'q': 'Doubling speed on the same curve multiplies a_n by…', 'opts': ['2', '4', '½', '1'], 'ok': 1, 'why': 'v².'}],
 'cards': [('Projectile', 'a_x = 0, a_y = −g.'), ('Range', 'R = v₀² sin 2θ/g.'), ('Tangential', 'a_t = dv/dt.'), ('Normal', 'a_n = v²/ρ.'), ('Polar', 'a_r = r̈ − rθ̇², a_θ = rθ̈ + 2ṙθ̇.'), ('Relative velocity', 'v_A = v_B + v_A/B.')],
 'planet': {'text': ['The space station shows curvilinear motion at its most extreme. NASA says it travels at five miles per second, orbiting Earth about every 90 minutes and making 16 orbits in 24 hours, and that its path takes it over 90 percent of Earth’s population; astronauts have taken millions of images of the planet below. The same normal-acceleration balance keeps every Earth-observing satellite in orbit.'],
            'site': [('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html')],
            'src': [_ISS, ('OpenStax UP1, 4.4 Uniform circular motion', _O + '4-4-uniform-circular-motion')]},
 'res': [('OpenStax UP1, 4.3 Projectile motion', _O + '4-3-projectile-motion', 'Free textbook section.'), ('OpenStax UP1, 4.4 Uniform circular motion', _O + '4-4-uniform-circular-motion', 'Circular motion.'),
         ('PhET: Projectile Motion', _PH + 'projectile-motion', 'Interactive.'), ('PhET: Ladybug Motion 2D', _PH + 'ladybug-motion-2d', 'Velocity and acceleration vectors.')]})
UNITS.append(
{'id': 'u3', 'title': 'Kinetics of Particles: Newton’s Second Law', 'weeks': 'Weeks 4–5',
 'summary': 'ΣF = ma in rectangular, normal–tangential and polar coordinates, friction and connected bodies, banked curves, and orbits.',
 'objectives': ['Draw free-body and kinetic diagrams.', 'Apply ΣF = ma with friction and connected bodies.', 'Solve curve and banking problems with normal–tangential components.', 'Find circular-orbit speeds.'],
 'concepts': ['Newton’s second law: ΣF = ma, in an inertial frame. Write it in the coordinates that match the motion.', 'Kinetic friction while sliding is μ_kN, opposite to the sliding direction.',
              'Connected bodies share accelerations through constraints (a rope of fixed length, a pulley); write one equation per body.', 'On a curve, the net normal force supplies mv²/ρ; banking lets the normal force provide it without friction.',
              'For a circular orbit, gravity supplies the normal force: GMm/r² = mv²/r, so v = √(GM/r).'],
 'eqs': [('\\sum\\vec F=m\\vec a', 'Newton’s second law'), ('\\sum F_n=\\frac{mv^2}{\\rho},\\quad \\sum F_t=m\\dot v', 'Normal–tangential'), ('v=\\sqrt{g\\rho\\tan\\theta}', 'Banked curve, no friction'), ('v=\\sqrt{GM/r}', 'Circular orbit')],
 'worked': [
  {'q': 'A 1200 kg car skids to a stop from 25 m/s with μ_k = 0.7. Find the deceleration and stopping distance.', 'steps': ['a = μ_k g = 6.87 m/s² (mass cancels).', 'x = v²/(2a) = 625/13.73.'], 'a': '6.87 m/s²; 45.5 m.'},
  {'q': 'Masses of 5 kg and 3 kg hang on either side of a light, frictionless pulley. Find the acceleration and rope tension.', 'steps': ['a = (5 − 3)g/(5 + 3).', 'T = 2m₁m₂g/(m₁ + m₂).'], 'a': 'a = 2.45 m/s²; T = 36.8 N.'},
  {'q': 'A curve of radius 80 m is banked at 15°. At what speed is no friction needed?', 'steps': ['v = √(gρ tan 15°) = √(9.81 × 80 × 0.268).'], 'a': '14.5 m/s (52 km/h).'}],
 'practice': [('A 10 kg block is pushed with 50 N along a floor with μ_k = 0.3. Find its acceleration.', 'a = (50 − 29.4)/10 = 2.06 m/s².'),
              ('A 70 kg person stands in an elevator accelerating upward at 1.5 m/s². Find the floor force.', 'N = m(g + a) = 792 N.'),
              ('Find the circular-orbit speed at a sample radius of 6,791 km (GM = 3.986 × 10¹⁴ m³/s²).', 'v = √(GM/r) = 7,661 m/s.'),
              ('Find the top speed on a flat curve of radius 50 m with μ_s = 0.8.', 'v = √(μ_s g r) = 19.8 m/s.')],
 'misc': [('A moving object needs a net force to keep moving.', 'Only to change its velocity.'), ('ma is a force on the free-body diagram.', 'ma is the result, drawn on the kinetic diagram.'),
          ('Centrifugal force pushes you out on a curve.', 'In an inertial frame, the net inward force makes you turn; nothing pushes outward.')],
 'quiz': [{'q': 'Newton’s second law holds in…', 'opts': ['any frame', 'an inertial frame', 'only on Earth', 'only for particles at rest'], 'ok': 1, 'why': 'Non-inertial frames need extra terms.'},
          {'q': 'On a skidding car, μ_k g is the…', 'opts': ['speed', 'deceleration', 'force', 'distance'], 'ok': 1, 'why': 'a = μ_kN/m.'},
          {'q': 'A circular orbit at a larger radius is…', 'opts': ['faster', 'slower', 'the same speed', 'impossible'], 'ok': 1, 'why': 'v = √(GM/r).'},
          {'q': 'What supplies the normal acceleration on a frictionless banked curve?', 'opts': ['gravity alone', 'the normal force component', 'engine thrust', 'drag'], 'ok': 1, 'why': 'N sin θ.'}],
 'cards': [('Second law', 'ΣF = ma.'), ('Kinetic diagram', 'Shows ma (and later Iα).'), ('Kinetic friction', 'μ_kN, opposite sliding.'), ('Atwood machine', 'a = (m₁ − m₂)g/(m₁ + m₂).'), ('Banked curve', 'v = √(gρ tan θ).'), ('Circular orbit', 'v = √(GM/r).')],
 'planet': {'text': ['GRACE-FO weighs Earth’s water with Newton’s second law. NASA JPL explains that the twin satellites fly about 220 km apart; areas of slightly stronger gravity pull the lead satellite ahead first, and a microwave ranging system measures the tiny change in distance. An accelerometer at each satellite’s center of mass measures non-gravitational accelerations such as atmospheric drag so that only gravity is counted. The result is monthly maps showing how water moves in aquifers, lakes, ice sheets and oceans.'],
            'site': [('Earth Observation', 'Earth_Observation.html')],
            'src': [_GFO, ('OpenStax UP1, 6.3 Centripetal force', _O + '6-3-centripetal-force')]},
 'res': [('OpenStax UP1, 6.3 Centripetal force', _O + '6-3-centripetal-force', 'Free textbook section.'), ('OpenStax UP1, 6.2 Friction', _O + '6-2-friction', 'Friction.'), (_MIT8[0], _MIT8[1], 'MIT lectures.')]})
UNITS.append(
{'id': 'u4', 'title': 'Work, Energy and Power', 'weeks': 'Week 6',
 'summary': 'Work of forces (gravity, springs, friction), the work–energy principle, conservative forces and potential energy, conservation of energy, power and efficiency.',
 'objectives': ['Compute the work of gravity, springs and friction.', 'Use the work–energy principle to find speeds between two positions.', 'Use conservation of mechanical energy when only conservative forces do work.', 'Compute power and efficiency.'],
 'concepts': ['Work is U = ∫F·dr. Gravity does −mgΔh, a spring does −½k(x₂² − x₁²), and kinetic friction does −μ_kN × distance.', 'Work–energy principle: T₁ + ΣU₁→₂ = T₂, with kinetic energy T = ½mv².',
              'For conservative forces, work equals the loss of potential energy, so T₁ + V₁ = T₂ + V₂ when only they do work.', 'Power is the rate of work: P = F·v. Efficiency is output power divided by input power.',
              'Energy methods give speeds directly without finding accelerations, which is why they are so useful.'],
 'eqs': [('T_1+\\sum U_{1\\to2}=T_2,\\quad T=\\tfrac12mv^2', 'Work–energy principle'), ('V_g=mgh,\\quad V_e=\\tfrac12kx^2', 'Potential energies'), ('P=\\vec F\\cdot\\vec v,\\quad \\eta=\\frac{P_{\\text{out}}}{P_{\\text{in}}}', 'Power and efficiency')],
 'worked': [
  {'q': 'A 2 kg block slides from rest down a smooth ramp, dropping 3 m. Find its speed at the bottom.', 'steps': ['mgh = ½mv².', 'v = √(2gh).'], 'a': '7.67 m/s (mass does not matter).'},
  {'q': 'A spring (k = 500 N/m) compressed 0.2 m launches a 0.5 kg block on a smooth floor. Find the launch speed.', 'steps': ['½kx² = ½mv².', 'v = x√(k/m).'], 'a': '6.32 m/s.'},
  {'q': 'A 1500 kg car climbs a 5% grade at a steady 20 m/s. Ignoring drag and rolling losses, what power lifts it?', 'steps': ['θ = tan⁻¹ 0.05 = 2.86°.', 'P = mg sin θ × v.'], 'a': '14.7 kW.'}],
 'practice': [('Sample values: a pumped-storage plant raises 1 million m³ of water by 300 m. How much energy does it store?', 'E = mgh = 10⁹ × 9.81 × 300 = 2.94 × 10¹² J ≈ 818 MWh (sample values).'),
              ('A motor with 85% efficiency delivers 10 kW. What power does it draw?', 'P_in = 10/0.85 = 11.8 kW.'),
              ('A 20 kg box is pushed 5 m across a floor with μ_k = 0.4. How much work does friction do?', 'U = −0.4 × 196.2 × 5 = −392 J.'),
              ('A pendulum bob is released 0.5 m above its lowest point. Find its speed there.', 'v = √(2g × 0.5) = 3.13 m/s.')],
 'misc': [('Work is force times distance in every case.', 'Only the component along the motion does work.'), ('The normal force does work on a sliding block.', 'It is perpendicular to the motion, so its work is zero.'),
          ('Energy is lost to friction.', 'It is converted to heat; total energy is conserved, mechanical energy is not.')],
 'quiz': [{'q': 'The SI unit of work is the…', 'opts': ['watt', 'joule', 'newton', 'pascal'], 'ok': 1, 'why': 'N·m = J.'},
          {'q': 'Doubling speed multiplies kinetic energy by…', 'opts': ['2', '4', '8', '√2'], 'ok': 1, 'why': '½mv².'},
          {'q': 'Mechanical energy is conserved when…', 'opts': ['friction acts', 'only conservative forces do work', 'speed is constant', 'always'], 'ok': 1, 'why': 'Definition.'},
          {'q': 'Power equals…', 'opts': ['F·v', 'F/v', 'mv', 'mgh'], 'ok': 0, 'why': 'Rate of work.'}],
 'cards': [('Work', 'U = ∫F·dr.'), ('Kinetic energy', 'T = ½mv².'), ('Work–energy', 'T₁ + ΣU = T₂.'), ('Potential energy', 'mgh; ½kx².'), ('Power', 'P = F·v.'), ('Efficiency', 'P_out/P_in.')],
 'planet': {'text': ['Pumped storage banks clean electricity as height. The U.S. Department of Energy describes pumped storage hydropower as two reservoirs at different elevations that generate power as water flows down through a turbine and use power to pump it back up, acting like a giant battery. DOE says it accounts for 88% of all utility-scale energy storage in the United States, at 43 plants. The stored energy is simply mgh, as in the sample practice problem.'],
            'site': [('Physics II', 'Physics_II.html')],
            'src': [_PSH, ('OpenStax UP1, 8.3 Conservation of energy', _O + '8-3-conservation-of-energy')]},
 'res': [('OpenStax UP1, 7.3 Work-energy theorem', _O + '7-3-work-energy-theorem', 'Free textbook section.'), ('OpenStax UP1, 8.3 Conservation of energy', _O + '8-3-conservation-of-energy', 'Energy conservation.'),
         ('PhET: Energy Skate Park', _PH + 'energy-skate-park', 'Interactive.')]})
UNITS.append(
{'id': 'u5', 'title': 'Impulse, Momentum and Impact', 'weeks': 'Week 7',
 'summary': 'Linear impulse and momentum, conservation of momentum, direct central impact and the coefficient of restitution, and angular momentum of a particle.',
 'objectives': ['Use the impulse–momentum principle to find average forces.', 'Apply conservation of momentum to collisions and recoil.', 'Solve impacts with the coefficient of restitution.', 'Use conservation of angular momentum for central-force motion.'],
 'concepts': ['Linear momentum is L = mv. Impulse–momentum: mv₁ + ∫F dt = mv₂.', 'If no external impulse acts on a system, its total momentum is conserved, even when kinetic energy is not.',
              'The coefficient of restitution e = (v₂′ − v₁′)/(v₁ − v₂) ranges from 0 (perfectly plastic) to 1 (perfectly elastic).', 'Angular momentum about O is H_O = r × mv. If all forces pass through O (a central force like gravity), H_O is conserved.',
              'In orbit, conservation of angular momentum means a satellite moves fastest at periapsis: r₁v₁ = r₂v₂ at the apsides.'],
 'eqs': [('m\\vec v_1+\\int\\vec F\\,dt=m\\vec v_2', 'Impulse–momentum'), ('\\sum m\\vec v_1=\\sum m\\vec v_2', 'Conservation of momentum'), ('e=\\frac{v_2\'-v_1\'}{v_1-v_2}', 'Coefficient of restitution'), ('\\vec H_O=\\vec r\\times m\\vec v', 'Angular momentum')],
 'worked': [
  {'q': 'A 0.15 kg ball arrives at 40 m/s and leaves the bat at 30 m/s the other way after 2 ms of contact. Find the impulse and average force.', 'steps': ['Impulse = m(v₂ − v₁) = 0.15 × 70.', 'F = impulse/Δt.'], 'a': '10.5 N·s; 5,250 N.'},
  {'q': 'A 1500 kg car at 20 m/s hits a stopped 1000 kg car and they lock together. Find the common speed and kinetic energy lost.', 'steps': ['1500 × 20 = 2500v.', 'T₁ = 300 kJ; T₂ = ½ × 2500 × 12².'], 'a': '12 m/s; 120 kJ (40%) lost.'},
  {'q': 'A 2 kg ball at 5 m/s hits a 3 kg ball at rest head-on with e = 0.8. Find both final velocities.', 'steps': ['Momentum: 10 = 2v₁′ + 3v₂′.', 'Restitution: v₂′ − v₁′ = 0.8 × 5 = 4.'], 'a': 'v₁′ = −0.4 m/s (bounces back), v₂′ = 3.6 m/s.'}],
 'practice': [('NASA reports DART shortened Dimorphos’s 11 h 55 min orbit to 11 h 23 min. What fraction of the orbit period is that?', '32 min/715 min = 4.48%.'),
              ('NASA gives DART’s impact speed as about 22,530 km/h. Convert to m/s.', '22,530/3.6 = 6,258 m/s.'),
              ('A satellite moves at 7.5 km/s at 7,000 km from Earth’s center (periapsis). Find its speed at 8,000 km (apoapsis).', 'r₁v₁ = r₂v₂: v₂ = 6.56 km/s.'),
              ('A 60 kg skater at rest throws a 2 kg ball forward at 10 m/s. Find her recoil speed.', '60v = 2 × 10, v = 0.333 m/s backward.')],
 'misc': [('Momentum and kinetic energy are both conserved in every collision.', 'Momentum is; kinetic energy only if e = 1.'), ('A bigger force always means a bigger impulse.', 'Impulse is force × time; a long, gentle push can match a short, hard one.'),
          ('Restitution depends only on the material.', 'It also depends on speed, shape and temperature.')],
 'quiz': [{'q': 'Impulse equals the change in…', 'opts': ['energy', 'momentum', 'speed', 'force'], 'ok': 1, 'why': 'Impulse–momentum.'},
          {'q': 'For a perfectly plastic impact, e =', 'opts': ['0', '0.5', '1', '∞'], 'ok': 0, 'why': 'They move together.'},
          {'q': 'A central force conserves…', 'opts': ['linear momentum', 'angular momentum about the center', 'speed', 'nothing'], 'ok': 1, 'why': 'No moment about O.'},
          {'q': 'Air bags reduce injury by…', 'opts': ['reducing impulse', 'increasing stopping time', 'adding mass', 'adding speed'], 'ok': 1, 'why': 'Same impulse over more time.'}],
 'cards': [('Momentum', 'L = mv.'), ('Impulse', '∫F dt = Δ(mv).'), ('Conservation', 'No external impulse: Σmv constant.'), ('Restitution', 'e from 0 to 1.'), ('Angular momentum', 'H_O = r × mv.'), ('Orbit apsides', 'r₁v₁ = r₂v₂.')],
 'planet': {'text': ['In 2022, NASA proved momentum can defend Earth. NASA reports that the DART spacecraft hit the asteroid Dimorphos at roughly 22,530 km/h and changed its orbit around Didymos by 32 minutes, from 11 hours 55 minutes to 11 hours 23 minutes, more than 25 times NASA’s minimum success benchmark. NASA adds that the recoil from ejected debris substantially enhanced DART’s push, like air streaming out of a balloon. Neither asteroid posed any hazard to Earth.'],
            'site': [('Planetary Defense', 'Planetary_Defense.html')],
            'src': [_DART, ('OpenStax UP1, 9.4 Types of collisions', _O + '9-4-types-of-collisions')]},
 'res': [('OpenStax UP1, 9.3 Conservation of linear momentum', _O + '9-3-conservation-of-linear-momentum', 'Free textbook section.'), ('OpenStax UP1, 9.4 Types of collisions', _O + '9-4-types-of-collisions', 'Collisions.'),
         ('PhET: Collision Lab', _PH + 'collision-lab', 'Interactive.')]})
UNITS.append(
{'id': 'u6', 'title': 'Systems of Particles and Variable Mass: Jets and Rockets', 'weeks': 'Week 8',
 'summary': 'Center of mass of a system, motion of the center of mass, momentum of systems, steady fluid streams, and variable-mass systems including the rocket equation.',
 'objectives': ['Find the center of mass of a system and its motion.', 'Use momentum for systems that push apart.', 'Find the force of a steady fluid jet.', 'Use the thrust and rocket equations.'],
 'concepts': ['The center of mass moves as if all external forces acted on the total mass there: ΣF_ext = m a_G. Internal forces cancel.', 'A steady stream that changes velocity needs a force: F = ṁ(v_out − v_in) for each direction.',
              'A rocket gains momentum by throwing mass backward. Ideal thrust is F = ṁv_e plus a pressure term (p_e − p_a)A_e.', 'The ideal rocket equation, Δv = v_e ln(m₀/m_f), shows why rockets are mostly propellant.',
              'Gravity and drag reduce the real Δv, so launch vehicles use stages to drop empty mass.'],
 'eqs': [('\\bar x=\\frac{\\sum m_ix_i}{\\sum m_i},\\quad \\sum\\vec F_{\\text{ext}}=m\\vec a_G', 'Center of mass'), ('F=\\dot m(v_{\\text{out}}-v_{\\text{in}})', 'Steady stream'),
         ('F=\\dot m v_e+(p_e-p_a)A_e', 'Rocket thrust'), ('\\Delta v=v_e\\ln\\frac{m_0}{m_f}', 'Ideal rocket equation')],
 'worked': [
  {'q': 'Find the center of mass of 3 kg at x = 0 and 5 kg at x = 4 m.', 'steps': ['x̄ = (3 × 0 + 5 × 4)/8.'], 'a': '2.5 m.'},
  {'q': 'Sample values: an engine burns 250 kg/s with exhaust at 3,000 m/s. Find the ideal thrust (ignore the pressure term).', 'steps': ['F = ṁv_e = 250 × 3000.'], 'a': '750 kN (sample values).'},
  {'q': 'A rocket stage has v_e = 3,000 m/s and burns until its mass is a quarter of its starting mass. Find the ideal Δv.', 'steps': ['Δv = 3000 ln 4.'], 'a': '4,159 m/s.'}],
 'practice': [('What mass ratio m₀/m_f gives Δv = 7,800 m/s with v_e = 3,500 m/s (ideal)?', 'm₀/m_f = e^(7800/3500) = e^2.229 = 9.29.'),
              ('A water jet of area 0.001 m² at 20 m/s hits a flat wall and stops. Find the force.', 'F = ρAv² = 1000 × 0.001 × 400 = 400 N.'),
              ('Skaters of 50 kg and 75 kg push apart from rest; the 75 kg skater moves at 2 m/s. Find the other’s speed.', '50v = 75 × 2, v = 3 m/s.'),
              ('Sample values: a 50,000 kg rocket lifts off with 750 kN of thrust. Find its initial acceleration.', 'a = (750,000 − 490,500)/50,000 = 5.19 m/s² (sample values).')],
 'misc': [('A rocket pushes on the air.', 'It pushes on its own exhaust; it works best in vacuum.'), ('Doubling the propellant doubles Δv.', 'Δv grows only with the logarithm of the mass ratio.'),
          ('Internal forces can move the center of mass.', 'Only external forces change a_G.')],
 'quiz': [{'q': 'The center of mass of a system is moved by…', 'opts': ['internal forces', 'external forces', 'both', 'neither'], 'ok': 1, 'why': 'ΣF_ext = m a_G.'},
          {'q': 'Ideal rocket Δv depends on v_e and…', 'opts': ['burn time only', 'the mass ratio', 'the air density', 'the color'], 'ok': 1, 'why': 'ln(m₀/m_f).'},
          {'q': 'Thrust grows with…', 'opts': ['mass flow rate and exhaust speed', 'rocket length', 'payload', 'altitude only'], 'ok': 0, 'why': 'F = ṁv_e + pressure term.'},
          {'q': 'Why stage a rocket?', 'opts': ['to look better', 'to drop empty mass', 'to slow down', 'to add drag'], 'ok': 1, 'why': 'Better mass ratio per stage.'}],
 'cards': [('Center of mass', 'Σm x/Σm.'), ('System motion', 'ΣF_ext = m a_G.'), ('Steady stream', 'F = ṁΔv.'), ('Thrust', 'ṁv_e + (p_e − p_a)A_e.'), ('Rocket equation', 'Δv = v_e ln(m₀/m_f).'), ('Staging', 'Drop empty tanks to improve the mass ratio.')],
 'planet': {'text': ['Every Earth-observing satellite rides a rocket built on this unit. NASA Glenn explains that thrust follows Newton’s third law and depends on the mass flow rate through the engine, the exit velocity of the exhaust and the pressure at the nozzle exit. Getting more Δv from each kilogram of propellant means fewer and smaller launches for the same payloads, such as the Landsat and weather satellites that monitor forests, crops and storms.'],
            'site': [('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html')],
            'src': [_GRC, ('OpenStax UP1, 9.7 Rocket propulsion', _O + '9-7-rocket-propulsion')]},
 'res': [('OpenStax UP1, 9.6 Center of mass', _O + '9-6-center-of-mass', 'Free textbook section.'), ('OpenStax UP1, 9.7 Rocket propulsion', _O + '9-7-rocket-propulsion', 'Rocket equation.'), ('NASA Glenn: Rocket thrust equation', _GRC[1], 'Thrust explained.')]})
UNITS.append(
{'id': 'u7', 'title': 'Planar Kinematics of Rigid Bodies', 'weeks': 'Weeks 9–10',
 'summary': 'Rotation about a fixed axis, angular velocity and acceleration, gear trains, relative velocity and acceleration in rigid bodies, instantaneous centers, and rolling without slipping.',
 'objectives': ['Relate ω and α to point velocities and accelerations.', 'Use gear and belt ratios.', 'Use relative velocity and the instantaneous center for linkages.', 'Describe rolling without slipping.'],
 'concepts': ['For rotation about a fixed axis, a point at radius r has v = rω, a_t = rα and a_n = rω².', 'Meshing gears share the contact speed: r₁ω₁ = r₂ω₂, so speed ratios follow tooth counts.',
              'Relative velocity in a rigid body: v_B = v_A + ω × r_B/A; relative acceleration adds α × r and −ω²r.', 'The instantaneous center of zero velocity (IC) lets you treat a moving body as pure rotation for velocities at that instant.',
              'Rolling without slipping: v_G = rω and a_G = rα; the contact point is momentarily at rest and the top moves at 2v_G.'],
 'eqs': [('v=r\\omega,\\quad a_t=r\\alpha,\\quad a_n=r\\omega^2', 'Fixed-axis rotation'), ('r_1\\omega_1=r_2\\omega_2', 'Gears and belts'), ('\\vec v_B=\\vec v_A+\\vec\\omega\\times\\vec r_{B/A}', 'Relative velocity'), ('v_G=r\\omega', 'Rolling without slipping')],
 'worked': [
  {'q': 'A 0.3 m radius wheel rolls without slipping at 15 m/s. Find ω and the speed of the top point.', 'steps': ['ω = v/r = 15/0.3.', 'Top: v = 2v_G.'], 'a': 'ω = 50 rad/s; top point 30 m/s.'},
  {'q': 'Sample values: a wind turbine rotor turns at 15 rpm and a gearbox with ratio 100 drives the generator. Find the generator speed in rpm and rad/s.', 'steps': ['n = 15 × 100.', 'ω = 1500 × 2π/60.'], 'a': '1,500 rpm = 157.1 rad/s (sample values).'},
  {'q': 'A 1 m bar slides with end A on the floor moving right at 2 m/s and end B on a wall. Find ω and v_B when the bar makes 30° with the floor.', 'steps': ['The IC is where perpendiculars to v_A and v_B meet; its distance from A is L sin 30° = 0.5 m.', 'ω = v_A/0.5; v_B = ω × L cos 30°.'], 'a': 'ω = 4 rad/s; v_B = 3.46 m/s downward.'}],
 'practice': [('Sample values: a 60 m rotor turns at 15 rpm. Find the blade-tip speed and normal acceleration.', 'v = 60 × 1.571 = 94.2 m/s; a_n = v²/r = 148 m/s² (sample values).'),
              ('A flywheel spins up from rest to 3,000 rpm in 10 s at constant α. Find α.', 'ω = 314.2 rad/s; α = 31.4 rad/s².'),
              ('A 0.5 m disk has ω = 2 rad/s and α = 4 rad/s². Find the rim acceleration.', 'a_t = 2, a_n = 2, |a| = 2.83 m/s².'),
              ('A 20-tooth gear drives an 80-tooth gear at 1,200 rpm. Find the output speed.', '1,200 × 20/80 = 300 rpm.')],
 'misc': [('Every point on a rolling wheel moves at the same speed.', 'The contact point is at rest and the top moves at 2v.'), ('Angular velocity differs from point to point on a rigid body.', 'ω is the same for the whole body.'),
          ('The IC has zero acceleration.', 'Only zero velocity, at that instant.')],
 'quiz': [{'q': 'Speed of a point at radius r on a rotating body:', 'opts': ['ω/r', 'rω', 'rω²', 'r/ω'], 'ok': 1, 'why': 'v = rω.'},
          {'q': 'Meshing gears share the same…', 'opts': ['ω', 'tooth count', 'contact speed', 'radius'], 'ok': 2, 'why': 'r₁ω₁ = r₂ω₂.'},
          {'q': 'The contact point of a wheel rolling without slipping moves at…', 'opts': ['v', '2v', '0', 'rω²'], 'ok': 2, 'why': 'No slip.'},
          {'q': '1 rpm in rad/s is about…', 'opts': ['0.1047', '1', '6.28', '60'], 'ok': 0, 'why': '2π/60.'}],
 'cards': [('Fixed axis', 'v = rω, a_t = rα, a_n = rω².'), ('Gear ratio', 'ω₂/ω₁ = r₁/r₂ = N₁/N₂.'), ('Relative velocity', 'v_B = v_A + ω × r_B/A.'), ('Instantaneous center', 'Point of zero velocity at an instant.'), ('Rolling', 'v_G = rω.'), ('rpm', '× 2π/60 for rad/s.')],
 'planet': {'text': ['A wind turbine is a chain of rotating rigid bodies. The U.S. Department of Energy explains that the rotor connects to the generator either directly, in a direct-drive turbine, or through a shaft and a gearbox that speeds up the rotation and allows a physically smaller generator. The gear-ratio kinematics in this unit is how engineers match a slow, huge rotor to a fast generator.'],
            'site': [('Physics II', 'Physics_II.html')],
            'src': [_WIND, ('OpenStax UP1, 10.3 Relating angular and translational quantities', _O + '10-3-relating-angular-and-translational-quantities')]},
 'res': [('OpenStax UP1, 10.3 Relating angular and translational quantities', _O + '10-3-relating-angular-and-translational-quantities', 'Free textbook section.'), ('OpenStax UP1, 11.1 Rolling motion', _O + '11-1-rolling-motion', 'Rolling.'), (_MIT[0], _MIT[1], 'MIT rigid-body kinematics.')]})
UNITS.append(
{'id': 'u8', 'title': 'Planar Kinetics of Rigid Bodies: Force, Mass and Acceleration', 'weeks': 'Week 11',
 'summary': 'Mass moments of inertia, the parallel-axis theorem, equations of motion for translation, fixed-axis rotation and general plane motion, and rolling with friction.',
 'objectives': ['Compute mass moments of inertia of common shapes.', 'Write ΣF = ma_G and ΣM_G = I_Gα.', 'Solve fixed-axis rotation and pulley problems.', 'Solve rolling problems and check for slip.'],
 'concepts': ['Mass moment of inertia I = ∫r² dm measures resistance to angular acceleration. Solid disk ½mr², hoop mr², solid sphere ⅖mr², rod about its center mL²/12.', 'Parallel-axis theorem: I = I_G + md².',
              'Plane motion equations: ΣF_x = m a_Gx, ΣF_y = m a_Gy, ΣM_G = I_Gα (or ΣM_P = sum of the moments of the kinetic diagram about any point P).', 'A body rolling down a slope without slipping has a = g sin θ/(1 + I_G/(mr²)); friction makes the rotation happen.',
              'Check rolling with f ≤ μ_sN; if the needed friction is larger, the body slides and rolls at once.'],
 'eqs': [('\\sum\\vec F=m\\vec a_G,\\quad \\sum M_G=I_G\\alpha', 'Plane motion'), ('I=I_G+md^2', 'Parallel axis'), ('a=\\frac{g\\sin\\theta}{1+I_G/(mr^2)}', 'Rolling down a slope')],
 'worked': [
  {'q': 'A 10 kg solid disk of radius 0.2 m on a fixed axle feels a 4 N·m torque. Find α.', 'steps': ['I = ½ × 10 × 0.2² = 0.2 kg·m².', 'α = M/I.'], 'a': '20 rad/s².'},
  {'q': 'A solid cylinder rolls without slipping down a 30° slope. Find its acceleration and the smallest μ_s that prevents slip.', 'steps': ['a = g sin 30°/(1 + ½) = (2/3)g sin 30°.', 'Moments about G: fr = ½mr²(a/r), so f = ½ma = (1/3)mg sin 30°; μ_s ≥ f/N = (1/3) tan 30°.'], 'a': 'a = 3.27 m/s²; μ_s ≥ 0.192.'},
  {'q': 'A 4 kg mass hangs from a rope wrapped on a 2 kg solid-disk pulley of radius 0.1 m. Find the acceleration and tension.', 'steps': ['Mass: 4g − T = 4a. Pulley: Tr = ½Mr² (a/r), so T = ½Ma = a.', '4g = 5a.'], 'a': 'a = 7.85 m/s²; T = 7.85 N.'}],
 'practice': [('Find I for a 3 kg, 2 m rod about one end.', 'I = mL²/3 = 4 kg·m².'),
              ('That rod is pinned at one end and released from horizontal. Find α at release.', 'α = 3g/(2L) = 7.36 rad/s².'),
              ('Sample values: a hydro turbine runner has I = 5 × 10⁴ kg·m² and a net torque of 1 × 10⁶ N·m at start-up. Find α.', 'α = 20 rad/s² (sample values).'),
              ('Find the acceleration of a solid sphere rolling down a 30° slope.', 'a = (5/7) g sin 30° = 3.50 m/s².')],
 'misc': [('Mass is all that resists angular acceleration.', 'Where the mass is (I) matters; a hoop accelerates slower than a disk of the same mass.'), ('Friction always slows a rolling wheel.', 'Static friction in pure rolling does no work and is what makes it spin.'),
          ('ΣM = Iα works about any point.', 'Use it about G or a fixed axis; about other points include the moment of ma_G.')],
 'quiz': [{'q': 'Which reaches the bottom of a slope first?', 'opts': ['hoop', 'solid disk', 'solid sphere', 'all tie'], 'ok': 2, 'why': 'Smallest I/(mr²).'},
          {'q': 'I of a solid disk about its axis:', 'opts': ['mr²', '½mr²', '⅖mr²', 'mL²/12'], 'ok': 1, 'why': 'Standard result.'},
          {'q': 'The parallel-axis theorem adds…', 'opts': ['md²', 'mr', 'I/d', 'd²'], 'ok': 0, 'why': 'I = I_G + md².'},
          {'q': 'Rotational form of Newton’s law:', 'opts': ['M = Iα', 'M = mα', 'F = Iω', 'P = Iα'], 'ok': 0, 'why': 'About G or a fixed axis.'}],
 'cards': [('Mass moment of inertia', 'I = ∫r² dm.'), ('Disk, hoop, sphere', '½mr², mr², ⅖mr².'), ('Rod', 'mL²/12 (center), mL²/3 (end).'), ('Plane motion', 'ΣF = ma_G, ΣM_G = I_Gα.'), ('Rolling a', 'g sin θ/(1 + I/(mr²)).'), ('Slip check', 'f ≤ μ_sN.')],
 'planet': {'text': ['Hydro turbines are rigid bodies spun by water. The U.S. Department of Energy describes two main families: reaction turbines, such as Francis and Kaplan, which run in the water stream and use pressure and moving water, and impulse turbines, such as the Pelton wheel, whose buckets are struck by free jets. DOE notes Francis turbines are commonly used for heads of about 130 to 2,000 feet. Sizing the runner’s moment of inertia and torque is the kinetics of this unit.'],
            'site': [('Physics II', 'Physics_II.html')],
            'src': [_HT, ('OpenStax UP1, 10.7 Newton’s second law for rotation', _O + '10-7-newtons-second-law-for-rotation')]},
 'res': [('OpenStax UP1, 10.5 Calculating moments of inertia', _O + '10-5-calculating-moments-of-inertia', 'Free textbook section.'), ('OpenStax UP1, 10.7 Newton’s second law for rotation', _O + '10-7-newtons-second-law-for-rotation', 'Rotation dynamics.'),
         ('PhET: Torque', _PH + 'torque', 'Interactive.')]})
UNITS.append(
{'id': 'u9', 'title': 'Rigid Bodies: Energy and Momentum Methods', 'weeks': 'Week 12',
 'summary': 'Kinetic energy of rigid bodies in translation, rotation and rolling, work of couples, power in rotating machines, angular impulse and momentum, and conservation of angular momentum.',
 'objectives': ['Write T = ½mv_G² + ½I_Gω².', 'Use work–energy for rolling and pivoting bodies.', 'Compute rotating-machine power P = Mω.', 'Apply conservation of angular momentum.'],
 'concepts': ['Rigid-body kinetic energy is T = ½mv_G² + ½I_Gω²; for rolling, part of the energy goes into spin.', 'A couple M turning through angle θ does work Mθ; power is P = Mω.',
              'Angular momentum about G is H_G = I_Gω. Angular impulse–momentum: I_Gω₁ + ∫M dt = I_Gω₂.', 'If no external moment acts about an axis, I ω is conserved: pulling mass inward spins faster.',
              'A flywheel stores energy ½Iω²; spinning it twice as fast stores four times the energy.'],
 'eqs': [('T=\\tfrac12mv_G^2+\\tfrac12I_G\\omega^2', 'Rigid-body kinetic energy'), ('U=M\\theta,\\quad P=M\\omega', 'Work and power of a couple'), ('I_1\\omega_1=I_2\\omega_2', 'Conservation of angular momentum'), ('v=\\sqrt{\\frac{2gh}{1+I_G/(mr^2)}}', 'Rolling from height h')],
 'worked': [
  {'q': 'A flywheel with I = 10 kg·m² spins at 300 rad/s. Find its stored energy in J and kWh.', 'steps': ['T = ½ × 10 × 300².', '÷ 3.6 × 10⁶.'], 'a': '450 kJ = 0.125 kWh.'},
  {'q': 'A solid sphere rolls from rest down a 2 m height without slipping. Find its speed.', 'steps': ['mgh = ½mv² + ½(⅖mr²)(v/r)² = (7/10)mv².', 'v = √(10gh/7).'], 'a': '5.29 m/s.'},
  {'q': 'A skater spins at 2 rad/s with I = 4 kg·m², then pulls in her arms to I = 1.6 kg·m². Find the new spin rate.', 'steps': ['4 × 2 = 1.6ω.'], 'a': '5 rad/s.'}],
 'practice': [('A solid cylinder rolls from rest down a 2 m height. Find its speed.', 'v = √(4gh/3) = 5.11 m/s.'),
              ('A 20 kg solid disk of radius 0.5 m spins at 100 rad/s. Find its kinetic energy.', 'I = 2.5 kg·m²; T = 12.5 kJ.'),
              ('A 2 m rod pinned at one end is released from horizontal. Find ω when it hangs vertically.', 'mg(L/2) = ½(mL²/3)ω², ω = √(3g/L) = 3.84 rad/s.'),
              ('Sample values: a turbine shaft carries 1 × 10⁶ N·m at 150 rpm. Find the power.', 'ω = 15.7 rad/s; P = Mω = 15.7 MW (sample values).')],
 'misc': [('A rolling ball has kinetic energy ½mv² only.', 'Add ½Iω² for the spin.'), ('Pulling in your arms adds energy from nowhere.', 'Your muscles do the work; angular momentum is conserved, not kinetic energy.'),
          ('Torque and power are the same thing.', 'P = Mω; the same torque gives more power at higher speed.')],
 'quiz': [{'q': 'Kinetic energy of a rolling body includes…', 'opts': ['only ½mv²', 'only ½Iω²', 'both terms', 'mgh'], 'ok': 2, 'why': 'Translation plus rotation.'},
          {'q': 'Power of a rotating shaft:', 'opts': ['Mω', 'M/ω', 'Iω', 'mv'], 'ok': 0, 'why': 'P = Mω.'},
          {'q': 'Halving I with no external moment makes ω…', 'opts': ['half', 'the same', 'double', 'four times'], 'ok': 2, 'why': 'Iω constant.'},
          {'q': 'Doubling a flywheel’s speed multiplies its energy by…', 'opts': ['2', '4', '8', '√2'], 'ok': 1, 'why': 'ω².'}],
 'cards': [('Rigid-body T', '½mv_G² + ½I_Gω².'), ('Couple work', 'U = Mθ.'), ('Shaft power', 'P = Mω.'), ('Angular momentum', 'H_G = I_Gω.'), ('Conservation', 'I₁ω₁ = I₂ω₂.'), ('Flywheel', 'Stores ½Iω².')],
 'planet': {'text': ['Hydropower is an energy chain from height to spin to electricity. The U.S. Department of Energy explains that water flows through a pipe called a penstock, spins the blades of a turbine, and the turbine spins a generator that produces electricity for the grid. The work–energy and power equations of this unit, from mgh to P = Mω, describe each link in that chain.'],
            'site': [('Physics II', 'Physics_II.html')],
            'src': [_HYDRO, ('OpenStax UP1, 11.3 Conservation of angular momentum', _O + '11-3-conservation-of-angular-momentum')]},
 'res': [('OpenStax UP1, 11.1 Rolling motion', _O + '11-1-rolling-motion', 'Free textbook section.'), ('OpenStax UP1, 11.3 Conservation of angular momentum', _O + '11-3-conservation-of-angular-momentum', 'Angular momentum.'), (_MIT[0], _MIT[1], 'MIT lectures.')]})
UNITS.append(
{'id': 'u10', 'title': 'Mechanical Vibrations', 'weeks': 'Weeks 13–14',
 'summary': 'Free undamped vibration, natural frequency, energy methods, viscous damping and the damping ratio, forced vibration, resonance and magnification.',
 'objectives': ['Find natural frequencies of spring-mass systems and pendulums.', 'Use the damping ratio to classify motion and estimate it from decay.', 'Find the steady-state amplitude of forced vibration.', 'Explain resonance and why low damping is dangerous.'],
 'concepts': ['A mass on a spring obeys mẍ + kx = 0 and vibrates at ω_n = √(k/m); the period is T = 2π/ω_n. A simple pendulum has ω_n = √(g/L) for small swings.',
              'With viscous damping, mẍ + cẋ + kx = 0. The damping ratio ζ = c/(2√(km)) sets the behavior: ζ < 1 oscillates and decays, ζ = 1 is critical, ζ > 1 creeps back.',
              'The logarithmic decrement δ = ln(x₁/x₂) between successive peaks gives ζ ≈ δ/(2π) for light damping.', 'A harmonic force F₀ sin ωt drives a steady response of amplitude X = (F₀/k)/√((1 − r²)² + (2ζr)²), with r = ω/ω_n.',
              'At resonance (r = 1) the magnification is 1/(2ζ): with light damping, a small push repeated at the right rhythm builds a large motion.'],
 'eqs': [('\\omega_n=\\sqrt{k/m},\\quad T=2\\pi/\\omega_n', 'Natural frequency'), ('\\zeta=\\frac{c}{2\\sqrt{km}},\\quad \\omega_d=\\omega_n\\sqrt{1-\\zeta^2}', 'Damping'),
         ('X=\\frac{F_0/k}{\\sqrt{(1-r^2)^2+(2\\zeta r)^2}},\\quad r=\\frac{\\omega}{\\omega_n}', 'Forced response'), ('\\left.\\frac{X}{F_0/k}\\right|_{r=1}=\\frac1{2\\zeta}', 'Resonant magnification')],
 'worked': [
  {'q': 'A 2 kg mass hangs on a spring with k = 800 N/m. Find ω_n, f and T.', 'steps': ['ω_n = √(800/2) = 20 rad/s.', 'f = ω_n/(2π); T = 1/f.'], 'a': '20 rad/s, 3.18 Hz, 0.314 s.'},
  {'q': 'Add a damper with c = 8 N·s/m. Find ζ and the damped frequency.', 'steps': ['ζ = 8/(2√(800 × 2)) = 8/80.', 'ω_d = 20√(1 − 0.01).'], 'a': 'ζ = 0.1; ω_d = 19.9 rad/s.'},
  {'q': 'The undamped system is driven by F₀ = 10 N at 15 rad/s. Find the steady amplitude.', 'steps': ['F₀/k = 12.5 mm; r = 0.75.', 'X = 12.5/(1 − 0.5625).'], 'a': '28.6 mm.'}],
 'practice': [('Find the period of a 1 m simple pendulum.', 'T = 2π√(1/9.81) = 2.01 s.'),
              ('A machine sags 10 mm on its mounts. Estimate its natural frequency.', 'ω_n = √(g/δ) gives f = 4.98 Hz.'),
              ('Find the resonant magnification for ζ = 0.02.', '1/(2 × 0.02) = 25.'),
              ('Successive peaks of a free vibration are 10 mm and 7 mm. Estimate ζ.', 'δ = ln(10/7) = 0.357; ζ ≈ δ/(2π) = 0.057.')],
 'misc': [('A heavier mass vibrates faster.', 'ω_n = √(k/m): more mass, lower frequency.'), ('More damping always means more safety.', 'It lowers resonant peaks but also passes more force at high frequency.'),
          ('A pendulum’s period depends on how heavy the bob is.', 'For small swings, only on L and g.')],
 'quiz': [{'q': 'Natural frequency of a spring-mass system:', 'opts': ['√(m/k)', '√(k/m)', 'k/m', 'km'], 'ok': 1, 'why': 'ω_n = √(k/m).'},
          {'q': 'Critical damping is ζ =', 'opts': ['0', '0.5', '1', '2'], 'ok': 2, 'why': 'Fastest return without oscillation.'},
          {'q': 'At resonance with ζ = 0.05, magnification is…', 'opts': ['5', '10', '20', '0.1'], 'ok': 1, 'why': '1/(2ζ).'},
          {'q': 'Driving well above ω_n (r ≫ 1) makes the response…', 'opts': ['huge', 'small', 'zero frequency', 'critical'], 'ok': 1, 'why': 'X → 0 as r grows.'}],
 'cards': [('Natural frequency', 'ω_n = √(k/m).'), ('Pendulum', 'ω_n = √(g/L).'), ('Damping ratio', 'ζ = c/(2√(km)).'), ('Log decrement', 'ζ ≈ ln(x₁/x₂)/(2π).'), ('Frequency ratio', 'r = ω/ω_n.'), ('Resonance', 'X/(F₀/k) = 1/(2ζ) at r = 1.')],
 'planet': {'text': ['Resonance decides which buildings survive earthquakes. IRIS (now EarthScope) explains that every building has a natural period, the time it takes to sway back and forth, and that when ground motion matches it the building undergoes its largest oscillations and greatest damage. A USGS study of 41 tall buildings found their damping ratios clearly lower than 3%, and the magnification formula in this unit shows why low damping makes resonance dangerous. Engineers tune periods and add damping so homes, hospitals and infrastructure stay standing.'],
            'site': [('Solutions', 'Solutions.html')],
            'src': [_IRIS, _BLDG]},
 'res': [('OpenStax UP1, 15.1 Simple harmonic motion', _O + '15-1-simple-harmonic-motion', 'Free textbook section.'), ('OpenStax UP1, 15.5 Damped oscillations', _O + '15-5-damped-oscillations', 'Damping.'),
         ('OpenStax UP1, 15.6 Forced oscillations', _O + '15-6-forced-oscillations', 'Resonance.'), ('PhET: Masses and Springs', _PH + 'masses-and-springs', 'Interactive.'), ('PhET: Pendulum Lab', _PH + 'pendulum-lab', 'Interactive.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Constant acceleration on a ramp', 'week': 'Week 2',
 'goal': 'Measure position against time for a ball rolling down a gentle ramp, show that x grows as t², and extract the acceleration.',
 'eq': ('x=\\tfrac12at^2', 'From rest; plot x against t² for a straight line of slope a/2'),
 'steps': ['Prop one end of a long board on a book to make a gentle slope; mark 0.25, 1.0, 2.25 and 4.0 m (or scaled-down marks).', 'Release a ball from rest and film it in slow motion with a phone; read the time at each mark.',
           'Plot x against t² and fit a line through the origin; a = 2 × slope.', 'Optional: compare with PhET or with a = (5/7) g sin θ for a rolling solid ball.'],
 'table': (['t (s)', 'x (m) for a = 0.5 m/s²'], [['1', '0.25'], ['2', '1.00'], ['3', '2.25'], ['4', '4.00']]),
 'note': 'Sample values for a = 0.5 m/s²; your slope sets your own a.',
 'calc': ['x/t² = 0.25 m/s² in every row, so a = 0.50 m/s².', 'Doubling the time quadruples the distance.', 'For a solid ball, a = 0.5 m/s² needs sin θ = 0.5 × 7/(5 × 9.81), θ = 4.1°.'],
 'safety': ['Keep the floor clear where the ball runs out; use a soft ball.'], 'home': ['The whole lab is a home lab.'],
 'sims': [('PhET: Ladybug Motion 2D', _PH + 'ladybug-motion-2d')],
 'planet': 'Measured acceleration data like this feeds the drive-cycle tests that rate how efficiently cars use energy.', 'planet_src': [_EV]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Projectile range and launch angle', 'week': 'Week 3',
 'goal': 'Measure how range depends on launch angle and compare with R = v₀² sin 2θ/g.',
 'eq': ('R=\\frac{v_0^2\\sin2\\theta}{g}', 'Level ground, no drag'),
 'steps': ['Open PhET Projectile Motion, turn off air resistance, set v₀ = 10 m/s and the launch height to 0.', 'Fire at 15°, 30°, 45°, 60° and 75° and record the range.',
           'Plot R against sin 2θ; the slope should be v₀²/g = 10.19 m.', 'Turn on air resistance and note which angle now gives the longest range.'],
 'table': (['θ (°)', 'R (m)'], [['15', '5.10'], ['30', '8.83'], ['45', '10.19'], ['60', '8.83'], ['75', '5.10']]),
 'note': 'Values computed from the formula with g = 9.81 m/s².',
 'calc': ['Complementary angles (15° and 75°, 30° and 60°) give the same range.', 'Maximum at 45°: R = v₀²/g = 10.19 m.'],
 'safety': ['None beyond normal computer use; if you try a home version, toss only soft balls and never toward people.'], 'home': ['Optional: toss a soft ball at estimated angles in a yard and measure ranges; drag and launch height make it less exact.'],
 'sims': [('PhET: Projectile Motion', _PH + 'projectile-motion')],
 'planet': 'The same equations, with drag added, plan rocket ascent paths that place Earth-observing satellites in orbit.', 'planet_src': [_ISS]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Bounces, collisions and the coefficient of restitution', 'week': 'Week 7',
 'goal': 'Find e for a bouncing ball from bounce heights, and check momentum conservation in simulated collisions.',
 'eq': ('e=\\sqrt{h_2/h_1}', 'Ball dropped on a heavy floor'),
 'steps': ['Drop a ball from 1.0 m in front of a tape measure and film it; read the first three bounce heights.', 'Compute e for each bounce.',
           'In PhET Collision Lab, collide 2 kg at 5 m/s with 3 kg at rest at elasticity 80% and check the final velocities against the Unit 5 example.', 'Repeat at 0% and 100% elasticity and compare total momentum and kinetic energy before and after.'],
 'table': (['Bounce', 'Height (m)', 'e'], [['Drop', '1.00', '—'], ['1', '0.64', '0.80'], ['2', '0.41', '0.80'], ['3', '0.26', '0.80']]),
 'note': 'Sample values for a ball with e ≈ 0.8.',
 'calc': ['e = √(0.64/1.00) = 0.80; √(0.41/0.64) = 0.80; √(0.26/0.41) = 0.80.', 'Simulation at 80%: v₁′ = −0.4 m/s, v₂′ = 3.6 m/s; momentum 10 kg·m/s before and after.'],
 'safety': ['Use a soft ball and keep breakables away.'], 'home': ['The bounce part is the home version.'],
 'sims': [('PhET: Collision Lab', _PH + 'collision-lab')],
 'planet': 'NASA’s DART test was a planned collision; measuring how momentum transfers in impacts is how planetary defense is designed.', 'planet_src': [_DART]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: The rolling race', 'week': 'Week 11',
 'goal': 'Race a ball, a full can and a ring down the same slope and explain the order with a = g sin θ/(1 + I/(mr²)).',
 'eq': ('a=\\frac{g\\sin\\theta}{1+I_G/(mr^2)},\\quad t=\\sqrt{2L/a}', 'Rolling from rest down length L'),
 'steps': ['Set a board at 10° (phone inclinometer) and mark a 1 m run.', 'Release pairs together: solid ball against full soup can, full can against a ring or empty can (thin-walled).',
           'Film the finishes and time each run; repeat three times.', 'Compare with the predicted times.'],
 'table': (['Object', 'I/(mr²)', 'a (m/s²)', 't over 1 m (s)'], [['Solid sphere', '0.4', '1.22', '1.28'], ['Solid cylinder', '0.5', '1.14', '1.33'], ['Hoop', '1.0', '0.852', '1.53']]),
 'note': 'Values computed for θ = 10° and rolling without slipping; a full soup can behaves only roughly like a solid cylinder because the liquid can slosh.',
 'calc': ['Sphere: a = 9.81 sin 10°/1.4 = 1.22 m/s²; t = √(2/1.22) = 1.28 s.', 'Hoop: a = 9.81 sin 10°/2 = 0.852 m/s²; t = 1.53 s.', 'Mass and radius cancel: only the shape factor matters.'],
 'safety': ['Catch the objects at the bottom; keep fingers out from under heavy cans.'], 'home': ['The whole lab is a home lab.'],
 'sims': [('PhET: Torque', _PH + 'torque')],
 'planet': 'Where a rotor’s mass sits changes how fast it spins up, which matters for wind and hydro turbines.', 'planet_src': [_HT]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Pendulum period and g', 'week': 'Week 13',
 'goal': 'Measure the period of a simple pendulum at several lengths and find g from a fit.',
 'eq': ('T=2\\pi\\sqrt{L/g}\\ \\Rightarrow\\ T^2=\\frac{4\\pi^2}{g}L', 'Plot T² against L'),
 'steps': ['Tie a small weight to a string and hang it from a door frame. Set L (to the weight’s center) at 0.25, 0.50 and 1.00 m.', 'Pull it aside about 10° and time 10 swings; divide by 10.',
           'Plot T² against L and fit a line through the origin; g = 4π²/slope.', 'Check in PhET Pendulum Lab that mass does not change the period.'],
 'table': (['L (m)', 'T (s)'], [['0.25', '1.003'], ['0.50', '1.419'], ['1.00', '2.006']]),
 'note': 'Values computed for g = 9.81 m/s²; small-angle formula.',
 'calc': ['T²/L = 4.024 s²/m in each row, so g = 4π²/4.024 = 9.81 m/s².', 'Quadrupling L doubles T.'],
 'safety': ['Use a light weight and keep the swing away from faces.'], 'home': ['The whole lab is a home lab.'],
 'sims': [('PhET: Pendulum Lab', _PH + 'pendulum-lab')],
 'planet': 'Every building also has a natural period; matching it to ground shaking is what makes earthquakes dangerous.', 'planet_src': [_IRIS]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Spring-mass vibration and damping', 'week': 'Week 14',
 'goal': 'Measure natural frequency against mass, and estimate the damping ratio from decaying peaks.',
 'eq': ('f=\\frac{1}{2\\pi}\\sqrt{k/m},\\quad \\zeta\\approx\\frac{\\ln(x_1/x_2)}{2\\pi}', 'Natural frequency and log decrement'),
 'steps': ['In PhET Masses and Springs, set a spring of 10 N/m and hang 100, 200 and 400 g; time 10 oscillations for each.', 'Turn on damping, release, and read three successive peak heights from the ruler.',
           'Home: hang a bag of coins from a rubber band or soft spring and repeat with a phone stopwatch.', 'Plot f against 1/√m.'],
 'table': (['m (kg)', 'f (Hz) for k = 10 N/m'], [['0.1', '1.592'], ['0.2', '1.125'], ['0.4', '0.796']]),
 'note': 'Values computed from the formula; sample damping peaks of 10, 8 and 6.4 cm are used below.',
 'calc': ['Quadrupling m halves f: 1.592 → 0.796 Hz.', 'Peaks 10 → 8 → 6.4 cm: δ = ln 1.25 = 0.223, ζ ≈ 0.0355.', 'With ζ = 0.0355, resonant magnification would be 1/(2ζ) = 14.1.'],
 'safety': ['Rubber bands can snap; wear glasses and keep the mass small.'], 'home': ['The rubber-band step is the home version.'],
 'sims': [('PhET: Masses and Springs', _PH + 'masses-and-springs')],
 'planet': 'USGS measurements show tall buildings have little damping, so engineers add dampers to cut resonant motion.', 'planet_src': [_BLDG]})
SCHEDULE = [(1, 'u1', 'Position, velocity, acceleration; constant acceleration', 'OpenStax UP1 3.1–3.4'), (2, 'u1', 'Variable acceleration, a(x) and a(v); Lab A', 'UP1 3.6'),
            (3, 'u2', 'Projectiles, normal–tangential, polar, relative motion; Lab B', 'UP1 4.1–4.5'), (4, 'u3', 'Newton’s second law, friction, connected bodies', 'UP1 5.1–6.2'),
            (5, 'u3', 'Curves, banking, orbits', 'UP1 6.3, 13.4'), (6, 'u4', 'Work, energy, conservation, power and efficiency', 'UP1 7.1–8.3'),
            (7, 'u5', 'Impulse, momentum, impact, angular momentum; Lab C; midterm practice', 'UP1 9.1–9.4'), (8, 'u6', 'Systems of particles, jets, rockets', 'UP1 9.5–9.7'),
            (9, 'u7', 'Rigid-body rotation, gears, relative velocity', 'UP1 10.1–10.3'), (10, 'u7', 'Instantaneous centers, relative acceleration, rolling', 'UP1 11.1'),
            (11, 'u8', 'Moments of inertia, plane motion equations, rolling; Lab D', 'UP1 10.4–10.7'), (12, 'u9', 'Rigid-body energy, power, angular momentum', 'UP1 10.8, 11.2–11.3'),
            (13, 'u10', 'Free vibration, pendulums, energy method; Lab E', 'UP1 15.1–15.4'), (14, 'u10', 'Damped and forced vibration, resonance; Lab F', 'UP1 15.5–15.6'),
            (15, 'exam', 'Review and final practice set', 'All units')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('A car accelerates from rest at 2.5 m/s² to 30 m/s. Find the time and distance.', ['t = v/a; x = v²/(2a).'], '12 s; 180 m.'),
  ('A ball is launched at 25 m/s and 40° over level ground. Find the range.', ['R = v₀² sin 80°/g.'], '62.7 m.'),
  ('A 5 kg block is pulled with 40 N along a floor with μ_k = 0.2. Find its acceleration.', ['a = (40 − 0.2 × 49.05)/5.'], '6.04 m/s².'),
  ('A 1 kg mass falls 5 m onto a spring (k = 2000 N/m). Find the maximum compression.', ['mg(5 + x) = ½kx², so 1000x² − 9.81x − 49.05 = 0.'], '0.226 m.'),
  ('A 0.06 kg ball at 50 m/s is stopped in 0.005 s. Find the average force.', ['F = mΔv/Δt.'], '600 N.')]),
 ('Final practice set (all units)', [
  ('A stage with v_e = 2,800 m/s has m₀/m_f = 3. Find the ideal Δv.', ['Δv = v_e ln 3.'], '3,076 m/s.'),
  ('A 0.4 m radius wheel rolls without slipping at 20 m/s. Find ω.', ['ω = v/r.'], '50 rad/s.'),
  ('A 4 kg solid disk of radius 0.25 m feels a 2 N·m torque. Find α.', ['I = ½mr² = 0.125 kg·m².'], '16 rad/s².'),
  ('A hoop rolls from rest down a 1.5 m height without slipping. Find its speed.', ['mgh = mv² for a hoop, v = √(gh).'], '3.84 m/s.'),
  ('A 5 kg mass on a spring with k = 1250 N/m. Find ω_n and f.', ['ω_n = √(k/m).'], '15.8 rad/s; 2.52 Hz.'),
  ('Find the resonant magnification for ζ = 0.05.', ['1/(2ζ).'], '10.')])]
FORMULAS = ['v=dx/dt,\\ a=dv/dt,\\ a\\,dx=v\\,dv', 'v^2=v_0^2+2a\\Delta x', 'R=v_0^2\\sin2\\theta/g', 'a_n=v^2/\\rho,\\ a_t=\\dot v', 'a_r=\\ddot r-r\\dot\\theta^2,\\ a_\\theta=r\\ddot\\theta+2\\dot r\\dot\\theta',
            '\\sum\\vec F=m\\vec a', 'T_1+\\sum U=T_2,\\ P=\\vec F\\cdot\\vec v', 'm\\vec v_1+\\int\\vec F dt=m\\vec v_2,\\ e=(v_2\'-v_1\')/(v_1-v_2)', '\\Delta v=v_e\\ln(m_0/m_f)', 'v=r\\omega,\\ a_t=r\\alpha,\\ a_n=r\\omega^2',
            '\\vec v_B=\\vec v_A+\\vec\\omega\\times\\vec r_{B/A}', '\\sum M_G=I_G\\alpha,\\ I=I_G+md^2', 'T=\\tfrac12mv_G^2+\\tfrac12I_G\\omega^2,\\ P=M\\omega', '\\omega_n=\\sqrt{k/m},\\ \\zeta=c/(2\\sqrt{km})',
            'X=(F_0/k)/\\sqrt{(1-r^2)^2+(2\\zeta r)^2}']
GLOSSARY = sorted([('Angular momentum', 'H = r × mv for a particle; I_Gω for a rigid body in plane motion.'), ('Coefficient of restitution', 'Ratio of separation to approach speed in an impact.'), ('Coriolis acceleration', '2ṙθ̇ term in polar coordinates.'),
    ('Damping ratio', 'ζ = c/(2√(km)); 1 is critical.'), ('Impulse', 'Integral of force over time.'), ('Instantaneous center', 'Point of a body with zero velocity at an instant.'),
    ('Kinetic diagram', 'Sketch showing ma_G and I_Gα.'), ('Logarithmic decrement', 'ln of the ratio of successive peaks.'), ('Mass moment of inertia', 'I = ∫r² dm.'),
    ('Natural frequency', 'Frequency of free vibration, √(k/m).'), ('Normal acceleration', 'v²/ρ, toward the center of curvature.'), ('Power', 'Rate of doing work, F·v or Mω.'),
    ('Projectile', 'Body moving under gravity alone.'), ('Resonance', 'Large response when forcing matches a natural frequency.'), ('Rocket equation', 'Δv = v_e ln(m₀/m_f).'),
    ('Rolling without slipping', 'v_G = rω; contact point at rest.'), ('Tangential acceleration', 'dv/dt along the path.'), ('Work–energy principle', 'T₁ + ΣU = T₂.')])
RUBRIC = [('4 · Mastery', 'Chooses coordinates and the best method (forces, energy or momentum), draws free-body and kinetic diagrams, and checks units and limiting cases.'), ('3 · Proficient', 'Solves the practice problems with occasional sign or unit slips.'),
          ('2 · Developing', 'Follows worked examples but mixes up methods or forgets rotational terms.'), ('1 · Beginning', 'Plugs numbers into formulas without diagrams; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '25%'), ('Labs', '20%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    g = 9.81; GM = 3.986e14; r_ = radians; d = degrees
    x = lambda t: t**3 - 6 * t**2 + 9 * t
    v15 = lambda th: 100 * sin(r_(2 * th)) / g
    roll = lambda k, th=10: g * sin(r_(th)) / (1 + k)
    th5 = atan(.05)
    r = [
     ('u1 v2', 3 * 4 - 24 + 9, -3), ('u1 a2', 12 - 12, 0), ('u1 x1', x(1), 4), ('u1 x3', x(3), 0), ('u1 x4', x(4), 4), ('u1 dist', abs(x(1)) + abs(x(3) - x(1)) + abs(x(4) - x(3)), 12),
     ('u1 v', 3 * 8, 24), ('u1 x', .5 * 3 * 64, 96), ('u1 stop', 900 / 12, 75), ('u1 t', 30 / 6, 5), ('u1 h', 225 / (2 * g), 11.47), ('u1 th', 15 / g, 1.529), ('u1 ax', sqrt(2) * 3, 4.24),
     ('u1 ev', 27 / 6, 4.5), ('u1 well', .5 * g * 2.5**2, 30.7),
     ('u2 R', 400 * sin(r_(60)) / g, 35.3), ('u2 h', 100 / (2 * g), 5.10), ('u2 t', 20 / g, 2.04), ('u2 vx', 20 * cos(r_(30)), 17.32), ('u2 an', 625 / 100, 6.25), ('u2 a', sqrt(6.25**2 + 4), 6.56),
     ('u2 ar', -.5 * 4, -2.0), ('u2 at', 2 * .3 * 2, 1.2), ('u2 |a|', sqrt(4 + 1.44), 2.33), ('u2 iss v', 2 * pi * 6.791e6 / 5400, 7902), ('u2 iss a', (2 * pi * 6.791e6 / 5400)**2 / 6.791e6, 9.19),
     ('u2 5mi', 5 * 1609, 8045), ('u2 boat', sqrt(16 + 9), 5), ('u2 boat ang', d(atan(3 / 4)), 36.9), ('u2 car', 225 / 50, 4.5), ('u2 g88', (6371 / 6791)**2, .88),
     ('u3 a', .7 * g, 6.87), ('u3 x', 625 / (2 * .7 * g), 45.5), ('u3 atw', 2 * g / 8, 2.45), ('u3 T', 2 * 5 * 3 * g / 8, 36.8), ('u3 bank', sqrt(g * 80 * tan(r_(15))), 14.5), ('u3 bank kmh', sqrt(g * 80 * tan(r_(15))) * 3.6, 52),
     ('u3 tan15', tan(r_(15)), .268), ('u3 push', (50 - .3 * 10 * g) / 10, 2.06), ('u3 push f', .3 * 10 * g, 29.4), ('u3 elev', 70 * (g + 1.5), 792), ('u3 orb', sqrt(GM / 6.791e6), 7661), ('u3 flat', sqrt(.8 * g * 50), 19.8),
     ('u4 v', sqrt(2 * g * 3), 7.67), ('u4 spr', .2 * sqrt(500 / .5), 6.32), ('u4 th', d(th5), 2.86), ('u4 P', 1500 * g * sin(th5) * 20, 14.7e3), ('u4 psh', 1e9 * g * 300, 2.94e12), ('u4 MWh', 1e9 * g * 300 / 3.6e9, 818),
     ('u4 eff', 10 / .85, 11.8), ('u4 fr', .4 * 20 * g * 5, 392), ('u4 fN', 20 * g, 196.2), ('u4 pend', sqrt(2 * g * .5), 3.13),
     ('u5 J', .15 * 70, 10.5), ('u5 F', 10.5 / .002, 5250), ('u5 v', 30000 / 2500, 12), ('u5 T1', .5 * 1500 * 400, 300e3), ('u5 T2', .5 * 2500 * 144, 180e3), ('u5 loss', 120 / 300, .4),
     ('u5 v1', (2 - .8 * 3) * 5 / 5, -.4), ('u5 v2', 1.8 * 2 * 5 / 5, 3.6), ('u5 dart', 32 / 715, .0448), ('u5 715', 11 * 60 + 55, 715), ('u5 683', 11 * 60 + 23 + 32, 715), ('u5 kmh', 22530 / 3.6, 6258),
     ('u5 mph', 14000 * 1.609, 22530), ('u5 apo', 7000 * 7.5 / 8000, 6.56), ('u5 skate', 20 / 60, .333),
     ('u6 xg', 20 / 8, 2.5), ('u6 F', 250 * 3000, 750e3), ('u6 dv', 3000 * log(4), 4159), ('u6 mr', exp(7800 / 3500), 9.29), ('u6 mr e', 7800 / 3500, 2.229), ('u6 jet', 1000 * .001 * 400, 400), ('u6 sk', 150 / 50, 3),
     ('u6 a', (750e3 - 50000 * g) / 50000, 5.19), ('u6 W', 50000 * g, 490.5e3),
     ('u7 w', 15 / .3, 50), ('u7 top', 30, 2 * 15), ('u7 gen', 1500 * 2 * pi / 60, 157.1), ('u7 ic', 2 / (1 * sin(r_(30))), 4), ('u7 vB', 4 * cos(r_(30)), 3.46), ('u7 tip', 60 * 15 * 2 * pi / 60, 94.2),
     ('u7 tipw', 15 * 2 * pi / 60, 1.571), ('u7 tipa', (60 * pi / 2)**2 / 60, 148), ('u7 fly', 3000 * 2 * pi / 60, 314.2), ('u7 alpha', 3000 * 2 * pi / 600, 31.4), ('u7 rim', sqrt(4 + 4), 2.83), ('u7 gear', 1200 * 20 / 80, 300),
     ('u8 I', .5 * 10 * .04, .2), ('u8 al', 4 / .2, 20), ('u8 cyl', 2 / 3 * g * .5, 3.27), ('u8 mu', tan(r_(30)) / 3, .192), ('u8 pul', 4 * g / 5, 7.85), ('u8 T', 4 * (g - 4 * g / 5), 7.85),
     ('u8 rod', 3 * 4 / 3, 4), ('u8 rodal', 3 * g / 4, 7.36), ('u8 turb', 1e6 / 5e4, 20), ('u8 sph', 5 / 7 * g * .5, 3.50),
     ('u9 fly', .5 * 10 * 9e4, 450e3), ('u9 kwh', 450e3 / 3.6e6, .125), ('u9 sph', sqrt(10 * g * 2 / 7), 5.29), ('u9 skate', 8 / 1.6, 5), ('u9 cyl', sqrt(4 * g * 2 / 3), 5.11), ('u9 diskI', .5 * 20 * .25, 2.5),
     ('u9 diskT', .5 * 2.5 * 1e4, 12.5e3), ('u9 rod', sqrt(3 * g / 2), 3.84), ('u9 w150', 150 * 2 * pi / 60, 15.7), ('u9 P', 1e6 * 150 * 2 * pi / 60, 15.7e6),
     ('u10 wn', sqrt(800 / 2), 20), ('u10 f', 20 / (2 * pi), 3.18), ('u10 T', 2 * pi / 20, .314), ('u10 z', 8 / (2 * sqrt(1600)), .1), ('u10 wd', 20 * sqrt(.99), 19.9), ('u10 st', 10 / 800, .0125),
     ('u10 r', 15 / 20, .75), ('u10 X', .0125 / (1 - .5625), .0286), ('u10 pend', 2 * pi * sqrt(1 / g), 2.01), ('u10 sag', sqrt(g / .01) / (2 * pi), 4.98), ('u10 mag', 1 / .04, 25), ('u10 dec', log(10 / 7), .357),
     ('u10 zeta', log(10 / 7) / (2 * pi), .057),
     ('A x/t2', 1.0 / 4, .25), ('A th', d(atan(.5 * 7 / (5 * g))), 4.1),
     ('B 15', v15(15), 5.10), ('B 30', v15(30), 8.83), ('B 45', v15(45), 10.19), ('B 60', v15(60), 8.83), ('B 75', v15(75), 5.10),
     ('C e1', sqrt(.64), .80), ('C e2', sqrt(.41 / .64), .80), ('C e3', sqrt(.26 / .41), .80), ('C p', 2 * -.4 + 3 * 3.6, 10),
     ('D sph', roll(.4), 1.22), ('D cyl', roll(.5), 1.14), ('D hoop', roll(1), .852), ('D ts', sqrt(2 / roll(.4)), 1.28), ('D tc', sqrt(2 / roll(.5)), 1.33), ('D th', sqrt(2 / roll(1)), 1.53),
     ('E .25', 2 * pi * sqrt(.25 / g), 1.003), ('E .5', 2 * pi * sqrt(.5 / g), 1.419), ('E 1', 2 * pi * sqrt(1 / g), 2.006), ('E slope', 4 * pi**2 / g, 4.024), ('E g', 4 * pi**2 / 4.024, 9.81),
     ('F .1', sqrt(100) / (2 * pi), 1.592), ('F .2', sqrt(50) / (2 * pi), 1.125), ('F .4', sqrt(25) / (2 * pi), .796), ('F dec', log(1.25), .223), ('F z', log(1.25) / (2 * pi), .0355), ('F mag', 1 / (2 * log(1.25) / (2 * pi)), 14.1),
     ('M1 t', 30 / 2.5, 12), ('M1 x', 900 / 5, 180), ('M2', 625 * sin(r_(80)) / g, 62.7), ('M3', (40 - .2 * 5 * g) / 5, 6.04), ('M4', (g + sqrt(g * g + 4 * 1000 * 5 * g)) / 2000, .226), ('M5', .06 * 50 / .005, 600),
     ('F1', 2800 * log(3), 3076), ('F2', 20 / .4, 50), ('F3', 2 / (.5 * 4 * .0625), 16), ('F4', sqrt(g * 1.5), 3.84), ('F5 w', sqrt(1250 / 5), 15.8), ('F5 f', sqrt(250) / (2 * pi), 2.52), ('F6', 1 / .1, 10)]
    return r
