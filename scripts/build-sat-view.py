#!/usr/bin/env python3
"""Earth-centered satellite view data for Space.html. Facts come from each solution page or a named NASA/ESA page."""
import html, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
V = '20261112tt'
LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']

# regime: leo (sun-synchronous counts as LEO), meo, geo, heo, l1, l2, l5, cruise, note
# fn: weather, land, ocean, ice, fire, defense, science, nav
M = [
 dict(id='landsat9', page='Landsat_9.html', fn='land', regime='leo', agency='NASA / USGS', official='https://landsat.gsfc.nasa.gov/', imageQ='Landsat 9', feed='https://www.nasa.gov/feed/'),
 dict(id='s2c', page='Sentinel-2C.html', fn='land', regime='leo', agency='ESA', official='https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2', imageQ='Sentinel-2', imageMust='sentinel'),
 dict(id='nisar', page='NISAR.html', fn='land', regime='leo', agency='NASA / ISRO', official='https://nisar.jpl.nasa.gov/', imageQ='NISAR satellite', feed='https://www.nasa.gov/feed/'),
 dict(id='biomass', page='Biomass.html', fn='land', regime='leo', agency='ESA', official='https://www.esa.int/Applications/Observing_the_Earth/Future_missions/Biomass', imageQ='Biomass satellite ESA', imageMust='biomass'),
 dict(id='alos4', page='ALOS-4.html', fn='land', regime='leo', agency='JAXA', official='https://www.eorc.jaxa.jp/ALOS/en/alos-4/a4_about.htm'),
 dict(id='smap', page='SMAP.html', fn='land', regime='leo', agency='NASA', official='https://smap.jpl.nasa.gov/', imageQ='SMAP satellite', feed='https://www.nasa.gov/feed/'),
 dict(id='pace', page='PACE.html', fn='ocean', regime='leo', agency='NASA', official='https://pace.oceansciences.org/', imageQ='PACE satellite NASA', feed='https://www.nasa.gov/feed/'),
 dict(id='swot', page='SWOT.html', fn='ocean', regime='leo', agency='NASA / CNES', official='https://swot.jpl.nasa.gov/', imageQ='SWOT satellite', feed='https://www.nasa.gov/feed/'),
 dict(id='s6', page='Sentinel-6B.html', fn='ocean', regime='leo', agency='ESA / NASA', official='https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-6', imageQ='Sentinel-6', feed='https://www.nasa.gov/feed/'),
 dict(id='eos06', page='EOS-06.html', fn='ocean', regime='leo', agency='ISRO', official='https://www.isro.gov.in/EOS-06Mission.html'),
 dict(id='s3', page='Sentinel-3.html', fn='ocean', regime='leo', agency='ESA / EUMETSAT', official='https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-3'),
 dict(id='icesat2', page='ICESat-2.html', fn='ice', regime='leo', agency='NASA', official='https://icesat-2.gsfc.nasa.gov/', imageQ='ICESat-2', feed='https://www.nasa.gov/feed/'),
 dict(id='cryosat', page='CryoSat.html', fn='ice', regime='leo', agency='ESA', official='https://www.esa.int/Applications/Observing_the_Earth/Future_missions/CryoSat'),
 dict(id='aws', page='Arctic_Weather_Satellite.html', fn='ice', regime='leo', agency='ESA / EUMETSAT', official='https://www.esa.int/Applications/Observing_the_Earth/Meteorological_missions/Arctic_Weather_Satellite'),
 dict(id='prefire', page='PREFIRE.html', fn='ice', regime='leo', agency='NASA', official='https://prefire.ssec.wisc.edu/', imageQ='PREFIRE NASA', feed='https://www.nasa.gov/feed/'),
 dict(id='goes19', page='GOES-19.html', fn='weather', regime='geo', agency='NOAA', official='https://www.nesdis.noaa.gov/our-satellites/currently-flying/goes-east-west/goes-19', imageQ='GOES-19', feed='https://www.nasa.gov/feed/'),
 dict(id='insat', page='INSAT-3DS.html', fn='weather', regime='geo', agency='ISRO', official='https://www.isro.gov.in/INSAT_3DS.html'),
 dict(id='mtg', page='Meteosat_Third_Generation.html', fn='weather', regime='geo', agency='EUMETSAT / ESA', official='https://www.eumetsat.int/meteosat-third-generation'),
 dict(id='tempo', page='TEMPO.html', fn='weather', regime='geo', agency='NASA', official='https://tempo.si.edu/', imageQ='TEMPO NASA air quality', feed='https://www.nasa.gov/feed/'),
 dict(id='oco2', page='OCO-2.html', fn='weather', regime='leo', agency='NASA', official='https://ocov2.jpl.nasa.gov/', imageQ='OCO-2', feed='https://www.nasa.gov/feed/'),
 dict(id='firesat', page='FireSat.html', fn='fire', regime='leo', agency='Earth Fire Alliance', official='https://www.earthfirealliance.org/'),
 dict(id='neossat', page='NEOSSat.html', fn='defense', regime='leo', agency='Canadian Space Agency', official='https://www.asc-csa.gc.ca/eng/satellites/neossat/'),
 dict(id='galileo', page='Galileo.html', fn='nav', regime='meo', agency='EU / ESA', official='https://www.esa.int/Applications/Satellite_navigation/Galileo'),
 dict(id='hubble', fn='science', regime='leo', agency='NASA / ESA', when='1990', official='https://science.nasa.gov/mission/hubble/', imageQ='Hubble Space Telescope', imageMust='hubble', feed='https://www.nasa.gov/feed/', nasaPlus=True),
 dict(id='chandra', fn='science', regime='heo', agency='NASA', when='1999', official='https://chandra.harvard.edu/', imageQ='Chandra X-ray Observatory', imageMust='chandra', feed='https://www.nasa.gov/feed/'),
 dict(id='tess', fn='science', regime='heo', agency='NASA', when='2018', official='https://science.nasa.gov/mission/tess/', imageQ='TESS exoplanet', imageMust='tess', feed='https://www.nasa.gov/feed/', nasaPlus=True),
 dict(id='webb', page='Webb_2024_YR4.html', fn='science', regime='l2', agency='NASA / ESA / CSA', when='2021', official='https://science.nasa.gov/mission/webb/', imageQ='James Webb Space Telescope', imageMust='webb', feed='https://www.nasa.gov/feed/', dsn=True, nasaPlus=True, photo='assets/sat/webb', credit="Photo: NASA. James Webb Space Telescope primary mirror fully assembled."),
 dict(id='roman', page='Nancy_Grace_Roman.html', fn='science', regime='l2', agency='NASA', when='2026-08-30', official='https://science.nasa.gov/mission/roman-space-telescope/', imageQ='Nancy Grace Roman Space Telescope', imageMust='roman', feed='https://www.nasa.gov/feed/', dsn=True, nasaPlus=True, photo='assets/sat/roman', credit='Photo: NASA. Roman lifts off, 30 August 2026.'),
 dict(id='euclid', fn='science', regime='l2', agency='ESA, with NASA', when='2023-07-01', official='https://www.esa.int/Science_Exploration/Space_Science/Euclid', imageQ='Euclid space telescope', imageMust='euclid', dsn=True, photo='assets/sat/euclid', credit='Photo: NASA/JPL-Caltech (PIA25783). Euclid spacecraft in a clean room.'),
 dict(id='soho', page='SOHO.html', fn='weather', regime='l1', agency='ESA / NASA', when='1995', official='https://science.nasa.gov/mission/soho/', imageQ='SOHO Sun', feed='https://www.nasa.gov/feed/', dsn=True, photo='assets/sat/soho', credit="Artist's concept (NASA), PIA18170."),
 dict(id='aditya', page='Aditya_L1.html', fn='weather', regime='l1', agency='ISRO', official='https://www.isro.gov.in/Aditya_L1.html', dsn=True),
 dict(id='dscovr', page='DSCOVR_EPIC.html', fn='land', regime='l1', agency='NASA / NOAA', official='https://www.nesdis.noaa.gov/current-satellite-missions/currently-flying/dscovr-deep-space-climate-observatory', imageQ='DSCOVR EPIC', feed='https://www.nasa.gov/feed/', dsn=True, photo='assets/sat/dscovr', credit='Photo: NASA. DSCOVR spacecraft at Kennedy Space Center.'),
 dict(id='imap', page='IMAP.html', fn='weather', regime='l1', agency='NASA', official='https://science.nasa.gov/mission/imap/', imageQ='IMAP spacecraft NASA', feed='https://www.nasa.gov/feed/', dsn=True, photo='assets/sat/imap', credit='Photo: NASA. IMAP spacecraft at Kennedy Space Center.'),
 dict(id='neosurveyor', page='NEO_Surveyor.html', fn='defense', regime='l1', agency='NASA', when='NET 2027-09', official='https://science.nasa.gov/mission/neo-surveyor/', imageQ='NEO Surveyor', feed='https://www.nasa.gov/feed/', photo='assets/sat/neo', credit='Photo: NASA (PIA26711). NEO Surveyor spacecraft bus during a test, not the finished observatory.'),
 dict(id='europa', page='Europa_Clipper.html', fn='science', regime='cruise', agency='NASA', official='https://science.nasa.gov/mission/europa-clipper/', imageQ='Europa Clipper', imageMust='europa', feed='https://www.nasa.gov/feed/', dsn=True, nasaPlus=True, photo='assets/sat/europa', credit='Photo: NASA (PIA25125). Europa Clipper during assembly.'),
 dict(id='juice', page='Juice.html', fn='science', regime='cruise', agency='ESA', official='https://www.esa.int/Science_Exploration/Space_Science/Juice', dsn=True, photo='assets/sat/juice', credit='Image: NASA/JPL-Caltech (PIA24026). Juice’s RIME radar.'),
 dict(id='psyche', page='Psyche.html', fn='science', regime='cruise', agency='NASA', official='https://science.nasa.gov/mission/psyche/', imageQ='Psyche spacecraft NASA', imageMust='psyche', feed='https://www.nasa.gov/feed/', dsn=True, photo='assets/sat/psyche', credit='Photo: NASA. Psyche spacecraft at Astrotech.'),
 dict(id='hera', page='Hera.html', fn='defense', regime='cruise', agency='ESA', official='https://www.esa.int/Space_Safety/Hera', dsn=True, photo='assets/sat/hera', credit="Artist's concept (ESA – Science Office, CC BY-SA 3.0 IGO)."),
]

