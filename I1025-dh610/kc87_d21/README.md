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

## Result (`summarize_kc87d21.py` > `summary_kc87d21.txt` prints the tables from the files; its control `--mutate` FIRED (exit 1); `selftest` exit 0, `selftest --mutate` exit 1)
The signs in the scan table are printed as each reader prints them, side by side by lambda; they are not compared across k_c (a root is identified by its position).

| record | k_c 87 (regrid, this machine) | k_c 79 source (win2's leap) | k_c 87 minus k_c 79 |
|---|---|---|---|
| F_start | 2.288336927471666e-05 | 1.0334830553286102e-05 | +1.255e-05 |
| F | 4.610998301576713e-10 | 4.6401788196957317e-10 | -2.918e-12 |
| steps | 2948 | 2678 | +2.700e+02 |
| constraint | 0.0031763514726419 | 0.004719788472577341 | -1.543e-03 |
| Delta | 1.118229686747366 | 1.1182445857206806 | -1.490e-05 |
| seconds | 5457 | 4610 |  |
| steps ratio | 1.1008 | | |

| lambda | hybrid sign (k_c 87 mine, k_c 79 leg) | noise signs (robust) | float64 sign | ln of abs det (k_c 87 mine, k_c 79 leg) | seconds |
|---|---|---|---|---|---|
| 0.895 | -, + | -- (True) | - | -2621.950113, -2323.535702 | 4528 |
| 0.900 | -, + | -- (True) | - | -2622.742195, -2324.341619 | 3483 |
| 0.905 | -, + | -- (True) | - | -2623.754412, -2325.484061 | 4233 |
| 0.910 | -, - | -- (True) | + | -2625.789586, -2327.768664 | 4419 |
| 0.910 | -, - | -- (True) | + | -2625.789586, -2327.768664 | 4527 |
| 0.915 | +, - | ++ (True) | + | -2625.112642, -2325.979162 | 4096 |
| 0.920 | +, - | ++ (True) | + | -2624.689784, -2325.722545 | 4845 |
| 0.925 | +, - | ++ (True) | + | -2624.661892, -2325.715028 | 3517 |

scan points: 8 evaluations, seconds per point min 3483, median 4326, max 4845, sum 33648; outside 1500 to 3500 s: [(0.895, 4528), (0.905, 4233), (0.91, 4419), (0.91, 4527), (0.915, 4096), (0.92, 4845), (0.925, 3517)]
float64 sign differs from the hybrid at: [0.91, 0.91]; not noise-robust: none

control: the two-point root of the k_c 79 leg rows at 0.905 and 0.910 is 0.909538; its reader's det-linear is 0.909538; difference -3.12e-08 (bar 1e-5): ok
this scan's reader: robust changes 1: (0.910, 0.915), - to +, det-linear 0.911685, range [0.911139, 0.911685]
k_c 87 minus k_c 79 (0.909538): +0.002147; within 0.002: False; within 0.005: True; within 0.0005: False
source check exits (kc79 check, controls F, steps, kc87 check): ('0', '1', '1', '1'); acceptance exits (kc87 check, controls F, steps, kc79 check): ('0', '1', '1', '1'); ell_refine ('0', '5460'); processes that printed the record system 8 of 8; pair check exit 0; lane 2.88 h

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc87_d21/scan 0.895 0.925
points 7 in 0.895-0.925; not noise-robust: none
hybrid signs: 0.895- 0.900- 0.905- 0.910- 0.915+ 0.920+ 0.925+
float64 sign differs from the hybrid sign at: [(0.91, '-', '+')]
repeated points: [(0.91, 'agree')]
  robust change (0.910, 0.915), - to +, det-linear 0.911685, range [0.911139, 0.911685]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 0.895, + at 0.925
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc87_d21/scan/scan_D21.0_all.jsonl: lambda [0.91]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.895- 0.900- 0.905- 0.910- 0.915+ 0.920+ 0.925+
robust changes: 1
   change (0.910, 0.915), - to +, det-linear 0.911685, range [0.911139, 0.911685]
against k_c 79 (win2's leg, D 21.0, det-linear 0.909538):
| position | mine: bracket, orientation as printed, det-linear, estimator range | k_c 79 (win2's leg, D 21.0, det-linear 0.909538): det-linear | mine minus it | within 0.002 |
|---|---|---|---|---|
| 1 | (0.910, 0.915), - to +, 0.911685, [0.911139, 0.911685] | 0.909538 | +0.002147 | False |
```

- **Regrid:** `ell_refine.py` exit 0, wall 5460 s (the record's 5457 s), 8 threads at nice 10 (ps samples: 7.2 to 7.7 cores busy, peak RSS 2.16 GiB). The record: |F| 4.610998301577e-10 (k_c 79's 4.640179e-10), steps 2948 (2678; ratio 1.1008), F_start 2.288e-05, constraint 0.003176, Delta 1.118229686747 (k_c 79's 1.118244585721). `kc87_syscheck_1025.py` exit 0, `--mutate=F` and `--mutate=steps` exit 1, `kc79_syscheck_1025.py` on it exit 1 (refuses): ACCEPTED at 03:25:53 UTC. The state and record were pushed at 04:14 UTC at the coordinator's order, with `VERDICT.txt` (raw 6e89d627), for dh370's k_c 87 leg as its second seed.
- **Scan:** 8 evaluations, all 8 processes printed the record system (|F| 4.6119182116e-10 against the record's 4.6109983016e-10, 2948 steps). Seconds per point 3483 to 4845 (median 4326), the load average median 18.23 (max 22.98: this scan's 8 processes, the leg lane's 8 processes for 03:26 to 04:01 and 04:22 to 04:46 UTC, the recount's 2), peak RSS per process 2.03 to 2.19 GiB (`/usr/bin/time -v`), MemAvailable at least 44.39 GiB. The lane, pins line to the scan's end, took 2.88 h (01:54:17 to 04:46:49 UTC).
- **One robust change in the window 0.895 to 0.925:** (0.910, 0.915), "- to +" as the reader prints it, det-linear **0.911685**, estimator range [0.911139, 0.911685] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs: - at 0.895, + at 0.925. No ln|det| minimum without a sign change; every point noise-robust. The k_c 87 root is not yet physical.
- **The repeat of 0.910** (p3 and p7) is bit-identical (hybrid -, ln|det| -2625.789586 in both; the pair check exit 0, `repeat_check.py` PASS).
- **Against k_c 79's 0.909538 (win2's leg, D 21.0; its bracket (0.905, 0.910), range [0.909234, 0.909538]):** +0.002147 by position. That is outside the bar written before (0.002) by 0.000147, inside 0.005, and not within 0.0005. The two brackets are adjacent (the grid step 0.005) and the two estimator ranges do not overlap. The coordinator's note: at D 20.90625 the step was 0.00013.
- **The float64 sign differs from the hybrid at 0.910** (both evaluations; float64 +, hybrid -); float64 alone would put the change in (0.905, 0.910), the bracket of k_c 79's root. The hybrid is read.
- **Control of the summarizer:** the two-point root of k_c 79's own leg rows (0.905 and 0.910) is 0.909538 and the reader's det-linear 0.909538 (difference -3.12e-08, bar 1e-5).

### Predictions scorecard (written before the run; right = the stated event happened)
| prediction (registered before the run; right = the stated event happened) | result | verdict |
|---|---|---|
| source accepted by the k_c 79 check (controls 1 1) and refused by the k_c 87 check (92%) | ('0', '1', '1', '1') | right |
| regrid exit 0 (92%) | ('0', '5460') | right |
| regrid accepted by the k_c 87 check, controls 1 1, refused by the k_c 79 check (85%) | ('0', '1', '1', '1') | right |
| steps ratio k_c 87 / k_c 79 between 1.05 and 1.15 (60%) | 1.1008 | right |
| regrid wall 2000 to 4500 s (60%) | 5460 | WRONG |
| all 8 scan processes print the record system (90%) | 8 of 8 | right |
| the repeat of 0.910 agrees (92%) | pair check exit 0 | right |
| every point noise-robust (85%) | none | right |
| one robust change in the window (80%) | 1 | right |
| the change within 0.002 of 0.909538 (65%) | +0.002147 | WRONG |
| within 0.005 (85%) | +0.002147 | right |
| within 0.0005 (25%) | +0.002147 | WRONG |
| float64 sign agrees with the hybrid at all 8 evaluations (55%) | [0.91, 0.91] | WRONG |
| scan points 1500 to 3500 s each (65%) | 3483 to 4845 | WRONG |
| the lane ends within 3.0 h of its pins line (65%) | 2.88 h | right |

Seconds per point and the regrid's wall were above their ranges; the regrid ran at 8 threads beside the k_c 79 leg lane (8 processes: D 21.03125 from 02:07 to 02:49 UTC, D 21.0625 from 03:05 UTC) and the recount (2 threads), a load the D 20.5 regrid (3076 s at 8 threads) did not have in that form; that this is the cause is not tested.

## Status
- 2026-11-24 01:54 UTC: folder, inputs, lane, reader and summarizer written (selftests as wanted: reader 0 and 1, summarizer 0 and 1, lane dry run 0); the unit `i1025an` starts after this README is pushed.
- 2026-11-24 03:25 UTC: the regrid ended (exit 0, wall 5460 s) and was ACCEPTED (kc87_syscheck exit 0, both controls exit 1, kc79_syscheck refuses); the scan started 03:25:53.
- 2026-11-24 04:14 UTC: at the coordinator's order (dh370's k_c 87 leg takes it as seed B) the state and record are copied from regrid/ to this folder's root beside a `VERDICT.txt` whose first line is `ACCEPTED`, and pushed with the scan still running (the scan files in this push are a snapshot); the summary, the scorecard and the verdict on the scan follow when the lane ends.
- 2026-11-24 05:08 UTC: the lane ended (scan 03:25:53 to 04:46:49, 8 of 8 exit 0); summary, Result and scorecard above: 10 of 15 registered predictions right; the k_c 87 root at D 21.0 is 0.911685, +0.002147 from k_c 79's 0.909538 (bar 0.002 missed).
