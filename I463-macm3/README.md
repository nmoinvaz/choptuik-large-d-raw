# I463-macm3: the box count at D 30, M 64, kf 13 with modecount_wind.py and the usual left column, then moments on the boxes that wind

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/463.
Raw output is not committed here while the raw repository's rewrite pause lasts.

State: I251-macm3/hp_data_after/modecount_state_D30.0688_M64_kf13.npz (sha256 in state_sha256.txt), copied into hp/data so the setup loads it with no refit. Command (count.cmd, caffeinate -is, nice 10, one thread), #249's and #293's with this state:
python3 hp/modecount_wind.py hp/data/states/up6_D30.0688.npz --M=64 --kf=13 --h0=0.6 --lam=2.079747703853262 --aLL=-0.096 --aL=0.124 --fmax=1e-15 --resolve=last --tag=D30.0688_M64_kf13 --data=<raw>/I463-macm3/data
"The usual left column" is read as #241's fixed one, aLL -0.096 and aL 0.124, as in #249 and #293; lambda_phys 2.079747703853262 is D 30's (I251). The cache starts empty.

Written before the run (the issue's). The boxes' windings with 0 last-pass mismatches on every edge (or the edges that have them named); the two expected real zeros counted (lambda_g and lambda_phys, and the zero at 0); any extra located by moment (hp/modecount_moment.py, --wtol=1e-4 for the strip)
and by a circle. Spreads of moments are search positions. Estimates are ranges, not bounds. Stop: the setup missing the 1e-15 gate or refitting the state.

## Results

Count exit 0 at 21:32:58 UTC (started 19:21 UTC; 80 determinants, all new, not the 600 to 800 the estimate assumed). The state loaded with no refit. 14 edges, mismatch 0 in any pass and 0 in the last pass on every edge (3 to 14 points each; 2 passes on the four long edges, the others 1).
wind(g): B0 0, U0 0, B1a 0, B1b 0, B1c 0, B1 0, U 0, full 0. Expected zeros inside: B0 1 (lambda = 0), B1a 1 (lambda_g 0.8265), B1b 1 (lambda_phys 2.0797); so the winding of det M is 1, 1, 1, 0 in B0, B1a, B1b, B1c and 2 in B1. Largest phase step 0.385 rad (U0, U, full), 0.199 (B1a, B1), 0.179 (B0), 0.066 (B1b), 0.038 (B1c).
Real-axis sign changes of det M: (0.5, 1.0) and (2.0, 2.5). No box winds beyond its expected zeros, so no moment or circle is needed.
