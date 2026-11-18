#!/usr/bin/env python3
"""Insert the to-scale ascent visual into Orbit_Lab.html (en, fr, es, ar, it)."""
import html, json, os, re
LANGS = ['en', 'fr', 'es', 'ar', 'it']
def T(en, fr, es, ar, it):
    return dict(en=en, fr=fr, es=es, ar=ar, it=it)
S = {
 'h': T('Reaching orbit', 'Atteindre l’orbite', 'Llegar a la órbita', 'الوصول إلى المدار', 'Raggiungere l’orbita'),
 'lead': T('A satellite stays up because it moves sideways fast enough to fall around Earth. At 400 km that speed is 7.67 km/s, from μ = 398 600.4418 km³/s² and the WGS-84 radius. Height alone brings you back down.',
           'Un satellite reste en l’air parce qu’il va assez vite de côté pour tomber autour de la Terre. À 400 km cette vitesse est 7,67 km/s, avec μ = 398 600,4418 km³/s² et le rayon WGS-84. La hauteur seule vous ramène au sol.',
           'Un satélite se mantiene porque se mueve de lado lo bastante rápido para caer alrededor de la Tierra. A 400 km esa velocidad es 7,67 km/s, con μ = 398 600,4418 km³/s² y el radio WGS-84. Solo la altura te devuelve al suelo.',
           'يبقى القمر الصناعي لأنه يتحرك جانبيًا بسرعة تكفي ليسقط حول الأرض. عند 400 كم هذه السرعة 7.67 كم/ث، من μ = 398600.4418 كم³/ث² ونصف قطر WGS-84. الارتفاع وحده يعيدك إلى الأرض.',
           'Un satellite resta su perché si muove di lato abbastanza veloce da cadere intorno alla Terra. A 400 km quella velocità è 7,67 km/s, con μ = 398 600,4418 km³/s² e il raggio WGS-84. La sola quota ti riporta a terra.'),
 'model': T('The gold path is a teaching model drawn to scale on a NASA Blue Marble, not a recording of one rocket. Speed grows from 0 to circular-orbit speed while the flight-path angle goes from straight up to horizontal. The chart under the globe plots altitude against downrange in kilometres, so the bend from straight up to sideways is easy to see. The globe itself is to scale. Drag and a real guidance computer are left out. Dynamic pressure uses the U.S. Standard Atmosphere, 1976, below its 86 km top.',
            'Le tracé doré est un modèle pédagogique à l’échelle sur un Blue Marble de la NASA, pas l’enregistrement d’une fusée. La vitesse va de 0 à la vitesse circulaire pendant que l’angle de trajectoire passe de la verticale à l’horizontale. Le graphique sous le globe porte l’altitude en fonction de la distance au sol, en kilomètres. Le globe lui-même est à l’échelle. La traînée et un vrai guidage sont omis. La pression dynamique utilise l’atmosphère standard américaine de 1976, sous son sommet à 86 km.',
            'La curva dorada es un modelo didáctico a escala sobre un Blue Marble de la NASA, no la grabación de un cohete. La velocidad va de 0 a la circular mientras el ángulo de trayectoria pasa de vertical a horizontal. El gráfico bajo el globo muestra la altitud frente a la distancia en kilómetros. El globo en sí está a escala. Se omiten el arrastre y un guiado real. La presión dinámica usa la atmósfera estándar de EE. UU. de 1976, bajo su tope de 86 km.',
            'المسار الذهبي نموذج تعليمي بمقياس حقيقي على صورة Blue Marble من ناسا، وليس تسجيل صاروخ بعينه. السرعة تنمو من صفر إلى السرعة الدائرية بينما تهبط زاوية المسار من الرأسي إلى الأفقي. الرسم تحت الكرة يضع الارتفاع مقابل المسافة الأفقية بالكيلومترات. الكرة نفسها بمقياس حقيقي. أُهمل السحب والتوجيه الحقيقي. الضغط الديناميكي يستخدم الغلاف القياسي الأمريكي 1976 تحت حده 86 كم.',
            'La traccia dorata è un modello didattico in scala su un Blue Marble della NASA, non la registrazione di un razzo. La velocità va da 0 a quella circolare mentre l’angolo di rotta passa da verticale a orizzontale. Il grafico sotto il globo mette la quota contro la distanza a terra, in chilometri. Il globo stesso è in scala. Resistenza e guida reale sono omesse. La pressione dinamica usa l’atmosfera standard USA 1976, sotto i suoi 86 km.'),
 'layers': T('The air, in NASA’s five layers', 'L’air, en cinq couches selon la NASA', 'El aire, en las cinco capas de la NASA', 'الهواء في طبقات ناسا الخمس', 'L’aria, nei cinque strati della NASA'),
 'scale': T('Why the air runs out: gravity holds it near the ground. In the 1976 standard, sea-level temperature is 288.15 K, pressure 101 325 Pa, and molar mass 28.9644 kg/kmol. The sea-level scale height R_specific T/g is 8.43 km, so pressure and density fall roughly by a factor of e every 8.43 km while the lower layer is near that temperature. The model’s density is 1.225 kg/m³ at sea level. Above 86 km the 1976 tables stop. NASA places the International Space Station in the thermosphere, near 400 km, where enough molecules remain to drag it down slowly.',
            'Pourquoi l’air se raréfie : la gravité le garde près du sol. Dans la norme de 1976, la température au niveau de la mer est 288,15 K, la pression 101 325 Pa, et la masse molaire 28,9644 kg/kmol. La hauteur d’échelle au sol, R T/g, vaut 8,43 km : pression et masse volumique chutent d’un facteur e tous les 8,43 km tant que la température reste proche de cette valeur. La masse volumique du modèle est 1,225 kg/m³ au niveau de la mer. Au-dessus de 86 km les tables de 1976 s’arrêtent. La NASA place la Station spatiale dans la thermosphère, vers 400 km, où il reste assez de molécules pour la freiner lentement.',
            'Por qué se acaba el aire: la gravedad lo retiene junto al suelo. En la norma de 1976, la temperatura al nivel del mar es 288,15 K, la presión 101 325 Pa y la masa molar 28,9644 kg/kmol. La altura de escala en el suelo, R T/g, es 8,43 km: presión y densidad caen cerca de un factor e cada 8,43 km mientras la temperatura se parece a esa. La densidad del modelo es 1,225 kg/m³ al nivel del mar. Por encima de 86 km las tablas de 1976 terminan. La NASA sitúa la Estación Espacial en la termosfera, cerca de 400 km, donde aún hay moléculas suficientes para frenarla poco a poco.',
            'لماذا يرقّ الهواء: الجاذبية تبقيه قرب السطح. في معيار 1976، درجة الحرارة عند سطح البحر 288.15 كلفن، والضغط 101325 باسكال، والكتلة المولية 28.9644 كغ/كمول. ارتفاع المقياس عند السطح R T/g يساوي 8.43 كم، فينخفض الضغط والكثافة بنحو عامل e كل 8.43 كم ما دامت الحرارة قريبة من ذلك. كثافة النموذج 1.225 كغ/م³ عند سطح البحر. فوق 86 كم تتوقف جداول 1976. تضع ناسا محطة الفضاء في الغلاف الحراري قرب 400 كم، حيث تبقى جزيئات كافية لسحبها ببطء.',
            'Perché l’aria finisce: la gravità la tiene vicino al suolo. Nello standard 1976 la temperatura al livello del mare è 288,15 K, la pressione 101 325 Pa e la massa molare 28,9644 kg/kmol. L’altezza di scala al suolo, R T/g, è 8,43 km: pressione e densità calano di circa un fattore e ogni 8,43 km finché la temperatura resta vicina a quel valore. La densità del modello è 1,225 kg/m³ al livello del mare. Sopra 86 km le tabelle 1976 finiscono. La NASA colloca la Stazione spaziale nella termosfera, verso i 400 km, dove restano abbastanza molecole da frenarla piano.'),
 'stagewhy': T('Rockets stage because empty tanks and a heavy engine are dead mass: the rocket equation, Δv = v_e ln(m0/mf), punishes every kilogram you still carry. A sea-level nozzle is smaller so the exhaust does not peel away from the wall in thick air. A vacuum nozzle is larger: outside pressure is nearly zero, so the gas can expand further before it leaves. NASA Glenn writes the thrust as ṁ v_e + (p_e − p_0) A_e.',
              'On étage parce que des réservoirs vides et un moteur lourd sont une masse morte : l’équation de la fusée, Δv = v_e ln(m0/mf), punit chaque kilogramme encore emporté. Une tuyère au sol est plus petite pour que le jet ne décolle pas de la paroi dans l’air dense. Une tuyère à vide est plus grande : la pression extérieure est presque nulle, le gaz peut donc se détendre davantage. NASA Glenn écrit la poussée ṁ v_e + (p_e − p_0) A_e.',
              'Se usan etapas porque los tanques vacíos y un motor pesado son masa muerta: la ecuación del cohete, Δv = v_e ln(m0/mf), castiga cada kilogramo que sigues cargando. Una tobera al nivel del mar es más pequeña para que el chorro no se despegue de la pared en aire denso. Una tobera de vacío es mayor: la presión exterior es casi cero y el gas puede expandirse más. NASA Glenn escribe el empuje como ṁ v_e + (p_e − p_0) A_e.',
              'تُقسَّم الصواريخ إلى مراحل لأن الخزانات الفارغة والمحرك الثقيل كتلة ميتة: معادلة الصاروخ Δv = v_e ln(m0/mf) تعاقب كل كيلوغرام ما زلت تحمله. فوهة سطح البحر أصغر حتى لا ينفصل العادم عن الجدار في الهواء الكثيف. فوهة الفراغ أكبر: الضغط الخارجي شبه صفر، فيتمدد الغاز أكثر. تكتب ناسا غلين الدفع ṁ v_e + (p_e − p_0) A_e.',
              'Si usano stadi perché serbatoi vuoti e un motore pesante sono massa morta: l’equazione del razzo, Δv = v_e ln(m0/mf), punisce ogni chilogrammo ancora a bordo. Un ugello a livello del mare è più piccolo così il getto non si stacca dalla parete nell’aria densa. Un ugello da vuoto è più grande: la pressione esterna è quasi zero e il gas può espandersi di più. NASA Glenn scrive la spinta ṁ v_e + (p_e − p_0) A_e.'),
 'stay': T('Stay in orbit: plan a transfer', 'Rester en orbite : planifier un transfert', 'Seguir en órbita: planifica una transferencia', 'البقاء في المدار: خطّط لانتقال', 'Restare in orbita: pianifica un trasferimento'),
 'credit': T('Earth photograph: NASA Visible Earth / Blue Marble Next Generation (December, topography and bathymetry). The interactive globe is drawn from the 1 280 px or 1 920 px WebP of that image. The 4 096×2 048 master is on this site and is not loaded with the page.',
             'Photo de la Terre : NASA Visible Earth / Blue Marble Next Generation (décembre, topographie et bathymétrie). Le globe interactif est dessiné à partir du WebP 1 280 ou 1 920 px. Le fichier maître 4 096×2 048 est sur le site et n’est pas chargé avec la page.',
             'Fotografía de la Tierra: NASA Visible Earth / Blue Marble Next Generation (diciembre, topografía y batimetría). El globo interactivo se dibuja desde el WebP de 1 280 o 1 920 px. El máster de 4 096×2 048 está en el sitio y no se carga con la página.',
             'صورة الأرض: NASA Visible Earth / Blue Marble Next Generation (ديسمبر، تضاريس وعمق). الكرة التفاعلية تُرسم من WebP بدقة 1280 أو 1920. الأصل 4096×2048 موجود في الموقع ولا يُحمَّل مع الصفحة.',
             'Fotografia della Terra: NASA Visible Earth / Blue Marble Next Generation (dicembre, topografia e batimetria). Il globo interattivo è disegnato dal WebP a 1 280 o 1 920 px. Il master 4 096×2 048 è sul sito e non viene caricato con la pagina.'),
}
UI_KEYS = {
 'read': T('{h} km up, {v} km/s, flight path {g}° from horizontal, {layer}.',
           '{h} km d’altitude, {v} km/s, trajectoire à {g}° de l’horizontale, {layer}.',
           '{h} km de altura, {v} km/s, trayectoria a {g}° de la horizontal, {layer}.',
           'الارتفاع {h} كم، السرعة {v} كم/ث، المسار {g}° عن الأفق، {layer}.',
           '{h} km di quota, {v} km/s, rotta a {g}° dall’orizzontale, {layer}.'),
 'inset': T('Altitude ×8 (inset)', 'Altitude ×8 (encart)', 'Altitud ×8 (recuadro)', 'الارتفاع ×8 (إطار)', 'Quota ×8 (riquadro)'),
 'sideways': T('Sideways', 'De côté', 'De lado', 'جانبيًا', 'Di lato'),
 'play': T('Play the path', 'Lire la trajectoire', 'Reproducir la trayectoria', 'شغّل المسار', 'Riproduci la traiettoria'),
 'pause': T('Pause', 'Pause', 'Pausa', 'إيقاف', 'Pausa'),
 'scrub': T('Position along the teaching path', 'Position sur la trajectoire pédagogique', 'Posición en la trayectoria didáctica', 'الموضع على المسار التعليمي', 'Posizione sulla traiettoria didattica'),
 'levels': T('Caption level', 'Niveau de la légende', 'Nivel del texto', 'مستوى الشرح', 'Livello della didascalia'),
 'kids': T('Kids', 'Enfants', 'Niños', 'الأطفال', 'Bambini'),
 'school': T('School', 'Collège et lycée', 'Escuela', 'المدرسة', 'Scuola'),
 'uni': T('University', 'Université', 'Universidad', 'الجامعة', 'Università'),
 'stages': T('Jump to a stage', 'Aller à une étape', 'Saltar a una etapa', 'انتقل إلى مرحلة', 'Vai a una fase'),
 'tropo': T('Troposphere', 'Troposphère', 'Troposfera', 'التروبوسفير', 'Troposfera'),
 'strato': T('Stratosphere', 'Stratosphère', 'Estratosfera', 'الستراتوسفير', 'Stratosfera'),
 'meso': T('Mesosphere', 'Mésosphère', 'Mesosfera', 'الميزوسفير', 'Mesosfera'),
 'thermo': T('Thermosphere', 'Thermosphère', 'Termosfera', 'الثرموسفير', 'Termosfera'),
 'exo': T('Exosphere', 'Exosphère', 'Exosfera', 'الإكسوسفير', 'Esosfera'),
}
ST_LAB = {
 'liftoff': T('Liftoff', 'Décollage', 'Despegue', 'الإقلاع', 'Decollo'),
 'maxq': T('Max-Q', 'Max-Q', 'Max-Q', 'أقصى ضغط', 'Max-Q'),
 'turn': T('Gravity turn', 'Virage gravitationnel', 'Giro por gravedad', 'انعطاف الجاذبية', 'Gravity turn'),
 'sep': T('Staging', 'Séparation', 'Separación', 'فصل المرحلة', 'Separazione'),
 'fairing': T('Fairing', 'Coiffe', 'Cofia', 'الغطاء', 'Ogiv'),
 'burn2': T('Second burn', 'Second étage', 'Segunda etapa', 'المرحلة الثانية', 'Secondo stadio'),
 'seco': T('Insertion', 'Insertion', 'Inserción', 'دخول المدار', 'Inserzione'),
}
CAPS = {
 'liftoff': {
  'k': T('The rocket leaves straight up. Orbit is not “being high.” It is going sideways fast.',
         'La fusée part tout droit. L’orbite n’est pas « être haut ». C’est aller vite de côté.',
         'El cohete sale recto. La órbita no es «estar alto». Es ir rápido de lado.',
         'الصاروخ يصعد رأسيًا. المدار ليس «أن تكون عاليًا». هو أن تسير جانبيًا بسرعة.',
         'Il razzo parte dritto. L’orbita non è «essere in alto». È andare veloci di lato.'),
  's': T('Thrust is greater than weight, so it accelerates upward. The speed is still nowhere near 7.67 km/s.',
         'La poussée dépasse le poids, donc ça accélère vers le haut. La vitesse est encore loin de 7,67 km/s.',
         'El empuje supera el peso, así que acelera hacia arriba. La velocidad aún está lejos de 7,67 km/s.',
         'الدفع أكبر من الوزن، فيتسارع إلى الأعلى. السرعة ما زالت بعيدة عن 7.67 كم/ث.',
         'La spinta supera il peso, quindi accelera verso l’alto. La velocità è ancora lontana da 7,67 km/s.'),
  'u': T('Liftoff is vertical to clear the pad. The orbit is won later, when the velocity is horizontal.',
         'Le décollage est vertical pour quitter le pas de tir. L’orbite se gagne plus tard, vitesse horizontale.',
         'El despegue es vertical para alejarse de la rampa. La órbita se gana después, con velocidad horizontal.',
         'الإقلاع رأسي لترك المنصة. المدار يُكسب لاحقًا عندما تصبح السرعة أفقية.',
         'Il decollo è verticale per lasciare la rampa. L’orbita si vince dopo, con velocità orizzontale.'),
 },
 'maxq': {
  'k': T('The air pushes hardest around here, while you are still in the thick lower air and already moving fast.',
         'L’air pousse le plus fort par ici, encore dans l’air bas et déjà rapide.',
         'El aire empuja más fuerte por aquí, aún en el aire bajo y ya rápido.',
         'الهواء يضغط بأشد ما يكون هنا، وما زلت في الهواء السفلي الكثيف وقد صرت سريعًا.',
         'L’aria spinge di più qui, ancora nell’aria bassa e già veloci.'),
  's': T('Dynamic pressure is ½ ρ v². In this model it peaks in the troposphere. Real rockets often throttle down for a moment at max-Q.',
         'La pression dynamique est ½ ρ v². Dans ce modèle elle culmine dans la troposphère. Les vraies fusées réduisent souvent un instant les gaz au max-Q.',
         'La presión dinámica es ½ ρ v². En este modelo alcanza el máximo en la troposfera. Los cohetes reales suelen bajar un momento los motores en el max-Q.',
         'الضغط الديناميكي ½ ρ v². في هذا النموذج يبلغ ذروته في التروبوسفير. الصواريخ الحقيقية تخفض الدفع لحظة عند أقصى ضغط.',
         'La pressione dinamica è ½ ρ v². In questo modello ha il picco nella troposfera. I razzi veri spesso riducono un attimo la spinta al max-Q.'),
  'u': T('The peak is a result of this pitch program plus the 1976 density. It is not a number from a countdown transcript.',
         'Le pic vient de ce programme de tangage et de la densité de 1976. Ce n’est pas un chiffre d’un compte à rebours.',
         'El pico sale de este programa de cabeceo y de la densidad de 1976. No es una cifra de una cuenta atrás.',
         'الذروة نتيجة برنامج الميل هذا وكثافة 1976. ليست رقمًا من عدّ تنازلي.',
         'Il picco è un risultato di questo programma di beccheggio e della densità 1976. Non è un numero di un conto alla rovescia.'),
 },
 'turn': {
  'k': T('The rocket leans. Gravity bends the path toward the horizon. You have to go around, not just up.',
         'La fusée s’incline. La gravité courbe la trajectoire vers l’horizon. Il faut faire le tour, pas seulement monter.',
         'El cohete se inclina. La gravedad curva la trayectoria hacia el horizonte. Hay que dar la vuelta, no solo subir.',
         'الصاروخ يميل. الجاذبية تحني المسار نحو الأفق. عليك أن تدور، لا أن تصعد فقط.',
         'Il razzo si inclina. La gravità piega la traiettoria verso l’orizzonte. Devi girare intorno, non solo salire.'),
  's': T('A gravity turn spends the engines’ speed mostly sideways. The flight-path angle here is 45° from the horizontal.',
         'Un virage gravitationnel dépense la vitesse des moteurs surtout de côté. Ici l’angle est à 45° de l’horizontale.',
         'Un giro por gravedad gasta la velocidad de los motores sobre todo de lado. Aquí el ángulo está a 45° de la horizontal.',
         'انعطاف الجاذبية يصرف سرعة المحركات جانبيًا في الغالب. زاوية المسار هنا 45° عن الأفق.',
         'Un gravity turn spende la velocità dei motori soprattutto di lato. Qui l’angolo è a 45° dall’orizzontale.'),
  'u': T('Angle from the local horizontal. This program takes it from 90° to 0° by the time speed equals √(μ/r).',
         'Angle depuis l’horizontale locale. Ce programme le mène de 90° à 0° quand la vitesse égale √(μ/r).',
         'Ángulo desde la horizontal local. Este programa lo lleva de 90° a 0° cuando la velocidad iguala √(μ/r).',
         'الزاوية من الأفق المحلي. هذا البرنامج ينقلها من 90° إلى 0° عندما تساوي السرعة √(μ/r).',
         'Angolo dall’orizzontale locale. Questo programma lo porta da 90° a 0° quando la velocità eguaglia √(μ/r).'),
 },
 'sep': {
  'k': T('The empty bottom drops off. Carrying empty tanks all the way would waste the fuel you have left.',
         'Le bas vide se détache. Garder des réservoirs vides jusqu’au bout gâcherait le carburant qui reste.',
         'La parte vacía de abajo se suelta. Llevar tanques vacíos hasta el final gastaría el combustible que queda.',
         'الجزء السفلي الفارغ ينفصل. حمل الخزانات الفارغة حتى النهاية يهدر الوقود المتبقي.',
         'La parte vuota sotto si stacca. Portare serbatoi vuoti fino in fondo sprecherebbe il propellente rimasto.'),
  's': T('This marker is the path crossing 80.5 km, which is 50 statute miles, the older United States line for space. The thick air is behind you.',
         'Ce repère est le passage à 80,5 km, soit 50 milles terrestres, l’ancienne limite américaine de l’espace. L’air épais est derrière.',
         'Esta marca es el cruce de 80,5 km, 50 millas terrestres, el antiguo límite estadounidense del espacio. El aire espeso quedó atrás.',
         'هذه العلامة عبور 80.5 كم، أي 50 ميلًا قانونيًا، الحد الأمريكي الأقدم للفضاء. الهواء الكثيف صار خلفك.',
         'Questo segno è l’attraversamento di 80,5 km, 50 miglia statutarie, il vecchio limite USA dello spazio. L’aria spessa è alle spalle.'),
  'u': T('Staging sheds dead mass. The second-stage nozzle is larger because p_0 in ṁ v_e + (p_e − p_0) A_e is nearly zero in vacuum.',
         'L’étage largue la masse morte. La tuyère du second étage est plus grande car p_0 dans ṁ v_e + (p_e − p_0) A_e est presque nul dans le vide.',
         'La etapa suelta masa muerta. La tobera de la segunda etapa es mayor porque p_0 en ṁ v_e + (p_e − p_0) A_e es casi cero en el vacío.',
         'فصل المرحلة يلقي الكتلة الميتة. فوهة المرحلة الثانية أكبر لأن p_0 في ṁ v_e + (p_e − p_0) A_e شبه صفر في الفراغ.',
         'Lo stadio lascia la massa morta. L’ugello del secondo stadio è più grande perché p_0 in ṁ v_e + (p_e − p_0) A_e è quasi zero nel vuoto.'),
 },
 'burn2': {
  'k': T('The top engine is still firing. It is turning the last of the climb into sideways speed.',
         'Le moteur du haut brûle encore. Il transforme la fin de la montée en vitesse de côté.',
         'El motor de arriba sigue encendido. Convierte el final de la subida en velocidad de lado.',
         'محرك الأعلى ما زال يعمل. يحوّل آخر الصعود إلى سرعة جانبية.',
         'Il motore in alto è ancora acceso. Trasforma la fine della salita in velocità laterale.'),
  's': T('Above 100 km the fairing is gone. The second stage’s larger nozzle is built for vacuum, where outside pressure is nearly zero.',
         'Au-dessus de 100 km la coiffe est partie. La plus grande tuyère du second étage est faite pour le vide, où la pression extérieure est presque nulle.',
         'Por encima de 100 km la cofia ya no está. La tobera mayor de la segunda etapa está hecha para el vacío, donde la presión exterior es casi cero.',
         'فوق 100 كم زال الغطاء. فوهة المرحلة الثانية الأكبر مصممة للفراغ حيث الضغط الخارجي شبه صفر.',
         'Oltre i 100 km l’ogiva non c’è più. L’ugello più grande del secondo stadio è fatto per il vuoto, dove la pressione esterna è quasi zero.'),
  'u': T('Vacuum bells run a higher expansion ratio so exit pressure stays near the outside pressure. Over-expanding that far at sea level would separate the flow inside the nozzle.',
         'Les tuyères à vide ont un plus grand rapport de détente pour que la pression de sortie reste proche de l’extérieur. Trop détendre au sol séparerait l’écoulement dans la tuyère.',
         'Las toberas de vacío usan una razón de expansión mayor para que la presión de salida se acerque a la exterior. Sobreexpandir así al nivel del mar separaría el flujo dentro de la tobera.',
         'فوهات الفراغ بنسبة تمدد أعلى حتى يبقى ضغط الخروج قريبًا من الخارج. التمدد الزائد هكذا عند سطح البحر يفصل الجريان داخل الفوهة.',
         'Gli ugelli da vuoto usano un rapporto di espansione più alto così la pressione di uscita resta vicina a quella esterna. Sovraespandere così al livello del mare separerebbe il flusso dentro l’ugello.'),
 },
 'fairing': {
  'k': T('The cover over the satellite comes off. Almost all of the air is already below you.',
         'La coiffe au-dessus du satellite s’ouvre. Presque tout l’air est déjà en dessous.',
         'La cubierta del satélite se abre. Casi todo el aire ya está debajo.',
         'غطاء القمر الصناعي ينفصل. كل الهواء تقريبًا صار تحتك.',
         'La copertura del satellite si apre. Quasi tutta l’aria è già sotto di te.'),
  's': T('100 km is the Kármán line used by the Fédération Aéronautique Internationale. NASA’s thermosphere chart already began near 80 km.',
         '100 km est la ligne de Kármán de la Fédération aéronautique internationale. Le schéma NASA de la thermosphère commençait déjà vers 80 km.',
         '100 km es la línea de Kármán de la Fédération Aéronautique Internationale. El esquema de la NASA de la termosfera ya empezaba cerca de 80 km.',
         '100 كم هو خط كارمان لدى الاتحاد الدولي للطيران. مخطط ناسا للغلاف الحراري يبدأ قرب 80 كم.',
         '100 km è la linea di Kármán della Fédération Aéronautique Internationale. Lo schema NASA della termosfera iniziava già verso gli 80 km.'),
  'u': T('Fairings are dropped once dynamic pressure can no longer damage the payload. This marker is simply the model crossing 100 km.',
         'On largue la coiffe quand la pression dynamique ne peut plus abîmer la charge. Ce repère est juste le modèle qui passe 100 km.',
         'La cofia se suelta cuando la presión dinámica ya no puede dañar la carga. Esta marca es solo el modelo al cruzar 100 km.',
         'يُرمى الغطاء عندما لا يعود الضغط الديناميكي قادرًا على إيذاء الحمولة. هذه العلامة مجرد عبور النموذج 100 كم.',
         'L’ogiva si sgancia quando la pressione dinamica non può più danneggiare il carico. Questo segno è solo il modello che passa i 100 km.'),
 },
 'seco': {
  'k': T('The last engine stops. At about 7.7 km every second sideways, you keep missing Earth. You are in orbit.',
         'Le dernier moteur s’arrête. À environ 7,7 km par seconde de côté, tu rates la Terre sans cesse. Tu es en orbite.',
         'El último motor se apaga. A unos 7,7 km por segundo de lado, sigues fallando la Tierra. Estás en órbita.',
         'يتوقف المحرك الأخير. عند نحو 7.7 كم في كل ثانية جانبيًا، تظل تفوّت الأرض. أنت في المدار.',
         'L’ultimo motore si spegne. A circa 7,7 km al secondo di lato, continui a mancare la Terra. Sei in orbita.'),
  's': T('A circle at 400 km needs 7.67 km/s. The station still flies in the thermosphere, so thin air slowly drags it and crews reboost it.',
         'Un cercle à 400 km demande 7,67 km/s. La station vole encore dans la thermosphère : l’air ténu la freine et les équipages la remontent.',
         'Un círculo a 400 km necesita 7,67 km/s. La estación sigue en la termosfera: el aire tenue la frena y las tripulaciones la elevan.',
         'الدائرة عند 400 كم تحتاج 7.67 كم/ث. المحطة ما زالت في الغلاف الحراري، فالهواء الرقيق يسحبها والطاقم يرفعها.',
         'Un cerchio a 400 km richiede 7,67 km/s. La stazione vola ancora nella termosfera: l’aria rada la frena e gli equipaggi la rialzano.'),
  'u': T('v = √(μ/r) at r = 6 778 km. MECO or SECO is this cutoff. Without the sideways speed, the same altitude is only a fall.',
         'v = √(μ/r) à r = 6 778 km. MECO ou SECO est cette extinction. Sans la vitesse latérale, la même altitude n’est qu’une chute.',
         'v = √(μ/r) con r = 6 778 km. MECO o SECO es ese apagado. Sin la velocidad lateral, la misma altitud es solo una caída.',
         'v = √(μ/r) عند r = 6778 كم. MECO أو SECO هو هذا الإيقاف. بلا السرعة الجانبية، الارتفاع نفسه مجرد سقوط.',
         'v = √(μ/r) a r = 6 778 km. MECO o SECO è questo spegnimento. Senza la velocità laterale, la stessa quota è solo una caduta.'),
 },
}
LAY = [
 ('tropo', T('Troposphere, surface to about 12 km', 'Troposphère, du sol à environ 12 km', 'Troposfera, del suelo a unos 12 km', 'التروبوسفير، من السطح إلى نحو 12 كم', 'Troposfera, dal suolo a circa 12 km'),
  T('NASA’s average top is about 12 km (lower at the poles, higher at the equator). The 1976 standard sets its first break, the tropopause, at 11 km geopotential. Weather lives here. The model’s max-Q is in this layer.',
     'La NASA place le sommet moyen vers 12 km (plus bas aux pôles, plus haut à l’équateur). La norme 1976 met sa première limite, la tropopause, à 11 km géopotentiel. La météo est ici. Le max-Q du modèle est dans cette couche.',
     'La NASA pone el tope medio cerca de 12 km (más bajo en los polos, más alto en el ecuador). La norma 1976 pone su primer corte, la tropopausa, a 11 km geopotenciales. Aquí está el tiempo. El max-Q del modelo cae en esta capa.',
     'تضع ناسا متوسط القمة قرب 12 كم (أدنى عند القطبين وأعلى عند الاستواء). معيار 1976 يضع أول حد، التروبوبوز، عند 11 كم من الارتفاع الجهدي. الطقس هنا. أقصى ضغط في النموذج يقع في هذه الطبقة.',
     'La NASA mette la cima media verso i 12 km (più bassa ai poli, più alta all’equatore). Lo standard 1976 mette il primo stacco, la tropopausa, a 11 km geopotenziali. Qui sta il meteo. Il max-Q del modello è in questo strato.')),
 ('strato', T('Stratosphere, about 12 km to 50 km', 'Stratosphère, d’environ 12 km à 50 km', 'Estratosfera, de unos 12 km a 50 km', 'الستراتوسفير، من نحو 12 كم إلى 50 كم', 'Stratosfera, da circa 12 km a 50 km'),
  T('Home of the ozone layer. In the 1976 model the temperature stops falling, then rises, through the breaks at 20, 32 and 47 km.',
     'Là se trouve la couche d’ozone. Dans le modèle 1976 la température cesse de baisser, puis remonte, aux coupures de 20, 32 et 47 km.',
     'Ahí está la capa de ozono. En el modelo de 1976 la temperatura deja de bajar y luego sube, en los cortes de 20, 32 y 47 km.',
     'هنا طبقة الأوزون. في نموذج 1976 تتوقف الحرارة عن الهبوط ثم ترتفع، عند حدود 20 و32 و47 كم.',
     'Qui sta l’ozono. Nel modello 1976 la temperatura smette di scendere e poi sale, agli stacchi di 20, 32 e 47 km.')),
 ('meso', T('Mesosphere, about 50 km to 80 km', 'Mésosphère, d’environ 50 km à 80 km', 'Mesosfera, de unos 50 km a 80 km', 'الميزوسفير، من نحو 50 كم إلى 80 كم', 'Mesosfera, da circa 50 km a 80 km'),
  T('NASA’s cold layer, up to about 80–85 km. Most meteors burn up here. The 1976 model continues to 86 km.',
     'La couche froide de la NASA, jusqu’à environ 80–85 km. La plupart des météores y brûlent. Le modèle 1976 continue jusqu’à 86 km.',
     'La capa fría de la NASA, hasta unos 80–85 km. La mayoría de los meteoros se queman aquí. El modelo de 1976 sigue hasta 86 km.',
     'الطبقة الباردة لدى ناسا، حتى نحو 80–85 كم. معظم الشهب تحترق هنا. نموذج 1976 يتابع حتى 86 كم.',
     'Lo strato freddo della NASA, fino a circa 80–85 km. La maggior parte delle meteore brucia qui. Il modello 1976 arriva a 86 km.')),
 ('thermo', T('Thermosphere, about 80 km to 600 or 700 km', 'Thermosphère, d’environ 80 km à 600 ou 700 km', 'Termosfera, de unos 80 km a 600 o 700 km', 'الثرموسفير، من نحو 80 كم إلى 600 أو 700 كم', 'Termosfera, da circa 80 km a 600 o 700 km'),
  T('NASA puts auroras and the space station here. 400 km is still this layer. The Kármán line, 100 km, and the United States 50-mile line, 80.5 km, both sit near its bottom. The air is thin enough to look black and thick enough to drag a station.',
     'La NASA y place les aurores et la station. 400 km est encore cette couche. La ligne de Kármán, 100 km, et la limite américaine de 50 milles, 80,5 km, sont près de sa base. L’air est assez mince pour paraître noir, et assez présent pour freiner une station.',
     'La NASA pone aquí las auroras y la estación. 400 km sigue en esta capa. La línea de Kármán, 100 km, y el límite estadounidense de 50 millas, 80,5 km, están cerca de su base. El aire es tan fino que se ve negro, y aún frena una estación.',
     'تضع ناسا هنا الشفق والمحطة. 400 كم ما زالت في هذه الطبقة. خط كارمان 100 كم والحد الأمريكي 50 ميلًا أي 80.5 كم يقعان قرب أسفلها. الهواء رقيق حتى يبدو أسود، وكافٍ ليسحب محطة.',
     'La NASA mette qui le aurore e la stazione. 400 km è ancora questo strato. La linea di Kármán, 100 km, e il limite USA di 50 miglia, 80,5 km, stanno vicino alla base. L’aria è così rada da sembrare nera, e abbastanza presente da frenare una stazione.')),
 ('exo', T('Exosphere, about 700 km to 10 000 km', 'Exosphère, d’environ 700 km à 10 000 km', 'Exosfera, de unos 700 km a 10 000 km', 'الإكسوسفير، من نحو 700 كم إلى 10000 كم', 'Esosfera, da circa 700 km a 10 000 km'),
  T('NASA’s outer edge, where the few remaining molecules can escape to space. Most navigation and many communications satellites fly here, not the station.',
     'Le bord externe selon la NASA, où les rares molécules peuvent s’échapper. La plupart des satellites de navigation et beaucoup de télécoms volent ici, pas la station.',
     'El borde exterior según la NASA, donde las pocas moléculas que quedan pueden escapar. La mayoría de los satélites de navegación y muchos de comunicaciones vuelan aquí, no la estación.',
     'الحافة الخارجية لدى ناسا، حيث يمكن للجزيئات القليلة المتبقية أن تهرب إلى الفضاء. معظم أقمار الملاحة وكثير من أقمار الاتصال تطير هنا، لا المحطة.',
     'Il bordo esterno secondo la NASA, dove le poche molecole rimaste possono fuggire. La maggior parte dei satelliti di navigazione e molti di comunicazione volano qui, non la stazione.')),
]
CSS = ('.ascent{margin:0 0 1.6rem}.ascent-c{width:100%;height:auto;aspect-ratio:16/9;background:#05070d;border-radius:16px;display:block}'
       '.ascent-sky{height:14px;border-radius:999px;margin:.45rem 0;border:1px solid rgba(255,255,255,.35)}'
       '.ascent-read{font-weight:800;min-height:2.6em}.ascent-cap{font-size:1.05rem}'
       '.ascent-row{display:flex;flex-wrap:wrap;gap:.45rem;margin:.4rem 0}'
       '.ascent-row button,#ascent-play{min-height:44px;padding:.35rem .8rem;border-radius:999px;font:inherit;font-weight:700;cursor:pointer;background:transparent;color:inherit;border:1px solid rgba(255,255,255,.5)}'
       '.ascent-row button[aria-pressed=true]{background:#ffd54a;color:#1a1300}'
       '.ascent-scrub{display:flex;flex-direction:column;gap:.2rem;font-weight:700}'
       '.ascent-scrub input{width:100%;min-height:44px}'
       '.ascent-layers{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:.7rem;padding:0;margin:0}'
       '.ascent-layers div{padding:.7rem .8rem;border-radius:12px;background:rgba(255,255,255,.05);border-inline-start:4px solid #8fd3ff}'
       '.ascent-layers strong{display:block;margin-bottom:.2rem}'
       '.ytf{display:flex;align-items:center;justify-content:center;gap:.7rem;width:min(100%,40rem);min-height:44px;aspect-ratio:16/9;border-radius:16px;border:1px solid rgba(255,213,74,.75);background:#07101f;color:#f4f7fb;font:inherit;font-weight:800;cursor:pointer;padding:1rem;text-align:start}'
       '.ytf-play{width:0;height:0;border-style:solid;border-width:10px 0 10px 16px;border-color:transparent transparent transparent #ffd54a;flex:none}'
       '.oc-frame{width:min(100%,40rem);aspect-ratio:16/9;border:0;border-radius:16px;display:block}'
       '.ascent-vid{margin:.8rem 0}.ascent-vid figcaption{font-size:.92rem}'
       '.ascent button:focus-visible,.ascent input:focus-visible,.ytf:focus-visible{outline:3px solid #ffd54a;outline-offset:2px}'
       '@media (forced-colors:active){.ascent-row button,.ytf{border:1px solid ButtonText}}'
       '@media (prefers-reduced-motion:reduce){.ascent-c{scroll-behavior:auto}}')

