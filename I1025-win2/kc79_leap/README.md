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

## The branch-point watch (the coordinator's hc ~01:40 UTC 24 Nov; report only, not a stop rule)

The order (verbatim): "Add a second watch, report-only (not a stop rule), for both legs: a BRANCH-POINT watch: any tracked regular mode falling at 5 or more consecutive points with tangent |cos| below 0.1 (a singular value going to zero orthogonal to the tangent, which the fold rule cannot see). Report in each row that mode's sigma, its fall per step and its distance to the cutoff in steps at the current rate. m1 on leg 6 is the candidate (4 falls, cos 0.034, ~300 steps from the cutoff at x0.992)."

`../kc71_leap/mode_tracker.py` (blob 807c2d95): the row's last-but-one column lists every tracked mode with >= 5 consecutive falls and cos < 0.1 (id, sigma, ratio to the previous sigma, number of falls, cos, and n = ln(cutoff / sigma) / ln(ratio) steps to the null cutoff 1e-12 sigma_max at that rate); the longest-fall-run column shows the same numbers for the leading candidate before it reaches 5. The guards and the fold rule are unchanged. Controls (`../kc71_leap/mode_tracker_tests/`): selftest 0 (a mode falling 0.992 per step at cos 0.03 is listed at the 5th fall and not the 4th, at 314 +- 3 steps from the cutoff 1.4e-11 from 1.75e-10; at cos 0.15 it is never listed), `--mutate=bcount` (3 falls suffice) and `--mutate=bcos` (cos ignored) exit 1, and the earlier three mutations still exit 1. Status at D 21.1875 (leg 6): m1, the third regular value, has 4 falls (x0.9975, x0.9986, x0.9907, x0.9922; 1.7872e-10 at D 21.0625 to 1.7500e-10), cos 0.034, about 322 steps from the cutoff 1.401e-11 at the last rate (about 1000 and 1850 steps at the first two rates: the fall has sped up); the 5th fall would list it. No mode of the k_c 79 leap (tags d, f) has more than 0 falls through D 21.0.

## Queued restarts at the caps (the coordinator's standing authorization, hc ~04:40 UTC 24 Nov)

The order (verbatim): "Authorized now, so nothing idles at the caps (~07:13 leg 6, ~07:17 k_c 79): when each ends by its cap, restart it the same way as your 19:17 restart (from its last two states, a new tag, seeds re-checked by the syscheck, guard with --seeds, fresh 12 h cap by exact pid): k_c 79 to D_end 21.5, k_c 71 (leg 6's scout) to D_end 21.75; h 0.03125, the same fold rule and watches. Record each restart in the README."

Two waiting drivers, headless, BelowNormal, started 04:3x UTC (dry runs 04:24 to 04:26 UTC with the then-last two records as stand-in seeds: pins pass, seeds accepted by the syscheck, controls exit 1, command printed):

| | k_c 79 (`run_leap8.sh`, here) | k_c 71, leg 6's scout (`run_leap9.sh`, `../kc71_leap/`) |
|---|---|---|
| waits for | `all7.done` (the restarted leap's end by its cap, 07:17:20 UTC) | `all6.done` (leg 6's end by its cap, 07:13:13 UTC) |
| restarts only if | `summary_leap7.txt` says "capped at 43200 s" and no `leap7_STOP.txt` | `summary_kcl6.txt` says "capped at 43200 s" and no `leg6_STOP.txt` |
| seeds | the last two records of tag l1kc79Lw1025f | the last two records of tag l1kc71Lw1025e |
| new tag | l1kc79Lw1025g | l1kc71Lw1025h |
| command | `ell_leap.py l1kc79Lw1025g 1 79 <seed A> A <seed B> B 21.5 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold` | `ell_leap.py l1kc71Lw1025h 1 71 <seed A> A <seed B> B 21.75 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold` |
| files | `leap8.log`, `exits_leap8.txt`, `summary_leap8.txt`, `leap8_points.txt`, `leap8_STOP.txt`, `all8.done` | `leap9.log`, `exits_kcl9.txt`, `summary_kcl9.txt`, `leg9_points.txt`, `leg9_STOP.txt`, `all9.done` |

