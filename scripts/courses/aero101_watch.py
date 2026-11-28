"""AERO 101 Watch and learn lectures. Bryan approved this pilot on November 25, 2026.

Box and tier labels, and the one-line reasons, are SI translations. No native speaker has reviewed them.
Every video id was checked with YouTube oEmbed (HTTP 200, embeddable) and the watch page had no
Unlisted badge. Lengths already on the page were measured from the media. Lengths added in the
open-license pass: MIT 16.885 from the Archive.org file length; TU Delft and the added NASA videos
from YouTube's duration label on that video's own search result. Do not add an id that has not been checked.
"""
import html
import json
import os

from courses import nasa_film as NF

HERE = os.path.dirname(os.path.abspath(__file__))
_TR = json.load(open(os.path.join(HERE, '..', '..', 'i18n', 'courses', '_shared.json'), encoding='utf8'))

# Timed captions could not be retrieved. Say so, and do not invent a transcript or chapters.
MISSING = {
    'en': 'A timed caption transcript could not be retrieved for this film, so the transcript, caption menu, and chapter marks are omitted.',
    'fr': 'Une transcription minutée n’a pas pu être récupérée pour ce film. La transcription, le menu des sous-titres et les chapitres sont donc omis.',
    'es': 'No se pudo recuperar una transcripción con tiempos de esta película, así que se omiten la transcripción, el menú de subtítulos y los capítulos.',
    'ar': 'تعذّر جلب تفريغ موقوت لهذا الفيلم، لذا حُذف التفريغ وقائمة الترجمة والفصول.',
    'it': 'Non è stato possibile recuperare una trascrizione con i tempi di questo film, quindi trascrizione, menu dei sottotitoli e capitoli sono omessi.',
    'he': 'לא ניתן היה לאחזר תמליל מתוזמן לסרט הזה, ולכן התמליל, תפריט הכתוביות והפרקים הושמטו.',
}
CITE_ND = {
    'en': 'The publication date was not in the source record, so the citation uses n.d.',
    'fr': 'La date de publication n’était pas dans la notice, donc la citation indique n.d.',
    'es': 'La fecha de publicación no estaba en la ficha, así que la cita usa n.d.',
    'ar': 'تاريخ النشر غير موجود في بيانات المصدر، لذا تستخدم الإحالة n.d.',
    'it': 'La data di pubblicazione non era nella scheda, quindi la citazione usa n.d.',
    'he': 'תאריך הפרסום לא הופיע ברשומת המקור, ולכן האזכור משתמש ב-n.d.',
}

CC = 'https://creativecommons.org/licenses/by-nc-sa/4.0/'
OCW_TERMS = 'https://ocw.mit.edu/pages/privacy-and-terms-of-use/'
NASA_MEDIA = 'https://www.nasa.gov/nasa-brand-center/images-and-media/'
OCW_16_687 = 'MIT 16.687 Private Pilot Ground School (IAP 2019), MIT OpenCourseWare'
OCW_16_346 = 'MIT 16.346 Astrodynamics (Fall 2008), MIT OpenCourseWare'
OCW_16_885 = 'MIT 16.885J Aircraft Systems Engineering (Fall 2005), MIT OpenCourseWare'
DELFT = 'TU Delft, Introduction to Aeronautical Engineering'

