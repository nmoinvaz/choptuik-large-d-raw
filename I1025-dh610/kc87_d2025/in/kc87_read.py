#!/usr/bin/env python3
"""#1025 kc87_d2025 (dh610) kc87_read.py READ_LOWER.txt [WIN2_K87_READ_LOWER.txt] | selftest [--mutate]: reads the printed output of read_lower.py (dh170's, blob 89309d3c) for this folder's k_c 87 D 20.25 scan (lambda 1.14 to 1.22 and a repeat of 1.17)
and sets its robust changes beside this machine's k_c 79 D 20.25 ones (`../kc79_d2025`: (1.160, 1.170) '- to +' det-linear 1.167526, range [1.163712, 1.167526]; (1.190, 1.200) '+ to -' det-linear 1.199763, range [1.199698, 1.199763]) by position
(first and second change in the window; orientation as the reader prints it) and, when a second file is given, beside win2's k_c 87 reading by position. The coordinator's written-before: the lambda_1 root stays within 0.005 of its k_c 79 value
(win2's k_c 87 scan says which root that is). Exit 0 after printing (the comparison is information). selftest: planted texts must read as written (equal and +-0.004 within the bar, +0.006 outside, an orientation swap flagged, one change only
flagged); --mutate widens the bar from 0.005 to 0.5, which the +0.006 case must then fail to catch (exit 1)."""
import sys, re

K79 = [(1.167526, "- to +"), (1.199763, "+ to -")]
BAR = 0.005
RC = re.compile(r"robust change \((\d\.\d+), (\d\.\d+)\), (.+?), det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]")


def parse(text):
    return [dict(lo=float(m[0]), hi=float(m[1]), orient=m[2], det=float(m[3]), r0=float(m[4]), r1=float(m[5])) for m in RC.findall(text)]


def compare(ch, ref, bar=BAR):
    """per position: (mine, reference (det, orientation), difference, same orientation, within bar); None when the counts differ"""
    if len(ch) != len(ref):
        return None
    return [(c, w, c["det"] - w[0], c["orient"] == w[1], abs(c["det"] - w[0]) <= bar) for c, w in zip(ch, ref)]


def planted(d1, d2, o1="- to +", o2="+ to -"):
    return (f"  robust change (1.160, 1.170), {o1}, det-linear {1.167526 + d1:.6f}, range [1.163712, {1.167526 + d1:.6f}]\n"
            f"  robust change (1.190, 1.200), {o2}, det-linear {1.199763 + d2:.6f}, range [1.199698, {1.199763 + d2:.6f}]\n")


def selftest(mutate):
    bar = 0.5 if mutate else BAR
    good = lambda r: r and all(x[3] and x[4] for x in r)
    cases = [("equal to the k_c 79 values", planted(0, 0), good), ("+0.004 and -0.004 within", planted(0.004, -0.004), good),
             ("+0.006 outside (first)", planted(0.006, 0), lambda r: r and not r[0][4] and r[1][4]),
             ("orientation swapped flagged", planted(0, 0, "+ to -", "- to +"), lambda r: r and not r[0][3] and not r[1][3]),
             ("one change only: no pairing", planted(0, 0).splitlines()[0] + "\n", lambda r: r is None)]
    bad = 0
    for name, txt, want in cases:
        ok = bool(want(compare(parse(txt), K79, bar)))
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
    print(f"| position | mine: bracket, orientation, det-linear, estimator range | {name}: det-linear, orientation | mine minus it | same orientation | within {BAR} |")
    print("|---|---|---|---|---|---|")
    for i, (c, w, d, so, wi) in enumerate(r, 1):
        print(f"| {i} | ({c['lo']:.3f}, {c['hi']:.3f}), {c['orient']}, {c['det']:.6f}, [{c['r0']:.6f}, {c['r1']:.6f}] | {w[0]:.6f}, {w[1]} | {d:+.6f} | {so} | {wi} |")


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    text = open(sys.argv[1]).read()
    ch = parse(text)
    sg = re.search(r"hybrid signs: (.*)", text)
    print(f"hybrid signs: {sg.group(1).strip() if sg else None}")
    print(f"robust changes: {len(ch)} (this machine's k_c 79: 2)")
    for c in ch:
        print(f"   change ({c['lo']:.3f}, {c['hi']:.3f}), {c['orient']}, det-linear {c['det']:.6f}, range [{c['r0']:.6f}, {c['r1']:.6f}]")
    table(ch, K79, "this machine's k_c 79")
    if len(sys.argv) > 2:
        w = parse(open(sys.argv[2]).read())
        table(ch, [(c["det"], c["orient"]) for c in w], "win2's k_c 87")
