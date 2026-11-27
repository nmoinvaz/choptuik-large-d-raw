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
