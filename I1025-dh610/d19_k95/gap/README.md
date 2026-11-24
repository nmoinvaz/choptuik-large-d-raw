# I1025-dh610/d19_k95/gap: the gap scan of the k_c 95 state at D 19 between 1.435 and 1.535 (closes the pair caveat of ../scan)

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 23:21 UTC, before the scan of this folder. The k_c 95 roots are not yet physical. Roots are read by position, never by sign orientation; the orientation is printed as the reader prints it and not compared across D or k_c.

## Order (coordinator t5, hc 2026-11-23, after the scan of `../scan`, raw 63689583), in part
"read and ruled: D 19's lower root is a discretization root (main 479f0a7d; #1025 comment of 00:00 UTC). Yes to one gap scan only, to close the pair caveat: your k_c 95 state, d18_hybsign at 1.445, 1.465, 1.485, 1.505, 1.525 (5 points, one round, nice 10; the leg lane keeps priority), read_lower. Written before: no sign change in 1.445-1.525 and equal edge signs with 1.435 and 1.535 (all -). Not the 1.0-1.395 scan. Raw I1025-dh610/d19_k95/gap/."

## Method
- `d18_hybsign.py` (xfkappa's, blob e089207a, unmodified) at D 19.0 on this folder's accepted state and record (blobs 545406e4 and 6cfed1aa, `../in_blobs_regrid.txt`; the lane refuses any other blob and requires `../regrid/VERDICT.txt` ACCEPTED), the same files, copies of the tools (`../in_blobs_scan.txt`) and worktrees as `../scan` (scan `~/Source/choptuik-large-d-1025f` at 505d8399; checks `~/Source/choptuik-large-d-1025g` at 48c36355). Five processes of 1 thread, nice 10, one round, one value each: p0 1.445, p1 1.465, p2 1.485, p3 1.505, p4 1.525 (the lane checks the lists against the order and refuses otherwise). The order has no repeat, so none is run (`../scan` showed the repeat of 1.415 bit-identical on this build).
- The source is checked again on the pinned copies before the scan: `kc95_syscheck_1025.py` accepts, `--mutate=F` and `--mutate=steps` exit 1, `kc87_syscheck_1025.py` refuses (exit 1); the lane stops on any other result.
- Reading: `read_lower.py` (blob 89309d3c) on the window 1.435 to 1.535 of `scan/`, which holds the five new rows and the two edge rows (1.435 and 1.535, copied by the lane from `../scan/scan_D19.0_p3.jsonl` and `p4.jsonl` by lambda as `scan_ref_p0.jsonl` and `scan_ref_p1.jsonl`, a written copy of rows the scan already printed, not a re-evaluation). A bracket is the grid step (0.02 here between new points, 0.01 to the edges); the det-linear estimate and the estimator range are a spread over interpolation choices, not an enclosure. A pair of changes closer together than the grid is not seen by this scan: the caveat it closes is for roots at least 0.02 apart.
- `summarize_d19k95_gap.py` prints the tables, the order's rule and the scorecard from the files (selftest exit 0, `selftest --mutate` exit 1, `--mutate` on the real files exit 1 when the control fires).
- Unit `i1025am` (`start_d19_k95_gap.sh`, `lane_d19_k95_gap.sh`, notifier `notify_d19_k95_gap.sh`). Files: `../exits_d19k95_gap.txt`, `scan/`, `src/`, `read_lower_gap.txt`, `summary_gap.txt`. Memory: the lane refuses to start with less than 5 x 4 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08); the sampler only writes `../MEMALERT_gap.txt` below 4 GiB.

