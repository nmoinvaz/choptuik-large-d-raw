# I856-mac: Newton's return from a pure Δ move at D 252.6135, rel 1e-68 and 1e-69

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/856

Code: hp/step_spread.py at main 56b87471 (as 5ca54afe, #850), on main 3c35f0c's hpkernel. One process at nice 10, 3
kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). State: I603-win2/chain/anm_pin3_D252.6135.npz in #837's
truth_system. Runs in `queue.sh` order, after I852-mac's queue. The issue's commands, with seed 1 and the same signs
as #850's runs; the power reading takes #850's rel 1e-67 run (`I850-mac/dl_D252_r67.json`, raw 811e84e2).

## Answer

At D 252.6135 the Δ step after a pure Δ move is quadratic over rel 1e-67 to 1e-69 (p 1.9978, 1.9998), and q = dev /
rel² changes by 5.062e-4 from 1e-68 to 1e-69, inside the 1% bar. So #850's reading of "neither" came only from its
1e-65 pair. q settles at −2.686175e89, and its change falls tenfold per decade (+5.090e-3, +5.062e-4), as a third-order
term would.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--ref` passes in both runs (+5.2645963792835124e-82), and `power`'s same-start check passes; its control `power --mutate start` must FAIL | the unperturbed step changes, or the control passes |
| C2 | `qcheck.py --selftest` passes (a planted quadratic passes, one with a 2% cubic term fails on q), and `qcheck.py` on #850's `power.json` FAILS (p 1.6481, q moved 5.381e-2) | the check misreads a planted case or passes #850's |
| C3 | the prediction: both p (1e-67 → 1e-68, 1e-68 → 1e-69) in [1.8, 2.2], and q = dev / rel² within 1% between 1e-68 and 1e-69 (`qcheck.py`) | either p outside the band, or q moves more than 1% |

## Results

| # | verdict | numbers (logs) |
| --- | --- | --- |
| C1 | pass | `--ref` equal in 2 of 2 runs; `power` same start pass; `power_start` FAIL ("the unperturbed step NOT the same in the 3 runs") |
| C2 | pass | `qcheck_selftest` PASS (the 2% cubic case fails on q, −1.957e-02); `qcheck_ctl850` FAIL (p 1.6481, q +5.381e-02) |
| C3 | pass | `qcheck`: p 1.9978, 1.9998 in [1.8, 2.2]; q's change 1e-68 → 1e-69 +5.062e-04 (\|.\| ≤ 0.01) |

`tables.md` (from `tables.py`):

| rel | move | dev | \|dev\| / move | q | smallest pivot / unperturbed − 1 |
| --- | --- | --- | --- | --- | --- |
| 1e-67 (#850) | 1.6845e-67 | −2.671220e-45 | 1.5857e+22 | −2.671220e+89 | −4.185e-04 |
| 1e-68 | 1.6845e-68 | −2.684816e-47 | 1.5938e+21 | −2.684816e+89 | −4.186e-05 |
| 1e-69 | 1.6845e-69 | −2.686175e-49 | 1.5946e+20 | −2.686175e+89 | −4.186e-06 |

q's change per decade: +5.090e-03, +5.062e-04, the second over the first 9.946e-02. The pivot change stays linear in
rel. If the linear part returns the move, it equals the quadratic term at rel_x = 6.271e-90 (an extrapolation).

## Discrepancies

None.

## Recommended tasks

1. **The linear return of a Δ move at D 252.6135, after #857.** What: #857's runs (seed 1 and the seed 3 control,
   `linear.py`) at D 252.6135 at rel 1e-92, 1e-93 and 1e-94, below rel_x 6.271e-90. Start them from a re-converged
   state as #874 makes one, since the stored truth's own step there is 5.2645963792835124e-82 in Δ. Why: it would test
   the Δ column where the weak pivot is 7.2869e-31 rather than 7.3062e-24. Acceptance as #857's: linear (both p in
   [0.9, 1.1]) and |dev| / move in [0.99, 1.01], with n < 1e-3. Fails otherwise. Depends on #857 and #874 (worth
   running only if #857 passes from u2).
