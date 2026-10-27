#!/usr/bin/env python3
"""Oct 26 2026 (founder): Big_Questions.html — question-shaped search landing page in all 6 langs.
Honest, cited answers (NASA, NOAA, IPCC, ESA, EPA) to high-intent queries like 'is the planet dying?'
and 'what organizations help save the planet?'. FAQPage JSON-LD, hreflang, internal links to solution
pages only. No orgs led by Russia/China/North Korea/Iran named as helpers. Say SI, not AI.
Usage: python3 scripts/build-big-questions.py
Run before seo-fix / i18n-sitemap / build-nav in weekly-sync (or alone for this PR)."""
import html, json, os, re, datetime
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = 'https://www.savingplanets.com/'
PAGE = 'Big_Questions.html'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
LOCALE = {'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES', 'ar': 'ar_AR', 'it': 'it_IT', 'he': 'he_IL'}
RTL = {'ar', 'he'}
TODAY = '2026-10-26'
N = json.load(open('assets/data/solutions.json', encoding='utf8'))['site']['solutions']
H = json.load(open('assets/data/solutions.json', encoding='utf8'))['site']['hubs']

def T(en, fr, es, ar, it, he):
    return {'en': en, 'fr': fr, 'es': es, 'ar': ar, 'it': it, 'he': he}

def esc(s): return html.escape(s, quote=False)
def escq(s): return html.escape(s, quote=True)
def d(l): return '' if l == 'en' else l + '/'
def path(l): return PAGE if l == 'en' else f'{l}/{PAGE}'
def url(l): return SITE + d(l) + PAGE

# UI chrome
UI = {
 'title': T(
  'Big Questions About Our Planet | Saving Planets',
  'Grandes questions sur notre planète | Saving Planets',
  'Grandes preguntas sobre nuestro planeta | Saving Planets',
  'أسئلة كبيرة عن كوكبنا | Saving Planets',
  'Le grandi domande sul nostro pianeta | Saving Planets',
  'שאלות גדולות על כדור הארץ שלנו | Saving Planets'),
 'desc': T(
  f'Honest, sourced answers to big questions about Earth and climate: is the planet dying, will Earth be gone in ten years, who is helping, and what you can do. {N} real solutions across {H} hubs.',
  f'Réponses honnêtes et sourcées aux grandes questions sur la Terre et le climat : la planète meurt-elle, la Terre disparaîtra-t-elle en dix ans, qui aide, et que pouvez-vous faire. {N} vraies solutions dans {H} pôles.',
  f'Respuestas honestas y con fuentes a grandes preguntas sobre la Tierra y el clima: ¿está muriendo el planeta, desaparecerá la Tierra en diez años, quién ayuda y qué puedes hacer. {N} soluciones reales en {H} ejes.',
  f'إجابات صادقة وموثّقة بالمصادر عن أسئلة كبيرة حول الأرض والمناخ: هل الكوكب يموت، وهل ستختفي الأرض خلال عشر سنوات، ومن يساعد، وماذا يمكنك أن تفعل. {N} حلاً حقيقياً عبر {H} محاور.',
  f'Risposte oneste e con fonti alle grandi domande su Terra e clima: il pianeta sta morendo, la Terra sparirà in dieci anni, chi aiuta e cosa puoi fare. {N} soluzioni reali in {H} hub.',
  f'תשובות כנות ומבוססות מקורות לשאלות גדולות על כדור הארץ והאקלים: האם הכוכב מת, האם כדור הארץ ייעלם בעשר שנים, מי עוזר ומה אפשר לעשות. {N} פתרונות אמיתיים ב-{H} מרכזים.'),
 'h1': T('Big Questions About Our Planet', 'Grandes questions sur notre planète', 'Grandes preguntas sobre nuestro planeta', 'أسئلة كبيرة عن كوكبنا', 'Le grandi domande sul nostro pianeta', 'שאלות גדולות על כדור הארץ שלנו'),
 'sub': T(
  'People ask hard questions about Earth. We answer with NASA, NOAA, IPCC and ESA sources — hopeful where the evidence is, honest where the work is not done.',
  'Les gens posent des questions difficiles sur la Terre. Nous répondons avec des sources NASA, NOAA, GIEC et ESA — espérés là où les preuves le sont, honnêtes là où le travail n’est pas fini.',
  'La gente hace preguntas difíciles sobre la Tierra. Respondemos con fuentes de la NASA, la NOAA, el IPCC y la ESA: esperanzadoras donde lo dice la evidencia, honestas donde el trabajo no está hecho.',
  'يطرح الناس أسئلة صعبة عن الأرض. نجيب بمصادر من ناسا وNOAA والهيئة الحكومية الدولية المعنية بتغير المناخ ووكالة الفضاء الأوروبية — بأمل حيث تدعم الأدلة ذلك، وبصدق حيث لم يكتمل العمل بعد.',
  'Le persone fanno domande difficili sulla Terra. Rispondiamo con fonti NASA, NOAA, IPCC ed ESA: speranzose dove lo dice l’evidenza, oneste dove il lavoro non è finito.',
  'אנשים שואלים שאלות קשות על כדור הארץ. אנחנו עונים עם מקורות של NASA, NOAA, IPCC ו-ESA — בתקווה במקום שהראיות תומכות, ובכנות במקום שהעבודה עדיין לא הושלמה.'),
 'src': T('Sources', 'Sources', 'Fuentes', 'المصادر', 'Fonti', 'מקורות'),
 'more': T('On Saving Planets', 'Sur Saving Planets', 'En Saving Planets', 'على Saving Planets', 'Su Saving Planets', 'ב-Saving Planets'),
 'credit': T('Created by SI and Biological SI Partner', 'Créé par SI et Biological SI Partner', 'Creado por SI y Biological SI Partner', 'من إعداد SI وBiological SI Partner', 'Creato da SI e Biological SI Partner', 'נוצר על ידי SI ו-Biological SI Partner'),
 'updated': T(f'Last checked against sources: {TODAY}', f'Dernière vérification des sources : {TODAY}', f'Última comprobación de fuentes: {TODAY}', f'آخر تحقق من المصادر: {TODAY}', f'Ultimo controllo delle fonti: {TODAY}', f'בדיקת מקורות אחרונה: {TODAY}'),
 'nav': T('Big Questions', 'Grandes questions', 'Grandes preguntas', 'أسئلة كبيرة', 'Grandi domande', 'שאלות גדולות'),
}

# Each Q: id, q(T), a(T paragraphs list), sources[(title,url)], links[(href,label T)]
# Helper orgs: NASA, NOAA, ESA, USGS, EPA, IPCC (UN science body), + site nonprofits already featured — never RU/CN/KP/IR-led.
Q = []

def add(id, q, a, sources, links):
    Q.append(dict(id=id, q=q, a=a, sources=sources, links=links))

