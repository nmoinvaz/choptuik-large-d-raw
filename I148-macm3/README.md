# I148-macm3: D 30 M 48 kf13 determinants re-evaluated fresh, and the October offset split by the origin of each line

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT 3.6.0,
hpkernel 0.1.0 neon), main d967f7a4. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/148

From the repository root with the venv's bin first on PATH, 1 thread, nice 10, caffeinate -is: python3 hp/modecount_circle.py
hp/data/states/up6_D30.0688.npz 4.267,1.324,0.35 --M=48 --fmax=1e-15 --kf=13, with October's hp/data/modecount_state_D30.0688_M48_kf13.npz
and modecount_D30.0688_M48_kf13_evals.jsonl moved to october_inputs/ first (so this build re-converges and re-evaluates). The hp/data files the
run creates or changes are copied to hp_data_after/ and the tracked ones restored. The comparison with October's cache is by each line's
ending (compare_by_origin.py). The .cmd has the exact line, exits.txt the exit, awake.log the awake time.

Results (macm3, main d967f7a4). Awake time equals wall time (awake.log).
  circle_M48_kf13_fresh.log: exit 0, 526 s. |F| 2.5e-08 in the resampled layout, 8.9e-28 after Newton (October 8.2e-28), winding +0.000000
  on 16 points (+2 for beta), max step 0.0533, verification mismatches 0: October's record for this circle (winding 0.0, 16 points) is
  reproduced, with beta [31.87856189450961, -1.6063879992194583] against [31.878561894509566, -1.606387999219636] and min_lndet
  372.58176661208256, identical to October's.
  compare_by_origin.txt: all 18 fresh points are among October's 18 non-CR lines; none is one of its 80 CR lines. Against the non-CR lines
  ln|det| differs by at most 1.1e-13 (median 0, ln|det| about 350 to 400, so one ulp) and arg by at most 2.5e-13; the CR group has 0 shared
  points, so it is not measured. The 80 CR lines are the points of the full M 48 kf13 count (|lam - c| 0.32 to 5.6, none on the circle), the 18
  non-CR lines the circle's points (|lam - c| 0.35 and the two beta points at 0.70): the ending marks the job as much as the machine.
  hp/data: four tracked files changed (the kf13 log, evals cache, circles.jsonl and state), copied to hp_data_after/ (with the diff of the text
  ones) and restored; they equal october_inputs/. hp/data is clean.

Round 2 (the coordinator's go for job 5, 2026-11-08 07:58 UTC; main d967f7a4; the saved kf13 state moved to october_inputs_full/ so that it is
re-converged here, data_full empty). Provenance given by the coordinator: the non-CR October lines were written by the cloud session (Linux, glibc
libm, 2026-10-22), the CR lines by win's T37 on Windows.
  wind_M48_kf13_fresh.log: exit 0, 2209 s (awake 2209 s), 82 new determinants (cache data_full/, 82 lines). |F| 2.5e-08 in the layout, 8.9e-28 after Newton.
  compare_by_origin_full.txt: 80 of the 82 fresh points are October's CR lines (the other 2 are in neither group, the 18 non-CR points were not visited):
    ln|det| differs by at most 3.4e-13 (median 1.1e-13), arg by at most 1.06e-11 (median 1.4e-12), pivot minimum by at most 2.9e-14 relative.
  box lines (october_inputs/modecount_D30.0688_M48_kf13.log, 40 of 42 lines with CR, against data_full/): 6 of 8 identical; U0 and U differ only in the
    sign of the printed zero "winding of g" (+0.000000 against -0.000000); winding of det M identical in all 8 (1, -1, 1, 1, 0, 2, -7, -12).
  state_fresh_vs_october.txt: both re-converged kf13 states (circle run and full count run) differ from October's by at most 1.1e-16 (1125 of 1153
    entries identical). state_nocut_fresh_vs_october.txt (from I68-macm3's files): the no-cut fresh state differs from October's by up to 1.09e-14
    (626 of 1153 identical, the largest differences at indices 1, 2, 45, 46, 47 of the first 3M block), with the same |F| (9.0063e-18, 9.0060e-18).
  hp/data: the kf13 state (rewritten) copied to hp_data_after_full/ and restored; hp/data is clean.
