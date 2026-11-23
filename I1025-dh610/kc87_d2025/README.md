# I1025-dh610/kc87_d2025: k_c 87 at D 20.25 on Linux, regridded from this machine's accepted k_c 79 D 20.25 state and scanned at lambda 1.14 to 1.22, against this machine's k_c 79 changes (and win2's k_c 87 scan)

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 11:52:30 UTC, before any run of this folder. The k_c 87 roots are not yet physical.

## Order (coordinator t5, hc, after `../kc79_d2025`, raw f7cbf67d), in part
"With the idle cores, beside the m3mp recount (keep its 12 processes first): k_c 87 at D 20.25 on Linux from your accepted k_c 79 D 20.25 state, as win2 did (kc79 check accepts the source, kc87 refuses it; ell_refine.py l1kc79dh610d2025 79 l1kc87dh610d2025 87 1 20.25 2.1099063840 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma, 8 threads; accept by kc87_syscheck with both controls exit 1 and the kc79 check refusing), then d18_hybsign at 1.140-1.220 by 0.01 plus a repeat of 1.17 (10 evals, 5 procs) and read_lower. Written before (README): the lambda_1 root stays within 0.005 of its k_c 79 value; win2's k_c 87 scan (due ~12:00) says which root that is. Raw I1025-dh610/kc87_d2025/, README first. Interim messages at each acceptance, please."
Memory alerts only (standing rule). My k_c 79 D 20.25 scan (`../kc79_d2025/read_lower.txt`): hybrid signs - at 1.13 to 1.16, + at 1.17 to 1.19, - at 1.20 to 1.24; two robust changes, (1.160, 1.170) "- to +" det-linear 1.167526 [1.163712, 1.167526] and (1.190, 1.200) "+ to -" det-linear 1.199763 [1.199698, 1.199763]. win2's k_c 79: 1.165140 and 1.203492; win2's k_c 87 regrid is accepted (`../../I1025-win2/kc79_d2025/rec_k87_D20.2500.jsonl`, copied as `in/ref_win2_rec_k87_D20.2500.jsonl`) and its scan runs.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lane refuses any other blob)
| item | blob |
|---|---|
| the k_c 79 D 20.25 state `sol_l1kc79dh610d2025_D20.2500.npy` and record `l1kc79dh610d2025.jsonl` (`../kc79_d2025/regrid`, raw f7cbf67d; norm F 4.6188739816e-10, 2762 steps, Delta 1.098607545025) | a5d69733, 01ab747b |
| `kc79_syscheck_1025.py`, `kc87_syscheck_1025.py` | 29dce7ea, 6df5d960 |
| `d18_hybsign.py` (xfkappa's, unmodified), `read_lower.py`, `d185_scan_read.py`, `d18c_read.py`, `repeat_check.py` | e089207a, 89309d3c, 7c9d400f, 1383470f, aaf598a9 |
| this machine's k_c 79 reading and rows (`ref_dh610_kc79_*`), win2's k_c 87 regrid record (`ref_win2_rec_k87_D20.2500.jsonl`) | in `in_blobs.txt` |
| `kc87_read.py` (mine: the two changes beside the k_c 79 ones by position, and beside win2's k_c 87 reading when `in/win2_k87_read_lower.txt` exists) | 030141ee |
Code: `ell_refine.py` 631e5801 and `ell_delta.py` fde699f5 in `~/Source/choptuik-large-d-1025g` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399); `d18_hybsign.py` in `~/Source/choptuik-large-d-1025f` at 505d8399; python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2).

