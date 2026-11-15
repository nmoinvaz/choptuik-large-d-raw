# I857-mac: the linear return of a Δ move at D 240.1244, rel 1e-83 to 1e-85

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/857

Code: hp/step_spread.py at main 56b87471 (as 5ca54afe, #850), on main 3c35f0c's hpkernel. One process at nice 10, 3
kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). State: I603-win2/chain/anm_pin3_D240.1244.npz in #837's
truth_system. Runs in `queue.sh` order, after I856-mac's queue. The issue's three commands (seed 1), plus one control
run, seed 3 at rel 1e-85.

In progress.

## The added control

The move is 24 orders below the root's own step (the issue, dΔ −4.38e-58). Rounding in the step that does not scale with
the move would bend p and |dev| / move at the smallest rel, and could not then be told from a wrong Δ column. Seed 3's Δ
sign is opposite to seed 1's, so at rel 1e-85 the linear parts of their devs cancel in dev(1) + dev(3). What remains, n
= |dev(1) + dev(3)| / (2 move), is the part of dev that does not flip with the move. That is the quadratic term,
6.538e-5 of the move in `linear.py --selftest`'s planted case (#850's q 1.1027e81), and any rounding floor.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--ref` passes in all four runs (−4.3765436014297066e-58), and `power`'s same-start check passes; its control `power --mutate start` must FAIL | the unperturbed step changes, or the control passes |
| C2 | `linear.py --selftest` passes (a planted linear return passes, one 2% off fails on the ratio, a floor of 1e-2 of the move fails on n); `linear.py` on #850's folder FAILS (quadratic); `--mutate samesign` (dev(1) − dev(3)) FAILS on n | the check misreads a planted case or a control passes |
| C3 | the noise floor: n < 1e-3 at rel 1e-85 | a floor of 0.1% of the move or more, which stops the reading of C4 at 1e-85 |
| C4 | the prediction: the reading is linear (both p in [0.9, 1.1]) and \|dev\| / move in [0.99, 1.01] at each rel (`linear.py`) | not linear, or the ratio outside that range: a wrong Δ column or a wrong quadratic extrapolation (if C3 passes) |
