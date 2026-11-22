# I1025-macm3/kc79_d19375: win2's k_c 71 D 19.375 state regridded to k_c 79 on macm3's own build, then a hybrid sign scan (lambda 1.34 to 1.52)

Written before the run, 2026-11-22 20:15 UTC. Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025.
Coordinator t5 (hc, 2026-11-22 about 20:10 UTC). Same three steps, same drivers and same code as `../kc79_d1925/` (README there), with the D, the source, lambda_0 and the window changed.

## Order

Why: k_c 79's line near lambda_1 (1.539658, 1.505784, 1.469975 at D 19, 19.125, 19.25) predicts about 1.434 at D 19.375, and k_c 71 at D 19.5 has two roots straddling the line (1.371531 and 1.449187; win2, raw 8ca6c3ed):
the window shows whether k_c 79 has one root near the line or a pair at D 19.375. Roots are read by position, never by sign orientation, across D as well as across k_c.

1. **Source:** win2's k_c 71 D 19.375 state (raw `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D19.375000.npy`, blob e883864a) with its line in `states/l1kc71Lw1025b.jsonl` (the blob of the file as of raw 1845c479, 9659eac3, one line;
   the D 19.375 line of the file at raw origin/main 8ca6c3ed (6 lines, blob 36cb46bd) is identical, checked). `kc71_syscheck.py` first, with its two controls.
2. **Regrid** to k_c 79 with `ell_refine.py` as dh370 did at D 19.125 and as `../kc79_d1925/` did at D 19.25 (lambda_0 from `ell_delta.lam0_at(19.375)`, `--no-gamma`), accepted only by `kc79_syscheck_1025.py` and its two controls. 6 threads, nice 10, own session.
3. **Scan** the accepted state with `d18_hybsign.py` (unmodified): lambda 1.34 to 1.52 at 0.01 (19 values) plus a repeat of 1.43, 4 processes of 1 thread, nice 10, own session under caffeinate; read with `read_lower.py` with its selftest and mutations.
Stop and report on any failure; change no code. Post on #1025; send each step's verdict with the raw commit.

## Inputs (pinned by `git hash-object --no-filters`; `prepare_inputs.sh` copies them with `git cat-file blob` into `in/`; `run_regrid.sh` and `run_scan.sh` check `in/` again)

```
e883864a  sol_l1kc71Lw1025b_D19.375000.npy  <- 1845c479:I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D19.375000.npy  ok
9659eac3  l1kc71Lw1025b.jsonl  <- 1845c479:I1025-win2/kc71_leap/states/l1kc71Lw1025b.jsonl  ok
4cd86cd4  kc71_syscheck.py  <- 8e4797ff:I1025-win2/kc71_d185/kc71_syscheck.py  ok
29dce7ea  kc79_syscheck_1025.py  <- 8e4797ff:I1025-win/kc79_d19/kc79_syscheck_1025.py  ok
e089207a  d18_hybsign.py  <- 8e4797ff:I1025-dh170/kc_break/d18_hybsign.py  ok
89309d3c  read_lower.py  <- 8e4797ff:I1025-dh170/lower_root/read_lower.py  ok
7c9d400f  d185_scan_read.py  <- 8e4797ff:I1025-mac/d18/d185_scan_read.py  ok
```

