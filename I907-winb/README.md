# I907-winb: sigdss at eta = 0.3, the m03up walks of #897 continued by 800 Jacobians (Windows x86-64)

Machine: winb (Surface Laptop 4, Windows 11, i7-1185G7). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/907
(follows #897, matter/SIGMA_DSS.md 11). Script: the coordinator's `run907.sh` (in this folder, unedited, md5
faa9cdb2f4be23b9f58fca30ed1661f7, its four path lines already fit this machine), run in Git Bash from this folder with the code of
the worktree `choptuik-i897` at main a1d5d879 (`sigdss_band.py --settle`), numpy 2.5.4, scipy 1.18.1, Python 3.14.10
(`env.txt`), `PYTHONUTF8=1`, `OPENBLAS_NUM_THREADS=3`, below-normal priority, two walks at a time.

Each walk starts from the end state of #897 (`I897-winb/walk2_up_10.0.npy` and `walk2_up_10.5.npy`) and runs
`sigdss_band.py walk --eps 3.33333333333 --kc 15 --maxjac 800 --settle 3` (no smoothness prior). Then one Jacobian of `walk`
from `walk2_up_10.5.npy` (`jac1_up_10.5`), then `width` at each walk's end. `exits_907.txt` has each run's exit code and wall
time (UTC), `<name>.log` each command's output, `walk3_<n>.jsonl` the history (jac, abs(F), Delta, change per Jacobian),
`walk3_<n>.npy` the end state, `width3.jsonl` the widths.

## Result

Started 04:26:20 UTC, finished 05:58:31 (1 h 32 min; the estimate was 1 h 50 min). All 5 commands exit 0.

D 10.5 ends at Delta 1.125743 after 800 more Jacobians, 3.63e-04 above the geometric 1.12538 and 4.3e-03 below 1.130, with
the step still shrinking (+4.26e-06 last), but the rate of shrinking has slowed from 1 part in 801 to 1 part in 1085 per
Jacobian, outside the 30% band around 1 part in 730, so the acceptance of the issue reads it as undecided. D 10.0 stalled on
the walk's abs(F) rule after 148 applied Jacobians at 1.152421, 3.3e-04 above 1.15209, with Delta still moving at -1.1e-06 per
Jacobian. The one Jacobian from #897's D 10.5 end prints abs(F) 1.5650e-08 after its step; the check `frozen.txt` shows abs(F)
at that start state is 3.6309e-06 when the steps are frozen from it, so the width's 3.6e-06 at #897's end was the refreeze.

## The two walks

"step" is the applied change of Delta per Jacobian (`readings.txt`, made by `read907.py`; the walk's abs(F) is the last
applied Jacobian's, the width's is at the saved end state).

| state | walk | Jacobians | Delta (#897 end) | Delta (end) | moved | abs(F) walk, width | W | step (last, mean of last 10, mean of last 50) | decay of the last 50 steps | Newton | end + Newton |
|---|---|---|---|---|---|---|---|---|---|---|---|
| m03up D 10.0 | stalled | 149 (148 applied) | 1.152612360 | 1.152420568 | -1.9179e-04 | 9.2716e-10, 9.2716e-10 | 1.4745e-03 | -1.0764e-06, -1.0530e-06, -1.1296e-06 | 1 part in 361 | -6.3910e-04 | 1.151781 |
| m03up D 10.5 | not settled | 800 (800 applied) | 1.120571241 | 1.125742990 | +5.1717e-03 | 1.1304e-08, 1.1263e-08 | 4.4707e-02 | +4.2636e-06, +4.2798e-06, +4.3247e-06 | 1 part in 1170 | +1.2011e-02 | 1.137754 |

Widths (`width3_<n>.log`, `width3.jsonl`), both exit 0: D 10.0 g 1.59034e+06 by SVD and by solve (agree), smax 19.15, smallest
singular value 2.99e-10; D 10.5 g 3.96943e+06 by SVD and by solve (agree), smax 35.13, smallest 4.46e-10 (Delta part +1.2e-03).

The D 10.0 walk stopped at Jacobian 148 (`no decrease of abs(F): stalled`): abs(F) went from 9.2716e-10 to 9.2720e-10 (relative
+4e-05) with a step of -7.162e-07 that was not applied; it is the walk's stall rule, not three quiet Jacobians (no step is
below 1e-9). The D 10.5 walk used all 800 Jacobians.

## The D 10.5 decay is not constant

Mean step per window of 100 Jacobians and the decay between consecutive windows (`windows.txt`, made by `win907.py`):

| Jacobians | mean step | decay from the window before |
|---|---|---|
| 0 to 99 | +9.2448e-06 | |
| 100 to 199 | +8.1596e-06 | 1 part in 801 |
| 200 to 299 | +7.2690e-06 | 1 part in 866 |
| 300 to 399 | +6.5209e-06 | 1 part in 921 |
| 400 to 499 | +5.8848e-06 | 1 part in 975 |
| 500 to 599 | +5.3383e-06 | 1 part in 1026 |
| 600 to 699 | +4.8643e-06 | 1 part in 1076 |
| 700 to 799 | +4.4358e-06 | 1 part in 1085 |

