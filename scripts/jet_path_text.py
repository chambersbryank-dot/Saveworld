"""Oct 28 2026 (founder): text for Learn_Jet_Propulsion.html, "Aerospace Studies with a focus on Jet Propulsion" (6 langs),
a separate track from Aeronautical Engineering (Learn_Aero.html). Concise: no school comparisons; one short credit line.
PNOTE / AERO_PINTRO are also used by the 'How this path helps the planet' block on Learn_Aero.html."""
L6 = ('en', 'fr', 'es', 'ar', 'it', 'he')
def T(*a): return dict(zip(L6, a))
PAGE = 'Learn_Jet_Propulsion.html'
NAME = T('Aerospace Studies with a focus on Jet Propulsion',
 'Études aérospatiales, spécialité propulsion par réaction',
 'Estudios aeroespaciales con enfoque en propulsión a reacción',
 'دراسات الطيران والفضاء مع التركيز على الدفع النفاث',
 'Studi aerospaziali con focus sulla propulsione a getto',
 'לימודי תעופה וחלל עם דגש על הנעה סילונית')
SHORT = T('Aerospace: Jet Propulsion', 'Aérospatial : propulsion', 'Aeroespacial: propulsión', 'الفضاء: الدفع النفاث', 'Aerospaziale: propulsione', 'תעופה וחלל: הנעה סילונית')
LINE = T('A free four-year aerospace engineering path, from first calculus to a two-semester jet propulsion capstone.',
 'Un parcours gratuit de quatre ans en génie aérospatial, du premier cours d’analyse à un projet final de propulsion sur deux semestres.',
 'Una ruta gratuita de cuatro años en ingeniería aeroespacial, del primer cálculo a un proyecto final de propulsión de dos semestres.',
 'مسار مجاني لأربع سنوات في هندسة الطيران والفضاء، من أول مقرر تفاضل إلى مشروع تخرج في الدفع النفاث على فصلين.',
 'Un percorso gratuito di quattro anni in ingegneria aerospaziale, dal primo corso di analisi a un progetto finale di propulsione in due semestri.',
 'מסלול חינמי של ארבע שנים בהנדסת תעופה וחלל, מהחשבון הראשון ועד פרויקט גמר בהנעה סילונית בשני סמסטרים.')
