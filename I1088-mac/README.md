# I1088-mac: Track B of #1088, the series formulation with the mass mode removed (form S), logs and solutions

Machine: the Mac (Apple M-series, macOS), Python 3.14 venv `venv-314` (numpy 2.5.4, scipy 1.18.1, sympy 1.14.0,
mpmath 1.3.0, python-flint 0.9.0), multidouble's Python package for double-double. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1088. Code: `solver/factored/` on branch `wip/large-d-factored` of
the main repository; notes: `notes/LARGE_D_FACTORED.md` there.

Starting states (read-only, from this repository): `T138-win2/chain/anm_pin3_D100.0000.npz`,
`T138-win2/chain_o/anm_pin3_D200.0000.npz`, `I603-win2/chain/anm_pin3_D245.1366.npz`,
`I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D263.4862.npz`.

| file | what |
|---|---|
| `derive.log`, `derive_mutate_*.log` | `derive_factored.py`: the algebra, each check with its control |
| `check_state_D100*.log` | `check_state.py`: form A's series against hp's D-100 nodes, and the control |
| `check_s_D*.log` | `check_s.py`: form S's slaving at hp's nodes, its series against the nodes, the Hamiltonian check |
| `anchor_noise.log` | form A's a-datum column against n (rounding gain near order n/2) |
| `cond_M6.log`, `cond_M6.jsonl` | `cond_table.py` at M 6 in float64: D 100 solved; jumps to 90..60 not converged |
| `S64_D*_M*.log/json` | `fsolve.py --form=S`, float64 damped Newton |
| `Sdd_D*_M*.log/json` | `solve_dd.py`, double-double split Newton (a json only where the run finished) |
| `cont_M8.log` | `cont.py`: the continuation step 100 -> 105 at M 8 (stopped by an exception in the weak step; not converged) |
| `seed_precision*.log` | `seed_precision.py`: float64 against dd horizon sums at rescaled seeds, D 100..400 |
| `s_noise_D100*.log` | `s_noise.py`: rounding amplification at the D-100 solution, and the rough-noise control |
| `cost.log` | `cost.py`: one residual's cost against D, full and banded (its PASS criterion is for solutions; FAIL at seeds) |
| `jac_check*.log` | `jac_check.py`: dual-number Jacobian against complex step and differences; banded against full |
| `G_D100_Mg32_ju9.log` | `galsolve.py` (fine grid, harmonics to 9): stopped after two split-Newton steps, not converged |

Converged solutions: `Sdd_D100_M8.json` (max|F| 1.9e-22) and `Sdd_D100_M10.json` (1.6e-27), with their float64
starts `S64_D100_M8`, `S64_D100_M10`. Every other solve is a failed attempt, kept as the record of how it failed:
`Sdd_D150_M8` (the jump 100 -> 150), `cont_M8` (100 -> 105), `S64_D200_M8`/`Sdd_D200_M8` (from hp's state, the json
has max|F| 1.2e-5), `S64_D200_M6`, `S64_D245_M6`, `S64_D245_M8`, `S64_D263_M6` (from hp's states), `S64_D200_M10`/
`Sdd_D200_M10` (stopped at max|F| 2e-11, weak residual 4e-14), `G_D100_Mg32_ju9` (stopped). Empty `run_*.out` and
`run_track_b.start` are the drivers' own output files.
