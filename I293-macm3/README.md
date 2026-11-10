# I293-macm3: D 58.01's boxes counted at M 40, kf 23 (fixed left column), then the moments on any box that winds

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main bfe5fd54.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/293. Beside I251, I273, I285, I290 and I292.

Command (count.cmd, caffeinate -is, nice 10, one thread): the issue's, as written. #286's M 40 state (I286-macm3/hp_data_after/, sha256 in state_sha256.txt) is copied into
hp/data first, so the setup loads it with no refit; a Newton or LM line in count.log means a refit and is reported. The cache starts empty (I286's circle cache is not copied).
Then hp/modecount_moment.py on each box that winds, as in #249 (--wtol=1e-4 for the strip).

Written before the run. Stop: setup |F| above 1e-15 or a refit; then report and stop. Table: the boxes' windings with both mismatch counts per edge, beside #249's M 48 row at D 58.0060
(B0 0, U0 +1, B1a +4, B1b +4, B1c 0, B1 +8, U +1, full +10). Acceptance: 0 last-pass mismatches on every edge, or the edges that have them named; the extras at M 40 are absent from every box,
present in the boxes of M 48, or present elsewhere with their moment positions. Estimates and spreads are ranges, not bounds.

## Results

Count exit 0 at 11:10:41 UTC (started 07:27 UTC; 604 determinants, all new). The state loaded with no refit (|F| 1.7e-19). 14 edges, mismatch 0 in any pass and 0 in the last pass on all.
wind(g) at M 40: B0 0, U0 0, B1a +8, B1b 0, B1c 0, B1 +8, U +8, full +24. #249's M 48 row: 0, +1, +4, +4, 0, +8, +1, +10. Moments (--wtol=1e-4, no new determinant, 604 lines before and after):
  B1a (4 upper-half zeros, spreads 0.03 to 0.21: search positions): 0.45204 +0.52250i, 0.72233 +0.58732i, 1.12654 +0.96799i, 1.48913 +1.28208i.
  U (8 zeros, spreads 0.5 to 0.75: search positions only): -0.335+3.955i, -0.231+2.815i, 0.264+4.940i, 0.645+2.076i, 1.365+5.277i, 1.592+2.087i, 2.040+3.225i, 2.062+4.700i.
