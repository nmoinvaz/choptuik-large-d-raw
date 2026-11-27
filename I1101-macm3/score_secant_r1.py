#!/usr/bin/env python3
"""score_secant_r1.py [--write] [--stand-in] [--controls] [--mutate=NAME] [--delta2=X] : scores the secant and the root of I1101-macm3 (R1, kappa 0.5) against the secant, root and lane items of the registration in README.md,
every number from the files: secant/secant.jsonl, secant/samples.csv, exits_r1.txt. With --delta2=X (R2's shift of the root from R0's 0.045968, from t5's #1101 record) it prints t5's ratio r = delta_1/(delta_2 - delta_1) with delta_1 = root - 0.045968,
the bar [3.0, 4.6] (kappa^4 predicts 3.74) and the order p solving (0.7^p - 0.5^p)/(0.5^p - 0.35^p) = r (arithmetic only, not a result).
--stand-in reads the files of kc143_d23125x (the k_c 143 cross-path lane, exit 0) to test the script; it never writes.
--controls runs mutations that must flip their items whatever the data say (exit 1 otherwise):
  exit0 / exit4 : the secant exit set to 0 (status tol) / 4 : the exit-0 item HIT / MISS and the exit-4 item the other way
  sec_in / sec_out : every evaluation 190 s / 590 s : the (150, 240) s item HIT / MISS;  wall_in / wall_out : the run wall 25 / 70 min : the 15 to 45 min item HIT / MISS
  rss_in / rss_out : the peak RSS 7.0 / 11.0 GiB : the (5.5, 8.0) GiB item HIT / MISS;  lane_in / lane_out : the lane 140 / 300 min : the 90 to 180 min item HIT / MISS
  root_a / root_b / root_c / root_d : the root 0.100 / 0.0888 / 0.050 / 0.040 : the items on 'above 0.045968', 'in (0.09, 0.115)' and 'in (0.0886, 0.1122)' must read (H, H, H) / (H, M, H) / (H, M, M) / (M, M, M)
Tail sums are arithmetic only, not a result. Read-only except for --write."""
import csv, json, math, re, subprocess, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/"
STAND = "--stand-in" in sys.argv
D = R + ("I1025-macm3/kc143_d23125x/" if STAND else "I1101-macm3/")
LAB = "kc143_d23125x" if STAND else "I1101 R1"; EXF = "exits_kc143.txt" if STAND else "exits_r1.txt"
R0 = 0.045968
hms = lambda s: sum(int(x) * k for x, k in zip(s.split(":"), (3600, 60, 1)))


def read_files():
    recs = [json.loads(l) for l in open(D + "secant/secant.jsonl") if l.strip()]
    ev = [r for r in recs if r.get("kind") == "eval"]; root = [r for r in recs if r.get("kind") == "root"][-1]
    ex = open(D + EXF).read(); U = r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC " + re.escape(LAB) + ": "
    t_launch = re.search(U + r"start \(mode full", ex).group(1); t0 = re.search(U + "secant starts", ex).group(1); t1 = re.search(U + r"secant exit (\d+)", ex)
    rows = list(csv.DictReader(open(D + "secant/samples.csv"))); pk = {}
    for s in rows:
        if s["rss_kB"]: pk[s["pid"]] = max(pk.get(s["pid"], 0), int(s["rss_kB"]))
    return dict(ev=ev, root=root, t_launch=t_launch, t0=t0, t1=t1.group(1), ecode=int(t1.group(2)), peak=max(pk.values()) / 1048576, nsamp=len(rows), lowav=min(float(s["avail_GiB"]) for s in rows if s["avail_GiB"]))


