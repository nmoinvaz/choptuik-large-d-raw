# I476-macm3: #178's discs around lambda = 1.14 at D 45.05, M 48, kf 21 on #443's converged background (inner node), with the lambda_phys control

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/476.
Raw output is not committed here while the raw repository's rewrite pause lasts.

State: I443-macm3/hp_data_after/modecount_state_D45.0507_M48_kf21_ct1e-150.npz (|F| 2.0e-17, series 6.4e-135 and 1.8e-33; in hp/data, loads with no refit). Cache: a copy of I443-macm3/data (the R 0.03 circle at 1.14 and the control), so the control is a replay of #443's.
Command (circles.cmd, caffeinate -is, nice 10, one thread), #178's discs: the original 1.11 R 0.12 (it winds 0 at kf 13 to 19 and +1 at kf 21 on the old layout), the halves 1.05 R 0.06 and 1.17 R 0.06 (old layout: 0 and +1), the quarter 1.20 R 0.03 (old: 0), and the control:
python3 hp/modecount_circle.py hp/data/states/up7_D45.0507.npz 1.11,0,0.12 1.05,0,0.06 1.17,0,0.06 1.20,0,0.03 2.056738610147195,0,0.1 --M=48 --kf=21 --centre_tol=1e-150 --fmax=1e-15 --n0=20 --tag=D45.0507_M48_kf21 --data=<raw>/I476-macm3/data
(The 1.14 R 0.03 circle is #443's.) Cost note from #178: the 1.11 circle's detrending point c - 2R = 0.87 is 0.0014 from lambda_g = 0.8714, so it needs more points.

Written before the run (the issue's). Each disc's winding with its mismatches and largest step; the control at +1 within 1e-6 of lambda_phys 2.056738610147195 (#443's: miss ~1e-11); the statement that no zero lies within the widest disc (1.11 R 0.12, which covers the real segment 0.99 to 1.23 where #170's sign change (1.0, 1.221) was), or its position.
A winding 0 in every disc says no zero in the union; a +1 gives a position with the circle's own estimate (a range, not a bound).

## Results

Exit 0 at 02:05:25 UTC (started 00:30 UTC; 142 lines in the cache, 90 new). All five circles 0 verification mismatches, 0 alias bisections, 20 to 28 points:
  1.11 R 0.12: winding 0 (25 points, largest step 0.374).  1.05 R 0.06: 0 (20, 0.050).  1.17 R 0.06: 0 (20, 0.016).  1.20 R 0.03: 0 (20, 0.003).  (1.14 R 0.03: 0 in #443, 0.005.)
  lambda_phys 2.056738610147195 R 0.1: +1, zero 2.0567386102 + 0.0000000000045i (estimate 6.3e-12), miss 8.1e-12 (replay of #443's circle).
