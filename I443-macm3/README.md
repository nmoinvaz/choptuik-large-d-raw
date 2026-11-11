# I443-macm3: D 45.05, M 48, kf 21 with the inner node (--centre_tol=1e-150): a background that passes the series gate and |F| <= 1e-15, then the R 0.03 circle at 1.14 with the lambda_phys control

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54 (the series gate of #265 and --centre_tol of #270). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/443 (was #264).
Raw output is not committed here while the raw repository's rewrite pause lasts.

Command (circles.cmd, caffeinate -is, nice 10, one thread; the coordinator's wording: the background with the inner node, then the circle at 1.14 with the control), as in #270 and #275:
python3 hp/modecount_circle.py hp/data/states/up7_D45.0507.npz 1.14,0,0.03 2.056738610147195,0,0.1 --M=48 --kf=21 --centre_tol=1e-150 --fmax=1e-15 --n0=20 --tag=D45.0507_M48_kf21 --data=<raw>/I443-macm3/data
The seed is M 32 native, so the setup resamples to M 48, fits the layout (a node at 0.15 where the centre series needs it) and re-converges (Newton, then Levenberg-Marquardt; #254's fit took 1716 s). No D 45 M 48 state is in hp/data at the start (hp_data_before_all.txt). The control is #178's (2.057, R 0.1) at lambda_phys 2.056738610147195.

Written before the run (the issue's and the coordinator's). Acceptance: a background with both series <= 1e-15 on the solution and |F| <= 1e-15 (the setup refuses otherwise, #265), or a report of why none is reached (#254's refit reached |F| 1.4e-16, centre 4.6e-149, horizon 1.2e-32, and its solve stalled there with Delta -1.4e-10 from the unfitted layout).
The R 0.03 circle at 1.14 winds +1 or 0 on it, with the lambda_phys control winding +1. If the background converges, #417's strip circles follow on it, under #417. #178's reading at kf 21 on the unconverged layout: R 0.03 at 1.14 wound +1 (29 points, largest step 0.376), R 0.03 at 1.20 wound 0.
Estimates are ranges, not bounds.

## Results

Exit 0 at 22:10:52 UTC (started 21:04 UTC; the setup refit took part of it). Setup: the centre series at x = 0.3 of the plain layout truncated at 3.3e-73 as resampled (ratio 0.668), nodes [0.15, 0.3, 0.4, 0.5, 0.6, 0.7]; |F| 3.3e-09 in the layout, 3.2e-09 after Newton, 2.0e-17 after Levenberg-Marquardt (saved modecount_state_D45.0507_M48_kf21_ct1e-150.npz, in hp_data_after/);
series on the solution: centre 6.4e-135 (ratio 0.486 at 0.15), horizon 1.8e-33 (ratio 0.463 at 0.3): both under 1e-15, and |F| 2.0e-17 under 1e-15: the background passes.
Circles: R 0.03 at 1.14: winding 0 (20 points, largest step 0.005 rad, 0 mismatches, 0 alias bisections). lambda_phys 2.056738610147195 (R 0.1): winding +1, zero 2.056739 +0i (estimate 6.3e-12), 28 points, largest step 0.348, 0 mismatches.
