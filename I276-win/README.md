# I276-win: #215's d6 and d10 chains from D 214.75 / D 214.5 to D 215.0 in quarter steps

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/276 (continues https://github.com/nmoinvaz/choptuik-large-d/issues/215). Worktree choptuik-t151 at origin/main 22daddc8, venv-t151, 3 threads per chain, below normal. Commands in chain_d6.cmd and chain_d10.cmd (#215's od command, `> log 2>&1`, exit code to chain_*.exit).

| chain | start state (read from I215-win, not copied) | sha256 (first 16) | step |
|---|---|---|---|
| chain_d6 | I215-win/chain_d6/anm_pin3_D214.7500.npz | 3457f46350218e3f | one step, a = 0.25 (room-limited) to D 215.0 |
| chain_d10 | I215-win/chain_d10/anm_pin3_D214.5000.npz | 32276825f7e04d13 | `--h_max 0.25`: D 214.75, then D 215.0 |

Both started 2026-11-10 about 06:47:40 UTC. The series at the start D is recomputed (about 45 min). Stop rules as #215: the driver's three halvings per step, the od stall rule, and a 6 h cap (13:47 UTC).

The assignment (coordinator, #98 comment of 2026-11-10 02:26 UTC) reached this session at 06:44 UTC, after a restart of the win session.

## Final state (2026-11-10 15:35 UTC)

Both chains ended on their own, with exit 0 (`chain_d6.exit`, `chain_d10.exit`; the driver's own end, not a kill). The win session was blocked on a question to Nathan from 07:27 to 15:15 UTC, so the coordinator's decision of 07:31 UTC to stop d6 early was not carried out, and the machine was idle from 13:29 UTC.

| chain | ended (UTC) | last saved D | how it ended |
|---|---|---|---|
| chain_d6 | 11:09:09 | 214.75 (the start state, nothing new saved) | `stopped: no convergence after three halvings` |
| chain_d10 | 13:29:27 | 215.0 | `done`, D_max reached |

chain_d10 saved three states (sha256 first 16, saved UTC, Delta from the eight parts summed exactly):

| D | file | sha256 | saved | od line |
|---|---|---|---|---|
| 214.625 | chain_d10/anm_pin3_D214.6250.npz | 5a7d78935d9ec343 | 11:31:30 | 6 steps, converged 2.0e-65 |
| 214.875 | chain_d10/anm_pin3_D214.8750.npz | 3f901a5fa33bdae0 | 12:40:08 | 5 steps, converged 2.0e-68 |
| 215.0 | chain_d10/anm_pin3_D215.0000.npz | 54f53a7d8b729d7c | 13:29:21 | 6 steps, converged 3.5e-65, Delta 1.691559557516578762604339 |

Its way: the first step from D 214.5 asked a = 0.25 (D 214.75) and was not converged after 12 od steps (max|F| 1.2e-21 against tol_od 1e-40, 12349 s, 30 failed projections), so the driver halved to D 214.625. Then D 214.875 (a = 0.25) and D 215.0 (a = 0.125, the room left).

`delta_extrap.py` (output in `delta_extrap.out`): d10's D 215.0 differs from the degree-5 extrapolation of the previous six saved Delta by 2.7e-16 (the six: 211.5, 212.5, 213.5, 214.5, 214.625, 214.875) and by 6.1e-14 (the six at unit spacing, 209.5 to 214.5), both below 1e-12. Its control `--mutate=shift=1e-11` fails (exit 1).

chain_d6: the base polish at D 214.75 did not converge (8 od solves, max|F| 1.54e-34 to 1.6e-19, 31 projections skipped), the series took 2973 s, and the attempts a = 0.25, 0.125, 0.0625, 0.03125 (D 215.0, 214.875, 214.8125, 214.78125) all failed at their start, the re-seed with |R| 16.5, 11.1, 10.8, 11.4.