UI = {
 'en': dict(all='All', weather='Weather and climate', land='Land', ocean='Oceans', ice='Ice and polar', fire='Wildfire', defense='Planetary defense', science='Science and discovery', lagrange='Lagrange points', beyond='Beyond Earth',
   rep='Representative place on its orbit type, not a live position.', agency='Agency', orbit='Orbit', does='What it does', helps='How this helps save planets',
   latest='Latest from the NASA image library', latestWait='Looking up the NASA image library…', latestFail='The NASA image library did not return a matching picture. Use the official page instead.',
   follow='Follow', following='Following', close='Close', site='Our page', official='Official mission page', feed='NASA news feed',
   dsn='NASA DSN Now', dsnNote='Live signals at the Deep Space Network. Not a video of the spacecraft.',
   plus='NASA+', plusNote='NASA’s own video service. This page does not embed it.',
   list='Mission list', diagram='Earth with orbit rings', farDiagram='Lagrange points and missions beyond Earth',
   leo='LEO', meo='MEO', geo='GEO', heo='HEO', l1='Sun–Earth L1', l2='Sun–Earth L2', l5='Sun–Earth L5', cruise='On the way',
   title='Earth-protecting satellites',
   lead='Each icon sits on the kind of orbit its mission uses. Low Earth orbit is the inner ring, then medium, geostationary, and a long ellipse for highly elliptical orbits. Distances are not to scale, so every ring stays visible. Nothing here is a live position.',
   scale='The ring order follows NASA Earth Observatory’s Catalog of Earth Satellite Orbits and the Earth-centered style of NASA Eyes on the Earth. Imagery: NASA Visible Earth / Blue Marble Next Generation. Created by the Founder and SI.',
   helpsPage='The sentence above is the mission page on this site. We do not add a broader claim than that page.'),
 'fr': dict(all='Tout', weather='Météo et climat', land='Terres', ocean='Océans', ice='Glace et pôles', fire='Feux de forêt', defense='Défense planétaire', science='Science et découverte', lagrange='Points de Lagrange', beyond='Au-delà de la Terre',
   rep='Place représentative sur ce type d’orbite, pas une position en direct.', agency='Agence', orbit='Orbite', does='Ce qu’il fait', helps='En quoi cela aide à protéger les planètes',
   latest='Dernière image de la bibliothèque NASA', latestWait='Recherche dans la bibliothèque d’images de la NASA…', latestFail='La bibliothèque d’images de la NASA n’a pas renvoyé d’image correspondante. Ouvrez la page officielle.',
   follow='Suivre', following='Suivi', close='Fermer', site='Notre page', official='Page officielle de la mission', feed='Fil d’actualités de la NASA',
   dsn='NASA DSN Now', dsnNote='Signaux en direct du Deep Space Network. Pas une vidéo de l’engin.',
   plus='NASA+', plusNote='Le service vidéo de la NASA. Cette page ne l’intègre pas.',
   list='Liste des missions', diagram='La Terre et les anneaux d’orbite', farDiagram='Points de Lagrange et missions au-delà de la Terre',
   leo='LEO', meo='MEO', geo='GEO', heo='HEO', l1='L1 Soleil–Terre', l2='L2 Soleil–Terre', l5='L5 Soleil–Terre', cruise='En route',
   title='Satellites qui protègent la Terre',
   lead='Chaque icône est placée sur le type d’orbite de sa mission. L’orbite basse est l’anneau intérieur, puis l’orbite moyenne, l’orbite géostationnaire, et une ellipse longue pour les orbites très elliptiques. Les distances ne sont pas à l’échelle. Rien ici n’est une position en direct.',
   scale='L’ordre des anneaux suit le catalogue des orbites terrestres du NASA Earth Observatory et le style centré sur la Terre de NASA Eyes on the Earth. Image : NASA Visible Earth / Blue Marble Next Generation. Créé par le fondateur et SI.',
   helpsPage='La phrase ci-dessus vient de la page de la mission sur ce site. Nous n’ajoutons pas d’autre affirmation.'),
 'es': dict(all='Todo', weather='Tiempo y clima', land='Tierra', ocean='Océanos', ice='Hielo y polos', fire='Incendios', defense='Defensa planetaria', science='Ciencia y descubrimiento', lagrange='Puntos de Lagrange', beyond='Más allá de la Tierra',
   rep='Lugar representativo en ese tipo de órbita, no una posición en vivo.', agency='Agencia', orbit='Órbita', does='Qué hace', helps='Cómo ayuda a cuidar los planetas',
   latest='Última imagen de la biblioteca de la NASA', latestWait='Buscando en la biblioteca de imágenes de la NASA…', latestFail='La biblioteca de imágenes de la NASA no devolvió una imagen que coincida. Abre la página oficial.',
   follow='Seguir', following='Siguiendo', close='Cerrar', site='Nuestra página', official='Página oficial de la misión', feed='Canal de noticias de la NASA',
   dsn='NASA DSN Now', dsnNote='Señales en vivo de la Red del Espacio Profundo. No es un video de la nave.',
   plus='NASA+', plusNote='El servicio de video de la NASA. Esta página no lo incrusta.',
   list='Lista de misiones', diagram='La Tierra con anillos orbitales', farDiagram='Puntos de Lagrange y misiones más allá de la Tierra',
   leo='LEO', meo='MEO', geo='GEO', heo='HEO', l1='L1 Sol–Tierra', l2='L2 Sol–Tierra', l5='L5 Sol–Tierra', cruise='De camino',
   title='Satélites que protegen la Tierra',
   lead='Cada icono está en el tipo de órbita de su misión. La órbita baja es el anillo interior, luego la media, la geoestacionaria y una elipse larga para las órbitas muy elípticas. Las distancias no están a escala. Nada aquí es una posición en vivo.',
   scale='El orden de los anillos sigue el catálogo de órbitas terrestres del NASA Earth Observatory y el estilo centrado en la Tierra de NASA Eyes on the Earth. Imagen: NASA Visible Earth / Blue Marble Next Generation. Creado por el fundador y SI.',
   helpsPage='La frase de arriba es la página de la misión en este sitio. No añadimos una afirmación más amplia.'),
 'ar': dict(all='الكل', weather='الطقس والمناخ', land='اليابسة', ocean='المحيطات', ice='الجليد والقطبان', fire='حرائق الغابات', defense='الدفاع الكوكبي', science='العلم والاكتشاف', lagrange='نقاط لاغرانج', beyond='ما بعد الأرض',
   rep='مكان تمثيلي على نوع المدار، وليس موقعًا مباشرًا.', agency='الوكالة', orbit='المدار', does='ماذا يفعل', helps='كيف يساعد على حماية الكواكب',
   latest='أحدث صورة من مكتبة ناسا', latestWait='جارٍ البحث في مكتبة صور ناسا…', latestFail='لم تُرجع مكتبة صور ناسا صورة مطابقة. افتح الصفحة الرسمية.',
   follow='متابعة', following='تُتابَع', close='إغلاق', site='صفحتنا', official='الصفحة الرسمية للمهمة', feed='تغذية أخبار ناسا',
   dsn='NASA DSN Now', dsnNote='إشارات مباشرة من شبكة الفضاء العميق. ليست فيديو للمركبة.',
   plus='NASA+', plusNote='خدمة فيديو ناسا. هذه الصفحة لا تدمجها.',
   list='قائمة المهام', diagram='الأرض مع حلقات المدارات', farDiagram='نقاط لاغرانج والمهام الأبعد من الأرض',
   leo='LEO', meo='MEO', geo='GEO', heo='HEO', l1='L1 الشمس–الأرض', l2='L2 الشمس–الأرض', l5='L5 الشمس–الأرض', cruise='في الطريق',
   title='أقمار تحمي الأرض',
   lead='كل أيقونة على نوع المدار الذي تستخدمه مهمتها. المدار الأرضي المنخفض هو الحلقة الداخلية، ثم المتوسط، ثم الثابت جغرافيًا، ثم قطع طويل للمدارات شديدة الإهليلجية. المسافات ليست بمقياس حقيقي. لا شيء هنا موقع مباشر.',
   scale='ترتيب الحلقات يتبع فهرس مدارات الأرض لدى NASA Earth Observatory وأسلوب ناسا Eyes on the Earth المتمركز على الأرض. الصورة: NASA Visible Earth / Blue Marble Next Generation. من إعداد المؤسس وSI.',
   helpsPage='الجملة أعلاه من صفحة المهمة على هذا الموقع. لا نضيف ادعاءً أوسع من الصفحة.'),
 'it': dict(all='Tutte', weather='Meteo e clima', land='Terra', ocean='Oceani', ice='Ghiaccio e poli', fire='Incendi', defense='Difesa planetaria', science='Scienza e scoperta', lagrange='Punti di Lagrange', beyond='Oltre la Terra',
   rep='Punto rappresentativo su quel tipo di orbita, non una posizione dal vivo.', agency='Agenzia', orbit='Orbita', does='Cosa fa', helps='Come aiuta a proteggere i pianeti',
   latest='Ultima immagine dalla biblioteca NASA', latestWait='Ricerca nella biblioteca immagini della NASA…', latestFail='La biblioteca immagini della NASA non ha restituito un’immagine corrispondente. Apri la pagina ufficiale.',
   follow='Segui', following='Seguita', close='Chiudi', site='La nostra pagina', official='Pagina ufficiale della missione', feed='Feed di notizie NASA',
   dsn='NASA DSN Now', dsnNote='Segnali in diretta del Deep Space Network. Non è un video della sonda.',
   plus='NASA+', plusNote='Il servizio video della NASA. Questa pagina non lo incorpora.',
   list='Elenco delle missioni', diagram='La Terra con gli anelli orbitali', farDiagram='Punti di Lagrange e missioni oltre la Terra',
   leo='LEO', meo='MEO', geo='GEO', heo='HEO', l1='L1 Sole–Terra', l2='L2 Sole–Terra', l5='L5 Sole–Terra', cruise='In viaggio',
   title='Satelliti che proteggono la Terra',
   lead='Ogni icona sta sul tipo di orbita della missione. L’orbita bassa è l’anello interno, poi la media, la geostazionaria e un’ellisse lunga per le orbite molto ellittiche. Le distanze non sono in scala. Nulla qui è una posizione dal vivo.',
   scale='L’ordine degli anelli segue il catalogo delle orbite terrestri del NASA Earth Observatory e lo stile centrato sulla Terra di NASA Eyes on the Earth. Immagine: NASA Visible Earth / Blue Marble Next Generation. Creato dal fondatore e da SI.',
   helpsPage='La frase sopra viene dalla pagina della missione su questo sito. Non aggiungiamo un’affermazione più ampia.'),
 'he': dict(all='הכל', weather='מזג אוויר ואקלים', land='יבשה', ocean='אוקיינוסים', ice='קרח וקטבים', fire='שריפות יער', defense='הגנה פלנטרית', science='מדע וגילוי', lagrange='נקודות לגראנז׳', beyond='מעבר לכדור הארץ',
   rep='מקום מייצג על סוג המסלול, לא מיקום חי.', agency='סוכנות', orbit='מסלול', does='מה הוא עושה', helps='איך זה עוזר לשמור על כוכבי לכת',
   latest='התמונה האחרונה מספריית התמונות של נאס״א', latestWait='מחפשים בספריית התמונות של נאס״א…', latestFail='ספריית התמונות של נאס״א לא החזירה תמונה מתאימה. פתחו את העמוד הרשמי.',
   follow='מעקב', following='במעקב', close='סגירה', site='העמוד שלנו', official='העמוד הרשמי של המשימה', feed='הזנת החדשות של נאס״א',
   dsn='NASA DSN Now', dsnNote='אותות חיים של רשת החלל העמוק. זה לא סרטון של החללית.',
   plus='NASA+', plusNote='שירות הווידאו של נאס״א. העמוד הזה לא מטמיע אותו.',
   list='רשימת משימות', diagram='כדור הארץ עם טבעות מסלול', farDiagram='נקודות לגראנז׳ ומשימות מעבר לכדור הארץ',
   leo='LEO', meo='MEO', geo='GEO', heo='HEO', l1='L1 שמש–ארץ', l2='L2 שמש–ארץ', l5='L5 שמש–ארץ', cruise='בדרך',
   title='לוויינים שמגנים על כדור הארץ',
   lead='כל סמל יושב על סוג המסלול של המשימה. מסלול נמוך הוא הטבעת הפנימית, אחר כך בינוני, גיאוסטציונרי, ואליפסה ארוכה למסלולים אליפטיים מאוד. המרחקים אינם בקנה מידה. שום דבר כאן אינו מיקום חי.',
   scale='סדר הטבעות עוקב אחרי קטלוג המסלולים של NASA Earth Observatory וסגנון NASA Eyes on the Earth שבמרכזו כדור הארץ. תמונה: NASA Visible Earth / Blue Marble Next Generation. נוצר על ידי המייסד ו-SI.',
   helpsPage='המשפט למעלה הוא מדף המשימה באתר הזה. איננו מוסיפים טענה רחבה יותר.'),
}

