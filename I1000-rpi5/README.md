# I1000-rpi5: the M = 7 zero at xi1 0.145, eight perturbed centre solves

Machine rpi5 (Raspberry Pi 5, 4 cores, 8 GB, aarch64), runner. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1000 (#989's recommendation 2, Lemma R), assigned by the coordinator by message
on 2026-11-19. Code: worktree `~/Source/choptuik-large-d-964` fast-forwarded to origin/main acb4b6a8 (since adc1f19e `solver/inner_stokes` changed only in hier.py's new `--polish`, default off; control below),
venv `~/Source/venv-choptuik` (numba 0.68.1, numpy 2.5.4). Started 2026-11-19 01:54 UTC.

## What was run, in order (the task changed twice while it ran)

1. 01:54 to 01:59 UTC, before #1000 existed (the coordinator first named #989 and raw `I989-rpi5/`): the eight solves at **`INNER_NB_RTOL=1e-13`**, code at adc1f19e. Then the coordinator's two corrections: the issue is #1000
   (raw `I1000-rpi5/`, this folder, renamed with `mv`; the scripts and logs keep the `989` in their names), and the rtol is **1e-14** (as #989's runs and Z14c), "if solves already started at 1e-13, stop them by exact pid and restart".
   The 1e-13 solves had finished before the correction arrived (no pid left to stop). They are kept as an extra, named `..._rtol13_...`, and are not the issue's result.
2. Control, 02:03 UTC (after the fast-forward to acb4b6a8): seed 980 at rtol 1e-13 again; its log equals the earlier one (normalized: times, the exit-time Traceback block) except a memory address in one line
   (`logs/ctrl1000_diff.txt`: 4 diff lines, 68 against another seed's log, so the comparison can fail). So the fast-forward changed no bits.
3. 02:03 UTC onward: the issue's run, `INNER_NB_RTOL=1e-14` (checked in the processes' environ), tag `rtol14_xi0145`, logs `logs/hier_nb_M7_rpi5_rtol14_xi0145_s<seed>.log`.

Deviation from the issue's text: it names #974 run 4's driver `run_repeat.py`; that one draws all perturbations from one `random.Random(rngseed)`. "Seeds 980 to 987" for eight solves is read as one generator per solve,
`random.Random(980 + k)`, which `run_pert989.py` does (same `perturbed()` function, same end state, two solves side by side, a standard-error analysis `analyze989.py`). Say if the single-generator reading was meant.

## Written down before the runs (2026-11-19 01:54 UTC; the rtol of the issue's run is 1e-14, see above)

- Eight zero solves at xi1 0.145, `INNER_NB_RTOL=1e-13` for the first set and `1e-14` for the issue's (checked in the processes' environ), `--h3=1e-4`, S and Z of #964, (A, w/w_inf) = (2.719219, 1.000022) fixed, nice 10, two side by side
  (`run_pert989.py`, selftest and three mutations in the script). Start of solve k: the 9-decimal x of the last `level 3 it` line of I989-win2's xi1 0.145 `zero` log
  (`0.1489782, 0.014770826, 0.008424259, 0.001511207, 0.00047421, 0.000121682`, |r_3| 2.8e-7) with every harmonic times 1 + 1e-7 u, u = 2 random() - 1 from `random.Random(980 + k)`,
  six draws in the harmonics' order, k = 0..7 (seeds 980 to 987, one generator per solve, none chained).
- `m7_outer.py --local` with the solves that pass the bar (|r_3| printed below 1e-6) as centre and I989-win2's `dA_pert1` and `dw_pert1` (|r_3| 1.8e-7, 3.5e-7) as offsets
  (read in place from the raw clone, commit ea7df927 of I989-win2's logs; those two are rtol 1e-14 solves on win2, so the offsets differ from the centre in rtol and architecture, as the coordinator's message sets).
  The seed `zero` log is only the source of the end state, not a centre solve.
- Statistics of the centre's r_1 (`run_pert989.py stats`): sigma = sqrt(trace of the sample covariance, ddof 1) (for #989's two solves 0.232, the issue's "about 0.23"), over the solves under the bar and, beside it, over all eight.
  Standard error of the zero, two ways, with the new J (the centre's mean r_1 and the two offsets): `bound` = sigma / (sqrt(n) s_min(J)) (#989's formula) and `prop` = sqrt(trace(J^-1 cov J^-T) / n).
  These are standard errors of the centre mean with J fixed. They do not include J's own noise (the two offset solves are single solves), which `m7_outer`'s estimate does through its J term.
- Compared with: #989's xi1 0.145 zero (2.719313276, 0.999998856), its estimate 1.94e-4 (6.6e-5 noise term, 1.28e-4 J term), and the xi1 0.15 zero of #977 (Z14c, 2.719234224, 1.000024742) and of #974 (2.719236, 1.000026).
- #989's acceptance for this task: 8 centre solves under the bar, sigma and the standard error reported beside 6.6e-5.

## Result (rtol 1e-14, the issue's run; finished 02:08 UTC, 294 s for the eight, two side by side)

Every seed passes the bar. Per seed (the rtol 1e-13 columns are the extra set of 01:54 UTC, code adc1f19e, not the issue's):

| seed | r_1 (1e-14) | \|r_3\| | under 1e-6 | residuals | s | r_1 (1e-13, extra) | \|r_3\| | under | residuals | s |
|---|---|---|---|---|---|---|---|---|---|---|
| 980 | -0.0783 -0.0414i | 8.9e-8 | yes | 567 | 64 | -0.0755 +0.0671i | 9.3e-8 | yes | 688 | 68 |
| 981 | -0.1444 -0.0207i | 3.7e-8 | yes | 581 | 68 | +0.0386 -0.0196i | 1.9e-7 | yes | 424 | 45 |
| 982 | -0.1169 +0.0999i | 7.4e-8 | yes | 944 | 106 | -0.1729 +0.1882i | 2.4e-7 | yes | 499 | 50 |
| 983 | -0.4090 +0.2547i | 3.2e-7 | yes | 568 | 63 | +0.0053 +0.0032i | 6.4e-8 | yes | 820 | 73 |
| 984 | -0.1523 +0.1283i | 1.4e-7 | yes | 568 | 66 | -0.2062 +0.0448i | 4.5e-8 | yes | 941 | 87 |
| 985 | -0.0072 +0.0233i | 1.3e-7 | yes | 491 | 52 | -0.1251 +0.0522i | 2.0e-7 | yes | 519 | 54 |
| 986 | -0.0890 +0.1366i | 2.8e-7 | yes | 595 | 68 | -0.1321 +0.0092i | 3.8e-8 | yes | 772 | 72 |
| 987 | -0.5149 -0.4339i | 2.0e-7 | yes | 567 | 65 | -0.0912 +0.3397i | 7.8e-8 | yes | 745 | 74 |

`m7_outer.py --local` (`logs/m7_outer_rpi5_rtol14_xi0145.txt`) with the eight as centre and I989-win2's `dA_pert1` and `dw_pert1` (rtol 1e-14 on x86 win2, read in place, ea7df927) as offsets, and `analyze989.py`
(`logs/scatter_rtol14_xi0145.txt`, cross-checked against `m7_outer`'s printed zero and singular values, its `--mutate` exits 1):

| | rtol 1e-14 (the issue's) | rtol 1e-13 (extra) | #989 (2 centre solves, 1e-14, win2) | Z14c, xi1 0.15 (#977) |
|---|---|---|---|---|
| zero A, w/w_inf | **2.719293175, 1.000003005** | 2.719267561, 1.000003411 | 2.719313276, 0.999998856 | 2.719234224, 1.000024742 |
| centre r_1 mean (8 solves) | -0.1890 +0.0184i | -0.0949 +0.0856i | -0.2614 +0.0100i | |
| sigma of r_1 (trace of the covariance, ddof 1) | 0.272 | 0.147 | 0.23 | |
| J singular values | 12527, 2382 | 11473, 2259 | 12934, 2486 | |
| **standard error, J fixed**: bound sigma / (sqrt 8 s_min) (#989's formula) | **4.03e-5** | 2.30e-5 | | |
| standard error, J fixed: propagated sqrt(tr(J^-1 cov J^-T) / 8) | 2.29e-5 | 1.57e-5 | | |
| bootstrap with J's noise, robust scale (half the 16-84 percentile width; std is heavy-tailed: 2.9e-3) | 3.58e-5 | 2.11e-5 | | |
| `m7_outer` estimate (half-range noise + J term) | 3.7e-4 (1.4e-4 + 2.2e-4) | 1.6e-4 | 1.94e-4 | 9.1e-6 |
| distance from Z14c (A, w/w_inf) | **6.28e-5** (+5.90e-5, -2.17e-5) | 3.96e-5 (+3.33e-5, -2.13e-5) | 8.3e-5 | |

Acceptance of the issue, as fixed before the run: the 0.145 estimate is "a standard error over the passing solves", Z14c's is its 9.1e-6, and the distance must be at most their sum.

| form of the 0.145 estimate | sum with Z14c's 9.1e-6 | distance 6.28e-5 is | verdict |
|---|---|---|---|
| bound sigma / (sqrt 8 s_min), 4.03e-5 | 4.94e-5 | 1.27 x the sum | **fails** |
| propagated, 2.29e-5 | 3.20e-5 | 1.96 x the sum | fails |
| bootstrap with J's noise, robust, 3.58e-5 | 4.49e-5 | 1.40 x the sum | fails |
| `m7_outer`'s own estimate, 3.7e-4 | 3.8e-4 | 0.17 x the sum | passes (not the issue's definition; its noise term is a half-range and does not shrink with more solves) |

By the rule as written (a standard error over the passing solves) the move from 0.15 to 0.145 fails it, by a factor 1.3 to 2.0 depending on the form; the extra rtol 1e-13 set fails the same way (3.96e-5 against
3.2e-5 for the bound, 1.24 x). Both sets and #989's zero lie above Z14c in A by 3e-5 to 8e-5 and below it in w/w_inf by 2e-5 (not independent: the three zeros share the same dA and dw offsets, so J's noise is common to them).
The 1e-13 and 1e-14 sets differ by 2.6e-5 in A, about their standard errors. Not established: whether the shift is a dependence on xi1 (Lemma R) or the offsets' noise, which is common to all three zeros.

The standard error of the zero is dominated by J's noise once the centre has 8 solves: the J-fixed error is 2.3e-5 to 4.0e-5 and the bootstrap with J's noise 2.1e-5 to 3.6e-5 (robust). A projection of that bootstrap (not a measurement),
8 solves for each of dA and dw as well as for the centre at the same scatter, gives a robust standard error of 2.1e-5 at 1e-14 (1.6e-5 at 1e-13), and 16 of each 1.5e-5 (1.1e-5).

Control and deviations: the fast-forward to acb4b6a8 changed no bits (seed 980 at 1e-13 reproduces the earlier log, `logs/ctrl1000_diff.txt`). The offsets are from win2 (x86), the centre from rpi5 (aarch64). The driver is not
`run_repeat.py` (see above). The `m7_outer` call lists the 8 centre solves and I989-win2's two offset logs by path; `logs/m7_outer_rpi5_rtol14_xi0145.txt` has the paths with the raw-clone prefix removed.

## Recommended tasks (one line each; the coordinator files them)

1. **Offsets measured the same way.** Eight perturbed dA solves (A + 2e-4) and eight perturbed dw solves (w/w_inf + 1e-4) at xi1 0.145, rtol 1e-14, seeds 988 to 1003 and 1004 to 1019, then `m7_outer --local` with the mean offsets (or `analyze989.py` with them) so that J's noise is measured; acceptance: the zero's standard error with J's noise is at most 2.5e-5 and its distance from Z14c in units of the sum is reported, or the floor is reported. Depends on #1000.
2. **Z14c's own centre by perturbed starts at the same rtol and code,** since the comparison uses a 0.15 zero with 9.1e-6 from 3 centre solves; acceptance: eight 0.15 solves, its standard error, and the distance recomputed. Depends on #1000.
