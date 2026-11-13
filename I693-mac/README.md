# I693-mac: the horizon series' radius at #603's chain states, D 225.13 to 253.80 (dd, qd, od; 13.6's pole law; the re-seed's start)

Machine: the Apple M5 Mac (the coordinator's), a subagent, 2 threads at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/693

Code: `hp/horizon_radius.py` on the branch `wip/i693-subagent` of choptuik-large-d (on main e1c5c9d0), hpkernel built
from main 3c35f0c (the exact freeze projector), venv-314 (Python 3.14). The note is `notes/HORIZON_RADIUS.md`.

Inputs: #603's states, raw `I603-win2/base/base_pin3_D225.1312.npz`, `I603-win2/chain/anm_pin3_D*.npz` and
`I603-win2/chain_nat/anm_pin3_D*.npz` (eight parts), their predictions `pred_pin3_D*.npz` and the records
`anm_run.jsonl`, as of raw 3ad5105. `states.txt` lists the 33 states read.

Files (`run_693.sh` holds every command; `exits_693.txt` each exit code, in order):
- `selftest.log`, `selftest_drop_term.log`: the planted check and its mutation (exit 0 and 1).
- `control_D253.7313.log`, `control_D253.7313_shift.log`, `control_D226.1312.log`: the extraction's controls C1, C2a,
  C2b and the mutation (exit 0, 1, 0).
- `onsol.jsonl`, `onsol.log`: the 33 states on the solution, in dd (horizon_alpha 0 and 1), qd and od, orders to 160,
  the estimators per field and harmonic; `coef/` their terms c_k u0^k (numpy, (161, 4, 32): order, field p m a c, lane).
- `law.jsonl`, `law.log`: 13.6's perturbation (a_h scaled by 1 + delta, delta 1e-40 to 1e-20) at 12 states, in qd;
  terms in `coef/`.
- `long.jsonl` (2 states), `long_all.jsonl` (33 states): qd to order 300, terms in `coef_long/`, `coef_long_all/`;
  `long_od.jsonl`: od to order 240 at D 253.73, terms in `coef_long_od/`.
- `ladder.log`: the re-seed (reseed.Reseeder, qd) on six stored predictions, the polish's history. The first four runs
  printed the start's a_h error with an f64 difference (0.0, below 1e-16); the last two with the exact one.
- `pdelta.log`: each stored prediction's horizon data against the converged state at the same D_str, exactly (54 pairs).
- `polish4.log`: the quad-double polish started from the prediction's own four parts, at three steps whose re-seed failed.
- `summary.log` (onsol and law, with #603's re-seed records), `summary_long.log`, `summary_long_all.log`,
  `summary_long_od.log`: `horizon_radius.py summary`. `csv.log`: the derived table `hp/data/horizon_radius.csv` (written
  twice; the second keeps the per-harmonic rows of the windows ending at 60 and 130 only).
