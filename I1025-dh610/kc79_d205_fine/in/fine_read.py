#!/usr/bin/env python3
"""#1025 kc79_d205_fine (dh610) fine_read.py READ_LOWER.txt | selftest [--mutate]: reads the printed output of read_lower.py (blob 89309d3c) for this folder's k_c 79 D 20.5 scan on dh170's state (lambda 1.060 to 1.090 by 0.005,
7 evaluations) and sets its robust change beside this machine's k_c 87 one at D 20.5 (`../kc87_d205`, raw 2514221e: (1.075, 1.080), det-linear 1.077872) by position, and beside dh170's two-point k_c 79 estimate 1.087574
(his 0.03 grid; (1.060, 1.090)). The coordinator's written-before: the k_c 79 root on the fine grid lies within 0.002 of 1.077872. The orientation is printed as the reader prints it and not compared across k_c. Exit 0 after
printing (information). selftest: planted texts must read as written (equal and +-0.0019 within the bar, +0.0021 outside, none or two changes against one: no pairing); --mutate widens the bar from 0.002 to 0.5, which the
+0.0021 case must then fail to catch (exit 1)."""
import sys, re

K87, DH170, BAR = 1.077872, 1.087574, 0.002
RC = re.compile(r"robust change \((\d\.\d+), (\d\.\d+)\), (.+?), det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]")


def parse(text):
    return [dict(lo=float(m[0]), hi=float(m[1]), orient=m[2], det=float(m[3]), r0=float(m[4]), r1=float(m[5])) for m in RC.findall(text)]


def compare(ch, ref=K87, bar=BAR):
    """(mine minus the reference, within bar) for the single change; None unless exactly one change"""
    if len(ch) != 1:
        return None
    d = ch[0]["det"] - ref
    return d, abs(d) <= bar


def planted(*dets):
    return "".join(f"  robust change ({x - 0.005:.3f}, {x + 0.005:.3f}), - to +, det-linear {x:.6f}, range [{x - 0.001:.6f}, {x:.6f}]\n" for x in dets)


def selftest(mutate):
    bar = 0.5 if mutate else BAR
    cases = [("equal to the k_c 87 root", planted(K87), lambda r: r and r[1]), ("+0.0019 within", planted(K87 + 0.0019), lambda r: r and r[1]), ("-0.0019 within", planted(K87 - 0.0019), lambda r: r and r[1]),
             ("+0.0021 outside", planted(K87 + 0.0021), lambda r: r and not r[1]), ("no change: no pairing", "", lambda r: r is None),
             ("two changes: no pairing", planted(K87, K87 + 0.02), lambda r: r is None)]
    bad = 0
    for name, txt, want in cases:
        ok = bool(want(compare(parse(txt), K87, bar)))
        bad += not ok
        print(f"  {name}: {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    text = open(sys.argv[1]).read()
    ch = parse(text)
    sg = re.search(r"hybrid signs: (.*)", text)
    print(f"hybrid signs: {sg.group(1).strip() if sg else None}")
    print(f"robust changes: {len(ch)}")
    for c in ch:
        print(f"   change ({c['lo']:.3f}, {c['hi']:.3f}), {c['orient']}, det-linear {c['det']:.6f}, range [{c['r0']:.6f}, {c['r1']:.6f}]")
    r = compare(ch)
    if r is None:
        print(f"against this machine's k_c 87 (1.077872): the count is {len(ch)}, not 1: no pairing by position")
    else:
        print(f"against this machine's k_c 87 root {K87}: k_c 79 (fine grid) minus k_c 87 = {r[0]:+.6f}; within {BAR}: {r[1]}")
        print(f"against dh170's coarse two-point estimate {DH170} (0.03 grid, bracket (1.060, 1.090)): fine grid minus coarse = {ch[0]['det'] - DH170:+.6f}")
