# I805-mac: chain_fit's error past its comparison frontier, #603's states and jets at D 240–259.7 against track C

Machine: the Mac (Apple M5, the coordinator's machine), one process at nice 10, venv-314 (Python 3.14, mpmath, numpy,
scipy). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/805 (pre-registration in its comments).
Code: `hp/frontier_audit.py` on branch `wip/i805` at 9cdfca19 of choptuik-large-d. Note: notes/LARGE_D_WALL.md "The
chain past the comparison frontier". Inputs: `I603-win2/` (chain, chain_nat, chain_ns, chain_nsr: states, records,
logs, predictions, jets) and `I801-mac/real.json`, both at raw 1a3c1d04.

## Commands (from hp/, RAW a clone of this repository, T = this folder's table.json)

    python3 frontier_audit.py table RAW RAW/I801-mac/real.json --out=table.json        > table.log
    python3 frontier_audit.py jet RAW --table=T --out=jet.json                          > jet.log      (exit 0)
    python3 frontier_audit.py causes --table=T --out=causes.json                        > causes.log   (exit 1)
    python3 frontier_audit.py rule RAW RAW/I801-mac/real.json --out=rule.json           > rule.log     (exit 0)
    python3 frontier_audit.py held RAW --out=held.json                                  > held.log
    python3 frontier_audit.py envelope RAW RAW/I801-mac/real.json --table=T --out=envelope.json > envelope.log
    python3 frontier_audit.py planted RAW RAW/I801-mac/real.json --table=T --out=planted.json   > planted.log

## Files

- `table.json`, `table.log`: per state 240–255.8, chain − series, a local cubic residual of Δ, od steps and max|F|, the
  first Δ correction, a, refusals, the corrector's move, the LU pivots, |z_N|, |chain − series|·p_min.
- `jet.json`, `jet.log`: test J, plants W, S, N first, then the real chain from the jets at 253.9266 and 254.3086,
  with the controls and each step's Δ correction from the stored predictions.
- `jet_dps50.*`, `jet_plants_dps50.*`: the first run, at mpmath's 50 digits instead of the registered 200. Its first
  control failed (2.7e-51 against 1e-60) on that rounding. It is kept as the record, and the verdicts are otherwise
  the same.
- `causes.*`: test 2. Its plants failed, see below.
- `rule.*`: test 3, rule R in sample and out of sample.
- `held.*`: data/delta_fits.csv's held-degree differences against p_min, D 150–231.
- `envelope.*`: post hoc, the 1/p_min envelope on the chain and the plants.
- `planted.*`: exploratory, the first candidate ranking, superseded by test J.

## Results

| test | result | verdict |
|---|---|---|
| J control, each jet against its next prediction | 1.5e-67, 1.6e-66 (bound 1e-60) | passes |
| J plants W and S (smooth, known cause) | worst \|d\|/(10T) 3.6e-4, 5.6e-5; 0.046, 0.014 | pass, as required |
| J plant N (per-state errors ∝ (refused + 0.2)/p_min) | worst ratio 3.5e19, 1.4e19 | fails, as required |
| J real, states 251.89–254.21 (19 and 24 in reach) | worst \|d\|/(10T) 0.026, 0.016; \|d\| ≤ 1.5e-13 where the local cubic misses by 3–4e-8 | one analytic function |
| each step's Δ correction, 104 steps, 240–259.74 | max 1.7e-29, median 2.6e-35 | negligible |
| plan hash, 240–255.8 | one, 17758509 | constant |
| held degree response, 150–231 | d6 − d8 1.1e-11 → 4.0e-11, linear, while p_min 5.9e-8 → 1.3e-20 | not amplified |
| test 2, Spearman with per-state quantities | every plant names a (ρ ≈ +0.9, p 1e-4); N does not name refused | fails its plants: no conclusion |
| test 3, R = max(fits extrapolated, K/p_min), K = 2 × 2.194e-37 | in sample 246.26–253.35 (18 states); out of sample 66 states 253.64–259.72, worst 0.819 at 259.05 | covers every state |
| post hoc envelope: slope of log\|v\| on log(1/p_min), range of windowed max of \|v\|·p_min | real 1.04, 1.78; W 0.95, 2.56; S −0.21, 1.4e7 | real follows W |
| post hoc, median \|local residual\|/\|v\| on 248–253 | real 0.200, W 0.204, S 0.000 | the residuals are the term's curvature |

**Deviations from the pre-registration.**
- The calibration range was stated as 245.6–253.53. The series rows start at 246.26, and the state at 253.5301 lies
  just above 253.53, so it is in neither set. In sample it gives |dep|·p_min = 8.3e-38, so R covers it.
- Test 2 was registered with plants that it could not pass on this grid. A smooth term's local residual grows as the
  span⁴, and the span follows a, so every plant names a. In N, W's smooth residuals swamp the per-state errors. Test 2
  is reported as failed, and no per-state cause is drawn from it. Test J, whose plants behave, answers the per-state
  question.

## Recommended tasks (full text)

1. **Adopt rule R for the chain's rows past 245.64.**
   - **What:** in `hp/export_delta_all.py`, give #603's chain rows past the frontier, when they enter delta_all.csv,
     err = max(fits extrapolated, 4.4e-37/p_min), with err_kind "weak pivot".
   - **Why:** the "fits extrapolated" 4.4e-11 understates the departure by up to 7000× by 252.6.
   - **Acceptance:** the export's control reproduces R's out-of-sample coverage, every state 253.64–259.72 covered.
     Its mutation (K halved) must fail at 255.05 (ratio 0.655 × 2 > 1).
   - **Depends on:** #805.
2. **Test #787's λ_g against the same law.**
   - **What:** λ_g's departures from its neighbours' cubic, 250.47–259.7, against 1/p_min. If the jets carry λ_g, also
     test J for λ_g.
   - **Why:** the screen fails on the same states, and a local cubic cannot follow this term.
   - **Acceptance:** |δλ_g|·p_min bounded within a factor 3 over 250.47–259.7, or the statement that it is not. A plant
     with a per-state error must fail.
   - **Depends on:** #787, #805.
3. **What the weak direction amplifies.**
   - **What:** at 3–4 stored states in 250–253.5, Newton at fixed D with the held values of the degree-6 and
     degree-10 fits.
   - **Why:** this measures whether K changes with the held values (the held fit's extrapolation) or not (the
     discretization).
   - **Acceptance:** Δ(d6) − Δ(d8) against K/p_min at each state. A control state at 240 gives the known linear
     response, about 4e-11.
   - **Depends on:** #805. It runs alongside #801's continuum test.
