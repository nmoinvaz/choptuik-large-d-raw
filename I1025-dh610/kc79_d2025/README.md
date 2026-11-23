# I1025-dh610/kc79_d2025: k_c 79 at D 20.25 on Linux, regridded from win2's leg 3 k_c 71 D 20.25 state and scanned at lambda 1.13 to 1.24, against win2's two robust changes

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 10:11:42 UTC, before any run of this folder. The k_c 79 roots are not yet physical.

## Order (coordinator t5, hc, after `../repro_d1975`), in part
"With 8 cores free beside the m3mp recount: k_c 79 at D 20.25 on Linux, from leg 3's k_c 71 D 20.25 state (I1025-win2/kc71_leap/states/sol_l1kc71Lw1025c_D20.250000.npy, blob 8e137d6b, record l1kc71Lw1025c.jsonl at raw 589d5f2a), as win2 did: kc71_syscheck on the source (controls exit 1), ell_refine.py l1kc71Lw1025c 71 l1kc79dh610d2025 79 1 20.25 2.1099063840 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (8 threads, nice 10), accept by kc79_syscheck (both controls exit 1); then d18_hybsign at 1.13-1.24 by 0.01 plus a repeat of 1.16 (13 evals, 4 procs) and read_lower. Written before (README): two robust changes near win2's 1.165140 and 1.203492, each within about 0.005 of win2's (the regrid reproducibility). Raw I1025-dh610/kc79_d2025/, README first. Keep the m3mp recount's 12 processes first."
Memory alerts only (standing rule). win2's folder `../../I1025-win2/kc79_d2025/` (README, regrid and scan scripts, rows) is the model; its regrid took 4977 s on Windows (|F| 4.6133e-10, 2762 steps, Delta 1.098607275130, k_c 79 minus k_c 71 -1.5719e-05) and its scan (lambda 1.12 to 1.24 and a repeat of 1.18, 14 evaluations) read two robust changes, (1.160, 1.170) "- to +" det-linear 1.165140, range [1.162108, 1.165140], and (1.200, 1.210) "+ to -" det-linear 1.203492, range [1.202702, 1.203492].

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lane refuses any other blob)
| item | blob |
|---|---|
| leg 3's D 20.25 k_c 71 state `sol_l1kc71Lw1025c_D20.250000.npy` and record `l1kc71Lw1025c.jsonl` (win2's `inputs/`, equal to raw 589d5f2a's) | 8e137d6b, cc1e872c |
| `kc71_syscheck.py` (the source acceptance), `kc79_syscheck_1025.py` (the result's acceptance) | 4cd86cd4, 29dce7ea |
| `d18_hybsign.py` (xfkappa's, unmodified), `read_lower.py`, `d185_scan_read.py`, `d18c_read.py`, `repeat_check.py` | e089207a, 89309d3c, 7c9d400f, 1383470f, aaf598a9 |
| win2's reading `ref_win2_read_lower_k79_D2025.txt`, rows `ref_win2_scan_k79_D20.25.jsonl` (14 rows), records `ref_win2_rec_k79_D20.2500.jsonl`, `ref_win2_rec_k71_D20.2500.jsonl` | e229442a, bbfca0e9, f6f5a3ab, 456d6578 |
| `kc79_read.py` (mine: the two changes beside win2's by position) | in `in_blobs.txt` |
Code: `ell_refine.py` 631e5801 and `ell_delta.py` fde699f5 in `~/Source/choptuik-large-d-1025g` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399), the same code win2's worktree ran; `d18_hybsign.py` in `~/Source/choptuik-large-d-1025f` at 505d8399; python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2). lambda_0(20.25) reads 2.109906384 (the order's 2.1099063840; unused with `--no-gamma`).

## Commands (`lane_kc79_d2025.sh` via `start_kc79_d2025.sh` = systemd user unit i1025af under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails)
1. Pins and the controls of the tools: selftests of `kc79_syscheck_1025.py` and `kc71_syscheck.py` (exit 0), `read_lower.py` and its `--mutate=shift`, `--mutate=round2` (exits 0 1 1), `repeat_check.py` (0), `kc79_read.py` (0) and its `--mutate` (1).
2. The source: `kc71_syscheck.py` accepts it (exit 0; its `--mutate=F` and `--mutate=steps` exit 1).
3. The regrid: the order's `ell_refine.py` command, 8 threads (OMP, OPENBLAS, MKL = 8), nice 10, cap 21600 s (a time cap only), in `solver/matter` of 1025g; refuses to start with less than 8 GiB free; log and per-minute samples in `regrid/`.
4. Acceptance: `kc79_syscheck_1025.py` on the regrid record and state (exit 0; `--mutate=F` and `--mutate=steps` exit 1), else the scan is not started.
5. The scan: `d18_hybsign.py` at 1.13 to 1.24 by 0.01 and a repeat of 1.16 (13 evaluations) on 4 processes of 1 thread, nice 10, value i to process i mod 4: p0 1.13, 1.17, 1.21, 1.16 (the repeat); p1 1.14, 1.18, 1.22; p2 1.15, 1.19, 1.23; p3 1.16 (the original), 1.20, 1.24. Each prints the record system first (exit 3 if not). Refuses to start with less than 4 x 2.5 GB + 4 GB free.
6. The reading: `read_lower.py scan 1.13 1.24`, `repeat_check.py` on the merged rows, then `kc79_read.py` (win2's two changes beside mine by position).
Threads: this uses 8 (regrid) or 4 (scan) beside the #1076 recount's 12 processes of `../../I1021-dh610/fu022mp_m3mp`, 20 at most, all at nice 10; that recount keeps its 12 first.

## Acceptance (fixed before the run)
- Source accepted and its two controls exit 1; the regrid exits 0 and is accepted by `kc79_syscheck_1025.py` with both controls exit 1 (a failing control stops the work and I report it; no bar is loosened); every scan process prints the record system.
- Reported: the regrid's |F|, steps, Delta (beside win2's 4.6133e-10, 2762, 1.098607275130), wall; every robust change by position with bracket, orientation as printed, det-linear and range, beside win2's 1.165140 and 1.203492 and the differences; the repeat of 1.16 (sign, noise signs, ln|det| within 1e-6); the edge signs.
- The coordinator's reading: two robust changes near win2's, each within about 0.005 (the regrid reproducibility, `../repro_d1975`: a thread-count change moved lambda_1 by 0.0051 at D 19.75).

## Predictions, registered before the run (information)
- The source is accepted (95%). The regrid exits 0 (95%) in 1500 to 3500 s (65%; win2 4977 s on Windows, dh170's k_c 79 regrid at D 20 2389 s, mine beside the 12-process recount) and is accepted (90%) with 2762 steps as win2's (85%), |F| between 3.5e-10 and 6e-10 (80%), Delta within 1e-6 of win2's 1.098607275130 (70%).
- Each scan point takes 800 to 1800 s (60%); all 4 processes exit 0 with the record system (90%); the repeat of 1.16 agrees with its original (85%).
- Two robust changes (85%), with win2's orientations ("- to +" near 1.165, "+ to -" near 1.203; 80%), hybrid signs - at 1.13 and - at 1.24 (85%).
- The first change within 0.005 of 1.165140 (50%), the second within 0.005 of 1.203492 (55%), both (35%), neither (20%).

## Status
- 2026-11-23 10:11:42 UTC: folder, inputs, lane and the reading prepared before any run.

## Result (2026-11-23 11:49 UTC; the tables are printed by `summarize_kc79.py` into `summary_kc79.txt`, `in/kc79_read.py` into `kc79_read.txt`, `read_lower.py` and `repeat_check.py` into `read_lower.txt`)

Everything ran as ordered, all exit 0. Source: `kc71_syscheck.py` ACCEPTED, its two controls exit 1 (10:12:00 UTC). Regrid: `ell_refine.py` exit 0, 2164 s wall (10:12:00 to 10:48:04 UTC; win2's 4977 s on Windows), **ACCEPTED** by `kc79_syscheck_1025.py` at 10:48:07 (exit 0; |F| 4.6188739816e-10 and 2762 steps come back; its two controls exit 1). Scan: 13 evaluations on 4 processes, each printing "the record system" (|F| 4.6181941293e-10 against the record's 4.6188739816e-10, steps 2762), 10:48:07 to 11:46:37 UTC (p0 with four points last). No memory alert. The k_c 79 roots are not yet physical.

```
| record | this machine (Linux) | win2 (Windows) | difference |
|---|---|---|---|
| F_start | 3.760619529562024e-05 | 3.760619529560235e-05 | +1.789e-17 |
| F | 4.6188739816379066e-10 | 4.613302409241101e-10 | +5.572e-13 |
| steps | 2762 | 2762 | +0.000e+00 |
| constraint | 0.002629070151119348 | 0.0026290648606842578 | +5.290e-09 |
| Delta | 1.098607545025376 | 1.0986072751302585 | +2.699e-07 |
| seconds | 2162 | 4977 |  |
| Delta minus its k_c 71 source | -1.544936e-05 | -1.571926e-05 | |

| lambda | hybrid sign (mine, win2) | noise signs (robust) | float64 sign (mine, win2) | ln of abs det (mine, win2) | mine minus win2 | seconds (mine) |
|---|---|---|---|---|---|---|
| 1.13 | -, - | -- (True) | +, + | -2419.383324, -2419.413476 | +0.030151 | 955 |
| 1.14 | -, - | -- (True) | -, + | -2420.531984, -2420.584874 | +0.052891 | 955 |
| 1.15 | -, - | -- (True) | -, + | -2421.862865, -2421.977642 | +0.114777 | 957 |
| 1.16 | -, - | -- (True) | +, + | -2423.760696, -2424.284117 | +0.523421 | 699 |
| 1.16 | -, - | -- (True) | +, + | -2423.760696, -2424.284117 | +0.523421 | 957 |
| 1.17 | +, + | ++ (True) | +, + | -2424.873017, -2424.340132 | -0.532885 | 928 |
| 1.18 | +, + | ++ (True) | +, + | -2424.728919, -2424.428845 | -0.300074 | 923 |
| 1.19 | +, + | ++ (True) | -, + | -2425.517906, -2425.149435 | -0.368471 | 925 |
| 1.20 | -, + | -- (True) | +, + | -2429.238333, -2426.967110 | -2.271223 | 924 |
| 1.21 | -, - | -- (True) | +, + | -2426.047688, -2426.344530 | +0.296842 | 926 |
| 1.22 | -, - | -- (True) | +, + | -2425.752597, -2425.871194 | +0.118597 | 924 |
| 1.23 | -, - | -- (True) | -, + | -2425.765702, -2425.834485 | +0.068784 | 921 |
| 1.24 | -, - | -- (True) | -, + | -2425.915865, -2425.962114 | +0.046249 | 919 |

scan points: 13 evaluations, seconds per point min 699, median 925, max 957, sum 11913; outside 800 to 1800 s: 1
```

**Reading** (`read_lower.txt`): hybrid signs - at 1.13 to 1.16, + at 1.17 to 1.19, - at 1.20 to 1.24, every point noise-robust (float64 signs differ from the hybrid at 1.13, 1.16, 1.19, 1.20, 1.21, 1.22, as the reader prints them); the repeat of 1.16 (on p0, its original on p3) agrees in sign, noise signs, float64 sign and ln|det| (`repeat_check.py` PASS). Two robust changes, by position beside win2's:

```
hybrid signs: 1.130- 1.140- 1.150- 1.160- 1.170+ 1.180+ 1.190+ 1.200- 1.210- 1.220- 1.230- 1.240-
robust changes: 2 (win2's: 2)
| position | mine: bracket, orientation, det-linear, estimator range | win2's: det-linear, range | mine minus win2's | same orientation | within 0.005 |
|---|---|---|---|---|---|
| 1 | (1.160, 1.170), - to +, 1.167526, [1.163712, 1.167526] | 1.165140, [1.162108, 1.165140] | +0.002386 | True | True |
| 2 | (1.190, 1.200), + to -, 1.199763, [1.199698, 1.199763] | 1.203492, [1.202702, 1.203492] | -0.003729 | True | True |
```

- **Both are within the coordinator's 0.005 of win2's:** the first (1.160, 1.170) "- to +" at 1.167526 against 1.165140 (+0.002386; the estimator ranges, spreads over interpolation choices and not enclosures, overlap: [1.163712, 1.167526] and [1.162108, 1.165140]); the second at 1.199763 against 1.203492 (-0.003729; ranges [1.199698, 1.199763] and [1.202702, 1.203492], which do not overlap, a gap of 0.0029).
- **The second change sits one grid cell lower:** my bracket is (1.190, 1.200) and win2's (1.200, 1.210), because the hybrid sign at 1.20 is - here and + on win2's build; the root lies within 0.0004 of the grid point 1.20 on this build and 0.0035 above it on win2's. The two scans' ln|det| differ by +0.03 to +0.12 away from the changes and by up to 0.53 (1.16, 1.17) and 2.27 (1.20) beside them, as a shift of the det's zero would give.
- The regrids differ little: same step count (2762), Delta +2.70e-07 and norm F +0.12% against win2's, the same k_c 79 minus k_c 71 shift of Delta to 2.7e-07 (-1.5449e-05 here, -1.5719e-05 there). The root shifts of +0.0024 and -0.0037 are of the size of the regrid reproducibility measured in `../repro_d1975` (0.0051 between two thread counts at D 19.75).

### Predictions against outcomes (registered before the run)
| prediction | outcome |
|---|---|
| source accepted (95%); regrid exit 0 (95%), 1500 to 3500 s (65%), accepted (90%), 2762 steps (85%), norm F 3.5e-10 to 6e-10 (80%), Delta within 1e-6 of win2's (70%) | yes to all: 2164 s, 2762 steps, 4.6189e-10, +2.7e-07 |
| each scan point 800 to 1800 s (60%) | no for one: 12 of 13 evaluations took 919 to 957 s, one (1.16 on p3) 699 s |
| all 4 exit 0 with the record system (90%); the repeat of 1.16 agrees (85%) | yes; yes |
| two robust changes (85%); win2's orientations (80%); signs - at 1.13 and 1.24 (85%) | yes; yes; yes |
| first within 0.005 of 1.165140 (50%); second within 0.005 of 1.203492 (55%); both (35%) | yes (+0.002386); yes (-0.003729); yes |
The coordinator's written-before ("two robust changes near win2's 1.165140 and 1.203492, each within about 0.005 of win2's, the regrid reproducibility") holds as read, on the det-linear estimates.
