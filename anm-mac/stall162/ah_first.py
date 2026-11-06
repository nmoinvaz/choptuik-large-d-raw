"""at a converged state, the u0 rung polish from the dd-rounded horizon data: plain Newton (QDLu) against a first step
in a_h alone (least squares in the a_h columns, normal equations in mpmath) followed by Newton steps"""
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np, mpmath as mp
from hpkernel.driver import load_q
from multidouble import QDLu, qd_axpy
from reseed import Reseeder
mp.mp.dps = 90
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
def res(d): F = s.residual_q(*put(d)); return [np.asarray(F[q])[rows] for q in range(4)]
def nr(R): return float(np.max(np.abs(R[0] + R[1])))
def add(x, d): return [np.ascontiguousarray(np.asarray(p)) for p in qd_axpy(1.0, *x, *d)]
def block(d): J = s.jacobian_q(*put(d)); return [np.asarray(x)[np.ix_(rows, cols)] for x in J]
def to_mp(parts):  # 4 part arrays -> mp vector / matrix
    return [sum(mp.mpf(float(p[i])) for p in parts) for i in range(len(parts[0]))]
def from_mp(v):  # mp vector -> 4 parts
    out = [np.zeros(len(v)) for _ in range(4)]
    for i, x in enumerate(v):
        r = x
        for q in range(4):
            f = float(r); out[q][i] = f; r = r - mp.mpf(f)
    return out
truth = [np.ascontiguousarray(np.asarray(p)[sl_]) for p in z4]
d0 = [truth[0].copy(), truth[1].copy(), np.zeros(2 * M), np.zeros(2 * M)]
print(f"D {m['D_str'][:10]}: |R(d0)| {nr(res(d0)):.3e}")
# plain Newton, 4 steps, refactoring each step
d = d0
tr = []
for it in range(4):
    R = res(d); B = block(d)
    x = [np.asarray(p) for p in QDLu(*B).solve(*[-np.asarray(r) for r in R])]
    d = add(x, d); tr.append(f"{nr(res(d)):.2e}")
print("  plain Newton:", " ".join(tr))
# a_h first: least squares in the a_h columns (M..2M-1 of the block), then Newton
d = d0
R = res(d); B = block(d)
A = mp.matrix([[sum(mp.mpf(float(B[q][i, j])) for q in range(4)) for j in range(M, 2 * M)] for i in range(len(rows))])
r = mp.matrix(to_mp(R))
xa = mp.lu_solve(A.T * A, -(A.T * r))
x = [np.zeros(2 * M) for _ in range(4)]
xa4 = from_mp([xa[i] for i in range(M)])
for q in range(4):
    x[q][M:] = xa4[q]
d = add(x, d); tr = [f"a_h step {nr(res(d)):.2e}"]
for it in range(4):
    R = res(d); B = block(d)
    xs = [np.asarray(p) for p in QDLu(*B).solve(*[-np.asarray(rr) for rr in R])]
    d = add(xs, d); tr.append(f"{nr(res(d)):.2e}")
print("  a_h first, then Newton:", " ".join(tr))
