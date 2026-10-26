"""Sustainable Aviation (AERO 470): aviation and climate, efficiency metrics, aerodynamic efficiency, engine efficiency, sustainable aviation fuels, contrails and non-CO2 effects, electric and hybrid propulsion, hydrogen, operations, noise and air quality, and pathways to net zero.
Oct 25 2026, founder-approved four-year track, senior course 7 (final course in the track). Same module fields as capstone.py / avionics.py. Every number is re-computed in CHECKS() (build-courses.py --check)."""
from math import sqrt, log, log10, exp, pi
ID = 'sustain'
STATUS = 'live'
YEAR = 4
PAGE = 'Sustainable_Aviation.html'
CODE = 'AERO 470'
TITLE = 'Sustainable Aviation'
LAB_NAME = 'Sustainable aviation lab'
TAGLINE = 'Cleaner fuels, efficient aircraft and lower emissions: CO₂ accounting, efficiency metrics, wings and engines that burn less fuel, sustainable aviation fuels, contrails, batteries and hydrogen, cleaner operations, and pathways to net zero, with six labs. Free, self-paced, and tied to NASA’s Sustainable Flight National Partnership, NASA-DLR contrail research, DOE’s SAF data and EIA emission factors.'
DESC = 'Free self-study Sustainable Aviation: 10 units, worked examples, solved practice, quizzes, flashcards, 6 spreadsheet and PhET labs, practice exams, tied to NASA, DOE, EIA and EPA sources.'
ALT = 'Earth’s full disk in NASA’s Blue Marble image, showing land, ocean, ice and clouds'
_PH = 'https://phet.colorado.edu/en/simulations/'
_SFNP = ('NASA Aeronautics: Sustainable Flight National Partnership', 'https://www.nasa.gov/aeronautics/sustainable-flight-national-partnership/')
_SAF = ('U.S. DOE Alternative Fuels Data Center: Sustainable aviation fuel', 'https://afdc.energy.gov/fuels/sustainable-aviation-fuel')
_EIA = ('U.S. EIA: Carbon dioxide emissions coefficients', 'https://www.eia.gov/environment/emissions/co2_vol_mass.php')
_CON = ('NASA: NASA-DLR study finds sustainable aviation fuel can reduce contrails (2021)', 'https://www.nasa.gov/news-release/nasa-dlr-study-finds-sustainable-aviation-fuel-can-reduce-contrails/')
_EPA = ('U.S. EPA: Regulations for lead emissions from aircraft', 'https://www.epa.gov/regulations-emissions-vehicles-and-engines/regulations-lead-emissions-aircraft')
_MIT = ('MIT OpenCourseWare 16.885J Aircraft Systems Engineering (Fall 2004), Lecture 8: Environmental Factors', 'https://ocw.mit.edu/courses/16-885j-aircraft-systems-engineering-fall-2004/pages/lecture-notes/')
BANNER = ['images/earth-blue-marble-land-ocean-ice-cloud.jpg', 'images/ISS_Flyaround_2021.jpg', 'images/Pacific_Clouds_Sunset_ISS.jpg', 'images/GOES19_GOESU_KSC.jpg']
CREDITS = {'images/earth-blue-marble-land-ocean-ice-cloud.jpg': 'NASA', 'images/ISS_Flyaround_2021.jpg': 'NASA (ISS066-E-080762, Nov. 8, 2021)',
           'images/Pacific_Clouds_Sunset_ISS.jpg': 'NASA', 'images/GOES19_GOESU_KSC.jpg': 'NASA/KSC'}
ABOUT = ['This is a free self-study course outline written by Saving Planets. It is not a university course, it carries no academic credit, and no school is involved.',
         'Its scope follows a senior elective on aviation and the environment. It draws on the environmental-factors lecture in MIT 16.885J Aircraft Systems Engineering (free on MIT OpenCourseWare) and on public NASA, DOE, EIA and EPA material, which we link where it helps. None of them endorses this page.',
         'What we add: every unit ties to real work with a cited public source, every number on the page is re-computed by a checking script before it goes live, and every lab runs in a free spreadsheet or simulation.',
         'Work through it in order. Each unit has goals, key ideas, equations, step-by-step examples, practice with full answers, common mistakes, flashcards and a quiz. Your progress is saved only in this browser.']
COURSE_PLANET = ['This whole course is a planet section: DOE’s Alternative Fuels Data Center says aviation produces about 2% of all CO₂ worldwide and 12% of CO₂ from transportation, and contrails add warming beyond CO₂.',
                 'NASA’s Sustainable Flight National Partnership works toward the aviation community’s goal of net-zero carbon emissions by 2050. Each unit ends with a short, sourced section. Values that are not from a source are labeled as sample or textbook values.']
PREREQS = ['Propulsion: thrust, efficiency and TSFC.', 'Aircraft Performance: lift, drag and the Breguet range equation.',
           'Thermodynamics: energy, heating values and cycle efficiency.', 'Capstone Design or Avionics & Systems Engineering: requirements and trades.']
STUDY = ['Keep units straight: kg, gallons, liters, MJ and Wh.', 'Always ask “per what?”: per flight, per passenger-km, per kg of fuel.',
         'Separate combustion CO₂ from lifecycle CO₂.', 'Check every claimed saving against a baseline.',
         'Remember non-CO₂ effects such as contrails.', 'Do every practice problem on paper before opening the answer, and retake the quizzes a few days later.']
LAB_GEAR = ['Spreadsheet software (any free one works), or Python.', 'A computer or tablet for the free PhET Greenhouse Effect simulation.', 'The free MIT 16.885J lecture notes in a web browser.', 'A calculator.']
LAB_INTRO = ['The lab is the hands-on part of the course. Here it is free and for practice only, with no credit.',
             'Every lab runs in a spreadsheet or a free simulation, so there are no fuel, battery or hydrogen hazards. Do not handle fuels, batteries or pressurized gases for this course. Take screen breaks, sit with good posture, and keep cables out of walkways.']
SAFETY_SRC = ('OSHA: Walking-working surfaces (slip, trip and fall hazards)', 'https://www.osha.gov/walking-working-surfaces')
CONST_SRC = ('NIST: CODATA value, standard acceleration of gravity', 'https://physics.nist.gov/cgi-bin/cuu/Value?gn')
CONSTANTS = [('Standard gravity', 'g = 9.80665 m/s²'), ('Jet fuel CO₂ (EIA)', '9.75 kg CO₂ per gallon (21.50 lb)'), ('Jet fuel heating value (textbook value)', '43 MJ/kg'),
             ('Hydrogen heating value (textbook value)', '120 MJ/kg'), ('Liquid hydrogen density (textbook value)', '70.8 kg/m³'), ('Gallon', '3.785411784 L')]
REF_TITLE = 'Free texts and sources'
REF_INTRO = 'Use these free lectures, data pages and simulations alongside the course.'
PTABLE = [(_MIT[0], _MIT[1], 'Free MIT lecture notes.'), (_SFNP[0], _SFNP[1], 'NASA program.'), (_SAF[0], _SAF[1], 'DOE SAF data.'),
          (_EIA[0], _EIA[1], 'EIA emission factors.'), (_CON[0], _CON[1], 'NASA contrail study.'), ('PhET: Greenhouse Effect', _PH + 'greenhouse-effect', 'Radiation balance.')]
def _q(q, opts, ok, why):
    return {'q': q, 'opts': opts, 'ok': ok, 'why': why}
def _w(q, steps, a):
    return {'q': q, 'steps': steps, 'a': a}
def _u(i, t, wk, summ, obj, con, eqs, worked, prac, misc, quiz, cards, ptext, site, src, res):
    return {'id': i, 'title': t, 'weeks': wk, 'summary': summ, 'objectives': obj, 'concepts': con, 'eqs': eqs, 'worked': worked, 'practice': prac, 'misc': misc,
            'quiz': quiz, 'cards': cards, 'planet': {'text': ptext, 'site': site, 'src': src}, 'res': res}
