#!/usr/bin/env python3
"""Oct 15: sourced Five W's sections for pages/sections that lacked one (Nancy Grace Roman; the three
on-the-horizon tsunami tools: GUARDIAN, SWOT tsunami forecasts, seafloor cable sensing).
English HTML is written between <!-- FIVEWS:<id>:START/END --> markers (idempotent); fr/es/ar/it strings are
merged into i18n/<lang>.json so scripts/i18n-build.py translates them. Every fact is taken from the page's own
cited sources, linked under each card. Run before i18n-build.py (weekly-sync does)."""
import json, re, html
L = ['fr', 'es', 'ar', 'it']
NASA_ROMAN = ('https://science.nasa.gov/mission/roman-space-telescope/', 'NASA, Roman mission page')
ROMAN_LAUNCH = ('https://www.nasa.gov/news-release/nasas-dark-universe-seeking-nancy-grace-roman-space-telescope-launches/', 'NASA, Roman launch release (Aug 30, 2026)')
ROMAN_WHO = ('https://science.nasa.gov/mission/roman-space-telescope/who-is-nancy-grace-roman/', 'NASA, Who is Nancy Grace Roman?')
L2 = ('https://science.nasa.gov/resource/what-is-a-lagrange-point/', 'NASA, What is a Lagrange point?')
JPL_G = ('https://www.jpl.nasa.gov/news/nasas-guardian-tsunami-detection-tech-catches-wave-in-real-time/', 'NASA JPL, GUARDIAN catches wave in real time')
JPL_GA = ('https://guardian.jpl.nasa.gov/about.html', 'NASA JPL, About GUARDIAN')
SWOT_N = ('https://www.nasa.gov/missions/swot/us-french-swot-satellite-measures-tsunami-after-massive-quake/', 'NASA, SWOT satellite measures tsunami after massive quake')
SWOT_S = ('https://doi.org/10.1126/science.aeb8634', 'Sepúlveda et al., Science (2026)')
CAB = ('https://arxiv.org/abs/2509.24813', 'Mazur et al., arXiv preprint')
UNESCO = ('https://www.unesco.org/en/articles/pacific-tsunami-leaders-advance-regional-readiness-and-innovation-honolulu', 'UNESCO, Pacific tsunami leaders meet in Honolulu')

