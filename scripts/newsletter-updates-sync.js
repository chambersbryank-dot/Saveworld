#!/usr/bin/env node
/* Append notable site improvements to scripts/newsletter-updates.json (shown under "What's New" in the Weekly Brief).
   Sources, both optional:
   1. Commits whose subject starts with "feat:" or "feat(Page.html):" since the newest entry, e.g.
        feat(Kids_Map.html): Kids Planet Map now has a sound toggle
      The scope (if it is a site page) becomes the link; the rest is the reader-facing sentence, so write it for readers.
   2. A "## Newsletter" section in NOTES.md, one bullet per item: "- YYYY-MM-DD | Page.html | sentence"
   Entries get only an English "what"; the newsletter falls back to English for fr/es/ar until translations are added
   (edit the entry and add what.fr/es/ar). Deduped by commit hash / note text. Never invents text. Usage: node scripts/newsletter-updates-sync.js [--dry-run] */
const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..'), F = path.join(ROOT, 'scripts', 'newsletter-updates.json'), DRY = process.argv.includes('--dry-run');
const data = JSON.parse(fs.readFileSync(F, 'utf8')); data.entries = data.entries || [];
const seen = new Set(data.entries.map(e => e.commit || e.note || '').filter(Boolean));
const hst = iso => new Date(Date.parse(iso) - 10 * 36e5).toISOString().slice(0, 10);
const added = [];
const since = data.entries.filter(e => e.commit).map(e => e.date).sort().pop() || '2026-10-14';
let log = ''; try { log = execSync(`git log --since="${since}T00:00:00-10:00" --format=%H%x09%cI%x09%s`, { cwd: ROOT }).toString(); } catch (e) {}
for (const line of log.split('\n').reverse()) {
  const [h, d, subj] = line.split('\t'); if (!subj) continue;
  const m = subj.match(/^feat(?:\(([^)]+)\))?!?:\s*(.+)$/i); if (!m || seen.has(h)) continue;
  const page = m[1] && /\.html$/.test(m[1]) && fs.existsSync(path.join(ROOT, m[1])) ? m[1] : undefined;
  const e = { date: hst(d), ...(page ? { page } : {}), what: { en: m[2].trim() }, commit: h };
  data.entries.push(e); seen.add(h); added.push(e);
}
const notes = fs.existsSync(path.join(ROOT, 'NOTES.md')) ? fs.readFileSync(path.join(ROOT, 'NOTES.md'), 'utf8') : '';
const sec = (notes.match(/^## Newsletter\s*\n([\s\S]*?)(?=^## |\Z)/m) || [])[1] || '';
for (const b of sec.split('\n')) {
  const m = b.match(/^\s*[-*]\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]*?)\s*\|\s*(.+)$/); if (!m) continue;
  const note = m[1] + '|' + m[3].trim(); if (seen.has(note)) continue;
  const e = { date: m[1], ...(m[2] ? { page: m[2] } : {}), what: { en: m[3].trim() }, note };
  data.entries.push(e); seen.add(note); added.push(e);
}
if (added.length && !DRY) fs.writeFileSync(F, JSON.stringify(data, null, 2) + '\n');
console.log(`newsletter-updates: ${added.length} new entr${added.length === 1 ? 'y' : 'ies'}${DRY ? ' (dry run)' : ''}` + added.map(e => `\n  ${e.date} ${e.page || '-'}: ${e.what.en}`).join(''));
