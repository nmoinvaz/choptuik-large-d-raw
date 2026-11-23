# I1025-macm3/kc87_d195: dh370's k_c 79 D 19.5 state regridded to k_c 87 on macm3's own build, then a hybrid sign scan (lambda 1.28 to 1.42), beside dh610's Linux regrid and scan

Written before the run, 2026-11-23 00:57 UTC. Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025.
Coordinator t5 (hc, 2026-11-23 about 00:55 UTC). The same three steps as `../kc87_d19375/` and `../kc87_d1975/` (READMEs there), at D 19.5, on the source dh610 used.

## Order

Why (the coordinator's, as information): dh610's k_c 87 at D 19.5 (a Linux regrid of dh370's k_c 79 state; raw `I1025-dh610/kc87_d195/`) has lambda_1 at 1.399169 (bracket (1.39, 1.40), range [1.398747, 1.399169]; window 1.36 to 1.44, one robust change). The second root ran parallel to it at -0.0638 (D 19.375) and -0.0628 (D 19.75) on this machine, so at D 19.5 it would sit near 1.336 (1.399169 - 0.063).
Whether that second root is k_c-stable is the question; k_c 79's side: dh370 and dh610 found one change (1.397565) and nothing else in 1.30 to 1.50 at D 19.5; dh170's k_c 79 scan at D 19.75 (1.27 to 1.38) is running (the coordinator expects it at about 02:48 UTC).
Report every robust change by position, and lambda_1 beside dh610's (a build difference shows there). Roots are read by position, never by sign orientation; in posts "the root near lambda_1's line" and "the second root".

1. **Source:** dh370's accepted k_c 79 D 19.5 state and record (raw `I1025-dh370/kc79_d195/`, `sol_l1kc79dh370d195_D19.5000.npy` blob 9528b355 and `l1kc79dh370d195.jsonl` blob 5777d2a2, pinned at raw f40a4556). `kc79_syscheck_1025.py` on it first, with its two controls.
2. **Regrid** to k_c 87 with `ell_refine.py` as at D 19.375 and D 19.75 and as dh610 did at D 19.5 (lambda_0 from `ell_delta.lam0_at(19.5)`, `--no-gamma`). Accept the k_c 87 state only by dh610's `kc87_syscheck_1025.py` (blob 6df5d960) with both controls; the k_c 79 check must refuse it. 6 threads, nice 10, own session.
3. **Scan** the accepted state with `d18_hybsign.py` (unmodified): lambda 1.28 to 1.42 at 0.01 (15 values) plus a repeat of 1.35, 4 processes of 1 thread, nice 10, own session under caffeinate; read with `read_lower.py` with its selftest and mutations.
Stop and report on any failure; change no code. Memory (the coordinator's correction of 2026-11-22, Nathan's rule of 2026-11-08): alerts only. My watcher posts the free memory to the coordinator by hc when available memory is under 2 GiB, free memory under 8% or free disk under 3 GiB, and never stops, kills or signals a process; the only refusal is to start the scan with less than 12 GiB available. Post on #1025; send each step's verdict with the raw commit.

## Inputs (pinned by `git hash-object --no-filters`; `prepare_inputs.sh` copies them with `git cat-file blob` into `in/`; `run_regrid.sh` and `run_scan.sh` check `in/` again)

The `ref_dh610_*` files are dh610's regrid result and scan at raw 94e9ebc6, for comparison only; the run does not use them.

```
9528b355  sol_l1kc79dh370d195_D19.5000.npy  <- f40a4556:I1025-dh370/kc79_d195/sol_l1kc79dh370d195_D19.5000.npy  ok
5777d2a2  l1kc79dh370d195.jsonl  <- f40a4556:I1025-dh370/kc79_d195/l1kc79dh370d195.jsonl  ok
6df5d960  kc87_syscheck_1025.py  <- ec9fb489:I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py  ok
dfb42ff7  kc87_syscheck_1025.diff.dh610  <- ec9fb489:I1025-dh610/kc87_d195/kc87_syscheck_1025.diff  ok
29dce7ea  kc79_syscheck_1025.py  <- 8e4797ff:I1025-win/kc79_d19/kc79_syscheck_1025.py  ok
e089207a  d18_hybsign.py  <- 8e4797ff:I1025-dh170/kc_break/d18_hybsign.py  ok
89309d3c  read_lower.py  <- 8e4797ff:I1025-dh170/lower_root/read_lower.py  ok
7c9d400f  d185_scan_read.py  <- 8e4797ff:I1025-mac/d18/d185_scan_read.py  ok
57f8e2d3  ref_dh610_sol_l1kc87dh610d195_D19.5000.npy  <- 94e9ebc6:I1025-dh610/kc87_d195/sol_l1kc87dh610d195_D19.5000.npy  ok
64b8db7c  ref_dh610_l1kc87dh610d195.jsonl  <- 94e9ebc6:I1025-dh610/kc87_d195/l1kc87dh610d195.jsonl  ok
8c37aa4d  ref_dh610_scan_D19.5_1025.jsonl  <- 94e9ebc6:I1025-dh610/kc87_d195/scan/scan_D19.5_1025.jsonl  ok
0669efe7  ref_dh610_read_lower.txt  <- 94e9ebc6:I1025-dh610/kc87_d195/read_lower.txt  ok
```

The source record (dh370, k_c 79 at D 19.5, from win2's k_c 71 D 19.5 state): |F| 3.5122938292373126e-10, 2879 steps, constraint 1.2726e-3, Delta 1.0798406632 (dh370's regrid 2237 s on 6 threads). dh610's k_c 87 record: |F| 3.5228509267e-10, F_start 5.096e-06, 3171 steps, constraint 7.311e-04, Delta 1.0798374906, 3213 s on 8 threads, rss 2.27 GB (Fedora 45, i7-12700, multidouble avx2).
Code, build and venv as `../kc87_d19375/README.md`: worktree `~/Source/choptuik-large-d-1025m` at 505d8399, `venv-macm3-1058b` (Python 3.14.3, multidouble 5.1.0, hpkernel neon), `P4_WT_MATTER=<worktree>/solver/matter`; `ell_refine.py` blob 631e5801. dh610's build: `venv-i1058` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble avx2), worktree `~/Source/choptuik-large-d-1025g` at 48c36355 whose `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's (his README). The two builds therefore differ in the platform (Linux x86 against macOS arm64), the SIMD kernels (avx2 against neon), the Python and library versions and the thread count; the solver code is the same.
lambda_0: `ell_delta.lam0_at(19.5, *lam0_table())` = **2.1132623525** (error estimate 6.2e-7, dh610's value; `--no-gamma` does not use it).

## Commands

Regrid (`run_regrid.sh`; the source state and its record are copied into the worktree's `solver/matter/data/` under the names `ell_refine.py` reads and checked by blob):

    cd ~/Source/choptuik-large-d-1025m/solver/matter && nice -n 10 python -u capped_run.py 21600 python -u ell_refine.py l1kc79dh370d195 79 l1kc87macm3d195 87 1 19.5 2.1132623525 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma        (6 threads by env, own session, caffeinate -is)

dh610's command: `ell_refine.py l1kc79dh370d195 79 l1kc87dh610d195 87 1 19.5 2.1132623525 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma` (8 threads, `timeout 21600`, a systemd unit); mine differs in the output tag only, `timeout` -> `capped_run.py`, and 6 threads by env.
`run_regrid.sh` stops at the first failure (`VERDICT.txt`, `steps.txt`): the pins, the diff of the two checks, the worktree check, lambda_0, the two selftests, the source check with its two controls and the k_c 87 check's refusal of the k_c 79 source, the regrid, the result check with its two controls and the k_c 79 check's refusal of the result; then (information) `compare_regrid.py`: this regrid's record fields and state array against dh610's.
Scan (`run_scan.sh`, after ACCEPTED, at least 12 GiB available): `d18_hybsign.py STUB STATE 19.5 "<lambdas>" OUT` in 4 processes, each under `capped_run.py 28800` by exact pid: p0 1.28,1.32,1.36,1.40; p1 1.29,1.33,1.37,1.41; p2 1.30,1.34,1.38 and the repeat 1.35; p3 1.31,1.35,1.39,1.42 (the repeat of 1.35 runs on another process than the first 1.35).
A sampler (log only) writes rss, cpu, available GiB, free memory percent and free disk every 60 s into `scan/scan_samples.csv`. Then `read_lower.py selftest`, its mutations `shift` and `round2` (each must exit 1), `read_lower.py scan 1.28 1.42`, and (information) `compare_scan.py`: my points against dh610's at the lambdas both evaluated (1.36 to 1.42).
Own session: `launch_1070.py` (double fork, `setsid`) running `caffeinate -is /bin/bash run_*.sh`; `session_check_*.txt` after each start.

## Acceptance (fixed before the run)

1. **Source.** `kc79_syscheck_1025.py` accepts dh370's k_c 79 D 19.5 state and record on this machine (record |F| at most 1e-9, `freeze_from` gives the record's 2879 steps, the state's |F| within 1%), its selftest exits 0, both controls (`--mutate=F`, `--mutate=steps`) exit 1; extra control: `kc87_syscheck_1025.py` on the k_c 79 source exits 1. Otherwise no regrid.
2. **Result.** `kc87_syscheck_1025.py` accepts the regridded record and state (k_c 87 at D 19.5, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), its selftest exits 0, both controls exit 1; extra control: `kc79_syscheck_1025.py` on the k_c 87 result exits 1. A regrid that exits non-zero or hits the cap is a stop. The comparison with dh610's regrid is information, not a gate.
3. **Scan.** Only after ACCEPTED. Every process prints `the record system` first; anything else is a stop. The reader's selftest passes and its two mutations exit 1; the repeat of 1.35 agrees (sign, noise signs, float64 sign, ln|det| within 1e-6).

## Reading (fixed before the run; roots by position)

Every robust change by its position (bracket, det-linear estimate, estimator range; orientation is printed but not used to identify a root); the edge signs; every ln|det| minimum without a change (a candidate for two changes closer than the 0.01 step); the repeat; the float64 sign beside the hybrid (information); each point's noise-robustness.
**Beside dh610's:** the root near the line against his 1.399169 (the difference, and whether the brackets agree); at 1.36 to 1.42 each point's hybrid sign and ln|det| against his (`compare_dh610_scan.txt`); the regrid's record and state against his (`compare_dh610_regrid.txt`). A difference between the two machines is reported as a build difference only if the source and the commands are the same, which they are, up to the thread count and the output tag.
Each change is also compared by distance with 1.336 (the coordinator's second-root estimate) and 1.339 (my linear interpolation in D of the second root between 1.370705 at D 19.375 and 1.276162 at D 19.75). Called k_c 87 roots (macOS build). The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.01 grid step. The window ends at 1.28 and 1.42: nothing is said outside it.

## Beside which the scan is reported (information, not a pass rule)

k_c 87 on this machine (D 19.375, D 19.75): root near the line 1.434463, 1.338993; second root 1.370705, 1.276162; gap -0.063758, -0.062831. Linear in D, the root near the line would be 1.402640 at D 19.5 (dh610's 1.399169 is 0.003471 below it), the second root 1.339191.
k_c 79 at D 19.5: one change, 1.397565 (dh370, range [1.396781, 1.397565]); none in 1.30 to 1.50 otherwise (dh370 1.30 to 1.40, dh610 1.41 to 1.50). k_c 71 at D 19.5: 1.371531 and 1.449187 (win2).

## Predictions (information, not a pass rule; written before any run)

Source check passes with 2879 steps and all controls as wanted (95%); the regrid is accepted (80%) with about 3170 steps (2879 x 1.1004; dh610: 3171), taking about 19 min (12 to 25; 1051 s at D 19.375, 1181 s at D 19.75), rss max about 3.6 GB.
Against dh610's regrid: |F| and constraint of the same order (|F| within a factor 1.5: 80%); the step count within 5 of 3171 (65%); the states not bitwise equal (95%) and agreeing to a relative max difference below 1e-6 (60%).
The scan takes about 57 min (4 points a process at 830 to 870 s; 45 to 70), each process 2.6 to 4.3 GB, the four together near 11 GB.
Robust changes in 1.28 to 1.42: none (3%), one (30%), two (60%), more (7%). The change near the line within 0.003 of dh610's 1.399169 (75%; the brackets agree, (1.39, 1.40), 85%). A second change within 0.03 of 1.336 (55%).

## Status (23 Nov 2026)

| step | verdict | numbers | time (UTC) |
|---|---|---|---|
| source check | not started | | |
| regrid | not started | | |
| scan | not started | | |
