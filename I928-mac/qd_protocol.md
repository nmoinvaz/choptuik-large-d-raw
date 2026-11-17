# The quad-double stage on the band: checks before it is used (#928)

Written 2026-11-17 14:10 UTC, before either run. The coordinator's terms are in the issue's comments.

The double-double error of Delta near the stop. Two double-double runs at one D differ in Delta by 3.4e-21 at
D 12.375 (one stalled at max |F| 1.1e-27, one converged at 6.7e-29) and by 2.7e-21 at D 12.46875
(`out/sm_records.jsonl`). The error quoted for a double-double Delta near the stop is 1e-20, three times the larger
difference, rounded up.

Check 1 (consistency). The quad-double Newton (`run_eta.py --qd --qd_jac dd`, the exact quad-double Jacobian) from
the converged double-double state at eta 0.3, D 12.375 (Delta 1.111899734008754743955872521, max |F| 6.7e-29).
Pass: the quad-double max |F| is at most 1e-28, and |Delta_qd - Delta_dd| <= 1e-20. A failure stops the route.

Check 2 (the stalled state). The same from the stalled state at D 12.5 (max |F| 8.1e-28), with the double-double
stage's tolerance at 3e-27 so that it hands over. Pass: the quad-double max |F| is at most 1e-28, and the
double-double residual of the result, its first two parts, is at most the stall's 8.1e-28.

Only if both pass does the chain continue in quad-double. The 1e-28 bound then applies to the quad-double residual
of those points, and the double-double chain's stop at D 12.46875 (eta 0.3) stays the record of where double-double
ends.
