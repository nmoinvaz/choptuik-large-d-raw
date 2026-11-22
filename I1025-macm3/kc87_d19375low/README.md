# I1025-macm3/kc87_d19375low: the k_c 87 D 19.375 state of ../kc87_d19375/ scanned below lambda_1's line, lambda 1.28 to 1.40

Written before the run, 2026-11-22 22:44 UTC. Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025.
Coordinator t5 (hc, 2026-11-22 about 22:45 UTC). The same state and record as `../kc87_d19375/` (raw f7862ac2: `sol_l1kc87macm3d19375_D19.3750.npy` blob 448970da, `l1kc87macm3d19375.jsonl` blob f399e0f2), scanned in a window below the one read there. Step 3 of `../kc87_d19375/` only: no regrid.

## Order

Why: `../kc87_d19375/` (1.40 to 1.50) found one robust change at k_c 87, D 19.375: the root near lambda_1's line, det-linear 1.434463 (k_c 79: 1.431552, k_c 71: 1.437773), and no root near 1.4698 (k_c 79's second root; k_c 71's is 1.543839): that root moves with k_c.
The coordinator's prediction, written before this run: k_c 87's rising root has not crossed lambda_1 by D 19.5 (dh610 saw only lambda_1 in 1.36 to 1.44 there), so at D 19.375 it lies **below** lambda_1; the k_c 71 to 79 shift at D 19.125 (1.488 to 1.400, about -0.088) put on k_c 79's 1.4698 gives about 1.38 (an extrapolation, not a pass rule).
The k_c 71 to 79 step at D 19.375 (1.543839 to 1.469771, -0.074068) put on 1.469771 gives 1.395703 (my own second extrapolation, from numbers already posted; both are in the window).

Scan the same state, lambda 1.28 to 1.40 at 0.01 (13 values) plus a repeat of 1.34, 4 processes of 1 thread, nice 10, own session under caffeinate; read with `read_lower.py` with its selftest and mutations.
Report every robust change by position and whether one sits in 1.33 to 1.40. Stop and report if available memory falls under 2 GiB (the earlier scan's four processes peaked at 11.2 GB against 17.4 GiB available). Post on #1025; send the verdict with the raw commit. Stop and report on any failure; change no code.

## Inputs (pinned by `git hash-object --no-filters`; `prepare_inputs.sh` copies them with `git cat-file blob` into `in/`; `run_scan.sh` checks `in/` and the worktree's copies again)

```
448970da  sol_l1kc87macm3d19375_D19.3750.npy  <- f7862ac2:I1025-macm3/kc87_d19375/sol_l1kc87macm3d19375_D19.3750.npy  ok
f399e0f2  l1kc87macm3d19375.jsonl  <- f7862ac2:I1025-macm3/kc87_d19375/l1kc87macm3d19375.jsonl  ok
6df5d960  kc87_syscheck_1025.py  <- ec9fb489:I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py  ok
e089207a  d18_hybsign.py  <- 8e4797ff:I1025-dh170/kc_break/d18_hybsign.py  ok
89309d3c  read_lower.py  <- 8e4797ff:I1025-dh170/lower_root/read_lower.py  ok
7c9d400f  d185_scan_read.py  <- 8e4797ff:I1025-mac/d18/d185_scan_read.py  ok
```

The record: k_c 87, D 19.375, |F| 3.290884534691364e-10, 3195 steps, constraint 6.308e-04, Delta 1.0767926055 (my regrid of my k_c 79 state, `../kc87_d19375/`).
Code, build and venv as `../kc79_d19375/README.md` and `../kc87_d19375/README.md`: worktree `~/Source/choptuik-large-d-1025m` at 505d8399, `venv-macm3-1058b` (Python 3.14.3, multidouble 5.1.0, hpkernel neon), `P4_WT_MATTER=<worktree>/solver/matter`.

## Commands

`run_scan.sh` (own session: `launch_1070.py`, double fork and `setsid`, running `caffeinate -is /bin/bash run_scan.sh`; `session_check_scan.txt` after the start):
1. the pins, the worktree check, and `kc87_syscheck_1025.py` on the state again (selftest exit 0, state check exit 0, `--mutate=F` and `--mutate=steps` exit 1); then at least 12 GiB available (vm_stat: free + inactive + speculative + purgeable);
2. `d18_hybsign.py STUB STATE 19.375 "<lambdas>" OUT` in 4 processes, each under `capped_run.py 28800` by exact pid: p0 1.28,1.32,1.36,1.40; p1 1.29,1.33,1.37 and the repeat 1.34; p2 1.30,1.34,1.38; p3 1.31,1.35,1.39 (the repeat of 1.34 runs on another process than the first 1.34);
3. a sampler (log only, never stops or kills anything) writes rss, cpu, available GiB, free memory percent and free disk every 60 s into `scan/scan_samples.csv`;
4. `read_lower.py selftest`, its mutations `shift` and `round2` (each must exit 1), and `read_lower.py scan 1.28 1.40`; the point 1.40 was also evaluated in `../kc87_d19375/`, and `cross_run_1.40.txt` compares the two (information).
My watcher is alert-only (it ends and tells me when available memory is under 2 GiB or free disk under 3 GiB); the stop on the coordinator's 2 GiB rule is mine, by exact pid.

## Acceptance (fixed before the run)

Every process prints `the record system` first (|F| 3.2908845347e-10, 3195 steps); anything else is a stop. The reader's selftest passes and its two mutations exit 1; the repeat of 1.34 agrees (sign, noise signs, float64 sign, ln|det| within 1e-6).

## Reading (fixed before the run; roots by position)

Every robust change by its position (bracket, det-linear estimate, estimator range; orientation is printed but not used to identify a root); the edge signs; every ln|det| minimum without a change; the repeat; the float64 sign beside the hybrid (information); each point's noise-robustness.
A change "sits in 1.33 to 1.40" if its det-linear estimate lies in [1.33, 1.40] (the bracket is also stated). Called k_c 87 roots (macOS build). Positions are compared with 1.434463 (the root near the line at k_c 87), with the two extrapolations above (1.382 and 1.396) and with k_c 79's 1.469771 by distance, never by orientation.
The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. The window ends at 1.28 and 1.40: nothing is said outside it.

## Predictions (information, not a pass rule; written before any run)

Robust changes in 1.28 to 1.40: none (25%), one (50%), two (20%), more (5%). A change sitting in 1.33 to 1.40 (the coordinator's question): 60%. Its position within 0.02 of 1.382 or of 1.396: 40%.
Scan time: p0 and p1 have four points of about 950 to 1000 s (the k_c 87 scan above: 913 to 1004 s per point, mean 959 s), so about 65 min (55 to 80); p2 and p3 finish about 16 min earlier. Memory: each process 2.8 to 3.6 GB as sampled before, the four together peaking near 11 GB.

## Status (22 Nov 2026)

| step | verdict | numbers | time (UTC) |
|---|---|---|---|
| pins and `kc87_syscheck_1025.py` on the state | not started | | |
| scan | not started | | |
