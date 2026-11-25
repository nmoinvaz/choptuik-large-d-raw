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

## Result (lane `lane_map.sh`, unit `i1076map`, 2026-11-25 23:36:00 to 23:53:03 UTC, map exit 0 after 1018 s, `reading.txt` is the reader's output)
**Two roots of S_3 exist at the same (A, wf) at 6 of the 27 locations, all in the column A = 3.7873456 (wf 0.21904 to 0.25654 and the gap's two points); in the other four columns the two forced seeds give the same root, so by the case defined before the run the jump is *isolated* to that column. A look at the F_3 values afterwards (not registered) shows another change of sheet between two rows of the column A = 3.8498456, so the isolated verdict is a statement about where the forced seeds find two roots, not a proof that the switch ends there.**
- **Repeat check (control): PASS.** The L solve at the gap's lower point and the R solve at its upper point reproduce the recount's F_3 to 2.1e-12 and 1.7e-12 (wanted 1e-4). Prefix check `0 1`, selftests as wanted.
- **Solves:** 57 of the 68 new solves have a float64 value (STD 11 of 14, L 22 of 27, R 24 of 27). The 11 without: 4 hit the right-hand-side bound 2.4e6 at xi1 0.25 (A 3.8498456 wf 0.24404321 with the L seed; A 3.9123456 wf 0.21904321 and 0.23154321, L and R, and STD at 0.21904321), the others read "continuation lost S3's zero after []".
- **The six two-root locations** (L = the root the L seed reaches, R = the R seed's; the L and R solves differ in F_3 by 0.043 to 0.066; the same root from the two seeds agrees to 5e-11 or better at the 16 one-root locations):

| wf (A = 3.7873456) | L root F_3 | R root F_3 | abs difference | STD landed on |
|---|---|---|---|---|
| 0.25654321 | -0.065105 - 0.490114 i | -0.000929 - 0.504301 i | 0.0657 | R |
| 0.24404321 | -0.047713 - 0.487970 i | -0.000390 - 0.509708 i | 0.0521 | R |
| 0.239874508828 (gap, upper) | -0.042004 - 0.489003 i | +0.000263 - 0.511773 i | 0.0480 | R |
| 0.239868405312 (gap, lower) | -0.041996 - 0.489005 i | +0.000264 - 0.511777 i | 0.0480 | L |
| 0.23154321 | -0.031400 - 0.492804 i | +0.003241 - 0.517495 i | 0.0425 | L |
| 0.21904321 | -0.020753 - 0.499035 i | +0.017642 - 0.543063 i | 0.0584 | L |

At wf 0.20654321 of the same column both seeds give one root, -0.017250 - 0.501176 i (the L root's continuation: the R root is not found there).
- **So the recount's jump is the nearest-seed rule switching sheets inside a region where S_3 has two roots:** the STD solves land on the R root for wf >= 0.24404 and on the L root for wf <= 0.23154, and R is two-valued on the whole edge A = 3.7873456 from wf 0.21904 to 0.25654. The L root is tuned (|r_3| 1e-5 to 1e-4) at all five grid rows of the edge and at the gap; the R root at the top four grid rows and at the gap, not at wf 0.20654.
- **Other columns (A spacing 0.0625):** one root at 16 locations (L, R and, where it has a value, STD agree to 7e-11); R seed only at (3.8498456, 0.24404321) and (3.6623456, 0.20654321); no value from any pass at (3.7248456, 0.20654321), (3.9123456, 0.21904321) and (3.9123456, 0.23154321); STD only has no value at (3.8498456, 0.23154321) (L and R both give +0.009343 - 0.563006 i).
- **Case, by the definition registered before the run:** the STD labels contain both L and R only in the column A = 3.7873456: **isolated**. Map (class / STD landed on; 2 two roots, 1 one root, r R seed only, - none; L, R, B both seeds, . no value):

| wf \ A | 3.6623 | 3.7248 | 3.7873 | 3.8498 | 3.9123 |
|---|---|---|---|---|---|
| 0.25654 | 1/B | 1/B | 2/R | 1/B | 1/B |
| 0.24404 | 1/B | 1/B | 2/R | r/R | 1/B |
| 0.23154 | 1/B | 1/B | 2/L | 1/. | -/. |
| 0.21904 | 1/B | 1/B | 2/L | 1/B | -/. |
| 0.20654 | r/R | -/. | 1/B | 1/B | 1/B |

- **After the run, not registered (read off `reading.txt`):** in the column A = 3.8498456 F_3 goes +0.001520 - 0.519322 i, +0.004966 - 0.535041 i, +0.009343 - 0.563006 i (wf 0.25654, 0.24404, 0.23154; steps 0.016, 0.028) and then -0.015074 - 0.486649 i, -0.012461 - 0.493561 i (wf 0.21904, 0.20654; a step of 0.080 between 0.23154 and 0.21904, then 0.007), each with one root found from both seeds; the second root of those rows, if it exists, was not reached. The columns A = 3.6623456 and 3.7248456 change smoothly over all rows with values (steps 0.006 to 0.018). That is consistent with the switch of sheets running from the gap (3.7873456, 0.239871) east and down to between wf 0.21904 and 0.23154 at A = 3.8498456 and on toward the east edge, where the three points without value lie (3.9123456, wf 0.21904 and 0.23154), and not into the west half. Resolution: 0.0625 in A, 0.0125 in wf; no point lies between the columns.
- **What this shows and does not show:** R, as the recount builds it, is two-valued along the shared edge A = 3.7873456 from wf 0.21904 to 0.25654, so the phase of the loop around SW or SE depends on which root each point lands on (the printed SW winding -1.0 or 0.0 by the reading of the step). It does not show which root is the one wanted, whether the two roots exist at xi1 0.17 or 0.2, how wide the two-valued region is in A (below 0.125 at the rows tested, since the neighbours at +-0.0625 give one root), or that SE can be counted at 0.249: its east edge has no value at wf 0.21904 and 0.23154 in any pass (the right-hand-side bound 2.4e6 or a lost zero).
- **Checks:** the source cache and the STD cache's first 231 lines unchanged (`cmp` 0, one-byte edit 1); the yield watcher set nice 19 on every thread while the i1088a unit was active (nothing stopped).

## Scorecard (the predictions above; "right" = the stated event happened)
| prediction | registered | result |
|---|---|---|
| pins, selftests and prefix checks as wanted | 95% | right |
| the repeat check passes | 90% | right (2e-12) |
| both seeds valued at both gap points | 80% | right |
| the gap's two points are two-root | 65% | right |
| at least 55 of the 68 new solves valued | 65% | right (57) |
| two-root locations in a column other than A = 3.7873456 | 60% | wrong (none) |
| at least 3 of the 27 locations two-root | 60% | right (6) |
| all 27 two-root | 5% | no (6) |
| case: line / isolated / other | 40% / 25% / 35% | isolated (25%) |
| done within 45 min | 60% | right (17 min) |
| done within 2 h | 90% | right |

## Status
- 2026-11-25 23:35 UTC: folder, inputs (pinned), scripts and README written before any run; `lane_map.sh dry` next, then the unit `i1076map`.
- 2026-11-25 23:55 UTC: the lane ended (map exit 0 at 23:53:03, repeat check PASS, `reading.txt`); Result and Scorecard written above from the files; next: push, post on #1076, report to the coordinator. Nothing is running.
