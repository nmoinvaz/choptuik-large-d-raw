# I70-macm3/job3: the D = 4 mode count in double-double (job 3 of hp/modecount_local.sh), on Python 3.14

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel 0.1.0 cp314 neon,
modecount_cx rebuilt for 3.14), main 84d166fe. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/70. Raw folder of the issue: I70-macm3/ (jobs 6 and 7 are in its parent).

Before the job: the modecount_cx extension built for Python 3.13 segfaults under 3.14 (exit 139, smoke_cx_old_so_py314.log), so it was rebuilt with the 3.14 venv active (hp/modecount_build.sh, 32 s,
build_cx.log; the 3.13 build is kept at ~/Source/hp-dist-stale-cp313/modecount_cx_cp313.so). smoke_cx.py then gives one D 61 M 32 kf 13 determinant bit-identical to I160-macm3's record, and a changed
lambda differs (smoke_cx_rebuilt_py314.log). The rebuilt build/modecount_cx.so serves 3.14 only; the 3.13 venv would need the saved copy back.

Commands (job 3 as in hp/modecount_local.sh, caffeinate -is, nice 10, 1 thread, from the repository root, venv-macm3-314 first on PATH), in two stages:
  pilot: python3 hp/modecount_lowD.py solver/data/neB_kc39_D4.0000.npy --kc=39 --M=32,48          (writes hp/data/modecount_state_D4.0000_M48.npz; moved here afterwards)
  count: python3 hp/modecount_wind.py hp/data/modecount_state_D4.0000_M48.npz --h0=0.6 --lam=2.6740838 --data=<raw>/I70-macm3/job3/data
Below D = 35 the default layout has no cut (coordinator, 2026-11-08), so there is no --kf.

Written before the run.
  Pilot gate (the issue's): at M 32 |F| < 1e-20, and Delta within 1e-6 of 3.4454555. The count does not start unless both hold; a miss is reported, not forced.
  Count: wind(g) not 0 in any resolved box is a finding (stop, report). An edge that does not resolve is "not a count". Report the boxes' windings, the largest phase step and the verification
  mismatches. No October cache or state of D 4 M 48 at this tag is in hp/data (hp_data_before.txt), so every determinant is fresh; the state comes from the pilot.

Pilot attempt 1 (21:57 UTC): modecount_lowD.py stopped at once, `No module named 'spec_long'` (attempt1_pilot_no_DSS_SOLVER_DIR.log). The installed hpkernel (site-packages, not the tree) looks for the f64 solver
at $DSS_SOLVER_DIR, else at ../../../solver relative to the package (absent), else /home/claude/dss-residual-kernel/solver (the cloud machine). Attempt 2 sets DSS_SOLVER_DIR to this checkout's solver/
(the variable the driver documents; no code changed). No earlier task on macm3 seeded from an f64 state.

Results (macm3, main 84d166fe, venv-macm3-314 = Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0; awake.log: awake = wall for all three windows).
  STOP at the pilot gate. pilot.log (attempt 2, exit 0, 2 min 4 s): M 32 converged, |F| 1.7e-30 (below 1e-20: passes), Delta 3.445490888642500, 3.54e-5 above the f64 seed's 3.445455489194 and above
  the gate's 3.4454555 by 3.54e-5, so the "within 1e-6" half of the gate FAILS. M 48 did not converge: 12 Newton steps (the script's it_max), |F| 1.3e-04, Delta 3.445488723226338 (minus f64
  +3.32e-05), line-search steps 0.0625 to 0.5; the script saved that state (hp_data_after/modecount_state_D4.0000_M48_py314_F1.3e-4.npz, moved out of hp/data; setup would raise at --fmax anyway).
  The count was not started.
  Control: the same command on Python 3.13.3 (pilot_py313.log, run_pilot_py313.sh, --out into this folder): every Newton line equal to the 3.14 run's apart from the timings
  (pilot_newton_diff_314_vs_313.txt is empty), the same Delta and |F| at M 32 and M 48, and the M 48 state arrays equal bit for bit (zh, zl). So not caused by 3.14.
  Pointer, not a result of this task: notes/LOW_D.md has the validated Delta(4) = 3.4454524022410 (M 80, M 48 within 2.6e-7 of it, Martin-Garcia and Gundlach 3.445452402(3)), so the M 32 value
  here is 3.85e-5 high (the f64 seed 3.4454555 is 3.1e-6 high) and the pilot's 1e-6 gate would need an M 32 that resolves D 4's slowly decaying harmonics (beta 0.157, LOW_D.md).
