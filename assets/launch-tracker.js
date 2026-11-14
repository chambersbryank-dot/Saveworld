/* Live Launch Tracker (Launch Library 2). Purpose blurbs + Saving Planets connection.
   Data: https://ll.thespacedevs.com (The Space Devs). Free tier; we cache 10 min client-side.
   Do not scrape nextspaceflight.com. No invented facts: purpose from LL2 mission.description;
   connection from published mission type/name vs our solution hubs; else "not yet published". */
(function () {
  /* Feed (upcoming + recent launches, kept for the rest of launch day in Hawaii / 24 h): assets/launch-feed.js */
  var FEED = window.SPLaunchFeed;
  var nextEl = document.getElementById('lw-next');
  var listEl = document.getElementById('lw-list');
  if (!nextEl || !listEl || !FEED) return;
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
      '.launch-widget .lw-card-top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.25rem 1rem}' +
      '.launch-widget .lw-local{margin:.2rem 0 0;font-size:.9rem}' +
      '.launch-widget .lw-watch{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:.45rem 1rem;border-radius:999px;color:#fff;font-weight:800;text-decoration:none;background-color:#0a4f78;background-image:linear-gradient(180deg,rgba(255,255,255,.28),rgba(255,255,255,.06)),linear-gradient(#0a4f78,#0a4f78);border:1px solid rgba(160,225,255,.7)}' +
      '.launch-widget .lw-watch-note{margin:.35rem 0;font-size:.85rem;color:rgba(255,255,255,.8)}' +
      '.launch-widget .lw-pay{margin-top:.65rem;padding:.7rem .8rem;border-radius:14px;background:transparent}' +
      '.launch-widget .lw-mini{display:flex;gap:.35rem;margin:.35rem 0}' +
      '.launch-widget .lw-mini b{font-size:1rem}' +
      '.launch-widget .lw-stage{position:relative;width:100%;max-width:40rem;aspect-ratio:16/9;margin:.65rem 0;background:#041018;border-radius:12px;overflow:hidden}' +
      '.launch-widget .lw-stage iframe{position:absolute;inset:0;width:100%;height:100%;border:0}' +
      '.launch-widget .lw-play{position:absolute;inset:0;width:100%;margin:0;border:0;cursor:pointer;color:#fff;font:800 1rem/1.3 Montserrat,sans-serif;background-color:#0a4f78;background-image:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.06))}' +
      '.launch-widget a.lw-play{display:flex;align-items:center;justify-content:center;text-align:center;text-decoration:none;padding:0 1rem;box-sizing:border-box}' +
      '.launch-widget .lw-play:focus-visible{outline:3px solid #fff;outline-offset:-6px}' +
      '.launch-widget .lw-nsf{margin:.45rem 0 .2rem;font-size:.92rem;line-height:1.4;color:#f4fbff}' +
      '.launch-widget .lw-nsf a{color:#8fd3ff;font-weight:700}' +
      '.launch-widget .lw-done{display:inline-block;margin:.35rem 0;padding:.45rem .9rem;border-radius:999px;font-weight:800;font-size:.95rem;color:#7dffd0;background:rgba(0,184,148,.16);border:1px solid rgba(0,184,148,.5)}';
    document.head.appendChild(st);
  }

  /* RU/CN/KP/IR-led (founder Oct 26):
     - When relevant: link our Saving Planets solution page (tight Earth / solar-system benefit wording).
     - Never outbound to their agency/operator sites (no links, embeds, images, scripts, APIs, or data feeds).
     - We never invite or enable access by connecting our site to theirs.
     - Facts from LL2 / neutral notes only (code comments / plain source line, not their domains). */
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
      exclNote: 'When relevant we link our solution page; we never link Russia-, China-, North Korea- or Iran-led operator sites.',
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
      exclNote: 'When relevant we link our solution page; we never link Russia-, China-, North Korea- or Iran-led operator sites.',
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
      exclNote: 'When relevant we link our solution page; we never link Russia-, China-, North Korea- or Iran-led operator sites.',
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
      exclNote: 'When relevant we link our solution page; we never link Russia-, China-, North Korea- or Iran-led operator sites.',
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
      exclNote: 'When relevant we link our solution page; we never link Russia-, China-, North Korea- or Iran-led operator sites.',
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
      exclNote: 'When relevant we link our solution page; we never link Russia-, China-, North Korea- or Iran-led operator sites.',
      seeSolution: 'פתחו את עמוד הפתרון',
      seeHub: 'ראו פתרונות קשורים'
    }
  };
  var t = T[lang] || T.en;
  var PICK = {
    en: { choose:'Choose an upcoming launch', loading:'Loading launches…', summary:'Summary', mission:'What this mission is', watch:'Come back and watch', watchInvite:'Come back and watch the live event. Times move, so check again close to liftoff.', watchMissing:'This listing does not include a public livestream or info link we can share.', watchRestricted:'We do not link a watch page for this launch.', history:'A short history', historyMissing:'A longer history of this vehicle is not on this page. The facts above are from the launch listing.', net:'No earlier than', tbdNote:'The date is still to be confirmed (TBD / NET).', sources:'Sources', live:'Official livestream or info', restrictedHist:'This launch is led by a program whose sites we do not link. We only say how this kind of mission can help Earth or the solar system, and we link our own solution page when one matches.' },
    fr: { choose:'Choisir un lancement à venir', loading:'Chargement des lancements…', summary:'Résumé', mission:'En quoi consiste la mission', watch:'Revenir pour regarder', watchInvite:'Revenez pour le direct. Les horaires bougent : revérifiez près du décollage.', watchMissing:'Cette fiche n’indique pas de lien public de direct que nous pouvons partager.', watchRestricted:'Nous ne proposons pas de lien pour suivre ce lancement.', history:'Une courte histoire', historyMissing:'Une histoire plus longue de cet engin n’est pas sur cette page. Les faits ci-dessus viennent de la fiche de lancement.', net:'Pas avant', tbdNote:'La date reste à confirmer (TBD / NET).', sources:'Sources', live:'Direct ou page officielle', restrictedHist:'Ce lancement est mené par un programme dont nous ne lions pas les sites. Nous disons seulement comment ce type de mission peut aider la Terre ou le système solaire, et nous renvoyons à notre page de solution quand elle correspond.' },
    es: { choose:'Elige un lanzamiento próximo', loading:'Cargando lanzamientos…', summary:'Resumen', mission:'Qué es esta misión', watch:'Vuelve para verlo', watchInvite:'Vuelve para el evento en vivo. Los horarios cambian: revísalo cerca del despegue.', watchMissing:'Esta ficha no incluye un enlace público de transmisión que podamos compartir.', watchRestricted:'No ofrecemos un enlace para ver este lanzamiento.', history:'Una historia breve', historyMissing:'Una historia más larga de este vehículo no está en esta página. Los datos de arriba salen de la ficha de lanzamiento.', net:'No antes de', tbdNote:'La fecha sigue por confirmar (TBD / NET).', sources:'Fuentes', live:'Transmisión o ficha oficial', restrictedHist:'Este lanzamiento lo dirige un programa cuyos sitios no enlazamos. Solo decimos cómo este tipo de misión puede ayudar a la Tierra o al sistema solar, y enlazamos nuestra página de solución cuando encaja.' },
    ar: { choose:'اختر إطلاقاً قادماً', loading:'جارٍ تحميل الإطلاقات…', summary:'ملخص', mission:'ما هذه المهمة', watch:'عُد للمشاهدة', watchInvite:'عُد لمشاهدة البث المباشر. المواعيد تتغير، فراجعها قرب الإقلاع.', watchMissing:'لا تتضمن هذه البطاقة رابط بث عام يمكننا مشاركته.', watchRestricted:'لا نعرض رابط مشاهدة لهذا الإطلاق.', history:'تاريخ موجز', historyMissing:'لا يوجد في هذه الصفحة تاريخ أطول لهذه المركبة. الحقائق أعلاه من بطاقة الإطلاق.', net:'ليس قبل', tbdNote:'التاريخ ما زال بانتظار التأكيد (TBD / NET).', sources:'المصادر', live:'بث أو صفحة رسمية', restrictedHist:'يقود هذا الإطلاق برنامج لا نربط بمواقعه. نذكر فقط كيف يمكن لهذا النوع من المهام أن يفيد الأرض أو المجموعة الشمسية، ونربط بصفحة حلّنا عندما تنطبق.' },
    it: { choose:'Scegli un lancio in programma', loading:'Caricamento dei lanci…', summary:'Sintesi', mission:'Che cos’è questa missione', watch:'Torna a guardare', watchInvite:'Torna per l’evento in diretta. Gli orari si spostano: ricontrolla vicino al decollo.', watchMissing:'Questa scheda non include un link pubblico di diretta che possiamo condividere.', watchRestricted:'Non offriamo un link per seguire questo lancio.', history:'Una breve storia', historyMissing:'Una storia più lunga di questo veicolo non è in questa pagina. I fatti sopra vengono dalla scheda di lancio.', net:'Non prima del', tbdNote:'La data è ancora da confermare (TBD / NET).', sources:'Fonti', live:'Diretta o pagina ufficiale', restrictedHist:'Questo lancio è guidato da un programma di cui non colleghiamo i siti. Diciamo solo come questo tipo di missione può aiutare la Terra o il sistema solare, e colleghiamo la nostra pagina di soluzione quando corrisponde.' },
    he: { choose:'בחרו שיגור קרוב', loading:'טוען שיגורים…', summary:'תקציר', mission:'מהי המשימה', watch:'חזרו לצפות', watchInvite:'חזרו לאירוע החי. הזמנים זזים, אז בדקו שוב סמוך להמראה.', watchMissing:'ברשומה הזו אין קישור שידור פומבי שאפשר לשתף.', watchRestricted:'איננו מציעים קישור צפייה לשיגור הזה.', history:'היסטוריה קצרה', historyMissing:'היסטוריה ארוכה יותר של הרכב הזה אינה בעמוד. העובדות למעלה לקוחות מרשומת השיגור.', net:'לא לפני', tbdNote:'התאריך עדיין לאישור (TBD / NET).', sources:'מקורות', live:'שידור או עמוד רשמי', restrictedHist:'את השיגור הזה מוביל גוף שאת אתריו איננו מקשרים. אנו מציינים רק איך סוג משימה כזה יכול לעזור לכדור הארץ או למערכת השמש, ומקשרים לעמוד הפתרון שלנו כשיש התאמה.' }
  };
  var pk = PICK[lang] || PICK.en;
  var ADD = {
    en: { watchLive:'Watch live', play:'View The Launch Here', playNsf:'Play live coverage', yourTime:'Your time:', going:"What's going up", tba:'TBA', onMap:'See it on the satellite map', watchTba:'Watch link: TBA. No public stream was listed.', nsf:'Live coverage by NASASpaceflight (independent, not SpaceX’s official feed).', nsfChannel:'NASASpaceflight channel', officialSx:'Official SpaceX webcast & mission guide', altView:'Alternate view' },
    fr: { watchLive:'Regarder en direct', play:'Voir le lancement ici', playNsf:'Lire la couverture en direct', yourTime:'Votre heure :', going:'Ce qui décolle', tba:'À confirmer', onMap:'Voir sur la carte des satellites', watchTba:'Lien du direct : à confirmer. Aucun flux public n’est indiqué.', nsf:'Couverture en direct par NASASpaceflight (indépendante, ce n’est pas le flux officiel de SpaceX).', nsfChannel:'Chaîne NASASpaceflight', officialSx:'Webcast officiel de SpaceX et guide de mission', altView:'Vue alternative' },
    es: { watchLive:'Ver en vivo', play:'Ver el lanzamiento aquí', playNsf:'Reproducir la cobertura en vivo', yourTime:'Tu hora:', going:'Qué sube', tba:'Por confirmar', onMap:'Verlo en el mapa de satélites', watchTba:'Enlace del directo: por confirmar. No hay una transmisión pública indicada.', nsf:'Cobertura en vivo de NASASpaceflight (independiente, no es la señal oficial de SpaceX).', nsfChannel:'Canal de NASASpaceflight', officialSx:'Webcast oficial de SpaceX y guía de la misión', altView:'Vista alternativa' },
    ar: { watchLive:'شاهد البث المباشر', play:'شاهد الإطلاق هنا', playNsf:'تشغيل التغطية المباشرة', yourTime:'وقتك المحلي:', going:'ما الذي ينطلق', tba:'غير مؤكد', onMap:'شاهده على خريطة الأقمار', watchTba:'رابط المشاهدة: غير مؤكد. لا يوجد بث عام مذكور.', nsf:'تغطية مباشرة من NASASpaceflight (مستقلة، وليست البث الرسمي لسبيس إكس).', nsfChannel:'قناة NASASpaceflight', officialSx:'البث الرسمي لسبيس إكس ودليل المهمة', altView:'عرض بديل' },
    it: { watchLive:'Guarda in diretta', play:'Guarda il lancio qui', playNsf:'Avvia la copertura in diretta', yourTime:'Il tuo orario:', going:'Che cosa sale', tba:'Da confermare', onMap:'Vedilo sulla mappa dei satelliti', watchTba:'Link della diretta: da confermare. Nessun flusso pubblico è indicato.', nsf:'Copertura in diretta di NASASpaceflight (indipendente, non è il feed ufficiale di SpaceX).', nsfChannel:'Canale NASASpaceflight', officialSx:'Webcast ufficiale di SpaceX e guida della missione', altView:'Vista alternativa' },
    he: { watchLive:'צפו בשידור החי', play:'צפו בשיגור כאן', playNsf:'נגנו את הסיקור החי', yourTime:'השעה אצלכם:', going:'מה עולה', tba:'טרם פורסם', onMap:'ראו במפת הלוויינים', watchTba:'קישור לצפייה: טרם פורסם. אין שידור פומבי ברשימה.', nsf:'שידור חי של NASASpaceflight (עצמאי, לא הערוץ הרשמי של ספייס אקס).', nsfChannel:'הערוץ של NASASpaceflight', officialSx:'השידור הרשמי של ספייס אקס ומדריך המשימה', altView:'תצוגה חלופית' }
  };
  var ui = ADD[lang] || ADD.en;
  /* SpaceX page checked 13 Nov 2026: window opens 4:45 p.m. CT (22:45 UTC), 75 minutes, pending approval. */
  var STAR = {
    en: ['SpaceX says Flight 15 is preparing to launch as soon as Friday, 13 November 2026. A 75-minute window opens at 4:45 p.m. Central Time, pending regulatory approval.','The upper stage is planned to deploy 26 Starlink V3 satellites. SpaceX says each one is meant to add 1 terabit of capacity to the Starlink network.','SpaceX describes these V3 satellites as communications capacity, not Earth sensing.','Three of the satellites carry cameras to photograph Starship’s heat shield for this flight test. That is a rocket-test job, not an instrument for the planet’s health.'],
    fr: ['SpaceX dit que le vol 15 se prépare à partir dès le vendredi 13 novembre 2026. Une fenêtre de 75 minutes s’ouvre à 16 h 45, heure du Centre, sous réserve d’autorisation.','L’étage supérieur doit déployer 26 satellites Starlink V3. SpaceX dit que chacun doit ajouter 1 térabit de capacité au réseau Starlink.','SpaceX décrit ces satellites V3 comme de la capacité de communication, pas comme des capteurs de la Terre.','Trois satellites emportent des caméras pour photographier le bouclier thermique de Starship pendant cet essai. C’est un travail d’essai de fusée, pas un instrument pour la santé de la planète.'],
    es: ['SpaceX dice que el vuelo 15 se prepara para lanzarse a partir del viernes 13 de noviembre de 2026. Una ventana de 75 minutos se abre a las 4:45 p. m., hora del Centro, pendiente de aprobación.','La etapa superior debe desplegar 26 satélites Starlink V3. SpaceX dice que cada uno aportará 1 terabit de capacidad a la red Starlink.','SpaceX describe estos satélites V3 como capacidad de comunicaciones, no como sensores de la Tierra.','Tres satélites llevan cámaras para fotografiar el escudo térmico de Starship en esta prueba. Es una tarea de ensayo del cohete, no un instrumento para la salud del planeta.'],
    ar: ['تقول سبيس إكس إن الرحلة 15 تستعد للانطلاق ابتداءً من الجمعة 13 نوفمبر 2026. تفتح نافذة من 75 دقيقة عند 4:45 مساءً بتوقيت الوسط، بانتظار الموافقة التنظيمية.','يُخطط للمرحلة العليا أن تنشر 26 قمرًا من ستارلينك V3. تقول سبيس إكس إن كل قمر يهدف إلى إضافة 1 تيرابت من السعة إلى شبكة ستارلينك.','تصف سبيس إكس أقمار V3 بأنها سعة اتصالات، وليست استشعارًا للأرض.','ثلاثة أقمار تحمل كاميرات لتصوير الدرع الحراري لستارشيب في هذا الاختبار. هذا عمل اختبار للصاروخ، وليس أداة لصحة الكوكب.'],
    it: ['SpaceX dice che il volo 15 si prepara a partire da venerdì 13 novembre 2026. Una finestra di 75 minuti si apre alle 16:45 ora del Centro, in attesa di autorizzazione.','Lo stadio superiore deve rilasciare 26 satelliti Starlink V3. SpaceX dice che ciascuno deve aggiungere 1 terabit di capacità alla rete Starlink.','SpaceX descrive questi satelliti V3 come capacità di comunicazione, non come sensori della Terra.','Tre satelliti portano telecamere per fotografare lo scudo termico di Starship in questo test. È un compito di prova del razzo, non uno strumento per la salute del pianeta.'],
    he: ['ספייס אקס אומרת שטיסה 15 נערכת לשיגור החל מיום שישי, 13 בנובמבר 2026. חלון של 75 דקות נפתח ב-16:45 לפי שעון המרכז, בכפוף לאישור.','השלב העליון מתוכנן לשחרר 26 לווייני סטארלינק V3. ספייס אקס אומרת שכל אחד אמור להוסיף טרה-ביט אחד של קיבולת לרשת.','ספייס אקס מתארת את לווייני V3 כקיבולת תקשורת, לא כחישה של כדור הארץ.','שלושה לוויינים נושאים מצלמות כדי לצלם את מגן החום של סטארשיפ במבחן הזה. זו עבודת מבחן של הטיל, לא מכשיר לבריאות כוכב הלכת.']
  };

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

  function isRestricted(l) {
    var loc = (l.pad && l.pad.location && l.pad.location.name) || '';
    var cc = (l.pad && l.pad.country && l.pad.country.alpha_3_code) || '';
    if (cc === 'RUS' || cc === 'CHN' || cc === 'PRK' || cc === 'IRN') return true;
    return EXCL.test(loc + ' | ' + provider(l));
  }

  /* Hosts we never link to or fetch from (RU/CN/KP/IR-led agencies / state space entities). */
  var BLOCKED_HOST = /(?:^|\.)(?:roscosmos\.ru|gov\.ru|mil\.ru|cnsa\.gov\.cn|cmse\.gov\.cn|calt\.com\.cn|casc\.com\.cn|casic\.com\.cn|spacechina\.com|clep\.org\.cn|nssc\.ac\.cn|irna\.ir|isa\.ir|isa\.gov\.ir|nksa\.go\.kr|kcnawatch\.org)$/i;

  function blockedUrl(u) {
    if (!u || !/^https?:\/\//i.test(u)) return true;
    try {
      var h = (new URL(u)).hostname.replace(/^www\./i, '');
      if (BLOCKED_HOST.test(h)) return true;
      /* Broad country-code / state space cut: never invite access via their TLDs when restricted. */
      if (/\.(?:ru|xn--p1ai|cn|xn--fiqs8s|ir|kp)$/i.test(h)) return true;
    } catch (e) { return true; }
    return false;
  }

  function isStarship15(l) {
    var s = ((l && l.name) || '') + ' ' + missionName(l);
    return /starship flight 15|starlink group 31-2/i.test(s);
  }
  var STREAMS = [];
  function parseEmbed(url, title) {
    if (!url || blockedUrl(url)) return null;
    var yt = String(url).match(/(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/|youtube-nocookie\.com\/embed\/)([\w-]{6,})/);
    if (yt) return { kind: 'youtube', id: yt[1], title: title || 'Official live stream' };
    if (/(?:^|\.)(?:x|twitter)\.com$/i.test((function () { try { return new URL(url).hostname.replace(/^www\./i, ''); } catch (e) { return ''; } })()) &&
        /\/status\/\d+|\/i\/broadcasts\/[A-Za-z0-9]+/.test(url)) {
      return { kind: 'x', url: url, title: title || 'Official live stream' };
    }
    return null;
  }
  function publisherOk(v, l) {
    var pub = String((v && v.publisher) || '').toLowerCase();
    if (/spaceflight now|nasa ?spaceflight|everyday astronaut|teslarati/.test(pub)) return false;
    if (/nasa|united launch|rocket lab|\besa\b|arianespace|spacex|jaxa|isro|blue origin|northrop/.test(pub)) return true;
    var prov = String(provider(l) || '').toLowerCase();
    return !!(pub && prov && (prov.indexOf(pub) >= 0 || pub.indexOf(prov) >= 0));
  }
  function streamRow(l) {
    if (isRestricted(l)) return null;
    var name = (((l && l.name) || '') + ' ' + missionName(l)).toLowerCase();
    for (var s = 0; s < STREAMS.length; s++) {
      var row = STREAMS[s];
      if (row && row.match && name.indexOf(String(row.match).toLowerCase()) >= 0) return row;
    }
    return null;
  }
  function officialEmbed(l) {
    if (isRestricted(l)) return null;
    var row = streamRow(l);
    if (row && row.url) {
      var set = parseEmbed(row.url, missionName(l));
      if (set) return set;
    }
    var vids = [].concat((l && l.vid_urls) || [], (l && l.mission && l.mission.vid_urls) || []);
    for (var i = 0; i < vids.length; i++) {
      var v = vids[i];
      var u = typeof v === 'string' ? v : (v && v.url);
      var typ = v && v.type && v.type.name;
      if (!u || blockedUrl(u) || !/official webcast/i.test(typ || '') || !publisherOk(v, l)) continue;
      var emb = parseEmbed(u, (v && v.title) || missionName(l));
      if (emb) return emb;
    }
    return null;
  }
  function altEmbed(l) {
    var row = streamRow(l);
    var a = row && row.alternate;
    if (!a || !a.url || isRestricted(l)) return null;
    var emb = parseEmbed(a.url, a.credit || 'NASASpaceflight');
    if (!emb) return null;
    emb.channel = a.channel || 'https://www.youtube.com/@NASASpaceflight';
    return emb;
  }
  function stageHtml(emb, buttonText) {
    var title = emb.title || buttonText;
    if (emb.kind === 'youtube') {
      return '<div class="lw-stage"><button type="button" class="lw-play" data-kind="youtube" data-id="' + esc(emb.id) + '" data-title="' + esc(title) + '">' + esc(buttonText) + '</button></div>';
    }
    /* X does not allow its live broadcasts to be embedded on other sites, so the official X stream opens on X in a new tab. */
    return '<div class="lw-stage"><a class="lw-play" data-kind="x" href="' + esc(emb.url) + '" target="_blank" rel="noopener noreferrer" title="' + esc(title) + '">' + esc(buttonText) + ' \u2197</a></div>';
  }
  function playerHtml(l) {
    var off = officialEmbed(l);
    var alt = altEmbed(l);
    var html = '';
    if (off) html += stageHtml(off, ui.play);
    if (alt) {
      html += '<p class="lw-nsf">' + esc(off ? ui.altView : ui.nsf) + ' <a href="' + esc(alt.channel) + '" target="_blank" rel="noopener noreferrer">' + esc(ui.nsfChannel) + '</a></p>';
      html += stageHtml(alt, off ? ui.altView : ui.playNsf);
    }
    return html;
  }
  function loadXWidgets(stage) {
    function draw() {
      if (window.twttr && window.twttr.widgets) window.twttr.widgets.load(stage);
    }
    if (window.twttr && window.twttr.widgets) { draw(); return; }
    if (document.getElementById('lw-x-widgets')) {
      document.getElementById('lw-x-widgets').addEventListener('load', draw);
      return;
    }
    var s = document.createElement('script');
    s.id = 'lw-x-widgets';
    s.async = true;
    s.src = 'https://platform.twitter.com/widgets.js';
    s.onload = draw;
    document.body.appendChild(s);
  }
  function onPlay(e) {
    var b = e.target && e.target.closest && e.target.closest('.lw-play');
    if (!b || b.tagName === 'A') return;
    var stage = b.parentNode;
    var title = b.getAttribute('data-title') || 'Official live stream';
    if (b.getAttribute('data-kind') === 'youtube') {
      var id = b.getAttribute('data-id') || '';
      if (!/^[\w-]{6,}$/.test(id)) return;
      stage.innerHTML = '<iframe title="' + esc(title) + '" src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?rel=0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>';
      return;
    }
    var url = b.getAttribute('data-url') || '';
    if (!parseEmbed(url, title)) return;
    stage.innerHTML = '<blockquote class="twitter-tweet" data-dnt="true"><a href="' + esc(url) + '">' + esc(title) + '</a></blockquote>';
    loadXWidgets(stage);
  }
  function watchUrl(l) {
    if (isRestricted(l)) return null;
    var vids = [].concat((l && l.vid_urls) || [], (l && l.mission && l.mission.vid_urls) || []);
    for (var i = 0; i < vids.length; i++) {
      var v = vids[i];
      var u = typeof v === 'string' ? v : (v && v.url);
      var typ = v && v.type && v.type.name;
      if (u && !blockedUrl(u) && /official webcast/i.test(typ || '')) return u;
    }
    return agencyUrl(l);
  }
  function matchedPage(l) {
    var name = missionName(l);
    var desc = ((l.mission && l.mission.description) || '') + ' ' + name;
    for (var i = 0; i < PAGE_MATCH.length; i++) {
      if (PAGE_MATCH[i].re.test(name) || PAGE_MATCH[i].re.test(desc)) return PAGE_MATCH[i].page;
    }
    return null;
  }
  function watchBtn(l) {
    if (isRestricted(l)) return '<p class="lw-watch-note">' + esc(pk.watchRestricted) + '</p>';
    var u = watchUrl(l);
    var players = playerHtml(l);
    if (isStarship15(l)) {
      return players + '<p class="lw-acts"><a class="lw-watch" href="https://www.spacex.com/launches/starship-flight-15" target="_blank" rel="noopener noreferrer">' + esc(ui.officialSx) + '</a></p>';
    }
    if (!u) return players || ('<p class="lw-watch-note">' + esc(ui.watchTba) + '</p>');
    return players + '<p class="lw-acts"><a class="lw-watch" href="' + esc(u) + '" target="_blank" rel="noopener noreferrer">' + esc(ui.watchLive) + '</a></p>';
  }
  function goingHtml(l) {
    var c = classify(l);
    var lines = [];
    if (isStarship15(l)) {
      (STAR[lang] || STAR.en).forEach(function (s) { lines.push('<p>' + esc(s) + '</p>'); });
    } else {
      var purpose = purposeText(l);
      lines.push('<p><b>' + esc(missionName(l)) + '</b></p>');
      lines.push('<p>' + esc(purpose || ui.tba) + '</p>');
      lines.push('<p>' + esc((c && c.text) || t.detailsMissing) + '</p>');
      var page = matchedPage(l);
      if (page && c && c.kind === 'yes' && !isRestricted(l)) {
        lines.push('<p class="lw-blurb-link"><a href="' + esc(prefix + page) + '">' + esc(t.seeSolution) + '</a> · <a href="' + esc(prefix + 'Space.html#satmap') + '">' + esc(ui.onMap) + '</a></p>');
      }
    }
    var src = isStarship15(l) ? 'https://www.spacex.com/launches/starship-flight-15' : (isRestricted(l) ? null : watchUrl(l));
    var srcHtml = src ? '<a href="' + esc(src) + '" target="_blank" rel="noopener noreferrer">' + esc(pk.sources) + '</a>' : esc(t.srcLL2);
    return '<div class="lw-pay"><p class="lw-blurb-k">' + esc(ui.going) + '</p>' + lines.join('') + '<p class="lw-blurb-src">' + srcHtml + '</p></div>';
  }
  function localLine(iso) {
    if (!iso || isNaN(new Date(iso).getTime())) return esc(ui.tba);
    return esc(ui.yourTime) + ' ' + esc(fmt(iso, {
      weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZoneName: 'short'
    }));
  }
  function agencyUrl(l) {
    /* Policy: never return an outbound URL for RU/CN/KP/IR-led launches. */
    if (isRestricted(l)) return null;
    var urls = l.infoURLs || l.info_urls || [];
    for (var i = 0; i < urls.length; i++) {
      var u = typeof urls[i] === 'string' ? urls[i] : (urls[i] && urls[i].url);
      if (u && /^https?:\/\//i.test(u) && !blockedUrl(u)) return u;
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
  var DTC = {
    en: {
      both: 'Supports a Saving Planets solution — disaster alerts & future science lift',
      alerts: 'Supports a Saving Planets solution — disaster alerts',
      lift: 'Supports a Saving Planets solution — future science lift',
      bothBody: 'Direct-to-Cell emergency alerts (disaster communications) and low-cost heavy lift that can carry future Earth-science and planetary missions. SpaceX describes these V3 satellites as communications capacity, not Earth sensing.',
      alertBody: 'Direct-to-Cell emergency alerts (disaster communications). SpaceX describes the satellites as communications capacity, not Earth sensing.',
      liftBody: 'Low-cost heavy lift that can carry future Earth-science and planetary missions. This flight’s published payload is not described as Earth sensing unless the listing names a sensor.',
      otherBody: 'This payload has a confirmed disaster-communications role: emergency alerts when ground networks are down.'
    },
    fr: {
      both: 'Soutient une solution Saving Planets — alertes catastrophe et futur lancement scientifique',
      alerts: 'Soutient une solution Saving Planets — alertes catastrophe',
      lift: 'Soutient une solution Saving Planets — futur lancement scientifique',
      bothBody: 'Alertes d’urgence Direct-to-Cell (communications en cas de catastrophe) et un lanceur lourd à moindre coût qui peut emporter de futures missions de science de la Terre et de science planétaire. SpaceX décrit ces satellites V3 comme de la capacité de communication, pas comme des capteurs de la Terre.',
      alertBody: 'Alertes d’urgence Direct-to-Cell (communications en cas de catastrophe). SpaceX décrit ces satellites comme de la capacité de communication, pas comme des capteurs de la Terre.',
      liftBody: 'Lanceur lourd à moindre coût qui peut emporter de futures missions de science de la Terre et de science planétaire. La charge publiée de ce vol n’est pas décrite comme un capteur de la Terre, sauf si la fiche nomme un instrument.',
      otherBody: 'Cette charge a un rôle confirmé de communication en cas de catastrophe : des alertes d’urgence quand les réseaux au sol sont coupés.'
    },
    es: {
      both: 'Apoya una solución de Saving Planets — alertas de desastre y futuro transporte científico',
      alerts: 'Apoya una solución de Saving Planets — alertas de desastre',
      lift: 'Apoya una solución de Saving Planets — futuro transporte científico',
      bothBody: 'Alertas de emergencia Direct-to-Cell (comunicaciones de desastre) y un lanzador pesado de menor costo que puede llevar futuras misiones de ciencia de la Tierra y planetaria. SpaceX describe estos satélites V3 como capacidad de comunicaciones, no como sensores de la Tierra.',
      alertBody: 'Alertas de emergencia Direct-to-Cell (comunicaciones de desastre). SpaceX describe estos satélites como capacidad de comunicaciones, no como sensores de la Tierra.',
      liftBody: 'Lanzador pesado de menor costo que puede llevar futuras misiones de ciencia de la Tierra y planetaria. La carga publicada de este vuelo no se describe como un sensor de la Tierra, salvo que la ficha nombre un instrumento.',
      otherBody: 'Esta carga tiene un papel confirmado de comunicaciones de desastre: alertas de emergencia cuando las redes terrestres están caídas.'
    },
    ar: {
      both: 'يدعم حلًا من Saving Planets — تنبيهات الكوارث ورفع علمي مستقبلي',
      alerts: 'يدعم حلًا من Saving Planets — تنبيهات الكوارث',
      lift: 'يدعم حلًا من Saving Planets — رفع علمي مستقبلي',
      bothBody: 'تنبيهات الطوارئ Direct-to-Cell (اتصالات الكوارث) ورفع ثقيل منخفض التكلفة يمكنه حمل بعثات مستقبلية لعلوم الأرض والكواكب. تصف سبيس إكس أقمار V3 بأنها سعة اتصالات، وليست استشعارًا للأرض.',
      alertBody: 'تنبيهات الطوارئ Direct-to-Cell (اتصالات الكوارث). تصف سبيس إكس الأقمار بأنها سعة اتصالات، وليست استشعارًا للأرض.',
      liftBody: 'رفع ثقيل منخفض التكلفة يمكنه حمل بعثات مستقبلية لعلوم الأرض والكواكب. الحمولة المنشورة لهذه الرحلة ليست موصوفة كاستشعار للأرض، إلا إذا سمّت البطاقة جهازًا.',
      otherBody: 'لهذه الحمولة دور مؤكد في اتصالات الكوارث: تنبيهات طوارئ عندما تتعطل الشبكات الأرضية.'
    },
    it: {
      both: 'Sostiene una soluzione Saving Planets — allerte disastri e futuri lanci scientifici',
      alerts: 'Sostiene una soluzione Saving Planets — allerte disastri',
      lift: 'Sostiene una soluzione Saving Planets — futuri lanci scientifici',
      bothBody: 'Allerte di emergenza Direct-to-Cell (comunicazioni di disastro) e un lanciatore pesante a basso costo che può portare future missioni di scienza della Terra e planetaria. SpaceX descrive questi satelliti V3 come capacità di comunicazione, non come sensori della Terra.',
      alertBody: 'Allerte di emergenza Direct-to-Cell (comunicazioni di disastro). SpaceX descrive i satelliti come capacità di comunicazione, non come sensori della Terra.',
      liftBody: 'Lanciatore pesante a basso costo che può portare future missioni di scienza della Terra e planetaria. Il carico pubblicato di questo volo non è descritto come un sensore della Terra, salvo che la scheda nomini uno strumento.',
      otherBody: 'Questo carico ha un ruolo confermato di comunicazione in caso di disastro: allerte di emergenza quando le reti a terra sono giù.'
    },
    he: {
      both: 'תומך בפתרון של Saving Planets — התרעות אסון ושיגור עתידי למדע',
      alerts: 'תומך בפתרון של Saving Planets — התרעות אסון',
      lift: 'תומך בפתרון של Saving Planets — שיגור עתידי למדע',
      bothBody: 'התרעות חירום Direct-to-Cell (תקשורת אסון) ושיגור כבד בעלות נמוכה שיכול לשאת משימות עתידיות של מדעי כדור הארץ ומדעים פלנטריים. ספייס אקס מתארת את לווייני V3 כקיבולת תקשורת, לא כחישה של כדור הארץ.',
      alertBody: 'התרעות חירום Direct-to-Cell (תקשורת אסון). ספייס אקס מתארת את הלוויינים כקיבולת תקשורת, לא כחישה של כדור הארץ.',
      liftBody: 'שיגור כבד בעלות נמוכה שיכול לשאת משימות עתידיות של מדעי כדור הארץ ומדעים פלנטריים. המטען שפורסם לטיסה הזו אינו מתואר כחישה של כדור הארץ, אלא אם הרשומה מציינת מכשיר.',
      otherBody: 'למטען הזה יש תפקיד מאושר של תקשורת אסון: התרעות חירום כשרשתות הקרקע מושבתות.'
    }
  };
  function dtcPack() { return DTC[lang] || DTC.en; }
  function confirmedDisaster(l) {
    var blob = missionName(l) + ' ' + ((l.mission && l.mission.description) || '');
    return /starlink|direct[ -]?to[ -]?cell|wireless emergency alert|\bWEA\b/i.test(blob);
  }
  function specialClassify(l) {
    var d = dtcPack();
    var src = 'Sources: <a href="https://www.spacex.com/updates/starlink-disaster-response/" target="_blank" rel="noopener noreferrer">SpaceX, Direct to Cell</a>; <a href="https://starlink.com/public-files/DIRECT_TO_CELL_SERVICE_FEB_25.pdf" target="_blank" rel="noopener noreferrer">Starlink, Direct to Cell service (Feb 2025)</a>; <a href="https://www.spacex.com/launches/starship-flight-15" target="_blank" rel="noopener noreferrer">SpaceX, Starship Flight 15</a> (V3 is communications capacity).';
    if (isStarlink(l) && isStarship(l)) {
      return { kind: 'yes', label: d.both, text: d.bothBody, page: null, out: 'https://www.spacex.com/updates/starlink-disaster-response/', srcHtml: src };
    }
    if (isStarlink(l)) {
      return { kind: 'yes', label: d.alerts, text: d.alertBody, page: null, out: 'https://www.spacex.com/updates/starlink-disaster-response/', srcHtml: src };
    }
    if (confirmedDisaster(l)) {
      return { kind: 'yes', label: d.alerts, text: d.otherBody, page: null, out: agencyUrl(l), srcHtml: esc(t.srcLL2) };
    }
    if (isStarship(l)) {
      return { kind: 'yes', label: d.lift, text: d.liftBody, page: null, out: 'https://www.spacex.com/vehicles/starship', srcHtml: 'Sources: <a href="https://www.spacex.com/vehicles/starship" target="_blank" rel="noopener noreferrer">SpaceX Starship</a>.' };
    }
    return null;
  }


  /* Tight Earth / solar-system benefit lines for restricted-led launches that still map to a solution. */
  var RESTRICTED_WHY = {
    earth: 'Earth-observation knowledge that helps everyone understand and care for our shared planet.',
    ocean: 'Ocean-monitoring knowledge that helps everyone understand and care for our shared seas.',
    polar: 'Polar and ice knowledge that helps everyone understand and care for our shared climate system.',
    forest: 'Forest-monitoring knowledge that helps everyone understand and care for our shared living lands.',
    weather: 'Space-weather knowledge that helps everyone protect people and systems on our shared planet.',
    defense: 'Planetary-defense knowledge that helps everyone protect our shared home in the solar system.',
    space: 'Space-science knowledge that helps everyone understand Earth and our shared solar system.'
  };

  function finalize(c, restricted) {
    if (!c) return c;
    if (!restricted) return c;
    /* No outbound operator links, embeds, or their-domain sources — ever. */
    c.out = null;
    if (c.srcHtml) c.srcHtml = null;
    if (c.kind === 'yes') {
      var w = c._why || 'earth';
      c.text = RESTRICTED_WHY[w] || RESTRICTED_WHY.earth;
      /* Keep c.page (our solution only). */
    } else {
      /* Not relevant: plain text only, no link of any kind. */
      c.page = null;
      c.hub = null;
      c.out = null;
      if (c.kind === 'skip') {
        c.kind = 'no';
        c.label = t.no;
      }
      c.text = c.text || t.noSpin.other;
    }
    return c;
  }

  function classify(l) {
    var restricted = isRestricted(l);
    var spec = specialClassify(l);
    if (spec) return finalize(spec, restricted);
    var name = missionName(l);
    var typ = mtype(l);
    var desc = ((l.mission && l.mission.description) || '') + ' ' + name + ' ' + typ;
    var purpose = purposeText(l);

    for (var i = 0; i < PAGE_MATCH.length; i++) {
      var m = PAGE_MATCH[i];
      if (m.re.test(name) || m.re.test(desc)) {
        return finalize({
          kind: 'yes', label: t.yes, text: t.why[m.why] || t.why.earth,
          page: m.page, hub: m.hub, out: null, _why: m.why
        }, restricted);
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
      return finalize({ kind: 'yes', label: t.yes, text: t.why[why], page: hub, hub: hub, out: null, _why: why }, restricted);
    }
    if (/planetary science|planetary defence|planetary defense|asteroid|heliophysics|solar|astronomy|astrophysics|lunar science/i.test(typ + ' ' + desc)) {
      var w = /asteroid|defence|defense|neo|impactor/i.test(desc + typ) ? 'defense'
        : /solar|helio|space weather|coronal/i.test(desc + typ) ? 'weather' : 'space';
      var hub2 = w === 'defense' ? 'Planetary_Defense.html' : w === 'weather' ? 'Space_Weather.html' : 'Space.html';
      return finalize({ kind: 'yes', label: t.yes, text: t.why[w], page: hub2, hub: hub2, out: null, _why: w }, restricted);
    }

    if (/top secret|government\/top secret|classified/i.test(typ + ' ' + desc) || (!purpose && /government/i.test(typ))) {
      return finalize({ kind: 'unk', label: t.unk, text: t.noSpin.secret + ' ' + t.detailsMissing, page: null, out: agencyUrl(l) }, restricted);
    }
    if (!purpose && !typ) {
      return finalize({ kind: 'unk', label: t.unk, text: t.detailsMissing, page: null, out: agencyUrl(l) }, restricted);
    }

    var spinKey = 'other';
    if (/communication/i.test(typ) || /starlink|kuiper|amazon leo|oneweb|satnet|broadband/i.test(name + desc)) spinKey = 'communications';
    else if (/navigation|gps|gnss|irnss|galileo|beidou/i.test(typ + name)) spinKey = 'navigation';
    else if (/resupply|cargo|iss|cygnus|progress|dragon/i.test(typ + name) && !/science/i.test(typ)) spinKey = 'resupply';
    else if (/human|crew|crew dragon|starliner|shenzhou|gaganyaan/i.test(typ + name)) spinKey = 'human';

    return finalize({ kind: 'no', label: t.no, text: t.noSpin[spinKey] || t.noSpin.other, page: null, out: agencyUrl(l) }, restricted);
  }

  function blurbHtml(l) {
    var purpose = purposeText(l);
    var c = classify(l);
    var srcLine = (isRestricted(l) || !(c && c.srcHtml)) ? esc(t.srcLL2) : c.srcHtml;
    var purposeBlock = '<div class="lw-blurb-block"><p class="lw-blurb-k">' + esc(t.purpose) + '</p><p class="lw-blurb-t">' +
      esc(purpose || t.detailsMissing) + '</p>' +
      '<p class="lw-blurb-src">' + srcLine + '</p></div>';

    var link = '';
    if (c.kind === 'yes' && c.page) {
      link = '<p class="lw-blurb-link"><a class="lw-sol" href="' + esc(prefix + c.page) + '">' + esc(t.seeSolution) + '</a></p>';
    } else if (c.out && !isRestricted(l) && !blockedUrl(c.out)) {
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


  function showError() {
    if (timer) clearInterval(timer);
    nextEl.innerHTML = '<p class="lw-error">' + t.err + '</p>';
    listEl.innerHTML = '';
  }

  function tickCards() {
    var nodes = listEl.querySelectorAll('.lw-mini');
    for (var i = 0; i < nodes.length; i++) {
      var ms = new Date(nodes[i].getAttribute('data-net')).getTime();
      if (!isNaN(ms)) tick(ms, nodes[i]);
    }
  }
  /* Past T-0: show launch status instead of a countdown (e.g. "Launched today, 12:47 PM HST · In flight"). */
  function tick(netMs, el) {
    var diff = netMs - Date.now();
    if (diff <= 0) {
      var txt = FEED.statusText(el.getAttribute('data-net'), el.getAttribute('data-ab'));
      if (el.getAttribute('data-done') !== txt) {
        el.setAttribute('data-done', txt);
        el.innerHTML = '<p class="lw-done">' + esc(txt) + '</p>';
      }
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

  function abOf(l) { return (l && l.status && l.status.abbrev) || ''; }
  function render(data) {
    var r = FEED.filter((data && data.results) || [], Date.now());
    if (!r.length) { showError(); return; }

    var n = r[0];
    var status = n.status && n.status.abbrev ? ' · ' + esc(t.status) + ': ' + esc(n.status.abbrev) : '';
    var where = n.pad && n.pad.location && n.pad.location.name ? '<br>' + esc(n.pad.location.name) : '';
    nextEl.innerHTML =
      '<p class="lw-kicker">' + esc(FEED.isPast(n) ? FEED.recentLabel : t.next) + '</p>' +
      '<h3 class="lw-mission">' + esc(missionName(n)) + '</h3>' +
      '<p class="lw-meta">' + esc(provider(n)) + ' · ' + esc(rocket(n)) + '</p>' +
      '<p class="lw-when">' + esc(fmt(n.net, {
        weekday: 'short', month: 'short', day: 'numeric', year: 'numeric',
        hour: 'numeric', minute: '2-digit', timeZoneName: 'short'
      })) + status + where + '</p>' +
      '<p class="lw-local">' + localLine(n.net) + '</p>' +
      metaLine(n) +
      '<div class="lw-countdown" role="timer" aria-label="' + esc(t.next) + '" data-net="' + esc(n.net || '') + '" data-ab="' + esc(abOf(n)) + '" data-lid="' + esc(n.id || '') + '" data-watch="' + esc(watchUrl(n) || '') + '"></div>' +
      watchBtn(n) +
      '<div class="lw-blurbs">' + goingHtml(n) + blurbHtml(n) + '</div>';

    var cd = nextEl.querySelector('.lw-countdown');
    var netMs = new Date(n.net).getTime();
    if (timer) clearInterval(timer);
    if (isNaN(netMs)) { cd.innerHTML = ''; }
    else { tick(netMs, cd); timer = setInterval(function () { tick(netMs, cd); tickCards(); }, 1000); }
    tickCards();

    listEl.innerHTML = r.slice(1, 20).map(function (l) {
      var st = l.status && l.status.abbrev ? ' · ' + esc(l.status.abbrev) : '';
      return '<li class="lw-card" data-lid="' + esc(l.id || '') + '" data-watch="' + esc(watchUrl(l) || '') + '">' +
        '<div class="lw-card-top">' +
        '<span class="lw-l-name">' + esc(missionName(l)) +
        '<span class="lw-l-sub">' + esc(provider(l)) + ' · ' + esc(rocket(l)) + st + '</span></span>' +
        '<span class="lw-l-date">' + esc(fmt(l.net, { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' })) + '</span>' +
        '</div>' +
        '<p class="lw-local">' + localLine(l.net) + '</p>' +
        '<div class="lw-mini" data-net="' + esc(l.net || '') + '" data-ab="' + esc(abOf(l)) + '" role="timer"></div>' +
        metaLine(l) + watchBtn(l) +
        '<div class="lw-blurbs">' + goingHtml(l) + blurbHtml(l) + '</div></li>';
    }).join('');
    tickCards();
  }

  nextEl.addEventListener('click', onPlay);
  listEl.addEventListener('click', onPlay);
  FEED.load()
    .then(function (d) { return FEED.streams().then(function (sr) { STREAMS = sr || []; return d; }); })
    .then(function (d) { try { render(d); } catch (e) { showError(); } })
    .catch(function () { showError(); });
})();
