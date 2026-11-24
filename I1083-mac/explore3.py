"""the matched layout: segments past match_node integrated inward; residual, blocks, equilibrated pivots, mode_det"""
import sys, time
import numpy as np
sys.path.insert(0, "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/mh")
from common import *
import mode_scale as MS

key = sys.argv[1]
mn = int(sys.argv[2])
full = sys.argv[3] == "full"
lams = [float(v) for v in sys.argv[4:]]
zh, zl, meta = load_state(key)
M = meta["M"]; nodes = meta["nodes"]; K = len(nodes)
s = solver(meta, match_node=mn)
segs = s.plan(zh, zl, 1e-32, 0.05)
print("match_node", mn, "steps", [len(g) - 1 for g in segs], "total", sum(len(g) - 1 for g in segs),
      "first/last of seg", [(round(g[0], 6), round(g[-1], 6)) for g in segs[mn - 1:mn + 2]], flush=True)
s.set_segs(segs)
fh, fl = s.residual(zh, zl)
F = np.abs(np.asarray(fh) + np.asarray(fl))
print("|F|", F.max(), "at", int(F.argmax()), flush=True)
n4 = 4 * M
for lam in lams:
    t = time.time()
    if full:
        Mh, Ml = s.mode_matrix(zh, zl, lam, 0.0)
        Mh, Ml = np.asarray(Mh), np.asarray(Ml)
        print(f"lam {lam}: mode_matrix {Mh.shape} in {time.time() - t:.1f} s", flush=True)
        A = Mh + Ml
        col = lambda i: 2 * M + n4 * i
        I = np.eye(n4)
        for r in range(1, K):
            rows = slice(r * n4, (r + 1) * n4)
            if r <= mn:
                T = A[rows, col(r - 1):col(r - 1) + n4]; E = A[rows, col(r):col(r) + n4]; tag = "out"
            else:
                T = A[rows, col(r):col(r) + n4]; E = A[rows, col(r - 1):col(r - 1) + n4]; tag = "in"
            sv = np.linalg.svd(T, compute_uv=False)
            print(f"  row {r:2d} ({tag}) [{nodes[r-1]},{nodes[r]}]: -I check {np.abs(E + I).max():.1e}; transfer sv "
                  f"{sv.max():.3e}..{sv.min():.3e} ratio {sv.min() / sv.max():.1e}; ln det {np.sum(np.log(sv)):.6f}", flush=True)
        d = MS.scaled_det(Mh, Ml, small=12)
        print(f"  equilibrated f64: sign {d['sign']:+.0f} ln {d['ln']:.6f} pmin {d['pmin']:.2e} pmax {d['pmax']:.2e} "
              f"(unscaled ratio {d['ratio_unscaled']:.1e}); smallest {[(i, f'{v:.1e}') for i, v in d['small']]}", flush=True)
        del A, Mh, Ml
    t = time.time()
    sg, la, pmin, pmax = s.mode_det(zh, zl, lam, 0.0)
    print(f"  lam {lam!r} kernel mode_det: sign {sg:+.0f} ln {la:.9f} pivots {pmin:.2e}..{pmax:.2e} ({time.time() - t:.1f} s)",
          flush=True)