# SI drafts. Keys: box, start, deep, seasoned, play, added, nasa_note, nasa_lic, gov, univ_lic.
LABELS = {
    'en': {
        'box': 'Watch and learn', 'start': 'Start here', 'deep': 'Go deeper', 'seasoned': 'Seasoned',
        'play': 'Play', 'added': 'Watch and learn lectures added',
        'nasa_note': 'Linked for free study only; Saving Planets is not affiliated with or endorsed by NASA.',
        'nasa_lic': 'NASA images and media guidelines', 'gov': 'U.S. government work',
        'univ_lic': 'official channel; free to watch; embedding enabled',
    },
    'fr': {
        'box': 'Regarder pour apprendre', 'start': 'Commencez ici', 'deep': 'Pour aller plus loin', 'seasoned': 'Niveau avancé',
        'play': 'Lire', 'added': 'leçons « Regarder pour apprendre » ajoutées',
        'nasa_note': 'Lien fourni uniquement pour l’étude gratuite ; Saving Planets n’est ni affilié à la NASA ni soutenu par elle.',
        'nasa_lic': 'directives de la NASA sur les images et les médias', 'gov': 'œuvre du gouvernement des États-Unis',
        'univ_lic': 'chaîne officielle ; visionnage gratuit ; intégration autorisée',
    },
    'es': {
        'box': 'Ver y aprender', 'start': 'Empiece aquí', 'deep': 'Para profundizar', 'seasoned': 'Nivel avanzado',
        'play': 'Reproducir', 'added': 'lecciones «Ver y aprender» añadidas',
        'nasa_note': 'Enlace solo para estudio gratuito; Saving Planets no está afiliado a la NASA ni cuenta con su respaldo.',
        'nasa_lic': 'directrices de la NASA sobre imágenes y medios', 'gov': 'obra del gobierno de EE. UU.',
        'univ_lic': 'canal oficial; visionado gratuito; inserción permitida',
    },
    'ar': {
        'box': 'شاهد لتتعلّم', 'start': 'ابدأ من هنا', 'deep': 'للتعمّق', 'seasoned': 'مستوى متقدم',
        'play': 'تشغيل', 'added': 'أُضيفت دروس «شاهد لتتعلّم»',
        'nasa_note': 'الرابط للدراسة المجانية فقط؛ Saving Planets غير تابع لناسا ولا يحظى بتأييدها.',
        'nasa_lic': 'إرشادات ناسا للصور والوسائط', 'gov': 'عمل لحكومة الولايات المتحدة',
        'univ_lic': 'قناة رسمية؛ المشاهدة مجانية؛ التضمين مسموح',
    },
    'it': {
        'box': 'Guarda e impara', 'start': 'Inizia qui', 'deep': 'Per approfondire', 'seasoned': 'Livello avanzato',
        'play': 'Riproduci', 'added': 'aggiunte le lezioni «Guarda e impara»',
        'nasa_note': 'Link fornito solo per lo studio gratuito; Saving Planets non è affiliato alla NASA né approvato da essa.',
        'nasa_lic': 'linee guida NASA su immagini e media', 'gov': 'opera del governo degli Stati Uniti',
        'univ_lic': 'canale ufficiale; visione gratuita; incorporamento consentito',
    },
    'he': {
        'box': 'צפו ולמדו', 'start': 'התחילו כאן', 'deep': 'להעמקה', 'seasoned': 'רמה מתקדמת',
        'play': 'הפעלה', 'added': 'נוספו שיעורי «צפו ולמדו»',
        'nasa_note': 'הקישור מיועד ללימוד חינמי בלבד; Saving Planets אינו קשור לנאס״א ואינו נתמך על ידה.',
        'nasa_lic': 'הנחיות נאס״א לתמונות ולמדיה', 'gov': 'יצירה של ממשלת ארצות הברית',
        'univ_lic': 'ערוץ רשמי; צפייה חינם; הטמעה מותרת',
    },
}

