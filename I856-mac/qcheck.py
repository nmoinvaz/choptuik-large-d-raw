"""I856-mac check: at D 252.6135, the Delta block's dev settles to a quadratic.

Reads a power.json (`step_spread.py power --json`) and its D 252.6 Delta group. Passes when power's same-start check
passed, both p are in the quadratic band [1.8, 2.2], and q = dev / rel^2 changes by at most --tol (default 0.01,
relative) between the two smallest rels. Its control is #850's I850-mac/power.json, which must FAIL (p 1.6481, and q
moved 5.381e-2 from 1e-66 to 1e-67).

Run: python3 qcheck.py POWER.json [--tol 0.01], or python3 qcheck.py --selftest (a planted quadratic must pass, and
one with a 2% cubic term must fail on q). Exits 1 when a check fails.
"""
import json
import math
import sys


def check(pw, tol):
    g = next(g for g in pw["groups"] if g["D_str"].startswith("252.6") and g["blocks"] == ["Delta"])
    lo, hi = pw["quad"]
    devs = sorted(g["devs"], key=lambda t: -t[0])
    qs = [dev / rel ** 2 for rel, dev in devs]
    print(f"qcheck: D {g['D_str'][:12]}, seed {g['seed']}, tol {tol}")
    for (rel, dev), q in zip(devs, qs):
        print(f"  rel {rel:.0e}: dev {dev:+.6e}, q {q:+.6e}")
    ps = g["p"]
    p_ok = len(ps) == 2 and all(p is not None and lo <= p <= hi for p in ps)
    dq = qs[-1] / qs[-2] - 1
    checks = [("same start", g["same_start"], "power's same-start check"),
              ("p", p_ok, "p " + ", ".join("none" if p is None else f"{p:.4f}" for p in ps) + f" in [{lo}, {hi}]"),
              ("q", abs(dq) <= tol, f"q's change {devs[-2][0]:.0e} -> {devs[-1][0]:.0e}: {dq:+.3e} (|.| <= {tol})")]
    for name, ok, what in checks:
        print(f"  check {name}: {what}: {'pass' if ok else 'FAIL'}")
    return all(c[1] for c in checks)


def planted(cubic):
    # dev = q rel^2 (1 + c rel / 1e-69), so q's change from 1e-68 to 1e-69 is about -9c
    rels = [1e-67, 1e-68, 1e-69]
    devs = [[r, -2.7e89 * r * r * (1 + cubic * r / 1e-69)] for r in rels]
    ps = [math.log(devs[i][1] / devs[i + 1][1]) / math.log(rels[i] / rels[i + 1]) for i in range(2)]
    return dict(quad=[1.8, 2.2], groups=[dict(D_str="252.6134675651788711898", blocks=["Delta"], seed=1, devs=devs,
                                               p=ps, same_start=True)])


argv = sys.argv[1:]
if argv[0] == "--selftest":
    want = [(0.0, True), (0.02 / 9, False)]
    res = []
    for c, w in want:
        print(f"planted cubic {c:.3e} (want {'pass' if w else 'FAIL'})")
        res.append(check(planted(c), 0.01) == w)
    ok = all(res)
    print(f"qcheck selftest: {'PASS' if ok else 'FAIL'}")
else:
    tol = float(argv[argv.index("--tol") + 1]) if "--tol" in argv else 0.01
    print(f"qcheck {argv[0]}")
    ok = check(json.load(open(argv[0])), tol)
    print(f"qcheck: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
