# -*- coding: utf-8 -*-
"""Undergraduate Studies hook film. The picture is NASA's. We only add a player around it.

English lines are the captions YouTube shows for NASA Glenn Research Center,
"Materials Science—A Building Block for the Future of Aerospace Technologies"
(https://www.youtube.com/watch?v=c0EXAuWkMqA), published September 21, 2023,
length 5:56. Cues after 5:55 belong to a following segment and are not included.
Chapter times are the five chapter markers on that film.
French, Spanish, Arabic, Italian, and Hebrew lines are SI translations of those
English captions, not NASA translations.
"""
import html
import json
import os

from study_aero_text import T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CUES_PATH = os.path.join(ROOT, 'assets', 'courses', 'nasa-materials-cues.json')
FILM_ID = 'c0EXAuWkMqA'
TITLE = 'Materials Science—A Building Block for the Future of Aerospace Technologies'
WATCH = 'https://www.youtube.com/watch?v=' + FILM_ID
POSTER = 'assets/courses/nasa-materials-poster.jpg'
CUES_URL = 'assets/courses/nasa-materials-cues.json'
META_URL = 'assets/courses/nasa-film-meta.json'
PLYR_JS = 'assets/vendor/plyr/plyr.min.js'
PLYR_CSS = 'assets/vendor/plyr/plyr.css'
JS = 'assets/courses/nasa-film.js?v=20261127a'
LOGO = 'assets/brand/sp-logo-72.webp?v=20261020'
NASA_MEDIA = 'https://www.nasa.gov/nasa-brand-center/images-and-media/'
APA = ('NASA Glenn Research Center. (2023, September 21). '
       'Materials Science—A Building Block for the Future of Aerospace Technologies [Video]. '
       'YouTube. https://www.youtube.com/watch?v=c0EXAuWkMqA')
MLA = ('"Materials Science—A Building Block for the Future of Aerospace Technologies." '
       'YouTube, uploaded by NASA Glenn Research Center, 21 Sept. 2023, '
       'https://www.youtube.com/watch?v=c0EXAuWkMqA.')

# (seconds, titles). English titles are the ones on the YouTube film.
CHAPTERS = (
    (0, {
        'en': 'Defining Material Science',
        'fr': 'Définir la science des matériaux',
        'es': 'Definir la ciencia de los materiales',
        'ar': 'تعريف علم المواد',
        'it': 'Definire la scienza dei materiali',
        'he': 'להגדיר את מדע החומרים',
    }),
    (60.519, {
        'en': "NASA's Material Advancements",
        'fr': 'Les avancées de la NASA sur les matériaux',
        'es': 'Avances de la NASA en materiales',
        'ar': 'تقدم ناسا في المواد',
        'it': 'I progressi della NASA sui materiali',
        'he': 'ההתקדמות של נאס״א בחומרים',
    }),
    (103.399, {
        'en': 'Personal Journey to NASA',
        'fr': 'Parcours personnel vers la NASA',
        'es': 'Trayectoria personal hacia la NASA',
        'ar': 'رحلة شخصية إلى ناسا',
        'it': 'Percorso personale verso la NASA',
        'he': 'מסע אישי אל נאס״א',
    }),
    (170.720, {
        'en': 'Innovations in Aerospace',
        'fr': 'Innovations en aérospatial',
        'es': 'Innovaciones aeroespaciales',
        'ar': 'ابتكارات في الطيران والفضاء',
        'it': 'Innovazioni aerospaziali',
        'he': 'חדשנות באווירונאוטיקה ובחלל',
    }),
    (280.759, {
        'en': 'Future Exploration Challenges',
        'fr': 'Les défis de l’exploration à venir',
        'es': 'Desafíos de la exploración futura',
        'ar': 'تحديات الاستكشاف المقبل',
        'it': 'Sfide dell’esplorazione futura',
        'he': 'אתגרי החקר הבאים',
    }),
)