add('orgs-helping',
 T('What organizations are helping save our planet?',
   'Quelles organisations aident à sauver notre planète ?',
   '¿Qué organizaciones ayudan a salvar nuestro planeta?',
   'ما المنظمات التي تساعد في إنقاذ كوكبنا؟',
   'Quali organizzazioni aiutano a salvare il nostro pianeta?',
   'אילו ארגונים עוזרים להציל את כדור הארץ שלנו?'),
 [T(f'Many groups are already doing measurable work. On Saving Planets we document {N} real solutions across {H} hubs — agencies such as NASA, NOAA, ESA and USGS that watch Earth from space and the ground; government programs; and nonprofits that clean oceans, restore forests and rivers, and protect wildlife. Every solution page lists who does the work, the published numbers, and a path to donate or join when one exists.',
   f'De nombreux groupes font déjà un travail mesurable. Sur Saving Planets, nous documentons {N} vraies solutions dans {H} pôles — des agences comme la NASA, la NOAA, l’ESA et l’USGS qui observent la Terre depuis l’espace et le sol ; des programmes publics ; et des associations qui nettoient les océans, restaurent forêts et rivières, et protègent la faune. Chaque page de solution indique qui fait le travail, les chiffres publiés, et un moyen de donner ou de rejoindre le projet quand il existe.',
   f'Muchos grupos ya hacen un trabajo medible. En Saving Planets documentamos {N} soluciones reales en {H} ejes: agencias como la NASA, la NOAA, la ESA y el USGS que observan la Tierra desde el espacio y el suelo; programas públicos; y organizaciones sin ánimo de lucro que limpian océanos, restauran bosques y ríos y protegen la fauna. Cada página de solución indica quién hace el trabajo, las cifras publicadas y una vía para donar o unirse cuando existe.',
   f'كثير من المجموعات تقوم بالفعل بعمل قابل للقياس. على Saving Planets نوثّق {N} حلاً حقيقياً عبر {H} محاور — وكالات مثل ناسا وNOAA ووكالة الفضاء الأوروبية وUSGS التي تراقب الأرض من الفضاء ومن الأرض؛ وبرامج حكومية؛ ومنظمات غير ربحية تنظّف المحيطات وتستعيد الغابات والأنهار وتحمي الحياة البرية. كل صفحة حل تذكر من يقوم بالعمل والأرقام المنشورة ومسارًا للتبرع أو الانضمام عند توفره.',
   f'Molti gruppi stanno già facendo un lavoro misurabile. Su Saving Planets documentiamo {N} soluzioni reali in {H} hub: agenzie come NASA, NOAA, ESA e USGS che osservano la Terra dallo spazio e da terra; programmi pubblici; e organizzazioni non profit che ripuliscono oceani, restaurano foreste e fiumi e proteggono la fauna. Ogni pagina di soluzione indica chi fa il lavoro, i numeri pubblicati e un modo per donare o unirsi quando esiste.',
   f'קבוצות רבות כבר עושות עבודה מדידה. ב-Saving Planets אנחנו מתעדים {N} פתרונות אמיתיים ב-{H} מרכזים — סוכנויות כמו NASA, NOAA, ESA ו-USGS שצופות בכדור הארץ מהחלל ומהקרקע; תוכניות ממשלתיות; ועמותות שמנקות אוקיינוסים, משקמות יערות ונהרות ומגנות על חיות בר. בכל דף פתרון מפורטים מי עושה את העבודה, המספרים שפורסמו, ונתיב לתרומה או הצטרפות כשקיים כזה.')],
 [('NASA Science', 'https://science.nasa.gov/'), ('NOAA', 'https://www.noaa.gov/'), ('ESA Earth Observation', 'https://www.esa.int/Applications/Observing_the_Earth')],
 [('Solutions.html', T('Browse all solutions', 'Parcourir toutes les solutions', 'Ver todas las soluciones', 'تصفّح كل الحلول', 'Sfoglia tutte le soluzioni', 'עיינו בכל הפתרונות')),
  ('Ways_to_Help.html', T('Ways to Help', 'Comment aider', 'Formas de ayudar', 'طرق المساعدة', 'Come aiutare', 'דרכים לעזור'))])

add('planet-dying',
 T('Is our planet dying?',
   'Notre planète est-elle en train de mourir ?',
   '¿Está muriendo nuestro planeta?',
   'هل كوكبنا يموت؟',
   'Il nostro pianeta sta morendo?',
   'האם כדור הארץ שלנו מת?'),
 [T('Earth is not “dying” as a planet — it will keep orbiting the Sun — but it is warming fast because of human greenhouse-gas emissions, and living systems are already under stress. NASA says the evidence that Earth is warming at an unprecedented rate, with human activity as the principal cause, is unequivocal. The IPCC reports substantial damages and increasingly irreversible losses in ecosystems, while also stressing that deep, rapid emissions cuts can still limit further harm.',
   'La Terre ne « meurt » pas en tant que planète — elle continuera d’orbiter autour du Soleil — mais elle se réchauffe vite à cause des gaz à effet de serre humains, et les systèmes vivants sont déjà sous stress. La NASA dit que les preuves d’un réchauffement à un rythme sans précédent, dont l’activité humaine est la cause principale, sont sans équivoque. Le GIEC signale des dommages importants et des pertes de plus en plus irréversibles dans les écosystèmes, tout en soulignant que des réductions d’émissions profondes et rapides peuvent encore limiter les dégâts.',
   'La Tierra no está «muriendo» como planeta —seguirá orbitando el Sol—, pero se calienta rápido por los gases de efecto invernadero humanos, y los sistemas vivos ya están bajo estrés. La NASA dice que la evidencia de que la Tierra se calienta a un ritmo sin precedentes, con la actividad humana como causa principal, es inequívoca. El IPCC informa daños sustanciales y pérdidas cada vez más irreversibles en los ecosistemas, y también subraya que recortes profundos y rápidos de emisiones aún pueden limitar más daño.',
   'الأرض لا «تموت» ككوكب — ستواصل الدوران حول الشمس — لكنها تزداد حرارة بسرعة بسبب انبعاثات غازات الدفيئة البشرية، والأنظمة الحية تحت ضغط بالفعل. تقول ناسا إن الأدلة على احترار الأرض بمعدل غير مسبوق، والنشاط البشري هو السبب الرئيسي، قاطعة. وتشير الهيئة الحكومية الدولية المعنية بتغير المناخ إلى أضرار كبيرة وخسائر متزايدة غير قابلة للعكس في النظم البيئية، مع التأكيد أن خفضًا عميقًا وسريعًا للانبعاثات ما زال يمكنه الحد من المزيد من الضرر.',
   'La Terra non sta «morendo» come pianeta — continuerà a orbitare intorno al Sole — ma si sta scaldando in fretta per i gas serra umani, e i sistemi viventi sono già sotto stress. La NASA dice che le prove di un riscaldamento a un ritmo senza precedenti, con l’attività umana come causa principale, sono inequivocabili. L’IPCC riferisce danni sostanziali e perdite sempre più irreversibili negli ecosistemi, sottolineando anche che tagli profondi e rapidi alle emissioni possono ancora limitare ulteriori danni.',
   'כדור הארץ אינו «מת» ככוכב לכת — הוא ימשיך להקיף את השמש — אבל הוא מתחמם מהר בגלל פליטות גזי חממה אנושיות, ומערכות החיים כבר תחת לחץ. NASA אומרת שהראיות לכך שכדור הארץ מתחמם בקצב חסר תקדים, כשהפעילות האנושית היא הסיבה העיקרית, הן חד-משמעיות. IPCC מדווח על נזקים משמעותיים ואובדן הולך וגדל שאינו הפיך במערכות אקולוגיות, ומדגיש גם שקיצוץ עמוק ומהיר בפליטות עדיין יכול להגביל נזק נוסף.')],
 [('NASA, Evidence', 'https://science.nasa.gov/climate-change/evidence/'),
  ('IPCC AR6 Synthesis Report SPM', 'https://www.ipcc.ch/report/ar6/syr/summary-for-policymakers/')],
 [('Myth_vs_Fact.html', T('Myth vs Fact', 'Mythe ou réalité', 'Mito o realidad', 'خرافة أم حقيقة', 'Mito o realtà', 'מיתוס מול עובדה')),
  ('Earth_Observation.html', T('Earth Observation', 'Observation de la Terre', 'Observación de la Tierra', 'رصد الأرض', 'Osservazione della Terra', 'תצפית כדור הארץ'))])

