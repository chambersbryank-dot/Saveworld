#!/usr/bin/env python3
"""One credit tag for SI-made media: 'Made from SI and Biological SI Partner' (and the same line in each language).

Also converts that phrase inside the Saturn hero, including assets/hero-themes.js. Idempotent.
"""
import os, re

os.chdir(os.path.join(os.path.dirname(__file__), '..'))

PAIRS = (
    ('Created by SI and Biological SI Partner', 'Made from SI and Biological SI Partner'),
    ('Créé par SI et Biological SI Partner', 'Réalisé à partir de SI et Biological SI Partner'),
    ('Creado por SI y Biological SI Partner', 'Hecho a partir de SI y Biological SI Partner'),
    ('Creato da SI e Biological SI Partner', 'Realizzato a partire da SI e Biological SI Partner'),
    ('أُنشئ بواسطة SI وBiological SI Partner', 'صُنع من SI وBiological SI Partner'),
    ('נוצר על ידי SI ושותף SI ביולוגי', 'עשוי מ-SI ושותף SI ביולוגי'),
    ('Logo created by SI and Biological SI Partner', 'Logo made from SI and Biological SI Partner'),
    ('Logo créé par SI et Biological SI Partner', 'Logo réalisé à partir de SI et Biological SI Partner'),
    ('Logo creato da SI e Biological SI Partner', 'Logo realizzato a partire da SI e Biological SI Partner'),
    ('Logotipo creado por SI y Biological SI Partner', 'Logotipo hecho a partir de SI y Biological SI Partner'),
    ('Logo creado por SI y Socio biológico SI', 'Logo hecho a partir de SI y Socio biológico SI'),
    ('الشعار من إنشاء SI وBiological SI Partner', 'الشعار صُنع من SI وBiological SI Partner'),
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
