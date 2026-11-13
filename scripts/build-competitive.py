#!/usr/bin/env python3
"""Nine recommendations approved by the site owner on Nov 8, 2026.
Idempotent. Touches en/fr/es/ar/it/he. Does not invent ratings, gift math, or partner totals.
Run from the repo root: python3 scripts/build-competitive.py
"""
import html, json, os, re, glob
from datetime import date
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
E = lambda s: html.escape(s if s is not None else '', quote=True)
TODAY = '2026-11-09'

def pre(lang):
    return '' if lang == 'en' else '../'

def help_kind(url):
    u = url or ''
    if re.search(r'career|/(jobs|employ)(/|$|\.)|recruiting/jobs', u, re.I):
        return 'careers'
    if re.search(r'/(contact|inquiries|enquiry)(/|$|\.)|contact\.html|contact-us|contact-2', u, re.I):
        return 'contact'
    return 'volunteer' if u else 'none'

# UI strings. Org quotations stay in the organization's words.
UI = {
 'en': dict(
    h1='<h1 class="hero-welcome"><span class="welcome-brand">Saving Planets</span> <span class="welcome-minus">from the ocean floor to orbit</span></h1>',
    sub='Every working fix for the planet — checked for you, explained for kids, and one click from helping.',
    desc='Free STEM courses, teacher tools, and planet-health solutions, from the ocean floor to orbit — checked for you, explained for kids, and one click from helping.',
    title='From the ocean floor to orbit: free STEM courses and teacher tools | Saving Planets',
    match='Match me to a solution',
    how='How we check a Donate link',
    don='Donate', vol='Volunteer', learn='Learn', car='Careers', con='Contact',
    vol_words=('Volunteer', 'Join the work', 'Offer to Help'),
    don_re=r'Donate',
    one_kicker='This week, one action',
    note_don='Opens the organization\'s donation page. Saving Planets does not receive the money.',
    note_cs='Opens NASA citizen science. This is not a donation.',
    note_learn='Opens the solution page on Saving Planets.',
    where='Where', any='Any place', remote='From home', local='At a place',
    where_note='A place is listed only when we have one. Other rows stay under Any place.',
    citsci_h='Official citizen science',
    citsci_p='ESA, JAXA and some other agencies do not publish a public volunteer sign-up. A button says Careers or Contact when that is the real page. These official projects are actions you can take:',
    open='Open the official page',
    gift_h='What a gift does',
    gift_p='A number appears only when that organization publishes it. We do not turn it into a price they did not state.',
    claimed='Claimed by',
    read_on='Saving Planets read this sentence on the organization\'s page on November 9, 2026.',
    adopt_link='Adopt a solution for your class',
    wth_match='Not sure where to start?',
 ),
 'fr': dict(
    h1='<h1 class="hero-welcome"><span class="welcome-brand">Saving Planets</span> <span class="welcome-minus">du plancher océanique à l\'orbite</span></h1>',
    sub='Chaque solution qui marche pour la planète — vérifiée pour vous, expliquée aux enfants, et à un clic d\'aider.',
    desc='Cours STEM gratuits, outils pour les enseignants et solutions pour la santé de la planète, du plancher océanique à l\'orbite — vérifiée pour vous, expliquée aux enfants, et à un clic d\'aider.',
    title='Du plancher océanique à l\'orbite : cours STEM gratuits et outils enseignants | Saving Planets',
    match='Trouvez-moi une solution',
    how='Comment nous vérifions un lien Don',
    don='Faire un don', vol='Bénévolat', learn='Apprendre', car='Carrières', con='Contact',
    vol_words=('Bénévolat', 'Rejoindre le mouvement', 'Offer to Help', 'Devenir bénévole'),
    don_re=r'Faire un don|Don\b',
    one_kicker='Cette semaine, une action',
    note_don='Ouvre la page de don de l\'organisation. Saving Planets ne reçoit pas l\'argent.',
    note_cs='Ouvre la science participative de la NASA. Ce n\'est pas un don.',
    note_learn='Ouvre la page de la solution sur Saving Planets.',
    where='Lieu', any='Tous les lieux', remote='Depuis chez vous', local='Sur un lieu',
    where_note='Un lieu n\'est indiqué que lorsque nous en avons un. Les autres lignes restent sous Tous les lieux.',
    citsci_h='Science participative officielle',
    citsci_p='L\'ESA, la JAXA et d\'autres agences ne publient pas d\'inscription bénévole pour le public. Le bouton dit Carrières ou Contact lorsque c\'est la vraie page. Ces projets officiels sont de vraies actions :',
    open='Ouvrir la page officielle',
    gift_h='Ce que fait un don',
    gift_p='Un chiffre n\'apparaît que si l\'organisation le publie. Nous ne le transformons pas en prix qu\'elle n\'a pas écrit.',
    claimed='Selon',
    read_on='Saving Planets a lu cette phrase sur la page de l\'organisation le 9 novembre 2026.',
    adopt_link='Adopter une solution avec la classe',
    wth_match='Vous ne savez pas par où commencer ?',
 ),
 'es': dict(
    h1='<h1 class="hero-welcome"><span class="welcome-brand">Saving Planets</span> <span class="welcome-minus">del fondo del océano a la órbita</span></h1>',
    sub='Cada arreglo que funciona para el planeta — revisado para ti, explicado para niños y a un clic de ayudar.',
    desc='Cursos STEM gratuitos, herramientas para docentes y soluciones para la salud del planeta, del fondo del océano a la órbita — revisado para ti, explicado para niños y a un clic de ayudar.',
    title='Del fondo del océano a la órbita: cursos STEM gratis y herramientas docentes | Saving Planets',
    match='Encuéntrame una solución',
    how='Cómo comprobamos un enlace de donación',
    don='Donar', vol='Voluntariado', learn='Aprender', car='Empleo', con='Contacto',
    vol_words=('Voluntariado', 'Únete al trabajo', 'Offer to Help', 'Hazte voluntario'),
    don_re=r'Donar',
    one_kicker='Esta semana, una acción',
    note_don='Abre la página de donación de la organización. Saving Planets no recibe el dinero.',
    note_cs='Abre la ciencia ciudadana de la NASA. No es una donación.',
    note_learn='Abre la página de la solución en Saving Planets.',
    where='Lugar', any='Cualquier lugar', remote='Desde casa', local='En un lugar',
    where_note='Solo mostramos un lugar cuando lo tenemos. Las demás filas siguen en Cualquier lugar.',
    citsci_h='Ciencia ciudadana oficial',
    citsci_p='La ESA, la JAXA y otras agencias no publican un alta de voluntariado para el público. El botón dice Empleo o Contacto cuando esa es la página real. Estos proyectos oficiales sí son acciones:',
    open='Abrir la página oficial',
    gift_h='Qué hace un regalo',
    gift_p='Un número aparece solo si la organización lo publica. No lo convertimos en un precio que ella no escribió.',
    claimed='Lo afirma',
    read_on='Saving Planets leyó esta frase en la página de la organización el 9 de noviembre de 2026.',
    adopt_link='Adopta una solución con tu clase',
    wth_match='¿No sabes por dónde empezar?',
 ),
 'ar': dict(
    h1='<h1 class="hero-welcome"><span class="welcome-brand">Saving Planets</span> <span class="welcome-minus">من قاع المحيط إلى المدار</span></h1>',
    sub='كل حل يعمل من أجل الكوكب — نراجعه لك، ونشرحه للأطفال، وبضغطة واحدة يمكن المساعدة.',
    desc='مقررات STEM مجانية، وأدوات للمعلمين، وحلول لصحة الكوكب، من قاع المحيط إلى المدار — نراجعها لك، ونشرحها للأطفال، وبضغطة واحدة يمكن المساعدة.',
    title='من قاع المحيط إلى المدار: مقررات STEM مجانية وأدوات للمعلمين | Saving Planets',
    match='طابقني مع حل',
    how='كيف نتحقق من رابط التبرع',
    don='تبرّع', vol='تطوّع', learn='تعلّم', car='وظائف', con='تواصل',
    vol_words=('تطوّع', 'انضم إلى العمل', 'Offer to Help'),
    don_re=r'تبرّع',
    one_kicker='هذا الأسبوع، فعل واحد',
    note_don='يفتح صفحة التبرع الخاصة بالمنظمة. لا تتلقى Saving Planets المال.',
    note_cs='يفتح علوم المواطن في ناسا. هذا ليس تبرعًا.',
    note_learn='يفتح صفحة الحل على Saving Planets.',
    where='المكان', any='أي مكان', remote='من المنزل', local='في مكان',
    where_note='نذكر المكان فقط عندما نعرفه. بقية الصفوف تبقى تحت أي مكان.',
    citsci_h='علوم مواطن رسمية',
    citsci_p='لا تنشر وكالة الفضاء الأوروبية ولا جاكسا وغيرهما صفحة تطوع عامة. يقول الزر «وظائف» أو «تواصل» عندما تكون تلك هي الصفحة الحقيقية. هذه مشاريع رسمية يمكن المشاركة فيها:',
    open='افتح الصفحة الرسمية',
    gift_h='ماذا تفعل الهدية',
    gift_p='لا يظهر رقم إلا إذا نشرته المنظمة. لا نحوّله إلى سعر لم تكتبه.',
    claimed='حسب قول',
    read_on='قرأت Saving Planets هذه الجملة في صفحة المنظمة في 9 نوفمبر 2026.',
    adopt_link='تبنَّ حلًا مع صفك',
    wth_match='لا تعرف من أين تبدأ؟',
 ),
 'it': dict(
    h1='<h1 class="hero-welcome"><span class="welcome-brand">Saving Planets</span> <span class="welcome-minus">dal fondo dell\'oceano all\'orbita</span></h1>',
    sub='Ogni soluzione che funziona per il pianeta — controllata per te, spiegata ai bambini e a un clic dall\'aiutare.',
    desc='Corsi STEM gratuiti, strumenti per i docenti e soluzioni per la salute del pianeta, dal fondo dell\'oceano all\'orbita — controllata per te, spiegata ai bambini e a un clic dall\'aiutare.',
    title='Dal fondo dell\'oceano all\'orbita: corsi STEM gratuiti e strumenti per docenti | Saving Planets',
    match='Abbinami a una soluzione',
    how='Come controlliamo un link per donare',
    don='Dona', vol='Volontariato', learn='Impara', car='Carriere', con='Contatti',
    vol_words=('Volontariato', 'Unisciti a loro', 'Offer to Help', 'Fai volontariato'),
    don_re=r'\bDona\b',
    one_kicker='Questa settimana, un\'azione',
    note_don='Apre la pagina di donazione dell\'organizzazione. Saving Planets non riceve il denaro.',
    note_cs='Apre la citizen science della NASA. Non è una donazione.',
    note_learn='Apre la pagina della soluzione su Saving Planets.',
    where='Luogo', any='Qualsiasi luogo', remote='Da casa', local='In un luogo',
    where_note='Indichiamo un luogo solo quando ne abbiamo uno. Le altre righe restano sotto Qualsiasi luogo.',
    citsci_h='Citizen science ufficiale',
    citsci_p='ESA, JAXA e altre agenzie non pubblicano un\'iscrizione di volontariato per il pubblico. Il pulsante dice Carriere o Contatti quando quella è la pagina vera. Questi progetti ufficiali sono azioni possibili:',
    open='Apri la pagina ufficiale',
    gift_h='Che cosa fa un dono',
    gift_p='Un numero compare solo se lo pubblica l\'organizzazione. Non lo trasformiamo in un prezzo che non ha scritto.',
    claimed='Lo dichiara',
    read_on='Saving Planets ha letto questa frase sulla pagina dell\'organizzazione il 9 novembre 2026.',
    adopt_link='Adotta una soluzione con la classe',
    wth_match='Non sai da dove iniziare?',
 ),
 'he': dict(
    h1='<h1 class="hero-welcome"><span class="welcome-brand">Saving Planets</span> <span class="welcome-minus">מקרקעית האוקיינוס עד למסלול</span></h1>',
    sub='כל תיקון שעובד לכדור הארץ — נבדק עבורכם, מוסבר לילדים, ובמרחק לחיצה אחת מעזרה.',
    desc='קורסי STEM חינמיים, כלי מורים ופתרונות לבריאות כדור הארץ, מקרקעית האוקיינוס עד למסלול — נבדק עבורכם, מוסבר לילדים, ובמרחק לחיצה אחת מעזרה.',
    title='מקרקעית האוקיינוס עד למסלול: קורסי STEM חינמיים וכלי מורים | Saving Planets',
    match='התאימו לי פתרון',
    how='איך אנחנו בודקים קישור תרומה',
    don='לתרומה', vol='להתנדבות', learn='ללמוד', car='קריירה', con='יצירת קשר',
    vol_words=('להתנדבות', 'הצטרפו לעבודה', 'Offer to Help', 'Volunteer'),
    don_re=r'לתרומה|תרומה',
    one_kicker='השבוע, פעולה אחת',
    note_don='נפתח עמוד התרומה של הארגון. Saving Planets אינה מקבלת את הכסף.',
    note_cs='נפתח המדע האזרחי של נאס״א. זו אינה תרומה.',
    note_learn='נפתח עמוד הפתרון ב-Saving Planets.',
    where='מקום', any='כל מקום', remote='מהבית', local='במקום',
    where_note='מקום מופיע רק כשיש לנו אחד. שאר השורות נשארות תחת כל מקום.',
    citsci_h='מדע אזרחי רשמי',
    citsci_p='ל-ESA, ל-JAXA ולסוכנויות אחרות אין לעיתים דף התנדבות לציבור. הכפתור אומר קריירה או יצירת קשר כשזה הדף האמיתי. אלה פרויקטים רשמיים שאפשר להצטרף אליהם:',
    open='פתיחת הדף הרשמי',
    gift_h='מה מתנה עושה',
    gift_p='מספר מופיע רק אם הארגון פרסם אותו. אנחנו לא הופכים אותו למחיר שהארגון לא כתב.',
    claimed='לפי',
    read_on='Saving Planets קראה את המשפט הזה בדף הארגון ב-9 בנובמבר 2026.',
    adopt_link='אמצו פתרון עם הכיתה',
    wth_match='לא בטוחים מאיפה להתחיל?',
 ),
}

