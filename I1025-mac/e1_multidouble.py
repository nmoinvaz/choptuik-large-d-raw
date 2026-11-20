import sys, os, json, time, math, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
import multidouble as md
import ddnp as dd
from ell_dd import lu_dd, bandwidths
from dss_ell import DSSEll, NODES_STD
out = "/Users/nathan/Source/choptuik-1025/solver/matter/data/ell_dd_e1md_1025.jsonl"
import mpmath as mp
mp.mp.dps = 60
g = np.random.default_rng(3)
n = 80
for i in range(n):
    for j in range(max(0, i - 6), min(n, i + 6)):
        g.standard_normal()
n = 100
Q1, Q2 = (np.linalg.qr(np.random.default_rng(11).standard_normal((n, n)))[0] for _ in range(2))
sig = np.concatenate([np.logspace(0, -6, n - 20), np.logspace(-14, -26, 20)])
B = (Q1 * sig) @ Q2.T
ex = 1.0 if mp.det(mp.matrix(B.tolist())) > 0 else -1.0
z = np.zeros_like(B)
sd = md.dd_logdet(B, z, True)[0]; sq = md.qd_logdet(B, z, z, z, True)[0]; sf = np.linalg.slogdet(B)[0]
print(f"planted ladder: exact {ex:+.0f}; dd_logdet {sd:+.0f}, qd_logdet {sq:+.0f}, LAPACK {sf:+.0f}: {'OK' if sd == ex and sq == ex else 'BAD'}", flush=True)
cases = [("data/sol_l1kc31L1025_D13.0000.npy", 13.0, 31, [2.6641484641099442, 2.7041484641099442]),
         ("data/sol_l1kc55Fs1025_D17.5000.npy", 17.5, 55, [1.93, 1.97, 1.935, 1.945, 1.9505, 1.9515, 1.955, 1.965])]
os.chdir("/Users/nathan/Source/choptuik-1025/solver/matter")
for st, D, kc, lams in cases:
    zz = np.load(st)
    S = DSSEll(kc=kc, nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=zz[-1], Ks=30, u0=0.04); S.freeze_from(zz, 0.7)
    for lam in lams:
        with np.errstate(all="ignore"):
            M = S.mode_matrix(zz, lam)
        t0 = time.time(); sdd, ldd, umin, umax = md.dd_logdet(M, np.zeros_like(M), True); t1 = time.time()
        lb, ub = bandwidths(M); s2, l2 = lu_dd(dd.R(M.copy()), lb, ub); t2 = time.time()
        rec = dict(D=D, kc=kc, lam=lam, dd_logdet=[sdd, ldd, umin, umax], lu_dd=[s2, l2], sec=[round(t1 - t0, 1), round(t2 - t1, 1)])
        rec["agree"] = bool(sdd == s2 and abs(ldd - l2) <= 1e-9)
        if D == 17.5 and lam in (1.9505, 1.9515):
            t3 = time.time(); z0 = np.zeros_like(M); sq, lq, _, _ = md.qd_logdet(M, z0, z0, z0, True)
            rec["qd_logdet"] = [sq, lq, round(time.time() - t3, 1)]
            rec["agree"] = rec["agree"] and sq == sdd
        print(f"D {D} k_c {kc} lam {lam}: dd_logdet {sdd:+.0f} {ldd:.10f} (min|u| {umin:.1e}, {rec['sec'][0]} s); lu_dd {s2:+.0f} {l2:.10f} ({rec['sec'][1]} s)"
              + (f"; qd_logdet {rec['qd_logdet'][0]:+.0f} {rec['qd_logdet'][1]:.10f} ({rec['qd_logdet'][2]} s)" if 'qd_logdet' in rec else "")
              + f": {'agree' if rec['agree'] else 'DISAGREE'}", flush=True)
        open(out, "a").write(json.dumps(rec) + "\n")