UNITS = [
 _u('u1', 'Aviation and Climate: Counting CO₂', 'Week 1', 'Where aviation emissions come from, emission factors, combustion versus lifecycle CO₂, and aviation’s share of the total.',
    ['Use an emission factor to compute CO₂.', 'Convert between gallons, liters and kilograms.', 'Explain combustion versus lifecycle CO₂.', 'State aviation’s share of global CO₂.'],
    ['Burning jet fuel turns its carbon into CO₂; the mass of CO₂ is about three times the fuel mass because each carbon atom gains two oxygen atoms.',
     'The U.S. EIA gives 21.50 lb (9.75 kg) of CO₂ per gallon of jet fuel burned.',
     'Lifecycle CO₂ adds production and transport of the fuel; for sustainable fuels, growing the feedstock can absorb CO₂.',
     'DOE’s Alternative Fuels Data Center says aviation accounts for 2% of all CO₂ and 12% of transportation CO₂ worldwide.',
     'Aviation also warms the climate through non-CO₂ effects such as contrails and NOx.'],
    [('m_{CO_2}=EF\\times V_{fuel}', 'Emissions from fuel volume'), ('EF=9.75\\ \\text{kg/gal}', 'EIA jet fuel factor'), ('1\\ \\text{gal}=3.785\\ \\text{L}', 'Volume conversion'), ('\\frac{44}{12}\\approx3.67', 'CO₂-to-carbon mass ratio')],
    [_w('A flight burns 5000 gallons of jet fuel. CO₂?', ['5000 × 9.75.'], '48,750 kg (48.75 t).'),
     _w('Check EIA’s pound and kilogram values.', ['21.50 × 0.45359237.'], '9.75 kg, consistent.'),
     _w('How many liters is 5000 gallons?', ['5000 × 3.785.'], '18,927 L.')],
    [('CO₂ from 1000 gallons?', '9750 kg.'), ('Mass ratio of CO₂ to carbon?', '44/12 = 3.67.'),
     ('Aviation’s share of transport CO₂ (DOE)?', '12%.'), ('What does lifecycle add?', 'Production, transport and feedstock effects.')],
    [('CO₂ weighs less than the fuel.', 'It weighs about three times more.'), ('Aviation only emits CO₂.', 'Contrails and NOx matter too.'), ('Lifecycle and combustion CO₂ are equal.', 'They differ, especially for SAF.')],
    [_q('CO₂ from 5000 gal…', ['48,750 kg', '4875 kg', '9750 kg', '487,500 kg'], 0, '× 9.75.'), _q('EIA factor…', ['9.75 kg/gal', '3.16 kg/gal', '21.5 kg/gal', '1 kg/gal'], 0, 'EIA.'),
     _q('Aviation share of all CO₂…', ['2%', '12%', '25%', '0.2%'], 0, 'DOE.'), _q('Liters in 5000 gal…', ['18,927', '1321', '5000', '37,854'], 0, '× 3.785.')],
    [('Emission factor', 'CO₂ per unit fuel.'), ('Combustion CO₂', 'From burning.'), ('Lifecycle CO₂', 'Well-to-wake total.'), ('Non-CO₂ effects', 'Contrails, NOx, soot.'), ('Jet A', 'Standard jet fuel.'), ('t CO₂', 'Tonne of CO₂.')],
    ['The U.S. EIA lists 21.50 lb (9.75 kg) of CO₂ per gallon of jet fuel.', 'DOE’s Alternative Fuels Data Center says aviation accounts for 2% of all CO₂ worldwide and 12% of all CO₂ from transportation.'],
    [('Solutions', 'Solutions.html'), ('Earth Observation', 'Earth_Observation.html')], [_EIA, _SAF], [(_EIA[0], _EIA[1], 'EIA table.'), (_MIT[0], _MIT[1], 'Free MIT lecture.')]),
 _u('u2', 'Efficiency Metrics', 'Week 2', 'Fuel and CO₂ per passenger-kilometer, energy intensity, and how to compare aircraft fairly.',
    ['Compute fuel per passenger-km.', 'Compute CO₂ per passenger-km.', 'Apply a percentage efficiency gain.', 'Compare fairly across aircraft.'],
    ['Total emissions mislead; normalize by passengers and distance.', 'Load factor matters: empty seats raise emissions per passenger.',
     'Energy intensity (MJ per passenger-km) compares different fuels on one scale.', 'An efficiency gain lowers fuel per unit of transport, not necessarily total fuel if traffic grows.',
     'NASA’s Sustainable Flight National Partnership targets 25–30% energy-efficiency improvements in next-generation transports.'],
    [('\\frac{V_{fuel}}{n_{pax}d}', 'Fuel per passenger-km'), ('\\frac{m_{CO_2}}{n_{pax}d}', 'CO₂ per passenger-km'), ('m^\\prime=m(1-g)', 'After a fractional gain g'), ('LF=\\frac{n_{pax}}{n_{seats}}', 'Load factor')],
    [_w('5000 gallons carry 180 passengers 2000 km (sample values). Liters per passenger-km?', ['18,927/(180 × 2000).'], '0.0526 L.'),
     _w('CO₂ per passenger-km?', ['48,750/360,000.'], '0.135 kg (135 g).'),
     _w('A 25% efficiency gain on the same trip. New CO₂?', ['48,750 × 0.75.'], '36,563 kg.')],
    [('Same flight with 150 passengers: g CO₂ per pkm?', '162.5 g.'), ('Load factor, 180 of 200 seats?', '0.9.'),
     ('A 30% gain on 48,750 kg?', '34,125 kg.'), ('Why normalize?', 'To compare different trips and aircraft fairly.')],
    [('Bigger planes always emit more per passenger.', 'Often less per passenger.'), ('Efficiency cuts total emissions.', 'Only if traffic doesn’t grow faster.'), ('Seats equal passengers.', 'Use load factor.')],
    [_q('L per pkm…', ['0.0526', '0.526', '5.26', '0.00526'], 0, '18,927/360,000.'), _q('g CO₂ per pkm…', ['135', '13.5', '1350', '48.75'], 0, '48,750/360,000.'),
     _q('After 25% gain…', ['36,563 kg', '12,188 kg', '48,750 kg', '60,938 kg'], 0, '× 0.75.'), _q('SFNP target…', ['25–30%', '2–3%', '50–70%', '100%'], 0, 'NASA.')],
    [('Passenger-km', 'One passenger carried one km.'), ('Load factor', 'Passengers over seats.'), ('Energy intensity', 'MJ per pkm.'), ('Rebound', 'Growth offsetting efficiency.'), ('Baseline', 'Reference case.'), ('Normalization', 'Per-unit comparison.')],
    ['NASA says the Sustainable Flight National Partnership aims to enable 25–30% energy-efficiency improvements in next-generation transports that can use 100% sustainable aviation fuel and fly optimal trajectories.', 'This unit’s per-passenger metrics are how such gains are measured.'],
    [('Aircraft Performance', 'Aircraft_Performance.html'), ('Solutions', 'Solutions.html')], [_SFNP], [(_SFNP[0], _SFNP[1], 'NASA SFNP.'), (_MIT[0], _MIT[1], 'Free MIT lecture.')]),
 _u('u3', 'Aerodynamic Efficiency', 'Weeks 3–4', 'L/D, induced drag and aspect ratio, high-aspect-ratio and truss-braced wings, and fuel burn from the Breguet equation.',
    ['Compute fuel fraction from Breguet.', 'Show how L/D cuts fuel.', 'Compute induced drag coefficient.', 'Explain why long, slender wings save fuel.'],
    ['From Breguet, the fuel fraction is 1 − exp(−Rc/(V·L/D)).', 'Higher L/D means less fuel for the same range.',
     'Induced drag C_Di = C_L²/(πeAR) falls as aspect ratio rises.', 'Very slender wings need bracing (truss-braced designs) to stay light and stiff.',
     'NASA’s partnership centerpiece is a full-scale X-plane demonstrator testing an ultra-efficient aerodynamic design.'],
    [('\\frac{W_f}{W_i}=1-e^{-Rc/(V\\,L/D)}', 'Fuel fraction'), ('C_{D_i}=\\frac{C_L^2}{\\pi eAR}', 'Induced drag'), ('AR=b^2/S', 'Aspect ratio'), ('L/D=C_L/C_D', 'Lift-to-drag ratio')],
    [_w('3000 km at 230 m/s, c = 0.6 /h, L/D = 17 (textbook values). Fuel fraction?', ['Rc/(V L/D) = 3 × 10⁶ × 1.667 × 10⁻⁴/(230 × 17) = 0.1279.', '1 − e^(−0.1279).'], '0.120.'),
     _w('Same with L/D = 20.', ['1 − e^(−0.1087).'], '0.103: 14.2% less fuel.'),
     _w('C_Di at C_L = 0.5, e = 0.85, AR = 9?', ['0.25/(π × 0.85 × 9).'], '0.0104.')],
    [('C_Di at AR = 12?', '0.0078.'), ('At AR = 19 (truss-braced class)?', '0.0049.'),
     ('Aspect ratio for b = 36 m, S = 120 m²?', '10.8.'), ('Why brace a slender wing?', 'To keep it light and stiff.')],
    [('Drag is all friction.', 'Induced drag is large at cruise.'), ('Longer wings are free.', 'Weight and gate limits.'), ('Fuel scales linearly with L/D.', 'It follows the exponential.')],
    [_q('Fuel fraction, L/D 17…', ['0.120', '0.103', '0.128', '0.017'], 0, 'Breguet.'), _q('Fuel saved at L/D 20…', ['14.2%', '17.6%', '3%', '30%'], 0, 'Compare fractions.'),
     _q('C_Di AR 9…', ['0.0104', '0.104', '0.00104', '0.0078'], 0, 'C_L²/(πeAR).'), _q('Higher AR…', ['lowers induced drag', 'raises it', 'no effect', 'raises friction only'], 0, 'Formula.')],
    [('L/D', 'Lift-to-drag ratio.'), ('Induced drag', 'Drag due to lift.'), ('Aspect ratio', 'b²/S.'), ('Oswald factor', 'Span efficiency e.'), ('Truss-braced wing', 'Slender wing with struts.'), ('Fuel fraction', 'Fuel over takeoff weight.')],
    ['NASA says the centerpiece of its Sustainable Flight National Partnership will be a full-scale X-plane demonstrator built to test an ultra-efficient aerodynamic design, to inform the next generation of single-aisle aircraft.', 'NASA lists the demonstrator’s first flight as no earlier than late 2026.'],
    [('Aerodynamics I', 'Aerodynamics_I.html'), ('Aircraft Performance', 'Aircraft_Performance.html')], [_SFNP], [(_SFNP[0], _SFNP[1], 'NASA SFNP.'), (_MIT[0], _MIT[1], 'Free MIT lecture.')]),
 _u('u4', 'Engine Efficiency', 'Week 5', 'Thermal, propulsive and overall efficiency, bypass ratio, and advanced engine cores.',
    ['Compute propulsive efficiency.', 'Combine thermal and propulsive efficiency.', 'Explain why high bypass saves fuel.', 'Relate efficiency to TSFC.'],
    ['Overall efficiency is thermal efficiency times propulsive efficiency.', 'Propulsive efficiency 2/(1 + V_e/V₀) rises as exhaust velocity approaches flight speed.',
     'High-bypass turbofans move more air more slowly, raising propulsive efficiency.', 'Hotter, higher-pressure, compact cores raise thermal efficiency.',
     'NASA’s Hybrid Thermally Efficient Core work develops high-power-density turbine cores for next-generation transports.'],
    [('\\eta_p=\\frac{2}{1+V_e/V_0}', 'Propulsive efficiency'), ('\\eta_o=\\eta_{th}\\eta_p', 'Overall efficiency'), ('TSFC\\propto\\frac{V_0}{\\eta_o}', 'Fuel use per thrust'), ('BPR=\\dot m_{bypass}/\\dot m_{core}', 'Bypass ratio')],
    [_w('V₀ = 230 m/s, V_e = 400 m/s. η_p?', ['2/(1 + 400/230).'], '0.730.'),
     _w('Lower V_e to 300 m/s (higher bypass).', ['2/(1 + 300/230).'], '0.868.'),
     _w('With η_th = 0.5, overall efficiency at V_e = 300?', ['0.5 × 0.868.'], '0.434.')],
    [('η_p at V_e = 350 m/s?', '0.793.'), ('Overall at V_e = 400, η_th = 0.5?', '0.365.'),
     ('Fuel saving from 0.365 to 0.434 overall?', '15.9% less fuel for the same work.'), ('What is bypass ratio?', 'Bypass over core mass flow.')],
    [('Faster exhaust is more efficient.', 'It lowers propulsive efficiency.'), ('Thermal efficiency is everything.', 'Propulsive matters as much.'), ('Bypass is free.', 'Bigger fans add weight and drag.')],
    [_q('η_p at 400…', ['0.730', '0.868', '0.575', '1.0'], 0, '2/(1 + 1.739).'), _q('η_p at 300…', ['0.868', '0.730', '0.5', '0.95'], 0, '2/(1 + 1.304).'),
     _q('Overall…', ['0.434', '0.868', '0.5', '0.25'], 0, '0.5 × 0.868.'), _q('High bypass…', ['raises η_p', 'lowers η_p', 'raises V_e', 'no effect'], 0, 'Slower jet.')],
    [('Propulsive efficiency', 'Useful thrust power fraction.'), ('Thermal efficiency', 'Cycle efficiency.'), ('Overall efficiency', 'Product of both.'), ('Bypass ratio', 'Fan air over core air.'), ('TSFC', 'Fuel per thrust per time.'), ('Engine core', 'Compressor, burner, turbine.')],
    ['NASA says its Hybrid Thermally Efficient Core work is accelerating the development and demonstration of advanced turbine engine technologies in a high-power-density core for next-generation commercial transports.', 'Both efficiencies in this unit feed directly into the fuel burned per passenger.'],
    [('Propulsion', 'Propulsion.html'), ('Thermodynamics', 'Thermodynamics.html')], [_SFNP], [(_SFNP[0], _SFNP[1], 'NASA SFNP.'), (_MIT[0], _MIT[1], 'Free MIT lecture.')]),
 _u('u5', 'Sustainable Aviation Fuels', 'Weeks 6–7', 'What SAF is, production pathways, blend limits, lifecycle reductions and national goals.',
    ['Define SAF.', 'Compute blended lifecycle savings.', 'Size goal-level savings.', 'Explain blend limits.'],
    ['DOE defines SAF as an alternative fuel made from non-petroleum feedstocks that reduces air pollution from air transportation.',
     'SAF can be blended at levels between 10% and 50%, depending on feedstock and production pathway (ASTM D7566).',
     'Blended SAF works in existing aircraft and infrastructure.', 'Lifecycle savings scale with blend fraction times the SAF’s own lifecycle reduction.',
     'The SAF Grand Challenge aims for 3 billion gallons in 2030 and 35 billion in 2050 with at least 50% lifecycle reduction.'],
    [('s=b\\times r', 'Blend saving = blend × SAF reduction'), ('m_{saved}=V\\times EF\\times r', 'CO₂ saved by SAF volume'), ('b\\le0.5', 'Maximum blend (pathway-dependent)'), ('EF=9.75\\ \\text{kg/gal}', 'EIA factor')],
    [_w('A 50% blend of SAF with a 50% lifecycle reduction. Overall saving?', ['0.5 × 0.5.'], '25%.'),
     _w('3 billion gallons with a 50% reduction, using the EIA factor as the baseline (simplified).', ['3 × 10⁹ × 9.75 × 0.5.'], 'About 14.6 million tonnes CO₂ a year.'),
     _w('Same for 35 billion gallons.', ['35 × 10⁹ × 9.75 × 0.5.'], 'About 171 million tonnes.')],
    [('A 10% blend at 80% reduction?', '8%.'), ('Flights using SAF per ICAO via DOE?', 'Over 360,000 at 46 airports.'),
     ('Why the blend limit?', 'Fuel properties must meet Jet A specifications.'), ('Does SAF need new engines?', 'Blends work in existing aircraft.')],
    [('SAF has zero emissions.', 'It burns to CO₂; savings are lifecycle.'), ('Any blend works.', 'Limits depend on pathway.'), ('SAF only affects CO₂.', 'NASA-DLR found fewer contrail ice crystals.')],
    [_q('Blend saving…', ['25%', '50%', '100%', '75%'], 0, '0.5 × 0.5.'), _q('2030 savings…', ['≈ 14.6 Mt', '≈ 1.5 Mt', '≈ 146 Mt', '≈ 29 Mt'], 0, '× 9.75 × 0.5.'),
     _q('Blend range…', ['10–50%', '0–5%', '90–100%', 'unlimited'], 0, 'DOE.'), _q('2050 goal…', ['35 billion gal', '3 billion gal', '360,000 gal', '46 billion gal'], 0, 'DOE.')],
    [('SAF', 'Sustainable aviation fuel.'), ('HEFA', 'Hydroprocessed esters and fatty acids pathway.'), ('Blend limit', 'Maximum SAF share.'), ('ASTM D7566', 'Synthetic jet fuel spec.'), ('Lifecycle reduction', 'Cut vs fossil fuel.'), ('Drop-in fuel', 'Works in existing systems.')],
    ['DOE’s Alternative Fuels Data Center says over 360,000 commercial flights have used SAF at 46 airports (per ICAO), and the SAF Grand Challenge aims for 3 billion gallons in 2030 and 35 billion gallons in 2050 with at least 50% lifecycle reduction.', 'DOE notes that all three existing U.S. plants use the HEFA pathway, with alcohol-to-jet plants expected.'],
    [('Solutions', 'Solutions.html'), ('General Chemistry I', 'General_Chemistry_I.html')], [_SAF], [(_SAF[0], _SAF[1], 'DOE SAF page.'), (_EIA[0], _EIA[1], 'EIA factors.')]),
 _u('u6', 'Contrails and Non-CO₂ Effects', 'Week 8', 'How contrails form, why they warm, soot and ice crystals, and how fuels and routing reduce them.',
    ['Explain contrail formation.', 'Compute ice-crystal reductions.', 'Describe non-CO₂ warming.', 'Name mitigation options.'],
    ['Contrails form when hot, humid exhaust mixes with cold air and water condenses and freezes on soot particles.',
     'Persistent contrails can spread into cirrus that trap outgoing heat.', 'Fewer soot particles mean fewer, larger ice crystals that disappear sooner.',
     'NASA and DLR found cleaner-burning sustainable fuels produced 50%–70% fewer ice crystals at cruise.', 'Routing around ice-supersaturated air can avoid persistent contrails.'],
    [('N=EI\\times m_f', 'Ice crystals from emission index and fuel'), ('N^\\prime=N(1-r)', 'After a reduction r'), ('r\\in[0.5,0.7]', 'NASA-DLR range'), ('\\Delta T\\propto F', 'Warming scales with forcing')],
    [_w('A sample emission index of 10¹⁵ ice crystals per kg of fuel. With a 50% reduction?', ['10¹⁵ × 0.5.'], '5 × 10¹⁴ per kg.'),
     _w('With a 70% reduction?', ['10¹⁵ × 0.3.'], '3 × 10¹⁴ per kg.'),
     _w('A flight burns 15,000 kg of fuel at cruise (sample). Crystals at the 70% reduction?', ['3 × 10¹⁴ × 15,000.'], '4.5 × 10¹⁸.')],
    [('Why do contrails warm at night?', 'They trap outgoing infrared with no sunlight to reflect.'), ('What seeds contrail ice?', 'Soot and other particles.'),
     ('Reduction from 5 × 10¹⁴ to 3 × 10¹⁴?', '40%.'), ('One operational fix?', 'Route around ice-supersaturated air.')],
    [('Contrails are just water, so harmless.', 'They can add warming.'), ('All contrails persist.', 'Only in ice-supersaturated air.'), ('Only CO₂ matters.', 'Non-CO₂ effects are significant.')],
    [_q('50% reduction…', ['5 × 10¹⁴', '5 × 10¹⁵', '10¹⁴', '0'], 0, '× 0.5.'), _q('NASA-DLR range…', ['50%–70%', '5%–7%', '90%–100%', '20%'], 0, 'NASA.'),
     _q('Crystals per flight…', ['4.5 × 10¹⁸', '4.5 × 10¹⁴', '3 × 10¹⁴', '1.5 × 10¹⁹'], 0, '× 15,000.'), _q('Contrail ice forms on…', ['soot particles', 'CO₂', 'nitrogen', 'ozone'], 0, 'Nucleation.')],
    [('Contrail', 'Condensation trail.'), ('Contrail cirrus', 'Spread persistent contrails.'), ('Ice supersaturation', 'Air able to grow ice.'), ('Soot', 'Carbon particles.'), ('Emission index', 'Amount per kg of fuel.'), ('Non-CO₂ forcing', 'Warming besides CO₂.')],
    ['NASA reports that cleaner-burning jet fuels made from sustainable sources can produce 50%–70% fewer ice crystal contrails at cruising altitude, from joint NASA and DLR (German Aerospace Center) research.', 'NASA notes ice-crystal contrails can linger in the upper atmosphere for hours and affect the way Earth is heated and cooled.'],
    [('Earth Observation', 'Earth_Observation.html'), ('Heat Transfer', 'Heat_Transfer.html')], [_CON], [(_CON[0], _CON[1], 'NASA study.'), (_MIT[0], _MIT[1], 'Free MIT lecture.')]),
 _u('u7', 'Electric and Hybrid Propulsion', 'Weeks 9–10', 'Battery energy density, drivetrain efficiency, electric range, and where hybrid systems help.',
    ['Compare battery and fuel energy density.', 'Account for drivetrain efficiency.', 'Compute electric aircraft range.', 'Identify suitable missions.'],
    ['Jet fuel stores about 43 MJ/kg (11,944 Wh/kg); today’s batteries store a few hundred Wh/kg (textbook values).',
     'Electric drivetrains convert energy far more efficiently (about 90%) than turbines (about 35%), shrinking the gap (textbook values).',
     'Battery-electric range is R = (e η/g)(L/D)(m_b/m).', 'Batteries don’t get lighter as they discharge, unlike fuel.',
     'NASA says electrified aircraft propulsion offers new possibilities for reducing fuel and energy use, from small passenger aircraft to single-aisle transports.'],
    [('R=\\frac{e\\eta}{g}\\frac{L}{D}\\frac{m_b}{m}', 'Battery-electric range'), ('\\frac{e_{fuel}}{e_{batt}}', 'Energy-density ratio'), ('e=250\\ \\text{Wh/kg}=9\\times10^5\\ \\text{J/kg}', 'Sample battery'), ('1\\ \\text{Wh}=3600\\ \\text{J}', 'Conversion')],
    [_w('Jet fuel at 43 MJ/kg in Wh/kg, and ratio to a 250 Wh/kg battery?', ['43 × 10⁶/3600 = 11,944 Wh/kg.', '11,944/250.'], '47.8 times.'),
     _w('Adjust for efficiency: turbine 0.35, electric 0.9.', ['47.8 × 0.35/0.9.'], 'About 18.6 times.'),
     _w('Range with e = 250 Wh/kg, η = 0.8, L/D = 15, battery fraction 0.3.', ['9 × 10⁵ × 0.8/9.80665 × 15 × 0.3.'], 'About 330 km.')],
    [('Range if battery energy doubles to 500 Wh/kg?', 'About 661 km.'), ('250 Wh/kg in J/kg?', '9 × 10⁵.'),
     ('Why do hybrids help?', 'Electric power boosts takeoff and climb while fuel provides range.'), ('Best first missions?', 'Short regional and training flights.')],
    [('Batteries will soon equal jet fuel.', 'The gap is large even after efficiency.'), ('Electric means zero emissions.', 'It depends on the grid.'), ('Battery weight falls in flight.', 'It stays constant.')],
    [_q('Energy ratio…', ['47.8', '4.78', '478', '18.6'], 0, '11,944/250.'), _q('Efficiency-adjusted…', ['18.6', '47.8', '2.6', '100'], 0, '× 0.35/0.9.'),
     _q('Electric range…', ['≈ 330 km', '≈ 33 km', '≈ 3300 km', '≈ 660 km'], 0, 'Formula.'), _q('Doubled energy range…', ['≈ 661 km', '≈ 330 km', '≈ 1320 km', '≈ 165 km'], 0, 'Linear.')],
    [('Specific energy', 'Energy per mass.'), ('Drivetrain efficiency', 'Battery-to-shaft efficiency.'), ('Hybrid-electric', 'Fuel plus electric power.'), ('Battery fraction', 'Battery over aircraft mass.'), ('Wh/kg', 'Battery specific energy unit.'), ('Grid intensity', 'CO₂ per kWh.')],
    ['NASA says electrified aircraft propulsion offers new possibilities for reducing fuel and energy usage in aviation from small passenger aircraft to single-aisle transports, using new technologies, concepts, test aircraft and ground facilities.', 'This unit’s range equation shows why the first electric aircraft fly short routes. Energy densities here are textbook values.'],
    [('Circuits', 'Circuits.html'), ('Solutions', 'Solutions.html')], [_SFNP], [(_SFNP[0], _SFNP[1], 'NASA SFNP.'), (_MIT[0], _MIT[1], 'Free MIT lecture.')]),
 _u('u8', 'Hydrogen Aircraft', 'Week 11', 'Hydrogen’s energy per mass and volume, tank sizing, water emissions, and design trade-offs.',
    ['Compare hydrogen and jet fuel by mass and volume.', 'Size a hydrogen tank volume.', 'Compute water produced.', 'Explain design trade-offs.'],
    ['Hydrogen holds about 120 MJ/kg, 2.8 times jet fuel, but liquid hydrogen is only about 70.8 kg/m³ (textbook values).',
     'Per liter, liquid hydrogen holds about 8.5 MJ versus about 34.4 MJ for jet fuel, so tanks are about four times larger.',
     'Burning or using hydrogen in a fuel cell makes water, about 8.9 kg per kg of hydrogen, and no CO₂ at the aircraft.',
     'Cryogenic tanks are bulky and heavy, shaping the whole aircraft.', 'Green hydrogen depends on clean electricity for electrolysis.'],
    [('e_v=\\rho\\,e_m', 'Energy per volume'), ('V=\\frac{E}{e_v}', 'Tank volume'), ('m_{H_2O}=8.94\\,m_{H_2}', 'Water from hydrogen'), ('\\frac{e_{H_2}}{e_{jet}}=\\frac{120}{43}', 'Mass ratio')],
    [_w('Hydrogen vs jet fuel by mass?', ['120/43.'], '2.79 times more per kg.'),
     _w('Volumetric energy of liquid hydrogen?', ['70.8 × 120/1000.'], '8.50 MJ/L.'),
     _w('Tank-volume ratio vs jet fuel (0.8 kg/L, textbook)?', ['34.4/8.50.'], 'About 4.05 times larger.')],
    [('Water from 100 kg of hydrogen?', 'About 894 kg.'), ('Jet fuel volumetric energy?', '0.8 × 43 = 34.4 MJ/L.'),
     ('Why are hydrogen tanks heavy?', 'Insulated cryogenic walls.'), ('When is hydrogen low-carbon?', 'When made with clean energy.')],
    [('Hydrogen is light, so tanks are small.', 'Low density means big tanks.'), ('Hydrogen aircraft emit nothing.', 'They emit water vapor, which can form contrails.'), ('All hydrogen is green.', 'Most today is made from fossil gas.')],
    [_q('Mass ratio…', ['2.79', '0.36', '4.05', '120'], 0, '120/43.'), _q('MJ/L of LH₂…', ['8.50', '34.4', '120', '0.85'], 0, '70.8 × 0.12.'),
     _q('Tank ratio…', ['≈ 4', '≈ 0.25', '≈ 1', '≈ 40'], 0, '34.4/8.5.'), _q('Water per kg H₂…', ['≈ 8.9 kg', '≈ 1 kg', '≈ 18 kg', '0'], 0, '18.015/2.016.')],
    [('LH₂', 'Liquid hydrogen.'), ('Cryogenic', 'Very cold storage.'), ('Fuel cell', 'Electrochemical power source.'), ('Electrolysis', 'Splitting water with electricity.'), ('Volumetric energy', 'Energy per volume.'), ('Green hydrogen', 'Made with clean power.')],
    ['NASA’s Sustainable Flight National Partnership works across advanced vehicle technologies, efficient operations and sustainable aviation fuels; this unit adds hydrogen as a further option, where tank volume is the main design challenge.', 'Hydrogen values in this unit are textbook values, not NASA figures.'],
    [('General Chemistry I', 'General_Chemistry_I.html'), ('Thermodynamics', 'Thermodynamics.html')], [_SFNP], [(_MIT[0], _MIT[1], 'Free MIT lecture.'), (_SFNP[0], _SFNP[1], 'NASA SFNP.')]),
 _u('u9', 'Operations, Noise and Air Quality', 'Weeks 12–13', 'Efficient taxi and trajectories, decibel arithmetic, airport noise, local air quality and leaded aviation gasoline.',
    ['Estimate taxi fuel savings.', 'Add sound levels in decibels.', 'Apply the inverse-square law.', 'Explain the leaded-fuel issue.'],
    ['Operations matter: single-engine taxi, continuous descents and optimal trajectories cut fuel with today’s aircraft.',
     'Decibels add logarithmically: two equal sources are 3 dB louder, not twice the number.', 'In open air, sound level drops about 6 dB per doubling of distance.',
     'Engine NOx, particles and CO affect air quality near airports.', 'EPA says most aircraft using leaded fuel are piston-engine aircraft carrying 2–10 passengers; commercial jets don’t use leaded fuel.'],
    [('L=10\\log_{10}\\sum10^{L_i/10}', 'Adding sound levels'), ('\\Delta L=20\\log_{10}(r_2/r_1)', 'Spherical spreading'), ('m_f=\\dot m_ft', 'Fuel used'), ('m_{CO_2}=3.16\\,m_f', 'CO₂ per kg fuel (textbook)')],
    [_w('Two 80 dB sources together?', ['10 log₁₀(2 × 10⁸).'], '83.0 dB.'),
     _w('Level drop from doubling distance?', ['20 log₁₀ 2.'], '6.02 dB.'),
     _w('Taxi 10 minutes on one engine instead of two at 0.1 kg/s each (sample). Fuel and CO₂ saved?', ['0.1 × 600 = 60 kg.', '60 × 3.16.'], '60 kg of fuel, about 190 kg of CO₂.')],
    [('Ten equal 70 dB sources?', '80 dB.'), ('Drop when distance quadruples?', '12.0 dB.'),
     ('Fuel for two engines over 10 minutes?', '120 kg.'), ('Which aircraft use leaded fuel (EPA)?', 'Mostly piston-engine aircraft.')],
    [('Decibels add linearly.', 'They add logarithmically.'), ('Operations can’t cut emissions.', 'They cut fuel today.'), ('Airliners burn leaded fuel.', 'EPA says commercial jets don’t.')],
    [_q('Two 80 dB…', ['83.0 dB', '160 dB', '80 dB', '86 dB'], 0, '+3 dB.'), _q('Doubling distance…', ['−6.02 dB', '−3 dB', '−10 dB', '−20 dB'], 0, '20 log 2.'),
     _q('CO₂ saved taxiing…', ['≈ 190 kg', '≈ 60 kg', '≈ 19 kg', '≈ 600 kg'], 0, '60 × 3.16.'), _q('Leaded fuel users…', ['piston aircraft', 'airliners', 'rockets', 'helicopters only'], 0, 'EPA.')],
    [('Decibel', 'Log measure of sound.'), ('Inverse-square law', 'Intensity falls with r².'), ('Single-engine taxi', 'Taxi on one engine.'), ('Continuous descent', 'Idle descent without level-offs.'), ('NOx', 'Nitrogen oxides.'), ('Avgas', 'Aviation gasoline.')],
    ['EPA says the majority of aircraft operating on leaded fuel are piston-engine aircraft, typically carrying 2–10 passengers, and that jets used for commercial transport do not use leaded fuel.', 'EPA has issued a final determination that lead emissions from certain aircraft engines endanger public health and welfare, triggering duties for EPA and the FAA to set standards.'],
    [('Solutions', 'Solutions.html'), ('Aircraft Performance', 'Aircraft_Performance.html')], [_EPA], [(_EPA[0], _EPA[1], 'EPA page.'), (_MIT[0], _MIT[1], 'Free MIT lecture.')]),
 _u('u10', 'Pathways to Net Zero', 'Weeks 14–15', 'Traffic growth, efficiency, SAF, new aircraft and offsets combined into scenarios toward 2050.',
    ['Project traffic growth.', 'Combine reductions multiplicatively.', 'Build a simple wedge scenario.', 'Discuss policy tools.'],
    ['Emissions = traffic × energy per traffic unit × carbon per energy.', 'Growth compounds: 3% a year doubles traffic in about 24 years (sample rate).',
     'Reductions multiply: (1 − efficiency gain) × (1 − SAF lifecycle saving).', 'Remaining emissions need new aircraft, more SAF, or removals.',
     'DOE notes ICAO’s CORSIA caps net CO₂ from international aviation at 2020 levels through 2035.'],
    [('E=T\\times\\frac{MJ}{T}\\times\\frac{CO_2}{MJ}', 'Emissions identity'), ('T_n=T_0(1+g)^n', 'Traffic growth'), ('E^\\prime=E(1-a)(1-b)', 'Combined reductions'), ('n_2=\\frac{\\ln2}{\\ln(1+g)}', 'Doubling time')],
    [_w('Traffic grows 3% a year from 2026 to 2050 (sample). Growth factor?', ['1.03²⁴.'], '2.03.'),
     _w('With a 25% efficiency gain, emissions relative to today?', ['2.033 × 0.75.'], '1.52.'),
     _w('Add SAF with a 50% fleet-wide lifecycle saving.', ['1.525 × 0.5.'], '0.762, still 76% of today’s level.')],
    [('Doubling time at 3%?', '23.4 years.'), ('Saving needed to reach 0 from 0.762?', 'The full remainder: new aircraft, more SAF and removals.'),
     ('Years from 2026 to 2050?', '24.'), ('What does CORSIA cap?', 'Net international aviation CO₂ at 2020 levels through 2035.')],
    [('Reductions add.', 'They multiply.'), ('Efficiency alone reaches net zero.', 'Growth outpaces it.'), ('Offsets cut emissions at the engine.', 'They compensate elsewhere.')],
    [_q('Growth factor…', ['2.03', '1.72', '1.03', '3.0'], 0, '1.03²⁴.'), _q('With efficiency…', ['1.52', '2.03', '0.76', '1.0'], 0, '× 0.75.'),
     _q('With SAF too…', ['0.762', '0.25', '1.52', '0'], 0, '× 0.5.'), _q('Net-zero goal year…', ['2050', '2030', '2035', '2100'], 0, 'NASA.')],
    [('Net zero', 'Emissions balanced by removals.'), ('Wedge', 'Slice of a reduction plan.'), ('CORSIA', 'ICAO offsetting scheme.'), ('Traffic growth', 'Rise in passenger-km.'), ('Removal', 'Taking CO₂ from the air.'), ('Scenario', 'Consistent set of assumptions.')],
    ['NASA says its Sustainable Flight National Partnership works with industry, academia and other agencies toward the aviation community’s goal of net-zero carbon emissions by 2050.', 'DOE notes that ICAO’s CORSIA caps net CO₂ from international aviation at 2020 levels through 2035.'],
    [('Solutions', 'Solutions.html'), ('Capstone Design', 'Capstone_Design.html')], [_SFNP, _SAF], [(_SFNP[0], _SFNP[1], 'NASA SFNP.'), (_SAF[0], _SAF[1], 'DOE SAF page.')])]
