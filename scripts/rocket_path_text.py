"""Oct 28 2026 (founder, follow-up to #153): text + data for Learn_Rocket_Propulsion.html, "Aerospace Studies with a focus on
Rocket Propulsion" (6 langs). Same look as Learn_Jet_Propulsion.html. Every spec below carries its source and date; nothing is
estimated. Where SpaceX's numbers changed over time, the newest official SpaceX figure is used and the older one is noted.
Raptor 4 = only what Elon Musk said publicly (Oct 26 2026), shown as an announced target. fr/es/ar/it/he text is machine-drafted.
Links in BEST / JET_BEST were checked with curl on Oct 28 2026 (404s dropped)."""
L6 = ('en', 'fr', 'es', 'ar', 'it', 'he')
def T(*a): return dict(zip(L6, a))
PAGE = 'Learn_Rocket_Propulsion.html'
NAME = T('Aerospace Studies with a focus on Rocket Propulsion',
 'Études aérospatiales, spécialité propulsion des fusées',
 'Estudios aeroespaciales con enfoque en propulsión de cohetes',
 'دراسات الطيران والفضاء مع التركيز على دفع الصواريخ',
 'Studi aerospaziali con focus sulla propulsione a razzo',
 'לימודי תעופה וחלל עם דגש על הנעה רקטית')
SHORT = T('Aerospace: Rocket Propulsion', 'Aérospatial : fusées', 'Aeroespacial: cohetes', 'الفضاء: دفع الصواريخ', 'Aerospaziale: razzi', 'תעופה וחלל: הנעה רקטית')
LINE = T('Thrust, Isp, the rocket equation, nozzles and engine cycles, then today’s engines, 30 years of launch footage, and where to study.',
 'Poussée, Isp, équation de la fusée, tuyères et cycles moteurs, puis les moteurs d’aujourd’hui, 30 ans d’images de lancements et où étudier.',
 'Empuje, Isp, la ecuación del cohete, toberas y ciclos de motor; luego los motores de hoy, 30 años de lanzamientos y dónde estudiar.',
 'الدفع، والدفع النوعي، ومعادلة الصاروخ، والفوهات ودورات المحركات، ثم محركات اليوم، و30 عامًا من لقطات الإطلاق، وأين تدرس.',
 'Spinta, Isp, equazione del razzo, ugelli e cicli motore; poi i motori di oggi, 30 anni di lanci filmati e dove studiare.',
 'דחף, דחף סגולי, משוואת הרקטה, נחירים ומחזורי מנוע, ואז המנועים של היום, 30 שנות צילומי שיגור והיכן ללמוד.')
