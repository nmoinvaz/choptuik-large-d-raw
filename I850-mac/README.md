# I850-mac: Newton's return from a pure Δ move at D 240.1244 and 252.6135

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/850

Code: hp/step_spread.py on wip/xf-850 (d78c0a90, from main 4694993d), which adds `--blocks`, `--match`, `--mutate noop`
and the `power` subcommand, on main 3c35f0c's hpkernel. One process at nice 10, 3 kernel threads,
OPENBLAS_NUM_THREADS=1 (`run.sh`). States: I603-win2/chain/anm_pin3_D240.1244.npz and D252.6135.npz in #837's
truth_system. Runs in `queue.sh` order.

## Answer

At D 240.1244 the Δ step after a pure Δ move is quadratic in the move (p 2.0000, 2.0000), with |dev| / move 6.5377e15,
6.5377e14 and 6.5377e13 at rel 1e-65, 1e-66 and 1e-67. So the step's second-order term outweighs the move by 13 to 15
orders, and the linear return of Δ's own column is not seen at these rels. At D 252.6135 the reading is neither
(p 1.6481, 1.9772). There dev / rel² is −1.1274e89, −2.5348e89 and −2.6712e89, settling toward a quadratic as the move's
change of the smallest pivot falls from −4.060e-2 to −4.185e-4.

