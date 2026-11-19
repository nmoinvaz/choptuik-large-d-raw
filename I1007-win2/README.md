# I1007-win2: M = 9, level 5's polish radius at the fixed approach radius 0.105

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session (now claude-me2), runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1007 (coordinator task, #999's first recommendation). Left open on the coordinator's word.

Code: worktree `D:\choptuik-inner` (the session's own) fast-forwarded from efad7afd to origin/main ec7cfea7: its only change in `solver/inner_stokes` is hier.py printing each level's
stop reason (`--verbose=2`, replacing the old `stop at |g| ... (noise floor)` line) and every trial (`--verbose=3`); venv `C:\Users\nathan\Source\venv-i962` with numba 0.68.1,
llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1. win2b's ks_chain2 and #945 run beside it; nothing is run from or changed in `D:\choptuik-i962`.

## Written down before the runs (2026-11-19 06:31 UTC)

- #999's command with `--verbose=3 --approach=5:0.105 --polish=5:XI`, XI in 0.105, 0.115 and 0.12, `INNER_NB_RTOL=1e-13`, no `--floor`, `--procs 2`, BelowNormal; 0.105 and 0.115 side by side,
  0.12 when a slot frees; 1 h cap each (`chain1007.py`, whole process tree killed at the cap). Full command:
  `python -u hier_nb.py 9 2.719219 1.000022 --x=0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168 --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4
  --verbose=3 --approach=5:0.105 --polish=5:XI`.
- Cap rule of the issue: a run whose FIRST level-5 solve ends below 1e-6 gets a 3 h cap from its start and goes on to the M = 9 zero (the same computation). A later level-5 solve below 1e-6 does
  not extend the cap and is noted in the driver log. The driver's selftest passes and fails under `--mutate=nokill` and `--mutate=anysolve` (`logs/selftest_chain1007.txt`).
- Each log's `level radii` line is checked with `check_polish.py LOG XI 0.105` (r_5's polish and approach radii; `--mutate` must exit 1).
- Control for the moved worktree (done after the runs, from the logs, free): the prefix of the XI 0.115 log up to level 5's first stop line (pretune, levels 9 and 7, level 5's approach solve; none depends
  on XI) must equal the same prefix of #999's 0.11/0.105 log (efad7afd) once the verbose-3 trial lines are dropped and the stop-line format is normalized; the same comparison against #999's
  0.10/0.095 log (a different approach radius) must differ.
- Report per XI: level 5's solves (|r_5|, the stop reason), level 3's iterations and stop reason, and the run's end values of r_1, r_3, r_5, r_7, r_9; the table of level-5 and level-3 ends against XI
  at fixed approach radius, with the 0.11 row from #999 (first solve 7.43, lowest level-5 solve 1.17e-4, level 3 solved at 7.57), whose log has no stop reasons.
- Acceptance (the issue): that table, with each stop reason. A first level-5 solve below 1e-6 is the success case.

## The control fired once; my assumption in it was wrong (2026-11-19 06:36 to 06:42 UTC)

The control written above compared the XI 0.115 log's approach-stage prefix with #999's 0.11/0.105 log, assuming level 5's approach solve does not depend on the polish radius. **It fired**
(`logs/control1007_v2_fired_across_XI.txt`): the first level-9 solve after pretune, line 20, prints |r_9| 1.52e-10 in both new logs (XI 0.105 and 0.115, same code) and 1.53e-10 in #999's
0.11 log, lines 1 to 19 (pretune, to full digits) equal. (The first version of the script, comparing the raw prefix with the radii line and the old stop-line format, also fired and could not have
matched; this is the second version, which normalizes those.) Two probes (a 12 s start of the 0.11/0.105 command from ec7cfea7 at `--verbose=2` and `--verbose=3`, killed by pid) give 1.53e-10 in both,
so neither the new code nor the verbose level moves it: **the polish radius XI does.** `hier_nb.py` `res_raw` passes every radius to the integrator, `R = H.demixed_multi(x, M, [r for r in allr if r <= need])` with
`allr = [r1] + low.values() + pol.values()`, so XI is one of the integrator's output radii and changes its step sequence and rounding; I did not trace the exact mechanism to line 20. Consequence for
this scan: the scan's values at the 1e-10 level carry that XI-dependent rounding, the 1e-4 and larger |r_5| values do not.

The control that does what the first one meant to do: the 0.11/0.105 command from ec7cfea7 itself (`control_run1007.py`, `--verbose=3`, stopped by its own pid at the first `level 5 (low): stop at` line, 219 s,
`logs/hier_nb_M9_polish5_0.11_approach5_0.105_v3_ctrl_win2.log`, truncated on purpose), compared with #999's 0.11 log over the lines before that stop line (stop lines and trial lines dropped, seconds and addresses
and the radii line's polish radius normalized; `control1007.py`): **239 lines equal, so ec7cfea7 reproduces efad7afd's numerics up to level 5's approach stop; with the other approach radius (#999's 0.10 log) it
differs at the radii line, and with one line dropped it differs at line 21** (`logs/control1007.txt`). The control run went beyond what the scan needs (3.7 min of two threads) and is not part of the table.

