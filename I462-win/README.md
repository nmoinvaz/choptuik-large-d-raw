# I462-win: the d10 and d6 held-fit chains past D 215 on chain_fit's D values, with the fixed driver

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/462 (follows #215, #276, #461). Worktree choptuik-t151 at main dd4c70f (the re-seed fix #446, d9e7f78, and the base rule #461, d84cc51), venv-t151 (its build is unchanged: the commits since 22daddc8 change Python, and the Rust edits only add M = 40 to the solver binding), 3 threads per chain, below normal. Commands are #276's per chain with `--od_junk 0 --D_max 400`, in `d10_s1.cmd` and `d6_s1.cmd` (log `chain_*.log`, exit codes `chain_*_s*.exit`).

| chain | start state (read, not copied) | sha256 (first 16) | first steps |
|---|---|---|---|
| chain_d10 | I276-win/chain_d10/anm_pin3_D215.0000.npz | 54f53a7d8b729d7c | `--h_max 0.13125 --steps 1` to D 215.13125 |
| chain_d6 | I215-win/chain_d6/anm_pin3_D214.7500.npz | 3457f46350218e3f | `--h_max 0.25 --steps 1` to D 215.0, then `--h_max 0.13125 --steps 1` to D 215.13125 |

Then from D 215.13125, each chain with `--h_max 1.0 --steps 400` (D 216.13125, ...). Stop rules: the driver's three halvings, D 400, #215's stall rule, and a 24 h cap per chain.

**Reading rule, fixed before the run** (the issue's). At each start the log prints a converged base polish or the line `base polish not adopted`, and the step 0 series line has |z_N| below 1e-25 and a_max above 3, otherwise that chain stops and its lines are reported. Every re-seed line reads `ok`; the first that does not is reported with its rung and residual. A step is accepted when its octo-double Newton line reads converged below 1e-40, and max|F| after the first Newton step of each accepted step is reported.

## Restart with --base_polish 0 (2026-11-10 16:10 UTC)

The first start (15:31 UTC, main dd4c70f) was stopped at 16:09:53 UTC, in the base polish of both chains, on the coordinator's word (agent-comms `choptuik-large-d/2026-11-10/160918Z-coordinator-be13.md`): a reloaded state near D 215 starts a few 1e-36 off because the held values are taken again from its first two parts, so the polish is lost time (d10's D 215.0 state: 3.86e-36, then 7.80e-19 after its first step at lam 1/32; d6's D 214.75 state repeated #276's polish to three digits). Nothing was saved. The logs `chain_d10.log` and `chain_d6.log` keep those lines, followed by a `=== restart` line.

Both chains restart with the same commands plus `--base_polish 0` (in `d10_s1.cmd` and `d6_s1.cmd`), on main 718ca35 (`hp/anm_run.py` only, Python; the venv build is unchanged), and every later restart of this task uses it. **The reading rule changes in one line:** at each start the log prints `base polish skipped (--base_polish 0): the stored state is the base`, then the step 0 series line with |z_N| below 1e-25 and a_max above 3. The rest of the rule stands.


## Start rule, a_max bound (2026-11-11 17:57 UTC, coordinator 175746Z)

The start rule above (the step 0 series line has a_max above 3) is now a_max above 2.0, the bound of the step verdicts. Reason: a_max falls smoothly with D on every chain (win_d10 3.110, 2.976, 2.917 at bases D 227.13, 228.13, 229.13; 2.444 on crawlJ at D 242.36), the series radius shrinking with n and not a bad start. The |z_N| bound of 1e-25 stays. win_d10 was left running at its step 0 a_max of 2.917 (message 175651Z, answer 175746Z).


## End of the task (2026-11-11 21:27:44 UTC)

Both chains of the resume (16:27:43 UTC, `d6_long3.cmd` and `d10_long3.cmd`) ended at their 5 h cap, `run_capped` exit 124 in `chain_d6_long3.exit` and `chain_d10_long3.exit` (written 21:27:44 UTC). `chain_*_long2.exit` (1073807364, 11:12:19 UTC) is the record of the Windows Update restart that killed the first long run.

| chain | last converged state | Delta | saved (UTC) | what the cap ended |
|---|---|---|---|---|
| win_d6 | chain_d6/anm_pin3_D232.1312.npz, D 232.13125 | 1.68808082466 | 21:11:41 | the series of the next step, from D 232.13125 |
| win_d10 | chain_d10/anm_pin3_D231.6312.npz, D 231.63125 | 1.68817514541 | 20:27:28 | solve 1 of the step D 231.63125 -> 232.63125 at a=1 (its solve 0 took 4.09e-33 to 7.02e-27) |

win_d10's step D 231.13125 -> 232.13125 at a=1 was refused at 20:15:15 UTC (the octo-double Newton did not converge, `no trial step accepted`, max|F| 1.4e-27); the driver halved to a=0.5 and converged at D 231.63125. The prediction files of both attempts are `chain_d10/pred_pin3_D232.1312.npz` (a=1, refused) and `chain_d10/pred_pin3_D231.6312.npz` (a=0.5). The coordinator (agent-comms `choptuik-large-d/2026-11-11/201728Z-coordinator-3e90.md`) calls this the signature of win2's chain at D 242.5 (#499).
