# I1088-mac: Track B of #1088, the series formulation with the mass mode removed (form S), logs and solutions

Machine: the Mac (Apple M-series, macOS), Python 3.14 venv `venv-314` (numpy 2.5.4, scipy 1.18.1, sympy 1.14.0,
mpmath 1.3.0, python-flint 0.9.0), multidouble's Python package for double-double. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1088. Code: `solver/factored/` on branch `wip/large-d-factored` of
the main repository; notes: `notes/LARGE_D_FACTORED.md` there.

Starting states (read-only, from this repository): `T138-win2/chain/anm_pin3_D100.0000.npz`,
`T138-win2/chain_o/anm_pin3_D200.0000.npz`, `I603-win2/chain/anm_pin3_D245.1366.npz`.

| file | what |
|---|---|
| `derive.log`, `derive_mutate_*.log` | `derive_factored.py`: the algebra (parity variables, singular combinations, beta, horizon recurrence, centre recurrence, cancellation, the fast mode at x*), each check with its control |
| `check_state_D100.log` | `check_state.py` on the D 100 state: form A's series against hp's nodes |
| `check_s_D100.log`, `check_s_D100_mutate_*.log` | `check_s.py`: form S's slaving at hp's nodes, its series against the nodes, the Hamiltonian equation order by order |
| `anchor_noise.log` | `anchor_noise.py`: form A's a-datum column against n (rounding gain near order n/2) |
| `cond_M6.log`, `cond_M6.jsonl` | `cond_table.py` at M 6 in float64 (form S solved; form A evaluated at S's state) |
| `Sdd_*.log`, `Sdd_*.json` | `solve_dd.py`: collocation layout, dd split Newton |
| `G_*.log`, `G_*.json` | `galsolve.py`: fine tau grid, few unknown harmonics, dd split Newton |