## Results (runs from 06:31:31 UTC; XI 0.115 ended 06:54:51 (exit 0, 1400 s), 0.12 started 06:54:51 and ended 07:22:12 (exit 0, 1640 s), 0.105 killed at its 3600 s cap 07:31:32)

No cap extension fired (no first level-5 solve below 1e-6), so no M = 9 zero solve. No Traceback in any log. Nothing of this task runs. Tables from `summarize1007.py` (`logs/summary_polish5_v3.txt`;
its checks and their mutations: `logs/selftest_summarize1007.txt`); the `level radii` lines are checked (`logs/check_polish.txt`).

**Level-5 solves against XI at the fixed approach radius 0.105** (|r_5| at each solve's end; the 0.11 row is #999's run from efad7afd, old log format, no stop reasons; the 0.11 run's first 239 lines were reproduced from ec7cfea7):

| XI | solve 1 | solve 2 | solve 3 | later solves | level-5 solves | level 3 | the run's end |
|---|---|---|---|---|---|---|---|
| 0.105 (= AP) | 8.25 | 5.15 | 6.32 | 0.252, 9.14e-3, 9.07e-3, 14.7 (8th unfinished) | 7 | it 0 9.31e3 (lam 0.5), it 1 757 (lam 1), it 2 both trials rejected (897, 4.35e5) | killed at the cap, no FIXED-A |
| 0.11 (#999) | 7.43 | **1.17e-4** | 6.73e-4 | 3.92e-4, 3.37e-4 | 5 | solved at 7.57 | 2270 s, r_1 +5.7e5 |
| 0.115 | 9.07 | 1.44 | 1.17 | | 3 | one trial (lam 1) 2.523e4 -> 2.229e4, then stop | 1387 s, r_1 -7.3e8 + 3.9e8 i, r_3 2.2e4, r_5 1.2, r_7 6.6e-8, r_9 7.3e-10 |
| 0.12 | 12.3 | 5.12 | 4.10 | | 3 | one trial (lam 1) 5.249e4 -> 3.890e4, then stop | 1631 s, r_1 -2.3e9 - 5.2e8 i, r_3 3.9e4, r_5 4.1, r_7 1.1e-7, r_9 3.3e-9 |

**Stop reasons** (every stop of the runs, `--verbose=2`): level 5 has 27 finished stages (0.105: 8 approach + 7 polish; 0.115: 3 + 3; 0.12: 3 + 3). 24 of them stop with "a fresh Jacobian no longer halves |g|"
and 3 with "every trial rejected with a fresh Jacobian (noise floor)": 0.105's fifth polish stage (9.14e-3), and the third approach stage of 0.115 (1.26) and of 0.12 (3.18). No stop of level 5, 7 or 9 was "maxit",
"below --tol" or "at the recorded floor"; level 9's polish stops are all "step below rounding". The counts by level and stage:

| run | level 5 low | level 5 top | level 3 top |
|---|---|---|---|
| 0.105 | 8 x no longer halves | 6 x no longer halves, 1 x every trial rejected | (still iterating at the cap) |
| 0.115 | 2 x no longer halves, 1 x every trial rejected | 3 x no longer halves | 1 x no longer halves, at |r_3| 2.23e4 after one accepted trial (ratio 0.88) |
| 0.12 | 2 x no longer halves, 1 x every trial rejected | 3 x no longer halves | 1 x no longer halves, at |r_3| 3.89e4 after one accepted trial (ratio 0.74) |

**Level 3's end** (the second question of #999): at XI 0.115 and 0.12 level 3 makes one accepted trial and stops by the halving rule at |r_3| 2.2e4 and 3.9e4, where the accepted trial reduced |g| by 0.88 and 0.74, not
by half, and the stop is therefore not a noise floor but the Newton step's poor reduction. At XI 0.105 level 3 does descend, 1.05e5 -> 9.31e3 -> 757 (reductions 0.089 and 0.081, the first at lam 0.5), and its third
iteration had both trials rejected (897 against 757, and 4.35e5) before the cap ended the run, so a longer cap might have shown more; #999's 0.11 run ended on its own at 7.57.

**Reading, with its limits.** At the fixed approach radius 0.105 the first level-5 solve is 7.4 to 12 for XI 0.105 to 0.12, so the polish radius moves it little. The second solve is 4 orders lower at XI 0.11 (1.17e-4) than
at 0.105 (5.15), 0.115 (1.44) or 0.12 (5.12), and level 3's end is lowest there too (7.57 against 757 unfinished, 2.2e4 and 3.9e4). So the best XI is a narrow minimum near 0.11 or a path-dependent luck of that one run;
two runs at 0.005 on each side do not show which, and no XI reaches 1e-6. Counts of level-5 solves differ between runs (3, 5, 7), because level 3 stops sooner at 0.115 and 0.12, so "lowest |r_5|" is not compared across them.
Each point is a single run. The integrator's output radii include XI (control section), so XI also moves rounding at the 1e-10 level, which does not touch values at 1e-4 and above.
