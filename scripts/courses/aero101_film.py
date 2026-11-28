# -*- coding: utf-8 -*-
"""Unit 1 featured film for Intro to Aerospace Engineering.

The Wright Brothers, NASA Connect (NASAconnect on YouTube), published August 18, 2007,
length 6:01. https://www.youtube.com/watch?v=L_mJxmO7_8A
oEmbed: title "The Wright Brothers", author NASAconnect.
License: NASA media guidelines. NASA content is generally not subject to copyright
in the United States (U.S. government work). The same NASA Connect segment is
catalogued Public Domain by the NASA Langley Office of Education on archive.org
(NasaConnect-Twm-TheWrightBrothers). NASA produced the film and does not endorse this page.

English lines follow YouTube's transcript through 5:53. Names the automatic
transcript misspelled (Pulley, Orville, Wilbur, Graham Bell, Hiram Maxim) are restored.
French, Spanish, Arabic, Italian, and Hebrew lines are SI translations of that English.
Chapter times are the chapter headings on the YouTube transcript.
"""
import html
import json
import os

from study_aero_text import T
from courses import nasa_film as NF

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CUES_PATH = os.path.join(ROOT, 'assets', 'courses', 'wright-brothers-cues.json')
FILM_ID = 'L_mJxmO7_8A'
TITLE = 'The Wright Brothers'
WATCH = 'https://www.youtube.com/watch?v=' + FILM_ID
POSTER = 'assets/courses/wright-brothers-poster.jpg'
CUES_URL = 'assets/courses/wright-brothers-cues.json'
META_URL = 'assets/courses/wright-brothers-meta.json'
LENGTH = '6:01'
CHANNEL = 'NASA Connect'
APA = ('NASA Connect. (2007, August 18). The Wright Brothers [Video]. '
       'YouTube. https://www.youtube.com/watch?v=L_mJxmO7_8A')
MLA = ('"The Wright Brothers." YouTube, uploaded by NASAconnect, 18 Aug. 2007, '
       'https://www.youtube.com/watch?v=L_mJxmO7_8A.')

CHAPTERS = (
    (2, {
        'en': 'Introduction to the Wrights',
        'fr': 'Présentation des frères Wright',
        'es': 'Presentación de los hermanos Wright',
        'ar': 'تقديم الأخوين رايت',
        'it': 'Introduzione ai fratelli Wright',
        'he': 'היכרות עם האחים רייט',
    }),
    (34, {
        'en': 'Overcoming obstacles',
        'fr': 'Surmonter les obstacles',
        'es': 'Superar los obstáculos',
        'ar': 'تجاوز العقبات',
        'it': 'Superare gli ostacoli',
        'he': 'להתגבר על המכשולים',
    }),
    (75, {
        'en': 'The engineering method',
        'fr': 'La méthode d’ingénierie',
        'es': 'El método de ingeniería',
        'ar': 'منهج الهندسة',
        'it': 'Il metodo ingegneristico',
        'he': 'שיטת ההנדסה',
    }),
    (126, {
        'en': 'Defining the problem',
        'fr': 'Définir le problème',
        'es': 'Definir el problema',
        'ar': 'تحديد المشكلة',
        'it': 'Definire il problema',
        'he': 'להגדיר את הבעיה',
    }),
    (166, {
        'en': 'Learning from bicycles',
        'fr': 'Apprendre de la bicyclette',
        'es': 'Aprender de la bicicleta',
        'ar': 'التعلّم من الدراجة',
        'it': 'Imparare dalla bicicletta',
        'he': 'ללמוד מהאופניים',
    }),
    (229, {
        'en': 'Proposing a solution',
        'fr': 'Proposer une solution',
        'es': 'Proponer una solución',
        'ar': 'اقتراح حل',
        'it': 'Proporre una soluzione',
        'he': 'להציע פתרון',
    }),
    (309, {
        'en': 'Testing prototypes',
        'fr': 'Essayer des prototypes',
        'es': 'Probar prototipos',
        'ar': 'اختبار النماذج',
        'it': 'Provare i prototipi',
        'he': 'לבחון אבות־טיפוס',
    }),
)

