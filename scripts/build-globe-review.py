#!/usr/bin/env python3
"""Build the unlinked GLOBE_Review.html pages (en, fr, es, ar, it, he).

Keeps each language's standard nav, Related Solutions, and the rest of the
GLOBE_Program.html tail (cite, share, footer). Drops the floating Donate button.
"""
import html, json, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

LANGS = ['en', 'fr', 'es', 'ar', 'it', 'he']
SITE = 'https://www.savingplanets.com/'

def E(s):
    return html.escape(s, quote=True)

def A(url, label):
    return f'<a href="{E(url)}" target="_blank" rel="noopener noreferrer">{E(label)}</a>'

# UI strings. Fact sentences stay tied to the official pages linked beside them.
UI = {
'en': {
 'title': 'Clouds teacher sheet for The GLOBE Program',
 'desc': 'A working draft for The GLOBE Program team: a Clouds teacher sheet and a lesson builder that link official GLOBE documents and films.',
 'skip': 'Skip to content',
 'invite': 'A working draft for The GLOBE Program team. Please review, suggest edits, share ideas, or point us to further solutions. We learn from each other to improve education for everyone.',
 'h1': 'Clouds for the classroom',
 'lead': 'A teacher sheet and a lesson builder that point to official GLOBE documents and films. This page adds practical tools around those resources. It does not replace them.',
 'credit': 'Created by the Founder and SI',
 'show': 'This page is a showcase of official GLOBE resources for teachers. It is not a partnership with GLOBE or NASA, and it is not an endorsement by either of them.',
 'sheetH': 'Clouds teacher sheet',
 'sumH': 'For students',
 'sum': 'GLOBE is an international science program. The Clouds protocol is how observers report which clouds they see, how much of the sky the clouds cover, how thick the clouds look, and what the sky and the ground are like. A class can do this at a time that fits the day. Satellites see the tops of clouds. People on the ground see the bottoms.',
 'whyH': 'Why clouds matter',
 'why': 'GLOBE says cloud observations help NASA understand cloud types and the effects clouds have on Earth’s climate. Putting the ground view and the satellite view together gives a fuller picture.',
 'doH': 'What students do',
 'do': 'Students follow GLOBE’s own Clouds documents. This sheet does not rewrite the measurement steps.',
 'gradesH': 'Grade bands',
 'grades': 'Elementary GLOBE’s Clouds module is for primary grades K–4. Grades 5–12 use the Clouds protocol learning activities and field guides. GLOBE says children under 13 should be supervised by an adult.',
 'qH': 'Discussion questions',
 'qs': [
  'What can a person on the ground see in a cloud that a satellite looking down might miss?',
  'Why does GLOBE ask for training on a protocol before that protocol’s data is entered?',
  'GLOBE matches cloud observations with satellites such as GOES, Himawari, JPSS, and PACE. Why can the time of the observation matter?',
 ],
 'idH': 'Cloud-type quick guide',
 'id': 'The names and the steps live on GLOBE’s own cloud chart, cloud-type field guide, and Clouds protocol. Use those, and the GLOBE Observer app, instead of a chart made for this page.',
 'dataH': 'Student data page',
 'dataIntro': 'Write your name and the date. Then use GLOBE’s official Clouds 1-day data sheet for the observation itself.',
 'name': 'Name', 'date': 'Date', 'class': 'Class', 'notice': 'One thing I noticed about the sky',
 'ngssH': 'NGSS notes', 'standardsH': 'Standards', 'sourceGLOBE': 'Source: GLOBE',
 'ngss': 'GLOBE’s NGSS guide lists the Clouds protocol on the kindergarten page for K-ESS2-1, “Use and share observations of local weather conditions to describe patterns over time.” The same guide lists the Clouds protocol and the activity “Observing, Describing, and Identifying Clouds” on the middle-school page for MS-ESS2-5, about air masses and weather. Several other atmosphere protocols are listed on those pages too. The PDF is the authority.',
 'train': 'Since December 2025, a GLOBE member completes one training for each protocol before entering data for that protocol. The training can be a review of the field guide, a Data Collection eTraining where GLOBE offers one, a full Protocol eTraining and assessment, or a GLOBE workshop.',
 'buildH': 'Lesson builder',
 'buildL': 'Choose a grade band, a GLOBE topic, and a length. The plan links the official protocol page and the official films for that topic. It does not copy the measurement steps.',
 'band': 'Grade band', 'topic': 'Topic', 'length': 'Length',
 'printSheet': 'Print the teacher sheet', 'printPlan': 'Print Plan', 'copyLink': 'Copy Link', 'copyPlan': 'Copy the plan', 'classroom': 'Share to Google Classroom', 'buildBtn': 'Build plan', 'videoCredit': 'Title video credits:', 'appLink': 'Yes, right now get your GLOBE app',
 'suggestH': 'Suggest an edit or another solution',
 'suggest': 'Write to the partnerships desk. There is no form on this page.',
 'cite': 'The source of this material is the GLOBE Program website at www.globe.gov. All Rights Reserved.',
 'src': 'Source',
 'spheres': {'atm':'Atmosphere','hyd':'Hydrosphere','ped':'Pedosphere (Soil)','bio':'Biosphere','obs':'GLOBE Observer'},
 'topics': {'clouds':'Clouds','airtemp':'Air temperature','precip':'Precipitation','watertemp':'Water temperature','ph':'Water pH','mosquito':'Mosquito Habitat Mapper','soil':'Soil characterization','landcover':'Land cover','trees':'Trees (biometry and tree height)','greenup':'Green-Up / Green-Down','observer':'GLOBE Observer app'},
 'bands': {'k2':'K-2','g35':'3-5','g68':'6-8','g912':'9-12'},
 'lengths': {'class':'One class period','week':'One week'},
 'planH':'Lesson plan','planMeta':'{name} · {band} · {length}',
 'objH':'Objective','matH':'Materials','stepsH':'Steps','vidH':'Official films','dataLab':'Data collection','qLab':'Discussion','ngssLab':'NGSS',
 'obj':'Students follow GLOBE’s official {name} materials for {band}, in {length}, and can say what the protocol asks them to observe.',
 'steps':'Open the official {name} protocol page and use that document for the measurement. This plan does not rewrite those steps.|Watch an official film for this topic, or the matching protocol video on GLOBE’s video page.|For one class period, hold one observation session. For one week, repeat only as often as the protocol page allows.|An adult supervises anyone under 13. A GLOBE member finishes that protocol’s training before data is entered.',
 'data':'Record the observation on GLOBE’s own data sheet or in the GLOBE Observer app. Do not copy the measurement form onto this plan.',
 'questions':['What does the official {name} page ask an observer to notice?','What has to happen before this protocol’s data is entered in GLOBE?','Which official film or field guide will you use, and why that one?'],
 'ngssClouds':'For Clouds, GLOBE’s guide lists the protocol with K-ESS2-1 and, with the activity “Observing, Describing, and Identifying Clouds,” on the page for MS-ESS2-5. Other atmosphere protocols are listed there too.',
 'ngssGeneric':'Look up this protocol in GLOBE’s NGSS guide. This plan does not add performance expectations that the guide does not show.',
 'ngssName':'GLOBE NGSS connections (PDF)','openProtocol':'Official protocol page','openTrain':'GLOBE eTraining','openVideos':'GLOBE instructional videos','openElem':'Elementary GLOBE module for primary grades',
 'wmvNote':'This is GLOBE’s Windows Media film from the instructional-video page.','noFilm':'GLOBE’s video page does not list a separate film for this protocol.',
 'copied':'Copied',
},
}
# The other languages reuse the same keys. Protocol names that are GLOBE's own stay recognizable.
def tr(**kw):
    base = json.loads(json.dumps(UI['en']))
    base.update(kw)
    return base

