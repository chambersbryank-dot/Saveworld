"""Differential Equations (MATH 220): first-order ODEs, modeling, second-order linear equations and oscillations, forced vibration and resonance, Laplace transforms, linear systems and eigenvalues, nonlinear systems and stability, numerical methods, series solutions and Fourier series / the heat equation.
Oct 25 2026, founder-approved four-year track, sophomore course 2. Same module fields as chem110.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, sin, cos, exp, log
ID = 'diffeq'
STATUS = 'live'
YEAR = 2
PAGE = 'Differential_Equations.html'
CODE = 'MATH 220'
TITLE = 'Differential Equations'
LAB_TITLE = 'Computer labs'
TAGLINE = 'Modeling change: first-order equations, oscillations and resonance, Laplace transforms, systems and phase planes, stability, numerical methods and the heat equation, with four computer labs on epidemics, predators and prey, climate and wind-turbine vibration.'
DESC = 'Free self-study Differential Equations: first-order ODEs, oscillations, resonance, Laplace, systems, eigenvalues, stability, RK4, Fourier and PDEs.'
ALT = 'NASA image of Earth'
_L = 'https://www.jirka.org/diffyqs/html/'
OS = _L
_EB = ('NASA Earth Observatory: Climate and Earth’s Energy Budget', 'https://earthobservatory.nasa.gov/features/EnergyBalance')
_CC = ('NASA Earth Observatory: The Carbon Cycle', 'https://earthobservatory.nasa.gov/features/CarbonCycle')
_GL = ('U.S. EPA: Physical features of the Great Lakes (retention times)', 'https://www.epa.gov/greatlakes/physical-features-great-lakes')
_GWP = ('U.S. EPA: Understanding global warming potentials', 'https://www.epa.gov/ghgemissions/understanding-global-warming-potentials')
_FISH = ('NOAA Fisheries: population assessments', 'https://www.fisheries.noaa.gov/topic/population-assessments')
_ISR = ('National Park Service: Wolves of Isle Royale', 'https://www.nps.gov/isro/learn/nature/wolves.htm')
_ISW = ('Wolves and Moose of Isle Royale project (long-term data)', 'https://www.isleroyalewolf.org/')
_WT = ('U.S. DOE: How do wind turbines work?', 'https://www.energy.gov/eere/wind/how-do-wind-turbines-work')
_CO2 = ('NOAA Global Monitoring Laboratory: Trends in atmospheric CO₂', 'https://gml.noaa.gov/ccgg/trends/')
_IPCC = ('IPCC AR6 Working Group I: The Physical Science Basis', 'https://www.ipcc.ch/report/ar6/wg1/')
_TR = ('Trench: Elementary Differential Equations (free text)', 'https://digitalcommons.trinity.edu/mono/8/')
_MIT = ('MIT OpenCourseWare 18.03SC Differential Equations', 'https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/')
_PH = 'https://phet.colorado.edu/en/simulations/'
BANNER = ['images/earth-blue-marble-land-ocean-ice-cloud.jpg', 'images/GRACE_FO_PIA22445.jpg', 'images/Sentinel6B_Launch.jpg', 'images/SWOT_Orbit_Illustration.jpg']
CREDITS = {'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA', 'images/GRACE_FO_PIA22445.jpg': 'NASA/JPL-Caltech',
           'images/Sentinel6B_Launch.jpg': 'NASA/Carla Thomas (AFRC2025-0170-03)', 'images/SWOT_Orbit_Illustration.jpg': 'CNES (PIA25623)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a sophomore course in ordinary differential equations, modeled on the topics and depth of MIT OpenCourseWare 18.03 and the free textbooks by Jiří Lebl (Notes on Diffy Qs) and William Trench, and on the syllabi of courses such as Georgia Tech MATH 2552 and Stanford Math 53. We link to the free materials throughout. None of those authors or organizations endorses this page.',
         'What we add: every unit connects to a real planet problem with a cited public source (lakes, methane, fisheries, carbon, climate, epidemics, wind turbines), every number on the page is re-computed by a checking script before it goes live, and four computer labs solve real models numerically.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Almost every model of the living planet is a differential equation: how fast a lake flushes out a pollutant, how a fish stock recovers, how carbon moves between air and sea, how quickly Earth warms when its energy balance shifts, how an epidemic spreads, and how a wind-turbine tower sways.',
                 'Each unit ends with a short, sourced section showing how its ideas help both people and nature. Model parameters that are not from a source are labeled as sample values.']
PREREQS = ['Calculus I and II: derivatives, integrals, partial fractions, Taylor series.', 'Matrices, determinants and eigenvalues of 2 × 2 matrices (taught briefly in Unit 6).', 'Calculus III helps for the heat equation but is not required.']
STUDY = ['Check every solution by substituting it back into the equation.', 'Do every practice problem on paper before opening the answer.',
         'Sketch a slope field or phase portrait before solving; know what the answer should look like.', 'Ask of every model: what are the units, and does the long-run behavior make sense?',
         'Solve one problem from each unit numerically too, and compare with the formula.', 'Retake the quizzes a few days later. Spaced practice beats one long session.']
LAB_GEAR = ['A computer or tablet with a spreadsheet.', 'A free graphing calculator such as Desmos.', 'Optional: Python with NumPy (free in Google Colab).']
LAB_INTRO = ['Four computer labs: an SIR epidemic solved with Euler and RK4, a predator-prey phase plane, a climate energy-balance model, and a frequency sweep of a wind-turbine tower model.',
             'Sample parameters are labeled as such; each lab links to a public source for the real system.']
SAFETY_SRC = ('Lebl: Notes on Diffy Qs (free textbook)', 'https://www.jirka.org/diffyqs/')
CONST_SRC = _EB
CONSTANTS = [('Stefan–Boltzmann constant σ', '5.67 × 10⁻⁸ W/(m²·K⁴)'), ('Average sunlight at the top of the atmosphere', '340 W/m²'), ('Fraction of sunlight reflected', '29%'),
             ('Lake Superior retention time', '191 years'), ('Lake Erie retention time', '2.6 years'), ('Methane’s average lifetime', 'about a decade')]
REF_TITLE = 'Free texts and tools'
REF_INTRO = 'Use these free textbooks and tools alongside the course.'
PTABLE = [('Lebl: Notes on Diffy Qs', 'https://www.jirka.org/diffyqs/', 'Free, complete textbook for this course.'), (_TR[0], _TR[1], 'Free textbook with many exercises.'),
          (_MIT[0], _MIT[1], 'Free MIT lectures, recitations and problem sets.'), ('Desmos graphing calculator', 'https://www.desmos.com/calculator', 'Graph solutions and slope fields.'),
          ('PhET: Masses and Springs', _PH + 'masses-and-springs', 'Damping and oscillation intuition.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'First-Order Equations', 'weeks': 'Weeks 1–2',
 'summary': 'Slope fields, separable equations, linear equations with integrating factors, exact equations, and when a solution exists and is unique.',
 'objectives': ['Read a slope field and sketch solutions.', 'Solve separable and linear first-order equations.', 'Recognize and solve exact equations.', 'State the existence and uniqueness theorem and spot when it fails.'],
 'concepts': ['A differential equation relates an unknown function to its derivatives; a solution is a function that makes it true.', 'Separable: dy/dx = g(x)h(y). Divide and integrate both sides.',
              'Linear: y′ + p(x)y = q(x). Multiply by the integrating factor μ = e^(∫p dx) so the left side becomes (μy)′.', 'Exact: M dx + N dy = 0 with M_y = N_x is dF = 0, so F(x, y) = C.',
              'If f and ∂f/∂y are continuous near (x₀, y₀), then y′ = f(x, y), y(x₀) = y₀ has exactly one solution nearby. Solutions may still blow up in finite time.'],
 'eqs': [('\\frac{dy}{h(y)}=g(x)\\,dx', 'Separable equation'), ('\\mu=e^{\\int p\\,dx},\\quad(\\mu y)\'=\\mu q', 'Integrating factor'),
         ('M_y=N_x\\Rightarrow F(x,y)=C', 'Exact equation'), ('y\'=f(x,y),\\ y(x_0)=y_0', 'Initial value problem')],
 'worked': [
  {'q': 'Solve dy/dx = xy, y(0) = 2, and find y(1).', 'steps': ['dy/y = x dx, so ln|y| = x²/2 + C.', 'y = 2e^(x²/2).', 'y(1) = 2e^0.5.'], 'a': '≈ 3.297.'},
  {'q': 'Solve y′ + 2y = 4, y(0) = 0, and find y(1).', 'steps': ['μ = e^(2t), so (e^(2t)y)′ = 4e^(2t).', 'e^(2t)y = 2e^(2t) + C; y(0) = 0 gives C = −2.', 'y = 2(1 − e^(−2t)).'], 'a': 'y(1) ≈ 1.729, approaching the steady state 2.'},
  {'q': 'Solve 2xy dx + (x² + 2y) dy = 0 with y(0) = 1, and find y when x = 1.', 'steps': ['M_y = 2x = N_x: exact.', 'F = x²y + y²; F(0, 1) = 1.', 'At x = 1: y + y² = 1, so y = (−1 + √5)/2.'], 'a': '≈ 0.618.'}],
 'practice': [('Solve y′ = y², y(0) = 1. Where does the solution exist?', 'y = 1/(1 − t); it blows up at t = 1, even though y² is smooth everywhere.'),
              ('Solve t y′ + y = t² for t > 0.', '(ty)′ = t², so y = t²/3 + C/t.'), ('Solve y′ = −y/τ.', 'y = y₀e^(−t/τ).'),
              ('Is (y cos x) dx + (sin x + 2y) dy = 0 exact? Solve.', 'M_y = cos x = N_x; F = y sin x + y² = C.'),
              ('Does y′ = √y, y(0) = 0 have a unique solution?', 'No: y = 0 and y = t²/4 both work; ∂f/∂y = 1/(2√y) is not continuous at y = 0.')],
 'misc': [('Every first-order equation is separable.', 'y′ = x + y is not; it is linear.'), ('Forgetting +C until the end is fine.', 'Add C when you integrate, before solving for y, or the initial condition comes out wrong.'),
          ('A smooth right-hand side means the solution lives forever.', 'y′ = y² blows up at a finite time.')],
 'quiz': [{'q': 'The integrating factor for y′ + 3y = x is…', 'opts': ['e^(3x)', 'e^x', '3x', 'e^(−3x)'], 'ok': 0, 'why': 'e^(∫3 dx).'},
          {'q': 'M dx + N dy = 0 is exact when…', 'opts': ['M = N', 'M_y = N_x', 'M_x = N_y', 'MN = 1'], 'ok': 1, 'why': 'Mixed partials of F agree.'},
          {'q': 'y′ = ky has solution…', 'opts': ['y₀ + kt', 'y₀e^(kt)', 'kt²', 'sin kt'], 'ok': 1, 'why': 'Separable.'},
          {'q': 'Uniqueness can fail when…', 'opts': ['f is linear', '∂f/∂y is discontinuous', 'y₀ = 1', 'the equation is separable'], 'ok': 1, 'why': 'e.g. y′ = √y at 0.'}],
 'cards': [('Separable', 'dy/dx = g(x)h(y).'), ('Linear first-order', 'y′ + p y = q.'), ('Integrating factor', 'μ = e^(∫p dx).'), ('Exact', 'M_y = N_x; F = C.'),
           ('Initial value problem', 'An ODE plus y(x₀) = y₀.'), ('Existence and uniqueness', 'f, f_y continuous ⇒ one local solution.')],
 'planet': {'text': ['The simplest first-order equation, y′ = −y/τ, describes how a pollutant clears from a well-mixed lake or how a gas leaves the atmosphere. Its one number, the time scale τ, decides whether a mistake fades in years or lasts for centuries (Unit 2).'],
            'site': [('Rivers hub', 'Rivers.html')],
            'src': [_GL, ('Lebl, 1.4 Linear equations and the integrating factor', _L + 'intfactor_section.html')]},
 'res': [('Lebl, 1.3 Separable equations', _L + 'separable_section.html', 'Free textbook section.'), ('Lebl, 1.4 Integrating factor', _L + 'intfactor_section.html', 'Linear equations.'),
         ('Lebl, 1.8 Exact equations', _L + 'exact_section.html', 'Exact equations.'), ('Lebl, 1.2 Slope fields', _L + 'slopefields_section.html', 'Existence and uniqueness.')]})
UNITS.append(
{'id': 'u2', 'title': 'Modeling with First-Order Equations', 'weeks': 'Week 3',
 'summary': 'Turning a situation into an equation: mixing and lake pollution, decay and lifetimes, Newton cooling, logistic growth, harvesting, and equilibria with their stability.',
 'objectives': ['Build rate-in minus rate-out models.', 'Interpret time constants and lifetimes.', 'Find equilibria of autonomous equations and classify their stability.', 'Use the logistic model with harvesting to find maximum sustainable yield.'],
 'concepts': ['Rate of change = rate in − rate out. Write the units of every term.', 'A well-mixed lake with retention time τ loses a pollutant at rate C/τ once the inflow is clean.',
              'For an autonomous equation y′ = f(y), equilibria solve f(y) = 0; an equilibrium is stable if f′(y) < 0.', 'Logistic growth P′ = rP(1 − P/K) levels off at K. With constant harvest H, the largest sustainable harvest is rK/4, at P = K/2.'],
 'eqs': [('\\frac{dx}{dt}=(\\text{rate in})-(\\text{rate out})', 'Balance law'), ('C(t)=C_0e^{-t/\\tau}', 'Flushing with retention time τ'),
         ('P\'=rP\\left(1-\\frac PK\\right)-H', 'Logistic growth with harvest'), ('H_{\\max}=\\frac{rK}{4}', 'Maximum sustainable yield')],
 'worked': [
  {'q': 'Lake Erie’s retention time is 2.6 years and Lake Superior’s 191 years (EPA). If a pollutant’s inflow stops, how long until each lake’s concentration falls to 10%, treating each as well mixed?', 'steps': ['C/C₀ = e^(−t/τ) = 0.1, so t = τ ln 10.', 'Erie: 2.6 × 2.303 = 5.99 years.', 'Superior: 191 × 2.303 = 440 years.'], 'a': 'About 6 years for Erie but about 440 for Superior. Prevention matters most where flushing is slow.'},
  {'q': 'EPA says methane lasts about a decade in the atmosphere on average. Treat a methane pulse as decaying with τ = 10 years. What fraction is left after 30 years?', 'steps': ['Fraction = e^(−30/10) = e^(−3).'], 'a': 'About 5%. Cutting methane leaks therefore pays off within decades, unlike CO₂, which lingers far longer.'},
  {'q': 'A fish stock follows P′ = 0.4P(1 − P/10,000) − H (tonnes, years; sample values). Find the maximum sustainable yield.', 'steps': ['Growth rP(1 − P/K) is largest at P = K/2 = 5,000 t.', 'There it equals rK/4 = 0.4 × 10,000/4.'], 'a': '1,000 tonnes per year. Harvesting more than that drives the stock to collapse.'}],
 'practice': [('Coffee at 90 °C cools in a 20 °C room with T′ = −0.1(T − 20) (minutes). Find T(10).', 'T = 20 + 70e^(−1) ≈ 45.8 °C.'),
              ('A 100 L tank of fresh water gets brine of 0.5 g/L at 2 L/min and drains at 2 L/min. Find the salt after 50 minutes.', 'x′ = 1 − x/50, x = 50(1 − e^(−t/50)); x(50) = 50(1 − e^(−1)) ≈ 31.6 g.'),
              ('Find and classify the equilibria of y′ = y(1 − y).', 'y = 0 (f′ = 1, unstable) and y = 1 (f′ = −1, stable).'),
              ('In the fishery example, what happens if H = 1,200 t/yr?', 'rP(1 − P/K) − H < 0 for every P, so the stock declines to zero.')],
 'misc': [('Retention time is how long it takes to remove all the pollutant.', 'After one τ, 37% is still there; exponential decay never quite reaches zero.'),
          ('More fishing effort always means more catch.', 'Past the maximum sustainable yield, more harvest shrinks the stock and future catch.'),
          ('An equilibrium is always where the system ends up.', 'Only stable equilibria attract nearby solutions.')],
 'quiz': [{'q': 'With τ = 5 years, the fraction left after 5 years is…', 'opts': ['0', 'e^(−1) ≈ 0.37', '0.5', '0.1'], 'ok': 1, 'why': 'e^(−t/τ) at t = τ.'},
          {'q': 'Maximum sustainable yield of logistic growth is…', 'opts': ['rK', 'rK/4', 'K/2', 'r/K'], 'ok': 1, 'why': 'Peak of rP(1 − P/K).'},
          {'q': 'y* is a stable equilibrium of y′ = f(y) if…', 'opts': ['f′(y*) > 0', 'f′(y*) < 0', 'f(y*) > 0', 'y* > 0'], 'ok': 1, 'why': 'Nearby solutions are pushed back.'},
          {'q': 'Which lake recovers faster from pollution?', 'opts': ['Superior (191 yr)', 'Erie (2.6 yr)', 'Same', 'Neither'], 'ok': 1, 'why': 'Shorter retention time.'}],
 'cards': [('Balance law', 'Rate in − rate out.'), ('Time constant', 'τ in e^(−t/τ); 63% of the change is done after τ.'), ('Retention time', 'Lake volume ÷ outflow.'),
           ('Equilibrium', 'f(y*) = 0.'), ('Stability test', 'f′(y*) < 0 stable.'), ('Max sustainable yield', 'rK/4 at P = K/2.')],
 'planet': {'text': ['The EPA lists Great Lakes retention times from 2.6 years (Erie) to 191 years (Superior), which is why toxins entering Lake Superior are a multi-generation problem.',
                     'Fishery scientists at NOAA assess stocks with population models built on these ideas; the logistic model’s maximum sustainable yield is the classic starting point.'],
            'site': [('Oceans hub', 'Oceans.html'), ('Rivers hub', 'Rivers.html')],
            'src': [_GL, _GWP, _FISH]},
 'res': [('Lebl, 1.6 Autonomous equations', _L + 'auteq_section.html', 'Equilibria, logistic growth, harvesting.'), ('Lebl, 1.4 Integrating factor', _L + 'intfactor_section.html', 'Mixing problems.'),
         ('OpenStax Calculus 2, 4.4 The Logistic Equation', 'https://openstax.org/books/calculus-volume-2/pages/4-4-the-logistic-equation', 'Logistic model.')]})
UNITS.append(
{'id': 'u3', 'title': 'Second-Order Linear Equations and Oscillations', 'weeks': 'Weeks 4–5',
 'summary': 'Linear equations with constant coefficients, the characteristic equation, and free vibrations: undamped, underdamped, critically damped and overdamped.',
 'objectives': ['Solve ay″ + by′ + cy = 0 with the characteristic equation.', 'Handle real, repeated and complex roots.', 'Model mass-spring-damper systems.', 'Classify damping and compute natural frequency and critical damping.'],
 'concepts': ['Try y = e^(rt): ar² + br + c = 0. Two real roots give two exponentials; a repeated root gives (c₁ + c₂t)e^(rt); complex roots α ± iβ give e^(αt)(c₁ cos βt + c₂ sin βt).',
              'Superposition: sums of solutions of a homogeneous linear equation are solutions.', 'mx″ + cx′ + kx = 0 has natural frequency ω₀ = √(k/m).',
              'Damping c < 2√(mk) oscillates and decays (underdamped); c = 2√(mk) returns fastest without overshoot (critical).'],
 'eqs': [('ar^2+br+c=0', 'Characteristic equation'), ('y=e^{\\alpha t}(c_1\\cos\\beta t+c_2\\sin\\beta t)', 'Complex roots α ± iβ'),
         ('mx\'\'+cx\'+kx=0,\\ \\omega_0=\\sqrt{k/m}', 'Mass-spring-damper'), ('c_{\\text{crit}}=2\\sqrt{mk}', 'Critical damping')],
 'worked': [
  {'q': 'Solve y″ + 4y = 0, y(0) = 1, y′(0) = 0. What is the period?', 'steps': ['r² + 4 = 0, r = ±2i.', 'y = cos 2t.', 'Period 2π/2.'], 'a': 'y = cos 2t, period π ≈ 3.14.'},
  {'q': 'Solve y″ + 2y′ + 5y = 0, y(0) = 1, y′(0) = 0, and find y(1).', 'steps': ['r = −1 ± 2i.', 'y = e^(−t)(cos 2t + ½ sin 2t) fits both conditions.', 'y(1) = e^(−1)(cos 2 + ½ sin 2).'], 'a': '≈ 0.0142: the oscillation has nearly died out.'},
  {'q': 'A 2 kg mass hangs on a spring with k = 50 N/m. Find ω₀, the frequency in hertz, and the critical damping.', 'steps': ['ω₀ = √(50/2) = 5 rad/s.', 'f = 5/(2π) = 0.796 Hz.', 'c_crit = 2√(2 × 50) = 20 N·s/m.'], 'a': '5 rad/s, 0.80 Hz, 20 N·s/m.'}],
 'practice': [('Solve y″ − 3y′ + 2y = 0.', 'r = 1, 2: y = c₁eᵗ + c₂e^(2t).'), ('Solve y″ + 2y′ + y = 0.', 'Repeated r = −1: y = (c₁ + c₂t)e^(−t).'),
              ('Classify x″ + 6x′ + 5x = 0.', 'r = −1, −5: overdamped (c = 6 > 2√5).'), ('Find the period of x″ + 9x = 0.', 'ω = 3, period 2π/3 ≈ 2.09.')],
 'misc': [('Complex roots mean complex solutions.', 'Real and imaginary parts give real solutions: e^(αt)cos βt and e^(αt)sin βt.'), ('A repeated root gives only one solution.', 'The second is t e^(rt).'),
          ('More damping always means faster settling.', 'Overdamped systems creep back slower than critically damped ones.')],
 'quiz': [{'q': 'Roots 2 ± 3i give solutions…', 'opts': ['e^(2t), e^(3t)', 'e^(2t)cos 3t, e^(2t)sin 3t', 'cos 2t', 'te^(2t)'], 'ok': 1, 'why': 'α = 2, β = 3.'},
          {'q': 'Natural frequency of mx″ + kx = 0:', 'opts': ['k/m', '√(k/m)', 'm/k', '√(mk)'], 'ok': 1, 'why': 'r² = −k/m.'},
          {'q': 'Critical damping c equals…', 'opts': ['√(mk)', '2√(mk)', 'mk', 'k/m'], 'ok': 1, 'why': 'Discriminant zero.'},
          {'q': 'y″ + 2y′ + y = 0 is…', 'opts': ['underdamped', 'critically damped', 'overdamped', 'undamped'], 'ok': 1, 'why': 'Repeated root.'}],
 'cards': [('Characteristic equation', 'ar² + br + c = 0.'), ('Superposition', 'Sums of solutions are solutions (homogeneous linear).'), ('Repeated root', '(c₁ + c₂t)e^(rt).'),
           ('Natural frequency', 'ω₀ = √(k/m).'), ('Underdamped', 'Oscillates while decaying.'), ('Critical damping', 'c = 2√(mk).')],
 'planet': {'text': ['Every tall structure, from a wind-turbine tower to a bridge, has natural frequencies set by its stiffness and mass, exactly ω₀ = √(k/m) in the simplest model. Damping decides how fast gust-driven sway dies out, which affects fatigue and how long a structure lasts.'],
            'site': [('Physics I, Unit 8: oscillations', 'Physics_I.html#u8')],
            'src': [_WT, ('Lebl, 2.4 Mechanical vibrations', _L + 'sec_mv.html')]},
 'res': [('Lebl, 2.1 Second-order linear ODEs', _L + 'solinear_section.html', 'Theory.'), ('Lebl, 2.2 Constant coefficient equations', _L + 'sec_ccsol.html', 'Characteristic equation.'),
         ('Lebl, 2.4 Mechanical vibrations', _L + 'sec_mv.html', 'Damping.'), ('PhET: Masses and Springs', _PH + 'masses-and-springs', 'Simulation.')]})
UNITS.append(
{'id': 'u4', 'title': 'Forced Vibration and Resonance', 'weeks': 'Week 6',
 'summary': 'Nonhomogeneous equations, undetermined coefficients, the amplitude response of a driven oscillator, beats and resonance.',
 'objectives': ['Find particular solutions by undetermined coefficients.', 'Write the general solution as homogeneous plus particular.', 'Compute the steady-state amplitude of a driven damped oscillator.', 'Explain resonance and how engineers avoid it.'],
 'concepts': ['General solution = homogeneous solution + one particular solution.', 'Guess the form of the forcing: for cos ωt try A cos ωt + B sin ωt.',
              'Driven at frequency ω, a damped oscillator settles into steady motion with amplitude X = F₀/√((k − mω²)² + (cω)²).',
              'Near ω = ω₀ the amplitude peaks; with damping ratio ζ = c/c_crit, the peak dynamic amplification is about 1/(2ζ). With no damping, the response grows without bound.'],
 'eqs': [('y=y_h+y_p', 'General solution'), ('X=\\frac{F_0}{\\sqrt{(k-m\\omega^2)^2+(c\\omega)^2}}', 'Steady-state amplitude'),
         ('\\frac{X}{F_0/k}=\\frac1{\\sqrt{(1-r^2)^2+(2\\zeta r)^2}},\\ r=\\frac{\\omega}{\\omega_0}', 'Dynamic amplification'), ('y\'\'+\\omega^2y=\\cos\\omega t\\Rightarrow y_p=\\frac{t\\sin\\omega t}{2\\omega}', 'Pure resonance')],
 'worked': [
  {'q': 'Find a particular solution of y″ + y = cos 2t.', 'steps': ['Try y_p = A cos 2t: −4A + A = 1.', 'A = −1/3.'], 'a': 'y_p = −⅓ cos 2t (out of phase, since the drive is above the natural frequency).'},
  {'q': 'Model a wind-turbine tower as a single oscillator with natural frequency 0.30 Hz and damping ratio ζ = 0.01 (sample values). The rotor turns at 12 rpm = 0.20 Hz, and three blades pass the tower at 0.60 Hz. Find the dynamic amplification at each, and at resonance.', 'steps': ['At 0.20 Hz, r = 0.667: 1/√((1 − 0.444)² + (0.0133)²) = 1.80.', 'At 0.60 Hz, r = 2: 1/√(9 + 0.0016) = 0.333.', 'At r = 1: 1/(2ζ) = 50.'], 'a': '1.8 and 0.33, but 50 at resonance. That is why designers keep a tower’s natural frequency away from the rotor and blade-passing frequencies.'},
  {'q': 'Solve y″ + y = cos t, y(0) = y′(0) = 0.', 'steps': ['The forcing matches the natural frequency, so try y_p = t(A cos t + B sin t).', 'Substituting gives A = 0, B = ½.', 'y = ½ t sin t.'], 'a': 'The amplitude grows like t/2 without limit: pure resonance.'}],
 'practice': [('Find y_p for y″ + 3y′ + 2y = 4.', 'y_p = 2.'), ('Find y_p for y″ − y = eᵗ.', 'eᵗ solves the homogeneous equation, so y_p = ½ t eᵗ.'),
              ('A 1 kg mass, k = 100 N/m, c = 2 N·s/m is driven by 10 cos 10t N. Find the steady amplitude.', 'k − mω² = 0, so X = 10/(2 × 10) = 0.5 m.'),
              ('For ζ = 0.05, what is the peak amplification?', 'About 1/(2 × 0.05) = 10.')],
 'misc': [('Resonance needs a large force.', 'A small periodic force at the natural frequency builds up a large response.'), ('Damping removes resonance.', 'It caps the peak at about 1/(2ζ), which is still large for lightly damped structures.'),
          ('Undetermined coefficients works for any forcing.', 'Only for polynomials, exponentials, sines and cosines and their products; otherwise use variation of parameters or Laplace.')],
 'quiz': [{'q': 'General solution =', 'opts': ['y_p only', 'y_h + y_p', 'y_h × y_p', 'y_h − y_p'], 'ok': 1, 'why': 'Linearity.'},
          {'q': 'Resonance occurs when the driving frequency is near…', 'opts': ['zero', 'the natural frequency', 'twice it', 'infinity'], 'ok': 1, 'why': 'Denominator smallest.'},
          {'q': 'With ζ = 0.01 the peak amplification is about…', 'opts': ['1', '10', '50', '100'], 'ok': 2, 'why': '1/(2ζ).'},
          {'q': 'Driving well above ω₀ gives amplification…', 'opts': ['large', 'less than 1', 'exactly 1', 'infinite'], 'ok': 1, 'why': '≈ 1/r².'}],
 'cards': [('Particular solution', 'Any one solution of the forced equation.'), ('Undetermined coefficients', 'Guess the forcing’s form.'), ('Amplitude response', 'X = F₀/√((k − mω²)² + (cω)²).'),
           ('Damping ratio', 'ζ = c/(2√(mk)).'), ('Resonance', 'Large response near ω₀; peak ≈ 1/(2ζ).'), ('Beats', 'Two close frequencies make a slow envelope.')],
 'planet': {'text': ['Wind turbines turn ever larger and taller to harvest more energy, and their towers and blades are lightly damped. Avoiding resonance between the structure and the rotating rotor is a core part of keeping clean-energy machines safe and long-lived. Lab D explores it with a sample model.'],
            'site': [('Physics I, Unit 3: wind power', 'Physics_I.html#u3')],
            'src': [_WT, ('Lebl, 2.6 Forced oscillations and resonance', _L + 'forcedo_section.html')]},
 'res': [('Lebl, 2.5 Nonhomogeneous equations', _L + 'sec_nonhom.html', 'Undetermined coefficients and variation of parameters.'), ('Lebl, 2.6 Forced oscillations and resonance', _L + 'forcedo_section.html', 'Resonance.'),
         ('MIT OCW 18.03SC, Unit II', _MIT[1], 'Second-order equations, lectures and problems.')]})
UNITS.append(
{'id': 'u5', 'title': 'Laplace Transforms', 'weeks': 'Weeks 7–8',
 'summary': 'Transforming differential equations into algebra: the transform and its table, derivatives, step functions for switched inputs, impulses, and convolution.',
 'objectives': ['Compute Laplace transforms from the definition and a table.', 'Solve initial value problems with transforms and partial fractions.', 'Model switched inputs with unit step functions and shifts.', 'Model sudden impulses with the delta function.'],
 'concepts': ['L{f}(s) = ∫₀^∞ e^(−st) f(t) dt turns derivatives into multiplication by s, with initial values built in.', 'Solve for Y(s), split with partial fractions, then invert with the table.',
              'A switch flipped at time a is u(t − a); the shift rule is L{u(t − a)f(t − a)} = e^(−as)F(s).', 'An instant kick is δ(t − a), with L{δ(t − a)} = e^(−as).'],
 'eqs': [('\\mathcal L\\{f\\}=\\int_0^\\infty e^{-st}f(t)\\,dt', 'Definition'), ('\\mathcal L\\{y\'\\}=sY-y(0),\\ \\mathcal L\\{y\'\'\\}=s^2Y-sy(0)-y\'(0)', 'Derivatives'),
         ('\\mathcal L\\{e^{at}\\}=\\frac1{s-a},\\ \\mathcal L\\{\\sin\\omega t\\}=\\frac{\\omega}{s^2+\\omega^2}', 'Table entries'), ('\\mathcal L\\{u(t-a)f(t-a)\\}=e^{-as}F(s)', 'Shift rule')],
 'worked': [
  {'q': 'Solve y′ − 2y = e^(3t), y(0) = 1.', 'steps': ['sY − 1 − 2Y = 1/(s − 3).', 'Y = 1/((s − 2)(s − 3)) + 1/(s − 2) = [1/(s − 3) − 1/(s − 2)] + 1/(s − 2).', 'Y = 1/(s − 3).'], 'a': 'y = e^(3t). Check: 3e^(3t) − 2e^(3t) = e^(3t).'},
  {'q': 'A clean lake starts receiving a steady pollutant inflow at t = 2: y′ + y = u(t − 2), y(0) = 0. Find y(3).', 'steps': ['(s + 1)Y = e^(−2s)/s.', '1/(s(s + 1)) = 1/s − 1/(s + 1), so y = (1 − e^(−(t − 2)))u(t − 2).', 'y(3) = 1 − e^(−1).'], 'a': '≈ 0.632 of the final level, one time constant after the switch.'},
  {'q': 'A resting oscillator y″ + 4y = δ(t − 1) gets a kick at t = 1. Find y(1 + π/4).', 'steps': ['(s² + 4)Y = e^(−s).', 'y = ½ sin(2(t − 1)) u(t − 1).', 'At t = 1 + π/4: ½ sin(π/2).'], 'a': '0.5, the first peak.'}],
 'practice': [('Find L{t}.', '1/s².'), ('Invert 3/(s² + 9).', 'sin 3t.'), ('Solve y′ + y = 0, y(0) = 4.', 'Y = 4/(s + 1), y = 4e^(−t).'),
              ('Solve y″ + y = 0, y(0) = 0, y′(0) = 2.', 'Y = 2/(s² + 1), y = 2 sin t.'), ('Find L{u(t − 3)}.', 'e^(−3s)/s.')],
 'misc': [('L{fg} = L{f}L{g}.', 'The product of transforms corresponds to convolution, not the product.'), ('Initial conditions are applied at the end.', 'They enter immediately through L{y′} = sY − y(0).'),
          ('Step functions need piecewise solving.', 'Laplace handles switches in one pass.')],
 'quiz': [{'q': 'L{y′} =', 'opts': ['sY', 'sY − y(0)', 'Y/s', 'Y − s'], 'ok': 1, 'why': 'Integration by parts.'},
          {'q': 'L{e^(−2t)} =', 'opts': ['1/(s − 2)', '1/(s + 2)', 's + 2', '−2/s'], 'ok': 1, 'why': 'a = −2.'},
          {'q': 'A switch turned on at t = 5 is written…', 'opts': ['δ(t − 5)', 'u(t − 5)', 'e^(5t)', 't − 5'], 'ok': 1, 'why': 'Unit step.'},
          {'q': 'L{δ(t)} =', 'opts': ['0', '1', 's', '1/s'], 'ok': 1, 'why': 'e^(−0s).'}],
 'cards': [('Laplace transform', '∫₀^∞ e^(−st) f dt.'), ('L{y′}', 'sY − y(0).'), ('L{eᵃᵗ}', '1/(s − a).'), ('Unit step', 'u(t − a): off then on.'), ('Delta', 'δ(t − a): instant impulse; L = e^(−as).'), ('Convolution', 'L{f * g} = FG.')],
 'planet': {'text': ['Real environmental inputs switch on and off: a factory discharge starts, a dam release stops, a volcanic eruption injects aerosols in a single burst. Step and impulse inputs with Laplace transforms give the response to each in one calculation, the method engineers use for control systems in power grids and treatment plants.'],
            'site': [('Rivers hub', 'Rivers.html')],
            'src': [('Lebl, 6.1 The Laplace transform', _L + 'laplace_section.html'), ('Lebl, 6.4 Dirac delta and impulse response', _L + 'diracdelta_section.html')]},
 'res': [('Lebl, 6.1 The Laplace transform', _L + 'laplace_section.html', 'Definition and table.'), ('Lebl, 6.2 Transforms of derivatives and ODEs', _L + 'transformsofders_section.html', 'Solving IVPs.'),
         ('Lebl, 6.3 Convolution', _L + 'convolution_section.html', 'Convolution.'), ('Lebl, 6.4 Dirac delta', _L + 'diracdelta_section.html', 'Impulses.')]})
UNITS.append(
{'id': 'u6', 'title': 'Linear Systems, Eigenvalues and Phase Planes', 'weeks': 'Weeks 9–10',
 'summary': 'Systems x′ = Ax, eigenvalue methods, the phase plane, and the classification of equilibria as nodes, saddles, spirals and centers.',
 'objectives': ['Write coupled equations and higher-order equations as first-order systems.', 'Solve x′ = Ax with eigenvalues and eigenvectors.', 'Sketch phase portraits.', 'Classify the origin with the trace and determinant.'],
 'concepts': ['If Av = λv, then x = e^(λt)v solves x′ = Ax; the general solution combines one such term per eigenvalue.', 'Real eigenvalues of opposite sign: a saddle. Both negative: a stable node.',
              'Complex eigenvalues α ± iβ: spirals (stable if α < 0); centers if α = 0.', 'For a 2 × 2 matrix, λ² − (tr A)λ + det A = 0.'],
 'eqs': [('\\mathbf x\'=A\\mathbf x', 'Linear system'), ('\\det(A-\\lambda I)=0', 'Eigenvalues'), ('\\mathbf x=c_1e^{\\lambda_1t}\\mathbf v_1+c_2e^{\\lambda_2t}\\mathbf v_2', 'General solution (distinct real eigenvalues)'),
         ('\\lambda^2-(\\operatorname{tr}A)\\lambda+\\det A=0', 'Characteristic polynomial (2 × 2)')],
 'worked': [
  {'q': 'A two-box carbon model: atmosphere A and ocean O exchange carbon with A′ = −0.2A + 0.1O, O′ = 0.2A − 0.1O (per year; sample rates). Start with 3 units in the air and none in the ocean.', 'steps': ['Eigenvalues: tr = −0.3, det = 0, so λ = 0 and −0.3.', 'λ = 0 has eigenvector (1, 2): the equilibrium split is 1 : 2. Total carbon (3) is conserved, so A → 1, O → 2.', 'A(t) = 1 + 2e^(−0.3t).'], 'a': 'The air keeps one third of the pulse in this toy model, with time scale 1/0.3 ≈ 3.33 years.'},
  {'q': 'Classify the origin for A = [[1, 2], [2, 1]].', 'steps': ['λ² − 2λ − 3 = 0, λ = 3, −1.'], 'a': 'Opposite signs: a saddle (unstable).'},
  {'q': 'Classify the origin for A = [[−1, −2], [2, −1]].', 'steps': ['tr = −2, det = 5: λ² + 2λ + 5 = 0.', 'λ = −1 ± 2i.'], 'a': 'A stable spiral: solutions circle inward, decaying like e^(−t).'}],
 'practice': [('Write y″ + 3y′ + 2y = 0 as a system.', 'x₁ = y, x₂ = y′: x₁′ = x₂, x₂′ = −2x₁ − 3x₂.'), ('Eigenvalues of [[2, 0], [0, −3]]?', '2 and −3: a saddle.'),
              ('Classify [[0, 1], [−4, 0]].', 'λ = ±2i: a center (undamped oscillation).'), ('Classify [[−3, 1], [0, −2]].', 'λ = −3, −2: a stable node.')],
 'misc': [('Eigenvectors are unique.', 'Any nonzero multiple works.'), ('A zero eigenvalue means no motion.', 'It means a line of equilibria or a conserved quantity, as in the carbon box model.'),
          ('Complex eigenvalues give complex solutions only.', 'Real and imaginary parts give real solutions.')],
 'quiz': [{'q': 'Eigenvalues 2 and −1 give…', 'opts': ['a node', 'a saddle', 'a spiral', 'a center'], 'ok': 1, 'why': 'Opposite signs.'},
          {'q': 'Eigenvalues −1 ± 3i give…', 'opts': ['unstable spiral', 'stable spiral', 'center', 'saddle'], 'ok': 1, 'why': 'α < 0.'},
          {'q': 'For 2 × 2 A, the eigenvalues’ sum is…', 'opts': ['det A', 'tr A', '0', '1'], 'ok': 1, 'why': 'λ₁ + λ₂ = tr A.'},
          {'q': 'A center has eigenvalues…', 'opts': ['real, equal', 'purely imaginary', 'zero', 'positive'], 'ok': 1, 'why': 'α = 0.'}],
 'cards': [('Linear system', 'x′ = Ax.'), ('Eigenvalue method', 'x = e^(λt)v.'), ('Saddle', 'Real eigenvalues of opposite sign.'), ('Node', 'Real eigenvalues of the same sign.'),
           ('Spiral', 'Complex eigenvalues, α ≠ 0.'), ('Trace–determinant', 'λ² − tr λ + det = 0.')],
 'planet': {'text': ['Carbon-cycle models are linear systems of boxes (atmosphere, surface ocean, deep ocean, land) exchanging carbon. Their eigenvalues are the time scales on which a CO₂ pulse is absorbed: some fast, some taking centuries or longer. NASA’s carbon-cycle overview describes the fast and slow cycles these boxes represent.'],
            'site': [('Oceans hub', 'Oceans.html')],
            'src': [_CC, _CO2]},
 'res': [('Lebl, 3.1 Introduction to systems', _L + 'sec_introtosys.html', 'Systems.'), ('Lebl, 3.4 Eigenvalue method', _L + 'eigenmethod_section.html', 'Eigenvalues.'),
         ('Lebl, 3.5 Two-dimensional systems and their vector fields', _L + 'sec_twodimaut.html', 'Phase portraits.')]})
UNITS.append(
{'id': 'u7', 'title': 'Nonlinear Systems and Stability', 'weeks': 'Weeks 11–12',
 'summary': 'Equilibria of nonlinear systems, linearization with the Jacobian, predator-prey cycles, and the SIR epidemic model.',
 'objectives': ['Find equilibria of nonlinear systems.', 'Linearize with the Jacobian and classify equilibria.', 'Analyze the Lotka–Volterra predator-prey model.', 'Use the SIR model: R₀, herd-immunity threshold and final size.'],
 'concepts': ['Near an equilibrium, a nonlinear system behaves like its linearization x′ = J x, where J is the Jacobian (unless the linearization is a center).',
              'Lotka–Volterra: prey x′ = ax − bxy, predators y′ = −cy + dxy. The equilibrium is (c/d, a/b); populations cycle around it.',
              'SIR: S′ = −βSI, I′ = βSI − γI, R′ = γI. The basic reproduction number R₀ = β/γ; an outbreak grows only if R₀S > 1.',
              'The herd-immunity threshold is 1 − 1/R₀; the final uninfected share s∞ solves ln s∞ = R₀(s∞ − 1).'],
 'eqs': [('J=\\begin{pmatrix}f_x&f_y\\\\g_x&g_y\\end{pmatrix}', 'Jacobian'), ('x\'=ax-bxy,\\ y\'=-cy+dxy', 'Lotka–Volterra'),
         ('S\'=-\\beta SI,\\ I\'=\\beta SI-\\gamma I,\\ R\'=\\gamma I', 'SIR model'), ('R_0=\\beta/\\gamma,\\ \\ln s_\\infty=R_0(s_\\infty-1)', 'Reproduction number and final size')],
 'worked': [
  {'q': 'Prey and predators follow x′ = x − 0.02xy, y′ = −0.5y + 0.005xy (sample values, years). Find the coexistence equilibrium and the period of small cycles.', 'steps': ['x′ = 0 needs y = 1/0.02 = 50; y′ = 0 needs x = 0.5/0.005 = 100.', 'The Jacobian there has eigenvalues ±i√(ac) = ±i√0.5.', 'Period 2π/√0.5.'], 'a': '100 prey and 50 predators; small cycles last about 8.9 years, with predators lagging prey.'},
  {'q': 'An epidemic has β = 0.3 per day and γ = 0.1 per day. Find R₀, the herd-immunity threshold, and the final share ever infected.', 'steps': ['R₀ = 3.', 'Threshold 1 − 1/3 = 0.667.', 'Iterate s = e^(3(s − 1)): s∞ = 0.0595.'], 'a': 'R₀ = 3; immunity in 67% stops growth; with no intervention about 94% are eventually infected, more than the threshold because the epidemic overshoots.'},
  {'q': 'Classify the equilibrium P = K of logistic growth P′ = rP(1 − P/K).', 'steps': ['f′(P) = r − 2rP/K; f′(K) = −r < 0.'], 'a': 'Stable: small disturbances decay at rate r.'}],
 'practice': [('Find the equilibria of x′ = x(3 − x − y), y′ = y(2 − x − y).', '(0, 0), (3, 0), (0, 2) (no interior one: the lines x + y = 3 and x + y = 2 are parallel).'),
              ('Linearize x′ = sin x near x = 0 and x = π.', 'f′(0) = 1 (unstable), f′(π) = −1 (stable).'), ('If R₀ = 2, what is the herd-immunity threshold?', '1 − 1/2 = 50%.'),
              ('In the predator-prey example, what happens to the prey if predators are removed?', 'x′ = x: exponential growth (until other limits apply).')],
 'misc': [('Linearization always predicts the behavior.', 'Not when it gives a center; the nonlinear terms decide.'), ('Herd immunity means the epidemic stops at once.', 'Infections decline after the threshold but can still overshoot.'),
          ('Predator-prey cycles mean the model is unstable.', 'Lotka–Volterra orbits are closed: neutrally stable, neither growing nor shrinking.')],
 'quiz': [{'q': 'R₀ = β/γ = 4 gives a threshold of…', 'opts': ['25%', '50%', '75%', '100%'], 'ok': 2, 'why': '1 − 1/4.'},
          {'q': 'Lotka–Volterra equilibrium prey level is…', 'opts': ['a/b', 'c/d', 'b/a', 'd/c'], 'ok': 1, 'why': 'y′ = 0 needs x = c/d.'},
          {'q': 'Linearization uses…', 'opts': ['the Hessian', 'the Jacobian', 'the Laplacian', 'the trace'], 'ok': 1, 'why': 'First partial derivatives.'},
          {'q': 'An epidemic grows initially if…', 'opts': ['R₀S > 1', 'R₀ < 1', 'γ > β', 'I = 0'], 'ok': 0, 'why': 'I′ = (βS − γ)I.'}],
 'cards': [('Jacobian', 'Matrix of first partials.'), ('Linearization', 'x′ ≈ J x near an equilibrium.'), ('Lotka–Volterra', 'Predator-prey cycles around (c/d, a/b).'),
           ('SIR', 'Susceptible, infected, recovered.'), ('R₀', 'β/γ, new infections per case.'), ('Herd-immunity threshold', '1 − 1/R₀.')],
 'planet': {'text': ['On Isle Royale in Lake Superior, the National Park Service charts wolf and moose numbers back to 1980, a long predator-prey record. Their linked ups and downs, and the Park Service’s decision to relocate new wolves to the island, are exactly the kind of system Lotka–Volterra models begin to explain.',
                     'The same SIR mathematics that guides public-health response is used for wildlife diseases that threaten ecosystems.'],
            'site': [('Oceans hub', 'Oceans.html')],
            'src': [_ISR, _ISW]},
 'res': [('Lebl, 8.1 Linearization, critical points and equilibria', _L + 'linearization_section.html', 'Linearization.'), ('Lebl, 8.2 Stability and classification', _L + 'nlinstability_section.html', 'Stability.'),
         ('Lebl, 8.3 Applications of nonlinear systems', _L + 'nlinapps_section.html', 'Predator-prey and more.')]})
UNITS.append(
{'id': 'u8', 'title': 'Numerical Methods', 'weeks': 'Week 13',
 'summary': 'Euler, improved Euler and Runge–Kutta methods, step size and error, and a climate energy-balance model solved numerically.',
 'objectives': ['Apply Euler, improved Euler (Heun) and RK4.', 'Explain the order of a method and how error scales with step size.', 'Solve systems numerically.', 'Build and solve a zero-dimensional energy-balance climate model.'],
 'concepts': ['Euler steps along the slope: y_{n+1} = y_n + h f(t_n, y_n). Its global error is proportional to h.', 'Improved Euler averages two slopes (error ∝ h²); RK4 averages four (error ∝ h⁴).',
              'Halving h cuts RK4 error about 16 times, which is why it is the workhorse.', 'Energy balance: C dT/dt = absorbed sunlight − εσT⁴. Its equilibrium and time scale come from the equation directly.'],
 'eqs': [('y_{n+1}=y_n+hf(t_n,y_n)', 'Euler’s method'), ('y_{n+1}=y_n+\\tfrac h6(k_1+2k_2+2k_3+k_4)', 'Runge–Kutta 4'),
         ('C\\frac{dT}{dt}=S(1-\\alpha)-\\varepsilon\\sigma T^4', 'Energy-balance model'), ('\\lambda=4\\varepsilon\\sigma T^3,\\ \\tau=C/\\lambda', 'Linearized feedback and time scale')],
 'worked': [
  {'q': 'Approximate y(1) for y′ = y, y(0) = 1 with h = 0.1 using Euler, improved Euler and RK4.', 'steps': ['Each Euler step multiplies by 1.1: 1.1¹⁰ = 2.5937.', 'Improved Euler multiplies by 1.105: 2.7141.', 'RK4 multiplies by 1.1051708: 2.7182797.'], 'a': 'True e = 2.7182818. Errors: 0.12, 0.0042 and 0.000002.'},
  {'q': 'Earth absorbs 340 × (1 − 0.29) = 241.4 W/m² of sunlight (NASA). If it radiated as a blackbody (ε = 1), what temperature would balance it? What effective ε gives today’s average of about 288 K?', 'steps': ['σT⁴ = 241.4 gives T = (241.4/5.67 × 10⁻⁸)^(1/4) = 255 K.', 'ε = 241.4/(σ × 288⁴) = 0.619.'], 'a': '255 K (−18 °C) without a greenhouse effect; an effective emissivity of 0.62 represents the greenhouse effect that keeps Earth habitable.'},
  {'q': 'With ε = 0.619 at 288 K and an ocean mixed layer 50 m deep (C = 1,000 × 4,186 × 50 J/(m²·K); sample depth), find λ, the time scale, and the no-feedback warming for a 4 W/m² forcing (sample value).', 'steps': ['λ = 4εσT³ = 3.35 W/(m²·K).', 'τ = C/λ = 6.24 × 10⁷ s ≈ 1.98 years (about 2).', 'ΔT = 4/3.35.'], 'a': 'About 1.2 K of warming, approached on a 2-year time scale in this simple model. Real feedbacks (water vapor, ice) make the warming larger, as the IPCC assesses.'}],
 'practice': [('One Euler step for y′ = t + y, y(0) = 1, h = 0.1.', 'y₁ = 1 + 0.1(0 + 1) = 1.1.'), ('If Euler’s error is 0.12 at h = 0.1, estimate it at h = 0.05.', 'About 0.06 (first order).'),
              ('If RK4’s error is 2 × 10⁻⁶ at h = 0.1, estimate it at h = 0.05.', 'About 2 × 10⁻⁶/16 ≈ 1.3 × 10⁻⁷.'), ('What equilibrium temperature does the EBM give with ε = 1 and albedo 0.29?', 'About 255 K.')],
 'misc': [('Smaller steps are always better.', 'Round-off and cost grow; a higher-order method is usually better than tiny Euler steps.'), ('A numerical answer is exact if the code runs.', 'Always check convergence by halving h.'),
          ('The 255 K result means the model is wrong.', 'It shows how much the greenhouse effect warms Earth: about 33 K.')],
 'quiz': [{'q': 'Euler’s method has global error proportional to…', 'opts': ['h', 'h²', 'h⁴', '1/h'], 'ok': 0, 'why': 'First order.'},
          {'q': 'RK4 is order…', 'opts': ['1', '2', '4', '8'], 'ok': 2, 'why': 'Error ∝ h⁴.'},
          {'q': 'Earth without a greenhouse effect would average about…', 'opts': ['288 K', '255 K', '273 K', '300 K'], 'ok': 1, 'why': 'σT⁴ = 241 W/m².'},
          {'q': 'Halving h in RK4 cuts error by about…', 'opts': ['2', '4', '16', '32'], 'ok': 2, 'why': '2⁴.'}],
 'cards': [('Euler’s method', 'y + h f.'), ('Improved Euler', 'Average of two slopes; order 2.'), ('RK4', 'Four slopes; order 4.'), ('Step size', 'h; check convergence by halving.'),
           ('Energy-balance model', 'C T′ = S(1 − α) − εσT⁴.'), ('Climate time scale', 'τ = C/λ.')],
 'planet': {'text': ['Every climate model, from this one-line energy balance to the global models assessed by the IPCC, is a system of differential equations solved numerically. NASA’s energy budget gives the inputs: 340 W/m² of sunlight arrives on average and 29% is reflected.'],
            'site': [('Intro to Programming, simulation unit', 'Intro_to_Programming.html')],
            'src': [_EB, _IPCC]},
 'res': [('Lebl, 1.7 Numerical methods: Euler’s method', _L + 'numer_section.html', 'Euler and error.'), ('Trench, Ch. 3: Numerical methods', _TR[1], 'Improved Euler and RK4.')]})
UNITS.append(
{'id': 'u9', 'title': 'Series Solutions, Fourier Series and the Heat Equation', 'weeks': 'Week 14',
 'summary': 'Power-series solutions of ODEs, Fourier series of periodic functions, and separation of variables for the heat equation.',
 'objectives': ['Find power-series solutions from a recurrence.', 'Compute Fourier coefficients of simple periodic functions.', 'Solve the heat equation on a rod by separation of variables.', 'Estimate how deep seasonal temperature waves reach into the ground.'],
 'concepts': ['Substitute y = Σaₙxⁿ, match powers, and get a recurrence for the coefficients.', 'A periodic function is a sum of sines and cosines; for an odd function on (−π, π), bₙ = (2/π)∫₀^π f sin nx dx.',
              'The heat equation u_t = α u_xx spreads heat; each sine mode decays like e^(−α(nπ/L)²t), fast modes first.', 'A periodic surface temperature penetrates the ground with damping depth d = √(2α/ω).'],
 'eqs': [('y=\\sum a_nx^n', 'Power-series solution'), ('b_n=\\frac2\\pi\\int_0^\\pi f(x)\\sin nx\\,dx', 'Fourier sine coefficient'),
         ('u_t=\\alpha u_{xx}', 'Heat equation'), ('d=\\sqrt{2\\alpha/\\omega}', 'Damping depth of a periodic temperature wave')],
 'worked': [
  {'q': 'Solve y″ + y = 0 by power series.', 'steps': ['Σ(n + 2)(n + 1)aₙ₊₂xⁿ + Σaₙxⁿ = 0.', 'aₙ₊₂ = −aₙ/((n + 2)(n + 1)).', 'Even terms build cos x, odd terms sin x.'], 'a': 'y = a₀ cos x + a₁ sin x, recovered from the recurrence.'},
  {'q': 'Find the Fourier series of the square wave f = 1 on (0, π), −1 on (−π, 0).', 'steps': ['Odd, so only sines: bₙ = (2/π)∫₀^π sin nx dx = (2/(nπ))(1 − cos nπ).', 'bₙ = 4/(nπ) for odd n, 0 for even n.'], 'a': 'f = (4/π)(sin x + sin 3x/3 + sin 5x/5 + …); b₁ ≈ 1.273.'},
  {'q': 'Soil with diffusivity α = 5 × 10⁻⁷ m²/s (sample value) feels a yearly surface temperature cycle. Find the damping depth.', 'steps': ['ω = 2π/(3.156 × 10⁷ s) = 1.99 × 10⁻⁷ s⁻¹.', 'd = √(2 × 5 × 10⁻⁷/1.99 × 10⁻⁷).'], 'a': 'About 2.24 m: the yearly swing shrinks by a factor e for each 2.2 m of depth, so deeper ground responds to warming slowly, over many years.'}],
 'practice': [('Find the recurrence for y′ = y by power series.', 'aₙ₊₁ = aₙ/(n + 1), so y = a₀eˣ.'), ('Is f(x) = x² odd or even? Which Fourier terms appear?', 'Even: cosines only (plus a constant).'),
              ('A rod mode decays like e^(−α(π/L)²t). How does doubling L change its decay time?', 'It multiplies the decay time by 4.'), ('Find b₃ for the square wave.', '4/(3π) ≈ 0.424.')],
 'misc': [('Fourier series only work for smooth functions.', 'They work for jumps too, converging to the midpoint at a jump.'), ('Heat diffuses at a fixed speed.', 'Diffusion time grows with distance squared.'),
          ('Series solutions are always better than formulas.', 'They are most useful when no closed form exists, as for Airy or Bessel equations.')],
 'quiz': [{'q': 'In the heat equation, higher modes decay…', 'opts': ['slower', 'faster', 'not at all', 'linearly'], 'ok': 1, 'why': 'Rate ∝ n².'},
          {'q': 'An odd function’s Fourier series has only…', 'opts': ['cosines', 'sines', 'constants', 'exponentials'], 'ok': 1, 'why': 'Odd × even integrals vanish.'},
          {'q': 'Doubling the period of a surface temperature cycle changes the damping depth by…', 'opts': ['2', '√2', '1/2', '4'], 'ok': 1, 'why': 'd ∝ 1/√ω.'},
          {'q': 'b₁ for the square wave is…', 'opts': ['1', '4/π', '2/π', 'π/4'], 'ok': 1, 'why': '4/(1·π).'}],
 'cards': [('Power-series method', 'Substitute Σaₙxⁿ; get a recurrence.'), ('Fourier series', 'Sum of sines and cosines.'), ('Fourier coefficient', 'bₙ = (2/π)∫₀^π f sin nx dx.'),
           ('Heat equation', 'u_t = α u_xx.'), ('Separation of variables', 'u = X(x)T(t).'), ('Damping depth', '√(2α/ω).')],
 'planet': {'text': ['Permafrost in the Northern Hemisphere holds about 1,672 billion tons of organic carbon, according to NASA. How fast surface warming reaches it is a heat-equation problem, and the damping depth shows why deeper layers respond slowly but keep responding long after the surface warms.'],
            'site': [('Calculus III', 'Calculus_III.html')],
            'src': [_CC, ('Lebl, 4.6 PDEs, separation of variables, and the heat equation', _L + 'heateq_section.html')]},
 'res': [('Lebl, 7.1 Power series', _L + 'powerseries_section.html', 'Power series.'), ('Lebl, 7.2 Series solutions of linear second-order ODEs', _L + 'seriessols_section.html', 'Series solutions.'),
         ('Lebl, 4.2 Trigonometric series', _L + 'ts_section.html', 'Fourier series.'), ('Lebl, 4.6 The heat equation', _L + 'heateq_section.html', 'Heat equation.')]})
LABS = [
{'id': 'labA', 'title': 'Lab A: An SIR epidemic with Euler and RK4', 'week': 'Week 12',
 'goal': 'Solve the SIR model numerically, find the peak, and compare Euler with RK4 against the exact final size.',
 'eq': ('S\'=-0.3SI,\\ I\'=0.3SI-0.1I,\\ R\'=0.1I', 'SIR with R₀ = 3 (sample rates per day)'),
 'steps': ['Start with S = 0.999, I = 0.001, R = 0 (fractions of the population).', 'Run Euler with h = 1 day and h = 0.1 day to day 160, then RK4 with h = 1 day.', 'Record the final R and the peak of I and when it occurs; compare with theory.'],
 'table': (['Method', 'Final R (day 160)'], [['Euler, h = 1', '0.9467'], ['Euler, h = 0.1', '0.9411'], ['RK4, h = 1', '0.9405'], ['Exact final size (theory)', '0.9405']]),
 'note': 'Computed values for sample rates; not a real outbreak.',
 'calc': ['The peak is 30.1% infected at once, near day 38.4; theory gives I_max = 1 − (1 + ln R₀)/R₀ = 0.300.', 'Euler with h = 1 overstates the final size by 0.006; RK4 with the same step matches theory to 4 digits.'],
 'safety': ['None beyond normal computer use.'], 'home': ['A spreadsheet works; Python is easier for RK4.'],
 'sims': [('Lebl, 8.3 Applications of nonlinear systems', _L + 'nlinapps_section.html')],
 'planet': 'The same model structure is used for disease outbreaks in people and in wildlife.', 'planet_src': []},
{'id': 'labB', 'title': 'Lab B: The predator-prey phase plane', 'week': 'Week 11',
 'goal': 'Integrate the Lotka–Volterra model with RK4 and plot the closed orbit in the phase plane.',
 'eq': ('x\'=x-0.02xy,\\quad y\'=-0.5y+0.005xy', 'Lotka–Volterra (sample values)'),
 'steps': ['Start at 150 prey and 50 predators.', 'Use RK4 with a small step (0.001 years in Python, or 0.01 in a spreadsheet) for 40 years.', 'Plot y against x and record the prey range and the period.'],
 'table': (['Quantity', 'Value'], [['Equilibrium', '(100, 50)'], ['Prey range', '62.6 to 150'], ['Period', '8.99 years'], ['Small-cycle period (linear theory)', '8.89 years']]),
 'note': 'Computed values; sample parameters.',
 'calc': ['The orbit closes: the populations repeat every 8.99 years, slightly longer than the 8.89 years linear theory predicts for small cycles, because this cycle is large.', 'Predators peak after prey, a lag seen in many real predator-prey records.'],
 'safety': ['None beyond normal computer use.'], 'home': ['Desmos can draw the phase plane slope field.'],
 'sims': [_ISW],
 'planet': 'Long-term records such as Isle Royale’s wolves and moose test these models.', 'planet_src': [_ISR]},
{'id': 'labC', 'title': 'Lab C: A climate energy-balance model', 'week': 'Week 13',
 'goal': 'Step a one-box climate model through time after a sudden forcing and find its time scale.',
 'eq': ('C\\frac{d\\Delta T}{dt}=F-\\lambda\\,\\Delta T', 'Linearized energy-balance model'),
 'steps': ['Use C = 2.09 × 10⁸ J/(m²·K) (50 m of ocean), λ = 3.35 W/(m²·K) from Unit 8, and a sudden forcing F = 4 W/m² (sample value).', 'Step with Euler using monthly steps for 10 years.', 'Compare with the exact solution ΔT = (F/λ)(1 − e^(−t/τ)).'],
 'table': (['Year', 'ΔT (K)'], [['1', '0.48'], ['2', '0.77'], ['5', '1.10'], ['10', '1.19']]),
 'note': 'Computed model values; no feedbacks other than radiation.',
 'calc': ['Equilibrium ΔT = F/λ = 1.19 K; τ = C/λ ≈ 2.0 years, so the warming is about 63% done after 2 years in this model.', 'Real climate responds more slowly and warms more, because heat mixes into the deep ocean and feedbacks amplify it.'],
 'safety': ['None beyond normal computer use.'], 'home': ['A spreadsheet is enough.'],
 'sims': [_EB],
 'planet': 'Energy-balance models are the first step toward the climate projections assessed by the IPCC.', 'planet_src': [_IPCC]},
{'id': 'labD', 'title': 'Lab D: Resonance sweep of a wind-turbine tower model', 'week': 'Week 6',
 'goal': 'Compute the dynamic amplification of a single-oscillator tower model across driving frequencies.',
 'eq': ('A(f)=\\frac1{\\sqrt{(1-r^2)^2+(2\\zeta r)^2}},\\ r=f/f_0', 'Dynamic amplification'),
 'steps': ['Use f₀ = 0.30 Hz and ζ = 0.01 (sample values).', 'Tabulate A for driving frequencies from 0.1 to 0.6 Hz.', 'Mark the rotor frequency (0.20 Hz at 12 rpm) and the blade-passing frequency (0.60 Hz) and judge the design.'],
 'table': (['Driving frequency (Hz)', 'Amplification'], [['0.10', '1.12'], ['0.20', '1.80'], ['0.25', '3.27'], ['0.30', '50.0'], ['0.35', '2.76'], ['0.60', '0.333']]),
 'note': 'Computed values for a sample model, not a specific turbine.',
 'calc': ['Both operating frequencies sit well away from the 0.30 Hz peak, where the response would be 50 times the static deflection.', 'If the rotor sped up to 18 rpm (0.30 Hz), it would drive the tower at resonance; this is why designers check the natural frequency against the whole speed range.'],
 'safety': ['None beyond normal computer use.'], 'home': ['A spreadsheet is enough.'],
 'sims': [('PhET: Masses and Springs', _PH + 'masses-and-springs')],
 'planet': 'Avoiding resonance keeps wind turbines generating clean power safely for decades.', 'planet_src': [_WT]},
]
SCHEDULE = [(1, 'u1', 'Slope fields; separable equations', 'Lebl 1.1–1.3'), (2, 'u1', 'Linear and exact equations; existence and uniqueness', 'Lebl 1.2, 1.4, 1.8'),
            (3, 'u2', 'Modeling: mixing, decay, logistic growth, harvesting', 'Lebl 1.6'), (4, 'u3', 'Second-order linear equations; characteristic equation', 'Lebl 2.1–2.2'),
            (5, 'u3', 'Mechanical vibrations and damping', 'Lebl 2.4'), (6, 'u4', 'Undetermined coefficients; forced oscillation and resonance; Lab D', 'Lebl 2.5–2.6'),
            (7, 'u5', 'Laplace transforms; solving IVPs', 'Lebl 6.1–6.2'), (8, 'u5', 'Step functions, impulses, convolution; midterm practice', 'Lebl 6.3–6.4'),
            (9, 'u6', 'Systems; matrices and eigenvalues', 'Lebl 3.1–3.4'), (10, 'u6', 'Phase portraits and classification', 'Lebl 3.5'),
            (11, 'u7', 'Nonlinear systems, linearization; predator-prey; Lab B', 'Lebl 8.1–8.3'), (12, 'u7', 'Stability; SIR epidemics; Lab A', 'Lebl 8.2–8.3'),
            (13, 'u8', 'Numerical methods; energy-balance model; Lab C', 'Lebl 1.7, Trench 3'), (14, 'u9', 'Series solutions; Fourier series; heat equation', 'Lebl 7.1–7.2, 4.2, 4.6'),
            (15, 'exam', 'Review and final practice set', 'All units')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Solve y′ = −2ty, y(0) = 3, and find y(1).', ['dy/y = −2t dt; y = 3e^(−t²).'], '3e^(−1) ≈ 1.104.'),
  ('A lake with retention time 4 years: how long until a pollutant falls to half after inflow stops?', ['t = 4 ln 2.'], '≈ 2.77 years.'),
  ('Solve y″ + 6y′ + 9y = 0, y(0) = 1, y′(0) = 0, and find y(1).', ['y = (1 + 3t)e^(−3t).'], '4e^(−3) ≈ 0.199.'),
  ('Solve y′ + y = 1, y(0) = 0 by Laplace and find y(2).', ['Y = 1/(s(s + 1)) = 1/s − 1/(s + 1).'], '1 − e^(−2) ≈ 0.865.')]),
 ('Final practice set (all units)', [
  ('Classify the origin of x′ = [[0, 1], [−2, −2]]x.', ['λ² + 2λ + 2 = 0, λ = −1 ± i.'], 'Stable spiral.'),
  ('An SIR epidemic has β = 0.5, γ = 0.25 per day. Find R₀ and the herd-immunity threshold.', ['R₀ = 2.'], 'R₀ = 2, threshold 50%.'),
  ('Two Euler steps with h = 0.5 for y′ = −y, y(0) = 1.', ['Each step multiplies by 0.5.'], 'y(1) ≈ 0.25 (true e^(−1) ≈ 0.368).'),
  ('A mass-spring system with m = 1 kg, k = 16 N/m, c = 0.4 N·s/m. Find ω₀ and ζ.', ['ω₀ = 4 rad/s; c_crit = 8.'], 'ω₀ = 4 rad/s, ζ = 0.05 (peak amplification about 10).')])]
FORMULAS = ['\\mu=e^{\\int p\\,dx}', 'M_y=N_x\\Rightarrow F=C', 'C=C_0e^{-t/\\tau}', 'H_{\\max}=rK/4', 'ar^2+br+c=0', '\\omega_0=\\sqrt{k/m},\\ c_{\\text{crit}}=2\\sqrt{mk}',
            'X=F_0/\\sqrt{(k-m\\omega^2)^2+(c\\omega)^2}', '\\mathcal L\\{y\'\\}=sY-y(0)', '\\mathcal L\\{e^{at}\\}=1/(s-a)', '\\mathcal L\\{u(t-a)f(t-a)\\}=e^{-as}F(s)',
            '\\lambda^2-(\\operatorname{tr}A)\\lambda+\\det A=0', 'R_0=\\beta/\\gamma,\\ 1-1/R_0', 'y_{n+1}=y_n+hf', 'C\\,T\'=S(1-\\alpha)-\\varepsilon\\sigma T^4', 'u_t=\\alpha u_{xx}', 'b_n=\\tfrac2\\pi\\int_0^\\pi f\\sin nx\\,dx']
GLOSSARY = sorted([('Autonomous equation', 'y′ = f(y), with no explicit t.'), ('Characteristic equation', 'ar² + br + c = 0 for constant-coefficient ODEs.'), ('Critical damping', 'Fastest return without overshoot.'),
    ('Eigenvalue', 'λ with Av = λv.'), ('Energy-balance model', 'Climate model balancing absorbed sunlight and emitted heat.'), ('Equilibrium', 'Constant solution.'), ('Euler’s method', 'First-order numerical stepping.'),
    ('Exact equation', 'M dx + N dy = 0 with M_y = N_x.'), ('Fourier series', 'Expansion in sines and cosines.'), ('Heat equation', 'u_t = α u_xx.'), ('Integrating factor', 'Multiplier making a linear ODE exact.'),
    ('Jacobian', 'Matrix of first partials used to linearize.'), ('Laplace transform', '∫₀^∞ e^(−st) f dt.'), ('Lotka–Volterra', 'Predator-prey model.'), ('Phase portrait', 'Trajectories in the state plane.'),
    ('R₀', 'Basic reproduction number.'), ('Resonance', 'Large response when forcing matches a natural frequency.'), ('Runge–Kutta (RK4)', 'Fourth-order numerical method.'),
    ('Separable equation', 'dy/dx = g(x)h(y).'), ('SIR model', 'Susceptible–infected–recovered epidemic model.')])
RUBRIC = [('4 · Mastery', 'Builds models from a description, solves them by formula and numerically, checks units and long-run behavior.'), ('3 · Proficient', 'Solves the practice problems with occasional slips.'),
          ('2 · Developing', 'Follows worked examples but struggles to set up models or choose a method.'), ('1 · Beginning', 'Applies formulas without checking solutions; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '30%'), ('Computer labs', '15%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    def rk4(f, y, h, n):
        for _ in range(n):
            k1 = f(y); k2 = f([a + h / 2 * b for a, b in zip(y, k1)]); k3 = f([a + h / 2 * b for a, b in zip(y, k2)]); k4 = f([a + h * b for a, b in zip(y, k3)])
            y = [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
        return y
    def eul(f, y, h, n):
        for _ in range(n): y = [a + h * b for a, b in zip(y, f(y))]
        return y
    def ode1(f, y, t1, n=4000):
        h = t1 / n; t = 0
        for _ in range(n):
            k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3); y += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
        return y
    sir = lambda y: [-.3 * y[0] * y[1], .3 * y[0] * y[1] - .1 * y[1], .1 * y[1]]
    s = .5
    for _ in range(300): s = exp(3 * (s - 1))
    y = [.999, .001, 0]; pk = 0; pt = 0
    for i in range(1600):
        y = rk4(sir, y, .1, 1)
        if y[1] > pk: pk, pt = y[1], (i + 1) * .1
    lv = lambda y: [y[0] - .02 * y[0] * y[1], -.5 * y[1] + .005 * y[0] * y[1]]
    p = [150, 50]; t = 0; tim = []; mn = 1e9
    for _ in range(40000):
        q = rk4(lv, p, .001, 1); t += .001; mn = min(mn, q[0])
        if p[1] < 50 <= q[1] and q[0] > 100: tim.append(t)
        p = q
    sig = 5.67e-8; Fin = 340 * .71; eps = Fin / (sig * 288**4); lam = 4 * eps * sig * 288**3; C = 1000 * 4186 * 50
    T = 0; dt = 3.156e7 / 12; ebm = {}
    for n in range(1, 121):
        T += dt * (4 - lam * T) / C
        ebm[n] = T
    A = lambda r, z=.01: 1 / sqrt((1 - r * r)**2 + (2 * z * r)**2)
    damp = lambda t: exp(-t) * (cos(2 * t) + .5 * sin(2 * t))
    return [('xy', ode1(lambda t, y: t * y, 2., 1), 3.297), ('lin', ode1(lambda t, y: 4 - 2 * y, 0., 1), 1.729), ('exact', (-1 + sqrt(5)) / 2, .618), ('exact chk', .618 + .618**2, 1),
            ('erie', 2.6 * log(10), 5.99), ('sup', 191 * log(10), 440), ('ch4', exp(-3), .05), ('msy', .4 * 10000 / 4, 1000), ('cool', 20 + 70 * exp(-1), 45.8), ('mix', ode1(lambda t, x: 1 - x / 50, 0., 50), 31.6),
            ('per', pi, 3.14), ('damp', damp(1), .0142), ('damp num', rk4(lambda y: [y[1], -2 * y[1] - 5 * y[0]], [1, 0], .001, 1000)[0], .0142),
            ('w0', sqrt(50 / 2), 5), ('fHz', 5 / 2 / pi, .796), ('ccrit', 2 * sqrt(100), 20), ('per9', 2 * pi / 3, 2.09),
            ('yp', 1 / (1 - 4), -1 / 3), ('1P', A(.2 / .3), 1.80), ('3P', A(2), .333), ('res', A(1), 50), ('Xamp', 10 / (2 * 10), .5), ('z05', 1 / (2 * .05), 10),
            ('lap1', ode1(lambda t, y: 2 * y + exp(3 * t), 1., 1), exp(3)), ('step', 1 - exp(-1), .632), ('kick num', rk4(lambda y: [y[1], -4 * y[0]], [0, 1], pi / 4 / 1000, 1000)[0], .5),
            ('carbon', rk4(lambda y: [-.2 * y[0] + .1 * y[1], .2 * y[0] - .1 * y[1]], [3, 0], .01, 500)[0], 1 + 2 * exp(-1.5)), ('tau c', 1 / .3, 3.33),
            ('LV eq x', .5 / .005, 100), ('LV eq y', 1 / .02, 50), ('LV per lin', 2 * pi / sqrt(.5), 8.89), ('R0', .3 / .1, 3), ('herd', 1 - 1 / 3, .667), ('sinf', s, .0595), ('inf', 1 - s, .94),
            ('eu', 1.1**10, 2.5937), ('ie', 1.105**10, 2.7141), ('rk', (1 + .1 + .005 + .001 / 6 + .0001 / 24)**10, 2.7182797), ('e', exp(1), 2.7182818),
            ('err eu', exp(1) - 1.1**10, .1245), ('err ie', exp(1) - 1.105**10, .0042), ('Fin', Fin, 241.4), ('T255', (Fin / sig)**.25, 255), ('eps', eps, .619), ('lam', lam, 3.35), ('tau s', C / lam, 6.24e7), ('tau', C / lam / 3.156e7, 1.98),
            ('dT', 4 / lam, 1.19), ('C', C, 2.09e8), ('omega', 2 * pi / 3.156e7, 1.99e-7), ('depth', sqrt(2 * 5e-7 / (2 * pi / 3.156e7)), 2.24), ('b1', 4 / pi, 1.273), ('b3', 4 / 3 / pi, .424),
            ('labA E1', eul(sir, [.999, .001, 0], 1, 160)[2], .9467), ('labA E01', eul(sir, [.999, .001, 0], .1, 1600)[2], .9411), ('labA RK', rk4(sir, [.999, .001, 0], 1, 160)[2], .9405), ('labA th', 1 - s, .9405),
            ('peak', pk, .301), ('peak t', pt, 38.4), ('peak th', 1 - (1 + log(3)) / 3, .300), ('labB min', mn, 62.6), ('labB per', tim[1] - tim[0], 8.99),
            ('ebm1', ebm[12], .48), ('ebm2', ebm[24], .77), ('ebm5', ebm[60], 1.10), ('ebm10', ebm[120], 1.19),
            ('D.1', A(1 / 3), 1.12), ('D.25', A(.25 / .3), 3.27), ('D.35', A(.35 / .3), 2.76), ('rpm18', 18 / 60, .3),
            ('m1', 3 * exp(-1), 1.104), ('m2', 4 * log(2), 2.77), ('m3', 4 * exp(-3), .199), ('m3 num', rk4(lambda y: [y[1], -6 * y[1] - 9 * y[0]], [1, 0], .001, 1000)[0], .199), ('m4', 1 - exp(-2), .865),
            ('f3t', exp(-1), .368), ('f4', .4 / 8, .05)]
