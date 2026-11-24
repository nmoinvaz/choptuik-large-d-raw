# I1025-dh610/kc79_far/D21.28125: win2's tag g leap state and tag i far scout state at D 21.28125, side by side (no lambda_1 scan)

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (the orders, win2's plan, the lane, the predictions for the four comparisons). Written 2026-11-24 12:03 UTC, before either state of this D may be on origin and before any run of this folder. The k_c 79 states are not yet physical.

## Order (coordinator t5, hc, 24 Nov)
"Far-scout points at D the tag g leap also reaches (21.28125, 21.34375, 21.40625, 21.46875; tag g ends at 21.5): no lambda_1 scan; record instead the two states' Delta, |F|, steps and constraint side by side (two continuation paths to one D and k_c: the state reproducibility)."

## What is done here
- `wait_compare.sh 21.28125` (unit `i1025-cmp-21_28125`): waits for the tag g state (`sol_l1kc79Lw1025g_D21.281250.npy`, h 0.03125) and the tag i state (`sol_l1kc79Lw1025i_D21.281250.npy`, h 0.0625) of `I1025-win2/`, pins each with its record by blob (`g/in_blobs.txt`, `i/in_blobs.txt`, `g/source_commit.txt`, `i/source_commit.txt`), pushes the pins, then `lane_compare.sh 21.28125`: selftests (`kc79_syscheck_1025.py --selftest`, `compare_states.py selftest` exit 0 and its `--mutate` exit 1), the source check on each state (exit 0; `--mutate=F` and `--mutate=steps` exit 1), `compare_states.py` into `compare.txt`.
- No scan, no widening. `compare.txt`: Delta, |F|, steps, psi-constraint side by side with the difference and ratio i over g, then h and seconds, and, as an extra the order does not ask for, the L2 distance of the two state vectors.

## Acceptance (fixed before the run)
Both states accepted by the source check with both controls exit 1 (a refusal stops the lane and I report it, I do not loosen it); the selftests as wanted; the pins equal the commits' blobs. Reported: the four ordered quantities side by side as printed, by position, with the predictions of the parent README scored here.

## Predictions
The parent README's, for each D (registered before any of the four): sources accepted 90%; steps equal 55%, within 2 85%; |F| ratio within 1 +- 0.01 70%, within 0.05 90%; Delta within 1e-6 55%, within 1e-4 85%; constraints within 0.1% 60%; state distance below 1e-6 45%, below 1e-4 80%.

## Result (`compare.txt`, written by `compare_states.py 21.28125`; lane 13:16:37 to 13:17:11 UTC, 34 s)
```
D 21.28125: tag g (h 0.03125) against tag i (h 0.0625); kc 79 and 79
| quantity | tag g | tag i | i - g | i / g |
|---|---|---|---|---|
| Delta | 1.1258083077444154 | 1.1258094106440943 | 1.1028996789175238e-06 | 1.0000009796513947 |
| |F| | 4.5267187993303683e-10 | 4.5269051444188447e-10 | 1.8634508847640624e-14 | 1.0000411655984693 |
| steps | 2652 | 2652 | 0 | 1.0 |
| psi-constraint | 0.005713642093285211 | 0.005713664231001841 | 2.213771663032993e-08 | 1.0000038745368136 |
| h | 0.03125 | 0.0625 | 0.03125 | 2.0 |
| seconds | 4578 | 4059 | -519 | 0.8866317169069463 |
extra, not ordered: L2 distance of the two state vectors (Delta entry included): 4.405669441836917e-06 (shapes (5175,) and (5175,)); Delta entries np.float64(1.1258083077444154) and np.float64(1.1258094106440943)
```
- **Sources:** tag g: win2 commit 6e781f4d (2026-11-24 04:42:19 -08:00 = 12:42:19 UTC); tag i: win2 commit 6d922950 (05:15:27 -08:00 = 13:15:27 UTC, 71 min after the far scout's start at 12:04:28 UTC). `kc79_syscheck_1025.py` exit 0 on both, `--mutate=F` exit 1 and `--mutate=steps` exit 1 on both (record |F| 4.5267187993e-10 and 4.5269051444e-10; the states' own |F| 4.5326701826e-10 and 4.5273929147e-10; `freeze_from` steps 2652 on both). The selftests of `compare_states.py` exit 0 and its `--mutate` exit 1 with the FIRED line.
- **Side by side (the four ordered quantities):** Delta 1.1258083077444154 (g, h 0.03125) and 1.1258094106440943 (i, h 0.0625), i - g = +1.1029e-06 (ratio 1.00000098); |F| 4.5267187993303683e-10 and 4.5269051444188447e-10, ratio 1.0000412; steps 2652 and 2652 (equal); psi-constraint 0.005713642093285211 and 0.005713664231001841, i - g = +2.2138e-08 (ratio 1.0000039). The record seconds were 4578 (g) and 4059 (i). Extra, not ordered: the L2 distance of the two state vectors 4.4057e-06 (5175 entries each; the Delta entries alone differ by 1.1029e-06).
- **For scale:** along the g path Delta moves about +8.4e-04 per 0.03125 in D (1.1249625860927213 at D 21.25 to 1.1258083077444154), so the difference between the two paths is 0.13% of one g step in Delta; the constraint moved +1.16e-04 per 0.03125 (0.005597282453435274 to 0.005713642093285211), against a path difference of 2.2e-08.

### Predictions scorecard (parent README, registered before the four comparisons)
| prediction | result |
|---|---|
| both states accepted, controls 1 1 (90%) | right |
| steps equal (55%); differ by at most 2 (85%) | right (2652 and 2652); right |
| \|F\| ratio within 1 +- 0.01 (70%); within 1 +- 0.05 (90%) | right (1.0000412); right |
| Delta entries differ by less than 1e-6 (55%) | WRONG (1.1029e-06) |
| Delta entries differ by less than 1e-4 (85%) | right |
| psi-constraints differ by less than 0.1% (60%) | right (ratio 1.0000039, 0.00039%) |
| state distance below 1e-6 (45%); below 1e-4 (80%) (extra) | WRONG (4.4057e-06); right |

## Status
- 2026-11-24 12:03 UTC: folder and README written.
- 2026-11-24 13:18 UTC: done (lane 13:16:37 to 13:17:11 UTC): result and scorecard above, row added to the parent's table. The next D is 21.34375 (the unit waits for both states).