# why[lang] is one sentence. kind is mit, nasa, or delft.
VIDEOS = {
    # The Wright Brothers film is Unit 1's featured player, so it is not repeated here.
    1: [{
        'tier': 'deep', 'id': 'j0SaIXktsQg', 'length': '15:00', 'kind': 'delft',
        'title': 'History of Flight',
        'page': 'https://www.youtube.com/watch?v=j0SaIXktsQg',
        'source': DELFT,
        'why': {
            'en': 'TU Delft’s lecture on the history of flight, from the earliest ideas to the modern airplane.',
            'fr': 'Le cours de TU Delft sur l’histoire du vol, des premières idées à l’avion moderne.',
            'es': 'La clase de TU Delft sobre la historia del vuelo, desde las primeras ideas hasta el avión moderno.',
            'ar': 'محاضرة جامعة دلفت للتكنولوجيا عن تاريخ الطيران، من الأفكار الأولى إلى الطائرة الحديثة.',
            'it': 'La lezione della TU Delft sulla storia del volo, dalle prime idee all’aeroplano moderno.',
            'he': 'שיעור של אוניברסיטת דלפט על תולדות הטיסה, מהרעיונות הראשונים עד המטוס המודרני.',
        },
    }, {
        'tier': 'seasoned', 'id': 'IHVf3ukiIiA', 'length': '1:49:43', 'kind': 'mit',
        'title': 'Lecture 19: Design Process as it Relates to the Shuttle',
        'page': 'https://ocw.mit.edu/courses/16-885j-aircraft-systems-engineering-fall-2005/resources/lecture-19/',
        'source': OCW_16_885,
        'why': {
            'en': 'A graduate lecture on how the design process shaped the Space Shuttle.',
            'fr': 'Un cours de cycle supérieur sur la façon dont le processus de conception a façonné la navette spatiale.',
            'es': 'Una clase de posgrado sobre cómo el proceso de diseño dio forma al transbordador espacial.',
            'ar': 'محاضرة دراسات عليا عن كيف شكّلت عملية التصميم مكوك الفضاء.',
            'it': 'Una lezione avanzata su come il processo di progettazione ha dato forma allo Space Shuttle.',
            'he': 'שיעור מתקדם על איך תהליך התכן עיצב את מעבורת החלל.',
        },
    }],
    2: [{
        'tier': 'start', 'id': 'vLh4Zb0dgOE', 'length': '6:41', 'kind': 'nasa',
        'title': 'NASA Now: Earth’s Atmosphere: Earth Science Week',
        'page': 'https://www.youtube.com/watch?v=vLh4Zb0dgOE',
        'source': 'NASA',
        'why': {
            'en': 'A NASA scientist walks through the layers of the atmosphere and what the air is made of.',
            'fr': 'Un scientifique de la NASA parcourt les couches de l’atmosphère et de quoi l’air est fait.',
            'es': 'Un científico de la NASA recorre las capas de la atmósfera y de qué está hecho el aire.',
            'ar': 'عالم من ناسا يشرح طبقات الغلاف الجوي وممّ يتكون الهواء.',
            'it': 'Uno scienziato della NASA percorre gli strati dell’atmosfera e di che cosa è fatta l’aria.',
            'he': 'מדען של נאס״א עובר על שכבות האטמוספירה וממה האוויר עשוי.',
        },
    }, {
        'tier': 'deep', 'id': 'Hdix6qj9qs8', 'length': '17:00', 'kind': 'delft',
        'title': 'The ISA, Part I',
        'page': 'https://www.youtube.com/watch?v=Hdix6qj9qs8',
        'source': DELFT,
        'why': {
            'en': 'The first part of TU Delft’s lecture on the International Standard Atmosphere.',
            'fr': 'La première partie du cours de TU Delft sur l’atmosphère type internationale.',
            'es': 'La primera parte de la clase de TU Delft sobre la atmósfera estándar internacional.',
            'ar': 'الجزء الأول من محاضرة جامعة دلفت للتكنولوجيا عن الغلاف الجوي القياسي الدولي.',
            'it': 'La prima parte della lezione della TU Delft sull’atmosfera standard internazionale.',
            'he': 'החלק הראשון של שיעור אוניברסיטת דלפט על האטמוספירה התקנית הבין-לאומית.',
        },
    }],
    3: [{
        'tier': 'start', 'id': 'JPD0Be4eSos', 'length': '12:25', 'kind': 'delft',
        'title': 'Lift',
        'page': 'https://www.youtube.com/watch?v=JPD0Be4eSos',
        'source': DELFT,
        'why': {
            'en': 'How a wing makes lift, from TU Delft’s introduction to aeronautical engineering.',
            'fr': 'Comment une aile produit la portance, dans l’introduction à l’ingénierie aéronautique de TU Delft.',
            'es': 'Cómo un ala produce sustentación, en la introducción a la ingeniería aeronáutica de TU Delft.',
            'ar': 'كيف يولّد الجناح الرفع، في مقدمة هندسة الطيران من جامعة دلفت للتكنولوجيا.',
            'it': 'Come un’ala genera portanza, nell’introduzione all’ingegneria aeronautica della TU Delft.',
            'he': 'איך כנף יוצרת עילוי, במבוא להנדסה אווירונאוטית של אוניברסיטת דלפט.',
        },
    }, {
        'tier': 'deep', 'id': 'edLnZgF9mUg', 'length': '1:12:07', 'kind': 'mit',
        'title': 'Lecture 2: Airplane Aerodynamics',
        'page': 'https://ocw.mit.edu/courses/16-687-private-pilot-ground-school-january-iap-2019/resources/lecture-2-airplane-aerodynamics/',
        'source': OCW_16_687,
        'why': {
            'en': 'The ground-school lecture on lift, drag, and how a wing is controlled.',
            'fr': 'Le cours de l’école au sol sur la portance, la traînée et le contrôle d’une aile.',
            'es': 'La clase de escuela de tierra sobre la sustentación, la resistencia y el control de un ala.',
            'ar': 'محاضرة المدرسة الأرضية عن الرفع والسحب وكيف يُتحكم في الجناح.',
            'it': 'La lezione di scuola a terra su portanza, resistenza e controllo di un’ala.',
            'he': 'שיעור בית הספר הקרקעי על עילוי, גרר ואיך שולטים בכנף.',
        },
    }, {
        'tier': 'seasoned', 'id': '2QRfkG7jOfY', 'length': '1:50:38', 'kind': 'mit',
        'title': 'Lecture 7: Aerodynamics (From Subsonic to Hypersonic and Back)',
        'page': 'https://ocw.mit.edu/courses/16-885j-aircraft-systems-engineering-fall-2005/resources/lecture-7/',
        'source': OCW_16_885,
        'why': {
            'en': 'A graduate lecture on aerodynamics from subsonic flight through hypersonic and back.',
            'fr': 'Un cours de cycle supérieur sur l’aérodynamique, du subsonique à l’hypersonique et retour.',
            'es': 'Una clase de posgrado sobre aerodinámica, del vuelo subsónico al hipersónico y de vuelta.',
            'ar': 'محاضرة دراسات عليا في الديناميكا الهوائية من الطيران دون الصوتي إلى فوق الصوتي ثم العودة.',
            'it': 'Una lezione avanzata di aerodinamica, dal volo subsonico all’ipersonico e ritorno.',
            'he': 'שיעור מתקדם באווירודינמיקה, מטיסה תת-קולית עד על-קולית גבוהה ובחזרה.',
        },
    }],
    4: [{
        'tier': 'start', 'id': 'rCbPkb85Q4o', 'length': '9:23', 'kind': 'delft',
        'title': 'Aerofoil Profiles',
        'page': 'https://www.youtube.com/watch?v=rCbPkb85Q4o',
        'source': DELFT,
        'why': {
            'en': 'How an aerofoil profile is defined, in TU Delft’s lecture on wing sections.',
            'fr': 'Comment se définit un profil d’aile, dans le cours de TU Delft sur les profils.',
            'es': 'Cómo se define un perfil aerodinámico, en la clase de TU Delft sobre perfiles de ala.',
            'ar': 'كيف يُعرَّف مقطع الجناح، في محاضرة جامعة دلفت للتكنولوجيا عن مقاطع الأجنحة.',
            'it': 'Come si definisce un profilo alare, nella lezione della TU Delft sulle sezioni d’ala.',
            'he': 'איך מגדירים פרופיל אווירודינמי, בשיעור של אוניברסיטת דלפט על חתכי כנף.',
        },
    }],
    5: [{
        'tier': 'start', 'id': 'A-8Xfh1Ibmw', 'length': '9:52', 'kind': 'delft',
        'title': 'Horizontal Flight: Introduction',
        'page': 'https://www.youtube.com/watch?v=A-8Xfh1Ibmw',
        'source': DELFT,
        'why': {
            'en': 'Level flight as the start of performance: lift balances weight, and thrust balances drag.',
            'fr': 'Le vol en palier comme point de départ des performances : la portance équilibre le poids, et la poussée équilibre la traînée.',
            'es': 'El vuelo nivelado como punto de partida del rendimiento: la sustentación equilibra el peso y el empuje equilibra la resistencia.',
            'ar': 'الطيران الأفقي كنقطة بداية للأداء: الرفع يوازن الوزن، والدفع يوازن السحب.',
            'it': 'Il volo livellato come punto di partenza delle prestazioni: la portanza equilibra il peso e la spinta equilibra la resistenza.',
            'he': 'טיסה ישרה ואופקית כנקודת הפתיחה של הביצועים: העילוי מאזן את המשקל, והדחף מאזן את הגרר.',
        },
    }, {
        'tier': 'deep', 'id': '3sB64Au76h0', 'length': '1:05:32', 'kind': 'mit',
        'title': 'Lecture 12: Aircraft Performance',
        'page': 'https://ocw.mit.edu/courses/16-687-private-pilot-ground-school-january-iap-2019/resources/lecture-12-aircraft-performance/',
        'source': OCW_16_687,
        'why': {
            'en': 'The ground-school lecture on predicting performance in every phase of flight.',
            'fr': 'Le cours de l’école au sol sur la prévision des performances à chaque phase de vol.',
            'es': 'La clase de escuela de tierra sobre cómo predecir el rendimiento en cada fase del vuelo.',
            'ar': 'محاضرة المدرسة الأرضية عن التنبؤ بالأداء في كل مرحلة من الطيران.',
            'it': 'La lezione di scuola a terra su come prevedere le prestazioni in ogni fase del volo.',
            'he': 'שיעור בית הספר הקרקעי על חיזוי ביצועים בכל שלב של הטיסה.',
        },
    }],
    6: [{
        'tier': 'start', 'id': 'hoR770EIbkQ', 'length': '4:05', 'kind': 'delft',
        'title': 'Stability Introduction',
        'page': 'https://www.youtube.com/watch?v=hoR770EIbkQ',
        'source': DELFT,
        'why': {
            'en': 'TU Delft’s short introduction to what stability means for an airplane.',
            'fr': 'La courte introduction de TU Delft à ce que la stabilité signifie pour un avion.',
            'es': 'La breve introducción de TU Delft a lo que significa la estabilidad para un avión.',
            'ar': 'المقدمة القصيرة من جامعة دلفت للتكنولوجيا لمعنى الاستقرار للطائرة.',
            'it': 'La breve introduzione della TU Delft a che cosa significa la stabilità per un aeroplano.',
            'he': 'המבוא הקצר של אוניברסיטת דלפט למשמעות היציבות של מטוס.',
        },
    }, {
        'tier': 'deep', 'id': 'jh58Em8WmJI', 'length': '32:00', 'kind': 'delft',
        'title': 'Longitudinal Stability',
        'page': 'https://www.youtube.com/watch?v=jh58Em8WmJI',
        'source': DELFT,
        'why': {
            'en': 'How the tail and the center of gravity set an airplane’s longitudinal stability.',
            'fr': 'Comment l’empennage et le centre de gravité fixent la stabilité longitudinale d’un avion.',
            'es': 'Cómo la cola y el centro de gravedad fijan la estabilidad longitudinal de un avión.',
            'ar': 'كيف يحدّد الذيل ومركز الثقل الاستقرار الطولي للطائرة.',
            'it': 'Come i piani di coda e il baricentro determinano la stabilità longitudinale di un aeroplano.',
            'he': 'איך הזנב ומרכז הכובד קובעים את היציבות האורכית של מטוס.',
        },
    }, {
        'tier': 'seasoned', 'id': 'n068fel-W9I', 'length': '1:06:48', 'kind': 'mit',
        'title': 'Special Lecture: F-22 Flight Controls',
        'page': 'https://ocw.mit.edu/courses/16-687-private-pilot-ground-school-january-iap-2019/resources/special-lecture-f-22-flight-controls/',
        'source': OCW_16_687,
        'why': {
            'en': 'An F-22 pilot explains the fighter’s flight controls, beyond the first-year stability definitions.',
            'fr': 'Un pilote de F-22 explique les commandes de vol du chasseur, au-delà des définitions de stabilité de première année.',
            'es': 'Un piloto de F-22 explica los controles de vuelo del caza, más allá de las definiciones de estabilidad de primer año.',
            'ar': 'طيار طائرة F-22 يشرح أدوات التحكم في الطائرة المقاتلة، بعد تعريفات الاستقرار في السنة الأولى.',
            'it': 'Un pilota di F-22 spiega i comandi di volo del caccia, oltre le definizioni di stabilità del primo anno.',
            'he': 'טייס F-22 מסביר את בקרות הטיסה של המטוס, מעבר להגדרות היציבות של השנה הראשונה.',
        },
    }],
    7: [{
        'tier': 'start', 'id': 'TcKPczKDLqc', 'length': '6:40', 'kind': 'nasa',
        'title': 'NASA Now: Jet Engine Testing',
        'page': 'https://www.youtube.com/watch?v=TcKPczKDLqc',
        'source': 'NASA Glenn Research Center, NASA',
        'why': {
            'en': 'A NASA Glenn test engineer shows how a jet engine compresses air, burns fuel, and makes thrust.',
            'fr': 'Un ingénieur d’essai de la NASA Glenn montre comment un réacteur comprime l’air, brûle le carburant et produit la poussée.',
            'es': 'Un ingeniero de ensayos de NASA Glenn muestra cómo un motor a reacción comprime el aire, quema combustible y produce empuje.',
            'ar': 'مهندس اختبار في ناسا غلين يبيّن كيف يضغط المحرك النفاث الهواء ويحرق الوقود وينتج الدفع.',
            'it': 'Un ingegnere di prova della NASA Glenn mostra come un motore a getto comprime l’aria, brucia il carburante e produce spinta.',
            'he': 'מהנדס ניסוי בנאס״א גלן מראה איך מנוע סילון דוחס אוויר, שורף דלק ויוצר דחף.',
        },
    }, {
        'tier': 'deep', 'id': 'cgnL8v8YRcs', 'length': '14:32', 'kind': 'delft',
        'title': 'Propulsion',
        'page': 'https://www.youtube.com/watch?v=cgnL8v8YRcs',
        'source': DELFT,
        'why': {
            'en': 'TU Delft’s introduction to how an aircraft propulsion system produces thrust.',
            'fr': 'L’introduction de TU Delft à la façon dont un système de propulsion produit la poussée.',
            'es': 'La introducción de TU Delft a cómo un sistema de propulsión produce empuje.',
            'ar': 'مقدمة جامعة دلفت للتكنولوجيا لكيفية إنتاج منظومة الدفع للقوة الدافعة.',
            'it': 'L’introduzione della TU Delft a come un sistema di propulsione produce spinta.',
            'he': 'המבוא של אוניברסיטת דלפט לאיך מערכת הנעה יוצרת דחף.',
        },
    }],
    8: [{
        'tier': 'seasoned', 'id': 'uow6v1EuybE', 'length': '2:00:07', 'kind': 'mit',
        'title': 'Lecture 6: Propulsion - Space Shuttle Main Engines',
        'page': 'https://ocw.mit.edu/courses/16-885j-aircraft-systems-engineering-fall-2005/resources/lecture-6/',
        'source': OCW_16_885,
        'why': {
            'en': 'A graduate lecture on the Space Shuttle’s main engines.',
            'fr': 'Un cours de cycle supérieur sur les moteurs principaux de la navette spatiale.',
            'es': 'Una clase de posgrado sobre los motores principales del transbordador espacial.',
            'ar': 'محاضرة دراسات عليا عن المحركات الرئيسية لمكوك الفضاء.',
            'it': 'Una lezione avanzata sui motori principali dello Space Shuttle.',
            'he': 'שיעור מתקדם על המנועים הראשיים של מעבורת החלל.',
        },
    }],
    9: [{
        'tier': 'start', 'id': 'wjOOrr2uPuU', 'length': '6:55', 'kind': 'nasa',
        'title': 'Solar System Dynamics: Orbits and Kepler’s Laws',
        'page': 'https://www.youtube.com/watch?v=wjOOrr2uPuU',
        'source': 'NASA Solar System',
        'why': {
            'en': 'Kepler’s laws: the rules that describe how one body orbits another.',
            'fr': 'Les lois de Kepler : les règles qui décrivent comment un corps orbite autour d’un autre.',
            'es': 'Las leyes de Kepler: las reglas que describen cómo un cuerpo orbita alrededor de otro.',
            'ar': 'قوانين كبلر: القواعد التي تصف كيف يدور جسم حول جسم آخر.',
            'it': 'Le leggi di Keplero: le regole che descrivono come un corpo orbita intorno a un altro.',
            'he': 'חוקי קפלר: הכללים שמתארים איך גוף חג סביב גוף אחר.',
        },
    }, {
        'tier': 'deep', 'id': 'Am7EwmxBAW8', 'length': '36:00', 'kind': 'nasa',
        'title': 'Space Flight: The Application of Orbital Mechanics',
        'page': 'https://www.youtube.com/watch?v=Am7EwmxBAW8',
        'source': 'NASA STI Program',
        'why': {
            'en': 'A NASA primer on orbital mechanics, made for college physics students.',
            'fr': 'Une introduction de la NASA à la mécanique orbitale, faite pour des étudiants de physique à l’université.',
            'es': 'Una introducción de la NASA a la mecánica orbital, hecha para estudiantes universitarios de física.',
            'ar': 'مدخل من ناسا إلى ميكانيكا المدارات، أُعدّ لطلاب الفيزياء في الجامعة.',
            'it': 'Un’introduzione della NASA alla meccanica orbitale, pensata per studenti universitari di fisica.',
            'he': 'מבוא של נאס״א למכניקת מסלולים, שנכתב לסטודנטים לפיזיקה באוניברסיטה.',
        },
    }, {
        'tier': 'seasoned', 'id': 'SJI-SAs1Rnk', 'length': '1:19:26', 'kind': 'mit',
        'title': 'A Funny Thing Happened on the way to the Moon | MIT 16.346 Astrodynamics, Fall 2008',
        'page': 'https://ocw.mit.edu/courses/16-346-astrodynamics-fall-2008/resources/video-lecture/',
        'source': OCW_16_346,
        'why': {
            'en': 'Richard Battin’s graduate astrodynamics lecture on flying a trajectory to the Moon.',
            'fr': 'Le cours d’astrodynamique de cycle supérieur de Richard Battin sur une trajectoire vers la Lune.',
            'es': 'La clase de astrodinámica de posgrado de Richard Battin sobre una trayectoria a la Luna.',
            'ar': 'محاضرة ريتشارد باتن للدراسات العليا في ديناميكا الفضاء عن مسار إلى القمر.',
            'it': 'La lezione di astrodinamica avanzata di Richard Battin su una traiettoria verso la Luna.',
            'he': 'שיעור האסטרודינמיקה המתקדם של ריצ׳רד באטין על מסלול אל הירח.',
        },
    }],
    10: [{
        'tier': 'start', 'id': 'rROmLTibG5w', 'length': '6:46', 'kind': 'nasa',
        'title': 'NASA Tests Model Wing to Bring Fuel Savings to Commercial Aviation',
        'page': 'https://www.youtube.com/watch?v=rROmLTibG5w',
        'source': 'NASA Armstrong Flight Research Center',
        'why': {
            'en': 'NASA flight-tests a laminar-flow wing built to cut fuel burn on future airliners.',
            'fr': 'La NASA essaie en vol une aile à écoulement laminaire conçue pour réduire la consommation des futurs avions de ligne.',
            'es': 'La NASA prueba en vuelo un ala de flujo laminar hecha para reducir el consumo de los futuros aviones de línea.',
            'ar': 'تختبر ناسا في الطيران جناحًا ذا جريان طبقي صُمم لخفض استهلاك الوقود في طائرات الركاب المقبلة.',
            'it': 'La NASA prova in volo un’ala a flusso laminare pensata per ridurre il consumo dei futuri aerei di linea.',
            'he': 'נאס״א בוחנת בטיסה כנף בזרימה למינרית שנועדה להפחית את צריכת הדלק של מטוסי נוסעים עתידיים.',
        },
    }],
}