UI['fr'] = tr(
 title='Fiche Nuages pour le programme GLOBE',
 desc='Ébauche de travail pour l’équipe du programme GLOBE : une fiche Nuages et un générateur de leçon qui renvoient aux documents et films officiels.',
 skip='Aller au contenu',
 invite='Une ébauche de travail pour l’équipe du programme GLOBE. Merci de la relire, de proposer des corrections, de partager des idées ou de nous indiquer d’autres solutions. Nous apprenons les uns des autres pour améliorer l’éducation de toutes et tous.',
 h1='Les nuages en classe',
 lead='Une fiche enseignant et un générateur de leçon qui renvoient aux documents et aux films officiels de GLOBE. Cette page ajoute des outils pratiques autour de ces ressources. Elle ne les remplace pas.',
 credit='Créé par le fondateur et SI',
 show='Cette page présente des ressources officielles de GLOBE pour les enseignants. Ce n’est pas un partenariat avec GLOBE ou la NASA, ni une approbation de leur part.',
 sheetH='Fiche Nuages', sumH='Pour les élèves',
 sum='GLOBE est un programme scientifique international. Le protocole Nuages indique comment signaler les nuages visibles, la part du ciel qu’ils couvrent, leur opacité, ainsi que le ciel et le sol. Une classe peut le faire au moment qui lui convient. Les satellites voient le dessus des nuages. Les personnes au sol en voient le dessous.',
 whyH='Pourquoi les nuages comptent',
 why='GLOBE indique que les observations de nuages aident la NASA à comprendre les types de nuages et leurs effets sur le climat de la Terre. Réunir la vue du sol et la vue du satellite donne une image plus complète.',
 doH='Ce que font les élèves', do='Les élèves suivent les documents Nuages de GLOBE. Cette fiche ne réécrit pas les étapes de mesure.',
 gradesH='Niveaux', grades='Le module Nuages d’Elementary GLOBE s’adresse au primaire, de la maternelle à la 4e année. De la 5e à la 12e année, on utilise les activités et les guides du protocole Nuages. GLOBE indique qu’un adulte accompagne les enfants de moins de 13 ans.',
 qH='Questions de discussion',
 qs=['Que voit une personne au sol dans un nuage, que le satellite qui regarde d’en haut peut manquer ?','Pourquoi GLOBE demande-t-il une formation sur un protocole avant d’entrer les données de ce protocole ?','GLOBE apparie les observations de nuages à des satellites comme GOES, Himawari, JPSS et PACE. Pourquoi l’heure de l’observation peut-elle compter ?'],
 idH='Repères pour le type de nuage', id='Les noms et les étapes sont sur le nuage-chart, le guide des types et le protocole Nuages de GLOBE. Utilisez-les, ainsi que l’application GLOBE Observer, plutôt qu’un tableau fait pour cette page.',
 dataH='Page de données de l’élève', dataIntro='Écris ton nom et la date. Puis utilise la feuille officielle Nuages d’une journée pour l’observation elle-même.',
 name='Nom', date='Date', **{'class':'Classe'}, notice='Une chose que j’ai remarquée dans le ciel',
 ngssH='Notes NGSS', ngss='Le guide NGSS de GLOBE place le protocole Nuages sur la page de maternelle pour K-ESS2-1. Il place aussi ce protocole et l’activité « Observing, Describing, and Identifying Clouds » sur la page du collège pour MS-ESS2-5. D’autres protocoles de l’atmosphère y figurent. Le PDF fait foi.',
 train='Depuis décembre 2025, un membre GLOBE termine une formation pour chaque protocole avant d’entrer des données pour ce protocole. La formation peut être une relecture du guide de terrain, un eTraining de collecte quand GLOBE en propose un, un Protocol eTraining complet, ou un atelier GLOBE.',
 buildH='Générateur de leçon', buildL='Choisis un niveau, un sujet GLOBE et une durée. Le plan renvoie à la page officielle du protocole et aux films officiels. Il ne copie pas les étapes de mesure.',
 band='Niveau', topic='Sujet', length='Durée',
 printSheet='Imprimer la fiche', printPlan='Imprimer le plan', copyLink='Copier le lien', copyPlan='Copier le plan', classroom='Partager sur Google Classroom', buildBtn='Créer le plan', standardsH='Normes', sourceGLOBE='Source : GLOBE', videoCredit='Crédits de la vidéo de titre :', appLink='Oui, tout de suite, prends ton application GLOBE',
 suggestH='Proposer une correction ou une autre solution', suggest='Écrivez au bureau des partenariats. Il n’y a pas de formulaire sur cette page.',
 src='Source',
 spheres={'atm':'Atmosphère','hyd':'Hydrosphère','ped':'Pédosphère (sol)','bio':'Biosphère','obs':'GLOBE Observer'},
 topics={'clouds':'Nuages','airtemp':'Température de l’air','precip':'Précipitations','watertemp':'Température de l’eau','ph':'pH de l’eau','mosquito':'Mosquito Habitat Mapper','soil':'Caractérisation du sol','landcover':'Couverture du sol','trees':'Arbres (biométrie et hauteur)','greenup':'Green-Up / Green-Down','observer':'Application GLOBE Observer'},
 bands={'k2':'Maternelle–2e','g35':'3e–5e','g68':'6e–8e','g912':'9e–12e'},
 lengths={'class':'Une période de cours','week':'Une semaine'},
 planH='Plan de leçon', planMeta='{name} · {band} · {length}',
 objH='Objectif', matH='Matériel', stepsH='Étapes', vidH='Films officiels', dataLab='Collecte des données', qLab='Discussion', ngssLab='NGSS',
 obj='Les élèves suivent les documents officiels GLOBE « {name} » pour {band}, sur {length}, et peuvent dire ce que le protocole demande d’observer.',
 steps='Ouvre la page officielle du protocole {name} et sers-t’en pour la mesure. Ce plan ne réécrit pas ces étapes.|Regarde un film officiel sur ce sujet, ou la vidéo du protocole sur la page vidéo de GLOBE.|Pour une période, fais une séance d’observation. Pour une semaine, ne répète que selon ce que la page du protocole permet.|Un adulte accompagne toute personne de moins de 13 ans. Un membre GLOBE termine la formation de ce protocole avant d’entrer des données.',
 data='Note l’observation sur la feuille de GLOBE ou dans l’application GLOBE Observer. Ne copie pas le formulaire de mesure dans ce plan.',
 questions=['Que demande la page officielle {name} à un observateur ?','Que faut-il faire avant d’entrer les données de ce protocole dans GLOBE ?','Quel film officiel ou quel guide vas-tu utiliser, et pourquoi ?'],
 ngssClouds='Pour les nuages, le guide de GLOBE associe le protocole à K-ESS2-1 et, avec l’activité « Observing, Describing, and Identifying Clouds », à la page de MS-ESS2-5. D’autres protocoles de l’atmosphère y figurent.',
 ngssGeneric='Cherche ce protocole dans le guide NGSS de GLOBE. Ce plan n’ajoute pas d’attentes que le guide ne montre pas.',
 ngssName='Connexions NGSS de GLOBE (PDF)', openProtocol='Page officielle du protocole', openTrain='eTraining GLOBE', openVideos='Vidéos pédagogiques GLOBE', openElem='Module Elementary GLOBE pour le primaire',
 wmvNote='C’est le film Windows Media de GLOBE, sur la page des vidéos pédagogiques.', noFilm='La page vidéo de GLOBE ne donne pas de film séparé pour ce protocole.',
 copied='Copié')

