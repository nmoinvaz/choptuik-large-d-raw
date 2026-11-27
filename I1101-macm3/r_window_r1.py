#!/usr/bin/env python3
"""r_window_r1.py [--mutate=root] > r_window_r1_output.txt : t5's ratio r = delta_1/(delta_2 - delta_1) (#1101 comment 7220957360) turned around: with delta_1 = root(R1) - 0.045968 from point_summary.txt, the root of R2 that gives r = 3.0, 3.74 (kappa^4)
and 4.6, i.e. the window in which his bar [3.0, 4.6] confirms kappa^4, and the order p of (0.7^p - 0.5^p)/(0.5^p - 0.35^p) = r for a few roots of R2. Arithmetic only, not a result: R2's secant root is not known to me when this is written.
--mutate=root moves the R1 root by +0.01 (every number must move)."""
import re, sys
R0 = 0.045968
r1 = float(re.search(r"det-linear root (-?[\d.]+)", open("/Users/nathan/Source/choptuik-large-d-raw-903/I1101-macm3/point_summary.txt").read()).group(1)) + (0.01 if "--mutate=root" in sys.argv else 0.0)
d1 = r1 - R0
ratio = lambda p: (0.7 ** p - 0.5 ** p) / (0.5 ** p - 0.35 ** p)
print("R1 root %+.8f, delta_1 = root - 0.045968 = %+.6f" % (r1, d1))
for r in (3.0, 3.74, 4.6): print("r = %.2f: delta_2 = %+.6f, root(R2) = %.6f" % (r, d1 * (1 + 1 / r), R0 + d1 * (1 + 1 / r)))
print("so his bar [3.0, 4.6] holds when the root of R2 lies in [%.6f, %.6f] (kappa^4, r = 3.74, at %.6f)" % (R0 + d1 * (1 + 1 / 4.6), R0 + d1 * (1 + 1 / 3.0), R0 + d1 * (1 + 1 / 3.74)))
for p in (2.0, 3.0, 4.0, 5.0, 6.0): print("p = %.0f: r = %.3f, root(R2) = %.6f" % (p, ratio(p), R0 + d1 * (1 + 1 / ratio(p))))
