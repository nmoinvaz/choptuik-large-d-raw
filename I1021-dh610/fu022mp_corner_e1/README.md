# I1021-dh610/fu022mp_corner_e1: option (e), level 1: the one unresolved box of the #1076 recount tiled into its four quarters, each recounted as its own box

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1076. Written 2026-11-25 18:24 UTC (the clock), before any run of this folder's work.

## Order (coordinator t5, hc, 25 Nov), the part for (e), verbatim
"Then (e), tiling the box into sub-box cells, one level at a time, only if (d) leaves it unvalued. Register before each: (d) valued = a branch to 0.17 exists from the 0.2 start; else unvalued. Run at nice 19 under the i1088a yield watcher; the quest comes first. Post each reading on #1076."
(d) left the corner unvalued (`../fu022mp_corner_d/`, raw 86a70082; #1076 comment 7170808025), so (e) follows.

## Background
The recount i1076d (`../fu022mp_m3mp/`, raw 3d274b5d) left one unresolved leaf, the box A 3.6623456 to 3.9123456, wf 0.20654321 to 0.30654321. Its corner (3.9123456, 0.20654321) has no value (inner solve for F_3 not converged: float64 continuation lost after [0.25, 0.24875]; extended precision, 34 and 42 digits, no Newton step accepted, |r_3| 3.85e6; also with `--m3starts=0.2,0.25`). The box's other 13 cached boundary points all have float64 values. The recount's own rule: an edge that ends at a point without value is not bisected, and a cell with such an edge is unresolved, so the box's winding is unknown while the corner stays without value. Tiling the box shrinks the part that holds the corner: a quarter whose four corners have values is counted by the recount code like any cell, and the quarter holding the corner stays unresolved.

## What this run does (level 1)
The four quarters of the box (the midpoints A 3.7873456 and wf 0.25654321, computed as argcount's own split computes them, `tile_cells.py` with its checks) as the recount's cells, in the order SW, NW, NE, SE (`in/cells_e1.jsonl`; the SE quarter, which holds the corner (3.9123456, 0.20654321), last). Of the nine corner and edge-midpoint points of the tiling, six are cached and valued (the box's four corners other than the failing one, the left midpoint (3.6623456, 0.25654321) and the top midpoint (3.7873456, 0.30654321)) and the corner is cached without value; **three are new: the bottom midpoint (3.7873456, 0.20654321), the centre (3.7873456, 0.25654321) and the right midpoint (3.9123456, 0.25654321)**. The recount counts each quarter by its boundary (bisecting an edge while a phase step is 0.5 or more, as before; a quarter with winding 0 is split further only by the code's own rules), from a copy of attempt 4's final cache (4159 lines); no `--retry`, so the corner's rows (already in the cache, without value) are not computed again. The quarters' edges shared with the box's old boundary reuse the cached bisection points; the two new inner lines (A 3.7873456 and wf 0.25654321) need new points.

## Inputs (copies in this folder; `in_blobs.txt` lists the blobs of this folder's files, `in_blobs_src.txt` those of the source caches; the lane refuses any other blob)
| file | blob |
|---|---|
| `in/cells_parent.jsonl` (the box; the line of `../fu022mp_m3mp/in/cells_unresolved11.jsonl`) | 45ecd727 |
| `in/cells_e1.jsonl` (the four quarters, from `tile_cells.py in/cells_parent.jsonl ... 3.9123456,0.20654321`) | a19d531e |
| `tile_cells.py`, `read_tiles.py`, `renice_threads.sh` | see `in_blobs.txt` |
| source cache `../fu022mp_m3mp/m3/points_M3_r0.17.jsonl`, 4159 lines; `points_M3_r0.2.jsonl`, 1639 lines | fdfc811a; 86ffeb0e |
| code `~/Source/choptuik-large-d-1076b`, detached, clean | 20ad2589 |

## Commands (`lane_tiles_e1.sh` in this folder, `start_tiles_e1.sh` = systemd user unit `i1076e1` under `systemd-inhibit` with the alert-only memory log; `watch_i1088a_tiles.sh` runs beside it)
1. Pins; selftests at nice 19: `argcount.py --selftest` 0 and `--mutate=nosplit`, `conj`, `norecount` 1 each; `argcount_tie_check.py` 0 and `--mutate=pykey` 1; `tile_cells.py selftest` 0 and `--mutate=drop`, `--mutate=shift` 1 each (the areas of the quarters add to the parent's; the quarters' edges lie on three A and three wf values; exactly one quarter holds the corner); `read_tiles.py selftest` 0 and `--mutate` 1; `tile_cells.py` on the parent reproduces `in/cells_e1.jsonl` byte for byte (`cmp`). Wanted `0 1 1 1 | 0 1 | 0 1 1 | 0 1 | 0 0`. A mode `dry` does only these.
2. The recount, cwd the worktree's `solver/inner_stokes`, 4 processes of 1 thread, nice 10, `timeout 43200`: `argcount.py --M=3 --recount=in/cells_e1.jsonl --r1=0.17 --r1b=0.2 --seed=m3/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --m3mp --out=m3 --tag=M3_fu022mp_corner_e1_r0.17`. `watch_i1088a_tiles.sh` sets nice 19 on every thread of the python and its descendants while any `i1088a-*` unit is active (nothing stopped).
3. After it: the first 4159 lines of the new cache equal the source cache (`head -c | cmp` 0; a one-byte edit of a copy of the source fails it, 1); `read_tiles.py m3/points_M3_r0.17.jsonl 4159 m3/count_M3_fu022mp_corner_e1_r0.17.json` writes `reading.txt`.

## Acceptance (fixed before the run)
Pins pass; every selftest and control as wanted; the recount exits 0 (124 at the cap is reported; any other exit stops the lane and I report it); the prefix check `0 1`; a failing control stops the work and is reported. **The reading:** per quarter, resolved (no unresolved leaf and a finite boundary winding) or unresolved; for each resolved quarter its boundary winding (an integer), leaf sum and zeros (located at xi1 0.17 and 0.2); which of the three new points have a value. The next level tiles the quarter that holds the corner, with its own README section written before it.

## Predictions, registered before the run (mine, information)
Basis: the corner's failure is a fold of the xi1 continuation near 0.2488; the nearest valued points are 0.125 in A (the bottom midpoint) and 0.05 in wf (the right midpoint) from the corner, and 0.07 from it in the scaled distance of the cache's nearest neighbours; 10 of the 11 boxes of the recount resolved; the 8 zeros found lie in 6 of the 10 resolved boxes.
- Pins pass and every control as wanted (95%).
- The new points have a value: bottom midpoint 85%, centre 90%, right midpoint 60%.
- Quarters: SE (holds the corner) unresolved 97%; SW resolved 80%; NW resolved 85%; NE resolved 55%; all three of SW, NW, NE resolved 40%.
- A boundary winding of a resolved quarter is an integer to 1e-9 (95%); at least one zero is located in the resolved quarters (25%).
- The cache grows by 8 to 40 rows (60%), 2 to 12 of them extended-precision rows (55%); at most 2 appended points end without value (65%).
- The lane done within 4 h of its start (60%), within 8 h (85%).
- A level 2 (tiling the SE quarter) is needed (97%).
- The first 4159 lines of the cache unchanged (100%).

## Result of level 1 (20:21 UTC, 25 Nov; the run 18:24:26 to 20:19:26 UTC, 6900 s): two quarters resolved, two unresolved
The recount exited 0 (`reading.txt`, `m3/count_M3_fu022mp_corner_e1_r0.17.json`): 25 leaves after 7 splits, 3893 points (3824 before), 0 zeros, 2 unresolved cells.

| quarter | boundary winding | leaf sum | unresolved leaves | zeros |
|---|---|---|---|---|
| SW: A 3.6623456 to 3.7873456, wf 0.20654321 to 0.25654321 | nan | 0 | 1 | 0 |
| NW: A 3.6623456 to 3.7873456, wf 0.25654321 to 0.30654321 | 2.1e-16 (0) | 0 | 0 | 0 |
| NE: A 3.7873456 to 3.9123456, wf 0.25654321 to 0.30654321 | -7.1e-17 (0) | 0 | 0 | 0 |
| SE: A 3.7873456 to 3.9123456, wf 0.20654321 to 0.25654321 (holds the corner) | nan | 0 | 1 | 0 |

- **The three new points all have a value**, each by the continuation in xi1 (`fix` ok in its row): the bottom midpoint (3.7873456, 0.20654321), the centre (3.7873456, 0.25654321) and the right midpoint (3.9123456, 0.25654321) (rows 4161, 4160 and 4184 of the cache). **One point of the walk has no value: (3.7873456, 0.23154321), the midpoint of the edge A 3.7873456 between the bottom midpoint and the centre**, which SW and SE share, so both stay unresolved (SE also by the corner). Its float64 line reads "no value: continuation lost S3's zero after [0.25, 0.24, 0.23, 0.22, 0.21, 0.2, 0.19, 0.18, 0.175]" (145 CPU s): the continuation went down to 0.175 and lost the zero stepping to 0.17, where the corner lost it after 0.24875. The extended-precision attempt (34 and 42 digits): "|R|/sigma_mp 0.0562, NOT valued", 770 s, |r_3| 3.5e5.
- **NW and NE have no zero**: both boundary windings are zero to 1e-16, so no zero in the 0.125 by 0.05 pieces A 3.6623 to 3.7873 and 3.7873 to 3.9123 at wf 0.25654 to 0.30654. SW and SE, the lower half of the box (wf 0.20654 to 0.25654), are not counted: the winding of each is unknown while the point (3.7873456, 0.23154321) and the corner have no value.
- **The cache:** 4228 lines, 69 appended: 68 float64 rows for 68 distinct points (CPU seconds per point min 72, median 160, max 350, sum 12040) and 1 extended-precision row (the point above); 67 of the 68 points have a value, the one without being that point. The first 4159 lines are unchanged (`cmp` exit 0, the one-byte-edit control exit 1). The yield watcher raised the python and its 4 workers to nice 19 at 18:24:53 UTC (6 pids in `i1088a_yield.txt`, per thread); load median 13.48, max 16.0 over 114 samples, MemAvailable at least 47.7 GiB, no alert.
- **Next:** level 2 tiles the two unresolved quarters (`../fu022mp_corner_e2/`), with its README written before it runs.

### Scorecard of level 1 (registered before the run)
| prediction | result |
|---|---|
| pins pass and every control as wanted (95%) | right |
| the new points have a value: bottom midpoint 85%, centre 90%, right midpoint 60% | right; right; right |
| SE unresolved (97%); SW resolved (80%); NW resolved (85%); NE resolved (55%); all of SW, NW, NE resolved (40%) | right; WRONG (a new midpoint without value); right; right; WRONG |
| a resolved quarter's boundary winding an integer to 1e-9 (95%); at least one zero located in the resolved quarters (25%) | right; WRONG (none) |
| the cache grows by 8 to 40 rows (60%); 2 to 12 of them extended precision (55%); at most 2 appended points without value (65%) | WRONG (69); WRONG (1); right (1) |
| the lane done within 4 h (60%), within 8 h (85%) | right (1.92 h); right |
| a level 2 is needed (97%) | right |
| the first 4159 lines of the cache unchanged (100%) | right |

## Status
- 2026-11-25 18:24 UTC: folder, inputs (pinned), lane, watcher and README written before any run; `lane_tiles_e1.sh dry` is run next, then the unit `i1076e1`. Beside it: the k_c 103 D 22.5 scan (4 processes, `../../I1025-dh610/kc103_d225/`).
- 20:21 UTC: level 1 ended (exit 0, 6900 s): NW and NE resolved with no zero; SW and SE unresolved by the new point (3.7873456, 0.23154321) and the corner.
