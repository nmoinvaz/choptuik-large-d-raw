# I668-rpi5: an error-weighted far-end estimator recalibrated on #547's plants

Machine: rpi5 (Raspberry Pi 5, aarch64, 4 cores), one process at `nice -n 10`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/668

Made by `solver/inner_amp/pade_farend_w.py` (branch `wip/i668`, the frozen estimator E6 at 43481472) from the σ₀–σ₂₂ of
`solver/inner_amp/scan45J1250` and `scan45J1500`. Design, frozen criteria, amendments and results: `notes/PADE_FAR_END.md` §19
(§19.9 for the 35 plants).

## State

The task stopped after the 35-plant run. **C1 and C3 fail on 6 arcjump plants each** (29 of 35 pass both; the 26 plants of the
chord2, arc, arcmid and arcsteps families pass at 0.015 and 0.008). The controls (`--mutate=unweighted`, `err_reversed`,
`noise1000`, `err_flat` on D1–D5), the real series and the scale1.03 control were NOT run: the coordinator reassigned the
runner on 2026-11-18. The files below that would hold them (`controls_*`, `real*.json`) do not exist.

## Files

| file | what |
|---|---|
| `selftest.log`, `selftest_mutate_*.log` | the selftest (B-regression, S1–S4) and its five mutations, all as required (exit 0 and 1) |
| `development.{json,log,time}` | development round 1, presets E1 and E2 on D1–D5 |
| `development_r1.{json,log,time}` | round 1, presets E3 and E4 (the χ² gate) |
| `development_r2.{json,log,time}` | round 2, presets E5 and E6, then the freeze on E6 |
| `table_E3.{log,time}` | the member table of E3 on the development plants (the gate's threshold was read from it) |
| `plants.started` | start time of the frozen 35-plant run, 2026-11-18 05:33 UTC (the shell clock), run time 51 min |
| `plants.log`, `plants.json` | the frozen run: per plant the estimate, the error against the noise-free plant, the spread, the noise on 10 draws (547000+i) and on fresh draws (668000+i), the 17 members (degrees, lp, zero, χ², ν, counted), the ratio-law baseline, and the C1–C3, C3′, B1 verdicts |

## Result of the 35 plants (frozen E6)

| criterion | result |
|---|---|
| C1, within 0.02 | FAIL, 6 plants: V arcjump R1.80 0.045, R1.85 0.042, R−0.05 0.023, R+0.05 0.043, R1.75 0.053, R1.9 0.041 |
| C2, 9 pairs differ by more than 0.03 | pass, 0.046–0.062 |
| C3, noise ≤ 0.01 | FAIL, 6 plants: D2 arcjump 0.038, V arcjump wf0.99 0.033, wf1.01 0.069, R−0.05 0.026, R+0.05 0.040, R1.9 inf |
| C3′, fresh draws | FAIL, the same 6, largest 0.077 |
| B1, ratio law misses the κ⋆ plants by more than 0.05 | holds |

`inf` means a noise draw left fewer than 3 counted members (the gate of §19.6), so there is no estimate for it.

## Remaining steps (not run)

Each runs from `solver/inner_amp/` of branch `wip/i668`, at `nice -n 10`, one at a time, with `--allow_unraw` not needed when the
output folder is this one. `run_real` must run unmutated before `--mutate=scale1.03`, which reads its `real.json`.

1. `pade_farend_w.py plants $RAW --mutate=unweighted` (must fail C1 and C3 on D1–D5), `--mutate=err_reversed` (must fail),
   `--mutate=noise1000` (must fail C3), `--mutate=err_flat` (reported). Each takes 4–8 minutes. A mutation that does not fire exits 2.
2. `pade_farend_w.py real $RAW`, then `real $RAW --mutate=scale1.03` (the estimate × 1.03 within 1e-6, moved by more than 0.03), then
   `real $RAW --mutate=sigma7` (reported). The real series' members' χ²/ν were 88 to 7×10⁵ on the ones seen (§19.7), so the gate
   probably leaves fewer than 3 counted members and gives no estimate, in which case the scale1.03 control cannot pass.

The acceptance (C1–C3 on all 35 plants, and the scale1.03 control on the real series) is not met by what ran, so a run of these
steps would not change the verdict on the plants.

## Recommended tasks

1. **Why the weighted estimator fails on the jump.** The arcjump plants fail with a 0.033–0.042 bias at |P1| 1.75–1.90 and a noise
   of 0.026–0.069 at 1.62–1.68. What: log each arcjump plant's counted members' zeros (`plants.json`, `members`), test a pole-only
   variant and a larger window past 3.0·ρ/ρ_ref. Why: C1 and C3 both fail only here. Acceptance: C1 and C3 on the 9 arcjump plants, with
   the unweighted control failing them. Depends on #668.
2. **Stop the gate from emptying the member list.** R1.9 has a draw with fewer than 3 counted members. What: replace the χ²/ν ≤ 10 gate
   by a bound set from the plants' noise-free χ²/ν. Acceptance: no `inf` noise on the 35 plants, and the real series' member count
   reported. Depends on #668.
3. **The controls and the real series of 19.3 on E6 as frozen.** What: the steps above. Why: they test whether the weights are what
   removes the noise on the 29 passing plants. Acceptance: the controls fire as required, and the scale1.03 control passes if there is
   a real-series estimate. Depends on #668.
