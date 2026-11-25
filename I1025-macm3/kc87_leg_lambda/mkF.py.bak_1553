#!/usr/bin/env python3
"""mkF.py: the scans of t5's order of 25 Nov (hc after 15:48 UTC, quoted): "(a) yes and (b) yes, now, before anything else. (c) In roots87.txt keep one line per root with a branch label: F (the upper, flat branch =
lambda_1) and L (the lower root of D 22.8125-22.875) ... Let the running D 22.75 scan finish, then scan D 22.75 and below on -0.10 to 0.50 by 0.02 (both roots), D 22.75 first, then 22.5 (b2, unscanned at k_c 87),
then the rest. Register for each: F near its line (0.4425 at 22.25 to ~0.171 at 22.875), L unknown."
  mkF.py setup KIND     KIND a (D 22.875: the upper root F in 0.17-0.19), b (D 22.8125: F in 0.24-0.40) or a plain D (both roots on -0.10 to 0.50 by 0.02): writes the folder's point.env and appends the README
                        section with the registration (before any run); prints the folder name
  mkF.py read KIND      merged reading of the earlier scans of that D and this one (ext23.read_merged) -> FOLDER/read_lower_merged.txt; prints its path
  mkF.py selftest [--mutate=grid]
"""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ext23

L = ext23.L
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
ORDER = ("t5's order (hc 25 Nov, after 15:48 UTC, quoted): \"(a) yes and (b) yes, now, before anything else. (c) In roots87.txt keep one line per root with a branch label: F (the upper, flat branch = lambda_1) and L (the lower root of D 22.8125-22.875); "
         "the chain's lambda_1 line at D 22.8125 and 22.875 becomes F's once (a) and (b) are read, with L's root kept beside it, annotated. Let the running D 22.75 scan finish, then scan D 22.75 and below on -0.10 to 0.50 by 0.02 (both roots), "
         "D 22.75 first, then 22.5 (b2, unscanned at k_c 87), then the rest. Register for each: F near its line (0.4425 at 22.25 to ~0.171 at 22.875), L unknown.\"")


def now():
    return subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M:%S"]).decode().strip()


def spec(kind):
    """-> dict(D, folder, lamp, win, rep, dirs (earlier scans of the D), mwin (merged window))"""
    if kind == "a":
        return dict(D=22.875, folder="22.875_F", lamp=[0.18, 0.18, 0.17, 0.19], win=(0.17, 0.19), rep=0.18, dirs=["22.875/scan", "22.875_wide/scan"], mwin=(-0.10, 0.30))
    if kind == "b":
        vals = [round(0.24 + 0.02 * i, 2) for i in range(9)]                 # 0.24 .. 0.40
        rep = 0.32
        lamp = [rep, rep] + [v for v in vals if v != rep]
        return dict(D=22.8125, folder="22.8125_F", lamp=lamp, win=(0.24, 0.40), rep=rep, dirs=["22.8125/scan", "22.8125_ext/scan"], mwin=(0.11, 0.40))
    D = float(kind)
    n = 31 if MUT != "grid" else 30
    vals = [round(-0.10 + 0.02 * i, 2) for i in range(n)]                    # -0.10 .. 0.50 by 0.02
    rep = 0.20
    lamp = [rep, rep] + [v for v in vals if v != rep]
    dirs = ["%r/scan" % D] if os.path.isdir("%s/%r/scan" % (L, D)) else []
    return dict(D=D, folder="%r_both" % D, lamp=lamp, win=(-0.10, 0.50), rep=rep, dirs=dirs, mwin=(-0.10, 0.50))


def froots():
    """the lambda_1 (F) roots in roots87.txt: {D: root} from the lines the chain reads, and the L comment lines {D: root}"""
    f, l = {}, {}
    for ln in open(L + "/roots87.txt"):
        w = ln.split()
        if ln.startswith("#L ") and len(w) >= 3:
            l[float(w[1])] = float(w[2])
        elif w and not ln.startswith("#"):
            f[float(w[0])] = float(w[1])
    return f, l


def fmt(v):
    return "%.3f" % v


