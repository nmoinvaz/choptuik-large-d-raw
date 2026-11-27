#!/usr/bin/env python3
"""score_secant_kmm.py [--write] [--controls] [--mutate=NAME] : scores the K4 secant (R1's state with --kappa_mm=0.25, tol 5e-5, Rust block 12) and its root against the registration of the section "The fourth kappa point" in README.md and t5's three
numbers (0.111 = kappa^4, 0.120 = kappa^3, 0.133 = kappa^2; #1101 comment 7223316450), every number from the files: kmm025/secant/secant.jsonl, kmm025/secant/samples.csv, kmm025/exits_kmm.txt.
It also prints the order p of root(kappa) = r_inf - c kappa^p from the three roots R0 (kappa 0.7, 0.045968), R1 (kappa 0.5, 0.09500769) and this one at kappa_mm 0.25 (arithmetic only, not a result: the points are not three solves of one kind).
--controls runs mutations that must flip their items whatever the data say (exit 1 otherwise):
  exit0 / exit4 : the secant exit set to 0 (status tol) / 4;  sec_in / sec_out : every evaluation 450 s / 800 s : the (330, 560) s item HIT / MISS;  wall_in / wall_out : the run wall 60 / 130 min : the 40 to 100 min item HIT / MISS
  rss_in / rss_out : the peak RSS 8.0 / 12.0 GiB : the (6.0, 10.0) GiB item HIT / MISS;  lane_in / lane_out : the lane 200 / 350 min : the 150 to 260 min item HIT / MISS
  root_a / root_b / root_c / root_d / root_e : the root 0.133 / 0.120 / 0.111 / 0.150 / 0.090 : exactly the items of the kappa^2 band (0.1265, 0.14), the kappa^3 band (0.1155, 0.1265), the kappa^4 band (0.105, 0.1155), 'none of the three' (below 0.105 or above 0.14) and 'above 0.095008' read as written
Tail sums are arithmetic only, not a result. Read-only except for --write."""
import csv, json, math, re, subprocess, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/"
STAND = "--stand-in" in sys.argv   # reads the R1 lane's files (I1101-macm3/secant, exits_r1.txt) to test the script; never writes
D = R + ("I1101-macm3/" if STAND else "I1101-macm3/kmm025/")
LAB = "I1101 R1" if STAND else "I1101 K4"; EXF = "exits_r1.txt" if STAND else "exits_kmm.txt"
R0 = 0.045968; R1 = 0.09500769
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
    if mut == "sec_in": secs = [450] * len(secs)
    if mut == "sec_out": secs = [800] * len(secs)
    if mut == "wall_in": wall = 60 * 60
    if mut == "wall_out": wall = 130 * 60
    if mut == "rss_in": peak = 8.0
    if mut == "rss_out": peak = 11.0
    if mut == "lane_in": lane = 200 * 60
    if mut == "lane_out": lane = 350 * 60
    rt = dict(root_a=0.133, root_b=0.120, root_c=0.111, root_d=0.150, root_e=0.090).get(mut, rt)
    L = []
    item = lambda name, pct, hit, val: L.append((name, pct, hit, val))
    item("secant exit 0 (tol)", 55, ecode == 0 and status == "tol", "exit %d, status %s, %d evaluations" % (ecode, status, root["n_eval"]))
    item("secant exit 4", 40, ecode == 4, "exit %d (%s)" % (ecode, root.get("why") or status))
    item("per evaluation in (330, 560) s at all of them", 60, all(330 < s_ < 560 for s_ in secs), "%s s, mean %.0f s" % (", ".join(map(str, secs)), sum(secs) / len(secs)))
    item("run wall 40 to 100 min", 60, 40 * 60 <= wall <= 100 * 60, "%d s = %.1f min (%s to %s UTC)" % (wall, wall / 60.0, d["t0"], d["t1"]))
    item("peak RSS in (6.0, 10.0) GiB", 55, 6.0 < peak < 10.0, "%.3f GiB (60 s samples of the secant process, %d samples; lowest available %.1f GiB)" % (peak, d["nsamp"], d["lowav"]))
    item("the lane (launch to the secant exit line) 150 to 260 min", 60, 150 * 60 <= lane <= 260 * 60, "%d s = %.1f min (%s to %s UTC)" % (lane, lane / 60.0, d["t_launch"], d["t1"]))
    item("root above 0.1265 (nearest of t5's three: 0.133, kappa^2)", 40, rt > 0.1265, "root %+.8f, minus 0.133 %+.5f" % (rt, rt - 0.133))
    item("root in (0.1155, 0.1265) (nearest 0.120, kappa^3)", 30, 0.1155 < rt < 0.1265, "root %+.8f, minus 0.120 %+.5f" % (rt, rt - 0.120))
    item("root in (0.105, 0.1155) (nearest 0.111, kappa^4)", 20, 0.105 < rt < 0.1155, "root %+.8f, minus 0.111 %+.5f" % (rt, rt - 0.111))
    item("root below 0.105 or above 0.14 (none of the three)", 10, rt < 0.105 or rt > 0.14, "root %+.8f" % rt)
    item("root within 0.003 of one of the three", 45, min(abs(rt - h) for h in (0.111, 0.120, 0.133)) < 0.003, "root %+.8f, distances %.5f, %.5f, %.5f" % (rt, abs(rt - 0.111), abs(rt - 0.120), abs(rt - 0.133)))
    item("root above R1's 0.095008", 99, rt > 0.095008, "root %+.8f" % rt)
    return L, dict(rt=rt, lo=lo, hi=hi, ecode=ecode, status=status, wall=wall, lane=lane)


