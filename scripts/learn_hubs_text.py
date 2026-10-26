"""Oct 26 2026 (founder): Learn topic hubs + Aeronautical Engineering 4-year roadmap text, 6 languages (en fr es ar it he).
Roadmap order modeled on typical aerospace engineering programs (reference: the published suggested plan of study at
https://catalog.erau.edu/daytona-beach/engineering/bachelors/aerospace-engineering/ ; no affiliation, never branded on the site)."""
L6 = ('en', 'fr', 'es', 'ar', 'it', 'he')
def T(*a): return dict(zip(L6, a))
VISION = T(
 'Free, university-level STEM and aerospace learning in six languages. Start from first principles and work all the way to designing what flies, with every lesson tied to real work that helps people and the planet.',
 'Un apprentissage gratuit des sciences et de l’aérospatiale, de niveau universitaire, en six langues. Partez des premiers principes et allez jusqu’à concevoir ce qui vole, avec des leçons toujours reliées à un travail réel qui aide les gens et la planète.',
 'Aprendizaje gratuito de ciencia, tecnología y aeroespacial, de nivel universitario, en seis idiomas. Empieza por los primeros principios y llega hasta diseñar lo que vuela, con cada lección ligada a un trabajo real que ayuda a las personas y al planeta.',
 'تعلّم مجاني للعلوم والهندسة والفضاء بمستوى جامعي، بست لغات. ابدأ من المبادئ الأولى وتقدّم حتى تصمّم ما يطير، مع ربط كل درس بعمل حقيقي يساعد الناس والكوكب.',
 'Studio gratuito di scienze e ingegneria aerospaziale, di livello universitario, in sei lingue. Parti dai principi primi e arriva fino a progettare ciò che vola, con ogni lezione legata a un lavoro reale che aiuta le persone e il pianeta.',
 'לימוד חינמי של מדעים, הנדסה ותעופה וחלל ברמה אוניברסיטאית, בשש שפות. מתחילים מעקרונות היסוד ומגיעים עד לתכנון של מה שטס, וכל שיעור קשור לעבודה אמיתית שעוזרת לאנשים ולכוכב הלכת.')
