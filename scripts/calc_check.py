#!/usr/bin/env python3
"""Oct 16 2026: numbers for the search-named calculator pages. Every value printed on those pages comes from here (built on
learn_calc.py / aero_calc.py / phys_calc.py), and checks() compares them with textbook / reference values at build time.
Also writes scripts/calc-vectors.json, which scripts/test-calcs.js uses to check assets/calc.js gives the same answers."""
import math, json, sys
sys.path.insert(0, 'scripts')
import learn_calc as LC, aero_calc as AC, phys_calc as PC
G0 = 9.80665
def dv(isp, m0, mf): mr = m0 / mf; return dict(dv=isp * G0 * math.log(mr), mr=mr, pf=(1 - mf / m0) * 100)
def hohmann(h1, h2):
    h = LC.hohmann(LC.RE + h1, LC.RE + h2); return dict(dv1=abs(h['dv1']), dv2=abs(h['dv2']), dv=h['dv'], tof=h['tof'] / 3600)
def period(h): a = LC.RE + h; T = LC.period(a); return dict(tmin=T / 60, th=T / 3600, v=LC.vcirc(a))
def vel(h): r = LC.RE + h; return dict(vc=LC.vcirc(r), ve=LC.vesc(r))
def stall(m, S, cl, alt, bank):
    rho = AC.isa(alt)[2]; vs = AC.stall_speed(m, S, cl, rho); n = 1 / math.cos(math.radians(bank))
    return dict(rho=rho, vs=vs, kn=vs / 0.514444, kmh=vs * 3.6, n=n, vb=vs * math.sqrt(n))
def lift(alt, V, S, cl): rho = AC.isa(alt)[2]; q = 0.5 * rho * V * V; L = q * S * cl; return dict(rho=rho, q=q, L=L, kg=L / G0)
def mach(alt, V): T = AC.isa(alt)[0]; a = AC.sound(T); return dict(T=T, TC=T - 273.15, a=a, akmh=a * 3.6, M=V / a)
def tw(F, m, g): return dict(tw=F * 1000 / (m * g), a=F * 1000 / m - g)
def rotor(m, R, FM, alt):
    hv = AC.hover(m, R, rho=AC.isa(alt)[2]); return dict(T=hv['T'] / 1000, A=hv['A'], DL=hv['DL'], vi=hv['vi'], Pi=hv['P_kW'], Pa=hv['P_kW'] / FM)
def proj(v0, ang, m, d, cd):
    r, top, t = PC.drag_traj(v0, ang, m, d, cd) if cd > 0 else PC.drag_traj(v0, ang, m, d, 1e-12)
    th = math.radians(ang); return dict(range=r, top=top, time=t, r0=v0 ** 2 * math.sin(2 * th) / G0, top0=(v0 * math.sin(th)) ** 2 / (2 * G0))
def pend(L, a): T0, T = PC.pend_period(L, a); return dict(T0=T0, T=T, pct=(T / T0 - 1) * 100)
FN = dict(dv=dv, hohmann=hohmann, period=period, vel=vel, stall=stall, lift=lift, mach=mach, tw=tw, rotor=rotor, proj=proj, pend=pend)
# Worked examples shown on the pages (inputs in the order of each calculator's form)
EX = dict(dv=dict(isp=300, m0=1000, mf=400), hohmann=dict(h1=300, h2=35786), period=dict(h=400), vel=dict(h=400),
          stall=dict(m=1100, S=16.2, cl=1.6, alt=0, bank=30), lift=dict(alt=0, V=50, S=16.2, cl=0.5), mach=dict(alt=11000, V=250),
          tw=dict(F=6000, m=400000, g=G0), rotor=dict(m=2700, R=5.1, FM=0.75, alt=0), proj=dict(v0=40, ang=35, m=0.145, d=0.074, cd=0.35),
          pend=dict(L=1, a=60))
