#!/usr/bin/env python3
"""One credit tag for SI-made media: 'Created by the Founder and SI' (and the same line in each language).

Also converts that phrase inside the Saturn hero, including assets/hero-themes.js. Idempotent.
"""
import os, re

os.chdir(os.path.join(os.path.dirname(__file__), '..'))

PAIRS = (
    ('Created by the Founder and SI', 'Created by the Founder and SI'),
    ('Créé par SI et Biological SI Partner', 'Créé par le fondateur et SI'),
    ('Creado por SI y Biological SI Partner', 'Creado por el fundador y SI'),
    ('Creato da SI e Biological SI Partner', 'Creato dal fondatore e da SI'),
    ('أُنشئ بواسطة SI وBiological SI Partner', 'من إعداد المؤسس وSI'),
    ('נוצר על ידי SI ושותף SI ביולוגי', 'נוצר על ידי המייסד ו-SI'),
    ('Logo created by the Founder and SI', 'Logo created by the Founder and SI'),
    ('Logo créé par SI et Biological SI Partner', 'Logo créé par le fondateur et SI'),
    ('Logo creato da SI e Biological SI Partner', 'Logo creato dal fondatore e da SI'),
    ('Logotipo creado por el fundador y SI', 'Logotipo creado por el fundador y SI'),
    ('Logo creado por SI y Socio biológico SI', 'Logo hecho a partir de SI y Socio biológico SI'),
    ('الشعار من إعداد المؤسس وSI', 'الشعار من إعداد المؤسس وSI'),
)
SKIP = {
    'NOTES.md',
    'scripts/fix-si-credit-tag.py',
}
EXTS = {'.html', '.py', '.js', '.json', '.vtt', '.csv', '.css', '.md', '.sh'}

def convert(text):
    for old, new in PAIRS:
        text = text.replace(old, new)
    return text

def convert_file(text, path):
    return convert(text)

n = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.venv')]
    for name in files:
        path = os.path.join(root, name)[2:]
        if path in SKIP or os.path.splitext(name)[1] not in EXTS:
            continue
        raw = open(path, encoding='utf8').read()
        nxt = convert_file(raw, path)
        if nxt != raw:
            open(path, 'w', encoding='utf8').write(nxt)
            n += 1
print('si credit tag updated in', n, 'files')
