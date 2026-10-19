#!/usr/bin/env python3
"""Oct 18 2026 (owner: 'whatever free images we can during the trip to, around and back home. Not too much, just awesome
images to denote the time in history'): 'Moments in History' gallery on Artemis_II.html (the Artemis Program page), all languages.
Six public-domain NASA photos per flown mission (Artemis I 2022, Artemis II 2026), each from images.nasa.gov at original
resolution, uploaded untouched to R2 with scripts/r2-upload.py --srcset (AVIF/WebP widths 480..3840 served lazily).
Every caption fact is taken from NASA's own caption for that image ID; the IDs are printed in each credit.
Idempotent: replaces the block between ARTEMIS-GALLERY markers; writes i18n strings and the ARTEMIS-GALLERY CSS block."""
import json, re, html
P = 'Artemis_II.html'
LANGS = ['fr', 'es', 'ar', 'it', 'he']
man = json.load(open('assets/data/media-manifest.json', encoding='utf-8'))
E = lambda x: html.escape(x, quote=True)

# key, manifest entry, stage, date, caption, alt, credit, object-position
A1 = [
 ('images/artemis-gallery/NHQ202211160030.jpg', 'Launch', 'Nov. 16, 2022',
  "SLS and Orion lift off at 1:47 a.m. EST on the first integrated test of NASA's deep space systems.",
  "NASA's SLS rocket lifting off at night with Orion on the Artemis I flight test", 'Photo: NASA/Joel Kowsky · NHQ202211160030', '50% 40%'),
 ('images/artemis-gallery/art001e000268.jpg', 'Around the Moon', 'Nov. 21, 2022',
  "The Moon's far side looms beyond Orion on the day it passed within 80 miles of the surface.",
  "The Moon's far side beyond part of the Orion spacecraft", 'Photo: NASA · art001e000268', '50% 50%'),
 ('images/artemis-gallery/art001e000673.jpg', 'Around the Moon', 'Nov. 28, 2022',
  'At 268,563 miles from Earth, Orion flew farther than any spacecraft built for humans before it.',
  'Orion with Earth and the Moon in the distance', 'Photo: NASA · art001e000673', '50% 50%'),
 ('images/artemis-gallery/art001e002083.jpg', 'Around the Moon', 'Dec. 5, 2022',
  'Earth rises behind the Moon after a 3-minute, 27-second burn set Orion on course for home.',
  "Earth rising behind the Moon's edge beside Orion", 'Photo: NASA · art001e002083', '50% 50%'),
 ('images/artemis-gallery/KSC-20221211-PH-KLS01-0011.jpg', 'Home', 'Dec. 11, 2022',
  'Orion splashes down in the Pacific at 12:40 p.m. EST after a 25.5-day mission to the Moon.',
  'Orion descending under orange and white parachutes over the Pacific', 'Photo: NASA/Kim Shiflett · KSC-20221211-PH-KLS01-0011', '50% 45%'),
 ('images/artemis-gallery/KSC-20221211-PH-RGG01-0002.jpeg', 'Home', 'Dec. 11, 2022',
  'Recovered: Orion inside the well deck of USS Portland off Baja California.',
  'The Orion capsule inside the well deck of USS Portland with the recovery team', 'Photo: NASA/Regan Geeseman · KSC-20221211-PH-RGG01-0002', '50% 50%'),
]
A2 = [
 ('images/ArtemisII_Launch_KSC_Hancock.jpg', 'Launch', 'Apr. 1, 2026',
  "Four astronauts lift off at 6:35 p.m. ET on the first crewed mission of NASA's Artemis campaign.",
  'The SLS rocket lifting off from Launch Complex 39B with the Artemis II crew', 'Photo: NASA/Brandon Hancock · KSC-04012026-Artemis II_Launch-4', '50% 40%'),
 ('images/artemis-gallery/art002e000193.jpg', 'To the Moon', 'Apr. 3, 2026',
  'Commander Reid Wiseman photographs a backlit Earth after the burn that sent the crew to the Moon.',
  'A dark, backlit Earth with a thin bright edge, seen from Orion', 'Photo: NASA · art002e000193', '50% 50%'),
 ('images/artemis-gallery/art002e014235.jpg', 'Around the Moon', 'Apr. 6, 2026',
  'Jeremy Hansen (CSA) photographs the flyby; at closest approach the crew passed 4,067 miles from the surface.',
  'Astronaut Jeremy Hansen taking photos through an Orion window', 'Photo: NASA · art002e014235', '50% 45%'),
 ('images/artemis-gallery/art002e021278.jpg', 'Around the Moon', 'Apr. 6, 2026',
  "Earthset from behind the Moon's far side, echoing Apollo 8's Earthrise of 1968.",
  "A small, partly lit Earth setting behind the Moon's cratered horizon", 'Photo: NASA · art002e021278', '50% 60%'),
 ('images/artemis-gallery/art002e016324.jpg', 'Around the Moon', 'Apr. 6, 2026',
  'From the far side, the crew saw the Sun hide behind the Moon for nearly an hour.',
  "The Moon's dark disk ringed by a glowing halo during a solar eclipse seen from Orion", 'Photo: NASA · art002e016324', '60% 50%'),
 ('images/artemis-gallery/KSC-20260410-PH-JMB01_0004.jpg', 'Home', 'Apr. 10, 2026',
  "Koch, Glover, Hansen and Wiseman leave Orion for the 'front porch' raft after splashdown near San Diego.",
  'The four Artemis II astronauts on an inflatable raft beside Orion in the Pacific', 'Photo: NASA/James Blair · KSC-20260410-PH-JMB01_0004', '50% 50%'),
]
H2 = 'Moments in History'
INTRO = 'NASA photos from the two flown missions. Tap a photo to open the full-resolution original.'
M1 = 'Artemis I · Uncrewed test flight · Nov. 16 to Dec. 11, 2022'
M2 = 'Artemis II · Four astronauts around the Moon · Apr. 1 to 10, 2026'
SIZES = '(max-width: 600px) 100vw, (max-width: 900px) 50vw, 380px'

