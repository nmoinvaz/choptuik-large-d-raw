# I215-win: #13's degree-6 and degree-10 held-fit chains continued from D 192 (d6) and D 191.5 (d10) toward 215

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/215 (continues https://github.com/nmoinvaz/choptuik-large-d/issues/13). Worktree choptuik-t151 at origin/main 22daddc8, venv-t151, 3 threads per chain, below normal. Commands in chain_d6.cmd and chain_d10.cmd (the issue's commands; log in chain_*.log, exit code in chain_*.exit).

The issue expected the start near D 194 at #13's 24 h cap (03:54 UTC). Nathan asked for the stop earlier (2026-11-09 00:53 UTC, "Give it 15 more minutes and then do the recommended thing"), the coordinator agreed, and each chain was stopped right after a save, so the start states are the last saved ones of #13:

| chain | start state | saved (UTC) | stopped (UTC) |
|---|---|---|---|
| chain_d6 | I13-win/chain_d6/anm_pin3_D192.0000.npz | 2026-11-09 01:30:25 | 01:30:51 |
| chain_d10 | I13-win/chain_d10/anm_pin3_D191.5000.npz | 2026-11-09 01:26:09 | 01:32:26 |

chain_d10 halved its step once (its qd corrector stalled at |F| 1.6e-20 for D 192, then converged at D 191.5), so it starts at D 191.5. Rules as #13: a qd stall above 1e-28 twice in a row means a restart of that chain from its last state with --corrector od --tol_od 1e-40; stop on three halvings, after 24 h, at D 215, or on the hang rule.

chain_d6 switched to the octo-double corrector (2026-11-09 02:50 UTC). Its qd corrector stalled above 1e-28 twice in a row: D 193.0 attempt (a 1.0) ended at max|F| 1.6e-27, "no trial step accepted", and the halved retry (D 192.5, a 0.5) at 1.1e-20, "no trial step accepted" (1142 s). The third attempt (a 0.25) was in its re-seed when the chain was stopped at 02:49:5x UTC (taskkill of launcher 13780 and python 27244; chain_d6.exit holds 1 from that stop). Restart from I13-win/chain_d6/anm_pin3_D192.0000.npz, `chain_d6_od.cmd`: `--corrector od --tol_od 1e-40 --qd_it 12`, everything else as chain_d6.cmd, log appended to chain_d6.log, exit code to chain_d6_od.exit. The series at D 192 (2656 s) is recomputed. chain_d10 stays on qd.
