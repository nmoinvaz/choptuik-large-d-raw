"""signtest_q.py: signtest.py (blob 179ea096, frozen because the finished low-D drivers pin it) plus --nq=N, the number of
random orthogonal Q (default 3, which reproduces signtest.py's output). The first 3 Q are the same at any N (same seed).
Is sign(det M) resolved? det(Q M) = det(Q) det(M) exactly for orthogonal Q, so in exact arithmetic the sign from an LU
of Q M, times sign(det Q), equals the sign from an LU of M. Rounding-floor singular values make it disagree.
usage (from solver/matter of a choptuik-large-d worktree, which supplies dss_ell):
  signtest.py planted
  signtest.py STATE D kc lam1,lam2,...
  signtest.py STATE D kc around=RECORDS.jsonl:D:dl [dry]   (the record's lam at D, minus and plus dl; dry prints them)
  either form takes --u0=U --Ks=K --kappa=k --rk=r (defaults 0.04, 30, 0.7, 1, the settings of most records); with around=
  it first checks that these rebuild the record's discrete system (|F| within 1% of the record's or 1e-13, the same step count) and
  exits 3 without signs if not; syscheck stops after that check"""
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
opt = dict(a[2:].split("=", 1) for a in sys.argv[5:] if a.startswith("--") and "=" in a)
Ks, u0 = int(opt.get("Ks", 30)), float(opt.get("u0", 0.04))     # the records' horizon series; pass the record's own
kappa, rk = float(opt.get("kappa", 0.7)), int(opt.get("rk", 1))  # the records' step rule; pass the record's own
S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=Ks, u0=u0, rk=rk)
steps = S.freeze_from(z, kappa)
if sys.argv[4].startswith("around="):            # is this the record's discrete system? its F (to 1%, or 1e-13 at rounding
    # level, where F is noise: D 6's 2.5e-15 record reads 2.8e-15 today) and its step count
    rec = [json.loads(q) for q in open(fn) if json.loads(q)["D"] == float(Dr) and json.loads(q).get("lam")][-1]
    with np.errstate(all="ignore"):
        F = float(np.linalg.norm(S.residual(z[None, :])[0]))
    ns = sum(steps.values())
    same = (rec.get("F") is None or abs(F - rec["F"]) <= max(1e-2 * rec["F"], 1e-13)) and (rec.get("steps") is None or ns == rec["steps"])
    print(json.dumps(dict(system_check=st.split("/")[-1], D=D, kc=kc, u0=u0, Ks=Ks, kappa=kappa, rk=rk, F=F, F_record=rec.get("F"),
                          steps=ns, steps_record=rec.get("steps"), same=same)), flush=True)
    if not same:
        print("signtest: NOT the record's discrete system (check --u0/--Ks/--kappa/--rk); no signs computed", flush=True)
        sys.exit(3)
    if "syscheck" in sys.argv[5:]:
        sys.exit(0)
for l in lams:
    t = time.time()
    with np.errstate(all="ignore"):
        M = S.mode_matrix(z, l)
    sv = np.linalg.svd(M, compute_uv=False)
    sg, la = signs(M, nq=int(opt.get("nq", 3)))
    print(json.dumps(dict(state=st.split("/")[-1], D=D, kc=kc, u0=u0, Ks=Ks, lam=l, signs=sg, agree=len(set(sg)) == 1, logabs=la,
                          n_below_1e_12=int(np.sum(sv < 1e-12 * sv[0])), n_below_1e_15=int(np.sum(sv < 1e-15 * sv[0])),
                          smallest=[float(v / sv[0]) for v in sv[-3:]], sec=round(time.time() - t, 1))), flush=True)
