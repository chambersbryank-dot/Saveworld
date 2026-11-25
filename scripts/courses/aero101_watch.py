"""AERO 101 Watch and learn lectures. Bryan approved this pilot on November 25, 2026.

Box and tier labels, and the one-line reasons, are SI translations. No native speaker has reviewed them.
Every video id below was checked with YouTube oEmbed (public, embeddable, owner matches) and the
length was read from the media itself. Do not add an id that has not been checked the same way.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_TR = json.load(open(os.path.join(HERE, '..', '..', 'i18n', 'courses', '_shared.json'), encoding='utf8'))

CC = 'https://creativecommons.org/licenses/by-nc-sa/4.0/'
OCW_TERMS = 'https://ocw.mit.edu/pages/privacy-and-terms-of-use/'
NASA_MEDIA = 'https://www.nasa.gov/nasa-brand-center/images-and-media/'
OCW_16_687 = 'MIT 16.687 Private Pilot Ground School (IAP 2019), MIT OpenCourseWare'
OCW_16_346 = 'MIT 16.346 Astrodynamics (Fall 2008), MIT OpenCourseWare'

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

# why[lang] is one sentence. kind is mit, nasa, or univ.
VIDEOS = {
    1: [{
        'tier': 'start', 'id': 'L_mJxmO7_8A', 'length': '6:01', 'kind': 'nasa',
        'title': 'The Wright Brothers',
        'page': 'https://www.youtube.com/watch?v=L_mJxmO7_8A',
        'source': 'NASA Connect, NASA',
        'why': {
            'en': 'See how the Wright brothers used the engineering method to design and fly the first airplane.',
            'fr': 'Voyez comment les frères Wright ont utilisé la méthode d’ingénierie pour concevoir et faire voler le premier avion.',
            'es': 'Vea cómo los hermanos Wright usaron el método de ingeniería para diseñar y volar el primer avión.',
            'ar': 'شاهد كيف استخدم الأخوان رايت منهج الهندسة لتصميم أول طائرة وتحليقها.',
            'it': 'Guarda come i fratelli Wright hanno usato il metodo ingegneristico per progettare e far volare il primo aeroplano.',
            'he': 'ראו איך האחים רייט השתמשו בשיטת ההנדסה כדי לתכנן ולהטיס את המטוס הראשון.',
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
    }],
    3: [{
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
    }],
    4: [{
        'tier': 'deep', 'id': 'aa2kBZAoXg0', 'length': '31:27', 'kind': 'univ',
        'title': 'Krzysztof Fidkowski | How Planes Fly',
        'page': 'https://www.youtube.com/watch?v=aa2kBZAoXg0',
        'source': 'Krzysztof Fidkowski, Michigan Engineering, University of Michigan',
        'channel': 'Michigan Engineering',
        'why': {
            'en': 'A University of Michigan professor takes apart the usual explanations of how a wing makes lift.',
            'fr': 'Un professeur de l’Université du Michigan reprend les explications courantes de la portance d’une aile.',
            'es': 'Un profesor de la Universidad de Míchigan desmonta las explicaciones habituales de cómo un ala produce sustentación.',
            'ar': 'أستاذ في جامعة ميشيغان يفكك التفسيرات الشائعة لكيفية توليد الجناح للرفع.',
            'it': 'Un professore dell’Università del Michigan smonta le spiegazioni abituali di come un’ala genera portanza.',
            'he': 'פרופסור מאוניברסיטת מישיגן מפרק את ההסברים הרגילים לאיך כנף יוצרת עילוי.',
        },
    }],
    5: [{
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
    }],
    8: [{
        'tier': 'start', 'id': 'VnM9b2QtHYg', 'length': '5:04', 'kind': 'univ',
        'title': 'Why Planes Can’t Reach Space | Rocket Science for Everyone, Yale',
        'page': 'https://www.youtube.com/watch?v=VnM9b2QtHYg',
        'source': 'Marla Geha, Yale University (YaleCourses)',
        'channel': 'YaleCourses',
        'why': {
            'en': 'Why a jet cannot reach orbit, and why a rocket must carry its own oxidizer and so much propellant.',
            'fr': 'Pourquoi un réacteur ne peut pas atteindre l’orbite, et pourquoi une fusée doit emporter son comburant et tant de propergol.',
            'es': 'Por qué un reactor no puede llegar a órbita, y por qué un cohete debe llevar su propio oxidante y tanto propelente.',
            'ar': 'لماذا لا يبلغ المحرك النفاث المدار، ولماذا يجب أن يحمل الصاروخ مؤكسده وكمية كبيرة من الوقود الدافع.',
            'it': 'Perché un motore a getto non può raggiungere l’orbita, e perché un razzo deve portare il proprio ossidante e tanto propellente.',
            'he': 'למה מנוע סילון לא מגיע למסלול, ולמה טיל חייב לשאת את המחמצן שלו וכל כך הרבה דלק.',
        },
    }],
    9: [{
        'tier': 'start', 'id': 'hBE00PL04FM', 'length': '5:51', 'kind': 'univ',
        'title': 'What Is an Orbit | Rocket Science for Everyone, Yale',
        'page': 'https://www.youtube.com/watch?v=hBE00PL04FM',
        'source': 'Marla Geha, Yale University (YaleCourses)',
        'channel': 'YaleCourses',
        'why': {
            'en': 'What an orbit is: falling sideways fast enough to keep missing Earth.',
            'fr': 'Ce qu’est une orbite : tomber de côté assez vite pour continuer à manquer la Terre.',
            'es': 'Qué es una órbita: caer de lado lo bastante rápido como para seguir sin tocar la Tierra.',
            'ar': 'ما المدار: سقوط جانبي بسرعة تكفي لمواصلة إخطاء الأرض.',
            'it': 'Che cos’è un’orbita: cadere di lato abbastanza in fretta da continuare a mancare la Terra.',
            'he': 'מהו מסלול: נפילה הצידה במהירות שמספיקה כדי להמשיך להחטיא את כדור הארץ.',
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
    '.crs-watch>summary h3{margin:0}'
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
    return (f'{length} · {source}. {_esc(_shared(lang, "License:"))} '
            f'<a href="{_esc(vid["page"])}" rel="noopener">{_esc(vid["channel"])}</a> ({_esc(L["univ_lic"])}). '
            + _esc(_shared(lang, 'Linked for free study only; Saving Planets is not affiliated with or endorsed by this university.')))


def _player(lang, vid):
    L = LABELS[lang]
    title = _esc(vid['title'])
    return (f'<div class="crs-watch-frame"><button type="button" class="crs-watch-play" data-id="{vid["id"]}" '
            f'data-title="{title}" aria-label="{_esc(L["play"])}: {title}">'
            f'<span class="crs-watch-poster" aria-hidden="true"><span class="crs-watch-tri"></span></span>'
            f'<span class="crs-watch-cap"><span lang="en">{title}</span></span></button></div>')


def box(lang, unit):
    """One closed details box for unit 1..10. Tiers with no video are omitted."""
    L = LABELS[lang]
    parts = [f'<details class="crs-watch"><summary><h3>{_esc(L["box"])}</h3></summary>']
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
