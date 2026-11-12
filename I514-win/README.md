# I514-win: win_d6's and win_d10's step D 229.13125 -> 230.13125 re-solved with the other chain's held fit

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/514 (follows #462; the coordinator's message `choptuik-large-d/2026-11-11/213340Z-coordinator-7d6f.md`). Worktree `choptuik-i513` at main 14dc3863 (Python only, the venv-t151 build of #462), 3 threads per run at BelowNormal, at most two runs at once.

Each run is one attempt at a = 1 from a stored state of #462 (read from `I462-win`, not copied), with the commands of `I462-win/d6_long3.cmd` and `d10_long3.cmd` and `--steps 1`, in `i514_<run>.cmd`; the exit codes are in `run_<run>.exit`. A run that is refused would halve and try again, so it is stopped by hand after its first `-> D` line (`stop_514.sh` in the scratch), and an accepted step ends by itself.

| run | start state (sha256, first 16) | held fit (sha256, first 16) | what it is |
|---|---|---|---|
| run_s6f10 | chain_d6/anm_pin3_D229.1312.npz (fd7f22f3a3d59689) | held_fit_d10.json (f970a8f97826e448) | swap: d6's state, d10's fit |
| run_s10f6 | chain_d10/anm_pin3_D229.1312.npz (644083bfcac95ca0) | held_fit_d6.json (bc4403ace795fdb0) | swap: d10's state, d6's fit |
| run_s6f6_a | chain_d6/anm_pin3_D229.1312.npz | held_fit_d6.json | control, d6's own fit |
| run_s6f6_b | chain_d6/anm_pin3_D229.1312.npz | held_fit_d6.json | the same command as run_s6f6_a |

**#462's originals at D 230.13125** (the step into D 230 of `chain_d6.log` and `chain_d10.log`): win_d6 Delta 1.68846054003310231 (last residual 1.95e-95), win_d10 Delta 1.68846054000988466 (last residual 2.50e-84).
win_d10's step was the first of its process (loaded from the stored state, base polished, D_start 229.13125, the same start as run_s10f6 and run_s6f10 have), win_d6's was the second after the resume at 228.13125, so its base was the previous step's accepted state in memory and not a loaded one. The control pair starts from the stored state, which the original d6 step did not.

**Acceptance (the issue's, can fail; the coordinator found its first half ill-posed after run_s6f10, message 002859Z).** With the held values taken relative to the base, v(D) = v(D0) + fit(D) - fit(D0) (`hp/anm_run.py` lines 35 to 40), a one-step swap can show only the fit's increment over that step, not the whole gap between the chains, so "the swapped Deltas equal the originals exchanged" could not hold. The results below give the one-step share both ways and the control's spread instead. If the swapped Deltas equal the originals with the chains exchanged, to the digits printed (run_s6f10 against win_d10's 1.68846054000988466, run_s10f6 against win_d6's 1.68846054003310231), the difference is the fit's. Control: run_s6f6_a and run_s6f6_b give Deltas that differ by less than 1e-20. The control uses d6's fit and state because it is the cheaper of the two and the only pairing for which #462 has no rerun from a stored state; run_s6f6_a also shows whether the stored state alone reproduces the original d6 Delta.

Code that differs on the run path from #462's main cc6d51b: 2967dcd2, e5bbdcd9, de63a118, 7c8548cb and 14dc3863 (see `I513-win/README.md`).

## Results (2026-11-12)

| run | state, fit | started (UTC) | ended (UTC) | exit | Delta at D 230.13125 (exact, from the saved state) |
|---|---|---|---|---|---|
| win_d6 original (#462) | d6, d6 | | | | 1.68846054003310231294 |
| win_d10 original (#462) | d10, d10 | | | | 1.68846054000988470951 |
| run_s6f10 | d6, d10 | 23:05 | 00:25:11 | 0 | 1.68846054003298485017 |
| run_s10f6 | d10, d6 | 23:18 | 00:45:05 | 0 | 1.68846054001000220923 |
| run_s6f6_a | d6, d6 | 00:26 | 01:52:45 | 0 | 1.68846054003310231294 |
| run_s6f6_b | d6, d6 | 00:46 | 02:05:47 | 0 | 1.68846054003310231294 |

All four steps were accepted at a = 1; no Traceback; each ended by itself (the stop watchers saw the `-> D` line and found nothing to kill). The Deltas are the sum of the eight parts of entry 768 of each run's `anm_pin3_D230.1312.npz`, added exactly (Python `Fraction`); the 18-digit `converged, Delta` lines of the logs omit the second term (for example `+4.5440e-18`), so the differences in the earlier #514 posts, which used the 18-digit lines, differ from these in the 4th digit (run_s10f6 minus win_d10's original is +1.1750e-13, not +1.1746e-13).

**One-step share of the fit** (gap between the originals 2.32176e-11, the error bar at D 230.131):

| comparison | difference | share of the gap |
|---|---|---|
| run_s6f10 minus run_s6f6_a (d6 state, fit d10 against fit d6) | -1.17463e-13 | 0.50592% |
| run_s10f6 minus win_d10's original (d10 state, fit d6 against fit d10) | +1.17500e-13 | 0.50608% |
| run_s6f10 minus run_s10f6 (the swapped pair's gap) | 2.29826e-11 | 98.99% of the original gap |

The two shifts are equal and opposite to 3 digits (their sum is 3.7e-17). Their sum, 2.3496e-13, is 14.6% of the 1.609e-12 by which the gap grew in this step (2.1609e-11 at D 229.13125 and 2.3218e-11 at D 230.13125, from the 18-digit lines of #462's logs); that holds if each state responds linearly to its fit, and is arithmetic on these Deltas, not a separate measurement.

**Control** (the same command twice from win_d6's stored D 229.13125 state with d6's fit): run_s6f6_a and run_s6f6_b have byte-identical saved states (sha256 107d4c2d41aed77e both); the difference of Delta is 0 and the largest difference over the 769 entries of the eight-part states is 0.0, against the criterion below 1e-20. Both match win_d6's original step, which ran from a state in memory: Delta differs by 6.95e-88 and the largest entry by 1.6e-87.

**Log numbers of the step** (the originals from `I462-win/chain_d6.log` and `chain_d10.log`):

| run | Newton steps | halved solve | start |F| | first move | plateau | final |F| | series, re-seed, Newton (s) |
|---|---|---|---|---|---|---|---|
| win_d6 original | 6 | yes | 7.08e-34 | 4.4e-31 | 1.23e-48 | 1.95e-95 | 2812, 183, 1142 |
| win_d10 original | 6 | yes | 3.78e-33 | 1.8e-30 | 6.80e-43 | 2.50e-84 | 2768, 194, 1121 |
| run_s6f10 | 5 | no | 8.06e-34 | 3.7e-31 | 3.37e-47 | 2.53e-95 | 3209, 224, 845 |
| run_s10f6 | 6 | yes | 3.72e-33 | 2.0e-30 | 6.49e-43 | 2.21e-84 | 3129, 228, 1275 |
| run_s6f6_a | 6 | yes | 7.08e-34 | 4.4e-31 | 1.23e-48 | 2.68e-95 | 3201, 221, 1209 |
| run_s6f6_b | 6 | yes | 7.08e-34 | 4.4e-31 | 1.23e-48 | 2.68e-95 | 3181, 233, 811 |

The Newton steps of run_s6f6_a, run_s6f6_b and win_d6's original agree to the digits printed in every solve except the last: 2.68e-95 in both runs and 1.95e-95 in the original (the same kind of difference as #513's win_d6 rerun, 6.25e-95 against 4.35e-95, whose saved state at D 232.13125 differs from #462's by at most 3.9e-85 over the entries). The two identical runs agree with each other in every number but the timings, so the last residual is reproducible in this configuration; the difference from #462's number is therefore not noise within it. The candidates are the code (the five commits), the loaded and polished base against the state in memory, and the machine's load; none is tested.

Series line at the base D 229.13125 (|z_N|, fourth ratio, a_max): win_d6 original 1.53e-29, 252.9, 3.135 (the same in run_s6f6_a and run_s6f6_b); win_d10 original 8.03e-29, 226.6, 2.917; run_s6f10 1.68e-29, 252.5, 3.122; run_s10f6 7.89e-29, 227.1, 2.919. The series follows the state and moves a little with the fit.

Horizon rung of the refinement (before, then after each of three passes): win_d6 original 1.34e-29 -> 1.18e-62 -> 1.39e-70 -> 2.49e-76; run_s6f6_a and run_s6f6_b 1.88e-29 -> 1.60e-49 -> 6.87e-56 -> 2.84e-62 (identical in the two); win_d10 original 2.25e-29 -> 5.57e-53 -> 3.83e-59 -> 1.06e-65; run_s10f6 1.38e-29 -> 5.19e-50 -> 3.35e-56 -> 2.17e-62; run_s6f10 2.25e-29 -> 1.14e-62 -> 1.24e-69 -> 6.03e-76. All end below the OK bound 1e-50. Both controls differ from win_d6's original in the rung by 14 orders at the end while the saved state agrees with it to 1.6e-87, so the rung's path does not reach the state.
