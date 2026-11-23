"""#1078: the radius of convergence of the horizon and centre series per tau-harmonic from the SCALED series coefficients, with the state's own (mapped) solver.

    cd hp && python3 radius_scaled.py STATE.npz M [--mutate=sigma]

highm_diag.py radius reads s.series(zh, zl, which) (unscaled c_k, which overflow to inf beyond the f64 range: at D 3.044375 the horizon series has 250 orders and a radius below
about 0.06, so the unscaled coefficients are inf and the fit is nan). Here s.series(..., scaled=True) gives c~_k = c_k sigma^k, sigma = s.series_scale(which); for c_k ~ r^-k the least-squares
slope of log |c~_n(k)| over the second half of the orders is ln(sigma / r), so r = sigma exp(-slope), and x / r is printed with x = u0 (horizon), x0 (centre). Harmonics: the same
transform as highm_diag (p, m odd and a, c even on the half grid, |rfft| / M, max over the fields). The check: where the unscaled fit is finite (the D 3.15 states), the two radii agree
to 1e-3 relative; --mutate=sigma doubles sigma, which must break it (exit 1)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.getcwd())
import lowD_gamma as LG  # noqa: E402
from hpkernel.driver import load  # noqa: E402

MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
path, M = args[0], int(args[1])
zh, zl, m = load(path)
s, grid = LG.build_solver(m["D"], M, m, 2)


def harmonics(c, M):
    amp = np.zeros((c.shape[0], M))
    for q in range(4):
        f = c[:, q, :]
        full = np.concatenate([f, -f if q < 2 else f], axis=1)
        amp = np.maximum(amp, np.abs(np.fft.rfft(full, axis=1))[:, :M] / M)
    return amp


def fit(amp, n, n0, k):
    y = amp[n0:, k]
    ok = (y > 0) & np.isfinite(y)
    if ok.sum() < 5:
        return None
    return np.polyfit(n[n0:][ok], np.log(y[ok]), 1)[0]


worst = 0.0
ks_ = list(range(1, 12, 2)) + list(range(M // 2 - 1, M, M // 8)) + [M - 1]
for which, x, name in ((1, 1 - m["nodes"][-1], "horizon (u0)"), (0, m["nodes"][0], "centre (x0)")):
    sig = s.series_scale(which) * (2.0 if MUT == "sigma" else 1.0)
    h, l = s.series(zh, zl, which, True)
    cs = (np.asarray(h) + np.asarray(l)).reshape(-1, 4, M)
    h2, l2 = s.series(zh, zl, which)
    cu = (np.asarray(h2) + np.asarray(l2)).reshape(-1, 4, M)
    nmax = cs.shape[0] - 1
    n = np.arange(nmax + 1)
    n0 = nmax // 2
    amp_s, amp_u = harmonics(cs, M), harmonics(np.where(np.isfinite(cu), cu, 0.0), M)
    bad_u = int((~np.isfinite(cu)).sum())
    tail = (amp_s.max(1) * (x / sig) ** n)[-3:].max()
    print(f"{name} = {x:.4g}: {nmax} terms, sigma {sig:.4g}, non-finite unscaled coefficients {bad_u}; tail max_k |c~_n(k)| (x/sigma)^n over the last 3 n: {tail:.1e}")
    for k in ks_:
        sl = fit(amp_s, n, n0, k)
        if sl is None:
            continue
        r = sig * np.exp(-sl)
        su = fit(amp_u, n, n0, k) if bad_u == 0 else None
        ru = None if su is None else np.exp(-su)
        if ru is not None:
            worst = max(worst, abs(r / ru - 1))
        print(f"  k {k:3d}: |c_0| {amp_s[0, k] / sig ** 0:.1e}, radius {r:.4f} (x/r = {x / r:.3f})" + ("" if ru is None else f"   [unscaled fit {ru:.4f}]"))
ok = worst < 1e-3
print(f"check: the scaled and the unscaled fits agree where the unscaled one is finite, largest relative difference {worst:.1e} (bar 1e-3): {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
