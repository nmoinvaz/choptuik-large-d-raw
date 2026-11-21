#!/usr/bin/env python3
"""#1064 part 3 (README, written before it ran): the Lyapunov-Schmidt reduced function of the weak pair at D 262.0099, ks 315.

    cd hp && python3 ls1064.py RAWDIR STATE --ks=K [--keep_plan=0|1] [--its=32] [--threads=4] [--axes=1,2] [--emin=-30] [--emax=-10] [--estep=0.5]
                  [--tstar=1e-25] [--frozen=scan_ks315.json] [--json=OUT] [--mutate=shift|noproj]

The weak pair (v_1, v_2: the two smallest singular values of J(z_0), sigma_1 = 6.4e-21, sigma_2 = 2.1e-20) is held at z_0 + t v_j; the strong rows (all rows except u_1, u_2) are solved for w orthogonal to v_1, v_2 by a
chord through the octo-double LU of J(z_0) (octo_corrector.chord_strong's scheme, projection done to octo-double), z = z_0 + t v_j + w; the reduced function is g_i(t) = u_i . R(z), i = 1, 2.
See the README (part 3) for the grid, the convergence and failure rules, the controls and the readings, all fixed before the run."""
import json
import os
import sys
import time
import types

import numpy as np
import mpmath as mp

mp.mp.dps = 140
HP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("HP_DIR", HP))
TOLW = mp.mpf(10) ** -55          # |v_j . x| after the weak removal
TOL_RS, TOL_DW, TOL_G, TOL_DW_G = 1e-45, 1e-55, 1e-6, 1e-30
IT_MAX = 25


def nstr(x, n=5):
    return mp.nstr(x, n)


def parts_to_mp(parts, c):
    return mp.fsum(mp.mpf(float(p[c])) for p in parts)


def setup(raw, st, ks, keep_plan="0", threads=4, its=32):
    """near_null's pinned system at the state's kfreeze with the horizon series to order ks (plan made again when ks differs), one octo-double LU, the weak pair refined in eight parts; returns a namespace"""
    from hpkernel.driver import make_solver
    from octo_corrector import load_o
    import near_null as nn
    from multidouble import od_axpy
    from pinning import PinnedSolver, band_coeffs, band_field
    z, m = load_o(os.path.join(raw, st))
    z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
    M, nodes = int(m["M"]), list(m["nodes"])
    D = m.get("D_str", repr(float(m["D"])))
    kf = int(m.get("kfreeze", 3))
    s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=ks, threads=threads, kfreeze=kf)
    kp = keep_plan == "1" and "segs" in m and ks == m.get("ks", 130)
    s.set_segs(m["segs"] if kp else s.plan(z[0], z[1], 1e-32, 0.05))
    print(f"{st}: D {float(m['D']):g}, ks {ks} (the state's {m.get('ks', 130)}), plan {'stored' if kp else 'made again'}, M {M}, kfreeze {kf}", flush=True)
    L = len(z[0])
    zero = np.zeros(L)
    Z8 = [zero] * 8
    t0 = time.time()
    keep = hasattr(s, "jacobian_o_kept")
    out = s.newton_o(z, keep_jacobian=True) if keep else s.newton_o(z)
    print(f"L = {L}; octo-double LU {time.time() - t0:.0f} s, pivots {out[3]:.1e}..{out[4]:.1e}", flush=True)
    F8 = s.newton_o_residual(z) if hasattr(s, "newton_o_residual") else s.residual_o(z)
    F8 = [np.ascontiguousarray(np.asarray(p)) for p in F8]
    ks_held = [h for h in range(kf + 1, 14) if h % 2 == 1]
    hc = band_coeffs(z[0][:M], z[1][:M], M, ks_held, exact=True, rest=[p[:M] for p in z[2:]])
    hf = band_field(hc, ks_held, M, parts=8)
    c8 = [np.ascontiguousarray(p) for p in PinnedSolver(s, M, hf[0], hf[1], h_rest=hf[2:]).c8]

    def ax8(a, x8, y8):
        return [np.ascontiguousarray(np.asarray(p)) for p in od_axpy(a, *x8, *y8)]
    R8 = ax8(-1.0, c8, F8)

    def solve(b, transpose=False):
        x = s.olu_solve([np.ascontiguousarray(b)] + [zero] * 7, transpose)
        return np.asarray(x[0]) + np.asarray(x[1])
    V, hist = nn.subspace(solve, L, 3, its)
    sig = hist[-1]
    ctx = types.SimpleNamespace(s=s, L=L, zero=zero, Z8=Z8, ax8=ax8, c8=c8, sig_f=sig, od_axpy=od_axpy, raw=raw, st=st, ks=ks, keep_plan=kp, m=m)
    ctx.z8 = [np.ascontiguousarray(np.asarray(p)) for p in z]
    # u_i = J^-T v_i normalized (mp); sigma_i = 1 / its norm
    uvec, sgm = [], []
    for i in range(2):
        x = s.olu_solve([np.ascontiguousarray(V[:, i])] + [zero] * 7, True)
        x = [np.ascontiguousarray(np.asarray(p)) for p in x]
        rv = [parts_to_mp(x, c) for c in range(L)]
        nr = mp.sqrt(mp.fsum(r * r for r in rv))
        uvec.append([r / nr for r in rv])
        sgm.append(1 / nr)
    ctx.uvec, ctx.sg = uvec, sgm

    def dot8(a8, b8):
        return mp.fsum(parts_to_mp(a8, c) * parts_to_mp(b8, c) for c in range(L))

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
    ctx.vs = [x1, x2]
    ctx.vm = [[parts_to_mp(v, c) for c in range(L)] for v in ctx.vs]
    ctx.um8 = [mp_to_8(ctx, u) for u in uvec]
    ctx.R8 = R8
    ctx.a = [mp.fsum(uvec[i][c] * parts_to_mp(R8, c) for c in range(L)) for i in range(2)]
    print(f"sigma_1, sigma_2 from ||J^-T v||: {nstr(sgm[0], 10)}, {nstr(sgm[1], 10)}; a_1 = u_1.R {nstr(ctx.a[0], 10)}, a_2 = u_2.R {nstr(ctx.a[1], 10)}; "
          f"v_1.v_2 {nstr(dot8(x1, x2), 3)}, u_1.u_2 {nstr(mp.fsum(a * b for a, b in zip(*uvec)), 3)}", flush=True)
    return ctx


