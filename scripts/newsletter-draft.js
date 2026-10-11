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
const today = new Date(), iso = today.toISOString().slice(0, 10);

const T = {
  en: { title: 'This Week in Saving Planets', subject: d => `This Week in Saving Planets: ${d}`, intro: 'Your weekly brief of sourced solutions for our planet, minus the doom.', newS: 'New Solutions This Week', none: 'No new solutions this week, but every page was refreshed with the latest figures.', fact: 'Amazing Fact', next: 'Coming Up: Launches & Milestones', why: 'Why It Matters', whyText: 'Space and Earth are one system. Cleaner orbits protect the satellites that track storms, forests and oceans; planetary defense protects us all; and every fix on the ground shows that progress is real and measurable. Share this brief with someone who needs some good news backed by numbers.', read: 'Read more', src: 'Source', visit: 'Explore all solutions', launch: 'launch', arrival: 'arrival', flyby: 'flyby', foot: 'You are receiving this because you subscribed at savingplanets.com.', dateLoc: 'en-US' },
  fr: { title: 'Cette semaine chez Saving Planets', subject: d => `Cette semaine chez Saving Planets : ${d}`, intro: 'Votre brief hebdomadaire de solutions sourcées pour notre planète, sans la fatalité.', newS: 'Nouvelles solutions cette semaine', none: 'Pas de nouvelle solution cette semaine, mais chaque page a été mise à jour avec les derniers chiffres.', fact: 'Fait étonnant', next: 'À venir : lancements et étapes clés', why: 'Pourquoi c\u2019est important', whyText: 'L\u2019espace et la Terre forment un seul système. Des orbites plus propres protègent les satellites qui suivent les tempêtes, les forêts et les océans ; la défense planétaire nous protège tous ; et chaque solution sur le terrain montre que les progrès sont réels et mesurables. Partagez ce brief avec quelqu\u2019un qui a besoin de bonnes nouvelles chiffrées.', read: 'Lire la suite', src: 'Source', visit: 'Découvrir toutes les solutions', launch: 'lancement', arrival: 'arrivée', flyby: 'survol', foot: 'Vous recevez ce message car vous vous êtes abonné sur savingplanets.com.', dateLoc: 'fr-FR' },
  es: { title: 'Esta semana en Saving Planets', subject: d => `Esta semana en Saving Planets: ${d}`, intro: 'Tu resumen semanal de soluciones con fuentes para nuestro planeta, sin catastrofismo.', newS: 'Nuevas soluciones esta semana', none: 'No hay soluciones nuevas esta semana, pero todas las páginas se actualizaron con las cifras más recientes.', fact: 'Dato asombroso', next: 'Próximamente: lanzamientos e hitos', why: 'Por qué importa', whyText: 'El espacio y la Tierra son un solo sistema. Órbitas más limpias protegen los satélites que vigilan tormentas, bosques y océanos; la defensa planetaria nos protege a todos; y cada solución en tierra demuestra que el progreso es real y medible. Comparte este resumen con alguien que necesite buenas noticias respaldadas por datos.', read: 'Leer más', src: 'Fuente', visit: 'Explora todas las soluciones', launch: 'lanzamiento', arrival: 'llegada', flyby: 'sobrevuelo', foot: 'Recibes este correo porque te suscribiste en savingplanets.com.', dateLoc: 'es-ES' },
  ar: { title: 'هذا الأسبوع في Saving Planets', subject: d => `هذا الأسبوع في Saving Planets: ${d}`, intro: 'نشرتك الأسبوعية لحلول موثقة المصادر من أجل كوكبنا، بلا تهويل.', newS: 'حلول جديدة هذا الأسبوع', none: 'لا توجد حلول جديدة هذا الأسبوع، لكن جميع الصفحات حُدّثت بأحدث الأرقام.', fact: 'حقيقة مذهلة', next: 'قريبًا: عمليات الإطلاق والمحطات المهمة', why: 'لماذا يهم ذلك', whyText: 'الفضاء والأرض نظام واحد. المدارات الأنظف تحمي الأقمار الصناعية التي ترصد العواصف والغابات والمحيطات، والدفاع الكوكبي يحمينا جميعًا، وكل حل على الأرض يثبت أن التقدم حقيقي وقابل للقياس. شارك هذه النشرة مع من يحتاج إلى أخبار جيدة مدعومة بالأرقام.', read: 'اقرأ المزيد', src: 'المصدر', visit: 'استكشف جميع الحلول', launch: 'إطلاق', arrival: 'وصول', flyby: 'تحليق', foot: 'تتلقى هذه الرسالة لأنك اشتركت عبر savingplanets.com.', dateLoc: 'ar' }
};
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const dec = s => String(s).replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&');
const rd = f => { try { return fs.readFileSync(path.join(ROOT, f), 'utf8'); } catch (e) { return null; } };
const pageFile = (lang, f) => lang === 'en' ? f : `${lang}/${f}`;
function meta(html) {
  const t = (html.match(/<title>([^<]*)<\/title>/) || [])[1] || '';
  const d = (html.match(/<meta name="description" content="([^"]*)"/) || [])[1] || '';
  return { title: dec(t.replace(/\s*[|·–-]\s*(Saving Planets|Français|Español|بالعربية).*$/, '').trim()), desc: dec(d) };
}
function newSolutions() {
  const data = JSON.parse(rd('assets/data/solutions.json'));
  const since = Date.now() - DAYS * 864e5, out = [];
  for (const p of data.pages) {
    if (p.type === 'hub') continue;
    let added; try { added = execSync(`git log --diff-filter=A --format=%cI -- "${p.url}" | tail -1`, { cwd: ROOT }).toString().trim(); } catch (e) { continue; }
    if (added && Date.parse(added) >= since) out.push({ url: p.url, added });
  }
  return out.sort((a, b) => b.added.localeCompare(a.added)).slice(0, 5);
}
function facts(lang) {
  const html = rd(pageFile(lang, 'Amazing_Facts.html')) || rd('Amazing_Facts.html');
  const cards = html.match(/<div class="w-card" data-fact-origin[\s\S]*?<\/div>/g) || [];
  if (!cards.length) return null;
  const week = Math.floor(today / 6048e5), c = cards[week % cards.length];
  const g = re => (c.match(re) || [])[1];
  const img = g(/<img[^>]*src="([^"]+)"/);
  const ps = [...c.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m => m[1].replace(/<[^>]+>/g, ''));
  return { h: dec(g(/<h3>([\s\S]*?)<\/h3>/) || ''), img: img && SITE + img.replace(/^\.\.\//, ''), alt: dec(g(/alt="([^"]*)"/) || ''), text: dec(ps[0] || ''),
    page: g(/data-fact-page="([^"]+)"/), srcUrl: g(/Source: <a href="([^"]+)"/) || g(/<a href="(https?:[^"]+)"/), srcLabel: dec((c.match(/Source: <a [^>]*>([^<]+)</) || [])[1] || '') };
}
async function milestones() {
  const data = JSON.parse(rd('assets/data/solutions.json')), now = Date.now(), list = [];
  for (const p of data.pages) for (const m of p.missions || []) if (m.next && Date.parse(m.next.date) > now) list.push({ name: m.name, event: m.next.event, date: m.next.date, url: p.url });
  const seen = new Set(), uniq = list.sort((a, b) => a.date.localeCompare(b.date)).filter(x => !seen.has(x.name + x.event) && seen.add(x.name + x.event));
  let launches = [];
  try {
    const r = await fetch('https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=3&mode=list', { headers: { Accept: 'application/json' } });
    if (r.ok) launches = (await r.json()).results.map(l => ({ name: l.name, date: l.net, event: 'launch', ext: 'https://thespacedevs.com/llapi' }));
  } catch (e) { /* offline: milestones only */ }
  return { launches, ms: uniq.slice(0, 4) };
}
function fmtDate(d, lang) { return new Date(d).toLocaleDateString(T[lang].dateLoc, { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }); }
function build(lang, sols, fact, mil) {
  const t = T[lang], rtl = lang === 'ar', dir = rtl ? 'rtl' : 'ltr', al = rtl ? 'right' : 'left', pre = lang === 'en' ? '' : lang + '/';
  const h2 = s => `<h2 style="margin:28px 0 10px;font-size:20px;color:#003755;border-bottom:2px solid #009cde;padding-bottom:6px">${esc(s)}</h2>`;
  let solsHtml = sols.length ? sols.map(s => { const m = meta(rd(pageFile(lang, s.url)) || rd(s.url)); return `<p style="margin:0 0 14px"><a href="${SITE + pre + s.url}" style="color:#009cde;font-weight:700;text-decoration:none">${esc(m.title)}</a><br>${esc(m.desc)}</p>`; }).join('') : `<p>${esc(t.none)}</p>`;
  let factHtml = fact ? `<h3 style="margin:0 0 8px;color:#003755">${esc(fact.h)}</h3>${fact.img ? `<img src="${fact.img}" alt="${esc(fact.alt)}" width="560" style="width:100%;max-width:560px;height:auto;border-radius:8px;display:block;margin:0 0 10px">` : ''}<p style="margin:0 0 6px">${esc(fact.text)}</p><p style="margin:0;font-size:13px">${fact.page ? `<a href="${SITE + pre + fact.page}" style="color:#009cde">${esc(t.read)}</a>` : ''}${fact.srcUrl ? ` · ${esc(t.src)}: <a href="${fact.srcUrl}" style="color:#009cde">${esc(fact.srcLabel || fact.srcUrl)}</a>` : ''}</p>` : '';
  const ev = e => t[e] || e;
  const items = [...mil.launches.map(l => `<li style="margin:0 0 6px"><strong>${esc(l.name)}</strong>: ${esc(ev('launch'))}, ${fmtDate(l.date, lang)} <span style="font-size:12px">(The Space Devs)</span></li>`),
    ...mil.ms.map(m => `<li style="margin:0 0 6px"><a href="${SITE + pre + m.url}" style="color:#009cde;font-weight:700;text-decoration:none">${esc(m.name)}</a>: ${esc(ev(m.event))}, ${fmtDate(m.date, lang)}</li>`)];
  return `<!DOCTYPE html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(t.title)}</title></head>
<body style="margin:0;background:#eef5fa"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef5fa"><tr><td align="center" style="padding:20px 10px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:10px"><tr><td dir="${dir}" style="padding:28px 24px;font-family:Montserrat,Segoe UI,Arial,sans-serif;font-size:15px;line-height:1.55;color:#003755;text-align:${al}">
<p style="margin:0;font-size:12px;letter-spacing:1px;color:#009cde;font-weight:700">SAVING PLANETS · ${fmtDate(today, lang)}</p>
<h1 style="margin:6px 0 8px;font-size:26px;color:#003755">${esc(t.title)}</h1><p style="margin:0">${esc(t.intro)}</p>
${h2(t.newS)}${solsHtml}${fact ? h2(t.fact) + factHtml : ''}${items.length ? h2(t.next) + `<ul style="padding-${al}:18px;margin:0">${items.join('')}</ul>` : ''}
${h2(t.why)}<p style="margin:0">${esc(t.whyText)}</p>
<p style="margin:26px 0 0;text-align:center"><a href="${SITE + pre}index.html" style="display:inline-block;background:#009cde;color:#fff;font-weight:700;padding:12px 22px;border-radius:6px;text-decoration:none">${esc(t.visit)}</a></p>
<p style="margin:26px 0 0;font-size:12px;color:#5b7486;text-align:center">${esc(t.foot)}<br>{$account_address}<br><a href="{$unsubscribe}" style="color:#5b7486">Unsubscribe</a></p>
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
  const sols = newSolutions(), mil = await milestones();
  let existing = [];
  if (!DRY) existing = (await api('GET', '/campaigns?filter[status]=draft&limit=100')).data.map(c => c.name);
  for (const lang of LANGS) {
    const html = build(lang, sols, facts(lang), mil), name = `Weekly Brief ${iso} (${lang.toUpperCase()})`;
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
})().catch(e => { console.error('ERROR', e.message); process.exit(1); });
