# I1025-dh610/kc79_d195: k_c 79 at D 19.5 on dh370's regridded state: the control at D 19.125 first, then the hybrid sign scan at lambda_1 1.41 to 1.50

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../kc71_d1925up/` (raw 93fce3d7), which ends k_c 71's roots: "half of the k_c 79 scan at D 19.5 (dh370 takes 1.30-1.40)".

## Order (the coordinator's)

1. **Control, 1 process:** `d18_hybsign.py` on dh370's k_c 79 D 19.125 state and record (raw `I1025-dh370/kc79_d19125/`, c58e5052; blobs pinned) at lambda 1.50. It must print the record system and dh370's hybrid sign and ln|det| at 1.50 (-2537.823195774449) to 1e-9 relative (dh170 matched it to 1.1e-15). Stop and report if not.
2. **Scan,** when dh370 pushes its accepted k_c 79 D 19.5 state and record (`I1025-dh370/kc79_d195/`; the coordinator forwards the commit): lambda 1.41 to 1.50 at 0.01 (10 values) plus a repeat of 1.45, 6 processes of 1 thread, nice 10, a systemd unit, `read_lower.py`. The k_c 79 line puts lambda_1 near 1.404 at D 19.5 (information, not a pass rule).
3. Report every robust change with det-linear estimate and range, the edge signs, any ln|det| minimum without a change; k_c 79 roots. Estimate: control about 15 min, scan 2 rounds of about 15 to 20 min. Post on #1025 and send the verdict with the raw commit.

The cross-machine record at k_c 79 (information): the control at D 19.0 of `../kc79_d19low/` differed from winb's Windows build by 1.914e-6 relative in ln|det| with this machine's own spread over 1, 2 and 4 threads at 2.9e-15 (raw c0d4213f); the bar here is 1e-9 against dh370's Linux build, which dh170's run matched to 1.1e-15.

## Setup

Budget: 1 process of 1 thread for the control (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, a systemd user unit `i1025n` (`lane_kc79_d195_control.sh`, started by `start_kc79_d195_control.sh`, log `exits_kc79_d195.txt`); nothing else of mine runs. Worktree `~/Source/choptuik-large-d-1025f` clean at 505d8399 (its `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` are the ones dh370's worktree 48c36355 matched, README of `I1025-dh370/kc79_d19125/`), interpreter `~/Source/venv-i1058/bin/python`.

Inputs (dh370's, raw `I1025-dh370/kc79_d19125/` at c58e5052, copied to `in/`; pinned by `git hash-object --no-filters`, `in_blobs.txt`; the lane refuses on any other blob): `sol_l1kc79dh370_D19.1250.npy` 3ff3fcb5, `l1kc79dh370.jsonl` 15ac964f (the D 19.125 line is used), `ref_dh370_scan_kc79_D19.125_1025.jsonl` 9a6ef239 (dh370's scan of that state; its lambda 1.50 rows, both -2537.823195774449, bit-identical), `d18_hybsign.py` e089207a (xfkappa's, unmodified). For the scan: `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9 (dh170's, unedited).

## Commands

1. `d18_hybsign.py in/l1kc79dh370.jsonl in/sol_l1kc79dh370_D19.1250.npy 19.125 1.50 control/scan_D19.125_p0.jsonl`, cap 3 h by exact pid, 1 process of 1 thread, nice 10.
2. `control_check.py control/control.log control/scan_D19.125_p0.jsonl in/ref_dh370_scan_kc79_D19.125_1025.jsonl 1.50`: pass only if the log prints `the record system`, the hybrid sign equals dh370's (-1) and ln|det| equals dh370's -2537.823195774449 to 1e-9 relative. Its selftest (planted agreeing rows for a + and a - reference and a 5e-10 shift pass; a not-the-record-system log, both sign flips and a 1e-8 shift fail) must exit 0 and its `--mutate` (bar raised to 1e-6) must exit 1: `selftest_control_exits.txt`, wanted 0 1. The bar is not changed whatever the control reads.

## Acceptance (the coordinator's)

- the control prints the record system and matches dh370's sign and ln|det| to 1e-9 relative; otherwise stop and report, no scan. The scan has its own lane, written after the state arrives.

Written as the run goes.

## Control (22 Nov, 19:16:46 to 19:29:24 UTC): PASS, bit-identical to dh370's row

`d18_hybsign.py` at D 19.125, k_c 79, lambda 1.50 on dh370's state and record, 1 process of 1 thread: exit 0, wall 758 s (the point's own 756 s), peak RSS 1.77 GB (`control/control.log`, `control/control_check.txt`, `exits_kc79_d195.txt`).
- the record system: |F| 2.9254572718e-10 against the record's 2.9245143117e-10 (relative 3.2e-4, inside the check's 1e-2 bar), steps 2949 = 2949; the printed |F| is the one dh370's log prints;
- hybrid sign -1 = dh370's -1; both noise seeds -1 (noise_robust True);
- **ln|det| -2537.823195774449 against dh370's -2537.823195774449: relative difference 0.000e+00 (bar 1e-9): PASS**; the float64 ln -2534.506173253555 and sign -1 also equal dh370's.
The bar was not touched. The scan of the order (`lane_kc79_d195_scan.sh`, unit `i1025o`) started at 19:30:05 UTC on dh370's D 19.5 state and record (raw f40a4556; `sol_l1kc79dh370d195_D19.5000.npy` 9528b355, `l1kc79dh370d195.jsonl` 5777d2a2): lambda 1.41, 1.42, 1.43, 1.44, 1.45, 1.45 (the repeat, process 5; its original runs on process 4), 1.46 to 1.50; 11 evaluations on 6 processes of 1 thread, nice 10, log `exits_kc79_d195_scan.txt`; the reading is `read_lower.py scan 1.41 1.50` and `repeat_check.py` (`read_lower.txt`), selftests wanted 0 1 1 0 (`selftest_exits.txt`: 0 1 1 0). The k_c 79 line puts lambda_1 near 1.404 at D 19.5 (information, not a pass rule); dh370 scans 1.30 to 1.40.

