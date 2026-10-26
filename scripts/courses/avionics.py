"""Avionics & Systems Engineering (AERO 450): the systems engineering life cycle and requirements, architecture and interfaces, reliability and redundancy, safety analysis, digital electronics and data buses, navigation sensors, sensor fusion and Kalman filtering, communication and surveillance, real-time flight software, and integration, verification and operations.
Oct 25 2026, founder-approved four-year track, senior course 5. Same module fields as heat.py / scdesign.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, log10, exp, pi
ID = 'avionics'
STATUS = 'live'
YEAR = 4
PAGE = 'Avionics_Systems_Engineering.html'
CODE = 'AERO 450'
TITLE = 'Avionics & Systems Engineering'
LAB_NAME = 'Avionics and systems lab'
TAGLINE = 'Flight electronics and managing complex systems: requirements and the V-model, interfaces, reliability and redundancy, safety analysis, data buses, navigation sensors, Kalman filtering, ADS-B surveillance, real-time software, and verification, with six labs. Free, self-paced, and tied to Landsat 9, Hubble’s gyros, Dragonfly’s autonomy and FAA air traffic.'
DESC = 'Free self-study Avionics & Systems Engineering: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and spreadsheet labs, practice exams, tied to Landsat 9, Hubble, Dragonfly and ADS-B.'
ALT = 'The International Space Station seen from a departing spacecraft during a 2021 flyaround'
_PH = 'https://phet.colorado.edu/en/simulations/'
_SEH = ('NASA Systems Engineering Handbook', 'https://www.nasa.gov/reference/systems-engineering-handbook/')
_MIT = ('MIT OpenCourseWare 16.842 Fundamentals of Systems Engineering (Fall 2015)', 'https://ocw.mit.edu/courses/16-842-fundamentals-of-systems-engineering-fall-2015/')
_L9 = ('NASA Science: Landsat 9', 'https://landsat.gsfc.nasa.gov/satellites/landsat-9/landsat-9-overview/')
_HUB = ('NASA Science: NASA to change how it points Hubble Space Telescope', 'https://science.nasa.gov/missions/hubble/nasa-to-change-how-it-points-hubble-space-telescope/')
_DF = ('NASA Science: Dragonfly completes first simulated flight (Oct. 23, 2026)', 'https://science.nasa.gov/blogs/dragonfly/2026/10/23/nasas-dragonfly-completes-first-simulated-flight/')
_ADSB = ('FAA: Automatic Dependent Surveillance-Broadcast (ADS-B)', 'https://www.faa.gov/air_traffic/technology/adsb')
_ATO = ('FAA: Air Traffic By The Numbers', 'https://www.faa.gov/air_traffic/by_the_numbers')
_CCK = ('PhET: Circuit Construction Kit: DC', _PH + 'circuit-construction-kit-dc')
BANNER = ['images/ISS_Flyaround_2021.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg', 'images/ArtemisII_Launch_KSC_Hancock.jpg', 'images/JPSS2_Atlas_V_Launch_Pad.jpg']
CREDITS = {'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)', 'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)',
           'images/ArtemisII_Launch_KSC_Hancock.jpg': 'NASA', 'images/JPSS2_Atlas_V_Launch_Pad.jpg': 'NASA/Liz Wilk (KSC-20221109-PH-LNW01_0001)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester senior course in avionics and systems engineering. It is modeled on the topics and depth of MIT 16.842 Fundamentals of Systems Engineering (free on MIT OpenCourseWare) and the NASA Systems Engineering Handbook, which we link where they help. Neither MIT nor NASA endorses this page.',
         'What we add: every unit ties to real work with a cited public source (Landsat 9, Hubble, Dragonfly and the FAA’s air traffic system), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a spreadsheet.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Earth-observing satellites, weather spacecraft and efficient air traffic all depend on avionics that work for years without a repair visit, and on systems engineering that makes thousands of parts behave as one.',
                 'Good requirements, redundancy and testing are what let a satellite keep measuring forests, ice and oceans long past its design life. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Circuits: voltage, current, resistance and digital signals.', 'Probability & Statistics: probability rules, exponential distribution and variance.',
           'Flight Dynamics & Controls: feedback, sensors and actuators.', 'Intro to Programming: loops, functions and timing.']
STUDY = ['Start every problem from the requirement it serves.', 'Draw block diagrams and interfaces before computing anything.',
         'Keep probabilities as numbers between 0 and 1 and check that they stay there.', 'Track units: bits, bytes, seconds, hertz, decibels.',
         'Ask “what happens if this part fails?” for every box you draw.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Circuit Construction Kit: DC simulation.', 'Spreadsheet software (any free one works), or Python.',
            'The free NASA Systems Engineering Handbook in a web browser.', 'A calculator.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free simulation or a spreadsheet, so there are no electrical hazards. Do not open or modify real aircraft, drone or vehicle electronics for this course. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST: CODATA value, speed of light in vacuum', 'https://physics.nist.gov/cgi-bin/cuu/Value?c')
CONSTANTS = [('Speed of light', 'c = 299,792,458 m/s (exact)'), ('Standard gravity', 'g = 9.80665 m/s²'), ('ADS-B frequency (textbook value)', '1090 MHz'),
             ('ARINC 429 high speed (textbook value)', '100 kbit/s'), ('MIL-STD-1553 (textbook value)', '1 Mbit/s'), ('Hours per year', '8760 h')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free texts, lectures and simulations alongside the course.'
PTABLE = [(_SEH[0], _SEH[1], 'Free NASA handbook.'), (_MIT[0], _MIT[1], 'Free MIT lectures.'), (_ADSB[0], _ADSB[1], 'FAA overview.'),
          (_CCK[0], _CCK[1], 'Circuits and redundancy.'), (_DF[0], _DF[1], 'Avionics testing story.'), (_HUB[0], _HUB[1], 'Redundancy in practice.')]
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS = []
UNITS.append(
{'id': 'u1', 'title': 'The Systems Engineering Life Cycle and Requirements', 'weeks': 'Week 1',
 'summary': 'Stakeholders, the V-model, life-cycle phases and reviews, good requirements, technical performance measures and margins.',
 'objectives': ['Describe the V-model.', 'Write verifiable requirements.', 'Compute margins against a requirement.', 'Track a technical performance measure.'],
 'concepts': ['Systems engineering turns stakeholder needs into a system that works, on time and on budget, across its whole life.',
              'The V-model goes down the left side (requirements, architecture, design) and up the right (integration, verification, validation).',
              'A good requirement is necessary, clear, feasible and verifiable, with a number, a unit and a test method.',
              'Technical performance measures such as mass, power and data rate are tracked against allocations with margin.',
              'Reviews (concept, preliminary design, critical design) gate each phase; MIT 16.842 students prepare a preliminary-design-review-level design.'],
 'eqs': [('\\text{Margin}=\\frac{C-N}{N}', 'Margin over need'), ('m_{alloc}=m_{est}(1+M)', 'Allocation with margin'), ('S=\\sum w_is_i', 'Weighted trade score'), ('\\sum w_i=1', 'Weights sum to one')],
 'worked': [
  _w('NASA requires Landsat 9 to collect at least 400 scenes a day; it collects 740. Find the margin.', ['(740 − 400)/400.'], '85% above the requirement.'),
  _w('An avionics box is estimated at 12 kg. Allocate with 25% margin (sample values).', ['12 × 1.25.'], '15 kg.'),
  _w('Option A scores 7 (cost) and 8 (reliability); B scores 9 and 6. Weights 0.3 and 0.7. Which wins?', ['A = 2.1 + 5.6 = 7.7.', 'B = 2.7 + 4.2 = 6.9.'], 'A, 7.7 to 6.9.')],
 'practice': [('Landsat 9 design life is 5 years and consumables last 10 years. Ratio?', '2.'), ('Allocate 400 W of power at 30% margin.', '520 W.'),
              ('Rewrite “the radio shall be fast” as a verifiable requirement.', 'For example: “The radio shall downlink at least 300 Mbit/s, verified by test.”'), ('Which side of the V holds verification?', 'The right side.')],
 'misc': [('Requirements describe the design.', 'They state what is needed, not how.'), ('Margin is waste.', 'It absorbs growth and surprises.'), ('Verification and validation are the same.', 'Verification: built right; validation: right thing built.')],
 'quiz': [_q('Landsat 9 margin…', ['85%', '74%', '40%', '185%'], 0, '(740 − 400)/400.'), _q('12 kg + 25%…', ['15 kg', '13 kg', '12.25 kg', '16 kg'], 0, 'Multiply.'),
          _q('Trade winner…', ['A', 'B', 'tie', 'neither'], 0, '7.7 > 6.9.'), _q('A good requirement is…', ['verifiable', 'vague', 'a design', 'optional'], 0, 'Testable.')],
 'cards': [('V-model', 'Decompose down, integrate and verify up.'), ('Requirement', 'Verifiable need.'), ('TPM', 'Tracked technical performance measure.'), ('PDR', 'Preliminary design review.'), ('Verification', 'Built right.'), ('Validation', 'Right thing built.')],
 'planet': {'text': ['NASA lists Landsat 9’s requirements, including at least 400 scenes a day and a 5-year design life; Landsat 9 collects 740 scenes a day, almost double the minimum, and carries enough fuel to operate for at least 10 years.',
                     'With Landsat 8, it observes the same place every 8 days, enabling near-weekly tropical deforestation alerts, water-quality monitoring and crop reports, payoffs of requirements written and met with margin.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Spacecraft Design', 'Spacecraft_Design.html')],
            'src': [_L9]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook, Sections 3–4.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u2', 'title': 'Architecture, Interfaces and Integration', 'weeks': 'Week 2',
 'summary': 'Functional and physical architecture, interface control, N² diagrams, model-based systems engineering and why interfaces grow fast.',
 'objectives': ['Map functions to components.', 'Count potential interfaces.', 'Read an N² diagram.', 'Explain model-based systems engineering.'],
 'concepts': ['A functional architecture says what the system does; a physical architecture says which boxes do it.',
              'Every pair of components could need an interface, so potential interfaces grow as n(n − 1)/2.',
              'An N² diagram puts components on the diagonal and the data or power between them off the diagonal.',
              'Interface control documents fix connectors, signals, timing and data formats so teams can build in parallel.',
              'NASA notes its handbook update includes Model-Based Systems Engineering, which keeps requirements, architecture and analyses in one connected model.'],
 'eqs': [('I=\\frac{n(n-1)}{2}', 'Potential two-way interfaces'), ('N_{cells}=n(n-1)', 'Off-diagonal N² cells'), ('B=\\sum_i r_i', 'Total bus load'), ('U=B/B_{max}', 'Bus utilization')],
 'worked': [
  _w('An avionics suite has 8 boxes. How many potential interfaces?', ['8 × 7/2.'], '28.'),
  _w('Add 4 boxes (n = 12).', ['12 × 11/2.'], '66, more than double.'),
  _w('Three boxes send 20, 35 and 15 kbit/s on a 100 kbit/s bus. Utilization?', ['70/100.'], '70%.')],
 'practice': [('Off-diagonal N² cells for n = 8?', '56.'), ('Interfaces for n = 4?', '6.'),
              ('Why keep bus utilization below 100%?', 'Room for growth, retries and timing jitter.'), ('What is an ICD?', 'Interface control document.')],
 'misc': [('Interfaces grow linearly.', 'They grow roughly as n².'), ('Architecture is just a parts list.', 'It includes functions and connections.'), ('MBSE replaces engineers.', 'It connects their work.')],
 'quiz': [_q('Interfaces for 8 boxes…', ['28', '56', '16', '64'], 0, 'n(n − 1)/2.'), _q('For 12 boxes…', ['66', '132', '24', '144'], 0, '12 × 11/2.'),
          _q('Bus utilization…', ['70%', '35%', '100%', '7%'], 0, '70/100.'), _q('MBSE means…', ['model-based systems engineering', 'mass budget', 'mission baseline', 'mean bus error'], 0, 'NASA.')],
 'cards': [('Architecture', 'Functions mapped to components.'), ('N² diagram', 'Interface matrix.'), ('ICD', 'Interface control document.'), ('MBSE', 'Model-based systems engineering.'), ('Integration', 'Joining components.'), ('Bus load', 'Sum of data rates.')],
 'planet': {'text': ['NASA says its Systems Engineering Handbook was updated to include Model-Based Systems Engineering, drawing on lessons from missions and mishaps.',
                     'Clear interfaces let instrument and spacecraft teams build in parallel, which is how Earth-observing missions such as Landsat 9 reach orbit on schedule.'],
            'site': [('Spacecraft Design', 'Spacecraft_Design.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_SEH]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook, Section 4.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u3', 'title': 'Reliability and Redundancy', 'weeks': 'Weeks 3–4',
 'summary': 'Failure rates, exponential reliability, MTBF, series and parallel systems, triple modular redundancy, k-of-n systems and availability.',
 'objectives': ['Compute reliability from a failure rate.', 'Combine series and parallel blocks.', 'Compute 2-of-3 voting reliability.', 'Compute availability.'],
 'concepts': ['With a constant failure rate λ, reliability falls as e^(−λt) and the mean time between failures is 1/λ.',
              'Series systems fail if any part fails, so reliabilities multiply.',
              'Parallel (redundant) systems fail only if all parts fail.',
              'Triple modular redundancy votes 2 of 3; it beats a single unit early in life but not after R drops below 0.5.',
              'Availability is the fraction of time a system works: MTBF/(MTBF + MTTR).'],
 'eqs': [('R(t)=e^{-\\lambda t}', 'Exponential reliability'), ('R_s=\\prod R_i,\\ R_p=1-\\prod(1-R_i)', 'Series and parallel'), ('R_{2/3}=3R^2-2R^3', 'Two-of-three voting'), ('A=\\frac{MTBF}{MTBF+MTTR}', 'Availability')],
 'worked': [
  _w('A unit has λ = 10⁻⁵ per hour. Reliability over 10,000 h?', ['e^(−0.1).'], '0.905.'),
  _w('Two such units in parallel?', ['1 − (1 − 0.9048)².'], '0.991.'),
  _w('Three units voting 2 of 3?', ['3(0.9048)² − 2(0.9048)³.'], '0.975.')],
 'practice': [('MTBF for λ = 10⁻⁵ /h?', '100,000 h.'), ('Single, dual and TMR at 50,000 h?', '0.607, 0.845, 0.657.'),
              ('Availability with MTBF 1000 h and MTTR 2 h?', '0.998.'), ('Hubble needs one of three working gyros. Which model?', '1-of-3 (parallel).')],
 'misc': [('Redundancy always helps.', 'TMR loses to a single unit once R < 0.5.'), ('MTBF is guaranteed life.', 'It is a mean; many fail sooner.'), ('Series reliability adds.', 'It multiplies.')],
 'quiz': [_q('R(10,000 h)…', ['0.905', '0.990', '0.1', '0.5'], 0, 'e^(−0.1).'), _q('Parallel pair…', ['0.991', '0.819', '0.905', '1'], 0, '1 − 0.0952².'),
          _q('TMR…', ['0.975', '0.905', '0.991', '0.857'], 0, '3R² − 2R³.'), _q('MTBF…', ['100,000 h', '10,000 h', '1000 h', '10⁻⁵ h'], 0, '1/λ.')],
 'cards': [('Failure rate', 'Failures per hour.'), ('MTBF', 'Mean time between failures.'), ('Redundancy', 'Backup units.'), ('TMR', 'Triple modular redundancy, 2-of-3 voting.'), ('Availability', 'Fraction of time working.'), ('k-of-n', 'Works if k of n work.')],
 'planet': {'text': ['NASA says Hubble received six new gyroscopes in 2009, three remained operational, and when one returned faulty readings NASA moved Hubble to one-gyro mode while keeping another in reserve.',
                     'Launched in 1990, Hubble has more than doubled its expected design lifetime; redundancy planned decades earlier keeps a working observatory in orbit instead of a replacement.'],
            'site': [('Flight Dynamics & Controls', 'Flight_Dynamics_Controls.html'), ('Spacecraft Design', 'Spacecraft_Design.html')],
            'src': [_HUB]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook.'), (_HUB[0], _HUB[1], 'NASA Hubble gyro story.')]})
UNITS.append(
{'id': 'u4', 'title': 'Safety Analysis: FMEA and Fault Trees', 'weeks': 'Week 5',
 'summary': 'Hazards, failure modes and effects analysis, risk priority numbers, fault trees with AND and OR gates, and safety-critical design.',
 'objectives': ['Run a simple FMEA.', 'Compute a risk priority number.', 'Evaluate AND and OR gates.', 'Choose mitigations.'],
 'concepts': ['FMEA works bottom-up: for each part, list how it can fail, the effect, and how it will be detected.',
              'A risk priority number multiplies severity, occurrence and detection scores (each 1–10, textbook scale).',
              'A fault tree works top-down from an unwanted event; OR gates add risk, AND gates (redundancy) shrink it.',
              'For small independent probabilities, an OR gate is nearly the sum and an AND gate is the product.',
              'Lessons from accidents shape practice; NASA notes its handbook drew on the Columbia Accident Investigation Board and other reports.'],
 'eqs': [('RPN=S\\times O\\times D', 'Risk priority number'), ('P_{OR}=1-\\prod(1-p_i)', 'OR gate'), ('P_{AND}=\\prod p_i', 'AND gate'), ('P_{OR}\\approx\\sum p_i', 'Rare-event approximation')],
 'worked': [
  _w('A sensor failure scores S = 8, O = 4, D = 5. RPN?', ['8 × 4 × 5.'], '160.'),
  _w('Either of two faults (p = 10⁻³ and 2 × 10⁻³) causes loss of data. Probability?', ['1 − (0.999)(0.998).'], '2.998 × 10⁻³.'),
  _w('Loss needs both faults (redundant design).', ['10⁻³ × 2 × 10⁻³.'], '2 × 10⁻⁶.')],
 'practice': [('Better detection drops D to 2. New RPN?', '64.'), ('Rare-event approximation for the OR gate?', '3 × 10⁻³.'),
              ('Which gate does redundancy create?', 'AND.'), ('Top-down or bottom-up: fault tree?', 'Top-down.')],
 'misc': [('RPN is a probability.', 'It is a ranking score.'), ('OR gates multiply.', 'AND gates multiply.'), ('Redundant parts fail independently.', 'Common causes can fail both.')],
 'quiz': [_q('RPN…', ['160', '17', '40', '320'], 0, '8 × 4 × 5.'), _q('OR gate…', ['≈ 3 × 10⁻³', '2 × 10⁻⁶', '10⁻³', '0.5'], 0, '1 − ∏(1 − p).'),
          _q('AND gate…', ['2 × 10⁻⁶', '3 × 10⁻³', '10⁻³', '2 × 10⁻³'], 0, 'Product.'), _q('FMEA works…', ['bottom-up', 'top-down', 'sideways', 'randomly'], 0, 'Part by part.')],
 'cards': [('FMEA', 'Failure modes and effects analysis.'), ('RPN', 'Severity × occurrence × detection.'), ('Fault tree', 'Top-down logic of failure.'), ('OR gate', 'Any input causes the event.'), ('AND gate', 'All inputs needed.'), ('Common cause', 'One event failing several parts.')],
 'planet': {'text': ['NASA says lessons documented by the Columbia Accident Investigation Board, the NASA Integrated Action Team and others, plus mishaps in ground operations and commercial spaceflight, shaped its systems engineering handbook.',
                     'The same safety tools protect the satellites that track wildfires, storms and sea ice. Probabilities in this unit are sample values.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_SEH]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook, Section 6.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u5', 'title': 'Digital Avionics and Data Buses', 'weeks': 'Weeks 6–7',
 'summary': 'Binary data, analog-to-digital conversion, quantization, serial data buses (ARINC 429, MIL-STD-1553), message timing and data volume.',
 'objectives': ['Compute ADC resolution and SNR.', 'Compute message transmission time.', 'Compare bus types.', 'Estimate data volume.'],
 'concepts': ['An N-bit converter divides its input range into 2ᴺ levels; one step is the least significant bit.',
              'Ideal quantization SNR is about 6.02N + 1.76 dB.',
              'ARINC 429 is a one-transmitter, many-receiver bus at 100 kbit/s high speed (textbook value); MIL-STD-1553 is a command/response bus at 1 Mbit/s (textbook value).',
              'Message time is bits divided by bit rate; overhead and gaps add to it.',
              'Higher radiometric resolution (more bits) shows finer differences but makes more data.'],
 'eqs': [('\\Delta V=\\frac{V_{FS}}{2^N}', 'ADC step'), ('SNR\\approx6.02N+1.76\\ \\text{dB}', 'Quantization SNR'), ('t=\\frac{bits}{R_b}', 'Transmission time'), ('L=2^N', 'Number of levels')],
 'worked': [
  _w('A 12-bit ADC spans 10 V. Step size?', ['10/4096.'], '2.44 mV.'),
  _w('Its ideal SNR?', ['6.02 × 12 + 1.76.'], '74.0 dB.'),
  _w('A 32-bit ARINC 429 word at 100 kbit/s takes how long?', ['32/100,000.'], '0.32 ms.')],
 'practice': [('Landsat 9 has 14-bit radiometric resolution. Levels?', '16,384.'), ('SNR for 8 bits?', '49.9 dB.'),
              ('Same 32-bit word on a 1 Mbit/s bus?', '0.032 ms.'), ('Step for 16 bits over 10 V?', '0.153 mV.')],
 'misc': [('More bits means more accuracy automatically.', 'Noise and calibration also limit it.'), ('Bit rate equals data rate of useful data.', 'Overhead takes a share.'), ('One bus fits all.', 'Pick by timing, integrity and cost.')],
 'quiz': [_q('12-bit step over 10 V…', ['2.44 mV', '24.4 mV', '0.244 mV', '10 mV'], 0, '10/4096.'), _q('12-bit SNR…', ['74.0 dB', '72 dB', '49.9 dB', '98 dB'], 0, '6.02N + 1.76.'),
          _q('ARINC word time…', ['0.32 ms', '3.2 ms', '32 ms', '0.032 ms'], 0, '32/10⁵.'), _q('14-bit levels…', ['16,384', '4096', '65,536', '14'], 0, '2¹⁴.')],
 'cards': [('ADC', 'Analog-to-digital converter.'), ('LSB', 'Least significant bit step.'), ('ARINC 429', 'One-way avionics bus.'), ('MIL-STD-1553', 'Command/response bus.'), ('Quantization', 'Rounding to levels.'), ('Bit rate', 'Bits per second.')],
 'planet': {'text': ['NASA lists Landsat 9 with 14-bit radiometric resolution, 11 spectral bands and more than 700 scenes a day, each 185 km by 180 km.',
                     'Fine radiometric steps let scientists see subtle changes in water quality and vegetation health, at the cost of more data for the avionics to store and send.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Circuits', 'Circuits.html')],
            'src': [_L9]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_SEH[0], _SEH[1], 'Free NASA handbook.')]})
UNITS.append(
{'id': 'u6', 'title': 'Navigation Sensors: IMUs, GNSS, Cameras and Lidar', 'weeks': 'Week 8',
 'summary': 'Gyros and accelerometers, inertial navigation drift, satellite navigation ranging, and vision and lidar sensors for autonomy.',
 'objectives': ['Compute drift from an accelerometer bias.', 'Relate timing error to range error.', 'Compare sensor strengths.', 'Explain why sensors are combined.'],
 'concepts': ['An inertial measurement unit (IMU) measures rotation rates (gyros) and specific force (accelerometers).',
              'Integrating twice turns a small accelerometer bias into a position error that grows with t².',
              'Satellite navigation measures range from signal travel time; 1 µs of clock error is about 300 m of range.',
              'Cameras and lidar measure the surroundings directly, giving position and hazard information that does not drift.',
              'No single sensor is enough: IMUs are fast but drift; external sensors are slower but bounded.'],
 'eqs': [('e=\\tfrac12bt^2', 'Position error from accelerometer bias'), ('\\rho=c\\,\\Delta t', 'Range from travel time'), ('\\theta_e=\\omega_bt', 'Heading error from gyro bias'), ('b=10^{-3}g', 'Sample bias of 1 milli-g')],
 'worked': [
  _w('An accelerometer bias of 1 milli-g (9.807 × 10⁻³ m/s²) runs uncorrected for 60 s. Position error?', ['½ × 9.807 × 10⁻³ × 60².'], '17.7 m.'),
  _w('After 600 s?', ['½ × 9.807 × 10⁻³ × 600².'], '1765 m, 100 times worse for 10 times the time.'),
  _w('A receiver clock is off by 1 µs. Range error?', ['299,792,458 × 10⁻⁶.'], '300 m.')],
 'practice': [('Error after 10 s with the same bias?', '0.49 m.'), ('Gyro bias 0.01°/h for 10 h?', '0.1° of heading.'),
              ('Why does Dragonfly need lidar at Titan?', 'To measure terrain altitude and slope and spot hazards.'), ('Clock error for 3 m of range?', '10 ns.')],
 'misc': [('IMUs never need correction.', 'Their errors grow with time.'), ('GNSS works everywhere.', 'Not indoors, underwater or at Titan.'), ('Drift grows linearly.', 'Bias drift grows with t².')],
 'quiz': [_q('Error at 60 s…', ['17.7 m', '0.59 m', '1765 m', '35 m'], 0, '½bt².'), _q('Error at 600 s…', ['1765 m', '177 m', '17.7 km', '600 m'], 0, '100×.'),
          _q('1 µs clock error…', ['300 m', '3 m', '30 km', '0.3 m'], 0, 'c Δt.'), _q('Sensor that drifts…', ['IMU', 'lidar', 'camera map match', 'GNSS'], 0, 'Integration.')],
 'cards': [('IMU', 'Gyros and accelerometers.'), ('Dead reckoning', 'Navigation by integration.'), ('GNSS', 'Satellite navigation.'), ('Lidar', 'Laser ranging.'), ('Bias', 'Constant sensor offset.'), ('Pseudorange', 'Range including clock error.')],
 'planet': {'text': ['NASA says Dragonfly’s recent “first flight” test ran flight software and flight-like avionics with simulated data from its navigation cameras, inertial measurement units and lidar.',
                     'Lidar measures terrain altitude and slope and identifies hazards, letting the rotorcraft choose a safe landing site on Titan, where it is due to arrive in 2034.'],
            'site': [('Flight Dynamics & Controls', 'Flight_Dynamics_Controls.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_DF]},
 'res': [(_DF[0], _DF[1], 'NASA Dragonfly story.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u7', 'title': 'Sensor Fusion and the Kalman Filter', 'weeks': 'Week 9',
 'summary': 'Combining noisy measurements, inverse-variance weighting, the scalar Kalman filter and its predict-update cycle.',
 'objectives': ['Fuse two measurements by variance.', 'Compute a Kalman gain.', 'Run one predict-update step.', 'Explain why fusion beats either sensor.'],
 'concepts': ['Two independent estimates are best combined by weighting each by the inverse of its variance.',
              'The fused variance is smaller than either input variance.',
              'The Kalman filter predicts the state forward, then corrects it with a measurement using gain K.',
              'K = P/(P + R): trust the measurement more when the prediction is uncertain (large P) and the sensor is good (small R).',
              'Navigation systems fuse fast IMU predictions with slower camera, lidar or GNSS updates.'],
 'eqs': [('\\sigma^2=\\frac{\\sigma_1^2\\sigma_2^2}{\\sigma_1^2+\\sigma_2^2}', 'Fused variance'), ('K=\\frac{P}{P+R}', 'Scalar Kalman gain'), ('\\hat x^+=\\hat x^-+K(z-\\hat x^-)', 'Update'), ('P^+=(1-K)P', 'Updated variance')],
 'worked': [
  _w('Sensors with σ = 4 m and 3 m are fused. Fused σ?', ['σ² = 16 × 9/25 = 5.76.', 'σ = √5.76.'], '2.4 m.'),
  _w('Prediction variance P = 16 m², measurement R = 9 m². Gain?', ['16/25.'], '0.64.'),
  _w('Prediction 100 m, measurement 105 m. Update and new variance?', ['x = 100 + 0.64 × 5 = 103.2 m.', 'P = 0.36 × 16.'], '103.2 m with variance 5.76 m².')],
 'practice': [('Fuse two equal sensors of σ = 2 m.', 'σ = 1.41 m.'), ('Gain if R = 0?', '1: trust the measurement fully.'),
              ('Gain if R is huge?', 'Near 0: keep the prediction.'), ('What grows P between updates?', 'Process noise in the prediction.')],
 'misc': [('Average sensors equally.', 'Weight by inverse variance.'), ('Fusion can’t beat the best sensor.', 'It beats both.'), ('Kalman filters remove all error.', 'They minimize variance under assumptions.')],
 'quiz': [_q('Fused σ…', ['2.4 m', '3.5 m', '1 m', '5 m'], 0, '√5.76.'), _q('Kalman gain…', ['0.64', '0.36', '1.78', '0.5'], 0, 'P/(P + R).'),
          _q('Updated estimate…', ['103.2 m', '105 m', '100 m', '102.5 m'], 0, '100 + 0.64 × 5.'), _q('New variance…', ['5.76 m²', '16 m²', '9 m²', '25 m²'], 0, '(1 − K)P.')],
 'cards': [('Sensor fusion', 'Combining measurements.'), ('Kalman gain', 'Weight on the measurement.'), ('Covariance', 'Uncertainty of the estimate.'), ('Predict', 'Propagate the state.'), ('Update', 'Correct with a measurement.'), ('Innovation', 'Measurement minus prediction.')],
 'planet': {'text': ['NASA reports that Dragonfly’s team added sensors and capabilities step by step, ending with lidar, the final piece needed to fully simulate what the rotorcraft will encounter on Titan.',
                     'A camera emulator rendered each simulated Titan scene in roughly the 20 to 70 millisecond exposure times the cameras will use, so fusion software saw realistic timing. Variances in this unit are sample values.'],
            'site': [('Flight Dynamics & Controls', 'Flight_Dynamics_Controls.html'), ('Spacecraft Design', 'Spacecraft_Design.html')],
            'src': [_DF]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_DF[0], _DF[1], 'NASA Dragonfly story.')]})
UNITS.append(
{'id': 'u8', 'title': 'Communication and Surveillance: ADS-B', 'weeks': 'Week 10',
 'summary': 'Aircraft radios, line-of-sight range, free-space path loss, ADS-B Out and In, and how surveillance supports air traffic control.',
 'objectives': ['Compute radio horizon range.', 'Compute free-space path loss.', 'Explain ADS-B Out and In.', 'Put FAA traffic numbers in scale.'],
 'concepts': ['VHF and higher frequencies travel by line of sight, so range depends on antenna heights.',
              'Free-space path loss grows with distance and frequency, 20 log₁₀(4πd/λ).',
              'With ADS-B Out, an aircraft broadcasts its satellite-derived position; ADS-B In lets other aircraft and the ground receive it.',
              'The FAA calls real-time ADS-B the preferred method of surveillance for air traffic control in the National Airspace System.',
              'In the U.S., aircraft must carry ADS-B Out to fly in the airspace defined in 14 CFR 91.225.'],
 'eqs': [('d\\approx4.12(\\sqrt{h_1}+\\sqrt{h_2})\\ \\text{km}', 'Radio horizon (h in m)'), ('L=20\\log_{10}\\frac{4\\pi d}{\\lambda}', 'Free-space path loss'), ('\\lambda=c/f', 'Wavelength'), ('\\bar n=N/24', 'Average flights per hour')],
 'worked': [
  _w('An aircraft at 10,000 m and a ground antenna at 10 m. Radio horizon?', ['4.12(100 + 3.162).'], '425 km.'),
  _w('Path loss at 1090 MHz over 200 km.', ['λ = 0.2750 m.', '20 log₁₀(4π × 2 × 10⁵/0.2750).'], '139.2 dB.'),
  _w('The FAA serves more than 44,000 flights a day. Average per hour?', ['44,000/24.'], 'About 1833.')],
 'practice': [('Double the distance: added path loss?', '6.02 dB.'), ('Wavelength at 1090 MHz?', '0.275 m.'),
              ('Passengers per flight from 3 million and 44,000?', 'About 68.'), ('What does ADS-B Out require on board?', 'A transmitter broadcasting position.')],
 'misc': [('Radio range is unlimited.', 'Line of sight limits it.'), ('ADS-B uses radar.', 'Aircraft broadcast their own position.'), ('Path loss is linear in distance.', 'It grows as 20 log₁₀ d.')],
 'quiz': [_q('Radio horizon…', ['425 km', '42.5 km', '4250 km', '100 km'], 0, '4.12 × 103.2.'), _q('Path loss…', ['139.2 dB', '119 dB', '160 dB', '13.9 dB'], 0, '20 log₁₀(4πd/λ).'),
          _q('Flights per hour…', ['≈ 1833', '≈ 440', '≈ 44,000', '≈ 183'], 0, '44,000/24.'), _q('ADS-B Out does…', ['broadcast position', 'jam radar', 'track weather only', 'land the plane'], 0, 'FAA.')],
 'cards': [('ADS-B', 'Automatic dependent surveillance-broadcast.'), ('ADS-B Out', 'Broadcasts own position.'), ('ADS-B In', 'Receives traffic and weather.'), ('Path loss', 'Signal spreading loss.'), ('Radio horizon', 'Line-of-sight limit.'), ('NAS', 'National Airspace System.')],
 'planet': {'text': ['The FAA says ADS-B improves safety and efficiency in the air and on runways, reduces costs, and lessens harmful effects on the environment.',
                     'The FAA’s Air Traffic Organization serves more than 44,000 flights and more than 3 million airline passengers a day across more than 29 million square miles of airspace (FY24 figures), so small efficiency gains add up.'],
            'site': [('Aircraft Performance', 'Aircraft_Performance.html'), ('Solutions', 'Solutions.html')],
            'src': [_ADSB, _ATO]},
 'res': [(_ADSB[0], _ADSB[1], 'FAA overview.'), (_ATO[0], _ATO[1], 'FAA facts.')]})
UNITS.append(
{'id': 'u9', 'title': 'Real-Time Flight Software', 'weeks': 'Weeks 11–12',
 'summary': 'Tasks, periods and deadlines, CPU utilization, rate-monotonic scheduling, frame rates, watchdogs and fault protection.',
 'objectives': ['Compute CPU utilization.', 'Apply the rate-monotonic bound.', 'Relate frame rate and period.', 'Describe fault protection.'],
 'concepts': ['Flight software runs periodic tasks that must finish before their deadlines, not just quickly on average.',
              'Utilization is the sum of each task’s run time divided by its period.',
              'Rate-monotonic scheduling gives higher priority to shorter periods; it is guaranteed when U ≤ n(2^(1/n) − 1).',
              'Watchdog timers reset a processor that stops responding; fault protection puts a spacecraft in a safe mode.',
              'Autonomy matters when ground help is far away; NASA says Dragonfly must fly without real-time help from Earth.'],
 'eqs': [('U=\\sum\\frac{C_i}{T_i}', 'Utilization'), ('U\\le n(2^{1/n}-1)', 'Rate-monotonic bound'), ('f=1/T', 'Frame rate'), ('\\text{slack}=1-U', 'Spare capacity')],
 'worked': [
  _w('Tasks take 2, 3 and 5 ms with periods 10, 20 and 50 ms. Utilization?', ['0.2 + 0.15 + 0.1.'], '0.45.'),
  _w('Rate-monotonic bound for three tasks?', ['3(2^(1/3) − 1).'], '0.780, so 0.45 is guaranteed schedulable.'),
  _w('Dragonfly’s camera exposures run about 20 to 70 ms. Matching frame rates?', ['1/0.07 and 1/0.02.'], 'About 14.3 to 50 Hz.')],
 'practice': [('Bound for n = 2?', '0.828.'), ('Bound for n = 4?', '0.757.'),
              ('Slack with U = 0.45?', '0.55.'), ('Why safe mode?', 'To keep the vehicle stable and wait for help or a fix.')],
 'misc': [('Fast on average is enough.', 'Every deadline matters.'), ('U ≤ 1 always means schedulable under RMS.', 'Only the bound guarantees it.'), ('Safe mode means failure.', 'It protects the mission.')],
 'quiz': [_q('Utilization…', ['0.45', '0.10', '1.0', '0.78'], 0, 'Sum C/T.'), _q('RM bound n = 3…', ['0.780', '0.693', '0.828', '1'], 0, 'n(2^(1/n) − 1).'),
          _q('70 ms frame…', ['14.3 Hz', '70 Hz', '7 Hz', '50 Hz'], 0, '1/0.07.'), _q('Watchdog does…', ['resets a hung processor', 'counts bits', 'measures gyros', 'cools boxes'], 0, 'Timer.')],
 'cards': [('Deadline', 'Latest finish time.'), ('Utilization', 'CPU fraction used.'), ('Rate-monotonic', 'Shorter period, higher priority.'), ('Watchdog', 'Reset timer.'), ('Safe mode', 'Protective configuration.'), ('Autonomy', 'Acting without ground help.')],
 'planet': {'text': ['NASA reports Hubble entered safe mode several times when a gyro gave faulty readings, suspending science while the telescope awaited instructions; fault protection kept it safe.',
                     'NASA says Dragonfly engineers will deliberately introduce faults in tests so the rotorcraft can respond autonomously, because everything it does on Titan must happen without real-time help from Earth.'],
            'site': [('Intro to Programming', 'Intro_to_Programming.html'), ('Flight Dynamics & Controls', 'Flight_Dynamics_Controls.html')],
            'src': [_HUB, _DF]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_DF[0], _DF[1], 'NASA Dragonfly story.')]})
UNITS.append(
{'id': 'u10', 'title': 'Integration, Verification and Operations', 'weeks': 'Weeks 13–15',
 'summary': 'Incremental integration, verification methods, hardware-in-the-loop testing, fault injection, commissioning and life extension.',
 'objectives': ['Name the four verification methods.', 'Plan incremental integration.', 'Explain hardware-in-the-loop testing.', 'Connect operations to mission life.'],
 'concepts': ['Requirements are verified by test, analysis, inspection or demonstration.',
              'Integration goes step by step so a problem can be traced to the last thing added.',
              'Hardware-in-the-loop and flight-like testbeds run real flight software against simulated sensors.',
              'Fault-injection tests prove the system responds correctly when something breaks.',
              'Good operations, spares and consumables can stretch a mission well past its design life.'],
 'eqs': [('t_{arr}=t_{launch}+t_{cruise}', 'Arrival year'), ('L_{ext}=\\frac{L_{actual}}{L_{design}}', 'Life extension ratio'), ('A=\\frac{MTBF}{MTBF+MTTR}', 'Availability'), ('V=\\{T,A,I,D\\}', 'Verification methods')],
 'worked': [
  _w('NASA says Dragonfly launches no earlier than 2028 on a six-year voyage. Earliest arrival?', ['2028 + 6.'], '2034, matching NASA.'),
  _w('Landsat 9 consumables last at least 10 years against a 5-year design life. Extension ratio?', ['10/5.'], '2.'),
  _w('Dragonfly will spend three years flying at Titan. Mission end at the earliest?', ['2034 + 3.'], '2037 (computed).')],
 'practice': [('Name the four verification methods.', 'Test, analysis, inspection, demonstration.'), ('Why integrate incrementally?', 'To trace problems to the last change.'),
              ('Hubble launched in 1990; its 34th anniversary was in which year?', '2024.'), ('What is fault injection?', 'Deliberately causing faults in test.')],
 'misc': [('Test everything at the end.', 'Integrate and test in steps.'), ('Analysis is weaker than test.', 'Each method fits different requirements.'), ('Design life is the end.', 'Missions often run longer.')],
 'quiz': [_q('Dragonfly arrival…', ['2034', '2028', '2030', '2040'], 0, '2028 + 6.'), _q('Landsat 9 ratio…', ['2', '0.5', '5', '10'], 0, '10/5.'),
          _q('Methods count…', ['4', '2', '3', '6'], 0, 'T, A, I, D.'), _q('Testbed with real software…', ['hardware-in-the-loop', 'FMEA', 'N² diagram', 'trade study'], 0, 'HIL.')],
 'cards': [('Verification by test', 'Measure it.'), ('Analysis', 'Prove by calculation.'), ('Inspection', 'Look at it.'), ('Demonstration', 'Show it works.'), ('HIL', 'Hardware-in-the-loop.'), ('Commissioning', 'Checkout after launch.')],
 'planet': {'text': ['NASA says Dragonfly’s team built flight capabilities incrementally, from spinning a single rotor to a full simulated first flight, and plans to repeat it on the actual flight system.',
                     'NASA notes Landsat 9’s onboard calibration and redundancy keep its data accurate and reliable for the mission’s life, extending the longest record of Earth observation.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Spacecraft Design', 'Spacecraft_Design.html')],
            'src': [_DF, _L9]},
 'res': [(_SEH[0], _SEH[1], 'Free NASA handbook, Section 5.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Interface growth and an N² diagram', 'week': 'Week 2',
 'goal': 'Build an N² diagram for a small avionics suite and see how potential interfaces grow with the number of boxes.',
 'eq': ('I=n(n-1)/2', 'Potential interfaces'),
 'steps': ['List boxes: flight computer, IMU, GNSS receiver, radio, display, power unit, air data, autopilot.', 'Draw an 8 × 8 grid with boxes on the diagonal and mark which pairs exchange data.', 'Compute n(n − 1)/2 for n = 4, 8 and 12.', 'Count your marked cells and compare with the maximum.'],
 'table': (['Boxes n', 'Potential interfaces'], [['4', '6'], ['8', '28'], ['12', '66']]),
 'note': 'Computed values.',
 'calc': ['8 × 7/2 = 28.', '12 × 11/2 = 66.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_SEH[0], _SEH[1])],
 'planet': 'NASA: its handbook update includes Model-Based Systems Engineering.', 'planet_src': [_SEH]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Reliability of single, dual and triple units', 'week': 'Week 4',
 'goal': 'Compare a single unit, a parallel pair and 2-of-3 voting over time in a spreadsheet.',
 'eq': ('R_{2/3}=3R^2-2R^3', 'Two-of-three voting'),
 'steps': ['Enter λ = 10⁻⁵ per hour.', 'Compute R = e^(−λt) for t = 1000, 10,000 and 50,000 h.', 'Compute the parallel pair and 2-of-3 voting.', 'Find where 2-of-3 drops below a single unit (R = 0.5).'],
 'table': (['t (h)', 'Single', 'Dual', '2-of-3'], [['1000', '0.990', '0.9999', '0.9997'], ['10,000', '0.905', '0.991', '0.975'], ['50,000', '0.607', '0.845', '0.657']]),
 'note': 'Computed sample values.',
 'calc': ['R(50,000) = e^(−0.5) = 0.607.', '2-of-3 = 3(0.607)² − 2(0.607)³ = 0.657.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_SEH[0], _SEH[1])],
 'planet': 'NASA: Hubble can make science observations with only one working gyro.', 'planet_src': [_HUB]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Redundant circuits', 'week': 'Week 5',
 'goal': 'Use PhET Circuit Construction Kit: DC to compare series and parallel bulbs when one fails.',
 'eq': ('R_p=\\frac{R_1R_2}{R_1+R_2}', 'Parallel resistance'),
 'steps': ['Build two 10 Ω bulbs in series on a 12 V battery, then break one wire.', 'Rebuild them in parallel and break one branch.', 'Measure current before and after each failure.', 'Relate the result to series and parallel reliability.'],
 'table': (['Circuit', 'Resistance (Ω)', 'Current at 12 V (A)'], [['Parallel, both good', '5', '2.4'], ['Parallel, one failed', '10', '1.2'], ['Series, both good', '20', '0.6']]),
 'note': 'Computed sample values.',
 'calc': ['10 × 10/20 = 5 Ω.', '12/5 = 2.4 A.'],
 'safety': ['Computer only.'], 'home': ['Runs in a browser.'],
 'sims': [(_CCK[0], _CCK[1])],
 'planet': 'NASA: Landsat 9’s onboard redundancy keeps its data reliable.', 'planet_src': [_L9]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: ADC resolution and data volume', 'week': 'Week 7',
 'goal': 'Compute step size and SNR for several converter resolutions.',
 'eq': ('\\Delta V=V_{FS}/2^N', 'ADC step'),
 'steps': ['Enter a 10 V full scale.', 'Compute step and SNR for 8, 12 and 16 bits.', 'Compute word time for 32 bits at 100 kbit/s and 1 Mbit/s.', 'Discuss why Landsat 9 uses 14 bits.'],
 'table': (['Bits', 'Step (mV)', 'SNR (dB)'], [['8', '39.06', '49.9'], ['12', '2.441', '74.0'], ['16', '0.1526', '98.1']]),
 'note': 'Computed values.',
 'calc': ['10/256 = 39.06 mV.', '6.02 × 16 + 1.76 = 98.1 dB.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_L9[0], _L9[1])],
 'planet': 'NASA: Landsat 9 has 14-bit radiometric resolution.', 'planet_src': [_L9]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Inertial drift and sensor fusion', 'week': 'Week 9',
 'goal': 'Model position drift from an accelerometer bias, then fuse two position sensors.',
 'eq': ('e=\\tfrac12bt^2', 'Bias drift'),
 'steps': ['Enter b = 9.807 × 10⁻³ m/s² (1 milli-g).', 'Compute error at 10, 60 and 600 s.', 'Fuse σ = 4 m and 3 m sensors and compute the Kalman gain for P = 16, R = 9.', 'Add noise with a random-number column and watch the filter.'],
 'table': (['t (s)', 'Error (m)'], [['10', '0.49'], ['60', '17.65'], ['600', '1765']]),
 'note': 'Computed sample values.',
 'calc': ['½ × 9.807 × 10⁻³ × 100 = 0.49 m.', 'Fused σ = √5.76 = 2.4 m.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_DF[0], _DF[1])],
 'planet': 'NASA: Dragonfly’s test used simulated camera, IMU and lidar data.', 'planet_src': [_DF]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Rate-monotonic schedulability', 'week': 'Week 12',
 'goal': 'Compute utilization bounds and test task sets in a spreadsheet.',
 'eq': ('U\\le n(2^{1/n}-1)', 'Rate-monotonic bound'),
 'steps': ['Compute the bound for n = 1 to 4.', 'Enter Unit 9’s task set and compute U.', 'Add a task until U exceeds the bound.', 'Discuss what to do when the bound fails.'],
 'table': (['n', 'Bound'], [['1', '1.000'], ['2', '0.828'], ['3', '0.780'], ['4', '0.757']]),
 'note': 'Computed values.',
 'calc': ['2(√2 − 1) = 0.828.', '4(2^(1/4) − 1) = 0.757.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MIT[0], _MIT[1])],
 'planet': 'NASA: Dragonfly must fly autonomously, without real-time help from Earth.', 'planet_src': [_DF]})
SCHEDULE = [(1, 'u1', 'Life cycle and requirements', 'NASA SE Handbook'), (2, 'u2', 'Architecture and interfaces; Lab A', 'MIT 16.842'),
            (3, 'u3', 'Reliability models', 'NASA SE Handbook'), (4, 'u3', 'Redundancy; Lab B', 'NASA Hubble'),
            (5, 'u4', 'FMEA and fault trees; Lab C', 'NASA SE Handbook'), (6, 'u5', 'Digital avionics', 'MIT 16.842'),
            (7, 'u5', 'Data buses; Lab D; midterm practice', 'NASA Landsat 9'), (8, 'u6', 'Navigation sensors', 'NASA Dragonfly'),
            (9, 'u7', 'Sensor fusion and Kalman filters; Lab E', 'MIT 16.842'), (10, 'u8', 'Communication and ADS-B', 'FAA ADS-B'),
            (11, 'u9', 'Real-time software', 'MIT 16.842'), (12, 'u9', 'Fault protection; Lab F', 'NASA Hubble'),
            (13, 'u10', 'Integration and verification', 'NASA SE Handbook'), (14, 'u10', 'Testbeds and fault injection', 'NASA Dragonfly'), (15, 'u10', 'Review; final practice', 'MIT 16.842')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Potential interfaces for 10 boxes?', ['10 × 9/2.'], '45.'),
  ('Parallel pair, λ = 2 × 10⁻⁵ /h over 5000 h?', ['R = e^(−0.1) = 0.905.', '1 − 0.095².'], '0.991.'),
  ('RPN for S = 6, O = 3, D = 7?', ['6 × 3 × 7.'], '126.'),
  ('Step of a 10-bit ADC over 5 V?', ['5/1024.'], '4.88 mV.'),
  ('Ideal SNR for 10 bits?', ['6.02 × 10 + 1.76.'], '62.0 dB.')]),
 ('Final practice set (Units 1–10)', [
  ('Drift after 30 s with a 2 milli-g bias?', ['½ × 0.01961 × 900.'], '8.83 m.'),
  ('Fuse two sensors of σ = 5 m.', ['σ² = 12.5.'], '3.54 m.'),
  ('Kalman gain for P = 4, R = 1?', ['4/5.'], '0.8.'),
  ('Radio horizon from 1000 m to a 10 m antenna?', ['4.12(31.62 + 3.162).'], '143.3 km.'),
  ('Utilization for tasks 1/5, 2/10, 3/30 ms?', ['0.2 + 0.2 + 0.1.'], '0.5.'),
  ('Availability, MTBF 500 h, MTTR 5 h?', ['500/505.'], '0.990.')])]
FORMULAS = ['\\text{Margin}=(C-N)/N,\\ m_{alloc}=m_{est}(1+M)', 'I=n(n-1)/2,\\ U_{bus}=B/B_{max}', 'R=e^{-\\lambda t},\\ R_p=1-\\prod(1-R_i),\\ R_{2/3}=3R^2-2R^3',
            'RPN=SOD,\\ P_{OR}=1-\\prod(1-p_i),\\ P_{AND}=\\prod p_i', '\\Delta V=V_{FS}/2^N,\\ SNR=6.02N+1.76', 'e=\\tfrac12bt^2,\\ \\rho=c\\Delta t',
            '\\sigma^2=\\sigma_1^2\\sigma_2^2/(\\sigma_1^2+\\sigma_2^2),\\ K=P/(P+R)', 'd=4.12(\\sqrt{h_1}+\\sqrt{h_2}),\\ L=20\\log_{10}(4\\pi d/\\lambda)',
            'U=\\sum C_i/T_i\\le n(2^{1/n}-1)', 'A=MTBF/(MTBF+MTTR)']
GLOSSARY = sorted([('ADS-B', 'Automatic dependent surveillance-broadcast.'), ('ARINC 429', 'One-way avionics data bus.'), ('Availability', 'Fraction of time a system works.'), ('Fault tree', 'Top-down failure logic.'),
    ('FMEA', 'Failure modes and effects analysis.'), ('Hardware-in-the-loop', 'Real software and hardware with simulated inputs.'), ('IMU', 'Inertial measurement unit.'), ('Interface control document', 'Agreement on an interface.'),
    ('Kalman filter', 'Optimal recursive estimator.'), ('Lidar', 'Laser ranging.'), ('MBSE', 'Model-based systems engineering.'), ('MIL-STD-1553', 'Command/response data bus.'),
    ('MTBF', 'Mean time between failures.'), ('N² diagram', 'Interface matrix.'), ('Rate-monotonic scheduling', 'Shorter period gets higher priority.'), ('Redundancy', 'Extra units for backup.'),
    ('Requirement', 'Verifiable statement of need.'), ('Safe mode', 'Protective spacecraft configuration.'), ('V-model', 'Decompose then integrate and verify.'), ('Watchdog timer', 'Resets a hung processor.')])
RUBRIC = [('4 · Mastery', 'Traces every design choice to a requirement, checks interfaces and failure cases, keeps units and probabilities consistent, and explains trades in plain words.'),
          ('3 · Proficient', 'Solves the practice and exam sets with minor slips and checks units.'),
          ('2 · Developing', 'Follows worked examples but mixes up series and parallel reliability or OR and AND gates.'),
          ('1 · Beginning', 'Computes without a requirement or block diagram; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    c = 299792458; g0 = 9.80665
    I = lambda n: n * (n - 1) / 2
    R = lambda t, l=1e-5: exp(-l * t); par = lambda r: 1 - (1 - r) ** 2; tmr = lambda r: 3 * r ** 2 - 2 * r ** 3
    snr = lambda n: 6.02 * n + 1.76
    drift = lambda b, t: .5 * b * g0 * 1e-3 * t ** 2
    fus = lambda a, b: a * a * b * b / (a * a + b * b)
    hor = lambda h1, h2: 4.12 * (sqrt(h1) + sqrt(h2))
    lam = c / 1090e6; fspl = lambda d: 20 * log10(4 * pi * d / lam)
    rm = lambda n: n * (2 ** (1 / n) - 1)
    r = [
     ('u1 L9', (740 - 400) / 400, .85), ('u1 m', 12 * 1.25, 15), ('u1 A', .3 * 7 + .7 * 8, 7.7), ('u1 B', .3 * 9 + .7 * 6, 6.9), ('u1 life', 10 / 5, 2), ('u1 P', 400 * 1.3, 520), ('u1 x', 740 / 400, 1.85),
     ('u2 8', I(8), 28), ('u2 12', I(12), 66), ('u2 U', (20 + 35 + 15) / 100, .7), ('u2 N2', 8 * 7, 56), ('u2 4', I(4), 6), ('u2 r', I(12) / I(8), 2.357),
     ('u3 R', R(1e4), .905), ('u3 par', par(R(1e4)), .991), ('u3 tmr', tmr(R(1e4)), .975), ('u3 mtbf', 1 / 1e-5, 1e5), ('u3 R50', R(5e4), .607), ('u3 p50', par(R(5e4)), .845), ('u3 t50', tmr(R(5e4)), .657),
     ('u3 A', 1000 / 1002, .998), ('u3 q', 1 - R(1e4), .0952), ('u3 tmr5', tmr(.5), .5),
     ('u4 RPN', 8 * 4 * 5, 160), ('u4 OR', 1 - (1 - 1e-3) * (1 - 2e-3), 2.998e-3), ('u4 AND', 1e-3 * 2e-3, 2e-6), ('u4 RPN2', 8 * 4 * 2, 64), ('u4 approx', 1e-3 + 2e-3, 3e-3),
     ('u5 step', 10 / 2 ** 12, 2.44e-3), ('u5 snr', snr(12), 74.0), ('u5 t', 32 / 1e5, 3.2e-4), ('u5 L', 2 ** 14, 16384), ('u5 snr8', snr(8), 49.9), ('u5 t1553', 32 / 1e6, 3.2e-5), ('u5 s16', 10 / 2 ** 16, 1.53e-4),
     ('u5 lv12', 2 ** 12, 4096),
     ('u6 b', 1e-3 * g0, 9.807e-3), ('u6 60', drift(1, 60), 17.7), ('u6 600', drift(1, 600), 1765), ('u6 10', drift(1, 10), .49), ('u6 rho', c * 1e-6, 300), ('u6 head', .01 * 10, .1), ('u6 3m', 3 / c, 1e-8),
     ('u6 r', drift(1, 600) / drift(1, 60), 100),
     ('u7 var', fus(4, 3), 5.76), ('u7 s', sqrt(fus(4, 3)), 2.4), ('u7 K', 16 / 25, .64), ('u7 x', 100 + .64 * 5, 103.2), ('u7 P', .36 * 16, 5.76), ('u7 eq', sqrt(fus(2, 2)), 1.41),
     ('u8 hor', hor(1e4, 10), 425), ('u8 lam', lam, .275), ('u8 L', fspl(2e5), 139.2), ('u8 fph', 44000 / 24, 1833), ('u8 dbl', 20 * log10(2), 6.02), ('u8 ppf', 3e6 / 44000, 68), ('u8 s', sqrt(10), 3.162),
     ('u9 U', 2 / 10 + 3 / 20 + 5 / 50, .45), ('u9 rm3', rm(3), .78), ('u9 f70', 1 / .07, 14.3), ('u9 f20', 1 / .02, 50), ('u9 rm2', rm(2), .828), ('u9 rm4', rm(4), .757), ('u9 slack', 1 - .45, .55),
     ('u10 arr', 2028 + 6, 2034), ('u10 L9', 10 / 5, 2), ('u10 end', 2034 + 3, 2037), ('u10 hub', 1990 + 34, 2024),
     ('labA 4', I(4), 6), ('labA 8', I(8), 28), ('labA 12', I(12), 66),
     ('labB 1', R(1e3), .990), ('labB d1', par(R(1e3)), .9999), ('labB t1', tmr(R(1e3)), .9997), ('labB 10', R(1e4), .905), ('labB d10', par(R(1e4)), .991), ('labB t10', tmr(R(1e4)), .975),
     ('labB 50', R(5e4), .607), ('labB d50', par(R(5e4)), .845), ('labB t50', tmr(R(5e4)), .657),
     ('labC Rp', 10 * 10 / 20, 5), ('labC I', 12 / 5, 2.4), ('labC I1', 12 / 10, 1.2), ('labC Is', 12 / 20, .6),
     ('labD 8', 10 / 256 * 1e3, 39.06), ('labD 12', 10 / 4096 * 1e3, 2.441), ('labD 16', 10 / 65536 * 1e3, .1526), ('labD s8', snr(8), 49.9), ('labD s12', snr(12), 74.0), ('labD s16', snr(16), 98.1),
     ('labE 10', drift(1, 10), .49), ('labE 60', drift(1, 60), 17.65), ('labE 600', drift(1, 600), 1765), ('labE s', sqrt(fus(4, 3)), 2.4),
     ('labF 1', rm(1), 1), ('labF 2', rm(2), .828), ('labF 3', rm(3), .78), ('labF 4', rm(4), .757),
     ('mid I', I(10), 45), ('mid R', R(5000, 2e-5), .905), ('mid p', par(R(5000, 2e-5)), .991), ('mid RPN', 6 * 3 * 7, 126), ('mid step', 5 / 1024, 4.88e-3), ('mid snr', snr(10), 62.0),
     ('fin d', drift(2, 30), 8.83), ('fin b', 2e-3 * g0, .01961), ('fin s', sqrt(fus(5, 5)), 3.54), ('fin v', fus(5, 5), 12.5), ('fin K', 4 / 5, .8), ('fin h', hor(1000, 10), 143.3), ('fin U', 1 / 5 + 2 / 10 + 3 / 30, .5),
     ('fin A', 500 / 505, .99),
     ('c c', c, 299792458), ('c g', g0, 9.80665), ('c f', 1090e6, 1.09e9), ('c 429', 1e5, 1e5), ('c 1553', 1e6, 1e6), ('c yr', 365 * 24, 8760),
     ('x L9 orb', 1440 / 99, 14.5), ('x L9 sw', 185 * 180, 33300), ('x L9 8', 16 / 2, 8), ('x L9 b', 11, 11), ('x hub g', 6 - 3, 3), ('x hub l', 2024 - 1990, 34), ('x df cr', 2034 - 2028, 6),
     ('x df ms', 70 / 20, 3.5), ('x ato', 29e6 * 2.589988, 7.51e7), ('x u3 r', .991 / .905, 1.095), ('x u4 r', 160 / 64, 2.5), ('x u5 r', 98.1 - 74.0, 24.1), ('x u6 r', 1765 / 17.65, 100), ('x u7 r', 4 / 2.4, 1.667),
     ('x u8 hft', 1e4 * 3.28084, 32808), ('x u9 r', .78 / .45, 1.733), ('x labC r', 2.4 / 1.2, 2), ('x labD r', 39.06 / .1526, 256), ('x labF d', 1 - .757, .243), ('x mid r', 45 / 28, 1.607),
     ('y u1 s', 740 - 400, 340), ('y u2 g', 66 - 28, 38), ('y u3 un', 1 - .991, .009), ('y u4 r', 2.998e-3 / 2e-6, 1499), ('y u5 lv', 2 ** 16, 65536), ('y u6 c', c / 1e3, 299792.458), ('y u7 g', 1 - .64, .36),
     ('y u8 km', 425 * .621371, 264.1), ('y u9 ms', 1000 / 50, 20), ('y u10 r', 2037 - 2028, 9), ('y labB r', .845 / .607, 1.392), ('y fin d', 8.83 / 2, 4.415), ('y L9 km', 705 * .621371, 438),
     ('z u1 A1', .3 * 7, 2.1), ('z u1 A2', .7 * 8, 5.6), ('z u1 B1', .3 * 9, 2.7), ('z u1 B2', .7 * 6, 4.2), ('z u2 sum', 20 + 35 + 15, 70), ('z u3 qq', (1 - R(1e4)) ** 2, .00906),
     ('z u3 R2', R(1e4) ** 2, .8187), ('z u3 R3', R(1e4) ** 3, .7408), ('z u4 p', .999 * .998, .997), ('z u5 w', 1e5 / 32, 3125), ('z u6 q', .5 * 9.807e-3 * 3600, 17.65), ('z u7 n', 16 + 9, 25),
     ('z u7 i', 105 - 100, 5), ('z u8 sh', sqrt(1e4), 100), ('z u8 a', 4 * pi * 2e5 / lam, 9.139e6), ('z u9 t1', 2 / 10, .2), ('z u9 t2', 3 / 20, .15), ('z u9 t3', 5 / 50, .1), ('z u9 c', 2 ** (1 / 3), 1.26),
     ('z mid q', 1 - R(5000, 2e-5), .0952), ('z fin s1', sqrt(1000), 31.62), ('z fin sq', 30 ** 2, 900), ('z labB x', 1e-5 * 5e4, .5), ('z labE b', .5 * 9.807e-3 * 100, .49)]
    return r
