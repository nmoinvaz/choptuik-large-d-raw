# I1025-dh610/d19125: hybrid sign scan at D 19.125 (k_c 63), lambda_1 1.505 to 1.545 at 0.0025: do the two roots still exist?

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../d1909/` (raw f2405ef9, accepted): the same setup and acceptance at D 19.125, the decisive point. #997's rerun (unit `i997t`) and #1067's series (unit `i1067d`) run beside it and are not touched.

Why: the gap between the two lambda_1 roots was 0.0548 at D 19 (dh370: 1.4832, 1.5380) and 0.0205 at D 19.09375 (`../d1909/`: 1.511102, 1.531607, det-linear). Their midpoint moved from 1.5106 to 1.5214.

## Model predictions (information, not pass rules)

| model | gap at D 19.125 | the roots meet near | what the scan would show |
|---|---|---|---|
| gap linear in D (two points: 0.0548 at 19, 0.0205 at 19.09375) | about 0.0091 | D 19.150 | two sign changes near 1.5204 (+ to -) and 1.5295 (- to +) |
| gap squared linear in D (the generic shape at a collision of two real roots): gap^2 is 3.0e-3 and 4.2e-4, slope -0.0276 per unit D | none | D 19.109 | no sign change; ln\|det\| with a minimum without a change near the midpoint, expected about 1.525 (midpoint trend 1.5214 + 0.0036) |

## Setup (as `../d1909/`; no control rerun: same machine and build, and its control passed)

Budget: 6 processes of 1 thread (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, one systemd user unit `i1025g` (lane script `lane_d19125.sh`, started by `start_d19125.sh`, log `exits_d19125.txt`). Worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean), `~/Source/venv-i1058/bin/python`, `P4_WT_MATTER=<worktree>/solver/matter`.

Inputs (raw origin/main f2405ef9, copied to `in/`, pinned by `git hash-object --no-filters`, `in_blobs.txt`; the lane script refuses to start on any other blob): `d18_hybsign.py` e089207a (xfkappa's, unmodified), `sol_l1kc63dh370_D19.125000.npy` 832e07e4, `l1kc63dh370.jsonl` 11454d97 (raw d4412097, the record row of D 19.125: |F| 2.7024818241652036e-10, 2354 steps), the reader `read_lower.py` 89309d3c (dh170's, unedited) with `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9.

Scan: lambda 1.505 to 1.545 at 0.0025 (17 values) plus a repeat of 1.525 (18 evaluations) over 6 processes, cap 8 h each by exact pid: value i goes to process i mod 6 (`scan_hyb.sh`'s splitting), so the repeat (index 17) runs on process 5 and its original (index 8) on process 2. The system check is `d18_hybsign.py`'s first line per process (exit 3 stops that process). Lambdas are written with four decimals.

## Does `read_lower.py` read a 0.0025 grid? (checked before the run, reader not edited)

Its keys are `round(lambda, 4)`, its change finder takes the real x of each point, and it prints lambdas to three decimals (display only: 0.0025 steps give no collision, but a label such as 1.5075 prints as 1.507 or 1.508; the tables below use the exact values). `plant_grid4.py` plants three scans on this run's lambda list, written as six files like the lane's and read through the reader's command line: A two roots 0.0092 apart (1.5204, 1.5296), B a merged pair (no root, a minimum at 1.525), C one root at 1.51137. The plain run reads all three as planted (A: 1.52051 and 1.52949; B: no change, one free minimum at 1.525; C: 1.51137; the repeat agrees). `--mutate=shift` (expected roots moved by 0.003) exits 1, and `--mutate=round2` (lambdas written to two decimals) exits 1. So it reads four-decimal keys.

## Acceptance (the coordinator's, as at D 19.09375)

- the system check passes on all six processes; the reader's selftest passes and its mutations `shift` and `round2` each exit 1 (`selftest_exits.txt`: read_lower 0, shift 1, round2 1, repeat_check 0, plant_grid4 0, its shift 1, its round2 1);
- the repeat of 1.525 agrees (sign, noise signs, float64 sign, ln|det| within 1e-6);
- read: every robust change with its det-linear estimate and estimator range (a spread over interpolation choices, not an enclosure), orientation as printed; or none, and then the smallest ln|det| of the scan and whether ln|det| shows a minimum without a change (what a merged pair leaves behind); changes touching a non-robust point listed and not counted.

Estimate (coordinator's): about 40 min; at D 19.09375 the points took 567 to 860 s each with six processes beside the series, three rounds here.

Written as the run goes.
