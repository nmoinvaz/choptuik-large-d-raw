#!/usr/bin/env python3
"""score_scan_r3.py [--write] [--controls] [--mutate=NAME] : scores the R3 scan of I1101-macm3 (the kappa 0.25 re-solve, its own steps, lambda 0.100, 0.115, 0.130, 0.145, window (0.100, 0.145), one process, no repeat) against the scan items of the
registration of the section "R3" in README.md, every number from the files: kc87_leg_lambda/23.0_r3k025/{read_lower.txt, scan/scan_D23.0_1025.jsonl, scan/scan_samples.csv} and r3/exits_r3.txt. The widening (23.0_r3k025_ext, merged in 23.0_r3k025_m) is not scored here.
--controls runs mutations that must flip their items whatever the data say (exit 1 otherwise):
  pair_a/b/c : the one robust change set to (0.100, 0.115) / (0.115, 0.130) / (0.130, 0.145): that pair item HIT and the others MISS, 'exactly one' HIT, 'none' MISS
  (no steps or control items: R3's scan has no --kappa_mm and no control)
  none / multi : no robust change / two: 'none' HIT and 'exactly one' MISS / 'more than one' HIT and 'exactly one' MISS
  sec_in / sec_out, wall_in / wall_out, rss_in / rss_out : seconds 450 / 800, wall 35 / 70 min, peak RSS 7.0 / 12.0 GiB: the (330, 560) s, 25 to 45 min and (5.0, 9.0) GiB items HIT / MISS
Tail sums are arithmetic only, not a result. Read-only except for --write."""
import csv, json, re, subprocess, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
STAND = False
D = "/Users/nathan/Source/choptuik-large-d-raw-903/I1101-macm3/r3/"
S = R + "kc87_leg_lambda/23.0_r3k025/"
LAB = "I1101 R3"; EXF = "exits_r3.txt"; SCANF = "scan/scan_D23.0_1025.jsonl"
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
PAIRS = {"a": (0.100, 0.115, 8), "b": (0.115, 0.130, 25), "c": (0.130, 0.145, 29)}


def read_files():
    rd = open(S + "read_lower.txt").read()
    m = re.search(r"robust change \((\S+), (\S+)\), (\S) to (\S), det-linear (\S+), range \[(\S+), (\S+)\]", rd)
    nrob = int(re.search(r"robust changes: (\d+)", rd).group(1))
    br = (float(m.group(1).rstrip(",")), float(m.group(2).rstrip(",")), m.group(3), m.group(4), float(m.group(5).rstrip(",")), float(m.group(6)), float(m.group(7).rstrip("]"))) if m else None
    nonrob = re.search(r"not noise-robust: (.*)", rd).group(1).strip()
    sc = [json.loads(l) for l in open(S + SCANF) if l.strip()]
    ex = open(D + EXF).read()
    t0 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC %s: scan starts" % re.escape(LAB), ex).group(1)
    t1 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC %s: scan exit (\d+)" % re.escape(LAB), ex)
    pk = {}; low = 1e9
    for r in csv.DictReader(open(S + "scan/scan_samples.csv")):
        if r["rss_kB"]: pk[r["pid"]] = max(pk.get(r["pid"], 0), int(r["rss_kB"]))
        if r["avail_GiB"]: low = min(low, float(r["avail_GiB"]))
    return dict(br=br, nrob=nrob, nonrob=nonrob, sc=sc, t0=t0, t1=t1.group(1), ecode=int(t1.group(2)), pks=sorted(v / 1048576 for v in pk.values())[-1:], low=low)


