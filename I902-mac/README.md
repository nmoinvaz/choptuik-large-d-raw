# I902-mac: the σ test without a polish, at the stored z with the horizon order raised (D 237–254, and D 60)

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/902

Code: wip/xf-902 (main 62f64c9a, then 4e3e5234, 2a73d409, 8f1da6a2 and 5e8b08db: `near_null.py --ks`), on main 3c35f0c's
hpkernel, from the choptuik-large-d-902 worktree; the model from `solver/factored_horizon_sympy.py model` at the same
commit. One process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). Runs in `queue.sh` order, after
I875-mac's queue.

States: #603's I603-win2/chain/anm_pin3_D237.1312.npz and anm_pin3_D249.0113.npz, and
I603-win2/chain_nat/anm_pin3_D253.8043.npz (the one #693's model rows use), each at ks 130 with its stored plan. The
control is I611-win/kf13_D60_D60.001952.npz (M 32, quad-double, kfreeze 13, ks 100, no stored plan, so near_null.py
makes one at the state, the same for every ks).

## What near_null.py does here

- **The system at the stored z, no Newton step.** `newton_o` factors J at z and returns its step, which is printed
  and not applied; the run checks that z is unchanged after every kernel call. The stored plan is kept at every ks.
- **`--ks K`.** The horizon series is summed to order K. hp sizes it at run time (`model.rs`: vectors of length
  ks + 2, horizon LUs for orders 0..ks), so no compiled size limits it; #696's r300 ran at ks 300.
- **The rows check.** At a changed ks, F and the exact Jacobian at z are formed at both orders, and the residual
  blocks whose rows differ are listed (centre, Taylor 1–4, horizon, phase): only the horizon block may differ.
- **`--mutate=ks`.** The solver is built at the state's order while the run is otherwise the `--ks 250` run, and it
  must reproduce the ks 130 run bit for bit. Main's kernel has no weight on the tail (wip/i800's `--ks_w_from` is on
  a branch from before #523), so this control checks the override's path; the rows check covers the kernel.
- **The reading, g = 1 / ‖e_Δᵀ J⁻¹‖₂.** This is the grip on Δ, from one transpose solve: how far Δ moves for a unit
  residual. The issue reads σ₃. g is used instead, because σ₃ by index changes identity once a weak mode rises past
  another (at D 237.13 σ₄ / σ₃ = 1.8, #488). σ₁–σ₆ by index, with their Δ shares, and the Δ mode followed by its
  vector's overlap are reported beside it. The coordinator accepted this on the issue, with the same bars, and
  asked for a note wherever g and σ₃ disagree on the verdict: `sigma.py` prints σ₃'s verdict beside g's.

In progress. `queue.sh` ran the model and the pilot, D 253.80 at ks 250 (8f1da6a2), which passed its check. The
queue was then stopped at 05:20 UTC: on the loaded Mac the pilot took 40 min, most of it the check's 140-digit mpmath
product ‖J v₁‖. `--jv=od` (5e8b08db) forms that product in octo-double by columns. `queue2.sh` runs the other sixteen
runs with it, the first (D 253.80, ks 130) with `--jv=both` to set the two against each other.

## Criteria (posted on the issue before the runs)

P(K) = ln f(K) − ln f(130), μ = 1, from `model.log`'s M2 lines (FACTORED_HORIZON.md 4.2's table).

| # | criterion | fails when |
| --- | --- | --- |
| C1 | every near_null check passes (σ₁ converged to 1e-3, ‖J v₁‖ / σ₁ within 1e-2, z unchanged), and at every changed ks only the horizon block's rows of F and J differ, F's there nonzero | a run's check fails, or another block changes |
| C2 | `--ks 250 --mutate=ks` at D 253.80 equals the ks 130 run bit for bit (σ, g, pivots, steps); `sigma.py --selftest` passes (planted: model-like supports, flat refutes, a control off by 0.1 and a mutation one ulp off fail) | the override's path changes the system, or a planted case is misread |
| C3 | control, D 60: \|ln g(K) − ln g(130)\| and \|ln σᵢ(K) − ln σᵢ(130)\|, i = 1–4, below 0.05 for K = 160, 200, 250 | either reaches 0.05 |
| C4 | supports the reading: at D 237.13, 249.01 and 253.80, ln g(200) − ln g(130) within 30% of P(200), and \|ln g(250) − ln g(200)\| < 1 | any of the six fails |
| C5 | refutes it: \|ln g(250) − ln g(130)\| < ln 2 at D 253.80 | (it is the refutation) |
| C6 | reported: σ₁–σ₆ by index and the Δ mode tracked, at every D and ks; the step's Δ component at each ks; the horizon rows' max\|ΔF\| | (reported) |

The verdict is "supports" if C4 holds and C5 does not, "refutes" if C5 holds, and "neither" otherwise.
