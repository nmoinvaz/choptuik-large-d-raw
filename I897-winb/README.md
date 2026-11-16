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

(the widths and the readings follow)
