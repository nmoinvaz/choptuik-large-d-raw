"""I190-macm3: do the kf 23, 25 and 27 caches differ from each other (a replay would not)? ln|det| and arg at the shared points, and the saved states.    python3 compare_K.py"""
import json, math, numpy as np
def load(K):
    d = {}
    for l in open(f"data_kf{K}/modecount_D45.0507_M48_kf{K}_circ_evals.jsonl"):
        r = json.loads(l); d[(r["re"], r["im"])] = r
    return d
c = {K: load(K) for K in (21, 23, 25, 27)}
for A, B in ((21, 23), (23, 25), (25, 27)):
    sh = sorted(set(c[A]) & set(c[B]))
    dl = [c[B][k]["lnabs"] - c[A][k]["lnabs"] for k in sh]
    da = [abs((c[B][k]["arg"] - c[A][k]["arg"] + math.pi) % (2 * math.pi) - math.pi) for k in sh]
    print(f"kf {B} vs kf {A}: {len(sh)} shared points, ln|det| diff {min(dl):.2f} to {max(dl):.2f}; |d arg| max {max(da):.2e} median {sorted(da)[len(da)//2]:.2e}")
S = {K: np.load(f"data_kf{K}/modecount_state_D45.0507_M48_kf{K}.npz", allow_pickle=True) for K in (21, 23, 25, 27)}
Z = {K: S[K]["zh"] + S[K]["zl"] for K in S}
for A, B in ((21, 23), (23, 25), (25, 27)):
    print(f"max |z_kf{B} - z_kf{A}| = {np.abs(Z[B] - Z[A]).max():.2e}")
