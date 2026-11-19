import os, sys
import numpy as np
SRC = sys.argv[1]
os.environ["HIER_NB_H5"] = sys.argv[2]
sys.path.insert(0, SRC)
import hier_nb as HN, hier as H
x = np.array([2.719219, 1.000022, 0.148977988, 0.014770713, 0.008424206, 0.001511189, 0.000474205, 0.00012168, 2.6602985034854245e-05, 8.947854197796251e-06])
h = HN.LazyHier(9, 0.15, top=99, verbose=0)
want = float(sys.argv[3])
ok = True
for l in (3, 5, 7, 9):
    d = 1e-6 * np.maximum(np.abs(x[H.idx(l)]), 1e-3 * np.abs(x[0]))
    r = h.h(l, x) / d
    w = want if l == 5 else 1.0
    ok = ok and np.allclose(r, w, rtol=1e-12)
    print(f"HIER_NB_H5={sys.argv[2]} level {l}: {r} x the default (want {w})")
sys.exit(0 if ok else 1)
