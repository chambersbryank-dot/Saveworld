#!/usr/bin/env python3
"""Oct 16: numeric engine for the Learn pages (Orbit_Math worked examples + Orbit Lab test cases).
Every number printed on the pages is computed here, never typed by hand. Constants: Earth mu and equatorial radius
(IERS/WGS-84 values used by Vallado 4th ed. and NASA JPL SSD), J2 (EGM2008 C20 -> J2 = 1.08262668e-3), g0 = 9.80665 m/s^2 (standard)."""
import math
MU = 398600.4418        # km^3/s^2
RE = 6378.137           # km
J2 = 1.08262668e-3
G0 = 9.80665e-3         # km/s^2
SIDEREAL_DAY = 86164.0905  # s
R_GEO = (MU * (SIDEREAL_DAY / (2 * math.pi)) ** 2) ** (1 / 3)
def vcirc(r): return math.sqrt(MU / r)
def vis_viva(r, a): return math.sqrt(MU * (2 / r - 1 / a))
def period(a): return 2 * math.pi * math.sqrt(a ** 3 / MU)
def vesc(r): return math.sqrt(2 * MU / r)
def hohmann(r1, r2):
    at = (r1 + r2) / 2
    dv1 = vis_viva(r1, at) - vcirc(r1); dv2 = vcirc(r2) - vis_viva(r2, at)
    return dict(at=at, dv1=dv1, dv2=dv2, dv=abs(dv1) + abs(dv2), tof=period(at) / 2)
def bielliptic(r1, r2, rb):
    a1, a2 = (r1 + rb) / 2, (r2 + rb) / 2
    d1 = vis_viva(r1, a1) - vcirc(r1); d2 = vis_viva(rb, a2) - vis_viva(rb, a1); d3 = vis_viva(r2, a2) - vcirc(r2)
    return dict(dv1=d1, dv2=d2, dv3=abs(d3), dv=abs(d1) + abs(d2) + abs(d3), tof=(period(a1) + period(a2)) / 2)
def plane_change(v, di_deg): return 2 * v * math.sin(math.radians(di_deg) / 2)
def combined(v1, v2, di_deg): return math.sqrt(v1 ** 2 + v2 ** 2 - 2 * v1 * v2 * math.cos(math.radians(di_deg)))
def mass_ratio(dv, isp): return math.exp(dv / (isp * G0))
def kepler_E(M, e, tol=1e-12):
    E = M if e < 0.8 else math.pi; steps = []
    for _ in range(50):
        f = E - e * math.sin(E) - M; d = f / (1 - e * math.cos(E)); E -= d; steps.append(E)
        if abs(d) < tol: break
    return E, steps
def raan_rate(a, e, i_deg):
    n = math.sqrt(MU / a ** 3); p = a * (1 - e * e)
    return -1.5 * n * J2 * (RE / p) ** 2 * math.cos(math.radians(i_deg))   # rad/s
def sun_sync_incl(alt):
    a = RE + alt; n = math.sqrt(MU / a ** 3); target = 2 * math.pi / (365.2422 * 86400)
    return math.degrees(math.acos(-target / (1.5 * n * J2 * (RE / a) ** 2)))
def coe(r, v):
    import numpy as np
    r = np.array(r, float); v = np.array(v, float); R = np.linalg.norm(r); V = np.linalg.norm(v)
    h = np.cross(r, v); H = np.linalg.norm(h); i = math.degrees(math.acos(h[2] / H))
    N = np.cross([0, 0, 1], h); Nn = np.linalg.norm(N)
    ev = ((V ** 2 - MU / R) * r - np.dot(r, v) * v) / MU; e = np.linalg.norm(ev)
    raan = math.degrees(math.acos(N[0] / Nn)); raan = raan if N[1] >= 0 else 360 - raan
    w = math.degrees(math.acos(np.dot(N, ev) / (Nn * e))); w = w if ev[2] >= 0 else 360 - w
    nu = math.degrees(math.acos(np.dot(ev, r) / (e * R))); nu = nu if np.dot(r, v) >= 0 else 360 - nu
    a = 1 / (2 / R - V ** 2 / MU)
    return dict(h=H, i=i, raan=raan, e=e, w=w, nu=nu, a=a, energy=V ** 2 / 2 - MU / R)
# --- universal-variable Lambert (Curtis Alg. 5.2 / Bate-Mueller-White ch.5) + Kepler propagation check
def _C(z): return (1 - math.cos(math.sqrt(z))) / z if z > 0 else ((math.cosh(math.sqrt(-z)) - 1) / -z if z < 0 else 0.5)
def _S(z):
    if z > 0: s = math.sqrt(z); return (s - math.sin(s)) / s ** 3
    if z < 0: s = math.sqrt(-z); return (math.sinh(s) - s) / s ** 3
    return 1 / 6
