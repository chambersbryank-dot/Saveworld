"""Numerical Methods (MATH 340): floating-point error, root finding, direct and iterative linear solvers, interpolation and least squares, numerical differentiation and integration, ODE solvers, finite differences for PDEs, and optimization, eigenvalues and computing at scale.
Oct 25 2026, founder-approved four-year track, junior course 7. Same module fields as orbit.py / struct.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, sin, cos, exp, log, log2, ceil, e
ID = 'numerics'
STATUS = 'live'
YEAR = 3
PAGE = 'Numerical_Methods.html'
CODE = 'MATH 340'
TITLE = 'Numerical Methods'
LAB_NAME = 'Computation lab'
TAGLINE = 'Solving engineering math on a computer: rounding error, roots of equations, linear systems, curve fitting, derivatives and integrals from data, ODE solvers, finite differences and optimization, with six labs. Free, self-paced, and tied to NOAA weather forecasting, the Mauna Loa CO₂ record and USGS groundwater models.'
DESC = 'Free self-study Numerical Methods: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and spreadsheet labs, practice exams, tied to weather and climate models and environmental data.'
ALT = 'NASA astronaut photo of the Spaceborne Computer-2 aboard the International Space Station'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 18.330 Introduction to Numerical Analysis (Spring 2012)', 'https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/')
_MIT2 = ('MIT OpenCourseWare 2.086 Numerical Computation for Mechanical Engineers (Fall 2014)', 'https://ocw.mit.edu/courses/2-086-numerical-computation-for-mechanical-engineers-fall-2014/')
_MIT10 = ('MIT OpenCourseWare 10.34 Numerical Methods Applied to Chemical Engineering (Fall 2015)', 'https://ocw.mit.edu/courses/10-34-numerical-methods-applied-to-chemical-engineering-fall-2015/')
_OSI = ('OpenStax Calculus Volume 2, 3.6 Numerical integration', 'https://openstax.org/books/calculus-volume-2/pages/3-6-numerical-integration', 'Free textbook section.')
_ONM = ('OpenStax Calculus Volume 1, 4.9 Newton’s method', 'https://openstax.org/books/calculus-volume-1/pages/4-9-newtons-method', 'Free textbook section.')
_GFS = ('NOAA Environmental Modeling Center: Global Forecast System (GFS)', 'https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gfs.php')
_WC = ('NOAA: NOAA completes upgrade to weather and climate supercomputer system (Aug. 10, 2023)', 'https://www.noaa.gov/news-release/noaa-completes-upgrade-to-weather-and-climate-supercomputer-system')
_MLO = ('NOAA Global Monitoring Laboratory: Trends in atmospheric CO₂ (Mauna Loa)', 'https://gml.noaa.gov/ccgg/trends/')
_MLOD = ('NOAA GML: Mauna Loa annual mean CO₂ data', 'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt')
_MF = ('USGS: MODFLOW and Related Programs', 'https://www.usgs.gov/mission-areas/water-resources/science/modflow-and-related-programs')
_GISS = ('NASA GISS: GISS Earth System Model, ModelE', 'https://www.giss.nasa.gov/tools/modelE/')
_GT = ('NASA GISS: GISS Surface Temperature Analysis (GISTEMP v4)', 'https://data.giss.nasa.gov/gistemp/')
BANNER = ['images/Spaceborne_Computer2_iss065e009492.jpg', 'images/GOES19_GOESU_KSC.jpg', 'images/ISS_Flyaround_2021.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg']
CREDITS = {'images/Spaceborne_Computer2_iss065e009492.jpg': 'NASA/Michael Hopkins (ISS065-E-009492, April 29, 2021)', 'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC',
           'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester junior numerical methods course for engineers. It is modeled on the topics and depth of MIT 18.330 Introduction to Numerical Analysis, MIT 2.086 Numerical Computation for Mechanical Engineers and MIT 10.34 (free on MIT OpenCourseWare), using free OpenStax calculus sections, which we link where they help. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (NOAA’s Global Forecast System and supercomputers, the Mauna Loa CO₂ record, USGS groundwater models and NASA climate models), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a spreadsheet.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Weather forecasts, climate projections and groundwater plans are all numerical methods running on computers: the equations cannot be solved by hand, so they are broken into grids, time steps and huge linear systems.',
                 'Knowing how those methods work, and how they fail, is how engineers judge a forecast or a model. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Calculus I and II: derivatives, integrals and Taylor series.', 'Differential Equations: first-order and second-order ODEs.',
           'Linear Algebra: matrices, determinants and eigenvalues.', 'Intro Programming: loops, functions and arrays (a spreadsheet also works).']
STUDY = ['Before computing, estimate the answer and decide what accuracy you need.', 'Always compare against an exact answer on a test problem before trusting a method on a real one.',
         'Track the error as you halve the step: the ratio tells you the order of the method.', 'Keep units in SI and write the step size with its units.',
         'Watch for subtracting nearly equal numbers; rewrite the formula if you can.', 'Do every practice problem on paper or in a spreadsheet before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Least-Squares Regression, Curve Fitting, Calculus Grapher and Projectile Motion simulations.', 'Spreadsheet software (any free one works), or Python if you know it.',
            'NOAA’s Mauna Loa CO₂ data file in a web browser.', 'A calculator.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free simulation or a spreadsheet, so there are no physical hazards. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('Double precision (IEEE 754)', 'machine epsilon 2⁻⁵² = 2.22 × 10⁻¹⁶, about 16 significant digits'), ('Single precision (IEEE 754)', 'machine epsilon 2⁻²³ = 1.19 × 10⁻⁷, about 7 significant digits'),
             ('e', '2.718281828'), ('π', '3.141592654'), ('Earth’s surface area (textbook value)', '5.1 × 10⁸ km²'), ('1 petaflop', '10¹⁵ floating-point operations per second')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, textbook sections and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT numerical analysis lectures and problem sets.'), (_MIT2[0], _MIT2[1], 'Free MIT engineering computation course.'), (_MIT10[0], _MIT10[1], 'Free MIT applied numerical methods course.'),
          (_OSI[0], _OSI[1], 'Free textbook section.'), (_ONM[0], _ONM[1], 'Free textbook section.'), ('PhET: Least-Squares Regression', _PH + 'least-squares-regression', 'Fit lines interactively.')]
UNITS = []
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS.append(
{'id': 'u1', 'title': 'Errors, Floating-Point Numbers and Taylor Series', 'weeks': 'Week 1',
 'summary': 'Absolute and relative error, significant digits, IEEE 754 floating-point numbers, machine epsilon, rounding and cancellation, and truncation error from Taylor series.',
 'objectives': ['Compute absolute and relative error.', 'Explain machine epsilon for single and double precision.', 'Spot and fix catastrophic cancellation.', 'Bound truncation error with the next Taylor term.'],
 'concepts': ['Absolute error is |approximate − exact|; relative error divides by |exact|. Relative error tells you how many digits are right.',
              'Computers store numbers in binary floating point. Double precision has machine epsilon 2⁻⁵² ≈ 2.22 × 10⁻¹⁶ (about 16 digits); single precision has 2⁻²³ ≈ 1.19 × 10⁻⁷ (about 7 digits).',
              'Most decimals, like 0.1, have no exact binary form, so 0.1 + 0.2 − 0.3 comes out as about 5.55 × 10⁻¹⁷ instead of 0.',
              'Subtracting nearly equal numbers loses digits (catastrophic cancellation). Rewriting the formula algebraically often fixes it.',
              'Truncation error comes from cutting off an infinite process, such as a Taylor series. The first dropped term estimates the error.'],
 'eqs': [('e_{rel}=\\frac{|\\tilde x-x|}{|x|}', 'Relative error'), ('\\varepsilon_{mach}=2^{-52}\\approx2.22\\times10^{-16}', 'Double-precision epsilon'), ('f(x+h)=f(x)+hf\'(x)+\\frac{h^2}{2}f\'\'(x)+\\dots', 'Taylor series'), ('\\sqrt{x+1}-\\sqrt{x}=\\frac{1}{\\sqrt{x+1}+\\sqrt{x}}', 'Avoiding cancellation')],
 'worked': [
  _w('Find the relative error of 22/7 as an approximation to π.', ['|22/7 − π| = 0.001264.', 'Divide by π.'], 'Relative error = 4.02 × 10⁻⁴, so about 3 correct digits.'),
  _w('Compute √(10⁸ + 1) − √(10⁸) safely.', ['Direct subtraction cancels most digits.', 'Use 1/(√(10⁸ + 1) + √(10⁸)).'], '5.0 × 10⁻⁵ (more exactly 4.99999999875 × 10⁻⁵).'),
  _w('Estimate the error of e^0.1 ≈ 1 + 0.1.', ['The next term is 0.1²/2 = 0.005.', 'The true error is e^0.1 − 1.1.'], 'Error = 0.00517, close to the 0.005 estimate.')],
 'practice': [('How many correct digits does double precision give?', 'About 16 (ε = 2.22 × 10⁻¹⁶).'), ('Add the 0.1³/6 term to e^0.1 ≈ 1.1. New error?', '1.71 × 10⁻⁴.'),
              ('Why is 0.1 + 0.2 − 0.3 not exactly 0 on a computer?', '0.1 and 0.2 have no exact binary form; the result is about 5.55 × 10⁻¹⁷.'), ('What is single-precision epsilon?', '2⁻²³ = 1.19 × 10⁻⁷.')],
 'misc': [('Computers do exact arithmetic.', 'Every operation rounds to the nearest floating-point number.'), ('Smaller steps always mean smaller error.', 'Rounding error grows as steps shrink.'), ('Relative and absolute error are the same.', 'Relative error divides by the true size.')],
 'quiz': [_q('Double-precision epsilon is about…', ['2.2 × 10⁻¹⁶', '10⁻⁷', '10⁻³', '0'], 0, '2⁻⁵².'), _q('Subtracting nearly equal numbers causes…', ['cancellation', 'overflow', 'nothing', 'exact results'], 0, 'Lost digits.'),
          _q('Truncation error comes from…', ['cutting off a series', 'binary storage', 'typing errors', 'units'], 0, 'Definition.'), _q('Relative error divides by…', ['the true value', 'the step', 'epsilon', '10'], 0, 'Definition.')],
 'cards': [('Absolute error', '|approx − exact|.'), ('Relative error', 'Absolute error / |exact|.'), ('Machine epsilon', '2⁻⁵² ≈ 2.22 × 10⁻¹⁶ in double.'), ('Cancellation', 'Digit loss when subtracting close numbers.'), ('Truncation error', 'From cutting off an infinite process.'), ('Single precision', 'About 7 digits.')],
 'planet': {'text': ['NOAA’s Environmental Modeling Center describes a coupled global forecast run at about 3 km resolution that ran its atmospheric dynamics in 32-bit precision and everything else in 64-bit precision, a deliberate trade between speed and accuracy.',
                     'That is this unit’s epsilon choice in practice: single precision (about 7 digits) is faster and uses half the memory, so modelers use it where the error it adds stays below the error the model already has.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Intro to Programming', 'Intro_to_Programming.html')],
            'src': [_GFS]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_MIT2[0], _MIT2[1], 'Free MIT course.')]})
UNITS.append(
{'id': 'u2', 'title': 'Roots of Equations: Bisection, Newton and Secant', 'weeks': 'Weeks 2–3',
 'summary': 'Bracketing with bisection, Newton’s method, the secant method, fixed-point iteration, convergence order and stopping rules.',
 'objectives': ['Find a root by bisection and predict the number of steps.', 'Apply Newton’s method and recognize quadratic convergence.', 'Use the secant method when the derivative is unknown.', 'Choose a stopping rule.'],
 'concepts': ['Bisection halves a bracket [a, b] where f changes sign. It always converges, but only one binary digit per step: n ≥ log₂((b − a)/tol).',
              'Newton’s method follows the tangent line: x_{n+1} = x_n − f(x_n)/f′(x_n). Near a simple root it converges quadratically, doubling the correct digits each step.',
              'The secant method replaces f′ with the slope through the last two points. It needs no derivative and converges with order about 1.618.',
              'Newton can fail if f′ is near zero or the start is far away; a bracketing fallback makes it safe.',
              'Stop when |x_{n+1} − x_n| and |f(x_n)| are both below tolerance, and always cap the number of iterations.'],
 'eqs': [('x_{n+1}=x_n-\\frac{f(x_n)}{f\'(x_n)}', 'Newton’s method'), ('x_{n+1}=x_n-f(x_n)\\frac{x_n-x_{n-1}}{f(x_n)-f(x_{n-1})}', 'Secant method'), ('n\\ge\\log_2\\frac{b-a}{tol}', 'Bisection steps'), ('|e_{n+1}|\\approx C|e_n|^2', 'Quadratic convergence')],
 'worked': [
  _w('Use bisection on f(x) = x³ − x − 2 on [1, 2]. Give the first three midpoints and the root.', ['f(1) = −2, f(2) = 4.', 'Midpoints 1.5, 1.75, 1.625.'], 'Root x = 1.5214.'),
  _w('How many bisection steps shrink a width-1 bracket below 10⁻⁶?', ['log₂(10⁶) = 19.93.'], '20 steps.'),
  _w('Use Newton’s method on x² − 2 from x₀ = 1.', ['x₁ = 1.5, x₂ = 1.41667.', 'x₃ = 1.414216.'], 'x₃ = 1.414216, already 6 correct digits.')],
 'practice': [('Apply Newton to x³ − x − 2 from x₀ = 1.5. First step?', '1.52174.'), ('Apply the secant method to x² − 2 from 1 and 2. First three iterates?', '1.3333, 1.4000, 1.4146.'),
              ('What convergence order does the secant method have?', 'About 1.618.'), ('Why cap the iteration count?', 'A method may diverge or cycle.')],
 'misc': [('Newton always converges.', 'It can diverge from a poor start.'), ('Bisection is fast.', 'It gains one bit per step.'), ('A small f(x) means x is close to the root.', 'Not if f is very flat.')],
 'quiz': [_q('Newton converges…', ['quadratically', 'linearly', 'never', 'cubically always'], 0, 'Near a simple root.'), _q('Bisection needs…', ['a sign change', 'a derivative', 'a matrix', 'nothing'], 0, 'Bracket.'),
          _q('Secant avoids…', ['the derivative', 'f', 'iteration', 'starting points'], 0, 'Slope from two points.'), _q('Steps to 10⁻⁶ from width 1 by bisection…', ['20', '6', '100', '2'], 0, 'log₂ 10⁶.')],
 'cards': [('Bisection', 'Halve a sign-change bracket.'), ('Newton', 'x − f/f′.'), ('Secant', 'Newton with a two-point slope.'), ('Quadratic convergence', 'Digits double each step.'), ('Bracket', 'Interval with a sign change.'), ('Stopping rule', 'Step and residual below tolerance.')],
 'planet': {'text': ['The USGS says MODFLOW is considered an international standard for simulating groundwater. One of its versions, MODFLOW-NWT, uses a Newton-Raphson formulation to improve the solution of unconfined groundwater-flow problems.',
                     'Unconfined aquifers make the equations nonlinear, because the saturated thickness depends on the water level being solved for. Newton’s method from this unit is what makes those runs converge reliably.'],
            'site': [('Oceans', 'Oceans.html'), ('Calculus I', 'Calculus_I.html')],
            'src': [_MF]},
 'res': [_ONM, (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u3', 'title': 'Linear Systems: Gaussian Elimination, LU and Conditioning', 'weeks': 'Week 4',
 'summary': 'Gaussian elimination with partial pivoting, LU factorization, operation counts, the condition number and how it limits accuracy.',
 'objectives': ['Solve a 3 × 3 system by elimination.', 'Explain LU factorization and reuse.', 'Estimate the cost of elimination.', 'Use the condition number to judge accuracy.'],
 'concepts': ['Gaussian elimination reduces Ax = b to an upper-triangular system, then back-substitutes. Partial pivoting swaps rows so the largest pivot is used, which controls rounding error.',
              'LU factorization stores the elimination as A = LU. Once factored, each new right-hand side costs only two triangular solves.',
              'Elimination costs about 2n³/3 floating-point operations: doubling n multiplies the work by 8.',
              'The condition number κ(A) = ‖A‖‖A⁻¹‖ measures sensitivity. You can lose about log₁₀ κ digits of accuracy.',
              'Never compute A⁻¹ to solve a system; factor and solve instead.'],
 'eqs': [('A=LU', 'LU factorization'), ('\\text{cost}\\approx\\tfrac23n^3', 'Elimination flops'), ('\\kappa(A)=\\|A\\|\\|A^{-1}\\|', 'Condition number'), ('\\frac{\\|\\delta x\\|}{\\|x\\|}\\le\\kappa\\frac{\\|\\delta b\\|}{\\|b\\|}', 'Error bound')],
 'worked': [
  _w('Solve 2x + y − z = 8, −3x − y + 2z = −11, −2x + y + 2z = −3.', ['Eliminate x from rows 2 and 3, then y from row 3.', 'Back-substitute.'], 'x = 2, y = 3, z = −1.'),
  _w('Estimate the elimination cost for n = 1000.', ['2 × 1000³/3.'], 'About 6.67 × 10⁸ flops.'),
  _w('Find the 2-norm condition number of [[1, 1], [1, 1.0001]].', ['The rows are nearly parallel.', 'κ = σ_max/σ_min.'], 'κ ≈ 40,002, so about 4–5 digits can be lost.')],
 'practice': [('How much more work is n = 2000 than n = 1000?', '8 times.'), ('Elimination flops for n = 3?', '2 × 27/3 = 18.'),
              ('Why pivot?', 'To avoid dividing by small numbers and amplifying rounding.'), ('Digits lost with κ = 10⁸ in double precision?', 'About 8 of 16.')],
 'misc': [('Use A⁻¹ to solve systems.', 'Factor and solve; it is cheaper and more accurate.'), ('A small determinant means ill-conditioned.', 'Use the condition number.'), ('Pivoting is optional.', 'Without it, elimination can fail or lose accuracy.')],
 'quiz': [_q('Elimination costs about…', ['2n³/3', 'n', 'n²', '2ⁿ'], 0, 'Triple loop.'), _q('LU helps when…', ['many right-hand sides', 'n = 1', 'no solution', 'never'], 0, 'Reuse factors.'),
          _q('Large κ means…', ['sensitive', 'easy', 'singular always', 'symmetric'], 0, 'Amplifies errors.'), _q('Partial pivoting picks…', ['largest pivot', 'smallest', 'zero', 'random'], 0, 'Stability.')],
 'cards': [('Gaussian elimination', 'Reduce to triangular form.'), ('LU', 'A = LU.'), ('Pivoting', 'Row swaps for stability.'), ('Condition number', '‖A‖‖A⁻¹‖.'), ('Back substitution', 'Solve triangular systems.'), ('Cost', '≈ 2n³/3.')],
 'planet': {'text': ['The USGS says a key feature of MODFLOW 6 is its ability to solve multiple tightly coupled numerical models in a single system of equations.',
                     'Its map of depth to the water table across the continental United States came from a parallel simulation of 256 tightly coupled model domains on 256 cores of a USGS supercomputer. Each domain is a large sparse linear system like the ones in this unit.'],
            'site': [('Linear Algebra', 'Linear_Algebra.html'), ('Oceans', 'Oceans.html')],
            'src': [_MF]},
 'res': [(_MIT2[0], _MIT2[1], 'Free MIT course.'), (_MIT10[0], _MIT10[1], 'Free MIT course.')]})
UNITS.append(
{'id': 'u4', 'title': 'Iterative Solvers: Jacobi, Gauss–Seidel and Convergence', 'weeks': 'Week 5',
 'summary': 'Jacobi and Gauss–Seidel iteration, diagonal dominance, the iteration matrix and spectral radius, sparse systems and why iterative methods scale.',
 'objectives': ['Carry out Jacobi and Gauss–Seidel steps.', 'Test diagonal dominance.', 'Use the spectral radius to predict convergence speed.', 'Explain why large sparse systems use iteration.'],
 'concepts': ['Jacobi updates every unknown from the previous iterate; Gauss–Seidel uses new values as soon as they are computed.',
              'If A is strictly diagonally dominant, both methods converge from any start.',
              'The error shrinks each step by about the spectral radius ρ of the iteration matrix. Gauss–Seidel often has ρ_GS = ρ_J².',
              'Large grids give sparse matrices with only a few nonzeros per row. Iterative methods store only those nonzeros, while elimination fills in.',
              'Stop when the residual ‖b − Ax‖ is small relative to ‖b‖.'],
 'eqs': [('x_i^{(k+1)}=\\frac{1}{a_{ii}}\\Big(b_i-\\sum_{j\\ne i}a_{ij}x_j^{(k)}\\Big)', 'Jacobi'), ('|a_{ii}|>\\sum_{j\\ne i}|a_{ij}|', 'Diagonal dominance'), ('\\|e_{k}\\|\\approx\\rho^k\\|e_0\\|', 'Convergence rate'), ('r=b-Ax', 'Residual')],
 'worked': [
  _w('Do two Jacobi steps on 4x + y = 1, x + 3y = 2 from (0, 0).', ['Step 1: x = 1/4 = 0.25, y = 2/3 = 0.6667.', 'Step 2: x = (1 − 0.6667)/4, y = (2 − 0.25)/3.'], 'x = 0.0833, y = 0.5833 (exact 0.0909, 0.6364).'),
  _w('Do two Gauss–Seidel steps on the same system.', ['Step 1: x = 0.25, y = (2 − 0.25)/3 = 0.5833.', 'Step 2: x = 0.1042, y = 0.6319.'], 'x = 0.1042, y = 0.6319, closer than Jacobi.'),
  _w('Find the Jacobi and Gauss–Seidel spectral radii for that system.', ['ρ_J = √(1/12).', 'ρ_GS = ρ_J² = 1/12.'], 'ρ_J = 0.289; ρ_GS = 0.0833.')],
 'practice': [('Is [[4, 1], [1, 3]] diagonally dominant?', 'Yes: 4 > 1 and 3 > 1.'), ('Steps for Gauss–Seidel (ρ = 0.0833) to cut error by 10⁶?', 'About 6 (0.0833⁶ = 3.35 × 10⁻⁷).'),
              ('Third Gauss–Seidel iterate?', 'x = 0.0920, y = 0.6360.'), ('Why not eliminate on a million-unknown grid?', 'Fill-in uses too much memory and time.')],
 'misc': [('Iteration always converges.', 'It needs ρ < 1.'), ('Jacobi and Gauss–Seidel are the same.', 'Gauss–Seidel uses new values immediately.'), ('A small change between steps means converged.', 'Check the residual too.')],
 'quiz': [_q('Converges if…', ['ρ < 1', 'ρ > 1', 'n is even', 'A is singular'], 0, 'Error shrinks.'), _q('Gauss–Seidel uses…', ['newest values', 'old values only', 'no values', 'inverses'], 0, 'Definition.'),
          _q('Sparse means…', ['mostly zeros', 'dense', 'small n', 'singular'], 0, 'Few nonzeros.'), _q('Sufficient for convergence…', ['diagonal dominance', 'symmetry only', 'n = 2', 'nothing'], 0, 'Theorem.')],
 'cards': [('Jacobi', 'Update all from old values.'), ('Gauss–Seidel', 'Use new values immediately.'), ('Spectral radius', 'Largest |eigenvalue|.'), ('Diagonal dominance', '|a_ii| > row sum.'), ('Sparse', 'Mostly zeros.'), ('Residual', 'b − Ax.')],
 'planet': {'text': ['NOAA’s GFS divides the atmosphere into 127 vertical layers at about 13 km horizontal spacing. Each grid point couples only to its neighbours, so the systems such models build are huge and sparse.',
                     'With a textbook Earth surface area of 5.1 × 10⁸ km², a 13 km grid has about 3.0 million columns and 383 million cells. Systems that size are handled with iterative and other sparse methods, not plain elimination.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Linear Algebra', 'Linear_Algebra.html')],
            'src': [_GFS]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_MIT2[0], _MIT2[1], 'Free MIT course.')]})
UNITS.append(
{'id': 'u5', 'title': 'Interpolation, Splines and Least-Squares Fitting', 'weeks': 'Weeks 6–7',
 'summary': 'Linear and polynomial interpolation, Lagrange form, the danger of high-degree polynomials, cubic splines, and least-squares line and polynomial fits with residuals.',
 'objectives': ['Interpolate linearly between data points.', 'Build a Lagrange polynomial.', 'Fit a least-squares line and interpret its slope.', 'Choose between interpolation and fitting.'],
 'concepts': ['Interpolation passes exactly through the data; fitting passes near noisy data and minimizes the sum of squared residuals.',
              'A degree-n polynomial through n + 1 points is unique. High degrees on equally spaced points can oscillate wildly near the ends (Runge’s phenomenon).',
              'Cubic splines join cubic pieces with matching slope and curvature, giving smooth curves without wild swings.',
              'The least-squares line solves the normal equations AᵀAc = Aᵀy. The slope is a rate, with units.',
              'Plot the residuals: a pattern in them means the model is missing something, such as curvature.'],
 'eqs': [('y=y_0+\\frac{x-x_0}{x_1-x_0}(y_1-y_0)', 'Linear interpolation'), ('p(x)=\\sum_i y_i\\prod_{j\\ne i}\\frac{x-x_j}{x_i-x_j}', 'Lagrange form'), ('A^TA\\,c=A^Ty', 'Normal equations'), ('\\min\\sum_i r_i^2', 'Least squares')],
 'worked': [
  _w('NOAA’s Mauna Loa annual means are 390.10 ppm (2010) and 414.21 ppm (2020). Interpolate 2015.', ['y = 390.10 + 0.5 × 24.11.'], '402.16 ppm; NOAA’s 2015 value is 401.01, so the record curves upward.'),
  _w('Fit a least-squares line to the decade values 1960–2020 (316.91, 325.68, 338.76, 354.45, 369.71, 390.10, 414.21 ppm).', ['Solve the normal equations for slope and intercept.'], 'Slope 1.613 ppm per year; the line predicts 415.0 ppm for 2025.'),
  _w('Fit a quadratic in t = year − 1960 instead.', ['Least squares with columns 1, t, t².'], 'c = 316.84 + 0.810t + 0.01338t²; it predicts 426.0 ppm for 2025, close to NOAA’s 427.35.')],
 'practice': [('Average growth 2010–2020 from the decade values?', '2.41 ppm per year.'), ('Average growth 2000–2010?', '2.04 ppm per year.'),
              ('Why does the straight line underpredict 2025?', 'Growth is speeding up; the residuals curve.'), ('Interpolate or fit noisy lab data?', 'Fit.')],
 'misc': [('Higher-degree polynomials always fit better.', 'They can oscillate between points.'), ('A good R² means a good model.', 'Check the residual pattern.'), ('Extrapolation is as safe as interpolation.', 'It is much riskier.')],
 'quiz': [_q('Least squares minimizes…', ['sum of squared residuals', 'max error', 'slope', 'degree'], 0, 'Definition.'), _q('Runge’s phenomenon is…', ['end oscillation', 'cancellation', 'divergence', 'pivoting'], 0, 'High-degree polynomials.'),
          _q('Splines are…', ['piecewise cubics', 'single lines', 'random', 'Taylor series'], 0, 'Definition.'), _q('Normal equations are…', ['AᵀAc = Aᵀy', 'Ax = 0', 'LU', 'f = 0'], 0, 'Least squares.')],
 'cards': [('Interpolation', 'Exactly through the data.'), ('Least squares', 'Minimize squared residuals.'), ('Spline', 'Smooth piecewise cubic.'), ('Runge', 'Wiggles of high-degree fits.'), ('Residual', 'Data minus model.'), ('Normal equations', 'AᵀAc = Aᵀy.')],
 'planet': {'text': ['NOAA reports that the Mauna Loa record, started by C. David Keeling of Scripps in March 1958, is the longest record of direct CO₂ measurements in the atmosphere. The monthly mean was 426.07 ppm in September 2026, up from 424.37 ppm in September 2025.',
                     'NOAA’s annual means rose from 316.91 ppm in 1960 to 427.35 ppm in 2025. The upward curve shows up in this unit’s residuals: a straight line misses it, and a quadratic fits.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_MLO, _MLOD]},
 'res': [('PhET: Least-Squares Regression', _PH + 'least-squares-regression', 'Fit lines interactively.'), ('PhET: Curve Fitting', _PH + 'curve-fitting', 'Polynomial fits interactively.')]})
UNITS.append(
{'id': 'u6', 'title': 'Numerical Differentiation', 'weeks': 'Week 8',
 'summary': 'Forward, backward and central differences, their truncation error, the balance with rounding error and the best step size, second derivatives, and Richardson extrapolation.',
 'objectives': ['Apply forward and central differences.', 'State the order of each formula.', 'Choose a step size that balances truncation and rounding.', 'Estimate a second derivative.'],
 'concepts': ['The forward difference (f(x + h) − f(x))/h has error proportional to h (first order).',
              'The central difference (f(x + h) − f(x − h))/(2h) has error proportional to h² (second order), so halving h cuts the error by 4.',
              'Rounding error grows like ε/h as h shrinks. For forward differences the best h is about √ε ≈ 1.49 × 10⁻⁸; for central differences about ε^(1/3) ≈ 6.06 × 10⁻⁶.',
              'The second derivative is (f(x + h) − 2f(x) + f(x − h))/h², also second order.',
              'Richardson extrapolation combines two step sizes to cancel the leading error term.'],
 'eqs': [('f\'(x)\\approx\\frac{f(x+h)-f(x)}{h}', 'Forward difference'), ('f\'(x)\\approx\\frac{f(x+h)-f(x-h)}{2h}', 'Central difference'), ('f\'\'(x)\\approx\\frac{f(x+h)-2f(x)+f(x-h)}{h^2}', 'Second difference'), ('h_{opt}\\approx\\sqrt{\\varepsilon}', 'Best forward step')],
 'worked': [
  _w('Estimate the derivative of sin x at x = 1 with a forward difference, h = 0.1.', ['(sin 1.1 − sin 1)/0.1.'], '0.4974; exact cos 1 = 0.5403; error −0.0429.'),
  _w('Repeat with a central difference.', ['(sin 1.1 − sin 0.9)/0.2.'], '0.5394; error −0.00090, about 47.7 times smaller.'),
  _w('Find the best forward-difference step in double precision.', ['h ≈ √(2.22 × 10⁻¹⁶).'], 'h ≈ 1.49 × 10⁻⁸.')],
 'practice': [('Halve h in a central difference. Error?', 'About ¼ as large.'), ('Halve h in a forward difference. Error?', 'About ½ as large.'),
              ('Best central-difference step in double precision?', 'About ε^(1/3) = 6.06 × 10⁻⁶.'), ('Why not use h = 10⁻¹⁵?', 'Rounding error ε/h dominates.')],
 'misc': [('Smaller h is always better.', 'Below the optimum, rounding wins.'), ('Forward and central are equally accurate.', 'Central is second order.'), ('Differentiating noisy data is easy.', 'Differences amplify noise; smooth or fit first.')],
 'quiz': [_q('Central difference error ∝…', ['h²', 'h', '1/h', 'h³ always'], 0, 'Symmetric.'), _q('Forward difference is … order.', ['first', 'second', 'zero', 'fourth'], 0, 'Error ∝ h.'),
          _q('Best forward h is about…', ['√ε', 'ε', '1', '0.1'], 0, 'Balance.'), _q('Noise in data is … by differencing.', ['amplified', 'removed', 'halved', 'unchanged'], 0, 'Divides by h.')],
 'cards': [('Forward difference', 'First order.'), ('Central difference', 'Second order.'), ('Second difference', 'f(x+h) − 2f(x) + f(x−h) over h².'), ('Optimal h', '≈ √ε for forward.'), ('Richardson', 'Cancel the leading error.'), ('Order', 'Exponent of h in the error.')],
 'planet': {'text': ['NOAA says the GFS produces hourly forecast output for the first 120 hours, then 3-hourly output for days 5 to 16. Forecasters and downstream models difference those outputs to get rates such as pressure tendency and rainfall rate.',
                     'This unit shows why the time step of saved output matters: a rate taken from 3-hourly values with a central difference is far more accurate than a one-sided difference over the same interval.'],
            'site': [('GOES-19', 'GOES-19.html'), ('Calculus I', 'Calculus_I.html')],
            'src': [_GFS]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), ('PhET: Calculus Grapher', _PH + 'calculus-grapher', 'Derivatives interactively.')]})
UNITS.append(
{'id': 'u7', 'title': 'Numerical Integration', 'weeks': 'Week 9',
 'summary': 'Trapezoidal and Simpson’s rules, composite rules and error orders, Romberg extrapolation, Gaussian quadrature, and integrating measured data.',
 'objectives': ['Apply the composite trapezoidal and Simpson’s rules.', 'Predict how error falls with n.', 'Use Romberg to improve a result.', 'Apply 2-point Gaussian quadrature.'],
 'concepts': ['The trapezoidal rule joins points with straight lines. Its error falls like h²: doubling n cuts it by 4.',
              'Simpson’s rule fits parabolas through pairs of intervals (n even). Its error falls like h⁴: doubling n cuts it by 16.',
              'Romberg extrapolation: T₂ₙ + (T₂ₙ − Tₙ)/3 cancels the h² error of the trapezoidal rule (it equals Simpson’s rule).',
              'Gaussian quadrature picks the best points: 2 points at ±1/√3 integrate cubics exactly.',
              'For measured data at fixed spacing, use the trapezoidal or Simpson rule directly on the samples.'],
 'eqs': [('T_n=h\\Big[\\tfrac12f_0+f_1+\\dots+f_{n-1}+\\tfrac12f_n\\Big]', 'Trapezoidal rule'), ('S_n=\\tfrac h3\\big[f_0+4f_1+2f_2+\\dots+4f_{n-1}+f_n\\big]', 'Simpson’s rule'), ('\\int_{-1}^{1}f\\approx f(-\\tfrac1{\\sqrt3})+f(\\tfrac1{\\sqrt3})', '2-point Gauss'), ('E_T\\propto h^2,\\ E_S\\propto h^4', 'Error orders')],
 'worked': [
  _w('Estimate ∫₀¹ eˣ dx with the trapezoidal rule, n = 4.', ['h = 0.25; sum the weighted values.'], 'T₄ = 1.72722; exact e − 1 = 1.71828; error 0.00894.'),
  _w('Repeat with Simpson’s rule, n = 4.', ['Weights 1, 4, 2, 4, 1 times h/3.'], 'S₄ = 1.718319; error 3.70 × 10⁻⁵.'),
  _w('Use 2-point Gaussian quadrature on the same integral.', ['Map [0, 1] to [−1, 1]: points 0.5 ± 0.5/√3, weight ½ each.'], '1.717896; error −3.85 × 10⁻⁴ with only 2 function values.')],
 'practice': [('Trapezoidal error with n = 8?', '0.00224, about ¼ of the n = 4 error.'), ('Romberg from T₄ and T₈?', '1.718284.'),
              ('Simpson’s rule with n = 2?', '1.718861.'), ('Why must Simpson’s n be even?', 'It uses pairs of intervals.')],
 'misc': [('Simpson works for any n.', 'n must be even.'), ('More points always help equally.', 'Higher-order rules gain much faster.'), ('Gauss points can be anywhere.', 'They are fixed roots of Legendre polynomials.')],
 'quiz': [_q('Simpson error ∝…', ['h⁴', 'h²', 'h', '1'], 0, 'Fourth order.'), _q('Doubling n in the trapezoidal rule cuts error by…', ['4', '2', '16', '1'], 0, 'h².'),
          _q('2-point Gauss is exact for…', ['cubics', 'all functions', 'lines only', 'nothing'], 0, 'Degree 2n − 1.'), _q('Romberg cancels…', ['the leading error', 'all error', 'rounding', 'f'], 0, 'Extrapolation.')],
 'cards': [('Trapezoidal', 'Error ∝ h².'), ('Simpson', 'Error ∝ h⁴.'), ('Romberg', 'Extrapolate trapezoid results.'), ('Gauss quadrature', 'Optimal points and weights.'), ('Composite rule', 'Apply on many subintervals.'), ('Even n', 'Needed for Simpson.')],
 'planet': {'text': ['NOAA explains that every Mauna Loa monthly mean is the average of daily means, which are in turn based on hourly averages, using only hours with “background” conditions.',
                     'An average is an integral divided by the interval, so building monthly means from hourly values is numerical integration, the trapezoidal idea from this unit applied to real measurements.'],
            'site': [('Calculus II', 'Calculus_II.html'), ('Solutions', 'Solutions.html')],
            'src': [_MLO]},
 'res': [_OSI, ('PhET: Calculus Grapher', _PH + 'calculus-grapher', 'Integrals interactively.')]})
UNITS.append(
{'id': 'u8', 'title': 'Ordinary Differential Equations: Euler, Runge–Kutta and Stability', 'weeks': 'Weeks 10–11',
 'summary': 'Euler’s method, Heun’s method, fourth-order Runge–Kutta, local and global error, stability limits, stiff equations and implicit methods, and systems of ODEs.',
 'objectives': ['Step an ODE with Euler and RK4.', 'Relate step size to global error.', 'Find the explicit stability limit for y′ = −λy.', 'Recognize stiff problems.'],
 'concepts': ['Euler’s method y_{n+1} = y_n + h f(t_n, y_n) has global error proportional to h (first order).',
              'Fourth-order Runge–Kutta (RK4) uses four slope samples per step; its global error falls like h⁴.',
              'For y′ = −λy, explicit Euler is stable only if h < 2/λ. Outside that, the numerical solution grows even though the true one decays.',
              'Stiff problems have very fast and very slow parts. Implicit methods such as backward Euler stay stable with large steps.',
              'Higher-order ODEs become first-order systems, which the same methods solve.'],
 'eqs': [('y_{n+1}=y_n+hf(t_n,y_n)', 'Euler'), ('y_{n+1}=y_n+\\tfrac h6(k_1+2k_2+2k_3+k_4)', 'RK4'), ('h<\\frac{2}{\\lambda}', 'Euler stability for y′ = −λy'), ('y_{n+1}=y_n+hf(t_{n+1},y_{n+1})', 'Backward Euler')],
 'worked': [
  _w('Solve y′ = −y, y(0) = 1 to t = 1 with Euler, h = 0.1.', ['Each step multiplies by 0.9.', 'y(1) ≈ 0.9¹⁰.'], '0.34868 vs exact 0.36788; error −0.0192.'),
  _w('Take one RK4 step of h = 0.1 on the same problem.', ['k₁ = −1, k₂ = −0.95, k₃ = −0.9525, k₄ = −0.90475.'], 'y(0.1) = 0.9048375 vs exact 0.9048374.'),
  _w('A coffee cools by T′ = −0.1(T − 20) from 90 °C (sample values). Use Euler with h = 1 min for 10 min.', ['Each step: T − 20 shrinks by 0.9.'], '44.41 °C vs exact 45.75 °C.')],
 'practice': [('Euler with h = 0.05 to t = 1 on y′ = −y?', '0.95²⁰ = 0.35849, error about half.'), ('Stability limit for y′ = −50y with Euler?', 'h < 0.04.'),
              ('One Heun step of h = 0.1 on y′ = −y?', '0.905.'), ('How do you solve y″ = −y with these methods?', 'Write it as y′ = v, v′ = −y.')],
 'misc': [('A smaller step is always stable.', 'Only below the limit, and rounding grows with many steps.'), ('RK4 is exact.', 'Its error is small but not zero.'), ('Implicit methods are always slower.', 'For stiff problems they are much faster overall.')],
 'quiz': [_q('Euler global error ∝…', ['h', 'h⁴', 'h²', '1'], 0, 'First order.'), _q('RK4 uses … slopes.', ['4', '1', '2', '10'], 0, 'k₁ to k₄.'),
          _q('Euler stable for y′ = −λy if…', ['h < 2/λ', 'h > 2/λ', 'any h', 'λ < 0'], 0, 'Amplification |1 − hλ| < 1.'), _q('Stiff problems favour…', ['implicit methods', 'Euler', 'bisection', 'Simpson'], 0, 'Stability.')],
 'cards': [('Euler', 'First-order explicit.'), ('RK4', 'Fourth order, 4 slopes.'), ('Stability', 'Errors do not grow.'), ('Stiff', 'Fast and slow scales together.'), ('Backward Euler', 'Implicit, very stable.'), ('System', 'Higher order → first order.')],
 'planet': {'text': ['NOAA says the GFS runs four times a day and forecasts up to 16 days ahead. The EMC page also describes a 3 km coupled research run that took about 40,000 seconds of computer time for each 24-hour forecast, using 233 nodes.',
                     'That is about 11.1 hours of computing per forecast day, so the model ran only about 2.16 times faster than real time. Each forecast is a time-stepping ODE and PDE solve, and the stable step size sets the cost.'],
            'site': [('Differential Equations', 'Differential_Equations.html'), ('GOES-19', 'GOES-19.html')],
            'src': [_GFS]},
 'res': [(_MIT10[0], _MIT10[1], 'Free MIT course.'), ('PhET: Projectile Motion', _PH + 'projectile-motion', 'Compare with your solver.')]})
UNITS.append(
{'id': 'u9', 'title': 'Partial Differential Equations: Finite Differences', 'weeks': 'Weeks 12–13',
 'summary': 'Grids and stencils, the explicit heat equation and its stability limit, implicit and Crank–Nicolson schemes, Laplace’s equation and iterative solution, the CFL condition for waves, and the cost of resolution.',
 'objectives': ['Write finite-difference stencils for the heat and Laplace equations.', 'Apply the explicit stability limit r ≤ ½.', 'Explain the CFL condition.', 'Estimate how cost grows with resolution.'],
 'concepts': ['Replace derivatives with differences on a grid. For u_t = αu_xx, the explicit scheme is u_i^{n+1} = u_i^n + r(u_{i+1}^n − 2u_i^n + u_{i−1}^n) with r = αΔt/Δx².',
              'The explicit heat scheme is stable only if r ≤ ½, so halving Δx forces Δt down by 4.',
              'Implicit and Crank–Nicolson schemes are stable for any Δt but need a linear solve each step.',
              'Laplace’s equation u_xx + u_yy = 0 gives a 5-point stencil; Jacobi or Gauss–Seidel (Unit 4) solve it.',
              'For waves and flow, the CFL condition c Δt/Δx ≤ 1 links time step to grid spacing. Refining a 2D-horizontal grid by a factor k costs about k² more columns and k more time steps.'],
 'eqs': [('r=\\frac{\\alpha\\Delta t}{\\Delta x^2}\\le\\frac12', 'Explicit heat stability'), ('u_{i,j}=\\tfrac14(u_{i+1,j}+u_{i-1,j}+u_{i,j+1}+u_{i,j-1})', 'Laplace 5-point'), ('\\frac{c\\Delta t}{\\Delta x}\\le1', 'CFL condition'), ('\\text{cost}\\propto k^3', 'Horizontal refinement by k')],
 'worked': [
  _w('Find the largest stable explicit time step for α = 1.0 × 10⁻⁴ m²/s and Δx = 0.01 m (sample values).', ['Δt ≤ 0.5Δx²/α.'], 'Δt ≤ 0.5 s.'),
  _w('NOAA plans to refine the GFS from 13 km to 9 km. Estimate the change in horizontal columns.', ['(13/9)².'], 'About 2.09 times as many columns.'),
  _w('Including a CFL-limited time step, estimate the total cost increase.', ['(13/9)³.'], 'About 3.01 times the work.')],
 'practice': [('Halve Δx in the explicit heat scheme. New Δt limit?', '¼ as large.'), ('Columns on a 13 km global grid (Earth 5.1 × 10⁸ km², textbook)?', 'About 3.02 million.'),
              ('Cells with 127 layers?', 'About 3.83 × 10⁸.'), ('Cells at 9 km with 127 layers?', 'About 8.0 × 10⁸.')],
 'misc': [('Any time step works if the grid is fine.', 'Finer grids need smaller explicit steps.'), ('Implicit schemes are always more accurate.', 'They are more stable, not automatically more accurate.'), ('Doubling resolution doubles cost.', 'In 2D plus time it is about 8×.')],
 'quiz': [_q('Explicit heat stability…', ['r ≤ ½', 'r ≤ 2', 'any r', 'r ≥ 1'], 0, 'Von Neumann.'), _q('CFL links…', ['Δt and Δx', 'α and u', 'n and ε', 'x and y'], 0, 'Information speed.'),
          _q('Laplace stencil uses … points.', ['5', '2', '9 always', '1'], 0, 'Centre + 4.'), _q('Crank–Nicolson is…', ['unconditionally stable', 'explicit', 'unstable', 'first order'], 0, 'Implicit average.')],
 'cards': [('Stencil', 'Pattern of neighbour points.'), ('r', 'αΔt/Δx².'), ('CFL', 'cΔt/Δx ≤ 1.'), ('Crank–Nicolson', 'Implicit, second order.'), ('5-point Laplacian', 'Average of neighbours.'), ('Resolution cost', '≈ k³ for k-fold refinement.')],
 'planet': {'text': ['NOAA’s 2023 supercomputer upgrade was meant to let the GFS move to a horizontal resolution of nine kilometres, compared with 13 in the current version, so smaller-scale features can be seen and simulated.',
                     'This unit’s scaling shows why that needed new computers: 2.09 times as many columns and, with a CFL-limited time step, about 3 times the work for every forecast.'],
            'site': [('Fluid Mechanics', 'Fluid_Mechanics.html'), ('Thermodynamics', 'Thermodynamics.html')],
            'src': [_WC, _GFS]},
 'res': [(_MIT2[0], _MIT2[1], 'Free MIT course.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u10', 'title': 'Optimization, Eigenvalues and Computing at Scale', 'weeks': 'Weeks 14–15',
 'summary': 'Golden-section search, gradient descent and Newton’s method for minimization, the power method for eigenvalues, flop counts, parallel computing, and verifying and validating models.',
 'objectives': ['Minimize a 1D function by golden-section search.', 'Apply gradient descent and choose a step.', 'Find a dominant eigenvalue by the power method.', 'Estimate run time from flop counts and machine speed.'],
 'concepts': ['Golden-section search shrinks a bracket by 0.618 each step without derivatives.',
              'Gradient descent steps downhill: x ← x − α∇f. Too large an α diverges; too small crawls.',
              'Newton’s method for minimization solves ∇f = 0 using the Hessian; it converges quadratically near the minimum.',
              'The power method repeatedly multiplies by A; the vector lines up with the dominant eigenvector, and the Rayleigh quotient gives its eigenvalue.',
              'Verification asks whether the code solves the equations right; validation asks whether they are the right equations, checked against observations.'],
 'eqs': [('\\tau=\\frac{\\sqrt5-1}{2}\\approx0.618', 'Golden ratio factor'), ('x_{k+1}=x_k-\\alpha\\nabla f(x_k)', 'Gradient descent'), ('\\lambda\\approx\\frac{v^TAv}{v^Tv}', 'Rayleigh quotient'), ('t=\\frac{\\text{flops}}{\\text{flop rate}}', 'Run time')],
 'worked': [
  _w('How much does golden-section search shrink a bracket in 10 steps?', ['0.618¹⁰.'], 'To 0.0081 (0.81%) of its width.'),
  _w('Minimize f = (x − 3)² by gradient descent with α = 0.1 from x = 0. Where are you after 5 steps?', ['Each step: x − 3 shrinks by 0.8.', 'x₅ = 3(1 − 0.8⁵).'], 'x₅ = 2.017.'),
  _w('Apply the power method to [[2, 1], [1, 2]] from (1, 0), 5 steps.', ['v = (122, 121).', 'Rayleigh quotient.'], 'λ ≈ 2.99997 (exact 3).')],
 'practice': [('How long does a 10,000-unknown dense solve (2n³/3 flops) take at 14.5 petaflops?', '6.67 × 10¹¹/1.45 × 10¹⁶ = 4.6 × 10⁻⁵ s.'), ('Combined speed of NOAA’s two 14.5-petaflop computers?', '29 petaflops.'),
              ('Operational plus research capacity (20 petaflops)?', '49 petaflops.'), ('Verification or validation: comparing a model with Mauna Loa data?', 'Validation.')],
 'misc': [('A bigger step always speeds gradient descent.', 'It can overshoot and diverge.'), ('The power method finds every eigenvalue.', 'Only the dominant one.'), ('A converged code is a correct model.', 'It still needs validation.')],
 'quiz': [_q('Golden section shrinks by…', ['0.618', '0.5', '0.1', '2'], 0, 'Golden ratio.'), _q('Power method finds…', ['dominant eigenvalue', 'all roots', 'the inverse', 'the determinant'], 0, 'Repeated multiplication.'),
          _q('Validation compares with…', ['observations', 'the code', 'nothing', 'epsilon'], 0, 'Reality check.'), _q('Gradient descent moves…', ['downhill', 'uphill', 'randomly', 'sideways'], 0, '−∇f.')],
 'cards': [('Golden section', 'Bracket shrinks by 0.618.'), ('Gradient descent', 'x − α∇f.'), ('Power method', 'Dominant eigenvalue.'), ('Rayleigh quotient', 'vᵀAv/vᵀv.'), ('Verification', 'Solving the equations right.'), ('Validation', 'Solving the right equations.')],
 'planet': {'text': ['NOAA reports that its twin weather and climate supercomputers, Dogwood in Manassas, Virginia, and Cactus in Phoenix, Arizona, were upgraded in August 2023 to 14.5 petaflops each, so together the forecast system can process 29 quadrillion calculations per second. With research machines totalling 20 petaflops, NOAA’s capacity is 49 petaflops, and over 20 operational numerical weather prediction models run on the system.',
                     'NASA GISS makes the code of its ModelE Earth system model freely available, and its GISTEMP surface-temperature analysis is updated about the 10th of every month. Open code and data let anyone verify and validate the numerical methods behind climate science.'],
            'site': [('Solutions', 'Solutions.html'), ('Intro to Programming', 'Intro_to_Programming.html')],
            'src': [_WC, _GISS, _GT]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_MIT10[0], _MIT10[1], 'Free MIT course.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Machine epsilon and Taylor series in a spreadsheet', 'week': 'Week 1',
 'goal': 'Find machine epsilon by experiment and watch a Taylor series converge to e.',
 'eq': ('e\\approx\\sum_{k=0}^{n-1}\\frac{1}{k!}', 'Taylor series for e'),
 'steps': ['In a column, start at 1 and halve each row.', 'In the next column, test whether 1 + value > 1.', 'The last value that passes is machine epsilon.', 'Sum 1/k! for 5 and 10 terms and compare with e.'],
 'table': (['Quantity', 'Value'], [['Machine epsilon (double)', '2.22 × 10⁻¹⁶'], ['e, 5 terms', '2.70833'], ['e, 10 terms', '2.7182815'], ['e', '2.7182818']]),
 'note': 'Computed values; most spreadsheets use double precision.',
 'calc': ['Halving 52 times gives 2⁻⁵² = 2.22 × 10⁻¹⁶.', '1 + 1 + ½ + ⅙ + 1/24 = 2.70833.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MIT[0], _MIT[1])],
 'planet': 'NOAA describes a forecast run with dynamics in 32-bit and everything else in 64-bit precision.', 'planet_src': [_GFS]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Bisection versus Newton', 'week': 'Week 3',
 'goal': 'Solve cos x = x by bisection and by Newton’s method and count the correct digits each step.',
 'eq': ('x_{n+1}=x_n-\\frac{\\cos x_n-x_n}{-\\sin x_n-1}', 'Newton for cos x − x = 0'),
 'steps': ['Bracket the root in [0, 1].', 'Run 20 bisection steps in a spreadsheet.', 'Run Newton from x₀ = 1.', 'Plot log₁₀ of the error against the step number for both.'],
 'table': (['Newton step', 'x'], [['1', '0.750364'], ['2', '0.739113'], ['3', '0.739085133'], ['4', '0.739085133']]),
 'note': 'Computed values. Bisection needs about 20 steps for 6 digits; Newton needs 3.',
 'calc': ['x₁ = 1 − (cos 1 − 1)/(−sin 1 − 1) = 0.750364.', 'Root 0.7390851.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_ONM[0], _ONM[1])],
 'planet': 'The USGS says MODFLOW-NWT uses a Newton-Raphson formulation for unconfined groundwater flow.', 'planet_src': [_MF]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Fitting the Mauna Loa CO₂ record', 'week': 'Week 7',
 'goal': 'Fit straight-line and quadratic models to NOAA’s Mauna Loa annual means and judge them by their residuals.',
 'eq': ('A^TA\\,c=A^Ty', 'Least squares'),
 'steps': ['Explore PhET Least-Squares Regression and Curve Fitting to see how residuals change with the model.', 'Open NOAA’s annual-mean file and copy the 1960–2020 decade values.', 'Fit a line and a quadratic (spreadsheet LINEST or trendline).', 'Predict 2025 and compare with NOAA’s 427.35 ppm.'],
 'table': (['Model', 'Key coefficient', '2025 prediction (ppm)'], [['Line', 'slope 1.613 ppm/yr', '415.0'], ['Quadratic', '0.01338 ppm/yr²', '426.0'], ['NOAA 2025', '—', '427.35']]),
 'note': 'Data from NOAA GML; fits computed.',
 'calc': ['The line underpredicts 2025 by 12.3 ppm.', 'The quadratic is within 1.3 ppm.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('PhET: Least-Squares Regression', _PH + 'least-squares-regression'), ('PhET: Curve Fitting', _PH + 'curve-fitting'), (_MLOD[0], _MLOD[1])],
 'planet': 'NOAA reports the Mauna Loa monthly mean was 426.07 ppm in September 2026.', 'planet_src': [_MLO]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Trapezoid versus Simpson', 'week': 'Week 9',
 'goal': 'Integrate sin x from 0 to π with both rules, halve the step and measure the error order.',
 'eq': ('\\int_0^{\\pi}\\sin x\\,dx=2', 'Test integral'),
 'steps': ['Use PhET Calculus Grapher to see the area under a curve.', 'Build columns for x, sin x and the rule weights.', 'Compute T and S for n = 4, then n = 8.', 'Find the error ratios.'],
 'table': (['Rule, n = 4', 'Estimate', 'Error'], [['Trapezoidal', '1.89612', '−0.10388'], ['Simpson', '2.00456', '+0.00456']]),
 'note': 'Computed values; doubling to n = 8 cuts the errors by 4.03 and 16.9, close to the theoretical 4 and 16.',
 'calc': ['T₄ = (π/4)(sin π/4 + sin π/2 + sin 3π/4) = 1.89612.', 'S₄ = (π/12)(4 sin π/4 + 2 sin π/2 + 4 sin 3π/4) = 2.00456.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('PhET: Calculus Grapher', _PH + 'calculus-grapher'), (_OSI[0], _OSI[1])],
 'planet': 'NOAA builds each Mauna Loa monthly mean from daily means based on hourly averages.', 'planet_src': [_MLO]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Euler and RK4 error orders', 'week': 'Week 11',
 'goal': 'Solve y′ = −y to t = 1 with several step sizes and confirm first- and fourth-order convergence.',
 'eq': ('y(1)=e^{-1}=0.367879', 'Exact answer'),
 'steps': ['Build an Euler column for h = 0.2, 0.1 and 0.05.', 'Build an RK4 block for h = 0.2 and 0.1.', 'Record the error at t = 1.', 'Compare the error ratios when h halves; then try the same solver on PhET Projectile Motion’s no-drag case.'],
 'table': (['Method, h', 'Error at t = 1'], [['Euler, 0.2', '−0.0402'], ['Euler, 0.1', '−0.0192'], ['Euler, 0.05', '−0.00939'], ['RK4, 0.2', '5.80 × 10⁻⁶'], ['RK4, 0.1', '3.33 × 10⁻⁷']]),
 'note': 'Computed values. Euler’s error halves with h; RK4’s falls by about 17 (near 2⁴ = 16).',
 'calc': ['Euler h = 0.1: 0.9¹⁰ − e⁻¹ = −0.0192.', 'RK4 ratio 5.80 × 10⁻⁶/3.33 × 10⁻⁷ = 17.4.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('PhET: Projectile Motion', _PH + 'projectile-motion'), (_MIT10[0], _MIT10[1])],
 'planet': 'NOAA’s GFS runs four times a day, forecasting up to 16 days ahead.', 'planet_src': [_GFS]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: The heat equation and its stability limit', 'week': 'Week 13',
 'goal': 'Run the explicit heat scheme on a rod with a hot spot and see what happens above r = ½.',
 'eq': ('u_i^{n+1}=u_i^n+r(u_{i+1}^n-2u_i^n+u_{i-1}^n)', 'Explicit scheme'),
 'steps': ['Set 7 nodes with ends at 0 and the middle node at 100 (sample values).', 'Step with r = 0.25 for 10 steps.', 'Repeat with r = 0.6.', 'Describe both results.'],
 'table': (['Case', 'Middle value after 1 step', 'After 10 steps'], [['r = 0.25', '50.0', '16.7'], ['r = 0.6', '−20.0', '290.5']]),
 'note': 'Computed values. With r = 0.6 the values oscillate and grow: the scheme is unstable.',
 'calc': ['r = 0.25: 100 + 0.25(0 − 200 + 0) = 50.', 'r = 0.6: 100 + 0.6(−200) = −20.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MIT2[0], _MIT2[1])],
 'planet': 'NOAA planned to move the GFS from 13 km to 9 km resolution after its 2023 upgrade.', 'planet_src': [_WC]})
SCHEDULE = [(1, 'u1', 'Errors, floating point, Taylor series; Lab A', 'MIT 18.330'), (2, 'u2', 'Bisection and fixed-point iteration', 'MIT 18.330'),
            (3, 'u2', 'Newton and secant methods; Lab B', 'OpenStax Calculus 1, 4.9'), (4, 'u3', 'Gaussian elimination, LU and conditioning', 'MIT 2.086'),
            (5, 'u4', 'Jacobi, Gauss–Seidel and sparse systems', 'MIT 18.330'), (6, 'u5', 'Interpolation and splines', 'MIT 18.330'),
            (7, 'u5', 'Least squares; Lab C; midterm practice', 'NOAA GML'), (8, 'u6', 'Numerical differentiation', 'MIT 18.330'),
            (9, 'u7', 'Numerical integration; Lab D', 'OpenStax Calculus 2, 3.6'), (10, 'u8', 'Euler, Heun and RK4', 'MIT 10.34'),
            (11, 'u8', 'Stability, stiffness and systems; Lab E', 'MIT 10.34'), (12, 'u9', 'Finite differences for the heat equation', 'MIT 2.086'),
            (13, 'u9', 'Laplace, waves and CFL; Lab F', 'NOAA EMC'), (14, 'u10', 'Optimization and the power method', 'MIT 18.330'),
            (15, 'u10', 'Computing at scale, verification and validation; final practice', 'NOAA; NASA GISS')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Find the relative error of 3.14 as an approximation to π.', ['|3.14 − π|/π.'], '5.07 × 10⁻⁴.'),
  ('Take two Newton steps on x² − 5 from x₀ = 2.', ['x₁ = 2 − (−1)/4.', 'x₂ = 2.25 − 0.0625/4.5.'], 'x₁ = 2.25; x₂ = 2.23611.'),
  ('How many bisection steps shrink a width-4 bracket below 10⁻³?', ['log₂(4000) = 11.97.'], '12 steps.'),
  ('How much more elimination work is n = 500 than n = 100?', ['(500/100)³.'], '125 times.'),
  ('Interpolate Mauna Loa CO₂ for 2023 from NOAA’s 2020 (414.21) and 2025 (427.35) annual means.', ['414.21 + 0.6 × 13.14.'], '422.09 ppm (NOAA’s 2023 value is 421.08).')]),
 ('Final practice set (all units)', [
  ('Estimate ∫₀² x² dx with the trapezoidal rule, n = 2.', ['h = 1: 0.5 × 0 + 1 + 0.5 × 4.'], '3 (exact 2.667).'),
  ('Repeat with Simpson’s rule, n = 2.', ['(1/3)(0 + 4 + 4).'], '2.667, exact for a quadratic.'),
  ('Take two Euler steps of h = 0.1 on y′ = −2y, y(0) = 1.', ['0.8².'], '0.64 (exact 0.670).'),
  ('Find the largest explicit heat time step for α = 2 × 10⁻⁵ m²/s, Δx = 0.005 m.', ['0.5 × 0.005²/2 × 10⁻⁵.'], '0.625 s.'),
  ('Estimate the derivative of eˣ at 0 by central difference, h = 0.01.', ['(e^0.01 − e^−0.01)/0.02.'], '1.0000167.'),
  ('How much does golden-section search shrink a bracket in 20 steps?', ['0.618²⁰.'], 'To 6.6 × 10⁻⁵ of its width.')])]
FORMULAS = ['e_{rel}=|\\tilde x-x|/|x|,\\ \\varepsilon_{mach}=2^{-52}', 'x_{n+1}=x_n-f(x_n)/f\'(x_n),\\ n\\ge\\log_2((b-a)/tol)', 'A=LU,\\ \\text{cost}\\approx\\tfrac23n^3,\\ \\kappa=\\|A\\|\\|A^{-1}\\|', '\\|e_k\\|\\approx\\rho^k\\|e_0\\|',
            'A^TAc=A^Ty', 'f\'\\approx(f(x+h)-f(x-h))/(2h),\\ h_{opt}\\approx\\sqrt{\\varepsilon}', 'T_n:\\ E\\propto h^2,\\ S_n:\\ E\\propto h^4', 'y_{n+1}=y_n+hf,\\ h<2/\\lambda',
            'r=\\alpha\\Delta t/\\Delta x^2\\le\\tfrac12,\\ c\\Delta t/\\Delta x\\le1', 'x_{k+1}=x_k-\\alpha\\nabla f,\\ \\lambda\\approx v^TAv/v^Tv']
GLOSSARY = sorted([('Absolute error', 'Size of the difference from the true value.'), ('Bisection', 'Root finding by halving a sign-change bracket.'), ('CFL condition', 'Time-step limit cΔt/Δx ≤ 1.'), ('Catastrophic cancellation', 'Digit loss when subtracting close numbers.'),
    ('Condition number', 'How much a problem amplifies input errors.'), ('Crank–Nicolson', 'Implicit second-order time scheme.'), ('Diagonal dominance', 'Each diagonal entry outweighs the rest of its row.'), ('Gauss–Seidel', 'Iterative solver using new values at once.'),
    ('Gaussian quadrature', 'Integration with optimal points and weights.'), ('Least squares', 'Fit minimizing the sum of squared residuals.'), ('LU factorization', 'A = LU, reusable elimination.'), ('Machine epsilon', 'Gap between 1 and the next float.'),
    ('Newton’s method', 'Root finding along tangent lines.'), ('Power method', 'Repeated multiplication to find the dominant eigenvalue.'), ('Runge–Kutta (RK4)', 'Fourth-order ODE solver.'), ('Simpson’s rule', 'Fourth-order integration with parabolas.'),
    ('Spline', 'Smooth piecewise cubic curve.'), ('Stiff equation', 'ODE with very fast and very slow parts.'), ('Truncation error', 'Error from cutting off an infinite process.'), ('Validation', 'Checking a model against observations.')])
RUBRIC = [('4 · Mastery', 'Chooses a method for the accuracy needed, tests it on a problem with a known answer, measures its order, and explains its stability limits.'), ('3 · Proficient', 'Solves the practice problems with occasional slips in step size or units.'),
          ('2 · Developing', 'Follows worked examples but cannot tell truncation from rounding error.'), ('1 · Beginning', 'Runs formulas without checking error or stability; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def _fit(xs, ys, deg):
    n = deg + 1
    M = [[sum(x ** (i + j) for x in xs) for j in range(n)] for i in range(n)]
    v = [sum(y * x ** i for x, y in zip(xs, ys)) for i in range(n)]
    for c in range(n):
        for r_ in range(c + 1, n):
            f = M[r_][c] / M[c][c]
            M[r_] = [a - f * b for a, b in zip(M[r_], M[c])]; v[r_] -= f * v[c]
    out = [0] * n
    for i in range(n - 1, -1, -1):
        out[i] = (v[i] - sum(M[i][j] * out[j] for j in range(i + 1, n))) / M[i][i]
    return out
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    eps = 2 ** -52; e1 = exp(-1)
    f = lambda x: x ** 3 - x - 2
    def bis(a, b, k):
        for _ in range(k):
            m = (a + b) / 2
            if f(a) * f(m) <= 0: b = m
            else: a = m
        return (a + b) / 2
    def newt(g, dg, x, k):
        for _ in range(k): x = x - g(x) / dg(x)
        return x
    sq = lambda x: x * x - 2; dsq = lambda x: 2 * x
    def sec(k):
        x0, x1 = 1.0, 2.0
        for _ in range(k): x0, x1 = x1, x1 - sq(x1) * (x1 - x0) / (sq(x1) - sq(x0))
        return x1
    def jac(k):
        x = y = 0
        for _ in range(k): x, y = (1 - y) / 4, (2 - x) / 3
        return x, y
    def gs(k):
        x = y = 0
        for _ in range(k): x = (1 - y) / 4; y = (2 - x) / 3
        return x, y
    b_ = 1.0001  # matrix [[1, 1], [1, b_]]
    tr = 1 + b_ * b_ + 2; det = b_ - 1
    smax = sqrt((tr + sqrt(tr * tr - 4 * det * det)) / 2); smin = abs(det) / smax
    yrs = [0, 10, 20, 30, 40, 50, 60]; co = [316.91, 325.68, 338.76, 354.45, 369.71, 390.10, 414.21]
    L = _fit(yrs, co, 1); Q = _fit(yrs, co, 2)
    pl = lambda c, t: sum(ci * t ** i for i, ci in enumerate(c))
    fd = (sin(1.1) - sin(1)) / .1; cd = (sin(1.1) - sin(.9)) / .2
    def trap(g, a, b, n):
        h = (b - a) / n; return h * (0.5 * g(a) + sum(g(a + i * h) for i in range(1, n)) + 0.5 * g(b))
    def simp(g, a, b, n):
        h = (b - a) / n; return h / 3 * (g(a) + g(b) + sum((4 if i % 2 else 2) * g(a + i * h) for i in range(1, n)))
    ex = e - 1; gp = 1 / sqrt(3); G2 = 0.5 * (exp(.5 - .5 * gp) + exp(.5 + .5 * gp))
    def rk4(h, n):
        y = 1.0
        for _ in range(n):
            k1 = -y; k2 = -(y + h / 2 * k1); k3 = -(y + h / 2 * k2); k4 = -(y + h * k3); y += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return y
    T = 90.0
    for _ in range(10): T -= 0.1 * (T - 20)
    def heat(r, k):
        u = [0, 0, 0, 100, 0, 0, 0]
        for _ in range(k): u = [0] + [u[i] + r * (u[i + 1] - 2 * u[i] + u[i - 1]) for i in range(1, 6)] + [0]
        return u
    gold = (sqrt(5) - 1) / 2
    v = [1.0, 0.0]
    for _ in range(5): v = [2 * v[0] + v[1], v[0] + 2 * v[1]]
    Av = [2 * v[0] + v[1], v[0] + 2 * v[1]]; ray = (v[0] * Av[0] + v[1] * Av[1]) / (v[0] ** 2 + v[1] ** 2)
    xn = 1.0
    for _ in range(3): xn = xn - (cos(xn) - xn) / (-sin(xn) - 1)
    r = [
     ('u1 eps', eps, 2.22e-16), ('u1 eps32', 2 ** -23, 1.19e-7), ('u1 227', abs(22 / 7 - pi), .001264), ('u1 227r', abs(22 / 7 - pi) / pi, 4.02e-4), ('u1 sum', 0.1 + 0.2 - 0.3, 5.55e-17),
     ('u1 canc', 1 / (sqrt(1e8 + 1) + sqrt(1e8)), 4.99999999875e-5), ('u1 canc2', 1 / (sqrt(1e8 + 1) + sqrt(1e8)), 5.0e-5), ('u1 t2', exp(.1) - 1.1, .00517), ('u1 t2e', .1 ** 2 / 2, .005), ('u1 t3', exp(.1) - 1.105, 1.71e-4),
     ('u2 m1', (1 + 2) / 2, 1.5), ('u2 m2', 1.75, (1.5 + 2) / 2), ('u2 m3', (1.5 + 1.75) / 2, 1.625), ('u2 root', bis(1, 2, 40), 1.5214), ('u2 f1', f(1), -2), ('u2 f2', f(2), 4), ('u2 st', ceil(log2(1e6)), 20), ('u2 st2', log2(1e6), 19.93),
     ('u2 n1', newt(sq, dsq, 1, 1), 1.5), ('u2 n2', newt(sq, dsq, 1, 2), 1.41667), ('u2 n3', newt(sq, dsq, 1, 3), 1.414216), ('u2 nc', newt(f, lambda x: 3 * x * x - 1, 1.5, 1), 1.52174),
     ('u2 s1', sec(1), 1.3333), ('u2 s2', sec(2), 1.4), ('u2 s3', sec(3), 1.4146), ('u2 ord', (1 + sqrt(5)) / 2, 1.618),
     ('u3 x', 2, 2), ('u3 chk1', 2 * 2 + 3 - (-1), 8), ('u3 chk2', -3 * 2 - 3 + 2 * -1, -11), ('u3 chk3', -2 * 2 + 3 + 2 * -1, -3), ('u3 ops', 2 * 1000 ** 3 / 3, 6.67e8), ('u3 cond', smax / smin, 40002),
     ('u3 8', (2000 / 1000) ** 3, 8), ('u3 18', 2 * 27 / 3, 18), ('u3 dig', 16 - 8, 8),
     ('u4 j1x', jac(1)[0], .25), ('u4 j1y', jac(1)[1], .6667), ('u4 j2x', jac(2)[0], .0833), ('u4 j2y', jac(2)[1], .5833), ('u4 ex', 1 / 11, .0909), ('u4 ey', 7 / 11, .6364),
     ('u4 g1y', gs(1)[1], .5833), ('u4 g2x', gs(2)[0], .1042), ('u4 g2y', gs(2)[1], .6319), ('u4 g3x', gs(3)[0], .0920), ('u4 g3y', gs(3)[1], .6360),
     ('u4 rj', sqrt(1 / 12), .289), ('u4 rg', 1 / 12, .0833), ('u4 r6', (1 / 12) ** 6, 3.35e-7), ('u4 col', 5.1e8 / 13 ** 2, 3.0e6), ('u4 cell', 5.1e8 / 13 ** 2 * 127, 383e6),
     ('u5 int', 390.10 + .5 * (414.21 - 390.10), 402.16), ('u5 d', 414.21 - 390.10, 24.11), ('u5 sl', L[1], 1.613), ('u5 p25', pl(L, 65), 415.0), ('u5 q0', Q[0], 316.84), ('u5 q1', Q[1], .810), ('u5 q2', Q[2], .01338),
     ('u5 qp', pl(Q, 65), 426.0), ('u5 r1', (414.21 - 390.10) / 10, 2.41), ('u5 r2', (390.10 - 369.71) / 10, 2.04), ('u5 sep', 426.07 - 424.37, 1.70),
     ('u6 fd', fd, .4974), ('u6 c1', cos(1), .5403), ('u6 fe', fd - cos(1), -.0429), ('u6 cd', cd, .5394), ('u6 ce', cd - cos(1), -.00090), ('u6 rat', (fd - cos(1)) / (cd - cos(1)), 47.7),
     ('u6 ho', sqrt(eps), 1.49e-8), ('u6 hc', eps ** (1 / 3), 6.06e-6), ('u6 hc2', eps ** (1 / 3), 6.06e-6), ('u6 hs', sqrt(eps), 1.49e-8),
     ('u7 T4', trap(exp, 0, 1, 4), 1.72722), ('u7 ex', ex, 1.71828), ('u7 T4e', trap(exp, 0, 1, 4) - ex, .00894), ('u7 S4', simp(exp, 0, 1, 4), 1.718319), ('u7 S4e', simp(exp, 0, 1, 4) - ex, 3.70e-5),
     ('u7 G', G2, 1.717896), ('u7 Ge', G2 - ex, -3.85e-4), ('u7 T8e', trap(exp, 0, 1, 8) - ex, .00224), ('u7 R', trap(exp, 0, 1, 8) + (trap(exp, 0, 1, 8) - trap(exp, 0, 1, 4)) / 3, 1.718284), ('u7 S2', simp(exp, 0, 1, 2), 1.718861),
     ('u8 eu', .9 ** 10, .34868), ('u8 ex', e1, .36788), ('u8 ee', .9 ** 10 - e1, -.0192), ('u8 k2', -(1 - .05), -.95), ('u8 k3', -(1 + .05 * -.95), -.9525), ('u8 k4', -(1 + .1 * -.9525), -.90475),
     ('u8 rk', rk4(.1, 1), .9048375), ('u8 rkx', exp(-.1), .9048374), ('u8 cool', T, 44.41), ('u8 coolx', 20 + 70 * e1, 45.75), ('u8 e05', .95 ** 20, .35849), ('u8 st', 2 / 50, .04), ('u8 heun', 1 + .05 * (-1 - (1 - .1)), .905),
     ('u8 ufs', 40000 / 3600, 11.1), ('u8 rt', 86400 / 40000, 2.16),
     ('u9 dt', .5 * .01 ** 2 / 1e-4, .5), ('u9 col', (13 / 9) ** 2, 2.09), ('u9 cost', (13 / 9) ** 3, 3.01), ('u9 q', .5 ** 2, .25), ('u9 c13', 5.1e8 / 169, 3.02e6), ('u9 cell13', 5.1e8 / 169 * 127, 3.83e8), ('u9 cell9', 5.1e8 / 81 * 127, 8.0e8), ('u9 8x', 2 ** 3, 8),
     ('u10 g', gold, .618), ('u10 g10', gold ** 10, .0081), ('u10 gd', 3 * (1 - .8 ** 5), 2.017), ('u10 v0', v[0], 122), ('u10 v1', v[1], 121), ('u10 ray', ray, 2.99997),
     ('u10 t', 2 * 1e4 ** 3 / 3 / 14.5e15, 4.6e-5), ('u10 fl', 2 * 1e4 ** 3 / 3, 6.67e11), ('u10 29', 2 * 14.5, 29), ('u10 49', 29 + 20, 49),
     ('labA e5', sum(1 / _fa(k) for k in range(5)), 2.70833), ('labA e10', sum(1 / _fa(k) for k in range(10)), 2.7182815), ('labA e', e, 2.7182818), ('labA eps', eps, 2.22e-16),
     ('labB 1', newt(lambda x: cos(x) - x, lambda x: -sin(x) - 1, 1, 1), .750364), ('labB 2', newt(lambda x: cos(x) - x, lambda x: -sin(x) - 1, 1, 2), .739113), ('labB 3', xn, .739085133), ('labB r', xn, .7390851), ('labB 20', ceil(log2(1e6)), 20),
     ('labC sl', L[1], 1.613), ('labC lp', pl(L, 65), 415.0), ('labC q2', Q[2], .01338), ('labC qp', pl(Q, 65), 426.0), ('labC u', 427.35 - pl(L, 65), 12.3), ('labC w', 427.35 - pl(Q, 65), 1.3),
     ('labD T', trap(sin, 0, pi, 4), 1.89612), ('labD Te', trap(sin, 0, pi, 4) - 2, -.10388), ('labD S', simp(sin, 0, pi, 4), 2.00456), ('labD Se', simp(sin, 0, pi, 4) - 2, .00456),
     ('labD Tr', (trap(sin, 0, pi, 4) - 2) / (trap(sin, 0, pi, 8) - 2), 4.03), ('labD Sr', (simp(sin, 0, pi, 4) - 2) / (simp(sin, 0, pi, 8) - 2), 16.9),
     ('labE e2', .8 ** 5 - e1, -.0402), ('labE e1', .9 ** 10 - e1, -.0192), ('labE e05', .95 ** 20 - e1, -.00939), ('labE r2', rk4(.2, 5) - e1, 5.80e-6), ('labE r1', rk4(.1, 10) - e1, 3.33e-7),
     ('labE rr', (rk4(.2, 5) - e1) / (rk4(.1, 10) - e1), 17.4), ('labE x', e1, .367879),
     ('labF a1', heat(.25, 1)[3], 50), ('labF a10', heat(.25, 10)[3], 16.7), ('labF b1', heat(.6, 1)[3], -20), ('labF b10', heat(.6, 10)[3], 290.5),
     ('mid 1', abs(3.14 - pi) / pi, 5.07e-4), ('mid 2a', newt(lambda x: x * x - 5, lambda x: 2 * x, 2, 1), 2.25), ('mid 2b', newt(lambda x: x * x - 5, lambda x: 2 * x, 2, 2), 2.23611), ('mid 3', log2(4000), 11.97), ('mid 3c', ceil(log2(4000)), 12),
     ('mid 4', (500 / 100) ** 3, 125), ('mid 5', 414.21 + .6 * (427.35 - 414.21), 422.09), ('mid 5d', 427.35 - 414.21, 13.14),
     ('fin 1', trap(lambda x: x * x, 0, 2, 2), 3), ('fin 1x', 8 / 3, 2.667), ('fin 2', simp(lambda x: x * x, 0, 2, 2), 2.667), ('fin 3', .8 ** 2, .64), ('fin 3x', exp(-.4), .670),
     ('fin 4', .5 * .005 ** 2 / 2e-5, .625), ('fin 5', (exp(.01) - exp(-.01)) / .02, 1.0000167), ('fin 6', gold ** 20, 6.6e-5),
     ('x ml', 427.35 - 316.91, 110.44), ('x pf', 14.5 / 12.1, 1.198), ('x days', 16 * 4, 64), ('x rk', 2 ** 4, 16), ('x ln', 0.9 ** 2, .81), ('x hr', 120 / 24, 5), ('x sp', 1 / 2 ** 23, 1.19e-7), ('x lin', 427.35 - 415.007, 12.34), ('x qd', 427.35 - 426.045, 1.3)]
    return r
def _fa(k):
    out = 1
    for i in range(2, k + 1): out *= i
    return out
