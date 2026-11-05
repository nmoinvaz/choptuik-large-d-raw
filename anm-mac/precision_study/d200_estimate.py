"""Estimates (not measurements) for the quad-double chain at D 100-200, from the measured laws: the jet's order-1 error
e_1 (exp_multi.json: 2-norm, the chain's form 0) against its envelope eps_dd G |dF/dD|; |dF/dD| and the double-double
fix pass's contraction c_dd fitted against D; the corrector's |F| basin 1.1e-14 (2-norm, chain logs D 85-86.5). Quad-double
scales every rounding term by u_qd / u_dd = 2^-103 (2^-209 against 2^-106). G = 0.7^-(D - 3).
    python d200_estimate.py exp_multi.json"""
import json, sys
import numpy as np
R = json.load(open(sys.argv[1]))
D = np.array([r["D"] for r in R])
G = lambda x: 0.7 ** (-(np.asarray(x) - 3.0))
FD = np.array([r["FD_max"] for r in R]); e1 = np.array([r["e1_2_a0"] for r in R]); cdd = np.array([r["c_dd"] for r in R])
k_env = e1 / (2.0 ** -106 * G(D) * FD)
bF = np.polyfit(D, np.log10(FD), 1); bc = np.polyfit(D, np.log10(cdd), 1); be = np.polyfit(D, np.log10(e1), 1)
print(f"bases D {D.min():.2f}-{D.max():.2f} ({len(D)}): |dF/dD| grows {10 ** bF[0]:.3f}x per unit D; e_1 {10 ** be[0]:.3f}x (rms "
      f"{np.sqrt(np.mean((np.log10(e1) - np.polyval(be, D)) ** 2)):.2f} decades); c_dd {10 ** bc[0]:.3f}x; e_1 / (eps_dd G |dF/dD|) "
      f"{k_env.min():.2f}-{k_env.max():.2f}")
ratio = 2.0 ** -103
basin = 1.1e-14
kmax = k_env.max()
print(" D    G         |dF/dD|   e_1 dd     e_1 qd     h(order 1) qd   c_dd       c_qd")
for x in (86.5, 100, 125, 150, 175, 200):
    Fx = 10 ** np.polyval(bF, x)
    e_dd = kmax * 2.0 ** -106 * G(x) * Fx
    e_qd = e_dd * ratio
    c = 10 ** np.polyval(bc, x)
    print(f"{x:5.1f} {G(x):.2e} {Fx:.2e} {e_dd:.2e} {e_qd:.2e} {basin / e_qd:10.3g}     {c:.2e} {c * ratio:.2e}")
# where the quad-double quantities reach their limits
xs = np.linspace(86.5, 260, 17351)
eq = kmax * 2.0 ** -106 * G(xs) * 10 ** np.polyval(bF, xs) * ratio
cq = 10 ** np.polyval(bc, xs) * ratio
for h in (10.0, 1.0, 0.1):
    i = np.argmax(eq * h > basin)
    print(f"quad-double jets: order-1 error times h = {h} reaches the basin at D {xs[i]:.0f}")
for c in (0.01, 0.1, 1.0):
    i = np.argmax(cq > c)
    print(f"quad-double Jacobian (corrector, fix passes): contraction {c} at D {xs[i]:.0f}")
