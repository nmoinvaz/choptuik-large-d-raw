#!/usr/bin/env python3
"""#1064 (coordinator's hc, 21 Nov ~12:05 UTC): is the order raise's failure the start residual's component along the weak direction?

    cd hp && python3 raise_test1064.py RAWDIR STATE --ks=K [--keep_plan=0|1] [--k=6] [--its=32] [--threads=4] [--eps=1e-10] [--json=OUT] [--mutate=sigma1]

The hypothesis: the start residual of the raise has a component along u_1 (the weakest left singular vector), so Newton's first step along v_1 is (u_1.F)/sigma_1, far outside any basin. At the state STATE
(anm_run's base: the pinned system of the state's kfreeze, the horizon series summed to order K, the plan made again at the state when --keep_plan=0 as anm_run does for a changed --ks) this prints
  (1) the start residual: max|F| of the pinned octo-double system, R = F(z) - c (F = newton_o's residual, c the held offset of the state's own p1 coefficients, near_null's pinned step's c), and of the unpinned F;
  (2) near_null's k lowest right singular vectors v_i and sigma_i of that Jacobian (near_null's subspace iteration, near_null's own code), u_i = J v_i / sigma_i (formed as sigma_i J^-T v_i by the transpose solve);
  (3) per i: u_i.R, the step component (u_i.R)/sigma_i, the Delta share of v_i, and the same for the unpinned F.
It is near_null.py's setup, factorization, subspace iteration and exact-Jacobian check (J v_1 at 140 digits), with --ks and the plan chosen as anm_run does; the dot products are formed at 140 digits (mpmath).
Controls (exit 1 on failure): near_null's check (||J v_1|| / sigma_1 within 1e-2 of 1, sigma_1 converged to 1e-3); route B for i = 1: u_1 from the exact Jacobian at 140 digits (J v_1 / sigma_1, v_1 refined in octo-double) against u_1 from the transpose solve, 1e-6 relative; the planted check: R_pl = J (eps v_1)
(eight parts, od_axpy over J's columns, as near_null's --planted) put through the same analysis must return (u_1.R_pl)/sigma_1 = eps and u_i.R_pl = 0 (i > 1) to 1e-6 eps sigma_1, and the Newton step -J^-1 R_pl must have v_1 component -eps to 1e-6;
--mutate=sigma1 takes sigma_1 1.05 times too large in the analysis, and the planted check must fail."""
import json
import os
import sys
import time

import numpy as np

HP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("HP_DIR", HP))
import near_null as nn  # noqa: E402  (near_null's own layout, harmonics, subspace, step_report)
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o  # noqa: E402
import mpmath as mp  # noqa: E402

mp.mp.dps = 140


def parts_to_mp(parts, c):
    return mp.fsum(mp.mpf(float(p[c])) for p in parts)


