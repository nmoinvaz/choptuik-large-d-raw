#!/usr/bin/env python3
"""#564: the antiphase pair model for the sigma oscillation. Each pair (a, b) = (sigma_1, sigma_2) and (sigma_3, sigma_4) is fitted as one smooth sum S plus an antiphase oscillation of one amplitude with a shared period law:
  ln sigma_a = S/2 - T/2,   ln sigma_b = S/2 + T/2,   T(D) = c + c1 u + A cos phi + B sin phi,
  phi(D) = 2 pi int_228^D dD' / P(D'), P(D) = P0 + p1 x + p2 x^2, x = D - 228, u = x / 10; S a polynomial in u.
The model of the issue is M0, T = c + A cos phi + B sin phi (a constant c and the oscillation; A cos phi + B sin phi = a cos(phi + off)). M1 adds the linear term c1 u to T. With y_s = ln sigma_a + ln sigma_b and
y_d = ln sigma_b - ln sigma_a the model is y_s = S and y_d = T, and the least squares of the stacked pair is the sum of two independent fits: S by a polynomial on the sums, T on the differences.
M1 is a change made after the first fit, before any state of #558 was read: M0 does not fit the 63 states (rms of the difference 0.061 against 0.011 with c1), because the difference has a linear trend. #557's side look said
the differences carry no trend; it only showed that they carry none beyond degree 1 (its fits started at degree 1), which is corrected on #557. Both models' predictions are written and both are judged.
usage: python antiphase_564.py [--selftest] [--predict]       (run from I564-win2; needs ../I557-win2/joint_557.py, ../I533-win2/period_p2_533.py and what they need)
The degree rule for S (fixed before any fit of this task and before any state of #558 is read; it is #557's rule applied to the sums): on the training states, the last block of max(6, round(0.2 n)) states is left out, the
polynomial of degree d in {2, 3, 4} is fitted to the rest and predicts the block, and the degree with the smallest squared error is taken (ties: the smaller). The degree is chosen separately for each pair's sum, from the
training states only. NOTE: #557's side look had shown the sums' hold-outs H1, H2, H3 of #533 (degree 3 best in H1 and H2 for sigma_1 + sigma_2, degree 4 in H3 and for sigma_3 + sigma_4); the rule is #557's and was not tuned
after that, but its choice is not blind to it.
Equal amplitudes: the sum should carry no oscillation. R = (SS_poly - SS_poly+osc) / SS_poly+osc for the sum fitted by the polynomial alone and with cos phi, sin phi added at the difference's period law; null fraction from
N trials of (the polynomial fit of the sums) + white noise at the sum's residual rms, the share with R at least the observed (a small share flags unequal amplitudes).
--predict: fit the training states (the 63 states D 204.13 to 237.13 of #533 and #535) and write both models' predictions of ln sigma_a and ln sigma_b at the twelve states of #558 (D 203.63 ... 198.13) to
predictions_564.json, without reading any file of I558-win2.
--selftest: (1) a planted antiphase pair (P0 2.62, p1 +0.0165, p2 +0.0003, difference amplitude 0.222, c = 1.4, c1 = 0.063, cubic sum) at the D of the 63 states: M1 recovers p2 to within 0.00015, the difference amplitude to 3%
and c1 to within 0.01, M0's difference rms exceeds 4 times M1's, the sum-oscillation null fraction is at least 1%, and M1's extrapolation to 12 states below D 210 from the 51 above has rms at most 0.014; (2) a planted pair with
amplitudes 0.12 and 0.08 in antiphase (unequal) is flagged (null fraction below 1%)."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I557-win2", "I535-win2", "I533-win2", "I525-win2", "I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import joint_557 as j  # noqa: E402
import period_p2_533 as m  # noqa: E402
D0 = 228.0
LIMIT = 0.014
NEWD = np.array([203.6312 - 0.5 * k for k in range(12)])


def ucol(D, d):
    u = (D - D0) / 10.0
    return np.column_stack([u ** k for k in range(d + 1)])


def poly_fit(D, y, d):
    return np.linalg.lstsq(ucol(D, d), y, rcond=None)[0]


def choose_degree(D, ys):
    n = len(D)
    k = max(6, int(round(0.2 * n)))
    best = None
    for d in (2, 3, 4):
        c = poly_fit(D[: n - k], ys[: n - k], d)
        sse = float(np.sum((ys[n - k:] - ucol(D[n - k:], d) @ c) ** 2))
        if best is None or (sse, d) < best[0]:
            best = ((sse, d), d)
    return best[1]


def diff_cols(D, th, ddeg):
    ph = m.phase(D, th[0], th[1], th[2])
    return None if ph is None else m.columns(D, ddeg, ph)


def fit_diff(D, yd, ddeg):
    """T = polynomial of degree ddeg in u + A cos phi + B sin phi with the period law (P0, p1, p2): the grid of #522 for the start, then Nelder-Mead, as period_p2_533.Fitter"""
    F = m.Fitter(D, ddeg)
    best, f0 = F.fit_free(yd)
    th = best["theta"]
    beta, ss = m.lin(D, yd, ddeg, th)
    return dict(theta=th, ss=ss, ddeg=ddeg, beta=beta, c=float(beta[0]), c1=float(beta[1]) if ddeg >= 1 else 0.0, A=float(beta[ddeg + 1]), B=float(beta[ddeg + 2]), amp=float(math.hypot(beta[ddeg + 1], beta[ddeg + 2])))


