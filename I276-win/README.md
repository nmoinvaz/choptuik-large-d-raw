# I276-win: #215's d6 and d10 chains from D 214.75 / D 214.5 to D 215.0 in quarter steps

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/276 (continues https://github.com/nmoinvaz/choptuik-large-d/issues/215). Worktree choptuik-t151 at origin/main 22daddc8, venv-t151, 3 threads per chain, below normal. Commands in chain_d6.cmd and chain_d10.cmd (#215's od command, `> log 2>&1`, exit code to chain_*.exit).

| chain | start state (read from I215-win, not copied) | sha256 (first 16) | step |
|---|---|---|---|
| chain_d6 | I215-win/chain_d6/anm_pin3_D214.7500.npz | 3457f46350218e3f | one step, a = 0.25 (room-limited) to D 215.0 |
| chain_d10 | I215-win/chain_d10/anm_pin3_D214.5000.npz | 32276825f7e04d13 | `--h_max 0.25`: D 214.75, then D 215.0 |

Both started 2026-11-10 about 06:47:40 UTC. The series at the start D is recomputed (about 45 min). Stop rules as #215: the driver's three halvings per step, the od stall rule, and a 6 h cap (13:47 UTC).

The assignment (coordinator, #98 comment of 2026-11-10 02:26 UTC) reached this session at 06:44 UTC, after a restart of the win session.
