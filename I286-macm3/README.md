# I286-macm3: circles at D 58.01's four lower-box zeros (#249, M 48) on the M 40, kf 23 state, with a lam_phys control

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main bfe5fd54 (origin/main d2a75f4 differs in no file of hp/ that these runs read).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/286. Beside #271's script and I280, I282, I285.

Command (circles.cmd, caffeinate -is, nice 10, one thread): the issue's command as written. The state is M 32 native, and no D 58.0060 M 40 kf 23
state is in hp/data at the start (hp_data_before_all.txt), so setup re-converges and the cache starts empty.

Written before the run. Stop: setup |F| above 1e-15, or the lam_phys circle (first) not winding +1 within 1e-6 of 2.045529761478; then report and stop.
Report: each circle's winding, and its zero where it winds, beside the M 48 zero. A winding 0 means no zero of the M 40 determinant in that R 0.2
disc, not that none exists elsewhere. Estimates are the circles' own ranges, not bounds.

## Results

