#!/usr/bin/env python3
"""Oct 20 2026 (owner-approved corrections policy, decisions 3+4): SI-translated reader note on every translated page
(fr/es/ar/it/he) + Corrections_Policy.html in all six languages (built from each language's Corrections.html shell) +
a link block on Corrections.html. Idempotent (markers). Runs late in weekly-sync, after every page generator.
Replaces he-si-note.py (its HE-SI-NOTE block is swapped for the SI-NOTE block). Credit group name: Language Partners.
Phase 2 native-review triggers are NOT here (decision 5 pending)."""
import glob, html, os, re
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
SITE = 'https://www.savingplanets.com/'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
RTL = {'ar', 'he'}
MAIL = 'mailto:translate@savingplanets.com?subject=Translation%20correction'
ERR = 'mailto:errors@savingplanets.com?subject=Found%20an%20error%20or%20bug%2C%20please%20fix'
TA = '<a href="' + MAIL + '"><bdi>translate@savingplanets.com</bdi></a>'
EA = '<a href="' + ERR + '"><bdi>errors@savingplanets.com</bdi></a>'
# Reader note (approved text; + Language Partners credit name per decision 4; + policy link). {t} = translate@ link.
NOTE = {
 'fr': ("Cette page a été traduite de l'anglais par SI. Vous avez repéré une erreur ou une meilleure formulation ? Écrivez à {t}. Nous lisons chaque message et, avec votre accord, nous vous remercierons dans notre lettre d'information comme Language Partner.", 'Comment nous traitons les corrections'),
 'es': ('Esta página fue traducida del inglés por SI. ¿Viste un error o una mejor forma de decirlo? Escribe a {t}. Leemos cada mensaje y, con tu permiso, te lo agradeceremos en nuestro boletín como Language Partner.', 'Cómo gestionamos las correcciones'),
 'ar': ('تُرجمت هذه الصفحة من الإنجليزية بواسطة SI. هل لاحظت خطأً أو صياغة أفضل؟ راسلنا على {t}. نقرأ كل رسالة، وبإذنك سنشكرك في نشرتنا الإخبارية بصفتك أحد <bdi>Language Partners</bdi>.', 'كيف نتعامل مع التصحيحات'),
 'it': ("Questa pagina è stata tradotta dall'inglese da SI. Hai notato un errore o un modo migliore per dirlo? Scrivi a {t}. Leggiamo ogni messaggio e, con il tuo permesso, ti ringrazieremo nella nostra newsletter come Language Partner.", 'Come gestiamo le correzioni'),
 'he': ('דף זה תורגם מאנגלית על ידי SI. מצאתם טעות או ניסוח טוב יותר? כתבו לנו ל-{t}. אנחנו קוראים כל הודעה, ובאישורכם נודה לכם בניוזלטר שלנו כחלק מ-<bdi>Language Partners</bdi>.', 'איך אנחנו מטפלים בתיקונים'),
}
# Policy page text. Order: en fr es ar it he.
P = {
 'title': ('Corrections Policy for Translated Pages', 'Politique de correction des pages traduites', 'Política de correcciones de las páginas traducidas', 'سياسة تصحيح الصفحات المترجمة', 'Politica di correzione delle pagine tradotte', 'מדיניות תיקונים לדפים מתורגמים'),
 'desc': ('How Saving Planets handles reader corrections to its SI-translated pages: who to write to, how we check and fix, and how we credit you.',
          'Comment Saving Planets traite les corrections des lecteurs sur ses pages traduites par SI : à qui écrire, comment nous vérifions et corrigeons, et comment nous vous remercions.',
          'Cómo Saving Planets gestiona las correcciones de los lectores en sus páginas traducidas por SI: a quién escribir, cómo revisamos y corregimos, y cómo te damos crédito.',
          'كيف يتعامل Saving Planets مع تصحيحات القراء لصفحاته المترجمة بواسطة SI: لمن تكتب، وكيف نتحقق ونصحح، وكيف ننسب إليك الفضل.',
          'Come Saving Planets gestisce le correzioni dei lettori alle pagine tradotte da SI: a chi scrivere, come verifichiamo e correggiamo, e come ti ringraziamo.',
          'איך Saving Planets מטפל בתיקונים של קוראים לדפים שתורגמו על ידי SI: למי לכתוב, איך אנחנו בודקים ומתקנים, ואיך אנחנו נותנים לכם קרדיט.'),
 'h_write': ('Where to Write', 'À qui écrire', 'A quién escribir', 'لمن تكتب', 'A chi scrivere', 'לאן לכתוב'),
 'write': ('Our pages in French, Spanish, Arabic, Italian and Hebrew are translated from English by SI. For a translation mistake or a better way to say something, email {t}. For a science or fact error in any language, email {e}.',
           'Nos pages en français, espagnol, arabe, italien et hébreu sont traduites de l’anglais par SI. Pour une erreur de traduction ou une meilleure formulation, écrivez à {t}. Pour une erreur scientifique ou factuelle, dans n’importe quelle langue, écrivez à {e}.',
           'Nuestras páginas en francés, español, árabe, italiano y hebreo están traducidas del inglés por SI. Para un error de traducción o una mejor forma de decir algo, escribe a {t}. Para un error científico o de datos en cualquier idioma, escribe a {e}.',
           'صفحاتنا بالفرنسية والإسبانية والعربية والإيطالية والعبرية مترجمة من الإنجليزية بواسطة SI. لخطأ في الترجمة أو صياغة أفضل، راسل {t}. ولخطأ علمي أو في المعلومات بأي لغة، راسل {e}.',
           'Le nostre pagine in francese, spagnolo, arabo, italiano ed ebraico sono tradotte dall’inglese da SI. Per un errore di traduzione o un modo migliore di dire qualcosa, scrivi a {t}. Per un errore scientifico o di fatto in qualsiasi lingua, scrivi a {e}.',
           'הדפים שלנו בצרפתית, ספרדית, ערבית, איטלקית ועברית מתורגמים מאנגלית על ידי SI. על טעות בתרגום או ניסוח טוב יותר, כתבו ל-{t}. על טעות מדעית או עובדתית בכל שפה, כתבו ל-{e}.'),
 'h_steps': ('How We Handle a Correction', 'Comment nous traitons une correction', 'Cómo gestionamos una corrección', 'كيف نتعامل مع التصحيح', 'Come gestiamo una correzione', 'איך אנחנו מטפלים בתיקון'),
 'steps': [
  ('<strong>Reply:</strong> we acknowledge your note within 2 business days.', '<strong>Réponse :</strong> nous accusons réception de votre message sous 2 jours ouvrés.', '<strong>Respuesta:</strong> confirmamos la recepción de tu mensaje en 2 días hábiles.', '<strong>الرد:</strong> نؤكد استلام رسالتك خلال يومَي عمل.', '<strong>Risposta:</strong> confermiamo di aver ricevuto il tuo messaggio entro 2 giorni lavorativi.', '<strong>מענה:</strong> נאשר את קבלת ההודעה תוך 2 ימי עבודה.'),
  ('<strong>Check:</strong> we compare your suggestion with the English page and with trusted native-language references, such as Wikipedia in that language, national science and space agencies, and official terminology bodies. Then we translate it back into English to make sure the meaning still matches.',
   '<strong>Vérification :</strong> nous comparons votre suggestion avec la page en anglais et avec des références fiables dans la langue, comme Wikipédia dans cette langue, les agences nationales scientifiques et spatiales et les organismes officiels de terminologie. Puis nous la retraduisons en anglais pour vérifier que le sens est le même.',
   '<strong>Revisión:</strong> comparamos tu sugerencia con la página en inglés y con referencias fiables en ese idioma, como Wikipedia en ese idioma, las agencias científicas y espaciales nacionales y los organismos oficiales de terminología. Después la traducimos de nuevo al inglés para comprobar que el significado coincide.',
   '<strong>التحقق:</strong> نقارن اقتراحك بالصفحة الإنجليزية وبمراجع موثوقة باللغة نفسها، مثل ويكيبيديا بتلك اللغة ووكالات العلوم والفضاء الوطنية وهيئات المصطلحات الرسمية. ثم نترجمه عكسيًا إلى الإنجليزية للتأكد من تطابق المعنى.',
   '<strong>Verifica:</strong> confrontiamo il tuo suggerimento con la pagina in inglese e con riferimenti affidabili nella lingua, come Wikipedia in quella lingua, le agenzie scientifiche e spaziali nazionali e gli enti ufficiali di terminologia. Poi lo ritraduciamo in inglese per assicurarci che il significato corrisponda.',
   '<strong>בדיקה:</strong> אנחנו משווים את ההצעה לדף באנגלית ולמקורות אמינים בשפה עצמה, כמו ויקיפדיה באותה שפה, סוכנויות מדע וחלל לאומיות וגופי מינוח רשמיים. אחר כך אנחנו מתרגמים אותה חזרה לאנגלית כדי לוודא שהמשמעות זהה.'),
  ('<strong>Fix:</strong> we fix the text at its source in our page generator, never by hand on the live page, test it, and then publish it. We aim to fix anything that changes the meaning or safety information within 2 days, and wording improvements within 7 days.',
   '<strong>Correction :</strong> nous corrigeons le texte à la source, dans notre générateur de pages, jamais à la main sur la page en ligne, nous le testons, puis nous le publions. Nous visons 2 jours pour tout ce qui change le sens ou une information de sécurité, et 7 jours pour les améliorations de formulation.',
   '<strong>Corrección:</strong> corregimos el texto en su origen, en nuestro generador de páginas, nunca a mano en la página publicada, lo probamos y luego lo publicamos. Nuestro objetivo es corregir en 2 días todo lo que cambie el significado o información de seguridad, y en 7 días las mejoras de redacción.',
   '<strong>الإصلاح:</strong> نصحح النص في مصدره داخل مولّد الصفحات لدينا، ولا نعدّل الصفحة المنشورة يدويًا أبدًا، ثم نختبره وننشره. نسعى إلى إصلاح كل ما يغيّر المعنى أو معلومات السلامة خلال يومين، وتحسينات الصياغة خلال 7 أيام.',
   '<strong>Correzione:</strong> correggiamo il testo alla fonte, nel nostro generatore di pagine, mai a mano sulla pagina pubblicata, lo testiamo e poi lo pubblichiamo. Puntiamo a correggere entro 2 giorni tutto ciò che cambia il significato o le informazioni di sicurezza, ed entro 7 giorni i miglioramenti di formulazione.',
   '<strong>תיקון:</strong> אנחנו מתקנים את הטקסט במקור, במחולל הדפים שלנו, ולעולם לא ידנית בדף החי, בודקים אותו ואז מפרסמים. היעד שלנו: תוך יומיים לכל מה שמשנה את המשמעות או מידע בטיחותי, ותוך 7 ימים לשיפורי ניסוח.'),
  ('<strong>Decline politely:</strong> if a suggested change would alter the meaning of the English page or the facts we cite, we explain why we are not making it. Disputes about facts go through our normal source check.',
   '<strong>Refus courtois :</strong> si une modification proposée changeait le sens de la page anglaise ou les faits que nous citons, nous expliquons pourquoi nous ne la faisons pas. Les désaccords sur les faits passent par notre vérification habituelle des sources.',
   '<strong>Rechazo amable:</strong> si un cambio sugerido alterara el significado de la página en inglés o los datos que citamos, te explicamos por qué no lo hacemos. Las dudas sobre los datos pasan por nuestra revisión habitual de fuentes.',
   '<strong>الاعتذار بلطف:</strong> إذا كان التغيير المقترح سيغيّر معنى الصفحة الإنجليزية أو الحقائق التي نستشهد بها، نشرح لك سبب عدم إجرائه. أما الخلافات حول الحقائق فتمر بفحص المصادر المعتاد لدينا.',
   '<strong>Rifiuto cortese:</strong> se una modifica proposta cambiasse il significato della pagina inglese o i fatti che citiamo, ti spieghiamo perché non la facciamo. Le contestazioni sui fatti seguono la nostra normale verifica delle fonti.',
   '<strong>סירוב מנומס:</strong> אם שינוי מוצע ישנה את המשמעות של הדף באנגלית או את העובדות שאנחנו מצטטים, נסביר למה אנחנו לא מבצעים אותו. מחלוקות על עובדות עוברות את בדיקת המקורות הרגילה שלנו.'),
  ('<strong>Log:</strong> we record every correction (page, language, before and after, and date) so the history stays visible.',
   '<strong>Journal :</strong> nous consignons chaque correction (page, langue, avant et après, date) pour que l’historique reste visible.',
   '<strong>Registro:</strong> anotamos cada corrección (página, idioma, antes y después, y fecha) para que el historial siga visible.',
   '<strong>السجل:</strong> نسجّل كل تصحيح (الصفحة واللغة والنص قبل التعديل وبعده والتاريخ) ليبقى السجل واضحًا.',
   '<strong>Registro:</strong> annotiamo ogni correzione (pagina, lingua, prima e dopo, data) perché la cronologia resti visibile.',
   '<strong>תיעוד:</strong> אנחנו מתעדים כל תיקון (דף, שפה, לפני ואחרי ותאריך) כדי שההיסטוריה תישאר גלויה.'),
 ],
 'h_credit': ('Credit: Our Language Partners', 'Remerciements : nos Language Partners', 'Crédito: nuestros Language Partners', 'الشكر: <bdi>Language Partners</bdi>', 'Riconoscimenti: i nostri Language Partners', 'קרדיט: <bdi>Language Partners</bdi> שלנו'),
 'credit': [
  ('Readers who help fix our translations can be thanked in our newsletter as Language Partners. It is opt-in only: when we reply, we ask whether we may thank you by name.',
   'Les lecteurs qui nous aident à corriger nos traductions peuvent être remerciés dans notre lettre d’information comme Language Partners. C’est uniquement avec votre accord : quand nous répondons, nous vous demandons si nous pouvons vous remercier nommément.',
   'Los lectores que nos ayudan a corregir nuestras traducciones pueden aparecer en nuestro boletín como Language Partners. Solo si lo aceptas: cuando respondemos, te preguntamos si podemos agradecerte por tu nombre.',
   'يمكن أن نشكر القراء الذين يساعدوننا في تصحيح ترجماتنا في نشرتنا الإخبارية بصفتهم <bdi>Language Partners</bdi>. ويتم ذلك بموافقتك فقط: عندما نرد، نسألك إن كان بإمكاننا شكرك بالاسم.',
   'I lettori che ci aiutano a correggere le traduzioni possono essere ringraziati nella nostra newsletter come Language Partners. Solo con il tuo consenso: quando rispondiamo, ti chiediamo se possiamo ringraziarti per nome.',
   'קוראים שעוזרים לנו לתקן את התרגומים יכולים לקבל תודה בניוזלטר שלנו כחלק מ-<bdi>Language Partners</bdi>. זה רק בהסכמה: כשאנחנו עונים, אנחנו שואלים אם מותר להודות לכם בשמכם.'),
  ('We print your name or handle exactly as you give it, or “an anonymous reader” if you prefer. You can withdraw at any time.',
   'Nous publions votre nom ou pseudonyme exactement comme vous l’indiquez, ou « un lecteur anonyme » si vous préférez. Vous pouvez retirer votre accord à tout moment.',
   'Publicamos tu nombre o alias tal como nos lo des, o «un lector anónimo» si lo prefieres. Puedes retirar tu permiso en cualquier momento.',
   'ننشر اسمك أو اسمك المستعار كما تكتبه تمامًا، أو «قارئ مجهول» إن فضّلت. ويمكنك سحب موافقتك في أي وقت.',
   'Pubblichiamo il tuo nome o nickname esattamente come ce lo dai, oppure “un lettore anonimo” se preferisci. Puoi ritirare il consenso in qualsiasi momento.',
   'אנחנו מפרסמים את השם או הכינוי בדיוק כפי שמסרתם, או „קורא אנונימי” אם תעדיפו. אפשר לבטל את ההסכמה בכל עת.'),
  ('For children, we use only a first name and country, or keep it anonymous. No photos.',
   'Pour les enfants, nous indiquons seulement le prénom et le pays, ou restons anonymes. Aucune photo.',
   'En el caso de niños y niñas, usamos solo el nombre de pila y el país, o lo dejamos anónimo. Sin fotos.',
   'بالنسبة للأطفال، نذكر الاسم الأول والبلد فقط، أو نُبقي الشكر مجهول الاسم. بلا صور.',
   'Per i bambini usiamo solo il nome e il paese, oppure restiamo anonimi. Nessuna foto.',
   'לילדים אנחנו מציינים רק שם פרטי ומדינה, או שומרים על אנונימיות. בלי תמונות.'),
  ('We never publish email addresses or other personal details.',
   'Nous ne publions jamais d’adresses e-mail ni d’autres données personnelles.',
   'Nunca publicamos direcciones de correo ni otros datos personales.',
   'لا ننشر أبدًا عناوين البريد الإلكتروني أو أي بيانات شخصية أخرى.',
   'Non pubblichiamo mai indirizzi email né altri dati personali.',
   'אנחנו אף פעם לא מפרסמים כתובות דוא״ל או פרטים אישיים אחרים.'),
 ],
 'updated': ('Last updated: October 20, 2026', 'Dernière mise à jour : 20 octobre 2026', 'Última actualización: 20 de octubre de 2026', 'آخر تحديث: 20 أكتوبر 2026', 'Ultimo aggiornamento: 20 ottobre 2026', 'עודכן לאחרונה: 20 באוקטובר 2026'),
 'home': ('Home', 'Accueil', 'Inicio', 'الرئيسية', 'Home', 'דף הבית'),
 'back': ('Report a fact error', 'Signaler une erreur factuelle', 'Reportar un error de datos', 'الإبلاغ عن خطأ في المعلومات', 'Segnala un errore di fatto', 'דיווח על טעות עובדתית'),
 'link_h': ('Translated pages', 'Pages traduites', 'Páginas traducidas', 'الصفحات المترجمة', 'Pagine tradotte', 'דפים מתורגמים'),
 'link_p': ('Found a translation mistake? See how we handle it:', 'Une erreur de traduction ? Voici comment nous la traitons :', '¿Encontraste un error de traducción? Mira cómo lo gestionamos:', 'وجدت خطأ في الترجمة؟ اطّلع على طريقة تعاملنا معه:', 'Hai trovato un errore di traduzione? Ecco come lo gestiamo:', 'מצאתם טעות בתרגום? כך אנחנו מטפלים בה:'),
}
EN_LINK = 'How we handle corrections'
def T(k, L): return P[k][LANGS.index(L)]
def pre(L): return '' if L == 'en' else L + '/'
def fill(s): return s.replace('{t}', TA).replace('{e}', EA)

