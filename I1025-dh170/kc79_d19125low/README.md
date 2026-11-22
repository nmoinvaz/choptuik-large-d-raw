# I1025-dh170/kc79_d19125low: #1025 the k_c 79 lower root at D 19.125, hybrid sign scan lambda 1.10 to 1.44 at 0.02 on dh370's k_c 79 state

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-22 18:27:52 UTC, before any run of this folder. Raw origin/main when the inputs were taken: 9cd09b8a.

## Order (the coordinator t5's hc, 22 Nov), quoted in part
"The k_c 79 lower root at D 19.125, on dh370's k_c 79 state (a Linux build, like yours). k_c 71 had it at 1.488137 there; k_c 79 has no change in 1.44-1.50. Together with D 19 (1.483 at k_c 63, 1.296 at k_c 71) this tests at a second D whether the lower root recedes as k_c grows. 1. Control, 1 process: d18_hybsign.py on dh370's k_c 79 D 19.125 state and record (raw I1025-dh370/kc79_d19125/, 79b57212 or later; pin by blob) at lambda 1.50; it must print the record system and dh370's hybrid sign and ln|det| at 1.50 (its scan file there) to 1e-9 relative (Linux to Linux; dh370 and dh610 agreed to 0 at k_c 63). Stop and report if not. 2. Scan: lambda 1.10 to 1.44 at 0.02 (18 values) plus a repeat of 1.30, two lanes of 4 threads (or 8 of 1), nice 10, systemd units, read_lower.py. 3. Raw folder I1025-dh170/kc79_d19125low/, README first with k_c 71's 1.488137 beside which you report k_c 79's (information, not a pass rule). Report every robust change with det-linear estimate and range, the edge signs, any minimum without a change; call them k_c 79 roots. Estimate ~1.5 h. Post on #1025, send me the verdict with the raw commit."

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and every script refuses to start on any other blob)
| item | raw path | blob |
|---|---|---|
| k_c 79 D 19.125 state (dh370's regrid of win2's k_c 71 state, accepted by winb's check, VERDICT 15:51:03 UTC) | I1025-dh370/kc79_d19125/sol_l1kc79dh370_D19.1250.npy (the same blob as `in/` there) | 3ff3fcb5 |
| its record, one row: D 19.125, k_c 79, kappa 0.7, u0 0.04, Ks 30, |F| 2.9245143117e-10, 2949 steps, psi-constraint 8.306e-4, Delta 1.0707569213 | I1025-dh370/kc79_d19125/l1kc79dh370.jsonl | 15ac964f |
| dh370's scan rows at raw 9cd09b8a (12 rows, lambda 1.44 to 1.55; the six `scan/scan_D19.125_p*.jsonl` files, source blobs in `in/ref_dh370_scan_sources.txt`); the control's reference row `in/ref_dh370_row_lam1.50.jsonl`: hybrid -1, ln|det| -2537.823195774449, noise-robust, float64 -1 (one thread, 3813 s) | I1025-dh370/kc79_d19125/scan/ | rows file, row file |
| dh370's partial reading (12 of 16 points) | I1025-dh370/kc79_d19125/read_lower_partial_12pts.txt (raw 282c8fe2) | efb74ae9 |
| the scanner, xfkappa's, unmodified | I1025-mac/d18/d18_hybsign.py | e089207a |
| change finder (xfkappa's) | I1025-mac/d18/d185_scan_read.py, d18c_read.py | 7c9d400f, 1383470f |
| reader (mine, `../lower_root/read_lower.py`, the same blob as dh610's and dh370's copies); `repeat_check.py` (dh610's); `cross_check.py` (mine, `../lower_root/cross_check_mac.py`) | | 89309d3c, aaf598a9, and its own blob in `in_blobs.txt` |
| the control's checker (mine, derived from dh610's `control_check.py` c8ef82e5, bar 1e-6, kept as `in/control_check_k71_bar1e-6.py`) | `in/control_check_k79.py`, bar 1e-9 | in `in_blobs.txt` |
| k_c 71 at D 19.125, for the comparison (dh610, raw ee09203f) | I1025-dh610/kc71_d19125/read_lower.txt | 6acc88fb |
Code: worktree `~/Source/choptuik-large-d-1025p4` at 505d8399 (clean, checked by each script; dh370 notes its `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's), python the #1058 venv (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble's package with `dd_logdet`).

## Commands (systemd user units, so no terminal owns them)
    systemd-run --user --unit=i1025-k79ctl --working-directory=$PWD ./control_k79.sh
    systemd-run --user --unit=i1025-k79a --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 kc79_d19125low p0" --mode=block ./scan_k79.sh 0
    systemd-run --user --unit=i1025-k79b --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 kc79_d19125low p1" --mode=block ./scan_k79.sh 1
    systemd-run --user --unit=i1025-k79read --working-directory=$PWD ./read_k79.sh        (waits for both processes, then reads)
- **Control** (`control_k79.sh`): `d18_hybsign.py in/l1kc79dh370.jsonl in/sol_l1kc79dh370_D19.1250.npy 19.125 1.50 control/scan_D19.125_p0.jsonl`, 1 process of 4 threads at nice 10, 3 h cap by exact pid. **Pass** (`control_check_k79.py`; its selftest of nine cases passes and `--mutate`, which raises the bar to 1e-6, exits 1): the log prints the record system, the hybrid sign equals dh370's (-1), the point is noise-robust, and ln|det| equals dh370's -2537.823195774449 to **1e-9 relative**. Else stop and report; the scan script refuses unless `control/control_check.txt` says PASS.
- **Scan** (`scan_k79.sh 0|1`): pins, the planted `ell_ddm.py selftest` (must PASS) and `--mutate=slices` (must FAIL), then `nice -n 10 /usr/bin/time -v d18_hybsign.py in/l1kc79dh370.jsonl STATE 19.125 LAMS scan/scan_D19.125_p<P>.jsonl`, 4 threads, 8 h cap by exact pid. **Window:** lambda 1.10, 1.12, ..., 1.44 (18 values) and a repeat of 1.30: 19 evaluations in two processes: p0 the even-index values (1.10, 1.14, ..., 1.42: 9), p1 the odd-index ones (1.12, 1.16, ..., 1.44: 9) and the repeat of 1.30 at its end (10), so the repeat is on another process than the first 1.30. Per point: the hybrid sign (float64 blocks 0-11, dd block 12), the 1e-15 noise test on blocks 0-11 with 2 seeds, the float64 sign beside. The system check is the script's first line (exit 3 stops the process and I report).
- **Reading** (`read_k79.sh`): `read_lower.py scan 1.10 1.44`, `repeat_check.py` on the merged file, and `cross_check.py` of my 1.44 against dh370's 1.44 row.

## Reading, fixed now (the coordinator's)
Every robust change (both neighbouring points noise-robust) with bracket, orientation as printed (not compared across D), det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure); the edge signs (the endpoint signs of the window); changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged; the repeat of 1.30 must agree (sign, ln|det| within 1e-6, noise signs, float64 sign), else "repeat disagrees; no reading". The float64 sign is beside the hybrid's (information). They are called k_c 79 roots (not yet physical ones). Seam (information, a bar in the script): my 1.44 must have the same sign as dh370's 1.44 (-1) and be noise-robust; the ln|det| difference is printed.

## Beside which k_c 79's are reported (information, not a pass rule)
- **k_c 71 at D 19.125** (dh610, raw ee09203f): hybrid signs + from 1.44 to 1.48, - at 1.49, 1.50, 1.51, + from 1.52; robust + to - in (1.48, 1.49), det-linear **1.488137**, range [1.486996, 1.488137]; robust - to + in (1.51, 1.52), 1.511209. At D 19: k_c 71's lower root at 1.296, k_c 63's at 1.483 (t5).
- **k_c 79 at D 19.125** (dh370, raw 282c8fe2, 12 of 16 points): hybrid signs - from 1.44 to 1.50, + from 1.51; one robust change, - to + in (1.50, 1.51), det-linear 1.505784, range [1.505586, 1.505784] (its lambda_1: 1.539658 at D 19); no change in 1.44 to 1.50; no ln|det| minimum without a change. Orientation as printed: this scan's sign at 1.44 is minus, so the lower root, if it is in 1.10 to 1.44 as a + to - change (the k_c 71 orientation), has plus below it.
- The order's lines: the lower root at D 19 moves from 1.483 (k_c 63) to 1.296 (k_c 71), -0.187 for 8 more k_c; the same offset from k_c 71's 1.488137 at D 19.125 puts k_c 79's near 1.30, inside the window (information).

## Predictions, registered before the runs (mine, information)
- the control passes at 1e-9 about 90%; both system checks pass about 90%; the repeat agrees about 90%; every point noise-robust about 65% per process; the seam 1.44 equals dh370's sign about 90%;
- the reading: one robust change in 1.10 to 1.44, + to - as printed (the k_c 71 orientation) about 50%, no change about 30%, two or more about 15%, other 5%; if one, within 0.10 of 1.30 about 55% of those;
- the float64 sign differs from the hybrid at no more than 5 points per process about 50%;
- time: dh370's points took 3800 to 3900 s on 1 thread with 6 processes (i7-8700); the order's ~1.5 h would need about 500 s a point. My control (one process of 4 threads alone) measures it; I expect 1800 to 3000 s alone and 1.5 times that with two processes side by side, so **the scan could take 5 to 8 h, not 1.5 h**, and the 8 h cap is at risk for the 10-evaluation process; I decide the split from the control's time and report before launching the scan. Max RSS below 2.5 GiB about 80% (k_c 71's was 1.4 to 1.9 GiB).

## Acceptance (the coordinator's)
The control passes; the system check passes in each process; the reader's selftest passes and its mutations fail; the repeat agrees. A failed control or a stopped process stops me and I report.

## Budget
One process of 4 threads for the control, then two of 4 threads at nice 10. Nothing else of mine runs; no other job on dh170 at 18:25 UTC (load average 0.2).

## Log
- 2026-11-22 18:27:52 UTC: folder, scripts, pins, controls and the reading prepared before any run. Selftests: `control_check_k79.py` PASS and its mutate FAIL; `read_lower.py` PASS, `shift` and `round2` FAIL; `repeat_check.py` and `cross_check.py` PASS (`selftest_exits.txt`: 0 1 0 1 1 0 0). Dry runs: the control's pins pass; the scan refuses without a control PASS (as it must).

## Result (written 2026-11-22 22:17:46 UTC)
Control PASS (18:41:32 UTC, ln|det| relative difference 1.075e-15, bar 1e-9). **Both scan processes exit 0**: p0 (unit `i1025-k79a`) 18:41:41 to 22:03:47 UTC, 12126 s (3:21:56 by /usr/bin/time), 9 evaluations; p1 (`i1025-k79b`) 18:41:45 to 22:16:52, 12906 s (3:34:58), 10 evaluations. Both system checks passed (|F| 2.9245852083e-10 against the record's 2.9245143117e-10, 2949 steps equal); every point noise-robust (19 of 19 evaluations); the repeat of 1.30 (on p1, the first on p0) bit-identical (ln|det| -2529.5273571200623, sign, noise, float64); the seam, my 1.44 against dh370's, equal (sign -1, ln|det| difference -4.5e-13, `cross_check.py` PASS). Seconds per point 1321 to 1440 side by side, 776 for p1's last point (alone). Peak RSS 2.26 and 2.25 GiB (2365140 and 2361152 kB), lowest MemAvailable 24.2 and 24.6 GiB (24753 and 25181 MiB), no ALERT. The reader unit `i1025-k79read` ran at 22:16:53 UTC, exit 0 (`read_k79.txt`, `exits_read.txt`).

**Hybrid signs, as printed, lambda 1.10 to 1.44 at 0.02: minus from 1.10 to 1.22, plus from 1.24 to 1.40, minus at 1.42 and 1.44; edge signs minus and minus.** Two robust changes (both neighbours noise-robust), no change touching a non-robust point:
| position | bracket | orientation as printed | det-linear estimate | estimator range |
|---|---|---|---|---|
| the lower of the two | (1.22, 1.24) | - to + | **1.231731** | [1.223731, 1.231731] |
| the upper of the two | (1.40, 1.42) | + to - | **1.400174** | [1.400072, 1.400174] |
The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure; the first range is wide (0.008) because ln|det| is smooth there (-2525.225, -2527.684, -2528.033 at 1.20, 1.22, 1.24); the second sits within 0.0002 above the grid point 1.40, where ln|det| falls to -2539.836 (-2533.745 at 1.38, -2535.103 at 1.42). No ln|det| local minimum without a sign change. The float64 sign differs from the hybrid at 9 of 18 points (information).

**By position (t5's rule), beside k_c 71 at D 19.125 (dh610, raw ee09203f; information, not a pass rule):** k_c 71's roots there are 1.488137 (the rising root) and 1.511209 (the root near lambda_1's line); k_c 79's root near lambda_1's line is 1.505784 (dh370, raw 282c8fe2). In 1.10 to 1.44 k_c 79 has **two roots, near 1.2317 and 1.4002**: the 1.4002 root is 0.0879 below k_c 71's rising root (1.488137); the 1.2317 root is 0.2564 below it, and k_c 71 was not scanned below 1.44 at D 19.125 (dh610's window), so it has no k_c 71 counterpart in the data. This scan cannot say which of the two continues k_c 71's rising root, or whether the 1.2317 root is k_c-stable. At D 19 the order's rising root sat at 1.483 (k_c 63) and 1.296 (k_c 71), 0.187 apart for 8 more k_c.

## Predictions against the result
| prediction | result |
|---|---|
| control passes at 1e-9 (90%); both system checks pass (90%); the repeat agrees (90%); every point noise-robust (65% per process); the seam 1.44 equals dh370's sign (90%) | yes (1.075e-15); yes; yes (bit-identical); yes, 19 of 19; yes (ln difference -4.5e-13) |
| one robust change, + to - as printed, 50%; none 30%; two or more 15%; other 5% | **two** (the 15% case): near 1.2317 and 1.4002, by position; neither is the expected single change near 1.30 (the 1.2317 root is 0.068 below it, the 1.4002 root 0.100 above) |
| if one, within 0.10 of 1.30 (55% of those) | not applicable (two) |
| float64 differs at no more than 5 points per process (50%) | p0 **no** (6), p1 yes (3) |
| the scan could take 5 to 8 h (cap at risk) | **no**: 3.4 h and 3.6 h (a point 1321 to 1440 s beside the other process, 793 s alone); inside the caps. The ETA I gave t5 after the first points (22:35) was 18 min later than the actual end (22:17) |
| max RSS below 2.5 GiB (80%) | yes, 2.26 GiB |

## Log
- 2026-11-22 18:28:02 UTC: control started; 18:41:32 PASS; 18:41:41 and 18:41:45 the two scan processes started with the reader unit.
- 2026-11-22 22:03:47 and 22:16:52 UTC: the processes ended; 22:16:53 the reader ran.
- 2026-11-22 22:17:46 UTC: result written (this section).
- 2026-11-22 22:18:00 UTC: wording fixed in the predictions table (my ETA of 22:35 was 18 min later than the actual end, not the scan late).
