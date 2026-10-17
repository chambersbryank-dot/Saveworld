// Checks assets/aero-lab.js against the build-verified values in scripts/aero_calc.py (run by weekly-sync.sh).
const A = require('../assets/aero-lab.js'), assert = require('assert');
const near = (a, b, t) => assert(Math.abs(a - b) <= t, `${a} vs ${b}`);
const i = A.isa(11000); near(i.T, 216.65, 1e-9); near(i.p, 22632.04, 0.05); near(i.rho, 0.363918, 1e-6);
near(A.isa(5000).rho, 0.736116, 1e-6);
near(A.stall(1100, 16.2, 1.6, 1.225), 26.0667, 1e-3); near(A.stall(1100, 16.2, 1.6, A.isa(1500).rho), 28.05, 0.01);
const s = A.sp(-1.0, -1.5, -0.3, -8.0); near(s.wn, 3.0822, 1e-4); near(s.z, 0.4542, 1e-4); near(s.re, -1.4, 1e-9); near(s.im, 2.7459, 1e-4);
const h = A.hover(2700, 5.1, 0.761); near(h.T, 26478, 1); near(h.A, 81.71, 0.01); near(h.vi, 11.50, 0.01); near(h.Pi, 304.5, 0.1); near(h.DL, 324, 0.5);
assert(A.sp(-1, 0.5, -0.3, 2).r1 > 0);
console.log('test-aero-lab: ok');
