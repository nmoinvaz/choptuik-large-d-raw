"""python rung_fix_run.py HP_DIR [anm_run.py arguments]: anm_run.py with Reseeder.invert_q replaced: the u0 rung's quad-double polish refactors its Jacobian when a step does
not halve the residual (at most REFACTOR_MAX times) instead of stopping there. Prints every iterate."""
import os, runpy, sys, time
HP = os.path.abspath(sys.argv.pop(1))   # the hp directory of the checkout
sys.path.insert(0, HP)
import numpy as np
import reseed
from multidouble import QDLu, qd_axpy

REFACTOR_MAX = int(os.environ.get("REFACTOR_MAX", "3"))


def invert_q(self, z4, d4, it_max=12):
    M, a, o = self.M, self.aoff, self.off
    u = self.us[-1]
    s = self.rung_solver(u)
    rows = self.rung_rows()
    cols = np.r_[a["mh"]:a["mh"] + 2 * M]
    L = a["L"]
    base = [np.zeros(L) for _ in range(4)]
    n0, n1 = o["node"](0), o["node"](1)
    nk = o["node"](self.K - 1)
    for q in range(4):
        zq = np.asarray(z4[q], dtype=float)
        base[q][:2 * M] = zq[:2 * M]
        base[q][a["node"](0):a["node"](1)] = zq[n0:n1]
        base[q][a["node"](1):a["node"](1) + 4 * M] = zq[nk:nk + 4 * M]
        base[q][-1] = zq[-1]

    def put(d):
        v = [b.copy() for b in base]
        for q in range(4):
            v[q][cols] = d[q]
        return tuple(np.ascontiguousarray(x) for x in v)

    def res(d):
        F = s.residual_q(*put(d))
        return [np.asarray(F[q])[rows] for q in range(4)]

    def factor(d):
        J = s.jacobian_q(*put(d))
        return QDLu(*[np.asarray(J[q])[np.ix_(rows, cols)] for q in range(4)])

    d = [np.ascontiguousarray(np.asarray(x, dtype=float)) for x in d4]
    R = res(d)
    nR = float(np.max(np.abs(R[0] + R[1])))
    hist = [dict(it=0, R=nR)]
    if not np.isfinite(nR):
        return d, hist, False
    t0 = time.time()
    lu, refactors, steps, trace = factor(d), 0, 0, [f"{nR:.2e}"]
    for it in range(it_max):
        x = lu.solve(*[-np.asarray(r) for r in R])
        dn = [np.ascontiguousarray(np.asarray(p)) for p in qd_axpy(1.0, *x, *d)]
        Rn = res(dn)
        nn = float(np.max(np.abs(Rn[0] + Rn[1])))
        hist.append(dict(it=it + 1, R=nn))
        lower = np.isfinite(nn) and nn < nR
        trace.append(f"{nn:.2e}" + ("" if lower else "x"))
        halving = lower and nn <= 0.5 * nR
        if lower:
            d, R, nR = dn, Rn, nn
            steps += 1
        if nR < 1e-40:
            break
        if not halving:
            if refactors >= REFACTOR_MAX:
                break
            lu = factor(d)
            refactors += 1
            trace.append("J")
    hist.append(dict(it=len(hist), R=nR))
    print(f"      invert_q (refactor on stall): {' '.join(trace)}; {refactors} refactors, {time.time() - t0:.0f} s, "
          f"{'converged' if steps > 0 and nR < 1e-24 else 'NOT converged'}", flush=True)
    return d, hist, steps > 0 and nR < 1e-24


reseed.Reseeder.invert_q = invert_q
sys.argv = [os.path.join(HP, "anm_run.py")] + sys.argv[1:]
os.chdir(HP)
runpy.run_path(os.path.join(HP, "anm_run.py"), run_name="__main__")
