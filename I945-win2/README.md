# I945-win2: the residual floor of the D 3.04315 states, the plan's or the state's (M 320)

Machine: win2 (runner win2b), 8 threads. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/945 (recommended by #932).

Code: worktree `D:\choptuik-i932` at origin/main fa922af9 (`hp/plan_floor.py`, written by the coordinator), the installed hpkernel of #343's venv.
Command (from the coordinator's hc): `python plan_floor.py I945-win2/plan_floor.jsonl I932-win2/states/lowD343_D3.043150_M320_fail.npz
I932-win2/states/lowD343_p1_D3.043150_M320.npz --threads 8`, run in `hp/`. The `_fail` state is pass 2's stalled iterate (7.3e-21), the
pass-1 state (1.86e-18) is the reference.

- `run945.sh`: glue, runs the command and logs its exit in `exits_945.txt`.
- `w945.sh`: glue, a watcher that notifies when the `_fail` state's six records are written, on an exit, a Traceback, or after 2 h. It never kills.
- `plan_floor.log`, `plan_floor.jsonl`: the output, one record per state and plan.

## First launch and why the second uses `_ckpt_failed`

The coordinator's command put `I932-win2/states/lowD343_D3.043150_M320_fail.npz` first. `lowD_highM.py` saves that final iterate of pass 2 (7.3e-21) without a stored plan (its meta has D, M, kc, ks, kt, nodes only), so `plan_floor.py` stopped on `KeyError: 'segs'` after 4 s (`run945.sh`, `plan_floor.log` before the second launch). `lowD343_D3.043150_M320_ckpt_failed.npz` is the same iterate bit for bit (max |zh diff| 0.0, zh + zl the same) and stores pass 2's own plan of 14358 steps, so the coordinator's hc ordered the same command with it first (`run945b.sh`, `w945b.sh`). The pass-1 state (`lowD343_p1_D3.043150_M320.npz`, the reference) stores its plan of 10575 steps. `plan_floor.log` of the first launch is kept as `plan_floor_first_launch.log`.

## Second question: where the residual sits, and Newton with the refined step

The pass-1 reference state (`lowD343_p1_D3.043150_M320.npz`, 10575 steps) gave max |F| 1.865e-18 on its own plan, split 4, 8, 16, and replanned with hmax 0.025, and nan on the control, as on the coordinator's Mac (`plan_floor.jsonl`, `plan_floor.log`; exit 0 after 3068 s). The coordinator then ordered, at main 043834d9, `plan_floor.py ... ckpt_failed.npz --skip_plans --by_block --newton f64g --it_max 6 --threads 8` (`run945c.sh`, `w945d.sh`, output in the same `plan_floor.jsonl`, log `plan_floor_newton.log`). `w945c.sh` is the watcher of the second launch's end.

Result of that third launch (`run945c.sh`, exit 0 after 14289 s, 13:20:11 to 17:18:20 UTC): the by-block table (blocks 6 and 7 at 3.7e-21 and 7.3e-21, the rest 4e-24 to 5.3e-22), then Newton step 0 from |F| 7.35e-21 (7.3486e-21 in `plan_floor.jsonl`, record `newton f64g`, `it` 0, `failed: line search`). Its two log lines, the first written 15:04:36 UTC and the second at the exit: "no decrease along the f64-Jacobian step; retrying with the dd4 Jacobian (M > 128: no exact dense Jacobian)" and "no decrease along the Newton step, giving up". So it ran one step, not six: neither the f64-Jacobian step nor the dd4-Jacobian step lowered |F|. `w945e.sh` is the watcher of this launch's end (glue, never kills).

## Third question: how far the floor moves Delta (`--delta_corr`)

The coordinator ordered, at main 808b1fac (`plan_floor.py --delta_corr`, -y.F through `newton_mixed`'s f64 LU as `lowD_dd.sensitivity` reads it, with its bound sum|y F| and max|y| per block): `plan_floor.py plan_floor.jsonl lowD343_p1_D3.043150_M320.npz lowD343_D3.043150_M320_ckpt_failed.npz --skip_plans --delta_corr --threads 8` (`run945d.sh`, output in `plan_floor.jsonl`, log `plan_floor_delta.log`, watcher `w945f.sh`). The pass-1 state is the check: its -y.F must reproduce its record's dDelta_est (-1.831e-17) to a few percent.

The check failed (pass-1 -y.F -1.311e-17 against the record's -1.831e-17, max|y| from block 7 on 3 to 4.6 times smaller). The coordinator's reading, to test: near the closing the Jacobian is so ill-conditioned in the valley blocks that the f64 LU's y depends on the parallel rounding, so `--threads 10` (the thread count of #932's leg, which made the record) should reproduce the record. Fifth launch, `run945e.sh` (glue: waits for the fourth launch's exit, then the same command on the pass-1 state only with `--threads 10`), jsonl `plan_floor_t10.jsonl` (a separate file so the two thread counts are not mixed), log `plan_floor_delta_t10.log`, watcher `w945g.sh`.

## Fourth question's answer and the rerun of #932's step 2 with `--accept 1e-20` (`leg/`)

`--delta_corr` at 8 threads: the stalled state's -y.F is -1.014e-17 with bound sum|y F| 7.133e-15, the pass-1 state's -1.311e-17 with 7.666e-12 (the record's dDelta_est -1.831e-17, so that check failed at 8 threads), from `plan_floor.jsonl` (`run945d.sh`, `plan_floor_delta.log`). The 10-thread run of the pass-1 state is `plan_floor_t10.jsonl`, `plan_floor_delta_t10.log`.

The coordinator then ordered #932's step 2 again with one change, `--accept 1e-20` (floor rule `--floor_ratio` 0.5 at the default), in the fresh folder `leg/` (`run945f.sh`: glue from `I932-win2/run932b.sh`, waits for the 10-thread run, then the setup and the leg's command; watcher `w945h.sh` with the stop rules of `I926-mac/runner_task_M320.md`, as `w932b.sh`). The plan and its reason are in the issue comment of 2026-11-17 about 19:25 UTC. States, `leg.jsonl`, `leg_points.jsonl`, `leg.log` and the progress file are in `leg/`.
