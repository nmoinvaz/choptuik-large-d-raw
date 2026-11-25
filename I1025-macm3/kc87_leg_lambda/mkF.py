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
    if kind == "d":          # t5, hc 25 Nov ~16:50 UTC: D 22.9375 on -0.50..-0.10 by 0.04 (the lower track's position)
        vals = [round(-0.50 + 0.04 * i, 2) for i in range(11)]
        rep = -0.30
        lamp = [rep, rep] + [v for v in vals if v != rep]
        return dict(D=22.9375, folder="22.9375_low", lamp=lamp, win=(-0.50, -0.10), rep=rep, dirs=["22.9375/scan"], mwin=(-0.50, 0.30), step=0.04)
    if kind == "f":          # t5, hc 25 Nov ~18:25 UTC: D 23.0 on -0.50..-0.10 by 0.04 plus a repeat, right after 22.9375_low, before 22.875_up
        vals = [round(-0.50 + 0.04 * i, 2) for i in range(11)]
        rep = -0.30
        lamp = [rep, rep] + [v for v in vals if v != rep]
        return dict(D=23.0, folder="23.0_low", lamp=lamp, win=(-0.50, -0.10), rep=rep, dirs=["23.0/scan"], mwin=(-0.50, 0.30), step=0.04)
    if kind == "e":          # t5: D 22.875 on 0.30..0.50 by 0.04
        vals = [0.30, 0.34, 0.38, 0.42, 0.46, 0.50]
        rep = 0.38
        lamp = [rep, rep] + [v for v in vals if v != rep]
        return dict(D=22.875, folder="22.875_up", lamp=lamp, win=(0.30, 0.50), rep=rep, dirs=["22.875/scan", "22.875_wide/scan", "22.875_F/scan"], mwin=(-0.10, 0.50), step=0.04)
    if kind == "c":          # t5, hc 25 Nov ~16:44 UTC: D 22.8125 up, 0.42 to 0.50 by 0.02 plus a repeat, to find F (no F up to 0.400)
        vals = [0.42, 0.44, 0.46, 0.48, 0.50]
        rep = 0.46
        lamp = [rep, rep] + [v for v in vals if v != rep]
        return dict(D=22.8125, folder="22.8125_F2", lamp=lamp, win=(0.42, 0.50), rep=rep, dirs=["22.8125/scan", "22.8125_ext/scan", "22.8125_F/scan"], mwin=(0.11, 0.50))
    if kind == "b":
        vals = [round(0.24 + 0.02 * i, 2) for i in range(9)]                 # 0.24 .. 0.40
        rep = 0.32
        lamp = [rep, rep] + [v for v in vals if v != rep]
        return dict(D=22.8125, folder="22.8125_F", lamp=lamp, win=(0.24, 0.40), rep=rep, dirs=["22.8125/scan", "22.8125_ext/scan"], mwin=(0.11, 0.40))
    # a plain D: both roots on -0.10 to 0.50 by 0.02 (D 22.75, t5: "keep D 22.75 at 0.02 as queued"); "D@0.04": by 0.04, 16 points and a repeat of 0.30 (t5, hc 25 Nov after 15:53 UTC:
    # "for the rest use 0.04 (-0.10 to 0.50, 16 points + a repeat) and only D 22.5 and D 22.625")
    D = float(kind.split("@")[0]); step = float(kind.split("@")[1]) if "@" in kind else 0.02
    n = round(0.60 / step) + 1
    if MUT == "grid":
        n -= 1
    vals = [round(-0.10 + step * i, 2) for i in range(n)]
    rep = 0.30 if step > 0.03 else 0.20
    lamp = [rep, rep] + [v for v in vals if v != rep]
    dirs = ["%r/scan" % D] if os.path.isdir("%s/%r/scan" % (L, D)) else []
    return dict(D=D, folder="%r_both" % D, lamp=lamp, win=(-0.10, 0.50), rep=rep, dirs=dirs, mwin=(-0.10, 0.50), step=step)


