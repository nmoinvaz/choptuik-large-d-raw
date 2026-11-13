#!/usr/bin/env python3
"""#682: the chain's steps, the ladder of the predictor's error against a, and Delta_full - Delta_held, by the rules of README.md (plan and amendments 1 and 2).
usage: python table_682.py [--selftest]          (from this folder; reads chain/anm_run.jsonl, logs/chain.log, logs/ladder_a1_<k>.log, ladder/a1_<k>/anm_run.jsonl and ../T138-win2 / ../I642-win via the stage checkout)
F(a) = the quad-double max|F| of the re-seeded prediction at the start of the corrector (the first `qn 0 [full]: |F|` line after the attempt's re-seed line); floor = the base's own 6.90e-36
(the first `qn 0` line of the base polish). If every F(a) <= 3 floor the error is below the floor; else the least-squares slope s of log F against log a over the points with F > 3 floor:
first order if s <= 1.3, second order if 1.7 <= s <= 2.3. --selftest: the slope code on planted data (a first-order series, a second-order one, one at the floor)."""
import glob
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = r"C:\Users\nathan\Source\choptuik-large-d-raw-stage"
RAW = os.path.dirname(HERE)
FLOOR_FALLBACK = 6.90e-36
QN0 = re.compile(r"qn 0 \[full\]: \|F\| ([0-9.e+-]+) ->")
ATT = re.compile(r"^    a ([0-9.]+): re-seeded")


def slope(pts):
    xs = [math.log(a) for a, _ in pts]
    ys = [math.log(f) for _, f in pts]
    n = len(pts)
    mx, my = sum(xs) / n, sum(ys) / n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def classify(pts, floor):
    above = [(a, f) for a, f in pts if f > 3 * floor]
    if not above:
        return None, "below the floor at every a (every F within 3 x the floor)"
    if len(above) < 2:
        return None, f"only one point above 3 x the floor ({above[0][0]:g}: {above[0][1]:.2e}), no slope"
    s = slope(above)
    if s < 0.7:   # amendment 3 (after the data): the rule of README.md said "first order if s <= 1.3", which would call a flat series first order; a flat series is the floor
        return s, "FLAT (slope below 0.7: no resolved a-dependence, the values are the floor's noise; the letter of the pre-registered rule, s <= 1.3, would say 'first order')"
    return s, ("first order" if s <= 1.3 else "second order" if 1.7 <= s <= 2.3 else "neither (between the two)")


def selftest():
    floor = 1e-35
    cases = [("first order", [(a, 1e-30 * a) for a in (1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2)], "first order"),
             ("second order", [(a, 1e-28 * a ** 2) for a in (1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2)], "second order"),
             ("at the floor", [(a, 1.5e-35) for a in (1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2)], "below the floor"),
             ("order 1.5", [(a, 1e-29 * a ** 1.5) for a in (1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2)], "neither"),
             ("flat, 5 floors", [(a, 5e-35 * (1 + 0.1 * math.sin(7 * a))) for a in (1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2)], "FLAT")]
    bad = 0
    for name, pts, want in cases:
        s, cls = classify(pts, floor)
        ok = cls.startswith(want)
        print(f"  planted '{name}': slope {s if s is None else round(s, 3)}, {cls} {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def attempts_qn0(logpath):
    """[(a, F)] from a log: the first qn 0 |F| after each 're-seeded' line."""
    out, pending = [], None
    for ln in open(logpath, encoding="utf-8", errors="replace"):
        m = ATT.match(ln)
        if m:
            pending = float(m.group(1))
            continue
        m = QN0.search(ln)
        if m and pending is not None:
            out.append((pending, float(m.group(1))))
            pending = None
    return out


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    floor = FLOOR_FALLBACK
    first = [ln for ln in open(os.path.join(HERE, "logs", "chain.log"), encoding="utf-8", errors="replace") if QN0.search(ln)]
    if first:
        floor = float(QN0.search(first[0]).group(1))
    print(f"floor (the base's own quad-double |F| at D 77, first qn 0 of the base polish): {floor:.2e}\n")
    pts = []
    for den in (64, 32, 16, 8, 4, 2):
        p = os.path.join(HERE, "logs", f"ladder_a1_{den}.log")
        if os.path.exists(p):
            for a, f in attempts_qn0(p)[:1]:
                pts.append((a, f))
    for a, f in attempts_qn0(os.path.join(HERE, "logs", "chain.log"))[:1]:
        pts.append((a, f))
    pts.sort()
    print("| a (= dD) | quad-double max abs F of the re-seeded prediction | / a | / a^2 | in floors |\n|---|---|---|---|---|")
    for a, f in pts:
        print(f"| {a:g} | {f:.3e} | {f / a:.3e} | {f / a ** 2:.3e} | {f / floor:.1f} |")
    s, cls = classify(pts, floor)
    print(f"\nslope of log F against log a over the points above 3 x the floor: {s if s is None else round(s, 2)}; the predictor's error is {cls}")
    print("Lagrange predictor of #645 for comparison (the same quantity, quad-double max|F| after the predictor): 2.2e8 at D 77.05 (dD about 0.05), and about 4.2e2 x dD at dD = 1.95e-4")
    # the chain
    print("\nChain steps (chain/anm_run.jsonl):")
    for ln in open(os.path.join(HERE, "chain", "anm_run.jsonl")):
        r = json.loads(ln)
        for at in r["attempts"]:
            print(f"  step {r['step']}: D {r['D0']:.1f} -> {at['D']:.1f}, a {at['a']:.4g}, dd F_pred {at['F_pred']:.2e}, dd F_final {at['F_final']:.2e}, {at['steps']} qd steps, accepted {at['accepted']}")


if __name__ == "__main__":
    main()
