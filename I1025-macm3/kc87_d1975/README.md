# I1025-macm3/kc87_d1975: dh170's k_c 79 D 19.75 state regridded to k_c 87 on macm3's own build, then a hybrid sign scan (lambda 1.26 to 1.40)

Written before the run, 2026-11-22 23:35 UTC. Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025.
Coordinator t5 (hc, 2026-11-22 about 23:35 UTC). The same three steps as `../kc87_d19375/` (README there), at D 19.75 and with another source: source check, regrid to k_c 87, scan.

## Order

Why (the coordinator's, as information): lambda_1's line gives about 1.325 at D 19.75; k_c 87's second root (the rising root), which crosses lambda_1 after D 19.5, may sit near it here, so the window may hold two changes close together, or one.
Roots are read by position, never by sign orientation, across D as well as across k_c; in posts "the root near lambda_1's line" and "the second root".

1. **Source:** dh170's accepted k_c 79 D 19.75 state and record (raw `I1025-dh170/kc79_d1975/`, `sol_l1kc79dh170d1975_D19.7500.npy` blob f2ad34b5 and `l1kc79dh170d1975.jsonl` blob 0508163e, pinned at raw 5d0c8f74). `kc79_syscheck_1025.py` on it first, with its two controls.
2. **Regrid** to k_c 87 with `ell_refine.py` as at D 19.375 (`../kc87_d19375/`) and as dh610 did at D 19.5 (lambda_0 from `ell_delta.lam0_at(19.75)`, `--no-gamma`). Accept the k_c 87 state only by dh610's `kc87_syscheck_1025.py` (blob 6df5d960) with both controls; the k_c 79 check must refuse it. 6 threads, nice 10, own session.
3. **Scan** the accepted state with `d18_hybsign.py` (unmodified): lambda 1.26 to 1.40 at 0.01 (15 values) plus a repeat of 1.33, 4 processes of 1 thread, nice 10, own session under caffeinate; read with `read_lower.py` with its selftest and mutations.
Stop and report on any failure; change no code. Memory (the coordinator's correction of 2026-11-22, Nathan's rule of 2026-11-08: no guard stops or kills a process for memory): my watcher only alerts, by posting the free memory to the coordinator when available memory is under 2 GiB, free memory under 8% or free disk under 3 GiB; the only refusal is to start the scan with less than 12 GiB available (the k_c 87 scans at D 19.375 peaked at 11.2 GB for the four against 17 to 18 GiB available). Post on #1025; send each step's verdict with the raw commit.

## Inputs (pinned by `git hash-object --no-filters`; `prepare_inputs.sh` copies them with `git cat-file blob` into `in/`; `run_regrid.sh` and `run_scan.sh` check `in/` again)

```
f2ad34b5  sol_l1kc79dh170d1975_D19.7500.npy  <- 5d0c8f74:I1025-dh170/kc79_d1975/sol_l1kc79dh170d1975_D19.7500.npy  ok
0508163e  l1kc79dh170d1975.jsonl  <- 5d0c8f74:I1025-dh170/kc79_d1975/l1kc79dh170d1975.jsonl  ok
6df5d960  kc87_syscheck_1025.py  <- ec9fb489:I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py  ok
dfb42ff7  kc87_syscheck_1025.diff.dh610  <- ec9fb489:I1025-dh610/kc87_d195/kc87_syscheck_1025.diff  ok
29dce7ea  kc79_syscheck_1025.py  <- 8e4797ff:I1025-win/kc79_d19/kc79_syscheck_1025.py  ok
e089207a  d18_hybsign.py  <- 8e4797ff:I1025-dh170/kc_break/d18_hybsign.py  ok
89309d3c  read_lower.py  <- 8e4797ff:I1025-dh170/lower_root/read_lower.py  ok
7c9d400f  d185_scan_read.py  <- 8e4797ff:I1025-mac/d18/d185_scan_read.py  ok
```

The source record (dh170, k_c 79 at D 19.75, from win2's k_c 71 D 19.75 state): |F| 4.015866885481963e-10, 2839 steps, constraint 1.652e-3, Delta 1.0860054437 (his regrid 2410 s on 8 threads of an i7-7700, peak RSS 1.81 GiB). dh170's own scan of this state, lambda 1.27 to 1.38, started at 23:02:14 UTC; its result is not used here.
Code, build and venv as `../kc87_d19375/README.md`: worktree `~/Source/choptuik-large-d-1025m` at 505d8399, `venv-macm3-1058b` (Python 3.14.3, multidouble 5.1.0, hpkernel neon), `P4_WT_MATTER=<worktree>/solver/matter`; `ell_refine.py` blob 631e5801.
lambda_0: `ell_delta.lam0_at(19.75, *lam0_table())` = **2.1120935738** (error estimate 1.07e-5, the same value as dh170's; `--no-gamma` does not use it). The k_c 87 check is `kc79_syscheck_1025.py` with 3 lines changed, as in `../kc87_d19375/` (`run_regrid.sh` rebuilds the diff and requires dh610's hunks).

## Commands

Regrid (`run_regrid.sh`; the source state and its record are copied into the worktree's `solver/matter/data/` under the names `ell_refine.py` reads and checked by blob):

    cd ~/Source/choptuik-large-d-1025m/solver/matter && nice -n 10 python -u capped_run.py 21600 python -u ell_refine.py l1kc79dh170d1975 79 l1kc87macm3d1975 87 1 19.75 2.1120935738 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma        (6 threads by env, own session, caffeinate -is)

The D 19.375 command was `ell_refine.py l1kc79macm3d19375 79 l1kc87macm3d19375 87 1 19.375 2.1138515550 ...` (same options); dh610's D 19.5 command `ell_refine.py l1kc79dh370d195 79 l1kc87dh610d195 87 1 19.5 2.1132623525 ...` (8 threads, `timeout`, a systemd unit); `timeout` -> `capped_run.py` here.
`run_regrid.sh` stops at the first failure (`VERDICT.txt`, `steps.txt`): the pins, the diff of the two checks, the worktree check, lambda_0, the two selftests, the source check with its two controls and the k_c 87 check's refusal of the k_c 79 source, the regrid, the result check with its two controls and the k_c 79 check's refusal of the result.

Scan (`run_scan.sh`, after ACCEPTED, at least 12 GiB available): `d18_hybsign.py STUB STATE 19.75 "<lambdas>" OUT` in 4 processes, each under `capped_run.py 28800` by exact pid: p0 1.26,1.30,1.34,1.38; p1 1.27,1.31,1.35,1.39; p2 1.28,1.32,1.36 and the repeat 1.33; p3 1.29,1.33,1.37,1.40 (the repeat of 1.33 runs on another process than the first 1.33).
A sampler (log only) writes rss, cpu, available GiB, free memory percent and free disk every 60 s into `scan/scan_samples.csv`. Then `read_lower.py selftest`, its mutations `shift` and `round2` (each must exit 1), and `read_lower.py scan 1.26 1.40`.
Own session: `launch_1070.py` (double fork, `setsid`) running `caffeinate -is /bin/bash run_*.sh`; `session_check_*.txt` after each start. My watcher is alert-only (it posts the free memory or disk to the coordinator by hc, at most once per 10 min, and never stops, kills or signals a process; replaced at about 00:50 UTC, while the scan ran, after the coordinator's correction). The only kill in these lanes is `capped_run.py`'s wall-clock cap (28800 s for a scan process, 21600 s for the regrid), not a memory rule.

## Acceptance (fixed before the run)

1. **Source.** `kc79_syscheck_1025.py` accepts dh170's k_c 79 D 19.75 state and record on this machine (record |F| at most 1e-9, `freeze_from` gives the record's 2839 steps, the state's |F| within 1%), its selftest exits 0, both controls (`--mutate=F`, `--mutate=steps`) exit 1; extra control: `kc87_syscheck_1025.py` on the k_c 79 source exits 1. Otherwise no regrid.
2. **Result.** `kc87_syscheck_1025.py` accepts the regridded record and state (k_c 87 at D 19.75, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), its selftest exits 0, both controls exit 1; extra control: `kc79_syscheck_1025.py` on the k_c 87 result exits 1. A regrid that exits non-zero or hits the cap is a stop.
3. **Scan.** Only after ACCEPTED. Every process prints `the record system` first; anything else is a stop. The reader's selftest passes and its two mutations exit 1; the repeat of 1.33 agrees (sign, noise signs, float64 sign, ln|det| within 1e-6).

## Reading (fixed before the run; roots by position)

Every robust change by its position (bracket, det-linear estimate, estimator range; orientation is printed but not used to identify a root); the edge signs; every ln|det| minimum without a change (a candidate for two changes closer than the 0.01 step: a pair inside one cell shows no sign change); the repeat; the float64 sign beside the hybrid (information); each point's noise-robustness.
Called k_c 87 roots (macOS build). Each change is compared by distance with the line (about 1.325, the coordinator's; 1.3286 and 1.3311 below) and with k_c 87's two roots at D 19.375 (1.434463 near the line, 1.370705 the second root). The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. The window ends at 1.26 and 1.40: nothing is said outside it.

## Beside which the scan is reported (information, not a pass rule)

k_c 79's root near lambda_1's line at D 19, 19.125, 19.25, 19.375, 19.5: 1.539658 (winb), 1.505784 (dh370), 1.469975 (macm3b), 1.431552 (macm3b), 1.397565 (dh370); dh170's slope continuation gives 1.3296 to 1.3209 at D 19.75 (his README), the coordinator's 1.325.
k_c 87's root near the line: 1.434463 at D 19.375 (macm3b), 1.399169 at D 19.5 (dh610): slope -0.28235 per unit D; continued to D 19.75 it gives 1.3286 (with k_c 79's slope -0.2723 from D 19.5: 1.3311). k_c 87's second root: 1.370705 at D 19.375; at D 19.5 dh610 found only the root near the line in 1.36 to 1.44 and scanned nothing below 1.36.
k_c 71 had two roots near the line at D 19.5 (1.371531, 1.449187; win2).

## Predictions (information, not a pass rule; written before any run)

Source check passes with 2839 steps and all controls as wanted (95%); the regrid is accepted (80%) with about 3125 steps (2839 x 1.1006, the D 19.375 ratio of k_c 87 to k_c 79), taking about 17 min (12 to 25; 1051 s at D 19.375 with 3195 steps), rss max about 2.7 GB (2.68 GB at D 19.375).
The scan takes about 55 min (4 points a process at 750 to 1000 s; 45 to 70), each process 2.8 to 4.4 GB, the four together peaking near 11 GB.
Robust changes in 1.26 to 1.40: none (10%), one (40%), two (40%), more (10%). A change within 0.02 of 1.3286 (70%). Two changes within 0.05 of each other (25%).

## Status (22 Nov 2026)

| step | verdict | numbers | time (UTC) |
|---|---|---|---|
| source check (`kc79_syscheck_1025.py`) | accepted; selftests (kc79 and kc87 checks) exit 0; controls `--mutate=F` and `--mutate=steps` exit 1; extra control: `kc87_syscheck_1025.py` on the k_c 79 source exits 1 ("the record is not k_c 87 at D 19.75 (kc 79, D 19.75)") | state \|F\| 4.0195401131e-10 against the record's 4.0158668855e-10 (0.0915% apart, bar 1%); `freeze_from` 2839 steps = the record's | 23:35:50 (2 s) |
| regrid (`ell_refine.py`, exit 0), child pid 72878, own session (`session_check_regrid.txt`: every chain ends at launchd, no claude, tty ??) | **accepted** by `kc87_syscheck_1025.py` (selftest exit 0); controls `--mutate=F` and `--mutate=steps` exit 1; extra control: `kc79_syscheck_1025.py` on the k_c 87 result exits 1 ("the record is not k_c 79 at D 19.75 (kc 87, D 19.75)") | |F| 3.9802e-10, 3124 steps (freeze_from 3124 = the record's), constraint 9.697e-04, Delta 1.0860036806 (k_c 79: 1.0860054437; difference -1.763e-06); capped_run wall 1181 s (steps.txt: 1202 s with the start), the record's 1174 s; 1 core (ps %cpu 100 of 600 allowed), rss max 3.58 GB (19 samples of 60 s); 22 RuntimeWarning lines of `dss_ell.py` (D 19.375: 23) | 23:35:50 to 23:55:54 (20.1 min with the checks) |
| scan (`run_scan.sh`), 4 processes of 1 thread, all exit 0, each printed `the record system` | done, 16 evaluations (15 values and the repeat of 1.33); reader selftest exit 0, mutations `shift` and `round2` exit 1 | **two robust changes**: - to + in (1.330, 1.340), det-linear 1.338993, range [1.337945, 1.338993] (the root near the line); + to - in (1.270, 1.280), det-linear 1.276162, range [1.272785, 1.276162] (the second root, 0.062831 below it); edge signs + at 1.26 and + at 1.40; repeat of 1.33 bit-identical | 23:56:27 to 00:53:14 (56.8 min; 827 to 866 s per point; rss per process 2.63 to 4.27 GB) |

### Regrid result (22 Nov 2026, 23:35:50 to 23:55:54 UTC): ACCEPTED

Record `l1kc87macm3d1975.jsonl` (blob 84f75a48) and state `sol_l1kc87macm3d1975_D19.7500.npy` (blob 5825f5d0): k_c 87 at D 19.75, |F| 3.980170323712351e-10, F_start 6.533e-06, 3124 steps (dh170's k_c 79 state: 2839, x1.1004; at D 19.375 mine: x1.1006), constraint 9.697e-04, Delta 1.0860036806 (k_c 79: 1.0860054437).
`ell_refine.py` exit 0, capped_run wall 1181 s (the record's own 1174 s, x1.12 of the D 19.375 k_c 87 regrid's 1044 s); 1 core, rss max 3.58 GB (2.68 GB at D 19.375); load average up to 4.25 during the regrid (the system process `mediaanalysisd` held one core again; not mine); disk 25 GiB free.
Acceptance as fixed: `kc87_syscheck_1025.py` exit 0, `--mutate=F` exit 1 (the state's |F| is not within 1% of 1.5 times the record's), `--mutate=steps` exit 1 (freeze_from 3124, the record 3125); `kc79_syscheck_1025.py` on the k_c 87 result exit 1. `VERDICT.txt`: ACCEPTED 23:55:54 UTC.
My predictions: the regrid accepted: yes; about 3125 steps: 3124; about 17 min (12 to 25): 19.7 min (inside the range, above the point value); rss max about 2.7 GB: missed (3.58 GB).

### Scan result (22 to 23 Nov 2026, scan 23:56:27 to 00:53:14 UTC, 56.8 min)

All four processes exit 0 and each printed `the record system` (|F| 3.9801703237e-10, 3124 steps = the record's). 16 evaluations (15 values and the repeat of 1.33), each 827 to 866 s (mean 845 s) beside the other three processes.
Reader `read_lower.py` (89309d3c, unedited): selftest exit 0, mutations `shift` and `round2` each exit 1 (`selftest_read_lower*.txt`); reading in `read_lower.txt`.

| lambda | process | hybrid sign | ln\|det\| | noise-robust | float64 sign | seconds |
|---|---|---|---|---|---|---|
| 1.26 | p0 | + | -2799.993435 | yes | + | 858 |
| 1.27 | p1 | + | -2802.082445 | yes | + | 864 |
| 1.28 | p2 | - | -2802.555701 | yes | + | 866 |
| 1.29 | p3 | - | -2802.460129 | yes | + | 866 |
| 1.30 | p0 | - | -2802.901974 | yes | + | 835 |
| 1.31 | p1 | - | -2803.570217 | yes | + | 844 |
| 1.32 | p2 | - | -2804.444963 | yes | + | 847 |
| 1.33 | p2 | - | -2805.708990 | yes | + | 828 |
| 1.33 (repeat) | p3 | - | -2805.708990 | yes | + | 847 |
| 1.34 | p0 | + | -2807.898892 | yes | + | 838 |
| 1.35 | p1 | + | -2806.417729 | yes | + | 846 |
| 1.36 | p2 | + | -2806.318553 | yes | + | 849 |
| 1.37 | p3 | + | -2806.462248 | yes | + | 849 |
| 1.38 | p0 | + | -2806.710312 | yes | + | 831 |
| 1.39 | p1 | + | -2807.016009 | yes | + | 831 |
| 1.40 | p3 | + | -2807.359823 | yes | + | 827 |

- **Two robust changes, called by position.**
  The root near lambda_1's line: in (1.330, 1.340), - to + as printed, det-linear 1.338993, estimator range [1.337945, 1.338993].
  The second root, 0.062831 below it: in (1.270, 1.280), + to - as printed, det-linear 1.276162, estimator range [1.272785, 1.276162] (the wider range of the two).
  The range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. Orientation is printed, not used to identify a root.
- **One change or two close together? Two, 0.0628 apart.** Neither sits at the line (about 1.325, the coordinator's; 1.3286 and 1.3311 from k_c 87's own two points): 1.338993 is 0.0104 above 1.3286 and 0.0140 above 1.325; 1.276162 is 0.0524 below 1.3286.
- Edge signs: + at 1.26, + at 1.40. All 16 evaluations are noise-robust; no change touches a non-robust point. ln|det| minima without a sign change: none (the dip at 1.34, -2807.899, sits beside the upper change; at 1.27 and 1.28, -2802.082 and -2802.556, beside the lower).
- Repeat of 1.33 (process 3 against process 2): sign, noise signs, float64 sign and ln|det| (-2805.7089895001204) bit-identical: yes.
- The float64 sign differs from the hybrid at 6 points (1.28 to 1.33: hybrid -, float64 +); not used.
- Called **k_c 87 roots (macOS build)**: numerical evidence, not yet physical.

Beside (information, not a pass rule), by position, k_c 87 (D 19.375 and D 19.75 mine; D 19.5 is dh610's posted 1.399169, not rechecked here):

| D | root near the line | second root | second root minus root near the line |
|---|---|---|---|
| 19.375 | 1.434463 | 1.370705 | -0.063758 |
| 19.5 | 1.399169 | not read (window 1.36 to 1.44, nothing below 1.36) | |
| 19.75 | 1.338993 | 1.276162 | -0.062831 |

The root near the line falls -0.28235 per unit D from D 19.375 to 19.5 and -0.24070 from 19.5 to 19.75 (-0.2546 over the whole step); the second root falls 0.094543 over 0.375 in D (-0.2521 per unit D). The gap changes by +0.000927. Both stay below the line: the second root has not come up to the line at D 19.75 in this window.
What the scan does not say: whether the second root is the same root across D (the coordinator's identification) and where it is at D 19.5; the window ends at 1.26 and 1.40 and nothing is said outside it.
My predictions: source and regrid accepted: yes (3124 steps, I said about 3125; 19.7 min, I said about 17); one change (40%) or two (40%): two; a change within 0.02 of 1.3286 (70%): yes (0.0104); two changes within 0.05 of each other (25%): no (0.0628 apart); the scan about 55 min (45 to 70): 56.8 min; each process 2.8 to 4.4 GB: peak 2.63 to 4.27 GB; the four together near 11 GB: 11.27 GB. Missed: the regrid's rss (2.7 GB said; 3.58 GB).
Resources (`scan/scan_samples.csv`, 57 rounds of 60 s, log only): rss per process peak 2.63 to 4.27 GB (median of all live samples 2.03 GB), the four together peak 11.27 GB (00:29:38; median 8.34 GB); available memory 10.0 to 16.7 GiB; free memory by `memory_pressure` 82 to 87%; disk 25 GiB free throughout. The watcher posted no alert (it is alert-only since the coordinator's correction of about 00:50 UTC).