def mp_to_8(ctx, vec):
    """an mp vector as eight non-overlapping float parts (successive rounding)"""
    parts = [np.zeros(ctx.L) for _ in range(8)]
    rem = list(vec)
    for q in range(8):
        for c in range(ctx.L):
            f = float(rem[c])
            parts[q][c] = f
            if f != 0.0:
                rem[c] = rem[c] - mp.mpf(f)
    return parts


def resid(ctx, zc):
    Fx = ctx.s.residual_o([np.ascontiguousarray(p) for p in zc])
    return ctx.ax8(-1.0, ctx.c8, [np.ascontiguousarray(np.asarray(p)) for p in Fx])


def strong_step(ctx, R, mutate=""):
    """x = J^-1 P_strong R: the weak part of r is removed by iterating r <- r - sum_j sigma_j (v_j . x) u_j until |v_j . x| <= TOLW; returns (x, projected r, passes). With mutate 'noproj' x = J^-1 R, nothing removed."""
    L = ctx.L
    r = R
    cj = [mp.mpf(0), mp.mpf(0)]
    passes = 0
    for passes in range(1, 17):
        x = [np.ascontiguousarray(np.asarray(p)) for p in ctx.s.olu_solve([np.ascontiguousarray(p) for p in r])]
        if mutate == "noproj":
            return x, r, passes
        xm = [parts_to_mp(x, c) for c in range(L)]
        cj = [mp.fsum(ctx.vm[j][c] * xm[c] for c in range(L)) for j in range(2)]
        if max(abs(cj[0]), abs(cj[1])) <= TOLW:
            break
        for j in range(2):
            r = ctx.ax8(-float(ctx.sg[j] * cj[j]), ctx.um8[j], r)
    for j in range(2):
        x = ctx.ax8(-float(cj[j]), ctx.vs[j], x)
    return x, r, passes


def omax8(x):
    return float(np.abs(np.asarray(x[0]) + np.asarray(x[1])).max())


