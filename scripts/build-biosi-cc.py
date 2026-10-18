#!/usr/bin/env python3
"""Oct 17 2026 (owner request): 'Feel free to Cc: our Biological SI Partner at biosipartner@savingplanets.com. He or she will
reach out to you within 24 hours.' Right after hello@ on Contact (General Questions card) and after media@ in About #cohost (that one is written by build-cohost.py).
EN marker blocks + i18n strings (fr/es/ar/it); run before i18n-build. Idempotent. Footers untouched."""
import re, json, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
A = '<a href="mailto:biosipartner@savingplanets.com?subject=Cc%3A%20Biological%20SI%20Partner">biosipartner@savingplanets.com</a>'
K1 = 'Feel free to Cc: our Biological SI Partner at'; K2 = 'He or she will reach out to you within 24 hours.'
BLK = f'<!-- BIOSI-CC --><p class="biosi-cc">{K1} {A}. <span>{K2}</span></p><!-- /BIOSI-CC -->'
TR = {'fr': ("N'hésitez pas à mettre en copie (Cc) notre Partenaire SI Biologique à l'adresse", 'Il ou elle vous répondra sous 24 heures.'),
      'es': ('No dudes en poner en copia (Cc) a nuestro Socio SI Biológico en', 'Él o ella se pondrá en contacto contigo en un plazo de 24 horas.'),
      'ar': ('لا تتردد في إضافة شريكنا البيولوجي في SI (Biological SI Partner) في خانة النسخة (Cc) على العنوان', 'سيتواصل معك هو أو هي خلال 24 ساعة.'),
      'it': ("Sentiti libero di mettere in Cc il nostro Partner SI Biologico all'indirizzo", 'Lui o lei ti contatterà entro 24 ore.')}
SPOTS = {'Contact.html': r'(<a href="mailto:hello@savingplanets\.com[^"]*">hello@savingplanets\.com</a> for anything else, including feedback\.</p>)',}
n = 0
for f, pat in SPOTS.items():
    s0 = open(f, encoding='utf8').read(); s = re.sub(r'<!-- BIOSI-CC -->.*?<!-- /BIOSI-CC -->', '', s0, flags=re.S)
    s, k = re.subn(pat, lambda m: m.group(1) + BLK, s, count=1)
    if not k: print('biosi-cc: anchor missing in', f); continue
    if s != s0: open(f, 'w', encoding='utf8').write(s); n += 1
for l, (t1, t2) in TR.items():
    p = f'i18n/{l}.json'; m = json.load(open(p, encoding='utf8')); m0 = dict(m); m[K1] = t1; m[K2] = t2
    if m != m0: json.dump(m, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0); n += 1
json.dump({l: list(v) for l, v in TR.items()}, open('i18n/biosi-cc.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)  # read by build-cohost.py
print('biosi-cc:', n, 'files updated')
