# I1025-macm3/kc87_d19375: my accepted k_c 79 D 19.375 state regridded to k_c 87 on macm3's own build, then a hybrid sign scan (lambda 1.40 to 1.50)

Written before the run, 2026-11-22 21:32 UTC. Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025.
Coordinator t5 (hc, 2026-11-22 about 21:30 UTC). The same three steps as `../kc79_d19375/` (README there), one k_c up: source, regrid, scan, with dh610's k_c 87 check in place of the k_c 79 check.

## Order

Why: at D 19.375 k_c 79 has two roots in 1.34 to 1.52 (`../kc79_d19375/`, raw 98796643): the root near lambda_1's line at 1.431552 (bracket (1.43, 1.44), range [1.431039, 1.431552]) and a second root at 1.469771 (bracket (1.46, 1.47), range [1.469771, 1.469819]).
The coordinator's reading, by position: k_c 79's root near the line goes 1.4700 (D 19.25), 1.4316 (D 19.375), 1.3976 (D 19.5), smooth; the second root, 1.4698, is absent at D 19.25 in 1.42 to 1.52 and at D 19.5 in 1.30 to 1.50, which fits k_c 79's rising root crossing lambda_1 near D 19.3 (k_c 63 near D 19.0 to 19.1, k_c 71 near D 19.15).
The test is k_c 87 at D 19.375: report whether a root sits near 1.4316 and whether one sits near 1.4698. Roots are read by position, never by sign orientation, across D as well as across k_c.

1. **Source:** my accepted k_c 79 D 19.375 state and record (raw `I1025-macm3/kc79_d19375/`, `sol_l1kc79macm3d19375_D19.3750.npy` blob d5ef91f3 and `l1kc79macm3d19375.jsonl` blob a7c1addb, pinned at raw 98796643). `kc79_syscheck_1025.py` on it first, with its two controls.
2. **Regrid** to k_c 87 with `ell_refine.py` as dh610 did at D 19.5 (raw `I1025-dh610/kc87_d195/`, ec9fb489; lambda_0 from `ell_delta.lam0_at(19.375)`, `--no-gamma`). Accept the k_c 87 state only by dh610's `kc87_syscheck_1025.py` (blob 6df5d960, the k_c 79 check with 3 lines changed) with both controls; the k_c 79 check must refuse it. 6 threads, nice 10, own session.
3. **Scan** the accepted state with `d18_hybsign.py` (unmodified): lambda 1.40 to 1.50 at 0.01 (11 values) plus a repeat of 1.45, 4 processes of 1 thread, nice 10, own session under caffeinate; read with `read_lower.py` with its selftest and mutations.
Stop and report on any failure; change no code. Post on #1025; send each step's verdict with the raw commit.

## Inputs (pinned by `git hash-object --no-filters`; `prepare_inputs.sh` copies them with `git cat-file blob` into `in/`; `run_regrid.sh` and `run_scan.sh` check `in/` again)

```
d5ef91f3  sol_l1kc79macm3d19375_D19.3750.npy  <- 98796643:I1025-macm3/kc79_d19375/sol_l1kc79macm3d19375_D19.3750.npy  ok
a7c1addb  l1kc79macm3d19375.jsonl  <- 98796643:I1025-macm3/kc79_d19375/l1kc79macm3d19375.jsonl  ok
6df5d960  kc87_syscheck_1025.py  <- ec9fb489:I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py  ok
dfb42ff7  kc87_syscheck_1025.diff.dh610  <- ec9fb489:I1025-dh610/kc87_d195/kc87_syscheck_1025.diff  ok
29dce7ea  kc79_syscheck_1025.py  <- 8e4797ff:I1025-win/kc79_d19/kc79_syscheck_1025.py  ok
e089207a  d18_hybsign.py  <- 8e4797ff:I1025-dh170/kc_break/d18_hybsign.py  ok
89309d3c  read_lower.py  <- 8e4797ff:I1025-dh170/lower_root/read_lower.py  ok
7c9d400f  d185_scan_read.py  <- 8e4797ff:I1025-mac/d18/d185_scan_read.py  ok
```

