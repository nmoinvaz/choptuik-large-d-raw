"""At several stored bases of the quad-double chain (D 79.8-86.4): (1) the quad-double model's order-1 residual of the
double-double jet's z_1 (the prediction's |F| / a), in horizon_alpha 0 (the chain's form) and 1; (2) max |dF/dD| at
fixed data; (3) the contraction of --fix1's pass through the double-double LU and through the quad-double LU of
newton_q at the base. Exact Richardson weights. Prints 2-norms (as the chain's records) and max norms. Read-only; one
thread.   python exp_multi.py STATE [STATE ...]"""
import glob, json, os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np
import mpmath as mp
from hpkernel.driver import make_solver, load_q, qparts
from multidouble import dd_add, dd_scale
from pinning import qd_axpy, band_coeffs, band_field

mp.mp.dps = 50
RAW = "/Users/nathan/Source/choptuik-large-d-raw"
c4 = lambda v: tuple(np.ascontiguousarray(np.asarray(p)) for p in v)
A = lambda p: (np.asarray(p[0]), np.asarray(p[1]))
val = lambda p: np.asarray(p[0]) + np.asarray(p[1])
n2 = lambda p: float(np.sqrt(np.sum(val(p) ** 2)))
nmax = lambda p: float(np.abs(val(p)).max())
third_hi = 1.0 / 3.0; third_lo = float(mp.mpf(1) / 3 - mp.mpf(third_hi))
# trend exponents from T75 (anm_run --trend T75); the base coefficients per state
T75 = []
for f in sorted(glob.glob(os.path.join(RAW, "T75", "pin*_D*.npz")))[::4]:
    dd = np.load(f); mm = json.loads(str(dd["meta"])); T75.append((float(mm["D"]) - 2.0, int(mm["M"]), dd["zh"], dd["zl"]))