def fit_pair(D, ya, yb, ddeg, d=None):
    ys, yd = ya + yb, yb - ya
    if d is None:
        d = choose_degree(D, ys)
    cs = poly_fit(D, ys, d)
    fd = fit_diff(D, yd, ddeg)
    return dict(d=d, S=cs, diff=fd, rms_sum=float(math.sqrt(np.mean((ys - ucol(D, d) @ cs) ** 2))), rms_diff=float(math.sqrt(fd["ss"] / len(D))))


def predict_pair(D, f):
    S = ucol(D, f["d"]) @ f["S"]
    yd = diff_cols(D, f["diff"]["theta"], f["diff"]["ddeg"]) @ f["diff"]["beta"]
    return (S - yd) / 2.0, (S + yd) / 2.0


def flag_null(D, ya, yb, ddeg, trials, seed):
    """null fraction of an oscillation in the sum, at the difference's period law"""
    ys = ya + yb
    f = fit_pair(D, ya, yb, ddeg)
    d, th = f["d"], f["diff"]["theta"]
    Xo = diff_cols(D, th, ddeg)[:, ddeg + 1:]
    Xp = ucol(D, d)

    def R(y):
        c0 = np.linalg.lstsq(Xp, y, rcond=None)[0]
        s0 = float(np.sum((y - Xp @ c0) ** 2))
        X1 = np.hstack([Xp, Xo])
        c1 = np.linalg.lstsq(X1, y, rcond=None)[0]
        s1 = float(np.sum((y - X1 @ c1) ** 2))
        return (s0 - s1) / s1
    Robs = R(ys)
    c0 = np.linalg.lstsq(Xp, ys, rcond=None)[0]
    truth = Xp @ c0
    sig = math.sqrt(np.mean((ys - truth) ** 2))
    rng = np.random.default_rng(seed)
    hit = sum(R(truth + rng.normal(0, sig, len(D))) >= Robs for _ in range(trials))
    return hit / trials, Robs, f


def planted(D, amps, seed, noise=0.006, c1=0.063):
    ph = m.phase(D, 2.62, 0.0165, 0.0003)
    u = (D - D0) / 10.0
    S = -120.0 - 20.0 * u + 3.0 * u ** 2 - 0.5 * u ** 3
    T_a = -(1.4 + c1 * u) / 2 + amps[0] * np.cos(ph + 0.7)
    T_b = (1.4 + c1 * u) / 2 - amps[1] * np.cos(ph + 0.7)
    rng = np.random.default_rng(seed)
    return S / 2 + T_a + rng.normal(0, noise, len(D)), S / 2 + T_b + rng.normal(0, noise, len(D))


