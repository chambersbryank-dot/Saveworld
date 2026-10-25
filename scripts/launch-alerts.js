#!/usr/bin/env node
/* Launch-change alerts (MailerLite, free tier). Founder-approved Oct 24 2026.
   Fetches Launch Library 2 upcoming launches, diffs against the last snapshot and, when a launch's time,
   window or status changes, creates ONE DRAFT campaign for the "Launch alerts" group. It never sends or
   schedules: the founder reviews and sends each draft in MailerLite.
   Rules: skips launches led by RU/CN/KP/IR (same EXCL as map.js). First run only stores a baseline.
   API key: $MAILERLITE_KEY_FILE (default ~/.mailerlite_key). Never commit or print it.
   State: $LAUNCH_ALERTS_STATE (default ~/.launch-alerts-snapshot.json). --dry-run = no API writes. */
const fs = require('fs'), os = require('os'), path = require('path');
const API = 'https://connect.mailerlite.com/api', GROUP = '202276906528147418', LANG_EN = 4;
const FROM = { name: 'Saving Planets', email: 'newsletter@savingplanets.com' };
const DRY = process.argv.includes('--dry-run');
const STATE = process.env.LAUNCH_ALERTS_STATE || path.join(os.homedir(), '.launch-alerts-snapshot.json');
const EXCL = /roscosmos|russia|china|chinese|baikonur|plesetsk|vostochny|jiuquan|wenchang|xichang|taiyuan|haiyang|dongfeng|sohae|tonghae|korean committee|nada|korean people.s|landspace|galactic energy|i-space|orienspace|deep blue aero|space pioneer|cas space|expace|casc|casic|kazakhstan|iran/i;
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const fmt = iso => iso ? new Date(iso).toUTCString().replace('GMT', 'UTC') : 'TBD';
async function api(method, p, body) {
  const key = fs.readFileSync(process.env.MAILERLITE_KEY_FILE || path.join(os.homedir(), '.mailerlite_key'), 'utf8').trim();
  const r = await fetch(API + p, { method, headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json', Accept: 'application/json' }, body: body && JSON.stringify(body) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`${method} ${p} -> ${r.status} ${JSON.stringify(j).slice(0, 300)}`);
  return j;
}
function snap(l) { return { name: l.name, net: l.net, ws: l.window_start, we: l.window_end, status: l.status && l.status.abbrev, prov: l.launch_service_provider && l.launch_service_provider.name, pad: l.pad && l.pad.location && l.pad.location.name }; }
function changes(a, b) {
  const out = [], h = Math.abs(new Date(b.net) - new Date(a.net)) / 36e5, soon = (new Date(b.net) - Date.now()) < 48 * 36e5;
  if (a.net !== b.net && (h >= 1 || soon)) out.push(['Launch time', fmt(a.net), fmt(b.net)]);
  if (a.status !== b.status) out.push(['Status', a.status, b.status]);
  if ((a.ws !== b.ws || a.we !== b.we) && !out.length) out.push(['Launch window', `${fmt(a.ws)} – ${fmt(a.we)}`, `${fmt(b.ws)} – ${fmt(b.we)}`]);
  return out;
}
function html(items) {
  const rows = items.map(({ s, ch }) => `<h2 style="font-size:18px;margin:22px 0 6px;color:#003755">${esc(s.name)}</h2><p style="margin:0 0 6px;color:#5b7486;font-size:13px">${esc(s.prov)} · ${esc(s.pad)}</p>` +
    ch.map(([k, o, n]) => `<p style="margin:4px 0"><b>${esc(k)}:</b> <s>${esc(o)}</s> → <b>${esc(n)}</b></p>`).join('')).join('');
  return `<!DOCTYPE html><html lang="en"><body style="margin:0;background:#f4f8fb;font-family:Arial,sans-serif"><table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center"><table width="600" cellpadding="24" style="background:#fff;max-width:600px"><tr><td>
<h1 style="font-size:22px;color:#003755;margin:0">Launch update from Saving Planets</h1>
<p>A launch you follow on our Live Launch Tracker has changed:</p>${rows}
<p style="margin:24px 0 0;text-align:center"><a href="https://www.savingplanets.com/Artemis_II.html#launches" style="display:inline-block;background:#009cde;color:#fff;font-weight:700;padding:12px 22px;border-radius:6px;text-decoration:none">Open the Live Launch Tracker</a></p>
<p style="font-size:12px;color:#5b7486">Times are in UTC. Launch data: The Space Devs Launch Library 2. Schedules change often; check the tracker before you travel.</p>
<p style="margin:14px 0 0;font-size:12px;color:#5b7486;text-align:center">You get this because you asked for Saving Planets launch-change alerts.<br>{$account_address}<br><a href="{$unsubscribe}" style="color:#5b7486">Unsubscribe</a></p>
</td></tr></table></td></tr></table></body></html>`;
}
(async () => {
  const r = await fetch('https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=50&mode=normal');
  if (!r.ok) throw new Error('LL2 ' + r.status);
  const now = {};
  for (const l of (await r.json()).results) { const s = snap(l); if (!EXCL.test(`${s.pad} | ${s.prov}`)) now[l.id] = s; }
  const prev = fs.existsSync(STATE) ? JSON.parse(fs.readFileSync(STATE, 'utf8')) : null;
  const items = [];
  if (prev) for (const id in now) if (prev[id]) { const ch = changes(prev[id], now[id]); if (ch.length) items.push({ s: now[id], ch }); }
  console.log(prev ? `${Object.keys(now).length} launches, ${items.length} changed` : `baseline stored (${Object.keys(now).length} launches)`);
  if (items.length) {
    const body = html(items), name = `Launch alert ${new Date().toISOString().slice(0, 16)}Z (EN)`;
    fs.writeFileSync('/tmp/launch-alert-latest.html', body);
    const subject = items.length === 1 ? `Launch update: ${items[0].s.name}` : `Launch updates: ${items.length} launches changed`;
    if (DRY) console.log(`[dry-run] would create draft "${name}" -> /tmp/launch-alert-latest.html`);
    else { const c = await api('POST', '/campaigns', { name, type: 'regular', language_id: LANG_EN, groups: [GROUP], emails: [{ subject, from_name: FROM.name, from: FROM.email, content: body }] });
      console.log(`DRAFT created (not sent): ${name} id=${c.data.id}`); }
  }
  if (!DRY || !prev) fs.writeFileSync(STATE, JSON.stringify(now));
})().catch(e => { console.error(e.message); process.exit(1); });
