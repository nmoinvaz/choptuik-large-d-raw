#!/usr/bin/env python3
"""chain_next.py: the bookkeeping of the k_c 87 leg2 scan chain (#1025 macm3; t5's rules of 24 Nov: each leg point is scanned with the latest-local-slope rule, the -0.33 rule scored beside it).
usage: chain_next.py next            prints NEXT D PREV_D PREV_ROOT SLOPE SRC TAG | WAIT why | DONE | STOP why
       chain_next.py pending         prints the pushed points that have a SCAN_DONE.txt and no root yet
       chain_next.py record D        reads D/read_lower.txt and D/steps.txt; appends the root to roots87.txt and prints the hc line (OK ...) or STOP why
       chain_next.py selftest [--mutate=slope|changes|repeat|robust]
Files: roots87.txt (lines "D root lo hi source"), ../kc87_leg2/pushed_points.txt (part a, tag l1kc87Lmacm3), ../kc87_leg2/b/pushed_points.txt (part b, tag l1kc87Lmacm3b).
Rule: for the k-th point of the sequence [21.21875, 21.25, pushed points in D order]: slope = (root[k-1] - root[k-2]) / (D[k-1] - D[k-2]) (my det-linear roots), prediction = root[k-1] + slope x (D[k] - D[k-1]);
the beside rule is root[k-1] - 0.33 x (D[k] - D[k-1]). A point is scanned only when both predecessors have roots."""
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


def plan(roots, pushed, seeds=(21.21875, 21.25)):
    """pushed: {D: (src, tag)}; returns ('NEXT', D, PD, PR, slope, src, tag) or ('WAIT', why)."""
    seq = list(seeds) + sorted(pushed)
    for k in range(2, len(seq)):
        D = seq[k]
        if D in roots:
            continue
        a, b = seq[k - 1], seq[k - 2]
        if a not in roots or b not in roots:
            return ("WAIT", "the roots of D %r and D %r are not both known" % (a, b))
        slope = (roots[a] - roots[b]) / (a - b)
        if MUT == "slope":
            slope = BESIDE
        src, tag = pushed[D]
        return ("NEXT", D, a, roots[a], slope, src, tag)
    return ("WAIT", "no pushed point without a root")


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
    r = plan(roots, pushed)
    chk("first leg point: NEXT 21.3125, prev root 0.836238, slope -0.35130 (t5's -0.3513)", r[0] == "NEXT" and r[1] == 21.3125 and r[2] == 21.25 and abs(r[4] + 0.351296) < 1e-9 and r[3] == 0.836238)
    roots[21.3125] = 0.8143
    pushed.update({21.375: ("A", "ta"), 21.4375: ("B", "tb")})
    r = plan(roots, pushed)
    chk("second point: slope from the two latest roots", r[0] == "NEXT" and r[1] == 21.375 and abs(r[4] - (0.8143 - 0.836238) / 0.0625) < 1e-9)
    roots[21.375] = 0.79
    r = plan(roots, pushed)
    chk("third point: its source and tag come with it", r[0] == "NEXT" and r[1] == 21.4375 and r[5:] == ("B", "tb"))
    roots[21.4375] = 0.77
    chk("nothing left: WAIT", plan(roots, pushed)[0] == "WAIT")
    chk("a missing predecessor root: WAIT", plan({21.25: 0.8}, {21.3125: ("A", "ta")})[0] == "WAIT")
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
        r = plan(roots, pushed)
        if r[0] == "NEXT":
            print("NEXT %r %r %.6f %.6f %s %s" % (r[1], r[2], r[3], r[4], r[5], r[6]))
        else:
            fin = all(os.path.exists(f + "/LEG_DONE.txt") for _, f, _, _ in PARTS)
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
        seq = [21.21875, 21.25] + sorted(pushed)
        k = seq.index(D); a, b = seq[k - 1], seq[k - 2]
        slope = (roots[a] - roots[b]) / (a - b); pred = roots[a] + slope * (D - a); pred2 = roots[a] + BESIDE * (D - a)
        new = (root - roots[a]) / (D - a)
        with open(L + "/roots87.txt", "a") as f:
            f.write("%r %.6f %.6f %.6f macm3 bracket %.3f %.3f\n" % (D, root, lo, hi, br[0], br[1]))
        print("OK macm3 #1025 kc87 leg2 ROOT D %s: %.6f (det-linear; estimator range %.6f-%.6f, not an enclosure), bracket (%.3f, %.3f). Rule (local slope %.4f): %.6f, residual %+.6f; beside (-0.33): %.6f, residual %+.6f. New local slope %.4f." % (
            dn, root, lo, hi, br[0], br[1], slope, pred, root - pred, pred2, root - pred2, new))


if __name__ == "__main__":
    main()
