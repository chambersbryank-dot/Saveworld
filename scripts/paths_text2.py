"""Oct 16 2026: Cadets (JROTC + CAP) and AP/IB page text. See paths_text.py for markup rules."""
from paths_text import T, S, R
KYDOE = 'https://www.education.ky.gov/CTE/ctepa/Documents/25-26_JROTC_Courses.pdf'
CAP_AD = 'https://www.gocivilairpatrol.com/programs/cadets/library/cadet-audio'
CAP_ACE = 'https://www.gocivilairpatrol.com/programs/aerospace-education/programs/ace'
CAP_AEX = 'https://www.gocivilairpatrol.com/programs/aerospace-education/programs/aerospace-education-excellence-aex'
CD = dict(
 title=T('Start Here: JROTC and Civil Air Patrol Aerospace Topics', 'Commencer ici : thèmes aérospatiaux du JROTC et de la Civil Air Patrol', 'Empieza aquí: temas aeroespaciales de JROTC y Civil Air Patrol', 'ابدأ هنا: موضوعات الطيران والفضاء في JROTC ودورية الطيران المدني', 'Inizia qui: temi aerospaziali di JROTC e Civil Air Patrol'),
 desc=T('Free pages, labs and calculators matched to the aerospace topics in public JROTC course descriptions and Civil Air Patrol aerospace education, with an instructor guide and printable topic map.',
        'Pages, labos et calculateurs gratuits associés aux thèmes aérospatiaux des descriptions publiques des cours JROTC et de l’éducation aérospatiale de la CAP, avec guide de l’instructeur et carte imprimable.',
        'Páginas, laboratorios y calculadoras gratuitas emparejadas con los temas aeroespaciales de las descripciones públicas de JROTC y la educación aeroespacial de CAP, con guía para instructores y mapa imprimible.',
        'صفحات ومختبرات وحاسبات مجانية مطابقة لموضوعات الطيران والفضاء في الأوصاف العامة لدورات JROTC وتعليم الطيران في CAP، مع دليل للمدرب وخريطة قابلة للطباعة.',
        'Pagine, laboratori e calcolatori gratuiti abbinati ai temi aerospaziali delle descrizioni pubbliche dei corsi JROTC e dell’educazione aerospaziale CAP, con guida per istruttori e mappa stampabile.'),
 kicker=T('For cadets, instructors and families. Free, no sign-up, works on a school iPad.', 'Pour cadets, instructeurs et familles. Gratuit, sans inscription, fonctionne sur un iPad scolaire.',
          'Para cadetes, instructores y familias. Gratis, sin registro, funciona en un iPad escolar.', 'للطلاب العسكريين والمدربين والعائلات. مجاني، بلا تسجيل، ويعمل على آيباد المدرسة.', 'Per cadetti, istruttori e famiglie. Gratis, senza registrazione, funziona sull’iPad della scuola.'),
 disc=T('Not affiliated with or endorsed by the U.S. Air Force, Army, Navy or Marine Corps, any JROTC program, or Civil Air Patrol. Program names are used only to describe which topics our free pages cover. We matched a topic only where an official public description lists it; check your own curriculum.',
        'Non affilié à l’U.S. Air Force, l’Army, la Navy, le Marine Corps, un programme JROTC ou la Civil Air Patrol, ni approuvé par eux. Les noms servent seulement à indiquer les thèmes couverts par nos pages gratuites. Nous n’avons associé un thème que s’il figure dans une description officielle publique ; vérifiez votre programme.',
        'No afiliado ni respaldado por la U.S. Air Force, Army, Navy o Marine Corps, ningún programa JROTC ni Civil Air Patrol. Los nombres solo indican qué temas cubren nuestras páginas gratuitas. Solo emparejamos un tema si aparece en una descripción oficial pública; revisa tu propio currículo.',
        'غير تابع للقوات الجوية أو البرية أو البحرية أو مشاة البحرية الأمريكية أو أي برنامج JROTC أو دورية الطيران المدني، ولا يحظى بتأييدها. تُذكر الأسماء فقط لبيان الموضوعات التي تغطيها صفحاتنا المجانية. طابقنا الموضوع فقط حيث يذكره وصف رسمي عام؛ راجع منهجك.',
        'Non affiliato né approvato da U.S. Air Force, Army, Navy o Marine Corps, da alcun programma JROTC o dalla Civil Air Patrol. I nomi servono solo a indicare i temi coperti dalle nostre pagine gratuite. Abbiamo abbinato un tema solo se compare in una descrizione ufficiale pubblica; verifica il tuo programma.'),
 af=S('Air Force JROTC: Aerospace Science'),
 af_t=T('Topics are taken from the Kentucky Department of Education’s public “2025–2026 JROTC Courses” descriptions (Air Force JROTC courses 580135 and 580137).',
        'Les thèmes viennent des descriptions publiques « 2025–2026 JROTC Courses » du Kentucky Department of Education (cours Air Force JROTC 580135 et 580137).',
        'Los temas vienen de las descripciones públicas «2025–2026 JROTC Courses» del Kentucky Department of Education (cursos Air Force JROTC 580135 y 580137).',
        'الموضوعات مأخوذة من الأوصاف العامة «2025–2026 JROTC Courses» لوزارة التعليم في كنتاكي (دورتا JROTC للقوات الجوية 580135 و580137).',
        'I temi provengono dalle descrizioni pubbliche «2025–2026 JROTC Courses» del Kentucky Department of Education (corsi Air Force JROTC 580135 e 580137).'),
 nv=S('Navy JROTC'),
 nv_t=T('The same public source lists oceanography, meteorology, astronomy and physical sciences (Navy JROTC 2, 580311) and nautical astronomy / celestial navigation (Navy JROTC 3, 580312).',
        'La même source publique cite océanographie, météorologie, astronomie et sciences physiques (Navy JROTC 2, 580311) et astronomie nautique / navigation astronomique (Navy JROTC 3, 580312).',
        'La misma fuente pública cita oceanografía, meteorología, astronomía y ciencias físicas (Navy JROTC 2, 580311) y astronomía náutica / navegación astronómica (Navy JROTC 3, 580312).',
        'يذكر المصدر العام نفسه علم المحيطات والأرصاد والفلك والعلوم الفيزيائية (Navy JROTC 2، رقم 580311) والفلك الملاحي (Navy JROTC 3، رقم 580312).',
        'La stessa fonte pubblica cita oceanografia, meteorologia, astronomia e scienze fisiche (Navy JROTC 2, 580311) e astronomia nautica / navigazione astronomica (Navy JROTC 3, 580312).'),
 am=T('Army and Marine Corps JROTC', 'Army et Marine Corps JROTC', 'Army y Marine Corps JROTC', 'JROTC للجيش ومشاة البحرية', 'Army e Marine Corps JROTC'),
 am_t=T('The public course descriptions we checked focus on leadership and citizenship and list no specific physics or aerospace topics (only a “STEM Camp”), so we do not map them. Our calculators and labs work well for any STEM activity day.',
        'Les descriptions publiques consultées portent sur le leadership et la citoyenneté et ne citent aucun thème précis de physique ou d’aérospatiale (seulement un « STEM Camp ») : nous ne les associons donc pas. Nos calculateurs et labos conviennent à toute journée STEM.',
        'Las descripciones públicas revisadas se centran en liderazgo y ciudadanía y no citan temas concretos de física o aeroespacio (solo un «STEM Camp»), así que no las emparejamos. Nuestras calculadoras y laboratorios sirven para cualquier jornada STEM.',
        'تركّز الأوصاف العامة التي راجعناها على القيادة والمواطنة ولا تذكر موضوعات فيزياء أو طيران محددة (سوى «STEM Camp»)، لذا لا نطابقها. وتصلح حاسباتنا ومختبراتنا لأي يوم أنشطة علمية.',
        'Le descrizioni pubbliche consultate riguardano leadership e cittadinanza e non citano temi specifici di fisica o aerospazio (solo uno «STEM Camp»), quindi non le abbiniamo. Calcolatori e laboratori vanno bene per qualsiasi giornata STEM.'),
 cap=T('Civil Air Patrol aerospace education', 'Éducation aérospatiale de la Civil Air Patrol', 'Educación aeroespacial de Civil Air Patrol', 'تعليم الطيران والفضاء في دورية الطيران المدني', 'Educazione aerospaziale della Civil Air Patrol'),
 cap_t=T('Cadet Aerospace Dimensions modules as listed on CAP’s official cadet library page.', 'Modules Aerospace Dimensions des cadets, tels que listés sur la page officielle de la bibliothèque des cadets de la CAP.',
         'Módulos Aerospace Dimensions de cadetes, según la página oficial de la biblioteca de cadetes de CAP.', 'وحدات Aerospace Dimensions للطلاب كما تذكرها صفحة مكتبة الطلاب الرسمية في CAP.', 'Moduli Aerospace Dimensions per cadetti, come elencati nella pagina ufficiale della biblioteca cadetti CAP.'),
 ace=T('**ACE (grades K–6)**: CAP’s Aerospace Connections in Education program for elementary classrooms. Younger learners can use our no-sign-up kids pages alongside it: [Kids Map](Kids_Map.html), [Amazing Facts](Amazing_Facts.html), [Play and Learn](Play_and_Learn.html).',
       '**ACE (de la maternelle au CM2)** : le programme Aerospace Connections in Education de la CAP pour l’école primaire. Les plus jeunes peuvent utiliser en parallèle nos pages enfants sans inscription : [Carte des enfants](Kids_Map.html), [Faits étonnants](Amazing_Facts.html), [Jouer et apprendre](Play_and_Learn.html).',
       '**ACE (grados K–6)**: el programa Aerospace Connections in Education de CAP para primaria. Los más pequeños pueden usar a la vez nuestras páginas infantiles sin registro: [Mapa infantil](Kids_Map.html), [Datos asombrosos](Amazing_Facts.html), [Jugar y aprender](Play_and_Learn.html).',
       '**ACE (من الروضة حتى الصف السادس)**: برنامج Aerospace Connections in Education من CAP للمرحلة الابتدائية. يمكن للصغار استخدام صفحات الأطفال لدينا بلا تسجيل إلى جانبه: [خريطة الأطفال](Kids_Map.html)، [حقائق مدهشة](Amazing_Facts.html)، [العب وتعلّم](Play_and_Learn.html).',
       '**ACE (classi K–6)**: il programma Aerospace Connections in Education della CAP per la primaria. I più piccoli possono usare in parallelo le nostre pagine per bambini senza registrazione: [Mappa per bambini](Kids_Map.html), [Fatti sorprendenti](Amazing_Facts.html), [Gioca e impara](Play_and_Learn.html).'),
 aex=T('**AEX (grades 7–12)**: CAP’s Aerospace Education Excellence award asks participants to complete six aerospace activities plus a two-hour aerospace experience, and CAP says lessons may come from another aerospace education source. Check CAP’s current AEX requirements before counting one of our labs.',
       '**AEX (de la 5e à la terminale)** : le prix Aerospace Education Excellence de la CAP demande six activités aérospatiales et une expérience aérospatiale de deux heures, et la CAP indique que les leçons peuvent provenir d’une autre source d’éducation aérospatiale. Vérifiez les exigences AEX actuelles avant de compter un de nos labos.',
       '**AEX (grados 7–12)**: el premio Aerospace Education Excellence de CAP pide seis actividades aeroespaciales y una experiencia aeroespacial de dos horas, y CAP indica que las lecciones pueden venir de otra fuente de educación aeroespacial. Revisa los requisitos AEX vigentes antes de contar uno de nuestros laboratorios.',
       '**AEX (الصفوف 7–12)**: تطلب جائزة Aerospace Education Excellence من CAP إكمال ستة أنشطة في الطيران والفضاء وتجربة مدتها ساعتان، وتذكر CAP أن الدروس قد تأتي من مصدر آخر لتعليم الطيران والفضاء. راجع متطلبات AEX الحالية قبل احتساب أحد مختبراتنا.',
       '**AEX (classi 7–12)**: il premio Aerospace Education Excellence della CAP chiede sei attività aerospaziali e un’esperienza aerospaziale di due ore, e la CAP indica che le lezioni possono provenire da un’altra fonte di educazione aerospaziale. Verifica i requisiti AEX attuali prima di contare uno dei nostri laboratori.'),
 inst=T('For instructors', 'Pour les instructeurs', 'Para instructores', 'للمدربين', 'Per gli istruttori'),
 inst_steps=[
  T('Pick a row from the topic map below and open the guide first (10–15 minutes of reading, with pictures).', 'Choisissez une ligne de la carte ci-dessous et ouvrez d’abord le guide (10–15 minutes de lecture illustrée).', 'Elige una fila del mapa y abre primero la guía (10–15 minutos de lectura con imágenes).', 'اختر صفًا من خريطة الموضوعات أدناه وافتح الدليل أولًا (قراءة مصورة مدتها 10–15 دقيقة).', 'Scegli una riga della mappa e apri prima la guida (10–15 minuti di lettura illustrata).'),
  T('Run the lab or a calculator on the projector; let cadets predict, then change one input at a time.', 'Lancez le labo ou un calculateur au projecteur ; faites prédire, puis changez une valeur à la fois.', 'Proyecta el laboratorio o una calculadora; que los cadetes predigan y luego cambien un dato cada vez.', 'شغّل المختبر أو الحاسبة على جهاز العرض؛ دع الطلاب يتوقعون ثم غيّر مدخلًا واحدًا في كل مرة.', 'Proietta il laboratorio o un calcolatore; fai prevedere ai cadetti, poi cambia un dato alla volta.'),
  T('Older cadets work the worked example and practice problems on the math page (answers check themselves).', 'Les plus avancés font l’exemple résolu et les exercices de la page de maths (auto-corrigés).', 'Los cadetes mayores resuelven el ejemplo y los ejercicios de la página de matemáticas (se corrigen solos).', 'يحل الطلاب الأكبر المثال والتمارين في صفحة الرياضيات (تُصحَّح تلقائيًا).', 'I cadetti più grandi svolgono l’esempio e gli esercizi della pagina di matematica (autocorretti).'),
  T('Share any page with the Google Classroom or Copy link buttons. Nothing to install and no student accounts.', 'Partagez une page avec les boutons Google Classroom ou Copier le lien. Rien à installer, aucun compte élève.', 'Comparte cualquier página con los botones de Google Classroom o Copiar enlace. Nada que instalar ni cuentas de alumnos.', 'شارك أي صفحة بزرَّي Google Classroom أو نسخ الرابط. لا شيء للتثبيت ولا حسابات للطلاب.', 'Condividi qualsiasi pagina con i pulsanti Google Classroom o Copia link. Niente da installare, nessun account studente.'),
 ],
 map=T('Printable topic map', 'Carte des thèmes imprimable', 'Mapa de temas imprimible', 'خريطة موضوعات قابلة للطباعة', 'Mappa dei temi stampabile'),
)
AF_ROWS = [
 R(S('AFJROTC 580135'), T('Principles of flight, four forces, airfoil lift', 'Principes du vol, quatre forces, portance du profil', 'Principios del vuelo, cuatro fuerzas, sustentación del perfil', 'مبادئ الطيران، القوى الأربع، رفع الجنيح', 'Principi del volo, quattro forze, portanza del profilo'),
   ['Aero_Guide.html', 'Aero_Math.html#airfoil', 'Lift_Equation_Calculator.html', 'Stall_Speed_Calculator.html', 'Aero_Lab.html']),
 R(S('AFJROTC 580135'), T('Propulsion physics; supersonic and hypersonic flight; the atmosphere', 'Physique de la propulsion ; vol supersonique et hypersonique ; l’atmosphère', 'Física de la propulsión; vuelo supersónico e hipersónico; la atmósfera', 'فيزياء الدفع؛ الطيران فوق الصوتي والفرط صوتي؛ الغلاف الجوي', 'Fisica della propulsione; volo supersonico e ipersonico; l’atmosfera'),
   ['Thrust_to_Weight_Calculator.html', 'Mach_Number_Calculator.html', 'Aero_Math.html#compress']),
 R(S('AFJROTC 580137'), T('Kepler’s and Newton’s laws; orbits and orbit types', 'Lois de Kepler et de Newton ; orbites et types d’orbites', 'Leyes de Kepler y Newton; órbitas y tipos', 'قوانين كبلر ونيوتن؛ المدارات وأنواعها', 'Leggi di Keplero e Newton; orbite e tipi di orbita'),
   ['Orbits_Guide.html', 'Orbit_Math.html#circular', 'Orbital_Period_Calculator.html', 'Orbital_Velocity_Calculator.html']),
 R(S('AFJROTC 580137'), T('Trajectories and maneuvering; how rockets work and launch', 'Trajectoires et manœuvres ; fonctionnement et lancement des fusées', 'Trayectorias y maniobras; cómo funcionan y despegan los cohetes', 'المسارات والمناورات؛ كيف تعمل الصواريخ وتنطلق', 'Traiettorie e manovre; come funzionano e partono i razzi'),
   ['Orbit_Math.html#hohmann', 'Hohmann_Transfer_Calculator.html', 'Delta_V_Calculator.html', 'Orbit_Lab.html']),
]
NV_ROWS = [
 R(S('NJROTC 580311 / 580312'), T('Astronomy; physical sciences; celestial navigation', 'Astronomie ; sciences physiques ; navigation astronomique', 'Astronomía; ciencias físicas; navegación astronómica', 'الفلك؛ العلوم الفيزيائية؛ الملاحة الفلكية', 'Astronomia; scienze fisiche; navigazione astronomica'),
   ['Orbits_Guide.html', 'Physics_Guide.html', 'Pendulum_Period_Calculator.html', 'Satellite_Explorer.html']),
 R(S('NJROTC 580311'), T('Oceanography and meteorology', 'Océanographie et météorologie', 'Oceanografía y meteorología', 'علم المحيطات والأرصاد', 'Oceanografia e meteorologia'), ['Satellite_Explorer.html', 'Mach_Number_Calculator.html']),
]
CAP_ROWS = [
 R(S('Aerospace Dimensions 1'), T('Introduction to Flight', 'Introduction au vol', 'Introducción al vuelo', 'مقدمة في الطيران', 'Introduzione al volo'), ['Aero_Guide.html', 'Lift_Equation_Calculator.html', 'Stall_Speed_Calculator.html']),
 R(S('Aerospace Dimensions 2'), T('Aircraft Systems and Airports', 'Systèmes de l’avion et aéroports', 'Sistemas de la aeronave y aeropuertos', 'أنظمة الطائرة والمطارات', 'Sistemi dell’aereo e aeroporti'), ['Aero_Guide.html', 'Thrust_to_Weight_Calculator.html']),
 R(S('Aerospace Dimensions 3'), T('Air Environment', 'L’environnement aérien', 'El entorno aéreo', 'البيئة الجوية', 'L’ambiente aereo'), ['Mach_Number_Calculator.html', 'Aero_Math.html#compress']),
 R(S('Aerospace Dimensions 4'), T('Rockets', 'Fusées', 'Cohetes', 'الصواريخ', 'Razzi'), ['Orbit_Math.html#rocket', 'Delta_V_Calculator.html', 'Projectile_Motion_Drag_Calculator.html']),
 R(S('Aerospace Dimensions 5'), T('Space Environment', 'L’environnement spatial', 'El entorno espacial', 'البيئة الفضائية', 'L’ambiente spaziale'), ['Orbits_Guide.html', 'Orbital_Velocity_Calculator.html']),
 R(S('Aerospace Dimensions 6'), T('Spacecraft', 'Engins spatiaux', 'Naves espaciales', 'المركبات الفضائية', 'Veicoli spaziali'), ['Orbit_Lab.html', 'Hohmann_Transfer_Calculator.html', 'Orbital_Period_Calculator.html']),
]
CD_SRC = [f'Kentucky Department of Education, <a href="{KYDOE}">2025–2026 JROTC Courses</a> (PDF).', f'Civil Air Patrol, <a href="{CAP_AD}">Cadet library: Aerospace Dimensions</a>.',
          f'Civil Air Patrol, <a href="{CAP_ACE}">ACE program</a>.', f'Civil Air Patrol, <a href="{CAP_AEX}">Aerospace Education Excellence (AEX)</a>.']
