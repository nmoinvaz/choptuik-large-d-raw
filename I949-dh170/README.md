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
| 3 | planted fold fit, D* 260 and 262, three grids | pass | D* 260.0000 and 262.0000 on all three grids, max residual 1.3e-14; control A misses each time; `fold949.py --selftest` exit 0 (rerun at close) |
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
- An early hc line of mine called σ_Δ "Delta"; it is the singular value of the Δ-mode vector, not Δ(D) (`compare_delta949.py`).
- Reading, not a result: from D 251.2845 to 252.8861 the Δ share of σ_Δ's vector rose from 0.735 to 0.853 while σ_2/σ_Δ fell from 1.152 to 1.128, so the two lowest modes were still exchanging character at the end. The trigger and the fold fit follow σ_Δ as one branch.

Recommended tasks (coordinator opens the issues):
1. **Read ks_chain3b past D 252.8861.** What: when dh370's chain resumes after #1032, read each new state with `near_null.py --k=6 --its=32` through `queue_new949.py`, report the trigger excess and the σ_pair rule per state as here. Why: its excess is +0.0896 and rising, the only series near 0.10. Acceptance: three states in a row above 0.10 fire the trigger and a valid fold fit is then required before a fold is claimed; the planted controls (`fold949.py --selftest`, `--mutate`) pass at the start. Depends on: #966 and #1032 (the chain resuming).
2. **A two-mode fit for the avoided crossing.** What: fit σ_Δ and σ_2 together with a 2 by 2 avoided-crossing law (each branch an exponential in D) to ks_chain3b's last states, and report whether the Δ branch's own slope stays at 0.433 to 0.440. Why: the single-branch trigger and fold fit read through a share change of 0.735 to 0.853. Acceptance: on planted two-branch series with a known gap and crossing D the fit recovers both within 0.1 in D, and the same fit with the gap set to zero is rejected by its own test; it then runs on the real states. Depends on: the 19 ks_chain3b states in `track949.csv` and `sig2_949.py`, no new run.

## Reopened 2026-11-20 02:03 UTC (coordinator's comment, #949 after my D 253.3365 read on #966)

Criteria for the continuation, written before the first new read:

