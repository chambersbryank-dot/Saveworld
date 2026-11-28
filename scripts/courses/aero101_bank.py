# -*- coding: utf-8 -*-
"""AERO 101 check copy: topics, sources, and the start-screen strings.

The question files are built by build_aero_check.py from the six language pages.
extra() is an earlier hand-written Unit 1 draft and is not what the pages load.
"""
import json
import os

LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
G = 'https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/'

def S(en, fr, es, ar, it, he):
    return {'en': en, 'fr': fr, 'es': es, 'ar': ar, 'it': it, 'he': he}

def pick(obj, lang):
    if isinstance(obj, dict) and 'en' in obj and 'fr' in obj:
        return obj[lang]
    if isinstance(obj, list):
        return [pick(x, lang) for x in obj]
    return obj

GLENN = S('NASA Glenn', 'NASA Glenn', 'NASA Glenn', 'ناسا غلين', 'NASA Glenn', 'נאס״א גלן')
SMITH = S('Smithsonian', 'Smithsonian', 'Smithsonian', 'سميثسونيان', 'Smithsonian', 'סמיתסוניאן')
FAA = S('FAA handbook', 'manuel de la FAA', 'manual de la FAA', 'دليل FAA', 'manuale FAA', 'המדריך של ה-FAA')
NASA = S('NASA', 'NASA', 'NASA', 'ناسا', 'NASA', 'נאס״א')
EPA = S('EPA', 'EPA', 'EPA', 'EPA', 'EPA', 'EPA')
DOE = S('U.S. DOE', 'DOE des États-Unis', 'DOE de EE. UU.', 'وزارة الطاقة الأمريكية', 'DOE degli Stati Uniti', 'משרד האנרגיה של ארה״ב')
JPL = S('NASA JPL', 'NASA JPL', 'NASA JPL', 'ناسا JPL', 'NASA JPL', 'נאס״א JPL')

def mc(topic, q, opts, ok, why, src, name):
    return {'type': 'mc', 'topic': topic, 'q': q, 'opts': opts, 'ok': ok, 'why': why, 'src': src, 'srcName': name}

def tf(topic, q, ok, why, src, name):
    return {'type': 'tf', 'topic': topic, 'q': q, 'opts': [], 'ok': ok, 'why': why, 'src': src, 'srcName': name}

def num(topic, q, ok, tol, unit, why, src, name):
    return {'type': 'num', 'topic': topic, 'q': q, 'ok': ok, 'tol': tol, 'unit': unit, 'why': why, 'src': src, 'srcName': name}

def card(front, back):
    return {'f': front, 'b': back}

# Topics
FORCES = S('Forces', 'Forces', 'Fuerzas', 'القوى', 'Forze', 'כוחות')
HIST = S('History', 'Histoire', 'Historia', 'التاريخ', 'Storia', 'היסטוריה')
DESIGN = S('Design', 'Conception', 'Diseño', 'التصميم', 'Progetto', 'תכן')
AIR = S('Atmosphere', 'Atmosphère', 'Atmósfera', 'الغلاف الجوي', 'Atmosfera', 'אטמוספרה')
SOUND = S('Speed of sound', 'Vitesse du son', 'Velocidad del sonido', 'سرعة الصوت', 'Velocità del suono', 'מהירות הקול')
LIFT = S('Lift and drag', 'Portance et traînée', 'Sustentación y resistencia', 'الرفع والسحب', 'Portanza e resistenza', 'עילוי וגרר')
WING = S('Wings', 'Ailes', 'Alas', 'الأجنحة', 'Ali', 'כנפיים')
PERF = S('Performance', 'Performances', 'Actuaciones', 'الأداء', 'Prestazioni', 'ביצועים')
STAB = S('Stability', 'Stabilité', 'Estabilidad', 'الاستقرار', 'Stabilità', 'יציבות')
PROP = S('Propulsion', 'Propulsion', 'Propulsión', 'الدفع', 'Propulsione', 'הנעה')
ROCK = S('Rockets', 'Fusées', 'Cohetes', 'الصواريخ', 'Razzi', 'טילים')
ORBIT = S('Orbits', 'Orbites', 'Órbitas', 'المدارات', 'Orbite', 'מסלולים')
CLIM = S('Climate', 'Climat', 'Clima', 'المناخ', 'Clima', 'אקלים')

G4 = G + 'four-forces-on-an-airplane/'
ATM = G + 'earth-atmosphere-equation-metric/'
LEQ = G + 'lift-equation/'
DEQ = G + 'drag-equation/'
BERN = G + 'bernoulli-and-newton/'
IND = G + 'induced-drag-coefficient/'
GLIDE = G + 'glide-angle/'
TW = G + 'thrust-to-weight-ratio/'
ISP = G + 'specific-impulse/'
IEQ = G + 'ideal-rocket-equation/'
REQ = G + 'rocket-thrust-equation/'
ROT = G + 'aircraft-rotations/'
WF = 'https://airandspace.si.edu/collection-objects/1903-wright-flyer/nasm_A19610048000'
SUS = 'https://www.nasa.gov/aeronautics/sustainable-aviation/'
PHAK = 'https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak'
EPAU = 'https://www.epa.gov/regulations-emissions-vehicles-and-engines/regulations-greenhouse-gas-emissions-aircraft'
DOEU = 'https://www.energy.gov/eere/bioenergy/sustainable-aviation-fuels'
SF = 'https://science.nasa.gov/learn/basics-of-space-flight/'
FOIL = 'https://www.nasa.gov/stem-content/foilsim/'

