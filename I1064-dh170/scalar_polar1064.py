#!/usr/bin/env python3
"""#1064 part 2, design 4 (README, written before it ran): the polar sign map of the weak pair's true map G(s) = (u_1.R, u_2.R)(z + s_1 v_1 + s_2 v_2) at D 262.0099, ks 315.

    cd hp && python3 scalar_polar1064.py RAWDIR STATE --ks=K [--keep_plan=0|1] [--its=32] [--threads=4] [--json=OUT] [--design2=scan_ks315.json] [--mutate=shift]

Design 3 fitted the even part's quartic forms and found none negative-definite failing: E_1(theta) < 0 in all directions (max -1.6e78 near 166 degrees), but near that direction the quartic form is almost zero and a
sextic term, which design 3 could not determine (F came out at the fit's noise), can change the sign of g_1 at |s| ~ 1e-16. This design does not model: it evaluates G on a polar grid, theta = 0, 5, ..., 175 degrees (36 directions),
rho = 10^e, e = -20, -19, -18, -17.5, ..., -12 (14 radii), s = rho (cos theta, sin theta), both projections, and looks for the joint zeros directly.
Reading (README): along each direction the first sign change of g_i (from the sign of a_i, negative) among the radii, log-interpolated, gives rho_i(theta); a candidate joint root is a place between neighbouring directions where
both g_1 and g_2 have a sign change and ln(rho_1 / rho_2) changes sign; each candidate is refined by Newton on the true map (finite-difference Jacobian, mp) from the interpolated point and is a root of the pair when it ends with
max_i |g_i| / N_i <= 1e-10 (N_i the |g_i| at sqrt(10) times the radius).
Controls (exit 1 on failure):
  D1  plumbing: at theta = 0 and 90 degrees and e = -20 .. -12 (integers) G reproduces design 2's table (--design2 json) within 1e-6 relative;
  D2  planted joint root through the true residual: G_pl(s) = G(s) - G(s*), s* = 3e-17 (cos 45, sin 45) (an exact root of the pair G_pl): the same candidate finder (on the grid values minus G(s*)) must flag a candidate whose Newton
      refinement ends at s* within 1e-6 relative (the root can be located only to about 1e-16 relative, the evaluation point being rounded to doubles, so the success measure for a root of the data is the scaled residual
      max_i |g_i| / N_i <= 1e-10, N_i the |g_i| at sqrt(10) times the radius, not |g_i| <= 1e-6 |a_i|); --mutate=shift takes the shift 1.5 times too large: D2 must fail;
  D3  even dominance: G(-s) = G(s) within 1e-3 relative at theta = 0, 45, 90, 135 degrees and e = -16, -14 (the grid uses the + side only)."""
import json
import os
import sys
import time

import numpy as np

HP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("HP_DIR", HP))
import mpmath as mp  # noqa: E402