def lonly_set():
    return set(float(x) for ln in open(L + "/L_ONLY.txt") if not ln.startswith("#") for x in ln.split()) if os.path.exists(L + "/L_ONLY.txt") else set()


def froots():
    """the lambda_1 (F) roots in roots87.txt: {D: root} from the lines the chain reads, and the L comment lines {D: root}"""
    f, l = {}, {}
    lonly = set()
    if os.path.exists(L + "/L_ONLY.txt"):
        lonly = set(float(x) for ln in open(L + "/L_ONLY.txt") if not ln.startswith("#") for x in ln.split())
    for ln in open(L + "/roots87.txt"):
        w = ln.split()
        if ln.startswith("#L ") and len(w) >= 3:
            l[float(w[1])] = float(w[2])
        elif w and not ln.startswith("#") and float(w[0]) not in lonly:
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
    head = "\n## D %s %s scan (written before its check and scan, %s UTC)\n\n**Order** %s\n" % (dn, "F (upper root)" if kind in ("a", "b", "c") else ("lower root" if kind in ("d", "f") else ("upper range" if kind == "e" else "both roots")), now(), ORDER)
    grid = ("**Grid:** lambda %s, the repeat %s first (twice, on processes 0 and 1); %d evaluations on 4 processes of 1 thread at nice 15 (%d rounds, about %d min; %s); window read on this scan alone `read_lower.py scan %s %s` and merged with %s "
            "(`ext23.read_merged`; the earlier readings of D %s are not replaced) on lambda %s to %s.\n") % (
        "%s to %s%s" % (fmt(lo), fmt(hi), " by 0.01" if kind == "a" else " by %.2f" % sp.get("step", 0.02)), fmt(sp["rep"]), nev, rounds, rounds * 10, assign, fmt(lo), fmt(hi),
        ("the scans " + ", ".join("`%s`" % d for d in sp["dirs"])) if sp["dirs"] else "no earlier scan", dn, fmt(sp["mwin"][0]), fmt(sp["mwin"][1]))
    common = ("the source check accepts with all controls firing and the k_c 79 check refusing about 90%%; the repeat of %s bit-identical about 90%%; all %d noise-robust about %d%%; no ln|det| minimum without a sign change about 85%%; "
              "the float64 sign equals the hybrid at every evaluation about 55%%; scan wall %d to %d min about 70%%; no memory alert about 90%%.") % (fmt(sp["rep"]), nev, 80 if nev <= 10 else 70, rounds * 8, rounds * 14)
    if kind == "a":
        txt = (head +
               "**Why:** the merged reading of D 22.875 (`22.875_wide/read_lower_merged.txt`) has two robust changes: (0.120, 0.130) '- to +' (0.127834, L) and (0.160, 0.200) '+ to -' (det-linear 0.171403, range [0.161208, 0.171403], F); the grid has no point between 0.16 and 0.20.\n"
               "**Prediction (F, the upper root):** det-linear estimate of the merged reading **0.1714** (its estimate from 0.16 and 0.20); the chord of F between D 22.25 (0.442516) and D 22.9375 (0.056199) gives 0.0913 at D 22.875 and F, being concave (the roots fall faster toward D 23), lies at or above it; **0.1714** is my primary value. I expect F between the grid values 0.17 and 0.19 about 75%, between 0.16 and 0.17 about 12%, between 0.19 and 0.20 about 13%.\n" + grid +
               "**Predictions (mine, before the run):** " + common + " The merged reading has exactly two robust changes (L at 0.120-0.130 unchanged, F) about 85%; F's bracket narrows to a 0.01 interval inside (0.160, 0.200) about 85%; F's det-linear estimate within 0.01 of 0.1714 about 60%; the orientation of F '+ to -' about 95%.\n## Log\n")
    elif kind == "c":
        txt = (head +
               "**Why:** the merged reading of D 22.8125 (first scan 0.17-0.23, extension 0.11-0.16, F scan 0.24-0.40; `22.8125_F/read_lower_merged.txt`) has one change, L at (0.160, 0.170) '- to +', and the hybrid sign is + at every value from 0.17 to 0.40, so F is above 0.400 (t5: extend up to find it, and do not label D 22.8125 until F is found).\n"
               "**Prediction (F, the upper root):** if F falls monotonically with D, F at D 22.8125 lies between F at D 22.875 (0.162334) and F at D 22.25 (0.442516), and above 0.400 by the reading: in (0.400, 0.4425]. I expect: in the unscanned gap (0.400, 0.420) about 20%; in (0.420, 0.4425] about 25%; in (0.4425, 0.50) about 25%; above 0.50 about 25%; no change at all because F has left the real axis about 5%. If F is in (0.4, 0.4425), the F line is nearly flat (0.4425 at D 22.25, about 0.42 at D 22.8) and then falls to 0.162 within 0.0625 in D.\n" + grid +
               "**Predictions (mine, before the run):** " + common + " The merged reading has exactly two robust changes (L unchanged, F '+ to -') about 70%; one about 30% (F above 0.50 or gone).\n## Log\n")
    elif kind == "f":
        import re as _re
        r = None
        rd = L + "/22.9375_low/read_lower_merged.txt"
        if os.path.exists(rd):
            m = _re.search(r"robust change \((-?[\d.]+), (-?[\d.]+)\), - to \+, det-linear (-?[\d.]+)", open(rd).read())
            if m and float(m.group(1)) < -0.09:
                r = (float(m.group(1)), float(m.group(2)), float(m.group(3)))
        where = ("At D 22.9375 the negative root read %.6f (bracket (%.2f, %.2f), `22.9375_low/read_lower_merged.txt`). " % (r[2], r[0], r[1])) if r else "D 22.9375's negative scan has no '- to +' change below -0.09 in its merged reading (or it is not read), so this scan runs without a value to compare with. "
        pred = (("**Prediction:** the two readings differ in what the negative root does between D 22.9375 and D 23.0: (B) the newcomer keeps diving at its rate of at least 4 to 5 per unit D, so the root at D 23.0 is at least 0.25 below %.3f, i.e. at or below %.2f, probably outside the window (below -0.50 if the D 22.9375 root is below -0.25); (A) lambda_1 has just made its jump and then falls at a rate like the c2 points' (-1.2 per unit D), so the root at D 23.0 is within 0.15 of %.3f (centre about %.2f, one step of -1.2 per unit D). "
                 "I expect (registered with the 22.9375 reading in hand): the root in (-0.50, -0.10) with a change '- to +' about 60%%; no change in the window because the root is below -0.50 about 30%%; a change above the D 22.9375 value (rising) about 3%%; other about 7%%." % (r[2], r[2] - 0.25, r[2], r[2] - 0.075)) if r else
                "**Prediction:** (B) the negative root keeps falling past D 22.9375 and may leave the window below -0.50; (A) it is near its D 22.9375 place, within about 0.15. Without the D 22.9375 value: a change '- to +' in (-0.50, -0.10) about 55%, none about 35%, other 10%.")
        txt = (head + "**Why:** t5 (hc ~18:25 UTC, quoted): \"yes, queue D 23.0 on -0.50..-0.10 by 0.04 (plus a repeat) right after D 22.9375_low, before D 22.875_up.\" The readings (hc ~18:10 UTC, quoted): \"(A) lambda_1 0.128 (22.875) -> below -0.10 at 22.9375, a dive of < -3.6 per unit D, with the newcomer 0.162 -> 0.056 -> -0.022; (B) lambda_1 0.128 -> 0.056 -> -0.022 (slopes -1.15, -1.24, smooth steepening from -0.45, -0.78, -0.62), with the newcomer 0.162 -> below -0.10 (a fast dive like S). (B) predicts the D 22.9375 negative root well below -0.10 and continuing to fall at 23.0; (A) predicts it near -0.1 to -0.2.\" "
               "The scan of D 23.0 (-0.10 to 0.30) has one change, '+ to -' at -0.021546, and the sign is + at -0.10, so an odd number of roots lies below -0.10.\n" + where + "\n" + pred.replace("%%", "%") + "\n" + grid +
               "**Predictions (mine, before the run):** " + common + " The merged reading (-0.50 to 0.30) has exactly two robust changes (the negative root '- to +', then '+ to -' at -0.0215) about 55%.\n## Log\n")
    elif kind in ("d", "e"):
        hyp = ("t5's hypothesis (hc ~16:50 UTC, quoted): \"lambda_1 is the track you called L (0.4425 at 22.25, 0.2161 at 22.75, 0.1670 at 22.8125, 0.1278 at 22.875: slope -0.45 to -0.8, like F's earlier slope), and the upper root of D 22.875 (0.1623, then 0.0562 at 22.9375 and -0.0215 at 23.0) "
               "is a NEWCOMER diving from above 0.50 (like S). Under it, lambda_1 crosses 0 between 22.875 and 22.9375 (it is below -0.10 at 22.9375). Leave every label as is until D 22.75's both-roots scan reads: one root at 0.216 in -0.10..0.50 supports it. "
               "Then add D 22.9375 on -0.50..-0.10 by 0.04 (find the lower track's position there) and D 22.875 on 0.30..0.50 by 0.04.\"\n")
        if kind == "d":
            txt = (head + "**Why:** " + hyp +
                   "The scan of D 22.9375 (-0.10 to 0.30) has one change, '+ to -' at 0.056, and the sign is + at -0.10, so an odd number of roots lies below -0.10 (the lower track, in either reading).\n"
                   "**Prediction (the lower root at D 22.9375):** the track L (0.2161 at D 22.75, 0.1278 at D 22.875, slope -0.706 per unit D between them) would read +0.084 at D 22.9375 if it kept that slope; the signs say it is below -0.10, so it dives at least 3.65 per unit D faster between D 22.875 and 22.9375. I expect one change '- to +' in (-0.50, -0.10) about 65%, below -0.50 about 20%, no change (the + at -0.10 has another cause) about 15%.\n" + grid +
                   "**Predictions (mine, before the run):** " + common + " The merged reading (-0.50 to 0.30) has exactly two robust changes ('- to +' in the new window, then F's/N's '+ to -' at 0.056) about 65%.\n## Log\n")
        else:
            txt = (head + "**Why:** " + hyp +
                   "The scans of D 22.875 cover -0.10 to 0.30 (two changes: 0.127834 '- to +' and 0.162334 '+ to -', the sign - at 0.17 to 0.30); nothing above 0.30 is known.\n"
                   "**Prediction:** under the newcomer reading nothing else lies in (0.30, 0.50) at D 22.875 (the newcomer came from above 0.50 and is already at 0.162): all signs - about 65%; one change '- to +' in (0.30, 0.50) (a third root, the flat F rising into the window from above) about 15%; two changes about 12%; other about 8%.\n" + grid +
                   "**Predictions (mine, before the run):** " + common + " The merged reading (-0.10 to 0.50) keeps the two changes at 0.127834 and 0.162334 about 95%.\n## Log\n")
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
        pf = ("lambda_1 (the F lines of roots87.txt) near its line: the chord between its roots at D %r (%.6f) and D %r (%.6f) gives **%.4f** at D %r (lambda_1 is concave in D, so it lies at or above the chord)." % (a_, f[a_], c_, f[c_], chord, D)) if chord is not None else "lambda_1: no roots on both sides (no line)."
        txt = (head +
               "**Why:** reading B (t5's ruling, hc ~18:50 UTC, quoted): \"lambda_1 runs 0.4425 (22.25), 0.216 (22.75), 0.167 (22.8125), 0.128 (22.875), 0.056 (22.9375), -0.0215 (23.0), slopes -0.45, -0.78, -0.62, -1.15, -1.24, smooth. The newcomer runs >0.50 (22.8125), 0.162 (22.875), -0.226 (22.9375), slopes < -5.4 and -6.2, a steady fast dive like S.\" "
               "At D 22.75 the both-roots scan (-0.10 to 0.50) has one change only, lambda_1 at 0.216; the newcomer is above 0.50 there. D %r lies below D 22.75, where the newcomer is higher still, so one change is expected in -0.10 to 0.50.\n" % D +
               "**Prediction (lambda_1, the F line):** " + pf + " The newcomer: above 0.50, outside the window.\n" + grid +
               "**Predictions (mine, before the run):** " + common +
               " The merged reading has exactly one robust change, '- to +' (lambda_1), about 75%; none about 8% (lambda_1 outside -0.10 to 0.50 or unresolved); two or more about 12% (the newcomer or S inside the window: I cannot place S below -0.10, the sign at -0.10 would then change); other about 5%. "
               "Given one change: within 0.04 of the chord about 70%, above the chord about 70%.\n## Log\n")
    return txt


