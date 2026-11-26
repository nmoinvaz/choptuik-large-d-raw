"""Resample a form-S state from M to M' collocation points in theta (#1098's M budget), by its trigonometric series.

Layout (form_s.rs): z = p1, c0 | node i < K: p, m, c | m_h | Delta, each field M samples on the half grid
theta_j = 2 pi j / (2M), j < M. p, m (and p1, m_h) are odd under theta -> theta + pi: sum over odd k < M of
a_k cos(k theta) + b_k sin(k theta). c (and c0) is even: k = 0, 2, ..., M with the cosine at k = M (the Nyquist
term, sin(M theta_j) = 0 on the grid) and sines for 0 < k < M. A field's series is formed from its M samples at 160
digits from all eight parts and evaluated at the M' new points; the harmonics past M are zero (the resampled state is
the M-point solution's interpolant, which Newton then corrects at M').

    python3 resample_m.py STATE OUT M_NEW
"""
import sys

import numpy as np

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from mpmath import mp  # noqa: E402

from octo_corrector import load_o, save_o  # noqa: E402


def coeffs(vals, M, odd):
    """the series' (k, a_k, b_k) from M samples on the half grid"""
    N = 2 * M
    th = [2 * mp.pi * j / N for j in range(M)]
    out = []
    ks = range(1, M, 2) if odd else range(0, M + 1, 2)
    for k in ks:
        a = mp.fsum(v * mp.cos(k * t) for v, t in zip(vals, th))
        b = mp.fsum(v * mp.sin(k * t) for v, t in zip(vals, th))
        if odd:
            out.append((k, a * 2 / M, b * 2 / M))
        elif k == 0 or k == M:
            out.append((k, a / M, mp.mpf(0)))
        else:
            out.append((k, a * 2 / M, b * 2 / M))
    return out


def evaluate(cs, Mn):
    N = 2 * Mn
    return [mp.fsum(a * mp.cos(k * 2 * mp.pi * j / N) + b * mp.sin(k * 2 * mp.pi * j / N) for k, a, b in cs)
            for j in range(Mn)]


def main(path, out, Mn):
    z8, meta = load_o(path)
    M, K = int(meta["M"]), len(meta["nodes"])
    L = len(z8[0])
    assert L == 3 * M * (K + 1) + 1, (L, M, K)
    parity = [True, False] + [True, True, False] * K + [True]  # p1, c0 | p, m, c per node | m_h
    with mp.workdps(160):
        full = [mp.fsum(mp.mpf(float(z8[q][i])) for q in range(8)) for i in range(L)]
        newv = []
        for b, odd in enumerate(parity):
            vals = full[b * M:(b + 1) * M]
            cs = coeffs(vals, M, odd)
            back = evaluate(cs, M)
            err = max(abs(x - y) for x, y in zip(back, vals))
            if err > mp.mpf(10) ** -100 * max(abs(v) for v in vals) + mp.mpf(10) ** -140:
                raise SystemExit(f"block {b}: the series does not reproduce its samples ({mp.nstr(err, 3)})")
            newv += evaluate(cs, Mn)
        newv.append(full[-1])
        parts = [np.zeros(len(newv)) for _ in range(8)]
        for i, v in enumerate(newv):
            for q in range(8):
                parts[q][i] = float(v)
                v -= mp.mpf(parts[q][i])
    save_o(out, parts, dict(meta, M=Mn, resampled_from=f"{path.split('/')[-1]} at M {M}"))
    print(f"{path.split('/')[-1]}: M {M} -> {Mn}, {len(parity)} blocks, Delta kept; saved {out}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
