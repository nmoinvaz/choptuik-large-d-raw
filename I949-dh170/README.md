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

## Planted fold test (before any state was read)

`selftest949.log` (exit 0): planted σ² = 0.3 (D* − D) exp(−2 · 0.405 (D − 232)), D* 260 and 262, on the five #941 states, five states
at D 233 to 237 and five at D 232 to 240: model B returns D* to 1e-10 and c 0.3 (grid "941"), with s 0.405; the literal fit misses
every time; a pure exponential gives no interior minimum. `selftest949_mutate.log` (exit 1): fold law (D* − D)² in the fit.
