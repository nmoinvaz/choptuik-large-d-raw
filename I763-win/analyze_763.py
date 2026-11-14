#!/usr/bin/env python3
"""#763: the joint and single effects of the last segment's two plan nodes on Delta at D 99.875.
    python analyze_763.py [--selftest]      (venv-t151 python, from this folder; reads <name>/base_pin13_D99.8750.npz)
Delta of a state is the exact sum of its eight parts (I739-win/cmp_739.delta, arb at 600 bits), and an effect is
Delta - root, the root being X2c's Delta (I727-win/X2c, cont3's plan polished in octo-double).
  N1_<s>, N2_<s>   segs[3][1] or segs[3][2] moved by s times A1's shift; P_<s> both
  cross(s) = eff(P_s) - eff(N1_s) - eff(N2_s), quoted with its ratio to eff(P_s)
  linearity of each: eff(.._05) / eff(.._10), against 0.5
Criteria, fixed before the run:
  (control) eff(P_10) equals #754's LA effect (I754-win/LA) to 1e-40, the same plan polished again;
  (cross) quoted at both scales, with no pass or fail, since #751 leaves open whether it is large;
  (linear) a node's effect counts as linear in its shift when |eff_05 / eff_10 - 0.5| <= 0.05.
--selftest: the criteria on planted effects (a control off by 2e-40 fails, a ratio of 0.52 is linear and 0.56 is not, a
planted cross term is recovered), and must exit 0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
STATE = "base_pin13_D99.8750.npz"
ROOT = os.path.join(RAW, "I727-win", "X2c", STATE)
LA = os.path.join(RAW, "I754-win", "LA", STATE)
NAMES = ("N1_05", "N1_10", "N2_05", "N2_10", "P_05", "P_10")


def control_ok(p10, la):
    return abs(p10 - la) <= 1e-40


def linear(e05, e10):
    return e10 != 0 and abs(e05 / e10 - 0.5) <= 0.05


def cross(p, n1, n2):
    return p - n1 - n2


def selftest():
    cases = [("control off by 2e-40", control_ok(1e-26 + 2e-40, 1e-26), False),
             ("control equal", control_ok(1e-26, 1e-26), True),
             ("ratio 0.52 linear", linear(0.52e-26, 1e-26), True),
             ("ratio 0.56 not linear", linear(0.56e-26, 1e-26), False),
             ("planted cross term 3e-27", abs(cross(3.0e-26, 1.5e-26, 1.2e-26) - 3e-27) < 1e-40, True)]
    bad = 0
    for label, got, want in cases:
        print(f"  {label}: {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    print("selftest", "FAILED" if bad else "passed")
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.path.insert(0, os.path.join(RAW, "I739-win"))
    import cmp_739 as c
    c.flint.ctx.prec = 600
    root = c.delta(ROOT)
    eff = {}
    for n in NAMES:
        p = os.path.join(HERE, n, STATE)
        if os.path.exists(p):
            eff[n] = float((c.delta(p) - root).mid())
    print("| state | effect on Delta |\n|---|---|")
    for n in NAMES:
        print(f"| {n} | {eff[n]:+.4e} |" if n in eff else f"| {n} | not run |")
    if "P_10" in eff and os.path.exists(LA):
        d = float((c.delta(os.path.join(HERE, "P_10", STATE)) - c.delta(LA)).mid())
        print(f"\n(control) Delta(P_10) - Delta(#754's LA) = {d:+.4e}; bar 1e-40: {'met' if abs(d) <= 1e-40 else 'NOT MET'}")
    print("\n| scale | pair | N1 + N2 | cross term | cross / pair |\n|---|---|---|---|---|")
    for s in ("05", "10"):
        if all(f"{k}_{s}" in eff for k in ("P", "N1", "N2")):
            p, n1, n2 = eff[f"P_{s}"], eff[f"N1_{s}"], eff[f"N2_{s}"]
            x = cross(p, n1, n2)
            print(f"| {int(s) / 10:.1f} | {p:+.4e} | {n1 + n2:+.4e} | {x:+.4e} | {x / p:+.4f} |")
    print("\n| node | eff 0.5 / eff 1.0 | linear (0.5 +- 0.05) |\n|---|---|---|")
    for k in ("N1", "N2", "P"):
        if f"{k}_05" in eff and f"{k}_10" in eff:
            r = eff[f"{k}_05"] / eff[f"{k}_10"]
            print(f"| {k} | {r:+.4f} | {'yes' if linear(eff[k + '_05'], eff[k + '_10']) else 'NO'} |")


if __name__ == "__main__":
    main()
