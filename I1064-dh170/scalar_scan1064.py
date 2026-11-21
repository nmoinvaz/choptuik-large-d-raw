#!/usr/bin/env python3
"""#1064 part 2, design 2 (README, written before it ran): the weak scalar function g_i(t) = u_i . R(z + t v_j) scanned directly, at D 262.0099.

    cd hp && python3 scalar_scan1064.py RAWDIR STATE --ks=K [--keep_plan=0|1] [--its=32] [--threads=4] [--json=OUT] [--mutate=shift] [--expect293=1]

Same setup as scalar_eq1064_v1.py / raise_test1064.py: near_null's pinned system, horizon series to order K, one octo-double LU, subspace iteration for v_1, v_2 (refined in octo-double), u_i = J^-T v_i normalized.
R(z + t v_j) is the true pinned residual (eight parts), t = +-10^e for e = -50 .. -10, j = 1, 2, both projections i = 1, 2 each time. Then: the even and odd parts per decade, the sign changes of g_j along
v_j bracketed per decade and bisected in log t to 1e-9 (at most 6 roots per direction), the information on u_3 .. u_6, and the controls P1 to P4 of the README (exit 1 when one fails)."""
import json
import os
import sys
import time

import numpy as np

HP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("HP_DIR", HP))
import mpmath as mp  # noqa: E402

mp.mp.dps = 140
EMIN, EMAX = -50, -10
INFO_E = (-45, -40, -35, -30, -25)
KINFO = 6


def nstr(x, n=5):
    return mp.nstr(x, n)


def fl(sg, e):
    return sg * float(f"1e{e}")


def sgn(x):
    return 1 if x > 0 else -1


def bisect_log(f, lo, hi, tol=1e-9):
    """f on magnitudes lo < hi (floats), f(lo) and f(hi) of opposite sign: the geometric bisection to hi / lo - 1 <= tol; returns the geometric midpoint"""
    flo = f(lo)
    while hi / lo - 1 > tol:
        mid = (lo * hi) ** 0.5
        fm = f(mid)
        if sgn(fm) == sgn(flo):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo * hi) ** 0.5


