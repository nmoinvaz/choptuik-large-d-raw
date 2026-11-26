#!/usr/bin/env python3
"""i1101_eval.py DIR [--control] | --selftest [--mutate]   (#1101 I1101-win2; the bars of the README, written before the runs)

DIR holds R0/l1kc127k070w2.jsonl, R1/l1kc127k050w2.jsonl, R2/l1kc127k035w2.jsonl (the last record of each is read). Prints the table (steps, |F|, constraint, Delta,
seconds), the bars and, when all three exist, r and E:
  bar 1 (R0, the control): |F| <= 5e-10, steps == 4179, |Delta - 1.174322923415951| <= 1e-9
  bar 2 (R1, R2): |F| <= 5e-10, steps 5851 +- 2% (R1: 5734..5968) and 8358 +- 2% (R2: 8191..8525)
  bar 3: r = (D07 - D05)/(D05 - D035), formed only if |D05 - D035| >= 1e-10 (an RK4 error ~ kappa^4 predicts 3.74)
  bar 4: E = (D07 - D035) * 16/15; |E| >= 2e-6 step-dominated, |E| <= 4e-7 k_c-dominated, else mixed
--control: exit 0 only if bar 1 passes (exit 1 otherwise, 2 if R0's record is missing).
--selftest: planted records and Deltas (the bars pass on a good set, each bar fails on its broken case, r reads 3.74 on a planted kappa^4 law and is not formed
under 1e-10, E reads step/kc/mixed on planted values); --mutate makes bar 1 accept everything and the selftest then exits 1."""
import json
import os
import sys

MUT = "--mutate" in sys.argv
D_SRC = 1.174322923415951
STEPS0 = 4179
BAND = {"R1": (5734, 5968), "R2": (8191, 8525)}   # 5851 and 8358, +-2%, rounded outward to the integers inside
FILES = {"R0": "R0/l1kc127k070w2.jsonl", "R1": "R1/l1kc127k050w2.jsonl", "R2": "R2/l1kc127k035w2.jsonl"}
KAPPA = {"R0": 0.7, "R1": 0.5, "R2": 0.35}


def bar1(r):
    if MUT:
        return True, "mutated: accepts"
    ok = r["F"] <= 5e-10 and r["steps"] == STEPS0 and abs(r["Delta"] - D_SRC) <= 1e-9
    return ok, "|F| %.4e (<= 5e-10), steps %d (== %d), |Delta - source| %.3e (<= 1e-9)" % (r["F"], r["steps"], STEPS0, abs(r["Delta"] - D_SRC))


def bar2(name, r):
    lo, hi = BAND[name]
    ok = r["F"] <= 5e-10 and lo <= r["steps"] <= hi
    return ok, "|F| %.4e (<= 5e-10), steps %d (in %d..%d)" % (r["F"], r["steps"], lo, hi)


def order(d07, d05, d035):
    """(r or None, note)"""
    if abs(d05 - d035) < 1e-10:
        return None, "not formed: |D0.5 - D0.35| = %.3e < 1e-10" % abs(d05 - d035)
    return (d07 - d05) / (d05 - d035), "r = (D0.7 - D0.5)/(D0.5 - D0.35)"


def reading(E):
    a = abs(E)
    if a >= 2e-6:
        return "step-dominated (|E| >= 2e-6: kappa must come down before any threshold is quoted)"
    if a <= 4e-7:
        return "k_c-dominated (|E| <= 4e-7: Delta is not converged in k_c at the 1e-6 level)"
    return "mixed (4e-7 < |E| < 2e-6: the follow-on runs)"


def last(path):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    return rows[-1] if rows else None


def load(d):
    out = {}
    for k, f in FILES.items():
        p = os.path.join(d, f)
        if os.path.exists(p):
            r = last(p)
            if r:
                out[k] = r
    return out


