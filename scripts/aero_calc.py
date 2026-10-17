#!/usr/bin/env python3
"""Oct 16 Phase 2: every Aeronautical Engineering number on the site is computed here (never typed). SI units.
ISA: U.S. Standard Atmosphere 1976 troposphere/lower stratosphere. Generic aircraft only (illustrative values, no specific type)."""
import math
G0, R_AIR, GAM = 9.80665, 287.05287, 1.4
T0, P0 = 288.15, 101325.0
def isa(h):  # h geopotential metres, 0..20 000
    if h <= 11000:
        T = T0 - 0.0065 * h; p = P0 * (T / T0) ** (G0 / (0.0065 * R_AIR))
    else:
        T = 216.65; p11 = P0 * (216.65 / T0) ** (G0 / (0.0065 * R_AIR)); p = p11 * math.exp(-G0 * (h - 11000) / (R_AIR * T))
    return T, p, p / (R_AIR * T)
def sound(T): return math.sqrt(GAM * R_AIR * T)
def thin_cl(alpha_deg): return 2 * math.pi * math.radians(alpha_deg)
def stall_speed(m, S, clmax, rho=1.225): return math.sqrt(2 * m * G0 / (rho * S * clmax))
def k_ind(AR, e): return 1 / (math.pi * e * AR)
def cdi(CL, AR, e): return CL ** 2 * k_ind(AR, e)
def cla_finite(AR, e, a0=2 * math.pi): return a0 / (1 + a0 / (math.pi * e * AR))
def ld_max(CD0, AR, e): return 1 / (2 * math.sqrt(CD0 * k_ind(AR, e)))
def cl_star(CD0, AR, e): return math.sqrt(CD0 / k_ind(AR, e))
def breguet_jet(V, c_per_h, LD, wi_wf): return V / (c_per_h / 3600) * LD * math.log(wi_wf)  # metres
def isentropic(M, g=GAM): t = 1 + (g - 1) / 2 * M * M; return t, t ** (g / (g - 1))  # T0/T, p0/p
def normal_shock(M1, g=GAM):
    M2 = math.sqrt((1 + (g - 1) / 2 * M1 ** 2) / (g * M1 ** 2 - (g - 1) / 2)); p21 = 1 + 2 * g / (g + 1) * (M1 ** 2 - 1)
    t01, _ = isentropic(M1, g); p01 = isentropic(M1, g)[1]; p02 = isentropic(M2, g)[1]
    r21 = (g + 1) * M1 ** 2 / ((g - 1) * M1 ** 2 + 2)
    return M2, p21, (p21 * p02) / p01  # p02/p01 = (p2/p1)(p02/p2)/(p01/p1)
def brayton_eta(pi_c, g=GAM): return 1 - pi_c ** (-(g - 1) / g)
def short_period(ZaV, Mq, Mad, Ma):
    b = -(ZaV + Mq + Mad); c = ZaV * Mq - Ma; wn = math.sqrt(c); z = b / (2 * wn)
    disc = b * b - 4 * c; re = -b / 2; im = math.sqrt(-disc) / 2 if disc < 0 else 0.0
    return wn, z, re, im
def hover(m, R, rho=1.225, P_actual_kW=None):
    T = m * G0; A = math.pi * R * R; vi = math.sqrt(T / (2 * rho * A)); P = T * vi
    out = dict(T=T, A=A, vi=vi, P_kW=P / 1000, DL=T / A)
    if P_actual_kW: out['FM'] = P / 1000 / P_actual_kW
    return out
def fd_errors(x=1.0, h=0.1):
    fwd = (math.sin(x + h) - math.sin(x)) / h; cen = (math.sin(x + h) - math.sin(x - h)) / (2 * h); ex = math.cos(x)
    return fwd, cen, abs(fwd - ex), abs(cen - ex)
def examples():
    X = {}
    T, p, r = isa(11000); X.update(a_T11=T, a_p11=p, a_r11=r, a_a11=sound(T))
    T, p, r = isa(5000); X.update(a_T5=T, a_p5=p, a_r5=r)
    X['a_cl5'] = thin_cl(5)
    X['a_vs'] = stall_speed(1100, 16.2, 1.6); X['a_vs_kn'] = X['a_vs'] / 0.514444
    X['a_vs5'] = stall_speed(1100, 16.2, 1.6, isa(1500)[2])
    X['a_cdi'] = cdi(0.5, 9, 0.8); X['a_cla'] = cla_finite(9, 0.8); X['a_k'] = k_ind(9, 0.8)
    X['a_ldmax'] = ld_max(0.02, 9, 0.8); X['a_clstar'] = cl_star(0.02, 9, 0.8)
    X['a_range_km'] = breguet_jet(230, 0.6, 17, 1.25) / 1000; X['a_range_nmi'] = X['a_range_km'] / 1.852
    t, pr = isentropic(2.0); X.update(a_T0T=t, a_p0p=pr)
    M2, p21, p0r = normal_shock(2.0); X.update(a_M2=M2, a_p21=p21, a_p0r=p0r)
    X['a_eta30'] = brayton_eta(30); X['a_eta10'] = brayton_eta(10)
    X['a_thrust_kN'] = 100 * (600 - 250) / 1000
    wn, z, re, im = short_period(-1.0, -1.5, -0.3, -8.0); X.update(a_wn=wn, a_zeta=z, a_sre=re, a_sim=im)
    hv = hover(2700, 5.1, P_actual_kW=400); X.update(a_rT=hv['T'], a_rA=hv['A'], a_vi=hv['vi'], a_P=hv['P_kW'], a_DL=hv['DL'], a_FM=hv['FM'])
    f, c, ef, ec = fd_errors(); X.update(a_fwd=f, a_cen=c, a_efwd=ef, a_ecen=ec, a_cos1=math.cos(1.0))
    X['a_h11ft'] = 11000 / 0.3048
    return X
if __name__ == '__main__':
    for k, v in examples().items(): print(k, round(v, 6))
def bemt(sigma, a, theta_deg, cd0):  # combined blade-element momentum theory, hover, uniform inflow, linear twist-free, theta at 0.75R (Leishman ch. 3)
    th = math.radians(theta_deg); lam = sigma * a / 16 * (math.sqrt(1 + 64 * th / (3 * sigma * a)) - 1)
    CT = sigma * a / 2 * (th / 3 - lam / 2); CPi = CT ** 1.5 / math.sqrt(2); CPo = sigma * cd0 / 8
    return dict(lam=lam, CT=CT, CPi=CPi, CPo=CPo, CP=CPi + CPo, FM=CPi / (CPi + CPo))
_ex0 = examples
def examples():
    X = _ex0(); b = bemt(0.08, 5.73, 8.0, 0.011); X.update({'a_b' + k: v for k, v in b.items()})
    X['a_bchk'] = math.sqrt(b['CT'] / 2)  # must equal a_blam
    b2 = bemt(0.08, 5.73, 10.0, 0.011); X['a_b2CT'] = b2['CT']; X['a_b2FM'] = b2['FM']
    return X