NOTES = {
    'en': {
        'note_en': 'These lines follow YouTube’s transcript of this NASA Connect film, through 5:53. Names the automatic transcript misspelled are restored.',
        'note_tr': 'SI translation of that English transcript. Not a NASA translation.',
        'ch_note': 'The times are the chapter headings on the YouTube transcript. Titles in French, Spanish, Arabic, Italian, and Hebrew are SI translations of those English titles.',
        'cc_en': 'English (YouTube transcript)',
    },
    'fr': {
        'note_en': 'Ces lignes suivent la transcription YouTube de ce film NASA Connect, jusqu’à 5:53. Les noms mal lus par la transcription automatique sont rétablis.',
        'note_tr': 'Traduction SI de cette transcription anglaise. Ce n’est pas une traduction de la NASA.',
        'ch_note': 'Les temps sont les chapitres de la transcription YouTube. Les titres non anglais sont une traduction SI.',
        'cc_en': 'Anglais (transcription YouTube)',
    },
    'es': {
        'note_en': 'Estas líneas siguen la transcripción de YouTube de esta película de NASA Connect, hasta 5:53. Los nombres que la transcripción automática escribió mal están corregidos.',
        'note_tr': 'Traducción SI de esa transcripción inglesa. No es una traducción de la NASA.',
        'ch_note': 'Los tiempos son los capítulos de la transcripción de YouTube. Los títulos que no están en inglés son una traducción SI.',
        'cc_en': 'Inglés (transcripción de YouTube)',
    },
    'ar': {
        'note_en': 'هذه السطور تتبع تفريغ يوتيوب لهذا الفيلم من NASA Connect، حتى 5:53. أُعيدت الأسماء التي أخطأها التفريغ الآلي.',
        'note_tr': 'ترجمة SI لذلك التفريغ الإنجليزي. ليست ترجمة من ناسا.',
        'ch_note': 'الأوقات هي عناوين الفصول في تفريغ يوتيوب. العناوين غير الإنجليزية ترجمة SI.',
        'cc_en': 'الإنجليزية (تفريغ يوتيوب)',
    },
    'it': {
        'note_en': 'Queste righe seguono la trascrizione YouTube di questo film NASA Connect, fino a 5:53. I nomi che la trascrizione automatica ha storpiato sono ripristinati.',
        'note_tr': 'Traduzione SI di quella trascrizione inglese. Non è una traduzione della NASA.',
        'ch_note': 'I tempi sono i capitoli della trascrizione YouTube. I titoli non inglesi sono una traduzione SI.',
        'cc_en': 'Inglese (trascrizione YouTube)',
    },
    'he': {
        'note_en': 'השורות האלה עוקבות אחרי התמליל של יוטיוב לסרט הזה של NASA Connect, עד 5:53. שמות שהתמליל האוטומטי שיבש הוחזרו.',
        'note_tr': 'תרגום SI של התמליל האנגלי הזה. זה אינו תרגום של נאס״א.',
        'ch_note': 'הזמנים הם כותרות הפרקים בתמליל יוטיוב. כותרות שאינן באנגלית הן תרגום SI.',
        'cc_en': 'אנגלית (תמליל יוטיוב)',
    },
}


def cues():
    data = json.loads(open(CUES_PATH, encoding='utf-8').read())
    if len(data) != 45:
        raise SystemExit(f'expected 45 cues, got {len(data)}')
    if any(c['t'] > 361 for c in data):
        raise SystemExit('cue past the 6:01 film')
    return data


def transcript_href(lang, kind):
    return NF.prefix(lang) + f'assets/courses/transcripts/wright-brothers-{lang}.{kind}'


