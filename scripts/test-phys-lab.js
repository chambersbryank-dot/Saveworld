// Checks assets/phys-lab.js against the build-verified values in scripts/phys_calc.py (run by weekly-sync.sh).
const P = require('../assets/phys-lab.js'), assert = require('assert'), { execSync } = require('child_process');
const X = JSON.parse(execSync('python3 -c "import json,sys; sys.path.insert(0,\'scripts\'); import phys_calc as p; print(json.dumps(p.examples()))"').toString());
const near = (a, b, t) => assert(Math.abs(a - b) <= t, `${a} vs ${b}`);
const r = P.traj(40, 35, 0.145, 0.074, 0.35); near(r.R, X.p_rng, 1e-6); near(r.H, X.p_top, 1e-6); near(r.T, X.p_tf, 1e-6);
near(P.traj(40, 45, 0.145, 0.074, 0.35).R, X.p_np2, 1e-6);
const v = P.vac(40, 35); near(v.R, X.p_rng0, 1e-9); near(v.H, X.p_top0, 1e-9); near(v.T, X.p_tf0, 1e-9);
near(P.traj(40, 35, 0.145, 0.074, 0, 0.001).R, X.p_rng0, 1e-3);  // zero drag reproduces vacuum
const o = P.osc(4, 0.25); near(o.re, X.p_sre, 1e-12); near(o.im, X.p_wd, 1e-12);
near(P.x_t(4, 0.25, 0), 1, 1e-12); near(P.x_t(4, 2, 0), 1, 1e-12); near(P.x_t(4, 1, 0), 1, 1e-12);
const p = P.pend(1, 60); near(p.T0, X.p_T0, 1e-12); near(p.T, X.p_T60, 1e-12); near(P.pend(2, 90).T, X.p_np4, 1e-12);
console.log('test-phys-lab: ok');