The source record: k_c 79, D 19.375, |F| 3.2694081469e-10, 2903 steps, constraint 1.107e-3, Delta 1.0767941558 (my regrid from win2's k_c 71 state, 671 s).
Code, build and venv as `../kc79_d19375/README.md`: worktree `~/Source/choptuik-large-d-1025m` at 505d8399, `venv-macm3-1058b` (Python 3.14.3, multidouble 5.1.0, hpkernel neon), `P4_WT_MATTER=<worktree>/solver/matter`; `ell_refine.py` blob 631e5801 = dh370's and dh610's.
lambda_0: `ell_delta.lam0_at(19.375, *lam0_table())` = **2.1138515550** (error estimate 5.0e-6; the same function as at the k_c 79 point; at D 19.5 it gives dh610's 2.1132623525, checked here; `ell_delta.py` blob 059180e6 in this worktree, dh610's worktree names fde699f5; `--no-gamma` does not use lambda_0).
The k_c 87 check is `kc79_syscheck_1025.py` with 3 lines changed (the k_c test, its message and the selftest's planted record); `run_regrid.sh` rebuilds the diff, requires 3 changed lines on each side and hunks equal to dh610's (`kc87_diff_rebuilt.txt`).

## Commands

Regrid (`run_regrid.sh`; the source state and its record are copied into the worktree's `solver/matter/data/` under the names `ell_refine.py` reads and checked by blob):

    cd ~/Source/choptuik-large-d-1025m/solver/matter && nice -n 10 python -u capped_run.py 21600 python -u ell_refine.py l1kc79macm3d19375 79 l1kc87macm3d19375 87 1 19.375 2.1138515550 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma        (6 threads by env, own session, caffeinate -is)

dh610's D 19.5 command was `ell_refine.py l1kc79dh370d195 79 l1kc87dh610d195 87 1 19.5 2.1132623525 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma` (8 threads, nice 10, `timeout 21600`, a systemd unit); mine has the D, the tags and lambda_0 changed, `timeout` -> `capped_run.py` and 6 threads by env.
`run_regrid.sh` runs, stopping at the first failure (`VERDICT.txt`, `steps.txt`): the pins, the diff of the two checks, the worktree check, lambda_0, the two selftests, the source check with its two controls and the k_c 87 check's refusal of the k_c 79 source, the regrid, the result check with its two controls and the k_c 79 check's refusal of the result.

Scan (`run_scan.sh`): `d18_hybsign.py STUB STATE 19.375 "<lambdas>" OUT` in 4 processes: p0 1.40,1.44,1.48; p1 1.41,1.45,1.49; p2 1.42,1.46,1.50; p3 1.43,1.47 and the repeat 1.45 (so the repeat runs on another process than the first 1.45).
Free memory is checked first (at least 10 GiB available; the k_c 79 processes used about 1.3 GB each by the estimate I had, never sampled; k_c 87 is sampled this time into `scan/scan_samples.csv`, log only). Then `read_lower.py selftest`, its mutations `shift` and `round2` (each must exit 1), and `read_lower.py scan 1.40 1.50`.
Own session: `launch_1070.py` (double fork, `setsid`) running `caffeinate -is /bin/bash run_*.sh`; `session_check_*.txt` after each start.

## Acceptance (fixed before the run)

1. **Source.** `kc79_syscheck_1025.py` accepts my k_c 79 D 19.375 state and record on this machine (record |F| at most 1e-9, `freeze_from` gives the record's 2903 steps, the state's |F| within 1%), its selftest exits 0, both controls (`--mutate=F`, `--mutate=steps`) exit 1; extra control: `kc87_syscheck_1025.py` on the k_c 79 source exits 1. Otherwise no regrid.
2. **Result.** `kc87_syscheck_1025.py` accepts the regridded record and state (k_c 87 at D 19.375, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), its selftest exits 0, both controls exit 1; extra control: `kc79_syscheck_1025.py` on the k_c 87 result exits 1. A regrid that exits non-zero, hits the cap or cannot be built at k_c 87 is a stop.
3. **Scan.** Only after ACCEPTED. Every process prints `the record system` first; anything else is a stop. The reader's selftest passes and its two mutations exit 1; the repeat of 1.45 agrees.

## Reading (fixed before the run; roots by position)

Every robust change by its position (bracket, det-linear estimate, estimator range; orientation is printed but not used to identify a root); the edge signs; every ln|det| minimum without a change; the repeat; the float64 sign beside the hybrid (information); each point's noise-robustness.
Called k_c 87 roots (macOS build). The coordinator's two questions are answered as: the distance of every robust change to 1.431552 and to 1.469771 (k_c 79's two roots at D 19.375), and which change is nearest to each; "near" is stated with the distance, not by a threshold fixed here
(for scale: at D 19.5 k_c 79's root near the line, 1.397565, is 0.026 above k_c 71's, 1.371531). The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. The window ends at 1.40 and 1.50: nothing is said outside it.

## Predictions (information, not a pass rule; written before any run)

From dh610's and dh370's runs at D 19.5 (3171 steps at k_c 87 from 2879 at k_c 79: x1.1014; 3213 s against 2237 s: x1.436) and my own k_c 79 regrid (2903 steps, 671 s, rss max 2.83 GB, 1 core):
source check passes with 2903 steps and all controls as wanted (95%); the regrid is accepted (80%) with about 3200 steps (2903 x 1.1014 is 3197), taking about 16 min (671 s x 1.436 is 964 s; 12 to 25 min), rss max about 3.3 GB;
the scan takes about 50 min (3 points a process at about 1000 s each, 40 to 70 min; k_c 79 took 622 to 747 s per point beside the other three), each process about 1.6 GB.
Scan: number of robust changes in 1.40 to 1.50: none (10%), one (55%), two (30%), more (5%). A change within 0.03 of 1.431552 (70%); a change within 0.01 of 1.469771 (25%).

## Status (22 Nov 2026)

| step | verdict | numbers | time (UTC) |
|---|---|---|---|
| source check (`kc79_syscheck_1025.py`) | accepted; selftests (kc79 and kc87 checks) exit 0; controls `--mutate=F` and `--mutate=steps` exit 1; extra control: `kc87_syscheck_1025.py` on the k_c 79 source exits 1 ("the record is not k_c 87 at D 19.375 (kc 79, D 19.375)") | state \|F\| 3.2694081469e-10 = the record's; `freeze_from` 2903 steps = the record's | 21:32:47 (3 s) |
| regrid (`ell_refine.py`), child pid 52756, own session (`session_check_regrid.txt`: every chain ends at launchd, no claude, tty ??) | running | | started 21:32:47 |
| scan | not started | | |
