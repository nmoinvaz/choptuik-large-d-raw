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