UI['es'] = tr(
 title='Ficha de nubes para el programa GLOBE',
 desc='Borrador de trabajo para el equipo del programa GLOBE: una ficha de nubes y un generador de lecciones que enlazan documentos y vídeos oficiales.',
 skip='Saltar al contenido',
 invite='Un borrador de trabajo para el equipo del programa GLOBE. Revísenlo, sugieran cambios, compartan ideas o indíquennos otras soluciones. Aprendemos unos de otros para mejorar la educación de todas las personas.',
 h1='Nubes para la clase',
 lead='Una ficha docente y un generador de lecciones que señalan los documentos y vídeos oficiales de GLOBE. Esta página añade herramientas prácticas alrededor de esos recursos. No los sustituye.',
 credit='Creado por el fundador y SI',
 show='Esta página muestra recursos oficiales de GLOBE para docentes. No es una alianza con GLOBE o la NASA, ni un respaldo de ninguna de las dos.',
 sheetH='Ficha de nubes', sumH='Para el alumnado',
 sum='GLOBE es un programa científico internacional. El protocolo de nubes indica cómo informar qué nubes se ven, cuánto cielo cubren, qué opacas se ven y cómo están el cielo y el suelo. Una clase puede hacerlo en el momento que le venga bien. Los satélites ven la parte de arriba de las nubes. Las personas en el suelo ven la de abajo.',
 whyH='Por qué importan las nubes',
 why='GLOBE dice que las observaciones de nubes ayudan a la NASA a entender los tipos de nubes y sus efectos en el clima de la Tierra. Juntar la vista desde el suelo y la del satélite da una imagen más completa.',
 doH='Qué hace el alumnado', do='El alumnado sigue los documentos de nubes de GLOBE. Esta ficha no reescribe los pasos de medición.',
 gradesH='Niveles', grades='El módulo de nubes de Elementary GLOBE es para primaria, de K a 4.º. De 5.º a 12.º se usan las actividades y las guías del protocolo de nubes. GLOBE dice que un adulto acompaña a quien tenga menos de 13 años.',
 qH='Preguntas para dialogar',
 qs=['¿Qué ve una persona en el suelo en una nube que un satélite, mirando hacia abajo, puede no ver?','¿Por qué GLOBE pide una formación del protocolo antes de introducir los datos de ese protocolo?','GLOBE empareja las observaciones de nubes con satélites como GOES, Himawari, JPSS y PACE. ¿Por qué puede importar la hora de la observación?'],
 idH='Guía rápida del tipo de nube', id='Los nombres y los pasos están en la carta de nubes, la guía de tipos y el protocolo de nubes de GLOBE. Usa esos documentos y la aplicación GLOBE Observer, no una tabla hecha para esta página.',
 dataH='Página de datos del alumno', dataIntro='Escribe tu nombre y la fecha. Después usa la hoja oficial de nubes de un día para la observación.',
 name='Nombre', date='Fecha', **{'class':'Clase'}, notice='Algo que noté en el cielo',
 ngssH='Notas NGSS', ngss='La guía NGSS de GLOBE sitúa el protocolo de nubes en la página de infantil para K-ESS2-1. También sitúa ese protocolo y la actividad «Observing, Describing, and Identifying Clouds» en la página de secundaria para MS-ESS2-5. En esas páginas hay otros protocolos de la atmósfera. El PDF manda.',
 train='Desde diciembre de 2025, un miembro de GLOBE completa una formación por cada protocolo antes de introducir datos de ese protocolo. La formación puede ser una lectura de la guía de campo, un eTraining de toma de datos cuando GLOBE lo ofrece, un Protocol eTraining completo o un taller de GLOBE.',
 buildH='Generador de lecciones', buildL='Elige un nivel, un tema de GLOBE y una duración. El plan enlaza la página oficial del protocolo y los vídeos oficiales. No copia los pasos de medición.',
 band='Nivel', topic='Tema', length='Duración',
 printSheet='Imprimir la ficha', printPlan='Imprimir el plan', copyLink='Copiar el enlace', copyPlan='Copiar el plan', classroom='Compartir en Google Classroom', buildBtn='Crear el plan', standardsH='Estándares', sourceGLOBE='Fuente: GLOBE', videoCredit='Créditos del vídeo de título:', appLink='Sí, ahora mismo consigue tu aplicación GLOBE',
 suggestH='Sugerir un cambio u otra solución', suggest='Escribe al equipo de alianzas. En esta página no hay formulario.',
 src='Fuente',
 spheres={'atm':'Atmósfera','hyd':'Hidrosfera','ped':'Pedosfera (suelo)','bio':'Biosfera','obs':'GLOBE Observer'},
 topics={'clouds':'Nubes','airtemp':'Temperatura del aire','precip':'Precipitación','watertemp':'Temperatura del agua','ph':'pH del agua','mosquito':'Mosquito Habitat Mapper','soil':'Caracterización del suelo','landcover':'Cobertura del suelo','trees':'Árboles (biometría y altura)','greenup':'Green-Up / Green-Down','observer':'Aplicación GLOBE Observer'},
 bands={'k2':'K-2','g35':'3.º-5.º','g68':'6.º-8.º','g912':'9.º-12.º'},
 lengths={'class':'Una clase','week':'Una semana'},
 planH='Plan de lección', planMeta='{name} · {band} · {length}',
 objH='Objetivo', matH='Materiales', stepsH='Pasos', vidH='Vídeos oficiales', dataLab='Toma de datos', qLab='Diálogo', ngssLab='NGSS',
 obj='El alumnado sigue los materiales oficiales de GLOBE sobre {name} para {band}, en {length}, y puede decir qué pide observar el protocolo.',
 steps='Abre la página oficial del protocolo {name} y úsala para la medición. Este plan no reescribe esos pasos.|Mira un vídeo oficial de este tema, o el vídeo del protocolo en la página de vídeos de GLOBE.|En una clase, haz una sesión de observación. En una semana, repite solo lo que permita la página del protocolo.|Un adulto acompaña a quien tenga menos de 13 años. Un miembro de GLOBE termina la formación de ese protocolo antes de introducir datos.',
 data='Anota la observación en la hoja de GLOBE o en la aplicación GLOBE Observer. No copies el formulario de medición en este plan.',
 questions=['¿Qué pide notar la página oficial de {name}?','¿Qué tiene que ocurrir antes de introducir en GLOBE los datos de este protocolo?','¿Qué vídeo oficial o qué guía vas a usar, y por qué?'],
 ngssClouds='Para las nubes, la guía de GLOBE relaciona el protocolo con K-ESS2-1 y, con la actividad «Observing, Describing, and Identifying Clouds», con la página de MS-ESS2-5. También lista otros protocolos de la atmósfera.',
 ngssGeneric='Busca este protocolo en la guía NGSS de GLOBE. Este plan no añade expectativas que la guía no muestre.',
 ngssName='Conexiones NGSS de GLOBE (PDF)', openProtocol='Página oficial del protocolo', openTrain='eTraining de GLOBE', openVideos='Vídeos de enseñanza de GLOBE', openElem='Módulo de Elementary GLOBE para primaria',
 wmvNote='Es el vídeo en Windows Media de GLOBE, en la página de vídeos de enseñanza.', noFilm='La página de vídeos de GLOBE no lista un vídeo aparte para este protocolo.',
 copied='Copiado')

