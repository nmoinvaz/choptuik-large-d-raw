# I1025-dh610/d19_k95: dh170's k_c 87 D 19 state regridded to k_c 95 on Linux (for dh170's d19_lower, which scans it after its k_c 87 scan)

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 18:30 UTC, before the regrid of this folder (the dry run of the lane, which checks the source, ran at 18:30 UTC). The k_c 95 state is not yet physical.

## Order (coordinator t5, hc), in part
"Added task for your gaps, now, 8 threads at nice 10 beside the leg lane: the k_c 95 regrid at D 19 for dh170's d19_lower (#1025, comment of 17:25), from dh170's accepted k_c 87 state (raw I1025-dh170/d19_lower: state 08e92aca, record b18197d4, tag l1kc87dh170d19; pin by blob): ell_refine.py l1kc87dh170d19 87 l1kc95dh610d19 95 1 19.0 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma, accepted by your kc95_syscheck_1025.py (both controls exit 1, kc87 check refusing). Push the state and record to raw I1025-dh610/d19_k95/ (README first) and report; dh170 scans it after its k_c 87 scan."
dh170's task (#1025 comment of "17:25"): "k_c 87 from winb's accepted k_c 79 D 19 state, then k_c 95 from that k_c 87 state, the same way, and the same two windows; written before: from k_c 87 to 95 on this build the lower root moving less than 0.002 means it converges, more than 0.004 a discretization root." Memory alerts only (standing rule).

## Inputs (copies in `in/`; `in_blobs.txt`; the lane refuses any other blob)
| item | blob |
|---|---|
| dh170's k_c 87 D 19 state `sol_l1kc87dh170d19_D19.0000.npy` and record `l1kc87dh170d19.jsonl` (raw I1025-dh170/d19_lower/k87 at commit 599dff20, "k_c 87 regrid ACCEPTED on Linux (4578 s, |F| 2.8978e-10, 3276 steps, Delta 1.067769696966)") | 08e92aca, b18197d4 |
| `kc87_syscheck_1025.py`, `kc95_syscheck_1025.py` (the k_c 87 check with its k_c test changed to 95, its message and the selftest's planted record, nothing else: `kc95_syscheck_1025.diff`, rebuilt by the lane) | 6df5d960, d487e628 |
Code: `ell_refine.py` 631e5801 and `ell_delta.py` fde699f5 in `~/Source/choptuik-large-d-1025g` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399); python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2). lambda_0(19.0) = 2.1156378446 (`ell_delta.lam0_at`, checked by the lane as a number). The lane is `../kc95_d1975/lane_kc95_regrid.sh` (the same step at D 19.75) with the tag, D, lambda_0, state names and blobs changed.

## Commands (`lane_d19_k95.sh` via `start_d19_k95.sh` = systemd user unit i1025ak under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails)
1. Pins; the selftests of the two checks (exit 0); the source: `kc87_syscheck_1025.py` accepts it (exit 0; `--mutate=F` and `--mutate=steps` exit 1) and `kc95_syscheck_1025.py` refuses it (exit 1). (The dry run of 18:30:28 UTC passed this: exits 0, 1, 1, 1.)
2. The regrid: the order's `ell_refine.py` command, 8 threads, nice 10, cap 21600 s (a time cap only), in `solver/matter` of 1025g; refuses to start with less than 8 GiB free.
3. Acceptance: `kc95_syscheck_1025.py` on the result (exit 0; `--mutate=F` and `--mutate=steps` exit 1) and `kc87_syscheck_1025.py` refusing it (exit 1). On ACCEPTED the state `sol_l1kc95dh610d19_D19.0000.npy` and record `l1kc95dh610d19.jsonl` are copied to this folder's root with their blobs (`in_blobs_regrid.txt`), the files dh170 pins.
Threads: 8 beside the leg lane (8 threads while a point is scanned) and the #1076 recount (nominal 12, two processes in use); nominal 28, real about 18; all at nice 10.

## Acceptance (fixed before the run)
- Source accepted by the k_c 87 check (controls exit 1) and refused by the k_c 95 check; the regrid exits 0 and is accepted by `kc95_syscheck_1025.py` with both controls exit 1 and refused by the k_c 87 check. A failing control stops the work and I report it; no bar is loosened.
- Reported: |F|, steps, the constraint, Delta beside dh170's k_c 87 record (Delta 1.06776969696562, |F| 2.897762648832e-10, 3276 steps, constraint 3.9188e-4) and winb's Windows k_c 95 at D 19 (raw I1025-dh170/d19_lower/k87/in/ref_winb_kc95_d19_regrid_summary.txt: |F| 2.930751034295e-10, 3575 steps, constraint 1.39786e-4, Delta 1.06776937015196, 10230 s), wall.

