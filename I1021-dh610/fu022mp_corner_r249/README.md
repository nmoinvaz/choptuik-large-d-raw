# I1021-dh610/fu022mp_corner_r249: the two unresolved quarters of the #1076 box recounted at xi1 0.249, with the NW quarter as the control for "the zero set does not depend on xi1"

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1076. Written 2026-11-25 21:34 UTC (the clock), before any run of this folder's work.

## Order (coordinator t5, hc, 25 Nov, read at about 21:35 UTC), verbatim
"go with --r1=0.249 as a replacement: stop the r1 0.25 lane by exact pid, keep its one mp row in the record, and run NW (the control) then SW and SE at r1 0.249, with predictions registered first. The radius is a free parameter of the method (the zero set is taken as xi1-independent; #1080's x2 zero did not move between 0.17 and 0.2), so 0.249 serves the order."
It replaces `../fu022mp_corner_r25/` (stopped at 21:32 UTC by TERM to the exact pids 2123529, 2123602, 2123607, 2123608; its 0.25 cache keeps 5 rows: 4 without value, 1 valued in extended precision; see that folder's README). The earlier order that started it: "recount the two unresolved quarters (SW, SE) at --r1=0.25 ... As the control for the assumption that the zero set does not depend on xi1, recount NW at r1 0.25 too: it must give winding 0 as at 0.17 ... Register first; nice 19 under the yield watcher; post the reading on #1076."

## Background
At xi1 0.17 the unresolved quarters SW (A 3.6623456 to 3.7873456, wf 0.20654321 to 0.25654321) and SE (A 3.7873456 to 3.9123456, same wf) each hold a point without value: the corner (3.9123456, 0.20654321), where the continuation in xi1 (accepted at 0.25) loses S_3's zero after 0.24875, and (3.7873456, 0.23154321), where it loses it after 0.175. The recount's radius ladder (zero set taken as xi1-independent; each cell counted at one xi1 with no grid offset) had passes at 0.2 and 0.17.
At r1 0.25 `_continue3` skips every start radius that is not above r1 (its starts are 0.25 and 0.2), so a point had only its direct inner solve: all four NW corners read "no value: continuation lost S_3's zero after [], 5 to 6 CPU s", and each point then went to extended precision (3856 CPU s for the one that finished). At **r1 0.249** the start 0.25 is above r1: a point whose direct solve leaves |r_3| >= 1e-8 is solved at 0.25 (`_refine3`, `_accept3`) and marched one step to 0.249 (h0 0.01 is capped by r1; a failed step is retried with the same target until h < hmin 0.00125, so it is one distinct step). The start 0.2 is not used. The corner's fold is above 0.2475 and below 0.24875 (18 points of the 0.17 cache read trail `[0.25, 0.24875]`), so 0.249 should be reachable.
Data from the level 1 cache (`../fu022mp_corner_e1/m3/points_M3_r0.17.jsonl`, 4228 lines) behind the predictions: of the 3731 float64 rows valued by the continuation 3456 started at 0.25 and 275 at 0.2 (the 0.25 start was rejected by the noise cap); inside the three boxes the cached points are NW 27 (all started at 0.25), SW 10 (9 at 0.25, 1 mp: (3.7873456, 0.23154321)), SE 9 (7 at 0.25, 2 mp: that point and the corner).

## What this run does
Stage 1 (the control): the NW quarter (A 3.6623456 to 3.7873456, wf 0.25654321 to 0.30654321: resolved at 0.17 with boundary winding 2.1e-16, leaf sum 0, no zero) recounted at r1 0.249, `--r1b=0.17`. Stage 2: the SW and SE quarters at r1 0.249. Both with argcount 20ad2589, the options of the recount (`--m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --m3mp`, no `--retry`, `--procs=4`), `--seed` the 0.2 file, `--out m3/` whose 0.249 cache starts empty (every point of the three boxes is computed at 0.249) and whose `points_M3_r0.17.jsonl` is a copy of level 1's cache (4228 lines; the r1b file where the located zeros are found again at 0.17). The lane runs stage 2 only if the control does not fire.
**The control:** PASS = NW resolved at 0.249 with boundary winding 0 (to 1e-6), leaf sum 0 and no zero; FIRES = NW resolved with a nonzero winding, leaf sum or a zero: the work stops and is reported; INCONCLUSIVE = NW unresolved at 0.249 (a point without value): stage 2 still runs and the reading says the control was inconclusive.

## Inputs (copies in this folder; `in_blobs.txt` lists the blobs of this folder's files, `in_blobs_src.txt` those of the source caches; the lane refuses any other blob)
| file | blob |
|---|---|
| `in/cells_nw.jsonl` (the NW quarter, line 2 of `../fu022mp_corner_e1/in/cells_e1.jsonl`) | see `in_blobs.txt` |
| `in/cells_sw_se.jsonl` (the SW and SE quarters, lines 1 and 4 of the same file) | see `in_blobs.txt` |
| `renice_threads.sh`, `read_r249.py` (control and reading, with selftest and `--mutate`) | see `in_blobs.txt` |
| source `../fu022mp_corner_e1/m3/points_M3_r0.17.jsonl`, 4228 lines; `points_M3_r0.2.jsonl`, 1639 lines | 6e9ffcf5; 86ffeb0e |
| code `~/Source/choptuik-large-d-1076b`, detached, clean | 20ad2589 |

## Commands (`lane_r249.sh` in this folder, `start_r249.sh` = systemd user unit `i1076r249` under `systemd-inhibit` with the alert-only memory log; `watch_i1088a_r249.sh` runs beside it)
1. Pins; selftests at nice 19: `argcount.py --selftest` 0 and `--mutate=nosplit`, `conj`, `norecount` 1 each; `argcount_tie_check.py` 0 and `--mutate=pykey` 1; `read_r249.py selftest` 0 and `--mutate` 1 (the planted counts must read PASS, FIRES, INCONCLUSIVE; the mutation ignores the winding). A mode `dry` does only these.
2. Stage 1, cwd the worktree's `solver/inner_stokes`, 4 processes of 1 thread (OMP, OPENBLAS, MKL = 1), nice 10, `timeout 43200`: `argcount.py --recount=in/cells_nw.jsonl --M=3 --r1=0.249 --r1b=0.17 --seed=m3/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --m3mp --out=m3 --tag=M3_fu022mp_r249_nw_r0.249`; then `read_r249.py control` (0 PASS, 1 FIRES stops the lane, 2 INCONCLUSIVE goes on); stage 2 the same with `--recount=in/cells_sw_se.jsonl --tag=M3_fu022mp_r249_lower_r0.249`. `watch_i1088a_r249.sh` sets nice 19 on every thread of the python and its descendants while any `i1088a-*` unit is active (nothing stopped).
3. After it: the first 4228 lines of `m3/points_M3_r0.17.jsonl` and the whole 0.2 file equal the sources (`cmp`), a one-byte edit of a copy fails (1); `read_r249.py reading ...` writes `reading.txt`.

## Acceptance (fixed before the run)
Pins pass; every selftest and control as wanted; both recounts exit 0 (124 at the cap is reported; any other exit stops the lane and I report it); the control does not fire; the prefix checks `0 0 1`. **The reading:** the control's verdict; per quarter resolved or unresolved at 0.249, its boundary winding, leaf sum, zeros with the location at 0.249 and at 0.17 and their difference (for #1080's comparison: the x2 zero moved by less than 8.5e-28 between 0.17 and 0.2); the points of the 0.249 cache without value. A radius of 0.249 instead of 0.25 is the coordinator's choice; nothing else of the order changes.

