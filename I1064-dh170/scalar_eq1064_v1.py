#!/usr/bin/env python3
"""#1064 part 2 (coordinator's hc, 21 Nov ~13:10 UTC): the signed scalar equation along the weak pair at D 262.0099, ks 315.

    cd hp && python3 scalar_eq1064.py RAWDIR STATE --ks=K [--keep_plan=0|1] [--its=32] [--threads=4] [--t1=1e-47] [--t2=1e-50] [--ref=raise_test_ks315.json] [--json=OUT] [--mutate=sign|double]

Same setup as raise_test1064.py (near_null's pinned system at the state's kfreeze, horizon series to order K, plan made again when K differs from the state's ks, octo-double LU, subspace iteration for the
weak pair v_1, v_2 with sigma_1 < sigma_2, u_i = J v_i / sigma_i by the transpose solve). With R(z) the pinned residual F - c (eight parts) and g_i(s) = u_i . R(z + s_1 v_1 + s_2 v_2):

    g_i(s) = a_i + sigma_i s_i + (1/2) sum_jk q_i,jk s_j s_k,    a_i = u_i . R(z),   q_i,jk = u_i . D^2R[v_j, v_k]  (the second derivative, a signed projection).

The 1-D equation along v_1 is a_1 + sigma_1 t + (q_1,11 / 2) t^2 = 0 (the order's "sigma_1 t + q t^2 + u_1.R = 0" has q = q_1,11 / 2 here). The tensor is measured by central second differences of the
residual, R(z + t w) + R(z - t w) - 2 R(z) = t^2 D^2R[w, w] + O(t^4) (the linear and cubic terms cancel, so the direction's error does not enter), for w = v_1, v_2, v_1 + v_2, v_1 - v_2, and the
polarization q_12 = (Q[v_1 + v_2] - Q[v_1 - v_2]) / 4. v_1, v_2 are refined in octo-double (three block inverse iterations of (J^T J)^-1 with Gram-Schmidt, the vectors' errors in the strong directions
fall below 1e-33). The roots are solved at 140 digits (mpmath): the 1-D equation exactly, the 2-D system through the directions of its quadratic part and Newton from there with the linear terms.
Controls (exit 1 on failure):
  C0  part 1's numbers reproduced: u_1.R, u_2.R and the max-norm q along v_1 against --ref (1e-6, 1e-3); u_i unit to 1e-6; |u_1.u_2|, |v_1.v_2| small;
  C1  a_i from residual_o against a_i from newton_o's residual (1e-6);
  C2  the tensor scales as t^2: t1 against t2 within 1e-3 of the largest entry;
  C3  the parallelogram identity Q[v_1 + v_2] + Q[v_1 - v_2] = 2 (Q[v_1] + Q[v_2]) within 1e-3;
  C4  planted roots: R_pl(z) = R(z) - R(z + s* . v) (so z + s* . v is an exact root of R_pl; a_pl recomputed from the true residual), s* = (3e-42, -2e-42) for the 2-D solver and (3e-42) along v_1
      for the 1-D solver; each solver must return s* among its roots to 1e-3 relative;
  C5  direct check at the roots of the data: u_i . R(z + s_root . v) (the true residual, not the expansion) within 1e-3 |a_i| of 0 at every root returned;
  --mutate=sign takes q_1,11 with the wrong sign, --mutate=double takes every q twice too large, both in the solver only: C4 must fail.
Also printed, as information and not as a control: after each real 2-D root, R at z* and the Newton step of the complement (the step -J^-1 R(z*) with its v_1, v_2 components removed to 1e-50), the weak
projections u_1.R, u_2.R after that step and max|R|."""
import json
import os
import sys
import time

import numpy as np

HP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("HP_DIR", HP))
import near_null as nn  # noqa: E402  (near_null's own subspace iteration)
from hpkernel.driver import make_solver  # noqa: E402
from octo_corrector import load_o  # noqa: E402
import mpmath as mp  # noqa: E402

mp.mp.dps = 140


def parts_to_mp(parts, c):
    return mp.fsum(mp.mpf(float(p[c])) for p in parts)


def nstr(x, n=8):
    return mp.nstr(x, n)


