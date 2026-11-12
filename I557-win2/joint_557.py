#!/usr/bin/env python3
"""#557: a joint fit of each sigma pair (sigma_1 with sigma_2, sigma_3 with sigma_4) with one shared period law (P0, p1, p2) and phase, separate amplitudes and separate trends, a trend degree chosen by a rule written before the fit
and applied to the training states only, then #533's two hold-outs and #535's twelve states out of sample.
usage: python joint_557.py [--selftest] [--trials N]       (run from I557-win2; needs ../I533-win2/period_p2_533.py, ../I535-win2/period_535.py and the logs they read)
Model for a pair (y_a, y_b) at D, with phi(D) = 2 pi int_228^D dD' / P(D'), P(D) = P0 + p1 x + p2 x^2, x = D - 228, u = x / 10:
  shared  (J2): y_s = trend_s(u) + a_s cos(phi + off),  s = a, b      nonlinear: P0, p1, p2, off;  linear: the two trends and a_a, a_b
  free    (J1): y_s = trend_s(u) + A_s cos(phi) + B_s sin(phi)        nonlinear: P0, p1, p2;       linear: the two trends and A_s, B_s (a phase of its own for each series)
Each series has its own polynomial trend of degree d_s. Fits are variable projection (the linear parameters by least squares on the stacked 2n rows with equal weights, the nonlinear ones by Nelder-Mead from the best three of 16
starts around the pair's nominal law).
The degree rule (fixed here, before any fit to the data): on the training states only, the last block of max(6, round(0.2 n)) states is left out, J2 is fitted to the rest for every (d_a, d_b) in {2, 3, 4}^2, the block is
predicted, and the pair of degrees with the smallest summed squared prediction error is taken (ties: the smaller d_a + d_b, then the smaller d_a); J2 is then fitted to all the training states with those degrees. The separate fits
of the benchmark use the same rule per series (degree in {2, 3, 4}), and the separate fits of #533 (degree 3 fixed) are quoted beside them.
Merge test: of N trials of (J2 fitted to the data) + white noise at J1's residual rms, the share whose R = (SS_J2 - SS_J1) / SS_J1 is at least the observed one (the null fraction); a small value rejects the merge (different phases).
Hold-outs: H1 fits D <= 232.7 and predicts D 233.13 to 237.13 (9 states); H2 fits D >= 214 and predicts D 210.13 to 213.63 (8); H3 fits D >= 210.13 (the 51 states of #533) and predicts #535's twelve states D 204.13 to 209.63.
Acceptance of #557: planted truth first; the joint fit's prediction rms for sigma_1 and sigma_2 at most 0.014 in H1, H2 and H3, the separate fits beside them (the check fails if any entry misses); sigma_3 and sigma_4 reported.
--selftest: P1 a planted shared oscillation (P0 2.62, p1 +0.0165, p2 +0.0003, off 0.7, amplitudes 0.112 and 0.110, cubic trends, noise 0.006, at the D of the 63 states): J2 recovers p2 to within 0.00015 and the shared
phase to within 0.1, the merge null fraction is at least 1%, the rule-based H1 prediction rms is at most 0.014 for both; P2 planted phases 0.6 rad apart: J2's residual exceeds J1's by more than 25% and the merge null fraction is below 1%."""
import itertools, math, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I535-win2", "I533-win2", "I525-win2", "I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import period_p2_533 as m  # noqa: E402
import period_535 as p5  # noqa: E402
D0 = 228.0
LIMIT = 0.014
NOMINAL = {(1, 2): (2.62, 0.0165), (3, 4): (2.20, 0.0058)}


def trend_cols(D, d):
    u = (D - D0) / 10.0
    return np.column_stack([u ** k for k in range(d + 1)])


def design(D, da, db, ph, off, mode):
    n = len(D)
    Ta, Tb = trend_cols(D, da), trend_cols(D, db)
    z = np.zeros(n)
    top = np.hstack([Ta, np.zeros((n, db + 1))])
    bot = np.hstack([np.zeros((n, da + 1)), Tb])
    if mode == "free":
        c, s = np.cos(ph), np.sin(ph)
        to, bo = np.column_stack([c, s, z, z]), np.column_stack([z, z, c, s])
    else:
        c = np.cos(ph + off)
        to, bo = np.column_stack([c, z]), np.column_stack([z, c])
    return np.vstack([np.hstack([top, to]), np.hstack([bot, bo])])


