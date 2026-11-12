#!/usr/bin/env python3
"""#525 part 3 analysis: the periods of ln sigma_1..4 in the twelve new half-unit states D 210.13 to 215.63 (this task, below crawlG's D 216.13), against the chirp's extrapolation.
usage: python below216_525.py [--selftest] [--trials N]       (run from I525-win2 after run_i525.sh; needs the eq_D21*.log of this folder and ../I522-win2/halfunit_522.py, chirp_522.py, trend_525.py)
(A) The acceptance of #525: the period of ln sigma_1 in the 12 new states alone (trend + one sinusoid, period scanned from 1.1 to the D range over 1.5 in steps of 0.005, 1000-trial null test as in #521/#522, the
    quadratic trend of the rule; the line trend is shown too) is within 0.1 of the chirp's extrapolation 2.38 (P0 2.62 + 0.016 x (212.8 - 228) at the centre D 212.8), and its fitted interval excludes 2.525, the period
    that stays at the low half's value of #522. Pass needs both. The same table is shown for sigma_2..4 with their own extrapolations.
(B) The chirp fitted to the 39 states D >= 216.13 (trend of degree 2 or 3) extrapolated down to the 12 new states: rms prediction error against the p1 = 0 control (a: everything extrapolated; b: the oscillation extrapolated,
    the trend refitted to all 51 states).
(C) The chirp refitted to all 51 states D 210.13 to 237.13 (trend of degree 2 and 3): P0, p1, rms residual and the period at D 213.
--selftest: at the D of the new states, noise 0.006, amplitude 0.11, 40 seeds each of a planted period 2.38 and of a planted period 2.525 (quadratic trend like the data): the rule passes in at least 90% of the first and at
most 10% of the second, and for one seed of each the 1000-trial null fraction is below 1%."""
import glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
sys.path.insert(0, HERE)
import analysis_521 as a21  # noqa: E402
import halfunit_522 as h  # noqa: E402
import trend_525 as t  # noqa: E402
from table_505 import parse  # noqa: E402
c = h.a21 if hasattr(h, "a21") else None
D0 = 228.0
EXTRAP = {1: 2.62 + 0.016 * (212.8 - 228), 2: 2.62 + 0.016 * (212.8 - 228), 3: 2.20 + 0.004 * (212.8 - 228), 4: 2.20 + 0.006 * (212.8 - 228)}
STAY = {1: 2.525, 2: 2.525, 3: 2.165, 4: 2.160}


def collect_new():
    pts = {}
    for p in glob.glob(os.path.join(HERE, "eq_D2*.log")):
        if "ctl" in p:
            continue
        r = parse(p)
        s = {x["i"]: x["sigma"] for x in r["sig"]}
        pts.setdefault(round(r["D"], 4), []).append([math.log(s[i]) for i in (1, 2, 3, 4)])
    return pts


def rule(P, Plo, Phi, ext, stay):
    return abs(P - ext) <= 0.1 and Phi < stay


def selftest():
    D = np.arange(210.1312, 215.7, 0.5)
    u = (D - D0) / 10.0
    ok = True
    for ptrue, want in ((2.38, ">= 90%"), (2.525, "<= 10%")):
        passed = 0
        for s in range(40):
            y = 0.3 - 11 * u + 1.5 * u ** 2 + 0.11 * np.sin(2 * np.pi * (D - 213.0) / ptrue + 0.7) + np.random.default_rng(300 + s).normal(0, 0.006, len(D))
            f = a21.fit(D, y, 1.1, True)
            passed += rule(f["P"], f["Plo"], f["Phi"], 2.38, 2.525)
        y = 0.3 - 11 * u + 1.5 * u ** 2 + 0.11 * np.sin(2 * np.pi * (D - 213.0) / ptrue + 0.7) + np.random.default_rng(399).normal(0, 0.006, len(D))
        r = a21.one(f"planted {ptrue}", D, y, 1.1, True, 1000)
        print(f"planted period {ptrue}: the rule passes in {100 * passed / 40:.0f}% of 40 seeds (needed {want}); one seed: {a21.line(r)}")
        good = (passed / 40 >= 0.9 and ptrue == 2.38) or (passed / 40 <= 0.1 and ptrue == 2.525)
        good = good and r["nf"] < 0.01
        ok = ok and good
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def phase(D, P0, p1):
    x = D - D0
    return 2 * np.pi * x / P0 if abs(p1) < 1e-12 else (2 * np.pi / p1) * np.log(1 + p1 * x / P0)


def design(D, P0, p1, deg):
    u = (D - D0) / 10.0
    ph = phase(D, P0, p1)
    return np.column_stack([u ** k for k in range(deg + 1)] + [np.cos(ph), np.sin(ph)])


