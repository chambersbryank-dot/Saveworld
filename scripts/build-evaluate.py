#!/usr/bin/env python3
"""How we evaluate solutions, in all 6 languages.

Nov 2 2026 (Bryan-approved). Based on the Oct 28 feature policy: judged on its own
record; genuine, independent, and financially transparent; Donate links only to
audited or rated charities. Public text says "certain sanctioned countries" and
names none. The team/advisors layout is in the page but hidden until Bryan sends
real names. No invented people. Saturn hero and analytics unchanged.
"""
import os, re, html, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
PAGE = 'How_We_Evaluate.html'
E = lambda s: html.escape(s, quote=True)
NOTE = {
 'fr': 'Traduction rédigée par machine, à relire.',
 'es': 'Traducción hecha por máquina, pendiente de revisión.',
 'ar': 'ترجمة آلية بانتظار المراجعة.',
 'it': 'Traduzione automatica, da rivedere.',
 'he': 'תרגום מכונה, ממתין לבדיקה.',
}
COPY = {
 'en': {
  'title': 'How We Evaluate Solutions',
  'desc': 'How Saving Planets decides what to feature: the project’s own record, real work, open finances, and Donate links only to audited or rated charities.',
  'kicker': 'We look at the work itself. A 10-year-old can follow these rules.',
  'secs': [
   ('Judged on its own record', 'We judge each effort on its own record, not on the government of the country where the work happens. A good project in a difficult place can still be shown. A famous name with no real work cannot.'),
   ('Genuine, independent, and financially transparent', 'The group should do the work itself: clean up, plant, restore, or run the hardware. It should be independent, and it should say clearly how it uses money. We cite a source for every fact.'),
   ('Donate links', 'A Donate link goes only to an organization that publishes audited finances or has a recognized charity rating. Your gift should reach the work, not get lost. Featuring a project does not mean we are partners or that we endorse it.'),
   ('Certain sanctioned countries', 'We do not link Donate buttons, and we do not connect our pages, to government or operator sites of certain sanctioned countries. We do not name those countries on this page. A project is still judged on its own record.'),
  ],
  'team_h': 'Team and advisors',
  'team_p': 'This section stays hidden until Bryan sends the real names. No names are invented here.',
  'roles': ['Founder', 'Advisor', 'Advisor'],
  'needed': 'Name needed from Bryan',
  'link': 'How we evaluate solutions',
 },
 'fr': {
  'title': 'Comment nous évaluons les solutions',
  'desc': 'Comment Saving Planets choisit ce qu’il présente : le bilan propre du projet, un vrai travail, des finances claires, et des liens Donner seulement vers des organismes audités ou notés.',
  'kicker': 'Nous regardons le travail lui-même. Un enfant de 10 ans peut suivre ces règles.',
  'secs': [
   ('Jugé sur son propre bilan', 'Nous jugeons chaque effort sur son propre bilan, pas sur le gouvernement du pays où le travail se fait. Un bon projet dans un endroit difficile peut être montré. Un nom célèbre sans vrai travail, non.'),
   ('Sérieux, indépendant et transparent sur l’argent', 'Le groupe doit faire le travail : nettoyer, planter, restaurer ou faire tourner le matériel. Il doit être indépendant et dire clairement comment il utilise l’argent. Chaque fait a une source.'),
   ('Liens Donner', 'Un lien Donner ne mène qu’à un organisme qui publie des comptes audités ou qui a une note d’association reconnue. Votre don doit arriver au travail. Présenter un projet ne veut pas dire que nous sommes partenaires ni que nous le recommandons.'),
   ('Certains pays sanctionnés', 'Nous ne mettons pas de lien Donner, et nous ne relions pas nos pages, vers les sites de gouvernements ou d’opérateurs de certains pays sanctionnés. Nous ne nommons pas ces pays sur cette page. Un projet est quand même jugé sur son propre bilan.'),
  ],
  'team_h': 'Équipe et conseillers',
  'team_p': 'Cette section reste cachée jusqu’à ce que Bryan envoie les vrais noms. Aucun nom n’est inventé ici.',
  'roles': ['Fondateur', 'Conseiller', 'Conseiller'],
  'needed': 'Nom attendu de Bryan',
  'link': 'Comment nous évaluons les solutions',
 },
 'es': {
  'title': 'Cómo evaluamos las soluciones',
  'desc': 'Cómo Saving Planets decide qué mostrar: el propio historial del proyecto, trabajo real, finanzas claras, y enlaces de donación solo a organizaciones auditadas o calificadas.',
  'kicker': 'Miramos el trabajo en sí. Un niño de 10 años puede seguir estas reglas.',
  'secs': [
   ('Se juzga por su propio historial', 'Juzgamos cada esfuerzo por su propio historial, no por el gobierno del país donde se hace el trabajo. Un buen proyecto en un lugar difícil puede mostrarse. Un nombre famoso sin trabajo real, no.'),
   ('Genuino, independiente y transparente con el dinero', 'El grupo debe hacer el trabajo: limpiar, plantar, restaurar o hacer funcionar el equipo. Debe ser independiente y decir con claridad cómo usa el dinero. Cada dato tiene una fuente.'),
   ('Enlaces de donación', 'Un enlace de Donar solo lleva a una organización que publica finanzas auditadas o tiene una calificación de caridad reconocida. Tu regalo debe llegar al trabajo. Mostrar un proyecto no significa que seamos socios ni que lo respaldemos.'),
   ('Ciertos países sancionados', 'No ponemos enlaces de Donar, ni conectamos nuestras páginas, con sitios de gobiernos u operadores de ciertos países sancionados. No nombramos esos países en esta página. Un proyecto se juzga igual por su propio historial.'),
  ],
  'team_h': 'Equipo y asesores',
  'team_p': 'Esta sección sigue oculta hasta que Bryan envíe los nombres reales. Aquí no se inventa ningún nombre.',
  'roles': ['Fundador', 'Asesor', 'Asesor'],
  'needed': 'Nombre pendiente de Bryan',
  'link': 'Cómo evaluamos las soluciones',
 },
 'ar': {
  'title': 'كيف نقيّم الحلول',
  'desc': 'كيف تقرر Saving Planets ما تعرضه: سجل المشروع نفسه، وعمل حقيقي، وشفافية مالية، وروابط تبرع فقط لمنظمات مدققة أو مصنّفة.',
  'kicker': 'ننظر إلى العمل نفسه. طفل في العاشرة يستطيع أن يتبع هذه القواعد.',
  'secs': [
   ('يُحكم عليه بسجله هو', 'نحكم على كل جهد بسجله هو، لا بحكومة البلد الذي يجري فيه العمل. مشروع جيد في مكان صعب يمكن عرضه. اسم مشهور بلا عمل حقيقي لا يُعرض.'),
   ('حقيقي ومستقل وواضح في المال', 'يجب أن تقوم الجهة بالعمل: تنظيف أو زراعة أو ترميم أو تشغيل المعدات. وأن تكون مستقلة وتقول بوضوح كيف تستخدم المال. كل حقيقة لها مصدر.'),
   ('روابط التبرع', 'رابط التبرع يذهب فقط إلى منظمة تنشر حسابات مدققة أو تحمل تصنيفًا خيريًا معروفًا. يجب أن تصل هديتك إلى العمل. عرض مشروع لا يعني أننا شركاء ولا أننا نؤيده.'),
   ('بلدان معينة خاضعة لعقوبات', 'لا نضع روابط تبرع، ولا نربط صفحاتنا، بمواقع حكومات أو مشغّلين لبلدان معينة خاضعة لعقوبات. لا نسمّي تلك البلدان في هذه الصفحة. ويبقى المشروع محكومًا بسجله هو.'),
  ],
  'team_h': 'الفريق والمستشارون',
  'team_p': 'يبقى هذا القسم مخفيًا إلى أن يرسل براين الأسماء الحقيقية. لا أسماء مخترعة هنا.',
  'roles': ['المؤسس', 'مستشار', 'مستشار'],
  'needed': 'الاسم مطلوب من براين',
  'link': 'كيف نقيّم الحلول',
 },
 'it': {
  'title': 'Come valutiamo le soluzioni',
  'desc': 'Come Saving Planets decide cosa mostrare: il bilancio del progetto, lavoro vero, finanze chiare, e link Dona solo a enti con conti certificati o una valutazione riconosciuta.',
  'kicker': 'Guardiamo il lavoro stesso. Un bambino di 10 anni può seguire queste regole.',
  'secs': [
   ('Giudicato sulla sua storia', 'Giudichiamo ogni impegno sulla sua storia, non sul governo del paese in cui avviene il lavoro. Un buon progetto in un posto difficile può essere mostrato. Un nome famoso senza lavoro vero, no.'),
   ('Genuino, indipendente e trasparente sui soldi', 'Il gruppo deve fare il lavoro: pulire, piantare, restaurare o far funzionare le macchine. Deve essere indipendente e dire chiaramente come usa i soldi. Ogni fatto ha una fonte.'),
   ('Link per donare', 'Un link Dona porta solo a un’organizzazione che pubblica conti certificati o ha una valutazione di ente di beneficenza riconosciuta. Il tuo regalo deve arrivare al lavoro. Mostrare un progetto non significa che siamo partner né che lo appoggiamo.'),
   ('Alcuni paesi sanzionati', 'Non mettiamo link Dona, e non colleghiamo le nostre pagine, ai siti di governi o operatori di alcuni paesi sanzionati. Non nominiamo quei paesi in questa pagina. Un progetto è comunque giudicato sulla sua storia.'),
  ],
  'team_h': 'Team e consulenti',
  'team_p': 'Questa sezione resta nascosta finché Bryan non manda i nomi veri. Qui non si inventa nessun nome.',
  'roles': ['Fondatore', 'Consulente', 'Consulente'],
  'needed': 'Nome atteso da Bryan',
  'link': 'Come valutiamo le soluzioni',
 },
 'he': {
  'title': 'איך אנחנו מעריכים פתרונות',
  'desc': 'איך Saving Planets מחליטה מה להציג: הרקורד של המיזם עצמו, עבודה אמיתית, כספים גלויים, וקישורי תרומה רק לארגונים מבוקרים או מדורגים.',
  'kicker': 'אנחנו מסתכלים על העבודה עצמה. ילד בן 10 יכול לעקוב אחרי הכללים האלה.',
  'secs': [
   ('נשפט לפי הרקורד שלו', 'אנחנו שופטים כל מאמץ לפי הרקורד שלו, לא לפי הממשלה של המדינה שבה העבודה קורית. מיזם טוב במקום קשה יכול להופיע. שם מפורסם בלי עבודה אמיתית לא.'),
   ('אמיתי, עצמאי ושקוף בכסף', 'הקבוצה צריכה לעשות את העבודה: לנקות, לשתול, לשקם או להפעיל את הציוד. היא צריכה להיות עצמאית ולומר בבירור איך היא משתמשת בכסף. לכל עובדה יש מקור.'),
   ('קישורי תרומה', 'קישור תרומה מוביל רק לארגון שמפרסם דוחות מבוקרים או שיש לו דירוג צדקה מוכר. המתנה צריכה להגיע לעבודה. הצגת מיזם לא אומרת שאנחנו שותפים או שאנחנו ממליצים עליו.'),
   ('מדינות מסוימות תחת סנקציות', 'אנחנו לא שמים קישורי תרומה, ולא מחברים את העמודים שלנו, לאתרי ממשלה או מפעילים של מדינות מסוימות תחת סנקציות. אנחנו לא מציינים את שמות המדינות בעמוד הזה. מיזם עדיין נשפט לפי הרקורד שלו.'),
  ],
  'team_h': 'צוות ויועצים',
  'team_p': 'המקטע הזה נשאר מוסתר עד שבריאן שולח את השמות האמיתיים. אין כאן שמות מומצאים.',
  'roles': ['מייסד', 'יועץ', 'יועץ'],
  'needed': 'שם נדרש מבריאן',
  'link': 'איך אנחנו מעריכים פתרונות',
 },
}

