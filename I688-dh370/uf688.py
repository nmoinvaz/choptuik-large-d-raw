#!/usr/bin/env python3
"""#688: u_1^T r by residual block at a stored state, u_1 the left singular vector of the weakest direction of the chain's pinned Newton system and
r = F - c the pinned system's residual (the base polish's step is -J^-1 r, c the held offset at the state's own coefficients).

    cd hp && python3 -u UF688 RAWDIR STATE --out=OUT.json [--threads=12] [--mutate=shift]

The setup is near_null.py's main (stored plan, octo-double LU, subspace iteration for the k = 4 weakest right singular vectors, v_1 refined in octo-double,
J v_1 from the exact Jacobian at 140 digits), from its functions. J v_1 = sigma_1 u_1, so u_1 is the unit vector J v_1 / |J v_1|, and u_1^T r is summed in
mpmath over r's eight parts. Rows of r are the residual blocks of renode_o.blocks: 4 M b to 4 M (b + 1) for b = 0 (centre>n0), 1..K-1 (n(b-1)>n(b)),
K (horizon>n(K-1)), then the phase row.

Controls: (a) -sigma_1 v_1^T dz_pinned, which does not use J v_1, equals the sum over the blocks to 1e-3 (v_1 is in f64); (b) r' = r + beta u_1, beta 1e-30,
changes the sum by beta, and block b's by beta |u_1,b|^2, to 1e-10 relative; (c) --mutate=shift moves r by one row in the sum, which must break (a)."""
import json
import os
import sys
import time