def extrapolate(Dtr, ytr, Dte, yte, Dall, yall, deg):
    X, XtX, valid = t.grid_columns_deg(Dtr, deg)
    out = {}
    for tag, p1z in (("chirp", False), ("p1=0", True)):
        v = valid.copy()
        if p1z:
            v[:, :] = False
            v[:, np.argmin(np.abs(t.c.P1S))] = valid[:, np.argmin(np.abs(t.c.P1S))]
        ss, P0, p1, b = t.r.grid_fit(X, XtX, v, ytr)
        e = yte - design(Dte, P0, p1, deg) @ b
        osc = lambda DD: b[deg + 1] * np.cos(phase(DD, P0, p1)) + b[deg + 2] * np.sin(phase(DD, P0, p1))
        uu = (Dall - D0) / 10.0
        co = np.polyfit(uu, yall - osc(Dall), deg)
        e2 = (yall - osc(Dall) - np.polyval(co, uu))[np.isin(Dall, Dte)]
        out[tag] = (P0, p1, math.sqrt(np.mean(e ** 2)), math.sqrt(np.mean(e2 ** 2)))
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 1000
    new = collect_new()
    new = {d: v for d, v in new.items() if d < 216.0}
    old = h.collect()
    Dn = np.array(sorted(new))
    Yn = np.array([np.mean(new[d], axis=0) for d in Dn])
    print(f"{len(Dn)} new states D {Dn[0]:.4f} to {Dn[-1]:.4f}")
    print("\n(A) periods in the new states alone (scan from 1.1, 1000-trial null test)")
    print("| series | trend | period (interval) | amplitude | rms | null fraction | chirp extrapolation | stays at low half | rule |\n|---|---|---|---|---|---|---|---|---|")
    pass1 = False
    for i in (1, 2, 3, 4):
        for quad in (True, False):
            r = a21.one(f"ln sigma_{i}", Dn, Yn[:, i - 1], 1.1, quad, trials)
            ok = rule(r["P"], r["Plo"], r["Phi"], EXTRAP[i], STAY[i])
            if i == 1 and quad:
                pass1 = ok and r["nf"] < 0.01
            print(f"| sigma_{i} | {'quadratic' if quad else 'line'} | {r['P']:.3f} ({r['Plo']:.3f} to {r['Phi']:.3f}) | {r['amp']:.3f} +- {r['err']:.3f} | {r['rms']:.4f} | {100 * r['nf']:.1f}% | {EXTRAP[i]:.3f} | {STAY[i]:.3f} | {'meets' if ok else 'does not meet'} |")
    print(f"\nacceptance of #525 part 3 (ln sigma_1, quadratic trend, within 0.1 of {EXTRAP[1]:.3f}, interval below 2.525, null fraction below 1%): {'pass' if pass1 else 'FAIL'}")
    Do = np.array(sorted(d for d in old if d <= 237.2))
    Yo = np.array([np.mean(old[d], axis=0) for d in Do])
    Da = np.concatenate([Dn, Do])
    Ya = np.concatenate([Yn, Yo])
    print("\n(B) the chirp fitted to the 39 states D >= 216.13, extrapolated down to the new states")
    print("| series | trend | chirp P0, p1 | chirp prediction rms (a) | chirp (b) | p1 = 0: P | p1 = 0 prediction rms (a) | p1 = 0 (b) |\n|---|---|---|---|---|---|---|---|")
    for i in (1, 2, 3, 4):
        for deg in (2, 3):
            o = extrapolate(Do, Yo[:, i - 1], Dn, Yn[:, i - 1], Da, Ya[:, i - 1], deg)
            ch, z = o["chirp"], o["p1=0"]
            print(f"| sigma_{i} | degree {deg} | {ch[0]:.2f}, {ch[1]:+.3f} | {ch[2]:.4f} | {ch[3]:.4f} | {z[0]:.2f} | {z[2]:.4f} | {z[3]:.4f} |")
    print("\n(C) the chirp refitted to all 51 states D 210.13 to 237.13")
    print("| series | trend | P0 (D 228) | p1 | period at D 213 | rms residual |\n|---|---|---|---|---|---|")
    M = t.TrendModels(Da)
    for i in (1, 2, 3, 4):
        for deg in (2, 3):
            f = M.fit(deg, Ya[:, i - 1])
            print(f"| sigma_{i} | degree {deg} | {f['P0']:.2f} | {f['p1']:+.3f} | {f['P0'] + f['p1'] * (213 - 228):.3f} | {math.sqrt(f['ss'] / len(Da)):.4f} |")
