# I461-win2: the fixed re-seed (main d9e7f78) on Windows, then the crawl past D 215.03 with it

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/461 (follows from #446).

Worktree `D:\choptuik-i446`, detached at d9e7f78, made from `D:\choptuik-large-d` (whose own checkout stays at 188853c). Interpreter `venv-t126`
(Python 3.12.8; its `hpkernel` is `_hpkernel.cp312-win_amd64.pyd` built 2026-11-05 22:51 local, avx2, with the octo-double `Solver` entries; multidouble
Python package f092018). The newest commit touching `hp/src` on main is 1bad14f (M = 40 in the binding), after that build; the coordinator ruled at
08:20 UTC that it changes nothing for M = 32 and that part A runs with the venv as it is. `import reseed` from the worktree's `hp/` works.

Part A (`run_i461_a.sh`, 4 threads, the six runs one after the other): logs `A_<n>_*.log`, exits `exits.txt`.

## Part A result (2026-11-10 08:26 UTC)

Part A ran 2026-11-10 08:21:41 to 08:26:31 UTC (`exits.txt`), six runs one after the other at 4 threads beside #296's 18. `verdict_461_a.py` (`--selftest` ok:
required verdicts pass, a must-PASS that FAILs, a control that PASSes, an exit code that disagrees with the verdict and a missing log each give the
expected exit), output in `verdict_461_a_result.txt`, exit 0: **part A passes, all six as required**.

| run | must | win2 | on the M5 Mac |
|---|---|---|---|
| checkq d6 D 215.0 | PASS | PASS, u0 residual 8.78e-32 (64 s) | 8.78e-32 |
| the same, `--sweeps 1` (control) | FAIL | FAIL, stops at 1.21e-06 (12 s) | 1.21e-06 |
| checkq d6 D 209.0 | PASS | PASS, 1.07e-32 (66 s) | 1.08e-32 |
| checkq the crawl's D 215.0344 prediction | PASS | PASS, 6.89e-32 (64 s) | not run there |
| truthq d6 D 214.5 | PASS | PASS, error left 5.62e-63 in m_h, 1.14e-64 in a_h (68 s) | 5.6e-63, 1.1e-64 |
| the same, `--sweeps 1` (control) | FAIL | FAIL, error left 1.20e-32 in m_h, 1.83e-32 in a_h (16 s) | 1.2e-32 |

Every number agrees with the Mac's to the digits the issue gives, except the D 209.0 residual, 1.07e-32 against 1.08e-32, a last-digit difference at the
quad-double floor (the limit is 1e-24). The build: worktree `D:\choptuik-i446` at d9e7f78, `venv-t126`, `hpkernel` `_hpkernel.cp312-win_amd64.pyd` built
2026-11-05 22:51 local, multidouble Python package f092018. Logs `A_*.log` print every rung (the first pass at u 0.3 reads NOT converged and the repeated
block steps bring it to the floor).

## Part B result (2026-11-10 10:23:39 to 13:12:20 UTC)

`run_i461_b.sh`, 18 threads, worktree `D:\choptuik-i446` at d9e7f78 (the fixed re-seed), from the crawl's last state `I19-win2/crawl/anm_pin3_D215.0312.npz`.
It stopped itself with `stopped: no convergence after three halvings`, exit 0, wall 10121 s (`exits.txt`). Files: `crawlB.log` (67 lines), `crawlB/`
(`anm_run.jsonl` with the step 0 record and its four refused attempts, the four predictions `pred_pin3_D*.npz`), `compare_461_b_result.txt`
(`compare_461_b.py`, selftest ok, exit 1 because no step past D 215.03125 was accepted, which the issue's reading rule makes the result).

**No step was accepted. Every re-seed line reads ok.**

| attempt | target D | re-seed | start residual | Newton steps | last residual | last lam | elim projections (ladder / failed / skipped) | wall |
|---|---|---|---|---|---|---|---|---|
| a 0.1 | 215.13125 | ok, 18.4 s | 2.14e-20 | 3 | 1.2e-17 | 0.0039 | 2 / 25 / 1 | 1029 s |
| a 0.05 | 215.08125 | ok, 18.8 s | 4.89e-20 | 5 | 1.4e-17 | 0.0039 | 4 / 39 / 1 | 1635 s |
| a 0.025 | 215.05625 | ok, 18.1 s | 4.85e-20 | 7 | 1.5e-17 | 0.0039 | 6 / 50 / 1 | 2136 s |
| a 0.0125 | 215.04375 | ok, 18.4 s | 5.44e-20 | 12 | 1.5e-17 | 0.0039 | 12 / 80 / 1 | 3602 s |

The projection counts of `u0` and `u0q` are 0 in all four. The corrector's first step is |dz| 1.1e-06, 5.4e-07, 2.7e-07, 1.3e-07 (lam 0.0039, 0.0078,
0.0156, 0.0312) and lifts the residual from its start (2.1e-20 to 5.4e-20) to 5.4e-18 to 5.8e-18, after which it climbs to 1.2e-17 to 1.5e-17, just above the 1e-17
limit for accepting a stall. The step 0 line reads |z_N| 1.21e-10, ratios 2-5 24.5 1.3 1.6 1.7 and a_max 0.474 (the crawl's step 7 line at the same D reads
2.37e-30, 274.8 247.7 236.2 229.7 and 3.414). The start-up polish of the stored D 215.03125 state took max|F| from 4.42e-36 to 1.47e-18 over 12 iterations
without converging and `anm_run.py` adopted it as the base; this run is the control of the rule that does not adopt such a polish (part B2, below).

## Part B2 (running since 2026-11-10 13:12:42 UTC)

`run_i461_b2.sh`: part B's command with the base-polish rule of main's branch `fix/base-polish-not-adopted`, commit d84cc51 (one commit on 62e725d,
`hp/anm_run.py` only), worktree `D:\choptuik-i446` detached at d84cc51, output `crawlB2/`, log `crawlB2.log`, 18 threads, no `--base_adopt`. Two lines
must print before the first attempt: `base polish not adopted (max|F| 4.4e-36 -> 1.5e-18): the stored state is the base` and the step 0 line
`pivots 7.2e-16..2.3e+30, |z_1| 4.37e-04, |z_N| 2.37e-30, ratios 2-5 274.8 247.7 236.2 229.7, a_max 3.414`. Results follow at the end of the run.

## Parts B3, B4, B5 (the chain, running)

B3 (`run_i461_b3.sh`, `--od_junk 0 --h_max 1.0`, 14:13:54 to 15:51:07 UTC, stopped by the coordinator to raise `--qd_it`), B4 (`run_i461_b4.sh`, `--qd_it 40`, 15:51:31 to 17:14:41 UTC) and B5
(`run_i461_b5.sh`, 17:14:59 UTC on, from B4's last state) are one chain from D 215.13125, each starting from the previous run's last saved state, all at d84cc51 (see `exits.txt`).
`table_461_c.py` makes the step tables and the watcher events (its selftest checks the crawl's accepted steps against `delta_all.csv`).

**`crawlB4.log` is incomplete after 17:12:27 UTC.** A `git pull --rebase --autostash` of mine in this clone replaced the file under the running process, which went on writing to the
replaced file. The lost log lines are those of the last attempt of B4 (a 0.5 from D 231.13125 to D 231.63125: Newton iterations 6 to 7, the Newton and result lines). The run, its states and
`crawlB4/anm_run.jsonl` were not affected; the jsonl has that attempt (8 Newton steps, accepted). B4 was killed at 17:14:41 UTC and B5 started from its last state with a fresh log.
