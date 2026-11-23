# I1025-win2/kc79_leap: the k_c 79 march past D 20.75 (regrids of leg 3's D 20.5 and D 20.75, then a k_c 79 leap leg)

Machine: win2 (desktop-pc, Windows 11, 20 logical cores). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 12:18 UTC, before any run of this task.

## The order (the coordinator's hc, 2026-11-23 ~12:20 UTC, verbatim)

"Next, beside leg 4 (#1025 comment of 12:20 UTC): (1) regrid leg 3's k_c 71 states at D 20.5 (blob 63399965) and D 20.75 (blob fe8503cc) to k_c 79, both at once, 8 threads each, lam0 from lam0_at, tags l1kc79win2d205 and l1kc79win2d2075, accepted by kc79_syscheck (selftest 0, both controls exit 1); (2) then a k_c 79 leap leg from those two states, run_leap4.sh's pattern with k_c 79, tag l1kc79Lw1025d, h 0.03125, the same guard and stop rules, 12 h cap; (3) report each point with Delta, dDelta/dD, sigma_reg, |J+dF/dn|, h, constraint, |F|, beside leg 4's at the same D. Written before (README): resolution if k_c 79's sigma_reg stays above leg 4's and dDelta/dD does not turn; real if both turn within ~0.1 in D. Headless, no root-level files, no rm."

