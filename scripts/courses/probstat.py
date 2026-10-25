"""Probability & Statistics (MATH 350): descriptive statistics, probability rules, conditional probability and Bayes, discrete and continuous distributions, sampling and the central limit theorem, confidence intervals, hypothesis tests, regression and correlation, and reliability.
Oct 25 2026, founder-approved four-year track, junior course 8. Same module fields as numerics.py / orbit.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, exp, log, erf, comb
ID = 'probstat'
STATUS = 'live'
YEAR = 3
PAGE = 'Probability_Statistics.html'
CODE = 'MATH 350'
TITLE = 'Probability & Statistics'
LAB_NAME = 'Statistics lab'
TAGLINE = 'Uncertainty, data and reliability: describing data, the rules of probability, Bayes’ theorem, binomial, Poisson, normal and exponential models, sampling and the central limit theorem, confidence intervals, hypothesis tests, regression and system reliability, with six labs. Free, self-paced, and tied to USGS flood and earthquake probabilities, NOAA hurricane outlooks and the Mauna Loa CO₂ record.'
DESC = 'Free self-study Probability & Statistics: 10 units, worked examples, solved practice, quizzes, flashcards, 6 PhET and spreadsheet labs, practice exams, tied to flood, earthquake and hurricane risk and climate data.'
ALT = 'The GOES-U weather satellite, now GOES-19, in a processing facility at NASA’s Kennedy Space Center'
_PH = 'https://phet.colorado.edu/en/simulations/'
_MIT = ('MIT OpenCourseWare 18.05 Introduction to Probability and Statistics (Spring 2022)', 'https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/')
_MIT6 = ('MIT OpenCourseWare 6.041 Probabilistic Systems Analysis and Applied Probability (Fall 2010)', 'https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/')
_OS = ('OpenStax Introductory Statistics 2e', 'https://openstax.org/books/introductory-statistics-2e/pages/1-introduction')
_NIST = ('NIST/SEMATECH e-Handbook of Statistical Methods', 'https://www.itl.nist.gov/div898/handbook/')
_FL = ('USGS Water Science School: The 100-Year Flood', 'https://www.usgs.gov/special-topics/water-science-school/science/100-year-flood')
_EQ = ('USGS FAQ: What is the probability that an earthquake will occur in the Los Angeles area? In the San Francisco Bay area?', 'https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area')
_NHC = ('NOAA National Hurricane Center: Definition of the NHC Track Forecast Cone', 'https://www.nhc.noaa.gov/aboutcone.shtml')
_CPC = ('NOAA Climate Prediction Center: Atlantic Hurricane Outlook (updated Aug. 6, 2026)', 'https://cpc.ncep.noaa.gov/products/outlooks/hurricane.shtml')
_MLO = ('NOAA Global Monitoring Laboratory: Trends in atmospheric CO₂ (Mauna Loa)', 'https://gml.noaa.gov/ccgg/trends/')
_MLOD = ('NOAA GML: Mauna Loa annual mean CO₂ data', 'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt')
_GT = ('NASA GISS: GISS Surface Temperature Analysis (GISTEMP v4)', 'https://data.giss.nasa.gov/gistemp/')
BANNER = ['images/GOES19_GOESU_KSC.jpg', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg', 'images/ISS_Flyaround_2021.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg']
CREDITS = {'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC', 'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA',
           'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)', 'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a one-semester junior probability and statistics course for engineers. It is modeled on the topics and depth of MIT 18.05 Introduction to Probability and Statistics and MIT 6.041 Probabilistic Systems Analysis (free on MIT OpenCourseWare), using the free OpenStax Introductory Statistics text and the NIST/SEMATECH e-Handbook of Statistical Methods, which we link where they help. None of those authors, schools or agencies endorses this page.',
         'What we add: every unit ties to real work with a cited public source (USGS flood and earthquake probabilities, NOAA hurricane outlooks and forecast cones, the Mauna Loa CO₂ record and NASA’s temperature analysis), every number on the page is re-computed by a checking script before it goes live, and every lab has a free simulation or a spreadsheet.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['Protecting people and the planet is a question of odds: how likely a flood, earthquake or hurricane is, how sure we are that CO₂ is rising faster, and how reliable the systems that warn us are.',
                 'Statistics turns data into those odds and tells us how much to trust them. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Calculus I and II: derivatives, integrals and series.', 'Linear Algebra: vectors and least squares (helpful for regression).',
           'Intro Programming or spreadsheet skills: formulas, ranges and charts.', 'Numerical Methods (helpful, not required).']
STUDY = ['Write down the random variable and its units before computing anything.', 'Draw the distribution or a tree diagram first.',
         'Check that probabilities lie between 0 and 1 and add up to 1.', 'State assumptions such as independence out loud; most errors start there.',
         'Simulate when in doubt: a spreadsheet with RAND() can check almost any probability.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['A computer or tablet for the free PhET Center and Variability, Plinko Probability and Least-Squares Regression simulations.', 'Spreadsheet software (any free one works) with RAND(), NORM.DIST and LINEST, or Python.',
            'NOAA’s Mauna Loa CO₂ data file in a web browser.', 'A calculator; a pair of dice is optional.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a free simulation or a spreadsheet, so there are no physical hazards. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST/SEMATECH e-Handbook of Statistical Methods', 'https://www.itl.nist.gov/div898/handbook/')
CONSTANTS = [('Standard normal (textbook values)', 'Φ(1) = 0.8413, Φ(1.96) = 0.975, Φ(2) − Φ(−2) = 0.9545'), ('Student t, 4 degrees of freedom (textbook value)', 't₀.₉₇₅ = 2.776'),
             ('e', '2.718281828'), ('68–95–99.7 rule', 'share of a normal within 1, 2 and 3 standard deviations'), ('1 ppm', 'one part per million by mole fraction'), ('Annual exceedance probability', '1/(recurrence interval)')]
REF_TITLE = 'Free texts and simulations'
REF_INTRO = 'Use these free lectures, textbooks, handbooks and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT lectures, readings and problem sets.'), (_MIT6[0], _MIT6[1], 'Free MIT applied probability course.'), (_OS[0], _OS[1], 'Free textbook.'),
          (_NIST[0], _NIST[1], 'Free engineering statistics handbook.'), ('PhET: Plinko Probability', _PH + 'plinko-probability', 'Binomial and normal distributions interactively.'), ('PhET: Center and Variability', _PH + 'center-and-variability', 'Mean, median and spread interactively.')]
UNITS = []
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
UNITS.append(
{'id': 'u1', 'title': 'Describing Data: Center, Spread and Plots', 'weeks': 'Week 1',
 'summary': 'Types of data, histograms and box plots, mean and median, range, variance and standard deviation, quartiles and outliers, and why the sample standard deviation divides by n − 1.',
 'objectives': ['Compute mean, median, range and sample standard deviation.', 'Choose between mean and median.', 'Read a histogram and box plot.', 'Flag outliers with the 1.5 IQR rule.'],
 'concepts': ['The mean x̄ = Σx/n is the balance point; the median is the middle value and resists outliers.',
              'The sample variance s² = Σ(x − x̄)²/(n − 1) measures spread; s, its square root, has the data’s units. Dividing by n − 1 corrects for using x̄ instead of the true mean.',
              'The range is max − min; the interquartile range IQR = Q3 − Q1 holds the middle half of the data.',
              'Points more than 1.5 IQR beyond the quartiles are flagged as possible outliers: check them, do not just delete them.',
              'Always plot first: a histogram or box plot shows skew, gaps and outliers that a single number hides.'],
 'eqs': [('\\bar x=\\frac1n\\sum x_i', 'Sample mean'), ('s^2=\\frac{1}{n-1}\\sum(x_i-\\bar x)^2', 'Sample variance'), ('IQR=Q_3-Q_1', 'Interquartile range'), ('z=\\frac{x-\\bar x}{s}', 'Standard score')],
 'worked': [
  _w('NOAA’s Mauna Loa annual means give yearly CO₂ increases for 2021–2025 of 2.20, 2.12, 2.55, 3.53 and 2.74 ppm. Find the mean and median.', ['Sum = 13.14; divide by 5.', 'Sort: 2.12, 2.20, 2.55, 2.74, 3.53.'], 'Mean 2.628 ppm/yr; median 2.55 ppm/yr.'),
  _w('Find the range and sample standard deviation.', ['Range = 3.53 − 2.12.', 's = √(Σ(x − 2.628)²/4).'], 'Range 1.41 ppm/yr; s = 0.564 ppm/yr.'),
  _w('Find the z-score of the 3.53 ppm increase (2024).', ['z = (3.53 − 2.628)/0.564.'], 'z = 1.60.')],
 'practice': [('Which is pulled more by the 3.53 value, mean or median?', 'The mean (2.628 vs 2.55).'), ('Why divide by n − 1?', 'The deviations from x̄ are slightly too small; n − 1 corrects the bias.'),
              ('Units of s for CO₂ increases?', 'ppm per year.'), ('What does a long right tail do to mean vs median?', 'Mean > median.')],
 'misc': [('The mean is always typical.', 'Skew or outliers can pull it away.'), ('Outliers are mistakes.', 'They may be real events; investigate.'), ('Standard deviation can be negative.', 'It is a square root, never negative.')],
 'quiz': [_q('Resists outliers…', ['median', 'mean', 'range', 'variance'], 0, 'Middle value.'), _q('Sample variance divides by…', ['n − 1', 'n', 'n + 1', '2n'], 0, 'Bias correction.'),
          _q('IQR is…', ['Q3 − Q1', 'max − min', 'mean − median', 's²'], 0, 'Middle half.'), _q('Plot data…', ['first', 'never', 'last', 'only if asked'], 0, 'See shape.')],
 'cards': [('Mean', 'Σx/n.'), ('Median', 'Middle value.'), ('Standard deviation', '√(Σ(x − x̄)²/(n − 1)).'), ('IQR', 'Q3 − Q1.'), ('Outlier rule', '1.5 IQR beyond quartiles.'), ('z-score', '(x − x̄)/s.')],
 'planet': {'text': ['NOAA reports that the Mauna Loa CO₂ record, begun by C. David Keeling of Scripps in March 1958, is the longest record of direct measurements of CO₂ in the atmosphere. NOAA’s annual means rose from 414.21 ppm in 2020 to 427.35 ppm in 2025.',
                     'This unit’s summary statistics turn that record into a rate: the five yearly increases average 2.628 ppm per year, with a standard deviation of 0.564 ppm per year from year-to-year variation.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_MLO, _MLOD]},
 'res': [(_OS[0], _OS[1], 'Free textbook.'), ('PhET: Center and Variability', _PH + 'center-and-variability', 'Mean, median and spread interactively.')]})
UNITS.append(
{'id': 'u2', 'title': 'Probability Rules, Counting and Independence', 'weeks': 'Week 2',
 'summary': 'Sample spaces and events, the axioms, complements, addition and multiplication rules, independence, permutations and combinations, and “at least one” problems.',
 'objectives': ['Apply the complement, addition and multiplication rules.', 'Test independence.', 'Count with permutations and combinations.', 'Solve “at least one” problems.'],
 'concepts': ['Probabilities lie between 0 and 1 and the whole sample space has probability 1. P(not A) = 1 − P(A).',
              'Addition rule: P(A or B) = P(A) + P(B) − P(A and B).',
              'A and B are independent if P(A and B) = P(A)P(B); then knowing one tells you nothing about the other.',
              'For “at least one” in n independent trials, use the complement: 1 − (1 − p)ⁿ.',
              'Combinations C(n, k) = n!/(k!(n − k)!) count unordered selections; permutations count ordered ones.'],
 'eqs': [('P(A^c)=1-P(A)', 'Complement'), ('P(A\\cup B)=P(A)+P(B)-P(A\\cap B)', 'Addition rule'), ('P(A\\cap B)=P(A)P(B)', 'Independence'), ('P(\\ge1)=1-(1-p)^n', 'At least one')],
 'worked': [
  _w('A 100-year flood has a 1% chance each year. Find the chance of at least one in a 30-year mortgage.', ['P(none) = 0.99³⁰ = 0.740.', 'P(at least one) = 1 − 0.740.'], '26.0%.'),
  _w('Find the chance of at least one 100-year flood in 100 years.', ['1 − 0.99¹⁰⁰.'], '63.4%, not 100%.'),
  _w('Find the chance of at least one 50-year flood (2% a year) in 30 years.', ['1 − 0.98³⁰.'], '45.5%.')],
 'practice': [('At least one 250-year flood (0.4% a year) in 30 years?', '1 − 0.996³⁰ = 11.3%.'), ('How many ways to choose 6 of 9 items?', 'C(9, 6) = 84.'),
              ('Can two 100-year floods happen in back-to-back years?', 'Yes: each year starts with the same 1% chance.'), ('Are yearly floods treated as independent here?', 'Yes; the USGS notes a rare flood does not reduce the chance of another soon after.')],
 'misc': [('A 100-year flood happens once every 100 years.', 'It has a 1% chance every year.'), ('After a flood, the next is less likely.', 'Each year is independent.'), ('P(A or B) = P(A) + P(B) always.', 'Only if A and B cannot both happen.')],
 'quiz': [_q('P(at least one in n)…', ['1 − (1 − p)ⁿ', 'np', 'pⁿ', '1 − pⁿ'], 0, 'Complement.'), _q('Independent means…', ['P(A∩B) = P(A)P(B)', 'disjoint', 'equal', 'P = 0'], 0, 'Definition.'),
          _q('100-year flood annual chance…', ['1%', '100%', '10%', '0.1%'], 0, 'USGS.'), _q('C(n, k) counts…', ['unordered choices', 'orders', 'outcomes always', 'pairs only'], 0, 'Combinations.')],
 'cards': [('Complement', '1 − P(A).'), ('Addition rule', 'Subtract the overlap.'), ('Independence', 'P(A∩B) = P(A)P(B).'), ('At least one', '1 − (1 − p)ⁿ.'), ('Combination', 'n!/(k!(n − k)!).'), ('AEP', 'Annual exceedance probability.')],
 'planet': {'text': ['The USGS explains that a “100-year flood” is a flood with a 1 percent chance of happening in any year, and that 100-year floods can happen two years in a row. Its table pairs each recurrence interval with an annual exceedance probability: 2 years with 50%, 10 years with 10%, 100 years with 1% and 500 years with 0.2%.',
                     'The USGS notes that in the 1960s the United States chose the 1-percent annual exceedance probability flood as the basis for the National Flood Insurance Program. This unit’s complement rule shows that a 30-year home in that zone has a 26% chance of seeing at least one such flood.'],
            'site': [('Oceans', 'Oceans.html'), ('Solutions', 'Solutions.html')],
            'src': [_FL]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_OS[0], _OS[1], 'Free textbook.')]})
UNITS.append(
{'id': 'u3', 'title': 'Conditional Probability and Bayes’ Theorem', 'weeks': 'Week 3',
 'summary': 'Conditional probability, the multiplication rule, tree diagrams, the law of total probability, Bayes’ theorem, base rates, and turning a 30-year probability into a yearly rate.',
 'objectives': ['Compute conditional probabilities from a table or tree.', 'Apply the law of total probability.', 'Use Bayes’ theorem and explain base-rate effects.', 'Convert multi-year probabilities to annual rates.'],
 'concepts': ['P(A | B) = P(A and B)/P(B) is the probability of A once we know B happened.',
              'The law of total probability adds the branches of a tree: P(A) = Σ P(A | Bᵢ)P(Bᵢ).',
              'Bayes’ theorem reverses a condition: P(B | A) = P(A | B)P(B)/P(A).',
              'Rare events give many false alarms: even a good test has a low positive predictive value when the base rate is small.',
              'If events arrive at a constant rate λ, the chance of at least one in t years is 1 − e^(−λt), so λ = −ln(1 − P)/t.'],
 'eqs': [('P(A|B)=\\frac{P(A\\cap B)}{P(B)}', 'Conditional probability'), ('P(A)=\\sum_i P(A|B_i)P(B_i)', 'Total probability'), ('P(B|A)=\\frac{P(A|B)P(B)}{P(A)}', 'Bayes’ theorem'), ('\\lambda=-\\frac{\\ln(1-P)}{t}', 'Rate from a t-year probability')],
 'worked': [
  _w('A sensor flags a fault 95% of the time when one exists and falsely 5% of the time otherwise; 2% of units have the fault (sample values). Find P(fault | flag).', ['P(flag) = 0.95 × 0.02 + 0.05 × 0.98 = 0.068.', 'Bayes: 0.019/0.068.'], '27.9%: most flags are false alarms.'),
  _w('USGS gives a 72% chance of at least one M ≥ 6.7 earthquake in the San Francisco Bay region in 30 years. Find the yearly rate, assuming a constant rate.', ['λ = −ln(0.28)/30.'], 'λ = 0.0424 per year.'),
  _w('Find the chance of at least one such earthquake in a single year.', ['1 − e^(−0.0424).'], '4.15% per year.')],
 'practice': [('Chance of one in the next 10 years at that rate?', '1 − e^(−0.424) = 34.6%.'), ('Yearly rate for the Los Angeles region’s 60% in 30 years?', '−ln(0.4)/30 = 0.0305 per year.'),
              ('Why is P(fault | flag) so low?', 'The base rate (2%) is small.'), ('Is P(A | B) equal to P(B | A)?', 'Generally no.')],
 'misc': [('P(A | B) = P(B | A).', 'Bayes’ theorem relates them through base rates.'), ('A 95% accurate test is right 95% of the time it fires.', 'Not when the condition is rare.'), ('A 30-year probability divides evenly by 30.', 'Use the rate formula.')],
 'quiz': [_q('Bayes reverses…', ['a condition', 'a sum', 'a mean', 'a sample'], 0, 'P(B|A) from P(A|B).'), _q('Low base rates cause…', ['false alarms', 'more accuracy', 'nothing', 'bias in s'], 0, 'Few true positives.'),
          _q('P(A|B) is…', ['P(A∩B)/P(B)', 'P(A)P(B)', 'P(A) + P(B)', 'P(B)/P(A)'], 0, 'Definition.'), _q('Bay Area 30-year M ≥ 6.7 chance…', ['72%', '7%', '99%', '20%'], 0, 'USGS.')],
 'cards': [('Conditional', 'P(A∩B)/P(B).'), ('Total probability', 'Sum over branches.'), ('Bayes', 'P(A|B)P(B)/P(A).'), ('Base rate', 'Prior frequency.'), ('Rate', 'λ = −ln(1 − P)/t.'), ('Tree diagram', 'Branches multiply, paths add.')],
 'planet': {'text': ['The USGS, using the Uniform California Earthquake Rupture Forecast 3, gives 30-year probabilities of 72% for a magnitude 6.7 earthquake in the San Francisco Bay region and 60% in the Los Angeles region. It also notes that around the world, the chance an earthquake is followed by a larger one nearby within a week is about 5%.',
                     'Turning those 30-year numbers into a yearly rate of about 4% is how engineers and emergency planners compare earthquake risk with other hazards.'],
            'site': [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')],
            'src': [_EQ]},
 'res': [(_MIT6[0], _MIT6[1], 'Free MIT course.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u4', 'title': 'Discrete Random Variables: Binomial and Poisson', 'weeks': 'Weeks 4–5',
 'summary': 'Random variables, probability mass functions, expected value and variance, the Bernoulli and binomial distributions, the Poisson distribution for rare events, and the geometric distribution.',
 'objectives': ['Compute expected value and variance.', 'Apply the binomial distribution.', 'Apply the Poisson distribution to rare events.', 'Choose the right discrete model.'],
 'concepts': ['A random variable assigns a number to each outcome. Its expected value E[X] = Σx p(x) is the long-run average.',
              'Var(X) = E[(X − μ)²]; the standard deviation is its square root.',
              'Binomial: the number of successes in n independent trials with probability p. P(X = k) = C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ, mean np, variance np(1 − p).',
              'Poisson: counts of rare events at rate λ per interval. P(X = k) = e^(−λ)λᵏ/k!, mean and variance both λ.',
              'Geometric: the number of trials until the first success, mean 1/p, which is where “recurrence interval” comes from.'],
 'eqs': [('E[X]=\\sum x\\,p(x)', 'Expected value'), ('P(X=k)=\\binom nk p^k(1-p)^{n-k}', 'Binomial'), ('P(X=k)=\\frac{e^{-\\lambda}\\lambda^k}{k!}', 'Poisson'), ('E[T]=1/p', 'Geometric mean wait')],
 'worked': [
  _w('NOAA sizes its hurricane forecast cone so two-thirds of historical track errors fall inside. Over 9 independent forecasts, find the expected number inside and P(all 9 inside).', ['E = 9 × 2/3.', 'P = (2/3)⁹.'], 'E = 6; P(all 9) = 2.60%.'),
  _w('Find P(exactly 6 of 9 inside).', ['C(9, 6)(2/3)⁶(1/3)³ = 84 × 0.0878 × 0.0370.'], '27.3%.'),
  _w('Model 100-year floods over 100 years as Poisson with λ = 1. Find P(none) and P(2 or more).', ['P(0) = e⁻¹.', 'P(≥2) = 1 − 2e⁻¹.'], 'P(0) = 36.8%; P(≥2) = 26.4%.')],
 'practice': [('Standard deviation of the number inside the cone, n = 9?', '√(9 × 2/3 × 1/3) = 1.414.'), ('Mean wait for a 1%-per-year event (geometric)?', '1/0.01 = 100 years.'),
              ('Poisson P(at least one) with λ = 1?', '1 − e⁻¹ = 63.2%, close to the binomial 63.4%.'), ('When does Poisson approximate binomial well?', 'Large n, small p.')],
 'misc': [('Expected value is the most likely value.', 'It is the long-run average.'), ('Cone = where the storm’s impacts stay.', 'It shows only the probable track of the center.'), ('Poisson needs a fixed number of trials.', 'It counts events in an interval.')],
 'quiz': [_q('Binomial mean…', ['np', 'n/p', 'p', 'n'], 0, 'Sum of Bernoullis.'), _q('Poisson mean and variance…', ['both λ', 'λ and λ²', '1 and λ', '0'], 0, 'Property.'),
          _q('NHC cone circles contain…', ['two-thirds of errors', 'all errors', 'half', '95%'], 0, 'NOAA definition.'), _q('Geometric mean wait…', ['1/p', 'p', 'np', 'p²'], 0, 'Recurrence interval.')],
 'cards': [('Random variable', 'A number per outcome.'), ('E[X]', 'Long-run average.'), ('Binomial', 'Successes in n trials.'), ('Poisson', 'Rare-event counts.'), ('Geometric', 'Trials to first success.'), ('Variance', 'E[(X − μ)²].')],
 'planet': {'text': ['NOAA’s National Hurricane Center builds its track forecast cone from circles sized so that two-thirds of historical official forecast errors over a 5-year sample fall inside. For 2026 in the Atlantic, based on 2021–2025 errors, the circle radius grows from 25 nautical miles at 12 hours to 95 at 72 hours and 200 at 120 hours.',
                     'So the center of a storm will be outside the cone about one time in three, a binomial fact worth knowing before deciding the cone means “safe” or “not safe.”'],
            'site': [('GOES-19', 'GOES-19.html'), ('Oceans', 'Oceans.html')],
            'src': [_NHC]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), ('PhET: Plinko Probability', _PH + 'plinko-probability', 'Binomial interactively.')]})
UNITS.append(
{'id': 'u5', 'title': 'Continuous Distributions: Normal, Exponential and Extremes', 'weeks': 'Week 6',
 'summary': 'Probability density and cumulative distribution functions, the uniform, normal and exponential distributions, standardizing with z, the memoryless property, and return periods for extremes.',
 'objectives': ['Use a PDF and CDF.', 'Find normal probabilities with z-scores.', 'Apply the exponential distribution to waiting times.', 'Relate return period and annual exceedance probability.'],
 'concepts': ['For a continuous variable, probabilities are areas under the density f(x); the CDF F(x) = P(X ≤ x).',
              'The normal distribution is bell-shaped with mean μ and standard deviation σ. About 68%, 95% and 99.7% of values fall within 1, 2 and 3σ.',
              'Standardize with z = (x − μ)/σ and read Φ(z) from a table or NORM.S.DIST.',
              'Waiting times between events at constant rate λ are exponential: P(T > t) = e^(−λt), mean 1/λ. The process has no memory: past waiting does not change future odds.',
              'Return period T and annual exceedance probability are reciprocals: a 0.2 AEP event has a 5-year return period.'],
 'eqs': [('P(a<X<b)=\\int_a^b f(x)\\,dx', 'Probability as area'), ('z=\\frac{x-\\mu}{\\sigma}', 'Standardizing'), ('P(T>t)=e^{-\\lambda t}', 'Exponential survival'), ('T=\\frac{1}{AEP}', 'Return period')],
 'worked': [
  _w('Find P(Z < 1) and the share within ±1σ of a normal.', ['Φ(1) = 0.8413.', 'Φ(1) − Φ(−1).'], '0.8413; 68.3% within ±1σ.'),
  _w('With the Bay Area rate λ = 0.0424 per year from Unit 3, find the mean and median wait for an M ≥ 6.7 earthquake.', ['Mean = 1/λ.', 'Median = ln 2/λ.'], 'Mean 23.6 years; median 16.3 years.'),
  _w('What return period matches a 0.2 annual exceedance probability, and a 0.002 one?', ['T = 1/AEP.'], '5 years and 500 years, matching the USGS table.')],
 'practice': [('P(Z < −1.5)?', '0.0668.'), ('Share within ±2σ?', '95.4%.'),
              ('Φ(1.96)?', '0.975.'), ('A quake has not happened for 20 years. Does the exponential model raise the odds next year?', 'No: it is memoryless (real faults may differ).')],
 'misc': [('P(X = x) > 0 for continuous X.', 'Single points have probability 0.'), ('All data are normal.', 'Check with a plot; extremes are often skewed.'), ('Memoryless means events are scheduled.', 'It means the opposite.')],
 'quiz': [_q('Within ±2σ of a normal…', ['about 95%', '50%', '68%', '99.7%'], 0, 'Empirical rule.'), _q('Exponential mean…', ['1/λ', 'λ', 'λ²', 'ln λ'], 0, 'Property.'),
          _q('Return period of 1% AEP…', ['100 years', '1 year', '10 years', '1000 years'], 0, 'Reciprocal.'), _q('Φ(1) is…', ['0.8413', '0.5', '0.68', '1'], 0, 'Table.')],
 'cards': [('PDF', 'Density; area = probability.'), ('CDF', 'P(X ≤ x).'), ('Normal', 'Bell curve, μ and σ.'), ('z', '(x − μ)/σ.'), ('Exponential', 'Memoryless waiting time.'), ('Return period', '1/AEP.')],
 'planet': {'text': ['The USGS says recurrence intervals come from frequency analysis of historical data, that ten or more years of data are needed, and that an analysis based on 30 years of record earns more confidence than one based on 10. It defines a 1,000-year flood as one with a 0.1% chance in any given year.',
                     'Because flood levels are estimated from past data, the USGS notes the 100-year flood level changes as new floods are recorded or as dams and development alter a basin, so the distribution behind a flood map is an estimate, not a fixed fact.'],
            'site': [('Oceans', 'Oceans.html'), ('Calculus II', 'Calculus_II.html')],
            'src': [_FL]},
 'res': [(_OS[0], _OS[1], 'Free textbook.'), (_NIST[0], _NIST[1], 'Free handbook.')]})
UNITS.append(
{'id': 'u6', 'title': 'Sampling, Simulation and the Central Limit Theorem', 'weeks': 'Week 7',
 'summary': 'Populations and samples, bias and random sampling, the sampling distribution of the mean, standard error, the central limit theorem, the law of large numbers, and Monte Carlo simulation.',
 'objectives': ['Distinguish population and sample quantities.', 'Compute a standard error.', 'State and apply the central limit theorem.', 'Estimate a probability by Monte Carlo simulation.'],
 'concepts': ['A statistic computed from a sample varies from sample to sample; its distribution is the sampling distribution.',
              'The standard error of the mean is σ/√n: four times the data halves it.',
              'Central limit theorem: for large n, the sample mean is approximately normal whatever the shape of the data.',
              'Law of large numbers: sample averages and frequencies settle toward their true values as n grows.',
              'Monte Carlo simulation repeats a random experiment many times on a computer; its error also falls like 1/√n.'],
 'eqs': [('SE=\\frac{\\sigma}{\\sqrt n}', 'Standard error'), ('\\bar X\\approx N\\!\\left(\\mu,\\frac{\\sigma^2}{n}\\right)', 'Central limit theorem'), ('\\hat p=\\frac{\\#\\text{hits}}{N}', 'Monte Carlo estimate'), ('SE_{\\hat p}=\\sqrt{\\frac{p(1-p)}{N}}', 'Proportion standard error')],
 'worked': [
  _w('Measurements have σ = 10 (sample value). Find the standard error of the mean of 25.', ['10/√25.'], 'SE = 2.'),
  _w('A fair die has mean 3.5 and σ = 1.708. Find the standard error of the average of 25 rolls.', ['1.708/5.'], 'SE = 0.342.'),
  _w('How many Monte Carlo runs estimate a probability near 0.5 to ±0.05 (95%)?', ['n = 1.96² × 0.25/0.05².'], 'About 384 runs.')],
 'practice': [('SE of a die average over 100 rolls?', '0.171.'), ('Double the sample size. SE?', 'Divided by √2.'),
              ('Does the CLT make the data normal?', 'No, only the sample mean.'), ('95% margin for the σ = 10, n = 25 mean?', '1.96 × 2 = 3.92.')],
 'misc': [('A big sample fixes bias.', 'It reduces random error only.'), ('n = 30 always suffices.', 'Skewed data may need more.'), ('Simulation is exact.', 'It has its own sampling error.')],
 'quiz': [_q('SE of the mean…', ['σ/√n', 'σ/n', 'σ', 'nσ'], 0, 'Formula.'), _q('CLT is about…', ['the sample mean', 'every data point', 'the median only', 'bias'], 0, 'Sampling distribution.'),
          _q('Monte Carlo error falls like…', ['1/√n', '1/n', 'n', 'constant'], 0, 'SE.'), _q('Random sampling prevents…', ['selection bias', 'variance', 'all error', 'nothing'], 0, 'Design.')],
 'cards': [('Population', 'The whole group.'), ('Sample', 'The part measured.'), ('Standard error', 'σ/√n.'), ('CLT', 'Means become normal.'), ('Law of large numbers', 'Averages settle.'), ('Monte Carlo', 'Repeat random trials.')],
 'planet': {'text': ['NASA’s GISS Surface Temperature Analysis (GISTEMP v4) estimates global surface temperature change from NOAA station and ocean data and is updated about the 10th of every month. NASA also publishes a 2024 uncertainty ensemble for it.',
                     'An uncertainty ensemble is this unit’s Monte Carlo idea at planetary scale: many plausible versions of the record, whose spread shows how sure we are of each year’s value.'],
            'site': [('Earth Observation', 'Earth_Observation.html'), ('Solutions', 'Solutions.html')],
            'src': [_GT]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), ('PhET: Plinko Probability', _PH + 'plinko-probability', 'Watch sums become normal.')]})
UNITS.append(
{'id': 'u7', 'title': 'Confidence Intervals', 'weeks': 'Weeks 8–9',
 'summary': 'Point and interval estimates, z and t intervals for a mean, intervals for a proportion, margin of error and sample size, and what a confidence level does and does not mean.',
 'objectives': ['Build a t interval for a mean.', 'Build an interval for a proportion.', 'Choose a sample size for a target margin.', 'Interpret a confidence level correctly.'],
 'concepts': ['A confidence interval is estimate ± critical value × standard error.',
              'With σ unknown and small n, use Student’s t with n − 1 degrees of freedom; t has fatter tails than z.',
              'For a proportion, p̂ ± z√(p̂(1 − p̂)/n).',
              'A 95% level means 95% of intervals built this way would contain the true value; it is not a 95% chance for one computed interval.',
              'Halving the margin needs four times the sample size.'],
 'eqs': [('\\bar x\\pm t_{n-1}\\frac{s}{\\sqrt n}', 't interval'), ('\\hat p\\pm z\\sqrt{\\frac{\\hat p(1-\\hat p)}{n}}', 'Proportion interval'), ('n=\\frac{z^2p(1-p)}{E^2}', 'Sample size'), ('E=z\\frac{\\sigma}{\\sqrt n}', 'Margin of error')],
 'worked': [
  _w('Build a 95% interval for the mean yearly CO₂ increase from Unit 1 (x̄ = 2.628, s = 0.564, n = 5, t = 2.776).', ['Margin = 2.776 × 0.564/√5.'], '2.628 ± 0.700: from 1.93 to 3.33 ppm/yr.'),
  _w('NOAA says 22 of the 31 Atlantic seasons since 1995 were above normal. Give a 95% interval for that proportion.', ['p̂ = 0.710; SE = √(0.710 × 0.290/31).'], '0.710 ± 0.160: from 0.55 to 0.87.'),
  _w('How large a sample gives a ±0.05 margin for a proportion near 0.5?', ['1.96² × 0.25/0.05².'], 'About 385 (384.2, rounded up).')],
 'practice': [('Why t instead of z for n = 5?', 'σ is estimated from few points.'), ('Effect of 99% instead of 95%?', 'Wider interval.'),
              ('Does NOAA’s 70% range for named storms mean 70% of storms?', 'No: the season total falls in the range in 7 of 10 similar seasons.'), ('Margin for the proportion with n = 124?', 'About half (0.080).')],
 'misc': [('95% chance the true value is in this interval.', 'The procedure captures it 95% of the time.'), ('Wider is worse.', 'Wider is honest when data are few.'), ('Intervals fix bias.', 'They describe random error only.')],
 'quiz': [_q('Small n, σ unknown: use…', ['t', 'z', 'Poisson', 'none'], 0, 'Student.'), _q('Halve the margin…', ['4× the data', '2× the data', 'same data', '½ the data'], 0, '√n.'),
          _q('NOAA likely ranges hold in…', ['7 of 10 similar seasons', 'every season', 'half', '95%'], 0, 'CPC.'), _q('CI = estimate ± …', ['critical value × SE', 'mean', 'range', 'σ²'], 0, 'Structure.')],
 'cards': [('Confidence interval', 'Estimate ± margin.'), ('t distribution', 'Fatter tails, n − 1 df.'), ('Margin of error', 'Critical value × SE.'), ('Confidence level', 'Long-run capture rate.'), ('Proportion interval', 'p̂ ± z√(p̂(1−p̂)/n).'), ('Sample size', 'z²p(1−p)/E².')],
 'planet': {'text': ['NOAA’s Climate Prediction Center outlook for 2026, updated August 6, gives a 75% chance of a below-normal Atlantic season, 20% near-normal and 5% above-normal, and a 70% probability for each range, including 7–13 named storms and 2–6 hurricanes.',
                     'NOAA explains that the season is expected to fall within these ranges in 7 out of 10 seasons with similar conditions, which is exactly how a 70% interval should be read. It also stresses that it only takes one hurricane to cause a disaster.'],
            'site': [('GOES-19', 'GOES-19.html'), ('Oceans', 'Oceans.html')],
            'src': [_CPC]},
 'res': [(_OS[0], _OS[1], 'Free textbook.'), (_MIT[0], _MIT[1], 'Free MIT lectures.')]})
UNITS.append(
{'id': 'u8', 'title': 'Hypothesis Tests and p-Values', 'weeks': 'Week 10',
 'summary': 'Null and alternative hypotheses, test statistics, p-values, one- and two-sided tests, t tests and proportion tests, Type I and Type II errors, power, and statistical versus practical significance.',
 'objectives': ['Set up null and alternative hypotheses.', 'Run a one-sample t test and a proportion test.', 'Interpret a p-value.', 'Explain Type I and Type II errors and power.'],
 'concepts': ['A test asks whether data are surprising if the null hypothesis H₀ were true.',
              'The p-value is the probability, under H₀, of a result at least as extreme as the one seen. Small p is evidence against H₀; it is not the probability H₀ is true.',
              'A Type I error rejects a true H₀ (rate α); a Type II error misses a false H₀ (rate β). Power = 1 − β.',
              'More data raise power; a tiny, unimportant effect can be “significant” with enough data.',
              'Decide α and the test before looking at the data.'],
 'eqs': [('t=\\frac{\\bar x-\\mu_0}{s/\\sqrt n}', 't statistic'), ('z=\\frac{\\hat p-p_0}{\\sqrt{p_0(1-p_0)/n}}', 'Proportion z'), ('\\text{power}=1-\\beta', 'Power'), ('p=P(\\text{as extreme}\\mid H_0)', 'p-value')],
 'worked': [
  _w('Test H₀: μ = 2 ppm/yr against μ > 2 for the five CO₂ increases (x̄ = 2.628, s = 0.564).', ['t = (2.628 − 2)/(0.564/√5).'], 't = 2.49 with 4 df, above the one-sided 5% cutoff of 2.132: reject H₀.'),
  _w('If each Atlantic season had a 1/3 chance of being above normal, how many of 31 would we expect?', ['31/3.'], 'About 10.3; NOAA reports 22.'),
  _w('Find the exact binomial P(22 or more of 31) under p = 1/3.', ['Sum C(31, k)(1/3)ᵏ(2/3)³¹⁻ᵏ for k ≥ 22.'], 'p ≈ 2.06 × 10⁻⁵: strong evidence the high-activity era is real.')],
 'practice': [('Proportion z for 22 of 31 vs p₀ = 1/3?', 'z = 4.45.'), ('Is p = 0.03 the chance H₀ is true?', 'No.'),
              ('Type I error in a flood-warning test?', 'A false alarm.'), ('How do you raise power?', 'More data, larger effect, or larger α.')],
 'misc': [('p > 0.05 proves H₀.', 'It only fails to reject.'), ('Significant means important.', 'Check the effect size.'), ('Test many things, report the winner.', 'That inflates false positives.')],
 'quiz': [_q('p-value is…', ['P(data this extreme | H₀)', 'P(H₀)', 'α', 'power'], 0, 'Definition.'), _q('Type I error…', ['reject true H₀', 'miss false H₀', 'bad data', 'none'], 0, 'False alarm.'),
          _q('Power is…', ['1 − β', 'α', 'p', '1 − α'], 0, 'Detect a real effect.'), _q('More data…', ['raise power', 'lower power', 'no change', 'raise α'], 0, 'Smaller SE.')],
 'cards': [('H₀', 'Null hypothesis.'), ('p-value', 'Surprise under H₀.'), ('α', 'Type I rate.'), ('β', 'Type II rate.'), ('Power', '1 − β.'), ('Effect size', 'How big, not just whether.')],
 'planet': {'text': ['NOAA’s Climate Prediction Center reports that since the current Atlantic high-activity era began in 1995, 22 of 31 seasons (71%) were above normal, 5 (16%) near normal and 4 (13%) below normal.',
                     'NOAA also notes that every hurricane season coinciding with a strong El Niño since 1950 has had below-normal activity. Testing claims like these against chance is how forecasters decide which signals belong in an outlook.'],
            'site': [('GOES-19', 'GOES-19.html'), ('Solutions', 'Solutions.html')],
            'src': [_CPC]},
 'res': [(_MIT[0], _MIT[1], 'Free MIT lectures.'), (_NIST[0], _NIST[1], 'Free handbook.')]})
UNITS.append(
{'id': 'u9', 'title': 'Correlation and Linear Regression', 'weeks': 'Weeks 11–12',
 'summary': 'Scatter plots, correlation r, least-squares regression, slope interpretation, R², residuals, prediction versus extrapolation, and correlation versus causation.',
 'objectives': ['Compute and interpret r and R².', 'Fit and interpret a least-squares line.', 'Use residual plots to check a model.', 'Separate correlation from causation.'],
 'concepts': ['Correlation r measures linear association from −1 to 1; it has no units.',
              'The least-squares line ŷ = b₀ + b₁x has slope b₁ = Sxy/Sxx and passes through (x̄, ȳ).',
              'R² = r² is the share of variation in y explained by the line.',
              'Residual plots reveal curvature or changing spread that r hides.',
              'Correlation is not causation; physical mechanisms and designed studies are needed for that. Extrapolation beyond the data is risky.'],
 'eqs': [('b_1=\\frac{S_{xy}}{S_{xx}}', 'Slope'), ('b_0=\\bar y-b_1\\bar x', 'Intercept'), ('r=\\frac{S_{xy}}{\\sqrt{S_{xx}S_{yy}}}', 'Correlation'), ('R^2=r^2', 'Explained share')],
 'worked': [
  _w('Fit a line to NOAA’s Mauna Loa decade means 1960–2020 (316.91, 325.68, 338.76, 354.45, 369.71, 390.10, 414.21 ppm), with x in years since 1960.', ['x̄ = 30, ȳ = 358.55.', 'b₁ = Sxy/Sxx.'], 'ŷ = 310.15 + 1.613x ppm.'),
  _w('Find r and R².', ['r = Sxy/√(SxxSyy).'], 'r = 0.990; R² = 0.979.'),
  _w('Do the residuals support a straight line?', ['Residuals are positive at both ends and negative in the middle.'], 'No: the curve bends upward, so growth is accelerating despite R² = 0.979.')],
 'practice': [('Units of the slope?', 'ppm per year.'), ('Line prediction for 2025 (x = 65)?', '415.0 ppm vs NOAA’s 427.35.'),
              ('Does r = 0.99 prove the line is right?', 'No; check the residuals.'), ('Does a time trend alone prove its cause?', 'No; the cause comes from physics and other evidence.')],
 'misc': [('High r means a good model.', 'Curvature can hide behind high r.'), ('r has units.', 'It is unitless.'), ('Extrapolating is safe if R² is high.', 'Not outside the data range.')],
 'quiz': [_q('R² is…', ['share of variation explained', 'slope', 'p-value', 'residual'], 0, 'Definition.'), _q('The line passes through…', ['(x̄, ȳ)', 'origin', '(0, ȳ)', 'max point'], 0, 'Property.'),
          _q('Curved residuals mean…', ['wrong model form', 'perfect fit', 'no data', 'bias in x'], 0, 'Pattern.'), _q('Correlation shows…', ['association', 'causation', 'nothing', 'error'], 0, 'Caution.')],
 'cards': [('Correlation', '−1 to 1, unitless.'), ('Slope', 'Sxy/Sxx.'), ('R²', 'Share explained.'), ('Residual', 'y − ŷ.'), ('Extrapolation', 'Predicting outside the data.'), ('Causation', 'Needs mechanism or design.')],
 'planet': {'text': ['NOAA notes that the Mauna Loa data are taken at an altitude of 3400 m and may differ from the global average, and that during the 2022 Mauna Loa eruption measurements moved to Maunakea, about 21 miles north, until July 2023.',
                     'Knowing where and how data were collected is part of regression too: a fit is only as good as the record behind it, and NOAA documents its gaps and site changes openly.'],
            'site': [('Solutions', 'Solutions.html'), ('Linear Algebra', 'Linear_Algebra.html')],
            'src': [_MLO]},
 'res': [('PhET: Least-Squares Regression', _PH + 'least-squares-regression', 'Fit lines interactively.'), (_OS[0], _OS[1], 'Free textbook.')]})
UNITS.append(
{'id': 'u10', 'title': 'Reliability and Risk', 'weeks': 'Weeks 13–15',
 'summary': 'Reliability functions, failure rates and MTBF, series and parallel systems, redundancy, the exponential and Weibull life models, and combining probability with consequences into risk.',
 'objectives': ['Compute reliability of series and parallel systems.', 'Use the exponential life model with MTBF.', 'Explain the bathtub curve and Weibull shapes.', 'Combine likelihood and consequence into risk.'],
 'concepts': ['Reliability R(t) is the probability a part survives to time t. With constant failure rate λ, R(t) = e^(−λt) and MTBF = 1/λ.',
              'Series systems need every part: R = R₁R₂…Rₙ, always worse than the weakest part.',
              'Parallel (redundant) systems need only one: R = 1 − (1 − R₁)(1 − R₂)….',
              'The Weibull model covers early failures (shape < 1), random failures (shape = 1, exponential) and wear-out (shape > 1), the three parts of the bathtub curve.',
              'Risk combines probability and consequence; redundancy and warnings reduce it, but only if failures are independent.'],
 'eqs': [('R(t)=e^{-\\lambda t},\\ MTBF=1/\\lambda', 'Exponential reliability'), ('R_s=\\prod R_i', 'Series system'), ('R_p=1-\\prod(1-R_i)', 'Parallel system'), ('R(t)=e^{-(t/\\eta)^\\beta}', 'Weibull')],
 'worked': [
  _w('Three parts in series each have R = 0.99 (sample values). Find the system reliability.', ['0.99³.'], 'R = 0.9703.'),
  _w('Two redundant pumps each have R = 0.9. Find the system reliability.', ['1 − 0.1².'], 'R = 0.99.'),
  _w('A sensor has MTBF 50,000 h. Find its reliability over a 1000-hour mission.', ['e^(−1000/50,000).'], 'R = 0.980.')],
 'practice': [('Three redundant units of 0.9?', '1 − 0.1³ = 0.999.'), ('A 0.9 part in series with a redundant pair of 0.9?', '0.9 × 0.99 = 0.891.'),
              ('Reliability over a year (8760 h) at MTBF 100,000 h?', 'e^(−0.0876) = 0.916.'), ('Two 0.95 units in parallel?', '0.9975.')],
 'misc': [('Redundancy always helps.', 'Not against common-cause failures.'), ('MTBF is how long every unit lasts.', 'It is an average; many fail sooner.'), ('A series system is as reliable as its best part.', 'It is worse than its weakest.')],
 'quiz': [_q('Series reliability…', ['product', 'sum', 'max', 'min'], 0, 'All must work.'), _q('Exponential MTBF…', ['1/λ', 'λ', 'e^λ', 'ln λ'], 0, 'Mean life.'),
          _q('Weibull shape > 1 means…', ['wear-out', 'infant mortality', 'random', 'none'], 0, 'Rising hazard.'), _q('Redundancy fails against…', ['common causes', 'random failures', 'nothing', 'small λ'], 0, 'Shared failure.')],
 'cards': [('Reliability', 'P(survive to t).'), ('MTBF', '1/λ.'), ('Series', 'Multiply R.'), ('Parallel', '1 − Π(1 − R).'), ('Weibull', 'Bathtub shapes.'), ('Risk', 'Probability × consequence.')],
 'planet': {'text': ['NOAA’s 2026 hurricane outlook reminds residents, businesses and governments that hurricane-related disasters can occur in any season, even one with low activity, and that coastal communities should prepare every year regardless of the outlook.',
                     'That is reliability thinking: a low probability is not zero, so warning systems, backups and plans are designed to work in the rare bad year, not just the average one.'],
            'site': [('GOES-19', 'GOES-19.html'), ('Solutions', 'Solutions.html')],
            'src': [_CPC]},
 'res': [(_NIST[0], _NIST[1], 'Free handbook (reliability chapter).'), (_MIT6[0], _MIT6[1], 'Free MIT course.')]})
LABS = []
LABS.append(
{'id': 'labA', 'title': 'Lab A: Center and spread of the CO₂ record', 'week': 'Week 1',
 'goal': 'Explore mean, median and spread in PhET Center and Variability, then summarize NOAA’s recent yearly CO₂ increases.',
 'eq': ('s=\\sqrt{\\frac{\\sum(x-\\bar x)^2}{n-1}}', 'Sample standard deviation'),
 'steps': ['In PhET Center and Variability, drag values and watch the mean and median move.', 'Open NOAA’s Mauna Loa annual means and compute the yearly increases for 2021–2025.', 'Compute mean, median, range and s.', 'Make a dot plot and describe the 2024 value.'],
 'table': (['Statistic', 'Value (ppm/yr)'], [['Mean', '2.628'], ['Median', '2.55'], ['Range', '1.41'], ['Standard deviation', '0.564']]),
 'note': 'Data from NOAA GML; statistics computed.',
 'calc': ['Increases: 2.20, 2.12, 2.55, 3.53, 2.74.', 's = √(1.2735/4) = 0.564.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('PhET: Center and Variability', _PH + 'center-and-variability'), (_MLOD[0], _MLOD[1])],
 'planet': 'NOAA’s Mauna Loa monthly mean was 426.07 ppm in September 2026.', 'planet_src': [_MLO]})
LABS.append(
{'id': 'labB', 'title': 'Lab B: Plinko and the binomial distribution', 'week': 'Week 4',
 'goal': 'Drop balls in PhET Plinko Probability and compare the histogram with the binomial model.',
 'eq': ('\\mu=np,\\ \\sigma=\\sqrt{np(1-p)}', 'Binomial mean and spread'),
 'steps': ['Set 12 rows and p = 0.5.', 'Drop 1000 balls and record the mean and standard deviation.', 'Compute the binomial values.', 'Change p to 0.7 and predict the new mean before dropping.'],
 'table': (['Quantity', 'Binomial value'], [['Mean bin', '6'], ['Standard deviation', '1.732'], ['P(bin 6)', '0.2256']]),
 'note': 'Computed values; your simulation should come close.',
 'calc': ['σ = √(12 × 0.25) = 1.732.', 'P(6) = C(12, 6)/2¹² = 924/4096 = 0.2256.'],
 'safety': ['Computer only.'], 'home': ['Any browser works.'],
 'sims': [('PhET: Plinko Probability', _PH + 'plinko-probability')],
 'planet': 'NOAA sizes its hurricane cone so two-thirds of past track errors fall inside.', 'planet_src': [_NHC]})
LABS.append(
{'id': 'labC', 'title': 'Lab C: Simulating 100-year floods', 'week': 'Week 6',
 'goal': 'Use a spreadsheet Monte Carlo to estimate the chance of at least one 1%-per-year flood in 30 years.',
 'eq': ('P=1-0.99^{30}', 'Exact answer'),
 'steps': ['Make 30 columns of =RAND()<0.01 (one per year).', 'In each row, test whether any year flooded.', 'Copy to 1000 rows and average the result.', 'Compare with the exact answer and the expected Monte Carlo error.'],
 'table': (['Quantity', 'Value'], [['Exact probability', '0.260'], ['Monte Carlo SE, N = 1000', '0.0139'], ['Expected range (±2 SE)', '0.232 to 0.288']]),
 'note': 'Computed values; your estimate will vary each recalculation.',
 'calc': ['SE = √(0.26 × 0.74/1000) = 0.0139.', '0.260 ± 0.0278.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_MIT[0], _MIT[1])],
 'planet': 'The USGS stresses that 100-year floods can happen two years in a row.', 'planet_src': [_FL]})
LABS.append(
{'id': 'labD', 'title': 'Lab D: Dice and the central limit theorem', 'week': 'Week 7',
 'goal': 'Average simulated (or real) dice rolls and watch the distribution of averages become normal.',
 'eq': ('SE=\\frac{\\sigma}{\\sqrt n}', 'Standard error'),
 'steps': ['Simulate rolls with =RANDBETWEEN(1,6).', 'Average groups of 1, 5, 25 and 100 rolls, 500 times each.', 'Plot histograms and compute their standard deviations.', 'Compare with σ/√n.'],
 'table': (['Rolls per average', 'Predicted SE'], [['1', '1.708'], ['25', '0.342'], ['100', '0.171']]),
 'note': 'Computed values; a die has mean 3.5 and σ = √(35/12).',
 'calc': ['σ = √(35/12) = 1.708.', 'SE(25) = 1.708/5 = 0.342.'],
 'safety': ['Computer only.'], 'home': ['Real dice work too.'],
 'sims': [('PhET: Plinko Probability', _PH + 'plinko-probability')],
 'planet': 'NASA publishes an uncertainty ensemble for its GISTEMP temperature record.', 'planet_src': [_GT]})
LABS.append(
{'id': 'labE', 'title': 'Lab E: Regression and residuals', 'week': 'Week 12',
 'goal': 'Fit a line in PhET Least-Squares Regression, then fit NOAA’s Mauna Loa decade means and study the residuals.',
 'eq': ('\\hat y=b_0+b_1x', 'Least-squares line'),
 'steps': ['In PhET, place points and compare your line with the best fit.', 'Enter the 1960–2020 decade means with x = years since 1960.', 'Use LINEST or a trendline to get b₀, b₁ and r.', 'Plot the residuals and describe the pattern.'],
 'table': (['Quantity', 'Value'], [['Slope', '1.613 ppm/yr'], ['Intercept', '310.15 ppm'], ['r', '0.990'], ['Residuals 1960 / 2000 / 2020', '+6.76 / −4.97 / +7.27 ppm']]),
 'note': 'Data from NOAA GML; fit computed. The U-shaped residuals show upward curvature.',
 'calc': ['b₁ = Sxy/Sxx = 1.613.', 'Residual 2020 = 414.21 − (310.15 + 1.613 × 60) = 7.27.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [('PhET: Least-Squares Regression', _PH + 'least-squares-regression'), (_MLOD[0], _MLOD[1])],
 'planet': 'NOAA notes Mauna Loa samples air at 3400 m, which may differ from the global average.', 'planet_src': [_MLO]})
LABS.append(
{'id': 'labF', 'title': 'Lab F: Reliability of a warning system', 'week': 'Week 14',
 'goal': 'Build a spreadsheet for series and parallel reliability and test how redundancy changes a sample flood-warning chain.',
 'eq': ('R_s=\\prod R_i,\\ R_p=1-\\prod(1-R_i)', 'System reliability'),
 'steps': ['Model a sample chain: sensor, radio link and siren in series.', 'Compute R with each at 0.99, then with a redundant siren pair.', 'Use e^(−t/MTBF) for a 1000 h mission at 50,000 h MTBF.', 'Find which single upgrade helps most.'],
 'table': (['Configuration', 'Reliability'], [['Three parts in series (0.99 each)', '0.9703'], ['Two redundant units (0.9 each)', '0.99'], ['0.9 part + redundant 0.9 pair', '0.891'], ['1000 h at MTBF 50,000 h', '0.980']]),
 'note': 'Sample values; computed.',
 'calc': ['0.99³ = 0.9703.', '0.9 × (1 − 0.1²) = 0.891.'],
 'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'],
 'sims': [(_NIST[0], _NIST[1])],
 'planet': 'NOAA says disasters can occur even in low-activity hurricane seasons, so prepare every year.', 'planet_src': [_CPC]})
SCHEDULE = [(1, 'u1', 'Describing data; Lab A', 'OpenStax Intro Stats'), (2, 'u2', 'Probability rules and counting', 'MIT 18.05'),
            (3, 'u3', 'Conditional probability and Bayes', 'MIT 6.041'), (4, 'u4', 'Discrete variables and the binomial; Lab B', 'MIT 18.05'),
            (5, 'u4', 'Poisson and geometric models', 'MIT 18.05'), (6, 'u5', 'Continuous distributions; Lab C', 'USGS 100-year flood'),
            (7, 'u6', 'Sampling and the CLT; Lab D; midterm practice', 'MIT 18.05'), (8, 'u7', 'Confidence intervals for means', 'OpenStax Intro Stats'),
            (9, 'u7', 'Intervals for proportions and sample size', 'NOAA CPC'), (10, 'u8', 'Hypothesis tests and p-values', 'MIT 18.05'),
            (11, 'u9', 'Correlation and regression', 'OpenStax Intro Stats'), (12, 'u9', 'Residuals and model checking; Lab E', 'NOAA GML'),
            (13, 'u10', 'Reliability and MTBF', 'NIST e-Handbook'), (14, 'u10', 'System reliability; Lab F', 'NIST e-Handbook'),
            (15, 'u10', 'Risk and review; final practice', 'NOAA CPC; USGS')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('Find the mean, median and sample standard deviation of 4, 8, 6, 10, 12.', ['Mean = 40/5.', 's = √(40/4).'], 'Mean 8, median 8, s = 3.16.'),
  ('Find the chance of at least one 25-year flood (4% a year) in 10 years.', ['1 − 0.96¹⁰.'], '33.5%.'),
  ('A test detects a condition 90% of the time and false-alarms 10%; the base rate is 1%. Find P(condition | positive).', ['0.009/(0.009 + 0.099).'], '8.33%.'),
  ('Find P(X = 0) for a binomial with n = 5, p = 0.2.', ['0.8⁵.'], '0.328.'),
  ('Find P(X = 0) for a Poisson with λ = 2.', ['e⁻².'], '0.135.')]),
 ('Final practice set (all units)', [
  ('Find P(Z > 1.96).', ['1 − 0.975.'], '0.025.'),
  ('Find the standard error for σ = 6, n = 36.', ['6/6.'], '1.'),
  ('Build a 95% interval for x̄ = 50, s = 4, n = 16 (t = 2.131).', ['2.131 × 4/4.'], '50 ± 2.13.'),
  ('Test H₀: μ = 50 with x̄ = 52, s = 4, n = 16.', ['t = 2/(4/4).'], 't = 2.0, just below 2.131: do not reject at 5% (two-sided).'),
  ('Find the reliability of four 0.95 parts in series.', ['0.95⁴.'], '0.815.'),
  ('A part has MTBF 2000 h. Find P(it survives 500 h).', ['e^(−0.25).'], '0.779.')])]
FORMULAS = ['\\bar x=\\sum x/n,\\ s^2=\\sum(x-\\bar x)^2/(n-1)', 'P(\\ge1)=1-(1-p)^n,\\ P(A\\cup B)=P(A)+P(B)-P(A\\cap B)', 'P(B|A)=P(A|B)P(B)/P(A),\\ \\lambda=-\\ln(1-P)/t',
            'P(X=k)=\\binom nk p^k(1-p)^{n-k},\\ P(X=k)=e^{-\\lambda}\\lambda^k/k!', 'z=(x-\\mu)/\\sigma,\\ P(T>t)=e^{-\\lambda t},\\ T=1/AEP', 'SE=\\sigma/\\sqrt n',
            '\\bar x\\pm t\\,s/\\sqrt n,\\ \\hat p\\pm z\\sqrt{\\hat p(1-\\hat p)/n}', 't=(\\bar x-\\mu_0)/(s/\\sqrt n)', 'b_1=S_{xy}/S_{xx},\\ r=S_{xy}/\\sqrt{S_{xx}S_{yy}}', 'R_s=\\prod R_i,\\ R_p=1-\\prod(1-R_i),\\ MTBF=1/\\lambda']
GLOSSARY = sorted([('Annual exceedance probability', 'Chance an event is equalled or exceeded in a year.'), ('Bayes’ theorem', 'Reverses a conditional probability.'), ('Binomial distribution', 'Successes in n independent trials.'), ('Central limit theorem', 'Sample means become normal.'),
    ('Conditional probability', 'Probability given that another event occurred.'), ('Confidence interval', 'Range from a procedure that captures the truth at a set rate.'), ('Correlation', 'Strength of linear association.'), ('Expected value', 'Long-run average.'),
    ('Exponential distribution', 'Memoryless waiting time.'), ('Independence', 'One event does not change another’s probability.'), ('MTBF', 'Mean time between failures.'), ('Median', 'Middle value.'),
    ('Monte Carlo', 'Estimating by repeated random simulation.'), ('Normal distribution', 'Bell-shaped distribution.'), ('p-value', 'Chance of data this extreme if H₀ holds.'), ('Poisson distribution', 'Counts of rare events.'),
    ('Recurrence interval', 'Average years between events of a given size.'), ('Reliability', 'Probability of surviving to a given time.'), ('Standard error', 'Standard deviation of a statistic.'), ('Type I error', 'Rejecting a true null hypothesis.')])
RUBRIC = [('4 · Mastery', 'Names the random variable, states assumptions, picks the right model, reports uncertainty and interprets results in plain words.'), ('3 · Proficient', 'Solves the practice problems with occasional slips in assumptions or units.'),
          ('2 · Developing', 'Follows worked examples but misreads p-values or confidence levels.'), ('1 · Beginning', 'Plugs numbers into formulas without checking assumptions; needs to revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
    ann = [414.21, 416.41, 418.53, 421.08, 424.61, 427.35]
    d = [ann[i + 1] - ann[i] for i in range(5)]; m = sum(d) / 5; ss = sum((x - m) ** 2 for x in d); s = sqrt(ss / 4)
    lam = -log(.28) / 30; lamLA = -log(.4) / 30
    bp = lambda n, k, p: comb(n, k) * p ** k * (1 - p) ** (n - k)
    yrs = [0, 10, 20, 30, 40, 50, 60]; co = [316.91, 325.68, 338.76, 354.45, 369.71, 390.10, 414.21]
    mx = sum(yrs) / 7; my = sum(co) / 7
    sxy = sum((x - mx) * (y - my) for x, y in zip(yrs, co)); sxx = sum((x - mx) ** 2 for x in yrs); syy = sum((y - my) ** 2 for y in co)
    b1 = sxy / sxx; b0 = my - b1 * mx; rr = sxy / sqrt(sxx * syy); res = lambda x, y: y - (b0 + b1 * x)
    ph = 22 / 31; seh = sqrt(ph * (1 - ph) / 31)
    tail = sum(bp(31, k, 1 / 3) for k in range(22, 32))
    sd6 = sqrt(35 / 12)
    ex = [4, 8, 6, 10, 12]; exm = sum(ex) / 5
    r = [
     ('u1 sum', sum(d), 13.14), ('u1 mean', m, 2.628), ('u1 med', sorted(d)[2], 2.55), ('u1 rng', max(d) - min(d), 1.41), ('u1 s', s, .564), ('u1 z', (3.53 - m) / s, 1.60),
     ('u1 d1', d[0], 2.20), ('u1 d2', d[1], 2.12), ('u1 d3', d[2], 2.55), ('u1 d4', d[3], 3.53), ('u1 d5', d[4], 2.74), ('u1 low', min(d), 2.12), ('u1 hi', max(d), 3.53), ('u1 tot', 427.35 - 414.21, 13.14),
     ('u2 none', .99 ** 30, .740), ('u2 30', 1 - .99 ** 30, .260), ('u2 100', 1 - .99 ** 100, .634), ('u2 50y', 1 - .98 ** 30, .455), ('u2 250', 1 - .996 ** 30, .113), ('u2 c96', comb(9, 6), 84),
     ('u2 aep2', 1 / 2, .5), ('u2 aep10', 1 / 10, .1), ('u2 aep100', 1 / 100, .01), ('u2 aep500', 1 / 500, .002),
     ('u3 pf', .95 * .02 + .05 * .98, .068), ('u3 num', .95 * .02, .019), ('u3 bayes', .019 / .068, .279), ('u3 lam', lam, .0424), ('u3 yr', 1 - exp(-lam), .0415), ('u3 10', 1 - exp(-10 * lam), .346), ('u3 la', lamLA, .0305),
     ('u3 la2', 1 - .60, .4), ('u3 sf2', 1 - .72, .28),
     ('u4 E', 9 * 2 / 3, 6), ('u4 all', (2 / 3) ** 9, .0260), ('u4 p6', bp(9, 6, 2 / 3), .273), ('u4 a', (2 / 3) ** 6, .0878), ('u4 b', (1 / 3) ** 3, .0370), ('u4 p0', exp(-1), .368), ('u4 p2', 1 - 2 * exp(-1), .264),
     ('u4 sd', sqrt(9 * 2 / 3 / 3), 1.414), ('u4 g', 1 / .01, 100), ('u4 p1', 1 - exp(-1), .632), ('u4 nhc', 200 / 25, 8),
     ('u5 phi1', Phi(1), .8413), ('u5 68', Phi(1) - Phi(-1), .683), ('u5 mean', 1 / lam, 23.6), ('u5 med', log(2) / lam, 16.3), ('u5 T5', 1 / .2, 5), ('u5 T500', 1 / .002, 500), ('u5 m15', Phi(-1.5), .0668),
     ('u5 95', Phi(2) - Phi(-2), .954), ('u5 196', Phi(1.96), .975), ('u5 1000', 1 / 1000, .001),
     ('u6 se', 10 / sqrt(25), 2), ('u6 die', sd6, 1.708), ('u6 se25', sd6 / 5, .342), ('u6 n', 1.96 ** 2 * .25 / .05 ** 2, 384), ('u6 se100', sd6 / 10, .171), ('u6 mar', 1.96 * 2, 3.92), ('u6 dm', 3.5, (1 + 6) / 2),
     ('u7 marg', 2.776 * s / sqrt(5), .700), ('u7 lo', m - 2.776 * s / sqrt(5), 1.93), ('u7 hi', m + 2.776 * s / sqrt(5), 3.33), ('u7 ph', ph, .710), ('u7 seh', 1.96 * seh, .160), ('u7 plo', ph - 1.96 * seh, .55),
     ('u7 phi', ph + 1.96 * seh, .87), ('u7 n', 1.96 ** 2 * .25 / .05 ** 2, 384.2), ('u7 n124', 1.96 * sqrt(ph * (1 - ph) / 124), .080), ('u7 seh2', ph * (1 - ph), .2060),
     ('u8 t', (m - 2) / (s / sqrt(5)), 2.49), ('u8 exp', 31 / 3, 10.3), ('u8 tail', tail, 2.06e-5), ('u8 z', (ph - 1 / 3) / sqrt((1 / 3) * (2 / 3) / 31), 4.45), ('u8 71', 22 / 31, .71),
     ('u8 sum', 22 + 5 + 4, 31),
     ('u9 xm', mx, 30), ('u9 ym', my, 358.55), ('u9 b0', b0, 310.15), ('u9 b1', b1, 1.613), ('u9 r', rr, .990), ('u9 R2', rr ** 2, .979), ('u9 p25', b0 + b1 * 65, 415.0), ('u9 gap', 427.35 - (b0 + b1 * 65), 12.3),
     ('u10 ser', .99 ** 3, .9703), ('u10 par', 1 - .1 ** 2, .99), ('u10 mis', exp(-1000 / 50000), .980), ('u10 p3', 1 - .1 ** 3, .999), ('u10 mix', .9 * .99, .891), ('u10 yr', exp(-8760 / 100000), .916), ('u10 yrx', 8760 / 100000, .0876), ('u10 p95', 1 - .05 ** 2, .9975),
     ('labA m', m, 2.628), ('labA md', sorted(d)[2], 2.55), ('labA rg', max(d) - min(d), 1.41), ('labA s', s, .564), ('labA ss', ss, 1.2735),
     ('labB m', 12 * .5, 6), ('labB sd', sqrt(12 * .25), 1.732), ('labB p6', bp(12, 6, .5), .2256), ('labB c', comb(12, 6), 924), ('labB 2', 2 ** 12, 4096), ('labB m7', 12 * .7, 8.4),
     ('labC p', 1 - .99 ** 30, .260), ('labC se', sqrt(.26 * .74 / 1000), .0139), ('labC lo', .26 - 2 * .0139, .232), ('labC hi', .26 + 2 * .0139, .288), ('labC 2se', 2 * .0139, .0278),
     ('labD 1', sd6, 1.708), ('labD 25', sd6 / 5, .342), ('labD 100', sd6 / 10, .171), ('labD 35', 35 / 12, 2.9167),
     ('labE b1', b1, 1.613), ('labE b0', b0, 310.15), ('labE r', rr, .990), ('labE r60', res(0, 316.91), 6.76), ('labE r00', res(40, 369.71), -4.97), ('labE r20', res(60, 414.21), 7.27),
     ('labF s', .99 ** 3, .9703), ('labF p', 1 - .1 ** 2, .99), ('labF m', .9 * (1 - .1 ** 2), .891), ('labF e', exp(-.02), .980),
     ('mid m', exm, 8), ('mid md', sorted(ex)[2], 8), ('mid s', sqrt(sum((x - exm) ** 2 for x in ex) / 4), 3.16), ('mid fl', 1 - .96 ** 10, .335), ('mid b', .009 / (.009 + .099), .0833), ('mid b0', .8 ** 5, .328), ('mid p0', exp(-2), .135),
     ('mid b1', .9 * .01, .009), ('mid b2', .1 * .99, .099), ('mid ss', sum((x - exm) ** 2 for x in ex), 40),
     ('fin z', 1 - Phi(1.96), .025), ('fin se', 6 / sqrt(36), 1), ('fin ci', 2.131 * 4 / 4, 2.13), ('fin t', (52 - 50) / (4 / 4), 2.0), ('fin ser', .95 ** 4, .815), ('fin ex', exp(-500 / 2000), .779),
     ('x cpc', .75 + .20 + .05, 1.0), ('x cone', 95 / 25, 3.8), ('x cone2', 200 / 95, 2.105), ('x la', 1 - exp(-lamLA * 30), .60), ('x sf', 1 - exp(-lam * 30), .72), ('x gw', 1 / 3, .333), ('x pois', exp(-1) * 1, .368),
     ('c phi1', Phi(1), .8413), ('c 196', Phi(1.96), .975), ('c 2s', Phi(2) - Phi(-2), .9545), ('c 3s', Phi(3) - Phi(-3), .997), ('c 1s', Phi(1) - Phi(-1), .68), ('c 7of10', 7 / 10, .70),
     ('x u6 4x', sqrt(4), 2), ('x u7 4x', sqrt(4), 2), ('x u3 72', 1 - exp(-30 * lam), .72), ('x u1 z', (3.53 - 2.628) / .564, 1.60), ('x u2 m', 1 - .99 ** 30, .26), ('x u4 6of9', 6 / 9, 2 / 3),
     ('x u5 aep', 1 / 5, .2), ('x u7 half', .160 / 2, .080), ('x u8 d', 2.628 - 2, .628), ('x u9 R', .990 ** 2, .980), ('x u10 1', 1 - .9703, .0297), ('x labB v', 12 * .25, 3),
     ('x mid s2', 40 / 4, 10), ('x fin ci lo', 50 - 2.13, 47.87), ('x fin ci hi', 50 + 2.13, 52.13), ('x u3 sf', -log(.28), 1.273), ('x u5 ln2', log(2), .693), ('x labA d', 3.53 - 2.12, 1.41), ('x cone', 25 * 8, 200), ('x lam4', .0424 * 100, 4.24)]
    return r
