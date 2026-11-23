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
