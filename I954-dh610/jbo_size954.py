#!/usr/bin/env python3
"""#954, AD HOC (a labelled copy of the planted-change row of hp/jet_by_order_check.py that prints the size of the difference): at a stored state, the series z_1..z_Np by jets of growing
length (coefficients_o, by_order=False) and one order at a time (by_order=True), both with jet_by_order_check's planted change (its `planted` hook), and per order k
    max_i |z_jets_i - z_byorder_i| / max_i |z_jets_i|    over the eight-part sums of each entry (mpmath at 140 digits, exact for eight doubles),
plus the number of 64-bit words that differ. Run from a build's hp/ (PYTHONPATH there):
    python3 jbo_size954.py RAW STATE.npz [--threads 8] [--Np 6]"""
import os
import sys
import time

sys.path.insert(0, os.getcwd())
import numpy as np  # noqa: E402
from mpmath import mp, mpf  # noqa: E402

mp.dps = 140
raw, state = sys.argv[1], sys.argv[2]
threads = int(sys.argv[sys.argv.index("--threads") + 1]) if "--threads" in sys.argv else 8
Np = int(sys.argv[sys.argv.index("--Np") + 1]) if "--Np" in sys.argv else 6
from anm_run import coefficients_o  # noqa: E402
from jet_by_order_check import planted  # noqa: E402
from octo_corrector import truth_system  # noqa: E402

z, meta, (s, _, _, _), info = truth_system(raw, state, threads=threads)
zo = [np.ascontiguousarray(np.asarray(p)) for p in z]
print(f"jbo_size954 {state}: D {meta.get('D_str', meta.get('D'))!s:.18}, {info['plan']} plan, Np {Np}, {threads} threads, hpkernel {__import__('hpkernel').__file__}", flush=True)
t0 = time.time()
s.newton_o(list(zo))
print(f"  newton_o {time.time() - t0:.1f} s", flush=True)
t0 = time.time()
Ap, _ = coefficients_o(s, zo, Np, perturb=planted)
t1 = time.time()
Bp, _ = coefficients_o(s, zo, Np, perturb=planted, by_order=True)
print(f"  jets {t1 - t0:.1f} s, by order {time.time() - t1:.1f} s", flush=True)
print("  order  max|z|          max|z_jets - z_byorder| / max|z|   words differing (of 8 x entries)")
for k in range(1, Np + 1):
    n = len(Ap[k][0])
    maxd = mpf(0)
    maxz = mpf(0)
    for i in range(n):
        a = sum((mpf(float(Ap[k][q][i])) for q in range(8)), mpf(0))
        b = sum((mpf(float(Bp[k][q][i])) for q in range(8)), mpf(0))
        maxd = max(maxd, abs(a - b))
        maxz = max(maxz, abs(a))
    nd = sum(int((np.asarray(p).view(np.uint64) != np.asarray(q).view(np.uint64)).sum()) for p, q in zip(Ap[k], Bp[k]))
    rel = maxd / maxz if maxz else mpf(0)
    print(f"  {k:5d}  {mp.nstr(maxz, 5):14s}  {mp.nstr(rel, 6) if rel else '0':28s}  {nd} (of {8 * n})", flush=True)
