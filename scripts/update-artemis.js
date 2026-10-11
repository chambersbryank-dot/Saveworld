#!/usr/bin/env node
/* Weekly Artemis check: fetches NASA's Artemis mission pages, compares what can be parsed
   reliably (mission-page "LAUNCH" and "crew" fields, Artemis III crew names) with
   assets/data/artemis.json, prints a diff summary, and updates only those fields.
   Never invents data: if a page fails or a field can't be parsed, it is reported and left alone.
   Usage: node scripts/update-artemis.js [--dry-run]   (exit 0 = no change, 2 = changed, 1 = fetch/parse errors) */
'use strict';
const fs = require('fs'), path = require('path');
const FILE = path.join(__dirname, '..', 'assets', 'data', 'artemis.json');
const DRY = process.argv.includes('--dry-run');
const UA = { headers: { 'User-Agent': 'Mozilla/5.0 (SavingPlanets Artemis tracker)' } };
const CREW_PAGE = 'https://www.nasa.gov/our-artemis-iii-crew/';
const ROLES = ['Commander', 'Pilot', 'Mission Specialist'];

function text(html) {
  return html.replace(/<(script|style|nav|header|footer)[\s\S]*?<\/\1>/gi, '')
    .replace(/<[^>]+>/g, '\n').replace(/&#8217;|&rsquo;/g, "'").replace(/&amp;/g, '&').replace(/&nbsp;/g, ' ')
    .split('\n').map(s => s.trim()).filter(Boolean);
}
function after(lines, label) {
  const i = lines.findIndex(l => l.toLowerCase() === label.toLowerCase());
  return i >= 0 && lines[i + 1] && lines[i + 1].length < 40 ? lines[i + 1] : null;
}
async function get(url) {
  const r = await fetch(url, UA);
  if (!r.ok) throw new Error(url + ' -> HTTP ' + r.status);
  return text(await r.text());
}
(async () => {
  const data = JSON.parse(fs.readFileSync(FILE, 'utf8'));
  const changes = [], notes = [], errors = [];
  for (const m of data.missions) {
    if (m.state === 'flown' || !m.watch) continue;
    let lines;
    try { lines = await get(m.watch); } catch (e) { errors.push(m.name + ': ' + e.message); continue; }
    const launch = after(lines, 'LAUNCH');
    if (!launch) notes.push(m.name + ': LAUNCH field not found on ' + m.watch + ' (left unchanged)');
    else if (launch !== m.target) {
      changes.push(`${m.name} target: "${m.target}" -> "${launch}"`);
      m.target = launch; m.targetLabel = 'NASA target: ' + launch.replace(/^Early/, 'early').replace(/^Late/, 'late').replace(/^Mid/, 'mid');
    }
    const crewN = after(lines, 'crew');
    if (crewN && /^\d+$/.test(crewN) && m.crew.length && +crewN !== m.crew.length)
      notes.push(`${m.name}: NASA page says crew of ${crewN}, JSON lists ${m.crew.length} names (review manually)`);
    const type = after(lines, 'Mission Type');
    if (type && type !== m.missionType) { changes.push(`${m.name} mission type: "${m.missionType}" -> "${type}"`); m.missionType = type; }
    if (m.id === 'artemis-iv' && !m.crew.length && lines.some(l => /Artemis IV crew/i.test(l)))
      notes.push('Artemis IV: page mentions an Artemis IV crew - check NASA and add names manually');
  }
  // Artemis III crew names: name line followed by a role line
  try {
    const lines = await get(CREW_PAGE), found = [];
    lines.forEach((l, i) => { if (ROLES.includes(lines[i + 1]) && /^[A-Z][a-z]+ [A-Z][A-Za-z'-]+$/.test(l) && !found.some(f => f.name === l)) found.push({ name: l, role: lines[i + 1] }); });
    const m3 = data.missions.find(m => m.id === 'artemis-iii');
    if (found.length === 4) {
      const cur = m3.crew.map(c => c.name + '/' + c.role).sort().join(', '), now = found.map(c => c.name + '/' + c.role).sort().join(', ');
      if (cur !== now) {
        changes.push(`Artemis III crew: [${cur}] -> [${now}]`);
        m3.crew = found.map(f => ({ name: f.name, role: f.role, agency: (m3.crew.find(c => c.name === f.name) || {}).agency || 'CHECK' }));
        notes.push('New crew member agency set to CHECK - confirm with NASA release');
      }
    } else notes.push(`Artemis III crew page: parsed ${found.length} names, expected 4 (left unchanged)`);
  } catch (e) { errors.push('Artemis III crew: ' + e.message); }
  const today = new Date().toLocaleDateString('en-CA', { timeZone: 'Pacific/Honolulu' });
  console.log('Artemis check ' + today + (DRY ? ' (dry run)' : ''));
  console.log(changes.length ? 'CHANGES:\n  ' + changes.join('\n  ') : 'No changes in parsed fields.');
  if (notes.length) console.log('NOTES:\n  ' + notes.join('\n  '));
  if (errors.length) console.log('ERRORS:\n  ' + errors.join('\n  '));
  if (!errors.length) data.asOf = today;
  if (changes.length) data.updated = today;
  if (!DRY && (changes.length || !errors.length)) fs.writeFileSync(FILE, JSON.stringify(data, null, 2) + '\n');
  process.exitCode = errors.length ? 1 : changes.length ? 2 : 0;
})();
