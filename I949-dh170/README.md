# I949-dh170: the Δ mode's σ along the order-tied chain, its slope in D and the fold

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/949

## Setup

- Worktree `~/Source/choptuik-large-d-935` at main 787f1006, its 4.8.2 `.venv` (hpkernel on multidouble 4.8.2 / multishoot 3.2.0 /
  multisolver 0.1.1, Python multidouble package 482c6835). `hp/near_null.py` is unchanged since c714694a.
- Command per state: `near_null.py ~/scratch949 STATE --k=6 --its=16 --threads=4 --json=NAME.json`, two at a time, nice 10
  (`run949.sh lane N`, reads `queue949.txt`, writes `exits_949.txt`). Each state is read on its stored plan.
- States: win2b's `I903-win2/ks_chain/leg*/anm_pin3_D*.npz`, copied by `sync949.sh` byte for byte from the committed blobs of
  origin/main of the raw repository into `~/scratch949/` (same paths), so a raw pull cannot move them.
- Tracker: `track949.py` reads the JSONs and writes `track949.csv` (one row per state: D, ks, σ_Δ, σ_pair, Δ share, convergence,
  local slope −d ln σ_Δ/dD over the two neighbours) and `intervals949.csv` (the slope per consecutive pair). The five states #941
  read are taken from its JSONs (copied to `from941/`, I941-dh370 9da736f7), not read again, except two re-reads below.

## Definitions

- Classification as in #941's `analyze941.py` (copied into `track949.py`): the Δ mode is the vector with the largest Δ share (it must
  exceed 0.5), σ_pair is the geometric mean of the two vectors whose two largest components are (p1, 3) and (m_h, 3). A state
  that does not classify is flagged and read by hand.
- Local slope at state i: −ln(σ_{i+1}/σ_{i−1}) / (D_{i+1} − D_{i−1}). An interval's slope is −ln(σ_{i+1}/σ_i) / (D_{i+1} − D_i), the
  quantity #941 quotes (0.412, 0.410, 0.407, 0.405). An interval that crosses a leg boundary (ks changes) is marked and not
  used for any trigger or fit.

## Pass criteria, written before any state was read

| # | check | pass |
|---|---|---|
| 1 | `near_null.py --planted=1` on this build (order-tied chain state D 229.0509, ks 240) | exit 0, planted check pass |
| 2 | the same with `--mutate=scale_block` | exit 1, planted check FAIL |
| 3 | planted fold fit, D* 260 and 262 (`fold949.py --selftest`) | D* within 0.05 of the planted value, on three grids |
| 4 | its mutation (`--selftest --mutate`, a wrong fold law) | exit 1 |
| 4a | the validity rule's planted checks (fold 1 unit past: valid; 5 past: fails c2; sixth state off: fails c3 alone; 2.9 past with scatter: fails c4 alone; no fold: no window valid) | pass, and the mutation fails |
| 5 | slope over D 229–232 reproduces #941's 0.405–0.412 | each interval's slope within 0.01 of #941's, from the five states (two re-read here, bit-compared) |
| 6 | every state's σ_Δ converged | relative change over the last two iterations below 1e-3, else rerun with `--its=32` |
| 7 | null control on the backfill's five-state windows (rule above) | no window valid, ks 211's D* 212.8 fails by condition 2 |
| 8 | the baseline frozen before leg 8's first read | `baseline949.json` committed before any ks 250 state is read (the freeze refuses otherwise) |

## The rule (coordinator, issue #949 comment of 2026-11-17 23:18 UTC, fixed before leg 8's first read)

My readings of the issue's first text (the fit cannot be the literal linear one, because the planted series has the exponential in
it; the trigger cannot be the literal 0.10, because the baseline slope is 0.4 to 0.5) were adopted, and then the rule was made exact:

- **Baseline.** s(ks) is the least-squares slope of ln σ_Δ against D over each backfill leg (ks 211, 220, 230, 240, five or more states
  each), fitted as a + b/ks and frozen in `baseline949.json` (`track949.py --freeze`, which refuses once a state of ks ≥ 250 has been
  read) before leg 8's first read. For ks ≥ 250 it is extrapolated, and the spread against a line in ks is reported.
- **Trigger.** An interval's slope (−d ln σ_Δ/dD between a state and the previous state of the same leg) minus s(ks) above 0.10 at
  three consecutive states of one leg.
