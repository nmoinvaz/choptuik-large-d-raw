#!/usr/bin/env python3
"""#954, AD HOC (labelled): jet_by_order_check.py's own sequence at a stored state on one build, with the detail of the words that differ. As the check does: newton_o; the series to N by jets and by order
(no hook); then, with the planted hook given to both, the series to Np by jets and by order. For each of those series and order k: the 64-bit words that differ between the two forms, how many of the
differing words are non-finite in either form, and the first three differing words as hex; and the number of non-finite words per form. Run from a build's hp/ (PYTHONPATH there):
    python3 jbo_nan954.py RAW STATE.npz [--threads 8] [--N 6] [--Np 6]"""
import os
import sys

sys.path.insert(0, os.getcwd())
import numpy as np  # noqa: E402

raw, state = sys.argv[1], sys.argv[2]
opt = dict(threads=8, N=6, Np=6)
for k in opt:
    if "--" + k in sys.argv:
        opt[k] = int(sys.argv[sys.argv.index("--" + k) + 1])
from anm_run import coefficients_o  # noqa: E402
from jet_by_order_check import planted  # noqa: E402
from octo_corrector import truth_system  # noqa: E402

z, meta, (s, _, _, _), info = truth_system(raw, state, threads=opt["threads"])
zo = [np.ascontiguousarray(np.asarray(p)) for p in z]
print(f"jbo_nan954 {state}: D {meta.get('D_str', meta.get('D'))!s:.18}, {info['plan']} plan, {opt}, hpkernel {__import__('hpkernel').__file__}", flush=True)
s.newton_o(list(zo))
A, _ = coefficients_o(s, zo, opt["N"])
B, _ = coefficients_o(s, zo, opt["N"], by_order=True)
Ap, _ = coefficients_o(s, zo, opt["Np"], perturb=planted)
Bp, _ = coefficients_o(s, zo, opt["Np"], perturb=planted, by_order=True)


def report(name, X, Y):
    print(f"-- {name}", flush=True)
    for k in range(1, min(len(X), len(Y))):
        xs = np.concatenate([np.asarray(p, dtype=np.float64).ravel() for p in X[k]])
        ys = np.concatenate([np.asarray(p, dtype=np.float64).ravel() for p in Y[k]])
        xu, yu = xs.view(np.uint64), ys.view(np.uint64)
        d = np.nonzero(xu != yu)[0]
        nf = int((~np.isfinite(xs[d]) | ~np.isfinite(ys[d])).sum()) if len(d) else 0
        first = ", ".join(f"{int(xu[i]):016x}/{int(yu[i]):016x}" for i in d[:3])
        print(f"  order {k}: non-finite words jets {int((~np.isfinite(xs)).sum())}, by order {int((~np.isfinite(ys)).sum())} of {xs.size}; "
              f"words differing {len(d)}, of them non-finite {nf}" + (f"; first: {first}" if len(d) else ""), flush=True)


report(f"no hook, N {opt['N']}", A, B)
report(f"planted hook given to both, Np {opt['Np']}", Ap, Bp)
