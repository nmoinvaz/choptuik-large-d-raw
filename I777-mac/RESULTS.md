# I777-mac: results (mac752, 2026-11-15)

The coordinator wrote README.md, run.sh and queue.sh. This file holds the results, by mac752.

## Answer

The full-step drop for the own test does what #752 asked at D 118. #752's crawling iterate converges to 4.16e-65 with
it and crawls without it, and the toy and its control behave as expected. At #713's C2 start at D 252.6 it fails the
bar. The drop takes step 3 from 7.19e-16 to 4.42e-32, but Delta stays 2.0184e-11 below the planted truth, where #713's
run ended (2.1e-17 apart), and the next correction, +1.10e-5 in Delta at pivot 7.3e-31, fails its projection at all 9
trials. The queue stopped there by its rule, and the coordinator ended #777 there, so the rest was not run.

## Every job

Steps are counted as the tools count them, so the last line is the converged check or the step that found no trial.

| job | build, code | expected exit | exit | steps | final max\|F\| | criterion |
|---|---|---|---|---|---|---|
| toy | old, 8e10d127 | 0 | 0 | | all six cases pass | the toy passes: met |
| toy_mutate_drop | old, 8e10d127 | 1 | 1 | | both drop cases FAIL | its control fails: met |
| fixA | old, 8e10d127 | 1 | 1 | 6, lam 1/2 each | 2.17e-17 | crawls without the option: met |
| fixB | old, 8e10d127 | 0 | 0 | 5 (4 taken, lam 1) | 4.16e-65 | converges to 1e-60 within 6 steps: met |
| s0_D252, first run (kept as `stopped_s0_D252.*`) | new, 8e10d127 | 0 | 1 | 5 | 2.54e-22 | not #713's C2, since the re-seeder flags were dropped (stop_s0_D252.md) |
| s0_D252 | new, 165b1da3 | 0 | 1 | 5 (3 by the own test, 1 by the drop) | 4.42e-32 | seed 1 below 1e-40: **not met** |
| s0_D252_seed2 | new | 0 | not run | | | seed 2 below 1e-40: not tested |
| c2_compare | | 0 | not run | | | the seeds agree to 1e-30: not tested |
| s0_D252_mo, s0_D252_m10 | new | 1, 1 | not run | | | both controls fail: not tested |
| s0_D200 | new | 0 | not run | | | planted's bar at D 200: not tested |
| s0_wall, s0_wall_mo, s0_wall_m10 | new | 0, 1, 1 | not run | | | the wall passes, both controls fail: not tested |

Wall times: fixA 53 min, fixB 29 min, the first s0_D252 12836 s, the rerun 16755 s, all at 3 threads and nice 10 or
lower priority.

## s0_D252 on 165b1da3

The step table, the comparison with #713's run and both stops are in [stop_s0_D252.md](stop_s0_D252.md). The rest
below is measured:

- **The re-seeder settings took effect.** The first trial matched #713's to every printed digit (max|F| 2.48e+22, raw
  |dz_t| 1.200e+17).
- **Every refused trial was a failed projection.** All 19 refused trials had max|F| of 1 or more, and the projection
  counts record `failed: 19`. Six came at step 0, four at step 1 and nine at step 4.
- **The corrector moves Delta by Newton's first move.** The steps' Delta corrections are -2.018e-11, -1.987e-11 and
  -1.863e-11, at lam 1/64, 1/16 and 1. Three runs from this start take the same first three steps: #713's ref_D252
  at switch 1e-15, #713's s0_D252 and this rerun. The two that finished end at Delta = truth - 2.0184e-11, and
  ref_D252 was stopped at step 6. The planted start leaves Delta at the truth's value, since `plant_start` moves only
  the centre data and the nodes before the last.
- **The drop's step fixes the strong rows and not Delta.** Step 3's full step was taken by the drop (`by_drop` in the
  JSON). Its Delta correction was +2.4e-16, and the next one is +1.1036e-5, all of it in Delta (|dz| = |dDelta|). That
  is the step whose 9 trials failed projection.

## Discrepancies (reported, not fixed)

1. **The first s0_D252 run lost `--reseed_o 3 --reseed_start pred`.** `octo_corrector.py planted` at 8e10d127 had
   neither option, and `_parse` dropped unknown flags silently. Main 165b1da3 fixed both, and the rerun is on it.
