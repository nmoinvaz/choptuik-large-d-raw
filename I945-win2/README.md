# I945-win2: the residual floor of the D 3.04315 states, the plan's or the state's (M 320)

Machine: win2 (runner win2b), 8 threads. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/945 (recommended by #932).

Code: worktree `D:\choptuik-i932` at origin/main fa922af9 (`hp/plan_floor.py`, written by the coordinator), the installed hpkernel of #343's venv.
Command (from the coordinator's hc): `python plan_floor.py I945-win2/plan_floor.jsonl I932-win2/states/lowD343_D3.043150_M320_fail.npz
I932-win2/states/lowD343_p1_D3.043150_M320.npz --threads 8`, run in `hp/`. The `_fail` state is pass 2's stalled iterate (7.3e-21), the
pass-1 state (1.86e-18) is the reference.

- `run945.sh`: glue, runs the command and logs its exit in `exits_945.txt`.
- `w945.sh`: glue, a watcher that notifies when the `_fail` state's six records are written, on an exit, a Traceback, or after 2 h. It never kills.
- `plan_floor.log`, `plan_floor.jsonl`: the output, one record per state and plan.
