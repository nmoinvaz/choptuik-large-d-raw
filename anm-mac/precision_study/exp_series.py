"""The jet series at a stored base in two arithmetic forms of the same model (horizon_alpha 0, the chain's, and 1):
|z_k| and |z_k(0) - z_k(1)| (if the high orders are rounding, they differ by their own size), a_max, and the
predictions' |F| in quad-double at a = 1/8..1, without and with anm_run's --fix1 (z_1 by quad-double central
differences, Richardson with exact weights here). Controls: form 0 must reproduce the chain's |F_pred| / a = 1.0492e-12
at a = 1/16 (notes/QUAD_DOUBLE.md 13.19, probe at D 82.1642) and the fixed series' 2.7-2.8e-14 a^2.
Read-only; one thread.   python exp_series.py [STATE]"""
import glob, json, os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import numpy as np
import mpmath as mp
from hpkernel.driver import make_solver, load_q, qparts
from multidouble import dd_add, dd_scale, dd_norm
from pinning import qd_axpy, band_coeffs, band_field, PinnedQ

mp.mp.dps = 50
RAW = "/Users/nathan/Source/choptuik-large-d-raw"
state = sys.argv[1] if len(sys.argv) > 1 else "anm-mac/run_trend_pin3_qd6/anm_pin3_D82.1642.npz"
N = 24
zq, m = load_q(os.path.join(RAW, state))
zq = tuple(np.ascontiguousarray(p) for p in zq)
zh, zl = zq[0].copy(), zq[1].copy()
D, M, nodes = mp.mpf(m["D_str"]), int(m["M"]), list(m["nodes"])
kt, kc, ks, kf = m["kt"], m["kc"], m["ks"], 3
mk = lambda Dx, al=0: make_solver(Dx, M, nodes=nodes, kt=kt, kc=kc, ks=ks, threads=1, kfreeze=kf, horizon_alpha=al)
c4 = lambda v: tuple(np.ascontiguousarray(np.asarray(p)) for p in v)
A = lambda p: (np.asarray(p[0]), np.asarray(p[1]))
val = lambda p: np.asarray(p[0]) + np.asarray(p[1])
s0 = mk(D); segs = s0.plan(zh, zl, 1e-32, 0.05); s0.set_segs(segs)
K = len(nodes); L = len(zh); hb = K * 4 * M; rows = slice(hb, hb + M)
ks_held = [k for k in range(kf + 1, 14) if k % 2 == 1]
base_coeffs = band_coeffs(zh[:M], zl[:M], M, ks_held)
slopes = [[0.0, 0.0] for _ in ks_held]; ns, vals = [], []
for f in sorted(glob.glob(os.path.join(RAW, "T75", "pin*_D*.npz")))[::4]:
    dd = np.load(f); mm = json.loads(str(dd["meta"]))
    if int(mm["M"]) == M:
        ns.append(float(mm["D"]) - 2.0); vals.append(band_coeffs(dd["zh"][:M], dd["zl"][:M], M, ks_held))
ns = np.array(ns)
for i, k in enumerate(ks_held):
    for j in (0, 1):
        v = np.array([c[i][j] for c in vals])
        if len(v) >= 6 and (np.all(v > 0) or np.all(v < 0)):
            sl, c0 = np.polyfit(np.log(ns), np.log(np.abs(v)), 1)
            if float(np.max(np.abs(np.log(np.abs(v)) - (c0 + sl * np.log(ns))))) < 0.05:
                slopes[i][j] = float(sl)
n0 = float(D) - 2.0
def binom(sx, j):
    r = 1.0
    for t in range(j):
        r *= (sx - t) / (t + 1)
    return r
held_jet = lambda j: band_field([(a * binom(sa, j) / n0 ** j, b * binom(sb, j) / n0 ** j) for (a, b), (sa, sb) in zip(base_coeffs, slopes)], ks_held, M)
held_at = lambda Dx: [(a * ((float(Dx) - 2.0) / n0) ** sa, b * ((float(Dx) - 2.0) / n0) ** sb) for (a, b), (sa, sb) in zip(base_coeffs, slopes)]

def coefficients(s, z1=None):
    Zh, Zl, norms = [zh], [zl], [float(dd_norm(zh, zl))]
    for k in range(1, N + 1):
        Hs, Ls = s.residual_jet(Zh, Zl, k + 1, 0)
        bh, bl = -np.asarray(Hs[k]), -np.asarray(Ls[k])
        bh, bl = bh.copy(), bl.copy()
        th, tl = held_jet(k)
        bh[rows], bl[rows] = dd_add(bh[rows], bl[rows], np.asarray(th), np.asarray(tl))
        if k == 1 and z1 is not None:
            xh, xl = A(z1)
        else:
            xh, xl = A(s.lu_solve(bh, bl))
            jh, jl = A(s.jvp(zh, zl, xh, xl)[:2])
            ch, cl = A(s.lu_solve(*dd_add(bh, bl, -jh, -jl)))
            xh, xl = A(dd_add(xh, xl, ch, cl))
        Zh.append(xh); Zl.append(xl); norms.append(float(dd_norm(xh, xl)))
    return Zh, Zl, norms