# (English, fr, es, ar, it)
S = {
 'h_roman': ("The Five W's of the Roman Space Telescope", "Les cinq W du télescope spatial Roman", "Las cinco W del telescopio espacial Roman", "الأسئلة الخمسة عن تلسكوب رومان الفضائي", "Le cinque W del telescopio spaziale Roman"),
 'roman_who': ("NASA builds and operates Roman. The telescope is named for Nancy Grace Roman, NASA's first Chief of Astronomy, known as the \"mother of Hubble.\"",
   "La NASA construit et exploite Roman. Le télescope porte le nom de Nancy Grace Roman, première responsable de l’astronomie de la NASA, surnommée la « mère de Hubble ».",
   "La NASA construye y opera Roman. El telescopio lleva el nombre de Nancy Grace Roman, la primera jefa de Astronomía de la NASA, conocida como la «madre del Hubble».",
   "تبني ناسا تلسكوب رومان وتشغّله. ويحمل التلسكوب اسم نانسي غريس رومان، أول رئيسة لقسم الفلك في ناسا، والملقبة بـ«أم هابل».",
   "La NASA costruisce e gestisce Roman. Il telescopio porta il nome di Nancy Grace Roman, prima responsabile dell’astronomia della NASA, nota come la «madre di Hubble»."),
 'roman_what': ("A space telescope with a mirror the size of Hubble's (2.4 m) and images just as sharp, but each picture covers at least 100 times more sky. It is built to study dark energy and dark matter, map a billion galaxies and take a census of planets.",
   "Un télescope spatial doté d’un miroir de la taille de celui de Hubble (2,4 m) et d’images tout aussi nettes, mais chaque image couvre au moins 100 fois plus de ciel. Il est conçu pour étudier l’énergie noire et la matière noire, cartographier un milliard de galaxies et recenser les planètes.",
   "Un telescopio espacial con un espejo del tamaño del de Hubble (2,4 m) e imágenes igual de nítidas, pero cada imagen cubre al menos 100 veces más cielo. Está diseñado para estudiar la energía oscura y la materia oscura, cartografiar mil millones de galaxias y hacer un censo de planetas.",
   "تلسكوب فضائي بمرآة بحجم مرآة هابل (2.4 م) وصور بالدقة نفسها، لكن كل صورة تغطي من السماء ما لا يقل عن 100 ضعف. صُمّم لدراسة الطاقة المظلمة والمادة المظلمة ورسم خريطة لمليار مجرة وإحصاء الكواكب.",
   "Un telescopio spaziale con uno specchio grande come quello di Hubble (2,4 m) e immagini altrettanto nitide, ma ogni immagine copre almeno 100 volte più cielo. È progettato per studiare l’energia oscura e la materia oscura, mappare un miliardo di galassie e fare un censimento dei pianeti."),
 'roman_when': ("Launched August 30, 2026 on a SpaceX Falcon Heavy. NASA expects its first images by early 2027.",
   "Lancé le 30 août 2026 par une Falcon Heavy de SpaceX. La NASA attend ses premières images d’ici début 2027.",
   "Lanzado el 30 de agosto de 2026 en un Falcon Heavy de SpaceX. La NASA espera sus primeras imágenes a principios de 2027.",
   "أُطلق في 30 أغسطس 2026 على صاروخ فالكون هيفي من سبيس إكس. وتتوقع ناسا صوره الأولى بحلول أوائل 2027.",
   "Lanciato il 30 agosto 2026 con un Falcon Heavy di SpaceX. La NASA prevede le prime immagini entro l’inizio del 2027."),
 'roman_where': ("In orbit around Sun-Earth L2, a balance point about 1.5 million km (about 930,000 miles) from Earth, near the Webb telescope.",
   "En orbite autour du point L2 Soleil-Terre, un point d’équilibre à environ 1,5 million de km de la Terre, près du télescope Webb.",
   "En órbita alrededor del punto L2 Sol-Tierra, un punto de equilibrio a unos 1,5 millones de km de la Tierra, cerca del telescopio Webb.",
   "في مدار حول نقطة L2 بين الشمس والأرض، وهي نقطة توازن على بعد نحو 1.5 مليون كم من الأرض، قرب تلسكوب ويب.",
   "In orbita attorno al punto L2 Sole-Terra, un punto di equilibrio a circa 1,5 milioni di km dalla Terra, vicino al telescopio Webb."),
 'roman_why': ("Roman's census of planets across our galaxy, with more than 1,000 exoplanets expected, will help show how rare a world like Earth may be. Knowing how special our home is gives people one more reason to protect its oceans, forests and wildlife.",
   "Le recensement des planètes de notre galaxie par Roman, avec plus de 1 000 exoplanètes attendues, aidera à montrer à quel point un monde comme la Terre est peut-être rare. Savoir combien notre planète est précieuse donne une raison de plus de protéger ses océans, ses forêts et sa faune.",
   "El censo de planetas de nuestra galaxia que hará Roman, con más de 1.000 exoplanetas previstos, ayudará a mostrar lo raro que puede ser un mundo como la Tierra. Saber lo especial que es nuestro hogar da una razón más para proteger sus océanos, bosques y fauna.",
   "سيساعد إحصاء رومان للكواكب في مجرتنا، مع توقع اكتشاف أكثر من 1000 كوكب خارجي، على إظهار مدى ندرة عالم مثل الأرض. ومعرفة مدى تميّز موطننا تمنح الناس سببًا إضافيًا لحماية محيطاته وغاباته وحياته البرية.",
   "Il censimento dei pianeti della nostra galassia condotto da Roman, con oltre 1.000 esopianeti attesi, aiuterà a capire quanto possa essere raro un mondo come la Terra. Sapere quanto è speciale la nostra casa dà un motivo in più per proteggerne oceani, foreste e fauna."),
 'h_tools': ("The Five W's of the Tsunami Tools on the Horizon", "Les cinq W des outils anti-tsunami à l’horizon", "Las cinco W de las herramientas contra tsunamis en el horizonte", "الأسئلة الخمسة عن أدوات رصد التسونامي القادمة", "Le cinque W degli strumenti per gli tsunami in arrivo"),
 'tools_intro': ("These three tools are potential solutions still being tested. None of them issues official warnings today.",
   "Ces trois outils sont des solutions potentielles encore à l’essai. Aucun n’émet aujourd’hui d’alerte officielle.",
   "Estas tres herramientas son soluciones potenciales que aún se están probando. Ninguna emite hoy alertas oficiales.",
   "هذه الأدوات الثلاث حلول محتملة لا تزال قيد الاختبار، ولا يُصدر أيٌّ منها تحذيرات رسمية حتى اليوم.",
   "Questi tre strumenti sono soluzioni potenziali ancora in fase di test. Nessuno di essi oggi emette allerte ufficiali."),
 'g_title': ("GUARDIAN (NASA JPL)",)*5,
 'g_who': ("NASA's Jet Propulsion Laboratory (JPL) develops GUARDIAN; trained experts review its outputs.",
   "Le Jet Propulsion Laboratory (JPL) de la NASA développe GUARDIAN ; des experts formés vérifient ses résultats.",
   "El Jet Propulsion Laboratory (JPL) de la NASA desarrolla GUARDIAN; expertos capacitados revisan sus resultados.",
   "يطوّر مختبر الدفع النفاث (JPL) التابع لناسا نظام GUARDIAN، ويراجع خبراء مدرَّبون نتائجه.",
   "Il Jet Propulsion Laboratory (JPL) della NASA sviluppa GUARDIAN; esperti qualificati ne verificano i risultati."),
 'g_what': ("A system that uses SI to spot the tiny ripples a tsunami sends up to the ionosphere, which slightly bend GPS and other navigation signals.",
   "Un système qui utilise la SI pour repérer les minuscules ondulations qu’un tsunami envoie jusqu’à l’ionosphère, où elles dévient légèrement les signaux GPS et d’autres signaux de navigation.",
   "Un sistema que usa SI para detectar las diminutas ondulaciones que un tsunami envía hasta la ionosfera, que desvían ligeramente las señales GPS y otras de navegación.",
   "نظام يستخدم SI لرصد التموجات الدقيقة التي يرسلها التسونامي إلى طبقة الأيونوسفير، فتنحرف بسببها إشارات GPS وغيرها من إشارات الملاحة قليلًا.",
   "Un sistema che usa la SI per individuare le minuscole increspature che uno tsunami spinge fino alla ionosfera, dove deviano leggermente i segnali GPS e altri segnali di navigazione."),
 'g_when': ("During the July 29, 2025 (UTC) Kamchatka earthquake it sent notices to experts in as little as 20 minutes and confirmed the tsunami about 30 to 40 minutes before waves reached Hawaii.",
   "Lors du séisme du Kamtchatka du 29 juillet 2025 (UTC), il a alerté des experts en 20 minutes seulement et confirmé le tsunami environ 30 à 40 minutes avant que les vagues n’atteignent Hawaï.",
   "Durante el terremoto de Kamchatka del 29 de julio de 2025 (UTC) envió avisos a expertos en apenas 20 minutos y confirmó el tsunami unos 30 a 40 minutos antes de que las olas llegaran a Hawái.",
   "خلال زلزال كامتشاتكا في 29 يوليو 2025 (بالتوقيت العالمي) أرسل إشعارات إلى الخبراء خلال 20 دقيقة فقط، وأكّد وجود التسونامي قبل وصول الأمواج إلى هاواي بنحو 30 إلى 40 دقيقة.",
   "Durante il terremoto della Kamčatka del 29 luglio 2025 (UTC) ha inviato avvisi agli esperti in appena 20 minuti e ha confermato lo tsunami circa 30-40 minuti prima che le onde raggiungessero le Hawaii."),
 'g_where': ("It reads data from more than 350 ground stations around the world and can sense a tsunami up to about 1,200 km (745 miles) from a station.",
   "Il exploite les données de plus de 350 stations au sol dans le monde et peut détecter un tsunami jusqu’à environ 1 200 km d’une station.",
   "Lee datos de más de 350 estaciones terrestres de todo el mundo y puede detectar un tsunami hasta a unos 1.200 km de una estación.",
   "يقرأ بيانات أكثر من 350 محطة أرضية حول العالم، ويمكنه رصد تسونامي على بعد نحو 1200 كم من المحطة.",
   "Legge i dati di oltre 350 stazioni a terra in tutto il mondo e può rilevare uno tsunami fino a circa 1.200 km da una stazione."),
 'g_why': ("Every extra data point helps warning centers decide sooner to evacuate, which saves lives on the coast and gives coastal communities time to protect what they depend on.",
   "Chaque donnée supplémentaire aide les centres d’alerte à décider plus tôt d’évacuer, ce qui sauve des vies sur la côte et laisse aux communautés côtières le temps de protéger ce dont elles dépendent.",
   "Cada dato adicional ayuda a los centros de alerta a decidir antes una evacuación, lo que salva vidas en la costa y da a las comunidades costeras tiempo para proteger aquello de lo que dependen.",
   "كل معلومة إضافية تساعد مراكز الإنذار على اتخاذ قرار الإخلاء أسرع، مما ينقذ الأرواح على الساحل ويمنح المجتمعات الساحلية وقتًا لحماية ما تعتمد عليه.",
   "Ogni dato in più aiuta i centri di allerta a decidere prima un’evacuazione: salva vite sulla costa e dà alle comunità costiere il tempo di proteggere ciò da cui dipendono."),
 's_title': ("SWOT for tsunami forecasts (NASA and CNES)", "SWOT pour la prévision des tsunamis (NASA et CNES)", "SWOT para pronosticar tsunamis (NASA y CNES)", "SWOT للتنبؤ بالتسونامي (ناسا وCNES)", "SWOT per le previsioni degli tsunami (NASA e CNES)"),
 's_who': ("NASA and France's space agency CNES run the SWOT satellite; NOAA tsunami scientists and university teams study its tsunami data.",
   "La NASA et l’agence spatiale française CNES exploitent le satellite SWOT ; des scientifiques de la NOAA et des équipes universitaires étudient ses données sur les tsunamis.",
   "La NASA y la agencia espacial francesa CNES operan el satélite SWOT; científicos de la NOAA y equipos universitarios estudian sus datos de tsunamis.",
   "تشغّل ناسا ووكالة الفضاء الفرنسية CNES القمر الصناعي SWOT، ويدرس علماء التسونامي في NOAA وفرق جامعية بياناته عن التسونامي.",
   "La NASA e l’agenzia spaziale francese CNES gestiscono il satellite SWOT; scienziati della NOAA e gruppi universitari ne studiano i dati sugli tsunami."),
 's_what': ("A water-measuring satellite whose wide radar swath gave the first high-resolution, two-dimensional view of a great tsunami from space.",
   "Un satellite de mesure de l’eau dont la large fauchée radar a offert la première vue en deux dimensions et à haute résolution d’un grand tsunami depuis l’espace.",
   "Un satélite que mide el agua y cuya amplia franja de radar ofreció la primera vista bidimensional y de alta resolución de un gran tsunami desde el espacio.",
   "قمر صناعي لقياس المياه أتاح نطاقه الراداري الواسع أول رؤية ثنائية الأبعاد عالية الدقة لتسونامي كبير من الفضاء.",
   "Un satellite che misura l’acqua, la cui ampia fascia radar ha offerto la prima vista bidimensionale ad alta risoluzione di un grande tsunami dallo spazio."),
 's_when': ("About 70 minutes after the July 2025 Kamchatka earthquake, SWOT measured the leading wave at more than 45 cm (1.5 feet) high.",
   "Environ 70 minutes après le séisme du Kamtchatka de juillet 2025, SWOT a mesuré la vague de tête à plus de 45 cm de haut.",
   "Unos 70 minutos después del terremoto de Kamchatka de julio de 2025, SWOT midió la ola principal con más de 45 cm de altura.",
   "بعد نحو 70 دقيقة من زلزال كامتشاتكا في يوليو 2025، قاس SWOT الموجة الأمامية بارتفاع يزيد على 45 سم.",
   "Circa 70 minuti dopo il terremoto della Kamčatka di luglio 2025, SWOT ha misurato l’onda di testa a oltre 45 cm di altezza."),
 's_where': ("Over the open Pacific Ocean, from orbit.", "Au-dessus du Pacifique, depuis l’orbite.", "Sobre el océano Pacífico abierto, desde la órbita.", "فوق المحيط الهادئ المفتوح، من المدار.", "Sopra il Pacifico aperto, dall’orbita."),
 's_why': ("NOAA's Vasily Titov said SWOT data \"could significantly enhance operational tsunami forecasts.\" Better forecasts mean safer coasts for people and less needless disruption.",
   "Vasily Titov, de la NOAA, estime que les données de SWOT « pourraient améliorer considérablement les prévisions opérationnelles de tsunamis ». De meilleures prévisions signifient des côtes plus sûres et moins de perturbations inutiles.",
   "Vasily Titov, de la NOAA, dijo que los datos de SWOT «podrían mejorar significativamente los pronósticos operativos de tsunamis». Mejores pronósticos significan costas más seguras y menos trastornos innecesarios.",
   "قال فاسيلي تيتوف من NOAA إن بيانات SWOT «قد تحسّن بشكل كبير التنبؤات التشغيلية بالتسونامي». والتنبؤات الأفضل تعني سواحل أكثر أمانًا للناس واضطرابًا أقل بلا داعٍ.",
   "Vasily Titov della NOAA ha detto che i dati di SWOT «potrebbero migliorare in modo significativo le previsioni operative degli tsunami». Previsioni migliori significano coste più sicure e meno disagi inutili."),
 'c_title': ("Seafloor cable sensing", "Détection par câbles sous-marins", "Detección con cables submarinos", "الاستشعار بكابلات قاع البحر", "Rilevamento con cavi sottomarini"),
 'c_who': ("Research teams working with telecom cables; Pacific tsunami warning leaders are reviewing SMART cables (cables with built-in sensors).",
   "Des équipes de recherche travaillant avec des câbles de télécommunication ; les responsables de l’alerte aux tsunamis du Pacifique étudient les câbles SMART (câbles équipés de capteurs).",
   "Equipos de investigación que trabajan con cables de telecomunicaciones; los responsables de alerta de tsunamis del Pacífico están evaluando los cables SMART (cables con sensores integrados).",
   "فرق بحثية تعمل على كابلات الاتصالات، ويدرس قادة الإنذار من التسونامي في المحيط الهادئ كابلات SMART (كابلات مزوّدة بأجهزة استشعار).",
   "Gruppi di ricerca che lavorano con i cavi per telecomunicazioni; i responsabili dell’allerta tsunami del Pacifico stanno valutando i cavi SMART (cavi con sensori integrati)."),
 'c_what': ("Researchers turned a 4,400 km internet cable into about 44,000 sensors spaced 100 meters apart. It recorded the magnitude 8.8 earthquake and, in a first, a tsunami wave in the deep ocean.",
   "Des chercheurs ont transformé un câble internet de 4 400 km en environ 44 000 capteurs espacés de 100 mètres. Il a enregistré le séisme de magnitude 8,8 et, pour la première fois, une vague de tsunami en eau profonde.",
   "Investigadores convirtieron un cable de internet de 4.400 km en unos 44.000 sensores separados 100 metros. Registró el terremoto de magnitud 8,8 y, por primera vez, una ola de tsunami en aguas profundas.",
   "حوّل باحثون كابل إنترنت طوله 4400 كم إلى نحو 44000 جهاز استشعار تفصل بينها 100 متر. فسجّل الزلزال بقوة 8.8، وللمرة الأولى موجة تسونامي في أعماق المحيط.",
   "Alcuni ricercatori hanno trasformato un cavo internet di 4.400 km in circa 44.000 sensori distanziati 100 metri. Ha registrato il terremoto di magnitudo 8,8 e, per la prima volta, un’onda di tsunami in acque profonde."),
 'c_when': ("The recording came from the July 2025 Kamchatka event. On October 5, 2026, Pacific tsunami leaders in Honolulu asked for more testing before warning centers rely on cables.",
   "L’enregistrement date de l’événement du Kamtchatka de juillet 2025. Le 5 octobre 2026, à Honolulu, les responsables du Pacifique ont demandé davantage d’essais avant que les centres d’alerte ne s’appuient sur ces câbles.",
   "El registro procede del evento de Kamchatka de julio de 2025. El 5 de octubre de 2026, en Honolulu, los responsables del Pacífico pidieron más pruebas antes de que los centros de alerta dependan de los cables.",
   "جاء التسجيل من حدث كامتشاتكا في يوليو 2025. وفي 5 أكتوبر 2026 طلب قادة الإنذار في المحيط الهادئ، خلال اجتماعهم في هونولولو، مزيدًا من الاختبارات قبل أن تعتمد مراكز الإنذار على الكابلات.",
   "La registrazione risale all’evento della Kamčatka di luglio 2025. Il 5 ottobre 2026, a Honolulu, i responsabili del Pacifico hanno chiesto altri test prima che i centri di allerta si affidino ai cavi."),
 'c_where': ("On the Pacific seafloor; the tsunami was detected about 1,000 km offshore.", "Sur le fond du Pacifique ; le tsunami a été détecté à environ 1 000 km au large.", "En el fondo del Pacífico; el tsunami se detectó a unos 1.000 km de la costa.", "في قاع المحيط الهادئ، ورُصد التسونامي على بعد نحو 1000 كم من الساحل.", "Sul fondale del Pacifico; lo tsunami è stato rilevato a circa 1.000 km dalla costa."),
 'c_why': ("Cables already cross the oceans, so reusing them could add many deep-ocean sensors without building new ones, giving coastal people earlier, surer warnings. The study is a preprint and is not yet used for official warnings.",
   "Les câbles traversent déjà les océans : les réutiliser pourrait ajouter de nombreux capteurs en eau profonde sans en construire de nouveaux, et donner aux populations côtières des alertes plus précoces et plus sûres. L’étude est une prépublication et n’est pas encore utilisée pour les alertes officielles.",
   "Los cables ya cruzan los océanos, así que reutilizarlos podría añadir muchos sensores en aguas profundas sin construir otros nuevos y dar a la población costera alertas más tempranas y fiables. El estudio es una preimpresión y aún no se usa para alertas oficiales.",
   "تعبر الكابلات المحيطات بالفعل، لذا فإن إعادة استخدامها قد تضيف أجهزة استشعار كثيرة في أعماق المحيط دون بناء أجهزة جديدة، وتمنح سكان السواحل تحذيرات أبكر وأدق. الدراسة نسخة أولية ولا تُستخدم بعد في التحذيرات الرسمية.",
   "I cavi attraversano già gli oceani: riutilizzarli potrebbe aggiungere molti sensori in acque profonde senza costruirne di nuovi e dare alle popolazioni costiere allerte più precoci e affidabili. Lo studio è un preprint e non è ancora usato per le allerte ufficiali."),
}
e = lambda s: html.escape(s, quote=False)
W = ['Who', 'What', 'When', 'Where', 'Why']
def card(w, key, srcs):
    return (f'<div class="w-card"><h3>{w}</h3><p>{e(S[key][0])}</p>' +
            ''.join(f'<p class="fact-source">Source: <a href="{u}" target="_blank" rel="noreferrer">{e(n)}</a></p>' for u, n in srcs) + '</div>')
