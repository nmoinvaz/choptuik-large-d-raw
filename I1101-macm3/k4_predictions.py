#!/usr/bin/env python3
"""k4_predictions.py [--mutate=r1] > k4_predictions_output.txt : the roots at kappa 0.25 and 0.35 and at kappa -> 0 that the order p of an error root(kappa) = r_inf - c kappa^p predicts from R0 (kappa 0.7, 0.045968) and R1 (kappa 0.5, the secant root of point_summary.txt),
for p = 2, 3, 4 (t5's table of comment 7223316450 and his 0.111, 0.120, 0.133). Arithmetic only, not a result. --mutate=r1 moves the R1 root by +0.01 (every number must move)."""
import re, sys
r0, r1 = 0.045968, float(re.search(r"det-linear root (-?[\d.]+)", open("/Users/nathan/Source/choptuik-large-d-raw-903/I1101-macm3/point_summary.txt").read()).group(1)) + (0.01 if "--mutate=r1" in sys.argv else 0.0)
for p in (2, 3, 4):
    c = (r1 - r0) / (0.7 ** p - 0.5 ** p); rinf = r1 + c * 0.5 ** p
    print("order %d: root(kappa) = %.6f - %.6f kappa^%d; kappa 0.35 -> %.4f, kappa 0.25 -> %.4f, kappa -> 0 -> %.4f; E_root at kappa 0.7 %+.4f" % (p, rinf, c, p, rinf - c * 0.35 ** p, rinf - c * 0.25 ** p, rinf, rinf - r0))
