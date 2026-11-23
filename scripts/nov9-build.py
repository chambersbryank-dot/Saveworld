#!/usr/bin/env python3
"""Translate the Nov 9 solution pages and apply the Nov 23 quality fixes.
Created by the Founder and SI.
"""
import importlib.util, json, os, re, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, 'scripts')
NOV9 = ['Vera_C_Rubin_Observatory.html', 'Hawaiian_Monk_Seal_Recovery.html', 'Ice_Memory_Sanctuary.html',
        'Blue_Ventures.html', 'North_Aral_Sea.html', 'Mono_Lake_Committee.html', 'Mekong_River_Commission.html',
        'SOS_Mata_Atlantica.html', 'Proba-3.html', 'MicroCarb.html']
LANGS = ['fr', 'es', 'ar', 'it', 'he']
TODAY = '2026-11-23'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def fix_switchers():
    for page in NOV9:
        s = open(page, encoding='utf8').read()
        orig = s
        for lang in LANGS:
            s = s.replace(f'href="{lang}/index.html"', f'href="{lang}/{page}"')
        if 'hreflang="fr"' not in s:
            block = '\n'.join(
                f'<link rel="alternate" hreflang="{lang}" href="https://www.savingplanets.com/{lang}/{page}">'
                for lang in LANGS)
            s = s.replace(
                f'<link rel="alternate" hreflang="x-default" href="https://www.savingplanets.com/{page}">',
                block + '\n<link rel="alternate" hreflang="x-default" href="https://www.savingplanets.com/' + page + '">')
        if s != orig:
            open(page, 'w', encoding='utf8').write(s)
            print('switcher', page)

def merge_tr():
    tr = load('nov9', 'scripts/nov9-tr.py')
    for lang in LANGS:
        path = f'i18n/{lang}.json'
        data = json.load(open(path, encoding='utf8'))
        n = 0
        for en, bag in tr.EXTRA.items():
            if lang in bag and data.get(en) != bag[lang]:
                data[en] = bag[lang]
                n += 1
        for page in NOV9:
            # cite lines if present
            s = open(page, encoding='utf8').read()
            m = re.search(r'data-cite="apa">(.*?)</p>', s)
            if not m:
                continue
            apa = re.sub(r'<[^>]+>', '', m.group(1))
            # leave cite to i18n patterns where possible
        text = json.dumps(data, ensure_ascii=False, indent=0) + '\n'
        open(path, 'w', encoding='utf8').write(text)
        print(lang, 'nov9 strings', n)

def lists():
    for fn in ('i18n/pages.txt', 'i18n/he-pages.txt'):
        lines = open(fn, encoding='utf8').read().splitlines()
        for p in NOV9:
            if p not in lines:
                lines.append(p)
        open(fn, 'w', encoding='utf8').write('\n'.join(lines) + '\n')

def translate():
    ib = load('i18n_build', 'scripts/i18n-build.py')
    ib.PAGES = [l.strip() for l in open('i18n/pages.txt', encoding='utf8') if l.strip() and not l.startswith('#')]
    for lang in LANGS:
        m = json.load(open(f'i18n/{lang}.json', encoding='utf8'))
        ib.CUR_PAGES = ib.L10N.pages_for(lang, ib.PAGES)
        for page in NOV9:
            ib.build(page, lang, m)
        print('built', lang, len(NOV9))

def sitemap():
    block_src = open('sitemap-en.xml', encoding='utf8').read()
    i = block_src.find('<url><loc>https://www.savingplanets.com/Lake_Washington_Cleanup.html</loc>')
    j = block_src.find('</url>', i) + len('</url>')
    sample = block_src[i:j]
    for lang, prefix in [('en', ''), ('fr', 'fr/'), ('es', 'es/'), ('ar', 'ar/'), ('it', 'it/'), ('he', 'he/')]:
        path = f'sitemap-{lang}.xml'
        sm = open(path, encoding='utf8').read()
        for page in NOV9:
            if f'/{prefix}{page}' in sm or (lang == 'en' and f'/{page}' in sm and f'/fr/{page}' not in sm[sm.find(page)-5:sm.find(page)+5]):
                # still insert if the language loc is missing
                loc = f'https://www.savingplanets.com/{prefix}{page}'
                if f'<loc>{loc}</loc>' in sm:
                    continue
            entry = sample.replace('Lake_Washington_Cleanup.html', page).replace('2026-11-19', TODAY)
            if lang != 'en':
                entry = entry.replace(
                    f'<loc>https://www.savingplanets.com/{page}</loc>',
                    f'<loc>https://www.savingplanets.com/{prefix}{page}</loc>', 1)
            sm = sm.replace('</urlset>', '  ' + entry + '\n</urlset>')
        open(path, 'w', encoding='utf8').write(sm)
        print('sitemap', lang)

