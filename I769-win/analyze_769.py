#!/usr/bin/env python3
"""#769: each last-segment node's effect on Delta at D 99.875 against its shift, s = 0.25 to 2.0 of A1's.
    python analyze_769.py [--selftest]      (venv-t151 python, from this folder)
An effect is Delta - root (I739-win/cmp_739.delta, arb at 600 bits; the root X2c's, I727-win). The points s = 0.5 and 1.0
are #763's (I763-win/N<k>_05, N<k>_10), the others this folder's.
Criteria, fixed before the run:
  (control) C_N2_05 reproduces #763's N2_05 Delta to 1e-40;
  (shape) for each node, over s = 0.25, 0.5, 0.75, 1.0, 1.5, 2.0: monotone or not, the sign changes, and where every
  effect has one sign, the least-squares power p of |effect| against s with the largest residual of ln|effect|. The
  shape is quoted, with no pass or fail, since the task asks what it is.
--selftest: the shape code on planted series (a power 2 is recovered to 1e-12 with residual below 1e-12, a series with a
maximum is called not monotone, a sign change is counted, and a control off by 2e-40 fails); it must exit 0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
STATE = "base_pin13_D99.8750.npz"
ROOT = os.path.join(RAW, "I727-win", "X2c", STATE)
SCALES = [(0.25, "025"), (0.5, "05"), (0.75, "075"), (1.0, "10"), (1.5, "15"), (2.0, "20")]


def path(node, tag):
    folder = os.path.join(RAW, "I763-win") if tag in ("05", "10") else HERE
    return os.path.join(folder, f"{node}_{tag}", STATE)


def control_ok(d):
    """the control's criterion: C_N2_05's Delta within 1e-40 of #763's N2_05"""
    return abs(d) <= 1e-40


def shape(ss, es):
    """(monotone, sign changes, power p or None, largest residual of ln|e| or None)"""
    d = [b - a for a, b in zip(es[:-1], es[1:])]
    mono = all(x > 0 for x in d) or all(x < 0 for x in d)
    flips = sum(1 for a, b in zip(es[:-1], es[1:]) if (a > 0) != (b > 0))
    if flips or any(e == 0 for e in es):
        return mono, flips, None, None
    xs, ys = [math.log(s) for s in ss], [math.log(abs(e)) for e in es]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    p = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    c = my - p * mx
    return mono, flips, p, max(abs(y - (c + p * x)) for x, y in zip(xs, ys))


def selftest():
    ss = [s for s, _ in SCALES]
    bad = 0
    mono, flips, p, r = shape(ss, [3e-27 * s ** 2 for s in ss])
    for label, ok in (("power 2 recovered", p is not None and abs(p - 2) < 1e-12 and r < 1e-12),
                      ("power 2 monotone", mono), ("power 2 no sign change", flips == 0)):
        print(f"  {label}: {'ok' if ok else 'WRONG'}")
        bad += not ok
    mono, flips, p, r = shape(ss, [1e-26 * s * math.exp(-2 * s) for s in ss])
    print(f"  a maximum: monotone {mono} (expected False) {'ok' if not mono else 'WRONG'}")
    bad += mono
    mono, flips, p, r = shape(ss, [1e-26 * (s - 0.6) for s in ss])
    print(f"  a sign change: {flips} (expected 1) {'ok' if flips == 1 else 'WRONG'}")
    bad += flips != 1
    for d, want in ((2e-40, False), (-2e-40, False), (5e-41, True), (0.0, True)):
        ok = control_ok(d) == want
        print(f"  the control at {d:+.0e}: {'met' if control_ok(d) else 'not met'} (expected {'met' if want else 'not met'}) {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.path.insert(0, os.path.join(RAW, "I739-win"))
    import cmp_739 as c
    c.flint.ctx.prec = 600
    root = c.delta(ROOT)
    cp, rp = os.path.join(HERE, "C_N2_05", STATE), path("N2", "05")
    if os.path.exists(cp) and os.path.exists(rp):
        d = float((c.delta(cp) - c.delta(rp)).mid())
        print(f"(control) Delta(C_N2_05) - Delta(#763's N2_05) = {d:+.4e}; bar 1e-40: {'met' if control_ok(d) else 'NOT MET'}\n")
    print("| s | " + " | ".join(f"{s}" for s, _ in SCALES) + " |\n|---|" + "---|" * len(SCALES))
    for node in ("N1", "N2"):
        es, ss = [], []
        cells = []
        for s, tag in SCALES:
            p = path(node, tag)
            if os.path.exists(p):
                e = float((c.delta(p) - root).mid())
                es.append(e)
                ss.append(s)
                cells.append(f"{e:+.4e}")
            else:
                cells.append("not run")
        print(f"| {node} | " + " | ".join(cells) + " |")
        if len(es) == len(SCALES):
            mono, flips, pw, res = shape(ss, es)
            print(f"   {node}: monotone {mono}, sign changes {flips}"
                  + (f", power {pw:+.3f} with largest ln residual {res:.3f}" if pw is not None else ", no power (a sign change)"))


if __name__ == "__main__":
    main()
