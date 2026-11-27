#!/usr/bin/env python3
"""arith_x.py [--mutate=rx] > arith_x_output.txt : the root of kc143_d23125x against the earlier k_c 143 root and the k_c 127, 135 roots at D 23.125, and the zero by the line through the two k_c 143 roots,
every number from the point summaries (kc143_d23125x/point_summary.txt, kc143_d23125/point_summary.txt, kc143_d230625, kc135_d23125, kc127_leg) and kc135_d230625, kc127_d230625 (the k_c 127 and 135 zeros by the same line).
Arithmetic only, not a result. --mutate=rx moves the x root by +0.001 (every difference built on it must move)."""
import re, sys
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
root = lambda p: float(re.search(r"det-linear root (-?[\d.]+)", open(R + p).read()).group(1))
rx = root("kc143_d23125x/point_summary.txt") + (0.001 if "--mutate=rx" in sys.argv else 0.0)
rb = root("kc143_d23125/point_summary.txt"); ra = root("kc143_d230625/point_summary.txt"); r135 = root("kc135_d23125/point_summary.txt"); r127 = root("kc127_leg/point_D23.125_summary.txt")
z = lambda a, b: 23.0625 - a * 0.0625 / (b - a)
z135 = z(root("kc135_d230625/point_summary.txt"), r135); z127 = z(root("kc127_d230625/point_summary.txt"), r127)
lz = lambda r: z(ra, r)
zx, zb = lz(rx), lz(rb)
print("D 23.125 roots: k_c 127 %+.8f, 135 %+.8f, 143 via 135 %+.8f, 143 direct from 127 %+.8f; the direct root minus the one via 135: %+.6f" % (r127, r135, rb, rx, rx - rb))
print("shifts of the root with k_c at D 23.125: 127 to 135 %+.6f; 135 to 143 via 135 %+.6f (%.3f times the first); 127 to 143 direct %+.6f, by the chain %+.6f (direct over chain %.3f); direct over twice the 127 to 135 shift %.3f; the direct root minus the k_c 135 root %+.6f (%.3f times the 127 to 135 shift)" % (
    r135 - r127, rb - r135, (rb - r135) / (r135 - r127), rx - r127, rb - r127, (rx - r127) / (rb - r127), (rx - r127) / (2 * (r135 - r127)), rx - r135, (rx - r135) / (r135 - r127)))
print("zero by the line through the D 23.0625 root %+.8f and the D 23.125 root: k_c 143 direct D %.5f, via 135 D %.5f; k_c 135 D %.5f, k_c 127 D %.5f; steps 127 to 135 %+.5f, 135 to 143 direct %+.5f (ratio %.4f), via 135 %+.5f (ratio %.4f); slope magnitude direct %.5f, via 135 %.5f" % (
    ra, zx, zb, z135, z127, z135 - z127, zx - z135, (zx - z135) / (z135 - z127), zb - z135, (zb - z135) / (z135 - z127), abs((rx - ra) / 0.0625), abs((rb - ra) / 0.0625)))