# Extra lines only where the site page is not the whole claim. Kept short and tied to a named source.
HELPS = {
 'en': {
  'hubble': ('Hubble Space Telescope', 'NASA lists Hubble as an extended mission in low Earth orbit. A January 2026 Space Telescope Science Institute status said it was operating in reduced-gyro mode.', 'Hubble has measured what some atmospheres of planets around other stars are made of (NASA). That is a comparison, not a watch on Earth.'),
  'chandra': ('Chandra X-ray Observatory', 'NASA’s Chandra X-ray Observatory, run day to day by the Smithsonian, flies a highly elliptical Earth orbit out to about 139,000 km. A Chandra status report on 2 October 2026 said it had completed that week’s observing schedule.', 'Chandra shows exploding stars and hot gas, the violent settings in which planetary systems form. It does not watch Earth’s weather.'),
  'tess': ('TESS', 'NASA’s TESS surveys the sky for planets that pass in front of nearby stars. It flies a high Earth orbit.', 'Finding those planets is the first step before anyone can ask whether they keep an atmosphere. TESS does not monitor Earth.'),
  'euclid': ('Euclid', 'ESA’s Euclid, with NASA contributions, launched on 1 July 2023 to Sun–Earth L2 and is in operation (CNES mission sheet).', 'Euclid maps dark matter and dark energy. It does not study Earth’s air or oceans. It describes the universe planets sit in.'),
  'webb': ('James Webb Space Telescope', 'Webb works at Sun–Earth L2 (NASA). This site’s page is Webb’s February 2026 look at asteroid 2024 YR4.', 'That page says Webb ruled out a 2032 impact on the Moon. NASA also uses Webb to study atmospheres of planets around other stars. It is not an Earth-monitoring satellite.'),
  'roman': ('Nancy Grace Roman Space Telescope', 'NASA launched Roman on 30 August 2026 toward Sun–Earth L2. On 22 October 2026 NASA said it was in science commissioning. The launch announcement said first public images by early 2027.', 'Roman is built for a wide census of planetary systems and a coronagraph that practices photographing planets around other stars. It is not yet in routine science operations.'),
  'europa': ('Europa Clipper', '', 'The mission page says it is on the way to Jupiter’s ocean moon, with an Earth gravity assist on 3 December 2026 and close Europa flybys from 2030. It studies another ocean world, not Earth’s oceans.'),
  'juice': ('Juice', '', 'The mission page says Juice is cruising and will study Ganymede, Callisto and Europa after reaching Jupiter in July 2031. That is comparative planetology, not an Earth forecast.'),
  'psyche': ('Psyche', '', 'The mission page says a Mars flyby on 15 May 2026 sent Psyche toward a metal-rich asteroid it will orbit from August 2029, to learn what a planet’s core can be like.'),
  'hera': ('Hera', '', 'The mission page says Hera arrives at Dimorphos in November 2026 to measure what NASA’s DART impact did. That is a planetary-defense measurement, and the arrival date is the one the page states.'),
 },
}
# Fill other languages with careful translations of the same claims.
HELPS['fr'] = {
 'hubble': ('Télescope spatial Hubble', 'La NASA classe Hubble comme une mission prolongée en orbite basse. Un état de janvier 2026 du Space Telescope Science Institute indiquait qu’il fonctionnait en mode gyro réduit.', 'Hubble a mesuré la composition de certaines atmosphères de planètes autour d’autres étoiles (NASA). C’est une comparaison, pas une surveillance de la Terre.'),
 'chandra': ('Observatoire Chandra', 'Chandra, opéré au jour le jour par le Smithsonian, suit une orbite terrestre très elliptique jusqu’à environ 139 000 km. Un rapport du 2 octobre 2026 disait qu’il avait achevé le programme d’observation de la semaine.', 'Chandra montre les étoiles qui explosent et le gaz chaud, le cadre violent où se forment les systèmes planétaires. Il ne surveille pas la météo terrestre.'),
 'tess': ('TESS', 'TESS de la NASA cherche des planètes qui passent devant des étoiles proches. Il est sur une orbite terrestre haute.', 'Trouver ces planètes est la première étape avant de demander si elles gardent une atmosphère. TESS ne surveille pas la Terre.'),
 'euclid': ('Euclid', 'Euclid de l’ESA, avec la NASA, a été lancé le 1er juillet 2023 vers le point L2 Soleil–Terre et est en opération (fiche CNES).', 'Euclid cartographie la matière noire et l’énergie noire. Il n’étudie ni l’air ni les océans de la Terre.'),
 'webb': ('Télescope spatial James Webb', 'Webb travaille au point L2 Soleil–Terre (NASA). La page du site porte sur son observation de février 2026 de l’astéroïde 2024 YR4.', 'Cette page dit que Webb a écarté un impact sur la Lune en 2032. La NASA utilise aussi Webb pour les atmosphères d’exoplanètes. Ce n’est pas un satellite de surveillance de la Terre.'),
 'roman': ('Télescope spatial Nancy Grace Roman', 'La NASA a lancé Roman le 30 août 2026 vers L2. Le 22 octobre 2026, la NASA disait qu’il était en mise en service scientifique. L’annonce de lancement prévoyait les premières images publiques début 2027.', 'Roman est conçu pour un recensement large des systèmes planétaires et un coronographe qui s’entraîne à photographier des planètes autour d’autres étoiles. Il n’est pas encore en opérations scientifiques de routine.'),
 'europa': ('Europa Clipper', '', 'La page dit qu’il est en route vers la lune océanique de Jupiter, avec une assistance gravitationnelle de la Terre le 3 décembre 2026 et des survols d’Europe à partir de 2030. Il étudie un autre monde océanique, pas les océans terrestres.'),
 'juice': ('Juice', '', 'La page dit que Juice est en croisière et étudiera Ganymède, Callisto et Europe après son arrivée à Jupiter en juillet 2031. C’est de la planétologie comparée, pas une prévision pour la Terre.'),
 'psyche': ('Psyche', '', 'La page dit qu’un survol de Mars le 15 mai 2026 a envoyé Psyche vers un astéroïde riche en métal qu’il orbitera à partir d’août 2029, pour comprendre à quoi peut ressembler le cœur d’une planète.'),
 'hera': ('Hera', '', 'La page dit qu’Hera arrive à Dimorphos en novembre 2026 pour mesurer l’effet de l’impact DART de la NASA. C’est une mesure de défense planétaire, à la date indiquée sur la page.'),
}
HELPS['es'] = {
 'hubble': ('Telescopio espacial Hubble', 'La NASA incluye a Hubble como misión extendida en órbita baja. Un informe de enero de 2026 del Space Telescope Science Institute decía que operaba en modo de giroscopio reducido.', 'Hubble ha medido de qué están hechas algunas atmósferas de planetas alrededor de otras estrellas (NASA). Es una comparación, no una vigilancia de la Tierra.'),
 'chandra': ('Observatorio Chandra', 'Chandra, operado día a día por el Smithsonian, sigue una órbita terrestre muy elíptica hasta unos 139.000 km. Un informe del 2 de octubre de 2026 decía que había completado las observaciones de esa semana.', 'Chandra muestra estrellas que explotan y gas caliente, el entorno violento donde se forman los sistemas planetarios. No vigila el tiempo de la Tierra.'),
 'tess': ('TESS', 'TESS de la NASA busca planetas que pasan delante de estrellas cercanas. Vuela en una órbita terrestre alta.', 'Encontrar esos planetas es el primer paso antes de preguntar si conservan una atmósfera. TESS no vigila la Tierra.'),
 'euclid': ('Euclid', 'Euclid de la ESA, con la NASA, se lanzó el 1 de julio de 2023 hacia L2 Sol–Tierra y está en operación (ficha del CNES).', 'Euclid cartografía la materia oscura y la energía oscura. No estudia el aire ni los océanos de la Tierra.'),
 'webb': ('Telescopio espacial James Webb', 'Webb trabaja en L2 Sol–Tierra (NASA). La página de este sitio es su mirada de febrero de 2026 al asteroide 2024 YR4.', 'Esa página dice que Webb descartó un impacto en la Luna en 2032. La NASA también usa Webb para estudiar atmósferas de exoplanetas. No es un satélite de vigilancia de la Tierra.'),
 'roman': ('Telescopio espacial Nancy Grace Roman', 'La NASA lanzó Roman el 30 de agosto de 2026 hacia L2. El 22 de octubre de 2026 la NASA dijo que estaba en puesta en marcha científica. El anuncio del lanzamiento preveía las primeras imágenes públicas a principios de 2027.', 'Roman está hecho para un censo amplio de sistemas planetarios y un coronógrafo que practica fotografiar planetas alrededor de otras estrellas. Aún no está en operaciones científicas de rutina.'),
 'europa': ('Europa Clipper', '', 'La página dice que va hacia la luna oceánica de Júpiter, con una asistencia gravitatoria de la Tierra el 3 de diciembre de 2026 y sobrevuelos de Europa desde 2030. Estudia otro mundo oceánico, no los océanos de la Tierra.'),
 'juice': ('Juice', '', 'La página dice que Juice está de camino y estudiará Ganímedes, Calisto y Europa tras llegar a Júpiter en julio de 2031. Es planetología comparada, no un pronóstico de la Tierra.'),
 'psyche': ('Psyche', '', 'La página dice que un sobrevuelo de Marte el 15 de mayo de 2026 envió a Psyche hacia un asteroide rico en metal que orbitará desde agosto de 2029, para saber cómo puede ser el núcleo de un planeta.'),
 'hera': ('Hera', '', 'La página dice que Hera llega a Dimorphos en noviembre de 2026 para medir lo que hizo el impacto DART de la NASA. Es una medida de defensa planetaria, en la fecha que dice la página.'),
}
HELPS['ar'] = {
 'hubble': ('تلسكوب هابل الفضائي', 'تدرج ناسا هابل كمهمة ممتدة في مدار أرضي منخفض. قال تقرير يناير 2026 من معهد علوم تلسكوب الفضاء إنه يعمل بوضع الجيروسكوب المخفّض.', 'قاس هابل مكوّنات بعض أغلفة الكواكب حول نجوم أخرى (ناسا). هذه مقارنة، وليست مراقبة للأرض.'),
 'chandra': ('مرصد تشاندرا', 'يطير تشاندرا، وتديره سميثسونيان يوميًا، في مدار أرضي شديد الإهليلجية يصل إلى نحو 139 ألف كم. قال تقرير 2 أكتوبر 2026 إنه أكمل جدول الرصد لذلك الأسبوع.', 'يُظهر تشاندرا النجوم المنفجرة والغاز الحار، وهي البيئات العنيفة التي تتكون فيها الأنظمة الكوكبية. لا يراقب طقس الأرض.'),
 'tess': ('TESS', 'يبحث TESS التابع لناسا عن كواكب تمر أمام نجوم قريبة. وهو في مدار أرضي مرتفع.', 'العثور على تلك الكواكب هو الخطوة الأولى قبل السؤال إن كانت تحتفظ بغلاف جوي. TESS لا يراقب الأرض.'),
 'euclid': ('إقليدس', 'أُطلق إقليدس التابع لوكالة الفضاء الأوروبية، بمساهمة ناسا، في 1 يوليو 2023 نحو L2 وهو قيد التشغيل (بطاقة CNES).', 'يرسم إقليدس المادة المظلمة والطاقة المظلمة. لا يدرس هواء الأرض ولا محيطاتها.'),
 'webb': ('تلسكوب جيمس ويب الفضائي', 'يعمل ويب عند L2 بين الشمس والأرض (ناسا). صفحة هذا الموقع عن نظرته في فبراير 2026 إلى الكويكب 2024 YR4.', 'تقول الصفحة إن ويب استبعد اصطدامًا بالقمر عام 2032. وتستخدم ناسا ويب أيضًا لدراسة أغلفة الكواكب حول نجوم أخرى. ليس قمر مراقبة للأرض.'),
 'roman': ('تلسكوب نانسي غريس رومان الفضائي', 'أطلقت ناسا رومان في 30 أغسطس 2026 نحو L2. في 22 أكتوبر 2026 قالت ناسا إنه في مرحلة التشغيل العلمي. أعلن الإطلاق أن الصور العامة الأولى ستكون أوائل 2027.', 'صُمم رومان لإحصاء واسع للأنظمة الكوكبية ولكوروناغراف يتدرّب على تصوير كواكب حول نجوم أخرى. ليس بعد في تشغيل علمي روتيني.'),
 'europa': ('يوروبا كليبر', '', 'تقول الصفحة إنه في طريقه إلى قمر المشتري المحيطي، مع مساعدة جاذبية الأرض في 3 ديسمبر 2026 وتحليقات قريبة من يوروبا من 2030. يدرس عالمًا محيطيًا آخر، لا محيطات الأرض.'),
 'juice': ('جوس', '', 'تقول الصفحة إن جوس في رحلة وسيدرس غانيميد وكاليستو ويوروبا بعد وصوله إلى المشتري في يوليو 2031. هذا علم كواكب مقارن، لا توقع لطقس الأرض.'),
 'psyche': ('سايكي', '', 'تقول الصفحة إن تحليقًا بالمريخ في 15 مايو 2026 وجّه سايكي إلى كويكب غني بالمعدن سيدور حوله من أغسطس 2029، لمعرفة كيف يمكن أن يكون لب كوكب.'),
 'hera': ('هيرا', '', 'تقول الصفحة إن هيرا تصل إلى ديمورفوس في نوفمبر 2026 لتقيس ما فعله اصطدام DART التابع لناسا. هذا قياس دفاع كوكبي في التاريخ الذي تذكره الصفحة.'),
}
HELPS['it'] = {
 'hubble': ('Telescopio spaziale Hubble', 'La NASA elenca Hubble come missione estesa in orbita bassa. Uno stato di gennaio 2026 dello Space Telescope Science Institute diceva che operava in modalità giroscopio ridotto.', 'Hubble ha misurato di che cosa sono fatte alcune atmosfere di pianeti intorno ad altre stelle (NASA). È un confronto, non un controllo della Terra.'),
 'chandra': ('Osservatorio Chandra', 'Chandra, gestito giorno per giorno dallo Smithsonian, vola su un’orbita terrestre molto ellittica fino a circa 139.000 km. Un rapporto del 2 ottobre 2026 diceva che aveva completato le osservazioni di quella settimana.', 'Chandra mostra stelle che esplodono e gas caldo, gli ambienti violenti in cui nascono i sistemi planetari. Non osserva il meteo della Terra.'),
 'tess': ('TESS', 'TESS della NASA cerca pianeti che passano davanti a stelle vicine. Vola in un’orbita terrestre alta.', 'Trovare quei pianeti è il primo passo prima di chiedere se conservano un’atmosfera. TESS non sorveglia la Terra.'),
 'euclid': ('Euclid', 'Euclid dell’ESA, con la NASA, è stato lanciato il 1° luglio 2023 verso L2 Sole–Terra ed è in operazione (scheda CNES).', 'Euclid mappa la materia oscura e l’energia oscura. Non studia l’aria né gli oceani della Terra.'),
 'webb': ('Telescopio spaziale James Webb', 'Webb lavora al punto L2 Sole–Terra (NASA). La pagina di questo sito riguarda l’osservazione del febbraio 2026 dell’asteroide 2024 YR4.', 'Quella pagina dice che Webb ha escluso un impatto sulla Luna nel 2032. La NASA usa Webb anche per le atmosfere degli esopianeti. Non è un satellite di sorveglianza della Terra.'),
 'roman': ('Telescopio spaziale Nancy Grace Roman', 'La NASA ha lanciato Roman il 30 agosto 2026 verso L2. Il 22 ottobre 2026 la NASA ha detto che era in commissioning scientifico. L’annuncio del lancio prevedeva le prime immagini pubbliche all’inizio del 2027.', 'Roman è fatto per un ampio censimento dei sistemi planetari e un coronografo che si esercita a fotografare pianeti intorno ad altre stelle. Non è ancora in operazioni scientifiche di routine.'),
 'europa': ('Europa Clipper', '', 'La pagina dice che è in viaggio verso la luna oceanica di Giove, con un assist gravitazionale della Terra il 3 dicembre 2026 e sorvoli di Europa dal 2030. Studia un altro mondo oceanico, non gli oceani della Terra.'),
 'juice': ('Juice', '', 'La pagina dice che Juice è in crociera e studierà Ganimede, Callisto ed Europa dopo l’arrivo a Giove nel luglio 2031. È planetologia comparata, non una previsione per la Terra.'),
 'psyche': ('Psyche', '', 'La pagina dice che un sorvolo di Marte il 15 maggio 2026 ha indirizzato Psyche verso un asteroide ricco di metallo che orbiterà dall’agosto 2029, per capire come può essere il nucleo di un pianeta.'),
 'hera': ('Hera', '', 'La pagina dice che Hera arriva a Dimorphos nel novembre 2026 per misurare l’effetto dell’impatto DART della NASA. È una misura di difesa planetaria, nella data indicata dalla pagina.'),
}
HELPS['he'] = {
 'hubble': ('טלסקופ החלל האבל', 'נאס״א מציינת את האבל כמשימה מוארכת במסלול נמוך. דוח מינואר 2026 של המכון המדעי לטלסקופ החלל אמר שהוא פועל במצב ג׳יירו מופחת.', 'האבל מדד ממה עשויות כמה אטמוספרות של כוכבי לכת סביב כוכבים אחרים (נאס״א). זו השוואה, לא מעקב אחרי כדור הארץ.'),
 'chandra': ('מצפה צ׳נדרה', 'צ׳נדרה, שסמיתסוניאן מפעילה יום-יום, טס במסלול ארצי אליפטי מאוד עד כ-139,000 ק״מ. דוח מ-2 באוקטובר 2026 אמר שהשלים את לוח התצפיות של אותו שבוע.', 'צ׳נדרה מראה כוכבים מתפוצצים וגז חם, הסביבה הסוערת שבה נוצרות מערכות פלנטריות. הוא לא עוקב אחרי מזג האוויר של כדור הארץ.'),
 'tess': ('TESS', 'TESS של נאס״א מחפש כוכבי לכת שחולפים לפני כוכבים קרובים. הוא במסלול ארצי גבוה.', 'מציאת כוכבי הלכת האלה היא הצעד הראשון לפני השאלה אם הם שומרים על אטמוספרה. TESS לא מנטר את כדור הארץ.'),
 'euclid': ('אוקלידס', 'אוקלידס של סוכנות החלל האירופית, עם נאס״א, שוגר ב-1 ביולי 2023 אל L2 ופועל (גיליון CNES).', 'אוקלידס ממפה חומר אפל ואנרגיה אפלה. הוא לא חוקר את האוויר או את האוקיינוסים של כדור הארץ.'),
 'webb': ('טלסקופ החלל ג׳יימס וב', 'וב פועל ב-L2 שמש–ארץ (נאס״א). העמוד באתר הזה הוא המבט שלו מפברואר 2026 על האסטרואיד 2024 YR4.', 'העמוד אומר שוב שלל פגיעה בירח ב-2032. נאס״א גם משתמשת בוב לחקר אטמוספרות של כוכבי לכת סביב כוכבים אחרים. זה לא לוויין ניטור של כדור הארץ.'),
 'roman': ('טלסקופ החלל ננסי גרייס רומן', 'נאס״א שיגרה את רומן ב-30 באוגוסט 2026 לעבר L2. ב-22 באוקטובר 2026 נאס״א אמרה שהוא בהרצה מדעית. הודעת השיגור צפתה תמונות ציבוריות ראשונות בתחילת 2027.', 'רומן נבנה לסקר רחב של מערכות פלנטריות ולקורונגרף שמתרגל צילום כוכבי לכת סביב כוכבים אחרים. הוא עדיין לא בהפעלה מדעית שוטפת.'),
 'europa': ('אירופה קליפר', '', 'העמוד אומר שהוא בדרך לירח האוקייני של צדק, עם סיוע כבידתי של כדור הארץ ב-3 בדצמבר 2026 ומעברים קרובים לאירופה מ-2030. הוא חוקר עולם אוקייני אחר, לא את האוקיינוסים של כדור הארץ.'),
 'juice': ('ג׳וס', '', 'העמוד אומר שג׳וס בשיוט ויחקור את גנימד, קליסטו ואירופה אחרי ההגעה לצדק ביולי 2031. זו פלנטולוגיה השוואתית, לא תחזית לכדור הארץ.'),
 'psyche': ('פסיכה', '', 'העמוד אומר שמעבר ליד מאדים ב-15 במאי 2026 כיוון את פסיכה לאסטרואיד עשיר במתכת שהוא יקיף מאוגוסט 2029, כדי ללמוד איך יכול להיראות ליבה של כוכב לכת.'),
 'hera': ('הרא', '', 'העמוד אומר שהרא מגיעה לדימורפוס בנובמבר 2026 כדי למדוד מה עשתה פגיעת DART של נאס״א. זו מדידת הגנה פלנטרית, בתאריך שהעמוד מציין.'),
}