def lambert(r1, r2, tof, prograde=True):
    import numpy as np
    r1 = np.array(r1, float); r2 = np.array(r2, float); R1, R2 = np.linalg.norm(r1), np.linalg.norm(r2)
    c = np.cross(r1, r2); dth = math.acos(np.dot(r1, r2) / (R1 * R2))
    if (prograde and c[2] < 0) or (not prograde and c[2] >= 0): dth = 2 * math.pi - dth
    A = math.sin(dth) * math.sqrt(R1 * R2 / (1 - math.cos(dth)))
    y = lambda z: R1 + R2 + A * (z * _S(z) - 1) / math.sqrt(_C(z))
    F = lambda z: (y(z) / _C(z)) ** 1.5 * _S(z) + A * math.sqrt(y(z)) - math.sqrt(MU) * tof
    lo, hi = -4 * math.pi ** 2, 4 * math.pi ** 2
    while y(lo) < 0: lo += 0.1
    for _ in range(200):  # bisection on F (monotonic in z for the single-revolution case)
        mid = (lo + hi) / 2
        if F(mid) > 0: hi = mid
        else: lo = mid
    z = (lo + hi) / 2; yz = y(z)
    f = 1 - yz / R1; g = A * math.sqrt(yz / MU); gd = 1 - yz / R2
    v1 = (r2 - f * r1) / g; v2 = (gd * r2 - r1) / g
    return v1, v2
def propagate(r, v, t, steps=20000):
    import numpy as np
    r = np.array(r, float); v = np.array(v, float); h = t / steps
    acc = lambda x: -MU * x / np.linalg.norm(x) ** 3
    for _ in range(steps):  # RK4 on the two-body ODE r'' = -mu r / |r|^3
        k1v = acc(r); k1r = v
        k2v = acc(r + h / 2 * k1r); k2r = v + h / 2 * k1v
        k3v = acc(r + h / 2 * k2r); k3r = v + h / 2 * k2v
        k4v = acc(r + h * k3r); k4r = v + h * k3v
        r = r + h / 6 * (k1r + 2 * k2r + 2 * k3r + k4r); v = v + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    return r, v
def examples():
    import numpy as np
    X = {}
    r = RE + 400; X['iss_v'] = vcirc(r); X['iss_T'] = period(r) / 60
    X['vesc0'] = vesc(RE); X['rgeo'] = R_GEO; X['vgeo'] = vcirc(R_GEO)
    h = hohmann(RE + 300, R_GEO); X.update({'h_' + k: v for k, v in h.items()}); X['v300'] = vcirc(RE + 300)
    X['h_vp'] = vis_viva(RE + 300, h['at']); X['h_va'] = vis_viva(R_GEO, h['at'])
    r1 = RE + 300; X['bi_r1'] = r1; X['bi_r2'] = 20 * r1; X['bi_rb'] = 40 * r1
    X['bi_h'] = hohmann(r1, 20 * r1)['dv']; X['bi_b'] = bielliptic(r1, 20 * r1, 40 * r1)['dv']
    X['pc_leo'] = plane_change(vcirc(RE + 300), 28.5); X['pc_geo'] = plane_change(R_GEO and vcirc(R_GEO), 28.5)
    X['pc_comb'] = combined(h_va := vis_viva(R_GEO, h['at']), vcirc(R_GEO), 28.5); X['pc_sep'] = (vcirc(R_GEO) - h_va) + plane_change(vcirc(R_GEO), 28.5)
    X['mr'] = mass_ratio(h['dv'], 450); X['mr_prop'] = 1 - 1 / X['mr']
    E, st = kepler_E(math.radians(30), 0.5); X['kep_E'] = math.degrees(E); X['kep_steps'] = [math.degrees(s) for s in st]
    X['ss_i'] = sun_sync_incl(700); X['iss_raan'] = math.degrees(raan_rate(RE + 420, 0, 51.64)) * 86400
    c = coe([7000, 1000, 500], [-1.0, 7.4, 1.0]); X.update({'coe_' + k: v for k, v in c.items()})
    r1v, r2v, tof = [7000, 0, 0], [0, 8000, 0], 3600
    v1, v2 = lambert(r1v, r2v, tof); rf, vf = propagate(r1v, v1, tof)
    X['lam_v1'] = list(v1); X['lam_v2'] = list(v2); X['lam_err'] = float(np.linalg.norm(rf - np.array(r2v)))
    X['T_geo_h'] = period(R_GEO) / 3600
    return X
if __name__ == '__main__':
    for k, v in examples().items(): print(k, v)


def kepler_table(M, e, tol=1e-10):
    """Newton-Raphson on M = E - e sin E (radians); E0 = M (or pi if e > 0.8). Returns [(n, E_n, |dE|)]."""
    E = math.pi if e > 0.8 else M; rows = []
    for n in range(1, 50):
        dE = (E - e * math.sin(E) - M) / (1 - e * math.cos(E)); E -= dE; rows.append((n, E, abs(dE)))
        if abs(dE) < tol: break
    return rows


def extras():
    """Oct 16 benchmark-spec flagship numbers (verified in build): Curtis Ex. 3.2-style Kepler case, combined LEO->GEO total,
    hover momentum theory for a generic ~2700 kg light helicopter (R = 5.1 m, sea-level ISA rho = 1.225 kg/m^3) for the Phase 2 plan."""
    ex = examples(); out = {}
    rows = kepler_table(3.6029, 0.37255); out['k2_rows'] = rows; out['k2_E'] = rows[-1][1]; out['k2_n'] = len(rows)
    out['geo_comb_total'] = ex['h_dv1'] + ex['pc_comb']
    T = 2700 * 9.80665; A = math.pi * 5.1 ** 2; vi = math.sqrt(T / (2 * 1.225 * A))
    out.update(rot_T=T, rot_A=A, rot_vi=vi, rot_P_kW=T * vi / 1000)
    return out
