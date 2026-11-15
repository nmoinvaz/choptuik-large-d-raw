# I875-mac: #852's horizon contraction from the re-converged root at D 240.1244

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/875

Code: hp/step_spread.py at main 2283596e (`--steps`), on main 3c35f0c's hpkernel, from the wip/xf-874 worktree. One
process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). State: #874's
`I874-mac/anm_pin3_D240.1244_u2.npz` in `truth_system`. Runs in `queue.sh` order, after I857-mac's queue.

In progress.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--ref` passes (the unperturbed dΔ at #874's state, from `I874-mac/check_u2.json`) | the unperturbed step changes |
| C2 | `gain.py --selftest` passes (a planted quadratic gain passes; one with #852's linear gain 9.306e3 fails), and `gain.py` on #852's `steps_D240.json` FAILS (it does: gain 9.3060e3 at 1e-96) | the check misreads a planted case or passes #852's |
| C3 | the prediction, at the first step: gain e_1 / e_0 below 1 at 1e-96 and above 1 at 1e-90, and gain / rel at 1e-90 within 10% of 7.5556e92 | any of the three fails |
| C4 | reported: the unperturbed path's own steps from #874's state, and e_2 | (the floor) |
