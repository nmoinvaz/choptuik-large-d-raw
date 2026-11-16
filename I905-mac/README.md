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
