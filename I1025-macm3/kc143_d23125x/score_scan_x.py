#!/usr/bin/env python3
"""score_scan_x.py [--write] [--stand-in] [--controls] [--mutate=NAME] : scores the main scan of kc143_d23125x (lambda -0.030, -0.025, -0.020 and the repeat of -0.030,
window (-0.030, -0.020)) against the scan items of the registration in README.md (the 'Scan' bullet), every number from the files:
kc87_leg_lambda/23.125_kc143x/{read_lower.txt, scan/scan_D23.125_1025.jsonl, scan/scan_samples.csv}, exits_kc143.txt.
The extension scan (23.125_kc143x_ext), if the follower ran one, is not scored here.
--stand-in reads the files of kc143_d23125 (the earlier lane, 6 evaluations) to test the script; it never writes.
--controls runs the mutations below against the real read and exits 1 unless each one flips its item the way it must (the controls hold whatever the data say):
  br_hi / br_lo : the read bracket set to (-0.025, -0.020) / (-0.030, -0.025): the item of that bracket must read HIT and the other MISS
  nrob0 / nrob1 : the number of robust changes set to 0 / 1: the item 'exactly one robust change' MISS / HIT
  sec_in / sec_out : every evaluation set to 470 s / 770 s: the (440, 500) s item HIT / MISS
  wall_in / wall_out : the scan wall set to 16 min / 40 min: the 14 to 20 min item HIT / MISS
  rss_in / rss_out : the two peak RSS set to 5.5 / 9.5 GiB: the (5.0, 6.0) GiB item HIT / MISS
Tail sums are arithmetic only, not a result. Read-only except for --write."""
import csv, json, re, subprocess, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
STAND = "--stand-in" in sys.argv
D = R + ("kc143_d23125/" if STAND else "kc143_d23125x/")
S = R + "kc87_leg_lambda/" + ("23.125_kc143/" if STAND else "23.125_kc143x/")
LABEL = "kc143_d23125" if STAND else "kc143_d23125x"
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))


def read_files():
    rd = open(S + "read_lower.txt").read()
    m = re.search(r"robust change \((\S+), (\S+)\), (\S) to (\S), det-linear (\S+), range \[(\S+), (\S+)\]", rd)
    nrob = int(re.search(r"robust changes: (\d+)", rd).group(1))
    if m:
        br = (float(m.group(1).rstrip(",")), float(m.group(2).rstrip(",")), m.group(3), m.group(4), float(m.group(5).rstrip(",")), float(m.group(6).rstrip(",")), float(m.group(7).rstrip("]")))
    else:
        br = None
    nonrob = re.search(r"not noise-robust: (.*)", rd).group(1).strip()
    sc = [json.loads(l) for l in open(S + "scan/scan_D23.125_1025.jsonl") if l.strip()]
    ex = open(D + "exits_kc143.txt").read()
    t0 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC %s: scan starts" % LABEL, ex).group(1)
    t1 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC %s: scan exit (\d+)" % LABEL, ex)
    pk = {}; low = 1e9
    for r in csv.DictReader(open(S + "scan/scan_samples.csv")):
        if r["rss_kB"]: pk[r["pid"]] = max(pk.get(r["pid"], 0), int(r["rss_kB"]))
        if r["avail_GiB"]: low = min(low, float(r["avail_GiB"]))
    pks = sorted(v / 1048576 for v in pk.values())[-2:]
    return dict(br=br, nrob=nrob, nonrob=nonrob, sc=sc, t0=t0, t1=t1.group(1), ecode=int(t1.group(2)), pks=pks, low=low)