def _lab(i, t, wk, goal, eq, steps, table, calc, src, planet, psrc):
    return {'id': i, 'title': t, 'week': wk, 'goal': goal, 'eq': eq, 'steps': steps, 'table': table, 'note': 'Computed sample values.', 'calc': calc,
            'safety': ['Computer only.'], 'home': ['Any spreadsheet works.'], 'sims': [src], 'planet': planet, 'planet_src': [psrc]}
LABS = [
 _lab('labA', 'Lab A: Flight CO₂ calculator', 'Week 1', 'Build a spreadsheet that turns fuel burned into CO₂ and CO₂ per passenger-km.',
      ('m=9.75V', 'EIA factor'), ['Enter fuel in gallons for three sample flights.', 'Compute CO₂ with EIA’s 9.75 kg/gal.', 'Divide by passengers × km.', 'Compare short and long flights.'],
      (['Fuel (gal)', 'CO₂ (kg)'], [['1000', '9750'], ['5000', '48,750'], ['20,000', '195,000']]), ['5000 × 9.75 = 48,750 kg.', '20,000 × 9.75 = 195,000 kg.'],
      (_EIA[0], _EIA[1]), 'EIA: 9.75 kg CO₂ per gallon of jet fuel.', _EIA),
 _lab('labB', 'Lab B: L/D and fuel burn', 'Week 4', 'See how lift-to-drag ratio changes fuel for a 3000 km trip.',
      ('W_f/W_i=1-e^{-Rc/(V\\,L/D)}', 'Fuel fraction'), ['Enter R = 3000 km, V = 230 m/s, c = 0.6 /h.', 'Compute the fuel fraction for L/D = 15, 17 and 20.', 'Compute the saving relative to L/D = 17.', 'Add aspect-ratio effects on induced drag.'],
      (['L/D', 'Fuel fraction'], [['15', '0.135'], ['17', '0.120'], ['20', '0.103']]), ['1 − e^(−0.1449) = 0.135.', '1 − e^(−0.1087) = 0.103.'],
      (_MIT[0], _MIT[1]), 'NASA’s X-plane demonstrator tests an ultra-efficient aerodynamic design.', _SFNP),
 _lab('labC', 'Lab C: Propulsive efficiency explorer', 'Week 5', 'Compute propulsive and overall efficiency across exhaust velocities.',
      ('\\eta_p=2/(1+V_e/V_0)', 'Propulsive efficiency'), ['Enter V₀ = 230 m/s and η_th = 0.5.', 'Compute η_p for V_e = 400, 350 and 300 m/s.', 'Compute overall efficiency.', 'Relate to bypass ratio.'],
      (['V_e (m/s)', 'η_p', 'η_o'], [['400', '0.730', '0.365'], ['350', '0.793', '0.397'], ['300', '0.868', '0.434']]), ['2/(1 + 350/230) = 0.793.', '0.5 × 0.793 = 0.397.'],
      (_MIT[0], _MIT[1]), 'NASA: Hybrid Thermally Efficient Core develops high-power-density turbine cores.', _SFNP),
 _lab('labD', 'Lab D: SAF blend calculator', 'Week 7', 'Compute lifecycle savings for blends and SAF reductions.',
      ('s=b\\times r', 'Blend saving'), ['Enter blends of 10%, 30% and 50%.', 'Enter a SAF lifecycle reduction of 50%, then 80%.', 'Compute the saving and CO₂ saved per 1000 gallons.', 'Compare with the Grand Challenge goals.'],
      (['Blend', 'Saving at r = 50%', 'kg CO₂ saved per 1000 gal'], [['10%', '5%', '487.5'], ['30%', '15%', '1462.5'], ['50%', '25%', '2437.5']]), ['0.3 × 0.5 = 15%.', '9750 × 0.25 = 2437.5 kg.'],
      (_SAF[0], _SAF[1]), 'DOE: SAF can be blended at 10% to 50% depending on pathway.', _SAF),
 _lab('labE', 'Lab E: Electric aircraft range', 'Week 10', 'Compute battery-electric range for several battery energy densities.',
      ('R=(e\\eta/g)(L/D)(m_b/m)', 'Electric range'), ['Enter η = 0.8, L/D = 15, battery fraction 0.3.', 'Compute range for 250, 400 and 500 Wh/kg.', 'Compare with a 300 km regional route.', 'Change the battery fraction.'],
      (['e (Wh/kg)', 'Range (km)'], [['250', '330'], ['400', '529'], ['500', '661']]), ['400 × 3600 × 0.8/9.80665 × 15 × 0.3 = 529 km.', '500 Wh/kg doubles the 250 Wh/kg range.'],
      (_MIT[0], _MIT[1]), 'NASA: electrified aircraft propulsion can cut fuel and energy use.', _SFNP),
 _lab('labF', 'Lab F: Net-zero wedge model', 'Week 14', 'Explore warming in PhET Greenhouse Effect, then build a 2026–2050 aviation scenario.',
      ('E=(1+g)^n(1-a)(1-b)', 'Scenario emissions'), ['In PhET Greenhouse Effect, add greenhouse gases and watch the temperature respond.', 'Enter 3% traffic growth for 24 years.', 'Apply a 25% efficiency gain and 50% SAF saving.', 'Find the growth rate at which the two measures hold emissions flat.'],
      (['Case', 'Emissions vs today'], [['Growth only', '2.03'], ['+ efficiency', '1.52'], ['+ SAF', '0.762']]), ['1.03²⁴ = 2.033.', '2.033 × 0.75 × 0.5 = 0.762.'],
      ('PhET: Greenhouse Effect', _PH + 'greenhouse-effect'), 'NASA: the aviation community’s goal is net-zero carbon emissions by 2050.', _SFNP)]
