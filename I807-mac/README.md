# I807-mac: the gauge rate lam_g past the comparison frontier, #787's screen against #805's weak-pivot law

Machine: the Mac (Apple M5, the coordinator's machine), one process at nice 10, venv-314. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/807, with the pre-registration and one amendment in its comments.
Code: `hp/lam_frontier.py` on branch `wip/i807` at 2e116e53 of choptuik-large-d. Note: notes/LARGE_D_WALL.md "The gauge
rate carries the same term". Inputs: `I603-win2/` (states, records, predictions, chain_nsr's jets) and the chain_fit
backbone states named in hp/data/delta_all.csv, all at raw 1a3c1d04.

## Commands (from hp/, RAW a clone of this repository)

    python3 export_delta_all.py RAW --lam_screen              > export_lam_screen.log  (#787's screen, reproduced; exit 1)
    python3 lam_frontier.py jet RAW --out=jet.json            > jet.log                (exit 0)
    python3 lam_frontier.py law RAW --out=law.json            > law.log                (exit 0)
    python3 lam_frontier.py screen RAW --out=screen.json      > screen.log
    python3 lam_frontier.py pred RAW --out=pred.json          > pred.log               (exit 0)
    python3 lam_frontier.py pred RAW --mutate=lam             > pred_mutate_lam.log    (exit 1, as it must)
    python3 lam_frontier.py posthoc RAW --out=posthoc.json    > posthoc.log

`jet_ctl_Dstr.*` is test J's first run. Its control took a from the stored D strings and failed, as described below.

## Results

| test | result | verdict |
|---|---|---|
| J control, 62 jets against their next prediction (amended) | 1.2e-63 (bound 1e-60); n-mutation 1.1e-4 | passes; mutation fails |
| J plants W, S | worst 0.026, 0.125 of the bound | pass, as required |
| J plants N (per-state errors), N1 (one state moved by 1e-10) | 3.6e21, 1e20 | fail, as required |
| J real: 1236 comparisons, 83 states 251.30–259.74 | worst 0.31 of 10T, \|d\| ≤ 2.2e-12 | lam_g is one analytic function |
| each step's lam_g change from its prediction, 121 steps 226.13–259.74 | ≤ 5.1e-31 | negligible |
| L: R's residual on 150–245.64 | 4.7e-13; spread 1.4e-11 (250.47) to 3.6e-10 (259.7) | all 82 states enter |
| L real, windows ending by 259.7 | windowed max of \|lam − R\|·p_min 2.9e-39 to 5.1e-39, factor 1.77 | the law holds (≤ 3) |
| L plant W | factor 2.24 | passes, as required |
| L plants S, E (as registered) | no state clears 3 × spread | fail, but through the entry rule |
| post hoc: S, E past the frontier only | factors 3.6e4, 1.4e4 | fail on the statistic |
| post hoc: windows cut short by the last state | real 17.7, W 3.4 | near the fold the law is an upper envelope |
| screen on lam_g and on lam_g − R | #787's departures exactly; equal to 1.3e-19 | the departures are the term's |
| literal reading, screen departure × p_min | factor 69 | not within 3 (depends on spacing) |
| proposed rule: \|lam(state) − lam(prediction)\| ≤ 1e-20 | 121 states at ≤ 5.1e-31; 1e-10 mutation caught | passes, control fails |

**The amendment.** The first control, each jet's lam at its next state's D against the prediction file's, failed at 42
of 62 jets, from the jet at 257.50 on: 1e-53 to 3.1e-51.
- The run keeps D in about 50 significant digits. Past 257.5 the stored D strings differ from base + a, where a is the
  prediction's own float, by 2.5e-48 to 6e-48.
- Jet and prediction differ in every entry, Δ included.
- The amended control evaluates the jet at the prediction's a, with both sides' n = D_b + a − 2.
- Test J's comparisons are unchanged. The ~1e-50 that this leaves is far below their 1e-30 floor.

## Recommended tasks (full text)

1. **Adopt the prediction check as #787's screen past the frontier.**
   - **What:** in `export_delta_all.py --lam_screen`, for backbone states whose run stored predictions, test
     |lam_g(state) − lam_g(pred file)| ≤ 1e-20 in place of the polynomial. Keep the polynomial below 250.46 and where
     no prediction exists.
   - **Why:** the polynomial cannot follow the weak-pivot term past 250.46. The prediction check needs no smoothness
     over neighbours.
   - **Acceptance:** all 121 of #603's states pass. `--mutate=lam` (1e-10 at the state nearest 240) must fail.
   - **Depends on:** #807, #787.
