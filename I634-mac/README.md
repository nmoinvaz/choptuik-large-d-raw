# I634-mac: the chain's jets at D 236.63, 243.64 and 245.14 recomputed, noise or a complex-D singularity in orders 5–8

Machine: the Apple M5 Mac (subagent of the coordinator), 4 threads at nice 10. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/634.

Code: choptuik-large-d branch `wip/i634-subagent` (main e6d46f0 plus `anm_run.py --save_jet` and `hp/jet_singularity.py`), hpkernel built from main 3c35f0c (the #523 kernel and exact projector), Python 3.14 venv-314.

Inputs: #603's states `I603-win2/chain/anm_pin3_D*.npz` and records `I603-win2/chain/anm_run.jsonl` (read from this repository at 3046bc7d).

Contents (filled in as the runs land):
- `repro/`: `anm_run.py --save_jet 2` at each base with #603's flags, the octo-double jet at the stored state (the reproduction of the records' norms).
- `polish/`: the same with `--tol_od 1e-80`, the base polished further before its jet.
- `jets/`: `jet_singularity.py jet` variants (base perturbed by J^-1 r at max|r| 1e-60, the quad-double jet, noise injected into each order's right-hand side).
- `planted/`: the estimator's planted controls.
- `*.log`: every run's log.