EXPLAIN = {
 'en': dict(
   explainTitle='What is a Lagrange point?',
   explain1='A Lagrange point is a place where the gravity of the Sun and the Earth lines up with the motion of an orbit, so a spacecraft can keep pace with Earth. NASA says the pull of the two large masses equals the centripetal force a small object needs to move with them. There are five. L1, L2, and L3 sit on the Sun–Earth line and are unstable. L4 leads Earth and L5 follows, at the tips of equilateral triangles, and those two are stable.',
   explain2='L1 and L2 are each about 1.5 million kilometers from Earth. NASA’s Webb orbit page rounds that to 1 million miles, which is about 930,000 miles if you convert 1.5 million kilometers directly. L1 faces the Sun, so SOHO and DSCOVR get a steady view of it. L2 is on the night side, a cold and steady spot for telescopes such as Webb, Euclid, and Roman. A spacecraft does not sit on the point. It loops around the point in a halo or Lissajous orbit.',
   explain3='Webb’s trip started with launch on an Ariane 5 on 25 December 2021. NASA says that launch put Webb on a transfer path of about 30 days. Three mid-course correction burns refined the path, and the last one, on 24 January 2022, pointed Webb into its halo orbit. Because L1, L2, and L3 are unstable, Webb fires small station-keeping burns, on average about every 42 days, or it would drift away. L4 and L5 do not need that kind of care. L3 stays hidden behind the Sun, about 1 AU from the Sun and about 2 AU from Earth. L4 and L5 are about 1 AU from Earth, 60 degrees ahead and behind. This drawing is not to scale. NASA’s Moon fact sheet lists a mean distance of 384,400 km (238,855 miles).',
   sources='Sources:',
   dL12='about 1.5 million km · about 1 million miles',
   dL3='about 2 AU from Earth · far side of the Sun',
   dL4='about 1 AU · 60° ahead',
   dL5='about 1 AU · 60° behind',
   l3='L3', l4='L4',
   sunNote='Sun, not to scale', moonNote='Moon, not to scale', notScale='Not to scale',
   viewOrbit='Click here to view the satellite in orbit protecting our planet'),
 'fr': dict(
   explainTitle='Qu’est-ce qu’un point de Lagrange ?',
   explain1='Un point de Lagrange est un endroit où la gravité du Soleil et de la Terre s’accorde avec le mouvement d’une orbite, pour qu’un engin spatial reste au rythme de la Terre. La NASA dit que l’attraction des deux grandes masses égale la force centripète dont un petit objet a besoin pour se déplacer avec elles. Il y en a cinq. L1, L2 et L3 sont sur la ligne Soleil–Terre et sont instables. L4 précède la Terre et L5 la suit, aux sommets de triangles équilatéraux, et ces deux-là sont stables.',
   explain2='L1 et L2 sont chacun à environ 1,5 million de kilomètres de la Terre. La page d’orbite de Webb de la NASA arrondit cela à 1 million de miles, soit environ 930 000 miles si l’on convertit directement 1,5 million de kilomètres. L1 fait face au Soleil : SOHO et DSCOVR y ont une vue stable. L2 est du côté nuit, un endroit froid et stable pour des télescopes comme Webb, Euclid et Roman. Un engin ne se pose pas sur le point. Il tourne autour, sur une orbite halo ou de Lissajous.',
   explain3='Le voyage de Webb a commencé par un lancement Ariane 5 le 25 décembre 2021. La NASA dit que cette fusée l’a placé sur un trajet d’environ 30 jours. Trois corrections de trajectoire ont affiné le chemin, et la dernière, le 24 janvier 2022, a dirigé Webb vers son orbite halo. Comme L1, L2 et L3 sont instables, Webb allume de petites poussées de maintien, en moyenne environ tous les 42 jours, sinon il dériverait. L4 et L5 n’ont pas besoin de ce soin. L3 reste caché derrière le Soleil, à environ 1 UA du Soleil et environ 2 UA de la Terre. L4 et L5 sont à environ 1 UA de la Terre, 60 degrés devant et derrière. Ce dessin n’est pas à l’échelle. La fiche de la Lune de la NASA indique une distance moyenne de 384 400 km (238 855 miles).',
   sources='Sources :',
   dL12='environ 1,5 million de km · environ 1 million de miles',
   dL3='environ 2 UA de la Terre · de l’autre côté du Soleil',
   dL4='environ 1 UA · 60° devant',
   dL5='environ 1 UA · 60° derrière',
   l3='L3', l4='L4',
   sunNote='Soleil, pas à l’échelle', moonNote='Lune, pas à l’échelle', notScale='Pas à l’échelle',
   viewOrbit='Cliquez ici pour voir le satellite en orbite qui protège notre planète'),
 'es': dict(
   explainTitle='¿Qué es un punto de Lagrange?',
   explain1='Un punto de Lagrange es un lugar donde la gravedad del Sol y de la Tierra encaja con el movimiento de una órbita, de modo que una nave puede seguir el ritmo de la Tierra. La NASA dice que la atracción de las dos masas grandes es igual a la fuerza centrípeta que un objeto pequeño necesita para moverse con ellas. Hay cinco. L1, L2 y L3 están en la línea Sol–Tierra y son inestables. L4 va por delante de la Tierra y L5 por detrás, en las puntas de triángulos equiláteros, y esos dos son estables.',
   explain2='L1 y L2 están cada uno a unos 1,5 millones de kilómetros de la Tierra. La página de la órbita de Webb de la NASA redondea eso a 1 millón de millas, unas 930.000 millas si conviertes 1,5 millones de kilómetros directamente. L1 mira al Sol, así que SOHO y DSCOVR tienen una vista estable. L2 está en el lado de noche, un lugar frío y estable para telescopios como Webb, Euclid y Roman. Una nave no se queda sobre el punto. Gira alrededor en una órbita de halo o de Lissajous.',
   explain3='El viaje de Webb empezó con el lanzamiento en un Ariane 5 el 25 de diciembre de 2021. La NASA dice que ese cohete lo puso en un camino de transferencia de unos 30 días. Tres encendidos de corrección afinaron la ruta, y el último, el 24 de enero de 2022, dirigió a Webb a su órbita de halo. Como L1, L2 y L3 son inestables, Webb enciende pequeños empujes de mantenimiento, en promedio cada unos 42 días, o se alejaría. L4 y L5 no necesitan ese cuidado. L3 permanece oculto detrás del Sol, a cerca de 1 UA del Sol y unas 2 UA de la Tierra. L4 y L5 están a cerca de 1 UA de la Tierra, 60 grados por delante y por detrás. Este dibujo no está a escala. La ficha de la Luna de la NASA da una distancia media de 384.400 km (238.855 millas).',
   sources='Fuentes:',
   dL12='unos 1,5 millones de km · cerca de 1 millón de millas',
   dL3='unas 2 UA de la Tierra · al otro lado del Sol',
   dL4='cerca de 1 UA · 60° por delante',
   dL5='cerca de 1 UA · 60° por detrás',
   l3='L3', l4='L4',
   sunNote='Sol, no a escala', moonNote='Luna, no a escala', notScale='No a escala',
   viewOrbit='Haga clic aquí para ver el satélite en órbita protegiendo nuestro planeta'),
 'ar': dict(
   explainTitle='ما هي نقطة لاغرانج؟',
   explain1='نقطة لاغرانج مكان تتوافق فيه جاذبية الشمس والأرض مع حركة المدار، فيستطيع مركبة أن تواكب الأرض. تقول ناسا إن جذب الكتلتين الكبيرتين يساوي القوة المركزية التي يحتاجها جسم صغير ليتحرك معهما. هناك خمس نقاط. تقع L1 وL2 وL3 على خط الشمس–الأرض وهي غير مستقرة. تتقدم L4 الأرض وتتبعها L5، عند رؤوس مثلثين متساويي الأضلاع، وهاتان النقطتان مستقرتان.',
   explain2='تبعد كل من L1 وL2 نحو 1.5 مليون كيلومتر عن الأرض. تقرب صفحة مدار ويب لدى ناسا ذلك إلى مليون ميل، أي نحو 930 ألف ميل إذا حوّلت 1.5 مليون كيلومتر مباشرة. تواجه L1 الشمس، فتحصل SOHO وDSCOVR على رؤية ثابتة لها. تقع L2 في جهة الليل، مكان بارد وثابت لتلسكوبات مثل ويب وإقليدس ورومان. لا تقف المركبة على النقطة. إنها تدور حولها في مدار هالة أو مدار ليساجو.',
   explain3='بدأت رحلة ويب بإطلاق أريان 5 في 25 ديسمبر 2021. تقول ناسا إن الصاروخ وضعه على مسار انتقال لنحو 30 يومًا. عدّلت ثلاث حرقات تصحيح المسار الطريق، ووجّهته الأخيرة في 24 يناير 2022 إلى مدار الهالة. ولأن L1 وL2 وL3 غير مستقرة، يشعل ويب حرقات صغيرة للإبقاء على المدار، في المتوسط كل 42 يومًا تقريبًا، وإلا انجرف بعيدًا. لا تحتاج L4 وL5 إلى هذه العناية. تبقى L3 مخفية خلف الشمس، على بعد نحو 1 وحدة فلكية من الشمس ونحو 2 وحدة فلكية من الأرض. تقع L4 وL5 على بعد نحو 1 وحدة فلكية من الأرض، بزاوية 60 درجة أمامها وخلفها. هذا الرسم ليس بمقياس حقيقي. تذكر ورقة ناسا عن القمر مسافة متوسطة قدرها 384,400 كم (238,855 ميلًا).',
   sources='المصادر:',
   dL12='نحو 1.5 مليون كم · نحو مليون ميل',
   dL3='نحو 2 وحدة فلكية من الأرض · خلف الشمس',
   dL4='نحو 1 وحدة فلكية · 60° أمام الأرض',
   dL5='نحو 1 وحدة فلكية · 60° خلف الأرض',
   l3='L3', l4='L4',
   sunNote='الشمس، ليست بمقياس', moonNote='القمر، ليس بمقياس', notScale='ليس بمقياس حقيقي',
   viewOrbit='انقر هنا لرؤية القمر الصناعي في مداره وهو يحمي كوكبنا'),
 'it': dict(
   explainTitle='Che cos’è un punto di Lagrange?',
   explain1='Un punto di Lagrange è un luogo in cui la gravità del Sole e della Terra si accorda con il moto di un’orbita, così una sonda può tenere il passo della Terra. La NASA dice che l’attrazione delle due grandi masse è uguale alla forza centripeta di cui un oggetto piccolo ha bisogno per muoversi con loro. Ce ne sono cinque. L1, L2 e L3 stanno sulla linea Sole–Terra e sono instabili. L4 precede la Terra e L5 la segue, ai vertici di triangoli equilateri, e quei due sono stabili.',
   explain2='L1 e L2 distano ciascuno circa 1,5 milioni di chilometri dalla Terra. La pagina dell’orbita di Webb della NASA arrotonda a 1 milione di miglia, circa 930.000 miglia se converti direttamente 1,5 milioni di chilometri. L1 guarda il Sole, quindi SOHO e DSCOVR ne hanno una vista stabile. L2 è sul lato notte, un posto freddo e stabile per telescopi come Webb, Euclid e Roman. Una sonda non sta sul punto. Gira intorno al punto in un’orbita halo o di Lissajous.',
   explain3='Il viaggio di Webb è iniziato con il lancio su un Ariane 5 il 25 dicembre 2021. La NASA dice che quel razzo lo ha messo su un trasferimento di circa 30 giorni. Tre accensioni di correzione hanno affinato la rotta, e l’ultima, il 24 gennaio 2022, ha indirizzato Webb nella sua orbita halo. Poiché L1, L2 e L3 sono instabili, Webb accende piccole spinte di mantenimento, in media circa ogni 42 giorni, altrimenti si allontanerebbe. L4 e L5 non hanno bisogno di quella cura. L3 resta nascosto dietro il Sole, a circa 1 UA dal Sole e circa 2 UA dalla Terra. L4 e L5 sono a circa 1 UA dalla Terra, 60 gradi davanti e dietro. Questo disegno non è in scala. La scheda della Luna della NASA indica una distanza media di 384.400 km (238.855 miglia).',
   sources='Fonti:',
   dL12='circa 1,5 milioni di km · circa 1 milione di miglia',
   dL3='circa 2 UA dalla Terra · oltre il Sole',
   dL4='circa 1 UA · 60° davanti',
   dL5='circa 1 UA · 60° dietro',
   l3='L3', l4='L4',
   sunNote='Sole, non in scala', moonNote='Luna, non in scala', notScale='Non in scala',
   viewOrbit='Fai clic qui per vedere il satellite in orbita che protegge il nostro pianeta'),
 'he': dict(
   explainTitle='מהי נקודת לגראנז׳?',
   explain1='נקודת לגראנז׳ היא מקום שבו כוח המשיכה של השמש ושל כדור הארץ מתיישר עם תנועת המסלול, כך שחללית יכולה להישאר בקצב של כדור הארץ. נאס״א אומרת שמשיכת שתי המסות הגדולות שווה לכוח המרכזי שגוף קטן צריך כדי לנוע איתן. יש חמש. L1‏, L2 ו-L3 יושבות על קו השמש–ארץ ואינן יציבות. L4 מובילה את כדור הארץ ו-L5 באה אחריו, בקודקודים של משולשים שווי צלעות, ושתיהן יציבות.',
   explain2='L1 ו-L2 נמצאות כל אחת במרחק של כ-1.5 מיליון קילומטרים מכדור הארץ. עמוד המסלול של וב בנאס״א מעגל זאת למיליון מייל, בערך 930 אלף מייל אם ממירים 1.5 מיליון קילומטרים ישירות. L1 פונה אל השמש, ולכן SOHO ו-DSCOVR רואות אותה באופן יציב. L2 בצד הלילה, מקום קר ויציב לטלסקופים כמו וב, אוקלידס ורומן. חללית לא יושבת על הנקודה. היא מקיפה את הנקודה במסלול הילה או ליסאז׳ו.',
   explain3='המסע של וב התחיל בשיגור על אריאן 5 ב-25 בדצמבר 2021. נאס״א אומרת שהשיגור שם את וב על מסלול מעבר של כ-30 יום. שלוש הצתות תיקון באמצע הדרך דייקו את המסלול, והאחרונה, ב-24 בינואר 2022, כיוונה את וב למסלול ההילה. מכיוון ש-L1‏, L2 ו-L3 אינן יציבות, וב מצית הדלקות קטנות לשמירת מסלול, בממוצע בערך כל 42 יום, אחרת הוא יסחף. L4 ו-L5 לא זקוקות לטיפול כזה. L3 נשארת מוסתרת מאחורי השמש, בערך 1 יחידה אסטרונומית מהשמש וכ-2 יחידות אסטרונומיות מכדור הארץ. L4 ו-L5 במרחק של כ-1 יחידה אסטרונומית מכדור הארץ, 60 מעלות לפניו ואחריו. הציור הזה אינו בקנה מידה. דף העובדות של נאס״א על הירח מציין מרחק ממוצע של 384,400 ק״מ (238,855 מייל).',
   sources='מקורות:',
   dL12='כ-1.5 מיליון ק״מ · כמיליון מייל',
   dL3='כ-2 יח״א מכדור הארץ · מעבר לשמש',
   dL4='כ-1 יח״א · 60° לפני כדור הארץ',
   dL5='כ-1 יח״א · 60° אחרי כדור הארץ',
   l3='L3', l4='L4',
   sunNote='שמש, לא בקנה מידה', moonNote='ירח, לא בקנה מידה', notScale='לא בקנה מידה',
   viewOrbit='לחצו כאן כדי לראות את הלוויין במסלול המגן על כוכב הלכת שלנו'),
}