## Commands (`lane_kc87_d2025.sh` via `start_kc87_d2025.sh` = systemd user unit i1025ag under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails; `notify_kc87.sh` sends the coordinator an hc line at the source check, the regrid's end, its acceptance and the end)
1. Pins and the tools' controls: selftests of the two syscheck scripts (exit 0), `read_lower.py` and its two mutations (0 1 1), `repeat_check.py` (0), `kc87_read.py` (0) and its `--mutate` (1).
2. The source: `kc79_syscheck_1025.py` accepts it (exit 0; its `--mutate=F` and `--mutate=steps` exit 1) and `kc87_syscheck_1025.py` refuses it (exit 1).
3. The regrid: the order's `ell_refine.py` command, 8 threads, nice 10, cap 21600 s (a time cap only), in `solver/matter` of 1025g; refuses to start with less than 8 GiB free.
4. Acceptance: `kc87_syscheck_1025.py` on the result (exit 0; `--mutate=F` and `--mutate=steps` exit 1) and `kc79_syscheck_1025.py` refusing it (exit 1), else the scan is not started.
5. The scan: `d18_hybsign.py` at 1.14 to 1.22 by 0.01 and a repeat of 1.17 (10 evaluations), 5 processes of 1 thread, nice 10, value i to process i mod 5: p0 1.14, 1.19; p1 1.15, 1.20; p2 1.16, 1.21; p3 1.17 (the original), 1.22; p4 1.18, 1.17 (the repeat). Each prints the record system first (exit 3 if not). Refuses to start with less than 5 x 2.5 GB + 4 GB free.
6. The reading: `read_lower.py scan 1.14 1.22`, `repeat_check.py` on the merged rows, `kc87_read.py`.
Threads: 8 (regrid) or 5 (scan) beside the #1076 recount's up to 12 (`../../I1021-dh610/fu022mp_m3mp`), 20 at most, all at nice 10; that recount keeps its 12 first (it uses 2 to 3 now, its batches being small).

## Acceptance (fixed before the run)
- The source accepted by the k_c 79 check (controls exit 1) and refused by the k_c 87 check; the regrid exits 0 and is accepted by `kc87_syscheck_1025.py` with both controls exit 1 and refused by the k_c 79 check (a failing control stops the work and I report it; no bar is loosened); every scan process prints the record system.
- Reported: the regrid's norm F, steps, Delta (beside win2's k_c 87 record and this machine's k_c 79), wall; every robust change by position with bracket, orientation as printed, det-linear and range, beside my k_c 79 ones (and win2's k_c 87 ones) and the differences; the repeat of 1.17; the edge signs. Interim messages at the source check and at the regrid's acceptance.
- The coordinator's reading: the lambda_1 root stays within 0.005 of its k_c 79 value; which of the two roots is lambda_1 is read from win2's k_c 87 scan.

## Predictions, registered before the run (information)
- The source is accepted by the k_c 79 check (95%) and refused by the k_c 87 check (97%). The regrid exits 0 (95%) in 2000 to 4500 s (65%; the k_c 79 regrid took 2164 s) and is accepted (90%), the k_c 79 check refusing it (97%).
- Steps between 3000 and 3080 (70%; k_c 79 to 87 added 10.0% at D 19.75: 2839 to 3124, on 2762 that is 3039); Delta(k_c 87) minus Delta(k_c 79) = -3.17e-06 +- 0.15e-06 (70%; -3.17e-06 at D 19.5 and 19.75), that is about 1.098604375; norm F between 4e-10 and 6e-10 (80%).
- Each scan point takes 1000 to 1900 s (60%); all 5 processes exit 0 with the record system (90%); the repeat of 1.17 agrees (85%).
- Two robust changes in 1.14 to 1.22 (85%), with the k_c 79 orientations ("- to +" then "+ to -"; 80%); the first within 0.005 of 1.167526 (70%), the second within 0.005 of 1.199763 (55%; it lies 0.0002 under the grid point 1.20, so its bracket may move one cell), both (45%).

## Status
- 2026-11-23 11:52:30 UTC: folder, inputs, lane and the reading prepared before any run.
- 2026-11-23 11:52:54 UTC: regrid started; 12:39:16 ACCEPTED; scan 12:39:16 to 13:33:59 UTC; lane exit 0 (`exits_kc87_d2025.txt`).

## Result (`summarize_kc87.py` > `summary_kc87.txt` prints the tables from the files; the comparison with win2's k_c 87 reading is `kc87_read_vs_win2.txt`)

