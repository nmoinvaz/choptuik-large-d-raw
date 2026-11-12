#!/usr/bin/env python3
"""#525 part 2: what is left in ln sigma_3 and ln sigma_4 after the chirp? The 39 states D 216 to 237 refitted with (M0) the chirp of #522, (M1) the chirp with an amplitude linear in D, (M2h) the chirp plus its
second harmonic, and (M2s) the chirp plus a second sinusoid of its own constant period (scanned 1.1 to 15).
usage: python residual_525.py [--selftest] [--trials N]       (run from I525-win2; needs ../I522-win2/chirp_522.py, halfunit_522.py and the logs they read)
Models: trend = c0 + c1 u + c2 u^2, u = (D - 228) / 10; chirp phase phi(D) = (2 pi / p1) ln(1 + p1 (D - 228) / P0), period P(D) = P0 + p1 (D - 228), P0 on 1.50..3.50 step 0.01, p1 on -0.12..0.12 step 0.002.
M0:  trend + A cos(phi) + B sin(phi).            M1:  M0 + u (A' cos(phi) + B' sin(phi)), i.e. an amplitude linear in D.      M2h: M0 + C cos(2 phi) + S sin(2 phi).
M2s: M0 + C cos(2 pi D / P2) + S sin(2 pi D / P2): staged, (P0, p1) from M0, then P2 scanned on a grid of step 0.01, then (P0, p1) rescanned with P2 fixed, twice.
Null fraction: of 300 trials of (M0 fitted to the data) + white noise, the share whose relative drop in the sum of squares from M0 to the extended model, R = (SS0 - SSext) / SSext, is at least the observed one;
the extended model's whole scan is repeated in each trial. Two noise levels, as in #522: (i) the extended model's residual rms, (ii) M0's residual rms (stricter).
Acceptance of #525: the residual falls to 0.008 or less with a null fraction below 1%, or the report names the model that did not.
--selftest (the planted-truth protocol, run before the data): at the D of the data, noise 0.0065,
  T1 a planted chirp alone (P0 2.2, p1 +0.004, amplitude 0.124, like sigma_3): no extended model may reach residual <= 0.008 with null fraction < 1% and also be better than M0 by more than chance, i.e. each null fraction >= 1%;
  T2 a planted amplitude slope (A(u) = 0.124 (1 + 0.6 u)): M1 recovers the slope 0.6 to within 0.15 with residual <= 1.3 x noise and null fraction < 1%;
  T3 a planted second harmonic (0.04 at 2 phi): M2h recovers its amplitude to within 0.01 with residual <= 1.3 x noise and null fraction < 1%;
  T4 a planted second sinusoid (P2 5.3, amplitude 0.04): M2s recovers P2 to within 0.1 with residual <= 1.3 x noise and null fraction < 1%."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I522-win2"))
import chirp_522 as c  # noqa: E402
import halfunit_522 as h  # noqa: E402

D0 = c.D0
P2S = np.arange(1.1, 15.0 + 1e-9, 0.01)
LIMIT = 0.008


def grid_columns(D, kind, fixed=None):
    """X[i, j, k, m] for the (P0, p1) grid; fixed = (cos, sin) of a fixed second sinusoid for M2s."""
    phi, valid = c.phases(D)
    u = ((D - D0) / 10.0)[None, None, :]
    one = np.ones_like(phi)
    cols = [one, one * u, one * u ** 2, np.cos(phi), np.sin(phi)]
    if kind == "M1":
        cols += [u * np.cos(phi), u * np.sin(phi)]
    elif kind == "M2h":
        cols += [np.cos(2 * phi), np.sin(2 * phi)]
    elif kind == "M2s":
        cols += [one * fixed[0][None, None, :], one * fixed[1][None, None, :]]
    X = np.stack(cols, axis=-1)
    return X, np.einsum("ijkm,ijkn->ijmn", X, X), valid


def grid_fit(X, XtX, valid, y):
    m = X.shape[-1]
    Xty = np.einsum("ijkm,k->ijm", X, y)
    beta = np.linalg.solve(XtX + 1e-12 * np.eye(m)[None, None], Xty[..., None])[..., 0]
    ss = np.sum((y[None, None, :] - np.einsum("ijkm,ijm->ijk", X, beta)) ** 2, axis=2)
    ss = np.where(valid, ss, np.inf)
    i, j = np.unravel_index(np.argmin(ss), ss.shape)
    return ss[i, j], c.P0S[i], c.P1S[j], beta[i, j]


class Models:
    def __init__(self, D):
        self.D = D
        self.u = (D - D0) / 10.0
        self.g = {k: grid_columns(D, k) for k in ("M0", "M1", "M2h")}
        w = 2 * np.pi / P2S
        self.c2 = np.cos(w[:, None] * D[None, :])            # (nP2, n)
        self.s2 = np.sin(w[:, None] * D[None, :])

    def phi_of(self, P0, p1):
        x = self.D - D0
        return 2 * np.pi * x / P0 if abs(p1) < 1e-12 else (2 * np.pi / p1) * np.log(1 + p1 * x / P0)

    def fit_basic(self, kind, y):
        ss, P0, p1, b = grid_fit(*self.g[kind], y)
        return dict(ss=ss, P0=P0, p1=p1, b=b)

    def fit_M2s(self, y, start):
        P0, p1 = start["P0"], start["p1"]
        n = len(y)
        best = None
        for _ in range(2):
            ph = self.phi_of(P0, p1)
            base = np.column_stack([np.ones(n), self.u, self.u ** 2, np.cos(ph), np.sin(ph)])
            X = np.concatenate([np.broadcast_to(base, (len(P2S), n, 5)), self.c2[:, :, None], self.s2[:, :, None]], axis=2)
            XtX = np.einsum("pkm,pkn->pmn", X, X)
            beta = np.linalg.solve(XtX + 1e-12 * np.eye(7)[None], np.einsum("pkm,k->pm", X, y)[..., None])[..., 0]
            ss = np.sum((y[None, :] - np.einsum("pkm,pm->pk", X, beta)) ** 2, axis=1)
            q = int(np.argmin(ss))
            Xg = grid_columns(self.D, "M2s", fixed=(self.c2[q], self.s2[q]))
            ssg, P0, p1, b = grid_fit(*Xg, y)
            best = dict(ss=ssg, P0=P0, p1=p1, b=b, P2=float(P2S[q]))
        return best

    def fit_all(self, y, kinds=("M1", "M2h", "M2s")):
        out = {"M0": self.fit_basic("M0", y)}
        for k in kinds:
            out[k] = self.fit_basic(k, y) if k != "M2s" else self.fit_M2s(y, out["M0"])
        return out


def rms(f, n):
    return math.sqrt(f["ss"] / n)


def amp_at(b, u):
    return math.hypot(b[3] + b[5] * u, b[4] + b[6] * u)


def nullfrac(M, y, fits, kind, trials, which, seed):
    """share of trials of (M0 fit) + white noise with R >= the observed R; which = 'ext' (noise at the extended model's rms) or 'm0' (noise at M0's rms)"""
    n = len(y)
    truth = M.D * 0.0
    ph = M.phi_of(fits["M0"]["P0"], fits["M0"]["p1"])
    b = fits["M0"]["b"]
    truth = b[0] + b[1] * M.u + b[2] * M.u ** 2 + b[3] * np.cos(ph) + b[4] * np.sin(ph)
    sig = rms(fits[kind], n) if which == "ext" else rms(fits["M0"], n)
    Robs = (fits["M0"]["ss"] - fits[kind]["ss"]) / fits[kind]["ss"]
    rng = np.random.default_rng(seed)
    hit = 0
    for _ in range(trials):
        yy = truth + rng.normal(0, sig, n)
        f = M.fit_all(yy, kinds=(kind,))
        if (f["M0"]["ss"] - f[kind]["ss"]) / f[kind]["ss"] >= Robs:
            hit += 1
    return hit / trials


def report(name, M, y, trials, seed=3):
    n = len(y)
    fits = M.fit_all(y)
    lines = [f"{name}: M0 chirp rms {rms(fits['M0'], n):.4f} (P0 {fits['M0']['P0']:.2f}, p1 {fits['M0']['p1']:+.3f})"]
    nf = {}
    for k in ("M1", "M2h", "M2s"):
        f = fits[k]
        extra = ""
        if k == "M1":
            extra = f", amplitude {amp_at(f['b'], (216.1 - D0) / 10):.4f} at D 216, {amp_at(f['b'], 0.0):.4f} at D 228, {amp_at(f['b'], (237.1 - D0) / 10):.4f} at D 237 (slope per unit u: {amp_at(f['b'], 1.0) / amp_at(f['b'], 0.0) - 1:+.3f} of the D 228 value)"
        elif k == "M2h":
            extra = f", second-harmonic amplitude {math.hypot(f['b'][5], f['b'][6]):.4f}, first {math.hypot(f['b'][3], f['b'][4]):.4f}"
        elif k == "M2s":
            extra = f", P2 {f['P2']:.2f}, amplitude {math.hypot(f['b'][5], f['b'][6]):.4f}, first {math.hypot(f['b'][3], f['b'][4]):.4f}"
        a = nullfrac(M, y, fits, k, trials, "ext", seed)
        b = nullfrac(M, y, fits, k, trials, "m0", seed + 1)
        nf[k] = (a, b)
        lines.append(f"  {k}: rms {rms(f, n):.4f} (P0 {f['P0']:.2f}, p1 {f['p1']:+.3f}{extra}); null fraction {100 * a:.1f}% (noise = this rms), {100 * b:.1f}% (noise = M0 rms)")
    return fits, nf, lines


def selftest(trials=150):
    D = np.array(sorted(d for d in h.collect() if d <= 237.2))
    M = Models(D)
    n = len(D)
    u = (D - D0) / 10.0
    noise = 0.0065
    P0, p1, A = 2.2, 0.004, 0.124
    ph = M.phi_of(P0, p1)
    trend = 0.3 - 11 * u + 1.5 * u ** 2
    cases = {
        "T1 chirp alone": trend + A * np.sin(ph + 0.7),
        "T2 amplitude slope 0.6": trend + A * (1 + 0.6 * u) * np.sin(ph + 0.7),
        "T3 second harmonic 0.04": trend + A * np.sin(ph + 0.7) + 0.04 * np.sin(2 * ph + 0.3),
        "T4 second sinusoid P2 5.3, 0.04": trend + A * np.sin(ph + 0.7) + 0.04 * np.sin(2 * np.pi * D / 5.3 + 0.4),
    }
    ok = True
    for t, (name, truth) in enumerate(cases.items()):
        y = truth + np.random.default_rng(40 + t).normal(0, noise, n)
        fits, nf, lines = report(name, M, y, trials, seed=7 + t)
        print("\n".join(lines))
        r = lambda k: rms(fits[k], n)
        if t == 0:
            good = all(nf[k][0] >= 0.01 or r(k) > LIMIT or True for k in nf)          # reported; the check is the next line
            good = all(max(nf[k]) >= 0.01 for k in nf)
        elif t == 1:
            slope = amp_at(fits["M1"]["b"], 1.0) / amp_at(fits["M1"]["b"], 0.0) - 1
            good = abs(slope - 0.6) <= 0.15 and r("M1") <= 1.3 * noise and max(nf["M1"]) < 0.01
        elif t == 2:
            good = abs(math.hypot(fits["M2h"]["b"][5], fits["M2h"]["b"][6]) - 0.04) <= 0.01 and r("M2h") <= 1.3 * noise and max(nf["M2h"]) < 0.01
        else:
            good = abs(fits["M2s"]["P2"] - 5.3) <= 0.1 and r("M2s") <= 1.3 * noise and max(nf["M2s"]) < 0.01
        print(f"  -> {name}: {'pass' if good else 'FAIL'}")
        ok = ok and good
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 300
    if "--selftest" in sys.argv:
        sys.exit(selftest(int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 150))
    pts = h.collect()
    Ds = sorted(d for d in pts if d <= 237.2)
    D = np.array(Ds)
    Y = np.array([np.mean(pts[d], axis=0) for d in Ds])
    M = Models(D)
    print(f"{len(D)} states D {D[0]:.4f} to {D[-1]:.4f}; {trials} null trials; acceptance: residual <= {LIMIT} with a null fraction below 1%")
    summary = []
    for i in (3, 4, 1, 2):
        fits, nf, lines = report(f"ln sigma_{i}", M, Y[:, i - 1], trials)
        print("\n".join(lines), flush=True)
        for k in ("M1", "M2h", "M2s"):
            r = rms(fits[k], len(D))
            summary.append((i, k, r, max(nf[k]), r <= LIMIT and max(nf[k]) < 0.01))
    print("\n| series | model | rms residual | worst null fraction | meets the acceptance |\n|---|---|---|---|---|")
    for i, k, r, nfw, okk in summary:
        print(f"| ln sigma_{i} | {k} | {r:.4f} | {100 * nfw:.1f}% | {'yes' if okk else 'no'} |")
