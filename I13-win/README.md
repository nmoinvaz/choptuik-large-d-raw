# I13-win: T140 degree-6 and degree-10 held-fit chains continued past D 165 with the octo-double series

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/13 (T152). Worktree choptuik-t151 at origin/main 22daddc8 (hpkernel avx512 and multidouble 4.0.0 avx512), venv-t151, 3 threads per chain, below normal. Start states T140-win/chain_d6/anm_pin3_D165.0000.npz and chain_d10/ (Delta 1.705781623906 and 1.705781623884). Pilots (pilot_d6, pilot_d10): 2 steps each first, then chains (chain_d6, chain_d10, --steps 200, D_max 215). Commands in pilot_*.cmd and chain_*.cmd. Rules: quad-double corrector stalls above 1e-28 twice in a row, restart that chain from its last state with --corrector od --tol_od 1e-40; stop on a three-halvings stop, after 24 h, or at D 215; hang rule (20 min with no log line and one core busy: one py-spy dump, kill, restart from the last state with h_max halved, post).

Pilots (2026-11-08 00:22 to 02:18 UTC), both passed: 2 steps each, 0 halvings, held-fit degree lines printed, qd converged every step (max|F| 7e-33 to 7e-39), no hang. pilot_d6: re-seed 1 ok / 1 failed (D 167 attempt, prediction kept, qd converged, one 708 s corrector), Delta(167.0) 1.705051632762. pilot_d10: re-seed 2 ok / 0 failed, Delta(167.0) 1.705051632739. d6 minus d10: 2.2e-11 at 166.0, 2.3e-11 at 167.0. Octo-double series 2950 to 3030 s per step with both running, corrector and re-seed 1.5 to 12 min, about 57 min per step.
Chains (chain_d6, chain_d10) started 02:19 UTC from the pilots' last states I13-win/pilot_d6/anm_pin3_D167.0000.npz and pilot_d10/ (instead of T140-win's D 165, to keep the pilots' two steps), otherwise the issue's command (chain_*.cmd). Pilot states stay, so the chain rows begin at D 167.

Final state (2026-11-09 01:32 UTC). Nathan asked for the stop early ("Give it 15 more minutes and then do the recommended thing", 00:53 UTC), the coordinator agreed, and #13 closed before its 24 h cap, to continue as #215 (I215-win/). Each chain was stopped (taskkill of the venv launcher and its python child) right after a save. The first run was stopped by Nathan once (restart from D 168 at 03:54:07 UTC on 2026-11-08, chain_*_resume1.cmd), the logs are appended.

| chain | last state | saved (UTC) | stopped (UTC) | Delta at that D |
|---|---|---|---|---|
| chain_d6 | chain_d6/anm_pin3_D192.0000.npz | 2026-11-09 01:30:25 | 01:30:51 | 1.697193549539 |
| chain_d10 | chain_d10/anm_pin3_D191.5000.npz | 2026-11-09 01:26:09 | 01:32:26 | 1.697330862868 |

chain_d10 halved once: its qd corrector stalled at |F| 1.6e-20 for D 192 ("no trial step accepted", not converged), the step was halved and D 191.5 converged at 6.4e-29. Counts over the chain logs: halvings d6 0, d10 1; re-seeds ok / failed d6 22 / 2, d10 25 / 0 (the failed ones keep the prediction).
