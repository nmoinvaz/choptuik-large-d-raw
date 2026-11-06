"""at a converged state: one polish step from the dd-rounded horizon data (d1), then the computed step x against the
exact one (truth - d1); R at d1 + exact and d1 + x; the normalization of d1's parts"""
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np, mpmath as mp
from hpkernel.driver import load_q
from multidouble import QDLu, qd_axpy
from reseed import Reseeder
z4, m = load_q(sys.argv[1])
rs = Reseeder(m, mp.mpf(m["D_str"]), threads=4, qd=True)
M, a, o = rs.M, rs.aoff, rs.off
s = rs.rung_solver(rs.us[-1]); rows = rs.rung_rows(); cols = np.r_[a["mh"]:a["mh"] + 2 * M]; L = a["L"]
n0, n1, nk = o["node"](0), o["node"](1), o["node"](rs.K - 1)
sl_ = slice(o["mh"], o["mh"] + 2 * M)
base = [np.zeros(L) for _ in range(4)]
for q in range(4):
    zq = np.asarray(z4[q], dtype=float)
    base[q][:2 * M] = zq[:2 * M]; base[q][a["node"](0):a["node"](1)] = zq[n0:n1]
    base[q][a["node"](1):a["node"](1) + 4 * M] = zq[nk:nk + 4 * M]; base[q][-1] = zq[-1]
def put(d):
    v = [b.copy() for b in base]
    for q in range(4):
        v[q][cols] = d[q]
    return tuple(np.ascontiguousarray(x) for x in v)
def res(d):
    F = s.residual_q(*put(d)); return [np.asarray(F[q])[rows] for q in range(4)]
def nr(R): return float(np.max(np.abs(R[0] + R[1])))
def lu_at(d):
    J = s.jacobian_q(*put(d)); return QDLu(*[np.asarray(J[q])[np.ix_(rows, cols)] for q in range(4)])
def add(x, d): return [np.ascontiguousarray(np.asarray(p)) for p in qd_axpy(1.0, *x, *d)]
def sub(x, y): return [np.ascontiguousarray(np.asarray(p)) for p in qd_axpy(-1.0, *y, *x)]
def mx(v): return float(np.max(np.abs(np.asarray(v[0]) + np.asarray(v[1]))))
truth = [np.ascontiguousarray(np.asarray(p)[sl_]) for p in z4]
d0 = [truth[0].copy(), truth[1].copy(), np.zeros(2 * M), np.zeros(2 * M)]
R0 = res(d0); lu = lu_at(d0)
x0 = [np.asarray(p) for p in lu.solve(*[-np.asarray(r) for r in R0])]
e0 = sub(truth, d0)
print(f"d0: |R| {nr(R0):.3e}; |x0| {mx(x0):.3e}, |truth - d0| {mx(e0):.3e}, |x0 - (truth - d0)| {mx(sub(x0, e0)):.3e}")
d1 = add(x0, d0); R1 = res(d1)
e1 = sub(truth, d1)
print(f"d1: |R| {nr(R1):.3e}; |truth - d1| {mx(e1):.3e} (relative {mx(e1) / np.max(np.abs(truth[0])):.1e})")
print(f"   R at d1 + (truth - d1): {nr(res(add(e1, d1))):.3e}")
lu1 = lu_at(d1)
x1 = [np.asarray(p) for p in lu1.solve(*[-np.asarray(r) for r in R1])]
print(f"   step at d1 (J at d1): |x1| {mx(x1):.3e}, |x1 - (truth - d1)| {mx(sub(x1, e1)):.3e}; R at d1 + x1 {nr(res(add(x1, d1))):.3e}")
x1b = [np.asarray(p) for p in lu.solve(*[-np.asarray(r) for r in R1])]
print(f"   step at d1 (J at d0): |x1| {mx(x1b):.3e}, |x1 - (truth - d1)| {mx(sub(x1b, e1)):.3e}; R at d1 + x1 {nr(res(add(x1b, d1))):.3e}")
# parts' normalization of d1: |p_{k+1}| <= ulp(p_k)
for k in range(3):
    p, q = np.abs(np.asarray(d1[k])), np.abs(np.asarray(d1[k + 1]))
    bad = int(np.sum(q > np.spacing(p) * 1.0001))
    print(f"   d1 parts {k}/{k + 1}: entries with |p{k + 1}| > ulp(p{k}): {bad} of {len(p)}")
# J's quality: J (d1 + h e_j) differences against the Jacobian column, for the column of the largest |e1|
j = int(np.argmax(np.abs(np.asarray(e1[0]) + np.asarray(e1[1]))))
print(f"   largest |truth - d1| at column {j} (of {2 * M}: m_h 0..{M - 1}, a_h {M}..{2 * M - 1}), value {float(e1[0][j] + e1[1][j]):.3e}, d {float(truth[0][j]):.3e}")
