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

## The ladder at D 225.13 (`ladder_903.sh`, `rung_info.py`, `ladder/`)

These are the coordinator's rungs of +10 in the horizon order, each `--ks K --keep_plan 0 --steps 0 --save_base 1` from the previous rung's base. A failed rung is retried at +5, then +2 (+2 stands for +2.5, since `--ks` is an integer). After a reduced success the next step doubles, up to +10. A rung counts when its base is saved and the polish ends at max|F| ≤ 1e-60. `rung_info.py` takes each base on its own system (its ks, its new plan). The table is updated as rungs finish (`ladder/rungs.jsonl`).

| rung | polish | max\|F\| | p_min | ln(p_K/p_130) | Δ_K − Δ_130 | wall |
|---|---|---|---|---|---|---|
| 130 (q130) | 1 step | 4.2e-95 | 9.769e-19 | 0 | 0 | 4 min |
| 140 from 130 | 5 steps (start 4.5e-28, first step 2.4e-12) | 3.1e-96 | 6.773e-15 | +8.844 | −4.338e-13 | 59 min |
| 150 from 140 | **failed**: start 2.9e-26, step 4.4e-13, every λ 1 … 1/256 refused (2.1e12 … 2.2e4, ∝ λ⁴), 11 projections failed | | | | | 34 min |
| 145 from 140 | **failed**: iterate 0 accepted at 1.1e-27 → 1.1e-20, then iterate 1 refused at every λ (2.4e-16 at λ 1, 3.7e10 … 1.5e11 below), 9 projections failed | | | | | 56 min |
| 142 from 140 | 14 steps | 2.7e-71 | 4.499e-14 | +10.738 | −4.783e-13 | 63 min |
| 146 from 142 | **failed**: iterate 0 accepted at 1.3e-27 → 1.4e-21, then iterate 1 refused at every λ, 18 projections failed | | | | | 68 min |

The ladder stopped after rung 146 on the coordinator's redirect (#903, 13:16 UTC). The loop was stopped by hand while 146 ran, and 146's result line in `exits_ladder.txt` is written by hand. The highest converged rung is 142.

## The fixed-order chain (`chain_fixed_903.sh`, `chain_fixed/`, `compare_903.py`)

This chain runs at `--ks 142` from rung 142's base toward the fold, using `anm_run.py` with chain_nsr's flags at 8 threads and `--steps 400 --D_max 262`. It tests whether the fold moves with the order. #603's chain at order 130 folds at D* = 259.9033. If the fold moves by more than 0.05, it is the truncation's. If it stays within 0.01, it is not. Anything between is reported. `compare_903.py` sets p_min at each base against #603's chain at the same D, with ln p_603 interpolated linearly in D between #603's 181 bases. Its control, #603's log against itself, gives 0.00 everywhere.

### End: stopped at D 251.128 on the coordinator's order, before the fold (2026-11-18 00:47 UTC)

The chain ran from 2026-11-16 14:24 to 2026-11-18 00:47 UTC (exit 143, SIGTERM, `exits_chain.txt`). Its last state is `anm_pin3_D251.1277.npz` (Δ 1.684772725973740514410640365969032734566, ks 142), saved before the stop, without its series. It can resume from there. The last series is at D 251.008. No base reached the counted range (D ≥ 257.5), so the fold reading (`fold/`, `fold_est_903.py verdict`) was not run on this chain.

- From D 245, Δ142 − Δ603 (`delta_cmp.txt`, this chain's series at #603's states) equals minus #805's chain − series (`I805-mac/table.json`) to a smooth −2.25e-12 at D 246.26, falling to −3.1e-12 at 250.84. That holds while #603's departure grows to 2.7e-8 and changes sign twice.
- Past D 247 the steps were capped near a 0.5 by the horizon rung refinement, which diverged at a 0.625 and a 1. At D 251.008 the corrector's first damped step left the basin (|F| 2e-35 to 1e-23) at a 0.477 and 0.238, as #944 found at orders 150 and 160. a 0.119 recovered in 15 iterations to 1.9e-61.
- Unexplained discrepancy: this chain's rung refinement floors at 1e-43 to 1e-54 (1e-28 to 1e-30 at a 1 near D 242–246), while #603's (order 130, same flags) reaches 2e-79 to 6e-80 in 3 corrections.