def fig(key, stage, date, cap, alt, credit, pos):
    e = man[key]
    webp = e['srcset']; avif = e['srcset_avif']
    small = [u for u, w in (t.strip().rsplit(' ', 1) for t in webp.split(',')) if w in ('800w',)] or [webp.split(',')[0].strip().rsplit(' ', 1)[0]]
    return (f'<figure class="ag-item"><a class="ag-link" href="{e["url"]}" target="_blank" rel="noopener">'
            f'<picture><source type="image/avif" srcset="{avif}" sizes="{SIZES}">'
            f'<img src="{small[0]}" srcset="{webp}" sizes="{SIZES}" width="{e["width"]}" height="{e["height"]}" loading="lazy" decoding="async" '
            f'alt="{E(alt)}" style="object-position:{pos}"></picture></a>'
            f'<figcaption><span class="ag-meta"><span class="ag-stage">{E(stage)}</span><span class="ag-date">{E(date)}</span></span>'
            f'<span class="ag-cap">{E(cap)}</span><span class="ag-credit">{E(credit)}</span></figcaption></figure>')

BLOCK = ('<!-- ARTEMIS-GALLERY:START --><section class="art-gallery" id="moments" aria-labelledby="moments-h">'
         f'<h2 id="moments-h">{H2}</h2><p class="ag-intro">{E(INTRO)}</p>'
         f'<h3 class="ag-mission">{E(M1)}</h3><div class="ag-grid">' + ''.join(fig(*x) for x in A1) + '</div>'
         f'<h3 class="ag-mission">{E(M2)}</h3><div class="ag-grid">' + ''.join(fig(*x) for x in A2) + '</div>'
         '</section><!-- ARTEMIS-GALLERY:END -->')

s = open(P, encoding='utf-8').read(); s0 = s
s = re.sub(r'<!-- ARTEMIS-GALLERY:START -->.*?<!-- ARTEMIS-GALLERY:END -->', '', s, flags=re.S)
i = s.index('<section class="five-ws" id="tracker">'); j = s.index('</section>', i) + len('</section>')
s = s[:j] + BLOCK + s[j:]
if s != s0: open(P, 'w', encoding='utf-8').write(s)