add('gone-ten-years',
 T('Will Earth really be gone in the next ten years?',
   'La Terre va-t-elle vraiment disparaître dans les dix prochaines années ?',
   '¿Desaparecerá de verdad la Tierra en los próximos diez años?',
   'هل ستختفي الأرض حقًا خلال السنوات العشر القادمة؟',
   'La Terra sparirà davvero nei prossimi dieci anni?',
   'האם כדור הארץ באמת ייעלם בעשר השנים הקרובות?'),
 [T('No. Earth will not be “gone” in ten years. Talk of a ten-year clock usually means a window to cut emissions enough to keep warming closer to 1.5°C — not that the planet vanishes. NASA is clear that warming and its effects are already here, and that future risk depends strongly on how much we emit next. The IPCC says some changes are unavoidable or irreversible over long timescales, but deep, rapid, sustained cuts can still limit further sea-level rise and the chance of abrupt, high-impact changes.',
   'Non. La Terre ne va pas « disparaître » en dix ans. Quand on parle d’une horloge de dix ans, on parle en général d’une fenêtre pour réduire assez les émissions afin de rester plus près de 1,5 °C — pas d’une planète qui s’évanouit. La NASA est claire : le réchauffement et ses effets sont déjà là, et le risque futur dépend fortement de ce que nous émettrons ensuite. Le GIEC dit que certains changements sont inévitables ou irréversibles sur de longues échelles, mais que des réductions profondes, rapides et durables peuvent encore limiter la hausse du niveau de la mer et le risque de changements brusques à fort impact.',
   'No. La Tierra no «desaparecerá» en diez años. Hablar de un reloj de diez años suele referirse a una ventana para recortar emisiones lo bastante como para mantener el calentamiento más cerca de 1,5 °C, no a que el planeta se esfume. La NASA deja claro que el calentamiento y sus efectos ya están aquí, y que el riesgo futuro depende mucho de cuánto emitamos después. El IPCC dice que algunos cambios son inevitables o irreversibles a largo plazo, pero que recortes profundos, rápidos y sostenidos aún pueden limitar más subida del nivel del mar y la probabilidad de cambios abruptos de alto impacto.',
   'لا. لن «تختفي» الأرض خلال عشر سنوات. الحديث عن ساعة لعشر سنوات يعني عادة نافذة لخفض الانبعاثات بما يكفي لإبقاء الاحترار أقرب إلى 1.5 درجة مئوية — لا اختفاء الكوكب. ناسا واضحة أن الاحترار وآثاره موجودة بالفعل، وأن الخطر المستقبلي يعتمد بقوة على ما سنطلقه لاحقًا. تقول الهيئة الحكومية الدولية المعنية بتغير المناخ إن بعض التغيرات لا مفر منها أو غير قابلة للعكس على مدى طويل، لكن خفضًا عميقًا وسريعًا ومستدامًا ما زال يمكنه الحد من ارتفاع إضافي لمستوى البحر واحتمال تغيرات مفاجئة عالية الأثر.',
   'No. La Terra non «sparirà» in dieci anni. Parlare di un orologio di dieci anni di solito indica una finestra per tagliare abbastanza le emissioni da tenere il riscaldamento più vicino a 1,5 °C — non che il pianeta scompaia. La NASA è chiara: il riscaldamento e i suoi effetti ci sono già, e il rischio futuro dipende fortemente da quanto emetteremo dopo. L’IPCC dice che alcuni cambiamenti sono inevitabili o irreversibili su scale lunghe, ma tagli profondi, rapidi e sostenuti possono ancora limitare ulteriore innalzamento del mare e la probabilità di cambiamenti abrupti ad alto impatto.',
   'לא. כדור הארץ לא «ייעלם» בעשר שנים. דיבור על שעון של עשר שנים מתכוון בדרך כלל לחלון זמן לחתוך פליטות מספיק כדי לשמור על ההתחממות קרוב יותר ל-1.5°C — לא שהכוכב נעלם. NASA ברורה: ההתחממות וההשפעות כבר כאן, והסיכון העתידי תלוי מאוד בכמה נפלוט בהמשך. IPCC אומר שחלק מהשינויים בלתי נמנעים או בלתי הפיכים על פני זמן ארוך, אבל קיצוץ עמוק, מהיר ומתמשך עדיין יכול להגביל עלייה נוספת במפלס הים ואת הסיכוי לשינויים פתאומיים בעלי השפעה גבוהה.')],
 [('NASA, Is it too late?', 'https://science.nasa.gov/climate-change/faq/is-it-too-late-to-prevent-climate-change/'),
  ('IPCC AR6 SYR SPM B.3', 'https://www.ipcc.ch/report/ar6/syr/summary-for-policymakers/')],
 [('Solutions.html', T('Real solutions', 'Vraies solutions', 'Soluciones reales', 'حلول حقيقية', 'Soluzioni reali', 'פתרונות אמיתיים')),
  ('Ways_to_Help.html', T('What you can do', 'Ce que vous pouvez faire', 'Qué puedes hacer', 'ما يمكنك فعله', 'Cosa puoi fare', 'מה אפשר לעשות'))])

add('too-late',
 T('Is it too late to stop climate change?',
   'Est-il trop tard pour arrêter le changement climatique ?',
   '¿Es demasiado tarde para detener el cambio climático?',
   'هل فات الأوان لوقف تغير المناخ؟',
   'È troppo tardi per fermare il cambiamento climatico?',
   'האם מאוחר מדי לעצור את שינוי האקלים?'),
 [T('It is not too late to limit how bad things get. NASA explains that if greenhouse-gas emissions stopped today, the rise in global temperatures would begin to flatten within a few years, though temperatures would stay elevated for many centuries. Responding means both mitigation (cutting emissions) and adaptation (living with change already locked in). Every bit of avoided future warming reduces damage that would otherwise last essentially forever.',
   'Il n’est pas trop tard pour limiter la gravité. La NASA explique que si les émissions de gaz à effet de serre s’arrêtaient aujourd’hui, la hausse des températures mondiales commencerait à s’aplatir en quelques années, même si les températures resteraient élevées pendant de nombreux siècles. Répondre signifie à la fois l’atténuation (réduire les émissions) et l’adaptation (vivre avec le changement déjà engagé). Chaque fraction de réchauffement évité réduit des dommages qui, sinon, dureraient pratiquement pour toujours.',
   'No es demasiado tarde para limitar lo malo que puede ponerse. La NASA explica que si las emisiones de gases de efecto invernadero se detuvieran hoy, el aumento de la temperatura global empezaría a aplanarse en unos pocos años, aunque las temperaturas seguirían elevadas durante muchos siglos. Responder implica mitigación (recortar emisiones) y adaptación (vivir con el cambio ya en marcha). Cada poco de calentamiento futuro evitado reduce daños que, de lo contrario, durarían esencialmente para siempre.',
   'لم يفت الأوان للحد من سوء الأمور. توضح ناسا أنه لو توقفت انبعاثات غازات الدفيئة اليوم، لبدأ ارتفاع درجات الحرارة العالمية في التسطح خلال بضع سنوات، رغم أن درجات الحرارة ستبقى مرتفعة لقرون كثيرة. الاستجابة تعني التخفيف (خفض الانبعاثات) والتكيف (العيش مع التغير الذي بدأ بالفعل). كل قدر من الاحترار المستقبلي يُتجنّب يقلل ضررًا كان ليدوم عمليًا إلى الأبد.',
   'Non è troppo tardi per limitare quanto possa peggiorare. La NASA spiega che se le emissioni di gas serra si fermassero oggi, l’aumento delle temperature globali inizierebbe ad appiattirsi in pochi anni, anche se le temperature resterebbero elevate per molti secoli. Rispondere significa mitigazione (tagliare le emissioni) e adattamento (convivere con il cambiamento già innescato). Ogni pezzo di riscaldamento futuro evitato riduce danni che altrimenti durerebbero sostanzialmente per sempre.',
   'לא מאוחר מדי להגביל עד כמה זה יכול להיות גרוע. NASA מסבירה שאם פליטות גזי החממה ייעצרו היום, עליית הטמפרטורות העולמיות תתחיל להתיישר תוך כמה שנים, אף שהטמפרטורות יישארו גבוהות במשך מאות שנים רבות. התגובה כוללת הפחתה (קיצוץ פליטות) והסתגלות (לחיות עם השינוי שכבר ננעל). כל מעט התחממות עתידית שנמנעת מקטינה נזק שהיה נמשך למעשה לנצח.')],
 [('NASA FAQ: Is it too late?', 'https://science.nasa.gov/climate-change/faq/is-it-too-late-to-prevent-climate-change/')],
 [('Solutions.html', T('Solutions directory', 'Annuaire des solutions', 'Directorio de soluciones', 'دليل الحلول', 'Elenco delle soluzioni', 'מדריך הפתרונות'))])