## Acceptance (fixed before the run)
- The lane's pins and selftests as wanted (`kc95_syscheck` selftest 0, `read_lower` 0 and mutations `shift` and `round2` 1 1); the k_c 95 check accepts, both controls exit 1, the k_c 87 check refuses; all five processes print "the record system". A control that fires or a check that fails stops the lane and I report it.
- The order's rule, written before: **no sign change in 1.445 to 1.525 and equal edge signs with 1.435 and 1.535 (all -)** closes the pair caveat; a sign change, or a hybrid sign + at any of the five points, leaves it open and is reported by position.
- Reported: the five hybrid signs and ln|det|, every robust change by position, non-robust points, ln|det| minima without a sign change, the float64 sign against the hybrid, seconds per point, peak RSS.

## Predictions, registered before the run (mine, information)
- The pinned copies are accepted with controls 1 1 and the k_c 87 check refusing (96%); all five processes print the record system (93%); every point noise-robust (85%).
- **No robust change in 1.445 to 1.525 and all five hybrid signs -, equal to the edges: 88%** (one change 7%, two or more 5%); ln|det| strictly falls from 1.435 to 1.535 along the seven points (80%; in `../scan` it fell at every step from 1.395 to 1.435 and from 1.535 to 1.545 it is level at -3249.12); ln|det| at 1.525 within 0.3 of -3248.05 (60%; the value of a single zero at lambda_1 = 1.540058 beside the 1.535 point, ln|lambda - lambda_1| plus a smooth part).
- The float64 sign agrees with the hybrid at all five points (85%; at 1.535 it differed).
- Seconds per point 3500 to 6000 s (65%; `../scan` 3763 to 6562 s with 16 threads, now 5 + the leg lane's 8 from about 23:30 UTC, about 65 min, + the recount's 2 = 15 of 20); the lane ends by 01:30 UTC (70%); peak RSS per process below 3.6 GiB (85%; 3.07 to 3.14 GiB in `../scan`).