def find_roots(G, j, a_j, shift=0, maxroots=6, bisect_it=True):
    """sign changes of g(t) = G(j, t)[j] - shift along v_j: brackets per decade on each side (and the origin to the smallest |t|); bisected unless bisect_it is False.
    Returns a list of dict(side, lo, hi, t)."""
    out = []
    n = 0
    for sg in (1, -1):
        vals = {e: G(j, fl(sg, e))[j] - shift for e in range(EMIN, EMAX + 1)}
        prev = (None, a_j - shift)
        if sgn(prev[1]) != sgn(vals[EMIN]):
            out.append(dict(side=sg, lo=0.0, hi=float(f"1e{EMIN}"), t=None, note="between 0 and the smallest |t|"))
        for e in range(EMIN, EMAX):
            if sgn(vals[e]) != sgn(vals[e + 1]):
                r = dict(side=sg, lo=float(f"1e{e}"), hi=float(f"1e{e + 1}"), t=None)
                if bisect_it and n < maxroots:
                    r["t"] = sg * bisect_log(lambda tm: G(j, sg * tm)[j] - shift, r["lo"], r["hi"])
                    n += 1
                out.append(r)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
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
    print(f"{st}: D {float(m['D']):g}, ks {ks} (the state's {m.get('ks', 130)}), plan {'stored' if keep_plan else 'made again'}, M {M}, kfreeze {kf}"
          + (f", MUTATE {mutate}" if mutate else ""), flush=True)
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
    print(f"start residual: max|R| (pinned, F - c) {float(np.abs(R8[0] + R8[1]).max()):.3e}", flush=True)

    def ax8(a, x8, y8):
        return [np.ascontiguousarray(np.asarray(p)) for p in od_axpy(a, *x8, *y8)]

    def solve(b, transpose=False):
        x = s.olu_solve([np.ascontiguousarray(b)] + [zero] * 7, transpose)
        return np.asarray(x[0]) + np.asarray(x[1])
    V, hist = nn.subspace(solve, L, KINFO, its)
    sig = hist[-1]
    conv = np.abs(hist[-1] - hist[-2]) / hist[-1]
    print(f"sigma_1..6 " + ", ".join(f"{x:.4e}" for x in sig) + f"; sigma_1, sigma_2 converged to {conv[0]:.1e}, {conv[1]:.1e}", flush=True)

    def dot8(a8, b8):
        return mp.fsum(parts_to_mp(a8, c) * parts_to_mp(b8, c) for c in range(L))

    def parts_to_mp(parts, c):
        return mp.fsum(mp.mpf(float(p[c])) for p in parts)
    uvec, sg_mp = [], []
    for i in range(KINFO):
        x = s.olu_solve([np.ascontiguousarray(V[:, i])] + [zero] * 7, True)
        x = [np.ascontiguousarray(np.asarray(p)) for p in x]
        raw_v = [parts_to_mp(x, c) for c in range(L)]
        nr = mp.sqrt(mp.fsum(r * r for r in raw_v))
        uvec.append([r / nr for r in raw_v])
        sg_mp.append(1 / nr)

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
    n1, n2 = mp.sqrt(dot8(x1, x1)), mp.sqrt(dot8(x2, x2))
    print(f"refined v_1, v_2: norms {nstr(n1, 10)}, {nstr(n2, 10)}; v_1.v_2 {nstr(dot8(x1, x2), 3)}; sigma_i from ||J^-T v_i||: {nstr(sg_mp[0], 10)}, {nstr(sg_mp[1], 10)}", flush=True)
    z8 = [np.ascontiguousarray(np.asarray(p)) for p in z]

    def at(combo, t=1.0):
        zt = z8
        for cf, v in combo:
            zt = ax8(cf * t, v, zt)
        Fx = s.residual_o([np.ascontiguousarray(p) for p in zt])
        return ax8(-1.0, c8, [np.ascontiguousarray(np.asarray(p)) for p in Fx])

    R0 = at([])
    a = [proj(0, R0), proj(1, R0)]
    a_newton = [proj(0, R8), proj(1, R8)]
    ak = [proj(i, R0) for i in range(2, KINFO)]
    relP4 = max(float(abs(a[i] - a_newton[i]) / abs(a_newton[i])) for i in range(2))
    print(f"a_1 = u_1.R {nstr(a[0], 10)}, a_2 = u_2.R {nstr(a[1], 10)} (newton_o's residual: {nstr(a_newton[0], 10)}, {nstr(a_newton[1], 10)}; relative difference {relP4:.1e})", flush=True)
    ctl = {"P4": relP4 <= 1e-6}
    sg = [sg_mp[0], sg_mp[1]]

    cache, extra = {}, {}

    def G(j, t):
        key = (j, t)
        if key not in cache:
            Rt = at([(t, vs[j])])
            cache[key] = (proj(0, Rt), proj(1, Rt))
            if j == 0 and any(abs(t) == float(f"1e{e}") for e in INFO_E):
                extra[t] = [proj(i, Rt) for i in range(2, KINFO)]
        return cache[key]

    t1 = time.time()
    rec = dict(state=st, ks=ks, plan="stored" if keep_plan else "new", sigma=[nstr(x, 12) for x in sg], a=[nstr(x, 12) for x in a], scan={}, roots={}, controls={})
    for j in (0, 1):
        print(f"\nscan along v_{j + 1}: g_i(t) = u_i . R(z + t v_{j + 1}); even q_i(t) = (g_i(t) + g_i(-t) - 2 a_i)/t^2 and odd (g_i(t) - g_i(-t))/(2 t)", flush=True)
        print("| e | g_1(+t) | g_1(-t) | g_2(+t) | g_2(-t) | even q_1 | even q_2 | odd_1 | odd_2 |\n|---|---|---|---|---|---|---|---|---|")
        rows = []
        for e in range(EMIN, EMAX + 1):
            tp, tm = fl(1, e), fl(-1, e)
            gp, gm = G(j, tp), G(j, tm)
            ev = [(gp[i] + gm[i] - 2 * a[i]) / mp.mpf(tp) ** 2 for i in range(2)]
            od = [(gp[i] - gm[i]) / (2 * mp.mpf(tp)) for i in range(2)]
            rows.append(dict(e=e, gp=[gp[0], gp[1]], gm=[gm[0], gm[1]], ev=ev, od=od))
            print(f"| {e} | {nstr(gp[0], 4)} | {nstr(gm[0], 4)} | {nstr(gp[1], 4)} | {nstr(gm[1], 4)} | {nstr(ev[0], 4)} | {nstr(ev[1], 4)} | {nstr(od[0], 4)} | {nstr(od[1], 4)} |", flush=True)
        rec["scan"][f"v{j + 1}"] = [dict(e=r["e"], gp=[nstr(x, 8) for x in r["gp"]], gm=[nstr(x, 8) for x in r["gm"]], ev=[nstr(x, 8) for x in r["ev"]], od=[nstr(x, 8) for x in r["od"]]) for r in rows]
        # reading rule 2: resolved q_j in a window
        evd = [abs(r["ev"][j]) * mp.mpf(fl(1, r["e"])) ** 2 for r in rows]
        floor = min(evd)
        res = []
        for n in range(1, len(rows) - 1):
            q0, qa, qb = rows[n]["ev"][j], rows[n - 1]["ev"][j], rows[n + 1]["ev"][j]
            if q0 != 0 and abs(qa - q0) <= 0.1 * abs(q0) and abs(qb - q0) <= 0.1 * abs(q0) and evd[n] >= mp.mpf(10) ** 6 * floor:
                res.append((rows[n]["e"], q0))
        rec["scan"][f"q{j + 1}_resolved"] = [(e, nstr(q0, 8)) for e, q0 in res]
        print(f"reading rule 2: smallest |even part| in the scan {nstr(floor, 3)}; q_{j + 1}(t) resolved at decades " + (", ".join(f"e = {e} (q = {nstr(q0, 5)})" for e, q0 in res) if res else "none (not resolved)"), flush=True)
    print(f"scan: {len(cache)} residual evaluations, {time.time() - t1:.0f} s", flush=True)

    # information: the curvature on the next left vectors along v_1
    print("\ninformation: q_k,11(t) = (u_k.R(z + t v_1) + u_k.R(z - t v_1) - 2 u_k.R(z)) / t^2, k = 3 .. 6 (second derivative of the projection; noise level 4e-12 at t = 1e-47 for the weak pair)")
    print("| e | " + " | ".join(f"q_{k + 3},11" for k in range(KINFO - 2)) + " |\n|---|" + "---|" * (KINFO - 2))
    rec["info"] = []
    for e in INFO_E:
        tp, tm = fl(1, e), fl(-1, e)
        qk = [(extra[tp][k] + extra[tm][k] - 2 * ak[k]) / mp.mpf(tp) ** 2 for k in range(KINFO - 2)]
        print(f"| {e} | " + " | ".join(nstr(x, 4) for x in qk) + " |")
        rec["info"].append(dict(e=e, q=[nstr(x, 8) for x in qk]))
    print("sigma_k: " + ", ".join(f"k={k + 3}: {sig[k + 2]:.4e}" for k in range(KINFO - 2)) + "; u_k.R(z): " + ", ".join(f"{nstr(x, 4)}" for x in ak))
    for tt in (1e-34, 1e-30):
        e = int(round(np.log10(tt)))
        row = next((r for r in rec["info"] if r["e"] == e), None)
        if row:
            print(f"  strong shift w_k = |q_k,11| t^2 / (2 sigma_k) at t = {tt:g}: " + ", ".join(nstr(abs(mp.mpf(row['q'][k])) * mp.mpf(tt) ** 2 / (2 * mp.mpf(float(sig[k + 2]))), 3) for k in range(KINFO - 2)))

    # roots of g_j along v_j
    for j in (0, 1):
        rts = find_roots(G, j, a[j])
        rec["roots"][f"v{j + 1}"] = [dict(side=r["side"], lo=r["lo"], hi=r["hi"], t=None if r["t"] is None else nstr(mp.mpf(r["t"]), 12), note=r.get("note", "")) for r in rts]
        print(f"\nsign changes of g_{j + 1} along v_{j + 1}: {len(rts)}")
        for r in rts:
            print(f"  between |t| {r['lo']:.0e} and {r['hi']:.0e} on the {'+' if r['side'] > 0 else '-'} side" + (f": t = {r['t']:.9e}" if r["t"] is not None else ("" if "note" not in r else f" ({r['note']})")), flush=True)
        if j == 0:
            roots1 = rts
        else:
            roots2 = rts
    print(f"scan and bisection: {len(cache)} residual evaluations in all, {time.time() - t1:.0f} s", flush=True)

    # P1 planted root
    tstar = 3e-42
    c = G(0, tstar)[0] * (mp.mpf("1.5") if mutate == "shift" else 1)
    pl = find_roots(G, 0, a[0], shift=c)
    hit = [r for r in pl if r["t"] is not None and abs(r["t"] - tstar) / tstar <= 1e-6]
    inbr = [r for r in pl if r["side"] > 0 and r["lo"] <= tstar <= r["hi"]]
    ctl["P1"] = bool(hit) and bool(inbr)
    print(f"\nP1 planted root t* = 3e-42 along v_1 (shift u_1.R(z + t* v_1) = {nstr(c, 6)}{', x1.5 (MUTATE)' if mutate == 'shift' else ''}): {len(pl)} sign change(s); bracket of t*'s decade: {'yes' if inbr else 'NO'}; "
          f"returned {', '.join(f'{r['t']:.9e}' for r in pl if r['t'] is not None) or 'none'}: {'pass' if ctl['P1'] else 'FAIL'}", flush=True)
    rec["planted"] = dict(shift=nstr(c, 10), roots=[None if r['t'] is None else r['t'] for r in pl], ok=bool(ctl["P1"]))

    # P2 known truth at ks 293
    if opts.get("expect293") == "1":
        exp = [-7.1162e-48, +6.0419e-48]
        ok = True
        for j, rts in ((0, roots1), (1, roots2)):
            got = [r["t"] for r in rts if r["t"] is not None]
            near = min(got, key=lambda x: abs(x - exp[j])) if got else None
            rel = abs(near - exp[j]) / abs(exp[j]) if near is not None else None
            ok &= bool(rel is not None and rel <= 1e-3)
            print(f"P2 ks 293: root of g_{j + 1} along v_{j + 1} expected {exp[j]:.4e} (part 1: -a/sigma); nearest sign change {near if near is None else f'{near:.6e}'}; relative difference {rel if rel is None else f'{rel:.1e}'}", flush=True)
        ctl["P2"] = ok
    # P3 run 2's direct evaluations at ks 315
    if opts.get("expect315") == "1":
        e1 = G(0, 1.2173691e-14)[0]
        e2 = G(1, 6.4265201e-15)[1]
        r1, r2 = abs(e1 - mp.mpf("-2.391e24")) / mp.mpf("2.391e24"), abs(e2 - mp.mpf("7.8919e24")) / mp.mpf("7.8919e24")
        ctl["P3"] = bool(r1 <= 1e-3 and r2 <= 1e-3)
        print(f"P3 ks 315: u_1.R(z + 1.2173691e-14 v_1) = {nstr(e1, 5)} (run 2: -2.391e24, relative difference {nstr(r1, 2)}); u_2.R(z + 6.4265201e-15 v_2) = {nstr(e2, 5)} (run 2: 7.8919e24, {nstr(r2, 2)})", flush=True)
    rec["controls"] = {k: bool(v) for k, v in ctl.items()}
    print("\ncontrols: " + ", ".join(f"{k} {'pass' if v else 'FAIL'}" for k, v in sorted(ctl.items())))
    ok = all(ctl.values())
    print("check:", "pass" if ok else "FAIL")
    if opts.get("json"):
        json.dump(rec, open(opts["json"], "w"), indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