# Existing four questions, in page order, get a topic and a source.
OLD = {
    'u1': [(FORCES, G4, GLENN), (HIST, WF, SMITH), (DESIGN, G, GLENN), (DESIGN, G, GLENN)],
    'u2': [(AIR, ATM, GLENN), (SOUND, ATM, GLENN), (AIR, ATM, GLENN), (SOUND, ATM, GLENN)],
    'u3': [(LIFT, LEQ, GLENN), (LIFT, LEQ, GLENN), (LIFT, LEQ, GLENN), (LIFT, DEQ, GLENN)],
    'u4': [(WING, IND, GLENN), (WING, IND, GLENN), (WING, IND, GLENN), (WING, IND, GLENN)],
    'u5': [(PERF, GLIDE, GLENN), (PERF, GLIDE, GLENN), (PERF, GLIDE, GLENN), (PERF, TW, GLENN)],
    'u6': [(STAB, ROT, GLENN), (STAB, ROT, GLENN), (STAB, ROT, GLENN), (STAB, ROT, GLENN)],
    'u7': [(PROP, ISP, GLENN), (PROP, ISP, GLENN), (PROP, ISP, GLENN), (PROP, ISP, GLENN)],
    'u8': [(ROCK, IEQ, GLENN), (ROCK, IEQ, GLENN), (ROCK, TW, GLENN), (ROCK, ISP, GLENN)],
    'u9': [(ORBIT, SF, JPL), (ORBIT, SF, JPL), (ORBIT, SF, JPL), (ORBIT, SF, JPL)],
    'u10': [(CLIM, SUS, NASA), (CLIM, SUS, NASA), (CLIM, SUS, NASA), (CLIM, EPAU, EPA)],
}

