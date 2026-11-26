# I1098-mm5/ladder/D360m48: D 360's tail at M 48 on fastmul6, the cross-check against dh610's M 32 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-26 21:02 UTC): a short cross-check that D 360 lacks, D 360's M 48 tail on fastmul6 (about 40 min), run while D 2231 is held for dh610's ks scan. D 2231 waits for it if the scan answers first.

Input: dh610's D 360 M 32 h13 state `I1098-dh610/ladder/D360/rls/release_ls_h13_D360.0000.npz`, copied to `../inputs/D360_rls_h13.npz` (**blob 572bc483fc379317b8c9bf0b64add16431ea4ad3**, equal to raw's).
Tools: `../tools3/` from raw origin/main (`I1098-mac-a/tools/`), blobs verified with `git hash-object`: `ladder_tail.sh` 322f0995ace89827d8265882f2c03defafaa7f1a, `kstar_stage.sh` 6d29dfc0225a2eff0be932cb849e656c190a0b6e, `kstar_gain.py` e74b4fc7464175341dc0b9a77e60507eeccf4363,
`kstar_summary.py` 8e22d799c3822f57919018f60b63beb59bded157, `variant_state.py` 19b05a5a70e1b6e49f700e176a4d86c265a0ea48, `resample_m.py` 4de5c3174ad1bad3a5a311f909db9d3ecec64b5b.

```
MT=48 KS=957 KMAX=23 INNER_CHORD=0 HP=$HOME/Source/choptuik-fastmul6/hp SITE=$HOME/Source/fastmul6-site bash tools3/ladder_tail.sh mob 360 <ladder>/inputs/D360_rls_h13.npz <ladder>/D360m48 6
```

Detached, 6 threads, from the ladder folder; Python 478e9d86 (HP's HEAD, the commit the records name), kernel `~/Source/fastmul6-site`. The Moebius horizon a = max(8, (D - 2)/400) = 8 at **ks 957** (= ceil(1.5 (D - 2)) + 420 = 537 + 420), the state resampled to M 48, h13 re-converged, h15..h23 released
(qq, od, tol 1e-48, tol_h 1e-44, --ddelta 1e-25, --inner_chord 0: the chord-free path of D 432-622, as for every later point), then the k* stage by itself (`kstar_stage.sh`: the bound at kfree 15, re-converged when gain x F > 1e-27).

## Bars, written before the run (coordinator's order)

- The h13 re-converge at M 48 moves Delta by about **1e-25 or less** (D 300: +7.3e-26; D 622: +4.6e-26).
- The final Delta against dh610's M 32 final **1.672499793793157083326890316334382065517** differs by less than **1e-24**. That difference is D 360's `err_xcheck_M`, and it also differs in machine.
- The tail falls as at D 432 (h15 -4.5351e-17, h17 -2.4908e-19, h19 +8.0779e-22, h21 +8.8627e-24, h23 pending +2.24e-28), with no turn at h23.
- Stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped.
- Reported: both shifts (the h13 re-converge and the final against dh610's M 32), pushed at the end. Times from `date -u`.

### Refinement of the stop rule for resampled states (2026-11-26 21:09 UTC, coordinator's order)

A qq inner floor at h13 outer 0 right after an M resample (the first large correction, as at D300m48: floor 9.90e-31 against 2.68e-17, then outer 1 converged to 2.11e-64) is logged, not stopped. **A floor above 1e-48 at any later outer step stops the run.**
Here: h13 outer 0 (21:02:22 UTC): trial lam 1 "inner floor in 2 steps (|F| 1.99e-31), target |F| 1.99e-31 against 1.05e-17 (381 s)", the step accepted (full-step dDelta -1.77e-20); logged, run left going. The refinement applies to the later points too (the ladder README).

## Result (the run ended 2026-11-26 22:18:10 UTC, rc 0, k* stage rc 0; 21:02:20 - 22:18:10, 4550 s)

By script from `run.log`, `rls.log`, `release_ls.jsonl`, `direct_s.jsonl` and `kstar/`.

- **ks used: 957** (a 8, kc 146, M 48 tail, Python 478e9d86, chord-free; the records say 478e9d86).
- **The tail** (h13 re-converged on M 48, then h15..h23; per-harmonic wall in brackets):

| harmonic | change in Delta | pending dDelta at release | wall |
|---|---|---|---|
| h13 (M 32 -> 48 re-converge; outers 0, 1, 2) | **+4.8306e-26** (-7.9194e-23, +7.8856e-23, +3.869e-25) | +3.48e-45 (outer 3) | 1286 s |
| h15 | -5.6237e-17 | +9.10e-32 | 618 s |
| h17 | -2.9926e-19 | -9.36e-32 | 631 s |
| h19 | +1.1268e-21 | +1.74e-36 | 607 s |
| h21 | +1.1575e-23 | +4.39e-35 | 656 s |
| h23 | none | **-3.47e-27** (harmonic step 4.59e-14), released at outer 0 | 126 s |

- **Final Delta of the tail (the state's `Delta_parts` summed at 60 digits): 1.67249979379315708332689036416651288399** (h23's pending not in it); total -5.65352e-17 from the M 48 start. State `release_ls_h23_D360.0000.npz`, blob fc3c4ebeb29a1b6786704026a85b29b6ffbe4667; od solve max |F| 5.02173e-55, qd check 5.02173e-55; Hamiltonian check at the four nodes at most: p 8.7e-31, m 9.2e-31, a 4.3e-31, c 6.0e-29.
- **The two shifts the order asked for:**
  - **The h13 re-converge at M 48: +4.8306e-26** (bar: about 1e-25 or less; D 300 +7.3e-26, D 622 +4.6e-26, D 747 -7.6e-27): met.
  - **The final Delta against dh610's M 32 final (1.672499793793157083326890316334382065517): +4.78321e-26** (bar: less than 1e-24): met. This is D 360's `err_xcheck_M` and it also differs in machine (dh610's M 32 run against this runner's M 48).
- **The tail falls as at D 432:** h15/h17 = 188, h17/h19 = 266, h19/h21 = 97 (D 432: 182, 308, 91); h21's change 1.1575e-23 (D 432 8.86e-24); h23 released with pending -3.47e-27 (D 432 +2.24e-28): no turn: met.
- **h13 outer 0 (qq, right after the resample):** trial lam 1 "inner floor in 2 steps (|F| 1.99e-31), target |F| 1.99e-31 against 1.05e-17 (381 s)", logged under the refinement of the stop rule; outer 1 converged in 2 steps to 4.25e-49 (below 1e-48). No other floor, no line-search trial below lam 1, no outer step above 3x its harmonic's first.
- **k* stage** (`kstar/`, 624 s, 22:07:46 - 22:18:10): kfree 15, gain 1.669717e+28, F before 4.82777e-50, **bound before 8.06102e-22** (gain x F), above 1e-27, so re-converged (qq, od, tol 1e-62, h15 outer 1 released, pending +7.81e-48): F after 2.79133e-75, Delta of the k* system moved **+9.09764e-32**, **bound after 9.0976e-32**.
  The k* system's Delta (1.672499793793157083625014766148364158392 at the start) is the Delta at kfree 15, 2.98124e-19 above the tail's final (the harmonics h17..h23's fall); it is not the final Delta.
