# I1025-dh610/kc79_far/D21.34375: win2's tag g leap state and tag i far scout state at D 21.34375, side by side, and the lambda_1 scan of the tag i state

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (the orders, win2's plan, the lane, the predictions for the four comparisons). Written 2026-11-24 12:03 UTC, before either state of this D may be on origin and before any run of this folder. The k_c 79 states are not yet physical.

## Order (coordinator t5, hc, 24 Nov)
"Far-scout points at D the tag g leap also reaches (21.28125, 21.34375, 21.40625, 21.46875; tag g ends at 21.5): no lambda_1 scan; record instead the two states' Delta, |F|, steps and constraint side by side (two continuation paths to one D and k_c: the state reproducibility)."

## What is done here
- `wait_compare.sh 21.34375` (unit `i1025-cmp-21_34375`): waits for the tag g state (`sol_l1kc79Lw1025g_D21.343750.npy`, h 0.03125) and the tag i state (`sol_l1kc79Lw1025i_D21.343750.npy`, h 0.0625) of `I1025-win2/`, pins each with its record by blob (`g/in_blobs.txt`, `i/in_blobs.txt`, `g/source_commit.txt`, `i/source_commit.txt`), pushes the pins, then `lane_compare.sh 21.34375`: selftests (`kc79_syscheck_1025.py --selftest`, `compare_states.py selftest` exit 0 and its `--mutate` exit 1), the source check on each state (exit 0; `--mutate=F` and `--mutate=steps` exit 1), `compare_states.py` into `compare.txt`.
- No scan, no widening. `compare.txt`: Delta, |F|, steps, psi-constraint side by side with the difference and ratio i over g, then h and seconds, and, as an extra the order does not ask for, the L2 distance of the two state vectors.

## Acceptance (fixed before the run)
Both states accepted by the source check with both controls exit 1 (a refusal stops the lane and I report it, I do not loosen it); the selftests as wanted; the pins equal the commits' blobs. Reported: the four ordered quantities side by side as printed, by position, with the predictions of the parent README scored here.

## Predictions
The parent README's, for each D (registered before any of the four): sources accepted 90%; steps equal 55%, within 2 85%; |F| ratio within 1 +- 0.01 70%, within 0.05 90%; Delta within 1e-6 55%, within 1e-4 85%; constraints within 0.1% 60%; state distance below 1e-6 45%, below 1e-4 80%.

## Third order (coordinator t5, hc, 24 Nov, about 14:36 UTC): the tag i state of this D is scanned too, after the comparison
Verbatim: "Coordinator (t5): one change at the shared D 21.34375 only: after the side-by-side comparison, scan the far scout's state too (same window and rule as tag g's scan there), so the lambda_1 spread between the two paths is measured where their Delta may differ by ~5e-6 (win2's qualification of 14:34). Report both roots and their difference. The other shared D stay comparison-only."

- Run: `scan_after_compare.sh 21.34375 0.800 0.7987` as unit `i1025-scan-21_34375`: it waits for the line "states compared ... far point done" of this folder's `exits_far.txt` (a STOP or refuse line there stops it with nothing scanned), the thread gate (`../budget.txt`, 99), the far lock, then `lane_far.sh` with `FARDIR=D21.34375/i`: the state is the tag i state the comparison pinned (`i/in`, `i/in_blobs.txt`), its source check is repeated by the lane, the scan is lambda 0.785 to 0.815 by 0.005 and a repeat of 0.800 (8 processes of 1 thread, nice 8), readings against 0.7987 (bar 0.01), widen once by 0.015 if there is no robust change. Everything of the scan is in `i/`. The tag g scan of this D is in `../../kc79_leg/D21.34375/` (same window, same prediction).
- Acceptance (fixed before the run): the lane's selftests as wanted (0 0 1 1 0 0 1), the source check exit 0 with both controls exit 1, all 8 processes print the record system, the repeat of 0.800 agrees; a failing control or check stops the lane and I report it. Reported: both roots (tag g and tag i) by position (bracket, det-linear, estimator range, a spread over interpolation choices and not an enclosure) with their difference, beside the Delta difference of the comparison; orientation as the reader prints it, not compared across D or k_c.
- Predictions, registered before the run (mine, information): the source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%); one robust change in the window (84%), within 0.01 of 0.7987 (90%); the bracket of the tag i root equals the tag g root's (85%); the det-linear roots differ by at most 1e-3 (90%), at most 3e-4 (70%), at most 1e-4 (40%); the two estimator ranges overlap (65%). Basis: along the tag g leg the root moves -0.010629 per 8.47e-04 of Delta (-12.6 per unit), so a Delta difference of 1e-6 to 5e-6 moves it by 1e-5 to 6e-5 if Delta alone mattered, and the estimator ranges of the last three tag g points were 3.6e-04, 6.3e-05 and 3.0e-04 wide. The float64 sign agrees with the hybrid at all 8 evaluations (15%). Each scan point takes 1700 to 3200 s (65%; it runs beside the tag g scan and the recount: 28 nominal threads on 20 logical). The point is done (no widening) within 90 min of the lane's start (70%). The median load over the overlap with the tag g scan stays below 22 (70%).