## Predictions, registered before the run (mine, information)
Basis: the cache data above; at 0.17 every NW point had a float64 value by the 0.25 start, and of the 69 rows level 1 added, 67 are float64 values by the 0.25 start; the other two are the second point's float64 row (lost after 0.175) and its extended-precision row (no value). The corner's no-value row is from the earlier recount.
- Pins pass and every control as wanted (95%).
- **Control:** NW resolved at 0.249 (85%); given resolved, winding 0 with no zero, PASS (95%): PASS 80%, FIRES 3%, INCONCLUSIVE 17%.
- The corner (3.9123456, 0.20654321) has a value at 0.249 in float64 (70%), in float64 or extended precision (80%); (3.7873456, 0.23154321) in float64 (90%).
- SW resolved (70%); SE resolved (65%); both (55%).
- If SW and SE are both resolved: at least one zero located in them (50%); a zero located at both radii agrees to 1e-6 in A and in wf (85%).
- The 0.249 cache has 40 to 150 points in all (65%); at most 3 points without value (65%); at most 4 extended-precision rows (65%).
- Stage 1 done within 1 h of the lane's start (80%); both stages within 4 h (70%), within 8 h (90%).
- The first 4228 lines of the r1b cache and the 0.2 file unchanged (100%).

## Result (lane `lane_r249.sh`, unit `i1076r249`, 2026-11-25 21:35:34 to 23:26:07 UTC, both stages exit 0; `reading.txt` is the reader's output)
**The control passes; the corner and the second point have values at xi1 0.249; SW and SE are still not counted, now for a different reason: the multiplier R jumps along the edge the two quarters share.**
- **Control (stage 1, 4025 s):** NW recounted at r1 0.249: resolved, boundary winding 0.0 (max |leaf winding| 3.5e-16), leaf sum 0, 0 zeros, 40 leaves after 13 splits, 211 points, all with a float64 value. PASS (exit 0; the reader's selftest and `--mutate` as wanted). The control tests a quarter that holds no zero at 0.17 either, so it can fail only by making a zero or a winding appear; it did not.
- **The corner and the second point:** (3.9123456, 0.20654321) has a float64 value by the continuation `[0.25, 0.249]` (58 CPU s): R = 1.60497e7 + 8.30336e7 i. (3.7873456, 0.23154321) likewise (61 CPU s): R = 1.71719e7 + 2.99771e7 i.
- **Stage 2 (SW and SE, 2608 s):** 20 rows added (19 points valued in float64, one with no value after both precisions); the 0.249 cache holds 231 rows, 230 points, 1 extended-precision row, 1 point without value.

| quarter | resolved | boundary winding (as printed) | leaf sum | unresolved leaves | zeros |
|---|---|---|---|---|---|
| NW (control): A 3.66235 to 3.78735, wf 0.25654 to 0.30654 | yes | 0.0 | 0 | 0 | 0 |
| SW: A 3.66235 to 3.78735, wf 0.20654 to 0.25654 | no | -1.0 | 0 | 1 | 0 |
| SE: A 3.78735 to 3.91235, wf 0.20654 to 0.25654 | no | nan | 0 | 1 | 0 |

- **Why SW is unresolved:** on the shared edge A = 3.7873456 the phase step between wf 0.23986841 and wf 0.23987451 (a piece 6.1e-6 long, below hmin 1e-5) is -179.67 degrees, so the edge's refinement ends there unresolved. The two sides are each smooth, and R and F_3 jump across the gap:

| wf (A = 3.7873456) | abs R | arg R (deg) | F_3 | sigma |
|---|---|---|---|---|
| 0.23984399 | 6.02589e7 | +54.416 | -0.041963 - 0.489014 i | 1.24e-1 |
| 0.23986841 | 6.03460e7 | +54.399 | -0.041996 - 0.489005 i | 1.25e-1 |
| 0.23987451 | 8.21076e6 | -125.267 | +0.000263 - 0.511773 i | 6.27e-3 |
| 0.23988061 | 8.20840e6 | -125.271 | +0.000261 - 0.511770 i | 6.03e-3 |

Each side is smooth (left of the gap |R| rises from 3.45e7 at wf 0.2315 to 6.03e7 and flattens toward the gap; right of it |R| falls from 8.21e6 to 3.73e6 at wf 0.2565), and neither goes to 0; all 14 points of the edge between wf 0.2315 and 0.2565 lie on one side or the other. The boundary winding -1.0 of SW sums that step as -0.49908 turns; read the other way round (+0.50092) the same loop gives 0.0, so the printed -1.0 is not a count. What this shows: at xi1 0.249 the point's S_3 zero (F_3) differs by 0.042 + 0.023 i across that gap. What it does not show: whether the jump is a property of the function or of which zero the solve lands on, or where it runs in A (only the one line was sampled).
- **Why SE is unresolved:** the same shared edge, and its east edge midpoint (3.9123456, 0.23154321) has no value: float64 "continuation lost S3's zero after []" (75 CPU s; the 0.25 start is not accepted either), extended precision "|R|/sigma_mp 0.766, NOT valued" (2031 s), the row has |r_3| 4.24e6 (S_3 never converged; as the "0.4" of the corner at 0.17 and "0.0562" of the second point, a ratio at an unconverged solve is not evidence of a zero).
- **The control's quarter is not featureless:** the smallest |R| of the 230 points is 2.15e4 at (3.7639081, 0.257129147) (sigma 1.0e-2; the quarter's four corners have |R| 6.1e5 to 3.7e6); the five leaves with the largest total variation (6.10 to 6.18, depth 4, smallest |R| on their boundaries 2.3e4 to 2.8e4) lie along a line from (3.7639, 0.2597) to (3.7873, 0.2847), and the east edge A = 3.7873456 has 2.9e4 at wf 0.28877 with the phase turning by 145 degrees over wf 0.2878 to 0.2909. All 40 leaves have winding 0 and no zero is located. At xi1 0.17 (a different R) the quarter was 7 leaves of depth at most 2, smallest |R| on a leaf boundary 3.3e5, total variation at most 2.6; nothing there was refined to this depth.
- **#1080's x2 comparison:** no zero was located in any quarter at 0.249, so there is no zero position to compare with 0.17.
- **Checks:** pins and selftests as wanted (argcount 0 1 1 1; tie check 0 and `--mutate=pykey` 1; the reader 0 and `--mutate` 1); prefix check of the 0.17 cache (first 4228 lines) and the 0.2 file: `cmp` 0 0, one-byte edit of a copy 1; the yield watcher set nice 19 on every thread while the i1088a unit was active (12 lines in `i1088a_yield.txt`, nothing stopped).

