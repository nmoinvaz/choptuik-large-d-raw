# I856-mac: Newton's return from a pure Δ move at D 252.6135, rel 1e-68 and 1e-69

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/856

Code: hp/step_spread.py at main 56b87471 (as 5ca54afe, #850), on main 3c35f0c's hpkernel. One process at nice 10, 3
kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). State: I603-win2/chain/anm_pin3_D252.6135.npz in #837's
truth_system. Runs in `queue.sh` order, after I852-mac's queue. The issue's commands, with seed 1 and the same signs
as #850's runs; the power reading takes #850's rel 1e-67 run (`I850-mac/dl_D252_r67.json`, raw 811e84e2).

In progress.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--ref` passes in both runs (+5.2645963792835124e-82), and `power`'s same-start check passes; its control `power --mutate start` must FAIL | the unperturbed step changes, or the control passes |
| C2 | `qcheck.py --selftest` passes (a planted quadratic passes, one with a 2% cubic term fails on q), and `qcheck.py` on #850's `power.json` FAILS (p 1.6481, q moved 5.381e-2) | the check misreads a planted case or passes #850's |
| C3 | the prediction: both p (1e-67 → 1e-68, 1e-68 → 1e-69) in [1.8, 2.2], and q = dev / rel² within 1% between 1e-68 and 1e-69 (`qcheck.py`) | either p outside the band, or q moves more than 1% |