def folder(kind):
    print(spec(kind)["folder"])


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
    cc = spec("c")
    chk("c: D 22.8125 up, 0.42 to 0.50 by 0.02 with 0.46 twice first (6 evaluations), folder 22.8125_F2, three earlier scans", cc["D"] == 22.8125 and cc["lamp"] == [0.46, 0.46, 0.42, 0.44, 0.48, 0.5] and cc["folder"] == "22.8125_F2" and len(cc["dirs"]) == 3 and cc["win"] == (0.42, 0.5))
    dd, ee, ff = spec("d"), spec("e"), spec("f")
    chk("f: D 23.0 on -0.50 to -0.10 by 0.04 and -0.30 twice first: 12 evaluations, folder 23.0_low", ff["D"] == 23.0 and len(set(ff["lamp"])) == 11 and len(ff["lamp"]) == 12 and ff["lamp"][:2] == [-0.3, -0.3] and ff["folder"] == "23.0_low" and ff["dirs"] == ["23.0/scan"])
    chk("d: D 22.9375 on -0.50 to -0.10 by 0.04 (11 values) and -0.30 twice first: 12 evaluations, folder 22.9375_low", dd["D"] == 22.9375 and len(set(dd["lamp"])) == 11 and len(dd["lamp"]) == 12 and min(dd["lamp"]) == -0.5 and max(dd["lamp"]) == -0.1 and dd["lamp"][:2] == [-0.3, -0.3] and dd["folder"] == "22.9375_low")
    chk("e: D 22.875 on 0.30 to 0.50 by 0.04 (6 values) and 0.38 twice first: 7 evaluations, folder 22.875_up", ee["D"] == 22.875 and sorted(set(ee["lamp"])) == [0.3, 0.34, 0.38, 0.42, 0.46, 0.5] and len(ee["lamp"]) == 7 and ee["lamp"][:2] == [0.38, 0.38] and ee["folder"] == "22.875_up")
    d4 = spec("22.5@0.04")
    chk("D@0.04: 16 values -0.10 to 0.50 by 0.04 and the repeat 0.30 first: 17 evaluations, folder 22.5_both", len(set(d4["lamp"])) == 16 and len(d4["lamp"]) == 17 and min(d4["lamp"]) == -0.1 and max(d4["lamp"]) == 0.5 and d4["lamp"][:2] == [0.3, 0.3] and d4["folder"] == "22.5_both" and d4["D"] == 22.5)
    chk("the repeats sit on processes 0 and 1", all([i % 4 for i, x in enumerate(s["lamp"]) if x == s["rep"]] == [0, 1] for s in (a, b, c, d4, cc, dd, ee, ff)))
    chk("merge windows: a -0.10 to 0.30 with two earlier scans; b 0.11 to 0.40; a plain D covers -0.10 to 0.50", a["mwin"] == (-0.1, 0.3) and len(a["dirs"]) == 2 and b["mwin"] == (0.11, 0.4) and c["mwin"] == (-0.1, 0.5))
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "selftest":
        sys.exit(selftest())
    kind = sys.argv[2]
    {"setup": setup, "read": read, "folder": folder}[cmd](kind)