UI = {
 'learn': T('Learn', 'Apprendre', 'Aprender', 'تعلّم', 'Impara', 'למידה'),
 'topics': T('Choose a topic', 'Choisir un thème', 'Elige un tema', 'اختر موضوعًا', 'Scegli un argomento', 'בחרו נושא'),
 'ncourses': T('{n} courses', '{n} cours', '{n} cursos', '{n} دورات', '{n} corsi', '{n} קורסים'),
 'ncourse1': T('1 course', '1 cours', '1 curso', 'دورة واحدة', '1 corso', 'קורס אחד'),
 'more': T('More ways to learn', 'Autres façons d’apprendre', 'Más formas de aprender', 'طرق أخرى للتعلّم', 'Altri modi per imparare', 'עוד דרכים ללמוד'),
 'courses': T('Courses', 'Cours', 'Cursos', 'الدورات', 'Corsi', 'קורסים'),
 'guides': T('Guides and labs', 'Guides et labos', 'Guías y laboratorios', 'أدلة ومختبرات', 'Guide e laboratori', 'מדריכים ומעבדות'),
 'calc': T('Built-in calculator', 'Calculateur intégré', 'Calculadora integrada', 'الحاسبة المدمجة', 'Calcolatore integrato', 'מחשבון מובנה'),
 'subject': T('Subject', 'Matière', 'Materia', 'المادة', 'Materia', 'תחום'),
 'tool': T('Calculator', 'Calculateur', 'Calculadora', 'الحاسبة', 'Calcolatore', 'מחשבון'),
 'full': T('Open full page', 'Ouvrir la page complète', 'Abrir página completa', 'افتح الصفحة كاملة', 'Apri la pagina intera', 'פתיחת העמוד המלא'),
 'nocalc': T('A calculator for this topic is coming. Use the subject tabs to open a related one.', 'Un calculateur pour ce thème arrive. Utilisez les onglets pour en ouvrir un proche.', 'Pronto habrá una calculadora para este tema. Usa las pestañas para abrir una relacionada.', 'حاسبة هذا الموضوع قادمة. استخدم تبويبات المادة لفتح حاسبة قريبة.', 'Un calcolatore per questo argomento è in arrivo. Usa le schede per aprirne uno affine.', 'מחשבון לנושא הזה בדרך. אפשר לפתוח מחשבון קרוב דרך לשוניות התחום.'),
 'inroad': T('Its place in the roadmap', 'Sa place dans le parcours', 'Su lugar en la ruta', 'موقعها في خريطة الطريق', 'Il suo posto nel percorso', 'המקום במפת הדרכים'),
 'road': T('Four-year roadmap', 'Parcours sur quatre ans', 'Ruta de cuatro años', 'خريطة طريق لأربع سنوات', 'Percorso di quattro anni', 'מפת דרכים לארבע שנים'),
 'road_t': T('Modeled on typical aerospace engineering degree programs. Self-study only: no credit, no school involved. Tick a course when you finish it; your progress stays in this browser.',
             'Inspiré des cursus habituels d’ingénierie aérospatiale. Autoformation uniquement : aucun crédit, aucune école. Cochez un cours une fois terminé ; votre progression reste dans ce navigateur.',
             'Basado en los planes habituales de ingeniería aeroespacial. Solo autoestudio: sin créditos ni escuela. Marca un curso al terminarlo; tu progreso se guarda en este navegador.',
             'مستوحاة من برامج هندسة الطيران والفضاء المعتادة. للدراسة الذاتية فقط: بلا ساعات معتمدة ولا جامعة. علّم الدورة عند إنهائها؛ يبقى تقدّمك في هذا المتصفح.',
             'Modellato sui tipici corsi di laurea in ingegneria aerospaziale. Solo autoapprendimento: nessun credito, nessuna università. Spunta un corso quando lo finisci; i progressi restano in questo browser.',
             'בנוי לפי תוכניות לימודים טיפוסיות בהנדסת תעופה וחלל. ללימוד עצמי בלבד: בלי נקודות זכות ובלי מוסד. סמנו קורס כשסיימתם; ההתקדמות נשמרת בדפדפן הזה.'),
 'fall': T('Fall', 'Automne', 'Otoño', 'الخريف', 'Autunno', 'סתיו'),
 'spring': T('Spring', 'Printemps', 'Primavera', 'الربيع', 'Primavera', 'אביב'),
 'done': T('Done', 'Terminé', 'Hecho', 'أُنجز', 'Fatto', 'הושלם'),
 'after': T('After:', 'Après :', 'Después de:', 'بعد:', 'Dopo:', 'אחרי:'),
 'progress': T('Your progress', 'Votre progression', 'Tu progreso', 'تقدّمك', 'I tuoi progressi', 'ההתקדמות שלך'),
 'of': T('{a} of {b} courses done', '{a} cours terminés sur {b}', '{a} de {b} cursos hechos', 'أُنجزت {a} من {b} دورة', '{a} corsi su {b} completati', 'הושלמו {a} מתוך {b} קורסים'),
 'next': T('Up next', 'À suivre', 'Lo siguiente', 'التالي', 'Prossimi', 'הבא בתור'),
 'exams': T('Upcoming checks and exams', 'Contrôles et examens à venir', 'Próximas pruebas y exámenes', 'الاختبارات القادمة', 'Prossime verifiche ed esami', 'בדיקות ומבחנים קרובים'),
 'units': T('Unit checks 1–10', 'Contrôles des unités 1–10', 'Pruebas de las unidades 1–10', 'اختبارات الوحدات 1–10', 'Verifiche delle unità 1–10', 'בדיקות יחידות 1–10'),
 'exam': T('Midterm and final practice', 'Partiel et examen final (entraînement)', 'Parcial y final de práctica', 'تدريب منتصف الفصل والنهائي', 'Prove intermedia e finale', 'תרגול אמצע ומבחן סופי'),
 'alldone': T('All 30 courses done. Well flown!', 'Les 30 cours sont terminés. Bravo !', '¡Los 30 cursos hechos! ¡Buen vuelo!', 'أنجزت الدورات الثلاثين كلها. أحسنت!', 'Tutti i 30 corsi completati. Ottimo volo!', 'כל 30 הקורסים הושלמו. טיסה מצוינת!'),
 'reset': T('Reset progress', 'Réinitialiser', 'Reiniciar progreso', 'إعادة ضبط التقدّم', 'Azzera i progressi', 'איפוס ההתקדמות'),
 'year': T('Year {n}', 'Année {n}', 'Año {n}', 'السنة {n}', 'Anno {n}', 'שנה {n}'),
 'yeartabs': T('Years', 'Années', 'Años', 'السنوات', 'Anni', 'שנים'),
 'kids': T('Kids', 'Enfants', 'Niños', 'الأطفال', 'Bambini', 'ילדים'),
 'teach': T('Teachers', 'Enseignants', 'Docentes', 'المعلّمون', 'Insegnanti', 'מורים'),
 'allc': T('All courses by year', 'Tous les cours par année', 'Todos los cursos por año', 'كل الدورات حسب السنة', 'Tutti i corsi per anno', 'כל הקורסים לפי שנה'),
}
TOPICS = [  # (key, page, emoji, name, one line, guides, calc subject)
 ('aero', 'Learn_Aero.html', '✈️', T('Aeronautical Engineering', 'Génie aéronautique', 'Ingeniería aeronáutica', 'هندسة الطيران', 'Ingegneria aeronautica', 'הנדסת אווירונאוטיקה'),
  T('The core path: a four-year roadmap from first chemistry and calculus to designing an aircraft or CubeSat.', 'Le parcours central : quatre ans, de la chimie et du calcul jusqu’à la conception d’un avion ou d’un CubeSat.', 'La ruta central: cuatro años, de la química y el cálculo al diseño de un avión o un CubeSat.', 'المسار الأساسي: أربع سنوات من الكيمياء والتفاضل إلى تصميم طائرة أو قمر CubeSat.', 'Il percorso centrale: quattro anni, dalla chimica e dall’analisi fino a progettare un aereo o un CubeSat.', 'המסלול המרכזי: ארבע שנים, מכימיה וחשבון ועד תכנון מטוס או CubeSat.'),
  ['Aero_Guide.html', 'Aero_Math.html', 'Aero_Lab.html'], 'aero'),
 ('orbits', 'Learn_Orbits.html', '🛰️', T('Orbits & Orbital Elements', 'Orbites et éléments orbitaux', 'Órbitas y elementos orbitales', 'المدارات وعناصرها', 'Orbite ed elementi orbitali', 'מסלולים ויסודות מסלוליים'),
  T('How satellites move: Kepler, transfers, delta-v and spacecraft design.', 'Comment bougent les satellites : Kepler, transferts, delta-v et conception d’engins.', 'Cómo se mueven los satélites: Kepler, transferencias, delta-v y diseño de naves.', 'كيف تتحرك الأقمار: كبلر والمناورات ودلتا-v وتصميم المركبات.', 'Come si muovono i satelliti: Keplero, trasferimenti, delta-v e progetto di veicoli.', 'איך לוויינים נעים: קפלר, מעברים, delta-v ותכנון חלליות.'),
  ['Orbits_Guide.html', 'Orbit_Math.html', 'Orbit_Lab.html'], 'orbits'),
 ('physics', 'Learn_Physics.html', '⚛️', T('Physics', 'Physique', 'Física', 'الفيزياء', 'Fisica', 'פיזיקה'),
  T('Motion, forces, energy, fields and waves, from first principles.', 'Mouvement, forces, énergie, champs et ondes, depuis les premiers principes.', 'Movimiento, fuerzas, energía, campos y ondas desde los primeros principios.', 'الحركة والقوى والطاقة والمجالات والموجات من المبادئ الأولى.', 'Moto, forze, energia, campi e onde, dai principi primi.', 'תנועה, כוחות, אנרגיה, שדות וגלים, מעקרונות היסוד.'),
  ['Physics_Guide.html', 'Physics_Math.html', 'Physics_Lab.html', 'AP_IB_Physics.html'], 'physics'),
 ('math', 'Learn_Math.html', '∑', T('Mathematics', 'Mathématiques', 'Matemáticas', 'الرياضيات', 'Matematica', 'מתמטיקה'),
  T('Calculus, differential equations, linear algebra, numerical methods and statistics.', 'Analyse, équations différentielles, algèbre linéaire, méthodes numériques et statistiques.', 'Cálculo, ecuaciones diferenciales, álgebra lineal, métodos numéricos y estadística.', 'التفاضل والتكامل والمعادلات التفاضلية والجبر الخطي والطرق العددية والإحصاء.', 'Analisi, equazioni differenziali, algebra lineare, metodi numerici e statistica.', 'חשבון דיפרנציאלי, משוואות דיפרנציאליות, אלגברה לינארית, שיטות נומריות וסטטיסטיקה.'),
  [], 'physics'),
 ('eng', 'Learn_Engineering.html', '🛠️', T('Engineering Core', 'Tronc commun d’ingénierie', 'Núcleo de ingeniería', 'أساسيات الهندسة', 'Base di ingegneria', 'ליבת הנדסה'),
  T('CAD, programming, mechanics, circuits, thermodynamics, fluids and heat transfer.', 'CAO, programmation, mécanique, circuits, thermodynamique, fluides et transferts thermiques.', 'CAD, programación, mecánica, circuitos, termodinámica, fluidos y transferencia de calor.', 'التصميم بالحاسوب والبرمجة والميكانيكا والدوائر والديناميكا الحرارية والموائع وانتقال الحرارة.', 'CAD, programmazione, meccanica, circuiti, termodinamica, fluidi e scambio termico.', 'שרטוט ממוחשב, תכנות, מכניקה, מעגלים, תרמודינמיקה, זורמים ומעבר חום.'),
  [], 'aero'),
 ('chem', 'Learn_Chemistry.html', '🧪', T('Chemistry', 'Chimie', 'Química', 'الكيمياء', 'Chimica', 'כימיה'),
  T('Atoms, reactions, bonding, gases and energy, with labs.', 'Atomes, réactions, liaisons, gaz et énergie, avec TP.', 'Átomos, reacciones, enlaces, gases y energía, con laboratorios.', 'الذرات والتفاعلات والروابط والغازات والطاقة مع مختبرات.', 'Atomi, reazioni, legami, gas ed energia, con laboratori.', 'אטומים, תגובות, קשרים, גזים ואנרגיה, עם מעבדות.'),
  [], 'physics'),
]
# Roadmap: id -> (year, semester 'fall'|'spring', topic, prereqs, default calculator or None).
# Semester placement follows the reference plan's scope by year (see docstring); prerequisites are the usual ones for these subjects.
ROAD = [
 ('chem110', 1, 'fall', 'chem', [], None), ('calc1', 1, 'fall', 'math', [], None), ('aero101', 1, 'fall', 'aero', [], 'lift'), ('cad101', 1, 'fall', 'eng', [], None),
 ('calc2', 1, 'spring', 'math', ['calc1'], None), ('prog101', 1, 'spring', 'eng', [], None), ('phys110', 1, 'spring', 'physics', ['calc1'], 'projectile'),
 ('calc3', 2, 'fall', 'math', ['calc2'], None), ('statics', 2, 'fall', 'eng', ['phys110', 'calc2'], None), ('thermo', 2, 'fall', 'eng', ['phys110', 'calc2'], 'mach'), ('phys2', 2, 'fall', 'physics', ['phys110', 'calc2'], 'pendulum'),
 ('diffeq', 2, 'spring', 'math', ['calc2'], None), ('linalg', 2, 'spring', 'math', ['calc2'], None), ('mom', 2, 'spring', 'eng', ['statics'], None), ('dynamics', 2, 'spring', 'eng', ['statics'], 'projectile'),
 ('aero1', 3, 'fall', 'aero', ['dynamics', 'calc3', 'diffeq'], 'lift'), ('fluids', 3, 'fall', 'eng', ['dynamics', 'calc3'], 'mach'), ('orbit', 3, 'fall', 'orbits', ['dynamics', 'diffeq'], 'hohmann'), ('circuits', 3, 'fall', 'eng', ['phys2', 'diffeq'], None), ('numerics', 3, 'fall', 'math', ['prog101', 'linalg', 'diffeq'], None),
 ('perf', 3, 'spring', 'aero', ['aero1'], 'stall'), ('struct', 3, 'spring', 'aero', ['mom'], None), ('prop', 3, 'spring', 'aero', ['thermo', 'fluids'], 'tw'), ('fdc', 3, 'spring', 'aero', ['dynamics', 'diffeq', 'aero1'], 'stall'), ('probstat', 3, 'spring', 'math', ['calc2'], None),
 ('heat', 4, 'fall', 'eng', ['thermo', 'fluids'], None), ('scdesign', 4, 'fall', 'orbits', ['orbit'], 'dv'), ('avionics', 4, 'fall', 'aero', ['circuits'], None),
 ('capstone', 4, 'spring', 'aero', ['perf', 'struct', 'prop', 'fdc'], 'rotor'), ('sustain', 4, 'spring', 'aero', ['prop', 'perf'], 'lift'),
]
# Calculator subjects (tab order) -> [(id, page)]
CALCS = [
 ('aero', [('lift', 'Lift_Equation_Calculator.html'), ('stall', 'Stall_Speed_Calculator.html'), ('mach', 'Mach_Number_Calculator.html'), ('tw', 'Thrust_to_Weight_Calculator.html'), ('rotor', 'Rotor_Hover_Power_Calculator.html')]),
 ('orbits', [('period', 'Orbital_Period_Calculator.html'), ('vel', 'Orbital_Velocity_Calculator.html'), ('hohmann', 'Hohmann_Transfer_Calculator.html'), ('dv', 'Delta_V_Calculator.html')]),
 ('physics', [('projectile', 'Projectile_Motion_Drag_Calculator.html'), ('pendulum', 'Pendulum_Period_Calculator.html')]),
]
