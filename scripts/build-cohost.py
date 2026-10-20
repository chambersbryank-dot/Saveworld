#!/usr/bin/env python3
"""Oct 16: "Co-host with us" section on About (#cohost) + homepage teaser link, all 5 langs.
Idempotent marker blocks COHOST / COHOST-TEASER. Counts come from the repo (English pages, solutions.json)."""
import json, glob, os, re, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PAGES = min(len(glob.glob(d + '*.html')) for d in ['', 'fr/', 'es/', 'ar/', 'it/'] + (['he/'] if os.path.exists('he/About.html') else [])) // 100 * 100  # 'more than N', true in every PUBLIC language (Oct 17: he/ is partial, not counted)
SOL = json.load(open('assets/data/solutions.json'))['site']['solutions']
MAIL = 'media@savingplanets.com'
T = {
 'en': dict(h='Co-host with us', subj='Co-host request: Biological SI Partner and SI',
  intro=f'Saving Planets was built by a Biological SI Partner working with SI: more than {PAGES} pages in each of six languages and {SOL} solutions, free, with no ads on learning pages. We would love to co-host a conversation about how that partnership works, and what it means for education.',
  who_h='Who we co-host with', who=['Podcasts and radio','Schools, teachers and universities','Webinars and conferences','Journalists and media'],
  top_h='Conversation topics', top=['The human and SI workflow, step by step','Guardrails: every fact sourced, no invented facts, human approval before anything is published or sent','Multilingual education at scale (English, French, Spanish, Arabic, Italian, Hebrew)','Lessons for teachers and students using SI well'],
  ask_h='Get in touch', ask='Tell us about your show, class or event, your audience and a few possible dates.', btn='Invite us to co-host',
  teaser='Host a podcast, class or event? Co-host a conversation with us about how a Biological SI Partner and SI built this site.', tlink='Co-host with us'),
 'fr': dict(h='Coanimez avec nous', subj="Demande de coanimation : Partenaire SI Biologique et SI",
  intro=f"Saving Planets a été construit par un Partenaire SI Biologique travaillant avec une SI : plus de {PAGES} pages dans chacune des six langues et {SOL} solutions, gratuit, sans publicité sur les pages d'apprentissage. Nous serions ravis de coanimer une conversation sur le fonctionnement de ce partenariat et ce qu'il signifie pour l'éducation.",
  who_h='Avec qui nous coanimons', who=['Podcasts et radio','Écoles, enseignants et universités','Webinaires et conférences','Journalistes et médias'],
  top_h='Thèmes de discussion', top=["Le travail entre l'humain et la SI, étape par étape","Garde-fous : chaque fait sourcé, aucun fait inventé, validation humaine avant toute publication ou tout envoi","L'éducation multilingue à grande échelle (anglais, français, espagnol, arabe, italien, hébreu)","Leçons pour les enseignants et les élèves qui utilisent bien la SI"],
  ask_h='Nous contacter', ask='Parlez-nous de votre émission, de votre classe ou de votre événement, de votre public et de quelques dates possibles.', btn='Invitez-nous à coanimer',
  teaser="Vous animez un podcast, un cours ou un événement ? Coanimez avec nous une conversation sur la façon dont un Partenaire SI Biologique et une SI ont construit ce site.", tlink='Coanimez avec nous'),
 'es': dict(h='Copresenta con nosotros', subj='Solicitud de copresentación: Socio SI Biológico y SI',
  intro=f'Saving Planets fue creado por un Socio SI Biológico que trabaja con SI: más de {PAGES} páginas en cada uno de los seis idiomas y {SOL} soluciones, gratis y sin anuncios en las páginas de aprendizaje. Nos encantaría copresentar una conversación sobre cómo funciona esta colaboración y lo que significa para la educación.',
  who_h='Con quién copresentamos', who=['Pódcasts y radio','Escuelas, docentes y universidades','Seminarios web y congresos','Periodistas y medios'],
  top_h='Temas de conversación', top=['El flujo de trabajo entre la persona y la SI, paso a paso','Salvaguardas: cada dato con fuente, ningún dato inventado, aprobación humana antes de publicar o enviar nada','Educación multilingüe a gran escala (inglés, francés, español, árabe, italiano, hebreo)','Lecciones para docentes y estudiantes que usan bien la SI'],
  ask_h='Contáctanos', ask='Cuéntanos sobre tu programa, clase o evento, tu público y algunas fechas posibles.', btn='Invítanos a copresentar',
  teaser='¿Presentas un pódcast, una clase o un evento? Copresenta con nosotros una conversación sobre cómo un Socio SI Biológico y la SI crearon este sitio.', tlink='Copresenta con nosotros'),
 'ar': dict(h='شاركنا التقديم', subj='طلب مشاركة في التقديم: الشريك البيولوجي و SI',
  intro=f'بُني موقع Saving Planets على يد شريك بيولوجي يعمل مع SI: أكثر من {PAGES} صفحة بكل لغة من اللغات الست و{SOL} حلاً، مجاناً ودون إعلانات في صفحات التعلّم. يسعدنا أن نشارك في تقديم حوار حول كيفية عمل هذه الشراكة وما تعنيه للتعليم.',
  who_h='مع من نشارك في التقديم', who=['البودكاست والإذاعة','المدارس والمعلمون والجامعات','الندوات عبر الإنترنت والمؤتمرات','الصحفيون ووسائل الإعلام'],
  top_h='مواضيع الحوار', top=['سير العمل بين الإنسان و SI خطوة بخطوة','الضوابط: كل معلومة موثقة بمصدر، لا معلومات مختلقة، وموافقة بشرية قبل نشر أو إرسال أي شيء','التعليم متعدد اللغات على نطاق واسع (الإنجليزية والفرنسية والإسبانية والعربية والإيطالية والعبرية)','دروس للمعلمين والطلاب لاستخدام SI بشكل جيد'],
  ask_h='تواصل معنا', ask='أخبرنا عن برنامجك أو صفك أو فعاليتك، وعن جمهورك وبعض المواعيد الممكنة.', btn='ادعنا للمشاركة في التقديم',
  teaser='هل تقدّم بودكاست أو درساً أو فعالية؟ شاركنا تقديم حوار حول كيف بنى شريك بيولوجي و SI هذا الموقع.', tlink='شاركنا التقديم'),
 'it': dict(h='Conduci con noi', subj='Richiesta di co-conduzione: Partner SI Biologico e SI',
  intro=f"Saving Planets è stato creato da un Partner SI Biologico che lavora con la SI: oltre {PAGES} pagine in ciascuna delle sei lingue e {SOL} soluzioni, gratis e senza pubblicità nelle pagine di apprendimento. Ci piacerebbe co-condurre una conversazione su come funziona questa collaborazione e cosa significa per l'istruzione.",
  who_h='Con chi co-conduciamo', who=['Podcast e radio','Scuole, insegnanti e università','Webinar e conferenze','Giornalisti e media'],
  top_h='Temi di conversazione', top=["Il flusso di lavoro tra persona e SI, passo dopo passo","Garanzie: ogni fatto con una fonte, nessun fatto inventato, approvazione umana prima di pubblicare o inviare qualsiasi cosa","Istruzione multilingue su larga scala (inglese, francese, spagnolo, arabo, italiano, ebraico)","Lezioni per insegnanti e studenti che usano bene la SI"],
  ask_h='Contattaci', ask='Raccontaci del tuo programma, corso o evento, del tuo pubblico e di alcune date possibili.', btn='Invitaci a co-condurre',
  teaser='Conduci un podcast, un corso o un evento? Co-conduci con noi una conversazione su come un Partner SI Biologico e la SI hanno creato questo sito.', tlink='Conduci con noi'),
 'he': dict(h='הנחו איתנו', subj='בקשה להנחיה משותפת: שותף SI ביולוגי ו-SI',
  intro=f'Saving Planets נבנה על ידי שותף SI ביולוגי שעובד עם SI (בינה סינתטית): יותר מ-{PAGES} דפים בכל אחת משש שפות ו-{SOL} פתרונות, בחינם, ללא פרסומות בדפי הלמידה. נשמח להנחות יחד שיחה על האופן שבו השותפות הזו עובדת, ומה משמעותה לחינוך.',
  who_h='עם מי אנחנו מנחים', who=['פודקאסטים ורדיו','בתי ספר, מורים ואוניברסיטאות','וובינרים וכנסים','עיתונאים ומדיה'],
  top_h='נושאים לשיחה', top=['תהליך העבודה בין האדם ל-SI, צעד אחר צעד','מעקות בטיחות: לכל עובדה יש מקור, אין עובדות מומצאות, ואישור אנושי לפני שמשהו מתפרסם או נשלח','חינוך רב-לשוני בקנה מידה גדול (אנגלית, צרפתית, ספרדית, ערבית, איטלקית, עברית)','שיעורים למורים ולתלמידים שמשתמשים ב-SI היטב'],
  ask_h='צרו קשר', ask='ספרו לנו על התוכנית, הכיתה או האירוע שלכם, על הקהל שלכם ועל כמה תאריכים אפשריים.', btn='הזמינו אותנו להנחות יחד',
  teaser='מנחים פודקאסט, שיעור או אירוע? הנחו איתנו שיחה על האופן שבו שותף SI ביולוגי ו-SI (בינה סינתטית) בנו את האתר הזה.', tlink='הנחו איתנו'),
}
# Oct 17: biosipartner@ Cc line right after media@ (strings shared with build-biosi-cc.py)
CC = {'en': ('Feel free to Cc: our Biological SI Partner at', 'He or she will reach out to you within 24 hours.')}
CC.update(json.load(open(os.path.join(ROOT, 'i18n', 'biosi-cc.json'), encoding='utf8')))
CCA = '<a href="mailto:biosipartner@savingplanets.com?subject=Cc%3A%20Biological%20SI%20Partner">biosipartner@savingplanets.com</a>'
def ul(xs): return '<ul class="partner-list">' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'
def put(s, name, block, after):
    s = re.sub(rf'<!-- {name}:START -->.*?<!-- {name}:END -->', '', s, flags=re.S)
    i = s.find(after)
    if i < 0: return None
    i += len(after)
    return s[:i] + f'<!-- {name}:START -->{block}<!-- {name}:END -->' + s[i:]
