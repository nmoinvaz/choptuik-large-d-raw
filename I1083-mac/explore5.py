"""per segment: ln|det Phi_b| (outward blocks) and ln|det Psi_b| (matched, inward blocks) at two lam, from the full
mode matrices, against the Liouville trace integral of the segment"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a984952191346adc9/hp")
import mode_matched as MM
from hpkernel.driver import load

path, m, sub = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
lams = [float(v) for v in sys.argv[4:]]
zh, zl, meta = load(path)
M, K = meta["M"], len(meta["nodes"])
n4 = 4 * M
so = MM.make(meta, 2)
segs = MM.planned(so, zh, zl, 0.05)
sm = MM.make(meta, 2, match_node=m)
MM.planned(sm, zh, zl, 0.05)
rows = MM.trace_integrals(so, zh, zl, meta, segs, sub, log=lambda s: None)
col = lambda i: 2 * M + n4 * i
res = {}
for lam in lams:
    for tag, s in (("out", so), ("m", sm)):
        t = time.time()
        Mh, Ml = s.mode_matrix(zh, zl, lam, 0.0)
        A = np.asarray(Mh) + np.asarray(Ml)
        del Mh, Ml
        lds = []
        for b in range(1, K):
            r = slice(b * n4, (b + 1) * n4)
            inward = tag == "m" and b > m
            T = A[r, col(b):col(b) + n4] if inward else A[r, col(b - 1):col(b - 1) + n4]
            sg, ld = np.linalg.slogdet(T)
            lds.append(ld)
        sg, ld = np.linalg.slogdet(A)
        res[(tag, lam)] = (lds, ld)
        print(f"lam {lam} {tag}: full f64 slogdet {sg:+.0f} {ld:.6f} ({time.time() - t:.0f} s)", flush=True)
        del A
l1, l2 = lams
print("b  trace_lam_part(I_b*(l1-l2))  dlnPhi_out  -dlnPsi_m(b>m)", flush=True)
for b in range(1, K):
    I = rows[b - 1]["Tp_sum"] - rows[b - 1]["Tm_sum"]
    d_out = res[("out", l1)][0][b - 1] - res[("out", l2)][0][b - 1]
    d_m = -(res[("m", l1)][0][b - 1] - res[("m", l2)][0][b - 1]) if b > m else float("nan")
    print(f"{b:2d} {I * (l1 - l2):14.6f} {d_out:14.6f} {d_m:14.6f}", flush=True)
