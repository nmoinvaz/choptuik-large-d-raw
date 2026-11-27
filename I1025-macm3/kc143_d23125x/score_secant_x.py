#!/usr/bin/env python3
"""score_secant_x.py [--write] [--stand-in] [--controls] [--mutate=NAME] : scores the secant and the root of kc143_d23125x against the secant, root and lane items of the registration in README.md
and against t5's bars (#1025 comment 7213649039: |root - (-0.024495)| <= 1e-3 reproduced, >= 3e-3 path-dependent, between as measured; a Delta difference above 1e-6 is a different state whatever the root says),
every number from the files: secant/secant.jsonl, secant/samples.csv, exits_kc143.txt, in/l1kc143macm3d23125x.jsonl (Delta), kc143_d23125/in/l1kc143macm3d23125.jsonl (the reference's Delta), the point summaries of the
k_c 143 D 23.0625 root (zero by the line through the two roots, arithmetic only).
--stand-in reads the files of kc143_d23125 (the earlier lane) to test the script; it never writes.
--controls runs mutations that must flip their items whatever the data say (exit 1 otherwise):
  exit0 / exit4 : the secant exit set to 0 (status tol) / 4 : the exit-0 item HIT / MISS and the exit-4 item the other way
  sec_in / sec_out : every evaluation 270 s / 570 s : the (240, 300) s item HIT / MISS
  wall_in / wall_out : the run wall 25 min / 60 min : the 15 to 35 min item HIT / MISS
  rss_in / rss_out : the peak RSS 8.0 / 11.0 GiB : the (7.5, 9.0) GiB item HIT / MISS
  lane_in / lane_out : the lane 170 min / 300 min : the 130 to 220 min item HIT / MISS
  root_rep / root_mid / root_path / root_low : the root -0.0245 / -0.0265 / -0.0295 / -0.0310 : reproduced / between / path-dependent / path-dependent and below -0.030, each HIT with the others MISS
Tail sums are arithmetic only, not a result. Read-only except for --write."""
import csv, json, math, re, subprocess, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
STAND = "--stand-in" in sys.argv
D = R + ("kc143_d23125/" if STAND else "kc143_d23125x/")
LABEL = "kc143_d23125" if STAND else "kc143_d23125x"
INREC = R + ("kc143_d23125/in/l1kc143macm3d23125.jsonl" if STAND else "kc87_leg_lambda/23.125_kc143x/in/l1kc143macm3d23125x.jsonl")
REF = -0.024495; REFROOT = -0.02449537; DREF = 1.178015433613
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))
DA, DB = 23.0625, 23.125


def readsum(p):
    t = open(p).read()
    return float(re.search(r"det-linear root (-?[\d.]+)", t).group(1))


