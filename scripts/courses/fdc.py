"""Flight Dynamics & Controls (AERO 420): axes and moments, longitudinal static stability, trim, lateral-directional stability, equations of motion and dynamic modes, transfer functions, time response, feedback and PID, stability analysis, and spacecraft attitude control.
Oct 25 2026, founder-approved four-year track, senior course 2. Same module fields as prop.py / probstat.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, log, exp, pi, atan, cos, degrees, radians
ID = 'fdc'
STATUS = 'live'
YEAR = 4
PAGE = 'Flight_Dynamics_Controls.html'
CODE = 'AERO 420'
TITLE = 'Flight Dynamics & Controls'
LAB_NAME = 'Flight dynamics and controls lab'
TAGLINE = 'Stability and control of aircraft and spacecraft: axes and moments, static stability and trim, lateral-directional stability, dynamic modes, transfer functions, time response, feedback and PID control, stability margins, and spacecraft attitude control, with six labs. Free, self-paced, and tied to NASA’s X-59, Hubble and Dragonfly.'
DESC = 'Free self-study Flight Dynamics & Controls: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and spreadsheet labs, practice exams, tied to NASA’s X-59 quiet supersonic jet, Hubble pointing and the Dragonfly rotorcraft.'
ALT = 'The International Space Station seen from a departing spacecraft during a 2021 flyaround'
_PH = 'https://phet.colorado.edu/en/simulations/'
_GG = 'https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/'
_MIT = ('MIT OpenCourseWare 16.333 Aircraft Stability and Control (Fall 2004)', 'https://ocw.mit.edu/courses/16-333-aircraft-stability-and-control-fall-2004/')
_MITC = ('MIT OpenCourseWare 16.06 Principles of Automatic Control (Fall 2012)', 'https://ocw.mit.edu/courses/16-06-principles-of-automatic-control-fall-2012/')
_MITF = ('MIT OpenCourseWare 16.30 Feedback Control Systems (Fall 2010)', 'https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/')
_GROT = ('NASA Glenn Beginner’s Guide: Aircraft rotations', _GG + 'aircraft-rotations/')
_GCG = ('NASA Glenn Beginner’s Guide: Center of gravity', _GG + 'center-of-gravity/')
_GEL = ('NASA Glenn Beginner’s Guide: Aircraft elevator interactive', _GG + 'aircraft-elevator-interactive/')
_GAIL = ('NASA Glenn Beginner’s Guide: Ailerons', _GG + 'ailerons/')
_X59 = ('NASA: X-59 aircraft builds momentum through 25th flight (Sept. 4, 2026)', 'https://www.nasa.gov/blogs/quesst/2026/09/04/nasas-x-59-aircraft-builds-momentum-through-25th-flight/')
_QU = ('NASA: Quesst mission', 'https://www.nasa.gov/mission/quesst/')
_HUB = ('NASA Science: NASA to change how it points Hubble Space Telescope (June 4, 2024)', 'https://science.nasa.gov/missions/hubble/nasa-to-change-how-it-points-hubble-space-telescope/')
_DF = ('NASA Science: Dragonfly completes first simulated flight (Oct. 23, 2026)', 'https://science.nasa.gov/blogs/dragonfly/2026/10/23/nasas-dragonfly-completes-first-simulated-flight/')
BANNER = ['images/ISS_Flyaround_2021.jpg', 'images/GOES19_GOESU_KSC.jpg', 'images/ArtemisII_Launch_KSC_Hancock.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg']
CREDITS = {'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)', 'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC', 'images/ArtemisII_Launch_KSC_Hancock.jpg': 'NASA',
           'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester senior flight dynamics and controls course for aerospace engineers. It is modeled on the topics and depth of MIT 16.333 Aircraft Stability and Control, MIT 16.06 Principles of Automatic Control and MIT 16.30 Feedback Control Systems (free on MIT OpenCourseWare), using NASA Glenn’s free Beginner’s Guide to Aeronautics, which we link where it helps. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (NASA’s X-59 flight tests, Hubble’s pointing system and the Dragonfly rotorcraft), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a spreadsheet.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Stable, well-controlled vehicles fly efficient paths, and the same control ideas point Earth-observing satellites and telescopes precisely enough to measure our planet and universe.',
                 'Control engineering also makes new, quieter and more autonomous aircraft possible. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Dynamics: rigid-body rotation, moments of inertia and angular momentum.', 'Differential Equations: linear ODEs and the Laplace transform.',
           'Linear Algebra: matrices and eigenvalues.', 'Aerodynamics I and Aircraft Performance: lift, drag, moments and turning flight.']
STUDY = ['Draw the body axes and the center of gravity before writing any moment equation.', 'Keep angles in radians inside formulas; convert to degrees only for the answer.',
         'Separate static stability (the first tendency after a disturbance) from dynamic stability (what happens over time).', 'Sketch the poles in the s-plane for every system you meet.',
         'Check every answer against physical sense: stable systems settle, unstable ones grow.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Balancing Act and Masses and Springs simulations.', 'Spreadsheet software (any free one works), or Python.',
            'NASA Glenn’s Beginner’s Guide to Aeronautics pages in a web browser.', 'A calculator.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free simulation or a spreadsheet, so there are no physical hazards. Do not build or fly drones or models for this course. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('Standard gravity', 'g₀ = 9.80665 m/s²'), ('1 radian', '57.2958°'), ('1 ft', '0.3048 m'),
             ('Settling time rule (textbook)', 't_s ≈ 4/(ζω_n) for 2% settling'), ('First-order step', '63.2% of final value at t = τ'), ('Sea-level air density (standard atmosphere)', '1.225 kg/m³')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, NASA guides and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT stability and control lectures.'), (_MITC[0], _MITC[1], 'Free MIT control lectures and problems.'), (_MITF[0], _MITF[1], 'Free MIT feedback control course.'),
          (_GROT[0], _GROT[1], 'Free NASA explainer.'), (_GCG[0], _GCG[1], 'Free NASA explainer.'), ('PhET: Masses and Springs', _PH + 'masses-and-springs', 'Damped oscillation interactively.')]
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Axes, Rotations and Moments', 'weeks': 'Week 1',
 'summary': 'Body axes through the center of gravity, roll, pitch and yaw, control surfaces and the moments they make, finding the center of gravity, and Euler angles.',
 'objectives': ['Define the roll, pitch and yaw axes.', 'Locate a center of gravity from component masses.', 'Compute the moment of a control force.', 'Match each control surface to its moment.'],
 'concepts': ['In flight an aircraft rotates about its center of gravity (cg), the average location of its mass.',
              'Body axes: roll toward the nose, pitch toward the right wing tip, yaw toward the bottom of the aircraft.',
              'Control surfaces make aerodynamic forces at a distance from the cg, producing moments: elevators pitch, the rudder yaws, ailerons roll.',
              'The cg of several masses is x_cg = Σm_ix_i/Σm_i; moving it changes stability and control.',
              'Euler angles (yaw ψ, pitch θ, roll φ, applied in that order) describe attitude relative to the Earth.'],
 'eqs': [('x_{cg}=\\frac{\\sum m_ix_i}{\\sum m_i}', 'Center of gravity'), ('M=Fd', 'Moment of a force'), ('L,\\ M,\\ N', 'Roll, pitch and yaw moments'), ('\\psi\\to\\theta\\to\\phi', 'Euler angle order')],
 'worked': [
  _w('A tail force of 2000 N acts 6 m behind the cg (sample values). Find the pitching moment.', ['M = 2000 × 6.'], '12,000 N·m.'),
  _w('Masses of 1000 kg at 2 m, 500 kg at 6 m and 300 kg at 10 m from the nose (sample values). Find the cg.', ['Σm = 1800 kg.', 'Σmx = 2000 + 3000 + 3000 = 8000 kg·m.'], 'x_cg = 4.44 m.'),
  _w('Which surface rolls the aircraft?', ['Ailerons deflect in opposite directions on each wing.'], 'Ailerons produce a rolling moment.')],
 'practice': [('Moment of 500 N at 4 m?', '2000 N·m.'), ('Which surface yaws the nose?', 'The rudder.'),
              ('Add 200 kg at 10 m to the example. New cg?', '10,000/2000 = 5.0 m.'), ('About which point does a kite rotate?', 'Its bridle point.')],
 'misc': [('Aircraft rotate about their nose.', 'They rotate about the cg.'), ('Elevators roll the aircraft.', 'They pitch it.'), ('Euler angle order does not matter.', 'Rotations do not commute.')],
 'quiz': [_q('Aircraft rotate about…', ['the cg', 'the nose', 'the tail', 'the wing tip'], 0, 'NASA Glenn.'), _q('Rudder makes…', ['yaw', 'roll', 'pitch', 'lift only'], 0, 'Yawing moment.'),
          _q('Example cg…', ['4.44 m', '6 m', '2 m', '10 m'], 0, '8000/1800.'), _q('Pitch axis points to…', ['the right wing tip', 'the nose', 'down', 'up'], 0, 'Definition.')],
 'cards': [('cg', 'Average location of mass.'), ('Roll', 'Rotation about the nose axis.'), ('Pitch', 'Nose up or down.'), ('Yaw', 'Nose side to side.'), ('Moment', 'Force × distance.'), ('Euler angles', 'ψ, θ, φ.')],
 'planet': {'text': ['NASA Glenn explains that control surfaces produce forces at their centers of pressure, some distance from the cg, creating torques about the principal axes: elevators pitch, the rudder yaws and ailerons roll. The first aircraft to show active control about all three axes was the Wrights’ 1902 glider.',
                     'Every modern efficient airliner and Earth-observing aircraft still uses those three moments, now often commanded through flight-control computers.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Dynamics', 'Dynamics.html')],
            'src': [_GROT, _GCG]},
 'res': [(_GROT[0], _GROT[1], 'Free NASA explainer.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u2', 'title': 'Longitudinal Static Stability', 'weeks': 'Week 2',
 'summary': 'Pitching-moment coefficient, the stability derivative C_mα, the neutral point, static margin, and how cg position and tail size set stability.',
 'objectives': ['State the condition for static pitch stability.', 'Compute static margin.', 'Relate static margin to C_mα.', 'Explain the effect of moving the cg.'],
 'concepts': ['Static stability is the first tendency after a disturbance: a statically stable aircraft makes a moment that pushes it back.',
              'In pitch this needs C_mα < 0: more angle of attack makes a nose-down moment.',
              'The neutral point is the cg location where C_mα = 0.',
              'Static margin SM = (x_np − x_cg)/c̄; positive means stable. Approximately C_mα = −C_Lα × SM.',
              'Moving the cg aft reduces stability and control forces; too far aft makes the aircraft unstable unless a computer stabilizes it.'],
 'eqs': [('C_{m_\\alpha}=\\frac{\\partial C_m}{\\partial\\alpha}<0', 'Pitch stability'), ('SM=\\frac{x_{np}-x_{cg}}{\\bar c}', 'Static margin'), ('C_{m_\\alpha}=-C_{L_\\alpha}SM', 'Stability derivative'), ('M=\\tfrac12\\rho V^2S\\bar cC_m', 'Pitching moment')],
 'worked': [
  _w('The neutral point is at 0.35c̄ and the cg at 0.25c̄ (sample values). Find the static margin.', ['SM = 0.35 − 0.25.'], 'SM = 0.10 (10%).'),
  _w('With C_Lα = 5.5 per radian, find C_mα.', ['C_mα = −5.5 × 0.10.'], 'C_mα = −0.55 per radian: stable.'),
  _w('Move the cg to 0.30c̄. Find the new C_mα.', ['SM = 0.05; −5.5 × 0.05.'], '−0.275 per radian: half as stiff.')],
 'practice': [('SM with cg at 0.35c̄?', '0: neutrally stable.'), ('Sign of C_mα for cg at 0.40c̄?', 'Positive: unstable.'),
              ('Does a bigger tail move the neutral point fore or aft?', 'Aft, raising static margin.'), ('Why fly with small margins?', 'Less trim drag and lighter controls.')],
 'misc': [('Static stability guarantees dynamic stability.', 'It is only the first tendency.'), ('Aft cg is always safer.', 'It reduces stability.'), ('C_mα should be positive.', 'Negative is stable.')],
 'quiz': [_q('Pitch stable if C_mα…', ['< 0', '> 0', '= 1', '= 0'], 0, 'Restoring.'), _q('SM example…', ['0.10', '0.35', '0.25', '0.60'], 0, '0.35 − 0.25.'),
          _q('Neutral point: C_mα = …', ['0', '1', '−1', '∞'], 0, 'Definition.'), _q('Moving cg aft…', ['reduces SM', 'raises SM', 'no change', 'adds lift'], 0, 'Margin shrinks.')],
 'cards': [('Static stability', 'First tendency to return.'), ('C_mα', 'Pitch stiffness.'), ('Neutral point', 'cg where C_mα = 0.'), ('Static margin', '(x_np − x_cg)/c̄.'), ('Mean chord c̄', 'Reference length.'), ('Relaxed stability', 'Small or negative margin with computer help.')],
 'planet': {'text': ['NASA reports that after 25 flights the X-59’s real-world flight characteristics closely match simulations, including its flying qualities and its stability margin, which NASA describes as how close the aircraft is to becoming unstable under certain conditions.',
                     'The X-59 is shaped to turn a loud sonic boom into a quiet thump, and confirming its stability margin in flight is part of proving that quieter supersonic flight is practical.'],
            'site': [('Aerodynamics I', 'Aerodynamics_I.html'), ('Aircraft Performance', 'Aircraft_Performance.html')],
            'src': [_X59]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_GCG[0], _GCG[1], 'Free NASA explainer.')]})
UNITS.append(
{'id': 'u3', 'title': 'Trim and Elevator Control', 'weeks': 'Week 3',
 'summary': 'Trim as zero net pitching moment, elevator effectiveness, the elevator angle to trim, tail download and trim drag, and stick-fixed versus stick-free stability.',
 'objectives': ['Write the trim condition.', 'Solve for elevator angle to trim.', 'Explain why tails often push down.', 'Describe trim drag.'],
 'concepts': ['Trim means zero net pitching moment: C_m = C_m0 + C_mα α + C_mδe δ_e = 0.',
              'Elevator effectiveness C_mδe is negative for a tail elevator: trailing edge down gives nose down.',
              'The elevator lift acts some distance from the cg, so it makes a torque and the aircraft rotates about its cg.',
              'Modern tails often carry negative lift to keep the nose up, which the wing must offset with extra lift.',
              'That extra lift costs induced drag, called trim drag; a smaller static margin reduces it.'],
 'eqs': [('C_m=C_{m_0}+C_{m_\\alpha}\\alpha+C_{m_{\\delta_e}}\\delta_e=0', 'Trim condition'), ('\\delta_e=-\\frac{C_{m_0}+C_{m_\\alpha}\\alpha}{C_{m_{\\delta_e}}}', 'Elevator to trim'), ('C_L=C_{L_\\alpha}\\alpha', 'Lift slope'), ('L=\\tfrac12\\rho V^2SC_L', 'Lift')],
 'worked': [
  _w('C_m0 = 0.05, C_mα = −0.55, C_mδe = −1.2 per radian (sample values). Find δ_e to trim at α = 0.05 rad.', ['0.05 − 0.0275 − 1.2δ_e = 0.', 'δ_e = 0.0225/1.2.'], 'δ_e = 0.01875 rad = 1.07°.'),
  _w('What angle of attack trims with zero elevator?', ['α = 0.05/0.55.'], 'α = 0.0909 rad = 5.21°.'),
  _w('Find C_L at that trim with C_Lα = 5.5.', ['5.5 × 0.0909.'], 'C_L = 0.50.')],
 'practice': [('δ_e to trim at α = 0.1 rad?', '−0.00417 rad (−0.24°).'), ('Sign convention for δ_e?', 'Trailing edge down positive.'),
              ('Why does tail download cost fuel?', 'The wing makes more lift, adding induced drag.'), ('Where was the Wright Flyer’s elevator?', 'At the front.')],
 'misc': [('Trim means level flight.', 'It means zero net moment at any steady condition.'), ('Tails always lift upward.', 'Many push down.'), ('Elevator only changes pitch angle.', 'It sets the trimmed angle of attack and speed.')],
 'quiz': [_q('Trim: C_m = …', ['0', '1', 'C_L', 'C_mα'], 0, 'No net moment.'), _q('Example δ_e…', ['1.07°', '10°', '0°', '−5°'], 0, 'Worked.'),
          _q('Trim drag comes from…', ['extra wing lift', 'friction only', 'engines', 'gear'], 0, 'Induced.'), _q('C_mδe for a tail is…', ['negative', 'positive', 'zero', 'infinite'], 0, 'Nose down.')],
 'cards': [('Trim', 'Zero net moment.'), ('C_mδe', 'Elevator effectiveness.'), ('Elevator', 'Pitch control surface.'), ('Tail download', 'Negative tail lift.'), ('Trim drag', 'Drag from trimming.'), ('Canard', 'Forward elevator surface.')],
 'planet': {'text': ['NASA Glenn explains that the horizontal stabilizer on modern aircraft is usually set at a negative angle, making a downward force that keeps the tail down and the airplane trimmed, and that this negative force must be overcome with greater lift from the wing.',
                     'Every bit of extra lift adds drag and fuel burn, so careful trim and cg management are small but real ways to cut aviation emissions.'],
            'site': [('Aircraft Performance', 'Aircraft_Performance.html'), ('Solutions', 'Solutions.html')],
            'src': [_GEL]},
 'res': [(_GEL[0], _GEL[1], 'Free NASA interactive.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u4', 'title': 'Lateral-Directional Stability and Turns', 'weeks': 'Week 4',
 'summary': 'Weathercock (directional) stability, dihedral effect, aileron roll control, roll damping and the roll mode, adverse yaw, and the coordinated turn.',
 'objectives': ['State directional and roll stability conditions.', 'Compute roll-mode time constant and steady roll rate.', 'Find bank angle and load factor for a coordinated turn.', 'Explain adverse yaw.'],
 'concepts': ['Directional (weathercock) stability needs C_nβ > 0: a sideslip yaws the nose back into the wind.',
              'Dihedral effect needs C_lβ < 0: a sideslip rolls the aircraft away from the slip.',
              'Ailerons deflect oppositely to make a rolling moment; roll damping L_p resists roll rate, giving the roll mode with τ = 1/|L_p|.',
              'The down-going aileron makes more lift and drag, yawing the nose away from the turn (adverse yaw); the rudder fixes it.',
              'In a coordinated level turn tan φ = V²/(gR) and load factor n = 1/cos φ.'],
 'eqs': [('C_{n_\\beta}>0,\\ C_{l_\\beta}<0', 'Lateral-directional stability'), ('p_{ss}=-\\frac{L_{\\delta_a}}{L_p}\\delta_a', 'Steady roll rate'), ('\\tan\\phi=\\frac{V^2}{gR}', 'Coordinated turn'), ('n=\\frac{1}{\\cos\\phi}', 'Load factor')],
 'worked': [
  _w('A turn at 100 m/s with radius 2000 m (sample values). Find the bank angle.', ['tan φ = 100²/(9.80665 × 2000) = 0.510.'], 'φ = 27.0°.'),
  _w('Find the load factor.', ['n = 1/cos 27.0°.'], 'n = 1.122.'),
  _w('L_δa = 2.0 s⁻², L_p = −4.0 s⁻¹ (sample values), δ_a = 0.1 rad. Find τ and steady roll rate.', ['τ = 1/4.', 'p = 2.0 × 0.1/4.0.'], 'τ = 0.25 s; p = 0.05 rad/s.')],
 'practice': [('Load factor at 60° bank?', '2.0.'), ('Radius at 100 m/s and 45° bank?', '1020 m.'),
              ('What does dihedral do?', 'Rolls the aircraft level after a sideslip.'), ('Why use the rudder in a turn?', 'To cancel adverse yaw.')],
 'misc': [('Ailerons alone make a clean turn.', 'Adverse yaw needs rudder.'), ('Bank angle is independent of speed.', 'It grows with V² for a fixed radius.'), ('C_nβ should be negative.', 'Positive is stable.')],
 'quiz': [_q('Weathercock stable if…', ['C_nβ > 0', 'C_nβ < 0', 'C_lβ > 0', 'L_p > 0'], 0, 'Restoring yaw.'), _q('Example bank…', ['27.0°', '45°', '10°', '60°'], 0, 'tan⁻¹ 0.51.'),
          _q('n at 60° bank…', ['2', '1', '1.5', '3'], 0, '1/cos.'), _q('Roll mode τ…', ['1/|L_p|', 'L_p', 'L_δa', '2π'], 0, 'First order.')],
 'cards': [('Sideslip β', 'Wind angle from the side.'), ('C_nβ', 'Directional stability.'), ('C_lβ', 'Dihedral effect.'), ('Roll damping', 'L_p.'), ('Adverse yaw', 'Yaw opposite the roll.'), ('Load factor', 'Lift/weight.')],
 'planet': {'text': ['NASA Glenn’s guide explains that ailerons usually work in opposition, one up and one down, to change lift on each wing, and that airplanes turn because of the banking created by the ailerons, not because of a rudder input: the bank tilts the wing’s lift and curves the flight path.',
                     'This unit’s turn equation is that idea in numbers. Coordinated, efficient turns keep extra drag, and so extra fuel burn, small.'],
            'site': [('Aircraft Performance', 'Aircraft_Performance.html'), ('Aerodynamics I', 'Aerodynamics_I.html')],
            'src': [_GAIL, _GROT]},
 'res': [(_GAIL[0], _GAIL[1], 'Free NASA explainer.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u5', 'title': 'Equations of Motion and Dynamic Modes', 'weeks': 'Weeks 5–6',
 'summary': 'Six-degree-of-freedom equations, small-disturbance linearization, state-space form, eigenvalues, and the short-period, phugoid, roll, spiral and Dutch-roll modes.',
 'objectives': ['Linearize equations about trim.', 'Write state-space form.', 'Find natural frequency and damping from a characteristic equation.', 'Estimate the phugoid period.'],
 'concepts': ['Newton’s laws in body axes give six coupled nonlinear equations; for small disturbances about trim they become linear.',
              'State-space form ẋ = Ax + Bu; the eigenvalues of A are the modes.',
              'Longitudinal modes: a fast, well-damped short period (pitch) and a slow, lightly damped phugoid (speed–altitude exchange).',
              'Lateral modes: a fast roll mode, a slow spiral mode and the oscillating Dutch roll.',
              'A second-order mode s² + 2ζω_n s + ω_n² has natural frequency ω_n and damping ratio ζ. The phugoid approximation is ω_n ≈ √2 g/V.'],
 'eqs': [('\\dot x=Ax+Bu', 'State space'), ('\\det(sI-A)=0', 'Characteristic equation'), ('s^2+2\\zeta\\omega_ns+\\omega_n^2=0', 'Second-order mode'), ('\\omega_{ph}\\approx\\frac{\\sqrt2g}{V}', 'Phugoid approximation')],
 'worked': [
  _w('A short-period mode has s² + 2.8s + 16 = 0 (sample values). Find ω_n and ζ.', ['ω_n = √16.', 'ζ = 2.8/(2 × 4).'], 'ω_n = 4 rad/s; ζ = 0.35.'),
  _w('Estimate the phugoid frequency and period at 100 m/s.', ['ω = 1.4142 × 9.80665/100.', 'T = 2π/ω.'], 'ω = 0.1387 rad/s; T = 45.3 s.'),
  _w('Find the damped frequency of the short period.', ['ω_d = 4√(1 − 0.35²).'], 'ω_d = 3.75 rad/s.')],
 'practice': [('Phugoid period at 200 m/s?', '90.6 s.'), ('ζ for s² + 4s + 16?', '0.5.'),
              ('Which mode trades speed for height?', 'Phugoid.'), ('Which lateral mode oscillates?', 'Dutch roll.')],
 'misc': [('Linear models work at any condition.', 'Only near the trim point.'), ('All modes oscillate.', 'Roll and spiral are not oscillatory.'), ('Phugoid is fast.', 'It takes tens of seconds.')],
 'quiz': [_q('Example ζ…', ['0.35', '0.7', '4', '2.8'], 0, '2.8/8.'), _q('Phugoid period at 100 m/s…', ['45.3 s', '4.5 s', '453 s', '1 s'], 0, 'Approx.'),
          _q('Modes are…', ['eigenvalues of A', 'entries of B', 'inputs', 'gains'], 0, 'State space.'), _q('Short period is…', ['fast pitch', 'slow speed', 'roll', 'yaw'], 0, 'Definition.')],
 'cards': [('Short period', 'Fast pitch mode.'), ('Phugoid', 'Slow speed–height mode.'), ('Dutch roll', 'Yaw–roll oscillation.'), ('Spiral mode', 'Slow bank divergence or convergence.'), ('ω_n', 'Natural frequency.'), ('ζ', 'Damping ratio.')],
 'planet': {'text': ['NASA says the X-59 team uses a real-time digital twin that compares flight data to simulated predictions, and that the aircraft has shown no unexpected phenomena such as instability or excessive vibration in response to aerodynamic forces.',
                     'NASA reports the X-59 reached its target cruise of Mach 1.4 (924 mph) at 55,000 feet relatively early in testing. Models built from this unit’s linear equations are what a digital twin compares against.'],
            'site': [('Differential Equations', 'Differential_Equations.html'), ('Linear Algebra', 'Linear_Algebra.html')],
            'src': [_X59]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_MITF[0], _MITF[1], 'Free MIT course.')]})
UNITS.append(
{'id': 'u6', 'title': 'Laplace Transforms and Transfer Functions', 'weeks': 'Week 7',
 'summary': 'Transfer functions, poles and zeros, block diagrams, first-order systems, time constants, DC gain and the final value theorem.',
 'objectives': ['Write a transfer function from an ODE.', 'Find poles, DC gain and time constant.', 'Use the final value theorem.', 'Reduce simple block diagrams.'],
 'concepts': ['With zero initial conditions, the Laplace transform turns a linear ODE into algebra: Y(s) = G(s)U(s).',
              'Poles (roots of the denominator) set the natural response; left-half-plane poles decay, right-half-plane poles grow.',
              'A first-order system K/(τs + 1) reaches 63.2% of its final value at t = τ and about 98% at 4τ.',
              'The final value theorem: y(∞) = lim s→0 of sY(s), if the system is stable. For a unit step, y(∞) = G(0).',
              'Blocks in series multiply; a negative feedback loop gives G/(1 + GH).'],
 'eqs': [('G(s)=\\frac{Y(s)}{U(s)}', 'Transfer function'), ('y(t)=K(1-e^{-t/\\tau})', 'First-order step response'), ('y(\\infty)=\\lim_{s\\to0}sY(s)', 'Final value theorem'), ('T=\\frac{G}{1+GH}', 'Closed loop')],
 'worked': [
  _w('Find the pole, time constant and DC gain of G(s) = 5/(s + 2).', ['Pole at s = −2.', 'τ = 1/2.', 'G(0) = 5/2.'], 'Pole −2; τ = 0.5 s; gain 2.5.'),
  _w('Find its unit-step response at t = 0.5 s and 1 s.', ['y = 2.5(1 − e^(−2t)).'], 'y(0.5) = 1.580; y(1) = 2.162.'),
  _w('Close a unity feedback loop around G. Find the closed-loop DC gain.', ['T = 5/(s + 7).'], 'T(0) = 0.714.')],
 'practice': [('2% settling time of G?', 'About 4τ = 2 s.'), ('Fraction reached at t = τ?', '63.2%.'),
              ('Is a pole at +1 stable?', 'No; it grows as e^t.'), ('Two blocks 2 and 3/(s+1) in series?', '6/(s+1).')],
 'misc': [('Final value theorem always applies.', 'Only for stable systems.'), ('Zeros set stability.', 'Poles do.'), ('τ is the settling time.', 'Settling is about 4τ.')],
 'quiz': [_q('G(0) for 5/(s+2)…', ['2.5', '5', '2', '0.4'], 0, 'DC gain.'), _q('At t = τ…', ['63.2%', '50%', '100%', '98%'], 0, '1 − e⁻¹.'),
          _q('Stable poles lie…', ['in the left half plane', 'right half', 'on the real axis only', 'at infinity'], 0, 'Decay.'), _q('Closed loop…', ['G/(1+GH)', 'GH', 'G − H', '1/G'], 0, 'Feedback.')],
 'cards': [('Transfer function', 'Output/input in s.'), ('Pole', 'Denominator root.'), ('Zero', 'Numerator root.'), ('Time constant', 'τ.'), ('DC gain', 'G(0).'), ('Final value theorem', 'lim sY(s).')],
 'planet': {'text': ['NASA explains that Hubble’s gyroscopes measure the telescope’s slew rates and are part of the system that determines and controls the direction the telescope points.',
                     'Sensors like these are the measurement blocks in this unit’s diagrams: a controller can only be as good as the rates and angles it measures.'],
            'site': [('Differential Equations', 'Differential_Equations.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_HUB]},
 'res': [(_MITC[0], _MITC[1], 'Free MIT lectures.'), (_MITF[0], _MITF[1], 'Free MIT course.')]})
UNITS.append(
{'id': 'u7', 'title': 'Second-Order Time Response', 'weeks': 'Week 8',
 'summary': 'Underdamped step response, overshoot, peak time, settling time, damping ratio and natural frequency, and handling-quality targets.',
 'objectives': ['Compute percent overshoot from ζ.', 'Compute peak and settling times.', 'Read ζ and ω_n from pole locations.', 'Choose damping for good response.'],
 'concepts': ['Poles at −ζω_n ± jω_n√(1 − ζ²) for 0 < ζ < 1 give an oscillating response that decays.',
              'Percent overshoot depends only on ζ: M_p = exp(−ζπ/√(1 − ζ²)).',
              'Peak time t_p = π/ω_d, with ω_d = ω_n√(1 − ζ²).',
              'Settling time (2%) is about t_s = 4/(ζω_n), set by the real part of the poles.',
              'Damping near 0.7 gives small overshoot (about 4.6%) with a quick rise; pilots dislike both sluggish and oscillating responses.'],
 'eqs': [('M_p=e^{-\\zeta\\pi/\\sqrt{1-\\zeta^2}}', 'Overshoot'), ('t_p=\\frac{\\pi}{\\omega_n\\sqrt{1-\\zeta^2}}', 'Peak time'), ('t_s\\approx\\frac{4}{\\zeta\\omega_n}', 'Settling time'), ('s=-\\zeta\\omega_n\\pm j\\omega_n\\sqrt{1-\\zeta^2}', 'Poles')],
 'worked': [
  _w('For the Unit 5 short period (ω_n = 4, ζ = 0.35), find the overshoot.', ['M_p = exp(−0.35π/√(1 − 0.1225)).'], '30.9%.'),
  _w('Find its peak and settling times.', ['t_p = π/3.747.', 't_s = 4/(0.35 × 4).'], 't_p = 0.838 s; t_s = 2.86 s.'),
  _w('Find the overshoot for ζ = 0.7.', ['exp(−0.7π/√0.51).'], '4.6%.')],
 'practice': [('Overshoot at ζ = 0.25?', '44.4%.'), ('Poles for ω_n = 4, ζ = 0.35?', '−1.4 ± 3.75j.'),
              ('Overshoot at ζ = 1?', 'None (critically damped).'), ('What sets settling time?', 'The real part ζω_n.')],
 'misc': [('More damping is always better.', 'Too much makes the response sluggish.'), ('Overshoot depends on ω_n.', 'Only on ζ.'), ('Peak time uses ω_n.', 'It uses ω_d.')],
 'quiz': [_q('M_p at ζ = 0.35…', ['30.9%', '4.6%', '50%', '0%'], 0, 'Formula.'), _q('t_s ≈ …', ['4/(ζω_n)', 'π/ω_n', 'ζ/ω_n', '1/ω_n'], 0, '2% rule.'),
          _q('ζ = 0.7 overshoot…', ['4.6%', '30%', '0%', '70%'], 0, 'Formula.'), _q('Overshoot depends on…', ['ζ only', 'ω_n only', 'gain', 'input'], 0, 'Formula.')],
 'cards': [('Overshoot', 'Peak above final value.'), ('Peak time', 'π/ω_d.'), ('Settling time', '≈4/(ζω_n).'), ('ω_d', 'Damped frequency.'), ('Critical damping', 'ζ = 1.'), ('Handling qualities', 'How easily pilots fly a vehicle.')],
 'planet': {'text': ['NASA reports that between X-59 test flights, engineers made minor adjustments to the aircraft’s control software, and that its flying qualities, or controllability, matched simulations closely.',
                     'Tuning response speed and damping, the quantities in this unit, is how control software turns a radical quiet-supersonic shape into an aircraft pilots describe as “exciting but uneventful.”'],
            'site': [('Differential Equations', 'Differential_Equations.html'), ('Aircraft Performance', 'Aircraft_Performance.html')],
            'src': [_X59]},
 'res': [(_MITC[0], _MITC[1], 'Free MIT lectures.'), ('PhET: Masses and Springs', _PH + 'masses-and-springs', 'Damped oscillation.')]})
UNITS.append(
{'id': 'u8', 'title': 'Feedback and PID Control', 'weeks': 'Weeks 9–10',
 'summary': 'Why feedback, proportional, integral and derivative action, steady-state error and system type, gain selection for damping, and a pitch-attitude autopilot example.',
 'objectives': ['Close a loop and find the characteristic equation.', 'Choose a gain for a target damping.', 'Compute steady-state error.', 'Explain what D and I terms add.'],
 'concepts': ['Feedback compares the measured output to the command and acts on the error, reducing sensitivity to disturbances and model errors.',
              'Proportional gain speeds response but can reduce damping; derivative action adds damping; integral action removes steady-state error.',
              'For a plant 1/(s(s + 2)) with gain K, the closed loop is s² + 2s + K = 0, so ω_n = √K and ζ = 1/√K.',
              'System type (integrators in the loop) sets steady-state error: a type-1 loop has zero step error and ramp error a/K for this plant.',
              'PID: u = K_p e + K_i∫e dt + K_d de/dt.'],
 'eqs': [('u=K_pe+K_i\\int e\\,dt+K_d\\dot e', 'PID law'), ('1+KG(s)=0', 'Closed-loop characteristic equation'), ('s^2+(2+K_d)s+K_p=0', 'PD on 1/(s(s+2))'), ('e_{ss,ramp}=\\frac{2}{K}', 'Ramp error (this plant)')],
 'worked': [
  _w('With K = 16 on 1/(s(s + 2)), find ω_n and ζ.', ['s² + 2s + 16.', 'ω_n = 4; ζ = 2/8.'], 'ω_n = 4 rad/s; ζ = 0.25 (44% overshoot).'),
  _w('What K gives ζ = 0.7?', ['2ζω_n = 2 ⇒ ω_n = 1/0.7 = 1.429.', 'K = ω_n².'], 'K = 2.04 (slower response).'),
  _w('Keep K_p = 16 and add derivative gain for ζ = 0.7.', ['2 + K_d = 2 × 0.7 × 4.'], 'K_d = 3.6: fast and well damped.')],
 'practice': [('Ramp error with K = 16?', '0.125.'), ('Step error for this type-1 loop?', 'Zero.'),
              ('What does integral action fix?', 'Steady-state error.'), ('Risk of too much derivative gain?', 'Noise amplification.')],
 'misc': [('Higher gain always helps.', 'It can cut damping and margins.'), ('Derivative removes error.', 'Integral does.'), ('Feedback needs a perfect model.', 'It tolerates model error.')],
 'quiz': [_q('ζ with K = 16…', ['0.25', '0.7', '4', '1'], 0, '1/√K.'), _q('Integral action…', ['removes steady error', 'adds damping', 'adds noise only', 'nothing'], 0, 'PID.'),
          _q('K_d for ζ = 0.7 at K_p = 16…', ['3.6', '16', '0.7', '2'], 0, 'Worked.'), _q('Ramp error K = 16…', ['0.125', '0', '1', '2'], 0, '2/K.')],
 'cards': [('Feedback', 'Act on measured error.'), ('K_p', 'Proportional gain.'), ('K_i', 'Integral gain.'), ('K_d', 'Derivative gain.'), ('System type', 'Number of loop integrators.'), ('Steady-state error', 'Error after transients.')],
 'planet': {'text': ['NASA reports that Dragonfly recently completed its most comprehensive simulated “first flight” on flight-like avionics at Johns Hopkins APL, with flight software using simulated navigation-camera, inertial-measurement-unit and lidar data; the rotorcraft is due at Saturn’s moon Titan in 2034.',
                     'NASA’s mobility lead notes that everything Dragonfly does on Titan has to happen autonomously, without real-time help from Earth. Closed-loop feedback like this unit’s is what makes that possible.'],
            'site': [('Solutions', 'Solutions.html'), ('Orbital Mechanics', 'Orbital_Mechanics.html')],
            'src': [_DF]},
 'res': [(_MITC[0], _MITC[1], 'Free MIT lectures.'), (_MITF[0], _MITF[1], 'Free MIT course.')]})
UNITS.append(
{'id': 'u9', 'title': 'Stability Analysis: Routh, Root Locus and Margins', 'weeks': 'Week 11',
 'summary': 'The Routh–Hurwitz test, root-locus sketching, frequency response and Bode plots, gain and phase margin, and the link between phase margin and damping.',
 'objectives': ['Apply the Routh test to find a gain limit.', 'Sketch how poles move with gain.', 'Compute a phase margin.', 'Relate phase margin to damping.'],
 'concepts': ['Routh–Hurwitz finds how many poles are in the right half plane without solving the polynomial.',
              'The root locus shows closed-loop pole paths as gain rises from 0 to ∞.',
              'Bode plots show loop gain and phase versus frequency; gain margin and phase margin measure distance from instability.',
              'Phase margin PM = 180° + ∠G(jω_c) at the crossover frequency where |G| = 1.',
              'A rule of thumb for second-order loops: ζ ≈ PM/100 (PM in degrees).'],
 'eqs': [('s^3+6s^2+11s+(6+K)=0', 'Example characteristic equation'), ('66>6+K', 'Routh condition'), ('PM=180^\\circ+\\angle G(j\\omega_c)', 'Phase margin'), ('\\zeta\\approx PM/100', 'Rule of thumb')],
 'worked': [
  _w('Unity feedback around K/((s + 1)(s + 2)(s + 3)). Find the K limit.', ['Characteristic: s³ + 6s² + 11s + 6 + K.', 'Routh: 6 × 11 > 6 + K.'], 'Stable for K < 60.'),
  _w('At K = 60, at what frequency does it oscillate?', ['Auxiliary 6s² + 66 = 0.'], 'ω = √11 = 3.317 rad/s.'),
  _w('Find the phase margin of 16/(s(s + 2)).', ['|G| = 1 at ω_c = 3.758 rad/s.', 'PM = 90° − tan⁻¹(3.758/2).'], 'PM = 28.0°, so ζ ≈ 0.28 (exact 0.25).')],
 'practice': [('Is K = 30 stable in the example?', 'Yes.'), ('Gain margin at K = 30?', '2 (60/30).'),
              ('What happens to the locus as K → ∞ here?', 'Two branches cross into the right half plane.'), ('Typical PM target?', 'About 45°–60°.')],
 'misc': [('Stable at one gain means stable at all.', 'Gain limits are common.'), ('Phase margin is measured at 180° crossing.', 'At gain crossover.'), ('Routh gives pole locations.', 'Only counts.')],
 'quiz': [_q('K limit example…', ['60', '6', '11', '66'], 0, 'Routh.'), _q('Oscillation at K = 60…', ['3.317 rad/s', '6 rad/s', '1 rad/s', '60 rad/s'], 0, '√11.'),
          _q('PM example…', ['28°', '45°', '90°', '0°'], 0, 'Worked.'), _q('ζ ≈ …', ['PM/100', 'PM', '1/PM', 'GM'], 0, 'Rule.')],
 'cards': [('Routh test', 'Counts RHP poles.'), ('Root locus', 'Pole paths with gain.'), ('Bode plot', 'Gain and phase vs frequency.'), ('Gain margin', 'Gain factor to instability.'), ('Phase margin', 'Phase to instability.'), ('Crossover', '|G| = 1.')],
 'planet': {'text': ['NASA says Dragonfly engineers will test other flight profiles and deliberately introduce faults to make sure the rotorcraft can respond autonomously if something goes wrong.',
                     'Margins are the engineering answer to “what if”: a loop with healthy gain and phase margins keeps working when parts age, sensors drift or the environment surprises it.'],
            'site': [('Linear Algebra', 'Linear_Algebra.html'), ('Solutions', 'Solutions.html')],
            'src': [_DF]},
 'res': [(_MITC[0], _MITC[1], 'Free MIT lectures.'), (_MITF[0], _MITF[1], 'Free MIT course.')]})
UNITS.append(
{'id': 'u10', 'title': 'Spacecraft Attitude Determination and Control', 'weeks': 'Weeks 12–13',
 'summary': 'Rigid-body rotation, attitude sensors (gyros, star trackers), reaction wheels and momentum, bang-bang slews, safe modes, and pointing for Earth and space science.',
 'objectives': ['Use τ = Iα for single-axis slews.', 'Compute a minimum-time slew.', 'Compute wheel momentum.', 'Explain gyro roles and safe modes.'],
 'concepts': ['Single-axis rotation: torque τ = Iα; angular momentum H = Iω.',
              'A bang-bang slew accelerates for half the angle and brakes for the other half: t = 2√(θ/α).',
              'Reaction wheels trade momentum with the spacecraft; wheels saturate and must be unloaded with thrusters or magnetic torquers.',
              'Gyros measure rates and star trackers measure attitude; filters combine them.',
              'Safe modes put a spacecraft in a simple, power-positive attitude when something looks wrong.'],
 'eqs': [('\\tau=I\\alpha', 'Rotational Newton’s law'), ('t=2\\sqrt{\\theta/\\alpha}', 'Bang-bang slew time'), ('H=I\\omega', 'Angular momentum'), ('\\omega_{max}=\\alpha t/2', 'Peak slew rate')],
 'worked': [
  _w('A spacecraft with I = 1000 kg·m² has 0.5 N·m of wheel torque (sample values). Find α and the 90° slew time.', ['α = 0.5/1000 = 5 × 10⁻⁴ rad/s².', 't = 2√(1.5708/0.0005).'], 't = 112.1 s.'),
  _w('Find the peak rate during that slew.', ['ω = 0.0005 × 112.1/2.'], '0.0280 rad/s (1.61°/s).'),
  _w('A wheel has I = 0.1 kg·m² spinning at 600 rad/s (sample values). Find its momentum.', ['H = 0.1 × 600.'], '60 N·m·s.')],
 'practice': [('45° slew time?', '79.3 s.'), ('Time for 0.5 N·m to build 60 N·m·s?', '120 s.'),
              ('What do gyros measure?', 'Rotation rates.'), ('Why unload wheels?', 'They saturate at maximum speed.')],
 'misc': [('Slew time scales with angle.', 'It scales with √θ for bang-bang.'), ('Wheels add momentum forever.', 'They saturate.'), ('Gyros give absolute attitude.', 'They give rates; trackers give attitude.')],
 'quiz': [_q('90° slew example…', ['112.1 s', '11 s', '1000 s', '56 s'], 0, '2√(θ/α).'), _q('H = …', ['Iω', 'Iα', 'τt²', 'm v'], 0, 'Momentum.'),
          _q('Wheel H example…', ['60 N·m·s', '6', '600', '0.1'], 0, '0.1 × 600.'), _q('Hubble now points with…', ['one gyro', 'six gyros', 'no gyros', 'thrusters only'], 0, 'NASA 2024.')],
 'cards': [('Reaction wheel', 'Momentum-exchange actuator.'), ('Star tracker', 'Attitude from stars.'), ('Gyro', 'Rate sensor.'), ('Bang-bang', 'Full torque, then full reverse.'), ('Saturation', 'Wheel at maximum speed.'), ('Safe mode', 'Protective fallback state.')],
 'planet': {'text': ['NASA reported in June 2024 that Hubble would switch to operating with one gyro, keeping another in reserve, after a gyro began “saturating”—reading the maximum slew rate regardless of actual motion—and repeatedly sent the telescope into safe mode. NASA said most observations would be unaffected, with longer slews, less pointing flexibility and no tracking of moving objects closer than Mars.',
                     'The same attitude-control ideas point Earth-observing satellites such as GOES-19 and Landsat at the planet they measure.'],
            'site': [('GOES-19', 'GOES-19.html'), ('Orbital Mechanics', 'Orbital_Mechanics.html')],
            'src': [_HUB]},
 'res': [(_MITF[0], _MITF[1], 'Free MIT course.'), (_HUB[0], _HUB[1], 'NASA article.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Balancing moments and finding the cg', 'week': 'Week 1',
 'goal': 'Balance masses on a plank in PhET Balancing Act, then compute an aircraft-style center of gravity in a spreadsheet.',
 'eq': ('x_{cg}=\\frac{\\sum m_ix_i}{\\sum m_i}', 'Center of gravity'),
 'steps': ['In PhET Balancing Act, place 10 kg at 1 m on one side and find where 5 kg balances it.', 'Record moment = mass × distance on each side.', 'In a spreadsheet, list the Unit 1 masses and distances and compute x_cg.', 'Add 200 kg at 10 m and recompute.'],
 'table': (['Case', 'Σm (kg)', 'x_cg (m)'], [['Base', '1800', '4.44'], ['+200 kg at 10 m', '2000', '5.00']]),
 'note': 'Computed sample values.',
 'calc': ['8000/1800 = 4.44 m.', '10,000/2000 = 5.00 m.'],
 'safety': ['Computer only.'], 'home': ['Any browser and spreadsheet work.'],
 'sims': [('PhET: Balancing Act', _PH + 'balancing-act'), (_GCG[0], _GCG[1])],
 'planet': 'NASA Glenn: in flight, airplanes and rockets rotate about their centers of gravity.', 'planet_src': [_GCG]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Static margin and trim sweep', 'week': 'Week 3',
 'goal': 'Sweep cg position and compute static margin, C_mα and the zero-elevator trim angle.',
 'eq': ('\\alpha_{trim}=\\frac{C_{m_0}}{C_{L_\\alpha}SM}', 'Trim angle with zero elevator'),
 'steps': ['Use x_np = 0.35c̄, C_Lα = 5.5 /rad, C_m0 = 0.05 (sample values).', 'Sweep x_cg from 0.20 to 0.40 c̄.', 'Compute SM, C_mα and α_trim.', 'Note what happens at and beyond the neutral point.'],
 'table': (['x_cg/c̄', 'SM', 'C_mα (/rad)', 'α_trim (rad)'], [['0.20', '0.15', '−0.825', '0.0606'], ['0.25', '0.10', '−0.55', '0.0909'], ['0.30', '0.05', '−0.275', '0.182']]),
 'note': 'Computed sample values; no stable trim at or aft of the neutral point.',
 'calc': ['C_mα = −5.5 × 0.15 = −0.825.', 'α = 0.05/0.275 = 0.182 rad.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_GEL[0], _GEL[1])],
 'planet': 'NASA reports the X-59’s stability margin matched predictions in flight.', 'planet_src': [_X59]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Damped oscillation as a second-order mode', 'week': 'Week 6',
 'goal': 'Watch damped oscillation in PhET Masses and Springs and compare with the second-order formulas.',
 'eq': ('\\omega_n=\\sqrt{k/m},\\ \\zeta=\\frac{c}{2\\sqrt{km}}', 'Spring-mass-damper'),
 'steps': ['In PhET Masses and Springs, hang a mass, add some damping and pull it down.', 'Time several cycles and estimate the period and decay.', 'In a spreadsheet, compute ω_n, ζ, period and overshoot for m = 0.5 kg, k = 20 N/m, c = 1 N·s/m (sample values).', 'Explain how this matches the short-period mode.'],
 'table': (['Quantity', 'Value'], [['ω_n', '6.32 rad/s'], ['ζ', '0.158'], ['Damped period', '1.006 s'], ['Overshoot', '60.5%']]),
 'note': 'Computed sample values; simulation readings will differ.',
 'calc': ['ω_n = √40 = 6.32.', 'ζ = 1/(2√10) = 0.158.'],
 'safety': ['Computer only.'], 'home': ['Any browser and spreadsheet work.'],
 'sims': [('PhET: Masses and Springs', _PH + 'masses-and-springs')],
 'planet': 'NASA says the X-59 has shown no unexpected instability or excessive vibration.', 'planet_src': [_X59]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Step responses by time-stepping', 'week': 'Week 8',
 'goal': 'Simulate first- and second-order step responses with small Euler steps and compare with the formulas.',
 'eq': ('x_{k+1}=x_k+\\Delta t\\,\\dot x_k', 'Euler step'),
 'steps': ['Simulate ẏ = −2y + 5 from y = 0 with Δt = 0.001 s.', 'Simulate ÿ + 2.8ẏ + 16y = 16 from rest.', 'Find y(0.5) for the first and the peak and peak time for the second.', 'Compare with exact formulas.'],
 'table': (['Quantity', 'Exact'], [['First order y(0.5)', '1.580'], ['Second order peak', '1.309'], ['Peak time', '0.838 s'], ['Settling (2%)', '2.86 s']]),
 'note': 'Computed values; small steps match closely.',
 'calc': ['2.5(1 − e⁻¹) = 1.580.', '1 + 0.309 = 1.309.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet or Python works.'],
 'sims': [(_MITC[0], _MITC[1])],
 'planet': 'NASA’s X-59 team compares flight data with a real-time digital twin.', 'planet_src': [_X59]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Tuning a pitch-attitude autopilot', 'week': 'Week 10',
 'goal': 'Compare P and PD control of the plant 1/(s(s + 2)) by simulation.',
 'eq': ('s^2+(2+K_d)s+K_p=0', 'Closed loop with PD'),
 'steps': ['Simulate θ̈ + 2θ̇ = u with u = K_p(θ_cmd − θ) − K_dθ̇.', 'Try K_p = 16, K_d = 0; then K_p = 2.04; then K_p = 16, K_d = 3.6.', 'Record overshoot and settling time.', 'Choose the best design and explain.'],
 'table': (['Design', 'Overshoot', 'Settling (s)'], [['K_p = 16', '44.4%', '4.0'], ['K_p = 2.04', '4.6%', '4.0'], ['K_p = 16, K_d = 3.6', '4.6%', '1.43']]),
 'note': 'Computed from second-order formulas.',
 'calc': ['ζ = 0.25 ⇒ 44.4%; t_s = 4/(0.25 × 4) = 4.0 s.', 'PD: t_s = 4/(0.7 × 4) = 1.43 s.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet or Python works.'],
 'sims': [(_MITF[0], _MITF[1])],
 'planet': 'NASA: Dragonfly must fly autonomously at Titan without real-time help from Earth.', 'planet_src': [_DF]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Reaction-wheel slew planner', 'week': 'Week 13',
 'goal': 'Plan bang-bang slews for a spacecraft and check peak rates and wheel momentum.',
 'eq': ('t=2\\sqrt{\\theta/\\alpha}', 'Bang-bang slew time'),
 'steps': ['Set I = 1000 kg·m² and τ = 0.5 N·m (sample values).', 'Compute slew times for 30°, 90° and 180°.', 'Compute the peak rate and the momentum the wheels must absorb.', 'Discuss how losing a sensor would change planning.'],
 'table': (['Slew', 'Time (s)'], [['30°', '64.7'], ['90°', '112.1'], ['180°', '158.5']]),
 'note': 'Computed sample values.',
 'calc': ['t = 2√(0.5236/0.0005) = 64.7 s.', 't = 2√(3.1416/0.0005) = 158.5 s.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_HUB[0], _HUB[1])],
 'planet': 'NASA: in one-gyro mode Hubble needs more time to slew and lock onto targets.', 'planet_src': [_HUB]})
SCHEDULE = [(1, 'u1', 'Axes, cg and moments; Lab A', 'NASA Glenn'), (2, 'u2', 'Longitudinal static stability', 'MIT 16.333'),
            (3, 'u3', 'Trim and elevator; Lab B', 'NASA Glenn'), (4, 'u4', 'Lateral-directional stability and turns', 'MIT 16.333'),
            (5, 'u5', 'Equations of motion and linearization', 'MIT 16.333'), (6, 'u5', 'Dynamic modes; Lab C', 'MIT 16.333'),
            (7, 'u6', 'Transfer functions; midterm practice', 'MIT 16.06'), (8, 'u7', 'Second-order response; Lab D', 'MIT 16.06'),
            (9, 'u8', 'Feedback and PID', 'MIT 16.06'), (10, 'u8', 'Autopilot design; Lab E', 'MIT 16.30'),
            (11, 'u9', 'Routh, root locus and margins', 'MIT 16.06'), (12, 'u10', 'Attitude dynamics and sensors', 'MIT 16.30'),
            (13, 'u10', 'Reaction wheels and slews; Lab F', 'NASA Hubble'), (14, 'u10', 'Autonomy and fault response', 'NASA Dragonfly'), (15, 'u10', 'Review; final practice', 'MIT 16.06')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Masses 600 kg at 3 m and 400 kg at 8 m. Find the cg.', ['(1800 + 3200)/1000.'], '5.0 m.'),
  ('x_np = 0.40c̄, x_cg = 0.28c̄, C_Lα = 5 /rad. Find SM and C_mα.', ['SM = 0.12.', '−5 × 0.12.'], 'SM = 0.12; C_mα = −0.60 /rad.'),
  ('C_m0 = 0.04, C_mα = −0.6, C_mδe = −1.0. Find δ_e to trim at α = 0.05 rad.', ['0.04 − 0.03 − δ_e = 0.'], 'δ_e = 0.01 rad (0.57°).'),
  ('Bank angle for a 1500 m radius turn at 80 m/s?', ['tan φ = 6400/14,710.'], '23.5°.'),
  ('Find ω_n and ζ for s² + 3s + 25.', ['ω_n = 5; ζ = 3/10.'], 'ω_n = 5 rad/s; ζ = 0.3.')]),
 ('Final practice set (Units 1–10)', [
  ('Step response of 4/(s + 4) at t = 0.25 s?', ['1 − e⁻¹.'], '0.632.'),
  ('Overshoot and settling time for ω_n = 5, ζ = 0.3?', ['exp(−0.3π/√0.91).', '4/1.5.'], '37.2%; 2.67 s.'),
  ('K on 1/(s(s + 4)) for ζ = 0.5?', ['2ζω_n = 4 ⇒ ω_n = 4.'], 'K = 16.'),
  ('Max K for s³ + 3s² + 2s + K?', ['3 × 2 > K.'], 'K < 6.'),
  ('Slew time for 60° with α = 0.001 rad/s²?', ['2√(1.0472/0.001).'], '64.7 s.'),
  ('Momentum of a 0.05 kg·m² wheel at 400 rad/s?', ['0.05 × 400.'], '20 N·m·s.')])]
FORMULAS = ['x_{cg}=\\sum m_ix_i/\\sum m_i,\\ M=Fd', 'SM=(x_{np}-x_{cg})/\\bar c,\\ C_{m_\\alpha}=-C_{L_\\alpha}SM', '\\delta_e=-(C_{m_0}+C_{m_\\alpha}\\alpha)/C_{m_{\\delta_e}}',
            '\\tan\\phi=V^2/(gR),\\ n=1/\\cos\\phi,\\ \\tau_r=1/|L_p|', 's^2+2\\zeta\\omega_ns+\\omega_n^2,\\ \\omega_{ph}\\approx\\sqrt2g/V', 'y=K(1-e^{-t/\\tau}),\\ y(\\infty)=G(0)',
            'M_p=e^{-\\zeta\\pi/\\sqrt{1-\\zeta^2}},\\ t_p=\\pi/\\omega_d,\\ t_s\\approx4/(\\zeta\\omega_n)', 'u=K_pe+K_i\\int e+K_d\\dot e,\\ T=G/(1+GH)',
            'PM=180^\\circ+\\angle G(j\\omega_c),\\ \\zeta\\approx PM/100', '\\tau=I\\alpha,\\ H=I\\omega,\\ t=2\\sqrt{\\theta/\\alpha}']
GLOSSARY = sorted([('Aileron', 'Roll control surface.'), ('Center of gravity', 'Average location of mass.'), ('Damping ratio', 'ζ, how fast oscillations decay.'), ('Dutch roll', 'Coupled yaw–roll oscillation.'),
    ('Elevator', 'Pitch control surface.'), ('Gain margin', 'Gain increase to instability.'), ('Gyroscope', 'Sensor that measures rotation rate.'), ('Natural frequency', 'ω_n of an undamped mode.'),
    ('Neutral point', 'cg location with neutral pitch stability.'), ('Overshoot', 'Peak above the final value.'), ('Phase margin', 'Extra phase lag to instability.'), ('Phugoid', 'Slow speed–altitude mode.'),
    ('PID controller', 'Proportional-integral-derivative control.'), ('Reaction wheel', 'Spinning wheel for attitude control.'), ('Root locus', 'Closed-loop pole paths with gain.'), ('Rudder', 'Yaw control surface.'),
    ('Short period', 'Fast pitch mode.'), ('Static margin', 'Distance from cg to neutral point over chord.'), ('Transfer function', 'Laplace-domain output over input.'), ('Trim', 'Zero net moment.')])
RUBRIC = [('4 · Mastery', 'Draws axes and block diagrams, picks the right model, checks poles, damping and margins, and explains handling and safety trades in plain words.'), ('3 · Proficient', 'Solves the practice problems with occasional slips in signs or units.'),
          ('2 · Developing', 'Follows worked examples but confuses static and dynamic stability or ω_n and ω_d.'), ('1 · Beginning', 'Plugs numbers into formulas without a diagram; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    g = 9.80665
    mp = lambda z: exp(-z * pi / sqrt(1 - z * z))
    bank = lambda V, R: degrees(atan(V * V / (g * R)))
    slew = lambda d, a: 2 * sqrt(radians(d) / a)
    w2 = (-4 + sqrt(16 + 1024)) / 2; wc = sqrt(w2); pm = 90 - degrees(atan(wc / 2))
    de = (0.05 - 0.55 * 0.05) / 1.2
    wnC = sqrt(20 / .5); zC = 1 / (2 * sqrt(20 * .5))
    r = [
     ('u1 M', 2000 * 6, 12000), ('u1 m', 1000 + 500 + 300, 1800), ('u1 mx', 1000 * 2 + 500 * 6 + 300 * 10, 8000), ('u1 cg', 8000 / 1800, 4.44), ('u1 p1', 500 * 4, 2000), ('u1 p3', (8000 + 2000) / 2000, 5.0),
     ('u2 SM', .35 - .25, .10), ('u2 Cma', -5.5 * .10, -.55), ('u2 SM2', .35 - .30, .05), ('u2 Cma2', -5.5 * .05, -.275),
     ('u3 de', de, .01875), ('u3 deg', degrees(de), 1.07), ('u3 a0', .05 / .55, .0909), ('u3 a0d', degrees(.05 / .55), 5.21), ('u3 CL', 5.5 * .05 / .55, .50), ('u3 p1', (0.05 - 0.055) / 1.2, -.00417),
     ('u3 p1d', degrees((0.05 - 0.055) / 1.2), -.24), ('u3 q', degrees(de), 1.07),
     ('u4 tan', 100 ** 2 / (g * 2000), .510), ('u4 phi', bank(100, 2000), 27.0), ('u4 n', 1 / cos(atan(100 ** 2 / (g * 2000))), 1.122), ('u4 tau', 1 / 4, .25), ('u4 p', 2 * .1 / 4, .05),
     ('u4 n60', 1 / cos(radians(60)), 2.0), ('u4 R45', 100 ** 2 / g, 1020),
     ('u5 wn', sqrt(16), 4), ('u5 z', 2.8 / 8, .35), ('u5 wph', sqrt(2) * g / 100, .1387), ('u5 Tph', 2 * pi / (sqrt(2) * g / 100), 45.3), ('u5 wd', 4 * sqrt(1 - .35 ** 2), 3.75),
     ('u5 T200', 2 * pi / (sqrt(2) * g / 200), 90.6), ('u5 z4', 4 / 8, .5), ('u5 mach', 924 / 1.4, 660),
     ('u6 tau', 1 / 2, .5), ('u6 G0', 5 / 2, 2.5), ('u6 y05', 2.5 * (1 - exp(-1)), 1.580), ('u6 y1', 2.5 * (1 - exp(-2)), 2.162), ('u6 cl', 5 / 7, .714), ('u6 ts', 4 * .5, 2),
     ('u6 63', 1 - exp(-1), .632), ('u6 ser', 2 * 3, 6),
     ('u7 mp', mp(.35), .309), ('u7 tp', pi / (4 * sqrt(1 - .35 ** 2)), .838), ('u7 ts', 4 / (.35 * 4), 2.86), ('u7 mp7', mp(.7), .046), ('u7 mp25', mp(.25), .444), ('u7 re', .35 * 4, 1.4),
     ('u7 im', 4 * sqrt(1 - .35 ** 2), 3.75),
     ('u8 wn', sqrt(16), 4), ('u8 z', 2 / 8, .25), ('u8 os', mp(.25), .444), ('u8 wn7', 1 / .7, 1.429), ('u8 K7', (1 / .7) ** 2, 2.04), ('u8 Kd', 2 * .7 * 4 - 2, 3.6), ('u8 ess', 2 / 16, .125),
     ('u9 Km', 6 * 11 - 6, 60), ('u9 w', sqrt(11), 3.317), ('u9 wc', wc, 3.758), ('u9 pm', pm, 28.0), ('u9 z', pm / 100, .28), ('u9 gm', 60 / 30, 2), ('u9 ex', 1 / sqrt(16), .25),
     ('u10 a', .5 / 1000, 5e-4), ('u10 t90', slew(90, 5e-4), 112.1), ('u10 wpk', 5e-4 * slew(90, 5e-4) / 2, .0280), ('u10 wdeg', degrees(5e-4 * slew(90, 5e-4) / 2), 1.61), ('u10 H', .1 * 600, 60),
     ('u10 t45', slew(45, 5e-4), 79.3), ('u10 tH', 60 / .5, 120), ('u10 rad', radians(90), 1.5708),
     ('labA m', 10 * 1 / 5, 2), ('labA cg', 8000 / 1800, 4.44), ('labA cg2', 10000 / 2000, 5.0), ('labA M', 2000, 1800 + 200),
     ('labB s1', .35 - .20, .15), ('labB c1', -5.5 * .15, -.825), ('labB a1', .05 / (5.5 * .15), .0606), ('labB s2', .35 - .25, .10), ('labB c2', -5.5 * .10, -.55), ('labB a2', .05 / (5.5 * .10), .0909),
     ('labB s3', .35 - .30, .05), ('labB c3', -5.5 * .05, -.275), ('labB a3', .05 / (5.5 * .05), .182),
     ('labC wn', wnC, 6.32), ('labC z', zC, .158), ('labC T', 2 * pi / (wnC * sqrt(1 - zC ** 2)), 1.006), ('labC os', mp(zC), .605), ('labC w2', 20 / .5, 40),
     ('labD y', 2.5 * (1 - exp(-1)), 1.580), ('labD pk', 1 + mp(.35), 1.309), ('labD tp', pi / (4 * sqrt(1 - .35 ** 2)), .838), ('labD ts', 4 / 1.4, 2.86),
     ('labE os1', mp(.25), .444), ('labE ts1', 4 / (.25 * 4), 4.0), ('labE os2', mp(.7), .046), ('labE ts2', 4 / (.7 * sqrt(2.04)), 4.0), ('labE ts3', 4 / (.7 * 4), 1.43), ('labE kd', 2 * .7 * 4 - 2, 3.6),
     ('labF 30', slew(30, 5e-4), 64.7), ('labF 90', slew(90, 5e-4), 112.1), ('labF 180', slew(180, 5e-4), 158.5), ('labF r30', radians(30), .5236), ('labF r180', radians(180), 3.1416),
     ('mid cg', (600 * 3 + 400 * 8) / 1000, 5.0), ('mid sm', .40 - .28, .12), ('mid cma', -5 * .12, -.60), ('mid de', .04 - .6 * .05, .01), ('mid ded', degrees(.01), .57), ('mid tan', 6400 / (g * 1500), .435),
     ('mid phi', bank(80, 1500), 23.5), ('mid wn', sqrt(25), 5), ('mid z', 3 / 10, .3), ('mid gr', g * 1500, 14710),
     ('fin y', 1 - exp(-1), .632), ('fin os', mp(.3), .372), ('fin ts', 4 / (.3 * 5), 2.67), ('fin K', 4 ** 2, 16), ('fin Km', 3 * 2, 6), ('fin sl', slew(60, .001), 64.7), ('fin H', .05 * 400, 20),
     ('fin r60', radians(60), 1.0472),
     ('c g', g, 9.80665), ('c rad', degrees(1), 57.2958), ('c ft', .3048, .3048), ('c 63', 1 - exp(-1), .632), ('c 98', 1 - exp(-4), .98), ('c rho', 1.225, 1.225),
     ('x u1 d', 8000 / 1800 - 2, 2.44), ('x u2 r', .55 / .275, 2), ('x u3 r', .0225 / 1.2, .01875), ('x u4 v2', 100 ** 2, 10000), ('x u5 r', 90.6 / 45.3, 2), ('x u6 e', exp(-2), .135),
     ('x u7 r', .309 / .046, 6.72), ('x u8 r', 16 / 2.04, 7.84), ('x u9 r', 3.758 / 2, 1.879), ('x u10 r', 112.1 / 79.3, 1.414), ('x labC c', 2 * sqrt(20 * .5), 6.32), ('x labF r', 158.5 / 112.1, 1.414),
     ('x mid r', 1800 / 1000, 1.8), ('x fin r', 2.67 * 1.5, 4.0), ('x u4 n2', 1.122 ** 2, 1.259), ('x u5 z2', .35 ** 2, .1225), ('x u7 s', sqrt(1 - .35 ** 2), .937), ('x u9 sq', 16 + 1024, 1040),
     ('x u3 c', .05 - .0275, .0225), ('x u8 2z', 2 * .7 * 4, 5.6), ('x u10 h', 60 / 1000, .06), ('x labB r', .182 / .0909, 2.0), ('x labE r', 4.0 / 1.43, 2.8), ('x x59', 924 * 1.609, 1487),
     ('x u6 c', 7 - 2, 5), ('x u2 p', .35 - .40, -.05), ('x u5 4', 16 ** .5, 4), ('x labA b', 10 * 1, 5 * 2), ('x lp', 4.0, 1 / .25), ('x mid r2', 25 ** .5, 5),
     ('y u4 R', 100 ** 2 / (g * .5098581), 2000), ('y u5 pp', -2.8 / 2, -1.4), ('y u6 y2', 2.5 * (1 - exp(-4)), 2.454), ('y u7 wd', pi / .838, 3.75), ('y u8 os7', mp(.7), .046), ('y u9 a', degrees(atan(wc / 2)), 62.0),
     ('y u10 t180', slew(180, 5e-4), 158.5), ('y labC zz', 1 / sqrt(40), .158), ('y labD e', exp(-1), .368), ('y mid t', 80 ** 2, 6400), ('y fin z', 4 / (2 * 4), .5), ('y fin wd', 5 * sqrt(.91), 4.77),
     ('y u2 np', .25 + .10, .35), ('y u3 m', .05 - .55 * .05, .0225), ('y u1 add', 200 * 10, 2000), ('y u9 k30', 60 / 2, 30), ('y labB d', .0909 / .0606, 1.5)]
    return r
