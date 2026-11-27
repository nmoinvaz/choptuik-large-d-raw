# I1105-dh170: how the horizon series start u0 and the tau grid N move the last block's residual of win2's k_c 135 state at D 23.0 (step 1, residual checks on a stored state, no solve)

Machine `dh170` (Fedora, i7-7700, 4 cores / 8 threads, 31 GiB), account claude-me2. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1105 (depends on #1103). Coordinator t5. Written 2026-11-27 07:44 UTC by the clock, before any run of this folder (the worktree, the pins and the script's header came first; the order is quoted at the end). Runs beside the #1101 scans (`I1101-dh170/`), which keep priority.

## Bars (t5's, fixed before the run; each can fail)
1. `i1105_u0.py STATE 23.0 135 u0_kc135_d23.json --u0=0.01,0.015,0.02,0.03,0.04,0.05,0.06 --N=408,544,816,1088` exits **0**. Its exit is its sanity check: u0 0.04 at the record's N reproduces the record system's residual bit for bit (`np.array_equal` of F).
2. The control `... u0_kc135_d23_mut.json --u0=0.04 --N=408 --mutate=steps` (one RK step added to the horizon segment; the sanity check must fail) exits **1**. Otherwise stop and report.
3. |F| at u0 0.04, N 408 matches the record's **3.188e-10 to 1%** (t5's number). The record `l1kc135win2d23.jsonl` (bc295fbc) says F = 3.1834404599371294e-10; 3.188e-10 and 3.1834e-10 differ by 0.14%, and I read the bar against both: the interval is 3.156e-10 to 3.220e-10 either way.

## Reading rules (t5's, stated before the run; the numbers are reported as measured, whichever way they fall)
- **N:** if dF_last at u0 0.02 changes by less than 20% from N 816 to 1088, that limit is the u0 effect proper, and the part that falls with N is aliasing. (Change = |dF(1088) - dF(816)| / dF(816).)
- **Horizon RK:** if `hz2` (horizon steps doubled, u0 0.02, N 408) moves dF_last by less than 10% from the sweep's dF_last at u0 0.02, N 408, the horizon segment's RK is not the cause, as #1103 found. More than that makes it a cause.
- **Shape in u0:** a power fit of dF_last over u0 0.02 to 0.06. p near 30 means the series cut (Ks 30), p of 4 to 5 an RK error, and p of 0 to 1 a matching error between the series and the segment. dF_last is the change of the last block against u0 0.04 at the same N, so it is zero at the reference and is a difference of two errors: dF(u0) = e(u0) - e(0.04). I therefore fit two things and name each: (a) the log-log slope of |dF| between neighbouring u0 (0.02 to 0.03, 0.05 to 0.06), which is **not** p when e(0.04) is not negligible; (b) the model dF = c (u0^p - 0.04^p), p by least squares on ln|dF| over the nonzero points, c free in sign, which is p when e = c u0^p. Both are estimator values from at most four points per N, not error bars. `read_1105.py` is written while the sweep runs, from the JSON only, and has a planted selftest for (b) (p = 0.5, 4.5, 30 recovered; mutation `--mutate=ref` must fail it); it is pushed with the result and the definitions above are fixed now.
- **Bands:** where dF_last sits by tau harmonic (0-10, 11-50, 51-100, 101+), at u0 0.02 and 0.06, for each N.

