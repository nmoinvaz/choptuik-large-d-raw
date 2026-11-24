"""outward blocks only: per segment, the lam-change of ln|det Phi_b| against the Liouville trace integral, on the plan
with the given hmax (and tol)"""
import sys, time
import numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a984952191346adc9/hp")
import mode_matched as MM
from hpkernel.driver import load

path, hmax, tol, sub = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
lams = [float(v) for v in sys.argv[5:]]
zh, zl, meta = load(path)
M, K = meta["M"], len(meta["nodes"])
n4 = 4 * M
so = MM.make(meta, 2)
segs = so.plan(zh, zl, tol, hmax)
so.set_segs(segs)
print("steps", [len(g) - 1 for g in segs], sum(len(g) - 1 for g in segs), "|F|", MM.residual_max(so, zh, zl), flush=True)
rows = MM.trace_integrals(so, zh, zl, meta, segs, sub, log=lambda s: None)
col = lambda i: 2 * M + n4 * i
res = {}
for lam in lams:
    t = time.time()
    Mh, Ml = so.mode_matrix(zh, zl, lam, 0.0)
    A = np.asarray(Mh) + np.asarray(Ml)
    del Mh, Ml
    lds, svr = [], []
    for b in range(1, K):
        T = A[b * n4:(b + 1) * n4, col(b - 1):col(b - 1) + n4]
        lds.append(np.linalg.slogdet(T)[1])
        sv = np.linalg.svd(T, compute_uv=False)
        svr.append((sv.max(), sv.min()))
    sg, ld = np.linalg.slogdet(A)
    res[lam] = (lds, svr)
    print(f"lam {lam}: full f64 slogdet {sg:+.0f} {ld:.9f} ({time.time() - t:.0f} s)", flush=True)
    del A
l1, l2 = lams
print("b  steps  trace*(l1-l2)  dlnPhi  diff  sv(l1) max..min", flush=True)
for b in range(1, K):
    I = rows[b - 1]["Tp_sum"] - rows[b - 1]["Tm_sum"]
    d = res[l1][0][b - 1] - res[l2][0][b - 1]
    smax, smin = res[l1][1][b - 1]
    print(f"{b:2d} {len(segs[b - 1]) - 1:5d} {I * (l1 - l2):14.6f} {d:14.6f} {d - I * (l1 - l2):+.2e}  {smax:.2e}..{smin:.2e}",
          flush=True)
