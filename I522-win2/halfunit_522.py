#!/usr/bin/env python3
"""#522 part 2: the periods of ln sigma_1..4 in D 216 to 227 at half-unit spacing, without the alias assumption of #521.
usage: python halfunit_522.py [--selftest] [--trials N]     (run from I522-win2; needs ../I521-win2/analysis_521.py, ../I516-win2/fit_516.py and the logs of the earlier tasks and this folder)
Data: the 12 unit states D 216.13 to 227.13 and the 11 new states D 216.63 to 226.63 (23 states at 0.5 spacing), fitted over D 216 to 227.2 with (a) line + sinusoid and (c) quadratic + sinusoid, the period scanned from 1.1 (below the
unit-spacing Nyquist period of 2, which is the point) to the D range over 1.5 in steps of 0.005, 1000-trial null test as in #521. Also the D 216 to 237 chirp fit of chirp_522.py with all states.
Rule of #522: a period within 0.1 of #521's unit-spacing value (2.530, 2.525, 2.165, 2.155 with the quadratic trend) confirms that reading, and one near its alias 1/(1 - 1/P) (1.654, 1.656, 1.858, 1.866) refutes it.
--selftest: at half-unit spacing a planted period 2.53 is recovered as 2.53 and a planted period 1.654 (the alias at unit spacing) as 1.654, not as 2.53."""
import glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I521-win2"))
sys.path.insert(0, os.path.join(HERE, "..", "I516-win2"))
sys.path.insert(0, os.path.join(HERE, "..", "I505-win2"))
import analysis_521 as a21  # noqa: E402
from table_505 import parse  # noqa: E402
RAW = os.path.join(HERE, "..")
UNIT = {1: 2.530, 2: 2.525, 3: 2.165, 4: 2.155}


def collect():
    pts = a21.collect()
    for p in glob.glob(os.path.join(HERE, "eq_D2*.log")):
        if "ctl" in p:
            continue
        r = parse(p)
        s = {x["i"]: x["sigma"] for x in r["sig"]}
        pts.setdefault(round(r["D"], 4), []).append([math.log(s[i]) for i in (1, 2, 3, 4)])
    return pts


def alias(P):
    return 1.0 / (1.0 - 1.0 / P)


def selftest():
    D = np.arange(216.1312, 227.2, 0.5)
    rng = np.random.default_rng(8)
    ok = True
    for ptrue in (2.53, alias(2.53)):
        y = -1.05 * (D - 222.0) + 0.2 * (D - 222.0) ** 2 / 10 + 0.12 * np.sin(2 * np.pi * (D - 220.0) / ptrue) + rng.normal(0, 0.005, len(D))
        r = a21.one(f"planted {ptrue:.3f}", D, y, 1.1, True, trials=200)
        print(a21.line(r))
        ok = ok and abs(r["P"] - ptrue) < 0.05 and r["nf"] < 0.01
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    trials = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 1000
    pts = collect()
    Ds = sorted(pts)
    D = np.array(Ds)
    Y = np.array([np.mean(pts[d], axis=0) for d in Ds])
    low = D <= 227.2
    print(f"{int(low.sum())} distinct D in 216 to 227.2 ({D[low][0]:.4f} to {D[low][-1]:.4f}); spacings {sorted(set(np.round(np.diff(D[low]), 3)))}")
    res = {}
    for i in (1, 2, 3, 4):
        for quad, ftag in ((False, "(a) line + sinusoid"), (True, "(c) quadratic + sinusoid")):
            r = a21.one(f"ln sigma_{i} {ftag}", D[low], Y[low, i - 1], 1.1, quad, trials)
            res[(i, quad)] = r
            print("  " + a21.line(r))
    print("\nrule of #522: within 0.1 of the unit-spacing value confirms, near its alias refutes (quadratic trend, the fit of #521's table)")
    print("| series | unit-spacing value (#521) | its alias | half-unit period (quadratic) | difference | null fraction | verdict | half-unit period (line) | null fraction |")
    print("|---|---|---|---|---|---|---|---|---|")
    for i in (1, 2, 3, 4):
        r, rl = res[(i, True)], res[(i, False)]
        u, al = UNIT[i], alias(UNIT[i])
        diff = r["P"] - u
        if abs(diff) <= 0.1 and r["nf"] < 0.01:
            v = "confirms"
        elif abs(r["P"] - al) <= 0.1:
            v = "near the alias: refutes"
        else:
            v = "neither (between)"
        print(f"| sigma_{i} | {u:.3f} | {al:.3f} | {r['P']:.3f} ({r['Plo']:.3f} to {r['Phi']:.3f}) | {diff:+.3f} | {100 * r['nf']:.1f}% | {v} | {rl['P']:.3f} | {100 * rl['nf']:.1f}% |")
