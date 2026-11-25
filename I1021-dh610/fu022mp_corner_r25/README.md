# I1021-dh610/fu022mp_corner_r25: the two unresolved quarters of the #1076 box recounted at xi1 0.25, with the NW quarter as the control for "the zero set does not depend on xi1"

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1076. Written 2026-11-25 20:25 UTC (the clock), before any run of this folder's work.

## Order (coordinator t5, hc, 25 Nov, read at about 20:22 UTC), verbatim
"take your option instead of deeper tiling: recount the two unresolved quarters (SW, SE) at --r1=0.25, the radius at which the continuation is accepted at the corner and at (3.787, 0.2315). As the control for the assumption that the zero set does not depend on xi1, recount NW at r1 0.25 too: it must give winding 0 as at 0.17 (and #1080's x2 zero did not move between r1 0.17 and 0.2, to 8.5e-28). Register first; nice 19 under the yield watcher; post the reading on #1076."
This replaces level 2 of (e) (`../fu022mp_corner_e1/` ended with NW and NE resolved, no zero; SW and SE unresolved; raw 894d6684; #1076 comment 7173569846). A level 2 folder was prepared and not run; it is in the Trash.

## Background
At xi1 0.17 the unresolved quarters SW (A 3.6623456 to 3.7873456, wf 0.20654321 to 0.25654321) and SE (A 3.7873456 to 3.9123456, same wf) each hold a point without value: the corner (3.9123456, 0.20654321), where the continuation in xi1 (accepted at 0.25) loses S_3's zero after 0.24875, and (3.7873456, 0.23154321), where it loses it after 0.175 (their midpoint of the shared edge; extended precision does not value either). `argcount.py`'s recount is a rung of a radius ladder: its comment says the zero set does not depend on xi1 and each cell is counted at one xi1, so a cell unresolved at one radius is counted again at another with no grid offset; the passes so far were at xi1 0.2 (the first count, #1021) and 0.17 (the recount). Here the rung is **xi1 0.25**, where the corner and the second point have values from the continuation's own start.
At r1 0.25 `_continue3` has no start (its start radii 0.25 and 0.2 are not above 0.25), so a point needs its direct inner solve (`nested.inner`) to tune S_3 below 1e-8 (or be blocked only by the 10 sigma guard, then `--m3mp`); a point whose direct solve fails has no value. That is an unknown of this run.

## What this run does
Stage 1 (the control): the NW quarter (A 3.6623456 to 3.7873456, wf 0.25654321 to 0.30654321: resolved at 0.17 with boundary winding 2.1e-16, leaf sum 0, no zero) recounted at r1 0.25, `--r1b=0.17`. Stage 2: the SW and SE quarters recounted at r1 0.25. Both with argcount 20ad2589, the options of the recount (`--m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --m3mp`, no `--retry`, `--procs=4`), `--seed` the 0.2 file, `--out m3/` whose 0.25 cache starts empty (every point of the three boxes is computed at 0.25) and whose `points_M3_r0.17.jsonl` is a copy of level 1's cache (4228 lines; the r1b file where the located zeros are found again at 0.17). The lane runs stage 2 only if the control does not fire.
**The control (the order's):** PASS = NW resolved at 0.25 with boundary winding 0 (to 1e-6), leaf sum 0 and no zero; FIRES = NW resolved with a nonzero winding, leaf sum or a zero: the work stops and is reported; INCONCLUSIVE = NW unresolved at 0.25 (a point without value): stage 2 still runs and the reading says the control was inconclusive.

## Inputs (copies in this folder; `in_blobs.txt` lists the blobs of this folder's files, `in_blobs_src.txt` those of the source caches; the lane refuses any other blob)
| file | blob |
|---|---|
| `in/cells_nw.jsonl` (the NW quarter, line 2 of `../fu022mp_corner_e1/in/cells_e1.jsonl`) | see `in_blobs.txt` |
| `in/cells_sw_se.jsonl` (the SW and SE quarters, lines 1 and 4 of the same file) | see `in_blobs.txt` |
| `renice_threads.sh`, `read_r25.py` (control and reading, with selftest and `--mutate`) | see `in_blobs.txt` |
| source `../fu022mp_corner_e1/m3/points_M3_r0.17.jsonl`, 4228 lines; `points_M3_r0.2.jsonl`, 1639 lines | 6e9ffcf5; 86ffeb0e |
| code `~/Source/choptuik-large-d-1076b`, detached, clean | 20ad2589 |

## Commands (`lane_r25.sh` in this folder, `start_r25.sh` = systemd user unit `i1076r25` under `systemd-inhibit` with the alert-only memory log; `watch_i1088a_r25.sh` runs beside it)
1. Pins; selftests at nice 19: `argcount.py --selftest` 0 and `--mutate=nosplit`, `conj`, `norecount` 1 each; `argcount_tie_check.py` 0 and `--mutate=pykey` 1; `read_r25.py selftest` 0 and `--mutate` 1 (the planted counts must read PASS, FIRES, INCONCLUSIVE; the mutation ignores the winding). A mode `dry` does only these.
2. Stage 1, cwd the worktree's `solver/inner_stokes`, 4 processes of 1 thread (OMP, OPENBLAS, MKL = 1), nice 10, `timeout 43200`: `argcount.py --recount=in/cells_nw.jsonl --M=3 --r1=0.25 --r1b=0.17 --seed=m3/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --m3mp --out=m3 --tag=M3_fu022mp_r25_nw_r0.25`; then `read_r25.py control` (0 PASS, 1 FIRES stops the lane, 2 INCONCLUSIVE goes on); stage 2 the same with `--recount=in/cells_sw_se.jsonl --tag=M3_fu022mp_r25_lower_r0.25`. `watch_i1088a_r25.sh` sets nice 19 on every thread of the python and its descendants while any `i1088a-*` unit is active (nothing stopped).
3. After it: the first 4228 lines of `m3/points_M3_r0.17.jsonl` and the whole 0.2 file equal the sources (`cmp`), a one-byte edit of a copy fails (1); `read_r25.py reading ...` writes `reading.txt`.

## Acceptance (fixed before the run)
Pins pass; every selftest and control as wanted; both recounts exit 0 (124 at the cap is reported; any other exit stops the lane and I report it); the control does not fire; the prefix checks `0 0 1`. **The reading:** the control's verdict; per quarter resolved or unresolved at 0.25, its boundary winding, leaf sum, zeros with the location at 0.25 and at 0.17 and their difference (for #1080's comparison: the x2 zero moved by less than 8.5e-28 between 0.17 and 0.2); the points of the 0.25 cache without value.

## Predictions, registered before the run (mine, information)
Basis: the corner and (3.787, 0.2315) have values from the continuation's 0.25 start; a direct solve at 0.25 is a different, untested thing for 100 or so new points; NW at 0.17 had a winding 0 and 13 of the box's 14 cached points valued.
- Pins pass and every control as wanted (95%).
- **Control:** NW resolved at 0.25 (60%); given resolved, winding 0 with no zero, PASS (95%): PASS 57%, FIRES 3%, INCONCLUSIVE 40%.
- The corner has a value at 0.25 (70%); (3.7873456, 0.23154321) has a value (85%).
- SW resolved (55%); SE resolved (45%); both (38%).
- If SW and SE are both resolved: at least one zero located in them (50%); a zero located at both radii agrees to 1e-6 in A and in wf (85%).
- The 0.25 cache has 60 to 200 points (65%); at most 6 points without value (60%); at most 10 extended-precision rows (60%).
- Both stages done within 4 h of the lane's start (55%), within 8 h (85%).
- The first 4228 lines of the r1b cache and the 0.2 file unchanged (100%).

## Status
- 2026-11-25 20:25 UTC: folder, inputs (pinned), lane, watcher and README written before any run; `lane_r25.sh dry` is run next, then the unit `i1076r25`.
- 2026-11-25 21:32 UTC: **stopped by the coordinator's order** (hc of 25 Nov, "go with --r1=0.249 as a replacement: stop the r1 0.25 lane by exact pid, keep its one mp row in the record"; the replacement is `../fu022mp_corner_r249/`). TERM to the exact pids 2123529 (lane), 2123602 (sampler loop), 2123607 (stage 1 subshell) and 2123608 (timeout); the unit `i1076r25` is inactive and no process of it is left. Stage 1 had run 1 h 07 min: all four NW corners had no float64 value (the direct solve fails in 5 to 6 CPU s and `_continue3` has no start radius above r1 0.25), the extended-precision attempt at (3.6623456, 0.30654321) was valued (3856 CPU s, |R|/sigma_mp 1e28, R 6.05e5 + 1.02e5 i), the other three attempts were at about 64 CPU min and unfinished. `m3/points_M3_r0.25.jsonl` keeps its 5 rows (4 without value, 1 mp row valued) as the record. No control, reading or count came out of this lane, so the predictions above are unscored: the run did not reach their events. What it showed: at r1 0.25 a point costs about 1 CPU hour in extended precision when float64 has no start.
