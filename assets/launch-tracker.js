/* Live Launch Tracker (Launch Library 2). Purpose blurbs + Saving Planets connection.
   Data: https://ll.thespacedevs.com (The Space Devs). Free tier; we cache 10 min client-side.
   Do not scrape nextspaceflight.com. No invented facts: purpose from LL2 mission.description;
   connection from published mission type/name vs our solution hubs; else "not yet published". */
(function () {
  var API = 'https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=20&mode=detailed';
  var CACHE_KEY = 'sp-ll2-upcoming';
  var CACHE_MS = 10 * 60 * 1000;
  var nextEl = document.getElementById('lw-next');
  var listEl = document.getElementById('lw-list');
  if (!nextEl || !listEl) return;
  var timer = null;
  var lang = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase();
  var prefix = (location.pathname.indexOf('/' + lang + '/') >= 0) ? '../' : '';

  if (!document.getElementById('lw-blurb-style')) {
    var st = document.createElement('style'); st.id = 'lw-blurb-style';
    st.textContent = '.launch-widget .lw-blurb-note{margin:.55rem 0 .35rem;font-size:.85rem;line-height:1.45;color:rgba(255,255,255,.82)}' +
      '.launch-widget .lw-extra{margin:.35rem 0 0;font-size:.82rem;color:rgba(255,255,255,.72)}' +
      '.launch-widget .lw-blurbs{margin-top:.75rem;display:grid;gap:.55rem}' +
      '.launch-widget .lw-blurb-block{background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:.65rem .8rem}' +
      '.launch-widget .lw-blurb-k{margin:0 0 .25rem;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8fd3ff}' +
      '.launch-widget .lw-blurb-t{margin:0;font-size:.9rem;line-height:1.45;color:rgba(255,255,255,.92)}' +
      '.launch-widget .lw-blurb-src{margin:.35rem 0 0;font-size:.72rem;color:rgba(255,255,255,.55)}' +
      '.launch-widget .lw-blurb-src a{color:#8fd3ff}' +
      '.launch-widget .lw-blurb-link{margin:.45rem 0 0}' +
      '.launch-widget .lw-blurb-link a{color:#8fd3ff;font-weight:700;text-decoration:none}' +
      '.launch-widget .lw-blurb-link a:hover,.launch-widget .lw-blurb-link a:focus{text-decoration:underline}' +
      '.launch-widget .lw-badge{display:inline-block;margin-inline-start:.35rem;padding:.12rem .45rem;border-radius:999px;font-size:.68rem;letter-spacing:.04em;text-transform:none;font-weight:700;vertical-align:middle}' +
      '.launch-widget .lw-yes .lw-badge{background:rgba(0,184,148,.25);color:#7dffd0;border:1px solid rgba(0,184,148,.55)}' +
      '.launch-widget .lw-no .lw-badge{background:rgba(255,209,102,.15);color:#ffd166;border:1px solid rgba(255,209,102,.45)}' +
      '.launch-widget .lw-unk .lw-badge,.launch-widget .lw-skip .lw-badge{background:rgba(255,255,255,.08);color:rgba(255,255,255,.85);border:1px solid rgba(255,255,255,.25)}' +
      '.launch-widget .lw-list li.lw-card{display:block;padding:.85rem 0}' +
      '.launch-widget .lw-card-top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.25rem 1rem}';
    document.head.appendChild(st);
  }

  /* RU/CN/KP/IR-led: listed, never given a solution tie-in (same spirit as map/alerts). */
  var EXCL = /roscosmos|russia|china|chinese|baikonur|plesetsk|vostochny|jiuquan|wenchang|xichang|taiyuan|haiyang|dongfeng|sohae|tonghae|korean committee|nada|korean people.?s|landspace|galactic energy|i-space|orienspace|deep blue aero|space pioneer|cas space|expace|casc|casic|khrunichev|progress rocket|kazakhstan|iran|islamic republic|iranian|ministry of defence of the russian|cnsa|calt/i;

  /* Exact solution pages when the mission name clearly matches a published SP page. */
  var PAGE_MATCH = [
    { re: /\bNISAR\b/i, page: 'NISAR.html', hub: 'Earth_Observation.html', why: 'earth' },
    { re: /\bSWOT\b/i, page: 'SWOT.html', hub: 'Oceans.html', why: 'ocean' },
    { re: /Sentinel-6/i, page: 'Sentinel-6B.html', hub: 'Oceans.html', why: 'ocean' },
    { re: /ICESat-2/i, page: 'ICESat-2.html', hub: 'Polar.html', why: 'polar' },
    { re: /\bBiomass\b/i, page: 'Biomass.html', hub: 'Earth_Observation.html', why: 'earth' },
    { re: /\bPACE\b/i, page: 'PACE.html', hub: 'Oceans.html', why: 'ocean' },
    { re: /\bFLEX\b/i, page: 'FLEX.html', hub: 'Earth_Observation.html', why: 'earth' },
    { re: /\bFORUM\b/i, page: 'FORUM.html', hub: 'Earth_Observation.html', why: 'earth' },
    { re: /\bCHIME\b/i, page: 'CHIME.html', hub: 'Earth_Observation.html', why: 'earth' },
    { re: /\bCRISTAL\b/i, page: 'CRISTAL.html', hub: 'Polar.html', why: 'polar' },
    { re: /\bCIMR\b/i, page: 'CIMR.html', hub: 'Polar.html', why: 'polar' },
    { re: /\bGOES-?19\b|\bGOES-U\b/i, page: 'GOES-19.html', hub: 'Space_Weather.html', why: 'weather' },
    { re: /\bIMAP\b/i, page: 'IMAP.html', hub: 'Space_Weather.html', why: 'weather' },
    { re: /Parker Solar/i, page: 'Parker_Solar_Probe.html', hub: 'Space_Weather.html', why: 'weather' },
    { re: /\bPUNCH\b/i, page: 'PUNCH.html', hub: 'Space_Weather.html', why: 'weather' },
    { re: /NEO Surveyor/i, page: 'NEO_Surveyor.html', hub: 'Planetary_Defense.html', why: 'defense' },
    { re: /\bHera\b/i, page: 'Hera.html', hub: 'Planetary_Defense.html', why: 'defense' },
    { re: /\bDART\b/i, page: 'Planetary_Defense.html', hub: 'Planetary_Defense.html', why: 'defense' },
    { re: /Europa Clipper/i, page: 'Europa_Clipper.html', hub: 'Space_Disposal.html', why: 'space' },
    { re: /\bJuice\b|\bJUICE\b/i, page: 'Juice.html', hub: 'Space_Disposal.html', why: 'space' },
    { re: /\bMMX\b/i, page: 'MMX.html', hub: 'Space_Disposal.html', why: 'space' },
    { re: /FireSat/i, page: 'FireSat.html', hub: 'Deforestation.html', why: 'forest' },
    { re: /ALOS-?4|DAICHI-4/i, page: 'ALOS-4.html', hub: 'Earth_Observation.html', why: 'earth' }
  ];

  var T = {
    en: {
      next: 'Next launch', days: 'Days', hrs: 'Hrs', min: 'Min', sec: 'Sec', window: 'Launch window',
      err: 'Launch data unavailable right now. See the <a href="https://www.nextspaceflight.com/" target="_blank" rel="noreferrer">full launch schedule at Next Spaceflight</a>.',
      unnamed: 'Unnamed mission', unkProv: 'Unknown provider', unkRock: 'Unknown rocket', tbd: 'Date TBD',
      status: 'Status', purpose: 'Mission purpose', conn: 'Saving Planets connection',
      yes: 'Supports a Saving Planets solution', no: 'Does not support a Saving Planets solution',
      unk: 'Connection not yet known', skip: 'Not assessed for our solutions',
      detailsMissing: 'Mission details not yet published.',
      srcLL2: 'Launch Library 2 (The Space Devs)',
      type: 'Type', orbit: 'Orbit', pad: 'Pad',
      moreAgency: 'Operator / agency page',
      why: {
        earth: 'Earth-observation and Earth-science missions supply the land, atmosphere and disaster data our Earth Observation solutions cover.',
        ocean: 'Ocean-observing missions feed sea-level, color and marine monitoring covered by our Ocean solutions.',
        polar: 'Polar and ice-monitoring missions support the cryosphere work on our Polar solutions page.',
        forest: 'Forest and fire-monitoring missions support the work on our Forests solutions page.',
        weather: 'Space-weather and solar missions support forecasting covered on our Space Weather page.',
        defense: 'Planetary-defense missions support asteroid and near-Earth object work on our Planetary Defense page.',
        space: 'This space-science or exploration mission is covered among our Space / Project Rawane solutions.'
      },
      noSpin: {
        communications: 'It is a commercial or government communications mission (for example broadband or relay satellites), not an Earth-observation or planetary-science flight for our solutions.',
        navigation: 'It is a navigation / GNSS mission, not an Earth-observation or planetary-science flight for our solutions.',
        resupply: 'It is a crew or cargo resupply flight, not an Earth-observation or planetary-science flight for our solutions.',
        human: 'It is a human spaceflight mission, not an Earth-observation or planetary-science flight for our solutions.',
        secret: 'Public information is limited (government / classified). That is not enough to claim a Saving Planets connection.',
        other: 'Its published purpose is not Earth observation, planetary science or space weather tied to our solutions.'
      },
      exclNote: 'Saving Planets does not tie launches led by Russia, China, North Korea or Iran to our solutions.',
      seeSolution: 'Open the solution page',
      seeHub: 'See related solutions'
    },
    fr: {
      next: 'Prochain lancement', days: 'Jours', hrs: 'H', min: 'Min', sec: 'S', window: 'Fenêtre de tir',
      err: 'Données de lancement indisponibles pour le moment. Consultez le <a href="https://www.nextspaceflight.com/" target="_blank" rel="noreferrer">calendrier complet des lancements sur Next Spaceflight</a>.',
      unnamed: 'Mission sans nom', unkProv: 'Opérateur inconnu', unkRock: 'Fusée inconnue', tbd: 'Date à confirmer',
      status: 'Statut', purpose: 'Objectif de la mission', conn: 'Lien avec Saving Planets',
      yes: 'Soutient une solution Saving Planets', no: 'Ne soutient pas une solution Saving Planets',
      unk: 'Lien pas encore connu', skip: 'Non évalué pour nos solutions',
      detailsMissing: 'Détails de la mission pas encore publiés.',
      srcLL2: 'Launch Library 2 (The Space Devs)',
      type: 'Type', orbit: 'Orbite', pad: 'Pas de tir',
      moreAgency: 'Page de l’opérateur / agence',
      why: {
        earth: 'Les missions d’observation de la Terre fournissent les données land / atmosphère / catastrophes couvertes par nos solutions Observation de la Terre.',
        ocean: 'Les missions océaniques alimentent le suivi du niveau de la mer et du milieu marin sur nos solutions Océan.',
        polar: 'Les missions polaires et glace soutiennent le travail cryosphère de nos solutions Pôle.',
        forest: 'Les missions forêts et feux soutiennent nos solutions Forêts.',
        weather: 'Les missions météo spatiale soutiennent nos solutions Météo spatiale.',
        defense: 'Les missions de défense planétaire soutiennent nos solutions Défense planétaire.',
        space: 'Cette mission scientifique ou d’exploration figure parmi nos solutions Espace / Projet Rawane.'
      },
      noSpin: {
        communications: 'C’est une mission de télécommunications, pas un vol d’observation de la Terre ou de science planétaire pour nos solutions.',
        navigation: 'C’est une mission de navigation / GNSS, pas un vol d’observation de la Terre pour nos solutions.',
        resupply: 'C’est un vol de ravitaillement équipage ou cargo, pas un vol d’observation de la Terre pour nos solutions.',
        human: 'C’est un vol habité, pas un vol d’observation de la Terre pour nos solutions.',
        secret: 'Les informations publiques sont limitées (gouvernement / classifié). Insuffisant pour un lien Saving Planets.',
        other: 'Son objectif publié n’est pas l’observation de la Terre, la science planétaire ou la météo spatiale liées à nos solutions.'
      },
      exclNote: 'Saving Planets ne rattache pas les lancements menés par la Russie, la Chine, la Corée du Nord ou l’Iran à nos solutions.',
      seeSolution: 'Ouvrir la page de la solution',
      seeHub: 'Voir les solutions liées'
    },
    es: {
      next: 'Próximo lanzamiento', days: 'Días', hrs: 'H', min: 'Min', sec: 'S', window: 'Ventana de lanzamiento',
      err: 'Datos de lanzamiento no disponibles por ahora. Consulta el <a href="https://www.nextspaceflight.com/" target="_blank" rel="noreferrer">calendario completo de lanzamientos en Next Spaceflight</a>.',
      unnamed: 'Misión sin nombre', unkProv: 'Operador desconocido', unkRock: 'Cohete desconocido', tbd: 'Fecha por confirmar',
      status: 'Estado', purpose: 'Propósito de la misión', conn: 'Vínculo con Saving Planets',
      yes: 'Apoya una solución de Saving Planets', no: 'No apoya una solución de Saving Planets',
      unk: 'Vínculo aún desconocido', skip: 'No evaluado para nuestras soluciones',
      detailsMissing: 'Detalles de la misión aún no publicados.',
      srcLL2: 'Launch Library 2 (The Space Devs)',
      type: 'Tipo', orbit: 'Órbita', pad: 'Rampa',
      moreAgency: 'Página del operador / agencia',
      why: {
        earth: 'Las misiones de observación de la Tierra aportan datos de tierra, atmósfera y desastres que cubren nuestras soluciones de Observación de la Tierra.',
        ocean: 'Las misiones oceánicas alimentan el seguimiento del nivel del mar y el medio marino en nuestras soluciones Océano.',
        polar: 'Las misiones polares y de hielo apoyan el trabajo de criosfera en nuestras soluciones Polar.',
        forest: 'Las misiones de bosques e incendios apoyan nuestras soluciones Bosques.',
        weather: 'Las misiones de clima espacial apoyan nuestras soluciones Clima espacial.',
        defense: 'Las misiones de defensa planetaria apoyan nuestras soluciones Defensa planetaria.',
        space: 'Esta misión científica o de exploración figura entre nuestras soluciones Espacio / Proyecto Rawane.'
      },
      noSpin: {
        communications: 'Es una misión de comunicaciones, no un vuelo de observación de la Tierra o ciencia planetaria para nuestras soluciones.',
        navigation: 'Es una misión de navegación / GNSS, no un vuelo de observación de la Tierra para nuestras soluciones.',
        resupply: 'Es un vuelo de reabastecimiento tripulado o de carga, no un vuelo de observación de la Tierra para nuestras soluciones.',
        human: 'Es un vuelo tripulado, no un vuelo de observación de la Tierra para nuestras soluciones.',
        secret: 'La información pública es limitada (gobierno / clasificado). No basta para un vínculo Saving Planets.',
        other: 'Su propósito publicado no es observación de la Tierra, ciencia planetaria o clima espacial ligado a nuestras soluciones.'
      },
      exclNote: 'Saving Planets no vincula lanzamientos liderados por Rusia, China, Corea del Norte o Irán a nuestras soluciones.',
      seeSolution: 'Abrir la página de la solución',
      seeHub: 'Ver soluciones relacionadas'
    },
    it: {
      next: 'Prossimo lancio', days: 'Giorni', hrs: 'Ore', min: 'Min', sec: 'Sec', window: 'Finestra di lancio',
      err: 'Dati sui lanci non disponibili al momento. Consulta il <a href="https://www.nextspaceflight.com/" target="_blank" rel="noreferrer">calendario completo dei lanci su Next Spaceflight</a>.',
      unnamed: 'Missione senza nome', unkProv: 'Operatore sconosciuto', unkRock: 'Razzo sconosciuto', tbd: 'Data da confermare',
      status: 'Stato', purpose: 'Scopo della missione', conn: 'Legame con Saving Planets',
      yes: 'Sostiene una soluzione Saving Planets', no: 'Non sostiene una soluzione Saving Planets',
      unk: 'Legame non ancora noto', skip: 'Non valutato per le nostre soluzioni',
      detailsMissing: 'Dettagli della missione non ancora pubblicati.',
      srcLL2: 'Launch Library 2 (The Space Devs)',
      type: 'Tipo', orbit: 'Orbita', pad: 'Rampa',
      moreAgency: 'Pagina dell’operatore / agenzia',
      why: {
        earth: 'Le missioni di osservazione della Terra forniscono i dati su suolo, atmosfera e disastri coperti dalle nostre soluzioni Osservazione della Terra.',
        ocean: 'Le missioni oceaniche alimentano il monitoraggio di livello del mare e ambiente marino nelle nostre soluzioni Oceano.',
        polar: 'Le missioni polari e sul ghiaccio sostengono il lavoro sulla criosfera nelle nostre soluzioni Polare.',
        forest: 'Le missioni su foreste e incendi sostengono le nostre soluzioni Foreste.',
        weather: 'Le missioni di meteorologia spaziale sostengono le nostre soluzioni Meteo spaziale.',
        defense: 'Le missioni di difesa planetaria sostengono le nostre soluzioni Difesa planetaria.',
        space: 'Questa missione scientifica o di esplorazione figura tra le nostre soluzioni Spazio / Progetto Rawane.'
      },
      noSpin: {
        communications: 'È una missione di comunicazioni, non un volo di osservazione della Terra o scienza planetaria per le nostre soluzioni.',
        navigation: 'È una missione di navigazione / GNSS, non un volo di osservazione della Terra per le nostre soluzioni.',
        resupply: 'È un volo di rifornimento equipaggio o carico, non un volo di osservazione della Terra per le nostre soluzioni.',
        human: 'È un volo con equipaggio, non un volo di osservazione della Terra per le nostre soluzioni.',
        secret: 'Le informazioni pubbliche sono limitate (governo / classificato). Non bastano per un legame Saving Planets.',
        other: 'Lo scopo pubblicato non è osservazione della Terra, scienza planetaria o meteo spaziale legato alle nostre soluzioni.'
      },
      exclNote: 'Saving Planets non collega lanci guidati da Russia, Cina, Corea del Nord o Iran alle nostre soluzioni.',
      seeSolution: 'Apri la pagina della soluzione',
      seeHub: 'Vedi soluzioni correlate'
    },
    ar: {
      next: 'الإطلاق التالي', days: 'أيام', hrs: 'س', min: 'د', sec: 'ث', window: 'نافذة الإطلاق',
      err: 'بيانات الإطلاق غير متاحة حاليًا. راجع <a href="https://www.nextspaceflight.com/" target="_blank" rel="noreferrer">جدول الإطلاق الكامل على Next Spaceflight</a>.',
      unnamed: 'مهمة بلا اسم', unkProv: 'مشغّل غير معروف', unkRock: 'صاروخ غير معروف', tbd: 'التاريخ غير مؤكد',
      status: 'الحالة', purpose: 'غرض المهمة', conn: 'الصلة بـ Saving Planets',
      yes: 'يدعم أحد حلول Saving Planets', no: 'لا يدعم أحد حلول Saving Planets',
      unk: 'الصلة غير معروفة بعد', skip: 'غير مُقيَّم لحلولنا',
      detailsMissing: 'تفاصيل المهمة غير منشورة بعد.',
      srcLL2: 'Launch Library 2 (The Space Devs)',
      type: 'النوع', orbit: 'المدار', pad: 'منصة الإطلاق',
      moreAgency: 'صفحة المشغّل / الوكالة',
      why: {
        earth: 'مهام رصد الأرض توفّر بيانات الأرض والغلاف الجوي والكوارث التي تغطيها حلول رصد الأرض لدينا.',
        ocean: 'مهام المحيطات تغذي مراقبة مستوى البحر والبيئة البحرية في حلول المحيطات لدينا.',
        polar: 'مهام القطبين والجليد تدعم عمل الغلاف الجليدي في حلول القطب لدينا.',
        forest: 'مهام الغابات والحرائق تدعم حلول الغابات لدينا.',
        weather: 'مهام طقس الفضاء تدعم حلول طقس الفضاء لدينا.',
        defense: 'مهام الدفاع الكوكبي تدعم حلول الدفاع الكوكبي لدينا.',
        space: 'هذه المهمة العلمية أو الاستكشافية ضمن حلول الفضاء / مشروع روان لدينا.'
      },
      noSpin: {
        communications: 'هذه مهمة اتصالات، وليست رحلة رصد أرض أو علوم كوكبية لحلولنا.',
        navigation: 'هذه مهمة ملاحة / GNSS، وليست رحلة رصد أرض لحلولنا.',
        resupply: 'هذه رحلة إمداد طاقم أو بضائع، وليست رحلة رصد أرض لحلولنا.',
        human: 'هذه رحلة مأهولة، وليست رحلة رصد أرض لحلولنا.',
        secret: 'المعلومات العامة محدودة (حكومية / سرية). لا تكفي لصلة Saving Planets.',
        other: 'غرضها المنشور ليس رصد الأرض أو العلوم الكوكبية أو طقس الفضاء المرتبط بحلولنا.'
      },
      exclNote: 'لا تربط Saving Planets الإطلاقات التي تقودها روسيا أو الصين أو كوريا الشمالية أو إيران بحلولنا.',
      seeSolution: 'افتح صفحة الحل',
      seeHub: 'اطّلع على الحلول ذات الصلة'
    },
    he: {
      next: 'השיגור הבא', days: 'ימים', hrs: 'שע׳', min: 'דק׳', sec: 'שנ׳', window: 'חלון שיגור',
      err: 'נתוני השיגורים אינם זמינים כרגע. ראו את <a href="https://www.nextspaceflight.com/" target="_blank" rel="noreferrer">לוח השיגורים המלא ב-Next Spaceflight</a>.',
      unnamed: 'משימה ללא שם', unkProv: 'מפעיל לא ידוע', unkRock: 'רקטה לא ידועה', tbd: 'תאריך לאישור',
      status: 'סטטוס', purpose: 'מטרת המשימה', conn: 'קשר ל-Saving Planets',
      yes: 'תומך בפתרון של Saving Planets', no: 'אינו תומך בפתרון של Saving Planets',
      unk: 'הקשר עדיין לא ידוע', skip: 'לא הוערך לפתרונות שלנו',
      detailsMissing: 'פרטי המשימה טרם פורסמו.',
      srcLL2: 'Launch Library 2 (The Space Devs)',
      type: 'סוג', orbit: 'מסלול', pad: 'כן שיגור',
      moreAgency: 'עמוד המפעיל / הסוכנות',
      why: {
        earth: 'משימות תצפית כדור הארץ מספקות נתוני קרקע, אטמוספרה ואסונות שמכסים פתרונות תצפית כדור הארץ שלנו.',
        ocean: 'משימות אוקיינוס מזינות ניטור מפלס הים והסביבה הימית בפתרונות האוקיינוס שלנו.',
        polar: 'משימות קוטב וקרח תומכות בעבודת הקריוספירה בפתרונות הקוטב שלנו.',
        forest: 'משימות יערות ושריפות תומכות בפתרונות היערות שלנו.',
        weather: 'משימות מזג אוויר בחלל תומכות בפתרונות מזג האוויר בחלל שלנו.',
        defense: 'משימות הגנה פלנטרית תומכות בפתרונות ההגנה הפלנטרית שלנו.',
        space: 'משימת מדע או חקר זו מופיעה בין פתרונות החלל / פרויקט רוואן שלנו.'
      },
      noSpin: {
        communications: 'זו משימת תקשורת, לא טיסת תצפית כדור הארץ או מדע פלנטרי לפתרונות שלנו.',
        navigation: 'זו משימת ניווט / GNSS, לא טיסת תצפית כדור הארץ לפתרונות שלנו.',
        resupply: 'זו טיסת אספקה לצוות או מטען, לא טיסת תצפית כדור הארץ לפתרונות שלנו.',
        human: 'זו טיסה מאוישת, לא טיסת תצפית כדור הארץ לפתרונות שלנו.',
        secret: 'המידע הציבורי מוגבל (ממשלתי / מסווג). אין די בו לקשר Saving Planets.',
        other: 'המטרה שפורסמה אינה תצפית כדור הארץ, מדע פלנטרי או מזג אוויר בחלל הקשורים לפתרונות שלנו.'
      },
      exclNote: 'Saving Planets אינה מקשרת שיגורים בהובלת רוסיה, סין, צפון קוריאה או איראן לפתרונות שלנו.',
      seeSolution: 'פתחו את עמוד הפתרון',
      seeHub: 'ראו פתרונות קשורים'
    }
  };
  var t = T[lang] || T.en;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function missionName(l) {
    if (l.mission && l.mission.name) return l.mission.name;
    var p = String(l.name || '').split('|');
    return (p[1] || p[0] || t.unnamed).trim();
  }
  function provider(l) { return (l.launch_service_provider && l.launch_service_provider.name) || t.unkProv; }
  function rocket(l) { return (l.rocket && l.rocket.configuration && l.rocket.configuration.name) || t.unkRock; }
  function mtype(l) { return (l.mission && l.mission.type) || ''; }
  function orbit(l) {
    var o = l.mission && l.mission.orbit;
    if (!o) return '';
    return typeof o === 'string' ? o : (o.name || '');
  }
  function padName(l) {
    var p = l.pad || {};
    return [p.name, p.location && p.location.name].filter(Boolean).join(', ');
  }
  function purposeText(l) {
    var sp = specialPurpose(l);
    if (sp) return sp;
    var d = (l.mission && l.mission.description) ? String(l.mission.description).replace(/\s+/g, ' ').trim() : '';
    if (!d) return null;
    if (d.length > 320) {
      var cut = d.lastIndexOf('.', 300);
      d = (cut > 120 ? d.slice(0, cut + 1) : d.slice(0, 300).replace(/\s+\S*$/, '')) + (cut > 120 ? '' : '…');
    }
    return d;
  }
  function fmt(iso, opts) {
    var d = new Date(iso);
    if (isNaN(d)) return t.tbd;
    var loc = lang === 'en' ? undefined : lang;
    return d.toLocaleString(loc, opts);
  }
  function pad(n) { return n < 10 ? '0' + n : String(n); }

  function excluded(l) {
    var loc = (l.pad && l.pad.location && l.pad.location.name) || '';
    var cc = (l.pad && l.pad.country && l.pad.country.alpha_3_code) || '';
    if (cc === 'RUS' || cc === 'CHN' || cc === 'PRK' || cc === 'IRN') return true;
    return EXCL.test(loc + ' | ' + provider(l));
  }

  function agencyUrl(l) {
    var urls = l.infoURLs || l.info_urls || [];
    for (var i = 0; i < urls.length; i++) {
      var u = typeof urls[i] === 'string' ? urls[i] : (urls[i] && urls[i].url);
      if (u && /^https?:\/\//i.test(u)) return u;
    }
    var name = missionName(l);
    var prov = provider(l);
    if (/starlink/i.test(name) || /starlink/i.test(prov + name)) return 'https://www.spacex.com/missions/starlink';
    if (/iQPS|QPS-SAR|Sea God Surveys|Mountain God Rises/i.test(name)) return 'https://i-qps.net/en/';
    if (/SpaceX/i.test(prov)) return 'https://www.spacex.com/launches';
    if (/Rocket Lab/i.test(prov)) return 'https://www.rocketlabusa.com/missions/';
    if (/Indian Space Research|ISRO/i.test(prov)) return 'https://www.isro.gov.in/';
    if (/Arianespace/i.test(prov)) return 'https://www.arianespace.com/';
    if (/NASA/i.test(prov)) return 'https://www.nasa.gov/missions/';
    if (/ESA|Arianespace|European Space/i.test(prov)) return 'https://www.esa.int/Enabling_Support/Space_Transportation';
    if (/United Launch Alliance|ULA/i.test(prov)) return 'https://www.ulalaunch.com/missions';
    if (/Northrop/i.test(prov)) return 'https://www.northropgrumman.com/space';
    if (/Blue Origin/i.test(prov)) return 'https://www.blueorigin.com/';
    if (/Amazon|Kuiper|Leo/i.test(name) && /Arianespace|ULA|Blue Origin|SpaceX/i.test(prov)) return 'https://www.aboutamazon.com/news/innovation-at-amazon/amazon-leo';
    return null;
  }


  function isStarlink(l) {
    var n = missionName(l) + ' ' + ((l.mission && l.mission.description) || '');
    return /starlink/i.test(n);
  }
  function isStarship(l) {
    var rock = rocket(l) + ' ' + missionName(l) + ' ' + ((l.mission && l.mission.description) || '');
    return /\bstarship\b/i.test(rock) || /super heavy/i.test(rock);
  }
  /* Starlink / Starship: confirmed vs potential kept separate; no invented EO claims.
     Sources used in blurbs: SpaceX Direct to Cell / disaster update; MediaTek MWC 2026 WEA;
     SpaceX Starshield (EO is separate); SpaceX Starship 100+ t; SpaceX Starlink V3 via Starship. */
  function specialPurpose(l) {
    if (isStarlink(l)) {
      return 'SpaceX Starlink is a low-Earth-orbit broadband internet constellation. Confirmed: Starlink Direct to Cell has delivered Wireless Emergency Alerts (WEA / CMAS) and Earthquake and Tsunami Warning System (ETWS) messages to unmodified phones when terrestrial networks were down (SpaceX; MediaTek, MWC 2026). Starlink V3 is SpaceX’s next-generation communications capacity upgrade (SpaceX describes roughly 20× Direct-to-Cell throughput vs the first generation) — not an announced Earth-observation imaging payload.';
    }
    if (isStarship(l)) {
      return 'Starship is SpaceX’s fully reusable Super Heavy + Starship system, designed for more than 100 metric tonnes to low Earth orbit and a large payload volume for satellites and cargo (SpaceX). This flight’s published role is vehicle testing and/or deploying Starlink unless a different payload is named in the launch listing.';
    }
    return null;
  }
  function specialClassify(l) {
    if (isStarlink(l)) {
      return {
        kind: 'no', label: t.no,
        text: 'This launch does not support a Saving Planets Earth-observation or planetary-science solution page. Confirmed disaster-communications role: Direct-to-Cell emergency alerts (SpaceX; MediaTek). Not claimed here: Starlink V3 as optical/SAR Earth sensing — SpaceX describes V3 as communications capacity; Earth-observation sensing is listed under Starshield, a separate government product (SpaceX).',
        page: null, out: 'https://www.spacex.com/updates/starlink-disaster-response/',
        srcHtml: 'Sources: <a href="https://www.spacex.com/updates/starlink-disaster-response/" target="_blank" rel="noopener noreferrer">SpaceX, Direct to Cell / disaster response</a>; <a href="https://www.mediatek.com/press-room/mediatek-demonstrates-emergency-satellite-services-for-mobile-devices-with-starlink-mobile" target="_blank" rel="noopener noreferrer">MediaTek, emergency satellite alerts (Mar 2026)</a>; <a href="https://www.spacex.com/starshield" target="_blank" rel="noopener noreferrer">SpaceX Starshield</a> (EO is separate).'
      };
    }
    if (isStarship(l)) {
      return {
        kind: 'no', label: t.no,
        text: 'A Starship flight does not by itself support a Saving Planets solution page unless its published payload is an Earth-observation or planetary-science mission we cover. Confirmed (SpaceX): 100+ t-class capacity and large fairing for satellite delivery to LEO. Stated potential only (SpaceX capacity; science commentary e.g. Physics Today on larger observatories): that capacity could enable heavier climate and hazard sensors in LEO/MEO/GEO — not confirmed for this flight unless a specific sensor mission is listed.',
        page: null, out: 'https://www.spacex.com/vehicles/starship',
        srcHtml: 'Sources: <a href="https://www.spacex.com/vehicles/starship" target="_blank" rel="noopener noreferrer">SpaceX Starship</a>; <a href="https://www.spacex.com/updates/" target="_blank" rel="noopener noreferrer">SpaceX updates</a> (Starlink V3 via Starship).'
      };
    }
    return null;
  }

  function classify(l) {
    if (excluded(l)) {
      return { kind: 'skip', label: t.skip, text: t.exclNote, page: null, out: agencyUrl(l) };
    }
    var spec = specialClassify(l);
    if (spec) return spec;
    var name = missionName(l);
    var typ = mtype(l);
    var desc = ((l.mission && l.mission.description) || '') + ' ' + name + ' ' + typ;
    var purpose = purposeText(l);

    for (var i = 0; i < PAGE_MATCH.length; i++) {
      var m = PAGE_MATCH[i];
      if (m.re.test(name) || m.re.test(desc)) {
        return {
          kind: 'yes', label: t.yes, text: t.why[m.why] || t.why.earth,
          page: m.page, hub: m.hub, out: null
        };
      }
    }

    var tl = typ.toLowerCase();
    if (/earth science|earth observation|remote sensing|meteorology|climate|oceanography|hydrology/i.test(typ + ' ' + desc) ||
        /\b(SAR|synthetic aperture|earth imaging|earth observation|remote sensing)\b/i.test(desc)) {
      var why = 'earth';
      var hub = 'Earth_Observation.html';
      if (/ocean|sea level|marine|altimeter|swot/i.test(desc)) { why = 'ocean'; hub = 'Oceans.html'; }
      else if (/ice|polar|cryo|glacier|snow/i.test(desc)) { why = 'polar'; hub = 'Polar.html'; }
      else if (/forest|fire|biomass|deforestation/i.test(desc)) { why = 'forest'; hub = 'Deforestation.html'; }
      return { kind: 'yes', label: t.yes, text: t.why[why], page: hub, hub: hub, out: null };
    }
    if (/planetary science|planetary defence|planetary defense|asteroid|heliophysics|solar|astronomy|astrophysics|lunar science/i.test(typ + ' ' + desc)) {
      var w = /asteroid|defence|defense|neo|impactor/i.test(desc + typ) ? 'defense'
        : /solar|helio|space weather|coronal/i.test(desc + typ) ? 'weather' : 'space';
      var hub2 = w === 'defense' ? 'Planetary_Defense.html' : w === 'weather' ? 'Space_Weather.html' : 'Space.html';
      return { kind: 'yes', label: t.yes, text: t.why[w], page: hub2, hub: hub2, out: null };
    }

    if (/top secret|government\/top secret|classified/i.test(typ + ' ' + desc) || (!purpose && /government/i.test(typ))) {
      return { kind: 'unk', label: t.unk, text: t.noSpin.secret + ' ' + t.detailsMissing, page: null, out: agencyUrl(l) };
    }
    if (!purpose && !typ) {
      return { kind: 'unk', label: t.unk, text: t.detailsMissing, page: null, out: agencyUrl(l) };
    }

    var spinKey = 'other';
    if (/communication/i.test(typ) || /starlink|kuiper|amazon leo|oneweb|satnet|broadband/i.test(name + desc)) spinKey = 'communications';
    else if (/navigation|gps|gnss|irnss|galileo|beidou/i.test(typ + name)) spinKey = 'navigation';
    else if (/resupply|cargo|iss|cygnus|progress|dragon/i.test(typ + name) && !/science/i.test(typ)) spinKey = 'resupply';
    else if (/human|crew|crew dragon|starliner|shenzhou|gaganyaan/i.test(typ + name)) spinKey = 'human';

    return { kind: 'no', label: t.no, text: t.noSpin[spinKey] || t.noSpin.other, page: null, out: agencyUrl(l) };
  }

  function blurbHtml(l) {
    var purpose = purposeText(l);
    var c = classify(l);
    var srcLine = (c && c.srcHtml) ? c.srcHtml : esc(t.srcLL2);
    var purposeBlock = '<div class="lw-blurb-block"><p class="lw-blurb-k">' + esc(t.purpose) + '</p><p class="lw-blurb-t">' +
      esc(purpose || t.detailsMissing) + '</p>' +
      '<p class="lw-blurb-src">' + srcLine + '</p></div>';

    var link = '';
    if (c.kind === 'yes' && c.page) {
      link = '<p class="lw-blurb-link"><a class="lw-sol" href="' + esc(prefix + c.page) + '">' + esc(t.seeSolution) + '</a></p>';
    } else if (c.out) {
      link = '<p class="lw-blurb-link"><a class="lw-out" href="' + esc(c.out) + '" target="_blank" rel="noopener noreferrer">' + esc(t.moreAgency) + '</a></p>';
    }

    return purposeBlock +
      '<div class="lw-blurb-block lw-' + c.kind + '"><p class="lw-blurb-k">' + esc(t.conn) +
      ' <span class="lw-badge">' + esc(c.label) + '</span></p><p class="lw-blurb-t">' + esc(c.text) + '</p>' + link + '</div>';
  }

  function metaLine(l) {
    var bits = [];
    if (mtype(l)) bits.push(esc(t.type) + ': ' + esc(mtype(l)));
    if (orbit(l)) bits.push(esc(t.orbit) + ': ' + esc(orbit(l)));
    var p = padName(l); if (p) bits.push(esc(t.pad) + ': ' + esc(p));
    return bits.length ? '<p class="lw-extra">' + bits.join(' · ') + '</p>' : '';
  }

  function readCache() {
    try {
      var c = JSON.parse(sessionStorage.getItem(CACHE_KEY));
      if (c && Date.now() - c.t < CACHE_MS && c.d && c.d.results) return c.d;
    } catch (e) {}
    return null;
  }
  function writeCache(d) {
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ t: Date.now(), d: d })); } catch (e) {}
  }

  function showError() {
    if (timer) clearInterval(timer);
    nextEl.innerHTML = '<p class="lw-error">' + t.err + '</p>';
    listEl.innerHTML = '';
  }

  function tick(netMs, el) {
    var diff = netMs - Date.now();
    if (diff <= 0) {
      el.innerHTML = '<div class="lw-unit"><b>T-0</b><small>' + esc(t.window) + '</small></div>';
      return;
    }
    var s = Math.floor(diff / 1000), d = Math.floor(s / 86400), h = Math.floor((s % 86400) / 3600),
      m = Math.floor((s % 3600) / 60), sec = s % 60;
    el.innerHTML =
      '<div class="lw-unit"><b>' + d + '</b><small>' + esc(t.days) + '</small></div>' +
      '<div class="lw-unit"><b>' + pad(h) + '</b><small>' + esc(t.hrs) + '</small></div>' +
      '<div class="lw-unit"><b>' + pad(m) + '</b><small>' + esc(t.min) + '</small></div>' +
      '<div class="lw-unit"><b>' + pad(sec) + '</b><small>' + esc(t.sec) + '</small></div>';
  }

  function render(data) {
    var now = Date.now();
    var r = ((data && data.results) || []).filter(function (l) {
      var ab = l.status && l.status.abbrev ? String(l.status.abbrev).toLowerCase() : '';
      if (ab === 'success' || ab === 'failure' || ab === 'partial failure') return false;
      var x = new Date(l.net).getTime();
      return isNaN(x) || x > now;
    });
    if (!r.length) { showError(); return; }

    var n = r[0];
    var status = n.status && n.status.abbrev ? ' · ' + esc(t.status) + ': ' + esc(n.status.abbrev) : '';
    var where = n.pad && n.pad.location && n.pad.location.name ? '<br>' + esc(n.pad.location.name) : '';
    nextEl.innerHTML =
      '<p class="lw-kicker">' + esc(t.next) + '</p>' +
      '<h3 class="lw-mission">' + esc(missionName(n)) + '</h3>' +
      '<p class="lw-meta">' + esc(provider(n)) + ' · ' + esc(rocket(n)) + '</p>' +
      '<p class="lw-when">' + esc(fmt(n.net, {
        weekday: 'short', month: 'short', day: 'numeric', year: 'numeric',
        hour: 'numeric', minute: '2-digit', timeZoneName: 'short'
      })) + status + where + '</p>' +
      metaLine(n) +
      '<div class="lw-countdown" role="timer" aria-label="' + esc(t.next) + '"></div>' +
      '<div class="lw-blurbs">' + blurbHtml(n) + '</div>';

    var cd = nextEl.querySelector('.lw-countdown');
    var netMs = new Date(n.net).getTime();
    if (timer) clearInterval(timer);
    if (isNaN(netMs)) { cd.innerHTML = ''; }
    else { tick(netMs, cd); timer = setInterval(function () { tick(netMs, cd); }, 1000); }

    listEl.innerHTML = r.slice(1, 20).map(function (l) {
      var st = l.status && l.status.abbrev ? ' · ' + esc(l.status.abbrev) : '';
      return '<li class="lw-card">' +
        '<div class="lw-card-top">' +
        '<span class="lw-l-name">' + esc(missionName(l)) +
        '<span class="lw-l-sub">' + esc(provider(l)) + ' · ' + esc(rocket(l)) + st + '</span></span>' +
        '<span class="lw-l-date">' + esc(fmt(l.net, { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' })) + '</span>' +
        '</div>' + metaLine(l) +
        '<div class="lw-blurbs">' + blurbHtml(l) + '</div></li>';
    }).join('');
  }

  var cached = readCache();
  if (cached) { render(cached); return; }
  var done = false;
  var guard = setTimeout(function () { if (!done) { done = true; showError(); } }, 10000);
  var ctl = window.AbortController ? new AbortController() : null;
  if (ctl) setTimeout(function () { ctl.abort(); }, 10000);
  try {
    fetch(API, { headers: { Accept: 'application/json' }, signal: ctl ? ctl.signal : undefined })
      .then(function (res) { if (!res.ok) throw new Error('HTTP ' + res.status); return res.json(); })
      .then(function (d) {
        if (done) return; done = true; clearTimeout(guard); writeCache(d);
        try { render(d); } catch (e) { showError(); }
      })
      .catch(function () { if (done) return; done = true; clearTimeout(guard); showError(); });
  } catch (e) { done = true; clearTimeout(guard); showError(); }
})();