add('humans-cause',
 T('Are humans causing climate change?',
   'Les humains causent-ils le changement climatique ?',
   '¿Los humanos están causando el cambio climático?',
   'هل يتسبب البشر في تغير المناخ؟',
   'Gli esseri umani stanno causando il cambiamento climatico?',
   'האם בני האדם גורמים לשינוי האקלים?'),
 [T('Yes. NASA states that human activity is the principal cause of the current warming, which is happening at a rate not seen in the past 10,000 years. The IPCC likewise treats human influence on the climate system as established fact. Natural factors such as the Sun and volcanoes matter for climate history, but they do not explain the warming trend of recent decades.',
   'Oui. La NASA affirme que l’activité humaine est la cause principale du réchauffement actuel, à un rythme jamais vu depuis 10 000 ans. Le GIEC traite aussi l’influence humaine sur le système climatique comme un fait établi. Le Soleil et les volcans comptent dans l’histoire du climat, mais ils n’expliquent pas la tendance au réchauffement des dernières décennies.',
   'Sí. La NASA afirma que la actividad humana es la causa principal del calentamiento actual, a un ritmo no visto en los últimos 10.000 años. El IPCC también trata la influencia humana sobre el sistema climático como un hecho establecido. El Sol y los volcanes importan en la historia del clima, pero no explican la tendencia de calentamiento de las últimas décadas.',
   'نعم. تقول ناسا إن النشاط البشري هو السبب الرئيسي للاحترار الحالي، بمعدل لم يُرَ في آخر 10,000 سنة. وتتعامل الهيئة الحكومية الدولية المعنية بتغير المناخ أيضًا مع التأثير البشري على نظام المناخ كحقيقة ثابتة. الشمس والبراكين مهمان في تاريخ المناخ، لكنهما لا يفسران اتجاه الاحترار في العقود الأخيرة.',
   'Sì. La NASA afferma che l’attività umana è la causa principale del riscaldamento attuale, a un ritmo non visto negli ultimi 10.000 anni. Anche l’IPCC tratta l’influenza umana sul sistema climatico come fatto stabilito. Sole e vulcani contano nella storia del clima, ma non spiegano la tendenza al riscaldamento degli ultimi decenni.',
   'כן. NASA קובעת שהפעילות האנושית היא הסיבה העיקרית להתחממות הנוכחית, בקצב שלא נראה ב-10,000 השנים האחרונות. גם IPCC מתייחס להשפעה האנושית על מערכת האקלים כעובדה מבוססת. השמש והרי געש חשובים להיסטוריית האקלים, אבל הם לא מסבירים את מגמת ההתחממות בעשורים האחרונים.')],
 [('NASA, Evidence', 'https://science.nasa.gov/climate-change/evidence/'),
  ('NASA FAQ: Is the Sun causing global warming?', 'https://science.nasa.gov/climate-change/faq/')],
 [('Amazing_Facts.html', T('Amazing Facts', 'Faits étonnants', 'Datos sorprendentes', 'حقائق مذهلة', 'Fatti sorprendenti', 'עובדות מדהימות'))])

add('what-i-can-do',
 T('How can I help save the planet?',
   'Comment puis-je aider à sauver la planète ?',
   '¿Cómo puedo ayudar a salvar el planeta?',
   'كيف يمكنني المساعدة في إنقاذ الكوكب؟',
   'Come posso aiutare a salvare il pianeta?',
   'איך אפשר לעזור להציל את כדור הארץ?'),
 [T('Start with actions that compound: cut energy waste at home, choose cleaner travel when you can, eat more plants and waste less food, buy less and repair more, and support groups that already remove plastic, restore forests or protect wildlife. The United Nations ActNow campaign lists practical steps anyone can take. On Saving Planets, Ways to Help links you straight to donate and join pages for the organizations doing the work — we do not take a cut.',
   'Commencez par des gestes qui s’additionnent : moins d’énergie gaspillée chez vous, des déplacements plus propres quand c’est possible, plus de plantes et moins de gaspillage alimentaire, acheter moins et réparer plus, et soutenir des groupes qui retirent déjà le plastique, restaurent les forêts ou protègent la faune. La campagne ActNow des Nations Unies liste des gestes concrets. Sur Saving Planets, Comment aider vous mène aux pages de don et d’engagement des organisations qui font le travail — nous ne prenons aucune commission.',
   'Empieza por acciones que suman: menos energía desperdiciada en casa, un viaje más limpio cuando puedas, más plantas y menos desperdicio de comida, comprar menos y reparar más, y apoyar a grupos que ya retiran plástico, restauran bosques o protegen la fauna. La campaña ActNow de la ONU lista pasos prácticos. En Saving Planets, Formas de ayudar te lleva a las páginas de donación y de unirte de las organizaciones que hacen el trabajo: nosotros no nos quedamos con nada.',
   'ابدأ بأفعال تتراكم: قلّل هدر الطاقة في المنزل، واختر تنقلاً أنظف حين تستطيع، وكل المزيد من النباتات وأقل من هدر الطعام، واشترِ أقل وأصلِح أكثر، وادعم مجموعات تزيل البلاستيك أو تستعيد الغابات أو تحمي الحياة البرية. حملة ActNow للأمم المتحدة تسرد خطوات عملية. على Saving Planets، «طرق المساعدة» توصلك إلى صفحات التبرع والانضمام للمنظمات التي تقوم بالعمل — ونحن لا نأخذ عمولة.',
   'Inizia da azioni che si sommano: meno energia sprecata in casa, spostamenti più puliti quando puoi, più piante e meno spreco di cibo, compra meno e ripara di più, e sostieni gruppi che già rimuovono plastica, restaurano foreste o proteggono la fauna. La campagna ActNow delle Nazioni Unite elenca passi pratici. Su Saving Planets, Come aiutare ti porta alle pagine di donazione e adesione delle organizzazioni che fanno il lavoro — noi non tratteniamo nulla.',
   'התחילו בפעולות שמצטברות: חתכו בזבוז אנרגיה בבית, בחרו נסיעה נקייה יותר כשאפשר, אכלו יותר צמחים ובזבזו פחות אוכל, קנו פחות ותקנו יותר, ותמכו בקבוצות שכבר מסירות פלסטיק, משקמות יערות או מגנות על חיות בר. קמפיין ActNow של האו״ם מפרט צעדים מעשיים. ב-Saving Planets, «דרכים לעזור» מוביל לדפי תרומה והצטרפות של הארגונים שעושים את העבודה — אנחנו לא לוקחים עמלה.')],
 [('UN ActNow: ten actions', 'https://www.un.org/en/actnow/ten-actions/')],
 [('Ways_to_Help.html', T('Ways to Help', 'Comment aider', 'Formas de ayudar', 'طرق المساعدة', 'Come aiutare', 'דרכים לעזור'))])