Each driver re-checks the two seeds against the record file and the copies in `states/` (byte for byte), with the syscheck (selftest 0, accepts, `--mutate=F` and `--mutate=steps` exit 1), writes the seeds' own records (which carry n_null and cos_t_reg) for the guard (`leap_guard.py` f1fe7c7c, `--seeds`; the same rule), starts the guard and the alert-only samplers headless, then the leap: 4 threads, cap 43200 s (fresh 12 h) by the exact root pid with the `ell_leap.py` command-line check. A leg that ends any other way (its guard's stop, the leap's own stop, reaching its D_end) is not restarted; the driver logs why and exits. Each restart is recorded below when it happens.

## Restart log: the two cap restarts of 24 Nov (the coordinator's standing authorization above)

**k_c 71, leg 6 -> leg 9** (`../kc71_leap/run_leap9.sh`). Leg 6 ended by its cap: the leap root pid 43128 was killed at 07:13:23 UTC (43219 s, exit 1, "capped at 43200 s"); 12 points D 21.03125 to D 21.375 (the last in raw 9af2e8282). The waiting driver found no `leg6_STOP.txt` and the cap in `summary_kcl6.txt`, and at 07:17:40 UTC took the last two records of tag l1kc71Lw1025e as seeds: D 21.34375 (state blob 2e2b00bc) and D 21.375 (blob 52f92e3b), record file blob 6948a267 with 12 records, equal to the copies in `states/`; `kc71_syscheck.py` accepted both at 07:17:50 UTC (selftest 0; `--mutate=F` and `--mutate=steps` exit 1; D 21.375 |F| 4.3390e-10 with 2378 steps, D 21.34375 4.3780e-10 with 2381). The guard (`leap_guard.py` f1fe7c7c, `--seeds` = the two seeds' own records; table `leg9_points.txt`, stop file `leg9_STOP.txt`; pid 44436, worker 41480) and the samplers (`leg9/`) started at 07:17:58 UTC, and the leap at 07:18:11 UTC: `ell_leap.py l1kc71Lw1025h 1 71 data/sol_l1kc71Lw1025e_D21.343750.npy 21.34375 data/sol_l1kc71Lw1025e_D21.375000.npy 21.375 21.75 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`, root pid 34332 (worker 44404), 4 threads, BelowNormal, fresh 12 h cap = 19:18:11 UTC by the exact root pid; files `leap9.log`, `exits_kcl9.txt`, `summary_kcl9.txt`, `all9.done`.

**k_c 79, restarted leap (tag f) -> tag g** (`run_leap8.sh`). The restarted leap ended by its cap: the leap root pid 33464 was killed at 07:17:30 UTC (43211 s, exit 1, "capped at 43200 s"); 9 points D 20.90625 to D 21.15625 (the last in raw 11ebcd944). The waiting driver found no `leap7_STOP.txt` and the cap in `summary_leap7.txt`, and at 07:19:41 UTC took the last two records of tag l1kc79Lw1025f as seeds: D 21.125 (state blob 797c73e7) and D 21.15625 (blob ff2a8451), record file blob 2c12fa10 with 9 records, equal to the copies in `states/`; `kc79_syscheck_1025.py` accepted both at 07:19:48 UTC (selftest 0; `--mutate=F` and `--mutate=steps` exit 1; D 21.15625 |F| 4.5898e-10 with 2664 steps, D 21.125 4.6060e-10 with 2667). The guard (pid 22956, worker 34208; table `leap8_points.txt`, stop file `leap8_STOP.txt`) and the samplers (`leap8/`) started at 07:19:49 UTC, and the leap at 07:19:49 UTC: `ell_leap.py l1kc79Lw1025g 1 79 data/sol_l1kc79Lw1025f_D21.125000.npy 21.125 data/sol_l1kc79Lw1025f_D21.156250.npy 21.15625 21.5 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`, root pid 26568 (worker 41244), 4 threads, BelowNormal, fresh 12 h cap = 19:19:49 UTC; files `leap8.log`, `exits_leap8.txt`, `summary_leap8.txt`, `all8.done`.

## The k_c 79 far scout (the coordinator's hc ~11:10 UTC 24 Nov), and leg 9's psi-constraint stop

**Leg 9 (k_c 71, tag h)** reached the leap's psi-constraint bar: the solve at D 21.5 converged (|F| 4.177e-10, 2370 steps, Delta 1.131801109) with psi-constraint 1.00348e-2 above `--cmax 1e-2`, so it was rejected and not recorded (the constraint rose 9.469e-3, 9.655e-3, 9.843e-3, 1.0035e-2 at D 21.406 to 21.5, 5.1e-3 per unit D, crossing 1e-2 near D 21.4993); h halved to 0.015625, the hmin floor. The coordinator's ruling (verbatim): "(a): let leg 9 end where it stops (D 21.484375 by its retry), no raised bar, no restart." A stop of the leap's own is not a cap end, so no restart is queued for leg 9.

The order for the freed threads (verbatim): "With its freed threads (4), start a k_c 79 FAR SCOUT ahead of the tag g leap: tag l1kc79Lw1025i, seeds the tag g records D 21.1875 and D 21.21875 (re-checked by kc79_syscheck, controls exit 1), ell_leap.py l1kc79Lw1025i 1 79 <D 21.1875 state> 21.1875 <D 21.21875 state> 21.21875 22.5 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold (h 0.0625; the leap halves to 0.03125 if a step fails), the guard with --seeds, the same fold rule, tracked-mode and branch-watch reporting, 12 h cap by exact pid; a cap restart to D_end 22.5 is authorized the same way as before. Report each point with your columns, and say the seconds per point at h 0.0625 against 0.03125. The tag g leap continues to D 21.5 unchanged."

`run_leap10.sh` (headless, BelowNormal; dry run 11:08 UTC passed) waits for `all9.done`, takes the tag g records at D 21.1875 and D 21.21875 (states blobs 9d3351f6 and 5d263c46, byte-equal to the raw copies; the two seed records equal between the worktree's record file and the raw copy, since the tag g leap keeps appending; |F| 4.5790e-10 with 2660 steps and 4.5648e-10 with 2658), re-checks them with `kc79_syscheck_1025.py` (selftest 0, accepts, `--mutate=F` and `--mutate=steps` exit 1), starts the guard (`leap_guard.py` f1fe7c7c, `--seeds` = those two records; table `leap10_points.txt`, stop file `leap10_STOP.txt`) and the samplers (`leap10/`), then:

```
ell_leap.py l1kc79Lw1025i 1 79 data/sol_l1kc79Lw1025g_D21.187500.npy 21.1875 data/sol_l1kc79Lw1025g_D21.218750.npy 21.21875 22.5 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
```

4 threads, cap 43200 s by the exact root pid; files `leap10.log`, `exits_leap10.txt`, `summary_leap10.txt`, `all10.done`. The first predictor extrapolates over two seed differences (h 0.0625 against a seed gap of 0.03125). Seconds per point at h 0.0625 against 0.03125 are reported with each point (the k_c 79 tag g leap at h 0.03125: 4475 to 4896 s a point).

## Leg 9 ended by order at D 21.484375 (the coordinator's hc ~12:00 UTC 24 Nov)

The order (verbatim): "leg 9's next step is known to fail its constraint bar, so stop leg 9 now by exact pid (record it: ended by order at D 21.484375, the D 21.5 step would exceed cmax), and start the far scout at once. Your timing finding (cost per point flat in h) is noted: report the far scout's seconds per point at h 0.0625."

Leg 9 (k_c 71, tag l1kc71Lw1025h) was stopped at 12:03:07 UTC: the leap root pid 34332 was killed by exact pid after the check that its command line held `ell_leap.py l1kc71Lw1025h` (the run had lasted 4 h 45 min). Four accepted points D 21.40625 to D 21.484375 (the last at h 0.015625, 3264 s, |F| 4.196e-10, psi-constraint 9.939e-3); the retry's next step, D 21.5 at h 0.015625, would have had psi-constraint about 1.0035e-2 above `--cmax 1e-2` (the D 21.5 solve at h 0.03125 had converged, |F| 4.177e-10, Delta 1.131801109, and was rejected for 1.00348e-2), and h cannot halve below `hmin`, so the leap would have stopped there. No restart. The in-flight step (about 45 minutes in) is discarded. The scout driver `run_leap10.sh`, waiting for `all9.done`, starts after the driver's final copy.

Timing finding (reported 11:50 UTC): seconds per point at h 0.03125 against h 0.015625 at k_c 71: 3588, 3478, 2987 s against 3264 s, so the cost per point does not fall with the step (F_start 3.8e-6 against 1.0e-5, the same ~2370 steps).

## The far scout started (12:04:28 UTC 24 Nov)

`run_leap10.sh` found leg 9 ended (`all9.done` after the by-order stop at 12:03:07 UTC), compared the tag g seeds (states blobs 9d3351f6 for D 21.1875 and 5d263c46 for D 21.21875, equal to the raw copies; the two seed records equal between the worktree's record file and the raw copy: |F| 4.5790e-10 with 2660 steps and 4.5648e-10 with 2658), and `kc79_syscheck_1025.py` accepted both at 12:04:16 UTC (selftest 0; `--mutate=F` and `--mutate=steps` exit 1). The guard (`leap_guard.py` f1fe7c7c, `--seeds`; pid 7596, worker 30308; table `leap10_points.txt`, stop file `leap10_STOP.txt`) and the samplers (`leap10/`) started at 12:04:22 UTC, and the leap at 12:04:28 UTC: `ell_leap.py l1kc79Lw1025i 1 79 data/sol_l1kc79Lw1025g_D21.187500.npy 21.1875 data/sol_l1kc79Lw1025g_D21.218750.npy 21.21875 22.5 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`, root pid 40680 (worker 20128), 4 threads, BelowNormal, cap 43200 s = 00:04:28 UTC on 25 Nov by the exact root pid. A cap restart to D_end 22.5 is authorized (driver to follow in this README).

## Queued cap restart of the far scout (the coordinator's authorization, hc ~11:10 UTC 24 Nov; queued 14:36 UTC)

`run_leap11.sh` (headless, BelowNormal; dry run 14:35 UTC with the scout's two points as stand-in seeds: pins pass, seeds D 21.28125 (blob ee63bdf2) and D 21.34375 (blob b7efa3d3) accepted, controls exit 1, command printed) waits for `all10.done` (the scout's end by its cap, 00:04:28 UTC 25 Nov), restarts only if `summary_leap10.txt` says "capped at 43200 s" and there is no `leap10_STOP.txt`, from the last two records of tag l1kc79Lw1025i as tag l1kc79Lw1025j to D_end 22.5 with h = the last record's h (0.0625 now; logged), the seeds re-checked by `kc79_syscheck_1025.py` (selftest, accepts, `--mutate=F` and `--mutate=steps` exit 1), the guard (`leap_guard.py` f1fe7c7c, `--seeds`; table `leap11_points.txt`, stop file `leap11_STOP.txt`) and samplers (`leap11/`) started by `launch_leap11_extras.ps1`, 4 threads, a fresh 12 h cap by the exact root pid; files `leap11.log`, `exits_leap11.txt`, `summary_leap11.txt`, `all11.done`. Any other end (a guard stop, the leap's own stop, reaching D 22.5) is not restarted. The restart is recorded here when it happens.

## Result

Not yet run.
