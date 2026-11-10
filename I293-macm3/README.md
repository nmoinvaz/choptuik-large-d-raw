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