def ui_for(l):
    ui = {k: UI_KEYS[k][l] for k in UI_KEYS}
    ui['caps'] = {sid: {lv: CAPS[sid][lv][l] for lv in ('k', 's', 'u')} for sid in CAPS}
    return ui

def block(l):
    pre = '' if l == 'en' else '../'
    e = lambda s: html.escape(s, quote=True)
    ui = e(json.dumps(ui_for(l), ensure_ascii=False))
    levels = ''.join(
        f'<button type="button" data-lv="{k}" aria-pressed="{"true" if k=="k" else "false"}">{e(UI_KEYS[{"k":"kids","s":"school","u":"uni"}[k]][l])}</button>'
        for k in ('k', 's', 'u'))
    stages = ''.join(f'<button type="button" data-stage="{sid}">{e(ST_LAB[sid][l])}</button>' for sid in ('liftoff', 'maxq', 'sep', 'fairing', 'turn', 'burn2', 'seco'))
    layers = ''.join(f'<div><strong>{e(title[l])}</strong>{e(body[l])}</div>' for _, title, body in LAY)
    vids = (
        f'<figure class="ascent-vid"><button type="button" class="ytf" data-yt="aWCCNYJV3Zw" data-title="Slow Motion Liftoff of NASA\'s Artemis I Moon Rocket">'
        f'<span class="ytf-play" aria-hidden="true"></span><span>{e(T("Play: NASA Kennedy slow-motion liftoff of Artemis I","Lire : décollage au ralenti d’Artemis I, NASA Kennedy","Reproducir: despegue a cámara lenta de Artemis I, NASA Kennedy","تشغيل: إقلاع أرتميس 1 بالحركة البطيئة، ناسا كينيدي","Riproduci: decollo al rallentatore di Artemis I, NASA Kennedy")[l])}</span></button>'
        f'<figcaption>{e(T("NASA’s Kennedy Space Center channel. Slow-motion liftoff of Artemis I, 16 November 2022. The rocket leaves the pad going up.","Chaîne du Kennedy Space Center de la NASA. Décollage au ralenti d’Artemis I, 16 novembre 2022. La fusée quitte le pas de tir vers le haut.","Canal del Centro Espacial Kennedy de la NASA. Despegue a cámara lenta de Artemis I, 16 de noviembre de 2022. El cohete deja la rampa hacia arriba.","قناة مركز كينيدي الفضائي لناسا. إقلاع أرتميس 1 بالحركة البطيئة في 16 نوفمبر 2022. الصاروخ يغادر المنصة إلى الأعلى.","Canale del Kennedy Space Center della NASA. Decollo al rallentatore di Artemis I, 16 novembre 2022. Il razzo lascia la rampa verso l’alto.")[l])} <a href="https://www.youtube.com/watch?v=aWCCNYJV3Zw">YouTube</a>.</figcaption></figure>'
        f'<figure class="ascent-vid"><button type="button" class="ytf" data-yt="FSyfFrMcuQI" data-title="Artemis I Launching to the Moon: Official NASA Launch Trailer">'
        f'<span class="ytf-play" aria-hidden="true"></span><span>{e(T("Play: NASA trailer, pitching downrange","Lire : bande-annonce NASA, inclinaison vers l’aval","Reproducir: tráiler de la NASA, inclinación a favor del vuelo","تشغيل: إعلان ناسا، الميل مع اتجاه الطيران","Riproduci: trailer NASA, beccheggio in rotta")[l])}</span></button>'
        f'<figcaption>{e(T("NASA’s official Artemis I trailer. After liftoff, the call is that the vehicle is pitching downrange: the gravity turn has begun.","Bande-annonce officielle NASA d’Artemis I. Après le décollage, l’appel dit que le véhicule s’incline vers l’aval : le virage gravitationnel a commencé.","Tráiler oficial de la NASA de Artemis I. Tras el despegue, la llamada dice que el vehículo se inclina a favor del vuelo: el giro por gravedad ha empezado.","الإعلان الرسمي لناسا عن أرتميس 1. بعد الإقلاع يُقال إن المركبة تميل مع اتجاه الطيران: بدأ انعطاف الجاذبية.","Trailer ufficiale NASA di Artemis I. Dopo il decollo, la chiamata dice che il veicolo beccheggia in rotta: il gravity turn è iniziato.")[l])} <a href="https://www.youtube.com/watch?v=FSyfFrMcuQI">YouTube</a>.</figcaption></figure>'
    )
    ns = (f'<noscript><p>{e(S["lead"][l])}</p><picture><source type="image/webp" srcset="{pre}assets/earth/blue-marble-1280.webp 1280w, {pre}assets/earth/blue-marble-1920.webp 1920w, {pre}assets/earth/blue-marble-4096.webp 4096w" sizes="(min-width:900px) 720px, 100vw">'
          f'<img src="{pre}assets/earth/blue-marble-1280.webp" width="1920" height="960" alt="{e(T("NASA Blue Marble photograph of Earth","Photographie Blue Marble de la Terre par la NASA","Fotografía Blue Marble de la Tierra de la NASA","صورة ناسا Blue Marble للأرض","Fotografia Blue Marble della Terra della NASA")[l])}" loading="lazy" decoding="async"></picture></noscript>')
    return (f'<section class="ascent" id="ascent" aria-labelledby="ascent-h"><h2 id="ascent-h">{e(S["h"][l])}</h2>'
            f'<p>{e(S["lead"][l])}</p><p>{e(S["model"][l])}</p>'
            f'<div id="ascent-app" data-ui="{ui}">'
            f'<div class="ascent-row" role="group" aria-label="{e(UI_KEYS["levels"][l])}">{levels}</div>'
            f'<canvas class="ascent-c" id="ascent-c" width="1280" height="720" role="img" aria-label="{e(S["h"][l])}"></canvas>'
            f'<div class="ascent-sky" id="ascent-sky" aria-hidden="true"></div>'
            f'<p class="ascent-read" id="ascent-read" role="status" aria-live="polite"></p>'
            f'<label class="ascent-scrub">{e(UI_KEYS["scrub"][l])}<input id="ascent-scrub" type="range" min="0" max="1000" step="1" value="0"></label>'
            f'<div class="ascent-row" role="group" aria-label="{e(UI_KEYS["stages"][l])}">{stages}</div>'
            f'<p><button type="button" id="ascent-play">{e(UI_KEYS["play"][l])}</button></p>'
            f'<p class="ascent-cap" id="ascent-cap"></p></div>'
            f'<h3>{e(S["layers"][l])}</h3><div class="ascent-layers">{layers}</div>'
            f'<p>{e(S["scale"][l])}</p><p>{e(S["stagewhy"][l])}</p>{vids}'
            f'<p class="lnote">{e(S["credit"][l])} <a href="https://visibleearth.nasa.gov/images/73909/december-blue-marble-next-generation-w-topography-and-bathymetry">NASA Visible Earth 73909</a>. '
            f'<a href="https://science.nasa.gov/earth/earth-atmosphere/earths-atmosphere-a-multi-layered-cake/">NASA Science</a>. '
            f'<a href="https://www.nasa.gov/image-article/earths-atmospheric-layers-3/">NASA layers</a>. '
            f'<a href="https://www.grc.nasa.gov/www/k-12/airplane/rockth.html">NASA Glenn thrust</a>.</p>{ns}</section>'
            f'<h2>{e(S["stay"][l])}</h2>')

