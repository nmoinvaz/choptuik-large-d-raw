# I857-mac: the linear return of a Δ move at D 240.1244, rel 1e-83 to 1e-85

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/857

Code: hp/step_spread.py at main 2283596e (as 5ca54afe for these options), on main 3c35f0c's hpkernel, from the
wip/xf-874 worktree. One process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). Runs in `queue.sh`
order, after I874-mac's queue, from two starts (the coordinator, after #852): the stored truth as written,
I603-win2/chain/anm_pin3_D240.1244.npz (`truth/`), and #874's re-converged state, I874-mac/anm_pin3_D240.1244_u2.npz
(`u2/`), both in #837's truth_system. Each start has the issue's three commands (seed 1) and one control run, seed 3
at rel 1e-85. The acceptance is read on #874's state; the stored truth's runs are reported beside it, and the
difference between the two is the cross term −J⁻¹F''(·, d0) of the truth's offset (#852).

Done: 2026-11-16 00:47 to 03:20 UTC. C1 to C4 pass from u2; C5 is reported below.

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

## Result

From #874's re-converged state, Newton's step returns a pure Δ move linearly and as the move itself. The odd part of
the return at rel 1e-85 is 1 to the double rounding of the ratio (L − 1 = 0), and the even part n = 6.537732e-05 is
#850's quadratic term, read at rel 1e-67, 18 orders above. From the stored truth the return is linear too, but 1.0832
of the move. The difference, +8.324447e-02 of the move at all three rels, is the cross term of the truth's offset.

## Acceptance

| # | verdict | numbers (logs and `tables.md`) |
| --- | --- | --- |
| C1 | pass | `--ref` equal in 8 of 8 runs; `power`'s same-start check passes from each start; `power --mutate start` FAILS from each (`truth_power_start.log`, `u2_power_start.log`) |
| C2 | pass | `linear_selftest.log` PASS (the planted 2% offset fails the ratio, the 1e-2 floor fails n); `linear_ctl850.log` FAILS (p 2.0000, 2.0000); `--mutate samesign` FAILS on n, 1.083e+00 from the truth and 1.000e+00 from u2 |
| C3 | pass | n 6.538e-05 at rel 1e-85 from u2 (< 1e-3) |
| C4 | pass | from u2, p 1.0025, 1.0003 (linear); \|dev\| / move 1.006538, 1.000654, 1.000065 at rel 1e-83, 1e-84, 1e-85 |
| C5 | reported | from the truth, p 1.0024, 1.0002 (linear), \|dev\| / move 1.089782, 1.083898, 1.083310 (outside [0.99, 1.01]); truth less u2 +8.324447e-02 at each rel |

## Readings (`tables.py`, `tables.md`)

- **The linear part.** From u2 the odd part L = |dev(1) − dev(3)| / (2 move) at rel 1e-85 is 1.0000000000, with
  L − 1 = 0 in double. Newton's step at a root returns −J⁻¹J dz = −dz, so this is the expected identity, met to the
  rounding of one double.
- **The quadratic part.** The even part n is 6.537732e-05 from both starts (difference 8.472e-17). #850's quadratic,
  q = dev / rel² at rel 1e-67 (I850-mac/power.json), predicts 6.537732e-05; u2's n less it is +6.42e-12 of it. #850's
  own cubic at 1e-67, read from its last p, accounts for this: after it, u2's n differs by −5.25e-13 of it, inside the
  1.7e-12 bound on the rounding of n from the stored doubles dev(1), dev(3) (a rounding bound, not a spread). So the
  even part at 1e-85 is the quadratic term with no floor above that bound.
- **The cross term.** The truth's |dev| / move less u2's is +8.324447e-02 at rel 1e-83, 1e-84 and 1e-85, with a spread
  over the rels of 0 in double, and the odd parts differ by the same amount. The quadratic parts agree (above), so the
  difference is linear in the move, as −J⁻¹F''(·, d0) is. Divided by the truth's max|d0| / max|z_h| 3.2085e-57, it is
  2.5945e+55 (max norms, a scale, not a fitted coefficient).
- **u2's system.** These runs used #874's code, which reads u2 with held values recomputed from u2 itself. They differ
  from the truth's by at most 1.767e-100 (I874-mac/check_u2.json); #884 changes this. u2's own step, 1.5634e-99 of
  max|z_h|, is the root of that system, and L − 1 = 0 from it.
- **`step_spread`'s verdict lines** read "determined" from the truth and "not determined" from u2. That verdict is the
  spread check's, dΔ(seed) against the unperturbed dΔ at a bar of 1e-3. From the truth the root's own dΔ, −4.38e-58,
  is far above the moves, 1.687e-83 to 1.687e-85. It is not a criterion here.

## Discrepancies

- Against the issue as first written, from the stored truth, C4's ratio fails, at 1.083310 to 1.089782. The
  coordinator's comment on the issue expected this (the cross term), and the criteria were revised to read C4 from u2
  before the runs. The cross term is reported under C5.

## Recommended tasks

1. **The linear return at D 252.6135 (#856's follow-up).** What: re-converge the stored truth at 252.6135 with
   `truth_restep.py store` (with #884's held values), then #857's runs from it and from the stored truth, seed 1 at
   rel 1e-93, 1e-94 and 1e-95, and seed 3 at 1e-95. Why: #856 read a quadratic return there (q −2.686175e+89,
   I856-mac/qcheck.log), and #857 separates the linear and quadratic parts with the seed 1 and seed 3 pair.
   Acceptance: from the re-converged state L in [0.99, 1.01] at 1e-95 and n < 1e-3 there (the floor);
   `--mutate samesign` must FAIL. Depends on: #857, #884.
2. **The cross term is linear in the offset.** What: a state z = u2 + s (truth − u2) in eight parts for s = 1/2 and
   1/4, and #857's seed 1 and seed 3 pair at rel 1e-85 from each. Why: #857 attributes the truth's 8.324447e-02 to the
   cross term −J⁻¹F''(·, d0), which is linear in d0, and this tests that directly. Acceptance: L − 1 within 1% of
   s × 8.324447e-02 for both s; a planted s of 1 must give the truth's L. Depends on: #857, #884.

## Files

- `queue.sh`, `run.sh`: the runs, in order. `truth/`, `u2/`: each start's `dl_D240_r<k>.json`, `power.json`,
  `power_s3.json`. `<start>_<run>.log`: each run's log.
- `linear.py`: the C2 to C4 check, with `--selftest` and `--mutate samesign`.
- `tables.py`, `tables.md`: the readings above, from the JSONs (`python3 tables.py`).
