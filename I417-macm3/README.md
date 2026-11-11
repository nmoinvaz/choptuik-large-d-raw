# I417-macm3: the strip zero of D 45.05's kf 21 M 48 count (1.687 < |Im lambda| < 5.061), by moment and circles

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/417 (was #192).
Raw output is not committed here while the raw repository's rewrite pause lasts.

Inputs: I170-macm3 (the count at kf 21, tag D45.0507_M48_kf21, 129 cached determinants, copied to data/; its box U has wind(g) +1: the one zero of the strip) and its re-converged state (hp_data_after/, sha256 in state_sha256.txt, copied into hp/data so the setup loads it with no refit).
The issue gives no command ("circles and moments as in #169"); the commands here are the ones used in #249, #293 and #286, with this count's tag.
1. Moment (no new determinant): python3 hp/modecount_moment.py D45.0507_M48_kf21 hp/data/states/up7_D45.0507.npz U --wtol=1e-4 --data=<raw>/I417-macm3/data --out=<raw>/I417-macm3/moments_U.json
2. Circles (circles.cmd, caffeinate -is, nice 10, one thread): python3 hp/modecount_circle.py hp/data/states/up7_D45.0507.npz <moment>,0.15 <conjugate>,0.15 2.056738610147195,0,0.1 --M=48 --kf=21 --n0=20 --fmax=1e-15 --tag=D45.0507_M48_kf21 --data=<raw>/I417-macm3/data

Written before the run (the issue's). Each zero located inside a circle of winding +1 with 0 verification mismatches, and compared with the copies of the real-axis zero 1.14 (#178) at 1.14 + 2 i k omega: omega = 2 pi / Delta = 3.374 here (y1 = omega/2 = 1.687, y2 = 1.5 omega = 5.061), so the copies for k = +-1 lie at Im +-6.75, outside the strip.
The control: the lambda_phys circle (2.056738610147195, R 0.1) winds +1. Estimates and spreads are ranges, not bounds.

## Results

Moment of U (exit 0, no new determinant): winding of g +1.000000, 1 zero of g at 3.96403 +1.81547i, spread 2.2e-02. It is 0.13 from the strip's lower edge (Im 1.687).


Continuation on the converged layout (coordinator 21:03 UTC: #443 first; if its background converges, #417's strip circles follow on it). #443 converged (I443-macm3: |F| 2.0e-17, series 6.4e-135 and 1.8e-33; its state in I443-macm3/hp_data_after, in hp/data as modecount_state_D45.0507_M48_kf21_ct1e-150.npz), and the 1.14 circle wound 0 there. The strip zero of the old layout (3.96403 +1.81547i) cannot be assumed on the new layout, so the count of #170 is repeated on it first,
then the moment and the circles:
1. python3 hp/modecount_wind.py hp/data/states/up7_D45.0507.npz --M=48 --kf=21 --centre_tol=1e-150 --h0=0.6 --lam=2.056738610147195 --fmax=1e-15 --tag=D45.0507_M48_kf21 --data=<raw>/I417-macm3/data_ct   (#170's count.cmd with --centre_tol; cache empty)
2. python3 hp/modecount_moment.py D45.0507_M48_kf21 hp/data/states/up7_D45.0507.npz U --wtol=1e-4 --data=<raw>/I417-macm3/data_ct --out=...   (if box U winds)
3. circles on the zeros found, with the lambda_phys control (R 0.1).
Written before: the strip zero is "found" only if box U winds +1 on this layout and a +1 circle holds its moment position with 0 mismatches; if U winds 0 the zero of the old layout is absent here, as the 1.14 zero was.
Count on the converged layout (count_ct.cmd): exit 0 at 01:48:53 UTC (started 22:11 UTC; 80 determinants, all new). The state loaded with no refit (|F| 2.0e-17; series centre 6.4e-135, ratio 0.486 at 0.15; horizon 1.8e-33). 14 edges, 81 points, mismatch 0 in any pass and 0 in the last pass.
wind(g): B0 0, U0 0, B1a 0, B1b 0, B1c 0, B1 0, U 0, full 0. Expected zeros inside: B0 1 (0), B1a 1 (lambda_g 0.8714), B1b 1 (lambda_phys 2.0567); winding of det M 1, 0, 1, 1, 0, 2, -7, -12. Largest phase step 0.390 (U0, U, full). Real-axis sign changes (0.5, 1.0) and (2.0, 2.5) only.
Old layout (I170, refused by the gate): B1a +1, B1 +1, U +1, full +3, and a sign change in (1.0, 1.221). So neither the real-axis zero at 1.14 nor the strip zero (moment 3.96403 +1.81547i) exists here; no moment or circle is needed (U winds 0).