def ss_of(th, D, y2, da, db, mode):
    ph = m.phase(D, th[0], th[1], th[2])
    if ph is None:
        return 1e9
    X = design(D, da, db, ph, th[3] if mode == "shared" else 0.0, mode)
    beta = np.linalg.lstsq(X, y2, rcond=None)[0]
    e = y2 - X @ beta
    return float(e @ e)


def nm(f, x0, steps, maxfev=600):
    sim = [np.array(x0, float)] + [np.array(x0, float) + s for s in np.diag(steps)]
    r = minimize(f, x0, method="Nelder-Mead", options=dict(initial_simplex=np.array(sim), xatol=1e-6, fatol=1e-13, maxiter=maxfev, maxfev=maxfev))
    return r.x, r.fun


def fit_joint(D, ya, yb, da, db, mode, pair, extra_starts=()):
    y2 = np.concatenate([ya, yb])
    P0n, p1n = NOMINAL[pair]
    starts = []
    for P0 in (P0n, P0n + 0.04):
        for p1 in (p1n * 0.5, p1n):
            for off in ((0.0, 1.5, 3.0, 4.5) if mode == "shared" else (0.0,)):
                starts.append([P0, p1, 0.0002] + ([off] if mode == "shared" else []))
    starts += [list(s) for s in extra_starts]
    scored = sorted(((ss_of(s, D, y2, da, db, mode), i) for i, s in enumerate(starts)))[:3]
    steps = [0.03, 0.004, 0.0004] + ([0.5] if mode == "shared" else [])
    best = None
    for _, i in scored:
        x, f = nm(lambda th: ss_of(th, D, y2, da, db, mode), starts[i], steps)
        if best is None or f < best[1]:
            best = (x, f)
    return dict(theta=best[0], ss=best[1])


def predict(Dte, D, ya, yb, da, db, mode, theta):
    ph = m.phase(D, theta[0], theta[1], theta[2])
    off = theta[3] if mode == "shared" else 0.0
    X = design(D, da, db, ph, off, mode)
    beta = np.linalg.lstsq(X, np.concatenate([ya, yb]), rcond=None)[0]
    pte = m.phase(Dte, theta[0], theta[1], theta[2])
    Xt = design(Dte, da, db, pte, off, mode)
    pr = Xt @ beta
    n = len(Dte)
    return pr[:n], pr[n:], beta


def choose_degrees(D, ya, yb, pair):
    """the pre-registered rule, on the training states only"""
    n = len(D)
    k = max(6, int(round(0.2 * n)))
    tr, bl = slice(0, n - k), slice(n - k, n)
    best = None
    for da, db in itertools.product((2, 3, 4), (2, 3, 4)):
        f = fit_joint(D[tr], ya[tr], yb[tr], da, db, "shared", pair)
        pa, pb, _ = predict(D[bl], D[tr], ya[tr], yb[tr], da, db, "shared", f["theta"])
        sse = float(np.sum((ya[bl] - pa) ** 2) + np.sum((yb[bl] - pb) ** 2))
        key = (sse, da + db, da)
        if best is None or key < best[0]:
            best = (key, da, db)
    return best[1], best[2]


def choose_degree_single(D, y, pair_index):
    n = len(D)
    k = max(6, int(round(0.2 * n)))
    best = None
    for d in (2, 3, 4):
        F = m.Fitter(D[: n - k], d)
        f, _ = F.fit_free(y[: n - k])
        pr = m.predict(D[n - k:], D[: n - k], y[: n - k], d, f["theta"])
        sse = float(np.sum((y[n - k:] - pr) ** 2))
        key = (sse, d)
        if best is None or key < best[0]:
            best = (key, d)
    return best[1]


def rms(e):
    return float(math.sqrt(np.mean(np.asarray(e) ** 2)))


def holdout_pair(D, Y, pair, tr, te):
    """returns joint (rule), separate (rule), separate (cubic) prediction rms for both series of the pair"""
    ia, ib = pair[0] - 1, pair[1] - 1
    ya, yb = Y[:, ia], Y[:, ib]
    da, db = choose_degrees(D[tr], ya[tr], yb[tr], pair)
    f = fit_joint(D[tr], ya[tr], yb[tr], da, db, "shared", pair)
    pa, pb, _ = predict(D[te], D[tr], ya[tr], yb[tr], da, db, "shared", f["theta"])
    out = dict(deg=(da, db), joint=(rms(ya[te] - pa), rms(yb[te] - pb)), theta=f["theta"])
    sep_rule, sep_cubic = [], []
    for i, y in ((ia, ya), (ib, yb)):
        d = choose_degree_single(D[tr], y[tr], i)
        Fd = m.Fitter(D[tr], d)
        bd, _ = Fd.fit_free(y[tr])
        sep_rule.append((d, rms(y[te] - m.predict(D[te], D[tr], y[tr], d, bd["theta"]))))
        F3 = m.Fitter(D[tr], 3)
        b3, _ = F3.fit_free(y[tr])
        sep_cubic.append(rms(y[te] - m.predict(D[te], D[tr], y[tr], 3, b3["theta"])))
    out["sep_rule"], out["sep_cubic"] = sep_rule, sep_cubic
    return out


