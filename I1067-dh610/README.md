# I1067-dh610: M 512 lift of B2's M 384 state at D 3.0475 (low D), then Delta's Taylor series N 12

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1067 (coordinator, 2026-11-21). Follows #1014 (dh170's B1/B2 procedure, `I1014-dh170/run1014b.py`).

Input (raw origin/main commit dbcafa0f, copies here in `ref/` with their blobs): `ref/lowD1014b_D3.0475_M384.npz` (blob 74daf429), the converged M 384 vector on the planner's 2638-step plan, B1's output. `ref/` also holds unmodified copies of dh170's `resid1014.py`, `make_planb_1014.py`, `compare4_1014.py`, `run1014b.py`, `launch_b_1014.sh`.

Stages (issue and the coordinator's message of 17:3x UTC): 1. B1 `lowD_dd.py --Ms 512` from the M 384 state, the pilot being its first Newton call (stop rule: a first call above 8 h or an RSS above 45 GB stops the task with a report), then on to the residual's floor; 2. `make_planb_1014.py` with B2's settings (tol_step 1e-45, hmax 0.05), step count recorded; 3. `anm_lowd.py --N 12` on the resulting `_plan.npz`; 4. `compare4_1014.py`, M 512 against M 384.

Everything below is written as the run goes.

## Files

- `run1067_s1.py` (stage 1; `--selftest` 14 cases, `--selftest --mutate` fails as it must), `run1067_s23.py` (the plan and the series; `--selftest`, `--mutate`), `run1067.sh` (stage 1, then stages 2 and 3 only if stage 1 chose a state), `start_1067.sh` (unit `i1067a`, memory log `memlog_i1067a.log`).
- Stage 1 started 17:44:20 UTC 21 Nov in the worktree `~/Source/choptuik-large-d-1067` (detached at main 276aa1cd, venv-i1058, 10 threads, `nice -n 10`). Plan comment: https://github.com/nmoinvaz/choptuik-large-d/issues/1067#issuecomment-7066706257.
- Logs as they come: `stage1.log`, `exits_1067.txt` (every decision with its time), `rss_1067.txt` (RSS, peak RSS, MemAvailable, load every 60 s), `m512b.jsonl`, `states/`.

## Pilot report (first Newton call, 20:20 UTC 21 Nov)

First Newton call of `lowD_dd.py --Ms 512`: wall since the start 9340 s, the call's own `t` 9214.3 s; start max|F| 9.2e-07; line `newton 0: |F| 9.23e-07 |dz| 4.70e-03 lam 1 dDelta -1.31e-13 Delta 2.466012146521581 piv 4.0e-05..2.6e+01`; peak RSS 3.46 GiB (1.9 GiB for most of the call); about 940 to 970% CPU (10 threads); MemAvailable 58.4 to 59.8 GB. The stop rule (8 h, 45 GB) did not trip. Call 2 started 20:20 UTC. Posted as a comment on #1067.