for lang, t in T.items():
    pre = '' if lang == 'en' else lang + '/'
    if lang != 'en' and not os.path.exists(pre + 'About.html'): continue  # Oct 17: Hebrew is built only once its pages exist
    href = f'mailto:{MAIL}?subject=' + urllib.parse.quote(t['subj'])
    sec = (f'<section class="five-ws" id="cohost"><h2>{t["h"]}</h2><p class="src-intro">{t["intro"]}</p><div class="ws-grid">'
           f'<div class="w-card"><h3>{t["who_h"]}</h3>{ul(t["who"])}</div>'
           f'<div class="w-card"><h3>{t["top_h"]}</h3>{ul(t["top"])}</div>'
           f'<div class="w-card"><h3>{t["ask_h"]}</h3><p>{t["ask"]}</p><p><a href="{href}">{MAIL}</a></p>'
           f'<p class="biosi-cc">{CC[lang][0]} {CCA}. <span>{CC[lang][1]}</span></p>'
           f'<p class="partner-cta"><a class="btn-nav" href="{href}">{t["btn"]}</a></p></div></div></section>')
    p = pre + 'About.html'; s = open(p).read()
    n = put(s, 'COHOST', sec, '<!-- PARTNER:END -->')
    if n is None: print('skip', p, '(no PARTNER block)')
    else: open(p, 'w').write(n)
    p = pre + 'index.html'; s = open(p).read()
    tz = f'<p class="src-intro" id="cohost-teaser">{t["teaser"]} <a href="About.html#cohost">{t["tlink"]}</a></p>'
    n = put(s, 'COHOST-TEASER', tz, '<!-- PARTNER-TEASER:START --><section class="five-ws" id="partner-teaser">')
    if n is not None:
        # place after the teaser intro paragraph, before the CTA
        n = re.sub(r'(<!-- COHOST-TEASER:START -->.*?<!-- COHOST-TEASER:END -->)(<h2>.*?</h2><p class="src-intro">.*?</p>)', r'\2\1', n, count=1, flags=re.S)
        open(p, 'w').write(n)
    else: print('skip', p)
print('cohost: pages', PAGES, 'solutions', SOL)
