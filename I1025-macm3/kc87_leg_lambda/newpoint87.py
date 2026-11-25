#!/usr/bin/env python3
"""#1025 macm3 kc87_leg_lambda: the setup of one point of dh370's k_c 87 leg (t5's standing order of 24 Nov: take every state from D 21.125 on).
usage: newpoint87.py D PREV_D PREV_ROOT [--slope=-0.28] [--rawc=COMMIT]
Finds the raw commit that added the state sol_l1kc87Ldh370_D<D:.6f>.npy (or takes --rawc), pins its blobs, writes <D>/point.env (D, TAG, RAWC, STATEFILE, STATEBLOB, RECBLOB, NP=4, GATE=10,
LAMP = a 0.005 grid over +-0.010 around m and a repeat of m, WIN, REP) and appends the README section (written before the check and scan). The prediction is t5's rule:
the previous k_c 87 root plus slope x (D - PREV_D); m is the prediction rounded to 0.005; one robust change within 0.005 of the prediction.
selftest: newpoint87.py selftest (the grid rule on planted numbers: it must fail with --mutate=round)"""
import json, math, os, subprocess, sys, time

RAWG = os.path.expanduser("~/Source/choptuik-large-d-raw-1076p")
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
TAG = os.environ.get("TAG", "l1kc87Ldh370")
SRC = os.environ.get("SRC", "I1025-dh370/kc87_leg")      # the raw folder holding the states
NP = int(os.environ.get("NP", "4")); NICE = int(os.environ.get("NICE", "10"))
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)


def dlabel(x):
    return format(x, "g") if MUT == "g" else repr(float(x))          # repr round-trips; "g" keeps 6 digits (the mutation)


def predict(pr, slope, step):
    return pr + (-0.28 if MUT == "slope" else slope) * step             # t5's rule; the mutation ignores the ordered slope


def quality_note(c):
    """t5, 25 Nov: a row with psi-constraint above 1e-2 is reduced quality (part c2 runs with --cmax 2e-2)"""
    return "" if (MUT == "flag" or c <= 1e-2) else " **REDUCED QUALITY: psi-constraint %.3e is above 1e-2 (t5, 25 Nov: part c2 runs with --cmax 2e-2; the goal there is to locate lambda_1 = 0 approximately, not to quote digits).**" % c


def fmt(x):
    r = "%.3f" % x
    return "0.000" if r == "-0.000" else r


def grid(pred):
    k = pred / 0.005
    n = math.floor(k + 0.5) if MUT != "round" else int(k)      # the prediction rounded to 0.005 (floor: right for negatives too; the mutation truncates)
    vals = [fmt((n + j) * 0.005) for j in (-2, -1, 0, 1, 2)]
    return fmt(n * 0.005), vals + [fmt(n * 0.005)]