HP = "/home/nathan/Source/choptuik-large-d-685/hp"
sys.path.insert(0, HP)
import mpmath as mp  # noqa: E402
import numpy as np  # noqa: E402
from hpkernel.driver import make_solver  # noqa: E402
from multidouble import od_axpy  # noqa: E402
from near_null import layout, printed, step_report, subspace  # noqa: E402
from octo_corrector import load_o  # noqa: E402
from pinning import PinnedSolver, band_coeffs, band_field  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    mutate = "--mutate=shift" in sys.argv
    raw, st = args
    z, m = load_o(os.path.join(raw, st))
    z = [np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z]
    M, nodes = int(m["M"]), list(m["nodes"])
    K = len(nodes)
    D = m.get("D_str", repr(float(m["D"])))
    kf = int(m.get("kfreeze", 3))
    s = make_solver(D, M, nodes=nodes, kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130), threads=int(opts.get("threads", 12)), kfreeze=kf)
    assert "segs" in m, "the state has no stored plan"
    s.set_segs(m["segs"])
    L = len(z[0])
    t0 = time.time()
    out = s.newton_o(z)
    print(f"{st}: D {float(m['D']):g}, L {L}, octo-double LU {time.time() - t0:.0f} s, pivots {out[3]:.1e}..{out[4]:.1e}", flush=True)
    ks_held = [h for h in range(kf + 1, 14) if h % 2 == 1]
    hc = band_coeffs(z[0][:M], z[1][:M], M, ks_held, exact=True, rest=[p[:M] for p in z[2:]])
    hf = band_field(hc, ks_held, M, parts=8)
    c8 = [np.ascontiguousarray(p) for p in PinnedSolver(s, M, hf[0], hf[1], h_rest=hf[2:]).c8]
    dz8 = [np.asarray(p) for p in out[0]]
    dpin8 = od_axpy(1.0, *[np.asarray(p) for p in s.olu_solve(c8)], *dz8)
    F8 = [np.ascontiguousarray(np.asarray(p)) for p in s.residual_o(z)]
    r8 = od_axpy(-1.0, *c8, *F8)
    zero = np.zeros(L)

    def solve(b, transpose=False):
        x = s.olu_solve([np.ascontiguousarray(b)] + [zero] * 7, transpose)
        return np.asarray(x[0]) + np.asarray(x[1])

    V, hist = subspace(solve, L, 4, 16)
    sig = hist[-1]
    conv = np.abs(hist[-1] - hist[-2]) / hist[-1]
    x8 = [np.ascontiguousarray(V[:, 0])] + [zero] * 7
    for _ in range(3):
        y = s.olu_solve(x8, True)
        y = s.olu_solve([np.ascontiguousarray(p) for p in y])
        nrm = float(np.linalg.norm(np.asarray(y[0])))
        x8 = [np.ascontiguousarray(p) for p in od_axpy(1.0 / nrm, *[np.asarray(p) for p in y], *([zero] * 8))]
    mp.mp.dps = 140
    t1 = time.time()
    J = [np.asarray(p) for p in s.jacobian_o(z)]
    xv = [mp.fsum(mp.mpf(float(x8[q][c])) for q in range(8)) for c in range(L)]
    nz = [c for c in range(L) if xv[c] != 0]
    jv = [mp.fsum(mp.fsum(mp.mpf(float(J[q][r, c])) for q in range(8) if J[q][r, c] != 0) * xv[c] for c in nz) for r in range(L)]
    jn = mp.sqrt(mp.fsum(a * a for a in jv))
    xn = mp.sqrt(mp.fsum(a * a for a in xv))
    sigma1 = jn / xn
    u = [a / jn for a in jv]
    print(f"  ||J v_1|| {mp.nstr(sigma1, 6)} (subspace sigma_1 {sig[0]:.6e}, ratio {float(sigma1 / sig[0]):.6f}), J v_1 at 140 digits ({time.time() - t1:.0f} s)", flush=True)
    r = [mp.fsum(mp.mpf(float(r8[q][i])) for q in range(8)) for i in range(L)]
    rmax = [float(max(abs(r[i]) for i in range(4 * M * b, 4 * M * (b + 1)))) for b in range(K + 1)] + [float(abs(r[-1]))]
    names = ["centre>n0"] + [f"n{b - 1}>n{b}" for b in range(1, K)] + [f"horizon>n{K - 1}", "phase"]
    rows = [range(4 * M * b, 4 * M * (b + 1)) for b in range(K + 1)] + [range(4 * M * (K + 1), L)]
    assert 4 * M * (K + 1) + 1 == L

    def blocksum(rv, shift=0):
        sg, ab, uu = [], [], []
        for rg in rows:
            terms = [u[i] * rv[(i + shift) % L] for i in rg]
            sg.append(mp.fsum(terms))
            ab.append(mp.fsum(abs(t) for t in terms))
            uu.append(mp.fsum(u[i] * u[i] for i in rg))
        return sg, ab, uu

    sg, ab, uu = blocksum(r, 1 if mutate else 0)
    tot = mp.fsum(sg)
    # control (a): u_1^T r from the pinned step, -sigma_1 v_1^T dz_pinned
    dpin = printed(dpin8, layout(M, K), M)
    vt1 = float(V[:, 0] @ dpin)
    via = -float(sigma1) * vt1
    # the sign of v_1 in V and in x8 agree (the inverse iteration keeps it), checked by x8 . V[:, 0]
    sgn = float(mp.fsum(mp.mpf(float(V[i, 0])) * xv[i] for i in range(L)) / xn)
    rel_a = abs(float(tot) - via) / abs(via) if via else float("inf")
    # control (b): the planted residual
    beta = mp.mpf("1e-30")
    rp = [r[i] + beta * u[i] for i in range(L)]
    sgp, _, _ = blocksum(rp, 1 if mutate else 0)
    d_tot = (mp.fsum(sgp) - tot) / beta - 1
    d_blk = [float(abs((sgp[b] - sg[b]) / (beta * uu[b]) - 1)) if uu[b] != 0 else 0.0 for b in range(len(rows))]
    ok_b = bool(abs(d_tot) <= 1e-10 and max(d_blk) <= 1e-10)
    ok_a = bool(rel_a <= 1e-3 and np.sign(sgn) == 1)
    print(f"  u_1^T r = {mp.nstr(tot, 6)}; -sigma_1 v_1^T dz_pinned = {via:.6e} (v_1^T dz_pinned {vt1:+.4e}, v_1 signs agree {sgn:+.6f}): relative {rel_a:.2e} -> {'ok' if ok_a else 'FAIL'}", flush=True)
    print(f"  planted r + beta u_1 (beta 1e-30): total change/beta - 1 = {mp.nstr(d_tot, 3)}, largest block {max(d_blk):.1e} -> {'ok' if ok_b else 'FAIL'}", flush=True)
    sabs = mp.fsum(ab)
    order = sorted(range(len(rows)), key=lambda b: -ab[b])
    acc, named = mp.mpf(0), []
    for b in order:
        acc += ab[b]
        named.append(names[b])
        if acc >= 0.99 * sabs:
            break
    print("  block              max|r|       u_1^T r (signed)   sum |u_i r_i|   share of that sum   |u_1|^2 in the block", flush=True)
    for b in range(len(rows)):
        print(f"  {names[b]:16s} {rmax[b]:10.3e}   {mp.nstr(sg[b], 4):>16s}   {mp.nstr(ab[b], 4):>12s}   {float(ab[b] / sabs):10.4f}         {float(uu[b]):.4f}", flush=True)
    print(f"  blocks carrying 99% of sum |u_i r_i| ({mp.nstr(sabs, 4)}): {', '.join(named)}", flush=True)
    blocks = layout(M, K)
    rep = step_report(printed(dpin8, blocks, M), V, blocks, M)
    print(f"  pinned step: max {rep['max']:.3e}, norm {rep['norm']:.3e}, Delta {rep['delta']:+.3e}; V^T dz " + " ".join(f"{x:+.2e}" for x in rep["vt"]) +
          f"; sigma {' '.join(f'{x:.3e}' for x in sig)} (converged {' '.join(f'{x:.0e}' for x in conv)})", flush=True)
    rec = dict(state=st, D=float(m["D"]), pivots=[out[3], out[4]], sigma=[float(x) for x in sig], conv=[float(x) for x in conv], sigma1_exact=float(sigma1),
               r_max_by_block=dict(zip(names, rmax)), uTr_total=float(tot), uTr_signed=dict(zip(names, [float(x) for x in sg])), abs_sum=dict(zip(names, [float(x) for x in ab])),
               u_norm2=dict(zip(names, [float(x) for x in uu])), blocks_99=named, via_pinned_step=via, rel_a=rel_a, ok_a=ok_a, planted=dict(beta=1e-30, total=float(d_tot), blocks=d_blk, ok=ok_b),
               pinned_step=rep, mutate="shift" if mutate else "")
    if opts.get("out"):
        json.dump(rec, open(opts["out"], "w"), indent=1)
    ok = ok_a and ok_b
    print("check:", "pass" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
