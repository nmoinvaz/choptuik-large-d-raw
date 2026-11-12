#!/usr/bin/env python3
"""#537: raw and equilibrated sigma_1..4 of the three layouts at D 242.36 (first node 0.3, 0.35; last node 0.7, 0.72) and the shifts of ln sigma_3 from the baseline, judged by the issue's rule.
usage: python table_537.py        (run from I537-win2 after lane_a.sh and lane_b.sh; reads nn_base.log, nn_first035.log, nn_last072.log, eq_base.log, eq_first035.log, eq_last072.log)
Rule: fast mode holds if both raw shifts of ln sigma_3 are within 20% of +41 (first node 0.3 -> 0.35) and -13.7 (last node 0.7 -> 0.72); G^p holds if the first shift is below 8.2 in size and the last is positive (p = shift / 6.7).
The same rule is applied to the equilibrated shifts (Curtis-Reid + Ruiz) beside the raw ones. Exits 1 if the check lines of the six logs are not all pass."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TAGS = (("base", "baseline (0.3 ... 0.7)"), ("first035", "first node 0.35 (0.35 ... 0.7)"), ("last072", "last node 0.72 (0.3 ... 0.72)"))
FAST_FIRST, FAST_LAST, G_FIRST_MAX = 41.0, -13.7, 8.2


def read(name):
    return open(os.path.join(HERE, name), encoding="utf-8").read()


def raw(tag):
    s = read(f"nn_{tag}.log")
    v = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s+sigma_(\d) ([0-9.e+-]+) \(converged", s, re.M)}
    ok = "check: pass" in s
    return [v[i] for i in (1, 2, 3, 4)], ok


def eq(tag, method="Curtis-Reid + Ruiz"):
    s = read(f"eq_{tag}.log")
    v = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s+" + re.escape(method) + r" sigma_(\d) ([0-9.e+-]+) \(converged", s, re.M)}
    ok = bool(re.search(r"^check: pass", s, re.M))
    return [v[i] for i in (1, 2, 3, 4)], ok


def verdict(first, last):
    fast = abs(first - FAST_FIRST) <= 0.2 * FAST_FIRST and abs(last - FAST_LAST) <= 0.2 * abs(FAST_LAST)
    g = abs(first) < G_FIRST_MAX and last > 0
    return fast, g


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    R, E, allok = {}, {}, True
    for tag, _ in TAGS:
        R[tag], ok1 = raw(tag)
        E[tag], ok2 = eq(tag)
        allok = allok and ok1 and ok2
    print("| layout | raw sigma_1 | raw sigma_2 | raw sigma_3 | raw sigma_4 | equilibrated sigma_1 | sigma_2 | sigma_3 | sigma_4 |\n|---|---|---|---|---|---|---|---|---|")
    for tag, name in TAGS:
        print(f"| {name} | " + " | ".join(f"{x:.4e}" for x in R[tag]) + " | " + " | ".join(f"{x:.4e}" for x in E[tag]) + " |")
    print("\nshifts of ln sigma_i from the baseline (new layout minus baseline)")
    print("| change | reading | ln sigma_1 | ln sigma_2 | ln sigma_3 | ln sigma_4 |\n|---|---|---|---|---|---|")
    sh = {}
    for tag, name in TAGS[1:]:
        for kind, S in (("raw", R), ("equilibrated", E)):
            d = [math.log(S[tag][i] / S["base"][i]) for i in range(4)]
            sh[(tag, kind)] = d
            print(f"| {name} | {kind} | " + " | ".join(f"{x:+.2f}" for x in d) + " |")
    print(f"\nthe issue's predictions: fast mode +{FAST_FIRST:g} (first node) and {FAST_LAST:g} (last node), G^p 0 and +6.7p")
    for kind in ("raw", "equilibrated"):
        f, l = sh[("first035", kind)][2], sh[("last072", kind)][2]
        fast, g = verdict(f, l)
        p = l / 6.7
        print(f"{kind}: first shift of ln sigma_3 {f:+.2f} ({100 * f / FAST_FIRST:.0f}% of +41), last shift {l:+.2f} ({100 * l / FAST_LAST:.0f}% of -13.7); fast mode {'holds' if fast else 'excluded'}; G^p {'holds' if g else 'excluded'}" + (f" (p = {p:.2f})" if g else ""))
    fr, lr = sh[("first035", "raw")][2], sh[("last072", "raw")][2]
    fe, le = sh[("first035", "equilibrated")][2], sh[("last072", "equilibrated")][2]
    vr, ve = verdict(fr, lr), verdict(fe, le)
    print("raw and equilibrated readings " + ("agree" if vr == ve else "DISAGREE (a discrepancy)"))
    print("all six checks pass" if allok else "a check line is not pass")
    sys.exit(0 if allok else 1)
