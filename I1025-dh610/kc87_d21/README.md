# I1025-dh610/kc87_d21: k_c 87 at D 21.0 on Linux, regridded from win2's restarted k_c 79 leap state at D 21.0 and scanned at lambda 0.895 to 0.925, against the k_c 79 root 0.909538

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 01:54 UTC, before any run of this folder. The k_c 87 and k_c 79 roots are not yet physical. A root is identified by position, never by sign orientation (printed as the reader prints it, not compared across k_c).

## Order (coordinator t5, hc after record_c was accepted), in part
"With your free 8 threads (#1025, beside the leg lane): k_c 87 at D 21.0 from the restarted leap's D 21.0 state (win2 raw 497efffe: state 3626d0b1, record 4eca1b01, tag l1kc79Lw1025f; pin by blob): kc79_syscheck accept (controls exit 1), ell_refine.py l1kc79Lw1025f 79 l1kc87dh610e 87 1 21.0 <lam0_at(21.0), in the README> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (8 threads, nice 10), kc87_syscheck accept (controls exit 1, kc79 refusing); then d18_hybsign 0.895-0.925 by 0.005 plus a repeat of 0.910, read_lower. Written before: within 0.002 of k_c 79's 0.909538 (at D 20.90625 the step was 0.00013). Raw I1025-dh610/kc87_d21/, README first."

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lane refuses any other blob)
| item | blob |
|---|---|
| win2's k_c 79 leap state at D 21.0 `sol_l1kc79Lw1025f_D21.0000.npy` (win2's file `sol_l1kc79Lw1025f_D21.000000.npy` renamed to the 4-decimal name `ell_refine.py` reads; the bytes are unchanged) and record `l1kc79Lw1025f.jsonl` (`I1025-win2/kc79_leap/states`, commit 497efffe; the same pins as `../kc79_leg/D21.0/in_blobs.txt`) | 3626d0b1, 4eca1b01 |
| `kc79_syscheck_1025.py`, `kc87_syscheck_1025.py` | 29dce7ea, 6df5d960 |
| `d18_hybsign.py` (xfkappa's, unmodified), `read_lower.py`, `d185_scan_read.py`, `d18c_read.py`, `repeat_check.py` | e089207a, 89309d3c, 7c9d400f, 1383470f, aaf598a9 |
| `ref_k79_leg_scan_D21.0.jsonl`, `k79_read_lower_D21.0.txt`: the k_c 79 scan of this D (`../kc79_leg/D21.0/scan/scan_D21.0_all.jsonl` and `read_lower.txt`: robust change (0.905, 0.910), det-linear 0.909538, range [0.909234, 0.909538]) | in `in_blobs.txt` |
| `kc87d21_read.py` (mine, from `../kc87_d205/in/kc87d205_read.py`: the k_c 87 changes beside k_c 79's 0.909538 by position, bar 0.002; selftest exit 0, `--mutate` exit 1) | in `in_blobs.txt` |
Code: `ell_refine.py` 631e5801 and `ell_delta.py` fde699f5 in `~/Source/choptuik-large-d-1025g` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399); `d18_hybsign.py` in `~/Source/choptuik-large-d-1025f` at 505d8399; python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2). lambda_0(21.0) = **2.1067409501** (`ell_delta.lam0_at(21.0, *ell_delta.lam0_table())`, rounded to 10 decimals as the D 20.5 order's 2.1088217835; the lane recomputes and refuses a different value).

## Commands (`lane_kc87_d21.sh` via `start_kc87_d21.sh` = systemd user unit i1025an under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails; `notify_kc87.sh` sends the coordinator an hc line at the source check, the regrid's end, its acceptance, the pair check of 0.910 and the end)
1. Pins and the tools' controls: selftests of the two syscheck scripts (exit 0), `read_lower.py` and its two mutations (0 1 1), `repeat_check.py` (0), `kc87d21_read.py` (0) and its `--mutate` (1). Dry run passed at 01:53:40 UTC (its three lines are the first of `exits_kc87_d21.txt`).
2. The source: `kc79_syscheck_1025.py` accepts it (exit 0; `--mutate=F` and `--mutate=steps` exit 1) and `kc87_syscheck_1025.py` refuses it (exit 1).
3. The regrid: the order's `ell_refine.py` command, 8 threads, nice 10, cap 21600 s (a time cap only), in `solver/matter` of 1025g; refuses to start with less than 8 GiB free.
4. Acceptance: `kc87_syscheck_1025.py` on the result (exit 0; `--mutate=F` and `--mutate=steps` exit 1) and `kc79_syscheck_1025.py` refusing it (exit 1), else the scan is not started.
5. The scan: `d18_hybsign.py` at 0.895 to 0.925 by 0.005 (7 values) and a repeat of 0.910 (8 evaluations), 8 processes of 1 thread, nice 10 (the repeat and its original run together). When both 0.910 rows exist a watcher runs `repeat_check.py` and logs the result (it stops nothing). Each process prints the record system first (exit 3 if not). Refuses to start with less than 8 x 2.5 GB + 4 GB free.
6. The reading: `read_lower.py scan 0.895 0.925`, `repeat_check.py` on the merged rows, `kc87d21_read.py`; `summarize_kc87d21.py` (tables, a control on the k_c 79 two-point formula, scorecard; `selftest` exit 0, `selftest --mutate` exit 1, `--mutate` on the real files exit 1 with "control FIRED") after.
Threads: 8 (regrid or scan) beside the k_c 79 leg lane (8 per point; the leg lane is also nice 10, so its priority is by order only) and the #1076 recount's 2: 18 of 20 while both run.

## Acceptance (fixed before the run)
- The source accepted by the k_c 79 check (controls exit 1) and refused by the k_c 87 check; the regrid exits 0 and is accepted by `kc87_syscheck_1025.py` with both controls exit 1 and refused by the k_c 79 check (a failing control stops the work and I report it; no bar is loosened); every scan process prints the record system.
- Reported: the regrid's norm F, steps, Delta (beside the k_c 79 record at D 21.0), wall; every robust change by position with bracket, orientation as printed, det-linear and range, beside k_c 79's 0.909538; the repeat of 0.910; the edge signs; ln|det| minima without a sign change; the float64 sign against the hybrid; seconds per point.
- **The coordinator's reading, written before:** one robust change within 0.002 of k_c 79's det-linear 0.909538 (k_c 79 at D 21.0: robust change (0.905, 0.910), range [0.909234, 0.909538]; the coordinator notes that at D 20.90625 the step was 0.00013). Reported by position; a different count is reported as it is.

## Predictions, registered before the run (mine, information)
- The source is accepted by the k_c 79 check with both controls exit 1 and refused by the k_c 87 check (92%); the regrid exits 0 (92%) and is accepted by the k_c 87 check with both controls exit 1 and refused by the k_c 79 check (85%).
- The regrid's steps ratio k_c 87 over k_c 79 (D 20.5: 1.1007) is between 1.05 and 1.15 (60%); its wall is 2000 to 4500 s (60%; D 20.5: 3076 s with the recount's 12 beside).
- All 8 scan processes print the record system (90%); the repeat of 0.910 agrees (92%); every point noise-robust (85%).
- One robust change in the window (80%; none 12%, two or more 8%). It lies within 0.002 of 0.909538: 65%; within 0.005: 85%; within 0.0005: 25%.
- The float64 sign agrees with the hybrid at all 8 evaluations (55%; at the k_c 79 D 21.0 scan it did).
- Each scan point takes 1500 to 3500 s (65%; k_c 79's D 21.0 points 1651 to 2137 s; k_c 87's at D 20.5, 998 to 1758 s with 5 processes); the lane (pins to the scan's end) takes at most 3.0 h (65%).

## Status
- 2026-11-24 01:54 UTC: folder, inputs, lane, reader and summarizer written (selftests as wanted: reader 0 and 1, summarizer 0 and 1, lane dry run 0); the unit `i1025an` starts after this README is pushed.
