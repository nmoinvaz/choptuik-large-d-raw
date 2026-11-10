# AC54-mac: the finite-D states' D = infinity amplitude against the selection's M = 7 amplitude, with planted truth and controls

Machine mac (Apple M5), subagent of the coordinator, 2026-11-10. Issue https://github.com/nmoinvaz/agent-comms/issues/54
(no number here goes outside the project while the selection rule is a conjecture).

Code: `solver/inner_pert/ainf_from_states.py` of the worktree `/Users/nathan/Source/choptuik-ac54`, branch
`wip/ac54-amplitude` (from main 5eadc67), at 37f93ea (notes ae6c5b5) for the files at this folder's top level (`exits.txt` names it). It
imports `nnlo_closed_form.py`, `nnlo_vs_solution.py`, `solver/proof/trunc_seq_M7.py` and
`solver/inner_stokes/m7_outer.py`, all unchanged. Inputs: the field files of the raw-data repository's
`I126-mac/fields/` (63 states, D 15-215), and `I126-mac/fields_t140_d6/` and `fields_t140_d10/` for the chain swap,
read from the clone `/Users/nathan/Source/choptuik-large-d-raw` at d4d8258d. The M = 7 logs of
`solver/inner_stokes/logs/`. Python: /Users/nathan/venv-314/bin/python (3.14.7, numpy 2.5.4). One process, nice -n 10.

- `run_all.cmd`: every command as run, in order, from `solver/inner_pert/` of the worktree.
- `exits.txt`: the code's commit and each command's exit. For `planted --mutate=offset`, `states --mutate=...` and
  `controls`, 0 means the control behaved.
- `selection.*`: the M = 7 zero, the A and omega truncation sequences, the scenarios past M = 7, R1, R2.
- `planted.*`, `planted_mut_offset.*`, `planted_noise.*`: planted truth (P1, P2, Pm, and P3 with the real fit's residual
  as noise).
- `states.*`: the real states (R0, the grid, the reference fit, sensitivities, step diagnostic, chain swap, the gap).
- `states_mut_{shift,slope,step}.*` and `controls.*`: the mutations, and all controls together.
- `ainf_from_states_summary.json`: the summary the notes cite, the same as the branch's
  `solver/inner_pert/data/ainf_from_states.json`.
- `earlier_passes/pass1`-`pass10`: the same runs at the branch's earlier commits (3e924b8 to 15ced00, squashed into
  37f93ea and ae6c5b5), kept as run. Their numbers equal the final ones. The code changes between them only added
  outputs (cross-applied criteria, the summary file, the converged choices, the implied ratio).