UI['it'] = tr(
 title='Scheda nuvole per il programma GLOBE',
 desc='Bozza di lavoro per il team del programma GLOBE: una scheda sulle nuvole e un generatore di lezioni che collegano documenti e video ufficiali.',
 skip='Vai al contenuto',
 invite='Una bozza di lavoro per il team del programma GLOBE. Vi chiediamo di rivederla, suggerire modifiche, condividere idee o indicarci altre soluzioni. Impariamo gli uni dagli altri per migliorare l’istruzione di tutte e tutti.',
 h1='Nuvole in classe',
 lead='Una scheda per insegnanti e un generatore di lezioni che indicano i documenti e i video ufficiali di GLOBE. Questa pagina aggiunge strumenti pratici intorno a quelle risorse. Non le sostituisce.',
 credit='Creato dal fondatore e da SI',
 show='Questa pagina mostra risorse ufficiali GLOBE per gli insegnanti. Non è una partnership con GLOBE o la NASA, e non è un endorsement di nessuna delle due.',
 sheetH='Scheda nuvole', sumH='Per gli studenti',
 sum='GLOBE è un programma scientifico internazionale. Il protocollo Nuvole indica come segnalare quali nuvole si vedono, quanta parte del cielo coprono, quanto sembrano spesse e com’è il cielo e il suolo. Una classe può farlo nell’orario che le è comodo. I satelliti vedono la cima delle nuvole. Le persone a terra ne vedono la base.',
 whyH='Perché le nuvole contano',
 why='GLOBE dice che le osservazioni delle nuvole aiutano la NASA a capire i tipi di nuvole e gli effetti che hanno sul clima della Terra. Mettere insieme la vista da terra e quella dal satellite dà un quadro più completo.',
 doH='Che cosa fanno gli studenti', do='Gli studenti seguono i documenti Nuvole di GLOBE. Questa scheda non riscrive i passi di misura.',
 gradesH='Fasce di età', grades='Il modulo Nuvole di Elementary GLOBE è per la primaria, dalla scuola dell’infanzia alla quarta. Dalla quinta alla dodicesima si usano le attività e le guide del protocollo Nuvole. GLOBE dice che un adulto accompagna chi ha meno di 13 anni.',
 qH='Domande per la discussione',
 qs=['Che cosa vede una persona a terra in una nuvola, che un satellite dall’alto può non vedere?','Perché GLOBE chiede una formazione sul protocollo prima di inserire i dati di quel protocollo?','GLOBE abbina le osservazioni delle nuvole a satelliti come GOES, Himawari, JPSS e PACE. Perché l’ora dell’osservazione può contare?'],
 idH='Guida rapida al tipo di nuvola', id='I nomi e i passi stanno nella carta delle nuvole, nella guida ai tipi e nel protocollo Nuvole di GLOBE. Usa quelli e l’app GLOBE Observer, non una tabella fatta per questa pagina.',
 dataH='Pagina dati dello studente', dataIntro='Scrivi il nome e la data. Poi usa il foglio ufficiale delle nuvole di un giorno per l’osservazione.',
 name='Nome', date='Data', **{'class':'Classe'}, notice='Una cosa che ho notato nel cielo',
 ngssH='Note NGSS', ngss='La guida NGSS di GLOBE mette il protocollo Nuvole nella pagina della scuola dell’infanzia per K-ESS2-1. Mette anche quel protocollo e l’attività «Observing, Describing, and Identifying Clouds» nella pagina della scuola media per MS-ESS2-5. In quelle pagine ci sono altri protocolli dell’atmosfera. Fa fede il PDF.',
 train='Dal dicembre 2025, un membro GLOBE completa una formazione per ogni protocollo prima di inserire dati di quel protocollo. La formazione può essere una lettura della guida di campo, un eTraining di raccolta quando GLOBE lo offre, un Protocol eTraining completo o un laboratorio GLOBE.',
 buildH='Generatore di lezioni', buildL='Scegli una fascia, un tema GLOBE e una durata. Il piano collega la pagina ufficiale del protocollo e i video ufficiali. Non copia i passi di misura.',
 band='Fascia', topic='Tema', length='Durata',
 printSheet='Stampa la scheda', printPlan='Stampa il piano', copyLink='Copia il link', copyPlan='Copia il piano', classroom='Condividi su Google Classroom', buildBtn='Crea il piano', standardsH='Standard', sourceGLOBE='Fonte: GLOBE', videoCredit='Crediti del video del titolo:', appLink='Sì, prendi subito la tua app GLOBE',
 suggestH='Suggerisci una modifica o un’altra soluzione', suggest='Scrivi all’ufficio partnership. In questa pagina non c’è un modulo.',
 src='Fonte',
 spheres={'atm':'Atmosfera','hyd':'Idrosfera','ped':'Pedosfera (suolo)','bio':'Biosfera','obs':'GLOBE Observer'},
 topics={'clouds':'Nuvole','airtemp':'Temperatura dell’aria','precip':'Precipitazioni','watertemp':'Temperatura dell’acqua','ph':'pH dell’acqua','mosquito':'Mosquito Habitat Mapper','soil':'Caratterizzazione del suolo','landcover':'Copertura del suolo','trees':'Alberi (biometria e altezza)','greenup':'Green-Up / Green-Down','observer':'App GLOBE Observer'},
 bands={'k2':'Infanzia–2ª','g35':'3ª–5ª','g68':'6ª–8ª','g912':'9ª–12ª'},
 lengths={'class':'Una lezione','week':'Una settimana'},
 planH='Piano di lezione', planMeta='{name} · {band} · {length}',
 objH='Obiettivo', matH='Materiali', stepsH='Passi', vidH='Video ufficiali', dataLab='Raccolta dati', qLab='Discussione', ngssLab='NGSS',
 obj='Gli studenti seguono i materiali ufficiali GLOBE su {name} per {band}, in {length}, e sanno dire che cosa il protocollo chiede di osservare.',
 steps='Apri la pagina ufficiale del protocollo {name} e usala per la misura. Questo piano non riscrive quei passi.|Guarda un video ufficiale su questo tema, o il video del protocollo nella pagina video di GLOBE.|In una lezione, fai una sessione di osservazione. In una settimana, ripeti solo quanto consente la pagina del protocollo.|Un adulto accompagna chi ha meno di 13 anni. Un membro GLOBE completa la formazione di quel protocollo prima di inserire i dati.',
 data='Annota l’osservazione sul foglio di GLOBE o nell’app GLOBE Observer. Non copiare il modulo di misura in questo piano.',
 questions=['Che cosa chiede di notare la pagina ufficiale di {name}?','Che cosa deve succedere prima di inserire in GLOBE i dati di questo protocollo?','Quale video ufficiale o quale guida userai, e perché?'],
 ngssClouds='Per le nuvole, la guida di GLOBE collega il protocollo a K-ESS2-1 e, con l’attività «Observing, Describing, and Identifying Clouds», alla pagina di MS-ESS2-5. Vi compaiono anche altri protocolli dell’atmosfera.',
 ngssGeneric='Cerca questo protocollo nella guida NGSS di GLOBE. Questo piano non aggiunge aspettative che la guida non mostra.',
 ngssName='Collegamenti NGSS di GLOBE (PDF)', openProtocol='Pagina ufficiale del protocollo', openTrain='eTraining GLOBE', openVideos='Video didattici GLOBE', openElem='Modulo Elementary GLOBE per la primaria',
 wmvNote='È il filmato Windows Media di GLOBE, nella pagina dei video didattici.', noFilm='La pagina video di GLOBE non elenca un filmato a parte per questo protocollo.',
 copied='Copiato')