GIFTS = json.load(open('assets/data/gift-claims.json', encoding='utf8'))
CITSCI = json.load(open('assets/data/citizen-science.json', encoding='utf8'))['actions']
WHERE = {a['href']: a['where'] for a in CITSCI}

def where_of(url):
    for href, w in WHERE.items():
        if url.startswith(href.rstrip('/')) or href.rstrip('/') in url:
            return w
    return ''

def plain(fragment):
    t = re.sub(r'<[^>]+>', ' ', fragment)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()

POLICY = re.compile(r'go only|van sólo|vanno solo|uniquement|فقط إلى المنظمات|רק לארגונים', re.I)
RATING = re.compile(r'Charity Navigator|Charity Commission|Four-Star|cuatro estrellas|quattro stelle|quatre étoiles|audited financial|bilancio|estados financieros|ארבע|أربع', re.I)

def basis_of(page_html):
    chunks = re.findall(r'<p[^>]*class="[^"]*help-note[^"]*"[^>]*>(.*?)</p>', page_html, re.S)
    if not any(RATING.search(plain(c)) for c in chunks):
        chunks += re.findall(r'<p[^>]*>(.*?)</p>', page_html, re.S)
    for c in chunks:
        text = plain(c)
        if not RATING.search(text):
            continue
        parts = re.split(r'(?<=[.!?])\s+', text)
        kept = [p for p in parts if RATING.search(p) and not POLICY.search(p)]
        if kept:
            sentence = kept[0].strip()
            return sentence[:420]
    return ''

def reviewed_bits(page_html, solution_href):
    m = re.search(r'<p class="page-reviewed".*?</p>', page_html, re.S)
    if not m:
        return '', ''
    block = m.group(0)
    tm = re.search(r'<time[^>]*>.*?</time>', block, re.S)
    lab = re.search(r'<span class="rv-label">(.*?)</span>', block, re.S)
    src = re.search(r'<a href="#solution"[^>]*>(.*?)</a>', block, re.S)
    date = ''
    if tm:
        label = plain(lab.group(1)) if lab else 'Last reviewed:'
        date = f'<span class="vet-rev">{E(label)} {tm.group(0)}</span>'
    sources = ''
    if src:
        href = solution_href or '#solution'
        sources = f'<a href="{E(href)}">{src.group(1)}</a>'
    return date, sources

_PAGE_CACHE = {}
def read(path):
    if path not in _PAGE_CACHE:
        _PAGE_CACHE[path] = open(path, encoding='utf8').read() if os.path.exists(path) else ''
    return _PAGE_CACHE[path]

def write(path, text):
    _PAGE_CACHE[path] = text
    if not os.path.exists(path) or open(path, encoding='utf8').read() != text:
        open(path, 'w', encoding='utf8').write(text)
        return 1
    return 0

def vet_html(page_path, lang, solution_href):
    u = UI[lang]
    src = read(page_path) if page_path else ''
    bits = []
    b = basis_of(src) if src else ''
    if b:
        bits.append(f'<span class="vet-basis">{E(b)}</span>')
    date, sources = reviewed_bits(src, solution_href) if src else ('', '')
    if date:
        bits.append(date)
    if sources:
        bits.append(sources)
    bits.append(f'<a class="vet-how" href="{pre(lang)}How_We_Evaluate.html#s3">{E(u["how"])}</a>')
    return '<p class="vet-line">' + ' <span aria-hidden="true">·</span> '.join(bits) + '</p>'

def is_donate_text(text, lang):
    return re.search(UI[lang]['don_re'], plain(text)) is not None

def relabel_buttons(src, lang):
    u = UI[lang]
    def repl(m):
        kind = help_kind(m.group('href'))
        if kind not in ('careers', 'contact'):
            return m.group(0)
        text = m.group('text')
        if text.strip() not in u['vol_words']:
            return m.group(0)
        word = u['car'] if kind == 'careers' else u['con']
        return m.group(0).replace('>' + text + '<', '>' + word + '<', 1)
    return re.sub(r'<a class="btn help-btn[^"]*" href="(?P<href>[^"]+)"[^>]*>(?P<text>[^<]+)<', repl, src)

def patch_help_sections(src, lang, page_path):
    src = re.sub(r'<!-- VETLINE:START -->.*?<!-- VETLINE:END -->', '', src, flags=re.S)
    line = '<!-- VETLINE:START -->' + vet_html(page_path, lang, '#solution') + '<!-- VETLINE:END -->'
    def repl(m):
        if not is_donate_text(m.group(0), lang):
            return m.group(0)
        return m.group(0) + line
    return re.sub(r'<div class="help-btns">.*?</div>', repl, src, flags=re.S)

def gift_block(lang, claims):
    u = UI[lang]
    cards = []
    for c in claims:
        cards.append(
            '<article class="sp9-gift"><h3>' + E(u['gift_h'] if c['heading'].startswith('What') else c['heading']) + '</h3>'
            '<blockquote><p>' + E(c['quote']) + '</p></blockquote>'
            '<p class="sp9-claimed">' + E(u['claimed']) + ' ' + E(c['org']) + '. '
            '<a href="' + E(c['source']) + '" target="_blank" rel="noopener">' + E(c['sourceName']) + '</a></p>'
            '<p class="sp9-read">' + E(u['read_on']) + '</p></article>'
        )
    # heading: use the claim's own heading translated only for the section; card h3 uses a mapped heading
    return cards

HEADING = {
 'en': {'What $10 a month does': 'What $10 a month does', 'What one bracelet does': 'What one bracelet does', 'What one dollar does': 'What one dollar does'},
 'fr': {'What $10 a month does': 'Ce que font 10 $ par mois', 'What one bracelet does': 'Ce que fait un bracelet', 'What one dollar does': 'Ce que fait un dollar'},
 'es': {'What $10 a month does': 'Qué hacen 10 $ al mes', 'What one bracelet does': 'Qué hace una pulsera', 'What one dollar does': 'Qué hace un dólar'},
 'ar': {'What $10 a month does': 'ماذا تفعل 10 دولارات في الشهر', 'What one bracelet does': 'ماذا يفعل سوار واحد', 'What one dollar does': 'ماذا يفعل دولار واحد'},
 'it': {'What $10 a month does': 'Che cosa fanno 10 $ al mese', 'What one bracelet does': 'Che cosa fa un braccialetto', 'What one dollar does': 'Che cosa fa un dollaro'},
 'he': {'What $10 a month does': 'מה עושים 10 דולר בחודש', 'What one bracelet does': 'מה עושה צמיד אחד', 'What one dollar does': 'מה עושה דולר אחד'},
}

def gift_html(lang, claims):
    u = UI[lang]
    cards = []
    for c in claims:
        h = HEADING[lang].get(c['heading'], c['heading'])
        cards.append(
            '<article class="sp9-gift"><h3>' + E(h) + '</h3>'
            '<blockquote cite="' + E(c['source']) + '"><p>' + E(c['quote']) + '</p></blockquote>'
            '<p class="sp9-claimed">' + E(u['claimed']) + ' ' + E(c['org']) + '. '
            '<a href="' + E(c['source']) + '" target="_blank" rel="noopener">' + E(c['sourceName']) + '</a></p>'
            '<p class="sp9-read">' + E(u['read_on']) + '</p></article>'
        )
    return '<!-- GIFT:START --><section class="sp9-gifts" id="what-a-gift-does" aria-labelledby="gift-h"><h2 id="gift-h">' + E(u['gift_h']) + '</h2><p>' + E(u['gift_p']) + '</p>' + ''.join(cards) + '</section><!-- GIFT:END -->'

