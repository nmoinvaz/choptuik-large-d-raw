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

## The k_c 79 leap's fold watch at D 20.875 and the restart (the coordinator's ruling, hc ~19:20 UTC 23 Nov)

The leap's fold watch fired after its fourth point, D 20.875 (4612 s; |F| 4.663e-10, constraint 4.316e-3, 2689 steps, Delta 1.114916069672, dDelta/dD +0.026524, guard quiet): `sigma_reg 4.103e-11 -> 1.377e-11, |J^+ dF/dn| 0.444 -> 0.422; h -> 0.015625`. It is the same artifact as leg 4's at D 20.75: n_null 72 -> 71 (a mode entered the regular set from below the cutoff 1.359e-11), the tracked modes rose (sv_reg_small [4.103e-11, 1.509e-10, 2.111e-10, 2.120e-10] -> [1.377e-11, 4.267e-11, 1.526e-10, 2.167e-10]: the old first three reappear as +4.0%, +1.1% and +2.7%), the largest cos_t_reg is 0.048, and |J^+ dF/dn| fell. For k_c 79 the mode enters at D 20.875, for k_c 71 at D 20.75. The halving cost: h 0.015625 is the leap's hmin floor (a later failed solve would stop it) and the remaining cap (6.4 h) would have reached about D 20.95.

The ruling (the coordinator's, verbatim): "GO on the restart, same ruling as (b) at D 18.75: not a fold (n_null 72 -> 71 is a mode entering the regular set; tracked modes rose; |J+dF/dn| fell). Restart the k_c 79 leap at h 0.03125 from its D 20.84375 and D 20.875 states under new tag l1kc79Lw1025f, guard with --seeds = those two records, seeds re-checked by kc79_syscheck, old leap + guard killed by exact pid, fresh 12 h cap, D_end 21.5 (so it overlaps leg 6's range). Record the ruling and the restart in the README. The D 20.875 state stands as the leg point (dh610 scans it now)."

The restart (`run_leap7.sh 20.84375 20.875`, headless, BelowNormal; dry run 19:15 UTC passed):

```
ell_leap.py l1kc79Lw1025f 1 79 data/sol_l1kc79Lw1025d_D20.843750.npy 20.84375 data/sol_l1kc79Lw1025d_D20.875000.npy 20.875 21.5 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
```

New tag `l1kc79Lw1025f` (own record file and states; the seeds are tag d's, blobs d4a9414b and 2f6d6b8a, record file of tag d e443a587 with 4 records, equal to the copies in `states/`), files `leap7.log`, `exits_leap7.txt`, `summary_leap7.txt`, `leap7.finished`, `all7.done`; 4 BLAS threads, cap 43200 s (12 h from the restart) by the exact root pid. The old leap (tag d, root pid 43740, worker 30648) and its guard (pid 35888) are killed by exact pid after command-line checks; the old driver (`run_leap5.sh`, pid 44404) then finishes by itself (final copy, `all5.done`), and the new driver waits for `all5.done` and refuses if the old guard had stopped the leap. The seeds are re-checked by `kc79_syscheck_1025.py` (dry run: selftest 0, D 20.84375 and D 20.875 accepted, `--mutate=F` and `--mutate=steps` exit 1). The new guard (`leap_guard.py` f1fe7c7c with `--seeds` = the two seeds' own records, which carry n_null and cos_t_reg; table `leap7_points.txt`, stop file `leap7_STOP.txt`) is the same rule as before. Tag d keeps its four points (D 20.78125, 20.8125, 20.84375, 20.875); the D 20.890625 step in flight when the restart began is discarded.

## The coordinator's ruling on the criterion (hc ~21:00 UTC 23 Nov): the fold reading by tracked modes

