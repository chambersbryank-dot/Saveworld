# -*- coding: utf-8 -*-
"""Visible authorship, review, and standards text for course pages.
Public titles only: Founder and Co-founder. Say SI, never AI.
The check sentence matches CHK_T in build-courses.py."""
import html, re

REVIEWED = '2026-11-27'
ABET = 'https://www.abet.org/accreditation/accreditation-criteria/criteria-for-accrediting-engineering-programs-2025-2026/'
# Official Engineering Accreditation Commission Criterion 3 wording, 2025–2026 cycle.
ABET_OUT = {
 '1': 'an ability to identify, formulate, and solve complex engineering problems by applying principles of engineering, science, and mathematics.',
 '2': 'an ability to apply engineering design to produce solutions that meet specified needs with consideration of public health, safety, and welfare, as well as global, cultural, social, environmental, and economic factors.',
 '4': 'an ability to recognize ethical and professional responsibilities in engineering situations and make informed judgments, which must consider the impact of engineering solutions in global, economic, environmental, and societal contexts.',
 '6': 'an ability to develop and conduct appropriate experimentation, analyze and interpret data, and use engineering judgment to draw conclusions.',
}
CHK = {
 'en': 'A check is one number or code result on a course page that a script recomputes before the page is published. The printed number and the recomputed number have to match.',
 'fr': 'Un contrôle est un nombre ou un résultat de code sur une page de cours qu’un script recalcule avant publication. Le nombre affiché et le nombre recalculé doivent correspondre.',
 'es': 'Una comprobación es un número o un resultado de código en una página de curso que un script vuelve a calcular antes de publicar. El número impreso y el recalculado tienen que coincidir.',
 'ar': 'التحقق هو رقم أو نتيجة برمجية في صفحة مقرر يعيد سكربت حسابها قبل النشر. يجب أن يطابق الرقم المعروض الرقم المعاد حسابه.',
 'it': 'Un controllo è un numero o un risultato di codice in una pagina del corso che uno script ricalcola prima della pubblicazione. Il numero stampato e quello ricalcolato devono coincidere.',
 'he': 'בדיקה היא מספר או תוצאת קוד בעמוד קורס שסקריפט מחשב מחדש לפני הפרסום. המספר המודפס והמספר שחושב מחדש חייבים להתאים.',
}

