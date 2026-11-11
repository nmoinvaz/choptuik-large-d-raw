# I441-macm3: the two D 4, M 48 test-field counts of hp/data/modecount_test_results.jsonl re-evaluated with #242's alias rule

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54 (it has #242's alias rule: modecount_wind.count with --alias default pi/2). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/441 (was #258).
Raw output is not committed here while the raw repository's rewrite pause lasts.

Inputs (october_inputs_sha256.txt), copied from the tracked hp/data into data/ so that nothing is written to hp/data: the raw determinant cache of the test-field det M_psi (modecount_test_D4.0000_M48_raw.jsonl), the two contour caches (modecount_test_D4.0000_M48_evals.jsonl, ..._plant3.1+1j_evals.jsonl),
the results file (the two October records, tags test_D4.0000_M48 and test_D4.0000_M48_plant3.1+1j; new records are appended after them) and the October log. State: hp/data/lowD_states/lowD_D4.0000_M48.npz (the record's state).
The issue gives no command; hp/modecount_test.py's own usage (tag default D<D>_M<M>, the contour cache test_<tag>, the raw cache modecount_test_<tag>_raw.jsonl) is used, with the October record's options by default (kfreeze none, contour aLL -0.114, aL 0.1933, a1 2.3241, a2 3.2741, aR 6.7 chosen by the code):
1. python3 hp/modecount_test.py hp/data/lowD_states/lowD_D4.0000_M48.npz --kf=none --data=<raw>/I441-macm3/data
2. python3 hp/modecount_test.py hp/data/lowD_states/lowD_D4.0000_M48.npz --kf=none --plant=3.1+1j --data=<raw>/I441-macm3/data

Written before the run (the issue's). Each box is stated as unchanged or corrected, against the October record, with the new determinants (evaluations new) and the verification mismatches. The old caches hold the October points, so only the intervals the alias rule bisects (26 and 38 flagged) need new determinants;
a replay that adds none would say the rule flags nothing new, and is reported as such. Stop: the setup missing the gate (series or |F|) is reported, not forced.

## Results

Both runs exit 1 within 2 s (21:11:25 to 21:11:28 UTC), in the setup, before any determinant: series_gate (#265) refuses the state hp/data/lowD_states/lowD_D4.0000_M48.npz: "series not converged in this layout (start; M = 48, nodes [0.02, 0.05, 0.1, 0.16, 0.23, 0.3, 0.4, 0.5, 0.6]):
centre 2.6e-05 (ratio 0.829 at 0.02), horizon 1.7e-06 (ratio 0.844 at 0.4); more than 1e-15". No cache line was added (data/ is as copied). The gate was not loosened and the command not changed. The October counts (2026-10-25, before the gate) used this layout.

Second attempt (coordinator, 21:13 UTC): the gate is not waived; use hp/data/lowD_states/lowDn_D4.0000_M48.npz. If its setup passes the series gate and reaches |F| below 1e-15, the two test-field counts run on it with #242's alias rule, and the October counts (made on a state the gate now refuses) are REPLACED, not re-evaluated; otherwise stop and report its tails.
Fresh caches (data_lowDn/ is empty, so every determinant is evaluated here by this build; the tracked lowDn raw cache of October is not copied). Commands (run_lowDn.sh, caffeinate -is, nice 10, one thread, plain then planted):
1. python3 hp/modecount_test.py hp/data/lowD_states/lowDn_D4.0000_M48.npz --kf=none --tag=D4.0000_M48_lowDn --data=<raw>/I441-macm3/data_lowDn
2. python3 hp/modecount_test.py hp/data/lowD_states/lowDn_D4.0000_M48.npz --kf=none --plant=3.1+1j --tag=D4.0000_M48_lowDn --data=<raw>/I441-macm3/data_lowDn
The summary lists every state under hp/data seen refused by the gate so far, with tails (coordinator's request).
lowDn runs: plain exit 0 (21:13:38 to 21:45:18 UTC, 85 new determinants), planted exit 0 (to 22:00:42 UTC, 132 evaluations in its contour cache, 47 new raw determinants beyond the plain run's 85; the raw cache has 132 lines). Setup: |F| 3.8e-31, series centre 1.2e-66 (ratio 0.159 at 0.01), horizon 1.9e-49 (ratio 0.562 at 0.3): passes the gate. 14 edges each, mismatch 0 in any pass and in the last pass.
wind(g), plain: B0 0, U0 0, B1a 0, B1b 0, B1c 0, B1 0, U 0, full 0 (expected zero 0 counted in B0). Planted 3.1+1j: B0 0, U0 0, B1a 0, B1b 0, B1c 0, B1 0, U +1, full +2 (the planted zero and its conjugate found; the control passes).
October (lowD state, refused by the gate now): plain B0 0, U0 3, B1a 0, B1b 0, B1c 0, B1 0, U 0, full 0; planted B0 2, U0 3, U 1, full 2. The new runs REPLACE them.
