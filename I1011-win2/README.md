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

## Results (runs from 07:42:35 UTC, stopped by me on the coordinator's word at 08:05:13 UTC, 1360 s, by taskkill /T /F on their exact pids 9720 and 31856)

The driver's `.exit` files say "exit 1 after 1360 s": that is the kill, not a crash (no Traceback in either log; no level 3 reached). The 3 h caps were not reached. Tables by `summarize1007.py` (`logs/summary_polish5_fm_at_stop.txt`);
`level radii` and the log control above: `logs/control1011.txt`.

| run | solve 1 | solve 2 | stops (approach / polish) | level 3 |
|---|---|---|---|---|
| XI 0.11, AP 0.105 | 11.9 (2193 residuals, 603 s) | **3.92e-5** (2634 residuals, 683 s; accepted polish iterations 10.94, 5.93e-2, 4.04e-4, 3.92e-5) | solve 1: every trial rejected / every trial rejected; solve 2: every trial rejected at 10.5 (approach), every trial rejected at 3.92e-5 (polish) | not reached |
| XI 0.105, AP 0.105 | 11.4 (2187, 566 s) | 11.5 (1633, 349 s) | every trial rejected in all four stages | not reached |

No stop of either run was "maxit", "below --tol", "at the recorded floor" or "a fresh Jacobian no longer halves |g|" (which `--floor_max=1e-4` suppresses above 1e-4); all 8 level-5 stages stopped on "every trial rejected with a fresh Jacobian".
The XI 0.11 run reproduces #999's shape: a first solve stuck at about 10, then a second solve (after the leakage Jacobian K is computed) that reaches 10^-4 to 10^-5 (3.92e-5 here against 1.17e-4 in #999). At XI 0.105 the second solve stays at 11.5.
So the stall at |r_5| about 11 is the first solve's, which runs before K exists; the 3.92e-5 stop is at a level where "noise floor" may be true.

The first report to the coordinator (hc, 07:54 UTC) called both runs "stuck at about 11"; that was true of the first solves, and I had not read the XI 0.11 run's second solve (3.92e-5, ended at 1300 s) when I stopped the runs.