UI['ar'] = tr(
 title='ورقة السحب لبرنامج GLOBE',
 desc='مسودة عمل لفريق برنامج GLOBE: ورقة عن السحب ومنشئ دروس يربطان بالوثائق والأفلام الرسمية.',
 skip='تخطٍ إلى المحتوى',
 invite='مسودة عمل لفريق برنامج GLOBE. نرجو مراجعتها واقتراح التعديلات ومشاركة الأفكار أو إرشادنا إلى حلول إضافية. نتعلم من بعضنا لنحسّن التعليم للجميع.',
 h1='السحب في الصف',
 lead='ورقة للمعلم ومنشئ دروس يشيران إلى وثائق GLOBE وأفلامها الرسمية. تضيف هذه الصفحة أدوات عملية حول تلك الموارد. وهي لا تحل محلها.',
 credit='من إعداد المؤسس وSI',
 show='تعرض هذه الصفحة موارد GLOBE الرسمية للمعلمين. وهي ليست شراكة مع GLOBE أو ناسا، وليست تزكية من أي منهما.',
 sheetH='ورقة السحب', sumH='للطلاب',
 sum='GLOBE برنامج علمي دولي. يبيّن بروتوكول السحب كيف يُبلّغ الراصد عن أنواع السحب الظاهرة، ومقدار ما تغطيه من السماء، ومدى كثافتها، وحال السماء والأرض. يمكن للصف أن يفعل ذلك في الوقت الذي يناسبه. ترى الأقمار الصناعية أعالي السحب. ويرى الناس على الأرض أسفلها.',
 whyH='لماذا تهم السحب',
 why='يقول GLOBE إن رصد السحب يساعد ناسا على فهم أنواع السحب وأثرها في مناخ الأرض. جمع رؤية الأرض ورؤية القمر الصناعي يعطي صورة أوفى.',
 doH='ماذا يفعل الطلاب', do='يتبع الطلاب وثائق السحب الخاصة بـ GLOBE. لا تعيد هذه الورقة كتابة خطوات القياس.',
 gradesH='المراحل', grades='وحدة السحب في Elementary GLOBE للصفوف الابتدائية من الروضة حتى الرابع. من الصف الخامس حتى الثاني عشر تُستخدم أنشطة بروتوكول السحب وأدلته. يقول GLOBE إن من هم دون 13 عامًا يرافقهم بالغ.',
 qH='أسئلة للنقاش',
 qs=['ماذا يرى شخص على الأرض في السحابة وقد لا يراه قمر صناعي ينظر من الأعلى؟','لماذا يطلب GLOBE تدريبًا على البروتوكول قبل إدخال بياناته؟','يطابق GLOBE رصد السحب مع أقمار مثل GOES وHimawari وJPSS وPACE. لماذا قد يهم وقت الرصد؟'],
 idH='دليل سريع لنوع السحابة', id='الأسماء والخطوات موجودة في مخطط سحب GLOBE ودليل الأنواع وبروتوكول السحب. استخدموا هذه وتطبيق GLOBE Observer، لا جدولًا صُنع لهذه الصفحة.',
 dataH='صفحة بيانات الطالب', dataIntro='اكتب اسمك والتاريخ. ثم استخدم ورقة بيانات السحب الرسمية ليوم واحد للرصد نفسه.',
 name='الاسم', date='التاريخ', **{'class':'الصف'}, notice='شيء لاحظته في السماء',
 ngssH='ملاحظات NGSS', ngss='يضع دليل NGSS لدى GLOBE بروتوكول السحب في صفحة الروضة للمعيار K-ESS2-1. ويضع البروتوكول ونشاط Observing, Describing, and Identifying Clouds في صفحة المرحلة المتوسطة للمعيار MS-ESS2-5. وتظهر في تلك الصفحات بروتوكولات جو أخرى. المرجع هو ملف PDF.',
 train='منذ ديسمبر 2025، يكمل عضو GLOBE تدريبًا واحدًا لكل بروتوكول قبل إدخال بيانات ذلك البروتوكول. قد يكون التدريب مراجعة لدليل الميدان، أو eTraining لجمع البيانات حين يوفّره GLOBE، أو Protocol eTraining كاملًا، أو ورشة GLOBE.',
 buildH='منشئ الدروس', buildL='اختر مرحلة وموضوعًا من GLOBE ومدة. تربط الخطة بصفحة البروتوكول الرسمية والأفلام الرسمية. وهي لا تنسخ خطوات القياس.',
 band='المرحلة', topic='الموضوع', length='المدة',
 printSheet='اطبع ورقة المعلم', printPlan='طباعة الخطة', copyLink='نسخ الرابط', copyPlan='انسخ الخطة', classroom='المشاركة في Google Classroom', buildBtn='أنشئ الخطة', standardsH='المعايير', sourceGLOBE='المصدر: GLOBE', videoCredit='اعتمادات فيديو العنوان:', appLink='نعم، احصل على تطبيق GLOBE الآن',
 suggestH='اقترح تعديلًا أو حلًا آخر', suggest='اكتب إلى مكتب الشراكات. لا يوجد نموذج في هذه الصفحة.',
 src='المصدر',
 spheres={'atm':'الغلاف الجوي','hyd':'الغلاف المائي','ped':'غلاف التربة','bio':'المحيط الحيوي','obs':'GLOBE Observer'},
 topics={'clouds':'السحب','airtemp':'درجة حرارة الهواء','precip':'الهطول','watertemp':'درجة حرارة الماء','ph':'الأس الهيدروجيني للماء','mosquito':'Mosquito Habitat Mapper','soil':'وصف التربة','landcover':'الغطاء الأرضي','trees':'الأشجار (القياسات والارتفاع)','greenup':'الاخضرار وتساقط الأوراق','observer':'تطبيق GLOBE Observer'},
 bands={'k2':'الروضة–2','g35':'3–5','g68':'6–8','g912':'9–12'},
 lengths={'class':'حصة واحدة','week':'أسبوع واحد'},
 planH='خطة الدرس', planMeta='{name} · {band} · {length}',
 objH='الهدف', matH='المواد', stepsH='الخطوات', vidH='أفلام رسمية', dataLab='جمع البيانات', qLab='النقاش', ngssLab='NGSS',
 obj='يتبع الطلاب مواد GLOBE الرسمية عن {name} للمرحلة {band} خلال {length}، ويستطيعون أن يقولوا ماذا يطلب البروتوكول رصده.',
 steps='افتح صفحة بروتوكول {name} الرسمية واستخدمها للقياس. لا تعيد هذه الخطة كتابة تلك الخطوات.|شاهد فيلمًا رسميًا عن هذا الموضوع، أو فيديو البروتوكول في صفحة فيديوهات GLOBE.|في حصة واحدة، اجعل جلسة رصد واحدة. في أسبوع، كرر فقط بالقدر الذي تسمح به صفحة البروتوكول.|يرافق بالغ كل من هو دون 13 عامًا. ويكمل عضو GLOBE تدريب ذلك البروتوكول قبل إدخال البيانات.',
 data='سجّل الرصد في ورقة GLOBE أو في تطبيق GLOBE Observer. لا تنسخ نموذج القياس إلى هذه الخطة.',
 questions=['ماذا تطلب صفحة {name} الرسمية من الراصد أن يلاحظ؟','ماذا يجب أن يحدث قبل إدخال بيانات هذا البروتوكول في GLOBE؟','أي فيلم رسمي أو دليل ستستخدم، ولماذا؟'],
 ngssClouds='بالنسبة إلى السحب، يربط دليل GLOBE البروتوكول بـ K-ESS2-1، ومع نشاط Observing, Describing, and Identifying Clouds بصفحة MS-ESS2-5. وتُذكر بروتوكولات جو أخرى هناك أيضًا.',
 ngssGeneric='ابحث عن هذا البروتوكول في دليل NGSS لدى GLOBE. لا تضيف هذه الخطة توقعات لا يظهرها الدليل.',
 ngssName='روابط NGSS لدى GLOBE (PDF)', openProtocol='صفحة البروتوكول الرسمية', openTrain='تدريب GLOBE الإلكتروني', openVideos='فيديوهات GLOBE التعليمية', openElem='وحدة Elementary GLOBE للمرحلة الابتدائية',
 wmvNote='هذا فيلم Windows Media من GLOBE في صفحة الفيديوهات التعليمية.', noFilm='لا تعرض صفحة فيديوهات GLOBE فيلمًا مستقلًا لهذا البروتوكول.',
 copied='تم النسخ')