This is #840's "not explained" ratio (6.5e15 at 240.1, 6.7e23 at 252.6, CRAWL 13): it is the second-order term, not a
failure of the step's linear part. Whether the linear part returns the move is not tested here (recommended task 2).

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `--selftest` passes, and `--mutate=nosub` (the power read without subtracting the unperturbed step) and `power --mutate start` (one run's unperturbed step an ulp off) fail | a planted power is misread, or a control passes |
| C2 | `--blocks centre --seeds 1` at D 240.1244 reproduces #840's centre control (I840-mac/ss_D240.json) with dΔ and max\|F\| equal as doubles (`--match`); `--mutate noop` (seed runs left unperturbed) must FAIL on max\|F\| | the option perturbs the wrong block or nothing, or the control passes |
| C3 | `--ref` passes in every run: −4.3765436014297066e-58 at 240.1244, +5.2645963792835124e-82 at 252.6135 | the unperturbed step changes |
| C4 | `--blocks Delta` at rel 1e-65 reproduces #840's Delta control (seed 1, the same signs) at both D (`--match`) | the new path differs from #840's |
| C5 | per D, the power p of dev = dΔ(seed) − dΔ(unperturbed) at 1e-65 → 1e-66 and 1e-66 → 1e-67: quadratic (both p in [1.8, 2.2]), linear (both in [0.9, 1.1]), or neither; with \|dev\| / move, which an accurate step makes 1 | (a reading, stated per D) |

A linear reading with |dev| / move near 1 is an accurate step. A linear reading far from 1 means the Jacobian does not
return Δ's own column, and a quadratic reading means the step's second-order term dominates the move.

## Results

| # | verdict | numbers (logs) |
| --- | --- | --- |
| C1 | pass | `selftest.log` PASS (4 planted powers read right). `selftest_nosub.log` FAIL, the planted quadratic read p 1.9826, 1.3073. `power_start.log` FAIL, "the unperturbed step NOT the same in the 3 runs" |
| C2 | pass | `ctl_centre_D240.log`: dΔ −4.3765436014297066e-58 and max\|F\| 9.999846920363875e-66, equal to #840's centre control. `ctl_noop_D240.log` FAIL on max\|F\|, 1.713463779201813e-66 against 9.999846920363875e-66 |
| C3 | pass | `--ref` equal in 8 of 8 runs (2 controls, 6 Delta runs) |
| C4 | pass | `dl_D240_r65.log`: dΔ 1.1026706491654993e-49, max\|F\| 1.987897136061064e-34. `dl_D252_r65.log`: dΔ −1.1274425574259287e-41, max\|F\| 1.4416338796697443e-32. Both equal #840's Delta control as doubles |
| C5 | reading | D 240.1244 quadratic, p 2.0000, 2.0000. D 252.6135 neither, p 1.6481, 1.9772 (`power.log`, `power.json`) |

`tables.md` (from `tables.py`, which reads `power.json` and the `dl_*.json` runs) has the rows. dev is exact from
eight parts. q = dev / rel² is the quadratic coefficient.

| D | rel | move | \|dev\| / move | q | smallest pivot / unperturbed − 1 |
| --- | --- | --- | --- | --- | --- |
| 240.1244 | 1e-65 | 1.6866e-65 | 6.5377e+15 | +1.1027e+81 | +2.118e-09 |
| 240.1244 | 1e-66 | 1.6866e-66 | 6.5377e+14 | +1.1027e+81 | +2.118e-10 |
| 240.1244 | 1e-67 | 1.6866e-67 | 6.5377e+13 | +1.1027e+81 | +2.118e-11 |
| 252.6135 | 1e-65 | 1.6845e-65 | 6.6929e+23 | −1.1274e+89 | −4.060e-02 |
| 252.6135 | 1e-66 | 1.6845e-66 | 1.5048e+23 | −2.5348e+89 | −4.174e-03 |
| 252.6135 | 1e-67 | 1.6845e-67 | 1.5857e+22 | −2.6712e+89 | −4.185e-04 |

### Notes

- At 240.1244, q changes by +6.253e-10 and +6.255e-11 per decade, and the move changes the smallest pivot by 2.118e-9
  at most. The Δ move's own quadratic coefficient, 1.1027e81, is far below that of #840's m_h and a_h move,
  dΔ / rel² 2.4200e92 (`I840-mac/tables.md`).
- At 252.6135, q changes by +1.248 and +5.381e-2 per decade (relative), and the second change over the first is
  9.691e-2. That tenfold fall per decade is a third-order term, as is the pivot change, which is linear in rel and
  −4.060e-2 at 1e-65. The second pair's p, 1.9772, is inside the quadratic band, so the reading is "neither" only
  because of the first pair.
- If the move's linear return is the move itself (|dev| / move 1), it would equal the quadratic term at rel_x =
  (move / rel) / |q|: 1.530e-81 at 240.1244 and 6.306e-90 at 252.6135 (`tables.md`). Those are extrapolations of the
  quadratic term, not measurements.
- In C2's no-op control, dΔ was equal as a double (−4.3765436014297066e-58), since the centre move at 1e-65 does not
  change dΔ at that precision. Only max|F| caught the no-op. A `--match` on dΔ alone would have passed it.
- max|F| after the step scales as rel at both D (1.9879e-34, -35, -36 at 240.1244; 1.4416e-32, -33, -34 at 252.6135).

## Discrepancies

None against the text. The ratio CRAWL 13 lists as not explained is reproduced as doubles (C4) and read here as the
second-order term.

## Recommended tasks

1. **Δ return at D 252.6135, rel 1e-68 and 1e-69.** What: `step_spread.py --blocks Delta --seeds 1` at rel 1e-68 and
   1e-69, with `power` over 1e-67, 1e-68 and 1e-69. Why: the reading here is "neither" only because of the 1e-65 pair,
   and q still moves 5.381e-2 per decade. Acceptance: both p in [1.8, 2.2] and q within 1% between 1e-68 and 1e-69.
   Fails when either p is outside the band. Depends on #850 (wip/xf-850's `--blocks` and `power`).
2. **The linear return of a Δ move at D 240.1244.** What: `--blocks Delta --seeds 1` at rel 1e-83, 1e-84 and 1e-85,
   below rel_x 1.530e-81, with `power`. Why: at rel 1e-65..1e-67 the second-order term hides the linear part, so whether
   Newton returns Δ's own column (|dev| / move 1) is untested. Acceptance: p in [0.9, 1.1] at both pairs and |dev| /
   move in [0.99, 1.01]. Fails when the reading is not linear or the ratio is outside that range, which would mean the
   Jacobian's Δ column is wrong. Depends on #850. The move is then far below the unperturbed step (dΔ
   −4.38e-58), so the dev subtraction needs the eight-part sums (`power` reads them).