def selftest(trials=300):
    Dall, _ = j.all_states()
    ok = True
    D = Dall[Dall >= 204.0]
    ya, yb = planted(D, (0.111, 0.111), 7)
    nf, Robs, f1 = flag_null(D, ya, yb, 1, trials, 3)
    f0 = fit_pair(D, ya, yb, 0)
    th = f1["diff"]["theta"]
    print(f"S1 planted antiphase pair, equal amplitudes 0.111, difference = 1.4 + 0.063 u + oscillation: M1 degree of S {f1['d']}, P0 {th[0]:.3f}, p1 {th[1]:+.4f}, p2 {th[2]:+.5f}, amplitude {f1['diff']['amp']:.4f} (0.222), c {f1['diff']['c']:+.3f}, c1 {f1['diff']['c1']:+.4f} (0.063), rms of the difference M1 {f1['rms_diff']:.4f}, M0 {f0['rms_diff']:.4f}; sum-oscillation null fraction {100 * nf:.1f}% (R {Robs:.3f})")
    good = abs(th[2] - 0.0003) <= 0.00015 and abs(f1["diff"]["amp"] - 0.222) <= 0.0067 and abs(f1["diff"]["c1"] - 0.063) <= 0.01 and f0["rms_diff"] > 4 * f1["rms_diff"] and nf >= 0.01
    tr, te = D >= 210.0, D < 210.0
    f2 = fit_pair(D[tr], ya[tr], yb[tr], 1)
    pa, pb = predict_pair(D[te], f2)
    ra, rb = math.sqrt(np.mean((ya[te] - pa) ** 2)), math.sqrt(np.mean((yb[te] - pb) ** 2))
    print(f"   M1 extrapolation to the 12 states below D 210 from the 51 above (degree {f2['d']}): prediction rms {ra:.4f}, {rb:.4f}")
    good = good and max(ra, rb) <= LIMIT
    print(f"   -> {'pass' if good else 'FAIL'}")
    ok = ok and good
    ya, yb = planted(D, (0.12, 0.08), 8)
    nf, Robs, f = flag_null(D, ya, yb, 1, trials, 4)
    print(f"S2 planted antiphase pair, unequal amplitudes 0.12 and 0.08: sum-oscillation null fraction {100 * nf:.1f}% (R {Robs:.3f})")
    good = nf < 0.01
    print(f"   -> {'pass' if good else 'FAIL'}")
    ok = ok and good
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def main_predict(trials):
    D, Y = j.all_states()
    print(f"{len(D)} training states D {D[0]:.4f} to {D[-1]:.4f}; predictions at the {len(NEWD)} states of #558: D {NEWD[0]:.4f} to {NEWD[-1]:.4f}")
    out = dict(D_new=[float(x) for x in NEWD], models={})
    for ddeg, mname in ((0, "M0"), (1, "M1")):
        out["models"][mname] = {}
        print(f"\n===== {mname}: the difference T has a polynomial of degree {ddeg} in u plus the oscillation")
        for pair in ((1, 2), (3, 4)):
            ya, yb = Y[:, pair[0] - 1], Y[:, pair[1] - 1]
            nf, Robs, f = flag_null(D, ya, yb, ddeg, trials, 21 + pair[0])
            th, fd = f["diff"]["theta"], f["diff"]
            pa, pb = predict_pair(NEWD, f)
            print(f"pair sigma_{pair[0]} + sigma_{pair[1]}: degree of S by the rule {f['d']}, S coefficients in u {', '.join(f'{x:+.4f}' for x in f['S'])}, rms of the sum {f['rms_sum']:.4f}")
            print(f"  difference: P0 {th[0]:.4f}, p1 {th[1]:+.5f}, p2 {th[2]:+.6f}, c {fd['c']:+.4f}, c1 {fd['c1']:+.4f}, A {fd['A']:+.4f}, B {fd['B']:+.4f} (amplitude {fd['amp']:.4f}, each series {fd['amp'] / 2:.4f}), rms of the difference {f['rms_diff']:.4f}")
            print(f"  oscillation in the sum at this period law: null fraction {100 * nf:.1f}% (R {Robs:.3f}); period at D 200.88: {th[0] + th[1] * (200.88 - D0) + th[2] * (200.88 - D0) ** 2:.3f}")
            ya_f, yb_f = predict_pair(D, f)
            print(f"  residual rms of ln sigma_{pair[0]} {math.sqrt(np.mean((ya - ya_f) ** 2)):.4f}, of ln sigma_{pair[1]} {math.sqrt(np.mean((yb - yb_f) ** 2)):.4f} over the 63 states")
            out["models"][mname][f"{pair[0]}{pair[1]}"] = dict(degree=f["d"], S=[float(x) for x in f["S"]], theta=[float(x) for x in th], beta=[float(x) for x in fd["beta"]],
                                                              pred_a=[float(x) for x in pa], pred_b=[float(x) for x in pb], sum_null_fraction=nf)
    json.dump(out, open(os.path.join(HERE, "predictions_564.json"), "w"), indent=1)
    for mname in ("M0", "M1"):
        P = out["models"][mname]
        print(f"\npredictions of ln sigma at the twelve states, {mname} (written to predictions_564.json):")
        print("| D | ln sigma_1 | ln sigma_2 | ln sigma_3 | ln sigma_4 |\n|---|---|---|---|---|")
        for i, d in enumerate(NEWD):
            print(f"| {d:.4f} | {P['12']['pred_a'][i]:.3f} | {P['12']['pred_b'][i]:.3f} | {P['34']['pred_a'][i]:.3f} | {P['34']['pred_b'][i]:.3f} |")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 500
    if "--selftest" in sys.argv:
        sys.exit(selftest(300))
    if "--predict" in sys.argv:
        main_predict(trials)
