# I823-mac: the reduced map along Delta at s0_D252's planted truth (D 252.6)

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/823.

Code: branch `wip/i823` at 3cc51ed5 (on main 7658b35c), in the worktree /Users/nathan/Source/choptuik-large-d-823.
Build: main 3c35f0c's hpkernel (i599/site2), as #816; hp/src is unchanged since. 3 threads, nice 10, one job at a time.

## Plan and criteria (written by 2026-11-15 05:54 UTC, before the first run)

The criterion, as amended on the issue before the real run
(https://github.com/nmoinvaz/choptuik-large-d/issues/823#issuecomment-6889972314): **a root on the + or - ray within
|c| <= 1e-4**, meaning every component of g changes sign between neighbouring grid points (t = 0 is g(0)). The + ray's
grid gains t = |a| (`--curve_t=a`), and the root's Delta is read there. The issue's literal 1e-5 reading is reported.

1. **The DZ0 file.** `octo_corrector.py planted --save_dz0` (new) writes the start and its first Newton step in
   anm_run.py's dz0 format, with planted's own plan (segs) and held offset (c0..c7), and stops before the trials:

       run.sh dz0_truth octo_corrector.py planted RAW I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --rel 0 \
           --qd 0 --reseed_o 3 --reseed_start pred --save_dz0 RAW/I823-mac/dz0_truth.npz

   These are #816's flags without `--switch 0` (default 1e-15) and the drop: the truth's residual (3.58e-20) is below
   the switch, so the start is not projected, and the step is the pinned system's own Newton step, the one
   reduced_cubic rebuilds. Its dDelta is reported against #816's +1.100878e-5 (switch 0, a projected start).
2. **The stored system's check.** reduced_cubic's `Real` uses the file's plan and offset, and requires the stored step
   to be that system's Newton step at z0: |-J^-1 F(z0) - dz0| / |dz0| < 1e-20. Control, which must fail:
   `curve RAW I823-mac/dz0_truth.npz BASE --mutate=dz0` (the step scaled by 1 + 1e-6).
3. **The plant first.** `curve planted` must pass, and `curve planted --mutate=w0` must fail.
4. **The real curve**, + ray first (curve's order). Its reading is posted before the - ray's:

       run.sh curve_truth reduced_cubic.py curve RAW I823-mac/dz0_truth.npz I603-win2/chain/anm_pin3_D252.6135.npz \
           --threads=3 --curve_t=a --json=RAW/I823-mac/curve_truth.json

   curve's own checks Z1 and Z2 need #677's ray and #694's rows at this start, which do not exist, so its exit is
   reported, not judged.
5. **The verdict.** `verdict_823.py curve_truth.json dz0_truth.npz` reads g(0), g at each converged point, and the
   move's Delta (dlast): per ray, root within 1e-4 (judged) and within 1e-5 (reported), the bracket, and at t = |a|
   the Delta and |g| / |g(0)|. A ray that stops before 1e-4 without a bracket is undecided (exit 1). Its check:
   `--selftest` (six planted rays) must pass, and `--selftest --mutate=any` (a root when any component changes
   sign) must fail. Both were run before the real data: PASS (exit 0) and FAIL (exit 1), verdict_selftest*.log.

## Runs

| run | result | exit |
|---|---|---|
| `dz0_truth` (05:54:00–05:55:43 UTC) | written; projections skipped 1; \|dz\| = dDelta = **+3.311085e-8** (#816 at switch 0: +1.100878e-5) | 0 |
| `curve_planted` | PC1 worst point error 1.3e-48 (1e-3), PC2 pass, check pass | 0 |
| `curve_planted_w0` | PC1 7.3e+56, PC2 FAIL, check FAIL | 1 |
| `curve_dz0mut` | stored step against its re-solve 1.0e-6 (bound 1e-20): FAIL; the held offset's check FAIL too (4.21e9 on its rows, 9.02e10 elsewhere) | 1 |

The control fired at both checks, and `main_curve` stops at the offset check first. queue.sh's gate looked for the
second check's line only, so it did not start the real curve (queue.log). The real curve was started by hand at 05:59
UTC, with the command of the plan.