def score(d, mut=""):
    br, nrob, sc = d["br"], d["nrob"], d["sc"]
    secs = [r["sec"] for r in sc]; wall = hms(d["t1"]) - hms(d["t0"]); pks = list(d["pks"])
    if mut.startswith("pair_"): a, b, _ = PAIRS[mut[5]]; br = (a, b) + (br[2:] if br else ("+", "-", 0.0, 0.0, 0.0)); nrob = 1
    if mut == "none": br, nrob = None, 0
    if mut == "multi": nrob = 2
    if mut == "sec_in": secs = [440] * len(secs)
    if mut == "sec_out": secs = [700] * len(secs)
    if mut == "wall_in": wall = 35 * 60
    if mut == "wall_out": wall = 70 * 60
    if mut == "rss_in": pks = [7.0]
    if mut == "rss_out": pks = [12.0]
    pair = lambda a, b: br is not None and nrob == 1 and abs(br[0] - a) < 1e-9 and abs(br[1] - b) < 1e-9
    allrob = all(r["noise_robust"] and r["robust"] for r in sc)
    allrob = all(r["noise_robust"] and r["robust"] for r in sc)
    f64n = sum(1 for r in sc if r["f64_sign"] != r["sign"]); f64pts = sorted({r["lam"] for r in sc if r["f64_sign"] != r["sign"]})
    L = []
    item = lambda name, pct, hit, val: L.append((name, pct, hit, val))
    rv = ("read (%.3f, %.3f), %s to %s, det-linear %.6f, range [%.6f, %.6f]" % br) if br else "no robust change read"
    item("exactly one robust change in (0.100, 0.145)", 62, nrob == 1, "%d robust change(s); not noise-robust points: %s" % (nrob, d["nonrob"]))
    for k, (a_, b_, p) in PAIRS.items(): item("pair (%.3f, %.3f)" % (a_, b_), p, pair(a_, b_), rv)
    item("no robust change in the window", 33, nrob == 0, "%d robust change(s)" % nrob)
    item("more than one robust change", 5, nrob >= 2, "%d robust change(s)" % nrob)
    item("all %d evaluations noise-robust" % len(sc), 80, allrob, "%d of %d robust, dln largest %.2e" % (sum(1 for r in sc if r["noise_robust"] and r["robust"]), len(sc), max(r["dln"] for r in sc)))
    item("float64 sign equal to the hybrid sign at all %d" % len(sc), 30, f64n == 0, "differs at lambda %s (%d of %d evaluations)" % (", ".join("%+.3f" % x for x in f64pts) or "none", f64n, len(sc)))
    item("seconds per evaluation in (400, 480) at all %d" % len(sc), 65, all(400 < s_ < 480 for s_ in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
    item("scan wall 25 to 36 min", 65, 25 * 60 <= wall <= 36 * 60, "%d s = %.1f min (%s to %s UTC, exit %d)" % (wall, wall / 60.0, d["t0"], d["t1"], d["ecode"]))
    item("peak RSS of the scan process in (5.0, 7.5) GiB", 60, all(5.0 < p < 7.5 for p in pks), "%s GiB (60 s samples); lowest available memory %.1f GiB" % (", ".join("%.3f" % p for p in pks), d["low"]))
    return L, dict(wall=wall)


def controls(d):
    one, none, multi = "exactly one robust change in (0.100, 0.145)", "no robust change in the window", "more than one robust change"
    pn = {k: "pair (%.3f, %.3f)" % (a_, b_) for k, (a_, b_, p) in PAIRS.items()}
    want = []
    for k in PAIRS: want.append(("pair_" + k, dict({one: True, none: False, multi: False}, **{pn[j]: (j == k) for j in PAIRS})))
    want += [("none", {one: False, none: True, multi: False, **{pn[j]: False for j in PAIRS}}), ("multi", {one: False, none: False, multi: True, **{pn[j]: False for j in PAIRS}})]
    nlen = len(d["sc"]); sname = "seconds per evaluation in (400, 480) at all %d" % nlen
    want += [("sec_in", {sname: True}), ("sec_out", {sname: False}), ("wall_in", {"scan wall 25 to 36 min": True}), ("wall_out", {"scan wall 25 to 36 min": False}),
             ("rss_in", {"peak RSS of the scan process in (5.0, 7.5) GiB": True}), ("rss_out", {"peak RSS of the scan process in (5.0, 7.5) GiB": False})]
    bad = 0
    for mut, w in want:
        got = {n: h for n, p, h, v in score(d, mut)[0]}
        ok = all(got[k] == v for k, v in w.items()); bad += (not ok)
        print("control --mutate=%s: %s (%d items checked)" % (mut, "ok" if ok else "FAILED " + str({k: (v, got[k]) for k, v in w.items() if got[k] != v}), len(w)))
    print("controls: %d of %d failed" % (bad, len(want)))
    return bad


def main():
    d = read_files()
    mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
    if "--controls" in sys.argv:
        sys.exit(1 if controls(d) else 0)
    L, x = score(d, mut); sc = d["sc"]; br = d["br"]
    H = [i for i in L if i[2]]; M = [i for i in L if not i[2]]
    fmt = lambda i: "%s (%d%%): %s" % (i[0], i[1], i[3])
    hy = " ".join("%+.3f%s" % (r["lam"], "+" if r["sign"] > 0 else "-") for r in sc)
    out = ["**the R3 scan (kappa 0.25 re-solve, own steps), scored** (read_lower.txt, scan/scan_D23.0_1025.jsonl, scan_samples.csv, exits_r3.txt; `score_scan_r3.py`, controls `--controls`: pair, count, seconds, wall and RSS mutations that must flip their items either way): scan %s to %s UTC (%.1f min), exit %d, 1 process of 4 Rust threads, %d evaluations. Hybrid signs %s; %s."
           % (d["t0"], d["t1"], x["wall"] / 60.0, d["ecode"], len(sc), hy,
              ("**robust change (%.3f, %.3f), %s to %s, det-linear %.6f, estimator range [%.6f, %.6f] (an estimator range, not an enclosure; the root is read from the secant)**" % br) if br else "**%d robust changes in the window (0.100, 0.145)**" % d["nrob"])]
    out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + ("; ".join("MISS " + fmt(i) for i in M) + ". " if M else "") + "(%d items: %d HIT, %d MISS; the three pair items, the no-change item and the more-than-one item are registered alternatives of one event, so the ones that read MISS are the events that did not occur.)" % (len(L), len(H), len(M)))
    txt = "\n".join(out); print(txt)
    if "--write" in sys.argv and not mut:
        stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
        open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " "))); print("written")


if __name__ == "__main__":
    main()
