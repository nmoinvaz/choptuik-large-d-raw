# I562-mac: the held-offset homotopy of #562's main arm (probes, controls, traces)

Machine mac (the shared Apple M5 Mac, 4 threads at nice 10), issue https://github.com/nmoinvaz/choptuik-large-d/issues/562 (the main arm, subagent).
Code: `hp/held_homotopy.py` on branch `wip/i562-subagent` of the code repository (commits named per file below).
Inputs: `I562-win2/renode_0975_D242.3642.npz` (the 0.3, 0.4, 0.5, 0.6, 0.975 start) and `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (crawlJ's 0.7 state).

| file | what | code | exit |
|---|---|---|---|
| `probe_real_v1_float_offset.*` | first probe of the real start; its chord ladder below h = 1e-16 is wrong (the offset was formed with the float 1 - t, which is 1 there) | f118357 | 0 |
| `probe_real.*` | the probe of the real start, offset fixed: t = 0 check, tangent, weak basis, Delta's linear response by rows, chord ladder h = 1e-0..1e-46; `probe_real_setup.npz` holds a, b (= r0), tau0, V, sigma, h0 | ae2afa7 | 0 |
| `fd_tau.log` | finite differences of the residual along tau0 (h = 1e-40, 1e-50, 1e-60) against -b = J tau0; the f64 V rows are not accurate enough to show sigma (stopped before its Jacobian part) | scratch script | stopped |
| `mut_sign.*` | control `--mutate sign`: the t = 0 check must fail | 4d37ece | 1 (as it must) |
| `test_planted_f64w.*` | first planted code test, w in f64: discarded, since tau0's f64 rounding (1e-16 of it in strong directions) reaches the weak rows through the mixed curvature (planted tangent 1.4e-15 in Delta against \|w\| 2.5e-17); stopped during rung 0 | 4d37ece | stopped |
| `test_planted_2rungs.*` | code test with w in eight parts (eps 2.5e-17): rung 0 to t = 0.01 accepted after 2 corrections (1.2e-20, 4.6e-24, then 5.4e-31 below tol), Delta - Delta0 +5.32e-19; stopped during rung 1, the loop being shown | 1c38a4b | stopped |
| `run_mac_tests.sh`, `exits.txt` | the linear planted tests (eps 1e-25, h_max 1: one rung, the endpoint polish and the planted check; then `--mutate tsign`, which must fail) | 6dcadb8 | see below |
| `test_lin.*` | planted, linear regime: one rung to t = 1, endpoint max\|H\| 3.0e-52 -> 4.8e-85, max\|z(1) - zP\| 7.3e-59 against 1e-32: pass | 6dcadb8 | 0 |
| `test_lin_tsign.*` | its control `--mutate tsign`: the trace goes to z0 - w, max\|z(1) - zP\| 2.0e-26 against 1e-32: FAIL, as it must | 6dcadb8 | 1 |
| `freeze_jac_0975.*` | `hp/freeze_jac.py`: the projector's rounding dJ on the weak directions, \|\|dJ v_i\|\| = 2.05, 2.12, 2.12, 2.17 sigma_i; \|\|dJ\|\|_2 1.16e-31; check (dJ v against the residuals' difference) pass | 2d4a9a3 | 0 |
| `freeze_jac_0975_mut.log` | its control `--mutate=scale`: 0.01 against 1e-3, FAIL, as it must | 2d4a9a3 | 1 |
| `freeze_jac_uw_0975.*` | `--uw=1`: W = U^T dJ V equals diag(sigma) to 4 digits for i = 2..4, so the exact rows' weak block diag(sigma) - W has singular values 1.87e-37, 1.81e-38, 1.69e-38, 2.82e-39 (first-order model); check (1 / \|J^-T v_i\| = sigma_i to 1e-3) pass | 2d4a9a3 | 0 |
| `run_i562_main.sh` | the traces sent to win2 (planted, tsign, real, the 0.7 control at -rho and +rho, planted beyond the fold); their output goes to `I562-win2/` | 6dcadb8 | sent |
