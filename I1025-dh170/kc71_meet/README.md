# I1025-dh170/kc71_meet: #1025 k_c 71 at D 19.1875 and D 19.25, where k_c 71's pair of changes may meet, hybrid sign scans lambda 1.42 to 1.58 at 0.01

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-22 15:04:02 UTC, before any run of this folder. Raw origin/main when the inputs were taken: 8e4797ff.

## Order (the coordinator t5's hc, 22 Nov), quoted in part
"#1025: k_c 71 at D 19.1875 and D 19.25, where k_c 71's pair may meet. win2 is pushing those states now (I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.187500.npy and _D19.250000.npy, record l1kc71Lw1025.jsonl); start each lane when its state is on raw. 1. Control first, 1 process: d18_hybsign.py at D 19.0, k_c 71, win2's D 19 state and record, lambda 1.55; it must print the record system, and the hybrid sign and ln|det| of win2's lambda 1.55 row (I1025-win2/kc71_leap/scan_D19_P*.jsonl) to 1e-6 relative. dh610 passed this at 6.2e-8 (raw c8d98339); if yours fails, stop and report. 2. Lane 1: D 19.1875, lambda 1.42 to 1.58 at 0.01 (17 values) plus a repeat of 1.50. Lane 2: D 19.25, the same window. 4+4 threads, nice 10, systemd units, 8 h caps; d18_hybsign.py unmodified, read_lower.py. 3. Raw folder I1025-dh170/kc71_meet/, README first, with k_c 71's changes at D 19.125 beside which you will report yours (information, not a pass rule). Read: every robust change with det-linear estimate and range, orientation as printed; any ln|det| minimum without a change (a merged pair); the repeats. Estimate: control ~15 min, lanes ~2.5-3 h. Post on #1025, send me the verdict with the raw commit."
Follow-up (hc): "both states are on raw now, commit 8e4797ff [...], record states/l1kc71Lw1025.jsonl (12 lines). Start the lanes after your control passes. Later states (leg 2, after 15:50) come under tag l1kc71Lw1025b (states/sol_l1kc71Lw1025b_D*.npy, record states/l1kc71Lw1025b.jsonl)."

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs, and every script here refuses to start on any other blob)
| item | raw path | blob |
|---|---|---|
| D 19.0 state (control) | I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.000000.npy | f320a4c1 |
| D 19.1875 state (lane 1) | same folder, sol_l1kc71Lw1025_D19.187500.npy | 0849e005 |
| D 19.25 state (lane 2) | same folder, sol_l1kc71Lw1025_D19.250000.npy | 36bc6b83 |
| record, 12 rows D 18.5625 to 19.25 (the order's path lacks `states/`) | I1025-win2/kc71_leap/states/l1kc71Lw1025.jsonl | c5fc14a9 |
| win2's D 19 scan, its lambda 1.55 row: hybrid +1, ln|det| -2208.97905006932 | I1025-win2/kc71_leap/scan_D19_P2.jsonl | b5aaf575 |
| the scanner, xfkappa's, unmodified | I1025-mac/d18/d18_hybsign.py | e089207a |
| change finder (xfkappa's) | I1025-mac/d18/d185_scan_read.py, d18c_read.py | 7c9d400f, 1383470f |
| reader (mine, `../lower_root/read_lower.py`, the same blob as dh610's copy; its planted selftest has six cases on both grids, two mutations `shift` and `round2`) | | 89309d3c |
| `repeat_check.py`, `control_check.py` (dh610's, raw c8d98339) | I1025-dh610/kc71_d19125/ | aaf598a9, c8ef82e5 |
| dh610's D 19.125 reading and exits, for the comparison below | I1025-dh610/kc71_d19125/read_lower.txt, exits_kc71.txt | 6acc88fb, 8e1951f1 |
Record rows used: D 19.0 |F| 2.7619908383e-10, 2676 steps; D 19.1875 |F| 2.9139861587e-10, 2639 steps, psi-constraint 1.885e-3, Delta 1.0722612310; D 19.25 |F| 3.0023964493e-10, 2630 steps, 1.990e-3, Delta 1.0737683214 (kappa 0.7, u0 0.04, Ks 30, h 0.0625). Code: worktree `~/Source/choptuik-large-d-1025p4` at 505d8399 (clean, checked by each script), python the #1058 venv (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble's package with `dd_logdet`).

## Commands (systemd user units, so no terminal owns them)
    systemd-run --user --unit=i1025-kc71ctl --working-directory=$PWD ./control_kc71.sh
    systemd-run --user --unit=i1025-kc71a --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 kc71_meet D 19.1875" --mode=block ./lane_kc71.sh 1
    systemd-run --user --unit=i1025-kc71b --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 kc71_meet D 19.25" --mode=block ./lane_kc71.sh 2
    systemd-run --user --unit=i1025-kc71read --working-directory=$PWD ./read_kc71.sh        (waits for both lanes, then reads)
- **Control** (`control_kc71.sh`): `d18_hybsign.py in/l1kc71Lw1025.jsonl in/sol_l1kc71Lw1025_D19.000000.npy 19.0 1.55 control/scan_D19.0_p0.jsonl`, 1 process of 4 threads at nice 10, 3 h cap by exact pid. Pass (`control_check.py`, selftest passes, its `--mutate` exits 1): the log prints the record system; the hybrid sign equals win2's (+1); ln|det| equals win2's -2208.97905006932 to 1e-6 relative (win2 is a Windows build). Else stop and report; the lane script refuses to start unless `control/control_check.txt` says PASS.
- **Lanes** (`lane_kc71.sh 1|2`): pins, the planted `ell_ddm.py selftest` (must PASS) and `--mutate=slices` (must FAIL), then `nice -n 10 /usr/bin/time -v d18_hybsign.py in/l1kc71Lw1025.jsonl STATE D LAMS lane<N>/scan_D<D>_p0.jsonl`, 4 threads, 8 h cap by exact pid, a memory sampler every 30 s (alert only). **Window:** lambda 1.42, 1.43, ..., 1.58 (17 values), then a repeat of 1.50: 18 evaluations per lane. Per point: the hybrid sign (float64 blocks 0-11, dd block 12), the 1e-15 noise test on blocks 0-11 with 2 seeds, the float64 sign beside. The system check is the script's first line (exit 3 stops the lane and I report).
- **Reading** (`read_kc71.sh`): `read_lower.py` on each lane, then `repeat_check.py`.

## Reading, fixed now (the coordinator's)
Every robust change (both neighbouring points noise-robust) with bracket, orientation as printed (not compared across D), det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure); changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged (a merged pair would show as one); the repeat of 1.50 must agree (sign, ln|det| within 1e-6, noise signs, float64 sign), else "repeat disagrees; no reading". The float64 sign is beside the hybrid's (information). The lower root's physical status is open (t5); these are k_c 71 changes, not yet physical roots.

## k_c 71's changes at D 19.125, beside which mine are reported (information, not a pass rule)
dh610, raw ee09203f (`ref_dh610_D19.125_read_lower.txt`), lambda 1.44 to 1.58 at 0.01: hybrid signs + from 1.44 to 1.48, - at 1.49, 1.50, 1.51, + from 1.52 to 1.58; **robust + to - in (1.48, 1.49), det-linear 1.488137, range [1.486996, 1.488137]; robust - to + in (1.51, 1.52), 1.511209, range [1.511209, 1.511571]**; 0.0231 apart; no ln|det| minimum without a change. At D 19 (win2, raw 2c37fd37): one change, - to + at 1.536547, none in 1.40 to 1.53 (so the + to - change sat below 1.40).
Straight lines, information: the - to + change from 1.536547 (D 19) to 1.511209 (D 19.125), -0.2027 per unit D: 1.4986 at D 19.1875, 1.4859 at D 19.25. The + to - change from below 1.40 (D 19) to 1.488137 (D 19.125), at least +0.705 per unit D: at least 1.5322 at D 19.1875 and 1.5763 at D 19.25. With those slopes the two lines cross near D 19.150, before D 19.1875.

## Predictions, registered before the runs (mine, information)
- control passes (6e-8 as dh610's) about 90%; the system checks pass in both lanes about 90%; both repeats agree about 90%; every point noise-robust: about 75% per lane;
- D 19.1875: no robust change in the window (a merged pair) about 45%, two changes about 40%, one change about 10%, other about 5%; D 19.25: none about 50%, two about 35%, one about 10%, other about 5%; a ln|det| minimum without a change in a lane without a change about 70%;
- the float64 sign differs from the hybrid at no more than 5 points per lane about 65% (dh610's D 19.125: 2 of 16);
- seconds a point with 4 threads beside the other lane: 650 to 900 s about 60% (dh610's control: 778 s on 1 thread alone); a lane 3.3 to 4.5 h about 55%; both inside the 8 h caps about 95%; max RSS below 2.5 GiB about 90% (dh610: 1.56 GB).

## Acceptance (the coordinator's)
Control passes; both lanes exit 0 with the system check passing; the reader's selftest passes and its mutations fail; the repeats agree. A lane that stops (exit 3 included) or a control that fails stops me and I report.

## Budget
One process of 4 threads for the control, then two of 4 threads at nice 10. Nothing else of mine runs; the i349 and other agents' jobs: none seen on dh170 (load average 0.1 at 15:01 UTC).

## Log
- 2026-11-22 15:04:02 UTC: folder, scripts, pins, controls and the reading prepared before any run. Selftests: `control_check.py` PASS and its mutate FAIL; `read_lower.py` PASS, `shift` and `round2` FAIL; `repeat_check.py` PASS (`selftest_exits.txt`: 0 1 0 1 1 0). Dry runs: the control's pins pass; a lane refuses without a control PASS (as it must).
- 2026-11-22 16:16:19 UTC: **lane 2 (D 19.25) stopped on t5's order** (hc, about 16:15: stop the unit after the point in flight lands; dh610 reruns the whole D 19.25 window on 6 processes after about 17:15 and my points become a cross-machine check). Lane 2's fourth point had landed at 16:16:03, 2 s before my waiter (`stop_lane2_after_point.sh`, `stop_lane2.log`) started; it would have held lane 2 for a fifth point, so I stopped the waiter and ran `systemctl --user stop i1025-kc71b` at once; the fifth point (1.46, started 16:16:03) was lost, 16 s of work. Lane 2's four finished points (all hybrid +1, noise-robust, float64 +1; sec per point 956, 911, 915, 912): lambda 1.42 ln|det| -2186.7628971332; 1.43 -2187.2342474896; 1.44 -2187.7516439930; 1.45 -2188.3515899133. The folder was renamed `lane2/` to `lane2_stopped/`, nothing deleted (its `exits.txt` has a line for the stop).
- 2026-11-22 16:16:33 UTC: the reader unit `i1025-kc71read` (`read_kc71.sh`, which waits for both lanes) was stopped and `i1025-kc71read1` started on `read_kc71_lane1.sh` (the same reading of lane 1 only, lane 2's four points listed beside). Lane 1 (unit `i1025-kc71a`, D 19.1875, 4 of 18 evaluations at 957, 914, 913, 913 s side by side) runs on alone: new ETA about 18:35 UTC at about 585 s a point (the control alone took 571 s).
- 2026-11-22 16:16:59 UTC: the stop recorded (this entry).