UI = {
 'to_aero': T('Prefer aircraft? See the Aeronautical Engineering track', 'Plutôt avions ? Voir le parcours génie aéronautique', '¿Prefieres aviones? Mira la ruta de ingeniería aeronáutica', 'تفضّل الطائرات؟ اطّلع على مسار هندسة الطيران', 'Preferisci gli aerei? Vedi il percorso di ingegneria aeronautica', 'מעדיפים מטוסים? ראו את מסלול הנדסת האווירונאוטיקה'),
 'to_jet': T('Also see: Aerospace Studies with a focus on Jet Propulsion', 'Voir aussi : Études aérospatiales, spécialité propulsion', 'Mira también: Estudios aeroespaciales con enfoque en propulsión', 'اطّلع أيضًا على: دراسات الطيران والفضاء مع التركيز على الدفع النفاث', 'Vedi anche: Studi aerospaziali con focus sulla propulsione', 'ראו גם: לימודי תעופה וחלל עם דגש על הנעה סילונית'),
 'plan_h': T('Four-year roadmap', 'Parcours sur quatre ans', 'Ruta de cuatro años', 'خريطة الطريق لأربع سنوات', 'Percorso in quattro anni', 'מפת דרכים לארבע שנים'),
 'plan_t': T('Study in order. Heat Transfer comes before Propulsion; the capstone runs two semesters.', 'Suivez l’ordre. Transferts thermiques avant Propulsion ; le projet final dure deux semestres.', 'Estudia en orden. Transferencia de calor va antes de Propulsión; el proyecto final dura dos semestres.', 'ادرس بالترتيب: انتقال الحرارة قبل الدفع، ومشروع التخرج يمتد فصلين.', 'Studia in ordine. Trasmissione del calore prima di Propulsione; il progetto finale dura due semestri.', 'לומדים לפי הסדר: מעבר חום לפני הנעה; פרויקט הגמר נמשך שני סמסטרים.'),
 'mod': T('Study module', 'Module d’étude', 'Módulo de estudio', 'وحدة دراسية', 'Modulo di studio', 'יחידת לימוד'),
 'part': T('Part {n} of 2', 'Partie {n} sur 2', 'Parte {n} de 2', 'الجزء {n} من 2', 'Parte {n} di 2', 'חלק {n} מתוך 2'),
 'labs_h': T('About the labs', 'À propos des labos', 'Sobre los laboratorios', 'عن المختبرات', 'Sui laboratori', 'על המעבדות'),
 'labs': T('Labs here are simulation-based (calculators and virtual experiments). They stand in for wind tunnels and engine test stands; they do not replace them.', 'Les labos sont des simulations (calculateurs et expériences virtuelles). Ils remplacent provisoirement souffleries et bancs d’essai moteur, sans les égaler.', 'Los laboratorios son simulaciones (calculadoras y experimentos virtuales). Sustituyen a túneles de viento y bancos de pruebas de motores, pero no los reemplazan.', 'المختبرات هنا قائمة على المحاكاة (حاسبات وتجارب افتراضية). هي بديل مؤقت لأنفاق الرياح ومنصات اختبار المحركات ولا تُغني عنها.', 'I laboratori sono simulazioni (calcolatori ed esperimenti virtuali). Fanno le veci di gallerie del vento e banchi prova motori, senza sostituirli.', 'המעבדות כאן מבוססות סימולציה (מחשבונים וניסויים וירטואליים). הן ממלאות את מקומן של מנהרות רוח ועמדות ניסוי למנועים, אך אינן מחליפות אותן.'),
 'credit': T('Sequence informed by published aerospace engineering curricula, including the MIT Course 16 catalog. Independent study guide: no affiliation, credit or endorsement.', 'Ordre inspiré de cursus publiés en génie aérospatial, dont le catalogue MIT Course 16. Guide d’étude indépendant : aucune affiliation, aucun crédit, aucun parrainage.', 'Orden basado en planes publicados de ingeniería aeroespacial, incluido el catálogo MIT Course 16. Guía de estudio independiente: sin afiliación, créditos ni respaldo.', 'الترتيب مستند إلى مناهج منشورة في هندسة الطيران والفضاء، منها كتالوج MIT Course 16. دليل دراسة مستقل: بلا انتماء أو ساعات معتمدة أو اعتماد.', 'Sequenza ispirata a piani di studio pubblicati di ingegneria aerospaziale, tra cui il catalogo MIT Course 16. Guida di studio indipendente: nessuna affiliazione, credito o approvazione.', 'הסדר מבוסס על תוכניות לימודים שפורסמו בהנדסת תעופה וחלל, כולל קטלוג MIT Course 16. מדריך לימוד עצמאי: ללא שיוך, נקודות זכות או אישור.'),
 'planet_h': T('How this path helps the planet', 'En quoi ce parcours aide la planète', 'Cómo ayuda esta ruta al planeta', 'كيف يساعد هذا المسار الكوكب', 'Come questo percorso aiuta il pianeta', 'איך המסלול הזה עוזר לכוכב הלכת'),
 'anim': T('Animation: a jet engine blowing exhaust', 'Animation : un moteur à réaction qui souffle ses gaz', 'Animación: un motor a reacción expulsando gases', 'رسم متحرك: محرك نفاث يطلق العادم', 'Animazione: un motore a getto che espelle i gas di scarico', 'הנפשה: מנוע סילון פולט גזי פליטה'),
}
# Study modules with no site course yet: id -> (name, one-line scope)
MOD = {
 'write': (T('Technical Writing & Communication', 'Rédaction technique et communication', 'Redacción técnica y comunicación', 'الكتابة التقنية والتواصل', 'Scrittura tecnica e comunicazione', 'כתיבה טכנית ותקשורת'),
           T('Lab reports, design reviews, presenting data.', 'Rapports de labo, revues de conception, présentation de données.', 'Informes de laboratorio, revisiones de diseño, presentar datos.', 'تقارير المختبر، مراجعات التصميم، عرض البيانات.', 'Relazioni di laboratorio, revisioni di progetto, presentazione dei dati.', 'דוחות מעבדה, סקירות תכנון, הצגת נתונים.')),
 'mats': (T('Aerospace Materials', 'Matériaux aérospatiaux', 'Materiales aeroespaciales', 'مواد الطيران والفضاء', 'Materiali aerospaziali', 'חומרים לתעופה וחלל'),
          T('Alloys, composites, high-temperature materials for engines.', 'Alliages, composites, matériaux haute température pour moteurs.', 'Aleaciones, compuestos, materiales de alta temperatura para motores.', 'السبائك والمواد المركبة ومواد الحرارة العالية للمحركات.', 'Leghe, compositi, materiali ad alta temperatura per motori.', 'סגסוגות, חומרים מרוכבים וחומרים לטמפרטורות גבוהות במנועים.')),
 'pde': (T('Engineering Math Methods (PDEs)', 'Méthodes mathématiques de l’ingénieur (EDP)', 'Métodos matemáticos de ingeniería (EDP)', 'الطرق الرياضية الهندسية (المعادلات التفاضلية الجزئية)', 'Metodi matematici per l’ingegneria (EDP)', 'שיטות מתמטיות בהנדסה (משוואות חלקיות)'),
         T('Partial differential equations, Fourier series, vector calculus.', 'Équations aux dérivées partielles, séries de Fourier, analyse vectorielle.', 'Ecuaciones en derivadas parciales, series de Fourier, cálculo vectorial.', 'المعادلات التفاضلية الجزئية، متسلسلات فورييه، التفاضل المتجهي.', 'Equazioni alle derivate parziali, serie di Fourier, calcolo vettoriale.', 'משוואות דיפרנציאליות חלקיות, טורי פורייה, חשבון וקטורי.')),
}
# year -> {sem: [course id | 'mod:<id>' | 'capstone:<part>']}
PLAN = {
 1: {'fall': ['calc1', 'chem110', 'aero101', 'cad101'], 'spring': ['calc2', 'phys110', 'prog101', 'mod:write']},
 2: {'fall': ['calc3', 'statics', 'thermo', 'phys2'], 'spring': ['diffeq', 'linalg', 'mom', 'dynamics']},
 3: {'fall': ['aero1', 'fluids', 'numerics', 'probstat', 'mod:mats'], 'spring': ['heat', 'perf', 'struct', 'circuits', 'mod:pde']},
 4: {'fall': ['prop', 'fdc', 'orbit', 'avionics', 'capstone:1'], 'spring': ['capstone:2', 'sustain', 'scdesign']},
}
# Planet notes per year: text with {Page.html|label} link markers. Shared by both paths.
PNOTE = {
 1: T('Chemistry and calculus are the language of combustion and of the air itself: the base for judging cleaner fuels later. See {Sustainable_Aviation.html|Sustainable Aviation}.',
      'La chimie et l’analyse sont la langue de la combustion et de l’air lui-même : la base pour juger plus tard des carburants plus propres. Voir {Sustainable_Aviation.html|Aviation durable}.',
      'La química y el cálculo son el idioma de la combustión y del propio aire: la base para evaluar después combustibles más limpios. Mira {Sustainable_Aviation.html|Aviación sostenible}.',
      'الكيمياء والتفاضل هما لغة الاحتراق والهواء نفسه: أساس للحكم لاحقًا على الوقود الأنظف. انظر {Sustainable_Aviation.html|الطيران المستدام}.',
      'Chimica e analisi sono la lingua della combustione e dell’aria stessa: la base per valutare in seguito carburanti più puliti. Vedi {Sustainable_Aviation.html|Aviazione sostenibile}.',
      'כימיה וחשבון הם השפה של בעירה ושל האוויר עצמו: הבסיס לשפוט בהמשך דלקים נקיים יותר. ראו {Sustainable_Aviation.html|תעופה בת-קיימא}.'),
 2: T('Thermodynamics and fluids decide how much fuel an engine burns for each unit of thrust, so this year is where efficiency, and lower emissions, begin.',
      'La thermodynamique et les fluides déterminent combien de carburant un moteur brûle pour chaque unité de poussée : c’est ici que commencent l’efficacité et la baisse des émissions.',
      'La termodinámica y los fluidos deciden cuánto combustible quema un motor por cada unidad de empuje: aquí empiezan la eficiencia y la reducción de emisiones.',
      'تحدّد الديناميكا الحرارية والموائع كمية الوقود التي يحرقها المحرك مقابل كل وحدة دفع، فهنا تبدأ الكفاءة وخفض الانبعاثات.',
      'Termodinamica e fluidi decidono quanto carburante brucia un motore per ogni unità di spinta: qui iniziano l’efficienza e la riduzione delle emissioni.',
      'תרמודינמיקה וזורמים קובעים כמה דלק מנוע שורף לכל יחידת דחף, ולכן כאן מתחילות היעילות והפחתת הפליטות.'),
 3: T('Propulsion and orbits are how Earth-observation satellites reach orbit to watch {Oceans.html|oceans}, {Deforestation.html|forests} and {Polar.html|ice}. See {Earth_Observation.html|Earth Observation} and {Upcoming_Launches.html|Upcoming Launches}.',
      'La propulsion et les orbites permettent aux satellites d’observation de la Terre d’atteindre l’orbite pour surveiller {Oceans.html|les océans}, {Deforestation.html|les forêts} et {Polar.html|les glaces}. Voir {Earth_Observation.html|Observation de la Terre} et {Upcoming_Launches.html|Prochains lancements}.',
      'La propulsión y las órbitas llevan a los satélites de observación de la Tierra a vigilar {Oceans.html|los océanos}, {Deforestation.html|los bosques} y {Polar.html|el hielo}. Mira {Earth_Observation.html|Observación de la Tierra} y {Upcoming_Launches.html|Próximos lanzamientos}.',
      'بالدفع والمدارات تصل أقمار رصد الأرض إلى مداراتها لتراقب {Oceans.html|المحيطات} و{Deforestation.html|الغابات} و{Polar.html|الجليد}. انظر {Earth_Observation.html|رصد الأرض} و{Upcoming_Launches.html|عمليات الإطلاق القادمة}.',
      'Propulsione e orbite portano i satelliti di osservazione della Terra a sorvegliare {Oceans.html|gli oceani}, {Deforestation.html|le foreste} e {Polar.html|i ghiacci}. Vedi {Earth_Observation.html|Osservazione della Terra} e {Upcoming_Launches.html|Prossimi lanci}.',
      'הנעה ומסלולים הם הדרך שבה לווייני תצפית על כדור הארץ מגיעים למסלול כדי לעקוב אחר {Oceans.html|האוקיינוסים}, {Deforestation.html|היערות} ו{Polar.html|הקרח}. ראו {Earth_Observation.html|תצפית על כדור הארץ} ו{Upcoming_Launches.html|שיגורים קרובים}.'),
 4: T('Senior work turns this into design: quieter, lower-emission engines and alternative fuels ({Sustainable_Aviation.html|Sustainable Aviation}), spacecraft for {Space.html|space solutions} and missions for {Planetary_Defense.html|planetary defense}.',
      'La dernière année transforme tout cela en conception : moteurs plus silencieux et moins émetteurs, carburants alternatifs ({Sustainable_Aviation.html|Aviation durable}), engins pour {Space.html|les solutions spatiales} et missions de {Planetary_Defense.html|défense planétaire}.',
      'El último año lo convierte en diseño: motores más silenciosos y con menos emisiones y combustibles alternativos ({Sustainable_Aviation.html|Aviación sostenible}), naves para {Space.html|soluciones espaciales} y misiones de {Planetary_Defense.html|defensa planetaria}.',
      'تحوّل السنة الأخيرة ذلك إلى تصميم: محركات أهدأ وأقل انبعاثًا ووقود بديل ({Sustainable_Aviation.html|الطيران المستدام})، ومركبات لـ{Space.html|حلول الفضاء}، ومهمات لـ{Planetary_Defense.html|الدفاع الكوكبي}.',
      'L’ultimo anno trasforma tutto in progetto: motori più silenziosi e meno inquinanti e carburanti alternativi ({Sustainable_Aviation.html|Aviazione sostenibile}), veicoli per {Space.html|le soluzioni spaziali} e missioni di {Planetary_Defense.html|difesa planetaria}.',
      'השנה האחרונה הופכת את כל זה לתכנון: מנועים שקטים יותר עם פחות פליטות ודלקים חלופיים ({Sustainable_Aviation.html|תעופה בת-קיימא}), חלליות ל{Space.html|פתרונות בחלל} ומשימות ל{Planetary_Defense.html|הגנה פלנטרית}.'),
}
PINTRO = T('Every Saving Planets solution helps both people and nature. Efficient engines cut fuel use and emissions; launch vehicles carry the satellites that watch oceans, forests and ice.',
 'Chaque solution de Saving Planets aide les humains et la nature. Des moteurs efficaces réduisent consommation et émissions ; les lanceurs placent les satellites qui surveillent océans, forêts et glaces.',
 'Cada solución de Saving Planets ayuda a las personas y a la naturaleza. Los motores eficientes reducen consumo y emisiones; los lanzadores llevan los satélites que vigilan océanos, bosques y hielo.',
 'كل حل على Saving Planets يساعد الناس والطبيعة معًا. المحركات الكفؤة تخفّض الوقود والانبعاثات، ومركبات الإطلاق تحمل الأقمار التي تراقب المحيطات والغابات والجليد.',
 'Ogni soluzione di Saving Planets aiuta persone e natura. Motori efficienti riducono consumi ed emissioni; i lanciatori portano i satelliti che sorvegliano oceani, foreste e ghiacci.',
 'כל פתרון ב-Saving Planets עוזר גם לבני האדם וגם לטבע. מנועים יעילים מפחיתים דלק ופליטות; משגרים נושאים את הלוויינים שעוקבים אחר אוקיינוסים, יערות וקרח.')
AERO_PINTRO = T('Every solution on Saving Planets has to help both people and nature, and this roadmap is built the same way. Here is how each year connects to that work.',
 'Chaque solution de Saving Planets doit aider à la fois les humains et la nature, et ce parcours est conçu de la même façon. Voici comment chaque année s’y rattache.',
 'Cada solución de Saving Planets debe ayudar a las personas y a la naturaleza, y esta ruta está pensada igual. Así se conecta cada año con ese trabajo.',
 'يجب أن يساعد كل حل على Saving Planets الناس والطبيعة معًا، وقد بُنيت خريطة الطريق هذه بالطريقة نفسها. إليك كيف ترتبط كل سنة بهذا العمل.',
 'Ogni soluzione su Saving Planets deve aiutare sia le persone sia la natura, e questo percorso è costruito allo stesso modo. Ecco come ogni anno si collega a quel lavoro.',
 'כל פתרון ב-Saving Planets חייב לעזור גם לבני האדם וגם לטבע, והמסלול הזה בנוי באותה דרך. כך כל שנה מתחברת לעבודה הזו.')