def controls(d):
    k2, k3, k4, nn, ab = "root above 0.1265 (nearest of t5's three: 0.133, kappa^2)", "root in (0.1155, 0.1265) (nearest 0.120, kappa^3)", "root in (0.105, 0.1155) (nearest 0.111, kappa^4)", "root below 0.105 or above 0.14 (none of the three)", "root above R1's 0.095008"
    names = {"exit0": {"secant exit 0 (tol)": True, "secant exit 4": False}, "exit4": {"secant exit 0 (tol)": False, "secant exit 4": True},
             "sec_in": {"per evaluation in (330, 560) s at all of them": True}, "sec_out": {"per evaluation in (330, 560) s at all of them": False},
             "wall_in": {"run wall 40 to 100 min": True}, "wall_out": {"run wall 40 to 100 min": False}, "rss_in": {"peak RSS in (6.0, 10.0) GiB": True}, "rss_out": {"peak RSS in (6.0, 10.0) GiB": False},
             "lane_in": {"the lane (launch to the secant exit line) 150 to 260 min": True}, "lane_out": {"the lane (launch to the secant exit line) 150 to 260 min": False},
             "root_a": {k2: True, k3: False, k4: False, nn: False, ab: True}, "root_b": {k2: False, k3: True, k4: False, nn: False, ab: True}, "root_c": {k2: False, k3: False, k4: True, nn: False, ab: True},
             "root_d": {k2: True, k3: False, k4: False, nn: True, ab: True}, "root_e": {k2: False, k3: False, k4: False, nn: True, ab: False}}
    bad = 0
    for mut, w in names.items():
        got = {n: h for n, p, h, v in score(d, mut)[0]}
        ok = all(got[k] == v for k, v in w.items()); bad += (not ok)
        print("control --mutate=%s: %s (wanted %s, read %s)" % (mut, "ok" if ok else "FAILED", list(w.values()), [got[k] for k in w]))
    print("controls: %d of %d failed" % (bad, len(names)))
    return bad


def order3(rt):
    """the order p of root(kappa) = r_inf - c kappa^p through (0.7, R0), (0.5, R1), (0.25, rt): (rt - R1)/(R1 - R0) = (0.5^p - 0.25^p)/(0.7^p - 0.5^p), decreasing in p"""
    g = lambda p: (0.5 ** p - 0.25 ** p) / (0.7 ** p - 0.5 ** p) - (rt - R1) / (R1 - R0)
    lo, hi = 0.2, 14.0
    if g(lo) * g(hi) > 0: return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(lo) * g(mid) <= 0: hi = mid
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
    out = ["**the K4 secant (kappa_mm 0.25) and the root, scored** (secant/secant.jsonl, samples.csv, exits_kmm.txt; `score_secant_kmm.py`, controls `--controls`: %d mutations of exit, seconds, wall, RSS, lane and root that must flip their items either way). Secant %s to %s UTC, tol 5e-5, Rust block 12 with 4 threads, one process, **exit %d (%s)**, %d evaluations (the two ends included; interior points %s), **final robust bracket [%.8f, %.8f], width %.3e, signs %s, det-linear root %+.8f** (inside the bracket by position), Brent's last point %.8f; interior evaluations not robust: %s."
           % (15, d["t0"], d["t1"], x["ecode"], x["status"], root["n_eval"], ", ".join("%.8f" % r["lam"] for r in ev[2:]) or "none", x["lo"], x["hi"], x["hi"] - x["lo"], root["signs"], rt, root["lam_brent"],
              ", ".join("%.8f (dln %.3f)" % (r["lam"], r["dln"]) for r in ev if not r["robust"]) or "none")]
    p = order3(rt)
    t = "**Against t5's three numbers (arithmetic only, not a result):** the root %+.8f minus 0.111 (kappa^4) is %+.5f, minus 0.120 (kappa^3) %+.5f, minus 0.133 (kappa^2) %+.5f; nearest %s. The order p of root = r_inf - c kappa^p through R0 (0.7, 0.045968), R1 (0.5, 0.09500769) and this root (0.25) is %s%s." % (
        rt, rt - 0.111, rt - 0.120, rt - 0.133, min([("0.111 (kappa^4)", 0.111), ("0.120 (kappa^3)", 0.120), ("0.133 (kappa^2)", 0.133)], key=lambda h: abs(rt - h[1]))[0],
        "%.3f" % p if p is not None else "not in (0.2, 14)", (", r_inf = %.5f" % (R1 + (R1 - R0) * 0.5 ** p / (0.7 ** p - 0.5 ** p))) if p is not None else "")
    out.append(t)
    out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + ("; ".join("MISS " + fmt(i) for i in M) + ". " if M else "") + "(%d items: %d HIT, %d MISS; exit 0 and exit 4 exclude each other.)" % (len(L), len(H), len(M)))
    txt = "\n".join(out); print(txt)
    if "--write" in sys.argv and not mut and not STAND:
        stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
        open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " "))); print("written")


if __name__ == "__main__":
    main()
