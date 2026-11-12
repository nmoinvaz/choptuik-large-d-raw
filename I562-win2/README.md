# I562-win2: the control arm, crawlJ's D 242.3642 state re-noded to last node 0.975, its pinned step and the plain base polish

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/562 (the control arm; the refined start, the main arm, is the coordinator's code and follows).
Code: worktree `D:\choptuik-i562` at main 80b5056 (`near_null.py` with the pinned step and `--keep_plan=1`), Python only, venv-t126.
(1) `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,0.975 --threads 4` on `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (its check must pass; the control `--mutate sign` once). (2) `near_null.py ... --keep_plan=1 --threads=4`: sigma_1..4 and the pinned step's |dz|, max|dz|, share on V and Delta part, as #501 tabled them at 0.8. (3) The plain base polish of that start: crawlJ's `anm_run.py` options with `--steps 0 --save_base 1`, 8 threads, capped at 2 h (`run_i562.sh`). Exit codes in `exits.txt`. Results follow in this README.

## Results so far (2026-11-12 07:33 to 07:37 UTC)

**(1) The renode to nodes 0.3, 0.4, 0.5, 0.6, 0.975** (`renode_0975.log`): exit 0, check pass (node 0.975 refined by block 5, the horizon series, rows 1.67e-16 -> 0.00; the gap between the horizon series and the Taylor steps 4.9e-36 in p, 4.8e-36 in m, 2.1e-36 in c). The start's pinned max|F| is 1.62e-34, all of it in the horizon block's p rows for harmonics k <= 3 (1.65e-34), the same as at the 0.3-0.8 start. The control `--mutate sign` exited 1 (check FAIL) as it must.

**(2) `near_null.py --keep_plan=1 --threads=4`** (`nn_0975.log`, `nn_0975.json`; check pass: sigma_1 converged to 0e+00, ||J v_1|| / sigma_1 = 1.000000; octo-double LU 99 s, pivots 1.1e-36 to 4.3e+02):

| sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|
| 1.348e-37 (the Delta direction, delta share 1.00) | 7.399e-35 | 7.412e-35 | 1.842e-34 |

The pinned step (dz + J^-1 c, the base polish's step), against the same step at the 0.3-0.8 start (#501):

| start | max abs dz | 2-norm of dz | Delta part | V^T dz (v_1 ... v_4) | share on span(V) |
|---|---|---|---|---|---|
| 0.3-0.975 (here) | 1.683e-01 | **1.657** | -1.423e-02 | -6.99e-02, -6.94e-02, -3.46e-03, **+1.65** | 1.0000 |
| 0.3-0.8 (#501) | 1.68e-01 | 1.73 | +7.62e-02 | -2.7e-02, -6.8e-02, -1.2e-02, +1.72 | 1.0000 |

The step of newton_o (dz = -J^-1 F) is max 1.690e-01, 2-norm 1.657, Delta -1.424e-02, the same V^T dz. **The pinned step is of order 1 at 0.975, as at 0.8**: 1.657 of it lies on v_4 (the harmonic-1 mode of p and m at every node, sigma_4 = 1.842e-34), and the start's own horizon residual 1.62e-34 divided by sigma_4 is about 1, as at 0.8 (1.62e-34 / 1.77e-34). The residual and sigma_4 are nearly independent of the last node, so the layout does not change the first step: the outer layout does not polish as it is, by this measure.

**(3) The plain base polish.** With crawlJ's options and `--steps 0 --save_base 1` (the default `--tol 1e-20`) anm_run.py exited 0 after 1 s **without polishing** (`polish_0975_default_options_skipped.log`): it polishes only if the double-double |F| of the start (3.5e-29, printed on the "base" line) exceeds `--tol`, and it does not. At the 0.3-0.8 start #489 saw the polish run, so its |F| there was above 1e-20. The control is therefore run with `--tol 1e-30` added (everything else crawlJ's, 8 threads, `timeout 7200`, `polish_forced.log`, started 07:34:49 UTC). Its outcome follows below.

**(3) The plain base polish, with `--tol 1e-30` (`polish_forced.log`, 07:34:49 to 07:44:35 UTC, 7.6 min wall at 8 threads, exit 0).** The log reads:

```
the base keeps its stored plan (49 steps)
  on 0: |F| 1.62e-34, |dz| 1.7e-01: no trial step accepted, stopping
      elim projections {'u0': 0, 'u0q': 9, 'ladder': 0, 'failed': 0, 'skipped': 1}
      octo-double Newton: 1 steps, max|F| 1.6e-34, not converged; double-double |F| of its first two parts 3.5e-29
base polish not adopted (max|F| 1.6e-34 -> 1.6e-34): the stored state is the base
```

So the polish makes **one Newton step, with max|F| 1.62e-34 at its start; no trial step is accepted (the step's |dz| 1.7e-01, the pinned step of (2)), the Newton stops not converged at 1.6e-34, and the polish is not adopted**: the stored state stays the base and nothing is saved. This is the expected failure. At the 0.3-0.8 start #489's polish had not finished its first step in 2.6 h on the Mac (2 threads); here, at 8 threads, the same first step ends in 7.6 min with every trial rejected, which is the same outcome (order-1 step, no acceptable trial) found faster. With the default `--tol 1e-20` the polish is not attempted at all (`polish_0975_default_options_skipped.log`).