def meta(lang, page):
    path = page if lang == 'en' else os.path.join(lang, page)
    if not os.path.exists(path):
        path = page
    if not os.path.exists(path):
        return ''
    t = open(path, encoding='utf-8', errors='replace').read()
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    return html.unescape(m.group(1)).strip() if m else ''

def h1(lang, page):
    path = page if lang == 'en' else os.path.join(lang, page)
    if not os.path.exists(path):
        return ''
    t = open(path, encoding='utf-8', errors='replace').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    if not m:
        return ''
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1)))).strip()

LEGEND = ['all', 'weather', 'land', 'ocean', 'ice', 'fire', 'defense', 'science', 'lagrange', 'beyond']

def section(lang, ui):
    pre = '' if lang == 'en' else '../'
    btns = []
    for key in LEGEND:
        pressed = 'true' if key == 'all' else 'false'
        btns.append(f'<button type="button" class="wm-cat" data-cat="{key}" aria-pressed="{pressed}">{html.escape(ui[key])}</button>')
    sources = ('<p class="sat-explain"><span>' + html.escape(ui['sources']) + '</span> '
               '<a href="https://science.nasa.gov/resource/what-is-a-lagrange-point/">NASA, What is a Lagrange Point?</a> · '
               '<a href="https://science.nasa.gov/mission/webb/orbit/">NASA, Webb’s orbit</a> · '
               '<a href="https://science.nasa.gov/blogs/webb/2022/01/24/orbital-insertion-burn-a-success-webb-arrives-at-l2/">NASA, Webb arrives at L2</a> · '
               '<a href="https://www.esa.int/Enabling_Support/Operations/What_are_Lagrange_points">ESA, What are Lagrange points?</a> · '
               '<a href="https://jwst-docs.stsci.edu/jwst-observatory-characteristics/jwst-orbit">STScI, JWST orbit</a> · '
               '<a href="https://ntrs.nasa.gov/citations/20220012121">NASA, 30-day transfer</a></p>')
    return (
      f'<section class="sat-view" id="satmap" data-src="{pre}assets/data/sat-view.{lang}.json?v={V}" data-earth="{pre}assets/earth/blue-marble-disc.webp" data-earth-lg="{pre}assets/earth/blue-marble-disc-lg.webp" data-moon="{pre}assets/earth/moon-disc.webp" aria-labelledby="satmap-title">'
      f'<div class="wm-cats" role="group" aria-label="{html.escape(ui["all"])}">' + ''.join(btns) + '</div>'
      '<div class="sat-layout"><div class="sat-stage" id="sat-stage"></div>'
      '<div class="sat-card" id="sat-card" role="region" aria-labelledby="sat-card-title" hidden></div></div>'
      f'<div class="sat-explain" id="lagrange-explainer"><h3>{html.escape(ui["explainTitle"])}</h3>'
      f'<p>{html.escape(ui["explain1"])}</p><p>{html.escape(ui["explain2"])}</p><p>{html.escape(ui["explain3"])}</p>'
      + sources + '</div>'
      f'<details class="sat-list"><summary>{html.escape(ui["list"])}</summary><ul id="sat-list-ul"></ul></details>'
      f'<p class="sat-scale">{html.escape(ui["scale"])}</p></section>\n'
    )

