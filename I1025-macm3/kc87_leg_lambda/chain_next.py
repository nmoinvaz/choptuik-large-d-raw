#!/usr/bin/env python3
"""chain_next.py: the bookkeeping of the k_c 87 leg2 scan chain (#1025 macm3; t5's rules of 24 Nov: each leg point is scanned with the latest-local-slope rule, the -0.33 rule scored beside it).
usage: chain_next.py next            prints NEXT D PREV_D PREV_ROOT SLOPE SRC TAG | WAIT why | DONE | STOP why
       chain_next.py pending         prints the pushed points that have a SCAN_DONE.txt and no root yet
       chain_next.py record D        reads D/read_lower.txt and D/steps.txt; appends the root to roots87.txt and prints the hc line (OK ...) or STOP why
       chain_next.py selftest [--mutate=slope|changes|repeat|robust]
Files: roots87.txt (lines "D root lo hi source"), ../kc87_leg2/pushed_points.txt (part a, tag l1kc87Lmacm3), ../kc87_leg2/b/pushed_points.txt (part b, tag l1kc87Lmacm3b).
Rule (t5, 24 Nov): for a point D, with a and b the two largest D below it that have a root (a > b; the seeds D 21.21875 and D 21.25 included): slope = (root[a] - root[b]) / (a - b) (my det-linear roots, whatever their spacing),
prediction = root[a] + slope x (D - a); the beside rule is root[a] - 0.33 x (D - a).
Which points: while a leap runs (part a or part b not finished; phase 1) only the pushed points on the 0.125 grid (D x 8 an integer: 21.375, 21.5, 21.625, ...), lowest first; when the leaps have ended (phase 2) every pushed point, in D order
(t5: "the points between are scanned after part b ends, in D order"). A point is scanned only when two roots lie below it."""
import os, re, sys
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
L2 = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2")
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
PARTS = (("a", L2, "I1025-macm3/kc87_leg2", "l1kc87Lmacm3"), ("b", L2 + "/b", "I1025-macm3/kc87_leg2/b", "l1kc87Lmacm3b"))
BESIDE = -0.33


def read_roots(path):
    r = {}
    if os.path.exists(path):
        for l in open(path):
            f = l.split()
            if len(f) >= 2 and not l.startswith("#"):
                r[float(f[0])] = float(f[1])
    return r


def read_pushed(folder):
    p = folder + "/pushed_points.txt"
    return [float(x) for x in open(p).read().split()] if os.path.exists(p) else []


def on_grid(D):
    return abs(D * 8 - round(D * 8)) < 1e-9


def plan(roots, pushed, phase1=True):
    """pushed: {D: (src, tag)}; phase1: only the 0.125 grid (a leap is running). Returns ('NEXT', D, a, root[a], slope, src, tag) or ('WAIT', why)."""
    for D in sorted(pushed):
        if D in roots:
            continue
        if phase1 and MUT != "all" and not on_grid(D):
            continue
        below = sorted(x for x in roots if x < D)
        if len(below) < 2:
            return ("WAIT", "fewer than two roots below D %r" % D)
        a, b = below[-1], below[-2]
        slope = (roots[a] - roots[b]) / (a - b)
        if MUT == "slope":
            slope = BESIDE
        src, tag = pushed[D]
        return ("NEXT", D, a, roots[a], slope, src, tag)
    return ("WAIT", "no pushed point without a root" + (" on the 0.125 grid" if phase1 else ""))


def phase1_now():
    """a leap is running unless both parts have a LEG_DONE.txt, or part a is done and part b was refused (start_b.log says NOT started)"""
    a = os.path.exists(L2 + "/LEG_DONE.txt"); b = os.path.exists(L2 + "/b/LEG_DONE.txt")
    refused = os.path.exists(L2 + "/start_b.log") and "NOT started" in open(L2 + "/start_b.log").read()
    return not (b or (a and refused))


def parse(text, steps, mutate=None):
    """-> (ok, why, bracket(a, b), root, lo, hi)"""
    m = re.search(r"robust changes: (\d+);", text)
    n = int(m.group(1)) if m else -1
    if (n != 1 and mutate != "changes") or n < 1:
        return (False, "robust changes: %d (one wanted)" % n, None, None, None, None)
    if mutate != "robust" and not re.search(r"not noise-robust: none", text):
        return (False, "a point is not noise-robust", None, None, None, None)
    if mutate != "repeat" and "PASS" not in text:
        return (False, "the repeat check did not pass", None, None, None, None)
    if not re.search(r"local minima without a sign change: none", text):
        return (False, "an ln|det| minimum without a sign change", None, None, None, None)
    c = re.search(r"robust change \(([\d.]+), ([\d.]+)\), ([-+] to [-+]), det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]", text)
    if not c:
        return (False, "no robust change line", None, None, None, None)
    return (True, "", (float(c.group(1)), float(c.group(2))), float(c.group(4)), float(c.group(5)), float(c.group(6)))


