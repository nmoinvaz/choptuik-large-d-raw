# I511-win2: where the equilibrated sigma_1's steepening starts, D 228 to 236 (near_null_eq.py --plant=7)

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/511 (follows from #510).
Code: worktree `D:\choptuik-i505` at `origin/wip/i502-subagent` 0cce81e (Python only; interpreter and `hpkernel` build of `C:\Users\nathan\Source\venv-t126`), as in #505 and #510.
Seven states, four at a time (2 threads each, below-normal priority, `run_i511.sh`), then the control `--mutate=rows_only` at D 231.13, which must exit nonzero. Exit codes in `exits.txt`.
States (all under `I461-win2/`): crawlG at D 229.1312, 230.1312, 231.1312, 232.6312; crawlI at D 233.1312, 234.1312, 236.1312. The twelve states of #505 and #510 are tabled with them. Results follow in this README.

## Results (2026-11-11 21:25:13 to 21:37:32 UTC)

Seven runs exited 0 (wave 1 21:25:16 to 21:29:30, wave 2 21:29:30 to 21:33:35 UTC), the control `--mutate=rows_only` at D 231.13 exited 1, as it must (`exits.txt`). The planted check passes at each state (max deviation 3.1e-15 to 6.7e-15, bound 1e-3). `results_511_fit.txt` is `fit_511.py` (selftest ok: a planted break at 232.13 is found with residual 1e-9, a smooth drift of the rate is called gradual) on the nineteen states, #505's four, #510's eight and these seven.

Equilibrated sigma_1 of the new states: D 229.1312 2.0867e-54, 230.1312 5.7023e-55, 231.1312 1.8210e-55, 232.6312 3.2755e-56, 233.1312 1.6574e-56, 234.1312 5.7825e-57, 236.1312 4.4774e-58 (sigma_2..4 in the logs).
Local rates of sigma_1 per unit of D between neighbouring states: 1.027, 0.987, 1.145 (4 apart); then 0.914 (228.13 to 229.13), 1.297, 1.141, 1.010 (231.13 to 232.13), 1.410 (232.13 to 232.63, 0.5 apart), 1.362, 1.053 (233.13 to 234.13), 1.187, 1.371 (235.13 to 236.13), 1.029 (236.13 to 237.13), then 1.292, 1.287, 1.286.
The two-rate fit (continuous, a break at each state D with two states on each side): the best candidate break is D 231.13 (rates 1.061 below, 1.239 above), sum of squares 0.2665, largest residual 0.2984 in ln sigma_1; second best D 230.13 with 0.2741 (ratio 1.03); on a 0.05 grid D 230.68 (1.056 and 1.236, sum 0.2578). The one-rate fit has sum 3.218. The rule (largest residual below 0.02 and the best break better by a factor 2 over the second best): neither holds, so **the steepening is gradual by the rule**. What the fit shows is that a broken line explains 92% of the one-rate sum and puts the break at D 230 to 232, but the unit-spaced local rates scatter by +-0.2 about it (0.91 to 1.41), a residual 15 times the rule's bound.