def gift_details_html(lang, claims):
    """Ways to Help only: same gift copy, collapsed <details> instead of an always-open section."""
    block = gift_html(lang, claims)
    block = block.replace(
        '<section class="sp9-gifts" id="what-a-gift-does" aria-labelledby="gift-h"><h2 id="gift-h">',
        '<details class="sp9-gifts" id="what-a-gift-does"><summary id="gift-h">', 1)
    block = block.replace('</h2>', '</summary>', 1)
    return block.replace('</section><!-- GIFT:END -->', '</details><!-- GIFT:END -->', 1)

def upsert(src, name, inner):
    pat = re.compile(r'<!-- %s:START -->.*?<!-- %s:END -->' % (name, name), re.S)
    block = '<!-- %s:START -->%s<!-- %s:END -->' % (name, inner, name)
    if pat.search(src):
        return pat.sub(lambda m: block, src, count=1)
    return None

def citsci_cards(lang):
    u = UI[lang]
    out = []
    for a in CITSCI:
        out.append(
            '<li class="wh-card sp9-citsci" id="citsci-' + re.sub(r'[^a-z]+', '-', a['name'].lower()).strip('-') + '" data-where="' + a['where'] + '">'
            '<h3>' + E(a['name']) + '</h3><p>' + E(a['quote']) + '</p>'
            '<a class="btn help-btn" href="' + E(a['href']) + '" target="_blank" rel="noopener">' + E(u['open']) +
            '<span class="sr-only"> – ' + E(a['name']) + '</span></a></li>'
        )
    return ''.join(out)

def patch_wth(path, lang):
    src = read(path)
    u = UI[lang]
    src = relabel_buttons(src, lang)
    src = re.sub(r'<!-- GIFT:START -->.*?<!-- GIFT:END -->', '', src, flags=re.S)
    src = re.sub(r'<!-- WHWHERE:START -->.*?<!-- WHWHERE:END -->', '', src, flags=re.S)
    src = re.sub(r'<!-- CITSCI:START -->.*?<!-- CITSCI:END -->', '', src, flags=re.S)
    src = re.sub(r'<p class="sp9-citsci-note">.*?</p>', '', src, flags=re.S)
    gift = gift_details_html(lang, list(GIFTS['claims']))
    if '<p class="wh-jump">' in src:
        src = re.sub(r'(<p class="wh-jump">.*?</p>)', r'\1' + gift, src, count=1, flags=re.S)
    elif 'class="wh-intro"' in src:
        src = re.sub(r'(<p class="wh-intro">.*?</p>)', r'\1' + gift, src, count=1, flags=re.S)
    filt = ('<!-- WHWHERE:START --><div class="sp9-where" id="wh-where"><div role="group" aria-labelledby="wh-where-l">'
            '<span id="wh-where-l">' + E(u['where']) + '</span>'
            '<button type="button" data-where="any" aria-pressed="true">' + E(u['any']) + '</button>'
            '<button type="button" data-where="remote" aria-pressed="false">' + E(u['remote']) + '</button>'
            '<button type="button" data-where="local" aria-pressed="false">' + E(u['local']) + '</button></div>'
            '<p>' + E(u['where_note']) + '</p></div><!-- WHWHERE:END -->')
    src = re.sub(r'(id="roll-up-your-sleeves".*?<p class="wh-sub">.*?</p>)', r'\1' + filt, src, count=1, flags=re.S)
    cards = '<!-- CITSCI:START -->' + citsci_cards(lang) + '<!-- CITSCI:END -->'
    src = src.replace('id="vol-hub-earth-observation"', 'id="vol-hub-earth-observation"', 1)
    src = re.sub(r'(id="vol-hub-earth-observation"[^>]*>.*?<ul class="wh-grid">)', r'\1' + cards, src, count=1, flags=re.S)
    note = '<p class="sp9-citsci-note">' + E(u['citsci_p']) + '</p>'
    if 'sp9-citsci-note' not in src:
        src = re.sub(r'(id="vol-hub-earth-observation"[^>]*>\s*<summary>.*?</summary>)', r'\1' + note, src, count=1, flags=re.S)
    def one_card(m):
        card = m.group(0)
        hrefs = re.findall(r'href="(https?://[^"]+)"', card)
        w = ''
        for h in hrefs:
            w = where_of(h) or w
        if w and 'data-where=' not in card[:80]:
            card = card.replace('<li class="wh-card"', '<li class="wh-card" data-where="%s"' % w, 1)
        sh = re.search(r'class="wh-s" href="([^"]+\.html)"', card)
        if sh and 'vet-line' not in card:
            page = sh.group(1).split('/')[-1]
            folder = '' if lang == 'en' else lang + '/'
            line = vet_html(folder + page, lang, page + '#solution')
            def add(bm):
                if not is_donate_text(bm.group(0), lang):
                    return bm.group(0)
                return bm.group(0) + line
            card = re.sub(r'<a class="btn help-btn[^"]*"[^>]*>.*?</a>', add, card, count=1, flags=re.S)
        return card
    src = re.sub(r'<li class="wh-card"(?: data-where="[^"]*")?>.*?</li>', one_card, src, flags=re.S)
    if 'id="wh-where-js"' not in src:
        src = src.replace('</body>', WHERE_JS + '</body>', 1)
    match = '<p class="sp9-match"><a href="Match.html">' + E(u['wth_match']) + ' ' + E(u['match']) + '</a></p>'
    if 'href="Match.html"' not in src:
        if '<!-- GIFT:END -->' in src:
            src = src.replace('<!-- GIFT:END -->', '<!-- GIFT:END -->' + match, 1)
        else:
            src = re.sub(r'(<p class="wh-jump">.*?</p>|<p class="wh-intro">.*?</p>)', r'\1' + match, src, count=1, flags=re.S)
    return src

WHERE_JS = '''<script id="wh-where-js">(function(){var bar=document.getElementById("wh-where");var sec=document.getElementById("roll-up-your-sleeves");if(!bar||!sec)return;
var cards=[].slice.call(sec.querySelectorAll(".wh-card"));var where="any";
function run(){cards.forEach(function(c){var w=c.getAttribute("data-where")||"";c.classList.toggle("sp9-where-off",where!=="any"&&w!==where);});
[].forEach.call(sec.querySelectorAll(".wh-hub"),function(h){var on=[].some.call(h.querySelectorAll(".wh-card"),function(c){return !c.hidden&&!c.classList.contains("sp9-where-off");});if(where!=="any")h.open=on;});}
bar.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;where=b.getAttribute("data-where");[].forEach.call(bar.querySelectorAll("button"),function(x){x.setAttribute("aria-pressed",x===b?"true":"false");});run();});})();</script>'''

def note_for(lang, action):
    u = UI[lang]
    n = action.get('note') or ''
    if 'citizen science' in n.lower() or 'NASA' in n:
        return u['note_cs']
    if action.get('kind') == 'donate':
        return u['note_don']
    if action.get('kind') == 'learn':
        return u['note_learn']
    return u['note_don'] if action.get('kind') == 'donate' else u['note_cs'] if action.get('kind') == 'volunteer' else u['note_learn']

def action_button(lang, action):
    u = UI[lang]
    label = {'donate': u['don'], 'volunteer': u['vol'], 'learn': u['learn']}[action['kind']]
    ext = ' target="_blank" rel="noopener"' if action['href'].startswith('http') else ''
    return ('<a class="btn" href="%s"%s>%s</a><span class="sp9-actnote">%s</span>' % (E(action['href']), ext, E(label), E(note_for(lang, action))))

def patch_index(path, lang):
    src = read(path)
    u = UI[lang]
    src = re.sub(r'<h1 class="hero-welcome">.*?</h1>\s*<p class="hero-example">.*?</p>',
                 u['h1'] + '<p class="hero-example">' + E(u['sub']) + '</p>', src, count=1, flags=re.S)
    src = re.sub(r'<title>[^<]*</title>', '<title>' + E(u['title']) + '</title>', src, count=1)
    for attr, key in (('name', 'description'), ('property', 'og:description'), ('name', 'twitter:description'),
                      ('property', 'og:title'), ('name', 'twitter:title')):
        val = u['desc'] if 'description' in key else u['title']
        src = re.sub(r'(<meta %s="%s" content=")[^"]*"' % (attr, key), r'\1' + E(val) + '"', src, count=1)
    if 'href="Match.html"' not in src.split('id="newsletter"')[0]:
        src = src.replace('</p><!-- HERO-CTA:END -->', '<a class="btn hero-cta" href="Match.html">' + E(u['match']) + '</a></p><!-- HERO-CTA:END -->', 1)
    sw = json.load(open('assets/data/solution-of-week.json', encoding='utf8'))
    m = re.search(r'data-sotw-page="([^"]+)"', src)
    page = m.group(1) if m else sw['rotation'][0]['page']
    action = next((e['action'] for e in sw['rotation'] if e['page'] == page and e.get('action')), None)
    if not action:
        action = {'kind': 'learn', 'href': page, 'note': ''}
    btn = action_button(lang, action)
    src = re.sub(r'<p class="sotw-actions">.*?</p>\s*(?:<p class="sotw-note">.*?</p>)?',
                 '<p class="sotw-actions">' + btn + '</p>', src, count=1, flags=re.S)
    block = ('<section class="sp9-one" id="one-action" aria-labelledby="one-action-h"><p class="sotw-kicker">' + E(u['one_kicker']) + '</p>'
             '<h2 id="one-action-h"><a href="' + E(page) + '">' + E(page.replace('.html', '').replace('_', ' ')) + '</a></h2>'
             '<p class="sotw-actions">' + btn + '</p></section>')
    # Prefer the visible title already in the sotw card
    tm = re.search(r'id="sotw-title"><a[^>]*>(.*?)</a>', src, re.S)
    if tm:
        block = block.replace(E(page.replace('.html', '').replace('_', ' ')), tm.group(1), 1)
    src = re.sub(r'<!-- ONEACTION:START -->.*?<!-- ONEACTION:END -->', '', src, flags=re.S)
    src = src.replace('<section id="newsletter"', '<!-- ONEACTION:START -->' + block + '<!-- ONEACTION:END --><section id="newsletter"', 1)
    if 'id="newsletter"' in src and 'ONEACTION:START' not in src:
        src = re.sub(r'(<section[^>]*id="newsletter")', '<!-- ONEACTION:START -->' + block + '<!-- ONEACTION:END -->' + r'\1', src, count=1)
    return src

def patch_adopt_links(path, lang):
    src = read(path)
    u = UI[lang]
    block = '<p class="sp9-adopt"><a class="btn" href="Adopt_a_Solution.html">' + E(u['adopt_link']) + '</a></p>'
    src = re.sub(r'<!-- ADOPTLINK:START -->.*?<!-- ADOPTLINK:END -->', '', src, flags=re.S)
    src = re.sub(r'(<section class="page-hero hero-teach">.*?</section>)',
                 r'\1<!-- ADOPTLINK:START -->' + block + '<!-- ADOPTLINK:END -->', src, count=1, flags=re.S)
    return src

