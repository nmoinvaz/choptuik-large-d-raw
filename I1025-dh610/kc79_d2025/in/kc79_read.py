#!/usr/bin/env python3
"""#1025 kc79_d2025 (dh610) kc79_read.py READ_LOWER.txt | selftest [--mutate]: reads the printed output of read_lower.py (dh170's, blob 89309d3c) for this folder's k_c 79 D 20.25 scan (lambda 1.13 to 1.24 and a repeat of 1.16) and sets its robust changes beside
win2's (`in/ref_win2_read_lower_k79_D2025.txt`, blob e229442a: (1.160, 1.170) '- to +' det-linear 1.165140, range [1.162108, 1.165140]; (1.200, 1.210) '+ to -' det-linear 1.203492, range [1.202702, 1.203492]), by position (first and second change in the window),
orientation as the reader prints it. The coordinator's written-before: two robust changes, each within about 0.005 of win2's. Exit 0 after printing (the comparison is information). selftest: planted texts must read as written (equal and +0.004 within the bar,
+0.006 outside, an orientation swap flagged, one change only flagged); --mutate widens the bar from 0.005 to 0.5, which the +0.006 case must then fail to catch (exit 1)."""
import sys, re

WIN2 = [(1.165140, "- to +", 1.162108, 1.165140), (1.203492, "+ to -", 1.202702, 1.203492)]
BAR = 0.005
RC = re.compile(r"robust change \((\d\.\d+), (\d\.\d+)\), (.+?), det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]")


def parse(text):
    return [dict(lo=float(m[0]), hi=float(m[1]), orient=m[2], det=float(m[3]), r0=float(m[4]), r1=float(m[5])) for m in RC.findall(text)]


def compare(ch, bar=BAR):
    """per position: (mine, win2's, difference, same orientation, within bar); None when the count is not 2"""
    if len(ch) != len(WIN2):
        return None
    return [(c, w, c["det"] - w[0], c["orient"] == w[1], abs(c["det"] - w[0]) <= bar) for c, w in zip(ch, WIN2)]


def planted(d1, d2, o1="- to +", o2="+ to -"):
    return (f"  robust change (1.160, 1.170), {o1}, det-linear {1.165140 + d1:.6f}, range [1.162108, {1.165140 + d1:.6f}]\n"
            f"  robust change (1.200, 1.210), {o2}, det-linear {1.203492 + d2:.6f}, range [1.202702, {1.203492 + d2:.6f}]\n")


def selftest(mutate):
    bar = 0.5 if mutate else BAR
    cases = [("equal to win2's", planted(0, 0), lambda r: r and all(x[3] and x[4] for x in r)), ("+0.004 and -0.004 within", planted(0.004, -0.004), lambda r: r and all(x[3] and x[4] for x in r)),
             ("+0.006 outside (first)", planted(0.006, 0), lambda r: r and not r[0][4] and r[1][4]), ("orientation swapped flagged", planted(0, 0, "+ to -", "- to +"), lambda r: r and not r[0][3] and not r[1][3]),
             ("one change only: no pairing", planted(0, 0).splitlines()[0] + "\n", lambda r: r is None)]
    bad = 0
    for name, txt, want in cases:
        ok = bool(want(compare(parse(txt), bar)))
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
    print(f"robust changes: {len(ch)} (win2's: 2)")
    r = compare(ch)
    if r is None:
        for c in ch:
            print(f"   change ({c['lo']:.3f}, {c['hi']:.3f}), {c['orient']}, det-linear {c['det']:.6f}, range [{c['r0']:.6f}, {c['r1']:.6f}]")
        print("the count is not 2: no pairing by position")
    else:
        print("| position | mine: bracket, orientation, det-linear, estimator range | win2's: det-linear, range | mine minus win2's | same orientation | within 0.005 |")
        print("|---|---|---|---|---|---|")
        for i, (c, w, d, so, wi) in enumerate(r, 1):
            print(f"| {i} | ({c['lo']:.3f}, {c['hi']:.3f}), {c['orient']}, {c['det']:.6f}, [{c['r0']:.6f}, {c['r1']:.6f}] | {w[0]:.6f}, [{w[2]:.6f}, {w[3]:.6f}] | {d:+.6f} | {so} | {wi} |")