## Scorecard (the predictions above; "right" = the stated event happened)
| prediction | registered | result |
|---|---|---|
| pins pass and every control as wanted | 95% | right |
| NW resolved at 0.249 | 85% | right |
| control PASS (FIRES 3%, INCONCLUSIVE 17%) | 80% | right |
| the corner has a float64 value at 0.249 | 70% | right |
| the corner has a value in float64 or extended precision | 80% | right |
| (3.7873456, 0.23154321) has a float64 value | 90% | right |
| SW resolved | 70% | wrong |
| SE resolved | 65% | wrong |
| both resolved | 55% | wrong |
| if both resolved: a zero located; agreement 1e-6 | 50%; 85% | not tested (they are not resolved) |
| the 0.249 cache has 40 to 150 points | 65% | wrong (230) |
| at most 3 points without value | 65% | right (1) |
| at most 4 extended-precision rows | 65% | right (1) |
| stage 1 within 1 h | 80% | wrong (67 min) |
| both stages within 4 h | 70% | right (1 h 51 min) |
| both stages within 8 h | 90% | right |
| first 4228 lines of the r1b cache and the 0.2 file unchanged | 100% | right |
The wrong ones share a cause I did not foresee: 0.249 removed the no-value points, but the multiplier itself jumps along the shared edge, and the NW quarter's valley of small |R| took 211 points, not about 30.

## Status
- 2026-11-25 21:34 UTC: folder, inputs (pinned), lane, watcher and README written before any run; `lane_r249.sh dry` is run next, then the unit `i1076r249`.
- 2026-11-25 23:30 UTC: the lane ended (stage 1 exit 0 at 22:42:39, stage 2 exit 0 at 23:26:07, `reading.txt`: control PASS; SW and SE unresolved); Result and Scorecard written above from the files; next: push, post on #1076, report to the coordinator. Nothing else is running.