CSS = (
    '.crs-watch{margin:1rem 0;border:1px solid rgba(255,255,255,.22);border-radius:16px;background:rgba(255,255,255,.05)}'
    '.crs-watch>summary{cursor:pointer;min-height:44px;display:flex;align-items:center;padding:.35rem 1rem;list-style:none}'
    '.crs-watch>summary::-webkit-details-marker{display:none}'
    '.crs-watch>summary::before{content:"▸";margin-inline-end:.55rem}'
    '.crs-watch[open]>summary::before{content:"▾"}'
    'html[dir="rtl"] .crs-watch>summary::before{content:"◂"}'
    '.crs-watch>summary{flex-wrap:wrap}'
    '.crs-watch>summary h3{margin:0;min-width:0;overflow-wrap:anywhere}'
    '.crs-watch-tier{padding:0 1rem 1rem}'
    '.crs-watch h4{margin:1rem 0 .35rem;font-size:1.02rem}'
    '.crs-watch-frame{position:relative;aspect-ratio:16/9;margin:.55rem 0;border-radius:12px;overflow:hidden;background:#071422}'
    '.crs-watch-play{appearance:none;border:0;padding:0;margin:0;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.75rem;cursor:pointer;color:#fff;background:linear-gradient(160deg,#12304d,#071422 70%);font:inherit}'
    '.crs-watch-play:focus-visible{outline:3px solid #ffd54a;outline-offset:-6px}'
    '.crs-watch-tri{display:block;width:0;height:0;border-style:solid;border-width:16px 0 16px 28px;border-color:transparent transparent transparent #fff}'
    '.crs-watch-cap{max-width:36rem;text-align:center;font-weight:700;padding:0 1rem}'
    '.crs-watch-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}'
)