- Read every new ks_chain3b state past D 253.3365 (`c3b_` names, dh370's `I966-dh370/ks_chain3b/leg07...`) with the same `near_null.py --k=6 --its=16 --its=32` at `--threads=2` (one lane, nice 10, beside the #1014 M 384 series), hp build 787f1006. The rule is unchanged: the trigger is σ_Δ's interval slope minus the frozen D-trend (0.9692 − 0.00245 D at the interval's midpoint, `dtrend_frozen949.json`) above 0.10 at three consecutive states. Post each row on #949; tell the coordinator at once (hc and the issue) if the trigger fires.
- The D 253.3365 state was read before the reopening in `I966-dh170/` (exit 0, 1771 s, controls exit 0 and 1 there); its JSON and log are copied here as `c3b_ks293_D253.3365.*` and it counts as the first state past 0.10 (excess +0.1035).
- Controls: `track949.py --selftest` and `--mutate`, `pairfold949.py --selftest` and `--mutate` rerun at the reopening (`selftest_*_reopen.log`: the plain runs exit 0 and the mutations exit 1). near_null's planted pair was rerun at 02:00 UTC in `I966-dh170/` (exit 0 and exit 1).
- The two-mode (avoided-crossing) fit of σ_Δ and σ_2 waits until three states past 0.10 exist, with its planted two-branch test first (its criteria are written here before its code).
- No stop time was given: the lane and `autoqueue949.sh` (sync and queue every 5 min) run until `STOP949` exists. The old `STOP949` is kept as `STOP949.closed_2026-11-19`.
- **Stop rule (coordinator's hc, 2026-11-20 about 02:07 UTC):** stop at 2026-11-21 02:00 UTC (24 h after the reopening), or earlier when the trigger has fired and the two-mode fit is posted, whichever comes first; post a closing row then. This replaces "no stop time given" above. At the stop I create `STOP949`, end the lane, the autoqueue and the waits, push, post the closing row on #949 (with the table of every state read since the reopening, the trigger run, and the two-mode fit if it was run), remove `running` and close the issue as for the first close.

## The two-mode fit: law and pass criteria, written before `twomode949.py` (2026-11-20 about 02:08 UTC)

Run only after three ks_chain3b states past 0.10 exist (coordinator), on the five latest states of the leg. This is my reading of recommended task 2 above.

- Law: x = D − D_last. Two diabatic branches a1 = exp(p1 − s1 x) (the Δ branch, the lower of the two at the last state) and a2 = exp(p2 − s2 x), coupling g = γ sqrt(a1 a2), 0 ≤ γ ≤ 0.9. The observed pair is the eigenvalues of [[a1, g], [g, a2]]: σ_Δ = (a1 + a2)/2 − sqrt(((a1 − a2)/2)² + g²) and σ_2 = the plus root. Five free numbers (p1, s1, p2, s2, γ) against ten values ln σ_Δ, ln σ_2 of five states; fit by least squares on ln σ with a grid of starts. Crossing D_c: a1 = a2. The gap at the crossing is σ_2/σ_Δ = (1 + γ)/(1 − γ).
- Reported on the real states: s1 (the Δ branch's own slope: does it stay at 0.433 to 0.440?), s2, D_c, γ, the rms residual of ln σ, and, as a check the fit did not use, the mixing's prediction of the lowest vector's Δ share (1 + (a2 − a1)/sqrt((a1 − a2)² + 4 g²))/2 against the measured share.
- Planted test, first: noiseless-to-1e-6 pairs on a five-state grid spaced 0.45 (the chain's spacing) with the truth known: (a) gap γ = 0.06 and 0.15, D_c inside the window or up to 0.5 outside it, s1 = 0.43, s2 = 0.47 and also s1 = 0.47, s2 = 0.43: pass = D_c within 0.1 and γ within 20% of the truth and s1, s2 within 0.02, for every planted case; any case outside is reported with its distance, not loosened. (b) γ = 0 (true crossing): pass = the fitted γ ≤ 0.01. (c) the gap-zero fit (γ fixed at 0) on the data planted with γ = 0.06 or 0.15 must be rejected: its rms residual above 3e-3 where the free fit's is below 1e-5. (d) `--mutate` drops the coupling term from the model, so the recovery (a) must fail (exit 1).
- The planted test must pass (exit 0, the mutation exit 1) before the fit touches a real state.

First planted run of `twomode949.py` (`selftest_twomode949_first_run.log`, exit 1, as the criteria above were written): (a) 6 of 8 cases pass with D_c and γ exact to 1e-3, the two failures are the cases with D_c exactly at the last state (a1 = a2 there, so "the lower diabatic value at the last state" is a tie and the fit returned the branches swapped: an ill-posed case, not a recovery failure); (c) **fails as written**: the gap-zero fit's rms is 8.4e-4 (γ 0.06) and 4.3e-4 (γ 0.15), below the 3e-3 I guessed, against the free fit's 4.9e-7 (the noise). Amendments made after seeing this, before any real state: (i) the tie cases D_c = D_last are replaced by D_c = D_last ± 0.05 (crossing just after the last state when s1 < s2, just before it when s1 > s2) and the cases are the crossing 0.05 and 0.5 after the last state (s1 < s2) and 0.05, 0.5 and 1.3 before it (s1 > s2, inside the window); (ii) criterion (c) becomes: the gap-zero fit's rms is above 1e-4 and at least 100 times the free fit's. The 3e-3 had no noise scale behind it. Both amendments are mine, not the coordinator's.

Planted test of `twomode949.py` after the amendments (`selftest_twomode949.log`, exit 0): (a) all 10 planted cases recover D_c (to 1e-3) and γ (to 1e-3 relative) and s1, s2 exactly, rms 4.9e-7 (the planted noise); (b) γ = 0 returns γ = 0.0000; (c) the gap-zero fit on gapped data has rms 8.4e-4 and 4.3e-4 against the free fit's 4.9e-7 (rejected). A first rerun of the mutation (`selftest_twomode949_mutate_run1.log`) also dropped the coupling from the planted data, which made its failure uninformative; the final `--mutate` drops it from the fitter only, and then all 10 recoveries, (b) and (c) fail (`selftest_twomode949_mutate.log`, exit 1: the check can fail). `twomode949.py` runs on real states only while `selftest_twomode949.log` is newer than the script and ends `exit 0`. Not yet run on real states: three states past 0.10 do not exist yet (D 253.3365 is the first).

**Stop rule changed again (coordinator's hc, 2026-11-20 about 03:16 UTC, after the trigger fired at D 254.1769):** the trigger is noted and the fits are read as I posted (no fold and no avoided crossing claimed). Keep reading new ks_chain3b states until 2026-11-21 02:00 UTC at 2 threads beside #1014; at each new state post its row and rerun both fits on the last five states (`step949.sh`: tracker, pair fold, `row949.py`, `twomode949.py 5`, `stopcheck949.py`); stop early, with a closing row, when the fold fit passes all four conditions or when the excess is below 0.10 for two states in a row. The fits' code (`fold949.py`, `twomode949.py`) and their pass criteria stay fixed while reading. I had started the close-out steps (a `STOP949`, the lane and sync killed by exact pid, 03:15:29 to 03:15:50 UTC, the lane idle, no read lost) before this order arrived; they were restarted at 03:15:50 UTC and the stray marker is kept as `STOP949.premature_2026-11-20`.

## Closing summary of the reopening (2026-11-20 16:35 UTC, stop rule (b): the excess below 0.10 at two states in a row)

**Answer.** No fold and no avoided crossing: ks_chain3b's trigger fired at D 254.1769 and the excess peaked at +0.2948 at D 257.6920, then fell back to +0.0598 and +0.0269 at D 259.4568 and 259.7352, so σ_Δ's slope went 0.44 to 0.633 and back to 0.360 against a baseline of 0.333, a bump on a plain exponential. None of the 30 fold windows of ks 293 passed the rule (TTTF three times, TTTT never), and the two-mode fit did not reproduce the measured Δ shares where it had a coupling. I stopped at D 259.7352 because the stop rule's second condition was met.

States read since the reopening: 21 (D 253.3365 to 259.7352, `c3b_ks293_D<D>.log/.json`, 2 threads each, 791 to 2039 s; 40 ks_chain3b states in all). Not kept: the read of D 260.0073, stopped 114 s in at the stop (`c3b_ks293_D260.0073.log.aborted_at_stop`).

| D | σ_Δ | Δ share | σ_Δ slope | baseline | excess | σ_2 (σ_2/σ_Δ) | σ_2 slope | σ_pair, slope | pair D*(4)/(5), shifts | rule | pinned Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 253.3365 | 1.1458e-18 | 0.925 | 0.4526 | 0.3491 | +0.1035 | 1.2922e-18 (1.128) | 0.454 | 3.086e-13, +0.4380 | 276.863 (-1.861) / 275.723 (-1.486) | not met | +2.120e-38 |
| 253.7634 | 9.3704e-19 | 0.973 | 0.4713 | 0.3480 | +0.1233 | 1.0695e-18 (1.141) | 0.443 | 2.559e-13, +0.4384 | 276.426 (+0.437) / 276.564 (-0.842) | not met | -5.991e-32 |
| 254.1769 | 7.6585e-19 | 0.990 | 0.4878 | 0.3470 | +0.1408 | 8.9434e-19 (1.168) | 0.432 | 2.134e-13, +0.4390 | 274.337 (+2.089) / 275.302 (+1.262) | not met | -1.935e-31 |
| 254.5903 | 6.2379e-19 | 0.992 | 0.4963 | 0.3460 | +0.1504 | 7.4883e-19 (1.200) | 0.430 | 1.779e-13, +0.4397 | 272.238 (+2.100) / 273.188 (+2.114) | not met | -2.758e-33 |
| 255.0004 | 5.0868e-19 | 0.990 | 0.4974 | 0.3450 | +0.1525 | 6.2593e-19 (1.231) | 0.437 | 1.485e-13, +0.4405 | 270.751 (+1.487) / 271.432 (+1.756) | not met | -6.349e-33 |
| 255.3972 | 4.1783e-19 | 0.988 | 0.4958 | 0.3440 | +0.1519 | 5.2291e-19 (1.252) | 0.453 | 1.247e-13, +0.4415 | 269.866 (+0.884) / 270.286 (+1.146) | not met | -7.016e-46 |
| 255.7960 | 3.4261e-19 | 0.984 | 0.4977 | 0.3430 | +0.1548 | 4.3297e-19 (1.264) | 0.473 | 1.045e-13, +0.4425 | 269.437 (+0.429) / 269.651 (+0.635) | not met | -1.467e-54 |
| 256.1776 | 2.8214e-19 | 0.977 | 0.5088 | 0.3420 | +0.1668 | 3.5904e-19 (1.273) | 0.491 | 8.823e-14, +0.4436 | 269.375 (+0.062) / 269.416 (+0.235) | not met | -4.553e-43 |
| 256.5265 | 2.3440e-19 | 0.966 | 0.5313 | 0.3411 | +0.1902 | 3.0183e-19 (1.288) | 0.497 | 7.555e-14, +0.4446 | 269.530 (-0.155) / 269.457 (-0.041) | not met | -3.115e-52 |
| 256.8479 | 1.9567e-19 | 0.953 | 0.5620 | 0.3403 | +0.2217 | 2.5779e-19 (1.317) | 0.491 | 6.547e-14, +0.4455 | 269.844 (-0.314) / 269.683 (-0.225) | not met | +4.358e-47 |
| 257.1452 | 1.6399e-19 | 0.943 | 0.5940 | 0.3396 | +0.2545 | 2.2394e-19 (1.366) | 0.473 | 5.734e-14, +0.4463 | 270.263 (-0.419) / 270.033 (-0.350) | not met | -6.487e-41 |
| 257.4254 | 1.3785e-19 | 0.940 | 0.6196 | 0.3389 | +0.2807 | 1.9740e-19 (1.432) | 0.450 | 5.059e-14, +0.4471 | 270.717 (-0.454) / 270.472 (-0.439) | not met | -2.977e-48 |
| 257.6920 | 1.1645e-19 | 0.943 | 0.6330 | 0.3382 | +0.2948 | 1.7617e-19 (1.513) | 0.427 | 4.489e-14, +0.4478 | 271.215 (-0.498) / 270.946 (-0.475) | not met | -8.939e-44 |
| 257.9477 | 9.9094e-20 | 0.952 | 0.6312 | 0.3375 | +0.2937 | 1.5875e-19 (1.602) | 0.407 | 4.003e-14, +0.4484 | 271.708 (-0.493) / 271.445 (-0.498) | not met | -4.852e-45 |
| 258.1958 | 8.5096e-20 | 0.962 | 0.6136 | 0.3369 | +0.2767 | 1.4387e-19 (1.691) | 0.396 | 3.581e-14, +0.4490 | 272.212 (-0.504) / 271.949 (-0.504) | not met | -1.362e-46 |
| 258.4403 | 7.3810e-20 | 0.972 | 0.5819 | 0.3363 | +0.2456 | 1.3055e-19 (1.769) | 0.397 | 3.208e-14, +0.4496 | 272.768 (-0.555) / 272.480 (-0.532) | not met | -2.219e-49 |
| 258.6851 | 6.4687e-20 | 0.979 | 0.5391 | 0.3357 | +0.2034 | 1.1800e-19 (1.824) | 0.413 | 2.874e-14, +0.4501 | 273.352 (-0.585) / 273.054 (-0.573) | not met | +1.123e-49 |
| 258.9339 | 5.7266e-20 | 0.985 | 0.4898 | 0.3351 | +0.1547 | 1.0563e-19 (1.845) | 0.445 | 2.569e-14, +0.4506 | 273.986 (-0.634) / 273.672 (-0.618) | not met | +1.311e-49 |
| 259.1902 | 5.1169e-20 | 0.989 | 0.4393 | 0.3345 | +0.1048 | 9.3052e-20 (1.819) | 0.495 | 2.288e-14, +0.4511 | 274.734 (-0.748) / 274.370 (-0.698) | not met | -5.413e-50 |
| 259.4568 | 4.6071e-20 | 0.990 | 0.3937 | 0.3339 | +0.0598 | 8.0126e-20 (1.739) | 0.561 | 2.029e-14, +0.4515 | 275.570 (-0.836) / 275.166 (-0.796) | not met | +2.275e-51 |
| 259.7352 | 4.1675e-20 | 0.991 | 0.3601 | 0.3332 | +0.0269 | 6.7021e-20 (1.608) | 0.641 | 1.789e-14, +0.4520 | 276.580 (-1.010) / 276.104 (-0.938) | not met | -3.409e-54 |

| # | check | verdict | number |
|---|---|---|---|
| 1 | selftests of `track949`, `pairfold949`, `fold949`, `twomode949`, `stopcheck949`, `relay_dh370_949` rerun at close, each with its mutation | pass | `close_selftests949.log`: 6 selftests exit 0, 7 mutations exit 1, "all ok" |
| 2 | planted two-branch test of `twomode949.py` before it touched a real state | pass | `selftest_twomode949.log` exit 0 (10 planted cases, D_c to 1e-3, γ to 1e-3 relative), its mutation exit 1 |
| 3 | every state's σ_Δ converged and its check | pass | 21 of 21 `check: pass`, ‖J v₁‖/σ₁ = 1.000000, largest relative change over the last two iterations 1.8e-7 (D 253.3365) |
| 4 | trigger (excess above 0.10 at three states in a row) | fired | D 254.1769 (+0.1035, +0.1233, +0.1408); 19 states above 0.10 (D 253.3365 to 259.1902); peak +0.2948 |
| 5 | fold fit passes all four conditions (stop (a)) | not met | 0 of 30 ks 293 windows valid; TTTF at the windows ending D 254.1769, 257.1452, 257.4254; FFF− at the last seven windows |
| 6 | excess below 0.10 at two states in a row (stop (b)) | met | +0.0598 (D 259.4568), +0.0269 (D 259.7352); stopped 2026-11-20 16:33 UTC |
| 7 | σ_pair rule (last-4 and last-5 D* within 0.1, window shifts within 0.1, twice) | not met at any of 21 states | the pair's D*(4) went 276.9 (D 253.3365), 269.4 (D 255.8 to 256.2), 276.6 (D 259.7352), shifts −0.9 to −1.0 at the end |
| 8 | two-mode fit, 19 windows (D 254.1769 to 259.7352) | no avoided crossing | γ > 0 in 9 windows (0.058 to 0.059, then 0.112 to 0.131), 0 in 10; rms of ln σ 8.6e-4 to 1.2e-2 (worst at the end); with γ > 0 the fitted Δ share is off by 0.14 to 0.54 at its worst state; with γ = 0 it is 1.000 (no mixing) against measured 0.94 to 0.99 |

Discrepancies and corrections, reported and not fixed:
- My read at D 255.7960 said the pair fold's D*(4)/D*(5) gap and shifts were shrinking by about half per state and so approaching the σ_pair rule. They then reversed (D* from 269.4 to 276.6, shifts to −1.0). That was a trend read from four states, not a result.
- Five posts carried an error that I corrected by comment id within minutes: the two-mode gap sentence (7036856832), a raw hash taken from the live clone instead of the push (7037136236 said 6be60ab2, now 96319321), a Δ-share "first time" claim (7040325563), an arithmetic slip, 0.07 for 0.09 (7043705842), and a σ_2/σ_Δ "first time since D 257.4" claim (7044307881).
- `row949.py N` fails with `ValueError` for N past the first state with a trigger baseline (N 40); N 21 works. Code unchanged. The output of the failed call is `closing_rows949_all.md.failed_N40`.
- `pairfold949.py` prints the same ALERT about D 238.6789 at every run (the old one, reported 2026-11-18); it is not new.
- The σ convergence estimate prints 0e+00 for σ_Δ from D 258.4403 on: the iteration changed nothing at that precision, and the check and ‖J v₁‖/σ₁ = 1 pass.
- Reading, not a result: the Δ share of σ_Δ's vector fell from 0.992 (D 254.59) to 0.9395 (D 257.43) and returned to 0.991, σ_2's slope rose from 0.397 (D 258.44) to 0.641 and crossed σ_Δ's between D 258.93 and 259.19, and σ_2/σ_Δ peaked at 1.845 (D 258.93) then fell to 1.608. That is what two branches passing each other looks like, but the two-mode law with constant slopes does not fit it.

Recommended tasks (coordinator opens the issues):
1. **Read ks_chain3b past D 259.7352 to see whether the bump has closed.** What: read the next states of dh370's chain (D 260.0073 and on) with `near_null.py --k=6 --its=32`, report the excess and σ_Δ's slope per state. Why: the excess is +0.0269 and falling 0.03 to 0.05 per state; a return to 0 means the steepening was transient, a rise again means a second bump. Acceptance: the excess stays within ±0.05 for five states in a row, or the issue is reopened with the new peak; the planted controls (`close_selftests949.sh`) pass first. Depends on: dh370's chain being written past D 260.0073.
2. **A two-mode fit with branch slopes that vary with D.** What: fit σ_Δ and σ_2 over D 256.5 to 259.7 with each branch's log slope linear in D (two more parameters), on its own planted test (known gap, known slope drift, recover D_c within 0.1 and γ within 20%, and the same fit with γ = 0 rejected). Why: the constant-slope law never reproduced the Δ-share dip. Acceptance: the fitted Δ share matches the measured one to 0.02 at every state of the window, or the fit is rejected by its own test. Depends on: the 12 states in `track949.csv` (D 256.5265 to 259.7352).