def solve_point(ctx, weak, w=None, mutate="", it_max=IT_MAX, verbose=False):
    """the strong rows at the weak displacement weak = [(coefficient, v8), ...]: z = z_0 + weak + w, w from `w` (eight parts, or None for 0). Returns (w, info) with info = dict(ok, why, its, g, rs, dw, delta, hist)"""
    L = ctx.L
    zw = ctx.z8
    for cf, v in weak:
        zw = ctx.ax8(cf, v, zw)
    if w is None:
        w = [ctx.zero.copy() for _ in range(8)]
    hist, gprev, grow = [], None, 0
    ok, why = False, "it_max"
    g = None
    w_start = w
    for it in range(1, it_max + 1):
        zc = ctx.ax8(1.0, w, zw)
        R = resid(ctx, zc)
        rm = [parts_to_mp(R, c) for c in range(L)]
        g = [mp.fsum(ctx.uvec[i][c] * rm[c] for c in range(L)) for i in range(2)]
        xs, r, passes = strong_step(ctx, R, mutate)
        dw, rs = omax8(xs), omax8(r)
        hist.append((it, rs, dw, passes))
        if verbose:
            print(f"      it {it}: |P R| {rs:.2e}, |dw| {dw:.3e}, passes {passes}, g_1 {nstr(g[0], 4)}, g_2 {nstr(g[1], 4)}", flush=True)
        if not np.isfinite(dw) or not np.isfinite(rs):
            ok, why = False, "not finite"
            break
        if dw > 1.0:
            ok, why = False, "diverged (|dw| > 1)"
            break
        if rs <= TOL_RS:
            ok, why = True, "strong residual"
            break
        if dw <= TOL_DW:
            ok, why = True, "|dw|"
            break
        if it >= 3 and gprev is not None and dw <= TOL_DW_G and all(abs(g[i] - gprev[i]) <= TOL_G * abs(g[i]) for i in range(2)):
            ok, why = True, "g stable"
            break
        if len(hist) >= 2 and dw > 4 * hist[-2][2]:
            grow += 1
            if grow >= 2:
                ok, why = False, "|dw| grows"
                break
        else:
            grow = 0
        gprev = g
        w = ctx.ax8(-1.0, xs, w)
    if why in ("not finite", "diverged (|dw| > 1)"):
        w = w_start
    zc = ctx.ax8(1.0, w, zw)
    delta = mp.fsum(mp.mpf(float(p[-1])) for p in zc)
    return w, dict(ok=ok, why=why, its=len(hist), g=g, rs=hist[-1][1], dw=hist[-1][2], delta=delta, hist=hist)


def lam_scan(ctx, kmax=8):
    """information: the residual along the strong chord step at t = 0, z_0 - lambda x, lambda = 1e-12 .. 1: max|R| and u_k . R for k = 1 .. kmax (u_k from the subspace iteration, the transposed solve)"""
    import near_null as nn
    L = ctx.L
    zero = ctx.zero

    def solve(b, transpose=False):
        x = ctx.s.olu_solve([np.ascontiguousarray(b)] + [zero] * 7, transpose)
        return np.asarray(x[0]) + np.asarray(x[1])
    V, hist = nn.subspace(solve, L, kmax, 32)
    sig = hist[-1]
    uk = []
    for i in range(kmax):
        x = ctx.s.olu_solve([np.ascontiguousarray(V[:, i])] + [zero] * 7, True)
        x = [np.ascontiguousarray(np.asarray(p)) for p in x]
        rv = [parts_to_mp(x, c) for c in range(L)]
        nr = mp.sqrt(mp.fsum(a * a for a in rv))
        uk.append([a / nr for a in rv])

    def pk(X8):
        xm = [parts_to_mp(X8, c) for c in range(L)]
        return [mp.fsum(uk[i][c] * xm[c] for c in range(L)) for i in range(kmax)]
    R0 = resid(ctx, ctx.z8)
    xs, r, passes = strong_step(ctx, R0)
    dwm = [parts_to_mp(xs, c) for c in range(L)]
    print(f"strong chord step at t = 0: max|dw| {omax8(xs):.3e}; sigma_1..{kmax}: " + " ".join(f"{x:.3e}" for x in sig))
    print(f"u_k . R(z_0), k = 1..{kmax}: " + " ".join(nstr(v, 4) for v in pk(R0)))
    print(f"v_k . dw, k = 1..{kmax}: " + " ".join(nstr(mp.fsum(mp.mpf(float(V[c, i])) * dwm[c] for c in range(L)), 4) for i in range(kmax)))
    rows = []
    print("| lambda | max abs R(z_0 - lambda x) | max abs R / lambda^2 | u_k.R, k = 1.." + str(kmax) + " |\n|---|---|---|---|")
    for e in range(-12, 1):
        lam = float(f"1e{e}")
        R = resid(ctx, ctx.ax8(-lam, xs, ctx.z8))
        pm = pk(R)
        rmax = omax8(R)
        print(f"| 1e{e} | {rmax:.3e} | {rmax / lam ** 2:.3e} | " + " ".join(nstr(v, 3) for v in pm) + " |", flush=True)
        rows.append(dict(e=e, rmax=rmax, uk=[nstr(v, 6) for v in pm]))
    return rows


