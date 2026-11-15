# I827-mac: Newton's Delta step at s0_D252's truth under 1e-65 perturbations of one block

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/827.

Code: branch `wip/i827` at daf24da5 (`hp/step_spread.py`, on main 78687d7c), worktree
/Users/nathan/Source/choptuik-large-d-827. Build: main 3c35f0c's hpkernel (i599/site2), as #816 and #823. 3 threads,
nice 10.

## Plan and criteria (written by 2026-11-15 07:01 UTC, before the run)

    run.sh spread step_spread.py RAW I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --rel 1e-65 --seeds 1,2,3,4 \
        --ref 3.3110848587422764e-08 --json RAW/I827-mac/spread.json

The system is proj_shift's (#823): planted's pinned system at the truth, no projection. The plain pinned Newton step
is taken at the unperturbed truth, at the horizon data (m_h, a_h) perturbed by z_i -> z_i (1 + 1e-65 s_i) with
random signs s_i for seeds 1-4, and at each other block alone (centre, nodes 0-4, Delta) by the same size with seed 1.

- **Check:** the unperturbed step's Delta part equals +3.3110848587422764e-08 exactly (I823-mac's dz0_truth).
- **Control (reported beside it):** the centre data alone, perturbed by the same size.
- **Verdict:** "determined" if every horizon seed's Delta step is within 1e-3 relative of the unperturbed one, else
  "not determined", with the spread over seeds. Its rule's self-test passes, and `--mutate=bar` (the bar at 1e3)
  fails. Both were run before the real run: selftest.log, PASS, exit 0; selftest_bar.log, FAIL, exit 1.

Estimate: 12 Newton steps at 2.5–3.5 min each (#823's proj_shift), about 35 min.

## Results (2026-11-15 07:43 UTC)

**Not determined.** A 1e-65 relative perturbation of the horizon data alone moves Newton's Delta step from
+3.311e-8 to anywhere in -8.68e-9 .. +2.58e-8 over four seeds, its sign included. The same perturbation of the centre
or any node leaves the step equal as a double. `spread.log`, `spread.json` (07:02:01–07:42:57 UTC, exit 0):

| perturbed | move | dDelta | relative change (exact, from the parts) | smallest pivot |
|---|---|---|---|---|
| nothing | 0 | +3.3110848587e-8 (= --ref, check pass) | 0 | 7.095e-29 |
| m_h, a_h, seed 1 | 1.0e-65 | +6.7559529896e-9 | 0.796 | 2.089e-28 |
| m_h, a_h, seed 2 | 1.0e-65 | -4.1157295438e-9 | 1.12 | 6.365e-29 |
| m_h, a_h, seed 3 | 1.0e-65 | -8.6766951957e-9 | 1.26 | 2.762e-28 |
| m_h, a_h, seed 4 | 1.0e-65 | +2.5846129496e-8 | 0.219 | 2.764e-28 |
| centre (control) | 1.0e-65 | +3.3110848587e-8 | 1.05e-65 | 7.095e-29 |
| node 0 | 1.0e-65 | same | 2.33e-65 | same |
| node 1 | 1.0e-65 | same | 6.26e-57 | same |
| node 2 | 1.0e-65 | same | 1.57e-48 | same |
| node 3 | 1.0e-65 | same | 4.11e-39 | same |
| node 4 | 1.0e-65 | same | 2.98e-97 | same |
| Delta | 1.7e-65 | +3.3111596431e-8 | 2.26e-5 | 7.095e-29 |

Over the four horizon seeds the Delta step has mean +4.95e-9 and standard deviation 1.33e-8 (population, a spread
over four samples, not an error bar). The unperturbed +3.31e-8 lies outside the seeds' range. The ratio to it runs
from -0.262 to 0.781, and the largest relative deviation is 1.26, against the bar of 1e-3.

## Reading (inferred, not shown)

- Newton's Delta step at this start is octo-double rounding in the horizon data amplified, about 1e-8 for a 1e-65
  move, a gain near 1e57 in Delta. #816's +3.3e-8 (unprojected) and +1.1e-5 (projected) are both single samples of
  that noise, and the smallest pivot moves with it (6.4e-29 to 2.8e-28).
- The sensitivity grows along the nodes toward the horizon (centre 1e-65, node 1 6e-57, node 2 2e-48, node 3 4e-39 in
  relative change), but node 4's is 3e-97. So the gain is not simply distance along the chain. Why node 4 is so
  insensitive is not measured here.
- For #826 (Newton from the unprojected truth at the default switch): a Delta step at this start is not a property
  of the root beyond about 3e-8. Its Delta readings and its converged Delta, if any, carry that much of the horizon
  data's rounding unless its later steps are shown to be determined.

## Discrepancies

None against the issue's text. The verdict's bar (1e-3) is missed by a factor of 1260.

## Recommended tasks

1. **Is ElimO's projected step determined?**
   - What: step_spread with ElimO's step from each perturbed point (switch 0, reseed_o 3, reseed_start pred: the
     horizon data re-inverted from the other unknowns before the step), the same seeds and blocks.
   - Why: the projection sets the horizon data from the rest, so it may remove their rounding, and then the projected
     step (+1.1e-5 here) is the one with meaning. #823 found the projection itself moves them by 1.7e-65 only.
   - Acceptance (can fail): the unperturbed ElimO step reproduces #816's +1.1008780516254376e-5 exactly, and the
     verdict is as here: "determined" if every seed is within 1e-3 relative.
   - Estimate: 12 steps at 5–11 min each (projection plus step, #823's proj_shift), 1–2 h at 3 threads.
   - Depends on #827.
2. **The same spread at a start below the wall.**
   - What: step_spread at a converged chain state well below D 252, for example near D 240 (#808's s240.1244), with
     the same rel and seeds.
   - Why: it tells whether this indeterminacy belongs to D 252.6 or to the method, and where in D it sets in.
   - Acceptance (can fail): its unperturbed step reproduced against a recorded run, and the verdict as here.
   - Estimate: under 1 h at 3 threads.
   - Depends on #827.