def patch_eo(path, lang):
    src = read(path)
    u = UI[lang]
    items = ''.join('<li><a href="%s" target="_blank" rel="noopener">%s</a> — %s <span class="sp9-tag">%s</span></li>' % (
        E(a['href']), E(a['name']), E(a['quote']), E(UI[lang]['remote'] if a['where'] == 'remote' else UI[lang]['local'])) for a in CITSCI)
    block = ('<section class="five-ws" id="citizen-science"><h2>' + E(u['citsci_h']) + '</h2><p>' + E(u['citsci_p']) + '</p><ul>' + items + '</ul></section>')
    src = re.sub(r'<!-- CITSCI-HUB:START -->.*?<!-- CITSCI-HUB:END -->', '', src, flags=re.S)
    src = src.replace('<footer', '<!-- CITSCI-HUB:START -->' + block + '<!-- CITSCI-HUB:END --><footer', 1)
    return src

def gift_on_solution(path, lang):
    base = os.path.basename(path)
    claims = [c for c in GIFTS['claims'] if c['page'] == base]
    if not claims:
        return read(path)
    src = re.sub(r'<!-- GIFT:START -->.*?<!-- GIFT:END -->', '', read(path), flags=re.S)
    block = gift_html(lang, claims)
    if re.search(r'<section[^>]*class="[^"]*help-actions', src):
        return re.sub(r'(<section[^>]*class="[^"]*help-actions)', block + r'\1', src, count=1)
    return src.replace('</main>', block + '</main>', 1) if '</main>' in src else src

# ---------- new pages ----------
MATCH_COPY = {
 'en': dict(title='Match me to a solution', desc='Four questions lead to three Saving Planets solutions. Nothing you answer is saved.',
            h='Match me to a solution', lead='Four questions. Three ideas from the solutions already on this site. We do not save what you pick.',
            q1='Which cause?', q2='How do you want to help?', q3='Where?', q4='Who is this for?',
            ocean='Ocean', rivers='Rivers and lakes', forests='Forests', polar='Polar', earth='Earth from orbit', space='Space',
            money='Give money', time='Give time', learn='Learn', near='Near a place the work happens', remote='From home',
            kid='A kid (kindergarten through grade 5)', adult='An adult',
            go='Show three ideas', priv='We do not ask for a name, a school, or a location, and we do not save these answers.',
            out='Three ideas', exact='These three match all four answers.',
            relaxed='Fewer than three matched the place you picked, so these include a wider set. Same cause and same kind of help.',
            short='Fewer than three solutions matched. We are not adding any that do not fit.',
            none='No solution on this site matches these answers.',
            why_near='The solution page names a place.', why_remote='You can do this without traveling to a worksite.',
            kid_empty='No kindergarten-to-grade-5 page in this cause matches. We did not fill the list with older pages.'),
 'fr': dict(title='Trouvez-moi une solution', desc='Quatre questions mènent à trois solutions Saving Planets. Rien de ce que vous répondez n\'est enregistré.',
            h='Trouvez-moi une solution', lead='Quatre questions. Trois idées parmi les solutions déjà sur ce site. Nous n\'enregistrons pas vos choix.',
            q1='Quelle cause ?', q2='Comment voulez-vous aider ?', q3='Où ?', q4='Pour qui ?',
            ocean='Océan', rivers='Rivières et lacs', forests='Forêts', polar='Pôles', earth='La Terre depuis l\'orbite', space='Espace',
            money='Donner de l\'argent', time='Donner du temps', learn='Apprendre', near='Près d\'un lieu où le travail se fait', remote='Depuis chez vous',
            kid='Un enfant (maternelle au CM2)', adult='Un adulte',
            go='Voir trois idées', priv='Nous ne demandons ni nom, ni école, ni lieu, et nous n\'enregistrons pas ces réponses.',
            out='Trois idées', exact='Ces trois répondent aux quatre questions.',
            relaxed='Moins de trois correspondaient au lieu choisi, donc la liste est un peu plus large. Même cause, même type d\'aide.',
            short='Moins de trois solutions correspondent. Nous n\'en ajoutons pas qui ne conviennent pas.',
            none='Aucune solution de ce site ne correspond.',
            why_near='La page de la solution nomme un lieu.', why_remote='On peut le faire sans se rendre sur un chantier.',
            kid_empty='Aucune page de la maternelle au CM2 ne correspond à cette cause. Nous n\'avons pas complété avec des pages plus âgées.'),
 'es': dict(title='Encuéntrame una solución', desc='Cuatro preguntas llevan a tres soluciones de Saving Planets. No guardamos lo que respondes.',
            h='Encuéntrame una solución', lead='Cuatro preguntas. Tres ideas de las soluciones que ya están en este sitio. No guardamos lo que eliges.',
            q1='¿Qué causa?', q2='¿Cómo quieres ayudar?', q3='¿Dónde?', q4='¿Para quién?',
            ocean='Océano', rivers='Ríos y lagos', forests='Bosques', polar='Polos', earth='La Tierra desde la órbita', space='Espacio',
            money='Dar dinero', time='Dar tiempo', learn='Aprender', near='Cerca de un lugar donde ocurre el trabajo', remote='Desde casa',
            kid='Un niño (kínder a 5.º grado)', adult='Un adulto',
            go='Ver tres ideas', priv='No pedimos nombre, escuela ni lugar, y no guardamos estas respuestas.',
            out='Tres ideas', exact='Estas tres coinciden con las cuatro respuestas.',
            relaxed='Menos de tres coincidían con el lugar, así que la lista es un poco más amplia. La misma causa y el mismo tipo de ayuda.',
            short='Coinciden menos de tres soluciones. No añadimos otras que no encajan.',
            none='Ninguna solución de este sitio coincide.',
            why_near='La página de la solución nombra un lugar.', why_remote='Se puede hacer sin viajar a la obra.',
            kid_empty='Ninguna página de kínder a 5.º coincide con esta causa. No rellenamos la lista con páginas para mayores.'),
 'ar': dict(title='طابقني مع حل', desc='أربعة أسئلة تقود إلى ثلاثة حلول من Saving Planets. لا نحفظ ما تجيب عنه.',
            h='طابقني مع حل', lead='أربعة أسئلة. ثلاث أفكار من الحلول الموجودة أصلًا في هذا الموقع. لا نحفظ ما تختاره.',
            q1='أي قضية؟', q2='كيف تريد أن تساعد؟', q3='أين؟', q4='لمن هذا؟',
            ocean='المحيط', rivers='الأنهار والبحيرات', forests='الغابات', polar='القطبان', earth='الأرض من المدار', space='الفضاء',
            money='أعطِ مالًا', time='أعطِ وقتًا', learn='تعلّم', near='قرب مكان يحدث فيه العمل', remote='من المنزل',
            kid='طفل (من الروضة إلى الصف الخامس)', adult='بالغ',
            go='أظهر ثلاث أفكار', priv='لا نطلب اسمًا ولا مدرسة ولا مكانًا، ولا نحفظ هذه الإجابات.',
            out='ثلاث أفكار', exact='هذه الثلاثة تطابق الإجابات الأربع.',
            relaxed='أقل من ثلاثة طابقت المكان، لذلك القائمة أوسع قليلًا. نفس القضية ونفس نوع المساعدة.',
            short='أقل من ثلاثة حلول تطابق. لا نضيف ما لا يناسب.',
            none='لا حل في هذا الموقع يطابق.',
            why_near='صفحة الحل تذكر مكانًا.', why_remote='يمكن فعل ذلك دون السفر إلى موقع العمل.',
            kid_empty='لا صفحة من الروضة إلى الصف الخامس تطابق هذه القضية. لم نملأ القائمة بصفحات أكبر.'),
 'it': dict(title='Abbinami a una soluzione', desc='Quattro domande portano a tre soluzioni di Saving Planets. Non salviamo quello che rispondi.',
            h='Abbinami a una soluzione', lead='Quattro domande. Tre idee dalle soluzioni già su questo sito. Non salviamo quello che scegli.',
            q1='Quale causa?', q2='Come vuoi aiutare?', q3='Dove?', q4='Per chi è?',
            ocean='Oceano', rivers='Fiumi e laghi', forests='Foreste', polar='Poli', earth='La Terra dall\'orbita', space='Spazio',
            money='Dare denaro', time='Dare tempo', learn='Imparare', near='Vicino a un luogo dove avviene il lavoro', remote='Da casa',
            kid='Un bambino (dalla scuola dell\'infanzia alla quinta)', adult='Un adulto',
            go='Mostra tre idee', priv='Non chiediamo nome, scuola o luogo, e non salviamo queste risposte.',
            out='Tre idee', exact='Queste tre corrispondono a tutte e quattro le risposte.',
            relaxed='Meno di tre corrispondevano al luogo, quindi l\'elenco è un po\' più ampio. Stessa causa e stesso tipo di aiuto.',
            short='Corrispondono meno di tre soluzioni. Non ne aggiungiamo che non c\'entrano.',
            none='Nessuna soluzione di questo sito corrisponde.',
            why_near='La pagina della soluzione indica un luogo.', why_remote='Si può fare senza andare sul posto del lavoro.',
            kid_empty='Nessuna pagina dalla scuola dell\'infanzia alla quinta corrisponde a questa causa. Non abbiamo riempito con pagine più grandi.'),
 'he': dict(title='התאימו לי פתרון', desc='ארבע שאלות מובילות לשלושה פתרונות של Saving Planets. מה שאתם עונים לא נשמר.',
            h='התאימו לי פתרון', lead='ארבע שאלות. שלושה רעיונות מהפתרונות שכבר באתר. אנחנו לא שומרים את מה שבחרתם.',
            q1='איזו מטרה?', q2='איך רוצים לעזור?', q3='איפה?', q4='למי זה?',
            ocean='אוקיינוס', rivers='נהרות ואגמים', forests='יערות', polar='הקטבים', earth='כדור הארץ מהמסלול', space='חלל',
            money='לתת כסף', time='לתת זמן', learn='ללמוד', near='ליד מקום שבו העבודה קורית', remote='מהבית',
            kid='ילד או ילדה (גן עד כיתה ה)', adult='מבוגר או מבוגרת',
            go='הציגו שלושה רעיונות', priv='אנחנו לא שואלים שם, בית ספר או מקום, ולא שומרים את התשובות.',
            out='שלושה רעיונות', exact='שלושת אלה מתאימים לארבע התשובות.',
            relaxed='פחות משלושה התאימו למקום, אז הרשימה רחבה מעט יותר. אותה מטרה ואותו סוג עזרה.',
            short='פחות משלושה פתרונות התאימו. לא מוסיפים כאלה שלא מתאימים.',
            none='אין באתר פתרון שמתאים.',
            why_near='עמוד הפתרון מציין מקום.', why_remote='אפשר לעשות את זה בלי לנסוע לאתר העבודה.',
            kid_empty='אין עמוד מגן עד כיתה ה שמתאים למטרה הזו. לא מילאנו את הרשימה בעמודים למבוגרים יותר.'),
}

