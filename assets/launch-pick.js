/* Launch picker. Same Launch Library 2 feed and 10-minute cache as launch-tracker.js.
   No invented dates: NET/TBD come from the listing. Vehicle history is only the sourced
   notes below. Russia, China, North Korea and Iran-led launches never get their sites. */
(function () {
  /* Feed: assets/launch-feed.js (upcoming + launches from the last day, Pacific/Honolulu). */
  var sel = document.getElementById('lw-pick');
  var panel = document.getElementById('lw-pick-panel');
  if (!sel || !panel) return;
  var lang = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase();
  var prefix = (location.pathname.indexOf('/' + lang + '/') >= 0) ? '../' : '';
  var EXCL = /roscosmos|russia|china|chinese|baikonur|plesetsk|vostochny|jiuquan|wenchang|xichang|taiyuan|haiyang|dongfeng|sohae|tonghae|korean committee|nada|korean people.?s|landspace|galactic energy|i-space|orienspace|deep blue aero|space pioneer|cas space|expace|casc|casic|khrunichev|progress rocket|kazakhstan|iran|islamic republic|iranian|ministry of defence of the russian|cnsa|calt/i;
  var BLOCKED = /(?:^|\.)(?:roscosmos\.ru|gov\.ru|mil\.ru|cnsa\.gov\.cn|cmse\.gov\.cn|calt\.com\.cn|casc\.com\.cn|casic\.com\.cn|spacechina\.com|clep\.org\.cn|irna\.ir|isa\.ir|isa\.gov\.ir)$/i;
  var UI = {
    en: { choose: 'Choose an upcoming launch', empty: 'No upcoming launches in the listing right now.', summary: 'Summary', mission: 'What this mission is', watch: 'Come back and watch', watchInvite: 'Come back and watch the live event. Times move, so check again close to liftoff.', watchMissing: 'This listing does not include a public livestream or info link we can share.', watchRestricted: 'We do not link a watch page for this launch.', history: 'A short history', historyMissing: 'A longer history of this vehicle is not on this page. The facts above are from the launch listing.', net: 'No earlier than', tbd: 'The date is still to be confirmed (TBD / NET).', sources: 'Sources', live: 'Official livestream or info', restricted: 'This launch is led by a program whose sites we do not link. We only say how this kind of mission can help Earth or the solar system, and we link our own solution page when one matches.', see: 'Open the solution page', ll2: 'Launch Library 2 (The Space Devs)' },
    fr: { choose: 'Choisir un lancement à venir', empty: 'Aucun lancement à venir dans la liste pour le moment.', summary: 'Résumé', mission: 'En quoi consiste la mission', watch: 'Revenir pour regarder', watchInvite: 'Revenez pour le direct. Les horaires bougent : revérifiez près du décollage.', watchMissing: 'Cette fiche n’indique pas de lien public de direct que nous pouvons partager.', watchRestricted: 'Nous ne proposons pas de lien pour suivre ce lancement.', history: 'Une courte histoire', historyMissing: 'Une histoire plus longue de cet engin n’est pas sur cette page. Les faits ci-dessus viennent de la fiche de lancement.', net: 'Pas avant', tbd: 'La date reste à confirmer (TBD / NET).', sources: 'Sources', live: 'Direct ou page officielle', restricted: 'Ce lancement est mené par un programme dont nous ne lions pas les sites. Nous disons seulement comment ce type de mission peut aider la Terre ou le système solaire, et nous renvoyons à notre page de solution quand elle correspond.', see: 'Ouvrir la page de la solution', ll2: 'Launch Library 2 (The Space Devs)' },
    es: { choose: 'Elige un lanzamiento próximo', empty: 'Ahora mismo la lista no tiene lanzamientos próximos.', summary: 'Resumen', mission: 'Qué es esta misión', watch: 'Vuelve para verlo', watchInvite: 'Vuelve para el evento en vivo. Los horarios cambian: revísalo cerca del despegue.', watchMissing: 'Esta ficha no incluye un enlace público de transmisión que podamos compartir.', watchRestricted: 'No ofrecemos un enlace para ver este lanzamiento.', history: 'Una historia breve', historyMissing: 'Una historia más larga de este vehículo no está en esta página. Los datos de arriba salen de la ficha de lanzamiento.', net: 'No antes de', tbd: 'La fecha sigue por confirmar (TBD / NET).', sources: 'Fuentes', live: 'Transmisión o ficha oficial', restricted: 'Este lanzamiento lo dirige un programa cuyos sitios no enlazamos. Solo decimos cómo este tipo de misión puede ayudar a la Tierra o al sistema solar, y enlazamos nuestra página de solución cuando encaja.', see: 'Abrir la página de la solución', ll2: 'Launch Library 2 (The Space Devs)' },
    ar: { choose: 'اختر إطلاقاً قادماً', empty: 'لا توجد إطلاقات قادمة في القائمة الآن.', summary: 'ملخص', mission: 'ما هذه المهمة', watch: 'عُد للمشاهدة', watchInvite: 'عُد لمشاهدة البث المباشر. المواعيد تتغير، فراجعها قرب الإقلاع.', watchMissing: 'لا تتضمن هذه البطاقة رابط بث عام يمكننا مشاركته.', watchRestricted: 'لا نعرض رابط مشاهدة لهذا الإطلاق.', history: 'تاريخ موجز', historyMissing: 'لا يوجد في هذه الصفحة تاريخ أطول لهذه المركبة. الحقائق أعلاه من بطاقة الإطلاق.', net: 'ليس قبل', tbd: 'التاريخ ما زال بانتظار التأكيد (TBD / NET).', sources: 'المصادر', live: 'بث أو صفحة رسمية', restricted: 'يقود هذا الإطلاق برنامج لا نربط بمواقعه. نذكر فقط كيف يمكن لهذا النوع من المهام أن يفيد الأرض أو المجموعة الشمسية، ونربط بصفحة حلّنا عندما تنطبق.', see: 'افتح صفحة الحل', ll2: 'Launch Library 2 (The Space Devs)' },
    it: { choose: 'Scegli un lancio in programma', empty: 'In questo momento l’elenco non ha lanci in programma.', summary: 'Sintesi', mission: 'Che cos’è questa missione', watch: 'Torna a guardare', watchInvite: 'Torna per l’evento in diretta. Gli orari si spostano: ricontrolla vicino al decollo.', watchMissing: 'Questa scheda non include un link pubblico di diretta che possiamo condividere.', watchRestricted: 'Non offriamo un link per seguire questo lancio.', history: 'Una breve storia', historyMissing: 'Una storia più lunga di questo veicolo non è in questa pagina. I fatti sopra vengono dalla scheda di lancio.', net: 'Non prima del', tbd: 'La data è ancora da confermare (TBD / NET).', sources: 'Fonti', live: 'Diretta o pagina ufficiale', restricted: 'Questo lancio è guidato da un programma di cui non colleghiamo i siti. Diciamo solo come questo tipo di missione può aiutare la Terra o il sistema solare, e colleghiamo la nostra pagina di soluzione quando corrisponde.', see: 'Apri la pagina della soluzione', ll2: 'Launch Library 2 (The Space Devs)' },
    he: { choose: 'בחרו שיגור קרוב', empty: 'אין כרגע שיגורים קרובים ברשימה.', summary: 'תקציר', mission: 'מהי המשימה', watch: 'חזרו לצפות', watchInvite: 'חזרו לאירוע החי. הזמנים זזים, אז בדקו שוב סמוך להמראה.', watchMissing: 'ברשומה הזו אין קישור שידור פומבי שאפשר לשתף.', watchRestricted: 'איננו מציעים קישור צפייה לשיגור הזה.', history: 'היסטוריה קצרה', historyMissing: 'היסטוריה ארוכה יותר של הרכב הזה אינה בעמוד. העובדות למעלה לקוחות מרשומת השיגור.', net: 'לא לפני', tbd: 'התאריך עדיין לאישור (TBD / NET).', sources: 'מקורות', live: 'שידור או עמוד רשמי', restricted: 'את השיגור הזה מוביל גוף שאת אתריו איננו מקשרים. אנו מציינים רק איך סוג משימה כזה יכול לעזור לכדור הארץ או למערכת השמש, ומקשרים לעמוד הפתרון שלנו כשיש התאמה.', see: 'פתחו את עמוד הפתרון', ll2: 'Launch Library 2 (The Space Devs)' }
  };
  var u = UI[lang] || UI.en;
  var label = document.querySelector('label[for="lw-pick"]');
  if (label) label.textContent = u.choose;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function nameOf(l) {
    if (l.mission && l.mission.name) return l.mission.name;
    var p = String(l.name || '').split('|');
    return (p[1] || p[0] || 'Mission').trim();
  }
  function provider(l) { return (l.launch_service_provider && l.launch_service_provider.name) || ''; }
  function rocket(l) { return (l.rocket && l.rocket.configuration && l.rocket.configuration.name) || ''; }
  function restricted(l) {
    var loc = (l.pad && l.pad.location && l.pad.location.name) || '';
    var cc = (l.pad && l.pad.country && (l.pad.country.alpha_3_code || l.pad.country.alpha_2_code)) || '';
    if (/^(RUS|CHN|PRK|IRN|RU|CN|KP|IR)$/i.test(cc)) return true;
    return EXCL.test(loc + ' | ' + provider(l) + ' ' + rocket(l));
  }
  function badUrl(url) {
    if (!url || !/^https?:\/\//i.test(url)) return true;
    try {
      var h = new URL(url).hostname.replace(/^www\./i, '');
      if (BLOCKED.test(h)) return true;
      if (/\.(?:ru|xn--p1ai|cn|xn--fiqs8s|ir|kp)$/i.test(h)) return true;
    } catch (e) { return true; }
    return false;
  }
  function urlsOf(l) {
    if (restricted(l)) return [];
    var bags = [l.vidURLs, l.vid_urls, l.infoURLs, l.info_urls];
    var out = [], seen = {};
    bags.forEach(function (bag) {
      (bag || []).forEach(function (item) {
        var href = typeof item === 'string' ? item : (item && (item.url || item.link));
        if (!href || seen[href] || badUrl(href)) return;
        seen[href] = 1;
        out.push(href);
      });
    });
    return out.slice(0, 2);
  }
  function whenLine(l) {
    var st = ((l.status && (l.status.name || l.status.abbrev)) || '').toLowerCase();
    if (!l.net || /tbd|tbc|to be|confirm/.test(st)) return u.tbd;
    var d = new Date(l.net);
    if (isNaN(d)) return u.tbd;
    if (window.SPLaunchFeed && window.SPLaunchFeed.isPast(l)) {
      if (window.SPLaunchFeed.statusLine) return window.SPLaunchFeed.statusLine(l);
      return window.SPLaunchFeed.statusText(l.net, l.status && l.status.abbrev);
    }
    return u.net + ' ' + d.toLocaleString(lang === 'en' ? undefined : lang, {
      weekday: 'short', month: 'short', day: 'numeric', year: 'numeric',
      hour: 'numeric', minute: '2-digit', timeZoneName: 'short'
    });
  }
  function purpose(l) {
    var d = l.mission && l.mission.description ? String(l.mission.description).replace(/\s+/g, ' ').trim() : '';
    if (!d) return '';
    if (d.length > 420) {
      var cut = d.lastIndexOf('.', 380);
      d = (cut > 140 ? d.slice(0, cut + 1) : d.slice(0, 380).replace(/\s+\S*$/, '') + '…');
    }
    return d;
  }
  function solution(l) {
    var blob = nameOf(l) + ' ' + ((l.mission && l.mission.description) || '') + ' ' + ((l.mission && l.mission.type) || '');
    var rows = [
      [/NISAR/i, 'NISAR.html'], [/SWOT/i, 'SWOT.html'], [/Sentinel-6/i, 'Sentinel-6B.html'],
      [/ICESat-2/i, 'ICESat-2.html'], [/\bPACE\b/i, 'PACE.html'], [/GOES-?19|GOES-U/i, 'GOES-19.html'],
      [/NEO Surveyor/i, 'NEO_Surveyor.html'], [/\bHera\b/i, 'Hera.html'], [/Europa Clipper/i, 'Europa_Clipper.html'],
      [/FireSat/i, 'FireSat.html'], [/earth observation|earth science|remote sensing/i, 'Earth_Observation.html'],
      [/space weather|heliophysics/i, 'Space_Weather.html'], [/planetary defense|asteroid/i, 'Planetary_Defense.html']
    ];
    for (var i = 0; i < rows.length; i++) if (rows[i][0].test(blob)) return rows[i][1];
    return '';
  }
  /* Official pages only. Dates below are the ones those pages state. */
  var HIST = [
    { re: /starship|super heavy/i, items: {
      en: [
        ['SpaceX describes Starship and Super Heavy as a fully reusable system designed to carry crew and cargo to Earth orbit, the Moon, Mars and beyond, with more than 100 metric tonnes to orbit. Super Heavy uses 33 methane-oxygen Raptor engines and is designed to fly back and be caught by the launch tower.', 'https://www.spacex.com/vehicles/starship/', 'SpaceX, Starship'],
        ['SpaceX lists the first integrated flight test on April 20, 2023, from Starbase, Texas. On the fifth flight test, October 13, 2024, SpaceX says the Super Heavy booster was caught by the tower arms and Starship splashed down in the Indian Ocean.', 'https://www.spacex.com/launches/starship-flight-5', 'SpaceX, fifth flight test'],
        ['SpaceX’s flight-test index lists later flights through Flight 14 on September 28, 2026, which it calls the first orbital Starship flight and the first to place Starlink V3 satellites into orbit. This page does not add results after that index.', 'https://www.spacex.com/content/starship-flight-tests', 'SpaceX, Starship flight tests']
      ],
      fr: [
        ['SpaceX décrit Starship et Super Heavy comme un système entièrement réutilisable, conçu pour emporter équipage et cargo vers l’orbite terrestre, la Lune, Mars et au-delà, avec plus de 100 tonnes vers l’orbite. Super Heavy a 33 moteurs Raptor méthane-oxygène et doit revenir se faire attraper par la tour.', 'https://www.spacex.com/vehicles/starship/', 'SpaceX, Starship'],
        ['SpaceX date le premier vol intégré du 20 avril 2023, depuis Starbase, au Texas. Au cinquième essai, le 13 octobre 2024, SpaceX indique que le booster a été attrapé par les bras de la tour et que Starship s’est posé dans l’océan Indien.', 'https://www.spacex.com/launches/starship-flight-5', 'SpaceX, cinquième essai'],
        ['L’index des essais de SpaceX va jusqu’au vol 14, le 28 septembre 2026, présenté comme le premier vol orbital de Starship et le premier à placer des satellites Starlink V3 en orbite. Cette page n’ajoute pas de résultat après cet index.', 'https://www.spacex.com/content/starship-flight-tests', 'SpaceX, essais Starship']
      ],
      es: [
        ['SpaceX describe Starship y Super Heavy como un sistema totalmente reutilizable para llevar tripulación y carga a la órbita terrestre, la Luna, Marte y más allá, con más de 100 toneladas a órbita. Super Heavy usa 33 motores Raptor de metano y oxígeno y está diseñado para volver y ser atrapado por la torre.', 'https://www.spacex.com/vehicles/starship/', 'SpaceX, Starship'],
        ['SpaceX fecha el primer vuelo integrado el 20 de abril de 2023, desde Starbase, Texas. En el quinto ensayo, el 13 de octubre de 2024, SpaceX dice que la torre atrapó el propulsor y que Starship amerizó en el océano Índico.', 'https://www.spacex.com/launches/starship-flight-5', 'SpaceX, quinto ensayo'],
        ['El índice de ensayos de SpaceX llega al vuelo 14, el 28 de septiembre de 2026, que llama el primer vuelo orbital de Starship y el primero en poner satélites Starlink V3 en órbita. Esta página no añade resultados posteriores a ese índice.', 'https://www.spacex.com/content/starship-flight-tests', 'SpaceX, ensayos de Starship']
      ],
      ar: [
        ['تصف SpaceX مركبة Starship ومعزز Super Heavy بأنهما نظام قابل لإعادة الاستخدام بالكامل، مصمم لنقل الطاقم والحمولة إلى مدار الأرض والقمر والمريخ وما بعدهما، بأكثر من 100 طن إلى المدار. يستخدم Super Heavy 33 محرك Raptor بالميثان والأكسجين، ومصمم ليعود فتلتقطه برج الإطلاق.', 'https://www.spacex.com/vehicles/starship/', 'SpaceX, Starship'],
        ['تؤرخ SpaceX أول رحلة متكاملة في 20 أبريل 2023 من Starbase في تكساس. وفي التجربة الخامسة في 13 أكتوبر 2024 تقول إن البرج التقط المعزز وإن Starship هبطت في المحيط الهندي.', 'https://www.spacex.com/launches/starship-flight-5', 'SpaceX، التجربة الخامسة'],
        ['يصل فهرس تجارب SpaceX إلى الرحلة 14 في 28 سبتمبر 2026، وتصفها بأنها أول رحلة مدارية لـ Starship وأول رحلة تضع أقمار Starlink V3 في المدار. لا تضيف هذه الصفحة نتائج بعد ذلك الفهرس.', 'https://www.spacex.com/content/starship-flight-tests', 'SpaceX، تجارب Starship']
      ],
      it: [
        ['SpaceX descrive Starship e Super Heavy come un sistema completamente riutilizzabile, pensato per portare equipaggio e carico in orbita terrestre, sulla Luna, su Marte e oltre, con oltre 100 tonnellate in orbita. Super Heavy usa 33 motori Raptor a metano e ossigeno ed è progettato per tornare ed essere preso dalla torre.', 'https://www.spacex.com/vehicles/starship/', 'SpaceX, Starship'],
        ['SpaceX data il primo volo integrato al 20 aprile 2023, da Starbase, in Texas. Nel quinto test, il 13 ottobre 2024, SpaceX dice che la torre ha preso il booster e che Starship è ammarata nell’oceano Indiano.', 'https://www.spacex.com/launches/starship-flight-5', 'SpaceX, quinto test'],
        ['L’indice dei test di SpaceX arriva al volo 14, il 28 settembre 2026, che chiama il primo volo orbitale di Starship e il primo a mettere in orbita satelliti Starlink V3. Questa pagina non aggiunge risultati dopo quell’indice.', 'https://www.spacex.com/content/starship-flight-tests', 'SpaceX, test di Starship']
      ],
      he: [
        ['SpaceX מתארת את Starship ואת Super Heavy כמערכת רב-פעמית לגמרי, שנועדה לשאת צוות ומטען למסלול סביב כדור הארץ, לירח, למאדים ומעבר להם, עם יותר מ-100 טונות למסלול. ל-Super Heavy יש 33 מנועי Raptor על מתאן וחמצן, והוא מתוכנן לחזור ולהיתפס במגדל.', 'https://www.spacex.com/vehicles/starship/', 'SpaceX, Starship'],
        ['SpaceX מתארכת את הטיסה המשולבת הראשונה ל-20 באפריל 2023, מ-Starbase בטקסס. בטיסת הניסוי החמישית, ב-13 באוקטובר 2024, SpaceX אומרת שהמגדל תפס את המאיץ ו-Starship נחתה באוקיינוס ההודי.', 'https://www.spacex.com/launches/starship-flight-5', 'SpaceX, הטיסה החמישית'],
        ['אינדקס טיסות הניסוי של SpaceX מגיע עד טיסה 14 ב-28 בספטמבר 2026, שהיא קוראת לה הטיסה המסלולית הראשונה של Starship והראשונה שהציבה לווייני Starlink V3 במסלול. העמוד הזה לא מוסיף תוצאות אחרי האינדקס.', 'https://www.spacex.com/content/starship-flight-tests', 'SpaceX, טיסות ניסוי']
      ]
    }},
    { re: /falcon heavy/i, items: {
      en: [['SpaceX describes Falcon Heavy as a heavy-lift rocket made of three Falcon 9 first-stage cores, for larger payloads than a single Falcon 9.', 'https://www.spacex.com/vehicles/falcon-heavy/', 'SpaceX, Falcon Heavy']],
      fr: [['SpaceX décrit Falcon Heavy comme une fusée lourde faite de trois premiers étages de Falcon 9, pour des charges plus grandes qu’une seule Falcon 9.', 'https://www.spacex.com/vehicles/falcon-heavy/', 'SpaceX, Falcon Heavy']],
      es: [['SpaceX describe Falcon Heavy como un cohete pesado hecho de tres primeras etapas de Falcon 9, para cargas mayores que un solo Falcon 9.', 'https://www.spacex.com/vehicles/falcon-heavy/', 'SpaceX, Falcon Heavy']],
      ar: [['تصف SpaceX صاروخ Falcon Heavy بأنه صاروخ رفع ثقيل من ثلاثة مراحل أولى من Falcon 9، لحمولات أكبر من Falcon 9 واحد.', 'https://www.spacex.com/vehicles/falcon-heavy/', 'SpaceX, Falcon Heavy']],
      it: [['SpaceX descrive Falcon Heavy come un razzo pesante fatto di tre primi stadi Falcon 9, per carichi maggiori di un singolo Falcon 9.', 'https://www.spacex.com/vehicles/falcon-heavy/', 'SpaceX, Falcon Heavy']],
      he: [['SpaceX מתארת את Falcon Heavy כרקטת שיגור כבדה משלושה שלבים ראשונים של Falcon 9, למטענים גדולים יותר מ-Falcon 9 יחיד.', 'https://www.spacex.com/vehicles/falcon-heavy/', 'SpaceX, Falcon Heavy']]
    }},
    { re: /falcon 9|falcon-9/i, items: {
      en: [['SpaceX describes Falcon 9 as a reusable two-stage rocket for people and payloads to Earth orbit and beyond, and as the first orbital-class rocket capable of reflight. The first stage uses nine Merlin engines with liquid oxygen and rocket-grade kerosene.', 'https://www.spacex.com/vehicles/falcon-9/', 'SpaceX, Falcon 9']],
      fr: [['SpaceX décrit Falcon 9 comme une fusée réutilisable à deux étages pour des personnes et des charges vers l’orbite terrestre et au-delà, et comme la première fusée de classe orbitale capable de revoler. Le premier étage a neuf moteurs Merlin à oxygène liquide et kérosène.', 'https://www.spacex.com/vehicles/falcon-9/', 'SpaceX, Falcon 9']],
      es: [['SpaceX describe Falcon 9 como un cohete reutilizable de dos etapas para personas y cargas a la órbita terrestre y más allá, y como el primer cohete de clase orbital capaz de volar de nuevo. La primera etapa usa nueve motores Merlin con oxígeno líquido y queroseno.', 'https://www.spacex.com/vehicles/falcon-9/', 'SpaceX, Falcon 9']],
      ar: [['تصف SpaceX صاروخ Falcon 9 بأنه صاروخ قابل لإعادة الاستخدام من مرحلتين لنقل الأشخاص والحمولات إلى مدار الأرض وما بعده، وأول صاروخ من فئة مدارية يستطيع الطيران مجددًا. المرحلة الأولى فيها تسعة محركات Merlin بالأكسجين السائل والكيروسين.', 'https://www.spacex.com/vehicles/falcon-9/', 'SpaceX, Falcon 9']],
      it: [['SpaceX descrive Falcon 9 come un razzo riutilizzabile a due stadi per persone e carichi verso l’orbita terrestre e oltre, e come il primo razzo di classe orbitale capace di rivolare. Il primo stadio usa nove motori Merlin a ossigeno liquido e cherosene.', 'https://www.spacex.com/vehicles/falcon-9/', 'SpaceX, Falcon 9']],
      he: [['SpaceX מתארת את Falcon 9 כרקטה דו-שלבית רב-פעמית לאנשים ולמטענים למסלול סביב כדור הארץ ומעבר לו, וכרקטה המסלולית הראשונה שיכולה לטוס שוב. בשלב הראשון תשעה מנועי Merlin על חמצן נוזלי וקרוסין.', 'https://www.spacex.com/vehicles/falcon-9/', 'SpaceX, Falcon 9']]
    }}
  ];
  function history(l) {
    if (restricted(l)) return null;
    var blob = rocket(l) + ' ' + nameOf(l) + ' ' + provider(l);
    for (var i = 0; i < HIST.length; i++) {
      if (HIST[i].re.test(blob)) return HIST[i].items[lang] || HIST[i].items.en;
    }
    return null;
  }
  function show(l) {
    if (!l) { panel.hidden = true; panel.innerHTML = ''; return; }
    var rest = restricted(l);
    var links = urlsOf(l).map(function (href) {
      return '<p><a href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">' + esc(u.live) + '</a></p>';
    }).join('');
    var watch = rest ? '<p>' + esc(u.watchRestricted) + '</p>' : (links || '<p>' + esc(u.watchMissing) + '</p>');
    var sol = solution(l);
    var solHtml = sol ? '<p><a href="' + esc(prefix + sol) + '">' + esc(u.see) + '</a></p>' : '';
    var hist = history(l);
    var histHtml;
    if (rest) histHtml = '<p>' + esc(u.restricted) + '</p>' + solHtml;
    else if (!hist) histHtml = '<p>' + esc(u.historyMissing) + '</p><p class="lw-pick-src">' + esc(u.sources) + ': ' + esc(u.ll2) + '</p>';
    else histHtml = hist.map(function (row) {
      return '<p>' + esc(row[0]) + '</p><p class="lw-pick-src">' + esc(u.sources) + ': <a href="' + esc(row[1]) + '" target="_blank" rel="noopener noreferrer">' + esc(row[2]) + '</a></p>';
    }).join('');
    var mission = purpose(l);
    panel.hidden = false;
    panel.innerHTML =
      '<h3>' + esc(nameOf(l)) + '</h3>' +
      '<p>' + esc([provider(l), rocket(l)].filter(Boolean).join(' · ')) + '</p>' +
      '<p>' + esc(whenLine(l)) + '</p>' +
      '<h4>' + esc(u.summary) + '</h4><p>' + esc(nameOf(l) + (rocket(l) ? ' — ' + rocket(l) : '') + '. ' + whenLine(l)) + '</p>' +
      '<h4>' + esc(u.mission) + '</h4><p>' + esc(mission || u.historyMissing) + '</p><p class="lw-pick-src">' + esc(u.sources) + ': ' + esc(u.ll2) + '</p>' +
      '<h4>' + esc(u.watch) + '</h4><p>' + esc(u.watchInvite) + '</p>' + watch +
      '<h4>' + esc(u.history) + '</h4>' + histHtml + solHtml;
  }
  var byId = {};
  function fill(data) {
    var rows = window.SPLaunchFeed.filter((data && data.results) || [], Date.now());
    byId = {};
    if (!rows.length) {
      sel.innerHTML = '<option value="">' + esc(u.empty) + '</option>';
      show(null);
      return;
    }
    var star = 0;
    sel.innerHTML = rows.map(function (l, i) {
      var id = l.id || String(i);
      byId[id] = l;
      var blob = rocket(l) + ' ' + nameOf(l);
      if (/starship/i.test(blob)) star = i;
      var when = whenLine(l);
      return '<option value="' + esc(id) + '">' + esc(nameOf(l) + (rocket(l) ? ' — ' + rocket(l) : '') + ' — ' + when) + '</option>';
    }).join('');
    sel.selectedIndex = star;
    show(rows[star]);
  }
  sel.addEventListener('change', function () { show(byId[sel.value] || null); });
  if (!window.SPLaunchFeed) return;
  window.SPLaunchFeed.load().then(fill).catch(function () {
    sel.innerHTML = '<option value="">' + esc(u.empty) + '</option>';
  });
})();
