# I1025-macm3/kc79_d2075: lambda_1 at D 20.75 from win2's accepted k_c 79 state, no regrid: source check, then a hybrid sign scan (lambda 0.95 to 1.07)

Written before the run, 2026-11-23 14:56 UTC. Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025.
Coordinator t5 (hc, 2026-11-23 about 14:55 UTC).

## Order (the coordinator's, as given)

"lambda_1 at D 20.75 on win2's accepted k_c 79 state (raw `I1025-win2/kc79_leap/`, the D 20.75 regrid: state blob 1368e4ac and its record, raw 60d75f9f), no regrid. `kc79_syscheck_1025.py` must accept the state on your build (|F| within 1% of the record,
`freeze_from` = the record's 2700 steps; both controls exit 1). Then `d18_hybsign.py` (the pinned copy you used for kc87_d1975) at 0.95-1.07 by 0.01 plus a repeat of 1.01 (14 evals, 4 procs, own session + caffeinate), and `read_lower.py` with its selftest and both mutations.
Memory alerts only."

**Prediction (the coordinator's, written before):** one robust change within 0.02 of 1.010 (lambda_1's line at -0.31 per unit D from D 20.5's 1.0876: 1.0876 - 0.31 x 0.25 = 1.0101); a second change is information.
Roots are read by position, never by sign orientation (the coordinator's correction of 2026-11-22); in posts "the root near lambda_1's line" and "the second root".
Stop and report on any failure; change no code. Memory (Nathan's rule of 2026-11-08, the coordinator's correction of 2026-11-22): nothing stops or kills a process for memory; my watcher only alerts, by posting the free memory to the coordinator when available memory is under 2 GiB,
free memory under 8% or free disk under 3 GiB; a refusal to START the scan when less than 8 GiB is available (4 processes x about 1.3 GB at k_c 79) is allowed.

## Inputs (pinned by `git hash-object --no-filters`; `prepare_inputs.sh` copies them with `git cat-file blob` into `in/`; `run_source.sh` and `run_scan.sh` check `in/` again)

```
1368e4ac  sol_l1kc79win2d2075_D20.7500.npy  <- 60d75f9f:I1025-win2/kc79_leap/sol_l1kc79win2d2075_D20.7500.npy   (win2's accepted k_c 79 state at D 20.75)
c83fa5b2  l1kc79win2d2075.jsonl             <- 60d75f9f:I1025-win2/kc79_leap/l1kc79win2d2075.jsonl            (its record, 1 line; the same bytes as rec_k79_D20.7500.jsonl)
29dce7ea  kc79_syscheck_1025.py             <- 8e4797ff:I1025-win/kc79_d19/kc79_syscheck_1025.py
e089207a  d18_hybsign.py                    <- 8e4797ff:I1025-dh170/kc_break/d18_hybsign.py
89309d3c  read_lower.py                     <- 8e4797ff:I1025-dh170/lower_root/read_lower.py
7c9d400f  d185_scan_read.py                 <- 8e4797ff:I1025-mac/d18/d185_scan_read.py
```

The record (win2, `regrid_accepted_D20.7500.txt`): k_c 79 at D 20.75, tag `l1kc79win2d2075`, source `l1kc71Lw1025c` (win2's leg-3 k_c 71 state, Delta_src 1.1116399184373311), |F| 4.673942570926068e-10, F_start 6.54056974712568e-05, **2700 steps**, constraint 3.934555992537646e-03,
Delta 1.111605142861567, lam_gauge 0.9349855515742403, kappa 0.7, u0 0.04, Ks 30, 4785 s. Code, build and venv as `../kc79_d19375/README.md`: worktree `~/Source/choptuik-large-d-1025m` at 505d8399 (`solver/matter`), `venv-macm3-1058b` (Python 3.14.3, multidouble 5.1.0, hpkernel neon),
`P4_WT_MATTER=<worktree>/solver/matter`. The state and its record are copied into the worktree's `solver/matter/data/` under the names the scripts read (`sol_<tag>_D20.7500.npy`, `<tag>.jsonl`) and checked by blob.

## Commands

Source check (`run_source.sh`, from `solver/matter`'s data folder as before): `kc79_syscheck_1025.py --selftest` (exit 0); `kc79_syscheck_1025.py RECORD STATE 20.75 <solver/matter>` (exit 0); the controls `--mutate=F` and `--mutate=steps` (exit 1 each).

Scan (`run_scan.sh`, only after `VERDICT.txt` reads ACCEPTED and at least 8 GiB are available): `d18_hybsign.py STUB STATE 20.75 "<lambdas>" OUT` in 4 processes of 1 thread (nice 10, each under `capped_run.py 28800` by exact pid), lambda 0.95 to 1.07 at 0.01 (13 values) and a repeat of 1.01 on another process than the first 1.01
(14 evaluations; p0 0.95, 0.99, 1.03, 1.07; p1 0.96, 1.00, 1.04, and the repeat 1.01; p2 0.97, 1.01, 1.05; p3 0.98, 1.02, 1.06); a sampler (log only) writes rss, cpu, available GiB, free memory percent and free disk every 60 s into `scan/scan_samples.csv`.
Then `read_lower.py selftest` (exit 0), `read_lower.py selftest --mutate=shift` and `--mutate=round2` (exit 1 each), and `read_lower.py scan 0.95 1.07`. Own session: `launch_1070.py` (double fork, `setsid`) running `caffeinate -is /bin/bash run_all.sh`; `session_check_*.txt` after the start.

## Acceptance (fixed before the run)

1. **Source.** `kc79_syscheck_1025.py` accepts the state and record on this machine (record |F| at most 1e-9, `freeze_from` gives the record's 2700 steps, the state's |F| within 1% of the record's), its selftest exits 0, both controls exit 1.
2. **Scan.** Only after ACCEPTED. Every process prints `the record system` first; anything else is a stop. The reader's selftest passes and its two mutations exit 1; the repeat of 1.01 agrees (sign, noise signs, float64 sign, ln|det| within 1e-6).

## Reading (fixed before the run; roots by position)

Every robust change by its position (bracket, det-linear estimate, estimator range; orientation is printed but not used to identify a root); the edge signs; every ln|det| minimum without a change (a candidate for two changes closer than the 0.01 step). The estimator range is a spread over interpolation choices, not an enclosure.
Each change is compared by distance with the line (1.0101, the coordinator's) and with k_c 79's root near the line at the earlier D (1.397565 at D 19.5, dh370; 1.431552 at D 19.375, macm3b); a second change is reported as information.


## Results (scan 2026-11-23 14:57:56 to 15:26:10 UTC, 28 min; reading 15:26:10)

**Verdict: the source is accepted; the scan has one robust change, + to -, between 0.98 and 0.99, at 0.9898 (det-linear; estimator range 0.988339 to 0.989779); no other change in 0.95 to 1.07.** The prediction ("one robust change within 0.02 of 1.010") is **just not met**: the change is 0.0203 below the line value 1.0101 (1.0876 - 0.31 x 0.25), 3e-4 outside the stated 0.02.

Source check (`run_source.sh`, `steps.txt`, `VERDICT.txt`): ACCEPTED at 14:57:56 UTC on this build: `kc79_syscheck_1025.py` exit 0, state |F| 4.6807304117e-10 against the record's 4.6739425709e-10 (0.15% apart), `freeze_from` 2700 steps = the record's 2700; its selftest exit 0; controls `--mutate=F` exit 1, `--mutate=steps` exit 1.
The scan: 4 processes (p0 0.95, 0.99, 1.03, 1.07; p1 0.96, 1.00, 1.04, the repeat 1.01; p2 0.97, 1.01, 1.05; p3 0.98, 1.02, 1.06), each exit 0, each began with `the record system` (|F| 4.6807304117e-10, steps 2700; 4 lines in `steps.txt`), 14 points in `scan/scan_D20.75_1025.jsonl`.
Memory (alert-only): 106 samples; the largest child RSS 3.16 GB, the lowest available memory 9.4 GiB, the lowest free memory 79%: no alert.

`read_lower.py` (`read_lower.txt`): selftest exit 0, `--mutate=shift` exit 1, `--mutate=round2` exit 1 (`selftest_read_lower*.txt`); `read_lower.py scan 0.95 1.07` exit 0:

    points 13 in 0.950-1.070; not noise-robust: none
    hybrid signs: 0.950+ 0.960+ 0.970+ 0.980+ 0.990- 1.000- 1.010- 1.020- 1.030- 1.040- 1.050- 1.060- 1.070-
    float64 sign differs from the hybrid sign at: [(0.99, '-', '+'), (1.0, '-', '+')]
    repeated points: [(1.01, 'agree')]
      robust change (0.980, 0.990), + to -, det-linear 0.989779, range [0.988339, 0.989779]
    robust changes: 1; touching a non-robust point (not counted): none
    ln|det| local minima without a sign change: none
    endpoint signs: + at 0.950, - at 1.070

| lambda | hybrid sign | noise-robust | float64 sign | ln\|det\| hybrid | ln\|det\| float64 |
|---|---|---|---|---|---|
| 0.95 | +1 | yes | +1 | -2351.8725 | -2351.7865 |
| 0.96 | +1 | yes | +1 | -2352.8737 | -2352.9531 |
| 0.97 | +1 | yes | +1 | -2353.9950 | -2353.7169 |
| 0.98 | +1 | yes | +1 | -2355.4178 | -2355.3777 |
| 0.99 | -1 | yes | +1 | -2359.2063 | -2355.5007 |
| 1.00 | -1 | yes | +1 | -2356.7396 | -2357.8151 |
| 1.01 | -1 | yes | -1 | -2356.7702 | -2356.9280 |
| 1.01 | -1 | yes | -1 | -2356.7702 | -2356.9280 |
| 1.02 | -1 | yes | -1 | -2357.0729 | -2356.8911 |
| 1.03 | -1 | yes | -1 | -2357.4883 | -2357.7408 |
| 1.04 | -1 | yes | -1 | -2357.9653 | -2358.0371 |
| 1.05 | -1 | yes | -1 | -2358.4809 | -2358.5359 |
| 1.06 | -1 | yes | -1 | -2359.0227 | -2358.8754 |
| 1.07 | -1 | yes | -1 | -2359.5834 | -2359.7045 |

- **The repeat of 1.01 agrees** (sign -, noise signs -, float64 sign -, ln|det| -2356.770169044411 in both: difference 0 within 1e-6).
- **Position** (by position, not by sign orientation): lambda_1 at D 20.75 on k_c 79 lies in (0.98, 0.99), at 0.9898 by the det-linear estimate and in 0.988339 to 0.989779 by the estimator range (a spread over interpolation choices, not an enclosure). The hybrid ln|det| at 0.99 (-2359.21) is 3.8 below its neighbours' (-2355.42 at 0.98, -2356.74 at 1.00), which a determinant crossing zero at 0.9898 explains.
  The line's value 1.0101 is 0.0203 above the estimate (0.0203 to 0.0218 above the range); the bracket's upper end 0.99 is 0.0201 from it. From D 20.5's 1.0876 (the coordinator's) to the estimate the slope is -0.3913 per unit D (-0.3970 to -0.3913 over the range), against the line's -0.31.
- **The float64 sign** alone reads + at 0.99 and 1.00 and flips between 1.00 and 1.01 (the hybrid sign is the verdict; the float64 sign is information only, as in the earlier scans): it differs from the hybrid at 0.99 and 1.00, the two points beside the change, where the float64 |det| (ln -2355.50 and -2357.82) is not near the dip.
- No second change, no ln|det| minimum without a change, in 0.95 to 1.07; the endpoint signs are + at 0.95 and - at 1.07 (one change between).
