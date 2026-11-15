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
| `curve_truth` (05:59:33–06:02:46 UTC) | offset 6.72e-44 off its rows (0.000789 on them): pass; stored step re-solved 3.12e-89: pass; basis \|a\| 3.343e-8, sigma of B 9.09e-30..7.62e-28, \|B a\| 7.118e-37, \|w0\| 2.257e-19; g(0)'s chord NOT converged, floor0 2.53e-18 (3.6e18 \|B a\|); no point evaluated | 1 |
| `diag_g0` (06:04:45–06:09:09 UTC) | the chord at c = 0 and newton_strong at c = 0, below | 0 |
| `proj_shift` (06:10–06:31:20 UTC) | both checks pass, below | 0 |
| `proj_shift_block` (`--mutate block`) | displacement outside m_h and a_h 6.78e-67 (must be 0): FAIL | 1 |

The control fired at both checks, and `main_curve` stops at the offset check first. queue.sh's gate looked for the
second check's line only, so it did not start the real curve (queue.log). The real curve was started by hand at 05:59
UTC, with the command of the plan.

## Results (2026-11-15 06:57 UTC)

**The reduced map is not defined at this start with curve's strong solves**, so neither the amended criterion (a root
within |c| <= 1e-4) nor the literal 1e-5 one can be read. The strong part of Newton's move, |w0| 2.257e-19, takes the
pinned max|F| from 3.58e-20 to 8.6e-4 (`diag_g0.log`):

| strong solve at c = 0 | step | max\|F\| | \|dw\| | \|g\| |
|---|---|---|---|---|
| (z0) | | 3.583e-20 | | 7.118e-37 (U^T F(z0) = \|B a\|) |
| chord through z0's LU | 0 (at z0 + w0) | 8.611e-4 | 2.764e-13 | 6.333e-14 |
| | 1 | 1.776e10 | 6.418e10 | 3.29e10 |
| | 2 | nan | nan | nan |
| newton_strong (LU refactored at z0 + w0) | 1 LU | 8.611e-4 | 2.764e-13, above its bound max(\|c\|, \|w0\|) = 2.26e-19: stops | 6.333e-14, not converged |

**Newton's first move from the unprojected truth** asks Delta for +3.311085e-8 (|a| 3.343e-8; a = V^T dz0 = -3.335e-8,
-1.939e-9, 9.913e-10, 5.348e-10). #816's +1.100878e-5 is the step at the switch-0 projected start.

**The switch-0 projection moves only the horizon data, by about quad-double rounding**, and still changes the Delta
step 332-fold (`proj_shift.log`). Per block, max|.|:

| block | z | z_proj - z | plain step at z | plain step at z_proj | ElimO's step from z |
|---|---|---|---|---|---|
| centre | 0.99999 | 0 | 6.998e-10 | 1.095e-6 | 1.095e-6 |
| node 0 | 1.0 | 0 | 2.074e-10 | 3.229e-7 | 3.229e-7 |
| node 1 | 1.0 | 0 | 2.740e-10 | 4.248e-7 | 4.248e-7 |
| node 2 | 1.0 | 0 | 3.387e-10 | 5.221e-7 | 5.221e-7 |
| node 3 | 1.0 | 0 | 4.014e-10 | 6.135e-7 | 6.135e-7 |
| node 4 | 1.0001 | 0 | 4.621e-10 | 6.984e-7 | 6.984e-7 |
| m_h | 0.15843 | 1.789e-66 | 6.350e-10 | 9.074e-7 | 9.074e-7 |
| a_h | 1.0001 | 1.697e-65 | 8.004e-13 | 1.100e-9 | 1.100e-9 |
| Delta | 1.6845 | 0 | **3.311e-8** | **1.101e-5** | **1.101e-5** |

The pinned max|F| is 3.5827e-20 at both points. The smallest pivot is 7.095e-29 at z and 7.287e-31 at z_proj. ElimO's
step from z reproduces #816's dDelta and the plain step at z reproduces dz0_truth's, both to relative 0 (bound 1e-6).