def grid(prefix, srcs):
    return '<div class="ws-grid">' + ''.join(card(w, f'{prefix}_{w.lower()}', srcs[w]) for w in W) + '</div>'
roman = ('<section class="five-ws" id="five-ws"><h2>' + e(S['h_roman'][0]) + '</h2>' +
         grid('roman', {'Who': [NASA_ROMAN, ROMAN_WHO], 'What': [NASA_ROMAN, ROMAN_LAUNCH], 'When': [ROMAN_LAUNCH], 'Where': [NASA_ROMAN, L2], 'Why': [ROMAN_LAUNCH]}) + '</section>')
tools = ('<section class="five-ws" id="horizon-five-ws"><h2>' + e(S['h_tools'][0]) + '</h2><p>' + e(S['tools_intro'][0]) + '</p>' +
         '<h3 id="guardian-five-ws">' + e(S['g_title'][0]) + '</h3>' + grid('g', {'Who': [JPL_GA], 'What': [JPL_G], 'When': [JPL_G], 'Where': [JPL_G], 'Why': [JPL_G]}) +
         '<h3 id="swot-five-ws">' + e(S['s_title'][0]) + '</h3>' + grid('s', {'Who': [SWOT_N], 'What': [SWOT_N], 'When': [SWOT_N], 'Where': [SWOT_N], 'Why': [SWOT_N, SWOT_S]}) +
         '<h3 id="cable-five-ws">' + e(S['c_title'][0]) + '</h3>' + grid('c', {'Who': [CAB, UNESCO], 'What': [CAB], 'When': [CAB, UNESCO], 'Where': [CAB], 'Why': [CAB, UNESCO]}) + '</section>')