def dot8(a8, b8, L):
    """a . b at 140 digits for two eight-part vectors (lists of 8 arrays)"""
    av = [parts_to_mp(a8, c) for c in range(L)]
    bv = [parts_to_mp(b8, c) for c in range(L)]
    return mp.fsum(x * y for x, y in zip(av, bv))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if len(args) < 2 or "ks" not in opts:
        sys.exit(__doc__)
    raw, st = args
    k, its, ks = int(opts.get("k", 6)), int(opts.get("its", 32)), int(opts["ks"])
    eps = float(opts.get("eps", 1e-10))
    mutate = opts.get("mutate", "")
    z, m = load_o(os.path.join(raw, st))
    z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
    M, nodes = int(m["M"]), list(m["nodes"])
    D = m.get("D_str", repr(float(m["D"])))
    kf = int(m.get("kfreeze", 3))
    s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=ks, threads=int(opts.get("threads", 4)), kfreeze=kf)
    ks_changed = ks != m.get("ks", 130)
    keep_plan = opts.get("keep_plan", "1") == "1" and "segs" in m and not ks_changed
    s.set_segs(m["segs"] if keep_plan else s.plan(z[0], z[1], 1e-32, 0.05))
    print(f"{st}: D {float(m['D']):g}, ks {ks} (the state's {m.get('ks', 130)}), plan {'stored' if keep_plan else 'made again'}, M {M}, kfreeze {kf}", flush=True)
    L = len(z[0])
    zero = np.zeros(L)
    from multidouble import od_axpy
    from pinning import PinnedSolver, band_coeffs, band_field
    t0 = time.time()
    keep = hasattr(s, "jacobian_o_kept")
    out = s.newton_o(z, keep_jacobian=True) if keep else s.newton_o(z)
    print(f"octo-double LU {time.time() - t0:.0f} s, pivots {out[3]:.1e}..{out[4]:.1e}", flush=True)
    F8 = s.newton_o_residual(z) if hasattr(s, "newton_o_residual") else None
    F8 = [np.ascontiguousarray(np.asarray(p)) for p in (s.residual_o(z) if F8 is None else F8)]
    ks_held = [h for h in range(kf + 1, 14) if h % 2 == 1]
    hc = band_coeffs(z[0][:M], z[1][:M], M, ks_held, exact=True, rest=[p[:M] for p in z[2:]])
    hf = band_field(hc, ks_held, M, parts=8)
    c8 = [np.ascontiguousarray(p) for p in PinnedSolver(s, M, hf[0], hf[1], h_rest=hf[2:]).c8]
    R8 = [np.ascontiguousarray(np.asarray(p)) for p in od_axpy(-1.0, *c8, *F8)]          # the pinned system's residual F - c
    dz8 = [np.asarray(p) for p in out[0]]
    dpin8 = od_axpy(1.0, *[np.asarray(p) for p in s.olu_solve(c8)], *dz8)                # near_null's pinned step: -J^-1 (F - c)
    Rmax, Fmax = float(np.abs(R8[0] + R8[1]).max()), float(np.abs(F8[0] + F8[1]).max())
    print(f"start residual: max|R| (pinned, F - c) {Rmax:.3e}, max|F| (unpinned) {Fmax:.3e}", flush=True)

    def solve(b, transpose=False):
        x = s.olu_solve([np.ascontiguousarray(b)] + [zero] * 7, transpose)
        return np.asarray(x[0]) + np.asarray(x[1])
    V, hist = nn.subspace(solve, L, k, its)
    sig = hist[-1]
    conv = np.abs(hist[-1] - hist[-2]) / hist[-1]
    sig_an = sig.copy()
    if mutate == "sigma1":
        sig_an[0] *= 1.05
    # u_i = sigma_i J^-T v_i by the transpose solve (eight parts)
    U8 = []
    for i in range(k):
        x = s.olu_solve([np.ascontiguousarray(V[:, i])] + [zero] * 7, True)
        U8.append([np.ascontiguousarray(np.asarray(p)) for p in x])          # J^-T v_i = u_i / sigma_i

    def analyse(res8, label):
        """per i: u_i . res (u_i = sigma_i * J^-T v_i), and the step component (u_i . res)/sigma_i"""
        rows = []
        for i in range(k):
            ui_over_s = dot8(U8[i], res8, L)                                   # (J^-T v_i) . res = (u_i . res)/sigma_i
            rows.append(dict(i=i + 1, sigma=float(sig[i]), step=float(ui_over_s * (sig[i] / sig_an[i]) if mutate == "sigma1" and i == 0 else ui_over_s),
                             uF=float(ui_over_s * sig_an[i])))
        return rows
    rowsR, rowsF = analyse(R8, "R"), analyse(F8, "F")
    # route B for i = 1: v_1 refined in octo-double, J v_1 at 140 digits (near_null's check)
    t1 = time.time()
    x8 = [np.ascontiguousarray(V[:, 0])] + [zero] * 7
    for _ in range(3):
        y = s.olu_solve([np.ascontiguousarray(x8[0])] + [np.ascontiguousarray(p) for p in x8[1:]], True)
        y = s.olu_solve([np.ascontiguousarray(np.asarray(y[0]))] + [np.ascontiguousarray(p) for p in y[1:]])
        nrm = float(np.linalg.norm(np.asarray(y[0])))
        x8 = [np.ascontiguousarray(p) for p in od_axpy(1.0 / nrm, *[np.asarray(p) for p in y], *([zero] * 8))]
    J = s.jacobian_o_kept(z) if keep else None
    if J is None:
        J = s.jacobian_o(z)
    J = [np.asarray(p) for p in J]
    xv = [mp.fsum(mp.mpf(float(x8[q][c])) for q in range(8)) for c in range(L)]
    nz = [c for c in range(L) if xv[c] != 0]
    jv = [mp.fsum(mp.fsum(mp.mpf(float(J[q][r, c])) for q in range(8) if J[q][r, c] != 0) * xv[c] for c in nz) for r in range(L)]
    jn = mp.sqrt(mp.fsum(a * a for a in jv)) / mp.sqrt(mp.fsum(a * a for a in xv))
    ratio = float(jn / sig[0])
    print(f"||J v_1|| = {mp.nstr(jn, 6)} at 140 digits ({time.time() - t1:.0f} s); ||J v_1|| / sigma_1 = {ratio:.6f}", flush=True)
    # route B: u_1 = J v_1 / sigma_1 (140 digits); its dot with R against route A's
    uB_R = mp.fsum(a * parts_to_mp(R8, r) for r, a in enumerate(jv)) / (mp.sqrt(mp.fsum(a * a for a in xv)) * mp.mpf(float(sig[0])))
    routeA = mp.mpf(rowsR[0]["uF"])
    # (u_1 from route B has the sign of J v_1; route A's u_1 = sigma_1 J^-T v_1 of the f64 v_1: the signs of v_1 may differ between the two vectors, so compare the magnitudes)
    relB = float(abs(abs(uB_R) - abs(routeA)) / max(abs(routeA), mp.mpf(10) ** -60)) if routeA != 0 else 0.0
    print(f"route B (J v_1 / sigma_1 at 140 digits): u_1.R {mp.nstr(uB_R, 8)}; route A (sigma_1 J^-T v_1): {mp.nstr(routeA, 8)}; relative difference of the magnitudes {relB:.1e}", flush=True)
    # planted: R_pl = J w, w = eps v_1 (refined, eight parts), by columns
    t2 = time.time()
    w8 = [np.ascontiguousarray(eps * p) for p in x8]
    Jw = [zero] * 8
    wf = np.array([float(sum(float(w8[q][c]) for q in range(8))) for c in range(L)])
    for c in range(L):
        if wf[c] != 0:
            Jw = od_axpy(float(wf[c]), *[np.ascontiguousarray(J[q][:, c]) for q in range(8)], *Jw)
    Rpl8 = [np.ascontiguousarray(np.asarray(p)) for p in Jw]
    rowsP = analyse(Rpl8, "planted")
    dpl8 = s.olu_solve(Rpl8)                                                  # J^-1 R_pl = w
    v1dz = float(mp.fsum(mp.mpf(float(V[c, 0])) * parts_to_mp(dpl8, c) for c in range(L)))
    # |w| = eps in the 2-norm up to the refinement: the size to return is the (u_1.R_pl)/sigma_1 of w itself, |w| = eps * ||v_1 refined||
    wn = float(mp.sqrt(mp.fsum(a * a for a in [mp.mpf(float(wf[c])) for c in range(L)])))
    err1 = abs(rowsP[0]["step"] - wn) / wn
    errk = max(abs(r["uF"]) for r in rowsP[1:]) / abs(rowsP[0]["uF"]) if rowsP[0]["uF"] else float("inf")
    errstep = abs(abs(v1dz) - wn) / wn
    ok_p = bool(err1 <= 1e-6 and errk <= 1e-6 and errstep <= 1e-6)
    print(f"planted R_pl = J w, |w| {wn:.3e} ({time.time() - t2:.0f} s): (u_1.R_pl)/sigma_1 {rowsP[0]['step']:.6e} (|w| {wn:.6e}, relative error {err1:.1e}); largest |u_i.R_pl| (i > 1) over |u_1.R_pl| {errk:.1e}; "
          f"v_1.J^-1 R_pl {v1dz:.6e} (relative error {errstep:.1e}): planted check {'pass' if ok_p else 'FAIL'} (each within 1e-6)", flush=True)
    # the probe (--probe=1): the residual after the full pinned step, and along v_1 the quadratic term (the second derivative q) and the basin radius 2 sigma_1 / q
    probe = None
    if opts.get("probe", "0") == "1":
        z8 = [np.ascontiguousarray(np.asarray(p)) for p in load_o(os.path.join(raw, st))[0]]
        R0 = float(np.abs(R8[0] + R8[1]).max())

        def Rmax_at(z8x):
            Fx = s.residual_o([np.ascontiguousarray(np.asarray(p)) for p in z8x])
            Rx = od_axpy(-1.0, *c8, *[np.ascontiguousarray(np.asarray(p)) for p in Fx])
            return Rx
        zn = od_axpy(1.0, *[np.asarray(p) for p in dpin8], *z8)
        Rn = Rmax_at(zn)
        after = float(np.abs(np.asarray(Rn[0]) + np.asarray(Rn[1])).max())
        print(f"probe: max|R| at the start {R0:.3e}; at z + (the full pinned step) {after:.3e}", flush=True)
        probe = dict(R_start=R0, R_after_full_step=after, along_v1=[])
        v1 = [np.ascontiguousarray(x8[q]) for q in range(8)]                      # v_1 refined, eight parts
        for t in (1e-85, 1e-80, 1e-75, 1e-70, 1e-60, 1e-40, 1e-30, 1e-24, 1e-22, 1e-20, 1e-18):
            zt = od_axpy(t, *v1, *z8)
            Rt = Rmax_at(zt)
            d8 = od_axpy(-1.0, *[np.ascontiguousarray(np.asarray(p)) for p in R8], *[np.ascontiguousarray(np.asarray(p)) for p in Rt])   # R(z + t v_1) - R(z)
            dmax = float(np.abs(np.asarray(d8[0]) + np.asarray(d8[1])).max())
            lin = t * float(sig[0])
            q = 2.0 * dmax / (t * t) if dmax > 1.5 * lin else float("nan")
            print(f"probe: t {t:.0e}: max|R(z + t v_1) - R(z)| {dmax:.3e}; the linear term sigma_1 t {lin:.3e}; ratio {dmax / lin:.3e}" + (f"; q = 2 max/t^2 = {q:.3e}, basin radius 2 sigma_1/q = {2 * sig[0] / q:.2e}" if q == q else ""), flush=True)
            probe["along_v1"].append(dict(t=t, dmax=dmax, linear=lin, q=q))
    # the report
    blocks = nn.layout(M, len(nodes))
    d1 = np.asarray(dpin8[0]) + np.asarray(dpin8[1])
    vt = [float(V[:, i] @ d1) for i in range(k)]
    print(f"\n| i | sigma_i | Delta share of v_i | u_i.R | (u_i.R)/sigma_i | V^T(pinned step)_i | u_i.F (unpinned) | (u_i.F)/sigma_i |\n|---|---|---|---|---|---|---|---|")
    rec = dict(state=st, D=float(m["D"]), ks=ks, plan="stored" if keep_plan else "new", maxR=Rmax, maxF=Fmax, ratio=ratio, planted=dict(ok=ok_p, err1=err1, errk=errk, errstep=errstep, w_norm=wn),
               routeB_rel=relB, probe=probe, rows=[], pinned_step=dict(norm=float(np.linalg.norm(d1)), delta=float(d1[-1]), max=float(np.abs(d1).max())))
    for i in range(k):
        dsh = float(V[-1, i] ** 2)
        print(f"| {i + 1} | {sig[i]:.4e} | {dsh:.3e} | {rowsR[i]['uF']:+.4e} | {rowsR[i]['step']:+.4e} | {vt[i]:+.4e} | {rowsF[i]['uF']:+.4e} | {rowsF[i]['step']:+.4e} |")
        rec["rows"].append(dict(i=i + 1, sigma=float(sig[i]), conv=float(conv[i]), delta_share=dsh, uR=rowsR[i]["uF"], stepR=rowsR[i]["step"], vt_pinned=vt[i], uF=rowsF[i]["uF"], stepF=rowsF[i]["step"]))
    print(f"\nthe pinned Newton step: |dz| {np.linalg.norm(d1):.3e}, max {np.abs(d1).max():.3e}, Delta component {d1[-1]:+.3e}")
    ok = bool(conv[0] < 1e-3 and abs(ratio - 1) < 1e-2 and relB < 1e-6) and ok_p
    print(f"  sigma_1 converged to {conv[0]:.1e}; ||J v_1||/sigma_1 {ratio:.6f}; route B {relB:.1e}")
    print("check:", "pass" if ok else "FAIL")
    if opts.get("json"):
        json.dump(rec, open(opts["json"], "w"), indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