The whole run moves +5.1717e-03; its mean decay is 1 part in 891. A constant rate from the last 50 steps (1 part in 1170) would
add +4.98e-03 and end at 1.130726, a constant rate from #897 (1 part in 730) predicted 1.12538 at 800 Jacobians (the end is
3.63e-04 above it), and the rate keeps falling, so neither number is a measurement of where the walk ends. Newton's estimate
(end plus Newton's step) has moved 2.96e-04 (1.138050 at #897's end, 1.137754 now) while the walk's Delta moved 5.17e-03, and the
hi walk of #897 has 1.138000 (W 2.9e-03), so both branches still point to 1.1378 to 1.1380. Newton's step is a linear estimate;
W at this end is 4.5e-02.

D 10.0 (windows of 25 Jacobians, 148 steps): 1 part in 230, 376, 615, 362 between windows, 1 part in 366 over the whole run
(#897: 1 part in 370); the geometric rest of the last 50 steps is -3.87e-04, so the geometric end is 1.152033 (an extrapolation,
the walk did not get there). Newton's estimate is 1.151781, the same as #897's 1.151781.

## The one Jacobian and which abs(F) the walk sees

`jac1_up_10.5` (exit 0, 8 s): from `walk2_up_10.5.npy` the walk prints jac 0: abs(F) 1.5650e-08, Delta 1.120581694598, change
+1.0454e-05. The walk prints abs(F) after its step. `frozen.txt` (made by `frz907.py`, not part of `run907.sh`) evaluates
abs(F) of each state with the RK steps frozen from each of three states (the same `S.residual` the walk and the width use):

| steps frozen from | abs(F) at #892 end (1.115098687) | at #897 end (1.120571241) | at #907 end (1.125742990) | at jac1 end (1.120581695) |
|---|---|---|---|---|
| #892 end (`I892-rpi5/walk_up_10.5.npy`) | 2.0523e-08 | 1.5691e-08 | 3.6220e-06 | 3.6309e-06 |
| #897 end (`walk2_up_10.5.npy`) | 3.6423e-06 | 3.6309e-06 | 1.1304e-08 | 1.5650e-08 |
| #907 end (`walk3_up_10.5.npy`) | 3.6423e-06 | 3.6309e-06 | 1.1263e-08 | 1.5613e-08 |

So with the steps frozen at #897's end state the walk starts at abs(F) 3.6309e-06 (the width's number, the walk does not print
it) and one Jacobian brings it to 1.5650e-08. The 1.5691e-08 of #897's last Jacobian was abs(F) at that state with the steps
frozen from #892's end (the walk's start then). The walk's last abs(F) and the width's at the end state agree for the two ends
of this run (1.1304e-08 and 1.1263e-08, 9.2716e-10 and 9.2716e-10). #892's end and #897's end have abs(F) 2.1e-08 and 1.6e-08
under one freezing and 3.6e-06 under the other two tried; #907's end and the state after the one Jacobian have 1.1e-08 and
1.6e-08 under two freezings and 3.6e-06 under #892's. I did not find out why.

At #897's D 10.5 end the W printed there, 18.3, used the width's abs(F) 3.631e-06; at this end the two abs(F) agree and W is
4.47e-02.

## The readings against the acceptance of #907

| criterion | verdict | number |
|---|---|---|
| both walks exit 0, the one-Jacobian run exits 0 and prints abs(F) | yes | 5 of 5 exit 0; abs(F) 1.5650e-08 |
| D 10.5 geometric: end within 1e-3 of 1.12538 and decay within 30% of 1/730 | end yes, decay no | end +3.63e-04; 1 part in 1170 against 1 in 730 (band 1 in 562 to 1 in 1043) |
| D 10.5 toward 1.138: end above 1.130, or steps stop shrinking | no | end 1.125743; steps shrink (last +4.26e-06, first +1.05e-05) |
| D 10.5 reading | undecided | between the two, as fixed before the run |
| D 10.0 end within 2e-4 of 1.15209, or the disagreement reported | no, reported | 1.152421 (+3.31e-04), stalled at 149 Jacobians, Newton's estimate 1.151781 |
| each end reported with Delta, abs(F), W, the last step and the mean of the last 10 | yes | the table above |

## Discrepancies (listed, not fixed)

- D 10.5 is not settled after 800 Jacobians (step +4.3e-06 per Jacobian) and its decay rate falls from 1 part in 801 to 1 part
  in 1085, so the 1 part in 730 of #897 was a rate of its last 50 steps under another freezing, not a constant.
- D 10.0 stalled on the walk's rule at 149 Jacobians while Delta still moved -1.1e-06 per Jacobian, so it did not reach
  the 1.15209 of the issue and settled nothing; W at its end is 1.47e-03, above 1e-4.
- Each walk freezes the RK steps from its own start state, so a restart is another system: the first step at D 10.5 is
  +1.0454e-05 against #897's last +9.899e-06 (5.6% more), at D 10.0 -1.6086e-06 against -1.613e-06.
- `frozen.txt` and `win907.py` are my additions; `run907.sh` ran as placed.
- `walk3_up_10.5.log` has 28 and `jac1_up_10.5.log` 13 numpy RuntimeWarning lines (overflow and invalid value in
  `sigdss_solver.py`, the trial steps), as the walk logs of #897; the D 10.0 walk and the widths have none.

## Files

`<name>.log` one per command (5), `exits_907.txt`, `env.txt`, `run907.sh` (unedited), `walk3_<n>.jsonl` and `walk3_<n>.npy`
(the end states, the starts for longer walks), `jac1_up_10.5.jsonl` and `.npy`, `width3.jsonl`, `readings.txt` and `read907.py`,
`windows.txt` and `win907.py`, `frozen.txt` and `frz907.py`, `newton.txt` (this runner's readers of the jsonl records).
