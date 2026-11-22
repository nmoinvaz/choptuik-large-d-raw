# I1025-macm3/kc79_d1925: win2's k_c 71 D 19.25 state regridded to k_c 79 on macm3's own build, then a hybrid sign scan (lambda 1.42 to 1.52)

Written before the run, 2026-11-22 19:17 UTC. Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025.
Coordinator t5 (hc, 2026-11-22 about 19:10 UTC).

## Order

Why: lambda_1 of the l = 1 multiplet is k_c-stable at k_c 79 along a straight line (1.539658 at D 19, winb; 1.505784 at D 19.125, dh370; about -0.271 per unit D), which puts it
near 1.472 at D 19.25; k_c 71 fails there (dh610: one change, + to - at 1.475019). winb's laptop, which was regridding k_c 79 at D 19.25, is unreachable since 18:48 UTC.
This task is that point on this machine's own build (macOS, NEON hpkernel, multidouble 5.1.0).

1. **Source:** win2's k_c 71 D 19.25 state (raw `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.250000.npy`) with its line in `states/l1kc71Lw1025.jsonl` (raw 8e4797ff), both pinned by blob.
   Check it with win2's `kc71_syscheck.py` and its two controls before anything else.
2. **Regrid** to k_c 79 with `ell_refine.py` exactly as dh370 did at D 19.125 (raw `I1025-dh370/kc79_d19125/README.md`, 79b57212: the command, the lambda_0 argument from `ell_delta.lam0_at(D)`, `--no-gamma`),
   accepted only by `kc79_syscheck_1025.py` and its two controls. 6 threads, nice 10, own session.
3. **Scan** the accepted state with `d18_hybsign.py` (unmodified): lambda 1.42 to 1.52 at 0.01 (11 values) plus a repeat of 1.47, 4 processes of 1 thread, nice 10, own session; read with `read_lower.py`
   with its selftest and mutations. Report every robust change with det-linear estimate and range, the edge signs, any ln|det| minimum without a change; call them k_c 79 roots (macOS build).
   Check free memory before the scan (each process about 1.3 GB). Stop and report on any failure; change no code. Push as I go; post on #1025; send each step's verdict with the raw commit.
Estimate (t5): regrid about 1 h, scan about 1.5 to 2 h.

## Inputs (pinned by `git hash-object --no-filters`; `prepare_inputs.sh` copies them with `git cat-file blob` from raw 8e4797ff into `in/` and checks each; `run_regrid.sh` and `run_scan.sh` check `in/` again)

```
36bc6b83  sol_l1kc71Lw1025_D19.250000.npy  <- 8e4797ff:I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.250000.npy  ok
c5fc14a9  l1kc71Lw1025.jsonl  <- 8e4797ff:I1025-win2/kc71_leap/states/l1kc71Lw1025.jsonl  ok
4cd86cd4  kc71_syscheck.py  <- 8e4797ff:I1025-win2/kc71_d185/kc71_syscheck.py  ok
29dce7ea  kc79_syscheck_1025.py  <- 8e4797ff:I1025-win/kc79_d19/kc79_syscheck_1025.py  ok
e089207a  d18_hybsign.py  <- 8e4797ff:I1025-dh170/kc_break/d18_hybsign.py  ok
89309d3c  read_lower.py  <- 8e4797ff:I1025-dh170/lower_root/read_lower.py  ok
7c9d400f  d185_scan_read.py  <- 8e4797ff:I1025-mac/d18/d185_scan_read.py  ok
```