## Result (22 Nov, 19:30:05 to 20:18:08 UTC): no robust change in 1.41 to 1.50 at D 19.5; the hybrid sign is - at every point

All six processes exit 0 (`exits_kc79_d195_scan.txt`; process walls 25:58 for process 5 and 47:50 to 48:02 for processes 0 to 4; peak RSS 1.76 GB for the one-point process and 2.19 to 2.28 GB for the two-point processes). The system check printed "the record system" on all six: |F| 3.5131804762e-10 against the record's 3.5122938292e-10 (relative 2.5e-4, inside the 1e-2 bar), steps 2879 = 2879. The pre-run checks passed (`selftest_exits.txt`: read_lower 0, shift 1, round2 1, repeat_check 0). 11 evaluations, all noise-robust. A point took 1555 to 1575 s in round 1 (six processes) and 1301 to 1309 s in round 2 (five).

| lambda_1 | process | hybrid sign | ln\|det\| | noise_robust | float64 sign | point sec |
|---|---|---|---|---|---|---|
| 1.41 | 0 | -1 | -2502.1781329648 | True | +1 | 1559 |
| 1.42 | 1 | -1 | -2501.8886318716 | True | -1 | 1571 |
| 1.43 | 2 | -1 | -2501.8025259883 | True | -1 | 1565 |
| 1.44 | 3 | -1 | -2501.8067714610 | True | -1 | 1567 |
| 1.45 | 4 | -1 | -2501.8606474471 | True | -1 | 1575 |
| 1.45 (repeat) | 5 | -1 | -2501.8606474471 | True | -1 | 1555 |
| 1.46 | 0 | -1 | -2501.9447414019 | True | -1 | 1309 |
| 1.47 | 1 | -1 | -2502.0481285884 | True | -1 | 1309 |
| 1.48 | 2 | -1 | -2502.1641331420 | True | -1 | 1309 |
| 1.49 | 3 | -1 | -2502.2885417251 | True | -1 | 1308 |
| 1.50 | 4 | -1 | -2502.4181119799 | True | -1 | 1301 |

Reading (`read_lower.txt`, `read_lower.py` dh170's, unedited):
- **Robust changes:** none. No change touches a non-robust point.
- **Edge signs:** - at 1.41 (the sign t5 asked for) and - at 1.50; the signs are - at every one of the ten lambda.
- **ln|det| minima without a sign change:** none.
- **Repeat of 1.45:** agrees, bit-identical (`repeat_check.py` PASS; ln -2501.8606474471 on process 4 and on process 5).
- **Float64:** its sign differs from the hybrid at 1.41 only; the hybrid is the reading.
- ln|det| has a maximum at 1.43 (-2501.8025). It falls toward 1.50 by 0.616 in seven steps of 0.01 and toward 1.41 by 0.289 in the last step (1.42 to 1.41; the step before, 1.43 to 1.42, is -0.086).

### Beside the lambda_1 line (information, not a pass rule; roots named by position)

- The k_c 79 line of lambda_1 (the root near it at D 19.0 and D 19.125: 1.539658 and 1.505784; k_c 71's root near the line, 1.5365, 1.5112, 1.4907, 1.4750 at D 19, 19.125, 19.1875, 19.25, as the coordinator reads them) puts it near 1.398 to 1.404 at D 19.5, below this window's edge at 1.41. No root of k_c 79 was found in 1.41 to 1.50 at D 19.5, and the sign at 1.41 is -. A root below 1.41 is not excluded: this scan stops at 1.41, and dh370's scan of 1.30 to 1.40 reads that part.
- At D 19.125 the k_c 79 scan has its one root at 1.505784 (dh370, raw c58e5052), above this window's edge at 1.50; the sign at 1.50 is - here.