out = []
for state in sys.argv[1:]:
    t0 = time.time()
    zq, m = load_q(os.path.join(RAW, state)); zq = c4(zq); zh, zl = zq[0].copy(), zq[1].copy()
    D, M, nodes = mp.mpf(m["D_str"]), int(m["M"]), list(m["nodes"])
    kt, kc, ks, kf = m["kt"], m["kc"], m["ks"], 3
    mk = lambda Dx, al=0: make_solver(Dx, M, nodes=nodes, kt=kt, kc=kc, ks=ks, threads=1, kfreeze=kf, horizon_alpha=al)
    s0 = mk(D); segs = s0.plan(zh, zl, 1e-32, 0.05)
    K = len(nodes); L = len(zh); hb = K * 4 * M; rows = slice(hb, hb + M)
    ks_held = [k for k in range(kf + 1, 14) if k % 2 == 1]
    base = band_coeffs(zh[:M], zl[:M], M, ks_held)
    ns = np.array([t[0] for t in T75 if t[1] == M]); vals = [band_coeffs(t[2][:M], t[3][:M], M, ks_held) for t in T75 if t[1] == M]
    slopes = [[0.0, 0.0] for _ in ks_held]
    for i, k in enumerate(ks_held):
        for j in (0, 1):
            v = np.array([c[i][j] for c in vals])
            if len(v) >= 6 and (np.all(v > 0) or np.all(v < 0)):
                sl, c0 = np.polyfit(np.log(ns), np.log(np.abs(v)), 1)
                if float(np.max(np.abs(np.log(np.abs(v)) - (c0 + sl * np.log(ns))))) < 0.05:
                    slopes[i][j] = float(sl)
    n0 = float(D) - 2.0
    held1 = band_field([(a * sa / n0, b * sb / n0) for (a, b), (sa, sb) in zip(base, slopes)], ks_held, M)

    def order1(z1):
        rs = []
        for e in (2.0 ** -29, 2.0 ** -30):
            Ks = []
            for sg in (1.0, -1.0):
                sx = mk(D + sg * mp.mpf(e)); sx.set_segs(segs)
                Ks.append(sx.residual_q(*c4(qd_axpy(sg * e, *qparts(*z1), *zq))))
            d = qd_axpy(-1.0, *c4(Ks[1]), *c4(Ks[0]))
            rs.append(dd_scale(np.asarray(d[0]), np.asarray(d[1]), 0.5 / e))
        rh, rl = A(dd_add(*dd_scale(rs[1][0], rs[1][1], 4.0), -np.asarray(rs[0][0]), -np.asarray(rs[0][1])))
        rh, rl = A(dd_add(*dd_scale(rh, rl, third_hi), *dd_scale(rh, rl, third_lo)))
        rh, rl = rh.copy(), rl.copy()
        rh[rows], rl[rows] = dd_add(rh[rows], rl[rows], -np.asarray(held1[0]), -np.asarray(held1[1]))
        return rh, rl

    rec = dict(state=state, D=float(D))
    for al in (0, 1):
        s = mk(D, al); s.set_segs(segs); s.newton(zh, zl)
        Hs, Ls = s.residual_jet([zh], [zl], 2, 0)
        if al == 0:
            rec["FD_max"] = nmax((Hs[1], Ls[1])); rec["FD_2"] = n2((Hs[1], Ls[1]))
        bh, bl = -np.asarray(Hs[1]).copy(), -np.asarray(Ls[1]).copy()
        bh[rows], bl[rows] = dd_add(bh[rows], bl[rows], np.asarray(held1[0]), np.asarray(held1[1]))
        x = A(s.lu_solve(bh, bl)); j = A(s.jvp(zh, zl, *x)[:2])
        x = A(dd_add(*x, *A(s.lu_solve(*dd_add(bh, bl, -j[0], -j[1])))))
        r = order1(x)
        rec[f"e1_2_a{al}"] = n2(r); rec[f"e1_max_a{al}"] = nmax(r)
        if al == 0:
            # one fix pass through the double-double LU
            z1d = A(dd_add(*x, *A(s.lu_solve(-r[0], -r[1])))); rd = order1(z1d)
            rec["c_dd"] = n2(rd) / n2(r)
            # one fix pass through the quad-double LU at the base (newton_q factors it)
            tq = time.time(); s.newton_q(*zq); rec["t_newton_q"] = time.time() - tq
            q = s.qlu_solve(-r[0], -r[1], np.zeros(L), np.zeros(L))
            z1q = A(dd_add(*x, np.asarray(q[0]), np.asarray(q[1]))); rq = order1(z1q)
            rec["c_qd"] = n2(rq) / n2(r)
    rec["t"] = time.time() - t0
    G = 0.7 ** (-(float(D) - 3.0)); rec["epsG_FD"] = 2.0 ** -106 * G * rec["FD_max"]
    print(f"D {float(D):.4f}: |dF/dD| max {rec['FD_max']:.3e}; order-1 error (2-norm / max) alpha 0 {rec['e1_2_a0']:.3e} / {rec['e1_max_a0']:.3e}, "
          f"alpha 1 {rec['e1_2_a1']:.3e} / {rec['e1_max_a1']:.3e} (ratio {rec['e1_2_a0'] / rec['e1_2_a1']:.1f}); eps_dd G |dF/dD| {rec['epsG_FD']:.2e}; "
          f"fix pass contraction: dd LU {rec['c_dd']:.2e}, qd LU {rec['c_qd']:.2e} (newton_q {rec['t_newton_q']:.0f} s); {rec['t']:.0f} s", flush=True)
    out.append(rec)
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp_multi.json"), "w"), indent=1)
xs = np.array([r["D"] for r in out])
for key in ("FD_max", "e1_2_a0", "e1_2_a1", "c_dd"):
    y = np.log10([r[key] for r in out]); b = np.polyfit(xs, y, 1)
    print(f"{key}: growth {10 ** b[0]:.3f}x per unit D over D {xs.min():.2f}-{xs.max():.2f} (rms {np.sqrt(np.mean((y - np.polyval(b, xs)) ** 2)):.2f} decades)")
