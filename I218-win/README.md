# I218-win: the quad-double and octo-double correctors on #13's last chain states

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/218. Worktree choptuik-t151 at origin/main 22daddc8, venv-t151. Started 2026-11-10 06:55 UTC (the assignment, coordinator's #98 comment of 02:26 UTC, reached the session at 06:44 UTC).

The od run of #215 re-corrects its base state, which the qd run saved, so the two correctors are compared on the same state in the logs of #215. `compare_qd_od.py` reads them (`compare_qd_od.out` holds its output, its control `--mutate=shift=5e-18` and its selftest).

| state | in the logs of #215 | what is still to run |
|---|---|---|
| I13-win/chain_d6/anm_pin3_D192.0000.npz | qd and od, chain_d6.log | nothing |
| I215-win/chain_d10/anm_pin3_D193.5000.npz | qd and od, chain_d10.log | nothing |
| I13-win/chain_d10/anm_pin3_D191.5000.npz | qd only (chain_d10.log line 2) | the od polish, `d10_D191.5_od.cmd` (`--steps 0`: the base polish, no series; about 10 min on 3 threads) |

Then `octo_corrector.py planted` and `wall` with their controls (`--mutate_offset qd`, `--mutate 10`), which must fail.

## Closed without the remaining runs (2026-11-10)

The log comparison is `compare_qd_od.out` (d6 D 192.0 passes the 1e-18 bound in Delta, +4.48e-19; d10 D 193.5 fails it, -2.07e-18; both reach od max|F| below 1e-40; the control `--mutate=shift=5e-18` and the selftest behave). On 2026-11-10 15:19 UTC the coordinator asked for the issue's summary as reported and its closing. Not run: the od polish of `I13-win/chain_d10/anm_pin3_D191.5000.npz` (`d10_D191.5_od.cmd` is written and was never launched), and `octo_corrector.py planted` and `wall` with their controls.
