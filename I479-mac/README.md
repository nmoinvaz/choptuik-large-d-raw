# I479-mac: held_schur.py singular values for the big-picture figure

Machine: mac (Apple M5). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/479

The Schur complement S = dg/dh of the ten held coefficients (p1's harmonics 5-13) at chain states, from
`hp/held_schur.py` (main repository), its singular values per harmonic, and the logs. Each run has a `.log` (stdout,
ending in its exit code) and a `.json` (`--json`). `hp/data/held_grip.csv` in the main repository is derived from the
`_exact_e70` and `_exact_od` files by `hp/held_grip.py`.

| files | state | options | check |
|---|---|---|---|
| schur_D79.7657 | anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz | differences at 2^-40 (the run of notes/HELD_HARMONICS.md 4.3) | FAIL (differences unresolved) |
| schur_D79.7657_exact | the same | --jac=exact | pass |
| schur_D79.7657_ctl_jac_scale | the same | --jac=exact --mutate=jac_scale (control) | FAIL, as it must |
| schur_D79.7657_ctl_pinned_rows | the same | --jac=exact --mutate=pinned_rows (control) | FAIL, as it must |
| schur_D79.7657_exact_e70 | the same | --jac=exact --eps_pow=70 | pass |
| schur_D100.0000_exact, _exact_e70 | T138-win2/chain/anm_pin3_D100.0000.npz | --jac=exact; with --eps_pow=70 | FAIL (none resolved); pass |
| schur_D150.0000_exact, _exact_e70 | T138-win2/chain/anm_pin3_D150.0000.npz | the same | FAIL (none resolved); pass |
| schur_D150.0000_exact_od | the same | --jac=exact --od --eps_pow=100 | pass |
| schur_D200.0000_exact | T138-win2/chain_o/anm_pin3_D200.0000.npz | --jac=exact (quad-double) | FAIL; cosine-sine pairs broken |
| schur_D232.6312_exact | I461-win2/crawlG/anm_pin3_D232.6312.npz | --jac=exact (quad-double) | FAIL; cosine-sine pairs broken |
| schur_D175.0000_exact_e70 | T138-win2/chain_o/anm_pin3_D175.0000.npz | --jac=exact --eps_pow=70 (quad-double) | FAIL (differences unresolved) |
| schur_D175.0000_exact_od | the same | --jac=exact --od --eps_pow=100 | pass |
| schur_D200.0000_exact_od | T138-win2/chain_o/anm_pin3_D200.0000.npz | --jac=exact --od --eps_pow=100 | FAIL: sigma_1 3.0e-17 below the default floor 1e-14 |
| schur_D200.0000_exact_od_s25 | the same | the same with --sigma_min=1e-25 | pass |
| schur_D200.0000_ctl_pinned_rows_s25 | the same | --jac=exact --eps_pow=70 --sigma_min=1e-25 --mutate=pinned_rows (control) | FAIL, as it must (sigma_1 1.3e-33) |
| schur_D232.6312_exact_od | I461-win2/crawlG/anm_pin3_D232.6312.npz | --jac=exact --od --eps_pow=100 (stopped by hand: the default floor would fail) | log only |
| schur_D232.6312_exact_od_s25 | the same | --jac=exact --od --eps_pow=100 --sigma_min=1e-25 | FAIL: differences agree to 1.1e-3, over the 1e-3 bound |
| schur_D232.6312_exact_od_s25_e110 | the same | the same with --eps_pow=110 | pass |
