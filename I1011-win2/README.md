# I1011-win2: M = 9, levels 5 and 3 without the slow-progress stop above 1e-4

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session (claude-me2), runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1011 (coordinator task, #1007's finding). Left open on the coordinator's word.

Code: worktree `D:\choptuik-inner` (the session's own) fast-forwarded from ec7cfea7 to origin/main 656396fd: its only change in `solver/inner_stokes` is `hier.py --floor_max=X`
(default inf, unchanged behavior; passed to the spawn workers): the stop "a fresh Jacobian no longer halves |g|" (the `floor` rule) applies only when |g| < X; above X the solve goes on,
refreshing the Jacobian on slow steps, and each level still stops at its maxit of 15 iterations. It does NOT touch the other stops: "every trial rejected with a fresh Jacobian (noise floor)"
(3 of 27 level-5 stages in #1007), "step below rounding", "at the recorded floor", "below --tol". venv `C:\Users\nathan\Source\venv-i962` with numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1.
win2b's ks_chain2 and #945 run beside it; nothing is run from or changed in `D:\choptuik-i962`.

## Written down before the runs (2026-11-19 07:42 UTC)

- #1007's command with `--floor_max=1e-4 --verbose=2` (not 3): `INNER_NB_RTOL=1e-13 python -u hier_nb.py 9 2.719219 1.000022 --x=0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168
  --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --floor_max=1e-4 --verbose=2 --approach=5:AP --polish=5:XI`, at (1) XI 0.11, AP 0.105 and (2) XI 0.105, AP 0.105, `--procs 2` each, BelowNormal,
  side by side, 3 h cap each (`chain1011.py`, whole process tree killed at the cap; its selftest passes and fails under `--mutate=nokill` and `--mutate=anysolve`, `logs/selftest_chain1011.txt`). No cap extension
  is needed: if a run's first level-5 solve ends below 1e-6 it goes on to the zero within its 3 h (the driver only logs it).
- Each log's `level radii` line is checked with `check_polish.py LOG XI AP` (`--mutate` must fail).
- Control, done after the runs from the logs (free): a new log must equal a reference of the same radii from the code before `--floor_max`, line for line, up to the reference's first level-5 (low) stop line, and must not print that
  stop at that point (it is a slow-progress stop above 1e-4). References: run (2) against #1007's XI 0.105 log (`I1007-win2/logs/hier_nb_M9_polish5_0.105_approach5_0.105_v3_win2.log`); run (1) against #1007's truncated control run at
  XI 0.11 (`I1007-win2/logs/hier_nb_M9_polish5_0.11_approach5_0.105_v3_ctrl_win2.log`). `control1011.py`; its mutations (a reference of other radii, a dropped line) must make it fail. Rounding depends on XI (#1007), so the references
  must be at the same XI.
- Report (the issue): per run each level-5 and level-3 solve's end |r| and stop reason, the final r_1 to r_9, the wall time (`summarize1007.py`, whose checks and mutations are in `I1007-win2/logs/selftest_summarize1007.txt`).
- Acceptance (the issue): level 5's first solve below 1e-6 is the success case, then the run goes on to the M = 9 zero within the 3 h. Otherwise the table; "maxit" as the new commonest stop reason would point to the Newton direction
  rather than the stop rule.