The written-before criterion "k_c 79's sigma_reg stays above leg 4's" is violated from D 20.875 (k_c 79 sigma_reg 1.377e-11 at D 20.875 and 1.435e-11 at D 20.90625 against k_c 71's 1.848e-11 and 1.934e-11), but sigma_reg = `sv_reg_small[0]` is the smallest singular value above the null cutoff 1e-12 sigma_max, so in both legs it is the mode that ENTERED above the cutoff (k_c 71 at D 20.75, k_c 79 at D 20.875), not a mode that fell.

The ruling (the coordinator's, verbatim): "the written-before criterion 'k_c 79 sigma_reg stays above leg 4's' FAILS as written from D 20.875; the cause is the entering mode (k_c 71 at D 20.75, k_c 79 at D 20.875), the same artifact as ruling (b), so it is not read as a fold. Replacement, fixed now for every later point of both legs: a fold signature is (i) a regular mode's singular value (tracked by identity across points, entries included once tracked) falling at 3 consecutive points while its tangent |cos| rises above 0.3, or (ii) dDelta/dD changing sign. Report in each row: the tracked weak mode's sigma, the sigma of the mode with the largest tangent |cos| and that cos, and dDelta/dD. The guard's own stop rule is unchanged."

The tool: `../kc71_leap/mode_tracker.py` (reads the records' four-value lists `sv_reg_small`, `cos_t_reg` and `n_null`; identity across two points by the change of n_null: unchanged -> same order; n_null -1 = a mode entered, the first value is new; n_null +1 = the weakest sank below the cutoff; a mode is tracked once it has a predecessor; the tracked weak mode is the smallest sigma among tracked modes). Controls (`../kc71_leap/mode_tracker_tests/`): `--selftest` exits 0 (an entry; three falls with cos 0.35 flagged at the third and not the second; three falls at cos 0.2 not flagged; two falls then a rise not flagged; a slope sign change flagged as (ii); an exit); `--mutate=count` (two falls suffice), `--mutate=cos` (cos ignored) and `--mutate=entry` (entries mapped as no change) each exit 1. The guards (`leap_guard.py`) are unchanged.

Result so far (every point from D 20.6875 to D 21.03125 at k_c 71, tags c and e; every point with a predecessor at k_c 79, tags d and f; no fold signature in any row, (i) or (ii)):

k_c 71:

| D | dDelta/dD | n_null | tracked weak mode: sigma (x prev) | largest-cos mode: sigma, cos | longest fall run, its cos | signature | entry |
|---|---|---|---|---|---|---|---|
| 20.6875 | +0.026304 | 64 | m0 4.747e-11 (x1.086) | m2 2.756e-10 cos 0.0398 | 0 falls, cos 0.014 | none |  |
| 20.75 | +0.026405 | 63 | m0 5.134e-11 (x1.082) | new 1.451e-11 cos 0.0505 | 0 falls, cos 0.042 | none | entered m4 |
| 20.78125 | +0.026472 | 63 | m4 1.546e-11 (x1.065) | m4 1.546e-11 cos 0.0480 | 0 falls, cos 0.043 | none |  |
| 20.8125 | +0.026530 | 63 | m4 1.673e-11 (x1.082) | m4 1.673e-11 cos 0.0457 | 0 falls, cos 0.043 | none |  |
| 20.84375 | +0.026568 | 63 | m4 1.752e-11 (x1.048) | m2 3.159e-10 cos 0.0450 | 0 falls, cos 0.045 | none |  |
| 20.875 | +0.026601 | 63 | m4 1.848e-11 (x1.055) | m2 3.250e-10 cos 0.0461 | 0 falls, cos 0.046 | none |  |
| 20.90625 | +0.026644 | 63 | m4 1.934e-11 (x1.047) | m2 3.338e-10 cos 0.0473 | 0 falls, cos 0.047 | none |  |
| 20.9375 | +0.026693 | 63 | m4 2.029e-11 (x1.049) | m2 3.436e-10 cos 0.0485 | 0 falls, cos 0.048 | none |  |
| 20.96875 | +0.026737 | 63 | m4 2.107e-11 (x1.039) | m2 3.530e-10 cos 0.0495 | 0 falls, cos 0.050 | none |  |
| 21 | +0.026769 | 63 | m4 2.154e-11 (x1.022) | m2 3.626e-10 cos 0.0508 | 0 falls, cos 0.051 | none |  |
| 21.03125 | +0.026800 | 63 | m4 2.222e-11 (x1.032) | m2 3.736e-10 cos 0.0519 | 0 falls, cos 0.052 | none |  |

k_c 79:

| D | dDelta/dD | n_null | tracked weak mode: sigma (x prev) | largest-cos mode: sigma, cos | longest fall run, its cos | signature | entry |
|---|---|---|---|---|---|---|---|
| 20.8125 | +0.026490 | 72 | m0 3.937e-11 (x1.040) | m1 1.485e-10 cos 0.0219 | 0 falls, cos 0.008 | none |  |
| 20.84375 | +0.026507 | 72 | m0 4.103e-11 (x1.042) | m1 1.509e-10 cos 0.0222 | 0 falls, cos 0.008 | none |  |
| 20.875 | +0.026524 | 71 | m0 4.267e-11 (x1.040) | new 1.377e-11 cos 0.0479 | 0 falls, cos 0.002 | none | entered m4 |
| 20.90625 | +0.026584 | 71 | m4 1.435e-11 (x1.042) | m4 1.435e-11 cos 0.0448 | 0 falls, cos 0.005 | none |  |

In both legs the tracked weak mode rises at every step (k_c 79 x1.040 to x1.042 per 0.03125 in D); at k_c 71 its growth per step slows from x1.082 (D 20.8125) to x1.022 (D 21.0) and x1.032 (D 21.03125), still a rise. The largest tangent |cos| is at most 0.052 (k_c 71) and 0.048 (k_c 79).

## Result

Not yet run.