def register(kind, sp):
    D = sp["D"]; dn = repr(D)
    f, l = froots()
    lo, hi = sp["win"]
    nev = len(sp["lamp"])
    rounds = -(-nev // 4)
    assign = "; ".join("process %d: %s" % (q, ", ".join(fmt(sp["lamp"][i]) for i in range(q, nev, 4))) for q in range(4))
    head = "\n## D %s %s scan (written before its check and scan, %s UTC)\n\n**Order** %s\n" % (dn, "F (upper root)" if kind in ("a", "b") else "both roots", now(), ORDER)
    grid = ("**Grid:** lambda %s, the middle repeat %s first (twice, on processes 0 and 1); %d evaluations on 4 processes of 1 thread at nice 15 (%d rounds, about %d min; %s); window read on this scan alone `read_lower.py scan %s %s` and merged with %s "
            "(`ext23.read_merged`; the earlier readings of D %s are not replaced) on lambda %s to %s.\n") % (
        "%s to %s%s" % (fmt(lo), fmt(hi), " by 0.01" if kind == "a" else " by 0.02"), fmt(sp["rep"]), nev, rounds, rounds * 10, assign, fmt(lo), fmt(hi),
        ("the scans " + ", ".join("`%s`" % d for d in sp["dirs"])) if sp["dirs"] else "no earlier scan", dn, fmt(sp["mwin"][0]), fmt(sp["mwin"][1]))
    common = ("the source check accepts with all controls firing and the k_c 79 check refusing about 90%%; the repeat of %s bit-identical about 90%%; all %d noise-robust about %d%%; no ln|det| minimum without a sign change about 85%%; "
              "the float64 sign equals the hybrid at every evaluation about 55%%; scan wall %d to %d min about 70%%; no memory alert about 90%%.") % (fmt(sp["rep"]), nev, 80 if nev <= 10 else 70, rounds * 8, rounds * 14)
    if kind == "a":
        txt = (head +
               "**Why:** the merged reading of D 22.875 (`22.875_wide/read_lower_merged.txt`) has two robust changes: (0.120, 0.130) '- to +' (0.127834, L) and (0.160, 0.200) '+ to -' (det-linear 0.171403, range [0.161208, 0.171403], F); the grid has no point between 0.16 and 0.20.\n"
               "**Prediction (F, the upper root):** det-linear estimate of the merged reading **0.1714** (its estimate from 0.16 and 0.20); the chord of F between D 22.25 (0.442516) and D 22.9375 (0.056199) gives 0.0913 at D 22.875 and F, being concave (the roots fall faster toward D 23), lies at or above it; **0.1714** is my primary value. I expect F between the grid values 0.17 and 0.19 about 75%, between 0.16 and 0.17 about 12%, between 0.19 and 0.20 about 13%.\n" + grid +
               "**Predictions (mine, before the run):** " + common + " The merged reading has exactly two robust changes (L at 0.120-0.130 unchanged, F) about 85%; F's bracket narrows to a 0.01 interval inside (0.160, 0.200) about 85%; F's det-linear estimate within 0.01 of 0.1714 about 60%; the orientation of F '+ to -' about 95%.\n## Log\n")
    elif kind == "b":
        txt = (head +
               "**Why:** the merged reading of D 22.8125 (first scan 0.17-0.23 and the extension 0.11-0.16) has one change, (0.160, 0.170) '- to +' (0.166991), and '+' at every value from 0.17 to 0.23, so by the counting of the signs the upper root F lies above 0.230 (the pair at D 22.875 is L 0.128 and F about 0.171, at D 22.9375 F is 0.056).\n"
               "**Prediction (F, the upper root):** between the chord of F from D 22.25 (0.442516) to D 22.875 (about 0.171), which gives about 0.199 at D 22.8125, and the line through D 22.875 (0.171) and D 22.9375 (0.056) extended up by one step, slope -1.84, which gives 0.286. The signs already say F is above 0.230, so **0.29** is my primary value; I expect F in (0.24, 0.40) about 85% (one more change '+ to -'), above 0.40 about 12%, in (0.23, 0.24) about 3%.\n" + grid +
               "**Predictions (mine, before the run):** " + common + " The merged reading has exactly two robust changes (L at 0.160-0.170 unchanged, F) about 80%; F's det-linear estimate within 0.03 of 0.29 about 55%; the orientation of F '+ to -' about 95%.\n## Log\n")
    else:
        f_pts = sorted(x for x in f if x < D) + sorted(x for x in f if x > D)
        a_ = max([x for x in f if x < D] or [None], key=lambda x: -1 if x is None else x)
        c_ = min([x for x in f if x > D] or [None], key=lambda x: 9e9 if x is None else x)
        chord = f[a_] + (f[c_] - f[a_]) * (D - a_) / (c_ - a_) if a_ is not None and c_ is not None else None
        lpts = sorted(l)
        lline = (l[lpts[0]] + (l[lpts[-1]] - l[lpts[0]]) / (lpts[-1] - lpts[0]) * (D - lpts[0])) if len(lpts) >= 2 else None
        pf = ("F near its line: the chord between the F roots at D %r (%.6f) and D %r (%.6f) gives **%.4f** at D %r (the curve is concave, so F lies at or above the chord)." % (a_, f[a_], c_, f[c_], chord, D)) if chord is not None else "F: no F roots on both sides (no line)."
        pl = ("**L unknown:** the lower roots L at D %s (%s) give a line that reads %.4f at D %r; it is a guess, not a prediction I trust." % (" and ".join(repr(x) for x in lpts), ", ".join("%.6f" % l[x] for x in lpts), lline, D)) if lline is not None else "**L unknown.**"
        txt = (head +
               "**Why:** the two roots of the pair, L (lower, '- to +') and F (upper, '+ to -', lambda_1), are in the window together at D 22.875 (0.128 and about 0.171); the narrow windows built from the lower-root line saw only L, so the points below D 22.8125 are scanned on -0.10 to 0.50 by 0.02.\n"
               "**Prediction:** " + pf + " " + pl + " If L and F approach each other as D falls (L is 0.043 below F at D 22.875), a gap below the 0.02 grid shows as no change or one change.\n" + grid +
               "**Predictions (mine, before the run):** " + common.replace("all %d noise-robust about %d%%" % (nev, 70), "all %d noise-robust about 70%%" % nev) +
               " The merged reading has exactly two robust changes ('- to +' then '+ to -') about 50%, one about 15% (the other outside -0.10 to 0.50 or the pair unresolved), none about 20% (no real root in the window: the pair has merged or left it), three or more about 15%; "
               "given two, F within 0.04 of the chord about 60% and above the chord about 65%; L at or above 0.10 about 70%.\n## Log\n")
    return txt


def setup(kind):
    sp = spec(kind)
    D = sp["D"]; dn = repr(D)
    fe = "%s/%s" % (L, sp["folder"])
    os.makedirs(fe, exist_ok=True)
    env = ext23.read_first_env("%s/%s/point.env" % (L, dn))
    with open(fe + "/point.env", "w") as fh:
        fh.write("\n".join(env) + "\n# %s: %s\n" % (sp["folder"], ORDER))
        fh.write("LAMP=(%s)\n" % " ".join('"%.3f"' % x for x in sp["lamp"]))
        fh.write('WIN="%.3f %.3f"; REP=%.3f\n' % (sp["win"][0], sp["win"][1], sp["rep"]))
    open(L + "/README.md", "a").write(register(kind, sp))
    print(sp["folder"])


def read(kind):
    sp = spec(kind)
    dn = repr(sp["D"]); fe = "%s/%s" % (L, sp["folder"])
    dirs = ["%s/%s" % (L, d) for d in sp["dirs"]] + [fe + "/scan"]
    t = ext23.read_merged(dirs, fe + "/merged", dn, sp["mwin"][0], sp["mwin"][1])
    open(fe + "/read_lower_merged.txt", "w").write(t)
    print(fe + "/read_lower_merged.txt")


def selftest():
    ok = True
    def chk(name, cond):
        nonlocal ok
        print("planted:", name, "PASS" if cond else "FAIL"); ok = ok and cond
    a, b, c = spec("a"), spec("b"), spec("22.75")
    chk("a: 0.17, 0.18, 0.19 and the repeat 0.18 on processes 0 and 1: 4 evaluations", a["lamp"] == [0.18, 0.18, 0.17, 0.19] and a["rep"] == 0.18)
    chk("b: 0.24 to 0.40 by 0.02 (9 values) and the repeat 0.32 first: 10 evaluations", sorted(set(b["lamp"])) == [0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36, 0.38, 0.4] and len(b["lamp"]) == 10 and b["lamp"][:2] == [0.32, 0.32])
    chk("both: -0.10 to 0.50 by 0.02 (31 values) and the repeat 0.20 first: 32 evaluations", len(set(c["lamp"])) == 31 and len(c["lamp"]) == 32 and min(c["lamp"]) == -0.1 and max(c["lamp"]) == 0.5 and c["lamp"][:2] == [0.2, 0.2])
    chk("the repeats sit on processes 0 and 1", all([i % 4 for i, x in enumerate(s["lamp"]) if x == s["rep"]] == [0, 1] for s in (a, b, c)))
    chk("merge windows: a -0.10 to 0.30 with two earlier scans; b 0.11 to 0.40; a plain D covers -0.10 to 0.50", a["mwin"] == (-0.1, 0.3) and len(a["dirs"]) == 2 and b["mwin"] == (0.11, 0.4) and c["mwin"] == (-0.1, 0.5))
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "selftest":
        sys.exit(selftest())
    kind = sys.argv[2]
    {"setup": setup, "read": read}[cmd](kind)
