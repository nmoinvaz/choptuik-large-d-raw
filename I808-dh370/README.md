# I808-dh370: Delta at fixed D under the d6 and d10 held values and under a new plan, at #603's states

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/808.

Scripts (written by the coordinator): `run808.sh` (the jobs), `table808.py` (the table, the control and the verdicts,
with the rule fixed before the runs in its docstring). Code: worktree `choptuik-large-d-808` at main 0209d4d2
(`anm_run.py --held_from`), venv-i800 (main's kernel at ccc520e1 plus ks_w_from, off by default).

Each job polishes one of #603's states at its own D (`--steps 0`, #603's flags, `--qd_it 20`, `--save_base 1`):
- d6, d10: the held values of #608's chain of that fit (its last state, I608-dh610/chain_d6 at 243.1312 and chain_d10
  at 242.1312), carried to D by the fit, on #603's plan;
- plan: #603's own held values on a new plan (`--keep_plan 0`).

States: D 240.1244 (the control, against data/delta_fits.csv) and 250.8381, 251.8859, 252.6135, 253.5301, where
#603's departure from track C's series is near its envelope 2.2e-37/p_min. Pilot first: 253.5301 d10 (the hardest) and
240.1244 d6, 6 threads each; then the other 13 jobs, 3 at a time at 4 threads.

Why the design changed from the issue's text: anm_run holds the held values relative to the base, so `--held_fit` of
another degree alone changes nothing at fixed D. `--held_from` gives the other chain's values instead. #608's chains
use other plans (21 segments against #603's 61), so delta_fits.csv's differences carry a plan change too, and the plan
arm measures that part alone.