def solve_1d(a, sg, q):
    """roots of a + sg t + (q/2) t^2 = 0 (real ones)"""
    disc = sg * sg - 2 * q * a
    if disc < 0:
        return []
    r = mp.sqrt(disc)
    return sorted([(-sg + r) / q, (-sg - r) / q])


def solve_pair(a, sg, q):
    """real roots (s1, s2) of g_i(s) = a_i + sg_i s_i + (1/2) sum_jk q[i][j][k] s_j s_k, i = 0, 1 (mp). The quadratic part fixes the directions: a_2 Q_1(d) - a_1 Q_2(d) = 0, then rho^2 = -a_1 / Q_1(d);
    each seed (+-rho d) is refined by Newton with the linear terms. Returns (roots, info)."""
    def Qf(i, d):
        return sum(q[i][j][k] * d[j] * d[k] for j in range(2) for k in range(2)) / 2
    A = (a[1] * q[0][0][0] - a[0] * q[1][0][0]) / 2
    B = (a[1] * q[0][0][1] - a[0] * q[1][0][1]) / 2
    C = (a[1] * q[0][1][1] - a[0] * q[1][1][1]) / 2
    info = dict(B2_minus_AC=B * B - A * C)
    if B * B - A * C < 0:
        return [], info
    Rr = mp.sqrt((A - C) ** 2 / 4 + B * B)
    phi = mp.atan2(B, (A - C) / 2)
    dirs = []
    for sgn in (1, -1):
        c2 = -(A + C) / (2 * Rr)
        th = (phi + sgn * mp.acos(max(-1, min(1, c2)))) / 2
        dirs.append((mp.cos(th), mp.sin(th)))
    seeds = []
    for d in dirs:
        Q1, Q2 = Qf(0, d), Qf(1, d)
        rho2 = -a[0] / Q1
        info.setdefault("dirs", []).append(dict(d=[nstr(d[0], 10), nstr(d[1], 10)], Q1=nstr(Q1), Q2=nstr(Q2), rho2=nstr(rho2)))
        if rho2 > 0:
            rho = mp.sqrt(rho2)
            seeds += [[rho * d[0], rho * d[1]], [-rho * d[0], -rho * d[1]]]
    roots = []
    for s0 in seeds:
        s = list(s0)
        for _ in range(30):
            g = [a[i] + sg[i] * s[i] + sum(q[i][j][k] * s[j] * s[k] for j in range(2) for k in range(2)) / 2 for i in range(2)]
            Jg = mp.matrix(2, 2)
            for i in range(2):
                for j in range(2):
                    Jg[i, j] = (sg[i] if i == j else 0) + sum(q[i][j][k] * s[k] for k in range(2))
            ds = mp.lu_solve(Jg, mp.matrix([-g[0], -g[1]]))
            s = [s[0] + ds[0], s[1] + ds[1]]
            if max(abs(ds[0]), abs(ds[1])) <= mp.mpf(10) ** -100 * max(abs(s[0]), abs(s[1])):
                break
        if not any(max(abs(s[0] - r[0]), abs(s[1] - r[1])) <= mp.mpf(10) ** -20 * max(abs(s[0]), abs(s[1])) for r in roots):
            roots.append(s)
    return roots, info


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if len(args) < 2 or "ks" not in opts:
        sys.exit(__doc__)
    raw, st = args
    its, ks = int(opts.get("its", 32)), int(opts["ks"])
    t1, t2 = float(opts.get("t1", 1e-47)), float(opts.get("t2", 1e-50))
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
    k = 2
    V, hist = nn.subspace(solve, L, 6, its)
    sig = hist[-1]
    conv = np.abs(hist[-1] - hist[-2]) / hist[-1]
    print(f"sigma_1 {sig[0]:.6e}, sigma_2 {sig[1]:.6e}, sigma_3 {sig[2]:.4e}; subspace iteration converged to {conv[0]:.1e}, {conv[1]:.1e}", flush=True)

    def dot8(a8, b8):
        return mp.fsum(parts_to_mp(a8, c) * parts_to_mp(b8, c) for c in range(L))

    # u_i = J^-T v_i / ||J^-T v_i|| (so J v_i = sigma_i u_i, sigma_i = 1/||J^-T v_i||); mp vectors
    uvec, sg_mp, uraw = [], [], []
    for i in range(k):
        x = s.olu_solve([np.ascontiguousarray(V[:, i])] + [zero] * 7, True)
        x = [np.ascontiguousarray(np.asarray(p)) for p in x]
        raw_v = [parts_to_mp(x, c) for c in range(L)]
        nr = mp.sqrt(mp.fsum(r * r for r in raw_v))
        uvec.append([r / nr for r in raw_v])
        sg_mp.append(1 / nr)
        uraw.append(x)

    def proj(i, X8):
        return mp.fsum(uvec[i][c] * parts_to_mp(X8, c) for c in range(L))
    uu12 = mp.fsum(x * y for x, y in zip(uvec[0], uvec[1]))
    print(f"sigma_i from ||J^-T v_i||: {nstr(sg_mp[0], 10)}, {nstr(sg_mp[1], 10)} (subspace iteration: {sig[0]:.10e}, {sig[1]:.10e}); u_1.u_2 {nstr(uu12, 3)}", flush=True)

    # block inverse iteration of (J^T J)^-1 on (v_1, v_2), eight parts, Gram-Schmidt in 140 digits
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
    t3 = time.time()
    for _ in range(3):
        x1 = normalize(inv8(x1))
        x2 = normalize(deflate(inv8(x2), x1))
    x2 = deflate(x2, x1)
    n1, n2 = mp.sqrt(dot8(x1, x1)), mp.sqrt(dot8(x2, x2))
    v12 = dot8(x1, x2) / (n1 * n2)
    print(f"refined v_1, v_2 ({time.time() - t3:.0f} s): norms {nstr(n1, 12)}, {nstr(n2, 12)}; v_1.v_2 {nstr(v12, 3)}; f64 v_i . refined v_i: "
          f"{float(V[:, 0] @ (np.asarray(x1[0]) + np.asarray(x1[1]))):.12f}, {float(V[:, 1] @ (np.asarray(x2[0]) + np.asarray(x2[1]))):.12f}", flush=True)
    vs = [x1, x2]

    z8 = [np.ascontiguousarray(np.asarray(p)) for p in z]

    def at(combo, t=1.0):
        """the pinned residual R = F - c at z + t sum_j cf_j v_j (eight parts)"""
        zt = z8
        for cf, v in combo:
            zt = ax8(cf * t, v, zt)
        Fx = s.residual_o([np.ascontiguousarray(p) for p in zt])
        return ax8(-1.0, c8, [np.ascontiguousarray(np.asarray(p)) for p in Fx])

    R0 = at([])
    a = [proj(0, R0), proj(1, R0)]
    a_newton = [proj(0, R8), proj(1, R8)]
    relC1 = max(float(abs(a[i] - a_newton[i]) / abs(a_newton[i])) for i in range(2))
    print(f"a_1 = u_1.R {nstr(a[0], 10)}, a_2 = u_2.R {nstr(a[1], 10)} (residual_o; newton_o's residual gives {nstr(a_newton[0], 10)}, {nstr(a_newton[1], 10)}, relative difference {relC1:.1e})", flush=True)
    ctl = {}
    ctl["C1"] = relC1 <= 1e-6
    ref = json.load(open(opts["ref"])) if opts.get("ref") else None
    refq = None
    if ref:
        rr = [mp.mpf(ref["rows"][i]["uR"]) for i in range(2)]
        d0 = max(float(abs(a[i] - rr[i]) / abs(rr[i])) for i in range(2))
        refq = next((r["q"] for r in ref["probe"]["along_v1"] if r["t"] == 1e-40), None) if ref.get("probe") else None
        print(f"part 1 ({opts['ref']}): u_1.R {nstr(rr[0], 8)}, u_2.R {nstr(rr[1], 8)}; relative difference {d0:.1e}", flush=True)
        ctl["C0a"] = d0 <= 1e-6
    # the tensor
    combos = {"v1": [(1.0, vs[0])], "v2": [(1.0, vs[1])], "v1+v2": [(1.0, vs[0]), (1.0, vs[1])], "v1-v2": [(1.0, vs[0]), (-1.0, vs[1])]}
    Qs, qmax = {}, {}
    t4 = time.time()
    for t in (t1, t2):
        for name, cb in combos.items():
            Rp, Rm = at(cb, t), at(cb, -t)
            DD = ax8(-2.0, R0, ax8(1.0, Rp, Rm))
            Qs[(t, name)] = [proj(i, DD) / mp.mpf(t) ** 2 for i in range(2)]
            qmax[(t, name)] = float(np.abs(np.asarray(DD[0]) + np.asarray(DD[1])).max()) / t ** 2
    print(f"tensor measured by central second differences at t = {t1:g} and {t2:g} ({time.time() - t4:.0f} s)", flush=True)

    def tens(t):
        Qa = {n: Qs[(t, n)] for n in combos}
        q = [[[None, None], [None, None]] for _ in range(2)]
        for i in range(2):
            q[i][0][0] = Qa["v1"][i]
            q[i][1][1] = Qa["v2"][i]
            q[i][0][1] = q[i][1][0] = (Qa["v1+v2"][i] - Qa["v1-v2"][i]) / 4
        return q, Qa
    q, Qa = tens(t1)
    qb, _ = tens(t2)
    big = max(abs(q[i][j][kk]) for i in range(2) for j in range(2) for kk in range(2))
    dq = max(abs(q[i][j][kk] - qb[i][j][kk]) for i in range(2) for j in range(2) for kk in range(2))
    ctl["C2"] = dq <= 1e-3 * big
    print(f"C2 t^2 scaling: largest |q_i,jk| {nstr(big, 6)}; largest difference between t = {t1:g} and {t2:g}: {nstr(dq, 3)} ({nstr(dq / big, 3)} of it)", flush=True)
    par = max(abs(Qa["v1+v2"][i] + Qa["v1-v2"][i] - 2 * (Qa["v1"][i] + Qa["v2"][i])) for i in range(2))
    ctl["C3"] = par <= 1e-3 * big
    print(f"C3 parallelogram identity: largest violation {nstr(par, 3)} ({nstr(par / big, 3)} of the largest entry)", flush=True)
    qm1 = qmax[(t1, "v1")]
    print(f"max-norm of D^2R[v_1, v_1]: {qm1:.4e} (t = {t1:g}), {qmax[(t2, 'v1')]:.4e} (t = {t2:g})" + (f"; part 1's q along v_1: {refq:.4e}" if refq else ""), flush=True)
    if refq:
        ctl["C0b"] = abs(qm1 - refq) <= 1e-3 * refq
    ctl["C0c"] = bool(abs(sg_mp[0] * 1 - mp.mpf(float(sig[0]))) <= 1e-6 * sig[0] and abs(sg_mp[1] - mp.mpf(float(sig[1]))) <= 1e-6 * sig[1] and abs(uu12) <= 1e-8 and abs(v12) <= 1e-8)

    sg = [sg_mp[0], sg_mp[1]]
    qs = [[[q[i][j][kk] for kk in range(2)] for j in range(2)] for i in range(2)]      # what the solver gets (the mutation acts here only)
    if mutate == "sign":
        qs[0][0][0] = -qs[0][0][0]
    elif mutate == "double":
        qs = [[[2 * qs[i][j][kk] for kk in range(2)] for j in range(2)] for i in range(2)]

    print("\n| i | a_i = u_i.R | sigma_i | q_i,11 | q_i,12 | q_i,22 |\n|---|---|---|---|---|---|")
    for i in range(2):
        print(f"| {i + 1} | {nstr(a[i], 8)} | {nstr(sg[i], 8)} | {nstr(q[i][0][0], 6)} | {nstr(q[i][0][1], 6)} | {nstr(q[i][1][1], 6)} |")
    rec = dict(state=st, ks=ks, plan="stored" if keep_plan else "new", t1=t1, t2=t2, sigma=[nstr(x, 12) for x in sg], a=[nstr(x, 12) for x in a],
               q=[[[nstr(q[i][j][kk], 10) for kk in range(2)] for j in range(2)] for i in range(2)], qmax_v1=qm1, v1v2=nstr(v12, 6), u1u2=nstr(uu12, 6), controls={})

    # 1-D roots along v_1 and v_2 (the equation of component i along v_i alone)
    print("\n1-D equations a_i + sigma_i t + (q_i,ii / 2) t^2 = 0 (t along v_i):")
    rec["roots1d"] = []
    roots1 = [solve_1d(a[i], sg[i], qs[i][i][i]) for i in range(2)]
    for i in range(2):
        disc = sg[i] ** 2 - 2 * qs[i][i][i] * a[i]
        print(f"  i = {i + 1}: sign(q) {'+' if qs[i][i][i] > 0 else '-'}, sign(a) {'+' if a[i] > 0 else '-'}, discriminant sigma^2 - 2 q a = {nstr(disc, 5)}: "
              + (f"real roots t = {', '.join(nstr(r, 8) for r in roots1[i])}" if roots1[i] else "no real root"), flush=True)
        rec["roots1d"].append([nstr(r, 12) for r in roots1[i]])
    # 2-D roots
    roots2, info2 = solve_pair(a, sg, qs)
    print(f"\n2-D system (pair): B^2 - AC of the quadratic part's direction equation = {nstr(info2['B2_minus_AC'], 6)}: "
          + (f"{len(roots2)} real root(s)" if roots2 else "no real root"), flush=True)
    for d in info2.get("dirs", []):
        print(f"  direction ({d['d'][0]}, {d['d'][1]}): Q_1 {d['Q1']}, Q_2 {d['Q2']}, rho^2 {d['rho2']}")
    for r in roots2:
        print(f"  root s = ({nstr(r[0], 8)}, {nstr(r[1], 8)}), |s| {nstr(mp.sqrt(r[0] ** 2 + r[1] ** 2), 5)}")
    rec["roots2d"] = [[nstr(r[0], 12), nstr(r[1], 12)] for r in roots2]

    # C4 planted roots, through the same solvers (with the same mutation)
    st2 = (mp.mpf(3e-42), mp.mpf(-2e-42))
    Rst = at([(3e-42, vs[0]), (-2e-42, vs[1])])
    apl = [a[i] - proj(i, Rst) for i in range(2)]
    rp2, _ = solve_pair(apl, sg, qs)
    hit2 = [r for r in rp2 if max(abs(r[0] - st2[0]) / abs(st2[0]), abs(r[1] - st2[1]) / abs(st2[1])) <= 1e-3]
    err2 = min((max(abs(r[0] - st2[0]) / abs(st2[0]), abs(r[1] - st2[1]) / abs(st2[1])) for r in rp2), default=None)
    Rst1 = at([(3e-42, vs[0])])
    apl1 = a[0] - proj(0, Rst1)
    rp1 = solve_1d(apl1, sg[0], qs[0][0][0])
    st1 = mp.mpf(3e-42)
    hit1 = [r for r in rp1 if abs(r - st1) / st1 <= 1e-3]
    err1 = min((abs(r - st1) / st1 for r in rp1), default=None)
    ctl["C4"] = bool(hit2) and bool(hit1)
    print(f"\nC4 planted 2-D root s* = (3e-42, -2e-42): a_pl = ({nstr(apl[0], 6)}, {nstr(apl[1], 6)}); the solver returned {len(rp2)} root(s), closest relative error "
          f"{'none' if err2 is None else nstr(err2, 3)}: {'found' if hit2 else 'NOT found'}", flush=True)
    print(f"C4 planted 1-D root t* = 3e-42 along v_1: a_pl = {nstr(apl1, 6)}; the solver returned {len(rp1)} root(s), closest relative error {'none' if err1 is None else nstr(err1, 3)}: "
          f"{'found' if hit1 else 'NOT found'}", flush=True)
    rec["planted"] = dict(err2d=None if err2 is None else nstr(err2, 5), err1d=None if err1 is None else nstr(err1, 5), ok=bool(ctl["C4"]))

    # C5 direct check at the roots of the data; then the complement step (information)
    ok5 = True
    rec["direct"] = []
    for i in range(2):
        for r in roots1[i]:
            Rr = at([(float(r), vs[i])])
            gi = [proj(j, Rr) for j in range(2)]
            rel = abs(gi[i]) / abs(a[i])
            ok5 &= bool(rel <= 1e-3)
            print(f"C5 1-D root along v_{i + 1}, t = {nstr(r, 8)}: u_{i + 1}.R(z + t v_{i + 1}) = {nstr(gi[i], 5)} ({nstr(rel, 3)} of |a_{i + 1}|)", flush=True)
            rec["direct"].append(dict(kind=f"1d v{i + 1}", root=nstr(r, 12), g=nstr(gi[i], 8), rel=nstr(rel, 5)))
    for r in roots2:
        cb = [(float(r[0]), vs[0]), (float(r[1]), vs[1])]
        Rz = at(cb)
        gi = [proj(j, Rz) for j in range(2)]
        rel = max(abs(gi[j]) / abs(a[j]) for j in range(2))
        ok5 &= bool(rel <= 1e-3)
        print(f"C5 2-D root ({nstr(r[0], 6)}, {nstr(r[1], 6)}): (u_1.R, u_2.R) at z* = ({nstr(gi[0], 5)}, {nstr(gi[1], 5)}) ({nstr(rel, 3)} of |a|); max|R(z*)| {float(np.abs(np.asarray(Rz[0]) + np.asarray(Rz[1])).max()):.3e}", flush=True)
        # information: the Newton step of the complement
        cs = [np.ascontiguousarray(np.asarray(p)) for p in s.olu_solve(Rz)]          # J^-1 R(z*)
        for _ in range(8):
            for x in vs:
                c = dot8(x, cs) / dot8(x, x)
                cs = ax8(-float(c), x, cs)
            if all(abs(dot8(x, cs)) <= mp.mpf(10) ** -50 for x in vs):
                break
        csn = float(np.linalg.norm(np.asarray(cs[0]) + np.asarray(cs[1])))
        # z' = z* - (the complement step) = z + s.v - cs
        zz = z8
        for cf, v in cb:
            zz = ax8(cf, v, zz)
        zz = ax8(-1.0, cs, zz)
        Fx = s.residual_o([np.ascontiguousarray(p) for p in zz])
        Rc = ax8(-1.0, c8, [np.ascontiguousarray(np.asarray(p)) for p in Fx])
        gc = [proj(j, Rc) for j in range(2)]
        print(f"   information: complement Newton step |cs| {csn:.3e}; after it u_1.R = {nstr(gc[0], 5)}, u_2.R = {nstr(gc[1], 5)} ({nstr(max(abs(gc[j]) / abs(a[j]) for j in range(2)), 3)} of |a|); "
              f"max|R| {float(np.abs(np.asarray(Rc[0]) + np.asarray(Rc[1])).max()):.3e} (at z*: {float(np.abs(np.asarray(Rz[0]) + np.asarray(Rz[1])).max()):.3e})", flush=True)
        rec["direct"].append(dict(kind="2d", root=[nstr(r[0], 12), nstr(r[1], 12)], g=[nstr(gi[0], 8), nstr(gi[1], 8)], rel=nstr(rel, 5), complement_step=csn,
                                  g_after=[nstr(gc[0], 8), nstr(gc[1], 8)], maxR_zstar=float(np.abs(np.asarray(Rz[0]) + np.asarray(Rz[1])).max()),
                                  maxR_after=float(np.abs(np.asarray(Rc[0]) + np.asarray(Rc[1])).max())))
    if not roots1[0] and not roots1[1] and not roots2:
        print("C5 no real root of the data to check (vacuous)", flush=True)
    ctl["C5"] = ok5
    rec["controls"] = {kk: bool(vv) for kk, vv in ctl.items()}
    print("\ncontrols: " + ", ".join(f"{kk} {'pass' if vv else 'FAIL'}" for kk, vv in sorted(ctl.items())))
    ok = all(ctl.values())
    print("check:", "pass" if ok else "FAIL")
    if opts.get("json"):
        json.dump(rec, open(opts["json"], "w"), indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
