# I502-mac: singular values of the equilibrated pinned system at D 242.3642, layouts 0.3-0.7 and 0.3-0.8

Machine: the M5 Mac (subagent), 2 threads under nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/502 (depends on #488, #489, #493).

Code: `hp/near_null_eq.py` at choptuik-large-d 6df3f3c (branch `wip/i502-subagent`; its next commit, 0cce81e,
changes only the docstring), interpreter venv-314 (Python 3.14, its installed `hpkernel`). Each run is
`run_eq.sh <worktree>/hp RAW STATE TAG [options]`, which writes `TAG.log` and `TAG.json` and appends its exit and wall
time to `exits.txt`.

States: `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (0.3-0.7, L 769, #488) and
`I489-mac/renode_L1_horizon_D242.3642.npz` (0.3-0.8, L 897, #489, #493). Both get the plan near_null.py makes,
`s.plan(z, 1e-32, 0.05)`.

## Runs

| tag | state | options | exit | what it shows |
|---|---|---|---|---|
| `L07_plant7` | 0.3-0.7 | `--plant=7` | 0 | sigma of the three scalings; planted check 1.05e-14, pass; forward check 1.000000, pass |
| `L08_plant7` | 0.3-0.8 | `--plant=7` | 0 | the same at 0.3-0.8; planted 8.88e-15, pass; forward 1.000000, pass |
| `L07_ctl_rows_only` | 0.3-0.7 | `--plant=7 --mutate=rows_only --jv=0` | 1 | control: the planted check fails, as it must |
| `L07_ctl_sigma` | 0.3-0.7 | `--mutate=sigma` | 1 | control: the forward check fails (0.952381), as it must |

## Result: sigma_1..4 of D_r J D_c, Curtis-Reid + Ruiz (every row and column of max-norm 1)

| | 0.3-0.7 | 0.3-0.8 | 0.8 / 0.7 |
|---|---|---|---|
| sigma_1 | 1.8825e-61 | 1.4235e-56 | 7.6e4 |
| sigma_2 | 9.3856e-61 | 1.9109e-54 | 2.0e6 |
| sigma_3 | 2.6498e-59 | 2.7718e-54 | 1.0e5 |
| sigma_4 | 2.4555e-57 | 4.5224e-53 | 1.8e4 |
| sigma_1, Curtis-Reid alone | 1.3300e-59 | 6.4837e-55 | 4.9e4 |
| sigma_1, Ruiz from J (not scaling-invariant) | 1.5896e-60 | 7.1596e-56 | 4.5e4 |
| raw sigma_1 (near_null, #488, #493) | 2.551e-27 | 8.433e-38 | 3.3e-11 |
| largest \|J_ij\| | 2.4e37 | 3.1e23 | 1.3e-14 |

The components of each vector, in the scaled unknowns and as the direction D_c v in z, are in the logs and the json.

## explore/

Why the script uses neither Ruiz's iteration from J nor the 2-norm scaling. `dumpJ.py` wrote the f64 leading part of
the 0.3-0.7 Jacobian (`dumpJ_L07.log`; its `J0`, compressed, is `J0_L07.npz`). `explore_2norm.py J0_L07.npz`
(`explore_2norm.log`) shows that Ruiz's 2-norm iteration converges like 1/k (largest |1 - 2-norm| 4.06e-6 after 2e5
iterations, 8.33e-7 after 1e6). It also shows that Newton's Hessian for the same balancing, with u_0 held, has
eigenvalues -4.5e-15 and 4.9e-11 against a largest of 31.
