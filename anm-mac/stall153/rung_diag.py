"""Diagnose the u0 rung's quad-double polish (reseed.Reseeder.invert_q) at T118's 152.93 state, re-seeded at D + a:
every iterate, chord (Jacobian factored once, as invert_q) against Newton (refactored each step), past non-halving."""
import json, os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np
import mpmath as mp
from hpkernel.driver import load_q
from multidouble import QDLu, qd_axpy
from reseed import Reseeder

mp.mp.dps = 50
state, a, mode, its = sys.argv[1], float(sys.argv[2]), sys.argv[3], int(sys.argv[4])
z4, m = load_q(state)
D = mp.mpf(m["D_str"]) + mp.mpf(a)
rs = Reseeder(dict(M=m["M"], nodes=m["nodes"], kt=m["kt"], kc=m["kc"], ks=m["ks"]), D, threads=4, qd=True)
orig_invert_q = rs.invert_q


def invert_q_diag(z4, d4, it_max=6):
    M, aoff, o = rs.M, rs.aoff, rs.off
    u = rs.us[-1]
    s = rs.rung_solver(u)
    rows = rs.rung_rows()
    cols = np.r_[aoff["mh"]:aoff["mh"] + 2 * M]
    L = aoff["L"]
    base = [np.zeros(L) for _ in range(4)]
    n0, n1 = o["node"](0), o["node"](1)
    nk = o["node"](rs.K - 1)
    for q in range(4):
        zq = np.asarray(z4[q], dtype=float)
        base[q][:2 * M] = zq[:2 * M]
        base[q][aoff["node"](0):aoff["node"](1)] = zq[n0:n1]
        base[q][aoff["node"](1):aoff["node"](1) + 4 * M] = zq[nk:nk + 4 * M]
        base[q][-1] = zq[-1]

    def put(d):
        v = [b.copy() for b in base]
        for q in range(4):
            v[q][cols] = d[q]
        return tuple(np.ascontiguousarray(x) for x in v)

    def res(d):
        F = s.residual_q(*put(d))
        return [np.asarray(F[q])[rows] for q in range(4)]

    d = [np.ascontiguousarray(np.asarray(x, dtype=float)) for x in d4]
    R = res(d)
    nR = float(np.max(np.abs(R[0] + R[1])))
    print(f"  {mode}: it 0 |R| {nR:.3e}", flush=True)
    t0 = time.time()
    J = s.jacobian_q(*put(d))
    lu = QDLu(*[np.asarray(J[q])[np.ix_(rows, cols)] for q in range(4)])
    print(f"  jacobian_q + QDLu {time.time() - t0:.1f} s", flush=True)
    for it in range(its):
        if mode == "newton" and it > 0:
            J = s.jacobian_q(*put(d))
            lu = QDLu(*[np.asarray(J[q])[np.ix_(rows, cols)] for q in range(4)])
        x = lu.solve(*[-np.asarray(r) for r in R])
        dn = [np.ascontiguousarray(np.asarray(p)) for p in qd_axpy(1.0, *x, *d)]
        Rn = res(dn)
        nn = float(np.max(np.abs(Rn[0] + Rn[1])))
        print(f"  {mode}: it {it + 1} |R| {nn:.3e} step {float(np.max(np.abs(np.asarray(x[0])))):.3e}"
              f"{'  (not lower)' if nn >= nR else ''}", flush=True)
        if not np.isfinite(nn):
            break
        if nn < nR:
            d, R, nR = dn, Rn, nn
    return d, [dict(R=nR)], nR < 1e-24


rs.invert_q = invert_q_diag
print(f"D {mp.nstr(D, 15)} (state {m['D_str'][:12]} + {a}), u rungs {rs.us}", flush=True)
zr, diag = rs.reseed(z4, verbose=True)
print("ok", diag["ok"])
