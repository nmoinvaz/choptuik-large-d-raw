#!/usr/bin/env python3
"""score_scan_r1.py [--write] [--stand-in] [--controls] [--mutate=NAME] : scores the main scan of I1101-macm3 (R1: lambda 0.070, 0.085, 0.100, 0.115, 0.130 and the repeat of 0.070, window (0.070, 0.130)) against the scan items of the
registration in README.md, every number from the files: kc87_leg_lambda/23.0_r1k050/{read_lower.txt, scan/scan_D23.0_1025.jsonl, scan/scan_samples.csv} and exits_r1.txt. The extension scan (23.0_r1k050_ext), if the lane ran one, is not scored here.
--stand-in reads the files of kc143_d23125 (the earlier k_c 143 lane, 6 evaluations, repeat -0.030) to test the script; it never writes.
--controls runs mutations that must flip their items whatever the data say (exit 1 otherwise):
  pair_a/b/c/d : the one robust change set to (0.070, 0.085) / (0.085, 0.100) / (0.100, 0.115) / (0.115, 0.130): that pair item HIT and the others MISS, 'exactly one' HIT, 'none' MISS
  none / multi : no robust change / two: 'none' HIT and 'exactly one' MISS / 'more than one' HIT and 'exactly one' MISS
  sec_in / sec_out, wall_in / wall_out, rss_in / rss_out : seconds 320 / 620, wall 16 / 40 min, peak RSS 5.0 / 9.0 GiB: the (250, 400) s, 11 to 24 min and (4.0, 6.0) GiB items HIT / MISS
Tail sums are arithmetic only, not a result. Read-only except for --write."""
import csv, json, re, subprocess, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
STAND = "--stand-in" in sys.argv
D = R + "kc143_d23125/" if STAND else "/Users/nathan/Source/choptuik-large-d-raw-903/I1101-macm3/"
S = R + "kc87_leg_lambda/" + ("23.125_kc143/" if STAND else "23.0_r1k050/")
LAB = "kc143_d23125" if STAND else "I1101 R1"; EXF = "exits_kc143.txt" if STAND else "exits_r1.txt"; SCANF = "scan/scan_D23.125_1025.jsonl" if STAND else "scan/scan_D23.0_1025.jsonl"
REPLAM = -0.030 if STAND else 0.070
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
PAIRS = {"a": (0.070, 0.085, 7), "b": (0.085, 0.100, 25), "c": (0.100, 0.115, 29), "d": (0.115, 0.130, 14)}


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
    return dict(br=br, nrob=nrob, nonrob=nonrob, sc=sc, t0=t0, t1=t1.group(1), ecode=int(t1.group(2)), pks=sorted(v / 1048576 for v in pk.values())[-2:], low=low)


