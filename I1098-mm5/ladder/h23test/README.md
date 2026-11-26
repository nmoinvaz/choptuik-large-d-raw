# I1098-mm5/ladder/h23test: which horizon is right at D 300's h23 (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098
Coordinator's order (t5): the Moebius tail at M 32 and M 48 (a 8, ks 600) shows a converged -3.88e-22 at h23 where the u tail (ks 506) shows about -1e-26.
The jump agent's prediction: the Moebius ks 600 horizon's truncation (1.2e-53 in F), amplified by kfree 23's gain of about 1e38, makes the turn.

Tool: `../tools/h23test.sh` (raw a30ae7df, `I1098-mac-a/tools/h23test.sh`, blob f44db4588c08a96014ac1635817bccfceb25fee2, verified), beside `../tools/variant_state.py` (blob 19b05a5a70e1b6e49f700e176a4d86c265a0ea48, verified).
Inputs (both verified by `git hash-object`): the M 32 h21 states `../D300/tail/release_ls_h21_D300.0000.npz` (Moebius tail, blob fb8e0ff28d1974fb65076ec0684bd0a22c5d1e96) and `../D300u/tail/release_ls_h21_D300.0000.npz` (u tail, blob 3f609c95495bc61f8ff0b7443fa93b2b497aae61).
Six h23-only releases (`release_ls --harm 23 --kmax 31 --jac_by 23:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 3 --outer 8`, fastmul6, Python 478e9d86):
mob_ks800, mob_ks1000 (Moebius a 8), mob_a4, mob_a6 (ks 800) from the Moebius state; u_ks706, u_ks906 from the u state.

## Bar, written before the run (2026-11-26 coordinator's order, 18:0x UTC)

- **The prediction holds** if Moebius at ks 800 and at ks 1000 gives an h23 change near u's (about 1e-26, no turn), and u at 706 and 906 stays near u at 506 (pending dDelta about -1.2e-26).
- **The prediction is wrong** if Moebius at ks 800 and ks 1000 still shows about -3.9e-22.

Reported: each run's h23 change (by script from `*/rls.log`) and the verdict. mob_a4 and mob_a6 are read beside them, with no bar set.

## How it is run here

`h23test.sh` starts all six at once (18 threads) and cannot take a subset. D 432 and D 519 (4 threads each) and D300m48 (4) are running, so the six `run` calls of the script are queued two at a time (the same commands, copied from the script's `run` function,
`../h23test/queue_h23.sh`), in the order mob_ks800, mob_ks1000, u_ks706, mob_a4, mob_a6, u_ks906. Nothing about a run's command differs from the script's.
