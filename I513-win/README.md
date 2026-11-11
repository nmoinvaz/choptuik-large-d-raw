# I513-win: the wall signature at D 231, win_d10's refused and win_d6's accepted step rerun with --save_dz0

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/513 (follows #462, #499; the coordinator's message `choptuik-large-d/2026-11-11/213340Z-coordinator-7d6f.md`). Worktree `choptuik-i513` at main 14dc3863 (Python only: the venv-t151 build, hpkernel, is the one of #462), 3 threads per run at BelowNormal.

| run | start state (read from I462-win, not copied) | sha256 (first 16) | attempt |
|---|---|---|---|
| run_d10 | I462-win/chain_d10/anm_pin3_D231.1312.npz | c81bf04f7c16fcd1 | a = 1, D 231.13125 -> 232.13125 (refused in #462) |
| run_d6 | I462-win/chain_d6/anm_pin3_D231.1312.npz | 64f8de358ce5851a | a = 1, D 231.13125 -> 232.13125 (accepted in #462) |

The commands are those of `I462-win/d6_long3.cmd` and `d10_long3.cmd` (the resume of 16:27:43 UTC) with `--steps 1` and `--save_dz0 1`, in `i513_d10.cmd` and `i513_d6.cmd`; the exit codes are in `run_d10.exit` and `run_d6.exit`. run_d10 is stopped by hand after its first `-> D` line (the refused attempt), run_d6 ends by itself after its accepted step.

Code that differs on the run path from #462's main cc6d51b: 2967dcd2 (the chain keeps a step found by halving, ends a stalled attempt), e5bbdcd9 (the re-seed's octo-double rung LU is factored again after a poor correction), de63a118 (`--save_base`), 7c8548cb and 14dc3863 (`--save_dz0`).

**Acceptance (the issue's).** Each rerun's first move and |F| per solve equal #462's logged ones to the printed digits (first move 1.0e-29 for the refused step, 2.0e-30 for the accepted one), and max|d0 + d1| of each dz0 file equals the log's first |dz|. #462's logged solves: win_d10 3.88e-33 -> 2.70e-27 (lam 1), -> 1.35e-27 (lam 0.5), then no trial step; win_d6 7.50e-34 -> 1.00e-28 (lam 1), -> 5.02e-29 (lam 0.5), -> 4.88e-48, -> 4.86e-48, -> 4.35e-95.

## Results (2026-11-11)

| run | started | ended | exit | how it ended |
|---|---|---|---|---|
| run_d6 | 21:36 UTC | 23:00:45 UTC | 0 | by itself, step accepted, state `run_d6/anm_pin3_D232.1312.npz` saved |
| run_d10 | 21:36 UTC | 23:17:45 UTC | 1 | stopped by hand (`taskkill`) after the refused attempt's first `-> D` line, about 40 s into the a = 0.5 retry |

The stop watcher for run_d10 (`stop_d10_513.sh`, in the scratch) saw the `-> D` line at about 23:17:04 UTC, but its `taskkill` branch failed on a quoting error (the PowerShell filter lost its quotes, so `Get-CimInstance` printed "Invalid query" and killed nothing). I killed the process tree by hand at 23:17:45 UTC. The retry had written only `pred_pin3_D231.6312.npz` (the a = 0.5 prediction) and no line to the log; its exit code 1 is the kill's. The `dz0` and `pred` files of the refused attempt were written long before.

**Reproduction, #462's logged number against the rerun's, to the digits printed** (`I462-win/chain_d10.log` step into D 232.13125 at a = 1, `chain_d6.log`):

| quantity | #462 win_d10 | rerun | #462 win_d6 | rerun |
|---|---|---|---|---|
| start \|F\| | 3.88e-33 | 3.88e-33 | 7.50e-34 | 7.50e-34 |
| first move \|dz\| | 1.0e-29 | 1.0e-29 | 2.0e-30 | 2.0e-30 |
| dDelta of solve 0 | -1.02e-29 | -1.02e-29 | -1.98e-30 | -1.98e-30 |
| solve 0 \|F\| (lam 1) | 2.70e-27 | 2.70e-27 | 1.00e-28 | 1.00e-28 |
| solve 1 \|F\| (lam 0.5) | 1.35e-27 | 1.35e-27 | 5.02e-29 | 5.02e-29 |
| solve 2 | no trial step accepted | no trial step accepted | 4.88e-48 | 4.88e-48 |
| solve 3 | | | 4.86e-48 | 4.86e-48 |
| solve 4 | | | 4.35e-95 | **6.25e-95** |
| Newton steps, converged | 3, not converged | 3, not converged | 6, converged | 6, converged |
| Delta of the step (12 digits) | 1.688080824630 | 1.688080824630 | 1.688080824659 | 1.688080824659 |
| converged Delta (18 digits) | | | 1.68808082465851705 | 1.68808082465851705 |
| series line (pivots, \|z_N\|, ratios, a_max) | same | same | same | same |

Every number agrees to the digits printed except one: win_d6's last solve leaves \|F\| = 6.25e-95 against #462's 4.35e-95 (the line "max\|F\| 4.3e-95" reads 6.3e-95). That is a miss of the acceptance as written; it is at the arithmetic's floor, and the \|dz\| and dDelta of that solve (3.8e-66 -> 4.0e-79, +4.11e-67) agree. Not tuned, not explained.

Two other lines differ and are not in the acceptance:

| line | #462 win_d10 | rerun | #462 win_d6 | rerun |
|---|---|---|---|---|
| rung max\|R\| (before, after each of three passes) | 5.17e-29 -> 3.10e-62 -> 1.89e-69 -> 1.72e-75 | 3.55e-29 -> 4.69e-62 -> 1.35e-69 -> 7.64e-76 | 3.86e-29 -> 1.68e-62 -> 4.62e-69 -> 5.91e-75 | 3.88e-29 -> 2.18e-62 -> 1.20e-69 -> 7.50e-76 |
| `tol` in the step line | 3.0e-20 | 1.4e-20 | 4.4e-20 | 1.4e-20 |

The `tol` is 1e-20 * 1.45^(D - D_start) (`tol_at` in `anm_run.py`): #462's steps were the 3rd (win_d10, 1.45^3 = 3.05) and the 4th (win_d6, 1.45^4 = 4.42) of a resume, the reruns' are the 1st (1.45), so only the printout differs. By the docstring of `refine_o` the rung's first value is the quad-double polish's remainder, amplified by the mass mode; that the loaded and polished base here, against the state in memory in #462's chain, shifts it is a guess, not tested. e5bbdcd9 changes `refine_o` (a correction that lowers \|R\| by less than a factor 1e4 refactors the LU); every correction printed here lowered it by more than that (after-to-before ratios 1.3e-33, 2.9e-8 and 5.7e-7 in run_d10, 5.6e-34, 5.5e-8 and 6.2e-7 in run_d6), so the new branch did not trigger.

**The dz0 files** (`run_<chain>/dz0_pin3_D232.1312_a1.000000.npz`, keys z0..z7, d0..d7, meta; sha256 first 16: run_d10 e1943f653555688e, run_d6 4008dcb3ddeb33bf):

| file | max\|d0 + d1\| | log's first \|dz\| | d0 at index 768 | max \|d0\| over indices below 768 | z0 at index 768 |
|---|---|---|---|---|---|
| run_d10 | 1.0240582e-29 | 1.0e-29 | -1.0241e-29 | 1.440e-30 | 1.688080824630302 |
| run_d6 | 1.982735e-30 | 2.0e-30 | -1.9827e-30 | 2.735e-31 | 1.688080824658517 |

max\|d1\| is 3.0e-46 and 1.6e-46, below the float64 spacing of d0, so max\|d0 + d1\| equals max\|d0\|. The largest entry of d0 is the last one (index 768), whose value equals the log's dDelta of solve 0 (-1.02e-29, -1.98e-30), and z0 there equals the attempt's Delta. The files are as written by `--save_dz0 1`; the weak-direction analysis (`hp/dz0_weak.py`) is the Mac's.

The base polish of each run also wrote `dz0_pin3_D0.0000_a0.000000.npz` (the polish's start and first step, 3 Newton steps, max\|F\| 3.4e-89), kept in the folder.
