#!/usr/bin/env node
/* Weekly Saving Planets Brief: builds one issue per language (EN/FR/ES/AR) and saves it as a DRAFT campaign
   in MailerLite for the matching group. NEVER sends or schedules.
   Usage: node scripts/newsletter-draft.js [--dry-run] [--update] [--days 7] [--lang en,fr]
   API key: read at runtime from $MAILERLITE_KEY_FILE (default ~/.mailerlite_key). Never commit or print it.
   Output HTML is also written to /tmp/newsletter-<date>-<lang>.html for review. */
const fs = require('fs'), path = require('path'), os = require('os'), { execSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..'), SITE = 'https://www.savingplanets.com/', API = 'https://connect.mailerlite.com/api';
const GROUPS = { en: '201062857381512972', fr: '201062857692939304', es: '201062857966617859', ar: '201062858265462233' };
const LANG_IDS = { en: 4, fr: 6, es: 8, ar: 23 };  // MailerLite language_id (GET /campaigns/languages): sets unsubscribe/footer template language
const UPDATE = process.argv.includes('--update');  // --update: rewrite content of this issue's existing drafts in place (same facts/joke; rotation not advanced)
const FROM = { name: 'Saving Planets', email: 'newsletter@savingplanets.com' };
const args = process.argv.slice(2), DRY = args.includes('--dry-run');
const DAYS = +(args[args.indexOf('--days') + 1] || 0) || 7;
const LANGS = args.includes('--lang') ? args[args.indexOf('--lang') + 1].split(',') : ['en', 'fr', 'es', 'ar'];
const today = new Date(), iso = new Date(today.getTime() - 10 * 36e5).toISOString().slice(0, 10); // HST date
const CAP = 3; // max new solutions shown per hub
const JOKES = ["Why did the sun go to school? To get a little brighter.","How do you throw a party in space? You planet.","Why did the cow go to outer space? To visit the Milky Way.","What did Mars say to Saturn? Give me a ring sometime.","Why is the moon so broke? It's down to its last quarter.","How does the solar system hold up its pants? With an asteroid belt.","Why don't astronauts get hungry after blasting off? They just had a big launch.","What kind of music do planets like? Neptunes.","Why did the astronaut break up with their partner? They needed space.","How do you know when the moon has had enough to eat? When it's full.","What do you call a tick on the moon? A luna-tick.","Why couldn't the astronaut book a room on the moon? It was full.","What's an astronaut's favorite part of a computer? The space bar.","What did the alien say to the garden? Take me to your weeder.","Why did Pluto break up with the Sun? It needed more space after being demoted.","How do you organize a space party? You planet ahead.","What's a light-year? Like a regular year, but with fewer calories.","Why did the star get in trouble at school? It was caught twinkling in class.","What do planets read in their spare time? Comet books.","Why is Saturn so good at keeping secrets? It has rings of trust.","What holds the moon up? Moonbeams.","Where do astronauts keep their sandwiches? In a launch box.","What did one asteroid say to the other? Nothing, asteroids can't talk. But they rock.","Why did the comet win the race? It had a great tail wind.","What do you call a loony spaceman? An astro-nut.","How do astronauts serve drinks? In sunglasses.","Why did the satellite stay calm? It knew how to orbit its problems.","What's the Earth's favorite type of music? Rock, but only the classic layers.","Why did the meteor go to therapy? It had a crushing impact on everyone.","What did the Big Dipper say to the Little Dipper? Stop following me around."]; // EN dad jokes; translations (puns adapted) in JOKES_T
const JOKES_T = {"fr": ["Pourquoi le Soleil est-il allé à l'école ? Pour devenir encore plus brillant.", "Comment organise-t-on une fête dans l'espace ? On la planète à l'avance.", "Pourquoi la vache est-elle allée dans l'espace ? Pour voir la Voie lactée.", "Qu'a dit Mars à Saturne ? Passe-moi un coup d'anneau un de ces jours.", "Pourquoi la Lune est-elle fauchée ? Elle en est à son dernier quartier.", "Comment le système solaire tient-il son pantalon ? Avec une ceinture d'astéroïdes.", "Pourquoi les astronautes n'ont-ils pas faim après le décollage ? Ils viennent de faire un gros lancement.", "Quelle musique préfèrent les planètes ? Celle de Nep-tune.", "Pourquoi l'astronaute a-t-il rompu ? Il avait besoin d'espace.", "Comment sait-on que la Lune a assez mangé ? Quand elle est pleine.", "Comment appelle-t-on un fou sur la Lune ? Un lunatique.", "Pourquoi l'astronaute n'a-t-il pas trouvé d'hôtel sur la Lune ? Elle était pleine.", "Quelle est la touche préférée d'un astronaute ? La barre d'espace.", "Qu'a dit l'extraterrestre au potager ? Conduisez-moi à votre jardinier en chef.", "Pourquoi Pluton a-t-elle quitté le Soleil ? Après sa rétrogradation, elle voulait prendre ses distances.", "Comment prépare-t-on une soirée spatiale ? On la planète bien à l'avance.", "Qu'est-ce qu'une année-lumière ? Une année normale, mais allégée en calories.", "Pourquoi l'étoile a-t-elle été punie ? On l'a surprise à scintiller en classe.", "Que lisent les planètes pendant leur temps libre ? Des comètes illustrées.", "Pourquoi Saturne garde-t-elle si bien les secrets ? Elle a le sens de l'anneau-neur.", "Qu'est-ce qui tient la Lune en l'air ? Les rayons de lune.", "Où les astronautes rangent-ils leurs sandwiches ? Dans leur boîte de lancement.", "Que s'est dit un astéroïde à un autre ? Rien, les astéroïdes ne parlent pas. Mais ils sont solides comme le roc.", "Pourquoi la comète a-t-elle gagné la course ? Elle avait la queue dans le vent.", "Comment appelle-t-on un astronaute farfelu ? Un astro-zinzin.", "Comment les astronautes servent-ils les boissons ? Dans des soucoupes volantes.", "Pourquoi le satellite restait-il calme ? Il savait mettre ses problèmes en orbite.", "Quelle est la musique préférée de la Terre ? Le rock, en couches bien classiques.", "Pourquoi le météore est-il allé chez le psy ? Il avait un impact écrasant sur tout le monde.", "Qu'a dit la Grande Ourse à la Petite Ourse ? Arrête de me suivre partout."], "es": ["¿Por qué el Sol fue a la escuela? Para ser todavía más brillante.", "¿Cómo se organiza una fiesta en el espacio? Se planeta con tiempo.", "¿Por qué la vaca viajó al espacio? Para visitar la Vía Láctea.", "¿Qué le dijo Marte a Saturno? Dame un anillazo cuando puedas.", "¿Por qué la Luna está sin dinero? Va por su último cuarto.", "¿Cómo se sujeta los pantalones el sistema solar? Con un cinturón de asteroides.", "¿Por qué los astronautas no tienen hambre tras el despegue? Porque acaban de tener un gran lanzamiento.", "¿Qué música les gusta a los planetas? La de Nep-tuno.", "¿Por qué el astronauta terminó con su pareja? Necesitaba espacio.", "¿Cómo sabes que la Luna ya comió bastante? Cuando está llena.", "¿Cómo se llama un loco en la Luna? Un lunático.", "¿Por qué el astronauta no encontró hotel en la Luna? Estaba llena.", "¿Cuál es la tecla favorita de un astronauta? La barra espaciadora.", "¿Qué le dijo el extraterrestre al huerto? Llévame con tu jardinero.", "¿Por qué Plutón dejó al Sol? Tras perder su categoría, necesitaba más espacio.", "¿Cómo se prepara una fiesta espacial? Se planeta con antelación.", "¿Qué es un año luz? Un año normal, pero con menos calorías.", "¿Por qué castigaron a la estrella? La pillaron titilando en clase.", "¿Qué leen los planetas en su tiempo libre? Cometas ilustrados.", "¿Por qué Saturno guarda tan bien los secretos? Porque tiene anillos de confianza.", "¿Qué sostiene a la Luna? Los rayos de luna.", "¿Dónde guardan los astronautas sus bocadillos? En la caja de lanzamiento.", "¿Qué le dijo un asteroide a otro? Nada, los asteroides no hablan. Pero son unas rocas.", "¿Por qué ganó la carrera el cometa? Tenía la cola a favor del viento.", "¿Cómo se llama un astronauta chiflado? Un astro-chalado.", "¿Cómo sirven las bebidas los astronautas? En platillos voladores.", "¿Por qué el satélite estaba tan tranquilo? Sabía poner sus problemas en órbita.", "¿Cuál es la música favorita de la Tierra? El rock, en capas clásicas.", "¿Por qué el meteoro fue a terapia? Causaba un impacto aplastante en todos.", "¿Qué le dijo la Osa Mayor a la Osa Menor? Deja de seguirme a todas partes."], "ar": ["لماذا ذهبت الشمس إلى المدرسة؟ لتزداد إشراقًا.", "كيف تُقام حفلة في الفضاء؟ نخطط لها على مستوى الكواكب.", "لماذا سافرت البقرة إلى الفضاء؟ لتزور درب التبانة، فهي تحب الحليب.", "ماذا قال المريخ لزحل؟ لا تنسَ أن ترسل لي خاتمك.", "لماذا القمر مفلس؟ لأنه وصل إلى ربعه الأخير.", "كيف يثبّت النظام الشمسي بنطاله؟ بحزام الكويكبات.", "لماذا لا يجوع روّاد الفضاء بعد الإقلاع؟ لأنهم تناولوا انطلاقة كبيرة.", "ما الموسيقى المفضلة لدى الكواكب؟ ألحان نبتون.", "لماذا انفصل رائد الفضاء عن شريكه؟ كان يحتاج إلى مساحة... فضائية.", "كيف تعرف أن القمر شبع؟ عندما يصبح بدرًا مكتملًا.", "ماذا نسمّي المجنون على القمر؟ مخبول قمري.", "لماذا لم يجد رائد الفضاء غرفة على القمر؟ لأنه كان مكتملًا.", "ما المفتاح المفضل لدى رائد الفضاء في لوحة المفاتيح؟ مفتاح المسافة.", "ماذا قال الكائن الفضائي للحديقة؟ خذيني إلى بستانيك.", "لماذا ابتعد بلوتو عن الشمس؟ بعد أن خُفّضت رتبته، احتاج إلى مسافة أكبر.", "كيف تنظّم حفلة فضائية؟ تخطط لها قبل دورة كاملة.", "ما السنة الضوئية؟ سنة عادية لكن بسعرات حرارية أقل.", "لماذا عوقبت النجمة في المدرسة؟ ضُبطت وهي تتلألأ في الفصل.", "ماذا تقرأ الكواكب في وقت فراغها؟ مجلات المذنّبات المصوّرة.", "لماذا يحفظ زحل الأسرار جيدًا؟ لأن لديه حلقات من الثقة.", "ما الذي يحمل القمر في السماء؟ أشعة القمر.", "أين يضع روّاد الفضاء شطائرهم؟ في صندوق الإطلاق.", "ماذا قال كويكب لآخر؟ لا شيء، فالكويكبات لا تتكلم. لكنها صلبة كالصخر.", "لماذا فاز المذنّب بالسباق؟ لأن ذيله كان مع الريح.", "ماذا نسمّي رائد فضاء غريب الأطوار؟ رائد فضاء طائر العقل.", "كيف يقدّم روّاد الفضاء المشروبات؟ في صحون طائرة.", "لماذا بقي القمر الصناعي هادئًا؟ لأنه يعرف كيف يضع مشكلاته في المدار.", "ما الموسيقى المفضلة لدى الأرض؟ موسيقى الروك، بطبقاتها الكلاسيكية.", "لماذا ذهب النيزك إلى معالج نفسي؟ لأن تأثيره كان ساحقًا على الجميع.", "ماذا قال الدب الأكبر للدب الأصغر؟ توقف عن ملاحقتي في كل مكان."]};
const HUBIMG = { 'Project-Rawane.html': 'project-rawane.jpg', 'Earth_Observation.html': 'earth-observation.gif', 'Deforestation.html': 'forests.jpg', 'Lakes.html': 'lakes.jpg', 'Oceans.html': 'ocean.gif', 'Planetary_Defense.html': 'planetary-defense.gif', 'Rivers.html': 'rivers.jpg', 'Space.html': 'space.gif', 'Space_Disposal.html': 'space-disposal.gif', 'Space_Weather.html': 'space-weather.gif' };
const HUBCREDIT = { 'Project-Rawane.html': 'NASA, Apollo 17 (AS17-148-22742)', 'Earth_Observation.html': 'NASA/NOAA DSCOVR EPIC', 'Deforestation.html': 'SI Partner', 'Lakes.html': '{si}', 'Oceans.html': '{si}', 'Planetary_Defense.html': 'NASA/Johns Hopkins APL/Steve Gribben (PIA25329)', 'Rivers.html': '{si}', 'Space.html': 'NASA/JPL-Caltech/SwRI/MSSS, Kevin Gill (PIA21395)', 'Space_Disposal.html': 'NASA, ISS Expedition 29 (iss029e034092)', 'Space_Weather.html': 'NASA/SDO' };
const STATE = path.join(ROOT, 'scripts', 'newsletter-state.json');

const T = {
  en: { title: 'This Week in Saving Planets', subject: d => `This Week in Saving Planets: ${d}`, intro: 'Your weekly brief of sourced solutions for our planet, minus the doom.', newS: 'New Solutions This Week', none: 'No new solutions this week, but every page was refreshed with the latest figures.', fact: 'Amazing Fact', next: 'Coming Up: Launches & Milestones', why: 'Why It Matters', whyText: 'Space and Earth are one system. Cleaner orbits protect the satellites that track storms, forests and oceans; planetary defense protects us all; and every fix on the ground shows that progress is real and measurable. Share this brief with someone who needs some good news backed by numbers.', read: 'Read more', src: 'Source', visit: 'Explore all solutions', launch: 'launch', arrival: 'arrival', flyby: 'flyby', foot: 'You are receiving this because you subscribed at savingplanets.com.', dateLoc: 'en-US' },
  fr: { title: 'Cette semaine chez Saving Planets', subject: d => `Cette semaine chez Saving Planets : ${d}`, intro: 'Votre brief hebdomadaire de solutions sourcées pour notre planète, sans la fatalité.', newS: 'Nouvelles solutions cette semaine', none: 'Pas de nouvelle solution cette semaine, mais chaque page a été mise à jour avec les derniers chiffres.', fact: 'Fait étonnant', next: 'À venir : lancements et étapes clés', why: 'Pourquoi c\u2019est important', whyText: 'L\u2019espace et la Terre forment un seul système. Des orbites plus propres protègent les satellites qui suivent les tempêtes, les forêts et les océans ; la défense planétaire nous protège tous ; et chaque solution sur le terrain montre que les progrès sont réels et mesurables. Partagez ce brief avec quelqu\u2019un qui a besoin de bonnes nouvelles chiffrées.', read: 'Lire la suite', src: 'Source', visit: 'Découvrir toutes les solutions', launch: 'lancement', arrival: 'arrivée', flyby: 'survol', foot: 'Vous recevez ce message car vous vous êtes abonné sur savingplanets.com.', dateLoc: 'fr-FR' },
  es: { title: 'Esta semana en Saving Planets', subject: d => `Esta semana en Saving Planets: ${d}`, intro: 'Tu resumen semanal de soluciones con fuentes para nuestro planeta, sin catastrofismo.', newS: 'Nuevas soluciones esta semana', none: 'No hay soluciones nuevas esta semana, pero todas las páginas se actualizaron con las cifras más recientes.', fact: 'Dato asombroso', next: 'Próximamente: lanzamientos e hitos', why: 'Por qué importa', whyText: 'El espacio y la Tierra son un solo sistema. Órbitas más limpias protegen los satélites que vigilan tormentas, bosques y océanos; la defensa planetaria nos protege a todos; y cada solución en tierra demuestra que el progreso es real y medible. Comparte este resumen con alguien que necesite buenas noticias respaldadas por datos.', read: 'Leer más', src: 'Fuente', visit: 'Explora todas las soluciones', launch: 'lanzamiento', arrival: 'llegada', flyby: 'sobrevuelo', foot: 'Recibes este correo porque te suscribiste en savingplanets.com.', dateLoc: 'es-ES' },
  ar: { title: 'هذا الأسبوع في Saving Planets', subject: d => `هذا الأسبوع في Saving Planets: ${d}`, intro: 'نشرتك الأسبوعية لحلول موثقة المصادر من أجل كوكبنا، بلا تهويل.', newS: 'حلول جديدة هذا الأسبوع', none: 'لا توجد حلول جديدة هذا الأسبوع، لكن جميع الصفحات حُدّثت بأحدث الأرقام.', fact: 'حقيقة مذهلة', next: 'قريبًا: عمليات الإطلاق والمحطات المهمة', why: 'لماذا يهم ذلك', whyText: 'الفضاء والأرض نظام واحد. المدارات الأنظف تحمي الأقمار الصناعية التي ترصد العواصف والغابات والمحيطات، والدفاع الكوكبي يحمينا جميعًا، وكل حل على الأرض يثبت أن التقدم حقيقي وقابل للقياس. شارك هذه النشرة مع من يحتاج إلى أخبار جيدة مدعومة بالأرقام.', read: 'اقرأ المزيد', src: 'المصدر', visit: 'استكشف جميع الحلول', launch: 'إطلاق', arrival: 'وصول', flyby: 'تحليق', foot: 'تتلقى هذه الرسالة لأنك اشتركت عبر savingplanets.com.', dateLoc: 'ar' }
};

// Fixed strings for the v2 template (2026-10-11).
const T2 = {
  en: { corr: 'Corrections & Updates', corrIntro: 'We fix mistakes in the open. Changed since the last issue:', caught: 'Caught by', corrInvite: 'Spot an error? Tell us at', inIssue: 'In this issue', backTop: 'Back to top', imgLbl: 'Image', siImg: 'SI-generated image by Saving Planets', joke: 'Project Rawane\u2019s Favorite Dad Joke', hubAlt: 'Banner image for', seeAll: (n, h) => `See all ${n} new in ${h}`, issue: 'Issue date', hubsIntro: 'Grouped by hub. Tap a title to read the full page.', horizon: 'Potential solution on the horizon', horizonNote: "We'll keep you updated here if this becomes a reality.",
    noneAll: 'No new solutions this week.', launches: 'Launches This Week', noLaunch: 'No launches are on the books for this week yet.', vehicle: 'Vehicle', mission: 'Mission', shift: 'Launch dates shift often.', schedule: 'See our full launch schedule',
    suggest: 'Suggest a New Solution', suggestText: 'Know a group doing hands-on work with published numbers? Email your idea to', criteria: 'See our solutions criteria', facts: 'Amazing Facts', source: 'Source', allFacts: 'See all Amazing Facts', unsub: 'Unsubscribe', tz: 'UTC' },
  fr: { corr: 'Corrections et mises à jour', corrIntro: 'Nous corrigeons nos erreurs en toute transparence. Modifié depuis le dernier numéro :', caught: 'Signalé par', corrInvite: 'Vous avez repéré une erreur ? Écrivez-nous à', inIssue: 'Dans ce numéro', backTop: 'Retour en haut', imgLbl: 'Image', siImg: 'Image générée par SI par Saving Planets', joke: 'La blague de papa préférée de Projet Rawane', hubAlt: 'Image de bannière :', seeAll: (n, h) => `Voir les ${n} nouveautés : ${h}`, issue: 'Date du numéro', hubsIntro: 'Classées par thème. Touchez un titre pour lire la page complète.', horizon: "Solution potentielle à l'horizon", horizonNote: 'Nous vous tiendrons informés ici si cela se concrétise.',
    noneAll: 'Pas de nouvelle solution cette semaine.', launches: 'Lancements de la semaine', noLaunch: "Aucun lancement n'est encore prévu cette semaine.", vehicle: 'Lanceur', mission: 'Mission', shift: 'Les dates de lancement changent souvent.', schedule: 'Voir notre calendrier complet des lancements',
    suggest: 'Proposez une nouvelle solution', suggestText: 'Vous connaissez un groupe qui agit sur le terrain avec des chiffres publiés ? Envoyez votre idée à', criteria: 'Voir nos critères de sélection', facts: 'Faits étonnants', source: 'Source', allFacts: 'Voir tous les faits étonnants', unsub: 'Se désabonner', tz: 'UTC' },
  es: { corr: 'Correcciones y actualizaciones', corrIntro: 'Corregimos nuestros errores a la vista de todos. Cambios desde el último número:', caught: 'Detectado por', corrInvite: '¿Viste un error? Escríbenos a', inIssue: 'En este número', backTop: 'Volver arriba', imgLbl: 'Imagen', siImg: 'Imagen generada por SI por Saving Planets', joke: 'El chiste de papá favorito de Proyecto Rawane', hubAlt: 'Imagen de cabecera:', seeAll: (n, h) => `Ver las ${n} novedades en ${h}`, issue: 'Fecha del número', hubsIntro: 'Agrupadas por tema. Toca un título para leer la página completa.', horizon: 'Posible solución en el horizonte', horizonNote: 'Te mantendremos informado aquí si esto se hace realidad.',
    noneAll: 'No hay soluciones nuevas esta semana.', launches: 'Lanzamientos de esta semana', noLaunch: 'Todavía no hay lanzamientos programados para esta semana.', vehicle: 'Vehículo', mission: 'Misión', shift: 'Las fechas de lanzamiento cambian a menudo.', schedule: 'Ver nuestro calendario completo de lanzamientos',
    suggest: 'Sugiere una nueva solución', suggestText: '¿Conoces un grupo que hace trabajo práctico con cifras publicadas? Envía tu idea a', criteria: 'Ver nuestros criterios de soluciones', facts: 'Datos asombrosos', source: 'Fuente', allFacts: 'Ver todos los datos asombrosos', unsub: 'Darse de baja', tz: 'UTC' },
  ar: { corr: 'تصحيحات وتحديثات', corrIntro: 'نصحح أخطاءنا بشفافية. ما تغيّر منذ العدد الماضي:', caught: 'رصده', corrInvite: 'لاحظت خطأً؟ راسلنا على', inIssue: 'في هذا العدد', backTop: 'العودة إلى الأعلى', imgLbl: 'الصورة', siImg: 'صورة مولّدة بتقنية SI من Saving Planets', joke: 'نكتة الأب المفضلة لدى مشروع Rawane', hubAlt: 'صورة لافتة لقسم', seeAll: (n, h) => `عرض جميع الإضافات الجديدة (${n}) في ${h}`, issue: 'تاريخ العدد', hubsIntro: 'مصنفة حسب المحور. اضغط على العنوان لقراءة الصفحة كاملة.', horizon: 'حل محتمل في الأفق', horizonNote: 'سنبقيكم على اطلاع هنا إذا أصبح هذا واقعًا.',
    noneAll: 'لا توجد حلول جديدة هذا الأسبوع.', launches: 'عمليات الإطلاق هذا الأسبوع', noLaunch: 'لا توجد عمليات إطلاق مجدولة لهذا الأسبوع حتى الآن.', vehicle: 'المركبة', mission: 'المهمة', shift: 'تتغير مواعيد الإطلاق كثيرًا.', schedule: 'اطّلع على جدول الإطلاق الكامل',
    suggest: 'اقترح حلًا جديدًا', suggestText: 'هل تعرف جهة تقوم بعمل ميداني وتنشر أرقامًا موثقة؟ أرسل فكرتك إلى', criteria: 'اطّلع على معايير اختيار الحلول', facts: 'حقائق مذهلة', source: 'المصدر', allFacts: 'اطّلع على جميع الحقائق المذهلة', unsub: 'إلغاء الاشتراك', tz: 'UTC' }
};
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const dec = s => String(s).replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&');
const rd = f => { try { return fs.readFileSync(path.join(ROOT, f), 'utf8'); } catch (e) { return null; } };
const pageFile = (lang, f) => lang === 'en' ? f : `${lang}/${f}`;
const pre = lang => lang === 'en' ? '' : lang + '/';
const loadState = () => { try { return JSON.parse(fs.readFileSync(STATE, 'utf8')); } catch (e) { return { usedFacts: [], issues: {} }; } };
function meta(html) {
  const t = (html.match(/<title>([^<]*)<\/title>/) || [])[1] || '';
  const d = (html.match(/<meta name="description" content="([^"]*)"/) || [])[1] || '';
  return { title: dec(t.replace(/\s*[|·–-]\s*(Saving Planets|Français|Español|بالعربية).*$/, '').trim()), desc: dec(d) };
}
// Hub membership from the Solutions menu on each language's homepage (first hub that lists the page wins).
function hubMap(lang) {
  const html = rd(pageFile(lang, 'index.html')) || rd('index.html'), map = {}, order = [];
  const menu = (html.match(/<!-- SOLUTIONS-MENU:START -->([\s\S]*?)<!-- SOLUTIONS-MENU:END -->/) || [])[1] || '';
  if (!menu) { // Oct 12: the nav dropdown was removed; hub membership now comes from solutions.json (build-stats.js)
    try { for (const g of JSON.parse(rd('assets/data/solutions.json')).solutionsMenu || []) { order.push({ url: g.href, name: g.hub }); for (const i of g.items) if (!map[i.href]) map[i.href] = g.href; } } catch (e) {}
    return { map, order };
  }
  for (const g of menu.split('<li class="menu-group">').slice(1)) {
    const h = g.match(/class="menu-hub" href="([^"]+)">([^<]+)</); if (!h) continue;
    order.push({ url: h[1], name: dec(h[2]) });
    for (const m of g.matchAll(/<li><a href="([^"]+)">/g)) if (!map[m[1]]) map[m[1]] = h[1];
  }
  return { map, order };
}
function newSolutions() {
  const data = JSON.parse(rd('assets/data/solutions.json'));
  const since = Date.now() - DAYS * 864e5, status = {};
  for (const p of data.pages) if (p.type !== 'hub') (status[p.url] = status[p.url] || new Set()).add(p.status);
  const out = [];
  for (const url of Object.keys(status)) {
    let added; try { added = execSync(`git log --diff-filter=A --format=%cI -- "${url}" | tail -1`, { cwd: ROOT }).toString().trim(); } catch (e) { continue; }
    if (added && Date.parse(added) >= since) out.push({ url, added, horizon: !status[url].has('active') });
  }
  return out.sort((a, b) => a.url.localeCompare(b.url));
}
function factCards(lang) {
  const html = rd(pageFile(lang, 'Amazing_Facts.html')) || rd('Amazing_Facts.html');
  return (html.match(/<div class="w-card" data-fact-origin[\s\S]*?<\/div>/g) || []).map(c => {
    const g = re => (c.match(re) || [])[1];
    const img = g(/<img[^>]*src="([^"]+)"/), ps = [...c.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m => m[1].replace(/<[^>]+>/g, ''));
    return { key: g(/data-fact-page="([^"]+)"/) + '|' + (g(/<img[^>]*src="([^"]+)"/) || ''), h: dec(g(/<h3>([\s\S]*?)<\/h3>/) || ''), img: img && SITE + img.replace(/^\.\.\//, ''), alt: dec(g(/alt="([^"]*)"/) || ''), text: dec(ps[0] || ''),
      page: g(/data-fact-page="([^"]+)"/), srcUrl: g(/Source: <a href="([^"]+)"/), srcLabel: dec((c.match(/(?:Source|المصدر|Fuente)[^<]*<a [^>]*>([^<]+)</) || [])[1] || '') };
  });
}
// Pick 2 facts never used in an earlier issue (keys from the EN page); reuse this issue's picks on re-runs.
function pickFacts(state) {
  if (state.issues[iso] && state.issues[iso].facts) return state.issues[iso].facts;
  const prior = new Set(state.usedFacts), cards = factCards('en');
  let fresh = cards.filter(c => !prior.has(c.key));
  if (fresh.length < 2) { state.usedFacts = []; fresh = cards; }  // all used: start a new rotation
  return fresh.slice(0, 2).map(c => c.key);
}
// Launch week: Mon-Sun containing the issue date; on a Sunday the issue covers the coming Mon-Sun too.
function weekWindow() {
  const d = new Date(iso + 'T00:00:00-10:00'), dow = (d.getUTCDay() + 6) % 7; // 0 = Monday (HST date)
  const start = dow === 6 ? d : new Date(d - dow * 864e5), end = new Date(+start + (dow === 6 ? 8 : 7) * 864e5);
  return { start, end };
}
async function launches() {
  const { start, end } = weekWindow();
  const r = await fetch(`https://ll.thespacedevs.com/2.3.0/launches/?net__gte=${start.toISOString()}&net__lt=${end.toISOString()}&limit=30&mode=normal&ordering=net`, { headers: { Accept: 'application/json' } });
  if (!r.ok) throw new Error('Launch Library ' + r.status);
  return (await r.json()).results.map(l => ({ date: l.net, vehicle: (l.rocket && l.rocket.configuration && l.rocket.configuration.name) || l.name.split('|')[0].trim(), mission: (l.mission && l.mission.name) || l.name.split('|').pop().trim(), provider: l.launch_service_provider && l.launch_service_provider.name }));
}
function fmtDate(d, lang) { return new Date(d).toLocaleDateString(T[lang].dateLoc, { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'Pacific/Honolulu' }); }
function fmtDay(d, lang) { return new Date(d).toLocaleString(T[lang].dateLoc, { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'UTC' }) + ' UTC'; }
// Solution of the Week (same rotation as the homepage: assets/data/solution-of-week.json; text translated via i18n/<lang>.json)
const SOTW_T = { en: ['Solution of the Week', 'Watch and Learn More'], fr: ['Solution de la semaine', 'Regarder et en savoir plus'], es: ['Solución de la semana', 'Mira y aprende más'], ar: ['حل الأسبوع', 'شاهد واعرف المزيد'] };
function sotw(lang) {
  try {
    const d = JSON.parse(rd('assets/data/solution-of-week.json')), st = new Date(d.start + 'T00:00:00Z');
    const e = d.rotation[Math.floor(Math.floor((today.getTime() - 10 * 36e5 - st) / 864e5) / 7) % d.rotation.length];
    const tm = lang === 'en' ? {} : JSON.parse(rd(`i18n/${lang}.json`) || '{}'), tr = x => tm[x] || x;
    return { ...e, title: tr(e.title), blurb: tr(e.blurb), imageAlt: tr(e.imageAlt), label: SOTW_T[lang][0], cta: SOTW_T[lang][1] };
  } catch (err) { return null; }
}
// Corrections & Updates: entries from scripts/newsletter-corrections.json dated after the previous issue (state) up to this issue.
function corrections(state) {
  let d; try { d = JSON.parse(rd('scripts/newsletter-corrections.json')); } catch (e) { return []; }
  const prev = Object.keys(state.issues || {}).filter(k => k < iso).sort().pop() || '0000-00-00';
  return (d.entries || []).filter(e => e.date > prev && e.date <= iso);
}
function build(lang, sols, factKeys, launchList, joke, corr = []) {
  const t = { ...T[lang], ...T2[lang] }, rtl = lang === 'ar', dir = rtl ? 'rtl' : 'ltr', al = rtl ? 'right' : 'left', P = SITE + pre(lang);
  const a = (href, txt, bold) => `<a href="${href}" style="color:#009cde;${bold ? 'font-weight:700;' : ''}text-decoration:none">${esc(txt)}</a>`;
  const top = `<p style="margin:10px 0 0;font-size:12px;text-align:${rtl ? 'left' : 'right'}"><a href="#sp-top" style="color:#5b7486;text-decoration:none">${esc(t.backTop)} ↑</a></p>`;
  const h2 = (s, id) => `<h2${id ? ` id="${id}"` : ''} style="margin:30px 0 12px;font-size:20px;color:#003755;border-bottom:2px solid #009cde;padding-bottom:6px">${esc(s)}</h2>`;
  // 2. New solutions by hub
  const { map, order } = hubMap(lang), byHub = {};
  for (const s of sols) (byHub[map[s.url] || '_other'] = byHub[map[s.url] || '_other'] || []).push(s);
  let solsHtml = '';
  for (const hub of [...order, { url: '_other', name: '' }]) {
    const list = byHub[hub.url]; if (!list) continue;
    if (HUBIMG[hub.url]) solsHtml += `<a href="${P + hub.url}"><img src="${SITE}assets/newsletter/${HUBIMG[hub.url]}" width="552" height="140" alt="${esc(t.hubAlt + ' ' + hub.name)}" style="display:block;width:100%;max-width:552px;height:auto;border:0;border-radius:8px;margin:22px 0 0"></a>` + (HUBCREDIT[hub.url] ? `<p style="margin:3px 0 0;font-size:11px;color:#7b8f9d;text-align:${rtl ? 'left' : 'right'}">${HUBCREDIT[hub.url] === '{si}' ? esc(t.siImg) : esc(t.imgLbl) + ': ' + esc(HUBCREDIT[hub.url])}</p>` : '');
    solsHtml += `<h3 style="margin:18px 0 8px;font-size:16px;color:#003755;text-transform:uppercase;letter-spacing:.5px">${hub.url === '_other' ? '' : a(P + hub.url, hub.name, true)}</h3>`;
    const more = list.length > CAP && hub.url !== '_other' ? `<p style="margin:0 0 12px;font-size:14px">${a(P + hub.url, t.seeAll(list.length, hub.name) + ' →', true)}</p>` : '';
    solsHtml += list.slice(0, CAP).map(s => { const m = meta(rd(pageFile(lang, s.url)) || rd(s.url));
      const badge = s.horizon ? `<br><span style="display:inline-block;margin:4px 0;background:#fff4e0;color:#8a5a00;border:1px solid #f0c36d;border-radius:12px;padding:1px 9px;font-size:12px;font-weight:700">${esc(t.horizon)}</span> <span style="font-size:12px;color:#5b7486">${esc(t.horizonNote)}</span>` : '';
      return `<p style="margin:0 0 12px">${a(P + s.url, m.title, true)}${badge}<br><span style="font-size:14px">${esc(m.desc)}</span></p>`; }).join('') + more;
  }
  if (!sols.length) solsHtml = `<p>${esc(t.noneAll)}</p>`;
  else solsHtml = `<p style="margin:0 0 4px;font-size:13px;color:#5b7486">${esc(t.hubsIntro)}</p>` + solsHtml;
  // 2b. Solution of the Week
  const sw = sotw(lang), swHref = sw ? P + sw.page + (sw.video ? '#video' : '') : '';
  const swHtml = sw ? `<a href="${swHref}"><img src="${SITE}${sw.image}" width="552" alt="${esc(sw.imageAlt)}" style="display:block;width:100%;max-width:552px;height:auto;border:0;border-radius:8px"></a><p style="margin:3px 0 0;font-size:11px;color:#7b8f9d;text-align:${rtl ? 'left' : 'right'}">${esc(t.siImg)}</p><h3 style="margin:12px 0 6px;font-size:18px;color:#003755">${a(P + sw.page, sw.title, true)}</h3><p style="margin:0 0 12px">${esc(sw.blurb)}</p><p style="margin:0"><a href="${swHref}" style="display:inline-block;background:#009cde;color:#fff;font-weight:700;padding:10px 18px;border-radius:6px;text-decoration:none">${esc(sw.cta)}</a></p>` : '';
  // 3. Launches
  const lHtml = (launchList && launchList.length ? `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;border-collapse:collapse">` + launchList.map(l =>
    `<tr><td dir="${dir}" style="padding:8px 0;border-bottom:1px solid #e3edf4;text-align:${al}"><strong>${esc(fmtDay(l.date, lang))}</strong><br>${esc(t.vehicle)}: ${esc(l.vehicle)}${l.provider ? ' (' + esc(l.provider) + ')' : ''}<br>${esc(t.mission)}: ${esc(l.mission)}</td></tr>`).join('') + '</table>'
    : `<p style="margin:0">${esc(t.noLaunch)}</p>`) + `<p style="margin:12px 0 0;font-size:14px">${esc(t.shift)} ${a(P + 'Project-Rawane.html#launches', t.schedule + ' →', true)}</p>`;
  // 3b. Corrections & Updates (hidden when empty)
  const cHtml = corr.length ? `<p style="margin:0 0 10px;font-size:14px">${esc(t.corrIntro)}</p>` + corr.map(c => `<p style="margin:0 0 12px">${esc((c.what && (c.what[lang] || c.what.en)) || '')}${c.page ? ' ' + a(P + c.page, t.read + ' →', true) : ''}<br><span style="font-size:13px;color:#5b7486">${esc(fmtDate(c.date + 'T12:00:00-10:00', lang))} · ${esc(t.caught)}: ${esc((c.caught_by && (c.caught_by[lang] || c.caught_by.en)) || '')}</span></p>`).join('') + `<p style="margin:0;font-size:13px">${esc(t.corrInvite)} <a href="mailto:ideas@savingplanets.com?subject=Correction" style="color:#009cde;font-weight:700">ideas@savingplanets.com</a>.</p>` : '';
  // 4. Suggest
  const sugHtml = `<div style="background:#eef5fa;border-radius:8px;padding:16px 18px"><p style="margin:0 0 8px">${esc(t.suggestText)} <a href="mailto:ideas@savingplanets.com?subject=Solution%20idea" style="color:#009cde;font-weight:700">ideas@savingplanets.com</a>.</p><p style="margin:0">${a(P + 'About.html#criteria', t.criteria + ' →', true)}</p></div>`;
  // 5. Facts
  const cards = factCards(lang), enCards = factCards('en');
  const facts = factKeys.map(k => { const i = enCards.findIndex(c => c.key === k); return cards.find(c => c.key === k) || cards[i] || enCards[i]; }).filter(Boolean);
  const fHtml = facts.map(f => `<h3 style="margin:16px 0 8px;color:#003755;font-size:17px">${esc(f.h)}</h3>${f.img ? `<img src="${f.img}" alt="${esc(f.alt)}" width="552" style="width:100%;max-width:552px;height:auto;border-radius:8px;display:block;margin:0 0 10px">` : ''}<p style="margin:0 0 6px">${esc(f.text)}</p><p style="margin:0;font-size:13px">${f.page ? a(P + f.page, t.read) : ''}${f.srcUrl ? ` · ${esc(t.source)}: ${a(f.srcUrl, f.srcLabel || f.srcUrl)}` : ''}</p>`).join('')
    + `<p style="margin:16px 0 0">${a(P + 'Amazing_Facts.html', t.allFacts + ' →', true)}</p>`;
  return `<!DOCTYPE html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(t.title)}</title></head>
<body style="margin:0;background:#eef5fa"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef5fa"><tr><td align="center" style="padding:20px 10px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:10px;overflow:hidden">
<tr><td dir="${dir}" style="background:#003755;padding:22px 24px;font-family:Montserrat,Segoe UI,Arial,sans-serif;text-align:${al}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" dir="${dir}"><tr><td valign="middle" width="100%" dir="${dir}" style="text-align:${al}">
<p style="margin:0;font-size:12px;letter-spacing:2px;color:#7fd3f7;font-weight:700">SAVING PLANETS</p>
<p style="margin:8px 0 0;font-size:28px;font-weight:800;color:#ffffff;line-height:1.2">${esc(fmtDate(today, lang))}</p>
<p style="margin:4px 0 0;font-size:16px;color:#cfe9f7">${esc(t.title)}</p></td><td valign="middle" style="padding-${rtl ? 'right' : 'left'}:16px"><a href="${P}index.html"><img src="${SITE}assets/SavePlanetLogo-email.png" width="72" height="84" alt="Saving Planets" style="display:block;width:72px;height:84px;border:0;border-radius:8px"></a></td></tr></table></td></tr>
<tr><td dir="${dir}" style="padding:24px 24px 28px;font-family:Montserrat,Segoe UI,Arial,sans-serif;font-size:15px;line-height:1.55;color:#003755;text-align:${al}">
<p id="sp-top" style="margin:0;text-align:center;font-weight:700;font-size:17px">${esc(t.intro)}</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:16px 0 0;background:#eef5fa;border-radius:8px"><tr><td dir="${dir}" style="padding:10px 14px;font-size:13px;line-height:1.9;text-align:center"><strong style="color:#003755">${esc(t.inIssue)}:</strong> ${[...(sw ? [['sp-sotw', sw.label]] : []), ['sp-new', t.newS], ['sp-launches', t.launches], ['sp-facts', t.facts]].concat(cHtml ? [['sp-corr', t.corr]] : []).concat([['sp-suggest', t.suggest]]).concat(joke ? [['sp-joke', t.joke]] : []).map(x => `<a href="#${x[0]}" style="color:#009cde;font-weight:700;text-decoration:none;white-space:nowrap">${esc(x[1])}</a>`).join(' &middot; ')}</td></tr></table>
${sw ? h2(sw.label, 'sp-sotw') + swHtml + top : ''}
${h2(t.newS, 'sp-new')}${solsHtml}${top}
${h2(t.launches, 'sp-launches')}${lHtml}${top}
${cHtml ? h2(t.corr, 'sp-corr') + cHtml + top : ''}
${h2(t.suggest, 'sp-suggest')}${sugHtml}${top}
${h2(t.facts, 'sp-facts')}${fHtml}${top}
${joke ? h2(t.joke, 'sp-joke') + `<div style="background:#003755;color:#ffffff;border-radius:8px;padding:16px 18px;font-size:16px" dir="${dir}" lang="${lang}"><span style="font-size:22px">🚀</span> ${esc(joke)}</div>` + top : ''}
<p style="margin:28px 0 0;text-align:center"><a href="${P}index.html" style="display:inline-block;background:#009cde;color:#fff;font-weight:700;padding:12px 22px;border-radius:6px;text-decoration:none">${esc(t.visit)}</a></p>
<p style="margin:26px 0 0;font-size:12px;color:#5b7486;text-align:center">${esc(t.foot)}<br>{$account_address}<br><a href="{$unsubscribe}" style="color:#5b7486">${esc(t.unsub)}</a></p>
</td></tr></table></td></tr></table></body></html>`;
}
async function api(method, p, body) {
  const key = fs.readFileSync(process.env.MAILERLITE_KEY_FILE || path.join(os.homedir(), '.mailerlite_key'), 'utf8').trim();
  const r = await fetch(API + p, { method, headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json', Accept: 'application/json' }, body: body && JSON.stringify(body) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`${method} ${p} -> ${r.status} ${JSON.stringify(j).slice(0, 400)}`);
  return j;
}
(async () => {
  const sols = newSolutions(), state = loadState(), factKeys = pickFacts(state), corr = corrections(state);
  let jokeIdx = state.issues[iso] && state.issues[iso].joke != null ? state.issues[iso].joke : null;
  if (jokeIdx == null) { const used = new Set(state.usedJokes || []); let free = JOKES.map((_, i) => i).filter(i => !used.has(i)); if (!free.length) { state.usedJokes = []; free = JOKES.map((_, i) => i); } jokeIdx = free[0]; }
  const joke = JOKES[jokeIdx];
  let launchList = null; try { launchList = await launches(); } catch (e) { console.log('note: launches unavailable (' + e.message + ')'); }
  let existing = [];
  let drafts = [];
  if (!DRY) { drafts = (await api('GET', '/campaigns?filter[status]=draft&limit=100')).data; existing = drafts.map(c => c.name); }
  for (const lang of LANGS) {
    const html = build(lang, sols, factKeys, launchList, lang === 'en' ? joke : JOKES_T[lang][jokeIdx], corr), name = `Weekly Brief ${iso}${process.env.NL_SUFFIX || ""} (${lang.toUpperCase()})`;
    fs.writeFileSync(`/tmp/newsletter-${iso}-${lang}.html`, html);
    if (DRY) { console.log(`[dry-run] ${name}: ${html.length} bytes -> /tmp/newsletter-${iso}-${lang}.html`); continue; }
    const email = { subject: T[lang].subject(fmtDate(today, lang)), from_name: FROM.name, from: FROM.email, content: html };
    if (existing.includes(name)) {
      if (!UPDATE) { console.log(`skip (draft exists): ${name}`); continue; }
      const d = drafts.find(x => x.name === name);
      const u = await api('PUT', `/campaigns/${d.id}`, { name, language_id: LANG_IDS[lang], emails: [email], groups: [GROUPS[lang]] });
      console.log(`draft updated: ${name} id=${d.id} status=${u.data.status} language=${u.data.language && u.data.language.shortcode}`); continue;
    }
    let c;
    try { c = await api('POST', '/campaigns', { name, type: 'regular', language_id: LANG_IDS[lang], emails: [email], groups: [GROUPS[lang]] }); }
    catch (e) {
      if (!/content/i.test(e.message)) throw e;
      delete email.content;  // plan does not allow custom HTML via API: create the draft without content; paste /tmp HTML in the editor
      c = await api('POST', '/campaigns', { name, type: 'regular', language_id: LANG_IDS[lang], emails: [email], groups: [GROUPS[lang]] });
      console.log(`note: ${name} created WITHOUT HTML content (API refused content); use /tmp/newsletter-${iso}-${lang}.html`);
    }
    console.log(`draft created: ${name} id=${c.data.id} status=${c.data.status}`);
  }
  if (!DRY) {  // record facts so later issues never repeat them
    state.usedJokes = [...new Set([...(state.usedJokes || []), jokeIdx])];
    state.issues[iso] = { joke: jokeIdx, facts: factKeys, solutions: sols.length, launches: launchList ? launchList.length : null };
    state.usedFacts = [...new Set([...state.usedFacts, ...factKeys])];
    fs.writeFileSync(STATE, JSON.stringify(state, null, 2) + '\n');
  }
  console.log('facts:', factKeys.join(', '), '| solutions:', sols.length, '| launches:', launchList ? launchList.length : 'n/a');
})().catch(e => { console.error('ERROR', e.message); process.exit(1); });
