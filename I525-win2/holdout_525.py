#!/usr/bin/env python3
"""#525 part 1: a hold-out test of the chirp. Fit the chirp of #522 (quadratic trend + one sinusoid with period P(D) = P0 + p1 (D - 228)) to ln sigma_1..4 at the states with D <= 232.7 (30 states),
then predict the 9 states D 233.13 to 237.13 and compare. The control is the same fit with p1 = 0 (a constant period), predicted the same way.
usage: python holdout_525.py [--selftest]       (run from I525-win2; needs ../I522-win2/chirp_522.py, halfunit_522.py and the logs they read)
Two predictions per fit: (a) everything extrapolated (trend and oscillation), the pure hold-out; (b) the oscillation extrapolated, the trend refitted to all 39 states afterwards, which leaks the trend
(the quadratic trend extrapolated over 4.5 units can dominate the error) and holds out only the oscillation. Both are reported; (a) is the acceptance.
Acceptance of #525: the rms prediction error of ln sigma_1 and ln sigma_2 (a) is within 2 times their fit rms (0.007), i.e. at most 0.014, and the p1 = 0 control is reported beside it.
--selftest: 200 seeds of a planted chirp (P0 2.62, p1 +0.016, amplitude 0.11, noise 0.007) at the same D: the median prediction error of the p1 = 0 control must be at least twice the chirp's (the test tells
the drift from none), and 200 seeds of a planted constant period 2.60: the control's median error must be at most 0.014. The share of seeds in which the TRUE model meets the written limit 0.014 is printed:
the limit is not calibrated by the selftest, it is the one the issue wrote, and a real result is judged against it as written and read against that share."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I522-win2"))
import chirp_522 as c  # noqa: E402
import halfunit_522 as h  # noqa: E402

D0 = c.D0
J0 = int(np.argmin(np.abs(c.P1S)))
LIMIT = 0.014
CUT = 232.7


def phase(D, P0, p1):
    x = D - D0
    return 2 * np.pi * x / P0 if abs(p1) < 1e-12 else (2 * np.pi / p1) * np.log(1 + p1 * x / P0)


def design(D, P0, p1):
    u = (D - D0) / 10.0
    ph = phase(D, P0, p1)
    return np.column_stack([np.ones_like(D), u, u ** 2, np.cos(ph), np.sin(ph)])


class Trainer:
    def __init__(self, Dtr):
        self.Dtr = Dtr
        self.X, self.XtX, self.valid = c.build(Dtr)

    def fit(self, y, p1_zero):
        beta, ss = c.fit_grid(self.X, self.XtX, self.valid, y)
        if p1_zero:
            keep = np.full_like(ss, np.inf)
            keep[:, J0] = ss[:, J0]
            ss = keep
        i, j = np.unravel_index(np.argmin(ss), ss.shape)
        return c.P0S[i], c.P1S[j], beta[i, j], math.sqrt(ss[i, j] / len(y))


def holdout(D, y, cut=CUT):
    tr, te = D <= cut, D > cut
    T = Trainer(D[tr])
    out = {}
    for tag, p1z in (("chirp", False), ("p1=0", True)):
        P0, p1, b, rin = T.fit(y[tr], p1z)
        pred = design(D[te], P0, p1) @ b
        e = y[te] - pred
        # (b) the oscillation from the training fit, the trend refitted on all points
        osc = lambda DD: b[3] * np.cos(phase(DD, P0, p1)) + b[4] * np.sin(phase(DD, P0, p1))
        u = (D - D0) / 10.0
        co = np.polyfit(u, y - osc(D), 2)
        e2 = (y - osc(D) - np.polyval(co, u))[te]
        out[tag] = dict(P0=P0, p1=p1, rin=rin, rms=math.sqrt(np.mean(e ** 2)), mx=float(np.max(np.abs(e))), rms_b=math.sqrt(np.mean(e2 ** 2)), n_te=int(te.sum()), n_tr=int(tr.sum()))
    return out


def row(name, o):
    ch, z = o["chirp"], o["p1=0"]
    return (f"| {name} | {ch['P0']:.2f}, {ch['p1']:+.3f} | {ch['rin']:.4f} | {ch['rms']:.4f} ({ch['mx']:.4f}) | {ch['rms_b']:.4f} | {z['P0']:.2f} | {z['rin']:.4f} | {z['rms']:.4f} ({z['mx']:.4f}) | {z['rms_b']:.4f} |")


HEAD = ("| series | chirp P0, p1 (training) | chirp in-sample rms | chirp prediction rms (max) (a) | chirp (b) | p1 = 0: P | p1 = 0 in-sample rms | p1 = 0 prediction rms (max) (a) | p1 = 0 (b) |\n"
        "|---|---|---|---|---|---|---|---|---|")


def selftest(trials=200):
    D = np.array(sorted(h.collect()))
    D = D[D <= 237.2]
    u = (D - D0) / 10.0
    ok = True
    print(f"planted data at the same D, noise 0.007, {trials} seeds each; the written acceptance (chirp prediction rms <= {LIMIT}) applied to the true model")
    for name, P0, p1 in (("planted chirp (P0 2.62, p1 +0.016, amplitude 0.11)", 2.62, 0.016), ("planted constant period 2.60", 2.60, 0.0)):
        ch, z = [], []
        for seed in range(trials):
            rng = np.random.default_rng(1000 + seed)
            y = 0.3 - 11 * u + 1.5 * u ** 2 + 0.11 * np.sin(phase(D, P0, p1) + 0.7) + rng.normal(0, 0.007, len(D))
            o = holdout(D, y)
            ch.append(o["chirp"]["rms"]); z.append(o["p1=0"]["rms"])
        ch, z = np.array(ch), np.array(z)
        q = lambda a: " / ".join(f"{np.percentile(a, k):.4f}" for k in (50, 90))
        print(f"  {name}: chirp prediction rms median / 90th percentile {q(ch)}, p1 = 0 control {q(z)}; chirp <= {LIMIT} in {100 * np.mean(ch <= LIMIT):.0f}% of seeds, control <= {LIMIT} in {100 * np.mean(z <= LIMIT):.0f}%")
        if p1 != 0:
            ok = ok and np.median(z) >= 2 * np.median(ch)          # the test tells the drift from none
        else:
            ok = ok and np.median(z) <= LIMIT
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def bootstrap(D, y, trials=500):
    """parametric bootstrap of the hold-out: the chirp fitted to the training states is taken as the truth, white noise at its in-sample rms (scaled by sqrt(n / (n - 7))) is added at all D,
    and the hold-out is run again; returns the share of trials whose chirp prediction rms is at least the observed one, and the median and 90th percentile of the trials."""
    obs = holdout(D, y)["chirp"]
    tr = D <= CUT
    T = Trainer(D[tr])
    P0, p1, b, rin = T.fit(y[tr], False)
    sig = rin * math.sqrt(tr.sum() / (tr.sum() - 7))
    truth = design(D, P0, p1) @ b
    rng = np.random.default_rng(77)
    r = np.array([holdout(D, truth + rng.normal(0, sig, len(D)))["chirp"]["rms"] for _ in range(trials)])
    return float(np.mean(r >= obs["rms"])), float(np.median(r)), float(np.percentile(r, 90)), obs["rms"], sig


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    pts = h.collect()
    Ds = sorted(d for d in pts if d <= 237.2)
    D = np.array(Ds)
    Y = np.array([np.mean(pts[d], axis=0) for d in Ds])
    print(f"{len(D)} states D {D[0]:.4f} to {D[-1]:.4f}; training D <= {CUT} ({int((D <= CUT).sum())} states), test {', '.join(f'{d:.2f}' for d in D[D > CUT])}")
    print(HEAD)
    res = {}
    for i in (1, 2, 3, 4):
        res[i] = holdout(D, Y[:, i - 1])
        print(row(f"ln sigma_{i}", res[i]))
    print(f"\nacceptance (a): the chirp's rms prediction error of ln sigma_1 and ln sigma_2 is at most {LIMIT} (2 x 0.007)")
    ok = all(res[i]["chirp"]["rms"] <= LIMIT for i in (1, 2))
    for i in (1, 2):
        print(f"  ln sigma_{i}: chirp {res[i]['chirp']['rms']:.4f}, p1 = 0 {res[i]['p1=0']['rms']:.4f}: {'pass' if res[i]['chirp']['rms'] <= LIMIT else 'FAIL'}; the control {'is worse (the drift is needed)' if res[i]['p1=0']['rms'] > res[i]['chirp']['rms'] else 'predicts as well or better (the drift is not needed)'}")
    print("acceptance: pass" if ok else "acceptance: FAIL")
    if "--boot" in sys.argv:
        print(f"\nparametric bootstrap of the hold-out (diagnostic, not the acceptance): the chirp fitted to the 30 training states as the truth, white noise at its in-sample rms x sqrt(n/(n-7)), 500 trials")
        print("| series | noise used | observed chirp prediction rms | trials: median | trials: 90th percentile | share of trials at or above the observed |")
        print("|---|---|---|---|---|---|")
        for i in (1, 2, 3, 4):
            f, med, p90, o, sig = bootstrap(D, Y[:, i - 1])
            print(f"| ln sigma_{i} | {sig:.4f} | {o:.4f} | {med:.4f} | {p90:.4f} | {100 * f:.1f}% |")