def score(d, mut=""):
    ev, root = d["ev"], d["root"]
    lo, hi = root["bracket"]; rt = root["lam_lin"]; ecode = d["ecode"]; status = root["status"]
    secs = [r["sec"] for r in ev]; wall = root["sec"]; peak = d["peak"]
    lane = hms(d["t1"]) - hms(d["t_launch"])
    if lane < 0: lane += 86400
    if mut == "exit0": ecode, status = 0, "tol"
    if mut == "exit4": ecode, status = 4, "nonrobust"
    if mut == "sec_in": secs = [190] * len(secs)
    if mut == "sec_out": secs = [590] * len(secs)
    if mut == "wall_in": wall = 25 * 60
    if mut == "wall_out": wall = 70 * 60
    if mut == "rss_in": peak = 7.0
    if mut == "rss_out": peak = 11.0
    if mut == "lane_in": lane = 140 * 60
    if mut == "lane_out": lane = 300 * 60
    rt = dict(root_a=0.100, root_b=0.0888, root_c=0.050, root_d=0.040).get(mut, rt)
    L = []
    item = lambda name, pct, hit, val: L.append((name, pct, hit, val))
    item("secant exit 0 (tol)", 55, ecode == 0 and status == "tol", "exit %d, status %s, %d evaluations" % (ecode, status, root["n_eval"]))
    item("secant exit 4", 40, ecode == 4, "exit %d (%s)" % (ecode, root.get("why") or status))
    item("per evaluation in (150, 240) s at all of them", 60, all(150 < s < 240 for s in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
    item("run wall 15 to 45 min", 60, 15 * 60 <= wall <= 45 * 60, "%d s = %.1f min (%s to %s UTC)" % (wall, wall / 60.0, d["t0"], d["t1"]))
    item("peak RSS in (5.5, 8.0) GiB", 60, 5.5 < peak < 8.0, "%.3f GiB (60 s samples of the secant process, %d samples; lowest available %.1f GiB)" % (peak, d["nsamp"], d["lowav"]))
    item("the lane (launch to the secant exit line) 90 to 180 min", 60, 90 * 60 <= lane <= 180 * 60, "%d s = %.1f min (%s to %s UTC)" % (lane, lane / 60.0, d["t_launch"], d["t1"]))
    item("root above R0's 0.045968", 97, rt > R0, "root %+.8f, minus R0's %+.6f" % (rt, rt - R0))
    item("root in (0.09, 0.115) (t5's near 0.09-0.115)", 60, 0.09 < rt < 0.115, "root %+.8f" % rt)
    item("root in (0.0886, 0.1122) (t5's kappa^4 band from R2's bracket)", 50, 0.0886 < rt < 0.1122, "root %+.8f" % rt)
    return L, dict(rt=rt, lo=lo, hi=hi, ecode=ecode, status=status, wall=wall, lane=lane)


def controls(d):
    a, b, c = "root above R0's 0.045968", "root in (0.09, 0.115) (t5's near 0.09-0.115)", "root in (0.0886, 0.1122) (t5's kappa^4 band from R2's bracket)"
    names = {"exit0": {"secant exit 0 (tol)": True, "secant exit 4": False}, "exit4": {"secant exit 0 (tol)": False, "secant exit 4": True},
             "sec_in": {"per evaluation in (150, 240) s at all of them": True}, "sec_out": {"per evaluation in (150, 240) s at all of them": False},
             "wall_in": {"run wall 15 to 45 min": True}, "wall_out": {"run wall 15 to 45 min": False}, "rss_in": {"peak RSS in (5.5, 8.0) GiB": True}, "rss_out": {"peak RSS in (5.5, 8.0) GiB": False},
             "lane_in": {"the lane (launch to the secant exit line) 90 to 180 min": True}, "lane_out": {"the lane (launch to the secant exit line) 90 to 180 min": False},
             "root_a": {a: True, b: True, c: True}, "root_b": {a: True, b: False, c: True}, "root_c": {a: True, b: False, c: False}, "root_d": {a: False, b: False, c: False}}
    bad = 0
    for mut, w in names.items():
        got = {n: h for n, p, h, v in score(d, mut)[0]}
        ok = all(got[k] == v for k, v in w.items()); bad += (not ok)
        print("control --mutate=%s: %s (wanted %s, read %s)" % (mut, "ok" if ok else "FAILED", list(w.values()), [got[k] for k in w]))
    print("controls: %d of %d failed" % (bad, len(names)))
    return bad


def order(r):
    f = lambda p: (0.7 ** p - 0.5 ** p) / (0.5 ** p - 0.35 ** p) - r
    lo, hi = 0.5, 12.0
    if f(lo) * f(hi) > 0: return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)


def main():
    d = read_files()
    mut = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]; mut = mut[0] if mut else ""
    if "--controls" in sys.argv:
        sys.exit(1 if controls(d) else 0)
    L, x = score(d, mut); ev, root = d["ev"], d["root"]
    H = [i for i in L if i[2]]; M = [i for i in L if not i[2]]
    fmt = lambda i: "%s (%d%%): %s" % (i[0], i[1], i[3])
    rt = x["rt"]; d1 = rt - R0
    out = ["**the R1 secant and the root, scored** (secant/secant.jsonl, samples.csv, exits_r1.txt; `score_secant_r1.py`, controls `--controls`: %d mutations of exit, seconds, wall, RSS, lane and root that must flip their items either way). Secant %s to %s UTC, tol 5e-5, Rust block 12 with 4 threads, one process, **exit %d (%s)**, %d evaluations (the two ends included; interior points %s), **final robust bracket [%.8f, %.8f], width %.3e, signs %s, det-linear root %+.8f** (inside the bracket by position), Brent's last point %.8f; interior evaluations not robust: %s."
           % (14, d["t0"], d["t1"], x["ecode"], x["status"], root["n_eval"], ", ".join("%.8f" % r["lam"] for r in ev[2:]) or "none", x["lo"], x["hi"], x["hi"] - x["lo"], root["signs"], rt, root["lam_brent"],
              ", ".join("%.8f (dln %.3f)" % (r["lam"], r["dln"]) for r in ev if not r["robust"]) or "none")]
    d2 = [float(a.split("=")[1]) for a in sys.argv if a.startswith("--delta2=")]
    t = "**t5's quantities (arithmetic only, not a result):** delta_1 = root - 0.045968 = %+.6f." % d1
    if d2:
        r = d1 / (d2[0] - d1); p = order(r)
        t += " With delta_2 = %+.6f (R2's secant, from t5's record): r = delta_1/(delta_2 - delta_1) = %.3f, his bar [3.0, 4.6] (kappa^4 predicts 3.74): %s; the order p from (0.7^p - 0.5^p)/(0.5^p - 0.35^p) = r is %s." % (
            d2[0], r, "inside, kappa^4 confirmed by his rule" if 3.0 <= r <= 4.6 else "OUTSIDE (the order p is reported, not kappa^4)", "%.3f" % p if p is not None else "not in (0.5, 12)")
    else:
        t += " r needs delta_2 from R2's secant (t5's record; pass --delta2=X)."
    out.append(t)
    out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + ("; ".join("MISS " + fmt(i) for i in M) + ". " if M else "") + "(%d items: %d HIT, %d MISS; exit 0 and exit 4 exclude each other.)" % (len(L), len(H), len(M)))
    txt = "\n".join(out); print(txt)
    if "--write" in sys.argv and not mut and not STAND:
        stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
        open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " "))); print("written")


if __name__ == "__main__":
    main()