def merge_null(D, ya, yb, da, db, pair, trials, which, seed):
    fs = fit_joint(D, ya, yb, da, db, "shared", pair)
    ff = fit_joint(D, ya, yb, da, db, "free", pair, extra_starts=[list(fs["theta"][:3])])
    n2 = 2 * len(D)
    Robs = (fs["ss"] - ff["ss"]) / ff["ss"]
    pa, pb, _ = predict(D, D, ya, yb, da, db, "shared", fs["theta"])
    truth = np.concatenate([pa, pb])
    sig = math.sqrt(ff["ss"] / n2) if which == "free" else math.sqrt(fs["ss"] / n2)
    rng = np.random.default_rng(seed)
    hit = 0
    for _ in range(trials):
        yy = truth + rng.normal(0, sig, n2)
        a_, b_ = yy[: len(D)], yy[len(D):]
        s2 = fit_joint(D, a_, b_, da, db, "shared", pair)
        s1 = fit_joint(D, a_, b_, da, db, "free", pair, extra_starts=[list(s2["theta"][:3])])
        if (s2["ss"] - s1["ss"]) / s1["ss"] >= Robs:
            hit += 1
    return hit / trials, Robs, fs, ff


def planted_pair(D, offs, amps, seed, noise=0.006):
    u = (D - D0) / 10.0
    ph = m.phase(D, 2.62, 0.0165, 0.0003)
    ya = 0.3 - 11 * u + 1.5 * u ** 2 - 0.09 * u ** 3 + amps[0] * np.cos(ph + offs[0])
    yb = 0.1 - 10 * u + 1.2 * u ** 2 - 0.07 * u ** 3 + amps[1] * np.cos(ph + offs[1])
    rng = np.random.default_rng(seed)
    return ya + rng.normal(0, noise, len(D)), yb + rng.normal(0, noise, len(D))


def all_states():
    Do, Yo = m.collect51()
    new = p5.collect_new()
    Dn = np.array(sorted(new))
    Yn = np.array([np.mean(new[d], axis=0) for d in Dn])
    return np.concatenate([Dn, Do]), np.concatenate([Yn, Yo])


