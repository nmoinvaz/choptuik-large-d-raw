# I1025-macm3/kc79_leg_lambda: lambda_1 at each point of win2's k_c 79 leg (tag l1kc79Lw1025d), as it lands, no regrid

Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 15:29 UTC, before the first point's run.

## Order (the coordinator t5's hc, 2026-11-23 about 15:28 UTC, as given)

"Next, a rolling task on #1025: lambda_1 at each point of win2's k_c 79 leg (raw `I1025-win2/kc79_leap/states/`, tag l1kc79Lw1025d) as it lands, no regrid. Now: D 20.78125 (blob df800bba, record l1kc79Lw1025d.jsonl at raw 8378bd1b): `kc79_syscheck` accepts on your build
(both controls exit 1), then `d18_hybsign` at 0.93-1.03 by 0.01 plus a repeat of 0.98 (12 evals, 4 procs), `read_lower`. Then the leg's next point, window = its line (the last two lambda_1 points extrapolated) +-0.05 by 0.01 plus one repeat, each with its prediction in a README
section written before. One raw folder `I1025-macm3/kc79_leg_lambda/`, a section per D. Report each D's root and the slope from the previous D. Stop when the leg stops."

## Method (the same for every D; `point.sh DNAME`, parameters in `DNAME/point.env`)

1. Copy win2's state (`states/sol_l1kc79Lw1025d_D<D>.npy`) and the record file (`states/l1kc79Lw1025d.jsonl`) from the raw commit that carries them, with `git cat-file blob`, and check both blobs (the record file grows with the leg; the blob is the one at that commit).
2. `kc79_syscheck_1025.py` (29dce7ea) selftest (exit 0), the check on the state and the record at that D (must accept: |F| within 1% of the record's, `freeze_from` gives the record's steps), and both controls `--mutate=F` and `--mutate=steps` (exit 1 each). A refusal stops the point.
3. `d18_hybsign.py` (e089207a, unmodified) at the window's lambdas by 0.01 plus one repeat on another process than the first one, 4 processes of 1 thread, `nice -n 10`, each under `capped_run.py 28800` by exact pid, own session under `caffeinate -is` (`launch_1070.py`);
   at least 8 GiB available at the start (the D 20.75 scan: largest child 3.16 GB); every process must print `the record system` first, anything else is a stop. A sampler writes rss, cpu, available memory, free memory percent and free disk every 60 s (log only).
