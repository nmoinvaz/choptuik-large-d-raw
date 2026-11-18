# diagnostic on the planted-truth control only: three point masses at REF541 with free complex weights, solved so that
# the Pade poles at k = 8, 9, 10 land on REF541 (no scan plant)
import sys, math
import numpy as np
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-747/solver/inner_amp")
import pade_far_poles as PF
from scipy.optimize import least_squares
ss, mp, pg, KS = PF.ss, PF.mp, PF.pg, PF.KS
nodes = {wf: PF.FNode(wf) for wf in PF.NODES}
kind = sys.argv[1] if len(sys.argv) > 1 else "chord2"
def plant(wf, w3):
    """main + masses at REF541[wf][k] with complex weights w3 (share of sigma_22 per unit weight as eta e^{i phi})"""
    node = nodes[wf]; main = node.mains[kind]
    mp.mp.dps = pg.DPS_PLANT
    pts = [ss.REF541[wf][k] for k in KS]
    mom = PF.pole_moments(pts)       # equal weights 1/3 each; individual weights via separate parts
    parts = []
    for j in range(3):
        m = [ (mp.mpc(pts[j]) ** k) / mp.factorial(k) for k in range(pg.KM + 1)]
        parts.append(PF.pp.polymul(main.base.pref, m, pg.KM + 1))
    # combined part with weights; make_plant normalises by eta e^{i phi} real[22]/w[22]; use eta = 1, phase 0 on the sum
    w = [sum(complex_to_mp(w3[j]) * parts[j][k] for j in range(3)) for k in range(pg.KM + 1)]
    return ss.make_plant(main, w, 1.0, 0)
def complex_to_mp(z): return mp.mpc(z.real, z.imag)
def resid(x):
    w3 = [complex(x[2*j], x[2*j+1]) for j in range(3)]
    out = []
    for wf in PF.NODES:
        sig, info = plant(wf, w3)
        pl = PF.poles(sig, wf)
        for k in KS:
            d = pl[k]["nearest"] - ss.REF541[wf][k]
            out += [d.real, d.imag]
    return np.array(out)
best = None
for s0 in (1.0, 10.0, 100.0):
    x0 = np.array([s0/3, 0, s0/3, 0, s0/3, 0]) * 1e0
    # weights in units where w[22] normalises: make_plant scales lam = eta e^{i phi} real22 / w[22] for the SUM, so w3 is relative
    r0 = resid(x0)
    print(f"start scale {s0:g}: |resid| max {np.abs(r0).max():.4f}", flush=True)
    try:
        sol = least_squares(resid, x0, method="lm", max_nfev=60, xtol=1e-10, ftol=1e-10)
    except Exception as e:
        print("  failed", e); continue
    r = sol.fun
    d3 = max(math.hypot(r[2*i], r[2*i+1]) for i in range(9))
    print(f"  solved: max |pole - REF541| {d3:.2e}, weights {[complex(sol.x[2*j], sol.x[2*j+1]) for j in range(3)]}, nfev {sol.nfev}", flush=True)
    sig, info = plant(1.0, [complex(sol.x[2*j], sol.x[2*j+1]) for j in range(3)])
    print(f"  at wf 1.00: fit_resid {info['fit_resid']:.1e} M {info['M']} share12 {info['share'][12]:.2e} share22 {info['share'][22]:.2e} lam_abs {info['lam_abs']:.2e}", flush=True)