def extra():
    """Sixteen new questions and the added cards for each unit."""
    U = {}
    U['u1'] = {'quiz': [
        num(HIST, S(
            'The Wright Flyer’s first flight covered 36 m in 12 s. What was its average ground speed, in m/s?',
            'Le premier vol du Flyer des Wright a couvert 36 m en 12 s. Quelle était sa vitesse moyenne au sol, en m/s ?',
            'El primer vuelo del Flyer de los Wright cubrió 36 m en 12 s. ¿Cuál fue su velocidad media sobre el suelo, en m/s?',
            'غطت أول رحلة لفلاير الأخوين رايت 36 م في 12 ث. ما متوسط سرعته على الأرض، بالمتر في الثانية؟',
            'Il primo volo del Flyer dei Wright coprì 36 m in 12 s. Qual era la velocità media al suolo, in m/s?',
            'הטיסה הראשונה של הפלייר של האחים רייט עברה 36 מ׳ ב-12 שניות. מה הייתה המהירות הממוצעת על הקרקע, במ׳/ש׳?'),
            3, 0.05, 'm/s', S(
            '36 / 12 = 3 m/s over the ground. A headwind means the airspeed was higher.',
            '36 / 12 = 3 m/s au sol. Avec un vent de face, la vitesse air était plus élevée.',
            '36 / 12 = 3 m/s sobre el suelo. Con viento de frente, la velocidad respecto al aire era mayor.',
            '36 / 12 = 3 م/ث على الأرض. مع ريح معاكسة، سرعة الهواء كانت أعلى.',
            '36 / 12 = 3 m/s al suolo. Con vento contrario, la velocità rispetto all’aria era più alta.',
            '36 / 12 = 3 מ׳/ש׳ על הקרקע. ברוח נגדית, מהירות האוויר הייתה גבוהה יותר.'), WF, SMITH),
        num(FORCES, S(
            'A 1,100 kg airplane cruises level. How much lift must the wing produce, in N? Use g = 9.81 m/s².',
            'Un avion de 1 100 kg vole en palier. Quelle portance l’aile doit-elle produire, en N ? Prenez g = 9,81 m/s².',
            'Un avión de 1.100 kg vuela nivelado. ¿Cuánta sustentación debe producir el ala, en N? Usa g = 9,81 m/s².',
            'طائرة كتلتها 1100 كغ تطير أفقياً. كم رفعاً يجب أن ينتجه الجناح، بالنيوتن؟ استخدم g = 9.81 م/ث².',
            'Un aereo di 1.100 kg vola livellato. Quanta portanza deve produrre l’ala, in N? Usa g = 9,81 m/s².',
            'מטוס של 1,100 ק״ג טס ביישור. כמה עילוי הכנף חייבת לייצר, בניוטון? השתמשו ב-g = 9.81 מ׳/ש׳².'),
            10791, 50, 'N', S(
            'Level flight: lift = weight = mg = 1,100 × 9.81 = 10,791 N.',
            'En palier : portance = poids = mg = 1 100 × 9,81 = 10 791 N.',
            'En vuelo nivelado: sustentación = peso = mg = 1.100 × 9,81 = 10.791 N.',
            'في الطيران الأفقي: الرفع = الوزن = mg = 1100 × 9.81 = 10791 ن.',
            'In volo livellato: portanza = peso = mg = 1.100 × 9,81 = 10.791 N.',
            'בטיסה מיושרת: עילוי = משקל = mg = 1,100 × 9.81 = 10,791 נ׳.'), G4, GLENN),
        num(FORCES, S(
            'An airliner of mass 70,000 kg cruises level. Find its lift in N. Use g = 9.81 m/s².',
            'Un avion de ligne de 70 000 kg vole en palier. Trouvez sa portance en N. Prenez g = 9,81 m/s².',
            'Un avión de línea de 70.000 kg vuela nivelado. Halla su sustentación en N. Usa g = 9,81 m/s².',
            'طائرة ركاب كتلتها 70000 كغ تطير أفقياً. أوجد رفعها بالنيوتن. استخدم g = 9.81 م/ث².',
            'Un aereo di linea di 70.000 kg vola livellato. Trova la portanza in N. Usa g = 9,81 m/s².',
            'מטוס נוסעים במסה 70,000 ק״ג טס ביישור. מצאו את העילוי בניוטון. השתמשו ב-g = 9.81 מ׳/ש׳².'),
            686700, 500, 'N', S(
            'Lift = 70,000 × 9.81 = 686,700 N.',
            'Portance = 70 000 × 9,81 = 686 700 N.',
            'Sustentación = 70.000 × 9,81 = 686.700 N.',
            'الرفع = 70000 × 9.81 = 686700 ن.',
            'Portanza = 70.000 × 9,81 = 686.700 N.',
            'עילוי = 70,000 × 9.81 = 686,700 נ׳.'), G4, GLENN),
        num(FORCES, S(
            'In level cruise the engines give 30 kN of thrust. What is the drag, in kN?',
            'En croisière en palier, les moteurs donnent 30 kN de poussée. Quelle est la traînée, en kN ?',
            'En crucero nivelado los motores dan 30 kN de empuje. ¿Cuánto vale la resistencia, en kN?',
            'في الطيران الأفقي تعطي المحركات 30 كيلونيوتن من الدفع. كم السحب، بالكيلونيوتن؟',
            'In crociera livellata i motori danno 30 kN di spinta. Quanto vale la resistenza, in kN?',
            'בשיוט מיושר המנועים נותנים 30 קילו-ניוטון דחף. מה הגרר, בקילו-ניוטון?'),
            30, 0.01, 'kN', S(
            'In steady level flight, thrust equals drag, so the drag is 30 kN.',
            'En vol stabilisé en palier, la poussée égale la traînée, donc 30 kN.',
            'En vuelo nivelado y estable, el empuje es igual a la resistencia, así que 30 kN.',
            'في الطيران الأفقي الثابت، الدفع يساوي السحب، إذن 30 كيلونيوتن.',
            'In volo livellato e stazionario, la spinta è uguale alla resistenza, quindi 30 kN.',
            'בטיסה מיושרת ויציבה הדחף שווה לגרר, ולכן 30 קילו-ניוטון.'), G4, GLENN),
        tf(FORCES, S(
            'In steady level flight, thrust balances weight.',
            'En vol stabilisé en palier, la poussée équilibre le poids.',
            'En vuelo nivelado y estable, el empuje equilibra el peso.',
            'في الطيران الأفقي الثابت، الدفع يوازن الوزن.',
            'In volo livellato e stazionario, la spinta equilibra il peso.',
            'בטיסה מיושרת ויציבה, הדחף מאזן את המשקל.'),
            False, S(
            'Thrust balances drag. Lift balances weight.',
            'La poussée équilibre la traînée. La portance équilibre le poids.',
            'El empuje equilibra la resistencia. La sustentación equilibra el peso.',
            'الدفع يوازن السحب. الرفع يوازن الوزن.',
            'La spinta equilibra la resistenza. La portanza equilibra il peso.',
            'הדחף מאזן את הגרר. העילוי מאזן את המשקל.'), G4, GLENN),
        tf(HIST, S(
            'The Wright brothers built a wind tunnel before they added an engine.',
            'Les frères Wright ont construit une soufflerie avant d’ajouter un moteur.',
            'Los hermanos Wright construyeron un túnel de viento antes de añadir un motor.',
            'بنى الأخوان رايت نفقاً للرياح قبل أن يضيفا محركاً.',
            'I fratelli Wright costruirono una galleria del vento prima di aggiungere un motore.',
            'האחים רייט בנו מנהרת רוח לפני שהוסיפו מנוע.'),
            True, S(
            'Published lift data were unreliable, so they measured wing shapes themselves.',
            'Les données de portance publiées n’étaient pas fiables, alors ils ont mesuré les ailes eux-mêmes.',
            'Los datos publicados de sustentación no eran fiables, así que midieron las alas ellos mismos.',
            'بيانات الرفع المنشورة لم تكن موثوقة، فقاسوا أشكال الأجنحة بأنفسهم.',
            'I dati di portanza pubblicati non erano affidabili, quindi misurarono loro le forme alari.',
            'נתוני העילוי שפורסמו לא היו אמינים, ולכן הם מדדו את צורות הכנף בעצמם.'), WF, SMITH),
        tf(DESIGN, S(
            'Engineers design the aircraft first and then find a mission for it.',
            'Les ingénieurs dessinent d’abord l’avion, puis lui trouvent une mission.',
            'Los ingenieros diseñan primero el avión y después le buscan una misión.',
            'يصمم المهندسون الطائرة أولاً ثم يجدون لها مهمة.',
            'Gli ingegneri progettano prima l’aereo e poi gli trovano una missione.',
            'המהנדסים מתכננים קודם את המטוס ואז מוצאים לו משימה.'),
            False, S(
            'The mission and its requirements come first.',
            'La mission et ses exigences viennent en premier.',
            'La misión y sus requisitos van primero.',
            'المهمة ومتطلباتها تأتي أولاً.',
            'La missione e i suoi requisiti vengono prima.',
            'המשימה והדרישות שלה באות קודם.'), G, GLENN),
        tf(DESIGN, S(
            'Shaving a little weight off a design saves only that weight.',
            'Enlever un peu de masse à un dessin n’économise que cette masse.',
            'Quitar un poco de peso a un diseño ahorra solo ese peso.',
            'إنقاص وزن قليل من التصميم يوفر ذلك الوزن فقط.',
            'Togliere un po’ di peso a un progetto risparmia solo quel peso.',
            'הורדת מעט משקל מתכן חוסכת רק את המשקל הזה.'),
            False, S(
            'Weight compounds: extra structure needs more lift, a bigger wing, more drag and more fuel.',
            'La masse se compose : plus de structure demande plus de portance, une plus grande aile, plus de traînée et plus de carburant.',
            'El peso se compone: más estructura pide más sustentación, un ala mayor, más resistencia y más combustible.',
            'الوزن يتراكم: بنية إضافية تحتاج رفعاً أكبر، وجناحاً أكبر، وسحباً أكثر، ووقوراً أكثر.',
            'Il peso si compone: più struttura chiede più portanza, un’ala più grande, più resistenza e più carburante.',
            'המשקל מצטבר: מבנה נוסף דורש יותר עילוי, כנף גדולה יותר, יותר גרר ויותר דלק.'), G, GLENN),
        mc(HIST, S(
            'The best Wright flight on 17 December 1903 covered about…',
            'Le meilleur vol des Wright le 17 décembre 1903 a couvert environ…',
            'El mejor vuelo de los Wright el 17 de diciembre de 1903 cubrió unos…',
            'أفضل رحلة للأخوين رايت في 17 ديسمبر 1903 قطعت نحو…',
            'Il miglior volo dei Wright il 17 dicembre 1903 coprì circa…',
            'הטיסה הטובה ביותר של הרייטים ב-17 בדצמבר 1903 עברה כ…'),
            [S('12 m', '12 m', '12 m', '12 م', '12 m', '12 מ׳'),
             S('36 m', '36 m', '36 m', '36 م', '36 m', '36 מ׳'),
             S('260 m', '260 m', '260 m', '260 م', '260 m', '260 מ׳'),
             S('2 km', '2 km', '2 km', '2 كم', '2 km', '2 ק״מ')], 2, S(
            'That flight covered 260 m (852 ft) in 59 seconds. The first flight was 36 m in 12 seconds.',
            'Ce vol a couvert 260 m (852 ft) en 59 secondes. Le premier vol faisait 36 m en 12 secondes.',
            'Ese vuelo cubrió 260 m (852 ft) en 59 segundos. El primer vuelo fue de 36 m en 12 segundos.',
            'قطعت تلك الرحلة 260 م (852 قدماً) في 59 ثانية. أول رحلة كانت 36 م في 12 ثانية.',
            'Quel volo coprì 260 m (852 ft) in 59 secondi. Il primo volo fu di 36 m in 12 secondi.',
            'הטיסה הזו עברה 260 מ׳ (852 רגל) ב-59 שניות. הטיסה הראשונה הייתה 36 מ׳ ב-12 שניות.'), WF, SMITH),
        mc(HIST, S(
            'The Wright Flyer’s first flight lasted…',
            'Le premier vol du Flyer des Wright a duré…',
            'El primer vuelo del Flyer de los Wright duró…',
            'دامت أول رحلة لفلاير رايت…',
            'Il primo volo del Flyer dei Wright durò…',
            'הטיסה הראשונה של הפלייר של רייט נמשכה…'),
            [S('2 s', '2 s', '2 s', '2 ث', '2 s', '2 ש׳'),
             S('12 s', '12 s', '12 s', '12 ث', '12 s', '12 ש׳'),
             S('59 s', '59 s', '59 s', '59 ث', '59 s', '59 ש׳'),
             S('2 min', '2 min', '2 min', '2 د', '2 min', '2 דק׳')], 1, S(
            'The first flight was 12 seconds. The longest that day was 59 seconds.',
            'Le premier vol a duré 12 secondes. Le plus long ce jour-là a duré 59 secondes.',
            'El primer vuelo duró 12 segundos. El más largo de ese día duró 59 segundos.',
            'أول رحلة دامت 12 ثانية. أطول رحلة في ذلك اليوم دامت 59 ثانية.',
            'Il primo volo durò 12 secondi. Il più lungo quel giorno durò 59 secondi.',
            'הטיסה הראשונה נמשכה 12 שניות. הארוכה ביותר באותו יום נמשכה 59 שניות.'), WF, SMITH),
        mc(FORCES, S(
            'Weight is…',
            'Le poids est…',
            'El peso es…',
            'الوزن هو…',
            'Il peso è…',
            'המשקל הוא…'),
            [S('W = mg', 'W = mg', 'W = mg', 'W = mg', 'W = mg', 'W = mg'),
             S('W = m/g', 'W = m/g', 'W = m/g', 'W = m/g', 'W = m/g', 'W = m/g'),
             S('W = m + g', 'W = m + g', 'W = m + g', 'W = m + g', 'W = m + g', 'W = m + g'),
             S('W = g/m', 'W = g/m', 'W = g/m', 'W = g/m', 'W = g/m', 'W = g/m')], 0, S(
            'The unit writes weight as W = mg.',
            'L’unité écrit le poids W = mg.',
            'La unidad escribe el peso como W = mg.',
            'الوحدة تكتب الوزن W = mg.',
            'L’unità scrive il peso come W = mg.',
            'היחידה כותבת את המשקל כ-W = mg.'), G4, GLENN),
        mc(DESIGN, S(
            'In the worked trade study, concepts A and B both score…',
            'Dans l’étude d’arbitrage travaillée, les concepts A et B obtiennent tous deux…',
            'En el estudio de compromiso resuelto, los conceptos A y B obtienen ambos…',
            'في دراسة المفاضلة المحلولة، يحصل المفهومان A وB كلاهما على…',
            'Nello studio di compromesso svolto, i concetti A e B ottengono entrambi…',
            'במחקר הפשרות הפתוח, שני הרעיונות A ו-B מקבלים…'),
            [S('6.0', '6,0', '6,0', '6.0', '6,0', '6.0'),
             S('7.2', '7,2', '7,2', '7.2', '7,2', '7.2'),
             S('8.1', '8,1', '8,1', '8.1', '8,1', '8.1'),
             S('9.0', '9,0', '9,0', '9.0', '9,0', '9.0')], 1, S(
            'Both weighted scores are 7.2, so the study is a tie.',
            'Les deux scores pondérés valent 7,2 : c’est une égalité.',
            'Las dos puntuaciones ponderadas valen 7,2: hay empate.',
            'كلا الدرجتين المرجحتين 7.2، فالنتيجة تعادل.',
            'Entrambi i punteggi pesati valgono 7,2: è un pareggio.',
            'שני הציונים המשוקללים הם 7.2, ולכן זו תיקו.'), G, GLENN),
        tf(FORCES, S(
            'In steady level flight, lift equals drag.',
            'En vol stabilisé en palier, la portance égale la traînée.',
            'En vuelo nivelado y estable, la sustentación es igual a la resistencia.',
            'في الطيران الأفقي الثابت، الرفع يساوي السحب.',
            'In volo livellato e stazionario, la portanza è uguale alla resistenza.',
            'בטיסה מיושרת ויציבה, העילוי שווה לגרר.'),
            False, S(
            'Lift equals weight. Thrust equals drag.',
            'La portance égale le poids. La poussée égale la traînée.',
            'La sustentación es igual al peso. El empuje es igual a la resistencia.',
            'الرفع يساوي الوزن. الدفع يساوي السحب.',
            'La portanza è uguale al peso. La spinta è uguale alla resistenza.',
            'העילוי שווה למשקל. הדחף שווה לגרר.'), G4, GLENN),
        mc(FORCES, S(
            'This unit names how many forces of flight?',
            'Combien de forces du vol cette unité nomme-t-elle ?',
            '¿Cuántas fuerzas del vuelo nombra esta unidad?',
            'كم قوة طيران تسمي هذه الوحدة؟',
            'Quante forze del volo nomina questa unità?',
            'כמה כוחות טיסה היחידה הזו מונה?'),
            [S('2', '2', '2', '2', '2', '2'), S('3', '3', '3', '3', '3', '3'),
             S('4', '4', '4', '4', '4', '4'), S('5', '5', '5', '5', '5', '5')], 2, S(
            'The four forces are lift, weight, thrust and drag.',
            'Les quatre forces sont la portance, le poids, la poussée et la traînée.',
            'Las cuatro fuerzas son sustentación, peso, empuje y resistencia.',
            'القوى الأربع هي الرفع والوزن والدفع والسحب.',
            'Le quattro forze sono portanza, peso, spinta e resistenza.',
            'ארבעת הכוחות הם עילוי, משקל, דחף וגרר.'), G4, GLENN),
        mc(CLIM, S(
            'This unit quotes NASA’s three paths to sustainable aviation as…',
            'Cette unité cite les trois voies de la NASA vers une aviation durable :',
            'Esta unidad cita las tres vías de la NASA hacia una aviación sostenible:',
            'تذكر هذه الوحدة مسارات ناسا الثلاثة نحو طيران مستدام:',
            'Questa unità cita le tre vie della NASA verso un’aviazione sostenibile:',
            'היחידה מצטטת את שלושת המסלולים של נאס״א לתעופה בת-קיימא:'),
            [S('bigger fuel tanks only', 'seulement de plus grands réservoirs', 'solo depósitos más grandes', 'خزانات وقود أكبر فقط', 'solo serbatoi più grandi', 'מכלי דלק גדולים יותר בלבד'),
             S('efficient aircraft, sustainable fuel, and better operations', 'avions efficaces, carburant durable et meilleures opérations', 'aviones eficientes, combustible sostenible y mejores operaciones', 'طائرات أكفأ، ووقود مستدام، وعمليات أفضل', 'aerei efficienti, carburante sostenibile e operazioni migliori', 'מטוסים יעילים, דלק בר-קיימא ותפעול טוב יותר'),
             S('flying lower only', 'seulement voler plus bas', 'solo volar más bajo', 'الطيران على ارتفاع أقل فقط', 'solo volare più basso', 'טיסה נמוכה יותר בלבד'),
             S('slower climbs only', 'seulement des montées plus lentes', 'solo ascensos más lentos', 'تسلق أبطأ فقط', 'solo salite più lente', 'טיפוס איטי יותר בלבד')], 1, S(
            'The unit lists efficient aircraft technology, sustainable aviation fuel, and better operations and infrastructure.',
            'L’unité cite une technologie d’avion efficace, le carburant d’aviation durable, et de meilleures opérations et infrastructures.',
            'La unidad cita tecnología de avión eficiente, combustible sostenible de aviación y mejores operaciones e infraestructuras.',
            'تذكر الوحدة تقنية طائرات أكفأ، ووقود طيران مستداماً، وعمليات وبنية تحتية أفضل.',
            'L’unità cita tecnologia di aereo efficiente, carburante sostenibile e operazioni e infrastrutture migliori.',
            'היחידה מונה טכנולוגיית מטוס יעילה, דלק תעופה בר-קיימא, ותפעול ותשתית טובים יותר.'), SUS, NASA),
        mc(DESIGN, S(
            'A trade study, as this unit defines it, compares options…',
            'Une étude d’arbitrage, telle que cette unité la définit, compare des options…',
            'Un estudio de compromiso, como lo define esta unidad, compara opciones…',
            'دراسة المفاضلة، كما تعرفها هذه الوحدة، تقارن الخيارات…',
            'Uno studio di compromesso, come lo definisce questa unità, confronta le opzioni…',
            'מחקר פשרות, כפי שהיחידה מגדירה אותו, משווה אפשרויות…'),
            [S('by the lowest price only', 'selon le plus bas prix seulement', 'solo por el precio más bajo', 'حسب أدنى سعر فقط', 'solo in base al prezzo più basso', 'לפי המחיר הנמוך בלבד'),
             S('against weighted criteria', 'selon des critères pondérés', 'según criterios ponderados', 'وفق معايير مرجّحة', 'secondo criteri pesati', 'לפי קריטריונים משוקללים'),
             S('by painting them', 'en les peignant', 'pintándolas', 'بطلائها', 'verniciandole', 'על ידי צביעתן'),
             S('after the first flight only', 'seulement après le premier vol', 'solo después del primer vuelo', 'بعد أول طيران فقط', 'solo dopo il primo volo', 'רק אחרי הטיסה הראשונה')], 1, S(
            'A trade study ranks options against weighted criteria.',
            'Une étude d’arbitrage classe les options selon des critères pondérés.',
            'Un estudio de compromiso ordena las opciones según criterios ponderados.',
            'دراسة المفاضلة ترتب الخيارات وفق معايير مرجّحة.',
            'Uno studio di compromesso ordina le opzioni secondo criteri pesati.',
            'מחקר פשרות מדרג אפשרויות לפי קריטריונים משוקללים.'), G, GLENN),
    ], 'cards': [
        card(S('Four forces', 'Quatre forces', 'Cuatro fuerzas', 'القوى الأربع', 'Quattro forze', 'ארבעה כוחות'),
             S('Lift, weight, thrust and drag.', 'Portance, poids, poussée et traînée.', 'Sustentación, peso, empuje y resistencia.', 'الرفع والوزن والدفع والسحب.', 'Portanza, peso, spinta e resistenza.', 'עילוי, משקל, דחף וגרר.')),
        card(S('Level flight', 'Vol en palier', 'Vuelo nivelado', 'الطيران الأفقي', 'Volo livellato', 'טיסה מיושרת'),
             S('Lift = weight and thrust = drag.', 'Portance = poids et poussée = traînée.', 'Sustentación = peso y empuje = resistencia.', 'الرفع = الوزن والدفع = السحب.', 'Portanza = peso e spinta = resistenza.', 'עילוי = משקל ודחף = גרר.')),
        card(S('Weight', 'Poids', 'Peso', 'الوزن', 'Peso', 'משקל'),
             S('W = mg.', 'W = mg.', 'W = mg.', 'W = mg.', 'W = mg.', 'W = mg.')),
        card(S('First Wright flight', 'Premier vol des Wright', 'Primer vuelo de los Wright', 'أول رحلة لرايت', 'Primo volo dei Wright', 'הטיסה הראשונה של רייט'),
             S('17 December 1903: 36 m in 12 s.', '17 décembre 1903 : 36 m en 12 s.', '17 de diciembre de 1903: 36 m en 12 s.', '17 ديسمبر 1903: 36 م في 12 ث.', '17 dicembre 1903: 36 m in 12 s.', '17 בדצמבר 1903: 36 מ׳ ב-12 ש׳.')),
        card(S('Best flight that day', 'Meilleur vol ce jour-là', 'Mejor vuelo ese día', 'أفضل رحلة ذلك اليوم', 'Miglior volo quel giorno', 'הטיסה הטובה באותו יום'),
             S('260 m in 59 s.', '260 m en 59 s.', '260 m en 59 s.', '260 م في 59 ث.', '260 m in 59 s.', '260 מ׳ ב-59 ש׳.')),
        card(S('Ground speed of the first flight', 'Vitesse au sol du premier vol', 'Velocidad sobre el suelo del primer vuelo', 'السرعة على الأرض لأول رحلة', 'Velocità al suolo del primo volo', 'מהירות הקרקע של הטיסה הראשונה'),
             S('3 m/s.', '3 m/s.', '3 m/s.', '3 م/ث.', '3 m/s.', '3 מ׳/ש׳.')),
        card(S('Wind tunnel', 'Soufflerie', 'Túnel de viento', 'نفق الرياح', 'Galleria del vento', 'מנהרת רוח'),
             S('The Wrights measured wings before adding an engine.', 'Les Wright ont mesuré des ailes avant d’ajouter un moteur.', 'Los Wright midieron alas antes de añadir un motor.', 'قاس الأخوان رايت الأجنحة قبل إضافة محرك.', 'I Wright misurarono le ali prima di aggiungere un motore.', 'הרייטים מדדו כנפיים לפני שהוסיפו מנוע.')),
        card(S('Requirements', 'Exigences', 'Requisitos', 'المتطلبات', 'Requisiti', 'דרישות'),
             S('Measurable targets a design must meet.', 'Cibles mesurables qu’un dessin doit atteindre.', 'Metas medibles que un diseño debe cumplir.', 'أهداف قابلة للقياس يجب أن يحققها التصميم.', 'Obiettivi misurabili che un progetto deve raggiungere.', 'יעדים מדידים שתכן חייב לעמוד בהם.')),
        card(S('Trade study', 'Étude d’arbitrage', 'Estudio de compromiso', 'دراسة المفاضلة', 'Studio di compromesso', 'מחקר פשרות'),
             S('Weighted comparison of options.', 'Comparaison pondérée d’options.', 'Comparación ponderada de opciones.', 'مقارنة مرجّحة للخيارات.', 'Confronto pesato di opzioni.', 'השוואה משוקללת של אפשרויות.')),
        card(S('Tie at 7.2', 'Égalité à 7,2', 'Empate en 7,2', 'تعادل عند 7.2', 'Pareggio a 7,2', 'תיקו ב-7.2'),
             S('Concepts A and B scored the same.', 'Les concepts A et B ont eu le même score.', 'Los conceptos A y B obtuvieron la misma nota.', 'حصل المفهومان A وB على الدرجة نفسها.', 'I concetti A e B hanno avuto lo stesso punteggio.', 'הרעיונות A ו-B קיבלו אותו ציון.')),
        card(S('Design cycle', 'Cycle de conception', 'Ciclo de diseño', 'دورة التصميم', 'Ciclo di progetto', 'מחזור התכן'),
             S('Concept, analysis, test, then redesign.', 'Concept, analyse, essai, puis reprise.', 'Concepto, análisis, ensayo y rediseño.', 'مفهوم، ثم تحليل، ثم اختبار، ثم إعادة تصميم.', 'Concetto, analisi, prova, poi riprogettazione.', 'רעיון, ניתוח, ניסוי, ואז תכן מחדש.')),
        card(S('Weight spiral', 'Spirale de masse', 'Espiral de peso', 'لولب الوزن', 'Spirale del peso', 'סחרור המשקל'),
             S('Extra weight grows the wing, the drag and the fuel.', 'Une masse en plus agrandit l’aile, la traînée et le carburant.', 'Un peso extra agranda el ala, la resistencia y el combustible.', 'وزن إضافي يكبر الجناح والسحب والوقود.', 'Un peso in più ingrandisce l’ala, la resistenza e il carburante.', 'משקל נוסף מגדיל את הכנף, הגרר והדלק.')),
        card(S('1,100 kg airplane', 'Avion de 1 100 kg', 'Avión de 1.100 kg', 'طائرة 1100 كغ', 'Aereo di 1.100 kg', 'מטוס של 1,100 ק״ג'),
             S('Level lift is 10,791 N.', 'La portance en palier est 10 791 N.', 'La sustentación en vuelo nivelado es 10.791 N.', 'الرفع الأفقي 10791 ن.', 'La portanza in volo livellato è 10.791 N.', 'העילוי בטיסה מיושרת הוא 10,791 נ׳.')),
        card(S('70,000 kg airliner', 'Avion de 70 000 kg', 'Avión de 70.000 kg', 'طائرة 70000 كغ', 'Aereo di 70.000 kg', 'מטוס של 70,000 ק״ג'),
             S('Level lift is 686,700 N.', 'La portance en palier est 686 700 N.', 'La sustentación nivelada es 686.700 N.', 'الرفع الأفقي 686700 ن.', 'La portanza livellata è 686.700 N.', 'העילוי המיושר הוא 686,700 נ׳.')),
        card(S('30 kN of thrust', '30 kN de poussée', '30 kN de empuje', '30 كيلونيوتن دفع', '30 kN di spinta', '30 קילו-ניוטון דחף'),
             S('In level cruise the drag is also 30 kN.', 'En croisière en palier, la traînée est aussi 30 kN.', 'En crucero nivelado la resistencia también es 30 kN.', 'في الطيران الأفقي السحب أيضاً 30 كيلونيوتن.', 'In crociera livellata anche la resistenza è 30 kN.', 'בשיוט מיושר גם הגרר הוא 30 קילו-ניוטון.')),
        card(S('Mission first', 'La mission d’abord', 'La misión primero', 'المهمة أولاً', 'Prima la missione', 'המשימה קודם'),
             S('Requirements come before the drawings.', 'Les exigences viennent avant les dessins.', 'Los requisitos van antes que los dibujos.', 'المتطلبات تأتي قبل الرسوم.', 'I requisiti vengono prima dei disegni.', 'הדרישות באות לפני השרטוטים.')),
        card(S('Three NASA paths', 'Trois voies de la NASA', 'Tres vías de la NASA', 'مسارات ناسا الثلاثة', 'Tre vie della NASA', 'שלושת המסלולים של נאס״א'),
             S('Efficient aircraft, sustainable fuel, better operations.', 'Avion efficace, carburant durable, meilleures opérations.', 'Avión eficiente, combustible sostenible, mejores operaciones.', 'طائرة أكفأ، ووقود مستدام، وعمليات أفضل.', 'Aereo efficiente, carburante sostenibile, operazioni migliori.', 'מטוס יעיל, דלק בר-קיימא, תפעול טוב יותר.')),
        card(S('Headwind', 'Vent de face', 'Viento de frente', 'ريح معاكسة', 'Vento contrario', 'רוח נגדית'),
             S('The Flyer’s airspeed was higher than its 3 m/s ground speed.', 'La vitesse air du Flyer était plus haute que ses 3 m/s au sol.', 'La velocidad respecto al aire del Flyer era mayor que sus 3 m/s sobre el suelo.', 'سرعة هواء الفلاير كانت أعلى من 3 م/ث على الأرض.', 'La velocità rispetto all’aria del Flyer era più alta dei suoi 3 m/s al suolo.', 'מהירות האוויר של הפלייר הייתה גבוהה מ-3 מ׳/ש׳ על הקרקע.')),
    ]}
    return U


