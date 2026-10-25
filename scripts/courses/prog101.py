"""Intro to Programming for Engineers (ENGR 130): Python variables and types, control flow, functions, lists and dicts, files and CSV data, NumPy and Matplotlib, debugging and testing, algorithms and complexity, numerical simulation.
Oct 24 2026, founder-approved four-year track. Same module fields as chem110.py, plus optional 'code'/'out' on worked examples and labs (rendered by build-courses.py).
Every code listing in _S is executed by CHECKS() and its printed output must equal _OUT exactly (needs numpy + matplotlib in the Python running build-courses.py --check)."""
import math, subprocess, sys, tempfile
_S = {
    '1.1': 'mass_kg = 1100\ng = 9.81\nweight = mass_kg * g\nprint(weight)\nprint(type(mass_kg), type(weight))',
    '1.2': 'ppm_1959 = 315.98\nppm_2025 = 427.35\nrise = ppm_2025 - ppm_1959\nprint(f"CO2 rose {rise:.2f} ppm, or {rise / ppm_1959:.1%}")',
    '1.3': 'print(7 / 2, 7 // 2, 7 % 2, 2 ** 10)\nprint(0.1 + 0.2 == 0.3, abs((0.1 + 0.2) - 0.3) < 1e-9)\nprint(int("42") + 1, str(42) + "1")',
    '2.1': 'anomaly = 1.28   # NASA GISTEMP, 2024, deg C vs 1951-1980\nif anomaly >= 1.0:\n    print("at least 1.0 C above the 1951-1980 average")\nelif anomaly > 0:\n    print("warmer than average")\nelse:\n    print("at or below average")',
    '2.2': 'total = 0\nfor n in range(1, 101):\n    total += n\nprint(total)',
    '2.3': 'ppm = 427.35   # 2025 annual mean, Mauna Loa\nyear = 2025\nwhile ppm < 450:\n    ppm += 2.5\n    year += 1\nprint(year, round(ppm, 2))',
    '3.1': 'def c_to_f(c):\n    """Convert Celsius to Fahrenheit."""\n    return c * 9 / 5 + 32\n\nfor c in (-40, 0, 1.28, 100):\n    print(c, "->", round(c_to_f(c), 2))',
    '3.2': 'def stall_speed(weight_n, rho, area, cl_max=1.6):\n    return (2 * weight_n / (rho * area * cl_max)) ** 0.5\n\nprint(round(stall_speed(10791, 1.227, 16.2), 1))\nprint(round(stall_speed(10791, 0.738, 16.2), 1))',
    '3.3': 'def growth(values):\n    """Year-to-year changes of a list."""\n    return [b - a for a, b in zip(values, values[1:])]\n\nco2 = [418.53, 421.08, 424.61, 427.35]   # 2022-2025\nprint([round(d, 2) for d in growth(co2)])',
    '4.1': 'flows = [44700, 40200, 29100, 22700, 17300, 14100, 12600, 12200, 14300, 22600]\nprint(len(flows), max(flows), min(flows))\nprint(sum(flows) / len(flows))\nprint(sorted(flows)[:3])',
    '4.2': 'gistemp = {2016: 1.01, 2020: 1.01, 2023: 1.17, 2024: 1.28, 2025: 1.18}\nwarmest = max(gistemp, key=gistemp.get)\nprint(warmest, gistemp[warmest])\nprint([y for y, a in gistemp.items() if a > 1.1])',
    '4.3': 'words = "reduce reuse recycle reduce repair reduce".split()\ncounts = {}\nfor w in words:\n    counts[w] = counts.get(w, 0) + 1\nprint(counts)',
    '5.1': 'import csv, io\ntext = """year,mean,unc\n2021,416.41,0.12\n2022,418.53,0.12\n2023,421.08,0.12\n2024,424.61,0.12\n2025,427.35,0.12\n"""\nrows = list(csv.DictReader(io.StringIO(text)))\nyears = [int(r["year"]) for r in rows]\nppm = [float(r["mean"]) for r in rows]\nprint(years[0], years[-1], ppm[-1])\nprint(round((ppm[-1] - ppm[0]) / (years[-1] - years[0]), 2), "ppm per year")',
    '5.2': 'with open("flows.csv", "w") as f:\n    f.write("date,cfs\\n2025-06-01,44700\\n2025-06-02,40200\\n2025-06-03,29100\\n")\nwith open("flows.csv") as f:\n    next(f)                      # skip the header\n    for line in f:\n        date, cfs = line.strip().split(",")\n        print(date, round(int(cfs) * 0.0283168, 1), "m3/s")',
    '5.3': 'lines = ["# comment", "year,mean", "2024,424.61", "2025,bad", "2026,"]\ngood = []\nfor line in lines:\n    if line.startswith("#") or line.startswith("year"):\n        continue\n    year, value = line.split(",")\n    try:\n        good.append((int(year), float(value)))\n    except ValueError:\n        print("skipping", repr(line))\nprint(good)',
    '6.1': 'import numpy as np\nyears = np.array([2021, 2022, 2023, 2024, 2025])\nppm = np.array([416.41, 418.53, 421.08, 424.61, 427.35])\nprint(np.diff(ppm))\nprint(round(ppm.mean(), 3), round(np.diff(ppm).mean(), 3))\nslope, intercept = np.polyfit(years, ppm, 1)\nprint(round(slope, 3))',
    '6.2': 'import numpy as np\ncfs = np.array([44700, 40200, 29100, 22700, 17300, 14100, 12600, 12200, 14300, 22600])\nm3s = cfs * 0.0283168\nprint(np.round(m3s[:3], 1))\nprint(int((cfs > 20000).sum()), "days above 20,000 cfs")\nprint(round(m3s.sum() * 86400 / 1e9, 3), "km3 in 10 days")',
    '6.3': 'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nyears = [1880, 1951, 1980, 2000, 2016, 2020, 2023, 2024, 2025]\nanom = [-0.17, -0.07, 0.26, 0.39, 1.01, 1.01, 1.17, 1.28, 1.18]\nfig, ax = plt.subplots()\nax.plot(years, anom, "o-")\nax.set_xlabel("Year"); ax.set_ylabel("Anomaly (C)")\nax.set_title("NASA GISTEMP v4, selected years")\nfig.savefig("gistemp.png")\nprint(len(ax.lines[0].get_xdata()), "points saved")',
    '7.1': 'def mean(xs):\n    return sum(xs) / len(xs)\n\ntry:\n    print(mean([]))\nexcept ZeroDivisionError as e:\n    print("bug found:", e)',
    '7.2': 'def mean(xs):\n    if not xs:\n        raise ValueError("mean() of empty list")\n    return sum(xs) / len(xs)\n\nassert mean([1, 2, 3]) == 2\nassert abs(mean([0.1, 0.2]) - 0.15) < 1e-12\ntry:\n    mean([])\nexcept ValueError:\n    print("all tests passed")',
    '7.3': 'def f_to_c(f):\n    return (f - 32) * 5 / 9\n\ndef test_f_to_c():\n    assert f_to_c(32) == 0\n    assert f_to_c(212) == 100\n    assert abs(f_to_c(-40) - (-40)) < 1e-12\n\ntest_f_to_c()\nprint("ok")',
    '8.1': 'def linear_search(xs, target):\n    for i, x in enumerate(xs):\n        if x == target:\n            return i\n    return -1\n\ndef binary_search(xs, target):\n    lo, hi, steps = 0, len(xs) - 1, 0\n    while lo <= hi:\n        steps += 1\n        mid = (lo + hi) // 2\n        if xs[mid] == target:\n            return mid, steps\n        if xs[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1, steps\n\ndata = list(range(0, 2_000_000, 2))\nprint(linear_search(data, 1_999_998))\nprint(binary_search(data, 1_999_998))',
    '8.2': 'def bisect_root(f, a, b, tol=1e-6):\n    n = 0\n    while b - a > tol:\n        m = (a + b) / 2\n        if f(a) * f(m) <= 0:\n            b = m\n        else:\n            a = m\n        n += 1\n    return (a + b) / 2, n\n\nroot, n = bisect_root(lambda x: x**2 - 2, 0, 2)\nprint(round(root, 6), n)',
    '8.3': 'import math\nfor n in (10, 1_000, 1_000_000):\n    print(n, math.ceil(math.log2(n)), n * n)',
    '9.1': 'import math\nv0, angle, g, dt = 20.0, math.radians(45), 9.81, 0.001\nx, y = 0.0, 0.0\nvx, vy = v0 * math.cos(angle), v0 * math.sin(angle)\nwhile y >= 0:\n    vy -= g * dt\n    x += vx * dt\n    y += vy * dt\nprint(round(x, 2), "m simulated;", round(v0**2 / g, 2), "m exact")',
    '9.2': 'import math\nGM = 3.986e14\nr0 = 6.771e6\nx, y = r0, 0.0\nvx, vy = 0.0, math.sqrt(GM / r0)\ndt, t = 1.0, 0\nperiod = 2 * math.pi * math.sqrt(r0**3 / GM)\nwhile t < period:\n    r3 = (x * x + y * y) ** 1.5\n    vx -= GM * x / r3 * dt          # Euler-Cromer: update velocity first\n    vy -= GM * y / r3 * dt\n    x += vx * dt\n    y += vy * dt\n    t += dt\nprint(round(period / 60, 1), "min;", round(math.hypot(x, y) / 1000), "km from Earth\'s center")',
    '9.3': 'r, K, P, h = 0.5, 1000, 100.0, 1.0\nfor year in range(1, 5):\n    P += h * r * P * (1 - P / K)\n    print(year, round(P, 1))',
    'A': 'import csv, io\nimport numpy as np\ntext = """year,mean,unc\n1959,315.98,0.12\n1960,316.91,0.12\n2020,414.21,0.12\n2021,416.41,0.12\n2022,418.53,0.12\n2023,421.08,0.12\n2024,424.61,0.12\n2025,427.35,0.12\n"""\nrows = list(csv.DictReader(io.StringIO(text)))\nyr = np.array([int(r["year"]) for r in rows])\nppm = np.array([float(r["mean"]) for r in rows])\nprint(round(ppm[-1] - ppm[0], 2), "ppm since 1959")\nrecent = yr >= 2020\nslope = np.polyfit(yr[recent], ppm[recent], 1)[0]\nprint(round(slope, 2), "ppm per year, 2020-2025")',
    'B': 'import numpy as np\nyears = np.arange(2016, 2026)\nanom = np.array([1.01, 0.91, 0.85, 0.98, 1.01, 0.85, 0.89, 1.17, 1.28, 1.18])\nprint(round(anom.mean(), 3))\nprint(int(years[anom.argmax()]), anom.max())\nprint(round(np.polyfit(years, anom, 1)[0] * 10, 2), "C per decade (10-year fit)")',
    'C': 'import numpy as np\ncfs = np.array([44700, 40200, 29100, 22700, 17300, 14100, 12600, 12200, 14300, 22600])\nm3s = cfs * 0.0283168\nprint(round(m3s.mean(), 1), round(np.median(m3s), 1))\ndrops = np.diff(cfs)\nprint(int(drops.min()), "cfs biggest one-day drop")\nprint(round(m3s.sum() * 86400 / 1e6, 1), "million m3 in 10 days")',
    'D': 'import math\ndef fly(v0, deg, k=0.0, dt=0.001, g=9.81):\n    vx, vy = v0 * math.cos(math.radians(deg)), v0 * math.sin(math.radians(deg))\n    x = y = 0.0\n    while y >= 0:\n        v = math.hypot(vx, vy)\n        vx -= k * v * vx * dt\n        vy -= (g + k * v * vy) * dt\n        x += vx * dt\n        y += vy * dt\n    return x\nfor k in (0.0, 0.01, 0.05):\n    best = max(range(20, 61), key=lambda a: fly(20, a, k))\n    print(k, best, round(fly(20, best, k), 1))',
}
_OUT = {
    '1.1': "10791.0\n<class 'int'> <class 'float'>",
    '1.2': 'CO2 rose 111.37 ppm, or 35.2%',
    '1.3': '3.5 3 1 1024\nFalse True\n43 421',
    '2.1': 'at least 1.0 C above the 1951-1980 average',
    '2.2': '5050',
    '2.3': '2035 452.35',
    '3.1': '-40 -> -40.0\n0 -> 32.0\n1.28 -> 34.3\n100 -> 212.0',
    '3.2': '26.0\n33.6',
    '3.3': '[2.55, 3.53, 2.74]',
    '4.1': '10 44700 12200\n22980.0\n[12200, 12600, 14100]',
    '4.2': '2024 1.28\n[2023, 2024, 2025]',
    '4.3': "{'reduce': 3, 'reuse': 1, 'recycle': 1, 'repair': 1}",
    '5.1': '2021 2025 427.35\n2.73 ppm per year',
    '5.2': '2025-06-01 1265.8 m3/s\n2025-06-02 1138.3 m3/s\n2025-06-03 824.0 m3/s',
    '5.3': "skipping '2025,bad'\nskipping '2026,'\n[(2024, 424.61)]",
    '6.1': '[2.12 2.55 3.53 2.74]\n421.596 2.735\n2.796',
    '6.2': '[1265.8 1138.3  824. ]\n5 days above 20,000 cfs\n0.562 km3 in 10 days',
    '6.3': '9 points saved',
    '7.1': 'bug found: division by zero',
    '7.2': 'all tests passed',
    '7.3': 'ok',
    '8.1': '999999\n(999999, 20)',
    '8.2': '1.414214 21',
    '8.3': '10 4 100\n1000 10 1000000\n1000000 20 1000000000000',
    '9.1': '40.77 m simulated; 40.77 m exact',
    '9.2': "92.4 min; 6771 km from Earth's center",
    '9.3': '1 145.0\n2 207.0\n3 289.1\n4 391.8',
    'A': '111.37 ppm since 1959\n2.65 ppm per year, 2020-2025',
    'B': '1.013\n2024 1.28\n0.32 C per decade (10-year fit)',
    'C': '650.7 564.9\n-11100 cfs biggest one-day drop\n562.2 million m3 in 10 days',
    'D': '0.0 45 40.8\n0.01 43 31.4\n0.05 39 17.8',
}
ID = 'prog101'
STATUS = 'live'
YEAR = 1
PAGE = 'Intro_to_Programming.html'
CODE = 'ENGR 130'
TITLE = 'Intro to Programming for Engineers'
TAGLINE = 'Python from zero to simulations: variables, loops, functions, data files, NumPy and Matplotlib, testing, algorithms, and models of projectiles, orbits and populations, using real NOAA, NASA and USGS data. Free tools, nothing to install.'
DESC = 'Free intro to Python for engineers: control flow, functions, CSV data, NumPy, Matplotlib, testing, algorithms, simulations with NOAA, NASA, USGS data.'
ALT = 'NASA image of the International Space Station'
LAB_TITLE = 'Coding labs'
_CO2 = ('NOAA GML: Mauna Loa CO₂ annual means (CSV)', 'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.csv')
_CO2P = ('NOAA GML: Trends in atmospheric CO₂, data', 'https://gml.noaa.gov/ccgg/trends/data.html')
_GIS = ('NASA GISS: GISTEMP v4 surface temperature analysis', 'https://data.giss.nasa.gov/gistemp/')
_GISC = ('NASA GISTEMP v4 global means (CSV)', 'https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv')
_USGS = ('USGS: Potomac River near Washington, DC (Little Falls), site 01646500', 'https://waterdata.usgs.gov/monitoring-location/USGS-01646500/')
_USGSW = ('USGS Water Services (data API)', 'https://waterservices.usgs.gov/')
_COLAB = ('Google Colab (free notebooks)', 'https://colab.research.google.com/')
_JL = ('JupyterLite: Python in your browser (Pyodide)', 'https://jupyter.org/try-jupyter/lab/')
_PYO = ('Pyodide', 'https://pyodide.org/')
_TUT = ('The official Python tutorial', 'https://docs.python.org/3/tutorial/')
_CSV = ('Python docs: the csv module', 'https://docs.python.org/3/library/csv.html')
_NP = ('NumPy: the absolute basics for beginners', 'https://numpy.org/doc/stable/user/absolute_beginners.html')
_MPL = ('Matplotlib: pyplot tutorial', 'https://matplotlib.org/stable/tutorials/pyplot.html')
_PT = ('pytest documentation', 'https://docs.pytest.org/')
_MIT = ('MIT OpenCourseWare 6.100L: Introduction to CS and Programming Using Python', 'https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/')
_CS50 = ('Harvard CS50’s Introduction to Programming with Python', 'https://cs50.harvard.edu/python/')
_FISH = ('NOAA Fisheries: population assessments', 'https://www.fisheries.noaa.gov/topic/population-assessments')
BANNER = ['images/ISS_Flyaround_2021.jpg', 'images/Landsat9_Launch_KLS04_0013.jpg', 'images/Chem_Lab_KSC-20210707-PH-FMX01_0146.jpg', 'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg']
CREDITS = {'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)', 'images/Landsat9_Launch_KLS04_0013.jpg': 'NASA/Kim Shiflett (KSC-20210927-PH-KLS04_0013, Sept. 27, 2021)',
           'images/Chem_Lab_KSC-20210707-PH-FMX01_0146.jpg': 'NASA/Frank Michaux (KSC-20210707-PH-FMX01_0146)', 'images/SLS_Green_Run_Hot_Fire_MAF20210116_GR0006.jpg': 'NASA/Michael DeMocker (MAF20210116_GR0006)'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows first-year programming courses such as MIT 6.100L (formerly 6.0001), Harvard’s CS50, Stanford’s CS106A and Georgia Tech’s CS 1371 for engineers. We link to free materials throughout. None of these organizations endorse this page.',
         'What we add: every example is real Python that our build script runs before the page goes live, and its printed output must match what you see here exactly. The data comes from real public sources: NOAA’s Mauna Loa CO₂ record, NASA’s GISTEMP temperature analysis and USGS river gauges.',
         'You need nothing installed: use Google Colab or JupyterLite, which runs Python inside your browser with Pyodide. Your progress is saved only in this browser.']
