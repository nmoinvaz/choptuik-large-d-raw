#!/usr/bin/env python3
"""score_k4w.py [--write] [--controls] [--mutate=NAME] : scores the K4w scan (R1's state at --kappa_mm=0.25, lambda 0.070, 0.085, 0.160, 0.180, one process, folder kc87_leg_lambda/23.0_r1k050_kmm025w) and the merged reading of the eight lambda
(kc87_leg_lambda/23.0_r1k050_kmm025m/read_lower.txt, 'points 8') against the items of the section "K4w: the widening" in README.md, every number from the files: the scan's jsonl, scan_p0.log, scan_samples.csv, kmm025/exits_kmm_w.txt (the scan's
start and exit) and the merged read_lower.txt. The first reading of the merge ('points 0') was a read failure and is not scored.
--controls runs mutations that must flip their items whatever the data say (exit 1 otherwise): pair_a/b/c/d (the first robust change set to (0.145, 0.160) / (0.160, 0.180) / (0.085, 0.100) / (0.070, 0.085): that item HIT, the others MISS),
none / multi (no change / two: that item HIT, the pairs MISS), sec_in/out (seconds 445 / 620), wall_in/out (32 / 50 min), rss_in/out (6.0 / 9.0 GiB), steps_in/out (11687 / 9000). Tail sums are arithmetic only, not a result. Read-only except for --write."""
import csv, json, re, subprocess, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/"
S = R + "I1025-macm3/kc87_leg_lambda/"; W = S + "23.0_r1k050_kmm025w/"; M = S + "23.0_r1k050_kmm025m/"; D = R + "I1101-macm3/"
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
PAIRS = {"a": (0.145, 0.160, 12), "b": (0.160, 0.180, 28), "c": (0.085, 0.100, 12), "d": (0.070, 0.085, 10)}


def read_files():
    rd = open(M + "read_lower.txt").read()
    npts = int(re.search(r"^points (\d+)", rd, re.M).group(1))
    chs = [(float(a), float(b)) for a, b in re.findall(r"robust change \((\S+), (\S+)\), \S to \S", rd) for a, b in [(a.rstrip(","), b)]]
    est = re.search(r"robust change \((\S+), (\S+)\), (\S) to (\S), det-linear (\S+), range \[(\S+), (\S+)\]", rd)
    signs = re.search(r"^hybrid signs: (.*)$", rd, re.M).group(1)
    sc = [json.loads(l) for l in open(W + "scan/scan_D23.0_1025.jsonl") if l.strip()]
    ex = open(D + "kmm025/exits_kmm_w.txt").read()
    t0 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC I1101 K4w: scan starts", ex).group(1)
    t1 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC I1101 K4w: scan exit (\d+)", ex)
    ks = int(re.search(r"^kappa_mm 0\.25: .*?, (\d+) steps \(the record", open(W + "scan/scan_p0.log").read(), re.M).group(1))
    pk = {}
    for r in csv.DictReader(open(W + "scan/scan_samples.csv")):
        if r["rss_kB"]: pk[r["pid"]] = max(pk.get(r["pid"], 0), int(r["rss_kB"]))
    return dict(npts=npts, chs=chs, est=est.groups() if est else None, signs=signs, sc=sc, t0=t0, t1=t1.group(1), ecode=int(t1.group(2)), ks=ks, pk=max(pk.values()) / 1048576)


