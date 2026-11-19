# I1012-win2: M = 9, level 5's finite-difference step raised (--h5)

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session (claude-me2), runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1012 (coordinator task, #1011's finding). Raw output of this task only.

Code: main 23844822 (its change in `solver/inner_stokes` is `hier_nb.py --h5=REL` and `--h7=REL`, level 5's and 7's relative finite-difference step, passed to the spawn workers by the environment variables
HIER_NB_H5 / HIER_NB_H7 like `--h3`; hier's default step is 1e-6 relative, `1e-6 * max(|b|, 1e-3 |A|)`, i.e. 8.4e-9 and 2.7e-9 absolute for level 5). The worktree `D:\choptuik-inner` stays at
656396fd while #1011's two runs execute from it, and is fast-forwarded to origin/main only after they have ended. venv `C:\Users\nathan\Source\venv-i962` (numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1).
win2b's ks_chain2 and #945 run beside it; nothing is run from or changed in `D:\choptuik-i962`.

## Written down before any #1012 run (2026-11-19 08:04 UTC; #1011's runs are still going)

Order (the coordinator's hc and the issue): #1011's runs end first (their 3 h caps end at 10:42:35 UTC; `I1011-win2`, posted on #1011), then the plumbing control, then the runs.

**Done before the control, without a solve** (a scratch extract of main 23844822's `solver/inner_stokes`, no worktree touched): `unit_h5.py` calls `LazyHier.h(l, x)` at #999's pretuned x with HIER_NB_H5 unset, `1e-6`, `1e-4`, and a wrong
variable name (`unit_h5_result.txt`): level 5's step is exactly 1 x, 1 x, **100 x** and 1 x hier's default; levels 3 and 7 never move; a mutated expectation (100 x read as 1 x) fails. So `--h5=1e-6` is bit-identical to the default
step by arithmetic (same double, same expression) and `--h5=1e-4` changes level 5's step by a factor 100.

1. **Plumbing control** (`control_run1012.py`, `control1012.py`; the issue's step 1): #1011 run 1's command (XI 0.11, AP 0.105, `--floor_max=1e-4 --verbose=2`, `--procs 2`, rtol 1e-13) with `--h5=1e-6` and with `--h5=1e-4`, side by
   side, each stopped by its own pid when its first `level 5 (low): stop at` line appears (or at 600 s). `--h5=1e-6` must equal #1011 run 1's log line for line up to and including that stop line (seconds and addresses
   normalized): **pass**. `--h5=1e-4` must differ before that line (its first level-5 iteration): **pass if it differs**. Either failing stops the task and is reported. The comparison script's self-tests (the log against itself passes, other radii and a
   dropped line fail) are in `logs/selftest_control1012.txt`.
2. **Runs** (`chain1012.py`): #1011's two runs with `--h5=1e-4` added, side by side: (XI 0.11, AP 0.105) and (XI 0.105, AP 0.105), 3 h cap each, killed with their process tree. Command: `INNER_NB_RTOL=1e-13 python -u hier_nb.py 9
   2.719219 1.000022 --x=0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168 --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --h5=1e-4 --floor_max=1e-4 --verbose=2 --approach=5:AP --polish=5:XI`.
3. **Stage 2**: if neither first level-5 solve ends below 1e-6, **run 1 again with `--h5=1e-3`** (XI 0.11, AP 0.105; the issue's wording; the coordinator's hc can be read as both runs, so the XI 0.105 run at 1e-3 is not started
   unless asked). It starts as soon as both first solves have ended, beside the stage-1 runs, which go on to their caps. If either first solve is below 1e-6, stage 2 is not started and that run goes on to the zero within its cap.
   The driver's decision and its selftest (stage 2 starts for first solves 6.0 and 8.0, not for 5e-7 and 8.0; fails under `--mutate=anyone` and `--mutate=nokill`): `logs/selftest_chain1012.txt`.
4. **Radii check** on each log's `level radii` line (`check_polish.py LOG XI AP`, its mutation fails).
5. **Report** (the issue): per run, level 5's and level 3's solves (end |r|, stop reason, accepted trials) and the run's end r_1 to r_9 (`summarize1007.py`; its checks are tested in `I1007-win2/logs/selftest_summarize1007.txt`); beside #1011's table.
6. **Acceptance** (the issue): level 5's first solve below 1e-6 is the success case, then the run goes on to the zero within its cap. If the stop reason stays "every trial rejected" at |r_5| above 1, the Jacobian's step is not the
   cause either, and that is the report.

Deviation to note: the issue says "run 1 again with `--h5=1e-3`" and the hc says "then #1011's two runs with --h5=1e-4 ... and --h5=1e-3 if neither first solve gets below 1e-6"; I follow the issue (run 1 only) as the task's record.

## Added by the coordinator's hc, 08:14 UTC 19 Nov (before any level-5 solve of the h5 = 1e-4 runs had ended)

- **Success is any level-5 solve below 1e-6, not only the first** (the coordinator notes it on the issue). The driver's "later solve below 1e-6" notice is the matching check; the runs have 3 h caps already, so nothing is extended.
- Report each later level-5 solve's end |r_5| and stop reason too (`summarize1007.py` lists every solve with both stages' stops and accepted iterations).
- If the later solves floor near 4e-5 with every trial rejected (as #1011's XI 0.11 run did, 3.92e-5), that may be the integrator's floor at rtol 1e-13 rather than the Jacobian, and the next run is the same command at `INNER_NB_RTOL=1e-14`, which lowered M = 7's floors (#976, #977, #981). Not started before the h5 = 1e-4 results are read; it is a new command with its own pre-registration.
