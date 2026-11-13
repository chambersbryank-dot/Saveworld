import json
p = 'scripts/voyage-copy.json'
d = json.load(open(p, encoding='utf-8'))

def row(name, status, dest, dist, arrival, sentences, credit, **k):
    langs = ['en', 'fr', 'es', 'ar', 'it', 'he']
    out = {}
    fields = dict(name=name, status=status, destLabel=dest, distLabel=dist, arrival=arrival, sentences=sentences, credit=credit, **k)
    for i, lang in enumerate(langs):
        out[lang] = {}
        for key, val in fields.items():
            if not val:
                continue
            out[lang][key] = val[i]
    return out

d['juno'] = row(
 ['Juno']*6,
 ['Orbiting Jupiter. NASA’s page says Juno arrived in 2016.','En orbite autour de Jupiter. La page de la NASA dit que Juno est arrivée en 2016.','En órbita alrededor de Júpiter. La página de la NASA dice que Juno llegó en 2016.','في مدار حول المشتري. تقول صفحة ناسا إن جونو وصلت في 2016.','In orbita attorno a Giove. La pagina NASA dice che Juno è arrivata nel 2016.','מקיפה את צדק. עמוד נאס״א אומר שג׳ונו הגיעה ב-2016.'],
 ['Jupiter']*6,
 ['Distance from Jupiter:','Distance depuis Jupiter :','Distancia desde Júpiter:','المسافة من المشتري:','Distanza da Giove:','מרחק מצדק:'],
 ['There is no future arrival date. The spacecraft is already at Jupiter.','Il n’y a pas de date d’arrivée à venir. L’engin est déjà à Jupiter.','No hay una llegada futura. La nave ya está en Júpiter.','لا يوجد تاريخ وصول قادم. المركبة عند المشتري بالفعل.','Non c’è un arrivo futuro. Il veicolo è già a Giove.','אין תאריך הגעה עתידי. החללית כבר בצדק.'],
 [
  ['Since it arrived at Jupiter in 2016, NASA says Juno has been looking beneath the clouds.','It is the first orbiter to look so closely.','The picture of the spacecraft is an artist’s concept, not a photograph.'],
  ['Depuis son arrivée à Jupiter en 2016, la NASA dit que Juno observe sous les nuages.','C’est le premier orbiteur à regarder d’aussi près.','L’image de l’engin est une vue d’artiste, pas une photo.'],
  ['Desde que llegó a Júpiter en 2016, la NASA dice que Juno mira bajo las nubes.','Es el primer orbitador que mira tan de cerca.','La imagen de la nave es un concepto artístico, no una foto.'],
  ['منذ وصولها إلى المشتري في 2016، تقول ناسا إن جونو تنظر تحت السحب.','إنها أول مركبة مدارية تنظر عن هذا القرب.','صورة المركبة مفهوم فني، وليست صورة فوتوغرافية.'],
  ['Da quando è arrivata a Giove nel 2016, la NASA dice che Juno guarda sotto le nubi.','È il primo orbiter a guardare così da vicino.','L’immagine del veicolo è un concetto artistico, non una foto.'],
  ['מאז שהגיעה לצדק ב-2016, נאס״א אומרת שג׳ונו מביטה מתחת לעננים.','זו המקיפה הראשונה שמסתכלת מקרוב כל כך.','תמונת החללית היא המחשה אמנותית, לא צילום.'],
 ],
 ['Jupiter globe: NASA/JPL/Space Science Institute, Cassini cylindrical map (PIA07782). Spacecraft: NASA artist’s concept of Juno at Jupiter (PIA13746). Earth: NASA Visible Earth / Blue Marble.']*6,
 craftLabel=['Juno']*6, craftAlt=['Artist’s concept of Juno at Jupiter']*6, destAlt=['Jupiter from the Cassini map']*6,
)
d['psyche'] = row(
 ['Psyche']*6,
 ['En route to the metal-rich asteroid Psyche.','En route vers l’astéroïde riche en métal Psyché.','En camino al asteroide rico en metal Psyche.','في الطريق إلى الكويكب الغني بالمعدن سايكي.','In viaggio verso l’asteroide ricco di metallo Psyche.','בדרך אל האסטרואיד העשיר במתכת פסיכה.'],
 ['Asteroid Psyche']*6,
 ['', '', '', '', '', ''],
 ['NASA says the prime mission begins in August 2029. Horizons has no range from the asteroid itself after 13 October 2023, so only the distance from Earth is shown.','La NASA dit que la mission principale commence en août 2029. Horizons n’a pas de distance depuis l’astéroïde après le 13 octobre 2023, donc seule la distance depuis la Terre est affichée.','La NASA dice que la misión principal empieza en agosto de 2029. Horizons no tiene distancia desde el asteroide después del 13 de octubre de 2023, así que solo se muestra la distancia desde la Tierra.','تقول ناسا إن المهمة الأساسية تبدأ في أغسطس 2029. لا يملك Horizons مسافة من الكويكب نفسه بعد 13 أكتوبر 2023، لذلك تُعرض المسافة من الأرض فقط.','La NASA dice che la missione principale inizia nell’agosto 2029. Horizons non ha una distanza dall’asteroide dopo il 13 ottobre 2023, quindi è mostrata solo la distanza dalla Terra.','נאס״א אומרת שהמשימה העיקרית מתחילה באוגוסט 2029. ל-Horizons אין טווח מהאסטרואיד עצמו אחרי 13 באוקטובר 2023, ולכן מוצג רק המרחק מכדור הארץ.'],
 [
  ['NASA says Psyche is on its way to begin exploring the asteroid by August 2029.','Scientists think the asteroid has a high metal content and may be part of the core of an early planetesimal.','The prime mission is about two years in orbit, to map the surface and measure what it is made of.','The round picture is an artist’s concept, not a photograph of the asteroid.'],
  ['La NASA dit que Psyché est en route pour commencer l’étude de l’astéroïde d’ici août 2029.','Les scientifiques pensent que l’astéroïde est très riche en métal et pourrait être un morceau du noyau d’un planétésimal.','La mission principale dure environ deux ans en orbite, pour cartographier la surface et sa composition.','L’image ronde est une vue d’artiste, pas une photo de l’astéroïde.'],
  ['La NASA dice que Psyche va en camino para empezar a explorar el asteroide en agosto de 2029.','Los científicos creen que el asteroide tiene mucho metal y puede ser parte del núcleo de un planetesimal.','La misión principal dura unos dos años en órbita, para cartografiar la superficie y su composición.','La imagen redonda es un concepto artístico, no una foto del asteroide.'],
  ['تقول ناسا إن سايكي في الطريق لتبدأ استكشاف الكويكب بحلول أغسطس 2029.','يعتقد العلماء أن الكويكب غني بالمعدن وقد يكون جزءًا من نواة كوكب أولي.','المهمة الأساسية نحو عامين في المدار، لرسم السطح ومعرفة تركيبه.','الصورة الدائرية مفهوم فني، وليست صورة للكويكب.'],
  ['La NASA dice che Psyche è in viaggio per iniziare a esplorare l’asteroide entro agosto 2029.','Gli scienziati pensano che l’asteroide sia ricco di metallo e possa essere parte del nucleo di un planetesimo.','La missione principale dura circa due anni in orbita, per mappare la superficie e la composizione.','L’immagine rotonda è un concetto artistico, non una foto dell’asteroide.'],
  ['נאס״א אומרת שפסיכה בדרך כדי להתחיל לחקור את האסטרואיד עד אוגוסט 2029.','מדענים חושבים שהאסטרואיד עשיר במתכת ואולי הוא חלק מליבה של כוכב לכת קדום.','המשימה העיקרית היא כשנתיים במסלול, כדי למפות את פני השטח ואת ההרכב.','התמונה העגולה היא המחשה אמנותית, לא צילום של האסטרואיד.'],
 ],
 ['Asteroid: NASA artist’s concept. Earth: NASA Visible Earth / Blue Marble.']*6,
 destAlt=['Artist’s concept of the metal-rich asteroid Psyche']*6,
)
d['lucy'] = row(
 ['Lucy']*6,
 ['En route to Jupiter’s Trojan asteroids.','En route vers les astéroïdes troyens de Jupiter.','En camino a los asteroides troyanos de Júpiter.','في الطريق إلى كويكبات طروادة حول المشتري.','In viaggio verso gli asteroidi troiani di Giove.','בדרך אל אסטרואידי הטרויאנים של צדק.'],
 ['Jupiter’s Trojan asteroids','Astéroïdes troyens de Jupiter','Asteroides troyanos de Júpiter','كويكبات طروادة حول المشتري','Asteroidi troiani di Giove','אסטרואידי הטרויאנים של צדק'],
 ['']*6,
 ['NASA lists the next flyby as 11 August 2027. The page does not name that target, so no distance to one asteroid is shown.','La NASA indique le prochain survol le 11 août 2027. La page ne nomme pas cette cible, donc aucune distance vers un seul astéroïde n’est affichée.','La NASA indica el próximo sobrevuelo el 11 de agosto de 2027. La página no nombra ese objetivo, así que no se muestra una distancia a un solo asteroide.','تذكر ناسا التحليق التالي في 11 أغسطس 2027. الصفحة لا تسمّي ذلك الهدف، لذلك لا تُعرض مسافة إلى كويكب واحد.','La NASA indica il prossimo sorvolo l’11 agosto 2027. La pagina non nomina quel bersaglio, quindi non è mostrata una distanza verso un solo asteroide.','נאס״א מציינת את המעבר הבא ב-11 באוגוסט 2027. העמוד לא נוקב בשם היעד, ולכן לא מוצג מרחק לאסטרואיד אחד.'],
 [
  ['Lucy is the first mission to explore Jupiter’s Trojan asteroids.','NASA says it will fly by 11 asteroids: three in the main belt and eight Trojans.','It launched on 16 October 2021.','The spacecraft picture is a hangar photo, with the edges faded into the page.'],
  ['Lucy est la première mission vers les astéroïdes troyens de Jupiter.','La NASA dit qu’elle survolera 11 astéroïdes : trois dans la ceinture principale et huit troyens.','Lancement le 16 octobre 2021.','La photo de l’engin a été prise dans un hangar ; les bords sont fondus dans la page.'],
  ['Lucy es la primera misión a los asteroides troyanos de Júpiter.','La NASA dice que sobrevolará 11 asteroides: tres del cinturón principal y ocho troyanos.','Lanzamiento el 16 de octubre de 2021.','La foto de la nave es de un hangar; los bordes se funden con la página.'],
  ['لوسي أول مهمة لاستكشاف كويكبات طروادة حول المشتري.','تقول ناسا إنها ستحلّق قرب 11 كويكبًا: ثلاثة في الحزام الرئيسي وثمانية طروادية.','الإطلاق في 16 أكتوبر 2021.','صورة المركبة من حظيرة، وحوافها ممزوجة بالصفحة.'],
  ['Lucy è la prima missione verso gli asteroidi troiani di Giove.','La NASA dice che sorvolerà 11 asteroidi: tre nella fascia principale e otto troiani.','Lancio il 16 ottobre 2021.','La foto del veicolo è di un hangar; i bordi sfumano nella pagina.'],
  ['לוסי היא המשימה הראשונה אל אסטרואידי הטרויאנים של צדק.','נאס״א אומרת שהיא תחלוף ליד 11 אסטרואידים: שלושה בחגורה הראשית ושמונה טרויאנים.','השיגור היה ב-16 באוקטובר 2021.','תמונת החללית צולמה בהאנגר, והקצוות נמסים אל תוך העמוד.'],
 ],
 ['Spacecraft: NASA/Ben Smegelsky, Kennedy Space Center. Earth: NASA Visible Earth / Blue Marble. No single Trojan portrait is shown, because the mission has many targets.']*6,
 craftLabel=['Lucy']*6, craftAlt=['Lucy spacecraft in a hangar at Kennedy Space Center']*6,
)
d['bepicolombo'] = row(
 ['BepiColombo']*6,
 ['En route to Mercury. Not in orbit yet.','En route vers Mercure. Pas encore en orbite.','En camino a Mercurio. Aún no está en órbita.','في الطريق إلى عطارد. ليست في المدار بعد.','In viaggio verso Mercurio. Non è ancora in orbita.','בדרך אל כוכב חמה. עדיין לא במסלול.'],
 ['Mercury','Mercure','Mercurio','عطارد','Mercurio','כוכב חמה'],
 ['Distance from Mercury:','Distance depuis Mercure :','Distancia desde Mercurio:','المسافة من عطارد:','Distanza da Mercurio:','מרחק מכוכב חמה:'],
 ['ESA’s page, checked 13 November 2026, says BepiColombo is in operation and en route, with arrival at Mercury in December 2026. Routine science is listed for April 2027.','La page de l’ESA, consultée le 13 novembre 2026, dit que BepiColombo est en opération et en route, avec une arrivée à Mercure en décembre 2026. La science de routine est indiquée pour avril 2027.','La página de la ESA, revisada el 13 de noviembre de 2026, dice que BepiColombo está en operación y en camino, con llegada a Mercurio en diciembre de 2026. La ciencia rutinaria figura en abril de 2027.','صفحة وكالة الفضاء الأوروبية، التي رُوجعت في 13 نوفمبر 2026، تقول إن بيبي كولومبو تعمل وفي الطريق، والوصول إلى عطارد في ديسمبر 2026. العلم الروتيني مذكور في أبريل 2027.','La pagina dell’ESA, controllata il 13 novembre 2026, dice che BepiColombo è operativa e in viaggio, con arrivo a Mercurio nel dicembre 2026. La scienza di routine è indicata per aprile 2027.','עמוד סוכנות החלל האירופית, שנבדק ב-13 בנובמבר 2026, אומר ש-BepiColombo פועלת ובדרך, עם הגעה לכוכב חמה בדצמבר 2026. המדע השוטף מצוין לאפריל 2027.'],
 [
  ['BepiColombo is an ESA and JAXA mission to Mercury.','On 3 September 2026 the Mercury Transfer Module separated. ESA calls that the first major step of the arrival.','The round picture is a MESSENGER view of Mercury’s surface, not a full-planet globe.'],
  ['BepiColombo est une mission de l’ESA et de la JAXA vers Mercure.','Le 3 septembre 2026, le module de transfert s’est séparé. L’ESA appelle cela la première grande étape de l’arrivée.','L’image ronde est une vue MESSENGER de la surface de Mercure, pas un globe entier.'],
  ['BepiColombo es una misión de la ESA y la JAXA a Mercurio.','El 3 de septiembre de 2026 se separó el módulo de transferencia. La ESA lo llama el primer gran paso de la llegada.','La imagen redonda es una vista de MESSENGER de la superficie de Mercurio, no un globo completo.'],
  ['بيبي كولومبو مهمة لوكالة الفضاء الأوروبية وجاكسا إلى عطارد.','في 3 سبتمبر 2026 انفصل نموذج النقل. تسمّي الوكالة ذلك أول خطوة كبيرة في الوصول.','الصورة الدائرية منظر من مسنجر لسطح عطارد، وليست كرة كاملة للكوكب.'],
  ['BepiColombo è una missione ESA e JAXA verso Mercurio.','Il 3 settembre 2026 il modulo di trasferimento si è separato. L’ESA lo chiama il primo grande passo dell’arrivo.','L’immagine rotonda è una vista MESSENGER della superficie di Mercurio, non un globo intero.'],
  ['BepiColombo היא משימה של סוכנות החלל האירופית ושל ג׳אקסה אל כוכב חמה.','ב-3 בספטמבר 2026 נפרד מודול ההעברה. הסוכנות קוראת לזה הצעד הגדול הראשון של ההגעה.','התמונה העגולה היא מראה של MESSENGER מפני השטח של כוכב חמה, לא גלובוס שלם.'],
 ],
 ['Mercury: NASA/JHUAPL/Carnegie Institution, MESSENGER. Earth: NASA Visible Earth / Blue Marble.']*6,
 destAlt=['MESSENGER view of Mercury’s surface']*6,
)
d['hera'] = row(
 ['Hera']*6,
 ['Arrived at Didymos and Dimorphos.','Arrivée à Didymos et Dimorphos.','Llegó a Didymos y Dimorphos.','وصلت إلى ديديموس وديمورفوس.','Arrivata a Didymos e Dimorphos.','הגיעה אל דידימוס ודימורפוס.'],
 ['Didymos and Dimorphos','Didymos et Dimorphos','Didymos y Dimorphos','ديديموس وديمورفوس','Didymos e Dimorphos','דידימוס ודימורפוס'],
 ['Distance from Didymos:','Distance depuis Didymos :','Distancia desde Didymos:','المسافة من ديديموس:','Distanza da Didymos:','מרחק מדידימוס:'],
 ['ESA lists the rendezvous in November 2026 and says Hera has arrived. It is in the early characterisation phase, about 25 to 30 km from the pair. Horizons gives the live range.','L’ESA indique le rendez-vous en novembre 2026 et dit qu’Hera est arrivée. Elle est en phase de caractérisation précoce, à environ 25 à 30 km de la paire. Horizons donne la distance du jour.','La ESA indica el encuentro en noviembre de 2026 y dice que Hera ya llegó. Está en la fase de caracterización temprana, a unos 25 a 30 km del par. Horizons da la distancia del día.','تذكر وكالة الفضاء الأوروبية الموعد في نوفمبر 2026 وتقول إن هيرا وصلت. هي في مرحلة التوصيف المبكر، على بعد نحو 25 إلى 30 كم من الزوج. يعطي Horizons المسافة الحية.','L’ESA indica il rendez-vous nel novembre 2026 e dice che Hera è arrivata. È nella fase di caratterizzazione iniziale, a circa 25–30 km dalla coppia. Horizons dà la distanza del giorno.','סוכנות החלל האירופית מציינת את המפגש בנובמבר 2026 ואומרת שהרה הגיעה. היא בשלב האפיון המוקדם, בערך 25 עד 30 ק״מ מהזוג. Horizons נותן את הטווח החי.'],
 [
  ['Hera is ESA’s planetary-defence mission to the asteroid that NASA’s DART hit.','ESA describes Didymos as about 780 m across and Dimorphos as about 151 m across.','The picture is an artist’s concept of Hera at the asteroid, not the photo taken from 56 km.'],
  ['Hera est la mission de défense planétaire de l’ESA vers l’astéroïde percuté par DART de la NASA.','L’ESA décrit Didymos d’environ 780 m et Dimorphos d’environ 151 m.','L’image est une vue d’artiste d’Hera près de l’astéroïde, pas la photo prise à 56 km.'],
  ['Hera es la misión de defensa planetaria de la ESA al asteroide que golpeó DART de la NASA.','La ESA describe Didymos de unos 780 m y Dimorphos de unos 151 m.','La imagen es un concepto artístico de Hera junto al asteroide, no la foto tomada a 56 km.'],
  ['هيرا مهمة الدفاع الكوكبي لوكالة الفضاء الأوروبية إلى الكويكب الذي ضربته دارت التابعة لناسا.','تصف الوكالة ديديموس بنحو 780 م وديمورفوس بنحو 151 م.','الصورة مفهوم فني لهيرا عند الكويكب، وليست الصورة الملتقطة من 56 كم.'],
  ['Hera è la missione di difesa planetaria dell’ESA verso l’asteroide colpito da DART della NASA.','L’ESA descrive Didymos di circa 780 m e Dimorphos di circa 151 m.','L’immagine è un concetto artistico di Hera presso l’asteroide, non la foto scattata da 56 km.'],
  ['הרה היא משימת ההגנה הפלנטרית של סוכנות החלל האירופית אל האסטרואיד ש-DART של נאס״א פגעה בו.','הסוכנות מתארת את דידימוס כרוחב של כ-780 מ׳ ואת דימורפוס כרוחב של כ-151 מ׳.','התמונה היא המחשה אמנותית של הרה ליד האסטרואיד, לא הצילום מ-56 ק״מ.'],
 ],
 ['Scene: ESA artist’s concept of Hera at Didymos. Earth: NASA Visible Earth / Blue Marble.']*6,
 destAlt=['Artist’s concept of Hera at the Didymos asteroid']*6,
)
d['parker-solar-probe'] = row(
 ['Parker Solar Probe']*6,
 ['Orbiting the Sun. Primary mission in progress.','En orbite autour du Soleil. Mission principale en cours.','En órbita alrededor del Sol. Misión principal en curso.','في مدار حول الشمس. المهمة الأساسية جارية.','In orbita attorno al Sole. Missione principale in corso.','מקיפה את השמש. המשימה העיקרית נמשכת.'],
 ['The Sun','Le Soleil','El Sol','الشمس','Il Sole','השמש'],
 ['Distance from the Sun:','Distance depuis le Soleil :','Distancia desde el Sol:','المسافة من الشمس:','Distanza dal Sole:','מרחק מהשמש:'],
 ['There is no arrival date. Parker keeps orbiting closer to the Sun than any earlier probe.','Il n’y a pas de date d’arrivée. Parker continue d’orbiter plus près du Soleil qu’aucune sonde avant elle.','No hay fecha de llegada. Parker sigue orbitando más cerca del Sol que cualquier sonda anterior.','لا يوجد تاريخ وصول. تواصل باركر الدوران أقرب إلى الشمس من أي مسبار سابق.','Non c’è una data di arrivo. Parker continua a orbitare più vicino al Sole di qualsiasi sonda precedente.','אין תאריך הגעה. פארקר ממשיכה להקיף קרוב לשמש יותר מכל גשושית קודמת.'],
 [
  ['NASA says Parker launched on 12 August 2018.','It flies inside the orbit of Mercury and faces intense heat and radiation.','The Sun picture is a NASA Solar Dynamics Observatory image, with the black sky removed so the glow fades into the page.'],
  ['La NASA dit que Parker a été lancée le 12 août 2018.','Elle vole à l’intérieur de l’orbite de Mercure et affronte une chaleur et un rayonnement intenses.','L’image du Soleil vient du Solar Dynamics Observatory de la NASA ; le ciel noir a été retiré pour que la lueur se fonde dans la page.'],
  ['La NASA dice que Parker se lanzó el 12 de agosto de 2018.','Vuela dentro de la órbita de Mercurio y enfrenta calor y radiación intensos.','La imagen del Sol es del Solar Dynamics Observatory de la NASA; el cielo negro se quitó para que el brillo se funda con la página.'],
  ['تقول ناسا إن باركر أُطلقت في 12 أغسطس 2018.','تطير داخل مدار عطارد وتواجه حرارة وإشعاعًا شديدين.','صورة الشمس من مرصد ديناميكا الشمس التابع لناسا، وأُزيلت السماء السوداء حتى يذوب التوهج في الصفحة.'],
  ['La NASA dice che Parker è stata lanciata il 12 agosto 2018.','Vola dentro l’orbita di Mercurio e affronta calore e radiazione intensi.','L’immagine del Sole è del Solar Dynamics Observatory della NASA; il cielo nero è stato tolto così il bagliore sfuma nella pagina.'],
  ['נאס״א אומרת שפארקר שוגרה ב-12 באוגוסט 2018.','היא טסה בתוך מסלול כוכב חמה ופוגשת חום וקרינה עזים.','תמונת השמש היא ממצפה הדינמיקה הסולארית של נאס״א; השמיים השחורים הוסרו כדי שהזוהר יימס אל העמוד.'],
 ],
 ['Sun: NASA/SDO AIA 304. Earth: NASA Visible Earth / Blue Marble.']*6,
 destAlt=['The Sun, NASA Solar Dynamics Observatory']*6,
)
d['solar-orbiter'] = row(
 ['Solar Orbiter']*6,
 ['Orbiting the Sun. Science operations since November 2021.','En orbite autour du Soleil. Opérations scientifiques depuis novembre 2021.','En órbita alrededor del Sol. Operaciones científicas desde noviembre de 2021.','في مدار حول الشمس. العمليات العلمية منذ نوفمبر 2021.','In orbita attorno al Sole. Operazioni scientifiche dal novembre 2021.','מקיפה את השמש. פעולות מדעיות מאז נובמבר 2021.'],
 ['The Sun','Le Soleil','El Sol','الشمس','Il Sole','השמש'],
 ['Distance from the Sun:','Distance depuis le Soleil :','Distancia desde el Sol:','المسافة من الشمس:','Distanza dal Sole:','מרחק מהשמש:'],
 ['There is no single arrival. ESA lists launch in February 2020.','Il n’y a pas une arrivée unique. L’ESA indique un lancement en février 2020.','No hay una sola llegada. La ESA indica el lanzamiento en febrero de 2020.','لا يوجد وصول واحد. تذكر وكالة الفضاء الأوروبية الإطلاق في فبراير 2020.','Non c’è un singolo arrivo. L’ESA indica il lancio nel febbraio 2020.','אין הגעה אחת. סוכנות החלל האירופית מציינת שיגור בפברואר 2020.'],
 [
  ['Solar Orbiter is led by ESA, with NASA as a partner.','ESA says its tilted orbit made it the first mission to image the Sun’s poles from outside the ecliptic.','The spacecraft photo was taken on the ground, and its edges fade into the page.'],
  ['Solar Orbiter est menée par l’ESA, avec la NASA comme partenaire.','L’ESA dit que son orbite inclinée en a fait la première mission à photographier les pôles du Soleil hors de l’écliptique.','La photo de l’engin a été prise au sol, et ses bords se fondent dans la page.'],
  ['Solar Orbiter la lidera la ESA, con la NASA como socia.','La ESA dice que su órbita inclinada la hizo la primera misión en fotografiar los polos del Sol fuera de la eclíptica.','La foto de la nave se tomó en tierra, y sus bordes se funden con la página.'],
  ['سولار أوربيتر بقيادة وكالة الفضاء الأوروبية، وناسا شريكة.','تقول الوكالة إن مداره المائل جعله أول مهمة تصوّر قطبي الشمس من خارج مسار الكواكب.','صورة المركبة التُقطت على الأرض، وحوافها تذوب في الصفحة.'],
  ['Solar Orbiter è guidata dall’ESA, con la NASA come partner.','L’ESA dice che l’orbita inclinata l’ha resa la prima missione a fotografare i poli del Sole fuori dall’eclittica.','La foto del veicolo è stata scattata a terra, e i bordi sfumano nella pagina.'],
  ['סולאר אורביטר בהובלת סוכנות החלל האירופית, ונאס״א שותפה.','הסוכנות אומרת שהמסלול הנטוי הפך אותה למשימה הראשונה שמצלמת את קטבי השמש מחוץ למישור המילקה.','תמונת החללית צולמה על הקרקע, והקצוות נמסים אל העמוד.'],
 ],
 ['Sun: NASA/SDO AIA 304. Spacecraft: ESA Solar Orbiter on the ground. Earth: NASA Visible Earth / Blue Marble.']*6,
 craftLabel=['Solar Orbiter']*6, destAlt=['The Sun, NASA Solar Dynamics Observatory']*6, craftAlt=['Solar Orbiter spacecraft on the ground']*6,
)
d['new-horizons'] = row(
 ['New Horizons']*6,
 ['In the Kuiper Belt, at the outer edge of the solar system.','Dans la ceinture de Kuiper, au bord extérieur du système solaire.','En el cinturón de Kuiper, en el borde exterior del sistema solar.','في حزام كايبر، عند الحافة الخارجية للنظام الشمسي.','Nella fascia di Kuiper, al bordo esterno del sistema solare.','בחגורת קויפר, בשולי מערכת השמש.'],
 ['Kuiper Belt','Ceinture de Kuiper','Cinturón de Kuiper','حزام كايبر','Fascia di Kuiper','חגורת קויפר'],
 ['Distance from the Sun:','Distance depuis le Soleil :','Distancia desde el Sol:','المسافة من الشمس:','Distanza dal Sole:','מרחק מהשמש:'],
 ['NASA’s page lists the Pluto flyby on 14 July 2015 and does not give another arrival date.','La page de la NASA indique le survol de Pluton le 14 juillet 2015 et ne donne pas une autre date d’arrivée.','La página de la NASA indica el sobrevuelo de Plutón el 14 de julio de 2015 y no da otra fecha de llegada.','تذكر صفحة ناسا تحليق بلوتو في 14 يوليو 2015 ولا تعطي تاريخ وصول آخر.','La pagina NASA indica il sorvolo di Plutone il 14 luglio 2015 e non dà un’altra data di arrivo.','עמוד נאס״א מציין את מעבר פלוטו ב-14 ביולי 2015 ואינו נותן תאריך הגעה נוסף.'],
 [
  ['New Horizons launched on 19 January 2006.','It flew past Pluto and its moons, and NASA now places it at the outer edge of the solar system.','No single portrait of “the destination” is shown, because the spacecraft is traveling through the Kuiper Belt.'],
  ['New Horizons a été lancée le 19 janvier 2006.','Elle a survolé Pluton et ses lunes, et la NASA la place maintenant au bord extérieur du système solaire.','Aucun portrait unique de « la destination » n’est montré, car l’engin traverse la ceinture de Kuiper.'],
  ['New Horizons se lanzó el 19 de enero de 2006.','Sobrevueló Plutón y sus lunas, y la NASA ahora la sitúa en el borde exterior del sistema solar.','No se muestra un solo retrato de «el destino», porque la nave viaja por el cinturón de Kuiper.'],
  ['أُطلقت نيو هورايزنز في 19 يناير 2006.','حلّقت قرب بلوتو وأقماره، وتضعها ناسا الآن عند الحافة الخارجية للنظام الشمسي.','لا تُعرض صورة واحدة لـ«الوجهة»، لأن المركبة تسافر عبر حزام كايبر.'],
  ['New Horizons è stata lanciata il 19 gennaio 2006.','Ha sorvolato Plutone e le sue lune, e la NASA ora la colloca al bordo esterno del sistema solare.','Non è mostrato un solo ritratto della «destinazione», perché il veicolo sta attraversando la fascia di Kuiper.'],
  ['ניו הורייזנס שוגרה ב-19 בינואר 2006.','היא חלפה ליד פלוטו וירחיו, ונאס״א ממקמת אותה עכשיו בשולי מערכת השמש.','אין דיוקן אחד של «היעד», כי החללית נוסעת דרך חגורת קויפר.'],
 ],
 ['Earth: NASA Visible Earth / Blue Marble. Ranges: NASA/JPL Horizons.']*6,
)
d['voyager-1'] = row(
 ['Voyager 1']*6,
 ['In interstellar space.','Dans l’espace interstellaire.','En el espacio interestelar.','في الفضاء بين النجوم.','Nello spazio interstellare.','בחלל הבין-כוכבי.'],
 ['Interstellar space','Espace interstellaire','Espacio interestelar','الفضاء بين النجوم','Spazio interstellare','החלל הבין-כוכבי'],
 ['Distance from the Sun:','Distance depuis le Soleil :','Distancia desde el Sol:','المسافة من الشمس:','Distanza dal Sole:','מרחק מהשמש:'],
 ['NASA says Voyager 1 crossed into interstellar space in August 2012 and is still collecting data. There is no arrival ahead.','La NASA dit que Voyager 1 est entrée dans l’espace interstellaire en août 2012 et collecte encore des données. Il n’y a pas d’arrivée devant elle.','La NASA dice que Voyager 1 cruzó al espacio interestelar en agosto de 2012 y sigue recogiendo datos. No hay una llegada por delante.','تقول ناسا إن فوياجر 1 عبرت إلى الفضاء بين النجوم في أغسطس 2012 وما زالت تجمع البيانات. لا يوجد وصول أمامها.','La NASA dice che Voyager 1 è entrata nello spazio interstellare nell’agosto 2012 e sta ancora raccogliendo dati. Non c’è un arrivo davanti.','נאס״א אומרת שוויאג׳ר 1 חצתה לחלל הבין-כוכבי באוגוסט 2012 ועדיין אוספת נתונים. אין הגעה לפניה.'],
 [
  ['Voyager 1 launched in 1977 to fly by Jupiter and Saturn.','It is now outside the heliosphere, the bubble of the Sun’s particles and magnetic field.','The live distances are the Horizons ranges, not a rounded figure from an older caption.'],
  ['Voyager 1 a été lancée en 1977 pour survoler Jupiter et Saturne.','Elle est maintenant hors de l’héliosphère, la bulle de particules et de champ magnétique du Soleil.','Les distances du jour sont celles de Horizons, pas un chiffre arrondi d’une ancienne légende.'],
  ['Voyager 1 se lanzó en 1977 para sobrevolar Júpiter y Saturno.','Ahora está fuera de la heliosfera, la burbuja de partículas y campo magnético del Sol.','Las distancias del día son las de Horizons, no una cifra redondeada de un pie antiguo.'],
  ['أُطلقت فوياجر 1 في 1977 للتحليق قرب المشتري وزحل.','هي الآن خارج الغلاف الشمسي، فقاعة جسيمات الشمس ومجالها المغناطيسي.','مسافات اليوم هي أرقام Horizons، وليست رقمًا مقربًا من تعليق قديم.'],
  ['Voyager 1 è stata lanciata nel 1977 per sorvolare Giove e Saturno.','Ora è fuori dall’eliosfera, la bolla di particelle e campo magnetico del Sole.','Le distanze del giorno sono quelle di Horizons, non una cifra arrotondata di una vecchia didascalia.'],
  ['וויאג׳ר 1 שוגרה ב-1977 כדי לחלוף ליד צדק ושבתאי.','היא עכשיו מחוץ להליוספירה, בועת החלקיקים והשדה המגנטי של השמש.','המרחקים החיים הם טווחי Horizons, לא מספר מעוגל מכיתוב ישן.'],
 ],
 ['Earth: NASA Visible Earth / Blue Marble. Ranges: NASA/JPL Horizons.']*6,
)
d['voyager-2'] = row(
 ['Voyager 2']*6,
 ['In interstellar space. Extended mission.','Dans l’espace interstellaire. Mission prolongée.','En el espacio interestelar. Misión extendida.','في الفضاء بين النجوم. مهمة ممتدة.','Nello spazio interstellare. Missione estesa.','בחלל הבין-כוכבי. משימה מוארכת.'],
 ['Interstellar space','Espace interstellaire','Espacio interestelar','الفضاء بين النجوم','Spazio interstellare','החלל הבין-כוכבי'],
 ['Distance from the Sun:','Distance depuis le Soleil :','Distancia desde el Sol:','المسافة من الشمس:','Distanza dal Sole:','מרחק מהשמש:'],
 ['NASA says Voyager 2 entered interstellar space on 25 November 2018. There is no arrival ahead.','La NASA dit que Voyager 2 est entrée dans l’espace interstellaire le 25 novembre 2018. Il n’y a pas d’arrivée devant elle.','La NASA dice que Voyager 2 entró en el espacio interestelar el 25 de noviembre de 2018. No hay una llegada por delante.','تقول ناسا إن فوياجر 2 دخلت الفضاء بين النجوم في 25 نوفمبر 2018. لا يوجد وصول أمامها.','La NASA dice che Voyager 2 è entrata nello spazio interstellare il 25 novembre 2018. Non c’è un arrivo davanti.','נאס״א אומרת שוויאג׳ר 2 נכנסה לחלל הבין-כוכבי ב-25 בנובמבר 2018. אין הגעה לפניה.'],
 [
  ['Voyager 2 launched on 20 August 1977.','It is the only spacecraft to fly by Uranus and Neptune, after Jupiter and Saturn.','NASA lists the mission as extended, and the probe is outside the heliosphere.'],
  ['Voyager 2 a été lancée le 20 août 1977.','C’est le seul engin à avoir survolé Uranus et Neptune, après Jupiter et Saturne.','La NASA classe la mission comme prolongée, et la sonde est hors de l’héliosphère.'],
  ['Voyager 2 se lanzó el 20 de agosto de 1977.','Es la única nave que sobrevoló Urano y Neptuno, después de Júpiter y Saturno.','La NASA clasifica la misión como extendida, y la sonda está fuera de la heliosfera.'],
  ['أُطلقت فوياجر 2 في 20 أغسطس 1977.','هي المركبة الوحيدة التي حلّقت قرب أورانوس ونبتون، بعد المشتري وزحل.','تصنّف ناسا المهمة على أنها ممتدة، والمسبار خارج الغلاف الشمسي.'],
  ['Voyager 2 è stata lanciata il 20 agosto 1977.','È l’unico veicolo ad aver sorvolato Urano e Nettuno, dopo Giove e Saturno.','La NASA classifica la missione come estesa, e la sonda è fuori dall’eliosfera.'],
  ['וויאג׳ר 2 שוגרה ב-20 באוגוסט 1977.','היא החללית היחידה שחלפה ליד אורנוס ונפטון, אחרי צדק ושבתאי.','נאס״א מסווגת את המשימה כמורחבת, והגשושית מחוץ להליוספירה.'],
 ],
 ['Earth: NASA Visible Earth / Blue Marble. Ranges: NASA/JPL Horizons.']*6,
)
json.dump(d, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('missions', len(d))
# sanity: every mission has 6 langs and sentences
for mid, langs in d.items():
    assert set(langs)==set('en fr es ar it he'.split()), mid
    for lang, c in langs.items():
        assert c['sentences'] and c['name'] and c['status']
print('copy ok')
