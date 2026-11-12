#!/usr/bin/env python3
"""#525 part 2, follow-up: residual_525.py found that a second sinusoid takes ln sigma_3 and ln sigma_4 to rms 0.0081 only with P2 = 15.00, the edge of its scan, which is a slow term and not a second oscillation.
Is the missing piece a higher-order trend? The 39 states refitted with the chirp of #522 and a trend of degree 2 (M0), 3 or 4 in u = (D - 228) / 10.
usage: python trend_525.py [--selftest] [--trials N]       (run from I525-win2; needs residual_525.py, ../I522-win2/chirp_522.py, halfunit_522.py and the logs they read)
Null fraction as in residual_525.py: of N trials of (M0 fitted to the data) + white noise, the share whose R = (SS_M0 - SS_deg) / SS_deg is at least the observed one, at the noise of (i) the degree-d model's
residual rms, (ii) M0's. Acceptance as for part 2: residual <= 0.008 with a null fraction below 1%.
--selftest (before the data): noise 0.0065 at the D of the data. S1 a planted chirp with a quadratic trend alone: neither degree 3 nor 4 may reach a null fraction below 1% (no false claim). S2 the same plus a planted cubic term
(0.2 u^3): degree 3 reaches residual <= 1.3 x noise with null fraction < 1% and recovers the cubic coefficient to within 25%."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import residual_525 as r  # noqa: E402
c, h = r.c, r.h
D0 = c.D0


def grid_columns_deg(D, deg):
    phi, valid = c.phases(D)
    u = ((D - D0) / 10.0)[None, None, :]
    one = np.ones_like(phi)
    cols = [one * u ** k for k in range(deg + 1)] + [np.cos(phi), np.sin(phi)]
    X = np.stack(cols, axis=-1)
    return X, np.einsum("ijkm,ijkn->ijmn", X, X), valid


class TrendModels:
    def __init__(self, D):
        self.D = D
        self.u = (D - D0) / 10.0
        self.g = {deg: grid_columns_deg(D, deg) for deg in (2, 3, 4)}

    def phi_of(self, P0, p1):
        x = self.D - D0
        return 2 * np.pi * x / P0 if abs(p1) < 1e-12 else (2 * np.pi / p1) * np.log(1 + p1 * x / P0)

    def fit(self, deg, y):
        ss, P0, p1, b = r.grid_fit(*self.g[deg], y)
        return dict(ss=ss, P0=P0, p1=p1, b=b)


def nullfrac(M, y, f0, fd, deg, trials, which, seed):
    n = len(y)
    ph = M.phi_of(f0["P0"], f0["p1"])
    b = f0["b"]
    truth = b[0] + b[1] * M.u + b[2] * M.u ** 2 + b[3] * np.cos(ph) + b[4] * np.sin(ph)
    sig = math.sqrt(fd["ss"] / n) if which == "ext" else math.sqrt(f0["ss"] / n)
    Robs = (f0["ss"] - fd["ss"]) / fd["ss"]
    rng = np.random.default_rng(seed)
    hit = 0
    for _ in range(trials):
        yy = truth + rng.normal(0, sig, n)
        a0, ad = M.fit(2, yy), M.fit(deg, yy)
        if (a0["ss"] - ad["ss"]) / ad["ss"] >= Robs:
            hit += 1
    return hit / trials


def report(name, M, y, trials, seed=3):
    n = len(y)
    f0 = M.fit(2, y)
    lines = [f"{name}: M0 (quadratic trend + chirp) rms {math.sqrt(f0['ss'] / n):.4f} (P0 {f0['P0']:.2f}, p1 {f0['p1']:+.3f})"]
    res = {}
    for deg in (3, 4):
        fd = M.fit(deg, y)
        a = nullfrac(M, y, f0, fd, deg, trials, "ext", seed)
        b = nullfrac(M, y, f0, fd, deg, trials, "m0", seed + 1)
        res[deg] = (math.sqrt(fd["ss"] / n), max(a, b), fd)
        lines.append(f"  degree {deg}: rms {math.sqrt(fd['ss'] / n):.4f} (P0 {fd['P0']:.2f}, p1 {fd['p1']:+.3f}, amplitude {math.hypot(fd['b'][deg + 1], fd['b'][deg + 2]):.4f}, "
                     f"trend coefficients in u {', '.join(f'{x:+.3f}' for x in fd['b'][:deg + 1])}); null fraction {100 * a:.1f}% (noise = this rms), {100 * b:.1f}% (noise = M0 rms)")
    return res, lines


def selftest(trials=150):
    D = np.array(sorted(d for d in h.collect() if d <= 237.2))
    M = TrendModels(D)
    n = len(D)
    u = (D - D0) / 10.0
    noise = 0.0065
    ph = M.phi_of(2.2, 0.004)
    base = 0.3 - 11 * u + 1.5 * u ** 2 + 0.124 * np.sin(ph + 0.7)
    ok = True
    for t, (name, truth) in enumerate((("S1 chirp + quadratic trend alone", base), ("S2 plus a cubic term 0.2 u^3", base + 0.2 * u ** 3))):
        y = truth + np.random.default_rng(60 + t).normal(0, noise, n)
        res, lines = report(name, M, y, trials, seed=9 + t)
        print("\n".join(lines))
        if t == 0:
            good = res[3][1] >= 0.01 and res[4][1] >= 0.01
        else:
            good = res[3][0] <= 1.3 * noise and res[3][1] < 0.01 and abs(res[3][2]["b"][3] - 0.2) <= 0.05
        print(f"  -> {name}: {'pass' if good else 'FAIL'}")
        ok = ok and good
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else (150 if "--selftest" in sys.argv else 300)
    if "--selftest" in sys.argv:
        sys.exit(selftest(trials))
    pts = h.collect()
    Ds = sorted(d for d in pts if d <= 237.2)
    D = np.array(Ds)
    Y = np.array([np.mean(pts[d], axis=0) for d in Ds])
    M = TrendModels(D)
    print(f"{len(D)} states D {D[0]:.4f} to {D[-1]:.4f}; {trials} null trials; acceptance: residual <= {r.LIMIT} with a null fraction below 1%")
    rows = []
    for i in (3, 4, 1, 2):
        res, lines = report(f"ln sigma_{i}", M, Y[:, i - 1], trials)
        print("\n".join(lines), flush=True)
        for deg in (3, 4):
            rows.append((i, deg, res[deg][0], res[deg][1], res[deg][0] <= r.LIMIT and res[deg][1] < 0.01))
    print("\n| series | trend degree | rms residual | worst null fraction | meets the acceptance |\n|---|---|---|---|---|")
    for i, deg, rm, nf, okk in rows:
        print(f"| ln sigma_{i} | {deg} | {rm:.4f} | {100 * nf:.1f}% | {'yes' if okk else 'no'} |")