COURSE_PLANET = ['Climate and environmental science runs on code. The CO₂ curve, global temperature records and river forecasts are all built by programs reading public data, and you can read the same files.',
                 'Each unit ends with a short, sourced section showing how its ideas help people and the planet.']
PREREQS = ['High-school algebra.', 'No programming experience needed.', 'Physics I and Calculus I help for the simulation unit but are not required.']
STUDY = ['Type every example yourself instead of pasting; your fingers learn syntax.', 'Predict the output before you run the code.', 'When stuck, read the error message from the bottom up.',
         'Change one thing at a time and rerun.', 'Do every practice problem before opening the answer.', 'Retake the quizzes a few days later. Spaced practice beats one long session.']
LAB_GEAR = ['A computer or tablet with a modern web browser.', 'A free Google account for Colab, or JupyterLite with no account at all.', 'Optional: Python 3 installed locally with NumPy and Matplotlib.']
LAB_INTRO = ['Four coding labs use real public data and simulation: the Mauna Loa CO₂ record, NASA’s global temperature record, a USGS river gauge, and a projectile with air drag.',
             'Each lab’s starter code runs as shown; the printed results were produced by running it. Then download the full data set and extend the analysis.']
SAFETY_SRC = _TUT
CONST_SRC = _CO2P
CONSTANTS = [('1 cubic foot per second (cfs)', '0.0283168 m³/s'), ('Seconds per day', '86,400'), ('Mauna Loa CO₂, 1959 annual mean', '315.98 ppm'), ('Mauna Loa CO₂, 2025 annual mean', '427.35 ppm'),
             ('GISTEMP 2024 anomaly (vs 1951–1980)', '1.28 °C'), ('Earth’s GM', '3.986 × 10¹⁴ m³/s²'), ('g', '9.81 m/s²')]