- **Fold fit** (`fold949.py`, model B): σ_Δ² = c (D* − D) e^(−2 s D) with c, D*, s free on the five latest states of one ks. Valid only if
  (1) every relative residual of σ_Δ² is within 10%, (2) D* is past the last state by no more than 3 units, (3) the window moved back
  by one state gives D* within 0.3, (4) 400 planted series with the same D points, the frozen s and a Gaussian scatter of 0.03 in the
  interval slope (ln σ error 0.03 h/√2 per state) return the fit's own D* within 0.3 at the 16th and the 84th percentile.
- **Null control.** The rule on every five-state window of the backfill's legs must return no valid fold, and ks 211's D* of 212.8 must
  fail by condition 2. A window that passes stops the work until the cause is known.
- A fold is claimed only from a valid fit with the trigger fired. A later state that contradicts it is reported, not fitted around.

Why the issue's first text needed the change (`noise949.log`, `selftest949.log`): the literal linear fit misses a planted fold with the
exponential in it (D* 232 to 240, residuals 0.4 to 1.0); at 1e-3 relative noise on σ model B's D* is within 0.5 at 10 units from the fold
and undetermined at 28; and ks 211's five states gave a "valid" fit by the 10% rule alone with D* 212.8, which the chain's later states
(the same slope to D 232) refute.

## Post-freeze reports (coordinator, hc 2026-11-18 about 05:56 UTC; the frozen rule stands, the trigger is unchanged)

- **Ladder and chain 2.** win2b raises the order at D 237.43 by a +10 ladder (ks 260, 270, 280, bases `I903-win2/ks_chain/ladder8/ks*/base_pin*.npz`)
  and then runs on at ks about 275 in `I903-win2/ks_chain2/`. Every base and state is read as it is pushed (`sync949.sh`,
  `queue_new949.py`). `track949.py` keeps the ladder rows out of the chain's slopes and prints them as a table against the chain's state at
  the same D (what #948 did at D 232.0, where σ_Δ is the same from ks 240 to 320).
- **Caveat for every post.** #948 showed σ_Δ is the same from ks 240 to 320 at D 232, so the baseline's ks dependence was really D
  dependence along the chain. At the jump to ks 275 the frozen s(ks) (0.3364 at ks 275) reads about 0.04 below the D-trend, so an apparent
  excess near +0.04 there is not a fold. The 0.10 trigger is unaffected.
- **The slope against a D-trend line, labeled post-freeze.** `track949.py` also fits the backfill's 20 same-ks interval slopes against D
  (a line and a parabola, at each interval's midpoint) and prints each interval's slope minus them beside the one minus the frozen s(ks)
  (`postfreeze_*` columns of `track949.csv`). It is a report, not the trigger. Its fits are not frozen before leg 8; they are made
  from the backfill alone.

## Plan change (coordinator, hc 2026-11-18 about 07:30 UTC)

win2b's ks 260 rung at D 237.53 did not converge (ks 250 there is already below the needed order), so there are no `ladder8` bases. The chain
restarts from #948's converged ks 280 base at D 232.0 (`I948-dh370/up_K280_from270/base_pin3_D232.0000.npz`) in `I903-win2/ks_chain2`, with a
steeper order rule (about ks 291 for D 232 to 242). Its states are read as they come. They overlap leg 8's ks 250 states at D 232 to 237.5, so
`track949.py` prints, at equal D, σ_Δ and σ_pair at ks 291 against ks 250 (the ORDER EFFECT table: the same D where a D agrees to 1e-6,
else a cubic interpolation of ln σ through the four nearest ks 250 states, whose error is estimated by leaving each interior state out). The
two chains are kept apart: no interval, slope, trigger or fold window crosses from one chain to the other. The frozen baseline
extrapolates poorly to ks 291 (s = 0.3088 there, about 0.09 under the D-trend), so the excess against s(ks) can sit near the 0.10 trigger without
a fold; the post-freeze D-trend comparison stays beside it, and a fold needs a valid fit and an excess against the D-trend too.

## Amendment for ks_chain2 (coordinator, issue #949 comment of 2026-11-18 07:35 UTC, before any of its states was read)

The frozen s(ks) gives 0.309 at ks 291, about 0.09 under the chain's D-trend, so the trigger could fire from the baseline alone (and at ks 300 it
would: `selftest_track949.log`). For ks_chain2 the trigger's baseline is the backfill's linear D-trend as published, s(D) = 0.9692 − 0.00245 D
(`dtrend_frozen949.json`; the exact fit is 0.0011 to 0.0013 higher), at each interval's midpoint. The trigger (excess above 0.10 at three
consecutive states of one leg), the fold fit and its validity rules are otherwise unchanged, and s(ks) is still printed beside it. Leg 8 of
ks_chain keeps the original rule.

