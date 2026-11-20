import sys, os, json, time, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1025/solver/matter")
os.chdir("/Users/nathan/Source/choptuik-1025/solver/matter")
import multidouble as md
import ddnp as dd
import ell_ddm
lams = [float(v) for v in sys.argv[1].split(",")]
S, z = ell_ddm._setup("data/sol_l1kc55Fs1025_D17.5000.npy", 17.5, 55)
blocks, offs = S._block_list(); blk = 3 * S.n_odd + 2 * S.n_even
c0, nf, fun, tgt = blocks[12]; r0 = 12 * blk
sl = (slice(r0, r0 + blk), slice(c0, c0 + nf))
out = "data/ell_ddm_b12cause_1025.jsonl"


def b12(lam):
    Md = ell_ddm.DDEll(S).mode_matrix(z, lam, only=[12])
    return Md.h[sl].copy(), Md.l[sl].copy()


def errs(B, Bd):
    col = np.linalg.norm(B - Bd, axis=0) / np.maximum(np.linalg.norm(Bd, axis=0), 1e-300)
    return float(np.max(np.abs(B - Bd)) / np.max(np.abs(Bd))), float(np.max(col))


res = {}
for lam in lams:
    t0 = time.time()
    with np.errstate(all="ignore"):
        Mf = S.mode_matrix(z, lam)
    h, l = b12(lam)
    res[lam] = dict(Mf=Mf, h=h, l=l, t=time.time() - t0)
    print(f"lam {lam}: float64 M and dd block 12 in {res[lam]['t']:.0f} s", flush=True)
# hionly: ell_ddm's --mutate=hionly wrapper, applied after the dd builds; a fresh DDEll per build
for _nm in ("add", "sub", "mul", "div", "mul_d", "add_d", "neg"):
    setattr(dd, _nm, (lambda f: lambda *a: (lambda r: dd.R(r.h, np.zeros_like(r.h)))(f(*a)))(getattr(dd, _nm)))
ell_ddm.MUTATE = "hionly"
for lam in lams:
    t0 = time.time()
    hh, hl = b12(lam)
    r = res[lam]; Mf, h, l = r["Mf"], r["h"], r["l"]
    Bd = h + l
    ef, ef_col = errs(Mf[sl], Bd)
    eh, eh_col = errs(hh + hl, Bd)
    A, Al = Mf.copy(), np.zeros_like(Mf); A[sl] = h; Al[sl] = l
    Bm, Bl = Mf.copy(), np.zeros_like(Mf); Bm[sl] = hh; Bl[sl] = hl
    sa, la = md.dd_logdet(A, Al, True)[:2]
    sb, lb = md.dd_logdet(Bm, Bl, True)[:2]
    sc, lc = md.dd_logdet(Mf, np.zeros_like(Mf), True)[:2]
    rec = dict(D=17.5, kc=55, lam=lam, b12_rel_f64=[ef, ef_col], b12_rel_hionly=[eh, eh_col], hybrid_dd=[sa, la],
               hybrid_hionly=[sb, lb], f64=[sc, lc], hionly_lo_max=float(np.max(np.abs(hl))), sec=round(time.time() - t0 + r["t"]))
    print(f"lam {lam}: block 12 vs dd: float64 {ef:.2e} (column {ef_col:.2e}), hionly {eh:.2e} (column {eh_col:.2e}), "
          f"hionly lo max {rec['hionly_lo_max']:.1e}", flush=True)
    print(f"lam {lam}: det (a) f64 + dd b12 {sa:+.0f} {la:.10f}; (b) f64 + hionly b12 {sb:+.0f} {lb:.10f}; (c) f64 {sc:+.0f} {lc:.10f}",
          flush=True)
    open(out, "a").write(json.dumps(rec) + "\n")
