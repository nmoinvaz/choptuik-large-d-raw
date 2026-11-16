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

(the second pair and the widths follow)