SCHEDULE = [(1, 'u1', 'Counting CO₂; Lab A', 'EIA'), (2, 'u2', 'Efficiency metrics', 'NASA SFNP'),
            (3, 'u3', 'L/D and induced drag', 'MIT 16.885J'), (4, 'u3', 'Breguet fuel burn; Lab B', 'NASA SFNP'),
            (5, 'u4', 'Engine efficiency; Lab C', 'MIT 16.885J'), (6, 'u5', 'SAF basics', 'DOE AFDC'),
            (7, 'u5', 'SAF lifecycle; Lab D; midterm practice', 'DOE AFDC'), (8, 'u6', 'Contrails', 'NASA-DLR'),
            (9, 'u7', 'Batteries and electric range', 'NASA SFNP'), (10, 'u7', 'Hybrid systems; Lab E', 'NASA SFNP'),
            (11, 'u8', 'Hydrogen aircraft', 'MIT 16.885J'), (12, 'u9', 'Operations', 'NASA SFNP'),
            (13, 'u9', 'Noise and air quality', 'EPA'), (14, 'u10', 'Scenarios; Lab F', 'DOE AFDC'), (15, 'u10', 'Review; final practice', 'MIT 16.885J')]
EXAMS = [('Midterm practice set (Units 1–5)', [
  ('CO₂ from 2000 gallons of jet fuel?', ['2000 × 9.75.'], '19,500 kg.'),
  ('g CO₂ per passenger-km for 19,500 kg, 150 passengers, 1000 km?', ['19,500,000/150,000.'], '130 g.'),
  ('Fuel fraction for 3000 km at L/D = 15 (Unit 3 values)?', ['1 − e^(−0.1449).'], '0.135.'),
  ('η_p for V₀ = 250, V_e = 350 m/s?', ['2/(1 + 1.4).'], '0.833.'),
  ('Saving from a 40% blend at 70% lifecycle reduction?', ['0.4 × 0.7.'], '28%.')]),
 ('Final practice set (Units 1–10)', [
  ('Ice crystals after a 60% cut from 10¹⁵ per kg?', ['10¹⁵ × 0.4.'], '4 × 10¹⁴ per kg.'),
  ('Electric range with 300 Wh/kg (Unit 7 values)?', ['330.4 × 1.2.'], 'About 396 km.'),
  ('Liquid-hydrogen volume for 1000 MJ?', ['1000/8.50.'], '118 L.'),
  ('Three equal 75 dB sources?', ['75 + 10 log₁₀ 3.'], '79.8 dB.'),
  ('Growth factor at 2% for 24 years?', ['1.02²⁴.'], '1.61.'),
  ('Emissions vs today at 2% growth, 25% efficiency, 50% SAF?', ['1.608 × 0.75 × 0.5.'], '0.603.')])]