REF_TITLE = 'Free tools and references'
REF_INTRO = 'Run Python free in your browser and look things up here.'
PTABLE = [(_COLAB[0], _COLAB[1], 'Free notebooks with NumPy and Matplotlib preinstalled.'), (_JL[0], _JL[1], 'Python in the browser, no account, powered by Pyodide.'), (_TUT[0], _TUT[1], 'The reference tutorial.'),
          (_MIT[0], _MIT[1], 'MIT’s full intro course.'), (_CS50[0], _CS50[1], 'Harvard’s free Python course.')]

def _W(k, q, steps, a):
    return {'q': q, 'code': _S[k], 'steps': steps, 'out': _OUT[k], 'a': a}
UNITS = [
{'id': 'u1', 'title': 'Getting Started: Variables, Types & Expressions', 'weeks': 'Week 1',
 'summary': 'Run your first Python in a browser notebook, store values in variables, and compute with numbers and text.',
 'objectives': ['Open a Colab or JupyterLite notebook and run cells.', 'Use variables and the types int, float, str and bool.', 'Use arithmetic operators, including //, % and **.', 'Format output with f-strings.'],
 'concepts': ['A program is a sequence of instructions. A notebook lets you run them one cell at a time and see results immediately.',
              'A variable is a name bound to a value: mass_kg = 1100. Choose names that say what and in which units.',
              'Every value has a type. int (whole numbers), float (decimals), str (text) and bool (True/False) are the basics; type() tells you which.',
              '/ always gives a float; // is floor division; % is the remainder; ** is a power.',
              'Floats are binary approximations: 0.1 + 0.2 is not exactly 0.3, so compare floats with a tolerance.'],
 'eqs': [('W=mg', 'Example 1.1 computes a weight'), ('\\text{change}=\\frac{x_{new}-x_{old}}{x_{old}}', 'Relative change (Example 1.2)')],
 'worked': [
  _W('1.1', 'Compute the weight of a 1,100 kg aircraft and check the types.', ['mass_kg is an int; multiplying by the float g gives a float.'], '10,791 N, a float.'),
  _W('1.2', 'How much has Mauna Loa CO₂ risen from the 1959 to the 2025 annual mean (NOAA)?', ['Subtract, then divide by the starting value.', 'The f-string formats :.2f (2 decimals) and :.1% (percent).'], '111.37 ppm, a 35.2% rise.'),
  _W('1.3', 'Explore operators and float surprises.', ['7/2 = 3.5, 7//2 = 3, 7%2 = 1.', '0.1 + 0.2 == 0.3 is False; a tolerance test is True.', 'int("42") converts text to a number; str(42) + "1" joins text.'], 'Use tolerances for floats and convert types on purpose.')],
 'practice': [('What does 17 % 5 give?', '2.'), ('What type is 3 * 2.0?', 'float (6.0).'), ('Write an f-string that prints pi to 3 decimals.', 'f"{math.pi:.3f}" → 3.142 (after import math).'),
              ('Why is mass_kg a better name than m?', 'It states the quantity and its unit, preventing unit mistakes.')],
 'misc': [('= means equals.', 'In Python = assigns; == compares.'), ('0.1 + 0.2 == 0.3 is True.', 'It is False because of binary rounding.'), ('"5" + 5 gives 10.', 'It is a TypeError; convert with int("5").')],
 'quiz': [{'q': '7 // 2 =', 'opts': ['3.5', '3', '4', '1'], 'ok': 1, 'why': 'Floor division.'},
          {'q': 'type(2.0) is…', 'opts': ['int', 'float', 'str', 'bool'], 'ok': 1, 'why': 'It has a decimal point.'},
          {'q': '2 ** 10 =', 'opts': ['20', '100', '1024', '12'], 'ok': 2, 'why': 'Power.'},
          {'q': 'Assignment in Python uses…', 'opts': ['==', '=', ':=only', '->'], 'ok': 1, 'why': '= binds a name.'}],
 'cards': [('Variable', 'Name bound to a value.'), ('int / float', 'Whole number / decimal number.'), ('str', 'Text.'), ('bool', 'True or False.'), ('f-string', 'f"{x:.2f}" formatting.'), ('//, %', 'Floor division, remainder.')],
 'planet': {'text': ['The numbers in Example 1.2 come straight from NOAA’s Global Monitoring Laboratory, which publishes the Mauna Loa CO₂ record as a free CSV file. A few lines of Python turn it into the headline facts of climate science.'],
            'site': [('Calculus I', 'Calculus_I.html')], 'src': [_CO2P, _COLAB]},
 'res': [(_TUT[0], _TUT[1], 'Sections 3 and 4.'), (_COLAB[0], _COLAB[1], 'Start a notebook.'), (_JL[0], _JL[1], 'No-account option.')]},

{'id': 'u2', 'title': 'Control Flow: Conditions & Loops', 'weeks': 'Week 2',
 'summary': 'Make programs decide with if/elif/else and repeat with for and while loops.',
 'objectives': ['Write if/elif/else with comparison and boolean operators.', 'Loop over ranges and sequences with for.', 'Use while loops with a clear stopping condition.', 'Accumulate totals and counts.'],
 'concepts': ['Indentation defines blocks in Python. Four spaces per level is standard.', 'Comparisons (<, >=, ==, !=) produce booleans; combine with and, or, not.',
              'for x in sequence repeats once per item; range(a, b) gives a, a+1, …, b−1.', 'while repeats until its condition is False. Make sure something in the loop changes it, or it never ends.',
              'The accumulator pattern: start a total at 0 and add inside the loop.'],
 'eqs': [('\\sum_{n=1}^{100}n=\\frac{100\\cdot101}{2}=5050', 'Gauss’s sum checks Example 2.2'), ('x_{k+1}=x_k+\\Delta', 'A loop that steps a value')],
 'worked': [
  _W('2.1', 'Classify NASA’s 2024 global temperature anomaly.', ['1.28 ≥ 1.0, so the first branch runs and the rest are skipped.'], 'Branches are tested in order; only the first true one runs.'),
  _W('2.2', 'Add the numbers 1 to 100 with a loop.', ['range(1, 101) stops before 101.', 'total += n adds each number.'], '5,050, matching Gauss’s formula.'),
  _W('2.3', 'If CO₂ kept rising 2.5 ppm a year from the 2025 mean, when would it pass 450 ppm?', ['The loop adds 2.5 ppm and one year until ppm ≥ 450.'], 'In 2035, at 452.35 ppm under this simple constant-rate scenario (not a forecast).')],
 'practice': [('How many times does for i in range(3, 10, 2) run?', '4 times (3, 5, 7, 9).'), ('Write a loop that counts the odd numbers below 20.', 'count = sum(1 for n in range(20) if n % 2): 10.'),
              ('What is wrong with: while x < 10: print(x)', 'x never changes, so it loops forever.')],
 'misc': [('range(1, 10) includes 10.', 'It stops at 9.'), ('else after if is required.', 'It is optional.'), ('Indentation is just style.', 'In Python it defines the program’s structure.')],
 'quiz': [{'q': 'list(range(2, 6)) is…', 'opts': ['[2, 3, 4, 5, 6]', '[2, 3, 4, 5]', '[3, 4, 5, 6]', '[2, 6]'], 'ok': 1, 'why': 'Stops before 6.'},
          {'q': 'Which keyword adds another test after if?', 'opts': ['else if', 'elif', 'then', 'case'], 'ok': 1, 'why': 'elif.'},
          {'q': 'A while loop stops when…', 'opts': ['its condition is False', 'after 10 times', 'never', 'at a print'], 'ok': 0, 'why': 'Condition checked each pass.'},
          {'q': 'not (True and False) is…', 'opts': ['True', 'False', 'None', 'an error'], 'ok': 0, 'why': 'True and False is False.'}],
 'cards': [('if / elif / else', 'Choose one branch.'), ('for', 'Repeat per item.'), ('while', 'Repeat while true.'), ('range(a, b, s)', 'a up to b−1, step s.'), ('Accumulator', 'total += x in a loop.'), ('break / continue', 'Leave loop / skip to next pass.')],
 'planet': {'text': ['Thresholds like 1.0 °C or 450 ppm are exactly what monitoring programs test with if statements, flagging records and alerts automatically as new data arrives.'],
            'site': [('Physics I', 'Physics_I.html')], 'src': [_GIS, _CO2P]},
 'res': [(_TUT[0], _TUT[1], 'Section 4: control flow.'), (_MIT[0], _MIT[1], 'Lectures on branching and iteration.')]},

{'id': 'u3', 'title': 'Functions', 'weeks': 'Week 3',
 'summary': 'Package logic into reusable, testable functions with parameters, defaults and return values.',
 'objectives': ['Define functions with def, parameters and return.', 'Use default and keyword arguments.', 'Write docstrings.', 'Understand local scope.'],
 'concepts': ['A function names a piece of logic. Write it once, test it once, use it everywhere.', 'Parameters receive values; return sends a result back. A function with no return gives None.',
              'Default arguments (cl_max=1.6) make common cases short; keyword arguments make calls readable.', 'Variables created inside a function are local and vanish when it returns.',
              'A docstring (the string on the first line) documents what the function does.'],
 'eqs': [('F=\\tfrac95C+32', 'Example 3.1'), ('V_s=\\sqrt{\\frac{2W}{\\rho SC_{L,\\max}}}', 'Example 3.2, from Intro to Aerospace')],
 'worked': [
  _W('3.1', 'Write and test a Celsius-to-Fahrenheit function.', ['−40 is the same on both scales, a handy check.', 'round(…, 2) tidies the floats.'], 'A 1.28 °C anomaly is a 2.3 °F difference, but 1.28 °C as a temperature is 34.3 °F; units matter.'),
  _W('3.2', 'Turn the stall-speed formula into a function and use it at two densities.', ['cl_max has a default, so callers can omit it.', '** 0.5 is a square root.'], '26.0 m/s at sea level and 33.6 m/s at 5,000 m, matching the aerospace course.'),
  _W('3.3', 'Write a function that returns year-to-year changes of a list (Mauna Loa annual means 2022–2025).', ['zip pairs each value with the next.', 'A list comprehension builds the result.'], 'Increases of 2.55, 3.53 and 2.74 ppm.')],
 'practice': [('Write area_circle(r) and test it at r = 2.', 'return math.pi * r**2 → 12.566….'), ('What does a function without return give?', 'None.'),
              ('Why test c_to_f at −40?', 'Both scales agree there, so the expected answer is known.')],
 'misc': [('print and return are the same.', 'print shows a value; return hands it back for further use.'), ('Changing a parameter changes the caller’s variable.', 'Rebinding a parameter is local (mutable objects are an exception).'),
          ('Functions should be long and do everything.', 'Small, single-purpose functions are easier to test.')],
 'quiz': [{'q': 'Define a function with…', 'opts': ['func', 'def', 'function', 'lambda only'], 'ok': 1, 'why': 'def name(params):'},
          {'q': 'A function with no return statement returns…', 'opts': ['0', 'None', 'False', 'an error'], 'ok': 1, 'why': 'Implicit None.'},
          {'q': 'In def f(x, k=2), k is…', 'opts': ['required', 'a default argument', 'global', 'a constant'], 'ok': 1, 'why': 'Has a default.'},
          {'q': 'Variables made inside a function are…', 'opts': ['global', 'local', 'shared', 'permanent'], 'ok': 1, 'why': 'Local scope.'}],
 'cards': [('def', 'Defines a function.'), ('return', 'Sends a value back.'), ('Parameter', 'Name for an input.'), ('Default argument', 'Value used if omitted.'), ('Docstring', 'Documentation string.'), ('Scope', 'Where a name is visible.')],
 'planet': {'text': ['Climate and hydrology codes are built from small, tested functions like these, for unit conversions, rates of change and physical formulas, which is how large models stay trustworthy.'],
            'site': [('Intro to Aerospace Engineering', 'Intro_to_Aerospace_Engineering.html')], 'src': [_CO2P, _TUT]},
 'res': [(_TUT[0], _TUT[1], 'Section 4.8: defining functions.'), (_CS50[0], _CS50[1], 'Functions and variables.')]},

{'id': 'u4', 'title': 'Lists, Dictionaries & Strings', 'weeks': 'Week 4',
 'summary': 'Store collections of data: lists for sequences, dictionaries for lookups, and strings for text.',
 'objectives': ['Index, slice and modify lists.', 'Use len, sum, min, max and sorted.', 'Build and query dictionaries.', 'Split strings and count words.'],
 'concepts': ['A list holds an ordered sequence: flows[0] is the first item, flows[-1] the last, flows[2:5] a slice.', 'Lists are mutable: append, insert, remove and sort change them in place.',
              'A dictionary maps keys to values: gistemp[2024] → 1.28. Lookups are fast no matter how big it is.', 'List comprehensions build lists concisely: [x * 2 for x in xs if x > 0].',
              'Strings are sequences of characters with methods like split, strip, lower and startswith.'],
 'eqs': [('\\bar x=\\frac1n\\sum_{i=1}^n x_i', 'Mean of a list (Example 4.1)')],
 'worked': [
  _W('4.1', 'Summarize ten days of USGS daily mean flow for the Potomac at Little Falls (June 1–10, 2025, in cubic feet per second).', ['len, max and min work on any list.', 'sum/len is the mean; sorted returns a new list.'], 'Mean 22,980 cfs; range 12,200–44,700 cfs.'),
  _W('4.2', 'Find the warmest year in a dictionary of NASA GISTEMP anomalies.', ['max with key=gistemp.get compares values.', 'A comprehension filters items.'], '2024, at 1.28 °C; 2023–2025 are all above 1.1 °C.'),
  _W('4.3', 'Count words with a dictionary.', ['get(w, 0) returns 0 for a new word.'], '“reduce” appears 3 times.')],
 'practice': [('What is [10, 20, 30, 40][1:3]?', '[20, 30].'), ('How do you add 2026: 1.2 to gistemp?', 'gistemp[2026] = 1.2.'), ('Square each number in xs with a comprehension.', '[x**2 for x in xs].')],
 'misc': [('Lists start at index 1.', 'They start at 0.'), ('sorted(xs) changes xs.', 'sorted returns a new list; xs.sort() changes it.'), ('Dictionary keys can repeat.', 'Each key is unique; assigning again replaces the value.')],
 'quiz': [{'q': 'xs[-1] is…', 'opts': ['the first item', 'the last item', 'an error', 'the length'], 'ok': 1, 'why': 'Negative indices count from the end.'},
          {'q': 'len({"a": 1, "b": 2}) =', 'opts': ['1', '2', '4', '3'], 'ok': 1, 'why': 'Two keys.'},
          {'q': '"a,b,c".split(",") gives…', 'opts': ['"abc"', '["a", "b", "c"]', '("a","b","c")', '3'], 'ok': 1, 'why': 'A list of strings.'},
          {'q': 'Lists are…', 'opts': ['immutable', 'mutable', 'dictionaries', 'always sorted'], 'ok': 1, 'why': 'They can change in place.'}],
 'cards': [('List', 'Ordered, mutable sequence.'), ('Index / slice', 'xs[i], xs[a:b].'), ('Dictionary', 'Key → value map.'), ('Comprehension', '[f(x) for x in xs if cond].'), ('Tuple', 'Immutable sequence.'), ('str.split', 'Text → list of pieces.')],
 'planet': {'text': ['USGS publishes daily streamflow for thousands of river gauges. The ten numbers in Example 4.1 are real: a high-flow pulse on the Potomac receding over a week, the kind of record used for water supply and flood planning.'],
            'site': [('Rivers hub', 'Rivers.html')], 'src': [_USGS, _GIS]},
 'res': [(_TUT[0], _TUT[1], 'Section 5: data structures.'), (_USGSW[0], _USGSW[1], 'How to request USGS data.')]},

{'id': 'u5', 'title': 'Files & CSV Data', 'weeks': 'Weeks 5–6',
 'summary': 'Read and write files, parse CSV data, and handle messy rows without crashing.',
 'objectives': ['Open, read and write text files with with.', 'Parse CSV with the csv module.', 'Convert strings to numbers and handle errors with try/except.', 'Download a real dataset and analyze it.'],
 'concepts': ['with open(name) as f: opens a file and closes it automatically.', 'CSV (comma-separated values) is the most common format for public data. csv.DictReader turns each row into a dictionary keyed by the header.',
              'Everything read from a file is text: convert with int() and float().', 'Real data has comments, blanks and bad values. try/except ValueError lets you skip or log them.',
              'NOAA’s Mauna Loa annual-mean file starts with # comment lines, then year,mean,unc.'],
 'eqs': [('\\text{rate}=\\frac{x_{last}-x_{first}}{t_{last}-t_{first}}', 'Average rate of change (Example 5.1)'), ('1\\ \\text{cfs}=0.0283168\\ \\text{m}^3/\\text{s}', 'Unit conversion (Example 5.2)')],
 'worked': [
  _W('5.1', 'Parse the last five rows of NOAA’s Mauna Loa annual-mean CSV and find the average rate of rise.', ['io.StringIO lets csv read a string as if it were a file.', 'Convert the text fields to int and float.'], '2.73 ppm per year from 2021 to 2025.'),
  _W('5.2', 'Write a small CSV of USGS flows, read it back and convert to m³/s.', ['next(f) skips the header line.', 'strip removes the newline; split separates fields.'], '44,700 cfs ≈ 1,265.8 m³/s.'),
  _W('5.3', 'Read lines with comments and bad values without crashing.', ['continue skips comments and the header.', 'float("bad") and float("") raise ValueError, which is caught.'], 'Only the valid row is kept; the bad ones are reported.')],
 'practice': [('How do you read the full NOAA file in Colab?', 'Use urllib.request.urlopen(url) or download it, then skip lines starting with #.'), ('What does csv.DictReader give for each row?', 'A dict keyed by column name, with string values.'),
              ('Why use with open(...)?', 'The file is closed automatically, even if an error occurs.')],
 'misc': [('Numbers in a CSV are numbers.', 'They are read as strings until converted.'), ('Bad rows mean the dataset is useless.', 'Skip and log them, then report how many.'), ('Opening a file in "w" mode adds to it.', '"w" overwrites; "a" appends.')],
 'quiz': [{'q': 'float("3.5") gives…', 'opts': ['"3.5"', '3.5', '3', 'an error'], 'ok': 1, 'why': 'Converts text to a float.'},
          {'q': 'float("") raises…', 'opts': ['TypeError', 'ValueError', 'KeyError', 'nothing'], 'ok': 1, 'why': 'Empty string is not a number.'},
          {'q': 'The "a" file mode…', 'opts': ['overwrites', 'appends', 'reads', 'deletes'], 'ok': 1, 'why': 'Append.'},
          {'q': 'csv.DictReader keys come from…', 'opts': ['row numbers', 'the header row', 'the filename', 'random'], 'ok': 1, 'why': 'First line.'}],
 'cards': [('with open()', 'Opens and auto-closes a file.'), ('CSV', 'Comma-separated values.'), ('csv.DictReader', 'Rows as dicts.'), ('try / except', 'Handle errors.'), ('ValueError', 'Bad conversion.'), ('Mode "w" / "a"', 'Overwrite / append.')],
 'planet': {'text': ['NOAA, NASA and USGS share their measurements as free CSV files. Being able to read them yourself means you can check headlines against the source data.'],
            'site': [('Calculus II', 'Calculus_II.html')], 'src': [_CO2, _CSV]},
 'res': [(_CSV[0], _CSV[1], 'Reading and writing CSV.'), (_CO2[0], _CO2[1], 'The real file.'), (_TUT[0], _TUT[1], 'Section 7.2: files.')]},

{'id': 'u6', 'title': 'NumPy & Matplotlib', 'weeks': 'Weeks 7–8',
 'summary': 'Compute on whole arrays at once with NumPy, fit trends, and make clear plots with Matplotlib.',
 'objectives': ['Create NumPy arrays and use vectorized arithmetic.', 'Use mean, diff, boolean masks and polyfit.', 'Plot data with labeled axes and titles.', 'Save figures to files.'],
 'concepts': ['A NumPy array holds numbers of one type and does math on all of them at once: cfs * 0.0283168 converts every value.',
              'np.diff gives successive differences; a boolean mask like cfs > 20000 selects or counts values.', 'np.polyfit(x, y, 1) fits a straight line and returns slope and intercept.',
              'Matplotlib’s pyplot draws figures: fig, ax = plt.subplots(); ax.plot(x, y); label axes with units; fig.savefig saves the image.',
              'A good plot has labeled axes with units, a title and a cited data source.'],
 'eqs': [('y\\approx mx+b', 'Least-squares line from np.polyfit'), ('V=\\sum Q_i\\,\\Delta t', 'Volume from daily flows (Example 6.2)')],
 'worked': [
  _W('6.1', 'Use NumPy on Mauna Loa annual means 2021–2025: differences, mean and trend.', ['np.diff gives four yearly increases.', 'polyfit’s slope is the best-fit rate.'], 'Best-fit rise ≈ 2.80 ppm per year over 2021–2025.'),
  _W('6.2', 'Convert ten days of Potomac flow to m³/s, count high-flow days and find the total volume.', ['Multiply the whole array at once.', '(cfs > 20000).sum() counts True values.', 'Sum of m³/s × 86,400 s per day.'], 'Five days above 20,000 cfs; about 0.56 km³ of water passed in ten days.'),
  _W('6.3', 'Plot selected NASA GISTEMP annual anomalies and save the figure.', ['matplotlib.use("Agg") lets code save images without a screen (Colab shows plots inline anyway).', 'Label axes and title; save with savefig.'], 'A saved line plot of 9 points; open gistemp.png to see it.')],
 'practice': [('np.array([1, 2, 3]) * 2 gives?', 'array([2, 4, 6]).'), ('How do you select values above 1.0 in an array a?', 'a[a > 1.0].'), ('Which call adds an axis label?', 'ax.set_xlabel("Year").')],
 'misc': [('NumPy arrays and lists add the same way.', '[1, 2] + [3, 4] concatenates; arrays add elementwise.'), ('A fitted line proves a cause.', 'It summarizes a trend; causes need physical understanding.'), ('Plots without units are fine.', 'Always label units and cite the source.')],
 'quiz': [{'q': 'np.diff([1, 4, 9]) =', 'opts': ['[3, 5]', '[1, 4, 9]', '[0, 3, 5]', '14'], 'ok': 0, 'why': 'Successive differences.'},
          {'q': 'np.polyfit(x, y, 1) returns…', 'opts': ['the mean', 'slope and intercept', 'a plot', 'the max'], 'ok': 1, 'why': 'Degree-1 fit.'},
          {'q': '(a > 0).sum() counts…', 'opts': ['positive values', 'all values', 'zeros', 'nothing'], 'ok': 0, 'why': 'True counts as 1.'},
          {'q': 'fig.savefig("x.png")…', 'opts': ['prints', 'saves the figure', 'deletes it', 'shows code'], 'ok': 1, 'why': 'Writes an image file.'}],
 'cards': [('np.array', 'Fast numeric array.'), ('Vectorized', 'Math on whole arrays.'), ('Boolean mask', 'a[a > x].'), ('np.polyfit', 'Least-squares polynomial fit.'), ('plt.subplots', 'Make a figure and axes.'), ('savefig', 'Save a plot.')],
 'planet': {'text': ['NASA’s GISTEMP analysis is published with its data so anyone can reproduce the global temperature record. Plotting it yourself, with labeled units and the source, is the honest way to share climate facts.'],
            'site': [('Climate data on this site: CO2M', 'CO2M.html')], 'src': [_GIS, _NP]},
 'res': [(_NP[0], _NP[1], 'Arrays for beginners.'), (_MPL[0], _MPL[1], 'Plotting basics.'), (_GISC[0], _GISC[1], 'The real data.')]},

{'id': 'u7', 'title': 'Debugging & Testing', 'weeks': 'Week 9',
 'summary': 'Find bugs systematically, read tracebacks, and write tests that catch mistakes before they matter.',
 'objectives': ['Read a traceback and locate the failing line.', 'Use print and assertions to narrow down bugs.', 'Raise clear errors for bad input.', 'Write unit tests with assert and pytest.'],
 'concepts': ['Read error messages from the bottom: the last line names the error type, the lines above show where it happened.',
              'Debug scientifically: form a hypothesis, test it with a small input, change one thing.', 'Edge cases (empty lists, zero, negative numbers, missing data) cause most bugs.',
              'An assert states what must be true; a failing assert stops the program at the bug.', 'Tests are small functions that check known answers; pytest runs every function named test_… automatically.'],
 'eqs': [('|x_{computed}-x_{expected}|<\\varepsilon', 'Tolerance test for floats')],
 'worked': [
  _W('7.1', 'Find the bug in a mean function called on an empty list.', ['Dividing by len([]) = 0 raises ZeroDivisionError.', 'Catching it shows the message.'], 'The function needs to handle empty input.'),
  _W('7.2', 'Fix it with a clear error and add assertion tests.', ['Raise ValueError with a message for empty input.', 'Float results are compared with a tolerance.'], 'All tests pass.'),
  _W('7.3', 'Write a pytest-style test for f_to_c using known points.', ['Known pairs: 32 °F = 0 °C, 212 °F = 100 °C, −40 = −40.', 'In a file, pytest would discover test_f_to_c automatically; here we call it.'], 'The function passes all three checks.')],
 'practice': [('What does “IndexError: list index out of range” usually mean?', 'You used an index ≥ len(list), often an off-by-one error.'), ('Write an assert that x is positive.', 'assert x > 0, "x must be positive".'),
              ('Name three edge cases for a function that averages data.', 'Empty list, a single value, and missing or non-numeric values.')],
 'misc': [('If it runs, it is correct.', 'Code can run and give wrong answers; test against known results.'), ('Compare floats with ==.', 'Use a tolerance.'), ('Tests are only for big projects.', 'Small tests save time from the first day.')],
 'quiz': [{'q': 'The most useful line of a traceback is usually…', 'opts': ['the first', 'the last', 'the middle', 'none'], 'ok': 1, 'why': 'It names the error.'},
          {'q': 'pytest runs functions named…', 'opts': ['run_*', 'test_*', 'check_*', 'main'], 'ok': 1, 'why': 'Convention.'},
          {'q': 'An assert that fails raises…', 'opts': ['ValueError', 'AssertionError', 'nothing', 'TypeError'], 'ok': 1, 'why': 'AssertionError.'},
          {'q': 'A good first debugging step is…', 'opts': ['rewrite everything', 'reproduce with a small input', 'add random prints everywhere', 'ignore it'], 'ok': 1, 'why': 'Shrink the problem.'}],
 'cards': [('Traceback', 'Error report; read from the bottom.'), ('Edge case', 'Unusual input at the boundary.'), ('assert', 'Stop if a condition is false.'), ('Unit test', 'Checks one function against known answers.'), ('pytest', 'Test runner.'), ('raise', 'Signal an error deliberately.')],
 'planet': {'text': ['Scientific code that informs policy must be checked. This course practices what it preaches: every code example on this page is run by our build script, and its output must match exactly before the page goes live.'],
            'site': [('Courses', 'Courses.html')], 'src': [_PT, _TUT]},
 'res': [(_PT[0], _PT[1], 'Writing tests.'), (_TUT[0], _TUT[1], 'Section 8: errors and exceptions.')]},

{'id': 'u8', 'title': 'Algorithms & Complexity', 'weeks': 'Weeks 10–11',
 'summary': 'Searching, root finding and how running time grows with input size: big-O thinking.',
 'objectives': ['Implement linear and binary search.', 'Use bisection to solve equations.', 'Estimate complexity: O(1), O(log n), O(n), O(n²).', 'Choose data structures for speed.'],
 'concepts': ['An algorithm is a precise step-by-step method. Its cost is how the number of steps grows with the input size n.',
              'Linear search checks items one by one: O(n). Binary search halves a sorted list each step: O(log n).',
              'Bisection finds a root of f on [a, b] where f changes sign by halving the interval; after n steps the interval is (b − a)/2ⁿ.',
              'Nested loops over n items are O(n²): fine for 1,000 items, hopeless for a million.', 'Dictionary and set lookups are O(1) on average, list searches O(n).'],
 'eqs': [('\\text{steps}_{binary}\\approx\\lceil\\log_2 n\\rceil', 'Binary search steps'), ('n=\\left\\lceil\\log_2\\frac{b-a}{\\text{tol}}\\right\\rceil', 'Bisection iterations')],
 'worked': [
  _W('8.1', 'Search a sorted list of one million even numbers for the last one, both ways.', ['Linear search checks 1,000,000 items to reach index 999,999.', 'Binary search needs only 20 steps.'], '20 steps versus a million: log₂(10⁶) ≈ 20.'),
  _W('8.2', 'Find √2 by bisection on x² − 2 from [0, 2] to 10⁻⁶.', ['Each step halves the interval.', '2/2²¹ < 10⁻⁶ after 21 steps.'], '1.414214 after 21 iterations.'),
  _W('8.3', 'Compare log₂ n and n² growth.', ['math.ceil(math.log2(n)) is the binary-search step count.'], 'For n = 10⁶, log₂ n is 20 while n² is 10¹².')],
 'practice': [('How many binary-search steps for 1 billion sorted items?', '⌈log₂ 10⁹⌉ = 30.'), ('What is the complexity of summing a list?', 'O(n).'),
              ('Bisection on [0, 1] to 10⁻³: how many steps?', '⌈log₂ 1,000⌉ = 10.')],
 'misc': [('Faster computers make complexity irrelevant.', 'An O(n²) method on a million items is 10¹² steps; no computer fixes that.'), ('Binary search works on any list.', 'Only on sorted data.'), ('Big-O gives exact time.', 'It describes growth, ignoring constants.')],
 'quiz': [{'q': 'Binary search is…', 'opts': ['O(n)', 'O(log n)', 'O(n²)', 'O(1)'], 'ok': 1, 'why': 'Halves each step.'},
          {'q': 'Bisection requires…', 'opts': ['a derivative', 'a sign change on [a, b]', 'sorted data', 'integers'], 'ok': 1, 'why': 'Intermediate value theorem.'},
          {'q': 'A loop inside a loop over n items is…', 'opts': ['O(n)', 'O(n²)', 'O(log n)', 'O(1)'], 'ok': 1, 'why': 'n × n.'},
          {'q': 'Average lookup in a dict is…', 'opts': ['O(n)', 'O(1)', 'O(n²)', 'O(log n)'], 'ok': 1, 'why': 'Hashing.'}],
 'cards': [('Algorithm', 'Precise step-by-step method.'), ('Big-O', 'Growth rate of cost.'), ('Linear search', 'O(n).'), ('Binary search', 'O(log n), sorted data.'), ('Bisection', 'Root finding by halving.'), ('O(n²)', 'Nested loops.')],
 'planet': {'text': ['Efficient algorithms make it possible to process the flood of Earth-observation data, from satellites to thousands of river gauges. Choosing O(n log n) over O(n²) can turn a week of computing into seconds, and less computing also means less energy.'],
            'site': [('Calculus I', 'Calculus_I.html')], 'src': [_USGSW, _MIT]},
 'res': [(_MIT[0], _MIT[1], 'Lectures on search, bisection and complexity.'), (_CS50[0], _CS50[1], 'Problem-solving practice.')]},

{'id': 'u9', 'title': 'Numerical Simulation', 'weeks': 'Weeks 12–14',
 'summary': 'Step physical models forward in time: a projectile, an orbit and a population, the core of every climate and engineering model.',
 'objectives': ['Use time-stepping (Euler and Euler-Cromer) to simulate motion.', 'Check simulations against exact answers.', 'Simulate a circular orbit and a logistic population.', 'Explore how step size affects accuracy.'],
 'concepts': ['A simulation updates the state (position, velocity, population) in small time steps dt using the rates of change: x_new = x + v·dt.',
              'Euler-Cromer updates velocity first, then position with the new velocity; it keeps orbits stable much better than plain Euler.',
              'Always validate: compare with an exact solution in a case where one exists (no air drag, circular orbit, logistic formula).',
              'Smaller dt is more accurate but slower; halve dt and see whether the answer changes.',
              'Weather and climate models are vast versions of these loops, stepping the equations of physics across a global grid.'],
 'eqs': [('v_{k+1}=v_k+a_k\\,\\Delta t,\\quad x_{k+1}=x_k+v_{k+1}\\,\\Delta t', 'Euler-Cromer step'), ('R=\\frac{v_0^2\\sin2\\theta}{g}', 'Projectile range without drag'), ('\\vec a=-\\frac{GM}{r^3}\\vec r', 'Gravity for an orbit'),
         ('P_{k+1}=P_k+h\\,rP_k\\left(1-\\frac{P_k}K\\right)', 'Logistic model, Euler step')],
 'worked': [
  _W('9.1', 'Simulate a 20 m/s projectile at 45° and compare with the exact range.', ['Step velocity, then position, until it lands.', 'Exact range = v₀² sin 90°/g.'], 'Both give 40.77 m to two decimals with dt = 0.001 s.'),
  _W('9.2', 'Simulate one orbit 400 km above Earth with 1-second steps.', ['Start at r₀ with circular speed √(GM/r₀).', 'Update velocity from gravity, then position.'], 'After one period (92.4 minutes) the spacecraft is still 6,771 km from Earth’s center: the orbit stays circular.'),
  _W('9.3', 'Step a logistic fish population (r = 0.5, K = 1,000, P₀ = 100) for four years.', ['Each year adds rP(1 − P/K).'], '145.0, 207.0, 289.1, 391.8, matching Calculus II Lab A (391.9 there, a rounding difference).')],
 'practice': [('What happens to the Example 9.1 error if dt is 0.1 s?', 'The landing is detected late, so the range error grows; try it and compare.'), ('Why does plain Euler make an orbit spiral outward?', 'It adds a little energy every step; Euler-Cromer nearly conserves it.'),
              ('Add drag −k v v⃗ to Example 9.1. What happens to the best angle?', 'It drops below 45° (Lab D).')],
 'misc': [('A simulation that runs is correct.', 'Validate against exact cases and check that halving dt barely changes the answer.'), ('Smaller dt is always better.', 'It costs time and can add rounding error; choose dt by convergence tests.'),
          ('Models predict the future exactly.', 'They are approximations whose assumptions must be stated.')],
 'quiz': [{'q': 'Euler-Cromer updates…', 'opts': ['position first', 'velocity first, then position with the new velocity', 'only velocity', 'nothing'], 'ok': 1, 'why': 'Stable for orbits.'},
          {'q': 'To validate a simulation…', 'opts': ['trust it', 'compare with an exact solution', 'make dt huge', 'remove physics'], 'ok': 1, 'why': 'Known cases.'},
          {'q': 'Exact range at 20 m/s, 45°, g = 9.81:', 'opts': ['20.4 m', '40.8 m', '81.5 m', '9.8 m'], 'ok': 1, 'why': '400/9.81.'},
          {'q': 'Halving dt and seeing no change means…', 'opts': ['a bug', 'the result has converged', 'the model is wrong', 'nothing'], 'ok': 1, 'why': 'Convergence test.'}],
 'cards': [('Time step dt', 'Size of each update.'), ('Euler method', 'x += v·dt.'), ('Euler-Cromer', 'Velocity first, then position.'), ('Validation', 'Check against known answers.'), ('Convergence', 'Answer stops changing as dt shrinks.'), ('State', 'Variables that describe the system now.')],
 'planet': {'text': ['Population models like Example 9.3 are part of how fishery scientists assess stocks and set sustainable catch limits.',
                     'The same time-stepping idea, scaled up enormously, is how weather and climate models are built.'],
            'site': [('Calculus II, Lab A', 'Calculus_II.html#labA'), ('Orbits guide', 'Orbits_Guide.html')], 'src': [_FISH, _MIT]},
 'res': [(_MIT[0], _MIT[1], 'Simulation and modeling lectures.'), (_NP[0], _NP[1], 'Vectorizing simulations.')]},
]
LABS = [
{'id': 'labA', 'title': 'Lab A: The Mauna Loa CO₂ record (NOAA)', 'week': 'Week 6',
 'goal': 'Load NOAA’s annual-mean CO₂ CSV, compute the total rise and the recent growth rate, and plot the curve.',
 'eq': ('\\text{rate}=\\text{slope of }\\text{np.polyfit(year, ppm, 1)}', 'Growth rate from a linear fit'),
 'steps': ['Run the starter code (a few real rows from NOAA’s file).', 'Download the full CSV from NOAA (link below), skip the # lines, and load all years.', 'Plot ppm against year with labeled axes and the source.', 'Fit lines to 1960–1969 and 2016–2025. How has the rate changed?'],
 'code': _S['A'], 'out': _OUT['A'],
 'table': (['Year', 'Annual mean CO₂ (ppm)'], [['1959', '315.98'], ['1960', '316.91'], ['2020', '414.21'], ['2023', '421.08'], ['2024', '424.61'], ['2025', '427.35']]),
 'note': 'Real values from NOAA GML’s Mauna Loa annual-mean file, retrieved Oct. 24, 2026.',
 'calc': ['427.35 − 315.98 = 111.37 ppm since 1959.', 'Best-fit rate 2020–2025 ≈ 2.65 ppm per year.'],
 'safety': ['None beyond normal computer use.'], 'home': ['Colab or JupyterLite in a browser.'],
 'sims': [_CO2, _COLAB],
 'planet': 'This is the record behind the Keeling Curve, the longest continuous measurement of rising CO₂.', 'planet_src': [_CO2P]},
{'id': 'labB', 'title': 'Lab B: Global temperature from NASA GISTEMP', 'week': 'Week 8',
 'goal': 'Analyze NASA’s global annual temperature anomalies: averages, the warmest year and the trend.',
 'eq': ('\\Delta T\\ \\text{per decade}=10\\times\\text{slope}', 'Trend per decade'),
 'steps': ['Run the starter code with the 2016–2025 annual (J–D) anomalies.', 'Download the full GISTEMP global CSV; skip its first title line; handle *** missing values.', 'Plot 1880–2025 and compute the trend since 1975.', 'Compare a 10-year fit with a 50-year fit and explain why short trends are noisier.'],
 'code': _S['B'], 'out': _OUT['B'],
 'table': (['Year', 'Anomaly (°C vs 1951–1980)'], [['2016', '1.01'], ['2020', '1.01'], ['2023', '1.17'], ['2024', '1.28'], ['2025', '1.18']]),
 'note': 'Real values from NASA GISTEMP v4 (GLB.Ts+dSST, J–D column), retrieved Oct. 24, 2026. NASA updates the analysis, so later downloads can differ slightly.',
 'calc': ['Mean 2016–2025 = 1.013 °C.', 'A ten-year fit gives about 0.32 °C per decade, but ten years is short and noisy; use longer periods for the long-term trend.'],
 'safety': ['None beyond normal computer use.'], 'home': ['Colab or JupyterLite.'],
 'sims': [_GISC, _GIS],
 'planet': 'Reproducing NASA’s record yourself is the best answer to “how do we know?”', 'planet_src': [_GIS]},
{'id': 'labC', 'title': 'Lab C: A river through a USGS gauge', 'week': 'Week 9',
 'goal': 'Analyze daily streamflow from the USGS Potomac River gauge at Little Falls: units, statistics, recession and volume.',
 'eq': ('V=\\sum_iQ_i\\times86{,}400\\ \\text{s}', 'Volume from daily mean flows'),
 'steps': ['Run the starter code with ten real days (June 1–10, 2025).', 'Request a full year from USGS Water Services (format=rdb) for site 01646500 and parameter 00060, and parse the tab-separated file.', 'Plot daily flow, find the peak, and compute the annual volume in km³.', 'Write tests for your unit-conversion function.'],
 'code': _S['C'], 'out': _OUT['C'],
 'table': (['Date (2025)', 'Daily mean flow (cfs)'], [['June 1', '44,700'], ['June 3', '29,100'], ['June 5', '17,300'], ['June 8', '12,200'], ['June 10', '22,600']]),
 'note': 'Real approved daily values from USGS site 01646500, retrieved Oct. 24, 2026.',
 'calc': ['Mean 650.7 m³/s, median 564.9 m³/s (the mean is pulled up by the June 1 peak).', 'The largest one-day drop was 11,100 cfs; about 562 million m³ passed in ten days.'],
 'safety': ['None beyond normal computer use.'], 'home': ['Colab or JupyterLite.'],
 'sims': [_USGS, _USGSW],
 'planet': 'River gauges like this one support drinking-water supply, flood warnings and ecosystem flows.', 'planet_src': [_USGS]},
{'id': 'labD', 'title': 'Lab D: Projectile with air drag', 'week': 'Week 14',
 'goal': 'Extend the projectile simulation with quadratic drag and find the best launch angle as drag increases.',
 'eq': ('\\vec a=-g\\hat y-k\\,|\\vec v|\\,\\vec v', 'Quadratic drag (k per meter)'),
 'steps': ['Run the starter code, which searches whole-degree angles from 20° to 60°.', 'Check that k = 0 gives 45° and the exact range.', 'Halve dt and confirm the results barely change.', 'Plot range against angle for each k.'],
 'code': _S['D'], 'out': _OUT['D'],
 'table': (['Drag k (1/m)', 'Best angle', 'Range (m)'], [['0', '45°', '40.8'], ['0.01', '43°', '31.4'], ['0.05', '39°', '17.8']]),
 'note': 'Computed by the starter code (v₀ = 20 m/s, dt = 0.001 s).',
 'calc': ['With no drag the best angle is 45° and the range 40.8 m (exact 40.77 m).', 'Drag shortens the range and lowers the best angle.'],
 'safety': ['None beyond normal computer use.'], 'home': ['Colab or JupyterLite.'],
 'sims': [_COLAB, _JL],
 'planet': 'Drag is the same physics that sets an aircraft’s fuel burn (Intro to Aerospace Engineering).', 'planet_src': []},
]
SCHEDULE = [(1, 'u1', 'Notebooks, variables, types, expressions', 'Python tutorial §3'), (2, 'u2', 'Conditions and loops', 'Python tutorial §4'), (3, 'u3', 'Functions', 'MIT 6.100L'),
            (4, 'u4', 'Lists, dictionaries, strings', 'Python tutorial §5'), (5, 'u5', 'Files and CSV', 'csv module docs'), (6, 'u5', 'Real data with errors; Lab A', 'NOAA GML'),
            (7, 'u6', 'NumPy arrays; midterm practice', 'NumPy basics'), (8, 'u6', 'Matplotlib; Lab B', 'Matplotlib pyplot'), (9, 'u7', 'Debugging and testing; Lab C', 'pytest docs'),
            (10, 'u8', 'Search and complexity', 'MIT 6.100L'), (11, 'u8', 'Bisection and numerical methods', 'MIT 6.100L'), (12, 'u9', 'Projectile simulation', 'Physics I'),
            (13, 'u9', 'Orbits and populations', 'Calculus II'), (14, 'u9', 'Drag and convergence; Lab D', 'Intro to Aerospace'), (15, 'exam', 'Review and final practice set', 'All units')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('What does print(7 // 2, 7 % 2) print?', ['Floor division and remainder.'], '3 1'),
  ('Write a loop that sums 1 to 100.', ['total = 0; for n in range(1, 101): total += n.'], '5050'),
  ('Write stall_speed(W, rho, S, cl_max=1.6) and evaluate it at 10,791 N, 1.227 kg/m³, 16.2 m².', ['(2W/(ρSC))**0.5.'], '26.0 m/s'),
  ('Given co2 = [418.53, 421.08, 424.61, 427.35], compute the year-to-year changes.', ['[b - a for a, b in zip(co2, co2[1:])].'], '[2.55, 3.53, 2.74]'),
  ('Why does float("") need try/except when reading data?', ['It raises ValueError.'], 'To skip or log bad rows instead of crashing.')]),
 ('Final practice set (all units)', [
  ('Convert 44,700 cfs to m³/s.', ['× 0.0283168.'], '≈ 1,265.8 m³/s'),
  ('How many binary-search steps for one million sorted items?', ['⌈log₂ 10⁶⌉.'], '20'),
  ('How many bisection steps take [0, 2] below 10⁻⁶?', ['2/2ⁿ < 10⁻⁶.'], '21'),
  ('Exact range of a 20 m/s projectile at 45° (g = 9.81)?', ['v₀²/g.'], '40.77 m'),
  ('Four Euler steps of P += 0.5P(1 − P/1000) from 100?', ['145.0, 207.0, 289.1, …'], '391.8'),
  ('Write a test for f_to_c.', ['assert f_to_c(212) == 100, and others.'], 'Known pairs: 32 → 0, 212 → 100, −40 → −40.')])]
