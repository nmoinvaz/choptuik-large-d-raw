# I1021-dh610/fu022mp_jump_width: width in A of the region where S_3 has two roots, xi1 0.249, around A = 3.7873456 (#1076)

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1076. Written 2026-11-25 23:59 UTC (the clock), before any run of this folder's work.

## Order (coordinator t5, hc, read at about 23:58 UTC on 25 Nov), verbatim
"Run (a) now, the 32 two-seed solves for the width of the two-valued region, nice 19, registered first. Hold (b)." (The design question (c) is answered separately, in `../fu022mp_sheet_design/`.)

## Background
`../fu022mp_jump_map/` (raw 64847d86, #1076 comment 7178214031): at xi1 0.249, S_3 has two roots at the same (A, wf) at six locations, all on A = 3.7873456 (wf 0.21904 to 0.25654 and the gap's two points); at A = 3.7248456 and 3.8498456 (0.0625 either side) the two seeds gave the same root. This run measures how wide in A the two-valued region is.

## What this run does
`width_jump.py` (argcount.py 20ad2589 imported unchanged from `~/Source/choptuik-large-d-1076b`, detached, clean; r1 0.249, `--m3fix`, bounds rhs 2.4e6, wall 3600 s, noise3 1e7, no extended precision, 4 processes of 1 thread, nice 10 raised to 19 by `watch_i1088a_width.sh` while an i1088a unit is active) solves the 18 locations A = 3.7873456 + {-0.03125, -0.016, -0.004, -0.001, 0, +0.001, +0.004, +0.016, +0.03125} on the rows wf 0.23154321 and 0.24404321, each from two forced seeds: the L root and the R root that the map found on A = 3.7873456 at that row (row 0.23154321: L -0.031400 - 0.492804 i, R +0.003241 - 0.517495 i; row 0.24404321: L -0.047713 - 0.487970 i, R -0.000390 - 0.509708 i; read from the map's caches by the script). 36 solves in two passes (L, R), caches in `m3/`. The order said 32 solves: the 32 at the 16 offsets other than 0, plus the 4 at offset 0 that are the repeat check. About 40 CPU s each: about 25 CPU min, about 10 min of wall time on 4 processes if the machine is free.
**Reading** (`read_width.py`, from the files, no number typed by hand): per row and offset the F_3 and |r_3| of the L and R solves; class **two roots** = both valued and F_3 differing by more than 0.01; **one root** = within 1e-3; between; one seed only; none. The **two-valued width** of a row, west and east = the largest |offset| of the unbroken run of two-root offsets going out from 0. **Repeat check (a control that can fail):** at offset 0 the L and R solves reproduce the map's two roots of that row within 1e-4 and are two roots; if not the reader exits 1 and the lane stops and reports.

## Inputs (`in_blobs.txt`: blobs of this folder's files; `in_blobs_src.txt`: of the map's L and R caches; the lane refuses any other blob)
| file | blob |
|---|---|
| `width_jump.py`, `read_width.py` (selftest and `--mutate`: the forced seed is the seed, row by row; the classes and widths; the repeat comparison), `renice_threads.sh` | see `in_blobs.txt` |
| `../fu022mp_jump_map/m3/points_M3_r0.249_L.jsonl`, `..._R.jsonl` | 24073feb; 2dbd938c |
| code `~/Source/choptuik-large-d-1076b`, detached, clean | 20ad2589 |

## Commands (`lane_width.sh`, `start_width.sh` = systemd user unit `i1076wid` under `systemd-inhibit` with the alert-only memory log; `watch_i1088a_width.sh` beside it)
1. Pins; selftests at nice 19: `argcount.py --selftest` 0 and `--mutate=starts` 1; `width_jump.py selftest` 0 and `--mutate` 1; `read_width.py selftest` 0 and `--mutate` 1; the worktree still clean. Mode `dry` does only these.
2. cwd `solver/inner_stokes`: `nice -n 10 timeout 7200 python -u width_jump.py run ../fu022mp_jump_map m3/`; then the sources unchanged (blobs); `read_width.py reading` writes `reading.txt`.

## Acceptance (fixed before the run)
Pins and selftests as wanted; the run exits 0 (124 at the cap is reported); the sources unchanged; the repeat check passes (if it fires the work stops and is reported). The reading reports each row's classes and its west and east widths with the resolution of the offsets.

## Predictions, registered before the run (mine, information)
Basis: the map found one root at 0.0625 either side at the rows 0.25654, 0.21904 and (3.8498456, 0.23154321) and the two roots at A = 3.7873456 differ by 0.04 to 0.06 with smooth variation, so the second root's region is narrower than 0.0625 on both sides there.
- Pins, selftests as wanted (95%); the repeat check passes (90%).
- At least 28 of the 36 solves have a float64 value (70%).
- Two roots at the offsets +-0.001 and +-0.004 on both rows (4 offsets per row, 8 locations in all) (70%).
- Two roots at +-0.016 on both rows (all 4 locations) (40%); at +-0.03125 on both rows (all 4) (15%).
- The width (west and east) is the same on the two rows (50%).
- The run is done within 20 min of the start (70%), within 1 h (95%).

## Result (lane `lane_width.sh`, unit `i1076wid`, 2026-11-26 00:00:10 to 00:05:41 UTC, exit 0 after 329 s, `reading.txt` is the reader's output)
**The two-valued region is wider than the 0.001 and 0.004 of the first guess: two roots at every offset up to +-0.03125 on both rows (35 of 36 solves valued), with one exception at the east end of the upper row; with the map's one-root columns at +-0.0625 its edges lie between 0.03125 and 0.0625 from A = 3.7873456 on each side. The two roots do not come together toward its ends.**
- **Repeat check (control): PASS.** At offset 0 the L and R solves reproduce the map's two roots of both rows to 4e-12, 3e-13 (row 0.24404321) and 7e-12, 2e-12 (row 0.23154321) (wanted 1e-4), and are two roots. Selftests and pins as wanted.
- **Solves:** 36, of which 35 have a float64 value; the one without is the L solve at (3.8185956, 0.24404321) (continuation lost at xi1 0.25; the R solve there is valued).
- **Two roots (L and R valued, F_3 differing by 0.034 to 0.077)** at A = 3.7873456 + {-0.03125, -0.016, -0.004, -0.001, 0, +0.001, +0.004, +0.016} on the row wf 0.24404321 and at all nine offsets on the row wf 0.23154321. Unbroken widths from offset 0: row 0.24404321 west 0.03125, east 0.016 (the next, +0.03125, has the R root only); row 0.23154321 west 0.03125, east 0.03125.

| wf | A offset | L root F_3 | R root F_3 | abs difference |
|---|---|---|---|---|
| 0.24404321 | -0.03125 | -0.051429 - 0.531808 i | -0.002251 - 0.505690 i | 0.0557 |
| 0.24404321 | 0 | -0.047713 - 0.487970 i | -0.000390 - 0.509708 i | 0.0521 |
| 0.24404321 | +0.016 | -0.046835 - 0.470229 i | +0.001466 - 0.514294 i | 0.0654 |
| 0.24404321 | +0.03125 | no value | +0.003389 - 0.520492 i | |
| 0.23154321 | -0.03125 | -0.036049 - 0.517541 i | -0.002840 - 0.509501 i | 0.0342 |
| 0.23154321 | 0 | -0.031400 - 0.492804 i | +0.003241 - 0.517495 i | 0.0425 |
| 0.23154321 | +0.03125 | -0.027716 - 0.478174 i | +0.012416 - 0.543932 i | 0.0770 |

- **Edges of the region, with the map:** at A = 3.7248456 (0.0625 west) both seeds gave one root at both rows; at A = 3.8498456 (0.0625 east) one root at wf 0.23154321 and the R root only at wf 0.24404321. So the width in A is between 0.0625 and 0.125 at these rows (resolution: the offsets above and the map's columns).
- **The roots do not merge toward the ends.** The difference |F_3(L) - F_3(R)| is 0.034 to 0.077 over the whole region and larger at the east end of the lower row (0.0770 at +0.03125, 0.0425 at 0). The L root moves faster than the R root (row 0.24404321: Im F_3 -0.532 at -0.03125 to -0.470 at +0.016; the R root -0.506 to -0.514). So these data do not show the L root ending in a fold with the R root; how it ends (a fold with a third root, a singular locus of the inner integration, or leaving the region the solve reaches) is not shown. A proxy for the conditioning of J_3 stored in the records, dr1/(|r_3| + noise_3) (which scales as |J_1 |J_3^-1||), does not grow toward the ends (L 12 to 33, R 4 to 11); it is not det J_3.
- **Checks:** the map's caches unchanged (blobs); the yield watcher set nice 19 on every thread while the i1088a unit was active (nothing stopped).

## Scorecard (the predictions above; "right" = the stated event happened)
| prediction | registered | result |
|---|---|---|
| pins, selftests as wanted | 95% | right |
| the repeat check passes | 90% | right (4e-12 or better) |
| at least 28 of the 36 solves valued | 70% | right (35) |
| two roots at +-0.001 and +-0.004 on both rows (8 locations) | 70% | right |
| two roots at +-0.016 on both rows (4 locations) | 40% | right |
| two roots at +-0.03125 on both rows (4 locations) | 15% | wrong (3 of 4; the 4th has no L value) |
| the same width (west, east) on the two rows | 50% | wrong (east 0.016 against 0.03125) |
| done within 20 min | 70% | right (5.5 min) |
| done within 1 h | 95% | right |
The basis of the predictions (narrower than 0.0625 either side) held for the edges; the region is wider than I expected from the three rows of the map.

## Status
- 2026-11-25 23:59 UTC: folder, inputs (pinned), scripts and README written before any run; `lane_width.sh dry` next, then the unit `i1076wid`.
- 2026-11-26 00:06 UTC: the lane ended (exit 0 at 00:05:41, repeat check PASS, `reading.txt`); Result and Scorecard written above from the files; next: push, post on #1076 with the pointer to the design, report to the coordinator. Nothing is running.