def report(rs):
    lines, ok_all = [], True
    lines.append("%-4s %-6s %-7s %-12s %-14s %-22s %-8s" % ("run", "kappa", "steps", "|F|", "constraint", "Delta", "seconds"))
    for k in ("R0", "R1", "R2"):
        if k in rs:
            r = rs[k]
            lines.append("%-4s %-6s %-7d %-12.5e %-14.6e %-22.12f %-8s" % (k, KAPPA[k], r["steps"], r["F"], r["constraint"], r["Delta"], r.get("seconds")))
    lines.append("source (k_c 127, kappa 0.7, winb): steps 4179, |F| 3.1939646e-10, constraint 1.4638405e-3, Delta %.15f" % D_SRC)
    if "R0" in rs:
        ok, w = bar1(rs["R0"]); ok_all &= ok
        lines.append("bar 1 (R0 control): %s (%s)" % ("PASS" if ok else "FAIL", w))
    for k in ("R1", "R2"):
        if k in rs:
            ok, w = bar2(k, rs[k]); ok_all &= ok
            lines.append("bar 2 (%s): %s (%s)" % (k, "PASS" if ok else "FAIL", w))
    if all(k in rs for k in ("R0", "R1", "R2")):
        d07, d05, d035 = rs["R0"]["Delta"], rs["R1"]["Delta"], rs["R2"]["Delta"]
        r, note = order(d07, d05, d035)
        lines.append("bar 3: D0.7 - D0.5 = %.4e, D0.5 - D0.35 = %.4e; %s" % (d07 - d05, d05 - d035, ("r = %.3f (kappa^4 predicts 3.74)" % r) if r is not None else note))
        E = (d07 - d035) * 16.0 / 15.0
        lines.append("bar 4: E = (D0.7 - D0.35) x 16/15 = %.4e; against the 127 to 135 change of -3.9096e-6: %s" % (E, reading(E)))
        lines.append("constraints against the source's 1.4638e-3: R0 %.4e, R1 %.4e, R2 %.4e" % (rs["R0"]["constraint"], rs["R1"]["constraint"], rs["R2"]["constraint"]))
    return ok_all, lines


def selftest():
    bad = []
    good = dict(F=3.19e-10, steps=4179, Delta=D_SRC + 1e-10, constraint=1.46e-3, seconds=1)
    if not bar1(good)[0]:
        bad.append("the good R0 was refused")
    for name, r in (("steps 4180", dict(good, steps=4180)), ("Delta off by 2e-9", dict(good, Delta=D_SRC + 2e-9)), ("|F| 6e-10", dict(good, F=6e-10))):
        if bar1(r)[0]:
            bad.append("bar 1 accepted: " + name)
    g1, g2 = dict(good, steps=5851), dict(good, steps=8358)
    if not (bar2("R1", g1)[0] and bar2("R2", g2)[0]):
        bad.append("a good R1 or R2 was refused")
    for name, f, r in (("R1 steps 5700", "R1", dict(g1, steps=5700)), ("R1 steps 6000", "R1", dict(g1, steps=6000)), ("R2 |F| 7e-10", "R2", dict(g2, F=7e-10)), ("R2 steps 8600", "R2", dict(g2, steps=8600))):
        if bar2(f, r)[0]:
            bad.append("bar 2 accepted: " + name)
    # planted kappa^4 law: Delta(kappa) = D0 + c kappa^4
    D0, c = 1.17432, 5e-5
    d = {k: D0 + c * k ** 4 for k in (0.7, 0.5, 0.35)}
    r, _ = order(d[0.7], d[0.5], d[0.35])
    if r is None or abs(r - 3.74) > 0.01:
        bad.append("r on a planted kappa^4 law reads %r, not 3.74" % (r,))
    if order(1.0, 1.0 + 5e-11, 1.0)[0] is not None:
        bad.append("r was formed under 1e-10")
    E = (d[0.7] - d[0.35]) * 16.0 / 15.0
    if abs(E - c * 0.7 ** 4) > 1e-12:
        bad.append("E on the planted law is %r, not c kappa^4 = %r" % (E, c * 0.7 ** 4))
    for val, want in ((3e-6, "step"), (-3e-6, "step"), (1e-7, "k_c"), (1e-6, "mixed")):
        if not reading(val).startswith(want):
            bad.append("E %r read %r, wanted %s" % (val, reading(val), want))
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s" % ("FAILS" if bad else "passes"))
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    d = [a for a in sys.argv[1:] if not a.startswith("--")][0]
    rs = load(d)
    if "--control" in sys.argv:
        if "R0" not in rs:
            print("R0's record is missing")
            return 2
        ok, w = bar1(rs["R0"])
        print("bar 1 (R0 control): %s (%s)" % ("PASS" if ok else "FAIL", w))
        return 0 if ok else 1
    ok, lines = report(rs)
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