def score(d, mut=""):
    br, nrob, sc = d["br"], d["nrob"], d["sc"]
    secs = [r["sec"] for r in sc]; wall = hms(d["t1"]) - hms(d["t0"]); pks = list(d["pks"])
    if mut.startswith("pair_"): a, b, _ = PAIRS[mut[5]]; br = (a, b) + (br[2:] if br else ("+", "-", 0.0, 0.0, 0.0)); nrob = 1
    if mut == "none": br, nrob = None, 0
    if mut == "multi": nrob = 2
    if mut == "sec_in": secs = [320] * len(secs)
    if mut == "sec_out": secs = [620] * len(secs)
    if mut == "wall_in": wall = 16 * 60
    if mut == "wall_out": wall = 40 * 60
    if mut == "rss_in": pks = [5.0, 5.0]
    if mut == "rss_out": pks = [9.0, 9.0]
    pair = lambda a, b: br is not None and nrob == 1 and abs(br[0] - a) < 1e-9 and abs(br[1] - b) < 1e-9
    allrob = all(r["noise_robust"] and r["robust"] for r in sc)
    rep = [r for r in sc if abs(r["lam"] - REPLAM) < 1e-12]; assert len(rep) == 2, len(rep)
    keys = [k for k in rep[0] if k not in ("sec", "sec_parts")]; ident = all(rep[0][k] == rep[1][k] for k in keys)
    f64n = sum(1 for r in sc if r["f64_sign"] != r["sign"]); f64pts = sorted({r["lam"] for r in sc if r["f64_sign"] != r["sign"]})
    L = []
    item = lambda name, pct, hit, val: L.append((name, pct, hit, val))
    rv = ("read (%.3f, %.3f), %s to %s, det-linear %.6f, range [%.6f, %.6f]" % br) if br else "no robust change read"
    item("exactly one robust change in (0.070, 0.130)", 75, nrob == 1, "%d robust change(s); not noise-robust points: %s" % (nrob, d["nonrob"]))
    for k, (a, b, p) in PAIRS.items(): item("pair (%.3f, %.3f)" % (a, b), p, pair(a, b), rv)
    item("no robust change in the window", 22, nrob == 0, "%d robust change(s)" % nrob)
    item("more than one robust change", 3, nrob >= 2, "%d robust change(s)" % nrob)
    item("all %d evaluations noise-robust" % len(sc), 80, allrob, "%d of %d robust, dln largest %.2e" % (sum(1 for r in sc if r["noise_robust"] and r["robust"]), len(sc), max(r["dln"] for r in sc)))
    item("the repeat of %.3f bit-identical" % REPLAM, 88, ident, "ln %.10f and %.10f, every field but sec and sec_parts equal: %s" % (rep[0]["ln"], rep[1]["ln"], ident))
    item("float64 sign equal to the hybrid sign at all %d" % len(sc), 25, f64n == 0, "differs at lambda %s (%d of %d evaluations)" % (", ".join("%+.3f" % x for x in f64pts) or "none", f64n, len(sc)))
    item("seconds per evaluation in (250, 400) at all %d" % len(sc), 60, all(250 < s < 400 for s in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
    item("scan wall 11 to 24 min", 60, 11 * 60 <= wall <= 24 * 60, "%d s = %.1f min (%s to %s UTC, exit %d)" % (wall, wall / 60.0, d["t0"], d["t1"], d["ecode"]))
    item("peak RSS per scan process in (4.0, 6.0) GiB", 65, all(4.0 < p < 6.0 for p in pks), "%s GiB (60 s samples, the two scan processes); lowest available memory %.1f GiB" % (", ".join("%.3f" % p for p in pks), d["low"]))
    return L, dict(wall=wall)


def controls(d):
    N = [i[0] for i in score(d)[0]]; nlen = len(d["sc"])
    one, none, multi = "exactly one robust change in (0.070, 0.130)", "no robust change in the window", "more than one robust change"
    pn = {k: "pair (%.3f, %.3f)" % (a, b) for k, (a, b, p) in PAIRS.items()}
    want = []
    for k in PAIRS: want.append(("pair_" + k, dict({one: True, none: False, multi: False}, **{pn[j]: (j == k) for j in PAIRS})))
    want += [("none", {one: False, none: True, multi: False, **{pn[j]: False for j in PAIRS}}), ("multi", {one: False, none: False, multi: True, **{pn[j]: False for j in PAIRS}})]
    sname = "seconds per evaluation in (250, 400) at all %d" % nlen
    want += [("sec_in", {sname: True}), ("sec_out", {sname: False}), ("wall_in", {"scan wall 11 to 24 min": True}), ("wall_out", {"scan wall 11 to 24 min": False}),
             ("rss_in", {"peak RSS per scan process in (4.0, 6.0) GiB": True}), ("rss_out", {"peak RSS per scan process in (4.0, 6.0) GiB": False})]
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
    out = ["**the R1 scan, scored** (read_lower.txt, scan/scan_D23.0_1025.jsonl, scan_samples.csv, exits_r1.txt; `score_scan_r1.py`, controls `--controls`: pair, count, seconds, wall and RSS mutations that must flip their items either way): scan %s to %s UTC (%.1f min), exit %d, 2 processes of 4 Rust threads, %d evaluations. Hybrid signs %s; %s."
           % (d["t0"], d["t1"], x["wall"] / 60.0, d["ecode"], len(sc), hy,
              ("**robust change (%.3f, %.3f), %s to %s, det-linear %.6f, estimator range [%.6f, %.6f] (an estimator range, not an enclosure; the root is read from the secant)**" % br) if br else "**%d robust changes in the window (0.070, 0.130)**" % d["nrob"])]
    out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + ("; ".join("MISS " + fmt(i) for i in M) + ". " if M else "") + "(%d items: %d HIT, %d MISS; the four pair items, the no-change item and the more-than-one item are registered alternatives of one event, so the ones that read MISS are the events that did not occur.)" % (len(L), len(H), len(M)))
    txt = "\n".join(out); print(txt)
    if "--write" in sys.argv and not mut and not STAND:
        stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
        open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " "))); print("written")


if __name__ == "__main__":
    main()