## Pins (by blob, `git hash-object --no-filters`; the driver refuses any other)
| what | where | blob |
|---|---|---|
| code | worktree `~/Source/choptuik-large-d-1105` at `5b1e38e8` of `wip/i1105-u0`, `solver/matter/` | |
| script | `i1105_u0.py` | e522a5e7 |
| solver | `dss_ell.py` (the blob of the regrid worktrees' 48c36355) | 5d28c19e |
| state | raw `I1025-win2/kc135_d23/sol_l1kc135win2d23_D23.0000.npy`, copy in `in/` | cd134e2c |
| record | `l1kc135win2d23.jsonl` (|F| 3.1834e-10, 4441 steps, Delta 1.1743190138598711, D 23.0, k_c 135, kappa 0.7, u0 0.04, Ks 30) | bc295fbc |
| python | `~/Source/choptuik-large-d-1058b/.venv` (3.14.10), run with `-I` | |

## Commands (`run_1105.sh`, unit `i1105a` under systemd-inhibit; steps and exits in `steps.txt`; OMP, OPENBLAS, MKL threads = 1; nice 10; one process at a time)
1. `cd ~/Source/choptuik-large-d-1105/solver/matter; python -I -u i1105_u0.py STATE 23.0 135 u0_kc135_d23.json --u0=0.01,0.015,0.02,0.03,0.04,0.05,0.06 --N=408,544,816,1088` (the record's N is 4 ceil((3 k_c + 2)/4) = 408). Log `u0_kc135_d23.log`, result `u0_kc135_d23.json`.
2. `... u0_kc135_d23_mut.json --u0=0.04 --N=408 --mutate=steps`, log `u0_kc135_d23_mut.log`; exit 1 wanted.
3. `read_1105.py u0_kc135_d23.json` prints the table and the readings above.

## Predictions (mine, registered before the run; information, not pass rules)
| item | prediction |
|---|---|
| sweep exit 0 and control exit 1 | 90% (the Mac's k_c 31 run passed and failed as wanted; the k_c 135 state is a record system of the same code) |
| |F| at u0 0.04, N 408 | within 1% of 3.188e-10: 90% |
| dF_last at u0 0.02, N 408 | 2.0e-8 within 10% (#1103's number): 80% |
| N 816 to 1088 change of dF_last at u0 0.02 | below 20%: 60% (1.4e-8 at 816; the fall slows) |
| hz2 against the sweep's dF_last at u0 0.02 | more than 10% (a cause): 65% (#1103: 2.0e-8 to 1.75e-8, 12%) |
| shape (b), p at N 408 | p of 4 to 5: 25%; p of 0 to 1: 20%; p above 10: 20%; elsewhere or no power law: 35% |
| bands at u0 0.02 | band 0-10 largest: 50%; band 11-50 largest: 25% |
| wall | 0.5 to 2.5 h on one thread beside the #1101 scans (t5: under 1 h); peak RSS under 6 GiB: 70% |

## Status
- 2026-11-27 07:44 UTC: folder, pins, bars, reading rules, predictions and the driver written before any run; `run_1105.sh` starts next.

## Order, verbatim

### t5's hc (27 Nov 07:43 UTC)
> t5 07:43 UTC: a second task beside #1101, using your spare threads: #1105 step 1, comment 7212742507 (it is the record; read #1105's body first). In short: a worktree of wip/i1105-u0 at 5b1e38e8 (i1105_u0.py blob e522a5e7); win2's k_c 135 D 23.0 state (raw I1025-win2/kc135_d23/sol_l1kc135win2d23_D23.0000.npy, blob cd134e2c); from solver/matter, 1 process, 1 thread (OMP/OPENBLAS/MKL=1), nice 10, a systemd unit: 'python i1105_u0.py STATE 23.0 135 u0_kc135_d23.json --u0=0.01,0.015,0.02,0.03,0.04,0.05,0.06 --N=408,544,816,1088', then the control '--u0=0.04 --N=408 --mutate=steps' (must exit 1). Bars: exit 0 and the control 1; |F| at u0 0.04, N 408 matches 3.188e-10 to 1%. Raw folder I1105-dh170/, README with the bars first. The #1101 scans keep priority: if R2 lands while this runs, start R2's scan anyway; this run takes only 1 thread. Report the table (or its path) when done and post it on #1105. Python: your ~/Source/choptuik-large-d-1058b/.venv.

### #1105 comment 7212742507

> **Step 1 on dh170** (t5, 2026-11-27 07:42 UTC by the clock). The code is `solver/matter/i1105_u0.py` on `wip/i1105-u0`
> at 5b1e38e8 (blob e522a5e7). On the k_c 31 state of #1102's gate (raw `I1102-mac/in/`, D 10.5), the sanity check
> passes (exit 0) and `--mutate=steps` fails it (exit 1). At that state, u0 0.04 → 0.02 already moves the last block by
> 7.5e-11 against |F| 4.3e-12, and doubling the horizon steps cuts that to 3.0e-11.
> 
> **Run.** A worktree of `wip/i1105-u0` at 5b1e38e8. State: win2's k_c 135 at D 23.0 (raw `I1025-win2/kc135_d23/`,
> `sol_l1kc135win2d23_D23.0000.npy`, blob cd134e2c), blob-checked. From `solver/matter`, 1 process, 1 thread (OMP,
> OPENBLAS, MKL = 1), nice 10, after the #1101 scans in priority:
> 
> ```
> python i1105_u0.py STATE 23.0 135 u0_kc135_d23.json --u0=0.01,0.015,0.02,0.03,0.04,0.05,0.06 --N=408,544,816,1088
> python i1105_u0.py STATE 23.0 135 u0_kc135_d23_mut.json --u0=0.04 --N=408 --mutate=steps
> ```
> 
> **Bars, written before the run.**
> 1. The first command exits 0 (sanity), and the control exits 1. Otherwise stop and report.
> 2. |F| at u0 0.04, N 408 matches the record (3.188e-10) to 1%.
> 
> **Reading, stated before the run** (the numbers are reported as measured, whichever way they fall):
> - **N:** if dF_last at u0 0.02 changes by less than 20% from N 816 to 1088, that limit is the u0 effect proper, and
>   the part that falls with N is aliasing.
> - **Horizon RK:** if hz2 moves dF_last by less than 10%, the horizon segment's RK is not the cause, as #1103 found.
>   More than that makes it a cause.
> - **Shape in u0:** a power fit of dF_last over u0 0.02–0.06. p near 30 means the series cut (Ks 30), p of 4–5 an RK
>   error, and p of 0–1 a matching error between the series and the segment.
> - **Bands:** where dF_last sits by τ harmonic (0–10, 11–50, 51–100, 101+).
> 
> Raw folder `I1105-dh170/`, README with these bars first. Estimate: under 1 h.
> 

## Result (27 Nov 07:44:42 to 08:00:35 UTC = 953 s; unit `i1105a`; 1 process, 1 thread, nice 10; `u0_kc135_d23.json`, `u0_kc135_d23.log`, `u0_kc135_d23_mut.json`, `u0_kc135_d23_mut.log`, `results_1105.md`, `steps.txt`)
The sweep ran 935 s (peak RSS 176 MiB), the control 18 s. `read_1105.py` selftest exit 0 and `--mutate=ref` exit 1 (`selftest_read_1105*.txt`).

| bar | wanted | result |
|---|---|---|
| sweep exit | 0 (sanity: u0 0.04 at N 408 reproduces the record system's F bit for bit) | **0**, 935 s, peak RSS 176 MiB |
| control `--mutate=steps` exit | 1 | **1**, 18 s |
| \|F\| at u0 0.04, N 408 | 3.188e-10 within 1% | **3.1822e-10** (-0.18%; the record's field F is 3.1834e-10, +0.04% from this) |

**dF_last** (norm of the last block's change against u0 0.04 at the same N), `results_1105.md` has the bands and seconds:

| u0 | N 408 | N 544 | N 816 | N 1088 |
|---|---|---|---|---|
| 0.010 | 7.626e-06 | 6.995e-06 | 6.341e-06 | 1.022e-05 |
| 0.015 | 2.225e-07 | 2.153e-07 | 1.988e-07 | 4.849e-06 |
| 0.020 | 1.725e-08 | 1.698e-08 | 1.616e-08 | 4.985e-06 |
| 0.030 | 4.478e-10 | 4.368e-10 | 6.381e-10 | 4.977e-06 |
| 0.040 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.000e+00 |
| 0.050 | 1.662e-10 | 1.660e-10 | 2.851e-08 | 4.091e-04 |
| 0.060 | 3.846e-08 | 3.843e-08 | 1.056e-06 | 1.455e-02 |

**|F_last|** (the last block's own residual):

| u0 | N 408 | N 544 | N 816 | N 1088 |
|---|---|---|---|---|
| 0.010 | 7.626e-06 | 6.995e-06 | 6.340e-06 | 7.727e-06 |
| 0.015 | 2.225e-07 | 2.154e-07 | 1.990e-07 | 2.242e-07 |
| 0.020 | 1.723e-08 | 1.695e-08 | 1.633e-08 | 1.778e-08 |
| 0.030 | 4.463e-10 | 4.389e-10 | 4.271e-10 | 1.617e-08 |
| 0.040 | 2.249e-10 | 2.248e-10 | 4.243e-10 | 4.978e-06 |
| 0.050 | 2.734e-10 | 2.734e-10 | 2.854e-08 | 4.101e-04 |
| 0.060 | 3.846e-08 | 3.843e-08 | 1.056e-06 | 1.455e-02 |

**Readings, as measured** (t5's rules, stated before the run; `read_1105.py`, selftest exit 0, `--mutate=ref` exit 1):
- **N:** dF_last at u0 0.02 is 1.725e-8, 1.698e-8, 1.616e-8 and 4.985e-6 at N 408, 544, 816, 1088. The rule read literally (change 816 to 1088 below 20%): **not met** (3.1e4 %). The cause is the reference: the u0 0.04 evaluation at N 1088 has a last-block residual of 4.98e-6 (2.2e-10 at N 408 and 544, 4.2e-10 at N 816), so every dF at N 1088 is that reference. The rule is therefore **not settled** by N 816 to 1088. Read as |F_last| at u0 0.02, a different quantity chosen after the run: 1.633e-8 (816) and 1.778e-8 (1088), +8.9%.
- **Horizon RK:** hz2 (3508 horizon steps) gives dF_last 1.700e-8 against 1.725e-8 (**1.5%**, below 10%): the horizon segment's RK is **not** a cause. The series to order 45 gives 1.724e-8 (0.1%): not the series cut at u0 0.02.
- **Shape in u0:** the points do not follow one power law. On the low side the neighbour slope of dF_last is -8.7 (u0 0.01 to 0.015), -8.9 (0.015 to 0.02) and **-9.0** (0.02 to 0.03) at N 408 (-9.0 at N 544, -8.0 at N 816): dF_last grows as u0 shrinks, about u0^-9; there e(0.04) is negligible against dF (2.2e-10 against 1.7e-8 at 0.02), so the slope is p. On the high side the slope between 0.05 and 0.06 is **+29.9** (N 408, 544; +19.8 at 816, +19.6 at 1088); it is p only if e(0.04) is negligible, and it is not (dF at 0.05 is 1.7e-10 against the reference's 2.2e-10), so +29.9 is consistent with the series cut's 30 and not established as it. Model (b), a single p over the four points, fits badly (rms of ln|dF| 1.98 at N 408 and 544, p = 0.53 and 0.59), so its p is not a reading; at N 1088 the fit is good (rms 0.01, p = 19.7) only because dF is the reference's.
- **Bands:** at u0 0.02 the 0-10 band is the largest at every N (norm 1.64e-8 of the total 1.725e-8 at N 408), with 101+ next (5.4e-9). At u0 0.06 and N 408, 544 the 101+ band holds it (3.8e-8); at N 816, 1088 the 0-10 band does.

| N | u0 | 0-10 | 11-50 | 51-100 | 101+ |
|---|---|---|---|---|---|
| 408 | 0.02 | 1.64e-08 | 2.74e-10 | 1.75e-10 | 5.41e-09 |
| 408 | 0.06 | 3.30e-11 | 2.70e-13 | 3.09e-12 | 3.85e-08 |
| 816 | 0.02 | 1.52e-08 | 3.81e-10 | 1.52e-10 | 5.41e-09 |
| 816 | 0.06 | 9.93e-07 | 3.51e-07 | 6.60e-08 | 3.96e-08 |

**What disagrees or stands out (reported, not reconciled):**
- #1105's body quotes dF_last at u0 0.02 of 2.0e-8, 1.6e-8 and 1.4e-8 at N 408, 544, 816 (#1103). Here, at the same state and settings, it is 1.725e-8, 1.698e-8 and 1.616e-8: 14% lower at N 408 and falling 6% from 408 to 816, not 30%. The last block's whole |F_last| (all five fields) is 1.723e-8 at N 408, so the p-field alone cannot be 2.0e-8 against this run's. #1103's hz2 (2.0e-8 to 1.75e-8, 12%) differs from this run's 1.5% too.
- For u0 at or above 0.04 the last block's residual grows with N: at u0 0.05, 2.7e-10 (N 408, 544), 2.9e-8 (816), 4.1e-4 (1088); at 0.06, 3.8e-8, 3.8e-8, 1.1e-6, 1.5e-2. The u0 0.04 reference follows (2.2e-10, 2.2e-10, 4.2e-10, 5.0e-6). The record's N is 408.
- At N 408 the last block's own residual has its minimum between u0 0.03 and 0.05 (4.5e-10, 2.2e-10, 2.7e-10 at 0.03, 0.04, 0.05), so the record's u0 0.04 sits near the bottom of a V: dF_last about u0^-9 on the low side, rising again above 0.05 (slope +29.9 at N 408, with the caveat above).

### Predictions scorecard (mine, registered before the run)
| prediction | result |
|---|---|
| sweep exit 0 and control exit 1 (90%) | right |
| \|F\| at u0 0.04, N 408 within 1% of 3.188e-10 (90%) | right: 3.1822e-10 |
| dF_last at u0 0.02, N 408 = 2.0e-8 within 10% (80%) | WRONG: 1.725e-8, 14% below |
| N 816 to 1088 change below 20% (60%) | WRONG as the rule reads: 3.1e4 % (the N 1088 reference is 4.98e-6) |
| hz2 moves dF_last by more than 10%, a cause (65%) | WRONG: 1.5% |
| shape, (b) p at N 408: 0 to 1 (20%), 4 to 5 (25%), above 10 (20%), elsewhere (35%) | p = 0.53 formally in the 0-1 bin, but the fit is poor (rms 1.98 in ln), so not a reading; the neighbour slopes are -9.0 and +29.9 |
| bands at u0 0.02: 0-10 largest (50%) | right, at every N |
| wall 0.5 to 2.5 h (t5: under 1 h); peak RSS under 6 GiB (70%) | wall WRONG, shorter: 935 s + 18 s; RSS right: 176 MiB |

## Status
- 2026-11-27 08:05 UTC: step 1 done: both bars met; the N rule is not settled because the N 1088 reference is itself 4.98e-6; the horizon RK is not a cause (1.5%); the u0 dependence is about u0^-9 on the low side. Posted on #1105.

# Step 1b: does the record's u0 0.04 carry a lambda bias? (k_c 55, D 16, re-solves at u0 0.03, 0.04, 0.05 and their roots)

Written 2026-11-27 2026-11-27 08:11 UTC by the clock, before any run of step 1b (the inputs, the pins, the drivers and the bars came first; the order is quoted at the end of this section). Folder `step1b/`. Issue #1105; coordinator t5.

## Bars (t5's, fixed before the run; each can fail)
T3 = root(U30) - root(U40) and T5 = root(U50) - root(U40), both against the re-solve at u0 0.04 in the same code. The solve scatter here is about 1e-5 (the Ks 45 re-solve moved the root by 1.0e-5).
- **|T3| <= 1e-4:** the lambda shift falls with u0 at least as fast as u0^-9.7 (which predicts -1.5e-5). Then the record's u0 0.04 carries no u0 bias above about 1e-4/16, and ELL.md's -8.1e-4 is the u0 0.02 run's own.
- **|T3| >= 3e-4:** the bias is smooth in u0 (a linear law gives about -4e-4), so u0 0.04 is biased too, and the issue becomes a correction.
- **Between:** mixed, reported as measured. **T5** is reported against the prediction |T5| <= 1e-4.
- Each run's |F| and steps are reported. **A re-solve whose |F| exceeds 1e-8 is not rooted**, and that is reported.
- A root is read only from a `d18_secant.py run` that ends with status `tol`, both bracket ends robust and of opposite hybrid signs; anything else is reported as it is and T is not formed from it. The root is `lam_lin` (det-linear inside the final bracket, width at most 1e-7); `lam_brent` is printed beside it. Both are estimator values at the width of the final bracket, not rigorous enclosures.
- For information, not a bar: root(U40) against P4's re-root of the record at u0 0.04, 2.2440428096; the u0 0.02 root 2.2432296517 (T1 = -8.13e-4, raw `I1025-mac/u0resolve_note.log`); t5's hypothesis (an error at the series start carried to the last node by the homogeneous solution u^mu, mu about 9.7) predicts T3 about -1.5e-5 and T5 about +9e-7.

## Pins (by blob; the driver refuses any other)
| what | where | blob |
|---|---|---|
| source state | raw `I1025-mac/out/sol_l1kc55Fb1025_D16.0000.npy` (copies in `step1b/in/` and the regrid worktree's `solver/matter/data/`) | 94c8b048 |
| source record | `l1kc55Fb1025.jsonl` (D 16: |F| 1.7853e-10, 2565 steps, u0 0.04, Ks 30, kappa 0.7, Delta 1.0017135137307174, lambda 2.2426280416106374) | 5be40af4 |
| re-solve | worktree `~/Source/choptuik-large-d-1025k79` at 48c36355 (dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399's), `ell_refine.py` | 631e5801 |
| root | worktree `~/Source/choptuik-large-d-1102` at d4b6b6ce, `d18_secant.py` 9706e506 (`--b12=rust`), ellrs in `~/Source/ellrs-site-1102` | |
| python | `~/Source/choptuik-large-d-1058b/.venv` | |

## Commands (`step1b/run_step1b.sh TAG U0`, units `i1105u30`, `i1105u40`, `i1105u50` under systemd-inhibit, started together; steps in `steps_1b.txt`)
From `solver/matter` of the regrid worktree, 2 threads each (OMP, OPENBLAS, MKL = 2), `nice -n 10 timeout 10800` (cap 3 h on the python pid, no retry):
```
U30  python -u ell_refine.py l1kc55Fb1025 55 l1kc55u030 55 1 16 2.2426280416106374 --kappa 0.7 --u0 0.03 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
U40  python -u ell_refine.py l1kc55Fb1025 55 l1kc55u040 55 1 16 2.2426280416106374 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
U50  python -u ell_refine.py l1kc55Fb1025 55 l1kc55u050 55 1 16 2.2426280416106374 --kappa 0.7 --u0 0.05 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```
Then, if |F| <= 1e-8, from the #1102 worktree's `solver/matter`, 1 thread, nice 10, `PYTHONPATH=SITE`: `d18_secant.py run RECORD STATE 16 2.238 2.250 root_<TAG>.jsonl --tol=1e-7 --maxev=20 --b12=rust --b12_threads=1 --pin=<state blob>,<record blob>` (`--maxev=20` raised from the default 12 so that the width 1e-7 is reached; t5's order gave no value). `d18_secant.py` takes u0, Ks, kappa and the steps from the record. `read_1105b.py` (written while the runs go; planted selftest, `--mutate=ref` must fail it) forms T3 and T5 and reads them against the bars above.
Priority: R2's scan (#1101, 4 processes, 1 thread each) starts at once when `I1101-win2/R2/` lands, and shares the machine with these runs (6 threads of re-solves + up to 4 of scan on 8 logical CPUs; all at nice 10).

## Predictions (mine, registered before the run; information, not pass rules)
| item | prediction |
|---|---|
| |F| <= 1e-8 after the re-solve | U40 90%, U30 90%, U50 85% (the u0 0.02 re-solve at k_c 55 stopped at 1.0e-9) |
| root(U40) against 2.2440428096 | within 1e-4: 85% (the re-solve scatter is about 1e-5) |
| T3 | \|T3\| <= 1e-4: 55%; >= 3e-4: 20%; between: 25% |
| T5 | \|T5\| <= 1e-4: 65% |
| re-solve wall (2 threads, nice 10, beside the other two) | 0.5 to 2 h: 60% (the Mac's u0 0.02 LM took 1781 s) |
| root wall (1 thread; 12 to 20 evaluations) | 1 to 3 h per state: 50% |

## Status
- 2026-11-27 08:11 UTC: inputs staged and blob-checked, driver, bars and predictions written before any step 1b run; the three units start next.

## Order, verbatim

### t5's hc (27 Nov, after step 1 was accepted)
> t5: #1105 step 1 accepted (your table, and the machine difference is explained on #1105: comment 7213176945, Mac runs in raw I1105-mac). Next, #1105 step 1b, comment 7213197061 (the record): re-solve the k_c 55 D 16 state (raw I1025-mac/out/sol_l1kc55Fb1025_D16.0000.npy blob 94c8b048, record l1kc55Fb1025.jsonl blob 5be40af4, blob-checked into ~/Source/choptuik-large-d-1025k79/solver/matter/data/) at u0 0.03, 0.04 and 0.05 with the three ell_refine.py lines of the comment, together, 2 threads each, nice 10, systemd units, cap 3 h each. Then root each with d18_secant.py run (worktree -1102, --b12=rust if run takes it) on the bracket 2.238-2.250, --tol=1e-7. Report T3 = root(U30) - root(U40) and T5 = root(U50) - root(U40) against the bars in the comment (|T3| <= 1e-4 or >= 3e-4). A re-solve with |F| > 1e-8 is not rooted. Raw: a new section in I1105-dh170/README.md first. R2's scan (#1101) has priority when I1101-win2/R2/ lands: start it at once and let these runs share the machine.

### #1105 comment 7213197061

> **Step 1b on dh170: does the record's u0 0.04 carry a λ bias?** (t5, 2026-11-27 08:08 UTC by the clock)
> 
> At k_c 55, D 16, a re-solve at u0 0.02 moved the root by −8.13e-4 (raw `I1025-mac/u0resolve_note.log`, 2026-11-20)
> and stopped at |F| 1.0e-9, five times the u0 0.04 record's 1.79e-10. This step re-solves the same state at u0 0.03,
> 0.04 and 0.05 and roots each one.
> 
> **Inputs.** Raw `I1025-mac/out/`: state `sol_l1kc55Fb1025_D16.0000.npy` (blob 94c8b048), record `l1kc55Fb1025.jsonl`
> (5be40af4), blob-checked into the regrid worktree's `solver/matter/data/` (dh170: `~/Source/choptuik-large-d-1025k79`,
> 48c36355, `ell_refine.py` 631e5801).
> 
> ```
> U30  python ell_refine.py l1kc55Fb1025 55 l1kc55u030 55 1 16 2.2426280416106374 --kappa 0.7 --u0 0.03 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
> U40  python ell_refine.py l1kc55Fb1025 55 l1kc55u040 55 1 16 2.2426280416106374 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
> U50  python ell_refine.py l1kc55Fb1025 55 l1kc55u050 55 1 16 2.2426280416106374 --kappa 0.7 --u0 0.05 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
> ```
> 
> The three together, 2 threads each, nice 10, a cap of 3 h each. Then for each state, `d18_secant.py run` (the #1102
> worktree `~/Source/choptuik-large-d-1102`, d4b6b6ce; `--b12=rust` if `run` takes it, otherwise the default block) on
> the bracket 2.238–2.250, `--tol=1e-7`, with its sign and robustness checks. The u0 0.02 root was 2.2432297 and the u0
> 0.04 one 2.2440428.
> 
> **Bars, written before the run.** T3 = root(U30) − root(U40) and T5 = root(U50) − root(U40), both against the re-solve
> at u0 0.04 in the same code. The solve scatter here is about 1e-5 (the Ks 45 re-solve moved the root by 1.0e-5).
> - **|T3| ≤ 1e-4:** the λ shift falls with u0 at least as fast as u0⁻⁹·⁷ (which predicts −1.5e-5). Then the record's
>   u0 0.04 carries no u0 bias above about 1e-4/16, and ELL.md's −8.1e-4 is the u0 0.02 run's own.
> - **|T3| ≥ 3e-4:** the bias is smooth in u0 (a linear law gives about −4e-4), so u0 0.04 is biased too, and this
>   issue becomes a correction.
> - **Between:** mixed, reported as measured. T5 is reported against the prediction |T5| ≤ 1e-4.
> 
> Each run's |F| and steps are reported. A re-solve whose |F| exceeds 1e-8 is not rooted, and that is reported.
> Raw folder `I1105-dh170/`, a new README section first. Estimate about 2 h; R2's root scan (#1101) has priority when
> R2 lands.
> 

### #1105 comment 7213176945 (the reading that motivates it)

> **Reading of step 1, and two checks on the Mac** (t5, 2026-11-27 08:07 UTC, the post's own time; raw `I1105-mac/`, c5bbf8574).
> 
> dh170's sweep (comment 7213077426, raw `I1105-dh170/` b508c982b) gives dF_last ∝ u0⁻⁹ on the low side (slopes −8.7 to
> −9.0). On the high side, u0 0.05–0.06 has slope +29.9, which is the series cut at Ks 30. The low-side slope is close to
> the horizon's homogeneous exponent, Re μ ≈ 9.7 (#1103's closing summary, item 6).
> 
> Two checks on the Mac, same code (5b1e38e8) and state (cd134e2c):
> 
> | quantity | dh170 (Linux, OpenBLAS) | Mac (Accelerate) |
> |---|---|---|
> | dF_last, u0 0.02, N 408 | 1.725e-8 | 2.018e-8 (#1103's 2.0e-8 was also the Mac's) |
> | dF_last, u0 0.02, N 544 | 1.698e-8 | 1.628e-8 |
> | hz2 against u0 0.02 | 1.5% change | 13% change, with its harmonic bands rearranged |
> | state × (1 + 1e-16 g), seeds 1–4, dF_last at u0 0.02 | — | 2.020, 1.846, 2.036, 2.021e-8 (2.018e-8 without) |
> 
> - **The size is systematic, about 2e-8.** Its last 10–15% is round-off: it differs between machines and moves under
>   1e-16 noise. So the "disagreement with #1103" is the machine, and #1103's N dependence (2.0, 1.6, 1.4e-8) is partly
>   this jitter.
> - **Reading, a hypothesis:** an error e at the series start, roughly independent of u0, is carried to the last node
>   by the homogeneous solution u^μ. It grows by (u_node/u0)^μ, so as u0⁻⁹·⁷. Then the record's u0 0.04 carries about
>   2^−9.7 ≈ 1/830 of the u0 0.02 effect, about 2e-11 in F, below |F| 3.2e-10. Under the same scaling, ELL.md's
>   −8.1×10⁻⁴ in λ at u0 0.02 (k_c 55, D 16) would be about 1e-6 at u0 0.04.
> - **What would refute it:** the λ shift from u0 0.04 → 0.03 at k_c 55, D 16 is predicted at about −1.5e-5 (the
>   scaling (0.03⁻⁹·⁷ − 0.04⁻⁹·⁷)/(0.02⁻⁹·⁷ − 0.04⁻⁹·⁷) ≈ 0.019 times −8.1e-4). A shift near −8e-4 means u0 0.04 is biased
>   too. That is a re-solve and a root, filed as the next step when a machine frees.
> - **Not explained:** the reference at N 1088 has a last block of 4.98e-6 (2.2e-10 at N 408/544). The series or segment
>   does something wrong on that grid; it does not touch the record (N 408).
> 

## Result (27 Nov 08:11:55 to 09:31 UTC; units `i1105u030`, `i1105u040`, `i1105u050` and the added `i1105src`; re-solves 2 threads, roots 1 thread, nice 10; `results_1b.md`, `root_*.jsonl`, `root_*.log`, `resolve_*.log`, `l1kc55u0*0.jsonl`, `sol_l1kc55u0*0_D16.0000.npy`, `steps_1b.txt`)
All three re-solves exited 0 within the cap (2301 to 2477 s) with |F| below 1e-8, so all three were rooted. Selftests before each root: `d18_secant.py` exit 0. `read_1105b.py` selftest exit 0 and `--mutate=ref` exit 1. State and record blobs of the re-solves: U30 939aca10 / 46b7ea52, U40 491eb1e4 / 12a42fc8, U50 85c1d8f3 / 91d66dd0.

| run | u0 | \|F\| | steps | Delta | Delta - source | re-solve s | root s | status | final bracket (robust ends, opposite signs) | root (lam_lin) | evals |
|---|---|---|---|---|---|---|---|---|---|---|---|
| source (added control) | 0.04 | 1.7853e-10 (record) | 2565 | 1.0017135137307 | 0 | - | 845 | nonrobust | (2.2440423618, 2.2441319612), width 8.96e-5 | 2.2440424200 | 9 |
| U30 | 0.03 | 2.5624e-10 | 2778 | 1.0017135137230 | -7.7e-12 | 2474 | 1338 | nonrobust | (2.2429536199, 2.2429752386), width 2.16e-5 | 2.2429751796 | 8 |
| U40 | 0.04 | 1.7851e-10 | 2565 | 1.0017134267209 | -8.7e-8 | 2354 | 1311 | tol | (2.2449017139, 2.2449017639), width 5.00e-8 | 2.2449017148 | 9 |
| U50 | 0.05 | 1.8882e-10 | 2400 | 1.0017132545 | -2.6e-7 | 2301 | 1050 | tol | (2.2449095054, 2.2449095973), width 9.18e-8 | 2.2449095063 | 8 |

**Added control (not in t5's order; t5 accepted it by hc):** the source record (94c8b048, 5be40af4) rooted with the same command (`run_src_root.sh`, unit `i1105src`, 845 s). Its final robust bracket is (2.2440423618, 2.2441319612); the run stopped as `nonrobust` because its last interior point (2.2440424205, hybrid sign -) has dln 0.74. P4's re-root of the record, 2.2440428096, lies inside that bracket, 4.5e-7 above its lower end. **So this scanner and P4 agree on the source state, and the re-solve at the record's own u0 moved the root: U40 - source = +8.59e-4 (lam_lin; +7.70e-4 to +8.59e-4 over the source's bracket).** U50 - source = +8.67e-4; U30 - source is -1.178e-3 to -1.067e-3.

**Readings against the bars (written before the run):**
- **T5 = root(U50) - root(U40) = +7.79e-6**: |T5| <= 1e-4, as predicted (estimator values from `lam_lin`, widths 5e-8 and 9e-8).
- **T3 = root(U30) - root(U40): not formed**, because U30's run ended with status `nonrobust` (the written rule needs `tol`). Its final bracket ends are robust with opposite signs, which bounds T3 to **-1.948e-3 to -1.926e-3**: in the |T3| >= 3e-4 band whichever point of the bracket is the root. This bound is outside the written rule.
- **The bars' premise failed.** The bars assumed a solve scatter of about 1e-5. A re-solve at the record's own u0 and kappa moved the root by +8.6e-4 while |F| stayed 1.785e-10 and Delta moved by -8.7e-8 (steps equal), 86 times the assumed scatter and the size of the effect sought (-8.1e-4 at u0 0.02, ELL.md). U40 and U50 agree to 7.8e-6 and both sit +8.6e-4 above the source; U30 sits 1.1e-3 below it, with a Delta equal to the source's to 8e-12. The root is not a function of Delta here. T3 is 2.2 times the one same-u0 shift measured, a sample of one. So the reading attached to the >= 3e-4 band ("the bias is smooth in u0, so u0 0.04 is biased too") is not drawn: the same-u0 re-solve scatter is as large as T3.
- Against t5's hypothesis (T3 about -1.5e-5, T5 about +9e-7): T5 is about 9 times its value and inside the bar; T3 is more than 100 times its value, but the scatter above sits between them.

| prediction | result |
|---|---|
| \|F\| <= 1e-8 after each re-solve (U40 90%, U30 90%, U50 85%) | right: 2.56e-10, 1.785e-10, 1.888e-10 |
| root(U40) within 1e-4 of 2.2440428096 (85%) | WRONG: +8.59e-4 |
| T3: \|T3\| <= 1e-4 55%, >= 3e-4 20%, between 25% | not formed under the written rule; the robust bracket puts it at -1.948e-3 to -1.926e-3, the >= 3e-4 band (my 55% bin is wrong) |
| \|T5\| <= 1e-4 (65%) | right: +7.79e-6 |
| re-solve wall 0.5 to 2 h (60%) | right: 2301 to 2477 s (0.64 to 0.69 h) |
| root wall 1 to 3 h per state (50%) | WRONG, shorter: 1050 to 1338 s |

## Status
- 2026-11-27 09:32 UTC: step 1b done. T5 +7.79e-6; T3 not formed by the written rule, bounded to -1.95e-3..-1.93e-3; the control (re-solve at u0 0.04 against the source) moved the root by +8.6e-4, so the solve scatter is the limit. Posted on #1105.
