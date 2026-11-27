#!/usr/bin/env python3
"""reg_kc143.py : arithmetic behind the registrations of kc143_d230625/README.md and kc143_d23125/README.md, from the files (not a result).
(1) the regrids by k_c (111, 119, 127, 135 at D 23.0625; 135 at D 23.125): wall, peak RSS, steps ratio, constraint, Delta shift.
(2) the roots of lambda_1 at D 23.0625 by k_c (95..135), the steps, their ratios; at D 23.125 for k_c 127 and 135.
(3) the scan and secant times and memory of k_c 127 and 135.
(4) scenarios for the k_c 143 roots by the ratio of the shift, and the zero by the line through the two."""
import csv, json, os, re, sys
sys.path.insert(0, os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc135_d23125"))
sys.path.insert(0, os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda"))
import reg_d23125 as rg
import make_post_1126 as p
R = p.R; P = p.parse_sec; lz = p.lz

def secs(path):
    t = open(path).read()
    return [int(x) for x in re.findall(r"robust (?:True|False) (\d+) s", t)]

def main():
    print("(1) regrids")
    for lab, f, e in (("k_c 111 D 23.0625", "kc111_d230625", "exits_kc111.txt"), ("k_c 119 D 23.0625", "kc119_d230625", "exits_kc119b.txt"), ("k_c 127 D 23.0625", "kc127_d230625", "exits_kc127.txt"),
                      ("k_c 135 D 23.0625", "kc135_d230625", "exits_kc135.txt"), ("k_c 135 D 23.125", "kc135_d23125", "exits_kc135.txt")):
        v = rg.regrid(f, e)
        rec = [json.loads(l) for l in open(R + f + "/in/" + {"kc111_d230625": "l1kc111macm3d230625.jsonl", "kc119_d230625": "l1kc119macm3d230625.jsonl", "kc127_d230625": "l1kc127macm3d230625.jsonl", "kc135_d230625": "l1kc135macm3d230625.jsonl", "kc135_d23125": "l1kc135macm3d23125.jsonl"}[f]) if l.strip()][-1] if os.path.exists(R + f + "/in") else None
        print("  %s: wall %d s, peak RSS %.3f GiB, steps %d, steps ratio %.3f, constraint ratio %.3f, Delta shift %+.4e%s" % (lab, v["wall"], v["rss"], v["steps"], v["sr"], v["cr"], v["shift"], (", constraint %.4e" % rec["constraint"]) if rec else ""))
    print("(2) roots")
    K = R + "kc_d23_secant/"
    r = {95: P(K + "kc95L/secant_summary.txt")["root"], 103: P(R + "kc103_leg/point_D23.0625_summary.txt")["root"], 111: P(R + "kc111_d230625/point_summary.txt")["root"], 119: P(R + "kc119_d230625/point_summary.txt")["root"],
         127: P(R + "kc127_d230625/point_summary.txt")["root"], 135: P(R + "kc135_d230625/point_summary.txt")["root"]}
    ks = sorted(r); st = [r[ks[i + 1]] - r[ks[i]] for i in range(5)]
    print("  D 23.0625 roots: " + ", ".join("%d %+.8f" % (k, r[k]) for k in ks))
    print("  steps in k_c: " + ", ".join("%+.6f" % x for x in st) + "; ratios " + ", ".join("%.4f" % (st[i + 1] / st[i]) for i in range(4)))
    r127b = P(R + "kc127_leg/point_D23.125_summary.txt")["root"]; r135b = P(R + "kc135_d23125/point_summary.txt")["root"]
    s0 = r[135] - r[127]; s1 = r135b - r127b
    print("  D 23.125 roots: 127 %+.8f, 135 %+.8f; shift 127->135 %+.6f (D 23.0625: %+.6f), growth %.4f" % (r127b, r135b, s1, s0, s1 / s0))
    sl = {127: (r127b - r[127]) / 0.0625, 135: (r135b - r[135]) / 0.0625}
    print("  slopes over 23.0625-23.125: 127 %+.5f, 135 %+.5f (rise of the size %.5f)" % (sl[127], sl[135], abs(sl[135]) - abs(sl[127])))
    z127 = lz(23.0625, r[127], 23.125, r127b); z135 = lz(23.0625, r[135], 23.125, r135b)
    print("  zeros by the line: 127 %.5f, 135 %.5f, step %+.5f; earlier zero steps +0.02915 +0.02203 +0.01616 +0.01130 +0.00993 +0.00785 (ratios .7556 .7334 .6997 .8782 .7907)" % (z127, z135, z135 - z127))
    print("(3) scan and secant times")
    for lab, d in (("k_c 135 D 23.0625", "23.0625_kc135/scan/scan_D23.0625_1025.jsonl"), ("k_c 135 D 23.125", "23.125_kc135/scan/scan_D23.125_1025.jsonl"), ("k_c 127 D 23.125", "23.125_kc127/scan/scan_D23.125_1025.jsonl")):
        f = R + "kc87_leg_lambda/" + d
        if os.path.exists(f):
            sc = [json.loads(l) for l in open(f)]
            print("  scan %s: %d evaluations, seconds %s" % (lab, len(sc), sorted(x["sec"] for x in sc)))
    for lab, f in (("k_c 127 D 23.0625", "kc127_d230625/point_summary.txt"), ("k_c 127 D 23.125", "kc127_leg/point_D23.125_summary.txt"), ("k_c 135 D 23.0625", "kc135_d230625/point_summary.txt"), ("k_c 135 D 23.125", "kc135_d23125/point_summary.txt")):
        t = open(R + f).read(); m = re.search(r"secant memory: \d+ samples, lowest available (\S+) GiB, peak RSS (\S+) GiB", t); w = re.search(r"run wall (\d+) s", t)
        print("  secant %s: evaluation seconds %s, run wall %s s, peak RSS %s GiB" % (lab, secs(R + f), w.group(1), m.group(2) if m else "?"))
    print("(4) scenarios for the k_c 143 roots: shift = ratio x the last shift (D 23.0625: %+.6f; D 23.125: %+.6f x growth g of the shift with D, 0.976 at 127 -> 135)" % (s0, s1))
    for rr in (0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0):
        a = r[135] + rr * s0; b = r135b + rr * s1
        print("  ratio %.2f: root(23.0625) %+.6f, root(23.125) %+.6f, slope %+.5f, zero by the line %.5f" % (rr, a, b, (b - a) / 0.0625, lz(23.0625, a, 23.125, b)))
    for g in (0.9, 0.976, 1.05):
        a = r[135] + 0.8 * s0; b = r135b + 0.8 * s0 * g
        print("  ratio 0.80, growth %.3f (D 23.125 shift = 0.80 x %.6f x g): root(23.125) %+.6f, zero by the line %.5f" % (g, s0, b, lz(23.0625, a, 23.125, b)))
    print("  t5's: root(23.0625) +0.0139 +- 0.003, root(23.125) -0.0319 +- 0.003: zero by the line %.5f (slope %+.5f)" % (lz(23.0625, 0.0139, 23.125, -0.0319), (-0.0319 - 0.0139) / 0.0625))

if __name__ == "__main__":
    main()
