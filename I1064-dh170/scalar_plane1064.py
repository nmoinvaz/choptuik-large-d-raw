#!/usr/bin/env python3
"""#1064 part 2, design 3 (README, written before it ran): the weak pair's plane at D 262.0099, ks 315.

    cd hp && python3 scalar_plane1064.py RAWDIR STATE --ks=K [--keep_plan=0|1] [--its=32] [--threads=4] [--json=OUT] [--mutate=E1sign]

Design 2 (scalar_scan1064.py) found along v_1 and v_2 that g_i(t) = u_i . R(z + t v) has no t^2 term (|second derivative| below 5e-19, against 1.4e49 in the max norm) and a negative even quartic term (g_1) along both axes. The
pair's roots then lie where a_i + A_i(theta) r + E_i(theta) r^2 = 0 with r = rho^2 (the even part of g_i along v(theta) = cos(theta) v_1 + sin(theta) v_2), the odd terms being 1e-8 and 1e-15 of a_i at rho ~ 1e-29.
This script measures the even part on 12 directions (theta = 0, 15, ..., 165 degrees), t = +-10^e, e = -29 .. -24, both projections:
  Ev_i(theta, t) = (g_i(t v) + g_i(-t v) - 2 a_i) / 2 = A_i t^2 + E_i t^4 + F_i t^6,
fits (A_i, E_i, F_i)(theta) per direction (least squares over the six decades), fits E_i(theta) and A_i(theta) as forms of degree 4 and 2 in (cos, sin), solves the model system for (theta, r), and checks every model root against the true residual.
Controls (exit 1 on failure):
  Q1  per direction, the three-term fit reproduces Ev_i / t^2 at every decade within 1e-3 of the largest term at that decade;
  Q2  the quartic form E_i(theta) (five coefficients) reproduces the twelve fitted E_i within 1e-3 of max |E_i|;
  Q3  the axes agree with design 2: E_1(0) = -1.094e80, E_2(0) = +8.083e78, E_1(90) = -1.937e82, E_2(90) = +4.311e81 within 1e-2 (the table's g/t^4 at e = -24);
  Q4  planted root through the true residual: R_pl(z) = R(z) - R(z + rho* v(theta*)), theta* = 40 degrees, rho* = 1.5e-29 (an exact root of R_pl); the same model solver on a_pl = a - g(z*) must return (theta*, rho*) (or the equivalent -s*) within 1e-3 relative;
  Q5  every model root of the data (if any) is refined by Newton on the true weak map G(s) = (u_1.R, u_2.R)(z + s_1 v_1 + s_2 v_2) (finite-difference Jacobian) and must end with |g_i| <= 1e-6 |a_i|;
  --mutate=E1sign flips the sign of the fitted quartic form E_1 in the solver only: Q4 must fail."""
import json
import os
import sys
import time

import numpy as np

HP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("HP_DIR", HP))
import mpmath as mp  # noqa: E402

mp.mp.dps = 140
THETAS = [mp.pi * m / 12 for m in range(12)]
EXPS = [-29, -28, -27, -26, -25, -24]


def nstr(x, n=5):
    return mp.nstr(x, n)


def fit_ls(rows, ys):
    """least squares (mp) for y = sum_k c_k rows[k]; rows: list of lists (len n_points) -> coefficients"""
    n = len(rows)
    Amat = mp.matrix(n, n)
    b = mp.matrix(n, 1)
    for p in range(n):
        for q in range(n):
            Amat[p, q] = mp.fsum(rows[p][m] * rows[q][m] for m in range(len(ys)))
        b[p] = mp.fsum(rows[p][m] * ys[m] for m in range(len(ys)))
    return list(mp.lu_solve(Amat, b))


def quartic_basis(th):
    c, s = mp.cos(th), mp.sin(th)
    return [c ** 4, c ** 3 * s, c ** 2 * s ** 2, c * s ** 3, s ** 4]


def quad_basis(th):
    c, s = mp.cos(th), mp.sin(th)
    return [c * c, c * s, s * s]