# --- translations (numbers converted with NASA's own metric figures: 130 km, 432,210 km, 6,545 km)
T = {
 'Launch': ['Lancement', 'Lanzamiento', 'الإطلاق', 'Lancio', 'שיגור'],
 'To the Moon': ['Vers la Lune', 'Hacia la Luna', 'نحو القمر', 'Verso la Luna', 'אל הירח'],
 'Around the Moon': ['Autour de la Lune', 'Alrededor de la Luna', 'حول القمر', 'Intorno alla Luna', 'סביב הירח'],
 'Home': ['Retour', 'De vuelta a casa', 'العودة إلى الوطن', 'Ritorno a casa', 'הביתה'],
 'Nov. 16, 2022': ['16 nov. 2022', '16 nov. 2022', '16 نوفمبر 2022', '16 nov. 2022', '16 בנובמבר 2022'],
 'Nov. 21, 2022': ['21 nov. 2022', '21 nov. 2022', '21 نوفمبر 2022', '21 nov. 2022', '21 בנובמבר 2022'],
 'Nov. 28, 2022': ['28 nov. 2022', '28 nov. 2022', '28 نوفمبر 2022', '28 nov. 2022', '28 בנובמבר 2022'],
 'Dec. 5, 2022': ['5 déc. 2022', '5 dic. 2022', '5 ديسمبر 2022', '5 dic. 2022', '5 בדצמבר 2022'],
 'Dec. 11, 2022': ['11 déc. 2022', '11 dic. 2022', '11 ديسمبر 2022', '11 dic. 2022', '11 בדצמבר 2022'],
 'Apr. 1, 2026': ['1er avr. 2026', '1 abr. 2026', '1 أبريل 2026', '1 apr. 2026', '1 באפריל 2026'],
 'Apr. 3, 2026': ['3 avr. 2026', '3 abr. 2026', '3 أبريل 2026', '3 apr. 2026', '3 באפריל 2026'],
 'Apr. 6, 2026': ['6 avr. 2026', '6 abr. 2026', '6 أبريل 2026', '6 apr. 2026', '6 באפריל 2026'],
 'Apr. 10, 2026': ['10 avr. 2026', '10 abr. 2026', '10 أبريل 2026', '10 apr. 2026', '10 באפריל 2026'],
 H2: ["Moments d'histoire", 'Momentos históricos', 'لحظات تاريخية', 'Momenti storici', 'רגעים היסטוריים'],
 INTRO: ['Photos de la NASA des deux missions déjà effectuées. Touchez une photo pour ouvrir l\u2019original en pleine résolution.',
         'Fotos de la NASA de las dos misiones ya realizadas. Toca una foto para abrir el original en resolución completa.',
         'صور من ناسا للمهمتين اللتين نُفّذتا. اضغط على أي صورة لفتح الأصل بدقته الكاملة.',
         'Foto della NASA delle due missioni già volate. Tocca una foto per aprire l\u2019originale a piena risoluzione.',
         'תמונות של NASA משתי המשימות שכבר טסו. הקישו על תמונה כדי לפתוח את המקור ברזולוציה מלאה.'],
 M1: ['Artemis I · Vol d\u2019essai sans équipage · du 16 nov. au 11 déc. 2022', 'Artemis I · Vuelo de prueba sin tripulación · del 16 nov. al 11 dic. 2022',
      'Artemis I · رحلة تجريبية غير مأهولة · من 16 نوفمبر إلى 11 ديسمبر 2022', 'Artemis I · Volo di prova senza equipaggio · dal 16 nov. all\u201911 dic. 2022',
      'Artemis I · טיסת ניסוי ללא צוות · 16 בנובמבר עד 11 בדצמבר 2022'],
 M2: ['Artemis II · Quatre astronautes autour de la Lune · du 1er au 10 avr. 2026', 'Artemis II · Cuatro astronautas alrededor de la Luna · del 1 al 10 abr. 2026',
      'Artemis II · أربعة رواد حول القمر · من 1 إلى 10 أبريل 2026', 'Artemis II · Quattro astronauti intorno alla Luna · dall\u20191 al 10 apr. 2026',
      'Artemis II · ארבעה אסטרונאוטים סביב הירח · 1 עד 10 באפריל 2026'],
 A1[0][3]: ["SLS et Orion décollent à 1 h 47 (heure de l'Est) pour le premier essai intégré des systèmes d'exploration lointaine de la NASA.",
            'SLS y Orion despegan a la 1:47 a. m. (hora del Este) en la primera prueba integrada de los sistemas de espacio profundo de la NASA.',
            'ينطلق SLS وOrion الساعة 1:47 صباحًا بتوقيت شرق أمريكا في أول اختبار متكامل لأنظمة ناسا لاستكشاف الفضاء السحيق.',
            "SLS e Orion decollano alle 1:47 (ora della costa est) nel primo test integrato dei sistemi NASA per lo spazio profondo.",
            'SLS ו-Orion ממריאים ב-1:47 לפנות בוקר (שעון החוף המזרחי) בניסוי המשולב הראשון של מערכות החלל העמוק של NASA.'],
 A1[1][3]: ["La face cachée de la Lune se dresse derrière Orion, le jour où il est passé à 130 km (80 milles) de la surface.",
            'La cara oculta de la Luna se alza tras Orion el día en que pasó a 130 km (80 millas) de la superficie.',
            'الجانب البعيد من القمر يلوح خلف Orion في اليوم الذي مرّت فيه على بعد 130 كم (80 ميلًا) من سطحه.',
            'La faccia nascosta della Luna incombe oltre Orion nel giorno in cui passò a 130 km (80 miglia) dalla superficie.',
            'הצד הרחוק של הירח מתנשא מעבר ל-Orion ביום שבו חלפה 130 ק"מ (80 מייל) מעל פני השטח.'],
 A1[2][3]: ["À 432 210 km (268 563 milles) de la Terre, Orion est allé plus loin qu'aucun vaisseau conçu pour des humains avant lui.",
            'A 432.210 km (268.563 millas) de la Tierra, Orion llegó más lejos que cualquier nave construida para humanos antes que ella.',
            'على بعد 432,210 كم (268,563 ميلًا) من الأرض، ابتعدت Orion أكثر من أي مركبة صُممت للبشر قبلها.',
            "A 432.210 km (268.563 miglia) dalla Terra, Orion si è spinto più lontano di qualsiasi veicolo costruito per esseri umani prima di lui.",
            'במרחק 432,210 ק"מ (268,563 מייל) מכדור הארץ, Orion הגיעה רחוק יותר מכל חללית שנבנתה לבני אדם לפניה.'],
 A1[3][3]: ["La Terre se lève derrière la Lune après une poussée de 3 minutes 27 secondes qui a mis Orion sur le chemin du retour.",
            'La Tierra sale tras la Luna después de un encendido de 3 minutos y 27 segundos que puso a Orion rumbo a casa.',
            'الأرض تشرق خلف القمر بعد احتراق محرك دام 3 دقائق و27 ثانية وضع Orion على طريق العودة.',
            "La Terra sorge dietro la Luna dopo un\u2019accensione di 3 minuti e 27 secondi che ha messo Orion sulla rotta di casa.",
            'כדור הארץ זורח מאחורי הירח אחרי הפעלת מנוע של 3 דקות ו-27 שניות ששמה את Orion במסלול הביתה.'],
 A1[4][3]: ["Orion amerrit dans le Pacifique à 12 h 40 (heure de l'Est) après une mission de 25,5 jours vers la Lune.",
            'Orion amariza en el Pacífico a las 12:40 p. m. (hora del Este) tras una misión de 25,5 días a la Luna.',
            'تهبط Orion في المحيط الهادئ الساعة 12:40 ظهرًا بتوقيت شرق أمريكا بعد مهمة إلى القمر استمرت 25.5 يومًا.',
            "Orion ammara nel Pacifico alle 12:40 (ora della costa est) dopo una missione di 25,5 giorni verso la Luna.",
            'Orion נוחתת באוקיינוס השקט ב-12:40 בצהריים (שעון החוף המזרחי) אחרי משימה של 25.5 ימים לירח.'],
 A1[5][3]: ["Récupéré : Orion dans le radier de l'USS Portland, au large de la Basse-Californie.",
            'Recuperada: Orion dentro del dique del USS Portland, frente a Baja California.',
            'تم الاسترداد: Orion داخل الحوض الداخلي للسفينة USS Portland قبالة سواحل باخا كاليفورنيا.',
            "Recuperata: Orion nel bacino allagabile della USS Portland, al largo della Bassa California.",
            'חולצה: Orion בתוך תא העגינה של USS Portland מול חופי באחה קליפורניה.'],
 A2[0][3]: ["Quatre astronautes décollent à 18 h 35 (heure de l'Est) pour la première mission habitée du programme Artemis de la NASA.",
            'Cuatro astronautas despegan a las 6:35 p. m. (hora del Este) en la primera misión tripulada de la campaña Artemis de la NASA.',
            'أربعة رواد ينطلقون الساعة 6:35 مساءً بتوقيت شرق أمريكا في أول مهمة مأهولة ضمن حملة أرتيميس التابعة لناسا.',
            "Quattro astronauti decollano alle 18:35 (ora della costa est) nella prima missione con equipaggio della campagna Artemis della NASA.",
            'ארבעה אסטרונאוטים ממריאים ב-18:35 (שעון החוף המזרחי) במשימה המאוישת הראשונה של קמפיין ארטמיס של NASA.'],
 A2[1][3]: ["Le commandant Reid Wiseman photographie une Terre à contre-jour après la poussée qui a envoyé l'équipage vers la Lune.",
            'El comandante Reid Wiseman fotografía una Tierra a contraluz tras el encendido que envió a la tripulación hacia la Luna.',
            'القائد ريد وايزمان يصوّر الأرض وهي مضاءة من الخلف بعد احتراق المحرك الذي أرسل الطاقم نحو القمر.',
            "Il comandante Reid Wiseman fotografa una Terra in controluce dopo l\u2019accensione che ha spedito l\u2019equipaggio verso la Luna.",
            'המפקד ריד וייזמן מצלם את כדור הארץ מואר מאחור אחרי הפעלת המנוע ששלחה את הצוות לירח.'],
 A2[2][3]: ["Jeremy Hansen (ASC) photographie le survol ; au plus près, l'équipage est passé à 6 545 km (4 067 milles) de la surface.",
            'Jeremy Hansen (CSA) fotografía el sobrevuelo; en su máximo acercamiento, la tripulación pasó a 6.545 km (4.067 millas) de la superficie.',
            'جيريمي هانسن (وكالة الفضاء الكندية) يصوّر التحليق؛ وعند أقرب نقطة مرّ الطاقم على بعد 6,545 كم (4,067 ميلًا) من السطح.',
            "Jeremy Hansen (CSA) fotografa il sorvolo; al massimo avvicinamento l\u2019equipaggio è passato a 6.545 km (4.067 miglia) dalla superficie.",
            "ג'רמי הנסן (סוכנות החלל הקנדית) מצלם את הטיסה ליד הירח; בנקודה הקרובה ביותר חלף הצוות 6,545 ק\"מ (4,067 מייל) מפני השטח."],
 A2[3][3]: ["Coucher de Terre derrière la face cachée de la Lune, écho au lever de Terre d'Apollo 8 en 1968.",
            'Puesta de la Tierra tras la cara oculta de la Luna, eco del amanecer terrestre del Apolo 8 en 1968.',
            'غروب الأرض خلف الجانب البعيد من القمر، صدى لصورة شروق الأرض التي التقطتها أبولو 8 عام 1968.',
            "Tramonto della Terra dietro la faccia nascosta della Luna, eco della «Earthrise» dell\u2019Apollo 8 del 1968.",
            'שקיעת כדור הארץ מאחורי הצד הרחוק של הירח, הד לתמונת "זריחת כדור הארץ" של אפולו 8 מ-1968.'],
 A2[4][3]: ["Depuis la face cachée, l'équipage a vu le Soleil disparaître derrière la Lune pendant près d'une heure.",
            'Desde la cara oculta, la tripulación vio el Sol esconderse tras la Luna durante casi una hora.',
            'من الجانب البعيد، رأى الطاقم الشمس تختفي خلف القمر لما يقرب من ساعة.',
            "Dalla faccia nascosta, l\u2019equipaggio ha visto il Sole nascondersi dietro la Luna per quasi un\u2019ora.",
            'מהצד הרחוק ראה הצוות את השמש מסתתרת מאחורי הירח במשך כמעט שעה.'],
 A2[5][3]: ["Koch, Glover, Hansen et Wiseman quittent Orion pour le radeau « front porch » après l'amerrissage près de San Diego.",
            "Koch, Glover, Hansen y Wiseman salen de Orion a la balsa 'front porch' tras amarizar cerca de San Diego.",
            'كوك وغلوفر وهانسن ووايزمان يغادرون Orion إلى الطوف المسمى "الشرفة الأمامية" بعد الهبوط قرب سان دييغو.',
            "Koch, Glover, Hansen e Wiseman lasciano Orion per la zattera «front porch» dopo l\u2019ammaraggio vicino a San Diego.",
            'קוך, גלובר, הנסן ווייזמן יוצאים מ-Orion אל הרפסודה "המרפסת הקדמית" אחרי הנחיתה בים ליד סן דייגו.'],
}
ALT = {
 A1[0][4]: ["La fusée SLS de la NASA décollant de nuit avec Orion pour Artemis I", 'El cohete SLS de la NASA despegando de noche con Orion en Artemis I', 'صاروخ SLS التابع لناسا ينطلق ليلًا حاملًا Orion في مهمة Artemis I', 'Il razzo SLS della NASA decolla di notte con Orion per Artemis I', 'טיל ה-SLS של NASA ממריא בלילה עם Orion במשימת Artemis I'],
 A1[1][4]: ["La face cachée de la Lune derrière une partie du vaisseau Orion", 'La cara oculta de la Luna tras parte de la nave Orion', 'الجانب البعيد من القمر خلف جزء من مركبة Orion', 'La faccia nascosta della Luna oltre una parte della navicella Orion', 'הצד הרחוק של הירח מעבר לחלק מחללית Orion'],
 A1[2][4]: ['Orion avec la Terre et la Lune au loin', 'Orion con la Tierra y la Luna a lo lejos', 'Orion مع الأرض والقمر في البعيد', 'Orion con la Terra e la Luna in lontananza', 'Orion עם כדור הארץ והירח במרחק'],
 A1[3][4]: ['La Terre se levant derrière le bord de la Lune, à côté d\u2019Orion', 'La Tierra saliendo tras el borde de la Luna junto a Orion', 'الأرض تشرق خلف حافة القمر بجوار Orion', 'La Terra che sorge dietro il bordo della Luna accanto a Orion', 'כדור הארץ זורח מאחורי שפת הירח לצד Orion'],
 A1[4][4]: ['Orion descendant sous des parachutes orange et blancs au-dessus du Pacifique', 'Orion descendiendo bajo paracaídas naranjas y blancos sobre el Pacífico', 'Orion تهبط تحت مظلات برتقالية وبيضاء فوق المحيط الهادئ', 'Orion che scende sotto paracadute arancioni e bianchi sul Pacifico', 'Orion יורדת תחת מצנחים כתומים ולבנים מעל האוקיינוס השקט'],
 A1[5][4]: ["La capsule Orion dans le radier de l'USS Portland avec l'équipe de récupération", 'La cápsula Orion dentro del dique del USS Portland con el equipo de recuperación', 'كبسولة Orion داخل الحوض الداخلي للسفينة USS Portland مع فريق الاسترداد', 'La capsula Orion nel bacino della USS Portland con la squadra di recupero', 'קפסולת Orion בתוך תא העגינה של USS Portland עם צוות החילוץ'],
 A2[0][4]: ["La fusée SLS décollant du complexe de lancement 39B avec l'équipage d'Artemis II", 'El cohete SLS despegando del Complejo de Lanzamiento 39B con la tripulación de Artemis II', 'صاروخ SLS ينطلق من مجمع الإطلاق 39B حاملًا طاقم Artemis II', "Il razzo SLS decolla dal Launch Complex 39B con l\u2019equipaggio di Artemis II", 'טיל ה-SLS ממריא ממתחם השיגור 39B עם צוות Artemis II'],
 A2[1][4]: ['Une Terre sombre à contre-jour, bordée d\u2019un fin liseré lumineux, vue depuis Orion', 'Una Tierra oscura a contraluz con un fino borde brillante, vista desde Orion', 'أرض مظلمة مضاءة من الخلف بحافة رفيعة لامعة، كما تُرى من Orion', 'Una Terra scura in controluce con un sottile bordo luminoso, vista da Orion', 'כדור ארץ כהה מואר מאחור עם שוליים דקים בהירים, כפי שנראה מ-Orion'],
 A2[2][4]: ["L'astronaute Jeremy Hansen prenant des photos par un hublot d'Orion", 'El astronauta Jeremy Hansen tomando fotos por una ventana de Orion', 'رائد الفضاء جيريمي هانسن يلتقط صورًا من نافذة Orion', "L\u2019astronauta Jeremy Hansen scatta foto da un finestrino di Orion", "האסטרונאוט ג'רמי הנסן מצלם דרך חלון של Orion"],
 A2[3][4]: ['Une petite Terre partiellement éclairée se couchant derrière l\u2019horizon cratérisé de la Lune', 'Una pequeña Tierra parcialmente iluminada poniéndose tras el horizonte lleno de cráteres de la Luna', 'أرض صغيرة مضاءة جزئيًا تغرب خلف أفق القمر المليء بالفوهات', 'Una piccola Terra parzialmente illuminata che tramonta dietro l\u2019orizzonte craterizzato della Luna', 'כדור ארץ קטן ומואר בחלקו שוקע מאחורי האופק המכותש של הירח'],
 A2[4][4]: ['Le disque sombre de la Lune entouré d\u2019un halo lumineux lors d\u2019une éclipse solaire vue depuis Orion', 'El disco oscuro de la Luna rodeado de un halo brillante durante un eclipse solar visto desde Orion', 'قرص القمر المظلم تحيط به هالة متوهجة أثناء كسوف للشمس شوهد من Orion', 'Il disco scuro della Luna circondato da un alone luminoso durante un\u2019eclissi solare vista da Orion', 'הדיסקה הכהה של הירח מוקפת הילה זוהרת במהלך ליקוי חמה שנראה מ-Orion'],
 A2[5][4]: ["Les quatre astronautes d'Artemis II sur un radeau gonflable à côté d'Orion dans le Pacifique", 'Los cuatro astronautas de Artemis II en una balsa inflable junto a Orion en el Pacífico', 'رواد Artemis II الأربعة على طوف قابل للنفخ بجوار Orion في المحيط الهادئ', "I quattro astronauti di Artemis II su una zattera gonfiabile accanto a Orion nel Pacifico", 'ארבעת אסטרונאוטי Artemis II על רפסודה מתנפחת לצד Orion באוקיינוס השקט'],
}
PH = ['Photo : ', 'Foto: ', 'صورة: ', 'Foto: ', 'צילום: ']
for i, lang in enumerate(LANGS):
    p = f'i18n/{lang}.json'; m = json.load(open(p, encoding='utf-8')); before = dict(m)
    for k, v in list(T.items()) + list(ALT.items()): m[k] = v[i]
    for x in A1 + A2: m[x[5]] = PH[i] + x[5][len('Photo: '):]
    if m != before: json.dump(m, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

CSS = '''/* ARTEMIS-GALLERY:START (generated by scripts/build-artemis-gallery.py) */
body.artemis-page .art-gallery { max-width: 1200px; margin: 2rem auto; padding: 0 1.25rem; }
body.artemis-page .art-gallery h2 { text-align: center; margin: 0 0 .3rem; }
body.artemis-page .art-gallery .ag-intro { text-align: center; margin: 0 auto .9rem; max-width: 48rem; font-size: .95rem; opacity: .85; }
body.artemis-page .art-gallery .ag-mission { font-size: 1.05rem; margin: 1.1rem 0 .55rem; }
body.artemis-page .art-gallery .ag-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .75rem; align-items: start; }
body.artemis-page .art-gallery .ag-item { margin: 0; border: 1px solid rgba(127,127,127,.28); border-radius: 10px; overflow: hidden; }
body.artemis-page .art-gallery .ag-link { display: block; }
body.artemis-page .art-gallery .ag-item img { display: block; width: 100%; height: auto; aspect-ratio: 3 / 2; object-fit: cover; }
body.artemis-page .art-gallery figcaption { padding: .5rem .7rem .6rem; font-size: .86rem; line-height: 1.4; }
body.artemis-page .art-gallery .ag-meta { display: flex; flex-wrap: wrap; gap: .1rem .5rem; align-items: baseline; margin-bottom: .15rem; }
body.artemis-page .art-gallery .ag-stage { font-size: .7rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: #3fa9f5; }
body.artemis-page .art-gallery .ag-date { font-size: .78rem; font-weight: 600; opacity: .85; }
body.artemis-page .art-gallery .ag-cap { display: block; }
body.artemis-page .art-gallery .ag-credit { display: block; margin-top: .25rem; font-size: .7rem; opacity: .7; overflow-wrap: anywhere; }
@media (max-width: 900px) { body.artemis-page .art-gallery .ag-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 600px) { body.artemis-page .art-gallery .ag-grid { grid-template-columns: 1fr; } }
/* ARTEMIS-GALLERY:END */'''
css = open('styles.css', encoding='utf-8').read()
css2 = re.sub(r'/\* ARTEMIS-GALLERY:START.*?ARTEMIS-GALLERY:END \*/', lambda m: CSS, css, flags=re.S) if 'ARTEMIS-GALLERY:START' in css else css.rstrip('\n') + '\n' + CSS + '\n'
if css2 != css: open('styles.css', 'w', encoding='utf-8').write(css2)
print(f'build-artemis-gallery: {len(A1) + len(A2)} photos, page {"updated" if s != s0 else "unchanged"}')