# Co-founder line is the sentence already published on About.html.
T = {
 'en': {
  'h': 'Authorship and review',
  'who': 'The Founder sets direction and approves every page. The Co-founder brings 20+ years of teaching experience and is our native Arabic and French translator.',
  'check_h': 'Quality check.',
  'sources': 'Facts, worked examples and links on this page are checked against named sources, including NASA Glenn’s Beginner’s Guide to Aeronautics, MIT OpenCourseWare, and J. Gordon Leishman’s Introduction to Aerospace Flight Vehicles.',
  'reviewed': 'Last reviewed',
  'when': 'November 27, 2026',
  'about': 'About',
  'policy': 'Editorial & Sources Policy',
  'disclose': 'The Founder and Co-founder set direction, choose topics and scope, review the teaching approach and approve every page. SI researched, drafted, translated and checked sources. Every fact, worked example and link was checked against named sources and reviewed by the founders before publication.',
  'hub_disclose': 'The Founder and Co-founder set direction, choose topics and scope, review the teaching approach and approve every page. SI researched, drafted, translated and checked sources. Every fact and link on this page was checked against named sources and reviewed by the founders before publication.',
  'guide': 'Download the editable study guide (.docx)',
  'goals_h': 'Path goals',
  'goals': 'The courses on a track are there so a student can apply undergraduate engineering science to aircraft and spacecraft, carry a design from requirements through to a review, and weigh the environmental cost of flight. These are study goals for this free path, not an accredited degree.',
  'use_h': 'How to use these tracks',
  'use': 'Watch the film, then study AERO 101 before the later courses. Take each course in the order it appears under its year.',
  'std_h': 'Standards alignment',
  'std': 'These rows map this course’s learning outcomes to parts of the ABET Engineering Accreditation Commission Criterion 3 student outcomes for 2025–2026. A row says “maps to” only where this course actually teaches that part. This does not imply accreditation, academic credit, or an endorsement by ABET.',
  'col_a': 'ABET outcome',
  'col_b': 'Where this course maps',
  'skip': 'Outcomes 3, 5 and 7 are not mapped. This course does not teach communication to a range of audiences, teamwork, or a method for acquiring new knowledge.',
  'src': 'Source',
  'm1': 'Maps in part. Units 2 through 8 apply engineering, science and mathematics to introductory problems in the atmosphere, lift and drag, performance, propulsion, rockets and orbits. These are not the full range of complex engineering problems in the ABET definition.',
  'm2': 'Maps in part. Unit 1 teaches requirements, the design cycle and trade studies. Unit 9 compares the environmental cost of flight. The labs include a safety note. The course does not teach the public-health, cultural, social and economic design factors in this outcome.',
  'm4': 'Maps in part. Unit 9 covers the environmental and societal impact of aviation emissions and orbital debris. The course does not teach professional ethics or a method for ethical judgment.',
  'm6': 'Maps in part. The four labs ask you to run a test or a model, record the numbers, and explain the result: a virtual wind tunnel, a rocket-equation sheet, a glider you build and fly, and an atmosphere spreadsheet.',
 },
 'fr': {
  'h': 'Auteur et relecture',
  'who': 'Le Fondateur fixe la direction et approuve chaque page. La Cofondatrice apporte plus de 20 ans d’expérience dans l’enseignement et est notre traductrice de langue maternelle arabe et française.',
  'check_h': 'Contrôle de qualité.',
  'sources': 'Les faits, les exemples résolus et les liens de cette page sont vérifiés auprès de sources nommées, dont le Beginner’s Guide to Aeronautics de la NASA Glenn, le MIT OpenCourseWare, et Introduction to Aerospace Flight Vehicles de J. Gordon Leishman.',
  'reviewed': 'Dernière relecture',
  'when': '27 novembre 2026',
  'about': 'À propos',
  'policy': 'Politique éditoriale et des sources',
  'disclose': 'Le Fondateur et la Cofondatrice fixent la direction, choisissent les sujets et le périmètre, revoient l’approche pédagogique et approuvent chaque page. SI a recherché, rédigé, traduit et vérifié les sources. Chaque fait, exemple résolu et lien a été vérifié auprès des sources nommées et relu par les fondateurs avant publication.',
  'hub_disclose': 'Le Fondateur et la Cofondatrice fixent la direction, choisissent les sujets et le périmètre, revoient l’approche pédagogique et approuvent chaque page. SI a recherché, rédigé, traduit et vérifié les sources. Chaque fait et chaque lien de cette page a été vérifié auprès des sources nommées et relu par les fondateurs avant publication.',
  'guide': 'Télécharger le guide d’étude modifiable (.docx)',
  'goals_h': 'Objectifs du parcours',
  'goals': 'Les cours d’une filière sont là pour qu’un étudiant applique les sciences de l’ingénieur de premier cycle aux aéronefs et aux engins spatiaux, mène une conception des exigences jusqu’à une revue, et pèse le coût environnemental du vol. Ce sont des objectifs d’étude pour ce parcours gratuit, pas un diplôme accrédité.',
  'use_h': 'Comment utiliser ces filières',
  'use': 'Regardez le film, puis étudiez AERO 101 avant les cours suivants. Suivez chaque cours dans l’ordre où il apparaît sous son année.',
  'std_h': 'Correspondance avec les référentiels',
  'std': 'Ces lignes rapportent les objectifs de ce cours à des parties des student outcomes du critère 3 de l’Engineering Accreditation Commission d’ABET pour 2025–2026. Une ligne dit « correspond à » seulement là où ce cours enseigne vraiment cette partie. Cela n’implique ni accréditation, ni crédit académique, ni approbation par ABET.',
  'col_a': 'Résultat ABET',
  'col_b': 'Où ce cours correspond',
  'skip': 'Les résultats 3, 5 et 7 ne sont pas mis en correspondance. Ce cours n’enseigne pas la communication vers des publics variés, le travail en équipe, ni une méthode pour acquérir des connaissances nouvelles.',
  'src': 'Source',
  'm1': 'Correspond en partie. Les unités 2 à 8 appliquent l’ingénierie, les sciences et les mathématiques à des problèmes d’introduction : atmosphère, portance et traînée, performances, propulsion, fusées et orbites. Ce n’est pas toute l’étendue des problèmes d’ingénierie complexes au sens d’ABET.',
  'm2': 'Correspond en partie. L’unité 1 enseigne les exigences, le cycle de conception et les études d’arbitrage. L’unité 9 compare le coût environnemental du vol. Les labos comportent une note de sécurité. Le cours n’enseigne pas les facteurs de santé publique, culturels, sociaux et économiques de ce résultat.',
  'm4': 'Correspond en partie. L’unité 9 traite de l’impact environnemental et sociétal des émissions de l’aviation et des débris orbitaux. Le cours n’enseigne pas l’éthique professionnelle ni une méthode de jugement éthique.',
  'm6': 'Correspond en partie. Les quatre labos demandent de lancer un essai ou un modèle, de noter les nombres et d’expliquer le résultat : une soufflerie virtuelle, une feuille sur l’équation de la fusée, un planeur à construire et à faire voler, et un tableur d’atmosphère.',
 },
 'es': {
  'h': 'Autoría y revisión',
  'who': 'El Fundador marca la dirección y aprueba cada página. La Cofundadora aporta más de 20 años de experiencia docente y es nuestra traductora nativa de árabe y francés.',
  'check_h': 'Control de calidad.',
  'sources': 'Los datos, los ejemplos resueltos y los enlaces de esta página se comprueban con fuentes nombradas, entre ellas la Beginner’s Guide to Aeronautics de NASA Glenn, MIT OpenCourseWare y Introduction to Aerospace Flight Vehicles de J. Gordon Leishman.',
  'reviewed': 'Última revisión',
  'when': '27 de noviembre de 2026',
  'about': 'Acerca de',
  'policy': 'Política editorial y de fuentes',
  'disclose': 'El Fundador y la Cofundadora marcan la dirección, eligen los temas y el alcance, revisan el enfoque de enseñanza y aprueban cada página. SI investigó, redactó, tradujo y comprobó las fuentes. Cada dato, ejemplo resuelto y enlace se comprobó con las fuentes nombradas y lo revisaron los fundadores antes de la publicación.',
  'hub_disclose': 'El Fundador y la Cofundadora marcan la dirección, eligen los temas y el alcance, revisan el enfoque de enseñanza y aprueban cada página. SI investigó, redactó, tradujo y comprobó las fuentes. Cada dato y cada enlace de esta página se comprobó con las fuentes nombradas y lo revisaron los fundadores antes de la publicación.',
  'guide': 'Descargar la guía de estudio editable (.docx)',
  'goals_h': 'Metas del itinerario',
  'goals': 'Los cursos de un itinerario están para que un estudiante aplique las ciencias de la ingeniería de grado a aeronaves y naves espaciales, lleve un diseño desde los requisitos hasta una revisión, y valore el coste ambiental del vuelo. Son metas de estudio de este camino gratuito, no un título acreditado.',
  'use_h': 'Cómo usar estos itinerarios',
  'use': 'Mira la película y luego estudia AERO 101 antes de los cursos posteriores. Sigue cada curso en el orden en que aparece bajo su año.',
  'std_h': 'Alineación con estándares',
  'std': 'Estas filas relacionan los resultados de aprendizaje de este curso con partes de los student outcomes del Criterio 3 de la Engineering Accreditation Commission de ABET para 2025–2026. Una fila dice «corresponde a» solo donde este curso enseña de verdad esa parte. Esto no implica acreditación, crédito académico ni un respaldo de ABET.',
  'col_a': 'Resultado de ABET',
  'col_b': 'Dónde corresponde este curso',
  'skip': 'Los resultados 3, 5 y 7 no se relacionan. Este curso no enseña la comunicación con públicos distintos, el trabajo en equipo ni un método para adquirir conocimiento nuevo.',
  'src': 'Fuente',
  'm1': 'Corresponde en parte. Las unidades 2 a 8 aplican ingeniería, ciencia y matemáticas a problemas de introducción sobre la atmósfera, la sustentación y la resistencia, las actuaciones, la propulsión, los cohetes y las órbitas. No son toda la gama de problemas de ingeniería complejos de la definición de ABET.',
  'm2': 'Corresponde en parte. La unidad 1 enseña requisitos, el ciclo de diseño y los estudios de compromiso. La unidad 9 compara el coste ambiental del vuelo. Los laboratorios incluyen una nota de seguridad. El curso no enseña los factores de salud pública, culturales, sociales y económicos de este resultado.',
  'm4': 'Corresponde en parte. La unidad 9 trata el impacto ambiental y social de las emisiones de la aviación y de la basura orbital. El curso no enseña ética profesional ni un método de juicio ético.',
  'm6': 'Corresponde en parte. Los cuatro laboratorios piden hacer una prueba o un modelo, anotar los números y explicar el resultado: un túnel de viento virtual, una hoja de la ecuación del cohete, un planeador que construyes y haces volar, y una hoja de cálculo de la atmósfera.',
 },
 'ar': {
  'h': 'التأليف والمراجعة',
  'who': 'يحدد المؤسس الاتجاه ويعتمد كل صفحة. تجلب المؤسِّسة المشاركة أكثر من 20 عاماً من الخبرة في التدريس، وهي مترجمتنا الناطقة بالعربية والفرنسية كلغة أم.',
  'check_h': 'فحص الجودة.',
  'sources': 'تُفحص الحقائق والأمثلة المحلولة والروابط في هذه الصفحة مقابل مصادر مسمّاة، منها دليل ناسا غلين للمبتدئين في علم الطيران، وMIT OpenCourseWare، وكتاب Introduction to Aerospace Flight Vehicles لـ J. Gordon Leishman.',
  'reviewed': 'آخر مراجعة',
  'when': '27 نوفمبر 2026',
  'about': 'من نحن',
  'policy': 'السياسة التحريرية والمصادر',
  'disclose': 'يضع المؤسس والمؤسِّسة المشاركة الاتجاه، ويختاران الموضوعات والنطاق، ويراجعان أسلوب التدريس، ويعتمدان كل صفحة. بحثت SI وصاغت المسودات وترجمت وتحققت من المصادر. فُحصت كل حقيقة وكل مثال محلول وكل رابط مقابل المصادر المذكورة، ثم راجعها المؤسسان قبل النشر.',
  'hub_disclose': 'يضع المؤسس والمؤسِّسة المشاركة الاتجاه، ويختاران الموضوعات والنطاق، ويراجعان أسلوب التدريس، ويعتمدان كل صفحة. بحثت SI وصاغت المسودات وترجمت وتحققت من المصادر. فُحصت كل حقيقة وكل رابط في هذه الصفحة مقابل المصادر المذكورة، ثم راجعها المؤسسان قبل النشر.',
  'guide': 'تنزيل دليل الدراسة القابل للتعديل (.docx)',
  'goals_h': 'أهداف المسار',
  'goals': 'مقررات المسار موجودة ليقود الطالب علوم الهندسة في المرحلة الجامعية على الطائرات والمركبات الفضائية، وينقل تصميمًا من المتطلبات إلى مراجعة، ويوازن الكلفة البيئية للطيران. هذه أهداف دراسة لهذا المسار المجاني، وليست درجة معتمدة.',
  'use_h': 'كيف تستخدم هذه المسارات',
  'use': 'شاهد الفيلم، ثم ادرس AERO 101 قبل المقررات اللاحقة. خذ كل مقرر بالترتيب الذي يظهر به تحت سنته.',
  'std_h': 'المواءمة مع المعايير',
  'std': 'تربط هذه الصفوف نواتج تعلم هذا المقرر بأجزاء من نواتج الطلبة في المعيار 3 لدى لجنة الاعتماد الهندسي في ABET لدورة 2025–2026. وتقول الصف «يقابل» فقط حيث يدرّس هذا المقرر ذلك الجزء فعلًا. وهذا لا يعني اعتمادًا ولا ساعات معتمدة ولا تبنّيًا من ABET.',
  'col_a': 'ناتج ABET',
  'col_b': 'أين يقابل هذا المقرر',
  'skip': 'النواتج 3 و5 و7 غير مربوطة. هذا المقرر لا يدرّس التواصل مع جمهور متنوع، ولا العمل ضمن فريق، ولا طريقة لاكتساب معرفة جديدة.',
  'src': 'المصدر',
  'm1': 'يقابل جزئيًا. تطبق الوحدات من 2 إلى 8 الهندسة والعلوم والرياضيات على مسائل تمهيدية في الغلاف الجوي والرفع والسحب والأداء والدفع والصواريخ والمدارات. وهذه ليست كامل مدى مسائل الهندسة المعقدة في تعريف ABET.',
  'm2': 'يقابل جزئيًا. تدرّس الوحدة 1 المتطلبات ودورة التصميم ودراسات المفاضلة. وتقارن الوحدة 9 الكلفة البيئية للطيران. وتتضمن المختبرات ملاحظة سلامة. ولا يدرّس المقرر عوامل الصحة العامة والعوامل الثقافية والاجتماعية والاقتصادية في هذا الناتج.',
  'm4': 'يقابل جزئيًا. تتناول الوحدة 9 الأثر البيئي والمجتمعي لانبعاثات الطيران والحطام المداري. ولا يدرّس المقرر أخلاقيات المهنة ولا طريقة للحكم الأخلاقي.',
  'm6': 'يقابل جزئيًا. تطلب المختبرات الأربعة إجراء اختبار أو نموذج، وتسجيل الأرقام، وشرح النتيجة: نفق رياح افتراضي، وورقة معادلة الصاروخ، وطائرة شراعية تبنيها وتطيرها، وجدول غلاف جوي.',
 },
 'it': {
  'h': 'Autori e revisione',
  'who': 'Il Fondatore indica la direzione e approva ogni pagina. La Cofondatrice porta più di 20 anni di esperienza nell’insegnamento ed è la nostra traduttrice madrelingua araba e francese.',
  'check_h': 'Controllo di qualità.',
  'sources': 'I fatti, gli esempi svolti e i link di questa pagina sono controllati su fonti nominate, tra cui la Beginner’s Guide to Aeronautics della NASA Glenn, il MIT OpenCourseWare e Introduction to Aerospace Flight Vehicles di J. Gordon Leishman.',
  'reviewed': 'Ultima revisione',
  'when': '27 novembre 2026',
  'about': 'Chi siamo',
  'policy': 'Politica editoriale e delle fonti',
  'disclose': 'Il Fondatore e la Cofondatrice indicano la direzione, scelgono i temi e l’ambito, rivedono l’approccio didattico e approvano ogni pagina. SI ha ricercato, redatto, tradotto e controllato le fonti. Ogni fatto, esempio svolto e link è stato controllato sulle fonti indicate e rivisto dai fondatori prima della pubblicazione.',
  'hub_disclose': 'Il Fondatore e la Cofondatrice indicano la direzione, scelgono i temi e l’ambito, rivedono l’approccio didattico e approvano ogni pagina. SI ha ricercato, redatto, tradotto e controllato le fonti. Ogni fatto e ogni link di questa pagina è stato controllato sulle fonti indicate e rivisto dai fondatori prima della pubblicazione.',
  'guide': 'Scarica la guida di studio modificabile (.docx)',
  'goals_h': 'Obiettivi del percorso',
  'goals': 'I corsi di un indirizzo servono perché uno studente applichi le scienze ingegneristiche di primo livello ad aerei e veicoli spaziali, porti un progetto dai requisiti fino a una revisione e valuti il costo ambientale del volo. Sono obiettivi di studio di questo percorso gratuito, non una laurea accreditata.',
  'use_h': 'Come usare questi indirizzi',
  'use': 'Guarda il film, poi studia AERO 101 prima dei corsi successivi. Segui ogni corso nell’ordine in cui compare sotto il suo anno.',
  'std_h': 'Allineamento agli standard',
  'std': 'Queste righe collegano i risultati di apprendimento di questo corso a parti degli student outcomes del Criterio 3 dell’Engineering Accreditation Commission di ABET per il 2025–2026. Una riga dice «corrisponde a» solo dove questo corso insegna davvero quella parte. Questo non implica accreditamento, crediti accademici o un endorsement di ABET.',
  'col_a': 'Risultato ABET',
  'col_b': 'Dove corrisponde questo corso',
  'skip': 'I risultati 3, 5 e 7 non sono collegati. Questo corso non insegna la comunicazione verso pubblici diversi, il lavoro di squadra, né un metodo per acquisire nuove conoscenze.',
  'src': 'Fonte',
  'm1': 'Corrisponde in parte. Le unità da 2 a 8 applicano ingegneria, scienze e matematica a problemi introduttivi su atmosfera, portanza e resistenza, prestazioni, propulsione, razzi e orbite. Non sono l’intera gamma dei problemi ingegneristici complessi della definizione ABET.',
  'm2': 'Corrisponde in parte. L’unità 1 insegna requisiti, ciclo di progettazione e studi di compromesso. L’unità 9 confronta il costo ambientale del volo. I laboratori includono una nota di sicurezza. Il corso non insegna i fattori di salute pubblica, culturali, sociali ed economici di questo risultato.',
  'm4': 'Corrisponde in parte. L’unità 9 tratta l’impatto ambientale e sociale delle emissioni dell’aviazione e dei detriti orbitali. Il corso non insegna l’etica professionale né un metodo di giudizio etico.',
  'm6': 'Corrisponde in parte. I quattro laboratori chiedono di eseguire una prova o un modello, annotare i numeri e spiegare il risultato: una galleria del vento virtuale, un foglio sull’equazione del razzo, un aliante da costruire e far volare, e un foglio di calcolo dell’atmosfera.',
 },
 'he': {
  'h': 'מחברים וסקירה',
  'who': 'המייסד קובע את הכיוון ומאשר כל דף. המייסדת השותפה מביאה יותר מ־20 שנות ניסיון בהוראה, והיא המתרגמת שלנו שערבית וצרפתית הן שפות האם שלה.',
  'check_h': 'בקרת איכות.',
  'sources': 'עובדות, דוגמאות פתורות וקישורים בעמוד זה נבדקים מול מקורות נקובים, ובהם המדריך למתחילים באווירונאוטיקה של נאס״א גלן, MIT OpenCourseWare, ו־Introduction to Aerospace Flight Vehicles מאת J. Gordon Leishman.',
  'reviewed': 'נבדק לאחרונה',
  'when': '27 בנובמבר 2026',
  'about': 'אודות',
  'policy': 'מדיניות עריכה ומקורות',
  'disclose': 'המייסד והמייסדת השותפה קובעים את הכיוון, בוחרים את הנושאים ואת ההיקף, בודקים את גישת ההוראה ומאשרים כל דף. SI חקר, ניסח, תרגם ובדק את המקורות. כל עובדה, דוגמה פתורה וקישור נבדקו מול המקורות הנקובים ונבחנו על ידי המייסדים לפני הפרסום.',
  'hub_disclose': 'המייסד והמייסדת השותפה קובעים את הכיוון, בוחרים את הנושאים ואת ההיקף, בודקים את גישת ההוראה ומאשרים כל דף. SI חקר, ניסח, תרגם ובדק את המקורות. כל עובדה וכל קישור בעמוד זה נבדקו מול המקורות הנקובים ונבחנו על ידי המייסדים לפני הפרסום.',
  'guide': 'הורדת מדריך הלימוד הניתן לעריכה (.docx)',
  'goals_h': 'מטרות המסלול',
  'goals': 'הקורסים במסלול נועדו כדי שסטודנט יוכל ליישם מדעי הנדסה לתואר ראשון על כלי טיס וחלליות, להוביל תכן מדרישות ועד סקירה, ולשקול את העלות הסביבתית של טיסה. אלה מטרות לימוד למסלול החינמי הזה, לא תואר מוכר.',
  'use_h': 'איך להשתמש במסלולים האלה',
  'use': 'צפו בסרטון, ואז למדו את AERO 101 לפני הקורסים המאוחרים יותר. למדו כל קורס לפי הסדר שבו הוא מופיע תחת השנה שלו.',
  'std_h': 'התאמה לתקנים',
  'std': 'השורות האלה ממפות את תוצרי הלמידה של הקורס לחלקים מתוצרי הסטודנטים בקריטריון 3 של ועדת ההסמכה להנדסה של ABET למחזור 2025–2026. שורה אומרת «ממופה אל» רק במקום שבו הקורס הזה באמת מלמד את החלק. אין בכך הסמכה, נקודות זכות אקדמיות, או המלצה של ABET.',
  'col_a': 'תוצר ABET',
  'col_b': 'איפה הקורס ממופה',
  'skip': 'תוצרים 3, 5 ו־7 אינם ממופים. הקורס הזה אינו מלמד תקשורת לקהלים מגוונים, עבודת צוות, או שיטה לרכישת ידע חדש.',
  'src': 'מקור',
  'm1': 'ממופה חלקית. יחידות 2 עד 8 מיישמות הנדסה, מדע ומתמטיקה על בעיות מבוא באטמוספרה, עילוי וגרר, ביצועים, הנעה, רקטות ומסלולים. אלה אינם כל טווח בעיות ההנדסה המורכבות בהגדרה של ABET.',
  'm2': 'ממופה חלקית. יחידה 1 מלמדת דרישות, מחזור תכן ומחקרי חלופות. יחידה 9 משווה את העלות הסביבתית של טיסה. במעבדות יש הערת בטיחות. הקורס אינו מלמד את גורמי בריאות הציבור, התרבות, החברה והכלכלה שבתוצר הזה.',
  'm4': 'ממופה חלקית. יחידה 9 עוסקת בהשפעה הסביבתית והחברתית של פליטות תעופה ופסולת מסלולית. הקורס אינו מלמד אתיקה מקצועית או שיטה לשיקול דעת אתי.',
  'm6': 'ממופה חלקית. ארבע המעבדות מבקשות להריץ ניסוי או מודל, לרשום את המספרים ולהסביר את התוצאה: מנהרת רוח וירטואלית, גיליון משוואת הרקטה, דאון שבונים ומטיסים, וגיליון אטמוספרה.',
 },
}

