#!/usr/bin/env python3
"""Nov 1 2026 Site Assessor trust fixes that are not a full weekly-sync.
Idempotent. Generators (a11y-pass, apply-anim-banners, si-credits, build-courses,
build-solutions-index) keep the same rules for the next sync."""
import glob, html, json, os, re
from PIL import Image

os.chdir(os.path.join(os.path.dirname(__file__), '..'))

# --- banner map: the photo that opens the page is the subject, not a shared pool shot ---
CFG = 'assets/data/anim-banners.json'
cfg = json.load(open(CFG, encoding='utf8'))
cfg['images']['assets/Astroscale_ADRAS-J_H-IIA_Stage.jpg'] = {
    'credit': 'Astroscale, via Wikimedia Commons (CC BY-SA 4.0, illustration)',
    'alt': "Artist's illustration of Astroscale's ADRAS-J spacecraft approaching a spent H-IIA rocket upper stage in orbit",
    'local': 'assets/Astroscale_ADRAS-J_H-IIA_Stage.jpg',
    'pos': '50% 40%',
}
cfg['images']['assets/ALOS-4_Model_Tsukuba.jpg'] = {
    'credit': "Syced, via Wikimedia Commons (CC0). A 1/50 scale model of ALOS-4 at JAXA's Tsukuba Space Center.",
    'alt': "JAXA's 1/50 scale model of ALOS-4, with its PALSAR-3 radar antenna and solar arrays, at Tsukuba Space Center",
    'local': 'assets/ALOS-4_Model_Tsukuba.jpg',
    'pos': '50% 45%',
}
cfg['images']['assets/GEDI_on_ISS.jpg'] = {
    'credit': 'NASA (iss059e088632)',
    'alt': 'The GEDI forest-mapping laser mounted outside the Kibo module on the International Space Station',
    'pos': '50% 50%',
    'r2': 'images/sol-cards/GEDI_on_ISS_iss059e088632.jpg',
}
cfg['pages']['Astroscale.html'] = 'assets/Astroscale_ADRAS-J_H-IIA_Stage.jpg'
cfg['pages']['ALOS-4.html'] = 'assets/ALOS-4_Model_Tsukuba.jpg'
cfg['pages']['GEDI.html'] = 'assets/GEDI_on_ISS.jpg'
# Kilimanjaro is Eden's photo (Tanzania). The same file was also the hero, the further-info
# picture, and the related card for Justdiggit, Trees for the Future, and WeForest.
kili = cfg['images'].setdefault('assets/Kilimanjaro_STS72.jpg', {})
kili['alt'] = 'Mount Kilimanjaro and the surrounding highlands in Tanzania, seen from the Space Shuttle'
cfg['images']['assets/hub/ESA_S2_Southeast_Kenya.jpg'] = {
    'credit': 'contains modified Copernicus Sentinel data (2023), processed by ESA',
    'alt': 'Southeast Kenya seen by the Copernicus Sentinel-2 satellite, with green vegetated land along the coast and drier land inland',
    'pos': '50% 50%',
    'r2': 'images/hub/ESA_S2_Southeast_Kenya.jpg',
}
cfg['images']['assets/hub/ESA_S2_Tana_River_Kenya.jpg'] = {
    'credit': 'contains modified Copernicus Sentinel data (2020), processed by ESA',
    'alt': 'The Tana River winding across the land in Kenya, seen by the Copernicus Sentinel-2 satellite',
    'pos': '50% 50%',
    'r2': 'images/hub/ESA_S2_Tana_River_Kenya.jpg',
}
cfg['images']['assets/hub/USFS_Seedling_Planting_Custer_Gallatin.jpg'] = {
    'credit': 'U.S. Forest Service',
    'alt': 'A tree seedling being planted on the Sioux Ranger District of Custer Gallatin National Forest',
    'pos': '50% 40%',
    'r2': 'images/hub/USFS_Seedling_Planting_Custer_Gallatin.jpg',
}
cfg['pages']['Justdiggit.html'] = 'assets/hub/ESA_S2_Southeast_Kenya.jpg'
cfg['pages']['Trees_for_the_Future.html'] = 'assets/hub/ESA_S2_Tana_River_Kenya.jpg'
cfg['pages']['WeForest.html'] = 'assets/hub/USFS_Seedling_Planting_Custer_Gallatin.jpg'
# Empty curated list: only the page photo. A shared forest/orbit pool was putting a shuttle
# clearing on ALOS-4 and Eden, and the whole station on GEDI.
for page in ('Astroscale.html', 'ALOS-4.html', 'GEDI.html', 'Eden_People_Planet.html',
             'Justdiggit.html', 'Trees_for_the_Future.html', 'WeForest.html'):
    cfg['slides'].setdefault('curated', {})[page] = []