UI['he'] = tr(
 title='דף עננים לתוכנית GLOBE',
 desc='טיוטת עבודה לצוות תוכנית GLOBE: דף עננים ומחולל שיעורים שמקשרים למסמכים ולסרטים הרשמיים.',
 skip='דילוג לתוכן',
 invite='טיוטת עבודה לצוות תוכנית GLOBE. נשמח שתעיינו, תציעו תיקונים, תשתפו רעיונות או תפנו אותנו לפתרונות נוספים. אנחנו לומדים זה מזה כדי לשפר את החינוך לכולם.',
 h1='עננים לכיתה',
 lead='דף למורה ומחולל שיעורים שמצביעים על המסמכים והסרטים הרשמיים של GLOBE. העמוד מוסיף כלים מעשיים סביב המשאבים האלה. הוא לא מחליף אותם.',
 credit='נוצר על ידי המייסד ו-SI',
 show='העמוד מציג משאבים רשמיים של GLOBE למורים. אין כאן שותפות עם GLOBE או עם נאס״א, ואין כאן חסות או אישור מטעמם.',
 sheetH='דף עננים', sumH='לתלמידים',
 sum='GLOBE היא תוכנית מדע בין-לאומית. פרוטוקול העננים מסביר איך לדווח אילו עננים רואים, כמה מהשמיים הם מכסים, כמה הם נראים סמיכים, ומה מצב השמיים והקרקע. כיתה יכולה לעשות זאת בזמן שמתאים לה. לוויינים רואים את ראש הענן. אנשים על הקרקע רואים את תחתיתו.',
 whyH='למה עננים חשובים',
 why='GLOBE אומרת שתצפיות עננים עוזרות לנאס״א להבין סוגי עננים ואת ההשפעה שלהם על האקלים של כדור הארץ. חיבור המבט מהקרקע למבט מהלוויין נותן תמונה מלאה יותר.',
 doH='מה התלמידים עושים', do='התלמידים עובדים לפי מסמכי העננים של GLOBE. הדף הזה לא משכתב את שלבי המדידה.',
 gradesH='שכבות גיל', grades='מודול העננים של Elementary GLOBE מיועד לכיתות היסוד, מגן ועד כיתה ד׳. מכיתה ה׳ עד י״ב משתמשים בפעילויות ובמדריכים של פרוטוקול העננים. GLOBE אומרת שמבוגר מלווה ילדים מתחת לגיל 13.',
 qH='שאלות לדיון',
 qs=['מה אדם על הקרקע רואה בענן, ולוויין שמביט מלמעלה עלול לפספס?','למה GLOBE מבקשת הכשרה לפרוטוקול לפני שמזינים את הנתונים שלו?','GLOBE מתאימה תצפיות עננים ללוויינים כמו GOES,‏ Himawari,‏ JPSS ו-PACE. למה שעת התצפית יכולה להיות חשובה?'],
 idH='מדריך קצר לסוג הענן', id='השמות והשלבים נמצאים במפת העננים, במדריך הסוגים ובפרוטוקול העננים של GLOBE. השתמשו בהם וביישומון GLOBE Observer, לא בטבלה שנכתבה לעמוד הזה.',
 dataH='דף נתונים לתלמיד', dataIntro='כתבו שם ותאריך. אחר כך השתמשו בדף הנתונים הרשמי של עננים ליום אחד עבור התצפית עצמה.',
 name='שם', date='תאריך', **{'class':'כיתה'}, notice='דבר אחד ששמתי לב אליו בשמיים',
 ngssH='הערות NGSS', ngss='מדריך ה-NGSS של GLOBE מציב את פרוטוקול העננים בעמוד של גן הילדים עבור K-ESS2-1. הוא מציב גם את הפרוטוקול ואת הפעילות Observing, Describing, and Identifying Clouds בעמוד חטיבת הביניים עבור MS-ESS2-5. בעמודים האלה מופיעים גם פרוטוקולים אחרים של האטמוספרה. קובץ ה-PDF הוא המקור.',
 train='מדצמבר 2025, חבר GLOBE משלים הכשרה אחת לכל פרוטוקול לפני הזנת נתונים של אותו פרוטוקול. ההכשרה יכולה להיות קריאה של מדריך השדה, eTraining לאיסוף נתונים כש-GLOBE מציעה אותו, Protocol eTraining מלא, או סדנה של GLOBE.',
 buildH='מחולל שיעורים', buildL='בחרו שכבת גיל, נושא של GLOBE ומשך. התוכנית מקשרת לעמוד הפרוטוקול הרשמי ולסרטים הרשמיים. היא לא מעתיקה את שלבי המדידה.',
 band='שכבה', topic='נושא', length='משך',
 printSheet='הדפסת דף המורה', printPlan='הדפסת התוכנית', copyLink='העתקת הקישור', copyPlan='העתקת התוכנית', classroom='שיתוף ב-Google Classroom', buildBtn='בניית התוכנית', standardsH='תקנים', sourceGLOBE='מקור: GLOBE', videoCredit='קרדיטים לסרטון הכותרת:', appLink='כן, קבלו עכשיו את יישומון GLOBE',
 suggestH='הצעת תיקון או פתרון נוסף', suggest='כתבו אל שולחן השותפויות. אין טופס בעמוד הזה.',
 src='מקור',
 spheres={'atm':'אטמוספרה','hyd':'הידרוספרה','ped':'פדוספרה (קרקע)','bio':'ביוספרה','obs':'GLOBE Observer'},
 topics={'clouds':'עננים','airtemp':'טמפרטורת אוויר','precip':'משקעים','watertemp':'טמפרטורת מים','ph':'pH של מים','mosquito':'Mosquito Habitat Mapper','soil':'אפיון קרקע','landcover':'כיסוי קרקע','trees':'עצים (ביומטריה וגובה)','greenup':'לבלוב ונשירה','observer':'יישומון GLOBE Observer'},
 bands={'k2':'גן–ב׳','g35':'ג׳–ה׳','g68':'ו׳–ח׳','g912':'ט׳–י״ב'},
 lengths={'class':'שיעור אחד','week':'שבוע אחד'},
 planH='מערך שיעור', planMeta='{name} · {band} · {length}',
 objH='מטרה', matH='חומרים', stepsH='שלבים', vidH='סרטים רשמיים', dataLab='איסוף נתונים', qLab='דיון', ngssLab='NGSS',
 obj='התלמידים עובדים לפי החומרים הרשמיים של GLOBE על {name} עבור {band}, במשך {length}, ויכולים לומר מה הפרוטוקול מבקש לצפות.',
 steps='פתחו את העמוד הרשמי של פרוטוקול {name} והשתמשו בו למדידה. המערך הזה לא משכתב את השלבים.|צפו בסרט רשמי בנושא, או בסרטון הפרוטוקול בעמוד הסרטים של GLOBE.|בשיעור אחד ערכו מפגש תצפית אחד. בשבוע, חזרו רק בתדירות שהעמוד של הפרוטוקול מתיר.|מבוגר מלווה כל מי שמתחת לגיל 13. חבר GLOBE מסיים את ההכשרה של הפרוטוקול לפני הזנת נתונים.',
 data='רשמו את התצפית בדף של GLOBE או ביישומון GLOBE Observer. אל תעתיקו את טופס המדידה למערך הזה.',
 questions=['מה העמוד הרשמי של {name} מבקש מהצופה לשים לב אליו?','מה צריך לקרות לפני שמזינים ל-GLOBE את הנתונים של הפרוטוקול הזה?','באיזה סרט רשמי או מדריך תשתמשו, ולמה?'],
 ngssClouds='לעננים, המדריך של GLOBE מקשר את הפרוטוקול ל-K-ESS2-1, ועם הפעילות Observing, Describing, and Identifying Clouds לעמוד של MS-ESS2-5. מופיעים שם גם פרוטוקולים אחרים של האטמוספרה.',
 ngssGeneric='חפשו את הפרוטוקול במדריך ה-NGSS של GLOBE. המערך הזה לא מוסיף ציפיות שהמדריך לא מציג.',
 ngssName='קישורי NGSS של GLOBE ‏(PDF)', openProtocol='העמוד הרשמי של הפרוטוקול', openTrain='ההכשרה המקוונת של GLOBE', openVideos='סרטי ההדרכה של GLOBE', openElem='מודול Elementary GLOBE ליסודי',
 wmvNote='זהו סרט Windows Media של GLOBE מעמוד סרטי ההדרכה.', noFilm='בעמוד הסרטים של GLOBE אין סרט נפרד לפרוטוקול הזה.',
 copied='הועתק')

def sheet(u, prefix):
    q = ''.join(f'<li>{E(x)}</li>' for x in u['qs'])
    return f'''<p class="gr-banner" role="note">{E(u['invite'])}</p>
<section class="gr-hero" id="sheet" style="background-image:url('{prefix}assets/Pacific_Clouds_Sunset_ISS.jpg')">
<div class="page-hero-content"><h1>{E(u['h1'])}</h1><p>{E(u['lead'])}</p><p class="gr-founder">{E(u['credit'])}</p></div>
<p class="hero-credit">NASA (ISS074-E-0046371, Jan. 3, 2026)</p>
</section>
<div class="gr-wrap">
<p class="gr-note">{E(u['show'])}</p>
<p class="hero-ctas"><button type="button" class="hero-cta" id="gr-print-sheet">{E(u['printSheet'])}</button></p>
<section class="gr-card" aria-labelledby="sum-h"><h2 id="sum-h">{E(u['sheetH'])}</h2>
<h3>{E(u['sumH'])}</h3><p>{E(u['sum'])}</p>
<p class="gr-src">{E(u['src'])}: {A('https://www.globe.gov/web/atmosphere/protocols/clouds','Clouds — Atmosphere — GLOBE.gov')}</p>
<h3>{E(u['whyH'])}</h3><p>{E(u['why'])}</p>
<p class="gr-src">{E(u['src'])}: {A('https://www.globe.gov/web/atmosphere/protocols/clouds','GLOBE Clouds protocol')}</p>
<h3>{E(u['doH'])}</h3><p>{E(u['do'])}</p>
<ul>
<li>{A('https://www.globe.gov/web/atmosphere/protocols/clouds','Clouds protocol page')}</li>
<li>{A('https://www.globe.gov/documents/348614/7b79ee82-ebd6-4382-9283-181a412f063f','Clouds protocol PDF')}</li>
<li>{A('https://www.globe.gov/documents/348614/139cd526-ca0b-4192-9659-ad9ee5a5c893','Cloud type field guide')}</li>
<li>{A('https://www.globe.gov/documents/348614/1c29caf7-fb2f-4414-8b43-11fd64087ea8','Cloud cover field guide')}</li>
<li>{A('https://www.globe.gov/documents/348614/3d557e09-3bd9-4bc2-8b75-a0288a064cd1','Cloud opacity field guide')}</li>
<li>{A('https://www.globe.gov/documents/348614/782194b1-b5c3-4416-b3aa-b4a208ea5812','GLOBE cloud chart')}</li>
<li>{A('https://www.globe.gov/documents/348614/381dac63-2770-4517-95ab-275a2effcf9f','Cloud Watch')}</li>
<li>{A('https://www.globe.gov/documents/348614/d58984c8-381c-4783-ad30-221fc381d619','Estimating Cloud Cover')}</li>
<li>{A('https://www.globe.gov/web/elementary-globe/overview/clouds','Elementary GLOBE Clouds')}</li>
<li>{A('https://observer.globe.gov/','GLOBE Observer')}</li>
<li>{A('https://www.globe.gov/get-involved/training/globe-etraining','GLOBE eTraining')}</li>
</ul>
<h3>{E(u['gradesH'])}</h3><p>{E(u['grades'])}</p>
<p class="gr-src">{E(u['src'])}: {A('https://www.globe.gov/web/elementary-globe','Elementary GLOBE')} · {A('https://www.globe.gov/get-involved/join-globe/get-the-app','GLOBE, Get the App')}</p>
<h3>{E(u['qH'])}</h3><ol>{q}</ol>
<h3>{E(u['idH'])}</h3><p>{E(u['id'])}</p>
<h3>{E(u['dataH'])}</h3><p>{E(u['dataIntro'])}</p>
<div class="gr-data">
<p><label>{E(u['name'])}</label><span class="gr-line"></span></p>
<p><label>{E(u['date'])}</label><span class="gr-line"></span></p>
<p><label>{E(u['class'])}</label><span class="gr-line"></span></p>
<p><label>{E(u['notice'])}</label><span class="gr-line"></span><span class="gr-line"></span></p>
<p>{A('https://www.globe.gov/documents/348614/624fab53-4159-438e-b974-4a79c402c3cb','Clouds 1-Day Data Sheet 2017 (PDF)')}</p>
</div>
<h3>{E(u['ngssH'])}</h3><p>{E(u['ngss'])}</p>
<p class="gr-src">{E(u['src'])}: {A('https://www.globe.gov/documents/2629866/0/ConnectionsGLOBE_NGSS.pdf','Connections between the GLOBE Program and the NGSS (PDF)')}</p>
<h3>Training</h3><p>{E(u['train'])}</p>
<p class="gr-src">{E(u['src'])}: {A('https://www.globe.gov/get-involved/training/globe-etraining','GLOBE eTraining')}</p>
</section>
<section class="gr-card gr-builder" id="plan" aria-labelledby="build-h">
<h2 id="build-h">{E(u['buildH'])}</h2>
<p>{E(u['buildL'])}</p>
<form id="gr-form" class="gr-form">
<label>{E(u['band'])}<select name="band"><option value="k2">{E(u['bands']['k2'])}</option><option value="g35">{E(u['bands']['g35'])}</option><option value="g68">{E(u['bands']['g68'])}</option><option value="g912">{E(u['bands']['g912'])}</option></select></label>
<label>{E(u['topic'])}<select name="topic"></select></label>
<label>{E(u['length'])}<select name="length"><option value="class">{E(u['lengths']['class'])}</option><option value="week">{E(u['lengths']['week'])}</option></select></label>
</form>
<div class="gr-actions hero-ctas">
<button type="button" class="hero-cta" id="gr-print-plan">{E(u['printPlan'])}</button>
<button type="button" class="hero-cta" id="gr-copy-plan">{E(u['copyPlan'])}</button>
<button type="button" class="hero-cta" id="gr-copy">{E(u['copyLink'])}</button>
</div>
<div id="gr-plan" class="gr-plan" aria-live="polite"></div>
</section>
<section class="gr-card" id="suggest"><h2>{E(u['suggestH'])}</h2><p>{E(u['suggest'])}</p>
<p class="hero-ctas"><a class="hero-cta" href="mailto:partner-relations@savingplanets.com?subject=GLOBE%20review">partner-relations@savingplanets.com</a></p>
</section>
<p class="gr-legal">{E(u['cite'])}</p>
<script type="application/json" id="gr-i18n">{json.dumps({k:u[k] for k in ('spheres','topics','bands','lengths','planH','planMeta','objH','matH','stepsH','vidH','dataLab','qLab','ngssLab','obj','steps','data','questions','ngssClouds','ngssGeneric','ngssName','openProtocol','openTrain','openVideos','openElem','wmvNote','noFilm','copied','qH')}, ensure_ascii=False)}</script>
</div>
'''

