"""Linear Algebra (MATH 230): vectors, systems of equations, matrix algebra, input-output models, vector spaces, orthogonality and least squares, determinants, eigenvalues, Markov chains and the SVD.
Oct 25 2026, founder-approved four-year track, sophomore course 7. Same module fields as statics.py / mom.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, log, log10
ID = 'linalg'
STATUS = 'live'
YEAR = 2
PAGE = 'Linear_Algebra.html'
CODE = 'MATH 230'
TITLE = 'Linear Algebra'
LAB_NAME = 'Computation lab'
TAGLINE = 'Vectors, matrices and systems of equations: elimination, LU, inverses, input–output models, the four fundamental subspaces, projections and least squares, determinants, eigenvalues, Markov chains and the SVD, with six labs. Free, self-paced, and tied to GPS, Landsat, sea-level satellites, weather models, recycling and mineral mapping.'
DESC = 'Free self-study Linear Algebra: 10 units, worked examples, solved practice, quizzes, flashcards, 6 spreadsheet and home labs, practice exams, tied to GPS, Landsat and sea-level data.'
ALT = 'NASA photo of the Landsat 9 launch'
_ILA = 'https://textbooks.math.gatech.edu/ila/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 18.06 Linear Algebra (Strang, Spring 2010)', 'https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/')
_MITSC = ('MIT OpenCourseWare 18.06SC Linear Algebra (self-paced, Fall 2011)', 'https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/')
_HEF = ('Jim Hefferon, Linear Algebra (free text)', 'https://hefferon.net/linearalgebra/')
_GS = ('Gilbert Strang, Introduction to Linear Algebra (book site)', 'https://math.mit.edu/~gs/linearalgebra/')
_GPSS = ('GPS.gov: Space segment', 'https://www.gps.gov/space-segment')
_GPST = ('GPS.gov: Trilateration (NOAA classroom activity)', 'https://www.gps.gov/trilateration')
_L9 = ('USGS: Landsat 9', 'https://www.usgs.gov/landsat-missions/landsat-9')
_NOAA = ('NOAA: NOAA completes upgrade to weather and climate supercomputer system (Aug. 10, 2023)', 'https://www.noaa.gov/news-release/noaa-completes-upgrade-to-weather-and-climate-supercomputer-system')
_EIO = ('U.S. EPA: US Environmentally-Extended Input-Output (USEEIO) models', 'https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-models')
_SL = ('NASA: Global mean sea level (Vital Signs)', 'https://sealevel.nasa.gov/vital-signs/global-mean-sea-level/')
_BLD = ('USGS: Preliminary study of correlation of natural periods and damping percentages of tall buildings in several countries (Çelebi, 2022)', 'https://www.usgs.gov/publications/preliminary-study-correlation-natural-periods-and-damping-percentages-tall-buildings')
_MSW = ('U.S. EPA: National overview, facts and figures on materials, wastes and recycling', 'https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/national-overview-facts-and-figures-materials')
_EMIT = ('NASA JPL: EMIT, Earth Surface Mineral Dust Source Investigation', 'https://earth.jpl.nasa.gov/emit/')
BANNER = ['images/Landsat9_Launch_KLS04_0013.jpg', 'images/GRACE_FO_Orbit.jpg', 'images/SWOT_Orbit_Illustration.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg']
CREDITS = {'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)', 'images/GRACE_FO_Orbit.jpg': 'NASA/JPL-Caltech (PIA22431)',
           'images/SWOT_Orbit_Illustration.jpg': 'CNES (PIA25623)', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester sophomore linear algebra course. It is modeled on the topics and depth of MIT 18.06 Linear Algebra taught by Gilbert Strang (free on MIT OpenCourseWare), and on the Georgia Tech and Purdue sophomore linear algebra courses, using the free Georgia Tech text Interactive Linear Algebra by Dan Margalit and Joseph Rabinoff and Jim Hefferon’s free Linear Algebra, which we link where it helps. None of those authors or schools endorses this page.',
         'What we add: every unit ties to real planet work with a cited public source (GPS, Landsat 9, NASA sea-level satellites, NOAA weather supercomputers, EPA input–output and recycling data, USGS building studies, NASA’s EMIT mineral spectrometer), every number on the page is re-computed by a checking script before it goes live, and every lab runs in a free spreadsheet or on paper.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Linear algebra is the language of data about the planet. A satellite pixel is a vector, a GPS fix is the solution of a linear system, a weather forecast is millions of equations solved again and again, and an economy’s pollution can be traced with one matrix.',
                 'The same few ideas, elimination, projection, eigenvalues and the SVD, turn raw measurements into maps of forests, sea-level trends and mineral dust. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values.']
PREREQS = ['High-school algebra: solving two equations in two unknowns, and working with functions.', 'Calculus I helps with limits and derivatives in a few examples, but no calculus is needed for most of the course.',
           'Comfort with a spreadsheet; Intro to Programming helps for the optional Python versions of the labs.', 'Calculus III and Differential Equations pair well with this course but are not required.']
STUDY = ['Do every computation by hand first on small (2 × 2 and 3 × 3) examples, then check it with a spreadsheet or calculator.', 'Think of Ax two ways: as dot products of the rows with x, and as a combination of the columns of A.',
         'Check every answer: plug x back into Ax = b, multiply A by its inverse, or test Av = λv.', 'Keep track of sizes: an m × n matrix times an n × p matrix gives m × p, and sizes that do not match mean an error.',
         'Draw pictures in 2D and 3D: lines, planes, projections and stretches make the rules easy to remember.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer with free spreadsheet software (its MMULT, MINVERSE, MDETERM and LINEST functions do matrix work).', 'Graph paper, a ruler, a protractor and a pencil.',
            'Optional: free Python with NumPy for the larger versions of the labs.', 'A string and push pins or tape for the trilateration lab, and a printed map or sheet of paper.',
            'A grayscale photo or a small grid of numbers for the image-compression lab.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free spreadsheet or on paper; Python versions are optional. Take regular breaks from the screen, and handle pins and scissors with care.']
SAFETY_SRC = ('OSHA: Computer workstations eTool', 'https://www.osha.gov/etools/computer-workstations')
CONST_SRC = ('NIST Guide to the SI, Appendix B.9: conversion factors', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9')
CONSTANTS = [('Speed of light (used for GPS ranges)', '299,792,458 m/s'), ('1 mile', '1.609344 km'), ('1 foot', '0.3048 m'), ('1 inch', '25.4 mm'),
             ('Flops to solve an n × n system by elimination', 'about n³/3 multiply–adds (Strang)'), ('Identity matrix I', 'Ones on the diagonal, zeros elsewhere: AI = IA = A')]
REF_TITLE = 'Free texts and lectures'
REF_INTRO = 'Use these free textbooks, lectures and tools alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Strang’s full video lectures, problem sets and exams.'), (_MITSC[0], _MITSC[1], 'Self-paced version with recitation videos and worked problems.'),
          ('Interactive Linear Algebra (Margalit and Rabinoff, Georgia Tech)', _ILA, 'Free interactive textbook used at Georgia Tech.'), (_HEF[0], _HEF[1], 'Free full textbook with answers.'),
          (_GS[0], _GS[1], 'Strang’s book site with notes and figures.'), ('PhET: Vector Addition', _PH + 'vector-addition', 'Interactive vectors and components.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Vectors: Linear Combinations, Lengths and Dot Products', 'weeks': 'Weeks 1–2',
 'summary': 'Vectors in two, three and n dimensions, adding and scaling them, linear combinations and span, length, unit vectors, the dot product, the angle between vectors, orthogonality and the Cauchy–Schwarz and triangle inequalities.',
 'objectives': ['Add, scale and combine vectors by hand and in pictures.', 'Compute lengths, unit vectors and dot products.', 'Find the angle between two vectors and test for orthogonality.', 'Describe the span of one, two or three vectors.'],
 'concepts': ['A vector in ℝⁿ is an ordered list of n numbers. In 2D and 3D it is an arrow; in higher dimensions it is a list, such as the 11 band values of one satellite pixel.',
              'A linear combination c₁v₁ + c₂v₂ + … scales vectors and adds them. The span is the set of all linear combinations: a line, a plane or all of space.',
              'Length ‖v‖ = √(v·v). Dividing by the length gives a unit vector u = v/‖v‖ with length 1.',
              'Dot product v·w = v₁w₁ + v₂w₂ + … = ‖v‖‖w‖cos θ. If v·w = 0 the vectors are orthogonal (perpendicular).',
              'Cauchy–Schwarz: |v·w| ≤ ‖v‖‖w‖. Triangle inequality: ‖v + w‖ ≤ ‖v‖ + ‖w‖.'],
 'eqs': [('\\|v\\|=\\sqrt{v_1^2+v_2^2+\\cdots+v_n^2}', 'Length'), ('v\\cdot w=v_1w_1+\\cdots+v_nw_n', 'Dot product'), ('\\cos\\theta=\\frac{v\\cdot w}{\\|v\\|\\,\\|w\\|}', 'Angle between vectors'), ('|v\\cdot w|\\le\\|v\\|\\,\\|w\\|', 'Cauchy–Schwarz inequality')],
 'worked': [
  {'q': 'Find the length of v = (3, 4) and the unit vector in its direction.', 'steps': ['‖v‖ = √(3² + 4²) = √25 = 5.', 'u = v/5.'], 'a': '‖v‖ = 5, u = (0.6, 0.8).'},
  {'q': 'Find the angle between v = (3, 4) and w = (1, 2).', 'steps': ['v·w = 3 + 8 = 11.', '‖v‖ = 5, ‖w‖ = √5 = 2.236.', 'cos θ = 11/(5 × 2.236) = 0.9839.'], 'a': 'θ = 10.30°.'},
  {'q': 'Write 2(1, 0, 1) + 3(0, 1, 1) as one vector. Is (2, 3, 4) in the span of these two vectors?', 'steps': ['2(1, 0, 1) + 3(0, 1, 1) = (2, 3, 5).', 'Any combination c₁(1, 0, 1) + c₂(0, 1, 1) = (c₁, c₂, c₁ + c₂), so the third entry must equal the sum of the first two.'], 'a': '(2, 3, 5); (2, 3, 4) is not in the span because 2 + 3 ≠ 4.'}],
 'practice': [('Find ‖(1, 2, 2)‖.', '√(1 + 4 + 4) = 3.'), ('Find (1, 2, 3)·(4, −5, 6).', '4 − 10 + 18 = 12.'),
              ('Are (2, −1) and (1, 2) orthogonal?', 'Yes: 2 − 2 = 0.'), ('Find the unit vector in the direction of (6, 8).', '‖(6, 8)‖ = 10, so (0.6, 0.8).')],
 'misc': [('The dot product is a vector.', 'It is a single number (a scalar).'), ('‖v + w‖ = ‖v‖ + ‖w‖ always.', 'Only when v and w point the same way; otherwise it is smaller.'),
          ('Vectors only make sense in 2D or 3D.', 'Data vectors can have hundreds of entries; the same rules apply.')],
 'quiz': [{'q': '‖(3, 4)‖ equals…', 'opts': ['7', '5', '25', '12'], 'ok': 1, 'why': '√(9 + 16) = 5.'},
          {'q': 'v·w = 0 means the vectors are…', 'opts': ['parallel', 'orthogonal', 'equal', 'unit vectors'], 'ok': 1, 'why': 'cos θ = 0, so θ = 90°.'},
          {'q': 'The span of two non-parallel vectors in ℝ³ is…', 'opts': ['a point', 'a line', 'a plane', 'all of ℝ³'], 'ok': 2, 'why': 'Two independent directions fill a plane.'},
          {'q': 'Doubling v changes ‖v‖ by a factor of…', 'opts': ['1', '2', '4', '√2'], 'ok': 1, 'why': '‖cv‖ = |c|‖v‖.'}],
 'cards': [('Linear combination', 'c₁v₁ + c₂v₂ + …'), ('Span', 'All linear combinations of a set of vectors.'), ('Length', '‖v‖ = √(v·v).'), ('Dot product', 'v·w = Σ vᵢwᵢ = ‖v‖‖w‖cos θ.'), ('Orthogonal', 'v·w = 0.'), ('Unit vector', 'v/‖v‖.')],
 'planet': {'text': ['Every Landsat 9 pixel is a vector. According to USGS, Landsat 9’s Operational Land Imager 2 records 9 spectral bands at 30 m (15 m for the panchromatic band) and its Thermal Infrared Sensor 2 records 2 thermal bands at 100 m, so each spot on the ground becomes a list of 11 numbers. The data are 14-bit, 2¹⁴ = 16,384 shades per band, and Landsat 9 collects about 750 scenes a day, all free.',
                     'Forest and crop health is read from the red band (band 4, 0.64–0.67 µm) and the near-infrared band (band 5, 0.85–0.88 µm). The vegetation index NDVI = (NIR − red)/(NIR + red) compares two entries of the pixel vector. With sample reflectances of 0.40 (NIR) and 0.08 (red), NDVI = 0.32/0.48 = 0.667, typical of healthy vegetation; bare soil gives values near zero.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Deforestation', 'Deforestation.html')],
            'src': [_L9, ('Interactive Linear Algebra, 2.1 Vectors', _ILA + 'vectors.html')]},
 'res': [('Interactive Linear Algebra, 2.1 Vectors', _ILA + 'vectors.html', 'Free text with interactive pictures.'), ('Interactive Linear Algebra, 6.1 Dot products and orthogonality', _ILA + 'dot-product.html', 'Lengths, angles and orthogonality.'),
         (_MIT[0], _MIT[1], 'Lecture 1: the geometry of linear equations.'), ('PhET: Vector Addition', _PH + 'vector-addition', 'Interactive.')]})
UNITS.append(
{'id': 'u2', 'title': 'Systems of Linear Equations and Gaussian Elimination', 'weeks': 'Weeks 2–3',
 'summary': 'Linear systems in row and column pictures, augmented matrices, elimination to echelon form, back substitution, reduced row echelon form, pivots and free variables, and when a system has one, none or infinitely many solutions.',
 'objectives': ['Write a system as Ax = b and as an augmented matrix.', 'Solve systems by elimination and back substitution.', 'Find the reduced row echelon form and identify pivots and free variables.', 'Decide whether a system has one, no or infinitely many solutions.'],
 'concepts': ['Row picture: each equation is a line (2D) or plane (3D) and the solution is where they meet. Column picture: b is a combination of the columns of A, with weights x.',
              'Three row operations do not change the solutions: swap rows, multiply a row by a nonzero number, and add a multiple of one row to another.',
              'Elimination produces an upper-triangular (echelon) form; back substitution then solves from the bottom up. Pivots are the first nonzero entries of each row.',
              'A column without a pivot gives a free variable and infinitely many solutions. A row 0 = c with c ≠ 0 means no solution (inconsistent).',
              'Squared-distance equations like (x − a)² + (y − b)² = d² are not linear, but subtracting one from another cancels x² and y² and leaves linear equations. That is how positioning problems become linear systems.'],
 'eqs': [('A\\mathbf{x}=\\mathbf{b}', 'Matrix form'), ('R_i\\leftarrow R_i-\\ell_{ij}R_j,\\ \\ \\ell_{ij}=a_{ij}/a_{jj}', 'Elimination step and multiplier'), ('\\text{solutions: one, none, or infinitely many}', 'The only three cases'), ('d=c\\,t', 'Range from signal travel time (GPS)')],
 'worked': [
  {'q': 'Solve x + y + z = 6, 2x + y − z = 1, x − y + 2z = 5.', 'steps': ['R₂ − 2R₁: −y − 3z = −11. R₃ − R₁: −2y + z = −1.', 'R₃ − 2R₂: 7z = 21, so z = 3.', 'Back substitute: −y − 9 = −11 gives y = 2; then x = 6 − 2 − 3 = 1.'], 'a': '(x, y, z) = (1, 2, 3).'},
  {'q': 'Beacons sit at (0, 0), (10, 0) and (0, 10) km. A receiver measures squared distances 25, 65 and 45 km². Find its position.', 'steps': ['Equation 1 minus equation 2: x² + y² − [(x − 10)² + y²] = 25 − 65, so 20x − 100 = −40.', 'Equation 1 minus equation 3: 20y − 100 = −20.', 'Solve the two linear equations.'], 'a': '(x, y) = (3, 4) km.'},
  {'q': 'How many solutions do x + 2y = 3, 2x + 4y = 6 have? And x + 2y = 3, 2x + 4y = 7?', 'steps': ['R₂ − 2R₁ gives 0 = 0 in the first system: one pivot, one free variable.', 'In the second, R₂ − 2R₁ gives 0 = 1.'], 'a': 'Infinitely many; none.'}],
 'practice': [('Solve x + y = 5, x − y = 1.', 'Adding gives 2x = 6: x = 3, y = 2.'), ('A GPS-style signal takes 0.00505783 s to arrive. How far did it travel at 299,792,458 m/s?', 'd = ct = 1,516,299 m, about 1,516 km.'),
              ('Find the reduced row echelon form of [[1, 2, 3], [2, 5, 8]] (augmented).', 'R₂ − 2R₁ = [0, 1, 2]; R₁ − 2R₂ = [1, 0, −1]: x = −1, y = 2.'),
              ('A 3 × 5 system has 3 pivots. How many free variables?', '5 − 3 = 2.')],
 'misc': [('Multiplying a row by 0 is a legal row operation.', 'It destroys information; the multiplier must be nonzero.'), ('A system with more unknowns than equations has no solution.', 'If consistent, it has infinitely many; it can also be inconsistent.'),
          ('A zero row means no solution.', 'Only a row 0 = c with c ≠ 0 does; 0 = 0 just means a free variable.')],
 'quiz': [{'q': 'A row 0 0 0 | 5 in echelon form means…', 'opts': ['one solution', 'no solution', 'infinitely many', 'x = 5'], 'ok': 1, 'why': '0 = 5 is impossible.'},
          {'q': 'Which is NOT a row operation?', 'opts': ['swap two rows', 'add a multiple of a row to another', 'multiply a row by 3', 'square a row'], 'ok': 3, 'why': 'Squaring is not linear.'},
          {'q': 'A pivot-free column gives…', 'opts': ['a free variable', 'no solution', 'a zero determinant only', 'a unique solution'], 'ok': 0, 'why': 'Its variable can be chosen freely.'},
          {'q': 'In the column picture, Ax = b asks whether b is…', 'opts': ['orthogonal to A', 'a combination of the columns of A', 'a row of A', 'an eigenvector'], 'ok': 1, 'why': 'Ax = x₁a₁ + x₂a₂ + …'}],
 'cards': [('Augmented matrix', '[A | b].'), ('Pivot', 'First nonzero entry in a row of echelon form.'), ('Free variable', 'Variable whose column has no pivot.'), ('RREF', 'Pivots 1, zeros above and below.'), ('Inconsistent', 'A row 0 = c, c ≠ 0.'), ('Back substitution', 'Solve the triangular system from the bottom up.')],
 'planet': {'text': ['GPS is a linear algebra machine. GPS.gov reports that at least 24 operational satellites are kept available 95% of the time and that 31 operational satellites have been flown for more than a decade, at about 20,200 km altitude, each circling Earth twice a day. They sit in six equally spaced orbital planes so that users can view at least four satellites from virtually any point on the planet.',
                     'GPS.gov’s trilateration activity explains the idea: distance = rate × time, with the rate equal to the speed of light, 299,792,458 m/s, and distances from at least 3 satellites fix a 3D position. A real receiver’s clock is also unknown, so in the standard textbook model the unknowns are x, y, z and the clock offset, four unknowns that need four satellites; differencing the range equations, as in the worked example, turns them into a linear system. A clock error of just one microsecond would put a range off by 299.8 m. Precise positions guide farm tractors that apply less fertilizer, ships on efficient routes and the survey stations that measure sea level and ice.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Space', 'Space.html')],
            'src': [_GPSS, _GPST]},
 'res': [('Interactive Linear Algebra, 1.1 Systems of linear equations', _ILA + 'systems-of-eqns.html', 'Free text section.'), ('Interactive Linear Algebra, 1.2 Row reduction', _ILA + 'row-reduction.html', 'Echelon forms step by step.'),
         (_MIT[0], _MIT[1], 'Lecture 2: elimination with matrices.'), (_HEF[0], _HEF[1], 'Chapter One: linear systems.')]})
UNITS.append(
{'id': 'u3', 'title': 'Matrix Algebra: Multiplication, Inverses and LU Factorization', 'weeks': 'Week 4',
 'summary': 'Matrix–vector and matrix–matrix products, the rules (and non-rules) of matrix algebra, transposes, elimination matrices, the inverse and Gauss–Jordan, the 2 × 2 inverse formula, A = LU, and the cost of elimination.',
 'objectives': ['Multiply matrices and check that sizes match.', 'Find inverses by the 2 × 2 formula and by Gauss–Jordan.', 'Factor A = LU and use it to solve systems.', 'Estimate the cost of elimination as n grows.'],
 'concepts': ['(AB)ᵢⱼ = row i of A dotted with column j of B. An m × n times an n × p matrix is m × p. In general AB ≠ BA.',
              'The inverse A⁻¹ satisfies AA⁻¹ = A⁻¹A = I. It exists exactly when A has n pivots (det A ≠ 0). (AB)⁻¹ = B⁻¹A⁻¹ and (AB)ᵀ = BᵀAᵀ.',
              'Gauss–Jordan: row-reduce [A | I] to [I | A⁻¹].',
              'Elimination without row swaps records its multipliers in a lower-triangular L with ones on the diagonal, giving A = LU. Solve Lc = b, then Ux = c; with L and U saved, each new right side is cheap.',
              'Elimination on an n × n matrix costs about n³/3 multiply–add operations; solving with saved L and U costs about n² per right side.'],
 'eqs': [('(AB)_{ij}=\\sum_k a_{ik}b_{kj}', 'Matrix product'), ('\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}^{-1}=\\frac{1}{ad-bc}\\begin{bmatrix}d&-b\\\\-c&a\\end{bmatrix}', '2 × 2 inverse'), ('A=LU', 'LU factorization'), ('\\text{cost}\\approx n^3/3', 'Elimination operation count')],
 'worked': [
  {'q': 'Find AB and BA for A = [[1, 2], [3, 4]] and B = [[0, 1], [1, 0]].', 'steps': ['AB: row 1 · columns = (2, 1); row 2 = (4, 3).', 'BA swaps the rows of A: [[3, 4], [1, 2]].'], 'a': 'AB = [[2, 1], [4, 3]], BA = [[3, 4], [1, 2]], so AB ≠ BA.'},
  {'q': 'Invert A = [[4, 7], [2, 6]].', 'steps': ['ad − bc = 24 − 14 = 10.', 'A⁻¹ = (1/10)[[6, −7], [−2, 4]].'], 'a': 'A⁻¹ = [[0.6, −0.7], [−0.2, 0.4]].'},
  {'q': 'Factor A = [[2, 1], [6, 8]] as LU.', 'steps': ['Multiplier ℓ₂₁ = 6/2 = 3.', 'R₂ − 3R₁ = [0, 5].'], 'a': 'L = [[1, 0], [3, 1]], U = [[2, 1], [0, 5]].'}],
 'practice': [('What size is a 3 × 2 matrix times a 2 × 4 matrix?', '3 × 4.'), ('Invert [[2, 1], [5, 3]].', 'det = 1, inverse [[3, −1], [−5, 2]].'),
              ('About how many operations does elimination take for n = 1000?', 'n³/3 ≈ 3.33 × 10⁸.'), ('If A and B are invertible, what is (AB)⁻¹?', 'B⁻¹A⁻¹.')],
 'misc': [('AB = BA.', 'Matrix multiplication is usually not commutative.'), ('(AB)⁻¹ = A⁻¹B⁻¹.', 'The order reverses: B⁻¹A⁻¹.'),
          ('Computers solve Ax = b by computing A⁻¹.', 'They factor A = LU (or similar); forming A⁻¹ is slower and less accurate.')],
 'quiz': [{'q': 'A 2 × 3 matrix times a 3 × 5 matrix is…', 'opts': ['2 × 5', '3 × 3', '5 × 2', 'undefined'], 'ok': 0, 'why': 'Outer sizes.'},
          {'q': 'A matrix is invertible exactly when it has…', 'opts': ['no zeros', 'n pivots', 'a zero row', 'equal entries'], 'ok': 1, 'why': 'Full set of pivots.'},
          {'q': 'Doubling n multiplies elimination cost by about…', 'opts': ['2', '4', '8', '16'], 'ok': 2, 'why': 'n³ grows 2³ = 8 times.'},
          {'q': 'L in A = LU holds…', 'opts': ['the pivots', 'the multipliers', 'the inverse', 'the eigenvalues'], 'ok': 1, 'why': 'Below-diagonal multipliers, ones on the diagonal.'}],
 'cards': [('Identity', 'AI = IA = A.'), ('Inverse', 'AA⁻¹ = I.'), ('2 × 2 inverse', 'Swap a, d; negate b, c; divide by ad − bc.'), ('Transpose rule', '(AB)ᵀ = BᵀAᵀ.'), ('LU', 'A = LU from elimination.'), ('Cost', 'About n³/3 for elimination.')],
 'planet': {'text': ['Weather and climate forecasts are, at their core, enormous linear-algebra jobs repeated many times a day. NOAA reported in August 2023 that its twin operational supercomputers, Dogwood in Manassas, Virginia and Cactus in Phoenix, Arizona, were upgraded by 20% to 14.5 petaflops each, so that together the forecast system can process 29 quadrillion calculations per second, and that with its research supercomputers its total capacity is 49 petaflops.',
                     'The n³/3 rule shows why speed matters. As a sample, a dense system with n = 100,000 unknowns needs about 3.33 × 10¹⁴ operations; at a sustained 14.5 × 10¹⁵ operations per second that is about 0.023 s, but doubling n multiplies the work by 8. Real models use sparse matrices and clever solvers, yet the same cubic growth is what NOAA says the extra power will pay for: higher-resolution models that improve forecasts and warnings.'],
            'site': [('Intro to Programming', 'Intro_to_Programming.html'), ('Solutions', 'Solutions.html')],
            'src': [_NOAA, _MIT]},
 'res': [('Interactive Linear Algebra, 3.4 Matrix multiplication', _ILA + 'matrix-multiplication.html', 'Free text section.'), ('Interactive Linear Algebra, 3.5 Matrix inverses', _ILA + 'matrix-inverses.html', 'Inverses and Gauss–Jordan.'),
         (_MIT[0], _MIT[1], 'Lectures 3–4: multiplication, inverses and A = LU.'), (_MITSC[0], _MITSC[1], 'Recitation videos on LU.')]})
UNITS.append(
{'id': 'u4', 'title': 'Linear Models: Input–Output (Leontief) Economics, Networks and Balancing', 'weeks': 'Week 5',
 'summary': 'Building linear models from real systems: the Leontief input–output model x = Ax + d and its solution x = (I − A)⁻¹d, environmentally extended models that turn spending into emissions, network flows and balancing chemical equations.',
 'objectives': ['Set up and solve a Leontief input–output model.', 'Interpret the entries of (I − A)⁻¹.', 'Extend an input–output model with emission intensities to find a footprint.', 'Write flow-balance and chemical-balance problems as linear systems.'],
 'concepts': ['In an input–output model, column j of the consumption matrix A lists what sector j buys from each sector to make one dollar of output.',
              'Total output x must cover what industries use (Ax) plus final demand d: x = Ax + d, so (I − A)x = d and x = (I − A)⁻¹d.',
              'Entry (i, j) of the Leontief inverse (I − A)⁻¹ is the total output of sector i needed, directly and through all supply chains, for one dollar of final demand from sector j.',
              'Environmentally extended models multiply output by a row of emission intensities e (for example kg CO₂ per dollar): footprint = e·x.',
              'Conservation laws give linear equations too: flow in equals flow out at every node of a network, and atoms of each element balance in a chemical reaction.'],
 'eqs': [('\\mathbf{x}=A\\mathbf{x}+\\mathbf{d}', 'Input–output balance'), ('\\mathbf{x}=(I-A)^{-1}\\mathbf{d}', 'Leontief solution'), ('\\text{footprint}=\\mathbf{e}\\cdot\\mathbf{x}', 'Environmentally extended model'), ('\\sum \\text{in}=\\sum \\text{out}', 'Flow balance at a node')],
 'worked': [
  {'q': 'A two-sector economy has A = [[0.2, 0.3], [0.1, 0.4]] and final demand d = (100, 50) (sample values, $ million). Find the total output.', 'steps': ['I − A = [[0.8, −0.3], [−0.1, 0.6]], det = 0.48 − 0.03 = 0.45.', '(I − A)⁻¹ = (1/0.45)[[0.6, 0.3], [0.1, 0.8]].', 'x = (1/0.45)(60 + 15, 10 + 40).'], 'a': 'x = (166.7, 111.1) $ million.'},
  {'q': 'With sample emission intensities e = (0.5, 2.0) kg CO₂ per dollar, find the footprint of that final demand.', 'steps': ['footprint = 0.5 × 166.7 + 2.0 × 111.1 (in kg per $ × $ million).'], 'a': '305.6 million kg = 305.6 kt CO₂ (sample).'},
  {'q': 'Balance x CH₄ + y O₂ → z CO₂ + w H₂O.', 'steps': ['C: x = z. H: 4x = 2w. O: 2y = 2z + w.', 'Set x = 1: z = 1, w = 2, y = 2.'], 'a': 'CH₄ + 2 O₂ → CO₂ + 2 H₂O.'}],
 'practice': [('In the worked model, how much output of sector 1 does $1 of final demand for sector 2 require in total?', 'Entry (1, 2) of (I − A)⁻¹ = 0.3/0.45 = 0.667.'), ('A single-sector economy uses 0.25 of its own output. What total output meets a demand of 300?', 'x = 300/(1 − 0.25) = 400.'),
              ('A node has inflows 40 and 25 and one outflow f₁ plus an outflow of 30. Find f₁.', 'f₁ = 65 − 30 = 35.'), ('Balance H₂ + O₂ → H₂O.', '2 H₂ + O₂ → 2 H₂O.')],
 'misc': [('Total output equals final demand.', 'Industries also consume each other’s output, so x is larger than d.'), ('The footprint comes only from the sector you buy from.', 'The Leontief inverse adds every upstream supplier.'),
          ('Any A gives a sensible economy.', 'Column sums must be below 1 for (I − A)⁻¹ to have nonnegative entries.')],
 'quiz': [{'q': 'The Leontief solution is…', 'opts': ['x = Ad', 'x = (I − A)⁻¹d', 'x = A⁻¹d', 'x = d − A'], 'ok': 1, 'why': 'From x = Ax + d.'},
          {'q': 'Column j of A describes…', 'opts': ['what sector j sells', 'what sector j buys per dollar of output', 'final demand', 'emissions'], 'ok': 1, 'why': 'Inputs per unit of output.'},
          {'q': 'A footprint in an extended model is…', 'opts': ['e·x', 'e + x', 'det A', 'x/e'], 'ok': 0, 'why': 'Intensity times output, summed.'},
          {'q': 'Balancing a chemical equation is a…', 'opts': ['nonlinear problem', 'homogeneous linear system', 'determinant', 'eigenvalue problem'], 'ok': 1, 'why': 'Atom counts give Ax = 0.'}],
 'cards': [('Consumption matrix', 'Inputs per dollar of output.'), ('Leontief model', 'x = Ax + d.'), ('Leontief inverse', '(I − A)⁻¹, total requirements.'), ('Extended model', 'footprint = e·x.'), ('Flow balance', 'In = out at each node.'), ('Homogeneous system', 'Ax = 0.')],
 'planet': {'text': ['The U.S. EPA uses exactly this model to trace pollution through the economy. According to EPA, its USEEIO models combine data on economic transactions between 389 industry sectors with environmental data for those sectors, covering land, water, energy and mineral use, air pollution, nutrients and toxics, to evaluate the impacts of goods and services. EPA describes them as useful for carbon footprinting, and they support its sustainable materials management work.',
                     'A 389-sector consumption matrix has 389² = 151,321 entries, far too many for hand work but easy for the elimination and LU methods of Unit 3. The Leontief inverse is what lets a city, company or household see the emissions hidden in its supply chains, not just at the factory gate.'],
            'site': [('Solutions', 'Solutions.html'), ('General Chemistry I', 'General_Chemistry_I.html')],
            'src': [_EIO, ('Interactive Linear Algebra, 1.1 Systems of linear equations', _ILA + 'systems-of-eqns.html')]},
 'res': [(_EIO[0], _EIO[1], 'EPA’s environmentally extended input–output models.'), (_HEF[0], _HEF[1], 'Topic: Leontief input–output analysis.'),
         (_MIT[0], _MIT[1], 'Applications lectures and problem sets.'), ('Interactive Linear Algebra, 1.2 Row reduction', _ILA + 'row-reduction.html', 'Solving the systems.')]})
UNITS.append(
{'id': 'u5', 'title': 'Vector Spaces, Subspaces, Independence, Basis, Rank and the Four Fundamental Subspaces', 'weeks': 'Weeks 6–7',
 'summary': 'Vector spaces and subspaces, the column space and null space, solving Ax = 0 and Ax = b completely, linear independence, basis and dimension, rank, the rank–nullity theorem and Strang’s four fundamental subspaces.',
 'objectives': ['Test whether a set is a subspace.', 'Find bases for the column space and null space of a matrix.', 'Test vectors for linear independence.', 'Use rank–nullity and the dimensions of the four fundamental subspaces.'],
 'concepts': ['A subspace contains the zero vector and is closed under addition and scalar multiplication. Lines and planes through the origin are subspaces; ones that miss the origin are not.',
              'Column space C(A): all Ax, the set of b for which Ax = b is solvable. Null space N(A): all x with Ax = 0.',
              'Vectors are linearly independent if the only combination giving zero is the all-zero one. A basis is an independent spanning set; every basis of a space has the same number of vectors, its dimension.',
              'Rank r = number of pivots = dim C(A). Rank–nullity: r + dim N(A) = n, the number of columns.',
              'Four fundamental subspaces of an m × n matrix of rank r: C(A) (dim r) and N(Aᵀ) (dim m − r) in ℝᵐ; C(Aᵀ) (dim r) and N(A) (dim n − r) in ℝⁿ. N(A) is orthogonal to the row space.'],
 'eqs': [('C(A)=\\{A\\mathbf{x}\\},\\ \\ N(A)=\\{\\mathbf{x}:A\\mathbf{x}=0\\}', 'Column space and null space'), ('r+\\dim N(A)=n', 'Rank–nullity'), ('\\mathbf{x}=\\mathbf{x}_p+\\mathbf{x}_n', 'Complete solution of Ax = b'), ('\\dim N(A^T)=m-r', 'Left null space')],
 'worked': [
  {'q': 'Find the rank and a null-space basis of A = [[1, 2, 3], [2, 4, 6], [1, 0, 1]].', 'steps': ['R₂ − 2R₁ = 0; R₃ − R₁ = [0, −2, −2]. Two pivots, so r = 2.', 'Ax = 0: x + z = 0 and −2y − 2z = 0, with z free.', 'Take z = 1: x = −1, y = −1.'], 'a': 'r = 2, N(A) spanned by (−1, −1, 1); dim N(A) = 3 − 2 = 1.'},
  {'q': 'Are (1, 2, 3), (4, 5, 6), (7, 8, 9) independent?', 'steps': ['Row-reduce the matrix with these columns: R₂ − 2R₁ and R₃ − 3R₁ give rows [0, −3, −6] and [0, −6, −12], which are multiples.', 'Only two pivots.'], 'a': 'No: (7, 8, 9) = 2(4, 5, 6) − (1, 2, 3).'},
  {'q': 'A 5 × 8 matrix has rank 3. Give the dimensions of its four fundamental subspaces.', 'steps': ['C(A) and C(Aᵀ): r = 3.', 'N(A): n − r = 8 − 3; N(Aᵀ): m − r = 5 − 3.'], 'a': '3, 3, 5 and 2.'}],
 'practice': [('Is the line y = 2x + 1 a subspace of ℝ²?', 'No: it does not contain (0, 0).'), ('A 4 × 4 matrix has a 2-dimensional null space. What is its rank?', '4 − 2 = 2.'),
              ('What is the dimension of the space of 2 × 2 matrices?', '4.'), ('Can 4 vectors in ℝ³ be independent?', 'No: at most 3.')],
 'misc': [('Any plane in ℝ³ is a subspace.', 'Only planes through the origin.'), ('Rank counts nonzero entries.', 'It counts pivots (independent columns).'),
          ('The null space lives in the same space as b.', 'N(A) is in ℝⁿ (the x side); b is in ℝᵐ.')],
 'quiz': [{'q': 'Rank–nullity says r + dim N(A) equals…', 'opts': ['m', 'n', 'm + n', 'r'], 'ok': 1, 'why': 'Number of columns.'},
          {'q': 'Ax = b is solvable exactly when b is in…', 'opts': ['N(A)', 'C(A)', 'N(Aᵀ)', 'C(Aᵀ)'], 'ok': 1, 'why': 'b must be a combination of the columns.'},
          {'q': 'The null space is orthogonal to…', 'opts': ['the column space', 'the row space', 'b', 'the left null space'], 'ok': 1, 'why': 'Each row dotted with x is 0.'},
          {'q': 'A basis of ℝ³ has how many vectors?', 'opts': ['2', '3', '4', 'any number'], 'ok': 1, 'why': 'Dimension 3.'}],
 'cards': [('Subspace', 'Contains 0; closed under + and scaling.'), ('Column space', 'All Ax.'), ('Null space', 'All x with Ax = 0.'), ('Basis', 'Independent spanning set.'), ('Rank', 'Number of pivots.'), ('Rank–nullity', 'r + dim N(A) = n.')],
 'planet': {'text': ['Dimension counts unknowns, and better forecasts need more of them. NOAA said its 2023 supercomputer upgrade would let the U.S. Global Forecast System improve its horizontal resolution from 13 km to 9 km, helping smaller-scale features be seen and simulated.',
                     'A grid with spacing h has about (1/h)² columns per unit area, so going from 13 km to 9 km multiplies the number of grid columns by (13/9)² = 2.09. Every one of those columns carries temperature, wind, humidity and pressure at many levels, so the state vector of a forecast lives in a space with a vastly higher dimension, and the matrices that update it grow to match.'],
            'site': [('Calculus III', 'Calculus_III.html'), ('Differential Equations', 'Differential_Equations.html')],
            'src': [_NOAA, ('Interactive Linear Algebra, 2.7 Basis and dimension', _ILA + 'dimension.html')]},
 'res': [('Interactive Linear Algebra, 2.6 Subspaces', _ILA + 'subspaces.html', 'Free text section.'), ('Interactive Linear Algebra, 2.5 Linear independence', _ILA + 'linear-independence.html', 'Independence tests.'),
         ('Interactive Linear Algebra, 2.9 The rank theorem', _ILA + 'rank-thm.html', 'Rank and nullity.'), (_MIT[0], _MIT[1], 'Lectures 5–10: spaces, rank and the four subspaces.')]})
UNITS.append(
{'id': 'u6', 'title': 'Orthogonality, Projections, Least Squares and Gram–Schmidt', 'weeks': 'Weeks 8–9',
 'summary': 'Orthogonal vectors and subspaces, projection onto a line and onto a subspace, the normal equations AᵀAx̂ = Aᵀb, fitting lines and curves to data by least squares, orthonormal bases, Gram–Schmidt and A = QR.',
 'objectives': ['Project a vector onto a line and onto a column space.', 'Fit a line to data with the normal equations.', 'Build an orthonormal basis with Gram–Schmidt.', 'Explain why least squares is a projection.'],
 'concepts': ['The projection of b onto the line through a is p = (a·b/a·a) a; the error e = b − p is orthogonal to a.',
              'When Ax = b has no solution (more equations than unknowns, noisy data), choose x̂ to make ‖b − Ax̂‖ as small as possible. The error must be orthogonal to C(A), giving the normal equations AᵀAx̂ = Aᵀb.',
              'For a line y = C + Dt through points (tᵢ, yᵢ), the columns of A are all ones and the tᵢ values.',
              'Orthonormal vectors qᵢ satisfy qᵢ·qⱼ = 0 (i ≠ j) and ‖qᵢ‖ = 1. With Q having orthonormal columns, QᵀQ = I and projections become p = QQᵀb.',
              'Gram–Schmidt subtracts from each new vector its projections on the earlier ones, then normalizes. The result is A = QR with R upper triangular.'],
 'eqs': [('\\mathbf{p}=\\frac{\\mathbf{a}\\cdot\\mathbf{b}}{\\mathbf{a}\\cdot\\mathbf{a}}\\,\\mathbf{a}', 'Projection onto a line'), ('A^TA\\hat{\\mathbf{x}}=A^T\\mathbf{b}', 'Normal equations'), ('P=A(A^TA)^{-1}A^T', 'Projection matrix'), ('A=QR', 'Gram–Schmidt factorization')],
 'worked': [
  {'q': 'Project b = (2, 3) onto a = (1, 1).', 'steps': ['a·b = 5, a·a = 2.', 'p = 2.5(1, 1); e = b − p = (−0.5, 0.5), and e·a = 0.'], 'a': 'p = (2.5, 2.5).'},
  {'q': 'Fit y = C + Dt to (0, 1), (1, 2), (2, 4) by least squares.', 'steps': ['A has rows (1, 0), (1, 1), (1, 2); AᵀA = [[3, 3], [3, 5]], Aᵀb = (7, 10).', 'det = 6; C = (5 × 7 − 3 × 10)/6, D = (3 × 10 − 3 × 7)/6.'], 'a': 'C = 0.833, D = 1.5: y = 0.833 + 1.5t.'},
  {'q': 'Apply Gram–Schmidt to a₁ = (1, 1, 0), a₂ = (1, 0, 1).', 'steps': ['q₁ = (1, 1, 0)/√2.', 'a₂ − (a₂·q₁)q₁ = (1, 0, 1) − ½(1, 1, 0) = (0.5, −0.5, 1), length √1.5 = 1.225.'], 'a': 'q₁ = (0.707, 0.707, 0), q₂ = (0.408, −0.408, 0.816).'}],
 'practice': [('Project (3, 4) onto (1, 0).', '(3, 0).'), ('Write the normal equations for fitting y = Dt (no intercept) to (1, 2), (2, 3).', 'Σt² D = Σty: 5D = 8, D = 1.6.'),
              ('Is Q = [[0, 1], [1, 0]] orthogonal?', 'Yes: QᵀQ = I.'), ('If b is already in C(A), what is the least-squares error?', 'Zero: p = b.')],
 'misc': [('Least squares solves Ax = b exactly.', 'It finds the closest Ax̂ when no exact solution exists.'), ('Any basis makes projections easy.', 'Orthonormal bases do; otherwise you need (AᵀA)⁻¹.'),
          ('A straight-line fit means the data are linear.', 'Check the residuals; a curve may fit better (add a t² column).')],
 'quiz': [{'q': 'The normal equations are…', 'opts': ['Ax = b', 'AᵀAx̂ = Aᵀb', 'AAᵀx = b', 'Aᵀx = b'], 'ok': 1, 'why': 'Error orthogonal to C(A).'},
          {'q': 'The least-squares error vector is orthogonal to…', 'opts': ['b', 'the column space', 'the null space', 'x̂'], 'ok': 1, 'why': 'That is what makes it shortest.'},
          {'q': 'For Q with orthonormal columns, QᵀQ =…', 'opts': ['0', 'Q', 'I', 'QQᵀ'], 'ok': 2, 'why': 'Dot products 0 or 1.'},
          {'q': 'Gram–Schmidt produces…', 'opts': ['A = LU', 'A = QR', 'A = PDP⁻¹', 'A = UΣVᵀ'], 'ok': 1, 'why': 'Orthonormal Q, triangular R.'}],
 'cards': [('Projection on a line', 'p = (a·b/a·a)a.'), ('Normal equations', 'AᵀAx̂ = Aᵀb.'), ('Projection matrix', 'P = A(AᵀA)⁻¹Aᵀ.'), ('Orthonormal', 'qᵢ·qⱼ = 0, ‖qᵢ‖ = 1.'), ('Gram–Schmidt', 'Subtract projections, normalize.'), ('QR', 'A = QR.')],
 'planet': {'text': ['Sea-level rise is measured by fitting curves to noisy satellite data. NASA reports that satellite altimeters, TOPEX/Poseidon, Jason-1, -2 and -3 and now Sentinel-6 Michael Freilich, have tracked global mean sea level since 1993, that it has risen 114.4 mm since then, and that the rate of rise has increased from 0.08 inches per year (0.20 cm per year) in 1993 to 0.17 inches per year (0.44 cm per year) now, about 2.2 times faster.',
                     'A straight-line least-squares fit gives an average rate; adding a t² column to A fits a curve whose changing slope measures the acceleration NASA describes. Lab D fits sample data shaped like the NASA record with exactly the normal equations from this unit.'],
            'site': [('Oceans', 'Oceans.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_SL, ('Interactive Linear Algebra, 6.5 The method of least squares', _ILA + 'least-squares.html')]},
 'res': [('Interactive Linear Algebra, 6.3 Orthogonal projection', _ILA + 'projections.html', 'Free text section.'), ('Interactive Linear Algebra, 6.5 The method of least squares', _ILA + 'least-squares.html', 'Least squares with pictures.'),
         ('Interactive Linear Algebra, 6.4 Orthogonal sets', _ILA + 'orthogonal-sets.html', 'Gram–Schmidt.'), (_MIT[0], _MIT[1], 'Lectures 14–17: orthogonality, projections, least squares, Gram–Schmidt.')]})
UNITS.append(
{'id': 'u7', 'title': 'Determinants: Properties, Cofactors, Cramer’s Rule and Volume', 'weeks': 'Week 10',
 'summary': 'The determinant from its properties, computing it by elimination and by cofactor expansion, det(AB) = det A det B, the test for invertibility, Cramer’s rule, and the determinant as the area or volume scale factor of a linear map.',
 'objectives': ['Compute 2 × 2 and 3 × 3 determinants by cofactors and by elimination.', 'Use the properties of determinants under row operations.', 'Solve small systems by Cramer’s rule.', 'Interpret |det A| as an area or volume scale factor.'],
 'concepts': ['det A ≠ 0 exactly when A is invertible. The determinant of a triangular matrix is the product of its diagonal entries, so det A = ± (product of pivots).',
              'Row operations: a swap flips the sign, scaling a row by c scales det by c, and adding a multiple of one row to another leaves det unchanged.',
              'det(AB) = det A · det B, det(Aᵀ) = det A and det(A⁻¹) = 1/det A.',
              'Cofactor expansion along a row: det A = Σ aᵢⱼCᵢⱼ with Cᵢⱼ = (−1)ⁱ⁺ʲ times the minor. Cramer’s rule: xᵢ = det(Bᵢ)/det A, where Bᵢ has b in column i.',
              'A linear map x ↦ Ax multiplies areas (2D) or volumes (3D) by |det A|; a negative determinant also flips orientation.'],
 'eqs': [('\\det\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}=ad-bc', '2 × 2 determinant'), ('\\det(AB)=\\det A\\,\\det B', 'Product rule'), ('x_i=\\frac{\\det B_i}{\\det A}', 'Cramer’s rule'), ('\\text{area}(AS)=|\\det A|\\,\\text{area}(S)', 'Area scale factor')],
 'worked': [
  {'q': 'Find det [[1, 2, 0], [0, 1, 3], [2, 0, 1]] by cofactors along row 1.', 'steps': ['1 × (1 × 1 − 3 × 0) = 1.', '− 2 × (0 × 1 − 3 × 2) = −2 × (−6) = 12.', '+ 0 × (…) = 0.'], 'a': 'det = 13.'},
  {'q': 'Solve 2x + y = 5, x + 3y = 10 by Cramer’s rule.', 'steps': ['det A = 6 − 1 = 5.', 'x = det[[5, 1], [10, 3]]/5 = (15 − 10)/5.', 'y = det[[2, 5], [1, 10]]/5 = (20 − 5)/5.'], 'a': 'x = 1, y = 3.'},
  {'q': 'Find the area of the parallelogram with sides (3, 0) and (1, 2).', 'steps': ['Area = |det [[3, 1], [0, 2]]| = |6 − 0|.'], 'a': '6 square units.'}],
 'practice': [('det [[3, 1], [2, 4]]?', '12 − 2 = 10.'), ('det [[2, 0, 1], [1, 3, 2], [1, 1, 1]]?', '2(3 − 2) − 0 + 1(1 − 3) = 0, so it is singular.'),
              ('If det A = 4 for a 3 × 3 A, what is det(2A)?', '2³ × 4 = 32.'), ('If det A = 5, what is det(A⁻¹)?', '1/5 = 0.2.')],
 'misc': [('det(A + B) = det A + det B.', 'False in general; only det(AB) splits.'), ('det(2A) = 2 det A.', 'For n × n, det(2A) = 2ⁿ det A.'),
          ('Cofactor expansion is the fast way.', 'It takes about n! steps; elimination takes about n³/3.')],
 'quiz': [{'q': 'Swapping two rows multiplies det by…', 'opts': ['0', '1', '−1', '2'], 'ok': 2, 'why': 'Sign flips.'},
          {'q': 'det A = 0 means A is…', 'opts': ['orthogonal', 'singular', 'symmetric', 'the identity'], 'ok': 1, 'why': 'Not invertible.'},
          {'q': 'det of a triangular matrix is…', 'opts': ['the trace', 'the product of the diagonal', 'zero', 'the sum of the diagonal'], 'ok': 1, 'why': 'Expand down the diagonal.'},
          {'q': 'A map with det = 3 changes areas by a factor of…', 'opts': ['1/3', '3', '9', '√3'], 'ok': 1, 'why': '|det A|.'}],
 'cards': [('2 × 2 det', 'ad − bc.'), ('Invertibility', 'det A ≠ 0.'), ('Product rule', 'det(AB) = det A det B.'), ('Row swap', 'Changes the sign.'), ('Cramer’s rule', 'xᵢ = det Bᵢ/det A.'), ('Area factor', '|det A|.')],
 'planet': {'text': ['Turning pixels into land area is a determinant. USGS lists Landsat 9’s multispectral bands at 30 m and its panchromatic band at 15 m. The map from pixel indices (i, j) to ground coordinates is, locally, a matrix; for an aligned 30 m grid it is diag(30, 30) m, whose determinant is 900, so each pixel covers 900 m². The 15 m panchromatic grid has determinant 225 m², so four panchromatic pixels fit in one multispectral pixel.',
                     'Counting pixels classified as forest and multiplying by this scale factor is how satellite records measure forest loss in hectares (1 ha = 10,000 m², about 11.1 Landsat pixels). When an image is rotated or sheared to fit a map, the determinant of the new matrix keeps the area right.'],
            'site': [('Deforestation', 'Deforestation.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_L9, ('Interactive Linear Algebra, 4.3 Determinants and volumes', _ILA + 'determinants-volumes.html')]},
 'res': [('Interactive Linear Algebra, 4.1 Determinants: definition', _ILA + 'determinants-definitions-properties.html', 'Free text section.'), ('Interactive Linear Algebra, 4.3 Determinants and volumes', _ILA + 'determinants-volumes.html', 'Geometric meaning.'),
         (_MIT[0], _MIT[1], 'Lectures 18–20: determinants, cofactors, Cramer’s rule.'), (_HEF[0], _HEF[1], 'Chapter Four: determinants.')]})
UNITS.append(
{'id': 'u8', 'title': 'Eigenvalues and Eigenvectors', 'weeks': 'Week 11',
 'summary': 'Eigenvectors as directions a matrix only stretches, the characteristic equation det(A − λI) = 0, trace and determinant checks, eigenvalues of special matrices, complex eigenvalues and rotation, power iteration, and natural modes of vibrating structures.',
 'objectives': ['Find eigenvalues from det(A − λI) = 0 and eigenvectors from the null space of A − λI.', 'Check eigenvalues with the trace and determinant.', 'Recognize real, repeated and complex eigenvalues.', 'Use power iteration to find the dominant eigenvalue.'],
 'concepts': ['Av = λv with v ≠ 0: the eigenvector v keeps its direction and is scaled by the eigenvalue λ.',
              'The eigenvalues are the roots of det(A − λI) = 0, a polynomial of degree n. For each λ, the eigenvectors fill the null space of A − λI.',
              'Checks: the eigenvalues sum to the trace (sum of the diagonal) and multiply to det A.',
              'Symmetric matrices have real eigenvalues and orthogonal eigenvectors. Rotation matrices have complex eigenvalues. Triangular matrices show their eigenvalues on the diagonal.',
              'Power iteration: repeatedly multiply a starting vector by A and rescale; it lines up with the eigenvector of the largest |λ|. For vibration, Kv = ω²Mv gives the natural frequencies ω and mode shapes v.'],
 'eqs': [('A\\mathbf{v}=\\lambda\\mathbf{v}', 'Eigenvalue equation'), ('\\det(A-\\lambda I)=0', 'Characteristic equation'), ('\\lambda_1+\\cdots+\\lambda_n=\\operatorname{tr}A,\\ \\ \\lambda_1\\cdots\\lambda_n=\\det A', 'Trace and determinant checks'), ('K\\mathbf{v}=\\omega^2M\\mathbf{v}', 'Natural modes of a structure')],
 'worked': [
  {'q': 'Find the eigenvalues and eigenvectors of A = [[2, 1], [1, 2]].', 'steps': ['det(A − λI) = (2 − λ)² − 1 = λ² − 4λ + 3 = 0.', 'λ = 3: A − 3I = [[−1, 1], [1, −1]] gives v = (1, 1). λ = 1: v = (1, −1).', 'Check: 3 + 1 = 4 = trace; 3 × 1 = 3 = det.'], 'a': 'λ = 3 with (1, 1); λ = 1 with (1, −1).'},
  {'q': 'Find the eigenvalues of [[4, 1], [2, 3]].', 'steps': ['λ² − 7λ + 10 = 0 (trace 7, det 10).', '(λ − 5)(λ − 2) = 0.'], 'a': 'λ = 5 and λ = 2.'},
  {'q': 'A two-story sample building has equal floor masses m and story stiffness k, with K/m = (k/m)[[2, −1], [−1, 1]] and k/m = 100 s⁻². Find the fundamental frequency.', 'steps': ['Eigenvalues of [[2, −1], [−1, 1]]: λ = (3 ± √5)/2 = 0.382 and 2.618.', 'ω₁² = 100 × 0.382 = 38.2 s⁻², ω₁ = 6.18 rad/s.', 'f₁ = ω₁/(2π), T₁ = 1/f₁.'], 'a': 'f₁ = 0.984 Hz, period T₁ = 1.02 s (sample values).'}],
 'practice': [('Eigenvalues of [[5, 0], [0, −2]]?', '5 and −2 (diagonal).'), ('A 3 × 3 matrix has eigenvalues 1, 2, 3. Find its trace and determinant.', 'Trace 6, det 6.'),
              ('Eigenvalues of the 90° rotation [[0, −1], [1, 0]]?', 'λ² + 1 = 0: λ = ±i.'), ('If Av = 4v, what is A²v?', '16v.')],
 'misc': [('The zero vector is an eigenvector.', 'Eigenvectors must be nonzero.'), ('Row reduction keeps the eigenvalues.', 'It changes them; use det(A − λI).'),
          ('Every real matrix has real eigenvalues.', 'Rotations give complex ones; symmetric matrices are the safe case.')],
 'quiz': [{'q': 'The eigenvalues of a triangular matrix are…', 'opts': ['its pivots after swaps', 'its diagonal entries', 'all 1', 'its row sums'], 'ok': 1, 'why': 'det(A − λI) is a product of diagonal terms.'},
          {'q': 'The sum of the eigenvalues equals…', 'opts': ['the determinant', 'the trace', 'the rank', 'n'], 'ok': 1, 'why': 'Trace check.'},
          {'q': 'Power iteration finds…', 'opts': ['the smallest eigenvalue', 'the dominant eigenvalue', 'the determinant', 'the inverse'], 'ok': 1, 'why': 'Largest |λ| wins.'},
          {'q': 'Symmetric matrices have…', 'opts': ['complex eigenvalues', 'real eigenvalues and orthogonal eigenvectors', 'zero determinant', 'no eigenvectors'], 'ok': 1, 'why': 'Spectral theorem.'}],
 'cards': [('Eigenvector', 'Av = λv, v ≠ 0.'), ('Characteristic equation', 'det(A − λI) = 0.'), ('Trace check', 'Σλ = trace.'), ('Determinant check', 'Πλ = det A.'), ('Power iteration', 'Repeated multiplication finds the top eigenvector.'), ('Natural modes', 'Kv = ω²Mv.')],
 'planet': {'text': ['Earthquake engineers read buildings through their eigenvalues. A USGS study by Mehmet Çelebi (2022) used the fundamental periods and critical damping percentages of 41 tall buildings in several countries. It found a clear linear trend between building height and fundamental period for steel and reinforced-concrete buildings, though with a large scatter from differing structural designs, and that critical damping was clearly lower than 3%, consistent with other recent tall-building studies.',
                     'The fundamental period is set by the smallest eigenvalue of the stiffness–mass problem, as in the two-story sample example. Low damping means a tall building can ring for a long time when long-period earthquake waves match that period, which is why instrumented buildings and their measured modes guide safer, longer-lasting cities.'],
            'site': [('Differential Equations', 'Differential_Equations.html'), ('Dynamics', 'Dynamics.html')],
            'src': [_BLD, ('Interactive Linear Algebra, 5.1 Eigenvalues and eigenvectors', _ILA + 'eigenvectors.html')]},
 'res': [('Interactive Linear Algebra, 5.1 Eigenvalues and eigenvectors', _ILA + 'eigenvectors.html', 'Free text section.'), ('Interactive Linear Algebra, 5.2 The characteristic polynomial', _ILA + 'characteristic-polynomial.html', 'Finding eigenvalues.'),
         ('Interactive Linear Algebra, 5.5 Complex eigenvalues', _ILA + 'complex-eigenvalues.html', 'Rotation and scaling.'), (_MIT[0], _MIT[1], 'Lecture 21: eigenvalues and eigenvectors.')]})
UNITS.append(
{'id': 'u9', 'title': 'Diagonalization, Matrix Powers, Markov Chains and Linear Dynamical Systems', 'weeks': 'Week 12',
 'summary': 'Diagonalizing A = PDP⁻¹, computing powers Aᵏ quickly, symmetric matrices and the spectral theorem A = QΛQᵀ, Markov (stochastic) matrices and steady states, and the long-run behavior of xₖ₊₁ = Axₖ.',
 'objectives': ['Diagonalize a matrix with n independent eigenvectors.', 'Compute Aᵏ and predict the long-run behavior of xₖ₊₁ = Axₖ.', 'Find the steady state of a Markov chain.', 'Use the spectral theorem for symmetric matrices.'],
 'concepts': ['If A has n independent eigenvectors (the columns of P), then A = PDP⁻¹ with the eigenvalues on the diagonal of D, and Aᵏ = PDᵏP⁻¹.',
              'Write x₀ = c₁v₁ + … + cₙvₙ. Then xₖ = Aᵏx₀ = c₁λ₁ᵏv₁ + … + cₙλₙᵏvₙ; the largest |λ| dominates as k grows.',
              'A Markov matrix has nonnegative entries and columns that sum to 1. It always has λ = 1, and the other eigenvalues satisfy |λ| ≤ 1. The steady state is the eigenvector for λ = 1, scaled so its entries sum to 1.',
              'The second-largest |λ| sets how fast a Markov chain forgets its start: the gap shrinks like |λ₂|ᵏ.',
              'Spectral theorem: a real symmetric matrix can be written A = QΛQᵀ with orthonormal eigenvectors in Q.'],
 'eqs': [('A=PDP^{-1},\\ \\ A^k=PD^kP^{-1}', 'Diagonalization and powers'), ('\\mathbf{x}_k=c_1\\lambda_1^k\\mathbf{v}_1+\\cdots+c_n\\lambda_n^k\\mathbf{v}_n', 'Solution of x_{k+1} = Ax_k'), ('P\\mathbf{q}=\\mathbf{q},\\ \\ \\textstyle\\sum q_i=1', 'Markov steady state'), ('A=Q\\Lambda Q^T', 'Spectral theorem')],
 'worked': [
  {'q': 'Use diagonalization to find A¹⁰ for A = [[2, 1], [1, 2]].', 'steps': ['From Unit 8: λ = 3, 1 with v = (1, 1), (1, −1). P = [[1, 1], [1, −1]], P⁻¹ = ½[[1, 1], [1, −1]].', 'A¹⁰ = P diag(3¹⁰, 1) P⁻¹; each entry is (3¹⁰ ± 1)/2.'], 'a': 'A¹⁰ = [[29525, 29524], [29524, 29525]].'},
  {'q': 'A Markov matrix is P = [[0.8, 0.3], [0.2, 0.7]] (sample values). Find the steady state.', 'steps': ['(P − I)q = 0: −0.2q₁ + 0.3q₂ = 0, so q₁ = 1.5q₂.', 'q₁ + q₂ = 1 gives q₂ = 0.4.'], 'a': 'q = (0.6, 0.4).'},
  {'q': 'Starting from x₀ = (1, 0), find x₂ for the same P, and the general xₖ.', 'steps': ['x₁ = (0.8, 0.2); x₂ = (0.64 + 0.06, 0.16 + 0.14).', 'Eigenvalues are 1 and 0.5 (trace 1.5, det 0.5), so xₖ = (0.6, 0.4) + 0.5ᵏ(0.4, −0.4).'], 'a': 'x₂ = (0.70, 0.30); xₖ → (0.6, 0.4).'}],
 'practice': [('Is [[0.5, 0.2], [0.5, 0.8]] a Markov matrix?', 'Yes: nonnegative, columns sum to 1.'), ('Find its steady state.', '0.5q₁ = 0.2q₂, so q = (2/7, 5/7) = (0.286, 0.714).'),
              ('If A = PDP⁻¹ with D = diag(0.9, 0.5), what happens to Aᵏx for large k?', 'It decays to zero, dominated by 0.9ᵏ.'), ('Can [[1, 1], [0, 1]] be diagonalized?', 'No: λ = 1 twice but only one independent eigenvector.')],
 'misc': [('Every matrix can be diagonalized.', 'It needs n independent eigenvectors; [[1, 1], [0, 1]] has only one.'), ('A Markov chain’s steady state depends on the start.', 'For a regular chain it does not; every start converges to the same q.'),
          ('Aᵏ means raising each entry to the k-th power.', 'Only diagonal matrices work that way; that is why we diagonalize.')],
 'quiz': [{'q': 'Every Markov matrix has the eigenvalue…', 'opts': ['0', '1', '−1', '2'], 'ok': 1, 'why': 'Columns sum to 1.'},
          {'q': 'Aᵏ for A = PDP⁻¹ is…', 'opts': ['PᵏDPᵏ', 'PDᵏP⁻¹', 'DᵏP', 'kPDP⁻¹'], 'ok': 1, 'why': 'Inner P⁻¹P cancel.'},
          {'q': 'The convergence speed of a Markov chain is set by…', 'opts': ['λ₁ = 1', '|λ₂|', 'the trace', 'n'], 'ok': 1, 'why': 'The gap shrinks like |λ₂|ᵏ.'},
          {'q': 'Symmetric matrices diagonalize as…', 'opts': ['LU', 'QΛQᵀ', 'QR', 'UΣVᵀ only'], 'ok': 1, 'why': 'Spectral theorem.'}],
 'cards': [('Diagonalization', 'A = PDP⁻¹.'), ('Matrix power', 'Aᵏ = PDᵏP⁻¹.'), ('Markov matrix', 'Nonnegative, columns sum to 1.'), ('Steady state', 'Pq = q, entries sum to 1.'), ('Spectral theorem', 'A = QΛQᵀ.'), ('Defective matrix', 'Too few eigenvectors to diagonalize.')],
 'planet': {'text': ['Where materials end up is a Markov chain. EPA reports that the United States generated 292.4 million tons of municipal solid waste in 2018, 4.9 pounds per person per day. About 69 million tons were recycled and 25 million tons composted, a combined 32.1% rate; about 35 million tons (11.8%) were burned with energy recovery; and more than 146 million tons (50%) were landfilled.',
                     'If each year’s shares stayed fixed, a material would leave use for these destinations with these probabilities, and only the recycled share would return to the economy. Lab E builds a sample transition matrix with a 32.1% recovery share and shows, with matrix powers and the λ = 1 eigenvector, how raising recycling changes how long material stays in use and how much reaches landfill.'],
            'site': [('Solutions', 'Solutions.html')],
            'src': [_MSW, ('Interactive Linear Algebra, 5.6 Stochastic matrices', _ILA + 'stochastic-matrices.html')]},
 'res': [('Interactive Linear Algebra, 5.4 Diagonalization', _ILA + 'diagonalization.html', 'Free text section.'), ('Interactive Linear Algebra, 5.6 Stochastic matrices', _ILA + 'stochastic-matrices.html', 'Markov chains and steady states.'),
         (_MIT[0], _MIT[1], 'Lectures 22–25: diagonalization, Markov matrices, symmetric matrices.'), (_MITSC[0], _MITSC[1], 'Recitations on Markov matrices.')]})
UNITS.append(
{'id': 'u10', 'title': 'The Singular Value Decomposition, Principal Component Analysis and Positive Definite Matrices', 'weeks': 'Weeks 13–14',
 'summary': 'Positive definite matrices and AᵀA, the SVD A = UΣVᵀ, singular values and the geometry of a matrix as rotate–stretch–rotate, best low-rank approximation and image compression, the condition number, and principal component analysis of data.',
 'objectives': ['Test a symmetric matrix for positive definiteness.', 'Compute singular values from the eigenvalues of AᵀA.', 'Build a rank-k approximation and measure what it keeps.', 'Run a small principal component analysis.'],
 'concepts': ['A symmetric matrix is positive definite when xᵀAx > 0 for every x ≠ 0; equivalently all eigenvalues (or all pivots) are positive. AᵀA is always symmetric and positive semidefinite.',
              'Every m × n matrix has an SVD A = UΣVᵀ: V and U have orthonormal columns, and Σ holds the singular values σ₁ ≥ σ₂ ≥ … ≥ 0, the square roots of the eigenvalues of AᵀA.',
              'A = σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + …. Keeping the first k terms gives the best rank-k approximation (Eckart–Young); the error in the 2-norm is σₖ₊₁.',
              'The condition number σ₁/σₙ measures how much errors in b can be amplified when solving Ax = b.',
              'PCA: center the data (subtract column means), then the right singular vectors (eigenvectors of the covariance matrix) are the principal directions, and σᵢ² measures the variance each explains.'],
 'eqs': [('A=U\\Sigma V^T', 'Singular value decomposition'), ('\\sigma_i=\\sqrt{\\lambda_i(A^TA)}', 'Singular values'), ('A_k=\\sum_{i=1}^{k}\\sigma_i\\mathbf{u}_i\\mathbf{v}_i^T', 'Best rank-k approximation'), ('\\kappa=\\sigma_1/\\sigma_n', 'Condition number')],
 'worked': [
  {'q': 'Find the singular values of A = [[3, 0], [4, 5]].', 'steps': ['AᵀA = [[25, 20], [20, 25]], eigenvalues 45 and 5.', 'σ₁ = √45, σ₂ = √5. Check: σ₁σ₂ = 15 = |det A|.'], 'a': 'σ₁ = 6.708, σ₂ = 2.236.'},
  {'q': 'What share of AᵀA’s “energy” Σσ² does the rank-1 approximation of that A keep?', 'steps': ['σ₁²/(σ₁² + σ₂²) = 45/50.'], 'a': '90%.'},
  {'q': 'A 1000 × 1000 grayscale image is stored as a rank-50 SVD. How many numbers are stored, compared with the full image?', 'steps': ['Each term needs one u (1000), one v (1000) and one σ: 2001 numbers.', '50 × 2001 = 100,050 versus 1,000,000.'], 'a': '100,050 numbers, about 10.0% of the original.'}],
 'practice': [('Is [[2, 1], [1, 2]] positive definite?', 'Yes: eigenvalues 3 and 1 are positive.'), ('Find the condition number of diag(10, 0.1).', '10/0.1 = 100.'),
              ('Centered 2D data have covariance [[2, 1], [1, 2]]. What share of the variance does the first principal component explain?', 'Eigenvalues 3 and 1: 3/4 = 75%, along (1, 1).'), ('What are the singular values of an orthogonal matrix?', 'All equal to 1.')],
 'misc': [('Singular values are the eigenvalues of A.', 'They are square roots of the eigenvalues of AᵀA, and are never negative.'), ('Only square matrices have an SVD.', 'Every matrix does.'),
          ('PCA works on raw data.', 'Center the data first, and scale variables measured in different units.')],
 'quiz': [{'q': 'Singular values are…', 'opts': ['any real numbers', 'nonnegative', 'always integers', 'eigenvalues of A'], 'ok': 1, 'why': 'Square roots of eigenvalues of AᵀA ≥ 0.'},
          {'q': 'The best rank-k approximation keeps…', 'opts': ['the first k rows', 'the k largest singular terms', 'k random columns', 'the k smallest σ'], 'ok': 1, 'why': 'Eckart–Young.'},
          {'q': 'A large condition number means…', 'opts': ['a well-behaved system', 'errors can be amplified', 'A is orthogonal', 'det A = 1'], 'ok': 1, 'why': 'Near-singular.'},
          {'q': 'In PCA, the first principal direction is…', 'opts': ['the mean', 'the top right singular vector of the centered data', 'the null space', 'the first row'], 'ok': 1, 'why': 'Direction of most variance.'}],
 'cards': [('SVD', 'A = UΣVᵀ.'), ('Singular value', 'σᵢ = √λᵢ(AᵀA).'), ('Positive definite', 'xᵀAx > 0, all λ > 0.'), ('Eckart–Young', 'Truncated SVD is the best rank-k approximation.'), ('Condition number', 'σ₁/σₙ.'), ('PCA', 'SVD of centered data.')],
 'planet': {'text': ['NASA JPL’s EMIT imaging spectrometer on the International Space Station maps the minerals in Earth’s dust-source regions. JPL says it collects more than 100,000 spectra every second, which is 3.6 × 10⁸ spectra an hour, and that its mission has been extended through at least 2026. Dust matters for climate: JPL notes that darker minerals absorb sunlight and warm the air, while lighter minerals reflect it and cool.',
                     'Each spectrum is a long vector of reflectances at many wavelengths, and neighboring wavelengths are strongly correlated. PCA and the SVD compress such data into a few components, separate signal from noise, and pick out the signatures of individual minerals, the same mathematics as the image-compression lab.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Space', 'Space.html')],
            'src': [_EMIT, _MIT]},
 'res': [(_MIT[0], _MIT[1], 'Lectures 27–29: positive definite matrices and the SVD.'), (_MITSC[0], _MITSC[1], 'Session on the singular value decomposition.'),
         (_GS[0], _GS[1], 'Strang’s notes on the SVD and data.'), (_HEF[0], _HEF[1], 'Topics on orthogonal matrices and projections.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Pixel vectors and a vegetation index', 'week': 'Week 2',
 'goal': 'Treat satellite pixels as vectors: compute lengths, angles between pixels and the NDVI, and see that vegetation, soil and water point in different directions.',
 'eq': ('\\cos\\theta=\\frac{\\mathbf{p}\\cdot\\mathbf{q}}{\\|\\mathbf{p}\\|\\|\\mathbf{q}\\|},\\quad \\text{NDVI}=\\frac{\\text{NIR}-\\text{red}}{\\text{NIR}+\\text{red}}', 'Angle between pixels and NDVI'),
 'steps': ['In a spreadsheet, enter three sample pixels as rows of (green, red, NIR) reflectances: vegetation (0.10, 0.08, 0.40), soil (0.20, 0.25, 0.30), water (0.06, 0.04, 0.02).', 'Compute each pixel’s length with SQRT(SUMSQ(…)) and each pair’s dot product with SUMPRODUCT.',
           'Find the angle between each pair with ACOS and DEGREES.', 'Compute NDVI for each pixel. Optional: download a free Landsat scene and repeat for real pixels.'],
 'table': (['Pixel', 'Green', 'Red', 'NIR', 'NDVI'], [['Vegetation', '0.10', '0.08', '0.40', '0.667'], ['Soil', '0.20', '0.25', '0.30', '0.091'], ['Water', '0.06', '0.04', '0.02', '−0.333']]),
 'note': 'Sample reflectances chosen to look like typical vegetation, bare soil and water.',
 'calc': ['Vegetation NDVI = (0.40 − 0.08)/(0.40 + 0.08) = 0.667.', 'Soil NDVI = 0.05/0.55 = 0.091; water NDVI = −0.02/0.06 = −0.333.', 'Angle vegetation–soil: dot = 0.160, lengths 0.420 and 0.4387, cos θ = 0.8683, θ = 29.7°.'],
 'safety': ['Take a short screen break every half hour.'], 'home': ['The whole lab runs in a free spreadsheet.'],
 'sims': [('PhET: Vector Addition', _PH + 'vector-addition'), ('USGS: Landsat 9', _L9[1])],
 'planet': 'USGS lists Landsat 9’s red (band 4) and near-infrared (band 5) bands, and its data are free, so anyone can map vegetation this way.', 'planet_src': [_L9]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Trilateration, from strings to a linear system', 'week': 'Week 3',
 'goal': 'Find a position from distances, first with strings on a map as in the GPS.gov activity, then by turning the circle equations into a linear system and solving it by elimination.',
 'eq': ('2(a_2-a_1)x+2(b_2-b_1)y=d_1^2-d_2^2+a_2^2-a_1^2+b_2^2-b_1^2', 'Difference of two circle equations'),
 'steps': ['Print the GPS.gov trilateration map (without scaling) or mark three “satellites” on graph paper at (0, 0), (10, 0) and (0, 10) cm.', 'Convert signal times to distances with d = ct (c = 299,792,458 m/s); for the paper version use the sample distances below.',
           'Draw circles with a string and pencil and mark where they cross.', 'Subtract the circle equations in pairs to get two linear equations, solve them by elimination in a spreadsheet, and compare with your drawing.'],
 'table': (['Beacon', 'Position (cm)', 'Distance (cm)', 'd²'], [['1', '(0, 0)', '5.000', '25'], ['2', '(10, 0)', '8.062', '65'], ['3', '(0, 10)', '6.708', '45']]),
 'note': 'Sample distances for a receiver at (3, 4) cm. The GPS.gov activity uses four satellites on a map at 1:21,283,839.',
 'calc': ['Eq. 1 − Eq. 2: 20x − 100 = −40, x = 3. Eq. 1 − Eq. 3: 20y − 100 = −20, y = 4.', 'GPS.gov time A = 0.00505783 s gives d = 1,516,299 m; at 1:21,283,839 that is 7.12 cm on the map.'],
 'safety': ['Handle push pins and scissors with care.'], 'home': ['The string-and-paper version is the home lab.'],
 'sims': [('GPS.gov: Trilateration activity', _GPST[1]), ('Interactive Linear Algebra, 1.2 Row reduction', _ILA + 'row-reduction.html')],
 'planet': 'GPS.gov designed this activity with NOAA; real receivers solve the same kind of system, with a clock unknown, many times a second.', 'planet_src': [_GPST, _GPSS]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Matrices as transformations of the plane', 'week': 'Week 4',
 'goal': 'See matrices act on shapes: stretch, shear, rotate and reflect a square on graph paper, and confirm that areas scale by |det A|.',
 'eq': ('\\text{area}(AS)=|\\det A|\\,\\text{area}(S)', 'Area scale factor'),
 'steps': ['Draw the unit square with corners (0, 0), (1, 0), (1, 1), (0, 1).', 'Multiply each corner by A = [[2, 1], [0, 1]] (a shear and stretch), by R = [[0, −1], [1, 0]] (a 90° rotation) and by F = [[1, 0], [0, −1]] (a reflection).',
           'Draw each image and find its area by counting squares or with the shoelace formula.', 'Compare each area with |det| and note which maps flip orientation (det < 0). Then check det(AR) = det A det R.'],
 'table': (['Matrix', 'det', 'Image area', 'Orientation'], [['A = [[2, 1], [0, 1]]', '2', '2', 'kept'], ['R (90° rotation)', '1', '1', 'kept'], ['F (reflection)', '−1', '1', 'flipped'], ['AR', '2', '2', 'kept']]),
 'note': 'Exact values for the unit square.',
 'calc': ['det A = 2 × 1 − 1 × 0 = 2; the image is a parallelogram with base 2 and height 1.', 'det(AR) = det A × det R = 2 × 1 = 2.'],
 'safety': ['None beyond normal desk work.'], 'home': ['Graph paper and a pencil are all you need.'],
 'sims': [('Interactive Linear Algebra, 3.1 Matrix transformations', _ILA + 'matrix-transformations.html'), ('Interactive Linear Algebra, 4.3 Determinants and volumes', _ILA + 'determinants-volumes.html')],
 'planet': 'Map projections and image registration use these same matrices; the determinant keeps area measurements of forests and floods honest.', 'planet_src': [_L9]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Least-squares fit of sea-level data', 'week': 'Week 9',
 'goal': 'Fit a line, and then a parabola, to sea-level data with the normal equations, and compare with the spreadsheet’s built-in fit.',
 'eq': ('A^TA\\hat{\\mathbf{x}}=A^T\\mathbf{b},\\quad A=[\\,\\mathbf{1}\\ \\ \\mathbf{t}\\,]', 'Normal equations for y = C + Dt'),
 'steps': ['Enter the sample data below (or download NASA’s record from its Vital Signs page): t in years since 1993 and h in mm.', 'Build A with a column of ones and a column of t. Compute AᵀA and Aᵀb with MMULT and TRANSPOSE, then x̂ = MINVERSE(AᵀA)·Aᵀb.',
           'Check against LINEST or a chart trendline. Plot the residuals b − Ax̂.', 'Add a t² column and refit. A positive t² coefficient means the rise is speeding up.'],
 'table': (['t (years since 1993)', '0', '8', '16', '24', '32'], [['h (mm)', '0', '22', '48', '78', '114']]),
 'note': 'Sample values shaped like the NASA record (which reports 114.4 mm of rise since 1993); use the real data for a real answer.',
 'calc': ['t̄ = 16, h̄ = 52.4; Σ(t − t̄)(h − h̄) = 2272, Σ(t − t̄)² = 640.', 'D = 2272/640 = 3.55 mm/yr; C = 52.4 − 3.55 × 16 = −4.4 mm.', 'The residuals are positive at both ends and negative in the middle: a curve fits better, as NASA’s rising rate suggests.'],
 'safety': ['Take a short screen break every half hour.'], 'home': ['The whole lab runs in a free spreadsheet.'],
 'sims': [('NASA: Global mean sea level', _SL[1]), ('Interactive Linear Algebra, 6.5 Least squares', _ILA + 'least-squares.html')],
 'planet': 'NASA reports the rate of rise grew from 0.20 cm per year in 1993 to 0.44 cm per year now, an acceleration you can detect with a t² column.', 'planet_src': [_SL]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: A Markov model of materials and recycling', 'week': 'Week 12',
 'goal': 'Build a transition matrix for material in use and lost to landfill or burning, use matrix powers to follow it over time, and see how a higher recycling rate keeps material in use longer.',
 'eq': ('\\mathbf{x}_{k+1}=P\\mathbf{x}_k,\\quad P=\\begin{bmatrix}1-f(1-r)&0\\\\f(1-r)&1\\end{bmatrix}', 'Two-state chain: in use, lost'),
 'steps': ['Choose a sample discard rate f = 0.2 per year and a recovery rate r = 0.321 (EPA’s 2018 recycling-plus-composting share).', 'Build P in a spreadsheet and start with x₀ = (1, 0): all material in use.',
           'Use MMULT to step forward 10 years, and compare with the formula (1 − f(1 − r))ᵏ for the share still in use.', 'Repeat with r = 0.5 and compare the average years in use, 1/(f(1 − r)).'],
 'table': (['Recovery rate r', 'Stay-in-use probability', 'In use after 10 years', 'Average years in use'], [['0.321', '0.8642', '0.232', '7.36'], ['0.50', '0.9000', '0.349', '10.0']]),
 'note': 'Sample model: the discard rate f = 0.2 is a sample value; r = 0.321 is the EPA 2018 share.',
 'calc': ['Stay probability = 1 − 0.2 × 0.679 = 0.8642; 0.8642¹⁰ = 0.232.', 'Average years in use = 1/0.1358 = 7.36; at r = 0.5 it is 1/0.1 = 10.0 years.', 'λ = 1 belongs to the “lost” state, which absorbs everything in the long run; λ = 0.8642 sets how fast.'],
 'safety': ['Take a short screen break every half hour.'], 'home': ['The whole lab runs in a free spreadsheet.'],
 'sims': [('Interactive Linear Algebra, 5.6 Stochastic matrices', _ILA + 'stochastic-matrices.html'), ('EPA: National overview of materials and waste', _MSW[1])],
 'planet': 'EPA reports a 32.1% recycling and composting rate in 2018 and 50% landfilled; models like this show what raising that rate is worth.', 'planet_src': [_MSW]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Power iteration and SVD image compression', 'week': 'Week 14',
 'goal': 'Find a dominant eigenvalue by repeated multiplication, then compress a small grayscale image with a truncated SVD and see how few numbers keep the picture.',
 'eq': ('\\mathbf{x}_{k+1}=\\frac{A\\mathbf{x}_k}{\\|A\\mathbf{x}_k\\|},\\quad A_k=\\sum_{i=1}^k\\sigma_i\\mathbf{u}_i\\mathbf{v}_i^T', 'Power iteration and truncated SVD'),
 'steps': ['In a spreadsheet, start with x₀ = (1, 0) and multiply by A = [[2, 1], [1, 2]] ten times, rescaling each time; watch the ratio of lengths approach 3.', 'Make an 8 × 8 grid of gray levels (0–255) for a simple picture, or load a photo in free Python with NumPy.',
           'Compute the SVD (numpy.linalg.svd) and rebuild the image with k = 1, 2 and 4 terms.', 'Record the storage k(8 + 8 + 1) and the share of Σσ² kept, and judge when the picture looks right.'],
 'table': (['k', 'Numbers stored (8 × 8 image)', 'Share of 64'], [['1', '17', '26.6%'], ['2', '34', '53.1%'], ['4', '68', '106.3%']]),
 'note': 'Exact storage counts. For an 8 × 8 image, k = 4 already stores more than the raw 64 numbers; the savings appear for large images (Unit 10: rank 50 of a 1000 × 1000 image keeps 10.0%).',
 'calc': ['Power iteration: (1, 0) → (2, 1) → (5, 4) → (14, 13); ‖(14, 13)‖/‖(5, 4)‖ = 19.10/6.403 = 2.98, near λ = 3.', 'Storage for k = 1: 8 + 8 + 1 = 17 numbers, 17/64 = 26.6%.'],
 'safety': ['Take a short screen break every half hour.'], 'home': ['The spreadsheet and free Python versions are both home labs.'],
 'sims': [(_MIT[0], _MIT[1]), ('Interactive Linear Algebra, 5.1 Eigenvectors', _ILA + 'eigenvectors.html')],
 'planet': 'NASA JPL’s EMIT returns more than 100,000 spectra every second; compressing and separating that data uses exactly these tools.', 'planet_src': [_EMIT]})
SCHEDULE = [(1, 'u1', 'Vectors, linear combinations, span, length', 'MIT 18.06 L1; ILA 2.1–2.2'), (2, 'u1', 'Dot products, angles, orthogonality; Lab A; start elimination', 'ILA 6.1'),
            (3, 'u2', 'Elimination, echelon forms, solution sets; Lab B', 'MIT 18.06 L2; ILA 1.1–1.3'), (4, 'u3', 'Matrix multiplication, inverses, A = LU; Lab C', 'MIT 18.06 L3–4; ILA 3.4–3.5'),
            (5, 'u4', 'Input–output models, networks, balancing', 'Hefferon Topics; EPA USEEIO'), (6, 'u5', 'Subspaces, column space, null space, Ax = 0', 'MIT 18.06 L5–7; ILA 2.6'),
            (7, 'u5', 'Independence, basis, dimension, rank, four subspaces; midterm practice', 'MIT 18.06 L8–10; ILA 2.5, 2.7, 2.9'), (8, 'u6', 'Orthogonality and projections', 'MIT 18.06 L14–15; ILA 6.3'),
            (9, 'u6', 'Least squares, Gram–Schmidt, A = QR; Lab D', 'MIT 18.06 L16–17; ILA 6.4–6.5'), (10, 'u7', 'Determinants, cofactors, Cramer’s rule, volume', 'MIT 18.06 L18–20; ILA 4.1–4.3'),
            (11, 'u8', 'Eigenvalues, eigenvectors, power iteration, modes', 'MIT 18.06 L21; ILA 5.1–5.2, 5.5'), (12, 'u9', 'Diagonalization, Markov chains, dynamical systems; Lab E', 'MIT 18.06 L22–25; ILA 5.4, 5.6'),
            (13, 'u10', 'Positive definite matrices and the SVD', 'MIT 18.06 L27–29'), (14, 'u10', 'Low-rank approximation, PCA, condition number; Lab F', 'MIT 18.06 L29; Strang book site'),
            (15, 'exam', 'Review and final practice set', 'All units')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Find the angle between (1, 0, 1) and (0, 1, 1).', ['Dot = 1; lengths √2 each; cos θ = 1/2.'], '60°.'),
  ('Solve x + 2y = 4, 3x − y = 5.', ['R₂ − 3R₁: −7y = −7.'], 'x = 2, y = 1.'),
  ('Invert [[3, 2], [1, 1]].', ['det = 1.'], '[[1, −2], [−1, 3]].'),
  ('A one-sector economy uses 0.4 of its own output. What output meets demand 120?', ['x = 120/0.6.'], '200.'),
  ('A 6 × 9 matrix has rank 4. Find dim N(A) and dim N(Aᵀ).', ['n − r and m − r.'], '5 and 2.')]),
 ('Final practice set (all units)', [
  ('Fit y = C + Dt to (0, 0), (1, 2), (2, 2) by least squares.', ['AᵀA = [[3, 3], [3, 5]], Aᵀb = (4, 6); det 6.'], 'C = 0.333, D = 1.'),
  ('Find det [[2, 1, 0], [1, 2, 1], [0, 1, 2]].', ['2(4 − 1) − 1(2 − 0) + 0.'], '4.'),
  ('Find the eigenvalues of [[6, 2], [2, 3]].', ['Trace 9, det 14: λ² − 9λ + 14 = 0.'], '7 and 2.'),
  ('Find the steady state of the Markov matrix [[0.9, 0.2], [0.1, 0.8]].', ['0.1q₁ = 0.2q₂.'], '(0.667, 0.333).'),
  ('Find the singular values of [[2, 0], [0, −3]].', ['AᵀA = diag(4, 9).'], '3 and 2.'),
  ('How many numbers does a rank-20 SVD of a 500 × 800 image store, and what share of the full image is that?', ['20(500 + 800 + 1).'], '26,020, about 6.5%.')])]
FORMULAS = ['\\|v\\|=\\sqrt{v\\cdot v},\\ \\cos\\theta=\\frac{v\\cdot w}{\\|v\\|\\|w\\|}', 'A\\mathbf{x}=\\mathbf{b},\\ \\ A=LU', '\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}^{-1}=\\frac{1}{ad-bc}\\begin{bmatrix}d&-b\\\\-c&a\\end{bmatrix}',
            '(AB)^{-1}=B^{-1}A^{-1},\\ (AB)^T=B^TA^T', '\\mathbf{x}=(I-A)^{-1}\\mathbf{d}', 'r+\\dim N(A)=n', '\\mathbf{p}=\\frac{a\\cdot b}{a\\cdot a}a,\\ \\ A^TA\\hat{x}=A^Tb', 'A=QR,\\ Q^TQ=I',
            '\\det(AB)=\\det A\\det B,\\ x_i=\\det B_i/\\det A', '\\det(A-\\lambda I)=0,\\ \\sum\\lambda=\\operatorname{tr}A,\\ \\prod\\lambda=\\det A', 'A=PDP^{-1},\\ A^k=PD^kP^{-1},\\ A=Q\\Lambda Q^T',
            'A=U\\Sigma V^T,\\ \\sigma_i=\\sqrt{\\lambda_i(A^TA)},\\ \\kappa=\\sigma_1/\\sigma_n']
GLOSSARY = sorted([('Basis', 'A linearly independent set that spans a space.'), ('Column space', 'All combinations Ax of the columns of A.'), ('Condition number', 'σ₁/σₙ, how much errors can grow when solving Ax = b.'),
    ('Determinant', 'Signed volume scale factor of A; zero exactly when A is singular.'), ('Diagonalization', 'A = PDP⁻¹ with eigenvectors in P.'), ('Dimension', 'Number of vectors in any basis.'),
    ('Eigenvalue', 'λ with Av = λv for some nonzero v.'), ('Leontief inverse', '(I − A)⁻¹, total output needed per unit of final demand.'), ('Least squares', 'The x̂ minimizing ‖b − Ax‖.'),
    ('Linear independence', 'Only the zero combination gives the zero vector.'), ('LU factorization', 'A = LU from elimination.'), ('Markov matrix', 'Nonnegative entries, columns summing to 1.'),
    ('Null space', 'All x with Ax = 0.'), ('Orthonormal', 'Mutually orthogonal unit vectors.'), ('Pivot', 'First nonzero entry of a row in echelon form.'), ('Positive definite', 'Symmetric with xᵀAx > 0 for x ≠ 0.'),
    ('Projection', 'Closest point to b in a subspace.'), ('Rank', 'Number of pivots; dimension of the column space.'), ('Singular value', 'σᵢ = √λᵢ(AᵀA).'), ('Span', 'All linear combinations of a set of vectors.'),
    ('Subspace', 'A set containing 0 that is closed under addition and scaling.')])
RUBRIC = [('4 · Mastery', 'Chooses the right tool (elimination, projection, eigenvalues or SVD), computes small cases by hand, checks answers (Ax = b, trace and determinant), and explains the meaning in pictures and in context.'), ('3 · Proficient', 'Solves the practice problems with occasional arithmetic slips.'),
          ('2 · Developing', 'Follows worked examples but mixes up rows and columns or the four subspaces.'), ('1 · Beginning', 'Manipulates symbols without checking sizes or answers; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '25%'), ('Labs', '20%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    from math import acos, degrees
    c = 299792458
    dot = lambda u, v: sum(a * b for a, b in zip(u, v))
    nrm = lambda u: sqrt(dot(u, u))
    ang = lambda u, v: degrees(acos(dot(u, v) / (nrm(u) * nrm(v))))
    d2 = lambda a, b, c_, d: a * d - b * c_
    d3 = lambda m: m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    def eig2(a, b, c_, d):
        t, D = a + d, a * d - b * c_; r = sqrt(t * t / 4 - D); return t / 2 + r, t / 2 - r
    def mm(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    def ls(ts, ys):
        n = len(ts); St = sum(ts); Stt = sum(t * t for t in ts); Sy = sum(ys); Sty = sum(t * y for t, y in zip(ts, ys)); det = n * Stt - St * St
        return (Stt * Sy - St * Sty) / det, (n * Sty - St * Sy) / det
    ndvi = lambda nir, red: (nir - red) / (nir + red)
    AB = mm([[1, 2], [3, 4]], [[0, 1], [1, 0]]); BA = mm([[0, 1], [1, 0]], [[1, 2], [3, 4]])
    dI = d2(.8, -.3, -.1, .6); x1 = (.6 * 100 + .3 * 50) / dI; x2 = (.1 * 100 + .8 * 50) / dI
    C1, D1 = ls([0, 1, 2], [1, 2, 4]); C2, D2 = ls([0, 8, 16, 24, 32], [0, 22, 48, 78, 114]); C3, D3 = ls([0, 1, 2], [0, 2, 2])
    g2 = (.5, -.5, 1); ng2 = nrm(g2)
    l1, l2 = eig2(2, -1, -1, 1); w1 = sqrt(100 * l2); f1 = w1 / (2 * pi)
    s1, s2 = sqrt(45), sqrt(5)
    st = 1 - .2 * (1 - .321); st5 = 1 - .2 * .5
    r = [
     ('u1 |34|', nrm((3, 4)), 5), ('u1 u', 3 / 5, .6), ('u1 u2', 4 / 5, .8), ('u1 dot', dot((3, 4), (1, 2)), 11), ('u1 sqrt5', sqrt(5), 2.236), ('u1 cos', 11 / (5 * sqrt(5)), .9839), ('u1 ang', ang((3, 4), (1, 2)), 10.30),
     ('u1 lc3', 2 * 1 + 3 * 1, 5), ('u1 |122|', nrm((1, 2, 2)), 3), ('u1 dot2', dot((1, 2, 3), (4, -5, 6)), 12), ('u1 orth', dot((2, -1), (1, 2)) + 1, 1), ('u1 |68|', nrm((6, 8)), 10),
     ('u1 bands', 9 + 2, 11), ('u1 14bit', 2**14, 16384), ('u1 ndvi', ndvi(.40, .08), .667), ('u1 ndvi num', .40 - .08, .32), ('u1 ndvi den', .40 + .08, .48),
     ('u2 z', 21 / 7, 3), ('u2 chk1', 1 + 2 + 3, 6), ('u2 chk2', 2 * 1 + 2 - 3, 1), ('u2 chk3', 1 - 2 + 2 * 3, 5), ('u2 R2', -2 * 1 + 2 * 1 + (-1 - 2), -3), ('u2 rhs', 1 - 12, -11),
     ('u2 bx', (-40 + 100) / 20, 3), ('u2 by', (-20 + 100) / 20, 4), ('u2 d2', (3 - 10)**2 + 4**2, 65), ('u2 d3', 3**2 + (4 - 10)**2, 45), ('u2 d1', 3**2 + 4**2, 25),
     ('u2 ct', c * .00505783, 1516299), ('u2 ct km', c * .00505783 / 1e3, 1516), ('u2 free', 5 - 3, 2), ('u2 1us', c * 1e-6, 299.8), ('u2 gps alt', 20200, 20200),
     ('u3 AB11', AB[0][0], 2), ('u3 AB12', AB[0][1], 1), ('u3 AB21', AB[1][0], 4), ('u3 AB22', AB[1][1], 3), ('u3 BA11', BA[0][0], 3), ('u3 BA12', BA[0][1], 4),
     ('u3 det', d2(4, 7, 2, 6), 10), ('u3 i11', 6 / 10, .6), ('u3 i12', -7 / 10, -.7), ('u3 i21', -2 / 10, -.2), ('u3 i22', 4 / 10, .4), ('u3 l21', 6 / 2, 3), ('u3 u22', 8 - 3 * 1, 5),
     ('u3 det2', d2(2, 1, 5, 3), 1), ('u3 n1000', 1000**3 / 3, 3.33e8), ('u3 dbl', 2**3, 8), ('u3 n1e5', 1e15 / 3, 3.33e14), ('u3 time', 1e15 / 3 / 14.5e15, .023), ('u3 noaa', 2 * 14.5, 29),
     ('u4 det', dI, .45), ('u4 x1', x1, 166.7), ('u4 x2', x2, 111.1), ('u4 fp', .5 * x1 + 2 * x2, 305.6), ('u4 L12', .3 / .45, .667), ('u4 one', 300 / .75, 400), ('u4 node', 40 + 25 - 30, 35),
     ('u4 389', 389**2, 151321), ('u4 ch4 y', (2 * 1 + 2) / 2, 2), ('u4 ch4 w', 4 / 2, 2),
     ('u5 null r1', -1 + 2 * -1 + 3, 0), ('u5 nullity', 3 - 2, 1), ('u5 dep', 2 * 4 - 1, 7), ('u5 dep2', 2 * 5 - 2, 8), ('u5 dep3', 2 * 6 - 3, 9),
     ('u5 N', 8 - 3, 5), ('u5 NT', 5 - 3, 2), ('u5 rank44', 4 - 2, 2), ('u5 grid', (13 / 9)**2, 2.09),
     ('u6 p', 5 / 2, 2.5), ('u6 e', 2 - 2.5, -.5), ('u6 C', C1, .833), ('u6 D', D1, 1.5), ('u6 n15', ng2, 1.225), ('u6 q1', 1 / sqrt(2), .707), ('u6 q2a', .5 / ng2, .408), ('u6 q2c', 1 / ng2, .816),
     ('u6 D16', 8 / 5, 1.6), ('u6 rate', .44 / .20, 2.2),
     ('u7 det3', d3([[1, 2, 0], [0, 1, 3], [2, 0, 1]]), 13), ('u7 cx', (15 - 10) / 5, 1), ('u7 cy', (20 - 5) / 5, 3), ('u7 area', d2(3, 1, 0, 2), 6), ('u7 d10', d2(3, 1, 2, 4), 10),
     ('u7 sing', d3([[2, 0, 1], [1, 3, 2], [1, 1, 1]]) + 1, 1), ('u7 2A', 8 * 4, 32), ('u7 inv', 1 / 5, .2), ('u7 px', 30 * 30, 900), ('u7 pan', 15 * 15, 225), ('u7 4pan', 900 / 225, 4), ('u7 ha', 1e4 / 900, 11.1),
     ('u8 l3', eig2(2, 1, 1, 2)[0], 3), ('u8 l1', eig2(2, 1, 1, 2)[1], 1), ('u8 l5', eig2(4, 1, 2, 3)[0], 5), ('u8 l2', eig2(4, 1, 2, 3)[1], 2), ('u8 bl', l2, .382), ('u8 bh', l1, 2.618),
     ('u8 w2', 100 * l2, 38.2), ('u8 w', w1, 6.18), ('u8 f', f1, .984), ('u8 T', 1 / f1, 1.02), ('u8 A2', 4**2, 16), ('u8 tr', 1 + 2 + 3, 6), ('u8 det', 1 * 2 * 3, 6),
     ('u9 A10a', (3**10 + 1) / 2, 29525), ('u9 A10b', (3**10 - 1) / 2, 29524), ('u9 q1', .3 / .5, .6), ('u9 x2a', .8 * .8 + .3 * .2, .70), ('u9 x2b', .2 * .8 + .7 * .2, .30), ('u9 l2', .8 + .7 - 1, .5),
     ('u9 fk', .6 + .5**2 * .4, .70), ('u9 st1', 2 / 7, .286), ('u9 st2', 5 / 7, .714), ('u9 rec', 69 + 25, 94), ('u9 rate', 94 / 292.4, .321), ('u9 lf', 146 / 292.4, .50),
     ('u10 s1', s1, 6.708), ('u10 s2', s2, 2.236), ('u10 prod', s1 * s2, 15), ('u10 en', 45 / 50, .90), ('u10 store', 50 * 2001, 100050), ('u10 share', 50 * 2001 / 1e6, .100), ('u10 kappa', 10 / .1, 100),
     ('u10 pca', 3 / 4, .75), ('u10 emit', 1e5 * 3600, 3.6e8),
     ('A cos', 1 / 2, .5), ('A ndvi soil', ndvi(.30, .25), .091), ('A ndvi water', ndvi(.02, .04), -.333), ('A dot', dot((.10, .08, .40), (.20, .25, .30)), .160), ('A lv', nrm((.10, .08, .40)), .420),
     ('A ls', nrm((.20, .25, .30)), .4387), ('A cos', dot((.10, .08, .40), (.20, .25, .30)) / (nrm((.10, .08, .40)) * nrm((.20, .25, .30))), .8683), ('A ang', ang((.10, .08, .40), (.20, .25, .30)), 29.7),
     ('B d2', sqrt(65), 8.062), ('B d3', sqrt(45), 6.708), ('B scale', c * .00505783 / 21283839 * 100, 7.12),
     ('C det', d2(2, 1, 0, 1), 2), ('C detR', d2(0, -1, 1, 0), 1), ('C detF', d2(1, 0, 0, -1), -1),
     ('D tbar', 16, 16), ('D hbar', (0 + 22 + 48 + 78 + 114) / 5, 52.4), ('D D', D2, 3.55), ('D C', C2, -4.4), ('D Sxy', 3.55 * 640, 2272),
     ('E st', st, .8642), ('E 10', st**10, .232), ('E yrs', 1 / (1 - st), 7.36), ('E st5', st5, .9), ('E 10b', st5**10, .349), ('E yrs5', 1 / (1 - st5), 10.0), ('E loss', .2 * .679, .1358),
     ('F ratio', sqrt(14**2 + 13**2) / sqrt(5**2 + 4**2), 2.98), ('F n1', sqrt(14**2 + 13**2), 19.10), ('F n2', sqrt(41), 6.403), ('F k1', 17 / 64, .266), ('F k2', 34 / 64, .531), ('F k4', 68 / 64, 1.063),
     ('M1', ang((1, 0, 1), (0, 1, 1)), 60), ('M2 y', 7 / 7, 1), ('M2 x', 4 - 2, 2), ('M3', d2(3, 2, 1, 1), 1), ('M4', 120 / .6, 200), ('M5', 9 - 4, 5),
     ('F1 C', C3, .333), ('F1 D', D3, 1), ('F2', d3([[2, 1, 0], [1, 2, 1], [0, 1, 2]]), 4), ('F3a', eig2(6, 2, 2, 3)[0], 7), ('F3b', eig2(6, 2, 2, 3)[1], 2), ('F4', .2 / .3, .667),
     ('F5', sqrt(9), 3), ('F6', 20 * 1301, 26020), ('F6 pct', 26020 / 400000, .065)]
    return r