## Reading (inferred, not shown)

- The coordinator's reading, which these numbers fit: a strong move of 2.26e-19 that takes |F| to 8.6e-4 is the
  horizon block's gain, about 1e37 at this D, the same sensitivity that broke #800's rung and #808's held arm (the
  comparison is the coordinator's; I have not read those runs). Two ratios from here bear on it: the smallest pivot
  moves by 7.0e-29 for a horizon move of 1.7e-65, about 4e36 per unit, and |F(z0 + w0)| / |w0|^2 is 1.7e34.
- Newton's weak step at this start is set at the level of quad-double rounding in the horizon data. A 1.7e-65 move
  changes its Delta part from 3.3e-8 to 1.1e-5, so neither number is a property of the root. Both #816's verdict and
  any Delta read from a Newton step here inherit that.

## Discrepancies

1. #816's "the truth asks Delta for the same 1.1e-5 jump" was the projected start's step. It is corrected on #816
   (comment of 05:57 UTC).
2. The amendment's reason gives |a| as 1.10e-5, but |a| is 3.343e-8. The amended criterion stands, as the coordinator
   confirmed.
3. queue.sh's gate missed the `--mutate=dz0` control's failure (above), and the real curve was started by hand.
4. curve exits 1 at g(0), before any point, so its Z1/Z2 checks and the verdict script never ran on real data.

## Recommended tasks

1. **Newton's Delta step against rounding at the truth.**
   - What: perturb the horizon data (m_h, a_h) of the truth by 1e-65 relative, random signs, over four seeds, and
     separately every other block; take the plain pinned Newton step at each (proj_shift's system), and report the
     spread of its Delta part and of the smallest pivot.
   - Why: a 1.7e-65 move changes the Delta step 332-fold here, so whether the weak step is determined at octo-double
     precision at all decides what any Newton-based root test at this D can say.
   - Acceptance (can fail): a zero perturbation reproduces +3.3110848587e-8 exactly, and a perturbation of the centre
     data alone of the same size is reported beside it as the control. The spread over seeds is reported. It decides
     "determined" if every seed's Delta step is within 1e-3 relative of the unperturbed one, else "not determined".
   - Estimate: about 3 min per step at 3 threads, 9 steps, about 30 min. Depends on #823.
2. **Plain octo-double Newton from #777's final iterate, in the truth's system.**
   - What: a `planted --start FILE` option (the start read in eight parts, the system still the truth's), then
     newton_od at the default switch 1e-15 from `I777-mac/s0_D252.npz` (4.42e-32, below the switch, so not projected).
   - Why: #777's run stalled after its projected step (+1.10e-5). Without the projection, the step there is
     unmeasured.
   - Acceptance (can fail): pinned max|F| below 1e-40 within 12 steps, with Delta reported against the truth and
     truth - 2.0184e-11. Otherwise the log names the step where it stops, and its first step's Delta part.
   - Estimate: under 1 h at 3 threads (an LU here takes 2–3 min). Depends on #823.
3. **A strong solve with the horizon data projected, for the reduced map.**
   - What: reduced_cubic's strong solve (chord and newton_strong) composed with ElimO's projection, or run on the
     system with the horizon data eliminated (reseed's ElimO), so that g(c) is defined at this start.
   - Why: with the horizon data free, the first strong move leaves the regular family (8.6e-4) and no strong solve
     converges.
   - Acceptance (can fail): curve planted passes under the new solve and --mutate=w0 fails. At the truth, g(0)'s strong
     solve converges (|dw| < 1e-40 |w0|), and |g(0) - U^T F(z0)| is reported against |B a|. Then this issue's criterion.
   - Estimate: the code first (the coordinator's), then 1–2 h at 3 threads. Depends on #823.
4. **#817's switch-0 runs.** Their steps are ElimO's, whose Delta part here is 332 times the unprojected one. Read
   their Delta with that in mind, or add an arm at the default switch.