CSS = (
    '.crs-review{margin:0 0 .85rem;padding:.8rem .95rem;border-radius:18px;border:1px solid rgba(255,255,255,.3);'
    'background:linear-gradient(165deg,rgba(255,255,255,.16),rgba(255,255,255,.04) 48%,rgba(8,20,36,.24));'
    'box-shadow:inset 0 1px 0 rgba(255,255,255,.38),0 10px 24px rgba(0,0,0,.18)}'
    '.crs-review h2{margin:.05rem 0 .35rem;font-size:1.05rem}'
    '.crs-review p{margin:.35rem 0}'
    '.crs-review-links{display:flex;flex-wrap:wrap;gap:.4rem;margin:.55rem 0 0}'
    '.crs-review-links a{min-height:44px;display:inline-flex;align-items:center;padding:0 .85rem;border-radius:999px;'
    'border:1px solid rgba(255,255,255,.32);text-decoration:none;color:inherit;'
    'background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.04))}'
    '.crs-use{margin:0 0 .7rem;padding:.75rem .95rem;border-radius:16px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.05)}'
    '.crs-use h2{margin:.15rem 0 .25rem;font-size:1.02rem}'
    '.crs-use h2:first-child{margin-top:0}'
    '.crs-use p{margin:.25rem 0 .45rem}'
    '.crs-std{margin:.9rem 0 0}'
    '.crs-std h2{margin:0 0 .4rem;font-size:1.15rem}'
)

