#!/usr/bin/env python3
"""#522 part 1: a chirp fit of ln sigma_i against D, D 216 to 237 (28 distinct D): a quadratic trend plus one sinusoid whose period drifts linearly with D.
usage: python chirp_522.py [--selftest] [--trials N]     (run from I522-win2; needs ../I521-win2/analysis_521.py and the logs of #505, #510, #511, #515, #516, #521)
Model: y = c0 + c1 u + c2 u^2 + A cos(phi) + B sin(phi), u = (D - 228) / 10, phi(D) = (2 pi / p1) ln(1 + p1 (D - 228) / P0) (for p1 = 0, 2 pi (D - 228) / P0): the instantaneous period is P(D) = P0 + p1 (D - 228).
The grid is P0 in 1.50..3.50 step 0.01, p1 in -0.12..0.12 step 0.002 (a design is dropped where 1 + p1 (D - 228) / P0 <= 0.05 anywhere in the data); the five linear parameters by least squares
(normal equations on scaled columns, batched over the grid). Amplitude error by the delta method from s^2 (X^T X)^-1 at the best grid point; the interval of p1 = the values of p1 whose best sum of squares (over P0) is
within one residual variance of the minimum. Null fractions from 1000 trials of a pure line + white noise: (i) of the observed fit's residual rms (the convention of #516 to #521), (ii) the stricter one, of the residual rms of the
quadratic trend alone (no sinusoid); a trial counts if its best amplitude / error is at least the observed one.
Rule of #522: if the chirp fit reaches the residuals of the two half fits (about 0.005) with a null fraction below 1%, one oscillation with a drifting period describes both halves, and its drift rate is reported.
--selftest: a planted chirp (P0 2.6, p1 -0.02, amplitude 0.12, noise 0.005) at the same D is recovered (p1 within 0.006, P0 within 0.05, null fraction 0.0%), and a planted constant period is fitted with p1 consistent with 0."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I521-win2"))
import analysis_521 as a21  # noqa: E402

D0 = 228.0
P0S = np.arange(1.50, 3.50 + 1e-9, 0.01)
P1S = np.arange(-0.12, 0.12 + 1e-9, 0.002)
PP0, PP1 = np.meshgrid(P0S, P1S, indexing="ij")


def phases(D):
    """phi[i, j, k] for P0 index i, p1 index j, data index k, and a validity mask"""
    x = (D - D0)[None, None, :]
    arg = 1.0 + PP1[:, :, None] * x / PP0[:, :, None]
    valid = np.all(arg > 0.05, axis=2)
    arg = np.where(arg > 0.05, arg, 1.0)
    small = np.abs(PP1[:, :, None]) < 1e-12
    p1 = np.where(small, 1.0, PP1[:, :, None])
    phi = np.where(small, 2 * np.pi * x / PP0[:, :, None], (2 * np.pi / p1) * np.log(arg))
    return phi, valid


def build(D):
    phi, valid = phases(D)
    u = (D - D0) / 10.0
    n = len(D)
    X = np.empty(phi.shape[:2] + (n, 5))
    X[..., 0] = 1.0
    X[..., 1] = u
    X[..., 2] = u ** 2
    X[..., 3] = np.cos(phi)
    X[..., 4] = np.sin(phi)
    XtX = np.einsum("ijkm,ijkn->ijmn", X, X)
    return X, XtX, valid


def fit_grid(X, XtX, valid, y):
    Xty = np.einsum("ijkm,k->ijm", X, y)
    # a tiny ridge keeps near-collinear designs finite
    A = XtX + 1e-12 * np.eye(5)[None, None]
    beta = np.linalg.solve(A, Xty[..., None])[..., 0]
    pred = np.einsum("ijkm,ijm->ijk", X, beta)
    ss = np.sum((y[None, None, :] - pred) ** 2, axis=2)
    ss = np.where(valid, ss, np.inf)
    return beta, ss


def best(X, XtX, valid, y):
    beta, ss = fit_grid(X, XtX, valid, y)
    i, j = np.unravel_index(np.argmin(ss), ss.shape)
    return i, j, beta[i, j], ss


def stats(X, XtX, valid, y):
    i, j, b, ss = best(X, XtX, valid, y)
    n = len(y)
    dof = n - 7                       # five linear parameters, P0 and p1
    s2 = ss[i, j] / dof
    cov = s2 * np.linalg.inv(XtX[i, j])
    A, B = b[3], b[4]
    amp = math.hypot(A, B)
    g = np.array([A, B]) / amp
    err = math.sqrt(g @ cov[3:5, 3:5] @ g)
    thr = ss[i, j] * (1 + 1.0 / dof)
    prof = np.min(ss, axis=0)         # best sum of squares for each p1
    okp = P1S[prof <= thr]
    return dict(P0=P0S[i], p1=P1S[j], amp=amp, err=err, ratio=amp / err, rms=math.sqrt(ss[i, j] / n), p1lo=okp.min(), p1hi=okp.max(), dof=dof, ss=ss[i, j], b=b)


def nullfrac(D, X, XtX, valid, sigma, ratio, trials, seed=5):
    rng = np.random.default_rng(seed)
    hit = 0
    for _ in range(trials):
        yy = -1.1 * (D - D.mean()) + rng.normal(0, sigma, len(D))
        r = stats(X, XtX, valid, yy)
        if r["ratio"] >= ratio:
            hit += 1
    return hit / trials


def quad_rms(D, y):
    u = (D - D0) / 10.0
    c = np.polyfit(u, y, 2)
    return float(np.sqrt(np.mean((y - np.polyval(c, u)) ** 2)))


def analyse(name, D, y, X, XtX, valid, trials, out=print):
    r = stats(X, XtX, valid, y)
    s_strict = quad_rms(D, y)
    nf1 = nullfrac(D, X, XtX, valid, r["rms"], r["ratio"], trials)
    nf2 = nullfrac(D, X, XtX, valid, s_strict, r["ratio"], trials, seed=6)
    pa, pb = r["P0"] + r["p1"] * (216.1 - D0), r["P0"] + r["p1"] * (237.1 - D0)
    out(f"  {name}: P0 = {r['P0']:.2f} at D 228, drift p1 = {r['p1']:+.3f} per unit of D (interval {r['p1lo']:+.3f} to {r['p1hi']:+.3f}), so P = {pa:.2f} at D 216 and {pb:.2f} at D 237; amplitude {r['amp']:.4f} +- {r['err']:.4f} "
        f"(ratio {r['ratio']:.1f}), rms residual {r['rms']:.4f} (quadratic trend alone: {s_strict:.4f}); null fraction {100 * nf1:.1f}% (noise = observed rms), {100 * nf2:.1f}% (noise = trend-alone rms)")
    return r, nf1, nf2


def selftest():
    D = np.array(sorted({round(d, 4) for d in list(np.arange(216.1312, 232.2, 1.0)) + list(np.arange(232.6312, 237.2, 0.5))}))
    X, XtX, valid = build(D)
    rng = np.random.default_rng(1)
    u = (D - D0) / 10
    P0, p1 = 2.6, -0.02
    phi = (2 * np.pi / p1) * np.log(1 + p1 * (D - D0) / P0)
    y = 0.3 - 11 * u + 1.5 * u ** 2 + 0.12 * np.sin(phi + 0.7) + rng.normal(0, 0.005, len(D))
    sink = []
    r, nf1, nf2 = analyse("planted chirp", D, y, X, XtX, valid, 200, out=sink.append)
    print(sink[0])
    ok1 = abs(r["p1"] - p1) <= 0.006 and abs(r["P0"] - P0) <= 0.05 and nf1 < 0.01 and r["p1lo"] <= p1 <= r["p1hi"] + 0.002
    y2 = 0.3 - 11 * u + 1.5 * u ** 2 + 0.12 * np.sin(2 * np.pi * (D - D0) / 2.6 + 0.7) + rng.normal(0, 0.005, len(D))
    sink = []
    r2, _, _ = analyse("planted constant period", D, y2, X, XtX, valid, 100, out=sink.append)
    print(sink[0])
    ok2 = r2["p1lo"] - 0.002 <= 0.0 <= r2["p1hi"] + 0.002 and abs(r2["P0"] - 2.6) <= 0.05
    print("selftest: ok" if ok1 and ok2 else f"selftest FAILED: chirp recovered {ok1}, constant period consistent with p1 = 0 {ok2}")
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 1000
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    pts = a21.collect()
    Ds = sorted(d for d in pts if d <= 237.2)
    D = np.array(Ds)
    Y = np.array([np.mean(pts[d], axis=0) for d in Ds])
    print(f"{len(D)} distinct D from {D[0]:.4f} to {D[-1]:.4f}; grid P0 {P0S[0]:.2f}..{P0S[-1]:.2f} ({len(P0S)}), p1 {P1S[0]:+.3f}..{P1S[-1]:+.3f} ({len(P1S)}); {trials} null trials")
    X, XtX, valid = build(D)
    print(f"valid designs: {int(valid.sum())} of {valid.size}")
    for i in (1, 2, 3, 4):
        analyse(f"ln sigma_{i}", D, Y[:, i - 1], X, XtX, valid, trials)
