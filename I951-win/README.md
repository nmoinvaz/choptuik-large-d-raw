# I951-win: start c, a third K = 7 root and K = 0 control at D 40.02 from #145's 32 x 101 root, and 48 rough rt_sigma starts on each

Machine win (Surface Laptop 4, i7-1185G7, 4 cores and 8 threads, 32 GB), runner winb, issue https://github.com/nmoinvaz/choptuik-large-d/issues/951 (recommended by #943, raw `I943-win/` c9573179; the coordinator's `hc` message of 2026-11-18). Worktree `C:\Users\nathan\Source\choptuik-i951` at origin/main a80697d7 (detached; `git diff --stat 09ffaa1e origin/main -- solver/rt` and the same against #681's 5135cdeb are empty, so `solver/rt` is the code of #681, #701, #721 and #943), venv-t151 (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0) through `rt_launch.py` (copied from `I943-win/`, it supplies `multidouble._dd_dot` and `math.fma`, no repository file changes). Runs start in the worktree (`rt_run.py`) or in `solver\rt` (`rt_sigma.py`).

Drivers, from #701's and #943's with only the start, the tags and the rules changed: `checks_951.py` (the two planted checks), `run_951_solves.py` (the two solves at once, 1 BLAS thread each, from `I701-win/run_701_solves.py`), `start_951_solves.cmd` (launcher), `run_951.py` (the two `rt_sigma.py STATE --starts 48 --rough` runs at once, from `I943-win/run_943.py` without its #681 control), `start_951.cmd`, `table_951.py` (the tables and the verdict, with a selftest), `table_701.py` and `table_423.py` (the bootstrap and log parser, copied from `I943-win/`), `rt_launch.py`.

## Inputs

- Start c: `I145-mac/cont/cont_32x101_D40.0201_32x101.npz` (D 40.020065, 32 x 101, sha256 18221618c647a967...), read in place from the push worktree `choptuik-large-d-raw-754` (origin/main, last change in the raw history 6265e769).
- **The issue's file name is not the one used.** The issue names `cont_32x101_D50.0075_32x101.npz`, #145's 32 x 101 root at D 50.007491 (the file of RT_FORMULATION 13.7). #701's start was the 32 x 141 root at D 40.020065 (`I145-mac/fol/fol_32x141_D40.0201_32x141.npz`) and the issue says "instead of its 32 x 141", so start c is the 32 x 101 root at the same D, `cont_32x101_D40.0201_32x101.npz`. The D 50.0075 file would need a 10-unit continuation in D, which is not #701's procedure. Reported to the coordinator before the solves.
- For the distances and R_a, R_b: a's states `I671-win/solves/k7_D40_D40.0201_32x121.npz` (sha256 df81e4d2a6f098a6...) and `k0_D40_mutnorows_D40.0201_32x121.npz` (a6b9a729d78f39ce...), b's `I701-win/solves/k7b_D40_D40.0201_32x121.npz` (c5c3e03ceafb3b5e...) and `k0b_D40_mutnorows_D40.0201_32x121.npz` (b048df8c7504d477...); the bounds of a are `I943-win/logs/K7_D40_rough.log` and `K0_D40_rough.log`, of b `I721-win/logs/K7b_D40_rough.log` and win2's `I721-win2/logs/K0b_D40_rough.log`, all read in place from the push worktree.
- **The issue's "seed 943" is not a setting.** `rt_sigma.py --rough` draws its right-hand sides from `np.random.default_rng(163)` written in the code (successive draws, `rt_sigma.py` line 119), with no seed option, and #943 ran exactly that. I run the same code, so the 48 right-hand sides of start c are those of a and b ("as #943"). No code is changed.

## Plan, fixed before any solve and any sigma run (2026-11-18 01:49 UTC)

