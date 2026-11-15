# I842-mac: arclength continuation around the fold, the planted test (chain runs follow on dh370 or dh610)

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