| record | this machine (Linux) | win2 (Windows) | difference |
|---|---|---|---|
| F_start | 1.0660616665993483e-05 | 1.0660635193843783e-05 | -1.853e-11 |
| F | 4.511176956827055e-10 | 4.50958119026279e-10 | +1.596e-13 |
| steps | 3042 | 3042 | +0.000e+00 |
| constraint | 0.0016254630743778706 | 0.0016254804602660472 | -1.739e-08 |
| Delta | 1.0986034308284602 | 1.0986036662833156 | -2.355e-07 |
| seconds | 2775 | 7378 |  |
| Delta minus its k_c 79 source | -4.114197e-06 | -3.608847e-06 | |
| Delta_src (the k_c 79 state's) | 1.098607545025376 | 1.0986072751302585 | +2.699e-07 |
| steps: k_c 87 over k_c 79 | 3042/2762 = 1.1014 | 3042/3042 | |

| lambda | hybrid sign (mine, win2, my k_c 79) | noise signs (robust) | float64 sign (mine, win2) | ln of abs det (mine, win2) | mine minus win2 | ln (my k_c 79) | seconds (mine) |
|---|---|---|---|---|---|---|---|
| 1.14 | -, -, - | -- (True) | -, - | -2728.840803, -2728.854163 | +0.013359 | -2420.531984 | 1634 |
| 1.15 | -, -, - | -- (True) | -, - | -2729.991853, -2730.011344 | +0.019492 | -2421.862865 | 1625 |
| 1.16 | -, -, - | -- (True) | -, - | -2731.686333, -2731.735325 | +0.048993 | -2423.760696 | 1629 |
| 1.17 | +, +, + | ++ (True) | -, - | -2732.510747, -2732.462979 | -0.047768 | -2424.873017 | 1627 |
| 1.17 | +, +, + | ++ (True) | -, - | -2732.510747, -2732.462979 | -0.047768 | -2424.873017 | 1640 |
| 1.18 | +, +, + | ++ (True) | +, + | -2732.000288, -2731.987450 | -0.012838 | -2424.728919 | 1628 |
| 1.19 | +, +, + | ++ (True) | +, + | -2732.127133, -2732.120872 | -0.006261 | -2425.517906 | 1628 |
| 1.20 | +, +, - | ++ (True) | +, + | -2732.435101, -2732.431597 | -0.003505 | -2429.238333 | 1637 |
| 1.21 | +, +, - | ++ (True) | +, + | -2732.830516, -2732.828506 | -0.002011 | -2426.047688 | 1651 |
| 1.22 | +, +, - | ++ (True) | +, + | -2733.277686, -2733.276614 | -0.001072 | -2425.752597 | 1628 |

scan points: 10 evaluations, seconds per point min 1625, median 1628, max 1651, sum 16327; outside 1000 to 1900 s: 0
mine minus win2's ln|det| over the 10 evaluations: min -0.047768, max +0.048993

hybrid signs: 1.140- 1.150- 1.160- 1.170+ 1.180+ 1.190+ 1.200+ 1.210+ 1.220+
robust changes: 1 (this machine's k_c 79: 2)
   change (1.160, 1.170), - to +, det-linear 1.166952, range [1.164380, 1.166952]
against this machine's k_c 79: the counts differ (1 against 2): no pairing by position
against win2's k_c 87:
| position | mine: bracket, orientation, det-linear, estimator range | win2's k_c 87: det-linear, orientation | mine minus it | same orientation | within 0.005 |
|---|---|---|---|---|---|
| 1 | (1.160, 1.170), - to +, 1.166952, [1.164380, 1.166952] | 1.165265, - to + | +0.001687 | True | True |

### Reading (by position; orientation only as the reader prints it; "robust change" is a sign change of the hybrid determinant between two grid points, not yet a physical root)

- **Acceptance held.** Source: `kc79_syscheck_1025.py` exit 0 (`--mutate=F` 1, `--mutate=steps` 1), `kc87_syscheck_1025.py` exit 1. Regrid: ell_refine exit 0, 2778 s wall, `kc87_syscheck_1025.py` exit 0 (`--mutate=F` 1, `--mutate=steps` 1), `kc79_syscheck_1025.py` on the result exit 1. All five scan processes printed "the record system" (|F| 4.5142771610e-10 in the d18 context against the record's 4.5111769568e-10, 3042 steps = the record's).
- **One robust change in 1.14 to 1.22, not two.** (1.160, 1.170), "- to +", det-linear 1.166952, estimator range [1.164380, 1.166952] (a spread over interpolation choices, not an enclosure). Hybrid signs: - at 1.14 to 1.16, + at 1.17 to 1.22. The repeat of 1.17 agrees (same signs, same ln|det| to the digit printed; `repeat_check.py` PASS). The float64 sign reads - at 1.17 where the hybrid reads +; the hybrid is the sign read, as at every point.
- **The first change against this machine's k_c 79 one (1.167526):** -0.000574, same orientation. Within 0.005 and within win2's own bar of 0.002 between k_c 79 and k_c 87 (win2: 1.165140 to 1.165265, +0.000125).
- **The second change (k_c 79: (1.190, 1.200), "+ to -", 1.199763) is not in the window at k_c 87.** The signs at 1.20, 1.21 and 1.22 are + (at k_c 79 they were -). Nothing here says whether it left the window above 1.22 or closed: win2's k_c 87 scan over 1.13 to 1.24 (its k_c 87 files alone, `in/win2_k87_read_lower.txt`; its mixed k_c 79 + 87 reading `read_lower_k87_D2025.txt` is void by its own README) has + at every point from 1.17 to 1.24 as well. By win2's rule (the root that stays within 0.002 between k_c 79 and k_c 87 is lambda_1; the other moves with k_c) the root near lambda_1's line is the first one and the second moved with k_c, or closed; this scan cannot tell which.
- **Against win2's k_c 87 reading (same scan, win2's build):** one robust change, (1.165, 1.170), "- to +", det-linear 1.165265, range [1.165184, 1.165265]. Mine minus win2's: +0.001687, same orientation, within 0.005 (k_c 79: +0.002386). The same count of changes at the same position on both machines.
- **ln|det| beside win2's at the nine common lambdas** (win2's grid has 0.005 steps; mine 0.01): the difference is largest next to the change (-0.048 at 1.17, +0.049 at 1.16) and falls to -0.001 at 1.22; that is the 0.0017 shift of the root on a steep ln|det|, not a separate disagreement. Signs agree at all ten evaluations; the float64 signs agree with win2's at all ten.
- **The regrid beside win2's:** steps 3042 on both (k_c 79: 2762, so +10.14%); norm F 4.5112e-10 against 4.5096e-10; Delta(k_c 87) minus Delta(k_c 79) is -4.114e-06 here and -3.609e-06 for win2 (D 20: -2.972e-06). Delta differs between the two machines by -2.4e-07 at k_c 87 and by +2.7e-07 at the k_c 79 source (information; the thread-count test of `../repro_d1975` moved a state by 4e-06 in norm).