def selftest(trials=150):
    D, _ = all_states()
    pair = (1, 2)
    ok = True
    ya, yb = planted_pair(D, (0.7, 0.7), (0.112, 0.110), 31)
    da, db = 3, 3
    nf, Robs, fs, ff = merge_null(D, ya, yb, da, db, pair, trials, "free", 5)
    th = fs["theta"]
    print(f"P1 planted shared oscillation: J2 P0 {th[0]:.3f}, p1 {th[1]:+.4f}, p2 {th[2]:+.5f}, off {th[3] % (2 * math.pi):.3f} (planted 2.62, +0.0165, +0.0003, 0.7), rms {math.sqrt(fs['ss'] / (2 * len(D))):.4f}; merge null fraction {100 * nf:.1f}% (R {Robs:.3f})")
    good = abs(th[2] - 0.0003) <= 0.00015 and abs((th[3] - 0.7 + math.pi) % (2 * math.pi) - math.pi) <= 0.1 and nf >= 0.01
    Yp = np.column_stack([ya, yb, ya, yb])
    ho = holdout_pair(D, Yp, pair, D <= 232.7, D > 232.7)
    print(f"   rule-based H1: degrees {ho['deg']}, joint prediction rms {ho['joint'][0]:.4f}, {ho['joint'][1]:.4f}; separate (rule) {ho['sep_rule'][0][1]:.4f}, {ho['sep_rule'][1][1]:.4f}; separate (cubic) {ho['sep_cubic'][0]:.4f}, {ho['sep_cubic'][1]:.4f}")
    good = good and max(ho["joint"]) <= LIMIT
    print(f"   -> {'pass' if good else 'FAIL'}")
    ok = ok and good
    ya, yb = planted_pair(D, (0.7, 1.3), (0.112, 0.110), 32)
    nf, Robs, fs, ff = merge_null(D, ya, yb, 3, 3, pair, trials, "free", 6)
    r2, r1 = math.sqrt(fs["ss"] / (2 * len(D))), math.sqrt(ff["ss"] / (2 * len(D)))
    print(f"P2 planted phases 0.6 rad apart: J2 rms {r2:.4f}, J1 rms {r1:.4f}; merge null fraction {100 * nf:.1f}% (R {Robs:.3f})")
    good = fs["ss"] > 1.25 * ff["ss"] and nf < 0.01
    print(f"   -> {'pass' if good else 'FAIL'}")
    ok = ok and good
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 300
    if "--selftest" in sys.argv:
        sys.exit(selftest(trials if "--trials" in sys.argv else 150))
    D, Y = all_states()
    print(f"{len(D)} states D {D[0]:.4f} to {D[-1]:.4f}; {trials} merge trials; acceptance: joint prediction rms <= {LIMIT} for sigma_1, sigma_2 in H1, H2, H3")
    cfg = (("H1 fit D <= 232.7, predict D 233.13 to 237.13", (D >= 210.0) & (D <= 232.7), D > 232.7), ("H2 fit D >= 214, predict D 210.13 to 213.63", (D >= 214.0), (D < 214.0) & (D >= 210.0)),
           ("H3 fit D >= 210.13, predict #535's twelve states D 204.13 to 209.63", D >= 210.0, D < 210.0))
    res = {}
    for pair in ((1, 2), (3, 4)):
        print(f"\n== pair sigma_{pair[0]} + sigma_{pair[1]}")
        tr0 = D >= 210.0
        ya, yb = Y[tr0, pair[0] - 1], Y[tr0, pair[1] - 1]
        da, db = choose_degrees(D[tr0], ya, yb, pair)
        nf1, R1, fs, ff = merge_null(D[tr0], ya, yb, da, db, pair, trials, "free", 11)
        nf2, _, _, _ = merge_null(D[tr0], ya, yb, da, db, pair, trials, "m0", 12)
        th, tf = fs["theta"], ff["theta"]
        n2 = 2 * int(tr0.sum())
        print(f"fit to the 51 states D >= 210.13 (rule degrees {da}, {db}): shared P0 {th[0]:.4f}, p1 {th[1]:+.5f}, p2 {th[2]:+.6f}, off {th[3] % (2 * math.pi):.3f}, rms {math.sqrt(fs['ss'] / n2):.4f}; free phases rms {math.sqrt(ff['ss'] / n2):.4f}; merge null fraction {100 * nf1:.1f}% / {100 * nf2:.1f}%")
        for name, tr, te in cfg:
            ho = holdout_pair(D, Y, pair, tr, te)
            res[(pair, name[:2])] = ho
            print(f"{name}: degrees {ho['deg']}; joint {ho['joint'][0]:.4f}, {ho['joint'][1]:.4f}; separate (rule, degrees {ho['sep_rule'][0][0]}, {ho['sep_rule'][1][0]}) {ho['sep_rule'][0][1]:.4f}, {ho['sep_rule'][1][1]:.4f}; separate (cubic, as #533) {ho['sep_cubic'][0]:.4f}, {ho['sep_cubic'][1]:.4f}; shared law P0 {ho['theta'][0]:.3f}, p1 {ho['theta'][1]:+.4f}, p2 {ho['theta'][2]:+.5f}", flush=True)
    print("\n| pair | hold-out | joint rms (series a, b) | separate, rule rms | separate, cubic rms | meets 0.014 (joint) |\n|---|---|---|---|---|---|")
    ok = True
    for pair in ((1, 2), (3, 4)):
        for h in ("H1", "H2", "H3"):
            ho = res[(pair, h)]
            m_ = max(ho["joint"]) <= LIMIT
            if pair == (1, 2):
                ok = ok and m_
            print(f"| sigma_{pair[0]}, sigma_{pair[1]} | {h} | {ho['joint'][0]:.4f}, {ho['joint'][1]:.4f} | {ho['sep_rule'][0][1]:.4f}, {ho['sep_rule'][1][1]:.4f} | {ho['sep_cubic'][0]:.4f}, {ho['sep_cubic'][1]:.4f} | {'yes' if m_ else 'no'} |")
    print("\nacceptance (sigma_1, sigma_2 joint prediction rms <= 0.014 in H1, H2 and H3): " + ("pass" if ok else "FAIL"))
