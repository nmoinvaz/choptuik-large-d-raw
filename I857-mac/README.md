# I857-mac: the linear return of a Δ move at D 240.1244, rel 1e-83 to 1e-85

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/857

Code: hp/step_spread.py at main 2283596e (as 5ca54afe for these options), on main 3c35f0c's hpkernel, from the
wip/xf-874 worktree. One process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). Runs in `queue.sh`
order, after I874-mac's queue, from two starts (the coordinator, after #852): the stored truth as written,
I603-win2/chain/anm_pin3_D240.1244.npz (`truth/`), and #874's re-converged state, I874-mac/anm_pin3_D240.1244_u2.npz
(`u2/`), both in #837's truth_system. Each start has the issue's three commands (seed 1) and one control run, seed 3
at rel 1e-85. The acceptance is read on #874's state; the stored truth's runs are reported beside it, and the
difference between the two is the cross term −J⁻¹F''(·, d0) of the truth's offset (#852).

In progress.

## The added control

The move is 24 orders below the root's own step (the issue, dΔ −4.38e-58). Rounding in the step that does not scale with
the move would bend p and |dev| / move at the smallest rel, and could not then be told from a wrong Δ column. Seed 3's Δ
sign is opposite to seed 1's, so at rel 1e-85 the linear parts of their devs cancel in dev(1) + dev(3). What remains, n
= |dev(1) + dev(3)| / (2 move), is the part of dev that does not flip with the move. That is the quadratic term,
6.538e-5 of the move in `linear.py --selftest`'s planted case (#850's q 1.1027e81), and any rounding floor.

## Criteria (posted on the issue before the runs; revised for the two starts before they ran)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--ref` passes in all eight runs (−4.3765436014297066e-58 from the truth, `I874-mac/check_u2.json`'s dΔ from u2), and `power`'s same-start check passes; its control `power --mutate start` must FAIL, from each start | the unperturbed step changes, or a control passes |
| C2 | `linear.py --selftest` passes (a planted linear return passes, one 2% off fails on the ratio, a floor of 1e-2 of the move fails on n); `linear.py` on #850's folder FAILS (quadratic); `--mutate samesign` FAILS on n, from each start | the check misreads a planted case or a control passes |
| C3 | the noise floor n < 1e-3 at rel 1e-85, from u2 | a floor of 0.1% of the move or more, which stops C4's reading at 1e-85 |
| C4 | the prediction, from u2: the reading is linear (both p in [0.9, 1.1]) and \|dev\| / move in [0.99, 1.01] at each rel | not linear, or the ratio outside that range |
| C5 | reported: the same readings from the stored truth, and \|dev\| / move from the truth less that from u2 at each rel (the cross term) | (reported) |
