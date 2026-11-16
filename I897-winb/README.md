# I897-winb: sigdss at eta = 0.3 without the smoothness prior, the walks of #892 continued (Windows x86-64)

Machine: winb (Surface Laptop 4, Windows 11, i7-1185G7). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/897
(follows #892, matter/SIGMA_DSS.md 11). Script: the coordinator's `run897.sh` (in this folder; placed md5
2481a93125039cbd7090389cc6b3727a, mine 4cd8ac94edb36145d422b0e23d769b50, only its RAW path line changed), run in Git Bash
from `solver/matter/` of the worktree `choptuik-i897` at main a1d5d879 (it has `sigdss_band.py --settle`), numpy 2.5.4,
scipy 1.18.1, Python 3.14.10 (`env.txt`), `PYTHONUTF8=1`, `OPENBLAS_NUM_THREADS=3`, below-normal priority, two walks at a time.

Each walk starts from the end state of #892's walk (`I892-rpi5/walk_<n>.npy`, read from a separate worktree of raw main) and runs
`sigdss_band.py walk --eps 3.33333333333 --kc 15 --maxjac 400 --settle 3` (the prior is off, as in #892), so the walk stops
when three Jacobians in a row move Delta by less than 1e-9 (`--dtol`), or at 400 Jacobians. Then `width` at each walk's end.
`exits_897.txt` has each run's exit code and wall time (UTC), `<name>.log` each command's output, `walk2_<n>.jsonl` the
history (jac, abs(F), Delta, change per Jacobian), `walk2_<n>.npy` the end state, `width2.jsonl` the widths.

## The first pair (03:21:03 to 04:09:14 UTC)

Both walks exit 0 and ran all 400 Jacobians: neither settled. The smallest step of either walk is 1.1e-06 (D 10.0) and 9.9e-06 (D 10.5), far above 1e-9, and each
walk's step is still falling slowly (the last 50 steps shrink by 0.9973 and 0.9986 per Jacobian), so Delta is still moving.

| walk | start (end of #892): Delta, abs(F) | Jacobians | end: Delta, abs(F) | Delta moved | step (last, mean of last 10) | wall |
|---|---|---|---|---|---|---|
| walk2_up_10.0 (march D 10.0, Delta 1.154559202) | 1.153750697, 2.339e-09 | 400, not settled | 1.152612360, 1.115e-09 | -1.138e-03 | -1.613e-06, -1.577e-06 | 2765 s |
| walk2_up_10.5 (march D 10.5, Delta 1.112502242) | 1.115098687, 2.056e-08 | 400, not settled | 1.120571241, 1.569e-08 | +5.473e-03 | +9.899e-06, +9.960e-06 | 2889 s |

The first step of each walk is the last step of #892's walk continued (-4.51e-06 and +1.914e-05 against -4.52e-06 and
+1.93e-05 there), then each step shrinks by about 1 part in 370 (D 10.0) and 730 (D 10.5) per Jacobian. If the tail were geometric the rest of the
move would be about -6.0e-04 (D 10.0) and +7.2e-03 (D 10.5); that is an extrapolation of the last 50 steps, not a measurement.

## The second pair (04:09:14 to 04:17:37 UTC)

Both walks exit 0 and stopped on the walk's stall rule, not by settling: the last Jacobian of each did not lower abs(F)
and was not applied (the end state is the one before it). Delta was still moving.

| walk | start (end of #892): Delta, abs(F) | Jacobians | end: Delta, abs(F) | Delta moved | applied step (last, mean of last 10) | wall |
|---|---|---|---|---|---|---|
| walk2_hi_10.5 (march D 10.5, Delta 1.139109365) | 1.137696236, 1.275e-09 | 48, 47 applied, stalled | 1.137323569, 1.197e-09 | -3.727e-04 | -4.194e-06, -6.709e-06 | 456 s |
| walk2_hi_11.0 (march D 11.0, Delta 1.117461404) | 1.115934614, 1.011e-08 | 54, 53 applied, stalled | 1.114698451, 9.876e-09 | -1.236e-03 | -1.074e-05, -2.066e-05 | 503 s |

The Jacobian that ended `walk2_hi_10.5` had abs(F) 1.19672e-09 against 1.1966e-09 before it (its step would have been
-1.232e-05), the one that ended `walk2_hi_11.0` 9.87759e-09 against 9.8764e-09 (its step -3.18e-09). Each walk has two
Jacobians with a step below 1e-9 (jac 6 and 38, jac 8 and 50) and the next one is not quiet, so `--settle 3` did not
end them there (#892's walk at D 11.0 stopped on one such step, +2.7e-10, while Delta fell 2.3e-05 per Jacobian). The first
step of each walk (-7.6e-06 and -2.5e-05) is the rate #892's walk had before it stalled (-7.7e-06 and -2.3e-05).

## Result

Started 03:21:03 UTC, finished 04:18:00 (57 min of wall time; the estimate was about 4 h, a Jacobian took 7 s in the first
pair and 9 s in the second). 8 commands, all exit 0 except `width2_hi_11.0`, which exits 1 (its two g disagree, below).
No walk settled: `walk2_up_10.0` and `walk2_up_10.5` ran all 400 Jacobians with Delta still moving (-1.6e-06 and
+9.9e-06 per Jacobian), and `walk2_hi_10.5` and `walk2_hi_11.0` ended on the walk's stall rule after 48 and 54 Jacobians
(one Jacobian that did not lower abs(F)), with Delta moving at -6.7e-06 and -2.1e-05 per applied Jacobian. By the rule
of #892 all four ends are 1e-3 or more from their march's Delta, so each reads prior-held, and the one that was
undecided (D 10.0) now reads prior-held; none has an end W at or below 1e-4, so none is a settled prior-free Delta.

## The widths at the walks' ends (04:17:37 to 04:18:00 UTC)

`width` at each end state (`width2_<n>.log`, `width2.jsonl`). The Newton column is Newton's step of Delta at the end.

| walk end | Delta | abs(F) | g (SVD) | W = g abs(F) | Newton | smax, smallest singular value | g pair |
|---|---|---|---|---|---|---|---|
| walk2_up_10.0 (D 10.0) | 1.152612360 | 1.1146e-09 | 1.5887e+06 | 1.771e-03 | -8.314e-04 | 19.23, 2.98e-10 | agree (4.8e-09) |
| walk2_up_10.5 (D 10.5) | 1.120571241 | 3.6309e-06 | 5.0437e+06 | 1.831e+01 | +1.748e-02 | 31.25, 4.55e-10 | agree (1.9e-07) |
| walk2_hi_10.5 (D 10.5) | 1.137323569 | 1.1966e-09 | 2.4226e+06 | 2.899e-03 | +6.768e-04 | 44.50, 1.86e-10 | agree (1.5e-09) |
| walk2_hi_11.0 (D 11.0) | 1.114698451 | 9.8764e-09 | 8.4718e+06 | 8.367e-02 | +3.584e-02 | 93.56, 2.25e-11 | **disagree (5.2e-06)** |

`width2_hi_11.0` exits 1 because g (SVD) 8.47182e+06 and g (solve) 8.47177e+06 differ by 5.2e-06 against the tool's 1e-6
bar; the smallest singular value 2.25e-11 against smax 93.6 (condition 4e+12) is the cause, as in #892 (its march state
at D 11.0: 1.7e-05, condition 3e+13). The script and the bar are unchanged and W uses the SVD g.

At `walk2_up_10.5` the width's abs(F) is 3.6309e-06 and the walk's last abs(F) was 1.5691e-08. The other three ends agree
with their walk's last applied abs(F) to the digits printed (1.1146e-09, 1.1966e-09, 9.8764e-09). The tool's own text says
`width` freezes the RK steps from the state it is given (the end state) and `walk` freezes them once from its start state,
so the two abs(F) belong to systems built from different states; this end is 8.1e-03 from its march's Delta and 5.5e-03
from the walk's start. I did not test whether that is the whole cause.

## The readings of #892, restated on these ends

Rules of #892: prior-held when the walk ends 1e-3 or more from the march's Delta, or does not settle while Delta moves by
more than 1e-3; prior-free when it ends within the march state's own W of the march's Delta and the end's own W is at most
1e-4; otherwise undecided. None of the four walks settled, so each reading below is by the rule's 1e-3 line on an end that is
still moving. "step" is the applied change of Delta per Jacobian, the last and the mean of the last 10 (`readings.txt`,
made by `read897.py`).

| state | Delta (march), W | reading in #892 | walk of #897 | Delta (end) | end minus march | abs(F) (end) | W (end) | step | reading now |
|---|---|---|---|---|---|---|---|---|---|
| m03up D 10.0 | 1.154559202, 5.04e-03 | undecided | 400, not settled | 1.152612360 | -1.947e-03 | 1.115e-09 | 1.77e-03 | -1.613e-06, -1.577e-06 | **prior-held** |
| m03up D 10.5 | 1.112502242, 6.13 | prior-held | 400, not settled | 1.120571241 | +8.069e-03 | 1.569e-08 (width 3.631e-06) | 18.3 | +9.899e-06, +9.960e-06 | **prior-held** |
| m03hi D 10.5 | 1.139109365, 6.28e-03 | prior-held | 48, stalled | 1.137323569 | -1.786e-03 | 1.197e-09 | 2.90e-03 | -4.194e-06, -6.709e-06 | **prior-held** |
| m03hi D 11.0 | 1.117461404, 0.460 | prior-held | 54, stalled | 1.114698451 | -2.763e-03 | 9.876e-09 | 8.37e-02 | -1.074e-05, -2.066e-05 | **prior-held** |

(m03up D 9.0 was not continued; its reading in #892, prior-free, stands.)

Where the ends point. Newton's step is a linear estimate, a measurement only where W is small. The estimate "Delta plus
Newton's step" at the march state, at #892's end and at this end (`newton.txt`, made by `newton897.py`):

| state | march + Newton | #892 end + Newton | #897 end + Newton | the walk moves, Newton points |
|---|---|---|---|---|
| m03up D 10.0 | 1.151757 | 1.151769 | 1.151781 | down, down |
| m03up D 10.5 | 1.141216 | 1.139215 | 1.138050 | up, up |
| m03hi D 10.5 | 1.137918 | 1.137984 | 1.138000 | down, up |
| m03hi D 11.0 | 0.985591 | 1.125718 | 1.150537 | down, up |

At D 10.0 the three estimates agree to 2.4e-05 (W at the end 1.8e-03, so this is the one end where the estimate is close
to a measurement); the walk's end is 8.3e-04 above it and moving down, and the geometric tail of its last 50 steps would
add -6.0e-04. At D 10.5 the two branches are 2.26e-02 apart at #892's ends and 1.68e-02 apart now (the up walk gained
+5.5e-03 and the hi walk lost 3.7e-04), and their Newton estimates, 1.2e-03 apart at #892's ends, are now 5.0e-05 apart
(1.138050 and 1.138000); the up walk's W is 18, so its estimate is the weaker one. At D 11.0 the estimate has not settled
(0.986, 1.126, 1.151), the walk moves down and Newton points up, with the smallest singular value 2e-11.

## Discrepancies (listed, not fixed)

- No walk settled. `walk2_hi_10.5` and `walk2_hi_11.0` ended on the walk's stall rule (abs(F) rose from 1.1966e-09 to
  1.19672e-09 and from 9.8764e-09 to 9.87759e-09, relative 1e-4 and 1.2e-4) while Delta moved by -4.2e-06 to -1.2e-05 and
  -1.1e-05 to -3.2e-05 per Jacobian before it; the step alternates between sizes there, so a walk-rule stall is not a
  settled Delta (as in #859).
- `width2_hi_11.0` exits 1: the two g differ by 5.2e-06 against 1e-6.
- The width at `walk2_up_10.5` has abs(F) 3.6309e-06 against the walk's 1.5691e-08.
- Three of the four walk logs (all but `walk2_up_10.0.log`) print the numpy RuntimeWarnings that #892's logs have
  (overflow and invalid value in the trial steps, `sigdss_solver.py` lines 241 to 250 and 45, `dss.py:197`, numpy's
  norm): 20, 22 and 25 lines, the same 25 distinct warnings as the Pi's `walk_*.log`.

## Files

`<name>.log` one per command (8), `exits_897.txt`, `env.txt`, `run897.sh` (placed md5 2481a931, only its RAW line changed),
`walk2_<n>.jsonl` and `walk2_<n>.npy` (the end states, the start for a longer walk), `width2.jsonl`, `readings.txt` and
`read897.py`, `newton.txt` and `newton897.py` (this runner's readers of the jsonl records).
