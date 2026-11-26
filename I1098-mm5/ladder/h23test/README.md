# I1098-mm5/ladder/h23test: which horizon is right at D 300's h23 (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098
Coordinator's order (t5): the Moebius tail at M 32 and M 48 (a 8, ks 600) shows a converged -3.88e-22 at h23 where the u tail (ks 506) shows about -1e-26.
The jump agent's prediction: the Moebius ks 600 horizon's truncation (1.2e-53 in F), amplified by kfree 23's gain of about 1e38, makes the turn.

Tool: `../tools/h23test.sh` (raw a30ae7df, `I1098-mac-a/tools/h23test.sh`, blob f44db4588c08a96014ac1635817bccfceb25fee2, verified), beside `../tools/variant_state.py` (blob 19b05a5a70e1b6e49f700e176a4d86c265a0ea48, verified).
Inputs (both verified by `git hash-object`): the M 32 h21 states `../D300/tail/release_ls_h21_D300.0000.npz` (Moebius tail, blob fb8e0ff28d1974fb65076ec0684bd0a22c5d1e96) and `../D300u/tail/release_ls_h21_D300.0000.npz` (u tail, blob 3f609c95495bc61f8ff0b7443fa93b2b497aae61).
Six h23-only releases (`release_ls --harm 23 --kmax 31 --jac_by 23:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 3 --outer 8`, fastmul6, Python 478e9d86):
mob_ks800, mob_ks1000 (Moebius a 8), mob_a4, mob_a6 (ks 800) from the Moebius state; u_ks706, u_ks906 from the u state.

## Bar, written before the run (2026-11-26 17:44 UTC, coordinator's order)

- **The prediction holds** if Moebius at ks 800 and at ks 1000 gives an h23 change near u's (about 1e-26, no turn), and u at 706 and 906 stays near u at 506 (pending dDelta about -1.2e-26).
- **The prediction is wrong** if Moebius at ks 800 and ks 1000 still shows about -3.9e-22.

Reported: each run's h23 change (by script from `*/rls.log`) and the verdict. mob_a4 and mob_a6 are read beside them, with no bar set.

## How it is run here

`h23test.sh` starts all six at once (18 threads) and cannot take a subset. D 432 and D 519 (4 threads each) and D300m48 (4) are running, so the six `run` calls of the script are queued two at a time (the same commands, copied from the script's `run` function,
`../h23test/queue_h23.sh`), in the order mob_ks800, mob_ks1000, u_ks706, mob_a4, mob_a6, u_ks906. Nothing about a run's command differs from the script's.

## Results (all six ended 17:57:04 UTC, rc 0; queue 17:44:56 - 17:57:04, 12 min)

By script (`h23_table.py <this folder>`, from each `*/rls.log`). Starts: the Moebius h21 state's Delta 1.678171015400871495985657143659770710284; the u h21 state's Delta 1.678171015400871495985658066888237925236.

| run (horizon) | h23 harmonic step, outer 0 | h23 change in Delta | outer 1 | final Delta |
|---|---|---|---|---|
| mob_ks800 (a 8) | 7.45e-14 | +9.11293e-25 (210.8 s) | step 2.50e-19, pending +2.44e-31, released | 1.678171015400871495985658054953002784621 |
| mob_ks1000 (a 8) | 7.45e-14 | +9.11293e-25 (245.9 s) | the same | the same, to the last digit |
| mob_a4 (ks 800) | 7.45e-14 | +9.11293e-25 (206.2 s) | the same | ...784622 (1.0e-39 from mob_ks800) |
| mob_a6 (ks 800) | 7.45e-14 | +9.11293e-25 (210.5 s) | the same | ...784622 (1.0e-39 from mob_ks800) |
| u_ks706 | 7.45e-14 | none: pending -1.19e-26, released at outer 0 | | 1.678171015400871495985658066888237925236 |
| u_ks906 | 7.45e-14 | none: pending -1.19e-26, released at outer 0 | | the same |
| (the ladder's Moebius ks 600) | 3.54e-10 | M 48: -3.88494e-22; M 32: pending -3.89e-22, inner floor 1.36e-42 | M 48: step 2.08e-19, pending -1.33e-32 | |
| (D300u, u ks 506) | 7.45e-14 | none: pending -1.19e-26, released | | |

- **The turn is gone at ks 800 and 1000**, and the harmonic-23 step is u's (7.45e-14, against 3.54e-10 at ks 600). The inner solve converges in 2 steps (|F| 1.29e-54), where the Moebius M 32 ks 600 run hit a floor (1.36e-42).
  Moebius at ks 800, ks 1000, a 4 and a 6 agree to 1e-39 in Delta: the Moebius horizon is converged in ks and in a over this range. u at ks 706 and 906 is u at ks 506 (the same pending -1.19e-26, the same step).
- **Delta lands on u's.** After h23 the Moebius ks 800 Delta minus u's Delta after h21 is -1.19352e-26 (u's own pending h23 dDelta is -1.19e-26); adding it back leaves -3.5e-29.
- **The bar, read literally.** The prediction is not wrong (no run shows about -3.9e-22). The change "near u's, about 1e-26" is not met as written: the Moebius h23 change is +9.11293e-25 (76x u's pending dDelta). The reason is in the start state, not in h23:
  the ks 600 h21 state's Delta is -9.23228e-25 below u's, and the ks 800 solve re-converges all held harmonics on the finer horizon, which moves Delta by +9.11e-25 and leaves u's h23 shift (-1.19e-26) for the rest.
  So the ks 600 truncation also biased Delta at h21 by about -9.2e-25 (consistent with the above; the h21 bias itself was not run at another ks), and at h23 it is amplified into a -3.88e-22 shift (harmonic step 3.54e-10).
- **Verdict: the prediction holds for the turn.** The h23 turn of the Moebius tail at ks 600 (M 32 and M 48) is horizon truncation (ks), not M and not a property of the Moebius map. D300m48 (ks 600, M 48) showed a further pending +2.07e-22 at h25, of the same kind (u: -1.24e-26).
  The ladder's Moebius tails at ks 600 are not converged in ks past h21.
