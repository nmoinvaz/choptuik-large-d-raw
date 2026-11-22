# I1025-dh170/lower_root: #1025 the lower root's track at k_c 63, hybrid sign scans at D 18.5 (lambda 1.20 to 1.54) and D 19.03125 (lambda 1.47 to 1.55)

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-22 11:40:35 UTC, before any run of this folder. Raw origin/main when the inputs were taken: 1c9e7206.

## Order (the coordinator t5's hc, 22 Nov), quoted in part, with its amendment
"The lower root's track at k_c 63. Why: dh370 found two robust changes at D 19 (k_c 63, raw dd910799): + to - at det-linear 1.483165 and - to + at 1.537988 (lambda_1), 0.055 apart, while lambda_1 fell from 1.677 at D 18.5 (slope about -0.28 per unit D). [...] These two scans show whether the two roots are closing, which decides whether lambda_1 leaves the real axis near D 19 to 19.5. Two lanes, 4 threads each, nice 10, each its own systemd user unit, 8 h cap each. Same script as your bisection: xfkappa's d18_hybsign.py (blob e089207a, unmodified), your worktree at 505d8399 and venv; pin each state and record by git hash-object --no-filters in the lane script. Its first line is the system check: exit 3 (not the record system) stops that lane and you report. [...] the reading fixed now: report every robust sign change with its det-linear estimate and range (orientation as printed, not compared across D), the repeat must agree, flag any ln|det| minimum without a change; use a reader with a planted selftest and a mutation control that fires (dh370's read_d19.py from dd910799 or your own d18k2_read.py; name which). No reading of mine is fixed beyond that: I rule on the tracks. Acceptance: both lanes exit 0 with the system check passing, the reader's selftest passes and its mutation fails, the repeats agree."
The amendment, after I reported the Mac's lambda 1.2 reference signs (hc, same day): "change both windows before you launch. Lane A: D 18.5 (the Mac's k_c 63 state and record, as ordered), lambda 1.20 to 1.54 at 0.02 (18 values), plus a repeat of 1.30 at the end. The Mac's d185 scan covers 1.55 up; use its 1.55-1.61 minus signs only as you said, as a cross-machine control, not as lane points. Lane B: D 19.03125 instead of 18.84375: state I1025-dh370/kc63_leap/sol_l1kc63dh370_D19.031250.npy with record I1025-dh370/kc63_leap/l1kc63dh370.jsonl (its D 19.03125 line), lambda 1.47 to 1.55 at 0.005 (17 values), plus a repeat of 1.51. [...] Write both windows and this prediction in the README before the run (the prediction is information, not a pass rule)."

