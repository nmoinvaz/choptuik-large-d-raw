#!/usr/bin/env python3
"""reg_d23125.py [--r135 X] : arithmetic behind the registration of kc135_d23125/README.md, from the files (not a result).
(1) the four regrids at D 23.0625 (k_c 103->111, 111->119, 119->127, 127->135): wall, peak RSS (60 s samples), steps, constraint, Delta shift.
(2) the roots of lambda_1 at D 23.0 and D 23.0625 by k_c, the steps in k_c at each D and their ratio.
(3) the k_c 127 roots at D 23.0625 and 23.125 and the k_c 135 root at D 23.0625 (--r135, default: the final root of kc135_d230625/point_summary.txt if it exists,
    else the scan's det-linear root, marked PROVISIONAL), and scenarios for the k_c 135 root at D 23.125 by (a) t5's rule (k_c 127 root at 23.125 plus the shift seen at 23.0625)
    and (b) the shift growing with D by a factor g, and by the slope of k_c 135 over the pair (slope magnitude below k_c 127's 0.7288 as the slopes fell with k_c)."""
import os, re, sys, csv
sys.path.insert(0, os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda"))
import make_post_1125b as m
R = m.R; K = R + "kc_d23_secant/"; P = m.parse_sec

def regrid(folder, exitsname):
    t = open(R + folder + "/regrid/regrid_summary.txt").read()
    wall = int(re.search(r"regrid exit 0, wall (\d+) s", open(R + folder + "/" + exitsname).read()).group(1))
    rss = max(int(r["rss_kB"]) for r in csv.DictReader(open(R + folder + "/regrid/regrid_samples.csv")) if r["rss_kB"]) / 1048576
    g = lambda pat: float(re.search(pat, t).group(1))
    return dict(wall=wall, rss=rss, steps=int(re.search(r"record: D \S+ \|F\| \S+ steps (\d+)", t).group(1)), shift=g(r"Delta shift (\S+),"), sr=g(r"steps ratio (\S+),"), cr=g(r"constraint ratio (\S+)"))

def main():
    r135 = None
    if "--r135" in sys.argv: r135 = float(sys.argv[sys.argv.index("--r135") + 1]); src = "given"
    elif os.path.exists(R + "kc135_d230625/point_summary.txt"):
        r135 = P(R + "kc135_d230625/point_summary.txt")["root"]; src = "the final root of kc135_d230625/point_summary.txt (det-linear)"
    else:
        t = open(R + "kc87_leg_lambda/23.0625_kc135/read_lower.txt").read()
        r135 = float(re.search(r"det-linear (\d\.\d+)", t).group(1)); src = "PROVISIONAL: the scan's det-linear root (read_lower.txt)"
    print("(1) the regrids at D 23.0625")
    rg = {k: regrid(f, e) for k, f, e in ((111, "kc111_d230625", "exits_kc111.txt"), (119, "kc119_d230625", "exits_kc119b.txt"), (127, "kc127_d230625", "exits_kc127.txt"), (135, "kc135_d230625", "exits_kc135.txt"))}
    for k, v in rg.items(): print("  k_c %d: wall %d s, peak RSS %.3f GiB, steps %d, steps ratio %.3f, constraint ratio %.3f, Delta shift %+.4e" % (k, v["wall"], v["rss"], v["steps"], v["sr"], v["cr"], v["shift"]))
    print("  leg point k_c 127 at D 23.125 (the source): steps 4182, constraint 1.654e-03, Delta 1.178026593320 (kc127_leg/states/l1kc127Lmacm3.jsonl)")
    print("  steps of the regrid result by the ratios 1.078 1.071 1.067 1.063 (last four): 4182 x 1.063 = %.1f; x 1.060 = %.1f; x 1.057 = %.1f" % (4182 * 1.063, 4182 * 1.060, 4182 * 1.057))
    print("(2) roots at D 23.0 and D 23.0625 by k_c")
    a = {95: (P(K + "kc95/secant_summary.txt")["root"], P(K + "kc95L/secant_summary.txt")["root"]), 103: (P(R + "kc103_d23/secant/secant_summary.txt")["root"], P(R + "kc103_leg/point_D23.0625_summary.txt")["root"]),
         111: (P(K + "kc111dh/secant_summary.txt")["root"], P(R + "kc111_d230625/point_summary.txt")["root"]), 119: (P(R + "kc119_d23/point_summary.txt")["root"], P(R + "kc119_d230625/point_summary.txt")["root"])}
    for k, (x, y) in a.items(): print("  k_c %d: D 23.0 %+.8f, D 23.0625 %+.8f, slope %+.5f" % (k, x, y, (y - x) / 0.0625))
    for k1, k2 in ((95, 103), (103, 111), (111, 119)):
        s0 = a[k2][0] - a[k1][0]; s1 = a[k2][1] - a[k1][1]
        print("  step k_c %d->%d: at D 23.0 %+.6f, at D 23.0625 %+.6f, ratio %.3f" % (k1, k2, s0, s1, s1 / s0))
    r127a = P(R + "kc127_d230625/point_summary.txt")["root"]; r127b = P(R + "kc127_leg/point_D23.125_summary.txt")["root"]
    s = r135 - r127a
    print("(3) k_c 127 roots: D 23.0625 %+.8f, D 23.125 %+.8f (slope %+.5f); k_c 135 root at D 23.0625 %+.8f (%s); shift 127->135 at D 23.0625: %+.6f" % (r127a, r127b, (r127b - r127a) / 0.0625, r135, src, s))
    print("    shifts 119->127 at D 23.0625: %+.6f (k_c 119 %+.8f, k_c 127 %+.8f)" % (r127a - a[119][1], a[119][1], r127a))
    for g in (1.0, 1.15, 1.3, 1.5, 1.7):
        print("  (a/b) shift at D 23.125 = %.2f x %+.6f: k_c 135 root at D 23.125 = %+.6f" % (g, s, r127b + g * s))
    for mm in (0.66, 0.68, 0.70, 0.72, 0.7288):
        print("  (c) slope magnitude of k_c 135 over D 23.0625 to 23.125 = %.4f: root = %+.6f (shift %+.6f, growth %.3f)" % (mm, r135 - mm * 0.0625, r135 - mm * 0.0625 - r127b, (r135 - mm * 0.0625 - r127b) / s))

if __name__ == "__main__":
    main()