UI = {
    'en': {
        'badge': 'Featured film',
        'unmute': 'Unmute',
        'transcript': 'Transcript',
        'dl': 'Download transcript',
        'txt': 'Text file',
        'pdf': 'PDF',
        'cite': 'Cite this video',
        'copy': 'Copy',
        'copied': 'Copied',
        'chapters': 'Chapters',
        'captions': 'Captions',
        'speed': 'Speed',
        'cite_lead': 'Cite the English film.',
        'note_en': 'These lines are the captions YouTube shows for this NASA Glenn Research Center film, through 5:55.',
        'note_tr': 'SI translation of those English captions. Not a NASA translation.',
        'ch_note': 'The times are the chapter markers on the YouTube film. Titles in French, Spanish, Arabic, Italian, and Hebrew are SI translations of those English titles.',
        'endorse': 'NASA produced this film. NASA does not endorse this page.',
        'cc': {
            'en': 'English (NASA Glenn captions)',
            'fr': 'French (SI translation)',
            'es': 'Spanish (SI translation)',
            'ar': 'Arabic (SI translation)',
            'it': 'Italian (SI translation)',
            'he': 'Hebrew (SI translation)',
        },
        'plyr': {
            'play': 'Play', 'pause': 'Pause', 'mute': 'Mute', 'unmute': 'Unmute',
            'enterFullscreen': 'Enter fullscreen', 'exitFullscreen': 'Exit fullscreen',
            'settings': 'Settings', 'speed': 'Speed', 'normal': 'Normal',
            'captions': 'Captions', 'disabled': 'Disabled', 'enabled': 'Enabled',
        },
    },
    'fr': {
        'badge': 'Film à la une',
        'unmute': 'Activer le son',
        'transcript': 'Transcription',
        'dl': 'Télécharger la transcription',
        'txt': 'Fichier texte',
        'pdf': 'PDF',
        'cite': 'Citer cette vidéo',
        'copy': 'Copier',
        'copied': 'Copié',
        'chapters': 'Chapitres',
        'captions': 'Sous-titres',
        'speed': 'Vitesse',
        'cite_lead': 'Citation du film en anglais.',
        'note_en': 'Ces répliques sont les sous-titres que YouTube affiche pour ce film du NASA Glenn Research Center, jusqu’à 5:55.',
        'note_tr': 'Traduction SI de ces sous-titres anglais. Ce n’est pas une traduction de la NASA.',
        'ch_note': 'Les temps sont les marqueurs de chapitres du film sur YouTube. Les titres autres que l’anglais sont une traduction SI.',
        'endorse': 'La NASA a produit ce film. La NASA ne cautionne pas cette page.',
        'cc': {
            'en': 'Anglais (sous-titres NASA Glenn)',
            'fr': 'Français (traduction SI)',
            'es': 'Espagnol (traduction SI)',
            'ar': 'Arabe (traduction SI)',
            'it': 'Italien (traduction SI)',
            'he': 'Hébreu (traduction SI)',
        },
        'plyr': {
            'play': 'Lire', 'pause': 'Pause', 'mute': 'Couper le son', 'unmute': 'Activer le son',
            'enterFullscreen': 'Plein écran', 'exitFullscreen': 'Quitter le plein écran',
            'settings': 'Réglages', 'speed': 'Vitesse', 'normal': 'Normale',
            'captions': 'Sous-titres', 'disabled': 'Désactivés', 'enabled': 'Activés',
        },
    },
    'es': {
        'badge': 'Película destacada',
        'unmute': 'Activar el sonido',
        'transcript': 'Transcripción',
        'dl': 'Descargar la transcripción',
        'txt': 'Archivo de texto',
        'pdf': 'PDF',
        'cite': 'Citar este video',
        'copy': 'Copiar',
        'copied': 'Copiado',
        'chapters': 'Capítulos',
        'captions': 'Subtítulos',
        'speed': 'Velocidad',
        'cite_lead': 'Cita de la película en inglés.',
        'note_en': 'Estas líneas son los subtítulos que YouTube muestra para esta película del NASA Glenn Research Center, hasta 5:55.',
        'note_tr': 'Traducción de SI de esos subtítulos en inglés. No es una traducción de la NASA.',
        'ch_note': 'Los tiempos son los marcadores de capítulo de la película en YouTube. Los títulos que no están en inglés son una traducción de SI.',
        'endorse': 'La NASA produjo esta película. La NASA no respalda esta página.',
        'cc': {
            'en': 'Inglés (subtítulos de NASA Glenn)',
            'fr': 'Francés (traducción de SI)',
            'es': 'Español (traducción de SI)',
            'ar': 'Árabe (traducción de SI)',
            'it': 'Italiano (traducción de SI)',
            'he': 'Hebreo (traducción de SI)',
        },
        'plyr': {
            'play': 'Reproducir', 'pause': 'Pausa', 'mute': 'Silenciar', 'unmute': 'Activar el sonido',
            'enterFullscreen': 'Pantalla completa', 'exitFullscreen': 'Salir de pantalla completa',
            'settings': 'Ajustes', 'speed': 'Velocidad', 'normal': 'Normal',
            'captions': 'Subtítulos', 'disabled': 'Desactivados', 'enabled': 'Activados',
        },
    },
    'ar': {
        'badge': 'فيلم مميز',
        'unmute': 'تشغيل الصوت',
        'transcript': 'النص',
        'dl': 'تنزيل النص',
        'txt': 'ملف نصي',
        'pdf': 'PDF',
        'cite': 'استشهد بهذا الفيديو',
        'copy': 'نسخ',
        'copied': 'تم النسخ',
        'chapters': 'الفصول',
        'captions': 'الترجمة',
        'speed': 'السرعة',
        'cite_lead': 'استشهاد الفيلم الإنجليزي.',
        'note_en': 'هذه الأسطر هي الترجمة التي يعرضها يوتيوب لهذا الفيلم من مركز غلين للأبحاث في ناسا، حتى 5:55.',
        'note_tr': 'ترجمة SI لتلك الترجمة الإنجليزية. ليست ترجمة من ناسا.',
        'ch_note': 'الأوقات هي علامات الفصول على فيلم يوتيوب. العناوين بغير الإنجليزية ترجمة من SI.',
        'endorse': 'أنتجت ناسا هذا الفيلم. ولا تصادق ناسا على هذه الصفحة.',
        'cc': {
            'en': 'الإنجليزية (ترجمة ناسا غلين)',
            'fr': 'الفرنسية (ترجمة SI)',
            'es': 'الإسبانية (ترجمة SI)',
            'ar': 'العربية (ترجمة SI)',
            'it': 'الإيطالية (ترجمة SI)',
            'he': 'العبرية (ترجمة SI)',
        },
        'plyr': {
            'play': 'تشغيل', 'pause': 'إيقاف مؤقت', 'mute': 'كتم', 'unmute': 'تشغيل الصوت',
            'enterFullscreen': 'ملء الشاشة', 'exitFullscreen': 'الخروج من ملء الشاشة',
            'settings': 'الإعدادات', 'speed': 'السرعة', 'normal': 'عادي',
            'captions': 'الترجمة', 'disabled': 'متوقفة', 'enabled': 'مفعّلة',
        },
    },
    'it': {
        'badge': 'Film in evidenza',
        'unmute': 'Attiva l’audio',
        'transcript': 'Trascrizione',
        'dl': 'Scarica la trascrizione',
        'txt': 'File di testo',
        'pdf': 'PDF',
        'cite': 'Cita questo video',
        'copy': 'Copia',
        'copied': 'Copiato',
        'chapters': 'Capitoli',
        'captions': 'Sottotitoli',
        'speed': 'Velocità',
        'cite_lead': 'Citazione del film in inglese.',
        'note_en': 'Queste battute sono i sottotitoli che YouTube mostra per questo film del NASA Glenn Research Center, fino a 5:55.',
        'note_tr': 'Traduzione SI di quei sottotitoli inglesi. Non è una traduzione della NASA.',
        'ch_note': 'I tempi sono i marcatori dei capitoli sul film di YouTube. I titoli diversi dall’inglese sono una traduzione SI.',
        'endorse': 'La NASA ha prodotto questo film. La NASA non avalla questa pagina.',
        'cc': {
            'en': 'Inglese (sottotitoli NASA Glenn)',
            'fr': 'Francese (traduzione SI)',
            'es': 'Spagnolo (traduzione SI)',
            'ar': 'Arabo (traduzione SI)',
            'it': 'Italiano (traduzione SI)',
            'he': 'Ebraico (traduzione SI)',
        },
        'plyr': {
            'play': 'Riproduci', 'pause': 'Pausa', 'mute': 'Disattiva l’audio', 'unmute': 'Attiva l’audio',
            'enterFullscreen': 'Schermo intero', 'exitFullscreen': 'Esci da schermo intero',
            'settings': 'Impostazioni', 'speed': 'Velocità', 'normal': 'Normale',
            'captions': 'Sottotitoli', 'disabled': 'Disattivati', 'enabled': 'Attivati',
        },
    },
    'he': {
        'badge': 'סרט נבחר',
        'unmute': 'ביטול השתקה',
        'transcript': 'תמליל',
        'dl': 'הורדת התמליל',
        'txt': 'קובץ טקסט',
        'pdf': 'PDF',
        'cite': 'ציטוט הסרט',
        'copy': 'העתקה',
        'copied': 'הועתק',
        'chapters': 'פרקים',
        'captions': 'כתוביות',
        'speed': 'מהירות',
        'cite_lead': 'ציטוט הסרט באנגלית.',
        'note_en': 'השורות האלה הן הכתוביות שיוטיוב מציג לסרט הזה של מרכז המחקר גלן של נאס״א, עד 5:55.',
        'note_tr': 'תרגום SI של הכתוביות האנגליות האלה. זה אינו תרגום של נאס״א.',
        'ch_note': 'הזמנים הם סימוני הפרקים בסרט ביוטיוב. כותרות שאינן באנגלית הן תרגום SI.',
        'endorse': 'נאס״א הפיקה את הסרט הזה. נאס״א אינה מעניקה חסות לעמוד הזה.',
        'cc': {
            'en': 'אנגלית (כתוביות נאס״א גלן)',
            'fr': 'צרפתית (תרגום SI)',
            'es': 'ספרדית (תרגום SI)',
            'ar': 'ערבית (תרגום SI)',
            'it': 'איטלקית (תרגום SI)',
            'he': 'עברית (תרגום SI)',
        },
        'plyr': {
            'play': 'הפעלה', 'pause': 'השהיה', 'mute': 'השתקה', 'unmute': 'ביטול השתקה',
            'enterFullscreen': 'מסך מלא', 'exitFullscreen': 'יציאה ממסך מלא',
            'settings': 'הגדרות', 'speed': 'מהירות', 'normal': 'רגיל',
            'captions': 'כתוביות', 'disabled': 'כבוי', 'enabled': 'פעיל',
        },
    },
}