## Inputs (copies in `in/`, each pinned in `lane_lower_dh170.sh` by `git hash-object --no-filters` and taken from raw origin/main by `git cat-file blob`, checked against the tree)
| item | raw path | blob |
|---|---|---|
| lane A state | I1025-mac/d18/sol_l1kc63Wm1025_D18.5000.npy | 33c1a58b |
| lane A record (the stub `d18_stub_l1kc63W1025.jsonl` holds only the D 18 line, so the leap's file is used) | I1025-mac/d18/l1kc63Wm1025.jsonl, its D 18.5 row: F 2.7672415504e-10, 2461 steps, kappa 0.7, u0 0.04, Ks 30, h 0.0625 | 08f4dbf3 |
| lane B state | I1025-dh370/kc63_leap/sol_l1kc63dh370_D19.031250.npy | 53f3bd29 |
| lane B record | I1025-dh370/kc63_leap/l1kc63dh370.jsonl, its D 19.03125 row: F 2.6210543403e-10, 2368 steps, h 0.03125 | 168213b0 |
| the scanner | I1025-mac/d18/d18_hybsign.py | e089207a |
| the change finder (xfkappa's) | I1025-mac/d18/d185_scan_read.py, d18c_read.py, d18d_read.py | 7c9d400f, 1383470f, 6b608903 |
| dh370's reader | I1025-dh370/read_d19.py at dd910799 | 13bd4997 |
| the Mac's D 18.5 data on lane A's state (cross-machine control) | I1025-mac/d18/d18_refsign_1025.jsonl (lambda 1.2 and 2.6 at D 17.75 to 18.5), I1025-mac/d18/d185_scan_1025.jsonl (1.55 to 1.90) | 3e2d8b4e, 90540daf |
Code: worktree `~/Source/choptuik-large-d-1025p4` at 505d8399 (clean, checked by the lane), python the #1058 venv (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble's package with `dd_logdet`), as the scans of `../kc_break_D18.46875`.

## The commands
Each lane: `lane_lower_dh170.sh A|B`: pins, the planted `ell_ddm.py selftest` (must PASS) and `--mutate=slices` (must FAIL), then `nice -n 10 /usr/bin/time -v python -u d18_hybsign.py REC STATE D LAMS lane<X>/scan_D<D>_p0.jsonl` with 4 threads (OPENBLAS, OMP, MKL, VECLIB, RAYON = 4), an 8 h cap by exact pid, a memory sampler every 30 s (alert only). The lanes and the reader run as systemd user units, so no terminal owns them:

    systemd-run --user --unit=i1025-lowA --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 lower_root lane A D 18.5" --mode=block ./lane_lower_dh170.sh A
    systemd-run --user --unit=i1025-lowB --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 lower_root lane B D 19.03125" --mode=block ./lane_lower_dh170.sh B
    systemd-run --user --unit=i1025-lowread --working-directory=$PWD ./read_lower.sh        (waits for both lanes, then reads)

| | lane A | lane B |
|---|---|---|
| D | 18.5 | 19.03125 |
| window (hybrid sign, noise test 1e-15 on blocks 0-11 with 2 seeds, float64 sign beside) | lambda 1.20, 1.22, ..., 1.54 (18 values), then a repeat of 1.30 | lambda 1.470, 1.475, ..., 1.550 (17 values), then a repeat of 1.510 |
| evaluations | 19 | 18 |
| estimate at 425 to 650 s a point | 2.2 to 3.4 h | 2.1 to 3.3 h |

## Reader and its controls
**Reader: `read_lower.py` (mine), laid out as dh370's `read_d19.py` (blob 13bd4997, kept here unchanged as `read_d19.py`) with xfkappa's `d185_scan_read.changes` unchanged.** I changed two things, because `read_d19.py` keys the points by `round(lam, 2)`, which merges neighbours on lane B's 0.005 grid, and `d18c_read.minima` decides "beside a change" after rounding to two decimals, which mislabels a minimum on that grid: lambda keys and prints at three decimals, and a minimum finder with the same definition (an interior point whose ln|det| is below both neighbours') that matches the change's bracket by 1e-9. Its planted selftest has six cases on both grids (a root on lane A's grid; two roots 0.034 apart on lane B's; a non-robust point at a change; a deep minimum WITHOUT a change at 1.505 whose two-decimal rounding equals the neighbouring change's endpoints; a minimum with no change; a repeat that agrees and one that does not) and passes (`selftest_read_lower.log`). Two mutations each make it exit 1: `--mutate=shift` (the change finder's estimates move by 0.003: cases 1 and 2 fail, `selftest_read_lower_mutate_shift.log`) and `--mutate=round2` (the two-decimal matching: case 4 fails, `selftest_read_lower_mutate_round2.log`). The unmodified `read_d19.py` passes its own selftest and `--mutate=shift` exits 1 (`selftest_read_d19*.log`); the reading script also runs it on lane A (a 0.02 grid it can read) as a second reader.
Also: `repeat_check.py` (the repeated lambda must repeat sign, ln|det| within 1e-6, noise signs and float64 sign; selftest passes) and `cross_check_mac.py` (selftest passes), both from the earlier folders or new here.

## Reading, fixed now (the coordinator's; no reading is fixed beyond this, the coordinator rules on the tracks)
For each lane: report every robust sign change (both neighbouring points noise-robust) with its bracket, orientation as printed, det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure); changes touching a non-robust point are listed and not counted; flag every ln|det| minimum without a sign change (no dip fit unless the coordinator asks); the repeat (lambda 1.30 at lane A, 1.510 at lane B) must agree, or "repeat disagrees; no reading". The float64 sign is reported beside the hybrid's (information). Orientation is each state's own and is not compared across D.
**Cross-machine control, lane A (information, not a pass rule):** the Mac scanned this same state: its lambda 1.2 at D 18.5 is minus, ln|det| -1896.5871419008333 (`d18_refsign_1025.jsonl`), and its 1.55 to 1.61 are minus (`d185_scan_1025.jsonl`). Lane A's 1.20 must read minus and noise-robust, with the ln|det| difference printed (flagged above 1e-6); its 1.54 is compared with the Mac's 1.55 (the seam).

