"""#1102: DDEll's block 12 against itself with another, equally valid f64 LU in its periodic solves (the transposed
system: lu_factor(A^T), lu_solve(trans=1)), entry by entry: the reference's own rounding spread.
usage: ref_lu_spread.py MATTER_DIR STUB STATE D LAM"""
import sys, time
sys.path.insert(0, sys.argv[1])
import numpy as np
import scipy.linalg as sla
from ell_fastm import load_system
import ell_ddm, ell_b12rs
stub, st, D, lam = sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
S, z, rec, same, msg = load_system(stub, st, D)
print(msg, flush=True)
E = ell_ddm.DDEll(S)
with np.errstate(all="ignore"):
    t0 = time.time()
    A = ell_b12rs.block_of(E.mode_matrix(z, lam, only=[12]), S)
    ta = time.time() - t0
    f0, s0 = sla.lu_factor, sla.lu_solve
    sla.lu_factor = lambda M: ("T", f0(np.ascontiguousarray(M.T)))
    sla.lu_solve = lambda lu, b: s0(lu[1], b, trans=1)
    try:
        B = ell_b12rs.block_of(E.mode_matrix(z, lam, only=[12]), S)
    finally:
        sla.lu_factor, sla.lu_solve = f0, s0
c = ell_b12rs.compare(B, A)
a = np.abs(A.h)
print(f"k_c {S.kc} D {D} lambda {lam}: DDEll with the transposed LU against DDEll: {c['same']} of {c['n']} entries bit for bit, "
      f"max |d|/|entry| {c['rel_entry']:.3e}, max |d|/max|block| {c['rel_max']:.3e}; block entries from {a[a > 0].min():.2e} "
      f"to {a.max():.2e}, {np.mean(a < 1e-10 * a.max()):.0%} below 1e-10 of the largest ({ta:.0f} s per block)", flush=True)