# Loads nothing until a play button is clicked. The iframe is youtube-nocookie and is created only then.
JS = (
    '<script>'
    'document.addEventListener("click",function(e){'
    'var b=e.target.closest&&e.target.closest(".crs-watch-play");'
    'if(!b)return;'
    'var id=b.getAttribute("data-id")||"";'
    'if(!/^[A-Za-z0-9_-]{11}$/.test(id))return;'
    'var f=document.createElement("iframe");'
    'f.src="https://www.youtube-nocookie.com/embed/"+id+"?autoplay=1";'
    'f.title=b.getAttribute("data-title")||"";'
    'f.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen";'
    'f.allowFullscreen=true;'
    'f.referrerPolicy="strict-origin-when-cross-origin";'
    'b.replaceWith(f);'
    '});'
    '</script>'
)


def _esc(s):
    return html.escape(s, quote=True)


def _shared(lang, key):
    if lang == 'en':
        return key
    return _TR[key][lang]


def _credit(lang, vid):
    L = LABELS[lang]
    length = f'<bdi dir="ltr">{_esc(vid["length"])}</bdi>'
    source = f'<bdi dir="ltr" lang="en">{_esc(vid["source"])}</bdi>'
    if vid['kind'] == 'mit':
        note = _esc(_shared(lang, 'Linked for free study only; Saving Planets is not affiliated with or endorsed by this university.'))
        return (f'{length} · {source}. {_esc(_shared(lang, "License:"))} '
                f'<a href="{CC}" rel="noopener license">CC BY-NC-SA 4.0</a> · '
                f'<a href="{OCW_TERMS}" rel="noopener">{_esc(_shared(lang, "Terms of use"))}</a>. {note}')
    if vid['kind'] == 'nasa':
        return (f'{length} · {source}. {_esc(_shared(lang, "License:"))} '
                f'<a href="{NASA_MEDIA}" rel="noopener license">{_esc(L["nasa_lic"])}</a> ({_esc(L["gov"])}). {_esc(L["nasa_note"])}')
    if vid['kind'] == 'delft':
        note = _esc(_shared(lang, 'Linked for free study only; Saving Planets is not affiliated with or endorsed by this university.'))
        return (f'{length} · {source}. {_esc(_shared(lang, "License:"))} '
                f'<a href="{CC}" rel="noopener license">CC BY-NC-SA 4.0</a>. {note}')
    raise ValueError('unknown video kind ' + vid['kind'])