## Prediction (the coordinator's lines; information, not a pass rule)
The coordinator's two straight lines: the lower root from (D 18.28, 1.2) to (D 19, 1.4832), +0.3933 per unit D, and lambda_1 from (D 18.5, 1.677209) to (D 19, 1.537988), -0.2784 per unit D. They meet near D 19.08. At **D 19.03125** they give the lower root near 1.4955 and lambda_1 near 1.5293, 0.034 apart: brackets (1.495, 1.500) and (1.525, 1.530) on lane B's 0.005 grid (at D 19: 1.4832 and 1.5380, 0.0548 apart). At **D 18.5** the lower line puts the root near 1.2865: bracket (1.28, 1.30) on lane A's grid. If the 1.2 crossing near D 18.28 is not the same root, lane A shows no such change.
**A parity fact I noted before the run:** at D 18.5 the Mac's signs at lambda 1.2 (minus) and at 1.55 (minus) are equal, so the number of sign changes between them is even. A lone lower root in lane A's window (1.20 to 1.54) would contradict that, unless a change lies in the unscanned gap (1.54, 1.55) or the 1.2 point has a different sign convention: lane A should show 0 or 2 changes (or 1 with its partner in (1.54, 1.55)). The sign at lambda 1.2 also flips at D 18.0 to 18.0625 and again at D 18.25 to 18.3125 (`d18_refsign_1025.jsonl`), which the Mac's notes read as root crossings; I have not checked that against the step-count parity of the states (`d18_refsign_parity.py`).
**My own probabilities, registered before the runs:** system checks pass 95% each; the repeats agree 90% each; every point noise-robust: lane A 65%, lane B 80%; lane A's 1.20 equals the Mac's sign 90%, its ln|det| within 1e-6 60%; lane B shows both changes inside 1.47 to 1.55 80%, with the lower bracket within 0.01 of (1.495, 1.500) 55% and the lambda_1 bracket within 0.01 of (1.525, 1.530) 60%; their gap smaller than D 19's 0.0548 85%; lane A shows 0 changes 40%, 2 changes 25%, 1 change 25%, other 10%; the float64 sign differs at no more than 5 points: lane A 40%, lane B 60%; the wall of a lane 2.1 to 3.4 h 65%, both inside the 8 h cap 95%; max RSS below 2.5 GiB 90%.

## Acceptance (the coordinator's)
Both lanes exit 0 with the system check passing; the reader's selftest passes and its mutation fails; the repeats agree. I report any lane that stops (exit 3 included) and post the result on #1025 when the reader ends.

## Budget
Two processes of 4 threads each at nice 10 (as the bisection). No other job of mine or of the i349 agent runs on dh170 as I write this (load average 0.2).

## Discrepancy with the order's premise (reported to t5 before the run, accepted)
The order says no scan has looked below 1.62 at D 18.5. The Mac's scan `d185_scan_1025.jsonl` of this state covers 1.55 to 1.90 at 0.01 (7 points below 1.62, all minus) and `d18_refsign_1025.jsonl` holds single points at lambda 1.2 for D 17.75 to 18.5. The windows were changed on that.

## Log
- 2026-11-22 11:40:35 UTC: folder, scripts, controls and pins prepared; the windows, the reading and the prediction are fixed above before any run. Controls run now: `read_lower.py` selftest PASS, `--mutate=shift` and `--mutate=round2` FAIL; `read_d19.py` selftest PASS and `--mutate=shift` FAIL; `cross_check_mac.py` and `repeat_check.py` selftests PASS; dry runs of both lanes pass their pins.

