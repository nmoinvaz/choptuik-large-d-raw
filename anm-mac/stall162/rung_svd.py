"""singular values of the u0 rung block (reseed's m and a rows against m_h, a_h) at a converged state, from the
quad-double Jacobian summed exactly into mpmath at 110 digits"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np, mpmath as mp
from hpkernel.driver import load_q
from reseed import Reseeder
mp.mp.dps = 110
z4, m = load_q(sys.argv[1])
rs = Reseeder(m, mp.mpf(m["D_str"]), threads=4, qd=True)
M, a, o = rs.M, rs.aoff, rs.off
s = rs.rung_solver(rs.us[-1]); rows = rs.rung_rows(); cols = np.r_[a["mh"]:a["mh"] + 2 * M]; L = a["L"]
n0, n1, nk = o["node"](0), o["node"](1), o["node"](rs.K - 1)
base = [np.zeros(L) for _ in range(4)]
for q in range(4):
    zq = np.asarray(z4[q], dtype=float)
    base[q][:2 * M] = zq[:2 * M]; base[q][a["node"](0):a["node"](1)] = zq[n0:n1]
    base[q][a["node"](1):a["node"](1) + 4 * M] = zq[nk:nk + 4 * M]; base[q][-1] = zq[-1]
    base[q][cols] = zq[o["mh"]:o["mh"] + 2 * M]
J = s.jacobian_q(*[np.ascontiguousarray(b) for b in base])
B = [np.asarray(x)[np.ix_(rows, cols)] for x in J]
n = len(rows)
A = mp.matrix(n, n)
for i in range(n):
    for j in range(n):
        A[i, j] = mp.mpf(float(B[0][i, j])) + mp.mpf(float(B[1][i, j])) + mp.mpf(float(B[2][i, j])) + mp.mpf(float(B[3][i, j]))
t0 = time.time()
S = mp.svd_r(A, compute_uv=False)
sv = sorted([S[i] for i in range(n)], reverse=True)
G = float(m["nodes"][-1]) ** -(float(m["D"]) - 3.0)
print(f"D {m['D_str'][:10]}: G {G:.2e}; sigma max {mp.nstr(sv[0], 3)}, then " + ", ".join(mp.nstr(x, 2) for x in sv[1:4])
      + " ... smallest " + ", ".join(mp.nstr(x, 2) for x in sv[-6:]) + f"; cond {mp.nstr(sv[0] / sv[-1], 3)}; {time.time() - t0:.0f} s", flush=True)
gaps = [float(sv[i] / sv[i + 1]) for i in range(n - 1)]
k = int(np.argmax(gaps))
print(f"  largest gap: sigma_{k + 1}/sigma_{k + 2} = {gaps[k]:.2e}, so {n - 1 - k} value(s) below it", flush=True)