UI = {
 'mt': T('', 'Traduction rédigée par machine, à relire.', 'Traducción redactada por máquina, pendiente de revisión.', 'ترجمة آلية بانتظار المراجعة.', 'Traduzione redatta a macchina, da rivedere.', 'תרגום מכונה, ממתין לבדיקה.'),
 'anim': T('Animation: a rocket engine firing, with shock diamonds in the exhaust', 'Animation : un moteur-fusée en marche, avec des disques de Mach dans le jet', 'Animación: un motor cohete encendido, con diamantes de choque en el chorro', 'رسم متحرك: محرك صاروخي يعمل مع ماسات الصدمة في العادم', 'Animazione: un motore a razzo acceso, con diamanti d’urto nello scarico', 'הנפשה: מנוע רקטי פועל, עם יהלומי הלם בפליטה'),
 'fund_h': T('The fundamentals', 'Les bases', 'Los fundamentos', 'الأساسيات', 'I fondamenti', 'היסודות'),
 'unit': T('Course unit', 'Unité du cours', 'Unidad del curso', 'وحدة المقرر', 'Unità del corso', 'יחידה בקורס'),
 'calc': T('Calculator', 'Calculateur', 'Calculadora', 'حاسبة', 'Calcolatore', 'מחשבון'),
 'new_h': T('Latest and greatest: SpaceX Raptor', 'Le plus récent : Raptor de SpaceX', 'Lo más nuevo: Raptor de SpaceX', 'الأحدث: محرك Raptor من SpaceX', 'Il meglio di oggi: Raptor di SpaceX', 'החדש ביותר: Raptor של SpaceX'),
 'new_t': T('Raptor burns liquid methane and liquid oxygen (methalox) in a full-flow staged combustion cycle. Numbers below are SpaceX’s, with the date each was published.',
   'Raptor brûle du méthane et de l’oxygène liquides (méthalox) en cycle à combustion étagée à flux complet. Chiffres de SpaceX, avec leur date de publication.',
   'Raptor quema metano y oxígeno líquidos (metalox) en un ciclo de combustión escalonada de flujo completo. Cifras de SpaceX, con su fecha de publicación.',
   'يحرق Raptor الميثان والأكسجين السائلين (ميثالوكس) في دورة احتراق مرحلي كامل التدفق. الأرقام أدناه من SpaceX مع تاريخ نشر كل منها.',
   'Raptor brucia metano e ossigeno liquidi (metalox) in un ciclo a combustione stadiata a flusso completo. Numeri di SpaceX, con la data di pubblicazione.',
   'Raptor שורף מתאן וחמצן נוזליים (מתאלוקס) במחזור בעירה מדורגת בזרימה מלאה. המספרים הם של SpaceX, עם תאריך הפרסום של כל אחד.'),
 'ver': T('Version', 'Version', 'Versión', 'الإصدار', 'Versione', 'גרסה'),
 'sl': T('Thrust, sea level', 'Poussée, niveau mer', 'Empuje, nivel del mar', 'الدفع عند سطح البحر', 'Spinta, livello del mare', 'דחף, גובה פני הים'),
 'vac': T('Thrust, vacuum version', 'Poussée, version vide', 'Empuje, versión de vacío', 'الدفع، نسخة الفراغ', 'Spinta, versione vuoto', 'דחף, גרסת ריק'),
 'mass': T('Engine mass', 'Masse du moteur', 'Masa del motor', 'كتلة المحرك', 'Massa del motore', 'מסת המנוע'),
 'status': T('Status', 'Statut', 'Estado', 'الحالة', 'Stato', 'מצב'),
 'src': T('Source', 'Source', 'Fuente', 'المصدر', 'Fonte', 'מקור'),
 'flown': T('Flown', 'A volé', 'Ha volado', 'طار', 'Ha volato', 'טס'),
 'flying': T('Flying (Starship V3)', 'En vol (Starship V3)', 'En vuelo (Starship V3)', 'يطير (Starship V3)', 'In volo (Starship V3)', 'טס (Starship V3)'),
 'planned': T('Announced / planned', 'Annoncé / prévu', 'Anunciado / previsto', 'معلن / مخطط', 'Annunciato / previsto', 'הוכרז / מתוכנן'),
 'nr': T('not published', 'non publié', 'no publicado', 'غير منشور', 'non pubblicato', 'לא פורסם'),
 'same': T('“hopefully about the same mass” as Raptor 3', '« à peu près la même masse, on l’espère » que Raptor 3', '“ojalá con más o menos la misma masa” que Raptor 3', '"نأمل أن تكون بالكتلة نفسها تقريبًا" مثل Raptor 3', '“si spera più o meno la stessa massa” di Raptor 3', '"בתקווה בערך אותה מסה" כמו Raptor 3'),
 'notes_h': T('What changed, and what is still a plan', 'Ce qui a changé, et ce qui reste un projet', 'Qué cambió y qué sigue siendo un plan', 'ما الذي تغيّر وما الذي لا يزال خطة', 'Cosa è cambiato e cosa è ancora un piano', 'מה השתנה ומה עדיין תוכנית'),
 'bench_h': T('30 Years of Raw Power', '30 ans de puissance brute', '30 años de potencia bruta', '30 عامًا من القوة الخام', '30 anni di pura potenza', '30 שנה של עוצמה גולמית'),
 'bench_t': T('Real launch and test-fire footage, oldest to newest. Videos load only when you press play.', 'De vraies images de lancements et d’essais, du plus ancien au plus récent. Les vidéos ne se chargent que si vous lancez la lecture.', 'Lanzamientos y pruebas reales, del más antiguo al más reciente. Los videos solo cargan al pulsar reproducir.', 'لقطات حقيقية للإطلاق واختبارات الإشعال، من الأقدم إلى الأحدث. لا تُحمَّل الفيديوهات إلا عند الضغط على تشغيل.', 'Lanci e prove reali, dal più vecchio al più recente. I video si caricano solo quando premi play.', 'צילומי שיגור וניסויי הפעלה אמיתיים, מהישן לחדש. הסרטונים נטענים רק כשלוחצים על הפעלה.'),
 'play': T('Play video (loads from YouTube)', 'Lire la vidéo (chargée depuis YouTube)', 'Reproducir video (se carga desde YouTube)', 'تشغيل الفيديو (يُحمَّل من YouTube)', 'Riproduci il video (da YouTube)', 'הפעלת סרטון (נטען מ-YouTube)'),
 'watch': T('Watch on SpaceX.com', 'Voir sur SpaceX.com', 'Ver en SpaceX.com', 'شاهد على SpaceX.com', 'Guarda su SpaceX.com', 'צפייה ב-SpaceX.com'),
 'rocket': T('Vehicle / test', 'Lanceur / essai', 'Vehículo / prueba', 'المركبة / الاختبار', 'Veicolo / prova', 'רכב / ניסוי'),
 'date': T('Date', 'Date', 'Fecha', 'التاريخ', 'Data', 'תאריך'),
 'eng': T('Engine', 'Moteur', 'Motor', 'المحرك', 'Motore', 'מנוע'),
 'per': T('Thrust per engine', 'Poussée par moteur', 'Empuje por motor', 'الدفع لكل محرك', 'Spinta per motore', 'דחף למנוע'),
 'tot': T('Total liftoff thrust', 'Poussée totale au décollage', 'Empuje total al despegue', 'إجمالي دفع الإقلاع', 'Spinta totale al decollo', 'דחף המראה כולל'),
 'pc': T('Chamber pressure', 'Pression de chambre', 'Presión de cámara', 'ضغط الحجرة', 'Pressione in camera', 'לחץ תא'),
 'isp': T('Isp', 'Isp', 'Isp', 'الدفع النوعي', 'Isp', 'דחף סגולי'),
 'prop': T('Propellant', 'Ergols', 'Propelente', 'الوقود', 'Propellente', 'הדף'),
 'chart_h': T('Thrust per engine over time (kN)', 'Poussée par moteur au fil du temps (kN)', 'Empuje por motor a lo largo del tiempo (kN)', 'الدفع لكل محرك عبر الزمن (كيلونيوتن)', 'Spinta per motore nel tempo (kN)', 'דחף למנוע לאורך זמן (קילוניוטון)'),
 'chart_n': T('Sea-level thrust unless marked “vac” (NASA quotes RS-25 in vacuum). Dashed bar = announced target, not flown. Conversions: 1 tf = 9.80665 kN, 1 lbf = 4.448 N.',
   'Poussée au niveau de la mer sauf mention « vide » (la NASA donne le RS-25 dans le vide). Barre en pointillés = objectif annoncé, pas encore volé. Conversions : 1 tf = 9,80665 kN, 1 lbf = 4,448 N.',
   'Empuje a nivel del mar salvo “vacío” (la NASA da el RS-25 en vacío). Barra discontinua = objetivo anunciado, aún no voló. Conversión: 1 tf = 9,80665 kN, 1 lbf = 4,448 N.',
   'الدفع عند سطح البحر ما لم يُذكر "فراغ" (تذكر NASA محرك RS-25 في الفراغ). العمود المتقطع = هدف معلن لم يطر بعد. التحويل: 1 طن قوة = 9.80665 كيلونيوتن، 1 رطل قوة = 4.448 نيوتن.',
   'Spinta al livello del mare salvo “vuoto” (la NASA indica l’RS-25 nel vuoto). Barra tratteggiata = obiettivo annunciato, non ancora volato. Conversioni: 1 tf = 9,80665 kN, 1 lbf = 4,448 N.',
   'דחף בגובה פני הים אלא אם צוין "ריק" (NASA מציינת את RS-25 בריק). עמודה מקווקוות = יעד שהוכרז, טרם טס. המרות: 1 טון-כוח = 9.80665 קילוניוטון, 1 lbf = 4.448 ניוטון.'),
 'pc_n': T('Chamber pressure and Isp are left blank where the maker has not published a current figure. The one sourced Raptor value: 350 bar reached in a Raptor 3 ground test (Elon Musk, May 13, 2023), a test result, not a rating.',
   'Pression de chambre et Isp restent vides quand le fabricant n’a pas publié de chiffre actuel. Seule valeur sourcée pour Raptor : 350 bar atteints lors d’un essai au sol de Raptor 3 (Elon Musk, 13 mai 2023), un résultat d’essai, pas une valeur nominale.',
   'La presión de cámara y el Isp quedan en blanco si el fabricante no ha publicado una cifra actual. Único valor con fuente de Raptor: 350 bar en una prueba en tierra de Raptor 3 (Elon Musk, 13 de mayo de 2023), un resultado de prueba, no un valor nominal.',
   'تُترك خانات ضغط الحجرة والدفع النوعي فارغة حين لا تنشر الشركة رقمًا حاليًا. القيمة الوحيدة الموثقة لـ Raptor: ‏350 بار في اختبار أرضي لـ Raptor 3 (إيلون ماسك، 13 مايو 2023)، وهي نتيجة اختبار لا قيمة تشغيلية.',
   'Pressione in camera e Isp restano vuoti se il costruttore non ha pubblicato un valore attuale. L’unico valore Raptor con fonte: 350 bar in una prova a terra di Raptor 3 (Elon Musk, 13 maggio 2023), un risultato di prova, non un valore nominale.',
   'לחץ התא והדחף הסגולי נשארים ריקים כשהיצרן לא פרסם נתון עדכני. הערך היחיד עם מקור ל-Raptor: ‏350 בר בניסוי קרקעי של Raptor 3 (אילון מאסק, 13 במאי 2023), תוצאת ניסוי ולא דירוג.'),
 'best_h': T('Learn from the best', 'Apprendre auprès des meilleurs', 'Aprende de los mejores', 'تعلّم من الأفضل', 'Impara dai migliori', 'ללמוד מהטובים ביותר'),
 'best_t': T('Free courses, top programs and real career paths. No affiliation or endorsement; links checked Oct 28, 2026.', 'Cours gratuits, grands programmes et vrais débouchés. Aucune affiliation ni recommandation ; liens vérifiés le 28 oct. 2026.', 'Cursos gratis, grandes programas y carreras reales. Sin afiliación ni respaldo; enlaces revisados el 28 oct. 2026.', 'دورات مجانية وبرامج رائدة ومسارات مهنية حقيقية. لا انتساب ولا تزكية؛ رُوجعت الروابط في 28 أكتوبر 2026.', 'Corsi gratuiti, grandi programmi e carriere vere. Nessuna affiliazione o approvazione; link verificati il 28 ott. 2026.', 'קורסים חינמיים, תוכניות מובילות ומסלולי קריירה אמיתיים. ללא שיוך או המלצה; הקישורים נבדקו ב-28 באוקטובר 2026.'),
 'g_free': T('Free courses', 'Cours gratuits', 'Cursos gratis', 'دورات مجانية', 'Corsi gratuiti', 'קורסים חינמיים'),
 'g_uni': T('University programs and labs', 'Universités et laboratoires', 'Universidades y laboratorios', 'برامج ومختبرات جامعية', 'Università e laboratori', 'תוכניות ומעבדות אוניברסיטאיות'),
 'g_nasa': T('NASA', 'NASA', 'NASA', 'NASA', 'NASA', 'NASA'),
 'g_job': T('Careers and internships', 'Carrières et stages', 'Empleos y prácticas', 'الوظائف والتدريب', 'Carriere e tirocini', 'קריירה והתמחויות'),
 'to_jet': T('Prefer jet engines? See the Jet Propulsion track', 'Plutôt réacteurs ? Voir le parcours propulsion par réaction', '¿Prefieres motores a reacción? Mira la ruta de propulsión a reacción', 'تفضّل المحركات النفاثة؟ اطّلع على مسار الدفع النفاث', 'Preferisci i motori a getto? Vedi il percorso propulsione a getto', 'מעדיפים מנועי סילון? ראו את מסלול ההנעה הסילונית'),
 'to_rocket': T('Also see: Aerospace Studies with a focus on Rocket Propulsion', 'Voir aussi : Études aérospatiales, spécialité propulsion des fusées', 'Mira también: Estudios aeroespaciales con enfoque en propulsión de cohetes', 'اطّلع أيضًا على: دراسات الطيران والفضاء مع التركيز على دفع الصواريخ', 'Vedi anche: Studi aerospaziali con focus sulla propulsione a razzo', 'ראו גם: לימודי תעופה וחלל עם דגש על הנעה רקטית'),
 'credit': T('Specs from SpaceX, NASA and the outlets cited, as of Oct 28, 2026. Videos: NASA (public domain) and SpaceX (official players). Independent study guide: no affiliation, credit or endorsement.',
   'Données de SpaceX, de la NASA et des médias cités, au 28 oct. 2026. Vidéos : NASA (domaine public) et SpaceX (lecteurs officiels). Guide d’étude indépendant : aucune affiliation, aucun crédit, aucune recommandation.',
   'Datos de SpaceX, la NASA y los medios citados, al 28 oct. 2026. Videos: NASA (dominio público) y SpaceX (reproductores oficiales). Guía de estudio independiente: sin afiliación, créditos ni respaldo.',
   'المواصفات من SpaceX وNASA والمصادر المذكورة حتى 28 أكتوبر 2026. الفيديوهات: NASA (ملكية عامة) وSpaceX (مشغلات رسمية). دليل دراسة مستقل: لا انتساب ولا اعتماد ولا تزكية.',
   'Dati di SpaceX, NASA e delle testate citate, al 28 ott. 2026. Video: NASA (pubblico dominio) e SpaceX (player ufficiali). Guida di studio indipendente: nessuna affiliazione, credito o approvazione.',
   'נתונים מ-SpaceX, NASA ומקורות שצוטטו, נכון ל-28 באוקטובר 2026. סרטונים: NASA (נחלת הכלל) ו-SpaceX (נגנים רשמיים). מדריך לימוד עצמאי: ללא שיוך, נקודות זכות או המלצה.'),
}
# Fundamentals: (emoji, title, one line, formula or None, links [(href, label-key or literal)])
FUND = [
 ('🚀', T('Thrust', 'Poussée', 'Empuje', 'الدفع', 'Spinta', 'דחף'),
  T('Throw mass backward fast and the rocket is pushed forward (Newton’s third law). It works in vacuum.', 'Éjecter de la masse vers l’arrière très vite pousse la fusée vers l’avant (3e loi de Newton). Cela marche dans le vide.', 'Expulsar masa hacia atrás muy rápido empuja el cohete hacia delante (3.ª ley de Newton). Funciona en el vacío.', 'دفع الكتلة إلى الخلف بسرعة يدفع الصاروخ إلى الأمام (قانون نيوتن الثالث)، ويعمل ذلك في الفراغ.', 'Espellere massa all’indietro molto in fretta spinge il razzo in avanti (terza legge di Newton). Funziona nel vuoto.', 'השלכת מסה לאחור במהירות דוחפת את הרקטה קדימה (החוק השלישי של ניוטון). זה עובד גם בריק.'),
  'F = ṁ·vₑ + (pₑ − pₐ)·Aₑ', [('Propulsion.html#u7', 'unit7'), ('Thrust_to_Weight_Calculator.html', 'calc')]),
 ('⏱️', T('Specific impulse (Isp)', 'Impulsion spécifique (Isp)', 'Impulso específico (Isp)', 'الدفع النوعي (Isp)', 'Impulso specifico (Isp)', 'דחף סגולי (Isp)'),
  T('Thrust per unit of propellant weight burned each second. Higher Isp = more push from the same fuel.', 'Poussée par poids d’ergols brûlé chaque seconde. Isp plus élevée = plus de poussée avec le même carburant.', 'Empuje por peso de propelente quemado cada segundo. Más Isp = más empuje con el mismo combustible.', 'الدفع لكل وحدة وزن من الوقود المحترق في الثانية. Isp أعلى = دفع أكبر من الوقود نفسه.', 'Spinta per peso di propellente bruciato ogni secondo. Isp più alto = più spinta con lo stesso carburante.', 'דחף לכל יחידת משקל הדף שנשרף בשנייה. Isp גבוה יותר = יותר דחף מאותו דלק.'),
  'Isp = F / (ṁ·g₀)', [('Propulsion.html#u7', 'unit7')]),
 ('📈', T('The rocket equation', 'L’équation de la fusée', 'La ecuación del cohete', 'معادلة الصاروخ', 'L’equazione del razzo', 'משוואת הרקטה'),
  T('How much speed change (Δv) you get from exhaust speed and the ratio of full to empty mass. It is why rockets stage.', 'Le gain de vitesse (Δv) selon la vitesse d’éjection et le rapport masse pleine/vide. D’où les étages.', 'Cuánto cambio de velocidad (Δv) se obtiene según la velocidad de escape y la razón de masa llena/vacía. Por eso hay etapas.', 'مقدار تغيّر السرعة (Δv) بحسب سرعة العادم ونسبة الكتلة الممتلئة إلى الفارغة، ولهذا تُبنى الصواريخ على مراحل.', 'Quanto cambio di velocità (Δv) si ottiene dalla velocità di scarico e dal rapporto massa piena/vuota. Per questo i razzi hanno stadi.', 'כמה שינוי מהירות (Δv) מקבלים ממהירות הפליטה ומיחס המסה המלאה לריקה. לכן לרקטות יש שלבים.'),
  'Δv = vₑ · ln(m₀ / m_f)', [('Propulsion.html#u9', 'unit9'), ('Delta_V_Calculator.html', 'calc')]),
 ('🔔', T('Nozzles', 'Tuyères', 'Toberas', 'الفوهات', 'Ugelli', 'נחירים'),
  T('A converging-diverging bell turns hot, high-pressure gas into a supersonic jet. Bigger bells suit vacuum; shorter ones sea level.', 'Une cloche convergente-divergente transforme le gaz chaud sous pression en jet supersonique. Grandes cloches pour le vide, plus courtes au sol.', 'Una campana convergente-divergente convierte gas caliente a presión en un chorro supersónico. Campanas grandes para el vacío; cortas al nivel del mar.', 'الفوهة المتقاربة المتباعدة تحوّل الغاز الساخن عالي الضغط إلى نفاثة فوق صوتية. الفوهات الكبيرة للفراغ والقصيرة لسطح البحر.', 'Una campana convergente-divergente trasforma gas caldo ad alta pressione in un getto supersonico. Campane grandi per il vuoto, corte al livello del mare.', 'פעמון מתכנס-מתבדר הופך גז חם בלחץ גבוה לסילון על-קולי. פעמונים גדולים מתאימים לריק, קצרים לגובה פני הים.'),
  None, [('Propulsion.html#u8', 'unit8')]),
]
CYC_H = T('Engine cycles: how the pumps are powered', 'Cycles moteurs : comment les pompes sont entraînées', 'Ciclos de motor: cómo se mueven las bombas', 'دورات المحركات: كيف تُشغَّل المضخات', 'Cicli motore: come si azionano le pompe', 'מחזורי מנוע: איך מפעילים את המשאבות')
CYC = [
 (T('Gas generator', 'Générateur de gaz', 'Generador de gas', 'مولّد الغاز', 'Generatore di gas', 'מחולל גז'),
  T('A small burner drives the turbine; its exhaust is dumped overboard. Simple. Example: Merlin (SpaceX).', 'Un petit brûleur entraîne la turbine ; ses gaz sont rejetés. Simple. Exemple : Merlin (SpaceX).', 'Un pequeño quemador mueve la turbina y su escape se expulsa. Sencillo. Ejemplo: Merlin (SpaceX).', 'موقد صغير يدير التوربين ويُطرح عادمه خارجًا. بسيط. مثال: Merlin (SpaceX).', 'Un piccolo bruciatore muove la turbina; lo scarico viene espulso. Semplice. Esempio: Merlin (SpaceX).', 'מבער קטן מניע את הטורבינה והפליטה שלו נזרקת החוצה. פשוט. דוגמה: Merlin (SpaceX).')),
 (T('Staged combustion', 'Combustion étagée', 'Combustión escalonada', 'الاحتراق المرحلي', 'Combustione stadiata', 'בעירה מדורגת'),
  T('Preburner gas goes on into the main chamber, so nothing is wasted. Example: RS-25 (Shuttle, SLS).', 'Le gaz du pré-brûleur passe ensuite dans la chambre principale : rien n’est perdu. Exemple : RS-25 (navette, SLS).', 'El gas del prequemador sigue a la cámara principal: no se desperdicia nada. Ejemplo: RS-25 (transbordador, SLS).', 'يمر غاز الموقد الأولي إلى الحجرة الرئيسية فلا يُهدر شيء. مثال: RS-25 (المكوك، SLS).', 'Il gas del prebruciatore prosegue nella camera principale: nulla va sprecato. Esempio: RS-25 (Shuttle, SLS).', 'הגז מהמבער המקדים ממשיך לתא הראשי, כך ששום דבר לא מתבזבז. דוגמה: RS-25 (המעבורת, SLS).')),
 (T('Full-flow staged combustion', 'Combustion étagée à flux complet', 'Combustión escalonada de flujo completo', 'الاحتراق المرحلي كامل التدفق', 'Combustione stadiata a flusso completo', 'בעירה מדורגת בזרימה מלאה'),
  T('Two preburners, one fuel-rich and one oxygen-rich, so all propellant flows through the turbines. Raptor was the first to fly (Starhopper, July 2019).', 'Deux pré-brûleurs, l’un riche en carburant, l’autre en oxygène : tous les ergols traversent les turbines. Raptor a été le premier à voler (Starhopper, juillet 2019).', 'Dos prequemadores, uno rico en combustible y otro en oxígeno: todo el propelente pasa por las turbinas. Raptor fue el primero en volar (Starhopper, julio de 2019).', 'موقدان أوليان، أحدهما غني بالوقود والآخر بالأكسجين، فيمر كل الوقود عبر التوربينات. كان Raptor أول محرك يطير بها (Starhopper، يوليو 2019).', 'Due prebruciatori, uno ricco di combustibile e uno di ossigeno: tutto il propellente passa nelle turbine. Raptor è stato il primo a volare (Starhopper, luglio 2019).', 'שני מבערים מקדימים, אחד עשיר בדלק ואחד עשיר בחמצן, כך שכל ההדף זורם דרך הטורבינות. Raptor היה הראשון שטס (Starhopper, יולי 2019).')),
 (T('Expander', 'Expandeur', 'Expansor', 'دورة التمدد', 'Espansore', 'מרחיב (Expander)'),
  T('Fuel warmed in the cooling jacket drives the turbine. Clean and reliable for upper stages. Example: RL10.', 'Le carburant réchauffé dans les parois entraîne la turbine. Propre et fiable pour les étages supérieurs. Exemple : RL10.', 'El combustible calentado en la camisa de refrigeración mueve la turbina. Limpio y fiable en etapas superiores. Ejemplo: RL10.', 'الوقود المسخّن في غلاف التبريد يدير التوربين. نظيف وموثوق للمراحل العليا. مثال: RL10.', 'Il combustibile scaldato nella camicia di raffreddamento muove la turbina. Pulito e affidabile per stadi superiori. Esempio: RL10.', 'דלק שהתחמם במעטפת הקירור מניע את הטורבינה. נקי ואמין לשלבים עליונים. דוגמה: RL10.')),
 (T('Electric (ion, Hall)', 'Électrique (ionique, Hall)', 'Eléctrica (iónica, Hall)', 'الكهربائي (أيوني، هول)', 'Elettrica (ionica, Hall)', 'חשמלי (יונים, הול)'),
  T('Electric fields accelerate ions. Tiny thrust, very high Isp, for months-long burns in space.', 'Des champs électriques accélèrent des ions. Poussée infime, Isp très élevée, pour des poussées de plusieurs mois.', 'Campos eléctricos aceleran iones. Empuje mínimo, Isp muy alto, para encendidos de meses en el espacio.', 'تسرّع الحقول الكهربائية الأيونات. دفع ضئيل ودفع نوعي عالٍ جدًا لعمليات تشغيل تدوم أشهرًا في الفضاء.', 'Campi elettrici accelerano ioni. Spinta minima, Isp altissimo, per accensioni di mesi nello spazio.', 'שדות חשמליים מאיצים יונים. דחף זעיר, דחף סגולי גבוה מאוד, להפעלות של חודשים בחלל.')),
]
UNITLAB = {'unit7': 7, 'unit8': 8, 'unit9': 9}
# Raptor generations. Values exactly as published; sources/dates below.
S_SPX26 = ('SpaceX, “Introducing Starship V3”, May 12, 2026', 'https://www.spacex.com/updates')
S_TESLA = ('Teslarati, Oct 26, 2026 (quotes Elon Musk on X, Oct 26, 2026)', 'https://www.teslarati.com/spacex-raising-raptor-sea-level-thrust-engine-mass-steady/')
S_SPXPG = ('SpaceX, Starship / Raptor page (read Oct 28, 2026)', 'https://www.spacex.com/vehicles/starship/raptor')
S_FFSC = ('AIAA Aerospace America, 2020 year in review', 'https://aerospaceamerica.aiaa.org/year-in-review/milestones-reached-in-development-testing-and-flight-of-new-liquid-propulsion-systems/')
S_HOP = ('Spaceflight Now, Jul 26, 2019 (Starhopper hop)', 'https://spaceflightnow.com/2019/07/26/spacexs-starship-prototype-aces-first-untethered-hop-test/')
S_350 = ('Elon Musk on X, May 13, 2023 (archived)', 'https://web.archive.org/web/20230526002156/https://twitter.com/elonmusk/status/1657249739925258240')
S_RS25 = ('NASA, SLS RS-25 Core Stage Engine fact sheet (MSFC, Dec 2025)', 'https://www.nasa.gov/reference/space-launch-system-rs-25-core-stage-engine/')
S_A1 = ('NASA Image and Video Library, Artemis I launch recap, Nov 16, 2022', 'https://images.nasa.gov/details/Artemis%20I%20Launches%20to%20the%20Moon%20(Official%20NASA%20Recap)')
S_FH = ('SpaceX, Falcon Heavy page (read Oct 28, 2026)', 'https://www.spacex.com/vehicles/falcon-heavy/')
RAPTOR = [  # (version, SL, vac, mass, status-key, sources)
 ('Raptor 1', '185 tf', None, '2,080 kg', 'flown', [S_TESLA]),
 ('Raptor 2', '230 tf (507,000 lbf)', '258 tf (568,000 lbf)', '1,630 kg', 'flown', [S_SPX26]),
 ('Raptor 3', '250 tf (551,000 lbf)', '275 tf (606,000 lbf)', '1,525 kg', 'flying', [S_SPX26, S_SPXPG]),
 ('Raptor 4', '300 tf', None, 'same', 'planned', [S_TESLA]),
]
NOTES = [
 T('Raptor 3 integrates sensors and controllers inside the engine under its thermal protection, so the engine shrouds are gone; all variants get a redesigned ignition system; SpaceX says simplification saves about 1 ton per engine at vehicle level (May 12, 2026).',
   'Raptor 3 intègre capteurs et contrôleurs dans le moteur, sous sa protection thermique : plus de carénages ; nouveau système d’allumage pour toutes les versions ; selon SpaceX, la simplification fait gagner environ 1 tonne par moteur au niveau du véhicule (12 mai 2026).',
   'Raptor 3 integra sensores y controladores dentro del motor bajo su protección térmica, sin carenados; todas las versiones tienen un encendido rediseñado; según SpaceX, la simplificación ahorra cerca de 1 tonelada por motor en el vehículo (12 de mayo de 2026).',
   'يدمج Raptor 3 الحساسات ووحدات التحكم داخل المحرك تحت حمايته الحرارية فاختفت الأغطية؛ وكل النسخ بنظام إشعال جديد؛ وتقول SpaceX إن التبسيط يوفر نحو طن لكل محرك على مستوى المركبة (12 مايو 2026).',
   'Raptor 3 integra sensori e controllori nel motore, sotto la protezione termica: niente più carenature; nuovo sistema di accensione per tutte le versioni; secondo SpaceX la semplificazione fa risparmiare circa 1 tonnellata per motore sul veicolo (12 maggio 2026).',
   'Raptor 3 משלב חיישנים ובקרים בתוך המנוע מתחת להגנה התרמית, כך שמעטפות המנוע בוטלו; לכל הגרסאות מערכת הצתה חדשה; לפי SpaceX הפישוט חוסך כטון אחד לכל מנוע ברמת הרכב (12 במאי 2026).'),
 T('Sources differ on Raptor 3 thrust: SpaceX’s 2024 target was 280 tf; its newest official figure for flight engines is 250 tf (May 12, 2026), used here. On Oct 26, 2026 Elon Musk wrote that SpaceX can “only reliably get to around 230 t-F with Raptor 3”.',
   'Les sources divergent sur la poussée de Raptor 3 : l’objectif SpaceX de 2024 était 280 tf ; le chiffre officiel le plus récent pour les moteurs de vol est 250 tf (12 mai 2026), retenu ici. Le 26 oct. 2026, Elon Musk a écrit ne pouvoir atteindre « de façon fiable qu’environ 230 t-F avec Raptor 3 ».',
   'Las fuentes difieren sobre el empuje de Raptor 3: el objetivo de SpaceX en 2024 era 280 tf; su cifra oficial más reciente para motores de vuelo es 250 tf (12 de mayo de 2026), la usada aquí. El 26 de octubre de 2026 Elon Musk escribió que “solo de forma fiable llegan a unas 230 t-F con Raptor 3”.',
   'تختلف المصادر حول دفع Raptor 3: كان هدف SpaceX في 2024 هو 280 طن قوة، وأحدث رقم رسمي لمحركات الطيران هو 250 (12 مايو 2026) وهو المعتمد هنا. وفي 26 أكتوبر 2026 كتب إيلون ماسك أنهم "لا يصلون بموثوقية إلا إلى نحو 230 طن قوة مع Raptor 3".',
   'Le fonti divergono sulla spinta di Raptor 3: l’obiettivo SpaceX del 2024 era 280 tf; il dato ufficiale più recente per i motori di volo è 250 tf (12 maggio 2026), usato qui. Il 26 ottobre 2026 Elon Musk ha scritto che si arriva “in modo affidabile solo a circa 230 t-F con Raptor 3”.',
   'המקורות חלוקים לגבי הדחף של Raptor 3: היעד של SpaceX ב-2024 היה 280 טון-כוח; הנתון הרשמי העדכני למנועי טיסה הוא 250 (12 במאי 2026), והוא המשמש כאן. ב-26 באוקטובר 2026 כתב אילון מאסק שאפשר "להגיע באמינות רק לכ-230 טון-כוח עם Raptor 3".'),
 T('Raptor 4 is announced, not built or shown: on Oct 26, 2026 Elon Musk wrote “Raptor 4 will be 300 tons of thrust at sea level and hopefully about the same mass.” SpaceX has published no Raptor 4 spec sheet, date, chamber pressure or Isp.',
   'Raptor 4 est annoncé, ni construit ni montré : le 26 oct. 2026, Elon Musk a écrit « Raptor 4 will be 300 tons of thrust at sea level and hopefully about the same mass ». SpaceX n’a publié ni fiche technique, ni date, ni pression de chambre, ni Isp.',
   'Raptor 4 está anunciado, no construido ni mostrado: el 26 de octubre de 2026 Elon Musk escribió “Raptor 4 will be 300 tons of thrust at sea level and hopefully about the same mass”. SpaceX no ha publicado ficha, fecha, presión de cámara ni Isp.',
   'Raptor 4 معلن فقط، لم يُبنَ ولم يُعرض: في 26 أكتوبر 2026 كتب إيلون ماسك: "Raptor 4 will be 300 tons of thrust at sea level and hopefully about the same mass". لم تنشر SpaceX مواصفات أو موعدًا أو ضغط حجرة أو دفعًا نوعيًا له.',
   'Raptor 4 è annunciato, non costruito né mostrato: il 26 ottobre 2026 Elon Musk ha scritto “Raptor 4 will be 300 tons of thrust at sea level and hopefully about the same mass”. SpaceX non ha pubblicato scheda, data, pressione in camera o Isp.',
   'Raptor 4 הוכרז בלבד, לא נבנה ולא הוצג: ב-26 באוקטובר 2026 כתב אילון מאסק: "Raptor 4 will be 300 tons of thrust at sea level and hopefully about the same mass". SpaceX לא פרסמה מפרט, מועד, לחץ תא או דחף סגולי.'),
]
NOTE_SRC = [[S_SPX26], [S_SPX26, S_TESLA], [S_TESLA]]
CYC_SRC = [S_FFSC, S_HOP]
# 30 Years of Raw Power: clips oldest -> newest. kind 'nasa' = NASA-hosted MP4 (public domain, linked from images-assets.nasa.gov,
# not re-hosted), 'yt' = official SpaceX YouTube player (youtube-nocookie, click to load), 'link' = SpaceX page only.
NASA_V = 'https://images-assets.nasa.gov/video/'
CLIPS = [
 dict(kind='nasa', id='ksc_022411_sts133_launch', date='2011-02-24', t=T('Space Shuttle Discovery, STS-133 (last launch)', 'Navette Discovery, STS-133 (dernier lancement)', 'Transbordador Discovery, STS-133 (último lanzamiento)', 'المكوك ديسكفري، STS-133 (آخر إطلاق)', 'Shuttle Discovery, STS-133 (ultimo lancio)', 'מעבורת דיסקברי, STS-133 (שיגור אחרון)'), cr='NASA'),
 dict(kind='yt', id='wbSwFU6tY1c', date='2018-02-06', t=T('Falcon Heavy test flight (27 Merlin engines)', 'Vol d’essai de Falcon Heavy (27 moteurs Merlin)', 'Vuelo de prueba de Falcon Heavy (27 motores Merlin)', 'رحلة فالكون هيفي التجريبية (27 محرك Merlin)', 'Volo di prova di Falcon Heavy (27 motori Merlin)', 'טיסת ניסוי של Falcon Heavy (27 מנועי Merlin)'), cr='SpaceX'),
 dict(kind='nasa', id='KSC-20201115-MH-AJW02-0001-SpaceX_Crew_1_Live_Launch_Coverage_ISO_Broll_String_720p-3263009', date='2020-11-15', t=T('Falcon 9, NASA’s SpaceX Crew-1 (9 Merlin engines)', 'Falcon 9, mission Crew-1 NASA-SpaceX (9 moteurs Merlin)', 'Falcon 9, Crew-1 de NASA y SpaceX (9 motores Merlin)', 'فالكون 9، مهمة Crew-1 لناسا وSpaceX (9 محركات Merlin)', 'Falcon 9, missione Crew-1 NASA-SpaceX (9 motori Merlin)', 'Falcon 9, משימת Crew-1 של NASA ו-SpaceX (9 מנועי Merlin)'), cr='NASA'),
 dict(kind='nasa', id='Artemis I Launches to the Moon (Official NASA Recap)', date='2022-11-16', t=T('SLS, Artemis I (4 RS-25 + 2 solid boosters)', 'SLS, Artemis I (4 RS-25 + 2 propulseurs à poudre)', 'SLS, Artemis I (4 RS-25 + 2 propulsores sólidos)', 'SLS، أرتميس 1 (4 محركات RS-25 + معززان صلبان)', 'SLS, Artemis I (4 RS-25 + 2 booster solidi)', 'SLS, ארטמיס 1 (4 RS-25 + 2 מאיצים מוצקים)'), cr='NASA'),
 dict(kind='yt', id='hI9HQfCAw64', date='2024-10-13', t=T('Starship Flight 5, first booster catch (33 Raptor 2)', 'Starship vol 5, première capture du booster (33 Raptor 2)', 'Starship vuelo 5, primera captura del propulsor (33 Raptor 2)', 'ستارشيب الرحلة 5، أول التقاط للمعزز (33 Raptor 2)', 'Starship volo 5, prima cattura del booster (33 Raptor 2)', 'Starship טיסה 5, תפיסת המאיץ הראשונה (33 Raptor 2)'), cr='SpaceX'),
 dict(kind='nasa', id='SSC_2026-01-22_RS-25_Engine_Test', date='2026-01-22', t=T('RS-25 engine No. 2063 hot fire, NASA Stennis', 'Essai à feu du RS-25 n° 2063, NASA Stennis', 'Encendido del RS-25 n.º 2063, NASA Stennis', 'اختبار إشعال محرك RS-25 رقم 2063، ناسا ستينيس', 'Accensione dell’RS-25 n. 2063, NASA Stennis', 'הפעלת מנוע RS-25 מס׳ 2063, NASA סטניס'), cr='NASA'),
 dict(kind='link', id='https://www.spacex.com/launches/starship-flight-12', date='2026-05-22', t=T('Starship Flight 12, first flight of Starship V3 and Raptor 3', 'Starship vol 12, premier vol de Starship V3 et de Raptor 3', 'Starship vuelo 12, primer vuelo de Starship V3 y Raptor 3', 'ستارشيب الرحلة 12، أول رحلة لـ Starship V3 وRaptor 3', 'Starship volo 12, primo volo di Starship V3 e Raptor 3', 'Starship טיסה 12, הטיסה הראשונה של Starship V3 ו-Raptor 3'), cr='SpaceX'),
]
# Benchmark rows: vehicle, date, engine, per-engine thrust, total liftoff thrust, chamber pressure, Isp, propellant, sources
BENCH = [
 ('Space Shuttle (STS-133)', '2011-02-24', 'RS-25 ×3', '≈491,000 lbf (104.5%, vac)', None, None, None, 'LH₂ / LOX', [S_RS25]),
 ('Falcon Heavy', '2018-02-06', 'Merlin ×27', '845 kN / 190,000 lbf', '> 5 million lbf', None, None, 'LOX / RP-1', [S_FH]),
 ('Falcon 9 (Crew-1)', '2020-11-15', 'Merlin ×9', '845 kN / 190,000 lbf', None, None, None, 'LOX / RP-1', [S_FH]),
 ('SLS (Artemis I)', '2022-11-16', 'RS-25 ×4 + 2 SRB', '≈512,000 lbf (109%, vac)', '8.8 million lbf', None, None, 'LH₂ / LOX + solid', [S_RS25, S_A1]),
 ('Starship V3 Super Heavy', '2026-05-22', 'Raptor 3 ×33', '250 tf / 551,000 lbf', '8,240 tf / 18.1 million lbf', '350 bar (test, 2023)', None, 'CH₄ / LOX (subcooled)', [S_SPX26, S_SPXPG, S_350]),
]
# Chart: (label, kN, year, planned?) computed from the cited figures above.
CHART = [('RS-25 · Shuttle (vac)', round(491000 * 4.4482216 / 1000), False), ('Merlin', 845, False), ('Raptor 1', round(185 * 9.80665), False),
         ('RS-25 · SLS (vac)', round(512000 * 4.4482216 / 1000), False), ('Raptor 2', round(230 * 9.80665), False), ('Raptor 3', round(250 * 9.80665), False), ('Raptor 4', round(300 * 9.80665), True)]