def e(s):
    return html.escape(s, quote=True)

_NAMES = ('NASA Glenn’s Beginner’s Guide to Aeronautics', 'Beginner’s Guide to Aeronautics',
          'MIT OpenCourseWare', 'Introduction to Aerospace Flight Vehicles', 'J. Gordon Leishman',
          'NASA Glenn', 'Engineering Accreditation Commission', 'ABET', 'AERO 101', 'SI')

def _wrap(s, repl):
    parts = re.split(r'(<bdi dir="ltr">.*?</bdi>)', s)
    return ''.join(part if part.startswith('<bdi') else repl(part) for part in parts)

def _latins(s):
    """Keep Latin names and numbers in bdi so Arabic and Hebrew punctuation stays put."""
    for name in _NAMES:
        token = f'<bdi dir="ltr">{html.escape(name)}</bdi>'
        s = _wrap(s, lambda part, name=html.escape(name), token=token: part.replace(name, token))
    return _wrap(s, lambda part: re.sub(r'(?<![\w>])(\d+(?:\+|(?:[–-]\d+))?)', r'<bdi dir="ltr">\1</bdi>', part))

def box(lang, quality=False, disclosure=False, when_iso=None, when_label=None):
    t = T[lang]
    iso = when_iso or REVIEWED
    label = when_label or t['when']
    parts = [f'<section class="crs-review" id="authorship" aria-labelledby="authorship-h"><h2 id="authorship-h">{e(t["h"])}</h2>',
             f'<p>{_latins(e(t["who"]))}</p>']
    if quality:
        parts.append(f'<p><b>{e(t["check_h"])}</b> {_latins(e(t["sources"]))} {e(CHK[lang])}</p>')
    if disclosure:
        parts.append(f'<p class="crs-disclose">{_latins(e(t["hub_disclose"]))}</p>')
    parts.append(f'<p><b>{e(t["reviewed"])}:</b> <time datetime="{e(iso)}">{_latins(e(label))}</time></p>')
    parts.append(f'<p class="crs-review-links"><a href="About.html">{e(t["about"])}</a>'
                 f'<a href="Editorial_Policy.html">{e(t["policy"])}</a></p></section>')
    return ''.join(parts)

