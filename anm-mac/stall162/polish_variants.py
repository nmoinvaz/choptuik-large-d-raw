"""the u0 rung's quad-double polish on a stored prediction, from the start the re-seed's double-double ladder hands it,
under several rules: the refactoring rule, the a_h step first, pure Newton (refactored, every step taken), and
alternating a_h / m_h least-squares steps before Newton"""
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np, mpmath as mp
from hpkernel.driver import load_q
from multidouble import QDLu, qd_axpy
import reseed as RS
z4, m = load_q(sys.argv[1])
rs = RS.Reseeder(m, mp.mpf(m["D_str"]), threads=4, qd=True)
cap = {}
orig = rs.invert_q
def grab(z, d, **kw):
    cap["z"], cap["d"] = z, [np.array(p) for p in d]
    return orig(z, d, **kw)
rs.invert_q = grab
_, diag = rs.reseed(z4)
print(f"D {m['D_str'][:10]}: ladder {[(round(r['u'], 4), r.get('its'), f'{r.get(chr(82), 0):.1e}', r.get('conv')) for r in diag['rungs']]}", flush=True)
z, d0 = cap["z"], cap["d"]
M, a, o = rs.M, rs.aoff, rs.off
s = rs.rung_solver(rs.us[-1]); rows = rs.rung_rows(); cols = np.r_[a["mh"]:a["mh"] + 2 * M]; L = a["L"]
n0, n1, nk = o["node"](0), o["node"](1), o["node"](rs.K - 1)
base = [np.zeros(L) for _ in range(4)]
for q in range(4):
    zq = np.asarray(z[q], dtype=float)
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
def ls_cols(B, R, lo, hi, dps=90):
    with mp.workdps(dps):
        n = len(R[0]); k = hi - lo
        A = mp.matrix(n, k)
        for i in range(n):
            for j in range(k):
                A[i, j] = sum(mp.mpf(float(B[q][i, lo + j])) for q in range(4))
        r = mp.matrix([sum(mp.mpf(float(R[q][i])) for q in range(4)) for i in range(n)])
        xs = mp.lu_solve(A.T * A, -(A.T * r))
        out = [np.zeros(2 * M) for _ in range(4)]
        for j in range(k):
            v = xs[j]
            for q in range(4):
                f = float(v); out[q][lo + j] = f; v = v - mp.mpf(f)
    return out
def newton(d, n, tr):
    for _ in range(n):
        R = res(d); x = [np.asarray(p) for p in QDLu(*block(d)).solve(*[-np.asarray(r) for r in R])]
        d = add(x, d); tr.append(f"{nr(res(d)):.1e}")
    return d
R0 = nr(res(d0)); print(f"  start |R| {R0:.2e}", flush=True)
for name in ("refactoring rule", "a_h first rule"):
    dd, h, c = orig(z, d0, ah_first=(name == "a_h first rule"))
    print(f"  {name}: " + " ".join(f"{e['R']:.1e}" for e in h) + f" -> {'converged' if c else 'NOT'}", flush=True)
tr = []; newton(d0, 8, tr); print("  pure Newton:", " ".join(tr), flush=True)
for nalt in (1, 3):
    d = d0; tr = []
    for _ in range(nalt):
        B = block(d); d = add(ls_cols(B, res(d), M, 2 * M), d); tr.append(f"a {nr(res(d)):.1e}")
        B = block(d); d = add(ls_cols(B, res(d), 0, M), d); tr.append(f"m {nr(res(d)):.1e}")
    newton(d, 6, tr); print(f"  {nalt}x (a_h, m_h) then Newton:", " ".join(tr), flush=True)
