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

## Restart record and the scaled control (21 Nov, 20:25 to 20:33 UTC)

- First launch (unit `i1067a`, 17:44:20): call 1 landed 20:20:00 (pilot report above). My script's measurement control (dh170's planted +1e-20 via `ref/resid1014.py`, must read 1.0e-20) read 9.55e-13, the checkpoint's own max|F|, so it could not show; the script treated that as a failure and sent TERM to the exact pid 1072419 at 20:25:00, five minutes into call 2, and ran no later stage. The checkpoint after call 1 (`states/lowD1067_D3.0475_M512_ckpt_after_call1.npz`, `it` 1) survived. Log kept as `stage1_launch1.log`.
- Resume (unit `i1067b`, `run1067_resume.sh`, `start_1067b.sh`): 20:26:29 UTC, `RESUME_CALLS=1`: `lowD_dd.py --resume --it_max 2` ("resuming from checkpoint ... (iteration 1)"), log `stage1_resume1.log`; calls 2 and 3, the same floor rule (|dDelta| below 1e-25 accepts), then stages 2 and 3 automatically.
- The fix: `resid1067.py` (a copy of `ref/resid1014.py`; `--plant P`, `--plant 0` evaluates the planted case with nothing planted) and `plant_ok` in `run1067_s1.py`: the as-saved max|F| F is read first, P = max(1e-20, 1e3 F) is the nominal plant, the reading after planting must lie in [P/2, 2P] and above F. A failed control marks the measurement unvalidated and never stops the run. `run1067_s1.py --selftest` 18 cases (four for the control), `--selftest --mutate` fails.
- The control shown once on call 1's checkpoint (as-saved max|F| 9.551e-13, P 9.551e-10; `resid_test_call1.*`, `control_demo_noplant.txt`, `control_demo1067.py`): with the plant applied it reads 9.551e-10 and detects it (`plant_ok` True); with nothing planted (factor 0) it reads 9.551e-13 and reports the miss (`plant_ok` False, as expected).

## Command diff of the resumed stage 1 (the coordinator's request of 21 Nov)

`cmddiff_stage1_resume.txt`: the command of the resumed launch (unit `i1067c`, first line of `stage1_resume1.log`) against the command of the plan comment 7066706257, tokens, python3 against the venv's python normalized: `--it_max 3` becomes `2` and `--resume` is added, both intended (calls 2 and 3 after the call-1 checkpoint), nothing else.