def fl(sg, e):
    return sg * float(mp.mpf(10) ** mp.mpf(str(e)))


def sgn(x):
    return 1 if x > 0 else -1


def run(ctx, opts):
    mutate = opts.get("mutate", "")
    axes = [int(x) for x in opts.get("axes", "1,2").split(",")]
    emin, emax, estep = float(opts.get("emin", -30)), float(opts.get("emax", -10)), float(opts.get("estep", 0.5))
    EXPS = [round(emin + k * estep, 6) for k in range(int(round((emax - emin) / estep)) + 1)]
    rec = dict(state=ctx.st, ks=ctx.ks, plan="stored" if ctx.keep_plan else "new", a=[nstr(x, 12) for x in ctx.a], sigma=[nstr(x, 12) for x in ctx.sg], points=[], controls={}, grid=EXPS)
    t_all = time.time()
    # the start: t = 0
    w0, i0 = solve_point(ctx, [], None, "")
    print(f"t = 0: {'converged' if i0['ok'] else 'FAILED'} ({i0['why']}, {i0['its']} steps): |P R| {i0['rs']:.2e}, |dw| {i0['dw']:.2e}; g_1(0) = {nstr(i0['g'][0], 6)}, g_2(0) = {nstr(i0['g'][1], 6)} (a_1 {nstr(ctx.a[0], 6)}, a_2 {nstr(ctx.a[1], 6)}); Delta {nstr(i0['delta'], 20)}", flush=True)
    rec["t0"] = dict(ok=i0["ok"], why=i0["why"], its=i0["its"], g=[nstr(x, 10) for x in i0["g"]], rs=i0["rs"], dw=i0["dw"], delta=nstr(i0["delta"], 25), hist=i0["hist"])
    cache = {}
    ctx.cache = cache
    if opts.get("t0_only") == "1":
        ctx.rec, ctx.i0, ctx.w0, ctx.EXPS = rec, i0, w0, EXPS
        for it, rs, dw, ps in i0["hist"]:
            print(f"  t = 0 step {it}: |P R| {rs:.3e}, |dw| {dw:.3e}, passes {ps}")
        if opts.get("lam") == "1":
            rec["lam_scan"] = lam_scan(ctx)
        return rec
    for ax in axes:
        j = ax - 1
        print(f"\nreduced function along v_{ax}: | e | t | solve | steps | |P R| | |dw| | g_1 | g_2 | Delta - Delta_0 |", flush=True)
        for side in (1, -1):
            w = w0
            fails = 0
            stopped = None
            for e in EXPS:
                t = fl(side, e)
                if stopped:
                    rec["points"].append(dict(ax=ax, e=e, t=t, ok=None, why="not attempted (" + stopped + ")"))
                    continue
                w1, info = solve_point(ctx, [(t, ctx.vs[j])], w, mutate)
                cache[(ax, t)] = (w1 if info["ok"] else None, info)
                print(f"| {e:g} | {t:+.3e} | {'ok ' + info['why'] if info['ok'] else 'FAILED ' + info['why']} | {info['its']} | {info['rs']:.2e} | {info['dw']:.2e} | {nstr(info['g'][0], 5)} | {nstr(info['g'][1], 5)} | {nstr(info['delta'] - i0['delta'], 5)} |", flush=True)
                rec["points"].append(dict(ax=ax, e=e, t=t, ok=info["ok"], why=info["why"], its=info["its"], rs=info["rs"], dw=info["dw"], g=[nstr(x, 10) for x in info["g"]], ddelta=nstr(info["delta"] - i0["delta"], 10), hist=info["hist"]))
                if info["ok"]:
                    w, fails = w1, 0
                else:
                    fails += 1
                    if fails >= 2:
                        stopped = f"two failed solves in a row up to e = {e:g}"
                        print(f"  side {'+' if side > 0 else '-'} along v_{ax}: stopped, {stopped}", flush=True)
    print(f"\nscan: {len(cache)} strong solves, {time.time() - t_all:.0f} s", flush=True)
    if opts.get("lam") == "1":
        rec["lam_scan"] = lam_scan(ctx)
    ctx.rec, ctx.i0, ctx.w0, ctx.EXPS = rec, i0, w0, EXPS
    return rec


