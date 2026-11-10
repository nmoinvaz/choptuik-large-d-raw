# I215-win: #13's degree-6 and degree-10 held-fit chains continued from D 192 (d6) and D 191.5 (d10) toward 215

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/215 (continues https://github.com/nmoinvaz/choptuik-large-d/issues/13). Worktree choptuik-t151 at origin/main 22daddc8, venv-t151, 3 threads per chain, below normal. Commands in chain_d6.cmd and chain_d10.cmd (the issue's commands; log in chain_*.log, exit code in chain_*.exit).

The issue expected the start near D 194 at #13's 24 h cap (03:54 UTC). Nathan asked for the stop earlier (2026-11-09 00:53 UTC, "Give it 15 more minutes and then do the recommended thing"), the coordinator agreed, and each chain was stopped right after a save, so the start states are the last saved ones of #13:

| chain | start state | saved (UTC) | stopped (UTC) |
|---|---|---|---|
| chain_d6 | I13-win/chain_d6/anm_pin3_D192.0000.npz | 2026-11-09 01:30:25 | 01:30:51 |
| chain_d10 | I13-win/chain_d10/anm_pin3_D191.5000.npz | 2026-11-09 01:26:09 | 01:32:26 |

chain_d10 halved its step once (its qd corrector stalled at |F| 1.6e-20 for D 192, then converged at D 191.5), so it starts at D 191.5. Rules as #13: a qd stall above 1e-28 twice in a row means a restart of that chain from its last state with --corrector od --tol_od 1e-40; stop on three halvings, after 24 h, at D 215, or on the hang rule.

chain_d6 switched to the octo-double corrector (2026-11-09 02:50 UTC). Its qd corrector stalled above 1e-28 twice in a row: D 193.0 attempt (a 1.0) ended at max|F| 1.6e-27, "no trial step accepted", and the halved retry (D 192.5, a 0.5) at 1.1e-20, "no trial step accepted" (1142 s). The third attempt (a 0.25) was in its re-seed when the chain was stopped at 02:49:5x UTC (taskkill of launcher 13780 and python 27244; chain_d6.exit holds 1 from that stop). Restart from I13-win/chain_d6/anm_pin3_D192.0000.npz, `chain_d6_od.cmd`: `--corrector od --tol_od 1e-40 --qd_it 12`, everything else as chain_d6.cmd, log appended to chain_d6.log, exit code to chain_d6_od.exit. The series at D 192 (2656 s) is recomputed. chain_d10 stays on qd.

chain_d10 switched to the octo-double corrector (2026-11-09 04:47 UTC). Its qd corrector stalled above 1e-28 twice in a row: the D 194.5 attempt (a 1.0) ended at max|F| 2.4e-28, "no trial step accepted" (6 steps, 1738 s), and the halved retry (D 194.0, a 0.5) at 1.2e-28, "no trial step accepted" (6 steps, 1426 s). The third attempt (a 0.25) had not started when the chain was stopped at 04:47:3x UTC (taskkill of launcher 1244 and python 15372; chain_d10.exit holds 1 from that stop). Restart from I215-win/chain_d10/anm_pin3_D193.5000.npz (sha256 ed6be6e866bf2571…, saved 03:08:23 UTC), `chain_d10_od.cmd`: `--corrector od --tol_od 1e-40 --qd_it 12`, everything else as chain_d10.cmd, log appended to chain_d10.log, exit code to chain_d10_od.exit. Launched 04:47:50 UTC, python 28844, launcher 21456. The series at D 193.5 (2622 s) is recomputed.

## Final state (2026-11-10 02:16 UTC)

Neither chain reached D 215. Both were stopped by me at the coordinator's hard stop (02:15 UTC, amendment on the issue, comment 6752298494), by taskkill of the launcher tree. Run time 2026-11-09 01:33:05 to 2026-11-10 02:16:23 UTC (24 h 43 min).

| chain | last saved D | saved (UTC) | file | sha256 (first 16) | Delta |
|---|---|---|---|---|---|
| chain_d6 | 214.75 | 2026-11-10 02:07:30 | chain_d6/anm_pin3_D214.7500.npz | 3457f46350218e3f | 1.691614384367 |
| chain_d10 | 214.5 | 2026-11-10 00:27:42 | chain_d10/anm_pin3_D214.5000.npz | 32276825f7e04d13 | 1.691669337484 |

chain_d6 also saved D 214.5 (00:21:55, sha256 5a086416418ad7c9, Delta 1.691669337508), the one common D of the two chains at the end (d6 minus d10 = 2.3235e-11, direct).

Exit files: chain_d6.exit = 1 (my stop of the qd run, 2026-11-09 02:49 UTC), chain_d6_od.exit = 1 (my stop of the od run, 02:15:5x UTC Nov 10), chain_d10.exit = 1 (my stop of the qd run, 04:47 UTC Nov 9), chain_d10_od.exit = 1 (my stop of the od run, 02:16:2x UTC Nov 10). None is a chain exit. The driver's own "stopped: no convergence after three halvings" never printed.

The D 215.0 step. Both chains' attempts at D 215.0 failed (a 1.0 from D 214.0 on d6: the start's projection failed, 0 od steps, 90 s; a 0.5 from D 214.5 on both: re-seed FAILED, then 10 failed elimination projections and "no trial step accepted" at |F| 1.3e-09 (d6, 2396 s without output) and 7.2e-09 (d10, 2291 s)). The halved attempts a 0.25 (D 214.75): d6 converged in 5 od steps and saved; d10 was in its second Newton step when stopped, nothing saved. The series prediction of Delta at D 215.0 in anm_run.jsonl (1.69155955754 d6, 1.69155955752 d10) is a prediction, not a result.

Raw files: chain_d6/ (24 states D 193.0 to 214.75, pred_*, anm_run.jsonl), chain_d10/ (23 states D 192.5 to 214.5, pred_*, anm_run.jsonl), chain_d6.log and chain_d10.log (the qd and od runs appended), the commands chain_d6.cmd, chain_d6_od.cmd, chain_d10.cmd, chain_d10_od.cmd. The issue's closing summary has the tables.