def radio(name, value, label):
    rid = name + '-' + value
    return '<label class="sp9-opt" for="%s"><input type="radio" name="%s" id="%s" value="%s" required> <span>%s</span></label>' % (rid, name, rid, value, E(label))

def match_main(lang):
    c = MATCH_COPY[lang]
    u = UI[lang]
    qs = [
        ('cause', c['q1'], [('ocean', c['ocean']), ('rivers', c['rivers']), ('forests', c['forests']), ('polar', c['polar']), ('earth', c['earth']), ('space', c['space'])]),
        ('help', c['q2'], [('money', c['money']), ('time', c['time']), ('learn', c['learn'])]),
        ('where', c['q3'], [('near', c['near']), ('remote', c['remote'])]),
        ('who', c['q4'], [('kid', c['kid']), ('adult', c['adult'])]),
    ]
    fields = []
    for name, legend, opts in qs:
        fields.append('<fieldset><legend>' + E(legend) + '</legend>' + ''.join(radio(name, v, lab) for v, lab in opts) + '</fieldset>')
    js_copy = {k: c[k] for k in ('exact', 'relaxed', 'short', 'none', 'kid_empty', 'why_near', 'why_remote', 'out')}
    js_copy.update(don=u['don'], vol=u['vol'], learn=u['learn'])
    return ('<section class="page-hero hero-learn"><div class="page-hero-content"><h1>' + E(c['h']) + '</h1><p>' + E(c['lead']) + '</p></div></section>'
            '<main id="main"><form class="sp9-form" id="match-form">' + ''.join(fields) +
            '<p class="sp9-priv">' + E(c['priv']) + '</p>'
            '<button type="submit" class="btn">' + E(c['go']) + '</button></form>'
            '<section id="match-out" aria-live="polite" aria-labelledby="match-out-h" hidden><h2 id="match-out-h">' + E(c['out']) + '</h2><p id="match-note"></p><ol id="match-list"></ol></section>'
            '<p class="photo-credit">Created by the Founder and SI.</p></main>'
            '<script id="match-js">window.SP9MATCH=' + json.dumps(js_copy, ensure_ascii=False) + ';</script>'
            '<script src="' + pre(lang) + 'assets/match.js" defer></script>')

ADOPT = {
 'en': dict(title='Adopt a solution', desc='A class pairs a Teacher Sheet with a blank project template and a blank progress card.',
            h='Adopt a solution', lead='A class picks one solution already on this site, teaches from its Teacher Sheet, and fills in a progress card. The card starts blank. We do not count a class total.',
            how='How it works', s1='Pick one solution', s1p='Use Match me to a solution, or choose from Teacher Sheets.',
            s2='Teach from the sheet', s2p='Open that solution\'s Teacher Sheet. It has the Five W\'s, a short summary, sources, and three questions.',
            s3='Fill the card yourselves', s3p='Print the template and the progress card. Students write what they did. Leave a box empty if that week did not happen.',
            tpl='Class project template', card='Progress card',
            classn='Class name', sol='Solution we picked', did='What we will do', date='Date', source='Source we will cite',
            w='Week', empty='Your class writes here. This starts blank.',
            sheets='Teacher Sheets', plan='Printable lesson plan'),
 'fr': dict(title='Adopter une solution', desc='Une classe associe une fiche enseignant, un modèle de projet vide et une carte de suivi vide.',
            h='Adopter une solution', lead='Une classe choisit une solution déjà sur ce site, enseigne avec sa fiche, et remplit une carte de suivi. La carte commence vide. Nous ne comptons pas de total de classes.',
            how='Comment ça marche', s1='Choisir une solution', s1p='Utilisez Trouvez-moi une solution, ou choisissez dans les fiches enseignants.',
            s2='Enseigner avec la fiche', s2p='Ouvrez la fiche de cette solution. Elle a les cinq W, un résumé, les sources et trois questions.',
            s3='Remplir la carte vous-mêmes', s3p='Imprimez le modèle et la carte. Les élèves écrivent ce qu\'ils ont fait. Laissez une case vide si la semaine n\'a pas eu lieu.',
            tpl='Modèle de projet de classe', card='Carte de suivi',
            classn='Nom de la classe', sol='Solution choisie', did='Ce que nous ferons', date='Date', source='Source que nous citerons',
            w='Semaine', empty='La classe écrit ici. C\'est vide au départ.',
            sheets='Fiches enseignants', plan='Plan de cours imprimable'),
 'es': dict(title='Adopta una solución', desc='Una clase une una ficha docente, una plantilla de proyecto en blanco y una tarjeta de avance en blanco.',
            h='Adopta una solución', lead='Una clase elige una solución que ya está en este sitio, enseña con su ficha y completa una tarjeta de avance. La tarjeta empieza en blanco. No contamos un total de clases.',
            how='Cómo funciona', s1='Elige una solución', s1p='Usa Encuéntrame una solución o elige entre las fichas docentes.',
            s2='Enseña con la ficha', s2p='Abre la ficha de esa solución. Tiene las cinco W, un resumen, las fuentes y tres preguntas.',
            s3='Completen la tarjeta ustedes', s3p='Impriman la plantilla y la tarjeta. El alumnado escribe lo que hizo. Dejen una casilla vacía si esa semana no ocurrió.',
            tpl='Plantilla de proyecto de clase', card='Tarjeta de avance',
            classn='Nombre de la clase', sol='Solución elegida', did='Qué haremos', date='Fecha', source='Fuente que citaremos',
            w='Semana', empty='La clase escribe aquí. Empieza en blanco.',
            sheets='Fichas para docentes', plan='Plan de clase imprimible'),
 'ar': dict(title='تبنَّ حلًا', desc='يربط الصف ورقة المعلم بنموذج مشروع فارغ وبطاقة تقدم فارغة.',
            h='تبنَّ حلًا', lead='يختار الصف حلًا موجودًا أصلًا في هذا الموقع، ويدرس من ورقة المعلم، ويملأ بطاقة تقدم. البطاقة تبدأ فارغة. لا نحصي مجموع الصفوف.',
            how='كيف يعمل', s1='اختاروا حلًا واحدًا', s1p='استخدموا طابقني مع حل، أو اختاروا من أوراق المعلمين.',
            s2='درّسوا من الورقة', s2p='افتحوا ورقة ذلك الحل. فيها الأسئلة الخمسة وملخص قصير والمصادر وثلاثة أسئلة.',
            s3='املأوا البطاقة بأنفسكم', s3p='اطبعوا النموذج والبطاقة. يكتب الطلاب ما فعلوه. اتركوا مربعًا فارغًا إذا لم يحدث ذلك الأسبوع.',
            tpl='نموذج مشروع الصف', card='بطاقة التقدم',
            classn='اسم الصف', sol='الحل الذي اخترناه', did='ماذا سنفعل', date='التاريخ', source='المصدر الذي سنذكره',
            w='أسبوع', empty='يكتب الصف هنا. هذا يبدأ فارغًا.',
            sheets='أوراق المعلمين', plan='خطة درس للطباعة'),
 'it': dict(title='Adotta una soluzione', desc='Una classe unisce una scheda docente, un modello di progetto vuoto e una scheda di avanzamento vuota.',
            h='Adotta una soluzione', lead='Una classe sceglie una soluzione già su questo sito, insegna con la sua scheda e compila una scheda di avanzamento. La scheda inizia vuota. Non contiamo un totale di classi.',
            how='Come funziona', s1='Scegliete una soluzione', s1p='Usate Abbinami a una soluzione, oppure scegliete dalle schede docenti.',
            s2='Insegnate con la scheda', s2p='Aprite la scheda di quella soluzione. Ha le cinque W, un riassunto, le fonti e tre domande.',
            s3='Compilate la scheda voi', s3p='Stampate il modello e la scheda. Gli studenti scrivono che cosa hanno fatto. Lasciate una casella vuota se quella settimana non c\'è stata.',
            tpl='Modello di progetto di classe', card='Scheda di avanzamento',
            classn='Nome della classe', sol='Soluzione scelta', did='Che cosa faremo', date='Data', source='Fonte che citeremo',
            w='Settimana', empty='La classe scrive qui. All\'inizio è vuoto.',
            sheets='Schede per insegnanti', plan='Piano di lezione stampabile'),
 'he': dict(title='אמצו פתרון', desc='כיתה מחברת דף מורה, תבנית פרויקט ריקה וכרטיס התקדמות ריק.',
            h='אמצו פתרון', lead='כיתה בוחרת פתרון שכבר באתר, מלמדת מדף המורה וממלאת כרטיס התקדמות. הכרטיס מתחיל ריק. אנחנו לא סופרים סך כיתות.',
            how='איך זה עובד', s1='בחרו פתרון אחד', s1p='השתמשו ב״התאימו לי פתרון״, או בחרו מדפי המורים.',
            s2='למדו מהדף', s2p='פתחו את דף המורה של הפתרון. יש בו את חמש השאלות, סיכום קצר, מקורות ושלוש שאלות.',
            s3='מלאו את הכרטיס בעצמכם', s3p='הדפיסו את התבנית ואת הכרטיס. התלמידים כותבים מה עשו. השאירו משבצת ריקה אם השבוע לא קרה.',
            tpl='תבנית פרויקט לכיתה', card='כרטיס התקדמות',
            classn='שם הכיתה', sol='הפתרון שבחרנו', did='מה נעשה', date='תאריך', source='מקור שנציין',
            w='שבוע', empty='הכיתה כותבת כאן. זה מתחיל ריק.',
            sheets='דפי מורים', plan='מערך שיעור להדפסה'),
}

def blanks(labels):
    return ''.join('<p class="sp9-line"><span>' + E(lab) + '</span><span class="sp9-blank" aria-hidden="true"></span></p>' for lab in labels)

def adopt_main(lang):
    c = ADOPT[lang]
    weeks = ''.join('<li><label><input type="checkbox" disabled> ' + E(c['w']) + ' ' + str(i) + '</label><span class="sp9-blank"></span></li>' for i in range(1, 5))
    return ('<section class="page-hero hero-teach"><div class="page-hero-content"><h1>' + E(c['h']) + '</h1><p>' + E(c['lead']) + '</p></div></section>'
            '<main id="main"><section class="five-ws" id="how"><h2>' + E(c['how']) + '</h2><ol><li><strong>' + E(c['s1']) + '</strong> ' + E(c['s1p']) + ' <a href="Match.html">' + E(UI[lang]['match']) + '</a></li>'
            '<li><strong>' + E(c['s2']) + '</strong> ' + E(c['s2p']) + '</li>'
            '<li><strong>' + E(c['s3']) + '</strong> ' + E(c['s3p']) + '</li></ol>'
            '<p><a class="btn" href="Teachers.html">' + E(c['sheets']) + '</a> <a class="btn" href="Lesson_Plan.html">' + E(c['plan']) + '</a></p></section>'
            '<section class="five-ws sp9-print" id="template"><h2>' + E(c['tpl']) + '</h2>' + blanks([c['classn'], c['sol'], c['did'], c['date'], c['source']]) + '</section>'
            '<section class="five-ws sp9-print" id="card"><h2>' + E(c['card']) + '</h2><p>' + E(c['empty']) + '</p><ul class="sp9-weeks">' + weeks + '</ul></section>'
            '<p class="photo-credit">Created by the Founder and SI.</p></main>')