def glossary(pages):
    bb = load('batchb', 'scripts/build-batch-b.py')
    bb.GLOSS_LABEL['he'] = 'מילון'
    orig = list(bb.GL)
    total = 0
    for lang in ['en'] + LANGS:
        bb.GL = [t for t in orig if lang in t and isinstance(t.get(lang), dict) and t[lang].get('match')]
        for page in pages:
            f = page if lang == 'en' else f'{lang}/{page}'
            if not os.path.exists(f):
                continue
            s, n = bb.tooltipify(bb.rd(f), lang)
            total += n
            bb.wr(f, s)
    print('glossary tips', total)

def hwf_credit():
    rx = re.compile(r'(Hawksbill_Chris_Spain\.jpg".{0,900}?<bdi>)NASA \(ISS072-E-421839\)(</bdi>)', re.S)
    for lang in [''] + [l + '/' for l in LANGS]:
        path = lang + 'Solutions.html'
        s = open(path, encoding='utf8').read()
        s2, n = rx.subn(r'\1Chris Spain, CC0\2', s, count=1)
        if n != 1:
            print('CREDIT MISS', path, n)
        else:
            open(path, 'w', encoding='utf8').write(s2)
            print('credit', path)

HOOK = {
    'en': 'Since 1996, Hawaiʻi Wildlife Fund has protected more than 10,300 hawksbill hatchlings and removed more than 450 tons of marine debris.',
    'fr': 'Depuis 1996, Hawaiʻi Wildlife Fund a protégé plus de 10 300 nouveau-nés de tortue imbriquée et retiré plus de 450 tonnes de déchets marins.',
    'es': 'Desde 1996, Hawaiʻi Wildlife Fund ha protegido más de 10.300 crías de tortuga carey y ha retirado más de 450 toneladas de residuos marinos.',
    'ar': 'منذ 1996، حمى Hawaiʻi Wildlife Fund أكثر من 10,300 فرخ من سلاحف منقار الصقر وأزال أكثر من 450 طنًا من الحطام البحري.',
    'it': 'Dal 1996, Hawaiʻi Wildlife Fund ha protetto più di 10.300 piccoli di tartaruga embricata e ha rimosso più di 450 tonnellate di rifiuti marini.',
    'he': 'מאז 1996 הגן Hawaiʻi Wildlife Fund על יותר מ-10,300 אבקועים של צב ים קרני והוציא יותר מ-450 טונות של פסולת ימית.',
}
TYPE = {'en': 'Sheet', 'fr': 'Fiche', 'es': 'Ficha', 'it': 'Scheda', 'ar': 'ورقة', 'he': 'דף'}
PRINT = {'en': 'Print', 'fr': 'Imprimer', 'es': 'Imprimir', 'it': 'Stampa', 'ar': 'اطبع', 'he': 'הדפסה'}

def teacher_card(lang):
    pre = '' if lang == 'en' else '../'
    return (
        f'<li class="t-card" data-type="sheet" data-grades="6-8" data-subjects="earth life literacy" data-codes="MS-ESS3-3|MS-LS2-5|CCSS RST.6-8.1">'
        f'<a class="t-card-main" href="Hawaii_Wildlife_Fund.html#teachers"><figure class="t-shot"><picture>'
        f'<source type="image/webp" srcset="{pre}assets/Hawksbill_Chris_Spain-800.webp 800w" sizes="(max-width:720px) 92vw, 280px">'
        f'<img src="{pre}assets/Hawksbill_Chris_Spain.jpg" alt="A hawksbill sea turtle swimming over a coral reef" width="1200" height="675" loading="lazy" decoding="async"></picture>'
        f'<figcaption class="t-credit" dir="ltr">Photo: Chris Spain, CC0.</figcaption></figure>'
        f'<span class="t-card-body"><span class="t-type">{TYPE[lang]}</span><span class="t-card-title">Hawaiʻi Wildlife Fund</span>'
        f'<span class="t-hook">{HOOK[lang]}</span><span class="t-pills"><span class="t-pill" dir="ltr">6-8</span></span></span></a>'
        f'<a class="t-print t-chip" href="Hawaii_Wildlife_Fund.html?print=1" rel="nofollow">{PRINT[lang]}</a></li>'
    )

def teachers():
    for lang in ['en'] + LANGS:
        path = 'Teachers.html' if lang == 'en' else f'{lang}/Teachers.html'
        s = open(path, encoding='utf8').read()
        if 'Hawaii_Wildlife_Fund.html#teachers' in s:
            print('teacher exists', path)
            continue
        needle = 'Surfrider_Foundation.html#teachers'
        i = s.find(needle)
        if i < 0:
            print('no surfrider', path)
            continue
        j = s.rfind('<li class="t-card"', 0, i)
        s = s[:j] + teacher_card(lang) + s[j:]
        open(path, 'w', encoding='utf8').write(s)
        print('teacher', path)

def main():
    fix_switchers()
    lists()
    merge_tr()
    translate()
    sitemap()
    glossary(NOV9 + ['Hawaii_Wildlife_Fund.html', 'DART.html', 'Onondaga_Lake_Cleanup.html', 'Hudson_River_PCB_Cleanup.html', 'Lake_Geneva_CIPEL.html', 'Emscher_River_Restoration.html'])
    hwf_credit()
    teachers()
    print('nov9 build done')

if __name__ == '__main__':
    main()