def async_css(tag_href):
    return (f'<link rel="preload" as="style" href="{tag_href}" onload="this.onload=null;this.rel=\'stylesheet\'">'
            f'<noscript class="crit-ns"><link rel="stylesheet" href="{tag_href}"></noscript>')

def patch(path, l):
    s = open(path, encoding='utf-8').read()
    blk = block(l)
    if 'id="ascent"' in s:
        s = re.sub(r'<section class="ascent" id="ascent".*?</section>\s*<h2>.*?</h2>', blk, s, count=1, flags=re.S)
    else:
        s = s.replace('<div class="lw"><div id="ol"', '<div class="lw">' + blk + '<div id="ol"', 1)
    if '.ascent-c{' not in s:
        i = s.find('.lw{max-width')
        j = s.find('</style>', i)
        s = s[:j] + CSS + s[j:]
    pre = '' if l == 'en' else '../'
    old = f'<script src="{pre}assets/orbit-lab.js?v=20261016P" defer></script>'
    new = (f'<script src="{pre}assets/earth-globe.js?v=20261118b" defer></script>'
           f'<script src="{pre}assets/orbit-ascent.js?v=20261118b" defer></script>'
           f'<script src="{pre}assets/orbit-lab.js?v=20261118b" defer></script>')
    if 'earth-globe.js' not in s:
        if old not in s:
            raise SystemExit('script tag missing ' + path)
        s = s.replace(old, new, 1)
    for href in (f'{pre}assets/share-bar.css?v=20261113d', f'{pre}footer-v2.css?v=20261103a'):
        raw = f'<link rel="stylesheet" href="{href}">'
        if raw in s:
            s = s.replace(raw, async_css(href))
    open(path, 'w', encoding='utf-8').write(s)
    print('patched', path)

if __name__ == '__main__':
    for l in LANGS:
        patch('Orbit_Lab.html' if l == 'en' else f'{l}/Orbit_Lab.html', l)