def put(page, mid, block, anchor_re):
    s = open(page, encoding='utf8').read()
    wrapped = f'<!-- FIVEWS:{mid}:START -->{block}<!-- FIVEWS:{mid}:END -->'
    r = re.compile(rf'<!-- FIVEWS:{mid}:START -->.*?<!-- FIVEWS:{mid}:END -->', re.S)
    if r.search(s): s2 = r.sub(lambda m: wrapped, s)
    else:
        m = re.search(anchor_re, s, re.S)
        if not m: print(f'build-fivews: anchor not found in {page}'); return
        s2 = s[:m.start()] + wrapped + s[m.start():]
    if s2 != s: open(page, 'w', encoding='utf8').write(s2)
put('Nancy_Grace_Roman.html', 'roman', roman, r'<section class="impact" id="impact"')
put('Tsunami_Early_Warning.html', 'tsunami-horizon', tools, r'<section class="impact" id="impact"')
for i, l in enumerate(L, 1):
    p = f'i18n/{l}.json'; d = json.load(open(p, encoding='utf8')); n = 0
    for v in S.values():
        if len(v) == 5 and d.get(v[0]) != v[i]: d[v[0]] = v[i]; n += 1
    if n: json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('build-fivews: Nancy_Grace_Roman + Tsunami_Early_Warning (GUARDIAN, SWOT, cables) up to date')