def _license_short(lang, vid):
    L = LABELS[lang]
    word = _esc(_shared(lang, 'License:'))
    if vid['kind'] == 'nasa':
        return (f'{word} <a href="{NASA_MEDIA}" rel="noopener license">{_esc(L["nasa_lic"])}</a> '
                f'({_esc(L["gov"])}).')
    if vid['kind'] == 'mit':
        return (f'{word} <a href="{CC}" rel="noopener license">CC BY-NC-SA 4.0</a> · '
                f'<a href="{OCW_TERMS}" rel="noopener">{_esc(_shared(lang, "Terms of use"))}</a>.')
    if vid['kind'] == 'delft':
        return f'{word} <a href="{CC}" rel="noopener license">CC BY-NC-SA 4.0</a>.'
    raise ValueError('unknown video kind ' + vid['kind'])


def _player(lang, vid):
    """Click-to-play Plyr. No autoplay: a unit can hold several films."""
    L = LABELS[lang]
    U = NF.UI[lang]
    pre = NF.prefix(lang)
    title = _esc(vid['title'])
    vid_id = vid['id']
    speeds = ''.join(
        f'<option value="{v}"' + (' selected' if v == '1' else '') + f'>{v}×</option>'
        for v in NF.SPEEDS
    )
    apa_id = f'cite-apa-{vid_id}'
    mla_id = f'cite-mla-{vid_id}'
    url = vid['page']
    author = vid['source']
    apa = f'{author}. (n.d.). {vid["title"]} [Video]. YouTube. {url}'
    mla = f'"{vid["title"]}." YouTube, uploaded by {author}, n.d., {url}.'
    play = (
        f'<span class="crs-film-play" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28">'
        f'<path fill="#fff" d="M8 5v14l11-7z"/></svg></span>'
    )
    return (
        f'<figure class="crs-film crs-film-deep" data-id="{vid_id}" data-lang="{lang}" '
        f'data-meta="{pre}assets/courses/watch-meta/{vid_id}.json" '
        f'data-plyr="{pre}{NF.PLYR_JS}" data-plyr-css="{pre}{NF.PLYR_CSS}">'
        f'<div class="crs-film-bar">'
        f'<span class="crs-film-badge">{_esc(L[vid["tier"]])}</span>'
        f'<span class="crs-film-time"><bdi dir="ltr">{_esc(vid["length"])}</bdi></span>'
        f'</div>'
        f'<div class="crs-film-stage"><div class="crs-film-frame">'
        f'<a class="crs-film-poster" href="{url}">'
        f'<img src="{pre}assets/courses/posters/{vid_id}.webp" alt="" width="480" height="360" '
        f'loading="lazy" decoding="async">'
        f'{play}'
        f'<span class="crs-film-poster-label">{_esc(L["play"])}: <bdi lang="en" dir="ltr">{title}</bdi></span>'
        f'</a></div>'
        f'<button type="button" class="crs-film-unmute" hidden>{_esc(U["unmute"])}</button></div>'
        f'<p class="crs-film-cc" aria-live="polite"></p>'
        f'<figcaption>'
        f'<span class="crs-film-title"><bdi lang="en" dir="ltr">{title}</bdi></span>'
        f'<span class="crs-film-credit">{_license_short(lang, vid)}</span>'
        f'</figcaption>'
        f'<div class="crs-film-tools">'
        f'<label>{_esc(U["speed"])} <select class="crs-film-speed" dir="ltr">{speeds}</select></label>'
        f'<details class="crs-film-cite"><summary>{_esc(U["cite"])}</summary>'
        f'<p class="crs-film-note">{_esc(CITE_ND[lang])}</p>'
        f'<p class="crs-film-cite-k">APA</p>'
        f'<p class="crs-film-cite-t" id="{apa_id}" lang="en" dir="ltr">{_esc(apa)}</p>'
        f'<button type="button" data-copy="{apa_id}" data-copied="{_esc(U["copied"])}">{_esc(U["copy"])}</button>'
        f'<p class="crs-film-cite-k">MLA</p>'
        f'<p class="crs-film-cite-t" id="{mla_id}" lang="en" dir="ltr">{_esc(mla)}</p>'
        f'<button type="button" data-copy="{mla_id}" data-copied="{_esc(U["copied"])}">{_esc(U["copy"])}</button>'
        f'</details></div>'
        f'<p class="crs-film-note">{_esc(MISSING[lang])}</p>'
        f'</figure>'
    )


def box(lang, unit):
    """One closed details box for unit 1..10. Tiers with no video are omitted."""
    L = LABELS[lang]
    ident = ' id="u1-watch"' if unit == 1 else ''
    parts = [f'<details class="crs-watch"{ident}><summary><h3>{_esc(L["box"])}</h3></summary>']
    for vid in VIDEOS[unit]:
        parts.append(
            f'<div class="crs-watch-tier"><h4>{_esc(L[vid["tier"]])}</h4>'
            f'<p><a href="{_esc(vid["page"])}" rel="noopener" lang="en">{_esc(vid["title"])}</a> ({_esc(_shared(lang, "in English"))})</p>'
            f'<p>{_esc(vid["why"][lang])}</p>'
            f'{_player(lang, vid)}'
            f'<p class="crs-src">{_credit(lang, vid)}</p></div>'
        )
    parts.append('</details>')
    return ''.join(parts)


def added_note(lang):
    return LABELS[lang]['added']