def figure(lang):
    S = T[lang]
    U = NF.UI[lang]
    N = NOTES[lang]
    pre = NF.prefix(lang)
    lines = cues()
    ol = ''.join(
        f'<li><button type="button" data-t="{c["t"]}">'
        f'<bdi class="crs-film-timeb" dir="ltr">{NF.clock(c["t"])}</bdi> '
        f'<span class="crs-film-line">{NF.E(c[lang])}</span></button></li>'
        for c in lines
    )
    chapters = ''.join(
        f'<li><button type="button" data-t="{t}">'
        f'<bdi class="crs-film-timeb" dir="ltr">{NF.clock(t)}</bdi> '
        f'<span>{NF.E(names[lang])}</span></button></li>'
        for t, names in CHAPTERS
    )
    cc_labels = dict(U['cc'])
    cc_labels['en'] = N['cc_en']
    cc = ''.join(
        f'<option value="{code}"' + (' selected' if code == lang else '') + f'>{NF.E(cc_labels[code])}</option>'
        for code in NF.LANGS
    )
    speeds = ''.join(
        f'<option value="{v}"' + (' selected' if v == '1' else '') + f'>{v}×</option>'
        for v in NF.SPEEDS
    )
    cred_before, cred_after = S['film_credit'].split('{name}')
    title = NF.E(TITLE)
    i18n = NF.E(json.dumps(U['plyr'], ensure_ascii=False, separators=(',', ':')))
    note = N['note_en'] if lang == 'en' else N['note_tr']
    return (
        f'<figure class="crs-film" id="u1-watch" data-autoplay="1" data-id="{FILM_ID}" data-lang="{lang}" '
        f'data-cues="{pre}{CUES_URL}" data-meta="{pre}{META_URL}" '
        f'data-plyr="{pre}{NF.PLYR_JS}" data-plyr-css="{pre}{NF.PLYR_CSS}" '
        f'data-i18n="{i18n}">'
        f'<div class="crs-film-bar">'
        f'<span class="crs-film-badge">{NF.E(U["badge"])}</span>'
        f'<span class="crs-film-badge">{NF.E(S["film_credit"].format(name=S["film_name"]))}</span>'
        f'<span class="crs-film-time"><bdi dir="ltr">{LENGTH}</bdi></span>'
        f'<span class="crs-film-brand"><img src="{pre}{NF.LOGO}" alt="" width="28" height="28">'
        f'<bdi dir="ltr">Saving Planets</bdi></span></div>'
        f'<div class="crs-film-stage"><div class="crs-film-frame">'
        f'<a class="crs-film-poster" href="{WATCH}">'
        f'<img src="{pre}{POSTER}" alt="" width="480" height="360" decoding="async">'
        f'<span class="crs-film-play" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28">'
        f'<path fill="#fff" d="M8 5v14l11-7z"/></svg></span>'
        f'<span class="crs-film-poster-label">{NF.E(S["play"])}: <bdi lang="en" dir="ltr">{title}</bdi></span>'
        f'</a></div>'
        f'<button type="button" class="crs-film-unmute" hidden>{NF.E(U["unmute"])}</button></div>'
        f'<p class="crs-film-cc" aria-live="polite"></p>'
        f'<figcaption>'
        f'<span class="crs-film-title"><bdi lang="en" dir="ltr">{title}</bdi></span>'
        f'<span class="crs-film-meta"><bdi lang="en" dir="ltr">{NF.E(CHANNEL)}</bdi> · '
        f'<bdi dir="ltr">{LENGTH}</bdi> · {NF.E(S["film_caps"])}</span>'
        f'<span class="crs-film-credit">{NF.E(cred_before)}'
        f'<a href="{NF.NASA_MEDIA}" rel="noopener license">{NF.E(S["film_name"])}</a>{NF.E(cred_after)}</span>'
        f'<span class="crs-film-endorse">{NF.E(U["endorse"])}</span>'
        f'</figcaption>'
        f'<div class="crs-film-tools">'
        f'<label>{NF.E(U["speed"])} <select class="crs-film-speed" dir="ltr">{speeds}</select></label>'
        f'<label>{NF.E(U["captions"])} <select class="crs-film-cc-lang">{cc}</select></label>'
        f'<details class="crs-film-chapters"><summary>{NF.E(U["chapters"])}</summary>'
        f'<p class="crs-film-note">{NF.E(N["ch_note"])}</p>'
        f'<ol>{chapters}</ol></details>'
        f'<details class="crs-film-cite"><summary>{NF.E(U["cite"])}</summary>'
        f'<p class="crs-film-note">{NF.E(U["cite_lead"])}</p>'
        f'<p class="crs-film-cite-k">APA</p>'
        f'<p class="crs-film-cite-t" id="wright-cite-apa" lang="en" dir="ltr">{NF.E(APA)}</p>'
        f'<button type="button" data-copy="wright-cite-apa" data-copied="{NF.E(U["copied"])}">{NF.E(U["copy"])}</button>'
        f'<p class="crs-film-cite-k">MLA</p>'
        f'<p class="crs-film-cite-t" id="wright-cite-mla" lang="en" dir="ltr">{NF.E(MLA)}</p>'
        f'<button type="button" data-copy="wright-cite-mla" data-copied="{NF.E(U["copied"])}">{NF.E(U["copy"])}</button>'
        f'</details></div>'
        f'<details class="crs-film-script" open><summary>{NF.E(U["transcript"])}</summary>'
        f'<p class="crs-film-note" data-note-en="{NF.E(N["note_en"])}" data-note-tr="{NF.E(N["note_tr"])}">{NF.E(note)}</p>'
        f'<p class="crs-film-dl">{NF.E(U["dl"])} '
        f'<a href="{transcript_href(lang, "txt")}" download>{NF.E(U["txt"])}</a> '
        f'<a href="{transcript_href(lang, "pdf")}" download>{NF.E(U["pdf"])}</a></p>'
        f'<ol class="crs-film-lines" lang="{lang}">{ol}</ol></details>'
        f'</figure>'
    )


def plain(lang):
    N = NOTES[lang]
    note = N['note_en'] if lang == 'en' else N['note_tr']
    rows = [f'{NF.clock(c["t"])}  {c[lang]}' for c in cues()]
    return (
        f'{TITLE}\n'
        'NASA Connect. August 18, 2007. 6:01.\n'
        f'{WATCH}\n\n'
        f'{note}\n\n'
        + '\n'.join(rows) + '\n'
    )