2. **A step taken by the drop prints no trial line.** In `newton_od`'s own-test branch the outer condition includes
   `by_drop`, but the inner `verbose >= 2 or (verbose and not ok)` does not. At the default verbosity such a step logs
   only its `on N:` line, and only the JSON's `by_drop` records it (step 3 here, step 1 of the first run).
3. **The planted truth's own pinned octo-double residual is 3.58e-20,** 12 orders above the rerun's final 4.42e-32.
   So "Delta stays 2.0184e-11 below the truth" measures the iterate's error only if the truth is the octo-double root
   to better than that along Delta. That was not measured (task 1).

## Recommended tasks

What was tried at this start, checked first:

- **REDUCED_CUBIC 9–11 (#677, #694, #698).** These ran at REF and ACC (D 242.5), D 232.13 and the class A start D 249.39,
  and not at D 252.6. There, with the strong rows solved, the weak residual at c = a (Newton's first move) is 7.9e-7
  |Ba| or less, and along rays to 10⁵|a| the map is affine plus a small quadratic.
- **The strong-row chord (`--od_strong 4` / `planted --strong 4`, `chord_strong`, #528, #674).** No run from this
  planted start used it, since #713's and #777's queues have strong 0. #674's arm A ran it at the same D from a
  different start, #603's attempt 251.886 -> 252.613 (a = 0.7276, switch 1e-15). Its chord stalled at 3.5e-45 with
  |dw| equal to |F|, then crawled at lam 1/2 to 3.8e-48 at the step cap (I674-win2/README.md). CRAWL.md 9 infers that
  this crawl is the projection switch's, which this start's switch 0 removes.

1. **Is the planted truth the octo-double root at D 252.6?**
   - What: `octo_corrector.py planted` with the rerun's flags and `--rel 0 --it_max 2`, so the start is the truth
     itself.
   - Why: the two finished runs end 2.0184e-11 below the truth in Delta, agreeing to 2.1e-17, and this rerun's
     residual is 12 orders below the truth's own 3.58e-20. Which way is "out of the valley" depends on which point is the root.
   - Acceptance (can fail): the first Newton step's Delta correction from the truth is below 1e-20 in size, so the
     truth is the root along Delta, or it is within 1e-12 of -2.018e-11, so the root lies at the corrector's Delta.
     Anything else is reported as neither.
   - Estimate: 1–3 h at 3 threads, one or two Newton steps at 400–6100 s each here.
   - Depends on #777.
2. **The strong-row chord at s0_D252, which my reading says would move the iterate out of the valley.**
   - What: `planted` at the rerun's flags plus `--strong 4`, with and without `--full_drop 1e-6`.
   - Why: at this start the drop's full step solved the strong rows (4.42e-32), and the refactored Jacobian
     (pivot 7.3e-31) then asked Delta for +1.10e-5, which no projection survives. On REDUCED_CUBIC's evidence at four
     starts, the move that is needed keeps the first move's weak coordinates and solves only the strong rows through
     the start's LU. The chord does exactly that and never takes the refactored step. One obstacle is expected but not
     measured. The chord's first point is the full first step, whose projection failed in every run from this start
     (2.48e+22). planted has no projection log, so why it fails is not printed.
   - Acceptance (can fail): pinned max|F| below 1e-40 within 12 steps, with Delta within 1e-30 of the root of task 1.
     Otherwise the log names where it stops: the chord's first point failing its projection, the chord stalling, or
     the Newton steps after it.
   - Estimate: 5–8 h per arm at 3 threads.
   - Depends on task 1 for the Delta it is judged against.
3. **A trial line for a step taken by the drop.**
   - What: add `or by_drop` to the inner print condition of `newton_od`'s own-test branch.
   - Acceptance (can fail): `newton_od_toy.py`'s own-test drop case must print "accepted by the full step's drop" at
     verbose 1, and the case with the change undone must fail.
   - Depends on nothing.

## Raw commits

241f1fbb, 8b4fc2ed and a590ae82 (toy, fixA, fixB); a20bcc9a (the first stop); fc76e3ce (the restart on 165b1da3);
eb01328c (progress); 898a7ead and 8b5233f3 (the second stop); this file's commit follows.