BADGE = {
 'en': dict(title='Vetted by Saving Planets', desc='What the Vetted by Saving Planets badge means, and the embed code. The badge image is in English.',
            h='Vetted by Saving Planets',
            p1='The badge means the group has a solution page on Saving Planets.',
            p2='When we show a Donate link, it follows the rule on How We Evaluate: the organization publishes audited finances or carries a recognized charity rating. If we do not have that basis, we do not show a Donate link.',
            p3='The badge is not a partnership. It is not a promise that every number on the group\'s own site is right. It is not a star rating of our own.',
            p4='This page does not email anyone.',
            img='The badge artwork is in English so the embed code is the same on every site.',
            code='Embed code', copy='Copy embed code', copied='Copied.'),
 'fr': dict(title='Vérifié par Saving Planets', desc='Ce que signifie le badge Vetted by Saving Planets, et le code à intégrer. L\'image du badge est en anglais.',
            h='Vérifié par Saving Planets',
            p1='Le badge signifie que le groupe a une page de solution sur Saving Planets.',
            p2='Quand nous montrons un lien Don, il suit la règle de Comment nous évaluons : l\'organisation publie des comptes audités ou porte une note caritative reconnue. Sans cette base, nous ne montrons pas de lien Don.',
            p3='Le badge n\'est pas un partenariat. Il ne promet pas que chaque chiffre du site du groupe est exact. Ce n\'est pas notre propre note en étoiles.',
            p4='Cette page n\'envoie de courriel à personne.',
            img='Le dessin du badge est en anglais pour que le code intégré soit le même partout.',
            code='Code à intégrer', copy='Copier le code', copied='Copié.'),
 'es': dict(title='Revisado por Saving Planets', desc='Qué significa la insignia Vetted by Saving Planets y el código para insertarla. La imagen está en inglés.',
            h='Revisado por Saving Planets',
            p1='La insignia significa que el grupo tiene una página de solución en Saving Planets.',
            p2='Cuando mostramos un enlace de donación, sigue la regla de Cómo evaluamos: la organización publica finanzas auditadas o tiene una calificación benéfica reconocida. Sin esa base, no mostramos un enlace de donación.',
            p3='La insignia no es una alianza. No promete que cada cifra del sitio del grupo sea correcta. No es una calificación de estrellas nuestra.',
            p4='Esta página no envía correo a nadie.',
            img='El dibujo de la insignia está en inglés para que el código sea el mismo en todos los sitios.',
            code='Código para insertar', copy='Copiar el código', copied='Copiado.'),
 'ar': dict(title='راجعته Saving Planets', desc='معنى شارة Vetted by Saving Planets ورمز التضمين. صورة الشارة بالإنجليزية.',
            h='راجعته Saving Planets',
            p1='تعني الشارة أن لدى المجموعة صفحة حل على Saving Planets.',
            p2='عندما نعرض رابط تبرع، فهو يتبع قاعدة كيف نقيّم: تنشر المنظمة بيانات مالية مدققة أو تحمل تصنيفًا خيريًا معترفًا به. بلا هذا الأساس لا نعرض رابط تبرع.',
            p3='الشارة ليست شراكة. لا تعد بأن كل رقم في موقع المجموعة صحيح. ليست تقييمًا نجميًا من عندنا.',
            p4='هذه الصفحة لا ترسل بريدًا إلى أحد.',
            img='رسم الشارة بالإنجليزية حتى يبقى رمز التضمين نفسه في كل موقع.',
            code='رمز التضمين', copy='انسخ الرمز', copied='تم النسخ.'),
 'it': dict(title='Controllato da Saving Planets', desc='Che cosa significa il badge Vetted by Saving Planets e il codice di incorporamento. L\'immagine è in inglese.',
            h='Controllato da Saving Planets',
            p1='Il badge significa che il gruppo ha una pagina di soluzione su Saving Planets.',
            p2='Quando mostriamo un link per donare, segue la regola di Come valutiamo: l\'organizzazione pubblica bilanci verificati o ha un rating di beneficenza riconosciuto. Senza quella base non mostriamo un link per donare.',
            p3='Il badge non è una partnership. Non promette che ogni cifra sul sito del gruppo sia giusta. Non è un nostro voto in stelle.',
            p4='Questa pagina non invia email a nessuno.',
            img='Il disegno del badge è in inglese così il codice è lo stesso su ogni sito.',
            code='Codice da incorporare', copy='Copia il codice', copied='Copiato.'),
 'he': dict(title='נבדק על ידי Saving Planets', desc='מה משמעות התג Vetted by Saving Planets וקוד ההטמעה. התמונה באנגלית.',
            h='נבדק על ידי Saving Planets',
            p1='התג אומר שלקבוצה יש עמוד פתרון ב-Saving Planets.',
            p2='כשאנחנו מציגים קישור תרומה, הוא עומד בכלל שב״איך אנחנו מעריכים״: הארגון מפרסם כספים מבוקרים או נושא דירוג צדקה מוכר. בלי הבסיס הזה אין קישור תרומה.',
            p3='התג אינו שותפות. הוא לא מבטיח שכל מספר באתר הקבוצה נכון. הוא אינו דירוג כוכבים שלנו.',
            p4='העמוד הזה לא שולח דוא״ל לאף אחד.',
            img='ציור התג באנגלית כדי שקוד ההטמעה יהיה זהה בכל אתר.',
            code='קוד להטמעה', copy='העתקת הקוד', copied='הועתק.'),
}

EMBED = '<a href="https://www.savingplanets.com/Vetted_Badge.html"><img src="https://www.savingplanets.com/assets/badge/vetted-by-saving-planets.svg" width="320" height="96" alt="Vetted by Saving Planets"></a>'

def badge_main(lang):
    c = BADGE[lang]
    p = pre(lang)
    return ('<section class="page-hero hero-learn"><div class="page-hero-content"><h1>' + E(c['h']) + '</h1><p>' + E(c['img']) + '</p></div></section>'
            '<main id="main"><section class="five-ws" id="meaning"><img src="' + p + 'assets/badge/vetted-by-saving-planets.svg" width="320" height="96" alt="Vetted by Saving Planets">'
            '<p><a href="' + p + 'assets/badge/vetted-by-saving-planets.svg">SVG</a> · <a href="' + p + 'assets/badge/vetted-by-saving-planets.png">PNG</a></p>'
            '<p>' + E(c['p1']) + '</p><p>' + E(c['p2']) + ' <a href="How_We_Evaluate.html#s3">' + E(UI[lang]['how']) + '</a></p>'
            '<p>' + E(c['p3']) + '</p><p>' + E(c['p4']) + '</p></section>'
            '<section class="five-ws" id="embed"><h2>' + E(c['code']) + '</h2>'
            '<textarea id="badge-code" rows="4" readonly>' + E(EMBED) + '</textarea>'
            '<p><button type="button" class="btn" id="badge-copy" data-ok="' + E(c['copied']) + '">' + E(c['copy']) + '</button></p></section>'
            '<p class="photo-credit">Created by the Founder and SI.</p></main>'
            '<script>(function(){var b=document.getElementById("badge-copy"),t=document.getElementById("badge-code");if(!b)return;b.addEventListener("click",function(){var done=function(){b.textContent=b.getAttribute("data-ok")};if(navigator.clipboard)navigator.clipboard.writeText(t.value).then(done,function(){t.select();document.execCommand("copy");done();});else{t.select();document.execCommand("copy");done();}});})();</script>')

CHAL = {
 'en': dict(title='Classroom and creator challenge (draft)', desc='Internal draft. Not open. The counter starts at zero because no total is being counted.',
            h='Classroom and creator challenge', soon='Coming soon. Internal draft. Partners are not arranged. This page is not in the menu.',
            how='How it would work', howp='When partners are arranged, a class or a creator would pick vetted groups from this site and share one action. That step is not open.',
            count_l='Classrooms and creators joined', note='Placeholder. This counter starts at 0. Nothing is being counted yet.',
            groups='Vetted groups in this challenge', empty='No partner groups are confirmed. The list stays empty until they are.'),
 'fr': dict(title='Défi classes et créateurs (brouillon)', desc='Brouillon interne. Pas ouvert. Le compteur part de zéro car aucun total n\'est compté.',
            h='Défi classes et créateurs', soon='Bientôt. Brouillon interne. Les partenaires ne sont pas arrangés. Cette page n\'est pas dans le menu.',
            how='Comment cela marcherait', howp='Quand des partenaires seront là, une classe ou un créateur choisirait des groupes vérifiés sur ce site et partagerait une action. Cette étape n\'est pas ouverte.',
            count_l='Classes et créateurs inscrits', note='Espace réservé. Ce compteur commence à 0. Rien n\'est compté pour l\'instant.',
            groups='Groupes vérifiés dans ce défi', empty='Aucun groupe partenaire n\'est confirmé. La liste reste vide jusqu\'à ce qu\'ils le soient.'),
 'es': dict(title='Reto de aulas y creadores (borrador)', desc='Borrador interno. No está abierto. El contador empieza en cero porque no se cuenta ningún total.',
            h='Reto de aulas y creadores', soon='Próximamente. Borrador interno. Los socios no están acordados. Esta página no está en el menú.',
            how='Cómo funcionaría', howp='Cuando haya socios, una clase o un creador elegiría grupos revisados de este sitio y compartiría una acción. Ese paso no está abierto.',
            count_l='Aulas y creadores unidos', note='Marcador de posición. Este contador empieza en 0. Todavía no se cuenta nada.',
            groups='Grupos revisados en este reto', empty='No hay grupos socios confirmados. La lista sigue vacía hasta que los haya.'),
 'ar': dict(title='تحدي الصفوف والمبدعين (مسودة)', desc='مسودة داخلية. غير مفتوح. العداد يبدأ من صفر لأنه لا يُحصى مجموع.',
            h='تحدي الصفوف والمبدعين', soon='قريبًا. مسودة داخلية. الشركاء غير مرتبين. هذه الصفحة ليست في القائمة.',
            how='كيف سيعمل', howp='عندما يُرتَّب الشركاء، يختار صف أو مبدع مجموعات مراجعة من هذا الموقع ويشارك بفعل واحد. هذه الخطوة غير مفتوحة.',
            count_l='صفوف ومبدعون انضموا', note='عنصر نائب. هذا العداد يبدأ من 0. لا شيء يُحصى بعد.',
            groups='مجموعات مراجعة في هذا التحدي', empty='لا مجموعات شريكة مؤكدة. تبقى القائمة فارغة إلى أن تُؤكد.'),
 'it': dict(title='Sfida classi e creator (bozza)', desc='Bozza interna. Non è aperta. Il contatore parte da zero perché non si conta alcun totale.',
            h='Sfida classi e creator', soon='Presto. Bozza interna. I partner non sono organizzati. Questa pagina non è nel menu.',
            how='Come funzionerebbe', howp='Quando ci saranno dei partner, una classe o un creator sceglierebbe gruppi controllati da questo sito e condividerebbe un\'azione. Quel passo non è aperto.',
            count_l='Classi e creator iscritti', note='Segnaposto. Questo contatore parte da 0. Non si conta ancora nulla.',
            groups='Gruppi controllati in questa sfida', empty='Nessun gruppo partner è confermato. L\'elenco resta vuoto finché non lo saranno.'),
 'he': dict(title='אתגר כיתות ויוצרים (טיוטה)', desc='טיוטה פנימית. לא פתוח. המונה מתחיל באפס כי שום סך לא נספר.',
            h='אתגר כיתות ויוצרים', soon='בקרוב. טיוטה פנימית. אין עדיין שותפים. העמוד הזה לא בתפריט.',
            how='איך זה יעבוד', howp='כשיהיו שותפים, כיתה או יוצר יבחרו קבוצות שנבדקו באתר וישתפו פעולה אחת. הצעד הזה לא פתוח.',
            count_l='כיתות ויוצרים שהצטרפו', note='מציין מקום. המונה מתחיל ב-0. עדיין לא נספר דבר.',
            groups='קבוצות שנבדקו באתגר הזה', empty='אין קבוצות שותפות מאושרות. הרשימה נשארת ריקה עד שיהיו.'),
}

