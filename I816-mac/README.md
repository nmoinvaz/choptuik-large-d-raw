# I816-mac: Newton from #713's planted truth at D 252.6, and the drop's trial line

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/816.

Code: branch `wip/i816` at ec917706, on main 95039603, in the worktree /Users/nathan/Source/choptuik-large-d-816.
Build: main 3c35f0c's hpkernel (i599/site2, sha256 13b27ce3f9b60464...), the "new" build of #713 and #777's rerun.
Both run at 3 threads and nice 10.

## Plan and criteria (written by 2026-11-15 03:40 UTC, before the run of 03:41:08)

1. **Is the planted truth the octo-double root along Delta?** The command is #777's rerun flags plus `--rel 0
   --it_max 2`, so the start is the truth itself (`plant_start` moves nothing):

       run.sh truth_D252 octo_corrector.py planted RAW I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --switch 0 \
           --reseed_o 3 --reseed_start pred --qd 0 --full_drop 1e-6 --rel 0 --it_max 2 --out RAW/I816-mac/truth_D252

   `verdict_816.py truth_D252.json` reads the first Newton step's Delta correction dD from the JSON (`od.hist[0]`):
   - **truth**: |dD| < 1e-20, so the truth is the root along Delta.
   - **corrector**: |dD - (-2.018e-11)| <= 1e-12, so the root lies at the corrector's Delta (#713, #777).
   - **neither**: anything else, reported as such.

   Its check: `verdict_816.py --selftest` runs planted dD values (0, 9.9e-21, -3e-20, -2.0184e-11, ±1e-12 around the
   reference, +2.018e-11, 1.1e-5) through the same rule and must pass, and `--mutate=sign` flips the reference's sign
   and must fail. Both were run before the real run: PASS and FAIL. The script's reading of the JSON format was tried
   on #777's `s0_D252.json`, whose first step from the planted start, not the truth, reads -2.018440e-11.

   planted's own exit is reported, not judged. It compares against the truth itself, and 2 steps need not reach 1e-40.

2. **The drop's trial line.** In `newton_od`'s own-test branch, a trial accepted by the drop now prints its line at
   verbose 1 (`octo_corrector.py`). `newton_od_toy.py` requires the line in its first drop case for both tests, and
   `--mutate=noline` (`DROP_MUT["noline"]`) omits it in the own test, so that case must fail.

       cd hp && python3 newton_od_toy.py                    # must PASS, exit 0
       cd hp && python3 newton_od_toy.py --mutate=noline    # must FAIL, exit 1

   Before the fix, the new check failed on 95039603's code: own test, line printed False, FAIL.

## Results (2026-11-15 05:38 UTC)

**Criterion 1: neither.** From the truth (pinned max|F| 3.58e-20), Newton's first correction is +1.100878e-5, all of
it in Delta (|dz| equals |dDelta| to every printed digit), at a smallest pivot of 7.29e-31, which is 6.1e-67 of the
largest (1.20e36). That is neither below 1e-20 nor within 1e-12 of -2.018e-11. All nine trials, lam 1 to 1/256, were
refused, every projection failed (`failed` 9), and Delta was left at the truth. `verdict_816.py truth_D252.json`
prints "verdict: neither" and exits 1. planted's own check (a) failed (3.58e-20 is not below 1e-40) and it exits 1.
As planned, that is reported, not judged.

The step from the truth is the same step that ended #777's rerun at the corrector's iterate (Delta truth - 2.0184e-11,
max|F| 4.42e-32):

| | from the truth (#816, step 0) | #777's step 4, at the corrector's iterate |
|---|---|---|
| start max\|F\| | 3.58e-20 | 4.42e-32 |
| dDelta = \|dz\| | +1.100878e-5 | +1.103569e-5 |
| smallest pivot | 7.287e-31 | 7.259e-31 |
| dDelta × smallest pivot | 8.022e-36 | 8.011e-36 |
| trial max\|F\| at lam 1, 1/2, 1/4, 1/8 | 1.99e51, 7.42e48, 3.13e46, 1.66e44 | 2.04e51, 7.63e48, 3.21e46, 1.70e44 |
| fall per halving of lam, lam 1 to 1/256 | 268, 237, 189, 125, 84, 69, 65, 64 | 267, 238, 189, 125, 83, 70, 65, 64 |
| trials, projections failed | 9 refused, 9 | 9 refused, 9 (of the run's 19) |

The two corrections differ by 2.69e-8, about 1300 times the two points' 2.018e-11 separation in Delta.

**Criterion 2: pass.** The toy passes with the line printed in both tests' drop case, and both controls fail:

| run | own test's drop case | exit |
|---|---|---|
| `newton_od_toy.py` (ec917706) | accepted by the drop True, its trial line printed True: pass | 0, PASS |
| `--mutate=noline` | line printed False: FAIL | 1, FAIL |
| the toy against 95039603's octo_corrector.py (the change undone) | line printed False: FAIL | 1, FAIL |

Logs: `truth_D252.log` (03:41:08 to 05:38:23 UTC, 7032 s in newton_od at 3 threads), `truth_D252.json`,
`truth_D252.npz`, `toy.log`, `toy_noline.log`, `toy_undone.log`.

## Reading (inferred, not shown)

- The first step's Delta correction does not locate the root here. At both points the step is one jump of 1.1e-5
  along the weakest pivot's direction, and the product of the step and that pivot, a proxy for the residual's weak
  component if the step is that pivot's alone, is the same to 0.14%. A Newton step cannot tell the truth's Delta from
  the corrector's at this pivot.
- The smallest pivot falls with the residual on #777's way in (2.35e-14 at 3.4e-12, 1.21e-19 at 7.2e-16) and stops at
  7.3e-31 at both points. So the planted start's 1e-12 offset in the nodes is what lifted that pivot and gave #713's and
  #777's first steps their -2.018e-11, a correction that the truth itself does not produce.
- The trials' fall per halving tends to 64, so their failed projections leave a residual growing as lam^6 at small
  lam. #777's step 0, at 3.4e-12, fell by 16 per halving (lam^4). planted prints no projection log, so where the
  powers come from is not shown.

## Discrepancies

1. Criterion 1's verdict is neither. The first step from the truth is +1.100878e-5 in Delta, not 0 and not -2.018e-11.
2. #713's and #777's first step from the planted start, -2.018e-11, is not reproduced from the truth itself. It belongs
   to the offset start (smallest pivot 2.35e-14), and from the truth the pivot is 7.29e-31.
3. #817's acceptance asks for "Delta within 1e-30 of the root that #816 finds", and #816 finds none.

## Recommended tasks

1. **The reduced map along Delta at the truth of s0_D252.**
   - What: `reduced_cubic.py curve` (#698), or `ray` (#677), at the truth, I603-win2/chain/anm_pin3_D252.6135.npz,
     with g evaluated along +-e on the strong-solved manifold. It needs a DZ0 file of Newton's first move at the truth,
     which planted does not write (anm_run.py writes them for its attempts), so a small option is needed first.
   - Why: a Newton step at this pivot cannot place the root along Delta (above). The reduced map g(c) asks directly
     whether the weak residual has a root within |c| <= 1e-5 of the truth, and where.
   - Acceptance (can fail): `curve planted` passes and its `--mutate=w0` fails first; then g along +-e either changes
     sign within |c| <= 1e-5, which gives the root's Delta to report, or does not, which is reported as no root there.
   - Estimate: REDUCED_CUBIC 9.10's 25 to 47 min per start with tensors at 2 threads, at D 242 to 249.
   - Depends on #816, and on the DZ0 option.
2. **Print why a trial's projection fails.**
   - What: at verbose 1, `newton_od` prints the reason ElimO's projection failed for each trial (`failed` in counts).
   - Why: 9 of 9 trials failed here and 19 in #777, with residuals growing as lam^6 or lam^4, and the log does not say
     which stage of the projection gave up.
   - Acceptance (can fail): a toy case with a planted projection failure prints its reason, and with the print
     removed that case fails.
   - Depends on nothing.
3. **#817's Delta criterion.** #817 judges Delta against #816's root, which does not exist. Its pinned max|F| bar
   (1e-40) stands alone until task 1 gives a root, or it reports the final Delta against both the truth and
   truth - 2.0184e-11.