### Predictions scorecard (written before the run)

| prediction | result | verdict |
|---|---|---|
| source accepted by k_c 79 check (95%), refused by k_c 87 check (97%) | exit 0 and exit 1 | right |
| regrid exit 0 (95%) in 2000 to 4500 s (65%); accepted (90%); k_c 79 check refusing it (97%) | exit 0, 2778 s; accepted; refused | right |
| steps 3000 to 3080 (70%) | 3042 | right |
| Delta(k_c 87) minus Delta(k_c 79) = -3.17e-06 +- 0.15e-06 (70%) | -4.114e-06 | wrong (win2's -3.609e-06 is also outside) |
| norm F 4e-10 to 6e-10 (80%) | 4.5112e-10 | right |
| each scan point 1000 to 1900 s (60%) | 1625 to 1651 s | right |
| all 5 processes exit 0 with the record system (90%); the repeat of 1.17 agrees (85%) | yes; yes | right |
| two robust changes in 1.14 to 1.22 (85%) | one | wrong |
| the k_c 79 orientations (80%) | the one change is "- to +", the first one's | right for the change found; the second is missing |
| first change within 0.005 of 1.167526 (70%) | -0.000574 | right |
| second within 0.005 of 1.199763 (55%); both (45%) | no second change in the window | wrong |

The coordinator's reading ("the lambda_1 root stays within 0.005 of its k_c 79 value") holds for the root that is found: -0.000574 (mine) and +0.000125 (win2).
