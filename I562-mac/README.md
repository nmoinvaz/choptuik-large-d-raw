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
| `c2_probe_real.*` | on #523's cadcaf1 kernel (freeze projector in octo-double; its checked wheel in a scratch target, `hpkernel.__file__` printed on the first line; main's Python scripts, which cadcaf1 does not change): the 0.975 start's probe. Pinned max\|F\| 4.851e-36, all in n3>n4 (horizon rows 8.15e-43); raw sigma 2.818e-39, 1.745e-38, 1.740e-38, 1.874e-37; tau0 norm 2.302e-2, max 2.276e-3, Delta -1.171e-4; chord correction 2.816e30 h^3 along +tau0, h0 1e-18 | held_homotopy.py 2d4a9a3 | 0 |
| `c2_nn_0975.*` | `near_null.py --keep_plan=1` on cadcaf1 at the 0.975 start: check pass (\|\|J v_1\|\| / sigma_1 = 1.000000), the same sigma and pinned step | main's near_null.py | 0 |
| `c2_probe_07.*` | on cadcaf1, crawlJ's 0.7 state: pinned max\|F\| 1.616e-34 (#494's e, horizon p rows k <= 3); raw sigma 2.551e-27, 2.530e-27, 4.392e-26, 7.930e-26; tau0 norm 2.548e-8, max 3.375e-9, Delta +2.148e-9; chord correction 2.18e35 h^3 (h <= 1e-22) and 1.35e55 h^4 (1e-18 <= h <= 1e-2); h0 1e-24: the linear window ends near h 4e-23 of the step | held_homotopy.py 2d4a9a3 | 0 |
| `nn_k6_0975.log` | near_null k = 6 on main's kernel for sigma_5, stopped by me when the cadcaf1 test superseded it | main's near_null.py | stopped |
| `test_rule2_real_1rung.*` | code test of rule 2 on the real start (main's kernel), rung 0 only: the predictor's max\|H\| 8.2e-38 is now corrected, 6.1e-68 after one correction (corrections 2.2e-38, 3.6e-39), Delta - Delta0 -1.4227e-20; exit 3 is the rung limit | 1161f49 | 3 (limit) |
| `run_562d.sh`, `polish_c2_s242.log`, `exits.txt` | on cadcaf1, a direct base polish of crawlJ's D 242.3642 state (main d020d58's anm_run.py, crawlJ's flags, the stored plan, `--tol_od 1e-60`): step 0 at lam 1/128 took max\|F\| 1.62e-34 -> 7.16e-22, step 1 at lam 1/2 -> 4.20e-21; stopped by me as not converging (#523's runs at 44a0e702 failed alike), so no renode | main d020d58 + cadcaf1 wheel | 143 (stopped) |
| `run_i562_rule2.sh` | the rule-2 traces for win2 (a rung also needs max\|H\| <= 1e-6 h max\|b\|): planted, real, the 0.7 control at -rho and +rho; output to `I562-win2/hh2_*` | 1161f49 | sent |
| `run_i562_main.sh` | the traces sent to win2 (planted, tsign, real, the 0.7 control at -rho and +rho, planted beyond the fold); their output goes to `I562-win2/` | 6dcadb8 | sent |
