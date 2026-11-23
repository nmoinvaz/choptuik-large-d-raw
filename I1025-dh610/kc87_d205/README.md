# I1025-dh610/kc87_d205: k_c 87 at D 20.5 on Linux, regridded from dh170's accepted k_c 79 D 20.5 state and scanned at lambda 1.050 to 1.120, against dh170's k_c 79 root

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 13:40 UTC, before any run of this folder. The k_c 87 roots are not yet physical.

## Order (coordinator t5, hc, after `../kc87_d2025`, raw 10ddc4be), in part
"D 20.25 k_c 87 Linux accepted as read (raw 10ddc4be): lambda_1 1.166952, +0.0017 from Windows, and the second root gone on both builds. With your 8 free threads, beside the recount: k_c 87 at D 20.5 from dh170's accepted k_c 79 D 20.5 state (raw I1025-dh170/kc79_d205/, state 30a92b78, record 5406e21c): kc79 check accepts the source (controls exit 1), kc87 check refuses it; ell_refine.py l1kc79dh170d205 79 l1kc87dh610d205 87 1 20.5 2.1088217835 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (8 threads); accept by kc87_syscheck (both controls exit 1, kc79 check refusing). Then d18_hybsign at 1.050-1.120 by 0.005 plus a repeat of 1.085 (16 evals, 5 procs), read_lower. Written before (README): one robust change within 0.005 of dh170's k_c 79 root (det-linear 1.087574 on the 0.03 grid; his final reading lands ~14:15, use it if it differs). Raw I1025-dh610/kc87_d205/, README first; your auto-notifier as before."
Memory alerts only (standing rule). dh170's k_c 79 D 20.5 regrid (his README, raw 9535a78a): |F| 4.6763736498e-10, 2731 steps, psi-constraint 3.2382273e-3, Delta 1.105055446478, 3109 s on his machine (i7-7700); his scan on the 0.03 grid was running at 11:35 UTC.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lane refuses any other blob)
| item | blob |
|---|---|
| dh170's k_c 79 D 20.5 state `sol_l1kc79dh170d205_D20.5000.npy` and record `l1kc79dh170d205.jsonl` (`I1025-dh170/kc79_d205`, raw 9535a78a, taken from origin/main at 4ba67ab2) | 30a92b78, 5406e21c |
| `kc79_syscheck_1025.py`, `kc87_syscheck_1025.py` (the blobs of `../kc87_d2025`) | 29dce7ea, 6df5d960 |
| `d18_hybsign.py` (xfkappa's, unmodified), `read_lower.py`, `d185_scan_read.py`, `d18c_read.py`, `repeat_check.py` | e089207a, 89309d3c, 7c9d400f, 1383470f, aaf598a9 |
| `kc87d205_read.py` (mine, from `../kc87_d2025/in/kc87_read.py`: the changes of the scan beside dh170's k_c 79 D 20.5 ones by position, the coordinator's 1.087574 or dh170's final reading when `in/dh170_k79_read_lower.txt` exists; the orientation is printed as the reader prints it and not compared across k_c; selftest exit 0, `--mutate` exit 1) | in `in_blobs.txt` |
Code: `ell_refine.py` 631e5801 and `ell_delta.py` fde699f5 in `~/Source/choptuik-large-d-1025g` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399); `d18_hybsign.py` in `~/Source/choptuik-large-d-1025f` at 505d8399; python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2).
The state comes from another machine (dh170, i7-7700, same pins): the source check at the start says whether it is the record's system on this build (|F| at most 1e-9, state |F| within 1% of the record's, the `freeze_from` step count equal).

