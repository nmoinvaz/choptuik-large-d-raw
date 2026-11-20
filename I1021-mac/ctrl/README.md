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

## Results (20 Nov, noise 07:30-08:45 UTC; `noise/points.jsonl`, `noise/table.jsonl`, `stall/`, `crit/criteria.txt`)

Noise at the known zero (5 perturbed starts per row; sigma_1 is the spread over the converged starts; the |r_nu| are
each solve's final values):

| M | xi1 | converged | sigma_1 | 3 sigma_1 | \|mean r_1\| | \|r_3\| median, max | \|r_5\| median, max | \|r_7\| median, max |
|---|---|---|---|---|---|---|---|---|
| 5 | 0.15 | 5/5 | 1.3e-2 | 3.8e-2 | 1.1e-2 | 1.4e-8, 7.3e-8 | 8.9e-11, 1.8e-10 | |
| 5 | 0.175 | 5/5 | 1.2e-5 | 3.6e-5 | 9.2e-6 | 2.0e-10, 2.5e-10 | 1.3e-10, 8.0e-10 | |
| 5 | 0.2 | 5/5 | 5.5e-8 | 1.7e-7 | 1.3e-7 | 4.1e-10, 5.6e-10 | 2.8e-10, 4.8e-10 | |
| 5 | 0.225 | 5/5 | 7.1e-4 | 2.1e-3 | 4.4e-4 | 9.3e-9, 1.4e-8 | 3.9e-10, 8.1e-10 | |
| 5 | 0.25 | 5/5 | 2.4e-4 | 7.3e-4 | 8.5e-4 | 7.5e-9, 1.1e-8 | 3.5e-10, 5.0e-10 | |
| 7 | 0.15 | 5/5 | 8.2e-2 | 2.4e-1 | 2.3e-2 | 1.2e-7, 2.6e-7 | 1.3e-10, 3.3e-10 | 6.5e-10, 7.7e-10 |
| 7 | 0.175 | 0/5 | - | - | - | 1.4e-4, 2.3e-4 | 3.6e-9, 1.1e-8 | 5.2e-10, 7.1e-10 |
| 7 | 0.2 | 0/5 | - | - | - | 1.3e-2, 1.8e-2 | 5.9e-7, 2.6e-6 | 6.5e-10, 8.9e-10 |
| 7 | 0.225 | 0/5 | - | - | - | 2.2, 2.6 | 2.4e-6, 6.4e-6 | 6.2e-10, 4.3e-9 |
| 7 | 0.25 | 0/5 | - | - | - | 3.7, 4.9 | 2.4e-6, 5.1e-6 | 6.4e-10, 9.1e-10 |

The M = 5 solve converges at every radius. The M = 7 solve converges only at 0.15. The spread of r_1 over the five
unconverged M = 7 solves is 0.5 at 0.175, 2.6e2 at 0.2, 1.7e4 at 0.225 and 5e4 at 0.25.

The M = 7 stall at 0.2 (section 2, `stall/stall_control.txt`): the pre-registered reading gives harmonic 5 in all four
attempts. It gives 5 at 0.15 as well, because at each radius at least one level-5 solve ends above 1e-6 right after a
noise-floor stop, so the reading alone does not separate the radii. What separates them was found after the readings
were fixed. The median final |r_5| of the level-5 solves is 6.5e-7 to 2.3e-6 at 0.2, with 2 to 8 solves per attempt
above the bar. At 0.15 it is 3.2e-10 to 5.5e-10, with 1 above the bar. Level 3 above them stops at hier's noise floor,
|r_3| 5.6e-3 to 5.2e-2. The same reading on the noise solves (`stall/stall_noise_M7.txt`, outside the pre-registered
reading) gives these medians of final |r_5| by radius:
- 0.15: 3e-10 to 7e-10.
- 0.175: 4e-9 to 8e-9, while level 3 still ends at 2.5e-5 to 2.3e-4.
- 0.2: 7.5e-7 to 1.65e-6.
- 0.225: 1.5e-6 to 53. 0.25: 1.3e-6 to 8.8e2.

At 0.225 and 0.25, 3 of the 5 starts also have level-7 solves that end above the bar after a noise-floor stop. So the
failure reaches higher harmonics as xi1 grows. At 0.175 level 3 stops above the bar while level 5 ends near 1e-8. At
0.2 level 5 ends near 1e-6. At 0.225 and 0.25 some level-7 solves stop as well.

Criteria and the controls under them (section 3, `crit/criteria.txt`):
- **xi1 0.15: both controls pass, on the Mac's walks.** The M = 5 walk would stop at iteration 5 (|r_1| 0.024 against
  the bar 0.038), with a zero 2.2e-6 and 1.4e-6 from the stored one. The M = 7 walk would stop at iteration 1 (|r_1| 0.14
  against 0.24), 1.4e-6 and 6.1e-7 from #1027's zero, with |F7/F5| 0.0573.
- **No other radius passes.** At 0.175 to 0.25 no M = 7 noise solve converges, so M = 7 has no criterion there. At 0.2
  the M = 5 walks of both machines would need a rerun: under the bar 1.7e-7 their old stop at |r_1| 6.3e-3 to 6.4e-3 does
  not count.
- **dh610's M = 5 control at 0.15 still fails.** Its iteration 4 meets the walk bar (|r_1| 0.020) but not the unchanged
  step bar (|dA| 4.5e-6 against 3e-6), and the walk then stops by itself. The Newton step's noise there is about
  sigma_1 / sigma_min(J) = 1.3e-2 / 5.2e3 = 2.4e-6, taking sigma_min from the Mac walk's iteration 4. That is the size of
  walk1026's 3e-6 step bar, so the step bar is the next limit at 0.15 for M = 5. It is not changed here; that is for the
  coordinator.
