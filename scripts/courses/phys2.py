"""Physics II + Lab (PHYS 210 + PHYS 210L): calculus-based electricity and magnetism, with an introduction to optics.
Oct 25 2026, founder-approved four-year track, sophomore course 3. Same module fields as chem110.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, pi, sin, cos, exp, log, asin, atan, degrees, radians
ID = 'phys2'
STATUS = 'live'
YEAR = 2
PAGE = 'Physics_II.html'
CODE = 'PHYS 210 + PHYS 210L'
TITLE = 'Physics II + Lab'
LAB_NAME = 'PHYS 210L'
TAGLINE = 'Calculus-based electricity and magnetism: charge and fields, Gauss’s law, potential, circuits, magnetism, induction, AC power, Maxwell’s equations, light and optics, with six labs. Free, self-paced, and tied to clean power, the grid and space weather.'
DESC = 'Free self-study Physics II (electricity and magnetism) with lab: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and home labs, exam prep.'
ALT = 'NASA Solar Dynamics Observatory image of the Sun'
OS = 'https://openstax.org/books/university-physics-volume-2/pages/'
_O = OS
_O3 = 'https://openstax.org/books/university-physics-volume-3/pages/'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 8.02 Physics II: Electricity and Magnetism', 'https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/')
_EIA = ('U.S. EIA: How much electricity is lost in transmission and distribution?', 'https://www.eia.gov/tools/faqs/faq.php?id=105&t=3')
_GRID = ('U.S. EIA: Delivery to consumers (the power grid)', 'https://www.eia.gov/energyexplained/electricity/delivery-to-consumers.php')
_WIND = ('U.S. DOE: How do wind turbines work?', 'https://www.energy.gov/eere/wind/how-do-wind-turbines-work')
_HYDRO = ('U.S. DOE: How hydropower works', 'https://www.energy.gov/eere/water/how-hydropower-works')
_SOLAR = ('U.S. DOE: How does solar work?', 'https://www.energy.gov/eere/solar/how-does-solar-work')
_EV = ('FuelEconomy.gov (DOE/EPA): All-electric vehicles', 'https://www.fueleconomy.gov/feg/evtech.shtml')
_GEO = ('NOAA NCEI: Geomagnetism frequently asked questions', 'https://www.ngdc.noaa.gov/geomag/faqgeom.shtml')
_GS = ('NOAA Space Weather Prediction Center: Geomagnetic storms', 'https://www.swpc.noaa.gov/phenomena/geomagnetic-storms')
_CME = ('NOAA Space Weather Prediction Center: Coronal mass ejections', 'https://www.swpc.noaa.gov/phenomena/coronal-mass-ejections')
_EMS = ('NASA Science: Tour of the electromagnetic spectrum', 'https://science.nasa.gov/ems/')
_L9 = ('NASA Landsat Science: Landsat 9 instruments and spectral bands', 'https://landsat.gsfc.nasa.gov/satellites/landsat-9/landsat-9-instruments/')
BANNER = ['images/SDO_Sun.jpg', 'images/Aurora_Borealis_ISS072-E-159172.jpg', 'images/GOES19_GOESU_KSC.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg']
CREDITS = {'images/SDO_Sun.jpg': 'NASA/SDO', 'images/Aurora_Borealis_ISS072-E-159172.jpg': 'NASA (ISS072-E-159172)', 'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC',
           'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows the second semester of calculus-based college physics (electricity and magnetism, with a first look at optics). It is modeled on the topics and depth of MIT OpenCourseWare 8.02, Caltech’s Ph1b and Ph1c, Georgia Tech PHYS 2212 and the free OpenStax University Physics Volume 2, which we link throughout. None of those authors or schools endorses this page.',
         'What we add: every unit ties to real clean-energy or Earth-observation work with a cited public source (generators, solar panels, electric cars, the power grid, Earth’s magnetic field, space weather, satellite sensors), every number on the page is re-computed by a checking script before it goes live, and every lab has a free PhET version plus a safe low-voltage home version.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Almost all clean electricity is electromagnetism at work. Wind and hydro turbines spin generators that run on Faraday’s law, solar panels push charge with built-in electric fields, electric cars turn current into motion with magnetic forces, and the grid uses transformers and high voltage to move power with small losses.',
                 'Electromagnetic waves are also how we watch the planet: satellites such as Landsat 9 and GOES-19 read visible, infrared and microwave light to map crops, forests, water and storms. And Earth’s own magnetic field shields us, while space weather from the Sun can push currents into power lines. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample values.']
PREREQS = ['Physics I: forces, energy, momentum, circular motion and oscillations.', 'Calculus I and II: derivatives, integrals, and exponential growth and decay.',
           'Vectors: components, dot and cross products (taught briefly where needed).', 'Calculus III helps with Gauss’s and Ampère’s laws in integral form but is not required.']
STUDY = ['Draw the field or the circuit first. Most E&M mistakes are sign or direction mistakes.', 'Solve with symbols first, then put in numbers in SI units, and check the units of the answer.',
         'Use symmetry: before applying Gauss’s or Ampère’s law, ask which way the field must point and on what it can depend.', 'Do every practice problem on paper before opening the answer.',
         'Predict, then test it in the PhET simulation. A wrong prediction you fix sticks better than a right guess.', 'Retake the quizzes a few days later. Spaced practice beats one long session.']
LAB_GEAR = ['A computer or tablet for the free PhET simulations (they run in a browser).', 'A digital multimeter and a few AA batteries with a battery holder (low voltage only).',
            'A small set of resistors (100 Ω to 10 kΩ), a 100 µF or larger electrolytic capacitor rated above the battery voltage, jumper wires or a breadboard.',
            'A smartphone with a magnetometer app (most phones have the sensor), a small compass, a few fridge magnets.', 'A clear glass or plastic box of water, a laser pointer of class 2 or lower or a narrow flashlight beam, a protractor.',
            'Spreadsheet software for graphs and fits.']
LAB_INTRO = ['The lab is the hands-on part of the course, a 1-credit component in a typical college schedule. Here it is free and for practice only.',
             'Every lab can be done fully in a free PhET simulation, and most also have a home version that uses only batteries of 9 V or less. Never use wall power, never open a device that plugs into the wall, and never short a battery.']
SAFETY_SRC = ('OSHA: Electrical safety', 'https://www.osha.gov/electrical')
CONST_SRC = ('NIST: Fundamental physical constants', 'https://physics.nist.gov/cuu/Constants/')
CONSTANTS = [('Elementary charge, e', '1.602 × 10⁻¹⁹ C'), ('Coulomb constant, k = 1/(4πε₀)', '8.988 × 10⁹ N·m²/C²'), ('Vacuum permittivity, ε₀', '8.854 × 10⁻¹² F/m'),
             ('Vacuum permeability, μ₀', '1.257 × 10⁻⁶ T·m/A (≈ 4π × 10⁻⁷)'), ('Speed of light, c', '2.998 × 10⁸ m/s'), ('Electron mass, mₑ', '9.109 × 10⁻³¹ kg'),
             ('Proton mass, mₚ', '1.673 × 10⁻²⁷ kg'), ('Planck constant, h', '6.626 × 10⁻³⁴ J·s')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free textbooks, lectures and simulations alongside the course.'
PTABLE = [('OpenStax University Physics Volume 2', _O + '1-introduction', 'Free, complete textbook for this course.'), (_MIT[0], _MIT[1], 'Free MIT lectures, problem sets and exams.'),
          ('OpenStax University Physics Volume 3 (optics)', _O3 + '1-2-the-law-of-reflection', 'Free optics chapters for Unit 10.'),
          ('PhET: Charges and Fields', _PH + 'charges-and-fields', 'Place charges and map fields and equipotentials.'),
          ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc', 'Build and measure circuits.'),
          ('PhET: Faraday’s Electromagnetic Lab', _PH + 'faradays-electromagnetic-lab', 'Magnets, coils, generators and transformers.')]
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'Charge, Coulomb’s Law and Electric Fields', 'weeks': 'Weeks 1–2',
 'summary': 'Electric charge, conductors and insulators, Coulomb’s law, the electric field of point charges and continuous charge, field lines, and charges moving in fields.',
 'objectives': ['Use Coulomb’s law with vectors and superposition.', 'Find the electric field of point charges and simple charge distributions.', 'Sketch field lines and read them.', 'Find the force and acceleration of a charge in a field.'],
 'concepts': ['Charge comes in two signs, is conserved, and is quantized in units of e = 1.602 × 10⁻¹⁹ C.', 'Coulomb’s law: F = k|q₁q₂|/r², along the line between the charges; like charges repel.',
              'The electric field E = F/q is the force per unit charge. A point charge makes E = kq/r², pointing away from positive charge.', 'Fields add as vectors (superposition). For continuous charge, add up dE = k dq/r² with an integral.',
              'A charge in a field feels F = qE, so an electron accelerates opposite to E.'],
 'eqs': [('F=k\\frac{|q_1q_2|}{r^2},\\quad k=\\frac1{4\\pi\\varepsilon_0}', 'Coulomb’s law'), ('\\vec E=\\frac{\\vec F}{q},\\quad E=\\frac{k|q|}{r^2}', 'Electric field of a point charge'),
         ('\\vec E=\\int\\frac{k\\,dq}{r^2}\\hat r', 'Continuous charge'), ('\\vec F=q\\vec E', 'Force on a charge')],
 'worked': [
  {'q': 'Charges of +3.0 µC and −5.0 µC sit 0.20 m apart. Find the force between them.', 'steps': ['F = k|q₁q₂|/r² = 8.988 × 10⁹ × (3.0 × 10⁻⁶)(5.0 × 10⁻⁶)/0.20².', 'Opposite signs attract.'], 'a': '3.37 N, attractive.'},
  {'q': 'Find the field 0.30 m from a 2.0 nC point charge.', 'steps': ['E = kq/r² = 8.988 × 10⁹ × 2.0 × 10⁻⁹/0.09.'], 'a': '≈ 200 N/C, pointing away from the charge.'},
  {'q': 'Charges of +4.0 nC and −4.0 nC are 0.10 m apart. Find the field at the midpoint.', 'steps': ['Each charge is 0.05 m away and gives E = kq/r² = 14,380 N/C.', 'Both fields point toward the negative charge, so they add.'], 'a': '28,760 N/C (2.88 × 10⁴ N/C) toward the negative charge.'}],
 'practice': [('Find the electric force between the proton and electron in hydrogen (r = 5.29 × 10⁻¹¹ m).', 'F = ke²/r² ≈ 8.24 × 10⁻⁸ N.'),
              ('How many times stronger is the electric repulsion of two protons than their gravitational attraction?', 'ke²/(Gmₚ²) ≈ 1.23 × 10³⁶, independent of distance.'),
              ('An electron sits in a 200 N/C field. Find the force and acceleration.', 'F = eE = 3.20 × 10⁻¹⁷ N; a = F/mₑ ≈ 3.52 × 10¹³ m/s², opposite to E.'),
              ('Where is the field zero between +q and +4q a distance d apart?', 'kq/x² = 4kq/(d − x)² gives x = d/3 from +q.')],
 'misc': [('A bigger charge feels a bigger force from a smaller one.', 'Newton’s third law: the forces are equal and opposite.'), ('Field lines are paths charges follow.', 'They show force direction; a moving charge can leave a curved line.'),
          ('The field is zero wherever there is no charge.', 'Empty space can hold a strong field; only the charge density is zero there.')],
 'quiz': [{'q': 'Doubling the distance between two charges changes the force by…', 'opts': ['×2', '×½', '×¼', '×4'], 'ok': 2, 'why': 'Inverse square.'},
          {'q': 'The field of a positive point charge points…', 'opts': ['toward it', 'away from it', 'in circles', 'nowhere'], 'ok': 1, 'why': 'Direction of force on a positive test charge.'},
          {'q': 'An electron in a field pointing east accelerates…', 'opts': ['east', 'west', 'north', 'not at all'], 'ok': 1, 'why': 'F = qE with q < 0.'},
          {'q': 'The SI unit of electric field is…', 'opts': ['N/C', 'C/N', 'J', 'T'], 'ok': 0, 'why': 'Force per charge (also V/m).'}],
 'cards': [('Elementary charge', 'e = 1.602 × 10⁻¹⁹ C.'), ('Coulomb’s law', 'F = k|q₁q₂|/r².'), ('Electric field', 'E = F/q.'), ('Point-charge field', 'E = kq/r².'),
           ('Superposition', 'Fields from several charges add as vectors.'), ('Field lines', 'Start on + charge, end on − charge; denser means stronger.')],
 'planet': {'text': ['A solar cell works because sunlight frees charges that a built-in electric field then pushes apart. The U.S. Department of Energy explains that sunlight absorbed in a PV cell creates electrical charges that move in response to an internal electric field, so electricity flows. Every solar panel is a sheet of carefully engineered electric fields.'],
            'site': [('Physics I', 'Physics_I.html')],
            'src': [_SOLAR, ('OpenStax UP2, 5.3 Coulomb’s law', _O + '5-3-coulombs-law')]},
 'res': [('OpenStax UP2, 5.3 Coulomb’s law', _O + '5-3-coulombs-law', 'Free textbook section.'), ('OpenStax UP2, 5.4 Electric field', _O + '5-4-electric-field', 'Fields and superposition.'),
         ('OpenStax UP2, 5.5 Fields of charge distributions', _O + '5-5-calculating-electric-fields-of-charge-distributions', 'Integrals for E.'), ('PhET: Coulomb’s Law', _PH + 'coulombs-law', 'Interactive.')]})
UNITS.append(
{'id': 'u2', 'title': 'Gauss’s Law', 'weeks': 'Week 3',
 'summary': 'Electric flux, Gauss’s law, and using symmetry to find fields of spheres, lines and sheets; conductors in electrostatic equilibrium.',
 'objectives': ['Compute electric flux through a surface.', 'State Gauss’s law and choose a Gaussian surface that matches the symmetry.', 'Find fields of spherical, cylindrical and planar charge.', 'Explain why the field inside a conductor is zero and charge sits on its surface.'],
 'concepts': ['Flux Φ = ∮E·dA counts field lines through a surface.', 'Gauss’s law: the net flux out of any closed surface equals the enclosed charge divided by ε₀.',
              'Gauss’s law is always true but only useful when symmetry makes E constant on the surface: spheres, long lines, large sheets.', 'Outside a uniform sphere of charge, the field is the same as a point charge at the center.',
              'In a conductor in equilibrium E = 0 inside, excess charge sits on the surface, and E just outside is perpendicular to the surface.'],
 'eqs': [('\\Phi_E=\\oint\\vec E\\cdot d\\vec A=\\frac{Q_{\\text{enc}}}{\\varepsilon_0}', 'Gauss’s law'), ('E=\\frac{\\lambda}{2\\pi\\varepsilon_0 r}', 'Long line of charge'),
         ('E=\\frac{\\sigma}{2\\varepsilon_0}', 'Large sheet of charge'), ('E=\\frac{\\sigma}{\\varepsilon_0}', 'Just outside a conductor')],
 'worked': [
  {'q': 'A closed surface surrounds a 1.0 nC charge. Find the net flux.', 'steps': ['Φ = Q/ε₀ = 1.0 × 10⁻⁹/8.854 × 10⁻¹²; the shape does not matter.'], 'a': '≈ 113 N·m²/C.'},
  {'q': 'A long wire carries 2.0 nC per meter. Find E at 0.10 m.', 'steps': ['Use a cylinder: E(2πrL) = λL/ε₀, so E = λ/(2πε₀r) = 2kλ/r.', 'E = 2 × 8.988 × 10⁹ × 2.0 × 10⁻⁹/0.10.'], 'a': '≈ 360 N/C, pointing radially outward.'},
  {'q': 'A large sheet holds σ = 5.0 µC/m². Find E near it.', 'steps': ['A pillbox through the sheet: 2EA = σA/ε₀.'], 'a': 'E = σ/(2ε₀) ≈ 2.82 × 10⁵ N/C, the same at every distance near the sheet.'}],
 'practice': [('A 1.0 µC charge sits on a 0.10 m metal sphere. Find E at 0.50 m from the center and at 0.05 m.', 'Outside: kQ/r² = 3.60 × 10⁴ N/C. Inside the conductor: 0.'),
              ('Why does a car protect you from lightning?', 'Charge stays on the outer metal surface, so the field inside is small (a Faraday cage).'),
              ('A cube surrounds a dipole. What is the net flux?', 'Zero: the enclosed charge is zero.'), ('How does E from a line of charge fall with distance?', 'As 1/r, slower than a point charge’s 1/r².')],
 'misc': [('Zero flux means zero field everywhere on the surface.', 'Only the total is zero; field can go in on one side and out on another.'), ('Gauss’s law only works for symmetric charges.', 'It always holds; symmetry is what makes it easy to use.'),
          ('Charges outside the surface change the flux.', 'They change E on the surface but add zero net flux.')],
 'quiz': [{'q': 'Net flux through a closed surface depends on…', 'opts': ['its shape', 'the enclosed charge', 'its area', 'outside charges'], 'ok': 1, 'why': 'Q_enc/ε₀.'},
          {'q': 'Inside a conductor in equilibrium, E is…', 'opts': ['maximum', 'zero', 'kQ/r²', 'σ/ε₀'], 'ok': 1, 'why': 'Free charges rearrange until E = 0.'},
          {'q': 'E near a large charged sheet varies with distance as…', 'opts': ['1/r²', '1/r', 'constant', 'r'], 'ok': 2, 'why': 'σ/(2ε₀).'},
          {'q': 'The best Gaussian surface for a long wire is a…', 'opts': ['sphere', 'cube', 'coaxial cylinder', 'flat disk'], 'ok': 2, 'why': 'Matches the symmetry.'}],
 'cards': [('Electric flux', 'Φ = ∮E·dA.'), ('Gauss’s law', 'Φ = Q_enc/ε₀.'), ('Line of charge', 'E = λ/(2πε₀r).'), ('Sheet of charge', 'E = σ/(2ε₀).'),
           ('Conductor', 'E = 0 inside; charge on the surface.'), ('Faraday cage', 'A closed conductor shields its inside.')],
 'planet': {'text': ['Gauss’s law has a magnetic twin: the net magnetic flux through any closed surface is zero, because there are no magnetic monopoles. Earth’s field is a good example. NOAA’s National Centers for Environmental Information say more than 90% of the field measured at the surface is generated in Earth’s outer core. Every field line that leaves the planet comes back to it.'],
            'site': [('Space Weather', 'Space_Weather.html')],
            'src': [_GEO, ('OpenStax UP2, 6.3 Applying Gauss’s law', _O + '6-3-applying-gausss-law')]},
 'res': [('OpenStax UP2, 6.2 Explaining Gauss’s law', _O + '6-2-explaining-gausss-law', 'Flux and the law.'), ('OpenStax UP2, 6.3 Applying Gauss’s law', _O + '6-3-applying-gausss-law', 'Spheres, lines, sheets.'),
         ('OpenStax UP2, 6.4 Conductors in equilibrium', _O + '6-4-conductors-in-electrostatic-equilibrium', 'Conductors.'), _MIT + ('Lectures and problem sets.',)]})
UNITS.append(
{'id': 'u3', 'title': 'Electric Potential and Capacitance', 'weeks': 'Weeks 4–5',
 'summary': 'Potential energy and potential, equipotentials, finding E from V, capacitors in series and parallel, stored energy, and dielectrics.',
 'objectives': ['Compute potential and potential energy of point charges.', 'Relate E and V: E = −dV/dx.', 'Find capacitance and combine capacitors.', 'Compute stored energy and the effect of a dielectric.'],
 'concepts': ['Potential V is potential energy per charge (volts = joules per coulomb). Only differences matter.', 'A point charge gives V = kq/r; potentials add as numbers, not vectors.',
              'The field points downhill in potential: E = −dV/dx. Equipotentials are perpendicular to field lines.', 'A capacitor stores charge Q = CV. A parallel-plate capacitor has C = ε₀A/d.',
              'Stored energy U = ½CV². A dielectric with constant κ multiplies C by κ.', 'Parallel capacitors add; in series, reciprocals add.'],
 'eqs': [('V=\\frac{kq}{r},\\quad \\Delta U=q\\,\\Delta V', 'Potential of a point charge'), ('E_x=-\\frac{dV}{dx}', 'Field from potential'),
         ('C=\\frac{Q}{V}=\\frac{\\kappa\\varepsilon_0A}{d}', 'Parallel-plate capacitor'), ('U=\\tfrac12CV^2', 'Stored energy'), ('C_{\\parallel}=C_1+C_2,\\quad \\frac1{C_s}=\\frac1{C_1}+\\frac1{C_2}', 'Combinations')],
 'worked': [
  {'q': 'Find the potential 0.30 m from a 2.0 nC charge.', 'steps': ['V = kq/r = 8.988 × 10⁹ × 2.0 × 10⁻⁹/0.30.'], 'a': '≈ 59.9 V.'},
  {'q': 'An electron starts from rest and moves through a 100 V potential difference. Find its speed.', 'steps': ['eΔV = ½mv².', 'v = √(2 × 1.602 × 10⁻¹⁹ × 100/9.109 × 10⁻³¹).'], 'a': '≈ 5.93 × 10⁶ m/s.'},
  {'q': 'Plates of 0.010 m² sit 1.0 mm apart and connect to 12 V. Find C, Q and U.', 'steps': ['C = ε₀A/d = 8.854 × 10⁻¹² × 0.010/0.001 = 88.5 pF.', 'Q = CV = 1.06 nC.', 'U = ½CV² = 6.37 nJ.'], 'a': '88.5 pF, 1.06 nC, 6.37 nJ.'}],
 'practice': [('Combine 2 µF and 3 µF in series and in parallel.', 'Series 1.2 µF; parallel 5 µF.'), ('Fill the 88.5 pF capacitor with a dielectric of κ = 3.4.', 'C = 301 pF.'),
              ('A large supercapacitor of 3,000 F is charged to 2.7 V (sample values). How much energy does it hold?', 'U = ½CV² ≈ 10.9 kJ, a tiny fraction of an EV battery but delivered in seconds.'),
              ('V = 4x² volts. Find E at x = 2 m.', 'E = −dV/dx = −16 V/m (pointing toward −x).')],
 'misc': [('Potential and potential energy are the same thing.', 'U = qV; V is per unit charge.'), ('High voltage alone is what makes a shock dangerous.', 'Current through the body matters; voltage drives it through the body’s resistance.'),
          ('Where V = 0, E = 0.', 'Midway between +q and −q, V = 0 but E is large.')],
 'quiz': [{'q': '1 volt equals…', 'opts': ['1 J/C', '1 C/J', '1 N/C', '1 W/A²'], 'ok': 0, 'why': 'Energy per charge.'},
          {'q': 'Halving the plate gap of a capacitor makes C…', 'opts': ['half', 'double', 'four times', 'unchanged'], 'ok': 1, 'why': 'C = ε₀A/d.'},
          {'q': 'Doubling the voltage on a capacitor multiplies stored energy by…', 'opts': ['2', '4', '½', '1'], 'ok': 1, 'why': 'U ∝ V².'},
          {'q': 'Equipotential lines meet field lines at…', 'opts': ['0°', '45°', '90°', 'any angle'], 'ok': 2, 'why': 'No work along an equipotential.'}],
 'cards': [('Electric potential', 'V = U/q, in volts.'), ('Point-charge potential', 'V = kq/r.'), ('Field from potential', 'E = −dV/dx.'), ('Capacitance', 'C = Q/V; farads.'),
           ('Parallel plates', 'C = κε₀A/d.'), ('Capacitor energy', 'U = ½CV².'), ('Electron volt', '1 eV = 1.602 × 10⁻¹⁹ J.')],
 'planet': {'text': ['Electric cars store energy in batteries, not capacitors, because a capacitor holds far less energy per kilogram. The supercapacitor in the practice set holds about 10.9 kJ, about 3.04 watt-hours. Capacitors earn their place where power must flow in or out in seconds, such as smoothing the output of power electronics in EVs, solar inverters and wind turbines.'],
            'site': [('Physics I', 'Physics_I.html')],
            'src': [_EV, ('OpenStax UP2, 8.3 Energy stored in a capacitor', _O + '8-3-energy-stored-in-a-capacitor')]},
 'res': [('OpenStax UP2, 7.2 Electric potential and potential difference', _O + '7-2-electric-potential-and-potential-difference', 'Potential.'), ('OpenStax UP2, 7.3 Calculations of electric potential', _O + '7-3-calculations-of-electric-potential', 'Potential of charge distributions.'),
         ('OpenStax UP2, 8.1 Capacitors and capacitance', _O + '8-1-capacitors-and-capacitance', 'Capacitors.'), ('OpenStax UP2, 8.4 Capacitor with a dielectric', _O + '8-4-capacitor-with-a-dielectric', 'Dielectrics.'),
         ('PhET: Capacitor Lab: Basics', _PH + 'capacitor-lab-basics', 'Interactive.')]})
UNITS.append(
{'id': 'u4', 'title': 'Current, Resistance and DC Circuits', 'weeks': 'Weeks 6–7',
 'summary': 'Current and drift speed, resistivity and Ohm’s law, power, EMF and internal resistance, series and parallel resistors, Kirchhoff’s rules, and RC circuits.',
 'objectives': ['Relate current to drift speed and resistance to resistivity.', 'Use Ohm’s law and P = IV.', 'Reduce series-parallel networks and apply Kirchhoff’s rules.', 'Analyze charging and discharging RC circuits.'],
 'concepts': ['Current I = dQ/dt; in a wire I = nqv_dA, and the drift speed is tiny even though signals travel near light speed.', 'Resistance R = ρL/A. Ohm’s law V = IR holds for ohmic materials.',
              'Power P = IV = I²R = V²/R.', 'Series resistors add; in parallel, reciprocals add.', 'Kirchhoff: currents into a junction sum to zero; voltage changes around any loop sum to zero.',
              'An RC circuit charges as V = V₀(1 − e^(−t/RC)); the time constant is τ = RC.'],
 'eqs': [('I=\\frac{dQ}{dt}=nqv_dA', 'Current and drift speed'), ('R=\\rho\\frac{L}{A},\\quad V=IR', 'Resistance and Ohm’s law'), ('P=IV=I^2R', 'Electrical power'),
         ('\\sum I=0,\\quad \\sum\\Delta V=0', 'Kirchhoff’s rules'), ('V_C=V_0\\left(1-e^{-t/RC}\\right)', 'Charging capacitor')],
 'worked': [
  {'q': 'Find the resistance of 100 m of copper wire 1.0 mm in diameter (ρ = 1.68 × 10⁻⁸ Ω·m).', 'steps': ['A = π(0.5 × 10⁻³)² = 7.85 × 10⁻⁷ m².', 'R = ρL/A = 1.68 × 10⁻⁸ × 100/7.85 × 10⁻⁷.'], 'a': '≈ 2.14 Ω.'},
  {'q': 'Two batteries (12 V and 6 V) and three resistors: loop 1 has 12 V, R₁ = 2 Ω and the shared R₃ = 6 Ω; loop 2 has 6 V, R₂ = 3 Ω and R₃. Find the currents.', 'steps': ['Junction: I₃ = I₁ + I₂.', 'Loop 1: 12 = 2I₁ + 6I₃. Loop 2: 6 = 3I₂ + 6I₃.', 'Solve: I₁ = 2 A, I₂ = −0.667 A, I₃ = 1.33 A.'], 'a': 'I₁ = 2 A; I₂ = −0.667 A (the minus sign means the 12 V battery is pushing current backward through the 6 V one, charging it); I₃ = 1.33 A.'},
  {'q': 'A 100 µF capacitor charges from a 9 V battery through 10 kΩ. Find τ and the voltage after 1 s and 3 s.', 'steps': ['τ = RC = 10⁴ × 10⁻⁴ = 1.0 s.', 'V(1) = 9(1 − e^(−1)); V(3) = 9(1 − e^(−3)).'], 'a': '1.0 s; 5.69 V; 8.55 V.'}],
 'practice': [('A 60 W bulb runs on 120 V. Find its current and resistance.', 'I = 0.5 A; R = 240 Ω.'), ('Find the equivalent of 6 Ω and 3 Ω in parallel, then the current from 12 V through that pair in series with 4 Ω.', '2 Ω; I = 12/6 = 2 A.'),
              ('Find the drift speed for 1 A in the 1.0 mm copper wire (n = 8.5 × 10²⁸ m⁻³).', 'v_d = I/(neA) ≈ 9.4 × 10⁻⁵ m/s, about a third of a meter per hour.'),
              ('A solar panel has 60 cells in series, each giving 0.6 V (sample values). What is the panel voltage? How do you double the current instead?', '36 V; put two panels in parallel.')],
 'misc': [('Current is used up in a resistor.', 'Charge is conserved; energy is converted, not current.'), ('Electrons race through wires at near light speed.', 'The signal does; the electrons drift at fractions of a millimeter per second.'),
          ('A battery supplies constant current.', 'It supplies roughly constant EMF; the current depends on the circuit.')],
 'quiz': [{'q': 'Doubling a wire’s length doubles its…', 'opts': ['resistivity', 'resistance', 'current', 'area'], 'ok': 1, 'why': 'R = ρL/A.'},
          {'q': 'Two equal resistors R in parallel give…', 'opts': ['2R', 'R', 'R/2', 'R²'], 'ok': 2, 'why': '1/R + 1/R.'},
          {'q': 'After one time constant a charging capacitor is at…', 'opts': ['37%', '50%', '63%', '100%'], 'ok': 2, 'why': '1 − e^(−1).'},
          {'q': 'Kirchhoff’s loop rule comes from conservation of…', 'opts': ['charge', 'energy', 'momentum', 'mass'], 'ok': 1, 'why': 'Potential is energy per charge.'}],
 'cards': [('Current', 'I = dQ/dt; amperes.'), ('Ohm’s law', 'V = IR.'), ('Resistivity', 'R = ρL/A.'), ('Power', 'P = IV = I²R = V²/R.'), ('Junction rule', 'ΣI = 0.'), ('Loop rule', 'ΣΔV = 0.'), ('RC time constant', 'τ = RC.')],
 'planet': {'text': ['A solar panel is a DC circuit. Cells are wired in series to raise the voltage and panels in parallel to raise the current, exactly as in the practice set. A cell pushes charge one way only, so a panel’s output is direct current; it must be converted to alternating current before it can join the grid (Unit 9). The U.S. Department of Energy explains how the cells themselves work.'],
            'site': [('Earth Observation', 'Earth_Observation.html')],
            'src': [_SOLAR, ('OpenStax UP2, 10.3 Kirchhoff’s rules', _O + '10-3-kirchhoffs-rules')]},
 'res': [('OpenStax UP2, 9.1 Electrical current', _O + '9-1-electrical-current', 'Current.'), ('OpenStax UP2, 9.3 Resistivity and resistance', _O + '9-3-resistivity-and-resistance', 'Resistance.'),
         ('OpenStax UP2, 10.2 Resistors in series and parallel', _O + '10-2-resistors-in-series-and-parallel', 'Combinations.'), ('OpenStax UP2, 10.5 RC circuits', _O + '10-5-rc-circuits', 'RC circuits.'),
         ('PhET: Ohm’s Law', _PH + 'ohms-law', 'Interactive.')]})
UNITS.append(
{'id': 'u5', 'title': 'Magnetic Fields and Forces', 'weeks': 'Week 8',
 'summary': 'The magnetic force on moving charges and currents, circular motion of charged particles, torque on a current loop, and how electric motors work.',
 'objectives': ['Use F = qv × B with the right-hand rule.', 'Find the radius and frequency of a charged particle’s circular orbit.', 'Find the force on a current-carrying wire and the torque on a loop.', 'Explain how a DC motor turns current into rotation.'],
 'concepts': ['A magnetic field pushes on moving charge: F = qv × B, perpendicular to both v and B. It does no work, so it changes direction, not speed.',
              'A charge moving across a uniform field circles with radius r = mv/(|q|B) and cyclotron frequency f = |q|B/(2πm), independent of speed.',
              'A wire carrying current I in field B feels F = IL × B.', 'A current loop has magnetic moment μ = NIA and feels torque τ = μB sin θ. That torque is what spins an electric motor.',
              'Crossed E and B fields pass only particles with v = E/B (a velocity selector).'],
 'eqs': [('\\vec F=q\\vec v\\times\\vec B', 'Magnetic force on a charge'), ('r=\\frac{mv}{|q|B},\\quad f=\\frac{|q|B}{2\\pi m}', 'Circular motion in a field'),
         ('\\vec F=I\\vec L\\times\\vec B', 'Force on a current'), ('\\tau=NIAB\\sin\\theta', 'Torque on a loop')],
 'worked': [
  {'q': 'A solar-wind proton moves at 400 km/s perpendicular to a 50 µT field (sample values). Find the radius of its circle.', 'steps': ['r = mv/(eB) = 1.673 × 10⁻²⁷ × 4 × 10⁵/(1.602 × 10⁻¹⁹ × 5 × 10⁻⁵).'], 'a': '≈ 83.5 m. Charged particles spiral tightly along field lines instead of crossing them.'},
  {'q': 'A 0.20 m wire carrying 200 A sits perpendicular to a 0.50 T field. Find the force.', 'steps': ['F = ILB = 200 × 0.20 × 0.50.'], 'a': '20 N.'},
  {'q': 'A motor coil has 100 turns of area 0.01 m² carrying 2 A in a 0.5 T field. Find the maximum torque.', 'steps': ['τ = NIAB = 100 × 2 × 0.01 × 0.5.'], 'a': '1.0 N·m, when the coil’s plane is parallel to the field.'}],
 'practice': [('Find the cyclotron frequency of a proton in a 1 T field.', 'f = eB/(2πmₚ) ≈ 15.2 MHz.'), ('An electron moves at 1 × 10⁵ m/s across a 50 µT field. Find r.', 'r = mₑv/(eB) ≈ 1.14 cm.'),
              ('What speed passes undeflected through E = 10⁴ V/m and B = 0.1 T?', 'v = E/B = 10⁵ m/s.'), ('Can a static magnetic field speed up a charge?', 'No: F ⊥ v, so it does no work.')],
 'misc': [('Magnetic force points along the field.', 'It is perpendicular to B and to v.'), ('A charge at rest feels a magnetic force.', 'Only moving charges do.'), ('Bigger speed means a higher cyclotron frequency.', 'The radius grows with speed, but the frequency does not.')],
 'quiz': [{'q': 'The magnetic force on a charge moving parallel to B is…', 'opts': ['maximum', 'zero', 'qvB', 'qE'], 'ok': 1, 'why': 'sin 0 = 0.'},
          {'q': 'The SI unit of magnetic field is the…', 'opts': ['gauss', 'tesla', 'weber', 'henry'], 'ok': 1, 'why': '1 T = 1 N/(A·m); 1 G = 10⁻⁴ T.'},
          {'q': 'Doubling a charged particle’s speed in a uniform B changes its radius by…', 'opts': ['×½', '×1', '×2', '×4'], 'ok': 2, 'why': 'r = mv/(qB).'},
          {'q': 'The torque on a motor coil is largest when its plane is…', 'opts': ['perpendicular to B', 'parallel to B', 'at 30°', 'any angle'], 'ok': 1, 'why': 'μ is then perpendicular to B.'}],
 'cards': [('Lorentz force', 'F = q(E + v × B).'), ('Right-hand rule', 'Fingers v, curl to B, thumb F for positive q.'), ('Cyclotron radius', 'r = mv/(qB).'), ('Force on a wire', 'F = ILB sin θ.'),
           ('Magnetic moment', 'μ = NIA.'), ('Motor torque', 'τ = NIAB sin θ.')],
 'planet': {'text': ['Electric cars run on magnetic torque: current in the motor’s coils sits in a magnetic field, and τ = NIAB sin θ turns the wheels. FuelEconomy.gov says EVs convert over 77% of the electrical energy from the grid to power at the wheels, while gasoline cars convert only about 12% to 30% of the energy in their fuel.',
                     'Earth’s field, between about 25 and 65 µT at the surface according to NOAA, bends incoming charged particles of the solar wind into tight spirals, as in the first worked example. Particles trapped this way are guided along field lines toward the poles, where they light up the aurora.'],
            'site': [('Space Weather', 'Space_Weather.html')],
            'src': [_EV, _GEO]},
 'res': [('OpenStax UP2, 11.3 Motion of a charged particle in a magnetic field', _O + '11-3-motion-of-a-charged-particle-in-a-magnetic-field', 'Circular motion.'),
         ('OpenStax UP2, 11.4 Magnetic force on a current-carrying conductor', _O + '11-4-magnetic-force-on-a-current-carrying-conductor', 'Force on wires.'),
         ('OpenStax UP2, 11.5 Force and torque on a current loop', _O + '11-5-force-and-torque-on-a-current-loop', 'Motors.'), ('PhET: Magnets and Electromagnets', _PH + 'magnets-and-electromagnets', 'Interactive.')]})
UNITS.append(
{'id': 'u6', 'title': 'Sources of Magnetic Fields: Biot–Savart and Ampère', 'weeks': 'Week 9',
 'summary': 'How currents make magnetic fields: the Biot–Savart law, fields of wires, loops and solenoids, forces between parallel currents, and Ampère’s law.',
 'objectives': ['Use the Biot–Savart law for a wire and a loop.', 'Apply Ampère’s law to wires and solenoids.', 'Find the force between parallel currents.', 'Compare man-made fields with Earth’s field.'],
 'concepts': ['Biot–Savart: each bit of current I dl makes dB = (μ₀/4π) I dl × r̂/r². Field lines circle the current (right-hand rule: thumb along I, fingers curl with B).',
              'A long straight wire: B = μ₀I/(2πr). At the center of a loop of radius R: B = μ₀I/(2R).', 'Ampère’s law: ∮B·dl = μ₀I_enc. Like Gauss’s law, it is easiest with symmetry.',
              'Inside a long solenoid B = μ₀nI, uniform, where n is turns per meter.', 'Parallel currents attract; opposite currents repel, with force per length μ₀I₁I₂/(2πd).'],
 'eqs': [('d\\vec B=\\frac{\\mu_0}{4\\pi}\\frac{I\\,d\\vec l\\times\\hat r}{r^2}', 'Biot–Savart law'), ('B=\\frac{\\mu_0I}{2\\pi r}', 'Long straight wire'),
         ('\\oint\\vec B\\cdot d\\vec l=\\mu_0I_{\\text{enc}}', 'Ampère’s law'), ('B=\\mu_0nI', 'Long solenoid'), ('\\frac FL=\\frac{\\mu_0I_1I_2}{2\\pi d}', 'Parallel wires')],
 'worked': [
  {'q': 'A transmission line carries 1,000 A (sample value). Find B at 20 m and compare it with Earth’s field.', 'steps': ['B = μ₀I/(2πr) = 4π × 10⁻⁷ × 1,000/(2π × 20).'], 'a': '10 µT, smaller than Earth’s 25–65 µT surface field.'},
  {'q': 'A solenoid has 1,000 turns per meter and carries 2 A. Find B inside.', 'steps': ['B = μ₀nI = 4π × 10⁻⁷ × 1,000 × 2.'], 'a': '≈ 2.51 mT, about 50 times Earth’s field.'},
  {'q': 'Two parallel wires 1 cm apart each carry 10 A in the same direction. Find the force per meter.', 'steps': ['F/L = μ₀I₁I₂/(2πd) = 4π × 10⁻⁷ × 100/(2π × 0.01).'], 'a': '2.0 mN/m, attractive.'}],
 'practice': [('Find B at the center of a 5 cm radius loop carrying 5 A.', 'B = μ₀I/(2R) ≈ 62.8 µT.'), ('A wire carries 2 A. Find B at 1, 2 and 4 cm.', '40, 20 and 10 µT: halving with each doubling of distance.'),
              ('Use Ampère’s law to find B inside a thick wire of radius a at r < a (uniform current).', 'B(2πr) = μ₀I r²/a², so B = μ₀Ir/(2πa²), growing linearly from the center.'), ('What is B outside an ideal toroid?', 'Zero: the loop encloses no net current.')],
 'misc': [('Magnetic field lines start and end on poles.', 'They form closed loops; there are no monopoles.'), ('Ampère’s law gives B for any current.', 'It always holds, but it gives B directly only with symmetry.'),
          ('The field of a wire points along the wire.', 'It circles the wire.')],
 'quiz': [{'q': 'B from a long wire falls with distance as…', 'opts': ['1/r²', '1/r', 'constant', 'r'], 'ok': 1, 'why': 'μ₀I/(2πr).'},
          {'q': 'Inside a long solenoid, B depends on…', 'opts': ['radius', 'turns per meter and current', 'length only', 'distance from the axis'], 'ok': 1, 'why': 'B = μ₀nI.'},
          {'q': 'Two wires with currents in opposite directions…', 'opts': ['attract', 'repel', 'feel no force', 'twist'], 'ok': 1, 'why': 'Opposite currents repel.'},
          {'q': 'μ₀ is about…', 'opts': ['8.85 × 10⁻¹²', '1.26 × 10⁻⁶', '9 × 10⁹', '3 × 10⁸'], 'ok': 1, 'why': '4π × 10⁻⁷ T·m/A.'}],
 'cards': [('Biot–Savart', 'dB = (μ₀/4π) I dl × r̂/r².'), ('Wire field', 'B = μ₀I/(2πr).'), ('Loop center', 'B = μ₀I/(2R).'), ('Ampère’s law', '∮B·dl = μ₀I_enc.'), ('Solenoid', 'B = μ₀nI.'), ('Parallel currents', 'Same direction attract.')],
 'planet': {'text': ['Earth’s own field is made by currents: NOAA explains that more than 90% of it is generated in the outer core by what NOAA calls Earth’s internal dynamo: moving, electrically conducting material that carries current. The Biot–Savart law is the bridge between those currents and the field a compass reads. NOAA’s World Magnetic Model describes this main field.'],
            'site': [('Space Weather', 'Space_Weather.html')],
            'src': [_GEO, ('OpenStax UP2, 12.1 The Biot–Savart law', _O + '12-1-the-biot-savart-law')]},
 'res': [('OpenStax UP2, 12.1 The Biot–Savart law', _O + '12-1-the-biot-savart-law', 'Biot–Savart.'), ('OpenStax UP2, 12.5 Ampère’s law', _O + '12-5-amperes-law', 'Ampère’s law.'),
         ('PhET: Magnet and Compass', _PH + 'magnet-and-compass', 'Interactive.'), _MIT + ('Lectures and problem sets.',)]})
UNITS.append(
{'id': 'u7', 'title': 'Electromagnetic Induction: Faraday and Lenz', 'weeks': 'Week 10',
 'summary': 'Magnetic flux, Faraday’s law, Lenz’s law, motional EMF, induced electric fields, eddy currents, and the generators behind wind and hydro power.',
 'objectives': ['Compute magnetic flux and the EMF from a changing flux.', 'Use Lenz’s law to find the direction of induced current.', 'Find motional EMF for a moving rod.', 'Compute the output of an AC generator and the power of a hydro plant.'],
 'concepts': ['Magnetic flux Φ_B = ∫B·dA, in webers.', 'Faraday’s law: a changing flux through a coil of N turns induces EMF ε = −N dΦ_B/dt.',
              'Lenz’s law (the minus sign): the induced current opposes the change in flux that caused it, which is energy conservation.', 'A rod of length L moving at v across B has motional EMF ε = BLv.',
              'A coil spinning at angular speed ω in B gives ε = NBAω sin ωt: alternating current. Turning it takes mechanical work, which is how generators convert motion into electrical energy.'],
 'eqs': [('\\Phi_B=\\int\\vec B\\cdot d\\vec A', 'Magnetic flux'), ('\\varepsilon=-N\\frac{d\\Phi_B}{dt}', 'Faraday’s law'), ('\\varepsilon=BLv', 'Motional EMF'),
         ('\\varepsilon(t)=NBA\\omega\\sin\\omega t', 'AC generator'), ('P=\\eta\\rho gQh', 'Hydropower')],
 'worked': [
  {'q': 'A generator coil has 100 turns of area 0.04 m² spinning at 60 rev/s in a 0.5 T field. Find the peak EMF.', 'steps': ['ω = 2π × 60 = 377 rad/s.', 'ε_max = NBAω = 100 × 0.5 × 0.04 × 377.'], 'a': '≈ 754 V.'},
  {'q': 'A 200-turn coil of area 0.01 m² sees B rise from 0 to 0.3 T in 0.5 s. Find the average EMF.', 'steps': ['ΔΦ = BA = 0.003 Wb per turn.', 'ε = NΔΦ/Δt = 200 × 0.003/0.5.'], 'a': '1.2 V.'},
  {'q': 'A hydro plant passes 100 m³/s through a 50 m head at 90% efficiency (sample values). Find its power.', 'steps': ['P = ηρgQh = 0.9 × 1,000 × 9.81 × 100 × 50.'], 'a': '≈ 44.1 MW.'}],
 'practice': [('A 0.2 m rod moves at 3 m/s across a 0.5 T field. Find the EMF.', 'BLv = 0.3 V.'), ('A magnet’s north pole approaches a loop. Which way does the induced current flow, seen from the magnet?', 'Counterclockwise, making a north face that repels the approaching magnet.'),
              ('Why is it harder to turn a generator when lamps are switched on?', 'The current in the coil feels a magnetic torque opposing the motion (Lenz); that is where the electrical energy comes from.'),
              ('Doubling a generator’s spin rate changes its peak EMF by…?', '×2: ε_max = NBAω.')],
 'misc': [('A strong but steady field induces current.', 'Only a changing flux induces EMF.'), ('Lenz’s law opposes the field.', 'It opposes the change in flux.'), ('Generators make energy.', 'They convert mechanical work into electrical energy.')],
 'quiz': [{'q': 'Faraday’s law relates EMF to…', 'opts': ['flux', 'rate of change of flux', 'current', 'resistance'], 'ok': 1, 'why': 'ε = −N dΦ/dt.'},
          {'q': 'The minus sign in Faraday’s law is…', 'opts': ['Ohm’s law', 'Lenz’s law', 'Gauss’s law', 'a convention only'], 'ok': 1, 'why': 'Opposes the change.'},
          {'q': 'A coil spinning in a steady field produces…', 'opts': ['DC', 'AC', 'no EMF', 'static charge'], 'ok': 1, 'why': 'ε ∝ sin ωt.'},
          {'q': 'The SI unit of magnetic flux is the…', 'opts': ['tesla', 'weber', 'henry', 'farad'], 'ok': 1, 'why': '1 Wb = 1 T·m².'}],
 'cards': [('Magnetic flux', 'Φ = BA cos θ; webers.'), ('Faraday’s law', 'ε = −N dΦ/dt.'), ('Lenz’s law', 'Induced current opposes the change.'), ('Motional EMF', 'ε = BLv.'),
           ('Generator', 'ε = NBAω sin ωt.'), ('Eddy currents', 'Induced loops in bulk metal; used in braking.')],
 'planet': {'text': ['Wind and hydro power are Faraday’s law. The U.S. Department of Energy explains that wind turns a turbine’s blades around a rotor, which spins a generator that creates electricity, and that hydropower plants use turbines and generators to convert the kinetic energy of flowing water into electricity for the grid.'],
            'site': [('Physics I', 'Physics_I.html')],
            'src': [_WIND, _HYDRO]},
 'res': [('OpenStax UP2, 13.1 Faraday’s law', _O + '13-1-faradays-law', 'Faraday.'), ('OpenStax UP2, 13.2 Lenz’s law', _O + '13-2-lenzs-law', 'Lenz.'),
         ('OpenStax UP2, 13.3 Motional EMF', _O + '13-3-motional-emf', 'Moving conductors.'), ('OpenStax UP2, 13.6 Electric generators and back EMF', _O + '13-6-electric-generators-and-back-emf', 'Generators.'),
         ('PhET: Faraday’s Law', _PH + 'faradays-law', 'Interactive.')]})
UNITS.append(
{'id': 'u8', 'title': 'Inductance, RL and LC Circuits', 'weeks': 'Week 11',
 'summary': 'Mutual and self-inductance, energy stored in magnetic fields, RL circuits and their time constant, and LC oscillations.',
 'objectives': ['Find the self-inductance of a solenoid and the EMF of an inductor.', 'Analyze current growth and decay in RL circuits.', 'Compute energy in an inductor and magnetic energy density.', 'Find the frequency of an LC oscillator.'],
 'concepts': ['A changing current in one coil induces EMF in another: ε₂ = −M dI₁/dt (mutual inductance).', 'A coil opposes changes in its own current: ε = −L dI/dt. A long solenoid has L = μ₀N²A/l.',
              'In an RL circuit the current rises as I = (ε/R)(1 − e^(−t/τ)) with τ = L/R.', 'An inductor stores U = ½LI²; any magnetic field stores energy density u = B²/(2μ₀).',
              'An LC circuit swaps energy between capacitor and inductor at ω = 1/√(LC), the electrical twin of a mass on a spring.'],
 'eqs': [('\\varepsilon=-L\\frac{dI}{dt},\\quad L=\\frac{\\mu_0N^2A}{l}', 'Self-inductance'), ('I=\\frac{\\varepsilon}{R}\\left(1-e^{-t/\\tau}\\right),\\ \\tau=\\frac LR', 'RL circuit'),
         ('U=\\tfrac12LI^2,\\quad u_B=\\frac{B^2}{2\\mu_0}', 'Magnetic energy'), ('\\omega=\\frac1{\\sqrt{LC}}', 'LC oscillation')],
 'worked': [
  {'q': 'A solenoid has 500 turns, cross-section 1.0 × 10⁻³ m² and length 0.25 m. Find L, then τ with a 10 Ω resistor.', 'steps': ['L = μ₀N²A/l = 4π × 10⁻⁷ × 250,000 × 10⁻³/0.25 = 1.26 mH.', 'τ = L/R = 0.126 ms.'], 'a': '1.26 mH; 0.126 ms.'},
  {'q': 'How much energy does that inductor store at 2 A?', 'steps': ['U = ½LI² = ½ × 1.257 × 10⁻³ × 4.'], 'a': '≈ 2.51 mJ.'},
  {'q': 'Find the oscillation frequency of a 10 mH inductor with a 1 µF capacitor.', 'steps': ['f = 1/(2π√(LC)) = 1/(2π√(10⁻⁸)).'], 'a': '≈ 1.59 kHz.'}],
 'practice': [('Two coils have M = 0.01 H. The current in one changes at 100 A/s. Find the EMF in the other.', '1 V.'), ('What fraction of its final current does an RL circuit reach after 1τ and 3τ?', '63% and 95%.'),
              ('Find the magnetic energy density of Earth’s 50 µT field.', 'B²/(2μ₀) ≈ 9.9 × 10⁻⁴ J/m³.'), ('Why can switching off an inductive load make a spark?', 'Stopping I quickly makes L dI/dt huge.')],
 'misc': [('An inductor resists current.', 'It resists changes in current; with steady DC it is just a wire.'), ('Inductors store energy in charge.', 'In the magnetic field.'), ('LC oscillations last forever.', 'Real resistance damps them (an RLC circuit, Unit 9).')],
 'quiz': [{'q': 'The SI unit of inductance is the…', 'opts': ['farad', 'henry', 'tesla', 'ohm'], 'ok': 1, 'why': '1 H = 1 V·s/A.'},
          {'q': 'Doubling the turns of a solenoid multiplies L by…', 'opts': ['2', '4', '½', '1'], 'ok': 1, 'why': 'L ∝ N².'},
          {'q': 'The RL time constant is…', 'opts': ['RL', 'L/R', 'R/L', '√(LC)'], 'ok': 1, 'why': 'τ = L/R.'},
          {'q': 'An LC circuit is the electrical analog of…', 'opts': ['friction', 'a mass on a spring', 'a falling body', 'a lever'], 'ok': 1, 'why': 'Energy swaps back and forth.'}],
 'cards': [('Self-inductance', 'ε = −L dI/dt.'), ('Mutual inductance', 'ε₂ = −M dI₁/dt.'), ('Solenoid inductance', 'L = μ₀N²A/l.'), ('RL time constant', 'τ = L/R.'), ('Inductor energy', 'U = ½LI².'), ('LC frequency', 'ω = 1/√(LC).')],
 'planet': {'text': ['Space weather is induction on a planetary scale. NOAA’s Space Weather Prediction Center explains that geomagnetic storms create harmful geomagnetically induced currents in the power grid and pipelines, as well as beautiful aurora. The storms are driven by coronal mass ejections, which NOAA says leave the Sun at speeds from below 250 km/s to nearly 3,000 km/s; the fastest Earth-directed ones arrive in as little as 15 to 18 hours.'],
            'site': [('Space Weather', 'Space_Weather.html'), ('Solar Orbiter', 'Solar_Orbiter.html')],
            'src': [_GS, _CME]},
 'res': [('OpenStax UP2, 14.1 Mutual inductance', _O + '14-1-mutual-inductance', 'Mutual inductance.'), ('OpenStax UP2, 14.2 Self-inductance and inductors', _O + '14-2-self-inductance-and-inductors', 'Inductors.'),
         ('OpenStax UP2, 14.4 RL circuits', _O + '14-4-rl-circuits', 'RL circuits.'), ('OpenStax UP2, 14.5 Oscillations in an LC circuit', _O + '14-5-oscillations-in-an-lc-circuit', 'LC circuits.')]})
UNITS.append(
{'id': 'u9', 'title': 'AC Circuits, Transformers and the Power Grid', 'weeks': 'Week 12',
 'summary': 'Alternating current, RMS values, reactance and impedance, phasors, RLC resonance, power factor, transformers, and why the grid transmits at high voltage.',
 'objectives': ['Convert between peak and RMS values.', 'Find reactance, impedance, phase and current in a series RLC circuit.', 'Compute average power and power factor.', 'Use transformer ratios and explain high-voltage transmission.'],
 'concepts': ['Household AC is sinusoidal; meters read RMS values, with V_rms = V₀/√2.', 'Inductors have reactance X_L = ωL and capacitors X_C = 1/(ωC). In a series RLC circuit Z = √(R² + (X_L − X_C)²).',
              'The current leads or lags the voltage by φ with tan φ = (X_L − X_C)/R. Average power is P = I_rms V_rms cos φ; cos φ is the power factor.',
              'At resonance ω₀ = 1/√(LC), X_L = X_C and the current is largest.', 'An ideal transformer keeps power: V₂/V₁ = N₂/N₁ and I₂/I₁ = N₁/N₂. It works only with AC, by mutual induction.',
              'Line loss is I²R. Sending the same power at 10 times the voltage cuts current 10 times and losses 100 times.'],
 'eqs': [('V_{\\text{rms}}=\\frac{V_0}{\\sqrt2}', 'RMS value'), ('X_L=\\omega L,\\quad X_C=\\frac1{\\omega C}', 'Reactance'), ('Z=\\sqrt{R^2+(X_L-X_C)^2},\\ \\tan\\varphi=\\frac{X_L-X_C}{R}', 'Impedance and phase'),
         ('P=I_{\\text{rms}}V_{\\text{rms}}\\cos\\varphi', 'Average power'), ('\\frac{V_2}{V_1}=\\frac{N_2}{N_1}', 'Transformer'), ('P_{\\text{loss}}=I^2R=\\left(\\frac{P}{V}\\right)^2R', 'Line loss')],
 'worked': [
  {'q': 'A series circuit has R = 20 Ω, L = 0.1 H and C = 100 µF on 120 V RMS at 60 Hz. Find the impedance, current, phase and power.', 'steps': ['X_L = 2π × 60 × 0.1 = 37.7 Ω; X_C = 1/(2π × 60 × 10⁻⁴) = 26.5 Ω.', 'Z = √(20² + 11.2²) = 22.9 Ω; I = 120/22.9 = 5.24 A.', 'tan φ = 11.2/20, φ = 29.2°; P = I²R = 549 W.'], 'a': '22.9 Ω, 5.24 A, current lags by 29.2° (power factor 0.873), 549 W.'},
  {'q': 'Send 100 MW over a line with 10 Ω resistance at 345 kV and at 34.5 kV. Compare the losses.', 'steps': ['345 kV: I = 290 A, loss = I²R = 0.84 MW (0.84%).', '34.5 kV: I = 2,899 A, loss = 84 MW.'], 'a': '0.84 MW versus 84 MW. Ten times the voltage gives one hundredth of the loss, which is why long lines run at hundreds of kilovolts.'},
  {'q': 'A pole transformer steps 7,200 V down to 240 V (sample values). Find the turns ratio, and the primary current when the secondary supplies 30 A.', 'steps': ['N₁/N₂ = 7,200/240 = 30.', 'I₁ = I₂/30.'], 'a': '30:1; 1.0 A.'}],
 'practice': [('Find the peak voltage of 120 V RMS.', '169.7 V.'), ('Find the resonant frequency of the RLC circuit above.', 'f₀ = 1/(2π√(LC)) ≈ 50.3 Hz.'),
              ('Why can’t a transformer step up DC?', 'A steady current makes a steady flux, which induces no EMF.'), ('What happens to X_C as frequency rises?', 'It falls: capacitors pass high frequencies.')],
 'misc': [('RMS is the average voltage.', 'The average of a sine wave is zero; RMS is the root of the mean square.'), ('A transformer makes power.', 'It trades voltage for current; power out ≤ power in.'),
          ('Impedances add like resistances.', 'They add as vectors (phasors), not as plain numbers.')],
 'quiz': [{'q': 'At resonance in a series RLC circuit…', 'opts': ['X_L = X_C', 'Z = 0', 'I = 0', 'R = 0'], 'ok': 0, 'why': 'Reactances cancel, Z = R.'},
          {'q': 'Raising transmission voltage 10 times changes line loss by…', 'opts': ['×10', '×1/10', '×1/100', '×100'], 'ok': 2, 'why': 'Loss ∝ I² ∝ 1/V².'},
          {'q': 'A step-up transformer has…', 'opts': ['N₂ > N₁', 'N₂ < N₁', 'N₂ = N₁', 'no secondary'], 'ok': 0, 'why': 'V₂/V₁ = N₂/N₁.'},
          {'q': 'A power factor of 1 means…', 'opts': ['current and voltage in phase', 'no current', 'pure inductor', 'pure capacitor'], 'ok': 0, 'why': 'cos 0 = 1.'}],
 'cards': [('RMS', 'V_rms = V₀/√2.'), ('Inductive reactance', 'X_L = ωL.'), ('Capacitive reactance', 'X_C = 1/(ωC).'), ('Impedance', 'Z = √(R² + (X_L − X_C)²).'), ('Power factor', 'cos φ = R/Z.'),
           ('Transformer', 'V₂/V₁ = N₂/N₁.'), ('Line loss', 'I²R = (P/V)²R.')],
 'planet': {'text': ['The U.S. Energy Information Administration estimates that transmission and distribution losses averaged about 5% of the electricity sent through the U.S. grid in 2018 through 2022. EIA describes the grid as thousands of miles of high-voltage power lines and millions of miles of low-voltage lines. High voltage for distance, then transformers down to safe levels near customers, is the worked example above at national scale. Every percent saved means less fuel burned or more clean power delivered.'],
            'site': [('Physics I', 'Physics_I.html')],
            'src': [_EIA, _GRID]},
 'res': [('OpenStax UP2, 15.2 Simple AC circuits', _O + '15-2-simple-ac-circuits', 'AC basics.'), ('OpenStax UP2, 15.3 RLC series circuits with AC', _O + '15-3-rlc-series-circuits-with-ac', 'Impedance.'),
         ('OpenStax UP2, 15.4 Power in an AC circuit', _O + '15-4-power-in-an-ac-circuit', 'Power factor.'), ('OpenStax UP2, 15.6 Transformers', _O + '15-6-transformers', 'Transformers.'),
         ('PhET: Circuit Construction Kit: AC', _PH + 'circuit-construction-kit-ac', 'Interactive.')]})
UNITS.append(
{'id': 'u10', 'title': 'Maxwell’s Equations, Electromagnetic Waves and Optics', 'weeks': 'Weeks 13–14',
 'summary': 'The displacement current and Maxwell’s four equations, light as an electromagnetic wave, energy and momentum of light, the spectrum, and an introduction to optics: reflection, refraction, total internal reflection, polarization and thin lenses.',
 'objectives': ['State Maxwell’s equations and the role of displacement current.', 'Derive c = 1/√(μ₀ε₀) and relate f, λ and photon energy.', 'Compute intensity, field amplitudes and radiation pressure.', 'Use Snell’s law, the critical angle, Malus’s law and the thin-lens equation.'],
 'concepts': ['Maxwell added the displacement current ε₀ dΦ_E/dt to Ampère’s law. With it, the four equations (Gauss for E and B, Faraday, Ampère–Maxwell) predict waves.',
              'The waves travel at c = 1/√(μ₀ε₀) = 3.00 × 10⁸ m/s, with E ⊥ B ⊥ direction of travel and E = cB. Light is one of these waves.',
              'Waves carry energy: intensity I = ½cε₀E₀², and momentum, pressure I/c on an absorber.', 'The spectrum runs from radio through microwave, infrared, visible, ultraviolet and X-ray to gamma; c = fλ and photon energy E = hf.',
              'At a boundary, light reflects at equal angles and refracts by Snell’s law n₁ sin θ₁ = n₂ sin θ₂. Going from a denser medium, beyond the critical angle all light reflects.',
              'A polarizer passes I = I₀cos²θ (Malus). A thin lens obeys 1/f = 1/d_o + 1/d_i.'],
 'eqs': [('\\oint\\vec E\\cdot d\\vec A=\\frac{Q}{\\varepsilon_0},\\ \\oint\\vec B\\cdot d\\vec A=0', 'Gauss’s laws'), ('\\oint\\vec E\\cdot d\\vec l=-\\frac{d\\Phi_B}{dt},\\ \\oint\\vec B\\cdot d\\vec l=\\mu_0I+\\mu_0\\varepsilon_0\\frac{d\\Phi_E}{dt}', 'Faraday and Ampère–Maxwell'),
         ('c=\\frac1{\\sqrt{\\mu_0\\varepsilon_0}}=f\\lambda,\\quad E=cB', 'Electromagnetic waves'), ('I=\\tfrac12c\\varepsilon_0E_0^2,\\quad p=\\frac Ic', 'Intensity and radiation pressure'),
         ('n_1\\sin\\theta_1=n_2\\sin\\theta_2', 'Snell’s law'), ('I=I_0\\cos^2\\theta,\\quad \\frac1f=\\frac1{d_o}+\\frac1{d_i}', 'Malus and thin lens')],
 'worked': [
  {'q': 'Compute c from μ₀ and ε₀.', 'steps': ['c = 1/√(4π × 10⁻⁷ × 8.854 × 10⁻¹²).'], 'a': '2.998 × 10⁸ m/s, the measured speed of light, which told Maxwell that light is electromagnetic.'},
  {'q': 'Landsat 9’s near-infrared band runs 0.85–0.88 µm and its red band 0.64–0.67 µm (NASA). Find the frequency at each band’s center (0.865 and 0.655 µm) and the photon energy in the red.', 'steps': ['f = c/λ: 3.47 × 10¹⁴ Hz and 4.58 × 10¹⁴ Hz.', 'E = hc/λ = 3.03 × 10⁻¹⁹ J = 1.89 eV.'], 'a': 'NIR 3.47 × 10¹⁴ Hz; red 4.58 × 10¹⁴ Hz; 1.89 eV.'},
  {'q': 'Bright sunlight of 1,000 W/m² (sample value) hits a panel. Find E₀, B₀ and the pressure on an absorbing surface.', 'steps': ['E₀ = √(2I/(cε₀)) = 868 V/m.', 'B₀ = E₀/c = 2.90 µT.', 'p = I/c = 3.34 µPa.'], 'a': '868 V/m, 2.90 µT, 3.34 µPa.'},
  {'q': 'Light enters water (n = 1.33) at 30° from the normal. Find the refraction angle and the critical angle for light leaving water.', 'steps': ['sin θ₂ = sin 30°/1.33, θ₂ = 22.1°.', 'sin θ_c = 1/1.33, θ_c = 48.8°.'], 'a': '22.1°; 48.8°.'}],
 'practice': [('Find the wavelength of 2.4 GHz Wi-Fi.', '12.5 cm.'), ('About how long does sunlight take to cover 1.5 × 10¹¹ m?', '≈ 8.3 minutes.'),
              ('Find the critical angle for glass (n = 1.5) to air.', '41.8°.'), ('Unpolarized light passes two polarizers at 60°. What fraction of the light leaving the first passes the second?', 'cos² 60° = 0.25.'),
              ('An object sits 30 cm from a lens of focal length 10 cm. Where is the image?', '1/d_i = 1/10 − 1/30, d_i = 15 cm, real and inverted.'),
              ('Landsat 9’s thermal band 10 is near 11 µm. Find the photon energy.', '≈ 0.113 eV, far less than visible photons: thermal sensors read heat, not color.')],
 'misc': [('Light needs a medium.', 'EM waves travel through vacuum.'), ('Radio and light are different things.', 'Same waves, different wavelengths.'), ('Light bends away from the normal entering water.', 'Toward the normal: it slows down.')],
 'quiz': [{'q': 'The displacement current term was added by…', 'opts': ['Faraday', 'Ampère', 'Maxwell', 'Gauss'], 'ok': 2, 'why': 'Ampère–Maxwell law.'},
          {'q': 'In an EM wave, E and B are…', 'opts': ['parallel', 'perpendicular to each other and to the motion', 'along the motion', 'unrelated'], 'ok': 1, 'why': 'Transverse waves.'},
          {'q': 'Higher frequency means…', 'opts': ['longer λ, less energy per photon', 'shorter λ, more energy per photon', 'slower waves', 'no change'], 'ok': 1, 'why': 'c = fλ; E = hf.'},
          {'q': 'Total internal reflection happens when light goes from…', 'opts': ['air into water', 'water into air beyond θ_c', 'any medium', 'vacuum into glass'], 'ok': 1, 'why': 'Denser to less dense.'}],
 'cards': [('Maxwell’s equations', 'Gauss (E, B), Faraday, Ampère–Maxwell.'), ('Displacement current', 'ε₀ dΦ_E/dt.'), ('Speed of light', 'c = 1/√(μ₀ε₀).'), ('Wave relation', 'c = fλ.'), ('Photon energy', 'E = hf.'),
           ('Snell’s law', 'n₁ sin θ₁ = n₂ sin θ₂.'), ('Critical angle', 'sin θ_c = n₂/n₁.'), ('Malus’s law', 'I = I₀ cos²θ.'), ('Thin lens', '1/f = 1/d_o + 1/d_i.')],
 'planet': {'text': ['Satellites watch the planet by measuring electromagnetic waves. NASA lists Landsat 9’s bands, from the coastal/aerosol band at 0.43 µm through visible, near-infrared and shortwave infrared to thermal infrared at 10.60–12.51 µm. NASA says these observations support tropical deforestation alerts, water-quality monitoring and crop condition reports, and the thermal sensor measures land surface temperature to help manage water in drought-prone regions. Each band is a slice of the spectrum chosen because land, water and plants reflect or emit it differently.',
                     'NASA’s tour of the electromagnetic spectrum shows how each band, from radio to gamma rays, is used to study Earth and space.'],
            'site': [('Landsat 9', 'Landsat_9.html'), ('GOES-19', 'GOES-19.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_L9, _EMS]},
 'res': [('OpenStax UP2, 16.1 Maxwell’s equations and electromagnetic waves', _O + '16-1-maxwells-equations-and-electromagnetic-waves', 'Maxwell.'), ('OpenStax UP2, 16.3 Energy carried by EM waves', _O + '16-3-energy-carried-by-electromagnetic-waves', 'Intensity.'),
         ('OpenStax UP2, 16.5 The electromagnetic spectrum', _O + '16-5-the-electromagnetic-spectrum', 'Spectrum.'), ('OpenStax UP3, 1.3 Refraction', _O3 + '1-3-refraction', 'Snell’s law.'),
         ('OpenStax UP3, 1.7 Polarization', _O3 + '1-7-polarization', 'Polarization.'), ('OpenStax UP3, 2.4 Thin lenses', _O3 + '2-4-thin-lenses', 'Lenses.'), ('PhET: Bending Light', _PH + 'bending-light', 'Interactive.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Mapping electric fields and equipotentials', 'week': 'Week 2',
 'goal': 'Measure how the field of a point charge falls with distance, confirm the inverse-square law with a log-log fit, and map equipotentials around a dipole.',
 'eq': ('E=\\frac{kq}{r^2}\\ \\Rightarrow\\ \\log E=\\log(kq)-2\\log r', 'A straight line of slope −2 on a log-log plot'),
 'steps': ['Open PhET Charges and Fields. Place a single +1 nC charge and turn on the values and grid.', 'Use the E-field sensor at 0.5, 1.0, 1.5 and 2.0 m and record E.', 'Plot log E against log r and fit a line; compare the slope with −2 and the intercept with log(kq).',
           'Add a −1 nC charge 1 m away, use the voltmeter tool to trace the 0 V and ±10 V equipotentials, and sketch field lines perpendicular to them.'],
 'table': (['r (m)', 'E (V/m)'], [['0.5', '35.95'], ['1.0', '8.99'], ['1.5', '3.99'], ['2.0', '2.25']]),
 'note': 'Values computed from E = kq/r² for q = 1 nC; your simulation readings should match to within rounding.',
 'calc': ['From 0.5 m to 2.0 m (×4 in r), E falls from 35.95 to 2.25 V/m (×1/16), so the log-log slope is −2.', 'The 0 V equipotential of the dipole is the perpendicular bisector of the two charges, yet the field there is not zero.'],
 'safety': ['None beyond normal computer use.'], 'home': ['Rub a balloon on hair and watch it lift paper bits at different distances: a qualitative look at a field that falls off quickly with distance.'],
 'sims': [('PhET: Charges and Fields', _PH + 'charges-and-fields'), ('PhET: Coulomb’s Law', _PH + 'coulombs-law')],
 'planet': 'Field maps like these are how engineers design the electric fields inside solar cells and high-voltage equipment.', 'planet_src': [_SOLAR]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Capacitance and plate separation', 'week': 'Week 5',
 'goal': 'Measure how a parallel-plate capacitor’s capacitance depends on plate separation, and extract ε₀ from the data.',
 'eq': ('C=\\frac{\\varepsilon_0A}{d}', 'Plot C against 1/d; the slope is ε₀A'),
 'steps': ['Open PhET Capacitor Lab: Basics. Set the plate area to 400 mm² and connect the battery at 1.5 V.', 'Read C at plate separations of 2, 4, 6, 8 and 10 mm.', 'Plot C against 1/d and fit a line through the origin; divide the slope by A to get ε₀.',
           'At d = 5 mm, record the stored energy and compare with ½CV².'],
 'table': (['d (mm)', 'C (pF)'], [['2', '1.77'], ['4', '0.885'], ['6', '0.590'], ['8', '0.443'], ['10', '0.354']]),
 'note': 'Values computed from C = ε₀A/d; simulation readouts round them.',
 'calc': ['C × d is constant: 1.77 pF × 2 mm = 0.354 pF × 10 mm, so C ∝ 1/d.', 'Slope ε₀A = 3.54 × 10⁻¹⁵ F·m, so ε₀ = 3.54 × 10⁻¹⁵/(4 × 10⁻⁴) = 8.85 × 10⁻¹² F/m.', 'At 5 mm, C = 0.708 pF and U = ½CV² = 0.797 pJ at 1.5 V.'],
 'safety': ['None beyond normal computer use.'], 'home': ['Optional: with a multimeter that reads capacitance, measure two pieces of aluminum foil separated by one, two and three sheets of paper. C should fall as the stack grows.'],
 'sims': [('PhET: Capacitor Lab: Basics', _PH + 'capacitor-lab-basics')],
 'planet': 'Capacitors smooth power in electric cars, solar inverters and the grid; the same C = κε₀A/d sets their size.', 'planet_src': [_EV]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Ohm’s law, Kirchhoff’s rules and an RC time constant', 'week': 'Week 7',
 'goal': 'Confirm Ohm’s law, check Kirchhoff’s rules in a two-loop circuit, and measure the time constant of a charging capacitor.',
 'eq': ('V_C=V_0\\left(1-e^{-t/RC}\\right)', 'Charging curve; ln(1 − V_C/V₀) = −t/RC is a straight line'),
 'steps': ['Ohm’s law: put a 1 kΩ resistor across 1.5, 3.0, 4.5, 6.0 and 9.0 V (AA cells in series, or the PhET battery) and record the current; plot I against V.',
           'Kirchhoff: in PhET Circuit Construction Kit: DC, build the Unit 4 circuit (12 V, 6 V, 2 Ω, 3 Ω, 6 Ω) and measure the three currents; check the junction and loop sums.',
           'RC: charge a 100 µF capacitor from 9 V through 10 kΩ, reading V_C every second; plot ln(1 − V_C/9) against t and find RC from the slope.'],
 'table': (['t (s)', 'V_C (V), 10 kΩ and 100 µF from 9 V'], [['0', '0.00'], ['1', '5.69'], ['2', '7.78'], ['3', '8.55'], ['5', '8.94']]),
 'note': 'Values computed for ideal parts; real capacitors are often ±20% from their label, so your τ may differ.',
 'calc': ['Ohm’s law: the slope of I against V is 1 mA/V, so R = 1.00 kΩ; at 9 V the resistor dissipates only 81 mW.', 'Kirchhoff: 2 A − 0.667 A = 1.33 A at the junction, and 12 − 2(2) − 6(1.33) = 0 around loop 1.',
          'RC: the line through ln(1 − V_C/9) has slope −1.0 s⁻¹, so τ = 1.0 s = (10 kΩ)(100 µF).'],
 'safety': ['Use only batteries of 9 V or less; never wall power.', 'Never connect a wire straight across a battery: it heats fast and can burn.', 'Electrolytic capacitors have a + lead; connect it toward the battery’s + side, and use one rated above 9 V.'],
 'home': ['Everything here works with a multimeter, AA cells, a 9 V battery, resistors and a capacitor on a breadboard; time the RC readings with a phone video of the meter.'],
 'sims': [('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc'), ('PhET: Ohm’s Law', _PH + 'ohms-law'), ('PhET: Resistance in a Wire', _PH + 'resistance-in-a-wire')],
 'planet': 'Solar arrays are wired by the same rules: series strings raise voltage and parallel strings raise current.', 'planet_src': [_SOLAR]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Measuring magnetic fields, including Earth’s', 'week': 'Week 9',
 'goal': 'Measure Earth’s magnetic field with a phone magnetometer, map the field of a wire in simulation, and compare both with theory.',
 'eq': ('B=\\frac{\\mu_0I}{2\\pi r}', 'Field of a long wire'),
 'steps': ['Open a magnetometer app away from metal and electronics. Record the total field magnitude at five spots and average them.', 'Compare with NOAA’s stated range of about 25,000–65,000 nT at Earth’s surface.',
           'In PhET Magnets and Electromagnets, see how the field changes with current and number of loops; then compute B for a long wire with I = 2 A at r = 1, 2 and 4 cm and plot B against 1/r.',
           'Bring a fridge magnet toward the phone and note the distance at which its field equals Earth’s.'],
 'table': (['r (cm)', 'B for a 2 A wire (µT)'], [['1', '40'], ['2', '20'], ['4', '10']]),
 'note': 'Wire values computed from μ₀I/(2πr). Earth-field readings depend on your location; NOAA’s calculator gives the expected total for your spot.',
 'calc': ['B ∝ 1/r: doubling the distance halves the field, so the plot of B against 1/r is a straight line through the origin with slope μ₀I/(2π) = 0.4 µT·m.', 'A 2 A wire matches Earth’s 50 µT field at r = μ₀I/(2π × 50 µT) = 0.8 cm.'],
 'safety': ['Keep strong magnets away from phones’ card slots, pacemakers and credit cards.', 'Do not run high current through bare wire at home; the wire part of this lab is done in simulation.'],
 'home': ['The magnetometer and fridge-magnet steps are the home version.'],
 'sims': [('PhET: Magnets and Electromagnets', _PH + 'magnets-and-electromagnets'), ('PhET: Magnet and Compass', _PH + 'magnet-and-compass'), ('NOAA magnetic field calculators', 'https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml')],
 'planet': 'Knowing the normal field is the baseline for spotting geomagnetic storms, which NOAA warns can induce harmful currents in power grids.', 'planet_src': [_GEO, _GS]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Induction and a model generator', 'week': 'Week 10',
 'goal': 'Show that induced EMF depends on the rate of change of flux, and that a generator’s peak EMF grows in proportion to its spin rate.',
 'eq': ('\\varepsilon_{\\max}=NBA\\omega', 'Peak EMF of a spinning coil'),
 'steps': ['In PhET Faraday’s Law, push the magnet through the coil slowly and then quickly; record the peak voltage reading each time and note the sign change when it leaves.',
           'In PhET Faraday’s Electromagnetic Lab (Generator tab), change the turbine speed and record the peak bulb or voltmeter response.', 'Compute ε_max for a model coil with N = 200, A = 0.01 m² and B = 0.05 T at 1, 2 and 3 revolutions per second.',
           'Home: wind 100 turns of thin insulated wire around a toilet-paper tube, connect a multimeter on mV, and drop a strong magnet through it.'],
 'table': (['Spin rate (rev/s)', 'Peak EMF (V)'], [['1', '0.628'], ['2', '1.26'], ['3', '1.88']]),
 'note': 'Values computed for the model coil (sample values).',
 'calc': ['ε_max = NBA(2πf) = 200 × 0.05 × 0.01 × 2π f = 0.628 V per rev/s, so doubling the speed doubles the EMF.', 'A faster magnet gives a taller, shorter pulse; the area under the EMF-time curve (total flux change × N) stays the same.'],
 'safety': ['Strong neodymium magnets snap together hard and can pinch skin or shatter; handle one at a time.', 'Keep magnets away from pacemakers and electronics.'],
 'home': ['The coil-and-magnet step is the home version; any multimeter on its millivolt range works.'],
 'sims': [('PhET: Faraday’s Law', _PH + 'faradays-law'), ('PhET: Faraday’s Electromagnetic Lab', _PH + 'faradays-electromagnetic-lab'), ('PhET: Generator', _PH + 'generator')],
 'planet': 'Every wind turbine and hydro plant runs this lab at megawatt scale: the turbine spins a generator to make electricity.', 'planet_src': [_WIND, _HYDRO]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Refraction and Snell’s law', 'week': 'Week 14',
 'goal': 'Measure refraction angles from air into water, find the index of refraction, and observe total internal reflection.',
 'eq': ('n=\\frac{\\sin\\theta_1}{\\sin\\theta_2}', 'Slope of sin θ₁ against sin θ₂'),
 'steps': ['In PhET Bending Light, set the lower medium to water and shine the laser at 10° to 60° from the normal in 10° steps; read the refraction angle with the protractor tool.',
           'Plot sin θ₁ against sin θ₂ and fit a line through the origin; the slope is n.', 'Put the laser in the water and increase the angle until the refracted beam vanishes; record the critical angle.',
           'Home: shine a low-power laser or narrow flashlight beam into a clear box of water with a drop of milk and measure the angles on a printed protractor.'],
 'table': (['θ₁ in air (°)', 'θ₂ in water (°)'], [['10', '7.5'], ['20', '14.9'], ['30', '22.1'], ['40', '28.9'], ['50', '35.2'], ['60', '40.6']]),
 'note': 'Values computed from Snell’s law with n = 1.33.',
 'calc': ['sin 30°/sin 22.1° = 0.500/0.376 = 1.33, and every row gives the same ratio.', 'Critical angle from water to air: sin⁻¹(1/1.33) = 48.8°.'],
 'safety': ['Use only a class 2 (under 1 mW) laser pointer, and never look into the beam or aim it at anyone’s eyes; watch for reflections off the water and glass.'],
 'home': ['The water-box step is the home version.'],
 'sims': [('PhET: Bending Light', _PH + 'bending-light')],
 'planet': 'Satellite sensors are built from lenses, mirrors and filters designed with these same laws of refraction and reflection.', 'planet_src': [_L9]})
SCHEDULE = [(1, 'u1', 'Charge, Coulomb’s law, superposition', 'OpenStax UP2 5.1–5.3'), (2, 'u1', 'Electric fields, continuous charge, field lines; Lab A', 'UP2 5.4–5.6'),
            (3, 'u2', 'Flux and Gauss’s law; conductors', 'UP2 6.1–6.4'), (4, 'u3', 'Potential energy, potential, equipotentials', 'UP2 7.1–7.5'),
            (5, 'u3', 'Capacitance, energy, dielectrics; Lab B', 'UP2 8.1–8.4'), (6, 'u4', 'Current, resistance, power', 'UP2 9.1–9.5'),
            (7, 'u4', 'DC circuits, Kirchhoff’s rules, RC circuits; Lab C', 'UP2 10.1–10.5'), (8, 'u5', 'Magnetic force, particle orbits, motors; midterm practice', 'UP2 11.1–11.5'),
            (9, 'u6', 'Biot–Savart, Ampère’s law, solenoids; Lab D', 'UP2 12.1–12.7'), (10, 'u7', 'Faraday’s and Lenz’s laws, generators; Lab E', 'UP2 13.1–13.7'),
            (11, 'u8', 'Inductance, RL and LC circuits', 'UP2 14.1–14.6'), (12, 'u9', 'AC circuits, resonance, power, transformers', 'UP2 15.1–15.6'),
            (13, 'u10', 'Maxwell’s equations, EM waves, energy and the spectrum', 'UP2 16.1–16.5'), (14, 'u10', 'Optics: reflection, refraction, polarization, lenses; Lab F', 'UP3 1.1–1.7, 2.4'),
            (15, 'exam', 'Review and final practice set', 'All units')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Charges of +2.0 µC and +8.0 µC are 0.30 m apart. Find the force between them and the point between them where E = 0.', ['F = k(2 × 10⁻⁶)(8 × 10⁻⁶)/0.09.', 'k(2)/x² = k(8)/(0.3 − x)² gives x = 0.10 m.'], '1.60 N, repulsive; 0.10 m from the 2.0 µC charge.'),
  ('A closed surface surrounds a 3.0 nC charge. Find the net flux.', ['Φ = Q/ε₀.'], '≈ 339 N·m²/C.'),
  ('A 10 µF capacitor is charged to 12 V. Find Q and U.', ['Q = CV; U = ½CV².'], '120 µC; 0.72 mJ.'),
  ('A 9 V battery drives 3 Ω in series with a parallel pair of 6 Ω and 3 Ω. Find the current and total power.', ['Parallel pair = 2 Ω; total 5 Ω.', 'I = 9/5; P = IV.'], '1.8 A; 16.2 W.'),
  ('A proton moves at 1.0 × 10⁶ m/s across a 0.20 T field. Find the orbit radius.', ['r = mv/(eB).'], '≈ 5.22 cm.')]),
 ('Final practice set (all units)', [
  ('Find B 0.10 m from a long wire carrying 50 A.', ['B = μ₀I/(2πr).'], '100 µT, about twice Earth’s field.'),
  ('A 50-turn coil of area 0.05 m² spins at 50 rev/s in a 0.20 T field. Find the peak EMF.', ['ε = NBAω, ω = 2π × 50.'], '≈ 157 V.'),
  ('An RL circuit has L = 0.5 H and R = 100 Ω. Find τ and the fraction of the final current after 5 ms.', ['τ = L/R.'], '5 ms; 63%.'),
  ('Send 50 MW at 230 kV over a line with 5 Ω resistance. Find the current and loss.', ['I = P/V; loss = I²R.'], '217 A; 0.236 MW (0.47%).'),
  ('Find the frequency and photon energy of 500 nm light.', ['f = c/λ; E = hf.'], '6.00 × 10¹⁴ Hz; 2.48 eV.'),
  ('Light enters glass (n = 1.5) at 45°. Find the refraction angle.', ['sin θ₂ = sin 45°/1.5.'], '28.1°.')])]
FORMULAS = ['F=k|q_1q_2|/r^2', '\\vec E=\\vec F/q', '\\oint\\vec E\\cdot d\\vec A=Q_{\\text{enc}}/\\varepsilon_0', 'V=kq/r,\\ E_x=-dV/dx', 'C=\\kappa\\varepsilon_0A/d,\\ U=\\tfrac12CV^2',
            'V=IR,\\ R=\\rho L/A,\\ P=IV', '\\tau=RC,\\ \\tau=L/R', '\\vec F=q\\vec v\\times\\vec B,\\ r=mv/(qB)', '\\vec F=I\\vec L\\times\\vec B,\\ \\tau=NIAB\\sin\\theta', 'B=\\mu_0I/(2\\pi r),\\ B=\\mu_0nI',
            '\\varepsilon=-N\\,d\\Phi_B/dt,\\ \\varepsilon=BLv', 'L=\\mu_0N^2A/l,\\ U=\\tfrac12LI^2', 'X_L=\\omega L,\\ X_C=1/(\\omega C),\\ Z=\\sqrt{R^2+(X_L-X_C)^2}', 'V_2/V_1=N_2/N_1',
            'c=1/\\sqrt{\\mu_0\\varepsilon_0}=f\\lambda,\\ E=hf', 'n_1\\sin\\theta_1=n_2\\sin\\theta_2,\\ 1/f=1/d_o+1/d_i']
GLOSSARY = sorted([('Ampère’s law', '∮B·dl = μ₀I_enc.'), ('Capacitance', 'Charge stored per volt, C = Q/V.'), ('Coulomb’s law', 'Force between point charges, F = k|q₁q₂|/r².'),
    ('Critical angle', 'Angle beyond which light is totally reflected inside a denser medium.'), ('Displacement current', 'ε₀ dΦ_E/dt, Maxwell’s addition to Ampère’s law.'), ('Electric field', 'Force per unit charge.'),
    ('Electric potential', 'Potential energy per unit charge, in volts.'), ('EMF', 'Energy per charge supplied by a source such as a battery or generator.'), ('Faraday’s law', 'Changing magnetic flux induces EMF.'),
    ('Gauss’s law', 'Net electric flux out of a closed surface equals Q_enc/ε₀.'), ('Geomagnetically induced current', 'Current driven in grids and pipelines by geomagnetic storms.'), ('Impedance', 'Total opposition to AC, Z.'),
    ('Inductance', 'EMF per rate of change of current, in henries.'), ('Lenz’s law', 'Induced current opposes the change in flux.'), ('Magnetic flux', 'Φ_B = ∫B·dA, in webers.'),
    ('Maxwell’s equations', 'Four laws that unify electricity, magnetism and light.'), ('Power factor', 'cos φ, the fraction of apparent power that does work.'), ('Resistivity', 'Material property ρ in R = ρL/A.'),
    ('RMS value', 'Root-mean-square, V₀/√2 for a sine wave.'), ('Snell’s law', 'n₁ sin θ₁ = n₂ sin θ₂.'), ('Transformer', 'Two coupled coils that change AC voltage.')])
RUBRIC = [('4 · Mastery', 'Sets up fields and circuits from a description, chooses the right law, handles signs and directions, and checks units and limits.'), ('3 · Proficient', 'Solves the practice problems with occasional sign or unit slips.'),
          ('2 · Developing', 'Follows worked examples but struggles to choose a Gaussian surface, loop or right-hand rule.'), ('1 · Beginning', 'Plugs numbers into formulas without a picture; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '25%'), ('Labs (PHYS 210L)', '20%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]

def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    k = 8.9875e9; e = 1.602e-19; e0 = 8.854e-12; mu = 4 * pi * 1e-7; c = 2.998e8; me = 9.109e-31; mp = 1.673e-27; G = 6.674e-11; h = 6.626e-34
    I3 = (12 / 2 + 6 / 3) / (1 + 6 / 2 + 6 / 3)  # loop 1: I1 = (12 - 6 I3)/2; loop 2: I2 = (6 - 6 I3)/3; junction I3 = I1 + I2
    I1 = (12 - 6 * I3) / 2; I2 = (6 - 6 * I3) / 3
    Cpp = e0 * 0.01 / 1e-3; L = mu * 500**2 * 1e-3 / 0.25
    XL = 2 * pi * 60 * 0.1; XC = 1 / (2 * pi * 60 * 100e-6); Z = sqrt(20**2 + (XL - XC)**2)
    sn = lambda a, n: degrees(asin(sin(radians(a)) / n))
    r = [
     ('u1 F', k * 3e-6 * 5e-6 / .04, 3.37), ('u1 E', k * 2e-9 / .09, 200), ('u1 mid', 2 * k * 4e-9 / .05**2, 28760), ('u1 each', k * 4e-9 / .05**2, 14380), ('u1 H', k * e * e / 5.29e-11**2, 8.24e-8),
     ('u1 ratio', k * e * e / (G * mp * mp), 1.23e36), ('u1 Fe', e * 200, 3.20e-17), ('u1 ae', e * 200 / me, 3.52e13),
     ('u2 flux', 1e-9 / e0, 113), ('u2 line', 2 * k * 2e-9 / .1, 360), ('u2 sheet', 5e-6 / (2 * e0), 2.82e5), ('u2 sphere', k * 1e-6 / .25, 3.60e4),
     ('u3 V', k * 2e-9 / .3, 59.9), ('u3 v', sqrt(2 * e * 100 / me), 5.93e6), ('u3 C', Cpp * 1e12, 88.5), ('u3 Q', Cpp * 12 * 1e9, 1.06), ('u3 U', .5 * Cpp * 144 * 1e9, 6.37),
     ('u3 ser', 1 / (1 / 2 + 1 / 3), 1.2), ('u3 diel', 3.4 * Cpp * 1e12, 301), ('u3 sc', .5 * 3000 * 2.7**2, 10.9e3), ('u3 Wh', .5 * 3000 * 2.7**2 / 3600, 3.04),
     ('u4 A', pi * .5e-3**2, 7.85e-7), ('u4 R', 1.68e-8 * 100 / (pi * .5e-3**2), 2.14), ('u4 I1', I1, 2), ('u4 I2', I2, -.667), ('u4 I3', I3, 1.33), ('u4 tau', 1e4 * 1e-4, 1.0),
     ('u4 V1', 9 * (1 - exp(-1)), 5.69), ('u4 V2', 9 * (1 - exp(-2)), 7.78), ('u4 V3', 9 * (1 - exp(-3)), 8.55), ('u4 V5', 9 * (1 - exp(-5)), 8.94), ('u4 bulbR', 120**2 / 60, 240), ('u4 bulbI', 60 / 120, .5),
     ('u4 par', 1 / (1 / 6 + 1 / 3), 2), ('u4 drift', 1 / (8.5e28 * e * pi * .5e-3**2), 9.4e-5), ('u4 drift mh', 1 / (8.5e28 * e * pi * .5e-3**2) * 3600, .337), ('u4 pv', 60 * .6, 36),
     ('u5 rp', mp * 4e5 / (e * 50e-6), 83.5), ('u5 F', 200 * .2 * .5, 20), ('u5 tau', 100 * 2 * .01 * .5, 1.0), ('u5 fc', e / (2 * pi * mp), 15.2e6), ('u5 re', me * 1e5 / (e * 50e-6), .0114), ('u5 vs', 1e4 / .1, 1e5),
     ('u6 line', mu * 1000 / (2 * pi * 20), 10e-6), ('u6 sol', mu * 1000 * 2, 2.51e-3), ('u6 sol/earth', mu * 2000 / 50e-6, 50), ('u6 wires', mu * 100 / (2 * pi * .01), 2.0e-3), ('u6 loop', mu * 5 / (2 * .05), 62.8e-6),
     ('u6 w1', mu * 2 / (2 * pi * .01), 40e-6), ('u6 w2', mu * 2 / (2 * pi * .02), 20e-6), ('u6 w4', mu * 2 / (2 * pi * .04), 10e-6),
     ('u7 w', 2 * pi * 60, 377), ('u7 emf', 100 * .5 * .04 * 2 * pi * 60, 754), ('u7 avg', 200 * .3 * .01 / .5, 1.2), ('u7 hydro', .9 * 1000 * 9.81 * 100 * 50, 44.1e6), ('u7 rod', .5 * .2 * 3, .3),
     ('u8 L', L, 1.26e-3), ('u8 tau', L / 10, .126e-3), ('u8 U', .5 * L * 4, 2.51e-3), ('u8 f', 1 / (2 * pi * sqrt(10e-3 * 1e-6)), 1.59e3), ('u8 M', .01 * 100, 1), ('u8 63', 1 - exp(-1), .63), ('u8 95', 1 - exp(-3), .95),
     ('u8 uB', 50e-6**2 / (2 * mu), 9.9e-4),
     ('u9 XL', XL, 37.7), ('u9 XC', XC, 26.5), ('u9 X', XL - XC, 11.2), ('u9 Z', Z, 22.9), ('u9 I', 120 / Z, 5.24), ('u9 phi', degrees(atan((XL - XC) / 20)), 29.2), ('u9 pf', 20 / Z, .873), ('u9 P', (120 / Z)**2 * 20, 549),
     ('u9 f0', 1 / (2 * pi * sqrt(.1 * 100e-6)), 50.3), ('u9 peak', 120 * sqrt(2), 169.7), ('u9 I345', 100e6 / 345e3, 290), ('u9 L345', (100e6 / 345e3)**2 * 10, .84e6), ('u9 I34', 100e6 / 34.5e3, 2899),
     ('u9 L34', (100e6 / 34.5e3)**2 * 10, 84e6), ('u9 ratio', 7200 / 240, 30), ('u9 I1', 30 / 30, 1.0),
     ('u10 c', 1 / sqrt(mu * e0), 2.998e8), ('u10 fnir', c / .865e-6, 3.47e14), ('u10 fred', c / .655e-6, 4.58e14), ('u10 EJ', h * c / .655e-6, 3.03e-19), ('u10 eV', h * c / .655e-6 / e, 1.89),
     ('u10 E0', sqrt(2 * 1000 / (c * e0)), 868), ('u10 B0', sqrt(2 * 1000 / (c * e0)) / c, 2.90e-6), ('u10 p', 1000 / c, 3.34e-6), ('u10 snell', sn(30, 1.33), 22.1), ('u10 crit', degrees(asin(1 / 1.33)), 48.8),
     ('u10 wifi', c / 2.4e9, .125), ('u10 sun', 1.5e11 / c / 60, 8.3), ('u10 glass', degrees(asin(1 / 1.5)), 41.8), ('u10 malus', cos(radians(60))**2, .25), ('u10 lens', 1 / (1 / 10 - 1 / 30), 15), ('u10 th', h * c / 11e-6 / e, .113),
     ('A .5', k * 1e-9 / .25, 35.95), ('A 1', k * 1e-9, 8.99), ('A 1.5', k * 1e-9 / 2.25, 3.99), ('A 2', k * 1e-9 / 4, 2.25), ('A slope', log(35.95 / 2.25) / log(.5 / 2), -2),
     ('B 2', e0 * 400e-6 / 2e-3 * 1e12, 1.77), ('B 4', e0 * 400e-6 / 4e-3 * 1e12, .885), ('B 6', e0 * 400e-6 / 6e-3 * 1e12, .590), ('B 8', e0 * 400e-6 / 8e-3 * 1e12, .443), ('B 10', e0 * 400e-6 / 10e-3 * 1e12, .354),
     ('B slope', e0 * 400e-6, 3.54e-15), ('B e0', 3.54e-15 / 4e-4, 8.85e-12), ('B C5', e0 * 400e-6 / 5e-3 * 1e12, .708), ('B U5', .5 * e0 * 400e-6 / 5e-3 * 1.5**2 * 1e12, .797),
     ('C P9', 9**2 / 1000, .081), ('C loop', 2 * I1 + 6 * I3, 12), ('C junc', I1 + I2, 1.33),
     ('D slope', mu * 2 / (2 * pi) * 1e6, .4), ('D match', mu * 2 / (2 * pi * 50e-6), .008),
     ('E 1', 200 * .05 * .01 * 2 * pi, .628), ('E 2', 200 * .05 * .01 * 4 * pi, 1.26), ('E 3', 200 * .05 * .01 * 6 * pi, 1.88),
     ('F 10', sn(10, 1.33), 7.5), ('F 20', sn(20, 1.33), 14.9), ('F 40', sn(40, 1.33), 28.9), ('F 50', sn(50, 1.33), 35.2), ('F 60', sn(60, 1.33), 40.6), ('F ratio', .5 / sin(radians(sn(30, 1.33))), 1.33), ('F s22', sin(radians(sn(30, 1.33))), .376),
     ('M1 F', k * 16e-12 / .09, 1.60), ('M1 x', .3 / 3, .1), ('M2', 3e-9 / e0, 339), ('M3 Q', 10e-6 * 12, 120e-6), ('M3 U', .5 * 10e-6 * 144, .72e-3), ('M4 I', 9 / (3 + 1 / (1 / 6 + 1 / 3)), 1.8), ('M4 P', 9 * 1.8, 16.2),
     ('M5', mp * 1e6 / (e * .2), .0522), ('F1', mu * 50 / (2 * pi * .1), 100e-6), ('F2', 50 * .2 * .05 * 2 * pi * 50, 157), ('F3', .5 / 100, .005), ('F4 I', 50e6 / 230e3, 217), ('F4 L', (50e6 / 230e3)**2 * 5, .236e6),
     ('F4 pct', (50e6 / 230e3)**2 * 5 / 50e6 * 100, .47), ('F5 f', c / 500e-9, 6.00e14), ('F5 E', h * c / 500e-9 / e, 2.48), ('F6', sn(45, 1.5), 28.1)]
    return r