def score(d, mut=""):
    chs, sc = list(d["chs"]), d["sc"]; secs = [r["sec"] for r in sc]; wall = hms(d["t1"]) - hms(d["t0"]); pk = d["pk"]; ks = d["ks"]
    if mut.startswith("pair_"): a, b, _ = PAIRS[mut[5]]; chs = [(a, b)]
    if mut == "none": chs = []
    if mut == "multi": chs = [(0.070, 0.085), (0.160, 0.180)]
    if mut == "sec_in": secs = [445] * 4
    if mut == "sec_out": secs = [620] * 4
    if mut == "wall_in": wall = 32 * 60
    if mut == "wall_out": wall = 50 * 60
    if mut == "rss_in": pk = 6.0
    if mut == "rss_out": pk = 9.0
    if mut == "steps_in": ks = 11687
    if mut == "steps_out": ks = 9000
    first = chs[0] if chs else None
    L = []
    item = lambda name, pct, hit, val: L.append((name, pct, hit, val))
    rv = "first robust change read (%.3f, %.3f) of %d" % (first[0], first[1], len(chs)) if first else "no robust change read"
    for k, (a, b, p) in PAIRS.items(): item("first robust change in (%.3f, %.3f)" % (a, b), p, bool(chs) and len(chs) == 1 and abs(first[0] - a) < 1e-9 and abs(first[1] - b) < 1e-9, rv)
    item("no robust change in (0.070, 0.180)", 30, len(chs) == 0, "%d robust change(s), %d points read" % (len(chs), d["npts"]))
    item("two or more robust changes", 8, len(chs) >= 2, "%d robust change(s)" % len(chs))
    item("all 4 noise-robust", 80, all(r["noise_robust"] and r["robust"] for r in sc), "dln largest %.2e" % max(r["dln"] for r in sc))
    item("seconds per evaluation in (420, 470) at all 4", 75, all(420 < s < 470 for s in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
    item("scan wall 27 to 36 min", 70, 27 * 60 <= wall <= 36 * 60, "%d s = %.1f min (%s to %s UTC, exit %d)" % (wall, wall / 60.0, d["t0"], d["t1"], d["ecode"]))
    item("peak RSS of the scan process in (5.5, 7.0) GiB", 65, 5.5 < pk < 7.0, "%.3f GiB" % pk)
    item("the printed steps line 11687 (as K4's)", 90, ks == 11687, "%d steps" % ks)
    return L, wall


def controls(d):
    names = {k: "first robust change in (%.3f, %.3f)" % (a, b) for k, (a, b, p) in PAIRS.items()}; nn, mm = "no robust change in (0.070, 0.180)", "two or more robust changes"
    want = [("pair_" + k, {**{names[j]: (j == k) for j in PAIRS}, nn: False, mm: False}) for k in PAIRS]
    want += [("none", {**{names[j]: False for j in PAIRS}, nn: True, mm: False}), ("multi", {**{names[j]: False for j in PAIRS}, nn: False, mm: True})]
    want += [("sec_in", {"seconds per evaluation in (420, 470) at all 4": True}), ("sec_out", {"seconds per evaluation in (420, 470) at all 4": False}), ("wall_in", {"scan wall 27 to 36 min": True}), ("wall_out", {"scan wall 27 to 36 min": False}),
             ("rss_in", {"peak RSS of the scan process in (5.5, 7.0) GiB": True}), ("rss_out", {"peak RSS of the scan process in (5.5, 7.0) GiB": False}), ("steps_in", {"the printed steps line 11687 (as K4's)": True}), ("steps_out", {"the printed steps line 11687 (as K4's)": False})]
    bad = 0
    for mut, w in want:
        got = {n: h for n, p, h, v in score(d, mut)[0]}
        ok = all(got[k] == v for k, v in w.items()); bad += (not ok)
        print("control --mutate=%s: %s (%d items checked)" % (mut, "ok" if ok else "FAILED " + str({k: (v, got[k]) for k, v in w.items() if got[k] != v}), len(w)))
    print("controls: %d of %d failed" % (bad, len(want)))
    return bad


def main():
    d = read_files(); mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
    if "--controls" in sys.argv: sys.exit(1 if controls(d) else 0)
    L, wall = score(d, mut); H = [i for i in L if i[2]]; M_ = [i for i in L if not i[2]]
    fmt = lambda i: "%s (%d%%): %s" % (i[0], i[1], i[3])
    e = d["est"]
    out = ["**the K4w scan and the merged reading, scored** (kc87_leg_lambda/23.0_r1k050_kmm025w and ..._kmm025m/read_lower.txt, exits_kmm_w.txt; `score_k4w.py`, controls `--controls`: pair, count, seconds, wall, RSS and steps mutations that must flip their items either way): scan of lambda 0.070, 0.085, 0.160, 0.180 at --kappa_mm=0.25 %s to %s UTC (%.1f min), exit %d, 1 process of 4 Rust threads. The merged reading of the eight lambda read %d points; hybrid signs %s; %s. The first reading of the merge, 'points 0' (read_lower.py reads scan_*_p*.jsonl and merge_kmm.py had written scan_D23.0_1025.jsonl only), was a read failure, not scored."
           % (d["t0"], d["t1"], wall / 60.0, d["ecode"], d["npts"], d["signs"], ("**robust change (%s, %s), %s to %s, det-linear %s, estimator range [%s, %s] (an estimator range, not an enclosure; the root is read from the secant)**" % e) if e else "no robust change")]
    out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + ("; ".join("MISS " + fmt(i) for i in M_) + ". " if M_ else "") + "(%d items: %d HIT, %d MISS; the four pair items, the no-change item and the two-or-more item are registered alternatives of one event.)" % (len(L), len(H), len(M_)))
    txt = "\n".join(out); print(txt)
    if "--write" in sys.argv and not mut:
        stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
        open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " "))); print("written")


if __name__ == "__main__":
    main()
