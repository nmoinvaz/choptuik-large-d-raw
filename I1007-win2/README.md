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
