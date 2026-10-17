#!/usr/bin/env python3
"""Oct 16 Phase 3: every Physics-track number on the site is computed here (never typed). SI units, CODATA 2018 exact/recommended constants.
Placeholders {p_key:digits}. Generic, illustrative objects only."""
import math
G0 = 9.80665; C = 299792458.0; QE = 1.602176634e-19; MP = 1.67262192369e-27; ME = 9.1093837015e-31
EPS0 = 8.8541878128e-12; MU0 = 1.25663706212e-6; KB = 1.380649e-23; NA = 6.02214076e23
GM_E = 3.986004418e14; R_E = 6378137.0; GM_S = 1.32712440018e20
def collide1d(m1, u1, m2, u2):  # elastic
    v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2); v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2); return v1, v2
def drag_traj(v0, deg, m, d, cd, rho=1.225, dt=0.001, g=G0):  # RK4, quadratic drag; returns range, apex, flight time
    k = 0.5 * rho * cd * math.pi * d * d / 4 / m; th = math.radians(deg)
    def f(s):
        x, y, vx, vy = s; v = math.hypot(vx, vy); return (vx, vy, -k * v * vx, -g - k * v * vy)
    s = (0.0, 0.0, v0 * math.cos(th), v0 * math.sin(th)); t = 0.0; top = 0.0
    while True:
        a = f(s); b = f(tuple(s[i] + dt / 2 * a[i] for i in range(4))); c = f(tuple(s[i] + dt / 2 * b[i] for i in range(4))); e = f(tuple(s[i] + dt * c[i] for i in range(4)))
        n = tuple(s[i] + dt / 6 * (a[i] + 2 * b[i] + 2 * c[i] + e[i]) for i in range(4)); t += dt; top = max(top, n[1])
        if n[1] < 0:
            fr = s[1] / (s[1] - n[1]); return s[0] + fr * (n[0] - s[0]), top, t - dt + fr * dt
        s = n
def vterm(m, d, cd, rho=1.225, g=G0): return math.sqrt(2 * m * g / (rho * cd * math.pi * d * d / 4))
def damped(m, c, k):
    wn = math.sqrt(k / m); z = c / (2 * math.sqrt(k * m)); wd = wn * math.sqrt(1 - z * z) if z < 1 else 0.0; return wn, z, wd, -z * wn
def agm(a, b):
    while abs(a - b) > 1e-15: a, b = (a + b) / 2, math.sqrt(a * b)
    return a
def pend_period(L, deg, g=G0):  # exact: T = 2*pi*sqrt(L/g) / agm(1, cos(theta0/2))
    T0 = 2 * math.pi * math.sqrt(L / g); return T0, T0 / agm(1.0, math.cos(math.radians(deg) / 2))
def gyro(m, q, v, B): return m * v / (abs(q) * B), abs(q) * B / m  # radius m, angular freq rad/s
def plasma_f(n): return math.sqrt(n * QE * QE / (EPS0 * ME)) / (2 * math.pi)
def vrms(Mkg, T): return math.sqrt(3 * KB * T * NA / Mkg)
def vmean(Mkg, T): return math.sqrt(8 * KB * T * NA / (math.pi * Mkg))
def carnot(Tc, Th): return 1 - Tc / Th
def sutherland(T): return 1.458e-6 * T ** 1.5 / (T + 110.4)
def poiseuille(R, L, dp, mu): return math.pi * R ** 4 * dp / (8 * mu * L)
def gps_clock(a=26561750.0, R=R_E):  # microseconds per day: GR (potential), SR (velocity), net
    gr = GM_E * (1 / R - 1 / a) / C ** 2; sr = -(GM_E / a) / (2 * C ** 2); d = 86400e6; return gr * d, sr * d, (gr + sr) * d
def perihelion(a=5.7909050e10, e=0.205630, P_days=87.9691):
    dphi = 6 * math.pi * GM_S / (C * C * a * (1 - e * e)); return dphi * (36525 / P_days) * 180 / math.pi * 3600  # arcsec / century
