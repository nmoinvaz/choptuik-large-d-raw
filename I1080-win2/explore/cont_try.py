"""scratch feasibility: fixed-(A, w) hier solves along the straight path x1 -> x2, each from the previous solution"""
import sys, os, time, json
import numpy as np
sys.path.insert(0, "D:/choptuik-i1080main/solver/inner_stokes")
import hier_nb  # noqa  (installs numba, LazyHier)
import hier as H

M = int(sys.argv[1]); n = int(sys.argv[2]); fm = float(sys.argv[3])
P0 = np.array([3.446218246366727, 0.347606965217407])
P1 = np.array([3.526473056695715, 0.211497981391215])
v = np.array([float(t) for t in sys.argv[4].split(",")])
prev = []
for i in range(n + 1):
    t = i / n
    p = P0 + t * (P1 - P0)
    vp = v if len(prev) < 2 else 2 * prev[-1] - prev[-2]
    x = np.concatenate([p, vp])
    h = H.Hier(M, 0.2, top=3, verbose=0)
    h.schur = True
    h.floor_max = fm
    t0 = time.time()
    xs, r = h.solve_from(3, x)
    rn = [float(np.hypot(r[k], r[k + 1])) for k in range(0, M + 1, 2)]
    v = xs[2:]
    prev.append(v.copy())
    print(json.dumps(dict(t=t, A=p[0], wf=p[1], r=rn, v=v.tolist(), s=round(time.time() - t0, 1))), flush=True)
