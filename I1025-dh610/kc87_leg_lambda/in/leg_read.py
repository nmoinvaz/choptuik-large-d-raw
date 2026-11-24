#!/usr/bin/env python3
"""#1025 kc79_leg (dh610) leg_read.py read READ_LOWER.txt PRED [BAR=0.01] | widen SCAN.jsonl LO HI | selftest [--mutate]:
read: the printed output of read_lower.py (blob 89309d3c) for one D of win2's k_c 79 leg; prints the robust changes by position (bracket, orientation as the reader prints it, det-linear, estimator range) and, for exactly one change,
its difference from the coordinator's prediction and whether it is within BAR (0.01); zero or several changes: no pairing (zero is reported with the end signs).
widen: for a window with no robust change, the side to widen by 0.015: the window edge where the hybrid ln|det| is lower (|det| falls toward a root beyond that edge; the orientation of the sign change is not used, it
differs between D's); prints `low l1,l2,l3` or `high l1,l2,l3` (three values at 0.005 steps beyond that edge); exit 3 when the two edge ln values are equal.
Exit 0 after printing. selftest: planted texts and rows must read as written (within and outside the bar, no change, two changes; the widening side both ways); --mutate widens the bar to 0.5 and swaps the widening
side, which the outside-the-bar case and the side cases must then fail to catch (exit 1)."""
import sys, re, json

BAR = 0.01
RC = re.compile(r"robust change \((\d\.\d+), (\d\.\d+)\), (.+?), det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]")


def parse(text):
    return [dict(lo=float(m[0]), hi=float(m[1]), orient=m[2], det=float(m[3]), r0=float(m[4]), r1=float(m[5])) for m in RC.findall(text)]


def compare(ch, pred, bar=BAR):
    """(change minus prediction, within bar) for exactly one change; None otherwise"""
    if len(ch) != 1:
        return None
    d = ch[0]["det"] - pred
    return d, abs(d) <= bar


def widen_side(rows, lo, hi, swap=False):
    """rows: dicts with lam, ln. returns (side, three new lambdas) by the lower hybrid ln|det| at the two window edges; None when equal"""
    at = lambda x: [r for r in rows if abs(r["lam"] - x) < 1e-9][0]
    a, b = at(lo)["ln"], at(hi)["ln"]
    if a == b:
        return None
    low = a < b
    if swap:
        low = not low
    if low:
        return "low", [round(lo - 0.005 * k, 3) for k in (1, 2, 3)]
    return "high", [round(hi + 0.005 * k, 3) for k in (1, 2, 3)]


def planted(*dets):
    return "".join(f"  robust change ({x - 0.0025:.3f}, {x + 0.0025:.3f}), - to +, det-linear {x:.6f}, range [{x - 0.001:.6f}, {x:.6f}]\n" for x in dets)


def selftest(mutate):
    bar = 0.5 if mutate else BAR
    P = 0.958
    rows = [dict(lam=0.945 + 0.005 * k, ln=-2400.0 - k) for k in range(7)]      # ln falls toward the high edge
    rowsl = [dict(lam=r["lam"], ln=-r["ln"]) for r in rows]                       # ln falls toward the low edge
    ok = lambda c: bool(c)
    cases = [("one change within the bar", compare(parse(planted(P + 0.009)), P, bar), lambda r: r and r[1]),
             ("one change outside the bar", compare(parse(planted(P + 0.011)), P, bar), lambda r: r and not r[1]),
             ("no change: no pairing", compare(parse(""), P, bar), lambda r: r is None),
             ("two changes: no pairing", compare(parse(planted(P, P + 0.1)), P, bar), lambda r: r is None),
             ("ln falls toward the high edge: widen high", widen_side(rows, 0.945, 0.975, mutate), lambda r: r and r[0] == "high" and r[1] == [0.98, 0.985, 0.99]),
             ("ln falls toward the low edge: widen low", widen_side(rowsl, 0.945, 0.975, mutate), lambda r: r and r[0] == "low" and r[1] == [0.94, 0.935, 0.93]),
             ("equal edge ln: no side", widen_side([dict(lam=0.945, ln=-1.0), dict(lam=0.975, ln=-1.0)], 0.945, 0.975), lambda r: r is None)]
    bad = 0
    for name, got, want in cases:
        good = ok(want(got))
        bad += not good
        print(f"  {name}: {'ok' if good else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    if cmd == "read":
        text = open(sys.argv[2]).read()
        pred = float(sys.argv[3])
        bar = float(sys.argv[4]) if len(sys.argv) > 4 else BAR
        ch = parse(text)
        sg = re.search(r"hybrid signs: (.*)", text)
        print(f"hybrid signs: {sg.group(1).strip() if sg else None}")
        print(f"robust changes: {len(ch)}")
        for c in ch:
            print(f"   change ({c['lo']:.3f}, {c['hi']:.3f}), {c['orient']}, det-linear {c['det']:.6f}, range [{c['r0']:.6f}, {c['r1']:.6f}]")
        r = compare(ch, pred, bar)
        if r is None:
            print(f"against the prediction {pred} (+-{bar}): {len(ch)} changes, no pairing by position")
        else:
            print(f"against the prediction {pred}: change minus prediction {r[0]:+.6f}; within {bar}: {r[1]}")
    if cmd == "widen":
        rows = [json.loads(l) for l in open(sys.argv[2]) if l.strip()]
        w = widen_side(rows, float(sys.argv[3]), float(sys.argv[4]))
        if w is None:
            print("no side: the edge ln|det| values are equal")
            sys.exit(3)
        print(w[0], ",".join(f"{x:.3f}" for x in w[1]))
