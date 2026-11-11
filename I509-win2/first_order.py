#!/usr/bin/env python3
"""#509: first-order effect of the two forms of dtau_c on ln|det M| at one check point of October's cache.
usage: python first_order.py MATS_DIR POINT [BITS] [--control]
  reads mat_old_p<POINT>.npz and mat_new_p<POINT>.npz (dump_matrices.py), builds both complex matrices exactly (hi + lo, python-flint acb_mat at BITS bits, default 320),
  and prints
    - the size of dM = M_new - M_old against M (entries that differ, max and rms relative difference),
    - ln|det M_old| and ln|det M_new| to BITS bits (ball arithmetic), their difference, and the code's own values (CSolver.mode_det) with the difference of each,
    - the first-order estimate Re tr(M_old^-1 dM), and the second-order remainder (exact difference minus first order),
    - |M_old^-1| statistics: the largest |(M^-1)_ji| and the dM-weighted sum's largest terms.
  --control: plants a change of known size in M_old, M' = M_old + eps E_ij (eps = 1e-20 |M_ij|, (i, j) the entry with the largest |(M^-1)_ji|), and requires
    ln|det M'| - ln|det M_old| = Re(eps (M^-1)_ji) to a relative 1e-6 (the first-order formula at its own size) and exits 1 if it does not."""
import sys, time
import numpy as np
from flint import acb_mat, acb, arb, ctx

mats, pt = sys.argv[1], sys.argv[2]
bits = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 320
control = "--control" in sys.argv
ctx.prec = bits
t0 = time.time()
def log(s): print(f"[{time.time() - t0:6.0f} s] {s}", flush=True)

def load(tag):
    z = np.load(f"{mats}/mat_{tag}_p{pt}.npz")
    return z, z["re_hi"], z["re_lo"], z["im_hi"], z["im_lo"]

zo, rho, rlo, iho, ilo = load("old")
zn, rhn, rln, ihn, iln = load("new")
n = rho.shape[0]
log(f"point {pt}: n {n}, bits {bits}; code ln|det| old {zo['det'][0]!r}, new {zn['det'][0]!r}, difference {zn['det'][0] - zo['det'][0]:.4e}")

def to_acb(rh, rl, ih, il):
    # exact: hi + lo as balls at `bits` bits (two doubles add exactly well within 320 bits when the exponents differ by < 300)
    out = []
    for i in range(n):
        for j in range(n):
            out.append(acb(arb(float(rh[i, j])) + arb(float(rl[i, j])), arb(float(ih[i, j])) + arb(float(il[i, j]))))
    return acb_mat(n, n, out)

Mo = to_acb(rho, rlo, iho, ilo); log("built M_old")
Mn = to_acb(rhn, rln, ihn, iln); log("built M_new")

# dM in f64 pairs (exact difference of the DD values, as double-double sums; used for statistics)
dre = (rhn.astype(np.longdouble) - rho) + (rln.astype(np.longdouble) - rlo)
dim = (ihn.astype(np.longdouble) - iho) + (iln.astype(np.longdouble) - ilo)
dabs = np.hypot(dre.astype(float), dim.astype(float))
mabs = np.hypot(rho + rlo, iho + ilo)
diff = dabs > 0
rel = np.where(mabs > 0, dabs / np.where(mabs > 0, mabs, 1), 0.0)
log(f"dM: {int(diff.sum())} of {n * n} entries differ; max |dM_ij| / |M_ij| {rel.max():.3e}; rms over differing entries {np.sqrt((rel[diff] ** 2).mean()):.3e}; max |dM| {dabs.max():.3e}; max |M| {mabs.max():.3e}; Frobenius |dM| / |M| {np.linalg.norm(dabs) / np.linalg.norm(mabs):.3e}")

def lnabs_det(M):
    d = M.det()
    a = abs(d)
    return a.log(), d

lo, do_ = lnabs_det(Mo); log(f"exact ln|det M_old| = {lo.str(30)}  (code {zo['det'][0]!r})")
ln_, dn_ = lnabs_det(Mn); log(f"exact ln|det M_new| = {ln_.str(30)}  (code {zn['det'][0]!r})")
dex = ln_ - lo
log(f"exact difference ln|det M_new| - ln|det M_old| = {dex.str(15)}; the code's difference {zn['det'][0] - zo['det'][0]:.6e}")
log(f"code minus exact: old {float(zo['det'][0]) - float(lo.mid()):.3e}, new {float(zn['det'][0]) - float(ln_.mid()):.3e}")

# first order: Re tr(M_old^-1 dM) with dM = M_new - M_old
dM = Mn - Mo
X = Mo.solve(dM, algorithm="approx") if True else None
log("solved M_old X = dM")
tr = sum((X[i, i] for i in range(n)), acb(0))
first = tr.real
log(f"first-order Re tr(M_old^-1 dM) = {first.str(15)}; exact difference minus first order {(dex - first).str(10)}")

if control:
    Minv = Mo.solve(acb_mat(n, n, [acb(1) if i == j else acb(0) for i in range(n) for j in range(n)]), algorithm="approx")
    best = max(((abs(Minv[j, i]), i, j) for i in range(n) for j in range(n) if mabs[i, j] > 0), key=lambda t: float(t[0].mid()))
    _, i, j = best
    eps = arb(10) ** -20 * arb(float(mabs[i, j]))
    pert = acb_mat(n, n, [acb(0)] * (n * n))
    pert[i, j] = acb(eps)
    Mp = Mo + pert
    lp, _ = lnabs_det(Mp)
    meas = lp - lo
    pred = (eps * Minv[j, i]).real
    ratio = meas / pred
    log(f"control: planted eps {eps.str(5)} at ({i}, {j}); measured ln|det| change {meas.str(10)}, predicted Re(eps (M^-1)_ji) {pred.str(10)}, ratio {ratio.str(10)}")
    ok = abs(float(ratio.mid()) - 1.0) < 1e-6
    log("control " + ("passed" if ok else "FAILED"))
    sys.exit(0 if ok else 1)
