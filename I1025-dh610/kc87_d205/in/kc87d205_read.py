#!/usr/bin/env python3
"""#1025 kc87_d205 (dh610) kc87d205_read.py READ_LOWER.txt [DH170_K79_READ_LOWER.txt] | selftest [--mutate]: reads the printed output of read_lower.py (dh170's, blob 89309d3c) for this folder's k_c 87 D 20.5 scan
(lambda 1.050 to 1.120 by 0.005 and a repeat of 1.085) and sets its robust changes beside dh170's k_c 79 D 20.5 ones by position (the first change in the window, the second, ...). Without a second file the reference is the
coordinator's one number, det-linear 1.087574 (dh170's scan on the 0.03 grid, raw I1025-dh170/kc79_d205 at 9535a78a); with dh170's own final reading the reference is that reading's changes. The coordinator's written-before: one robust change
within 0.005 of dh170's k_c 79 root. Orientation is printed as the reader prints it and is not compared across k_c. Exit 0 after printing (the comparison is information). selftest: planted texts must read as written (equal and +-0.004
within the bar, +0.006 outside, one change against two references and none against one: no pairing); --mutate widens the bar from 0.005 to 0.5, which the +0.006 case must then fail to catch (exit 1)."""
import sys, re

REF = [1.087574]
BAR = 0.005
RC = re.compile(r"robust change \((\d\.\d+), (\d\.\d+)\), (.+?), det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]")


def parse(text):
    return [dict(lo=float(m[0]), hi=float(m[1]), orient=m[2], det=float(m[3]), r0=float(m[4]), r1=float(m[5])) for m in RC.findall(text)]


def compare(ch, ref, bar=BAR):
    """per position: (mine, reference det-linear, difference, within bar); None when the counts differ"""
    if len(ch) != len(ref):
        return None
    return [(c, w, c["det"] - w, abs(c["det"] - w) <= bar) for c, w in zip(ch, ref)]


def planted(*dets):
    return "".join(f"  robust change ({x - 0.005:.3f}, {x + 0.005:.3f}), - to +, det-linear {x:.6f}, range [{x - 0.002:.6f}, {x:.6f}]\n" for x in dets)


def selftest(mutate):
    bar = 0.5 if mutate else BAR
    good = lambda r: r and all(x[3] for x in r)
    r0 = REF[0]
    cases = [("equal to the reference", planted(r0), REF, good), ("+0.004 within", planted(r0 + 0.004), REF, good), ("-0.004 within", planted(r0 - 0.004), REF, good),
             ("+0.006 outside", planted(r0 + 0.006), REF, lambda r: r and not r[0][3]),
             ("one change against two references: no pairing", planted(r0), REF + [1.15], lambda r: r is None),
             ("no change against one reference: no pairing", "", REF, lambda r: r is None),
             ("two changes against two: second +0.006 outside", planted(r0, 1.15 + 0.006), REF + [1.15], lambda r: r and r[0][3] and not r[1][3])]
    bad = 0
    for name, txt, ref, want in cases:
        ok = bool(want(compare(parse(txt), ref, bar)))
        bad += not ok
        print(f"  {name}: {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


def table(ch, ref, name):
    r = compare(ch, ref)
    if r is None:
        print(f"against {name}: the counts differ ({len(ch)} against {len(ref)}): no pairing by position")
        return
    print(f"against {name}:")
    print(f"| position | mine: bracket, orientation as printed, det-linear, estimator range | {name}: det-linear | mine minus it | within {BAR} |")
    print("|---|---|---|---|---|")
    for i, (c, w, d, wi) in enumerate(r, 1):
        print(f"| {i} | ({c['lo']:.3f}, {c['hi']:.3f}), {c['orient']}, {c['det']:.6f}, [{c['r0']:.6f}, {c['r1']:.6f}] | {w:.6f} | {d:+.6f} | {wi} |")


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
    table(ch, REF, "the coordinator's dh170 k_c 79 number (0.03 grid)")
    if len(sys.argv) > 2:
        w = parse(open(sys.argv[2]).read())
        table(ch, [c["det"] for c in w], "dh170's final k_c 79 reading")
