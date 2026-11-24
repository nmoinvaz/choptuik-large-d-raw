#!/usr/bin/env python3
"""#1025 macm3 kc87_leg_lambda: the setup of one point of dh370's k_c 87 leg (t5's standing order of 24 Nov: take every state from D 21.125 on).
usage: newpoint87.py D PREV_D PREV_ROOT [--slope=-0.28] [--rawc=COMMIT]
Finds the raw commit that added the state sol_l1kc87Ldh370_D<D:.6f>.npy (or takes --rawc), pins its blobs, writes <D>/point.env (D, TAG, RAWC, STATEFILE, STATEBLOB, RECBLOB, NP=4, GATE=10,
LAMP = a 0.005 grid over +-0.010 around m and a repeat of m, WIN, REP) and appends the README section (written before the check and scan). The prediction is t5's rule:
the previous k_c 87 root plus slope x (D - PREV_D); m is the prediction rounded to 0.005; one robust change within 0.005 of the prediction.
selftest: newpoint87.py selftest (the grid rule on planted numbers: it must fail with --mutate=round)"""
import json, os, subprocess, sys, time

RAWG = os.path.expanduser("~/Source/choptuik-large-d-raw-1076p")
L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
TAG = "l1kc87Ldh370"
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)


def grid(pred):
    k = pred / 0.005
    m = (int(k + 0.5) if MUT != "round" else int(k)) * 0.005          # the prediction rounded to 0.005 (the mutation truncates)
    vals = ["%.3f" % (m + 0.005 * j) for j in (-2, -1, 0, 1, 2)]
    return "%.3f" % m, vals + ["%.3f" % m]


def selftest():
    cases = [(0.8771, "0.875"), (0.8730, "0.875"), (0.8724, "0.870"), (0.8780, "0.880"), (0.8749, "0.875"), (0.8926, "0.895")]
    ok = True
    for pred, want in cases:
        m, v = grid(pred)
        good = m == want and len(v) == 6 and v[2] == m and v[5] == m
        print("planted: prediction %.4f -> m %s, grid %s: %s" % (pred, m, " ".join(v), "PASS" if good else "FAIL (wanted m %s)" % want))
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
    path = "I1025-dh370/kc87_leg/" + sf
    rawc = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--rawc=")), None)
    if rawc is None:
        rawc = git("log", "-1", "--format=%h", "--diff-filter=A", "origin/main", "--", path).stdout.strip()
    assert rawc and git("cat-file", "-e", rawc + ":" + path).returncode == 0, "no commit with %s" % path
    rawc = git("rev-parse", "--short=8", rawc).stdout.strip()
    sb = git("rev-parse", "--short=8", rawc + ":" + path).stdout.strip()
    rb = git("rev-parse", "--short=8", rawc + ":I1025-dh370/kc87_leg/%s.jsonl" % TAG).stdout.strip()
    subj = git("log", "-1", "--format=%s (%ad)", "--date=iso", rawc).stdout.strip()
    rows = [json.loads(l) for l in git("cat-file", "blob", rawc + ":I1025-dh370/kc87_leg/%s.jsonl" % TAG).stdout.splitlines() if l.strip()]
    row = [r for r in rows if r["D"] == D][-1]
    pred = PR + slope * (D - PD)
    m, vals = grid(pred)
    dn = format(D, "g")
    os.makedirs("%s/%s" % (L, dn), exist_ok=True)
    env = """D=%s
TAG=%s
RAWC=%s
STATEFILE=%s
STATEBLOB=%s
RECBLOB=%s
# t5's rule (hc 24 Nov): %s + (%g) x (%s - %s) = %.4f; m = %s; a 0.005 grid over +-0.010 around m and a repeat of m: 6 evaluations on 4 processes in two rounds (process 0: %s then %s, process 1: %s then the repeat %s, process 2: the first %s, process 3: %s)
NP=4; GATE=10
LAMP=(%s)
WIN="%s %s"; REP=%s
""" % (format(D, "g"), TAG, rawc, sf, sb, rb, PR, slope, format(D, "g"), format(PD, "g"), pred, m, vals[0], vals[4], vals[1], vals[5], vals[2], vals[3],
       " ".join('"%s"' % v for v in vals), vals[0], vals[4], m)
    open("%s/%s/point.env" % (L, dn), "w").write(env)
    now = time.strftime("%F %H:%M:%S", time.gmtime())
    sec = """
## D %s (written before its check and scan, %s UTC)

**Inputs** (`%s/pins.txt`): dh370's commit %s (%s): state `I1025-dh370/kc87_leg/%s` blob **%s**, record `%s.jsonl` blob **%s** (%d rows; the check and the scan pick the row of D %s: |F| %.16g, %d steps, Delta %.16g, h %g, k_c %s).
**Prediction (t5's rule, hc 24 Nov):** the previous k_c 87 root plus slope -0.28 per unit D times the D step: %s %+g x %s = **%.4f**; one robust change within 0.005 of it.
**Grid:** m = %.4f rounded to 0.005 = %s; lambda %s and a repeat of %s: 6 evaluations on 4 processes of 1 thread in two rounds (process 0 runs %s then %s, process 1 runs %s then the repeat of %s, process 2 the first %s, process 3 %s); window read `read_lower.py scan %s %s` (the interval prediction +-0.005, %.4f to %.4f, lies inside it).
**Predictions (mine, before the run):** as D 21.0625's: the source check accepts with all controls firing and the k_c 79 check refusing about 90%%; all six noise-robust about 75%%; exactly one robust change in the window about 85%%; its det-linear estimate within 0.005 of the prediction about 75%%, within 0.002 about 40%%; edge signs unequal about 85%%; the repeat of %s bit-identical about 90%%; the float64 sign differs from the hybrid at one or more points about 55%%; scan wall 10 to 40 min about 70%%; peak RSS per process below 4.5 GB about 85%%.
## Log
""" % (dn, now, dn, rawc, subj, sf, sb, TAG, rb, len(rows), format(D, "g"), row["F"], row["steps"], row["Delta"], row.get("h", 0.03125), row["kc"],
       format(PR, ".6f"), slope, "%g" % (D - PD), pred, pred, m, ", ".join(vals[:5]), m, vals[0], vals[4], vals[1], m, m, vals[3], vals[0], vals[4], pred - 0.005, pred + 0.005, m)
    open(L + "/README.md", "a").write(sec)
    print("D %s: commit %s, state %s, record %s, prediction %.4f, m %s, grid %s" % (dn, rawc, sb, rb, pred, m, " ".join(vals)))