def score(d, mut=""):
    br, nrob, sc = d["br"], d["nrob"], d["sc"]
    secs = [r["sec"] for r in sc]
    wall = hms(d["t1"]) - hms(d["t0"]); pks = list(d["pks"])
    if mut == "br_hi": br = (-0.025, -0.020) + (br[2:] if br else ("+", "-", 0.0, 0.0, 0.0))
    if mut == "br_lo": br = (-0.030, -0.025) + (br[2:] if br else ("+", "-", 0.0, 0.0, 0.0))
    if mut == "nrob0": nrob = 0
    if mut == "nrob1": nrob = 1
    if mut == "sec_in": secs = [470] * len(secs)
    if mut == "sec_out": secs = [770] * len(secs)
    if mut == "wall_in": wall = 16 * 60
    if mut == "wall_out": wall = 40 * 60
    if mut == "rss_in": pks = [5.5, 5.5]
    if mut == "rss_out": pks = [9.5, 9.5]
    brk = lambda a, b: br is not None and nrob == 1 and abs(br[0] - a) < 1e-9 and abs(br[1] - b) < 1e-9
    allrob = all(r["noise_robust"] and r["robust"] for r in sc)
    rep = [r for r in sc if r["lam"] == -0.030]; assert len(rep) == 2, len(rep)
    keys = [k for k in rep[0] if k not in ("sec", "sec_parts")]; ident = all(rep[0][k] == rep[1][k] for k in keys)
    f64n = sum(1 for r in sc if r["f64_sign"] != r["sign"]); f64pts = sorted({r["lam"] for r in sc if r["f64_sign"] != r["sign"]})
    L = []
    item = lambda name, pct, hit, val: L.append((name, pct, hit, val))
    rv = ("read (%+.3f, %+.3f), %s to %s, det-linear %+.6f, range [%+.6f, %+.6f]" % br) if br else "no robust change read"
    item("exactly one robust change in the window", 72, nrob == 1, "%d robust change(s); not noise-robust points: %s" % (nrob, d["nonrob"]))
    item("bracket (-0.025, -0.020)", 52, brk(-0.025, -0.020), rv)
    item("bracket (-0.030, -0.025)", 18, brk(-0.030, -0.025), rv)
    item("no robust change in the window", 28, nrob == 0, "%d robust change(s)" % nrob)
    item("all %d evaluations noise-robust" % len(sc), 85, allrob, "%d of %d robust, dln largest %.2e" % (sum(1 for r in sc if r["noise_robust"] and r["robust"]), len(sc), max(r["dln"] for r in sc)))
    item("the repeat of -0.030 bit-identical", 88, ident, "ln %.10f and %.10f, every field but sec and sec_parts equal: %s" % (rep[0]["ln"], rep[1]["ln"], ident))
    item("float64 sign equal to the hybrid sign at all %d" % len(sc), 12, f64n == 0, "differs at lambda %s (%d of %d evaluations)" % (", ".join("%+.3f" % x for x in f64pts) or "none", f64n, len(sc)))
    item("seconds per evaluation in (440, 500) at all %d" % len(sc), 65, all(440 < s < 500 for s in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
    item("scan wall 14 to 20 min", 65, 14 * 60 <= wall <= 20 * 60, "%d s = %.1f min (%s to %s UTC, exit %d)" % (wall, wall / 60.0, d["t0"], d["t1"], d["ecode"]))
    item("peak RSS per scan process in (5.0, 6.0) GiB", 65, all(5.0 < p < 6.0 for p in pks), "%s GiB (60 s samples, the two scan processes); lowest available memory %.1f GiB" % (", ".join("%.3f" % p for p in pks), d["low"]))
    return L, dict(wall=wall, secs=secs, pks=pks, nrob=nrob)


def controls(d):
    base = {n: h for n, p, h, v in score(d)[0]}
    want = [("br_hi", {"bracket (-0.025, -0.020)": True, "bracket (-0.030, -0.025)": False}),
            ("br_lo", {"bracket (-0.025, -0.020)": False, "bracket (-0.030, -0.025)": True}),
            ("nrob0", {"exactly one robust change in the window": False, "no robust change in the window": True}),
            ("nrob1", {"exactly one robust change in the window": True, "no robust change in the window": False})]
    nlen = len(d["sc"])
    want += [("sec_in", {"seconds per evaluation in (440, 500) at all %d" % nlen: True}), ("sec_out", {"seconds per evaluation in (440, 500) at all %d" % nlen: False}),
             ("wall_in", {"scan wall 14 to 20 min": True}), ("wall_out", {"scan wall 14 to 20 min": False}),
             ("rss_in", {"peak RSS per scan process in (5.0, 6.0) GiB": True}), ("rss_out", {"peak RSS per scan process in (5.0, 6.0) GiB": False})]
    bad = 0
    for mut, w in want:
        got = {n: h for n, p, h, v in score(d, mut)[0]}
        ok = all(got[k] == v for k, v in w.items()); bad += (not ok)
        print("control --mutate=%s: %s (wanted %s, read %s)" % (mut, "ok" if ok else "FAILED", w, {k: got[k] for k in w}))
    print("controls: %d of %d failed" % (bad, len(want)))
    return bad


def main():
    d = read_files()
    mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
    if "--controls" in sys.argv:
        sys.exit(1 if controls(d) else 0)
    L, x = score(d, mut)
    sc = d["sc"]
    H = [i for i in L if i[2]]; M = [i for i in L if not i[2]]
    fmt = lambda i: "%s (%d%%): %s" % (i[0], i[1], i[3])
    hy = " ".join("%+.3f%s" % (r["lam"], "+" if r["sign"] > 0 else "-") for r in sc)
    br = d["br"]
    out = ["**the scan, scored** (read_lower.txt, scan/scan_D23.125_1025.jsonl, scan_samples.csv, exits_kc143.txt; `score_scan_x.py`, controls `--controls`: bracket, count, seconds, wall and RSS mutations that must flip their items either way): scan %s to %s UTC (%.1f min), exit %d, 2 processes of 4 Rust threads, %d evaluations. Hybrid signs %s; %s."
           % (d["t0"], d["t1"], x["wall"] / 60.0, d["ecode"], len(sc), hy,
              ("**robust change (%+.3f, %+.3f), %s to %s, det-linear %+.6f, estimator range [%+.6f, %+.6f] (an estimator range, not an enclosure; the root is read from the secant)**" % br) if br else "**%d robust changes in the window (-0.030, -0.020)**" % d["nrob"])]
    out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + "; ".join("MISS " + fmt(i) for i in M) + ". (%d items: %d HIT, %d MISS; the two bracket items and the no-change item are registered alternatives of one event, so the ones that read MISS are the events that did not occur.)" % (len(L), len(H), len(M)))
    txt = "\n".join(out)
    print(txt)
    if "--write" in sys.argv and not mut and not STAND:
        stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
        open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " ")))
        print("written")


if __name__ == "__main__":
    main()