def sign_changes(ctx, ax, i):
    """sign changes of the reduced g_i along v_ax between neighbouring converged grid points on one side (and from t = 0): list of (side, t_lo, t_hi)"""
    out = []
    j = ax - 1
    for side in (1, -1):
        prev_t, prev_g = 0.0, ctx.i0["g"][i]
        for e in ctx.EXPS:
            t = fl(side, e)
            ent = ctx.cache.get((ax, t))
            if ent is None or not ent[1]["ok"]:
                prev_t, prev_g = None, None
                continue
            g = ent[1]["g"][i]
            if prev_g is not None and (g > 0) != (prev_g > 0):
                out.append((side, prev_t, t))
            prev_t, prev_g = t, g
    return out


def bisect_root(ctx, ax, i, side, t_lo, t_hi, shift=0, mutate="", tol=1e-9):
    """log bisection on |t| of g_i(t) - shift with a fresh strong solve at each trial, warm start from the lower converged point; returns (t*, w*, info*) or None when a solve fails"""
    ent = ctx.cache.get((ax, t_lo)) if t_lo != 0.0 else (ctx.w0, ctx.i0)
    w_lo = ent[0]
    lo, hi = abs(t_lo), abs(t_hi)
    g_lo = ent[1]["g"][i] - shift
    last = (None, None)
    if lo == 0.0:
        lo = hi * 1e-3
        wl, il = solve_point(ctx, [(side * lo, ctx.vs[ax - 1])], w_lo, mutate)
        if not il["ok"]:
            return None
        w_lo, g_lo = wl, il["g"][i] - shift
    while hi / lo - 1 > tol:
        mid = (lo * hi) ** 0.5
        wm, im = solve_point(ctx, [(side * mid, ctx.vs[ax - 1])], w_lo, mutate)
        if not im["ok"]:
            return None
        gm = im["g"][i] - shift
        last = (wm, im)
        if (gm > 0) == (g_lo > 0):
            lo, g_lo, w_lo = mid, gm, wm
        else:
            hi = mid
    return side * (lo * hi) ** 0.5, last[0], last[1]


