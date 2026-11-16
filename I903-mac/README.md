# I903-mac: the jump from horizon order 130 to 250 at D 225.13 (q130, q250, t250), the Mac pilot of #903

Machine: the Mac (Apple M5), 8 threads at nice 10, one run at a time. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/903 (the coordinator's comment of 2026-11-16 08:08 UTC).

Code: worktree at main 663e3b2d, venv-314 with the #523 hpkernel build (i599/site2). Command: `run_903_mac.sh`. It writes to the scratchpad with --allow_unraw, and the outputs are copied here. Start: `I603-win2/base/base_pin3_D225.1312.npz`.

## Result: q250 does not converge, so the pilot stopped before t250 (`exits_903.txt`)

| run | result | acceptance |
|---|---|---|
| q130 (ks 130, stored plan, 08:09–08:13 UTC) | max\|F\| 4.2e-95 at the start, so 1 step and no move. Δ equals #603's base exactly: diff 0, 40 digits (`delta_check.log`). Base saved in `q130/`. | (a) for q130: pass |
| q250 (ks 250, new plan of 21 steps, 08:13–09:29 UTC) | Start max\|F\| 6.37e-21, first Newton step \|dz\| 2.29e-12. The full step reads 8.1e27 and the strong chord is refused. Every trial from λ 1 down to 1/256 is refused: max\|F\| 8.1e27, 3.1e25, 1.1e23, 4.2e20, 3.1e18, 7.3e16, 5.6e15, 3.8e14, 2.4e13. The re-seeder's projection fails at all 11 trials (u0, its quad-double polish and the ladder). No step is accepted, the polish is not adopted, and no base is saved. | (a) for q250: **fails** |
| t250 | not run | (c): not reached |

The trial residuals fall as about λ⁸ at large λ and λ⁴ near λ = 1/256, with a λ⁴ coefficient of about 1e23. On that trend the 2.3e-12 step would have to be about 1e10 shorter before F fell below its start. So the direct jump from order 130 to 250 diverges at D 225.13, as #696's did at 245.14 (first full step 1.18e20).

## The pivots at q130's point (`pivots_903.py`, `pivots_903.log`)

These were measured after the failure, with `adjoint_split.py`'s system and LU at 8 threads. They are the smallest octo-double LU pivot of each system at q130's point. The ks 250 one is the Jacobian q250 factored first, so it is a start-point value, not a converged state's.

| system at q130's point | plan | max\|F\| | pivots | \|ψ\| | Newton step max\|dz\| (its Δ) |
|---|---|---|---|---|---|
| ks 130 | stored, 61 steps | 4.2e-95 | 9.769e-19 .. 7.95e31 | 9.1e18 | 6.1e-76 |
| ks 250 | new, 21 steps | 6.4e-21 | 4.765e-13 .. 4.35e38 | 1.0e13 | 2.29e-12 (−4.88e-13) |

ln(p250/p130) is +13.10 at this point, against the model's predicted 14 to 16. Δ(q250) − Δ(q130) does not exist, because q250 has no converged state. The Newton step's Δ component, −4.9e-13, is a first-order estimate only (#905 found the first-order response unreliable for a change of horizon order).
