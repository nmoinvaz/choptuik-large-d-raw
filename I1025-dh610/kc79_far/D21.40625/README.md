# I1025-dh610/kc79_far/D21.40625: win2's tag g leap state and tag i far scout state at D 21.40625, side by side, and the lambda_1 scan of the tag i state

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

## Fifth order (coordinator t5, hc, read at 17:50 UTC 24 Nov): the tag i state of this D is scanned too, as at D 21.34375 (the pair moved here from D 21.46875)
Verbatim: "Coordinator (t5): move the paired scout scan from D 21.46875 to D 21.40625. Tag g's 12 h cap ends at 19:19:49 UTC, before its D 21.46875 point (~19:58), and it is not restarted, so there will be no g state at 21.46875. At D 21.40625 both states exist (Delta i - g +1.2334e-5), and g's scan there is running now: scan the scout's D 21.40625 state with the same window and rule as g's, then report both roots, the difference and the Delta difference, beside D 21.34375's (-6.7e-5 at +4.1e-6). Drop the 21.46875 pair."

- Consequence (mine, written 2026-11-24 17:53 UTC, before the run): the comparison above is done (Delta i - g +1.2334e-05). The tag i scan is `scan_after_compare.sh 21.40625 0.775 0.7770` (unit `i1025-scan-21_40625`, `FARDIR=D21.40625/i`, 8 processes nice 8, the pins of the comparison in `i/in`, `i/in_blobs.txt`, `i/tag.txt`), on the window and rule of tag g's scan of this D (`../../kc79_leg/D21.40625/`, running since 17:25:16 UTC): PRED 0.7770 (the g root at D 21.375, 0.787758, minus 0.0108), CENTER 0.775, lambda 0.760 to 0.790 by 0.005 plus a repeat of 0.775, bar 0.01, widen once by 0.015. **It starts when the tag g lane of this D has ended, not now:** the unit runs with `BUDGET=20` (the gate of `scan_after_compare.sh` counts the recount 12 and the tag g lane 8 and waits for 12 + 8 <= 20), because with the tag g scan (8, nice 5), the k_c 95 regrid (8, nice 10) and the recount (12) a scan started now would make 36 nominal threads against the 28 the coordinator accepted; started after the g lane it makes 12 + 8 + 8 = 28. The order has no start time; the coordinator can say "now" and I drop `BUDGET` (at D 21.34375 two scans together took 2.4 times longer per point and ended at about the same time as one after the other would have).
- Acceptance (fixed before the run): as at D 21.34375: the lane's selftests as wanted (0 0 1 1 0 0 1), the source check exit 0 with both controls exit 1, all 8 processes print the record system, the repeat of 0.775 agrees; a failing control or check stops the lane and I report it. Reported: both roots (tag g and tag i) by position (bracket, det-linear, estimator range, a spread over interpolation choices and not an enclosure), their difference, the Delta difference (+1.2334e-05), beside D 21.34375's (root i - root g -0.000067 at Delta i - g +4.1034e-06); `roots_pair.py 21.40625 21.375` prints it from the files (its PREV argument is the D of the previous tag g point, 21.375, for the slope context); orientation as the reader prints it, not compared across D or k_c.
- Basis for the predictions: the g leg's slope of the root against Delta, -12.709 per unit (D 21.3125 to 21.34375), times the Delta difference +1.2334e-05 gives -1.57e-04 if Delta alone moved the root; at D 21.34375 the observed shift (-6.7e-05) was 1.28 times that estimate (-5.2e-05).
- Predictions, registered before the run (mine, information): the source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%); one robust change in the window (84%), within 0.01 of 0.7770 (90%) (the leg README's registered window and prediction); the tag i root lies below the tag g root (85%); root_i - root_g lies between -3.5e-04 and -8e-05 (65%), is more negative than D 21.34375's -6.7e-05 (85%), is at least -3e-04 (80%) and at most -1e-04 in size (25%); the two roots are in the same bracket (90%); the two estimator ranges overlap (55%). The float64 sign agrees with the hybrid at all 8 evaluations (15%). Each scan point takes 1800 to 3300 s (60%; it runs beside the k_c 95 regrid or scan and the recount, not beside another kc79 scan). The point is done (no widening) within 75 min of the lane's start (60%). The median load over the scan stays below 22 (65%).

## Result of the tag i scan (`i/`; `../summarize_far.py 21.40625 0.7770` on a symlink to `i/` > `i/summary_far.txt`; lane 18:09:46 to 19:11:32 UTC, 61.8 min; it waited 960 s for the tag g lane of this D to end)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.760 | + | ++ (True) | - | -2273.7169435707756 | 3586 |
| 0.765 | + | ++ (True) | - | -2274.4640556665154 | 3665 |
| 0.770 | + | ++ (True) | - | -2275.4431291831265 | 3029 |
| 0.775 | + | ++ (True) | + | -2277.6156456140657 | 2957 |
| 0.775 | + | ++ (True) | + | -2277.6156456140657 | 3004 |
| 0.780 | - | -- (True) | - | -2276.5890200575786 | 3097 |
| 0.785 | - | -- (True) | - | -2276.1519265051857 | 3270 |
| 0.790 | - | -- (True) | - | -2276.082972034627 | 3241 |

scan points: 8 evaluations, seconds per point min 2957, median 3169, max 3665, sum 25849; outside 900 to 1900 s: [(0.76, 3586), (0.765, 3665), (0.77, 3029), (0.775, 2957), (0.775, 3004), (0.78, 3097), (0.785, 3270), (0.79, 3241)]
win2's record at D 21.40625: |F| 4.4399952854183986e-10, steps 2642, constraint 0.006194388083412839, Delta 1.129212511213776, h 0.0625, seconds 4461
float64 sign differs from the hybrid at: [0.76, 0.765, 0.77]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far/D21.40625/i/scan 0.760 0.790
points 7 in 0.760-0.790; not noise-robust: none
hybrid signs: 0.760+ 0.765+ 0.770+ 0.775+ 0.780- 0.785- 0.790-
float64 sign differs from the hybrid sign at: [(0.76, '+', '-'), (0.765, '+', '-'), (0.77, '+', '-')]
repeated points: [(0.775, 'agree')]
  robust change (0.775, 0.780), + to -, det-linear 0.776319, range [0.775923, 0.776319]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.760, - at 0.790
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_far/D21.40625/i/scan/scan_D21.40625_all.jsonl: lambda [0.775]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

- **Source accepted** (the lane's own check on the pinned tag i state): `kc79_syscheck_1025.py` exit 0, `--mutate=F` exit 1, `--mutate=steps` exit 1; the selftests as wanted; all 8 processes printed the record system (record |F| 4.4399952854e-10, steps 2642). The state is of win2's commit 07efddd1 (15:50:43 UTC).
- **One robust change in the window 0.760 to 0.790:** (0.775, 0.780), "+ to -", det-linear **0.776319**, estimator range [0.775923, 0.776319] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005); -0.000681 against the prediction 0.7770 (bar 0.01). Edge signs differ (+ at 0.760, - at 0.790). The repeat of 0.775 is bit-identical (ln|det| -2277.6156456140657 in both, on its own process). The float64 sign differs from the hybrid at 0.760, 0.765 and 0.770, below the change.
- **Both roots at D 21.40625 (`roots_pair.py 21.40625 21.375` > `roots_pair.txt`, selftest exit 0 and its `--mutate` exit 1 with the FIRED line):**
```
D 21.40625, k_c 79 roots, not yet physical; orientation as the reader prints it (g: + to -, i: + to -), identified by position
| tag | bracket | det-linear root | estimator range (spread over interpolation choices, not an enclosure) |
|---|---|---|---|
| g (h 0.03125) | (0.775, 0.780) | 0.776450 | [0.776024, 0.776450] |
| i (h 0.0625) | (0.775, 0.780) | 0.776319 | [0.775923, 0.776319] |

root i - root g = -0.000131; same bracket: True; the estimator ranges overlap on [0.776024, 0.776319]: True
Delta g 1.129200176938387, Delta i 1.129212511213776, i - g +1.233428e-05
context: along the tag g leg D 21.375 to 21.40625 the root moves -0.011308 for a Delta move of +8.485809e-04, slope -13.326 per unit Delta; if Delta alone moved the root, the Delta difference +1.2334e-05 would move it by -1.644e-04 (observed -1.310e-04)

| lambda | ln abs det, tag g | ln abs det, tag i | i - g |
|---|---|---|---|
| 0.760 | -2273.709081663907 | -2273.7169435707756 | -0.007862 |
| 0.765 | -2274.453115954725 | -2274.4640556665154 | -0.010940 |
| 0.770 | -2275.4239830113147 | -2275.4431291831265 | -0.019146 |
| 0.775 | -2277.5105857788535 | -2277.6156456140657 | -0.105060 |
| 0.780 | -2276.6155908932888 | -2276.5890200575786 | +0.026571 |
| 0.785 | -2276.1630373244066 | -2276.1519265051857 | +0.011111 |
| 0.790 | -2276.089726865895 | -2276.082972034627 | +0.006755 |
```
  The two roots are in the same bracket (0.775, 0.780); tag i's det-linear root is 0.000131 below tag g's (orientation "+ to -" for both, by position, not compared across D or k_c), the estimator ranges overlap. The slope line is context only: it assumes Delta alone moves the root along the g leg. **Beside D 21.34375:** root i - root g -0.000067 at Delta i - g +4.1034e-06 and -0.000131 at +1.2334e-05; both differences are well below the estimator ranges (3.5e-4 to 5.7e-4 wide) and the grid step 0.005, so what they show is the sign (tag i below tag g at both D) and a size under 1.5e-4, not the ratio of the two (about -16 and -11 per unit Delta against the leg's slope of -12.7 and -13.3).
- **Seconds per point 2957 to 3665 s** (median 3169; the tag i scan at nice 8 beside the tag g scan of D 21.4375 from 18:41 UTC, the k_c 95 regrid at nice 10 and the recount). The load average, median over `i/scan/sampler.log` (122 samples, 18:10:27 to 19:11:15 UTC), was 18.44 (max 26.65, mean 20.78), peak RSS per process 1.66 to 1.82 GiB, MemAvailable at least 44.65 GiB. The load alert (`load_alert.sh`, alert only) did not fire.

### Predictions scorecard of the tag i scan (registered before the run)
| prediction | result |
|---|---|
| source accepted (91%), 8 processes with the record system (92%), the repeat agrees (92%) | right |
| one robust change in the window (84%); within 0.01 of 0.7770 (90%) | right (-0.000681) |
| the tag i root lies below the tag g root (85%) | right (-0.000131) |
| root_i - root_g between -3.5e-04 and -8e-05 (65%) | right (-1.31e-04) |
| root_i - root_g more negative than D 21.34375's -6.7e-05 (85%) | right |
| root_i - root_g at least -3e-04 (80%); at most 1e-04 in size (25%) | right; WRONG (1.31e-04) |
| the two roots are in the same bracket (90%); the estimator ranges overlap (55%) | right; right ([0.776024, 0.776319]) |
| the float64 sign agrees with the hybrid at all 8 evaluations (15%) | WRONG (differs at 0.760, 0.765, 0.770) |
| each scan point 1800 to 3300 s (60%) | WRONG (2957 to 3665 s; 6 of 8 inside) |
| the point done, no widening, within 75 min of the lane's start (60%) | right (61.8 min) |
| the median load over the scan below 22 (65%) | right (18.44) |

## Status
- 2026-11-24 12:03 UTC: folder and README written.
- 2026-11-24 17:27 UTC: the comparison is done (lane 17:24:56 to 17:26:38 UTC): result and scorecard above, parent row added. No scan at this D (the coordinator's order). The next compare is D 21.46875 (unit `i1025-cmp-21_46875` since 17:09:53 UTC, the tag i state pinned; the tag i scan follows when the tag g root at D 21.4375 sets its window).
- 2026-11-24 17:53 UTC: fifth order registered above; the unit `i1025-scan-21_40625` (BUDGET=20) is started next and waits for the tag g lane of this D to end.
- 2026-11-24 19:12 UTC: the tag i scan is done (18:09:46 to 19:11:32 UTC): roots tag g 0.776450, tag i 0.776319 (i - g -0.000131, same bracket), Delta i - g +1.2334e-05; reported to the coordinator. This was the last far lane work: the far scout was stopped at 17:27 UTC (win2), the lane is disarmed.