def challenge_main(lang):
    c = CHAL[lang]
    return ('<section class="page-hero hero-learn"><div class="page-hero-content"><p class="sp9-soon">' + E(c['soon']) + '</p><h1>' + E(c['h']) + '</h1></div></section>'
            '<main id="main"><section class="five-ws" id="counter" aria-labelledby="ch-count-l"><h2 id="ch-count-l">' + E(c['count_l']) + '</h2>'
            '<p class="sp9-count" id="ch-count">0</p><p>' + E(c['note']) + '</p></section>'
            '<section class="five-ws" id="how"><h2>' + E(c['how']) + '</h2><p>' + E(c['howp']) + '</p></section>'
            '<section class="five-ws" id="groups"><h2>' + E(c['groups']) + '</h2><p>' + E(c['empty']) + '</p><ul></ul></section>'
            '<p class="photo-credit">Created by the Founder and SI.</p></main>')

def build_page(lang, filename, title, desc, main, robots):
    folder = '' if lang == 'en' else lang + '/'
    src_path = folder + 'How_We_Evaluate.html'
    if not os.path.exists(src_path):
        src_path = 'How_We_Evaluate.html'
    src = open(src_path, encoding='utf8').read()
    def retag(m):
        return m.group(0).replace('How_We_Evaluate.html', filename)
    src = re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>', retag, src)
    src = re.sub(r'<meta property="og:url"[^>]*>', retag, src)
    src = re.sub(r'<title>[^<]*</title>', '<title>' + E(title) + ' | Saving Planets</title>', src, count=1)
    for attr, key in (('name', 'description'), ('property', 'og:description'), ('name', 'twitter:description')):
        src = re.sub(r'(<meta %s="%s" content=")[^"]*"' % (attr, key), r'\1' + E(desc) + '"', src, count=1)
    for attr, key in (('property', 'og:title'), ('name', 'twitter:title')):
        src = re.sub(r'(<meta %s="%s" content=")[^"]*"' % (attr, key), r'\1' + E(title) + ' | Saving Planets"', src, count=1)
    src = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="%s">' % robots, src, count=1)
    src = re.sub(r'<script type="application/ld\+json">.*?</script>', '', src, flags=re.S)
    ld = '<script type="application/ld+json">' + json.dumps({
        '@context': 'https://schema.org', '@type': 'WebPage', 'name': title,
        'description': desc, 'url': 'https://www.savingplanets.com/' + ('' if lang == 'en' else lang + '/') + filename,
        'inLanguage': lang, 'isPartOf': {'@id': 'https://www.savingplanets.com/#website'}}, ensure_ascii=False) + '</script>'
    src = src.replace('</head>', ld + '</head>', 1)
    if robots.startswith('noindex') and 'name="robots"' not in src.split('</head>')[0]:
        src = src.replace('</head>', '<meta name="robots" content="%s"></head>' % robots, 1)
    body = main + '\n<footer'
    src = re.sub(r'<section class="page-hero.*?<footer', body, src, count=1, flags=re.S)
    if filename in ('Match.html', 'Challenge.html') and 'data-no-newsletter' not in src:
        src = src.replace('<body ', '<body data-no-newsletter ', 1)
    write(folder + filename, src)

def build_match_data():
    sols = json.load(open('assets/data/solutions.json', encoding='utf8'))['pages']
    wth = json.load(open('assets/data/ways-to-help.json', encoding='utf8'))
    locs = json.load(open('assets/data/map-locations.json', encoding='utf8'))['solutions']
    kids = set(re.findall(r'"u": "([^"]+\.html)"', open('assets/data/kids-world.en.json', encoding='utf8').read()))
    if not kids:
        kids = set(re.findall(r'"u":"([^"]+\.html)"', open('assets/data/kids-world.en.json', encoding='utf8').read()))
    theme_of = {'ocean': 'ocean', 'rivers': 'rivers', 'lakes': 'rivers', 'forests': 'forests', 'polar': 'polar',
                'earth-observation': 'earth', 'space': 'space', 'planetary-defense': 'space', 'space-weather': 'space',
                'space-disposal': 'space', 'project-r': 'space'}
    rows = []
    for p in sols:
        if p.get('type') != 'solution' or p.get('status') != 'active':
            continue
        slug = p['url'][:-5]
        org = wth['orgs'].get(wth['pages'].get(slug) or '', [None, None, None, None])
        don, hlp = org[1], org[2]
        kind = help_kind(hlp or '')
        loc = locs.get(p['url'], {})
        local = any(pin.get('basis') == 'page' for pin in loc.get('pins') or [])
        remote_flag = bool(don) or kind == 'volunteer' or loc.get('strip') in ('orbit', 'world') or not local
        where = where_of(hlp or '')
        meta = ''
        m = re.search(r'<meta name="description" content="([^"]*)"', read(p['url']))
        if m:
            meta = html.unescape(m.group(1)).strip()
            m2 = re.match(r'(.+?[.!?])(\s|$)', meta)
            meta = (m2.group(1) if m2 else meta)[:220]
        rows.append({'url': p['url'], 'title': p['title'], 'theme': theme_of.get(p.get('category'), 'space'),
                     'blurb': meta, 'give': bool(don), 'time': kind == 'volunteer', 'local': local,
                     'remote': remote_flag, 'kid': p['url'] in kids, 'where': where,
                     'donate': don or '', 'volunteer': hlp if kind == 'volunteer' else ''})
    for lang in LANGS:
        out = []
        for r in rows:
            folder = '' if lang == 'en' else lang + '/'
            path = folder + r['url']
            if lang != 'en' and not os.path.exists(path):
                continue
            title, blurb = r['title'], r['blurb']
            if lang != 'en' and os.path.exists(path):
                src = read(path)
                hm = re.search(r'<h1[^>]*>(.*?)</h1>', src, re.S)
                if hm:
                    title = plain(hm.group(1)) or title
                dm = re.search(r'<meta name="description" content="([^"]*)"', src)
                if dm:
                    blurb = html.unescape(dm.group(1)).strip()
                    m2 = re.match(r'(.+?[.!?])(\s|$)', blurb)
                    blurb = (m2.group(1) if m2 else blurb)[:220]
            item = dict(r)
            item['title'] = title
            item['blurb'] = blurb
            out.append(item)
        json.dump({'generated': TODAY, 'solutions': out}, open('assets/data/match.%s.json' % lang, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print('match', lang, len(out))

CSS = '''
/* SP9: Nov 9 2026 recommendations */
.vet-line{font-size:.92rem;line-height:1.45;margin:.55rem 0 0;max-width:46rem;color:#12324a}
html.dark .vet-line{color:#d6e4f0}
.vet-line a{text-decoration:underline}
.sp9-where{margin:.6rem 0 1rem}
.sp9-where [role=group]{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}
.sp9-where button{font:inherit;min-height:44px;padding:.35rem .8rem;border-radius:999px;border:1px solid currentColor;background:transparent;color:inherit;cursor:pointer}
.sp9-where button[aria-pressed=true]{background:#0b5c8a;border-color:#0b5c8a;color:#fff}
.sp9-where-off{display:none !important}
.sp9-gift{border:1px solid rgba(127,127,127,.35);border-radius:12px;padding:.8rem 1rem;margin:.6rem 0}
.sp9-gift blockquote{margin:.4rem 0;padding-inline-start:.8rem;border-inline-start:3px solid #009cde}
.sp9-form{max-width:720px;margin:1rem auto 2rem;padding:0 1rem}
.sp9-form fieldset{border:1px solid rgba(127,127,127,.4);border-radius:12px;margin:0 0 1rem;padding:.6rem .8rem 1rem}
.sp9-form legend{font-weight:700;padding:0 .3rem}
.sp9-opt{display:flex;align-items:center;gap:.6rem;min-height:44px;margin:.15rem 0}
.sp9-one,.sp9-gifts,.sp9-match{max-width:860px;margin:1rem auto;padding:0 1rem}
.sp9-count{font-size:3rem;font-weight:800;margin:.2rem 0}
.sp9-soon{font-weight:700}
.sp9-line{display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:flex-end;margin:.5rem 0}
.sp9-blank{flex:1 1 12rem;border-bottom:1px solid currentColor;min-height:1.4rem}
.sp9-weeks{list-style:none;padding:0}
.sp9-weeks li{display:flex;gap:1rem;align-items:center;min-height:44px}
#badge-code{width:100%;max-width:720px;min-height:6rem;font:1rem/1.4 ui-monospace,monospace}
.hero-ctas{display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center}
@media print{.sp9-form,.sp9-where,nav,footer,.sp9-adopt{display:none !important}.sp9-print{break-inside:avoid}}
'''

def append_css():
    path = 'extras.css'
    src = open(path, encoding='utf8').read()
    src = re.sub(r'\n?/\* SP9:.*?\*/\n.*', '', src, flags=re.S)
    # only strip our block if we wrap it
    src = re.sub(r'\n*/\* SP9: Nov 9 2026 recommendations \*/.*', '', src, flags=re.S)
    open(path, 'w', encoding='utf8').write(src.rstrip() + '\n' + CSS)

def write_match_js():
    open('assets/match.js', 'w', encoding='utf8').write(r'''(function(){
  var form=document.getElementById('match-form');
  if(!form)return;
  var lang=(document.documentElement.lang||'en').slice(0,2);
  var pre=location.pathname.indexOf('/'+lang+'/')>-1?'../':'';
  var T=window.SP9MATCH||{};
  fetch(pre+'assets/data/match.'+lang+'.json').then(function(r){return r.json()}).then(function(data){
    var all=data.solutions||[];
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var fd=new FormData(form);
      var cause=fd.get('cause'), help=fd.get('help'), where=fd.get('where'), who=fd.get('who');
      function ok(s, place){
        if(s.theme!==cause)return false;
        if(who==='kid'&&!s.kid)return false;
        if(help==='money'&&!s.give)return false;
        if(help==='time'&&!s.time)return false;
        if(!place)return true;
        if(where==='near')return !!(s.local||s.where==='local');
        if(help==='money')return true;
        if(help==='learn')return true;
        if(s.where==='remote')return true;
        if(s.where==='local')return false;
        return !!s.remote;
      }
      var exact=all.filter(function(s){return ok(s,true)});
      exact.sort(function(a,b){return a.title.localeCompare(b.title)});
      var note=T.exact, list=exact.slice(0,3), mode='exact';
      if(who==='kid'&&exact.length===0){
        note=T.kid_empty; list=[];
      } else if(list.length<3){
        var wide=all.filter(function(s){return ok(s,false)});
        wide.sort(function(a,b){return a.title.localeCompare(b.title)});
        if(wide.length>list.length){list=wide.slice(0,3); note=T.relaxed; mode='relaxed';}
        else {note=list.length?T.short:T.none;}
      }
      var out=document.getElementById('match-out');
      out.hidden=false;
      document.getElementById('match-note').textContent=note;
      var ol=document.getElementById('match-list');
      ol.textContent='';
      list.forEach(function(s){
        var li=document.createElement('li');
        var h=document.createElement('a'); h.href=s.url; h.textContent=s.title; li.appendChild(h);
        if(s.blurb){var p=document.createElement('p'); p.textContent=s.blurb; li.appendChild(p);}
        var href=s.url, label=T.learn||'Learn';
        if(help==='money'&&s.donate){href=s.donate; label=T.don||'Donate';}
        else if(help==='time'&&s.volunteer){href=s.volunteer; label=T.vol||'Volunteer';}
        var a=document.createElement('a'); a.className='btn'; a.href=href; a.textContent=label;
        if(/^https?:/.test(href)){a.target='_blank'; a.rel='noopener';}
        var why=document.createElement('p');
        why.textContent=(s.local?T.why_near:T.why_remote)||'';
        li.appendChild(a); li.appendChild(why); ol.appendChild(li);
      });
      out.focus&&out.setAttribute('tabindex','-1'); out.focus();
    });
  });
})();
''')

def make_png():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print('png skipped: no PIL')
        return
    im = Image.new('RGB', (640, 192), '#0b1220')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, 632, 184), radius=28, outline='#8fd3ff', width=6)
    d.ellipse((48, 48, 144, 144), outline='#3ddc97', width=6)
    d.line((78, 100, 100, 124, 132, 78), fill='#3ddc97', width=6)
    font = ImageFont.truetype('assets/fonts/og/Montserrat.ttf', 36)
    font2 = ImageFont.truetype('assets/fonts/og/Montserrat.ttf', 42)
    d.text((168, 48), 'Vetted by', fill='#f4f8fc', font=font)
    d.text((168, 100), 'Saving Planets', fill='#8fd3ff', font=font2)
    im.save('assets/badge/vetted-by-saving-planets.png', 'PNG')
    print('png ok')

