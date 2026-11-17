#!/usr/bin/env python3
"""Scratch: the low-D Taylor series in D at one stored state (anm_lowd.coefficients), its partial sums against stored
converged states at other D (same M and nodes), with timings. Not a pilot; a measurement for the design (#927)."""
import json
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
HP = sys.argv[1]
sys.path.insert(0, HP)
import numpy as np  # noqa: E402
from anm_lowd import coefficients, evaluate, fmax, solver_for  # noqa: E402
from hpkernel.driver import load  # noqa: E402

base, refs, N, threads, out = sys.argv[2], sys.argv[3].split(","), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
jf = open(out, "a")
zh, zl, m = load(base)
D0 = float(m["D"])
t0 = time.time()
s = solver_for(m, D0, threads, m["segs"])
F0 = fmax(s, zh, zl)
t1 = time.time()
_, _, _, _, pmin, pmax = s.newton_mixed(zh, zl)
t2 = time.time()
print(f"base D {D0} M {m['M']} L {len(zh)} steps {sum(len(g) - 1 for g in m['segs'])}: |F| {F0:.2e} ({t1 - t0:.1f} s), "
      f"newton_mixed {t2 - t1:.1f} s, pivots {pmin:.2e}..{pmax:.2e}", flush=True)
rec = []
Zh, Zl = coefficients(s, zh, zl, N, rec, step_tol=1e-20)
norms = [float(np.abs(zh).max())] + [o["norm"] for o in rec]
dD = [abs(float(Zh[k][-1])) for k in range(N + 1)]
print("norms", " ".join(f"{v:.3e}" for v in norms))
print("ratios", " ".join(f"{norms[k - 1] / norms[k]:.4g}" for k in range(2, N + 1)))
print("Delta_k", " ".join(f"{v:.3e}" for v in dD))
jf.write(json.dumps(dict(stage="series", base=base, D=D0, M=m["M"], L=len(zh), F0=F0, t_newton_mixed=t2 - t1,
                         pivots=[pmin, pmax], orders=rec, delta_k=dD, threads=threads)) + "\n"); jf.flush()
for r in refs:
    ch, cl, mc = load(r)
    Dc = float(mc["D"]); h = Dc - D0
    rows = []
    for n in range(N + 1):
        ph, pl = evaluate(Zh[:n + 1], Zl[:n + 1], h)
        e = float(np.abs((ph - ch) + (pl - cl)).max())
        dd = float((ph[-1] - ch[-1]) + (pl[-1] - cl[-1]))
        rows.append((n, e, dd))
    print(f"ref D {Dc} (h {h:+.4f}):")
    for n, e, dd in rows:
        print(f"  n {n:2d}: max|z - ref| {e:.3e}, Delta - ref {dd:+.3e}")
    jf.write(json.dumps(dict(stage="partial_sums", ref=r, D=Dc, h=h, rows=rows)) + "\n"); jf.flush()
print(f"done {time.time() - t0:.0f} s")
