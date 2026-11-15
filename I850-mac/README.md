# I850-mac: Newton's return from a pure Δ move at D 240.1244 and 252.6135

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/850

Code: hp/step_spread.py on wip/xf-850 (d78c0a90, from main 4694993d), which adds `--blocks`, `--match`, `--mutate noop`
and the `power` subcommand, on main 3c35f0c's hpkernel. One process at nice 10, 3 kernel threads,
OPENBLAS_NUM_THREADS=1 (`run.sh`). States: I603-win2/chain/anm_pin3_D240.1244.npz and D252.6135.npz in #837's
truth_system. Runs in `queue.sh` order.

In progress.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--selftest` passes, and `--mutate=nosub` (the power read without subtracting the unperturbed step) and `power --mutate start` (one run's unperturbed step an ulp off) fail | a planted power is misread, or a control passes |
| C2 | `--blocks centre --seeds 1` at D 240.1244 reproduces #840's centre control (I840-mac/ss_D240.json) with dΔ and max\|F\| equal as doubles (`--match`); `--mutate noop` (seed runs left unperturbed) must FAIL on max\|F\| | the option perturbs the wrong block or nothing, or the control passes |
| C3 | `--ref` passes in every run: −4.3765436014297066e-58 at 240.1244, +5.2645963792835124e-82 at 252.6135 | the unperturbed step changes |
| C4 | `--blocks Delta` at rel 1e-65 reproduces #840's Delta control (seed 1, the same signs) at both D (`--match`) | the new path differs from #840's |
| C5 | per D, the power p of dev = dΔ(seed) − dΔ(unperturbed) at 1e-65 → 1e-66 and 1e-66 → 1e-67: quadratic (both p in [1.8, 2.2]), linear (both in [0.9, 1.1]), or neither; with \|dev\| / move, which an accurate step makes 1 | (a reading, stated per D) |

A linear reading with |dev| / move near 1 is an accurate step. A linear reading far from 1 means the Jacobian does not
return Δ's own column, and a quadratic reading means the step's second-order term dominates the move.
