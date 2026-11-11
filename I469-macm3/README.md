# I469-macm3: circles on the eight strip positions of #293 at D 58.01, M 40, kf 23, with the lambda_phys control

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/469.
Raw output is not committed here while the raw repository's rewrite pause lasts.

State: #286's M 40 state (I286-macm3/hp_data_after, sha256 in state_sha256.txt; in hp/data, loads with no refit). The cache is a copy of I464-macm3/data (146 lines: the lambda_phys control and the four B1a circles), so the control is a replay of #464's.

Choice between the issue's two options (R 0.5 circles or a second moment pass on sub-boxes): hp/modecount_moment.py takes only the named boxes (B0, U0, B1a, ..., U), not sub-boxes, so R 0.5 circles. A circle of R 0.5 would take in the candidate pole at (2.0502, 3.4611) for the position
2.03995 +3.22483i (0.24 away), and the winding of det M counts a pole as -1; so that one circle has R 0.18, and a winding 0 there is not conclusive (the moment's spread is 0.75). The other seven positions are 0.58 or more from every candidate pole
(the candidates lie at Im 3.4611, Re -0.6346, 0.2603, 1.1552, 2.0502, 2.9451, 3.84, 4.7349 ...), so R 0.5 holds no pole. Three moment positions lie outside the strip U (Re 0.124 to 6.077, Im 1.731 to 5.192): -0.335 +3.955i, -0.231 +2.815i (Re < 0.124) and 1.365 +5.277i (Im > 5.192);
a circle there may hold a zero of U or not.

Command (circles.cmd, caffeinate -is, nice 10, one thread): hp/modecount_circle.py on hp/data/states/up12_D58.0060.npz, --M=40 --kf=23 --n0=20 --fmax=1e-15 --tag=D58.0060_M40_kf23 --data=<raw>/I469-macm3/data: the control 2.045529761477777 R 0.2 first, then
-0.33517,3.95460,0.5  -0.23129,2.81545,0.5  0.26435,4.94000,0.5  0.64532,2.07622,0.5  1.36483,5.27729,0.5  1.59158,2.08663,0.5  2.03995,3.22483,0.18  2.06249,4.69952,0.5.

Written before the run (the issue's). Each circle's winding with its mismatches; a zero within its estimate where it winds +1; the windings summed against the strip's +8 (a sum is read only with overlaps and the circles outside the strip named: circles of R 0.5 at
0.645 +2.076i and 1.592 +2.087i overlap slightly); the control +1 within 1e-6 of lambda_phys. Estimates are ranges, not bounds.

## Results

Exit 0 at 22:16:23 UTC (started 19:37 UTC; 479 lines in the cache: 146 copied from I464, 333 new). All circles 0 verification mismatches. The control and the eight:
  lambda_phys 2.045529761478 (R 0.2): +1, zero 2.0455297798 +0.0000000047i, estimate 2.6e-07, miss 1.9e-08.
  -0.33517 +3.95460i (R 0.5): +1, zero -0.221981 +3.548672i (estimate 2.0e-02), 38 points, 5 alias bisections, largest step 0.378.   -0.23129 +2.81545i: 0 (37 points, 10 alias bisections, 0.346).   0.26435 +4.94000i: 0 (24, 0, 0.327).   0.64532 +2.07622i: 0 (28, 0, 0.390).
  1.36483 +5.27729i (R 0.5): +1, zero 1.578462 +4.861791i (estimate 2.0e-02), 67 points, 17 alias bisections, 0.383.   1.59158 +2.08663i: +1, zero 1.371671 +2.308560i (estimate 8.5e-04), 35 points, 0 alias bisections, 0.386.
  2.03995 +3.22483i (R 0.18): 0 (22 points, 0.374).   2.06249 +4.69952i (R 0.5): 0 (66 points, 27 alias bisections, 0.380).
Sum of windings 3 (strip U needs 8; the zero at -0.222 +3.549i lies at Re < aLL = -0.096, outside U and U0, so 2 are in U).