def note_block(L):
    txt, link = NOTE[L]
    d = ' dir="rtl"' if L in RTL else ''
    return ('<!-- SI-NOTE:START --><aside class="si-note" role="note" lang="%s"%s data-pagefind-ignore '
            'style="max-width:60rem;margin:1.5rem auto;padding:.75rem 1rem;border-radius:10px;background:rgba(255,255,255,.06);font-size:.95rem;line-height:1.6">'
            '<p style="margin:0">%s <a href="Corrections_Policy.html">%s</a></p></aside><!-- SI-NOTE:END -->') % (L, d, fill(txt), link)

def main_html(L):
    st = ''.join('<li>%s</li>' % s[LANGS.index(L)] for s in P['steps'])
    cr = ''.join('<li>%s</li>' % s[LANGS.index(L)] for s in P['credit'])
    return ('<section class="page-hero hero-learn"><div class="page-hero-content"><h1>%s</h1><p>%s</p></div></section>'
            '<nav aria-label="Breadcrumb" class="breadcrumb"><ol><li><a href="index.html">%s</a></li><li><a href="Corrections.html">%s</a></li><li><span aria-current="page">%s</span></li></ol></nav>'
            '<p class="trust-updated">%s</p>'
            '<section class="five-ws" id="write"><h2>%s</h2><p>%s</p></section>'
            '<section class="five-ws" id="steps"><h2>%s</h2><ol>%s</ol></section>'
            '<section class="five-ws" id="credit"><h2>%s</h2><ul>%s</ul></section>'
            '<section class="help-actions"><p><a class="btn" href="Corrections.html#report">%s</a></p></section>') % (
        T('title', L), T('desc', L), T('home', L), CORR_T[L], T('title', L), T('updated', L),
        T('h_write', L), fill(T('write', L)), T('h_steps', L), st, T('h_credit', L), cr, T('back', L))

