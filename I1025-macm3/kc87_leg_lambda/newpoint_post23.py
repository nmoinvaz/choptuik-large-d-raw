#!/usr/bin/env python3
"""#1025 macm3 kc87_leg_lambda: the setup of one scan of the k_c 87 leg's late points, in t5's order of 25 Nov 12:0x UTC (after part c2's guard stop at D 23.0):
"(b). Keep the leg's end at D 23.0 ... release the chain hold. Scan in this order: D 23.0 and D 22.9375 first (lambda -0.10 to 0.30 by 0.02 plus a repeat ...), then part c's points from
D 22.875 down, then D 22.5 and 22.375. Rows above the 1e-2 constraint carry REDUCED QUALITY in every table. Register predictions per scan as before."
usage: newpoint_post23.py D --window=LO:HI:STEP --rep=X      the ordered grid (D 23.0, 22.9375)
       newpoint_post23.py D --auto                            the other points: window +-0.03 by 0.01 around m = the primary prediction rounded to 0.01, and a repeat of m
       newpoint_post23.py selftest [--mutate=rule|round|rep]
Writes <D>/point.env and appends the README section (predictions registered before the check and scan). The primary prediction (roots as in roots87.txt, later line of a D wins):
 two roots above D (c1 < c2): the line through them, extended down to D; one root above: the line through it and the largest root below (t5's interpolation rule for points between);
 none above: the line through the two largest roots below (the chain's rule). Scored beside it: the interpolation (when two roots lie above) and the below-only line."""
import json, math, os, subprocess, sys, time

RAWG = os.path.expanduser("~/Source/choptuik-large-d-raw-1076p")
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
L2 = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2")
PARTS = (("c2", L2 + "/c2", "I1025-macm3/kc87_leg2/c2", "l1kc87Lmacm3c2"), ("c", L2 + "/c", "I1025-macm3/kc87_leg2/c", "l1kc87Lmacm3c"),
         ("b2", L2 + "/b2", "I1025-macm3/kc87_leg2/b2", "l1kc87Lmacm3b2"), ("b", L2 + "/b", "I1025-macm3/kc87_leg2/b", "l1kc87Lmacm3b"), ("a", L2, "I1025-macm3/kc87_leg2", "l1kc87Lmacm3"))
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
NP = 4; NICE = 15


def fmt(x):
    r = "%.3f" % x
    return "0.000" if r == "-0.000" else r


def read_roots(path):
    r = {}
    for l in open(path):
        f = l.split()
        if len(f) >= 2 and not l.startswith("#"):
            r[float(f[0])] = float(f[1])
    return r


def line(r1, r2):
    """slope of the line through two (D, root) pairs"""
    return (r2[1] - r1[1]) / (r2[0] - r1[0])


def predictions(roots, D):
    """-> (primary, rule text, [(beside text, value)...])"""
    below = sorted(x for x in roots if x < D); above = sorted(x for x in roots if x > D)
    if MUT == "rule":
        above = []                                            # the mutation ignores the roots above
    a, b = below[-1], below[-2]
    pb = roots[a] + line((b, roots[b]), (a, roots[a])) * (D - a)
    txt_b = "below-only line through the roots at D %r and D %r (the chain's rule): %.4f" % (b, a, pb)
    if len(above) >= 2:
        c1, c2 = above[0], above[1]
        sl = line((c1, roots[c1]), (c2, roots[c2])); pr = roots[c1] + sl * (D - c1)
        pi = roots[a] + line((a, roots[a]), (c1, roots[c1])) * (D - a)
        return pr, "the line through the two nearest roots above, D %r (%.6f) and D %r (%.6f), slope %.4f per unit D, extended down to D %r" % (c1, roots[c1], c2, roots[c2], sl, D), [("interpolation between the roots at D %r and D %r (t5's rule for the points between): %.4f" % (a, c1, pi), pi), (txt_b, pb)]
    if len(above) == 1:
        c1 = above[0]; pi = roots[a] + line((a, roots[a]), (c1, roots[c1])) * (D - a)
        return pi, "the line through the root below at D %r (%.6f) and the root above at D %r (%.6f) (t5's interpolation rule), slope %.4f" % (a, roots[a], c1, roots[c1], line((a, roots[a]), (c1, roots[c1]))), [(txt_b, pb)]
    return pb, "the line through the two largest roots below, D %r (%.6f) and D %r (%.6f), slope %.4f per unit D (the chain's rule)" % (b, roots[b], a, roots[a], line((b, roots[b]), (a, roots[a]))), []


def round01(x):
    k = x / 0.01
    n = math.floor(k + 0.5) if MUT != "round" else int(k)
    return fmt(n * 0.01)


def auto_grid(pred):
    m = round01(pred); n = round(float(m) / 0.01)
    vals = [fmt((n + j) * 0.01) for j in (-3, -2, -1, 0, 1, 2, 3)]
    return m, [m, m] + [v for v in vals if v != m]             # m twice first (index 0, 1: two processes), then the others