def order1_exact(z1):
    """the quad-double model's order-1 residual of z_1 (central differences along (z_1, 1), 2^-29 and 2^-30, the
    Richardson value 4 r(e/2) - r(e) divided by 3 in double-double), the held slope subtracted"""
    rs = []
    for e in (2.0 ** -29, 2.0 ** -30):
        Ks = []
        for sg in (1.0, -1.0):
            sx = mk(D + sg * mp.mpf(e)); sx.set_segs(segs)
            Ks.append(sx.residual_q(*c4(qd_axpy(sg * e, *qparts(*z1), *zq))))
        d = qd_axpy(-1.0, *c4(Ks[1]), *c4(Ks[0]))
        rs.append(dd_scale(np.asarray(d[0]), np.asarray(d[1]), 0.5 / e))
    R3 = dd_add(*dd_scale(rs[1][0], rs[1][1], 4.0), -np.asarray(rs[0][0]), -np.asarray(rs[0][1]))
    # division by 3 in double-double: x / 3 = x * (1/3) with 1/3 as a double-double (hi 1/3, lo its remainder)
    third_hi = 1.0 / 3.0; third_lo = float((mp.mpf(1) / 3 - mp.mpf(third_hi)))
    rh, rl = A(R3)
    ph, pl = A(dd_scale(rh, rl, third_hi)); qh, ql = A(dd_scale(rh, rl, third_lo))
    rh, rl = A(dd_add(ph, pl, qh, ql))
    th, tl = held_jet(1)
    rh, rl = rh.copy(), rl.copy()
    rh[rows], rl[rows] = dd_add(rh[rows], rl[rows], -np.asarray(th), -np.asarray(tl))
    return rh, rl

def fix_z1(s, z1):
    x = order1_exact(z1); hist = [float(dd_norm(*x))]
    for _ in range(2):
        ch, cl = A(s.lu_solve(-np.asarray(x[0]), -np.asarray(x[1])))
        z1 = A(dd_add(*z1, ch, cl)); x = order1_exact(z1); hist.append(float(dd_norm(*x)))
    return z1, hist

def series_at(Zh, Zl, a):
    ph, pl = np.array(Zh[-1]), np.array(Zl[-1])
    for k in range(len(Zh) - 2, 0, -1):
        ph, pl = dd_add(Zh[k], Zl[k], *dd_scale(ph, pl, a))
    return dd_add(zh, zl, *dd_scale(ph, pl, a))

def predicted(Zh, Zl, a):
    ph, pl = A(series_at(Zh, Zl, a)); Dn = D + mp.mpf(a)
    sn = mk(Dn); sn.set_segs(segs)
    hh, hl = band_field(held_at(Dn), ks_held, M)
    ch, cl = np.zeros(L), np.zeros(L); ch[rows], cl[rows] = hh, hl
    Fh, Fl = A(sn.residual(ph, pl))
    if float(dd_norm(*dd_add(Fh, Fl, -ch, -cl))) <= 1e-6:
        sn.set_segs(sn.plan(ph, pl, 1e-32, 0.05))
    Fd = float(dd_norm(*dd_add(*A(sn.residual(ph, pl)), -ch, -cl)))
    Fq = PinnedQ(sn, ch, cl).residual_q(*qparts(ph, pl))
    return Fd, float(dd_norm(np.asarray(Fq[0]), np.asarray(Fq[1])))

res = {}
ser = {}
for al in (0, 1):
    s = mk(D, al); s.set_segs(segs)
    t = time.time(); s.newton(zh, zl); Zh, Zl, norms = coefficients(s); tc = time.time() - t
    ser[al] = (Zh, Zl)
    a_max = (1e-14 * norms[1] / norms[N]) ** (1.0 / (N - 1))
    print(f"alpha {al}: coefficients {tc:.0f} s; a_max (eps 1e-14) {a_max:.3f}; |z_k| k = 1..{N}: " + " ".join(f"{x:.1e}" for x in norms[1:]), flush=True)
    pr = []
    for a in (1 / 16, 1 / 4, 1 / 2, 1.0):
        Fd, Fq = predicted(Zh, Zl, a); pr.append((a, Fd, Fq))
        print(f"  plain series, a {a:.4f}: |F_pred| dd {Fd:.4e}, qd {Fq:.4e} ({Fq / a:.4e} per a, {Fq / a ** 2:.4e} per a^2)", flush=True)
    t = time.time(); z1f, hist = fix_z1(s, (Zh[1], Zl[1])); Zfh, Zfl, normsf = coefficients(s, z1=z1f); tf = time.time() - t
    ser[(al, "fix")] = (Zfh, Zfl)
    a_maxf = (1e-14 * normsf[1] / normsf[N]) ** (1.0 / (N - 1))
    print(f"  fix1 ({tf:.0f} s): order-1 residual norms {['%.2e' % x for x in hist]}; a_max {a_maxf:.3f}; |z_k|: " + " ".join(f"{x:.1e}" for x in normsf[1:]), flush=True)
    prf = []
    for a in (1 / 16, 1 / 4, 1 / 2, 1.0, 1.5):
        Fd, Fq = predicted(Zfh, Zfl, a); prf.append((a, Fd, Fq))
        print(f"  fixed series, a {a:.4f}: |F_pred| dd {Fd:.4e}, qd {Fq:.4e} ({Fq / a ** 2:.4e} per a^2)", flush=True)
    res[al] = dict(norms=norms, a_max=a_max, pred=pr, fix_hist=hist, norms_fix=normsf, a_max_fix=a_maxf, pred_fix=prf)
for key in ((0, 1), ((0, "fix"), (1, "fix"))):
    a, b = key
    d = [float(dd_norm(*dd_add(ser[a][0][k], ser[a][1][k], -ser[b][0][k], -ser[b][1][k]))) for k in range(1, N + 1)]
    na = [float(dd_norm(ser[a][0][k], ser[a][1][k])) for k in range(1, N + 1)]
    print(f"|z_k({a}) - z_k({b})| / |z_k({a})|, k = 1..{N}: " + " ".join(f"{x / y:.1e}" for x, y in zip(d, na)), flush=True)
    res[str(key)] = [x / y for x, y in zip(d, na)]
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp_series_" + os.path.basename(state).replace(".npz", ".json")), "w"), indent=1)