def path(lang):
    return PAGE if lang == 'en' else f'{lang}/{PAGE}'

def main_html(lang):
    t = COPY[lang]
    note = f'<p class="lnote" role="note"><small>🤖 {E(NOTE[lang])}</small></p>' if lang != 'en' else ''
    secs = ''.join(f'<section class="five-ws" id="s{i}"><h2>{E(h)}</h2><p>{E(p)}</p></section>' for i, (h, p) in enumerate(t['secs'], 1))
    roles = ''.join(f'<li><p class="crs-kicker">{E(role)}</p><p>{E(t["needed"])}</p></li>' for role in t['roles'])
    team = (f'<section class="five-ws" id="team" hidden><h2>{E(t["team_h"])}</h2><p>{E(t["team_p"])}</p>'
            f'<ul class="crs-grid">{roles}</ul></section>')
    hero = (f'<section class="page-hero hero-learn"><div class="page-hero-content"><h1>{E(t["title"])}</h1>'
            f'<p>{E(t["kicker"])}</p></div></section>\n')
    return hero + f'<div class="lw">{note}{secs}{team}<p><a href="About.html#feature-policy">{E(t["link"])}</a></p></div>\n'

def write_pages():
    spec = importlib.util.spec_from_file_location('bl', 'scripts/build-learn.py')
    BL = importlib.util.module_from_spec(spec); spec.loader.exec_module(BL)
    he = f'<link rel="alternate" hreflang="he" href="https://www.savingplanets.com/he/{PAGE}">'
    for lang in LANGS:
        t = COPY[lang]
        page = BL.shell(lang, PAGE, t['title'], t['desc'], main_html(lang), ld_type='WebPage')
        head, rest = page.split('</head>', 1)
        if 'hreflang="he"' not in head:
            head = head.replace('<link rel="alternate" hreflang="x-default"', he + '\n<link rel="alternate" hreflang="x-default"', 1)
        img_lang = lang if os.path.exists(f'assets/og/{lang}/About.jpg') else 'en'
        img = f'https://www.savingplanets.com/assets/og/{img_lang}/About.jpg'
        page = head + '</head>' + rest
        page = re.sub(r'(<meta property="og:image" content=")[^"]*"', r'\1' + img + '"', page, count=1)
        page = re.sub(r'(<meta name="twitter:image" content=")[^"]*"', r'\1' + img + '"', page, count=1)
        page = re.sub(r'(<meta property="og:image:alt" content=")[^"]*"', r'\1' + E(t['title']) + '"', page, count=1)
        # WebPage from shell may still say LearningResource fields; leave shell's JSON-LD (WebPage requested).
        open(path(lang), 'w', encoding='utf-8').write(page)

