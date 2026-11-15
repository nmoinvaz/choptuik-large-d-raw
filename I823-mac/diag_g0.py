#!/usr/bin/env python3
"""#823's diagnostic of curve's g(0) at s0_D252's truth, after curve_truth stopped there. With reduced_cubic's own
Real system and basis: (1) the chord of ray_solve at c = 0 from w0 through z0's LU, step by step (|w|, max|F|,
max|strong residual|, |dw|, |g| = |U^T F|), without ray_solve's stops; (2) newton_strong at c = 0 from w0 (the LU
refactored at the iterate, #698), its steps, |g| and error estimate. Diagnostic only: nothing is judged.
usage (from hp/): python3 diag_g0.py RAW DZ0 BASE [--threads=3] [--chord=12]"""
import os
import sys
import time

sys.path.insert(0, os.getcwd())
import reduced_cubic as rc         # noqa: E402  (from hp/, after the path)
from reduced_cubic import mp       # noqa: E402


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in argv if a.startswith("--") and "=" in a)

    def log(s):
        print(s, flush=True)
    sysm = rc.Real(*args[:3], int(opts.get("threads", 3)), log, fast=True)
    bas = rc.basis(sysm, {}, log, {}, lambda: None)
    X, Um, w0, nBa, k = bas["X"], bas["Um"], bas["w0"], bas["nBa"], bas["k"]
    F0 = bas["F0"]
    log(f"  at z0: |U^T F| {mp.nstr(rc.nrm(bas['gF0']), 4)}, |B a| {mp.nstr(nBa, 4)}, max|F| {mp.nstr(rc.amax(F0), 4)}, "
        f"max|strong part| {mp.nstr(rc.amax(rc.strong_part(Um, F0)), 4)}, |w0| {mp.nstr(rc.nrm(w0), 4)}")
    w = list(w0)
    t0 = time.time()
    for i in range(int(opts.get("chord", 12))):
        Fv = sysm.F(w)
        r = rc.strong_part(Um, Fv)
        dw = sysm.solve(r)
        nd = rc.nrm(dw)
        log(f"  chord {i}: |w| {mp.nstr(rc.nrm(w), 4)}, max|F| {mp.nstr(rc.amax(Fv), 4)}, max|strong r| "
            f"{mp.nstr(rc.amax(r), 4)}, |dw| {mp.nstr(nd, 4)}, |g| {mp.nstr(rc.nrm(rc.proj_U(Um, Fv)), 4)} "
            f"({time.time() - t0:.0f} s)")
        if not mp.isfinite(nd):
            break
        w = [x - y for x, y in zip(w, dw)]
    t0 = time.time()
    gv, wv, Fv, hv, ok, err, nlu = rc.newton_strong(sysm, X, Um, [mp.mpf(0)] * k, w0,
                                                    max(rc.nrm(w0), mp.mpf("1e-300")), nBa)
    log(f"  newton_strong at c = 0: converged {ok} (error estimate below 1e-20 |B a|), error estimate "
        f"{'none' if err is None else mp.nstr(err, 4)}, |g| {mp.nstr(rc.nrm(gv), 4)}, |w| {mp.nstr(rc.nrm(wv), 4)}, "
        f"max|F| {mp.nstr(rc.amax(Fv), 4)}, {nlu} LUs ({time.time() - t0:.0f} s)")
    log("    (LU, max|strong r|, |dw|): " + ", ".join(f"({h[0]}, {h[1]:.3e}, {h[2]:.3e})" for h in hv))
    log("  g = " + ", ".join(mp.nstr(x, 6) for x in gv))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