Later the same day (hc ~12:30 UTC), after my report that rule (2) of leg 4's guard (sigma_reg < 1e-12) cannot fire (sv_reg_small is above the null cutoff 1e-12 sigma_max by construction; at D 20.75 the "fall" of sigma_reg was a mode entering the regular set, n_null 64 -> 63, tangent |cos| <= 0.051 on the four weakest regular modes): "both findings accepted, and my rule (2) was wrong... Adopt your rule in both legs' guards: stop when max cos_t_reg >= 0.5, or when n_null rises by one with that cos >= 0.3; keep rule (1) (dDelta/dD changes sign); print n_null, the cutoff and max cos_t_reg in every row (leg 4's rows from its record file). Restart leg 4's guard with it (the guard only, not the leap; the same planted end-to-end tests plus one for the cos rule and its mutation first). Keep the k_c 79 leg: k_c 71's Delta correction grows fast (-9.9e-6 at D 20, -2.2e-5 at 20.5), so it becomes the march past D 20.75; leg 4 runs on as the pathfinder."

## Inputs (pinned by git blob; copies in `inputs/`)

| file | blob |
|---|---|
| `kc71_syscheck.py` | 4cd86cd4 |
| `kc79_syscheck_1025.py` | 29dce7ea |
| `sol_l1kc71Lw1025c_D20.500000.npy` (leg 3's D 20.5 state) | 63399965 |
| `sol_l1kc71Lw1025c_D20.750000.npy` (leg 3's D 20.75 state) | fe8503cc |
| `l1kc71Lw1025c_leg3.jsonl` (leg 3's 12 records) | b4f4bba7 |

Code: worktree `D:/choptuik-i1025k79` at 48c36355 (solver code = 505d8399; `ell_refine.py` 631e5801, `ell_delta.py` fde699f5, `ell_leap.py` 1eb873e4).

## Step 1: the two regrids (`regrid79x.sh D TAG SRCBLOB LAM0`, both at once)

As at D 20.25 (`../kc79_d2025/`): `ell_refine.py l1kc71Lw1025c 71 TAG 79 1 D LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 8 threads each (16 of the 20 logical cores; leg 4 holds 4), Normal priority, cap 21600 s by the exact root pid, no retry. `LAM0 = ell_delta.lam0_at(D, *lam0_table())` (unused with `--no-gamma`):

| D | tag | lam0 (error) |
|---|---|---|
| 20.5 | l1kc79win2d205 | 2.1088217835 (4.1e-7) |
| 20.75 | l1kc79win2d2075 | 2.1077704855 (2.7e-7) |

Source first: `kc71_syscheck.py` accepts each source against leg 3's record file (dry run 12:15 UTC: D 20.5 |F| 4.8617e-10, 2453 steps; D 20.75 |F| 4.8238e-10, 2427 steps; controls refused; `--mutate=F` and `--mutate=steps` exit 1). Result accepted only by `kc79_syscheck_1025.py` (selftest 0, controls refused, `--mutate=F` and `--mutate=steps` exit 1) with `kc71_syscheck.py` refusing it. A refusal, a failed control or a regrid that does not converge stops with a report; no retry.

## Step 2: the k_c 79 leap (written before it starts; `run_leap5.sh`, to follow)

`ell_leap.py l1kc79Lw1025d 1 79 data/sol_l1kc79win2d205_D20.5000.npy 20.5 data/sol_l1kc79win2d2075_D20.7500.npy 20.75 21 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`, the pattern of `../kc71_leap/run_leap4.sh` at k_c 79: 4 BLAS threads, BelowNormal, headless, cap 43200 s by the exact root pid. It starts by itself when both regrids are accepted (and the seeds pass the checks again). The seed pair is 0.25 apart (leg 4's is 0.0625), so the first secant predictor extrapolates over 0.125 of the seed difference; a failed first solve halves h as always.

Guard (the coordinator's rule, adopted at ~12:30 UTC): stop the leap when (1) dDelta/dD changes sign, or (2) the largest `cos_t_reg` is >= 0.5, or n_null rises by one with that cos >= 0.3. Every row prints n_null, the null cutoff (1e-12 sigma_max) and the largest cos_t_reg.

Written before the leap (the coordinator's): **resolution** if k_c 79's sigma_reg stays above leg 4's and dDelta/dD does not turn; **real** if both turn within about 0.1 in D. Both legs' sigma_reg are read with n_null and the cutoff beside them (a mode entering the regular set from below the cutoff makes sigma_reg fall without any mode falling).

## Step 2: launch (written 12:31 UTC, before the leap starts)

`launch_leap5.ps1` starts, outside the terminal (headless, BelowNormal, through `../kc71_leap/cim_start.ps1`): the driver `run_leap5.sh`, which waits for `regrid_accepted_D20.5000.txt` and `regrid_accepted_D20.7500.txt` (a refusal ends it), compares the worktree's seeds with the accepted copies byte for byte, re-checks both with `kc79_syscheck_1025.py` (selftest 0; accepts; `--mutate=F` and `--mutate=steps` exit 1 on the D 20.75 seed), then starts the leap with the command above (pins: `ell_leap.py` 1eb873e4, `leap_guard.py` f1fe7c7c, worktree 48c36355 with solver code 505d8399; cap 43200 s by the exact root pid with the `ell_leap.py` command-line check; copier into `states/`; files `leap5.log`, `exits_leap5.txt`, `summary_leap5.txt`, `leap5.finished`, `all5.done`); the guard `leap_guard.py --seeds rec_k79_D20.5000.jsonl rec_k79_D20.7500.jsonl` (table `leap5_points.txt`, stop file `leap5_STOP.txt`; it waits for the leap's root pid); and the alert-only samplers of leg 4's kind in `leap5/` (ended by `leap5_marker.sh`). Dry run of the driver 12:27 UTC: pins pass, command as above.

Reporting (the coordinator's): every point with Delta, dDelta/dD, sigma_reg, |J+dF/dn|, h, constraint, |F| (and n_null, the cutoff and max cos_t_reg), beside leg 4's at the same D. Leg 4 (k_c 71, `../kc71_leap/`, table `leg4_points_v2.txt`) runs on as the pathfinder; the k_c 79 leg is the march past D 20.75 (k_c 71's Delta correction against k_c 79: -9.9e-6 at D 20, -2.2e-5 at D 20.5, the coordinator's).

## Result

Not yet run.