The D 19.25 line of the record (the only one at D 19.25): k_c 71, kappa 0.7, u0 0.04, Ks 30, |F| 3.002396449323892e-10, 2630 steps, constraint 1.990e-3, Delta 1.0737683214116145 (win2's leap step, 2514 s).
The record blob c5fc14a9 (12 lines, to D 19.25) is the one at raw 8e4797ff, as the order says; the raw file has since grown (13 lines, blob a0e21703), its first 12 lines are identical to the pinned blob's (checked).

## Code and build

- Worktree `~/Source/choptuik-large-d-1025m` at 505d8399 (detached, clean). `P4_WT_MATTER=<worktree>/solver/matter`. The imports `dss_ell`, `ell_ddm`, `ell_delta`, `multidouble` succeed, and `ell_refine.py` imports through to its argument parser
  (`-h` exit 0; the module parses its arguments at import, so it cannot be imported bare).
- Python 3.14.3, `venv-macm3-1058b` (hpkernel `.so` sha1 6d8213c28d71, isa neon; multidouble 5.1.0), nice 10, OMP/OPENBLAS/MKL/VECLIB threads 6 for the regrid, 1 for each scan process.
- dh370's D 19.125 run used the worktree 48c36355. Against 505d8399: `ell_refine.py` is the same blob (631e5801), `dss_ell.py` 5d28c19e, `ell_ddm.py` 86578fee, `ell_dd.py` 7e58fcbc and `ddnp.py` 9b1fb195 are the same; only `ell_delta.py`
  differs (fde699f5 against 059180e6, and the data files `ell_lam_*.json`). `lam0_at` reads `solver/data/scan_ne6_lowD_kc39_rk2.jsonl` and `gamma_rust.jsonl`, identical in both commits; both versions give
  lambda_0(19) 2.1156378446 (winb's), lambda_0(19.125) 2.1150338480 (dh370's), lambda_0(19.5) 2.1132623525 (dh370's) and **lambda_0(19.25) = 2.1144367878**. `--no-gamma` does not use the argument.

## Commands

Regrid: dh370's (`cd ~/Source/choptuik-large-d-1025/solver/matter && nice -n 10 timeout 21600 env OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 python -u ell_refine.py l1kc71Lw1025 71 l1kc79dh370 79 1 19.125 2.1150338480 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`)
with the D, the tag and the lambda_0 changed (the source state is copied into the worktree's `solver/matter/data/` as `sol_l1kc71Lw1025_D19.2500.npy`, the name `ell_refine.py` reads, and checked by blob):

    cd ~/Source/choptuik-large-d-1025m/solver/matter && nice -n 10 python -u capped_run.py 21600 python -u ell_refine.py l1kc71Lw1025 71 l1kc79macm3 79 1 19.25 2.1144367878 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma        (6 threads by env, own session, caffeinate -is)

Differences from dh370's command: tag `l1kc79dh370` -> `l1kc79macm3`, D 19.125 -> 19.25, lambda_0 2.1150338480 -> 2.1144367878, and `timeout 21600` -> `capped_run.py 21600` (SIGTERM at the cap by the exact child pid, SIGKILL 60 s later; macOS has no `timeout`).
`run_regrid.sh` runs, in this order, stopping at the first failure (`VERDICT.txt`, `steps.txt`): the pins, the worktree check, the two selftests, the source check with its two controls, the regrid, the result check with its two controls.

Scan: `d18_hybsign.py STUB STATE 19.25 "<lambdas>" OUT` (e089207a, unmodified) in 4 processes (`run_scan.sh`): p0 1.42,1.46,1.50; p1 1.43,1.47,1.51; p2 1.44,1.48,1.52; p3 1.45,1.49 and the repeat 1.47 (so the repeat runs on another
process than the first 1.47). Then `read_lower.py selftest`, its mutations `shift` and `round2` (each must exit 1), and `read_lower.py scan 1.42 1.52`.

Own session: `launch_1070.py` (double fork, `setsid`, parent launchd, no controlling terminal) running `caffeinate -is /bin/bash run_*.sh`; a session check of the pids goes into the folder after the start.

## Acceptance (fixed before the run; winb's two steps)

1. **Source.** `kc71_syscheck.py` accepts the k_c 71 D 19.25 state and record on this machine (the record's |F| at most 1e-9, `freeze_from` gives the record's step count, 2630, |F| within 1% of the record's), its selftest exits 0, and both
   controls (`--mutate=F`, `--mutate=steps`) exit 1. Otherwise no regrid.
2. **Result.** `kc79_syscheck_1025.py` accepts the regridded record and state (k_c 79 at D 19.25, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), its selftest exits 0, and both controls exit 1.
   A regrid that exits non-zero or hits the 21600 s cap is a stop.
3. **Scan.** Starts only after the verdict ACCEPTED. Each scan process first checks the state against its record (`d18_hybsign.py` prints `the record system`); a process that prints anything else is a stop. The reader's selftest passes and
   its two mutations exit 1; the repeat of 1.47 agrees (sign, noise signs, float64 sign, ln|det| within 1e-6, as `read_lower.py` checks).

## Reading (fixed before the run)

Every robust change (bracket, orientation as printed, det-linear estimate, estimator range); the edge signs; every ln|det| minimum without a change; the repeat; the float64 sign beside the hybrid (information); each point's
noise-robustness. Orientation is as printed, not compared across D. The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. Roots are called k_c 79 roots (macOS build).

## Prediction beside the scan (information, not a pass rule)

k_c 79's lambda_1 straight line through 1.539658 at D 19 (winb) and 1.505784 at D 19.125 (dh370): slope -0.270992 per unit D, so 1.4719 at D 19.25 (the order's "near 1.472"). k_c 71 at D 19.25 has + to - at 1.475019 (dh610).
dh370's k_c 79 scan at D 19.125 had one change (- to +) at 1.505784 and none in 1.44 to 1.50 or 1.51 to 1.58.

My own predictions (written before any run): the source check passes with 2630 steps and both controls exit 1 (95%); the regrid exits 0 and is accepted (85%; dh370's D 19.125 regrid took 2576 s on 6 threads with 2949 steps against the
record's 2651 for k_c 71, so about 2930 steps here); the regrid's wall is 0.5 to 1.5 h (70%); the scan shows exactly one robust change in 1.42 to 1.52 (70%), none (15%), two (15%); a single change lies within 0.02 of 1.472 (75% given one);
the scan's points take 25 to 60 min each on 1 thread with 4 processes (65%), the scan 1.5 to 3 h.

## Status (22 Nov 2026)

| step | verdict | numbers | time (UTC) |
|---|---|---|---|
| source check (win2's `kc71_syscheck.py`) | accepted; selftests exit 0; controls `--mutate=F` and `--mutate=steps` exit 1 | state \|F\| 2.9977946350e-10 against the record's 3.0023964493e-10 (0.15% apart, bar 1%); `freeze_from` 2630 steps = the record's | 19:18 (1 s) |
| regrid (`ell_refine.py`, exit 0), child pid 31141, own session (`session_check_regrid.txt`: every chain ends at launchd, no claude, tty ??) | **accepted** by `kc79_syscheck_1025.py` (selftest exit 0); controls `--mutate=F` and `--mutate=steps` exit 1 | |F| 3.0661e-10, 2925 steps (freeze_from 2925 = the record's), constraint 9.574e-04, Delta 1.0737660558 (k_c 71: 1.0737683214; difference -2.266e-06); capped_run wall 581 s, the record's 578 s; 1 core (ps %cpu 100 of 600 allowed), rss max 2.33 GB (9 samples of 60 s); 23 RuntimeWarnings of `dss_ell.py` (dh370's D 19.125 log: 24 of the same lines) | 19:18 to 19:28 (601 s with the checks) |
| scan (`run_scan.sh`), 4 processes of 1 thread, all exit 0, each printed `the record system` | done, 12 evaluations; reader selftest exit 0, mutations `shift` and `round2` exit 1 | one robust change, + to - in (1.46, 1.47), det-linear 1.469975, range [1.469970, 1.469975]; no other; edge signs + at 1.42, - at 1.52; repeat of 1.47 bit-identical | 19:28:57 to 20:01:15 (600 to 661 s per point) |

### Scan result (22 Nov 2026, scan 19:28:57 to 20:01:15 UTC, 32.3 min)

All four processes exit 0 and each printed `the record system` (|F| 3.0660787498e-10, 2925 steps = the record's). 12 evaluations (11 values and the repeat of 1.47), each 600 to 661 s (mean 639 s) beside the other three processes.
Reader `read_lower.py` (89309d3c, unedited): selftest exit 0, mutations `shift` and `round2` each exit 1 (`selftest_read_lower*.txt`); reading in `read_lower.txt`.

| lambda | process | hybrid sign | ln\|det\| | noise-robust | float64 sign | seconds |
|---|---|---|---|---|---|---|
| 1.42 | p0 | + | -2520.621180 | yes | + | 600 |
| 1.43 | p1 | + | -2520.996459 | yes | + | 605 |
| 1.44 | p2 | + | -2521.433684 | yes | + | 607 |
| 1.45 | p3 | + | -2521.985804 | yes | + | 608 |
| 1.46 | p0 | + | -2522.823344 | yes | + | 647 |
| 1.47 | p1 | - | -2528.805069 | yes | + | 654 |
| 1.47 (repeat) | p3 | - | -2528.805069 | yes | + | 656 |
| 1.48 | p2 | - | -2523.091130 | yes | + | 654 |
| 1.49 | p3 | - | -2522.530382 | yes | + | 655 |
| 1.50 | p0 | - | -2522.252161 | yes | + | 656 |
| 1.51 | p1 | - | -2522.087142 | yes | + | 661 |
| 1.52 | p2 | - | -2521.982283 | yes | + | 660 |

- **One robust change, + to - as printed, in (1.460, 1.470), det-linear 1.469975, estimator range [1.469970, 1.469975].** The range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. Orientation is as printed, not compared across D.
- Edge signs: + at 1.42, - at 1.52. All 12 evaluations are noise-robust. ln|det| minima without a sign change: none (ln|det| is -2522.823 at 1.46, -2528.805 at 1.47, -2523.091 at 1.48: the dip at 1.47 sits beside the change).
- Repeat of 1.47 (process 3 against process 1): sign, noise signs, float64 sign and ln|det| (-2528.8050685050607) bit-identical: yes.
- The float64 sign is + at every point and differs from the hybrid at 1.47 to 1.52 (6 points); not used.
- Called a **k_c 79 root (macOS build)**: numerical evidence, not yet physical.

Beside (information, not a pass rule): the line's prediction was 1.4719; the change is at 1.469975, -0.001935 from it (k_c 79 through 1.539658 at D 19, 1.505784 at D 19.125, 1.469975 at D 19.25: successive differences -0.033874 and -0.035809 per 0.125 in D, slope -0.2865 per unit D against the line's -0.2710).
k_c 71 at D 19.25 (dh610): + to - at 1.475019 (range [1.474292, 1.475019]); k_c 79 is -0.005044 from it. At D 19.125 the k_c 79 change (- to + at 1.505784) was 0.005425 below k_c 71's - to + change (1.511209). Whether these are the same roots across D and k_c is not known from these points.
My predictions: one robust change in 1.42 to 1.52 (70%): yes; within 0.02 of 1.472 (75% given one): yes (0.0019); source and regrid accepted: yes; the regrid's steps about 2930: 2925; the regrid's wall 0.5 to 1.5 h: missed (10 min); a scan point 25 to 60 min: missed (10 to 11 min), the scan 1.5 to 3 h: missed (32 min).
Resources: the scan processes were not sampled (the regrid's samples: 1 core, rss max 2.33 GB); available memory before the scan 12.0 GiB.
