# AC42-mac: the closed-form large-D solution, the corrected NNLO with the profile's 1/n terms, against the finite-D solutions at D 40-200

Machine mac (Apple M5), subagent of the coordinator. Issue https://github.com/nmoinvaz/agent-comms/issues/42.
Code: `solver/inner_pert/nnlo_closed_form.py` of the main repository (merge of wip/ac42-closed-form). Inputs: the
field files of `I126-mac/fields/`, at commit 5762066d of this repository. Python: /Users/nathan/venv-314/bin/python.
One process, nice -n 10. The write-up is notes/SECOND_ORDER.md section 1.2 of the main repository.

- `planted.cmd`, `compare.cmd`: the commands as run, from `solver/inner_pert/` of the worktree, with this Mac's
  absolute paths. notes/SECOND_ORDER.md gives them with relative paths.
- `exits.txt`: each command's exit. Under `--mutate`, 0 means the control fired.
- `planted*.json`, `planted*.log`: the planted-truth run (C6) and its mutations.
- `compare*.json`, `compare*.log`, `controls.*`: the closed form against the stored solutions (C1-C5), its controls,
  and the resolution scan of mutated K1 and K2 (logs only).
- `closed_form_K.json`: F, K1, K2 of every odd harmonic up to 31 and the Delta series. The main repository keeps a copy
  as `solver/inner_pert/data/closed_form_K.json`.