### Second word of the coordinator (hc, 24 Nov, 2026-11-24 14:40 UTC), verbatim
"Coordinator (t5): yes, start the i scan at D 21.34375 now (same window, rule and registered predictions); the comparison runs when g lands, and the two roots' difference is reported after the g scan."

- The tag i scan therefore starts now, at nice 8, beside the recount only, and the comparison runs when the tag g state lands; the registered predictions above stand unchanged. The prediction about the load median over the overlap with the tag g scan is void if the two scans do not overlap (the tag i scan needs about 32 min, the tag g state is expected 15:15 to 15:25 UTC): it is then reported as void, not scored. The scan's source check is the lane's own, on the state pinned at 14:34 UTC (`i/in_blobs.txt`).

## Result of the comparison (`compare.txt`, written by `compare_states.py 21.34375`; lane 14:49:17 to 14:51:15 UTC, 118 s, with both scans' load beside it)
```
D 21.34375: tag g (h 0.03125) against tag i (h 0.0625); kc 79 and 79
| quantity | tag g | tag i | i - g | i / g |
|---|---|---|---|---|
| Delta | 1.1275035270998226 | 1.127507630527052 | 4.103427229340539e-06 | 1.0000036393919227 |
| |F| | 4.484968788840308e-10 | 4.4857763320637664e-10 | 8.07543223458453e-14 | 1.0001800554834335 |
| steps | 2648 | 2648 | 0 | 1.0 |
| psi-constraint | 0.005950886267504929 | 0.005950969181448842 | 8.291394391294477e-08 | 1.0000139330412623 |
| h | 0.03125 | 0.0625 | 0.03125 | 2.0 |
| seconds | 2808 | 4556 | 1748 | 1.6225071225071226 |
extra, not ordered: L2 distance of the two state vectors (Delta entry included): 1.6212815817896247e-05 (shapes (5175,) and (5175,)); Delta entries np.float64(1.1275035270998226) and np.float64(1.127507630527052)
```
- **Sources:** tag g: win2 commit 451fee48 (2026-11-24 06:48:05 -08:00 = 14:48:05 UTC, **48.2 min** after the D 21.3125 g state, not the 76 to 85 min of the earlier g states: its record's seconds are 2808, against 4584 at D 21.3125); tag i: win2 commit 9bb1884b (06:34:00 -08:00 = 14:34:00 UTC, 78.6 min after the D 21.28125 i state). `kc79_syscheck_1025.py` exit 0 on both, `--mutate=F` exit 1 and `--mutate=steps` exit 1 on both (record |F| 4.4849687888e-10 and 4.4857763321e-10; the states' own |F| 4.4900336580e-10 and 4.4849861144e-10; `freeze_from` steps 2648 on both). The selftests of `compare_states.py` exit 0 and its `--mutate` exit 1 with the FIRED line.
- **Side by side (the four ordered quantities):** Delta 1.1275035270998226 (g, h 0.03125) and 1.127507630527052 (i, h 0.0625), i - g = +4.1034e-06 (ratio 1.0000036); |F| 4.484968788840308e-10 and 4.4857763320637664e-10, ratio 1.0001801; steps 2648 and 2648 (equal); psi-constraint 0.005950886267504929 and 0.005950969181448842, i - g = +8.2914e-08 (ratio 1.0000139). The record seconds were 2808 (g) and 4556 (i). Extra, not ordered: the L2 distance of the two state vectors 1.6213e-05 (5175 entries each; the Delta entries alone differ by 4.1034e-06).
- **Against D 21.28125:** the Delta difference grew from +1.1029e-06 to +4.1034e-06 and the constraint difference from +2.2138e-08 to +8.2914e-08 over the two h 0.0625 steps of the i path (D 21.28125 to 21.34375: g's Delta moved +1.6952e-03 and its constraint +2.3724e-04), so the path difference is 0.24% of the g move in Delta and 0.035% in the constraint; the steps are equal at both D (2652, 2648).

### Predictions scorecard of the comparison (parent README, registered before the four comparisons)
| prediction | result |
|---|---|
| both states accepted, controls 1 1 (90%) | right |
| steps equal (55%); differ by at most 2 (85%) | right (2648 and 2648); right |
| \|F\| ratio within 1 +- 0.01 (70%); within 1 +- 0.05 (90%) | right (1.0001801); right |
| Delta entries differ by less than 1e-6 (55%) | WRONG (4.1034e-06) |
| Delta entries differ by less than 1e-4 (85%) | right |
| psi-constraints differ by less than 0.1% (60%) | right (ratio 1.0000139, 0.0014%) |
| state distance below 1e-6 (45%); below 1e-4 (80%) (extra) | WRONG (1.6213e-05); right |
| (unscored expectation of mine in the leg README: the tag g state on origin about 15:15 to 15:25 UTC) | WRONG: 14:48:05 UTC |

## Result of the tag i scan (`i/`; `../summarize_far.py 21.34375 0.7987` on a symlink to `i/` > `i/summary_far.txt`; lane 14:40:25 to 16:03:12 UTC, the scan 14:40:41 to 16:03:12 = 82.5 min)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.785 | + | ++ (True) | + | -2281.7998012892554 | 4826 |
| 0.790 | + | ++ (True) | + | -2282.6462568113193 | 4381 |
| 0.795 | + | ++ (True) | + | -2283.942459331604 | 4524 |
| 0.800 | - | -- (True) | - | -2284.989168989766 | 4323 |
| 0.800 | - | -- (True) | - | -2284.989168989766 | 4943 |
| 0.805 | - | -- (True) | - | -2283.9894708206866 | 3556 |
| 0.810 | - | -- (True) | + | -2283.8072895281753 | 4867 |
| 0.815 | - | -- (True) | - | -2283.827252841434 | 4640 |

scan points: 8 evaluations, seconds per point min 3556, median 4582, max 4943, sum 36060; outside 900 to 1900 s: [(0.785, 4826), (0.79, 4381), (0.795, 4524), (0.8, 4323), (0.8, 4943), (0.805, 3556), (0.81, 4867), (0.815, 4640)]
win2's record at D 21.34375: |F| 4.4857763320637664e-10, steps 2648, constraint 0.005950969181448842, Delta 1.127507630527052, h 0.0625, seconds 4556
float64 sign differs from the hybrid at: [0.81]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far/D21.34375/i/scan 0.785 0.815
points 7 in 0.785-0.815; not noise-robust: none
hybrid signs: 0.785+ 0.790+ 0.795+ 0.800- 0.805- 0.810- 0.815-
float64 sign differs from the hybrid sign at: [(0.81, '-', '+')]
repeated points: [(0.8, 'agree')]
  robust change (0.795, 0.800), + to -, det-linear 0.798701, range [0.798136, 0.798701]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.785, - at 0.815
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far/D21.34375/i/scan/scan_D21.34375_all.jsonl: lambda [0.8]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

- **Source accepted** (the lane's own check on the pinned tag i state): `kc79_syscheck_1025.py` exit 0, `--mutate=F` exit 1, `--mutate=steps` exit 1; the selftests as wanted; all 8 processes printed the record system (record |F| 4.4857763321e-10, steps 2648). The state is of win2's commit 9bb1884b (14:34:00 UTC).
- **One robust change in the window 0.785 to 0.815:** (0.795, 0.800), "+ to -", det-linear **0.798701**, estimator range [0.798136, 0.798701] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005); +0.000001 against the prediction 0.7987 (bar 0.01). Edge signs differ (+ at 0.785, - at 0.815). The repeat of 0.800 is bit-identical (ln|det| -2284.989168989766 in both). The float64 sign differs from the hybrid at 0.810, above the change.
- **Both roots at D 21.34375 (`roots_pair.py 21.34375 21.3125` > `roots_pair.txt`, selftest exit 0 and its `--mutate` exit 1 with the FIRED line):**
```
D 21.34375, k_c 79 roots, not yet physical; orientation as the reader prints it (g: + to -, i: + to -), identified by position
| tag | bracket | det-linear root | estimator range (spread over interpolation choices, not an enclosure) |
|---|---|---|---|
| g (h 0.03125) | (0.795, 0.800) | 0.798768 | [0.798216, 0.798768] |
| i (h 0.0625) | (0.795, 0.800) | 0.798701 | [0.798136, 0.798701] |

root i - root g = -0.000067; same bracket: True; the estimator ranges overlap on [0.798216, 0.798701]: True
Delta g 1.1275035270998226, Delta i 1.127507630527052, i - g +4.103427e-06
context: along the tag g leg D 21.3125 to 21.34375 the root moves -0.010781 for a Delta move of +8.483179e-04, slope -12.709 per unit Delta; if Delta alone moved the root, the Delta difference +4.1034e-06 would move it by -5.215e-05 (observed -6.700e-05)

| lambda | ln abs det, tag g | ln abs det, tag i | i - g |
|---|---|---|---|
| 0.785 | -2281.791622302807 | -2281.7998012892554 | -0.008179 |
| 0.790 | -2282.634517130593 | -2282.6462568113193 | -0.011740 |
| 0.795 | -2283.9166492174295 | -2283.942459331604 | -0.025810 |
| 0.800 | -2285.034941053603 | -2284.989168989766 | +0.045772 |
| 0.805 | -2283.9991526138233 | -2283.9894708206866 | +0.009682 |
| 0.810 | -2283.8119153279763 | -2283.8072895281753 | +0.004626 |
| 0.815 | -2283.829836605837 | -2283.827252841434 | +0.002584 |
```
  The two roots are in the same bracket (0.795, 0.800); tag i's det-linear root is 0.000067 below tag g's (the sign is from the printed orientation of each: both "+ to -", by position, not compared across D or k_c), the estimator ranges overlap. The slope line is context only: it assumes Delta alone moves the root along the g leg.
- **Seconds per point 3556 to 4943 s** (median 4582; the last tag i points at nice 8 beside the tag g scan at nice 5 and the recount, 1.69 to 1.84 GiB peak RSS per process). The load average, median over `i/scan/sampler.log` (164 samples, 14:40:51 to 16:02:51 UTC), was 18.13 over the whole scan and **18.16 over the overlap with the tag g scan** (147 samples from 14:49:14 UTC; max 28.91); MemAvailable at least 38.62 GiB. The load alert (`load_alert.sh`, alert only) did not fire.

### Predictions scorecard of the tag i scan (registered before the run)
| prediction | result |
|---|---|
| source accepted (91%), 8 processes with the record system (92%), the repeat agrees (92%) | right |
| one robust change in the window (84%); within 0.01 of 0.7987 (90%) | right (+0.000001) |
| the bracket of the tag i root equals the tag g root's (85%) | right ((0.795, 0.800) both) |
| the det-linear roots differ by at most 1e-3 (90%), at most 3e-4 (70%), at most 1e-4 (40%) | right (6.7e-05), right, right |
| the two estimator ranges overlap (65%) | right ([0.798216, 0.798701]) |
| the float64 sign agrees with the hybrid at all 8 evaluations (15%) | WRONG (differs at 0.810) |
| each scan point 1700 to 3200 s (65%) | WRONG (3556 to 4943 s) |
| the point done, no widening, within 90 min of the lane's start (70%) | right (82.5 min) |
| the median load over the overlap with the tag g scan below 22 (70%) | right (18.16) |

## Status
- 2026-11-24 12:03 UTC: folder and README written.
- 2026-11-24 14:38 UTC: third order registered above; the unit `i1025-scan-21_34375` waits for the comparison.
- 2026-11-24 14:40 UTC: the second word (above): the tag i scan starts now (unit `i1025-scan-21_34375` restarted with NOWAIT=1).
- 2026-11-24 14:52 UTC: the comparison is done (lane 14:49:17 to 14:51:15 UTC): result and scorecard above; the tag i scan (`i/`) runs since 14:40:41 UTC, and the tag g scan of the leg lane since 14:49:14 UTC, so the two overlap.
- 2026-11-24 16:08 UTC: the tag i scan is done (14:40:41 to 16:03:12 UTC) and the tag g scan of the leg lane (14:49:14 to 16:06:15 UTC): both roots above (i - g = -0.000067, same bracket); reported to the coordinator.
