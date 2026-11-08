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
