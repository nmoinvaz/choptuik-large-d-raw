# I1021-dh610/fu022mp_jump_map: float64 map of the M = 3 inner solve's F_3 around the jump of R at (3.7873456, 0.239871), xi1 0.249, lower half of the #1076 box

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1076. Written 2026-11-25 23:35 UTC (the clock), before any run of this folder's work.

## Order (coordinator t5, hc, 25 Nov, read at about 23:32 UTC), verbatim
"yes, the float64 map of F_3 around (3.7873456, 0.239871): about 25 points, 4 procs, nice 19 under the yield watcher, registered first (a branch-switch line of the inner solve, crossing the edge, vs an isolated jump). Report where the line runs through the lower half; post on #1076."

## Background
`../fu022mp_corner_r249/` (raw 7fc6c6d8, #1076 comment 7177674490): at xi1 0.249 the recount of SW and SE stays unresolved because on the shared edge A = 3.7873456 the multiplier R jumps between wf 0.23986841 and wf 0.23987451 (6.1e-6 apart): phase step -179.67 degrees, |R| 6.03e7 to 8.21e6, F_3 from -0.041996 - 0.489005 i to +0.000263 - 0.511773 i; each side is smooth. An inner solve starts from a seed F_3, and the recount's seed rule is "the F_3 of the nearest valued point" (`Multiplier.seed`), so the root a point lands on may depend on the seed. This run asks whether two roots of S_3 exist at the same (A, wf) (then R is two-valued there and the jump is where the nearest-seed rule switches) or one (then the jump is where a root ends or R really jumps), and where the jump runs through the lower half.

## What this run does
`map_jump.py` (argcount.py 20ad2589 imported unchanged from `~/Source/choptuik-large-d-1076b`, detached, clean; r1 0.249, `--m3fix`, bounds rhs 2.4e6, wall 3600 s, noise3 1e7, no extended precision, 4 processes of 1 thread, nice 10 raised to 19 by `watch_i1088a_map.sh` while an i1088a unit is active) solves the 27 locations: a 5 x 5 grid, A in {3.6623456, 3.7248456, 3.7873456, 3.8498456, 3.9123456} (spacing 0.0625), wf in {0.20654321, 0.21904321, 0.23154321, 0.24404321, 0.25654321} (spacing 0.0125), and the gap's two points (3.7873456, 0.239868405312) and (3.7873456, 0.239874508828). Three passes, each its own `Multiplier` and cache in `m3/`:
- **STD:** the recount's rule, from a copy of its final cache (231 lines, `../fu022mp_corner_r249/m3/points_M3_r0.249.jsonl`; the 13 of the 27 locations already in it are not solved again) plus the 0.2 file's seeds: 14 new solves, in one batch.
- **L:** every one of the 27 solved with the seed forced to the F_3 of the gap's lower point (-0.041996 - 0.489005 i); **R:** forced to the F_3 of its upper point (+0.000263 - 0.511773 i). 27 solves each, caches start empty.
The order said about 25 points: this is 27 locations and 68 new solves (14 + 27 + 27), about 40 CPU s each in the recount, so about 45 CPU min, about 12 min of wall time on 4 processes if the machine is free.
**Reading** (`read_map.py`, from the files, no number typed by hand): per location the F_3 and |r_3| of the three solves; class **two roots** = the L and R solves are both valued and their F_3 differ by more than 0.01 (the gap's two roots differ by 0.048; the same root from two seeds differs by 1e-4 or less, tested by the repeat check); **one root** = within 1e-3; **between** (flagged); one seed only; none. "STD landed on" = L or R when the STD solve's F_3 is within 1e-3 of that seed's root. A map of the grid prints both. **Repeat check (a control that can fail):** the L solve at the gap's lower point and the R solve at its upper point must reproduce the recount's F_3 of those points within 1e-4; if not the reader exits 1 and the lane stops and reports.
**The order's two cases, defined before the run:** a *line* = in at least 3 of the 5 grid columns the STD labels down the column contain both L and R (the switch crosses the lower half), the gap's column included; *isolated* = only the gap's column A = 3.7873456 has both L and R in its STD labels; anything else is reported as it is.

## Inputs (`in_blobs.txt`: blobs of this folder's files; `in_blobs_src.txt`: of the two source caches; the lane refuses any other blob)
| file | blob |
|---|---|
| `map_jump.py`, `read_map.py` (selftest and `--mutate`: the forced seed is the seed; the classes and labels; the repeat check passes and fires), `renice_threads.sh` | see `in_blobs.txt` |
| `../fu022mp_corner_r249/m3/points_M3_r0.249.jsonl` (231 lines), `points_M3_r0.2.jsonl` | cf3861be; 86ffeb0e |
| code `~/Source/choptuik-large-d-1076b`, detached, clean | 20ad2589 |

## Commands (`lane_map.sh`, `start_map.sh` = systemd user unit `i1076map` under `systemd-inhibit` with the alert-only memory log; `watch_i1088a_map.sh` beside it)
1. Pins; selftests at nice 19: `argcount.py --selftest` 0 and `--mutate=starts` 1; `map_jump.py selftest` 0 and `--mutate` 1; `read_map.py selftest` 0 and `--mutate` 1; the worktree still clean. Mode `dry` does only these.
2. cwd `solver/inner_stokes`: `nice -n 10 timeout 14400 python -u map_jump.py run <source cache> <0.2 file> m3/`; then the source cache is unchanged, the STD cache's first 231 lines equal it (`cmp` 0), a one-byte edit of a copy fails (1); `read_map.py reading` writes `reading.txt`.

## Acceptance (fixed before the run)
Pins and selftests as wanted; the map exits 0 (124 at the cap is reported); the prefix checks `0 1`; the repeat check passes (if it fires, the work stops and is reported). **The reading** reports, for each location, what the three solves gave, the classes, the STD labels and the map, and then which of the two cases (line, isolated, other) it is, and where the L to R switch of the STD labels runs through the lower half, with the resolution of the grid (0.0625 in A, 0.0125 in wf; the gap itself is 6.1e-6 wide in wf at A = 3.7873456).

## Predictions, registered before the run (mine, information)
Basis: both sides of the gap are smooth (F_3 changes by 1e-5 to 1e-3 per step of the bisection on each side), neither |R| nor F_3 shows a fold approaching, and the recount's seeds come from the nearest valued point, so a second root would be reached only from its own side.
- Pins, selftests and prefix checks as wanted (95%); the repeat check passes (90%).
- At the gap's two points both the L and the R solve are valued (80%), and they are two roots there (65%).
- At least 55 of the 68 new solves have a float64 value (65%).
- Two-root locations exist in a column other than A = 3.7873456 (60%); at least 3 of the 27 locations are two-root (60%); all 27 are (5%).
- Case: line 40%, isolated 25%, other 35%.
- The map is done within 45 min of the start (60%), within 2 h (90%).

## Status
- 2026-11-25 23:35 UTC: folder, inputs (pinned), scripts and README written before any run; `lane_map.sh dry` next, then the unit `i1076map`.
