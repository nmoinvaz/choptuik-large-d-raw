# I841-dh370: a chain on a new plan from #808's converged re-planned state at D 251.8859, to the fold

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/841.

`run841.sh` (written by the coordinator, md5 22e08cd3, run unedited by absolute path): `anm_run` from
`I808-dh370/s251.8859_plandrop/base_pin3_D251.8859.npz` (max|F| 2.1e-64 on its own 23-step plan, kept), #603's flags
(`--held_fit data/held_fit.json`) plus `--od_full_drop 1e-2` (#836), `--od_abort_theta 1e8 --od_abort_it 2` (#784), `--save_jet 1`
and `--D_max 259.95`, 12 threads at nice 10; worktree choptuik-large-d-841 at main 0cfff3c4, venv-i800.
`run841.sh pilot` (unit `i841p`): two steps, each must converge to max|F| <= 1e-60; then `run841.sh chain` to D_max 259.95.
Output: `chain.log`, `chain/` (states `anm_pin3_D*.npz`, series `jet_pin3_D*.npz`, predictions, `anm_run.jsonl`), `exits_841.txt`.

## Results (dh370, 2026-11-15 to 2026-11-17)

What ran. Unit `i841p` (`run841.sh pilot`), 12:33:29 to 13:51:13 UTC on 2026-11-15, exit 0: the two steps converged to max|F| 7.4e-73 (D 252.3859)
and 2.3e-65 (D 252.8859). Unit `i841c` (`run841.sh chain`, 12 threads at nice 10), from D 252.8859 at 13:51:27 UTC on 2026-11-15
until I stopped it with `systemctl --user stop i841c` at 12:58:53 UTC on 2026-11-17 (47 h 07 min), on the coordinator's order after
the D* verdict below. No Traceback and no non-zero exit; the stop is the last line of `exits_841.txt`.

What it holds. `chain/` has 59 states `anm_pin3_D*.npz` from D 252.3859 to 259.665356828 and 59 series `jet_pin3_D*.npz` (8 parts) from
D 251.8859 to 259.6470; the last state's series (D 259.6654) was being built and is not saved. The last state converged at a = 0.0184
in 19 octo-double steps, max|F| 3.5e-86, Delta 1.649398990376264106. There were 78 attempts, 59 accepted and 19 refused. The abort rule
(`--od_abort_theta 1e8`) refused 13 of them at iteration 1, and 17 of the 19 refused attempts were grown (x1.25) attempts, the other two
the a = 1 trials at the start. Each refusal was followed by a halved attempt that converged. The step bound a_max fell from 1.677
(D 251.89) to 0.080 (D 259.647) and the accepted a from 0.5 to 0.012 to 0.018, so the 13 states from D 259.4364 on took 45 to 85 min each.

The verdict (not computed here). The coordinator's agent xfkappa ran #903's fold rule, `hp/fold_est_903.py verdict` (main 3c1b9582), on
`chain/` and posted it on #841 (comment 6948684048; `I903-mac/fold/verdict_841.log` at d5b4d2b0): D*(#841) = 259.90361142 from 14
counted bases in 259.40 to 259.65, with 7e-7 spread over those bases, against D*(#603) = 259.90330383 under the same estimator,
3e-12 spread; the shift is +3.08e-4. Both spreads are spreads over approximants, methods and bases, not bounds.

Not run here. The acceptance's check that each series meets its neighbours' states to 1e-15 (no script was placed), and the chain's
Delta against track C's series at each state.