The D 19.375 record line: k_c 71, kappa 0.7, u0 0.04, Ks 30, |F| 3.229240472819225e-10, 2609 steps, constraint 2.217e-3, Delta 1.0767972283874574 (win2's leg 2, 2503 s, h 0.0625).
Code, build and venv as `../kc79_d1925/README.md`: worktree `~/Source/choptuik-large-d-1025m` at 505d8399, `venv-macm3-1058b` (Python 3.14.3, multidouble 5.1.0, hpkernel neon), `P4_WT_MATTER=<worktree>/solver/matter`; `ell_refine.py` blob 631e5801 = dh370's.
lambda_0: `ell_delta.lam0_at(19.375)` = **2.1138515550** (the same function that gave winb's 2.1156378446 at D 19, dh370's 2.1150338480 at D 19.125, 2.1132623525 at D 19.5 and 2.1144367878 at D 19.25).

## Commands

Regrid (`run_regrid.sh`; the source tag is win2's leg-2 tag `l1kc71Lw1025b`, the state is copied into the worktree's `solver/matter/data/` as `sol_l1kc71Lw1025b_D19.3750.npy`, the name `ell_refine.py` reads, and checked by blob):

    cd ~/Source/choptuik-large-d-1025m/solver/matter && nice -n 10 python -u capped_run.py 21600 python -u ell_refine.py l1kc71Lw1025b 71 l1kc79macm3d19375 79 1 19.375 2.1138515550 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma        (6 threads by env, own session, caffeinate -is)

(as dh370's D 19.5 command, `ell_refine.py l1kc71Lw1025b 71 l1kc79dh370d195 79 1 19.5 2.1132623525 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, with the D, the tag and lambda_0 changed; `timeout` -> `capped_run.py`, as before.)
`run_regrid.sh` runs, stopping at the first failure (`VERDICT.txt`, `steps.txt`): the pins, the worktree check, the two selftests, the source check with its two controls, the regrid, the result check with its two controls.

Scan (`run_scan.sh`): `d18_hybsign.py STUB STATE 19.375 "<lambdas>" OUT` in 4 processes: p0 1.34,1.38,1.42,1.46,1.50; p1 1.35,1.39,1.43,1.47,1.51; p2 1.36,1.40,1.44,1.48,1.52; p3 1.37,1.41,1.45,1.49 and the repeat 1.43 (so the repeat runs on another process than the first 1.43).
Free memory is checked first (need 4 x 1.3 GB, at least 8 GiB available). Then `read_lower.py selftest`, its mutations `shift` and `round2` (each must exit 1), and `read_lower.py scan 1.34 1.52`.
Own session: `launch_1070.py` (double fork, `setsid`) running `caffeinate -is /bin/bash run_*.sh`; `session_check_*.txt` after each start.

## Acceptance (fixed before the run; as `../kc79_d1925/`)

1. **Source.** `kc71_syscheck.py` accepts the k_c 71 D 19.375 state and record on this machine (record |F| at most 1e-9, `freeze_from` gives the record's 2609 steps, |F| within 1%), its selftest exits 0, both controls (`--mutate=F`, `--mutate=steps`) exit 1. Otherwise no regrid.
2. **Result.** `kc79_syscheck_1025.py` accepts the regridded record and state (k_c 79 at D 19.375, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), its selftest exits 0, both controls exit 1. A regrid that exits non-zero or hits the cap is a stop.
3. **Scan.** Only after ACCEPTED. Every process prints `the record system` first; anything else is a stop. The reader's selftest passes and its two mutations exit 1; the repeat of 1.43 agrees.

## Reading (fixed before the run; roots by position)

Every robust change by its position (bracket, det-linear estimate, estimator range; orientation is printed but not used to identify a root); the edge signs; every ln|det| minimum without a change; the repeat; the float64 sign beside the hybrid (information); each point's noise-robustness.
Called k_c 79 roots (macOS build). Positions are compared with the line's prediction and with k_c 71's roots (below) by distance, never by orientation. The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step.

## Prediction beside the scan (information, not a pass rule)

k_c 79's root near lambda_1's line: 1.539658 (D 19, winb), 1.505784 (D 19.125, dh370), 1.469975 (D 19.25, macm3b; raw cc30e59c). Successive differences -0.033874 and -0.035809 per 0.125 in D. Continuing the last difference gives 1.4342 at D 19.375 (the coordinator's "about 1.434");
continuing the second difference gives 1.4322. k_c 71 at D 19.5 (win2, raw 8ca6c3ed): two roots, 1.371531 and 1.449187, both within 0.052 of k_c 79's line at D 19.5 (predicted 1.398 to 1.404); at D 19.25 it has one root near the line (1.4750, dh610) and the rising root (1.296, 1.488, about 1.58, 1.661 at D 19, 19.125, 19.1875, 19.25), which is above this window.
win2's k_c 71 scan at D 19.375 (window 1.30 to 1.60) runs now; dh370 and dh610 scan k_c 79 at D 19.5.

My own predictions (written before any run): source check passes with 2609 steps and both controls exit 1 (95%); the regrid is accepted (85%) with about 2900 steps (2925 at D 19.25 against the k_c 71 record's 2630: x1.112 of 2609 is 2902), taking about 10 min (the D 19.25 regrid: 581 s);
the scan takes about 55 min (5 points a process at about 650 s); the scan shows one root in 1.42 to 1.44 near the line (55%), two roots in the window (25%), no root (10%), another count (10%).

## Status (22 Nov 2026)

| step | verdict | numbers | time (UTC) |
|---|---|---|---|
| source check (win2's `kc71_syscheck.py`) | accepted; selftests exit 0; controls `--mutate=F` and `--mutate=steps` exit 1 | state \|F\| 3.2279802889e-10 against the record's 3.2292404728e-10 (0.04% apart, bar 1%); `freeze_from` 2609 steps = the record's | 20:15 (2 s) |
| regrid (`ell_refine.py`, exit 0), child pid 41987, own session (`session_check_regrid.txt`: every chain ends at launchd, no claude, tty ??) | **accepted** by `kc79_syscheck_1025.py` (selftest exit 0); controls `--mutate=F` and `--mutate=steps` exit 1 | |F| 3.2694e-10, 2903 steps (freeze_from 2903 = the record's), constraint 1.107e-03, Delta 1.0767941558 (k_c 71: 1.0767972284; difference -3.073e-06); capped_run wall 671 s, the record's 662 s; 1 core (ps %cpu 100 of 600 allowed), rss max 2.83 GB (11 samples of 60 s); 18 RuntimeWarning lines of `dss_ell.py` | 20:15 to 20:27 (722 s with the checks) |
| scan (`run_scan.sh`), 4 processes of 1 thread, all exit 0, each printed `the record system` | done, 20 evaluations (19 values and the repeat of 1.43); reader selftest exit 0, mutations `shift` and `round2` exit 1 | **two robust changes**: + to - in (1.430, 1.440), det-linear 1.431552, range [1.431039, 1.431552]; - to + in (1.460, 1.470), det-linear 1.469771, range [1.469771, 1.469819]; edge signs + at 1.34 and + at 1.52; repeat of 1.43 bit-identical | 20:27:48 to 21:26:07 (58.3 min; 622 to 747 s per point) |

### Scan result (22 Nov 2026, scan 20:27:48 to 21:26:07 UTC, 58.3 min)

All four processes exit 0 and each printed `the record system` (|F| 3.2694081469e-10, 2903 steps = the record's). 20 evaluations (19 values and the repeat of 1.43), each 622 to 747 s (mean 694 s; the first eight points 622 to 641 s, the later twelve 718 to 747 s) beside the other three processes.
Reader `read_lower.py` (89309d3c, unedited): selftest exit 0, mutations `shift` and `round2` each exit 1 (`selftest_read_lower*.txt`); reading in `read_lower.txt`.

| lambda | process | hybrid sign | ln\|det\| | noise-robust | float64 sign | seconds |
|---|---|---|---|---|---|---|
| 1.34 | p0 | + | -2520.153598 | yes | + | 632 |
| 1.35 | p1 | + | -2520.167524 | yes | + | 641 |
| 1.36 | p2 | + | -2520.342583 | yes | + | 641 |
| 1.37 | p3 | + | -2520.617386 | yes | + | 640 |
| 1.38 | p0 | + | -2520.971810 | yes | + | 622 |
| 1.39 | p1 | + | -2521.404391 | yes | + | 629 |
| 1.40 | p2 | + | -2521.930505 | yes | + | 633 |
| 1.41 | p3 | + | -2522.596198 | yes | - | 633 |
| 1.42 | p0 | + | -2523.549418 | yes | - | 730 |
| 1.43 | p1 | + | -2526.226082 | yes | + | 741 |
| 1.43 (repeat) | p3 | + | -2526.226082 | yes | + | 720 |
| 1.44 | p2 | - | -2524.531701 | yes | - | 745 |
| 1.45 | p3 | - | -2524.306936 | yes | + | 741 |
| 1.46 | p0 | - | -2524.697160 | yes | + | 733 |
| 1.47 | p1 | + | -2528.450591 | yes | + | 747 |
| 1.48 | p2 | + | -2524.334183 | yes | + | 747 |
| 1.49 | p3 | + | -2523.553692 | yes | + | 746 |
| 1.50 | p0 | + | -2523.077272 | yes | + | 723 |
| 1.51 | p1 | + | -2522.732337 | yes | + | 723 |
| 1.52 | p2 | + | -2522.461798 | yes | + | 718 |

- **Two robust changes, called by position.**
  The root near lambda_1's line: + to - as printed in (1.430, 1.440), det-linear 1.431552, estimator range [1.431039, 1.431552].
  The second root, 0.038219 above it: - to + as printed in (1.460, 1.470), det-linear 1.469771, estimator range [1.469771, 1.469819].
  The range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. Orientation is printed, not used to identify a root and not compared across D.
- Edge signs: + at 1.34, + at 1.52 (at D 19.25: + at 1.42, - at 1.52; nothing is drawn from the orientation). All 20 evaluations are noise-robust; no change touches a non-robust point. ln|det| minima without a sign change: none (the dips at 1.43, -2526.226, and at 1.47, -2528.451, sit beside the two changes).
- Repeat of 1.43 (process 3 against process 1): sign, noise signs, float64 sign and ln|det| (-2526.226081788902) bit-identical: yes.
- The float64 sign differs from the hybrid at 4 points (1.41 and 1.42: hybrid +, float64 -; 1.45 and 1.46: hybrid -, float64 +); not used.
- Called **k_c 79 roots (macOS build)**: numerical evidence, not yet physical.

Beside (information, not a pass rule), by position:

| quantity | value |
|---|---|
| line's prediction at D 19.375, last difference | 1.434166 (the root near the line is -0.002614 from it) |
| line's prediction, second difference | 1.432231 (the root near the line is -0.000679 from it) |
| k_c 79 root near the line at D 19, 19.125, 19.25, 19.375 | 1.539658, 1.505784, 1.469975, 1.431552 |
| differences per 0.125 in D | -0.033874, -0.035809, -0.038423 (second differences -0.001935, -0.002614) |
| second root at D 19.375 against the D 19.25 root (1.469975) | -0.000204 |
| spacing of the two roots at D 19.375 | 0.038219 (k_c 71 at D 19.5, win2, a different D: 0.077656 between 1.371531 and 1.449187) |

This scan does not say which of the two k_c 79 roots at D 19.375 continues the D 19.25 root (the second root is 0.000204 from it; the root near the line is on the line's extrapolation to 0.0007 to 0.0026); that needs a D between 19.25 and 19.375, or a window below 1.34 and above 1.52 at D 19.375. The window ends at 1.34 and 1.52: nothing is said outside it.
My predictions: source accepted with 2609 steps and both controls: yes; the regrid accepted: yes, with 2903 steps (I said about 2900) in 671 s (about 10 min: yes); the scan about 55 min: 58.3 min; the scan's count: missed (I gave one root near the line 55%, two roots 25%; the scan has two).
Resources: the scan processes were not sampled (the regrid's samples: 1 core, rss max 2.83 GB); available memory 16.0 GiB before the scan, 86% free by `memory_pressure` after it.
