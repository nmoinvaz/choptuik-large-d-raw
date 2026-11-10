# I285-macm3: the D 56.01, M 48, kf 23 recount with the left column's edge at Re -0.2, then moments and circles on box B0

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main bfe5fd54 (origin/main d2a75f4 differs in no file of hp/ that these runs read).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/285. Beside #271's script and I280, I282, I286.

Commands: the issue's, in order (count.cmd first; the moments and circles by hand after it). The cache
I249-macm3/D56.0117/data/modecount_D56.0117_M48_kf23_evals.jsonl (714 lines: #249's count and its circles) is copied into data/ first.
The state I249-macm3/D56.0117/hp_data_after/modecount_state_D56.0117_M48_kf23.npz is copied into hp/data (state_sha256.txt), so that the
reused determinants and the new ones belong to one state; a Newton or LM line in count.log means it was refitted, and is reported.
The number of cached determinants the count reuses is reported in the first progress post.

Written before the run. Stop: box B0 unresolved, or the moment tool refusing B0's winding; then report and stop, with no other edge chosen here.
Report: B0's and U0's windings with their last-pass mismatches, the zero against #249's -0.089555 +0.032884i, and the three circles' windings
(the zero, its conjugate, lam_phys at 2.046953490259203). Acceptance: B0 with 0 last-pass mismatches and a +1 circle on each zero.

## Results

