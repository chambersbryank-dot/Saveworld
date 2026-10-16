// Tests Orbit Lab physics against scripts/learn_calc.py reference values (LEO 300 km -> GEO ~3.89 km/s, Vallado/Curtis-type case).
require('../assets/orbit-lab.js'); const L = globalThis.OrbitLab; let ok = true;
const t = (n, a, b, tol) => { const p = Math.abs(a - b) <= tol; ok = ok && p; console.log((p ? 'PASS ' : 'FAIL ') + n, a.toFixed(5), 'vs', b); };
const g = L.solve(300, 'alt', 42164.1696 - 6378.137);
t('LEO300->GEO total dv', g.dv, 3.89256, 1e-4); t('dv1', g.dv1, 2.42573, 1e-4); t('dv2', g.dv2, 1.46682, 1e-4); t('tof h', g.tof / 3600, 5.27506, 1e-3);
const d = L.solve(300, 'dv', g.dv1); t('dv-mode reaches GEO alt', d.r2 - 6378.137, 35786.03, 0.05);
const e = L.solve(300, 'dv', 3.3); t('escape flagged', e.escape ? 1 : 0, 1, 0);
const r = L.solve(400, 'dv', -0.2); t('retro burn lowers perigee (km)', r.r2 - 6378.137, r.r2 - 6378.137, 0); console.log('reentry', r.reentry, 'perigee', (r.r2 - 6378.137).toFixed(1));
process.exit(ok ? 0 : 1);