add('sea-level',
 T('Is sea level rising, and how fast?',
   'Le niveau de la mer monte-t-il, et à quelle vitesse ?',
   '¿Está subiendo el nivel del mar y a qué velocidad?',
   'هل يرتفع مستوى سطح البحر وبأي سرعة؟',
   'Il livello del mare sta salendo e quanto velocemente?',
   'האם מפלס הים עולה, ובאיזו מהירות?'),
 [T('Yes. Sea level is rising as oceans warm and land ice melts. The IPCC says sea-level rise is unavoidable for centuries to millennia, but deep, rapid emissions cuts would limit further acceleration. Relative to 1995–2014, likely global mean sea-level rise by 2100 ranges from about 0.28–0.55 m in a very low emissions pathway to about 0.63–1.01 m in a very high emissions pathway (medium confidence).',
   'Oui. Le niveau de la mer monte à mesure que les océans se réchauffent et que la glace terrestre fond. Le GIEC dit que la hausse est inévitable pour des siècles à des millénaires, mais que des réductions d’émissions profondes et rapides limiteraient l’accélération. Par rapport à 1995–2014, la hausse probable du niveau moyen mondial d’ici 2100 va d’environ 0,28–0,55 m dans une trajectoire à très faibles émissions à environ 0,63–1,01 m dans une trajectoire à très fortes émissions (confiance moyenne).',
   'Sí. El nivel del mar sube a medida que los océanos se calientan y el hielo terrestre se derrite. El IPCC dice que la subida es inevitable durante siglos o milenios, pero que recortes profundos y rápidos limitarían una mayor aceleración. Respecto a 1995–2014, la subida probable del nivel medio mundial hacia 2100 va de unos 0,28–0,55 m en una vía de emisiones muy bajas a unos 0,63–1,01 m en una vía de emisiones muy altas (confianza media).',
   'نعم. يرتفع مستوى سطح البحر مع احترار المحيطات وذوبان الجليد البري. تقول الهيئة الحكومية الدولية المعنية بتغير المناخ إن الارتفاع لا مفر منه لقرون إلى آلاف السنين، لكن خفضًا عميقًا وسريعًا للانبعاثات سيحد من التسارع. مقارنةً بـ1995–2014، الارتفاع المحتمل لمتوسط مستوى سطح البحر العالمي بحلول 2100 يتراوح بين نحو 0.28–0.55 م في مسار انبعاثات شديد الانخفاض ونحو 0.63–1.01 م في مسار شديد الارتفاع (ثقة متوسطة).',
   'Sì. Il livello del mare sale mentre gli oceani si scaldano e il ghiaccio terrestre si scioglie. L’IPCC dice che l’innalzamento è inevitabile per secoli o millenni, ma tagli profondi e rapidi limiterebbero un’ulteriore accelerazione. Rispetto al 1995–2014, l’innalzamento medio globale probabile entro il 2100 va da circa 0,28–0,55 m in uno scenario a emissioni molto basse a circa 0,63–1,01 m in uno a emissioni molto alte (media confidenza).',
   'כן. מפלס הים עולה כשהאוקיינוסים מתחממים וקרח יבשתי נמס. IPCC אומר שעליית המפלס בלתי נמנעת במשך מאות עד אלפי שנים, אבל קיצוץ עמוק ומהיר בפליטות יגביל האצה נוספת. יחסית ל-1995–2014, עלייה ממוצעת גלובלית סבירה עד 2100 נעה מכ-0.28–0.55 מ׳ במסלול פליטות נמוך מאוד עד כ-0.63–1.01 מ׳ במסלול גבוה מאוד (ביטחון בינוני).')],
 [('IPCC AR6 SYR SPM B.3.1', 'https://www.ipcc.ch/report/ar6/syr/summary-for-policymakers/')],
 [('Oceans.html', T('Oceans hub', 'Pôle Océans', 'Eje Océanos', 'محور المحيطات', 'Hub Oceani', 'מרכז האוקיינוסים'))])

add('ozone',
 T('Is the ozone hole fixed?',
   'Le trou dans la couche d’ozone est-il réparé ?',
   '¿Está arreglado el agujero de ozono?',
   'هل أُصلح ثقب الأوزون؟',
   'Il buco dell’ozono è riparato?',
   'האם חור האוזון תוקן?'),
 [T('It is healing, not finished. NOAA and NASA ranked the 2025 Antarctic ozone hole the fifth smallest since 1992, when the Montreal Protocol began to take effect, and the ozone layer remains on track to recover fully later this century. Recovery is slow because banned chemicals still leak from old products; scientists expect the Antarctic hole to recover around the late 2060s.',
   'Il guérit, ce n’est pas fini. La NOAA et la NASA ont classé le trou d’ozone antarctique de 2025 au cinquième rang des plus petits depuis 1992, quand le Protocole de Montréal a commencé à produire ses effets, et la couche d’ozone reste en voie de se rétablir pleinement plus tard dans ce siècle. Le rétablissement est lent car des produits chimiques interdits fuient encore d’anciens produits ; les scientifiques attendent un rétablissement du trou antarctique vers la fin des années 2060.',
   'Se está curando; no está terminado. La NOAA y la NASA clasificaron el agujero de ozono antártico de 2025 como el quinto más pequeño desde 1992, cuando el Protocolo de Montreal empezó a surtir efecto, y la capa de ozono sigue en camino de recuperarse por completo más adelante en este siglo. La recuperación es lenta porque aún se escapan químicos prohibidos de productos antiguos; los científicos esperan que el agujero antártico se recupere hacia finales de la década de 2060.',
   'إنه يتعافى، ولم ينتهِ بعد. صنّفت NOAA وناسا ثقب الأوزون فوق القارة القطبية الجنوبية لعام 2025 خامس أصغر ثقب منذ 1992، حين بدأ بروتوكول مونتريال يؤتي أثره، ولا تزال طبقة الأوزون في طريقها للتعافي الكامل لاحقًا هذا القرن. التعافي بطيء لأن موادًا محظورة ما زالت تتسرب من منتجات قديمة؛ ويتوقع العلماء تعافي الثقب فوق القطب الجنوبي حوالي أواخر ستينيات هذا القرن.',
   'Sta guarendo; non è finito. NOAA e NASA hanno classificato il buco dell’ozono antartico del 2025 come il quinto più piccolo dal 1992, quando il Protocollo di Montreal iniziò a fare effetto, e lo strato di ozono resta sulla strada di un recupero completo più avanti in questo secolo. Il recupero è lento perché sostanze vietate ancora fuoriescono da prodotti vecchi; gli scienziati si aspettano il recupero del buco antartico verso la fine degli anni 2060.',
   'הוא מחליס, עדיין לא הסתיים. NOAA ו-NASA דירגו את חור האוזון באנטארקטיקה ב-2025 כחמישי בקטנו מאז 1992, כשפרוטוקול מונטריאול החל להשפיע, ושכבת האוזון עדיין בדרך להחלמה מלאה בהמשך המאה. ההחלמה איטית כי כימיקלים אסורים עדיין דולפים ממוצרים ישנים; מדענים מצפים שהחור באנטארקטיקה יחלים בסביבות סוף שנות ה-60 של המאה.')],
 [('NOAA/NASA 2025 ozone hole', 'https://www.noaa.gov/news-release/noaa-nasa-2025-ozone-hole-is-5th-smallest-since-1992')],
 [('Myth_vs_Fact.html', T('Myth vs Fact', 'Mythe ou réalité', 'Mito o realidad', 'خرافة أم حقيقة', 'Mito o realtà', 'מיתוס מול עובדה')),
  ('Three_Shields.html', T('Three Invisible Shields', 'Trois boucliers invisibles', 'Tres escudos invisibles', 'ثلاثة دروع غير مرئية', 'Tre scudi invisibili', 'שלושה מגינים בלתי נראים'))])