def disclose(lang):
    return _latins(e(T[lang]['disclose']))

def use_block(lang):
    t = T[lang]
    return (f'<section class="crs-use" id="path-goals" aria-labelledby="path-goals-h">'
            f'<h2 id="path-goals-h">{e(t["goals_h"])}</h2><p>{_latins(e(t["goals"]))}</p>'
            f'<h2>{e(t["use_h"])}</h2><p>{_latins(e(t["use"]))}</p></section>')

def alignment(lang):
    t = T[lang]
    rows = []
    for n in ('1', '2', '4', '6'):
        rows.append('<tr><td>' + e(n) + '. <bdi dir="ltr">' + e(ABET_OUT[n]) + '</bdi></td><td>'
                    + _latins(e(t['m' + n])) + '</td></tr>')
    return (f'<div class="crs-std"><h2>{e(t["std_h"])}</h2><p>{_latins(e(t["std"]))}</p>'
            f'<div class="crs-tw"><table class="crs-tbl"><thead><tr><th scope="col">{e(t["col_a"])}</th>'
            f'<th scope="col">{e(t["col_b"])}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<p>{e(t["skip"])}</p><p>{e(t["src"])}: <a href="{ABET}" rel="noopener"><bdi dir="ltr">ABET</bdi> '
            f'Engineering Accreditation Commission, Criterion 3 (2025–2026)</a>.</p></div>')

def guide_href(lang):
    name = 'Intro_to_Aerospace_Engineering_Study_Guide' + ('' if lang == 'en' else '_' + lang) + '.docx'
    pre = '' if lang == 'en' else '../'
    return pre + 'assets/courses/' + name

def guide_link(lang):
    return f' <a class="crs-btn" href="{guide_href(lang)}" download>{e(T[lang]["guide"])}</a>'
