# I1021-dh610/fu022mp_corner_d: the one unresolved leaf of the #1076 recount, recounted as its own box with the continuation's start radii 0.2, 0.25 (option (d))

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1076. Written 2026-11-25 18:05 UTC (the clock), before any run of this folder's work.

## Order (coordinator t5, hc, read at about 18:00 UTC 25 Nov), verbatim
"your pick: (d) first, a one-box recount at that corner with --m3starts=0.2,0.25 (one float64 point, then mp if needed). Then (e), tiling the box into sub-box cells, one level at a time, only if (d) leaves it unvalued. Register before each: (d) valued = a branch to 0.17 exists from the 0.2 start; else unvalued. Run at nice 19 under the i1088a yield watcher; the quest comes first. Post each reading on #1076."

## Background (from the closing reading of attempt 4, raw 3d274b5d, `../fu022mp_m3mp/`; comment 7170335870 on #1076)
The recount i1076d ended exit 0 with one unresolved leaf: the box A 3.6623456 to 3.9123456, wf 0.20654321 to 0.30654321. Its corner (3.9123456, 0.20654321) has no value: 14 float64 rows in the cache, all |r_3| 3.8e6 to 1.2e7 (the continuation in xi1 starts at 0.25, which it accepts, and "lost S3's zero after [0.25, 0.24875]", 46 CPU s), and two extended-precision attempts (34 and 42 digits; 805 s in attempt 2, 745 s in attempt 4) that accept no Newton step from the seed F_3 (-0.0006877361546880503, -0.4987022104543663) and leave |r_3| 3.85e6. Only the 0.25 start has ever run at this corner, because the default start order is 0.25, 0.2 and the 0.25 start is accepted. The box's other 13 cached boundary points all have float64 values (top edge 9 points, left 5, bottom and right sides 2 each: the corners), and the walk cannot bisect the bottom and right sides without a value at the corner.

## What this run does
One recount of that one box (`in/cells_corner.jsonl`, the line of `../fu022mp_m3mp/in/cells_unresolved11.jsonl` for this box) with argcount at 20ad2589 and the same options as attempt 4 plus `--m3starts=0.2,0.25` (the continuation starts at xi1 0.2 first, then 0.25) and `--procs=4`, from a copy of attempt 4's final cache (4159 lines, `--retry` computes again only the points without value, which in this box is the corner). The walk takes the box's four corners (three cached), computes the corner in float64 with the new start order, then in extended precision if the float64 row has no value or is blocked by the 10 sigma guard; if the corner has a value it walks the box's bottom and right sides and the box's winding as in the recount. The other points of the cache are not recomputed. `--m3starts` is read by `_continue3` through `_BOUND["starts"]`; `argcount.py --selftest --mutate=starts` ignores the option and its "start order 0.2, 0.25" line fails (the control for this run).

## Inputs (copies in this folder; `in_blobs.txt` lists the blobs of this folder's files, `in_blobs_src.txt` those of the source caches; the lane refuses any other blob)
| file | blob |
|---|---|
| `in/cells_corner.jsonl` (the one box) | 45ecd727 |
| `renice_threads.sh` (copy of `../fu022mp_m3mp/renice_threads.sh`, per-thread renice with a `--mutate` control) | b0f73344 |
| `read_corner.py` (the reading below, with its selftest and `--mutate`) | see `in_blobs.txt` |
| source cache `../fu022mp_m3mp/m3/points_M3_r0.17.jsonl`, 4159 lines | fdfc811a |
| source `../fu022mp_m3mp/m3/points_M3_r0.2.jsonl`, 1639 lines (the seed file and the r1b cache) | 86ffeb0e |
| code `~/Source/choptuik-large-d-1076b`, detached, clean | 20ad2589 |

## Commands (`lane_corner_d.sh` in this folder, `start_corner_d.sh` = systemd user unit `i1076cd` under `systemd-inhibit` with the alert-only memory log; `watch_i1088a_corner.sh` runs beside it)
1. Pins (blobs, code, clean worktree, MemAvailable at least 16 GiB, outputs absent), selftests at nice 19: `argcount.py --selftest` exit 0 and its `--mutate=nosplit`, `conj`, `norecount`, `starts` exit 1 each (wanted `0 1 1 1 1`), `argcount_tie_check.py` exit 0 and `--mutate=pykey` exit 1, `read_corner.py selftest` 0 and `--mutate` 1. A mode `dry` does only these.
2. The recount, cwd the worktree's `solver/inner_stokes`, 4 processes of 1 thread (OMP, OPENBLAS, MKL = 1), nice 10, `timeout 43200`: `argcount.py --M=3 --recount=in/cells_corner.jsonl --r1=0.17 --r1b=0.2 --seed=m3/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --m3starts=0.2,0.25 --procs=4 --retry --m3mp --out=m3 --tag=M3_fu022mp_corner_d_r0.17`. `watch_i1088a_corner.sh` sets nice 19 on every thread of the python and its descendants while any `i1088a-*` unit is active (nothing stopped; `renice_threads.sh`).
3. After it: the first 4159 lines of the new cache equal the source cache (`head -c | cmp`, exit 0) and a one-byte edit of a copy of the source fails the same comparison (exit 1); `read_corner.py m3/points_M3_r0.17.jsonl 4159 m3/count_M3_fu022mp_corner_d_r0.17.json` writes `reading.txt`.