add('asteroid',
 T('Can we stop an asteroid from hitting Earth?',
   'Peut-on empêcher un astéroïde de frapper la Terre ?',
   '¿Podemos impedir que un asteroide golpee la Tierra?',
   'هل يمكننا منع كويكب من ضرب الأرض؟',
   'Possiamo impedire a un asteroide di colpire la Terra?',
   'האם אפשר למנוע מאסטרואיד לפגוע בכדור הארץ?'),
 [T('We have already moved one. NASA’s DART spacecraft hit the asteroid moonlet Dimorphos in 2022 and shortened its orbit by 33 minutes and 15 seconds. DART was a test on a small asteroid that posed no threat. Finding asteroids early gives time to act, which is why NASA is building NEO Surveyor.',
   'Nous en avons déjà dévié un. La sonde DART de la NASA a percuté la petite lune d’astéroïde Dimorphos en 2022 et raccourci son orbite de 33 minutes et 15 secondes. DART était un test sur un petit astéroïde sans danger. Repérer les astéroïdes tôt laisse le temps d’agir, c’est pourquoi la NASA construit NEO Surveyor.',
   'Ya movimos uno. La nave DART de la NASA impactó la pequeña luna de asteroide Dimorphos en 2022 y acortó su órbita en 33 minutos y 15 segundos. DART fue una prueba con un asteroide pequeño sin amenaza. Detectar asteroides pronto da tiempo para actuar; por eso la NASA construye NEO Surveyor.',
   'لقد حرّكنا واحدًا بالفعل. اصطدمت مركبة DART التابعة لناسا بالقمر الصغير للكويكب ديمورفوس عام 2022 وقصّرت مداره بمقدار 33 دقيقة و15 ثانية. كانت DART تجربة على كويكب صغير بلا تهديد. رصد الكويكبات مبكرًا يمنح وقتًا للتصرف، ولهذا تبني ناسا NEO Surveyor.',
   'Ne abbiamo già mosso uno. La sonda DART della NASA ha colpito la piccola luna asteroidale Dimorphos nel 2022 e ha accorciato la sua orbita di 33 minuti e 15 secondi. DART era un test su un piccolo asteroide senza minaccia. Trovare gli asteroidi presto dà tempo di agire; per questo la NASA sta costruendo NEO Surveyor.',
   'כבר הזזנו אחד. החללית DART של NASA פגעה בירחון האסטרואיד דימורפוס ב-2022 וקיצרה את מסלולו ב-33 דקות ו-15 שניות. DART הייתה ניסוי על אסטרואיד קטן שלא היווה איום. גילוי מוקדם נותן זמן לפעול, ולכן NASA בונה את NEO Surveyor.')],
 [('NASA DART', 'https://science.nasa.gov/mission/dart/')],
 [('Planetary_Defense.html', T('Planetary Defense', 'Défense planétaire', 'Defensa planetaria', 'الدفاع الكوكبي', 'Difesa planetaria', 'הגנה פלנטרית'))])

add('oxygen',
 T('Where does most of Earth’s oxygen come from?',
   'D’où vient la plus grande partie de l’oxygène de la Terre ?',
   '¿De dónde viene la mayor parte del oxígeno de la Tierra?',
   'من أين يأتي معظم أكسجين الأرض؟',
   'Da dove viene la maggior parte dell’ossigeno della Terra?',
   'מאיפה מגיע רוב החמצן של כדור הארץ?'),
 [T('About half of Earth’s oxygen comes from the ocean, mostly from tiny drifting plankton, according to NOAA. Ocean life also uses about as much oxygen as the ocean produces, so healthy forests and a healthy ocean both matter for the air we breathe.',
   'Environ la moitié de l’oxygène de la Terre vient de l’océan, surtout du plancton minuscule qui dérive, selon la NOAA. La vie marine consomme aussi à peu près autant d’oxygène que l’océan en produit, donc des forêts saines et un océan sain comptent tous les deux pour l’air que nous respirons.',
   'Cerca de la mitad del oxígeno de la Tierra viene del océano, sobre todo de diminuto plancton a la deriva, según la NOAA. La vida marina también consume más o menos tanto oxígeno como produce el océano, así que importan tanto bosques sanos como un océano sano para el aire que respiramos.',
   'نحو نصف أكسجين الأرض يأتي من المحيط، ومعظمه من عوالق دقيقة تنجرف، بحسب NOAA. تستهلك الحياة البحرية أيضًا نحو ما ينتجه المحيط من أكسجين، لذا فالغابات السليمة والمحيط السليم كلاهما مهم لهواء نتنفسه.',
   'Circa metà dell’ossigeno della Terra viene dall’oceano, soprattutto da minuscolo plancton alla deriva, secondo la NOAA. La vita marina consuma anche più o meno tanto ossigeno quanto ne produce l’oceano, quindi contano sia foreste sane sia un oceano sano per l’aria che respiriamo.',
   'כמחצית מהחמצן של כדור הארץ מגיע מהאוקיינוס, בעיקר מפלנקטון זעיר שנסחף, לפי NOAA. החיים בים גם צורכים בערך אותה כמות חמצן שהאוקיינוס מייצר, ולכן גם יערות בריאים וגם אוקיינוס בריא חשובים לאוויר שאנחנו נושמים.')],
 [('NOAA ocean oxygen', 'https://oceanservice.noaa.gov/facts/ocean-oxygen.html')],
 [('Oceans.html', T('Oceans hub', 'Pôle Océans', 'Eje Océanos', 'محور المحيطات', 'Hub Oceani', 'מרכז האוקיינוסים')),
  ('Deforestation.html', T('Forests hub', 'Pôle Forêts', 'Eje Bosques', 'محور الغابات', 'Hub Foreste', 'מרכז היערות'))])

add('space-junk',
 T('Is space junk a real problem?',
   'Les débris spatiaux sont-ils un vrai problème ?',
   '¿Es la basura espacial un problema real?',
   'هل الحطام الفضائي مشكلة حقيقية؟',
   'I detriti spaziali sono un problema reale?',
   'האם פסולת חלל היא בעיה אמיתית?'),
 [T('Yes, and agencies are acting. ESA guided its Aeolus satellite down in 2023 in a first-of-its-kind assisted reentry, and ESA’s Zero Debris approach aims to sharply limit new debris from its missions by 2030. ESA’s 2025 report still says better rule-following is not yet enough to stop debris from increasing, so removal missions are the next step.',
   'Oui, et les agences agissent. L’ESA a guidé la descente de son satellite Aeolus en 2023 lors d’une première rentrée assistée de ce type, et l’approche Zéro débris de l’ESA vise à limiter fortement les nouveaux débris de ses missions d’ici 2030. Le rapport 2025 de l’ESA dit encore qu’un meilleur respect des règles ne suffit pas à stopper l’augmentation, donc les missions de retrait sont la prochaine étape.',
   'Sí, y las agencias actúan. La ESA guió el descenso de su satélite Aeolus en 2023 en la primera reentrada asistida de su tipo, y el enfoque Cero Desechos de la ESA busca limitar drásticamente los nuevos desechos de sus misiones para 2030. El informe 2025 de la ESA aún dice que un mejor cumplimiento de las normas no basta para frenar el aumento, así que las misiones de retirada son el siguiente paso.',
   'نعم، والوكالات تتحرك. وجّهت وكالة الفضاء الأوروبية هبوط قمرها Aeolus عام 2023 في أول عودة مساعدة من نوعها، ويهدف نهج «صفر حطام» لديها إلى الحد بشدة من الحطام الجديد من مهامها بحلول 2030. تقرير الوكالة لعام 2025 يقول إن تحسّن الالتزام بالقواعد لا يكفي بعد لوقف التزايد، لذا فمهام الإزالة هي الخطوة التالية.',
   'Sì, e le agenzie agiscono. L’ESA ha guidato la discesa del satellite Aeolus nel 2023 nella prima rientrata assistita del suo genere, e l’approccio Zero Debris dell’ESA mira a limitare drasticamente i nuovi detriti dalle sue missioni entro il 2030. Il rapporto ESA 2025 dice ancora che un miglior rispetto delle regole non basta a fermare l’aumento, quindi le missioni di rimozione sono il passo successivo.',
   'כן, והסוכנויות פועלות. ESA הנחתה את הלוויין Aeolus ב-2023 בכניסה חוזרת מסויעת ראשונה מסוגה, וגישת Zero Debris שלה שואפת להגביל מאוד פסולת חדשה מהמשימות שלה עד 2030. דוח ESA ל-2025 עדיין אומר ששמירה טובה יותר על הכללים אינה מספיקה לעצור את הגידול, ולכן משימות הסרה הן השלב הבא.')],
 [('ESA Zero Debris', 'https://www.esa.int/Space_Safety/Clean_Space/ESA_s_Zero_Debris_approach')],
 [('Space_Disposal.html', T('Space Disposal', 'Élimination spatiale', 'Eliminación espacial', 'التخلص الفضائي', 'Smaltimento spaziale', 'סילוק חלל'))])