## Predictions, registered before the run (mine, information)
- Regrid exits 0 (93%) in 3000 to 4500 s (65%; k_c 95 at D 19.75 here took 3066 s, dh170's k_c 87 at D 19 4578 s on his machine); accepted by the k_c 95 check with both controls exit 1 (90%), the k_c 87 check refusing it (97%).
- Steps 3575 +- 40 (65%; winb's 3575; k_c 87 to 95 added 9.13% at winb's D 19 and 9.19% here at D 19.75, on 3276 that is 3575 to 3577). Delta(k_c 95) minus Delta(k_c 87) = -5.13e-07 +- 1.5e-07 (60%; winb's), that is Delta about 1.06776918; norm F 3e-10 to 5e-10 (80%); the constraint within 10% of winb's 1.398e-4 (60%).
- The lane ends 19:20 to 19:55 UTC (the leg lane's D 20.875 scan, due about 19:15 UTC, runs beside it for about 30 minutes).

## Status
- 2026-11-23 18:30 UTC: folder, inputs and lane written; dry run of the source check passed (18:30:28 UTC).
- 2026-11-23 18:31:01 UTC the regrid started (source check passed, unit i1025ak, 8 threads, nice 10); 20:05:29 UTC it exited 0; 20:05:35 UTC the k_c 95 check ACCEPTED it (both controls exit 1, the k_c 87 check refusing); the state and record are copied to this folder's root (`in_blobs_regrid.txt`).

## Result (`python3 -I summarize_d19k95.py > summary.txt` prints the tables and the scorecard from the files; `--mutate` plants a Delta shift of 1e-6 and a norm F scale of 1.4 and exits 1 when the scorecard's verdicts change, which they do)
Acceptance is by `kc95_syscheck_1025.py` (record at its own k_c, |F| at most 1e-9, state |F| within 1% of the record's, freeze_from steps equal), `--mutate=F` and `--mutate=steps` exit 1, and `kc87_syscheck_1025.py` refuses the result: `regrid/syscheck*.txt`, `regrid/steps.txt`, `regrid/VERDICT.txt`.

regrid 2026-11-23 18:31:01 to 2026-11-23 20:05:29 UTC, exit 0, wall 5668 s (the record's seconds 5667); kc95 check exit 0, controls --mutate=F 1, --mutate=steps 1, kc87 check on the result 1; peak RSS (60 s samples) 2.55 GiB

| record | norm F | F_start | steps | constraint | Delta | seconds |
|---|---|---|---|---|---|---|
| dh170 k_c 87 (the source) | 2.897762648832e-10 | 2.992207e-06 | 3276 | 3.918806e-04 | 1.06776969696562 | 4576 |
| this regrid, k_c 95 | 2.932640526780e-10 | 1.185238e-06 | 3575 | 1.397558e-04 | 1.0677690868324767 | 5667 |
| winb k_c 87 (Windows) | 2.900647440612e-10 | 2.992207e-06 | 3276 | 3.919128e-04 | 1.0677698834525378 | 7965 |
| winb k_c 95 (Windows) | 2.930751034295e-10 | 1.183945e-06 | 3575 | 1.397862e-04 | 1.0677693701519553 | 10230 |

Delta(k_c 95) - Delta(k_c 87): here -6.1013e-07 (dh170's k_c 87 source), winb -5.1330e-07; Delta(k_c 95) here minus winb's k_c 95 -2.8332e-07
steps ratio k_c 95 / k_c 87: here +9.1270%, winb +9.1270%; constraint here / winb's k_c 95: -0.0218%; F_start here / winb's +0.1092%

| prediction | result | verdict |
|---|---|---|
| regrid exit 0 (93%) | exit 0 | right |
| wall 3000 to 4500 s (65%) | 5668 s | WRONG |
| kc95 check accepts, controls 1 1 (90%) | exits 0 1 1 | right |
| kc87 check refuses the result (97%) | exit 1 | right |
| steps 3575 +- 40 (65%) | 3575 | right |
| Delta(95) - Delta(87) = -5.13e-7 +- 1.5e-7 (60%) | -6.1013e-07 | right |
| norm F 3e-10 to 5e-10 (80%) | 2.9326e-10 | WRONG |
| constraint within 10% of winb's 1.39786e-4 (60%) | 1.39756e-04 (-0.022%) | right |
| lane ends 19:20 to 19:55 UTC | 2026-11-23 20:05:29 | WRONG |

The new files, for dh170 to pin by blob (`in_blobs_regrid.txt`; copies equal the solver's `data/` files, `cmp`):
```
545406e41043cedb1ea43f4c47e7331ec111eada sol_l1kc95dh610d19_D19.0000.npy
6cfed1aad1633dc961d92c3e8a2bc219d3aa9dc5 l1kc95dh610d19.jsonl
```
Winb's reference summaries (copied from `I1025-dh170/d19_lower/k87/in/`, blobs in `in_blobs_ref.txt`):
```
725b42096fec80ce44bdc64a2afcce780940f72e ref_winb_kc95_d19_regrid_summary.txt  (I1025-dh170/d19_lower/k87/in/ at origin/main 982cc1789ba442b678fb6ff25e29ca4260c01152)
514342325f5bf02b9d2e0e9301fb9fa45ba88b88 ref_winb_kc87_d19_regrid_summary.txt  (I1025-dh170/d19_lower/k87/in/ at origin/main 982cc1789ba442b678fb6ff25e29ca4260c01152)
```

- **Same step count as winb's Windows regrid** (3575, +9.127% over the k_c 87 record's 3276 on both) and the constraint within 0.022% of winb's. |F| is 2.9326e-10, below my registered floor 3e-10 by 2.2%, so that line of the scorecard is WRONG; it is the record class's value (winb's 2.9308e-10, dh170's k_c 87 2.8978e-10).
- **Delta(k_c 95) - Delta(k_c 87) is -6.10e-7 on dh170's k_c 87 state and -5.13e-7 on winb's own pair.** Delta(k_c 95) is 2.83e-7 below winb's. The two k_c 87 sources differ in Delta (dh170's 1.06776969697, winb's 1.06776988345); I did not test why the shifts differ by 0.97e-7. The registered +-1.5e-7 around winb's -5.13e-7 held.
- **The wall was 5668 s**, longer than my 3000 to 4500 s: this regrid ran beside the #1076 recount (2 processes) and, from 19:17 to 19:58 UTC, the D 20.875 leg scan (8 processes); for comparison, dh170's k_c 87 regrid at this D (3276 steps) took 4576 s on his machine, and this machine's k_c 95 regrid at D 19.75 (3411 steps, `../kc95_d1975/l1kc95dh610d1975.jsonl`) took 3064 s. Load as the cause of the longer wall is not tested. Peak RSS (60 s samples) 2.55 GiB.

### Predictions scorecard (written before the run; the table above is from `summarize_d19k95.py`)
Right: exit 0, the k_c 95 check accepting with controls 1 1, the k_c 87 check refusing, steps 3575 +- 40, the Delta difference, the constraint. WRONG: the wall (3000 to 4500 s), norm F (3e-10 to 5e-10: 2.9326e-10), the lane's end time (19:20 to 19:55 UTC: 20:05).


## Next order: the scan of this k_c 95 state at D 19 (coordinator t5, hc 2026-11-23 about 20:08 UTC; written 20:10 UTC, before the scan)
"Next, now, 6 processes at nice 10 (the leg lane keeps priority at ~20:40): the k_c 95 scan of YOUR state at D 19 (#1025, D 19 lower root): d18_hybsign at 1.395-1.435 by 0.005 (9 points, matching winb's Windows k_c 95 window) plus a repeat of 1.415 on another process, and lambda_1 bracketed by 1.535 and 1.545 (12 evaluations, 2 rounds), read_lower on each window. Written before (README): the lower root moving < 0.002 from k_c 87's 1.414576 (dh170, Linux) = converges; > 0.004 or absent in 1.395-1.435 = discretization; lambda_1 within 0.005 of 1.539. Raw I1025-dh610/d19_k95/scan/. dh170 drops its k_c 95 stage; I tell it."
The k_c 95 roots are not yet physical. Roots are read by position, never by sign orientation; the orientation is printed as the reader prints it and not compared across D or k_c.

### Method
- `d18_hybsign.py` (xfkappa's, blob e089207a, unmodified) at D 19.0 on this folder's accepted state and record (root copies, blobs 545406e4 and 6cfed1aa in `in_blobs_regrid.txt`; the lane refuses any other blob and requires `regrid/VERDICT.txt` ACCEPTED). Lists, 6 processes of 1 thread, nice 10, two rounds (the order's 12 evaluations; the lane checks the lists against the order and refuses otherwise, its check tested on a wrong list): p0 1.415, 1.395; p1 1.410, 1.400; p2 1.420, 1.430; p3 1.405, 1.435; p4 1.425, 1.535; p5 1.415 (the repeat, on another process than p0's) and 1.545. Round 1 is the six points around dh170's k_c 87 root; round 2 the window's outer points and the two lambda_1 points.
- Scan tools, copies of the pinned blobs of `../kc95_d1975/in/` (`in_blobs_scan.txt`): `d18_hybsign.py` e089207a, `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9. Worktrees: scan `~/Source/choptuik-large-d-1025f` at 505d8399 (clean), checks `~/Source/choptuik-large-d-1025g` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399); Python 3.14.10, numpy 2.5.4, scipy 1.18.1, python-flint 0.9.0, multidouble 5.1.0 (avx2).
- Reading: `read_lower.py` on each window separately (1.395 to 1.435; 1.535 to 1.545: one call would bracket a change across the 0.1 gap), `repeat_check.py` on the merged file; bracket = the grid step 0.005 (window 2: the two points 0.010 apart, so its det-linear estimate is a single interpolation and its estimator range has no spread); det-linear estimate and estimator range are a spread over interpolation choices, not an enclosure.
- Unit `i1025al` (`start_d19_k95_scan.sh`, `lane_d19_k95_scan.sh`, notifier `notify_d19_k95_scan.sh`). Files: `exits_d19k95_scan.txt`, `scan/`, `scan_src/`, `read_lower_scan.txt`, `selftest_exits_scan.txt`.

### Acceptance (fixed before the run)
- The lane's own pins and selftests as wanted (`kc95_syscheck` selftest 0, `read_lower` 0 and mutations `shift` and `round2` 1 1, `repeat_check` 0; the dry run at 20:09:56 UTC gave 0 0 1 1 0).
- The k_c 95 check accepts the pinned copies on this build, `--mutate=F` and `--mutate=steps` exit 1, the k_c 87 check refuses them (exit 1); all six scan processes print "the record system"; the repeat of 1.415 agrees (`repeat_check.py`). A control that fires or a check that fails stops the lane and I report it. No other control: the reference values (dh170's k_c 87 reading, winb's Windows readings) are of other k_c states, so they are read as comparisons and not as controls; winb's k_c 95 scan is not on origin yet.
- Reported: per window every robust change by position (bracket, det-linear estimate, estimator range, orientation as printed), the edge signs, non-robust points, ln|det| minima without a sign change, the repeat's bits, the float64 sign against the hybrid, seconds per point; the lower root's distance from 1.414576 against the order's rule (< 0.002 converges, > 0.004 or absent discretization, between: no ruling), and lambda_1's distance from 1.539 (bar 0.005). Both estimates sit on a 0.005 grid (lambda_1 on a 0.010 pair), so each is good to about its bracket.
- References (information, not a pass rule): dh170's Linux k_c 87 lower root 1.414576 (t5's hc); winb's Windows lower root 1.410862 at k_c 79 and 1.414532 at k_c 87 on a 0.025 grid, lambda_1 1.539658 and 1.538986 (`../../I1025-dh170/d19_lower/README.md`).

### Predictions, registered before the scan (mine, information)
- The pinned copies are accepted with controls 1 1 and the k_c 87 check refusing (96%); all six processes print the record system (92%); every point noise-robust (70%); the repeat of 1.415 bit-identical (90%).
- Window 1 holds exactly one robust change (85%), edge signs unequal (88%); its det-linear estimate within 0.002 of 1.414576 (75%), 0.002 to 0.004 away (12%), more than 0.004 away or no change (13%); its bracket (1.410, 1.415) (50%), (1.415, 1.420) (40%). Window 2 holds one change with unequal signs at 1.535 and 1.545 (85%), its estimate within 0.005 of 1.539 (75%).
- The float64 sign differs from the hybrid at more than half of window 1's points (30%; at D 19.75, k_c 95, 3 of 7 differed).
- Seconds per point 2300 to 3200 s (65%; k_c 95 at D 19.5: 2238 to 2514 s, at D 19.75: 2442 to 2770 s, four processes beside the other jobs; now 6 processes, the leg lane's 8 from about 20:40 and the recount's 2); round 1 ends by 21:10 UTC (70%) and the lane at 21:30 to 22:10 UTC (60%), started about 20:11 UTC; peak RSS per process below 3.6 GiB (85%; 3.14 to 3.33 GB at D 19.5 and D 19.75).
- Threads: 6 here + the leg lane's 8 (D 20.90625 from about 20:40, about 45 min) + the recount's 2 = 16 of 20, under the 20 (the recount's nominal 12 would make 26; it really runs 2 processes). Nothing is stopped for memory.

### Status
- 2026-11-23 20:10 UTC: README, lane and notifier written; dry run passed (20:09:56 UTC); the scan starts after this README is on origin.

- 2026-11-23 20:10:48 UTC the scan started after the source check passed (kc95 exit 0, controls 1 1, kc87 check 1); 22:57:03 to 23:18:43 UTC the six processes ended, all exit 0; 23:18:43 UTC the reading written (`read_lower_scan.txt`), lane exit 0 (`exits_d19k95_scan.txt`).

### Result (`python3 -I summarize_d19k95_scan.py > summary_scan.txt` prints everything below from the files; selftest exit 0, `selftest --mutate` exit 1, `--mutate` on the real files exit 1 = "control FIRED", `summary_scan_mutate.txt`)
| lambda | process | round | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|---|---|
| 1.395 | p0 | 2 | - | -- (True) | - | -3246.20111370251 | 6562 |
| 1.400 | p1 | 2 | - | -- (True) | - | -3246.2115799315034 | 5551 |
| 1.405 | p3 | 1 | - | -- (True) | - | -3246.224671370778 | 4812 |
| 1.410 | p1 | 1 | - | -- (True) | - | -3246.240334708994 | 5717 |
| 1.415 | p0 | 1 | - | -- (True) | - | -3246.25854191131 | 3763 |
| 1.415 | p5 | 1 | - | -- (True) | - | -3246.25854191131 | 4845 |
| 1.420 | p2 | 1 | - | -- (True) | - | -3246.279299139076 | 5380 |
| 1.425 | p4 | 1 | - | -- (True) | - | -3246.3026403437366 | 4987 |
| 1.430 | p2 | 2 | - | -- (True) | - | -3246.328632507956 | 5029 |
| 1.435 | p3 | 2 | - | -- (True) | - | -3246.3573767144894 | 5158 |
| 1.535 | p4 | 2 | - | -- (True) | + | -3249.124221488627 | 5837 |
| 1.545 | p5 | 2 | + | ++ (True) | + | -3249.1473200273435 | 5928 |

evaluations 12 of 12; seconds per point min 3763, median 5380, max 6562; not noise-robust: none
float64 sign differs from the hybrid in window 1 at 0 of 10 evaluations: none; the repeat of 1.415 (p0 round 1, p5 round 1): ln|det| -3246.25854191131 and -3246.25854191131, bit-identical in sign, noise, float64 and ln|det|: True

source check on the pinned copies: kc95 exit 0, controls 1 1, kc87 check 1; processes that printed the record system: 6 of 6; peak RSS per process (time -v) [3.12, 3.07, 3.14, 3.09, 3.07, 3.1] GiB; process exits: 6 of 6 with exit 0; scan done line: 23:18:43
round 1 ended (start 20:10:48 UTC + the latest first-point seconds 5717) at 21:46 UTC

window 1 (1.395 to 1.435): hybrid signs 1.395- 1.400- 1.405- 1.410- 1.415- 1.420- 1.425- 1.430- 1.435-; robust changes 0: []

window 2 (1.535 to 1.545): hybrid signs 1.535- 1.545+; robust changes 1: [(1.535, 1.545, '- to +', 1.540058, (1.540058, 1.540058))]

repeat_check.py (merged scan file): lambda [1.415]: [2] evaluations each, agree -> PASS

the coordinator's rule, window 1 (all 9 points): ABSENT in the window: discretization
lambda_1, window 2 (both points): roots [1.540058]; within 0.005 of 1.539: True (+0.001058)

| prediction (registered before the run) | result | verdict |
|---|---|---|
| pinned copies accepted, controls 1 1, kc87 refuses (96%) | exits (0, 1, 1, 1) | right |
| all six print the record system (92%) | 6 of 6 | right |
| every point noise-robust (70%) | 12 of 12 | right |
| repeat of 1.415 bit-identical (90%) | True | right |
| window 1: exactly one robust change (85%) | 0 | WRONG |
| window 1: edge signs unequal (88%) | - at 1.395, - at 1.435 | WRONG |
| window 1: estimate within 0.002 of 1.414576 (75%) | none | WRONG |
| window 1: bracket (1.410, 1.415) (50%) or (1.415, 1.420) (40%) | None | WRONG |
| window 2: one change, signs unequal (85%) | 1 change, - at 1.535, + at 1.545 | right |
| window 2: estimate within 0.005 of 1.539 (75%) | [1.540058] | right |
| float64 sign differs from the hybrid at more than half of window 1 (30%; right = it happened) | 0 of 10 evaluations | WRONG |
| seconds per point 2300 to 3200 s (65%) | 3763 to 6562 | WRONG |
| round 1 ends by 21:10 UTC (70%) | 21:46 | WRONG |
| lane ends 21:30 to 22:10 UTC (60%) | 23:18:43 | WRONG |
| peak RSS per process below 3.6 GiB (85%) | max 3.14 GiB | right |

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/d19_k95/scan 1.395 1.435
points 9 in 1.395-1.435; not noise-robust: none
hybrid signs: 1.395- 1.400- 1.405- 1.410- 1.415- 1.420- 1.425- 1.430- 1.435-
float64 sign differs from the hybrid sign at: none
repeated points: [(1.415, 'agree')]
robust changes: 0; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 1.395, - at 1.435
read_lower exit 0
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/d19_k95/scan 1.535 1.545
points 2 in 1.535-1.545; not noise-robust: none
hybrid signs: 1.535- 1.545+
float64 sign differs from the hybrid sign at: [(1.535, '-', '+')]
repeated points: [(1.415, 'agree')]
  robust change (1.535, 1.545), - to +, det-linear 1.540058, range [1.540058, 1.540058]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 1.535, + at 1.545
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/d19_k95/scan/scan_D19.0_1025.jsonl: lambda [1.415]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

- **Window 1 (1.395 to 1.435; 9 grid points, 10 evaluations): no change.** The hybrid sign is - at every point, every point is noise-robust, the float64 sign agrees with the hybrid at all of them, the edge signs are equal, and there is no ln|det| minimum without a sign change (`read_lower.py`). ln|det| falls without a dip from -3246.20111 at 1.395 to -3246.35738 at 1.435. By the coordinator's rule, written before the run: **a lower root absent from 1.395 to 1.435 = discretization**. dh170's Linux k_c 87 root 1.414576 has no counterpart in this k_c 95 state within 0.02 of it. (This is the order's rule applied as written; a wider or finer scan of this state was not ordered and not run.)
- **Window 2 (1.535 to 1.545): one change** between 1.535 and 1.545, "- to +" as printed, det-linear **1.540058**. The window holds two points, so the estimator range collapses to one value; it is not an enclosure, and the bracket is the grid step 0.01. 1.540058 lies +0.001058 from 1.539, within the order's 0.005 (winb's Windows values are 1.539658 at k_c 79 and 1.538986 at k_c 87). The float64 sign at 1.535 is + against the hybrid's - (the hybrid's noise test is robust there); the hybrid is read.
- **The repeat of 1.415** (p0 and p5) is bit-identical in sign, noise signs, float64 sign and ln|det| (`repeat_check.py` PASS).
- **Checks and resources:** source check on the pinned copies passed with both controls exit 1 and the k_c 87 check refusing; all six processes printed the record system (|F| 2.9323981061e-10 against the record's 2.9326405268e-10, 3575 steps equal); peak RSS 3.07 to 3.14 GiB per process (`/usr/bin/time -v`); no `MEMALERT_scan.txt` (MemAvailable stayed above 46 GB); load median 16.00 over `scan/sampler.log` (the leg lane's 8 processes ran from 20:46 to 21:57 and from 22:08 to 23:14 UTC, the recount's 2 throughout).
- **What the data do not say.** Where a lower root of this state lies, if it lies in the range scanned at all: the scan covered 1.395 to 1.435 and 1.535 to 1.545 only. This state differs from winb's k_c 95 state: Delta here minus winb's is -2.8332e-7, and Delta(k_c 95) - Delta(k_c 87) is -6.1013e-7 here against -5.1330e-7 for winb (`summary.txt`). winb's k_c 95 scan is not on origin, so no comparison of the readings is possible yet.
- **Seconds per point were 3763 to 6562 s**, not 2300 to 3200 s: the machine ran 16 threads of mine (6 + 8 + 2) for most of the time, at a load median of 16. Round 1 ended at 21:46 UTC and the lane at 23:18:43 UTC.

### Scan predictions scorecard (written before the scan; "right" = the predicted event happened)
The table above carries the scorecard rows from `summarize_d19k95_scan.py`. The case registered at 13% (more than 0.004 away, or no change in window 1) is the one that happened.