## Acceptance (fixed before the run)
Pins pass; selftests `0 1 1 1 1`; the tie check `0 1`; the reader's selftest `0 1`; the recount exits 0 (124 at the cap is reported; any other exit stops the lane and I report it); the prefix check `0 1`; a failing control stops the work and is reported. **The reading (the order's definition):** (d) is **VALUED** when the corner's last appended row has a finite re and im and a tuned S_3 (|r_3| below 1e-8, or the continuation's `fix` ok), which can only come from the 0.2 start since the 0.25 start is known to lose the zero at 0.24875, i.e. a branch to xi1 0.17 exists from the 0.2 start; otherwise **UNVALUED**. If UNVALUED, (e) follows, one level at a time, with its own README section before it.

## Predictions, registered before the run (mine, information)
Basis: only the 0.25 start was ever tried at this corner; the code comment in `argcount.py` calls the 0.25 start "false" for the synthetic case and the 14 float64 and 2 mp rows of the cache never moved |r_3| below 3.8e6; the neighbours' direct solves at xi1 0.17 converge.
- Pins pass, selftests `0 1 1 1 1`, tie check `0 1`, reader `0 1` (95%).
- **(d) VALUED (35%); UNVALUED (65%).** If UNVALUED, the float64 log line for the corner reads "no value: continuation lost S3's zero after [0.25, 0.24875]" again, the 0.2 start rejected (45% of all outcomes), or after a trail that begins with 0.2 (20%); a different cause (a bound, the wall) 0%.
- If UNVALUED: one extended-precision attempt, NOT valued, 700 to 900 s (75%); the lane done within 30 min of its start (80%); the box's leaf unresolved again, 1 unresolved cell (100% given UNVALUED).
- If VALUED: the float64 row valued by the continuation with the guard passing, no mp attempt (55% of VALUED); the box then resolved with no unresolved cell (55%); its leaf sum 0 (55%), -1 or +1 (45%); at least one new zero located in the box (45%); the new points of the walk number 10 to 30 (60%); the lane done within 4 h (60%).
- The first 4159 lines of the cache unchanged (100%); the cache grows by 1 to 3 rows if UNVALUED (85%).

## Result of (d) (18:21 UTC, 25 Nov; the run 18:06:16 to 18:20:14 UTC, 838 s): UNVALUED
The recount exited 0. **The corner (3.9123456, 0.20654321) has no value with `--m3starts=0.2,0.25`: "no value: continuation lost S3's zero after [0.25, 0.24875], 89 CPU s"** (`logs/recount.log`), the same trail as with the default order, and then the extended-precision attempt "|R|/sigma_mp 0.4, NOT valued, 748 s" (805 s in attempt 2, 745 s in attempt 4). `reading.txt`: corner reading UNVALUED (last row line 4161); the count: boundary winding nan, leaf sum 0, 1 leaf after 0 splits, 3824 points, 1 unresolved cell (the whole box), 0 zeros.
- **What the rows say about the 0.2 start.** The float64 row is bit for bit the earlier one (|r_3| 3831151.090225316, sigma 35697.35189786909, F_3 (-0.0006877361546880503, -0.4987022104543663), trail [0.25, 0.24875], no `bound` entry); the mp row too (info 3849742.1280700336, sigma 49565439.570067756). With `starts` [0.2, 0.25] the continuation tries 0.2 first (the selftest control `--mutate=starts` shows the option is read); a start that `_accept3` does not accept without a cause leaves no `bound` entry and the loop goes on to 0.25, so the record reads as before. The float64 CPU time is 89 s against 46 s in attempts 2 and 4, which is what one more failed start before the 0.25 one costs. So the 0.2 start did not reach |r_3| below 3 times its noise from the seed F_3: **no branch to xi1 0.17 from the 0.2 start**, in the order's words. That the 0.2 start was rejected is read from the extra CPU time and the unchanged record, not from a printed cause: the log has none for a plain non-convergence.
- **The cache:** 4161 lines, 2 appended (the float64 and the mp row of the corner, both without value); the first 4159 lines unchanged (`cmp` exit 0, the one-byte-edit control exit 1). The yield watcher raised the python and its 4 workers to nice 19 at 18:09:42 UTC when an `i1088a-*` unit became active (`i1088a_yield.txt`, 6 pids, all threads); the load in `logs/sampler.log` was 4.87 to 6.51 (13 samples, one a minute), MemAvailable at least 49 GiB, no alert.
- **Next:** (e), tiling the box into sub-box cells, one level at a time, as the order says; its README section is written before it runs.

### Scorecard of (d) (registered before the run)
| prediction | result |
|---|---|
| pins pass, selftests `0 1 1 1 1`, tie check `0 1`, reader `0 1` (95%) | right |
| (d) VALUED (35%); UNVALUED (65%) | UNVALUED: the 65% outcome |
| if UNVALUED, "lost S3's zero after [0.25, 0.24875]" again, the 0.2 start rejected (45% of all outcomes) | right |
| a trail that begins with 0.2 (20%); a different cause, a bound or the wall (0%) | did not happen; did not happen |
| one extended-precision attempt, NOT valued, 700 to 900 s (75%) | right (748 s) |
| the lane done within 30 min of its start (80%) | right (14 min: 18:06:16 to 18:20:14 UTC) |
| 1 unresolved cell given UNVALUED (100%) | right |
| the first 4159 lines of the cache unchanged (100%); 1 to 3 rows added if UNVALUED (85%) | right; right (+2) |

## Status
- 2026-11-25 18:05 UTC: folder, inputs (pinned), lane, watcher and README written before any run; `lane_corner_d.sh dry` is run next, then the unit `i1076cd`. Beside it: the k_c 103 D 22.5 scan (4 processes, `../../I1025-dh610/kc103_d225/`).
- 18:21 UTC: (d) ended UNVALUED (exit 0, 838 s; raw below). (e) level 1 is next.