add('satellites-help',
 T('How do satellites help protect Earth?',
   'Comment les satellites aident-ils à protéger la Terre ?',
   '¿Cómo ayudan los satélites a proteger la Tierra?',
   'كيف تساعد الأقمار الصناعية في حماية الأرض؟',
   'Come i satelliti aiutano a proteggere la Terra?',
   'איך לוויינים עוזרים להגן על כדור הארץ?'),
 [T('Earth-observing satellites track forests, crops, ice, oceans, air quality and disasters so people can act earlier. Missions such as Landsat (NASA/USGS) and Copernicus Sentinels (ESA) deliver free public data used for deforestation alerts, flood maps, crop health and climate services. Saving Planets’ Earth Observation hub explains these missions in plain language and links each one to the problems it helps solve.',
   'Les satellites d’observation de la Terre suivent forêts, cultures, glace, océans, qualité de l’air et catastrophes pour que l’on puisse agir plus tôt. Des missions comme Landsat (NASA/USGS) et les Sentinelles Copernicus (ESA) fournissent des données publiques gratuites utilisées pour les alertes de déforestation, les cartes d’inondation, la santé des cultures et les services climatiques. Le pôle Observation de la Terre de Saving Planets explique ces missions en langage clair.',
   'Los satélites de observación de la Tierra siguen bosques, cultivos, hielo, océanos, calidad del aire y desastres para actuar antes. Misiones como Landsat (NASA/USGS) y los Sentinel de Copernicus (ESA) ofrecen datos públicos gratuitos usados en alertas de deforestación, mapas de inundación, salud de cultivos y servicios climáticos. El eje Observación de la Tierra de Saving Planets explica estas misiones en lenguaje claro.',
   'تراقب أقمار رصد الأرض الغابات والمحاصيل والجليد والمحيطات وجودة الهواء والكوارث كي يتسنى التصرف أبكر. مهام مثل Landsat (ناسا/USGS) وSentinel ضمن كوبرنيكوس (وكالة الفضاء الأوروبية) تقدّم بيانات عامة مجانية تُستخدم لتنبيهات إزالة الغابات وخرائط الفيضانات وصحة المحاصيل وخدمات المناخ. محور رصد الأرض في Saving Planets يشرح هذه المهام بلغة واضحة.',
   'I satelliti di osservazione della Terra seguono foreste, colture, ghiaccio, oceani, qualità dell’aria e disastri così si può agire prima. Missioni come Landsat (NASA/USGS) e i Sentinel di Copernicus (ESA) forniscono dati pubblici gratuiti usati per allerte di deforestazione, mappe di alluvione, salute delle colture e servizi climatici. L’hub Osservazione della Terra di Saving Planets spiega queste missioni in linguaggio chiaro.',
   'לווייני תצפית כדור הארץ עוקבים אחרי יערות, יבולים, קרח, אוקיינוסים, איכות אוויר ואסונות כדי שנוכל לפעול מוקדם יותר. משימות כמו Landsat (NASA/USGS) ו-Sentinel של קופרניקוס (ESA) מספקות נתונים ציבוריים חינמיים לשימוש בהתרעות כריתה, מפות שיטפונות, בריאות יבולים ושירותי אקלים. מרכז תצפית כדור הארץ של Saving Planets מסביר את המשימות האלה בשפה פשוטה.')],
 [('NASA Landsat 9', 'https://science.nasa.gov/mission/landsat-9/'),
  ('ESA Copernicus', 'https://www.esa.int/Applications/Observing_the_Earth/Copernicus')],
 [('Earth_Observation.html', T('Earth Observation', 'Observation de la Terre', 'Observación de la Tierra', 'رصد الأرض', 'Osservazione della Terra', 'תצפית כדור הארץ'))])

add('climate-vs-warming',
 T('What is the difference between climate change and global warming?',
   'Quelle est la différence entre changement climatique et réchauffement climatique ?',
   '¿Cuál es la diferencia entre cambio climático y calentamiento global?',
   'ما الفرق بين تغير المناخ والاحترار العالمي؟',
   'Qual è la differenza tra cambiamento climatico e riscaldamento globale?',
   'מה ההבדל בין שינוי אקלים להתחממות גלובלית?'),
 [T('NASA puts it simply: “global warming” is the long-term heating of the planet; “climate change” includes that warming plus broader shifts such as rising seas, shrinking glaciers, earlier ice melt and changes in when plants bloom.',
   'La NASA le dit simplement : le « réchauffement climatique » est le réchauffement à long terme de la planète ; le « changement climatique » inclut ce réchauffement plus des changements plus larges comme la hausse des mers, le recul des glaciers, une fonte plus précoce et des décalages dans la floraison.',
   'La NASA lo dice claro: el «calentamiento global» es el calentamiento a largo plazo del planeta; el «cambio climático» incluye ese calentamiento y cambios más amplios como la subida del mar, el retroceso de glaciares, un deshielo más temprano y cambios en la floración.',
   'تلخّصها ناسا ببساطة: «الاحترار العالمي» هو ارتفاع حرارة الكوكب على المدى الطويل؛ و«تغير المناخ» يشمل ذلك الاحترار مع تغيّرات أوسع مثل ارتفاع البحار وتراجع الأنهار الجليدية وذوبان أبكر وتغيّر مواعيد إزهار النباتات.',
   'La NASA lo dice in modo semplice: il «riscaldamento globale» è il riscaldamento a lungo termine del pianeta; il «cambiamento climatico» include quel riscaldamento più cambiamenti più ampi come l’innalzamento dei mari, il ritiro dei ghiacciai, uno scioglimento più precoce e lo spostamento della fioritura.',
   'NASA אומרת זאת בפשטות: «התחממות גלובלית» היא חימום ארוך-טווח של הכוכב; «שינוי אקלים» כולל את אותה התחממות ועוד שינויים רחבים כמו עליית מפלס הים, נסיגת קרחונים, הפשרה מוקדמת יותר ושינויים במועד הפריחה.')],
 [('NASA climate FAQ', 'https://science.nasa.gov/climate-change/faq/')],
 [('Glossary.html', T('Glossary', 'Glossaire', 'Glosario', 'مسرد', 'Glossario', 'מילון מונחים'))])