def read_files():
    recs = [json.loads(l) for l in open(D + "secant/secant.jsonl") if l.strip()]
    ev = [r for r in recs if r.get("kind") == "eval"]; root = [r for r in recs if r.get("kind") == "root"][-1]
    ex = open(D + "exits_kc143.txt").read()
    t_launch = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC %s: start \(mode full" % LABEL, ex).group(1)
    t0 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC %s: secant starts" % LABEL, ex).group(1)
    t1 = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC %s: secant exit (\d+)" % LABEL, ex)
    rows = list(csv.DictReader(open(D + "secant/samples.csv"))); pk = {}
    for s in rows:
        if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
    delta = [json.loads(l) for l in open(INREC) if l.strip()][-1]["Delta"]
    return dict(ev=ev, root=root, t_launch=t_launch, t0=t0, t1=t1.group(1), ecode=int(t1.group(2)), peak=max(pk.values()) / 1048576, nsamp=len(rows),
                lowav=min(float(s["avail_GiB"]) for s in rows if s["avail_GiB"]), delta=delta, ra=readsum(R + "kc143_d230625/point_summary.txt"))


def score(d, mut=""):
    ev, root = d["ev"], d["root"]
    lo, hi = root["bracket"]; rt = root["lam_lin"]; ecode = d["ecode"]; status = root["status"]
    secs = [r["sec"] for r in ev]; wall = root["sec"]; peak = d["peak"]
    lane = hms(d["t1"]) - hms(d["t_launch"])
    if lane < 0: lane += 86400
    if mut == "exit0": ecode, status = 0, "tol"
    if mut == "exit4": ecode, status = 4, "nonrobust"
    if mut == "sec_in": secs = [270] * len(secs)
    if mut == "sec_out": secs = [570] * len(secs)
    if mut == "wall_in": wall = 25 * 60
    if mut == "wall_out": wall = 60 * 60
    if mut == "rss_in": peak = 8.0
    if mut == "rss_out": peak = 11.0
    if mut == "lane_in": lane = 170 * 60
    if mut == "lane_out": lane = 300 * 60
    rt = dict(root_rep=-0.0245, root_mid=-0.0265, root_path=-0.0295, root_low=-0.0310).get(mut, rt)
    off = abs(rt - REF); dd = d["delta"] - DREF
    L = []
    item = lambda name, pct, hit, val: L.append((name, pct, hit, val))
    item("secant exit 0 (tol)", 40, ecode == 0 and status == "tol", "exit %d, status %s, %d evaluations" % (ecode, status, root["n_eval"]))
    item("secant exit 4", 55, ecode == 4, "exit %d (%s)" % (ecode, root.get("why")))
    item("per evaluation in (240, 300) s at all of them", 70, all(240 < s < 300 for s in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
    item("run wall 15 to 35 min", 65, 15 * 60 <= wall <= 35 * 60, "%d s = %.1f min (%s to %s UTC)" % (wall, wall / 60.0, d["t0"], d["t1"]))
    item("peak RSS in (7.5, 9.0) GiB", 60, 7.5 < peak < 9.0, "%.3f GiB (60 s samples of the secant process, %d samples; lowest available %.1f GiB)" % (peak, d["nsamp"], d["lowav"]))
    item("the lane (launch to the secant exit line) 130 to 220 min", 60, 130 * 60 <= lane <= 220 * 60, "%d s = %.1f min (%s to %s UTC)" % (lane, lane / 60.0, d["t_launch"], d["t1"]))
    item("root reproduced: within 1e-3 of -0.024495 (t5's bar)", 52, off <= 1e-3, "root %+.8f, minus the reference %+.6f" % (rt, rt - REF))
    item("root between the bars (1e-3 to 3e-3 from -0.024495)", 14, 1e-3 < off < 3e-3, "root %+.8f, minus the reference %+.6f" % (rt, rt - REF))
    item("root path-dependent: 3e-3 or more from -0.024495 (t5's bar)", 34, off >= 3e-3, "root %+.8f, minus the reference %+.6f" % (rt, rt - REF))
    item("root below -0.030 (a root outside the window, 5.5e-3 or more from the reference)", 24, rt < -0.030, "root %+.8f" % rt)
    item("root within 3e-4 of the reference", 35, off <= 3e-4, "root %+.8f, minus the reference %+.6f" % (rt, rt - REF))
    item("Delta within 1e-6 and the root within 1e-3 together", 48, abs(dd) <= 1e-6 and off <= 1e-3, "Delta difference %+.3e, root minus the reference %+.6f" % (dd, rt - REF))
    return L, dict(rt=rt, lo=lo, hi=hi, ecode=ecode, status=status, wall=wall, lane=lane, off=off, dd=dd)


def controls(d):
    names = {"exit0": {"secant exit 0 (tol)": True, "secant exit 4": False}, "exit4": {"secant exit 0 (tol)": False, "secant exit 4": True},
             "sec_in": {"per evaluation in (240, 300) s at all of them": True}, "sec_out": {"per evaluation in (240, 300) s at all of them": False},
             "wall_in": {"run wall 15 to 35 min": True}, "wall_out": {"run wall 15 to 35 min": False},
             "rss_in": {"peak RSS in (7.5, 9.0) GiB": True}, "rss_out": {"peak RSS in (7.5, 9.0) GiB": False},
             "lane_in": {"the lane (launch to the secant exit line) 130 to 220 min": True}, "lane_out": {"the lane (launch to the secant exit line) 130 to 220 min": False}}
    rep, mid, pth = "root reproduced: within 1e-3 of -0.024495 (t5's bar)", "root between the bars (1e-3 to 3e-3 from -0.024495)", "root path-dependent: 3e-3 or more from -0.024495 (t5's bar)"
    low = "root below -0.030 (a root outside the window, 5.5e-3 or more from the reference)"
    names["root_rep"] = {rep: True, mid: False, pth: False, low: False}; names["root_mid"] = {rep: False, mid: True, pth: False, low: False}
    names["root_path"] = {rep: False, mid: False, pth: True, low: False}; names["root_low"] = {rep: False, mid: False, pth: True, low: True}
    bad = 0
    for mut, w in names.items():
        got = {n: h for n, p, h, v in score(d, mut)[0]}
        ok = all(got[k] == v for k, v in w.items()); bad += (not ok)
        print("control --mutate=%s: %s (wanted %s, read %s)" % (mut, "ok" if ok else "FAILED", list(w.values()), [got[k] for k in w]))
    print("controls: %d of %d failed" % (bad, len(names)))
    return bad


def main():
    d = read_files()
    mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
    if "--controls" in sys.argv:
        sys.exit(1 if controls(d) else 0)
    L, x = score(d, mut)
    ev, root = d["ev"], d["root"]
    H = [i for i in L if i[2]]; M = [i for i in L if not i[2]]
    fmt = lambda i: "%s (%d%%): %s" % (i[0], i[1], i[3])
    ra = d["ra"]; z = DA - ra * (DB - DA) / (x["rt"] - ra); zB = DA - ra * (DB - DA) / (REFROOT - ra); slope = abs((x["rt"] - ra) / (DB - DA))
    word = "reproduced (within 1e-3)" if x["off"] <= 1e-3 else ("path-dependent (3e-3 or more)" if x["off"] >= 3e-3 else "between the bars (1e-3 to 3e-3), reported as measured")
    out = ["**the D 23.125 secant of the x state (k_c 143, regridded from k_c 127) and the root against t5's bars, scored** (secant/secant.jsonl, samples.csv, exits_kc143.txt, the records of the two states; `score_secant_x.py`, controls `--controls`: %d mutations of exit, seconds, wall, RSS, lane and root that must flip their items either way). Secant %s to %s UTC, tol 5e-5, Rust block 12 with 4 threads, one process, **exit %d (%s)**, %d evaluations (the two ends included; interior points %s), **final robust bracket [%.8f, %.8f], width %.3e, signs %s, det-linear root %+.8f** (inside the bracket by position), Brent's last point %.8f; interior evaluations not robust: %s."
           % (14, d["t0"], d["t1"], x["ecode"], x["status"], root["n_eval"], ", ".join("%.8f" % r["lam"] for r in ev[2:]) or "none", x["lo"], x["hi"], x["hi"] - x["lo"], root["signs"], x["rt"], root["lam_brent"],
              ", ".join("%.8f (dln %.3f)" % (r["lam"], r["dln"]) for r in ev if not r["robust"]) or "none")]
    out.append("**t5's bars** (as he wrote them, scored as written): the root %+.8f is %+.6f from his -0.024495 (the earlier lane's root %+.8f): **%s**. Delta difference %+.3e from 1.178015433613 against his 1e-6: %s. These are two words about two quantities; he decides what they mean together. Arithmetic only, not a result: the zero by the line through the D 23.0625 root %+.8f and this root is D %.5f (the earlier lane's: %.5f, k_c 135: 23.07535), slope magnitude %.5f (the earlier lane's 0.63415)." % (
        x["rt"], x["rt"] - REF, REFROOT, word, x["dd"], "a DIFFERENT STATE" if abs(x["dd"]) > 1e-6 else "the same state", ra, z, zB, slope))
    out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + "; ".join("MISS " + fmt(i) for i in M) + ". (%d items: %d HIT, %d MISS; the three bar items exclude each other, exit 0 and exit 4 exclude each other.)" % (len(L), len(H), len(M)))
    txt = "\n".join(out)
    print(txt)
    if "--write" in sys.argv and not mut and not STAND:
        stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
        open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " ")))
        print("written")


if __name__ == "__main__":
    main()
