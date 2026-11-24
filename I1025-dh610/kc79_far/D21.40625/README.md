# I1025-dh610/kc79_far/D21.40625: win2's tag g leap state and tag i far scout state at D 21.40625, side by side (comparison only)

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (the orders, win2's plan, the lane, the predictions for the four comparisons). Written 2026-11-24 12:03 UTC, before either state of this D may be on origin and before any run of this folder. The k_c 79 states are not yet physical.

## Order (coordinator t5, hc, 24 Nov)
"Far-scout points at D the tag g leap also reaches (21.28125, 21.34375, 21.40625, 21.46875; tag g ends at 21.5): no lambda_1 scan; record instead the two states' Delta, |F|, steps and constraint side by side (two continuation paths to one D and k_c: the state reproducibility)."

## What is done here
- `wait_compare.sh 21.40625` (unit `i1025-cmp-21_40625`): waits for the tag g state (`sol_l1kc79Lw1025g_D21.406250.npy`, h 0.03125) and the tag i state (`sol_l1kc79Lw1025i_D21.406250.npy`, h 0.0625) of `I1025-win2/`, pins each with its record by blob (`g/in_blobs.txt`, `i/in_blobs.txt`, `g/source_commit.txt`, `i/source_commit.txt`), pushes the pins, then `lane_compare.sh 21.40625`: selftests (`kc79_syscheck_1025.py --selftest`, `compare_states.py selftest` exit 0 and its `--mutate` exit 1), the source check on each state (exit 0; `--mutate=F` and `--mutate=steps` exit 1), `compare_states.py` into `compare.txt`.
- No scan, no widening. `compare.txt`: Delta, |F|, steps, psi-constraint side by side with the difference and ratio i over g, then h and seconds, and, as an extra the order does not ask for, the L2 distance of the two state vectors.

## Acceptance (fixed before the run)
Both states accepted by the source check with both controls exit 1 (a refusal stops the lane and I report it, I do not loosen it); the selftests as wanted; the pins equal the commits' blobs. Reported: the four ordered quantities side by side as printed, by position, with the predictions of the parent README scored here.

## Predictions
The parent README's, for each D (registered before any of the four): sources accepted 90%; steps equal 55%, within 2 85%; |F| ratio within 1 +- 0.01 70%, within 0.05 90%; Delta within 1e-6 55%, within 1e-4 85%; constraints within 0.1% 60%; state distance below 1e-6 45%, below 1e-4 80%.

## Result of the comparison (`compare.txt`, written by `compare_states.py 21.40625`; lane 17:24:56 to 17:26:38 UTC, 102 s, beside the tag g leg scan of this D)
```
D 21.40625: tag g (h 0.03125) against tag i (h 0.0625); kc 79 and 79
| quantity | tag g | tag i | i - g | i / g |
|---|---|---|---|---|
| Delta | 1.129200176938387 | 1.129212511213776 | 1.2334275389047633e-05 | 1.0000109230193557 |
| |F| | 4.441325526387151e-10 | 4.4399952854183986e-10 | -1.3302409687522317e-13 | 0.9997004855958319 |
| steps | 2642 | 2642 | 0 | 1.0 |
| psi-constraint | 0.0061941693797319146 | 0.006194388083412839 | 2.1870368092404002e-07 | 1.00003530799168 |
| h | 0.03125 | 0.0625 | 0.03125 | 2.0 |
| seconds | 4398 | 4461 | 63 | 1.014324693042292 |
extra, not ordered: L2 distance of the two state vectors (Delta entry included): 2.867791882706924e-05 (shapes (5175,) and (5175,)); Delta entries np.float64(1.129200176938387) and np.float64(1.129212511213776)
```
- **Sources:** tag g: win2 commit 64a59f15 (2026-11-24 09:23:41 -08:00 = 17:23:41 UTC, 78.5 min after the D 21.375 g state); tag i: win2 commit 07efddd1 (07:50:43 -08:00 = 15:50:43 UTC, 76.7 min after the D 21.34375 i state). `kc79_syscheck_1025.py` exit 0 on both, `--mutate=F` exit 1 and `--mutate=steps` exit 1 on both (record |F| 4.4413255264e-10 and 4.4399952854e-10; the states' own |F| 4.4426209506e-10 and 4.4416348200e-10; `freeze_from` steps 2642 on both). The selftests of `compare_states.py` exit 0 and its `--mutate` exit 1 with the FIRED line.
- **Side by side (the four ordered quantities):** Delta 1.129200176938387 (g, h 0.03125) and 1.129212511213776 (i, h 0.0625), i - g = +1.2334e-05 (ratio 1.0000109); |F| 4.441325526387151e-10 and 4.4399952854183986e-10, ratio 0.9997005; steps 2642 and 2642 (equal); psi-constraint 0.0061941693797319146 and 0.006194388083412839, i - g = +2.1870e-07 (ratio 1.0000353). The record seconds were 4398 (g) and 4461 (i). Extra, not ordered: the L2 distance of the two state vectors 2.8678e-05 (5175 entries each; the Delta entries alone differ by 1.2334e-05).
- **Against D 21.34375:** the Delta difference grew from +4.1034e-06 to +1.2334e-05 (ratios of successive differences 3.72, then 3.01) and the constraint difference from +8.2914e-08 to +2.1870e-07, over one h 0.0625 step of the i path; g's Delta moved +1.6966e-03 and its constraint +2.4328e-04 over the same two h 0.03125 steps, so the path difference is 0.73% of the g move in Delta and 0.090% in the constraint (0.24% and 0.035% at D 21.34375). The steps are equal at all three shared D so far (2652, 2648, 2642). The Delta difference registered for D 21.46875 (2e-05 to 4e-05, 70%) follows from these growth ratios if they keep falling.

### Predictions scorecard of the comparison (parent README, registered before the four comparisons)
| prediction | result |
|---|---|
| both states accepted, controls 1 1 (90%) | right |
| steps equal (55%); differ by at most 2 (85%) | right (2642 and 2642); right |
| \|F\| ratio within 1 +- 0.01 (70%); within 1 +- 0.05 (90%) | right (0.9997005); right |
| Delta entries differ by less than 1e-6 (55%) | WRONG (1.2334e-05) |
| Delta entries differ by less than 1e-4 (85%) | right |
| psi-constraints differ by less than 0.1% (60%) | right (ratio 1.0000353, 0.0035%) |
| state distance below 1e-6 (45%); below 1e-4 (80%) (extra) | WRONG (2.8678e-05); right |
| (unscored expectation of mine in the leg README: the tag g state on origin about 17:15 to 17:30 UTC) | right: 17:23:41 UTC |

## Status
- 2026-11-24 12:03 UTC: folder and README written.
- 2026-11-24 17:27 UTC: the comparison is done (lane 17:24:56 to 17:26:38 UTC): result and scorecard above, parent row added. No scan at this D (the coordinator's order). The next compare is D 21.46875 (unit `i1025-cmp-21_46875` since 17:09:53 UTC, the tag i state pinned; the tag i scan follows when the tag g root at D 21.4375 sets its window).