CSS = '''
.bq-wrap{max-width:820px;margin:0 auto;padding:0 1.2rem 3rem}
.bq-toc{display:flex;flex-wrap:wrap;gap:.45rem;margin:1rem 0 1.6rem}
.bq-toc a{font-size:.88rem;padding:.35rem .7rem;border-radius:999px;border:1px solid rgba(143,211,255,.35);color:#8fd3ff;text-decoration:none}
.bq-toc a:hover{background:rgba(0,156,222,.15)}
.bq-card{margin:1.1rem 0;padding:1rem 1.15rem;border-radius:16px;border:1px solid rgba(124,170,255,.4);background:rgba(124,170,255,.07)}
.bq-card h2{margin:.15rem 0 .55rem;font-size:1.15rem;line-height:1.35}
.bq-card p{margin:.4rem 0;line-height:1.55}
.bq-src,.bq-more{font-size:.9rem}
.bq-src ul,.bq-more ul{margin:.25rem 0 .4rem;padding-inline-start:1.2rem}
.bq-meta{font-size:.85rem;opacity:.85;margin-top:1.5rem}
'''

def shell_for(l):
    p = 'Glossary.html' if l == 'en' else f'{l}/Glossary.html'
    return open(p, encoding='utf8').read()

def faq_ld(l):
    ents = []
    for item in Q:
        text = ' '.join(item['a'][i][l] for i in range(len(item['a'])))
        ents.append({"@type": "Question", "name": item['q'][l],
                     "acceptedAnswer": {"@type": "Answer", "text": text}})
    return {"@context": "https://schema.org", "@type": "FAQPage", "url": url(l),
            "inLanguage": l, "mainEntity": ents,
            "isPartOf": {"@type": "WebSite", "name": "Saving Planets", "url": SITE}}

def crumbs(l):
    home = T('Home','Accueil','Inicio','الرئيسية','Home','דף הבית')[l]
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":home,"item":SITE + d(l)},
        {"@type":"ListItem","position":2,"name":UI['nav'][l],"item":url(l)}]}

def build_lang(l):
    raw = shell_for(l)
    title, desc = UI['title'][l], UI['desc'][l]
    head_end = raw.index('</head>')
    head = raw[:head_end]
    # wipe prior ld+json in head; we'll inject
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'Glossary\.html', PAGE, head)
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', head)
    for attr, val in (
        ('name="description" content="', desc),
        ('property="og:description" content="', desc),
        ('name="twitter:description" content="', desc),
        ('property="og:title" content="', title),
        ('name="twitter:title" content="', title),
        ('property="og:image:alt" content="', UI['h1'][l]),
    ):
        head = re.sub(re.escape(attr) + r'[^"]*', attr + escq(val), head, count=1)
    # hreflang block
    alts = ''.join(f'<link rel="alternate" hreflang="{x}" href="{url(x)}">\n' for x in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{url("en")}">\n'
    if 'hreflang="en"' in head:
        head = re.sub(r'(<link rel="alternate" hreflang="en"[^>]*>\n(?:<link rel="alternate" hreflang="[^"]+"[^>]*>\n)*)', alts, head, count=1)
    else:
        head = head.replace('<link rel="canonical"', alts + '<link rel="canonical"', 1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\1' + url(l), head, count=1)
    head = re.sub(r'(property="og:url" content=")[^"]*', r'\1' + url(l), head, count=1)
    head = re.sub(r'(property="og:locale" content=")[^"]*', r'\1' + LOCALE[l], head, count=1)
    # html lang/dir on opening tag later
    ld = f'<script type="application/ld+json">{json.dumps(faq_ld(l), ensure_ascii=False)}</script>\n'
    ld += f'<script type="application/ld+json">{json.dumps(crumbs(l), ensure_ascii=False)}</script>\n'
    head = head + ld
    # body
    bodym = re.search(r'<body[^>]*>', raw).group(0)
    navm = re.search(r'<a class="skip-link".*?</nav>', raw, re.S)
    nav = navm.group(0) if navm else ''
    nav = re.sub(r'Glossary\.html', PAGE, nav)
    foot = raw[raw.index('</main>'):]
    # content
    toc = ''.join(f'<a href="#{item["id"]}">{esc(item["q"][l])}</a>' for item in Q)
    cards = []
    for item in Q:
        paras = ''.join(f'<p>{esc(p[l])}</p>' for p in item['a'])
        srcs = ''.join(f'<li><a href="{escq(u)}" target="_blank" rel="noopener noreferrer">{esc(t)}</a></li>' for t,u in item['sources'])
        more = ''.join(f'<li><a href="{escq(h)}">{esc(lab[l])}</a></li>' for h,lab in item['links'])
        cards.append(
            f'<article class="bq-card" id="{item["id"]}">'
            f'<h2>{esc(item["q"][l])}</h2>{paras}'
            f'<div class="bq-src"><p><strong>{esc(UI["src"][l])}</strong></p><ul>{srcs}</ul></div>'
            f'<div class="bq-more"><p><strong>{esc(UI["more"][l])}</strong></p><ul>{more}</ul></div>'
            f'</article>')
    main = (
        f'<main id="main"><section class="page-hero learn-hero"><div class="page-hero-content">'
        f'<h1>{esc(UI["h1"][l])}</h1><p>{esc(UI["sub"][l])}</p></div></section>'
        f'<div class="bq-wrap"><nav class="bq-toc" aria-label="Questions">{toc}</nav>'
        + ''.join(cards) +
        f'<p class="bq-meta">{esc(UI["credit"][l])} · {esc(UI["updated"][l])}</p></div></main>')
    style = f'<style id="bq-css">{CSS}</style>'
    page = f'<!DOCTYPE html>\n<html lang="{l}"' + (' dir="rtl"' if l in RTL else '') + ' class="dark">\n<head>\n'
    # rebuild head opening carefully from existing head content after <head>
    inner = head
    if '<head>' in inner:
        inner = inner.split('<head>',1)[1]
    page += inner + style + '</head>\n' + bodym + '\n' + nav + '\n' + main + '\n' + foot
    # if foot already starts with </main>, ok; else ensure
    if not foot.strip().startswith('</main>'):
        pass
    out = path(l)
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    open(out, 'w', encoding='utf8').write(page)
    return out

def main():
    wrote = []
    for l in LANGS:
        wrote.append(build_lang(l))
    # pages lists
    for listpath in ('i18n/pages.txt', 'i18n/he-pages.txt'):
        lines = open(listpath, encoding='utf8').read().splitlines()
        if PAGE not in lines:
            open(listpath, 'a', encoding='utf8').write(PAGE + '\n')
            wrote.append(listpath + '+')
    # nav: add under kids next to Myth_vs_Fact
    navp = 'scripts/build-nav.py'
    nav = open(navp, encoding='utf8').read()
    if 'Big_Questions.html' not in nav:
        nav = nav.replace(
            "'Myth_vs_Fact.html', 'Glossary.html']",
            "'Myth_vs_Fact.html', 'Big_Questions.html', 'Glossary.html']")
        # labels — add UI string map entries if present; build-nav uses UX labels; for new pages it may fall back to filename
        open(navp, 'w', encoding='utf8').write(nav)
        wrote.append(navp)
    # weekly-sync hook near student-qa
    ws = 'scripts/weekly-sync.sh'
    if os.path.exists(ws):
        s = open(ws, encoding='utf8').read()
        if 'build-big-questions.py' not in s:
            s = s.replace(
                'python3 scripts/build-student-qa.py',
                'python3 scripts/build-big-questions.py  # Oct 26: Big Questions FAQ (6 langs, FAQPage)\npython3 scripts/build-student-qa.py')
            open(ws, 'w', encoding='utf8').write(s)
            wrote.append(ws)
    print('wrote', ', '.join(wrote), f'({len(Q)} questions × {len(LANGS)} langs)')

if __name__ == '__main__':
    main()
