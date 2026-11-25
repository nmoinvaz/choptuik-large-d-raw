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

## Status
- 2026-11-25 21:34 UTC: folder, inputs (pinned), lane, watcher and README written before any run; `lane_r249.sh dry` is run next, then the unit `i1076r249`.
