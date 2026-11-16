# I842-mac: arclength continuation around the fold, the planted test and the chain adapter's Mac runs (the chain runs on win2)

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/842.
Code: `hp/arclength.py` on branch `wip/xf-842` (112a5ece, then 6387aaf8, which rescales check (d)), venv-314 (Python 3.14, mpmath 1.3.0). One process, nice 10.
The design and its amendments are registered on the issue before the runs.

## The plant (`plant/`)

`cd hp && python3 arclength.py plant --out=plant.json > plant.log` (mpmath 50 digits, N 24, eps 1e-30, corrector to 1e-40, 60 steps at most), and `python3 arclength.py selfcheck > selfcheck.log`, which runs the plant and its two controls.

| check | bar | result | verdict |
|---|---|---|---|
| (a) every converged point on the truth curve | 1e-30 | 51 points, worst 5.9e-40 | pass |
| (b) both branches | ≥ 2 points with σ ≤ −0.3 and ≥ 2 with σ ≥ +0.3 | 20 and 18 | pass |
| (c) the turn, from the step that contains it (step 26, from the edge base) | 1e-10 | \|D − D*\| 2.7e-40, \|x − x*\| 2.9e-41 | pass |
| (d) composed series against the bordered recursion, per order | ≤ 100 × 1e-50 × cond_k | worst ratio 0.019 | pass |
| control `--border 0` (D-series, corrector at fixed D) | must fail (b) | 30 points with σ ≤ −0.3, 0 past the turn; no turn | fails, as it must |
| control `--mutate compose` (q_k without its m ≥ 2 terms) | must fail (d) | ratio 1e48 | fails, as it must |