## Requests of 2026-11-18 about 21:00 UTC (coordinator, hc)

- **σ_pair's slope**: `track949.py` prints σ_pair's interval slope of ln per state beside σ_Δ's (`pair` column; `pair_interval_slope` in
  `track949.csv`; −d ln σ_pair/dD over the interval ending at the state, positive where the pair falls), a reading and never a trigger.
- **σ_pair against win2b's re-seed failures** (from base D 236.7, `I903-win2/refused903.txt`): `pair_reseed949.py` (`pair_reseed949.log`)
  lists each attempt's base D, σ_pair there, the pair's slope into it, the step factor a, the result and the quad-double polish's R.
- **ks_chain3** (dh370's #966, `I966-dh370/ks_chain3`, ks 304 and up, restarting past D 238): `sync949.sh` and `queue_new949.py` read its states
  when they are pushed (none yet, only the log), `track949.py` keeps it as chain 3 apart from the others, with the ks_chain2 trigger baseline
  (the frozen D-trend) applied to it as well, which is my assumption, said in the posts, and its ORDER EFFECT against ks_chain2's ks 291 at equal D
  where the D's agree.

## The σ_pair reading rule (coordinator, hc 2026-11-18 about 22:50 UTC, fixed before more states came)

σ_pair has fallen since D 237.4 with a growing slope and its fold fit does not hold still (window shift −0.5), while it does not move with ks above 291.
Every new state of both chains is reported with σ_pair, its interval slope, and the fold law's D* over the last 4 and 5 states with the window
shift (`pairfold949.py`, `pairfold949.csv`; the series is ks ≥ 291 across ks_chain2, ks_chain3b and ks_chain3). A candidate zero of σ_pair at D* is
called only when, for two states in a row, the last-4 and last-5 D* agree within 0.1 and the window shift is within 0.1 for both; until then the
reading is "falling, no stable D*". A state that lands within 0.3 of the current D* estimate is reported at once. Selftest `selftest_pairfold949.log`
(planted fold 260 recovered and called after two states, a (260 − D)^2.5 law not called, one met state not enough, a rising pair "not falling", the
alert raised; `--mutate` turns the stability test off and fails).

## Planted fold test (before any state was read)

`selftest949.log` (exit 0): planted σ² = 0.3 (D* − D) exp(−2 · 0.405 (D − 232)), D* 260 and 262, on the five #941 states, five states
at D 233 to 237 and five at D 232 to 240: model B returns D* to 1e-10 and c 0.3 (grid "941"), with s 0.405; the literal fit misses
every time; a pure exponential gives no interior minimum. `selftest949_mutate.log` (exit 1): fold law (D* − D)² in the fit.

## Closing summary (2026-11-19 22:45 UTC, the 48 h stop of 2026-11-19 22:42 UTC)

**Answer.** No fold and no trigger on any chain through D 252.8861: σ_Δ falls as a plain exponential at 0.433 to 0.440 per unit D, σ_pair falls with no stable D* (the coordinator's rule was met at 0 of 44 states), and no fold window passed the validity rule. The one number still moving is ks_chain3b's trigger excess, +0.0801, +0.0803, +0.0827, +0.0896 over its last four states (D 251.2845 to 252.8861), against 0.10 at three states in a row. dh370's chain is paused for #1032 (raw 862ca41e), so there is no state past D 252.8861.

What was read: 83 states in `track949.csv` (D 192 to 252.8861; ks_chain 39, ks_chain2 25, ks_chain3b 19), plus dh610's two I971 bases. ks_chain3 (dh370, ks 304 and up) never pushed a state. Largest trigger excess per chain: ks_chain +0.0313 (D 208, against s(ks)), ks_chain2 +0.0020 (D 233), ks_chain3b +0.0896 (D 252.8861); the last two against the frozen D-trend, which for ks_chain3b is my assumption (the coordinator's amendment names ks_chain2 only).

| # | check | verdict | number |
|---|---|---|---|
| 1 | planted check of near_null on D 229.0509 | pass | `ctl_planted exit 0` (427 s) |
| 2 | `--mutate=scale_block` | pass | `ctl_planted_mut exit 1` |
| 3 | planted fold fit, D* 260 and 262, three grids | pass | D* 260.0000 and 262.0000 on all three grids, max residual 1.9e-14; control A misses each time; `fold949.py --selftest` exit 0 (rerun at close) |
| 4 | its mutation | pass | `--selftest --mutate` exit 1 (rerun at close) |
| 4a | validity rule's planted checks | pass | `selftest949.log` exit 0, its mutation exit 1 (27 no-fold windows valid: 0) |
| 5 | slope over D 229 to 232 against #941 | pass | 0.4124, 0.4097, 0.4067, 0.4047 against 0.412, 0.410, 0.407, 0.405: largest difference 0.0004 |
| 6 | every state's σ_Δ converged | pass | largest relative change over the last two iterations 3.7e-5 (D 247.2801), none over 1e-3, all 83 states |
| 7 | null control on the backfill's windows | pass | no window valid; ks 211's D* 212.8 fails by condition 2 |
| 8 | baseline frozen before leg 8 | pass | `baseline949.json` written 2026-11-18 00:01:39 UTC, the first ks 250 read started 00:01:42 UTC |

Other checks rerun at close, all exit codes as required: `track949.py --selftest` 0 and `--mutate` 1, `pairfold949.py --selftest` 0 and `--mutate` 1, `relay_dh370_949.py --selftest` 0.

Discrepancies and corrections, reported and not fixed:
- The s(ks) baseline's ks dependence was really D dependence (#948: σ_Δ is the same from ks 240 to 320 at D 232), so later chains' triggers use the D-trend. The trigger baseline for dh370's ks_chain3b is my assumption.
- Two forecasts of mine were wrong and were retracted on #949: that σ_2/σ_Δ would fall to 1.04 to 1.05 at D 247.28 with the Δ share dropping, and (07:21 UTC on 2026-11-19) that the trigger excess would pass 0.10 near D 250. It is +0.0896 at D 252.8861.
- One ALERT in the whole run: the state at D 238.6789 lay 0.195 from the previous D* estimate (reported 2026-11-18 23:26 UTC, comment 6994662166); the estimate moved on to 239.25 to 239.39 and there was no zero.
- My hc line of 2026-11-17 called σ_Δ "Delta"; it is the singular value of the Δ-mode vector, not Δ(D) (`compare_delta949.py`).
- Reading, not a result: from D 251.2845 to 252.8861 the Δ share of σ_Δ's vector rose from 0.735 to 0.853 while σ_2/σ_Δ fell from 1.152 to 1.128, so the two lowest modes were still exchanging character at the end. The trigger and the fold fit follow σ_Δ as one branch.

Recommended tasks (coordinator opens the issues):
1. **Read ks_chain3b past D 252.8861.** What: when dh370's chain resumes after #1032, read each new state with `near_null.py --k=6 --its=32` through `queue_new949.py`, report the trigger excess and the σ_pair rule per state as here. Why: its excess is +0.0896 and rising, the only series near 0.10. Acceptance: three states in a row above 0.10 fire the trigger and a valid fold fit is then required before a fold is claimed; the planted controls (`fold949.py --selftest`, `--mutate`) pass at the start. Depends on: #966 and #1032 (the chain resuming).
2. **A two-mode fit for the avoided crossing.** What: fit σ_Δ and σ_2 together with a 2 by 2 avoided-crossing law (each branch an exponential in D) to ks_chain3b's last states, and report whether the Δ branch's own slope stays at 0.433 to 0.440. Why: the single-branch trigger and fold fit read through a share change of 0.735 to 0.853. Acceptance: on planted two-branch series with a known gap and crossing D the fit recovers both within 0.1 in D, and the same fit with the gap set to zero is rejected by its own test; it then runs on the real states. Depends on: the 19 ks_chain3b states in `track949.csv` and `sig2_949.py`, no new run.