4. `read_lower.py` (89309d3c) with its selftest and both mutations (`--mutate=shift`, `--mutate=round2`: exit 1 each) and the reading of the window. Roots are read by position, never by sign orientation (the coordinator's correction of 2026-11-22); the estimator range is a spread over interpolation choices, not an enclosure; the float64 sign is information only, the hybrid sign the verdict.
5. Memory (Nathan's rule of 2026-11-08, the coordinator's correction of 2026-11-22): nothing stops or kills a process for memory; my watcher only alerts the coordinator by hc when available memory is under 2 GiB, free memory under 8% or free disk under 3 GiB.
   Stop and report on any failure; change no code. Each D gets a section below, its prediction written before its run; each D's files are in `D<D>/`. A point's window is the last two lambda_1 points extrapolated to its D, plus and minus 0.05 by 0.01 (11 values) plus one repeat, except the first (the coordinator's window).

Pins (scripts, as `../kc79_d2075/`): `kc79_syscheck_1025.py` 29dce7ea, `d18_hybsign.py` e089207a, `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f (raw 8e4797ff; `common/in/`). Code and build: worktree `~/Source/choptuik-large-d-1025m` at 505d8399, `venv-macm3-1058b` (Python 3.14.3, multidouble 5.1.0, neon).

## Previous points (information)

| D | lambda_1 | source |
|---|---|---|
| 20.5 | 1.0876 | the coordinator's (his line's anchor) |
| 20.75 | 0.989779 (det-linear; range 0.988339 to 0.989779) | `../kc79_d2075/` (this machine, raw 660e6fa0), comment 7105604010 |

The slope from 20.5 to 20.75 is -0.3913 per unit D.

## D 20.78125

**Inputs** (`D20.78125/pins.txt`): state `sol_l1kc79Lw1025d_D20.781250.npy` blob df800bba, record file `l1kc79Lw1025d.jsonl` blob a9d8281e, both at raw 8378bd1b (win2's leap point 1: Delta 1.1124310575074656, |F| 4.672744297624739e-10, 2698 steps, constraint 4.0278e-03, h 0.03125, 5348 s, from the D 20.75 state 1368e4ac).
**Window** (the coordinator's): lambda 0.93 to 1.03 by 0.01 (11 values) plus a repeat of 0.98 (on another process than the first 0.98): 12 evaluations.
**Prediction** (mine, from the coordinator's numbers; written before the run): the line through D 20.5 (1.0876) and D 20.75 (0.989779) has slope -0.3913 per unit D, so lambda_1 at D 20.78125 is 0.9776: **one robust change near 0.978, within 0.01, and no other change in 0.93 to 1.03.**


### D 20.78125: result (scan 15:29:55 to 15:56:11 UTC, 26 min)

**One robust change, + to -, between 0.97 and 0.98, at 0.979332 (det-linear; estimator range 0.977136 to 0.979332); no other change in 0.93 to 1.03. The prediction (one change near 0.9776, within 0.01) is met: the estimate is 0.0018 from it.**
The slope from D 20.75's 0.989779 is **-0.3343 per unit D** (range -0.4046 to -0.3343); the slope from D 20.5's 1.0876 to D 20.75 was -0.3913, the coordinator's line -0.31.

Source (`D20.78125/steps.txt`): ACCEPTED at 15:29:55 UTC on this build (`kc79_syscheck_1025.py`: exit 0, state |F| 4.6729631380e-10 against the record's 4.6727442976e-10, 2698 steps = the record's; selftest exit 0; controls `--mutate=F` and `--mutate=steps` exit 1).
The scan: 4 processes, each began with `the record system` and exited 0 (|F| 4.6729631380e-10, 2698 steps); 12 evaluations in `D20.78125/scan/scan_D20.78125_1025.jsonl`. `read_lower.py` selftest exit 0, `--mutate=shift` exit 1, `--mutate=round2` exit 1; the reading (exit 0):

    points 11 in 0.930-1.030; not noise-robust: none
    hybrid signs: 0.930+ 0.940+ 0.950+ 0.960+ 0.970+ 0.980- 0.990- 1.000- 1.010- 1.020- 1.030-
    float64 sign differs from the hybrid sign at: [(0.98, '-', '+')]
    repeated points: [(0.98, 'agree')]
      robust change (0.970, 0.980), + to -, det-linear 0.979332, range [0.977136, 0.979332]
    robust changes: 1; touching a non-robust point (not counted): none
    ln|det| local minima without a sign change: none
    endpoint signs: + at 0.930, - at 1.030

| lambda | hybrid sign | float64 sign | ln\|det\| hybrid | ln\|det\| float64 |
|---|---|---|---|---|
| 0.93 | +1 | +1 | -2346.7953 | -2346.4921 |
| 0.94 | +1 | +1 | -2347.7417 | -2347.7250 |
| 0.95 | +1 | +1 | -2348.7557 | -2348.3427 |
| 0.96 | +1 | +1 | -2349.8974 | -2349.2819 |
| 0.97 | +1 | +1 | -2351.3731 | -2351.3402 |
| 0.98 | -1 | +1 | -2354.0100 | -2351.3625 |
| 0.98 | -1 | +1 | -2354.0100 | -2351.3625 |
| 0.99 | -1 | -1 | -2352.5371 | -2351.6191 |
| 1.00 | -1 | -1 | -2352.6095 | -2355.3513 |
| 1.01 | -1 | -1 | -2352.9300 | -2353.6244 |
| 1.02 | -1 | -1 | -2353.3566 | -2353.8270 |
| 1.03 | -1 | -1 | -2353.8421 | -2353.7905 |

The repeat of 0.98 agrees (sign, noise signs, float64 sign, ln|det| -2354.0100 in both). The hybrid ln|det| at 0.98 (-2354.01) is 2.6 below 0.97's and 1.5 below 0.99's (the neighbour 0.99 is -2352.54): the dip a zero at 0.9793 gives. The float64 sign at 0.98 (+) differs from the hybrid (-), the one point beside the change.
Memory (alert-only): 89 samples, the largest child RSS 3.99 GB, the lowest available memory 10.3 GiB: no alert (this scan ran alone; the #1079 levers started after it).

| D | lambda_1 (det-linear) | range | slope from the previous D |
|---|---|---|---|
| 20.5 | 1.0876 | | (the coordinator's anchor) |
| 20.75 | 0.989779 | 0.988339 to 0.989779 | -0.3913 (from 20.5, using 1.0876) |
| 20.78125 | 0.979332 | 0.977136 to 0.979332 | -0.3343 (-0.4046 to -0.3343) |

The line for the next point: through D 20.75 and D 20.78125, slope -0.3343: lambda_1 at D 20.8125 is 0.9689, so its window is 0.92 to 1.02 by 0.01 plus a repeat (written when that point lands).


## D 20.8125

Written 2026-11-23 16:34 UTC, before the run. **Inputs** (`D20.8125/pins.txt`): state `sol_l1kc79Lw1025d_D20.812500.npy` blob 141bc9bc, record file `l1kc79Lw1025d.jsonl` blob b60b5403 (2 lines), both at raw c39988cb (win2's leap point 2: Delta 1.1132588598411506, |F| 4.670554648802493e-10, 2696 steps, constraint 4.1224e-03, 4866 s).
**Window** (the rule: the line through the last two lambda_1 points, plus and minus 0.05): D 20.75 0.989779 and D 20.78125 0.979332 give slope -0.3343 per unit D, so lambda_1 at D 20.8125 is 0.9689; the window is 0.92 to 1.02 by 0.01 (11 values) plus a repeat of 0.97 (nearest the line, on another process than the first 0.97): 12 evaluations. **2 processes** (beside the #1079 runs, the coordinator's word), each of 1 thread.
**Prediction** (mine, written before the run): **one robust change near 0.969, within 0.01, and no other change in 0.92 to 1.02.**


### D 20.8125: result (scan 16:35:03 to 17:08:36 UTC, 34 min, 2 processes)

**One robust change, + to -, between 0.96 and 0.97, at 0.969068 (det-linear; estimator range 0.966597 to 0.969068); no other change in 0.92 to 1.02. The prediction (one change near 0.9689, within 0.01) is met: the estimate is 0.00018 from it.**
The slope from D 20.78125's 0.979332 is **-0.3284 per unit D** (range -0.4075 to -0.3284).

Source (`D20.8125/steps.txt`): ACCEPTED at 16:35:03 UTC (`kc79_syscheck_1025.py` exit 0, |F| 4.6705546488e-10 as the record, 2696 steps; selftest 0; controls exit 1 each). The scan: 2 processes, each began with `the record system` (|F| 4.6665386001e-10, 2696 steps) and exited 0; 12 evaluations; `read_lower.py` selftest 0, `--mutate=shift` 1, `--mutate=round2` 1; the reading (exit 0):

    points 11 in 0.920-1.020; not noise-robust: none
    hybrid signs: 0.920+ 0.930+ 0.940+ 0.950+ 0.960+ 0.970- 0.980- 0.990- 1.000- 1.010- 1.020-
    float64 sign differs from the hybrid sign at: none
    repeated points: [(0.97, 'agree')]
      robust change (0.960, 0.970), + to -, det-linear 0.969068, range [0.966597, 0.969068]
    robust changes: 1; touching a non-robust point (not counted): none
    ln|det| local minima without a sign change: none
    endpoint signs: + at 0.920, - at 1.020

| lambda | hybrid sign | float64 sign | ln\|det\| hybrid | ln\|det\| float64 |
|---|---|---|---|---|
| 0.92 | +1 | +1 | -2343.1049 | -2343.3576 |
| 0.93 | +1 | +1 | -2344.0593 | -2343.9033 |
| 0.94 | +1 | +1 | -2345.0830 | -2345.2224 |
| 0.95 | +1 | +1 | -2346.2390 | -2346.2515 |
| 0.96 | +1 | +1 | -2347.7498 | -2347.5286 |
| 0.97 | -1 | -1 | -2350.0254 | -2348.0024 |
| 0.97 | -1 | -1 | -2350.0254 | -2348.0024 |
| 0.98 | -1 | -1 | -2348.8293 | -2349.1429 |
| 0.99 | -1 | -1 | -2348.9258 | -2349.2613 |
| 1.00 | -1 | -1 | -2349.2583 | -2348.8310 |
| 1.01 | -1 | -1 | -2349.6935 | -2349.6691 |
| 1.02 | -1 | -1 | -2350.1861 | -2350.2330 |

The repeat of 0.97 agrees (ln|det| -2350.0254 in both). Memory (alert-only): the largest child RSS 2.79 GB, the lowest available memory 12.3 GiB: no alert.

| D | lambda_1 (det-linear) | range | slope from the previous D |
|---|---|---|---|
| 20.5 | 1.0876 | | the coordinator's anchor |
| 20.75 | 0.989779 | 0.988339 to 0.989779 | -0.3913 |
| 20.78125 | 0.979332 | 0.977136 to 0.979332 | -0.3343 |
| 20.8125 | 0.969068 | 0.966597 to 0.969068 | -0.3284 (-0.4075 to -0.3284) |

Per the coordinator, the later k_c 79 leg points go to dh610; I stopped polling.
