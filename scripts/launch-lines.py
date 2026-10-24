#!/usr/bin/env python3
"""Factual launch-vehicle line on mission pages (founder-approved Oct 24 2026).
Adds one <p> after the first paragraph of the 'When' card, with a NASA LSP
launch-archive source, in en/fr/es/ar/it/he, and records the translations in
i18n/<lang>.json. Mission-centred wording, not promotion. Idempotent (class="launch-line" marker)."""
import json, re, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
SRC = ('https://www.nasa.gov/reference/lsp-primary-launches-archive/', 'NASA, LSP primary launches archive')
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
LINES = {
 'SWOT.html': ("Launched on a SpaceX Falcon 9 on December 16, 2022 from Vandenberg, California.",
  "Lancé sur une Falcon 9 de SpaceX le 16 décembre 2022 depuis Vandenberg, en Californie.",
  "Lanzado en un Falcon 9 de SpaceX el 16 de diciembre de 2022 desde Vandenberg, California.",
  "أُطلق على صاروخ Falcon 9 من SpaceX في 16 ديسمبر 2022 من فاندنبرغ، كاليفورنيا.",
  "Lanciato su un Falcon 9 di SpaceX il 16 dicembre 2022 da Vandenberg, in California.",
  "שוגר על Falcon 9 של SpaceX ב-16 בדצמבר 2022 מוונדנברג, קליפורניה."),
 'GOES-19.html': ("Launched (as GOES-U) on a SpaceX Falcon Heavy on June 25, 2024 from NASA's Kennedy Space Center, Florida.",
  "Lancé (sous le nom GOES-U) sur une Falcon Heavy de SpaceX le 25 juin 2024 depuis le centre spatial Kennedy de la NASA, en Floride.",
  "Lanzado (como GOES-U) en un Falcon Heavy de SpaceX el 25 de junio de 2024 desde el Centro Espacial Kennedy de la NASA, Florida.",
  "أُطلق (باسم GOES-U) على صاروخ Falcon Heavy من SpaceX في 25 يونيو 2024 من مركز كينيدي للفضاء التابع لناسا، فلوريدا.",
  "Lanciato (come GOES-U) su un Falcon Heavy di SpaceX il 25 giugno 2024 dal Kennedy Space Center della NASA, in Florida.",
  "שוגר (בשם GOES-U) על Falcon Heavy של SpaceX ב-25 ביוני 2024 ממרכז החלל קנדי של נאס\"א, פלורידה."),
 'Sentinel-6B.html': ("Launched on a SpaceX Falcon 9 from Vandenberg, California, as was Sentinel-6 Michael Freilich on November 21, 2020.",
  "Lancé sur une Falcon 9 de SpaceX depuis Vandenberg, en Californie, comme Sentinel-6 Michael Freilich le 21 novembre 2020.",
  "Lanzado en un Falcon 9 de SpaceX desde Vandenberg, California, igual que Sentinel-6 Michael Freilich el 21 de noviembre de 2020.",
  "أُطلق على صاروخ Falcon 9 من SpaceX من فاندنبرغ، كاليفورنيا، كما أُطلق Sentinel-6 Michael Freilich في 21 نوفمبر 2020.",
  "Lanciato su un Falcon 9 di SpaceX da Vandenberg, in California, come Sentinel-6 Michael Freilich il 21 novembre 2020.",
  "שוגר על Falcon 9 של SpaceX מוונדנברג, קליפורניה, כמו Sentinel-6 Michael Freilich ב-21 בנובמבר 2020."),
}
WHEN = {'en': 'When', 'fr': 'Quand', 'es': 'Cuándo', 'ar': 'متى', 'it': 'Quando', 'he': 'מתי'}
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
for i, lang in enumerate(LANGS):
    for page, texts in LINES.items():
        p = R / page if lang == 'en' else R / lang / page
        h = p.read_text(encoding='utf-8')
        if 'class="launch-line"' in h: continue
        m = re.search(r'(<h3>' + WHEN[lang] + r'</h3><p>(?:(?!</p>).)*</p>)(<p class="fact-source">([^<]*)<a)', h)
        assert m, (lang, page)
        lab = m.group(3)
        add = (f'<p class="launch-line">{esc(texts[i])}</p><p class="fact-source">{lab}'
               f'<a href="{SRC[0]}" target="_blank" rel="noreferrer">{SRC[1]}</a></p>')
        h = h[:m.end(1)] + add + h[m.end(1):]
        p.write_text(h, encoding='utf-8'); print('patched', lang, page)
    if lang == 'en': continue
    jp = R / 'i18n' / f'{lang}.json'
    raw = jp.read_text(encoding='utf-8'); d = json.loads(raw)
    new = [f'{json.dumps(t[0], ensure_ascii=False)}: {json.dumps(t[i], ensure_ascii=False)},' for t in LINES.values() if t[0] not in d]
    if new:
        k = raw.index('\n') + 1  # insert right after the opening brace line
        raw = raw[:k] + '\n'.join(new) + '\n' + raw[k:]
        json.loads(raw); jp.write_text(raw, encoding='utf-8')
