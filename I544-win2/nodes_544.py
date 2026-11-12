#!/usr/bin/env python3
"""#544: which nodes the weak directions feel. Each interior node of crawlJ's D 242.3642 layout moved by 0.02 (0.4 -> 0.42, 0.5 -> 0.52, 0.6 -> 0.62) and the first node the other way (0.3 -> 0.25), sigma_1..4 raw and equilibrated
as #537 did, against #537's baseline.
usage: python nodes_544.py [--selftest]       (run from I544-win2 after the lanes; needs ../I537-win2/ and the logs of this folder)
Raw sigma from nn_<tag>.log (`near_null.py`), equilibrated (Curtis-Reid + Ruiz) from eq_<tag>.log (`near_null_eq.py`); the shift is ln sigma_i(new layout) - ln sigma_i(baseline).
Acceptance of #544: a table of the equilibrated shift of ln sigma_3 per node move; the 0.25 move reproduces the null (|shift of ln sigma_3| < 0.01, i.e. under 1% in sigma_3, both readings; #537's 0.35 move gave -0.00 raw and +0.00
equilibrated) or the report says the null is not a property of the first node; renode checks and controls as in #537 (all check lines pass, the --mutate sign and --mutate=sigma controls exit 1).
Also printed: the shift per unit of node displacement, and the ratio of each to the last node's (#537: -2.20 equilibrated for 0.7 -> 0.72, i.e. -110 per unit).
--selftest: the null test on planted shifts (0.004 passes, 0.02 fails) and the per-node table on a planted example."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, "..", "I537-win2")
MOVES = (("node2_042", "second node 0.4 -> 0.42", +0.02), ("node3_052", "third node 0.5 -> 0.52", +0.02), ("node4_062", "fourth node 0.6 -> 0.62", +0.02), ("first025", "first node 0.3 -> 0.25", -0.05))
LAST = ("last node 0.7 -> 0.72 (#537)", +0.02, "last072")
NULL = 0.01


def read(p):
    return open(p, encoding="utf-8").read()


def raw(path):
    s = read(path)
    v = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s+sigma_(\d) ([0-9.e+-]+) \(converged", s, re.M)}
    return [v[i] for i in (1, 2, 3, 4)], "check: pass" in s


def eq(path):
    s = read(path)
    v = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s+Curtis-Reid \+ Ruiz sigma_(\d) ([0-9.e+-]+) \(converged", s, re.M)}
    return [v[i] for i in (1, 2, 3, 4)], bool(re.search(r"^check: pass", s, re.M))


def is_null(shift3_raw, shift3_eq):
    return abs(shift3_raw) < NULL and abs(shift3_eq) < NULL


def selftest():
    ok = is_null(0.004, -0.003) and not is_null(0.02, 0.0) and not is_null(0.0, -0.02) and is_null(-0.00, 0.00)
    print("null test on planted shifts: " + ("pass" if ok else "FAIL"))
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    base_r, o1 = raw(os.path.join(OLD, "nn_base.log"))
    base_e, o2 = eq(os.path.join(OLD, "eq_base.log"))
    allok = o1 and o2
    rows, shifts = [], {}
    print("| layout | raw sigma_1 | raw sigma_2 | raw sigma_3 | raw sigma_4 | equilibrated sigma_1 | sigma_2 | sigma_3 | sigma_4 |\n|---|---|---|---|---|---|---|---|---|")
    print("| baseline 0.3, 0.4, 0.5, 0.6, 0.7 (#537) | " + " | ".join(f"{x:.4e}" for x in base_r + base_e) + " |")
    for tag, name, disp in MOVES + ((LAST[2], LAST[0], LAST[1]),):
        d = OLD if tag == "last072" else HERE
        if not os.path.exists(os.path.join(d, f"eq_{tag}.log")):
            continue
        r, a = raw(os.path.join(d, f"nn_{tag}.log"))
        e, b = eq(os.path.join(d, f"eq_{tag}.log"))
        allok = allok and a and b
        shifts[tag] = ([math.log(r[i] / base_r[i]) for i in range(4)], [math.log(e[i] / base_e[i]) for i in range(4)], disp, name)
        print(f"| {name} | " + " | ".join(f"{x:.4e}" for x in r + e) + " |")
    print("\nshifts of ln sigma_i from the baseline (new layout minus baseline)\n| move | reading | ln sigma_1 | ln sigma_2 | ln sigma_3 | ln sigma_4 | ln sigma_3 per unit of node displacement |\n|---|---|---|---|---|---|---|")
    for tag, (sr, se, disp, name) in shifts.items():
        print(f"| {name} | raw | " + " | ".join(f"{x:+.3f}" for x in sr) + f" | {sr[2] / disp:+.1f} |")
        print(f"| {name} | equilibrated | " + " | ".join(f"{x:+.3f}" for x in se) + f" | {se[2] / disp:+.1f} |")
    if "first025" in shifts:
        sr, se = shifts["first025"][0][2], shifts["first025"][1][2]
        print(f"\nthe 0.25 move: shift of ln sigma_3 {sr:+.4f} raw, {se:+.4f} equilibrated; null (both under {NULL}): {'reproduced' if is_null(sr, se) else 'NOT reproduced (the null is not a property of the first node)'}")
    print("all check lines pass" if allok else "a check line is not pass")
    sys.exit(0 if allok else 1)
