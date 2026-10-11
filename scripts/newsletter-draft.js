#!/usr/bin/env node
/* Weekly Saving Planets Brief: builds one issue per language (EN/FR/ES/AR) and saves it as a DRAFT campaign
   in MailerLite for the matching group. NEVER sends or schedules.
   Usage: node scripts/newsletter-draft.js [--dry-run] [--days 7] [--lang en,fr]
   API key: read at runtime from $MAILERLITE_KEY_FILE (default ~/.mailerlite_key). Never commit or print it.
   Output HTML is also written to /tmp/newsletter-<date>-<lang>.html for review. */
const fs = require('fs'), path = require('path'), os = require('os'), { execSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..'), SITE = 'https://www.savingplanets.com/', API = 'https://connect.mailerlite.com/api';
const GROUPS = { en: '201062857381512972', fr: '201062857692939304', es: '201062857966617859', ar: '201062858265462233' };
const FROM = { name: 'Saving Planets', email: 'newsletter@savingplanets.com' };
const args = process.argv.slice(2), DRY = args.includes('--dry-run');
const DAYS = +(args[args.indexOf('--days') + 1] || 0) || 7;
const LANGS = args.includes('--lang') ? args[args.indexOf('--lang') + 1].split(',') : ['en', 'fr', 'es', 'ar'];
const today = new Date(), iso = new Date(today.getTime() - 10 * 36e5).toISOString().slice(0, 10); // HST date
const CAP = 3; // max new solutions shown per hub
const STATE = path.join(ROOT, 'scripts', 'newsletter-state.json');

const T = {
  en: { title: 'This Week in Saving Planets', subject: d => `This Week in Saving Planets: ${d}`, intro: 'Your weekly brief of sourced solutions for our planet, minus the doom.', newS: 'New Solutions This Week', none: 'No new solutions this week, but every page was refreshed with the latest figures.', fact: 'Amazing Fact', next: 'Coming Up: Launches & Milestones', why: 'Why It Matters', whyText: 'Space and Earth are one system. Cleaner orbits protect the satellites that track storms, forests and oceans; planetary defense protects us all; and every fix on the ground shows that progress is real and measurable. Share this brief with someone who needs some good news backed by numbers.', read: 'Read more', src: 'Source', visit: 'Explore all solutions', launch: 'launch', arrival: 'arrival', flyby: 'flyby', foot: 'You are receiving this because you subscribed at savingplanets.com.', dateLoc: 'en-US' },
  fr: { title: 'Cette semaine chez Saving Planets', subject: d => `Cette semaine chez Saving Planets : ${d}`, intro: 'Votre brief hebdomadaire de solutions sourcées pour notre planète, sans la fatalité.', newS: 'Nouvelles solutions cette semaine', none: 'Pas de nouvelle solution cette semaine, mais chaque page a été mise à jour avec les derniers chiffres.', fact: 'Fait étonnant', next: 'À venir : lancements et étapes clés', why: 'Pourquoi c\u2019est important', whyText: 'L\u2019espace et la Terre forment un seul système. Des orbites plus propres protègent les satellites qui suivent les tempêtes, les forêts et les océans ; la défense planétaire nous protège tous ; et chaque solution sur le terrain montre que les progrès sont réels et mesurables. Partagez ce brief avec quelqu\u2019un qui a besoin de bonnes nouvelles chiffrées.', read: 'Lire la suite', src: 'Source', visit: 'Découvrir toutes les solutions', launch: 'lancement', arrival: 'arrivée', flyby: 'survol', foot: 'Vous recevez ce message car vous vous êtes abonné sur savingplanets.com.', dateLoc: 'fr-FR' },
  es: { title: 'Esta semana en Saving Planets', subject: d => `Esta semana en Saving Planets: ${d}`, intro: 'Tu resumen semanal de soluciones con fuentes para nuestro planeta, sin catastrofismo.', newS: 'Nuevas soluciones esta semana', none: 'No hay soluciones nuevas esta semana, pero todas las páginas se actualizaron con las cifras más recientes.', fact: 'Dato asombroso', next: 'Próximamente: lanzamientos e hitos', why: 'Por qué importa', whyText: 'El espacio y la Tierra son un solo sistema. Órbitas más limpias protegen los satélites que vigilan tormentas, bosques y océanos; la defensa planetaria nos protege a todos; y cada solución en tierra demuestra que el progreso es real y medible. Comparte este resumen con alguien que necesite buenas noticias respaldadas por datos.', read: 'Leer más', src: 'Fuente', visit: 'Explora todas las soluciones', launch: 'lanzamiento', arrival: 'llegada', flyby: 'sobrevuelo', foot: 'Recibes este correo porque te suscribiste en savingplanets.com.', dateLoc: 'es-ES' },
  ar: { title: 'هذا الأسبوع في Saving Planets', subject: d => `هذا الأسبوع في Saving Planets: ${d}`, intro: 'نشرتك الأسبوعية لحلول موثقة المصادر من أجل كوكبنا، بلا تهويل.', newS: 'حلول جديدة هذا الأسبوع', none: 'لا توجد حلول جديدة هذا الأسبوع، لكن جميع الصفحات حُدّثت بأحدث الأرقام.', fact: 'حقيقة مذهلة', next: 'قريبًا: عمليات الإطلاق والمحطات المهمة', why: 'لماذا يهم ذلك', whyText: 'الفضاء والأرض نظام واحد. المدارات الأنظف تحمي الأقمار الصناعية التي ترصد العواصف والغابات والمحيطات، والدفاع الكوكبي يحمينا جميعًا، وكل حل على الأرض يثبت أن التقدم حقيقي وقابل للقياس. شارك هذه النشرة مع من يحتاج إلى أخبار جيدة مدعومة بالأرقام.', read: 'اقرأ المزيد', src: 'المصدر', visit: 'استكشف جميع الحلول', launch: 'إطلاق', arrival: 'وصول', flyby: 'تحليق', foot: 'تتلقى هذه الرسالة لأنك اشتركت عبر savingplanets.com.', dateLoc: 'ar' }
};

// Fixed strings for the v2 template (2026-10-11).
const T2 = {
  en: { seeAll: (n, h) => `See all ${n} new in ${h}`, issue: 'Issue date', hubsIntro: 'Grouped by hub. Tap a title to read the full page.', horizon: 'Potential solution on the horizon', horizonNote: "We'll keep you updated here if this becomes a reality.",
    noneAll: 'No new solutions this week.', launches: 'Launches This Week', noLaunch: 'No launches are on the books for this week yet.', vehicle: 'Vehicle', mission: 'Mission', shift: 'Launch dates shift often.', schedule: 'See our full launch schedule',
    suggest: 'Suggest a New Solution', suggestText: 'Know a group doing hands-on work with published numbers? Email your idea to', criteria: 'See our solutions criteria', facts: 'Amazing Facts', source: 'Source', allFacts: 'See all Amazing Facts', unsub: 'Unsubscribe', tz: 'UTC' },
  fr: { seeAll: (n, h) => `Voir les ${n} nouveautés : ${h}`, issue: 'Date du numéro', hubsIntro: 'Classées par thème. Touchez un titre pour lire la page complète.', horizon: "Solution potentielle à l'horizon", horizonNote: 'Nous vous tiendrons informés ici si cela se concrétise.',
    noneAll: 'Pas de nouvelle solution cette semaine.', launches: 'Lancements de la semaine', noLaunch: "Aucun lancement n'est encore prévu cette semaine.", vehicle: 'Lanceur', mission: 'Mission', shift: 'Les dates de lancement changent souvent.', schedule: 'Voir notre calendrier complet des lancements',
    suggest: 'Proposez une nouvelle solution', suggestText: 'Vous connaissez un groupe qui agit sur le terrain avec des chiffres publiés ? Envoyez votre idée à', criteria: 'Voir nos critères de sélection', facts: 'Faits étonnants', source: 'Source', allFacts: 'Voir tous les faits étonnants', unsub: 'Se désabonner', tz: 'UTC' },
  es: { seeAll: (n, h) => `Ver las ${n} novedades en ${h}`, issue: 'Fecha del número', hubsIntro: 'Agrupadas por tema. Toca un título para leer la página completa.', horizon: 'Posible solución en el horizonte', horizonNote: 'Te mantendremos informado aquí si esto se hace realidad.',
    noneAll: 'No hay soluciones nuevas esta semana.', launches: 'Lanzamientos de esta semana', noLaunch: 'Todavía no hay lanzamientos programados para esta semana.', vehicle: 'Vehículo', mission: 'Misión', shift: 'Las fechas de lanzamiento cambian a menudo.', schedule: 'Ver nuestro calendario completo de lanzamientos',
    suggest: 'Sugiere una nueva solución', suggestText: '¿Conoces un grupo que hace trabajo práctico con cifras publicadas? Envía tu idea a', criteria: 'Ver nuestros criterios de soluciones', facts: 'Datos asombrosos', source: 'Fuente', allFacts: 'Ver todos los datos asombrosos', unsub: 'Darse de baja', tz: 'UTC' },
  ar: { seeAll: (n, h) => `عرض جميع الإضافات الجديدة (${n}) في ${h}`, issue: 'تاريخ العدد', hubsIntro: 'مصنفة حسب المحور. اضغط على العنوان لقراءة الصفحة كاملة.', horizon: 'حل محتمل في الأفق', horizonNote: 'سنبقيكم على اطلاع هنا إذا أصبح هذا واقعًا.',
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
function build(lang, sols, factKeys, launchList) {
  const t = { ...T[lang], ...T2[lang] }, rtl = lang === 'ar', dir = rtl ? 'rtl' : 'ltr', al = rtl ? 'right' : 'left', P = SITE + pre(lang);
  const a = (href, txt, bold) => `<a href="${href}" style="color:#009cde;${bold ? 'font-weight:700;' : ''}text-decoration:none">${esc(txt)}</a>`;
  const h2 = s => `<h2 style="margin:30px 0 12px;font-size:20px;color:#003755;border-bottom:2px solid #009cde;padding-bottom:6px">${esc(s)}</h2>`;
  // 2. New solutions by hub
  const { map, order } = hubMap(lang), byHub = {};
  for (const s of sols) (byHub[map[s.url] || '_other'] = byHub[map[s.url] || '_other'] || []).push(s);
  let solsHtml = '';
  for (const hub of [...order, { url: '_other', name: '' }]) {
    const list = byHub[hub.url]; if (!list) continue;
    solsHtml += `<h3 style="margin:18px 0 8px;font-size:16px;color:#003755;text-transform:uppercase;letter-spacing:.5px">${hub.url === '_other' ? '' : a(P + hub.url, hub.name, true)}</h3>`;
    const more = list.length > CAP && hub.url !== '_other' ? `<p style="margin:0 0 12px;font-size:14px">${a(P + hub.url, t.seeAll(list.length, hub.name) + ' →', true)}</p>` : '';
    solsHtml += list.slice(0, CAP).map(s => { const m = meta(rd(pageFile(lang, s.url)) || rd(s.url));
      const badge = s.horizon ? `<br><span style="display:inline-block;margin:4px 0;background:#fff4e0;color:#8a5a00;border:1px solid #f0c36d;border-radius:12px;padding:1px 9px;font-size:12px;font-weight:700">${esc(t.horizon)}</span> <span style="font-size:12px;color:#5b7486">${esc(t.horizonNote)}</span>` : '';
      return `<p style="margin:0 0 12px">${a(P + s.url, m.title, true)}${badge}<br><span style="font-size:14px">${esc(m.desc)}</span></p>`; }).join('') + more;
  }
  if (!sols.length) solsHtml = `<p>${esc(t.noneAll)}</p>`;
  else solsHtml = `<p style="margin:0 0 4px;font-size:13px;color:#5b7486">${esc(t.hubsIntro)}</p>` + solsHtml;
  // 3. Launches
  const lHtml = (launchList && launchList.length ? `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;border-collapse:collapse">` + launchList.map(l =>
    `<tr><td dir="${dir}" style="padding:8px 0;border-bottom:1px solid #e3edf4;text-align:${al}"><strong>${esc(fmtDay(l.date, lang))}</strong><br>${esc(t.vehicle)}: ${esc(l.vehicle)}${l.provider ? ' (' + esc(l.provider) + ')' : ''}<br>${esc(t.mission)}: ${esc(l.mission)}</td></tr>`).join('') + '</table>'
    : `<p style="margin:0">${esc(t.noLaunch)}</p>`) + `<p style="margin:12px 0 0;font-size:14px">${esc(t.shift)} ${a(P + 'Project-Rawane.html#launches', t.schedule + ' →', true)}</p>`;
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
<table role="presentation" cellpadding="0" cellspacing="0" dir="${dir}"><tr><td valign="middle" style="padding-${rtl ? 'left' : 'right'}:16px"><a href="${P}index.html"><img src="${SITE}assets/SavePlanetLogo-email.png" width="72" height="84" alt="Saving Planets" style="display:block;width:72px;height:84px;border:0;border-radius:8px"></a></td><td valign="middle" dir="${dir}" style="text-align:${al}">
<p style="margin:0;font-size:12px;letter-spacing:2px;color:#7fd3f7;font-weight:700">SAVING PLANETS</p>
<p style="margin:8px 0 0;font-size:28px;font-weight:800;color:#ffffff;line-height:1.2">${esc(fmtDate(today, lang))}</p>
<p style="margin:4px 0 0;font-size:16px;color:#cfe9f7">${esc(t.title)}</p></td></tr></table></td></tr>
<tr><td dir="${dir}" style="padding:24px 24px 28px;font-family:Montserrat,Segoe UI,Arial,sans-serif;font-size:15px;line-height:1.55;color:#003755;text-align:${al}">
<p style="margin:0">${esc(t.intro)}</p>
${h2(t.newS)}${solsHtml}
${h2(t.launches)}${lHtml}
${h2(t.suggest)}${sugHtml}
${h2(t.facts)}${fHtml}
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
  const sols = newSolutions(), state = loadState(), factKeys = pickFacts(state);
  let launchList = null; try { launchList = await launches(); } catch (e) { console.log('note: launches unavailable (' + e.message + ')'); }
  let existing = [];
  if (!DRY) existing = (await api('GET', '/campaigns?filter[status]=draft&limit=100')).data.map(c => c.name);
  for (const lang of LANGS) {
    const html = build(lang, sols, factKeys, launchList), name = `Weekly Brief ${iso}${process.env.NL_SUFFIX || ""} (${lang.toUpperCase()})`;
    fs.writeFileSync(`/tmp/newsletter-${iso}-${lang}.html`, html);
    if (DRY) { console.log(`[dry-run] ${name}: ${html.length} bytes -> /tmp/newsletter-${iso}-${lang}.html`); continue; }
    if (existing.includes(name)) { console.log(`skip (draft exists): ${name}`); continue; }
    const email = { subject: T[lang].subject(fmtDate(today, lang)), from_name: FROM.name, from: FROM.email, content: html };
    let c;
    try { c = await api('POST', '/campaigns', { name, type: 'regular', emails: [email], groups: [GROUPS[lang]] }); }
    catch (e) {
      if (!/content/i.test(e.message)) throw e;
      delete email.content;  // plan does not allow custom HTML via API: create the draft without content; paste /tmp HTML in the editor
      c = await api('POST', '/campaigns', { name, type: 'regular', emails: [email], groups: [GROUPS[lang]] });
      console.log(`note: ${name} created WITHOUT HTML content (API refused content); use /tmp/newsletter-${iso}-${lang}.html`);
    }
    console.log(`draft created: ${name} id=${c.data.id} status=${c.data.status}`);
  }
  if (!DRY) {  // record facts so later issues never repeat them
    state.issues[iso] = { facts: factKeys, solutions: sols.length, launches: launchList ? launchList.length : null };
    state.usedFacts = [...new Set([...state.usedFacts, ...factKeys])];
    fs.writeFileSync(STATE, JSON.stringify(state, null, 2) + '\n');
  }
  console.log('facts:', factKeys.join(', '), '| solutions:', sols.length, '| launches:', launchList ? launchList.length : 'n/a');
})().catch(e => { console.error('ERROR', e.message); process.exit(1); });