def ordered_grid(lo, hi, step, rep):
    n = int(round((hi - lo) / step)); vals = [fmt(lo + i * step) for i in range(n + 1)]
    assert rep in vals
    return rep, [rep, rep] + [v for v in vals if v != rep]     # rep twice first (index 0, 1: two processes), then the others


def check_procs(lamp, rep):
    idx = [i for i, v in enumerate(lamp) if v == rep]
    return len(idx) == 2 and idx[0] % NP != idx[1] % NP


def quality_note(c):
    return "" if c <= 1e-2 else " **REDUCED QUALITY: psi-constraint %.3e is above 1e-2** (t5, 25 Nov: part c2 ran with --cmax 2e-2; the aim there is the approximate place of lambda_1 = 0, not digits)." % c


def git(*a):
    return subprocess.run(["git", "-C", RAWG] + list(a), capture_output=True, text=True)


def selftest():
    ok = True
    def chk(name, cond):
        nonlocal ok
        print("planted:", name, "PASS" if cond else "FAIL"); ok = ok and cond
    roots = {22.1875: 0.473467, 22.25: 0.442516}
    p, _, bs = predictions(roots, 23.0)
    chk("D 23.0, no root above: the chain's line, 0.442516 + (-0.49522) x 0.75 = 0.0711", abs(p - (0.442516 + (0.442516 - 0.473467) / 0.0625 * 0.75)) < 1e-9 and abs(p - 0.0711) < 5e-4 and bs == [])
    roots[23.0] = 0.07
    p, _, bs = predictions(roots, 22.9375)
    chk("D 22.9375, one root above: interpolation between 22.25 and 23.0 (0.442516 -> 0.07)", abs(p - (0.442516 + (0.07 - 0.442516) / 0.75 * 0.6875)) < 1e-9 and len(bs) == 1)
    roots[22.9375] = 0.10
    p, _, bs = predictions(roots, 22.875)
    chk("D 22.875, two roots above: the line through 22.9375 (0.10) and 23.0 (0.07) extended: 0.10 + (-0.48) x (-0.0625) = 0.13", abs(p - 0.13) < 1e-9 and len(bs) == 2)
    chk("the grid rule rounds to 0.01 (0.1299 -> 0.13, -0.004 -> 0.00, -0.006 -> -0.01, 0.1251 -> 0.13)", [round01(x) for x in (0.1299, -0.004, -0.006, 0.1251)] == ["0.13", "0.000", "-0.010", "0.130"] or [round01(x) for x in (0.1299, -0.004, -0.006, 0.1251)] == ["0.130", "0.000", "-0.010", "0.130"])
    m, lamp = auto_grid(0.1299)
    chk("auto grid: m 0.130, seven values 0.10 to 0.16 and the repeat first, on two processes", m == "0.130" and lamp == ["0.130", "0.130", "0.100", "0.110", "0.120", "0.140", "0.150", "0.160"] and check_procs(lamp, m))
    m, lamp = ordered_grid(-0.10, 0.30, 0.02, "0.100")
    chk("ordered grid: 21 values -0.10 to 0.30 and the repeat of 0.100 first, on two processes", len(lamp) == 22 and lamp[2] == "-0.100" and lamp[-1] == "0.300" and lamp[0] == lamp[1] == "0.100" and check_procs(lamp, "0.100"))
    chk("a negative zero prints 0.000", fmt(-0.0004) == "0.000")
    chk("quality flag: 1.021e-2 flagged, 1.0e-2 and 9.9e-3 not", "REDUCED" in quality_note(1.021e-2) and quality_note(1.0e-2) == "" and quality_note(9.9e-3) == "")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    D = float(sys.argv[1]); dn = repr(D)
    roots = read_roots(L + "/roots87.txt")
    part = None
    for name, folder, src, tag in PARTS:
        p = folder + "/pushed_points.txt"
        if os.path.exists(p) and any(abs(float(x) - D) < 1e-9 for x in open(p).read().split()):
            part = (name, src, tag); break
    assert part, "D %r is in no part's pushed_points.txt" % D
    pname, SRC, TAG = part
    sf = "sol_%s_D%.6f.npy" % (TAG, D); path = SRC + "/" + sf
    rawc = git("log", "-1", "--format=%h", "--diff-filter=A", "origin/main", "--", path).stdout.strip()
    assert rawc and git("cat-file", "-e", rawc + ":" + path).returncode == 0, "no commit with %s" % path
    rawc = git("rev-parse", "--short=8", rawc).stdout.strip()
    sb = git("rev-parse", "--short=8", rawc + ":" + path).stdout.strip()
    rb = git("rev-parse", "--short=8", rawc + ":" + SRC + "/%s.jsonl" % TAG).stdout.strip()
    subj = git("log", "-1", "--format=%s (%ad)", "--date=iso", rawc).stdout.strip()
    rows = [json.loads(l) for l in git("cat-file", "blob", rawc + ":" + SRC + "/%s.jsonl" % TAG).stdout.splitlines() if l.strip()]
    row = [r for r in rows if r["D"] == D][-1]
    pred, rule, besides = predictions(roots, D)
    if "--window" in " ".join(sys.argv):
        lo, hi, st = [float(x) for x in next(a.split("=", 1)[1] for a in sys.argv if a.startswith("--window=")).split(":")]
        rep = fmt(float(next(a.split("=", 1)[1] for a in sys.argv if a.startswith("--rep="))))
        m, lamp = ordered_grid(lo, hi, st, rep); how = "the order's grid: lambda %.2f to %.2f by %.2f (%d values) and a repeat of %s" % (lo, hi, st, len(lamp) - 1, m)
    else:
        m, lamp = auto_grid(pred); how = "my grid (the order gave none for this point): m = the primary prediction rounded to 0.01 = %s, lambda %s to %s by 0.01 (7 values) and a repeat of %s" % (m, fmt(min(float(v) for v in lamp)), fmt(max(float(v) for v in lamp)), m)
    assert check_procs(lamp, m), "the repeat is not on another process"
    fv = sorted(set(float(v) for v in lamp)); win = (fmt(fv[0]), fmt(fv[-1]))
    assign = "; ".join("process %d: %s" % (q, " then ".join(("the repeat " if (i == 1) else "") + lamp[i] for i in range(q, len(lamp), NP))) for q in range(NP))
    nev = len(lamp)
    os.makedirs("%s/%s" % (L, dn), exist_ok=True)
    env = """D=%s
TAG=%s
RAWC=%s
STATEFILE=%s
STATEBLOB=%s
RECBLOB=%s
# t5's order (hc 25 Nov ~12:10 UTC, after part c2's guard stop at D 23.0): %s; %d evaluations on %d processes at nice %d, round-robin (%s)
NP=%d; GATE=10; NICE=%d
SRC=%s
LAMP=(%s)
WIN="%s %s"; REP=%s
""" % (dn, TAG, rawc, sf, sb, rb, how, nev, NP, NICE, assign, NP, NICE, SRC, " ".join('"%s"' % v for v in lamp), win[0], win[1], m)
    open("%s/%s/point.env" % (L, dn), "w").write(env)
    nowt = time.strftime("%F %H:%M:%S", time.gmtime())
    bes = "".join("\n**Scored beside it:** %s." % t for t, v in besides)
    above = sorted(x for x in roots if x > D)
    sec = """
## D %s (part %s; written before its check and scan, %s UTC)

**Order** (t5, hc 25 Nov ~12:10 UTC, quoted): "(b). Keep the leg's end at D 23.0 (the guard's stop stands; the tangent turning onto the weakest regular mode as F nears 0 is itself a result to record) and release the chain hold. Scan in this order: D 23.0 and D 22.9375 first (lambda -0.10 to 0.30 by 0.02 plus a repeat, F's extrapolated zero is near D 23.09, so F should sit near 0.05-0.08 there), then part c's points from D 22.875 down, then D 22.5 and 22.375. Rows above the 1e-2 constraint carry REDUCED QUALITY in every table. Register predictions per scan as before."
**Inputs** (`%s/pins.txt`): the commit %s (%s): state `%s/%s` blob **%s**, record `%s.jsonl` blob **%s** (%d rows; the check and the scan pick the row of D %s: |F| %.16g, %d steps, Delta %.16g, h %g, k_c %s, psi-constraint %.3e).%s
**Prediction of F (lambda_1 of the leg), primary:** %s: **%.4f**. F is the flat branch; S (the steep one) lies far below -0.1 here (win2: S at D 22.28125 is -0.1976, falling), so one root of F is expected in the window.%s
**Grid:** %s; window read `read_lower.py scan %s %s`; %d evaluations on %d processes of 1 thread at nice %d, round-robin (%s).
**Predictions (mine, before the run):** the source check accepts with all controls firing and the k_c 79 check refusing about 90%%; the repeat of %s bit-identical about 90%%; all %d noise-robust about 80%%; exactly one robust change in the window about 80%% (none about 12%%: F outside the window; two or more about 8%%); its orientation '- to +' about 90%% (given one); its det-linear estimate within 0.01 of the primary prediction about 50%%, within 0.03 about 80%%; F positive at this D about %d%%; no ln|det| minimum without a sign change about 85%%; the float64 sign equals the hybrid at every evaluation about 60%%; scan wall %s about 70%%; no memory alert about 90%%.
## Log
""" % (dn, pname, nowt, dn, rawc, subj, SRC, sf, sb, TAG, rb, len(rows), dn, row["F"], row["steps"], row["Delta"], row.get("h", 0.0625), row["kc"], row["constraint"], quality_note(row["constraint"]),
       rule, pred, bes, how, win[0], win[1], nev, NP, NICE, assign, m, nev, 85 if D < 23.0 else 80, "22 to 110 min" if nev > 12 else "15 to 50 min")
    open(L + "/README.md", "a").write(sec)
    print("D %s: part %s, commit %s, state %s, record %s, primary prediction %.4f, m %s, grid %s" % (dn, pname, rawc, sb, rb, pred, m, " ".join(lamp)))


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    main()
