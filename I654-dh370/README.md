# I654-dh370: the 0.975 last node on the exact projector, polish and a chain leg beside #603 (the dh370 run of #654)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/654 (moved from win2 to dh370 by the coordinator, 2026-11-13).
Code: choptuik-large-d main at 37c7955c (a descendant of 141d9d48), worktree `choptuik-large-d-654`, run in the venv of `choptuik-large-d-614` (the 3c35f0c build, multishoot 1.2.2, multidouble 4.2.1);
hp/src, hp/Cargo.* and hp/pyproject.toml are unchanged between 3c35f0c and 37c7955c, and so is hp/python.
Start state S: `I603-win2/chain/anm_pin3_D252.2497.npz` (sha256 f9ee739b78cbd097..., #603's newest converged state in the raw repository at fd59b5b2, step 40, D 252.2497), read in place.
#603's flags: `I603-win2/run_603.sh`.

## Result: the base polish at 0.975 does not converge, so steps 3 and 4 are not run

The task says to stop and report the step history when the polish does not converge below 1e-60. It stopped at max|F| 3.8e-20 after 11 Newton steps, 94 min wall (`base.log`, exit 0), and was not adopted (the stored state is the base, so `base/` holds no saved base).

### Step 1: renode of S to 0.3, 0.4, 0.5, 0.6, 0.975 (`start/renode.log`, 4 s, exit 0)

| | |
|---|---|
| S | I603-win2/chain/anm_pin3_D252.2497.npz, D 252.2496697, nodes 0.3 to 0.7, pinned max\|F\| 6.61e-92 (horizon>n4 block) |
| the check | pass (the refined node's rows 2.06e-16 -> 0) |
| control `--mutate sign` (`start/ctl_sign.log`) | exit 1, check FAIL (rows 2.06e-16 -> 4.12e-16) |
| gap at node 0.975, horizon series minus Taylor steps | p 7.22e-37, m 7.18e-37, a 1.79e-39, c 4.82e-37 |
| the start's pinned max\|F\| | 7.22e-37, all in the block n3>n4 (the 0.6 to 0.975 segment); every other block below 1e-98 |

### Step 2: the polish (`polish654.sh`, `base.log`), #603's flags with `--steps 0 --save_base 1 --tol 1e-30`

| step | \|F\| before -> after | \|dz\| before -> after | lam | dDelta | smallest pivot | s |
|---|---|---|---|---|---|---|
| 0 | 7.22e-37 -> 3.25e-06 | 2.14e-02 -> 5.92e-06 | 0.125 | +7.11e-03 | 4.6e-07 | 780 |
| 1 | 3.25e-06 -> 8.51e-09 | 5.92e-06 -> 8.50e-09 | 1 | +8.29e-07 | 2.6e-11 | 197 |
| 2 | 8.51e-09 -> 3.28e-18 | 8.50e-09 -> 3.09e-17 | 1 | +4.17e-10 | 5.7e-19 | 177 |
| 3 | 3.28e-18 -> 1.64e-18 | 3.09e-17 -> 1.55e-17 | 0.5 | -3.09e-17 | 2.9e-19 | 364 |
| 4 | 1.64e-18 -> 8.21e-19 | 1.55e-17 -> 7.72e-18 | 0.5 | -1.55e-17 | 1.4e-19 | 354 |
| 5 | 8.21e-19 -> 4.11e-19 | 7.72e-18 -> 3.83e-18 | 0.5 | -7.72e-18 | 7.2e-20 | 355 |
| 6 | 4.11e-19 -> 2.05e-19 | 3.83e-18 -> 1.86e-18 | 0.5 | -3.83e-18 | 3.6e-20 | 354 |
| 7 | 2.05e-19 -> 1.03e-19 | 1.86e-18 -> 8.20e-19 | 0.5 | -1.86e-18 | 1.8e-20 | 355 |
| 8 | 1.03e-19 -> 5.13e-20 | 8.20e-19 -> 1.90e-19 | 0.5 | -8.20e-19 | 9.0e-21 | 355 |
| 9 | 5.13e-20 -> 3.85e-20 | 1.90e-19 -> 2.83e-20 | 0.25 | -1.90e-19 | 6.7e-21 | 541 |
| 10 | 3.85e-20, no trial step accepted (nine trials from lam 1 to 0.0039) | 2.83e-20 | | | | 1603 (trials only) |

Every Newton step costs about 177 s (an octo-double trial at 12 threads); 20 trials were refused, 3 of them (step 0, lam 1, 0.5, 0.25) with max|F| NaN. The largest pivot is 5.7e+02 throughout.
The polish's own line: `base polish not adopted (max|F| 7.2e-37 -> 3.8e-20): the stored state is the base`.
