# I156-macm3: D 30's no-cut M 48 circle evaluated on October's own state

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0,
hpkernel 0.1.0 neon), main e04d6f17. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/156

Reading, fixed before the run (2026-11-08): October's saved no-cut state hp/data/modecount_state_D30.0688_M48.npz stays in place, so setup must
load it without re-converging (the log must say "resampled state from modecount_state_D30.0688_M48.npz" and print no |F| ... Newton line), and the
no-cut evals cache hp/data/modecount_D30.0688_M48_evals.jsonl (174 lines, none with CR, written by the cloud session on Linux) is moved to
october_inputs/, so every determinant is evaluated fresh. At the lambdas shared with October's cache: if the largest |d ln|det|| is at most 1e-12
and the largest |d arg| at most 1e-10 ("a few ulp"), the whole of #68's offset (0.04 to 0.15 in ln|det|) is in the state; if the offset is 1e-3 or
more it persists with the state fixed, so it is in the evaluation; anything between is reported as such.

From the repository root with the venv's bin first on PATH, 1 thread, nice 10, caffeinate -is: python3 hp/modecount_circle.py
hp/data/states/up6_D30.0688.npz 4.267,1.324,0.35 --M=48 --fmax=1e-15. The hp/data files the run changes are copied to hp_data_after/ and the
tracked ones restored. Each .cmd has the exact line, exits.txt the exit, awake.log the awake time.

Results (macm3, main e04d6f17). Awake time equals wall time (awake.log).
  circle_M48_october_state.log: exit 0, 591 s. Its first line is "resampled state from modecount_state_D30.0688_M48.npz" and there is no "|F| ... Newton"
  line, so setup loaded October's saved no-cut state without re-converging (the state file is unchanged, equal to the copy taken before the run).
  winding +1.000000 on 24 points (+2 for beta), max step 0.369 rad, verification mismatches 0, as October. 26 fresh determinants.
  compare_nocut.txt, at the 26 lambdas shared with October's cache: ln|det| differs by at most 4.3e-08 (median 1.5e-08, signed mean +3.5e-09, 0 of 26
  identical), arg by at most 5.5e-08, pivot minimum by at most 4.2e-08 relative, with random signs. By the thresholds fixed above this is BETWEEN
  "a few ulp" (1e-12, 1e-10) and "persists" (1e-3).
  swap_state_summary.txt, 25 points common to this run, I68-macm3's round B and October's cache, on this machine with the evaluation code fixed:
  October's state gives October's determinants to 4.3e-08 (median 1.5e-08); the re-converged state gives them shifted by up to 1.47e-01 (median 8.06e-02);
  the two states differ from each other in ln|det| by the same 1.47e-01. The state effect is 3.4e+06 times the platform-level one.
  hp/data: three tracked files changed (the no-cut log, evals cache and circles.jsonl), copied to hp_data_after/ (with the diff of the text ones) and
  restored; they equal october_inputs/. hp/data is clean.