LANGS = ('en', 'fr', 'es', 'ar', 'it', 'he')
SPEEDS = ('0.5', '0.75', '1', '1.25', '1.5', '1.75', '2')


def cues():
    data = json.loads(open(CUES_PATH, encoding='utf-8').read())
    if len(data) != 50:
        raise SystemExit(f'expected 50 cues, got {len(data)}')
    if any(c['t'] > 355 for c in data):
        raise SystemExit('cue past the 5:56 film')
    return data


def prefix(lang):
    return '' if lang == 'en' else '../'


def clock(sec):
    sec = int(float(sec))
    return f'{sec // 60}:{sec % 60:02d}'


def E(text):
    return html.escape(text, quote=True)


def script_src(lang):
    return prefix(lang) + JS


def transcript_href(lang, kind):
    return prefix(lang) + f'assets/courses/transcripts/nasa-materials-{lang}.{kind}'


def figure(lang):
    S = T[lang]
    U = UI[lang]
    pre = prefix(lang)
    lines = cues()
    ol = ''.join(
        f'<li><button type="button" data-t="{c["t"]}">'
        f'<bdi class="crs-film-timeb" dir="ltr">{clock(c["t"])}</bdi> '
        f'<span class="crs-film-line">{E(c[lang])}</span></button></li>'
        for c in lines
    )
    chapters = ''.join(
        f'<li><button type="button" data-t="{t}">'
        f'<bdi class="crs-film-timeb" dir="ltr">{clock(t)}</bdi> '
        f'<span>{E(names[lang])}</span></button></li>'
        for t, names in CHAPTERS
    )
    cc = ''.join(
        f'<option value="{code}"' + (' selected' if code == lang else '') + f'>{E(U["cc"][code])}</option>'
        for code in LANGS
    )
    speeds = ''.join(
        f'<option value="{v}"' + (' selected' if v == '1' else '') + f'>{v}×</option>'
        for v in SPEEDS
    )
    cred_before, cred_after = S['film_credit'].split('{name}')
    title = E(TITLE)
    i18n = E(json.dumps(U['plyr'], ensure_ascii=False, separators=(',', ':')))
    note = U['note_en'] if lang == 'en' else U['note_tr']
    return (
        f'<figure class="crs-film" data-id="{FILM_ID}" data-lang="{lang}" '
        f'data-cues="{pre}{CUES_URL}" data-meta="{pre}{META_URL}" '
        f'data-plyr="{pre}{PLYR_JS}" data-plyr-css="{pre}{PLYR_CSS}" '
        f'data-i18n="{i18n}">'
        f'<div class="crs-film-bar">'
        f'<span class="crs-film-badge">{E(U["badge"])}</span>'
        f'<span class="crs-film-badge">{E(S["film_credit"].format(name=S["film_name"]))}</span>'
        f'<span class="crs-film-time"><bdi dir="ltr">5:56</bdi></span>'
        f'<span class="crs-film-brand"><img src="{pre}{LOGO}" alt="" width="28" height="28">'
        f'<bdi dir="ltr">Saving Planets</bdi></span></div>'
        f'<div class="crs-film-stage"><div class="crs-film-frame">'
        f'<a class="crs-film-poster" href="{WATCH}">'
        f'<img src="{pre}{POSTER}" alt="" width="1280" height="720" decoding="async">'
        f'<span class="crs-film-play" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28">'
        f'<path fill="#fff" d="M8 5v14l11-7z"/></svg></span>'
        f'<span class="crs-film-poster-label">{E(S["play"])}: <bdi lang="en" dir="ltr">{title}</bdi></span>'
        f'</a></div>'
        f'<button type="button" class="crs-film-unmute" hidden>{E(U["unmute"])}</button></div>'
        f'<p class="crs-film-cc" aria-live="polite"></p>'
        f'<figcaption>'
        f'<span class="crs-film-title"><bdi lang="en" dir="ltr">{title}</bdi></span>'
        f'<span class="crs-film-meta"><bdi lang="en" dir="ltr">NASA Glenn Research Center</bdi> · '
        f'<bdi dir="ltr">5:56</bdi> · {E(S["film_caps"])}</span>'
        f'<span class="crs-film-credit">{E(cred_before)}'
        f'<a href="{NASA_MEDIA}" rel="noopener license">{E(S["film_name"])}</a>{E(cred_after)}</span>'
        f'<span class="crs-film-endorse">{E(U["endorse"])}</span>'
        f'</figcaption>'
        f'<div class="crs-film-tools">'
        f'<label>{E(U["speed"])} <select class="crs-film-speed" dir="ltr">{speeds}</select></label>'
        f'<label>{E(U["captions"])} <select class="crs-film-cc-lang">{cc}</select></label>'
        f'<details class="crs-film-chapters"><summary>{E(U["chapters"])}</summary>'
        f'<p class="crs-film-note">{E(U["ch_note"])}</p>'
        f'<ol>{chapters}</ol></details>'
        f'<details class="crs-film-cite"><summary>{E(U["cite"])}</summary>'
        f'<p class="crs-film-note">{E(U["cite_lead"])}</p>'
        f'<p class="crs-film-cite-k">APA</p>'
        f'<p class="crs-film-cite-t" id="nasa-cite-apa" lang="en" dir="ltr">{E(APA)}</p>'
        f'<button type="button" data-copy="nasa-cite-apa" data-copied="{E(U["copied"])}">{E(U["copy"])}</button>'
        f'<p class="crs-film-cite-k">MLA</p>'
        f'<p class="crs-film-cite-t" id="nasa-cite-mla" lang="en" dir="ltr">{E(MLA)}</p>'
        f'<button type="button" data-copy="nasa-cite-mla" data-copied="{E(U["copied"])}">{E(U["copy"])}</button>'
        f'</details></div>'
        f'<details class="crs-film-script" open><summary>{E(U["transcript"])}</summary>'
        f'<p class="crs-film-note" data-note-en="{E(U["note_en"])}" data-note-tr="{E(U["note_tr"])}">{E(note)}</p>'
        f'<p class="crs-film-dl">{E(U["dl"])} '
        f'<a href="{transcript_href(lang, "txt")}" download>{E(U["txt"])}</a> '
        f'<a href="{transcript_href(lang, "pdf")}" download>{E(U["pdf"])}</a></p>'
        f'<ol class="crs-film-lines" lang="{lang}">{ol}</ol></details>'
        f'</figure>'
    )


