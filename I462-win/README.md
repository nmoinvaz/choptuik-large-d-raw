# I462-win: the d10 and d6 held-fit chains past D 215 on chain_fit's D values, with the fixed driver

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/462 (follows #215, #276, #461). Worktree choptuik-t151 at main dd4c70f (the re-seed fix #446, d9e7f78, and the base rule #461, d84cc51), venv-t151 (its build is unchanged: the commits since 22daddc8 change Python, and the Rust edits only add M = 40 to the solver binding), 3 threads per chain, below normal. Commands are #276's per chain with `--od_junk 0 --D_max 400`, in `d10_s1.cmd` and `d6_s1.cmd` (log `chain_*.log`, exit codes `chain_*_s*.exit`).

| chain | start state (read, not copied) | sha256 (first 16) | first steps |
|---|---|---|---|
| chain_d10 | I276-win/chain_d10/anm_pin3_D215.0000.npz | 54f53a7d8b729d7c | `--h_max 0.13125 --steps 1` to D 215.13125 |
| chain_d6 | I215-win/chain_d6/anm_pin3_D214.7500.npz | 3457f46350218e3f | `--h_max 0.25 --steps 1` to D 215.0, then `--h_max 0.13125 --steps 1` to D 215.13125 |

Then from D 215.13125, each chain with `--h_max 1.0 --steps 400` (D 216.13125, ...). Stop rules: the driver's three halvings, D 400, #215's stall rule, and a 24 h cap per chain.

**Reading rule, fixed before the run** (the issue's). At each start the log prints a converged base polish or the line `base polish not adopted`, and the step 0 series line has |z_N| below 1e-25 and a_max above 3, otherwise that chain stops and its lines are reported. Every re-seed line reads `ok`; the first that does not is reported with its rung and residual. A step is accepted when its octo-double Newton line reads converged below 1e-40, and max|F| after the first Newton step of each accepted step is reported.