def selftest():
    ok = True
    def chk(name, cond):
        nonlocal ok
        print("planted:", name, "PASS" if cond else "FAIL"); ok = ok and cond
    roots = {21.21875: 0.847216, 21.25: 0.836238}
    pushed = {21.3125: ("A", "ta")}
    r = plan(roots, pushed, phase1=False)
    chk("phase 2, first leg point: NEXT 21.3125, prev root 0.836238, slope -0.35130 (t5's -0.3513)", r[0] == "NEXT" and r[1] == 21.3125 and r[2] == 21.25 and abs(r[4] + 0.351296) < 1e-9 and r[3] == 0.836238)
    chk("phase 1: 21.3125 is not on the 0.125 grid, so WAIT", plan(roots, pushed, phase1=True)[0] == "WAIT")
    roots[21.3125] = 0.8143
    pushed.update({21.375: ("A", "ta"), 21.4375: ("B", "tb"), 21.5: ("A", "ta"), 21.5625: ("B", "tb"), 21.625: ("B", "tb")})
    r = plan(roots, pushed, phase1=True)
    chk("phase 1: the grid point 21.375 comes first, slope from the two latest roots", r[0] == "NEXT" and r[1] == 21.375 and abs(r[4] - (0.8143 - 0.836238) / 0.0625) < 1e-9)
    roots[21.375] = 0.79
    r = plan(roots, pushed, phase1=True)
    chk("phase 1: after 21.375 the next is 21.5 (21.4375 skipped), step 0.125 from the root of 21.375", r[0] == "NEXT" and r[1] == 21.5 and r[2] == 21.375 and abs(r[4] - (0.79 - 0.8143) / 0.0625) < 1e-9)
    roots[21.5] = 0.75
    r = plan(roots, pushed, phase1=True)
    chk("phase 1: then 21.625, slope across the 0.125 spacing of the two latest roots (21.5 and 21.375)", r[0] == "NEXT" and r[1] == 21.625 and r[2] == 21.5 and abs(r[4] - (0.75 - 0.79) / 0.125) < 1e-9 and r[5:] == ("B", "tb"))
    r = plan(roots, {k: v for k, v in pushed.items() if k != 21.625}, phase1=True)
    chk("phase 1: only off-grid points left: WAIT", r[0] == "WAIT")
    r = plan(roots, {k: v for k, v in pushed.items() if k != 21.625}, phase1=False)
    chk("phase 2: the skipped 21.4375 in D order, the two latest roots below it (21.375, 21.3125)", r[0] == "NEXT" and r[1] == 21.4375 and r[2] == 21.375 and abs(r[4] - (0.79 - 0.8143) / 0.0625) < 1e-9)
    chk("fewer than two roots below: WAIT", plan({21.25: 0.8}, {21.3125: ("A", "ta")}, phase1=False)[0] == "WAIT")
    good = "points 5 in 0.805-0.825; not noise-robust: none\nrobust changes: 1; touching a non-robust point (not counted): none\n  robust change (0.810, 0.815), - to +, det-linear 0.8143, range [0.8130, 0.8143]\nln|det| local minima without a sign change: none\nrepeat check x: agree -> PASS\n"
    p = parse(good, "", MUT)
    chk("a clean reading parses (bracket, root, range)", p[0] and p[2] == (0.81, 0.815) and p[3] == 0.8143 and p[4] == 0.813)
    chk("two robust changes: STOP", not parse(good.replace("robust changes: 1", "robust changes: 2"), "", MUT)[0])
    chk("a non-robust point: STOP", not parse(good.replace("not noise-robust: none", "not noise-robust: [0.82]"), "", MUT)[0])
    chk("a failed repeat: STOP", not parse(good.replace("PASS", "FAIL"), "", MUT)[0])
    chk("a minimum without a sign change: STOP", not parse(good.replace("local minima without a sign change: none", "local minima without a sign change: [0.8]"), "", MUT)[0])
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    cmd = sys.argv[1]
    if cmd == "selftest":
        sys.exit(selftest())
    roots = read_roots(L + "/roots87.txt")
    pushed = {}
    for part, folder, src, tag in PARTS:
        for D in read_pushed(folder):
            pushed[D] = (src, tag)
    if cmd == "next":
        r = plan(roots, pushed, phase1_now())
        if r[0] == "NEXT":
            print("NEXT %r %r %.6f %.6f %s %s" % (r[1], r[2], r[3], r[4], r[5], r[6]))
        else:
            fin = all(os.path.exists(f + "/LEG_DONE.txt") for _, f, _, _ in PARTS) and all(D in roots for D in pushed)
            print(("DONE" if fin else "WAIT " + r[1]))
    elif cmd == "pending":   # pushed points whose scan is done (SCAN_DONE.txt) and that have no root yet, in D order
        print(" ".join(repr(D) for D in sorted(pushed) if D not in roots and os.path.exists("%s/%r/SCAN_DONE.txt" % (L, D))))
    elif cmd == "record":
        D = float(sys.argv[2]); dn = repr(D)
        text = open("%s/%s/read_lower.txt" % (L, dn)).read()
        steps = open("%s/%s/steps.txt" % (L, dn)).read()
        if not os.path.exists("%s/%s/SCAN_DONE.txt" % (L, dn)):
            print("STOP no SCAN_DONE.txt for D %s" % dn); return
        ok, why, br, root, lo, hi = parse(text, steps, MUT)
        if not ok:
            print("STOP D %s: %s" % (dn, why)); return
        below = sorted(x for x in roots if x < D)
        a, b = below[-1], below[-2]
        slope = (roots[a] - roots[b]) / (a - b); pred = roots[a] + slope * (D - a); pred2 = roots[a] + BESIDE * (D - a)
        new = (root - roots[a]) / (D - a)
        with open(L + "/roots87.txt", "a") as f:
            f.write("%r %.6f %.6f %.6f macm3 bracket %.3f %.3f\n" % (D, root, lo, hi, br[0], br[1]))
        print("OK macm3 #1025 kc87 leg2 ROOT D %s: %.6f (det-linear; estimator range %.6f-%.6f, not an enclosure), bracket (%.3f, %.3f). Rule (local slope %.4f): %.6f, residual %+.6f; beside (-0.33): %.6f, residual %+.6f. New local slope %.4f." % (
            dn, root, lo, hi, br[0], br[1], slope, pred, root - pred, pred2, root - pred2, new))


if __name__ == "__main__":
    main()