def link_about():
    for lang in LANGS:
        f = 'About.html' if lang == 'en' else f'{lang}/About.html'
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'<!-- EVALINK:START -->.*?<!-- EVALINK:END -->', '', s, flags=re.S)
        link = (f'<!-- EVALINK:START --><p class="feat-policy-link"><a href="{PAGE}">{E(COPY[lang]["link"])}</a></p><!-- EVALINK:END -->')
        if '<!-- FEATPOL:END -->' not in s: raise SystemExit(f'no feature policy on {f}')
        s = s.replace('<!-- FEATPOL:END -->', '<!-- FEATPOL:END -->' + link, 1)
        open(f, 'w', encoding='utf-8').write(s)

def sitemap():
    sm = open('sitemap.xml', encoding='utf-8').read()
    if PAGE in sm: return
    def repl(m):
        return m.group(0) + m.group(0).replace('About.html', PAGE)
    sm2, n = re.subn(r'  <url><loc>https://www\.savingplanets\.com/(?:[a-z]{2}/)?About\.html</loc>.*?</url>\n', repl, sm)
    if n < 6: raise SystemExit(f'sitemap About entries: {n}')
    open('sitemap.xml', 'w', encoding='utf-8').write(sm2)

def apply():
    write_pages()
    link_about()
    sitemap()
    # refuse invented personal names
    banned = ('Bryan Chambers', 'Dr. ', 'Professor ')
    for lang in LANGS:
        text = open(path(lang), encoding='utf-8').read()
        if 'id="team" hidden' not in text: raise SystemExit('team section must stay hidden')
        for b in banned:
            if b in text: raise SystemExit(f'unexpected name-like text {b!r} in {lang}')
    print('evaluate: 6 pages, About links, sitemap, team hidden')

if __name__ == '__main__':
    apply()
