# I464-macm3: R 0.15 circles on the four B1a moment positions of #293 at D 58.01, M 40, kf 23, with the lambda_phys control

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/464.
Raw output is not committed here while the raw repository's rewrite pause lasts.

Command (circles.cmd, caffeinate -is, nice 10, one thread): #286's command with the issue's centres, the lambda_phys control first:
python3 hp/modecount_circle.py hp/data/states/up12_D58.0060.npz 2.045529761477777,0,0.2 0.452,0.523,0.15 0.722,0.587,0.15 1.127,0.968,0.15 1.489,1.282,0.15 --M=40 --kf=23 --n0=20 --fmax=1e-15 --tag=D58.0060_M40_kf23 --data=<raw>/I464-macm3/data
#286's M 40 state (I286-macm3/hp_data_after, sha256 in state_sha256.txt) is copied into hp/data so the setup loads it with no refit. The cache starts empty, so the control is evaluated again here.

Written before the run (the issue's). Each circle's winding with its mismatches; a zero position within its estimate where it winds +1; the control +1 within 1e-6 of lambda_phys 2.045529761477777. The centres are #293's moments (spreads 0.03 to 0.21), so a zero may lie outside an R 0.15 disc:
a winding 0 says only that. Estimates are ranges, not bounds.

## Results

Circles exit 0 at 19:10:18 UTC (started 17:54 UTC; 146 determinants). The control and the four circles wind +1, each with 0 verification mismatches and 0 alias bisections:
  lambda_phys 2.045529761477777 (R 0.2): zero 2.0455297798 +0.0000000047i, estimate 2.6e-07, miss 1.9e-08 (limit 1e-6).
  0.452 +0.523i (R 0.15): zero 0.459094 +0.490664i, estimate 1.4e-04, 27 points, largest step 0.352.   0.722 +0.587i: zero 0.690423 +0.611383i, 5.9e-05, 26 points, 0.383.
  1.127 +0.968i: zero 1.130985 +0.968508i, 3.3e-06, 27 points, 0.387.   1.489 +1.282i: zero 1.488789 +1.282350i, 1.6e-06, 28 points, 0.384.