json.dump(cfg, open(CFG, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
open(CFG, 'a').write('\n')
print('anim-banners: Astroscale, ALOS-4, GEDI, Eden curated')

# Local fallback for the GEDI hero CSS (the banner itself uses the R2 master).
if not os.path.exists('assets/GEDI_on_ISS.jpg'):
    import subprocess
    url = 'https://media.savingplanets.com/images/sol-cards/GEDI_on_ISS_iss059e088632-1280.a9b0642b19e6.webp'
    subprocess.check_call(['curl', '-fsSL', '-A', 'Mozilla/5.0', '-o', '/tmp/gedi-card.webp', url])
    Image.open('/tmp/gedi-card.webp').convert('RGB').save('assets/GEDI_on_ISS.jpg', quality=72, optimize=True)
    print('saved assets/GEDI_on_ISS.jpg', os.path.getsize('assets/GEDI_on_ISS.jpg'))

# --- solution-card photo book (next build-solutions-index) ---
photos = json.load(open('assets/data/solutions-card-photos.json', encoding='utf8'))
photos['keep']['assets/Kilimanjaro_STS72.jpg'] = 'Eden_People_Planet.html'
photos['photos']['Eden_People_Planet.html'] = {
    'src': 'assets/Kilimanjaro_STS72.jpg',
    'alt': 'Mount Kilimanjaro and the surrounding highlands in Tanzania, seen from the Space Shuttle',
    'credit': 'NASA (STS-72)',
}
photos['photos']['Justdiggit.html'] = {
    'src': 'assets/hub/ESA_S2_Southeast_Kenya.jpg',
    'alt': 'Southeast Kenya seen by the Copernicus Sentinel-2 satellite, with green vegetated land along the coast and drier land inland',
    'credit': 'contains modified Copernicus Sentinel data (2023), processed by ESA',
}
json.dump(photos, open('assets/data/solutions-card-photos.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
open('assets/data/solutions-card-photos.json', 'a').write('\n')

SI = {
    'en': 'Made from SI and Biological SI Partner',
    'fr': 'Réalisé à partir de SI et Biological SI Partner',
    'es': 'Hecho a partir de SI y Biological SI Partner',
    'ar': 'صُنع من SI وBiological SI Partner',
    'it': 'Creato da SI et Biological SI Partner'.replace(' et ', ' e '),
    'he': 'עשוי מ-SI ושותף SI ביולוגי',
}
SI['it'] = 'Realizzato a partire da SI e Biological SI Partner'
SHORT = re.compile(
    r'(?:Photo|Image|Imagen|Immagine|Foto|Illustration)\s*:\s*SI Partner\.?|'
    r'الصورة:\s*SI Partner\.?|תמונה:\s*SI Partner\.?'
)

def lang_of(path):
    top = path.split('/')[0]
    return top if top in SI else 'en'

def patch_credits(s, lang):
    return SHORT.sub(SI[lang], s)

# Hub / homepage / solutions card image swaps. (file glob, old src fragment, new src)
SWAPS = [
    ('Astroscale_Agena_Rendezvous.jpg', 'Astroscale_ADRAS-J_H-IIA_Stage.jpg'),
    ('Satellite_Servicing_Arm_GSFC.jpg', 'Astroscale_ADRAS-J_H-IIA_Stage.jpg'),
]
# Only inside links to Astroscale, so other pages that correctly use the servicing-arm photo stay.
def each_article(s, fn):
    parts = s.split('<article')
    out = [parts[0]]
    for part in parts[1:]:
        end = part.find('</article>')
        if end < 0:
            out.append('<article' + part)
            continue
        block = '<article' + part[:end] + '</article>'
        rest = part[end + len('</article>'):]
        out.append(fn(block) + rest)
    return ''.join(out)

def swap_astro(s):
    def one(block):
        if 'Astroscale.html' not in block:
            return block
        return (block.replace('Satellite_Servicing_Arm_GSFC.jpg', 'Astroscale_ADRAS-J_H-IIA_Stage.jpg')
                     .replace('Astroscale_Agena_Rendezvous.jpg', 'Astroscale_ADRAS-J_H-IIA_Stage.jpg'))
    return each_article(s, one)

def swap_gedi_hub(s):
    """Forests hub card for GEDI used the whole station. Use the instrument photo."""
    def one(block):
        if 'GEDI.html' not in block or 'GEDI_on_ISS' in block:
            return block
        img = ('<img src="assets/GEDI_on_ISS.jpg" alt="The GEDI forest-mapping laser mounted outside the Kibo module on the International Space Station" '
               'width="1280" height="854" loading="lazy" decoding="async">')
        if '../assets/' in block:
            img = img.replace('src="assets/', 'src="../assets/')
        return re.sub(r'<picture\b[^>]*>.*?</picture>|<img\b[^>]*>', img, block, count=1, flags=re.S)
    return each_article(s, one)

def swap_alos_hub(s):
    def one(block):
        if 'ALOS-4.html' not in block or 'ALOS-4_Model_Tsukuba' in block:
            return block
        img = ('<img src="assets/ALOS-4_Model_Tsukuba.jpg" alt="JAXA\'s 1/50 scale model of ALOS-4, with its PALSAR-3 radar antenna and solar arrays, at Tsukuba Space Center" '
               'width="1280" height="964" loading="lazy" decoding="async">')
        if '../assets/' in block or 'src="../' in block:
            img = img.replace('src="assets/', 'src="../assets/')
        return re.sub(r'<picture\b[^>]*>.*?</picture>|<img\b[^>]*>', img, block, count=1, flags=re.S)
    return each_article(s, one)

def swap_eden_sol(s):
    def one(block):
        if 'Eden_People_Planet.html' not in block:
            return block
        return block.replace('Portugal_Wildfires_ISS_2018.jpg', 'Kilimanjaro_STS72.jpg')
    return each_article(s, one)

def swap_just_sol(s):
    def one(block):
        if 'Justdiggit.html' not in block or 'Kilimanjaro_STS72' not in block:
            return block
        pre = '../' if '../assets/' in block else ''
        return block.replace(pre + 'assets/Kilimanjaro_STS72.jpg', pre + 'assets/hub/ESA_S2_Southeast_Kenya.jpg')
    return each_article(s, one)

# Homepage WebP fallbacks for card <img src> that still point at a full JPEG.
def webp_fallback(src_path):
    if not os.path.exists(src_path):
        return None
    base, ext = os.path.splitext(src_path)
    if ext.lower() not in ('.jpg', '.jpeg', '.png'):
        return None
    out = base + '-800.webp'
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src_path):
        im = Image.open(src_path).convert('RGB')
        w = 800 if im.width > 800 else im.width
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width != w else im
        im.save(out, quality=95, method=6)
    return out

def homepage_webp(s, lang):
    pre = '' if lang == 'en' else '../'
    def one(m):
        tag = m.group(0)
        src = re.search(r'\ssrc="([^"]+)"', tag)
        if not src:
            return tag
        path = src.group(1).split('?')[0]
        local = path[3:] if path.startswith('../') else path
        # The Saturn hero CSS background is not an <img>. Do not swap a Saturn master,
        # or any card that already has a srcset, for an 800px-only file.
        if 'Saturn' in local or 'srcset=' in tag:
            return tag
        if not local.startswith('assets/'):
            return tag
        if local.endswith('.webp'):
            return tag
        if os.path.getsize(local) < 80_000 if os.path.exists(local) else True:
            return tag
        web = webp_fallback(local)
        if not web:
            return tag
        new = pre + web
        tag = tag.replace(src.group(1), new, 1)
        if 'srcset=' not in tag:
            w480 = os.path.splitext(local)[0] + '-480.webp'
            if not os.path.exists(w480):
                im = Image.open(local).convert('RGB')
                im.resize((480, round(im.height * 480 / im.width)), Image.LANCZOS).save(w480, quality=95, method=6)
            tag = tag.replace('<img', f'<img srcset="{pre}{w480} 480w, {new} 800w" sizes="(max-width:700px) 92vw, 400px"', 1)
        return tag
    return re.sub(r'<img\b[^>]*>', one, s)

# Course pages: last-updated, real unit/lab counts, what a check is, no wet-lab heading on computer labs.
WET_PAGES = {'General_Chemistry_I.html', 'Physics_I.html'}
WET_H = {
    'en': 'Lab equipment (for the wet labs)',
    'fr': 'Matériel de TP (pour les TP en laboratoire)',
    'es': 'Material de laboratorio (para los laboratorios presenciales)',
    'ar': 'معدات المختبر (للمختبرات العملية)',
    'he': 'ציוד מעבדה (למעבדות הרטובות)',
    'it': 'Attrezzatura di laboratorio (per i laboratori reali)',
}
GEAR = {'en': 'What you need', 'fr': 'Ce qu’il vous faut', 'es': 'Qué necesitas', 'ar': 'ماذا تحتاج', 'it': 'Che cosa ti serve', 'he': 'מה צריך'}
UPD = {'en': 'Last updated', 'fr': 'Dernière mise à jour', 'es': 'Última actualización', 'ar': 'آخر تحديث', 'it': 'Ultimo aggiornamento', 'he': 'עודכן לאחרונה'}
VER = {'en': 'Version', 'fr': 'Version', 'es': 'Versión', 'ar': 'الإصدار', 'it': 'Versione', 'he': 'גרסה'}
CHK = {
 'en': 'A check is one number or code result on a course page that a script recomputes before the page is published. The printed number and the recomputed number have to match.',
 'fr': 'Un contrôle est un nombre ou un résultat de code sur une page de cours qu’un script recalcule avant publication. Le nombre affiché et le nombre recalculé doivent correspondre.',
 'es': 'Una comprobación es un número o un resultado de código en una página de curso que un script vuelve a calcular antes de publicar. El número impreso y el recalculado tienen que coincidir.',
 'ar': 'التحقق هو رقم أو نتيجة برمجية في صفحة مقرر يعيد سكربت حسابها قبل النشر. يجب أن يطابق الرقم المعروض الرقم المعاد حسابه.',
 'it': 'Un controllo è un numero o un risultato di codice in una pagina del corso che uno script ricalcola prima della pubblicazione. Il numero stampato e quello ricalcolato devono coincidere.',
 'he': 'בדיקה היא מספר או תוצאת קוד בעמוד קורס שסקריפט מחשב מחדש לפני הפרסום. המספר המודפס והמספר שחושב מחדש חייבים להתאים.',
}
SCOPE = {
 'en': 'This free course has {n} units and {m} labs. Those are the real counts, not a longer syllabus cut short.',
 'fr': 'Ce cours gratuit compte {n} unités et {m} travaux pratiques. Ce sont les vrais totaux, pas un programme plus long raccourci.',
 'es': 'Este curso gratuito tiene {n} unidades y {m} laboratorios. Son los totales reales, no un programa más largo recortado.',
 'ar': 'يتضمن هذا المقرر المجاني {n} وحدات و{m} مختبرات. هذه الأعداد الحقيقية وليست منهجًا أطول جرى اختصاره.',
 'it': 'Questo corso gratuito ha {n} unità e {m} laboratori. Sono i totali reali, non un programma più lungo accorciato.',
 'he': 'לקורס החינמי הזה יש {n} יחידות ו-{m} מעבדות. אלה המספרים האמיתיים, לא תוכנית ארוכה יותר שקוצרה.',
}

def course_patch(s, lang, page):
    if 'data-course=' not in s and page != 'Courses.html':
        return s
    if '<p class="crs-crumb"' in s and 'crs-updated' not in s:
        s = re.sub(r'(<p class="crs-crumb">.*?</p>)',
                   r'\1<p class="crs-updated">' + html.escape(UPD[lang]) + ': <time datetime="2026-11-01">November 1, 2026</time> · ' + html.escape(VER[lang]) + ' 2026.11.01</p>',
                   s, count=1, flags=re.S)
    if page not in WET_PAGES and WET_H[lang] in s:
        s = s.replace(WET_H[lang], GEAR[lang], 1)
    if page != 'Courses.html' and 'crs-scope' not in s and 'id="about"' in s:
        n = len(re.findall(r'<section class="crs-unit"', s))
        m = len(re.findall(r'class="crs-lab"', s)) or len(re.findall(r'id="lab[A-Z]"', s))
        if not m:
            m = len(re.findall(r'<div class="crs-card crs-lab"', s))
        note = ('<p class="crs-scope">' + html.escape(SCOPE[lang].replace('{n}', str(n)).replace('{m}', str(m)))
                + '</p><p class="crs-check">' + html.escape(CHK[lang]) + '</p>')
        s = s.replace('id="about"><h2>', 'id="about"><h2>', 1)
        s = re.sub(r'(<section id="about"><h2>.*?</h2>)', r'\1' + note, s, count=1, flags=re.S)
    if page == 'Courses.html' and 'crs-check' not in s:
        s = s.replace('</h2>', '</h2><p class="crs-check">' + html.escape(CHK[lang]) + '</p>', 1)
    return s

_TEX = [('\\tau', 'τ'), ('\\mu', 'μ'), ('\\rho', 'ρ'), ('\\nu', 'ν'), ('\\theta', 'θ'), ('\\Delta', 'Δ'),
        ('\\pi', 'π'), ('\\sigma', 'σ'), ('\\omega', 'ω'), ('\\alpha', 'α'), ('\\beta', 'β'), ('\\gamma', 'γ'),
        ('\\cdot', '·'), ('\\times', '×'), ('\\leq', '≤'), ('\\geq', '≥'), ('\\approx', '≈'), ('\\infty', '∞')]
def tex_plain(tex):
    s = html.unescape(tex)
    s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)
    s = re.sub(r'\\text\{([^{}]*)\}', r'\1', s)
    for a, b in _TEX:
        s = s.replace(a, b)
    s = s.replace('\\,', ' ').replace('{', '').replace('}', '')
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    s = re.sub(r'\(([A-Za-z0-9]+)\)/\(([A-Za-z0-9]+)\)', r'\1/\2', s)
    return re.sub(r'\s+', ' ', s).strip()

def eq_patch(s):
    if 'crs-eq' not in s:
        return s
    def repl(m):
        fig = m.group(0)
        if 'crs-eqtext' in fig:
            return fig
        ann = re.search(r'encoding="application/x-tex">(.*?)</annotation>', fig)
        if not ann:
            return fig
        plain = html.escape(tex_plain(ann.group(1)))
        return fig.replace('<figcaption>', f'<p class="crs-eqtext" dir="ltr">{plain}</p><figcaption>', 1)
    return re.sub(r'<figure class="crs-eq">.*?</figure>', repl, s, flags=re.S)

n = 0
for f in sorted(glob.glob('*.html') + glob.glob('[a-z][a-z]/*.html')):
    if os.path.basename(f).startswith('google'):
        continue
    s = open(f, encoding='utf8').read()
    o = s
    lang = lang_of(f)
    page = os.path.basename(f)
    s = patch_credits(s, lang)
    s = swap_astro(s)
    if page in ('Deforestation.html',):
        s = swap_gedi_hub(s)
    if page in ('Earth_Observation.html',):
        s = swap_alos_hub(s)
    if page == 'Solutions.html':
        s = swap_eden_sol(s)
        s = swap_just_sol(s)
    if page == 'index.html':
        # domain card for Astroscale follows the hero photo (ADRAS-J, not the servicing-arm lab)
        s = s.replace('Satellite_Servicing_Arm_GSFC.jpg', 'Astroscale_ADRAS-J_H-IIA_Stage.jpg')
        s = homepage_webp(s, lang)
    if 'data-course=' in s or page == 'Courses.html':
        s = course_patch(s, lang, page)
        s = eq_patch(s)
    # i18n brand key is not on the page; nothing to do here
    if s != o:
        open(f, 'w', encoding='utf8').write(s)
        n += 1
print('patched html files', n)

# Old brand phrase in translation memory cannot republish "Saving Our Planet".
for lang, path in [('fr', 'i18n/fr.json'), ('es', 'i18n/es.json'), ('ar', 'i18n/ar.json'), ('it', 'i18n/it.json'), ('he', 'i18n/he.json')]:
    m = json.load(open(path, encoding='utf8'))
    if m.get('Saving Our Planet') and m['Saving Our Planet'] != 'Saving Planets':
        m['Saving Our Planet'] = 'Saving Planets'
        json.dump(m, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
        print('brand key', path)
print('fix-assessor-trust done')
