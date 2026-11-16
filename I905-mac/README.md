# I905-mac: the adjoint split of the chain's departure past D 245, psi = J^-T e_Delta at #603's states

Machine: the Mac (Apple M5), up to 4 threads at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/905

Code: `hp/adjoint_split.py` on branch wip/xf-905. States: `I603-win2/chain/anm_pin3_D245.1366.npz` (the control) and `anm_pin3_D250.1676.npz`.

The hpkernel build is the #523 one, the one #842 used. Python is venv-314 with PYTHONPATH set to the i599/site2 build. Every run is `python3 adjoint_split.py ... --threads=4` at nice 10.

## Planted test (`planted.log`, `planted_diag.log`), D 245.14

`planted` at 99d72445 failed, and so did both mutations, which was expected. `planted --diag --eps=1e-40,1e-45,1e-50` at 1b8367ca locates the cause. The transposed and plain solves agree exactly, and the Newton step's Δ equals −ψᵀF to 6e-40. Central-difference errors scale as ε³ along e_Δ and along two random unit directions: 1.44e-20 → 1.44e-35 from ε = 1e-40 to 1e-45. So J is F's derivative, and F's cubic term is about 1e100 along e_Δ as ψ sees it. That puts the full system's linear range near |δz| ~ 1e-50. At ε = 1e-50 the octo-double addition loses the move itself: the e_Δ move came out as 9.35e-51, and one random move's Δ came out 0.

## The control at D 245.14

| run | file | ψᵀδF | predicted Δ shift | Newton (#696) | verdict |
|---|---|---|---|---|---|
| A1, ks131p against plan, chain state | `control_245.log` | +4.9231e-11 | −4.923e-11 | +3.825e-13 | fails |
| A1b, plan against stored, chain state | `control_245.log` | −2.3745e-14 | +2.3745e-14 | +2.374e-14 | agrees |
| A1′, ks131p projected (horizon data re-solved, moved 3.8e-37) | `control_245_proj.log` | +4.9231e-11 | −4.923e-11 | +3.825e-13 | fails |
| A0′, zero control: P z against z | `control_245_proj.log` | −1.3e-53 | | | clean |
| order 132 from r131k: full term, and w = 1/16 | `slope132.log` | −3.7211e-12 | +3.72e-12, and /16 = +2.33e-13 | +3.302e-13 at w = 1/16 (#744) | fails the 10% bar (−30%), right sign |
| r130k's state: ks131 / ks132 | `r130k.log` | +4.9201e-11 / +7.6588e-10 | | | |

The weakest pivot and |ψ| at D 245.14:

| state | ks, plan | smallest pivot | \|ψ\| |
|---|---|---|---|
| chain (I603) | 130, stored 61 steps | 1.1e-26 | 7.95e26 |
| r130k (I696) | 130, new 23 steps | 1.1e-26 | 7.95e26 |
| r131k (I696) | 131, new 23 steps | 8.6e-26 | 1.20e26 |

The order-131 term raises the weakest pivot 8×, and the plan does not move it. So the horizon order changes the weak mode's stiffness, which a first-order split cannot follow.

## D 250.17, every setting (`a2_250.log`)

|ψ| is 7.18e29 and the smallest pivot 1.1e-29. The base checks pass: max|F| 3.0e-61, the step's Δ to 1.5e-35, the transposed and plain solves identical. chain − series is +1.804e-9 (#805, `I805-mac/table.json`).

| setting | max\|δF\| | ψᵀδF (share of chain − truth) | split shown linear |
|---|---|---|---|
| plan made again at 1e-32 / 1e-36 | 7.5e-36 / 5.8e-36 | −3.0443e-10 / −3.0376e-10 | yes, at 245.14 (plan) |
| kc 170 | 1.3e-91 | +1.5e-95 | interior rows |
| kt 40 | 1.7e-45 | −5.5e-21 | interior rows |
| held fit d6 / d10, carried from 73.0 (values moved 7.1e-7 / 7.4e-6) | 9.3e-7 / 8.9e-6 | +4.3301e-10 / −1.2516e-9 | yes, at 231.13 (below) |
| ks 131 / 132 | 1.7e-37 / 1.5e-36 | +1.19e-7 / +1.45e-6 | no |
| ks 140 / 160 / 200 / 300 (and 300 on its own plan) | 1.9e-30 / 1.1e-21 / 1.3e-15 / 8.3e-15 | −1.55 / +7.3e8 / +9.5e14 / +3.0e14 | no |

## The held control at D 231.13125 (`held_231.log`)

#603's d8 state is solved with the held values carried by #608's d6 and d10 states at the same D. |ψ| is 9.4e20 and the smallest pivot 1.3e-20.

| held values from | predicted Δ shift | the states' Δ difference | verdict |
|---|---|---|---|
| I608-dh610/chain_d6 | +3.9565e-11 | +3.95652e-11 | agrees |
| I608-dh610/chain_d10 | +1.4102e-11 | +1.41011e-11 | agrees |
| held6 / held10, anchored at 73.0 | the same δF and products | | the anchor reproduces the states' held values |

## Reading

The first-order split reproduces Newton's response for the plan (245.14, 4 digits) and for the held values (231.13, 4–5 digits). For the horizon order it fails at 245.14, where one more order lifts the weakest pivot 8×. At 250.17, the settings whose split is shown linear sum to −3.0e-10 + (+4.3e-10 for d6, or −1.25e-9 for d10) = +1.3e-10 or −1.55e-9. Neither is within a factor 2 of +1.8e-9, so none of them is the source.

The horizon order's linear response is 66 times the departure for order 131 alone, and it is unbounded past that. That is evidence, not a share: it makes the horizon order the setting the weak direction amplifies. The held values' linearity is shown at 231, not at 250. M 48 against 32 is not split, because the octo-double kernel is M = 32 only and #636's M 48 solve did not converge at 240.12.

## Recommended tasks

1. **The held degree at D 250.17 by Newton.** What: at #603's 250.17 state, Newton at fixed D with the held values of data/held_fit_d6.json and data/held_fit_d10.json carried from 73.0, using `anm_run.py --held_fit` and the state as the base. Why: the adjoint predicts Δ shifts of −4.33e-10 and +1.25e-9 there, 9–25 times #805's extrapolated 5e-11. The split's held linearity is shown only at 231, where |ψ| is 1e9 times smaller. Acceptance: both shifts within 10% of the adjoint's, or the report says the held response is nonlinear at 250. Depends on #905. It overlaps #805's recommended task 3.
2. **The weak pivot along the horizon order at D 245.14, as input to #902.** What: the smallest pivot, and |ψ| from `adjoint_split.py run`, at the stored ks 131 and 132 states and at #744/#783/#796's weighted rungs, w = 1/16 … 1. Why: one order lifts it 8× (1.1e-26 → 8.6e-26), and #902 asks whether raising the horizon order lifts the weak pivot. Acceptance: p_min against the order or weight, with the ks 130 state reproduced at 1.1e-26, its control. Depends on #905, #744 and #796's states.