1. `rt_sigma.py --planted` exits 0 and `--planted --mutate=shift` exits 1, first (`checks_951.py`, `logs/planted*.log`). **Done 01:46:41 UTC:** exit 0 (best bound 1.4103e-21, as #701, #721, #943) and exit 1 (1.4244e-19, FAIL).
2. Two solves at once, 1 BLAS thread each, BelowNormal (as #701): `rt_run.py --start <start c> --grids 32x121 --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol 1e-40 --horizon 7 --resample_mp --out solves --tag k7c_D40`, and the same with `--mutate=norows --tag k0c_D40`. A solve counts if its jsonl record says `ok` with the last Newton max|F| at most 1e-36 (#701's rule). If a solve ends above that, I post its value and ask before the sigma runs. If `--resample_mp` refuses 101 to 121, I stop and report.
3. **Distinct from a and b.** From the stored double-double states (`zh` + `zl`), the max-norm and the 2-norm of z_c - z_a and z_c - z_b for the K 7 roots (and the same for the K 0 roots), and Delta_c - Delta_a, Delta_c - Delta_b from the records' `Delta_str` in arb at 400 bits, with each root's DD = Delta(K 7) - Delta(K 0). The tolerance is the stored state's resolution: the states are double-double with |z| at most 0.13, so a max-norm difference of 1e-30 or less is rounding. A root **re-finds** a or b if its max-norm distance to that root is at most 1e-30, and then I stop before the sigma runs and say so (K 7 or K 0 alone re-finding also stops it, and is reported). For scale, a against b is 2.9e-20 (max-norm) and 4.1e-19 (2-norm) for K 7, and 2.1e-21 and 1.1e-19 for K 0; within a pair K 7 against K 0 is 5.9e-19 and 7.1e-18 (a), 5.6e-19 and 6.8e-18 (b). The residual criterion alone cannot separate roots that close, since the solve's max|F| of about 1e-38 is met by all of them, which is why the distance is the criterion.
4. Two sigma runs at once, `rt_sigma.py STATE --starts 48 --rough` on each solve's state, `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=2` each (4 of the laptop's 8 threads), BelowNormal, detached, logs `logs/K7c_D40_rough.log` and `K0c_D40_rough.log`, exit files `logs/*_rough.exit`, driver log `logs/run_951.log`. #943 is the cost reference: K 0 6.2 min a start (5.2 h for 48) and K 7 24.5 to 31.5 min a start (17.0 h for 48) with the negative-mass jobs running; they are not running now (laptop at 17% CPU, 19.8 GB free at 01:45 UTC).
5. **Stop rules.** The issue's stop is 30 h: counted from the start of the solves, a run unfinished at that time is killed and reported with what it printed (code 5, partial rows are not the criterion). K 0 additionally 10 h from its start. A file `STOP_951` in this folder stops what runs (code 4). A nonzero exit of a run is reported, and the other run continues. Memory is watched (each run about 1.8 GB, peak 2.3 GB); I stop my runs if free memory falls under 6 GB.
6. **There is no first-12 control in this task** (a and b had #681's log for it, a new pair has none). The controls are the planted pair above (the same code path, and the mutation fires), the identical `solver/rt` (empty diff), the same hard-coded right-hand sides as a and b, a selftest of `run_951.py` on dummy children (a good one exits 0, a capped one gets 5, a stopped one 4) and of `table_951.py` (planted samples for each verdict and a mutation that must flip it), and the printed header of each run (its state's max|F| must equal the solve's last Newton value).

## Prediction and rule, written before the solves and the sigma runs

**Prediction** (winb, 2026-11-18 01:49 UTC):
- **P1, the pair is new.** Both solves converge (ok, max|F| at most 1e-36) and neither root re-finds a or b. I expect the max-norm distances to a's and b's roots between 1e-21 and 1e-18, the size of the a-b distance (2.9e-20 for K 7).
- **P2, the pair coincides.** |DD| = |Delta(K 7) - Delta(K 0)| is below 1e-15 (a 6.8e-18, b 6.4e-18).
- **P3, spread.** R_c lies outside both intervals. Basis: the two pairs differ by a factor 6 in R, and even the K 0 median differs by a factor 10 between a and b (2.7e-34 against 2.6e-33) at a root distance of 2e-21 (max-norm), so the bound moves with the root along the weak directions and I expect it to move for a third root instead of landing on one of two values. About 65% sure.

**Rule** (the issue's). R_c = median(K 7) / median(K 0) over the 48 starts of each run, the median of a run being the geometric mean of its 24th and 25th smallest bounds, as for R_a and R_b; R_a and R_b and their 95% bootstrap intervals are recomputed from their logs (10000 resamples of each run's 48 bounds with replacement, `random.Random(701)`, the 2.5th and 97.5th percentiles, `table_701.verdict` imported) and must equal #943's and #721's (R_a 0.98, 0.60 to 1.43; R_b 6.06, 4.56 to 9.26), else flagged.
- **Classes:** the point R_c lies inside R_a's interval or inside R_b's.
- **Spread:** the point R_c lies outside both.
- What each says. Spread excludes "two values, one per class" for these three roots. Classes is weak: it does not exclude a spread of R over roots (a log-uniform spread over 1/3 to 20 would land inside one of the two intervals 38% of the time), it says only that a third root fell where a first or a second did.
- Context, not the rule: R_c's own 95% bootstrap interval (same resampling), the joint bootstrap of R_c / R_a and R_c / R_b against 1 (as #943's R_a / R_b, one resample drawing the four runs in order), the best-of-48 ratio. If the point is inside one interval and one of these disagrees, I say so and do not resolve it.
- It informs RT_FORMULATION 14: classes lets it state the K = 7 rows' effect per root class, spread says it can be stated per root only.

The bounds are upper bounds on the smallest gain from one rough start each, and the intervals are bootstrap spreads over the random right-hand sides, not enclosures. The 250-product cap is as in #943 (46 of its 48 K 7 starts ended at it), and it is not tested again here (#720 checked 3 starts of a).

## Restated plan after the stop (2026-11-18 02:43 UTC, before the new solves and any sigma run)

The coordinator (issue comment 6967406677 and `hc`) went on with start c = #145's own 32 x 121 root, `I145-mac/fol/fol_32x121_D40.0201_32x121.npz` (D 40.020065, 32 x 121, sha256 a6767a7dec01e91c2c6f..., last change in the raw history 61216f6a; no resampling, the solves' grid). The first c, from the 32 x 101 file, was start a again and its files are in `a_rerun/` (not part of the result). The coordinator's stored-root check: a and b are the same root, apart by 2.9e-20 (K 7) and 2.1e-21 (K 0); #145's 32 x 121 root is 2.2e-21 from a's K 0 root, so c is a third floor-level sample of that root, and **the question is now how far the rough bounds spread over such samples**.
- The same two solves (`run_951_solves.py`, only the start path changed), the same distance rule, then the same two sigma runs (`run_951.py`, 48 rough starts, 2 BLAS threads each).
- **Reported:** R_c with its 95% bootstrap interval and the K 7 and K 0 medians of c beside those of a and b, and the max-norm (and 2-norm) distance of the two new roots from a's and b's (the table of `table_951.py`). The classes/spread rule above (R_c inside R_a's or R_b's interval) is still computed and printed, as the first reading of the issue.
- **Caps:** the same, the 30 h counted from 01:49:22 UTC (so the deadline stays 2026-11-19 07:49:22 UTC), K 0 10 h of its own. Nothing else changes. P1 is restated: the roots are new if the max-norm distance to a's and b's roots is above 1e-30, and I expect them near 1e-21 as the coordinator found for the K 0 root. P3 (R_c outside both intervals) stands as it was.

## Run record

- 01:49:22 UTC: `run_951_solves.py` started the two solves (`start_951_solves.cmd`, BelowNormal, 1 BLAS thread each). `--resample_mp` accepted 101 to 121.
- 02:13:04 UTC: **both solves crashed at their last step** (`ModuleNotFoundError: No module named 'resource'`, `rt_run.py` line 78): I did not copy #701's `resource.py` (a Windows stand-in for the Unix module, which `rt_run.py`'s `rss_peak_gb()` imports) into this folder. No record or state was written; the failed attempt's files are in `logs/attempt1_no_resource/` (its `solves/k7c_D40.log` was overwritten by the stdout log of the same name, which holds the same lines). 24 min lost; the 30 h clock stays at 01:49:22.
- 02:13:54 UTC: `resource.py` copied from `I701-win/`, solves started again. 02:30:26 UTC `k0c_D40` exit 0 (992 s), 02:38:22 UTC `k7c_D40` exit 0 (1467 s).
- 02:39 UTC: read by `table_951.py` (`table_951.txt`). **Both roots are bit-identical to start a's** (below), so by plan item 3 I stop before the sigma runs. Coordinator's rule on the K 7 floor (hc, during the rerun, "at or below 2e-36 at its floor: accept, record on the issue, go on"): K 7 ended at 1.19e-36 after three Newton steps between 4.9e-37 and 1.9e-36 (a floor), so it would have been accepted; it is moot.
- Nothing else runs; no sigma run was started.

## Result: start c is start a

| solve | ok | last Newton max abs F | Delta_RT | Delta_RT - Delta_hp | secs |
|---|---|---|---|---|---|
| `k7c_D40` (K 7) | True | 1.19e-36 | 1.88845166449061538966142548338 | +1.5517e-15 | 1464 |
| `k0c_D40` (K 0, `--mutate=norows`) | True | 2.20e-40 | 1.88845166449061538288377677162 | +1.5449e-15 | 985 |

| roots | max-norm of the difference | 2-norm | re-found (at most 1e-30) | Delta difference |
|---|---|---|---|---|
| K 7, c against a | 0 | 0 | **YES** | 0 |
| K 0, c against a | 0 | 0 | **YES** | 0 |
| K 7, c against b | 2.857e-20 | 4.085e-19 | no | +3.668e-19 |
| K 0, c against b | 2.097e-21 | 1.147e-19 | no | +2.743e-20 |

DD(c) = Delta(K 7) - Delta(K 0) = +6.7776e-18 (a's 6.8e-18, b's 6.4383e-18), so P2 holds. P1 (the pair is new) is wrong, and avoidably so.

**Why.** Start a's solves (#671, `I671-win/`, the commands in its README and `solves/k7_D40.log`) started from this same file, `I145-mac/cont/cont_32x101_D40.0201_32x101.npz`, resampled 101 to 121 by `--resample_mp`, with the same options and the same `solver/rt`. So the pair is the same computation: the arrays `z`, `zh`, `zl` of both `.npz` files equal a's byte for byte (K 7 sha256 df81e4d2a6f098a6e4cb, K 0 a6b9a729d78f39ce60bf, the same as a's), the records' Newton histories equal #671's to every printed digit (K 7: 2.258e-29, 6.185e-33, 2.148e-31, 1.936e-36, 4.852e-37, 1.188e-36), and Delta_RT equals a's in all 30 digits. The issue's "from #145's 32 x 101 root instead of its 32 x 141" describes start a against start b, not a third start. I read #701's and #943's READMEs and not #671's, and predicted a distance of 1e-21 to 1e-18 without checking where a came from.

**Candidates for start c** (the #145 states at D 40.0201 that no pair of this series used): `I145-mac/fol/fol_32x121_D40.0201_32x121.npz` (#145's own 32 x 121 root, the grid the solves run on, so no resampling). The same two `rt_run.py` commands with `--start` set to it (and `--resample_mp` dropped, or left, it only acts when the grids differ) take about 25 min; whether the result is distinct from a and b is read by this README's rule 3. Not run, since it changes the issue's start.

## Discrepancies

- The issue's start file (`cont_32x101_D50.0075`) and "seed 943" were read as D 40.0201 and the fixed `default_rng(163)`, which the coordinator confirmed (hc, during the first solve attempt).
- The first solve attempt failed on my missing `resource.py` (above); the rerun's records are the ones used.
- P1 of the prediction failed (above). P3 was not tested.

## Run record of the second c (#145's 32 x 121 root)

- 02:43:30 UTC: `run_951_solves.py` started the two solves from `fol_32x121_D40.0201_32x121.npz` (BelowNormal, 1 BLAS thread each). 02:48:40 `k0c_D40` exit 0 (311 s), 02:49:40 `k7c_D40` exit 0 (371 s). Each converged in one Newton step from the 32 x 121 root: K 7 max|F| 5.76e-29 -> 7.55e-44, K 0 4.45e-31 -> 2.82e-49 (a's and b's K 7 stalled at about 1e-36), both count by the 1e-36 rule. Delta(K 7) 1.88845166449061538291061373176, Delta(K 0) 1.88845166449061538290961246572, DD = +1.0013e-21 (a 6.78e-18, b 6.44e-18).
- Distances from a's and b's roots (`table_951.py`): K 7, c from a 5.864e-19 (max-norm), from b 5.579e-19; K 0, c from a 2.189e-21, from b 3.497e-21; so c is new in all four, and its K 7 root sits at the K 0 roots' place (its distance from c's K 0 root is 7.5e-23) while a's and b's K 7 roots sit 5.6e-19 to 5.9e-19 off theirs.
- 02:50:03 UTC: `start_951.cmd` started `run_951.py --t0 "2026-11-18 01:49:22"` (BelowNormal, detached): K 7 pid 22184 and K 0 pid 10584, 2 BLAS threads each, both BelowNormal, deadline 2026-11-19 07:49:22 UTC, K 0 own cap 10 h. Headers: K 7 max|F| 6.20e-29 (a's 6.21e-29), K 0 6.91e-31 (a's 4.39e-31); these `rt_sigma.py` header values are not the solves' last Newton values for a either, so plan item 6's last check (header equals the solve's last Newton value) does not apply and is dropped. Free memory 19.8 GB, laptop CPU 23% before the start, the negative-mass jobs are not running.

## 3 h progress (2026-11-18 05:34 UTC, sigma runs started 02:50:03 UTC)

- K 0 (K0c_D40) finished: exit 0, 48 of 48 starts, 9768 s. Median of the 48 bounds 1.514e-35 (geometric mean of the 24th and 25th), best 4.594e-36, spread of the starts a factor 114.8. a's K 0 median is 2.713e-34 (#943), b's 2.610e-33 (#721 with win2's K 0). c is 18 times below a and 172 times below b. The first 9 starts give 1.484e-35.
- K 7 (K7c_D40) is at start 9 of 48, about 17 min a start, expected end about 16:30 UTC (deadline 2026-11-19 07:49:22 UTC, no own cap).
- Free memory 17.7 GB of 31.8, CPU about 29%. No cap hit, no stop, no re-find.
- `table_951.py` is run when K 7 ends. Nothing is concluded from K 0 alone.

## 6 h progress (2026-11-18 08:46 UTC, sigma runs started 02:50:03 UTC)

- K 7 (K7c_D40) is at start 22 of 48 (start 21 printed 08:38 UTC), about 15 min a start since 05:22, expected end about 15:10 UTC. K 0 is done (above). No cap hit, no stop, no re-find. Free memory 17.5 GB of 31.8, CPU about 29%.
- Partial, not a result: median of K 7's first 22 bounds 8.547e-34, against K 0's first 22 median 1.480e-35, ratio 57.75. The same first-22 ratio for a is 1.06 (final 0.98) and for b 6.68 (final 6.06), so the first 22 starts tracked the 48 for both earlier pairs. The verdict, the interval and the first rule wait for the 48.

## 9 h progress (2026-11-18 11:46 UTC, sigma runs started 02:50:03 UTC)

- K 7 (K7c_D40) is at start 34 of 48 (start 33 printed 11:38 UTC), 15 min a start, expected end about 15:15 UTC. K 0 is done. No cap hit, no stop, no re-find. Free memory 17.6 GB of 31.8, CPU about 30%.
- Partial, not a result: first-34 medians. c K 7 8.014e-34, K 0 1.514e-35, ratio 52.92. The same first-34 ratio is 0.96 for a (final 0.98) and 6.39 for b (final 6.06). The verdict waits for the 48.
