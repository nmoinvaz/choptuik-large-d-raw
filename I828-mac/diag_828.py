#!/usr/bin/env python3
"""#828's diagnostic of g(0)'s first strong move with the horizon data eliminated (after curve_elim stopped there).
With reduced_cubic's Real, Elim (real_horizon, fast) and basis: (1) w0 by unknown block; (2) the full residual at
P(z0) + w0 with the horizon data held, max by row block, for w0, for each of its unknown blocks alone, and for its
Delta part times 1e-3 and 1e-6 (linearity); (3) the fast chord's history at P(z0) + w0; (4) unless --prod=0,
reseed's production projection at P(z0) + w0 (Reseeder.project and 3 octo-double corrections): how, the move of
m_h and a_h, max|F| on the eliminated rows after it, and |U^T F_red| there against |U^T F_red(P(z0))| and |B a|.
Diagnostic only: nothing is judged. usage (from hp/): python3 diag_828.py RAW DZ0 BASE [--threads=3] [--prod=1]"""
import os
import sys
import time

sys.path.insert(0, os.getcwd())
import numpy as np                 # noqa: E402
import reduced_cubic as rc         # noqa: E402  (from hp/, after the path)
from reduced_cubic import mp       # noqa: E402


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in argv if a.startswith("--") and "=" in a)

    def log(s):
        print(s, flush=True)
    base = rc.Real(*args[:3], int(opts.get("threads", 3)), log, fast=True)
    hc, hr, pr = rc.real_horizon(base, 3, fast=True, log=log)
    el = rc.Elim(base, hc, hr, pr, log)
    bas = rc.basis(el, {}, log, {}, lambda: None)
    Um, w0, nBa = bas["Um"], bas["w0"], bas["nBa"]
    M, K, L = base.M, base.K, base.L
    blocks = [("centre", range(0, 2 * M))] + [(f"node {i}", range(2 * M + 4 * M * i, 2 * M + 4 * M * (i + 1)))
                                              for i in range(K)] + [("Delta", [L - 1])]
    rblocks = [("rows 0..2M", range(0, 2 * M))] + [(f"node rows {i}", range(2 * M + 4 * M * i, 2 * M + 4 * M * (i + 1)))
                                                   for i in range(K - 1)] + \
        [(f"horizon {f}", range(4 * M * K + j * M, 4 * M * K + (j + 1) * M)) for j, f in enumerate("pma4")] + \
        [("last", [L - 1])]
    wf = [mp.mpf(0)] * L                            # w0 in the base's unknowns, horizon data 0
    for j, i in enumerate(el.keep):
        wf[i] = w0[j]
    p0 = el.p0
    log("  w0 by block, max|.|: " + ", ".join(f"{n} {mp.nstr(max(abs(wf[i]) for i in r), 3)}" for n, r in blocks))
    F0 = base.F(p0)

    def rowsum(F, label):
        log(f"    {label}: " + ", ".join(f"{n} {mp.nstr(max(abs(F[i]) for i in r), 3)}" for n, r in rblocks))
    rowsum(F0, "F at P(z0)")
    for name, part in [("w0", None)] + [(n, r) for n, r in blocks] + [("1e-3 Delta", "d3"), ("1e-6 Delta", "d6")]:
        v = list(wf) if part is None else [mp.mpf(0)] * L
        if part in ("d3", "d6"):
            v[L - 1] = wf[L - 1] * (mp.mpf("1e-3") if part == "d3" else mp.mpf("1e-6"))
        elif part is not None:
            for i in part:
                v[i] = wf[i]
        F = base.F([a + b for a, b in zip(p0, v)])
        rowsum([a - b for a, b in zip(F, F0)], f"F(P(z0) + {name}) - F(P(z0)), horizon data held")
    t1 = time.time()
    Fr = el.F(w0)
    log(f"  the fast chord at P(z0) + w0: max|F[hrows]| per step " + ", ".join(f"{x:.2e}" for x in pr.hist)
        + f" ({time.time() - t1:.0f} s); |U^T F_red| {mp.nstr(rc.nrm(rc.proj_U(Um, Fr)), 4)}, |B a| {mp.nstr(nBa, 4)}")
    if opts.get("prod", "1") == "1":
        from octo_corrector import q4_of_o, with_horizon
        rs = pr.rs
        z = base.o8(base.od_axpy(1.0, *base.parts8([a + b for a, b in zip(p0, wf)]), *base.z0))
        t1 = time.time()
        zp4, how = rs.project(q4_of_o(z))
        log(f"  the production projection at P(z0) + w0: '{how}' ({time.time() - t1:.0f} s), last stage "
            f"{getattr(rs, 'last_project', None)}")
        if how != "failed":
            zp = with_horizon(z, zp4, rs)
            dh = [a - b for a, b in zip(base.mpv(zp, hc), base.mpv(z, hc))]
            Fp = base.mpv(base.so.residual_o(zp), range(L))
            Fk = [Fp[r] for r in el.krows]
            log(f"    m_h moved {mp.nstr(max(abs(x) for x in dh[:M]), 3)}, a_h {mp.nstr(max(abs(x) for x in dh[M:]), 3)}; "
                f"refine_o {['%.2e' % x for x in rs.last_o]}; max|F[hrows]| {mp.nstr(max(abs(Fp[r]) for r in hr), 3)}; "
                f"|U^T F_red| {mp.nstr(rc.nrm(rc.proj_U(Um, Fk)), 4)} ({mp.nstr(rc.nrm(rc.proj_U(Um, Fk)) / nBa, 4)} "
                f"of |B a|), max|F_red| {mp.nstr(rc.amax(Fk), 4)}")
            rowsum([a - b for a, b in zip(Fp, F0)], "F at the projected P(z0) + w0 - F(P(z0))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
