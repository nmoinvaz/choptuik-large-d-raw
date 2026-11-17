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
| 5 | slope over D 229–232 reproduces #941's 0.405–0.412 | each interval's slope within 0.01 of #941's, from the five states (two re-read here, bit-compared) |
| 6 | every state's σ_Δ converged | relative change over the last two iterations below 1e-3, else rerun with `--its=32` |

## The fold fit, and two places where the issue's text needed a reading (reported, not quietly decided)

The issue fixes the fit as σ_Δ² = c (D* − D) on the last five states, tested on σ² = 0.3 (260 − D) "with the backfill's exponential
multiplied in". That linear fit cannot return 260 for a series with the exponential in it (`fold949.py --selftest` prints it:
the literal fit, model A, gives D* 232 to 240 with residuals 0.4 to 1.0, a control that must miss and does). So `fold949.py` fits
σ_Δ² = c (D* − D) exp(−2 s (D − D_last)) with c, D* and s free (model B), on the last five states of one leg (one ks), valid when
every relative residual of σ² is within 10% and D* is past the last state, as the issue says. Model A and model C (s fixed
from the baseline) are printed beside it. With 1e-3 relative noise on σ (near_null's convergence level; `noise949.log`) B's D* is
within 0.5 at 10 units from the fold and within 0.11 at 5 units (states 1 unit apart), but 7 at 28 units, with 17% of the draws
finding no interior minimum: far from the fold D* is not determined by five states, and a fold is claimed only from a fit that is
valid, whose D* lies within 40 units of the last state, and after the indicator below.

The second: the chain's σ_Δ already has a log slope of 0.405 at order 240 (#941), above the 0.10 trigger. Read literally the
trigger "slope above 0.10 for three consecutive states" fires at the first states, with no fold. The fold's own contribution to
the slope is 1/(2 (D* − D)), 0.10 at 5 units from D*, so the table also carries the excess over the baseline 0.405 and a
fold candidate is three consecutive states whose excess exceeds 0.10 (same ks). The literal trigger is also reported.

Both readings were adopted by the coordinator (hc, 2026-11-17, posted on the issue): the fit above, and the trigger on the excess slope
over the baseline, 0.405 or the backfill's own fit if it drifts, above 0.10 for three states.

## Planted fold test (before any state was read)

`selftest949.log` (exit 0): planted σ² = 0.3 (D* − D) exp(−2 · 0.405 (D − 232)), D* 260 and 262, on the five #941 states, five states
at D 233 to 237 and five at D 232 to 240: model B returns D* to 1e-10 and c 0.3 (grid "941"), with s 0.405; the literal fit misses
every time; a pure exponential gives no interior minimum. `selftest949_mutate.log` (exit 1): fold law (D* − D)² in the fit.