# Start-screen copy. Address: French vous, Spanish tú, Italian tu, Arabic singular, Hebrew plural.
START = S('Start', 'Commencez', 'Empieza', 'ابدأ', 'Inizia', 'התחילו')
QLEAD = S(
    '{n} questions · about {m} minutes',
    '{n} questions · environ {m} minutes',
    '{n} preguntas · unos {m} minutos',
    '{n} أسئلة · نحو {m} دقائق',
    '{n} domande · circa {m} minuti',
    '{n} שאלות · כ-{m} דקות')
CLEAD = S(
    '{n} cards · about {m} minutes',
    '{n} cartes · environ {m} minutes',
    '{n} tarjetas · unos {m} minutos',
    '{n} بطاقات · نحو {m} دقائق',
    '{n} carte · circa {m} minuti',
    '{n} כרטיסים · כ-{m} דקות')

CHECK_CSS = (
    '.crs-deck,.crs-quizapp{margin:.4rem 0 1rem;max-width:100%}'
    '.crs-start-lead{margin:.2rem 0 .6rem}'
    '.crs-check-bar{display:flex;align-items:center;gap:.6rem;margin:0 0 .7rem}'
    '.crs-check-bar progress{flex:1 1 auto;width:100%;height:.7rem;min-width:0}'
    '.crs-check-pos{font-variant-numeric:tabular-nums;white-space:nowrap}'
    '.crs-quizapp fieldset{border:0;margin:0;padding:0;min-width:0}'
    '.crs-quizapp legend{padding:0;margin:0 0 .6rem;font-weight:600}'
    '.crs-quizapp label{display:flex;align-items:flex-start;gap:.5rem;width:100%;margin:.35rem 0;padding:.55rem .7rem;'
    'border:1px solid rgba(255,255,255,.28);border-radius:12px;background:rgba(255,255,255,.05)}'
    '.crs-num{display:block;width:100%;max-width:16rem;min-height:44px;margin:.4rem 0;padding:.4rem .6rem;'
    'direction:ltr;font:inherit;color:inherit;background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.35);border-radius:10px}'
    '.crs-check-actions{display:flex;flex-wrap:wrap;gap:.5rem;margin:.7rem 0}'
    '.crs-deck .crs-card{display:block;width:100%;min-height:7.5rem;margin:.2rem 0;padding:1rem;text-align:start;'
    'font:inherit;color:inherit;cursor:pointer;border:1px solid rgba(255,255,255,.28);border-radius:16px;background:rgba(255,255,255,.06)}'
    '.crs-deck .crs-card.is-back{background:rgba(255,255,255,.12)}'
    '.crs-fb{min-height:1.4em;margin:.6rem 0}'
    '.crs-fb.ok{color:#b6f5c8}.crs-fb.no{color:#ffc1b5}'
    '.crs-miss,.crs-topics{padding-inline-start:1.2rem}'
    '.crs-miss li{margin:.7rem 0}'
    '.crs-miss a{overflow-wrap:anywhere}'
    '.crs-stage{transition:opacity .18s ease}'
    '.crs-stage.is-out{opacity:0}'
    '.crs-live{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}'
    '.crs-force-keep{list-style:none;padding:0;margin:.4rem 0 1rem}'
    '.crs-deck button:focus-visible,.crs-quizapp button:focus-visible,.crs-quizapp label:focus-within,.crs-num:focus-visible'
    '{outline:3px solid #ffd54a;outline-offset:2px}'
    '@media (prefers-reduced-motion:reduce){.crs-stage{transition:none}}'
)


def lead(lang, kind, n, minutes):
    tmpl = QLEAD[lang] if kind == 'quiz' else CLEAD[lang]
    return tmpl.replace('{n}', str(n)).replace('{m}', str(minutes))


def mount(lang, uid, n_quiz, n_cards):
    """Start screens. The question file loads only after Start."""
    pre = '' if lang == 'en' else '../'
    src = f'{pre}assets/courses/aero101/{uid}.{lang}.json'
    start = START[lang]
    deck = (
        f'<div class="crs-deck" data-unit="{uid}" data-src="{src}" data-kind="cards">'
        f'<p class="crs-start-lead">{lead(lang, "cards", n_cards, 8)}</p>'
        f'<button type="button" class="btn crs-btn crs-go">{start}</button></div>'
    )
    quiz = (
        f'<div class="crs-quizapp" data-unit="{uid}" data-src="{src}">'
        f'<p class="crs-start-lead">{lead(lang, "quiz", n_quiz, 15)}</p>'
        f'<button type="button" class="btn crs-btn crs-go">{start}</button></div>'
    )
    return deck, quiz