## Result (written 2026-11-22 14:59:06 UTC)
Both lanes exit 0, system checks passed (lane A |F| 2.7728396616e-10 against the record's 2.7672415504e-10, 2461 steps; lane B 2.6199729092e-10 against 2.6210543403e-10, 2368 steps), every point noise-robust, both repeats bit-identical (lane A's 1.30: ln|det| -1898.608474126855, lane B's 1.510: -1874.413401245264). The reader exit 0 at 14:57:55 UTC (`read_lower.txt`, `exits_read.txt`). Peak RSS 1.44 and 1.43 GiB, lowest MemAvailable 25.7 and 25.7 GiB (26484 and 26280 MiB), no ALERT line.

| | lane A (D 18.5, lambda 1.20 to 1.54, 19 evaluations) | lane B (D 19.03125, lambda 1.470 to 1.550, 18 evaluations) |
|---|---|---|
| started, ended (UTC), exit | 11:41:05, 14:57:40, 0 | 11:41:09, 14:46:33, 0 |
| wall | 11795 s (3:16:29 by /usr/bin/time) | 11124 s (3:05:23) |
| seconds per point | 401 to 672, mean 620 (the last two after lane B ended: 499 and 401) | 604 to 635, mean 618 |
| hybrid signs | all minus, 1.20 to 1.54 | plus from 1.470 to 1.520, minus from 1.525 to 1.550 |
| robust changes | **none** | **one**, (1.520, 1.525), plus to minus as printed: det-linear 1.523736, estimator range [1.523601, 1.523736]; none minus to plus |
| ln|det| minima without a sign change | none (ln|det| falls monotonically, -1896.587 at 1.20 to -1899.868 at 1.54) | none |
| repeat | 1.30 agrees (`repeat_check.py` PASS, the reader's check 'agree') | 1.510 agrees |
| float64 sign differs from the hybrid | none | 3 of 18 (1.530, 1.535, 1.540: minus against plus; float64 reads +-+++-- from 1.520 to 1.550) |

- **Cross-machine control, lane A:** the 1.20 point reads minus and noise-robust, as the Mac's reference point on the same state; its ln|det| -1896.5871396622 against the Mac's -1896.5871419008, difference 2.24e-6, flagged above 1e-6 (information). The seam: lane A's 1.54 is minus and the Mac's 1.55 (and its 1.55 to 1.61) is minus, so an even number of changes between them. With the Mac's scan, the hybrid sign of this state has no change from 1.20 to 1.67; lambda_1 (minus to plus) is at 1.677.
- **Parity note:** lane A shows 0 changes (the 40% case); a lone lower root near 1.29 is not there, no change in (1.28, 1.30).
- **Second reader:** the unmodified `read_d19.py` reads lane A the same (0 changes, repeat agrees).
- **Reader controls (run before the lanes):** `read_lower.py` selftest passes, `--mutate=shift` and `--mutate=round2` each exit 1; `read_d19.py` selftest passes and `--mutate=shift` exits 1; `repeat_check.py` and `cross_check_mac.py` selftests pass.

**Against D 19 (dh370, raw dd910799; k_c 63; orientation is not compared across D, so this is arithmetic and no reading):** D 19: plus to minus at 1.483165, minus to plus at 1.537988 (lambda_1). D 19.03125 (here): plus to minus at 1.523736 only, none minus to plus up to 1.550. If the orientations carry over, the plus-to-minus change moved +0.0406 in 0.03125 of D (+1.30 per unit D, against +0.39 in the order's line) and the minus-to-plus change is above 1.55 (while lambda_1 fell -0.28 per unit D from D 18.5 to D 19). If the sign convention flipped between the two states, the one change here is lambda_1 moved -0.0143 (-0.46 per unit D) and the other root is below 1.47 or gone. This window cannot say which; the other change's position and orientation can, at D 19.03125 outside 1.47 to 1.55. The lower root is a k_c 63 root, not yet a physical one (t5: win2's k_c 71 scan at D 19 has one change, 1.536547, and none near 1.4832).

## Predictions against the result
| prediction | result |
|---|---|
| system checks pass 95%; repeats agree 90%; every point noise-robust (A 65%, B 80%) | yes; yes; yes, yes |
| lane A's 1.20 equals the Mac's sign (90%); its ln|det| within 1e-6 (60%) | yes; **no**, 2.24e-6 |
| lane A: 0 changes 40%, 2 changes 25%, 1 change 25% | 0 |
| lane B: both changes inside 1.47 to 1.55 (80%) | **no**, one |
| lane B: lower bracket within 0.01 of (1.495, 1.500) (55%) | **no**: the one change is 0.025 away |
| lane B: the lambda_1 bracket within 0.01 of (1.525, 1.530) (60%) | position yes, (1.520, 1.525); orientation as printed no (plus to minus) |
| their gap smaller than D 19's 0.0548 (85%) | not defined: one change |
| float64 differs at no more than 5 points: A 40%, B 60% | A yes (0), B yes (3) |
| wall 2.1 to 3.4 h 65%; inside 8 h 95%; RSS below 2.5 GiB 90% | 3.28 h and 3.09 h yes; yes; yes |

## Log
- 2026-11-22 11:41:04 to 11:41:11 UTC: lanes A, B and the reader started (units `i1025-lowA`, `i1025-lowB`, `i1025-lowread`).
- 2026-11-22 12:39 UTC to 14:46 UTC: lane B's plus-to-minus change appeared at the point 1.525 (12:5x UTC) and was reported to t5 at once; the rest of lane B stayed minus.
- 2026-11-22 14:59:06 UTC: result written (this section).
