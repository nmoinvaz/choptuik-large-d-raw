"""the u0 rung residual (reseed.invert_q's rows) at a converged state's own four-part horizon data, at its dd rounding,
and with its node's parts 2-3 dropped"""
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np, mpmath as mp
from hpkernel.driver import load_q
from reseed import Reseeder
z4, m = load_q(sys.argv[1])
rs = Reseeder(m, mp.mpf(m["D_str"]), threads=4, qd=True)
M, a, o = rs.M, rs.aoff, rs.off
s = rs.rung_solver(rs.us[-1]); rows = rs.rung_rows(); cols = np.r_[a["mh"]:a["mh"] + 2 * M]; L = a["L"]
n0, n1, nk = o["node"](0), o["node"](1), o["node"](rs.K - 1)
sl_ = slice(o["mh"], o["mh"] + 2 * M)
def R(z, d):
    base = [np.zeros(L) for _ in range(4)]
    for q in range(4):
        zq = np.asarray(z[q], dtype=float)
        base[q][:2 * M] = zq[:2 * M]; base[q][a["node"](0):a["node"](1)] = zq[n0:n1]
        base[q][a["node"](1):a["node"](1) + 4 * M] = zq[nk:nk + 4 * M]; base[q][-1] = zq[-1]; base[q][cols] = d[q]
    F = s.residual_q(*[np.ascontiguousarray(b) for b in base])
    r = np.asarray(F[0])[rows] + np.asarray(F[1])[rows]
    return float(np.max(np.abs(r))), int(np.argmax(np.abs(r)))
truth = [np.asarray(p)[sl_] for p in z4]
z0 = np.zeros(2 * M)
print("rows", len(rows), "cols", len(cols), "u0", rs.us[-1], "x node", rs.nodes[-1])
print("truth data, 4 parts     ", R(z4, truth))
print("truth data, dd rounding ", R(z4, [truth[0], truth[1], z0, z0]))
print("node and all parts in dd", R([z4[0], z4[1], np.zeros_like(z4[0]), np.zeros_like(z4[0])], [truth[0], truth[1], z0, z0]))
print("max |z2|, |z3| of the state", float(np.max(np.abs(z4[2]))), float(np.max(np.abs(z4[3]))), "in the horizon data",
      float(np.max(np.abs(truth[2]))), float(np.max(np.abs(truth[3]))))
