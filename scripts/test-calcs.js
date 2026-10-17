// Oct 16 2026: assets/calc.js must match scripts/calc_check.py (vectors written by calc_check.py). Run: node scripts/test-calcs.js
const { C } = require('../assets/calc.js'); const V = require('./calc-vectors.json'); let bad = 0;
for (const t of V) { const r = C[t.id](t.x); for (const k in t.y) { const a = r[k], b = t.y[k], tol = t.id === 'proj' ? 2e-3 * Math.max(1, Math.abs(b)) : 1e-6 * Math.max(1, Math.abs(b));
  if (!(Math.abs(a - b) <= tol)) { bad++; console.error('MISMATCH', t.id, k, a, b); } } }
if (bad) { console.error(bad + ' calculator mismatches'); process.exit(1); } console.log('test-calcs: ' + V.length + ' cases OK');
