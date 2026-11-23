"""#1079 macm3b: a read-only probe of hier.py's own residual at an excited zero (my script; it imports main's hier and changes nothing).
For the starting point x = (A, w/w_inf, B3, C3): the raw residual r(x) (M = 3, xi 0.2), its 4 x 4 finite-difference Jacobian with hier's own steps (level 1: 1e-4 in A and w/w_inf; level 3: 1e-6 max(|b|, 1e-3 |A|)),
the linear Newton step dx = -J^-1 r, and the noise: r at x repeated with the steps' halves, to see how the finite-difference columns move.
    python -u hier_probe.py A wf B3 C3"""
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-1079/solver/inner_stokes")
import numpy as np
import hier as H

def main():
    A, wf, B3, C3 = (float(t) for t in sys.argv[1:5])
    x = np.array([A, wf, B3, C3])
    h = H.Hier(3, 0.2, top=1, verbose=0)
    r0 = h.res_raw(x)
    print("x      ", [repr(float(t)) for t in x])
    print("r(x)   ", [float(t) for t in r0], " |r_1| %.3e |r_3| %.3e" % (np.hypot(r0[0], r0[1]), np.hypot(r0[2], r0[3])))
    steps = np.array([1e-4, 1e-4] + [1e-6 * max(abs(x[k]), 1e-3 * abs(x[0])) for k in (2, 3)])
    for scale in (1.0, 0.5):
        J = np.zeros((4, 4))
        for k in range(4):
            xp = x.copy(); xp[k] += steps[k] * scale
            J[:, k] = (h.res_raw(xp) - r0) / (steps[k] * scale)
        dx = -np.linalg.solve(J, r0)
        print("FD steps x%.1f: J rows (r_1re, r_1im, r_3re, r_3im) by (A, wf, B3, C3):" % scale)
        for i in range(4):
            print("    " + "  ".join("%11.3e" % J[i, j] for j in range(4)))
        print("   cond(J) %.2e; Newton step dx = -J^-1 r: " % np.linalg.cond(J) + ", ".join("%+.3e" % t for t in dx))
main()