# The submit button label was clumsily set to the builder heading. Fix in sheet() by using a dedicated phrase.
# I'll set it from buildH only as "Show the plan" equivalents already in buildH. Leave the first button as the heading word is odd.
# Replace that button with a simpler one after generation if needed. I'll change the template now by editing the string above... 
# The line uses u['buildH'] which is "Lesson builder". That's an OK button: it updates the plan on submit. Acceptable.

EXTRA = {
'en': {
 'sheetKicker': 'Teacher sheet',
 'filmLead': 'Watch this official film with the sheet. The measurement steps stay on the protocol page.',
 'dataLead': 'Record the observation on GLOBE’s own data sheet or in the GLOBE Observer app, and only after that protocol’s training.',
 'talkLead': 'Use the film to ask what the protocol wants students to notice, and what must happen before anyone enters data.',
},
'fr': {
 'sheetKicker': 'Fiche enseignant',
 'filmLead': 'Regardez ce film officiel avec la fiche. Les étapes de mesure restent sur la page du protocole.',
 'dataLead': 'Notez l’observation sur la feuille de GLOBE ou dans l’application GLOBE Observer, et seulement après la formation de ce protocole.',
 'talkLead': 'À partir du film, demandez ce que le protocole veut que les élèves remarquent, et ce qui doit se passer avant d’entrer des données.',
},
'es': {
 'sheetKicker': 'Ficha docente',
 'filmLead': 'Ved este vídeo oficial con la ficha. Los pasos de medición siguen en la página del protocolo.',
 'dataLead': 'Anotad la observación en la hoja de GLOBE o en la aplicación GLOBE Observer, y solo después de la formación de ese protocolo.',
 'talkLead': 'Con el vídeo, preguntad qué quiere el protocolo que el alumnado note y qué tiene que ocurrir antes de introducir datos.',
},
'it': {
 'sheetKicker': 'Scheda docente',
 'filmLead': 'Guardate questo filmato ufficiale con la scheda. I passi di misura restano sulla pagina del protocollo.',
 'dataLead': 'Annotate l’osservazione sul foglio di GLOBE o nell’app GLOBE Observer, e solo dopo la formazione di quel protocollo.',
 'talkLead': 'Dal filmato, chiedete che cosa il protocollo vuole che gli studenti notino, e che cosa deve succedere prima di inserire i dati.',
},
'ar': {
 'sheetKicker': 'ورقة المعلم',
 'filmLead': 'شاهدوا هذا الفيلم الرسمي مع الورقة. تبقى خطوات القياس في صفحة البروتوكول.',
 'dataLead': 'سجّلوا الرصد في ورقة GLOBE أو في تطبيق GLOBE Observer، وبعد تدريب ذلك البروتوكول فقط.',
 'talkLead': 'استخدموا الفيلم لتسألوا ماذا يريد البروتوكول أن يلاحظ الطلاب، وما الذي يجب أن يحدث قبل إدخال البيانات.',
},
'he': {
 'sheetKicker': 'דף מורה',
 'filmLead': 'צפו בסרט הרשמי הזה עם הדף. שלבי המדידה נשארים בעמוד הפרוטוקול.',
 'dataLead': 'רשמו את התצפית בדף של GLOBE או ביישומון GLOBE Observer, ורק אחרי ההכשרה של הפרוטוקול.',
 'talkLead': 'בעזרת הסרט שאלו מה הפרוטוקול רוצה שהתלמידים יבחינו בו, ומה חייב לקרות לפני הזנת נתונים.',
},
}
for _lang, _extra in EXTRA.items():
    UI[_lang].update(_extra)

def install_video(chunk, prefix, credit_label):
    """Replace the still slideshow with one credited 1080p loop. Keep the program title and lead."""
    content = re.search(r'<div class="page-hero-content">.*?</div>', chunk, re.S)
    if not content:
        raise SystemExit('hero title missing')
    content_html = content.group(0).replace('<p>', '<p class="gr-lead">', 1)
    credit = ('NASA/GSFC, Earth from Orbit (2012); NASA (ISS071-E-449837, July 24, 2024); '
              'NASA/Shane Kimbrough (ISS065-E-144117, June 23, 2021); '
              'NASA/Glenn Benson (KSC-20230412-PH-GEB01_0006). Public domain.')
    poster = f'{prefix}assets/videos/globe-review-poster.jpg'
    src = f'{prefix}assets/videos/globe-review-hero.mp4'
    return f'''<section class="page-hero space-hero pg-anim has-video gr-hero">
<div class="hero-media" aria-hidden="true"><img class="gr-hero-still" src="{poster}" alt="" width="1920" height="1080"><video class="hero-video gr-hero-video" muted loop playsinline preload="none" poster="{poster}" width="1920" height="1080"><source data-src="{src}" type="video/mp4"></video><div class="hero-overlay"></div></div>
{content_html}
<p class="gr-vid-credit">{E(credit_label)} {credit}</p>
</section>
<script>(function(){{var v=document.querySelector(".gr-hero-video");if(!v)return;var mq=window.matchMedia("(prefers-reduced-motion: reduce)");function rate(){{if(!mq.matches)v.playbackRate=1.25;}}function arm(){{if(mq.matches){{v.pause();v.removeAttribute("autoplay");return;}}var s=v.querySelector("source");if(s&&!s.getAttribute("src")){{s.src=s.getAttribute("data-src");v.load();}}rate();var p=v.play();if(p&&p.catch)p.catch(function(){{}});}}v.addEventListener("loadedmetadata",rate);if(document.readyState==="complete")arm();else window.addEventListener("load",arm);}})();</script>
'''