mp.mp.dps = 140


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
    ctl = {}
    rec = dict(state=st, ks=ks, plan="stored" if keep_plan else "new", a=[nstr(x, 12) for x in a], controls={})
    EXP = [-20, -19, -18] + [-18 + 0.5 * k for k in range(1, 13)]
    THD = [5 * m for m in range(36)]
    rad = {e: mp.mpf(10) ** mp.mpf(str(e)) for e in EXP}

    def Gp(thd, e, sgn=1):
        th = mp.pi * thd / 180
        r = sgn * rad[e]
        return Gs(float(r * mp.cos(th)), float(r * mp.sin(th)))
    t1 = time.time()
    grid = {}
    if opts.get("grid_from"):
        # the mutation run of D2: the grid read from an earlier run's json (8 digits), D2 evaluates the true map only at s* and in Newton
        gj = json.load(open(opts["grid_from"]))["grid"]
        for thd in THD:
            for e in EXP:
                grid[(thd, e)] = tuple(mp.mpf(x) for x in gj[f"{thd}"][f"{e:g}"])
        print(f"grid read from {opts['grid_from']}", flush=True)
    else:
        print("\n| theta | " + " | ".join(f"g_1 at e={e:g}" for e in EXP[::2]) + " |\n|---|" + "---|" * len(EXP[::2]), flush=True)
        for thd in THD:
            for e in EXP:
                grid[(thd, e)] = Gp(thd, e)
            print(f"| {thd} | " + " | ".join(nstr(grid[(thd, e)][0], 3) for e in EXP[::2]) + " |", flush=True)
    print(f"({len(cache)} residual evaluations, {time.time() - t1:.0f} s)", flush=True)
    rec["grid"] = {f"{thd}": {f"{e:g}": [nstr(grid[(thd, e)][0], 8), nstr(grid[(thd, e)][1], 8)] for e in EXP} for thd in THD}

    def first_change(vals, ref_sign):
        """smallest index k with sign(vals[k]) != ref_sign, or None"""
        for k, v in enumerate(vals):
            if (v > 0) != (ref_sign > 0):
                return k
        return None

    def candidates(shift=(0, 0), a_ref=None):
        """per direction the radii rho_1, rho_2 of the first sign change (log-interpolated, None when absent) of g_i - shift_i, then candidate cells"""
        ar = a_ref if a_ref is not None else [a[0] - shift[0], a[1] - shift[1]]
        rows = []
        for thd in THD:
            rr = []
            for i in range(2):
                vals = [grid[(thd, e)][i] - shift[i] for e in EXP]
                k = first_change(vals, ar[i])
                if k is None:
                    rr.append(None)
                elif k == 0:
                    rr.append(mp.mpf(10) ** EXP[0] / 2)
                else:
                    e0, e1 = EXP[k - 1], EXP[k]
                    v0, v1 = vals[k - 1], vals[k]
                    f = v0 / (v0 - v1)
                    rr.append(mp.mpf(10) ** (mp.mpf(str(e0)) + f * (mp.mpf(str(e1)) - mp.mpf(str(e0)))))
            rows.append(rr)
        cands = []
        for m in range(len(THD)):
            m2 = (m + 1) % len(THD)
            if all(rows[m][i] is not None and rows[m2][i] is not None for i in range(2)):
                d0 = mp.log(rows[m][0] / rows[m][1])
                d1 = mp.log(rows[m2][0] / rows[m2][1])
                if (d0 > 0) != (d1 > 0):
                    w = d0 / (d0 - d1)
                    thd_c = THD[m] + w * 5
                    rho_c = mp.exp(mp.log(rows[m][0]) * (1 - w) + mp.log(rows[m2][0]) * w)
                    cands.append((thd_c, rho_c))
        return rows, cands

    def newton(seed, shift=(0, 0), a_ref=None, maxit=40):
        """damped Newton on the true map G - shift in polar coordinates (theta, u = ln rho) for h_i = (g_i - shift_i) / rho^4 (finite-difference Jacobian, step 1e-10, step halving on max_i |h_i|). The evaluation point is rounded to
        doubles (at() takes float coefficients), so the root is located to about 1e-16 relative; the returned scaled residual is max_i |g_i| / N_i with N_i = |g_i - shift_i| at sqrt(10) times the final radius."""
        th, u = mp.atan2(seed[1], seed[0]), mp.log(mp.sqrt(seed[0] ** 2 + seed[1] ** 2))

        def pt(th_, u_):
            r = mp.exp(u_)
            return [r * mp.cos(th_), r * mp.sin(th_)], r

        def gg(th_, u_):
            xy, r = pt(th_, u_)
            g = Gs(*xy)
            return [g[0] - shift[0], g[1] - shift[1]], r

        def hh(g, r):
            return [g[0] / r ** 4, g[1] / r ** 4]
        g0, r0 = gg(th, u)
        h0 = hh(g0, r0)
        for it in range(maxit):
            nrm0 = max(abs(h0[0]), abs(h0[1]))
            if nrm0 == 0:
                break
            hs = mp.mpf("1e-10")
            Jm = mp.matrix(2, 2)
            for j, (dth, du) in enumerate(((hs, 0), (0, hs))):
                gj, rj = gg(th + dth, u + du)
                hj = hh(gj, rj)
                for i in range(2):
                    Jm[i, j] = (hj[i] - h0[i]) / hs
            ds = mp.lu_solve(Jm, mp.matrix([-h0[0], -h0[1]]))
            lam, acc = mp.mpf(1), False
            while lam > mp.mpf(10) ** -8:
                gt, rt = gg(th + lam * ds[0], u + lam * ds[1])
                ht = hh(gt, rt)
                if max(abs(ht[0]), abs(ht[1])) < nrm0:
                    th, u, g0, r0, h0, acc = th + lam * ds[0], u + lam * ds[1], gt, rt, ht, True
                    break
                lam /= 2
            if not acc:
                break
        xy, r = pt(th, u)
        gN = Gs(xy[0] * mp.sqrt(10), xy[1] * mp.sqrt(10))
        N = [abs(gN[0] - shift[0]), abs(gN[1] - shift[1])]
        return xy, g0, max(abs(g0[0]) / N[0], abs(g0[1]) / N[1])

    rows, cands = candidates()
    print("\nfirst sign change of g_i along each direction (rho_1, rho_2; '-' = none up to 1e-12):")
    for thd, rr in zip(THD, rows):
        print(f"  theta {thd:3d}: " + ", ".join("-" if x is None else nstr(x, 4) for x in rr))
    rec["first_change"] = {f"{thd}": [None if x is None else nstr(x, 6) for x in rr] for thd, rr in zip(THD, rows)}
    print(f"\ncandidates (both g_i change sign and ln(rho_1/rho_2) changes sign between neighbouring directions): {len(cands)}", flush=True)
    found = []
    rec["roots"] = []
    for thd_c, rho_c in cands:
        th = mp.pi * thd_c / 180
        seed = [rho_c * mp.cos(th), rho_c * mp.sin(th)]
        sv, gend, rel = newton(seed)
        okr = bool(rel <= 1e-10)
        print(f"  candidate near theta {float(thd_c):.2f} deg, rho {nstr(rho_c, 4)}: Newton ends at s = ({nstr(sv[0], 8)}, {nstr(sv[1], 8)}), |s| {nstr(mp.sqrt(sv[0] ** 2 + sv[1] ** 2), 6)}, scaled residual max_i |g_i|/N_i {nstr(rel, 3)} (|g_i| {nstr(abs(gend[0]), 3)}, {nstr(abs(gend[1]), 3)}; N_i the |g_i| at sqrt(10) times the radius): {'a root of the pair' if okr else 'did not converge'}", flush=True)
        rec["roots"].append(dict(theta0=float(thd_c), rho0=nstr(rho_c, 8), s=[nstr(sv[0], 12), nstr(sv[1], 12)], rel=nstr(rel, 5), root=okr))
        if okr:
            found.append(sv)
    # D1
    d1 = None
    if opts.get("design2"):
        d2 = json.load(open(opts["design2"]))["scan"]
        worst = mp.mpf(0)
        for key, thd in (("v1", 0), ("v2", 90)):
            for r in d2[key]:
                if -20 <= r["e"] <= -12:
                    gp = Gp(thd, r["e"]) if r["e"] in rad else Gs(float(mp.mpf(10) ** r["e"] * mp.cos(mp.pi * thd / 180)), float(mp.mpf(10) ** r["e"] * mp.sin(mp.pi * thd / 180)))
                    for i in range(2):
                        ref = mp.mpf(r["gp"][i])
                        worst = max(worst, abs(gp[i] - ref) / abs(ref))
        d1 = worst
        ctl["D1"] = bool(worst <= 1e-6)
        print(f"\nD1 against design 2's table (theta 0 and 90, e = -20 .. -12): worst relative difference {nstr(worst, 3)}", flush=True)
    # D3
    w3 = mp.mpf(0)
    for thd in (0, 45, 90, 135):
        for e in (-16, -14):
            gp, gm = Gp(thd, e), Gp(thd, e, -1)
            for i in range(2):
                w3 = max(w3, abs(gp[i] - gm[i]) / abs(gp[i]))
    ctl["D3"] = bool(w3 <= 1e-3)
    print(f"D3 G(-s) against G(s) at theta 0, 45, 90, 135 and e = -16, -14: worst relative difference {nstr(w3, 3)}", flush=True)
    # D2 planted (with --grid_from: both the unmutated and the shifted-by-1.5 variants, the mutation check: unmutated must pass, mutated must fail)
    thp, rhop = mp.pi / 4, mp.mpf("3e-17")
    sstar = (float(rhop * mp.cos(thp)), float(rhop * mp.sin(thp)))
    gst = Gs(*sstar)

    def planted(mut):
        f = mp.mpf("1.5") if mut else 1
        shift = [gst[0] * f, gst[1] * f]
        rowsp, candp = candidates(shift=shift, a_ref=[a[0] - shift[0], a[1] - shift[1]])
        hit = []
        for thd_c, rho_c in candp:
            th = mp.pi * thd_c / 180
            sv, gend, relp = newton([rho_c * mp.cos(th), rho_c * mp.sin(th)], shift=shift)
            err = max(abs(sv[0] - sstar[0]) / abs(sstar[0]), abs(sv[1] - sstar[1]) / abs(sstar[1]))
            okc = bool(err <= 1e-6)
            print(f"D2 planted s* = 3e-17 (cos 45, sin 45), shift G(s*){' x1.5 (MUTATED)' if mut else ''}: candidate near theta {float(thd_c):.2f}, rho {nstr(rho_c, 4)} -> Newton s = ({nstr(sv[0], 8)}, {nstr(sv[1], 8)}), relative error vs s* {nstr(err, 3)}: {'found' if okc else 'no'}", flush=True)
            if okc:
                hit.append(sv)
        print(f"D2 planted joint root{' (MUTATED)' if mut else ''}: {len(candp)} candidate(s), {'recovered' if hit else 'NOT recovered'}", flush=True)
        return bool(hit)
    if opts.get("grid_from"):
        r0, r1 = planted(False), planted(True)
        ctl["D2 mutation check (unmutated passes, mutated fails)"] = bool(r0 and not r1)
    else:
        ctl["D2"] = planted(opts.get("mutate") == "shift")
    rec["controls"] = {k: bool(v) for k, v in ctl.items()}
    print("\ncontrols: " + ", ".join(f"{k} {'pass' if v else 'FAIL'}" for k, v in sorted(ctl.items())))
    ok = all(ctl.values())
    print("check:", "pass" if ok else "FAIL")
    if opts.get("json"):
        json.dump(rec, open(opts["json"], "w"), indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
