#!/usr/bin/env python3
"""#565: a trend for the sigma pair sums that extrapolates in every hold-out.
usage: python trend_565.py [--selftest]       (run from I565-win2; needs ../I557-win2/joint_557.py and what it needs)
The sums y_s = ln sigma_a + ln sigma_b of the pairs (sigma_1, sigma_2) and (sigma_3, sigma_4) over the 63 states D 204.13 to 237.13 (no oscillation in them: #557's side look, #564), fitted by least squares with a trend form and
tested in #533's hold-outs: H1 fit D <= 232.7 and predict D 233.13 to 237.13 (9 states), H2 fit D >= 214 and predict D 210.13 to 213.63 (8), H3 fit D >= 210.13 and predict D 204.13 to 209.63 (12). In H1 and H2 the states below
D 210 are not used. The forms are fixed before any hold-out is computed, with z = D / 228:
  poly(d):  1, u, ..., u^d, u = (D - 228) / 10, d = 2, 3, 4 (the reference)       invD(d):  1, w, ..., w^d, w = 228 / D - 1        lnD(d):  1, l, ..., l^d, l = ln z
  B1: 1, z, z ln z, z^2          B2: 1, z, ln z, z^2
(eleven forms; columns scaled to unit norm before the least squares).
Acceptance of #565: the prediction rms of the sum is at most 0.007 in H1, H2 and H3 (so each series' half is at most 0.0035), the polynomials of degree 2 to 4 reported beside it; the check fails if any window misses. It is applied
to every form and to both pairs; a form 'passes' if it meets 0.007 in all three windows for the pair. The number of forms tried (eleven) is stated, since the best of several is selected with the hold-outs in view.
--selftest: planted sums at the D of the data: (a) a wrong form (poly(2) for a planted lnD(3)) misses 0.007 in some window; (b) with noise 0.004 (the noise of the real sum of sigma_1 + sigma_2) the TRUE form's median
prediction rms over 100 seeds is at most 0.007 in each window, and the share of seeds in which it meets 0.007 in all three windows is printed (about half: the criterion is tight for noise of this size; the real sum of
sigma_3 + sigma_4 has in-sample rms 0.0064 with a quartic, so that criterion cannot be met even by its true form); (c) the same truth with noise 0.02 misses 0.007 (the check can fail)."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I557-win2", "I535-win2", "I533-win2", "I525-win2", "I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import joint_557 as j  # noqa: E402
LIMIT = 0.007


def cols(D, form):
    z = D / 228.0
    u = (D - 228.0) / 10.0
    kind = form[0]
    if kind == "poly":
        return np.column_stack([u ** k for k in range(form[1] + 1)])
    if kind == "invD":
        w = 228.0 / D - 1.0
        return np.column_stack([w ** k for k in range(form[1] + 1)])
    if kind == "lnD":
        l = np.log(z)
        return np.column_stack([l ** k for k in range(form[1] + 1)])
    if kind == "B1":
        return np.column_stack([np.ones_like(z), z, z * np.log(z), z ** 2])
    if kind == "B2":
        return np.column_stack([np.ones_like(z), z, np.log(z), z ** 2])
    raise ValueError(form)


FORMS = [("poly", d) for d in (2, 3, 4)] + [("invD", d) for d in (2, 3, 4)] + [("lnD", d) for d in (2, 3, 4)] + [("B1", 0), ("B2", 0)]


def name(f):
    return f"{f[0]}({f[1]})" if f[0] in ("poly", "invD", "lnD") else f[0]


def fit_predict(Dtr, ytr, Dte, form):
    X = cols(Dtr, form)
    sc = np.linalg.norm(X, axis=0)
    c = np.linalg.lstsq(X / sc, ytr, rcond=None)[0]
    return (cols(Dte, form) / sc) @ c


def windows(D):
    return (("H1", D <= 232.7, D > 232.7), ("H2", D >= 214.0, (D < 214.0) & (D >= 210.0)), ("H3", D >= 210.0, D < 210.0))


def table(D, y):
    out = {}
    for f in FORMS:
        r = []
        for h, tr, te in windows(D):
            r.append(float(np.sqrt(np.mean((y[te] - fit_predict(D[tr], y[tr], D[te], f)) ** 2))))
        out[f] = r
    return out


def selftest():
    D, _ = j.all_states()
    ok = True
    l = np.log(D / 228.0)
    u = (D - 228.0) / 10.0
    truth_l = -230.0 - 160.0 * l + 700.0 * l ** 2 - 2500.0 * l ** 3
    truth_p = -230.0 - 20.0 * u + 3.0 * u ** 2 - 0.4 * u ** 3
    y = truth_l + np.random.default_rng(5).normal(0, 0.004, len(D))
    T = table(D, y)
    a2 = max(T[("poly", 2)]) > LIMIT
    print(f"(a) truth lnD(3), noise 0.004, one seed: poly(2) rms {', '.join(f'{v:.4f}' for v in T[('poly', 2)])} (a wrong form misses {LIMIT} somewhere: {a2})")
    ok = ok and a2
    for nm, tr, f in (("lnD(3)", truth_l, ("lnD", 3)), ("poly(3)", truth_p, ("poly", 3))):
        R = np.array([table(D, tr + np.random.default_rng(100 + s).normal(0, 0.004, len(D)))[f] for s in range(100)])
        med = np.median(R, axis=0)
        share = float(np.mean(R.max(axis=1) <= LIMIT))
        good = bool(np.all(med <= LIMIT))
        print(f"(b) truth {nm}, noise 0.004 (the noise of the real sum of sigma_1 + sigma_2), 100 seeds: the true form's median rms H1 {med[0]:.4f}, H2 {med[1]:.4f}, H3 {med[2]:.4f} (each <= {LIMIT}: {good}); share of seeds meeting {LIMIT} in all three: {100 * share:.0f}%")
        ok = ok and good
    y = truth_l + np.random.default_rng(7).normal(0, 0.02, len(D))
    T = table(D, y)
    c = max(T[("lnD", 3)]) > LIMIT
    print(f"(c) truth lnD(3), noise 0.02: lnD(3) rms {', '.join(f'{v:.4f}' for v in T[('lnD', 3)])} (misses {LIMIT}, the check can fail: {c})")
    ok = ok and c
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    D, Y = j.all_states()
    print(f"{len(D)} states D {D[0]:.4f} to {D[-1]:.4f}; {len(FORMS)} forms; criterion: the sum's prediction rms <= {LIMIT} in H1, H2 and H3")
    res = {}
    for pair in ((1, 2), (3, 4)):
        y = Y[:, pair[0] - 1] + Y[:, pair[1] - 1]
        T = table(D, y)
        res[pair] = T
        print(f"\n== sum ln sigma_{pair[0]} + ln sigma_{pair[1]}: prediction rms in H1, H2, H3 (fit on 42, 43 and 51 states)")
        print("| form | parameters | H1 | H2 | H3 | meets 0.007 in all three |\n|---|---|---|---|---|---|")
        for f in FORMS:
            r = T[f]
            n = cols(D[:3], f).shape[1] if f[0] in ("B1", "B2") else f[1] + 1
            print(f"| {name(f)} | {n} | {r[0]:.4f} | {r[1]:.4f} | {r[2]:.4f} | {'yes' if max(r) <= LIMIT else 'no'} |")
    print("\nsummary")
    for pair in ((1, 2), (3, 4)):
        passing = [name(f) for f in FORMS if max(res[pair][f]) <= LIMIT]
        poly = [name(f) for f in FORMS if f[0] == "poly" and max(res[pair][f]) <= LIMIT]
        print(f"sum sigma_{pair[0]} + sigma_{pair[1]}: forms meeting 0.007 in all three windows: {', '.join(passing) if passing else 'none'} (of {len(FORMS)} tried); polynomials among them: {', '.join(poly) if poly else 'none'}")
    ok = all(any(max(res[pair][f]) <= LIMIT for f in FORMS) for pair in ((1, 2), (3, 4)))
    print("acceptance (a form meets 0.007 in H1, H2 and H3 for each pair): " + ("pass" if ok else "FAIL"))
