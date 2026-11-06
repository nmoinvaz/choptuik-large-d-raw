"""at a converged state: the u0 rung block's quad-double Jacobian against the octo-double one, and the polish step from
the dd-rounded horizon data with each (QDLu, ODLu), against the exact step truth - d"""
import sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np, mpmath as mp
from hpkernel.driver import load_q
from multidouble import QDLu, ODLu, qd_axpy, od_axpy
from reseed import Reseeder
z4, m = load_q(sys.argv[1])
rs = Reseeder(m, mp.mpf(m["D_str"]), threads=4, qd=True)
M, a, o = rs.M, rs.aoff, rs.off
s = rs.rung_solver(rs.us[-1]); rows = rs.rung_rows(); cols = np.r_[a["mh"]:a["mh"] + 2 * M]; L = a["L"]
n0, n1, nk = o["node"](0), o["node"](1), o["node"](rs.K - 1)
sl_ = slice(o["mh"], o["mh"] + 2 * M)
base = [np.zeros(L) for _ in range(8)]
for q in range(4):
    zq = np.asarray(z4[q], dtype=float)
    base[q][:2 * M] = zq[:2 * M]; base[q][a["node"](0):a["node"](1)] = zq[n0:n1]
    base[q][a["node"](1):a["node"](1) + 4 * M] = zq[nk:nk + 4 * M]; base[q][-1] = zq[-1]
def put(d, P):
    v = [b.copy() for b in base[:P]]
    for q in range(P):
        v[q][cols] = d[q] if q < len(d) else 0.0
    return [np.ascontiguousarray(x) for x in v]
def mx(v): return float(np.max(np.abs(np.asarray(v[0]) + np.asarray(v[1]))))
truth = [np.ascontiguousarray(np.asarray(p)[sl_]) for p in z4] + [np.zeros(2 * M)] * 4
d0 = [truth[0].copy(), truth[1].copy()] + [np.zeros(2 * M)] * 6
Rq = lambda d: [np.asarray(F)[rows] for F in s.residual_q(*put(d, 4))]
Ro = lambda d: [np.asarray(F)[rows] for F in s.residual_o(put(d, 8))]
print(f"D {m['D_str'][:10]}: |R_q(d0)| {mx(Rq(d0)):.3e}, |R_o(d0)| {mx(Ro(d0)):.3e}, |R_q(truth)| {mx(Rq(truth)):.3e}, |R_o(truth)| {mx(Ro(truth)):.3e}", flush=True)
t0 = time.time(); Jq = s.jacobian_q(*put(d0, 4)); tq = time.time() - t0
t0 = time.time(); Jo, *_ = (s.jacobian_o(put(d0, 8)),); to = time.time() - t0
Jo = Jo[0] if isinstance(Jo, tuple) and len(Jo) == 2 and not hasattr(Jo[0], 'shape') else Jo
Bq = [np.asarray(J)[np.ix_(rows, cols)] for J in Jq]
Bo = [np.asarray(J)[np.ix_(rows, cols)] for J in Jo]
dif = [Bo[q] - Bq[q] for q in range(4)]
big = np.abs(Bo[0]); rel = np.abs(dif[0] + dif[1] + dif[2] + dif[3]) / np.maximum(big, 1e-300)
print(f"  jacobian_q {tq:.0f} s, jacobian_o {to:.0f} s; block |J| max {big.max():.2e} min nonzero {big[big > 0].min():.2e}; "
      f"relative |J_o - J_q| median {np.median(rel):.1e}, max {rel.max():.1e}", flush=True)
# the steps from d0
R0q, R0o = Rq(d0), Ro(d0)
xq = [np.asarray(p) for p in QDLu(*Bq).solve(*[-np.asarray(r) for r in R0q])] + [np.zeros(2 * M)] * 4
xo = [np.asarray(p) for p in ODLu(*Bo).solve(*[-np.asarray(r) for r in R0o])]
e0 = [np.asarray(p) for p in od_axpy(-1.0, *d0, *truth)]
dq = [np.asarray(p) for p in od_axpy(1.0, *xq, *d0)]
do = [np.asarray(p) for p in od_axpy(1.0, *xo, *d0)]
for name, x, d in (("QDLu step", xq, dq), ("ODLu step", xo, do)):
    err = [np.asarray(p) for p in od_axpy(-1.0, *e0, *x)]
    print(f"  {name}: |x| {mx(x):.3e}, |x - (truth - d0)| {mx(err):.3e}; |R_q| after {mx(Rq(d)):.3e}, |R_o| after {mx(Ro(d)):.3e}", flush=True)