CAP_AP1 = 'https://apcentral.collegeboard.org/media/pdf/ap-physics-1-course-and-exam-description.pdf'
CAP_AP2 = 'https://apcentral.collegeboard.org/media/pdf/ap-physics-2-course-at-a-glance.pdf'
IBO = 'https://ibo.org/globalassets/new-structure/recognition/pdfs/dp_sciences_physics_subject-brief_jan_2022_e.pdf'
AP = dict(
 title=T('Start Here: AP Physics and IB Physics Topic Map', 'Commencer ici : correspondance des thèmes de physique AP et IB', 'Empieza aquí: mapa de temas de Física AP e IB', 'ابدأ هنا: خريطة موضوعات فيزياء AP وIB', 'Inizia qui: mappa dei temi di fisica AP e IB'),
 desc=T('Free physics, orbit and aeronautics math pages, labs and calculators matched to AP Physics 1, 2 and C: Mechanics units and IB Physics topics, with sources.',
        'Pages de maths, labos et calculateurs gratuits en physique, orbites et aéronautique, associés aux unités AP Physics 1, 2 et C: Mechanics et aux thèmes de l’IB Physics, avec sources.',
        'Páginas de matemáticas, laboratorios y calculadoras gratuitas de física, órbitas y aeronáutica emparejadas con las unidades de AP Physics 1, 2 y C: Mechanics y los temas de IB Physics, con fuentes.',
        'صفحات رياضيات ومختبرات وحاسبات مجانية في الفيزياء والمدارات والطيران مطابقة لوحدات AP Physics 1 و2 وC: Mechanics وموضوعات فيزياء IB، مع المصادر.',
        'Pagine di matematica, laboratori e calcolatori gratuiti di fisica, orbite e aeronautica abbinati alle unità di AP Physics 1, 2 e C: Mechanics e ai temi di IB Physics, con fonti.'),
 kicker=T('Extra practice with real aerospace examples. Use it alongside your course, not instead of it.', 'Entraînement supplémentaire avec de vrais exemples aérospatiaux. À utiliser avec votre cours, pas à sa place.',
          'Práctica extra con ejemplos aeroespaciales reales. Úsalo junto a tu curso, no en su lugar.', 'تدريب إضافي بأمثلة حقيقية من الطيران والفضاء. استخدمه مع مقررك لا بدلًا منه.', 'Pratica extra con veri esempi aerospaziali. Da usare insieme al corso, non al suo posto.'),
 tm=T('AP is a registered trademark of the College Board, which is not affiliated with this site. IB and International Baccalaureate are trademarks of the International Baccalaureate Organization, which is not affiliated with and does not endorse this site. We list a unit or topic only where it appears in the official public course description.',
      'AP est une marque déposée du College Board, qui n’est pas affilié à ce site. IB et International Baccalaureate sont des marques de l’International Baccalaureate Organization, qui n’est pas affiliée à ce site et ne l’approuve pas. Nous ne citons une unité ou un thème que s’il figure dans la description officielle publique.',
      'AP es una marca registrada del College Board, que no está afiliado a este sitio. IB e International Baccalaureate son marcas de la International Baccalaureate Organization, que no está afiliada a este sitio ni lo respalda. Solo citamos una unidad o tema si aparece en la descripción oficial pública.',
      'AP علامة تجارية مسجلة لـ College Board، وهي غير تابعة لهذا الموقع. وIB وInternational Baccalaureate علامتان لمنظمة البكالوريا الدولية، وهي غير تابعة لهذا الموقع ولا تؤيده. نذكر الوحدة أو الموضوع فقط إذا ورد في الوصف الرسمي العام للمقرر.',
      'AP è un marchio registrato del College Board, che non è affiliato a questo sito. IB e International Baccalaureate sono marchi dell’International Baccalaureate Organization, che non è affiliata a questo sito né lo approva. Citiamo un’unità o un tema solo se compare nella descrizione ufficiale pubblica.'),
 ap1=S('AP Physics 1'), apc=S('AP Physics C: Mechanics'), ap2=S('AP Physics 2'),
 ib=T('IB Physics (first assessment 2025)', 'IB Physique (première évaluation 2025)', 'IB Física (primera evaluación 2025)', 'فيزياء IB (أول تقييم 2025)', 'IB Fisica (prima valutazione 2025)'),
 apc_t=T('AP Physics C: Mechanics uses the same seven unit titles as AP Physics 1 units 1–7, with calculus, so the same pages apply (try the RK4 drag model in the projectile calculator).',
         'AP Physics C: Mechanics reprend les sept titres des unités 1–7 d’AP Physics 1, avec du calcul : les mêmes pages s’appliquent (essayez le modèle RK4 avec traînée du calculateur de projectile).',
         'AP Physics C: Mechanics usa los mismos siete títulos que las unidades 1–7 de AP Physics 1, con cálculo, así que sirven las mismas páginas (prueba el modelo RK4 con arrastre de la calculadora de proyectiles).',
         'تستخدم AP Physics C: Mechanics عناوين الوحدات السبع نفسها في AP Physics 1 (الوحدات 1–7) مع التفاضل والتكامل، فتنطبق الصفحات نفسها (جرّب نموذج RK4 مع السحب في حاسبة المقذوفات).',
         'AP Physics C: Mechanics usa gli stessi sette titoli delle unità 1–7 di AP Physics 1, con l’analisi, quindi valgono le stesse pagine (prova il modello RK4 con resistenza nel calcolatore del proiettile).'),
 how=T('How to use it', 'Mode d’emploi', 'Cómo usarlo', 'طريقة الاستخدام', 'Come usarlo'),
 how_t=T('Find your unit, read the matching section, then do the self-checking practice problems. Calculators let you test your algebra against a computed answer.',
         'Trouvez votre unité, lisez la section correspondante, puis faites les exercices auto-corrigés. Les calculateurs permettent de vérifier votre algèbre.',
         'Busca tu unidad, lee la sección correspondiente y haz los ejercicios autocorregidos. Las calculadoras te dejan comprobar tu álgebra.',
         'ابحث عن وحدتك، واقرأ القسم المطابق، ثم حل التمارين ذاتية التصحيح. تتيح لك الحاسبات التحقق من حساباتك الجبرية.',
         'Trova la tua unità, leggi la sezione corrispondente, poi svolgi gli esercizi autocorretti. I calcolatori ti fanno verificare l’algebra.'),
)
AP1_ROWS = [
 R(S('1'), T('Kinematics', 'Cinématique', 'Cinemática', 'علم الحركة', 'Cinematica'), ['Physics_Math.html#drag', 'Projectile_Motion_Drag_Calculator.html', 'Physics_Lab.html']),
 R(S('2'), T('Force and Translational Dynamics', 'Force et dynamique de translation', 'Fuerza y dinámica traslacional', 'القوة وديناميكا الانتقال', 'Forza e dinamica traslazionale'), ['Orbit_Math.html#circular', 'Orbital_Velocity_Calculator.html', 'Thrust_to_Weight_Calculator.html', 'Lift_Equation_Calculator.html']),
 R(S('3'), T('Work, Energy, and Power', 'Travail, énergie et puissance', 'Trabajo, energía y potencia', 'الشغل والطاقة والقدرة', 'Lavoro, energia e potenza'), ['Rotor_Hover_Power_Calculator.html', 'Orbital_Velocity_Calculator.html']),
 R(S('4'), T('Linear Momentum', 'Quantité de mouvement', 'Momento lineal', 'كمية الحركة الخطية', 'Quantità di moto'), ['Orbit_Math.html#rocket', 'Delta_V_Calculator.html']),
 R(S('7'), T('Oscillations', 'Oscillations', 'Oscilaciones', 'الاهتزازات', 'Oscillazioni'), ['Physics_Math.html#osc', 'Pendulum_Period_Calculator.html']),
 R(S('8'), T('Fluids', 'Fluides', 'Fluidos', 'الموائع', 'Fluidi'), ['Aero_Math.html#airfoil', 'Lift_Equation_Calculator.html', 'Stall_Speed_Calculator.html']),
]
AP2_ROWS = [
 R(S('9'), T('Thermodynamics (ideal gas)', 'Thermodynamique (gaz parfait)', 'Termodinámica (gas ideal)', 'الديناميكا الحرارية (الغاز المثالي)', 'Termodinamica (gas ideale)'), ['Mach_Number_Calculator.html']),
 R(S('14'), T('Waves, Sound, and Physical Optics (speed of sound)', 'Ondes, son et optique physique (vitesse du son)', 'Ondas, sonido y óptica física (velocidad del sonido)', 'الموجات والصوت والبصريات الفيزيائية (سرعة الصوت)', 'Onde, suono e ottica fisica (velocità del suono)'), ['Mach_Number_Calculator.html', 'Aero_Math.html#compress']),
]
IB_ROWS = [
 R(S('A.1'), T('Kinematics', 'Cinématique', 'Cinemática', 'علم الحركة', 'Cinematica'), ['Physics_Math.html#drag', 'Projectile_Motion_Drag_Calculator.html']),
 R(S('A.2'), T('Forces and momentum', 'Forces et quantité de mouvement', 'Fuerzas y momento', 'القوى وكمية الحركة', 'Forze e quantità di moto'), ['Delta_V_Calculator.html', 'Thrust_to_Weight_Calculator.html', 'Lift_Equation_Calculator.html']),
 R(S('A.3'), T('Work, energy and power', 'Travail, énergie et puissance', 'Trabajo, energía y potencia', 'الشغل والطاقة والقدرة', 'Lavoro, energia e potenza'), ['Rotor_Hover_Power_Calculator.html']),
 R(S('C.1'), T('Simple harmonic motion', 'Mouvement harmonique simple', 'Movimiento armónico simple', 'الحركة التوافقية البسيطة', 'Moto armonico semplice'), ['Physics_Math.html#osc', 'Pendulum_Period_Calculator.html']),
 R(S('D.1'), T('Gravitational fields (orbits, escape speed)', 'Champs gravitationnels (orbites, vitesse de libération)', 'Campos gravitatorios (órbitas, velocidad de escape)', 'مجالات الجاذبية (المدارات، سرعة الإفلات)', 'Campi gravitazionali (orbite, velocità di fuga)'), ['Orbit_Math.html#circular', 'Orbital_Period_Calculator.html', 'Orbital_Velocity_Calculator.html', 'Hohmann_Transfer_Calculator.html']),
]
AP_SRC = [f'College Board, <a href="{CAP_AP1}">AP Physics 1: Algebra-Based Course and Exam Description</a> (PDF).', f'College Board, <a href="{CAP_AP2}">AP Physics 2: Algebra-Based Course at a Glance</a> (PDF).',
          f'International Baccalaureate Organization, <a href="{IBO}">DP Physics subject brief</a> (PDF).']
