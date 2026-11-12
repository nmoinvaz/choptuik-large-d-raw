#!/usr/bin/env python3
"""#535: the periods of ln sigma_1..4 in the twelve new half-unit states D 204.13 to 209.63 against #533's prediction (comment 6813036441 on #533, written before this run).
usage: python period_535.py [--selftest] [--trials N]       (run from I535-win2 after run_i535.sh; needs the eq_D20*.log of this folder, ../I525-win2/ and ../I533-win2/period_p2_533.py)
(A) The acceptance of #535: the period of ln sigma_1 in the 12 new states alone (trend + one sinusoid, period scanned from 1.1 to the D range over 1.5 in steps of 0.005, 1000-trial null test as in #521, #522, #525; the
    quadratic trend of the rule, the line trend shown too) must be within 0.1 of 2.404 (the p2 chirp's value at the centre D 206.8 of the 51-state fit with a cubic trend, bootstrap sd 0.021). The distances to the other two
    models of #533's comment, the linear drift (2.334) and the constant period (2.560), are printed beside it, since a window of 0.1 does not separate 2.334 from 2.404.
    The same for sigma_2..4 against 2.408, 2.103, 2.139 (their linear-drift values 2.324, 2.092, 2.097 and constant-period values 2.560, 2.180, 2.180).
(B) The model of #533 (p2 chirp, cubic trend, fitted to the 51 states D >= 210.13) predicting the 12 new states: rms prediction error, with the p2 = 0 chirp and the constant period beside it.
(C) The p2 chirp refitted to all 63 states: P0, p1, p2, the null fraction of p2, the residual, the period at D 206.8.
--selftest: at the D of the new states, noise 0.006, amplitude 0.11, 40 seeds each of a planted period 2.404 and 2.56 (quadratic trend like the data): the within-0.1 rule passes in at least 90% of the first and at most 10% of
the second, and a planted 2.334 passes it (it cannot be told from 2.404 by the rule, which the report states)."""
import glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I533-win2", "I525-win2", "I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import analysis_521 as a21  # noqa: E402
import period_p2_533 as m  # noqa: E402
from table_505 import parse  # noqa: E402
PRED = {1: 2.404, 2: 2.408, 3: 2.103, 4: 2.139}
LIN = {1: 2.334, 2: 2.324, 3: 2.092, 4: 2.097}
CONST = {1: 2.560, 2: 2.560, 3: 2.180, 4: 2.180}
D0 = 228.0


def collect_new():
    pts = {}
    for p in glob.glob(os.path.join(HERE, "eq_D2*.log")):
        if "ctl" in p:
            continue
        r = parse(p)
        s = {x["i"]: x["sigma"] for x in r["sig"]}
        pts.setdefault(round(r["D"], 4), []).append([math.log(s[i]) for i in (1, 2, 3, 4)])
    return {d: v for d, v in pts.items() if d < 210.0}