## Commands (`lane_kc87_d205.sh` via `start_kc87_d205.sh` = systemd user unit i1025ah under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails; `notify_kc87.sh` sends the coordinator an hc line at the source check, the regrid's end, its acceptance, the first-round pair check of 1.085 and the end)
1. Pins and the tools' controls: selftests of the two syscheck scripts (exit 0), `read_lower.py` and its two mutations (0 1 1), `repeat_check.py` (0), `kc87d205_read.py` (0) and its `--mutate` (1).
2. The source: `kc79_syscheck_1025.py` accepts it (exit 0; its `--mutate=F` and `--mutate=steps` exit 1) and `kc87_syscheck_1025.py` refuses it (exit 1).
3. The regrid: the order's `ell_refine.py` command, 8 threads, nice 10, cap 21600 s (a time cap only), in `solver/matter` of 1025g; refuses to start with less than 8 GiB free.
4. Acceptance: `kc87_syscheck_1025.py` on the result (exit 0; `--mutate=F` and `--mutate=steps` exit 1) and `kc79_syscheck_1025.py` refusing it (exit 1), else the scan is not started.
5. The scan: `d18_hybsign.py` at 1.050 to 1.120 by 0.005 (15 values) and a repeat of 1.085 (16 evaluations), 5 processes of 1 thread, nice 10: p0 1.085 (the repeat), 1.050, 1.075, 1.100; p1 1.055, 1.080, 1.105; p2 1.085 (the original), 1.060, 1.110; p3 1.065, 1.090, 1.115; p4 1.070, 1.095, 1.120. The original and the repeat run in the first round on two processes; when both rows exist a watcher runs `repeat_check.py` on them and logs the result (it stops nothing; a disagreement stops the work when I read it). Each process prints the record system first (exit 3 if not). Refuses to start with less than 5 x 2.5 GB + 4 GB free.
6. The reading: `read_lower.py scan 1.050 1.120`, `repeat_check.py` on the merged rows, `kc87d205_read.py`.
Threads: 8 (regrid) or 5 (scan) beside the #1076 recount's up to 12 (`../../I1021-dh610/fu022mp_m3mp`), 20 at most, all at nice 10; that recount keeps its 12 first.

## Acceptance (fixed before the run)
- The source accepted by the k_c 79 check (controls exit 1) and refused by the k_c 87 check; the regrid exits 0 and is accepted by `kc87_syscheck_1025.py` with both controls exit 1 and refused by the k_c 79 check (a failing control stops the work and I report it; no bar is loosened); every scan process prints the record system.
- Reported: the regrid's norm F, steps, Delta (beside dh170's k_c 79 record and the D 20.25 ratios), wall; every robust change by position with bracket, orientation as printed, det-linear and range, beside dh170's k_c 79 root; the repeat of 1.085; the edge signs; ln|det| minima without a sign change. Interim messages at the source check and at the regrid's acceptance.
- The coordinator's reading: one robust change within 0.005 of dh170's k_c 79 root (det-linear 1.087574 on his 0.03 grid; his final reading, due about 14:15 UTC, is used if it differs).

## Predictions, registered before the run (mine, information)
- The source is accepted by the k_c 79 check (90%; the state was made on another machine) and refused by the k_c 87 check (97%). The regrid exits 0 (93%) in 2800 to 4300 s (65%; k_c 87 at D 20.25 took 2778 s here, k_c 79 at D 20.5 took 3112 s on dh170's machine) and is accepted (88%), the k_c 79 check refusing it (97%).
- Steps between 2960 and 3060 (65%; k_c 79 to 87 added 10.14% at D 20.25, on 2731 that is 3008). Delta(k_c 87) minus Delta(k_c 79) = -5.0e-06 (60% between -3.5e-06 and -7.0e-06; D 20: -2.97e-06 for win2, D 20.25: -3.61e-06 for win2 and -4.11e-06 here, the k_c 79 over k_c 71 shift grew from -9.9e-06 at D 20 to -2.24e-05 at D 20.5), that is Delta about 1.105050446. Norm F between 4e-10 and 6e-10 (80%).
- Each scan point takes 1300 to 2100 s (65%; 1625 to 1651 s at D 20.25); the scan ends 16:30 to 17:00 UTC if the regrid ends by 15:05 (four rounds on p0); all 5 processes exit 0 with the record system (90%); the repeat of 1.085 agrees (85%).
- One robust change in 1.050 to 1.120 (70%), none (8%), two or more (22%); the edge signs differ if one (85%). The change within 0.005 of 1.087574 (50%; that estimate is from a 0.03 grid); within 0.005 of dh170's final reading, if it differs (70%); within 0.002 (35%).

## Status
- 2026-11-23 13:40 UTC: folder, inputs, lane and the reading prepared before any run; dry run of the lane passed (13:39:23 UTC; pins, lambda_0(20.5) 2.1088217835, selftests 0 0 0 1 1 0 0 1).