# Learn from the best: (group, name, url, why). Checked with curl Oct 28 2026; 403/429 = bot check on a live page (kept).
def W(*a): return T(*a)
BEST = [
 ('g_free', 'MIT OpenCourseWare 16.512 Rocket Propulsion', 'https://ocw.mit.edu/courses/16-512-rocket-propulsion-fall-2005/',
  W('MIT’s graduate rocket propulsion course, free: lecture notes and problem sets.', 'Le cours de propulsion des fusées de master du MIT, gratuit : notes et exercices.', 'El curso de posgrado de propulsión de cohetes del MIT, gratis: apuntes y problemas.', 'مقرر دفع الصواريخ للدراسات العليا في MIT مجانًا: ملاحظات ومسائل.', 'Il corso magistrale di propulsione a razzo del MIT, gratis: dispense ed esercizi.', 'קורס התואר המתקדם של MIT בהנעה רקטית, בחינם: הרצאות ותרגילים.')),
 ('g_free', 'MIT OpenCourseWare 16.50 Introduction to Propulsion Systems', 'https://ocw.mit.edu/courses/16-50-introduction-to-propulsion-systems-spring-2012/',
  W('MIT’s undergraduate course on both jet and rocket engines, free.', 'Le cours de licence du MIT sur réacteurs et moteurs-fusées, gratuit.', 'El curso de grado del MIT sobre motores a reacción y cohetes, gratis.', 'مقرر MIT الجامعي عن المحركات النفاثة والصاروخية مجانًا.', 'Il corso triennale del MIT su motori a getto e a razzo, gratis.', 'הקורס של MIT לתואר ראשון על מנועי סילון ורקטות, בחינם.')),
 ('g_free', 'edX: Aerospace engineering courses', 'https://www.edx.org/learn/aerospace-engineering',
  W('University aerospace courses online; many can be audited for free.', 'Cours universitaires d’aérospatial en ligne ; beaucoup sont gratuits en auditeur libre.', 'Cursos universitarios de aeroespacial en línea; muchos se pueden auditar gratis.', 'دورات جامعية في الطيران والفضاء عبر الإنترنت، وكثير منها متاح مجانًا للاستماع.', 'Corsi universitari di aerospaziale online; molti si seguono gratis come uditore.', 'קורסים אוניברסיטאיים בתעופה וחלל ברשת; רבים פתוחים לשמיעה בחינם.')),
 ('g_uni', 'MIT AeroAstro', 'https://aeroastro.mit.edu/',
  W('MIT’s Department of Aeronautics and Astronautics (Course 16), home of the courses above.', 'Le département d’aéronautique et d’astronautique du MIT (Course 16), qui donne les cours ci-dessus.', 'El Departamento de Aeronáutica y Astronáutica del MIT (Course 16), de donde vienen esos cursos.', 'قسم الملاحة الجوية والفضائية في MIT (Course 16)، مصدر المقررات أعلاه.', 'Il Dipartimento di Aeronautica e Astronautica del MIT (Course 16), da cui vengono i corsi sopra.', 'המחלקה לאווירונאוטיקה ואסטרונאוטיקה של MIT (Course 16), מקור הקורסים שלמעלה.')),
 ('g_uni', 'Purdue University, Maurice J. Zucrow Laboratories', 'https://engineering.purdue.edu/Zucrow',
  W('Purdue’s propulsion research labs, founded in 1948, which describe themselves as the largest academic propulsion lab in the world.', 'Les labos de propulsion de Purdue, fondés en 1948, qui se présentent comme le plus grand labo universitaire de propulsion au monde.', 'Los laboratorios de propulsión de Purdue, fundados en 1948, que se describen como el mayor laboratorio académico de propulsión del mundo.', 'مختبرات الدفع في جامعة بيرديو، تأسست عام 1948، وتصف نفسها بأنها أكبر مختبر أكاديمي للدفع في العالم.', 'I laboratori di propulsione di Purdue, fondati nel 1948, che si definiscono il più grande laboratorio accademico di propulsione al mondo.', 'מעבדות ההנעה של פרדו, שנוסדו ב-1948 ומתארות את עצמן כמעבדת ההנעה האקדמית הגדולה בעולם.')),
 ('g_uni', 'Caltech GALCIT (Graduate Aerospace Laboratories)', 'https://aerospace.caltech.edu/',
  W('Caltech’s aerospace labs, the group whose early rocket work led to NASA’s Jet Propulsion Laboratory.', 'Les labos aérospatiaux de Caltech, dont les premiers travaux sur les fusées ont mené au JPL de la NASA.', 'Los laboratorios aeroespaciales de Caltech, cuyos primeros trabajos con cohetes dieron origen al JPL de la NASA.', 'مختبرات الطيران والفضاء في كالتك، التي قادت أعمالها المبكرة على الصواريخ إلى مختبر الدفع النفاث التابع لناسا.', 'I laboratori aerospaziali di Caltech, i cui primi lavori sui razzi portarono al JPL della NASA.', 'מעבדות התעופה והחלל של קלטק, שעבודתן המוקדמת על רקטות הובילה להקמת JPL של NASA.')),
 ('g_uni', 'Georgia Tech, Daniel Guggenheim School of Aerospace Engineering', 'https://ae.gatech.edu/',
  W('Georgia Tech’s aerospace school, with propulsion and combustion research.', 'L’école d’aérospatial de Georgia Tech, avec recherche en propulsion et combustion.', 'La escuela aeroespacial de Georgia Tech, con investigación en propulsión y combustión.', 'كلية الطيران والفضاء في جورجيا تك، مع أبحاث في الدفع والاحتراق.', 'La scuola aerospaziale di Georgia Tech, con ricerca su propulsione e combustione.', 'בית הספר לתעופה וחלל של ג׳ורג׳יה טק, עם מחקר בהנעה ובבעירה.')),
 ('g_uni', 'Stanford Aeronautics & Astronautics', 'https://aa.stanford.edu/',
  W('Stanford’s aero/astro department, including space propulsion and combustion research.', 'Le département aéro/astro de Stanford, avec recherche en propulsion spatiale et combustion.', 'El departamento aero/astro de Stanford, con investigación en propulsión espacial y combustión.', 'قسم الطيران والفضاء في ستانفورد، بما فيه أبحاث الدفع الفضائي والاحتراق.', 'Il dipartimento aero/astro di Stanford, con ricerca su propulsione spaziale e combustione.', 'מחלקת האווירונאוטיקה והאסטרונאוטיקה של סטנפורד, כולל מחקר בהנעה בחלל ובבעירה.')),
 ('g_uni', 'University of Michigan Aerospace Engineering', 'https://aero.engin.umich.edu/',
  W('Michigan’s aerospace department, home of the Plasmadynamics and Electric Propulsion Laboratory.', 'Le département d’aérospatial du Michigan, qui abrite le Plasmadynamics and Electric Propulsion Laboratory.', 'El departamento aeroespacial de Michigan, sede del Plasmadynamics and Electric Propulsion Laboratory.', 'قسم الطيران والفضاء في ميشيغان، مقر مختبر Plasmadynamics and Electric Propulsion.', 'Il dipartimento aerospaziale del Michigan, sede del Plasmadynamics and Electric Propulsion Laboratory.', 'מחלקת התעופה והחלל של מישיגן, בית ה-Plasmadynamics and Electric Propulsion Laboratory.')),
 ('g_nasa', 'NASA Glenn: Beginner’s Guide to Rockets', 'https://www.grc.nasa.gov/www/k-12/rocket/bgmr.html',
  W('NASA’s own plain-language pages on rocket thrust, nozzles and flight, with interactive simulators.', 'Les pages simples de la NASA sur la poussée, les tuyères et le vol des fusées, avec simulateurs.', 'Las páginas sencillas de la NASA sobre empuje, toberas y vuelo de cohetes, con simuladores.', 'صفحات ناسا المبسطة عن دفع الصواريخ والفوهات والطيران، مع محاكيات تفاعلية.', 'Le pagine semplici della NASA su spinta, ugelli e volo dei razzi, con simulatori.', 'הדפים הפשוטים של NASA על דחף רקטות, נחירים וטיסה, עם סימולטורים.')),
 ('g_nasa', 'NASA Glenn Research Center', 'https://www.nasa.gov/glenn/',
  W('NASA’s center for propulsion research, including electric propulsion.', 'Le centre de la NASA pour la recherche en propulsion, dont la propulsion électrique.', 'El centro de la NASA para investigación en propulsión, incluida la eléctrica.', 'مركز ناسا لأبحاث الدفع، بما فيه الدفع الكهربائي.', 'Il centro NASA per la ricerca sulla propulsione, inclusa quella elettrica.', 'מרכז NASA למחקר הנעה, כולל הנעה חשמלית.')),
 ('g_nasa', 'NASA STEM learning resources', 'https://www.nasa.gov/learning-resources/',
  W('NASA’s free lessons and activities for students and teachers.', 'Leçons et activités gratuites de la NASA pour élèves et enseignants.', 'Lecciones y actividades gratis de la NASA para estudiantes y docentes.', 'دروس وأنشطة مجانية من ناسا للطلاب والمعلمين.', 'Lezioni e attività gratuite della NASA per studenti e insegnanti.', 'שיעורים ופעילויות חינמיים של NASA לתלמידים ולמורים.')),
 ('g_job', 'NASA Internships', 'https://www.nasa.gov/learning-resources/internship-programs/',
  W('Paid NASA internships for students.', 'Stages rémunérés à la NASA pour étudiants.', 'Prácticas pagadas en la NASA para estudiantes.', 'تدريب مدفوع في ناسا للطلاب.', 'Tirocini retribuiti alla NASA per studenti.', 'התמחויות בתשלום ב-NASA לסטודנטים.')),
 ('g_job', 'NASA Pathways', 'https://www.nasa.gov/careers/pathways/',
  W('NASA’s student program that can lead to a full-time NASA job.', 'Le programme étudiant de la NASA qui peut mener à un poste permanent.', 'El programa de la NASA para estudiantes que puede llevar a un empleo fijo.', 'برنامج ناسا للطلاب الذي قد يقود إلى وظيفة دائمة.', 'Il programma NASA per studenti che può portare a un posto fisso.', 'תוכנית הסטודנטים של NASA שיכולה להוביל למשרה קבועה.')),
 ('g_job', 'SpaceX Careers', 'https://www.spacex.com/careers/',
  W('Jobs and internships at the maker of Merlin and Raptor.', 'Emplois et stages chez le fabricant de Merlin et Raptor.', 'Empleos y prácticas en el fabricante de Merlin y Raptor.', 'وظائف وتدريب لدى صانع Merlin وRaptor.', 'Lavori e tirocini presso il costruttore di Merlin e Raptor.', 'משרות והתמחויות אצל יצרנית Merlin ו-Raptor.')),
 ('g_job', 'Blue Origin Careers', 'https://www.blueorigin.com/careers',
  W('Jobs at the maker of the BE-4 engine.', 'Emplois chez le fabricant du moteur BE-4.', 'Empleos en el fabricante del motor BE-4.', 'وظائف لدى صانع محرك BE-4.', 'Lavori presso il costruttore del motore BE-4.', 'משרות אצל יצרנית מנוע BE-4.')),
 ('g_job', 'L3Harris Careers (Aerojet Rocketdyne)', 'https://careers.l3harris.com/',
  W('Aerojet Rocketdyne, maker of RS-25 and RL10, is part of L3Harris.', 'Aerojet Rocketdyne, fabricant du RS-25 et du RL10, fait partie de L3Harris.', 'Aerojet Rocketdyne, fabricante del RS-25 y el RL10, es parte de L3Harris.', 'Aerojet Rocketdyne، صانعة RS-25 وRL10، جزء من L3Harris.', 'Aerojet Rocketdyne, costruttore di RS-25 e RL10, fa parte di L3Harris.', 'Aerojet Rocketdyne, יצרנית RS-25 ו-RL10, היא חלק מ-L3Harris.')),
]
JET_BEST_IDS = ['MIT OpenCourseWare 16.50 Introduction to Propulsion Systems', 'edX: Aerospace engineering courses', 'MIT AeroAstro', 'Purdue University, Maurice J. Zucrow Laboratories',
                'Georgia Tech, Daniel Guggenheim School of Aerospace Engineering', 'Stanford Aeronautics & Astronautics', 'University of Michigan Aerospace Engineering',
                'NASA Glenn Research Center', 'NASA Internships', 'NASA Pathways', 'L3Harris Careers (Aerojet Rocketdyne)']
