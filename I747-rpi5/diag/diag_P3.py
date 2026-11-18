# diagnostic on the planted-truth control only: three point masses at REF541, ratios r2, r3, eta, phi solved at wf 1.00
import sys, math, time
import numpy as np
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-747/solver/inner_amp")
import pade_far_poles as PF
from scipy.optimize import least_squares
ss, mp, pg, KS = PF.ss, PF.mp, PF.pg, PF.KS
kind = sys.argv[1] if len(sys.argv) > 1 else "chord2"
nodes = {wf: PF.FNode(wf) for wf in PF.NODES}
cache = {}
def parts(wf):
    if wf not in cache:
        main = nodes[wf].mains[kind]
        mp.mp.dps = pg.DPS_PLANT
        out = []
        for k0 in KS:
            t = mp.mpc(ss.REF541[wf][k0])
            m = [t ** k / mp.factorial(k) for k in range(pg.KM + 1)]
            out.append(PF.pp.polymul(main.base.pref, m, pg.KM + 1))
        cache[wf] = out
    return cache[wf]
def plant(wf, x):
    r2, r3 = mp.mpc(x[0], x[1]), mp.mpc(x[2], x[3])
    p = parts(wf)
    w = [p[0][k] + r2 * p[1][k] + r3 * p[2][k] for k in range(pg.KM + 1)]
    return ss.make_plant(nodes[wf].mains[kind], w, 10.0 ** x[4], x[5])
def deltas(wf, x):
    sig, info = plant(wf, x)
    pl = PF.poles(sig, wf)
    return [pl[k]["nearest"] - ss.REF541[wf][k] for k in KS], info
def resid(x):
    d, _ = deltas(1.0, x)
    return np.array([v for z in d for v in (z.real, z.imag)])
x0 = np.array([1, 0, 1, 0, 0.0, 0.0])
t0 = time.time()
sol = least_squares(resid, x0, method="lm", max_nfev=120, xtol=1e-12, ftol=1e-12)
d, info = deltas(1.0, sol.x)
print(f"{kind}: solved at wf 1.00 in {time.time()-t0:.0f}s, nfev {sol.nfev}: max |pole - REF541| {max(abs(z) for z in d):.2e}; x {np.round(sol.x, 4).tolist()}")
print(f"  eta {10**sol.x[4]:.3g} phi {sol.x[5]:.1f}; fit_resid {info['fit_resid']:.1e} M {info['M']} share12 {info['share'][12]:.2e} share22 {info['share'][22]:.2e}")
for wf in PF.NODES:
    d, info = deltas(wf, sol.x)
    print(f"  wf {wf}: d_8,9,10 = " + ", ".join(f"{abs(z):.4f}" for z in d) + f"; fit_resid {info['fit_resid']:.1e}")