CORR_T = {}
n_pol = 0
for L in LANGS:
    src = pre(L) + 'Corrections.html'
    if not os.path.exists(src): continue
    s = open(src, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', s, re.S)
    CORR_T[L] = re.sub(r'\s*[:：].*$', '', html.unescape(m.group(1))) if m else 'Corrections'
    bm = re.search(r'aria-current="page">([^<]+)</span></li></ol></nav>', s)
    if bm: CORR_T[L] = bm.group(1)
    # 1) link block on Corrections.html (after the first section)
    blk = ('<!-- CPOL-LINK:START --><section class="five-ws" id="translations"><h2>%s</h2><p>%s <a href="Corrections_Policy.html">%s</a></p></section><!-- CPOL-LINK:END -->'
           % (T('link_h', L), T('link_p', L), T('title', L)))
    o = s
    s = re.sub(r'<!-- CPOL-LINK:START -->.*?<!-- CPOL-LINK:END -->', '', s, flags=re.S)
    i = s.find('</section>', s.find('class="five-ws"'))
    if i > 0: s = s[:i + 10] + blk + s[i + 10:]
    if s != o: open(src, 'w', encoding='utf-8').write(s)
    # 2) policy page from the Corrections shell
    head, rest = s.split('</head>', 1)
    t, d = html.escape(T('title', L) + ' | Saving Planets'), html.escape(T('desc', L))
    head = head.replace('Corrections.html', 'Corrections_Policy.html')
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % t, head, flags=re.S)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title"|property="og:image:alt") content=")[^"]*', lambda m: m.group(1) + t, head)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*', lambda m: m.group(1) + d, head)
    head = head.replace('Corrections_Policy.jpg', 'Corrections.jpg')  # reuse the Corrections share card
    head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "(BreadcrumbList|WebPage)".*?</script>\n?', '', head, flags=re.S)
    nav, after = rest.split('<main id="main">', 1)
    nav = re.sub(r'(class="spn-ls"[^>]*href=")([^"]*?)Corrections\.html', r'\1\2Corrections_Policy.html', nav)
    nav = nav.replace(' aria-current="page"', '', 1) if 'Corrections.html" aria-current="page"' in nav else nav
    tail = after[after.index('</main>'):]
    out = head + '</head>' + nav + '<main id="main">\n' + main_html(L) + '\n' + tail
    dst = pre(L) + 'Corrections_Policy.html'
    if not os.path.exists(dst) or open(dst, encoding='utf-8').read() != out:
        open(dst, 'w', encoding='utf-8').write(out); n_pol += 1
# 3) reader note on every translated page (fr/es/ar/it/he); replaces the old Hebrew-only HE-SI-NOTE
RX = re.compile(r'<!-- (?:HE-)?SI-NOTE:START -->.*?<!-- (?:HE-)?SI-NOTE:END -->\n?', re.S)
n = 0
for L in NOTE:
    nb = note_block(L)
    for p in sorted(glob.glob(L + '/*.html')):
        s = open(p, encoding='utf-8').read(); o = s
        if 'http-equiv="refresh"' in s[:3000]: continue
        s = RX.sub('', s)
        if '<footer' in s:
            i = s.rfind('<footer'); s = s[:i] + nb + '\n' + s[i:]
        if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print(f'corrections-policy: {n_pol} policy pages, {n} translated pages with reader note')