FORMULAS = ['m_{CO_2}=9.75V_{gal},\\ m_{CO_2}=3.16m_f', '\\text{CO}_2/\\text{pkm}=m_{CO_2}/(n_{pax}d)', 'W_f/W_i=1-e^{-Rc/(V\\,L/D)},\\ C_{D_i}=C_L^2/(\\pi eAR)',
            '\\eta_p=2/(1+V_e/V_0),\\ \\eta_o=\\eta_{th}\\eta_p', 's=b\\,r', 'N=EI\\,m_f,\\ N^\\prime=N(1-r)', 'R=(e\\eta/g)(L/D)(m_b/m)', 'e_v=\\rho e_m,\\ m_{H_2O}=8.94m_{H_2}',
            'L=10\\log_{10}\\sum10^{L_i/10},\\ \\Delta L=20\\log_{10}(r_2/r_1)', 'E=(1+g)^n(1-a)(1-b)']
GLOSSARY = sorted([('Aspect ratio', 'Span squared over wing area.'), ('Avgas', 'Aviation gasoline for piston engines.'), ('Blend limit', 'Maximum SAF share in jet fuel.'), ('Contrail', 'Condensation trail of ice crystals.'),
    ('CORSIA', 'ICAO carbon offsetting scheme.'), ('Decibel', 'Logarithmic sound measure.'), ('Electrified propulsion', 'Electric or hybrid aircraft power.'), ('Emission factor', 'CO₂ per unit of fuel.'),
    ('Energy intensity', 'Energy per passenger-km.'), ('Induced drag', 'Drag caused by lift.'), ('Lifecycle emissions', 'Well-to-wake CO₂.'), ('Liquid hydrogen', 'Cryogenic hydrogen fuel.'),
    ('Load factor', 'Passengers over seats.'), ('Net zero', 'Emissions balanced by removals.'), ('Non-CO₂ effects', 'Warming from contrails, NOx and particles.'), ('Passenger-km', 'One passenger carried one km.'),
    ('Propulsive efficiency', 'Share of jet power producing thrust.'), ('SAF', 'Sustainable aviation fuel.'), ('Soot', 'Carbon particles in exhaust.'), ('Specific energy', 'Energy per unit mass.')])
