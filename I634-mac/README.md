# I634-mac: the chain's jets at D 236.63, 243.64 and 245.14 recomputed, noise or a complex-D singularity in orders 5–8

Machine: the Apple M5 Mac (subagent of the coordinator), nice 10. Threads: the reproduction at D 236.63 ran with 4
(04:32–07:32 UTC), a variant run at D 245.14 with 6 was stopped after 6 min 40 s (07:33–07:39), and every run from
07:39 UTC on used 2 (the coordinator's cap). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/634.

Code: choptuik-large-d branch `wip/i634-subagent` (main e6d46f0 plus `anm_run.py --save_jet` and
`hp/jet_singularity.py`), hpkernel built from main 3c35f0c (the #523 kernel and exact projector), Python 3.14 venv-314.

Inputs: #603's states `I603-win2/chain/anm_pin3_D*.npz`, predictions `pred_pin3_D*.npz`, records
`I603-win2/chain/anm_run.jsonl` and log `I603-win2/chain.log`, read from this repository at 3046bc7d (the 27 steps
from D 225.13 to 245.64).

Contents:
- `planted/`: the estimator's planted controls (`jet_singularity.py planted`, exit 0) and their control
  (`--mutate drop_pole`, exit 1).
- `preds.log`, `preds_mutate_scale5.log`: the chain's stored predictions against its converged states (exit 0) and
  the control (exit 1).
- `refusals.log`: every corrector attempt's first move, start and after-move residual, from #603's log.
- `repro/jet_pin3_D236.6312.npz`, `repro_D236.6312.log`: `anm_run.py --save_jet 2` with #603's flags, the 24-order
  octo-double series at D 236.63 (equal to the record's 25 norms and pivots bit for bit).
- `jets/D<D>_<variant>.npz` and their logs: `jet_singularity.py jet`, N 8 (od; `inject_1e-80_1`, noise injected into
  every order at 1e-80 of its right-hand side; `pert_<L>_<seed>`, the base moved by J^-1 r with max|r| = L; `qd`, the
  quad-double series).
- `repro16/jet_pin3_D245.1366.npz`, `repro16_D245.1366.log`: the 16-order series at D 245.14 (equal to the record's 17 norms). `polish/`, `polish_D245.1366.log`: the base at D 245.14 polished to 7.9e-93 (`--tol_od 1e-80 --save_base 1`) and its 8-order series.
- `run_634.sh`, `run16_634.sh`, `queue_634.sh`, `queue2_634.sh`: the commands; `exits_634.txt`: each run's exit.