def main():
    for lang in LANGS:
        ui = dict(UI[lang]); ui.update(EXPLAIN[lang])
        helps = HELPS[lang]
        sats = []
        for m in M:
            extra = helps.get(m['id'])
            name = (extra[0] if extra else '') or h1(lang, m.get('page', '')) or m['id']
            does = meta(lang, m['page']) if m.get('page') else ''
            if extra and extra[1]:
                does = extra[1] if not does else does
            # Prefer the page blurb when it exists; keep the verified status sentence for missions whose page is narrow.
            if extra and m['id'] in ('hubble', 'chandra', 'tess', 'euclid'):
                does = extra[1]
            help_line = extra[2] if extra else ui['helpsPage']
            if extra and m.get('page') and m['id'] not in ('hubble', 'chandra', 'tess', 'euclid'):
                # Page blurb is "what it does"; the extra line is the careful tie.
                does = meta(lang, m['page']) or extra[1]
            row = dict(id=m['id'], fn=m['fn'], regime=m['regime'], name=name, does=does, helps=help_line,
                       orbit=ui.get(m['regime'], m['regime']), agency=m.get('agency', ''), when=m.get('when', ''),
                       page=m.get('page', ''), official=m.get('official', ''), feed=m.get('feed', ''),
                       imageQ=m.get('imageQ', ''), imageMust=(m.get('imageMust') or ''),
                       dsn=bool(m.get('dsn')), nasaPlus=bool(m.get('nasaPlus')),
                       photo=m.get('photo', ''), credit=m.get('credit', ''),
                       source=m.get('official', ''))
            sats.append(row)
        json.dump(dict(lang=lang, ui=ui, sats=sats), open(f'assets/data/sat-view.{lang}.json', 'w', encoding='utf-8'),
                  ensure_ascii=False, separators=(',', ':'))
        path = 'Space.html' if lang == 'en' else f'{lang}/Space.html'
        t = open(path, encoding='utf-8').read()
        t = re.sub(r'<section class="sat-view" id="satmap".*?</section>\n?', lambda _: section(lang, ui), t, count=1, flags=re.S)
        t = re.sub(r'<link rel="stylesheet" href="(?:\.\./)?assets/leaflet/leaflet\.css\?v=1\.9\.4">\n?', '', t)
        t = re.sub(r'<script src="(?:\.\./)?assets/leaflet/leaflet\.js\?v=1\.9\.4" defer></script>', '', t)
        pre = '' if lang == 'en' else '../'
        t = t.replace(f'{pre}map.css?v=20261112sv', f'{pre}map.css?v={V}').replace(f'{pre}map.css?v=20261112orb', f'{pre}map.css?v={V}')
        t = t.replace(f'{pre}assets/sat-view.js?v=20261112sv', f'{pre}assets/sat-view.js?v={V}').replace(f'{pre}assets/sat-view.js?v=20261112orb', f'{pre}assets/sat-view.js?v={V}')
        if 'sat-view.js' not in t:
            t = t.replace('</body>', f'<link rel="stylesheet" href="{pre}map.css?v={V}">\n<script src="{pre}assets/sat-view.js?v={V}" defer></script>\n</body>', 1)
        open(path, 'w', encoding='utf-8').write(t)
        print(lang, 'sats', len(sats), 'satmap', 'id="satmap"' in t)
    # bump world map stylesheet so the shared CSS refreshes
    for lang in LANGS:
        path = 'World_Map.html' if lang == 'en' else f'{lang}/World_Map.html'
        t = open(path, encoding='utf-8').read().replace('map.css?v=20261112sv', f'map.css?v={V}').replace('map.css?v=20261112orb', f'map.css?v={V}').replace('map.js?v=20261112sv', f'map.js?v={V}').replace('map.js?v=20261112orb', f'map.js?v={V}')
        open(path, 'w', encoding='utf-8').write(t)

if __name__ == '__main__':
    main()