## Status
- 2026-11-23 23:22 UTC: README, lane and notifier written (the summarizer is written while the scan runs, before its data are read); dry run passed (23:22:29 UTC; the lane's list check refuses a wrong list, tested on a copy); the scan starts after this README is on origin.


## Result (`summarize_d19k95_gap.py` > `summary_gap.txt` prints the tables from the files; its `--mutate` exit 1 with "control FIRED", `selftest` 0, `selftest --mutate` 1)
| lambda | source | process | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|---|---|
| 1.435 | ref (../scan) | - | - | -- (True) | - | -3246.3573767144894 | 5158 |
| 1.445 | new | p0 | - | -- (True) | - | -3246.4236929812714 | 4523 |
| 1.465 | new | p1 | - | -- (True) | - | -3246.598352940766 | 4615 |
| 1.485 | new | p2 | - | -- (True) | - | -3246.8529357825832 | 4711 |
| 1.505 | new | p3 | - | -- (True) | - | -3247.254710582512 | 4510 |
| 1.525 | new | p4 | - | -- (True) | - | -3248.0560314951526 | 4721 |
| 1.535 | ref (../scan) | - | - | -- (True) | + | -3249.124221488627 | 5837 |

new evaluations 5 of 5; seconds per new point min 4510, median 4615, max 4721; not noise-robust: none
float64 sign differs from the hybrid at 0 of 5 new points: none
ln|det| along the seven points: [-3246.35738, -3246.42369, -3246.59835, -3246.85294, -3247.25471, -3248.05603, -3249.12422]; steps [-0.06632, -0.17466, -0.25458, -0.40177, -0.80132, -1.06819]; strictly falling: True

source check on the pinned copies: kc95 exit 0, controls 1 1, kc87 check 1; processes that printed the record system: 5 of 5; peak RSS per process (time -v) [2.46, 2.46, 2.31, 2.49, 2.45] GiB; process exits 0: 5 of 5; scan done line: 00:41:41
read_lower.py on 1.435 to 1.535: points 7 in; robust changes 0: none

the coordinator's rule: closed: no sign change, all seven points -

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/d19_k95/gap/scan 1.435 1.535
points 7 in 1.435-1.535; not noise-robust: none
hybrid signs: 1.435- 1.445- 1.465- 1.485- 1.505- 1.525- 1.535-
float64 sign differs from the hybrid sign at: [(1.535, '-', '+')]
repeated points: none
robust changes: 0; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 1.435, - at 1.535
read_lower exit 0
```

- **The coordinator's rule: closed.** No sign change in 1.445 to 1.525, and the edge signs equal (- at 1.435, - at 1.535): the hybrid sign is - at all seven points, `read_lower.py` finds 0 robust changes, every point is noise-robust, no ln|det| minimum without a sign change. Read by position: none in 1.435 to 1.535. Together with `../scan` (1.395 to 1.435, nine points, all -) the hybrid sign of this k_c 95 state at D 19 is - at 15 distinct lambda from 1.395 to 1.535, with the first change above it at 1.540058 (`../scan`, window 1.535 to 1.545).
- **ln|det| falls at every step** along the seven points (-0.06632, -0.17466, -0.25458, -0.40177, -0.80132, -1.06819; the intervals are 0.01 at both ends and 0.02 between), steepening towards 1.540, consistent with the zero at 1.540058. No dip.
- **What the rule does not exclude (the limit stays):** a pair of sign changes closer together than the spacing between two grid points (0.02 in 1.445 to 1.525, 0.01 at the ends) would not be seen, and the smooth fall of ln|det| at the grid points does not exclude it either. The rule closes the pair caveat for pairs wider than the spacing.
- **float64 sign:** agrees with the hybrid at all five new points; the edge row 1.535 (from `../scan`) differs (float64 +, hybrid -), as it did there. The hybrid sign is the one read.
- **Source:** `kc95_syscheck_1025.py` exit 0 on the pinned copies, `--mutate=F` exit 1, `--mutate=steps` exit 1, `kc87_syscheck_1025.py` exit 1 (`src/`). All five processes printed the record system (|F| 2.9323981061e-10 against the record's 2.9326405268e-10, 3575 steps = the record's).
- **Time and resources:** lane 23:22:55 to 00:41:41 UTC (79 min); scan points 4510 to 4721 s (`../scan`: 3763 to 6562 s). Load average median 14.23 (min 3.36, max 15.98) over `scan/sampler.log`: 5 processes here, the leg lane's 8 (23:29 to 00:26 UTC) and the recount's 2. Peak RSS per process 2.31 to 2.49 GiB (`/usr/bin/time -v`); the sampled total at most 8.35 GiB; MemAvailable at least 39.63 GiB; the alert-only memory log `../memlog_i1025am.log` has no ALERT line.

### Predictions scorecard (written before the run; "right" = the predicted event happened)
| prediction (registered before the run) | result | verdict |
|---|---|---|
| pinned copies accepted, controls 1 1, kc87 refuses (96%) | exits (0, 1, 1, 1) | right |
| all five print the record system (93%) | 5 of 5 | right |
| every point noise-robust (85%) | 7 of 7 | right |
| no robust change and all seven hybrid signs - (88%) | 0 changes, signs ------- | right |
| ln|det| strictly falls along the seven points (80%) | True | right |
| ln|det| at 1.525 within 0.3 of -3248.05 (60%) | -3248.0560314951526 | right |
| float64 sign agrees with the hybrid at all five (85%) | 5 of 5 | right |
| seconds per point 3500 to 6000 s (65%) | 4510 to 4721 | right |
| lane ends by 01:30 UTC (70%) | 2026-11-24 00:41:41 | right |
| peak RSS per process below 3.6 GiB (85%) | max 2.49 GiB | right |

All ten rows are right; the 88% case happened (the 7% and 5% cases did not).

### Status after the scan
- 2026-11-24 00:42 UTC: scan done (lane exit lines in `../exits_d19k95_gap.txt`), result and scorecard above. The pair caveat is closed by the rule; the limit above stands.
