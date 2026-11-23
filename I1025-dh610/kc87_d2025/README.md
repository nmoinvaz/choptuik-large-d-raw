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
