"""Is sign(det M) resolved? det(Q M) = det(Q) det(M) exactly for orthogonal Q, so in exact arithmetic the sign from an LU
of Q M, times sign(det Q), equals the sign from an LU of M. Rounding-floor singular values make it disagree.
usage (from solver/matter of a choptuik-large-d worktree, which supplies dss_ell):
  signtest.py planted
  signtest.py STATE D kc lam1,lam2,...
  signtest.py STATE D kc around=RECORDS.jsonl:D:dl [dry]   (the record's lam at D, minus and plus dl; dry prints them)"""
import os, sys, time, json, numpy as np


def signs(M, nq=3, seed=11):
    g = np.random.default_rng(seed)
    s0, l0 = np.linalg.slogdet(M)
    out = [float(s0)]
    for _ in range(nq):
        Q = np.linalg.qr(g.standard_normal(M.shape))[0]
        sq = np.linalg.slogdet(Q)[0]
        out.append(float(np.linalg.slogdet(Q @ M)[0] * sq))
    return out, float(l0)


if sys.argv[1] == "planted":
    g = np.random.default_rng(3)
    n = 600
    U = np.linalg.qr(g.standard_normal((n, n)))[0]; V = np.linalg.qr(g.standard_normal((n, n)))[0]
    for floor, k in ((1.0, 0), (1e-13, 40), (1e-19, 40)):
        s = np.exp(g.uniform(-1, 1, n)); s[:k] = floor * g.uniform(0.5, 2, k)
        sg, la = signs(U @ np.diag(s) @ V.T, nq=5)
        print(f"planted: {k} singular values at {floor:.0e} of 1: signs {sg} -> {'agree' if len(set(sg)) == 1 else 'DISAGREE'}")
    sys.exit(0)
sys.path.insert(0, os.getcwd())
st, D, kc = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
if sys.argv[4].startswith("around="):
    fn, Dr, dl = sys.argv[4][7:].rsplit(":", 2)
    lam = [json.loads(q)["lam"] for q in open(fn) if json.loads(q)["D"] == float(Dr) and json.loads(q).get("lam")][-1]
    lams = [lam - float(dl), lam + float(dl)]
else:
    lams = [float(v) for v in sys.argv[4].split(",")]
print(f"signtest: {st} D {D} k_c {kc} at lam {lams}", flush=True)
if "dry" in sys.argv[5:]:
    sys.exit(0)
from dss_ell import DSSEll, NODES_STD
z = np.load(st)
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=30, u0=0.04)
S.freeze_from(z, 0.7)
for l in lams:
    t = time.time()
    with np.errstate(all="ignore"):
        M = S.mode_matrix(z, l)
    sv = np.linalg.svd(M, compute_uv=False)
    sg, la = signs(M)
    print(json.dumps(dict(state=st.split("/")[-1], D=D, kc=kc, lam=l, signs=sg, agree=len(set(sg)) == 1, logabs=la,
                          n_below_1e_12=int(np.sum(sv < 1e-12 * sv[0])), n_below_1e_15=int(np.sum(sv < 1e-15 * sv[0])),
                          smallest=[float(v / sv[0]) for v in sv[-3:]], sec=round(time.time() - t, 1))), flush=True)
