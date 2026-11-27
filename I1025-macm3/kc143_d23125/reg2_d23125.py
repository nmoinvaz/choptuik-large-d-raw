#!/usr/bin/env python3
"""reg2_d23125.py [--mutate=r1] : arithmetic behind the SECOND registration entry of kc143_d23125/README.md (written after the D 23.0625 secant of kc143_d230625 ended, before the regrid of this lane), from the files (not a result).
(1) the root of lambda_1(k_c 143, D 23.0625), r1, from kc143_d230625/secant/secant.jsonl; (2) the root at D 23.125 by r1 minus 0.0625 times a slope magnitude, the zero by the line through the two,
and the same by the shift route (the k_c 135 root at D 23.125 plus g times the D 23.0625 shift 135 -> 143); (3) the scan windows against these roots; (4) the regrid forecasts from the D 23.0625 regrid's ratios;
(5) the Rust timings. --mutate=r1 shifts r1 by +0.001 (a control: every root and zero below must move)."""
import json, re, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
rows = [json.loads(l) for l in open(R + "kc143_d230625/secant/secant.jsonl") if l.strip()]; root = [r for r in rows if r.get("kind") == "root"][-1]
r1 = root["lam_lin"] + (0.001 if "--mutate=r1" in sys.argv else 0.0)
reg = open(R + "kc143_d230625/reg_kc143_output.txt").read()
m = re.search(r"D 23\.125 roots: 127 (\S+), 135 (\S+);", reg); r127b, r135b = float(m.group(1).rstrip(",")), float(m.group(2).rstrip(","))
m0 = re.search(r"135 (\+0\.00939\d+)", reg); r135a = float(m0.group(1))
shift_a = r1 - r135a; shift_b135 = r135b - r127b; z135 = 23.07535
print("(1) r1 = lambda_1(k_c 143, D 23.0625) = %+.8f (bracket [%.8f, %.8f]); k_c 135 root there %+.8f, shift 135 -> 143 %+.8f; D 23.125: k_c 127 %+.8f, k_c 135 %+.8f, shift 127 -> 135 %+.6f (ratio to the D 23.0625 shift 127 -> 135 %.4f)"
      % (r1, root["bracket"][0], root["bracket"][1], r135a, shift_a, r127b, r135b, shift_b135, shift_b135 / (r135a - 0.00364182)))
print("(2) by the slope magnitude s over D 23.0625 to 23.125 (k_c 127 0.72880, k_c 135 0.73102): root(23.125) = r1 - 0.0625 s; zero by the line = 23.0625 + r1 / s")
for s in (0.7310, 0.7320, 0.7330, 0.7340, 0.7360, 0.7380, 0.7200, 0.7420):
    print("   s %.4f: root(23.125) %+.6f, zero %.5f, step from the k_c 135 zero %+.5f" % (s, r1 - 0.0625 * s, 23.0625 + r1 / s, 23.0625 + r1 / s - z135))
print("    by the shift route (the D 23.125 shift 135 -> 143 = g x the D 23.0625 shift of %+.6f; g 0.976 was the growth at 127 -> 135):" % shift_a)
for g in (0.90, 0.94, 0.976, 1.00, 1.05, 1.08, 0.88):
    rb = r135b + g * shift_a; s = (r1 - rb) / 0.0625
    print("   g %.3f: root(23.125) %+.6f, slope magnitude %.5f, zero %.5f" % (g, rb, s, 23.0625 + r1 / s))
for lo, hi in ((0.7310, 0.7360), (0.7209, 0.7421)):
    print("   slope magnitude in (%.4f, %.4f) <=> root in (%+.6f, %+.6f) <=> zero in (%.5f, %.5f)" % (lo, hi, r1 - 0.0625 * hi, r1 - 0.0625 * lo, 23.0625 + r1 / hi, 23.0625 + r1 / lo))
print("   t5's root -0.0319 +- 0.003 and the zero 23.0816 +- 0.003 (zero of his two roots by the line: %.5f)" % (23.0625 + r1 / ((r1 + 0.0319) / 0.0625)))
print("(3) scan window (-0.040, -0.035, -0.030, -0.025, -0.020 plus a repeat of -0.030): the read bracket for a root x is the pair of grid points around x")
for x in (-0.0300 - 0.0010, -0.0306, -0.0307, -0.0309, -0.0300, -0.0297, -0.0314):
    g = [-0.040, -0.035, -0.030, -0.025, -0.020]; b = [(g[i], g[i + 1]) for i in range(4) if g[i] < x < g[i + 1]]
    print("   root %+.4f: bracket %s, distance to the nearest grid point %.4f" % (x, b, min(abs(x - v) for v in g)))
m = re.search(r"k_c 135 D 23\.0625: wall (\d+) s, peak RSS (\S+) GiB, steps (\d+), steps ratio (\S+), constraint ratio (\S+), Delta shift (\S+)", reg)
print("(4) regrid forecasts for D 23.125 at k_c 143 from the D 23.0625 ratios (k_c 143 / k_c 135 at D 23.0625; the k_c 143 regrid: wall 5175 s, peak RSS 9.079 GiB, steps 4706, constraint ratio 0.617, Delta shift -9.0249e-06):")
w0, rs0, st0, sr0, cr0, ds0 = int(m.group(1)), float(m.group(2)), int(m.group(3)), float(m.group(4).rstrip(",")), float(m.group(5).rstrip(",")), float(m.group(6).rstrip(","))
mb = re.search(r"k_c 135 D 23\.125: wall (\d+) s, peak RSS (\S+) GiB, steps (\d+), steps ratio (\S+), constraint ratio (\S+), Delta shift (\S+), constraint (\S+)", reg)
wb, rsb, stb, srb, crb, dsb, cb = int(mb.group(1)), float(mb.group(2)), int(mb.group(3)), float(mb.group(4).rstrip(",")), float(mb.group(5).rstrip(",")), float(mb.group(6).rstrip(",")), float(mb.group(7))
print("   wall ratio 5175/%d = %.4f -> %.0f s; peak RSS ratio 9.079/%.3f = %.4f -> %.3f GiB; steps %d x 1.0594 = %.0f; constraint %.4e x 0.6174 = %.4e; Delta shift %+.4e x (9.0249e-06/%.4e = %.3f) = %+.4e"
      % (w0, 5175 / w0, wb * 5175 / w0, rs0, 9.079 / rs0, rsb * 9.079 / rs0, stb, stb * 1.0594, cb, cb * 0.6174, dsb, abs(ds0), 9.0249e-06 / abs(ds0), dsb * 9.0249e-06 / abs(ds0)))
print("(5) Rust timings (rust_b12/e2e, k_c 143, D 23.0625, lambda 0.015, 4 threads beside the secant): 344 s = 125 float64 + 211 block 12 + 9 dd_logdet, peak RSS 6.437 GiB; stored Python 1199 s; the scan of lane A 1191 to 1202 s (2 processes), the secant 841 to 1029 s")
print("    the scan: 3 rounds of 2 evaluations: block 12 with 8 threads at once on 8 cores (4 P + 4 E): block 12 x 1.0 to 1.6 -> evaluation %.0f to %.0f s, scan %.1f to %.1f min; the secant, 1 process: 5 or 6 evaluations of 290 to 400 s -> %.0f to %.0f min"
      % (125 + 211 + 9, 125 + 211 * 1.6 + 9, 3 * (125 + 211 + 9) / 60, 3 * (125 + 211 * 1.6 + 9) / 60, 5 * 290 / 60, 6 * 400 / 60))