def selftest():
    cases = [(0.8771, "0.875"), (0.8730, "0.875"), (0.8724, "0.870"), (0.8780, "0.880"), (0.8749, "0.875"), (0.8926, "0.895"), (-0.0087, "-0.010"), (-0.0024, "0.000"), (0.0024, "0.000"), (-0.0026, "-0.005"), (0.0126, "0.015")]
    ok = True
    for pred, want in cases:
        m, v = grid(pred)
        good = m == want and len(v) == 6 and v[2] == m and v[5] == m
        print("planted: prediction %.4f -> m %s, grid %s: %s" % (pred, m, " ".join(v), "PASS" if good else "FAIL (wanted m %s)" % want))
        ok = ok and good
    for pr, sl, st, want_pred, want_m in ((0.894588, -0.28, 0.0625, 0.877088, "0.875"), (0.857606, -0.32, 0.03125, 0.847606, "0.850"),
                                           (0.836238, -0.3513, 0.0625, 0.81428175, "0.815")):
        pd = predict(pr, sl, st)
        good = abs(pd - want_pred) < 1e-9 and grid(pd)[0] == want_m
        print("planted: root %.6f, slope %g, step %g -> prediction %.6f (wanted %.6f), m %s: %s" % (pr, sl, st, pd, want_pred, grid(pd)[0], "PASS" if good else "FAIL"))
        ok = ok and good
    for x in (21.125, 21.15625, 21.0625, 21.09375, 21.1875, 20.90625):
        good = float(dlabel(x)) == x
        print("planted: D %r -> label %s, float(label) == D: %s" % (x, dlabel(x), "PASS" if good else "FAIL"))
        ok = ok and good
    for c, want in ((9.9e-3, ""), (1.0e-2, ""), (1.2e-2, "REDUCED QUALITY")):
        good = (want in quality_note(c)) and (bool(want) == bool(quality_note(c)))
        print("planted: psi-constraint %.3e -> %r: %s" % (c, quality_note(c)[:40], "PASS" if good else "FAIL"))
        ok = ok and good
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def git(*a):
    return subprocess.run(["git", "-C", RAWG] + list(a), capture_output=True, text=True)


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    D = float(args[0]); PD = float(args[1]); PR = float(args[2])
    slope = float(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--slope=")), "-0.28"))
    sf = "sol_%s_D%.6f.npy" % (TAG, D)
    path = SRC + "/" + sf
    rawc = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--rawc=")), None)
    if rawc is None:
        rawc = git("log", "-1", "--format=%h", "--diff-filter=A", "origin/main", "--", path).stdout.strip()
    assert rawc and git("cat-file", "-e", rawc + ":" + path).returncode == 0, "no commit with %s" % path
    rawc = git("rev-parse", "--short=8", rawc).stdout.strip()
    sb = git("rev-parse", "--short=8", rawc + ":" + path).stdout.strip()
    rb = git("rev-parse", "--short=8", rawc + ":" + SRC + "/%s.jsonl" % TAG).stdout.strip()
    subj = git("log", "-1", "--format=%s (%ad)", "--date=iso", rawc).stdout.strip()
    rows = [json.loads(l) for l in git("cat-file", "blob", rawc + ":" + SRC + "/%s.jsonl" % TAG).stdout.splitlines() if l.strip()]
    row = [r for r in rows if r["D"] == D][-1]
    pred = predict(PR, slope, D - PD)
    m, vals = grid(pred)
    s2 = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--slope2=")), None)
    pred2 = (PR + float(s2) * (D - PD)) if s2 is not None else None
    m2 = grid(pred2)[0] if pred2 is not None else None
    beside = ("\n**Scored beside it (t5: keep scoring the -0.33 rule):** %s %+g x %s = **%.4f**, centre %s (%s grid as the primary's %s); one robust change within 0.005 of it is scored separately." % (
        format(PR, ".6f"), float(s2), "%.10g" % (D - PD), pred2, m2, "the same" if m2 == m else "another", m)) if pred2 is not None else ""
    s3 = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--slope3=")), None)
    pred3 = (PR + float(s3) * (D - PD)) if s3 is not None else None
    m3 = grid(pred3)[0] if pred3 is not None else None
    beside3 = ("\n**Interpolation (t5, for the points between):** the primary prediction above is the line through the bracketing roots (the root below at D %s and the nearest root above), so its residual measures the curvature. **Scored beside it:** the below-only extrapolation, %s %+g x %s = **%.4f**, centre %s (%s grid as the primary's %s)." % (
        dlabel(PD), format(PR, ".6f"), float(s3), "%.10g" % (D - PD), pred3, m3, "the same" if m3 == m else "another", m)) if pred3 is not None else ""
    dn = dlabel(D) + os.environ.get("DNSUFFIX", "")      # a suffix for a control scan of the same D (t5: the h 0.03125 control, folder 21.375_ctl)
    assign = "; ".join("process %d: %s" % (q, " then ".join(("the repeat " if i == 5 else "") + vals[i] for i in range(q, 6, NP))) for q in range(NP))
    wallp = "10 to 40 min about 70%" if NP >= 4 else "25 to 90 min about 65% (2 processes beside the leap's 4 threads)"
    os.makedirs("%s/%s" % (L, dn), exist_ok=True)
    env = """D=%s
TAG=%s
RAWC=%s
STATEFILE=%s
STATEBLOB=%s
RECBLOB=%s
# t5's rule (hc 24 Nov): %s + (%g) x (%s - %s) = %.4f; m = %s; a 0.005 grid over +-0.010 around m and a repeat of m: 6 evaluations on %d processes at nice %d, round-robin (%s)
NP=%d; GATE=10; NICE=%d
SRC=%s
LAMP=(%s)
WIN="%s %s"; REP=%s
""" % (dlabel(D), TAG, rawc, sf, sb, rb, PR, slope, dlabel(D), dlabel(PD), pred, m, NP, NICE, assign,
       NP, NICE, SRC, " ".join('"%s"' % v for v in vals), vals[0], vals[4], m)
    open("%s/%s/point.env" % (L, dn), "w").write(env)
    now = time.strftime("%F %H:%M:%S", time.gmtime())
    sec = """
## D %s (written before its check and scan, %s UTC)

**Inputs** (`%s/pins.txt`): the commit %s (%s): state `%s/%s` blob **%s**, record `%s.jsonl` blob **%s** (%d rows; the check and the scan pick the row of D %s: |F| %.16g, %d steps, Delta %.16g, h %g, k_c %s, psi-constraint %.3e).%s
**Prediction (t5's rule, hcs of 24 Nov):** the previous k_c 87 root plus slope %g per unit D times the D step (slope as ordered by t5: -0.28 up to D 21.1875, -0.32 for D 21.21875 and 21.25, and for the leg2 points from D 21.3125 on the latest measured local slope, -0.3513 at D 21.3125): %s %+g x %s = **%.4f**; one robust change within 0.005 of it.
%s%s
**Grid:** m = %.4f rounded to 0.005 = %s; lambda %s and a repeat of %s: 6 evaluations on %d processes of 1 thread at nice %d, round-robin (%s); window read `read_lower.py scan %s %s` (the interval prediction +-0.005, %.4f to %.4f, lies inside it).
**Predictions (mine, before the run):** as D 21.0625's: the source check accepts with all controls firing and the k_c 79 check refusing about 90%%; all six noise-robust about 75%%; exactly one robust change in the window about 85%%; its det-linear estimate within 0.005 of the prediction about 75%%, within 0.002 about 40%%; edge signs unequal about 85%%; the repeat of %s bit-identical about 90%%; the float64 sign differs from the hybrid at one or more points about 55%%; scan wall %s; peak RSS per process below 4.5 GB about 85%%.
## Log
""" % (dn, now, dn, rawc, subj, SRC, sf, sb, TAG, rb, len(rows), dlabel(D), row["F"], row["steps"], row["Delta"], row.get("h", 0.03125), row["kc"], row["constraint"], quality_note(row["constraint"]),
       slope, format(PR, ".6f"), slope, "%.10g" % (D - PD), pred, beside, beside3, pred, m, ", ".join(vals[:5]), m, NP, NICE, assign, vals[0], vals[4], pred - 0.005, pred + 0.005, m, wallp)
    open(L + "/README.md", "a").write(sec)
    print("D %s: commit %s, state %s, record %s, prediction %.4f, m %s, grid %s" % (dn, rawc, sb, rb, pred, m, " ".join(vals)))
