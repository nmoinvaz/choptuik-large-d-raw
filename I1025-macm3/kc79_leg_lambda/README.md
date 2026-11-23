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