def planted(ctx, opts, ax=1, i=0):
    """L1: g_pl(t) = g_i(t) - c, c = g_i(t*) (the weak row shifted, the strong rows unchanged): the sign change around t* from the cached scan values, then bisection with fresh strong solves; must return t* to 1e-6. L1b: the strong solve at t* from w = 0 reproduces the continuation's g_i to 1e-6"""
    tstar = float(opts.get("tstar", 1e-25))
    j = ax - 1
    ent = ctx.cache.get((ax, tstar))
    if ent is None:
        w = ctx.w0
        ent_w, info = solve_point(ctx, [(tstar, ctx.vs[j])], w)
        ent = (ent_w, info)
    if not ent[1]["ok"]:
        print("L1: the strong solve at t* failed; the control cannot run (reported)", flush=True)
        return None
    c = ent[1]["g"][i] * (mp.mpf("1.5") if opts.get("mutate") == "shift" else 1)
    # bracket from the scan: the grid points around t* on the + side, shifted
    pts = [(fl(1, e), ctx.cache.get((ax, fl(1, e)))) for e in ctx.EXPS]
    pts = [(t, en) for t, en in pts if en is not None and en[1]["ok"]]
    br = None
    prev = (0.0, ctx.i0["g"][i] - c, ctx.w0)
    for t, en in pts:
        g = en[1]["g"][i] - c
        if (g > 0) != (prev[1] > 0):
            br = (prev[0], t)
            break
        prev = (t, g, en[0])
    res = None
    if br is not None:
        t_lo, t_hi = br
        ent_lo = ctx.cache.get((ax, t_lo)) if t_lo != 0.0 else (ctx.w0, ctx.i0)
        res = bisect_root(ctx, ax, i, 1, t_lo, t_hi, shift=c, mutate="")
    ok1 = bool(res is not None and abs(res[0] - tstar) / tstar <= 1e-6)
    print(f"L1 planted reduced root t* = {tstar:.1e} along v_{ax} (g_{i + 1}(t*) = {nstr(ent[1]['g'][i], 6)}{', x1.5 (MUTATE)' if opts.get('mutate') == 'shift' else ''}): bracket {'none' if br is None else f'({br[0]:.2e}, {br[1]:.2e})'}; "
          f"returned {'none' if res is None else f'{res[0]:.9e}'}: {'pass' if ok1 else 'FAIL'}", flush=True)
    # L1b: cold start at t*
    wc, ic = solve_point(ctx, [(tstar, ctx.vs[j])], None)
    rel = abs(ic["g"][i] - ent[1]["g"][i]) / abs(ent[1]["g"][i]) if ic["ok"] else None
    ok1b = bool(ic["ok"] and rel <= 1e-6)
    print(f"L1b the strong solve at t* from w = 0 ({ic['why']}, {ic['its']} steps) gives g_{i + 1} = {nstr(ic['g'][i], 8)} against the continuation's {nstr(ent[1]['g'][i], 8)}: relative difference {'n/a' if rel is None else nstr(rel, 3)}: {'pass' if ok1b else 'FAIL'}", flush=True)
    return ok1, ok1b


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if len(args) < 2 or "ks" not in opts:
        sys.exit(__doc__)
    ctx = setup(args[0], args[1], int(opts["ks"]), opts.get("keep_plan", "0"), int(opts.get("threads", 4)), int(opts.get("its", 32)))
    rec = run(ctx, opts)
    if opts.get("t0_only") == "1":
        if opts.get("json"):
            json.dump(rec, open(opts["json"], "w"), indent=1, default=str)
        return 0
    ctl = {}
    ax_run = [int(x) for x in opts.get("axes", "1,2").split(",")]
    if 1 in ax_run:
        pl = planted(ctx, opts)
        if pl is not None:
            ctl["L1"], ctl["L1b"] = pl
        else:
            ctl["L1"] = False        # the planted control could not run: reported as a failed check
        # L2: no weak projection must not reproduce the projected solve
        tt = float(opts.get("tstar", 1e-25))
        wa, ia = solve_point(ctx, [(tt, ctx.vs[0])], None)
        wb, ib = solve_point(ctx, [(tt, ctx.vs[0])], None, "noproj")
        same = bool(ib["ok"] and ia["ok"] and abs(ib["g"][0] - ia["g"][0]) <= 1e-6 * abs(ia["g"][0]))
        ctl["L2"] = not same
        print(f"L2 t = {tt:.0e} along v_1: projected {ia['why']} g_1 = {nstr(ia['g'][0], 8)}; without the weak projection {'ok' if ib['ok'] else 'FAILED'} ({ib['why']}, {ib['its']} steps) g_1 = {nstr(ib['g'][0], 8)}: {'fires (differs or fails)' if ctl['L2'] else 'DOES NOT FIRE'}", flush=True)
    # sign changes
    rec["sign_changes"] = {}
    for ax in ax_run:
        for i in range(2):
            sc = sign_changes(ctx, ax, i)
            print(f"sign changes of the reduced g_{i + 1} along v_{ax} between neighbouring converged points: {len(sc)}" + "".join(f"\n  {'+' if s_ > 0 else '-'} side between {lo:.3e} and {hi:.3e}" for s_, lo, hi in sc), flush=True)
            rec["sign_changes"][f"g{i + 1}_v{ax}"] = [(s_, lo, hi) for s_, lo, hi in sc]
    rec["controls"] = {k: bool(v) for k, v in ctl.items()}
    print("\ncontrols: " + ", ".join(f"{k} {'pass' if v else 'FAIL'}" for k, v in sorted(ctl.items())))
    ok = all(ctl.values())
    print("check:", "pass" if ok else "FAIL")
    if opts.get("json"):
        json.dump(rec, open(opts["json"], "w"), indent=1, default=str)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
