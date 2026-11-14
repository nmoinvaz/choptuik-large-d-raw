#!/usr/bin/env python3
"""#741 control: is the polished Delta of a shifted plan reproducible from a different start state?
usage: python repro_741.py [--selftest]       (venv-t151 python, from this folder)
Compares Delta(R1) with Delta(S1) (S1's plan, shift 1e-4, from A1's arrays against cont3's) and Delta(R3) with Delta(S3) (shift 1e-3, from X2's arrays), Delta the exact sum of the eight parts (arb, 600 bits).
Reading, fixed in the README before the runs: a difference of at most 1e-40 means the Delta of a shifted plan is reproducible far below 1e-27, so the Delta shifts of S1 to S5 are a real function of the plan;
a difference of 1e-30 or more means they are not determined to that level; in between is reported as it is.
--selftest: a planted pair 1e-45 apart reads reproducible, 1e-27 apart reads NOT determined, 1e-35 apart reads in between."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I739-win"))
import cmp_739 as c          # noqa: E402

c.flint.ctx.prec = 600
BASE = lambda name: os.path.join(HERE, name, "base_pin13_D99.8750.npz")


def reading(diff):
    d = abs(diff)
    if d <= 1e-40:
        return "reproducible (at most 1e-40)"
    if d >= 1e-30:
        return "NOT determined to that level (1e-30 or more)"
    return "in between 1e-40 and 1e-30, reported as it is"


def selftest():
    bad = 0
    for d, want in ((1e-45, "reproducible"), (1e-27, "NOT determined"), (1e-35, "in between")):
        got = reading(d)
        ok = got.startswith(want)
        print(f"  planted difference {d:g}: '{got}' {'ok' if ok else 'WRONG'}")
        bad += not ok
    a = c.arb("1.745150028164499252944352893640343550633")
    shown = float(((a + c.arb("1e-27")) - a).mid())
    ok = abs(shown - 1e-27) < 1e-39
    print(f"  planted displaced pair 1e-27: difference {shown:.4e} {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for r, s, label in (("R1", "S1", "shift 1e-4, from A1's arrays"), ("R3", "S3", "shift 1e-3, from X2's arrays")):
        if not (os.path.exists(BASE(r)) and os.path.exists(BASE(s))):
            print(f"{r} against {s}: {r} not finished")
            continue
        dr, ds = c.delta(BASE(r)), c.delta(BASE(s))
        diff = float((dr - ds).mid())
        print(f"{r} ({label}) Delta {dr.str(40, radius=False)}\n{s} Delta {ds.str(40, radius=False)}\n  {r} - {s} = {diff:+.6e}: {reading(diff)}")


if __name__ == "__main__":
    main()