def drop_sunset(hero):
    """Drop the horizon sunset slide. Keep the other three and retarget the 3-slide animation."""
    if 'Pacific_Clouds_Sunset_ISS' not in hero:
        raise SystemExit('sunset slide not in hero')
    hero = re.sub(r'<div class="spx-slide spx-0" aria-hidden="true"><picture class="spb-media">.*?Pacific_Clouds_Sunset_ISS.*?</picture></div>', '', hero, count=1, flags=re.S)
    if 'Pacific_Clouds_Sunset_ISS' in hero.split('spx-cred')[0]:
        raise SystemExit('sunset slide still present')
    for old, new in (('spx-3', 'spx-T2'), ('spx-2', 'spx-T1'), ('spx-1', 'spx-T0')):
        hero = hero.replace(old, new)
    for old, new in (('spx-T2', 'spx-2'), ('spx-T1', 'spx-1'), ('spx-T0', 'spx-0')):
        hero = hero.replace(old, new)
    hero = re.sub(r'<span class="hero-credit spx-cred spx-c0">.*?</span>', '', hero, count=1)
    for old, new in (('spx-c3', 'spx-CT2'), ('spx-c2', 'spx-CT1'), ('spx-c1', 'spx-CT0')):
        hero = hero.replace(old, new)
    for old, new in (('spx-CT2', 'spx-c2'), ('spx-CT1', 'spx-c1'), ('spx-CT0', 'spx-c0')):
        hero = hero.replace(old, new)
    hero = hero.replace('spx-n4', 'spx-n3', 1)
    first = re.search(r'<span class="hero-credit spx-cred spx-c0">(.*?)</span>', hero)
    if not first:
        raise SystemExit('first credit missing')
    credit = first.group(1)
    def _credit(m):
        body = m.group(2)
        cut = body.find('NASA')
        prefix = body[:cut] if cut >= 0 else ''
        if prefix and not prefix.endswith((' ', '\u00a0', '\u200f')):
            prefix += ' '
        return m.group(1) + prefix + credit + '.' + m.group(3)
    hero2, n = re.subn(r'(<p class="photo-credit">)(.*?)(</p>)', _credit, hero, count=1)
    if n != 1 or 'ISS071-E-449837' not in hero2:
        raise SystemExit('photo credit was not retargeted')
    return hero2

def builder(u):
    keys = ('spheres','topics','bands','lengths','objH','matH','stepsH','vidH','dataLab','qLab','ngssH','standardsH','sourceGLOBE',
            'obj','steps','filmLead','dataLead','talkLead','ngssClouds','ngssGeneric','sheetKicker','cite','credit',
            'openProtocol','openTrain','openElem')
    blob = json.dumps({k: u[k] for k in keys}, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<div class="edu-wrap" id="plan">
<h2 id="build-h">{E(u['buildH'])}</h2>
<p class="edu-lead gr-build-lead">{E(u['buildL'])}</p>
<form id="lb" class="lb-form glass" data-tint="earth">
<div><label for="lb-band">{E(u['band'])}</label><select id="lb-band" name="band"><option value="k2">{E(u['bands']['k2'])}</option><option value="g35">{E(u['bands']['g35'])}</option><option value="g68">{E(u['bands']['g68'])}</option><option value="g912">{E(u['bands']['g912'])}</option></select></div>
<div><label for="lb-topic">{E(u['topic'])}</label><select id="lb-topic" name="topic"></select></div>
<div><label for="lb-len">{E(u['length'])}</label><select id="lb-len" name="length"><option value="class">{E(u['lengths']['class'])}</option><option value="week">{E(u['lengths']['week'])}</option></select></div>
<div class="hero-ctas gr-actions"><button type="submit" class="btn hero-cta" id="gr-build">{E(u['buildBtn'])}</button></div>
</form>
<div class="lb-actions hero-ctas gr-actions">
<button type="button" class="btn hero-cta" id="lb-print">{E(u['printPlan'])}</button>
<button type="button" class="btn hero-cta" id="gr-copy">{E(u['copyLink'])}</button>
<a class="btn hero-cta" id="gr-classroom" target="_blank" rel="noopener noreferrer">{E(u['classroom'])}</a>
</div>
<article class="lb-plan" id="lb-plan" aria-live="polite" hidden></article>
<script type="application/json" id="gr-i18n">{blob}</script>
</div>
'''

APP_PAGE = 'https://observer.globe.gov/about/get-the-app'
APP_AFTER = {
    'en': 'with an app.',
    'fr': 'avec une application.',
    'es': 'con una aplicación.',
    'ar': 'بتطبيق.',
    'it': "con un'app.",
    'he': 'באפליקציה.',
}

def add_app_link(opening, lang, label):
    a = opening.find('<!-- ELI10:START -->')
    b = opening.find('<!-- ELI10:END -->')
    if a < 0 or b < 0:
        raise SystemExit('ELI10 block missing')
    chunk = opening[a:b]
    spot = APP_AFTER[lang]
    if spot not in chunk:
        raise SystemExit(f'{lang}: app sentence not found')
    link = f' <a class="gr-app" href="{APP_PAGE}" target="_blank" rel="noopener">{E(label)}</a>'
    chunk = chunk.replace(spot, spot + link, 1)
    return opening[:a] + chunk + opening[b:]

def build(lang):
    path = 'GLOBE_Program.html' if lang == 'en' else f'{lang}/GLOBE_Program.html'
    raw = open(path, encoding='utf-8').read()
    pre, rest = raw.split('<main id="main">', 1)
    rel = rest.find('<!-- RELATED:START -->')
    save = rest.find('<section class="impact saves-planets"')
    if rel < 0 or save < 0:
        raise SystemExit(f'{path}: missing saves or related')
    save_end = rest.find('</section>', save)
    if save_end < 0 or save_end > rel:
        raise SystemExit(f'{path}: saves section does not end before related')
    opening = rest[:save_end + len('</section>')]
    hero_at = opening.find('<section class="page-hero')
    eli = opening.find('<!-- ELI10:START -->')
    if hero_at < 0 or eli < 0:
        raise SystemExit(f'{path}: hero or eli missing')
    prefix = '' if lang == 'en' else '../'
    u = UI[lang]
    opening = opening[:hero_at] + install_video(opening[hero_at:eli], prefix, u['videoCredit']) + opening[eli:]
    opening = add_app_link(opening, lang, u['appLink'])
    tail = rest[rel:]
    tail = re.sub(r'<a class="sticky-help"[^>]*>.*?</a>\s*', '', tail, count=1)
    pre = pre.replace('GLOBE_Program.html', 'GLOBE_Review.html')
    pre = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,nofollow">', pre, count=1)
    pre = pre.replace('class="hp-globe-program toc-sub globe-page"', 'class="hp-globe-program toc-sub globe-page globe-review"', 1)
    pre = pre.replace('<body ', '<body data-pagefind-ignore="all" data-no-newsletter ', 1)
    pre = pre.replace('assets/Pacific_Clouds_Sunset_ISS.jpg', 'assets/videos/globe-review-poster.jpg')
    pre = pre.replace('</head>', f'<link rel="stylesheet" href="{prefix}edu.css?v=20261113h">\n<link rel="stylesheet" href="{prefix}globe-review.css?v=20261113s">\n</head>', 1)
    tail = tail.replace('</body>', f'<script src="{prefix}globe-review.js?v=20261113m" defer></script>\n</body>', 1)
    out = pre + '<main id="main">\n' + opening + '\n' + builder(u) + tail
    if 'gr-banner' in out or u['invite'] in out:
        raise SystemExit(f'{path}: draft banner still present')
    if 'Pacific_Clouds_Sunset_ISS' in out:
        raise SystemExit(f'{path}: sunset image still referenced')
    if 'globe-review-hero.mp4' not in out:
        raise SystemExit(f'{path}: title video missing')
    if '<a class="sticky-help"' in out:
        raise SystemExit(f'{path}: donate button remains')
    dest = path.replace('GLOBE_Program.html', 'GLOBE_Review.html')
    open(dest, 'w', encoding='utf-8').write(out)
    print('wrote', dest, len(out))

if __name__ == '__main__':
    for lang in LANGS:
        build(lang)
