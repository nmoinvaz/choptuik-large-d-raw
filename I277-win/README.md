# I277-win: the octo-double corrector's start residual near D 215 against the step, series only

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/277 (follows #215 and #276). Worktree choptuik-t151 at origin/main 22daddc8, venv-t151, 3 threads per job, below normal. Started 2026-11-10 15:23 UTC, in two lanes of sequential jobs (`laneA.cmd`, `laneB.cmd`).

**Method.** `series_start.py` runs the stock `anm_run.main()` with `--corrector od --qd_it 0` and the options of #215's od chains (`--reseed 2 --reseed_q 1 --jet_o 1 --N 24 --eps 1e-14 --kfreeze 3 --held_fit`), `--steps 1`. Only `anm_run.newton_od` is replaced, and only for `it_max == 0`: the replacement makes `newton_od`'s first call (`s.newton_o(z)` on the same ElimO object, so the same projection, or the same StartNotProjected), prints `start: |F| ...` and takes no step. Every attempt then ends at its start and the driver halves a three times, so one series gives a, a/2, a/4, a/8. The polish of the base is also zero-iteration, so the base is the stored state as it is.

| job | base state (read from I215-win) | h_max | attempts a | logged start residual to reproduce (first `on 0` number, I215 logs) |
|---|---|---|---|---|
| d6_D214.5 | chain_d6/anm_pin3_D214.5000.npz | 0.5 | 0.5, 0.25, 0.125, 0.0625 | a 0.5: 1.34e-9, a 0.25: 3.65e-17 |
| d10_D214.5 | chain_d10/anm_pin3_D214.5000.npz | 0.5 | 0.5, 0.25, 0.125, 0.0625 | a 0.5: 7.23e-9, a 0.25: 1.97e-16 |
| d6_D214.0 | chain_d6/anm_pin3_D214.0000.npz | 0.5 | 0.5, ... | a 0.5 (into D 214.5): 2.46e-20 |
| d6_D205.0 (control) | chain_d6/anm_pin3_D205.0000.npz | 1.0 | 1.0, 0.5, ... | a 1: about 1e-20 |

**Criteria, fixed before the results** (the issue's): the table reproduces each logged start residual within a factor 2, and the D 205.0 control gives about 1e-20 at a = 1. The comparison script's control scales the logged values by 10 and must fail. A projection that fails at the start (`StartNotProjected`) prints no `start:` line, so such an attempt is recorded as its failure, with the `elim projections` counts. Where the logged and the new start residual differ by more than a factor 2 the work stops until the cause is known.

`laneA.cmd`: d6_D214.5, then d6_D205.0, then #218's D 191.5 od polish (`../I218-win/d10_D191.5_od.cmd`). `laneB.cmd`: d10_D214.5, then d6_D214.0. Expected 1 to 1.5 h per job (the series is 45 to 50 min).

## Stopped at the coordinator's word (2026-11-10 15:29 UTC)

The coordinator's message of 15:19 UTC (agent-comms `choptuik-large-d/2026-11-10/151949Z-coordinator-7a2d.md`): #277's question is answered by #446 and #461 (the D 215 wall had three causes), so it is superseded, and if it has started it is to be stopped with what it wrote kept. The win session had not read that message before it launched the lanes at 15:22:40 UTC, because its channel watch was not running. Both lane shells and their children were killed at 15:29:17 UTC (taskkill), 6.5 min in.

What exists: `d6_D214.5.log` and `d10_D214.5.log`, each up to the series computation, which did not finish, so no attempt ran and there are no `.exit` files. The zero-iteration base polish printed `start: |F| 6.32e-36` (d6) and `6.31e-36` (d10). The d10 value equals the start of #276's d10 base polish at the same stored state (6.31e-36, |dz| 2.3e-23), the same computation by two routes. The table of criteria above was not evaluated. `job_d6_D205.0.cmd` and `job_d6_D214.0.cmd` were never launched.
