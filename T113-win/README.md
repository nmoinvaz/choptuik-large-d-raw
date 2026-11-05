# T113-win: the large-D chain from the Mac's T114 state with the prediction in quad-double

hp from main on multidouble 2.1.0 (worktree ..\choptuik-t112, build of 612eb2d, highm_check.py from main 5cbc0fa5), plain corrector, no reseed, `--pred_q 1`, 4 threads, below normal. Cloud task 2026-11-05 14:46 UTC, start state from the cloud's 19:59 UTC entry (jets_inputs check passed, exit 0). Command in t113.cmd, log chain.log, states in chain/.

Ended at 20:17 UTC, step 0, "stopped: no convergence after three halvings" (exit 0, 12 min). The base polish from the stored D 135.0559 state did not converge (|F| 3.52e-12 to 2.3e-12 in 4 steps, no trial step accepted), then a = 1, 0.5, 0.25, 0.125 each stopped at qd 1 step, predicted |F| 2.4e-04, 3.7e-11, 2.8e-11, 3.6e-11. No state saved.

Restart 20:2x UTC (cloud 20:21 UTC entry): from the original start anm-mac/pred_q/A2/anm_pin3_D128.5559.npz, the 14:46 command unchanged. The attempt from T114's D 135.0559 is kept as chain_from135.log, chain_from135/ and t113_from135.cmd (the restart recomputes the plan, so the stored state did not polish). New run: chain.log, chain/, t113.cmd.