def model_roots(a, Acoef, Ecoef, ngrid=720):
    """the roots (theta, r) of a_i + A_i(theta) r + E_i(theta) r^2 = 0, i = 1, 2, r > 0, theta in [0, pi) (the even part is invariant under s -> -s). For each theta the first equation's positive roots r;
    H(theta) = the second equation there; sign changes of H over the grid are bisected."""
    def AE(i, th):
        return mp.fsum(c * b for c, b in zip(Acoef[i], quad_basis(th))), mp.fsum(c * b for c, b in zip(Ecoef[i], quartic_basis(th)))

    def eq(i, th, r):
        A, E = AE(i, th)
        return a[i] + A * r + E * r * r

    def rpos(th):
        A, E = AE(0, th)
        if E == 0:
            return [-a[0] / A] if A != 0 and -a[0] / A > 0 else []
        disc = A * A - 4 * E * a[0]
        if disc < 0:
            return []
        out = [(-A + s * mp.sqrt(disc)) / (2 * E) for s in (1, -1)]
        return sorted(r for r in out if r > 0)
    roots = []
    prev = {}
    for m in range(ngrid + 1):
        th = mp.pi * m / ngrid
        cur = {}
        for n, r in enumerate(rpos(th)):
            cur[n] = (r, eq(1, th, r))
        # branches are matched by order (the smaller or the larger positive root) while the count is unchanged
        for n in cur:
            if n in prev and len(prev) == len(cur) and (prev[n][1] > 0) != (cur[n][1] > 0):
                lo, hi = mp.pi * (m - 1) / ngrid, th
                for _ in range(150):
                    mid = (lo + hi) / 2
                    rm = rpos(mid)
                    if len(rm) != len(cur):
                        break
                    hm = eq(1, mid, rm[n])
                    h_lo = eq(1, lo, rpos(lo)[n])
                    if (hm > 0) == (h_lo > 0):
                        lo = mid
                    else:
                        hi = mid
                thm = (lo + hi) / 2
                rm = rpos(thm)
                if len(rm) == len(cur):
                    roots.append((thm, rm[n]))
        prev = cur
    return roots


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    opts = dict(x[2:].split("=", 1) for x in sys.argv[1:] if x.startswith("--") and "=" in x)
    if len(args) < 2 or "ks" not in opts:
        sys.exit(__doc__)
    from hpkernel.driver import make_solver
    from octo_corrector import load_o
    import near_null as nn
    raw, st = args
    its, ks = int(opts.get("its", 32)), int(opts["ks"])
    mutate = opts.get("mutate", "")
    z, m = load_o(os.path.join(raw, st))
    z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
    M, nodes = int(m["M"]), list(m["nodes"])
    D = m.get("D_str", repr(float(m["D"])))
    kf = int(m.get("kfreeze", 3))
    s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=ks, threads=int(opts.get("threads", 4)), kfreeze=kf)
    keep_plan = opts.get("keep_plan", "1") == "1" and "segs" in m and ks == m.get("ks", 130)
    s.set_segs(m["segs"] if keep_plan else s.plan(z[0], z[1], 1e-32, 0.05))
    print(f"{st}: D {float(m['D']):g}, ks {ks} (the state's {m.get('ks', 130)}), plan {'stored' if keep_plan else 'made again'}, M {M}, kfreeze {kf}" + (f", MUTATE {mutate}" if mutate else ""), flush=True)
    L = len(z[0])
    zero = np.zeros(L)
    Z8 = [zero] * 8
    from multidouble import od_axpy
    from pinning import PinnedSolver, band_coeffs, band_field
    t0 = time.time()
    keep = hasattr(s, "jacobian_o_kept")
    out = s.newton_o(z, keep_jacobian=True) if keep else s.newton_o(z)
    print(f"octo-double LU {time.time() - t0:.0f} s, pivots {out[3]:.1e}..{out[4]:.1e}", flush=True)
    F8 = s.newton_o_residual(z) if hasattr(s, "newton_o_residual") else s.residual_o(z)
    F8 = [np.ascontiguousarray(np.asarray(p)) for p in F8]
    ks_held = [h for h in range(kf + 1, 14) if h % 2 == 1]
    hc = band_coeffs(z[0][:M], z[1][:M], M, ks_held, exact=True, rest=[p[:M] for p in z[2:]])
    hf = band_field(hc, ks_held, M, parts=8)
    c8 = [np.ascontiguousarray(p) for p in PinnedSolver(s, M, hf[0], hf[1], h_rest=hf[2:]).c8]
    R8 = [np.ascontiguousarray(np.asarray(p)) for p in od_axpy(-1.0, *c8, *F8)]

    def ax8(a, x8, y8):
        return [np.ascontiguousarray(np.asarray(p)) for p in od_axpy(a, *x8, *y8)]

    def solve(b, transpose=False):
        x = s.olu_solve([np.ascontiguousarray(b)] + [zero] * 7, transpose)
        return np.asarray(x[0]) + np.asarray(x[1])
    V, hist = nn.subspace(solve, L, 2, its)
    sig = hist[-1]

    def parts_to_mp(parts, c):
        return mp.fsum(mp.mpf(float(p[c])) for p in parts)

    def dot8(a8, b8):
        return mp.fsum(parts_to_mp(a8, c) * parts_to_mp(b8, c) for c in range(L))
    uvec = []
    for i in range(2):
        x = s.olu_solve([np.ascontiguousarray(V[:, i])] + [zero] * 7, True)
        x = [np.ascontiguousarray(np.asarray(p)) for p in x]
        raw_v = [parts_to_mp(x, c) for c in range(L)]
        nr = mp.sqrt(mp.fsum(r * r for r in raw_v))
        uvec.append([r / nr for r in raw_v])

    def proj(i, X8):
        return mp.fsum(uvec[i][c] * parts_to_mp(X8, c) for c in range(L))

    def inv8(x8):
        y = s.olu_solve([np.ascontiguousarray(p) for p in x8], True)
        y = s.olu_solve([np.ascontiguousarray(np.asarray(p)) for p in y])
        return [np.ascontiguousarray(np.asarray(p)) for p in y]

    def deflate(y8, x8):
        for _ in range(8):
            c = dot8(x8, y8) / dot8(x8, x8)
            y8 = ax8(-float(c), x8, y8)
            if abs(dot8(x8, y8)) <= mp.mpf(10) ** -45 * mp.sqrt(dot8(y8, y8) * dot8(x8, x8)):
                break
        return y8

    def normalize(y8):
        return ax8(1.0 / float(np.linalg.norm(np.asarray(y8[0]))), y8, Z8)
    x1 = [np.ascontiguousarray(V[:, 0])] + [zero] * 7
    x2 = [np.ascontiguousarray(V[:, 1])] + [zero] * 7
    for _ in range(3):
        x1 = normalize(inv8(x1))
        x2 = normalize(deflate(inv8(x2), x1))
    x2 = deflate(x2, x1)
    vs = [x1, x2]
    print(f"sigma_1, sigma_2 {sig[0]:.6e}, {sig[1]:.6e}; v_1.v_2 {nstr(dot8(x1, x2), 3)}", flush=True)
    z8 = [np.ascontiguousarray(np.asarray(p)) for p in z]

    def at(combo, t=1.0):
        zt = z8
        for cf, v in combo:
            zt = ax8(cf * t, v, zt)
        Fx = s.residual_o([np.ascontiguousarray(p) for p in zt])
        return ax8(-1.0, c8, [np.ascontiguousarray(np.asarray(p)) for p in Fx])

    R0 = at([])
    a = [proj(0, R0), proj(1, R0)]
    print(f"a_1 = u_1.R {nstr(a[0], 10)}, a_2 = u_2.R {nstr(a[1], 10)}", flush=True)
    cache = {}

    def Gs(s1, s2):
        """(g_1, g_2) at z + s1 v_1 + s2 v_2 (floats)"""
        key = (float(s1), float(s2))
        if key not in cache:
            Rt = at([(key[0], vs[0]), (key[1], vs[1])])
            cache[key] = (proj(0, Rt), proj(1, Rt))
        return cache[key]

    def Gdir(th, t):
        thf = float(th)
        return Gs(t * float(mp.cos(th)), t * float(mp.sin(th)))
    if opts.get("q4_only") == "1":
        # the mutation check of Q4 (the planted control alone, the model coefficients read from --model_from): unmutated it must pass, with E_1 of the wrong sign it must fail
        mj = json.load(open(opts["model_from"]))
        Acoef = [[mp.mpf(x) for x in mj["Acoef1"]], [mp.mpf(x) for x in mj["Acoef2"]]]
        Ebase = [[mp.mpf(x) for x in mj["Ecoef1"]], [mp.mpf(x) for x in mj["Ecoef2"]]]
        ths_p, rho_p = mp.pi * 40 / 180, mp.mpf(1.5e-29)
        sp = (float(rho_p * mp.cos(ths_p)), float(rho_p * mp.sin(ths_p)))
        gz = Gs(*sp)
        apl = [a[i] - gz[i] for i in range(2)]

        def near(th, r):
            dth = abs((th - ths_p + mp.pi / 2) % mp.pi - mp.pi / 2)
            return max(dth / ths_p, abs(mp.sqrt(r) - rho_p) / rho_p)
        res = {}
        for mut in (False, True):
            Ecoef_s = [list(Ebase[0]), list(Ebase[1])]
            if mut:
                Ecoef_s[0] = [-x for x in Ecoef_s[0]]
            rts = model_roots(apl, Acoef, Ecoef_s)
            best = min((near(th, r) for th, r in rts), default=None)
            res[mut] = bool(best is not None and best <= 1e-3)
            print(f"Q4 {'MUTATED (E_1 sign)' if mut else 'unmutated'}: planted root (theta* 40 deg, rho* 1.5e-29), a_pl = ({nstr(apl[0], 5)}, {nstr(apl[1], 5)}): {len(rts)} model root(s); closest relative error {'none' if best is None else nstr(best, 3)}: {'pass' if res[mut] else 'FAIL'}", flush=True)
        okm = res[False] and not res[True]
        print(f"mutation check of Q4: unmutated {'pass' if res[False] else 'FAIL'}, mutated {'FAIL (as required)' if not res[True] else 'pass (the control did not fire)'}")
        print("check:", "pass" if okm else "FAIL")
        return 0 if okm else 1
    ctl = {}
    rec = dict(state=st, ks=ks, plan="stored" if keep_plan else "new", a=[nstr(x, 12) for x in a], controls={}, dirs=[])
    t1 = time.time()
    # the even parts
    tab = []
    q1ok = True
    print("\n| theta | A_1 | A_2 | E_1 | E_2 | F_1 | F_2 | worst fit misfit (Q1) |\n|---|---|---|---|---|---|---|---|", flush=True)
    for mm, th in enumerate(THETAS):
        ev = {e: [] for e in EXPS}
        for e in EXPS:
            t = float(f"1e{e}")
            gp, gm = Gdir(th, t), Gdir(th, -t)
            ev[e] = [(gp[i] + gm[i] - 2 * a[i]) / 2 for i in range(2)]
        coef, worst = [], mp.mpf(0)
        for i in range(2):
            ts = [mp.mpf(f"1e{e}") for e in EXPS]
            us = [t / mp.mpf("1e-26") for t in ts]                       # scaled variable, u = 1e-3 .. 1e2
            y = [ev[e][i] / t ** 2 for e, t in zip(EXPS, ts)]
            cu = fit_ls([[mp.mpf(1)] * len(us), [u ** 2 for u in us], [u ** 4 for u in us]], y)
            for u, yy in zip(us, y):
                big = max(abs(cu[0]), abs(cu[1] * u ** 2), abs(cu[2] * u ** 4))
                worst = max(worst, abs(cu[0] + cu[1] * u ** 2 + cu[2] * u ** 4 - yy) / big)
            coef.append([cu[0], cu[1] / mp.mpf("1e-52"), cu[2] / mp.mpf("1e-104")])      # A, E, F in t
        q1ok &= bool(worst <= 1e-3)
        tab.append(coef)
        print(f"| {float(th * 180 / mp.pi):g} | {nstr(coef[0][0], 3)} | {nstr(coef[1][0], 3)} | {nstr(coef[0][1], 5)} | {nstr(coef[1][1], 5)} | {nstr(coef[0][2], 3)} | {nstr(coef[1][2], 3)} | {nstr(worst, 2)} |", flush=True)
        rec["dirs"].append(dict(theta_deg=float(th * 180 / mp.pi), A=[nstr(coef[i][0], 8) for i in range(2)], E=[nstr(coef[i][1], 8) for i in range(2)], F=[nstr(coef[i][2], 8) for i in range(2)], misfit=nstr(worst, 3)))
    ctl["Q1"] = q1ok
    print(f"({len(cache)} residual evaluations, {time.time() - t1:.0f} s)", flush=True)
    # the forms
    Acoef, Ecoef, q2err = [], [], mp.mpf(0)
    for i in range(2):
        Ev = [tab[mm][i][1] for mm in range(12)]
        Av = [tab[mm][i][0] for mm in range(12)]
        cE = fit_ls([[quartic_basis(th)[k] for th in THETAS] for k in range(5)], Ev)
        cA = fit_ls([[quad_basis(th)[k] for th in THETAS] for k in range(3)], Av)
        Ecoef.append(cE)
        Acoef.append(cA)
        mx = max(abs(x) for x in Ev)
        q2err = max(q2err, max(abs(mp.fsum(c * b for c, b in zip(cE, quartic_basis(th))) - Ev[mm]) for mm, th in enumerate(THETAS)) / mx)
        print(f"E_{i + 1}(theta) = sum c_kl cos^k sin^l: c = [" + ", ".join(nstr(x, 5) for x in cE) + "]; A_" + str(i + 1) + " form coefficients [" + ", ".join(nstr(x, 3) for x in cA) + "]")
        rec[f"Ecoef{i + 1}"] = [nstr(x, 10) for x in cE]
        rec[f"Acoef{i + 1}"] = [nstr(x, 6) for x in cA]
    ctl["Q2"] = bool(q2err <= 1e-3)
    print(f"Q2 the quartic forms reproduce the twelve E_i within {nstr(q2err, 3)} of max |E_i|")
    ref = {(0, 0): -1.094e80, (1, 0): 8.083e78, (0, 6): -1.937e82, (1, 6): 4.311e81}
    q3 = max(abs(tab[mm][i][1] - mp.mpf(v)) / abs(v) for (i, mm), v in ref.items())
    ctl["Q3"] = bool(q3 <= 1e-2)
    print(f"Q3 axes against design 2's table: worst relative difference {nstr(q3, 3)}")
    # sign structure of E_1 over the circle
    ths = [mp.pi * k / 720 for k in range(720)]
    E1 = [mp.fsum(c * b for c, b in zip(Ecoef[0], quartic_basis(th))) for th in ths]
    E2 = [mp.fsum(c * b for c, b in zip(Ecoef[1], quartic_basis(th))) for th in ths]
    print(f"E_1(theta) over 720 directions: max {nstr(max(E1), 5)} at {float(ths[E1.index(max(E1))] * 180 / mp.pi):g} deg, min {nstr(min(E1), 5)}; E_2: max {nstr(max(E2), 5)}, min {nstr(min(E2), 5)}")
    rec["E1_max"], rec["E1_min"], rec["E2_max"], rec["E2_min"] = nstr(max(E1), 8), nstr(min(E1), 8), nstr(max(E2), 8), nstr(min(E2), 8)
    # solve
    Ecoef_s = [list(Ecoef[0]), list(Ecoef[1])]
    if mutate == "E1sign":
        Ecoef_s[0] = [-x for x in Ecoef_s[0]]
    roots = model_roots(a, Acoef, Ecoef_s)
    print(f"\nthe model system (even parts, odd terms 1e-8 and smaller of a_i at these sizes): {len(roots)} real root direction(s)", flush=True)
    for th, r in roots:
        print(f"  theta {float(th * 180 / mp.pi):.6f} deg, rho = {nstr(mp.sqrt(r), 8)}")
    rec["model_roots"] = [dict(theta_deg=float(th * 180 / mp.pi), rho=nstr(mp.sqrt(r), 12)) for th, r in roots]
    # Q4 planted through the true residual
    ths_p, rho_p = mp.pi * 40 / 180, mp.mpf(1.5e-29)
    sp = (float(rho_p * mp.cos(ths_p)), float(rho_p * mp.sin(ths_p)))
    gz = Gs(*sp)
    apl = [a[i] - gz[i] for i in range(2)]
    rts = model_roots(apl, Acoef, Ecoef_s)
    def near(th, r):
        dth = abs((th - ths_p + mp.pi / 2) % mp.pi - mp.pi / 2)
        return max(dth / ths_p, abs(mp.sqrt(r) - rho_p) / rho_p)
    best = min((near(th, r) for th, r in rts), default=None)
    ctl["Q4"] = bool(best is not None and best <= 1e-3)
    print(f"\nQ4 planted root (theta* 40 deg, rho* 1.5e-29), a_pl = ({nstr(apl[0], 5)}, {nstr(apl[1], 5)}): {len(rts)} model root(s); closest relative error {'none' if best is None else nstr(best, 3)}: {'pass' if ctl['Q4'] else 'FAIL'}", flush=True)
    rec["planted"] = dict(n=len(rts), err=None if best is None else nstr(best, 5), ok=bool(ctl["Q4"]))
    # Q5 Newton on the true weak map from every model root (both signs of s)
    ok5 = True
    rec["refined"] = []
    for th, r in roots:
        rho = mp.sqrt(r)
        for sgn in (1, -1):
            sv = [sgn * rho * mp.cos(th), sgn * rho * mp.sin(th)]
            for it in range(8):
                g0 = Gs(*sv)
                g0 = [g0[0], g0[1]]
                nrm = max(abs(g0[0] / a[0]), abs(g0[1] / a[1]))
                if nrm <= mp.mpf(10) ** -9:
                    break
                h = [max(abs(x), mp.mpf(10) ** -35) * mp.mpf("1e-4") for x in sv]
                Jm = mp.matrix(2, 2)
                for j in range(2):
                    sp_ = list(sv)
                    sp_[j] = sp_[j] + h[j]
                    gj = Gs(*sp_)
                    for i in range(2):
                        Jm[i, j] = (gj[i] - g0[i]) / h[j]
                ds = mp.lu_solve(Jm, mp.matrix([-g0[0], -g0[1]]))
                sv = [sv[0] + ds[0], sv[1] + ds[1]]
            g1 = Gs(*sv)
            nrm = max(abs(g1[0] / a[0]), abs(g1[1] / a[1]))
            ok5 &= bool(nrm <= 1e-6)
            print(f"Q5 root from theta {float(th * 180 / mp.pi):.3f} deg, sign {sgn:+d}: Newton on the true map ends at s = ({nstr(sv[0], 8)}, {nstr(sv[1], 8)}) with max |g_i/a_i| = {nstr(nrm, 3)}", flush=True)
            rec["refined"].append(dict(s=[nstr(sv[0], 12), nstr(sv[1], 12)], rel=nstr(nrm, 5)))
    if not roots:
        print("Q5 no model root to refine (vacuous)")
    ctl["Q5"] = ok5
    rec["controls"] = {k: bool(v) for k, v in ctl.items()}
    print("\ncontrols: " + ", ".join(f"{k} {'pass' if v else 'FAIL'}" for k, v in sorted(ctl.items())))
    ok = all(ctl.values())
    print("check:", "pass" if ok else "FAIL")
    if opts.get("json"):
        json.dump(rec, open(opts["json"], "w"), indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
