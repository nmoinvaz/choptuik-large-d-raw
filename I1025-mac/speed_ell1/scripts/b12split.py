"""where block 12's float64 error arises: dd series + float64 variational RK against the all-dd block 12"""
import sys, time, json, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-ell1-speed/solver/matter")
import ell_fastm as fm, ell_ddm, multidouble as md
from dss_ell import PAR
recf, st, D = sys.argv[1], sys.argv[2], float(sys.argv[3])
lams = [float(v) for v in sys.argv[4].split(",")]
S, z, rec, same, msg = fm.load_system(recf, st, D)
print(msg, flush=True)
E = ell_ddm.DDEll(S)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; X = z[c0:c0 + nf]; r0 = 12 * blk
sl = (slice(r0, r0 + blk), slice(c0, c0 + nf))
mask = np.zeros((S.layout()[2] - 1,) * 2, bool)
for b, (cc, nn, ff, tt) in enumerate(blocks[:12]):
    mask[b * blk:(b + 1) * blk, cc:cc + nn] = True
om = 2 * np.pi / z[-1]
no, ne = S.n_odd, S.n_even
ops = fm.CoefOps(S)
def rel(A, Bh, Bl):
    return float(np.max(np.abs((A - Bh) - Bl)) / np.max(np.abs(Bh)))
for lam in lams:
    t0 = time.time()
    with np.errstate(all="ignore"):
        Mf = fm.mode_matrix_fast(S, z, lam)
    t1 = time.time()
    Md = E.mode_matrix(z, lam, only=[12])
    t2 = time.time()
    E.om = om; E.lam = lam
    try:
        mS, aS, qS = E._inputs(X, [no, ne, no], ["odd", "even", "odd"])
        Sx = E.ssh_series(E.phys(mS, "odd"), E.phys(aS, "even"), E.phys(qS, "odd"))
        s = [E.spec(ell_ddm._eval_series(Sf, S.u0), E.PAR[f]) for f, Sf in enumerate(Sx)]
    finally:
        E.lam = 0.0
    t3 = time.time()
    v = [x.v.h + x.v.l for x in s]
    dc_dd = np.concatenate([x.t.h for x in s], axis=1); dc_ddl = np.concatenate([x.t.l for x in s], axis=1)
    with np.errstate(all="ignore"):
        s64, ds64 = fm.series_cs(S, 12, X, om, lam)
    dc64 = S.tospec(ds64)
    with np.errstate(all="ignore"):
        _, ds64c = fm.series_cs(S, 12, X, om, lam, one_lu=False)
    e_series_c = rel(S.tospec(ds64c), dc_dd, dc_ddl)
    Mcs = fm.mode_matrix_cs(S, z, lam, only=[12])
    e_cs = rel(Mcs[sl], Md.h[sl], Md.l[sl])
    s0 = np.stack([S.phys(v[f], PAR[f]) for f in range(5)])
    with np.errstate(all="ignore"):
        _, dcE = fm.seg_lin(S, s0, dc_dd + dc_ddl, 1 - S.u0, S.nodes[-1], om, lam, ops)
    t4 = time.time()
    B3 = Mf.copy(); B3[sl] = dcE.T
    e_series = rel(dc64, dc_dd, dc_ddl)
    e64 = rel(Mf[sl], Md.h[sl], Md.l[sl]); e3 = rel(B3[sl], Md.h[sl], Md.l[sl])
    H = Mf.copy(); Hl = np.zeros_like(Mf); H[sl] = Md.h[sl]; Hl[sl] = Md.l[sl]
    sh, lh = md.dd_logdet(H, Hl, True)[:2]
    s3, l3 = md.dd_logdet(B3, np.zeros_like(B3), True)[:2]
    sf, lf = np.linalg.slogdet(Mf)
    print(f"lam {lam}: starting tangents vs dd series: f64 series one LU {e_series:.2e}, per-member LU {e_series_c:.2e}; block 12 vs dd: fast f64 {e64:.2e}, complex step f64 {e_cs:.2e}, dd series + f64 RK {e3:.2e}", flush=True)
    print(f"   det: hybrid {sh:+.0f} {lh:.10f}; dd series + f64 RK {s3:+.0f} {l3:.10f} (diff {l3 - lh:+.2e}); float64 {sf:+.0f} {lf:.10f} (diff {lf - lh:+.2e})", flush=True)
    print(f"   seconds: fast M {t1 - t0:.0f}, dd block 12 {t2 - t1:.0f}, dd series {t3 - t2:.0f}, f64 RK of block 12 {t4 - t3:.0f}", flush=True)