def example(k): return FN[k](**EX[k])
def checks():
    r = lambda a, b, t: abs(a - b) <= t
    assert r(dv(300, math.e * 100, 100)['dv'], 300 * G0, 1e-9)                 # m0/mf = e  ->  dv = Isp g0 (definition)
    assert r(hohmann(300, 35786)['dv'], 3.89, 0.01)                             # LEO 300 km -> GEO about 3.89 km/s (Curtis ch. 6)
    assert r(period(35786)['th'], 23.934, 0.002)                                 # GEO period = sidereal day 23 h 56 min (Vallado)
    assert 92.4 < period(400)['tmin'] < 92.8                                     # ISS-like 400 km orbit about 92.6 min
    assert r(math.sqrt(2 * LC.MU / 6371.0), 11.186, 0.001) and r(vel(0)['ve'], 11.18, 0.001) and r(vel(0)['vc'], 7.905, 0.001)  # NASA Earth fact sheet: 11.186 km/s with the 6371 km mean radius; 11.18 at the equatorial radius used here
    assert r(AC.isa(0)[2], 1.225, 5e-4) and r(AC.isa(11000)[0], 216.65, 1e-9)   # USSA 1976
    assert r(stall(1100, 16.2, 1.6, 0, 60)['vb'] / stall(1100, 16.2, 1.6, 0, 0)['vs'], math.sqrt(2), 1e-12)   # 60 deg bank: n = 2, Vs x 1.414 (FAA PHAK ch. 5)
    s = stall(1100, 16.2, 1.6, 0, 0); assert r(lift(0, s['vs'], 16.2, 1.6)['kg'], 1100, 1e-9)                    # at Vs with CLmax, lift = weight
    assert r(mach(0, 0)['a'], 340.29, 0.01) and r(mach(11000, 0)['a'], 295.07, 0.01)                             # USSA 1976 speed of sound table
    assert r(tw(1, 1000 / G0, G0)['tw'], 1, 1e-12) and r(tw(1, 1000 / G0, G0)['a'], 0, 1e-9)                       # T/W = 1 -> no net acceleration
    h = rotor(2700, 5.1, 0.75, 0); assert r(h['vi'], math.sqrt(2700 * G0 / (2 * 1.225 * math.pi * 5.1 ** 2)), 1e-4)  # Leishman eq. 2.14
    assert r(proj(40, 35, 0.145, 0.074, 0)['range'], 40 ** 2 * math.sin(math.radians(70)) / G0, 1e-3)               # no drag -> v0^2 sin 2a / g
    assert r(proj(40, 35, 0.145, 0.074, 0.35)['range'], PC.examples()['p_rng'], 1e-9)                              # same engine as Physics Lab
    assert r(pend(1, 1e-6)['T0'], 2.006, 5e-4) and r(pend(1, 60)['T'] / pend(1, 60)['T0'], 1.0732, 1e-4)            # 1 m pendulum 2.006 s; 60 deg factor 1.0732 (elliptic integral tables)
    return True
VEC = [('dv', dict(isp=300, m0=1000, mf=400)), ('dv', dict(isp=450, m0=5000, mf=1200)), ('hohmann', dict(h1=300, h2=35786)), ('hohmann', dict(h1=35786, h2=400)),
       ('period', dict(h=400)), ('period', dict(h=35786)), ('vel', dict(h=0)), ('vel', dict(h=2000)), ('stall', dict(m=1100, S=16.2, cl=1.6, alt=1500, bank=45)),
       ('lift', dict(alt=3000, V=70, S=20, cl=0.6)), ('mach', dict(alt=15000, V=600)), ('mach', dict(alt=5000, V=200)), ('tw', dict(F=7600, m=549000, g=G0)), ('tw', dict(F=45, m=3000, g=1.62)),
       ('rotor', dict(m=2700, R=5.1, FM=0.75, alt=1500)), ('proj', dict(v0=40, ang=35, m=0.145, d=0.074, cd=0.35)), ('proj', dict(v0=25, ang=50, m=0.43, d=0.22, cd=0.25)),
       ('pend', dict(L=1, a=60)), ('pend', dict(L=2.5, a=120))]
if __name__ == '__main__':
    assert checks()
    json.dump([dict(id=k, x=x, y=FN[k](**x)) for k, x in VEC], open('scripts/calc-vectors.json', 'w'), indent=0)
    for k in FN: print(k, {a: round(b, 4) for a, b in example(k).items()})
