# I1021-mac/ctrl: why the known zero's M = 5 and M = 7 controls fail at xi1 0.15-0.25 (#1048)

Machine: the Mac (Apple M5), helper session xfchecks, 1 nice-10 slot, one solve at a time (--procs 1). Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1048 (#1021's follow-up). Code: `hier_nb.py` at fc7dee4d (worktree
`choptuik-large-d-1021nb`), venv `/Users/nathan/venv-i1021nb` (as `../z7_m7/README.md`). The solves are made by the
functions of `../z7_m7/walk1026.py` (`solve`, M = 5) and `../z7_m7/walk1027.py` (`attempt`, M = 7; INNER_NB_RTOL=1e-13),
unchanged, so each command line is the walks' own. Written 20 Nov 2026 07:29 UTC, before any solve of this task. The
0.2 control's log (`../z7_m7/logs/fix_control_xi0.2_01*.log`) was read before this was written.

## 1. Noise floor at the known zero (`noise1048.py`)

For M in (5, 7) and xi1 in (0.15, 0.175, 0.2, 0.225, 0.25): 5 fixed-(A, w) solves at the stored zero from perturbed
starts, every harmonic times (1 + 1e-7 u), u uniform in (-1, 1), one `random.Random(1048)` per (M, xi1) set, drawn in
start order (#1027's repeat perturbation; the start is the stored harmonics, not an end state). No repeats.
- M = 5: (A, w/w_inf) = (2.718579189229888, 0.9992284031945021), the stored M = 5 zero, x = (B3, C3, B5, C5) =
  (0.1492035749173264, 0.01471905249087869, 0.008405346906375517, 0.0014703451817031647), as run_z16.sh's CTRL.
- M = 7: (A, w/w_inf) = (2.7192361834604184, 1.0000243221375533), #1027's control zero at xi1 0.15
  (`../z7_m7/inputs/walk_control_xi0.15.json`, verdict), x = its best point's six harmonics (0.148979544, 0.014770959,
  0.008424396, 0.001511232, 0.000474221, 0.000121685).
Per solve: r_1 (complex), |r_3|, |r_5|, |r_7|, converged (every |r_nu|, nu >= 3, under 1e-6: the walks' bar), wall time.
Per set: n converged; the r_1 noise sigma_1 = sqrt(sum |r_1,i - mean r_1|^2 / (n - 1)) over the converged solves (the
spread over perturbed starts, a sample standard deviation of n <= 5, so about 35% uncertain); the mean r_1 (the stored
zero's offset at that radius); median and largest |r_3|, |r_5|, |r_7| over all 5. With n < 2 a set has no sigma_1.
Caps: the walks' own per solve (3600 s M = 5, 5400 s M = 7), the whole run 6 h.

## 2. Where #1027's M = 7 control stalls at 0.2 (`stall1048.py`)

From the four attempt logs of `../z7_m7/logs/fix_control_xi0.2_01*.log` (first attempt and three repeats), and for
comparison the 0.15 control's first point (`../z7_m7/xi015/logs/fix_control_xi0.15_01*.log`): per attempt, each level-3
iteration's |r_3|, and the final |r_5| of each level-5 solve and of each level-7 solve, with hier's "noise floor" stops
per level. Reading: the stall harmonic is the highest nu (7, then 5, then 3) whose level-nu solves end at a noise-floor
stop above the 1e-6 bar; the levels below it are given with their final values.

## 3. Proposed criteria per radius (`criteria1048.py`, from section 1's table)

Per xi1 and M, with sigma_1(M, xi1) from section 1:
- solve bar: unchanged, every |r_nu| (nu >= 3) under 1e-6;
- walk bar: |r_1| at the walk's best point at most 3 sigma_1(M, xi1), in place of walk1026's 1e-2, and added to
  walk1027's Newton-step test (both step bars unchanged: 3e-6 and 3e-4);
- position bar: the control's zero within 1e-5 in A and in w/w_inf of the stored zero (M = 5: (2.718579189, 0.999228404);
  M = 7: #1027's (2.71924, 1.000025)); the M = 7 control's |F7/F5| within 5% of 0.0574, as #1027.
A radius with no sigma_1 for an M (fewer than 2 converged solves there) has no criterion for that M: its control cannot
pass. The stored control walks (`../z7_m7` at 0.2 and 0.15) are judged again under these bars where their recorded
history decides it: a walk that met a bar at an iteration it ran would have stopped there (each iteration's test uses
only points already solved); a walk that never met it would need a rerun, reported as such. No criterion is changed
after any result of boxes 7 and 16 under them; the coordinator fixes the criteria for any rerun from this report.