def selftest():
    D = np.arange(204.1312, 209.7, 0.5)
    u = (D - D0) / 10.0
    ok = True
    for ptrue, want in ((2.404, "pass >= 90%"), (2.56, "pass <= 10%"), (2.334, "pass (not separable)")):
        passed = 0
        for s in range(40):
            y = 0.3 - 11 * u + 1.5 * u ** 2 + 0.11 * np.sin(2 * np.pi * (D - 207.0) / ptrue + 0.7) + np.random.default_rng(500 + s).normal(0, 0.006, len(D))
            f = a21.fit(D, y, 1.1, True)
            passed += abs(f["P"] - 2.404) <= 0.1
        frac = passed / 40
        print(f"planted period {ptrue}: the within-0.1-of-2.404 rule passes in {100 * frac:.0f}% of 40 seeds ({want})")
        good = (ptrue == 2.404 and frac >= 0.9) or (ptrue == 2.56 and frac <= 0.1) or (ptrue == 2.334 and frac >= 0.9)
        ok = ok and good
    y = 0.3 - 11 * u + 1.5 * u ** 2 + 0.11 * np.sin(2 * np.pi * (D - 207.0) / 2.404 + 0.7) + np.random.default_rng(599).normal(0, 0.006, len(D))
    r = a21.one("planted 2.404", D, y, 1.1, True, 1000)
    print(a21.line(r))
    ok = ok and r["nf"] < 0.01
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 1000
    new = collect_new()
    Dn = np.array(sorted(new))
    Yn = np.array([np.mean(new[d], axis=0) for d in Dn])
    print(f"{len(Dn)} new states D {Dn[0]:.4f} to {Dn[-1]:.4f}")
    print("\n(A) periods in the new states alone (scan from 1.1, 1000-trial null test)")
    print("| series | trend | period (interval) | amplitude | rms | null fraction | prediction (#533) | difference | within 0.1 | distance to linear drift / constant |\n|---|---|---|---|---|---|---|---|---|---|")
    accept = False
    for i in (1, 2, 3, 4):
        for quad in (True, False):
            r = a21.one(f"ln sigma_{i}", Dn, Yn[:, i - 1], 1.1, quad, trials)
            diff = r["P"] - PRED[i]
            within = abs(diff) <= 0.1
            if i == 1 and quad:
                accept = within and r["nf"] < 0.01
            print(f"| sigma_{i} | {'quadratic' if quad else 'line'} | {r['P']:.3f} ({r['Plo']:.3f} to {r['Phi']:.3f}) | {r['amp']:.3f} +- {r['err']:.3f} | {r['rms']:.4f} | {100 * r['nf']:.1f}% | {PRED[i]:.3f} | {diff:+.3f} | {'yes' if within else 'no'} | {abs(r['P'] - LIN[i]):.3f} / {abs(r['P'] - CONST[i]):.3f} |")
    print(f"\nacceptance of #535 (ln sigma_1, quadratic trend, within 0.1 of 2.404, null fraction below 1%): {'pass' if accept else 'FAIL'}")
    Do, Yo = m.collect51()
    Da = np.concatenate([Dn, Do])
    Ya = np.concatenate([Yn, Yo])
    print("\n(B) #533's model (cubic trend, fitted to the 51 states D >= 210.13) predicting the new states")
    print("| series | p2 chirp rms (max) | p2 = 0 chirp rms (max) | p1 = p2 = 0 rms (max) | P0, p1, p2 of the p2 chirp |\n|---|---|---|---|---|")
    F = m.Fitter(Do, 3)
    for i in (1, 2, 3, 4):
        best, f0 = F.fit_free(Yo[:, i - 1])
        cst = F.const(Yo[:, i - 1])
        cells = []
        for th in (best["theta"], f0["theta"], cst["theta"]):
            e = Yn[:, i - 1] - m.predict(Dn, Do, Yo[:, i - 1], 3, th)
            cells.append(f"{math.sqrt(np.mean(e ** 2)):.4f} ({np.max(np.abs(e)):.4f})")
        th = best["theta"]
        print(f"| sigma_{i} | {cells[0]} | {cells[1]} | {cells[2]} | {th[0]:.3f}, {th[1]:+.4f}, {th[2]:+.5f} |")
    print("\n(C) the p2 chirp refitted to all 63 states D 204.13 to 237.13 (cubic trend)")
    print("| series | p2 = 0: P0, p1 | rms | free: P0, p1, p2 | rms | period at D 206.8 / 228 / 237 | null fraction (i) / (ii) |\n|---|---|---|---|---|---|---|")
    F = m.Fitter(Da, 3)
    for i in (1, 2, 3, 4):
        y = Ya[:, i - 1]
        best, f0 = F.fit_free(y)
        th, t0 = best["theta"], f0["theta"]
        Pof = lambda x: th[0] + th[1] * (x - D0) + th[2] * (x - D0) ** 2
        if i in (1, 2):
            nf1, _ = m.nullfrac(F, y, min(trials, 500), "ext", 41 + i)
            nf2, _ = m.nullfrac(F, y, min(trials, 500), "m0", 51 + i)
            nfs = f"{100 * nf1:.1f}% / {100 * nf2:.1f}%"
        else:
            nfs = "not run"
        n = len(Da)
        print(f"| sigma_{i} | {t0[0]:.3f}, {t0[1]:+.4f} | {math.sqrt(f0['ss'] / n):.4f} | {th[0]:.3f}, {th[1]:+.4f}, {th[2]:+.5f} | {math.sqrt(best['ss'] / n):.4f} | {Pof(206.8):.3f} / {Pof(228):.3f} / {Pof(237):.3f} | {nfs} |", flush=True)
