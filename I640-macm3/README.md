# I640-macm3: release the chain's held harmonics at D 80, 100, 150, 200 (the fitted method's measured error)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, hpkernel cp314 neon of 2026-11-09, quad-double kernel; the coordinator: fine below D 215), worktree ~/Source/choptuik-large-d-b640 at main 9839474 (hp/release_held.py). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/640 (queued for macm3 by the coordinator's message of 2026-11-13 04:57 UTC, after #632). Inputs are read from the raw-repo clone ~/Source/choptuik-large-d-raw-push (up to date; the live clone is never pulled): T81/conv_pin5_D73.0000_D73.000000.npz and T138-win2/chain/anm_pin3_D{80,100,150}.0000.npz, T138-win2/chain_o/anm_pin3_D200.0000.npz.

Commands (run_640.sh), from hp/, nice 10, caffeinate -is, 2 threads per run, three runs at once. Step 1, the planted control on T81's D 73.0 full-system state: python3 -u release_held.py control_unperturbed/release.jsonl STATE --kfreeze=13; the same with --perturb=1e-10 (control_perturbed); the same with --perturb=1e-10 --it_max=0 (control_noreleas). compare640.py then checks the perturbed release equals the unperturbed one (Delta within 1e-25, coefficients within 1e-20) and that the no-release run does not (the run stops if either is wrong). Step 2: python3 -u release_held.py releases/release_D${D}_kf${K}.jsonl STATE_D --kfreeze=K for D in 80, 100, 150, 200 and K in 13, 9, 7 (12 runs). Each run's records, logs and released states (released_kf*_D*.npz next to the jsonl) are in its folder.

Written before the run (the issue's and the coordinator's comment of 2026-11-13 04:56 UTC). Control: the unperturbed release converges in 3 steps to |F| 3.3e-53 with Delta - the state's Delta = -2.76e-23 (the floor); the perturbed one equals it exactly; the --it_max=0 run is 1e-10 off in coefficients and 2.76e-23 in Delta, so the comparison fails as it must. Then for each (D, K): converged or not, |F| at the start and the end, Delta_released - Delta_held; where a release converges, that difference is the fitted method's measured error at that D, tabled against the row's "fits" err in delta_all.csv (4e-14 to 3e-11); where it does not, the stall's |F| and step are reported, and that D is where the fit stays necessary. About 2 h.

## Results (05:56 UTC; exits.txt: control passes 05:19:05; the 12 releases all exit 1, D 80 at 05:25:52 to 05:42:54, D 100 at 05:46:09 to 05:47:23, D 150 at 05:51:02, D 200 at 05:55:18 UTC)

Control (control_result.txt): the perturbed release equals the unperturbed one exactly (dDelta 0, dcoeff 0), the --it_max=0 run fails the comparison (coefficients 1.0e-10 off against 1e-20; its Delta differs by 8.4e-28, under the 1e-25 limit). The unperturbed release moves Delta by -8.387e-28 (the coordinator's run: -2.76e-23).

| D | K (kfreeze) | converged | steps | |F| at the start | |F| at the end | Δ_released − Δ_held | fits err (delta_all.csv) | last Newton step |dz| (rejected) | seconds |
|---|---|---|---|---|---|---|---|---|---|
| 80 | 13 | stalled | 5 | 4.62e-24 | 8.03e-19 | (+1.217e-14, not a measurement: not converged) | 4.2e-14 (fits d10) | 4.8e-13 | 407 |
| 80 | 9 | no (iteration limit) | 12 | 3.31e-06 | 8.50e-09 | (+7.848e-11, not a measurement: not converged) | 4.2e-14 (fits d10) | (iteration limit) | 1429 |
| 80 | 7 | stalled | 5 | 2.99e-05 | 2.57e-05 | (+5.009e-08, not a measurement: not converged) | 4.2e-14 (fits d10) | 2.4e-05 | 997 |
| 100 | 13 | stalled | 2 | 4.32e-23 | 2.75e-09 | (+2.015e-14, not a measurement: not converged) | 1.2e-12 (fits d10) | 1.2e-07 | 269 |
| 100 | 9 | stalled | 2 | 1.99e-06 | 1.87e-06 | (-5.491e-13, not a measurement: not converged) | 1.2e-12 (fits d10) | 1.9e-06 | 269 |
| 100 | 7 | stalled | 1 | 1.95e-05 | 1.95e-05 | (+0.000e+00, not a measurement: not converged) | 1.2e-12 (fits d10) | 1.8e-05 | 195 |
| 150 | 13 | stalled | 1 | 1.79e-22 | 1.79e-22 | (+0.000e+00, not a measurement: not converged) | 1.1e-11 (fits d6) | 1.5e-04 | 219 |
| 150 | 9 | stalled | 1 | 8.87e-07 | 8.87e-07 | (+0.000e+00, not a measurement: not converged) | 1.1e-11 (fits d6) | 1.1e-06 | 219 |
| 150 | 7 | stalled | 1 | 9.99e-06 | 9.99e-06 | (+0.000e+00, not a measurement: not converged) | 1.1e-11 (fits d6) | 9.7e-06 | 219 |
| 200 | 13 | stalled | 1 | 5.09e-26 | 5.09e-26 | (+0.000e+00, not a measurement: not converged) | 2.8e-11 (fits d6) | 1.3e-06 | 255 |
| 200 | 9 | stalled | 1 | 5.41e-07 | 5.41e-07 | (+0.000e+00, not a measurement: not converged) | 2.8e-11 (fits d6) | 1.0e-06 | 255 |
| 200 | 7 | stalled | 1 | 6.81e-06 | 6.81e-06 | (+0.000e+00, not a measurement: not converged) | 2.8e-11 (fits d6) | 1.3e-04 | 254 |

No release converged. kfreeze 13 starts from |F| 5e-26 to 4e-23 at D 80 to 200 (the held state satisfies the full system) and either takes steps that raise |F| (D 80, D 100) or none (D 150, D 200: the first Newton step is rejected, the state is unchanged, Delta difference exactly 0). Delta_released - Delta_held of a run that did not converge is not a measurement.
