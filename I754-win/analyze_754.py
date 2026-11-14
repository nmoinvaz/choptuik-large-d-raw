#!/usr/bin/env python3
"""#754: does the last segment's plan fix Delta's digits at D 99.875?
    python analyze_754.py [--selftest]      (venv-t151 python, from this folder; reads <name>/base_pin13_D99.8750.npz)
Delta of a state is the exact sum of its eight parts (I739-win/cmp_739.delta, arb at 600 bits). The root is X2c's Delta
(I727-win/X2c, cont3's plan polished in octo-double). A plan's offset is Delta(that plan's own state) - root, for A1
(I710-win/A1) and X2 (I725-win/X2), as #727 and #751 form it (+2.97e-26 and -1.66e-25).
Criteria, fixed before the run:
  (1) L<P>, the last segment at plan P's nodes, reproduces P's offset to 10%: |eff(L<P>) / offset(P) - 1| <= 0.1;
  (2) C<P>, every other interior node at P's, stays below 1e-30: |eff(C<P>)| <= 1e-30;
  (3) the repeat R_LX from A1's arrays reproduces LX's Delta to 1e-40.
The last segment's plan fixes the digits for P when (1) and (2) both hold. Each failure is reported with its numbers.
--selftest: the criteria on planted effects (a 9% miss passes (1) and an 11% miss fails it, the opposite sign fails it,
a complement of 2e-30 fails (2)), and must exit 0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
STATE = "base_pin13_D99.8750.npz"
ROOT = os.path.join(RAW, "I727-win", "X2c", STATE)
OWN = {"A1": os.path.join(RAW, "I710-win", "A1", "anm_pin13_D99.8750.npz"),
       "X2": os.path.join(RAW, "I725-win", "X2", "anm_pin13_D99.8750.npz")}
TAG = {"A1": "A", "X2": "X"}


def crit1(eff, off):
    return off != 0 and abs(eff / off - 1) <= 0.1


def crit2(eff):
    return abs(eff) <= 1e-30


def selftest():
    cases = [("1: a 9% miss", crit1(1.09e-26, 1e-26), True), ("1: an 11% miss", crit1(1.11e-26, 1e-26), False),
             ("1: the opposite sign", crit1(-1e-26, 1e-26), False), ("2: 5e-31", crit2(5e-31), True),
             ("2: 2e-30", crit2(-2e-30), False)]
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
    out, verdict = [], {}
    print("| plan | offset | L: last segment at its nodes | eff / offset | (1) | C: the rest at its nodes | (2) |")
    print("|---|---|---|---|---|---|---|")
    for p, t in TAG.items():
        off = float((c.delta(OWN[p]) - root).mid())
        cells = [p, f"{off:+.4e}"]
        ok = {}
        for part in ("L", "C"):
            path = os.path.join(HERE, part + t, STATE)
            if not os.path.exists(path):
                cells += ["not run"] * (3 if part == "L" else 2)
                continue
            eff = float((c.delta(path) - root).mid())
            if part == "L":
                ok[1] = crit1(eff, off)
                cells += [f"{eff:+.4e}", f"{eff / off:+.4f}", "met" if ok[1] else "NOT MET"]
            else:
                ok[2] = crit2(eff)
                cells += [f"{eff:+.4e}", "met" if ok[2] else "NOT MET"]
        print("| " + " | ".join(cells) + " |")
        if len(ok) == 2:
            verdict[p] = ok[1] and ok[2]
    rp, lp = os.path.join(HERE, "R_LX", STATE), os.path.join(HERE, "LX", STATE)
    if os.path.exists(rp) and os.path.exists(lp):
        d = float((c.delta(rp) - c.delta(lp)).mid())
        print(f"\n(3) Delta(R_LX) - Delta(LX) = {d:+.4e}; bar 1e-40: {'met' if abs(d) <= 1e-40 else 'NOT MET'}")
    for p, v in verdict.items():
        print(f"{p}: the last segment's plan {'fixes' if v else 'does NOT fix'} Delta's digits by criteria (1) and (2)")


if __name__ == "__main__":
    main()
