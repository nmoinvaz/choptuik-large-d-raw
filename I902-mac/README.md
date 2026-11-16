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

### Runs and timing

`queue.sh` ran the model and the pilot, D 253.80 at ks 250 (at 8f1da6a2, ‖J v₁‖ by mpmath at 140 digits), which passed
its check. The queue was then stopped at 05:20 UTC, because the pilot took 40 min and I took its 1646 s timer for the
check's mpmath product. `--jv=od` (5e8b08db) forms that product in octo-double by columns, and `queue2.sh` ran the other
sixteen runs with it, the first (D 253.80, ks 130) with `--jv=both`: the two agree to 2.22e-16, but the mpmath product
took 2 s. The time is the exact Jacobian (514 s at ks 130 on the loaded Mac), formed twice at a changed ks for the rows
check, so the restart saved little (a misreading of mine, corrected on the issue). Each run at a changed ks took 20–40
min at D 237–254 and 60–66 min at D 60. The queue ended at 15:06 UTC.

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

## Result

The ks = 130 cut is a real but partial cause of the weak grip on Δ. Raising ks lifts g at the stored z by e^18.5,
e^27.7 and e^34.8 at D 237.13, 249.01 and 253.80, all of it by ks 160 (D 237.13, 249.01) or ks 200 (D 253.80), and this
falls short of the model's P(200) by 54%, 49% and 43%. So by the posted bars the verdict is **neither** (C4 and C5 both
fail). The horizon residual and the harmonic-3 pair do follow the model's f; Δ and its harmonic-1 neighbour stop rising
early, with g at ks 250 7.1e-16, 7.7e-18 and 6.3e-18 (M5's σ_∞ at D 253.80 is 1.6e-5, `model.log`).

| # | criterion | verdict | number |
| --- | --- | --- | --- |
| C1 | runs' checks; only the horizon rows change | **FAIL** at D 249.01 ks 160; pass with its rerun at `--its=32` (below) | σ₁ converged to 1.35e-3 (bar 1e-3), and to 7.96e-07 in the rerun; the other 16 runs pass; at every changed ks only the horizon block changed, its max\|ΔF\| 1.76e-27 (D 60) to 2.09e-12 |
| C2 | mutation equals ks 130 bit for bit; selftest | pass | `--ks 250 --mutate=ks`: equal; `sigma.py --selftest`: PASS |
| C3 | control, D 60 | pass | largest \|Δ ln g\| or \|Δ ln σᵢ\| 0.00e+00 (bar 0.05) |
| C4 | supports | does not hold | ln g(200) − ln g(130) +18.512, +27.718, +34.740 against P(200) +40.25, +53.89, +60.51 (−0.54, −0.49, −0.43 of it, bar ±0.3); ln g(250) − ln g(200) −0.000, −0.006, +0.051 (bar 1) |
| C5 | refutes | does not hold | ln g(250) − ln g(130) +34.791 at D 253.80 (bar ln 2) |
| C6 | reported | below | |
| — | verdict on g | neither | σ₃ by index: supports, so **g and σ₃ disagree** (below) |

`sigma.log` exits 1, from C1. `sigma_its32.log`, with the rerun in place of the 16-iteration run, exits 0 with the same
verdict.

### g and σ₁–σ₄ by D and ks

g = 1/‖e_Δᵀ J⁻¹‖₂; σᵢ by index; "Δ mode" is the vector followed from ks 130 by overlap (`sigma.log`); "step Δ" is the
pinned Newton step's Δ at z (not applied), the linear estimate of Δ's move to the root at that ks; max|ΔF| is the
horizon rows' change of F at z from the state's ks.

| D | ks | g | ln g | σ₁ | σ₂ | σ₃ | σ₄ | Δ mode (overlap) | step Δ | max\|ΔF\| | check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 237.13 | 130 | 6.521710e-24 | −53.3869 | 3.040e-25 | 3.011e-25 | 1.500e-23 | 2.712e-23 | σ₃ (Δ share 0.99) | +5.314e-59 | – | pass |
| | 160 | 7.145228e-16 | −34.8749 | 7.070e-16 | 2.499e-15 | 2.394e-14 | 2.399e-14 | σ₁ (0.99) | +3.637e-12 | 4.31e-24 | pass |
| | 200 | 7.146480e-16 | −34.8747 | 7.071e-16 | 2.491e-15 | 1.891e-10 | 2.064e-10 | σ₁ (0.99) | −2.213e-12 | 6.77e-20 | pass |
| | 250 | 7.146444e-16 | −34.8747 | 7.071e-16 | 2.491e-15 | 2.631e-10 | 2.873e-10 | σ₁ (0.99) | −2.400e-12 | 9.79e-20 | pass |
| 249.01 | 130 | 7.140593e-30 | −67.1118 | 3.628e-30 | 3.602e-30 | 7.865e-30 | 1.664e-29 | σ₃ (Δ share 0.94) | −9.410e-49 | – | pass |
| | 160 | 7.790547e-18 | −39.3936 | 7.644e-18 | 8.542e-18 | 1.808e-16 | 1.856e-16 | σ₁ (0.95) | −3.289e-09 | 3.70e-22 | **FAIL** |
| | 200 | 7.786999e-18 | −39.3941 | 7.645e-18 | 8.648e-18 | 1.818e-12 | 2.302e-12 | σ₁ (0.95) | −2.877e-09 | 2.65e-16 | pass |
| | 250 | 7.737138e-18 | −39.4005 | 7.572e-18 | 9.159e-18 | 1.814e-12 | 2.298e-12 | σ₁ (0.94) | −2.675e-09 | 1.23e-15 | pass |
| 253.80 | 130 | 4.865133e-33 | −74.4032 | 4.662e-33 | 1.579e-32 | 2.747e-32 | 2.787e-32 | σ₁ (Δ share 0.91) | −4.198e-48 | – | pass |
| | 160 | 9.287446e-19 | −41.5205 | 9.226e-19 | 1.051e-18 | 1.784e-17 | 1.837e-17 | σ₁ (0.98) | −2.555e-06 | 2.28e-20 | pass |
| | 200 | 5.947689e-18 | −39.6635 | 5.920e-18 | 1.009e-16 | 2.215e-13 | 2.846e-13 | σ₁ (0.97) | −2.949e-07 | 3.30e-13 | pass |
| | 250 | 6.258595e-18 | −39.6126 | 6.217e-18 | 6.696e-16 | 2.212e-13 | 2.840e-13 | σ₁ (0.98) | −7.706e-06 | 2.09e-12 | pass |
| 60.00 | 130–250 | 3.522588e-09 | −19.4641 | 5.033e-15 | 5.032e-15 | 5.416e-14 | 5.415e-14 | – (Δ share ≤ 1.1e-9) | −5.082e-13 | 1.76e-27 (vs 100) | pass |

At D 60 every ks gives the same digits: the horizon series has converged before 130 there.

### Post-hoc readings (`posthoc.py`, `posthoc.log`; not criteria, read after the runs)

Each column is a change against ks 250, beside the model's ln f(K) (μ = 1); h1 and h3 are the ks 130 modes, other than
Δ, of harmonic 1 and 3, followed by overlap, beside the model's P(250) for μ 1 and μ 3.

| D | g at ks 160 (ln f) | ln max\|ΔF\| at ks 160, 200 (ln f) | h1 rise / P(250), μ 1 | h3 rise / P(250), μ 3 |
| --- | --- | --- | --- | --- |
| 237.13 | −0.000 (−11.63) | −10.030, −0.369 (−11.63, −0.80) | +18.336 / +41.05 (0.45) | +34.404 / +37.02 (0.93) |
| 249.01 | +0.007 (−17.07) | −15.020, −1.540 (−17.07, −1.90) | +27.034 / +55.79 (0.48) | +40.997 / +48.77 (0.84) |
| 253.80 | −1.908 (−19.63) | −18.335, −1.849 (−19.63, −2.53) | +38.286 / +63.04 (0.61) | +43.783 / +53.95 (0.81) |

- **The horizon residual follows f.** The omitted tail of F grows with ks close to the model's ln f (the table).
- **The harmonic-3 pair nearly follows its own f** (0.81–0.93 of μ 3's P).
- **Δ and the harmonic-1 mode beside it do not.** g (C4: −0.54 to −0.43 of P(200)) and h1 (0.45–0.61 of P(250))
  stop rising by ks 160–200, where the model still has e^−11.6 to e^−19.6 to go. What caps them is not the horizon
  order.

### Why g and σ₃ by index disagree

σ₃ by index is the Δ mode at ks 130 at D 237.13 and 249.01 (Δ share 0.99, 0.94), and a harmonic-3 mode at every ks
from 160 (Δ share 6.8e-5 to 7.5e-3). At D 253.80 it is a harmonic-3 mode at every ks (Δ share 5.6e-3 at 130). So its
rise (+30.165, +39.982, +43.534 to ks 200) mixes two modes at the first two D, and at D 253.80 is the harmonic-3 pair's,
which follows μ 3's model (above) closely enough to fall within 30% of μ 1's P(200). It is not a reading of Δ.

### Discrepancies

1. **C1 fails at D 249.01, ks 160.** σ₁'s relative change over the last two of 16 iterations is 1.35e-3 (bar 1e-3);
   σ₁ and σ₂ are close there (7.644e-18, 8.542e-18). g comes from one transpose solve, not from the iteration, and reads
   −39.3936 against −39.3941 at ks 200; the verdict uses ks 130, 200 and 250 only. Cleared by the rerun below, on the coordinator's word.
2. **g and σ₃ by index disagree** on the verdict (neither, supports), for the reason above.
3. **The model's last digit.** `model.log` gives ln f(130) −63.04 (μ 1, D 253.80), −48.77 (μ 3, D 249.01) and −53.95
   (μ 3, D 253.80); FACTORED_HORIZON.md 4.2's table has −63.05, −48.78 and −53.96.
4. **Δ's step at D 253.80 is not settled in ks.** The pinned step's Δ is −2.555e-06, −2.949e-07 and −7.706e-06 at ks
   160, 200 and 250, while g changes by 0.051 between 200 and 250. M5 estimates |Δ(300) − Δ(130)| ~ 1.4e-7, good to a
   factor 100 (a conjecture), which the ks 250 value is inside; it is a linear estimate at a point that is not a root.
5. **My timing note** (above): I first blamed the pilot's 40 min on the mpmath product; it was the exact Jacobian.

### Recommended tasks

1. **Rerun D 249.01 at ks 160 with `--its=32`.** What: `near_null.py ... --ks=160 --its=32 --jv=od`, one run, about
   30 min on the Mac. Why: C1's only failure, σ₁'s iteration. Acceptance: its check passes with σ₁ converged below
   1e-3 and g within 1e-3 of −39.3936 in ln; fails otherwise. Depends on: #902.
2. **The grip at a root of the raised order, D 253.80.** What: converge #603's D 253.80 state at ks 250 (octo-double
   pinned corrector) and run `near_null.py --ks 250` and `--ks 300` there. Why: this test read g at the stored z, which
   the ks 250 step would move by −7.7e-6 in Δ; #903's restart would work at such roots, and whether g stays near
   e^−39.6 there decides how much grip the restart gains. Acceptance: the corrector converges (its own check), and ln g
   at the new root is reported against −39.6126 with a bar of 1 (a change above 1 says the cap moves with the root);
   the run's near_null checks pass. Depends on: #902, and the math review that blocks #884, #899 and #900.

### Rerun of D 249.01 at ks 160 with `--its=32` (the coordinator's task, 2026-11-16)

`nn_D249_ks160_its32.{log,json}` and `V_D249_ks160_its32.npy` (15:14–15:41 UTC, 5e8b08db, the same command as the
queue's with `--its=32`); the 16-iteration files stay as they were. `cmp_its32.py` compares the two (`cmp_its32.log`):

| reading | `--its=16` | `--its=32` |
| --- | --- | --- |
| near_null check | FAIL | pass |
| σ₁ (converged to) | 7.644355e-18 (1.35e-03) | 7.626499e-18 (7.96e-07) |
| σ₂ (converged to) | 8.541933e-18 (2.09e-03) | 8.573513e-18 (1.27e-06) |
| σ₁'s Δ share | 9.10e-01 | 8.31e-01 |
| ln g | −39.393621 | −39.393621 (bit for bit) |
| pinned step's Δ | −3.288902e-09 | equal |

Its checks pass (the rerun's check, σ₁ below 1e-3, |Δ ln g| < 1e-3). The control `--mutate=self`, which reads the
16-iteration run as the rerun, fails on the first two; the third cannot fail under it, as both runs share one LU.
`sigma.py` on a folder of links with the rerun in place of the 16-iteration run (`sigma_its32.log`) differs from
`sigma.log` only in that run's σ line and passes C1: PASS, verdict neither, g and σ₃ still disagree. σ₁ and σ₂ share
Δ (0.83 and 0.16 at 32 iterations) and are 12% apart, so the 16-iteration σ₁ had not finished separating them.
