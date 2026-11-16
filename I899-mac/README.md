# I899-mac: the linear return of a Δ move at D 252.6135, from a re-converged truth

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/899

Code: wip/xf-900 (main 1dee59e4, #884's 6118a8be, and ea36b6c0), on main 3c35f0c's hpkernel, from the
choptuik-large-d-900 worktree. One process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). Runs in
`queue.sh` order, after I900-mac's queue.

`truth_restep.py store` takes two plain pinned Newton steps from the stored truth I603-win2/chain/anm_pin3_D252.6135.npz
and saves I899-mac/anm_pin3_D252.6135_u2.npz, read with the truth's held values (#884). From it (`u2/`) and from the
stored truth (`truth/`), `step_spread.py` moves the Δ block by seed 1 at rel 1e-93, 1e-94 and 1e-95 and seed 3 at
1e-95, whose Δ sign is opposite. `oddeven.py` reads the odd part L and the even part n of the two seeds' returns at
1e-95, as `I857-mac/tables.py` does. #856's quadratic, q −2.686175e+89 (I856-mac/qcheck.log), puts the even part at
about 1.6e-6 of the move at 1e-95 (`oddeven.py --selftest`'s planted case).

The truth_restep check's bounds were shown to fail on a stored truth by #874 (I874-mac/check_truth.log); here the
store's first step is the truth's own.

Deferred, before any run: the coordinator stopped the queue on 2026-11-16 at 04:03 UTC, pending a math review
of the wall's cause (label blocked). The code is on wip/xf-900 (ea36b6c0); `queue.sh` is ready to run as
written. `oddeven.py --selftest` passes.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | the store reads back equal; `check` of the re-converged state passes #874's bounds (max\|dz\| / max\|z_h\| ≤ 1e-97, pinned max\|F\| ≤ 1e-92), with held offsets equal to the truth's (difference 0) | not converged, or the system differs |
| C2 | `--ref` passes in all six runs (the truth's dΔ 5.2645963792835124e-82, `check_u2.json`'s from u2); `power`'s same-start check passes and `power --mutate start` FAILS, from each start | the unperturbed step changes, or the control passes |
| C3 | `oddeven.py --selftest` passes (linear passes, 2% off fails on L, a floor of 1e-2 fails on n); `--mutate samesign` FAILS from each start | a planted case is misread, or the control passes |
| C4 | from u2: L in [0.99, 1.01] at 1e-95 and n < 1e-3 there | either fails |
| C5 | reported: the same readings from the stored truth, and L from the truth less L from u2 (the cross term at 252.6) | (reported) |
