# I932-win2: the point at D 3.04315 with the sonic-refined plan, M 320 and 384

Machine: win2 (runner win2b), 10 threads. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/932 (recommended by #926).

Code: worktree `D:\choptuik-i932` at origin/main 65ec482f (`hp/sonic_valley.py`, `hp/lowD_highM.py --sonic_refine --sonic_stop`, Python
only, the installed hpkernel of #343's venv). The steps are those of `I926-mac/runner_task_M320.md` with main in place of `wip/sa-926`,
this folder, and the history file `I343-win2/leg2.jsonl.progress.json.bak` (the leg's state before the hand edit of its targets).

Glue launchers (they only chain the file's commands and log each exit in `exits_932.txt`):

- `run932a.sh`: step 0 (`sonic_valley.py planplant`, then the control `--mutate norefine`, which must exit 1) and step 1 (`startcase`).
- `run932_ctl.sh`: the control of step 2 in `control/`, without `--sonic_refine 4`, killed after its first Newton call.
- `run932b.sh`: step 2, the point at D 3.04315 at M 320 and 384 with `--sonic_refine 4 --sonic_stop`.