def examples():
    X = {}
    X['p_v_drop'] = math.sqrt(2 * G0 * 20)
    v1, v2 = collide1d(2.0, 3.0, 1.0, 0.0); X.update(p_v1=v1, p_v2=v2)
    X['p_ke0'] = 0.5 * 2 * 9; X['p_ke1'] = 0.5 * 2 * v1 ** 2 + 0.5 * 1 * v2 ** 2
    v1b, v2b = collide1d(1.0, 4.0, 3.0, 0.0); X.update(p_np1=v2b, p_np1b=v1b)
    rng, top, tf = drag_traj(40, 35, 0.145, 0.074, 0.35); X.update(p_rng=rng, p_top=top, p_tf=tf)
    X['p_rng0'] = 40 ** 2 * math.sin(math.radians(70)) / G0; X['p_top0'] = (40 * math.sin(math.radians(35))) ** 2 / (2 * G0); X['p_tf0'] = 2 * 40 * math.sin(math.radians(35)) / G0
    X['p_k'] = 0.5 * 1.225 * 0.35 * math.pi * 0.074 ** 2 / 4 / 0.145
    X['p_vt'] = vterm(0.145, 0.074, 0.35)
    X['p_rng2'] = drag_traj(40, 35, 0.145, 0.074, 0.35, dt=0.0005)[0]
    X['p_best'] = max((drag_traj(40, a / 2, 0.145, 0.074, 0.35, dt=0.002)[0], a / 2) for a in range(60, 91))[1]
    X['p_np2'] = drag_traj(40, 45, 0.145, 0.074, 0.35)[0]
    wn, z, wd, sre = damped(1.0, 2.0, 16.0); X.update(p_wn=wn, p_z=z, p_wd=wd, p_sre=sre, p_Q=1 / (2 * z))
    X['p_np3'] = damped(0.5, 1.2, 8.0)[1]
    T0, Tx = pend_period(1.0, 60); X.update(p_T0=T0, p_T60=Tx, p_Tpct=(Tx / T0 - 1) * 100)
    X['p_np4'] = pend_period(2.0, 90)[1]; X['p_np4T0'] = pend_period(2.0, 90)[0]
    r, w = gyro(MP, QE, 4.0e5, 5e-9); X.update(p_rg_km=r / 1000, p_wg=w, p_fg=w / (2 * math.pi), p_Tg=2 * math.pi / w)
    X['p_c'] = 1 / math.sqrt(MU0 * EPS0); X['p_fp_kHz'] = plasma_f(5e6) / 1000
    X['p_np5'] = gyro(ME, QE, 1.0e6, 3e-5)[0]
    X['p_vrms'] = vrms(0.0280134, 300); X['p_vmean'] = vmean(0.0280134, 300); X['p_carnot'] = carnot(300, 600)
    X['p_np6'] = vrms(0.0319988, 300)
    X['p_mu11'] = sutherland(216.65); X['p_rho11'] = 0.363918; X['p_Re'] = 0.363918 * 250 * 5 / sutherland(216.65)
    X['p_mu288'] = sutherland(288.15); X['p_np7'] = 1.225 * 30 * 0.2 / sutherland(288.15)
    X['p_Q_mL'] = poiseuille(0.0005, 0.1, 1000, 1.0e-3) * 1e6
    gr, sr, net = gps_clock(); X.update(p_gr=gr, p_sr=sr, p_sr_abs=-sr, p_net=net, p_net_m=net * 1e-6 * C / 1000)
    X['p_mer'] = perihelion(); X['p_np8'] = perihelion(1.0821e11, 0.006772, 224.701)
    return X
if __name__ == '__main__':
    for k, v in examples().items(): print(k, round(v, 6))
def checks():
    """Build-time guard: every literal number typed in learn_phys.py text must agree with the computed values / published references."""
    X = examples(); r = lambda a, b, t: abs(a - b) <= t
    assert r(X['p_mer'], 42.98, 0.01)                     # Will 2014
    assert r(X['p_mu11'], 1.4216e-5, 1e-9)                 # USSA 1976 at 11 km
    assert f'{X["p_mu11"]:.3g}' == '1.42e-05' and f'{X["p_Re"]:.2g}' == '3.2e+07' and f'{X["p_mu288"]:.4g}' == '1.789e-05'
    assert r(agm(1, math.cos(math.radians(30))), 0.931808, 1e-6) and r(agm(1, math.cos(math.radians(45))), 0.8472, 1e-4)
    assert round(math.radians(60) ** 2 / 16 * 100, 1) == 6.9 and round((X['p_np4'] / X['p_np4T0'] - 1) * 100) == 18
    assert pend_period(1, 20)[1] / pend_period(1, 20)[0] - 1 > 0.007
    assert 75 <= X['p_Re'] / X['p_np7'] <= 85               # "about 80 times"
    assert abs(X['p_net'] - 38.6) < 0.2 and abs(X['p_gr'] - 45.7) < 0.2 and abs(X['p_sr'] + 7.1) < 0.2   # Ashby 2003
    assert r(math.sqrt(3 * math.pi / 8), 1.085, 5e-4) and r(math.sqrt(1.4 * 287.05287 * 300), 347, 0.5) and X['p_vmean'] > 347
    assert r(KB * NA, 8.314463, 1e-6) and r(math.radians(8), 0.13963, 1e-5)
    assert abs(X['p_rng2'] - X['p_rng']) < 1e-3 and abs(X['p_vt'] - 40) < 1                     # converged; v0 ~ terminal
    assert 3.9 < 365.25 / 87.9691 < 4.3 and X['p_wn'] ** 2 == 16 and X['p_sre'] == -1.0
    return True
