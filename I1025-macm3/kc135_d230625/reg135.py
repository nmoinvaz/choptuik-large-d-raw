#!/usr/bin/env python3
"""reg135.py : arithmetic behind the registration of kc135_d230625/README.md (scenarios for lambda_1(k_c 135, D 23.0625), not a result): roots at D 23.0625
and zeros of k_c 95..127 from the files (kc127_leg/zero_arithmetic_127.txt, the secant summaries); scenarios by the ratio of the next step."""
import os, re, sys
sys.path.insert(0, os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda"))
import make_post_1125b as m
R = m.R
roots = {95: m.parse_sec(R + "kc_d23_secant/kc95L/secant_summary.txt")["root"], 103: m.parse_sec(R + "kc103_leg/point_D23.0625_summary.txt")["root"],
         111: m.parse_sec(R + "kc111_d230625/point_summary.txt")["root"], 119: m.parse_sec(R + "kc119_d230625/point_summary.txt")["root"], 127: m.parse_sec(R + "kc127_d230625/point_summary.txt")["root"]}
st = [roots[b] - roots[a] for a, b in ((95, 103), (103, 111), (111, 119), (119, 127))]
print("roots at D 23.0625:", " ".join("%d %+.8f" % (k, roots[k]) for k in sorted(roots)))
print("steps:", " ".join("%+.6f" % x for x in st), "ratios:", " ".join("%.4f" % (st[i + 1] / st[i]) for i in range(3)))
for r in (0.5, 0.6, 0.7, 0.8, 0.9):
    print("root-step ratio %.1f: k_c 135 root %+.6f" % (r, roots[127] + st[-1] * r))
z = {87: 22.97893, 95: 23.00808, 103: 23.03011, 111: 23.04627, 119: 23.05757, 127: 23.06750}
dz = [z[b] - z[a] for a, b in ((87, 95), (95, 103), (103, 111), (111, 119), (119, 127))]
sl = -0.72880
print("zeros (the posted table):", z, "steps", " ".join("%+.5f" % x for x in dz), "ratios", " ".join("%.4f" % (dz[i + 1] / dz[i]) for i in range(4)))
for r in (0.5, 0.6, 0.7, 0.8, 0.88):
    z135 = z[127] + dz[-1] * r
    print("zero-step ratio %.2f: zero of k_c 135 %.5f, root at D 23.0625 by the k_c 127 slope %.5f: %+.6f" % (r, z135, sl, sl * (23.0625 - z135)))
