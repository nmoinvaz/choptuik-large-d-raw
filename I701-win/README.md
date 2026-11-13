# I701-win: RT start b at D 40.02, K = 7 and K = 0 roots from #145's 32 x 141 root, and rough rt_sigma runs on both

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/701 (the coordinator's message `1794596199117-0` on the `choptuik-large-d` channel, and its prediction comment 6862130458; recommended by #681, raw `I681-win/` d092fdd4). Worktree `choptuik-i423` (main 5135cdeb, `solver/rt`), venv-t151 (Python 3.10.0, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0) through `rt_launch.py` and `resource.py` (copied from `I681-win/`; no repository file changes). The start state is read in place from the raw repository's stage checkout (origin/main 0e9206ac): `I145-mac/fol/fol_32x141_D40.0201_32x141.npz` (D 40.020065, 32 x 141, last changed at 61216f6a). Raw output to `I701-win/`.

Drivers, from #671's and #681's with only the start, the tags and the job count changed: `run_701_solves.py` (two solves at once, one BLAS thread each), `run_701_sigma.py` (two rough runs at once, two BLAS threads each; at most 4 busy threads at BelowNormal), `table_701.py` (the table, the bootstrap and the verdict, with a selftest), `table_423.py` (the log parser, copied).

## Plan, written before the runs: the coordinator's prediction and commands (comment 6862130458), verbatim

Coordinator: the prediction and the commands, written before any run (2026-11-13).

**Prediction.** The hypothesis from #681 is that R tracks how far the K = 7 root is from its K = 0 control, not D. At D 40.02, start a gave ΔΔ = Δ(K 7) − Δ(K 0) = 6.8e-18 and R = 0.98. All four of #671's D 40.02 solves agree with hp to 1.55e-15, so at this D the grid's roots sit on one plateau.

- **P1.** Start b's K 7 and K 0 roots coincide too, with |ΔΔ| < 1e-15.
- **P2.** Given P1, R_b = median(K 7) / median(K 0) lies in [1/3, 3], and so does R_b / R_a with R_a = 0.98.
- If P1 fails and |ΔΔ| ≥ 1e-12, the hypothesis predicts R_b ≥ 3, as at D 50.007 (ΔΔ 1.04e-12, R 5.88). The rival, that D sets R, predicts R_b in [1/3, 3] anyway, so this outcome separates the two.

**Verdict rule** (#681's bootstrap, 10000 resamples, seed 701). P2 holds if R_b's point value and its 95% interval lie inside [1/3, 3]. It fails if the point is outside and the interval lies entirely outside. Otherwise it is undecided.

**Start b** is #145's 32 × 141 root at D 40.020065, `I145-mac/fol/fol_32x141_D40.0201_32x141.npz`, resampled exactly in ξ to 32 × 121 (`--resample_mp`).

**Commands** (win, raw folder `I701-win/`), from #671's and #681's drivers with only the start and tags changed:

1. `rt_sigma.py --planted` exits 0, and `--planted --mutate=shift` exits 1.
2. Two solves at once, one BLAS thread each: `rt_run.py --start <start b> --grids 32x121 --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol 1e-40 --horizon 7 --resample_mp --out solves --tag k7b_D40`, and the same with `--mutate=norows --tag k0b_D40`. A solve counts if its jsonl record says `ok` with max|F| ≤ 1e-36. If `--resample_mp` refuses 141 → 121, stop and report.
3. Two sigma runs at once, two BLAS threads each: `rt_sigma.py STATE --starts 12 --rough` on each solve's state.
4. Report ΔΔ, each state's Δ_RT − Δ_hp, the 12 bounds of each run with their median, R_b with its bootstrap interval, R_b / R_a, and the verdict by the rule above.

**Threads**: at most 4. **Estimate**: about 4.5 h (the solves about 30 min, the K 7 sigma run about 3.8 h as in #681). **Stop**: a run unfinished after 6 h is reported with what it printed.

## Choices fixed here, 2026-11-13 18:58 UTC, before any run (win)

1. **P2 has two readings.** The prediction says R_b lies in [1/3, 3] "and so does R_b / R_a", while the verdict rule names only R_b. The verdict is formed by the rule as written, on R_b, the point and its 95% interval. R_b / R_a (R_a = 0.98, #681's median ratio at start a, `I681-win/table_681.txt`; a constant, so its interval is the interval of R_b divided by 0.98) is reported beside it with the same inside/outside test, and if the two readings disagree it is said so and not resolved here.
2. **The statistics are #681's** (`I681-win/table_681.py`): the bound of a run is the median of its 12 rough bounds (the geometric mean of the 6th and 7th smallest), R_b = median(K 7) / median(K 0), the bootstrap resamples each run's 12 bounds with replacement 10000 times with `random.Random(701)` and takes the 2.5th and 97.5th percentiles of R_b. The best-of-12 ratio and the quartiles are context. The selftest of `table_701.py` has planted samples with a known ratio that must come out HOLDS, FAILS and UNDECIDED.
3. **P1** is read from the two solve records: Delta_RT is the record's `Delta_str` (30 digits), subtracted in arb at 400 bits, DD = Delta(K 7) - Delta(K 0); P1 holds if |DD| < 1e-15. The records' `diff` (Delta_RT - Delta_hp) is quoted for each state.
4. **A solve counts** if its record says `ok` with the last Newton max|F| at most 1e-36 (the coordinator's rule). If a solve ends above that (#671's K = 7 solve at D 40.02 ended at 1.19e-36), I post the value and ask the coordinator before the sigma runs start, and the pair is called "not counted by the issue's rule" until the coordinator says otherwise. If `--resample_mp` refuses 141 to 121, I stop and report.
5. **Which outcome separates the two readings**, as the prediction states: P1 failing with |DD| >= 1e-12 predicts R_b >= 3 on the "root distance" hypothesis, while the rival (D sets R) predicts R_b in [1/3, 3] anyway. A start b with |DD| between 1e-15 and 1e-12 is reported as it is, with no hypothesis scored on it.
6. **Threads**: the two solves one BLAS thread each (2 busy threads), then the two sigma runs two BLAS threads each (4 busy threads), BelowNormal, nothing else of mine running. A run unfinished after 6 h is stopped and reported with what it printed. A pilot of the hardest case is the K = 7 solve itself (about 30 min); the sigma run starts only after both solves are read.

## Run record

- 18:59 UTC: `rt_sigma.py --planted` exits 0 (best bound 1.4103e-21 in [1e-22, 1e-20], `logs/planted.log`) and `--planted --mutate=shift` exits 1 (1.4244e-19, FAIL, `logs/planted_mutate_shift.log`). `table_701.py --selftest` passes (four planted cases, the mutation turns HOLDS into FAILS).
- 18:59:22 UTC: the two solves were first started by a driver launched without tracking, and stopped after 28 s (`taskkill /T /F`) before any Newton iteration had finished; the files they had begun were deleted, and `run_701_solves.py` was started again at 18:59:50 UTC (the first launch's two lines stay in `logs/run_701.log`).
- 19:19:27 UTC: both solves done, exit 0 (`k0b_D40` 932 s, `k7b_D40` 1172 s; 2 busy threads). `--resample_mp` accepted 141 to 121.

## Part 1 (the solves, read before any sigma bound): results

| solve | horizon K | ok | last Newton max abs F | counts (ok and at most 1e-36) | Delta_RT - Delta_hp |
|---|---|---|---|---|---|
| `k7b_D40` | 7 | True | 2.15e-38 | yes | +1.5513e-15 |
| `k0b_D40` (`--mutate=norows`) | 0 | True | 4.99e-41 | yes | +1.5449e-15 |

Delta(K 7) = 1.88845166449061538929462279651 and Delta(K 0) = 1.88845166449061538285634610600 (the records' `Delta_str`), so **DD = Delta(K 7) - Delta(K 0) = +6.4383e-18** (start a: 6.8e-18). P1 (|DD| < 1e-15) holds, and |DD| is below 1e-12, so the "root distance" outcome of the prediction's last bullet is not the one that occurred. Both solves count by the issue's rule. Delta_RT - Delta_hp is +1.55e-15 for both, as for #671's solves at D 40.02 from start a (+1.5517e-15 for K = 7, +1.5449e-15 for K = 0, `I671-win/solves/*.jsonl`). The sigma runs (12 rough starts each, two at once, two BLAS threads each) started at 19:19:36 UTC.

## Part 2 (the sigma runs and the verdict): results

Both rough runs (12 starts each, two BLAS threads each, started 19:19:36 UTC) ended with exit 0: `K0b_D40` after 2469 s (20:00:45 UTC) and `K7b_D40` after 3861 s (20:23:57 UTC). My 3.5 h estimate in the 19:29 post was wrong: it came from #681's 3.8 h, whose K = 7 starts ran to the 250-product cap, and none of this run's did. `table_701.txt` is the output of `table_701.py`.

| K | n starts | best | Q1 | **median (the bound)** | Q3 | max | max/min | starts at the 250 cap | worst residual max abs J x - v |
|---|---|---|---|---|---|---|---|---|---|
| 7 | 12 | 3.38e-33 | 5.45e-33 | **1.426e-32** | 2.86e-32 | 8.37e-32 | 24.8 | 0 of 12 | 4.1e-16 |
| 0 | 12 | 8.57e-34 | 1.18e-33 | **2.417e-33** | 4.13e-33 | 5.89e-33 | 6.9 | 0 of 12 | 4.4e-19 |

All 24 starts' x are class "mixed" (#423's rules, as in #681). The 12 bounds, sorted: K = 7: 3.38e-33, 4.89e-33, 5.02e-33, 5.91e-33, 1.06e-32, 1.32e-32, 1.54e-32, 1.55e-32, 2.83e-32, 2.89e-32, 3.25e-32, 8.37e-32. K = 0: 8.57e-34, 8.94e-34, 1.02e-33, 1.35e-33, 1.95e-33, 2.33e-33, 2.50e-33, 2.78e-33, 3.44e-33, 4.96e-33, 5.27e-33, 5.89e-33.

**Verdict, by the rules of the choices above.** The error bars are the bootstrap 95% intervals (10000 resamples of each run's 12 start bounds with replacement, `random.Random(701)`), a spread over the random starts, not an enclosure.

| quantity | value | 95% bootstrap interval | against [1/3, 3] |
|---|---|---|---|
| P1: DD = Delta(K 7) - Delta(K 0) | +6.4383e-18 | | holds (below 1e-15, and below 1e-12) |
| R_b = median(K 7) / median(K 0) | 5.90 | 2.13 to 14.67 | **UNDECIDED** (the point is outside, the interval straddles 3) |
| R_b / R_a, R_a = 0.98 | 6.02 | 2.17 to 14.97 | UNDECIDED (the other reading of P2, README choice 1; the two readings agree) |
| best-of-12 ratio (context) | 3.94 | | |

So P1 holds, and P2 is **not confirmed and not refuted**: the point R_b = 5.90 lies outside the window the prediction named, and the interval reaches down to 2.13. R_a's own uncertainty is not in the R_b / R_a interval (R_a is a constant there). Because P1 holds, the prediction says both the root-distance hypothesis and the rival (D sets R) expect R_b in the window; this outcome therefore does not separate them, and the point value strains both alike.

**Context, not criteria.** With the same D = 40.020065 and the K = 7 and K = 0 roots coinciding to 6.4e-18 (start a: 6.8e-18):

| | R at D 40.02 (median ratio) | best-of-12 ratio | K = 7 median | K = 0 median | K = 7 starts at the 250 cap |
|---|---|---|---|---|---|
| start a (#681) | 0.98 | 1.38 | 2.403e-34 | 2.463e-34 | 12 of 12 |
| start b (here) | 5.90 | 3.94 | 1.426e-32 | 2.417e-33 | 0 of 12 |

R at start b is near #681's R at D 50.007 (5.88) and D 54.996 (7.12), both from start a, and above its 0.98 at D 40.02. The start-b bounds are 59 times (K = 7) and 9.8 times (K = 0) larger than start a's at the same D. The two starts' Delta differ by -3.668e-19 (K = 7) and -2.743e-20 (K = 0). The K = 7 runs of the two starts did not stop alike: all 12 starts of start a's K = 7 state stopped at the 250-product cap (worst residual 4.3e-14), none of start b's did (4.1e-16). #681 argued that its bounds hold to a relative accuracy of the residual, far below the spreads; I did not test whether the cap changes the median, and I do not know why start a's K = 7 system needs more products.

## Recommended tasks (for the coordinator)

1. **Is start a's R(40.02) = 0.98 a product-cap artefact?** What: `rt_sigma.py --starts 3 --rough --max_products 1000` on `I671-win/solves/k7_D40_D40.0201_32x121.npz` (12 of 12 starts capped at 250 in #681; its first three bounds are 1.257e-34, 9.921e-34, 7.797e-34). Acceptance (can fail): each of the three bounds within a factor 1.5 of #681's (the cap is not limiting) or not (it is), and how many starts still reach the cap; the control is the same command at `--max_products 250`, which must reproduce #681's three bounds to 3 digits. Depends on #701. About 4 h at 2 threads, if each start uses the whole cap (scaled from #681's 3.8 h for 12 starts at 250).
2. **More starts for the pair.** What: `rt_sigma.py --starts 48 --rough` on each of the two start-b states, to see whether R_b's interval (2.13 to 14.67) narrows to one side of 3. Acceptance: the first 12 bounds of each run reproduce this run's to 3 digits (the start index sets the draw, as #681's reproduction of starts 0 to 2 showed), and R_b with its 95% bootstrap interval from the 48 starts against [1/3, 3]. Depends on #701. About 4.3 h at 4 threads (the K = 7 run, scaled from 64 min per 12 starts).