The edge base (coordinator's note 2): step 25 ends where the series' |t_D| = 0.05, and step 26 starts from it. There the composition's condition number reaches 8.6e47. Its coefficients differ from the bordered recursion's by up to 9.9e-5 relative at the top orders, inside (d)'s bar of 100 × 1e-50 × cond. Its step still converges in one iteration (predicted max|F| 7.7e-33), and the turn is located from its series to 2.7e-40, since s* = 0.033 weighs the high orders little.

The block elimination (coordinator's note 1): over all 51 corrector iterates, |t_D − ⟨t_z, b⟩| ≥ 1.6 with |b| ≤ 20, and |den| ≈ |b| at every iterate. Along the branch b ≈ −dz/dD and den ≈ 1/t_D, so the elimination's loss factor |b| |t_z| / |den| stays near 1. The loss that remains is J's own.

`plant/run1/`: the first run, at 112a5ece. The plant passed there too, but the control `--mutate compose` did not fail (d): its z_k = 0 made (d)'s bar, scaled by the composed series' condition number, infinite. Check (d) now scales the difference and the condition number by the bordered recursion's coefficients (6387aaf8), and its control fails.

## The chain adapter's smoke test (`smoke/`)

`anm_run.py --arclength 1` at e78779bb from chain_nsr's state at D 259.8875 (I603-win2/chain_nsr, raw 1b80022b), with chain_nsr's flags, but N 4, `--steps 1` and 4 threads. It ran 5.2 h and did not converge.

| attempt | a | start max\|F\| (after the re-seed) | \|b\| at the start | \|b\| at the first iterate | outcome |
|---|---|---|---|---|---|
| 1 | 1.50e-6 | 8.4e9 | none | none | re-seed failed |
| 2 | 7.52e-7 | 3.8e-31 | 0.0135 | 0.1419 | chord to 1.2e-46, then 11 steps at λ = 1/2, ending at 2.0e-36 |
| 3 | 3.76e-7 | 1.2e-32 | 0.0137 | none | one step, no trial accepted |
| 4 | 1.88e-7 | 3.7e-34 | 0.553 | 0.1419 | chord to 4.5e-46, then 11 steps at λ = 1/2, ending at 9.1e-38 |

After the chord, the bordered Newton step is 2.55e-26 (attempt 2) and 2.53e-29 (attempt 4), almost all in Δ. At the same stage, chain_nsr's fixed-D corrector takes 1.7e-40 (I603-win2/chain_nsr.log, its step from 259.8875). Each λ = 1 trial then rises to max|F| ≈ 1.8e35 δΔ², the Δ curvature that chain_nsr's own full steps show too (5.5e-45 after a 1.74e-40 step). λ = 1/2 is accepted with θ = 0.50, and the next step is half the last. The denominators t_D − ⟨t_z, b⟩ stay at 0.96–1.01.

## The adapter's diagnostic at the base (`diag/`)

`--arc_diag 1` at d5bf8536: the polished base (max|F| 3.3e-72) and the same flags.

| check | result | verdict |
|---|---|---|
| fixed-D Newton step at the base | 4.3e-60 | OK, chain_nsr's level |
| bordered step at s = 0, BorderedCore and BorderedElim | 4.3e-60 each, dD 6.6e-61 (rounded to 0), den 1.0100 | OK, equal to the fixed-D step |
| b = J⁻¹F_D against −w₁ of the order-1 series | \|b\| 0.14192 against 0.14192, equal | OK, but not independent: both come from F_D through the same LU |
| F_D formed before and after the factorization | identical | OK |
| the four weakest singular values, J against the bordered matrix | 5.72e-38, 1.21e-36, 4.91e-35, 5.02e-35 against 5.78e-38, 1.21e-36, 4.91e-35, 5.02e-35 | the border adds no weak direction |
| F_D against central differences, h 1e-22 and 1e-26 | relative 1.9e-3 and 1.9e-11, worst in the horizon block (row 670) | the error scales as h², so F_D is the derivative |

So at the base the adapter is consistent, and 0.1419 is the right \|b\|. The start's 0.0135 and 0.553 are J's at the predicted point: with σ_min 6e-38 against pivots up to 1.5e37, a point 1e-30 off the root sees different weak directions.

The smoke test's starts (3.8e-31 to 3.7e-34) all lie above the level that chain_nsr's corrector converges from. In its log a start at 5.0e-34 is refused at the chord (θ 1.01), and starts at 6.5e-36 and 3.7e-36 converge in 4 steps. At N 4 the predictor cannot reach that level even at a = 1.9e-7, so the failure is laid to the predictor's order (a hypothesis, which the N 24 pilot tests).

One point to watch: F_D's central-difference error scales as h² with a coefficient that puts the horizon block's D-scale near 1e-21 at fixed z. So a D move inside the corrector must stay small, or be followed by the projection.

## Pilot 1, N 24 from chain_nsr's D 259.8875 (`pilot1/`)

Command: chain_nsr's flags at `--threads 4 --qd_it 12`, with `--steps 1 --arclength 1 --a0 0.00097`, code wip/xf-842 d5bf8536. chain_nsr runs `--qd_it 20`; the 12 here was a slip. The series took 5131 s and is saved as `arcjet_000_D259.887490.npz`. Pilot 2 reads it back with `--arc_jet`.

The run did not converge, and the cause is the bordered D move. It was stopped in attempt 2, at 04:14 UTC on 2026-11-16, so `arc.jsonl` holds only the header line.

| quantity | chain_nsr, same step (log I603-win2 step 100) | pilot 1, attempt 1 (a 0.00097, D 259.888449719) |
|---|---|---|
| start max\|F\| | 3.7e-36 | 1.07e-35 |
| first step \|dz\| | 6.5e-35 | 1.86e-31, all Δ: 0.134·dD for dD ≈ 1.4e-30, about one double-double ulp of D |
| chord's full first step, max\|F\| | 6.5e-34 | 3.8e-27, about 2e33·dD² |
| after the chord | 2.9e-48, then λ = 1 steps of 6.9e-40 and 3.5e-54, converged 2.7e-72 | 1.7e-47, then a 6.8e-32 step in Δ |
| λ = 1 trials | accepted | 1.0e-27, 2.5e-28, 6.3e-29, 1.6e-29 (∝ \|dz\|², ratio 4.0), refused |
| λ = 1/2 trials | none | F halves exactly at every iterate: 12 iterates to 8.5e-51, not converged |
| attempt 2 (a/2) | | start 3.3e-36, the same crawl from 1.95e-49 |

The bordered step's denominators stayed at 1.01-1.02. |b| was 0.234 at the start and 0.147 after.

The border adds no weak direction (`diag/`: σ_min 5.72e-38 for J, 5.78e-38 bordered). chain_nsr's fixed-D corrector converges at this D with the same pivots, 5.7e-37..1.5e37. So the crawl is the D move's, not the system's weak pivot.

The fix is wip/xf-842 6d71cec5, `--arc_dhold 1e-12`: D is held, taking the fixed-D step, when the bordered dD is at most 1e-12.