def plain(lang):
    U = UI[lang]
    note = U['note_en'] if lang == 'en' else U['note_tr']
    rows = [f'{clock(c["t"])}  {c[lang]}' for c in cues()]
    return (
        f'{TITLE}\n'
        'NASA Glenn Research Center. September 21, 2023. 5:56.\n'
        f'{WATCH}\n\n'
        f'{note}\n\n'
        + '\n'.join(rows) + '\n'
    )


CSS = r"""
.crs-hook{display:block}
.crs-film{margin:.7rem 0 0}
.crs-film-bar{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .55rem;margin:0 0 .5rem}
.crs-film-badge,.crs-film-time{display:inline-flex;align-items:center;min-height:32px;padding:0 .7rem;border-radius:999px;font-size:.78rem;font-weight:800;color:#f7fbff;background:rgba(0,156,222,.22);border:1px solid rgba(0,156,222,.75)}
.crs-film-unmute{min-height:44px;padding:0 .9rem;border-radius:999px;border:1px solid #ffd54a;background:#10283f;color:#fff;font:inherit;font-weight:800;cursor:pointer}
.crs-film-unmute[hidden]{display:none}
.crs-film-brand{margin-inline-start:auto;display:inline-flex;align-items:center;gap:.4rem;font-weight:800}
.crs-film-brand img{width:28px;height:28px;border-radius:6px}
.crs-film-stage{position:relative;border-radius:18px;padding:.55rem;background:radial-gradient(120% 90% at 50% 0%,rgba(0,156,222,.42),rgba(0,156,222,.08) 46%,transparent 72%);box-shadow:0 0 0 1px rgba(0,156,222,.55),0 18px 40px rgba(0,40,70,.35)}
.crs-film-unmute{position:absolute;z-index:6;inset-inline-end:.7rem;inset-block-start:.7rem}
.crs-film-frame{position:relative;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#071422;direction:ltr}
.crs-film-poster{position:absolute;inset:0;display:block;color:inherit;text-decoration:none}
.crs-film-poster img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.crs-film-play{position:absolute;inset-inline-start:50%;top:50%;display:flex;align-items:center;justify-content:center;width:4.25rem;height:4.25rem;margin:-2.125rem 0 0 -2.125rem;border-radius:50%;background:rgba(8,20,36,.55);border:1px solid rgba(255,255,255,.7);box-shadow:0 8px 24px rgba(0,0,0,.35)}
.crs-film-poster-label{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.crs-film-poster:focus-visible,.crs-film-unmute:focus-visible,.crs-film-tools button:focus-visible,.crs-film-tools summary:focus-visible,.crs-film-lines button:focus-visible,.crs-film-chapters button:focus-visible,.crs-film-tools select:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}
.crs-film-frame .plyr,.crs-film-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.crs-film-cc{min-height:2.6rem;margin:.4rem 0 0;text-align:center}
.crs-film-cc:empty{visibility:hidden}
.crs-film figcaption{display:flex;flex-direction:column;gap:.15rem;margin-top:.45rem;font-size:.9rem;line-height:1.4}
.crs-film-title{font-weight:800}
.crs-film-endorse{font-weight:650}
.crs-film-tools{display:flex;flex-wrap:wrap;gap:.55rem .8rem;align-items:flex-end;margin:.55rem 0 0}
.crs-film-tools label{display:flex;flex-direction:column;gap:.15rem;font-size:.85rem;font-weight:750}
.crs-film-tools select,.crs-film-tools a,.crs-film-tools button,.crs-film-tools summary{min-height:44px;font:inherit}
.crs-film-tools select{padding:0 .4rem;border-radius:10px;color:#10283f;background:#f7fbff}
.crs-film-tools details{flex:1 1 16rem;min-width:0;max-width:100%}
@media (max-width:640px){.crs-film-tools label{flex:1 1 100%;min-width:0;max-width:100%}.crs-film-tools select{width:100%;max-width:100%}.crs-film-line{overflow-wrap:anywhere}.crs-film-bar{max-width:100%}}
.crs-film-tools summary,.crs-film-script>summary{cursor:pointer;display:flex;align-items:center;font-weight:800}
.crs-film-note{margin:.35rem 0;font-size:.88rem;line-height:1.4}
.crs-film-cite-k{margin:.45rem 0 .1rem;font-weight:800}
.crs-film-cite-t{margin:.1rem 0 .25rem;font-size:.88rem;line-height:1.4}
.crs-film-dl{margin:.2rem 0 .4rem}
.crs-film-dl a{min-height:44px;display:inline-flex;align-items:center;margin-inline-end:.8rem}
.crs-film-lines,.crs-film-chapters ol{list-style:none;margin:.3rem 0 0;padding:0}
.crs-film-lines{max-height:16rem;overflow:auto;border:1px solid rgba(255,255,255,.2);border-radius:12px}
.crs-film-lines button,.crs-film-chapters button{display:flex;gap:.65rem;align-items:flex-start;width:100%;text-align:start;color:inherit;background:transparent;border:0;border-radius:8px;padding:.4rem .55rem;min-height:44px;font:inherit;cursor:pointer}
.crs-film-line{flex:1;min-width:0}
.crs-film-timeb{flex:none;font-variant-numeric:tabular-nums}
.crs-film-lines button[aria-current="true"]{background:rgba(0,156,222,.32);font-weight:750}
@media (hover:hover) and (prefers-reduced-motion:no-preference){.crs-film-stage{transition:transform .2s ease}.crs-film:hover .crs-film-stage{transform:translateY(-2px)}}
@media (prefers-reduced-motion:reduce){.crs-film-stage{transform:none!important;transition:none!important}}
@media print{.crs-film-stage,.crs-film-unmute,.crs-film-tools{display:none!important}.crs-film-lines{max-height:none;overflow:visible}}
"""
