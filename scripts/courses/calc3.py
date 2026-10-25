"""Calculus III (MATH 210): vectors and 3D geometry, vector functions and motion, partial derivatives, gradients and optimization, multiple integrals and coordinate changes, vector fields, line and surface integrals, Green's, Stokes' and Divergence theorems.
Oct 25 2026, founder-approved four-year track, first sophomore course. Same module fields as chem110.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, sin, cos, exp, log, acos, atan, degrees, radians
ID = 'calc3'
STATUS = 'live'
YEAR = 2
PAGE = 'Calculus_III.html'
CODE = 'MATH 210'
TITLE = 'Calculus III'
LAB_TITLE = 'Computer labs'
TAGLINE = 'Multivariable calculus and vector fields: vectors, motion in space, partial derivatives, gradients and Lagrange multipliers, multiple integrals, and the theorems of Green, Stokes and Gauss, with four computer labs on winds, terrain, lakes and orbits.'
DESC = 'Free self-study Calculus III: vectors, partial derivatives, gradients, Lagrange multipliers, multiple integrals, vector fields, Green, Stokes, Divergence.'
ALT = 'NASA image of Earth'
OS = 'https://openstax.org/books/calculus-volume-3/pages/'
_O = OS
_PH = 'https://phet.colorado.edu/en/simulations/'
_EF = ('NASA Earth fact sheet', 'https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html')
_L9 = ('NASA: Landsat 9 quick facts', 'https://landsat.gsfc.nasa.gov/satellites/landsat-9/')
_EB = ('NASA Earth Observatory: Climate and Earth’s Energy Budget', 'https://earthobservatory.nasa.gov/features/EnergyBalance')
_GP = ('NOAA Marine Debris Program: Garbage patches', 'https://marinedebris.noaa.gov/discover-marine-debris/garbage-patches')
_GY = ('NOAA Ocean Service: Ocean currents tutorial (gyres)', 'https://oceanservice.noaa.gov/education/tutorial_currents/04currents4.html')
_CUR = ('NOAA Ocean Service: What is a current?', 'https://oceanservice.noaa.gov/facts/current.html')
_JW = ('NOAA/NWS JetStream: Wind', 'https://www.weather.gov/jetstream/wind')
_GFS = ('NOAA NCEI: Global Forecast System (GFS)', 'https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast')
_3DEP = ('USGS 3D Elevation Program (3DEP)', 'https://www.usgs.gov/3d-elevation-program')
_WT = ('U.S. DOE: How do wind turbines work?', 'https://www.energy.gov/eere/wind/how-do-wind-turbines-work')
_OHC = ('NOAA NCEI: Global ocean heat content', 'https://www.ncei.noaa.gov/access/global-ocean-heat-content/')
_NULL = ('earth.nullschool.net: live global wind and ocean-current map (from NOAA GFS and other public data)', 'https://earth.nullschool.net/')
BANNER = ['images/earth-blue-marble-land-ocean-ice-cloud.jpg', 'images/SWOT_Orbit_Illustration.jpg', 'images/GRACE_FO_PIA22445.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg']
CREDITS = {'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA', 'images/SWOT_Orbit_Illustration.jpg': 'CNES (PIA25623)', 'images/GRACE_FO_PIA22445.jpg': 'NASA/JPL-Caltech',
           'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows third-semester college calculus, modeled on the topics and depth of open materials such as OpenStax Calculus Volume 3 and MIT OpenCourseWare 18.02 Multivariable Calculus, and on the syllabi of courses such as Stanford Math 51/52 and Georgia Tech MATH 2551. We link to the free materials throughout. None of those organizations endorses this page.',
         'What we add: every unit connects to real wind, ocean, terrain, climate and satellite problems with a cited public source, every number on the page is re-computed by a checking script before it goes live, and four computer labs apply the ideas to wind fields, elevation grids, lake volumes and orbits.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['The planet is three-dimensional and always moving. Winds and ocean currents are vector fields, terrain and temperature are functions of two or three variables, heat and pollutants cross surfaces as flux, and the satellites that measure all of this follow vector-valued paths in space.',
                 'Each unit ends with a short, sourced section showing how its ideas help both people and nature.']
PREREQS = ['Calculus I and II: derivatives, integrals, substitution and integration by parts, parametric and polar curves.', 'Basic trigonometry and the equation of a circle and sphere.', 'Physics I helps for the work, flux and orbit examples but is not required.']
STUDY = ['Draw a 3D picture for every problem: axes, the region, the vectors.', 'Do every practice problem on paper before opening the answer.',
         'Check units and signs: a flux, work or circulation should make physical sense.', 'For multiple integrals, sketch the region and write the limits before integrating anything.',
         'Use a 3D grapher (Desmos 3D or GeoGebra 3D) to see surfaces and fields.', 'Retake the quizzes a few days later. Spaced practice beats one long session.']
LAB_GEAR = ['A computer or tablet with a spreadsheet.', 'A free 3D grapher such as Desmos 3D or GeoGebra 3D.', 'Optional: Python with NumPy (free in Google Colab).']
LAB_INTRO = ['Four computer labs apply the units: divergence and curl of a wind field from station data, slope and water-flow direction from an elevation grid, the volume of a lake by a polar double integral, and a satellite orbit stepped through time.',
             'Sample data is labeled as such; each lab links to the public data source to try next.']
SAFETY_SRC = ('OpenStax Calculus Volume 3 (free textbook)', 'https://openstax.org/books/calculus-volume-3/pages/1-introduction')
CONST_SRC = _EF
CONSTANTS = [('Earth’s GM', '3.986 × 10¹⁴ m³/s²'), ('Earth’s mean radius', '6,371 km'), ('Solar irradiance at Earth', '1,361 W/m²'), ('Mean surface pressure', '1,014 mb = 101,400 Pa'),
             ('Atmospheric scale height', '8.5 km'), ('Standard gravity', '9.81 m/s²')]
REF_TITLE = 'Graphing and data tools'
REF_INTRO = 'Use these free tools and data alongside the course.'
PTABLE = [('Desmos 3D calculator', 'https://www.desmos.com/3d', 'Graph surfaces, vectors and parametric curves in 3D.'),
          ('GeoGebra 3D', 'https://www.geogebra.org/3d', 'Another free 3D grapher.'),
          ('PhET: Vector Addition', _PH + 'vector-addition', 'Build intuition for components and sums.'),
          ('MIT OpenCourseWare 18.02SC', 'https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/', 'Free MIT lectures, recitations and problem sets.'),
          (_NULL[0], _NULL[1], 'See real wind and current vector fields worldwide.'),
          (_3DEP[0], _3DEP[1], 'Free U.S. elevation data for gradient and slope work.')]
UNITS = [
{'id': 'u1', 'title': 'Vectors and the Geometry of Space', 'weeks': 'Weeks 1–2',
 'summary': '3D coordinates, vectors, the dot and cross products, and equations of lines and planes.',
 'objectives': ['Add, scale and find the length of vectors in 3D.', 'Use the dot product for angles and projections.', 'Use the cross product for normals, areas and volumes.', 'Write equations of lines and planes, and find distances.'],
 'concepts': ['A vector has magnitude and direction; in components, v = ⟨v₁, v₂, v₃⟩ and |v| = √(v₁² + v₂² + v₃²).',
              'The dot product a · b = |a||b| cos θ measures how much two vectors point the same way. It is zero exactly when they are perpendicular.',
              'The cross product a × b is perpendicular to both, with length equal to the area of the parallelogram they span.',
              'A plane is fixed by a point and a normal vector n: n · (r − r₀) = 0. A line is a point plus multiples of a direction: r = r₀ + t v.'],
 'eqs': [('\\mathbf a\\cdot\\mathbf b=|\\mathbf a||\\mathbf b|\\cos\\theta', 'Dot product and angle'), ('\\operatorname{proj}_{\\mathbf b}\\mathbf a=\\frac{\\mathbf a\\cdot\\mathbf b}{|\\mathbf b|^2}\\mathbf b', 'Projection'),
         ('|\\mathbf a\\times\\mathbf b|=|\\mathbf a||\\mathbf b|\\sin\\theta', 'Cross product length = parallelogram area'), ('a(x-x_0)+b(y-y_0)+c(z-z_0)=0', 'Plane with normal ⟨a, b, c⟩'),
         ('D=\\frac{|ax_1+by_1+cz_1-d|}{\\sqrt{a^2+b^2+c^2}}', 'Distance from a point to the plane ax + by + cz = d')],
 'worked': [
  {'q': 'For a = ⟨1, 2, 2⟩ and b = ⟨2, −1, 2⟩, find |a|, a · b and the angle between them.', 'steps': ['|a| = √(1 + 4 + 4) = 3, and |b| = 3 too.', 'a · b = 2 − 2 + 4 = 4.', 'cos θ = 4/9, so θ = arccos(0.444).'], 'a': '|a| = 3, a · b = 4, θ ≈ 63.6°.'},
  {'q': 'Find a × b for the same vectors and the area of the parallelogram they span.', 'steps': ['a × b = ⟨2·2 − 2·(−1), 2·2 − 1·2, 1·(−1) − 2·2⟩.', '= ⟨6, 2, −5⟩. Check: it dots to 0 with a and with b.', 'Area = |⟨6, 2, −5⟩| = √65.'], 'a': '⟨6, 2, −5⟩; area √65 ≈ 8.06.'},
  {'q': 'A wind of 10 m/s blows at 30° to the axis of a wind turbine’s rotor. What fraction of the head-on power does the turbine see, if power grows with the cube of the wind speed along its axis?', 'steps': ['Component along the axis: 10 cos 30° = 8.66 m/s (a dot product with the unit axis vector).', 'Power ratio = (cos 30°)³.'], 'a': 'About 0.65: a 30° misalignment loses roughly a third of the power, which is why turbines yaw to face the wind.'}],
 'practice': [('Find the plane through (1, 0, 0), (0, 2, 0) and (0, 0, 3).', 'Intercept form x/1 + y/2 + z/3 = 1, i.e. 6x + 3y + 2z = 6.'), ('Find the distance from the origin to that plane.', '|−6|/√(36 + 9 + 4) = 6/7 ≈ 0.857.'),
              ('Find the projection of ⟨3, 4, 0⟩ onto ⟨1, 0, 0⟩.', '⟨3, 0, 0⟩.'), ('Find the volume of the box (parallelepiped) spanned by ⟨1, 0, 0⟩, ⟨0, 2, 0⟩ and ⟨1, 1, 3⟩.', '|a · (b × c)| = det = 1·(2·3 − 0·1) = 6.'),
              ('Are ⟨1, 2, 3⟩ and ⟨3, 0, −1⟩ perpendicular?', 'Dot product 3 + 0 − 3 = 0, so yes.')],
 'misc': [('a × b = b × a.', 'The cross product is anti-commutative: b × a = −(a × b).'), ('The dot product of two vectors is a vector.', 'It is a scalar (a number).'),
          ('A plane’s equation tells you its direction.', 'Its coefficients give the normal, which is perpendicular to the plane.')],
 'quiz': [{'q': 'If a · b = 0 (both nonzero), the vectors are…', 'opts': ['parallel', 'perpendicular', 'equal', 'opposite'], 'ok': 1, 'why': 'cos θ = 0, so θ = 90°.'},
          {'q': 'The length of a × b equals…', 'opts': ['the angle between them', 'the parallelogram’s area', 'a · b', '|a| + |b|'], 'ok': 1, 'why': '|a||b| sin θ.'},
          {'q': 'The normal to 2x − y + 5z = 7 is…', 'opts': ['⟨2, −1, 5⟩', '⟨7, 0, 0⟩', '⟨2, 1, 5⟩', '⟨1, 1, 1⟩'], 'ok': 0, 'why': 'Read off the coefficients.'},
          {'q': '|⟨2, 3, 6⟩| =', 'opts': ['11', '7', '√11', '49'], 'ok': 1, 'why': '√(4 + 9 + 36) = √49.'}],
 'cards': [('Dot product', 'a · b = |a||b| cos θ; zero when perpendicular.'), ('Cross product', 'Perpendicular to both; length = parallelogram area.'), ('Projection', '(a · b/|b|²) b.'),
           ('Triple product', '|a · (b × c)| = box volume.'), ('Plane', 'n · (r − r₀) = 0.'), ('Line', 'r = r₀ + t v.')],
 'planet': {'text': ['Wind is a vector, and turbines turn their rotors to face it because power depends on the cube of the component along the rotor axis, a dot product in disguise.',
                     'The same arithmetic tells a solar panel how much sunlight it catches: the useful part is the dot product of the sunlight direction with the panel’s normal vector.'],
            'site': [('Physics I, Unit 3: wind power', 'Physics_I.html#u3')],
            'src': [_WT, ('OpenStax Calculus 3, 2.3 The Dot Product', _O + '2-3-the-dot-product')]},
 'res': [('OpenStax Calculus 3, 2.3 The Dot Product', _O + '2-3-the-dot-product', 'Angles and projections.'), ('OpenStax Calculus 3, 2.4 The Cross Product', _O + '2-4-the-cross-product', 'Normals, areas and torque.'),
         ('OpenStax Calculus 3, 2.5 Equations of Lines and Planes in Space', _O + '2-5-equations-of-lines-and-planes-in-space', 'Lines, planes and distances.')]},

{'id': 'u2', 'title': 'Vector Functions and Motion in Space', 'weeks': 'Week 3',
 'summary': 'Curves in space as vector-valued functions: velocity, acceleration, arc length, curvature, and the motion of satellites.',
 'objectives': ['Differentiate and integrate vector-valued functions.', 'Find velocity, speed and acceleration along a path.', 'Compute arc length and curvature.', 'Analyze circular orbits with vector calculus.'],
 'concepts': ['A space curve is r(t) = ⟨x(t), y(t), z(t)⟩; differentiate component by component.', 'Velocity v = r′(t) is tangent to the path; speed is |v|; acceleration is a = v′.',
              'Arc length is the integral of speed: L = ∫|r′(t)| dt.', 'In uniform circular motion the speed is constant but the acceleration points to the center with size v²/r.'],
 'eqs': [('\\mathbf v=\\mathbf r\'(t),\\ \\mathbf a=\\mathbf r\'\'(t)', 'Velocity and acceleration'), ('L=\\int_a^b|\\mathbf r\'(t)|\\,dt', 'Arc length'),
         ('\\kappa=\\frac{|\\mathbf r\'\\times\\mathbf r\'\'|}{|\\mathbf r\'|^3}', 'Curvature'), ('v=\\sqrt{GM/r},\\ T=2\\pi r/v', 'Circular orbit speed and period')],
 'worked': [
  {'q': 'Find the length of one turn of the helix r(t) = ⟨cos t, sin t, t⟩, 0 ≤ t ≤ 2π.', 'steps': ['r′ = ⟨−sin t, cos t, 1⟩, speed √(sin²t + cos²t + 1) = √2.', 'L = ∫₀^(2π) √2 dt = 2π√2.'], 'a': '2π√2 ≈ 8.89.'},
  {'q': 'Landsat 9 orbits 705 km above Earth (mean radius 6,371 km). Treating the orbit as a circle, find its speed, acceleration and period.', 'steps': ['r = 7,076 km = 7.076 × 10⁶ m; GM = 3.986 × 10¹⁴ m³/s².', 'v = √(GM/r) = 7,505 m/s.', 'a = v²/r = 7.96 m/s², pointing to Earth’s center.', 'T = 2πr/v = 5,924 s.'], 'a': 'About 7.5 km/s and 98.7 minutes per orbit, matching NASA’s listed 99-minute period.'},
  {'q': 'Find the curvature of a circle of radius 2, r(t) = ⟨2 cos t, 2 sin t, 0⟩.', 'steps': ['r′ = ⟨−2 sin t, 2 cos t, 0⟩, |r′| = 2.', 'r′′ = ⟨−2 cos t, −2 sin t, 0⟩; r′ × r′′ = ⟨0, 0, 4⟩.', 'κ = 4/2³.'], 'a': 'κ = 1/2: a circle’s curvature is 1/radius.'}],
 'practice': [('A projectile has r(t) = ⟨20t, 20t − 4.9t²⟩ m. Find its velocity and speed at t = 1 s.', 'v = ⟨20, 20 − 9.8t⟩ = ⟨20, 10.2⟩; speed √(400 + 104.04) ≈ 22.45 m/s.'),
              ('Find the acceleration of r(t) = ⟨t², 3t, eᵗ⟩.', '⟨2, 0, eᵗ⟩.'), ('Find the length of r(t) = ⟨3t, 4t, 0⟩ for 0 ≤ t ≤ 2.', 'Speed 5, so L = 10.'),
              ('A satellite orbits at 35,786 km altitude. Find its period.', 'r = 42,157 km; T = 2π√(r³/GM) ≈ 86,160 s ≈ 23.93 h: one sidereal day, so it is geostationary.')],
 'misc': [('Constant speed means zero acceleration.', 'Turning is acceleration: a satellite in a circular orbit accelerates toward Earth the whole time.'),
          ('Arc length is |r(b) − r(a)|.', 'That is the straight-line distance; arc length integrates speed along the path.'),
          ('Higher satellites move faster.', 'v = √(GM/r) falls with distance; higher orbits are slower and longer.')],
 'quiz': [{'q': 'Velocity is…', 'opts': ['r(t)', 'r′(t)', '|r(t)|', '∫r dt'], 'ok': 1, 'why': 'The derivative of position.'},
          {'q': 'Arc length integrates…', 'opts': ['position', 'speed', 'acceleration', 'curvature'], 'ok': 1, 'why': 'L = ∫|r′| dt.'},
          {'q': 'Curvature of a circle of radius 5 is…', 'opts': ['5', '1/5', '25', '0'], 'ok': 1, 'why': 'κ = 1/R.'},
          {'q': 'Doubling a circular orbit’s radius changes its speed by a factor…', 'opts': ['2', '1/√2', '1/2', '√2'], 'ok': 1, 'why': 'v ∝ 1/√r.'}],
 'cards': [('Vector function', 'r(t) = ⟨x(t), y(t), z(t)⟩.'), ('Velocity', 'r′(t), tangent to the path.'), ('Speed', '|r′(t)|.'), ('Arc length', '∫|r′| dt.'), ('Curvature', '|r′ × r′′|/|r′|³.'), ('Circular orbit', 'v = √(GM/r).')],
 'planet': {'text': ['Earth-observing satellites such as Landsat 9 follow vector paths chosen with exactly these formulas. Its near-polar, sun-synchronous orbit at 705 km lets it image the same place every 16 days at about the same local time, so changes in forests, glaciers and cities stand out.'],
            'site': [('Landsat 9', 'Landsat_9.html'), ('Calculus II, Unit 7: polar orbits', 'Calculus_II.html#u7')],
            'src': [_L9, _EF]},
 'res': [('OpenStax Calculus 3, 3.2 Calculus of Vector-Valued Functions', _O + '3-2-calculus-of-vector-valued-functions', 'Derivatives and integrals.'),
         ('OpenStax Calculus 3, 3.4 Motion in Space', _O + '3-4-motion-in-space', 'Velocity, acceleration and Kepler’s laws.')]},

{'id': 'u3', 'title': 'Partial Derivatives', 'weeks': 'Weeks 4–5',
 'summary': 'Functions of several variables: level curves, partial derivatives, tangent planes, linear approximation and the multivariable chain rule.',
 'objectives': ['Read level curves and contour maps.', 'Compute partial derivatives and interpret them as rates.', 'Find tangent planes and use linear approximation.', 'Apply the multivariable chain rule.'],
 'concepts': ['A function z = f(x, y) is a surface; its level curves f = c are a contour map.', '∂f/∂x is the rate of change in x with y held fixed.',
              'Near a point, a smooth surface looks like its tangent plane: Δf ≈ fₓΔx + f_yΔy.', 'Chain rule: if x and y depend on t, df/dt = fₓ dx/dt + f_y dy/dt.'],
 'eqs': [('f_x=\\frac{\\partial f}{\\partial x}', 'Partial derivative'), ('z-z_0=f_x(x_0,y_0)(x-x_0)+f_y(x_0,y_0)(y-y_0)', 'Tangent plane'),
         ('\\frac{df}{dt}=f_x\\frac{dx}{dt}+f_y\\frac{dy}{dt}', 'Chain rule'), ('f_{xy}=f_{yx}', 'Clairaut’s theorem (smooth f)')],
 'worked': [
  {'q': 'For f(x, y) = x²y + y³, find fₓ and f_y at (1, 2), and use the tangent plane to estimate f(1.1, 1.9).', 'steps': ['fₓ = 2xy = 4; f_y = x² + 3y² = 13; f(1, 2) = 10.', 'f ≈ 10 + 4(0.1) + 13(−0.1) = 9.1.', 'True value: 1.21 × 1.9 + 6.859 = 9.158.'], 'a': 'Estimate 9.1 versus the true 9.158.'},
  {'q': 'For an ideal gas, P = nRT/V. With n = 1 mol, T = 300 K and V = 0.025 m³, find P, ∂P/∂T and ∂P/∂V.', 'steps': ['P = 8.314 × 300/0.025 = 99,768 Pa.', '∂P/∂T = nR/V = 332.6 Pa/K.', '∂P/∂V = −nRT/V² = −P/V = −3.99 × 10⁶ Pa/m³.'], 'a': 'P ≈ 99.8 kPa; warming 1 K raises it about 333 Pa; expanding lowers it.'},
  {'q': 'A drone flies with x = 2t, y = t². The temperature it measures is T = 20 + 0.1x − 0.05y (°C, km). Find dT/dt at t = 1.', 'steps': ['Tₓ = 0.1, T_y = −0.05; dx/dt = 2, dy/dt = 2t = 2.', 'dT/dt = 0.1(2) − 0.05(2).'], 'a': '0.1 °C per unit time.'}],
 'practice': [('Find fₓ and f_y for f = e^(xy).', 'fₓ = y e^(xy), f_y = x e^(xy).'), ('Find f_xy for f = x³y².', 'fₓ = 3x²y², f_xy = 6x²y (same as f_yx).'),
              ('Find the tangent plane to z = x² + y² at (1, 1, 2).', 'z = 2 + 2(x − 1) + 2(y − 1), i.e. z = 2x + 2y − 2.'),
              ('Estimate √(3.02² + 3.97²) by linear approximation at (3, 4).', 'f = 5, fₓ = 3/5, f_y = 4/5: 5 + 0.6(0.02) + 0.8(−0.03) = 4.988 (true 4.9880).')],
 'misc': [('∂f/∂x ignores y.', 'It holds y fixed; y can still appear in the answer.'), ('If both partials exist, f is smooth.', 'Partials can exist where f is not even continuous; differentiability needs more.'),
          ('Linear approximation is good anywhere.', 'Only near the base point.')],
 'quiz': [{'q': 'For f = x²y, fₓ =', 'opts': ['2x', '2xy', 'x²', 'x²y'], 'ok': 1, 'why': 'Treat y as a constant.'},
          {'q': 'Level curves of f(x, y) = x² + y² are…', 'opts': ['lines', 'circles', 'parabolas', 'points'], 'ok': 1, 'why': 'x² + y² = c.'},
          {'q': 'For smooth f, f_xy and f_yx are…', 'opts': ['opposite', 'equal', 'unrelated', 'zero'], 'ok': 1, 'why': 'Clairaut’s theorem.'},
          {'q': 'df/dt for f(x(t), y(t)) is…', 'opts': ['fₓ + f_y', 'fₓx′ + f_yy′', 'fₓf_y', 'x′y′'], 'ok': 1, 'why': 'Multivariable chain rule.'}],
 'cards': [('Partial derivative', 'Rate of change in one variable with the others fixed.'), ('Level curve', 'f(x, y) = c; a contour line.'), ('Tangent plane', 'z = z₀ + fₓΔx + f_yΔy.'),
           ('Linear approximation', 'Δf ≈ fₓΔx + f_yΔy.'), ('Chain rule', 'df/dt = fₓx′ + f_yy′.'), ('Clairaut', 'f_xy = f_yx for smooth f.')],
 'planet': {'text': ['Weather maps are contour maps of functions of two variables: isobars are level curves of pressure, isotherms of temperature. Partial derivatives tell forecasters how fast pressure or temperature changes eastward or northward, which drives the winds.'],
            'site': [('Calculus I', 'Calculus_I.html')],
            'src': [_JW, ('OpenStax Calculus 3, 4.3 Partial Derivatives', _O + '4-3-partial-derivatives')]},
 'res': [('OpenStax Calculus 3, 4.3 Partial Derivatives', _O + '4-3-partial-derivatives', 'Free textbook section.'),
         ('OpenStax Calculus 3, 4.4 Tangent Planes and Linear Approximations', _O + '4-4-tangent-planes-and-linear-approximations', 'Tangent planes.'),
         ('OpenStax Calculus 3, 4.5 The Chain Rule', _O + '4-5-the-chain-rule', 'Chain rule.')]},

{'id': 'u4', 'title': 'Gradients and Optimization', 'weeks': 'Weeks 6–7',
 'summary': 'The gradient vector, directional derivatives, critical points and the second-derivative test, and constrained optimization with Lagrange multipliers.',
 'objectives': ['Compute the gradient and directional derivatives.', 'Explain why the gradient points uphill and is perpendicular to level curves.', 'Classify critical points with the second-derivative test.', 'Solve constrained problems with Lagrange multipliers.'],
 'concepts': ['∇f = ⟨fₓ, f_y⟩ points in the direction of fastest increase, and its length is that fastest rate.', 'The rate of change in the direction of a unit vector u is D_u f = ∇f · u.',
              'The gradient is perpendicular to level curves, so water flows downhill along −∇h, across the contours.',
              'At an interior extremum ∇f = 0. The test D = f_xx f_yy − f_xy² decides: D > 0 and f_xx > 0 is a minimum; D < 0 is a saddle.',
              'To optimize f subject to g = c, solve ∇f = λ∇g: at the best point the level curve of f just touches the constraint.'],
 'eqs': [('\\nabla f=\\langle f_x,f_y,f_z\\rangle', 'Gradient'), ('D_{\\mathbf u}f=\\nabla f\\cdot\\mathbf u', 'Directional derivative'),
         ('D=f_{xx}f_{yy}-f_{xy}^2', 'Second-derivative test'), ('\\nabla f=\\lambda\\nabla g,\\quad g=c', 'Lagrange multiplier condition')],
 'worked': [
  {'q': 'A hill has height h(x, y) = 500 − 0.01x² − 0.02y² (meters, x and y in meters). At (100, 50), find ∇h, the steepest slope, and the slope heading toward ⟨3, 4⟩/5.', 'steps': ['∇h = ⟨−0.02x, −0.04y⟩ = ⟨−2, −2⟩.', 'Steepest uphill rate |∇h| = 2√2 = 2.83 m per m.', 'D_u h = ⟨−2, −2⟩ · ⟨0.6, 0.8⟩ = −2.8.'], 'a': 'Steepest climb 2.83 (uphill toward ⟨−1, −1⟩); heading ⟨3, 4⟩ you descend 2.8 m per m. Rain runs off along −∇h.'},
  {'q': 'Find and classify the critical point of f = x² + xy + y² − 3x.', 'steps': ['fₓ = 2x + y − 3 = 0, f_y = x + 2y = 0 give x = 2, y = −1.', 'f_xx = 2, f_yy = 2, f_xy = 1: D = 3 > 0, f_xx > 0.', 'f(2, −1) = 4 − 2 + 1 − 6 = −3.'], 'a': 'A minimum, f = −3 at (2, −1).'},
  {'q': 'A can must hold 1 liter (1,000 cm³). Which radius and height use the least metal (closed cylinder)?', 'steps': ['Minimize A = 2πr² + 2πrh with g = πr²h = 1,000.', '∇A = λ∇g gives 4πr + 2πh = λ2πrh and 2πr = λπr², so λ = 2/r and h = 2r.', 'πr²(2r) = 1,000 gives r = (500/π)^(1/3).'], 'a': 'r ≈ 5.42 cm, h ≈ 10.84 cm (height = diameter), area ≈ 554 cm².'}],
 'practice': [('Find ∇f for f = xyz at (1, 2, 3).', '⟨yz, xz, xy⟩ = ⟨6, 3, 2⟩.'), ('Find D_u f for f = x² + y² at (1, 1) toward ⟨1, 0⟩.', '∇f = ⟨2, 2⟩; D_u f = 2.'),
              ('Classify the critical point of f = x² − y².', 'At (0, 0): D = (2)(−2) − 0 = −4 < 0, a saddle.'),
              ('Fence a rectangle along a straight river with 40 m of fence (no fence on the river side). Maximize the area.', 'Maximize xy with x + 2y = 40: y = 10, x = 20, area 200 m².'),
              ('Maximize f = x + y on the circle x² + y² = 2.', '⟨1, 1⟩ = λ⟨2x, 2y⟩ gives x = y = 1; maximum 2.')],
 'misc': [('The gradient points along the level curve.', 'It is perpendicular to the level curve.'), ('∇f = 0 means a maximum or minimum.', 'It may be a saddle; use the D test.'),
          ('λ is just a trick to eliminate.', 'λ is the rate at which the best value changes as the constraint c changes, which is useful in economics and engineering.')],
 'quiz': [{'q': 'The gradient points…', 'opts': ['along level curves', 'in the direction of fastest increase', 'downhill', 'toward the origin'], 'ok': 1, 'why': 'Its length is the maximum rate.'},
          {'q': 'D < 0 at a critical point means…', 'opts': ['minimum', 'maximum', 'saddle', 'no conclusion'], 'ok': 2, 'why': 'Curving up one way, down another.'},
          {'q': 'Lagrange multipliers solve…', 'opts': ['∇f = 0', '∇f = λ∇g', 'f = g', 'f′ = λ'], 'ok': 1, 'why': 'Gradients are parallel at a constrained optimum.'},
          {'q': 'D_u f is largest when u is…', 'opts': ['perpendicular to ∇f', 'parallel to ∇f', 'opposite ∇f', 'any direction'], 'ok': 1, 'why': '∇f · u = |∇f| cos θ.'}],
 'cards': [('Gradient', '⟨fₓ, f_y, f_z⟩; fastest increase.'), ('Directional derivative', '∇f · u.'), ('Critical point', '∇f = 0.'), ('Saddle point', 'D < 0.'),
           ('Lagrange condition', '∇f = λ∇g.'), ('Steepest descent', 'Move along −∇f.')],
 'planet': {'text': ['Water flows down the gradient of terrain. Flood maps, watershed boundaries and erosion models are built by computing −∇h from elevation data, such as the free lidar elevation models of the USGS 3D Elevation Program.',
                     'Lagrange multipliers minimize material for a required volume or strength. Using less material for the same job is a direct cut in mining, energy and emissions.'],
            'site': [('Rivers hub', 'Rivers.html'), ('Engineering Graphics / CAD: lightweighting', 'Engineering_Graphics_CAD.html')],
            'src': [_3DEP, ('OpenStax Calculus 3, 4.8 Lagrange Multipliers', _O + '4-8-lagrange-multipliers')]},
 'res': [('OpenStax Calculus 3, 4.6 Directional Derivatives and the Gradient', _O + '4-6-directional-derivatives-and-the-gradient', 'Gradients.'),
         ('OpenStax Calculus 3, 4.7 Maxima/Minima Problems', _O + '4-7-maxima-minima-problems', 'Second-derivative test.'), ('OpenStax Calculus 3, 4.8 Lagrange Multipliers', _O + '4-8-lagrange-multipliers', 'Constrained optimization.')]},

{'id': 'u5', 'title': 'Double Integrals', 'weeks': 'Weeks 8–9',
 'summary': 'Integrating over regions in the plane: iterated integrals, Fubini’s theorem, general regions, polar coordinates, area, mass and averages.',
 'objectives': ['Evaluate double integrals as iterated integrals.', 'Set up limits for general regions and reverse the order.', 'Convert to polar coordinates with dA = r dr dθ.', 'Use double integrals for area, mass, averages and totals over a map.'],
 'concepts': ['∬_R f dA adds f times tiny areas. Over a rectangle, Fubini says integrate one variable, then the other, in either order.',
              'For a general region, the inner limits are curves; sketch the region to read them.', 'Round regions are easier in polar coordinates, where the area element is r dr dθ (not dr dθ).',
              'The average of f over R is ∬f dA divided by the area of R.'],
 'eqs': [('\\iint_Rf\\,dA=\\int_a^b\\!\\int_c^df(x,y)\\,dy\\,dx', 'Fubini’s theorem'), ('dA=r\\,dr\\,d\\theta', 'Polar area element'),
         ('\\bar f=\\frac{1}{\\text{Area}(R)}\\iint_Rf\\,dA', 'Average value'), ('\\int_{-\\infty}^{\\infty}e^{-x^2}dx=\\sqrt\\pi', 'Gaussian integral (via polar coordinates)')],
 'worked': [
  {'q': 'Evaluate ∬_R xy dA over R = [0, 2] × [0, 3].', 'steps': ['∫₀² x dx = 2 and ∫₀³ y dy = 4.5.', 'The integral separates: 2 × 4.5.'], 'a': '9.'},
  {'q': 'Rain falls on a 10 km × 5 km catchment with depth d(x, y) = 20 + 2x mm (x in km, across the 10 km side). How much water fell?', 'steps': ['Total = ∫₀¹⁰∫₀⁵ (20 + 2x) dy dx = 5 ∫₀¹⁰ (20 + 2x) dx.', '= 5(200 + 100) = 1,500 mm·km².', '1 mm over 1 km² is 1,000 m³.'], 'a': '1.5 × 10⁶ m³ (average depth 30 mm). This is how rain gauges and radar become river-flow forecasts.'},
  {'q': 'Evaluate ∬ e^(−(x² + y²)) dA over the unit disk, then over the whole plane.', 'steps': ['Polar: ∫₀^(2π)∫₀¹ e^(−r²) r dr dθ = 2π × ½(1 − e^(−1)).', 'Over the plane, the r-integral goes to ∞ and gives ½.'], 'a': 'π(1 − 1/e) ≈ 1.986 on the disk; π over the plane, which proves ∫e^(−x²) dx = √π.'}],
 'practice': [('∫₀¹∫₀ˣ x dy dx', '∫₀¹ x² dx = 1/3.'), ('Reverse the order of ∫₀¹∫_y¹ f dx dy.', '∫₀¹∫₀ˣ f dy dx.'), ('Find the area of a circle of radius a in polar coordinates.', '∫₀^(2π)∫₀ᵃ r dr dθ = πa².'),
              ('Find the volume under z = 4 − x² − y² above the disk x² + y² ≤ 4.', '∫₀^(2π)∫₀² (4 − r²) r dr dθ = 2π(8 − 4) = 8π ≈ 25.1.'),
              ('Average of f = x + y over [0, 1] × [0, 1].', '∬(x + y) dA = 1, area 1, average 1.')],
 'misc': [('In polar, dA = dr dθ.', 'dA = r dr dθ; forgetting r is the most common error.'), ('Inner limits must be numbers.', 'For a general region, inner limits are functions of the outer variable.'),
          ('Order never matters.', 'The value doesn’t, but the limits change, and one order is often much easier.')],
 'quiz': [{'q': 'Polar area element:', 'opts': ['dr dθ', 'r dr dθ', 'r² dr dθ', 'dθ/r'], 'ok': 1, 'why': 'A polar patch is r dθ by dr.'},
          {'q': '∬_R 1 dA equals…', 'opts': ['0', 'the area of R', 'the perimeter', '1'], 'ok': 1, 'why': 'Adds up the area.'},
          {'q': '∫₀¹∫₀² 3 dy dx =', 'opts': ['3', '5', '6', '2'], 'ok': 2, 'why': '3 × area 2.'},
          {'q': 'Fubini’s theorem lets you…', 'opts': ['skip limits', 'integrate one variable at a time', 'differentiate', 'use polar always'], 'ok': 1, 'why': 'Iterated integrals.'}],
 'cards': [('Double integral', '∬_R f dA.'), ('Fubini', 'Iterate in either order over a rectangle.'), ('Type I region', 'a ≤ x ≤ b, g₁(x) ≤ y ≤ g₂(x).'), ('Polar dA', 'r dr dθ.'),
           ('Average value', '∬f dA / Area.'), ('Gaussian integral', '∫e^(−x²) dx = √π.')],
 'planet': {'text': ['Totals over a map are double integrals: rain on a watershed, carbon stored in a forest, or crops harvested from a field. Hydrologists turn rainfall maps into volumes this way to predict floods and plan water supply.'],
            'site': [('Rivers hub', 'Rivers.html'), ('Deforestation hub', 'Deforestation.html')],
            'src': [('USGS Water Science School: Precipitation and the water cycle', 'https://www.usgs.gov/special-topics/water-science-school/science/precipitation-and-water-cycle'), ('OpenStax Calculus 3, 5.2 Double Integrals over General Regions', _O + '5-2-double-integrals-over-general-regions')]},
 'res': [('OpenStax Calculus 3, 5.1 Double Integrals over Rectangular Regions', _O + '5-1-double-integrals-over-rectangular-regions', 'Fubini.'),
         ('OpenStax Calculus 3, 5.2 Double Integrals over General Regions', _O + '5-2-double-integrals-over-general-regions', 'General regions.'),
         ('OpenStax Calculus 3, 5.3 Double Integrals in Polar Coordinates', _O + '5-3-double-integrals-in-polar-coordinates', 'Polar.')]},

{'id': 'u6', 'title': 'Triple Integrals and Change of Variables', 'weeks': 'Weeks 10–11',
 'summary': 'Integrating over solids in rectangular, cylindrical and spherical coordinates, and the Jacobian for general changes of variables.',
 'objectives': ['Set up and evaluate triple integrals.', 'Use cylindrical (r dz dr dθ) and spherical (ρ² sin φ dρ dφ dθ) coordinates.', 'Compute the Jacobian of a change of variables.', 'Find volumes, masses and centers of mass of solids.'],
 'concepts': ['∭_E f dV adds f over tiny boxes; with f = density it gives mass.', 'Cylindrical coordinates suit pipes, tanks and cones: dV = r dz dr dθ.',
              'Spherical coordinates suit balls and planets: dV = ρ² sin φ dρ dφ dθ.', 'Any substitution x = x(u, v) stretches area by the Jacobian |∂(x, y)/∂(u, v)|.'],
 'eqs': [('dV=r\\,dz\\,dr\\,d\\theta', 'Cylindrical volume element'), ('dV=\\rho^2\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta', 'Spherical volume element'),
         ('J=\\left|\\frac{\\partial(x,y)}{\\partial(u,v)}\\right|=|x_uy_v-x_vy_u|', 'Jacobian'), ('\\iint_Rf\\,dx\\,dy=\\iint_Sf\\,|J|\\,du\\,dv', 'Change of variables')],
 'worked': [
  {'q': 'Use spherical coordinates to find the volume of a ball of radius R.', 'steps': ['V = ∫₀^(2π)∫₀^π∫₀ᴿ ρ² sin φ dρ dφ dθ.', '= (R³/3)(2)(2π).'], 'a': '4πR³/3.'},
  {'q': 'Estimate the mass of Earth’s atmosphere: the weight of air above each square meter is the surface pressure, so M = ∬ p/g dA over the sphere.', 'steps': ['The surface integral of a constant is p/g times the area 4πR².', '4π(6.371 × 10⁶)² = 5.10 × 10¹⁴ m².', 'M = 101,400 × 5.10 × 10¹⁴ / 9.81.'], 'a': 'About 5.3 × 10¹⁸ kg, close to NASA’s 5.1 × 10¹⁸ kg (land above sea level holds up less air).'},
  {'q': 'Find the area of the ellipse x²/a² + y²/b² ≤ 1 with x = au, y = bv.', 'steps': ['The ellipse becomes the unit disk u² + v² ≤ 1.', 'J = ab.', 'Area = ab × π.'], 'a': 'πab.'}],
 'practice': [('Find the volume of the cone 0 ≤ z ≤ 1 − r (radius 1, height 1) in cylindrical coordinates.', '∫₀^(2π)∫₀¹ (1 − r) r dr dθ = 2π(1/2 − 1/3) = π/3.'),
              ('Evaluate ∭ 1 dV over the box [0, 1] × [0, 2] × [0, 3].', '6.'), ('Find the Jacobian of polar coordinates.', 'x_r y_θ − x_θ y_r = cos θ (r cos θ) + r sin θ (sin θ) = r.'),
              ('A cylinder of radius 1 m and height 2 m has density 1,000(1 − z/4) kg/m³. Find its mass.', 'π ∫₀² 1,000(1 − z/4) dz = π × 1,000 × 1.5 = 1,500π ≈ 4,712 kg.')],
 'misc': [('In spherical coordinates dV = dρ dφ dθ.', 'dV = ρ² sin φ dρ dφ dθ.'), ('φ runs from 0 to 2π.', 'φ (from the north pole) runs 0 to π; θ runs 0 to 2π.'),
          ('The Jacobian can be negative inside the integral.', 'Use its absolute value.')],
 'quiz': [{'q': 'The spherical volume element is…', 'opts': ['dρ dφ dθ', 'ρ² sin φ dρ dφ dθ', 'ρ dρ dθ', 'r dz dr dθ'], 'ok': 1, 'why': 'A spherical box of sides dρ, ρ dφ, ρ sin φ dθ.'},
          {'q': 'Cylindrical coordinates are best for…', 'opts': ['cubes', 'pipes and tanks', 'pyramids', 'planes'], 'ok': 1, 'why': 'Circular cross-sections.'},
          {'q': 'The Jacobian of x = 2u, y = 3v is…', 'opts': ['5', '6', '1', '2/3'], 'ok': 1, 'why': '2 × 3.'},
          {'q': 'Volume of a ball of radius 3:', 'opts': ['36π', '27π', '12π', '9π'], 'ok': 0, 'why': '4π(27)/3.'}],
 'cards': [('Triple integral', '∭_E f dV.'), ('Cylindrical', 'x = r cos θ, y = r sin θ, z; dV = r dz dr dθ.'), ('Spherical', 'dV = ρ² sin φ dρ dφ dθ.'),
           ('Jacobian', 'Area or volume stretch factor of a substitution.'), ('Mass', '∭ density dV.'), ('Center of mass', '∭ x ρ dV / mass.')],
 'planet': {'text': ['Climate scientists add up quantities through the volume of the ocean and atmosphere with exactly these integrals. Ocean heat content, the heat stored in the top 2,000 m of the sea, is a triple integral of temperature change times density and heat capacity, and it is one of the clearest records of global warming.'],
            'site': [('Oceans hub', 'Oceans.html')],
            'src': [_OHC, _EF]},
 'res': [('OpenStax Calculus 3, 5.4 Triple Integrals', _O + '5-4-triple-integrals', 'Free textbook section.'),
         ('OpenStax Calculus 3, 5.5 Triple Integrals in Cylindrical and Spherical Coordinates', _O + '5-5-triple-integrals-in-cylindrical-and-spherical-coordinates', 'Cylindrical and spherical.'),
         ('OpenStax Calculus 3, 5.7 Change of Variables in Multiple Integrals', _O + '5-7-change-of-variables-in-multiple-integrals', 'Jacobians.')]},

{'id': 'u7', 'title': 'Vector Fields, Line Integrals and Green’s Theorem', 'weeks': 'Week 12',
 'summary': 'Vector fields such as winds and currents, work and circulation along curves, conservative fields and potentials, and Green’s theorem in the plane.',
 'objectives': ['Sketch and interpret vector fields.', 'Evaluate line integrals of scalar functions and of vector fields (work).', 'Test whether a field is conservative and find a potential.', 'Apply Green’s theorem to circulation and flux in the plane.'],
 'concepts': ['A vector field assigns a vector to every point, like a wind or current map.', 'Work along a path is ∫_C F · dr; for a closed loop it is called circulation.',
              'A conservative field is a gradient, F = ∇φ; its work depends only on the endpoints, and it has zero circulation.',
              'Green’s theorem: circulation around a closed curve equals the integral of the curl (Q_x − P_y) over the region inside.'],
 'eqs': [('\\int_C\\mathbf F\\cdot d\\mathbf r=\\int_a^b\\mathbf F(\\mathbf r(t))\\cdot\\mathbf r\'(t)\\,dt', 'Line integral (work)'), ('\\int_C\\nabla\\varphi\\cdot d\\mathbf r=\\varphi(B)-\\varphi(A)', 'Fundamental theorem for line integrals'),
         ('\\oint_CP\\,dx+Q\\,dy=\\iint_D(Q_x-P_y)\\,dA', 'Green’s theorem'), ('\\text{Area}=\\tfrac12\\oint_Cx\\,dy-y\\,dx', 'Area from the boundary')],
 'worked': [
  {'q': 'F = ⟨y, x⟩. Find the work from (0, 0) to (2, 3) along any path.', 'steps': ['P_y = 1 = Q_x, so F is conservative.', 'φ = xy has ∇φ = ⟨y, x⟩.', 'Work = φ(2, 3) − φ(0, 0).'], 'a': '6, on every path.'},
  {'q': 'A gyre-like current F = ⟨−y, x⟩ circles the origin. Find its circulation around the unit circle directly and by Green’s theorem.', 'steps': ['r = ⟨cos t, sin t⟩, F · r′ = sin²t + cos²t = 1, so ∮ = 2π.', 'Green: Q_x − P_y = 1 − (−1) = 2; ∬2 dA = 2 × π.'], 'a': '2π ≈ 6.28 both ways.'},
  {'q': 'Use ½∮(x dy − y dx) to find the area inside x = 3 cos t, y = 2 sin t.', 'steps': ['x dy − y dx = (3 cos t)(2 cos t) + (2 sin t)(3 sin t) = 6 dt.', '½ ∫₀^(2π) 6 dt.'], 'a': '6π ≈ 18.85 (πab with a = 3, b = 2).'}],
 'practice': [('Is F = ⟨2xy, x² + 1⟩ conservative? Find φ.', 'P_y = 2x = Q_x; φ = x²y + y.'), ('Find ∫_C F · dr for F = ⟨x, y⟩ along y = x² from (0, 0) to (1, 1).', 'Conservative, φ = (x² + y²)/2: work 1.'),
              ('Find ∮(x² dx + xy dy) around the square [0, 1] × [0, 1], counterclockwise.', 'Green: ∬ y dA = 1/2.'),
              ('Find the circulation of F = ⟨−y, x⟩ around a circle of radius 3.', '2 × area = 18π ≈ 56.5.')],
 'misc': [('Every field with zero curl is conservative.', 'True only on simply connected regions (no holes).'), ('The work along a closed path is always zero.', 'Only for conservative fields; a gyre circulates.'),
          ('Green’s theorem works for any orientation.', 'It assumes counterclockwise; clockwise flips the sign.')],
 'quiz': [{'q': 'F = ∇φ means F is…', 'opts': ['rotational', 'conservative', 'zero', 'constant'], 'ok': 1, 'why': 'A gradient field.'},
          {'q': 'Work of a conservative field around a closed loop:', 'opts': ['2π', '0', 'its area', 'undefined'], 'ok': 1, 'why': 'φ(A) − φ(A).'},
          {'q': 'Green’s theorem links a line integral to…', 'opts': ['a derivative', 'a double integral', 'a triple integral', 'a series'], 'ok': 1, 'why': 'Boundary ↔ interior.'},
          {'q': 'Q_x − P_y for F = ⟨−y, x⟩ is…', 'opts': ['0', '1', '2', '−2'], 'ok': 2, 'why': '1 − (−1).'}],
 'cards': [('Vector field', 'A vector at every point.'), ('Line integral', '∫F · dr, work along a curve.'), ('Circulation', 'Line integral around a closed curve.'),
           ('Conservative', 'F = ∇φ; path-independent.'), ('Potential', 'φ with ∇φ = F.'), ('Green’s theorem', '∮P dx + Q dy = ∬(Q_x − P_y) dA.')],
 'planet': {'text': ['Ocean gyres are huge rotating current systems: there are five main ones, and each collects floating debris toward its center, forming the garbage patches. The circulation of a current field is a line integral, and Green’s theorem ties it to the rotation (curl) inside.',
                     'Winds and currents on maps such as earth.nullschool.net, which draws public NOAA forecast data, are vector fields you can read with this unit.'],
            'site': [('Oceans hub', 'Oceans.html')],
            'src': [_GP, _GY, _NULL]},
 'res': [('OpenStax Calculus 3, 6.1 Vector Fields', _O + '6-1-vector-fields', 'Fields.'), ('OpenStax Calculus 3, 6.2 Line Integrals', _O + '6-2-line-integrals', 'Work and circulation.'),
         ('OpenStax Calculus 3, 6.3 Conservative Vector Fields', _O + '6-3-conservative-vector-fields', 'Potentials.'), ('OpenStax Calculus 3, 6.4 Green’s Theorem', _O + '6-4-greens-theorem', 'Green’s theorem.')]},

{'id': 'u8', 'title': 'Surface Integrals, Stokes’ and the Divergence Theorem', 'weeks': 'Weeks 13–14',
 'summary': 'Divergence and curl, parametrized surfaces, flux through a surface, and the two great theorems that tie boundaries to interiors in 3D.',
 'objectives': ['Compute divergence and curl and interpret them as source strength and rotation.', 'Parametrize surfaces and compute surface area and flux.', 'Apply Stokes’ theorem.', 'Apply the Divergence (Gauss) theorem to net outward flux.'],
 'concepts': ['div F = ∇ · F measures outflow per volume; curl F = ∇ × F measures rotation.', 'Flux ∬_S F · n dS is how much of the field crosses a surface per unit time.',
              'Stokes: circulation around a surface’s edge equals the flux of curl F through the surface.', 'Divergence theorem: net outward flux through a closed surface equals the total divergence inside.'],
 'eqs': [('\\nabla\\cdot\\mathbf F=P_x+Q_y+R_z', 'Divergence'), ('\\nabla\\times\\mathbf F=\\langle R_y-Q_z,\\ P_z-R_x,\\ Q_x-P_y\\rangle', 'Curl'),
         ('\\oint_{\\partial S}\\mathbf F\\cdot d\\mathbf r=\\iint_S(\\nabla\\times\\mathbf F)\\cdot\\mathbf n\\,dS', 'Stokes’ theorem'),
         ('\\oiint_S\\mathbf F\\cdot\\mathbf n\\,dS=\\iiint_E\\nabla\\cdot\\mathbf F\\,dV', 'Divergence theorem')],
 'worked': [
  {'q': 'Find the outward flux of F = ⟨x, y, z⟩ through the sphere of radius R.', 'steps': ['div F = 3.', 'Divergence theorem: 3 × (4πR³/3).', 'Check directly: on the sphere F · n = R, so the flux is R × 4πR².'], 'a': '4πR³ both ways.'},
  {'q': 'Sunlight of 1,361 W/m² falls on Earth (radius 6,371 km). What total power does Earth intercept, and what is the average per square meter of its surface?', 'steps': ['The flux through Earth’s shadow disk is 1,361 × πR² = 1.735 × 10¹⁷ W.', 'Spread over the whole sphere (area 4πR²) it is 1,361/4.'], 'a': '1.74 × 10¹⁷ W, or 340 W/m² on average, the figure at the top of NASA’s energy-budget diagram.'},
  {'q': 'Verify Stokes’ theorem for F = ⟨−y, x, 0⟩ on the upper half of the unit sphere.', 'steps': ['curl F = ⟨0, 0, 2⟩.', 'Flux of curl through the hemisphere equals that through the flat unit disk (same edge): 2 × π.', 'The edge circulation is 2π (Unit 7).'], 'a': '2π both ways.'}],
 'practice': [('Find div and curl of F = ⟨x², yz, xy⟩.', 'div = 2x + z; curl = ⟨x − y, −y, 0⟩.'), ('Flux of F = ⟨0, 0, 5⟩ upward through the unit square in the plane z = 1.', '5 × 1 = 5.'),
              ('Use the Divergence theorem: flux of F = ⟨x, y, z⟩ out of the unit cube [0, 1]³.', 'div = 3; flux 3.'), ('Find the surface area of a sphere of radius 2 by integrating dS = 4 sin φ dφ dθ.', '4 × 2 × 2π = 16π ≈ 50.3.'),
              ('Is the curl of a gradient field ever nonzero?', 'No: ∇ × ∇φ = 0 for smooth φ.')],
 'misc': [('Flux is the same as circulation.', 'Flux crosses a surface; circulation runs along a curve.'), ('Divergence-free means nothing moves.', 'It means no net source: whatever flows in, flows out.'),
          ('The Divergence theorem works on open surfaces.', 'It needs a closed surface; Stokes handles surfaces with an edge.')],
 'quiz': [{'q': 'div ⟨x, y, z⟩ =', 'opts': ['0', '1', '3', 'x + y + z'], 'ok': 2, 'why': '1 + 1 + 1.'},
          {'q': 'Stokes’ theorem relates edge circulation to…', 'opts': ['flux of F', 'flux of curl F', 'div F', 'volume'], 'ok': 1, 'why': '∬(∇ × F) · n dS.'},
          {'q': 'The Divergence theorem needs…', 'opts': ['a closed surface', 'a curve', 'a flat region', 'a conservative field'], 'ok': 0, 'why': 'It encloses a solid.'},
          {'q': 'Average sunlight per square meter at Earth’s top of atmosphere is about…', 'opts': ['1,361 W/m²', '680 W/m²', '340 W/m²', '100 W/m²'], 'ok': 2, 'why': 'Disk area πR² over sphere area 4πR²: one quarter.'}],
 'cards': [('Divergence', '∇ · F; source strength.'), ('Curl', '∇ × F; rotation.'), ('Flux', '∬F · n dS.'), ('Stokes’ theorem', 'Edge circulation = flux of curl.'),
           ('Divergence theorem', 'Outward flux = ∭ div F dV.'), ('Closed surface', 'Encloses a solid; no edge.')],
 'planet': {'text': ['Earth’s climate is a flux balance: sunlight crosses the top of the atmosphere at about 340 W/m² on average, and Earth must send the same energy back out to space. When greenhouse gases trap some outgoing heat, the imbalance is a net flux into the planet, mostly stored in the ocean.',
                     'Pollutant transport is the same mathematics: the Divergence theorem says the pollutant leaving a lake or air basin through its boundary equals what its sources inside release, minus what is removed.'],
            'site': [('Earth Observation hub', 'Earth_Observation.html')],
            'src': [_EB, _EF]},
 'res': [('OpenStax Calculus 3, 6.5 Divergence and Curl', _O + '6-5-divergence-and-curl', 'Div and curl.'), ('OpenStax Calculus 3, 6.6 Surface Integrals', _O + '6-6-surface-integrals', 'Flux.'),
         ('OpenStax Calculus 3, 6.7 Stokes’ Theorem', _O + '6-7-stokes-theorem', 'Stokes.'), ('OpenStax Calculus 3, 6.8 The Divergence Theorem', _O + '6-8-the-divergence-theorem', 'Gauss.')]},
]
LABS = [
{'id': 'labA', 'title': 'Lab A: Divergence and curl of a wind field', 'week': 'Week 14',
 'goal': 'Estimate the divergence and curl of the wind at a point from four surrounding stations, and interpret them as rising air and storm rotation.',
 'eq': ('\\nabla\\cdot\\mathbf v\\approx\\frac{u_E-u_W}{2\\Delta}+\\frac{v_N-v_S}{2\\Delta},\\quad(\\nabla\\times\\mathbf v)_z\\approx\\frac{v_E-v_W}{2\\Delta}-\\frac{u_N-u_S}{2\\Delta}', 'Centered differences'),
 'steps': ['Enter the eastward (u) and northward (v) wind at stations 100 km east, west, north and south of a center (Δ = 100 km = 10⁵ m).', 'Compute the divergence and the vertical curl (vorticity).', 'Interpret the signs, then repeat with real winds read off earth.nullschool.net or NOAA forecast data.'],
 'table': (['Station', 'u (m/s, east)', 'v (m/s, north)'], [['East', '4', '8'], ['West', '6', '−6'], ['North', '−5', '−3'], ['South', '7', '−1']]),
 'note': 'Sample values for practice, not a real weather map.',
 'calc': ['Divergence = (4 − 6)/(2 × 10⁵) + (−3 − (−1))/(2 × 10⁵) = −2 × 10⁻⁵ s⁻¹: air converges, so it must rise, which favors clouds and rain.', 'Vorticity = (8 − (−6))/(2 × 10⁵) − (−5 − 7)/(2 × 10⁵) = 1.3 × 10⁻⁴ s⁻¹: positive, counterclockwise, like a Northern Hemisphere low.'],
 'safety': ['None beyond normal computer use.'], 'home': ['A spreadsheet is enough.'],
 'sims': [_NULL, _GFS],
 'planet': 'Convergence and vorticity are what forecasters track to warn of heavy rain and storms.', 'planet_src': [_JW]},
{'id': 'labB', 'title': 'Lab B: Slope and water flow from an elevation grid', 'week': 'Week 7',
 'goal': 'Estimate the gradient of terrain from a grid of elevations and find which way rainwater runs.',
 'eq': ('\\nabla h\\approx\\left\\langle\\frac{h_E-h_W}{2\\Delta},\\frac{h_N-h_S}{2\\Delta}\\right\\rangle', 'Gradient by centered differences'),
 'steps': ['Use elevations 100 m east, west, north and south of a point (Δ = 100 m).', 'Compute ∇h, its size (slope) and the slope angle arctan|∇h|.', 'The flow direction is −∇h. Then download a free USGS 3DEP elevation tile and repeat for a hillside near you.'],
 'table': (['Neighbor', 'Elevation (m)'], [['Center', '250'], ['East', '262'], ['West', '240'], ['North', '256'], ['South', '246']]),
 'note': 'Sample values for practice.',
 'calc': ['∇h ≈ ⟨(262 − 240)/200, (256 − 246)/200⟩ = ⟨0.11, 0.05⟩.', '|∇h| = 0.121, a slope angle of about 6.9°.', 'Water runs along −∇h, to the west-southwest; tracing these directions over a grid outlines a watershed.'],
 'safety': ['None beyond normal computer use.'], 'home': ['A spreadsheet is enough; GIS software is optional.'],
 'sims': [_3DEP],
 'planet': 'Flow directions from elevation grids are the basis of flood and erosion maps.', 'planet_src': [_3DEP]},
{'id': 'labC', 'title': 'Lab C: The volume of a lake by a polar double integral', 'week': 'Week 9',
 'goal': 'Compute the volume of a bowl-shaped lake exactly and with a numerical sum, and see how the error shrinks.',
 'eq': ('V=\\int_0^{2\\pi}\\!\\!\\int_0^RD\\left(1-\\frac{r^2}{R^2}\\right)r\\,dr\\,d\\theta=\\frac{\\pi R^2D}{2}', 'Lake with a paraboloid basin'),
 'steps': ['Take R = 1,000 m and maximum depth D = 20 m.', 'Compute the exact volume.', 'Split the lake into n rings, evaluate the depth at each ring’s middle radius, and add depth × ring area. Try n = 5 and n = 10.'],
 'table': (['Method', 'Volume (m³)'], [['Exact', '3.14 × 10⁷'], ['Midpoint, 5 rings', '3.20 × 10⁷'], ['Midpoint, 10 rings', '3.16 × 10⁷']]),
 'note': 'Computed values for a model lake.',
 'calc': ['Exact: π(1,000)²(20)/2 = 3.14 × 10⁷ m³ (31.4 million cubic meters).', 'The 5-ring sum is 2.0% high and the 10-ring sum 0.5% high: doubling n cuts the error about four times.'],
 'safety': ['None beyond normal computer use.'], 'home': ['A spreadsheet or Python.'],
 'sims': [('OpenStax Calculus 3, 5.3 Double Integrals in Polar Coordinates', _O + '5-3-double-integrals-in-polar-coordinates')],
 'planet': 'Lake and reservoir volumes from depth surveys tell water managers how much they can store and release.', 'planet_src': [('NASA: SWOT mission', 'https://swot.jpl.nasa.gov/')]},
{'id': 'labD', 'title': 'Lab D: Stepping a satellite orbit through time', 'week': 'Week 3',
 'goal': 'Integrate r′′ = −GM r/|r|³ numerically for a Landsat-like orbit and compare two stepping methods.',
 'eq': ('\\mathbf v_{n+1}=\\mathbf v_n-\\frac{GM\\,\\mathbf r_n}{|\\mathbf r_n|^3}\\Delta t,\\quad\\mathbf r_{n+1}=\\mathbf r_n+\\mathbf v_{n+1}\\Delta t', 'Semi-implicit (symplectic) Euler'),
 'steps': ['Start at r = ⟨7,076 km, 0⟩ with v = ⟨0, 7,505 m/s⟩ (Unit 2).', 'Step 592 times with Δt = 10 s (one period), first with plain Euler (update r with the old v), then with the semi-implicit version above.', 'Compare the final radius with the start.'],
 'table': (['Method (Δt = 10 s)', 'Radius change after one orbit'], [['Plain Euler', '+908 km'], ['Semi-implicit Euler', '+0.16 km']]),
 'note': 'Computed values; GM = 3.986 × 10¹⁴ m³/s².',
 'calc': ['Plain Euler spirals outward by about 908 km per orbit, a useless forecast; even Δt = 1 s still drifts about 94 km.', 'The semi-implicit update changes one line of code and keeps the orbit to within about 0.16 km.'],
 'safety': ['None beyond normal computer use.'], 'home': ['A spreadsheet works; Python in Colab is easier.'],
 'sims': [('Google Colab (free notebooks)', 'https://colab.research.google.com/'), _L9],
 'planet': 'Accurate orbit propagation keeps Earth-observing satellites on their repeat tracks.', 'planet_src': [_L9]},
]
SCHEDULE = [(1, 'u1', '3D coordinates, vectors, dot product', 'OpenStax 2.1–2.3'), (2, 'u1', 'Cross product, lines and planes', 'OpenStax 2.4–2.5'),
            (3, 'u2', 'Vector functions, motion in space, curvature; Lab D', 'OpenStax 3.1–3.4'), (4, 'u3', 'Functions of several variables, limits, partial derivatives', 'OpenStax 4.1–4.3'),
            (5, 'u3', 'Tangent planes, linear approximation, chain rule', 'OpenStax 4.4–4.5'), (6, 'u4', 'Gradient, directional derivatives, extrema', 'OpenStax 4.6–4.7'),
            (7, 'u4', 'Lagrange multipliers; Lab B; midterm practice', 'OpenStax 4.8'), (8, 'u5', 'Double integrals over rectangles and general regions', 'OpenStax 5.1–5.2'),
            (9, 'u5', 'Polar double integrals; Lab C', 'OpenStax 5.3'), (10, 'u6', 'Triple integrals; cylindrical and spherical coordinates', 'OpenStax 5.4–5.5'),
            (11, 'u6', 'Mass and center of mass; change of variables', 'OpenStax 5.6–5.7'), (12, 'u7', 'Vector fields, line integrals, conservative fields, Green’s theorem', 'OpenStax 6.1–6.4'),
            (13, 'u8', 'Divergence and curl; surface integrals and flux', 'OpenStax 6.5–6.6'), (14, 'u8', 'Stokes’ and Divergence theorems; Lab A', 'OpenStax 6.7–6.8'), (15, 'exam', 'Review and final practice set', 'All units')]
EXAMS = [('Midterm practice set (Units 1–4)', [
  ('Find the angle between ⟨1, 1, 0⟩ and ⟨0, 1, 1⟩.', ['Dot product 1; both lengths √2.', 'cos θ = 1/2.'], '60°.'),
  ('Find the plane through (1, 1, 1) with normal ⟨2, −1, 3⟩.', ['2(x − 1) − (y − 1) + 3(z − 1) = 0.'], '2x − y + 3z = 4.'),
  ('A satellite orbits at radius 6,771 km (400 km altitude). Find its period.', ['T = 2π√(r³/GM).'], '≈ 5,544 s ≈ 92.4 min.'),
  ('Maximize f = xy subject to x + y = 10.', ['⟨y, x⟩ = λ⟨1, 1⟩ gives x = y = 5.'], '25 at (5, 5).')]),
 ('Final practice set (all units)', [
  ('Evaluate ∫₀^(2π)∫₀³ r dr dθ.', ['4.5 × 2π.'], '9π ≈ 28.3 (area of a disk of radius 3).'),
  ('Find the volume of a hemisphere of radius 2 with spherical coordinates.', ['∫₀^(2π)∫₀^(π/2)∫₀² ρ² sin φ dρ dφ dθ = (8/3)(1)(2π).'], '16π/3 ≈ 16.76.'),
  ('Find ∮ F · dr for F = ⟨−y, x⟩ around the square [0, 2] × [0, 2], counterclockwise.', ['Green: ∬2 dA = 2 × 4.'], '8.'),
  ('Find the outward flux of F = ⟨2x, 0, 0⟩ through the sphere of radius 1.', ['div F = 2; flux = 2 × 4π/3.'], '8π/3 ≈ 8.38.')])]
FORMULAS = ['\\mathbf a\\cdot\\mathbf b=|\\mathbf a||\\mathbf b|\\cos\\theta', '|\\mathbf a\\times\\mathbf b|=|\\mathbf a||\\mathbf b|\\sin\\theta', 'n\\cdot(\\mathbf r-\\mathbf r_0)=0',
            'L=\\int|\\mathbf r\'(t)|\\,dt', '\\kappa=|\\mathbf r\'\\times\\mathbf r\'\'|/|\\mathbf r\'|^3', 'v=\\sqrt{GM/r}', '\\Delta f\\approx f_x\\Delta x+f_y\\Delta y',
            'D_{\\mathbf u}f=\\nabla f\\cdot\\mathbf u', 'D=f_{xx}f_{yy}-f_{xy}^2', '\\nabla f=\\lambda\\nabla g', 'dA=r\\,dr\\,d\\theta', 'dV=r\\,dz\\,dr\\,d\\theta',
            'dV=\\rho^2\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta', '\\int_C\\nabla\\varphi\\cdot d\\mathbf r=\\varphi(B)-\\varphi(A)', '\\oint P\\,dx+Q\\,dy=\\iint(Q_x-P_y)\\,dA',
            '\\oint\\mathbf F\\cdot d\\mathbf r=\\iint(\\nabla\\times\\mathbf F)\\cdot\\mathbf n\\,dS', '\\oiint\\mathbf F\\cdot\\mathbf n\\,dS=\\iiint\\nabla\\cdot\\mathbf F\\,dV']
GLOSSARY = sorted([('Circulation', 'Line integral of a field around a closed curve.'), ('Conservative field', 'A gradient field; work is path-independent.'), ('Cross product', 'Vector perpendicular to two vectors.'),
    ('Curl', '∇ × F; local rotation of a field.'), ('Curvature', 'How sharply a curve bends; 1/R for a circle.'), ('Directional derivative', 'Rate of change in a given direction, ∇f · u.'),
    ('Divergence', '∇ · F; net outflow per volume.'), ('Divergence theorem', 'Outward flux through a closed surface equals the integral of the divergence inside.'), ('Dot product', 'a · b = |a||b| cos θ.'),
    ('Flux', 'Amount of a field crossing a surface.'), ('Gradient', 'Vector of partial derivatives; points uphill.'), ('Green’s theorem', 'Circulation around a plane curve equals the integral of Q_x − P_y inside.'),
    ('Jacobian', 'Stretch factor of a change of variables.'), ('Lagrange multiplier', 'λ in ∇f = λ∇g for constrained optimization.'), ('Level curve', 'Curve where f(x, y) is constant.'),
    ('Line integral', 'Integral along a curve.'), ('Partial derivative', 'Derivative in one variable with the others fixed.'), ('Saddle point', 'Critical point that is neither a max nor a min.'),
    ('Stokes’ theorem', 'Edge circulation equals the flux of the curl.'), ('Vector field', 'Assignment of a vector to each point.')])
RUBRIC = [('4 · Mastery', 'Sets up integrals and fields from a picture unprompted, picks good coordinates, and checks answers by a second method or a theorem.'), ('3 · Proficient', 'Solves the practice problems with occasional slips.'),
          ('2 · Developing', 'Follows worked examples but struggles to set up limits or choose coordinates.'), ('1 · Beginning', 'Applies formulas without sketching or checking; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '30%'), ('Computer labs', '15%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    GM = 3.986e14
    def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    def dot(a, b): return sum(x * y for x, y in zip(a, b))
    nrm = lambda a: sqrt(dot(a, a))
    a, b = (1, 2, 2), (2, -1, 2); c = cross(a, b)
    def mid2(f, a1, b1, a2, b2, n=400):
        hx, hy = (b1 - a1) / n, (b2 - a2) / n
        return sum(f(a1 + (i + .5) * hx, a2 + (j + .5) * hy) for i in range(n) for j in range(n)) * hx * hy
    def orbit(dt, semi):
        r0 = 7.076e6; v0 = sqrt(GM / r0); T = 2 * pi * r0 / v0
        x, y, vx, vy = r0, 0., 0., v0
        for _ in range(round(T / dt)):
            r3 = (x * x + y * y)**1.5; ax, ay = -GM * x / r3, -GM * y / r3
            if semi: vx += ax * dt; vy += ay * dt; x += vx * dt; y += vy * dt
            else: x, y, vx, vy = x + vx * dt, y + vy * dt, vx + ax * dt, vy + ay * dt
        return (sqrt(x * x + y * y) - r0) / 1000
    def lake(n, R=1000, D=20): return sum(D * (1 - ((i + .5) * R / n)**2 / R**2) * 2 * pi * (i + .5) * R / n * R / n for i in range(n))
    rL = 7.076e6; vL = sqrt(GM / rL)
    f = lambda x, y: x * x * y + y**3
    circ = lambda F, n=2000: sum(dot(F(cos(t), sin(t)), (-sin(t), cos(t))) for t in [2 * pi * (k + .5) / n for k in range(n)]) * 2 * pi / n
    rcan = (500 / pi)**(1 / 3)
    gx, gy = .11, .05
    return [('|a|', nrm(a), 3), ('ab', dot(a, b), 4), ('angle', degrees(acos(4 / 9)), 63.6), ('cx0', c[0], 6), ('cx1', c[1], 2), ('cx2', c[2], -5), ('perp', dot(c, a) + 1, 1), ('area', nrm(c), 8.06),
            ('turb', 10 * cos(radians(30)), 8.66), ('turbP', cos(radians(30))**3, .65), ('plane d', 6 / 7, .857), ('box', abs(dot((1, 0, 0), cross((0, 2, 0), (1, 1, 3)))), 6),
            ('helix', 2 * pi * sqrt(2), 8.89), ('Lv', vL, 7505), ('La', vL**2 / rL, 7.96), ('LT', 2 * pi * rL / vL, 5924), ('LTm', 2 * pi * rL / vL / 60, 98.7), ('kappa', 4 / 8, .5),
            ('proj speed', sqrt(400 + 10.2**2), 22.45), ('geo', 2 * pi * sqrt(4.2157e7**3 / GM) / 3600, 23.93), ('geo s', 2 * pi * sqrt(4.2157e7**3 / GM), 86160),
            ('f', f(1, 2), 10), ('lin', 10 + .4 - 1.3, 9.1), ('true', f(1.1, 1.9), 9.158), ('P', 8.314 * 300 / .025, 99768), ('dPdT', 8.314 / .025, 332.6), ('dPdV', -8.314 * 300 / .025**2, -3.99e6),
            ('dT', .1 * 2 - .05 * 2, .1), ('sqrt lin', 5 + .6 * .02 - .8 * .03, 4.988), ('sqrt true', sqrt(3.02**2 + 3.97**2), 4.988),
            ('hill', 2 * sqrt(2), 2.83), ('Du', -2 * .6 - 2 * .8, -2.8), ('crit', 4 - 2 + 1 - 6, -3), ('D', 2 * 2 - 1, 3), ('can r', rcan, 5.42), ('can h', 2 * rcan, 10.84), ('can A', 6 * pi * rcan**2, 554),
            ('can V', pi * rcan**2 * 2 * rcan, 1000), ('fence', 20 * 10, 200), ('circmax', 2, 2),
            ('xy', mid2(lambda x, y: x * y, 0, 2, 0, 3), 9), ('rain', mid2(lambda x, y: 20 + 2 * x, 0, 10, 0, 5) * 1000, 1.5e6), ('rain avg', 1500 / 50, 30),
            ('gauss disk', pi * (1 - exp(-1)), 1.986), ('gauss disk num', mid2(lambda x, y: exp(-(x * x + y * y)) if x * x + y * y <= 1 else 0, -1, 1, -1, 1, 800), 1.986),
            ('tri', 1 / 3, 1 / 3), ('parab', 8 * pi, 25.1), ('parab num', mid2(lambda r, t: (4 - r * r) * r, 0, 2, 0, 2 * pi), 8 * pi),
            ('ball', 4 / 3 * pi * 2**3, 4 / 3 * pi * 8), ('earth A', 4 * pi * 6.371e6**2, 5.10e14), ('atm', 101400 * 4 * pi * 6.371e6**2 / 9.81, 5.3e18), ('cone', 2 * pi * (1 / 2 - 1 / 3), pi / 3),
            ('cylmass', pi * 1000 * (2 - 4 / 8), 4712), ('ellipse', 6 * pi, 18.85),
            ('work', 2 * 3, 6), ('circ gyre', circ(lambda x, y: (-y, x)), 2 * pi), ('circ gyre v', 2 * pi, 6.28), ('circ3', 18 * pi, 56.5),
            ('sun P', 1361 * pi * 6.371e6**2, 1.735e17), ('sun avg', 1361 / 4, 340), ('sph area', 16 * pi, 50.3), ('flux sph', 4 * pi * 1, 4 * pi),
            ('labA div', (4 - 6) / 2e5 + (-3 + 1) / 2e5, -2e-5), ('labA curl', (8 + 6) / 2e5 - (-5 - 7) / 2e5, 1.3e-4),
            ('labB |g|', sqrt(gx * gx + gy * gy), .121), ('labB ang', degrees(atan(sqrt(gx * gx + gy * gy))), 6.9),
            ('lake', pi * 1000**2 * 20 / 2, 3.14e7), ('lake5', lake(5), 3.20e7), ('lake10', lake(10), 3.16e7), ('lake5 err', lake(5) / (pi * 1e7) - 1, .020), ('lake10 err', lake(10) / (pi * 1e7) - 1, .005),
            ('steps', round(2 * pi * rL / vL / 10), 592), ('euler', orbit(10, False), 908), ('euler1', orbit(1, False), 94), ('semi', orbit(10, True), .16),
            ('m angle', degrees(acos(.5)), 60), ('m plane', 2 - 1 + 3, 4), ('m T', 2 * pi * sqrt(6.771e6**3 / GM), 5544), ('m Tm', 2 * pi * sqrt(6.771e6**3 / GM) / 60, 92.4), ('m lag', 25, 25),
            ('f1', 9 * pi, 28.3), ('f2', 16 * pi / 3, 16.76), ('f3', 8, 8), ('f4', 8 * pi / 3, 8.38)]
