#!/usr/bin/env python3
"""fit_zero_pole.py LN_TABLE.txt [LO HI] | --selftest [--mutate]   (#1025 kc87_d2228125_fine; written after a first run on the real values, see the README)

Question: is the sign change of the hybrid det M(lambda) at D 22.28125 a simple zero or a simple pole of det? Model for ln|det| near the change, for each kind:
    zero:  y(l) = a + s (l - l0) + q (l - l0)^2 + ln|l - lc|
    pole:  y(l) = a + s (l - l0) + q (l - l0)^2 - ln|l - lc|        (l0 = -0.18)
(a, s, q by linear least squares for each trial lc on a grid of 1e-4 inside the bracket of the sign change; best lc = smallest rms residual.) Also a smooth cubic with no singular term.
This is an estimator over a model class, not an enclosure: the answer is 'which model class the ln|det| values prefer'.
Pass criteria of the selftest (written before it was run), planted noiseless ln|det| at the real lambdas -0.20 -0.19 -0.18 -0.17 -0.16 -0.12 -0.08, background a = -2401.5, s = -60, q = 0:
  planted zero at -0.1976: the zero fit has rms < 1e-6 and lc within 2e-4 of -0.1976; the pole fit has rms > 0.05;
  planted pole at -0.1976: the pole fit has rms < 1e-6 and lc within 2e-4; the zero fit has rms > 0.05;
  the same with Gaussian noise 0.02 (seed 1): the right kind has the smaller rms by a factor above 3 and lc within 2e-3.
--mutate flips the sign of the singular term in the zero model (so it fits poles): the selftest must then exit 1.
usage: fit_zero_pole.py joint/ln_table.txt -0.20 -0.08"""
import sys
import numpy as np

MUT = "--mutate" in sys.argv
L0 = -0.18


def fit(kind, lc, x, y):
    sg = 1.0 if kind == "zero" else -1.0
    if MUT:
        sg = -sg if kind == "zero" else sg
    A = np.vstack([np.ones_like(x), x - L0, (x - L0) ** 2]).T
    t = y - sg * np.log(np.abs(x - lc))
    c, *_ = np.linalg.lstsq(A, t, rcond=None)
    r = t - A @ c
    return c, float(np.sqrt((r ** 2).mean())), r


def best(kind, x, y, lo, hi):
    out = None
    for lc in np.arange(lo, hi + 1e-12, 1e-4):
        if np.min(np.abs(x - lc)) < 1e-9:
            continue
        c, rms, r = fit(kind, lc, x, y)
        if out is None or rms < out[0]:
            out = (rms, float(lc), c, r)
    return out


def planted(kind, x, lc=-0.1976, noise=0.0, seed=1):
    sg = 1.0 if kind == "zero" else -1.0
    y = -2401.5 + (-60.0) * (x - L0) + sg * np.log(np.abs(x - lc))
    if noise:
        y = y + np.random.default_rng(seed).normal(0.0, noise, size=x.shape)
    return y


def selftest():
    x = np.array([-0.20, -0.19, -0.18, -0.17, -0.16, -0.12, -0.08])
    lo, hi = -0.1999, -0.1901
    bad = []
    for kind in ("zero", "pole"):
        other = "pole" if kind == "zero" else "zero"
        y = planted(kind, x)
        a = best(kind, x, y, lo, hi)
        b = best(other, x, y, lo, hi)
        if not (a[0] < 1e-6 and abs(a[1] + 0.1976) < 2e-4 and b[0] > 0.05):
            bad.append("noiseless planted %s: right rms %.2e lc %.4f, wrong rms %.3f" % (kind, a[0], a[1], b[0]))
        y = planted(kind, x, noise=0.02)
        a = best(kind, x, y, lo, hi)
        b = best(other, x, y, lo, hi)
        if not (b[0] > 3 * a[0] and abs(a[1] + 0.1976) < 2e-3):
            bad.append("noisy planted %s: right rms %.4f lc %.4f, wrong rms %.4f" % (kind, a[0], a[1], b[0]))
    for m in bad:
        print("SELFTEST FAIL:", m)
    print("selftest %s" % ("FAILS" if bad else "passes"))
    return 1 if bad else 0


def main():
    a = [v for v in sys.argv[1:] if not v.startswith("--")]
    if "--selftest" in sys.argv:
        return selftest()
    rows = []
    for l in open(a[0]):
        t = l.split()
        try:
            rows.append((float(t[0]), int(t[1]), float(t[3])))
        except (ValueError, IndexError):
            continue
    lo, hi = float(a[1]), float(a[2])
    rows = [r for r in rows if lo - 1e-9 <= r[0] <= hi + 1e-9]
    x = np.array([r[0] for r in rows]); y = np.array([r[2] for r in rows]); sg = [r[1] for r in rows]
    ch = [(x[i], x[i + 1]) for i in range(len(x) - 1) if sg[i] != sg[i + 1]]
    print("points", len(x), "lambda", " ".join("%+.2f" % v for v in x), "| sign changes between", ch)
    br_lo, br_hi = ch[0][0] + 1e-4, ch[0][1] - 1e-4
    for kind in ("zero", "pole"):
        rms, lc, c, r = best(kind, x, y, br_lo, br_hi)
        print("%s: best lc %.4f (grid 1e-4 inside the bracket), rms residual %.4f, a %.4f, s %.2f, q %.1f, residuals %s" % (kind, lc, rms, c[0], c[1], c[2], " ".join("%+.3f" % v for v in r)))
    A = np.vstack([np.ones_like(x), x - L0, (x - L0) ** 2, (x - L0) ** 3]).T
    c, *_ = np.linalg.lstsq(A, y, rcond=None); r = y - A @ c
    print("smooth cubic (no singular term): rms residual %.4f, residuals %s" % (np.sqrt((r ** 2).mean()), " ".join("%+.3f" % v for v in r)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