RUBRIC = [('4 · Mastery', 'Accounts for CO₂ and non-CO₂ effects with correct units and baselines, combines reductions correctly, and explains trade-offs between options in plain words.'),
          ('3 · Proficient', 'Solves the practice and exam sets with minor slips and checks units.'),
          ('2 · Developing', 'Follows worked examples but mixes up combustion and lifecycle CO₂ or adds reductions instead of multiplying.'),
          ('1 · Beginning', 'Quotes savings without baselines or units; needs to revisit the units.')]
WEIGHTS = [('Practice problems', '20%'), ('Labs', '25%'), ('Midterm practice set', '25%'), ('Final practice set', '30%')]
def CHECKS():
    """(label, computed, value printed on the page). build-courses.py --check fails if any differ by more than 0.6%."""
    g0 = 9.80665; EF = 9.75; gal = 3.785411784; c = .6 / 3600
    ff = lambda LD: 1 - exp(-3e6 * c / (230 * LD))
    cdi = lambda AR: .25 / (pi * .85 * AR)
    etap = lambda ve, v0=230: 2 / (1 + ve / v0)
    rng = lambda e: e * 3600 * .8 / g0 * 15 * .3 / 1000
    db = lambda *L: 10 * log10(sum(10 ** (x / 10) for x in L))
    r = [
     ('u1 CO2', 5000 * EF, 48750), ('u1 lb', 21.50 * .45359237, 9.75), ('u1 L', 5000 * gal, 18927), ('u1 1000', 1000 * EF, 9750), ('u1 r', 44 / 12, 3.67),
     ('u2 Lpk', 5000 * gal / 360000, .0526), ('u2 g', 48750 / 360000 * 1000, 135), ('u2 25', 48750 * .75, 36563), ('u2 150', 48750 / 300000 * 1000, 162.5), ('u2 LF', 180 / 200, .9), ('u2 30', 48750 * .7, 34125),
     ('u3 x', 3e6 * c / (230 * 17), .1279), ('u3 f17', ff(17), .120), ('u3 x20', 3e6 * c / (230 * 20), .1087), ('u3 f20', ff(20), .103), ('u3 sav', (ff(17) - ff(20)) / ff(17), .142), ('u3 cdi9', cdi(9), .0104),
     ('u3 cdi12', cdi(12), .0078), ('u3 cdi19', cdi(19), .0049), ('u3 AR', 36 ** 2 / 120, 10.8), ('u3 c', c, 1.667e-4),
     ('u4 p400', etap(400), .730), ('u4 p300', etap(300), .868), ('u4 o300', .5 * etap(300), .434), ('u4 p350', etap(350), .793), ('u4 o400', .5 * etap(400), .365), ('u4 sav', 1 - .5 * etap(400) / (.5 * etap(300)), .159),
     ('u5 s', .5 * .5, .25), ('u5 30', 3e9 * EF * .5 / 1e9, 14.6), ('u5 2050', 35e9 * EF * .5 / 1e9, 171), ('u5 10', .1 * .8, .08),
     ('u6 50', 1e15 * .5, 5e14), ('u6 70', 1e15 * .3, 3e14), ('u6 fl', 3e14 * 15000, 4.5e18), ('u6 red', 1 - 3e14 / 5e14, .4),
     ('u7 Wh', 43e6 / 3600, 11944), ('u7 rat', 43e6 / 3600 / 250, 47.8), ('u7 eff', 43e6 / 3600 / 250 * .35 / .9, 18.6), ('u7 R', rng(250), 330), ('u7 R500', rng(500), 661), ('u7 J', 250 * 3600, 9e5),
     ('u8 m', 120 / 43, 2.79), ('u8 v', 70.8 * 120 / 1000, 8.50), ('u8 jet', .8 * 43, 34.4), ('u8 t', .8 * 43 / (70.8 * .12), 4.05), ('u8 w', 18.015 / 2.016, 8.94), ('u8 w100', 100 * 18.015 / 2.016, 894),
     ('u9 db', db(80, 80), 83.0), ('u9 d2', 20 * log10(2), 6.02), ('u9 f', .1 * 600, 60), ('u9 co2', 60 * 3.16, 190), ('u9 ten', db(*[70] * 10), 80), ('u9 d4', 20 * log10(4), 12.0), ('u9 two', 2 * .1 * 600, 120),
     ('u10 g', 1.03 ** 24, 2.03), ('u10 e', 1.03 ** 24 * .75, 1.52), ('u10 s', 1.03 ** 24 * .75 * .5, .762), ('u10 dbl', log(2) / log(1.03), 23.4), ('u10 y', 2050 - 2026, 24),
     ('labA 1', 1000 * EF, 9750), ('labA 5', 5000 * EF, 48750), ('labA 20', 20000 * EF, 195000),
     ('labB 15', ff(15), .135), ('labB 17', ff(17), .120), ('labB 20', ff(20), .103), ('labB x15', 3e6 * c / (230 * 15), .1449),
     ('labC p4', etap(400), .730), ('labC o4', .5 * etap(400), .365), ('labC p35', etap(350), .793), ('labC o35', .5 * etap(350), .397), ('labC p3', etap(300), .868), ('labC o3', .5 * etap(300), .434),
     ('labD 10', .1 * .5, .05), ('labD 30', .3 * .5, .15), ('labD 50', .5 * .5, .25), ('labD k10', 9750 * .05, 487.5), ('labD k30', 9750 * .15, 1462.5), ('labD k50', 9750 * .25, 2437.5),
     ('labE 250', rng(250), 330), ('labE 400', rng(400), 529), ('labE 500', rng(500), 661),
     ('labF g', 1.03 ** 24, 2.033), ('labF e', 1.03 ** 24 * .75, 1.52), ('labF s', 1.03 ** 24 * .75 * .5, .762),
     ('mid co2', 2000 * EF, 19500), ('mid g', 19500e3 / 150000, 130), ('mid ff', ff(15), .135), ('mid p', etap(350, 250), .833), ('mid s', .4 * .7, .28),
     ('fin ice', 1e15 * .4, 4e14), ('fin R', rng(300), 396), ('fin V', 1000 / 8.496, 118), ('fin db', db(75, 75, 75), 79.8), ('fin g', 1.02 ** 24, 1.61), ('fin e', 1.02 ** 24 * .75 * .5, .603),
     ('c g', g0, 9.80665), ('c EF', EF, 9.75), ('c jet', 43, 43), ('c H2', 120, 120), ('c LH2', 70.8, 70.8), ('c gal', gal, 3.785411784),
     ('x saf fl', 360000, 360000), ('x saf ap', 46, 46), ('x saf 2', 35 / 3, 11.67), ('x saf lc', .5, .5), ('x afdc', 12 / 2, 6), ('x con', .7 - .5, .2), ('x sfnp', 2050 - 2026, 24), ('x sfnp hi', 1.3, 1.3),
     ('x eia lb', 21.50, 21.5), ('x epa', 10 - 2, 8), ('x u2 r', 162.5 / 135, 1.204), ('x u3 r', cdi(9) / cdi(19), 2.11), ('x u4 r', etap(300) / etap(400), 1.189), ('x u7 r', rng(500) / rng(250), 2),
     ('x u8 r', 34.4 / 8.5, 4.05), ('x u9 r', 83.0 - 80, 3), ('x u10 r', 2.033 / .762, 2.67), ('x labA r', 195000 / 48750, 4), ('x labD r', 2437.5 / 487.5, 5), ('x labE r', 529 / 330, 1.6),
     ('y u1 t', 48750 / 1000, 48.75), ('y u2 pk', 180 * 2000, 360000), ('y u3 b', 36 ** 2, 1296), ('y u4 v', 400 / 230, 1.739), ('y u5 b', 3e9 * EF / 1e9, 29.25), ('y u6 r', 5e14 / 3e14, 1.667),
     ('y u7 s', 9e5 * .8 / g0, 73422), ('y u8 c', 120 * 1000 / 70.8 / 1000, 1.695), ('y u9 kg', 190 / 1000, .19), ('y u10 p', .762 * 100, 76.2), ('y labB d', ff(15) - ff(20), .032), ('y mid v', 350 / 250, 1.4),
     ('z u1 c', 5000 * EF / 5000, 9.75), ('z u2 kg', 48750 / 360000, .1354), ('z u3 cl', .5 ** 2, .25), ('z u3 pi', pi * .85 * 9, 24.03), ('z u4 d', 1 + 400 / 230, 2.739), ('z u4 d3', 1 + 300 / 230, 2.304),
     ('z u5 g', 35e9 * EF / 1e9, 341.25), ('z u6 r', 1 - .7, .3), ('z u7 kJ', 9e5 / 1000, 900), ('z u8 g', 70.8 * .12, 8.496), ('z u9 s', 10 ** 8 * 2, 2e8), ('z u10 l', log(1.03), .02956),
     ('z fin l', log10(3) * 10, 4.77), ('z fin r', 300 / 250, 1.2), ('z mid pk', 150 * 1000, 150000), ('z labC v', 350 / 230, 1.522), ('z labE k', 400 * 3600, 1.44e6), ('z labF g', 1.03 ** 24 - 1, 1.033)]
    r += [('w a%d' % i, 1000 * i * EF, 9750 * i) for i in (2, 3, 4, 6, 8)]
    r += [('w b%d' % L, ff(L), v) for L, v in ((16, .1270), (18, .1139), (19, .1083))]
    r += [('w c%d' % v, etap(v), e) for v, e in ((250, .958), (280, .902), (320, .837), (380, .754))]
    r += [('w d%d' % b, b / 100 * .8, b / 100 * .8) for b in (10, 20, 30, 40, 50)]
    r += [('w e%d' % e, rng(e), v) for e, v in ((300, 396), (350, 463))]
    r += [('w f%d' % n, 1.03 ** n, v) for n, v in ((10, 1.344), (20, 1.806))]
    return r