FORMULAS = ['7 // 2 = 3,\\ 7\\,\\%\\,2=1,\\ 2^{10}=1024', '\\bar x=\\tfrac1n\\sum x_i', '\\text{rate}=\\Delta y/\\Delta x', 'y\\approx mx+b\\ (\\text{np.polyfit})', '1\\ \\text{cfs}=0.0283168\\ \\text{m}^3/\\text{s}',
            '\\text{binary search}\\approx\\lceil\\log_2n\\rceil', 'n_{bisect}=\\lceil\\log_2((b-a)/\\text{tol})\\rceil', 'v\\mathrel{+}=a\\,\\Delta t,\\ x\\mathrel{+}=v\\,\\Delta t', 'R=v_0^2\\sin2\\theta/g', 'P\\mathrel{+}=hrP(1-P/K)']
GLOSSARY = sorted([('Algorithm', 'Precise step-by-step method.'), ('Array', 'NumPy container for fast numeric math.'), ('Assertion', 'Check that stops the program if false.'), ('Big-O', 'How cost grows with input size.'),
    ('Bisection', 'Root finding by halving an interval.'), ('CSV', 'Comma-separated values file.'), ('Dictionary', 'Key → value mapping.'), ('Edge case', 'Unusual input at a boundary.'), ('Euler-Cromer', 'Stable time-stepping: velocity first.'),
    ('Exception', 'Error raised during execution.'), ('f-string', 'Formatted string literal.'), ('Function', 'Named, reusable block of code.'), ('List', 'Ordered, mutable sequence.'), ('Loop', 'Repeated execution.'),
    ('Notebook', 'Document of runnable code cells.'), ('Pyodide', 'Python compiled to run in a web browser.'), ('Simulation', 'Stepping a model forward in time.'), ('Traceback', 'Report of where an error happened.'),
    ('Unit test', 'Small check of one function.'), ('Variable', 'Name bound to a value.')])