def add_i18n_keys():
    # Keep future i18n-build from dropping the new homepage sentence back to English.
    keys = {
        'from the ocean floor to orbit': {l: UI[l]['h1'].split('welcome-minus">')[1].split('</span>')[0].replace("\\'", "'") for l in LANGS if l != 'en'},
    }
    # The span text is the phrase. Also full description.
    en_desc = UI['en']['desc']
    en_sub = UI['en']['sub']
    en_title_bit = 'From the ocean floor to orbit'
    mapping = {
        en_desc: {l: UI[l]['desc'] for l in LANGS if l != 'en'},
        en_sub: {l: UI[l]['sub'] for l in LANGS if l != 'en'},
        en_title_bit: {l: UI[l]['title'].split(' | ')[0] for l in LANGS if l != 'en'},
        'Match me to a solution': {l: UI[l]['match'] for l in LANGS if l != 'en'},
        "Opens the organization's donation page. Saving Planets does not receive the money.": {l: UI[l]['note_don'] for l in LANGS if l != 'en'},
        'Opens NASA citizen science. This is not a donation.': {l: UI[l]['note_cs'] for l in LANGS if l != 'en'},
    }
    for lang in LANGS:
        if lang == 'en':
            continue
        path = 'i18n/%s.json' % lang
        data = json.load(open(path, encoding='utf8'))
        for en, tr in mapping.items():
            data[en] = tr[lang]
        # append-only rewrite preserving insertion of new keys at end; full dump would reorder.
        # Load kept order; new keys are at the end in Py3.7+.
        text = json.dumps(data, ensure_ascii=False, indent=0, separators=(',', ': '))
        # indent=0 still pretty-prints. The existing file is one pair per line with indent None-like.
        # Avoid a multi-thousand-line reformat: splice new keys before the closing brace.
        raw = open(path, encoding='utf8').read().rstrip()
        if not raw.endswith('}'):
            continue
        body = raw[:-1].rstrip()
        if body.endswith(','):
            body = body[:-1]
        extra = []
        existing = json.load(open(path, encoding='utf8'))
        for en, tr in mapping.items():
            line = json.dumps(en, ensure_ascii=False) + ': ' + json.dumps(tr[lang], ensure_ascii=False)
            if en in existing and existing[en] == tr[lang]:
                continue
            # remove old line if present
            raw_now = open(path, encoding='utf8').read()
            pat = re.compile(r'\n' + re.escape(json.dumps(en, ensure_ascii=False)) + r': .*(?=,?\n)', re.M)
            # simpler: if key exists, skip (first run adds; later runs skip if equal)
            if en in existing:
                if existing[en] != tr[lang]:
                    existing[en] = tr[lang]
                continue
            extra.append(line)
        if not extra and all(existing.get(en) == tr[lang] for en, tr in mapping.items()):
            continue
        if extra:
            raw = open(path, encoding='utf8').read().rstrip()
            if raw.endswith('}'):
                raw = raw[:-1].rstrip()
                if not raw.endswith(','):
                    raw += ','
                raw += '\n' + ',\n'.join(extra) + '\n}\n'
                open(path, 'w', encoding='utf8').write(raw)
                print('i18n keys', lang, len(extra))

def self_check():
    problems = []
    idx = open('index.html', encoding='utf8').read()
    if 'ocean floor to orbit' not in idx:
        problems.append('homepage headline')
    if 'id="one-action"' not in idx:
        problems.append('one action')
    if 'Match.html' not in idx:
        problems.append('match cta')
    if 'class="vet-line"' not in open('4ocean.html', encoding='utf8').read():
        problems.append('vet line 4ocean')
    w = open('Ways_to_Help.html', encoding='utf8').read()
    if 'Careers<span class="sr-only"> – ESA' not in w and '>Careers<span class="sr-only"> – ESA' not in w:
        # button text then sr-only
        if not re.search(r'>Careers<span class="sr-only"> – ESA', w):
            problems.append('ESA careers label')
    if 'id="wh-where"' not in w:
        problems.append('where filter')
    if 'citsci-globe' not in w and 'Globe at Night' not in w:
        problems.append('citizen science cards')
    if 'what-a-gift-does' not in open('Terraformation.html', encoding='utf8').read():
        problems.append('gift card')
    if 'Adopt_a_Solution.html' not in open('Teachers.html', encoding='utf8').read():
        problems.append('adopt link')
    if 'Challenge.html' in open('scripts/build-nav.py', encoding='utf8').read():
        problems.append('challenge linked from nav generator')
    nav = open('index.html', encoding='utf8').read()
    if 'href="Challenge.html"' in nav:
        problems.append('challenge in homepage')
    ch = open('Challenge.html', encoding='utf8').read()
    if 'noindex' not in ch or '>0<' not in ch and 'sp9-count' not in ch:
        problems.append('challenge draft')
    for lang in LANGS:
        folder = '' if lang == 'en' else lang + '/'
        for fn in ('Match.html', 'Adopt_a_Solution.html', 'Vetted_Badge.html', 'Challenge.html'):
            if not os.path.exists(folder + fn):
                problems.append('missing ' + folder + fn)
    if problems:
        raise SystemExit('CHECK FAIL: ' + ', '.join(problems))
    print('self-check ok')

def main():
    append_css()
    write_match_js()
    make_png()
    n = 0
    for lang in LANGS:
        folder = '' if lang == 'en' else lang + '/'
        for fn in os.listdir(folder or '.'):
            if not fn.endswith('.html'):
                continue
            path = folder + fn
            if fn in ('Match.html', 'Adopt_a_Solution.html', 'Vetted_Badge.html', 'Challenge.html'):
                continue
            src = read(path)
            src2 = relabel_buttons(src, lang)
            src2 = patch_help_sections(src2, lang, path)
            if src2 != src:
                write(path, src2); n += 1
            else:
                _PAGE_CACHE[path] = src
        # targeted
        write(folder + 'index.html', patch_index(folder + 'index.html', lang)); n += 1
        for fn in ('Teachers.html', 'Lesson_Plan.html'):
            if os.path.exists(folder + fn):
                write(folder + fn, patch_adopt_links(folder + fn, lang))
        if os.path.exists(folder + 'Earth_Observation.html'):
            write(folder + 'Earth_Observation.html', patch_eo(folder + 'Earth_Observation.html', lang))
        if os.path.exists(folder + 'Ways_to_Help.html'):
            write(folder + 'Ways_to_Help.html', patch_wth(folder + 'Ways_to_Help.html', lang))
        for claim in GIFTS['claims']:
            p = folder + claim['page']
            if os.path.exists(p):
                write(p, gift_on_solution(p, lang))
    build_match_data()
    for lang in LANGS:
        c = MATCH_COPY[lang]
        build_page(lang, 'Match.html', c['title'], c['desc'], match_main(lang), 'index,follow')
        a = ADOPT[lang]
        build_page(lang, 'Adopt_a_Solution.html', a['title'], a['desc'], adopt_main(lang), 'index,follow')
        b = BADGE[lang]
        build_page(lang, 'Vetted_Badge.html', b['title'], b['desc'], badge_main(lang), 'index,follow')
        h = CHAL[lang]
        build_page(lang, 'Challenge.html', h['title'], h['desc'], challenge_main(lang), 'noindex,nofollow')
    add_i18n_keys()
    self_check()
    print('competitive build done', TODAY)

if __name__ == '__main__':
    main()
