# I68-macm3: the D = 30 extra pair at M = 64, circles without and with the cut

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), main 58b048ce.
Versions: python-flint 0.9.0, FLINT 3.6.0, Python 3.13.3; hpkernel 0.1.0 (isa neon, the T133 build of 2026-11-06 06:56 PST, kernel unchanged since); multidouble crate 4.0.0; cargo 1.99.1, rustc 1.99.1.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/68

From the repository root of the main checkout with the venv's bin first on PATH (the scripts call python3), 1 thread, nice 10,
caffeinate -is, in order: (1) CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
CARGO_PROFILE_RELEASE_STRIP=false bash hp/modecount_build.sh (build.log, peak memory in build_peak.txt), (2) python3
hp/modecount_planted.py (planted.log, must exit 0), (3) bash hp/modecount_local.sh 4 (circles.log), (4) the hp/data files the
run created or changed are copied into hp_data_after/ and the tracked ones restored in the checkout. Each .cmd has the
exact line, exits.txt the exits and wall times, with awake times from awake.py (pmset).
Stop condition: winding != 0 on the circle at 4.267 + 1.324i, R 0.35, at M = 64 without the cut.
M = 48 reference (hp/data/modecount_circles.jsonl, 2026-10-22): winding 1.0 without the cut, 0.0 with kf 13.

Results (macm3, main 58b048ce). Exits and wall times are in exits.txt, awake times in awake.log (no sleep in any of the three).
  1. build: exit 0, 46 s, build.log ends "modecount_cx ok .../hp/modecount_cx/build/modecount_cx.so". Peak memory: 1 574 992 KB
     (sum of the resident sets of rustc, cargo and the linker, sampled every 5 s, build_peak.txt) and 1 607 942 144 bytes
     maximum resident set (/usr/bin/time -l, in build.log). The build rewrote the tracked hp/modecount_cx/Cargo.lock
     (multidouble 1.8.0 to 4.0.0, Cargo.lock.diff), which was restored afterwards.
  2. planted: exit 0, 1 s, all 8 cases PASS.
  3. circles (job 4): exit 1, 71 s, no circle computed. The first command resampled hp/data/states/up6_D30.0688.npz (M = 32,
     769 numbers) straight to M = 64 (N = 1536); |F| was 2.1e+05 at the start, after Newton and after Levenberg-Marquardt, and
     modecount_common.setup raised "background not converged in this layout: |F| = 2.1e+05 > 1e-15 (M = 64)". The second
     command (with the cut) did not run. hp/data/modecount_circles.jsonl is unchanged (2 lines).
  4. hp/data: one new file, modecount_state_D30.0688_M64.npz (|F| 2.09e+05 in its meta), moved to hp_data_after/. No tracked
     hp/data file changed. hp_data_before.txt is the listing before the run.

Second round (the coordinator's amended commands, 2026-11-08 07:02 UTC; main 58b048ce). Awake time equals wall time in every
step (awake.log).
  A. circle_M48_control.log, as written: exit 0, 0 s. setup loaded the saved October state modecount_state_D30.0688_M48.npz and
     all 24 points came from the cache (modecount_D30.0688_M48_evals.jsonl, 174 lines before and after): winding +1.000000.
     That is a replay of October, not a test of this build. Its two changed tracked files (modecount_circles.jsonl,
     modecount_D30.0688_M48.log) are in hp_data_after_control_replay/ (with diffs) and were restored.
  B. circle_M48_control_fresh.log, the same command with the October state and cache moved to october_inputs/, so that this build
     re-converges and re-evaluates: exit 0, 984 s. |F| 1.6e-11 in the resampled layout, 9.0e-18 after Levenberg-Marquardt
     (October 9.00597e-18, here 9.00628e-18), winding +1.000000 on 23 points, max step 0.392 rad, verification mismatches 0.
     All 25 evaluated points are in October's cache; control_vs_october.txt compares them: ln|det| is lower here by 0.04 to
     0.15 at every point (smoothly along the circle) and arg differs by up to 0.068 rad. Changed files in
     hp_data_after_control_fresh/; the tracked ones restored, equal to october_inputs/.
  C. circle_M64.log, M = 64 from modecount_state_D30.0688_M48.npz: exit 1, 70 s, |F| 3.4e+05 in the resampled layout, 3.4e+05
     after Newton, 3.4e+05 after Levenberg-Marquardt, RuntimeError "background not converged in this layout". The unconverged
     state (meta F 3.4e+05) is in hp_data_after_M64_from_M48/. hp/data/modecount_circles.jsonl unchanged (2 lines).
  D. The _kf13 circle was not run: the amended commands stop at a non-zero exit.
  The first attempt (job 4, from the M = 32 state) failed the same way with |F| 2.1e+05, so the failure does not depend on the
  seed being M = 32. The working M = 48 control also prints the overflow RuntimeWarning, so that warning is not the cause.