RUBRIC = [('4 · Mastery', 'Writes clear, tested functions; validates results against known answers; explains choices.'), ('3 · Proficient', 'Programs work with occasional bugs found by testing.'),
          ('2 · Developing', 'Can modify examples but struggles to write from scratch.'), ('1 · Beginning', 'Copies code without understanding; revisit the unit.')]
WEIGHTS = [('Practice problems', '20%'), ('Coding labs', '35%'), ('Midterm practice set', '20%'), ('Final practice set', '25%')]

def _run(src):
    d = tempfile.mkdtemp()
    r = subprocess.run([sys.executable, '-c', src], cwd=d, capture_output=True, text=True, timeout=300)
    return r.stdout.rstrip('\n') if r.returncode == 0 else 'ERROR: ' + r.stderr[-300:]

def CHECKS():
    """(label, computed, value printed on the page). Each code listing is executed; 1 = its output matches the page exactly."""
    res = []
    for k in _S:
        got = _run(_S[k])
        if got != _OUT[k]: print(f'prog101 {k}: output differs:\n{got}\n--- page ---\n{_OUT[k]}')
        res.append((f'code {k}', 1 if got == _OUT[k] else 0, 1))
    return res + [('rise', 427.35 - 315.98, 111.37), ('pct', (427.35 - 315.98) / 315.98, .352), ('gauss', 100 * 101 / 2, 5050), ('2.5', 427.35 + 10 * 2.5, 452.35),
                  ('F', 1.28 * 9 / 5, 2.304), ('m3s', 44700 * .0283168, 1265.8), ('mean', 22980 * .0283168, 650.7), ('log', math.ceil(math.log2(1e9)), 30), ('bis', math.ceil(math.log2(1000)), 10),
                  ('range', 400 / 9.81, 40.77), ('pi3', round(math.pi, 3), 3.142), ('circle', math.pi * 4, 12.566)]
